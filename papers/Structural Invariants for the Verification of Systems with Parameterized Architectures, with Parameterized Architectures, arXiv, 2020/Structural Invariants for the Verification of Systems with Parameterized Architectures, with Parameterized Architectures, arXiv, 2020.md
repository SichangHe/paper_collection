                                            Structural Invariants for the Verification of Systems
                                                    with Parameterized Architectures

                                                      Marius Bozga1 , Javier Esparza2 , Radu Iosif1 , Joseph Sifakis1
                                                                         and Christoph Welzel2
                                                          1   Univ. Grenoble Alpes, CNRS, Grenoble INP?? , Verimag
                                                                       2 Technische Universität München
arXiv:2002.07672v2 [cs.DC] 7 Sep 2021




                                            We consider parameterized concurrent systems consisting of a finite but unknown
                                        number of components, obtained by replicating a given set of finite state automata.
                                        Components communicate by executing atomic interactions whose participants update
                                        their states simultaneously. We introduce an interaction logic to specify both the type of
                                        interactions (e.g. rendez-vous, broadcast) and the topology of the system (e.g. pipeline,
                                        ring). The logic can be easily embedded in monadic second order logic of κ ≥ 1 succes-
                                        sors (WSκS), and is therefore decidable.
                                            Proving safety properties of such a parameterized system, like deadlock freedom
                                        or mutual exclusion, requires to infer an inductive invariant that contains all reachable
                                        states of all system instances, and no unsafe state. We present a method to automati-
                                        cally synthesize inductive invariants directly from the formula describing the interac-
                                        tions, without costly fixed point iterations. We experimentally prove that this invariant
                                        is strong enough to verify safety properties of a large number of systems including
                                        textbook examples (dining philosophers, synchronization schemes), classical mutual
                                        exclusion algorithms, cache-coherence protocols and self-stabilization algorithms, for
                                        an arbitrary number of components.


                                        1    Introduction
                                        The problem of parameterized verification asks whether a system composed of n repli-
                                        cated processes is safe, for all n ≥ 2. By safety we mean that every execution of the
                                        system stays clear of a set of global error configurations, such as deadlocks or mutual
                                        exclusion violations. Even if we assume each process to be finite-state and every inter-
                                        action to be a synchronization of actions without exchange of data, ranging over large or
                                        infinite domains, the problem remains challenging because we ask for a general proof
                                        of safety, that works for any number of processes.
                                            In general, parameterized verification is undecidable, even if processes only manip-
                                        ulate data from a bounded domain [6]. Various restrictions of communication and ar-
                                        chitecture3 define decidable subproblems [16,29,25,5]. Seminal works consider rendez-
                                        vous communication, with participants placed in a ring [16,25] or a clique [29] of arbi-
                                        trary size. Recently, MSO-definable graphs (with bounded tree- and clique-width) and
                                        point-to-point rendez-vous communication have been considered [5]. Most approaches
                                        to define decidable problems focus on manually proving a cut-off bound c ≥ 2 such that
                                        ?? Institute of Engineering Univ. Grenoble Alpes
                                         3 We use the term architecture for the shape of the graph along which the interactions take place.
correctness for at most c processes implies correctness for any number of processes
[16,25,24,7,31]. Other methods identify systems with well-structured transition rela-
tions [29,1,27]. An exhaustive chart of decidability results for verification of parameter-
ized systems is drawn in [12]. When decidability is not of concern, over-approximating
and semi-algorithmic techniques such as regular model checking [33,2], SMT-based
bounded model checking [4,19], abstraction [10,14] and automata learning [17] can be
used to deal with more general classes of systems.
     The efficiency of a verification method crucially relies on its ability to synthesize an
inductive safety invariant, i.e., an infinite set of configurations that contains the initial
configurations, is closed under the transition relation, and excludes the error configura-
tions. In general, automatically synthesizing invariants requires computationally expen-
sive fixpoint iterations [20]. In the particular case of parameterized systems, invariants
can be either global, relating the local states of all processes [21], or modular, relating
the local states of a few processes whose identity is irrelevant [35,18].
Our Contributions. The novelty of the approach described in this paper is three-fold:
  1. The architecture of the system is not fixed a priori, but given as a parameter of
     the verification problem. In fact, we describe parameterized systems using the
     Behavior-Interaction-Priorities (BIP) framework [9], in which processes are in-
     stances of finite-state component types, whose interfaces are sets of ports, labeling
     transitions between local states, and interactions are sets of strongly synchronizing
     ports, described by formulae of an interaction logic. An interaction formula cap-
     tures the architecture of the interactions (pipeline, ring, clique, tree) and the com-
     munication scheme (rendez-vous, broadcast), which are not hardcoded, but rather
     specified by the designer of the system.
  2. We synthesize parameterized invariants directly from the interaction formula of a
     system, without iterating its transition relation. Such invariants depend only on the
     structure (and not on the operational semantics) of an infinite family of Petri Nets,
     one for each instance of the system, being thus structural invariants. Essentially,
     the invariants we infer use the traps4 of the system, which are sets W of local states
     with the property that, if a process is initially in a state from W, then always some
     process will be in a state from W. Following [11,15], we call them (parameter-
     ized) trap invariants. Computing trap invariants only requires a simple syntactic
     transformation of the interaction formula and the result is expressed using WSκS,
     the weak monadic second order logic of κ ≥ 1 successor functions. Thus invariant
     computation is very cheap, and the verification problem (proving the emptiness of
     the intersection between the invariant and the set of error states) is reduced to the
     unsatisfiability of a WSκS formula with a single quantifier alternation. In practice,
     this check can be carried out quite efficiently by existing tools, such as Mona [30].
  3. We refine the approach by considering another type of invariants, called 1-invariants,
     that can also be derived cheaply from the interaction formula of the system. We
     show that 1-invariants in conjunction with trap invariants successfully verify addi-
     tional examples.
Comparison to related work. Trap invariants have been very successfully used in the
verification of non-parameterized systems [11,26,13]. The technique was lifted to pa-
4 Called in this way by analogy with the notion of traps for Petri Nets [36].
rameterized systems in [15], but the work there is only applicable to clique architec-
tures, in which processes are indistinguishable, and the system can be described by
one single Petri Net with an infinite family of initial markings. Here, for the first time,
we show that the trap technique can be extended to pipelines, token rings and trees,
where the system is defined by an infinite family of Petri Nets, each with a different
structure. These systems cannot be analyzed using the techniques of [29,1,27], because
they do not yield well-structured transition systems. Contrary to [16,25,24,7,31], our
approach does not require a manual cut-off proof. Contrary to regular model checking
and automata learning [2,17], it does not require any symbolic state-space exploration.
Finally, our approach produces an explanation of why the property holds in terms of the
trap invariant and 1-invariants used. Summarizing, our approach provides a compara-
tively cheap technique for parameterized verification, that succeeds in numerous cases.
It is ideal as preprocessing step, that can very quickly lead to success with a very clear
explanation of why the property holds, and otherwise provides at least a strong invariant
that can be used for further analysis.



                    `(k)        t(k)    p(k)       g(k)   `(succ(k)) t(succ(k))

                            f                  w                    f


                     `             t     p           g         `        t


                           b                   e                   b

                         Fork(k)       Philosopher(k)      Fork((k + 1) mod N)
               Γphilo = (g(i) ∧ t(i) ∧ t(succ(i))) ∨ (p(i) ∧ `(i) ∧ `(succ(i)))
                          Fig. 1: Parameterized Dining Philosophers

Running Example. Consider the dining philosophers system in Fig. 1, consisting of
n ≥ 2 components of type Fork and Philosopher respectively, placed in a ring of size 2n.
The k-th philosopher has a left fork, of index k, and a right fork, of index (k + 1) mod n.
Each component is an instance of a finite state automaton with states f (ree) and b(usy)
for Fork, respectively w(aiting) and e(ating) for Philosopher. A fork goes from state f
to b via a t(ake) transition and from f to b via a `(eave) transition. A philosopher goes
from w to e via a g(et) transition and from e to w via a p(ut) transition. The g action of the
k-th philosopher is executed jointly with the t actions of the k-th and [(k + 1) mod n]-th
forks, in other words, the philosopher takes both its left and right forks simultaneously.
Similarly, the p action of the k-th philosopher is executed simultaneously with the `
action of the k-th and [(k + 1) mod n]-th forks, i.e. each philosopher leaves both its
left and right forks at the same time. We describe these interactions by the interaction
formula:
              Γphilo = (g(i) ∧ t(i) ∧ t(succ(i))) ∨ (p(i) ∧ `(i) ∧ `(succ(i))) .           (1)
where the free variable i refers at some arbitrary component index.
     Intuitively, the transitions of the system with n dining philosophers and n forks are
given by the minimal models of the disjuncts of Γphilo with universe {0, 1, . . . , n − 1}, and
succ interpreted as “successor modulo n’. In particular, for each 0 ≤ k ≤ n − 1 the first
disjunct has a minimal model that interprets the predicates g and t as the sets {k} and
{k, (k + 1) mod n}. This model describes the interaction in which the k-th philosopher
takes a g-transition (from waiting to eating), while, simultaneously, the k-th and (k + 1)-
th forks take t-transitions (from free to busy). This is graphically represented by one of
the dashed lines in Fig. 1. Observe that the ring topology of the system is implicit in the
modulo-n interpretation of the successor function.
     Since philosophers can only grab their two forks simultaneously, the system is
deadlock-free for any number n ≥ 2 of philosophers. An automatic proof requires to
compute an invariant, and prove that it has an empty intersection with the set of dead-
lock configurations defined by the WSκS formula
            deadlock(Xw , Xe , X f , Xb ) = ∀i . [¬Xw (i) ∨ ¬X f (i) ∨ ¬X f (succ(i))] ∧
                                                 [¬Xe (i) ∨ ¬Xb (i) ∨ ¬Xb (succ(i))]        (2)
where Xw , Xe , X f , Xb are set variables, the intended meaning of Xw (i) resp. Xe (i) is that
the i-th philosopher is waiting, resp. eating, and the intended meaning of X f (i) resp.
Xb (i) is that the i-th fork is free, resp. busy. Our method automatically computes from
Γphilo the formula
             trap-predS (Xw , Xe , X f , Xb ) = ∀i . [Xw (i) ∨ X f (i) ∨ X f (succ(i))] ↔
                                             [Xe (i) ∨ Xb (i) ∨ Xb (succ(i))] .       (3)
Contrary to other approaches, the computation does not require any state-space explo-
ration. The method guarantees that its set of models is an inductive invariant. Since the
conjunction deadlock ∧trap-predS is unsatisfiable, which can be automatically checked,
the system is deadlock-free, for any number of philosophers.


2   Parameterized Component-based Systems
A component type is a tuple C = hP, S, s0 , ∆i, where P = {p, q, r, . . .} is a finite set of
ports, S is a finite set of states, s0 ∈ S is an initial state and ∆ ⊆ S × P × S is a set of
                        p
transitions denoted s →− s0 , for s, s0 ∈ S and p ∈ P. We assume there are no two different
transitions with the same port.
    A component-based system S = hC1 , . . . , CN , Γi consists of a fixed number N ≥ 1
of component types Ck = hPk , Sk , s0 k , ∆k i and an interaction formula Γ. In the dining
philosophers there are two component types, Philosopher and Fork, each with two
states and two transitions, as shown in Fig. 1. We assume that Pi ∩ P j = ∅ and Si ∩ S j = ∅,
for all 1 ≤ i < j ≤ N. We denote the component type of a port p or a state s by type(p)
and type(s), respectively. For instance, in Fig. 1 we have type(p) = type(g) = type(w) =
type(e) = Philosopher and type(t) = type(`) = type( f ) = type(b) = Fork.
    The interaction formula Γ determines the family of systems we can construct out
of these components. It does so by specifying, for each possible number of replicated
instances (for example, 3 philosophers and 3 forks), which are the possible interac-
tions between them. An interaction consists of a set of transitions that are executed
simultaneously. For example, in an interaction philosopher 3 executes a g(et) transition
simultaneously with t(ake) transitions of the forks 2 and 3. Before formalizing this, we
introduce the syntax and semantics of Interaction Logic.
Interaction Logic. For a constant κ ≥ 1, fixed throughout the paper, the Interaction
Logic ILκ is built on top of a countably infinite set Var of variables, the set Pred =
SN k
  k=1 P of monadic predicate symbols ranged over by pr (i.e. the logic has a predicate
symbol for each port), the binary predicate ≤, and the successor functions succ0 , . . . , succκ−1 ,
of arity one. The formulae of ILκ are generated by the syntax
                          t := i ∈ Var | succ0 (t) | . . . | succκ−1 (t)   terms
                         φ := t1 ≤ t2 | pr(t) | φ1 ∧ φ2 | ¬φ1 | ∃i . φ1 formulae
Abbreviations like t1 = t2 , t1 < t2 , φ1 ∨ φ2 , φ1 ↔ φ2 , and ∀i . φ are defined as usual.
ILκ is interpreted over finite ranked trees of arity κ, which we identify with a prefix-
closed language of words, also called nodes, over the alphabet {0, . . . , κ − 1}. The root of
the tree is the empty word , and the children of w are w0, w1, . . . , w(κ − 1). Formally,
an interpretation or structure is a pair I = (U, ι), where the universe U is a tree and
ι assigns a node to each variable and a set of nodes to each predicate in Pred. The
predicate ≤ and the functions succ0 , . . . , succk−1 have the usual fixed interpretations: If t
and t0 are interpreted as w and w0 , then t1 ≤ t2 holds iff w is a prefix of w0 , and succi (t) is
interpreted as the node wi, if wi ∈ U, and as the root  otherwise. So, loosely speaking,
successor functions wrap around to the root.
     When κ = 1, formulae are interpreted on languages {, 0, 00, . . . , 0n−1 } for some num-
ber n. To simplify notation, in this case we assume that they are interpreted over the set
{0, 1, . . . , n − 1}, and succ0 is the usual successor function on numbers, modulo n.
     Intuitively, a universe U determines an instance of the component-based system,
with one instance of each component for each w ∈ U. So, for example, for κ = 1 and
U = {0, 1, 2, . . . , n − 1} we have in our running example philosophers 0, 1, . . . , n − 1 and
forks 0, 1, . . . , n − 1. Generally, with κ = 1 we can describe pipeline and token-ring ar-
chitectures, whereas higher values describe tree-shaped architectures.
Interaction formulae. A formula of ILκ is an interaction formula if it is the conjunction
of the following formula:
                       ∀i∀ j .
                               V
                                             p(i) ∧ q( j) → i , j
                                 p,q∈Pred                                             (4)
                                    type(p)=type(q)
with a finite disjunction of formulae of the form:
                  C(i1 , . . . , i` ) = ϕ ∧ `j=1 p j (i j ) ∧ mj=1 ∀k . ψ j → q j (k)
                                      def  V                 V
                                                                                        (5)
where ϕ, ψ1 , . . . , ψm are conjunctions of atomic formulae of the form t1 ≤ t2 and their
negations. Intuitively, formula (4) is a generic axiom that prevents two ports of the same
instance of a component type from interacting. The formulae of form (5) are called the
clauses of the interaction formula.

Example 1. Consider a component-based system S = hC1 , C2 , Γi, where C1 and C2 have
ports p1 and p2 , respectively, and Γ has one single clause
         C(i, j, k) = (i < j ∧ k = succ( j)) ∧ (p1 (i) ∧ p2 ( j)) ∧ ∀i.i > k → p1 (i)
Γ states that an interaction consists of: the i-th process of type C1 executes transition p1 ;
the j-th process of type C2 executes p2 ; and, for every i > ( j + 1) mod n, the i-th process
of type C1 executes transition p1 as well; all this happens simultaneously in one atomic
step.                                                                                 

     Loosely speaking, (5) states that in an interaction ` components can simultaneously
engage in a multiparty rendez-vous, together with a broadcast to the ports q1 , . . . , qm of
the components whose indices satisfy the constraints ψ1 , . . . , ψm , respectively. An exam-
ple of peer-to-peer rendez-vous with no broadcast is the dining philosophers system in
Fig. 1, whereas examples of broadcast are found among the test cases in §5. In the next
section we show that, despite this generality, it is possible to construct a trap invariant
for any interaction formula in a purely syntactic way.
     Observe that the formula does not explicitly specify that every other process remains
idle. Formally, as we will see in the next section, the system has an interaction for each
minimal model of (5), which allows us not to have to specify idleness. Given structures
I1 = (U, ι1 ) and I2 = (U, ι2 ) sharing the same universe U, we say I1 v I2 if and only if
ι1 (pr) ⊆ ι2 (pr) for every pr ∈ Pred. Given a formula φ, a structure I is a minimal model
of φ if I |= φ and, for all structures I0 such that I0 v I and I0 , I, we have I0 6|= φ.


2.1   Execution Semantics of Component-based Systems

The semantics of a component-based system S = hC1 , . . . , CN , Γi is an infinite family of
Petri Nets, one for each universe of Γ. The reachable markings and actions of the Petri
Net characterize the reachable global states and transitions of the system, respectively.
To fix notations, we recall several basic definitions.
Preliminaries: Petri Nets. A Petri Net (PN) is a tuple N = hS , T, Ei, where S is a set of
places, T is a set of transitions, S ∩ T = ∅, and E ⊆ (S × T ) ∪ (T × S ) is a set of edges.
                                                                                           def
The elements of S ∪ T are called nodes. Given nodes x, y ∈ S ∪ T , we write E(x, y) = 1
                          def                                    def
if (x, y) ∈ E and E(x, y) = 0, otherwise. For a node x, let • x = {y ∈ S ∪ T | E(y, x) = 1},
    def
x• = {y ∈ S ∪ T | E(x, y) = 1} and lift these definitions to sets of nodes.
     A marking of N is a function m : S → N. A transition t is enabled in m if and only if
                                                                                         t
m(s) > 0 for each place s ∈ • t. For all markings m, m0 and transitions t, we write m →  − m0
whenever t is enabled in m and m0 (s) = m(s) − E(s, t) + E(t, s), for all s ∈ S . Given two
markings m and m0 , a finite sequence of transitions σ = t1 , . . . , tn is a firing sequence,
             σ
written m − → m0 if and only if either (i) n = 0 and m = m0 , or (ii) n ≥ 1 and there exist
                                       t1              tn
markings m1 , . . . , mn−1 such that m −
                                       → m1 . . . mn−1 −
                                                       → m0 .
     A marked Petri Net is a pair N = (N, m0 ), where m0 is the initial marking of N.
                                                                                  σ
A marking m is reachable in N if there exists a firing sequence σ such that m0 − → m.
We denote by R(N) the set of reachable markings of N. A marked PN N is 1-safe if
m(s) ≤ 1, for each s ∈ S and m ∈ R(N). All PNs considered in the following will be
1-safe and we shall silently blur the distinction between a marking m : S → {0, 1} and
the boolean valuation βm : S → {⊥, >} defined as βm (s) = > ⇐⇒ m(s) = 1. A set of
markings M is an inductive invariant of N = (N, m0 ) if and only if m0 ∈ M and for each
   t
m→ − m0 such that m ∈ M, we have m0 ∈ M.
Petri Net Semantics of Component-Based Systems. We define the semantics of a
component-based system as an infinite family of 1-safe Petri Nets. Let S = hC1 , . . . , CN , Γi
be a system with component types Ck = hPk , Sk , s0 k , ∆k i, for every k = 1, . . . , N. Fix a uni-
                                                   def
verse U of Γ. We define a marked Petri Net NSU = (hS , T, Ei, m0 ) as follows:
        def S N
                    
 – S =             k
              k=1 S × U that is, the net has a place (s, u) for each state s of each compo-
     nent type, and for each node u.
 – For each minimal model I = (U, ι) of a clause C of Γ, the set T contains a transition
                                                                                             p
                 the set E contains edges ((s, u), tι ) and (tι , (s , u)) for every s →
                                                                     0                      − s0 ∈
    tιS∈ T , and
         k=1 ∆ such that u ∈ ι(p). Nothing else is in T or E. Intuitively, tι “synchronizes”
         N    k

                                  p
                           − s0 of the different components occurring in the interaction.
     all the transitions s →
  – For each 1 ≤ k ≤ N, each s ∈ Sk and each u ∈ U, m0 ((s, u)) = 1 if s = s0 k and
     m0 ((s, u)) = 0, otherwise that is, m0 contains the places (s, u) such that s is an initial
     state.
    It follows immediately from this definition that NSU is a 1-safe Petri Net. Indeed, for
every u ∈ U, for every component-type Ck , and for every reachable marking m, we have
  s∈Sk m((s, u)) = 1. This reflects that the instance of C at u is always in exactly one of
                                                              k
P
                 k
the states of S ; if s is that state, then (s, u) is the place carrying the token.
Example 2. Consider our running example, with U = {0, 1, . . . , n−1}, i.e., n philosophers
and n forks. Since the interaction formula (1) has no constants, its models are pairs
(U, ι), where ι gives the interpretation of the free variable i and the predicates g, t, etc.
The first disjunct of (1) is [g(i) ∧ t(i) ∧ t(succ(i))]. It has a minimal model for each k ∈ U,
namely the model with ι(i) = k, ι(g) = {k} and ι(t) = {k, (k + 1) mod n}. In the interaction
produced by this model, the k-th philosopher executes transition g(et), the forks with
numbers k and (k + 1) mod n execute transition t(ake), and all other philosophers and
forks remain idle. The second disjunct yields the interactions in which a philosopher
puts down its forks. Fig. 2 shows the Petri Net NSU for universe U = {0, 1, 2}. For clarity,


                         (w, 0)                       (w, 1)                   (w, 2)


          ( f, 0)                      ( f, 1)                  ( f, 2)                      ( f, 0)




                    i1                i2         i3            i4         i5            i6




          (b, 0)                       (b, 1)                   (b, 2)                       (b, 0)

                         (e, 0)                       (e, 1)                   (e, 2)

Fig. 2: Petri Net of the dining philosophers for the universe U = {0, 1, 2}. In reality, the
two pink and green places are only one place.


the places ( f, 0) and (b, 0) have been duplicated; in reality the two copies are merged.
The places of each philosopher are {(w, i), (e, i)} for i = 0, 1, 2. For example, transition
i3 corresponds to the minimal model {(g, 1), (t, 1), (t, 2)}, in which philosopher 1 takes
forks 1 and 2.


3     Trap Invariants

Given a Petri Net N = (S , T, E), a set of places W ⊆ S is called a trap if and only if
W • ⊆ • W. A trap W of N is an initially marked trap (IMT) of the marked PN N = (N, m0 )
if and only if m0 (s) = > for some s ∈ W.

Example 3. The Petri Net of Fig. 2 has many traps. Examples are {( f, 1), (b, 1)} and
{( f, 0), (b, 1), ( f, 2), (e, 2)}.

    An IMT defines an invariant of the Petri Net, because some place in the trap will
always be marked, no matter which sequence of transitions is fired. The trap invariant
of N is the set of markings that mark each IMT of N. Clearly, since marked traps
remain marked, the set of reachable markings is contained in the trap invariant. Hence,
to prove that a certain set of markings is unreachable, it is sufficient to prove that the
this set has empty intersection with the trap invariant. For self-completeness, we briefly
discuss the computation of the trap invariant for a given marked Petri Net of fixed size,
before explaining how this can be done for the infinite family of marked Petri Nets
defining the executions of parameterized systems.
    The trap constraint of a Petri Net N = (S , T, E) is the formula:
                                def V
                          Θ(N) = t∈T
                                          W             W         
                                            x ∈ •t x →     y ∈ t• y
where each place x, y ∈ S is viewed as a propositional variable. It is not hard to show5
that any boolean valuation β : S → {⊥, >} that satisfies the trap constraint Θ(N) defines
a trap Wβ of N in the obvious sense Wβ = {s ∈ S | β(s) = >}. Further, if m0 : S → {0, 1} is
                                             def W
the initial marking of a 1-safe PN N and µ0 = m0 (s)=1 s is a propositional formula, then
every valuation of µ0 ∧ Θ(N) defines an IMT of (N, m0 ). Usually, computing invariants
requires building a sequence of underapproximants whose limit is the least fixed point
of an abstraction of the transition relation of the system [20]. This is not the case of
the trap invariant, that can be directly computed from the trap constraint and the initial
marking [11,15].
    In the rest of the section we construct a parameterized trap constraint that charac-
terizes the traps, not of one single net, as Θ(N), but of the infinite family of Petri Nets
obtained from a component-based system. The parameterized trap constraint is a for-
mula of WSκS. In Section 3.1 we first explain how to embed our interaction logic into
WSκS, and in Section 3.2 we construct the parameterized trap constraint.


3.1   From ILκ to WSκS

We briefly recall the syntax and semantics of WSκS , the monadic second order logic
WSκS of κ successors (see e.g. [34]). Let SVar be a countably infinite set of second-
5 See e.g. [8] for a proof.
order variables (also called set variables), denoted as X, Y, . . . in the following. The syn-
tax of WSκS is:
                t :=  | x | succ0 (t) | . . . | succκ (t)                          terms
               φ := t1 = t2 | pr(t) | X(t) | φ1 ∧ φ2 | ¬φ1 | ∃x . φ1 | ∃X . φ1 formulae
So WSκS extends ILκ, with the constant symbol , atoms X(t) and monadic second
order quantifiers ∃X . φ. We can consider w.l.o.g. equality atoms t1 = t2 instead of the
inequalities t1 ≤ t2 in ILκ, because the latter can be defined in WSκS as usual:
  x ≤ y = ∀X . closed(X) ∧ X(x) → X(y) closed(X) = ∀x . X(x) → κ−1
         def                                                     def              V
                                                                                    i=0 X(succi (x))
     Like ILκ, the formulae of WSκS are interpreted on ordered trees of arity κ. The
models of WSκS are structures (U, ι), where ι assigns the root of the tree to , a node
ι(x) to each variable x ∈ Var and a set ι(X) ⊆ U to each set variable X ∈ SVar. The
satisfaction relation (U, ι) |=WSκS φ is defined as for ILκ, with one difference: in ILκ, the
successor of a leaf of a tree is the root of the tree, while in WSκS the successor of leaf
is, by convention, the leaf itself [34, Example 2.10.3]. This is the only reason why ILκ
is not just a fragment of WSκS.
     We define an embedding of ILκ formulae, without occurrences of predicates and
set variables, into WSκS. W.l.o.g. we consider ILκ formulae that have been previ-
ously flattened, i.e the successor function occurs only within atomic propositions of
the form succi (x) = y. This is done by replacing each atomic proposition of the form
succi1 (. . . succin (x) . . .) = y by the formula ∃x1 . . . ∃xn . xn = succin (x) ∧ y = succi1 (x1 ) ∧
   j=1 x j = succi j (x j+1 ). The translation of an ILκ formula φ into WSκS is the formula
Vn−1
Tr(φ), defined recursively on the structure of φ, is homomorphic w.r.t. the first-order
connectives and:
                                      def
                 Tr(succi (x) = y) = (¬ max(x) ∧ succi (x) = y) ∨ (max(x) ∧ y = )
We show that a formula φ of ILκ and its WSκS counterpart Tr(φ) are equivalent:

Lemma 1. Given an ILκ formula φ, for any structure I = (U, ι), we have I |=IL φ ⇐⇒
I |=WSκS Tr(φ).


3.2   Defining Parameterized Trap Invariants in WSκS

Fix a component-based system S = hC1 , . . . , CN , Γi and recall that every universe U in-
                                               SN k                                  SN i
duces a Petri Net NUS whose set of places is k=1     S × U. For every state s ∈ i=1     S , let
X s be a monadic second-order variable, and let X be the tuple of these variables in an
arbitrary but fixed order. We define a formula trap-predS (X), with X as set of free vari-
ables, that characterizes the traps of the infinitely many Petri Nets NUS corresponding to
S. Formally, trap-predS (X) has the following property:
                                                   SN k
     For every universe U and for every set P ⊆ k=1      S × U of places of NU    S
                                                                                    :
                     U
     P is a trap of NS iff the assignment Xq 7→ {u ∈ U | (q, u) ∈ P} satisfies trap-predS (X).

Observe that every assignment to X encodes a set of places, and vice versa. So, abusing
language, we can speak of the set of places X.
    We define auxiliary predicates that capture the intersection of the set of places X
with the pre and postset of a transition in NUS . For every clause C of Γ, of the form (5),
we define the WSκS formulae:
      intersects-preCS (X, x1 , . . . , x` ) = `j=1 X• p j (x j ) ∨ `+m    ∃x j . Tr(ψ j ) ∧ X• p j (x j ) and
                                              W                    W
                                                 `                  Wj=`+1
                                                                      `+m
      intersects-postS (X, x1 , . . . , x` ) = j=1 X p j (x j ) ∨ j=`+1 ∃x j . Tr(ψ j ) ∧ X p j • (x j ).
                      C                        W
                                                          •



Now we can define trap-predS (X) as the conjunction of the following formulae, one for
each clause C (5) in Γ:
                                  h                                               i
                   ∀x1 . . . ∀x` . Tr(ϕ) ∧ intersects-preCS (X, x1 , . . . , x` )
                                                                                    (6)
                                       → intersects-postCS (X, x1 , . . . , x` ).
So, intuitively, trap-predS (X) states that for every transition of the Petri Net, if the set
X of places intersects the preset of the transition, then it also intersects its postset. This
is the condition for the set of places to be a trap. Formally, we obtain:

Lemma 2. Given a component-based system S = hC1 , . . . , CN , Γi and a structure I =
(U, ι), where ι is an interpretation of the set variables X, the set P = {hs, ui ∈ k=1
                                                                                  SN k
                                                                                       S ×U |
u ∈ ι(X s )} is a trap of NUS if and only if (U, ι) |=WSκS trap-predS (X).

Parameterized Trap Invariants in WSκS. Loosely speaking, the intended meaning
of trap-predS (X) is “the set of places X is a trap”. Our goal is to construct a formula
stating: “the marking m marks all initially marked traps”.
    Recall that the Petri Nets obtained from component-based systems are always 1-
safe, and so a marking is also a set of places. Recall, however, that all reachable mark-
ings have the property that they place exactly one token in the set of places modeling the
set of states of a component (loosely speaking, the set of places of the k-th philosopher
is (w, k) and (e, k), and there is always one token in the one or the other). So we define
a formula markingS (X) with intended meaning “the set of places X is a legal marking”,
and another one, trap-invariantS (X) with intended meaning “the set of places X marks
every initially marked trap (IMT)”.
    In addition to the tuple of set variables X defined above, we consider now the “copy”
          def
tuple X 0 = hX s0 i s∈Si ,1≤i≤N . Intuitively, X and X 0 represent one set of places each.
    We define a (1-safe) marking as a set of places that marks exactly one state of each
copy of each component:
                                                                                  
                                              ^ _               ^               
                  markingS (X) = ∀x .                 X s (x) ∧
                                                      
                                                                       ¬X  s 0 (x)
                                                                                      .
                                                                                      
                                               1≤i≤N s∈S i              s0 ∈S i \ {s}
Secondly, we give a formula describing the intersection of two sets of places:
                                               _
                intersectionS (X, X 0 ) = ∃x .        (X s (x) ∧ X s0 (x)).
                                                             s∈ 1≤i≤N Si
                                                               S

Finally, to actually capture IMTs we need to determine if a trap is initially marked.
However, this can be easily described by the formula:
                                                    _
                       initially-markedS (X) = ∃x .   X s0 i (x).
                                                                    1≤i≤N
and so we can define the trap-invariant by the WSκS formula:
                                     h                                            i
        trap-invariantS (X) = ∀X 0 . trap-predS (X 0 ) ∧ initially-markedS (X 0 )
                                                                                                                 (7)
                                                        → intersectionS (X, X 0 ).
Relying on Lemma 2 we are assured that the set represented by X intersects all IMTs.
Further, let ϕ(X) be any formula that defines a set of good global states of the component-
based systems (or, equivalently, a good set of markings of their corresponding Petri
nets), with the intuition that, at any moment during execution, the current global state
of the component-based system should be good. We can now state the following theo-
rem, that captures the soundness of the verification method based on trap invariants:
Theorem 1. Given a component-based system S and a WSκS formula ϕ(X), if the
formula
                     ∃X . markingS (X) ∧ trap-invariantS (X) ∧ ¬ϕ(X)               (8)
is unsatisfiable, then for every universe U, the property defined by the formula ϕ(X)
holds in every reachable marking of NSU .
    In the light of the above theorem, verifying the correctness of a component-based
system with any number of active components boils down to deciding the satisfiability
of a WSκS formula. The latter problem is known to be decidable, albeit in general, with
non-elementary recursive complexity. A closer look at the verification conditions of the
form (8) generated by our method suffices to see that the quantifier alternation is finite,
which implies that the time needed to decide the (un)satisfiability of (8) is elementary
recursive. Moreover, our experiments show that these checks are very fast (less than 1
second on an average machine) for a non-trivial set of examples.


4    Refining Trap Invariants
Since the safety verification problem is undecidable for parameterized systems [6], the
verification method based on trap invariants cannot be complete. As an example, con-
sider the alternating dining philosophers system, of which an instance (for n = 3) is
shown in Fig. 3. The system consists of two philosopher component types, namely
Philosopherrl , which takes its right fork before its left fork, and Philosopherlr , tak-
ing the left fork before the right one. Each philosopher has two interaction ports for
taking the forks, namely g` (get left) and gr (get right) and one port for releasing the
forks p (put). The ports of the Philosopherrl component type are overlined, in order
to be distinguished. The Fork component type is the same as in Fig. 1. The interaction
formula for this system Γphilo
                             alt , shown in Fig. 3, implicitly states that only the 0-index

philosopher component is of type Philosopherrl , whereas all other philosophers are of
type Philosopherlr . Note that the interactions on ports g`, gr and p are only allowed if
         def
zero(x) = ∀y . x ≤ y holds, in other words if x is interpreted as the root of the universe
(in our case, 0 since U = {0, . . . , n − 1}).
    It is well-known that any instance of the parameterized alternating dining philoso-
phers system consisting of at least one Philosopherrl and one Philosopherlr is deadlock-
free. However, trap invariants are not enough to prove deadlock freedom, as shown by
the global state {hb, 0i, hh, 0i, hb, 1i, hw, 1i, h f, 2i, he, 2i}, marked with thick red lines in
Fig. 3. Note that no interaction is enabled in this state. Moreover, this state intersects
with any trap of the marked PN that defines the executions of this particular instance, as
proved below. Consequently, the trap invariant contains a deadlock configuration, and
the system cannot be proved deadlock-free by this method.
                                    Fig. 3: Alternating Dining Philosophers

          g(0)                 gr(0) g`(0)        g(1)             gr(1) g`(1)        g(2)               gr(2) g`(2)

         f                     w    getright     f                 w    getleft      f                   w    getleft
                get                                    get                                  get

                                      h                                   h                                     h
       leave                 put               leave             put               leave               put

         b                     e    getleft      b                 e    getright     b                   e    getright

       `(0)                 p(0)                `(1)             p(1)                `(2)             p(2)


      Fork(0)           Philosopherrl (0)      Fork(1)       Philosopherlr (1)     Fork(2)        Philosopherlr (2)

      Γphilo
       alt = zero(x) ∧ [(g`(x) ∧ g(x)) ∨ (gr(x) ∧ g(s(x))) ∨ (p(x) ∧ `(x) ∧ `(s(x)))] ∨
                      ¬zero(x) ∧ [(g`(x) ∧ g(x)) ∨ (gr(x) ∧ g(s(x))) ∨ (p(x) ∧ `(x) ∧ `(s(x)))]

Proposition 1. Consider an instance of the alternating dining philosophers system in
Fig. 3, consisting of components Fork(0), Philosopherrl (0), Fork(1), Philosopherlr (1),
Fork(2) and Philosopherlr (2) placed in a ring, in this order. Then each nonempty trap
of this system contains one of the places hb, 0i, hh, 0i, hb, 1i, hw, 1i, h f, 2i or he, 2i.

    However, the configuration is unreachable by a real execution of the PN, started in
the initial configuration that marks h f, ii and hw, ii, for all i = 0, 1, 2. An intuitive reason
is that, in any reachable configuration, each fork is in state f (ree) only if none of its
neighboring philosophers is in state e(ating). In order to prove deadlock freedom, one
must learn this and other similar constraints. Next, we present a heuristic method for
strengthening the trap invariant, that infers such universal constraints, involving a fixed
set of components.


4.1     One Invariants

As shown by the example above, trap constraints do sometimes fail to prove interesting
properties. Hence, it is desirable to refine the overapproximation of viable markings to
exclude more spurious counterexamples. In order to do so, we consider a special class
of linear invariants, called 1-invariants in the following. Although linear invariants are
not structural and rely on the set of reachable markings of a marked Petri Net, the set of
1-invariants can be sufficiently under-approximated by structural conditions.

Definition 1. Given a marked PN N = ((S , T, E), m0 ), with S = {s1 , . . . , sn }, a vector
a = (a1 , . . . , an ) ∈ {0, 1}n is a 1-invariant of N if and only if, for each reachable marking
m ∈ R(N), we have ni=1 ai · m(si ) = 1.
                             P

   The following lemma states the structural properties that sufficiently define 1-invariants.
However, the opposite is not true: the are 1-invariants not captured by these conditions.
Taking the intersection of this set of 1-invariants defines a weaker invariant, for the net,
which is sound for our verification purposes.

Lemma 3. Given a marked PN N = ((S, T, E), m0 ), a set of places F ⊆ S is a 1-
invariant if the following hold:
            m0 (s) = 1,
      P
 1.
      s∈F
 2. either ||F ∩ • t || = ||F ∩ t• || = k with k ∈ {0, 1} or ||F ∩ • t || > 1 for every t ∈ T .

    We devote the rest of this section to describe WSκS formulae which capture the
structural properties necessary to define 1-invariants as laid down by Lemma 3 (2). As
demonstrated in Section 3 the pre- and postset of transitions, as well as general sets of
places in a PN describing the execution semantics can be defined in WSκS. Hence, we
present the definitions of the following formulae only in the appendix and just give the
intuitions here.
    As before, we fix two tuples of set variables X and X 0 , with one variable X s for each
          SN i
state s ∈ i=1   S and we define the formulae:
  – unique-initS (X) which captures that the set of places induced by an interpretation
     of X uniquely intersects the set of all initial states, and
  – unique-intersectionS (X, X 0 ) which states that the set of places induced by an inter-
     pretation of X and X 0 intersect uniquely.
Given a transition t of the marked Petri Net NSU defining the execution semantics of a
component-based system S, for a universe U, we consider the following formulae:
  – uniquepreCS (X, x1 , . . . , x` ) which describes that the set of places encoded by the in-
     terpretation of X uniquely intersects • t and
  – uniquepostCS (X, x1 , . . . , x` ) which in the same sense captures the unique intersection
     with t• .
Now we define a predicate 1-predS which consists of a conjunction of unique-initS and
the formulae:
                    ∀x1 , . . . , ∀x` . (Tr(ϕ) → [¬ intersects-preCS ∧¬ intersects-postCS
                                                           ∨ uniquepreCS ∧ uniquepostCS           (9)
                                                     ∨ intersects-preCS ∧¬ uniquepreCS ])

one for each clause C in Γ. We show the soundness of this definition, by the following:

Lemma 4. Given a component-based system S = hC1 , . . . , CN , Γi and a tuple of set vari-
ables X, one for each state in a component of S. Then, for any structure (U, ι), such that
ι interprets the variables in X, the set P = {hs, ui ∈ i=1 S × U | u ∈ ι(X s )} is a 1-invariant
                                                      SN i

of NS if (U, ι) |=WSκS 1-predS (X).
      U


    We may now define the 1-invariant analogously to the trap-invariant before:
        1-invariantS (X) = ∀X 0 . 1-predS (X 0 ) → unique-intersectionS (X, X 0 ). (10)
And by analogously reasoning we obtain a refinement of Theorem 1 since every reach-
able marking has to satisfy both invariants.

Theorem 2. Given a component-based system S and a WSκS formula ϕ(X), if the
formula:
           ∃X . markingS (X) ∧ 1-invariantS (X) ∧ trap-invariantS (X) ∧ ¬ϕ(X)    (11)
is unsatisfiable, then for every universe U, the property defined by the formula ϕ(X)
holds in every reachable marking of NSU .
5   Experiments
We have implemented a prototype (called ostrich) of this verification procedure to
evaluate the viability of our approach. All the files and scripts used can be found online6 .
The current version of the prototype can only handle token-ring and pipeline topologies,
but not trees; for these topologies the verification reduces to checking satisfiability of
a formula of WS1S. We have also considered one example with tree-topology (see
below), for which the formula was constructed manually. Satisfiability of WS1S and
WSκS formulae was checked using version 1.4/17 of Mona [30]. We consider various
examples separated in categories:
Cache Coherence: Following [22] we formalized and checked the described safety
    properties and deadlock-freedom of the following cache coherence protocols: Illi-
    nois, Berkeley, Synapse, Firefly, MESI, MOESI, and Dragon.
Mutual Exclusion: We modelled and checked for deadlock-freedom and mutual ex-
    clusion Burns’ [32], Dijkstra’s and Szymanski’s [3] algorithms as well as a formu-
    lation of Dijkstra’s algorithm on a ring structure with token passing [28]. Further-
    more, we check synchronization via a semaphore which is atomically aquired and
    by broadcasting to ensure everyone else is not in the critical section.
Dining Philosophers: This is the classical problem of dining philosophers which all
    take first the right fork and then the left fork. We consider the following “flavors”
    of this problem:
      – there is one philosopher who takes first her left and then her right fork,
      – as above but the forks remember whom took them, and
      – there are two global forks everyone grabs in the same order.
Preemptive Tasks: There are tasks which can be either waiting, ready, executing or
    preempted. Initially one task is executing while all others are waiting. At any point
    a task may become ready and any ready task may preempt the currently executing
    task. Upon finishing the executing task re-enables one preempted task. Here, we
    have additionally two alternatives: Firstly, we consider the case where always the
    agent with highest index resumes execution. Secondly, we let the processes estab-
    lish the initial condition from a position where everyone is waiting.
Dijkstra-Scholten: This is an algorithm that is used to detect termination of distributed
    systems by message passing along a tree [23]. Since the prototype only supports
    linear topologies we can generate the necessary formula automatically only for this
    case.
Herman: This algorithm implements self-stabilizing token passing in rings. The for-
    mulation as well as all following follow [17].
Israeli-Jalfon: This is another self-stabilizing token passing algorithm in rings.
Lehmann-Rabin: This is a randomized solution to the dining philosophers problem.
Dining Cryptographers: This time a group of cryptographers want to determine if
    one of them paid for a meal or a stranger.
   The results are shown in Table 1. The first column reports which properties could
(X) and could not be verified (×) because the conjunction of trap and one-invariant
 6 https://gitlab.lrz.de/i7/ostrich
was not strong enough to prove the given property. For the consistency properties of
cache-coherence protocols we give (x/y) which reads: “from y properties x could be
established”. The following column reports the time (in second) it takes to prove all
considered properties. To understand the next four columns, recall that Mona constructs
for a given formula φ(X) a finite automaton recognizing all the sets X for which ϕ
holds. Since the automata can have very large alphabets, the transition relation of the
automaton is encoded as a binary decision diagram (BDD). The columns report the
sizes of the automata (in the format: number of states / number of nodes of the BDD)
for different formulas. More precisely, the columns trap, trap-inv, flow and flow-inv give
the sizes of the automata for trap-predS ∧ initially-markedS , trap-invariantS , 1-predS
and 1-invariantS respectively. We write “n.a.” (for “not available”) to indicate that Mona
timed out before the automaton was computed.
    The first observation is that the satisfiability checks often can be done in very short
time. This is surprising, because the formulas to be checked, namely (8) and (11), ex-
hibit one quantifier alternation (recall that trap-invariantS and 1-invariantS contain uni-
versal quantifiers). More specifically, since trap-invariantS is obtained by universally
quantifying over trap-predS ∧ initially-markedS , one would expect the automaton for
the former to be much larger than the one for the latter, at least in some cases. But this
does not happen: In fact, the automaton for trap-invariantS is almost always smaller.
Similarly, there is no blowup between 1-predS and 1-invariantS . A possible explanation
could be that the exponential blowup caused by universal quantification in WSκS man-
ifests only on theoretical corner cases, which do not occur in our examples.


6   Conclusions

We have shown that the trap technique used in [11,26,13] for the verification of single
systems can be extended to parameterized systems with sophisticated communication
structures, like pipelines, token rings and trees. Our extension constructs a parame-
terized trap invariant, a formula of WSκS satisfied by the reachable global states of all
instances of the system. The core of the approach is a purely syntactic, automatic deriva-
tion of the trap invariant from the interaction formula describing the possible transitions
of the system. When the set of safe global states can also be expressed in WSκS, which
is usually the case, we check using the Mona tool whether the trap invariant implies
the safety formula. The technique proves correctness of systems that do not produce
well-structured transition systems in the sense of [1,27], and of systems with broadcast
communication, for which, to the best of our knowledge, cut-off results have not been
obtained yet.
    Our experiments demonstrate that trap invariants can be very effective in finding
proofs of correctness (inductive invariants) of common benchmark examples. In prac-
tice, the technique is very cheap, since it avoids costly fixpoint computations. This
suggests incorporating it into other verifiers as a cheap preprocessing step.

Acknowledgements. The work of the second and fifth author has received funding from the
European Research Council (ERC) under the European Union’s Horizon 2020 research and in-
novation programme under grant agreement No 787367 (PaVeS).
                                                        time      trap        trap-inv        flow      flow-inv
       Benchmark                    Properties
                                                         (s.)   #st. / #tr.   #st. / #tr.   #st. / #tr. #st. / #tr.
                             deadlock-freedom       X
Berkeley                                                   0.25 18 / 95       18 / 77    8 / 27           7 / 24
                             consistency properties (1/3)
                             deadlock-freedom       X
Dragon                                                     0.79 39 / 343      32 / 154  10 / 56           9 / 43
                             consistency properties (6/7)
                             deadlock-freedom       X
Firefly                                                    0.43 55 / 400      36 / 212  10 / 47           9 / 36
                             consistency properties (0/4)
                             deadlock-freedom       X
Illinois                                                   0.29 14 / 83       11 / 32    8 / 32           8 / 27
                             consistency properties (2/2)
                             deadlock-freedom       X
MESI                                                       0.23 12 / 58       11 / 35    8 / 27           7 / 24
                             consistency properties (2/2)
                             deadlock-freedom       X
MOESI                                                      0.41 20 / 143      16 / 58    8 / 31           7 / 28
                             consistency properties (7/7)
                             deadlock-freedom       X
Synapse                                                    0.20 12 / 44       11 / 30    8 / 23           7 / 20
                             consistency properties (3/3)
Dijkstra-Scholten            deadlock-freedom X            0.16 13 / 53       11 / 31   10 / 37           9 / 31
                             deadlock-freedom X
Bakery                                                     0.18 10 / 29       10 / 25    8 / 23           7 / 20
                             mutual exclusion X
                             deadlock-freedom X
Burns                                                      0.19 10 / 84        9 / 40    8 / 35           7 / 32
                             mutual exclusion X
                             deadlock-freedom X
Dijkstra                                                  35.68 375 / 13164 106 / 4080 13 / 162          10 / 138
                             mutual exclusion X
                             deadlock-freedom X
Broadcast MutEx                                            0.15    9 / 23      9 / 19    8 / 19           7 / 16
                             mutual exclusion X
                             deadlock-freedom X
Preemptive (high)                                          0.18 41 / 293      17 / 67     3/3              6/8
                             mutual exclusion ×
                             deadlock-freedom X
Preemptive                                                 0.17 28 / 180      22 / 102  18 / 101          12 / 64
                             mutual exclusion X
                             deadlock-freedom X
Preemptive (uninitialized)                                 0.16 20 / 80       11 / 37    8 / 23           7 / 20
                             mutual exclusion ×
                             deadlock-freedom X
Semaphore                                                  0.15 14 / 41        9 / 31   10 / 36           8 / 31
                             mutual exclusion X
                             deadlock-freedom n.a.
Szymanski                                                 36.61     n.a.    495 / 39202  8 / 95           7 / 108
                             mutual exclusion n.a.
                             deadlock-freedom n.a.
Dijkstra (ring)                                           83.46 703 / 9287 1149 / 20455 20 / 244         20 / 346
                             mutual exclusion n.a.
                             deadlock-freedom ×
Dining Cryptographers                                      2.60 250 / 4396 288 / 4145   10 / 78           9 / 87
                             correctness        X
Dining          Philosophers deadlock-freedom X            0.23 32 / 174      19 / 112  15 / 80           11 / 59
(global)
                             deadlock-freedom ×
Herman (linear)                                            0.17 19 / 70       14 / 42   10 / 33           9 / 27
                             no token loss      X
                             deadlock-freedom X
Herman (ring)                                              0.17 19 / 71       14 / 42   10 / 33           9 / 27
                             no token loss      X
                             deadlock-freedom X
Israeli-Jalfon                                             0.17 43 / 185      14 / 40     3/3              6/8
                             no token loss      X
Dining Philosophers (lefty) deadlock-freedom X             0.16 37 / 187      27 / 149  12 / 64           11 / 54
Dining Philosophers (lefty, deadlock-freedom X             0.17 37 / 243      21 / 118  14 / 112          11 / 67
rem. forks)
Lehmann-Rabin                deadlock-freedom X            0.17 39 / 452      23 / 208  11 / 68           11 / 83

             Table 1: Experimental results of a prototype implementation.
7    Proofs from Section 3.1
Lemma 1. Given an ILκ formula φ, for any structure I = (U, ι), we have I |=IL φ ⇐⇒ I |=WSκS
Tr(φ).

Proof : By induction on the structure of φ. Since Tr(.) is homomorphic w.r.t the first-order con-

nectives, the only interesting case is when φ is succi (x) = y.
(⇒) If (U, ι) |=IL succi (x) = y then σi (ι(x)) = ι(y) and we distinguish two cases:
  – if ι(x) is not a maximal element of U, then σi (ι(x)) = ξi (ι(x)), hence (U, ι) |=WSκS ¬ max(x) ∧
     succi (x) = y,
  – else, ι(x) is a maximal element of U, we have ξi (ι(x)) = , hence (U, ι) |=WSκS max(x) ∧ y = .
In each case, we obtain (U, ι) |=WSκS Tr(succi (x) = y).
(⇐) Since (U, ι) |=WSκS Tr(succi (x) = y), we have two cases:
  – if (U, ι) |=WSκS ¬ max(x) ∧ succi (x) = y then ι(x) is not a maximal element of U and ξi (ι(x)) =
    ι(y), thus σi (ι(x)) = ι(y) and (U, ι) |=WSκS succi (x) = y.
  – else (U, ι) |=WSκS max(x) ∧ y =  and ι(x) is a maximal element of U. In this case we have
    σi (ι(x)) =  = ι(y), hence (U, ι) |=IL succi (x) = y.                                          t
                                                                                                    u


8    Proofs from Section 3.2
Lemma 2. Given a component-based system S = hC1 , . . . , CN , Γi and a structure I = (U, ι), where
ι is an interpretation of the set variables X, the set P = {hs, ui ∈ k=1 Sk × U | u ∈ ι(X s )} is a trap
                                                                    SN

of NS if and only if (U, ι) |=WSκS trap-predS (X).
     U


Proof : Central to our analysis of NU
                                    S
                                      = (S , T, E) is the following fact:


Fact 1 For any transition t ∈ T exists a clause

                C(x1 , . . . , x` ) = ∃ . ϕ ∧ `j=1 p j (x j ) ∧ `+m
                                                                 j=`+1 ∀x j . ψ j → p j (x j )
                                             V                 V

in Γ and values u1 , . . . , u` ∈ U such that:

       hU, ι[x1 ← u1 , . . . , x` ← u` ]i |=IL ϕ,

       • t = {hs, ui | u ∈ Ψ
                               j and s =        j for some ` + 1 ≤ j ≤ ` + m} ∪ {h p1 , u1 i, . . . , h p` , u` i}
                                           •p                                     •                    •


       t• = {hs, ui | u ∈ Ψ j and s = p j • for some ` + 1 ≤ j ≤ ` + m} ∪ {hp1 • , u1 i, . . . , hp` • , u` i}
           def
where Ψ j = {u ∈ U | hU, ν[x j ← u], ∅i |=IL ψ j } for ` + 1 ≤ j ≤ ` + m. Dually, for a fixed clause C in
Γ and a tuple of values u = hu1 , . . . , u` i such that hU, ι[x1 ← u1 , . . . , x` ← u` ]i |=IL ϕ there exists a
unique transition t ∈ T with • t and t• as above, denoted hC, ui.

Proof :    By the definition of NU
                                 S
                                   , for any t ∈ T there exists a clause C of Γ of the form (5)

and a minimal model I = hU, ιi of C. Hence, there are values u1 ∈ ι(p1 ), . . . , u` ∈ ι(p` ) such that
hU, ι[x1 ← u1 , . . . , x` ← u` ]i |=IL ϕ. By the minimality of I, u1 , . . . , u` are the only elements of
ι(p1 ), . . . , ι(p` ), respectively. Moreover, for every ` + 1 ≤ j ≤ ` + m and u ∈ Ψ j , we have u ∈ ι(p j )
and nothing else is in ι(p j ). By the definition of NU   S
                                                            , we obtain • t and t• as stated above.
   For the dual direction, we fix C in Γ and u1 , . . . , u` such that hU, ι[x1 ← u1 , . . . , x` ← u` ]i |=IL ϕ.
The structure I = (U, ι), where:
                                    ι(x j ) = u j and ι(p j ) = {u j }, for all 1 ≤ j ≤ `
                                    ι(p j ) = Ψ j , for all ` + 1 ≤ j ≤ ` + m
is a minimal model of C and uniquely determines t ∈ T with the above properties.                                     t
                                                                                                                     u
       Next, we prove the following points:
  1. P ∩ • hC, ι(x1 ), . . . , ι(x` )i , ∅ ⇐⇒ (U, ι) |=WSκS intersects-preCS (X, x1 , . . . , x` ):
        “⇒” If P ∩ • hC, ι(x1 ), . . . , ι(x` )i , ∅, then we have two cases:
             – if h• pi , ι(xi )i ∈ P, for some 1 ≤ i ≤ `, then by the definition of P, we obtain ι(xi ) ∈ ι(X• pi )
                and therefore (U, ι) |=WSκS X• pi (xi ),
             – else h• p j , ui ∈ P, for one ` + 1 ≤ j ≤ ` + m, leading to u ∈ Ψ j . But then (U, ι[x j ← u]) |=IL
                ψ j , hence (U, ι[x j ← u]) |=WSκS Tr(ψ j ), by Lemma 1. Since also (U, ι[x j ← u]) |=WSκS
                X• p j (x j ), by a similar argument as before, we obtain (U, ι) |=WSκS ∃x j . Tr(ψ j )∧ X• p j (x j ).
        “⇐” If (U, ι) |=WSκS intersects-preCS (X, x1 , . . . , x` ) then one of the following holds:
             – if (U, ι) |=WSκS X• pi (xi ) for some 1 ≤ i ≤ `, then, by the definition of P and Fact 1, we
                obtain h• pi , ν(xi )i ∈ P ∩ • hC, ι(x1 ), . . . , ι(x` )i.
             – else (U, ι) |=WSκS ∃x j . Tr(ψ j ) ∧ X• p j (x j ) for some ` + 1 ≤ j ≤ ` + m, leading to the ex-
                istence of a node u j ∈ U such that (U, ι[x j ← u j ]) |=WSκS Tr(ψ j ) ∧ X• p j (x j ) which, by
                Lemma 1, yields (U, ι[x j ← c j ]) |=IL ψ j ∧ X• p j (x j ). This in turn leads to u j ∈ Ψ j and
                therefore h• p j , u j i ∈ P ∩ • hC, ι(x1 ), . . . , ι(x` )i.
  2. P ∩ hC, ι(x1 ), . . . , ι(x` )i• , ∅ ⇐⇒ (U, ι) |=WSκS intersects-postCS (X, x1 , . . . , x` )
        This case is proved using a similar argument as (1) above.
Back to the main proof, we need to show that P is a trap in NU                S
                                                                                 ⇐⇒ (U, ι) |=WSκS trap-predS (X).
“⇒” Consider the case where (U, ι) 6|=WSκS trap-predS . Hence, there is a clause C and nodes
u1 , . . . , u` ∈ U such that (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS Tr(ϕ) thus, by Lemma 1, (U, ι[x1 ←
u1 , . . . , x` ← u` ]) |=IL ϕ, and (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS intersects-preCS , whereas (U, ι[x1 ←
u1 , . . . , x` ← u` ]) 6|=WSκS intersects-postCS . From 1 and 2, we conclude that P ∩ • hC, ι(x1 ), . . . , ι(x` )i ,
∅, whereas P ∩ hC, ι(x1 ), . . . , ι(x` )i• = ∅. But then, P is not a trap of NU       S
                                                                                         , because t ∈ • P, whereas
t < P• .
“⇐” Assume that (U, ι) |=WSκS trap-predS and let t ∈ P• be a transition. By Fact 1, there is a clause
C and nodes u = hu1 , . . . , u` i ∈ U, such that t = hC, ui. Then, we have (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=IL
ϕ, hence (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS Tr(ϕ), by Lemma 1. Since t ∈ P• , we have P ∩ • t , ∅,
thus (U, ι[x1 ← u1 , . . . , x` ← u` ) |=WSκS intersects-preCS , by (1). Because (U, ι) |=WSκS trap-predS , we
also obtain that (U, ι[x1 ← u1 , . . . , x` ← u` ) |=WSκS intersects-postCS , thus P ∩ t• , ∅, by (2). This
leads to t ∈ • P, and since the choice of t was arbitrary, we obtain P• ⊆ • P, as required.                          t
                                                                                                                     u
Theorem 1. Given a component-based system S and a WSκS formula ϕ(X), if the formula
                                  ∃X . markingS (X) ∧ trap-invariantS (X) ∧ ¬ϕ(X)                                  (8)
is unsatisfiable, then for every universe U, the property defined by the formula ϕ(X) holds in every
reachable marking of NSU .

Proof : Let (U, ι) be a structure, such that ι interprets X and X 0 and let m be a marking of NU
                                                                                               S
                                                                                                 . We

define the sets:
              def                                           def
           Gι = {hs, ui ∈ i=1  S × U | u ∈ ι(X s )} and G0ι = {hs, ui ∈ i=1 S × U | u ∈ ι(X s0 )}
                         SK i                                          SK i
               def                             def
           Gm = S               s where G s = {u ∈ U | m(hs, ui) = 1}
                     S
                         {s} × Gm            m
                        K     i
                   s∈   i=1 S
and note the following points (the proofs of which are easy checks left to the reader):

(a) for any marking m of NU
                          S
                            if ι(X s ) = Gm
                                          s then (U, ι) |=
                                                           WSκS markingS (X),

(b) (U, ι) |=WSκS intersectionS (X, X 0 ) ⇐⇒ Gι ∩ G0ι , ∅, and
(c) if m0 is the initial marking of NSU , then

                           (U, ι) |=WSκS initially-markedS (X) ⇐⇒ Gι ∩ Gm0 , ∅.

With (c) and Lemma 2 we conclude that (U, ι) |=WSκS trap-predS (X 0 )∧initially-markedS (X 0 ) if and
only if G0ι is a IMT. Which yields using (b) that (U, ι) |=WSκS trap-invariantS if and only if Gι in-
tersects all IMTs. Hence, if there is a marking m ∈ R(NSU ) such that (U, ι[X s ← Gms ]    K Si ) |=WSκS
                                                                                        s∈∪i=1
¬ϕ, i.e. Gm “violates” ϕ, then by (a), we obtain:

             (U, ι[X s ← Gm
                          s
                            ] s∈∪K Si |=WSκS markingS (X) ∧ trap-invariantS (X) ∧ ¬ϕ(X).
                                   i=1


The proof follows by contraposition.                                                                           t
                                                                                                               u



9    Proofs from Section 4

Proposition 1. Consider an instance of the alternating dining philosophers system in Fig. 3, con-
sisting of components Fork(0), Philosopherrl (0), Fork(1), Philosopherlr (1), Fork(2) and Philosopherlr (2)
placed in a ring, in this order. Then each nonempty trap of this system contains one of the places
hb, 0i, hh, 0i, hb, 1i, hw, 1i, h f, 2i or he, 2i.

Proof : Let C = {hb, 0i, hh, 0i, hb, 1i, hw, 1i, h f, 2i, he, 2i} in the following. We shall try to build a

nonempty trap T that avoids every state in C. If such a trap can be found, the counterexample is
shown to be spurious (unreachable). Below is the list of states allowed in T , indexed by compo-
nent (using other states that the ones listed below would result in a trap that is satisfied by the
counterexample C, which is exactly the opposite of what we want):


          Fork(0) Philosopherrl (0) Fork(1) Philosopherlr (1) Fork(2) Philosopherlr (2)
            h f, 0i    hw, 0i, he, 0i     h f, 1i     hh, 1i, he, 1i     hb, 2i      hw, 2i, hh, 2i

    Assume that h f, 0i ∈ T . Then T must contain hb, 0i or he, 2i (constraint gr(2) ∧ g(0)). However
neither is allowed, thus h f, 0i < T . Assume that h f, 1i ∈ T . Then T must contain hb, 1i or hh, 0i
(constraint gr(0) ∧ g(1)), contradiction, thus h f, 1i < T . Assume that hb, 2i ∈ T . Then T must
contain h f, 1i, hw, 1i or h f, 2i (constraint p(1) ∧ `(1) ∧ `(2)), contradiction, thus hb, 2i < T . Then T
contains only philosopher states, except for hh, 0i, hw, 1i and he, 2i. One can prove that there is no
such trap, for instance, for Philosopherlr (1) we have:

                                          hh, 1i ∈ T ⇒ he, 1i ∈ T
                                          he, 1i ∈ T ⇒ hw, 1i ∈ T

since h f, 1i, hb, 1i, h f, 2i, hb, 2i < T . Since hw, 1i < T , we obtain that hh, 1i, he, 1i < T . Then the only
possibility is T = ∅.                                                                                          t
                                                                                                               u
10         Missing Material from Section 4.1
Lemma 3. Given a marked PN N = ((S, T, E), m0 ), a set of places F ⊆ S is a 1-invariant if the
following hold:
        m0 (s) = 1,
     P
  1.
         s∈F
 2. either ||F ∩ • t || = ||F ∩ t• || = k with k ∈ {0, 1} or ||F ∩ • t || > 1 for every t ∈ T .
                                                                                  m(s) = 1 for every marking
                                                                               P
Proof : A simple inductive argument allows to prove the invariant
                                                                                          s∈F

m ∈ R(N) while additionally maintaining that any transition t such that ||W ∩ • t || > 1 cannot be
fired.                                                                                            t
                                                                                                  u
     In the following we give the missing formulae and auxiliaries from Section 4.1 for the case
that the preset of a transition is considered. The case of a postset is completely analogous. We let
x denote a vector x := (x1 , . . . , x` ).

                                                                                !       "             #
                                                                 o,c
           unique-initS (X) = ∃x .                                       ¬X s0 o ∧ ∀y .     X s0 c (y) → x = y
                                         W                       V                        W
                                                 X s0 c (x) ∧
                                       1≤c≤K                    1≤o≤K                       1≤c≤K
                                                                                                                
unique-intersectionS (X, X 0 ) = ∃x .                (Xq (x) ∧ Xq0 (x)) ∧                ¬(X p (x) ∧ X 0p (x))
                                          W                                  V                                
                                                 c
                                                     
                                      q∈∪1≤c≤K S                                    c
                                                                         p∈∪1≤c≤K S \{q}             
                                                                ∧∀y .            Xq (y) ∧ Xq0 (y) → x = y
                                                                         W                          
                                                                                       q∈∪1≤c≤K Sc

                                                                poV                        =pi
                                                                                         poV
                                                                  ,pi
                                                                                                                         !
          unique-pre-exCS (X, x) =                                                               X• po (xo ) → xi = xo
                                        W
                                               X• pi (xi ) ∧            ¬X• po (xo ) ∧
                                       1≤i≤`                   1≤o≤`                     1≤o≤`
                                                                                     h                      i
                       disjoint-pre-broadcastCS (X, x) = ∀y .                         ψ(x, y) → ¬X• p j (y)
                                                                           V
                                                                        `+1≤ j≤`+m

                                      disjoint-pre-exCS (X, x) =
                                                                           V
                                                                                 ¬X• pi (xi )
                                                                         1≤i≤`
                                                                                
                       unique-pre-broadcastCS (X, x) =                    ∃x j . ψ j (x, x j ) ∧ X• p j (x j )
                                                                   W
                                                               `+1≤ j≤`+m
                                                                       h                                     i
                                                                ∧∀y . ψ j (x, y) ∧ X• p j (y) → y = x j
                                                                      o,
                                                                      Vj h                                i
                                                                ∧             ψo (x, y) → ¬X• po (y)
                                                                  `+1≤o≤`+m
                                                                                                
                                        unique-pre-exCS (X, x) ∧ disjoint-pre-broadcastCS (X, x) ∨
                   uniquepreS (X, x) =
                            C                                                                   
                                        unique-pre-broadcastCS (X, x) ∧ disjoint-pre-exCS (X, x)

Lemma 4. Given a component-based system S = hC1 , . . . , CN , Γi and a tuple of set variables X,
one for each state in a component of S. Then, for any structure (U, ι), such that ι interprets the
variables in X, the set P = {hs, ui ∈ i=1 S × U | u ∈ ι(X s )} is a 1-invariant of NSU if (U, ι) |=WSκS
                                     SN i

1-predS (X).
Proof : We begin by formulating some auxilliary statements. For this we fix a clause C(x1 , . . . , x` )

in Γ and values u1 , . . . , u` such that (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=IL ϕ and by Fact 1 we get a
corresponding transition t. We separate • t and t• into its existential and universal part, i.e.
               •      •        •                                             •
     •
         t = t∃ ∪ t∀ with t∃ = {h• p1 , c1 i, . . . , h• p` , c` i} and t∀ = {{• p j } × Ψ j : ` + 1 ≤ j ≤ ` + m}.
                                •      •
W.l.o.g. we assume that t∃ ∩ t∀ = ∅ and moreover ||{p j : ` + 1 ≤ j ≤ ` + m}|| = m. This is achieved
by two steps. Namely, if there are two broadcasts
            ∀x j1 . ϕ j1 (x1 , . . . , x` , x j1 ) → p j1 (x j1 ) and ∀x j2 . ϕ j2 (x1 , . . . , x` , x j2 ) → p j2 (x j2 )
such that p j1 = p j2 = p then we replace these by one broadcast7
                            ∀x j . (ϕ j1 (x1 , . . . , x` , x j ) ∨ ϕ j2 (x1 , . . . , x` , x j )) → p(x j ).
Moreover, if there is 1 ≤ i ≤ ` with an atom pi (xi ) in C and a broadcast
                                                      ∀x j . ϕ j → p j (x j )
such that pi = p j then we replace the broadcast8 with
                                              ∀x j . (ϕ j ∧ x j , xi ) → p j (x j ).
This allows that there is for every port precisely one broadcast term and no broadcast “shadows”
an atom of a free variable in C.
    Our proof relies on the following observations:
(a) ||T ι ∩ {{s0 k } × U : 1 ≤ k ≤ K}|| = 1 ⇐⇒ (U, ι) |=WSκS unique-initS ,
            •
(b) ||T ι ∩ t∃ || = 1 ⇐⇒ (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS unique-pre-exCS ,
            • ∀
(c) ||T ι ∩ t || = 1 ⇐⇒ (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS unique-pre-broadcastCS ,
            •
(d) ||T ι ∩ t∃ || = 0 ⇐⇒ (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS disjoint-pre-exCS and
            • ∀
(e) ||T ι ∩ t || = 0 ⇐⇒ (U, ι[x1 ← u1 , . . . , x` ← u` ]) |=WSκS disjoint-pre-broadcastCS .
Since the line of reasoning can be easily adapted for the different cases we restrict our arguments
to (c) since it is the most elaborate formula.
                                                                                                      •
ad (c) “⇒”: Fix j ∈ {` +1, . . . , ` +m} such that q = • p j , and u j ∈ Ψ j with {hq, u j i} = T ι ∩ t∀ . Hence,
by definition of T ι , u j ∈ ι(Xq ) and therefore (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j ]) |=WSκS Xq (x j ),
while, by definition of Ψ j and Lemma 1, (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j ]) |=WSκS Tr(ψ j ). For
any fixed uy ∈ ∪`+1≤k≤`+m Ψk we distinguish different cases:                                         h                                                 i
     If uy = u j , we immediately have (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) |=WSκS ψ j (x1 , . . . , x` , y) ∧ X• p j (y) → y = x j
and, by pairwise disjointness of all Ψn for ` + 1 ≤ n ≤ ` + m, we get
                                                                                 o, j
                                                                                 ^            h                                        i
   (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) |=WSκS                                 ψo (x1 , . . . , x` , y) → ¬X• po (y)
                                                                            `+1≤o≤`+m

since (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) 6|=WSκS ψo (x1 , . . . , x` , y) for any o , j.
       If on the other hand, uy ∈ Ψk for k , j then we have by definiton of Ψk that (U, ι[x1 ←
u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) |=WSκS Tr(ψk ), however by pairwise disjointness of all Ψn for
` + 1 ≤ n ≤ ` + m we have (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) 6|=WSκS Tr(ψn ) for any ` + 1 ≤
n ≤ ` + m different from k and (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) 6|=WSκS X• pk (y) because
                                    •
otherwise h• pk , uy i ∈ T ι ∩ t∃ . This gives in combination (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ←
uy ]) |=WSκS `+1≤n≤`+m ψn → ¬X• pn (y) which already implies
                V

     (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) |=WSκS
              h                                                i    o,
                                                                    Vj                   h                                           i
               ψ j (x1 , . . . , x` , y) ∧ X• p j (y) → y = x j ∧                            ψo (x1 , . . . , x` , y) → ¬X• po (y)
                                                                         `+1≤o≤`+m

 7 Note that this is not a valid broadcast in the sense of clauses, however in the translation into

   WSκS we can incorporate these changes.
 8 This actually is a valid broadcast.
       Thirdly, consider the case that uy ∈ Ψ j but uy , u j . Again by pairwise disjointness of all Ψn
for ` + 1 ≤ n ≤ ` + m we have (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) 6|=WSκS Tr(ψn ) for any
                                                         •                                      •
n different from j. However, since hq, cy i ∈ t∀ it cannot be in T ι since it is in t∃ which gives
uy < ι(X• p j ) and therefore (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u j , y ← uy ]) |=WSκS ¬Xq (y).
       Concludingly, we may use u j as the witness for the existential quantification and get (U, ι[x1 ←
u1 , . . . , x` ← u` ]) |=WSκS unique-pre-broadcastCS .
                                                   •
ad (c) “⇐”: Consider the case that T ι ∩ t∀ = ∅, then for all u j ∈ Ψ j holds (U, ι[x1 ← u1 , . . . , x` ←
u` , x j ← u j ]) 6|=WSκS X• p j (x j ) since u j < ι(X• p j ) for all ` + 1 ≤ j ≤ ` + m. Moreover, (U, ι[x1 ←
u1 , . . . , x` ← u` , x j ← u j ]) |=WSκS ¬Tr(ψn ) for all ` + 1 ≤ n ≤ ` + m different from j for all ` + 1 ≤ j ≤
` +m ( again by pairwise disjointness). This specifically yields (U, ι[x1 ← u1 , . . . , x` ← u` ], ι) |=WSκS
                 ∃x j . ψ j ∧ X• p j (x j ).
          W
¬
  `+1≤ j≤`+m
                                    •                                                               •
    If on the other hand ||T ι ∩ t∀ || > 1 then we can fix an arbitrary hq1 , u1 i ∈ T ι ∩ t∀ with u1 ∈ Ψ j1
for ` + 1 ≤ j1 ≤ ` + m. Hence, (U, ι[x1 ← u1 , . . . , x` ← u` , x j1 ← u1 ]) |=WSκS Tr(ψ j1 ) ∧ Xq1 (x j1 ).
                                                               •
However, we always have a different hq2 , u2 i ∈ T ι ∩ t∀ such that u2 ∈ Ψ j2 with ` + 1 ≤ j2 ≤ ` + m.
Then, if j1 = j2 = j we get q1 = q2 = p j and therefore (U, ι[x1 ← u1 , . . . , x` ← u` , y ← u2 ]) |=WSκS
                                                  •

Tr(ψ j (x1 , . . . , x` , y)) ∧ X• p j (y). Since u1 , u2 we have (U, ι[x1 ← u1 , . . . , x` ← u` , x j ← u1 ]) 6|=WSκS
     h                                               i
∀y . ψ j (x1 , . . . , x` , y) ∧ X• p j (y) → y = x j .
    If on the other hand j1 , j2 then
                                                                       h                                          i
        (U, ι[x1 ← u1 , . . . , x` ← u` , x j1 ← u1 , y ← u2 ]) 6|=WSκS ψ j2 (x1 , . . . , x` , y) → ¬X• p j2 (y)

and consequently
                                                               o,
                                                               ^j1            h                                    i
    (U, ι[x1 ← u1 , . . . , x` ← u` , x j1 ← u1 ]) 6|=WSκS               ∀y . ψo (x1 , . . . , x` , y) → ¬X• po (y) .
                                                             `+1≤o≤`+m

      However, for any value u ∈ U such that (U, ν[x1 ← u1 , . . . , x` ← u` , x j ← u]) |=WSκS ψ j (x1 , . . . , x` , x j )∧
                                                                                       •
X• p j (x j ) for one ` + 1 ≤ j ≤ ` + m it is easy to see from the definitions of t∀ and T ι that h• p j , ci ∈
• ∀
 t ∩T ι . This concludes then that hU, ν[x1 ← c1 , . . . , x` ← c` , x j ← c1 ], ιi 6|=WSκS unique-pre-broadcastCS
because any choice for the existential quantification of x does not allow for all values chosen for
y to satisfy the formula as demonstrated above.
      In consequence, the statements (a) - (e) show that the given formulae model the properties
laid out in Lemma 3 and therefore the lemma follows.                                                               t
                                                                                                                   u

Theorem 2. Given a component-based system S and a WSκS formula ϕ(X), if the formula:

                  ∃X . markingS (X) ∧ 1-invariantS (X) ∧ trap-invariantS (X) ∧ ¬ϕ(X)                               (11)

is unsatisfiable, then for every universe U, the property defined by the formula ϕ(X) holds in every
reachable marking of NSU .

Proof : In the light of Theorem 1, it is sufficient to prove the theorem for the formula:


                               ∃X . markingS (X) ∧ 1-invariantS (X) ∧ ¬ϕ(X)                                        (12)

The proof goes along the lines of the proof of Theorem 1, with the additional observation:

                       (U, ι) |=WSκS unique-intersectionS (X, X 0 ) ⇐⇒ ||Gι ∩ G0ι || = 1

                                                                                                                        t
                                                                                                                        u
References

 1. Abdulla, P.A., Cerans, K., Jonsson, B., Tsay, Y.: General decidability theorems for infinite-
    state systems. In: LICS. pp. 313–321. IEEE Computer Society (1996)
 2. Abdulla, P.A., Delzanno, G., Henda, N.B., Rezine, A.: Regular model checking without
    transducers (on efficient verification of parameterized systems). In: Grumberg, O., Huth,
    M. (eds.) Tools and Algorithms for the Construction and Analysis of Systems. pp. 721–736
    (2007)
 3. Abdulla, P.A., Haziza, F., Holı́k, L.: Parameterized verification through view abstraction.
    STTT 18(5), 495–516 (2016)
 4. Alberti, F., Ghilardi, S., Sharygina, N.: A framework for the verification of parameterized
    infinite-state systems. CEUR Workshop Proceedings 1195, 302–308 (01 2014)
 5. Aminof, B., Kotek, T., Rubin, S., Spegni, F., Veith, H.: Parameterized model checking of
    rendezvous systems. Distributed Computing 31(3), 187–222 (Jun 2018)
 6. Apt, K.R., Kozen, D.C.: Limits for automatic verification of finite-state concurrent systems.
    Information Processing Letters 22(6), 307 – 309 (1986)
 7. Außerlechner, S., Jacobs, S., Khalimov, A.: Tight cutoffs for guarded protocols with fairness.
    In: VMCAI. Lecture Notes in Computer Science, vol. 9583, pp. 476–494. Springer (2016)
 8. Barkaoui, K., Lemaire, B.: An effective characterization of minimal deadlocks and traps in
    Petri nets based on graph theory. In: 10th Int. Conf. on Application and Theory of Petri Nets
    ICATPN’89. pp. 1–21 (1989)
 9. Basu, A., Bensalem, S., Bozga, M., Combaz, J., Jaber, M., Nguyen, T., Sifakis, J.: Rigor-
    ous component-based system design using the BIP framework. IEEE Software 28(3), 41–48
    (2011)
10. Baukus, K., Bensalem, S., Lakhnech, Y., Stahl, K.: Abstracting WS1S systems to verify
    parameterized networks. In: Graf, S., Schwartzbach, M. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems. pp. 188–203 (2000)
11. Bensalem, S., Bozga, M., Nguyen, T., Sifakis, J.: D-Finder: A tool for compositional dead-
    lock detection and verification. In: CAV’09 Proceedings. LNCS, vol. 5643, pp. 614–619
    (2009)
12. Bloem, R., Jacobs, S., Khalimov, A., Konnov, I., Rubin, S., Veith, H., Widder, J.: Decidability
    of Parameterized Verification. Synthesis Lectures on Distributed Computing Theory, Morgan
    & Claypool Publishers (2015)
13. Blondin, M., Finkel, A., Haase, C., Haddad, S.: Approaching the coverability problem con-
    tinuously. In: TACAS. Lecture Notes in Computer Science, vol. 9636, pp. 480–496. Springer
    (2016)
14. Bouajjani, A., Habermehl, P., Vojnar, T.: Abstract regular model checking. In: Alur, R., Peled,
    D.A. (eds.) Computer Aided Verification. pp. 372–386 (2004)
15. Bozga, M., Iosif, R., Sifakis, J.: Checking deadlock-freedom of parametric component-based
    systems. In: 25th Intl. Conf. on Tools and Algorithms for the Construction and Analysis of
    Systems (TACAS). (2019)
16. Browne, M., Clarke, E., Grumberg, O.: Reasoning about networks with many identical finite
    state processes. Information and Computation 81(1), 13 – 31 (1989)
17. Chen, Y., Hong, C., Lin, A.W., Rümmer, P.: Learning to prove safety over parameterised
    concurrent systems. In: 2017 Formal Methods in Computer Aided Design, FMCAD 2017,
    Vienna, Austria, October 2-6, 2017. pp. 76–83 (2017)
18. Clarke, E., Talupur, M., Veith, H.: Environment abstraction for parameterized verification.
    In: Emerson, E.A., Namjoshi, K.S. (eds.) Verification, Model Checking, and Abstract Inter-
    pretation. pp. 126–141 (2006)
19. Conchon, S., Goel, A., Krstić, S., Mebsout, A., Zaı̈di, F.: Cubicle: A parallel SMT-based
    model checker for parameterized systems. In: Madhusudan, P., Seshia, S.A. (eds.) Computer
    Aided Verification. pp. 718–724 (2012)
20. Cousot, P., Cousot, R.: Systematic design of program analysis frameworks. In: Conference
    Record of the Sixth Annual ACM SIGPLAN-SIGACT Symposium on Principles of Pro-
    gramming Languages. pp. 269–282. ACM Press, New York, NY, San Antonio, Texas (1979)
21. Dams, D., Lakhnech, Y., Steffen, M.: Iterating transducers. The Journal of Logic and Alge-
    braic Programming 52-53, 109 – 127 (2002)
22. Delzanno, G.: Automatic verification of parameterized cache coherence protocols. In: Com-
    puter Aided Verification, 12th International Conference, CAV 2000, Chicago, IL, USA, July
    15-19, 2000, Proceedings. pp. 53–68 (2000)
23. Dijkstra, E.W., Scholten, C.S.: Termination detection for diffusing computations. Inf. Pro-
    cess. Lett. 11(1), 1–4 (1980)
24. Emerson, E.A., Kahlon, V.: Reducing model checking of the many to the few. In: CADE.
    Lecture Notes in Computer Science, vol. 1831, pp. 236–254. Springer (2000)
25. Emerson, E.A., Namjoshi, K.S.: Reasoning about rings. In: POPL’95 Proceedings. pp. 85–94
    (1995)
26. Esparza, J., Ledesma-Garza, R., Majumdar, R., Meyer, P.J., Niksic, F.: An smt-based ap-
    proach to coverability analysis. In: CAV. Lecture Notes in Computer Science, vol. 8559, pp.
    603–619. Springer (2014)
27. Finkel, A., Schnoebelen, P.: Well-structured transition systems everywhere! Theor. Comput.
    Sci. 256(1-2), 63–92 (2001)
28. Fribourg, L., Olsén, H.: Reachability sets of parameterized rings as regular languages. Electr.
    Notes Theor. Comput. Sci. 9, 40 (1997)
29. German, S.M., Sistla, A.P.: Reasoning about systems with many processes. J. ACM 39(3),
    675–735 (1992)
30. Henriksen, J., Jensen, J., Jørgensen, M., Klarlund, N., Paige, B., Rauhe, T., Sandholm, A.:
    Mona: Monadic second-order logic in practice. In: Tools and Algorithms for the Construction
    and Analysis of Systems, First International Workshop, TACAS ’95, LNCS 1019 (1995)
31. Jacobs, S., Sakr, M.: Analyzing guarded protocols: Better cutoffs, more systems, more
    expressivity. In: VMCAI. Lecture Notes in Computer Science, vol. 10747, pp. 247–268.
    Springer (2018)
32. Jensen, H.E., Lynch, N.A.: A proof of Burns n-process mutual exclusion algorithm using
    abstraction. In: TACAS (1998)
33. Kesten, Y., Maler, O., Marcus, M., Pnueli, A., Shahar, E.: Symbolic model checking with
    rich assertional languages. Theoretical Computer Science 256(1), 93 – 112 (2001)
34. Khoussainov, B., Nerode, A.: Automata Theory and Its Applications. Birkhauser Boston,
    Inc. (2001)
35. Pnueli, A., Ruah, S., Zuck, L.: Automatic deductive verification with invisible invariants.
    In: Margaria, T., Yi, W. (eds.) Tools and Algorithms for the Construction and Analysis of
    Systems. pp. 82–97 (2001)
36. Sifakis, J.: Structural properties of petri nets. In: Winkowski, J. (ed.) Mathematical Founda-
    tions of Computer Science 1978. pp. 474–483 (1978)
