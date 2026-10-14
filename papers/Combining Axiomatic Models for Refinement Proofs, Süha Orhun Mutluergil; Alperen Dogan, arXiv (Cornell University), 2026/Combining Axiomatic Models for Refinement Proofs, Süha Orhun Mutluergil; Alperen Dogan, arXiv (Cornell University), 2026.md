                                         C OMBINING A XIOMATIC P ROGRAM L OGICS WITH R EFINEMENT
                                                                  P ROOFS

                                                                                               A P REPRINT


                                                           Süha Orhun Mutluergil                                          Alperen Doğan
                                                  Computer Science and Engineering Program                 Computer Science and Engineering Program
                                                             Sabancı University                                       Sabancı University
arXiv:2606.27916v1 [cs.LO] 26 Jun 2026




                                                              İstanbul, Türkiye                                       İstanbul, Türkiye
                                                   suha.mutluergil@sabanciuniv.edu                             alperend@sabanciuniv.edu


                                                                                              June 29, 2026

                                                                                              A BSTRACT
                                                  Refinement proofs verify an implementation by showing that its behaviours are subsumed by a simpler
                                                  specification, on which functional properties are easier to establish. We study how such proofs interact
                                                  with the axiomatic program logics used to verify the specification. We first give a uniform account of
                                                  Hoare, Incorrectness, Lisbon, and Necessary Preconditions logic, classified by the direction in which
                                                  each constrains a transition and by whether it over- or under-approximates its target set. We then show
                                                  that simulation relations transfer state-based safety properties: a forward simulation carries a Hoare
                                                  (inductive) invariant of the specification to one of the implementation, and forward and backward
                                                  simulations both carry ordinary invariants, via the pre-image of the relation. Finally, we characterize,
                                                  within these logics, when a relation is a simulation, forward simulations by the validity of Hoare or
                                                  Lisbon triples, backward simulations by Necessary Preconditions or Incorrectness triples, so that
                                                  the simulation obligation reduces to a triple in a functional logic. We illustrate the development
                                                  with a concurrent counter, carrying a safety bound from an atomic sequential specification to a
                                                  Left–Right implementation through an intermediate nondeterministic concurrent counter, with a
                                                  forward simulation on one side and a backward simulation on the other.

                                         Keywords functional verification · relational verification · simulation relations

                                         1   Introduction
                                         Ensuring the correctness of safety-critical software increasingly relies on formal verification. Functional correctness
                                         is commonly expressed in axiomatic program logics: Hoare logic [Hoare, 1969], which over-approximates the
                                         reachable states of a program; Incorrectness logic [O’Hearn, 2019], which under-approximates them. The more recent
                                         Lisbon [Ascari et al., 2023] and Necessary Preconditions [Cousot et al., 2013] logic reason in the backward direction.
                                         Verifying a property directly on an implementation, however, is costly, and the cost is paid again after every change to
                                         the code. Refinement avoids this: instead of reasoning about the implementation, one proves the property on a simpler
                                         abstract specification and shows that every behavior of the implementation is permitted by the specification Lynch and
                                         Vaandrager [1995]. Because specifications are stated over clean mathematical structures, the functional proof is usually
                                         easier.
                                         The standard techniques for relating an implementation to a specification is a simulation relation Lynch and Vaandrager
                                         [1995], and the standard technique for transferring a property is to pull it back along that relation. This paper studies
                                         the interaction between the two. We ask two questions: under forward or backward simulations, what a property proved
                                         on the specification guarantees on the implementation; and how the simulation itself can be discharged using the same
                                         functional logics that verify the specification.
                                         To keep the development concrete, we carry a single running example throughout: a shared counter supporting
                                         concurrent increment and read operations. The property of interest, that no read ever reports more increments than
                            Combining Axiomatic Program Logics with Refinement Proofs                          A P REPRINT



have been invoked, is immediate on an atomic sequential counter, and we transport it down to a Left–Right (LR)
concurrent implementation along simulation relations. No single simulation links the implementation to the sequential
specification, so the proof factors through an intermediate nondeterministic concurrent (NDC) counter, with a forward
simulation on one side and a backward simulation on the other.
Section 2 introduces the three machines and the two relations informally. Section 3 describes the simulation framework,
the functional logics, and the notion of invariant we transfer. Section 4 proves the transfer theorems and applies them
to the counter. Section 5 gives the simulation validity characterizations, and the appendices discharge the example’s
forward and backward simulations using Lisbon and Incorrectness triples.


2     Background

We illustrate the development with a single running example: a shared counter supporting concurrent increment and
read operations. Our goal is to verify a safety property of a particular implementation, that no read ever reports more
increments than that have actually been invoked. Implementations of concurrent objects are, however, awkward to
reason about directly. The strategy of this paper is therefore to prove the property on a simple specification, where it
is almost immediate, and to transport it down to the implementation along simulation relations. As we will see, no
single simulation links the implementation to the simplest specification; the proof factors through an intermediate
machine. This section introduces the three machines and the two relations informally and the remaining sections make
the reasoning axiomatic.


2.1   A Concurrent Counter: the Left–Right Implementation

The implementation we wish to verify, the Left–Right (LR) counter, keeps the count split across two registers L and R.
An increment bumps one of the two registers, chosen nondeterministically, modeling a counter split across two threads
or nodes. A read is performed in two steps: at begin it snapshots L into a local variable vL , and at return it adds the
current value of R and reports vL + R. This split makes the implementation efficient but subtle: the value a read returns
is not determined when it begins, but only when it returns, and it depends on every increment that touches R in between.
Throughout, II and IR are the (disjoint) sets of increment and read operation identifiers, and I = II ∪ IR . Each operation
identifier carries a program counter that moves from INIT to DONE (through MID for the two step operations); the maps
i• and o• record the input and output values of each operation and constitute the externally visible interface; the register
updates are internal.
Definition 1 (Left–Right counter). The state of the LR counter consists of L ∈ N, R ∈ N, a program counter
pc lr : I → {INIT, MID, DONE}, a snapshot map vL : IR → N, a set of old increment values old lr ⊆ N, and interface
maps ilr , olr . Its operations are
                                         increment(id) :
                                           assume pc lr (id) = INIT
                                           if (∗) L ← L + 1 else R ← R + 1
                                           old lr ← old lr ∪ {L + R}
                                           pc lr (id) ← DONE
                                         begin_read(id) :
                                           assume pc lr (id) = INIT
                                           vL (id) ← L
                                           pc lr (id) ← MID
                                         return_read(id) :
                                           assume pc lr (id) = MID
                                           pc lr (id) ← DONE
                                           olr (id) ← vL (id) + R
                                           return vL (id) + R


The correctness property of interest is a safety bound: for every read id that has completed, the reported value olr (id) is
at most L + R, the number of increments performed so far. Stating and proving this directly on the LR counter means
reasoning about all interleavings of the split reads with concurrent increments to R, which is precisely the kind of
global argument we prefer to avoid.


                                                             2
                            Combining Axiomatic Program Logics with Refinement Proofs                        A P REPRINT



2.2   Transferring Correctness from a Sequential Specification


An idealized sequential counter, in which each operation executes atomically, makes the property trivial: a single
variable x holds the count, an increment adds one to it atomically, and a read atomically returns x. The safety bound is
then trivial, because x is the number of increments.

Definition 2 (Sequential counter). The state consists of x ∈ N, a program counter pc s : I → {INIT, DONE}, a set of
old increment values old s ⊆ N, and interface maps is , os . Its operations are



                                               increment(id) :
                                                 assume pc s (id) = INIT
                                                 x←x+1
                                                 old s ← old s ∪ {x}
                                                 pc s (id) ← DONE
                                               read(id) :
                                                 assume pc s (id) = INIT
                                                 os (id) ← x
                                                 pc s (id) ← DONE
                                                 return x




Were the LR counter to refine the sequential counter, the safety bound would transfer downward: a simulation pulls
an invariant of the specification back to an invariant of the implementation. The difficulty is finding the witnessing
simulation. A forward simulation from LR to the sequential counter would have to match every implementation step
against specification steps using only the past and present. But the sequential read is atomic: it must commit to a
returned value at one instant, whereas the LR read fixes its value only at return_read, after an unknown number of
interleaving increments to R. At begin_read there is no way to know which sequential state to move to, because the
answer depends on the future. A single forward simulation between the two therefore does not exist, and this is the look
ahead that, in general, forces backward (prophecy style) reasoning.
Rather than search for a more delicate single relation, we factor the proof through an intermediate specification. This is
guaranteed by the completeness of forward and backward simulations: when one machine implements another, the trace
inclusion can always be witnessed by a forward simulation into some intermediate automaton followed by a backward
simulation out of it [Lynch and Vaandrager, 1995]. The next machine is an instance of that intermediate automaton.




2.3   An Intermediate Specification: the Nondeterministic Concurrent Counter


The nondeterministic concurrent (NDC) counter is designed to be loose. It does not track a single count; instead it
records, for each read, which increments that read is obliged to observe and which it is merely permitted to observe. It
maintains the set P of pending increments (begun but not finished), the set C of completed increments, and the set A
of active reads. When a read begins, it snapshots the completed increments into its must-see set MS and the pending
increments into its may-see set YS . When the read returns, it nondeterministically chooses any set S between these two
bounds and reports |S|. This freedom lets the NDC counter match the LR counter step for step: a value that the split LR
read produces at return time is always one of the admissible |S|. At the same time the must-see/may-see bookkeeping
allows NDC counter to be related to the atomic sequential counter.

Definition 3 (Nondeterministic concurrent counter). The state consists of P ⊆ II (pending increments), C ⊆ II
(completed increments), A ⊆ IR (active reads), maps MS , YS : IR → P(II ) (must-see and may-see), a program
counter pc n : I → {INIT, MID, DONE}, a set of old increment values old n ⊆ N, and interface maps in , on . Its


                                                            3
                            Combining Axiomatic Program Logics with Refinement Proofs                      A P REPRINT



operations are
                                  begin_increment(id) :
                                    assume pc n (id) = INIT, id ∈/ P, id ∈
                                                                         /C
                                    P ← P ∪ {id}
                                    old n ← old n ∪ {|C| + |P |}
                                    for all t ∈ A : YS (t) ← YS (t) ∪ {id}
                                    pc n (id) ← MID
                                  return_increment(id) :
                                    assume pc n (id) = MID, id ∈ P, id ∈ /C
                                    P ← P \ {id}; C ← C ∪ {id}
                                    pc n (id) ← DONE
                                  begin_read(id) :
                                    assume pc n (id) = INIT, id ∈/A
                                    A ← A ∪ {id}
                                    MS (id) ← C; YS (id) ← P
                                    pc n (id) ← MID
                                  return_read(id) :
                                    assume pc n (id) = MID, id ∈ A
                                    A ← A \ {id}
                                    choose S with MS (id) ⊆ S ⊆ MS (id) ∪ YS (id)
                                    on (id) ← |S|
                                    pc n (id) ← DONE
                                    return |S|

2.4     The Simulation Chain

We relate the three machines by
                                               forward         backward
                                         LR −−−−−→ NDC −−−−−−→ Seq,
which lets the composed simulation relation carry the sequential counter’s Hoare invariant, the bound stating that every
completed read reports at most L + R, back to the LR counter as a state predicate. The two relations are given below;
both require the interface maps to agree, forcing the same externally visible behaviour.

2.4.1    Forward Simulation from LR to NDC
Let the concrete (LR) state be σ = (L, R, pc lr , vL , ilr , olr ) and the abstract (NDC) state be τ                 =
(P, C, A, MS , YS , pc n , in , on ). The forward simulation relation R(σ, τ ) is the conjunction of
                        |C| = L + R                                                                                (F1)
                        ∀id ∈ I. pc lr (id) = MID ⇐⇒ id ∈ A                                                        (F2)
                        ∀id ∈ A. |MS (id)| ≤ vL (id) + R ≤ |MS (id) ∪ YS (id)|                                     (F3)
                        old n ⊆ old lr                                                                             (F4)
                        ∀id ∈ I. pc n (id) ̸= INIT =⇒ pc lr (id) ̸= INIT ∧ ilr (id) = in (id)                      (F5)
                        ∀id ∈ I. pc lr (id) = DONE =⇒ pc n (id) = DONE ∧ olr (id) = on (id)                        (F6)

The intuition is an action correspondence that matches each implementation step with a sequence of specification steps.

         • An LR increment, a single atomic step that bumps L or R, is matched by the pair begin_increment;
           return_increment, which moves one identifier into C. Either way the count rises by one, so |C| = L + R is
           restored (F1).
         • An LR begin_read is matched by an NDC begin_read: the snapshot vL ← L on the concrete side and
           MS ← C, YS ← P on the abstract side establish the two bounds of (F3) for the new read, with id entering A
           exactly as pc lr (id) enters MID (F2).
         • An LR return_read reports vL (id) + R. The matching NDC return_read chooses S with |S| = vL (id) + R;
           invariant (F3) guarantees such an S lies between MS (id) and MS (id) ∪ YS (id), so the two machines report
           the same value and (F6) is preserved.


                                                           4
                             Combining Axiomatic Program Logics with Refinement Proofs                           A P REPRINT



Conditions (F5) and (F6) keep the inputs and outputs of corresponding operations equal, so equal observable behaviour
is maintained throughout. Because every LR step is answered forward in this way, R is a forward simulation and
traces(LR) ⊆ traces(NDC).

2.4.2    Backward Simulation from NDC to the Sequential Counter
Now let the concrete (NDC) state be σ = (P, C, A, MS , YS , pc n , in , on ) and the abstract (sequential) state be
τ = (x, pc s , is , os ). The backward simulation relation R(σ, τ ) is the conjunction of
                          |C| ≤ x ≤ |C| + |P |                                                                           (B1)
                          old s ⊆ old n                                                                                  (B2)
                          ∀id ∈ I. pc s (id) ̸= INIT =⇒ pc n (id) ̸= INIT ∧ in (id) = is (id)                            (B3)
                          ∀id ∈ I. pc n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id)                              (B4)

The prophecy is expressed by invariant (B1): the sequential count x is pinned only to the interval between the completed
increments and the completed plus pending increments, leaving room to decide when an abstract increment takes effect.
Because the simulation is backward, that decision is made by looking at the post-state. The action correspondence runs
as follows.

         • Across an NDC begin_increment; return_increment pair, exactly one atomic sequential increment must
           fire. Which of the two concrete steps it accompanies, or whether the abstract machine stutters, is the prophecy,
           resolved by looking at the post-state so that the sequential count x stays inside the interval (B1); this is the
           look ahead that a forward simulation could not perform.
         • An NDC read reports |S|, a value between its must-see count |M S(id)| and its may-see count |M S(id) ∪
           Y S(id)|. The matching atomic sequential read takes effect at the read’s linearization point: the step at which
           the running count x first equals |S|. Because |S| may be smaller than the number of increments completed by
           the time the read returns, this point generally lies strictly before return_read, at begin_read, or at one of the
           increments interleaved with the read. Invariant (B1), together with the must-/may-see bounds, guarantees the
           count passes through |S| while the read is active, so such a step exists; there both machines report |S| and (B4)
           is established.
         • Every NDC step at which neither the increment nor a read takes effect, in particular return_read, whose value
           was already fixed at the linearization point, and begin_read for a read that linearizes later, is matched by a
           sequential stutter.

Since every NDC step admits such a matching (or stuttering) abstract step constructed from the future, R is a backward
simulation and traces(NDC) ⊆ traces(Seq).

Composing the two simulations relates the LR counter to the sequential counter, so the safety bound proved on the
sequential counter holds of the LR implementation. The forward half pins down how the implementation’s choices
are reflected in the intermediate machine, and the backward half supplies the look ahead that relates the intermediate
machine to the atomic specification. The rest of the paper recasts both halves axiomatically and shows how their validity
can be discharged using the functional program logics.

3     Preliminaries
3.1     Refinement Proofs

3.1.1    Automata, Executions, and Traces
We use the labelled transition system model of Lynch and Vaandrager [1995]. An automaton A consists of a
set states(A) of states, a nonempty set start(A) ⊆ states(A) of start states, a set acts(A) of actions containing
a distinguished internal action τ , and a set steps(A) ⊆ states(A) × acts(A) × states(A) of transitions. The
                                                                                                             a
external actions are ext(A) = acts(A) \ {τ }; these are the actions visible to an observer. We write s −    →A s′ for
        ′
(s, a, s ) ∈ steps(A), and βb for the sequence obtained from a sequence of actions β by deleting all τ events.
An execution fragment of A is a finite or infinite alternating sequence α = s0 a1 s1 a2 s2 · · · of states and actions with
    ai+1
si −−−→A si+1 for all i; it is an execution if s0 ∈ start(A). A state is reachable if it is the last state of some finite
execution, and we write reach(A) for the set of reachable states. The trace of α is trace(α) = a\  1 a2 · · ·, the sequence of



                                                              5
                              Combining Axiomatic Program Logics with Refinement Proofs                        A P REPRINT


                                                                                                                     β
                                                                                                                 →A s′
external actions along α, and traces(A) is the set of all traces. For a finite sequence β over ext(A) we write s −
when A has a finite execution fragment from s to s′ with trace β; this “weak” arrow absorbs internal steps and lets the
specification answer one implementation step with a sequence of its own steps.
The behavioral comparison of interest is trace inclusion. For automata S1 and S2 with ext(S1 ) = ext(S2 ) we write
                                                      △
                                      S1 ⊑T S2       ⇐⇒      traces(S1 ) ⊆ traces(S2 ),
read “S1 implements S2 ”. Throughout, S1 is the implementation (concrete) automaton and S2 the specification
(abstract) one.

3.1.2    Forward Simulations
A forward simulation from S1 to S2 is a relation f ⊆ states(S1 ) × states(S2 ) such that

        1. if s ∈ start(S1 ) then f [s] ∩ start(S2 ) ̸= ∅, and
                a                                                               a
                →S1 s′ and u ∈ f [s], then there exists u′ ∈ f [s′ ] such that u −
        2. if s −                                                                →S2 u′ ,
                                                                                b


where f [s] = { u | (s, u) ∈ f }. We write S1 ≤F S2 when such an f exists. The defining picture is forward in
time: starting from a related pair (s, u), every step of the implementation can be answered by a matching move of the
specification leading to a still related pair Lynch and Vaandrager [1995].
Theorem 1 (Soundness, [Lynch and Vaandrager, 1995]). S1 ≤F S2 =⇒ S1 ⊑T S2 .
Theorem 2 (Partial completeness, [Lynch and Vaandrager, 1995]). If S2 is deterministic and S1 ⊑T S2 , then S1 ≤F S2 .

Theorem 2 also exposes the limitation of forward simulations: completeness is only partial, and the determinism of B is
essential. When the specification is nondeterministic, trace inclusion need not be witnessed by any forward simulation.
The obstruction is temporal. A forward simulation must, at each step, commit to a matching specification state on the
basis of the past and present alone, whereas a correct implementation may resolve a nondeterministic choice later than
the specification does. This is the typical situation in linearizability arguments, where the abstract effect of an operation
is fixed only once some future event occurs.

3.1.3    Backward Simulations
Backward simulations are the dual remedy, propagating the relation backward in time so that “future” choices can be
matched. A backward simulation from S1 to S2 is a total relation b ⊆ states(S1 ) × states(S2 ) such that

        1. if s ∈ start(S1 ) then b[s] ⊆ start(S2 ), and
                a                                                              a
                →S1 s′ and u′ ∈ b[s′ ], then there exists u ∈ b[s] such that u −
        2. if s −                                                              →S2 u′ .
                                                                               b


We write S1 ≤B S2 when such a b exists, and S1 ≤iB S2 when moreover b is image-finite, i.e. b[s] is finite for every s.
The duality with forward simulations is not perfect. Two things differ: the totality requirement and the image-finite
condition. From any state the histories are finite but the futures may be infinite, so reasoning backward needs an extra
finiteness assumption to be sound for infinite behaviors Lynch and Vaandrager [1995].
Theorem 3 (Soundness, Lynch and Vaandrager [1995]). S1 ≤B S2 implies inclusion of finite traces, and S1 ≤iB
S2 =⇒ S1 ⊑T S2 (all traces, including infinite ones).

For finite traces a backward simulation is sound with no further hypotheses; for infinite traces image-finiteness lets one
assemble the infinitely many local matches into a single infinite specification execution, by a König’s-lemma argument
Lynch and Vaandrager [1995]. Backward simulations are likewise only partially complete, with the structural restriction
now on the implementation rather than the specification.
Theorem 4 (Partial completeness, Lynch and Vaandrager [1995]). If S1 is a forest and S1 ⊑T S2 , then S1 ≤B S2 ;
moreover, if S2 has finite invisible nondeterminism then S1 ≤iB S2 .

Neither forward nor backward simulations are complete on their own: each is guaranteed to exist only under the
structural hypotheses of Theorems 2 and 4. Their combination, however, is complete. Lynch and Vaandrager [1995]
show that whenever S1 ⊑T S2 there is an intermediate automaton S3 with a forward simulation from S1 to S3 and
a backward simulation from S3 to S2 (image-finite when S2 has finite invisible nondeterminism). Thus a forward
simulation, followed by a backward simulation, can witness any provable trace inclusion.


                                                                 6
                               Combining Axiomatic Program Logics with Refinement Proofs                               A P REPRINT



3.1.4      History and Prophecy Variables
This completeness has a familiar reading in terms of auxiliary state. A history relation is a forward simulation whose
inverse is a refinement, and a prophecy relation is a backward simulation whose inverse is a refinement [Lynch and
Vaandrager, 1995]; these are the abstract, relational counterparts of the auxiliary (history) variables of Owicki and
Gries [1976] and the prophecy variables of Abadi and Lamport [1991]. A history variable records information about
the past of an execution without affecting its behaviour, and adding one is what is needed when the only obstacle to a
refinement mapping is missing memory; this is the forward direction. A prophecy variable nondeterministically guesses
information about the future and later checks the guess, letting the specification anticipate a choice the implementation
has not yet made; this is the backward direction. The classical completeness theorem of Abadi and Lamport [1991]
states that, under machine closure, finite invisible nondeterminism, and internal continuity, trace inclusion always
implies the existence of a refinement mapping once the implementation is augmented with suitable history and prophecy
variables; the same statement, through the correspondence above, as the completeness of forward-then-backward
simulation. This is the theoretical justification for using a forward simulation, a backward simulation, or a composition
of the two as the simulation step of a refinement proof, and it is why the development in the remainder of the paper
treats both styles.
Remark 1 (From trace inclusion to invariants). Although the soundness and completeness results above are phrased
in terms of trace inclusion, the safety properties we transfer in this paper are sets of states rather than sets of traces
(Section 3.3). The two views meet through reachability: a forward simulation f from S1 to S2 relates every reachable
state of S1 to some reachable state of S2 , so an invariant of S2 pulls back, along f , to an invariant of S1 . This state
level transfer, and its analogue for backward simulations, is the form actually used in Sections 4 onward, where the
simulations are recast in the logic of actions and the transfer is carried out with the program logics of Section 3.2.

3.2       Axiomatic Models

There are new variants of Hoare logic. First, we would like to classify them. Program logics we consider define
axiomatic semantics on imperative programs. Hence, we assume that actions consist of triples of the form: a unary
predicate on pre-states, a binary predicate representing the program transformation and a unary predicate over post-states.
If a program logic fixes pre-states ( resp., post-states) and puts some restrictions on post-states (resp., pre-states) then it
is called a forward (resp., backward) logic. If the restriction requires being a subset (resp., superset) of some target set,
this logic is called an under-approximation (resp., over-approximation) logic. Target sets are either exact reachable
post-states of a program from a given pre-state set or exact and all pre-states needed by the program to reach a given
post-state set. To define these notions formally, we have to define the image and pre-image of a binary relation.
Definition 4 (Image and Pre-Image). Let R ⊆ Σ × Θ be a binary relation between two state spaces Σ and Θ.
Image of the set P ⊆ Σ is defined as
                                          R(P ) ≜ {σ ′ ∈ Θ | ∃σ.P (σ) ∧ R(σ, σ ′ )}
and pre-image of the set Q ⊆ Θ is defined as
                                       R−1 (Q) ≜ { σ ∈ Σ | ∃σ ′ . Q(σ ′ ) ∧ R(σ, σ ′ ) }.

If S ⊆ Σ × Σ is the binary predicate1 representing a program transformation, then S(P ) and S −1 (P ) represent the
strongest post-condition and the strongest precondition of S for a set of states P ⊆ Σ, respectively. 2 .
Using these definitions, one can define four program logics3 :
           • Hoare Logic: A forward over-approximation logic. A triple {P } S {Q} is a valid Hoare triple if and only if
             Q ⊇ S(P ).
           • Incorrectness Logic: A forward under-approximation logic. A triple [P ] S [Q] is a valid Incorrectness triple if
             and only if Q ⊆ S(P ).
      1
      Throughout the paper, we abuse the notation by using set and predicate notions in an interchanging way. For a unary predicate
P (σ), we assume the set P = {σ | P (σ)} and vice versa. Similarly, binary predicates correspond to binary relations over sets.
Predicates take their arguments from base program state sets like Σ and Θ.
    2
      Terms strongest postcondition and precondition are introduced with respect to semantics of Hoare Logic. They might be
confusing when used for other logics. Hence, we will stick to images and preimages from this point on.
    3
      Actually, there can be more. We deliberately omit the discussion on termination and non-determinism. Depending on what will
happen to non-terminating states and multiple states reachable from a single state in the presence of non-determinism or multiple
states terminating at the same target state, one can define different program logics. Decisions that logics we consider take on these
matters will be clear when we formally define them later. See [Verscht and Kaminski, 2025] for a more comprehensive treatment.


                                                                 7
                              Combining Axiomatic Program Logics with Refinement Proofs                        A P REPRINT



       • Lisbon Logic: A backward under-approximation logic Ascari et al. [2023]. A triple ⟨P ⟩ S ⟨Q⟩ is a valid
         Lisbon triple if and only if P ⊆ S −1 (Q).
       • Necessary Preconditions Logic: A backward over-approximation logic Cousot et al. [2013]. A triple (P ) S (Q)
         is a valid necessary precondition triple if and only if P ⊇ S −1 (Q).
Next, we will formally describe these logic in a language similar to logic of actions. For the following definitions,
assume S ⊆ Σ × Σ is the program transition relation where Σ is the set of states of S.
Definition 5 (Valid Hoare Triple). A Hoare triple {P } S {Q} is valid if and only if
                                           ∀σ ′ : (∃σ : P (σ) ∧ S(σ, σ ′ )) =⇒ Q(σ ′ )
Corollary 1. A Hoare triple {P } S {Q} is valid if and only if
                                             ∀σ, σ ′ : P (σ) ∧ S(σ, σ ′ ) =⇒ Q(σ ′ )
Definition 6 (Valid Incorrectness Triple). An Incorrectness triple [P ] S [Q] is a valid Incorrectness triple if and only if
                                             ∀σ ′ . Q(σ ′ ) =⇒ ∃σ. P (σ) ∧ S(σ, σ ′ ).
Definition 7 (Valid Lisbon Triple). A Lisbon triple ⟨P ⟩ S ⟨Q⟩ is a valid Lisbon triple if and only if
                                             ∀σ. P (σ) =⇒ ∃σ ′ . Q(σ ′ ) ∧ S(σ, σ ′ )
Definition 8 (Valid Necessary Preconditions Triple). A Necessary Preconditions triple (P ) S (Q) is a valid Necessary
Preconditions triple if and only if
                                     ∀σ. (∃σ ′ . Q(σ ′ ) ∧ S(σ, σ ′ )) =⇒ P (σ)
Corollary 2. A Necessary Preconditions triple (P ) S (Q) is valid if and only if
                                             ∀σ, σ ′ : Q(σ ′ ) ∧ S(σ, σ ′ ) =⇒ P (σ)

Corollary 1 and 2 are useful because it shows us checking validity of a Hoare triple and a Necessary Preconditions
triple lays in the decidable fragment of the FOL (first order logic) since there is no quantifier alternation provided that
the program transformation predicate S is also inside the decidable fragment.
The validity criteria of Section 5 single out programs whose transition relation behaves functionally in one direction or
the other. We record these properties of a transition relation S ⊆ Σ × Σ.
Definition 9 (Functionality conditions). A program with transition relation S ⊆ Σ × Σ is
       • total if ∀σ. ∃σ ′ . S(σ, σ ′ );
       • deterministic if ∀σ, σ1′ , σ2′ . S(σ, σ1′ ) ∧ S(σ, σ2′ ) =⇒ σ1′ = σ2′ ;
       • backward total if ∀σ ′ . ∃σ. S(σ, σ ′ );
       • backward deterministic if ∀σ1 , σ2 , σ ′ . S(σ1 , σ ′ ) ∧ S(σ2 , σ ′ ) =⇒ σ1 = σ2 .
A total, deterministic S is the graph of a total function on Σ; a backward total, backward deterministic S is one whose
converse is a total function. These are exactly the conditions under which the existential witness in a forward (resp.
backward) simulation is uniquely pinned, which is what Theorems 8 and 11 exploit.

3.3   Invariants

We take a safety property of a program to be a set of states J ⊆ Σ (equivalently, a predicate on states; we use the set and
predicate views interchangeably). A program satisfies J when every state it can ever reach lies in J. Writing reach(S)
for the set of states reachable from Init under finitely many steps of the transition relation S, this is the inclusion
                                                         reach(S) ⊆ J.
A set J with this property is called an invariant of the program: an over-approximation of its reachable states Manna
and Pnueli [1995], Cousot and Cousot [1977]. The strongest invariant is reach(S) itself, and every weaker invariant is
obtained by enlarging it. We deliberately phrase safety in terms of states rather than traces: it is the formulation that
meshes with the program logics of Section 3.2, whose pre- and post-conditions are themselves predicates on states.
Reachability quantifies over all executions, so checking reach(S) ⊆ J directly is a global obligation. The standard
device for reducing it to a local one is to require J to be closed under the transition relation, which turns the global
inclusion into a single step check Floyd [1967], Manna and Pnueli [1995]. In the image notation of Section 4 this
closure is exactly the validity of the Hoare triple {J} S {J}, since {J} S {J} holds iff S(J) ⊆ J. This motivates the
following notion.


                                                                8
                            Combining Axiomatic Program Logics with Refinement Proofs                         A P REPRINT



Definition 10 (Hoare invariant). A set I ⊆ Σ is a Hoare invariant of a program with transition relation S and initial
states Init if

      1. Init ⊆ I                                                                                         (initiation), and
      2. {I} S {I} is a valid Hoare triple, i.e. S(I) ⊆ I                                                   (consecution).

Definition 10 is the classical notion of an inductive invariant, whose two conditions are traditionally called initiation
and consecution, going back to Floyd’s inductive assertions Floyd [1967] and presented in this transition system form
by Manna and Pnueli Manna and Pnueli [1995]; we phrase it through the Hoare triple of Section 3.2 to align it with the
program logics used in the rest of the paper. Inductiveness makes a Hoare invariant a genuine invariant where a one step
induction is enough, with no reasoning about whole executions.
Proposition 1. Every Hoare invariant I is an invariant: reach(S) ⊆ I.

Proof. By induction on the length of a reaching execution. Every state of length 0 is in Init ⊆ I by initiation. If a
reachable state s lies in I and S(s, s′ ), then s′ ∈ S(I) ⊆ I by consecution. Hence reach(S) ⊆ I.

The converse fails: an invariant need not be closed under S, and proving a desired safety property typically requires
strengthening it to a Hoare invariant that implies it Manna and Pnueli [1995], Cousot and Cousot [1977]. This is the
role Hoare invariants play in our development. On the specification we establish a Hoare invariant {I} S2 {I} with
Init 2 ⊆ I; the simulation relation then transfers it to the implementation (Remark 1), yielding a Hoare invariant on S1
whose initiation and consecution are discharged by the transfer theorems of Section 4. Thus a safety property proved
once, on the simpler specification, is carried down to the implementation as a state predicate rather than as a property of
traces.

4   Axiomatic Models of Forward and Backward Simulations
Relational Hoare logics (RHLs) provide axiomatic semantics for reasoning over multiple programs. In this work, we
focus on logics relating two programs. The class of RHLs used in refinement proofs are called ∀∃ RHLs since they are
used for proving for all steps of the implementation program, there exists a related state of the specification program.
For the scope this work, we want RHLs corresponding to the standard backward and forward simulation definitions of
Lynch and Vaandrager [1995].
We start by defining forward relational triple (FRT) and backward relational triple (BRT) in order to define forward and
backward simulations in logic of actions. Let Σ and T be states of programs S1 and S2 ; and P and Q ⊆ Σ × T be
binary predicates.
Definition 11 (Forward Relational Triple). Let S1 and S2 be two programs executing on states from Σ and T , and P
and Q ⊆ Σ × T be a binary predicate. Then, |P ⟩ S1 ; S2 |Q⟩ is a valid Forward Relational Triple if and only if
                             ∀σ, σ ′ , τ.S1 (σ, σ ′ ) ∧ P (σ, τ ) =⇒ ∃τ ′ .S2 (τ, τ ′ ) ∧ Q(σ ′ , τ ′ )
Definition 12 (Backward Relational Triple). Let S1 and S2 be two programs executing on states from Σ and T , and P
and Q ⊆ Σ × T be a binary predicate. Then, |P ⟩ S1 ; S2 |Q⟩ is a valid Backward Relational Triple if and only if
                             ∀σ, σ ′ , τ ′ .S1 (σ, σ ′ ) ∧ P (σ ′ , τ ′ ) =⇒ ∃τ.S2 (τ, τ ′ ) ∧ Q(σ, τ )
Definition 13 (Forward Simulation Relation). A relation R ⊆ Σ × T is a forward simulation relation if
                                               R[start(S1 )] ∩ start(S2 ) ̸= ∅
                      for all atomic coordinated steps C1 , C2 of S1 , S2 ; we have |R⟩ C1 ; C2 |R⟩
Definition 14 (Backward Simulation Relation). A relation R ⊆ Σ × T is a backward simulation relation if
                                                 R[start(S1 )] ⊆ start(S2 )
                      for all atomic coordinated steps C1 , C2 of S1 , S2 ; we have ⟨R| C1 ; C2 ⟨R|

A standard refinement proof consists of two parts: (i) showing correctness of some properties on the specification
program, (ii) showing the implementation refines the specification by finding a simulation relation between two
programs. Then, one can infer some knowledge about the implementation.


                                                                 9
                             Combining Axiomatic Program Logics with Refinement Proofs                            A P REPRINT



In this work, we want to understand what kind of guarantees we can get for implementation programs if we use a
functional program logic from Section 3.2 for the first step and a ∀∃ RHL from Section 4 for the second step.
We claim that if a property represented by a Hoare invariant holds for the specification program and there is a forward
simulation relation from the implementation to the specification, then the corresponding property imposed by the
simulation relation holds for the implementation as a Hoare invariant, too. Similarly, an invariant that holds for the
specification program, and there is a backward simulation relation from the implementation to the specification, then
the corresponding property imposed by the simulation relation holds for the implementation as an invariant too.
Definition 15 (Forward Image along a Simulation Relation). Let R(σ, τ ) relate implementation states σ to specification
states τ . For a predicate P on implementation states,
                                         R(P ) ≜ { τ | ∃σ. P (σ) ∧ R(σ, τ ) }.
Definition 16 (Inverse Image along a Simulation Relation). Let R(σ, τ ) be as above. For a predicate Q on specification
states,
                                     R−1 (Q) ≜ { σ | ∃τ. Q(τ ) ∧ R(σ, τ ) }.
Theorem 5. Let I be a Hoare invariant on S2 , and R(S1 , S2 ) be a forward simulation relation. Then, R−1 (I) is a
Hoare invariant on S1 .

Proof. We verify that R−1 (I) satisfies initiation and consecution on S1 .
Initiation. Let σ ∈ Init(S1 ). By the start condition of Definition 10 there is τ ∈ Init(S2 ) with R(σ, τ ). Since
I is a Hoare invariant on S2 , initiation of I gives Init(S2 ) ⊆ I, so I(τ ). By Definition 13, σ ∈ R−1 (I). Hence
Init(S1 ) ⊆ R−1 (I).
Consecution. Let σ ∈ R−1 (I) and S1 (σ, σ ′ ). By Definition 13 there is τ with R(σ, τ ) and I(τ ). The forward
step condition (Definition 10) applied to S1 (σ, σ ′ ) and R(σ, τ ) yields τ ′ with S2 (τ, τ ′ ) and R(σ ′ , τ ′ ). Consecution
of I, i.e. S       ⊆ I, gives I(τ ′ ) from I(τ ) ∧ S2 (τ, τ ′ ). Thus R(σ ′ , τ ′ ) and I(τ ′ ), so σ ′ ∈ R−1 (I). Hence
            2 (I) −1
S1 R (I) ⊆ R (I), i.e. {R−1 (I)} S1 {R−1 (I)} is valid.
     −1


Therefore R−1 (I) is a Hoare invariant on S1 .
Lemma 1. Let σ be a reachable state in S1 and let R(S1 , S2 ) be a forward simulation. Then ∃τ.R(σ, τ )∧ τ is
reachable in S2 .

Proof. By induction on the length n of an execution of S1 reaching σ.
Base (n = 0). Then σ ∈ Init(S1 ). By the start condition there is τ ∈ Init(S2 ) with R(σ, τ ), and τ is reachable.
Step. Let σ be reached by an execution · · · σ0 → σ with σ0 reachable in n − 1 steps and S1 (σ0 , σ). By the induction
hypothesis there is a reachable τ0 with R(σ0 , τ0 ). The forward step condition applied to S1 (σ0 , σ) and R(σ0 , τ0 ) yields
τ with S2 (τ0 , τ ) and R(σ, τ ). Since τ0 is reachable and S2 (τ0 , τ ), τ is reachable.
Theorem 6. Let I be an invariant on S2 , and R(S1 , S2 ) be a forward simulation relation. Then R−1 (I) is an invariant
on S1 .

Proof. Let σ ∈ reach(S1 ). By Lemma 1 there is τ with R(σ, τ ) and τ ∈ reach(S2 ). Since I is an invariant on S2 ,
reach(S2 ) ⊆ I, so I(τ ). By Definition 13, σ ∈ R−1 (I). Hence reach(S1 ) ⊆ R−1 (I), i.e. R−1 (I) is an invariant on
S1 .
Lemma 2. Let σ be a reachable state in S1 , and R(S1 , S2 ) be a backward simulation relation. Then, ∀τ.R(σ, τ ) =⇒ τ
is reachable in S2 .

Proof. By induction on the length n of an execution of S1 reaching σ.
Base (n = 0). Then σ ∈ Init(S1 ). By the initiation condition of Definition 11, every τ with R(σ, τ ) lies in Init(S2 )
and is therefore reachable.
Step. Let σ be reached by · · · σ0 → σ with σ0 reachable and S1 (σ0 , σ), and let τ be any state with R(σ, τ ). The
backward step condition applied to S1 (σ0 , σ) and R(σ, τ ) yields τ0 with S2 (τ0 , τ ) and R(σ0 , τ0 ). By the induction
hypothesis applied to the reachable σ0 and τ0 (which satisfies R(σ0 , τ0 )), τ0 is reachable; since S2 (τ0 , τ ), τ is
reachable.


                                                              10
                            Combining Axiomatic Program Logics with Refinement Proofs                         A P REPRINT



Theorem 7. Let I be an invariant on S2 , and R(S1 , S2 ) be a backward simulation relation. Then, R−1 (I) is an
invariant on S1 .

Proof. Let σ ∈ reach(S1 ). By totality (Definition 11) there is τ with R(σ, τ ). By Lemma 2, τ ∈ reach(S2 ). Since I
is an invariant on S2 , I(τ ). By Definition 13, σ ∈ R−1 (I). Hence reach(S1 ) ⊆ R−1 (I), i.e. R−1 (I) is an invariant on
S1 .
Corollary 3. Let I be a Hoare invariant on S2 , and R(S1 , S2 ) be a backward simulation relation. Then, R−1 (I) is an
invariant on S1 .

Proof. Every Hoare invariant is an invariant (Proposition 1), so I is an invariant on S2 and Theorem 7 gives that R−1 (I)
is an invariant on S1 .

4.1   Application: Functional Correctness of the Counters

We apply the theory to the three counters of Section 2, whose states carry the history field old and whose simulation
relations contain the history containments (B2) and (F4). We transfer one property down the chain: that the history set
records every value up to the current count. On each machine it has the shape ∀v ≤ count. v ∈ old , with the count
instantiated to x, |C|, and L + R in turn. Established as a Hoare invariant on the sequential counter, it is carried to NDC
by the backward relation and to LR by the forward relation, arriving as ∀v ≤ L + R. v ∈ old lr on the implementation.
We first record the contents of the history fields fixed by the update rules of Section 2. They are used to interpret the
transferred invariants, not in the transfer itself.
Proposition 2 (Structural invariants). The augmented machines satisfy, at all reachable states,
                  old s = {0, . . . , x},     old n = {0, . . . , |C| + |P |}, old lr = {0, . . . , L + R}.

Proof. Each is a Hoare invariant by one step induction: initially every count is 0 and old = {0}; each increment raises
the relevant begun count (x, |C| + |P |, and L + R respectively) by one and inserts exactly that new value into old ;
reads change neither.

The two history containments are not independent obligations: under Proposition 2, (B2) old s ⊆ old n is the upper half
of (B1), and (F4) old n ⊆ old lr follows from (F1) once (F5) and (F6) force P = ∅ at related states; this is why adding
the clauses left the simulation proofs of Section 2 essentially unchanged.

The specification invariant.     On the sequential counter we take
                                            Is ≜ ∀v. v ≤ x ⇒ v ∈ old s ,
“every value up to the current count has been recorded.”
Proposition 3. Is is a Hoare invariant on the sequential counter.

Proof. Initiation. Initially x = 0 and old s = {0}, so the only v ≤ 0 is v = 0 ∈ old s .
Consecution. increment sends x to x + 1 and old s to old s ∪ {x + 1}; assuming ∀v ≤ x. v ∈ old s , any v ≤ x + 1 is
either ≤ x, hence in old s , or equal to x + 1 ∈ old s ∪ {x + 1}. read changes neither x nor old s .

                                                        −1
Step 1: Seq → NDC (backward).          By Corollary 4, RB  (Is ) is an invariant on NDC. Define
                                         In ≜ ∀v. v ≤ |C| ⇒ v ∈ old n .
Corollary 4. In is an invariant on the NDC counter.
                                                                              −1                        −1
Proof. Since a superset of an invariant is an invariant, it suffices to show RB  (Is ) ⊆ In . Let σn ∈ RB  (Is ), witnessed
by a Seq state τs with RB (σn , τs ) and Is (τs ), and let v ≤ |C|. By (B1), |C| ≤ x, so v ≤ x; by Is (τs ), v ∈ old s ; by
the history clause (B2), old s ⊆ old n . Hence v ∈ old n .

The bound |C| in In is the lower end of the interval [|C|, |C| + |P |] of (B1): the inverse image existentially chooses the
sequential count x, and the weakest, hence the only guaranteed, witness sits at x = |C|. In fact old n contains every
value up to |C| + |P | (Proposition 2), but the backward transfer certifies only the range up to |C|; the pending range is
not carried across. This is the one place in the chain where a relation weakens the transferred predicate, and it is why In
              −1
is stated as RB  (Is ) subsetted rather than as a count substituted copy of Is .


                                                            11
                              Combining Axiomatic Program Logics with Refinement Proofs                             A P REPRINT



Step 2: NDC → LR (forward). In is an invariant – not a Hoare invariant – on NDC, so Theorem 5 does not apply
and we use Theorem 6: RF−1 (In ) is an invariant on LR. Define
                                             Ilr ≜ ∀v. v ≤ L + R ⇒ v ∈ old lr .
Corollary 5. Ilr is an invariant on the LR counter.

Proof. It suffices to show RF−1 (In ) ⊆ Ilr . Let σlr ∈ RF−1 (In ), witnessed by an NDC state σn with RF (σlr , σn ) and
In (σn ), and let v ≤ L + R. By (F1), L + R = |C|, so v ≤ |C|; by In (σn ), v ∈ old n ; by the history clause (F4),
old n ⊆ old lr . Hence v ∈ old lr .

Unlike Step 1, this step loses nothing: (F1) is an equality, L + R = |C|, so the bound transfers at full strength with no
existential slack.

Summary. A single Hoare invariant on the trivially correct sequential counter (Proposition 3) is transported, by
Corollary 4 and then Theorem 6, to the containment invariant ∀v ≤ L + R. v ∈ old lr on the LR implementation
(Corollary 5). The same containment is, of course, immediate from the LR update rule (Proposition 2); the content
of the result is that it is reached purely by transfer – through the relation clauses (B1), (B2), (F1), (F4) – with no
reasoning about the LR machine’s own dynamics. The backward leg weakens the predicate to the floor of the (B1)
interval, while the forward leg, resting on the equality (F1), carries it across exactly. Finally, since an LR read reports
vL (id) + R ≤ L + R, the containment Ilr gives olr (id) ∈ old lr : every completed read returns a value the counter
realized.

5    Checking Validity of Forward and Backward Simulations
We are using forward and backward simulations to relate the implementation to the specification. In order to verify that
a relation is a forward simulation or a backward simulation, functional program logic can be used. For verifying that a
relation is a forward simulation, Hoare triples can be used as in Theorem 8 under the assumption that the specification
program is total and deterministic.
Theorem 8. If S2 is total and deterministic, then {R(σ, τ )} S2 ; S1 ; {R(σ, τ )} is a valid Hoare triple if and only if R is
a forward simulation.

Proof. Let T be the product transition T (σ, τ ), (σ ′ , τ ′ ) ≡ S1 (σ, σ ′ ) ∧ S2 (τ, τ ′ ). By Corollary 1, the Hoare triple
                                                              

{R} T {R} is valid iff
                            (⋆)    ∀σ, σ ′ , τ, τ ′ . R(σ, τ ) ∧ S1 (σ, σ ′ ) ∧ S2 (τ, τ ′ ) ⇒ R(σ ′ , τ ′ ).
The forward simulation condition (Definition 10) is
                            (†)   ∀σ, σ ′ , τ. R(σ, τ ) ∧ S1 (σ, σ ′ ) ⇒ ∃τ ′ . S2 (τ, τ ′ ) ∧ R(σ ′ , τ ′ ).

(† ⇒ ⋆) Assume (†) and the antecedent of (⋆). From R(σ, τ ) ∧ S1 (σ, σ ′ ), (†) gives τ ′′ with S2 (τ, τ ′′ ) ∧ R(σ ′ , τ ′′ ). As
S2 is deterministic and S2 (τ, τ ′ ) holds, τ ′′ = τ ′ , hence R(σ ′ , τ ′ ).
(⋆ ⇒ †) Assume (⋆) and R(σ, τ ) ∧ S1 (σ, σ ′ ). As S2 is total there is τ ′ with S2 (τ, τ ′ ). Then (⋆) gives R(σ ′ , τ ′ ), so
∃τ ′ . S2 (τ, τ ′ ) ∧ R(σ ′ , τ ′ ).

However, the specification being total and deterministic cannot always be guaranteed. In such a case, Lisbon triples can
be used to verify that a relation is a forward simulation as in Theorem 9, or alternatively as in Theorem 10.
Theorem 9. ⟨R(σ, τ ) ∧ S1 (σ, σ ′ )⟩ S2 (τ, τ ′ ) ⟨R(σ ′ , τ ′ )⟩ is a valid Lisbon triple ⇐⇒ R is a forward simulation.

Proof. The program S2 transforms the specification state τ into τ ′ , and σ, σ ′ are free. By the definition of a valid
Lisbon triple (Definition 7), ⟨R(σ, τ ) ∧ S1 (σ, σ ′ )⟩ S2 ⟨R(σ ′ , τ ′ )⟩ is valid iff
                               ∀τ. R(σ, τ ) ∧ S1 (σ, σ ′ ) ⇒ ∃τ ′ . R(σ ′ , τ ′ ) ∧ S2 (τ, τ ′ ).
                                                            

A triple with free variables is valid iff it holds for all their valuations; taking the conjunction over σ, σ ′ gives
                               ∀σ, σ ′ , τ. R(σ, τ ) ∧ S1 (σ, σ ′ ) ⇒ ∃τ ′ . S2 (τ, τ ′ ) ∧ R(σ ′ , τ ′ ),
which is exactly Definition 10. (When S1 (σ, σ ′ ) is false the premise fails and the triple holds vacuously, matching the
vacuous case of the simulation condition.)


                                                                  12
                               Combining Axiomatic Program Logics with Refinement Proofs                              A P REPRINT



Theorem 10. Let R1 = {σ|∃τ.R(σ, τ )} and R1 (σ) = {τ |σ ∈ R1 ∧ R(σ, τ )}. Then,
(∀σ, σ ′ .S1 (σ, σ ′ ) =⇒ ⟨R1 (σ)⟩ S2 ⟨R1 (σ ′ )⟩ is a valid Lisbon triple) ⇐⇒ R is a forward simulation.

Proof. For σ ∈ R1 we have R1 (σ) = {τ | R(σ, τ )}, and for σ ∈        / R1 we have R1 (σ) = ∅ = {τ | R(σ, τ )}; in both
cases R1 (σ)(τ ) ⇐⇒ R(σ, τ ), and likewise for σ ′ . By Definition 7, for fixed σ, σ ′ the triple ⟨R1 (σ)⟩ S2 ⟨R1 (σ ′ )⟩ is
valid iff
                                        ∀τ. R(σ, τ ) ⇒ ∃τ ′ . R(σ ′ , τ ′ ) ∧ S2 (τ, τ ′ ).
Hence the stated condition ∀σ, σ . S1 (σ, σ ′ ) ⇒ (this triple is valid) is
                                 ′

                            ∀σ, σ ′ , τ. S1 (σ, σ ′ ) ∧ R(σ, τ ) ⇒ ∃τ ′ . S2 (τ, τ ′ ) ∧ R(σ ′ , τ ′ ),
which is the forward simulation condition (Definition 10).

The relation defined in 2.4.1 is verified as a forward simulation relation using Theorem 10. For each implementation
operation, the corresponding Lisbon triple is shown to be valid using the proof rules defined by Ascari et al. [2023]. See
Appendix A.1 for the full proof.
Similarly, to verify that a relation is a backward simulation, Necessary Precondition triples can be used as in Theorem
11 under the assumption that the specification is backward total and backward deterministic.
Theorem 11. If S2 is backward total and backward deterministic, then (R(σ, τ )) S2 ; S1 ; (R(σ, τ )) is a valid Necessary
Preconditions triple ⇐⇒ R is a backward simulation.

Proof. Let T be the product transition as in the proof of Theorem 8. By Corollary 2, the Necessary Preconditions triple
(R) T (R) is valid iff
                         (⋆) ∀σ, σ ′ , τ, τ ′ . R(σ ′ , τ ′ ) ∧ S1 (σ, σ ′ ) ∧ S2 (τ, τ ′ ) ⇒ R(σ, τ ).
The backward simulation condition (Definition 11) is
                        (†) ∀σ, σ ′ , τ ′ . S1 (σ, σ ′ ) ∧ R(σ ′ , τ ′ ) ⇒ ∃τ. S2 (τ, τ ′ ) ∧ R(σ, τ ).
(† ⇒ ⋆) Assume (†) and the antecedent of (⋆). From S1 (σ, σ ′ ) ∧ R(σ ′ , τ ′ ), (†) gives τ ′′ with S2 (τ ′′ , τ ′ ) ∧ R(σ, τ ′′ ).
As S2 is backward deterministic and S2 (τ, τ ′ ) holds, τ ′′ = τ , hence R(σ, τ ).
(⋆ ⇒ †) Assume (⋆) and S1 (σ, σ ′ ) ∧ R(σ ′ , τ ′ ). As S2 is backward total there is τ with S2 (τ, τ ′ ). Then (⋆) gives
R(σ, τ ), so ∃τ. S2 (τ, τ ′ ) ∧ R(σ, τ ).

If the specification is not backward total or backward deterministic, Incorrectness triples can be used to verify that the
relation is a backward simulation as in Theorem 12, or alternatively as in Theorem 13.
Theorem 12. [R(σ, τ )] S2 (τ, τ ′ ) [R(σ ′ , τ ′ )∧S1 (σ, σ ′ )] is a valid Incorrectness triple ⇐⇒ R is a backward simulation.

Proof. The program S2 transforms τ into τ ′ , and σ, σ ′ are free. By the definition of a valid Incorrectness triple
(Definition 6), [R(σ, τ )] S2 [R(σ ′ , τ ′ ) ∧ S1 (σ, σ ′ )] is valid iff
                                ∀τ ′ . R(σ ′ , τ ′ ) ∧ S1 (σ, σ ′ ) ⇒ ∃τ. R(σ, τ ) ∧ S2 (τ, τ ′ ).
                                                                    

Holding for all valuations of the free σ, σ ′ , this is
                            ∀σ, σ ′ , τ ′ . R(σ ′ , τ ′ ) ∧ S1 (σ, σ ′ ) ⇒ ∃τ. S2 (τ, τ ′ ) ∧ R(σ, τ ),
which is the backward simulation condition (Definition 11).
Theorem 13. Let R1 = {σ|∃τ.R(σ, τ )} and R1 (σ) = {τ |σ ∈ R1 ∧ R(σ, τ )}. Then,
(∀σ, σ ′ .S1 (σ, σ ′ ) =⇒ [R1 (σ)] S2 [R1 (σ ′ )] is a valid Incorrectness triple) ⇐⇒ R is a backward simulation.

Proof. As in the proof of Theorem 10, R1 (σ)(τ ) ⇐⇒ R(σ, τ ) and R1 (σ ′ )(τ ′ ) ⇐⇒ R(σ ′ , τ ′ ). By Definition 6, for
fixed σ, σ ′ the triple [R1 (σ)] S2 [R1 (σ ′ )] is valid iff
                                            ∀τ ′ . R(σ ′ , τ ′ ) ⇒ ∃τ. R(σ, τ ) ∧ S2 (τ, τ ′ ).
               ′         ′
Hence ∀σ, σ . S1 (σ, σ ) ⇒ (this triple is valid) is
                               ∀σ, σ ′ , τ ′ . S1 (σ, σ ′ ) ∧ R(σ ′ , τ ′ ) ⇒ ∃τ. S2 (τ, τ ′ ) ∧ R(σ, τ ),
the backward simulation condition (Definition 11).

The relation defined in 2.4.2 is verified as a backward simulation relation using Theorem 13. For each implementation
operation, the corresponding Incorrectness triple is shown to be valid using the proof rules defined by O’Hearn [2019].
See Appendix A.2 for the full proof.


                                                                  13
                            Combining Axiomatic Program Logics with Refinement Proofs                        A P REPRINT



6   Conclusions
We have related axiomatic functional verification logic to refinement proofs through simulation relations. On the transfer
side, a forward simulation carries a Hoare invariant of the specification to a Hoare invariant of the implementation, and
forward and backward simulations carry ordinary invariants, so a safety property proved once on a simple specification
descends to the implementation as a state predicate. On the discharge side, we characterized forward simulations by
the validity of Hoare and Lisbon triples and backward simulations by the validity of Necessary Preconditions and
Incorrectness triples, reducing the simulation obligation to a triple in a standard functional logic.
We illustrated the framework on a concurrent counter. Linking a Left–Right implementation to an atomic sequential
specification through an intermediate nondeterministic concurrent counter, a forward simulation from LR counter to
NDC counter, and a backward simulation from the NDC counter to the sequential counter, we transferred the counter’s
safety bound down the chain without reasoning directly about the implementation’s interleavings. The two simulations
were verified operation by operation using Lisbon and Incorrectness triples (Appendices A.1 and A.2).
We aim to extend the work in two directions. The first concerns the reach of the transfer results. We have shown
that forward simulations preserve Hoare invariants and that backward simulations preserve invariants obtained by
backward reasoning; it remains open which properties expressible in Incorrectness logic, Lisbon logic, and the Necessary
Preconditions fragments are preserved under forward and backward simulations, and under what structural conditions.
A systematic map from (logic, simulation direction) pairs to the class of preserved properties is the main goal. The
second is to test the discharge method on implementations whose linearization points are genuinely value dependent,
richer concurrent data structures than the counter, to see how far the operation by operation triple verification scales.
Mechanizing the transfer theorems and the worked example in a proof assistant such as Lean 4 would additionally
provide machine checked guarantees.




                                                           14
                          Combining Axiomatic Program Logics with Refinement Proofs                     A P REPRINT



References
C. A. R. Hoare. An axiomatic basis for computer programming. Communications of the ACM, 12(10):576–580, 1969.
Peter W. O’Hearn. Incorrectness logic. Proc. ACM Program. Lang., 4(POPL), December 2019. doi:10.1145/3371078.
  URL https://doi.org/10.1145/3371078.
Flavio Ascari, Roberto Bruni, Roberta Gori, and Francesco Logozzo. Sufficient incorrectness logic: SIL and separation
  SIL. CoRR, abs/2310.18156, 2023. doi:10.48550/ARXIV.2310.18156. URL https://doi.org/10.48550/arXiv.
  2310.18156.
Patrick Cousot, Radhia Cousot, Manuel Fähndrich, and Francesco Logozzo. Automatic inference of necessary
  preconditions. In Roberto Giacobazzi, Josh Berdine, and Isabella Mastroeni, editors, Verification, Model Checking,
  and Abstract Interpretation, pages 128–148, Berlin, Heidelberg, 2013. Springer Berlin Heidelberg. ISBN 978-3-642-
  35873-9.
Nancy A. Lynch and Frits W. Vaandrager. Forward and backward simulations: I. untimed systems. Inf. Comput., 121
  (2):214–233, 1995. doi:10.1006/INCO.1995.1134. URL https://doi.org/10.1006/inco.1995.1134.
Susan Owicki and David Gries. An axiomatic proof technique for parallel programs I. Acta Informatica, 6(4):319–340,
  1976.
Martín Abadi and Leslie Lamport. The existence of refinement mappings. Theoretical Computer Science, 82(2):
  253–284, 1991.
Lena Verscht and Benjamin Lucien Kaminski. A taxonomy of hoare-like logics: Towards a holistic view using predicate
  transformers and kleene algebras with top and tests. Proc. ACM Program. Lang., 9(POPL):1782–1811, 2025.
  doi:10.1145/3704896. URL https://doi.org/10.1145/3704896.
Zohar Manna and Amir Pnueli. Temporal Verification of Reactive Systems: Safety. Springer-Verlag, 1995.
Patrick Cousot and Radhia Cousot. Abstract interpretation: A unified lattice model for static analysis of programs by
  construction or approximation of fixpoints. In POPL, pages 238–252, 1977.
Robert W. Floyd. Assigning meanings to programs. In Proc. Symposia in Applied Mathematics, volume 19, pages
  19–32. American Mathematical Society, 1967.




                                                        15
                             Combining Axiomatic Program Logics with Refinement Proofs                              A P REPRINT



A     Verification of Simulation Relations
A.1   Forward Simulation Verification

By Theorem 10, it suffices to show that for every implementation step (σ, σ ′ ) of Ai and every τ with R(σ, τ ), the
Lisbon triple ⟨R(σ, τ )⟩ c1 ; . . . ; cn ⟨R(σ ′ , τ ′ )⟩ is valid for the corresponding sequence of specification steps. We derive
each triple with the SIL proof rules. The following lemma is used in the increment case.
Lemma 3. If R(σ, τ ) then P = ∅.

Proof. If id ∈ P then pc n (id) = DONE ̸= DONE, so (F5) gives pc lr (id) ̸= DONE; as LR increments are atomic,
pc lr (id) = DONE, and then F 6 forces pc n (id) = DONE, contradicting DONE.

Case 1: increment(id ).
Implementation step:
Assumes pclr (id ) = INIT; nondeterministically sets either L ← L+1 or R ← R+1; inserts the new L + R into oldlr ;
sets pclr (id ) ← DONE. Without loss of generality take L ← L+1 (the case R ← R+1 is symmetric).
Corresponding specification steps:
c1 = begin_increment(id ); c2 = return_increment(id ).
Precondition and postcondition:
               P = ((|C| = L + R)
                    ∧ (∀id ∈ I. pclr (id) = MID ⇐⇒ id ∈ A)
                    ∧ (∀id ∈ A. |M S(id)| ≤ vL (id) + R ≤ |M S(id) ∪ Y S(id)|)
                    ∧ (oldn ⊆ oldlr )
                    ∧ (∀id ∈ I. pcn (id) ̸= IN IT =⇒ pclr (id) ̸= IN IT ∧ ilr (id) = in (id))
                    ∧ (∀id ∈ I. pclr (id) = DON E =⇒ pcn (id) = DON E ∧ olr (id) = on (id)))
                 Q = ((|C ′ | = L+R+1)
                       ∧ (∀id ′ ∈ I. pc′lr (id ′ ) = MID ⇐⇒ id ′ ∈ A′ )
                       ∧ (∀id ′ ∈ A′ . |M S ′ (id ′ )| ≤ vL (id ′ ) + R ≤ |M S ′ (id ′ ) ∪ Y S ′ (id ′ )|)
                       ∧ (old′n ⊆ old′lr )
                       ∧ (∀id ′ ∈ I. pc′n (id ′ ) ̸= INIT =⇒ pc′lr (id ′ ) ̸= INIT ∧ i′lr (id ′ ) = in′ (id ′ ))
                       ∧ (∀id ′ ∈ I. pc′lr (id ′ ) = DONE =⇒ pc′n (id ′ ) = DONE ∧ o′lr (id ′ ) = on′ (id ′ ))
Proof of Lisbon triple ⟨P ⟩ c1 ; c2 ⟨Q⟩.
Define the intermediate condition:
                Q1 = (|C ∪ {id }| = L+R+1)
                        ∧ (∀id ′ ∈ I. pclr (id ′ ) = MID ⇐⇒ id ′ ∈ A)
                        ∧ (∀id ′ ∈ A. |M S(id ′ )| ≤ vL (id ′ ) + R ≤ |M S(id ′ ) ∪ Y S(id ′ )|)
                        ∧ (oldn ⊆ old′lr )
                        ∧ (∀id ′ ∈ I. pcn (id ′ ) ̸= INIT =⇒ pclr (id ′ ) ̸= INIT ∧ ilr (id ′ ) = in (id ′ ))
                      ∧ (∀id ′ ∈ I. pclr (id ′ ) = DONE =⇒ pcn (id ′ ) = DONE ∧ olr (id ′ ) = on (id ′ ))
and the pre-intermediate condition:
                Q0 = (|C ∪ {id }| = L+R+1)
                        ∧ (∀id ′ ∈ I. pclr (id ′ ) = MID ⇐⇒ id ′ ∈ A)
                        ∧ (∀id ′ ∈ A. |M S(id ′ )| ≤ vL (id ′ ) + R ≤ |M S(id ′ ) ∪ Y S(id ′ ) ∪ {id }|)
                        ∧ (oldn ⊆ old′lr )
                        ∧ (∀id ′ ∈ I. pcn (id ′ ) ̸= INIT =⇒ pclr (id ′ ) ̸= INIT ∧ ilr (id ′ ) = in (id ′ ))
                        ∧ (∀id ′ ∈ I. pclr (id ′ ) = DONE =⇒ pcn (id ′ ) = DONE ∧ olr (id ′ ) = on (id ′ ))


                                                                 16
                             Combining Axiomatic Program Logics with Refinement Proofs                             A P REPRINT



By the atom rule, ⟨Q1 ⟩ c2 ⟨Q⟩ is valid: c2 moves id from P to C and sets pcn (id ) ← DONE, so |C ∪ {id }| becomes
|C ′ |, (F2) is preserved since pclr (id ) moved to DONE, (F3) and (F4) are unchanged, and F 6 is satisfied by the pcn
update.
By the atom rule, ⟨Q0 ⟩ c1 ⟨Q1 ⟩ is valid: c1 adds id to P (so |C ∪ {id }| = L+R+1 by (F1)) and updates Y S(t) ←
Y S(t) ∪ {id } for all t ∈ A, which relaxes the upper bound in (F3) from Q0 to Q1 , adds |C ∪ {id }| (since P = ∅
before c1 ) to oldn where (F4) is satisfied since old′lr also contains L + R + 1, and sets pcn (id ) ← MID satisfying (F5)
since pclr (id ) = DONE ̸= INIT.
By the seq rule, ⟨Q0 ⟩ c1 ; c2 ⟨Q⟩ is valid.
Finally, P ⊆ Q0 : From (F1) in P , |C| = L+R, and id ∈        / C (else pc n (id) = DONE would give pc lr (id) ̸= INIT by
(F5)), so |C ∪ {id}| = L+R+1. (F2) and (F5) agree between P and Q0 once pc lr (id) is read as DONE (id is neither
MID nor in A on either side). The F3 bound of Q0 is weaker than that of P (its upper bound has the extra element
id). For (F4), old n ⊆ old lr ⊆ old ′lr . The id′ ̸= id part of F6 is inherited from P . Hence P ⊆ Q0 . By the cons rule,
⟨P ⟩ c1 ; c2 ⟨Q⟩ is valid.

Case 2: begin_read(id ).
Implementation step:
Assumes pclr (id ) = INIT; sets vL (id ) ← L and pclr (id ) ← MID.
Corresponding specification steps:
c1 = begin_read(id ), which sets A ← A ∪ {id }, M S(id ) ← C, Y S(id ) ← P , and pcn (id ) ← MID.
Precondition and postcondition:
                 P = (|C| = L + R)
                       ∧ (∀id ′ ∈ I. pclr (id ′ ) = MID ⇐⇒ id ′ ∈ A)
                       ∧ (∀id ′ ∈ A. |M S(id ′ )| ≤ vL (id ′ ) + R ≤ |M S(id ′ ) ∪ Y S(id ′ )|)
                       ∧ (oldn ⊆ oldlr )
                       ∧ (∀id ′ ∈ I. pcn (id ′ ) ̸= INIT =⇒ pclr (id ′ ) ̸= INIT ∧ ilr (id ′ ) = in (id ′ ))
                       ∧ (∀id ′ ∈ I. pclr (id ′ ) = DONE =⇒ pcn (id ′ ) = DONE ∧ olr (id ′ ) = on (id ′ ))
                 Q = (|C| = L + R)
                       ∧ (∀id ′ ∈ I. pc′lr (id ′ ) = MID ⇐⇒ id ′ ∈ A ∪ {id })
                       ∧ (∀id ′ ∈ A ∪ {id }. |M S ′ (id ′ )| ≤ vL
                                                                ′
                                                                  (id ′ ) + R ≤ |M S ′ (id ′ ) ∪ Y S ′ (id ′ )|)
                       ∧ (oldn ⊆ oldlr )
                       ∧ (∀id ′ ∈ I. pc′n (id ′ ) ̸= INIT =⇒ pc′lr (id ′ ) ̸= INIT ∧ i′lr (id ′ ) = in′ (id ′ ))
                       ∧ (∀id ′ ∈ I. pc′lr (id ′ ) = DONE =⇒ pc′n (id ′ ) = DONE ∧ o′lr (id ′ ) = on′ (id ′ ))
where M S ′ (id ) = C, Y S ′ (id ) = P , vL
                                          ′
                                            (id ) = L, and primed variables for id ′ ̸= id are unchanged from the pre-state.
Proof of Lisbon triple ⟨P ⟩ c1 ⟨Q⟩. By the atom rule it suffices to verify each invariant is established.
       • (F1): L and R are unchanged, and C is unchanged, so |C ′ | = |C| = L + R.
       • (F2): pclr (id ) moves from INIT to MID, and id is added to A. For all other id ′ ̸= id , both sides are unchanged.
       • (F3): For the new entry id ∈ A′ : M S(id ) = C and Y S(id ) = P , so we need |C| ≤ vL (id ) + R ≤ |C ∪ P |.
         Since vL (id ) ← L and by (F1), |C| = L + R, we get vL (id ) + R = L + R = |C|, so both bounds hold with
         equality on the left. For existing id ′ ∈ A, M S, Y S, vL , and R are all unchanged, so (F3) is preserved.
       • (F4): Neither old n nor old lr changes, so old n ⊆ old lr is preserved.
       • (F5): pcn (id ) moves to MID ̸= INIT, requiring pclr (id ) ̸= INIT, which holds since pclr (id ) moved to MID.
         Inputs are null for reads so ilr (id ) = in (id ) = null. All other IDs are unaffected.
       • F 6: No ID reaches DONE in this step, so F 6 is vacuously preserved.
Hence ⟨P ⟩ c1 ⟨Q⟩ is valid by the atom rule.

Case 3: return_read(id ).


                                                                17
                             Combining Axiomatic Program Logics with Refinement Proofs                             A P REPRINT



Implementation step:
Assumes pclr (id ) = MID; sets pclr (id ) ← DONE and olr (id ) ← vL (id ) + R.
Corresponding specification steps
c1 = return_read(id ), which removes id from A, nondeterministically chooses S with M S(id ) ⊆ S ⊆ M S(id ) ∪
Y S(id ), sets on (id ) ← |S| and pcn (id ) ← DONE.
Precondition and postcondition:
                 P = (|C| = L + R)
                       ∧ (∀id ′ ∈ I. pclr (id ′ ) = MID ⇐⇒ id ′ ∈ A)
                       ∧ (∀id ′ ∈ A. |M S(id ′ )| ≤ vL (id ′ ) + R ≤ |M S(id ′ ) ∪ Y S(id ′ )|)
                       ∧ (oldn ⊆ oldlr )
                       ∧ (∀id ′ ∈ I. pcn (id ′ ) ̸= INIT =⇒ pclr (id ′ ) ̸= INIT ∧ ilr (id ′ ) = in (id ′ ))
                       ∧ (∀id ′ ∈ I. pclr (id ′ ) = DONE =⇒ pcn (id ′ ) = DONE ∧ olr (id ′ ) = on (id ′ ))
                 Q = (|C| = L + R)
                       ∧ (∀id ′ ∈ I. pc′lr (id ′ ) = MID ⇐⇒ id ′ ∈ A \ {id })
                       ∧ (∀id ′ ∈ A \ {id }. |M S(id ′ )| ≤ vL (id ′ ) + R ≤ |M S(id ′ ) ∪ Y S(id ′ )|)
                       ∧ (oldn ⊆ oldlr )
                       ∧ (∀id ′ ∈ I. pc′n (id ′ ) ̸= INIT =⇒ pc′lr (id ′ ) ̸= INIT ∧ i′lr (id ′ ) = in′ (id ′ ))
                       ∧ (∀id ′ ∈ I. pc′lr (id ′ ) = DONE =⇒ pc′n (id ′ ) = DONE ∧ o′lr (id ′ ) = on′ (id ′ ))
where pc′lr (id ) = DONE, o′lr (id ) = vL (id ) + R, pc′n (id ) = DONE, on′ (id ) = |S|, and all other variables are unchanged
from the pre-state.
Choice of S. We choose S such that |S| = vL (id ) + R to match the concrete return value and satisfy F 6. By (F3) in
the pre-state, |M S(id )| ≤ vL (id ) + R ≤ |M S(id ) ∪ Y S(id )|, so such an S exists.
Proof of Lisbon triple ⟨P ⟩ c1 ⟨Q⟩. By the atom rule we verify each invariant.

       • (F1): L, R, and C are unchanged.
       • (F3): id is removed from A, so the (F3) obligation for id is dropped. For all remaining id ′ ∈ A′ = A \ {id },
         M S, Y S, vL , and R are unchanged, so (F3) is preserved.
       • (F4): Neither old n nor old lr changes, so old n ⊆ old lr is preserved.
       • (F5): pcn (id ) moves to DONE ̸= INIT, requiring pclr (id ) ̸= INIT, which holds since pclr (id ) = MID in the
         pre-state. All other IDs are unaffected.
       • F 6: pclr (id ) moves to DONE, requiring pcn (id ) = DONE and olr (id ) = on (id ). The specification step sets
         pcn (id ) ← DONE and on (id ) ← |S| = vL (id ) + R = olr (id ), so both conditions hold by our choice of S.
         All other IDs are unaffected.

Hence ⟨P ⟩ c1 ⟨Q⟩ is valid by the atom rule.

Since the Lisbon triple ⟨R(σ, τ )⟩ c1 ; . . . ; cn ⟨R(σ ′ , τ ′ )⟩ is valid for every implementation operation, R is a valid
forward simulation by Theorem 10.




                                                                18
                            Combining Axiomatic Program Logics with Refinement Proofs                         A P REPRINT



A.2   Backward Simulation Verification

By Theorem 13, with NDC as S1 and Seq as S2 , it suffices to show that for every implementation step (σ, σ ′ ) of NDC
the Incorrectness triple [R1 (σ)] c [R1 (σ ′ )] is valid for the corresponding sequential program c. The NDC state is a
parameter (at σ in the precondition P , at σ ′ in the postcondition Q); the sequential state is the program state. We write
c = |C|, p = |P | for the pre-state NDC counts and reason over reachable states, using:
Lemma 4 (Structural invariants). At every reachable related state:
(i) old s = {0, . . . , x}, old n = {0, . . . , |C| + |P |};
(ii) x = |C| + |{a ∈ P : pc s (a) = DONE}|;
(iii) if pc s (id) = DONE then os (id) is the value of x at the step where id linearized.


Case 1:     return_increment(a).
Implementation step:
Assumes pc n (a) = MID, a ∈ P ; moves a from P to C; sets pc n (a) ← DONE.
Corresponding specification step:
c = skip.



                     P = (|C| ≤ x ≤ |C| + |P |)
                         ∧ (old s ⊆ old n )
                         ∧ (∀id. pc s (id) ̸= INIT =⇒ pc n (id) ̸= INIT ∧ in (id) = is (id))
                         ∧ (∀id. pc n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id))
                     Q = (|C|+1 ≤ x ≤ |C| + |P |)
                         ∧ (old s ⊆ old n )
                            ∧ (∀id. pc s (id) ̸= INIT =⇒ pc ′n (id) ̸= INIT ∧ in (id) = is (id))
                            ∧ (∀id. pc ′n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id)),


where pc ′n (a) = DONE and |C ′ | = |C|+1, |P ′ | = |P |−1 (so Q’s (B1) reads |C|+1 ≤ x ≤ |C| + |P |).
Since [P ] skip [P ] is a valid Incorrectness triple due to the unit rule, by the consequence rule it suffices to show that
Q =⇒ P . Let’s inspect this clause by clause:

       • (B1): |C|+1 ≤ x ≤ |C|+|P | =⇒ |C| ≤ x ≤ |C|+|P |.

       • (B2): old n is unchanged, identical.

       • (B3): pc ′n (a) = DONE ̸= INIT and pc n (a) = MID ̸= INIT, so Q’s clause implies P ’s as they are both
         vacuously true; other ids are unchanged.

       • (B4): pc n (a) = MID makes P ’s clause vacuous for a, while Q constrains it, so Q’s clause implies P ’s clause;
         other ids are unchanged.

Hence Q =⇒ P and [P ] skip [Q] is a valid Incorrectness triple.


Case 2:     return_read(a).
Implementation step:
Assumes pc n (a) = MID, a ∈ A; removes a from A; chooses S with MS (a) ⊆ S ⊆ MS (a) ∪YS (a); sets on (a) ← |S|,
pc n (a) ← DONE. Corresponding specification step:
c = skip.


                                                             19
                            Combining Axiomatic Program Logics with Refinement Proofs                           A P REPRINT




                      P = (|C| ≤ x ≤ |C| + |P |)
                          ∧ (old s ⊆ old n )
                          ∧ (∀id. pc s (id) ̸= INIT =⇒ pc n (id) ̸= INIT ∧ in (id′ ) = is (id′ ))
                          ∧ (∀id. pc n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id))
                      Q = (|C| ≤ x ≤ |C| + |P |)
                          ∧ (old s ⊆ old n )
                            ∧ (∀id. pc s (id) ̸= INIT =⇒ pc ′n (id) ̸= INIT ∧ in (id) = is (id))
                           ∧ (∀id. pc ′n (id) = DONE =⇒ pc s (id) = DONE ∧ o′n (id) = os (id))
where pc ′n (a) = DONE, o′n (a) = |S|, and |C|, |P | are unchanged.
Since [P ] skip [P ] is a valid Incorrectness triple due to the unit rule, by the consequence rule it suffices to show that
Q =⇒ P . Let’s inspect this clause by clause:
       • (B1), (B2): |C|, |P |, old n unchanged.
       • (B3): pc ′n (a) = DONE ̸= INIT and pc n (a) = MID ̸= INIT, so Q’s clause implies P ’s as they are both
         vacuously true; other ids are unchanged.
       • (B4): pc n (id) = MID makes P ’s clause vacuous for a, while Q constrains it, so Q’s clause implies P ’s clause;
         other ids are unchanged.
Hence Q =⇒ P and [P ] skip [Q] is a valid Incorrectness triple.

Case 3:   begin_read(a).
Implementation steps:
Assumes pc n (a) = INIT; adds a to A; sets MS (a) ← C, YS (a) ← P , pc n (a) ← MID.
Corresponding specification steps:
c = read(a) ⊔ skip.


                     P = (|C| ≤ x ≤ |C| + |P |)
                         ∧ (old s ⊆ old n )
                         ∧ (∀id. pc s (id) ̸= INIT =⇒ pc n (id) ̸= INIT ∧ in (id) = is (id))
                         ∧ (∀id. pc n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id)),
                     Q = (|C| ≤ x′ ≤ |C| + |P |)
                           ∧ (old ′s ⊆ old n )
                           ∧ (∀id. pc ′s (id) ̸= INIT ⇒ pc ′n (id) ̸= INIT ∧ in (id) = is (id))
                          ∧ (∀id. pc ′n (id) = DONE ⇒ pc ′s (id) = DONE ∧ on (id) = o′s (id)),
where pc ′n (a) = MID and |C|, |P | are unchanged. Split Q = Qs ∨ Qr on pc ′s (a), with Qs = Q ∧ pc ′s (a) = INIT and
Qr = Q ∧ pc ′s (a) = DONE.
Since [P ] skip [P ] is a valid Incorrectness triple due to the unit rule, by the consequence rule it suffices to show that
Qs =⇒ P for the skip choice: with pc ′s (a) = pc s (a) = INIT, P ’s (B3) is vacuous for a, and pc n (a) = INIT makes
P ’s (B4) vacuous for a; |C|, |P |, x, olds are unchanged, so the remaining clauses are identical. Hence, Qs =⇒ P and
[P ] skip [Qs ] is a valid Incorrectness triple.
read(a) assumes pc s (a) = INIT and sets os (a) ← x, pc ′s (a) ← DONE, so
                            Q′ = {τ ′ | pc ′s (a) = DONE, o′s (a) = x′ , τ ′ [pc s (a)←INIT] ∈ P }.
where [P ] read(a) [Q ] is a valid Incorrectness triple due to the assume and assigment rules. For τ ′ ∈ Qr , a began
                        ′

at this step, so by Lemma 4(iii) it linearized here and o′s (a) = x′ ; and the pre-image τ ′ [pc s (a)←INIT, os (a) unset]
satisfies P (x, olds unchanged; (B3) vacuous for a; (B4) vacuous for a at σ). Hence Qr =⇒ Q′ , and by consequence
[P ] read(a) [Qr ] is a valid Incorrectness triple.
As a result of the choice rule, [P ] read(id) ⊔ skip [Qr ∨ Qs ] = [P ] c [Q] is a valid Incorrectness triple.


                                                            20
                             Combining Axiomatic Program Logics with Refinement Proofs                             A P REPRINT



Case 4:    begin_increment(a).
Implementation step:
Assumes pc n (a) = INIT, a ∈/ P ∪ C; adds a to P ; inserts |C| + |P | = c + p + 1 into old n ; adds a to YS (t) for all
t ∈ A; sets pc n (a) ← MID.
Corresponding specification steps:
c = (increment(a) ⊔ skip); flush, where flush = (read(t) ⊔ skip);t∈A .


                      P = (c ≤ x ≤ c + p)
                          ∧ (old s ⊆ old n )
                          ∧ (∀id. pc s (id) ̸= INIT =⇒ pc n (id) ̸= INIT ∧ in (id) = is (id))
                          ∧ (∀id. pc n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id)),
                      Q = (c ≤ x′ ≤ c + p + 1)
                            ∧ (old ′s ⊆ old ′n )
                            ∧ (∀id. pc ′s (id) ̸= INIT =⇒ pc ′n (id) ̸= INIT ∧ in (id) = i′s (id))
                            ∧ (∀id. pc ′n (id) = DONE =⇒ pc ′s (id) = DONE ∧ on (id) = o′s (id)),
where pc ′n (a) = MID, |C ′ | = c, |P ′ | = p + 1, and old ′n = old n ∪ {c + p + 1}. Split Q = Qs ∨ Qi on pc ′s (a).
Skip branch (Qs = Q ∧ pc ′s (a) = INIT). Here skip; flush reduces to skip: with x unchanged, no read reaches a new
target, so every flush choice is skip. We show Qs ⊆ P . By Lemma 4(ii) at σ ′ , a unlinearized gives x′ = c + |{b ∈
P : pc ′s (b) = DONE}| ≤ c + p, so (B1) of P holds; (B2) follows from old ′s = {0, . . . , x′ } ⊆ {0, . . . , c + p} = old n ;
B3, B4 for a are vacuous at σ; the rest are inherited. By the consequence rule, [P ] skip [Qs ] is a valid Incorrectness
triple.
Increment branch (Qi = Q ∧ pc ′s (a) = DONE). We derive [P ] increment(a); flush [Qi ] by the seq rule through the
intermediate


                     M = (c+1 ≤ x ≤ c + p + 1)
                            ∧ (old s ⊆ old ′n )
                            ∧ (pc s (a) = DONE)
                            ∧ (∀id. pc s (id) ̸= INIT =⇒ pc ′n (id) ̸= INIT ∧ in (id) = is (id))
                            ∧ (∀id. pc ′n (id) = DONE =⇒ pc s (id) = DONE ∧ on (id) = os (id)),
i.e. R1 (σ ′ ) after a has linearized but before the reads, read with σ ′ parameters (so (B3) for a holds, as pc ′n (a) = MID ̸=
INIT).

[P ] increment(a) [M ]: increment(a) sends x to x+1 and old s to old s ∪ {x+1} and pc s (a) to DONE. For τM ∈ M ,
its pre-image has x=xM −1 ∈ [c, c + p] (so (B1) of P holds) and pc s (a) = INIT ((B3), (B4) vacuous for a at σ); thus
the triple is a valid Incorrectness triple.
[M ] flush [Qi ]: flush is the sequence (read(t) ⊔ skip);t∈A . Applying the seq and choice rules once per t ∈ A
exactly as in the read branch of Case 3 – taking the read(t) alternative for the active reads with o′s (t) = x′ (these
linearize at the new count x′ , by Lemma 4(iii), since M has x = x′ ) and skip for the rest – yields [M ] flush [Qi ].
The sequencing rule then gives [P ] increment(a); flush [Qi ] as a valid Incorrectness triple.
Distributing the leading choice, c = (increment(a); flush) ⊔ (skip; flush), the choice rule combines the two
branches into [P ] c [Qi ∨ Qs ] = [P ] c [Q][P ], which is a valid Incorrectness triple.

Since the corresponding Incorrectness triple is valid for every implementation operation, R is a backward simulation by
Theorem 13.




                                                              21
