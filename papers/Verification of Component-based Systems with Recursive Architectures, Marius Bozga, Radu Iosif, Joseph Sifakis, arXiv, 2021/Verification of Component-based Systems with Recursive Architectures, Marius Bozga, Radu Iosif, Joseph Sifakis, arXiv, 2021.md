                                                Verification of Component-based Systems with
                                                            Recursive Architectures

                                                             Marius Bozga∗, Radu Iosif, Joseph Sifakis
                                             Univ. Grenoble Alpes, CNRS, Grenoble INP, VERIMAG, 38000 Grenoble, France
arXiv:2112.08292v1 [cs.FL] 15 Dec 2021




                                         Abstract
                                         We study a sound verification method for parametric component-based systems.
                                         The method uses a resource logic, a new formal specification language for dis-
                                         tributed systems consisting of a finite yet unbounded number of components.
                                         The logic allows the description of architecture configurations coordinating in-
                                         stances of a finite number of types of components, by means of inductive defini-
                                         tions similar to the ones used to describe algebraic data types or recursive data
                                         structures. For parametric systems specified in this logic, we show that decision
                                         problems such as reaching deadlock or violating critical section are undecidable,
                                         in general. Despite this negative result, we provide for these decision prob-
                                         lems practical semi-algorithms relying on the automatic synthesis of structural
                                         invariants allowing the proof of general safety properties. The invariants are de-
                                         fined using the WSκS fragment of the monadic second order logic, known to be
                                         decidable by a classical automata-logic connection, thus reducing a verification
                                         problem to checking satisfiability of a WSκS formula.
                                         Keywords: Resource Logic, Component-based Distributed Systems,
                                         Parameterized Verification


                                         1. Introduction

                                             Mastering the complexity of a distributed system requires a deep under-
                                         standing of its coordination mechanisms. We distinguish between endogenous
                                         coordination, that explicitly uses synchronization primitives in the code describ-
                                         ing the behavior of the components (e.g. semaphores, monitors, compare-and-
                                         swap, etc.) and exogenous coordination, that defines global rules describing
                                         how the components interact. These two orthogonal paradigms play different
                                         roles in the design of a system: exogenous coordination is used during high-level

                                           ∗ Corresponding author

                                              Email addresses: marius.bozga@univ-grenoble-alpes.fr (Marius Bozga),
                                         radu.iosif@univ-grenoble-alpes.fr (Radu Iosif),
                                         joseph.sifakis@univ-grenoble-alpes.fr (Joseph Sifakis)
                                            1 Institute of Engineering Univ. Grenoble Alpes




                                         Preprint submitted to Theoretical Computer Science                  December 16, 2021
model building, whereas endogenous coordination is considered at a later stage
of development, to implement the model using low-level synchronization.
     In this paper we focus on (high-level) exogenous coordination of distributed
systems, consisting of a finite yet unbounded number of interconnected compo-
nents. Communication is assumed to be correct, i.e. we abstract from packet
losses and corruptions. Components behave according to a small set of finite-
state abstractions of sequential programs, whose transitions are labeled with
events. They communicate via interactions (handshaking) modeled as sets of
events that occur simultaneously in multiple components. For instance, Fig. 1(a)
shows a token-ring system, whose components are depicted by yellow boxes con-
taining state machines that represent their behavior and whose architecture is
the set of connectors between components depicted by solid lines.
     The separation between behavior and coordination is a fundamental princi-
ple in the design of large-scale distributed systems [1]. This modular view of a
distributed system, in which the internal computation and the state changes of
each component are encapsulated in a well defined interface, is key to scalable
design methods that exploit a conceptual hierarchy. For instance, a ring is a
chain whose final output port is connected to the initial input port, whereas a
chain consists of a (head) component linked to a separate (tail) chain as shown
in Fig. 1(b). Moreover, system designers are accustomed to using architectural
patterns, such as rings, pipelines, stars, trees, etc., that define interactions be-
tween (unboundedly large) sets of components. Such high-level models of real-
life distributed systems are suitable for reasoning about correctness in the early
stages of system design, when details related to network reliability or the imple-
mentation of coordination by means of low-level synchronization mechanisms
(e.g. semaphores, monitors, compare-and-swap, etc.) are abstracted away.

1.1. Running Example
    For starters, we consider the following recursive definition of a token-ring
architecture, composed of a finite but unbounded number of stations that are
instances of the same component type S, connected via transfer connectors, of
interaction type T. The behavior of each station is a machine with two states,
indicating whether the station has a token (t) or not (n). The number of tokens
is constant and equal to the number of stations that are initially in state t. Each
station not having a token may receive a token from the left, via the in port
                                 in
(that triggers the transition n −→ t) and send its token to the right, via the out
                                      out
port (that triggers the transition t −−→ n). We refer to Fig. 1(a) for a depiction
of a token-ring system, defined by the rules:

                Ring()   ←    ∃y1 ∃y2 . Chain(y1 , y2 ) ∗ T(y2 , y1 )           (1)
        Chain(x1 , x2 ) ← Comp(x1 ) ∗ T(x1 , x2 ) ∗ Comp(x2 )                   (2)
        Chain(x1 , x2 ) ←     ∃y1 . Comp(x1 ) ∗ T(x1 , y1 ) ∗ Chain(y1 , x2 )   (3)
            Comp(x1 ) ← Sn (x1 )                                                (4)
                               t
            Comp(x1 ) ← S (x1 )                                                 (5)


                                          2
                                                                   T[n, 1]

                               out   in                        out        in                       out     in

      in            n                              n               ···                    n                            n           out
                                T[1, 2]                                                            T[n − 1, n]
               in                             in                                     in                          in

                    out                            out                                    out                          out

                    t                              t                                      t                            t
                        S[1]                            S[2]                          S[n − 1]                             S[n]


                                                                   (a)

           1                                                                                                               Ring()


                          3                                                                        Chain(y1 , y2 )

                                                               3                                   Chain(y11 , y2 )
                                      out              in                      out            in
               in
                          S(y1 )                  1
                                          T(y1 , y1 )
                                                                   1
                                                                S(y1 )             1
                                                                                T(y1    2
                                                                                     , y1 )
                                                                                                    Chain(y12 , y2 )         out



                                                                   (b)

                        Figure 1: Recursive Specification of a Token-Ring System

Intuitively, rule 1 states that a token-ring consists of a chain of components
and an interaction between the out port of the last and the in port of the
first component in the chain. A chain consists of either two components and an
interaction between their out and in ports, respectively (rule 2), or a component
and an interaction between its out port and the in port of the first component
of a distinct chain (3). The rules (4) and (5) intuitively say that a component
has type S and can be in state n or in state t, respectively. The star symbol ∗
used in the rules 1-5 is a commutative and associative logical connective that
composes sub-systems with disjoint sets of components and interactions; for
instance, in rule 2, the two components declared as Comp(x1 ) and Comp(x2 )
are necessarily different, meaning that x1 and x2 cannot be mapped to the
same value. The rules 2 and 3 correspond to the base and the inductive case of
a recursive definition of finite chains of length at least two. We refer to Fig. 1(b)
for a depiction of the recursive unfolding of the above rules.
    Note that no transfer of tokens is possible if the number of tokens in the
system is either zero (there is no token to be transfered) or equals the number
of components (there is no room to place a token). In this case, we say that a
system is in a deadlock. The decision problem “can a token-ring started in a non-
deadlock actually reach a deadlock?” is challenging, because it requires a proof
that holds for systems of any size, i.e. number of components and interactions.
We show that, even if such problems are undecidable, in general, a large number
of instances of these problems can be handled by the methods developed in this
paper.


                                                                      3
1.2. Contributions of this Work
    The parameterized verification method presented in this paper relies on an
idea reported in [2]. In addition to a complete development of the technical
results, previously omitted for space reasons, here we apply the verification
method to a specification language based on a resource logic, that resembles
Separation Logic [3], instead of the recursive term algebra introduced in [2].
An extension of this resource logic has been recently developed for Hoare-style
reasoning about the safety properties of programmed reconfiguration in dis-
tributed systems [4], to which the work presented here provides a push-button
verification back-end. In combination with the proof system reported in [4],
the verification method presented in this paper can automatically prove the
correctness of a distributed system after the reconfiguration of its coordinating
architecture. Since various dialects of (Concurrent) Separation Logic are being
commonly used to specify and reason about concurrent systems [5, 6, 7], we
expect this new logic to be easily accepted by the research and development
community. The contribution of this paper is three-fold:
  1. We introduce a logic-based language, called Configuration Logic (CL), to
     describe the sets of configurations (i.e. architectures and local states of
     components) of distributed systems parameterized by (i) the number of
     components of each type that are active in the system, e.g. a system with
     n readers and m writers, in which n and m are not known a priori and (ii)
     the pattern in which the interactions occur (e.g. a pipeline, ring, star or
     more general hypergraph structures). The language uses predicate sym-
     bols to hierarchically break the architecture into specific patterns. The
     interpretation of these predicate symbols is defined inductively by rewrit-
     ing rules consisting of formulæ that contain predicate atoms, in a way that
     recalls the usual definitions of algebraic datatypes [8] or heaps [3].
  2. We tackle a parametric safety problem concerning systems described in
     this language, which is essentially checking that the reachable states of
     every instance stays clear of a set of global error configurations, such as
     deadlocks or critical section violations. In particular, we show that both
     the parametric deadlock freedom and critical section violation problems
     are undecidable, even for architectures as simple as a chain of components.
  3. We develop a verification method that synthesizes parametric invariants
     from the syntactic description of the architecture (in CL) and from the
     behavior of its components (finite-state machines). The invariants and the
     set of error configurations are both described using a decidable fragment of
     Monadic Second Order Logic (MSO), that enables the use of off-the-shelf
     solvers for checking the resulting verification conditions.

   The stages of the synthesis of verification conditions are depicted in Fig. 2.
The starting point is a set of inductive definitions and a CL formula describing
the initial configurations of the system, together with a description of compo-
nent behavior by finite-state machines. The CL formula uses inductively defined


                                       4
Finite-state Machines                                      Monadic Second Order Logic

  behavior
                                                                                          Deadlock
                                                            flow            trap/mutex
                                                          formula            invariants
 formula(e)
                                          path                                            Reachability
                      rewriting
                        trees          automaton
   SID
                                                          initial
Configuration Logic                                   configurations



                              Figure 2: The Synthesis of Verification Conditions


 predicate symbols defined by sets of rewriting trees, describing the unfoldings
 of their inductive definitions. In particular, these rewriting trees describe archi-
 tectures, up to a permutation of the indices of components of each type.
     We use rewriting trees as the backbones of architecture encoding, from which
 we derive a MSO flow formula, that essentially describes the operational seman-
 tics induced by the interactions of the architecture, relying on (i) a static de-
 scription of the profile of the interactions (how they glue component types), and
 (ii) the transition systems describing the behavior of component types in the
 architecture. The main technical problem in building flow formulæ is tracking
 the identities and values of the variables that occur within predicate symbols,
 which, in turn, are recursively replaced by their definitions, in a rewriting tree.
 For instance, the y2 variable introduced by rule (1) using existential quantifi-
 cation substitutes the x2 variable from the definition of a Chain predicate, in
 rules (2) and (3) several times, before the same variable (y2 ) substitutes the x1
 variable in rule (4) or (5) (§1.1). This is achieved by defining a path automaton
 that traverses the rewriting tree downwards tracking the introduction of a vari-
 able by existential quantification in a rule to the rule where it is instantiated in
 a component atom.
     The flow formula is subsequently used to define invariants, i.e. over-approx-
 imations of the sets of states reachable from some initial configuration, in a
 system defined by some unfolding (rewriting) of the predicate symbols in CL
 specifications. In contrast with the classical approach of invariant inference us-
 ing, e.g. abstract interpretation [9], our technique generates invariants as MSO
 formulæ obtained directly from the flow formulæ, by a syntactic translation.
 Analogously, the set of error configurations (deadlocks and critical section vio-
 lations) is obtained directly from the flow formula of the system. The verification
 condition asks that the conjunction of the MSO formulæ describing the invariant
 and error configurations, respectively, is unsatisfiable; a satisfiable verification
 condition might indicate the presence of a spurious error caused by the over-
 approximation introduced by the invariant synthesis. Since we represent the
 configurations of a system by rewriting trees, we use a decidable fragment of
 MSO, interpreted over trees to answer the verification condition automatically.
     The paper is structured as follows. Section 2 introduces the definitions of
 component-based systems and their operational semantics, Section 3 describes


                                                      5
the resource logic used to define sets of configurations, Section 4 describes the
parametric decision problems and gives the general undecidability results, Sec-
tion 5 defines rewriting trees formally, together with a notion of a canonical
model, induced by a rewriting tree of a logical formula, Section 6 describes
the invariant synthesis and the encoding of the verification conditions in MSO,
Section 8 gives concluding remarks and sketches directions for future work.

2. Component-based Systems

2.1. Definitions
     This section introduces the definitions needed to formally describe our model
of component-based systems. We denote by N the set of natural numbers. Given
integers i and j, we write [i, j] for the set {i, i + 1, . . . , j}, assumed to be empty
if i > j. For a set A and an integer i ≥ 1, we denote by Ai the i-times Cartesian
product of A with itself. By pow(A) we denote the powerset of A. For a finite
set A, we denote by ||A|| its cardinality.
     Let P be a countable set of ports. We consider classes of component-based
systems that share the same signature Σ = (C, I, P), where:
     • C = {C1 , . . . , CN } is a finite set of relation symbols of arity one, called
       component types,
     • I = {I1 , . . . , IM } is a finite set of relation symbols of arity #(Ij ) ≥ 1, called
       interaction types,
     • P : C ∪ I → pow(P) ∪ i≥1 Pi is an interface associating each component
                                     S
       type C ∈ C a finite set of ports P(C) ∈ pow(P) and each interaction type
       I ∈ I a finite tuple of ports P(I) ∈ P#(I) .
                                  SN
W.l.o.g., we assume that i=1 P(Ci ) = P and P(Ci ) ∩ P(Cj ) = ∅, for all 1 ≤
i < j ≤ N , i.e. each port p belongs to the interface of exactly one component
type, denoted by comp(p). We denote by I(k) the subset of interaction types of
                             def
arity k, formally I(k) = {I ∈ I | #(I) = k}, for any k ≥ 1.

Example 1 (contd. from §1.1). The signature for the token-ring example
from Fig. 1a is Σ = h{S}, {T}, Pi, where P(S) = {in, out} and P(T) = hout, ini,
i.e. the interaction type T connects an out port to an in port.              

    The component and interaction types are interpreted as sets and relations
over a countably infinite universe U of indices. The particular nature of indices
is not important at this point; we assume that two indices can only be compared
for equality, with no other associated relation or function. An architecture α over
the signature Σ = (C, I, P) associates each component type Ci a set α(Ci ) ⊆ U
and each interaction type Ij a relation α(Ij ) ⊆ U#(Ij ) , defining:
    • components Ci [u], for some u ∈ α(Ci ), and
    • interactions Ij [u1 , . . . , u#(Ij ) ], for some hu1 , . . . , u#(Ij ) i ∈ α(Ij ).
Intuitively, an architecture is a description of the static structure of a system.
Note that an index u ∈ U can refer two (or more) different components C1 [u]
and C2 [u] belonging to different component types and similarly, a tuple of in-
dices u can refer two (or more) different interactions I1 [u] and I2 [u] of different

                                             6
interaction types, with the same arity; interactions may occur disconnected from
components, e.g. I[u1 , . . . , u#(I) ] does not necessarily mean that each component
comp(hP(I)ii )[ui ], for all i ∈ [1, #(I)] is present in the structure.

Example 2 (contd. from Example 1). Letting indices be natural numbers,
the structure of Fig. 1a is described by the architecture α over Σ, such that
α(S) = [1, n] and α(T) = {h1, 2i, h2, 3i, . . . , hn, 1i}i, for some n ≥ 2. 

    A behavior is described by a finite state machine M = (Q, P, →        − ), where Q
is a finite set of states, P ⊆ P is a finite set of ports and →    − ⊆ Q × P × Q is a
                                   p
transition relation; we write q − → q 0 instead of (q, p, q 0 ) ∈−
                                                                 → . Let B be the set of
finite-state machines with ports from P. The behavior map β : C → B associates
each component type C ∈ C with a state machine β(C) = (QC , P(C), →               − C ),
                                                  def
whose set of states is denoted by states β (C) = QC . In the following, we consider
w.l.o.g. that states β (Ci ) ∩ states β (Cj ) = ∅, for all 1 ≤ i < j ≤ N and define
     def SN
Qβ = i=1 states β (Ci ).

Example 3 (contd. from Example 1). The behavior of the component type
S in Fig. 1a is described by the state machine β(S) = ({t, n}, {in, out}, →
                                                                          − ), with
               in         out
transitions n −→ t and t −−→ n.                                                  

    For a port p we denote by Tβ (p) the set of transitions labeled by p in the
finite-state machine associated by β to comp(p). We extend this notation to
                                                  def
tuples of ports by taking Tβ (hp1 , . . . , pn i) = Tβ (p1 ) × · · · × Tβ (pn ). That is, the
set Tβ (hp1 , . . . , pn i) contains n-tuples of transitions ht1 , . . . , tn i labeled respec-
tively with ports hp1 , . . . , pn i. For an interaction I we use Tβ (I) as a shortcut
for Tβ (P(I)). In particular, Tβ (I) contains the set of tuples of component’s
transitions that are synchronizing by interaction I.
    A system S is a tuple (Σ, α, β), where α is an architecture and β is a behavior
associated with the signature Σ. When Σ is clear from the context, we omit it
and denote a system as (α, β).

2.2. Operational Semantics
    We represent the operational semantics of a system as a Petri net, recalled
below for self-containment reasons. A Petri net is a tuple N = (S, T, E), where
S is a set of places, T is a set of transitions, S ∩ T = ∅, and E ⊆ (S ×
                                                                                def
T ) ∪ (T × S) is a set of edges. Given x, y ∈ S ∪ T , we write E(x, y) = 1 if
                               def                        def
(x, y) ∈ E and E(x, y) = 0, otherwise. Let • x = {y ∈ S ∪ T | E(y, x) = 1},
  • def
x = {y ∈ S ∪ T | E(x, y) = 1} and lift these definitions to sets of nodes. A
marking of N is a function m : S → N. A transition t is enabled in m if and
                                                             t
only if m(s) > 0 for each place s ∈ • t. We write m →      − m0 whenever t is enabled
in m and m0 (s) = m(s) − E(s, t) + E(t, s), for all s ∈ S and t ∈ T . A sequence
                                                                   σ
                                                                   → m0 if and only if
of transitions σ = t1 , . . . , tn is a firing sequence, written m −
                                   0
either (i) n = 0 and m = m , or (ii) n ≥ 1 and there exist markings m1 , . . . , mn−1
               t1                    tn
such that m −→    m1 . . . mn−1 −→       m0 . A marking m is a deadlock of a Petri net


                                              7
N = (S, T, E) if and only if no transition t ∈ T is enabled in m and let Dead (N)
denote the set of deadlocks of N.
    A marked Petri net is a pair N = (N, m0 ), where m0 is the initial marking
of N. A firing sequence is initial if it starts in m0 . A marking m is reach-
able in N if there exists an initial firing sequence ending in m. Let Reach(N )
(resp. Step(N )) be the set of markings reachable (in one step) in N . For sim-
plicity, we write Reach(N, m0 ) and Step(N, m0 ) instead of Reach((N, m0 )) and
Step((N, m0 )), respectively. A marked Petri net N is boolean 2 if m(s) ≤ 1, for
each s ∈ S and m ∈ Reach(N ). All marked Petri nets considered in the following
will be boolean and we blur the distinction between a marking m : S → {0, 1}
and the set {s ∈ S | m(s) = 1}, by writing s ∈ m (resp. s 6∈ m) instead of
m(s) = 1 (resp. m(s) = 0).
Definition 1. The operational semantics of a system S = (Σ, α, β) with sig-
nature Σ = (C, I, P) is represented by the Petri net N(S) = (S, T, E), where:
     def S
 S =       C∈C { q[u] | q ∈ states β (C), u ∈ α(C) }
     def S
 T =       I∈I { (I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i) | hp1 , . . . , p#(I) i = P(I),
                     hu1 , . . . , u#(I) i ∈ α(I), ht1 , . . . , t#(I) i ∈ Tβ (I),
                     ∀i, j ∈ [1, #(I)]. i 6= j ⇒ ui 6= uj or comp(pi ) 6= comp(pj ) }
     def S
 E =       I∈I { (q[ui ], (I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i)),
                 ((I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i), q 0 [ui ]) |
                                pi
                       ti = (q −→ q 0 ), i ∈ [1, #(I)] }
     The places, transitions and edges of N(S) are defined jointly by the ar-
chitecture α and the behavior β. For every component C[u] in α, the Petri
net contains the places q[u], for each state q in states β (C). For every interac-
tion I[u1 , . . . , u#(I) ] in α, the Petri net contains one transition for every tuple
ht1 , . . . , t#(I) i of transitions of component types behavior, which are synchroniz-
ing according to I, that is, where their labeling ports hp1 , . . . , p#(I) i form the tu-
ple P(I). Moreover, a transition corresponding to an interaction I[u1 , . . . , u#(I) ]
involves pairwise distinct components; the last condition in the definition of T
above requires that ui 6= uj or comp(pi ) 6= comp(pj ). Finally, edges are defined
according to the tuple of synchronizing transitions ht1 , . . . , t#(I) i and connect to
pre- and post- places, respectively q[ui ] and q 0 [ui ], for each involved component
C[ui ]. For the sake of clarity we omit writing the tuple ht1 , . . . , t#(I) i when it
is determined by I, namely for those behaviors where a port labels exactly one
transition, in each state machine, as it is the case in the example below:
Example 4 (contd. from Example 3). The Petri net describing the execu-
tion semantics of the token-ring system from Fig. 1(a) is given in Fig. 3. Con-
sider the marking of this Petri net depicted in dashed lines. From this marking,

   2 Boolean Petri nets are sometimes called 1-safe or 1-bounded in the literature.




                                               8
                 n[1]                  n[2]                                            n[n]



   T[n, 1]                 T[1, 2]               T[2, 3]        ...      T[n − 1, n]               T[n, 1]


                 t[1]                  t[2]                                             t[n]



                   Figure 3: The Execution Semantics of a Token-Ring System


the sequence of interactions T[1, 2], T[2, 3], . . . , T[n−1, n], T[n, 1] can be fired any
number of times, in this order. These interactions correspond to the joint exe-
cution of the transitions labeled by the ports out and in, from any two adjacent
components i and (i mod n) + 1 of the ring, respectively.                               

   The executions of a system S = (Σ, α, β) can be represented by the firing
sequences of a marked Petri net involving only those boolean markings of N(S),
that contain exactly one state q ∈ states β (C) per component C[u], such that
u ∈ α(C). We formalize and prove this fact below:

Definition 2. Given a system S = (Σ, α, β) with signature Σ = (C, I, P), a
marking m of the Petri net N(S) = (S, T, E) is precise if and only if, for each
C ∈ C and each u ∈ α(C), we have ||m ∩ {q[u] | q ∈ states β (C)}|| = 1.

Proposition 1. Given a system S and a precise initial marking m0 of N(S),
every marking m ∈ Reach(N(S), m0 ) is precise.

Proof : Let S = (Σ, α) and m0 ∈ Reach(N(S), m0 ) be a marking. The proof
goes by the length n ≥ 0 of the firing sequence taking m0 into m0 . For the base
case n = 0, we have that m0 = m0 is precise, by hypothesis. For the inductive
step n ≥ 1, let m be the predecessor of m0 in the sequence, hence m is precise
for S, by the inductive hypothesis. Then, by Def. 1, there exists a transition
(I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i) in T , such that

             m0 = (m \ {q1 [u1 ], . . . , q#(I) [u#(I) ]}) ∪ {q10 [u1 ], . . . , q#(I)
                                                                                  0
                                                                                       [u#(I) ]}         (6)
                                                           pi
where P(I) = hp1 , . . . , p#(I) i and ti = (qi −→ qi0 ) ∈−
                                                          →comp(pi ) for all i ∈ [1, #(I)]
and moreover ui 6= uj or comp(pi ) 6= comp(pj ) for all distinct i, j ∈ [1, #(I)].
    Let C ∈ C be a component type and let u ∈ α(C) be an index. Since m is
precise, we have m ∩ {q[u] | q ∈ states β (C)} = {q ∗ [u]}, for some state q ∗ . We
distinguish the following cases:
    • u = ui for some i ∈ [1, #(I)] and q ∗ = qi In this case, we have:

               m0 ∩ {q[u] | q ∈ states β (C)} = {qi0 [u]}, by definition of m0 in (6)

   • u = ui for some i ∈ [1, #(I)] and q ∗ 6= qi . In this case, as the transition
     (I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i) fires in m it follows that qi [u] ∈ m. But
     then qi [u] ∈ m ∩ {q[u] | q ∈ states β (C)} = {q ∗ [u]} implies qi = q ∗ , which
     is a contradiction.


                                                     9
     • u 6∈ {u1 , . . . , u#(I) }. In this case, we have:

                 m ∩ {q[u] | q ∈ states β (C)} = m0 ∩ {q[u] | q ∈ states β (C)}

In all non-contradictory cases, we obtain that ||m ∩ {q[u] | q ∈ states β (C)}|| = 1.
Because C ∈ C and u ∈ α(C) are arbitrary, m is precise for S.                     

3. The Configuration Logic

    By configuration of a system, we understand the architecture describing the
components and interactions from the system, together with a snapshot of its
current state. Configurations are used to reason about parametric systems,
that share a common architectural pattern (style) and differ in the number of
instances of a certain component type. For instance, a token-ring (Fig. 1) applies
the same architectural pattern (the output of each component is connected to
its right neighbor in a round-robin fashion) to any number n ≥ 2 of components.

Definition 3. A configuration of a system S = (Σ, α, β) is a pair (α, m), where
α is an architecture over the signature Σ and m is a precise marking of N(S).

   We aim at describing sets of configurations recursively (i.e. configurations
with more complex structure being obtained by composing simpler ones), using
the following definition of composition:

Definition 4. Two architectures α1 and α2 , over the signature Σ = (C, I, P),
are disjoint if and only if α1 (C) ∩ α2 (C) = ∅, for all C ∈ C and α1 (I) ∩ α2 (I) = ∅,
for all I ∈ I. If α1 and α2 are disjoint, the composition of configurations
                                                     def
(α1 , m1 ) and (α2 , m2 ) is (α1 , m1 ) • (α2 , m2 ) = (α1 ∪ α2 , m1 ∪ m2 ), where α1 ∪ α2
denotes the pointwise union of the architectures α1 and α2 :
    • (α1 ∪ α2 )(C) = α1 (C) ∪ α2 (C), for each C ∈ C,
    • (α1 ∪ α2 )(I) = α1 (I) ∪ α2 (I), for each I ∈ I.
The composition (α1 , m1 ) • (α2 , m2 ) is undefined if α1 and α2 are not disjoint.

It is easy to check that the composition of configurations (α1 , m1 ) and (α2 , m2 )
with disjoint architectures is again a configuration, in particular m1 ∩ m2 = ∅
and m1 ∪ m2 is a precise marking of the Petri net N(Σ, α1 ∪ α2 , β).
    We introduce the configuration logic (CL) to describe (possibly infinite) sets
of configurations, via inductive definitions. Let Σ = (C, I, P) be a signature and
β : C → B be a behavior map, fixed for the rest of this section. Let X1 be a set
of first-order variables and A be a countably infinite set of predicate symbols,
where #(A) ≥ 0 denotes the arity of a predicate symbol A ∈ A. The formulæ
of CL are inductively defined by the following syntax:

 φ    ::= emp | C(x) | Cq (x) | I(x1 , . . . , x#(I) ) | A(x1 , . . . , x#(A) ) | φ ∗ φ | ∃x . φ

where C ∈ C are component types, q ∈ states β (C) are states, I ∈ I are inter-
action types, A ∈ A are predicate symbols and x1 , x2 , . . . ∈ X1 denote first-
order variables. Atomic formulæ of the form C(x) or Cq (x), I(x1 , . . . , x#(I) ) and


                                               10
A(x1 , . . . , x#(A) ) are called component, interaction and predicate atoms, respec-
tively. The logical connective ∗ is an associative and commutative separating
conjunction operator.
    By fv(φ) we denote the set of free variables that do not occur within the scope
of a quantifier; φ is called quantifier-free (q.f.) if and only if it has no quantifiers
and a sentence if and only if fv(φ) = ∅, respectively. A substitution is a partial
mapping θ : X1 → X1 and φθ is the formula obtained by replacing each variable
                                                                  def
x ∈ fv(φ) ∩ dom(θ) by θ(x) in φ, where dom(θ) = {x ∈ X1 | θ is defined at x}.
We denote by [x1 /y1 , . . . , xk /yk ] the substitution that replaces xi with yi , for all
i ∈ [1, k] and is undefined everywhere else. This notation is extended to tuples of
variables of equal length as [x/y], where x = hx1 , . . . , xk i and y = hy1 , . . . , yk i.
    Intuitively, a formula emp describes configurations with empty architecture,
C(x) (resp. Cq (x)) describes configurations with architectures consisting of a
single instance of the component type C, indexed by the value of x (resp. in
state q), and I(x1 , . . . , xk ) describes a single interaction of type I, between com-
ponents indexed by x1 , . . . , xk , respectively. The formula Cq1 (x1 )∗. . .∗Cqk (xk )∗
I(x1 , . . . , xk ) describes an architecture consisting of k pairwise distinct instances
of the component type C, in states q1 , . . . , qk , respectively, joined by an inter-
action of type I. The formula I(x1 , . . . , xk ) ∗ I(x01 , . . . , x0k ) states the existence of
two interactions of type I, with distinct tuples of indices, given by the values
of hx1 , . . . , xk i and hx01 , . . . , x0k i, respectively, i.e. the values of xi and x0i must
differ for at least one i ∈ [1, k].
    The semantics of CL formulæ is given by a satisfaction relation |=s∆ between
configurations and formulæ. This relation is parameterized by:
    • a store s : X1 → U, i.e. a function mapping variables to indices, and
    • a set of inductive definitions (SID) ∆ consisting of rules of the form
         A(x1 , . . . , x#(A) ) ← φ, where φ is a CL formula such that fv(φ) = {x1 , . . . , x#(A) }.
The satisfaction relation is defined inductively on the structure of the formulæ:

 (α, m)    |=s∆   emp                        ⇐⇒    α(C) = ∅, for all C ∈ C, α(I) = ∅,
                                                   for all I ∈ I and m = ∅
 (α, m)    |=s∆   C(x)                       ⇐⇒    α(C) = {s(x)}, α(C0 ) = ∅, for all
                                                   C0 ∈ C r {C}, α(I) = ∅, for all I ∈ I and
                                                   m = {q[s(x)]}, for some q ∈ states β (C)
 (α, m)    |=s∆   Cq (x)                     ⇐⇒    α(C) = {s(x)}, α(C0 ) = ∅, for all
                                                   C0 ∈ C r {C}, α(I) = ∅, for all I ∈ I
                                                    and m = {q[s(x)]}
 (α, m)    |=s∆   I(x1 , . . . , x#(Ik ) )   ⇐⇒    α(C) = ∅, for all C ∈ C, α(I) = {hs(x1 ),
                                                   . . . , s(x#(Ik ) )i}, α(I0 ) = ∅, for all
                                                   I0 ∈ I r {I} and m = ∅
 (α, m)    |=s∆   A(x1 , . . . , x#(A) )     ⇐⇒    (α, m) |=s∆ φ[y1 /x1 , . . . , y#(A) /x#(A) ],
                                                   for some rule A(y1 , . . . , y#(A) ) ← φ ∈ ∆




                                              11
  (α, m)   |=s∆   φ1 ∗ φ2     ⇐⇒      there exist configurations (α1 , m1 ), (α2 , m2 )
                                      such that (α, m) = (α1 , m1 ) • (α2 , m2 ) and
                                      (αi , mi ) |=s∆ φi , for i = 1, 2.
                                                   0
  (α, m)   |=s∆   ∃x . φ1     ⇐⇒      (α, m) |=s∆ φ1 , for some store s0 that agrees
                                      with s on all variables from X1 r {x}
To simplify the notation, we consider that ∆ is fixed and omit the ∆ subscript
in the following. If the formula φ is a sentence, we can omit the store s from
the satisfaction relation |=s and write (α, m) |= φ. In this case, (α, m) is said to
be a model of φ and denote by [[φ]] the set of models of the sentence φ. For two
sentences φ and ψ, we say that φ entails ψ if [[φ]] ⊆ [[ψ]], written φ |= ψ.

Example 5 (contd. from §1.1). The SID consisting of the rules 1-5 (§1.1)
defines systems with token-ring architectures. On the other hand, the rules below
define chains of S and T components, with at least n, t ∈ N components in state
n and t, respectively:

           Chain 0,0 (x, x) ←       S(x)
           Chain 0,1 (x, x) ←       St (x)        Chain 1,0 (x, x) ← Sn (x)
           Chain n,t (x, z) ← ∃y. St (x) ∗ T(x, y) ∗ Chain n,t−̇1 (y, z)
           Chain n,t (x, z) ← ∃y. Sn (x) ∗ T(x, y) ∗ Chain n−̇1,t (y, z)
            def
where k −̇1 = max(k − 1, 0), k ∈ N.                                                       

   Below we show that CL sentences define indeed system configurations.

Proposition 2. Given a sentence φ of CL, if (α, m) ∈ [[φ]] then m is a precise
marking of the Petri net N(Σ, α, β).

Proof : We prove a more general statement: for each formula φ and each store
s, if (α, m) |=s φ then m is a precise marking of N(Σ, α, β). The proof is by
induction on the definition of the |=s relation, by distinguishing the following
cases:

   • φ ∈ {emp, I(x1 , . . . , x#(I) )}: m = ∅ and α(C) = ∅, for all C ∈ C, thus m is
     trivially precise for N(Σ, α, β).
   • φ = C(x): m = {q[s(x)]}, for some q ∈ states β (C), α(C) = {s(x)} and
     α(C0 ) = ∅, for all C0 ∈ C r {C}, hence m is precise for N(Σ, α, β).

   • φ = Cq (x): m = {q[s(x)]}, α(C) = {s(x)} and α(C0 ) = ∅, for all C0 ∈
     C r {C}, hence m is precise for N(Σ, α, β).
   • φ = A(x1 , . . . , x#(A) ): (α, m) |=s ψ[y1 /x1 , . . . , y#(A) /x#(A) ], for some rule
     A(y1 , . . . , y#(A) ) ← ψ ∈ ∆ and apply the inductive hypothesis.




                                             12
   • φ = φ1 ∗φ2 : if (α, m) |=s φ1 ∗φ2 then there exists configurations (αi , mi ) |=s
     φi , for i = 1, 2, such that α1 and α2 are disjoint, α = α1 ∪ α2 and
     m = m1 ∪ m2 . By the inductive hypothesis, mi is a precise marking of
     N(Σ, αi , β), for i = 1, 2. Let C ∈ C be a component type and let u ∈ α(C)
     be an index. Then either u ∈ α1 (C) or u ∈ α2 (C), but not both. Let
     us consider the case u ∈ α1 (C) r α2 (C), the other case being symmet-
     ric. Then m ∩ {q[u] | q ∈ states(C)} = m1 ∩ {q[u] | q ∈ states(C)}, hence
     ||m ∩ {q[u] | q ∈ states(C)}|| = ||m1 ∩ {q[u] | q ∈ states(C)}|| = 1. Since the
     choices of C and u were arbitrary, we obtain that m is precise.
   • φ = ∃x . φ1 : by an application of the inductive hypothesis.                        


4. Decision Problems

    A decision problem is a class of yes/no queries of the same kind, that differ
only in their input. All decision problems considered in this paper are parame-
terized by a given signature Σ = (C, I, P). The queries take as input a sentence
φ, a SID ∆, a behavior map β : C → B and a tuple of states hq1 , . . . , qn i ∈ Qnβ
for some n ∈ N. They are defined as follows:
   • deadlock (φ, ∆, β): is there a configuration (α, m), such that (α, m) |=∆ φ
     and Reach(N(Σ, α, β), m) ∩ Dead (N(Σ, α, β)) 6= ∅ ?
   • reach(φ, hq1 , . . . , qk i, ∆, β): are there configurations (α, m), (α, m0 ) and
     indices u1 , . . . , uk ∈ U, such that (α, m) |=∆ φ, m0 ∈ Reach(N(Σ, α, β), m)
     and {qi [ui ] | i ∈ [1, k]} ⊆ m0 , with q1 [u1 ], . . . , qk [uk ] pairwise distinct?
    The above queries occur typically as correctness conditions in system veri-
fication. For instance, proving that, in every system described by a formula φ,
no freeze configuration is reachable means showing that deadlock (φ, ∆, β) does
not hold. Similarly, proving that each system described by φ stays clear of a set
of error configurations e.g., at most one component is in some critical state qcrit
at any time amounts to proving that reach(φ, hqcrit , qcrit i, ∆, β) does not hold.

4.1. Undecidability Results for Linear Systems
    We show that the problems defined by the sets of queries above, taken over
all inputs, but parameterized by a fixed given signature, are undecidable. In
fact, we shall prove stronger results, in which the input formulæ define sets of
configurations with linear architectures.

Definition 5. Given a signature Σ = ({C}, I, P), a sentence φ, interpreted
over a SID ∆, is linear if and only if φ |=∆∪Λ φL , where Λ consists of the rules:

         L(x, x) ←      C(x) ∗        ∗   I∈I(1) I(x)
         L(x, y) ← ∃z . C(x) ∗        ∗   I∈I(1) I(x) ∗   ∗   I∈I(2) I(x, z) ∗ L(z, y)

where L is a binary predicate symbol and φL is the sentence ∃x∃y . L(x, y).


                                           13
For instance, the sentences ∃x∃y . Chain(x, y) (§1.1) and ∃x∃y . Chain n,t (x, y)
for n, t ≥ 0 (Example 5) are linear, when taking C = {S} and I = {T}.
    Below we show that undecidability occurs for classes of queries taking linear
sentences as input, over a fixed signature consisting of only one component type
and a fixed set of interaction types, which is not part of the input of a query.

Theorem 1. The following problems are undecidable:
                                def
             LinearDeadlock     =     {deadlock (φ, ∆, β) | φ |=∆∪Λ φL }
                                def
          LinearReachability    =     {reach(φ, hq1 i, ∆, β) | φ |=∆∪Λ φL }

The idea of the proof is to build a component-based system with linear archi-
tecture that simulates the execution of a Post-Turing machine. We present the
construction in §4.2 and complete the proof in §4.3.

4.2. Simulation of Post-Turing Machines by Linear Systems
    A Post-Turing machine [10, 11] executes sequential deterministic programs
M of the form 1 : stmt1 ; 2 : stmt2 ; . . . ; m : stmtm , where each statement
stmti is one of following: write 0, write 1, go right, go left, goto step j if read 0,
goto step j if read 1, stop, for some j ∈ [1, m]. The machine operates on an
infinite tape of zeroes and ones. Initially, the head is pointing at some position
on the tape and the program control is at the first statement. At any step,
the current statement is executed and the tape content, the head position and
control are updated according to that statement.
    We simulate a Post-Turing machine by a component-based system with lin-
ear architecture. Its signature ΣP T = (CP T , IP T , PP T ) is presented in Fig. 4(a)
and consists of one component type CP T and ten interaction types IP T , with
associated ports as presented in the figure. In particular, the signature does not
depend on the program executed by the machine.
    The linear system that simulates a Post-Turing machine is depicted in Fig. 4(b).
First of all, the machine program M is encoded in the behavior βM of the
component type CP T . In particular, this behavior includes three disjoint state
machines, as described in Table 1, labeled with the same set of ports. Second,
in the linear system, each component plays a different role depending on its
position, i.e. it runs according to one of the three state machines below:
    • the leftmost ctrl component behaves according to the control state ma-
       chine derived from the program M : it issues the commands to be executed
       by the tape components depending on the current statement, and proceeds
       further according to the control flow of M . In case of read commands, it
       goes to an intermediate state, waiting to receive either read 0 or read 1
       answers. In case of left! commands, it goes to an error state signaling the
       overflow of the tape on the left side. The complete definition is given in
       Table 1 (top).
    • the middle tape components behave according to the tape state machine
       and mimic the behavior of a single tape cell: the k-th component state
       records the k-th symbol of the tape γk and the presence (>) or absence


                                         14
                                 CP T                                                             IP T

          in write 0                         out write 0                    out write 0                      in write 0
          in write 1                         out write 1                    out write 1                      in write 1
             in right                        out right                          out right                    in right
           in right!                         out right!                        out right!                    in right!
              in lef t           CP T        out lef t                           out lef t                   in lef t
             in lef t!                       out lef t!                         out lef t!                   in lef t!
             in read                         out read                            out read                    in read
          out read 0                         in read 0                         in read 0                     out read 0
          out read 1                         in read 1                         in read 1                     out read 1
                                                                                  out err
                                  out err

                                                                   (a)

                                                                         i : stmt i

                          γ1                    ...                    γk                ...              γn




                a                       a                   in a              out a                a                a
                 .                       .                  .                     .                 .                .
   ctrl          .        tape           .                  .       tape          .                 .     tape       .     sink
                 .                       .                  .                     .                 .                .
i : stmt i      a0       γ1 , ⊥         a0      ...       out a0   γk , >     in a0      ...       a0    γn , ⊥     a0
                 .                       .                  .                     .                 .                .
                 .                       .                  .                     .                 .                .
                 .                       .                  .                     .                 .                .

                                                                   (b)

Figure 4: Undecidability of Deadlock and Reachability for Linear Component-based Systems


       (⊥) of the machine head at that cell. They react to commands (received
       through in-ports) by changing their state and/or further issuing com-
       mands to their neighbors (sent through out-ports). The complete defini-
       tion is given in Table 1 (middle).
     • the rightmost sink component behaves according to the sink state machine
       and detects the overflow of the tape on the right side and signals it as an
       error. This happens when this component receives the right! command.
       The complete definition is given in Table 1 (bottom).

4.3. Proof of Theorem 1
   Let M be the program of a Post-Turing machine and let w = γ1 γ2 . . . γn
be a finite word in {0, 1}n , assuming moreover wlog3 that n ≥ 2. Consider
the signature ΣP T and the behavior βM as defined in the previous section.
                                                              def (1)     def (2)
Furthermore, consider the following set ∆w of rules, where I1 = IP T , I2 = IP T :

   Zeroes(x, x) ←
                                                 (0,⊥)
                                             CP T (z) ∗            ∗   I∈I1 I(x)
   Zeroes(x, y) ←
                                              (0,⊥)
                                        ∃z . CP T (x) ∗            ∗   I∈I1 I(x) ∗    ∗      I∈I2 I(x, z) ∗ Zeroes(z, y)



   3 w can be augmented with extra zeroes on the right




                                                                   15
                                                        def
 control state machine with states QM
                                    ctrl = {i, (i, ) | i ∈ [1, m + 1]} represents the program M
                                             out write 0
 i : write 0                             i −−−−−−−→ i+1
                                            out write 1
 i : write 1                             i −−−−−−−→ i+1
                                             out right
 i : go right                            i −−−−−−→ i+1
                                             out lef t                  out lef t!                   out err
 i : go left                             i −−−−−→ i+1, i −−−−−→ (i, ), (i, ) −
                                                                             −−−−
                                                                                → (i, )
                                             out read                              in read 0           in read 1
 i : goto step j if read 0               i −−−−−→ (i, ), (i, ) −−−−−−→ j, (i, ) −−−−−−→ i+1
                                             out read                              in read 1           in read 0
 i : goto step j if read 1               i −−−−−→ (i, ), (i, ) −−−−−−→ j, (i, ) −−−−−−→ i+1
 i : stop                                / ∗ nothing ∗ /
                                                  def
 tape state machine with states Qtape = {(γ, π), (γ, π, a) | γ ∈ {0, 1}, π ∈ {⊥, >}, a ∈ IP T r {err }}
         in a                                                 out a
 (γ, ⊥) −−→ (γ, ⊥, a)                     (γ, ⊥, a) −−−→ (γ, ⊥)                           ∀a 6= right!, left!, err
         in right!                                              out lef t!
 (γ, ⊥) −−−−−→ (γ, >)                     (γ, ⊥, left) −−−−−→ (γ, >)
         in write γ 0
 (γ, >) −−−−−−−→ (γ 0 , >)
         in read                                                 out read γ
 (γ, >) −−−−−→ (γ, >, read )              (γ, >, read ) −−−−−−−→ (γ, >)
         in right                                                 out right!
 (γ, >) −−−−−→ (γ, >, right)              (γ, >, right) −−−−−−→ (γ, ⊥)
         in lef t!
 (γ, >) −−−−−→ (γ, ⊥)
                                                                             def
                      sink state machine with states Qsink = {idle, busy}
                          in right!                                                   out err
                      idle −−−−−→ busy                                       busy −
                                                                                  −−−−
                                                                                     → busy

   Table 1: The behavior βM of CP T for a Post-Turing machine executing a program M


        Word w (x, y) ←
                                                                      (γ ,>)
                                      ∃z2 . . . ∃zn−1 . CP T1 (x) ∗ I∈I1 I(x) ∗          ∗
                                         ∗                     (γ2 ,⊥)
                                            I∈I2 I(x, z2 ) ∗ CP T      (z2 ) ∗ I∈I1 I(z2 ) ∗   ∗
                                         ∗                      (γ3 ,⊥)
                                            I∈I2 I(z2 , z3 ) ∗ CP T     (z3 ) ∗ I∈I1 I(z3 ) ∗  ∗
                                           ...
                                         ∗                        (γn ,⊥)
                                            I∈I2 I(zn−1 , y) ∗ CP T       (y) ∗ I∈I1 I(y)       ∗
         Tape w (x, y) ←              ∃z1 ∃w1 ∃z2 ∃w2 . Zeroes(x, z1 ) ∗
                                         ∗ I∈I2 I(z1 , w1 ) ∗ Word w (w1 , w2 )
                                         ∗ I∈I2 I(w2 , z2 ) ∗ Zeroes(z2 , y)

          Init w (x, y) ←             ∃z1 ∃z2 . C1P T (x) ∗ I∈I1 I(x)  ∗
                                         ∗ I∈I2 I(x, z1 ) ∗ Tape w (z1 , z2 ) ∗
                                         ∗                   idle
                                           I∈I2 I(z2 , y) ∗ CP T (y) ∗    I∈I1 I(y)     ∗
                def
and let φw = ∃x ∃y . Init w (x, y). Intuitively, φw is a linear sentence which
defines the valid (initial) configurations of the linear system encoding the Post-
Turing machine, where moreover w is written on the tape and the machine head
is pointing at the beginning w. We prove the following two assertions equivalent:
   1. the Post-Turing machine running M terminates on input w
   2. the answer to deadlock (φw , ∆w , βM ) is yes


                                                         16
“1 ⇒ 2”: If the machine terminates then it terminates by visiting finite portions
of the tape to the left and to the right, with respect to the initial placement
of w on the tape. Henceforth, if the linear component-based system is started
with the amount of tape cells needed on both sides, it will run without errors
(that is, neither left or right tape overflow) until termination as well.
“2 ⇒ 1”: First of all, if the linear system reaches a deadlock from its initial
configuration, it means that neither left or right overflow occur (otherwise, the
unary err interactions are enabled and run in an endless loop). Henceforth, the
computation of the linear system involved only the allocated tape components
and followed the execution of the statements in M . Moreover, by construction
of the linear system, the relationship between the control and the tape state
machines ensures that no blocking can occur between them: tape cells are con-
tinuously ready to receive the commands from the control and to execute them,
in order. Therefore, the system stops in a deadlock only if no more commands
are sent, i.e. when the control machine reaches a stop statement and all tape
components are “idle”, that is, no other commands are pending for completion.
    The termination problem of Post-Turing machines being undecidable [11],
it implies that the LinearDeadlock problem is also undecidable. Moreover, we
can use a similar argument to show that the LinearReachability problem is
undecidable as well. Actually, we can restrict without loss of generality to
programs M containing a unique stop statement moreover occurring as the last
statement m in M . Then, for such programs we can prove the equivalence of
the previous assertions to the following one:

   3. the answer to reach(φw , hmi, ∆w , βM ) is yes

that is, the linear system reaches some configuration where a component is in
state m. In fact, by construction, the only component that could reach the
m state is the leftmost control component, and therefore we can map back
any execution of the linear component-based system reaching m in the control
component, to a terminating execution of the Post-Turing machine.


5. Translating CL Specifications into Rewriting Trees

    The inductive interpretation of predicate symbols in the CL logic, by means
of a finite set of definitions, supports the idea of designing systems hierarchically
(top-down). For instance, in §1.1, we specify a ring system first by a chain of
components, with an interaction between the out port of the last to the in
port of the first component (rule 1). Then a chain consists of one component
and an interaction between the out port of that component and the in port of
the first component of a separate chain (rule 2), or of two components (rule
3). Intuitively, one can view these stages of the definition as rewriting steps,
in which a predicate atom is replaced by one of the rules defining it. In this
section, we formalize this idea by introducing rewriting trees, i.e. trees labeled
with rules, that define a partial order in which the rules are applied.



                                         17
    Moreover, the verification method described in §6 uses rewriting trees as
backbones for the encoding of sets of configurations in MSO interpreted over
trees [12]. In particular, the component indices from the set U are going to be
interpreted as nodes of rewriting trees. As will be shown below, this interpre-
tation of logical variables loses no generality, because component indices can
only be compared for equality; their particular nature is of no importance from
the point of view of the verification problems considered. Furthermore, the in-
terpretation of component indices as tree nodes enables the use of a decidable
fragment of MSO, to encode verification conditions.
    The mapping of variables to the nodes of a rewriting tree is uniquely de-
fined by the occurrences of the component atoms in the tree. More precisely,
because all atomic propositions that occur in the rewriting tree are joined by
separating conjunctions, the variables of all component atoms C(x) with the
same component type C must be interpreted as different indices, or else the
formula corresponding to the tree would not be satisfiable. Hence, a rewriting
tree uniquely defines an architecture α over a given signature Σ and, implicitly,
a Petri net N(Σ, α, β), for a given behavior map β (Def. 1).

5.1. Rewriting Trees
    Trees play an important role in the subsequent developments, hence we in-
troduce a few formal definitions, for self-containment reasons. Let κ ≥ 1 be
an integer constant and let [1, κ]∗ denote the set of finite sequences of integers
between 1 and κ, called nodes in the following. We denote the concatenation of
nodes w, u ∈ [1, κ]∗ as w · u or simply wu, when no confusion arises. A set of
nodes T ⊆ [1, κ]∗ is said to be:
   1. prefix-closed if wi ∈ T , for some i ∈ [1, κ], only if w ∈ T , and
   2. complete if wi ∈ T , for some i ∈ [1, κ], only if wj ∈ T , for all j ∈ [1, i − 1].
A κ-ary tree T is a function mapping a complete prefix-closed set of nodes
nodes(T ) into a finite set of labels. The root of T is the empty sequence , the
                                                      def
children of a node w ∈ nodes(T ) are childsT (w) = {wi ∈ nodes(T ) | i ∈ [1, κ]}
and the parent of a node wi ∈ nodes(T ), where i ∈ [1, κ], is w. The leaves of T
                def
are leaves(T ) = {w ∈ nodes(T ) | w · 1 6∈ nodes(T )}. The subtree of T rooted at
                               def                                         def
w is defined by nodes(T ↓w ) = {w0 | ww0 ∈ nodes(T )} and T ↓w (w0 ) = T (ww0 ),
for all w0 ∈ nodes(T ↓w ). A prefix of a tree T is the restriction of T to a complete
prefix-closed subset of nodes(T ). We say that T is finite if nodes(T ) is finite.
    Let ∆ be a fixed SID in the rest of this section. For an arbitrary CL formula
φ, we denote by #pred (φ) the number of occurrences of predicate atoms and
by predi (φ) the i-th predicate atom from φ, in some predefined total ordering
of the symbols in the syntax tree of φ. A formula φ is said to be predicate-
free if #pred (φ) = 0. Without loss of generality, we assume from now on that
#pred (φ) ≤ κ, for each CL formula φ considered in the following. We shall also
simplify our technical life by considering the following assumption:

Assumption 1. For each sentence φ, there exists a rule Aφ () ← φ in ∆, where
Aφ is a predicate symbol of zero arity, not occurring in φ or elsewhere in ∆.


                                          18
This assumption loses no generality because each query in a decision problem
(§4) considers finitely many sentences, for which finitely many rules of the above
form are added to ∆.

Definition 6. Given a CL formula φ, a rewriting tree        for φ is a tree T with la-
bels from ∆, such that T () = A(x1 , . . . , x#(A) ) ← φ , for some predicate sym-      
bol A and, for each w ∈ nodes(T ), such that T (w) = A0 (x1 , . . . , x#(A0 ) ) ← ψ0 ,
the following hold:
   1. for all i ∈ [1, #pred (ψ0 )], if predi (ψ0 ) = Ai (y1i , . . . , y#(A
                                                                        i
                                                                           i)
                                                                              ), then wi ∈
                                                              
       nodes(T ) and T (wi) = Ai (x1 , . . . , x#(Ai ) ) ← ψi is a rule from ∆,
   2. wi 6∈ nodes(T ), for all i > #pred (ψi ).
We denote by T(φ) the set of rewriting trees for φ.

By slight abuse of notation, we write φ[ψ1 /ϕ1 . . . ψn /ϕn ] for the result of replac-
ing each subformula ψi of φ by the formula ϕi , for all i ∈ [1, n]. We associate
each rewriting tree T ∈ T(φ) a characteristic formula F(T ), defined inductively
on the structure of T , as follows:
              
               φ, if nodes(T ) = {}
              
          def
    F(T ) =     φ [A1 (y1 )/F(T ↓1 )[x1 /y1 ] . . . An (yn )/F(T ↓n )[xn /yn ]] ,
              
                 if n = #pred (φ) ≥ 1 and predi (φ) = Ai (yi ), for all i ∈ [1, n]
              

Intuitively, the characteristic formula of a rewriting tree is the predicate-free
formula obtained by replacing each predicate atom occurring in a node of the
tree by the characteristic formula of its corresponding subtree, recursively. In
the process of building a characteristic formula, the free variables of the char-
acteristic formulæ of the subtrees are substituted with the parameters of their
corresponding predicate atoms.

Example 6. Let Σ = ({N, L}, {R, I}, P) be a signature, where P(N) = {req, reply},
P(L) = {reply, in, out}, P(R) = hreq, reply, replyi and P(I) = hout, ini. Con-
sider a behavior map β, such that states β (N) = {q0 , q1 } and states β (L) =
{s0 , s1 , s2 }. The SID below defines tree-shaped architectures, whose leaves are
connected in a token ring:

       Root() ← ∃r∃n1 ∃`1 ∃r1 ∃n2 ∃`2 ∃r2 . Nq0 (r) ∗ R(r, n1 , n2 ) ∗ I(r1 , `2 ) ∗ I(r2 , `1 )
                                             ∗ Node(n1 , `1 , r1 ) ∗ Node(n2 , `2 , r2 ) (7)

 Node(n, `, r) ← ∃n1 ∃r1 ∃n2 ∃`2 . Nq0 (n) ∗ R(n, n1 , n2 ) ∗ I(r1 , `2 )
                                             ∗ Node(n1 , `, r1 ) ∗ Node(n2 , `2 , r)     (8)

 Node(n, `, r) ← Nq0 (n) ∗ R(n, `, r) ∗ Leaf (`) ∗ I(`, r) ∗ Leaf (r)                    (9)

      Leaf (x) ← Ls0 (x)                                                                (10)




                                            19
                                                Root() ← ∃r∃n1 ∃`1 ∃r1 ∃n2 ∃`2 ∃r2 . Nq0 (r) ∗ R(r, n1 , n2 ) ∗ I(r1 , `2 ) ∗ I(r2 , `1 )
                                                                                                              Node(n1 , `1 , r1 ) ∗ Node(n2 , `2 , r2 )



  Node(n, `, r) ← ∃n1 ∃r1 ∃n2 ∃`2 . Nq0 (n) ∗ R(n, n1 , n2 ) ∗ I(r1 , `2 )                            Node(n, `, r) ← ∃n1 ∃r1 ∃n2 ∃`2 . Nq0 (n) ∗ R(n, n1 , n2 ) ∗ I(r1 , `2 )
                                              Node(n1 , `, r1 ) ∗ Node(n2 , `2 , r)                                                                  Node(n1 , `, r1 ) ∗ Node(n2 , `2 , r)



Node(n, `, r) ← Nq0 (n) ∗ R(n, `, r) Node(n, `, r) ← N(n) ∗ R(n, `, r) Node(n, `, r) ← Nq0 (n) ∗ R(n, `, r) Node(n, `, r) ← N(n) ∗ R(n, `, r)
     ∗Leaf (`) ∗ I(`, r) ∗ Leaf (r)                    ∗Leaf (`) ∗ I(`, r) ∗ Leaf (r)                        ∗Leaf (`) ∗ I(`, r) ∗ Leaf (r)                      ∗Leaf (`) ∗ I(`, r) ∗ Leaf (r)



Leaf (x) ← Ls0 (x) Leaf (x) ← Ls0 (x) Leaf (x) ← Ls0 (x)Leaf (x) ← Ls0 (x) Leaf (x) ← Ls0 (x)Leaf (x) ← Ls0 (x) Leaf (x) ← Ls0 (x)Leaf (x) ← Ls0 (x)

                                                                                            (a)


                                                                                          N(r  )                                                                                 Root()

                                                                                                req
                                              reply                                                                                   reply

                                                                         Node(n         
                                                                               1 , l1 , r 1 )                                                                       Node(n        
                                                                                                                                                                          2 , l2 , r2 )
                                                N(n
                                                   1)                                                                                     N(n
                                                                                                                                             2)
                                                      req                                                                                      req

                                 reply                           reply                                                     reply                         reply
                                  Node(n1         1
                                        1 , l1 , r 1 )            N(n1
                                                                                      1
                                                                       Node(n2 , l2 , r1 )1       
                                                                                                                        N(n2
                                                                                                                                           2
                                                                                                                             Node(n1 , l2 , r1 )    2
                                                                                                                                                            N(n2
                                                                                                                                                                                 2
                                                                                                                                                                  Node(n2 , l2 , r2 )  2   
                             N(n1
                                1)                                   2)                                                    1)                                  2)
                                 req                                      req                                               req                                  req

                     reply            reply                      reply            reply                         reply             reply                     reply              reply


              in   L(l
                      1)     out in
                                          1
                                       L(r1 )         out in   L(l1
                                                                  2)     out in
                                                                                      
                                                                                   L(r1 )     out       in   L(l
                                                                                                                2)      out in
                                                                                                                                      2
                                                                                                                                   L(r1 )      out in    L(l2
                                                                                                                                                            2)      out   in
                                                                                                                                                                                   
                                                                                                                                                                                L(r2 ) out




                                                                                            (b)
                                                            Figure 5: Trees with Leaves Linked in a Token Ring


                         Fig. 6(a) shows an unfolding tree for φ = ∃r∃n1 ∃`1 ∃r1 ∃n2 ∃`2 ∃r2 . Nq0 (r) ∗
                    R(r, n1 , n2 ) ∗ I(r1 , `2 ) ∗ I(r2 , `1 ) ∗ Node(n1 , `1 , r1 ) ∗ Node(n2 , `2 , r2 ), with Aφ =
                    Root, and Fig. 6(b) shows a model of the characteristic formula of this unfolding
                    tree. To avoid name clashes, we annotate existentially quantified variables in the
                    characteristic formula with the node of the unfolding tree where they are intro-
                    duced, for instance r , n1 and n2 are introduced at the root, whereas n11 , n12 , `12 , r11
                    (n21 , n22 , `22 , r12 ) occur first at the left (right) child of the root.                     
                       The following result shows that each model of a sentence is the model of the
                    characteristic formula of some rewriting tree for that sentence, that represents
                    the way in which the model is “produced” by unfolding the rules in ∆. In
                    general, such rewriting trees are not unique, as different rewriting trees can
                    have equivalent characteristic formulæ.
                                                                         S
                    Lemma 1. For each CL sentence φ, we have [[φ]] = T ∈T(φ) [[F(T )]].
                    Proof : We prove a slightly more general statement: for each formula φ, each
                    rule A(x1 , . . . , x#(A) ) ← φ from ∆, each configuration (α, m) and each store s:
                                  (α, m) |=s φ                    ⇐⇒              (α, m) |=s F(T ), for some T ∈ T(φ), such
                                                                                  that T () = A(x1 , . . . , x#(A) ) ← φ

                                                                                                      20
“⇒” By induction on the definition of the satisfaction relation |=, considering
the following cases:

   • φ ∈ {emp, Cq (x), I(x1 , . . . , x#(I) )}: we define T by nodes(T ) = {} and
                                                                                          def

           def                              
     T () = A(x1 , . . . , x#(A) ) ← φ . By Def. 6, we have T ∈ T(φ) and
     F(T ) = φ, thus (α, m) |=s F(T ).

                                         ∗
   • φ = ∃y1 . . . ∃yn . φ0 ∗ ki=1 Ai (z1i , . . . , z#(A
                                                        i
                                                            i)
                                                               ), where φ0 is quantifier- and

                             0
                                           s

                                                                  1
                                                                        ∗
     predicate-free: since (α, m) |= ∃y1 . . . ∃yn . φ0 ∗ ki=1 Ai (z1i , . . . , z#(A   i
                                                                                            i)
                                                                                               ),
     there exists a store s that agrees with s over X \ {y1 , . . . , yn } and config-
                                                                                                0
     urations (αi , mi ), such that (α, m) = (α0 , m0 ) • . . . • (αk , mk ), (α0 , m0 ) |=s
                           0
     φ0 and (αi , mi ) |=s Ai (z1i , . . . , z#(A
                                              i
                                                  i)
                                                     ), for all i ∈ [1, k]. For each i ∈ [1, k],
                           0
     since (αi , mi ) |=s Ai (z1i , . . . , z#(A
                                             i
                                                i)
                                                   ), there exists Ai (x1 , . . . , x#(Ai ) ) ← ψi
                                             0
     in ∆, such that (αi , mi ) |=s ψi [x1 /z1i , . . . , x#(Ai ) /z#(A
                                                                    i
                                                                       i)
                                                                          ], by the defini-
                                   def
     tion of |=. Let s0i = s0 ◦ [x1 /z1i , . . . , x#(Ai ) /z#(A
                                                             i
                                                                 i)
                                                                    ] be a store. We have
                    0
     (αi , mi ) |=si ψi and, by the induction hypothesis, there exists a rewrit-      
     ing tree Ti ∈ T(ψi ), such that Ti () = Ai (x1 , . . . , x#(Ai ) ) ← ψi and
                   0                             0
     (αi , mi ) |=si F(Ti ), hence (αi , mi ) |=s F(Ti )[x1 /z1i , . . . , x#(Ai ) /z#(A
                                                                                     i
                                                                                        i)
                                                                                           ].
     We define the rewriting tree T as:
                                 Sk
        – nodes(T ) = {} ∪ i=1 i · nodes(Ti ),
        – T () = A(x1 , . . . , x#(A) ) ← φ,
        – T (iw) = Ti (w), for each i ∈ [1, k] and each w ∈ nodes(Ti ).
     We obtain F(T ) = ∃y1 . . . ∃yn . φ0 ∗           ∗   k               i                     i
                                                          i=1 F(Ti )[x1 /z1 , . . . , x#(Ai ) /z#(Ai ) ],
     leading to (α, m) |=s F(T ).
                                                                                           
”⇐” By induction on the structure of T ∈ T(φ), such that T () = A(x1 , . . . , x#(A) ) ← φ ,
by distinguishing the following cases:
   • nodes(T ) = {}: since T () = A(x1 , . . . , x#(A) ) ← φ , we have F(T ) =
                                                              

      φ, hence (α, m) |=s φ.
   • childsT () = {1, . . . , k}, for some k ≥ 1: assume w.l.o.g. that φ =
     ∃y1 . . . ∃yn . φ0 ∗     k
                                   ∗      i         i
                              i=1 Ai (z1 , . . . , z#(Ai ) ), where φ0 is a quantifier- and
     predicate-free formula. By the definition of characteristic formulæ, we
     have F(T ) = ∃y1 . . . ∃yn . φ0 ∗            ∗   k                   i                   i
                                                      i=1 F(T ↓i )[x1 /z1 , . . . , x#(Ai ) /z#(Ai ) ],
                                                         
     where T (i) = Ai (x1 , . . . , x#(Ai ) ) ← ψi , hence T ↓i ∈ T(ψi ). Since (α, m) |=s
     F(T ), there exists a store s0 that agrees with s over X1 \ {y1 , . . . , yn }
                                                                                            0
     and configurations (α0 , m0 ), . . . , (αk , mk ), such that (α0 , m0 ) |=s φ0 and
                   0
     (αi , mi ) |=s F(T ↓i )[x1 /z1i , . . . , x#(Ai ) /z#(A
                                                          i
                                                              i)
                                                                 ], for all i ∈ [1, m]. Consider
                                                            def
     an arbitrary index i ∈ [1, m] and let s0i = s0 ◦ [x1 /z1i , . . . , x#(Ai ) /z#(A
                                                                                   i
                                                                                      i)
                                                                                         ],
                               0                                                                            0
     hence (αi , mi ) |=si F(T ↓i ). By the inductive hypothesis, we have (αi , mi ) |=si
                              0                                              0
                                                                                                 i
     ψi , hence (αi , mi ) |=si Ai (x1 , . . . , x#(Ai ) ) and (αi , mi ) |=s Ai (z1i , . . . , z#(A i)
                                                                                                        )
     follows. Because the above holds for all i ∈ [1, k], we conclude that
     (α, m) |=s φ.                                                                                 


                                                 21
5.2. Canonical Models
    In the following, we shall equate the universe of indices U with the set [1, κ]∗
of tree nodes, i.e. finite sequences of integers between 1 and κ. This is without
loss of generality, because both sets are infinitely countable and the nature
of indices plays no role in the interpretation of CL formulæ. In this setting,
we define the canonical model (αT , mT ) of the characteristic formula F(T ) of
a rewriting tree T . In order to simplify its definition, we proceed under the
following assumption:

Assumption 2. Each rule of ∆ is of one of the forms:

                  A(x1 ) ← φ, such that φ 6= emp                                                  (I)
     A(x1 , . . . , x#(A) ) ← ∃y1 . . . ∃yn . φ ∗ ψ ∗     ∗   p        i            i
                                                              i=1 Ai (z1 , . . . , z#(Ai ) )     (II)

for some n, m ≥ 0 and p ≥ 1, where:
    • φ ∈ {Cq (x1 ) | C ∈ C, q ∈ states β (C)} ∪ {emp},
    • ψ
      Spis a separating      conjunction of interaction atoms,
    • i=1 {z1i , . . . , z#(A
                          i
                                                                 
                             i)
                                } = {x1 , . . . , x#(A) } \ fv(φ) ∪ {y1 , . . . , yn }, and
    • {z1i , . . . , z#(A
                      i
                         i)
                            } ∩ {z1j , . . . , z#(A
                                                j
                                                   j)
                                                      } = ∅, for all 1 ≤ i < j ≤ p.

The direct consequence of this assumption is that, each variable that occurs in
a characteristic formula of a rewriting tree, occurs in exactly one component
atom, in a rule that labels exactly one node from the rewriting tree. This fact
is proved below:

Lemma 2. Let φ be a CL formula and T ∈ T(φ) be a rewriting tree for φ. For
each variable x, that occurs free or existentially quantified in F(T ), there exists
exactly one node w ∈ nodes(T ) and one component atom Cq (x) in T (w).

Proof : It is sufficient to prove the statement for the case where x occurs in
the label of the root of T . If it is introduced at some node w ∈ nodes(T ) \ {}
by an existential quantifier, the same proof can be done taking T ↓w instead
of T . The proof goes by induction on the structure of T . For the base case
nodes(T ) = {}, the only possibility is that T () is a rule of the form (I) and
the proof is immediate. For the inductive step, let T () be the following rule:

       A(x1 , . . . , x#(A) ) ← ∃y1 . . . ∃yn . φ ∗ ψ ∗     ∗   p        i            i
                                                                i=1 Ai (v1 , . . . , v#(Ai ) )

If φ is of the form Cq (x1 ) and x = x1 , then  is the unique node such that x
occurs in a component atom. Else, x ∈ {x1 , . . . , x#(A) } ∪ {y1 , . . . , yn } \ fv(φ),
thus x ∈ {v1i , . . . , v#(A
                         i
                            i)
                               }, for exactly one i ∈ [1, p], by Assumption 2. In this
case the inductive hypothesis applies, thus x occurs in exactly one component
atom Cq (x) in T (w), for exactly one w ∈ nodes(T ↓i ).                                       
    Note, however, that Assumption 2 is not without loss of generality. For
instance, architectures of the form ∃z1 . . . ∃zk . I(x, z1 ) ∗ Cq (z1 ) ∗ I(z1 , z2 ) ∗ . . . ∗
Cq (zk ) ∗ I(zk , y), having unconnected (loose) interactions, cannot be defined by


                                               22
SIDs that meet the requirement of Assumption 2. On the positive side, all
examples considered in this paper can be written using only rules of this form,
for instance, the definition of the Chain n,t predicates, for constant integers
n, t ≥ 0 (Example 5) or the definition of the Root, Node and Leaf predicates
(Example 6).
     The canonical model of a characteristic formula F(T ) is obtained by instan-
tiating each variable x that occurs free or existentially quantified in F(T ) by the
unique node w ∈ nodes(T ), such that x occurs in a single component atom Cq (x)
                                                                   ∗
in T (w) (Lemma 2). Formally, let φ = ∃y1 . . . ∃yn . ψ ∗ pi=1 Ai (z1i , . . . , z#(A   i
                                                                                             i)
                                                                                                )
be a formula, where ψ is quantifier- and predicate-free,Sp             and   define, for  each
rewriting tree T ∈ T(φ), a store sT : fv(ψ) ∪ i=1 {z1i , . . . , z#(A  i
                                                                            i)
                                                                               } → nodes(T ),
as follows:
              
                              if x occurs in a component atom from ψ
          def
  sT (x) =     i · sT↓i (xj ) if x = zji , for some j ∈ [1, #(Ai )], where
                                T (i) = Ai (x1 , . . . , x#(Ai ) ) ← ϕi , for all i ∈ [1, p]
              

Note that, because the rules of the SID meet the conditions of Assumption
2, the two cases of the definition of sT above are exclusive and, moreover,

                                  
                                                                   ∗
sT (x) is defined for all free variables of the matrix ψ ∗ pi=1 Ai (z1i , . . . , z#(A
                                                                                    i
                                                                                        i)
                                                                                           )
of φ. We extend the store sT to a store sT : fv(η) → nodes(T ) mapping all
variables (free or existentially quantified) that occur in the characteristic formula
F(T ) = ∃z1 . . . ∃zk . η, where η is a quantifier- and predicate-free formula:
               
          def   sT (x)        if x ∈ fv(F(T ))
  sT (x) =                                                                            (11)
                w · sT↓w (x) if x is existentially quantified at w ∈ nodes(T )

In the above definition, we have assumed that all existentially quantified vari-
ables have pairwise distinct names (this is w.l.o.g. as quantified variables can
be α-renamed, if necessary). Note that sT is uniquely defined, for each given
rewriting tree T and induces a unique canonical model, defined below:

Definition 7. The canonical model of a rewriting tree T is the configuration
(αT , mT ), defined as follows:
   • αT (C) = {sT (x) | Cq (x) occurs in η},
                def


   • αT (I) = {hsT (x1 ), . . . , sT (x#(I) )i | I(x1 , . . . , x#(I) ) occurs in η}, and
               def



   • mT = {q[sT (x)] | Cq (x) occurs in η}.
           def




Lemma 3. Given a sentence φ, for each rewriting tree T ∈ T(φ), we have
(αT , mT ) |= F(T ).

Proof : Let F(T ) = ∃x1 . . . ∃xn . η. We prove a more general statement, namely
if φ is a formula, not necessarily a sentence, then (αT , mT ) |=sT η. The proof
goes by induction on the structure of T , distinguishing the cases below:
    • nodes(T ) = {} and T () = (A(x) ← Cq (x)) is a rule of type (I): then
       αT (C) = {sT (x)} = {}, mT = {q[sT (x)]} = {q[]}, αT (C0 ) = ∅, for all
       C0 ∈ C \ {C} and αT (I) = ∅, for all I ∈ I, thus (αT , mT ) |=sT Cq (x).


                                               23
     • nodes(T ) 6= {} and T () = A(x1 , . . . , x#(A) ) ← ∃y1 . . . ∃yn . φ ∗ ψ ∗
        ∗ p          i          i
          i=1 Ai (z1 , . . . , z#(Ai ) ) is a rule of type (II). Let ηi be the matrix of the
       characteristic formula F(T ↓i ), for all i ∈ [1, p]. By the definition of sT ,
       we have sT (x) = i · sT↓i (x), for all x ∈ ηi and i ∈ [1, p]. We define the
       structures (α0 , m0 ), (α1 , m1 ), . . . , (αp , mp ) as follows:
                       def                             def
          – α0 (C) = {sT (x)} = {} and m0 = {q[sT (x)]} = {q[]} if φ = Cq (x1 ),
                                                                       def
             else α0 (C) = ∅ and m0 = ∅ and, moreover, α0 (I) = {hsT (x1 ), . . . , sT (x#(I) )i |
             I(x1 , . . . , x#(I) ) occurs in ψ}, thus we have (α0 , m0 ) |=sT φ ∗ ψ.
                       def                                       def
          – αi (C) = {sT (x) | Cq (x) occurs in ηi }, mi = {hsT (x1 ), . . . , sT (x#(I) )i |
             I(x1 , . . . , x#(I) ) occurs in ηi }, for each i ∈ [1, p]. Since sT (x) = i ·
             sT↓i (x), for all x ∈ ηi and i ∈ [1, p], we have αi (C) = {i · u | u ∈ αT↓i (C)},
             for all C ∈ C, mi = {q[i · u] | q[u] ∈ mT↓i } and αi (I) = {hi · u1 , . . . , i · u#(I) i |
             hu1 , . . . , u#(I) i ∈ αT↓i (I)}, for all I ∈ I. By the inductive hypothesis,
             we have (αT↓i , mT↓i ) |=sT↓i ηi , thus (αi , mi ) |=sT ηi , for all i ∈ [1, p].
       Since the sets of indices of α0 , . . . , αp and m0 , . . . , mp are pairwise dis-
       joint, their composition is defined and, moreover, we have (αT , mT ) =
       (α0 , m0 ) • . . . • (αp , mp ). Consequently, we obtain (αT , mT ) |=sT φ ∗ ψ ∗
        ∗ p          i          i
          i=1 Ai (z1 , . . . , z#(Ai ) ), as required.                                        

 Example 7. Since T is a rewriting tree for a sentence, each variable occurs
 bound in F(T ) and is mapped by the store sT into the unique node of T that
 contains a unique component atom in which that variable occurs:

              sT (r ) =        sT (n1 ) = 1        sT (n2 ) = 2
              sT (n11 ) = 11     sT (n12 ) = 12       sT (n21 ) = 21 sT (n22 ) = 22
              sT (`1 ) = 111    sT (r11 ) = 112      sT (`12 ) = 121 sT (r1 ) = 122
              sT (`2 ) = 211    sT (r12 ) = 212      sT (`22 ) = 221 sT (r2 ) = 222

 The configuration (αT , mT ) corresponding to the rewriting tree T from Fig. 6(a)
 is given below:

αT (N) = {, 1, 2, 11, 12, 21, 22}
αT (L) = {111, 112, 121, 122, 211, 212, 221, 222}
αT (R) = {h, 1, 2i, h1, 11, 12i, h11, 111, 112i, h12, 121, 122i, h21, 211, 212i, h22, 221, 222i}
 αT (I) = {h111, 112i, h112, 121i, h121, 122i, h211, 212i, h212, 221i, h221, 222i, h222, 111i}
   mT = {q0 [], q0 [1], q0 [2], q0 [11], q0 [12], q0 [21], q0 [22], s0 [111], s0 [112], s0 [121], s0 [122],
          s0 [211], s0 [212], s0 [221], s0 [222]}                                                          

 5.3. Symmetry Reduction
     As shown in Lemma 1, each model of a sentence is a model of the character-
 istic formula of some rewriting tree for that sentence. In this section, we prove a
 symmetry property of the models of a characteristic formula corresponding to a
 given rewriting tree, that makes them indistinguishable from the point of view
 of the decision problems considered previously (§4). Let us fix a signature Σ,
 with component types C = {C1 , . . . , CN } and interaction types I = {I1 , . . . , IM },
 and a behavior map β, in the rest of this section.


                                                 24
     Intuitively, two architectures are symmetric if they differ only by a renaming
of indices used to interpret the component and interaction types. For instance,
the architectures α1 and α2 , where α1 (C1 ) = α1 (C2 ) = {1}, α1 (I1 ) = {h1, 1i}
and α2 (C1 ) = {1}, α2 (C2 ) = {2}, α2 (I1 ) = {h1, 2i} have the same shape (as-
suming N = 2 and M = 1). However, this isomorphism cannot be captured by
a global permutation of indices, as it is usually the case4 in the literature [13],
because the sets α1 (C1 ) ∪ α1 (C2 ) and α2 (C1 ) ∪ α2 (C2 ) have different cardinali-
ties. For this reason, our definition of symmetry considers one permutation per
component type.
     Formally, given an architecture α over Σ and a tuple of bijections f =
hf1 , . . . , fN i, where each fi : U → U renames the indices of the component
type Ci , for all i ∈ [1, N ], we define:
              def
(f (α))(Ci ) = fi (α(Ci )), for all i ∈ [1, N ]
             def
  (f (α))(I) = {hfi1 (u1 ), . . . , fi#(I) (u#(I) )i | hu1 , . . . , u#(I) i ∈ α(I),
                                                    ∀k ∈ [1, #(I)] . comp(hP(I)ik ) = Cik }

For a marking m of the Petri net N(Σ, α, β), we define, moreover:
                    def
             f (m) = {q[fi (u)] | q[u] ∈ m, q ∈ states β (Ci ), i ∈ [1, N ]}

Since the sets states β (Ci ), for i ∈ [1, N ], are assumed to be pairwise disjoint, for
each state q there is exactly one component type Ci , such that q ∈ states β (Ci ).

Definition 8. Two configurations are symmetric, denoted (α1 , m1 ) ∼ (α2 , m2 ),
if and only if there exists a tuple of bijections f = hf1 , . . . , fN i, where fi : U → U,
for all i ∈ [1, N ], such that f (α1 ) = α2 and f (m1 ) = m2 .

    The main idea of using symmetries is to prove that models of the same
characteristic formula F(T ) of some rewriting tree T are symmetric and, in
particular, symmetric with the canonical model (αT , mT ). This proof is greatly
simplified by considering only those architectures in which all interactions are
tightly connected to components, in the following sense:

Definition 9. An architecture α is tight if and only if, for each interaction
I[u1 , . . . , u#(I) ] from α and each k ∈ [1, #(I)], we have uk ∈ α(C), where C ∈ C
is the unique component type such that hP(I)ik ∈ P(C).

Note that interactions from an architecture α, having unconnected ports, cannot
fire in the Petri net N(Σ, α, β) (Def. 1), thus having no impact on the answer of
a decision problem (deadlock, reachability). Nevertheless, the CL logic is redun-
dant in this respect, as it allows to specify architectures with loose interactions.
We get rid of this redundancy and assume a syntactic restriction on formulæ,
which guarantees the tightness of models:

   4 Typically, global permutations suffice when only one component type is considered.




                                            25
Definition 10. A profile is a function λ : A → i≥1 Ci , that associates each
                                                         S
predicate symbol A(x1 , . . . , x#(A) ) of non-zero arity with a tuple of component
types of length #(A) ≥ 1. A formula φ is tight for a profile λ if and only if it
contains, for each interaction atom I(x1 , . . . , x#(I) ) and each k ∈ [1, #(I)]:
    • a component atom Cq (xk ), such that hP(I)ik ∈ P(C), or
    • a predicate atom A(y1 , . . . , y#(A) ), such that xk = y` and hP(I)ik ∈
      P(hλ(A)i` ), for some ` ∈ [1, #(A)].
A SID ∆ is tight if and only if there exists a profile λ∆ , such that, for each rule
A(x1 , . . . , x#(A) ) ← φ from ∆, the formula φ is tight for λ∆ and contains, for
each k ∈ [1, #(A)]:
    • a component atom Cq (xk ), such that hλ∆ (A)ik = C, or
    • a predicate atom B(y1 , . . . , y#(A) ), such that xk = y` and hλ∆ (A)ik =
      hλ∆ (B)i` , for some ` ∈ [1, #(B)].
A formula φ, interpreted over a tight SID ∆, is tight if and only if it is tight
for the profile λ∆ .

For instance, one can check that the predicate atoms Chain n,t (x, y) are tight, by
taking the profile λ∆ (Chain n,t ) = hS, Si, for all constants n, t ≥ 0 (Example 5).
Analogously, the predicate atoms Node(n, `, r) are tight, by taking the profile
λ∆ (Node) = hN, L, Li and λ∆ (Leaf ) = hLi (Example 6). The above conditions
guarantee the tightness of architectures described by tight formulæ:

Lemma 4. For each model (α, m) of a tight sentence, the architecture α is tight.

Proof : Let φ be a tight sentence, such that (α, m) |= φ. By Lemma 1, there
exists a rewriting tree T ∈ T(φ), such that (α, m) |= F(T ). Let I(z1 , . . . , z#(I) )
be an interaction atom from F(T ) and k ∈ [1, #(I)]. Also, let w ∈ nodes(T )
be the node where this interaction atom was introduced, such that T (w) =
 A(x1 , . . . , x#(A) ) ← ϕ and I(y1 , . . . , y#(I) ) occurs in ϕ, where y1 , . . . , y#(I) are
substituted by z1 , . . . , z#(A) , respectively, during the construction of F(T ). Since
the SID ∆, that interprets the formula φ, is tight, the rule body ϕ is tight, hence
one of the following holds:
    • there exists a component atom Cq (yk ) in ϕ, such that hP(I)ik = C, or
    • there exists a predicate atom B(ξ1 , . . . , ξ#(B) ) in ϕ, such that yk = ξ` and
      hP(I)ik = hλ∆ (B)i` , where λ∆ is the profile from Def. 10. In this case,
      we apply induction to prove the existence of a component atom Cq (ξk ) in
      F(T ↓i ), such that hP(I)ik = C, where i ∈ [1, #pred (ϕ)] is the child of w
      corresponding to B(ξ1 , . . . , ξ#(B) ) in T .
In both cases, F(T ) contains a component atom Cq (zk ), such that hP(I)ik = C,
hence (α, m) is tight, by Def. 9.                                                             
    The next result proves that each model of a tight sentence is necessarily
symmetric to a canonical model of that sentence:

Lemma 5. Given a tight sentence φ, for each T ∈ T(φ), if (α, m) |= F(T ),
then (α, m) ∼ (αT , mT ).



                                              26
Proof : Since (αT , mT ) |= F(T ), by Lemma 3, it is sufficient to prove that
(α1 , m1 ) ∼ (α2 , m2 ), for any two configurations (αi , mi ), such that (αi , mi ) |=
                     def
F(T ). Let F(T ) = ∃x1 . . . ∃xn . η, where η is a quantifier- and predicate-free
formula. Then (αi , mi ) |= F(T ) if and only if there exist stores si , such that
(αi , mi ) |=si η, for i = 1, 2. We define the sets Uji = {si (x) | Cqj (x) occurs in η}
                                                        def


                              1     2
and the bijections fj : Uj → Uj as fj (s1 (x)) = s2 (x), for all variables x, such
that Cqj (x) occurs in η. These bijections are extended to bijections f j : U → U,
by the following fact:

Fact 1. Given finite sets U1 , U2 ⊆ U, such that f : U1 → U2 is a bijection,
there exists a bijection f : U → U, such that f (u) = f (u), for all u ∈ U1 .
Proof : Since f is a bijection, we have ||U1 || = ||U2 || and, since ||Ui || = ||Ui \ U3−i ||+
||U1 ∩ U2 ||, for i = 1, 2, we obtain ||U1 \ U2 || = ||U2 \ U1 ||. Hence there exists a
bijection f : U → U, such that f (u) = f (u), for all u ∈ U1 , f (U2 \ U1 ) = U1 \ U2
and f (U \ (U1 ∪ U2 )) = f (U \ (U1 ∪ U2 )).                                                
       def
For f = hf 1 , . . . , f N i, we prove the following points:
    • f (α1 ) = α2 : by the definition of f j , we have f j (α1 (Cj )) = α2 (Cj ), for all
      j ∈ [1, N ]. Let I ∈ I and we prove α2 (I) = {hf i1 (u1 ), . . . , f i#(I) (u#(I) )i |
      hu1 , . . . , u#(I) i ∈ α1 (I), ∀k ∈ [1, #(I)] . comp(hP(I)ik ) = Cik }. “⊆” Let
      hu1 , . . . , u#(I) i ∈ α2 (I). Then there exists an interaction atom I(x1 , . . . , x#(I) )
      in η, such that ui = s2 (xi ), for i ∈ [1, #(I)]. Since φ is a tight sentence
      and (α2 , m2 ) |= φ, by Lemma 4, the architecture α2 is tight (Def. 9).
      Then, for each k ∈ [1, #(I)], we have uk ∈ α2 (Cik ), where Cik ∈ C is
      the unique component type such that hP(I)ik ∈ P(Cik ). By the previous
      point, there exists u0k ∈ α1 (Cik ), such that f ik (u0k ) = uk = s2 (xk ). By
      the definition of f ik , we have u0k = s1 (xk ), hence hu01 , . . . , u0#(I) i ∈ α1 (I).
      “⊇” Let hu1 , . . . , u#(I) i ∈ α1 (I), such that comp(hP(I)ik ) = Cik , for all
      k ∈ [1, #(I)]. Then there exists an interaction atom I(x1 , . . . , x#(I) ) in
      η, such that uk = s1 (xk ), for all k ∈ [1, #(I)]. Since φ is a tight sen-
      tence and (α1 , m1 ) |= φ, by Lemma 4, the architecture α1 is tight, thus
      s1 (xk ) = uk ∈ α1 (Cik ). By the definition of f ik , we have s2 (xk ) = f ik (uk ),
      for all k ∈ [1, #(I)], hence hf i1 (u1 ), . . . , f i#(I) (u#(I) )i ∈ α2 (I).
    • f (m1 ) = m2 : we prove m2 = {q[f i (u)] | q[u] ∈ m1 , q ∈ states β (Ci ), i ∈ [1, N ]}.
      “⊆” Let q[u] ∈ m2 . Since (α2 , m2 ) |=s2 η, there exists a component atom
      Cqi (x) in η, such that u = s2 (x) ∈ α2 (Ci ) and Ci is the unique compo-
      nent type, such that q ∈ states β (Ci ). By the definition of f i , we have
      s1 (x) ∈ α1 (Ci ) and s2 (x) = f i (s1 (x)). Moreover, since (α1 , m1 ) |=s1 η,
      we have q[s1 (x)] ∈ m1 . “⊇” Let q[u] ∈ m1 and q ∈ states β (Ci ), for some
      i ∈ [1, N ]. Since (α1 , m1 ) |=s1 η, there exists a component atom Cq (x) in
      η, such that u = s1 (x). By the definition of f i , we have f i (s1 (x)) = s2 (x),
      hence q[f i (u)] = q[s2 (x)] ∈ m2 , since (α2 , m2 ) |=s2 η.                          
    Moreover, the symmetry relation is preserved by the Petri net describing the
operational semantics of the system (Def. 1):



                                             27
Lemma 6. Given a tight architecture α and a behavior β, over a signature
Σ = ({C1 , . . . , CN }, I, P), for any tuple of bijections f = hf1 , . . . , fN i, where
fi : U → U, for all i ∈ [1, N ], the following hold:
   1. m0 ∈ Reach(N(Σ, α, β), m) ⇐⇒ f (m0 ) ∈ Reach(N(Σ, f (α), β), f (m)),
   2. m ∈ Dead (N(Σ, α, β)) ⇐⇒ f (m) ∈ Dead (N(Σ, f (α), β)),
for any two markings m, m0 of the Petri net N(Σ, α, β).

Proof : By Def. 1, let N(Σ, f (α), β) be the Petri net (S f , T f , E f ), where:
              SN
 Sf     =         i=1 {q[u] | q ∈ states(Ci ),            u ∈ (f (α))(Ci )}
              SN
        =         i=1 {q[fi (u)] | q ∈ states(Ci ),              u ∈ α(Ci )}
 Tf
              S
        =         I∈I { (I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i)
                                                                    | hp1 , . . . , p#(I) i = P(I),
                           hu1 , . . . , u#(I) i ∈ (f (α))(I), ht1 , . . . , t#(I) i ∈ Tβ (I),
                           ∀i, j ∈ [1, #(I)]. i 6= j ⇒ ui 6= uj or comp(pi ) 6= comp(pj ) }
              S
        =         I∈I { (I[fk1 (u1 ), . . . , fk#(I) (u#(I) )], ht1 , . . . , t#(I) i)
                                                                                     | hp1 , . . . , p#(I) i = P(I),
                           hCk1 , . . . Ck#(I) i = hcomp(p1 ), . . . , comp(p#(I) )i,
                           hu1 , . . . , u#(I) i ∈ α(I), ht1 , . . . , t#(I) i ∈ Tβ (I),
                           ∀i, j ∈ [1, #(I)]. i 6= j ⇒ fki (ui ) 6= fkj (uj ) or comp(pi ) 6= comp(pj ) }

   Ef
                 S
         =           I∈I { (q[fki (ui )], (I[fk1 (u1 ), . . . , fk#(I) (u#(I) )], ht1 , . . . , t#(I) i)),
                           ((I[fk1 (u1 ), . . . , fk#(I) (u#(I) )], ht1 , . . . , t#(I) i), q 0 [fki (ui )])   |
                                      pi
                            ti = (q −→comp(pi ) q 0 ), i ∈ [1, #(I)] }
We obtain the following equivalence:
                                (I[u1 ,...,u#(I) ],ht1 ,...,t#(I) i)
                           m −−−−−−−−−−−−−−−−−→ m0 in N(Σ, α, β)
                                          ⇐⇒
                      (I[fk1 (u1 ),...,fk#(I) (u#(I) )],ht1 ,...,t#(I) i)
            f (m) −−−−−−−−−−−−−−−−−−−−−−−−−→ f (m0 ) in N(Σ, f (α), β)

where k1 , . . . , k#(I) ∈ [1, N ] are such that Cki = comp(hP(I)ii ), for all i ∈
[1, #(I)]. Point (1) uses this fact inductively, on the length of the firing sequence
leading from m to m0 . For point (2) we use, moreover, that q[u] ∈ m ⇐⇒
                                          •
q[fi (u)] ∈ f (m) and q[u] ∈ (I[u1 , . . . , u#(I) ], ht1 , . . . , t#(I) i) ⇐⇒ q[fi (u)] ∈
•
  (I[fk1 (u1 ), . . . , fk#(I) (u#(I) )], ht1 , . . . , t#(I) i), where Ci is the unique component
type such that q ∈ states β (Ci ).                                                              

Theorem 2. Given a tight sentence φ, interpreted over a SID ∆, a behavior
map β and a tuple of states hq1 , . . . , qk i, the following equivalences hold:

                       deadlock t (φ, ∆, β)                ⇐⇒          deadlock (φ, ∆, β)
            reach t (φ, hq1 , . . . , qk i, ∆, β)          ⇐⇒          reach(φ, hq1 , . . . , qk i, ∆, β)

where deadlock t (φ, ∆, β) and reach t (φ, hq1 , . . . , qk i, ∆, β) are defined below:


                                                            28
    • deadlock t (φ, ∆, β): does there exist rewriting tree T ∈ T(φ), such that
      Reach(N(Σ, αT , β), mT ) ∩ Dead (N(Σ, αT , β)) 6= ∅?
    • reach t (φ, hq1 , . . . , qk i, ∆, β): does there exist a rewriting tree T ∈ T(φ)
      and a configuration (αT , m) ∈ Reach(N(Σ, αT , β), mT ), such that {qi [ui ]
      | i ∈ [1, k]} ⊆ m, with q1 [u1 ], . . . , qk [uk ] pairwise distinct?

Proof : We prove the following points:
   • deadlock t (φ, ∆, β) ⇒ deadlock (φ, ∆, β): assume that deadlock t (φ, ∆, β)
      has a positive answer and let T ∈ T(φ) be a rewriting tree, such that
      Reach(N(Σ, αT , β), mT ) ∩ Dead (N(Σ, αT , β)) 6= ∅, the existence of which
      is stated by deadlock t (φ, ∆, β). By Lemma 3, (αT , mT ) |= F(T ) and, by
      Lemma 1, we obtain (αT , mT ) |= φ, thus deadlock (φ, ∆, β) has a positive
      answer.
   • deadlock (φ, ∆, β) ⇒ deadlock t (φ, ∆, β): assume that deadlock (φ, ∆, β) has
      a positive answer and let (α, m) be a model of φ and m0 be a marking such
      that m0 ∈ Reach(N(Σ, α, β), m) ∩ Dead (N(Σ, α, β)). By Lemma 1, there
      exists a rewriting tree T ∈ T(φ), such that (α, m) |= F(T ). By Lemma
      5, since φ is a tight sentence, we obtain that (α, m) ∼ (αT , mT ) and
      let f = hf1 , . . . , fN i be the bijections from Def. 8, such that (αT , mT ) =
      (f (α), f (m)). By Lemma 6, we obtain that f (m0 ) ∈ Reach(N(Σ, f (α), β), f (m))∩
      Dead (N(Σ, f (α), β)), thus deadlock t (φ, ∆, β) has a positive answer.
   • reach t (φ, hq1 , . . . , qk i, ∆, β) ⇒ reach(φ, hq1 , . . . , qk i, ∆, β): assume that
      reach t (φ, hq1 , . . . , qk i, ∆, β) has a positive answer and let T ∈ T(φ) be a
      rewriting tree and m be a marking of N(Σ, αT , β), such that (αT , m) ∈
      Reach(N(Σ, αT , β), mT ) and {qi [ui ] | i ∈ [1, k]} ⊆ m, where q1 [u1 ], . . . , qk [uk ]
      are pairwise distinct places. By Lemma 3, (αT , mT ) |= F(T ) and, by
      Lemma 1, we obtain (αT , mT ) |= φ, thus reach(φ, hq1 , . . . , qk i, ∆, β) has a
      positive answer.
   • reach(φ, hq1 , . . . , qk i, ∆, β) ⇒ reach t (φ, hq1 , . . . , qk i, ∆, β): assume that
      reach(φ, hq1 , . . . , qk i, ∆, β) has a positive answer and let (α, m) be a model
      of φ and m0 ∈ Reach(N(Σ, α, β), m) be a marking, such that {qi [ui ] | i ∈ [1, k]} ⊆
      m0 , where q1 [u1 ], . . . , qk [uk ] are pairwise distinct places of N(Σ, α, β). By
      Lemma 1, there exists a rewriting tree T ∈ T(φ), such that (α, m) |=
      F(T ). By Lemma 5, since φ is a tight sentence, we obtain that (α, m) ∼
      (αT , mT ) and let f = hf1 , . . . , fN i be the bijections from Def. 8, such
      that (αT , mT ) = (f (α), f (m)). By Lemma 6, we obtain that f (m0 ) ∈
      Reach(N(Σ, f (α), β), f (m)). Moreover, if C`i is the unique component
      type, such that qi ∈ states β (Cki ), for all i ∈ [1, k], since {qi [ui ] | i ∈ [1, k]} ⊆
      m0 , we obtain {qi [f`i (ui )] | i ∈ [1, k]} ⊆ f (m0 ) and reach t (φ, hq1 , . . . , qk i, ∆, β)
      has a positive answer.                                                                      


6. Parametric Verification using Structural Invariants

   In this section we present a sound (but necessarily incomplete) method to
address practical instances of the (undecidable) decision problems of deadlock


                                              29
and reachability (Theorem 1). The method proceeds by synthesizing a sufficient
verification condition as a formula in a decidable fragment of MSO, interpreted
over trees of bounded arity κ, with second-order set variables ranging over finite
sets. This logic is known as the Weak Second-order calculus of κ Successors
(WSκS). Well-known automata-theoretic decision procedures exist for WSκS
[12] and we rely on optimized provers [14] to check the verification conditions.
    During the unfolding of the predicate symbols, according to the structure
of a rewriting tree T , an existentially quantified variable introduced by a rule
might be renamed several times (the renaming occurs when replacing a predicate
atom A(y1 , . . . , y#(A) ) with one of its definitions ϕ[x1 /y1 . . . x#(A) /y#(A) ], for
some rule A(x1 , . . . , x#(A) ) ← ϕ from the SID) before it is instantiated by
a component atom Cq (x), that occurs in some node w ∈ nodes(T ). Due to
Assumption 2 on the syntax of the rules in the SID, this node is unique and the
canonical store sT maps the variable to that node, i.e. sT (x) = w. In order to
determine this value, we must track x along the path in the rewriting tree that
leads from the node where it was introduced (by an existential quantifier, or the
root of the tree if the variable is a top-level parameter) to the node where the
component atom Cq (x) occurs.

Example 8. Let us consider the rewriting tree T depicted in Fig. 6(a). The
variable `1 introduced by an existential quantifier at the root of the tree replaces
the ` parameter of the rule that labels the left successor of the root, i.e. the node
1, that replaces the ` parameter of the label of the node 11, which finally replaces
the x parameter of the label of the node 111, that contains a component atom
Leaf s0 (x). Hence, the value of `1 in the canonical store is sT (`1 ) = 111.    

    Tracking variables is done by path automata that traverse the tree down-
wards, following the substitutions of a particular variable. A path automaton
is then transformed into an equivalent WSκS path formula, that defines the set
of trees over which the automaton has an accepting run. The path formula is
used to define a flow formula that describes the pre- and post-sets for each tran-
sition of the Petri net N(Σ, αT , β) corresponding to the canonical architecture
αT , defined by the rewriting tree T , and the given behavior map β. Moreover,
path formulæ allow to define WSκS formulæ describing the initial and final
configurations of the system.
    In particular, the flow formula is used to derive invariants (i.e. over-approxima-
tions of the set of reachable configurations) directly from the structure of the
Petri net N(Σ, αT , β). These invariants are defined by the sets of places of
N(Σ, αT , β) that do not lose (trap invariants) or generate extra tokens (mutex
invariants), respectively. All verification conditions for the problems considered
in this paper boil down to checking the satisfiability of a WSκS formula.

6.1. Weak Second Order Calculus of κ Successors
    We define the logic WSκS, which is a fragment of MSO interpreted over a
finite prefix of an infinite κ-ary tree. As a remainder, the prefix of a tree T is
the restriction of T to a prefix-closed and complete subset of nodes(T ) (§5.1).


                                           30
   Let X2 = {X, Y, Z, . . .} be a countably infinite set of second-order variables,
ranging over subsets of [1, κ]∗ . The formulæ of WSκS are defined inductively
by the following syntax:

          τ   ::=    | x | τ.i                                           terms
          ξ   ::=   τ = τ | X(τ ) | ξ ∧ ξ | ¬ξ | ∃x . ξ | ∃X . ξ       formulæ
                                                                                 def
where x ∈ X1 , X ∈ X2 and i ∈ [1, κ]. As usual, we write x 6= y = ¬x = y,
         def                      def                 def
ξ1 ∨ ξ2 = ¬(¬ξ1 ∧ ¬ξ2 ), ξ1 → ξ2 = ¬ξ1 ∨ ξ2 , ξ1 ↔ ξ2 = (ξ1 → ξ2 ) ∧ (ξ2 → ξ1 ),
       def                    def
∀x . ξ = ¬∃x . ¬ξ and ∀X . ξ = ¬∃X . ¬ξ. For a constant n ∈ N, we define:
                                                n
                                                _
      X = {y1 , . . . , yn } ⇐⇒ ∀x . X(x) ↔           x = yi                           (12)
                                                i=1
                                                 ^                    n
                                                                      ^
                ||X|| ≥ n ⇐⇒ ∃y1 . . . ∃yn .             yi 6= yj ∧         X(yi )     (13)
                                               1≤i<j≤n                i=1

                ||X|| = n ⇐⇒ ||X|| ≥ n ∧ ¬||X|| ≥ n + 1                                (14)

    The variables of a WSκS formula are interpreted by a store ν : X1 ∪ X2 →
                ∗
[1, κ]∗ ∪ 2[1,κ] , such that ν(x) ∈ [1, κ]∗ , for each x ∈ X1 and ν(X) ⊆ [1, κ]∗ is
a finite set, for each X ∈ X2 . The terms of WSκS are interpreted inductively,
         def              def
as ν() =  and ν(τ.i) = ν(τ ) · i. We denote by |=νwsks ξ the fact that the WSκS
formula ξ is valid for the valuation ν. This relation defined below, by induction
on the structure of the formulæ:
        |=νwsks τ1 = τ2   ⇐⇒    ν(τ1 ) = ν(τ2 )
        |=νwsks X(τ )     ⇐⇒    ν(τ ) ∈ ν(X)
        |=νwsks ξ1 ∧ ξ2   ⇐⇒    |=νwsks ξ1 and |=νwsks ξ2
        |=νwsks ¬ξ        ⇐⇒    not |=νwsks ξ
                                   ν[x←w]
        |=νwsks ∃x . ξ    ⇐⇒    |=wsks      ξ, for some node w ∈ [1, κ]∗
                                   ν[X←S]
        |=νwsks ∃X . ξ    ⇐⇒    |=wsks      ξ, for some finite set S ⊆ [1, κ]∗

A WSκS formula ξ is satisfiable if and only if there exists a store ν, such that
|=νwsks ξ. Such a store is said to be a model of ξ. Note that, because we have
assumed the successor functions .i to be total, for all i ∈ [1, κ], formulæ defining
infinite sets, such as e.g. ∀x . X(x) → X(x.1), are unsatisfiable, under the
interpretation of second-order variables as finite sets.

6.2. Rewriting Trees and Configurations
    We begin by building a WSκS formula that describes an infinite κ-ary tree,
whose finite prefix is a rewriting tree T ∈ T(φ), for a CL formula φ. Let
∆ = {ρ1 , . . . , ρP } be a fixed SID in the following, such that ρ1 is the rule that
labels the root of T , by convention. We use a designated tuple of second order
variables R = hR1 , . . . , RP i, where each variable Ri is interpreted as the set of
tree nodes labeled with the rule ρi in some rewriting tree, for all i ∈ [1, P ]. With
this convention, the RewrTree ∆ (R) formula (Fig. 6) defines rewriting trees:


                                          31
                        def
                                ^                                     
    RewrTree ∆ (R) = ∀x .            ¬Ri (x) ∨ ¬Rj (x) ∧ R1 (x) ↔ x =  ∧                   (15)
                              1≤i<j≤P
                                                     P ^
                                                     ^ κ                    P
                                                                            _
                                            ∀x .              Ri (x.`) →         Rj (x) ∧   (16)
                                                    i=1 `=1                j=1
                                      #pred (ϕ)
                          ^             ^                            _
          ∀x .                                    Ri (x) →                    R` (x.j) ∧    (17)
             i:ρi =(A(x1 ,...,x#(A) )←ϕ) j=1                          0
                                                       j:predj (ϕ)=A (y1 ,...,y#(A0 ) )
                                                       `:ρ` =(A0 (x1 ,...,x#(A0 ) )←ψ )

                                ^                     κ
                                                      ^                    P
                                                                           ^
                 ∀x .                                         Ri (x) →          ¬R` (x.j)   (18)
                    i:ρi =(A(x1 ,...,x#(A) )←ϕ) j=#pred (ϕ)+1             `=1

                                 Figure 6: Rewriting Trees


   • line (15) states that the sets that interpret the second-order variables R
     are pairwise disjoint and that R1 is a singleton containing the root of the
     rewriting tree,

   • line (16) states that the union of the sets R is prefix-closed, i.e. the par-
     ent of each node from the interpretation of a variable Ri belongs to the
     interpretation of some variable Rj , for i, j ∈ [1, P ],
   • lines (17) and (18) encode the conditions 1 and 2 of Def. 6, respectively, i.e.
     for that every predicate atom A0 (y1 , . . . , y#(A0 ) ) from a rule that labels a
     node w in the rewriting tree there is exactly one child of that node, labeled
     with a rule A0 (x1 , . . . , x#(A0 ) ) ← ψ and w has no other children.
It is not very hard to show that, for each model ν of RewrTree ∆ (R) there exists
                                                                                SP
a unique rewriting tree, denoted by TνR , such that nodes(TνR ) = i=1 ν(Ri )
and TνR (w) = ρi ⇐⇒ w ∈ ν(Ri ), for all i ∈ [1, P ] and w ∈ nodes(TνR ).
     As discussed in §5, a rewriting tree T defines a canonical configuration
(αT , mT ), where αT is the architecture consisting of the components and inter-
actions corresponding to the atoms of F(T ) and mT is a marking of the Petri
net N(Σ, αT , β), for a given signature Σ = ({C1 , . . . , CN }, {I1 , . . . , IM }, P) and
behavior map β. In the rest of this section, we consider Σ and β to be fixed
and recall that Qβ denotes the finite set of states used to describe the behaviors
β(C1 ), . . . , β(CN ).
     Our next concern is defining the precise markings of N(Σ, αT , β) (Def. 2) by
a WSκS formula. We define sets of places of N(Σ, αT , β) by means of a tuple of
                           def
second-order variables X = hXq | q ∈ Qβ i. Any valuation ν of the variables X
                                    def
corresponds to a set of places σνX = {q[u] | u ∈ ν(Xq )}. When needed, we shall
                                        def                     def
use distinct copies of X, such as X0 = hXq0 | q ∈ Qβ i, Y = hYq | q ∈ Qβ i and
   def
Z = hZq | q ∈ Qβ i. The WSκS formula below defines the precise markings of a


                                               32
Petri net N(Σ, αT , β), assuming that T is the rewriting tree corresponding to
some model of RewrTree ∆ (R):

                               N 
                               ^             ^
                      def                                                    
           m(X, R) = ∀x .                                  ¬Xq (x) ∨ ¬Xq0 (x) ∧       (19)
                               i=1   q6=q 0 ∈states   β (Ci )
                                             _                      _            
                                                        Xq (x) ↔           Rj (x)     (20)
                                      q∈states β (Ci )          ρj ∈inst(Ci )


Intuitively, line (19) above states that a component of type Ci may not be in
two different states from states β (Ci ), and line (20) states that the index of a
component of type Ci must be a node of the rewriting tree labeled with a rule
in which a component atom of the form Cqi (x) occurs (see Assumption 2 on the
syntax of the rules labeling a rewriting tree). We write inst(C) for the subset of
∆ consisting of those rules that contain a component atom of the form Cq (x).
The correctness of the encoding is stated and proved below:

Lemma 7. For any model ν of RewrTree ∆ (R)∧m(X, R), the set σνX is a precise
marking of the Petri net N(Σ, αTνR , β).

Proof : Let C ∈ C be a component type and u ∈ αTνR (C) be an index. We prove
that ||σνX ∩ {q[u] | q ∈ states β (C)}|| = 1, by proving the following points:
   • σνX ∩ {q[u] | q ∈ states β (C)} = 6 ∅: since |=νwsks RewrTree ∆ (R), we have that
                                                            SP
       Tν is a rewriting tree, such that nodes(TνR ) = i=1 ν(Ri ) and ν(Ri ) is the
          R

       set of nodes of TνR that are labeled with the rule ρi , for all i ∈ [1, P ]. Since
       u ∈ αTνR (C) ⊆ nodes(TνR ), there exists a rule ρi , such that C ∈ inst(ρi )
       and u ∈ ν(Ri ), hence by line (20), we have u ∈ ν(Xq ), i.e. q[u] ∈ σνX , for
       some q ∈ states β (C). Consequently, q[u] ∈ σνX ∩ {q[u] | q ∈ states β (C)}.
   • ||σνX ∩ {q[u] | q ∈ states β (C)}|| < 2: suppose that q[u], q 0 [u] ∈ σνX , for q 6=
       q 0 ∈ states β (C). Hence u ∈ ν(Xq ) ∩ ν(Xq0 ), which contradicts line (19)
       and the fact that |=νwsks m(X, R).                                               

6.3. Path Automata
    The next step in building WSκS verification conditions that are sufficient for
proving deadlock freedom and unreachability of several control states at once
(§4) is tracking the variables that occur in a rule labeling a node of a rewriting
tree T , down to the component atoms which set their values, in the canonical
architecture αT . These values are used to define the interactions of αT and, in
particular, to encode the pre-set (• t) and post-set (t• ) of a transition (t) from
the Petri net N(Σ, αT , β), by a flow formula, described next (§6.4).
    As briefly mentioned (see Example 8) a variable “traverses” the rewriting
tree of a given formula downwards, while replacing the formal parameters of
the rule labeling the child. This traversal is described by a special type of
tree automaton, that walks down the tree, following the identity of the tracked
variable. These automata are a restricted version of tree walking automata [15].


                                            33
                 def
                           ^                                _                           _
  ∆A (x, y, Y) =                      ∀z. ¬Yi (z) ∨ ¬Yj (z) ∧  Yi (x) ∧                         Yj (y)   (21)
                       1≤i6=j≤L                                   si ∈I                 sj ∈F
                           L
                           ^
                       ∧         ∀z . z 6= y ∧ Yi (z) →
                                 _                  _
                           i=1
                                                        ∃z 0 . z 0 .d = z ∧ Yj (z 0 )
                                                                                     
                                      Yj (z.d) ∨                                                         (22)
                                 d                      d
                            j:si −
                                 → sj              j:si −
                                                        → sj
                           L
                           ^
                       ∧          ∀z . z 6= x ∧ Yj (z) →
                           j=1
                                 _                                        _
                                      ∃z 0 . z 0 .d = z ∧ Yi (z 0 ) ∨
                                                                                            
                                                                                    Yi (z.d)             (23)
                                  d                                         d
                            i:si −
                                 → sj                                   i:si −
                                                                             → sj

              Figure 7: Definition of the Path Automaton formula ∆A (x, y, Y)



    A path in a tree T is a sequence n1 , . . . , n` ∈ nodes(T ), such that ni+1 is a
child of ni , for all i ∈ [1, ` − 1]. If m is a descendant of n, we denote by π(n, m)
the unique path starting in n and ending in m. Note that π(n, m) is determined
by n and the sequence of directions d1 , . . . , dp ∈ [1, κ], such that m = n·d1 ·. . .·dp .
A path automaton is a tuple A = (S, I, F, δ), where S is a set of states, I, F ⊆ S
are the sets of initial and final states, respectively, and δ ⊆ S × [1, κ] × S is a
                           d
                     → s0 , where s, s0 ∈ S are states and d ∈ [1, κ] is a direction.
set of transitions s −
A run of A over the path π(n, m), where m = n · d1 · . . . · dp , is a sequence of
                                                             i    d
states s1 , . . . , sp+1 ∈ S, such that s1 ∈ I and si −→        si+1 , for all i ∈ [1, p]. The
run is accepting if and ony if sp+1 ∈ F . The language L(A) of A is the set of
paths in T over which A has an accepting run.
    A path automaton A = ({s1 , . . . , sL }, I, F, δ) corresponds, in the sense of
Lemma 8 below, to the formula in Fig. 7, which is, moreover, built directly
from the syntactic description of A. Here Y = hY1 , . . . , YL i are second order
variables interpreted as the sets of tree nodes labeled by the automaton with the
states s1 , . . . , sL , respectively. Intuitively, the first three conjuncts of the above
formula (line 21) encode the facts that Y are disjoint (no tree node is labeled by
more than one state during the run) and that the run starts in an initial state
with node x and ends in a final state with node y. The fourth conjunct (line 22)
states that, for every non-final node on the path, if the automaton visits that
                                                                                          d
node by state si , then the node has a d-child visited by state sj , where si −           → sj
is a transition of the automaton. The fifth conjunct (line 23) is the reversed flow
condition on the path, needed to ensure that the sets Y do not contain useless
nodes, being thus symmetric to the fourth. The following result stems from the
classical automata-logic connection (see [16, §2.10] for a textbook presentation):

Lemma 8. Given nodes n, m ∈ [1, κ]∗ and directions d1 , . . . , dp ∈ [1, κ] such
that m = n · d1 · . . . · dp , for each valuation ν, such that ν(x) = n and ν(y) = m,


                                                     34
                                    1                       2

              `       1                                                    2        r
          s71                 s`8                                     sr
                                                                       8           s71


                  1       1                                       2            2


                                        1               2
                              s`9                 sn
                                                   10                 sr
                                                                       9




  Figure 8: Path Automata Recognizing the Paths to Component Atoms from Example 6


we have d1 . . . dp ∈ L(A) ⇐⇒ |=νwsks ∃Y . ∆A (x, y, Y) .

    Our purpose is to infer, directly from the syntax of the rules in ∆, path
automata that recognize the path between the node where a variable is intro-
duced (either as a formal parameter of a rule or by an existential quantifier)
and the node where the variable is instantiated, in each given rewriting tree.
Formally, for each rule ρ = (A(x1 , . . . , x#A ) ← ∃y1 . . . ∃ym . ψ), such that ψ
is a quantifie-free formula, and each variable x ∈ fv(ψ), we consider the path
automaton Axρ = (S, I, F, δ), where:

   • S = {szρ0 | ρ0 = (A0 (x1 , . . . , x#A0 ) ← ∃y1 . . . ∃ym . φ) , φ is q.f., z ∈ fv(φ)};
        def


     the intuition is that the automaton visits the state szρ0 while tracking vari-
     able z in the body of the rule ρ0 , that labels the node of the rewriting tree
     which is currently visited by the automaton,

   • the initial and final states are I = {sxρ } and F = {szρ0 | ρ0 = A0 (x1 , . . . , x#A0 )
                                            def                 def

                                    
     ← ∃y1 . . . ∃ym . Cq (z) ∗ φ , φ is q.f., C ∈ C, q ∈ states β (C)}; the automa-
     ton starts to track x in ρ and moves down in the rewriting tree, finally
     tracking a variable z that occurs in a component atom in ρ0 ,
                            y d       x
   • the transitions are sρj −
                                                                                      
                               → sρ0j , for all rules ρ = A(x1 , . . . , x#(A) ) ← ϕ and
     ρ0 = A0 (x1 , . . . , x#(A0 ) ) ← ϕ0 from ∆, all directions d ∈ [1, #pred (ϕ)],
                                         

     such that predd (ϕ) = A0 (y1 , . . . , y#(A0 ) ), and all j ∈ [1, #(A0 )]; if ρ labels
     the parent of the node labeled by ρ0 in the rewriting tree, the automaton
     moves down one step, from tracking yj in ρ to tracking xj in ρ0 .

Example 9. The path automata recognizing the paths to component atoms, for
the variables `1 and r1 in the rewriting tree from Example 6 are depicted in
Fig. 8. The initial states are s`71 and sr71 , respectively, and the final state is sn10
for both automata. The rule labels are the ones from Example 6.                       

    The lemma below shows that these automata recognize the set of paths
corresponding to the recursive substitutions of a given variable down to the
node where it occurs in a component atom, in all rewriting trees built using the
rules from the given SID:



                                                  35
                                                                    
Lemma 9. Given a rule ρ = A(x1 , . . . , x#(A) ) ← ∃y1 . . . ∃ym . φ , such that
φ is a quantifier-free formula, and a variable x ∈ fv(φ), for each sequence w ∈
[1, κ]∗ , the following are equivalent:
    1. there exists a rewriting tree T and nodes n, m ∈ nodes(T ), such that
       T (n) = ρ, m = n · w and sT (x) = m (see 11 for the definition of sT ).
    2. w ∈ L(Axρ ).

Proof :       (1) ⇒ (2) By the definition of sT , we have sT (x) = sT↓n (x) and
 
sT↓n (x) = m if there exist:
    • a sequence of nodes n = n1 , n2 , . . . , np = m ∈ nodes(T ), such that ni+1 =
       ni · di , for some di ∈ [1, κ], for all i ∈ [1, p − 1],
    • a sequence of variables x = z1 , . . . , zp ∈ X1 , such that zi replaces zi+1 in
       the construction of the characteristic formula F(T ), for all i ∈ [1, p − 1],
       and occurs in a component atom from T (m).
By the definition of rewriting trees, each          node ni is labeled by a rule ρi =
 Ai (x1 , . . . , x#(Ai ) ) ← ∃y1 . . . ∃ym . φi , where φi is quantifier-free, and there
exists j ∈ [1, #(Ai )] such that zi occurs on the j-th position in preddi (φi ) and
zi+1 occurs j-th within the head Ai+1 (x1 , . . . , x#(Ai+1 ) ) of ρi+1 . By the defini-
                                             d      z
tion of Axρ , there exist transitions szρii −→
                                             i
                                               sρi+1
                                                 i+1 , for all i ∈ [1, p − 1]. Moreover,
                   z
sxρ = szρ11 and sρpp are initial state and final states of Axρ , respectively. Since
m = n · d1 . . . dp = n · w, we obtain that w = d1 . . . dp ∈ L(Axρ ).
                                                                           d    z
(2) ⇒ (1) Let w = d1 . . . dp , where d1 , . . . , dp ∈ [1, κ], and szρii −→
                                                                           i
                                                                              sρi+1
                                                                                 i+1 , for all
                                   x                 z1     x                              z
i ∈ [1, p − 1], be transitions of Aρ , such that sρ1 = sρ is the initial state and sρpp
                                                                             def
is a final state of Axρ . Then, by the definition of Axρ , the nodes wi = n · d1 . . . di
                            def                               
are labeled by rules ρi = Ai (x1 , . . . , x#(Ai ) ) ← ϕi , such that zi occurs in
preddi (ϕi ) on the same position as zi+1 , which occurs in Ai (x1 , . . . , x#(Ai+1 ) ).
Then, there exists a rewriting tree T and nodes n, m ∈ nodes(T ), such that
m = n · d1 . . . do and Axρ has an accepting run over d1 . . . dp . By the definition
of sT , we have sT (x) = sT↓n (x) = m.                                                     
    The path automata Azρ are used to define the Path zρ (x, y, R) formulæ below:

 Path zρ (x, y, R) = ∃Y . ∆Azρ (x, y, Y) ∧ Υ(Y, R)
                     def

                   def V                               V                  z
        Υ(Y, R) =        i:ρi =(A0 (x1 ,...,x 0 )←ϕ0 )
                                            #(A )        z∈fv(ϕ0 ) ∀x . Yρi (x) → Ri (x)


The formula Υ(Y, R) above states that all nodes labeled with a state qρzi during
the run must be also labeled with ρi in the rewriting tree given as input to the
path automaton. Here we denote by Yρzi the second-order variable corresponding
to the state qρzi in a path automaton Axρ . Intuitively, the formula Path zρ (x, y, R)
states that, in each rewriting tree defined by a model ν of the RewrTree ∆ (R)
formula, there exists a path from ν(x) to ν(y), where ν(x) is a node labeled with
ρ, in which z occurs free or existentially quantified, and y is the node where a
variable necessarily equal to z occurs in a component atom.




                                             36
                                           P
                                           _                _
                 Φ(X, X0 , R) =                                     Ψ`,I(x1 ,...,x#(I) ) (X, X0 , R)
                                     def
                                                                                                          (24)
                                           `=1 I(x1 ,...,x#(I) )∈inter (ρ` )

                                                                               #(I)
                                                                               ^
 Ψ`,I(x1 ,...,x#(I) ) (X, X0 , R) = ∃y0 . . . ∃y#(I) . R` (y0 ) ∧                  Path xρ`i (y0 , yi , R)∧ (25)
                                     def


                                                                               i=1
              _              ^                                                        pi
                                     Xq = {yi | i ∈ [1, #(I)], τi = (qi −→ qi0 ), qi = q}∧ (26)
      hτ1 ,...,τ#(I) i∈Tβ (I) q∈Qβ
                                                                    pi
                               Xq0 = {yi | i ∈ [1, #(I)], τi = (qi −→ qi0 ), qi0 = q} ∧ (27)
                                                                                     
             ^                                                         
                       yi 6= yj ∨ comp(hP(I)ii ) = comp(hP(I)ij )                       (28)
       1≤i<j≤#(I)

                                       Figure 9: The Flow Formula


6.4. Flow Formulæ
    At this point, we introduce a WSκS formula Φ(X, X0 , R) that defines the
structure of transitions in the Petri net N(Σ, αTνR , β), where ν is a model of
RewrTree ∆ (R). By “structure” here we mean that ν(X) and ν(X0 ) encode the
pre- and post-sets of some transition in N(Σ, αTνR , β), as explained in §6.2.
    Fig. 9 shows the flow formula of a given SID, consisting of the rules ρ1 , . . . , ρP .
We denote by inter (ρ) the set of interaction atoms that occur in the body
of a rule ρ. Essentially, the formula (24) is split into a disjunction of for-
mulæ Ψ`,I(x1 ,...,x#(I) ) , one for each rule ρ` ∈ ∆ and each interaction atom
I(x1 , . . . , x#(I) ) that occurs in the body of ρ` . To understand the Ψ`,I(x1 ,...,x#(I) )
formulæ, recall that each of the variables xi is mapped to the (unique) node of
the rewriting tree containing an instance atom Cq (x), such that xi replaces x in
the characterizing formula of the rewriting tree TνR , provided that ν is a model
of RewrTree ∆ (R). In order to find this node, we track the variable xi from the
node labeled by the rule ρ, to the node where this instance atom occurs. This
is done by the Path xρ`i (y0 , yi , R) formula (25), that holds whenever y0 and yi are
respectively mapped to the source and the destination of a path from a node
ν(y0 ) ∈ nodes(TνR ), with label ρ` to a node ν(yi ) ∈ nodes(TνR ), such that the
component atom that gives the value of xi 5 occurs in TνR (ν(yi )). Hence, xi is
interpreted as ν(yi ) in the canonical model of the characteristic formula of TνR .
    The correctness of the encoding is formalized and proved by the following:

Lemma 10. Given a model ν of RewrTree ∆ (R), we have |=νwsks Φ(X, X0 , R) if
                             0
and only if σνX = • t and σνX = t• , for some transition t of N(Σ, αTνR , β).

Proof : “⇒” If |=νwsks Φ(X, X0 , R) then there exists a rule ρ` ∈ ∆ = {ρ1 , . . . , ρN }
and I(x1 , . . . , x#(I) ) ∈ inter (ρ` ), such that |=νwsks Ψ`,I(x1 ,...,x#(I) ) (X, X0 , R). Then,


                             TνR , see §5.2 for its definition.
   5 In the canonical store s




                                                         37
there exist nodes w0 , . . . , wn ∈ nodes(TνR ), such that ν(yi ) = wi , for all i ∈ [0, n]
                                                                      0
and let ν 0 = ν[y0 ← w0 , . . . , yn ← wn ]. Since, moreover, |=νwsks R` (y0 ), we ob-
             R
tain that Tν (w0 ) = ρ` , hence the variables x1 , . . . , x#(I) occur in the body of
the rule ρ` and are assigned to the unique nodes w10 , . . . , w#(I)0
                                                                          ∈ nodes(TνR ),
                                                                                              0
for which π(w0 , wi0 ) ∈ L(Axρ`i ), for all i ∈ [1, #(I)], by Lemma 9. Since |=νwsks
Path xρ`i (y0 , yi , R), by Lemma 8, we obtain π(w0 , wi ) ∈ L(Axρ`i ), thus wi = wi0 , for
all i ∈ [1, #(I)], by the uniqueness of these nodes. Let hτ1 , . . . , τ#(I) i be a tuple of
                                                           0
transitions from Tβ (I) synchronizing by I. Since |=νwsks Ψ`,I(x1 ,...,x#(I) ) (X, X0 , R),
we have wi 6= wj , for each 1 ≤ i < j ≤ #(I), such that comp(hP(I)ii ) =
comp(hP(I)ij ). By Def. 1, we have that t = (I[w1 , . . . , w#(I) ], hτ1 , . . . , τ#(I) i) is
a transition of N(Σ, αTνR , β) and, moreover, • t = {q1 , . . . , q#(I) } = σνX and t• =
                        0               0                                        pi
{q10 , . . . , q#(I)
                0
                     } = σνX , because |=νwsks Xq = {yi | i ∈ [1, #(I)], τi = (qi −→ qi0 ), qi = q}
         0                                         pi
and |=νwsks Xq0 = {yi | i ∈ [1, #(I)], τi = (qi −→ qi0 ), qi0 = q}, respectively.

“⇐” Let t = (I[w1 , . . . , w#(I) ], hτ1 , . . . , τ#(I) i) be a transition of N(Σ, αTνR , β),
                    hP(I)ii
where τi = qi −−−−→ qi0 is a transition of β(comp(hP(I)ii )), for each i ∈
[1, #(I)]. Then there exists a node w0 ∈ nodes(TνR ) and an interaction atom
I(x1 , . . . , x#(I) ) in TνR (w0 ), such that sTνR (xi ) = wi , for all i ∈ [1, #(I)]. As-
sume w.l.o.g. that TνR (w0 ) = ρ` , for some ` ∈ [1, P ] and let ν 0 = ν[y0 ←
w0 , . . . , y#(I) ← w#(I) ] be a valuation. We prove the following points:
               0
    • |=νwsks R` (y0 ): since |=νwsks RewrTree ∆ (R), TνR (w0 ) = ρ` , ν 0 (y0 ) = w0 and ν 0
         agrees with ν over R.
               0
    • |=νwsks Path xρ`i (y0 , yi , R), for all i ∈ [1, #(I)]: since sTνR (xi ) = wi , we obtain
                                                             0
         π(w0 , wi , ∈)L(Axρ`i ) by Lemma 9 and |=νwsks Path xρ`i (y0 , yi , R) follows, by
         Lemma 8.
               0
    • |=νwsks yi 6= yj , for all 1 ≤ i < j ≤ #(I), such that comp(hP(I)ii ) =
         comp(hP(I)ij ): by Def. 1, wi 6= wj for all i, j ∈ [1, #(I)], such that
         comp(hP(I)ii ) = comp(hP(I)ij ).
               0                                        pi
    • |=νwsks Xq = {yi | i ∈ [1, #(I)], τi = (qi −→ qi0 ), qi = q}, for all q ∈ Qβ : be-
                         •
         cause σν = t = {q1 , . . . , q#(I) }.
                   X

               0                                        pi
    • |=νwsks Xq = {yi | i ∈ [1, #(I)], τi = (qi −→ qi0 ), qi0 = q}, for all q ∈ Qβ : be-
                   X0      •       0       0
         cause σν = t = {q1 , . . . , q#(I) }
We obtain that |=νwsks Ψ`,I(x1 ,...,x#(I) ) and, consequently |=νwsks Φ(X, X0 , R).          

6.5. Structural Invariants
    An invariant I of a marked Petri net N = (N, m0 ), where N = (S, T, E)
is a Petri net, is a set of markings that over-approximates the reachable states
Reach(N ), that is Reach(N ) ⊆ I ⊆ pow(S). The invariant is, moreover, said to
be inductive if and only if it is closed under the transition relation of the Petri
                                             t
net, namely that {m0 | m ∈ I, t ∈ T, m →    − m0 } ⊆ I.
    The synthesis of inductive invariants is a notoriously difficult problem, that
has been received much attention in the past. The most common method of
infering inductive invariants is the iteration of an abstract (over-approximation)


                                              38
transition relation in an abstract domain, until a fixpoint is reached. Depend-
ing on the complexity of the abstract domain, this approach, known as abstract
interpretation [9], can be quite costly. In contrast, we consider inductive invari-
ants that can be synthesized directly from the structure of a Petri net, without
iterating (an abstraction of) its transition relation up to a fixpoint. Such invari-
ants are called structural in the literature [17]. The next definition introduces
two types of structural invariants:

Definition 11. Given a marked Petri net N = (N, m0 ), where N = (S, T, E),
a set of places σ ⊆ S is said to be a:
    • trap if ||σ ∩ m0 || ≥ 1 and, for any t ∈ T , if ||σ ∩ • t|| ≥ 1 then ||σ ∩ t• || ≥ 1,
    • mutex if ||σ ∩ m0 || = 1 and, for any t ∈ T , we have ||σ ∩ • t|| = ||σ ∩ t• || ≤ 1.
The trap and mutex invariant of N are the below sets of markings, respectively:

    • Θ(N ) = {m marking of N | ||m ∩ σ|| ≥ 1, for each trap σ of N },
              def




    • Ω(N ) = {m marking of N | ||m ∩ σ|| = 1, for each mutex σ of N }.
              def




   By substituting the reachable set with the intersection of the trap and mutex
invariant, we obtain the following sufficient queries, that allow to prove the
absence of deadlocks and unreachability of a tuple of states in a system described
by a CL formula:

Lemma 11. Given a tight sentence φ, interpreted over a SID ∆, a behavior
map β and a tuple of states hq1 , . . . , qn i, the following hold:

                    deadlock (φ, ∆, β) ⇒          deadlock ]t (φ, ∆, β)
           reach(φ, hq1 , . . . , qn i, ∆, β) ⇒   reach ]t (φ, hq1 , . . . , qn i, ∆, β)

where deadlock ]t (φ, ∆, β) and reach ]t (φ, hq1 , . . . , qn i, ∆, β) are defined below:

    • deadlock ]t (φ, ∆, β): does there exist a rewriting tree T ∈ T(φ), such that
      Θ(N(Σ, αT , β), mT ) ∩ Ω(N(Σ, αT , β), mT ) ∩ Dead (N(Σ, αT , β)) 6= ∅?

    • reach ]t (φ, hq1 , . . . , qn i, ∆, β): does there exist a rewriting tree T ∈ T(φ) and
      a configuration (αT , m) ∈ Θ(N(Σ, αT , β), mT ) ∩ Ω(N(Σ, αT , β), mT ), such
      that {qi [ui ] | i ∈ [1, n]} ⊆ m, with q1 [u1 ], . . . , qn [un ] pairwise distinct?

Proof : We show first that the trap Θ(N ) and mutex Ω(N ) invariants of a
marked Petri net N are invariants of N . If m0 = ∅ then N has no traps nor
mutexes and Reach(N ) = Θ(N ) = Ω(N ) = ∅, thus Θ(N ) and Ω(N ) are trivially
inductive invariants. So we assume m0 6= ∅.
    For the set Θ(N ), let σ be an arbitrary trap of N . Since m0 6= ∅, we have
||σ ∩ m0 || ≥ 1, hence m0 ∈ Θ(N ), by the choice of σ. For each pair of markings
                                              t
m and m0 , such that m ∈ Θ(N ) and m →        − m0 , for some transition t ∈ T , we
have m0 = (m \ • t) ∪ t• . If σ ∩ • t = ∅ then ||m0 ∩ σ|| ≥ ||m ∩ σ|| and ||m ∩ σ|| ≥ 1,


                                             39
               def
                                     ^                 _            
   Init(Y, R) = m(Y, R) ∧ ∀x .             Yq (x) ↔            R` (x)          (29)
                                    q∈Qβ
                                                 `∈[1,P ] such that
                                                 Cq (z) occurs in ρ`


               def
      θ(X, R) = ∀Y∀Z . Φ(Y, Z, R) → (||X ∩ Y|| ≥ 1 → ||X ∩ Z|| ≥ 1)            (30)
               def
  Θ(X, Y, R) = m(X, R) ∧ ∀Z . (||Y ∩ Z|| ≥ 1 ∧ θ(Z, R)) → ||X ∩ Z|| ≥ 1 (31)

               def
     ω(X, R) = ∀Y∀Z . Φ(Y, Z, R) → (||X ∩ Y|| = 0 ↔ ||X ∩ Z|| = 0) ∧
                                                                  
                                   (||X ∩ Y|| = 1 ↔ ||X ∩ Z|| = 1)   (32)
               def
  Ω(X, Y, R) = m(X, R) ∧ ∀Z . (||Y ∩ Z|| = 1 ∧ ω(Y, R)) → ||X ∩ Z|| = 1 (33)
               Figure 10: Initial Configurations and Structural Invariants


because m ∈ Θ(N ). Otherwise, ||σ ∩ • t|| ≥ 1, thus ||σ ∩ t• || ≥ 1 because σ is
a trap of N , hence ||m0 ∩ σ|| ≥ 1. In both cases, we obtain that ||m0 ∩ σ|| ≥ 1,
hence m0 ∈ Θ(N ), because σ is an arbitrary trap of N .
     A similar argument shows that Ω(N ) is an inductive invariant of N . Let
σ be an arbitrary mutex of N . Then ||σ ∩ m0 || = 1, hence m0 ∈ Ω(N ), by
the choice of σ. For each pair of markings m and m0 , such that m ∈ Θ(N )
            t
and m →    − m0 , for some transition t ∈ T , we have m0 = (m \ • t) ∪ t• and
||σ ∩ • t|| = ||σ ∩ t• || ≤ 1, hence ||m0 ∩ σ|| = 1 and m0 ∈ Ω(N ), because σ is an
arbitrary mutex of N . Moreover, since inductive invariants are closed under
intersection, the set Θ(N ) ∩ Ω(N ) is also an inductive invariant of N . Finally,
because Reach(N ) is known to be the least inductive invariant of N , we obtain
Reach(N ) ⊆ Θ(N ) ∩ Ω(N ). The rest of the proof follows from Theorem 2 and
the above fact.                                                                   
     Given a CL sentence φ that describes the set of initial configurations of a
system, Fig. 10 introduces WSκS formulæ that define the trap and mutex invari-
ants of the marked Petri nets (N(Σ, αT , β), m0 ), where T ∈ T(φ) are rewriting
trees and (αT , m0 ) |= φ are initial configurations. This construction uses the
flow formula (Fig. 9) derived from the SID that interprets the predicate symbols
from φ and the behavior map β of the system. Here we denote by X (resp. Y
and Z) the tuple of second-order variables hXq | q ∈ Qβ iS(resp. hYq | q ∈ Qβ i
and hZq | q ∈ Qβ i) and we write X ∩ Y (resp. X ∩ Z) for q∈Qβ Xq ∩ Yq (resp.
S
   q∈Qβ Xq ∩Zq ), where the definitions of set union and intersection are standard
in MSO and omitted to avoid clutter.
     Let ν be a model of RewrTree ∆ (R), meaning that TνR is a rewriting tree for
                                       def
φ. We recall that, by letting ρ1 = (Aφ () ← φ) be the first rule in the SID, we
                              R
capture the fact that Tν ∈ T(φ), for each model ν of RewrTree ∆ (R) (see the
second conjunct in line 15 from Fig. 6). The formula Init(X, R) (29) encodes
the fact that σνX is an initial marking of the Petri net N(Σ, αTνR , β) namely, that
each node of the rewriting tree TνR is the index of a component of type C in


                                           40
state q, if Cq (z) occurs in the rule that labels the node.
    We assume further that ν is a model of RewrTree ∆ (R) ∧ Init(Y, R). The
formulæ θ(X, R) (30) and Θ(X, Y, R) (31) define the traps and the trap in-
variant of the marked Petri net (N(Σ, αTνR , β), σνY ), respectively. Similarly,
ω(X, R) (32) and Ω(X, R) (33) define the mutexes and the mutex invariant
of (N(Σ, αTνR , β), σνY ), respectively. We intentionally use the same symbols to
denote trap (mutex) invariants and their defining WSκS formulæ, the distinc-
tion between sets of markings and formulæ being clear from the context. The
following lemma shows the correctness of the definitions from Fig. 10:

Lemma 12. If |=νwsks RewrTree ∆ (R) ∧ Init(Y, R) then the following hold:
                                          0
   1. Θ(N(Σ, αTνR , β), σνY ) = {σνX0 | |=νwsks Θ(X, Y, R), ν 0 (Y, R) = ν(Y, R)},
                                          0
   2. Ω(N(Σ, αTνR , β), σνY ) = {σνX0 | |=νwsks Ω(X, Y, R), ν 0 (Y, R) = ν(Y, R)}.

Proof : We give the proof for point (1), the proof for (2) uses a similar argument
and is left for the reader.

“⊆” Let m ∈ Θ(N(Σ, αTνR , β), σνY ) be a marking and ν 0 be a valuation such that
σνX0 = m and ν 0 agrees with ν over Y and R. Clearly, such a valuation exists
                                                0
and, in order to show that m ∈ {σνX0 | |=νwsks Θ(X, Y, R), ν 0 (Y, R) = ν(Y, R)},
                           0                                                0
it suffices to prove |=νwsks Θ(X, Y, R). Because σνX0 = m, we have |=νwsks m(X, R)
                                       0
and we are left with proving |=νwsks ∀Z . θ(Z, R) ∧ ||Y ∩ Z|| ≥ 1 → ||X ∩ Z|| ≥ 1.
To this end, let µ be any valuation that agrees with ν 0 over X, Y and R, such
that |=µwsks θ(Z, R) ∧ ||Y ∩ Z|| ≥ 1. It suffices to prove that σµZ is a trap of the
marked Petri net (N(Σ, αTνR , β), σνY ) to obtain |=µwsks ||X ∩ Z|| ≥ 1, using the fact
that m ∈ Θ(N(Σ, αTνR , β), σνY ) and σµX = m. Note that, since µ agrees with ν 0
over X, we also have σµX = σνX0 = m. Since |=µwsks ||Y ∩ Z|| ≥ 1 and µ agrees with
ν over Y, we have σµZ ∩ σνY 6= ∅. Let t be a transition of N(Σ, αTνR , β), such that
                                                                                  0
σµZ ∩ • t 6= ∅ and let µ0 be a valuation that agrees with µ over Z, such that σµY0 = • t
           0
and σµZ = t• , where Y0 and Z0 are distinct copies of Y and Z, respectively. By
                            0
Lemma 10, we obtain |=µwsks Φ(Y0 , Z0 , R). Since |=µwsks θ(Z, R) and µ0 agrees with
                         0
µ over Z, we obtain |=µwsks ||Z ∩ Z0 || ≥ 1, thus σµZ ∩ σµZ0 = σµZ ∩ t• 6= ∅. We have
                                                            0


showed that σµZ is a trap of the marked Petri net (N(Σ, αTνR , β), σνY ), which
concludes this direction of the proof.
                                                                                      0
“⊇” Let ν 0 be a valuation that agrees with ν over Y and R, such that |=νwsks
Θ(X, Y, R). To show that σνX0 ∈ Θ(N(Σ, αTνR , β), σνY ), we must prove that
σνX0 ∩ θ 6= ∅, for each trap θ of the marked Petri net (N(Σ, αTνR , β), σνY ). Let θ be
such a trap and let µ be a valuation that agrees with ν 0 over X, Y and R, such
that σµZ = θ. Since σmu    Z
                               is a trap of the marked Petri net (N(Σ, αTνR , β), σνY ),
we obtain:
     • |=µwsks ||Y ∩ Z|| ≥ 1, since |=νwsks Init(Y, R) and µ agrees with ν over Y, and
     • |=µwsks θ(X, R), by Lemma 10, since µ agrees with ν over X and R.


                                          41
                                    def
               DeadLock (X, R) = ∀Y∀Z . Φ(Y, Z, R) → ¬Y ⊆ X                         (34)
                                      def
                                          ^
             ErrSet hq1 ,...,qn i (X) =     ||Xq || ≥ ||{i ∈ [1, k] | qi = q}||     (35)
                                          q∈Qβ

       Figure 11: Error Configurations for the Deadlock and Reachability Problems


Since |=µwsks Θ(X, Y, R), we obtain that |=µwsks ||X ∩ Z|| ≥ 1, thus σµX ∩ σµZ = σνX0 ∩
θ 6= ∅, which concludes this direction of the proof.                                  

6.6. Verification Conditions
    The final step in generating sufficient verification conditions for the deadlock
and reachability problems (§4) is the encoding of the sets of error configurations
in WSκS. This is done separately, for the two kinds of errors considered, by
the formulæ in Fig. 11. The convention here is to use X to represent the
configurations in the error sets. However, none of the formulæ from Fig. 11
constrains X to be a marking, i.e. by conjunction with m(X), since the latter
formula is already included in the definition of the structural invariants, by the
formulæ Θ(X, Y, R) and Ω(X, Y, R) (Fig. 10).
    We recall that a marking m is a deadlock of a Petri net N = (S, T, E) if
and only if • t 6⊆ m, for all transitions t ∈ T (if • t ⊆ m for some transition
t, then that transition could be fired from m). This condition is captured by
the DeadLock (X, R) formula (34), where Φ(Y, Z, R) is the flow formula that
defines the pre- and post-sets, for some transition in the Petri net N(Σ, αTνR , β),
where ν is a model ofVRewrTree ∆ (R) (Lemma 10). Here we write Y ⊆ X as
a shorthand for ∀x . q∈Qβ Yq (x) → Xq (x), denoting the fact that the set of
places defined by Y is included in the one defined by X.
    The set defined by the ErrSet hq1 ,...,qn i (X) formula (35) captures the fact that
each configuration encoded by X contains pairwise distinct places q1 [w1 ], . . .,
qn [wn ] which is, essentially, the condition required by a reachability query. Note
that, because the tuple of states hq1 , . . . , qn i is part of the input of the query,
the number ||{i ∈ [1, k] | qi = q}|| of occurrences of each state q in the tuple is
constant, hence the cardinality of each set Xq is compared to a constant (13).
    The following theorem states the soundness of the verification conditions
built throughout this section:

Theorem 3. Given a tight sentence φ, interpreted over a SID ∆, a behavior
map β and a tuple of states hq1 , . . . , qn i, the following hold:
  1. DeadLock (X, R) ∧ Θ(X, Y, R) ∧ Ω(X, Y, R) ∧ Init(Y, R) ∧ RewrTree ∆ (R)
     is unsatisfiable only if deadlock (φ, ∆, β) has a negative answer.

  2. ErrSet hq1 ,...,qn i (X)∧Θ(X, Y, R)∧Ω(X, Y, R)∧Init(Y, R)∧RewrTree ∆ (R)
     is unsatisfiable only if reach(φ, hq1 , . . . , qn i, ∆, β) has a negative answer.




                                                 42
Proof : (1) To prove the contra-positive statement, assume that deadlock (φ, ∆, β)
has a positive answer. By Lemma 11, the query deadlock ]t (φ, ∆, β) has a pos-
itive answer as well, thus there exists a rewriting tree T ∈ T(φ) and a mark-
ing m ∈ Θ(N(Σ, αT , β), mT ) ∩ Ω(N(Σ, αT , β), mT ) ∩ Dead (N(Σ, αT , β)), where
(αT , mT ) is the canonical model of φ corresponding to T . Let ν be a valuation
such that TνR = T , σνY = mT and σνX = m. Since the tuples of second-order
variables X, Y and T are pairwise disjoint, such a valuation exists. We prove
the following points:
    • |=νwsks Init(Y, R) follows directly from the definitions of mT (Def. 7) and
      Init(Y, R) (29).
    • |=νwsks Θ(X, Y, R) follows from point 1 of Lemma 12, because σνX = m,
      TνR = T and m ∈ Θ(N(Σ, αT , β), mT ).
    • |=νwsks Ω(X, Y, R) follows from point 2 of Lemma 12, because σνX = m,
      TνR = T and m ∈ Ω(N(Σ, αT , β), mT ).
    • |=νwsks DeadLock (X, R) because Dead (N(Σ, αT , β)) is the set of markings
                                          0
      σνX0 of N(Σ, αT , β), such that |=νwsks DeadLock (X, R) ∧ RewrTree ∆ (R). This
      follows directly from the definition of a deadlock marking and the defini-
      tion of DeadLock (X, R) (34), using the characterization of the pre- and
      post-sets of the transitions from N(Σ, αT , β) provided by Lemma 10.

(2) The proof of this point follows a similar argument as for point 1, the only
difference being that the set of markings containing a set {qi [ui ] | i ∈ [1, n]} ⊆
                                                                                        0
m, with q1 [u1 ], . . . , qn [un ] pairwise distinct coincides with the set {σνX0 | |=νwsks
ErrSet hq1 ,...,qn i (X) ∧ m(X, R) ∧ RewrTree ∆ (R)}.                                   
    Since the WSκS logic is decidable with non-elementary complexity, in gen-
eral [12], the problem of checking the satisfiability of the verification conditions
provided by Theorem 3 is decidable. By inspection of the formulæ (1) and (2),
one can show that checking the verification conditions is in 4EXPTIME, where
4 is the maximum quantifier alternation depth of these formulæ. In practice,
however, these checks are quite fast, as shown by the preliminary experiments
performed on a similar encoding, reported in our previous work [2].


7. Related Work

    This paper reports on a resource logic for the specification of sets of config-
urations of parametric distributed systems with unbounded numbers of compo-
nents (processes) and a verification method for safety properties, such as absence
of deadlocks and critical section violations.
    Traditionally, verification of unbounded networks of parallel processes con-
siders known architectural patterns, typically cliques or rings [18, 19]. Because
the price for decidability is drastic restriction on architecture styles [20], more re-
cent works propose practical semi-algorithms, e.g. regular model checking [21, 22]
or automata learning [23]. Here the architectural pattern is implicitly deter-
mined by the class of language recognizers: word automata encode pipelines or
rings, whereas tree automata describe trees.


                                            43
    A first attempt at specifying architectures by logic is the interaction logic
of Konnov et al. [24], which is a combination of Presburger arithmetic with
monadic uninterpreted function symbols, that can describe cliques, stars and
rings. More structured architectures (pipelines and trees) can be described
using a second-order extension [25]. As such, these interaction logics are unde-
cidable and have no support for automated verification. Recently, interaction
logics that support the verification of safety properties, by structural invari-
ant synthesis have been developed. These logics use fragments of first order
logic with interpreted function symbols that implicitly determine the class of
architectures, such as cliques [26], or pipelines, rings and trees [27].
    From a theoretical point of view, our resource logic with inductive defini-
tions is strictly more expressive: for instance, a chain of components where
a certain component type occurs on all even (odd) positions is provably not
expressible in first order logic, but can be easily defined using our language,
whose inductive definitions allow to describe second order constructs in a con-
trolled manner (rather than using unrestricted second order quantification, as in
[25]). Moreover, first order logic with successor functions can describe at most
tree-like architectures, whereas our language describes structures more general
than trees6 , using no interpreted function symbols, other than ports involved in
interactions [26, 27].
    Specifying parameterized component-based systems by inductive definitions
is, however, not new. Network grammars [28] use context-free grammar rules
to describe systems with linear (pipeline, token-ring) architectures obtained by
composition of an unbounded number of processes. In contrast, we use predicate
symbols of unrestricted arities to describe architectural patterns that are, in
general, more complex than trees. Such complex structures can be specified
recursively using graph grammar rules with parameter variables [29, 30]. To
avoid clashes, these variables must be renamed to unique names and assigned
unique indices at each unfolding step. Our specifications use quantifiers to avoid
name clashes and separating conjunction to guarantee that the components and
interactions obtained by the unfolding of the rules are unique.
    Verification of network grammars against safety properties requires the syn-
thesis of network invariants [31], computed by rather costly fixpoint iterations
[32] or by abstracting (forgetting the particular values of indices in) the compo-
sition of a small bounded number of instances [33]. Instead, our method uses
lightweight structural invariants, that are synthesized with little computational
effort and prove to be efficient in many practical examples [27, 2].


8. Conclusions and Future Work

    The paper proposes a general framework for the practical semi-algorithmic
verification of parametric systems. The framework integrates previous work

  6 For instance, the tree-shaped architecture with leaves linked in a ring §5.




                                             44
of the authors and extends it through developments in two complementary di-
rections. The first direction is modeling parametric system architectures from
instances of predefined component types and interaction types. Configuration
logic allows the specification of configurations characterizing architecture styles
with snapshots of their component states. Parametric system behavior can be
obtained, in the form of Petri nets using operational semantics, from given
configuration logic specifications and behaviors of component types. We show
that even for very simple linear architectures, essential safety properties such as
deadlock-freedom or mutual explosion are undecidable.
    The second direction proposes a method that from given configuration logic
specifications and the finite-state behavior of its components, leads to formu-
las of WSκS characterizing two types of structural invariants used to prove
deadlock-freedom and mutual exclusion properties. The generation process
avoids the complexity of traditional fixpoint computation techniques. It synthe-
sizes constraints on the state space induced by the interactions of the parametric
architecture. Verification boils down to checking the satisfiability of WSκS for-
mulæ, for which optimized solvers exist. The whole generation process involves
transformations from configuration specifications into rewriting trees and then
into WSκS through path automata. Proving its soundness requires some te-
dious technical developments; nonetheless, its implementation does not suffer
from the usual limitations due to state space complexity and the number of
components. Experimental results show that the proposed verification method
is scalable and allows proving safety in a number of non-trivial cases [2].
    As future work, we plan on adding support for broadcast in our specification
language and develop further the invariant synthesis method to take broadcast
into account. We also envisage an extension of the finite-state model of behavior
to more complex automata, such as pushdown or timed automata.


References

 [1] J. Kramer, J. Magee, Analysing dynamic change in distributed software
     architectures, IEE Proceedings - Software 145 (5) (1998) 146–154.
 [2] M. Bozga, R. Iosif, Specification and safety verification of parametric hi-
     erarchical distributed systems, in: 17th International Conference, FACS
     2021, Virtual Event, October 28-29, 2021, Proceedings, Vol. 13077 of Lec-
     ture Notes in Computer Science, Springer, 2021, pp. 95–114.
 [3] J. C. Reynolds, Separation logic: A logic for shared mutable data struc-
     tures, in: 17th IEEE Symposium on Logic in Computer Science (LICS
     2002), IEEE Computer Society, 2002, pp. 55–74.

 [4] E. Ahrens, M. Bozga, R. Iosif, J. Katoen, Local reasoning about parame-
     terized reconfigurable distributed systems, CoRR abs/2107.05253 (2021).
     URL https://arxiv.org/abs/2107.05253




                                        45
 [5] P. W. O’Hearn, Resources, concurrency, and local reasoning, Theor. Com-
     put. Sci. 375 (1-3) (2007) 271–307.
 [6] I. Sergey, A. Nanevski, A. Banerjee, G. A. Delbianco, Hoare-style speci-
     fications as correctness conditions for non-linearizable concurrent objects,
     SIGPLAN Not. 51 (10) (2016) 92–110.

 [7] F. Farka, A. Nanevski, A. Banerjee, G. A. Delbianco, I. Fábregas, On al-
     gebraic abstractions for concurrent separation logics, Proc. ACM Program.
     Lang. 5 (POPL) (2021) 1–32.
 [8] C. W. Barrett, I. Shikanian, C. Tinelli, An abstract decision procedure for
     a theory of inductive data types, J. Satisf. Boolean Model. Comput. 3 (1-2)
     (2007) 21–46.
 [9] P. Cousot, R. Cousot, Systematic design of program analysis frameworks,
     in: 6th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Pro-
     gramming Languages, ACM Press, New York, NY, 1979, pp. 269–282.

[10] E. L. Post, Finite Combinatory Processes-Formulation 1, The Journal of
     Symbolic Logic 1 (3) (1936) 103–105.
[11] M. Davis, What is a Computation?, in: Mathematics Today Twelve In-
     formal Essays, Conference Board of the Mathematical Sciences, 1978, pp.
     241–267.

[12] J. Thatcher, J. Wright, Generalized finite automata theory with an appli-
     cation to a decision problem of second-order logic, Mathematical systems
     theory 2 (2005) 57–81.
[13] E. Emerson, A. Sistla, Symmetry and model checking, Formal Methods in
     System Design 9 (1996) 105–131. doi:10.1007/BF00625970.

[14] J. G. Henriksen, J. L. Jensen, M. E. Jørgensen, N. Klarlund, R. Paige,
     T. Rauhe, A. Sandholm, Mona: Monadic second-order logic in practice, in:
     First International Workshop, TACAS ’95, Vol. 1019 of LNCS, Springer,
     1995, pp. 89–110.

[15] M. Bojańczyk, Tree-walking automata, in: Language and Automata The-
     ory and Applications: Second International Conference, LATA 2008, Tar-
     ragona, Spain, March 13-19, 2008. Revised Papers, Springer-Verlag, Berlin,
     Heidelberg, 2008, p. 1–2.
[16] B. Khoussainov, A. Nerode, Automata Theory and its Applications,
     Springer, 2001.
[17] J. Sifakis, Structural properties of petri nets, in: Mathematical Founda-
     tions of Computer Science 1978, Proceedings, 7th Symposium, Zakopane,
     Poland, September 4-8, 1978, Vol. 64 of Lecture Notes in Computer Science,
     Springer, 1978, pp. 474–483.


                                       46
[18] S. M. German, A. P. Sistla, Reasoning about systems with many processes,
     J. ACM 39 (3) (1992) 675–735.
[19] M. Browne, E. Clarke, O. Grumberg, Reasoning about networks with many
     identical finite state processes, Information and Computation 81 (1) (1989)
     13 – 31.

[20] R. Bloem, S. Jacobs, A. Khalimov, I. Konnov, S. Rubin, H. Veith, J. Wid-
     der, Decidability of Parameterized Verification, Synthesis Lectures on Dis-
     tributed Computing Theory, Morgan & Claypool Publishers, 2015.
[21] Y. Kesten, O. Maler, M. Marcus, A. Pnueli, E. Shahar, Symbolic model
     checking with rich assertional languages, Theoretical Computer Science
     256 (1) (2001) 93–112.
[22] P. A. Abdulla, G. Delzanno, N. B. Henda, A. Rezine, Regular model
     checking without transducers (on efficient verification of parameterized sys-
     tems), in: 13th International Conference, TACAS 2007, Vol. 4424 of LNCS,
     Springer, 2007, pp. 721–736.
[23] Y. Chen, C. Hong, A. W. Lin, P. Rümmer, Learning to prove safety over
     parameterised concurrent systems, in: 2017 Formal Methods in Computer
     Aided Design, FMCAD 2017, IEEE, 2017, pp. 76–83.
[24] I. V. Konnov, T. Kotek, Q. Wang, H. Veith, S. Bliudze, J. Sifakis, Param-
     eterized systems in BIP: design and model checking, in: 27th International
     Conference on Concurrency Theory, CONCUR 2016, Vol. 59 of LIPIcs,
     Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2016, pp. 30:1–30:16.
[25] A. Mavridou, E. Baranov, S. Bliudze, J. Sifakis, Configuration logics: Mod-
     eling architecture styles, J. Log. Algebr. Meth. Program. 86 (1) (2017) 2–29.

[26] M. Bozga, R. Iosif, J. Sifakis, Checking deadlock-freedom of paramet-
     ric component-based systems, in: 25th International Conference, TACAS
     2019, Vol. 11428 of LNCS, Springer, 2019, pp. 3–20.
[27] M. Bozga, J. Esparza, R. Iosif, J. Sifakis, C. Welzel, Structural invariants
     for the verification of systems with parameterized architectures, in: 26th In-
     ternational Conference, TACAS 2020, Vol. 12078 of LNCS, Springer, 2020,
     pp. 228–246.
[28] Z. Shtadler, O. Grumberg, Network grammars, communication behaviors
     and automatic verification, in: Automatic Verification Methods for Finite
     State Systems, International Workshop, Vol. 407 of LNCS, Springer, 1989,
     pp. 151–165.
[29] D. Le Metayer, Describing software architecture styles using graph gram-
     mars, IEEE Transactions on Software Engineering 24 (7) (1998) 521–533.



                                        47
[30] D. Hirsch, P. Inverardi, U. Montanari, Graph grammars and constraint
     solving for software architecture styles, in: Proceedings of the Third In-
     ternational Workshop on Software Architecture, ISAW ’98, Association for
     Computing Machinery, New York, NY, USA, 1998, p. 69–72.
[31] P. Wolper, V. Lovinfosse, Verifying properties of large sets of processes
     with network invariants, in: Automatic Verification Methods for Finite
     State Systems, International Workshop, Vol. 407 of LNCS, Springer, 1989,
     pp. 68–80.
[32] D. Lesens, N. Halbwachs, P. Raymond, Automatic verification of parame-
     terized linear networks of processes, in: The 24th ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, ACM Press, 1997,
     pp. 346–357.
[33] Y. Kesten, A. Pnueli, E. Shahar, L. D. Zuck, Network invariants in action,
     in: CONCUR 2002 - Concurrency Theory, 13th International Conference,
     Vol. 2421 of LNCS, Springer, 2002, pp. 101–115.




                                      48
