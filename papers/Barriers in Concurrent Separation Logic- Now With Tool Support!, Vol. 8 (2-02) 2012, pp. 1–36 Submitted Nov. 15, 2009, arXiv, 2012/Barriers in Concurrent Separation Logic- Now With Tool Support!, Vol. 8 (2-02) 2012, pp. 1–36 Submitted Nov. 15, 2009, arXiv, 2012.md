Logical Methods in Computer Science
Vol. 8 (2:02) 2012, pp. 1–36                                                           Submitted      Nov. 15, 2009
www.lmcs-online.org                                                                    Published      Apr. 20, 2012




             BARRIERS IN CONCURRENT SEPARATION LOGIC:
                      NOW WITH TOOL SUPPORT!

                          AQUINAS HOBOR AND CRISTIAN GHERGHINA
     e-mail address: {hobor, cristian}@comp.nus.edu.sg

     National University of Singapore


         Abstract. We develop and prove sound a concurrent separation logic for Pthreads-style
         barriers. Although Pthreads barriers are widely used in systems, and separation logic is
         widely used for verification, there has not been any effort to combine the two. Unlike
         locks and critical sections, Pthreads barriers enable simultaneous resource redistribution
         between multiple threads and are inherently stateful, leading to significant complications
         in the design of the logic and its soundness proof. We show how our logic can be applied
         to a specific example program in a modular way. Our proofs are machine-checked in Coq.
         We showcase a program verification toolset that automatically applies the logic rules and
         discharges the associated proof obligations.




                                            1. Introduction
In a shared-memory concurrent program, threads communicate via a common memory.
Programmers use synchronization mechanisms, such as critical sections and locks, to avoid
data races. In a data race, threads “step on each others’ toes” by using the shared memory
in an unsafe manner. Recently, concurrent separation logic has been used to formally reason
about shared-memory programs that use critical sections and (first-class) locks [29, 22, 20,
21]. Programs verified with concurrent separation logic are provably data-race free.
     What about shared-memory programs that use other kinds of synchronization mech-
anisms, such as semaphores? The general assumption is that other mechanisms can be
implemented with locks, and that reasonable Hoare rules can be derived by verifying their
implementation. Indeed, the first published example of concurrent separation logic was im-
plementing semaphores using critical sections [29]. Unfortunately, not all synchronization
mechanisms can be easily reduced to locks in a way that allows for a reasonable Hoare
rule to be derived. In this paper we introduce a Hoare rule that natively handles one such
synchronization mechanism, the Pthreads-style barrier.
     Pthreads (POSIX Threads) is a widely-used API for concurrent programming, and
includes various procedures for thread creation/destruction and synchronization [9]. When
a thread issues a barrier call it waits until a specified number (typically all) of other threads
   1998 ACM Subject Classification: D.1.3 , D.2.1 D.2.4, D.4.4, F.3.1, F.3.3, F.4.1, F.4.3.
   Key words and phrases: Concurrency, Concurrent Separation Logic, Verification Tools.
   Aquinas Hobor is supported by a Lee Kuan Yew Fellowship and MOE AcRF Tier 1 #T1 251RES0902.




l    LOGICAL METHODS
     IN COMPUTER SCIENCE                DOI:10.2168/LMCS-8 (2:02) 2012
                                                                               c
                                                                               CC
                                                                                    Aquinas Hobor and Cristian Gherghina
                                                                                    Creative Commons
2                             AQUINAS HOBOR AND CRISTIAN GHERGHINA




have also issued a barrier call; at that point, all of the threads continue. Although barriers
do not get much attention in theory-oriented literature, they are very common in numerical
applications code. PARSEC is the standard benchmarking suite for multicore architectures,
and has thirteen workloads selected to provide a realistic cross-section for how concurrency
is used in practice today; a total of five (38%) of PARSEC’s workloads use barriers, covering
the application domains of financial analysis (blackscholes), computer vision (bodytrack),
engineering (canneal), animation (fluidanimate), and data mining (streamcluster) [5]. A
common use for barriers is to manage large numbers of threads in a pipeline setting. For
example, in a video-processing algorithm, each thread might read from some shared common
area containing the most recently completed frame while writing to some private area that
will contain some fraction of the next frame. (A thread might need to know what is
happening in other areas of the previous frame to properly handle objects entering or
exiting its part of the current frame.) In the next iteration, the old private areas become
the new shared common area as the algorithm continues.
     Our key insight is that a barrier is used to simultaneously redistribute ownership of
resources (typically, permission to read/write memory cells) between multiple threads. In
the video-processing example, each thread starts out with read-only access to the previ-
ous frame and write access to a portion of the current frame. At the barrier call, each
thread gives up its write access to its portion of the (just-finished) frame, and receives back
read-only access to the entire frame. Separation logic (when combined with fractional per-
missions [6, 15]) can elegantly model this kind of resource redistribution. Let Pre i be the
preconditions that held upon entering the barrier, and Post i be the postconditions that will
hold after being released; then the following equation is almost true:
                                        ∗ Pre
                                            i
                                                i       =      ∗ Post
                                                                i
                                                                        i                             (1.1)
Pipelined algorithms often operate in stages. Since barriers are used to ensure that one
computation has finished before the next can start, the barriers need to have stages as
well—a piece of ghost state associated with the barrier. We model this by building a finite
automaton into the barrier definition. We then need an assertion, written barrier(bn, π, cs),
which says that barrier bn, owned with fractional permission π, is currently in state cs.
The state of a barrier changes exactly as the threads are released from the barrier. We
can correct equation (1.1) by noting that barrier bn is transitioning from state cs (current
state) to state ns (next state), and that the other resources (frame F ) are not modified:
                            ∗ Pre                   =       F ∗ barrier(bn, , cs)
                                                                            `




                                    i
                             i                                                            (1.2)
                            ∗ Post       =        F ∗ barrier(bn, , ns)
                                                                            `




                                        i
                           i
We use the symbol to denote the full (∼100%) permission, which we require so that no
                       `




thread has a “stale” view of the barrier state. Although the on-chip (or erased) operational
behavior of a barrier is conceptually simple1, it may be already apparent that the verification
can rapidly become quite complicated.

Contributions.
(1) We give a formal characterization for sound barrier definitions.
(2) We design a natural Hoare rule in separation logic for verifying barrier calls.
    1Suspend each thread as it arrives; keep a counter of the number of arrived threads; and when all of the
threads have arrived, resume the suspended threads.
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                 NOW WITH TOOL SUPPORT!             3




(3) We give a formal resource-aware unerased concurrent operational semantics for barriers
    and prove our Hoare rules sound with respect to our semantics.
(4) Our soundness results are machine-checked in Coq and are available at:
                          www.comp.nus.edu.sg/∼hobor/barrier
(5) We extended a program verification toolchain to automatically apply our Hoare rules
    to concurrent programs using barrier synchronization and discharge the resulting proof
    obligations. Our prototype is available at:
           www.comp.nus.edu.sg/∼cristian/projects/barriers/tool.html

Relation to Previously Published Work. We previously published on the design of the pro-
gram logic and its soundness proof [24]; in §8 this presentation additionally presents our
work on the modifications to the HIP/SLEEK program verifier we developed to reason
about our logic.

             2. Syntax, Separation Algebras, Shares, and Assertions
Here we briefly introduce preliminaries: the syntax of our language, separation algebras,
share accounting, and the assertions of our separation logic.

2.1. Programming Language Syntax. To let us focus on the barriers, most of our pro-
gramming language is pure vanilla. We define four kinds of (tagged) values v: TRUE, FALSE,
ADDR(N), and DATA(N). We have two (tagged) expressions e: C(v) and V(x), where x are
local variable names (just N in Coq). To make the example more interesting we add the
arithmetical operations to e. We write bn for a barrier number, with bn ∈ N.
     We have ten commands c: skip (do nothing), x := e (local variable assignment), x := [e]
(load from memory), [e1 ] := e2 (store to memory), x:= new e (memory allocation), free e
(memory deallocation), c1 ; c2 (instruction sequence), if e then c1 else c2 (if-then-else),
while e {c} (loops), and barrier bn (wait for barrier bn). To run commands c1 . . . cn in
parallel (which, like O’Hearn, we only allow at the top level [29]), we write c1 || . . . ||cn . To
avoid clogging the presentation, we elide a setup sequence before the parallel composition.

2.2. Disjoint Multi-unit Separation Algebras. Separation algebras are mathematical
structures used to model separation logic. We use a variant described by Dockins et al.
called a disjoint multi-unit separation algebra (hereafter just “DSA”) [15]. Briefly, a DSA
is a set S and an associated three-place partial join relation ⊕, written x ⊕ y = z, such
that:
      A function:         x ⊕ y = z1 ⇒ x ⊕ y = z2 ⇒ z1 = z2
      Commutative:        x⊕y = y⊕x
      Associative:        x ⊕ (y ⊕ z) = (x ⊕ y) ⊕ z
      Cancellative:       x1 ⊕ y = z ⇒ x2 ⊕ y = z ⇒ x1 = x2
      Multiple units:     ∀x. ∃ux . x ⊕ ux = x
      Disjointness:       x⊕x=y ⇒ x=y
A key concept is the idea of an identity: x is an identity if x ⊕ y = z implies y = z. One
fundamental property of identities is that x is an identity if and only if x ⊕ x = x. Dockins
also develops a series of standard constructions (e.g., product, functions, etc.) for building
complicated DSAs from simpler DSAs. We make use of this idea to construct a variety
4                        AQUINAS HOBOR AND CRISTIAN GHERGHINA




of separation algebras as needed, usually with the concept of share as the “foundational”
DSA.

2.3. Shares. Separation logic is a logic of resource ownership. Concurrent algorithms some-
times want to have threads share some common resources. Bornat et al. introduced the
concept of fractional share to handle the necessary accounting [6]. Shares form a DSA; a full
share (complete ownership of a resource) can be broken into various partial shares; these
shares can then be rejoined into the full share. The empty share is the identity for shares.
We often need non-empty (strictly positive) shares, denoted by π. A critical invariant is
that the sum of each thread’s share of a given object is no more or less than the full share.
     The semantic meaning of partial shares varies; here we use them in two distinct ways.
We require the full share to modify a memory location; in contrast, we only require a positive
share to read from one. There is no danger of a data race even though we do not require
the full share to read: if a thread has a positive share of some location, no other thread
can have a full share for the same location. We use fractional permissions differently for
barriers: each precondition includes some positive share of the barrier itself and we require
that the preconditions combine to imply the full share of the barrier (plus a frame F ).
     In the Coq development we use a share model developed Dockins et al. that supports
sophisticated fractional ownership schemes [15]. Here we simplify this model into four




                                                                       ?
elements: the full share ; two distinct nonempty partial shares,            and    , and the
                         `




                                                                               ?
                                       ?
            




empty share . The key point is that          ⊕    = .
                                                  `
                                            ?




2.4. Assertion Language. We model the assertions of separation logic following Dockins
et al. [15]. Our states σ are triples of a store, heap, and barrier map (σ = (s, h, b)). Local
variables live in stores s (functions from variable names to values). In contrast, a heap h
contains the locations shared between threads; heaps are partial functions from addresses to
pairs of positive shares and values. We also equip our heaps with a distinguished location,
called the break, that tracks the boundary between allocated and unallocated locations.
The break lets us provide semantics for the x:= new e instruction in a natural way by
setting x equal to the current break and then incrementing the break. Since threads share
a common break, there is a covert communication channel (one thread can observe when
another thread is allocating memory); however the existence of this channel is a small price
to pay for avoiding the necessity of a concurrent garbage collector. We ensure that the
threads see the same break by equipping our break with ownership shares just as we equip
normal memory locations with shares.
     We denote the empty heap (which lacks ownership for both all memory locations and
the distinguished break location) by h0 . Of note, our expressions e are evaluated only in
the context of the store; we write s ⊢ e ⇓ v to mean that e evaluates to v in the context of
the store s. Finally, the barrier map b is a partial function from barrier numbers to pairs of
barrier states (represented as natural numbers) and positive shares; we denote the empty
barrier map by b0 .
     An assertion is a function from states to truth values (Prop in Coq). As is common, we
define the usual logical connectives via a straightforward embedding into the metalogic; for
example, the object-level conjunction P ∧Q is defined as λσ. (P σ)∧(Qσ). We will adopt the
convention of using the same symbol for both the object-level operators and the meta-level
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                      NOW WITH TOOL SUPPORT!        5




operators to avoid symbol bloat; it should be clear from the context which operator applies
in a given situation. We provide all of the standard connectives (⊤, ⊥, ∧, ∨, ⇒, ¬, ∀, ∃).
    We model the connectives of separation logic in the standard way2:
     emp                  =    λ(s, h, b). h = h0 ∧ b = b0
     P ∗Q                 =    λσ. ∃σ1 , σ2 . σ1 ⊕ σ2 = σ ∧ P (σ1 ) ∧ Q(σ2 )
         π
     e1 7−
         → e2             =    λ(s, h, b). ∃a, v. (s ⊢ e1 ⇓ ADDR(a)) ∧ (s ⊢ e2 ⇓ v) ∧




                                                                                          
                                b = b0 ∧ h(a) = (v, π) ∧ dom(h) = {a} ∧ break(h) =
     barrier(bn, π, s)    =    λ(s, h, b). h = h0 ∧ b(bn) = (s, π) ∧ dom(b) = {bn}
                                            π
The fractional points-to assertion, e1 7−  → e2 , means that the expression e1 is pointing to an
address a in memory; a is owned with positive share π, and contains the evaluated value v
of e2 . The fractional points-to assertion does not include any ownership of the break. The
barrier assertion, barrier(bn, π, s), means that the barrier bn, owned with positive share π,
is in state s.
     We also lift program expressions into the logic: e ⇓ v, which evaluates e with σ’s store
(i.e., λ(s, h, b). h = h0 ∧ b = b0 ∧ s ⊢ e ⇓ v); [e], equivalent to e ⇓ TRUE; and x = v, equivalent
to V(x) ⇓ v. These assertions have a “built-in” emp.

                                             3. Example
We present a detailed example inspired by a video decompression algorithm. The code
and a detailed-but-informal description of the barrier definition is given in Figure 1.3 Two
threads cooperate to repeatedly compute the elements of two size-two arrays x and y. In
each iteration, each thread writes to a single cell of the “current” array, and reads from
both cells of the “previous” array.
    In Figure 1 we give a pictorial representation of the state machine associated with the
barrier used in the code using the following specialized notation:




This notation is used to express the pre- and postconditions for a given barrier transition.
Each row is a pictorial representation (values, barrier states, and shares) of a formula in
separation logic as indicated above. The preconditions are on top (one per row) and the
postconditions below. Each row is associated with a move; move 1 is a pair of the first
precondition row and the first postcondition row, etc. A barrier that is waiting for n
threads will have n moves; n can be fewer than the total number of threads. We do not
require that a given thread always takes the same move each time it reaches a given barrier
transition.
  2Our Coq definition for emp is different but equivalent to the definition given here.
  3In our Coq development we give the full formal description of the example barrier.
6                      AQUINAS HOBOR AND CRISTIAN GHERGHINA




                `


                          `


                                   `


                                             `

                                                      `
    0:       {x1 7−
                  →0 ∗ x2 7−
                           →0 ∗ y1 7−
                                    →0 ∗ y2 7−
                                             →0 ∗ i7−
                                                    →0 ∗ barrier(bn, , 0 )}




                                                                        `
             ?

                        ?

                                   ?



                                                           ? ?

                                                                 ? ?

                                                                             ?
    0’:   {x1 7−−→0 ∗ x2 7−−→0 ∗ y1 7−−→0            {x1 7−−→0 ∗ x2 7−−→0 ∗ y1 7−−→0
           ?

                    ?



                                       ?
       ∗ y2 7−−→0 ∗ i7−−→0 ∗ barrier(bn,    , 0 )}   ∗ y2 7−−→0 ∗ i7−−→0 ∗ barrier(bn, , 0 )}




                                                                                       ?
          ...                                        ...
    1: barrier b;                                    barrier b; // b transitions 0→1
    2: n := 0;                                       m := 0;
    3: while n < 30 {                                while m < 30 {
    4:     a1 := [x1 ];                              a1 := [x1 ];
    5:     a2 := [x2 ];                              a2 := [x2 ];
    6:     [y1 ] := (a1 +2∗a2 );                     [y2 ] := (a1 +3∗a2 );
    7:     barrier b;                                barrier b; // b transitions 1→2
    8:     a1 := [y1 ];                              a1 := [y1 ];
    9:     a2 := [y2 ];                              a2 := [y2 ];
    10: [x1 ] := (a1 +2∗a2 );                        [x2 ] := (a1 +3∗a2 );
    11: n := (n+1);
    12: [i] := n;
    13: barrier b;                                   barrier b; // b transitions 2→1
    14:                                              m := [i];
    15: }                                            }
    16: barrier b;                                   barrier b; // b transitions 1→3
    17: [i] := 0;
          ...                                        ...




                   Figure 1: Example: Code and Barrier Diagram
       BARRIERS IN CONCURRENT SEPARATION LOGIC:                        NOW WITH TOOL SUPPORT!                 7




     Note that only the permissions on the memory cells change during a transition; the
contents (values) do not.4 The exception to this is the special column on the right side,
which denotes the assertion associated with the barrier itself. As the barrier transitions,
this value changes from the previous state to the next; we require that the sum of the
preconditions includes the full share of the barrier assertion to guarantee that no thread
has an out-of-date view of the barrier’s state. Observe that all of the preconditions join
together, and, except for the state of the barrier itself, are exactly equal to the join of the
postconditions.
     The initial state of the machine is given as an assertion in line 0. The machine starts
with full ownership of the array cells x1 , x2 , y1 , and y2 , as well as an additional cell i, used
as a condition variable. The barrier b is fully-owned and is in state 0. The initial state is
then partitioned into two parts on line 0’, with the left thread (A) and right thread (B)
                     ?




getting the shares        and , respectively.
                              ?



     Not shown (between lines 0’ and 1) is thread-specific initialization code; perhaps both
threads read both arrays and perform consistency checks. The real action starts with the
barrier call on line 1, which ensures that this initialization code has completed. Thread A
takes move 1 and thread B takes move 2. Afterwards, thread A has full ownership over
y1 and thread B has full ownership over y2 ; the ownership of x1 , x2 , and i remains split
between A and B. While the ownership of the barrier is unchanged, it is now in state 1.
     We then enter the main loop on line 3. On lines 4–5, both threads read from the shared
cells x1 and x2 , and on line 6 both threads update their fully-owned cell. The barrier call on
line 7 ensures that these updates have been completed before the threads continue. Since
the value T at memory location i is less than 30, only the 1–2 transition is possible; the 1–3
transition requires T≥ 30. Thread A takes move 1 and thread B takes move 25; afterwards,
both threads have partial shares of y1 and y2 , thread A has the full share of x1 and the
condition cell i, and thread B has the full share of x2 ; the barrier is in state 2.
     Lines 8–10 are mirrors of lines 4–6. On lines 11–12, thread A updates the condition cell
i. The barrier on line 13 ensures that the updates on lines 10 and 12 have completed before
the threads continue; thread A takes move 2 while thread B takes move 1. Afterwards, the
threads have the same permissions they had on entering the loop: A has full ownership of
y1 , B has full ownership of y2 , and they share ownership of x1 , x2 , and i; the barrier is
again in state 1.
     On line 14, thread B reads from the condition variable i, and then the program loops
back to line 3. After 30 iterations, the loop exits and control moves to the barrier on line
16. Observe that since the (shared) value T at memory location i is greater than or equal
to 30, only the 1–3 transition is possible; the 1–2 transition requires T< 30. Thread A
takes move 1 while thread B takes move 2; afterwards, both threads are sharing ownership
of x1 , x2 , y1 , and y2 (since the transition from 1 to 3 does not mention y1 and y2 they are
unchanged). Thread A has full permission over the condition variable i; the barrier is in
state 3. Finally, on line 17, thread A updates i; the barrier on line 16 ensures that thread
B’s read of i on line 14 has already occurred.
    4We use the same quantified variable names before and after the transition because an outside observer can
tell that the values are the same. A local verification can use ghost state to prove the equality; alternatively
we could add the ability to move the quantifier to other parts of the diagram, e.g., over an entire pre-post
pair.
    5In this example a given thread always takes the same move for a given transition; however, this is not
forced by the rules of our logic.
8                            AQUINAS HOBOR AND CRISTIAN GHERGHINA




         BarDef                      ≡      { bd bn : Nat                               barrier id
         (barrier definition)                bd limit : Nat                          # of threads
                                             bd states : list BarStateDef}               state list
         BarStateDef                 ≡      {bsd bn : Nat                               barrier id
         (barrier state)                     bsd cs : Nat                                 state id
                                             bsd directions : list BarMoveList      transition list
                                             bsd limit : Nat}                        # of threads
         BarMoveList                 ≡      {bml ns : Nat                               next state
         (transition)                        bml bn : Nat                               barrier id
                                             bml cs : Nat                            current state
                                             bml limit : Nat                         # of threads
                                             bml moves : list (assert × assert)}   pre/post pairs

                                     Figure 2: Barrier Definitions

                4. Barrier Definitions and Consistency Requirements
We present the type of a barrier definition in Figure 2 in the form of a data structure. The
definitions include numerous consistency requirements; in Coq these are maintained with
dependent types. From the top down, a barrier definition (BarDef) consists of a barrier
identifier (i.e., barrier number), the number of threads the barrier is synchronizing, and a
list of barrier state definitions. For programs that have more than one barrier, the individual
barrier definitions will be collected into a list and barrier number j will be in list slot j.
     A barrier state definition (BarStateDef) consists of a barrier number, the number of
threads synchronized, a state id, and a transition list; such that:
(1) the barrier number matches the barrier number in the containing BarDef
(2) the limit matches the limit of the containing BarDef 6
(3) the state identifier j indicates that this BarStateDef is the j element of the containing
     BarDef’s list of state definitions
(4) the directions are mutually exclusive
The first three are unexciting; we will discuss mutual exclusion shortly.
     A transition (BarMoveList) contains a barrier number (bn), number of threads syn-
chronized, current state identifier (cs), next state identifier (ns), and list of precondi-
tion/postcondition pairs (the move list). We require that:
(1) bn matches the barrier number in the containing BarStateDef
(2) the limit matches the limit in the containing BarStateDef
(3) cs matches the state identifier in the containing BarStateDef
(4) the length of list of moves (bml moves) is equal to the limit (bml limit)
(5) all of the pre/postconditions in the movelist ignore the store, focusing only on the
     memory and barrier map. Since stores are private to each thread (on a processor these
     would be registers), it does not make sense for them to be mentioned in the “public”
     pre/post conditions.
(6) all of the preconditions in the movelist are precise. Precision is a technical property
     involving the identifiability of states satisfying an assertion. An assertion P is precise
    6A command to dynamically alter the number of threads a barrier managed might allow different
states/transitions to wait for different numbers of threads.
       BARRIERS IN CONCURRENT SEPARATION LOGIC:                          NOW WITH TOOL SUPPORT!          9




    when
                     σ1 ⊕ σ2 = σ3    σ1 |= P      σ1′ ⊕ σ2′ = σ3  σ1′ |= P
                                            σ1 = σ1′
    That is, P can hold on at most one substate of an arbitrary state σ3 . 7
(7) each precondition P includes some positive share of the barrier assertion with bn and
    cs, i.e., ∃π. P ⇒ ⊤ ∗ barrier(bn, π, cs).
(8) the sum of the preconditions must equal the sum of the postconditions, except for the
    state of the barrier; moreover, the sum of the preconditions must include the full share
    of the barrier (equation (1.2), repeated here):
                           ∗ Pre               =          F ∗ barrier(bn, , cs)




                                                                            `
                                    i
                            i
                           ∗ Post              =          F ∗ barrier(bn, , ns)




                                                                            `
                                        i
                            i
Items 1–4 are simple bookkeeping; items 5–7 are similar to technical requirements required
in other variants of concurrent separation logic [29, 21, 20]. As previously mentioned, the
fundamental insight of this approach is property (8).
    The function lookup move simplifies the lookup of a move in a BarDef:
      lookup move(bd , cs, dir , mv ) = bd.bd states[cs].bsd directions[dir ].bml moves[mv ]
Using this notation, we can express the important requirement that all directions in the
barrier state cs of the barrier definition bd are mutually exclusive:
                         ∀dir 1 , dir 2 , mv 1 , mv 2 , pre 1 , pre 2 . dir 1 6= dir 2 ⇒
                          lookup move(bd , cs, dir 1 , mv 1 ) = (pre 1 , ) ⇒
                          lookup move(bd , cs, dir 2 , mv 2 ) = (pre 2 , ) ⇒
                          (⊤ ∗ pre 1 ) ∧ (⊤ ∗ pre 2 ) ≡ ⊥
In other words, it is impossible for any of the preconditions of more than one transition
(of a given state) to be true at a time. The simplest way to understand this is to consider
the 1–2 and 1–3 transitions in the example program. The 1–2 transition requires that the
value in memory cell i be strictly less than 30; in contrast, the 1–3 transition requires that
the same cell contains a value greater than or equal to 30. Plainly these are incompatible;
but in fact the above property is stronger: both of the moves on the 1–2 transition, and
both of the moves on the 1–3 transition include the incompatibility. Thus, if thread A takes
transition 1–2, it knows for certain that thread B cannot take transition 1–3. This way we
ensure that both threads always agree on the barrier’s current state.

                                            5. Hoare Logic
Our Hoare judgment has the form Γ ⊢ {P } c {Q}, where Γ is a list of barrier definitions
as given in §4, P and Q are assertions in separation logic, and c is a command. Our Hoare
rules come in three groups: standard Hoare logic (Skip, If, Sequence, While, Assignment,
Consequence); standard separation logic (Frame, Store, Load, New, Free); and the barrier
rule. We give all three groups two and three in Figure 3. We note four points for group
two.
   7Precision may not be required; another property (tentatively christened “token”) that might serve would
be if, for any precondition P , P ∗ P ≡ ⊥. Note that precision in conjunction with item (6) implies P is a
token.
10                         AQUINAS HOBOR AND CRISTIAN GHERGHINA




                                         Γ ⊢ {P ∗ [e]} ct {Q} Γ ⊢ {P ∗ ¬[e]} cf {Q}
                                Skip                                                If
          Γ ⊢ {P } skip {P }                  Γ ⊢ {P } if e then ct else cf {Q}


        Γ ⊢ {P } c1 {Q} Γ ⊢ {Q} c2 {R}            Γ ⊢ {I ∗ [e]} c {I}
                                       Seq.                                While
              Γ ⊢ {P } c1 ; c2 {R}          Γ ⊢ {I} while e {c} {I ∗ ¬[e]}

                                                  P ′ ⊢ P Γ ⊢ {P } c {Q} Q ⊢ Q′
                                         Assign                                 Conseq.
           Γ ⊢ {e⇓ v} x := e {x = v}                     Γ ⊢ {P ′ } c {Q′ }

            Γ ⊢ {P } c {Q} closed(F, c)                                           Store
                                        Frame




                                                          `




                                                                              `
             Γ ⊢ {F ∗ P } c {F ∗ Q}           Γ ⊢ {e1 7−
                                                       → } [e1 ] := e2 {e1 7−
                                                                            →e2 }

                      π                                          π                      Load
             Γ ⊢ {e1 7−
                      →e2 ∗ e1 ⇓ v1 ∗ e2 ⇓ v2 } x := [e1 ] {C(v1 )7−
                                                                   →C(v2 ) ∗ x = v2 }

                                                   New                                    Free
                                        `




                                                                `
          Γ ⊢ {e⇓ v} x:= new e {V(x)7−
                                     →C(v)}              Γ ⊢ {e1 7−
                                                                  →e2 } free e1 {emp}

                   Γ[bn] = bd      lookup move(bd , cs, dir , mv ) = (P, Q)
                                                                            Barrier
                                  Γ ⊢ {P } barrier bn {Q }

                                       Figure 3: Hoare rules

     First, as explained in §2.4, the assertions e ⇓ v, [e] and x = v are bundled with an
assertion that the heap and barrier map are empty(i.e., e ⇓ v ⇒ emp); thus, we use the
separating conjunction when employing them. Second, the rules are in “side-condition-free
                                                               π                              π
form”. Thus, instead of presenting the load rule as Γ ⊢ {e1 7− →e2 } x := [e1 ] {x = e2 ∗ e1 7−
                                                                                              →e2 },
which is aesthetically attractive but untrue in the pesky case when e2 depends on x (e.g.,
x := [x]), we use a form that is less visually pleasing but does not require side conditions.8
It is straightforward to restore rules with side conditions via the Consequence rule. Third,
our Store and Free rules require the full share of location e1 ; in contrast, our Load rule
only requires some positive share; this is consistent with our use of fractional permissions
as explained in §2.3. Fourth, memory allocation and deallocation are more complicated
in concurrent settings than in sequential settings, and so the New and Free rules cause
nontrivial complications in the semantic model.
     The Hoare rule for barriers is so simple that at first glance it may be hard to understand.
The variables for the current state cs, direction dir , and move mv appear to be free in the
lookup move! However, things are not quite as unconstrained as they initially appear. Recall
from §4 that one of the consistency requirements for the precondition P is that P implies
an assertion about the barrier itself: P ⇒ Q ∗ barrier(bn, π, cs); thus at a given program
point we can only use directions and moves from the current state. Similarly, recall from
§4 that since the directions are mutually exclusive, dir is uniquely determined.
   8Recall from §2: V(x) and C(v) are expression constructors for locals and constants.   In addition,
closed(F, c) means that F does not depend on locals modified by c.
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                 NOW WITH TOOL SUPPORT!            11




     This leaves the question of the uniqueness of mv . If a thread only satisfies a single
precondition, then the move mv is uniquely determined. Unfortunately, it is simple to
construct programs in which a thread enters a barrier while satisfying the preconditions of
multiple moves. What saves us is that we are developing a logic of partial correctness. Since
preconditions to moves must be precise and nonempty (i.e., token), only one thread is able to
satisfy a given precondition at a time. The pigeonhole principle guarantees that if a thread
holds multiple preconditions then some other thread will not be able to enter the barrier;
in this case, the barrier call will never return and we can guarantee any postcondition.
     We now apply the Barrier rule to the barrier calls in line 13 from our example program;
the lookup moves are direct from the barrier state diagram:
                
                
                                    lookup move(b, 2, 1, 2) = (P, Q)
                
                           ?


                                        ?
                




                                                     `


                                                               `
                




                                                                                 ? ?
                 P = y 7−−→v ∗ y 7−−→v ∗ x 7−
                                                     1 →vx1 ∗ i7−
                                                                →vi ∗barrier(bn, , 2 )
                
                           1     y1     2     y2
     Thread A
                                      ?


                                                    ?

                                                               ?
                          `




                   Q = y1 7−→vy1 ∗ x1 7−−→vx1 ∗ x2 7−−→vx2 ∗ i7−−→vi ∗barrier(bn, , 1 )
                
                
                
                
                
                
                                         Γ ⊢ {P } barrier b {Q}
                
                
                                     lookup  move(b, 2, 1, 1) = (P, Q)
                
                                                         `
                               ?


                                            ?


                
                        P = y1 7−−→vy1 ∗ y2 7−−→vy2 ∗ x2 7−→vx2 ∗barrier(bn, , 2 )}
                




                                                                            ?
                
     Thread B
                          `


                                      ?


                                                   ?

                                                               ?
                
                   Q = y2 7−→vy2 ∗ x1 7−−→vx1 ∗ x2 7−−→vx2 ∗ i7−−→vi ∗barrier(bn, , 1 )}
                




                                                                                 ?
                
                
                
                
                                          Γ ⊢ {P } barrier b {Q}
                

Note that in this line of the example program, the frame is emp in both threads.
    Not shown in Figure 3 is a parallel composition rule. As in [21], each thread is verified
independently using the Hoare rules given; a top-level safety theorem proves that the entire
concurrent machine behaves as expected.

                                     6. Semantic Models
Our operational semantics is divided into three parts: purely sequential, which executes all
of the instructions except for barrier in a thread-local manner; concurrent, which manages
thread scheduling and handles the barrier instruction; and oracular, which provides a pseu-
dosequential view of the concurrent machine to enable simple proofs of the sequential Hoare
rules. Our setup follows Hobor et al. very closely and we refer readers there for more detail
[22, 21].

Purely sequential semantics. The purely sequential semantics executes the instructions skip,
x := e, x := [e], [e1 ] := e2 , x:= new e, free e, c1 ; c2 , if e then c1 else c2 , and while e {c}.
The form of the sequential step judgment is (σ, c) 7→ (σ ′ , c′ ). Here σ is a state (triple of
store, heap, barrier map), just as in §2.4 and c is a command of our language. The semantics
of the sequential instructions is standard; the only “tricky” part is that the machine gets
stuck if one tries to write to a location for which one does not have full permission or read
from a location for which one has no permission; e.g., here is the store rule:
                      s ⊢ e1 ⇓ C(ADDR(n))        s ⊢ e2 ⇓ v
             n < break(h)       h(n) = ( , v ′ )   h′ = [n 7→ ( , v)]h
                                        `




                                                               `




                                                                       sstep − store
                    (s, h, b), [e1 ] := e2 ; c 7→ (s, h′ , b), c
                                                               
12                             AQUINAS HOBOR AND CRISTIAN GHERGHINA




The test that n < break(h) ensures that the address for the store is “in bounds”—that is,
less than the current value of the break between allocated and unallocated memory; since
we are updating the memory we require that the permission associated with the location n
be full ( ). We say that this step relation is unerased since these bounds and permission
          `


checks are virtual rather than on-chip.
     We define the other cases of the step relation in a similar way. Observe that if we
were in a sequential setting the proof of the Hoare store rule would be straightforward; this
is likewise the case for the other cases of the sequential step relation and their associated
Hoare rules. If the sequential step relation reaches a barrier call barrier bn then it simply
gets stuck.

Concurrent semantics. We define the notion of a concurrent state in Figure 4. A concurrent
state contains a scheduler Ω (modeled as a list of natural numbers), a distinguished heap
called the allocation pool, a list of threads, and a barrier pool 9 . The allocation pool “owns”
all of the unallocated memory cells and the “break” that indicates the division between
allocated and unallocated cells. Before we run a thread we transfer the allocation pool into
the local heap owned by the thread so that new can transfer a cell from this pool into the
local heap of a thread when required. When we suspend the thread we remove (what is left
of) the allocation pool from its heap so that we can transfer it to the next thread.
     A thread contains a (sequential) state (store, heap, and barrier map) and a concurrent
control, which is either Running(c), meaning the thread is available to run command c, or
Waiting(bn, dir , mv , c), meaning that the thread is currently waiting on barrier bn to make
move mv in direction dir ; after the barrier call completes the thread will resume running
with command c.
     The barrier pool (Barpool) contains a list of dynamic barrier statuses (DBSes) as well
as a state which is the join of all of the states inside the DBSes. Each DBS consists of a
barrier number (which must be its index into the array of its containing Barpool), a barrier
definition (from §4), and a waitpool (WP). A waitpool consists of a direction option (None
before the first barrier call in a given state; thereafter the unique direction for the next
state), a limit (the number of threads synchronized by the barrier, and comes from the
barrier definition in the enclosing DBS), a slot list, and a state (which is the join of all of
the states in the slot list). A slot is a heap and barrier map (the store is unneeded since
barrier pre/postconditions ignore it) as well as a thread id (whence the heap and barrier
map came as a precondition, and to which the postcondition will return).
     The concurrent step relation has the form (Ω, ap, thds, bp) ❀ (Ω′ , ap ′ , thds ′ , bp ′ ), where
Ω, ap, thds, and bp are the scheduler, allocation pool, thread list, and barrier pool respec-
tively. The concurrent step relation has only four cases; the following case CStep-Seq is
used to run all of the sequential commands:
                                              h ⊕ ap = h′         (s, h′ , b), c 7→ (s′ , h′′ , b), c′
                                                                                                      
       thds[i] = (s, h, b, Running(c))
       h′′′ ⊕ ap ′ = h′′     isAllocPool(ap ′ )     thds ′ = [i 7→ (s′ , h′′′ , b, Running(c′ ))]thds
                            (i :: Ω, thds, ap, bp) ❀ (i :: Ω, thds ′ , ap ′ , bp)          CStep-Seq
     9There is also a series of consistency requirements such as the fact that all of the heaps in the threads
and barrier pool join together with the allocation pool into one consistent heap; in the mechanization this is
carried around via a dependent type as a fifth component of the concurrent state. We elide this proof from
the presentation.
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                NOW WITH TOOL SUPPORT!           13




     Cstate            ≡     { cs sched : list N                                    schedule
                              cs allocpool : heap                                  alloc pool
                              cs thds : list Thread                              thread pool
                              cs barpool : Barpool}                              barrier pool
     Thread            ≡     { th stk : store
                              th hp : heap
                              th bs : BarrierMap                 local view of barrier states
                              th ctl : conc ctl}                          running or waiting
     conc ctl          ≡     | Running(c)                                   executing code c
                             | Waiting(bn, dir, mv, c)                         waiting on bn
     Barpool           ≡     { bp bars : list DyBarStatus            dynamic barrier status
                              bp st : store × heap × BarrierMap}                current state
     DyBarStatus       ≡     { dbs bn : N                                          barrier id
                              dbs wp : Waitpool                          waiting thread pool
                              dbs bd : BarDef}
     Waitpool          ≡     { wp dir : option N                                 direction id
                              wp slots : option (list slot)                       taken slots
                              wp limit : N
                              wp st : store × heap × BarrierMap}                current state
     slot              ≡     (thread id × heap × BarrierMap)                     waiting slot

                                  Figure 4: Concurrent state

That is, we look up the thread whose thread id is at the head of the scheduler, join in the
allocation pool, and run the sequential step relation. If the command c is a barrier call
then the sequential relation will not be able to run and so the CStep-Seq relation will not
hold; otherwise the sequential step relation will be able to handle any command. After
we have taken a sequential step, we subtract out the (possibly diminished) allocation pool,
and reinsert the modified sequential state into the thread list. Since we quantify over all
schedulers and our language does not have input/output, it is sufficient to utilize a non-
preemptive scheduler; for further justification on the use of such schedulers see [21].
     The second case of the concurrent step relation handles the case when a thread has
reached the last instruction, which must be a skip:
                              thds[i] = Running(skip)
                                                                CStep-Exit
                     (i :: Ω, thds, ap, bp) ❀ (Ω, thds, ap, bp)
When we reach the end of a thread we simply context switch to the next thread.
    The interesting cases occur when the instruction for the running thread is a barrier call;
here the CStep-Seq rule does not apply. The concurrent semantics handles the barrier call
directly via the last two cases of the step relation; before presenting these cases we will first
14                          AQUINAS HOBOR AND CRISTIAN GHERGHINA




give a technical definition called fill barrier slot:
                 thds[i] = Thread(stk, hp, bs, (Running (barrier bn; c)))
                     lookup move(bp.bp bars[bn], dir, mv) = (pre, post)
                 hp′ ⊕ hp′′ = hp        bs′ ⊕ bs′′ = bs       pre(stk, hp′ , bs′ )
                   bp inc waitpool (bp, bn, dir, mv, (i, (hp′ , bs′ ))) = bp′
          thds′ = [i → (Thread( stk, hp′′ , bs′′ , (Waiting (bn, dir, mv, c))))] thds
                          fill barrier slot (thds, bp, bn, i) = (thds′ , bp′ )
The predicate fill barrier slot gives the details of removing the (sub)state satisfying the pre-
condition of the barrier from the thread’s state, inserting it into the barrier pool, and
suspending the calling thread. The predicate bp inc waitpool does the insertion into the
barrier pool; the details of manipulating the data structure are straightforward but lengthy
to formalize10.
     We are now ready to give the first case for the barrier, used when a thread executes a
barrier but is not the last thread to do so:
                fill barrier slot (thds, bp, bn, i) = (thds′ , bp′ )
                                ¬ bp ready (bp′ , bn)
                                                                     CStep-Suspend
                    ((i :: Ω), ap, thds, bp) ❀ (Ω, ap, thds′ , bp′ )
After using fill barrier slot, CStep-Suspend checks to see if the barrier is full by counting the
number of slots that have been filled in the appropriate wait pool by using the bp ready
predicate, and then context switches.
    If the barrier is ready then instead of using the CStep-Suspend case of the concurrent
step relation, we must use the CStep-Release case:
                 fill barrier slot (thds, bp, bn, i) = (thds′ , bp′ )
                                  bp ready (bp′ , bn)
                          bp transition (bp′ , bn, out) = bp′′
                       transition threads (out, thds′ ) = thds′′
                                                                        CStep-Release
                   ((i :: Ω), ap, thds, bp) ❀ (Ω, ap, thds′′ , bp′′ )
The first requirement of CStep-Release is exactly the same as CStep-Suspend: we suspend
the thread and transfer the appropriate resources to the barrier pool. However, now all of
the threads have arrived at the barrier and so it is ready. We use the bp transition predicate
to go through the barrier’s slots in the waitpool, combine the associated heaps and barrier
maps, redivide these resources according to the barrier postconditions, and remove the
associated resources from the barrier pool into a list of slots called out. Finally, the states
in out are combined with the suspended threads, which are simultaneously resumed by the
transition threads predicate. The formal definitions of the bp transition and transition threads
predicates are extremely complex and very tedious and we refer interested readers to the
mechanization.

   10In Coq things are trickier since we track some technical side conditions via dependent types so this
relation also ensures that these side conditions remain satisfied.
       BARRIERS IN CONCURRENT SEPARATION LOGIC:                     NOW WITH TOOL SUPPORT!              15




Oracle semantics. Following Hobor et al. [22, 21], we define a third oracular semantics:
(σ, o, c) 7→ (σ ′ , o′ , c′ ). Here the sequential state σ and command c are exactly the same as in
the purely sequential step. The new parameter o is an oracle, a kind of box containing “the
rest” of the concurrent machine—that is, o contains a scheduler, a list of other threads, and
a barrier pool.
     The oracle semantics behaves exactly the same way as the purely sequential semantics
on all of the instructions except for the barrier call, with the oracle o being passed through
unchanged. That is to say:
                                             σ, c 7→ σ ′ , c′
                                                             
                                                                  os-seq
                                          σ, o, c 7→ σ ′ , o, c′
                                                 

When the oracle semantics reaches a barrier instruction, it consults the oracle o to determine
the state of the machine after the barrier:
                              consult(h, b, o) = (h′ , b′ , o′ )
                                                                       os-consult
                  (s, h, b), o, barrier bn; c 7→ (s, h′ , b′ ), o′ , c
                                               

The formal definition of the consult relation is detailed in [22, 21] but the idea is simple.
To consult the oracle, one unpacks the concurrent machine and runs (classically) all of the
other threads until control returns to the original thread; consult then returns the current h′
and b′ (that resulted from the barrier call) and repackages the concurrent machine into the
new oracle o′ . The final case of the oracle semantics occurs when the concurrent machine
never returns control (because it got stuck or due to sheer perversion of the scheduler):
                 6∃r. consult(h, b, o) = r  (i.e., consult diverges)
                                                                       os-diverge
             (s, h, b), o, barrier bn; c 7→ (s, h, b), o, barrier bn; c
When control will never return, it does not matter what this thread does as long as it does
not get stuck; accordingly we enter an (infinite) loop.

Soundness proof outline. Our soundness argument falls into several parts. We define our
Hoare tuple in terms of our oracle semantics using a definition by Appel and Blazy [3];
this definition was designed for a sequential language and we believe that other standard
sequential definitions for Hoare tuples would work as well11. We then prove (in Coq) all of
the Hoare rules for the sequential instructions; since the os-seq case of the oracle semantics
provides a straight lift into the purely sequential semantics this is straightforward12.
     Next, we prove (in Coq) the soundness for the barrier rule. This turns out to be much
more complicated than a proof of the soundness of (non-first-class) locks and took the bulk
of the effort. There are two points of particular difficulty: first, the excruciatingly painful
accounting associated with tracking resources during the barrier call as they move from a
source thread (as a precondition), into the barrier pool, and redistribution to the target
thread(s) as postcondition(s). The second difficulty is proving that a thread that enters a
barrier while holding more than one precondition will never wake up; the analogy is a door
    11We change Appel and Blazy’s definition so that our Hoare tuple guarantees that the allocation pool is
available for verifying the Hoare rule for x:= new e.
    12
       The Hoare rule for loops (While) is only proved on paper. The loop rule is known to be painful
to mechanize and so the mechanization was skipped due to time constraints. It has been proved in Coq
for similar (indeed, more complicated from a sequential control-flow perspective) settings in previous work
[3, 22].
16                        AQUINAS HOBOR AND CRISTIAN GHERGHINA




with n keys distributed among n owners; if an owner has a second key in his pocket when
he enters then one of the remaining owners will not be able to get in.
     After proving the Hoare rules from Figure 3 sound with respect to the oracle semantics,
the remaining task is to connect the oracle semantics to the concurrent semantics—that
is, oracle soundness. Oracle soundness says that if each of the threads on a machine are
safe with respect to the oracle semantics, then the entire concurrent machine combining the
threads together is safe. The (very rough) analogy to this result in Brookes’ semantics is
the parallel decomposition lemma. Here we use a progress/preservation style proof closely
following that given in [21, pp.242–255]; the proof was straightforward and quite short
to mechanize. A technical advance over previous work is that the progress/preservation
proofs do not require that the concurrent semantics be deterministic. In fact, allowing the
semantics to be nondeterministic simplified the proofs significantly.
     A direct consequence of oracle soundness is that if each thread is verified with the Hoare
rules, and is loaded onto a single concurrent machine, then if the machine does not get stuck
and if it halts then all of the postconditions hold.

Erasure. One can justly observe that our concurrent semantics is not especially realistic; e.g.,
we: explicitly track resource ownership permissions (i.e., our semantics is unerased); have
an unrealistic memory allocator/deallocator and scheduler; ignore issues of byte-addressable
memory; do not store code in the heap; and so forth. We believe that we could connect our
semantics to a more realistic semantics that could handle each of these issues, but most of
them are orthogonal to barriers. For brevity we will comment only on erasing the resource
accounting since it forms the heart of our soundness result.
     We have defined, in Coq, an erased sequential and concurrent semantics. An erased
memory is simply a pair of a break address and a total function from addresses to values.
The run-time state of an erased barrier is simply a pair of naturals: the first tracking the
number of threads currently waiting on the barrier, and the second giving the final number
of threads the barrier is waiting for. We define a series of erase functions that take an
unerased type (memory/barrier status/thread/etc.) to an erased one by “forgetting” all
permission information. The sequential erased semantics is quite similar to the unerased
one, with the exception that we do not check if we have read/write permission before exe-
cuting a load/store. The concurrent erased semantics is much simpler than the complicated
accounting-enabled semantics explained above since all that is needed to handle the barrier
is incrementing/resetting a counter, plus some modest management of the thread list to sus-
pend/resume threads. Critically, our erased semantics is a computable function, enabling
program evaluation. Finally, we have proved that our unerased semantics is a conservative
approximation to our erased one: that is, if our unerased concurrent machine can take a step
from some state Σ to Σ′ , then our erased machine takes a step from erase(Σ) to erase(Σ′ ).

                                   7. Coq Development
We detail our Coq development in Figure 5. We use the Mechanized Semantic Library [1]
for the definitions of share models, separation algebras, and various utility lemmas/tactics.
In addition to the standard Coq axioms, we use dependent and propositional extensionality
and the law of excluded middle.
     Over 7,000 lines of the development is devoted to proving the soundness of the Hoare
rule for barriers, largely in the files SLB BarDefs.v, SLB CLang.v, SLB Sem.v, SLB OSem.v,
      BARRIERS IN CONCURRENT SEPARATION LOGIC:              NOW WITH TOOL SUPPORT!          17




       File             LOC Time                    Description
       SLB Base         1,182 2s       Utility lemmas (largely list facts)
       SLB Lang        1,240   11s  States, program syntax, assertion model
       SLB BarDefs       265    2s              Barrier definitions
       SLB CLang       3,230 1m7s           Dynamic concurrent state
       SLB SSem          415   17s            Sequential semantics
       SLB Sem           784   33s            Concurrent semantics
       SLB ESSem         230    5s              Erased semantics
       SLB ESEquiv     3,352   30s                Erasure proofs
       SLB OSem        1,942 2m10s             Oracular semantics
       SLB HRules        170    2s          Definition of Hoare tuples
       SLB OSound        426   30s       Soundness of oracle semantics
       SLB HRulesSound 1,664 1m14s     Soundness proofs for Hoare rules
       SLB Ex          2,700   48s      Example of a barrier definition
       Total           16,598 7m34s

          Figure 5: Proof structure, size and compilation times (2.66GHz, 8GB)

SLB HRules.v, and a small part of SLB HRulesSound.v. The rest of the concurrent se-
mantics, the oracle semantics, and the soundness of the oracle semantics (∼the parallel
decomposition lemma) require approximately 1,000 lines, largely in the files SLB Sem.v,
SLB HRules.v, and SLB OSound. The erased semantics requires 230 lines in SLB ESSem.v,
while the associated equivalence proofs require 3352 lines in the file SLB ESEquiv.v.
    The sequential semantics and proofs for the associated Hoare rules require approx-
imately 2,000 lines drawn from the files SLB Lang.v, SLB SSem.v, SLB HRules.v, and
SLB HRulesSound.v. We estimate that the proof of the loop rule would require a fur-
ther 2,000-3,000 lines. The model of our assertions and the program syntax are both in
SLB Lang.v. Utility lemmas/tactics (SLB Base.v) and the example barrier (SLB Ex.v) com-
plete the development.

                                     8. Tool support
We have integrated our program logic for barriers into the HIP/SLEEK program verification
toolset [27, 17]. SLEEK is an entailment checker for separation logic and HIP applies
Hoare rules to programs and uses SLEEK to discharge the associated proof obligations. We
proceeded as follows:
(1) We developed an equational solver over the sophisticated fractional share model of
    Dockins et al. [15]. Permissions can be existentially or universally quantified and
    arbitrarily related to permission constants.
(2) We integrated our equational solver over shares into SLEEK to handle fractional permis-
    sions on separation logic assertions (e.g., points-to, etc.). We believe that SLEEK is the
    first automatic entailment checker for separation logic that can handle a sophisticated
    share model (although some other tools can handle simpler share models).
(3) We developed an encoding of barrier definitions (diagrams) in SLEEK, which now au-
    tomatically verifies the side conditions from §4.
18                         AQUINAS HOBOR AND CRISTIAN GHERGHINA




(4) We modified HIP to recognize barrier definitions (whose side conditions are then verified
     in SLEEK) and barrier calls using the Hoare rule from Figure 3.
Next we describe our equational solver for the Dockins et al. share model before giving a
more technical background to the HIP/SLEEK system and describing our modifications to
it in detail. Most of the technical work occurred in developing the equational solver and
its integration with the rest of the separation logic entailment procedures in SLEEK. Once
SLEEK understood fractional permissions, checking the validity side conditions on barriers
was quite simple.

8.1. Decision Procedure for Shares. SLEEK discharges the heap-related proof obliga-
tions but relies on external decision procedures for the pure logical fragments it extracts
from separation logic formulae. For example, SLEEK utilizes Omega for Presburger arith-
metic, Redlog for arithmetic in R, and MONA for monadic second-order logic. Adding
fractional permissions required an appropriate equational decision procedure for fractional
shares.
     Decision procedures for simple fraction share models such as rationals between 0 and 1
need only solve systems of linear equations. The more sophisticated fractional share model
of Dockins et al. [15] requires a more sophisticated solver.
     Dockins et al. represent shares as binary trees with boolean-valued leaves. The full

                                                                   
share is a tree with one true leaf • and the empty share        is a tree with one false leaf
     `




                        ?




◦. The left-half share     is a tree with two leaves, one true and one false: • ◦; similarly,
the right-half share     is a tree with two leaves, one false and one true: ◦ •. The trees can
                     ?




                                                                    ?
continue to be split indefinitely: for example, the right half of       . Joining is defined
                                                                         is
                                                                   ◦•◦
by structural induction on the shape of the trees with base cases ◦ ⊕ ◦ = ◦, • ⊕ ◦ = •, and
◦ ⊕ • = • (emphasis: ⊕ is partial). When two trees do not have the same shape, they are
                                  = • • and ◦ ∼
unfolded according to the rules • ∼           = ◦ ◦; for example:
                 ⊕              =               ⊕              =                =
          ◦•◦          •◦◦•           ◦•◦◦          •◦◦•            ••◦•             •◦•
     SLEEK takes a formula in separation logic with fractional shares and extracts a spe-
cialized formula over strictly positive shares whose syntax is as follows:
               φ ::= ∃v.φ | φ1 ∨ φ2 | φ1 ∧ φ2 | v1 ⊕ v2 = v3 | v1 = v2 | v = χ
Our share formulae φ contain share variables v, existentials ∃, conjunctions ∧, disjunctions
∨, join facts ⊕, equalities between variables, and assignments of variables to constants χ.
The tool also recognizes v∈[χ1 , χ2 ], pronounced “v is bounded by χ1 and χ2 ”, which is
semantically equal to:
             ((v = χ1 ) ∨ (∃v ′ . χ1 ⊕ v ′ = v)) ∧ ((v = χ2 ) ∨ (∃v ′′ . v ⊕ v ′′ = χ2 ))
Disjunctions are needed because share variables can only be instantiated with positive
shares: ∀v. 6 ∃v ′ .v ⊕ v ′ = v. Handling bounds checks “natively” rather than compiling them
into semantic definitions increases efficiency by reducing the number of existentials and
disjunctions.
     SLEEK asks the solver questions of the following forms:
(1) (UNSAT) Is a given formula φ unsatisfiable?
      BARRIERS IN CONCURRENT SEPARATION LOGIC:               NOW WITH TOOL SUPPORT!           19




(2) (∃-ELIM) Given a formula of the form ∃v. φ(v), is there a unique constant χ such that
     ∃v. φ(v) is equivalent to φ(χ)?
(3) (IMPL) Given two formulae φ1 and φ2 , does φ1 entail φ2 ?
Our solver is sound but incomplete. However, it is complete enough to help SLEEK check
a wide variety of entailments involving fractional permissions, including all of those in the
example from Figure 1.
      All of these questions can be reduced to solving a series of constraint systems whose
equations are of the form v1 ⊕ v2 = v3 , v∈[χ1 , χ2 ], and v = χ. Solving constraint systems in
separation algebras (i.e., cancellative partial commutative monoids) is not as straightfor-
ward as it might seem because many of the traditional algebraic techniques do not apply.
Our lightweight constraint solver finds an overapproximation to the solution, returning ei-
ther (a) the constant UNSAT or (b) for each variable vi either an assignment vi = χ or a
bound vi ∈ [χ1 , χ2 ] such that:
• (FALSE) If the algorithm returns UNSAT, then the formula is unsatisfiable. The algorithm
   will return UNSAT if it discovers a bound whose “lower value” is higher than its “upper
   value”, or if it discovers a falsehood (e.g., after constant propagation one of the equations
   becomes ⊕ = ).
          `
               `
                   `




• (COMPLETE) All solutions to the system (if any) lie within the bounds.
• (SAT-PRECISE) A solution is precise when all variables are given assignments. If a
   solution is precise, then the formula is satisfiable.
SLEEK queries are given in share formulae that must be transformed into the equational
systems understood by our constraint solver. To do this transformation, first we put the
relevant formulae into disjunctive normal form (DNF). Each disjunct becomes an indepen-
dent system of equations. Given one disjunct we form this system by simply treating each
basic constraint (i.e., v = v ′ , v = χ, v ∈ [χ1 , χ2 ], and v1 ⊕ v2 = v3 ) as an equation. Our
solver approximates each system independently and can then answer SLEEK’s questions as
follows:
• (UNSAT): Return False when the algorithm returns UNSAT for each constraint system
   obtained from the formula; otherwise return True.
• (∃-ELIM): If the variable v has the same assignment in all constraint systems derived
   from the DNF, then return that value. It is sound to substitute that value for v and
   eliminate the existential. (If the formula is satisfiable, then that is the unique assignment
   that makes it so; if the formula is false then after the assignment it will still be false.)
• (IMPL): Return True only when either:
   − the solver returns UNSAT for all systems derived from the antecedent
   − the solver returns a precise solution for each system of equations derived from the
       antecedent, and the solver also returns the same precise solution for at least one of
       the consequent systems.
      The constraint solver works by eliminating one class of constraints at a time:
(1) First we substitute v = χ constraints into the remaining equations.
(2) We handle ⊕ constraints with exactly one variable as follows:
     • χ1 ⊕ χ2 = v: we check if the join is defined, and if so substitute the sum for v in the
        remaining equations; otherwise, we return UNSAT.
     • χl ⊕ v = χr or v ⊕ χl = χr : we check if χr contains χl , and if so substitute the
        difference χr − χl for v in the remaining equations; otherwise return UNSAT. (“−” has
        the property that if χ1 − χ2 = χ3 then χ3 ⊕ χ2 = χ1 ).
20                        AQUINAS HOBOR AND CRISTIAN GHERGHINA




(3) Constraints involving constants (χ1 ⊕ χ2 = χ3 and χ∈[χ1 , χ2 ]) are dismissed if the
    equality/inequalities hold; otherwise return UNSAT.
(4) We attempt to dismiss certain kinds of unsatisfiable systems via a consistency check as
    follows. We first compute the transitive closure of variable substitutions, resulting in
    facts of the form v1 ⊕ . . . ⊕ vn ⊕ χ1 ⊕ . . . ⊕ χm = χ. Nonempty shares cannot join with
    themselves. Therefore, if the vi contain duplicates we return UNSAT. We also return
    UNSAT if the constants χi do not join or if χ does not contain χ1 ⊕ . . . ⊕ χm .




                                                                          
(5) Variables in the remaining constraints are given initial domains of ( , ).




                                                                             `
(6) Each ∈ constraint is used to restrict the domain of its corresponding variable.
(7) At this point only a1 ⊕ a2 = a3 constraints involving at least two variables remain. The
    algorithm then proceeds by iteratively selecting an equation, checking it for consistency,
    and then refining the associated domains via a forward and backward propagation. The
    algorithm iterates until either a fixpoint is reached or a consistency check fails. To check
    an equation for consistency, the algorithm verifies that:
    • for each variable, the lower bound is less than the upper bound
    • the current lower bounds of the LHS variables join together
    • the join of the LHS lower bounds is below the RHS upper bound
    • the join of the LHS upper bounds is above the RHS lower bound
    Forward propagation consists of (Fa) lowering the upper bound of the RHS by intersect-
    ing away any subtree that does not appear in the upper bounds of the LHS, and (Fb)
    increasing the lower bound of the RHS by unioning all subtrees present in the lower
    bounds in the LHS. Backwards propagation consists of (Ba) lowering the upper bounds
    of the LHS by intersecting away any subtree that does not appear in the upper bound
    on the RHS. Increasing the lower bounds of the LHS (Bb) is trickier since we do not
    know which operand should be increased. There are several possibilities we could have
    taken, but we selected the simplest: we simply leave the bounds as they were unless one
    of the operands has been determined to be a constant, in which case we can calculate
    exactly what the lower bound for the other variable should be. This solution is can
    lead to overapproximation, but a more refined solution would require a performance
    cost, which did not seem warranted by our experiments. After each forward/backwards
    propagation, if we have refined a domain to a single point, the variable is substituted
    for a constant value of that point in the remaining equations.
            Once we reach a fixpoint, the resulting variable bounds represent an over ap-
    proximation of the solution.

8.2. An introduction to SLEEK. SLEEK checks entailments in separation logic [28].
The antecedent may cover more of the heap than the consequent, in which case SLEEK
returns this residual heap together with the pure portion of the antecedent. SLEEK can
also discover instantiations for certain existentials in the consequent, a feature that we elide
here; details may be found in Chin et al. [12].
     One of SLEEK’s strong points is that it allows user-defined inductive predicates. Pred-
icates are defined as separation formulae that describe the shape of data structures and
associated properties (e.g., list length, tree height, and bag of values contained in a list).
SLEEK uses the keyword self as a pointer variable to the current object. Predicate invari-
ants can increase the precision of the verification (e.g., length ≥ 0). An invariant for a
predicate instance has two parts: a pure formula describing arithmetic constraints on the
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                          NOW WITH TOOL SUPPORT!             21




        Predicate            spred    ::=   [self::]chv ∗ i ≡ Q [inv (π, v ∗ )]
        Formula                  Q    ::=   R|R∨Q
                                                            +
                                  R   ::=   case{[π→Q]
                                            W                 } | Φ [Q]                   W
                                                     ∗
                                 Φ    ::=     i (∃vi · (κi ∧ πi ∧ τi ))          ∆ ::= i (κi ∧ πi ∧ τi )
        Frac form.                τ   ::=   vf ⊕ vf = vf | v∈[χ, χ] | v = χ | τ ∧ τ
        Pure form.                π   ::=   γ∧φ
        Pointer form.             γ   ::=   v = v | v = null | v 6= v | v 6= null | γ ∧ γ
        Heap form.                κ   ::=   emp | v :: cvf hv ∗ i | κ∗κ
        Presburger arith.         φ   ::=   arith | φ ∧ φ | φ ∨ φ | ¬φ | ∃v · φ | ∀v · φ
                              arith   ::=   a = a | a 6= a | a < a | a ≤ a
                                  a   ::=   z | v | z × a | a + a | −a | max(a, a) | min(a, a)
                     where     v, w   are variable names;
                                c     is a data type name or a predicate name;
                                z     is an integer constant;
                                τ     represents the fractional permission constraints
                                χ     represents constant fractional shares


           Figure 6: The Specification Language with Fractional Permissions.

arguments and the set of non null pointer arguments (e.g. the outward pointer for a list
segment).
      Figure 6 gives an outline of the specification language accepted by SLEEK with our
extensions for the fractional permissions. The system accepts disjunctive separation logic
formulae (Φ) with both heap (κ) and pure (π) constraints; we denote the disjunction by
W
   . The syntax allows richer structures as well, e.g. directed case analysis and staged
formulae (corresponding to the Φ [Q] form) as described in [17]. Staged formulae help
split implication proofs into stages such that redundant proving is eliminated and ensure
that key constraints are proven early, e.g., before applying case analysis. In order to prove
that Φ [Q] holds, Φ is proven before Q is proven.
      At the core of a separation logic formula are the heap constraints. Heap constraints
are heap node descriptions connected by the separating conjunction. A node is either an
instance of a data structure or an instance of a user-defined predicate. Here we use the same
notation for both cases: v :: chv ∗ i, where v is the pointer to the structure, c is the data
structure type or predicate name, and v ∗ is the list of arguments (either predicate arguments
for predicate instances or field values for data structures). Separation logic formulae can
also contain pure constraints over several domains: arithmetic, bag/list, etc. For brevity
we discuss only arithmetic constraints in this presentation.
      The syntax in Figure 6 contains two new extensions to SLEEK’s language. First, heap
node descriptions can contain permission annotations for fractional ownership. A heap
node partially-owned with share vf is indicated by v :: cvf hv ∗ i. If c denotes a predicate,
then the notation v :: cvf hv ∗ i indicates that v points to a memory region whose shape is
described by the definition of c. Furthermore this notation denotes that all heap nodes
                                                                                                    ?




abstracted by this predicate instance are owned with permission vf (e.g., in a            -owned
                             ?




list, each list cell is owned ). A node/predicate without a permission annotation indicates
full ownership. The second extension enables the expression of constraints over fractional
permission variables using the syntax vf 1 ⊕ vf 2 = vf 3 , v∈[χ1 , χ2 ], v1 = v2 , and v = χ.
22                        AQUINAS HOBOR AND CRISTIAN GHERGHINA




                                     XPure(emp) ≡ (true, ∅)

                                            IsData(c)
                                 XPure(p :: chv ∗ i) ≡ (p6=0; {p})

                        IsPred(c)       (chv ∗ i ≡ Q inv (π1 , π2 )) ∈ P
                   XPure(p :: chvp i) ≡ ([p/self, vp∗ /v ∗ ]π1 , [p/self, vp∗ /v ∗ ]π2 )
                                 ∗


                        XPure(κ1 ) ≡ (f1 , s1 ) XPure(κ2 ) ≡ (f2 , s2 )
                             XPure(κ1 ∗κ2 ) ≡ (f1 ∧ f2 , s1 ∪ s2 )


                        Figure 7: XPure : Translating to Pure Form

8.3. SLEEK entailment background. The core of the SLEEK entailment works by
algorithmically discharging the heap obligations and then referring any remaining pure
constraints to other provers. SLEEK discharges heap obligations in three ways: heap node
matching, predicate folding, and predicate unfolding. To guarantee termination, SLEEK
ensures that each predicate fold or unfold must be immediately followed by a match, and
that no two fold operations for the same predicate are performed in order to match one node.
These restrictions ensure that each successful fold, unfold, and match operation decreases
the number of RHS nodes.
     Entailments in SLEEK are written as follows: ∆A ⊢κV QC ∗ ∆R , which is shorthand for
κ∗∆A ⊢∃V ·(κ∗QC ) ∗ ∆R . The entailment checks whether the consequent heap nodes QC are
covered by heap nodes in antecedent ∆A , and if so, SLEEK returns the residual heap ∆R ,
which consists of the antecedent nodes that were not used to cover QC . The implementation
performs a proof search and thus returns a set of residues. For simplicity, assume that only
one residue is computed. In the entailment, κ is the history of nodes from the antecedent
that have been used to match nodes from the consequent, V is the list of existentially
quantified variables from the consequent. Note that κ and V are discovered iteratively:
entailment checking begins with κ = emp and V = ∅.
     The initial system behavior was described in detail in [28, 12, 17]. The main rules for
matching, folding, unfolding, and discharging of pure constraints are given here. The initial
main entailment checking rules are given in Fig 8. Later we show how we modified these
rules to accommodate fractional shares.
     Entailment between separation formulae is reduced to entailment between pure formulae
by matching heap nodes in the RHS to heap nodes in the LHS (possibly after a fold/unfold).
Once the RHS is pure, the remaining LHS heap formula is soundly approximated to a pair
of pure formula and set of disjoint pointers by function XPure as defined in Fig 7. The
functions IsData(c) and IsPred(c) decide respectively if c is a data structure or a predicate.
The procedure successively pairs up heap nodes that it proves are aliased. SLEEK keeps
the successfully matched nodes from the antecedent in κ for better precision in the next
iteration.
     All three heap reducing steps start by establishing that there is a heap node on the LHS
of the entailment that is aliased with the RHS heap node that is to be reduced (p1 = p2 ).
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                        NOW WITH TOOL SUPPORT!           23




                  EMP                                                  MATCH
          (ρ, S)=XPure(κ1 ∗κ)                    fst(XPure(p1 :: chv1∗ i∗κ1 ∗κ))∧π1=⇒p1 =p2
                                                         κ∗p ::chv ∗ i
                                                 κ1 ∧π1 ⊢V 1 1 κ2 ∧π2 ∧( i (v1i = v2i )) ∗ ∆
                                                                             V
      ρ∧(∀x, y ∈ S · x 6= y)=⇒∃V·π2
           κ1 ∧π1 ⊢κV π2 ∗ (κ1 ∧π1 )            p1 :: chv1∗ i∗κ1 ∧π1 ⊢κV (p2 :: chv2∗ i∗κ2 ∧π2 ) ∗ ∆

                                                  FOLD
                             IsPred(c2 )∧IsData(c1 ) c2 hv ∗ i≡Q ∈ P
                         fst(XPure(p1 :: c1 hv1∗ i∗κ1 ∗κ)) ∧ π1=⇒p1 =p2
                           p1 :: c1 hv1∗ i∗κ1 ∧π1 ⊢κ∅ [p1 /self, v1∗ /v ∗ ]Q ∗ ∆r
                                           ∆r ⊢κV (κ2 ∧π2 ) ∗ ∆
                        p1 :: c1 hv1∗ i∗κ1 ∧π1 ⊢κV (p2 :: c2 hv2∗ i∗κ2 ∧π2 ) ∗ ∆

                                               UNFOLD
                             IsPred(c1 )∧IsData(c2 ) c1 hv ∗ i≡Q ∈ P
                          fst(XPure(p1 :: c1 hv1∗ i∗κ1 ∗κ)) ∧ π1=⇒p1 =p2
                                          ∆Q = to disjunct(Q)
                    [p1 /self, v1∗ /v ∗ ]∆Q ∗κ1 ∧π1 ⊢κV (p2 :: c2 hv2∗ i∗κ2 ∧π2 ) ∗ ∆
                        p1 :: c1 hv1∗ i∗κ1 ∧π1 ⊢κV (p2 :: c2 hv2∗ i∗κ2 ∧π2 ) ∗ ∆

                         Figure 8: Separation Constraint Entailment

In order to prove the aliasing, the LHS heap together with the previously consumed nodes
are approximated to a pure formula, and together with the LHS pure formula the p1 = p2
implication is checked. Similarly, when a match occurs (rule MATCH), equality between
node arguments needs to be proven.
     Unfold and fold operations handle inductive predicates in a deductive manner. SLEEK
can unfold a predicate instance that appears in the LHS if the unfolding exposes a heap
node that matches immediately with a node in the RHS. Similarly, several LHS nodes can
be folded into a predicate instance if the resulting predicate instance can be immediately
matched with a RHS node. Well-formedness conditions imposed on the predicate definitions
ensure that after a fold or unfold a matching always takes place; these conditions have been
elided for this presentation. The unfold rule presents the replacement of a predicate instance
in which the predicate definition is reduced to a disjunctive form and in which the arguments
have been substituted. The fold step requires the LHS to entail the predicate definition.
The residue of this entailment is then used as the new LHS for the rest of the original
entailment. For a more detailed explanation of the SLEEK entailment process, see Chin
et al. [12].

8.4. Entailment Procedure for Separation Logic with Shares. Adding fractional
permissions required several modifications to the entailment process.
• Empty heap. In a separation logic without shares, whenever (∃a, b.x7−    →a∗y7−→b) then
  x 6= y. In SLEEK, this fact is captured in the EMP rule, which tries to prove the pure
  part of the consequent after enriching the antecedent pure formula with pure information
  collected from the previously consumed heap and the remaining LHS heap. It extracts
24                          AQUINAS HOBOR AND CRISTIAN GHERGHINA




                                    FXPure(emp, τ ) ≡ (true, ∅)
                                   IsData(c)           τ ⇒ vf = cs
                            FXPure(p :: cvf hv ∗ i, τ ) ≡ (p6=0; {(p, cs)})
                      FXPure(κ1 , τ ) ≡ (f1 , s1 ) FXPure(κ2 , τ ) ≡ (f2 , s2 )
                             FXPure(κ1 ∗κ2 , τ ) ≡ (f1 ∧ f2 , s1 ∪ s2 )
                         IsPred(c)    (chv ∗ i ≡ Q inv (π1 , π2 )) ∈ P
               τ ⇒ vf = cs     ′
                              π1 = [p/self]π1        π2′ = {∀v ∈ π2 , ([p/self]v, cs)}
                              XPure(p :: cvf hv ∗ i, τ ) ≡ (π1′ , π2′ )

                              Figure 9: FXPure: XPure with shares


                                                  FOLD
                             IsPred(c2 )∧IsData(c1 ) c2 hv ∗ i≡Q ∈ P
                       fst(FXPure(p1 :: cf11 hv1∗ i∗κ1 ∗κ, τ1 )) ∧ π1=⇒p1 =p2
                               Q′ = set shares([p1 /self, v1∗ /v]Q, f2 )
                                p1 :: cf11 hv1∗ i∗κ1 ∧π1 ∧τ1 ⊢κ∅ Q′ ∗ ∆r
                                               r
                                      ∆r ⊢κV (κ2 ∧π2 ∧τ2 ) ∗ ∆
                   p1 :: cf11 hv1∗ i∗κ1 ∧π1 ∧ τ1 ⊢κV (p2 :: cf22 hv2∗ i∗κ2 ∧π2 ∧ τ2 ) ∗ ∆

                                             UNFOLD
                            c1 hv ∗ i≡Q ∈ P IsPred(c1 )∧IsData(c2 )
                       fst(FXPure(p1 :: cf11 hv1∗ i∗κ1 ∗κ, τ1 )) ∧ π1=⇒p1 =p2
                             Q′ = set shares([p1 /self, v1∗ /v ∗ ]Q, f1 )
                                       ∆Q = to disjunct(Q′ )
                         ∆Q ∗κ1 ∧π1 ∧τ1 ⊢κV (p2 :: cf22 hv2∗ i∗κ2 ∧π2 ∧τ2 ) ∗ ∆
                    p1 :: cf11 hv1∗ i∗κ1 ∧π1 ∧τ1 ⊢κV (p2 :: cf22 hv2∗ i∗κ2 ∧π2 ∧τ2 ) ∗ ∆

                   Figure 10: Folding/Unfolding in the presence of shares

     both the invariants of the heap nodes and constructs a formula that ensures that all
     pointers in the heap are distinct.
        Introducing fractional permissions requires the relaxation of this constraint because
              xf     yf
     ∃a, b.x7−→a∗y 7−→b implies x 6= y only if the xf and yf shares overlap. We changed the
     XPure function to return a pair of a pure formula, and pairs of pointers and associated
     fractional shares. The new version of XPure allowed the EMP rule to be rewritten to
     enforce inequality only between pointers that have conflicting shares:
                                    (ρ, S)=FXPure(κ1 ∗κ, τ )
               ρ∧(∀(x, xf ), (y, yf ) ∈ S, (¬∃z · xf ⊕ yf = z) · x 6= y)=⇒∃V·π2
                                                                                            EMP
                              κ1 ∧ π1 ∧ τ1 ⊢κV π2 ∗ (κ1 ∧ π1 ∧ τ1 )
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                  NOW WITH TOOL SUPPORT!        25




• Folding/unfolding. By convention, all the heap nodes abstracted by a predicate in-
  stance are owned with the same fractional permission as the predicate instance. There-
  fore, unfolding a node first replaces the permissions of the nodes in the predicate definition
  with the permission of that LHS node. Then the updated predicate definition replaces
  the predicate instance. Similarly, folding a node replaces the permissions of all nodes in
  the definition with the permission of that RHS node before trying to entail the predicate
  definition. The set shares(Q, v) function sets the permissions of all heap nodes in Q to v.
  The new set of rules is shown in Figure 10.
• Matching. In order to properly handle a match in the presence of fractional shares, the
  entailment process needs to (a) reduce both LHS and RHS nodes entirely, or (b) split the
  LHS node and reduce one side, or (c) split the RHS and reduce one side.
            fst(FXPure(p1 :: cf1 hv1∗ i∗κ1 , τ1 )) ∧ π1 =⇒ p1 = p2
                                                           

                                κ′ = κ∗p1 V :: cf1 hv1∗ i
                            ρ = f1 =f2 ∧ ( i (v1i = v2i ))
                                        ′
                        κ1 ∧ π1 ∧ τ1 ⊢κV κ2 ∧ π2 ∧ τ2 ∧ ρ ∗ ∆
                                                                               FULL-MATCH (a)
        p1 :: cf1 hv1∗ i∗κ1 ∧ π1 ∧ τ1 ⊢κV (p2 :: cf2 hv2∗ i∗κ2 ∧ π2 ∧ τ2 ) ∗ ∆


              fst(FXPure(p1 :: cf1 hv1∗ i∗κ1 , τ1 ))∧π1 =⇒ p1 =p2
                               τ1′ = τ1 ∧ fc1 ⊕ fr1 = f1
                                  κ′ = κ∗p1 :: fc1 ∗
                                             Vc ihv1 i i
                             ρ = fc1 =f2 ∧( i (v1 = v2 ))
                                                  ′
                p1 :: cfr1 hv1∗ i∗κ1 ∧π1 ∧τ1′ ⊢κV κ2 ∧π2 ∧τ2 ∧ρ ∗ ∆           LEFT-
                                                                              SPLIT-
           p1 :: cf1 hv1∗ i∗κ1 ∧π1 ∧τ1 ⊢κV (p2 :: cf2 hv2∗ i∗κ2 ∧π2 ∧τ2 ) ∗ ∆ MATCH (b)


              fst(FXPure(p1 :: cf1 hv1∗ i∗κ1 , τ1 ))∧π1 =⇒ p1 =p2
                  V ′ = if f2 ∈ V then V ∪ {fc2 , fr2 } else V
              τ1′ = if f2 ∈ V then τ1 else (τ1 ∧fc2 ⊕ fr2 = f2 )
              τ2′ = if f2 ∈ V then (τ2 ∧fc2 ⊕ fr2 = f2 ) else τ2
                                 κ′ = κ∗p1 V :: cf1 hv1∗ i
                            ρ = f1 =fc2 ∧( i (v1i = v2i ))
                                ′
                 κ1 ∧π1 ∧τ1′ ⊢κV ′ p2 :: cfr2 hv2∗ i∗κ2 ∧π2 ∧τ2′ ∧ ρ∗∆         RIGHT-
                                                                               SPLIT-
            p1 :: cf1 hv1∗ i∗κ1 ∧π1 ∧τ1 ⊢κV (p2 :: cf2 hv2∗ i∗κ2 ∧π2 ∧τ2 ) ∗ ∆ MATCH (c)
  Because the search can be computationally expensive, we have devised an aggressive
  pruning technique. We try to determine to what extent the fractional constraints restrict
  the fractional variables. It may be that (a) f1 = f2 , in which case only FULL-MATCH is
  feasible, or (b) f1 is included in f2 , in which case RIGHT-SPLIT-MATCH is feasible, or (c)
  f1 includes f2 , in which case only
  LEFT-SPLIT-MATCH is feasible.
26                       AQUINAS HOBOR AND CRISTIAN GHERGHINA




8.5. Proving barrier soundness. The fractional share solver and enhancements to SLEEK’s
entailment procedures discussed above help with any program logic that needs fractional
shares (e.g., concurrent separation logic with locks, sequential separation logic with read-
only data). In contrast, our other enhancements are specific to the logic for Pthreads-style
barriers. Our initial goal is to automatically check the consistency of barrier definitions—
that is, whether a barrier definition meets the side conditions presented in §4. The first
step is to describe a barrier diagram to SLEEK.
     Although the barrier diagrams presented in §4 are intuitive and concise, programs need
a more textual representation. Barrier diagrams describe the possible transitions a barrier
state can make and the specifications associated with those transitions. In a sense, a barrier
definition can be viewed as a disjunctive predicate definition where the body is a disjunction
of possible transitions.
     SLEEK already contains user-defined predicates so it is easy to introduce the “is a
barrier” predicate barrier(bn, vf , s) as required by the barrier logic, with a slight change to
notation to accommodate the syntax presented in Figure 6 to bnvf hsi.
     We extended SLEEK’s language to accept barrier diagrams in the form:
           bdef          ::= barrier (b name , thread cnt , v ∗ , transition∗ )
           transition    ::= (from state , to state , pre-post-spec∗ )
           pre-post-spec ::= (Φpre , Φpost )
SLEEK can now automatically check the well-formedness conditions on the barrier defini-
tions as follows:
• All transitions must have exactly thread cnt specifications, one for each thread
• For each transition, let from and to be the state labels, then:
   − for each specification (Φpre , Φpost )
     (1) Φpre contains a fraction of the barrier in state from:
          Φpre ⊢ self :: bnvf hfromi ∗ ∆
     (2) Φpost contains a fraction of the barrier in state to:
          Φpre ⊢ self :: bnvf htoi ∗ ∆
     (3) Φpre ∗Φpre ⊢ False
               The soundness proof assumes that each precondition P is precise. Unfortu-
          nately, precision is not very easy to verify automatically. As indicated in footnote
          7, we believe that the logic will be sound if we can assume the (strictly) weaker
          property “token”: P ⋆ P ⊢ False instead of precision. At this stage, our prototype
          extension to SLEEK verifies that preconditions are tokens rather than that they
          are precise. We are in the process of attempting to update our soundness proof
          to require that preconditions be tokens rather than precise; if we are unable to do
          so then one solution would be for SLEEK to output a Coq file stating lemmas re-
          garding the precision of each precondition. Users would then be required to prove
          these lemmas manually to be sure that their barrier definitions were sound. In our
          example barrier, the Coq proofs of precision were only a small part of the 2,700
          total lines of Coq script, so the savings from using SLEEK to verify the soundness
          of a barrier definition should still be quite substantial. Another choice would be
          to devise a heuristic algorithm for determining precision; we suspect that such an
          algorithm could handle the examples from this paper.
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                     NOW WITH TOOL SUPPORT!              27




  − the star of all the preconditions contains the full barrier (recall that the entailment ⊢
     check in SLEEK can produce a residue)




                                   `
     ∗i=thread
      i=1
               cnt Φi
                    pre ⊢ self :: bn hfromi ∗ ∆
  − the star of all the postconditions contains the full barrier




                                    `
     ∗i=thread
      i=1
               cnt Φi
                    post ⊢ self :: bn htoi ∗ ∆
  − the star of all the preconditions equals the star of all postconditions modulo the barrier
     state change for a transition. We check this constraint by carving the full barrier out
     of the total heap using the residues ∆pre and ∆post of the entailments given in the
     previous constraints. ∆pre and ∆post are then tested for equality by requiring bi-
     entailment with empty residue. That is, given
                                   `
     ∗i=thread
      i=1
               cnt Φi
                    pre ⊢ self :: bn hfromi∗∆pre
     and
                                    `

      i=thread cnt Φi
     ∗i=1           post ⊢ self :: bn htoi∗∆post ,
     we check
     ∆pre ⊢ ∆post and ∆post ⊢ ∆pre with empty residues.
  − For states with more than one successor, we check mutual exclusion for the precon-
     ditions as required by §4 by verifying that for any two preconditions of two distinct
     transitions must entail False. This check was extremely tedious to do for the example
     barrier in Coq but SLEEK can do it easily.
Once SLEEK has verified each of the above conditions, the barrier definition is well-formed
according to the constraints described in §4 (modulo precision).

8.6. Extension to program verification. Integrating our Hoare rule for barriers into HIP
was the easiest part of adding our program logic to HIP/SLEEK. Following the concept
of structured specifications [17], we transform our barrier diagrams into disjunctions of the
form                               _
                         bn ::=      (requires Φpre ensures Φpost ),
where the disjunction spans all specifications in all transitions in the barrier definition.
Verification of barrier calls trivially reduces to an entailment check of the disjunction.

8.7. Tool performance outline. We have developed a small set of benchmarks for our
HIP/SLEEK with barriers prototype. Our SLEEK tests divide into two categories: entail-
ment checks for separation logic formulae containing fractional permissions and checking
barrier consistency checks as in §8.5. Individual entailment checks are quite speedy and
our benchmark covers a number of interesting cases (e.g., inductively defined predicates).
Barrier consistency checks take more time but the performance is more than adequate:
              Sleek Examples             Test details           Entailments       Time (s)
              fractions.slk         fractional entailments          54             0.08
              barrier.slk            6 barrier definitions         279              2.3
One of the barrier definitions in barrier.slk is the example barrier given in Figure 1. It
took 2,700 (highly tedious) lines of code and 48 seconds of verification time (Figure
5) to convince Coq that the example barrier definition met the soundness requirements13.
  13Techniques such as those developed by Braibant et al. [7], Nanevski et al. [26], and Gonthier et
al. [18] can probably eliminate some (but not all) of the tedium of reasoning about the associativity and
commutativity of ∗. Unfortunately, proofs of mutual exclusion for barrier transitions seem less tractable.
28                           AQUINAS HOBOR AND CRISTIAN GHERGHINA




SLEEK verifies this example barrier definition and analyzes five others (some sound, others
not) in 2.3 seconds without any interaction from the user14.
     We have also benchmarked HIP with a slightly modified variant of the example from
§3. We made two modifications due to certain existing weaknesses in the HIP/SLEEK
toolchain. First, we substituted recursive functions for loops due to the convenience of
specification of recursive functions in HIP; and second, we changed the way x1 , x2 , y1 , and
y2 are modified in lines 6 and 10 to enable the numerical decision procedures (i.e., Omega)
to discharge the associated obligations. Both of these changes are orthogonal to our logic
for barriers: for example, a more powerful decision procedure for numerical equalities would
allow us to return to the original program.
     We verified our modified code against three specifications. In barrier-paper.ss, we
verify a trivial correctness property for the exact barrier definition from 3—i.e., we ver-
ify the postcondition of True, meaning that the program does not get stuck. We also
verified two more complex postconditions by using two more finely-grained barrier defi-
nitions: in barrier-weak.ss, we verified the relationship between x1 , x2 , and n; finally,
in barrier-strong.ss we verified the precise value in x1 after the loop terminates (i.e.,
x1 = 59). The code and specification for barrier-strong.ss is given in Appendix A. We
recorded the following timings from HIP:
       File                        Postcondition       LOC (code + specification)           Time(s)
       barrier-paper.ss                True                      73                          2.55
       barrier-weak.ss              lax bounds                   73                          2.91
       barrier-strong.ss           exact bounds                  73                          3.04
As expected, the tighter bounds require more verification time; however, the differences are
relatively small because most of the work is dealing with the heap constraints as opposed
to the pure constraints. Part of the time for each example is spent verifying the correctness
of the included barrier definition; all three barrier definitions from the HIP examples were
also included in the barrier.slk benchmark.
     HIP verification times are decent, but barrier calls are fairly computationally expensive
to verify due to the need to check multiple entailments. We believe that performance can be
further improved by adding optimizations to SLEEK in the style of [13]. Since barrier calls
are fairly rare in actual code, we believe that the performance of HIP/SLEEK on larger
examples will be acceptable.

                               9. Limitations and Future Work
We can extend the logic by making the barriers first-class (i.e., dynamic barrier creation/
destruction). In the present work we thought we could simplify the proofs by having stat-
ically declared barriers in the style of O’Hearn [29]. This turned out to be somewhat of
a mistake, at least as far as the soundness proof went: since we were forced to track the
barrier states (and partial shares) explicitly in the Hoare logic, we estimate that 90% of the
work required to make the barriers first-class has already been done in the present work;
moreover, a further 8% (the intrinsic contravariant circularity) would be easy to handle via
An alternative approach would be to use a separation logic entailment procedure implemented in Coq such
as the one recently described by Appel [2].
   14
      As explained in §8.5, SLEEK verifies properties that are slightly different from those verified in Coq.
         BARRIERS IN CONCURRENT SEPARATION LOGIC:                      NOW WITH TOOL SUPPORT!   29




indirection theory [23]. With perfect foresight (or if it were trivial to restart a large mecha-
nized proof), we would have certainly made the barriers first-class. Our SLEEK prototype
does support first-class barriers using the barrier creation rule we expect to be true.
    We suspect that our SLEEK prototype could be improved in numerous ways. For
example, our decision procedure for share formulae is quite incomplete15 and we believe
that several performance enhancements to SLEEK would speed up the consistency checks.
Finally, we need to resolve the precision/token issue.
    We also do not address the tricky problem of barrier definition inference.

                                           10. Related Work
Calcagno et al. proposed separation algebras as models of separation logic [11]; fractional
permissions were discussed by Bornat et al. [6]. In our work we use the share model and
separation algebra development of Dockins et al. [15, 1].
     O’Hearn’s concurrent separation logic focused on programs that used critical regions
[29, 8]; subsequent work by Hobor et al. and Gotsman et al. added first-class locks and
threads [22, 20, 21]. Our basic soundness techniques (unerased semantics tracks resource
accounting; oracle semantics isolates sequential and concurrent reasoning from each other;
etc.) follow Hobor et al. Recently both Villard et al. and Bell et al. extended concurrent
separation logic to channels [4, 31]. The work on channels is similar to ours in that both
Bell and Villard track additional dynamic state in the logic and soundness proof. Bell tracks
communication histories while Villard tracks the state of a finite state automaton associated
with each communication channel. Of all of the previous soundness results, only Hobor et
al. had a machine-checked soundness proof, albeit an incomplete one.
     An interesting question is whether is it possible to reason about barriers in a setting
with locks or channels. The question has both an operational and a logical flavor. Speaking
operationally, in a practical sense the answer is no: for performance reasons barriers are not
implemented with channels or locks. If we ignore performance, however, it is possible to
implement barriers with channels or locks16. The logical part of the question then becomes,
are the program logics defined by O’Hearn, Hobor, Gotsman, Villard, or Bell (including
their coauthors) strong enough to reason about the (implementation of) barriers in the
style of the logic we have presented? As far as we can tell each previous solution is missing
at least one required feature, so in a strict sense, the answer here is again no.
     For illustration we examine what seems to be the closest solution to ours: the copyless
message passing channels of Villard et al. Operationally speaking, the best way to imple-
ment barriers seems to be by adding a central authority that maintains a channel with
each thread using a barrier. When a thread hits a barrier, it sends “waiting” to the central
authority, and then waits until it receives “proceed”. In turn, the central authority waits for
a “waiting” message from each thread, and then sends each of them a “proceed” message.
Fortunately Villard allows the central authority to wait on multiple channels simultaneously.
     The question then becomes a logical one. Although it should not pose any fundamental
difficulty, their logic would first need to be enhanced with fractional permissions; in fact
we believe that Villard’s Heap-Hop tool already uses the same fractional permission model
  15For example, we cannot verify ∀π , π , π . π ⊕ π = π ⊢ π ⊕ π = π .
                                    1   2   3   1   2   3   1   2   3
  16
       Indeed, it is possible to implement channels and locks in terms of each other.
30                           AQUINAS HOBOR AND CRISTIAN GHERGHINA




(by Dockins et al.) that we do17. Since Villard uses automata to track state, we think it
probable, but not certain, that our barrier state machines can be encoded as a series of his
channel state machines.
     There are some problems to solve. Villard requires certain side conditions on his chan-
nels; we require other kinds of side conditions on our barriers; these conditions do not seem
fully compatible18. Assuming that we can weaken/strengthen conditions appropriately, we
reach a second problem with the side conditions: some of our side conditions (e.g., mutual
exclusion) are restrictions on the shape of the entire diagram; in Villard’s setting the barrier
state diagram has been partitioned into numerous separate channel state machines. Verify-
ing our side conditions seems to require verification of the relationships that these channel
state machines have to each other; the exact process is unclear.
     Once the matter of side conditions is settled, there remains the issue of verifying the
individual threads and the central authority. Villard’s logic seems to have all that is required
for the individual threads; the question is how difficult it would be to verify the central
authority. Here we are less sure but suspect that with enough ghost state/instructions it
can be done.
     There remains a question as to whether it is a good idea to reason about barriers via
channels (or locks). We suspect that it is not a good idea, even ignoring the fact that
actual implementations of barriers do not use channels. The main problem seems to be a
loss of intuition: by distributing the barrier state machine across numerous channel state
machines and the inclusion of necessary ghost state, it becomes much harder to see what
is going on. We believe that one of the major contributions of our work is that our barrier
rule is extremely simple; with a quick reference to the barrier state diagram it is easy to
determine what is going on. There is a secondary problem: we believe that our barrier
rule will look and behave essentially the same way in a setting with first-class barriers in
which it is possible to define functions that are polymorphic over the barrier diagram; even
assuming a channel logic enriched in a similar way, the verification of a polymorphic central
authority seems potentially formidable.
     One interesting question is how our barrier rule would interact with the rules of other
flavors of concurrent separation logic (e.g., with locks or channels). We believe that the
answer is yes, at least in the context of a logic of partial correctness19, as long as the
primitives used remain strongly synchronizing (i.e., coarse-grained). It is not clear how our
barrier rule might interact with the kind of fine-grained concurrency that is the subject
of Vafeiadis and Parkinson [30], Dodds et al. [16], or Dinsdale-Young et al. [14]. We
believe that our barrier rule is sound on a machine with weak memory as long as all of the
concurrency is strongly synchronized.
     Finally, work on concurrent program analysis is in the early stages; Gotsman et al.,
Calcagno et al., and Villard et al. give techniques that cover some use cases involving locks
and channels but much remains to be done [19, 10, 32].

   17
      To be precise, Heap-Hop uses the code extracted from the fractional permission Coq proof development
by Dockins et al.
   18
      For example, Villard requires determinacy whereas we do not; he would also require that the postcon-
ditions of barriers be precise whereas we do not; etc.
   19
      Of course, the more concurrency primitives a programmer has, the easier it is to get into a deadlock. We
hypothesize that concurrent program logics of total correctness may not be as compositional as concurrent
program logics of partial correctness.
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                NOW WITH TOOL SUPPORT!             31




Connection to a result by Jacobs and Piessens. We recently learned that Jacobs and Piessens
have an impressive result on modular fine-grained concurrency [25]. Jacobs was able to
reason about our example program using his VeriFast tool by designing an implementation
of barriers using locks and reducing our barrier diagram to a large disjunction for a resource
invariant.
     However, VeriFast has some disadvantages compared to the HIP/SLEEK approach we
presented. First, HIP/SLEEK required far less input from the user. In the case of our
30-line example program, more than 600 lines of annotation were required in VeriFast,
not including the code/annotiations for the barrier implementation itself. HIP/SLEEK
were able to verify the same program with approximately 30 lines of annotation (mostly
the barrier definition). Second, it was harder to gain insight into the program from the
disjunction-form of the invariant; in contrast we find our barrier diagrams straightforward
to understand. Finally, it is unclear to us whether the reduction is always possible or
whether it was only enabled by the relative simplicity of our example program. That said,
Jacobs and Piessens have the only logic and tool proven to be able to reason about barriers
as derived from a more general mechanism.

                                       11. Conclusion
We have designed and proved sound a program logic for Pthreads-style barriers. Our devel-
opment includes a formal design for barrier definitions and a series of soundness conditions
to verify that a particular barrier can be used safely. Our Hoare rules can verify threads
independently, enabling a thread-modular approach. Our soundness proof defines an op-
erational semantics that explicitly tracks permission accounting during barrier calls and is
machine-checked in Coq. We have modified the verification toolset HIP/SLEEK to use our
logic to verify concurrent programs that use barriers.

    Our soundness results are machine-checked in Coq and are available at:
                          www.comp.nus.edu.sg/∼hobor/barrier
    Our prototype HIP/SLEEK verification tool is available at:
           www.comp.nus.edu.sg/∼cristian/projects/barriers/tool.html

Acknowledgements. We thank Christian Bienia for showcasing numerous example programs
containing barriers, Christopher Chak for help on an early version of this work, Jules Villard
for useful comments in general and in particular on the relation of our logic to the logic of
his Heap-Hop tool, and Bart Jacobs for discovering how to verify our example program in
his VeriFast tool.

                                         References
[1] Andrew Appel, Robert Dockins, and Aquinas Hobor. Mechanized Semantic Library. Available at
    http://msl.cs.princeton.edu, 2009–2010.
[2] Andrew W. Appel. VeriSmall: Verified smallfoot shape analysis. In CPP 2011: First International
    Conference on Certified Programs and Proofs, pages 231–246, 2011.
[3] Andrew W. Appel and Sandrine Blazy. Separation logic for small-step C minor. In TPHOLs, pages
    5–21, 2007.
32                           AQUINAS HOBOR AND CRISTIAN GHERGHINA




 [4] Christian J. Bell, Andrew W. Appel, and David Walker. Concurrent separation logic for pipelined
     parallelization. In SAS, pages 151–166, 2010.
 [5] Christian Bienia. Benchmarking Modern Multiprocessors. PhD thesis, Princeton University, Department
     of Computer Science, Princeton, NJ, December 2010.
 [6] Richard Bornat, Cristiano Calcagno, Peter O’Hearn, and Matthew Parkinson. Permission accounting
     in separation logic. In POPL, pages 259–270, 2005.
 [7] Thomas Braibant and Damien Pous. Tactics for reasoning modulo AC in Coq. In CPP, pages 167–182,
     2011.
 [8] Stephen D. Brookes. A semantics for concurrent separation logic. In CONCUR, pages 16–34, 2004.
 [9] David R. Butenhof. Programming with POSIX Threads. Addison-Wesley, 1997.
[10] Cristiano Calcagno, Dino Distefano, and Vikor Vafeiadis. Bi-abductive resource invariant synthesis. In
     APLAS, pages 259–274, 2009.
[11] Cristiano Calcagno, Peter W. O’Hearn, and Hongseok Yang. Local action and abstract separation logic.
     In LICS, pages 366–378, 2007.
[12] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. Automated verification of
     shape, size and bag properties via user-defined predicates in separation logic. Science of Computer
     Programming, 2010.
[13] Wei-Ngan Chin, Cristian Gherghina, Razvan Voicu, Quang Loc Le, Florin Craciun, and Shengchao
     Qin. A specialization calculus for pruning disjunctive predicates to support verification. In CAV, pages
     293–309, 2011.
[14] Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J. Parkinson, and Viktor Vafeiadis.
     Concurrent abstract predicates. In ECOOP, pages 504–528, 2010.
[15] Robert Dockins, Aquinas Hobor, and Andrew W. Appel. A fresh look at separation algebras and share
     accounting. In APLAS, pages 161–177, 2009.
[16] Mike Dodds, Xinyu Feng, Matthew J. Parkinson, and Viktor Vafeiadis. Deny-guarantee reasoning. In
     ESOP, pages 363–377, 2009.
[17] Cristian Gherghina, Cristina David, Shengchao Qin, and Wei-Ngan Chin. Structured specifications for
     better verification of heap-manipulating programs. In FM, pages 386–401, 2011.
[18] Georges Gonthier, Beta Ziliani, Aleksandar Nanevski, and Derek Dreyer. How to make ad hoc proof
     automation less ad hoc. In ICFP, pages 163–175, 2011.
[19] Alexey Gotsman, Josh Berdine, and Byron Cook. Interprocedural Shape Analysis with Separated Heap
     Abstractions. In SAS, pages 240–260, 2006.
[20] Alexey Gotsman, Josh Berdine, Byron Cook, Noam Rinetzky, and Mooly Sagiv. Local reasoning for
     storable locks and threads. In APLAS, pages 19–37, 2007.
[21] Aquinas Hobor. Oracle semantics. Technical Report TR-836-08, Princeton, 2008.
[22] Aquinas Hobor, Andrew W. Appel, and Francesco Zappa Nardelli. Oracle semantics for concurrent
     separation logic. In ESOP, pages 353–367, 2008.
[23] Aquinas Hobor, Robert Dockins, and Andrew W. Appel. A theory of indirection via approximation. In
     POPL, pages 171–185, 2010.
[24] Aquinas Hobor and Cristian Gherghina. Barriers in concurrent separation logic. In ESOP, pages 276–
     296, 2011.
[25] Bart Jacobs and Frank Piessens. Expressive modular fine-grained concurrency specification. In POPL,
     pages 271–282, 2011.
[26] Aleksandar Nanevski, Viktor Vafeiadis, and Josh Berdine. Structuring the verification of heap-
     manipulating programs. In POPL, pages 261–274, 2010.
[27] Huu Hai Nguyen and Wei-Ngan Chin. Enhancing program verification with lemmas. In CAV, pages
     355–369, 2008.
[28] Huu Hai Nguyen, Cristina David, Shengchao Qin, and Wei-Ngan Chin. Automated verification of shape
     and size properties via separation logic. In VMCAI, pages 251–266, 2007.
[29] Peter W. O’Hearn. Resources, concurrency and local reasoning. Theoretical Computer Science,
     375(1):271–307, May 2007.
[30] Viktor Vafeiadis and Matthew J. Parkinson. A marriage of rely/guarantee and separation logic. In
     CONCUR, pages 256–271, 2007.
[31] Jules Villard, Étienne Lozes, and Cristiano Calcagno. Proving copyless message passing. In APLAS,
     pages 194–209, 2009.
      BARRIERS IN CONCURRENT SEPARATION LOGIC:                  NOW WITH TOOL SUPPORT!            33




[32] Jules Villard, Étienne Lozes, and Cristiano Calcagno. Tracking heaps that hop with heap-hop. In
     TACAS, pages 275–279, 2010.
34                        AQUINAS HOBOR AND CRISTIAN GHERGHINA




                       Appendix A. Example from §3 revisited
Below we present a slight variation on the example from section §3 that we verified with
our HIP/SLEEK toolchain. In this example, we specify exact postconditions. Starting the
execution with x1 = x2 = 1 will lead to x1 = x2 = 59. The example is expressed in the
HIP/SLEEK input language (where [L] and [R] respectively denote the left and right half
of the full share). It makes use of recursive functions instead of while loops, but this is only
for aesthetic reasons.


data cl {int val;}

barrier bn, 2,x1 x2 y1 y2 i,
/* bn-barrier name, 2-thread count, x1..i shared heap                           */
/* the list of shared variables denotes the arguments of the barrier definition */
/* however for technical reasons we found it easier to list the variables here */
/* these could be infered with some additional work                             */
[(0,1,   // transition description, start/end state
  [ requires
        x1::cl@[L]<A1>*x2::cl@[L]<B1>* y1::cl@[L]<C1>*y2::cl@[L]<D1>*
        i::cl@[L]<T1>*self::bn@[L]<0>
    ensures
        x1::cl@[L]<A1>*x2::cl@[L]<B1>* y1::cl<C1>*i::cl@[L]<T1>*
        self::bn@[L]<1> & T1 < 30;,                             // one pre-post
    requires
        x1::cl@[R]<A2>*x2::cl@[R]<B2>*y1::cl@[R]<C2>*y2::cl@[R]<D2>*
        i::cl@[R]<T2>*self::bn@[R]<0>
    ensures
        x1::cl@[R]<A2>*x2::cl@[R]<B2>*y2::cl<D2>*i::cl@[R]<T2>*
        self::bn@[R]<1> & T2 < 30;]),

 (1,2,[
    requires
        x1::cl@[L]<A>*x2::cl@[L]<A>*y1::cl<C>* i::cl@[L]<T>* self::bn@[L]<1>&
        T<30 & A=2*T-1 & C = 3*A+2
    ensures
        x1::cl<A>*y1::cl@[L]<C>*y2::cl@[L]<D>*i::cl<T>*self::bn@[L]<2>&
        T<30 & A=2*T-1 & D=2*A & C = 3*A+2;,
    requires
        x1::cl@[R]<A>*x2::cl@[R]<A>*y2::cl<D>*i::cl@[R]<T>*self::bn@[R]<1>&
        T<30 & D=2*A & A=2*T-1
    ensures
        x2::cl<A>*y1::cl@[R]<C>*y2::cl@[R]<D>* self::bn@[R]<2> &
        D=2*A & C = 3*A+2 & A=2*T-1;]),

 (2,1,[
    requires
    BARRIERS IN CONCURRENT SEPARATION LOGIC:    NOW WITH TOOL SUPPORT!   35




        x2::cl<B>*y1::cl@[R]<C>*y2::cl@[R]<D>* self::bn@[R]<2> & B=C-D
    ensures
        x1::cl@[R]<A>*x2::cl@[R]<B>*y2::cl<D>*i::cl@[R]<T>*self::bn@[R]<1>&
        A=C-D & A=B & A=2*T-1 & T <= 30;,
    requires
        x1::cl<A>*y1::cl@[L]<C>*y2::cl@[L]<D>*i::cl<T>*self::bn@[L]<2>&
        A=C-D & A=2*T-1 & T <= 30
    ensures
        x1::cl@[L]<A>*x2::cl@[L]<B>*y1::cl<C>*i::cl@[L]<T>*self::bn@[L]<1>&
        A=C-D & A=B & A=2*T-1 & T <= 30;]) ,

 (1,3,[
    requires
        x1::cl@[L]<A>*x2::cl@[L]<B>*i::cl@[L]<T>*self::bn@[L]<1>& T=30
    ensures
        x1::cl@[L]<A>*x2::cl@[L]<B>*i::cl<T>*self::bn@[L]<3> & T=30;,
    requires
        x1::cl@[R]<A>*x2::cl@[R]<B>*i::cl@[R]<T>*self::bn@[R]<1>& T=30
    ensures
        x1::cl@[R]<A>*x2::cl@[R]<B> *self::bn@[R]<3>;])];

// end barrier definition, begin code

void th1 (cl x1, cl x2, cl y1, cl y2, cl i, bn b)
    requires
        x1::cl@[L]<1>*x2::cl@[L]<1>*y1::cl@[L]<_>*
        y2::cl@[L]<_>*i::cl@[L]<1>*b::bn@[L]<0>
    ensures
        x1::cl@[L]<v>*x2::cl@[L]<v>*b::bn@[L]<3>& v=59;
{                                 // stage 0
  barrier b;                      // stage 0->1
  th1_loop (x1,x2,y1,y2,i,b);
}

void th1_loop(cl x1, cl x2, cl y1, cl y2, cl i, bn b)
    requires
        x1::cl@[L]<v>*x2::cl@[L]<v>*y1::cl<_>*i::cl@[L]<a>*
        b::bn@[L]<1> & v=2*a -1 & a <= 30
    ensures
        x1::cl@[L]<v1>*x2::cl@[L]<v1>*b::bn@[L]<3>& v1=59;
{
  if (i.val<30)
  {                               // stage 1
    y1.val = x1.val + 2*x2.val+2;
    barrier b;                    // stage 1->2
    x1.val = y1.val - y2.val;
    i.val= i.val+1;
36                     AQUINAS HOBOR AND CRISTIAN GHERGHINA




       barrier b;                       // stage 2->1
       th1_loop (x1,x2,y1,y2,i,b);
     }
     else barrier b;                    // stage 1->3
}

void th2 (cl x1, cl x2, cl y1, cl y2, cl i, bn b)
    requires
        x1::cl@[R]<1>*x2::cl@[R]<1>*y1::cl@[R]<_>*y2::cl@[R]<_>*
        i::cl@[R]<1>*b::bn@[R]<0>
    ensures
        x1::cl@[R]<v>*x2::cl@[R]<v>*b::bn@[R]<3>& v=59;
{                                 // stage 0
  barrier b;                      // stage 0->1
  th2_loop (x1,x2,y1,y2,i,b);
}

void th2_loop(cl x1, cl x2, cl y1, cl y2, cl i, bn b)
    requires
        x1::cl@[R]<v>*x2::cl@[R]<v>*y2::cl<_>*i::cl@[R]<a>*
        b::bn@[R]<1> & v=2*a -1 & a <= 30
    ensures
        x1::cl@[R]<v1>*x2::cl@[R]<v1>*b::bn@[R]<3>& v1=59;
{
  if (i.val<30)
  {                               // stage 1
    y2.val = x1.val + x2.val;
    barrier b;                    // stage 1->2
    x2.val = y1.val - y2.val;
    barrier b;                    // stage 2->1
    th2_loop (x1,x2,y1,y2,i,b);
  }
  else barrier b;                 // stage 1->3
}




                                     This work is licensed under the Creative Commons Attribution-NoDerivs License. To view
                                     a copy of this license, visit http://creativecommons.org/licenses/by-nd/2.0/ or send a
                                     letter to Creative Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or
                                     Eisenacher Strasse 2, 10777 Berlin, Germany
