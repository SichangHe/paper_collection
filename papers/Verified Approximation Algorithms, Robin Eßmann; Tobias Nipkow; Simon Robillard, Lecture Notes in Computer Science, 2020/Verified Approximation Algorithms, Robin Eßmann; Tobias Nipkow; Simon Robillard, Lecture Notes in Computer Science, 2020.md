Logical Methods in Computer Science
Volume 18, Issue 1, 2022, pp. 36:1–36:21                                                 Submitted   Apr. 29, 2021
https://lmcs.episciences.org/                                                            Published   Mar. 01, 2022




                      VERIFIED APPROXIMATION ALGORITHMS

    ROBIN ESSMANN a , TOBIAS NIPKOW a , SIMON ROBILLARD b , AND UJKAN SULEJMANI a

   a
       Technische Universität München, Germany

   b
       LIRMM, Université de Montpellier & CNRS, Montpellier, France



          Abstract. We present the first formal verification of approximation algorithms for NP-
          complete optimization problems: vertex cover, independent set, set cover, center selection,
          load balancing, and bin packing. We uncover incompletenesses in existing proofs and
          improve the approximation ratio in one case. All proofs are uniformly invariant based.




                                                  1. Introduction
Approximation algorithms for NP-complete problems [Vaz03] are a rich area of research
untouched by automated verification. We present the first formal verifications of five classical
and one lesser known approximation algorithm. Three of these algorithms had been verified
on paper by program verification experts [BM03, BR03]. We found that their claimed
invariants need additional conjuncts before they are strong enough to be real invariants.
That is, their proofs are incomplete. The other three algorithms only come with informal
textbook proofs [KT06].
    To put an end to this situation we formalized the correctness proofs of six approximation
algorithms for fundamental NP-complete problems in the theorem prover Isabelle/HOL
[NK14, NPW02]. We verified (all proofs are online [ENRS20]) the following algorithms and
approximation ratios:
• the classic k-approximation algorithm for minimal vertex covers of rank k hypergraphs;
• Wei’s [Wei81] ∆-approximation algorithm for maximal independent sets of graphs with
  maximum degree ∆;
• the greedy 32 (resp. 2) approximation algorithm for the load balancing problem of sorted
  (resp. unsorted) job loads;
• the greedy 2-approximation algorithm for the center selection problem;
• the greedy H(d∗ )-approximation algorithm for set covers where d∗ is the size of the largest
  set and H(n) is the nth harmonic number;
• the 32 -approximation algorithm for bin packing by Berghammer and Reuter [BR03].

  This is a revised version of the conference publication [ENR20]; the sections on Center Selection and Set
Cover have been added.



l      LOGICAL METHODS
       IN COMPUTER SCIENCE                 DOI:10.46298/LMCS-18(1:36)2022
                                                                            ©
                                                                             CC
                                                                                  VERIFIED APPROXIMATION ALGORITHMS
                                                                                   Creative Commons
36:2                    VERIFIED APPROXIMATION ALGORITHMS                                Vol. 18:1




All algorithms are expressed in a simple imperative WHILE -language. In each case we
show that the approximation algorithm computes a valid solution that is at most a certain
factor worse than an optimum solution. The polynomial running time of the approximation
algorithm is easy to see in each case.
    Isabelle not only helped finding mistakes in pen-and-paper proofs but also encouraged
proof refactoring that led to simpler proofs, and in one case, to a stronger result: The
invariant given by Berghammer and Müller for Wei’s algorithm [BM03] is sufficient to show
that the algorithm has an approximation ratio of ∆ + 1. We managed to simplify their
argument significantly which led to an improved approximation ratio of ∆.
    Last but not least all our proofs are uniformly invariant-based. This is in contrast to
the three textbook proofs from [KT06] that rely on special ad hoc arguments about the
programs at hand. We show that this is completely unnecessary and that invariant based
proofs can even be simpler.


                     2. Isabelle/HOL and Imperative Programs
Isabelle/HOL is largely based on standard mathematical notation but with some differences
and extensions.
     Type variables are denoted by 0a, 0b, etc. The notation t :: τ means that term t has type
τ . Except for function types 0a ⇒ 0b, type constructors follow postfix syntax, e.g., 0a set is
the type of sets of elements of type 0a. The image of a function f over a set S is denoted
by f ‘ S. Function some :: 0a set ⇒ 0a picks an arbitrary element from a set; the result is
unspecified if the set is empty.
     The types nat and real represent the sets N and R. In this paper we drop the coercion
function real :: nat ⇒ real. The set {m..n} is the closed interval [m, n].
     The Isabelle/HOL distribution comes with a simple implementation of Hoare logic where
programs are annotated with pre- and post-conditions and invariants as in this example,
where all variables are of type nat:

 {m = 0 ∧ p = 0}
 WHILE m 6= a INV {p = m∗b}              DO p := p+b; m := m+1 OD
 {p = a∗b}

The box around the program means that it has been verified. All our proofs employ a
verification condition generator and essentially reduce to showing the preservation of the
invariants.
     Behind the scenes, a Hoare triple is just a HOL formula based on a formalized program
semantics. {P } c {Q} is syntactic sugar for the following partial correctness formula: if
execution of c starting in a state that satisfies P terminates, then the final state satisfies Q.
All expressions in a Hoare triple (pre- and post-conditions, invariants, tests in loops and
conditionals, and right-hand sides of assignments) are arbitrary HOL expressions and can
talk about both program variables and elements from the context.


                                     3. Vertex Cover
We verify the proof in [BM03] that the classic greedy algorithm for vertex cover is a 2-
approximation algorithm. In fact, we generalize the setup from graphs to hypergraphs. A
Vol. 18:1                    VERIFIED APPROXIMATION ALGORITHMS                            36:3




hypergraph is simply a set of edges E, where an edge is a set of vertices of type 0a. A vertex
cover for E is a set of vertices C that intersects with every edge of E :
vc :: 0a set set ⇒ 0a set ⇒ bool
vc E C = (∀ e∈E . e ∩ C 6= ∅)
     A matching (matching :: 0a set set ⇒ bool ) is a set of pairwise disjoint sets. The
following is a key property that relates vc and matching:
finite C ∧ matching M ∧ M ⊆ E ∧ vc E C −→ |M | ≤ |C |
     We fix a rank-k hypergraph E :: 0a set set with the assumptions ∅ ∈    / E, finite E and
e ∈ E −→ finite e ∧ |e| ≤ k . (Via an Isabelle “locale”. We use the same mechanism in all
of our proofs.)
     We have verified the well known greedy algorithm that computes a vertex cover C for
E. It keeps picking an arbitrary edge that is not covered by C yet until all vertices are
covered. The final C has at most k times as many vertices as any vertex cover of E (which
is essentially optimal [BK10]).

  {True}
  C :=∅; F := E ;
  WHILE F 6= ∅ INV {invar C F }
  DO C := C ∪ some F ; F := F − {e 0 ∈ F | some F ∩ e 0 6= ∅} OD
  {vc E C ∧ (∀ C 0. finite C 0 ∧ vc E C 0 −→ |C | ≤ k ∗ |C 0|)}

where invar is the following invariant:
invar :: 0a set ⇒ 0a set set ⇒ bool
invar C F =
   (F ⊆ E ∧ vc (E − F ) C ∧ finite C ∧ (∃ M . inv matching C F M ))
inv matching C F M =
   (matching M ∧ M ⊆ E ∧ |C | ≤ k ∗ |M | ∧ (∀ e∈M . ∀ f ∈F . e ∩ f = ∅))
The key step in the program proof is that the invariant is invariant:
Lemma 3.1. F 6= ∅ ∧ invar C F −→
   invar (C ∪ some F ) (F − {e 0 ∈ F | some F ∩ e 0 6= ∅})
     Our invariant is stronger than the one in [BM03] which lacks F ⊆ E. Indeed, without
this property, the claimed invariant is not invariant (as acknowledged by Müller-Olm).


                                   4. Independent Set
As in the previous section, a graph is a set of edges. An independent set of a graph E is a
subset of its vertices such that no two vertices are adjacent.
iv :: 0a set set ⇒  0
                 S a set ⇒ bool
iv E S = (S ⊆         E ∧ (∀ v 1 v 2 . v 1 ∈ S ∧ v 2 ∈ S −→ {v 1 , v 2 } ∈
                                                                         / E ))
     We fix a finite S              0
                      graph E :: a set set such that all edges of E are sets of cardinality 2.
The set of vertices      E is denoted V, and the maximum degree (number of neighbors) of
any vertex in V is denoted ∆. We show that the greedy algorithm proposed by Wei is a
∆-approximation algorithm. The proof is inspired by one given in [BM03]. In particular,
the proof relies on an auxiliary variable P, which is not needed for the execution of the
36:4                    VERIFIED APPROXIMATION ALGORITHMS                               Vol. 18:1




algorithm, but is used for bookkeeping in the proof. In [BM03], P is initially a program
variable and is later removed from the program and turned into an existentially quantified
variable in the invariant. We directly use the latter representation.

 { True }
 S := ∅; X :=∅;
 WHILE X 6= V INV { ∃ P . inv partition S X P }
 DO x := some (V − X ); S := S ∪ {x }; X := X ∪ neighbors x ∪ {x } OD
 { iv E S ∧ (∀ S 0. iv E S 0 −→ |S 0| ≤ |S | ∗ ∆) }

      To keep the size of definitions manageable, we split the invariant in two. The first part
is not concerned with P, but suffices to prove the functional correctness of the algorithm,
i.e., that it outputs an independent set of the graph:
inv iv :: 0a set ⇒ 0a set ⇒ bool
inv iv S X =
   (iv E S ∧ X ⊆ V ∧ (∀ v 1 ∈V − X . ∀ v 2 ∈S . {v 1 , v 2 } ∈
                                                             / E) ∧ S ⊆ X )
This invariant is taken almost verbatim from [BM03], except that in [BM03] it says that
S is an independent set of the subgraph generated by X. This is later used to show that
the x picked at each iteration from V − X is not already in S. Defining subgraphs adds
unnecessary complexity to the invariant. We simply state S ⊆ X, together with the fact
that S is an independent set of the whole graph.
      We now extend the invariant with properties of the auxiliary variable P.
inv partition :: 0a set ⇒ 0a set ⇒ 0a set set ⇒ bool
inv partition S X P =
     S iv S X ∧
   (inv
        P = X ∧ (∀ p∈P . ∃ s∈V . p = {s} ∪ neighbors s) ∧ |P | = |S | ∧ finite P )
We can view the set P as an auxiliary program variable. In order to satisfy the invariant,
P would be initially empty and the loop body would include the assignment P := P ∪
{neighbors x ∪ {x }}. Intuitively, P contains the sets of vertices that are added to X at
each iteration (or more precisely, an over-approximation, since some vertices in neighbors
x may have been added to X in a previous iteration). Instead of adding an unnecessary
variable to the program, we only use the existentially quantified invariant. The assignments
described above correspond directly to instantiations of the quantifier that are needed to
solve proof obligations. This is illustrated with the following lemma, which corresponds to
the preservation of the invariant:
Lemma 4.1. (∃ P . inv partition S X P ) ∧ x ∈ V − X −→
   (∃ P 0. inv partition (S ∪ {x }) (X ∪ neighbors x ∪ {x }) P 0)
The existential quantifier in the antecedent yields a witness P. After instantiating the quanti-
fier in the succedent with P ∪ {neighbors x ∪ {x }}, the goal can be solved straightforwardly.
Finally, the following lemma combines the invariant and the negated post-condition to prove
the approximation ratio:
Lemma 4.2. inv partition S V P −→ (∀ S 0. iv E S 0 −→ |S 0| ≤ |S | ∗ ∆)
To prove it, we observe that any set p ∈ P consists of a vertex x and its neighbors, therefore
an independent set S 0 can contain at most ∆ of the vertices in p, thus |S 0| ≤ |P | ∗ ∆.
Furthermore, as indicated by the invariant, |P | = |S |.
Vol. 18:1                    VERIFIED APPROXIMATION ALGORITHMS                              36:5




      Compared to the proof in [BM03], our invariant describes the contents of the set P more
precisely, and thus yields
                       S     a better approximation ratio. In [BM03], the invariant merely
indicates that X =         P, together with two cardinality properties: ∀ p∈P . |p| ≤ ∆ + 1
and |P | ≤ |S |. Taken with the negated post-condition, this invariant can be used to show
that for any independent set S 0, we have |S 0| ≤ |S | ∗ (∆ +S1). The   S proof of this lemma
makes use of the following (in)equalities: |S 0| ≤ |V |, |V | = | P |, | P | ≤ |P | ∗ (∆ + 1)
and finally |P | ∗ (∆ + 1) ≤ |S | ∗ (∆ + 1). Note that this only relies on the trivial fact
that an independent set cannot contain more vertices than the graph. By contrast, our own
argument takes into account information regarding the edges of the graph.
      Although this proof results in a weaker approximation ratio than our own, it yields a
useful insight: an approximation ratio is given by the cardinality of the largest set p ∈ P
(i.e., the largest number of vertices added to X during any given iteration). In the worst case,
this is equal to ∆ + 1, but in practice the number may be smaller. This suggests a variant
of the algorithm that stores that value in a variable r, as described in [BM03]. At every
iteration, the variable r is assigned the value max r |{x } ∪ neighbors x − X |. Ultimately,
the algorithm returns both the independent set S and the value r, with the guarantee that
|S 0| ≤ |S | ∗ r for any independent set S 0.
      We also formalized this variant and proved the aforementioned property. The proof
follows the idea outlined above, but does away with the variable P entirely: instead, the
invariant simply maintains that inv iv S X ∧ |X | ≤ |S | ∗ r, and the proof of preservation
is adapted accordingly. Indeed, this demonstrates that the argument used in [BM03] does
not require an auxiliary variable nor an existentially quantified invariant. For the proof
of the approximation ratio ∆, a similar simplification is not as easy to obtain, because
the argument relies on a global property of the graph (a constraint that edges impose on
independent sets) that is not easy to summarize in an inductive invariant.
      So far, we have only considered an algorithm where the vertex x is picked non-
deterministically. An obvious heuristic is to pick, at every iteration, the vertex with
the smallest number of neighbors among V − X. Halldórsson and Radhakrishnan [HR97]
prove that this heuristic achieves an approximation ratio of (∆ + 2) / 3. They proceed
by considering the sequence of graph reductions corresponding to the execution of the
algorithm. Formalizing this argument would require an inductive invariant to keep track of
the sequences of values of X and x at each iteration and the relations between those values,
providing a much more precise record than the auxiliary variable P. In addition, the proof
itself is far more complex than the arguments presented here, relying on case analysis for
different types of graphs. This is beyond the scope of our paper.




                                    5. Load Balancing
Our starting point for the load balancing problem is [KT06, Chapter 11.1]. We need to
distribute n :: nat jobs on m :: nat machines with 0 < m. A job j ∈ {1..n} has a load
t(j ) :: nat. Variables m, n, and t are fixed throughout this section. A solution is described
by a function A that maps machines to sets of jobs: k ∈ {1..m} has job j assigned to it iff
j ∈ A(k ). The sumP of job loads on a machine is given by a function T that is derived from t
and A: T k = ( j ∈A k . t j ). Predicate lb defines when T and A are a partial solution for
j ≤ n jobs:
36:6                     VERIFIED APPROXIMATION ALGORITHMS                            Vol. 18:1




lb :: (nat ⇒ nat) ⇒ (nat ⇒ nat set) ⇒ nat ⇒ bool
lb T A j =
   ((∀Sx ∈{1..m}. ∀ y∈{1..m}. x 6= y −→ A x ∩P   A y = ∅) ∧
    ( x ∈{1..m} A x ) = {1..j } ∧ (∀ x ∈{1..m}. ( y∈A x . t y) = T x ))
It consists of three conjuncts. The first ensures that the sets returned by A are pairwise
disjoint, thus, no job appears in more than one machine. The second conjunct ensures that
every job x ∈ {1..j } is contained in at least one machine. It also ensures that only jobs
{1..j } have been added. The final conjunct ensures that T is correctly defined to be the
total load on a machine. To ensure that jobs are distributed evenly, we need to consider the
machine with maximum load. This load is referred to as the makespan of a solution:
makespan :: (nat ⇒ nat) ⇒ nat
makespan T = Max (T ‘ {1..m})
    The greedy approximation algorithm outlined in [KT06] relies on the ability to determine
the machine k ∈ {1..m} that has a minimum combined load. As the goal is to approximate
the optimum in polynomial time, a linear scan through T suffices to find the machine
with minimum load. However, other methods may be considered to further improve time
complexity. To determine the machine with minimum load, we will use the following function:
min arg :: (nat ⇒ nat) ⇒ nat ⇒ nat
min arg T 0 = 1
min arg T (x + 1) =
  (let k = min arg T x in if T (x + 1) < T k then x + 1 else k )
    We will focus on the approximation factor of 32 , which can be proved if the job loads are
assumed to be sorted in descending order. The proof for the approximation factor of 2 if
jobs are unsorted is very similar and we describe the differences at the end. We say that j
jobs are sorted in descending order if sorted holds:
sorted :: nat ⇒ bool
sorted j = (∀ x ∈{1..j }. ∀ y∈{1..x }. t x ≤ t y)
    Below we prove the following conditional Hoare triple that expresses the approximation
factor and functional correctness of the algorithm given in [KT06]:

 sorted n −→
 {True}
 T := (λ . 0); A := (λ . ∅); j := 0;
 WHILE j < n INV {inv 2 T A j }
 DO i := min arg T m; j := j + 1;
     A := A(i := A(i ) ∪ {j }); T := T (i := T (i ) + t(j ))
 OD
 {lb T A n ∧
  (∀ T 0 A 0. lb T 0 A 0 n −→ makespan T ≤ 3 / 2 ∗ makespan T 0)}

Property sorted n does not need to be part of the precondition because it does not mention
any program variable. Therefore we can make sorted n an assumption of the whole Hoare
triple, which simplifies the proof. The notation f (a := b) denotes an updated version of
function f that maps a to b and behaves like f otherwise. Thus an assignment f := f (i :=
b) is nothing but the conventional imperative array update notation f [i ] := b.
Vol. 18:1                    VERIFIED APPROXIMATION ALGORITHMS                             36:7




    Functional correctness follows because each iteration extends a partial solution for j
jobs to one for j + 1 jobs:
Lemma 5.1. lb T A j ∧ x ∈ {1..m} −→
   lb (T (x := T x + t (j + 1))) (A(x := A x ∪ {j + 1})) (j + 1)
Moreover, it is easy to see that the initialization establishes lb T A j.
    To prove the approximation factor in both the sorted and unsorted case, the following
lower bound is important:
Lemma 5.2. lb T A j −→ ( jx = 1 t x ) / m ≤ makespan T
                                P
                                  Pj
This is a result of P m
                    P
                      x=1 T (x) =  x=1 t(x) together with this general property of sums: finite
A ∧ A 6= ∅ −→ ( a∈A. f a) ≤ |A| ∗ Max (f ‘ A).
    A similar observation applies to individual jobs. Any job must be a lower bound on
some machine, as it is assigned to one and, by extension, it must also be a lower bound of
the makespan:
Lemma 5.3. lb T A j −→ Max 0 (t ‘ {1..j }) ≤ makespan T
As any job load is a lower bound on the makespan over the machines, the job with maximum
load must also be a lower bound. Note that Max 0 returns 0 for the empty set.
     When jobs are sorted in descending order, a stricter lower bound for an individual job
can be established. We observe that an added job is at most as large as the jobs preceding
it. Therefore, if a machine contains at least two jobs, this added job is only at most half as
large as the makespan. We can use this observation by assuming the machines to be filled
with more than m jobs, as this will ensure that some machine must contain at least two jobs.
Lemma 5.4. lb T A j ∧ m < j ∧ sorted j −→ 2 ∗ t j ≤ makespan T
Note that this lower bound only holds if there are strictly more jobs than machines. One must,
however, also consider how the algorithm behaves in the other case. One may intuitively see
that the algorithm will be able to distribute the jobs such that every machine will only have
at most one job assigned to it, making the algorithm trivially optimal. To prove this, we
need to show the following behavior of min arg:
Lemma 5.5.
(1) x ∈ {1..m} ∧ T x = 0 −→ T (min arg T m) = 0
(2) x ∈ {1..m} ∧ T x = 0 −→ min arg T m ≤ x
Both properties can be shown by induction on the number of machines m.
     As the proof in [KT06] is only informal, Kleinberg and Tardos do not provide any loop
invariant. We propose the following invariant for sorted jobs:
inv 2 :: (nat ⇒ nat) ⇒ (nat ⇒ nat set) ⇒ nat ⇒ bool
inv 2 T A j =
(lb T A j ∧ j ≤ n ∧
 (∀ T 0 A 0. lb T 0 A 0 j −→ makespan T ≤ 3 / 2 ∗ makespan T 0) ∧
 (∀ x > j . T x = 0) ∧ (j ≤ m −→ makespan T = Max 0 (t ‘ {1..j })))
The final two conjuncts relate to the trivially optimal behavior of the algorithm if j ≤ m.
The penultimate conjunct shows that only as many machines can be occupied as there are
available jobs. The final conjunct ensures that every job is distributed on its own machine,
making the makespan equivalent to the job with maximum load.
36:8                    VERIFIED APPROXIMATION ALGORITHMS                             Vol. 18:1




    It should be noted that if the makespan is sufficiently large, an added job may not
increase the makespan at all, as the machine with minimum load combined with the job
may not exceed the previous makespan. As such, we will also consider the possibility that
an added job can simply be ignored without affecting the overall makespan.
Lemma 5.6. makespan (T (x := T x + y)) 6= T x + y −→
makespan (T (x := T x + y)) = makespan T
     To make use of this observation, we need to be able to relate the makespan of a solution
with the added job to the makespan of a solution without it. One can easily show the
following by removing j + 1 from the solution:
Lemma 5.7. lb T A (j + 1) −→
   (∃ T 0 A 0. lb T 0 A 0 j ∧ makespan T 0 ≤ makespan T )
    We can now prove the preservation of inv 2 . Let i = min arg T m be the machine with
minimum load. We define:
        T g := T (i := T (i ) + t(j + 1))      Ag := A (i := A(i ) ∪ {j + 1})
We begin with a case distinction. If j + 1 ≤ m, we can make use of the additional conjuncts
to prove the trivially optimal behavior. We first note in-range: j + 1 ∈ {1..m}. Moreover,
from the penultimate conjunct, T (j + 1) = 0. Combining this with Lemma 5.5.1, we can
see that T (i ) = 0. Therefore T g (i ) = t(j + 1) and with the final conjunct of the assumed
invariant, the makespan of T g remains equivalent to the job with maximum load. To
prove that the penultimate conjunct is preserved, we again use in-range, T (j + 1) = 0, and
Lemma 5.5.2 to prove that i ≤ j + 1. Moreover, T g only differs from T by the modification
of machine i. Thus, the penultimate conjunct for j + 1 jobs is preserved as well. From
Lemma 5.3 we can then see that, as the makespan of T g is equivalent to the job with
maximum load, it must be trivially optimal. Functional correctness can be shown using
Lemma 5.1, and proving the preservation of the remaining conjunct is trivial. We now come
to the case j + 1 > m. We first show that the penultimate conjunct is preserved (the final
conjunct can be ignored, as ¬ j + 1 ≤ m). This follows from the correctness of min arg, as
the index returned by it has to be in {1..m} as long as m > 0. Therefore, we can simply
show this from the penultimate conjunct of the assumed invariant. We now come to the
proof of the approximation factor:
∀ T 0 A 0. lb T 0 A 0 (j + 1) −→ makespan T g ≤ 3 / 2 ∗ makespan T 0
To prove it, we fix T 1 and A1 such that lb T 1 A1 (j + 1). Using Lemma 5.7, one can now
obtain T 0 and A0 such that lb T 0 A0 j and MK : makespan T 0 ≤ makespan T 1 . From the
assumed loop invariant, we can now show:
                                              3
                               makespan T ≤ makespan T 0                        by inv 2 -def
                                              2
                                              3
                                           ≤ makespan T 1                           by MK
                                              2
To prove the makespan for j + 1 jobs, there are now two cases to consider: The added job j
+ 1 contributes to the makespan or it does not. The case in which it does not can be shown
by combining the previous calculation with Lemma 5.6. For the first case, we may then
assume that makespan T g = T (i ) + t(j + 1). Like in Lemma 5.2, we note that sum-eq:
                  Pj
( m
 P                                                                             Pm
   x = 1 T x ) = ( x = 1 t x ). Moreover, min-avg: m ∗ T (min arg T m) ≤ ( i = 1 T i ).
Vol. 18:1                      VERIFIED APPROXIMATION ALGORITHMS                              36:9




This allows us to calculate the following lower bound for T (i ):
                             m
                             X             j
                                           X
              m ∗ T (i ) ≤       T (i) =         t(i)                   by min-avg and sum-eq
                             i=1           i=1
                             Pj
                                i=1 t(i)
             ⇐⇒ T (i) ≤                                                          because m > 0
                             m
                        ≤ makespan T 0 ≤ makespan T 1                   by Lemma 5.2 and MK
From Lemma 5.4 we can also show that t(j + 1) is a lower bound for 12 of the makespan of
T 1 . Therefore:
                                                                     makespan T 1
             makespan T g = T (i ) + t(j + 1) ≤ makespan T 1 +
                                                                          2
                                                   3
                                                 = makespan T 1
                                                   2
The proof of functional correctness and remaining conjuncts is again trivial.
     Let us now consider the unsorted case where one can still show an approximation factor
of 2. The algorithm is identical but the invariant is simpler:
inv 1 T A j =
   (lb T A j ∧ j ≤ n ∧ (∀ T 0 A 0. lb T 0 A 0 j −→ makespan T ≤ 2 ∗ makespan T 0))
The proof for this invariant is a simpler version of the proof above: We do not need the
initial case distinction (case j + 1 ≤ m need not be considered separately), and we use
Lemma 5.3 instead of Lemma 5.4 to obtain a bound for t(j + 1).



                                      6. Center Selection
This section is based on [KT06, Chapter 11.2]. Given a finite, non-empty set of sites
S :: 0a set (i.e., points) in a metric space, our objective is to select an optimal set of centers
C ⊆ S of size k > 0, such that
radius C = Max (distance C ‘ S )
is minimized, where distance C s = Min (dist s ‘ C ).
      We call a site s a candidate (with respect to some r ) if distance C s > 2r and call it
included if distance C s ≤ 2r (i.e., if it already lies within 2r of some center). Now consider
the following two observations for the optimal radius r∗ :
(1) Selecting as a center a candidate site s w.r.t. r∗ guarantees that at least one more site
     will now lie within 2r∗ of a center—namely s itself—and rightfully discards sites which
     are already included.
(2) Should there exist a candidate site w.r.t. r∗ , then a furthest site will also be a candidate
     (w.r.t. r∗ ).
      The strategy is then to construct C by repeatedly selecting a furthest site. Of course,
it’s not immediatly clear why this approach should work for the 2r∗ boundary but not, say,
for 1.5r∗ . We resolve this matter in the proof’s details.
      Before we proceed, we note that our formal proof diverges from that of Kleinberg
and Tardos. While they begin by constructing an algorithm around the first observation
and proceed to establish, rather informally, a semantic correspondence between it and the
36:10                    VERIFIED APPROXIMATION ALGORITHMS                                Vol. 18:1




algorithm presented in this paper, we follow a more direct approach—that is, we only reason
about the presented algorithm. This reduces the first algorithm to a pedagogical tool.
     The algorithm repeatedly selects a site that lies furthest from the set of all hitherto
selected centers. The following Hoare triple expresses functional correctness and the approx-
imation factor of 2.

 {k ≤ |S |}
 C := (SOME s. s ∈ S );
 WHILE |C | < k INV {invar C } DO
     C := C ∪ {furthest from C };
 OD
 {|C | = k ∧ (∀ C 0. 0 < |C 0| ∧ |C 0| ≤ k −→ radius C ≤ 2 ∗ radius C 0)}

where furthest from C = (SOME s. s ∈ S ∧ distance C s = Max (distance C ‘ S )).
      We now present the proof, beginning with the invariant. To motivate the choice of
invariant, consider the special case when there exists a candidate site (w.r.t. some fixed r )
in each loop iteration. Let r be the radius of an arbitrary set, C be the set of previously
selected centers, s ∈ S the site to be added to C, and s 0 ∈ S a candidate site w.r.t. r. (Recall:
candidate means distance C s 0 > 2 ∗ r ). By choice of s, we have distance C s ≥ distance C
s 0 and therefore distance C s > 2 ∗ r. Since distance C s = Min (dist C ‘ S ), we have ∀ c ∈
C . dist c s ≥ distance C s > 2 ∗ r. Inductively, it follows (which we prove later) that
∀ c 1 ∈ C . ∀ c 2 ∈ C . c 1 6= c 2 −→ dist c 1 c 2 > 2 ∗ r.
      Now consider the case when in some loop iteration no more candidate sites exist, i.e., all
sites are included. As before, let C be the set of previously selected centers. By assumption,
we have ∀ s ∈ S . distance C s ≤ 2 ∗ r.
      This case distinction forms the invariant, which is defined as:
invar C =
(C 6= ∅ ∧ |C | ≤ k ∧ C ⊆ S ∧
 (∀ C 0. (∀ c 1 ∈C . ∀ c 2 ∈C . c 1 6= c 2 −→ 2 ∗ radius C 0 < dist c 1 c 2 ) ∨
         (∀ s∈S . distance C s ≤ 2 ∗ radius C 0)))
It is obvious that the invariant holds initially for C = {SOME s. s ∈ S }. Before we prove
that the invariant holds in each iteration, we first prove a useful lemma.
Lemma 6.1. (∀ c 1 ∈C . ∀ c 2 ∈C . c 1 6= c 2 −→ x < dist c 1 c 2 ) ∧
x < distance C s ∧ finite C ∧ C 6= ∅ −→
(∀ c 1 ∈C ∪ {s}. ∀ c 2 ∈C ∪ {s}. c 1 6= c 2 −→ x < dist c 1 c 2 )
Proof. The case c 1 ∈ C ∧ c 2 ∈ C is true by assumption and the case c 1 = s ∧ c 2 = s is
vacuously true. Assume c 1 ∈ C ∧ c 2 = s. Then
                    x < distance C c 2                                     by distance C s > x
                      ≤ dist c 2 c 1                    by definition and C 6= {} and finite C
                      = dist c 1 c 2                                          by dist commute
By symmetry, the case c 1 = s ∧ c 2 ∈ C is also true.
    Now we prove the preservation of the invariant. Assuming invar C, we show invar (C
∪ {s}) where s = furthest from C. The first three conjuncts hold trivially.
Vol. 18:1                      VERIFIED APPROXIMATION ALGORITHMS                            36:11




Proof. Let C 0 be an arbitrary set and let r = radius C 0. To prove the fourth conjunct, we
distinguish two cases:
     Case 1 s is a candidate site w.r.t. r. This negates ∀ s 0 ∈ S . distance C s 0 ≤ 2 ∗ r.
Consequently, ∀ c 1 ∈ C . ∀ c 2 ∈ C . c 1 6= c 2 −→ 2 ∗ r < dist c 1 c 2 must hold, since one of
the two must be true by assumption invar C. By substituting 2r for x in Lemma 6.1, we
conclude ∀ c 1 ∈ (C ∪ {s}). ∀ c 2 ∈ (C ∪ {s}). c 1 6= c 2 −→ 2 ∗ r < dist c 1 c 2 , hence invar
(C ∪ {s}).
     Case 2 s is not a candidate site w.r.t. r, i.e., distance C s ≤ 2 ∗ r. Then, for an
arbitrary s 0 ∈ S
               distance (C ∪ {s}) s 0 ≤ distance C s 0                by monotonocity of Min
                                      ≤ distance C s                           by choice of s
                                           ≤ 2 ∗ radius C 0                      by assumption
Hence invar (C ∪ {s}), i.e., the invariant is preserved.
     We now prove a lemma concerning the cardinality of the selected centers C that will
be useful in showing the postcondition. It is furthermore in this lemma that the question
raised above about the factor 2 is answered. Concretely, we will show that the dist c 1 c 2 >
2 ∗ r for all c 1 6= c 2 in C condition implies that any smaller set of centers must have radius
larger than r.
Lemma 6.2.
finite C ∧ |C | > n ∧ C ⊆ S ∧
(∀ c 1 ∈ C . ∀ c 2 ∈ C . c 1 6= c 2 −→ dist c 1 c 2 > 2 ∗ r ) −→
(∀ C 0. 0 < |C 0| ∧ |C 0| ≤ n −→ radius C 0 > r )
Proof. Assume, to the contrary, that there exists a set of centers C 0 with 0 < |C 0| ≤ n and
radius C 0 ≤ r. We show that |C 0| > n, a contradiction. Since the selected centers in C are
themselves sites in S, each must be by definition within radius C 0 ≤ r of a center in C 0,
but the centers in C are all more than 2 ∗ r apart from each other. There cannot be two
distinct c 1 , c 2 ∈ C with dist c i c 0 ≤ r, otherwise we would have:
                    2 ∗ r < dist c 1 c 2                                         by assumption
                          ≤ dist c 1 c 0 + dist c 0 c 2              by the triangle inequality
                          ≤2 ∗ r                                              by dist c i c 0 ≤ r
(Note that this argument would not work for any α ∗ r with α < 2.) Therefore there is a
unique center in C 0 for each center in C, and hence n = |C 0| ≥ |C |. But we assume |C | >
n, a contradiction.
     Finally we prove that the invariant and k ≤ |C | imply the postcondition:
|C | = k ∧ (∀ C 0. |C 0| > 0 ∧ |C 0| ≤ k −→ radius C ≤ 2 ∗ radius C 0)
Proof. Here |C | = k follows immediately. Let C 0 be arbitrary and assume 0 < |C 0| ≤ k.
We define r = radius C 0. By the invariant, (∀ s ∈ S . distance C s ≤ 2 ∗ r ) ∨ (∀ c 1 ∈ C .
∀ c 2 ∈ C . c 1 6= c 2 −→ dist c 1 c 2 > 2 ∗ r ) holds for C 0. We prove radius C ≤ 2 ∗ r by case
distinction on this disjunction.
      Case 1 Assumption: ∀ s ∈ S . distance C s ≤ 2 ∗ r. Then it trivially follows that Max
(distance C ‘ S ) = radius C ≤ 2 ∗ r.
36:12                    VERIFIED APPROXIMATION ALGORITHMS                              Vol. 18:1




    Case 2 Assumption: ∀ c 1 ∈ C . ∀ c 2 ∈ C . c 1 =6 c 2 −→ dist c 1 c 2 > 2 ∗ r. We prove the
conclusion by contradiction. Assume, to the contrary, that radius C > 2 ∗ r. This implies
that the site s = furthest from C is a candidate site w.r.t. r since distance C s = radius C
> 2 ∗ r. Furthermore, s cannot be in C, for if it were, then 0 = distance C s = radius C >
2 ∗ r, which is impossible. We can therefore insert it into C to obtain a set satisfying ∀ c 1 ∈
C ∪ {s}. c 2 ∈ C ∪ {s}. c 1 = 6 c 2 −→ dist c 1 c 2 > 2 ∗ r by Lemma 6.1. We thus have, by
Lemma 6.2, that ∀ C . |C | ≤ k ∧ |C | > 0 −→ radius C > r. In particular, radius C 0 > r =
radius C 0, a contradiction.




                                        7. Set Cover
As in the two previous sections, we base our formalization on [KT06], but this time
Chapter 11.3. We are given a finite set of elements U :: 0a set and an indexed collec-
tion S :: nat ⇒S0a set of subsets of U, defined over a segment {1..m} of the natural numbers,
such that U =       (S ‘ {1..m}). A function w :: nat ⇒ real associates a non-negative weight
to each (index of a) subset. Our goal is to find a set cover C of U
sc :: nat set ⇒ 0a set ⇒ boolS
sc C U = (C ⊆ {1..m} ∧         (S ‘ C ) = U )
                                          P
that minimizes the total weight W C = ( i ∈C . w i ). The greedy approach takes the subset
that covers the most elements relative to its weight, i.e., the subset S i that minimizes
                 wi
cost R i =
             |S i ∩ R|
where R is the set of elements yet to be covered. We will prove that this greedy algorithm
has an approximation factor of H d ∗ where H n is the n-th harmonic number and d ∗ the
cardinality of the largest subset. The algorithm is described by the following Hoare triple:

 {True}
 R := U ; C := ∅;
 WHILE R 6= ∅ INV {inv C R}
 DO i := min arg R m;
     R := R − S i ;
     C := C ∪ {i };
 OD
 {sc C U ∧ (∀ C 0. sc C 0 U −→ W C ≤ H d ∗ ∗ W C 0)}

The invariant inv is explained later. The function min arg (a variant of the load balancing
min arg) selects a subset with minimum cost while taking care that the overlap with R is
non-empty (unless there is no alternative):
min arg :: 0a set ⇒ nat ⇒ nat
min arg R 0 = 1
  min arg R (x + 1) =
  (let j = min arg R x
   in if S j ∩ R = ∅ ∨ S (x + 1) ∩ R 6= ∅ ∧ cost R (x + 1) < cost R j
      then x + 1 else j )
Vol. 18:1                    VERIFIED APPROXIMATION ALGORITHMS                             36:13




Like with the load balancing problem, a linear scan suffices here. The following properties
of min arg can be shown by induction on m:
Lemma 7.1.
(1) 0 < m −→ min arg R m ∈ {1..m}
(2) S (min arg R m) ∩ R = ∅ −→ (∀ i ∈{1..m}. S i ∩ R = ∅)
(3) k ∈ {1..m} ∧ S k ∩ R 6= ∅ −→ cost R (min arg R m) ≤ cost R k
      Unlike the proof of the load balancing problem, the desired approximation factor does
not arise from general bounds. Instead we employ a function c that returns the cost an
individual element contributes to the set cover. Namely, at every iteration of the algorithm
let c s = cost R i for all s ∈ S i ∩ R where i is the subset picked by min arg. As this
function is only relevant to the proof of the algorithm, we can use existential quantification
to lift it into the invariant. This function satisfies two important properties upon termination
of the algorithm:
               P
• W C = ( s ∈P        U . c s)
• ∀ k ∈ {1..m}. ( s ∈ S k . c s) ≤ H |S k | ∗ w k
The former may be rather intuitive, but reasoning about the latter is more difficult. Kleinberg
and Tardos provide an informal proof that argues about the sum of all element costs in
the subset at an arbitrary step of the algorithm where an element j of the subset is being
covered. Doing so requires indexing and reordering the elements from 1 to d where d is the
cardinality of the subset. We can then show the bound by splitting the subset in such a way
that elements already covered come before the element(s) that will be covered in this step,
and elements that have not yet been covered come after. Assuming k ∈ {1..m}, we can see:
(1) At least the elements from index j to d (cardinality) are not covered yet
     (i.e., |S k ∩ R| ≥ d − j + 1).
(2) Therefore cost R k = |S kw ∩k R| ≤ d−j+1
                                           wk

(3) Covered elements up to index j were covered by subsets picked by min arg
(4) Therefore cost R i ≤ cost R k because of Lemma 7.1.3
     P               Pd            Pd      wk       wk    wk          wk
(5)      s∈S k c s =   j=1 c skj ≤    j=1 d−j+1 = d + d−1 + · · · + 1 = H d ∗ w k
This proof is concise and the final statement readily implies the desired approximation factor.
This is a nice textbook proof, but a direct formalization is very unpleasant: it requires
indexing elements in the order in which they were covered by the algorithm. We give an
invariant-based proof that builds on the same proof idea but does not require any indexing.
This is the invariant:
inv :: nat set ⇒ 0a set ⇒ bool
inv C R = (sc C (U − R) ∧ R ⊆ U ∧ c exists C R)
c exists :: nat set ⇒ 0a set ⇒ bool
c exists C R = P
   (∃ c. W C = ( s∈U − R. c s) ∧
         (∀ i . 0 ≤ c i ) ∧
         (∀ k ∈{1..m}.
               P                            P|S k|
             ( s∈S k ∩ (U − R). c s) ≤ ( j = |S k ∩ R| + 1 1 / j ) ∗ w k ))
Using U − R we can argue about the elements that have already been covered by the
algorithm. The relation between the proof above and the upper bound in the last conjunct
of c exists is less apparent, but we can perform an index shift that makes the relation more
36:14                        VERIFIED APPROXIMATION ALGORITHMS                                          Vol. 18:1




obvious. Let d = |S k |, then:

                d                      d − |S k ∩ R|                   |S k ∩ (U − R)|
                X            wk            X             wk                 X               wk
                                =                              =
                             j                         d −j +1                            d −j +1
           j=|S k ∩ R| + 1                 j=1                                 j=1


This is closer to the sum we see in the proof by Kleinberg and Tardos, but complicates the
invariant proof as one now has to argue about the bounds of the sum as well as the content
of it, while our definition in c exists leaves the content of the sum as 1j .
     We now come to the proof of the invariant. Initialization is trivial if we pick c = (λ . 0).
We may now assume the invariant and R 6= ∅. Let i be the subset picked by min arg, moreover
R g :=SR − S i and C g := C ∪ {i }. First note 0 < m, as R = ∅ otherwise (R ⊆ U and
U =      (S ‘ {1..m})), hence i ∈ {1..m} (Lemma 7.1.1). Correctness is preserved as S i is a
subset of U , thus sc C g (U − R g ). Since we are only removing elements from R, R g remains a
subset of U as well. Before we prove that c exists C g R g holds, note that the set cover actually
strictly grows in an iteration of the algorithm. We know that ∃ k ∈ {1..m}. S k ∩ R 6= ∅
because R 6= ∅ and R ⊆ U. Combined with Lemma 7.1.2 we know that S i ∩ R 6= ∅.
Therefore new elements are covered in this iteration and by extension a subset was picked
that was not in the cover before (i ∈/ C), thus weight-eq: W C g = W C + w i. We define the
cost function c g = (λx . if x ∈ S i ∩ R then cost R i else c x ), where c is the cost function
obtained using c exists, and see that
                    X             X               X
                          cg s =        cg s +          cg s                           by R ⊆ U
                 s∈U −Rg               s∈U −R          s∈S i ∩ R
                                        X
                                 =              c s + |S i ∩ R|cost R i                              by c g -def
                                       s∈U −R
                                        X                              wi
                                 =              c s + |S i ∩ R|                                     by cost-def
                                                                   |S i ∩ R|
                                       s∈U −R
                                        X
                                 =              c s+w i                                        by S i ∩ R 6= ∅
                                       s∈U −R
                                 = W C + w i = W Cg                                   by inv -def and weight-eq

As cost R i is always positive, we know that ∀ i . 0 ≤ c g i is preserved. Finally we come to
the last conjunct of c exists. Assume k ∈ {1..m} and let A = S k ∩ S i ∩ R be the elements
of subset S k that will be covered in this iteration. We can transform the lower bound of
the right sum as follows lbr : |S k ∩ R g | + 1 = |S k ∩ R| − |A| + 1. This allows for the
following transformation:
                      X                      X                X
                                cg s =               cg s +       cg s              by R ⊆ U
                s∈S k ∩ (U − R g )              s∈S k ∩ (U − R)          s∈A
                           X
                =                       c s + |A|cost R i                                            by c g -def
                    s∈S k ∩ (U − R)
                              |S k |
                               X            1
                ≤wk                           + |A|cost R k                          by inv -def and Lem. 7.1.3
                                            j
                        j=|S k ∩ R| + 1
Vol. 18:1                     VERIFIED APPROXIMATION ALGORITHMS                                        36:15



                                                                         
                               |S k |
                               X               1           1
               = w k                            + |A|                                         by cost-def
                                               j       |S k ∩ R|
                          j=|S k ∩ R| + 1
                                                                                       
                               |S k |                         |S k ∩ R|
                               X               1                X  1
               = w k                            +                       
                                               j               |S k ∩ R|
                     j=|S k ∩ R| + 1     j=|S k ∩ R| − |A| + 1
                                                                
                           |S k |              |S k ∩ R|
                           X         1            X            1
               ≤ w k                  +                         
                                     j                         j
                        j=|S k ∩ R| + 1               j=|S k ∩ R| − |A| + 1
                               |S k |                                 |S k |
                                X                    1                X             1
               =wk                                     =wk                                           by lbr
                                                     j                              j
                      j=|S k ∩ R| − |A| + 1                    j=|S k ∩ R g | + 1

Unlike the proof in [KT06] we only had to argue about the cost of A here, as the cost of
previous elements is already proved by the assumed invariant.
     Finally we show how the invariant implies the approximation factor upon termination
of the algorithm:
Lemma 7.2. inv C ∅ ∧ sc C 0 U −→ W C ≤ H d ∗ ∗ W C 0
                                                               P
From inv C ∅, cPexists and R = ∅ we can infer cost-eq: W C = ( s∈U . c s) and h-bound :
∀ k ∈ {1..m}. ( s ∈ S k . c s) ≤ H |S k | ∗ w k and can derive the claim:
                                 X
                          WC=       cs                                      by cost-eq
                                            s∈U
                                            X X
                                        ≤                 cs                                by ∀ i . 0 ≤ c i
                                            k∈C 0 s∈S k
                                            X
                                        ≤           H |S k | ∗ w k                             by h-bound
                                            k∈C 0
                                            X
                                        ≤           H d∗ ∗ w k                                   by d ∗ -def
                                            k∈C 0
                                                     X
                                        = H d∗              w k = H d∗ ∗ W C 0
                                                    k∈C 0




                                               8. Bin Packing
We consider the linear time 32 -approximation algorithm for the bin packing problem proposed
by Berghammer and Reuter [BR03]. We are given a finite, non-empty set of objects U :: 0a
set, whose weights are given by a function w :: 0a ⇒ real. Note that in this paper nats are
implicitly converted to real s if needed. The weight of an object in U is strictly greater
                                                                                    P      than
zero, but bounded by a maximum capacity c :: nat. The abbreviation W (B) ≡ u∈B w(u)
denotes the weight of a bin B ⊆ U. The set U can be separated into small and large objects.
An object u is considered small if w(u) ≤ 2c , and large otherwise. We assume that all small
objects in U can be found in a set S, and large objects in U can be found in a set L, such
that S ∪ L = U and S ∩ L = ∅. Of course L and S could also be computed from U in
linear time. Variables U, w, c, L, and S are fixed throughout this section.
36:16                      VERIFIED APPROXIMATION ALGORITHMS                             Vol. 18:1




        A solution P to the bin packing problem is defined as follows:
bp :: 0a set set ⇒ bool
bp P = (partition on U P ∧ (∀ B ∈P . W B ≤ c))
The predicate partition on :: 0a set ⇒ 0a set set ⇒ bool is defined in the Isabelle/HOL
library: partition on U P means that P is a partition of the set U. Viewing every element of
P as a bin, bp P expresses that all objects are contained in exactly one bin and the weight
of every bin is bounded by c.
     The idea behind the algorithm proposed by Berghammer and Reuter is to split the
solution P into two partial solutions P 1 and P 2 . At every step of the algorithm we consider
two bins B 1 and B 2 which we try to fill with remaining objects from V ⊆ U that have not
been assigned yet. If adding the object to B 1 or B 2 would cause it to exceed its maximum
capacity, the bin is moved into the partial solution P 1 or P 2 respectively and cleared. Once
there are no small objects left, the solution is the union of the partial solutions P 1 and P 2 ,
the bins B 1 and B 2 (if they still contain objects), and the remaining large objects, which
each receive their own bin, as no two large objects can fit into a single bin. To ensure that
no empty bins are added to the solution, we define:
[[·]] :: 0a set ⇒ 0a set set
[[B ]] = (if B = ∅ then ∅ else {B })
The final union can now be written as P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V } where V
contains the remaining large elements. The algorithm can be specified by the following
Hoare triple:

 {True}
 P 1 := ∅; P 2 := ∅; B 1 := ∅; B 2 := ∅; V := U ;
 WHILE V ∩ S 6= ∅ INV {inv 3 P 1 P 2 B 1 B 2 V } DO
 IF B 1 6= ∅ THEN u := some (V ∩ S )
 ELSE IF V ∩ L 6= ∅ THEN u := some (V ∩ L)
        ELSE u := some (V ∩ S ) FI FI ;
 V := V − {u};
 IF W (B 1 ) + w (u) ≤ c THEN B 1 := B 1 ∪ {u}
 ELSE IF W (B 2 ) + w (u) ≤ c THEN B 2 := B 2 ∪ {u}
        ELSE P 2 := P 2 ∪ [[B 2 ]]; B 2 := {u} FI ;
        P 1 := P 1 ∪ [[B 1 ]]; B 1 := ∅ FI
 OD;
 P := P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V }
 {bp P ∧ (∀ Q. bp Q −→ |P | ≤ 3 / 2 ∗ |Q|)}

     Berghammer and Reuter prove functional correctness using a simplified version of this
algorithm where an arbitrary element of V is assigned to u. This allows for fewer case
distinctions, as the first IF −THEN −ELSE block can be ignored. One needs to find a loop
invariant that implies functional correctness and prove that it is preserved in the following
cases:
Case 1 The object fits into B 1 :
inv 1 P 1 P 2 B 1 B 2 V ∧ u ∈ V ∧ W B 1 + w u ≤ c −→
inv 1 P 1 P 2 (B 1 ∪ {u}) B 2 (V − {u})
Case 2 The object fits into B 2 :
Vol. 18:1                      VERIFIED APPROXIMATION ALGORITHMS                                  36:17




inv 1 P 1 P 2 B 1 B 2 V ∧ u ∈ V ∧ W B 2 + w u ≤ c −→
inv 1 (P 1 ∪ [[B 1 ]]) P 2 ∅ (B 2 ∪ {u}) (V − {u})
Case 3 The object fits into neither bin:
inv 1 P 1 P 2 B 1 B 2 V ∧ u ∈ V −→
inv 1 (P 1 ∪ [[B 1 ]]) (P 2 ∪ [[B 2 ]]) ∅ {u} (V − {u})
Berghammer and Reuter [BR03] define the following predicate as their loop invariant:
inv 1 P 1 P 2 B 1 B 2 V = bp (P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V })
As it turns out, this invariant is too weak. Assume inv 1 P 1 P 2 B 1 B 2 V. Suppose P 1
(alternatively P 2 ) already contains the non-empty bin B 1 . Note that this does not violate
the invariant because P 1 ∪ [[B 1 ]] = P 1 . Now, if the algorithm modifies B 1 by adding an
element from V such that B 1 becomes some B 1 0 then B 1 ∩ B 1 0 =      6 ∅ and B 1 ∈ P 1 , i.e., B 1 0
is no longer disjoint from the elements of P. The same issue arises with the added object u
∈ V, if {u} is already in P 1 or P 2 . To account for such cases, we will require additional
conjuncts:
inv 1 :: 0a set set ⇒ 0a set set ⇒ 0a set ⇒ 0a set ⇒ 0a set ⇒ bool
inv 1 P 1 P 2 B 1 B 2 V =
     S (P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V }) ∧
   (bp
          (P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]]) = U − V ∧
     B1 ∈  / P 1 ∪ P 2 ∪ [[B 2 ]] ∧
     B2 ∈  / P 1 ∪ [[B 1 ]] ∪ P 2 ∧
     (P 1 ∪ [[B 1 ]]) ∩ (P 2 ∪ [[B 2 ]]) = ∅)
There are different ways to strengthen the original inv 1 . We use the above additional
conjuncts as they can be inserted in existing proofs with little modification, and their
preservation in the invariant can be proved quite trivially. The first additional conjunct
ensures that no element still in V is already in a bin or partial solution. The second and
third additional conjuncts ensure distinctness of the bins B 1 and B 2 with the remaining
solution. The final conjunct ensures that the partial solutions with their added bins are
disjoint from each other. It should be noted that the last conjunct is not necessary to prove
functional correctness. It will, however, be needed in later proofs, and as its preservation in
this invariant for the simplified algorithm can be used in the proof of the full algorithm, one
can save redundant case distinctions by proving it now. Another advantage of proving it
now is that later invariants can remain identical to the invariants proposed in the paper.
       We now prove the preservation of inv 1 in all three cases. As we assume the invariant S     to
hold before the execution of the loop body, we can see from the first additional conjunct
(P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]]) = U − V and the assumption u ∈ V that not-in: ∀ B ∈ P 1 ∪
[[B 1 ]] ∪ P 2 ∪ [[B 2 ]]. u ∈
                             / B holds. This will be needed for all three cases. Now, we can begin
with Case 1. We first show
           bp (P 1 ∪ [[B 1 ∪ {u}]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V − {u}})
One can see that this union does not contain the empty set. The object u is now moved from
a singleton set into B 1 . Therefore, the union of all bins will again return U. To show that
this union remains pairwise disjoint, we can use not-in and the second additional conjunct of
inv 1 to show that u is not yet contained in the partial solution and B 1 is distinct from any
other bin. Therefore, combined with the assumption that the union was pairwise disjoint
before the modification, the union remains pairwise disjoint. To prove the preservation of the
second conjunct of bp, we need to show that the bin weights do not exceed their maximum
36:18                     VERIFIED APPROXIMATION ALGORITHMS                               Vol. 18:1




capacity c. The only bin that was changed in this step is B 1 , which has increased its weight
by w (u). As we are in Case 1, we can assume that u fits into B 1 , W (B 1 ) + w (u) ≤ c.
Therefore, this conjunct holds as well. Now, one only needs to show that the additional
conjuncts are preserved. For the first additional conjunct, we can again use not-in to show:
                   [
                      (P 1 ∪ [[B 1 ∪ {u}]] ∪ P 2 ∪ [[B 2 ]]) = U − (V − {u})
                   [
        ⇐⇒            (P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]]) ∪ {u} = U − (V − {u})       by not-in
                   [
        ⇐⇒            (P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]]) ∪ {u} = U − V ∪ {u}        by u ∈ U
Using the first additional conjunct of the assumed invariant, one can see that this must hold.
The remaining conjuncts
        B 1 ∪ {u} ∈  / P 1 ∪ P 2 ∪ [[B 2 ]]
        B2 ∈ / P 1 ∪ [[B 1 ∪ {u}]] ∪ P 2
        (P 1 ∪ [[B 1 ∪ {u}]]) ∩ (P 2 ∪ [[B 2 ]]) = ∅
can be automatically proved in Isabelle using not-in and the assumption that the conjuncts
of inv 1 P 1 P 2 B 1 B 2 V held before the modification. The proof for Case 2 is almost
identical to that of Case 1. The main difference is that the focus now lies on B 2 and the fact
that B 1 is now emptied and the previous contents added to the partial solution P 1 . One
therefore has to show that
        bp (P 1 ∪ [[B 1 ]] ∪ [[∅]] ∪ P 2 ∪ [[B 2 ∪ {u}]] ∪ {{v } | v ∈ V − {u}})
holds. As [[∅]] can be ignored, one can see that the act of emptying B 1 and adding it to the
partial solution will not otherwise affect the proof. The proof of bp in Case 3 is trivial, as
the modifications made in this step can simply be undone by applying the following steps:
          P 1 ∪ [[B 1 ]] ∪ [[∅]] ∪ (P 2 ∪ [[B 2 ]]) ∪ [[{u}]] ∪ {{v } | v ∈ V − {u}}
           = P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{u}} ∪ {{v } | v ∈ V − {u}}            by [[·]]-def
           = P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V }                         by u ∈ V
Now, one only needs to show that the remaining additional conjuncts hold. This can again
be shown automatically using not-in and the fact that inv 1 P 1 P 2 B 1 B 2 V held before the
modifications. Therefore, inv 1 is preserved in all three cases.
    To prove the approximation factor, we proceed as in [BR03] and establish suitable lower
bounds. The first lower bound
Lemma 8.1. bp P −→ |L| ≤ |P |
holds because a bin can only contain at most one large object, and every large object needs
to be in the solution. To prove this in Isabelle, we first make the observation that for every
large object there exists a bin in P in which it is contained. Therefore, we may obtain a
function f that returns this bin for every u ∈ L. Using the fact that any bin can hold at
most one large object, we can show that this function has to be injective, as every large
object must map to a unique bin. Hence, the number of large objects is equal to the number
of bins f maps to. Moreover, the image of f has to be a subset of P. Thus, the number of
large objects has to be a lower bound on the number of bins in P.
    As it turns out, the algorithm will ensure that there is always at least one large object
in a bin for the first partial solution as long as large objects are available. This means we
can assume that V ∩ L 6= ∅ −→ (∀ B ∈P 1 ∪ [[B 1 ]]. B ∩ L 6= ∅). Therefore, we can use the
previous lower bound to show the following:
Vol. 18:1                       VERIFIED APPROXIMATION ALGORITHMS                            36:19




Lemma 8.2. bp P ∧ inv 1 P 1 P 2 B 1 B 2 V ∧ (∀ B ∈P 1 ∪ [[B 1 ]]. B ∩ L 6= ∅) −→
|P 1 ∪ [[B 1 ]] ∪ {{v } | v ∈ V ∩ L}| ≤ |P |
   Another easy lower bound is this one:
                       P
Lemma 8.3. bp P −→ ( u∈U w u) ≤ c ∗ |P |
      The next lower bound arises from the fact that an object is only ever put into B 2 , and
therefore P 2 , if it would have caused B 1 to overflow. As a result of this, we can define a
bijective function f that maps every bin of P 1 to the object in P 2 ∪ [[B 2 ]] that would have
caused the bin to overflow. We define:
bij exists :: 0a set set ⇒ 0a set ⇒ bool
bij exists P V = (∃ f . bij betw f P V ∧ (∀ B ∈P . c < W B + w (f B )))
From this, we can make the observation that the number of bins in P 1 is a strict lower
bound on the number of bins of any correct bin packing P :
                                                               S
Lemma 8.4. bp P ∧ inv 1 P 1 P 2 B 1 B 2 V ∧ bij exists P 1 ( (P 2 ∪ [[B 2 ]])) −→
|P 1 | + 1 ≤ |P |
    Unlike the proof outlined in [BR03], we begin with a case distinction on P 1 . The
reasoning behind this is that if P 1 is empty, the strict nature of the lower bound cannot
be shown from the calculation that Berghammer and Reuter make. Therefore, we consider
the case where P 1 is empty separately. If P 1 is empty, our goal is to prove that 1 is a
lower bound on the number of bins in P. This follows from the fact that U is non-empty,
and therefore any correct bin packing must contain at least one bin. For the other case,
we may now assume that P 1 is non-empty. In the following proof, we will need the final
conjunct of inv 1 , (P 1 ∪ [[B 1 ]]) ∩ (P 2 ∪ [[B 2 ]]) = ∅, which we can transform into disjoint:
P 1 ∩ (P 2 ∪ [[B 2 ]]) = ∅. We also obtain the bijective function f and observe that, as the
object obtained from f for a bin B ∈ P 1 caused B to exceed its capacity, exceed : c < W (B )
+ w (f (B )) must hold. We can now perform the following calculation:
                             X
                    c|P1 | =       c
                            B∈P1
                            X                   X
                        <          W (B) +             w(f (B))            by P 1 6= ∅ and exceed
                            B∈P1               B∈P1
                            X                         X
                        =          W (B) +                        W (B)            by f bijective
                            B∈P1               B∈P 2 ∪ [[B 2 ]]
                                    X
                        =                            W (B)                            by disjoint
                            B∈P 1 ∪ P 2 ∪ [[B 2 ]]
                            X
                        ≤         w(u) ≤ c|P |                            by inv 1 and Lemma 8.3
                            u∈U
Therefore |P 1 | < |P | and, by extension, |P 1 | + 1 ≤ |P |.
     We only sketch the rest of the proof because it is almost identical to that in [BR03].
First we need two extensions of inv 1 to show the approximation ratio:
inv 2 P 1 P 2 B 1 B 2 V =
  (inv 1 P 1 P 2 B 1 B 2 V ∧
    (V ∩ L 6= ∅ −→  S (∀ B ∈P 1 ∪ [[B 1 ]]. B ∩ L 6= ∅))
                                                       S ∧
    bij exists P 1 ( (P 2 ∪ [[B 2 ]])) ∧ 2 ∗ |P 2 | ≤ | P 2 |)
36:20                      VERIFIED APPROXIMATION ALGORITHMS                                   Vol. 18:1




inv 3 P 1 P 2 B 1 B 2 V = (inv 2 P 1 P 2 B 1 B 2 V ∧ B 2 ⊆ S )
The motivation for the last conjunct in inv 2 is the following lower bound:
                                        S                        S
inv 1 P 1 P 2 B 1 B 2 V ∧ 2 ∗ |P 2 | ≤ | P 2 | ∧ bij exists P 1 ( (P 2 ∪ [[B 2 ]])) −→
   2 ∗ |P 2 ∪ [[B 2 ]]| ≤ |P 1 | + 1
     The main lower bound lemma (Theorem 4.1 in [BR03]) is the following:
Lemma 8.5. V ∩ S = ∅ ∧ inv 2 P 1 P 2 B 1 B 2 V ∧ bp P −→
   |P 1 ∪ [[B 1 ]] ∪ P 2 ∪ [[B 2 ]] ∪ {{v } | v ∈ V }| ≤ 3 / 2 ∗ |P |
    From this lower bound the postcondition of the algorithm follows easily under the
assumption that inv 2 holds at the end of the loop. This in turn follows because inv 3 can be
shown to be a loop invariant.


                              9. Conclusion and Future Work
In this first application of theorem proving to approximation algorithms we have verified
a number of classical approximation algorithms for fundamental NP-complete problems,
have corrected purported invariants from the literature and could even strengthen the
approximation ratio in one case. Moreover we have given simple invariant-based proofs
for algorithms where the proofs in the literature (or their direct formalization) are more
complicated.
     Although we have demonstrated the benefits of formal verification of approximation
algorithms, we have only scratched the surface of this rich theory. The next step is to explore
the subject more systematically. As a large fraction of the theory of approximation algorithms
is based on linear programming, this is a promising and challenging direction to explore.
Some linear programming theory has been formalized in Isabelle already [BHT19, PK19].
Approximation algorithms can also be formulated as relational programs, and verified
accordingly. This approach was explored in [BHS16], with some support from theorem
provers, but has yet to be fully formalized.

Acknowledgement. Tobias Nipkow is supported by DFG grant NI 491/16-1.


                                            References
[BHS16] Rudolf Berghammer, Peter Höfner, and Insa Stucke. Cardinality of relations and relational
        approximation algorithms. Journal of Logical and Algebraic Methods in Programming, 85(2):269–
        286, 2016.
[BHT19] Ralph Bottesch, Max W. Haslbeck, and René Thiemann. Verifying an incremental theory solver
        for linear arithmetic in Isabelle/HOL. In Andreas Herzig and Andrei Popescu, editors, Frontiers
        of Combining Systems, FroCoS 2019, volume 11715 of Lecture Notes in Computer Science, pages
        223–239. Springer, 2019. doi:10.1007/978-3-030-29007-8\_13.
[BK10]  Nikhil Bansal and Subhash Khot. Inapproximability of hypergraph vertex cover and applications to
        scheduling problems. In Samson Abramsky, Cyril Gavoille, Claude Kirchner, Friedhelm Meyer auf
        der Heide, and Paul G. Spirakis, editors, Automata, Languages and Programming, ICALP 2010,
        Part I, volume 6198 of LNCS, pages 250–261. Springer, 2010. doi:10.1007/978-3-642-14165-2\
        _22.
[BM03]  Rudolf Berghammer and Markus Müller-Olm. Formal development and verification of approxima-
        tion algorithms using auxiliary variables. In Maurice Bruynooghe, editor, Logic Based Program
        Synthesis and Transformation, LOPSTR 2003, volume 3018 of LNCS, pages 59–74. Springer, 2003.
        doi:10.1007/978-3-540-25938-1\_6.
Vol. 18:1                      VERIFIED APPROXIMATION ALGORITHMS                                                                36:21




[BR03]   Rudolf Berghammer and Florian Reuter. A linear approximation algorithm for bin packing with
         absolute approximation factor 3/2. Sci. Comput. Program., 48(1):67–80, 2003. doi:10.1016/
         S0167-6423(03)00011-X.
[ENR20] Robin Eßmann, Tobias Nipkow, and Simon Robillard. Verified approximation algorithms. In
         Nicolas Peltier and Viorica Sofronie-Stokkermans, editors, Automated Reasoning, IJCAR 2020,
         Part II, volume 12167 of Lecture Notes in Computer Science, pages 291–306. Springer, 2020.
         doi:10.1007/978-3-030-51054-1\_17.
[ENRS20] Robin Eßmann, Tobias Nipkow, Simon Robillard, and Ujkan Sulejmani. Verified approxi-
         mation algorithms. Archive of Formal Proofs, January 2020. http://isa-afp.org/entries/
         Approximation_Algorithms.html, Formal proof development.
[HR97]   Magnús M Halldórsson and Jaikumar Radhakrishnan. Greed is good: Approximating independent
         sets in sparse and bounded-degree graphs. Algorithmica, 18(1):145–163, 1997.
[KT06]   Jon M. Kleinberg and Éva Tardos. Algorithm Design. Addison-Wesley, 2006.
[NK14]   Tobias Nipkow and Gerwin Klein. Concrete Semantics with Isabelle/HOL. Springer, 2014. http:
         //concrete-semantics.org.
[NPW02] Tobias Nipkow, Lawrence Paulson, and Markus Wenzel. Isabelle/HOL — A Proof Assistant for
         Higher-Order Logic, volume 2283 of LNCS. Springer, 2002.
[PK19]   Julian Parsert and Cezary Kaliszyk. Linear programming. Archive of Formal Proofs, August 2019.
         http://isa-afp.org/entries/Linear_Programming.html, Formal proof development.
[Vaz03]  Vijai Vazirani. Approximation Algorithms. Springer, 2003.
[Wei81]  V.K. Wei. A lower bound for the stability number of a simple graph. Technical Memorandum
         81-11217-9, Bell Laboratories, 1981.




                                            This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                            license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                            Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse
                                            2, 10777 Berlin, Germany
