                                           Finite Model Finding for Parameterized Verification

                                                                                 Alexei Lisitsa

                                                                      Department of Computer Science
                                                                        University of Liverpool, UK
arXiv:1011.0447v2 [cs.LO] 26 Nov 2010




                                                                     A.Lisitsa@liverpool.ac.uk



                                               Abstract. In this paper we investigate to what extent a very simple and natural
                                               ”reachability as deducibility” approach, originating in research on formal meth-
                                               ods for security, is applicable to the automated verification of large classes of
                                               infinite state and parameterized systems. This approach is based on modeling the
                                               reachability between (parameterized) states as deducibility between suitable en-
                                               codings of states by formulas of first-order predicate logic. The verification of
                                               a safety property is reduced to the purely logical problem of finding a counter-
                                               model for a first-order formula. This task is then delegated then to generic auto-
                                               mated finite model building procedures. In this paper we first establish the relative
                                               completeness of the finite countermodel finding method (FCM) for a class of pa-
                                               rameterized linear arrays of finite automata. The method is shown to be at least as
                                               powerful as known methods based on monotonic abstraction and symbolic back-
                                               ward reachability. Further, we extend the relative completeness of the approach
                                               and show that it can solve all safety verification problems which can be solved by
                                               regular model checking.


                                        1 Introduction
                                        The verification of infinite state systems and parameterized systems is, in general, an
                                        undecidable algorithmic problem. That means the search for efficient procedures to
                                        tackle the larger and larger subclasses of verification tasks will never end. In this paper
                                        we investigate to what extent a very simple and natural ”reachability as deducibility”
                                        approach is applicable to the verification such systems. Consider an encoding e : s 7→
                                        ϕs of states of a transition system S = hS, →i by formulae of first-order predicate
                                        logic satisfying the following property. The state s′ is reachable from s, i.e. s →∗ s′
                                        if and only if ϕs′ is the logical consequence of ϕs , that is ϕs |= ϕs′ or ϕs ⊢ ϕs′ .
                                        Under such assumptions establishing reachability amounts to theorem proving, while
                                        deciding non-reachability, becomes theorem disproving. To verify a safety property,
                                        i.e non-reachability of unsafe states, it is sufficient to disprove a formula of the form
                                        φ → ψ. Also, in the case of safety verification already half of the assumption on the
                                        encoding is suffcient: (s →∗ s′ ) ⇒ (ϕs ⊢ ϕs′ ). The task of disproving can be delegated
                                        then to generic model finding procedures for first-order predicate logic [5].
                                            Such an approach to verification originated within research on formal methods for
                                        the analysis of cryptographic protocols [23,22,11,15]. Being unaware of these develop-
                                        ments in the verification of cryptographic protocols and coming from a different per-
                                        spective we re-invented the finite countermodel finding approach and applied it in a
                                        different context of verification of parameterized and infinite state systems [17,18,19].
     We show in [19] that the parallel composition of a complete finite model finder and
a complete theorem prover provides a decision procedure for safety properties of lossy
channel systems [3] under appropriate encoding. Using a finite model finder, Mace4,
[20] coupled with a theorem prover Prover9 [20] we successfully applied the method to
the verification of alternating bit protocol, specified within a lossy channel system; all
parameterized cache coherence protocols from [7]; series of coverability and reachabil-
ity tasks conserning Petri Nets; parameterized Dining Philosophers Problem (DPP) and
to parameterized linear systems (arrays) of finite automata.
     Despite the wide range of parameterized verification tasks being tackled success-
fully by the method, the only result concerning completeness presented so far is that on
the verification of lossy channel systems [19]. The aim of this paper is to investigate fur-
ther the completeness of the finite countermodel finding method for much larger classes
of parameterized verification tasks. Note that we focus here on relative completeness
with respect to well-known methods. To introduce the method we present as case study
in Section 3 the details of automated verification of a parameterized mutual exclusion
protocol, which is an instance of parameterized model defined in Section 2. Further, we
present an appropriate translation of verification tasks for the parameterized systems
of finite automata arranged in linear arrays into formulae of first-order predicate logic
(subsection 4.1). We show, in subsection 4.2, that the proposed finite countermodel
finding method is at least as powerful as the methods based on monotone abstraction
and symbolic backward reachability analysis [1] for this class of verification problems.
Further, in Section 5 we extend the relative completeness of the approach and show that
it can solve all safety verification problems which can be solved by a traditional regular
model checking [21]. In Section 6 we discuss related work and Section 7 concludes the
paper.

1.1 Preliminaries
 We assume that the reader is familiar with the the basics of first-order logic and algebra.
In particular, we use without definitions the following concepts: first-order predicate
logic, first-order models, interpretations of relational, functional and constant symbols,
satisfaction M |= ϕ of a formula ϕ in a model M , semantical consequence ϕ |= ψ, de-
ducibility (derivability) ⊢ in first-order logic, monoid, homomorphism, finite automata
and the algebraic characterization of regular languages. We denote interpretations by
square brackets, so, for example, [f ] denotes an interpretation of a functional symbol
f in a model. We also use the existence of complete finite model finding procedures
for the first-order predicate logic [5,20], which given a first-order sentence ϕ eventually
produce a finite model for ϕ if such a model exists.

2 Parameterized linear arrays of automata

    The computational model we first consider in this paper consists of parameterized
systems of finite automata arranged in linear arrays [1]. Formally, a parameterized sys-
tem P is a pair (Q, T ), where Q is a finite set of local states of processes and T is finite
set of transition rules. Every transition rule has one of the following forms
 – q → q ′ where q, q ′ ∈ Q;
 – G : q → q ′ , where q, q ′ ∈ Q and G is a condition of the form ∀I J, or ∃I J

Here J ⊆ Q and I is an indicator of the context, and it may be one of the following: L
(for Left), R (for Right), or LR (for both Left and Right).
    Given a parameterized system P = (Q, T ) the configuration of the system is a
word c̄ = c1 c2 . . . cn ∈ Q∗ . Intuitively, the configuration represents the local states of a
family of n finite state automata (processes) arranged in a linear array, so, for example
ci ∈ Q is a local state of automaton at position i in the array.
    For a configuration c̄ = c1 . . . cn , position i : 1 ≤ i ≤ n and a condition, we define
|=, a satisfaction relation:

 – (c̄, i) |= ∀L J iff ∀k < i ck ∈ J;
 – (c̄, i) |= ∀R J iff ∀k > i ck ∈ J;
 – (c̄, i) |= ∀LR J iff (c̄, i) |= ∀L J and (c̄, i) |= ∀R J
 – (c̄, i) |= ∃L J iff ∃k < i ck ∈ J;
 – (c̄, i) |= ∃R J iff ∃k > i ck ∈ J;
 – (c̄, i) |= ∃LR J iff (c̄, i) |= ∃L J or (c̄, i) |= ∃R J

A parameterized system P = (Q, T ) induces a transition relation →P on the set C of
all configurations as follows. For two configurations c̄ →P c¯′ holds iff either

 – q → q ′ is a transtion in T and for some i : 1 ≤ i ≤ n ci = q, c′i = q ′ and
   ∀j 6= i cj = c′j , or
 – G : q → q ′ is a transition in T and for some i : 1 ≤ i ≤ n ci = q, c′i = q ′ ,
   (c̄, i) |= G and ∀j 6= i cj = c′j

The general form of the verification problem we consider here is as follows.

    Given: A parameterized system P = (Q, T ), a set In ⊆ C of initial configurations,
a set B ⊆ C of bad configurations.
    Question: Are there any configurations c ∈ In and c′ ∈ B such that c′ is reachable
from c in P, i.e. for which c →∗P c′ holds?
    A negative answer for the above question means the safety property (“not B”) holds
for the parameterized system.



3 Case study



3.1 Mutual Exclusion Protocol
We consider the verification of the parameterized mutual exclusion protocol which was
used as an illustrative example in [1]. This protocol is specified as a parameterized
system ME = (Q, T ), where Q = {green, black, blue, red} and T consists of the
following transitions:
 – ∀LR {green, black} : green → black
 – black → blue
 – ∃L {black, blue, red} : blue → blue
 – ∀L {green} : blue → red
 – red → black
 – black → green
    The set of initial configurations In = green∗ consists of all configurations with
all automata in green states. The safety property we would like to check is a mutual
exclusion of red states, i.e. in any reachable configuration, there are no more than one
automaton in the red state. The set B of bad configurations is defined then by straight-
forward regular expression B = Q∗ red Q∗ red Q∗ .

3.2 First-Order encoding
We define a translation of the above parameterized system into a set of formulae ΦP of
first-order logic. The vocabulary of ΦP consists of
 – constants green, blue, black, red and e
 – one binary functional symbol ∗
 – unary predicates R, G, GB
Given a configuration c̄ = c1 . . . cn of P define its term translation as tc̄ = c1 ∗ . . . ∗ cn .
It is well-defined modulo the associativity of ′ ∗′ which we will specify in the formula,
and uses an assumption that in the language we have all the elements of Q as constants.
     The intended meaning of atomic formula R(tc̄ ) is that the configuration c̄ is reach-
able, while G(tc̄ ) and GB(tc̄ ) mean c̄ has only automata in green states, and c̄ has only
automata in green or black states, respectively.
     Let ΦP be a set of the following formulae, which are all assumed to be universally
closed:

 – (x ∗ y) ∗ z = x ∗ (y ∗ z)
 – e∗x=x∗e=x

    (∗ is a monoid operation and e is a unit of a monoid)

 – G(e)
 – G(x) → G(x ∗ green)

    (specification of configurations with all green states)

 – GB(e)
 – GB(x) → GB(x ∗ green)
 – GB(x) → GB(x ∗ black)

    (specification of configurations with all states being green or black)

 – G(x) → R(x)
    (initial state assumption: “allgreen” configurations are reachable)

 – (R((x ∗ green) ∗ y) & GB(x) & GB(y)) → R((x ∗ black) ∗ y)
 – R((x ∗ black) ∗ y) → R((x ∗ blue) ∗ y)
 – R((x ∗ blue) ∗ y) & (x = (z ∗ black) ∗ w) → R((x ∗ blue) ∗ y)
 – R((x ∗ blue) ∗ y) & (x = (z ∗ blue) ∗ w) → R((x ∗ blue) ∗ y)
 – R((x ∗ blue) ∗ y) & (x = (z ∗ red) ∗ w) → R((x ∗ blue) ∗ y)
 – R((x ∗ blue) ∗ y) & G(x) → R((x ∗ red) ∗ y)
 – R((x ∗ red) ∗ y) → R((x ∗ black) ∗ y)
 – R((x ∗ black) ∗ y) → R((x ∗ green) ∗ y)

    (specification of reachability by one step transitions from T ; one formula per transition,
    except the case with an existential condition, where three formulae are used)

Now we have a key proposition

Proposition 1 (adequacy of encoding). If a configuration c̄ is reachable in ME then
ΦP ⊢ R(tc̄ )

Proof By straightforward induction on the length of transition sequences in ME ✷

3.3 Verification
It follows now, that to establish safety property of the protocol (mutual exclusion), it
does suffice to show that ΦP 6⊢ ∃x∃y∃zR((((x ∗ red) ∗ y) ∗ red) ∗ z). Indeed, if, on the
contrary, some bad configuration c̄ would be reachable, then by Proposition 1 we would
have for some terms t1 , t2 , t3 that ΦP ⊢ R(tc̄ ) where tc̄ = (((t1 ∗red)∗t2 )∗red)∗t3 , and
therefore ΦP ⊢ ∃x∃y∃zR((((x∗ red)∗ y)∗ red)∗ z). Further, to show non-deducibility,
it is sufficient to find a countermodel for ΦP → ∃x∃y∃zR((((x ∗ red) ∗ y) ∗ red) ∗ z).
     Now we propose to delegate this last task to an automated procedure for finite model
finding, which would search for a finite model for

                      ΦP ∧ ¬∃x∃y∃zR((((x ∗ red) ∗ y) ∗ red) ∗ z)

In the practical implementation of this scheme we used a finite model finder Mace4
[20], which was able to find a required model in 0.03 seconds. Actual input for Mace4
and further details can be found in [18].
    A priori, to disprove some implication in first-order logic, searching for finite coun-
termodels may be not sufficient, for such countermodels may inevitably be infinite.
It has turned out empirically though that for many known parameterized (classes of )
problems, finite model finding is, indeed, both sufficient and efficient. In [17] we es-
tablished the first result on completeness of the method for a particular class of infinite
state verification tasks. Here we demonstrate further results on relative completeness.


4 Correctness and Completeness
4.1 First-Order Encoding for General Case
 In the general form of the verification problem above we have to agree what are the
allowed sets of initial and bad configurations can be, and what are their constructive
representations. Here we assume that

 – one of the local states q0 ∈ Q is singled out as an initial state, and the set Init of
   initial configurations is always q0∗ , i.e. it consists of all configurations that have all
   the automata in their local initial states;
 – The set B of bad configurations is defined by a finite set of words F ⊆ Q∗ : B =
   {c̄ | ∃w̄ ∈ F ∧ w̄  c̄}, where w̄  w̄′ denotes that w̄ is a (not necessarily
   contiguous) subword of w̄′ . The elements of such F are called generators of B.

To illustrate this last point, in our Case Study above, the set of bad configurations B is
defined by an F consisting of one word with two symbols red red.
    Given a parameterized system P = (Q, T ), an intial local state q0 ∈ Q, a finite set
of words F , we translate all of this into a set of formulae in first-order logic.
    The vocabulary consists of
 – constants for all elements of Q plus one distinct constant, so we take Q ∪ {e}, with
   e 6∈ Q as the set of constants;
 – the binary functional symbol ∗;
 – the unary relational symbol In;
 – the unary relational symbol R;
 – for every condition ∀I J in the transitions from T a unary relational symbol P J
Let ΦP be the set of the following formulae, which are all assumed to be universally
closed:

 – (x ∗ y) ∗ z = x ∗ (y ∗ z)
 – e∗x=x∗e=x

 – In(e)
 – In(x) → In(x ∗ q0 )
 – In(x) → R(x)

For every condition ∀I J in the transitions from T :
 – P J (e)
 – wedgeq∈J (P J (x) → P J (x ∗ q))
For every unconditional transition q1 → q2 from T :
 – R((x ∗ q1 ) ∗ y) → R((x ∗ q2 ) ∗ y)
For every conditional transition ∀L J (q1 → q2 ) from T :

 – (R((x ∗ q1 ) ∗ y) ∧ P J (x)) → R((x ∗ q2 ) ∗ y)

For every conditional transition ∀R J (q1 → q2 ) from T :
 – (R((x ∗ q1 ) ∗ y) ∧ P J (y)) → R((x ∗ q2 ) ∗ y)

For every conditional transition ∀LR J (q1 → q2 ) from T :

 – (R((x ∗ q1 ) ∗ y) ∧ P J (x) ∧ P J (y)) → R((x ∗ q2 ) ∗ y)

For every conditional transition ∃L J (q1 → q2 ) from T :

 – ∧q∈J (R(x ∗ q1 ) ∗ y) ∧ (x = (z ∗ q) ∗ w)) → R((x ∗ q2 ) ∗ y)

For every conditional transition ∃R J (q1 → q2 ) from T :

 – ∧q∈J (R(x ∗ q1 ) ∗ y) ∧ (y = (z ∗ q) ∗ w)) → R((x ∗ q2 ) ∗ y)

   For every conditional transition ∃LR J (q1 → q2 ) from T :

 – ∧q∈J (R(x ∗ q1 ) ∗ y) ∧ ((x = (z ∗ q) ∗ w) ∨ (y = (z ∗ q) ∗ w))) → R((x ∗ q2 ) ∗ y)

That concludes the definition of ΦP . Next, for a word w̄ = w1 , . . . , wn ∈ Q∗ we define
(up to the associativity of ∗) the formula ψw̄ as R(x0 ∗ w1 ∗ x1 ∗ . . . ∗ xn−1 ∗ wn ∗ xn )
where x0 , . . . xn are variables. Finally, we define ΨF as ∃x̄ ∨w̄∈F ψw̄ (here we assume
that all variables are bound by existential quantifiers).
    The following generalization of Proposition 1 holds.

Proposition 2 (adequacy of encoding). If configuration c̄ is reachable in P then ΦP ⊢
R(tc̄ )

Proof By straightforward induction on the length of the transition sequences ✷.

Corollary 1 (correctness of the method). If ΦP 6⊢ ΨF then the answer to the question
of the verification problem is negative, that is no bad configuration is reachable from
any of the initial configurations, and therefore, the safety property holds.


4.2 Relative completeness

 Here we show that on the the class of the verification problems described above our
proposed method is at least as powerful as the standard approach based on monotone
abstraction [1]. Specifically, if for a parameterized system P the approach [1] proves a
safety property, then our method based on finite countermodel finding will also succeed
in establishing this property, provided a complete finite model finding procedure is used.
    First, we briefly outline the monotone abstraction approach. Given a parameterized
system P = (Q, T ) and corresponding transition relation →P on the configurations
withing P, [1] defines the monotonic abstraction →A    P of →P as follows.

    We have c¯1 →A                                        ′             ′
                 P c¯2 iff there exists a configuration c̄1 such that c̄1  c̄1 and
      ′
    c̄ →P c2 .
Such defined →A   P is an over-approximation of →P . To establish the safety property, i.e
to get a negative answer to the question of the verification problem above, [1] proposes
using a symbolic backward reachability algorithm for monotone abstraction. Starting
with an upwards closed (wrt to ) set of bad configurations B = {c̄ | ∃w̄ ∈ F ∧ w̄ 
c̄}, the algorithm proceeds iteratively with the computation of the sets of configurations
backwards reachable along →A    P from B:

 – U0 = B
 – Ui+1 = Ui ∪ P re(Ui )

    where P re(U ) = {c̄ | ∃c̄′ ∈ U ∧ c̄ →A            ′
                                                   P c̄ }. Since the relation  is a well
quasi-ordering [1] this iterative process is guaranteed to stabilize, i.e Un+1 = Un for
some finite n. During the computation each Ui is represented symbolically by a finite
sets of generators. Once the process stabilized on some U the check is performed on
whether Init ∩ U = ∅. If this condition is satisfied then the safety is established, for no
bad configuration can be reached from intial configurations via →A   P and, a fortiori, via
→P .

Theorem 1 (relative completeness). Given a parameterized system P = (Q, T ) and
the set of bad configurations B = {c̄ | ∃w̄ ∈ F ∧ w̄  c̄}. Assume the algorithm
described above terminates with Init ∩ U = ∅. Then there exists a finite model for
ΦP ∧ ¬ΨF

Proof. First we observe that since U ⊆ Q∗ has a finite set of generators, it is a regu-
lar set. According to the algebraic characterization of regular sets, there exists a finite
monoid M = (M, ◦), a subset S ⊆ M and a homomorphism h : Q∗ → M from the
free monoid Q∗ to M such that U = {w̄ | w̄ ∈ Q∗ ∧ h(w̄) ∈ S}. We set M to be
domain of the required finite model.
Now we define interpretations of constants: for q ∈ Q [q] = h(q) and [e] = 1, where 1
is an unit element of the monoid.
The interpretation [∗] of ∗ is a monoid operation ◦. We define an interpretation of R as
[R] = M − S.
We define an interpretation of In inductively: [In] is the least subset of M satisfying
1 ∈ [In] and ∀x ∈ [In] x ◦ [q0 ] ∈ [In].
    An interpretation of P J is defined inductively as follows. [P J ] is a least subset of
M satisfying 1 ∈ [P j ] and ∀x ∈ [P J ] ∀q ∈ J x ◦ [q] ∈ [P J ]. That concludes the
definition of the finite model, which we denote by M. The key property of the model is
given by the following lemma.

Lemma 1. h(w̄) ∈ [R] iff no bad configuration is →A
                                                  P -reachable from w̄.

Proof is straightforward from the definitions of U , M, h and [R].

It follows immediately that M |= ¬ΨF . To show that M |= ΦP we show that M |= ϕ
for every ϕ ∈ Φ. For the first seven formulae in the definition of ΦP this involves a
routine check of definitions. We show here only one case of the remaining formulae
axiomatizing R.
    To demonstrate M |= (R((x ∗ q1 ) ∗ y) ∧ P J (x)) → R((x ∗ q2 ) ∗ y) for some
∀L J (q1 → q2 ) in T assume that left-hand side of the implication is satisfied in M for
some assignment of the variables. That means there are t1 , t2 ∈ M such that t1 ∗h(q1 )∗
t2 ∈ [R] and t1 ∈ [P J ]. Furthermore, there are w¯1 , w¯2 ∈ Q∗ such that t1 = h(w¯1 ),
t2 = h(w¯2 ) and no bad states are →A     P -reachable from w1 q1 w2 . Now, transition by
the rule ∀L J (q1 → q2 ) is possible from w¯1 q1 w¯2 , resulting in the configuration
w¯1 q2 w¯2 , from which it is still the case that no bad configurations are reachable. This
implies h(w¯1 ) h(q2 ) h(w¯2 ) ∈ [R], and therefore M |= (R((x ∗ q1 ) ∗ y) ∧ P J (x)) →
R((x ∗ q2 ) ∗ y). The remaining cases are tackled in a similar way. ✷.


4.3 FCM is stronger than monotone abstraction

For some parameterized systems the method based on monotone abstraction may fail
to establish safety even though it may actually hold. The reason for this is a possible
overapproximation of the set of reachable states as a result of abstraction. A simple
example of such a case is given in [2]. The parameterized system (Q, T ) where Q =
{q0 , q1 , q2 , q3 , q4 } and where T includes the following transition rules

 1. ∀{q0 , q1 , q4 } : q0 → q1
 2. q1 → q2
 3. ∀L {q0 } : q2 → q3
 4. q3 → q0
 5. ∃LR {q2 } : q3 → q4
 6. q4 → q3

satisfies mutual exclusion for state q4 , but this fact can not be established by the mono-
tone abstraction method from [1]. However, using first-order encoding presented above
and the finite model finder we have verified mutual exclusion for this system, demon-
strating that FCM method is stronger than monotone abstraction. Mace4 has found a
finite countermodel of the size 6 in 341s. See details in [18] and the Appendix.
     The issue of overapproximation has been addressed in [2] where two refinements
of the monotonic abstraction method were proposed. One resulted in an exact context-
sensitive symbolic algorithm which allows one to compute exact symbolic representa-
tions of predecessor configurations, but the termination of which is not guaranteed. On
the other hand, an approximated context-sensitive symbolic algorithm is also proposed
and while guaranteed to terminate, may still lead to overapproximation. One can show
the relative completeness of the FCM method with respect to both algorithms for the
case of safety verification. In both algorithms the safety is established when a finite
representation of a set U of configurations backwards rechable from unsafe states, is
obtained upon an algorithm termination. In both cases such a set U can be shown is
regular, and therefore one can apply the arguments used in the proof of Theorem 1. We
postpone the detailed presentation till another occassion, but would like to emphasize
that the main reason for the relative completeness here is a mere existence of the regular
sets of configurations subsuming all reachable configurations and disjoint with unsafe
configurations.
5 Regular model checking


     The result of the previous section may appear rather narrow and related to a spe-
cific class of parameterized systems. The verification of safety for this class can be
re-formulated for, and dealt with the traditional regular model checking approach[21].
In this section we extend our relative completeness result and show that whenever safety
for a parameterized system can be established by the regular model checking approach
then it can also be verified by the finite countermodel finding method.
     We start with the basics of the traditional regular model checking approach, bor-
rowing standard definitions largely from [14]. A finite automaton is a tuple M =
hQ, Σ, δ, q0 , F i, where Q is a finite set of states, Σ is a finite alphabet, δ ⊆ Q × Σ × Q
is a set of transitions, q0 ∈ Q is an initial state and F ⊆ Q is a set of final (accept-
ing) states. M is deterministic automaton if ∀q ∈ Q ∀a ∈ Σ there esists at most
one q ′ such that hq, a, q ′ i ∈ δ. With every finite automaton we associate a transi-
tion relation → ⊆ Q × Σ ∗ × Q which is defined as the smallest relation satisfy-
ing: (1): ∀q ∈ Q; q →ǫ q, (2) if hq, a, q ′ i ∈ δ, then q →a q ′ , (3) if q →w q ′ and
q ′ →a q ′′ then q →wa q ′′ . The language recognized by the automaton M is defined as
L(M ) = {w | ∃q ′ ∈ F ∧ ∧ q0 →w q ′ }.
     Let Σ be a finite alphabet and ǫ 6∈ Σ. Let Σǫ = Σ ∪{ǫ}. A finite transducer over Σ is
a tuple τ = hQ, Σǫ∗ ×Σǫ∗ , δ, q0 , F i, where Q is a finite set of states, δ ⊆ Q×Σǫ ×Σǫ ×Q
a set of transitions, q0 ∈ Q is an initial state, and F ⊆ Q is a set of final (accepting)
states. The transition relation →⊆ Q × Σ ∗ × Σ ∗ × Q is defined as the smallest relation
staisfying: (1) q →ǫ,ǫ q for every q ∈ Q, (2) if hq, a, b, q ′ i ∈ δ, then q →a,b q ′ , and (3)
if q →w,u q ′ and q ′ →a,b q ′′ , then q →wa,ub q ′′ . With every transducer τ we associate
a binary relation rτ = {hw, ui | ∃q ′ ∈ F ∧ q0 →w,u q ′ }. Let rτ∗ denote the reflexive
and transitive closure of rτ .
     The verification of safety properties in the framework of regular model checking
proceeds as follows. The set of initial states of the parameterized (or infinite state)
system is presented by an effectively given (by a finite automaton) regular language
Init . The set of “bad”, or unsafe states is described by another regular language Bad.
One-step transitions of the system to be verified are presented by a transducer relation
rτ (for some finite state transducer τ ). The verification of safety property (“never get
into the bad states”) is reduced to the following

Problem 1. Given regular sets Init and Bad and a finite transducer τ , does rτ∗ (Init) ∩
Bad = ∅ hold?

Regular model checking (RMC) is one of the most general methods for formal veri-
fication of parameterized and infinite state systems [21,4]. One of the issues with the
method is that the termination of the computation of transitive closure rτ∗ (Init) is not
guaranteed. To alleviate this issue, various acceleration methods have been proposed.
We show that the finite countermodel finding method is actually as powerful as any
variant of RMC, the only assumption to guarantee its termination is the existence of a
regular set R subsuming rτ∗ (Init) and being disjoint with Bad.
5.1 From regular model checking to first-order disproving

In this subsection we show how to reduce the generic regular model checking question
posed in the Problem 1 above to the problem of disproving of a formula from classical
first-order predicate logic. Solution of the latter problem is then delegated to the generic
automated finite model finding procedure.
Assume we are given

  – a finite state automaton M1 = hQ1 , Σ, δ1 , q01 , F1 i recognizing a regular language
    Init;
  – a finite state automaton M2 = hQ2 , Σ, δ2 , q02 , F2 i recognizing a regular language
    Bad;
  – a finite state length-preserving transducer τ = hQ, Σ ∗ × Σ ∗ , δ, q0 , F i representing
    the transition relation rτ ;

Assume also (without loss of generality) that sets Q1 , Q2 , Q, Σ are disjoint.
Now define a set of formulae of first-order predicate logic as follows. In fact, it is a
formalization of the above definition of → within first-order predicate logic.
   The vocabulary consists of
  – constants for all elements of Σ ∪ Q1 ∪ Q2 ∪ Q plus one distinct constant e;
  – a binary functional symbol ∗;
  – unary relational symbols R, Init and Bad;
  – a binary relational symbol T rans;
  – a ternary relational symbol T (3) ;
  – a 4-ary relational symbol T (4) ;
Let Φ be the set of the following formulae, which are all assumed to be universally
closed:

 1. (x ∗ y) ∗ z = x ∗ (y ∗ z)
 2. T (3) (q, e, q) for all q ∈ Q1 ∪ Q2 ;
 3. T (3) (q, a, q ′ ) for all (q, a, q ′ ) ∈ δ1 ∪ δ2 ;
 4. T (3) (x, y, z) ∧ T (3) (z, v, w) → T (3) (x, y ∗ v, w)
 5. ∨q∈F1 T (3) (q01 , x, q) → Init(x)
 6. ∨q∈F2 T (3) (q02 , x, q) → Bad(x)
 7. T (4) (x, e, e, x)
 8. T (4) (q, a, b, q ′ ) for all (q, a, b, q ′ ) ∈ δ
 9. T (4) (x, y, z, v) ∧ T (4) (v, y ′ , z ′ , w) → T (4) (x, y ∗ y ′ , z ∗ z ′ , w)
10. T rans(x, y) ↔ ∨q∈F T (4) (q0 , x, y, q)
11. Init(x) → R(x)
12. R(x) ∧ T rans(x, y) → R(y)

Proposition 3 (adequacy of Init and Bad translations).

     If w ∈ Init then Φ ⊢ Init(tw )
     If w ∈ Bad then Φ ⊢ Bad(tw )
Proof For w = s1 , . . . sn ∈ Init we have w is accepted by the finite automaton
M1 , which means there is a sequence of states q01 , q1 , . . . qn with qn ∈ F1 such that
hqi , si , qi+1 i ∈ δ1 for i = 0, . . . n − 1. By the definition of Φ (clause 3) all formulae
T (qi , si , qi+1 ) are in Φ. Together with clause 4, this gives Φ ⊢ T (q01 , tw , qn ). This with
qn ∈ F1 and using clause 5 entails Φ ⊢ Init(tw ). The second statement is proved in
the same way. ✷

Proposition 4 (adequacy of encoding). If w ∈ rτ∗ (Init) then Φ ⊢ R(tw )

Proof. Easy induction on the length of transition sequences.

 – Induction Base Case. Let w ∈ Init. Then Φ ⊢ Init(tw ) (by Proposition 3), and,
   further, Φ ⊢ R(tw ) (using clause 11).
 – Induction Step Case. Let w ∈ rτn+1 (Init). Then there exists w′ such that w′ ∈
   rτn (Init) and hw′ , wi ∈ rτ . By the induction assumption Φ ⊢ R(tw′ ). Fur-
   ther, by an argument analogous to the proof in Proposition 3, hw′ , wi ∈ rτ en-
   tails Φ ⊢ T (q0 , tw′ , tw , q) for some q ∈ F . It follows, using clause 10, that Φ ⊢
   T rans(tw′ , tw ). From this, the clause 12 and the induction assumption Φ ⊢ R(tw′ )
   follows.

Corollary 2. If rτ∗ (Init) ∩ Bad 6= ∅ then Φ ⊢ ∃x(R(x) ∧ Bad(x)).

The Corollary 2 serves as a formal underpinning of the proposed verification method.
In order to prove safety, that is rτ∗ (Init) ∩ Bad = ∅ it suffices to demonstrate Φ 6⊢
∃x(R(x) ∧ Bad(x)), or equivalently, to disprove Φ → ∃x(R(x) ∧ Bad(x)). We dele-
gate this task to the finite model finding procedures, which search for the finite counter-
models for Φ → ∃x(R(x) ∧ Bad(x)).


5.2 Relative completeness with respect to RMC

As highlighted earlier, searching for finite countermodels to disprove non-valid first-
order formulae may not always lead to success, because for some formulae counter-
models are inevitably infinite. In this subsection we show that it is not the case for the
first-order encodings of the problems which can be positively answered by RMC, and
therefore such problems can also be resolved positively by the proposed finite counter-
model finding method, provided a complete finite model finding procedure is used.
     Assume that RMC answers positively the question of Problem 1 above. In the
RMC approach the positive answer follows from producing a regular set R such that
rτ∗ (Init) ⊆ R and R ∩ Bad = ∅. We show that in such a case there always exists a
finite countermodel for Φ → ∃x(R(x) ∧ Bad(x)).

Theorem 2 (relative completeness). Let Init and Bad be regular sets given by rec-
ognizing finite automata M1 and M2 , and τ be a finite state transducer. Let Φ be a first-
order formula defined above. If there exists a regular set R such that rτ∗ (Init) ⊆ R and
R ∩ Bad = ∅ then there exists a finite countermodel for Φ → ∃x(R(x) ∧ Bad(x))
Proof
Since R is regular, according to the algebraic characterization of regular sets, there
exists a finite monoid M = (M, ◦), a subset S ⊆ M and a homomorphism h : Σ ∗ →
M such that R = {w̄ | w̄ ∈ Σ ∗ ∧ h(w̄) ∈ S}.
    We take M ∪ Q1 ∪ Q2 to be domain of the required finite model, and then define
interpretations as follows.

 • For a ∈ Σ [a] = h(a);
 • [e] = 1, where 1 is an unit element of the monoid;
 • [∗] is a monoid operation ◦;
 • Interpretations of T 3 and T 4 are defined inductively, as the least subsets of tuples
   satisfying, respectively, formulae (2)-(4) and (7) - (9)(and assuming all interpreta-
   tions given above);
 • Interpretations of Init and Bad are defined to be the least subsets satisfying (5) and
   (6), respectively (assuming all interpretations above);
 • Interpretation of Trans is defined by (10)(assuming all interpretations above);
 • Interpretation of R is S.

    Now it is straightforward to check that such defined a finite model indeed satisfies
Φ ∧ ¬∃x(R(x) ∧ Bad(x)). Checking that Φ is satisfied is by routine inspection of the
definitions. To check that ¬∃x(R(x) ∧ Bad(x)) is satisfied, assume the opposite holds.
So there exists an element a of the monoid M such that a ∈ [R] and a ∈ [Bad]. Then,
for a word w ∈ Σ ∗ such that h(w) = a, we have w ∈ R ∩ Bad 6= ∅, which contradicts
with the assumption of the theorem. ✷.


5.3 Optimizations


In many cases (i.e. in many subclasses of verification tasks), the transition relation
and/or the sets of ‘initial’ and ‘bad’ states are described not by finite state transduc-
ers/automata, but in more explicit and simpler ways, e.g. by rewriting rules for transi-
tions and simple grammars generating sets of states. In such a cases, first-order trans-
lations can be made simpler and the whole procedure more efficient. Our treatment of
the case of parameterized linear automata in Section 4 can be seen as an illustration of
such a modification.


5.4 Experimental results


In the experiments we used the finite model finder Mace4[20] within the package
Prover9-Mace4, Version 0.5, December 2007. It is not the latest available version,
but it provides with convenient GUI for both the theorem prover and the finite model
finder. The system configuration used in the experiments: Microsoft Windows XP Pro-
fessional, Version 2002, Intel(R) Core(TM)2 Duo CPU, T7100 @ 1.8Ghz 1.79Ghz,
1.00 GB of RAM. The time measurements are done by Mace4 itself, upon completion
of the model search it communicates the CPU time used. The table below lists the pa-
rameterised/infinite state protocols together with the references and shows the time it
took Mace4 to find a countermodel and verify a safety property. The time shown is an
average of 10 attempts.

                    Protocol                      Reference Time
                    Token passing (non-optimized)     [14]    0.12s
                    Token passing (optimized)         [14]    0.01s
                    Mutual exclusion I             [1] and 3 0.03s
                    Mutual exclusion II           [2] and 4.2 341s
                    Bakery                            [21]    0.03s
                    Paterson−                     [8] and 5.5 0.77s

5.5 Beyond regular model checking
 The method of verification via disproving (countermodel finding) can be applied also
to classes of problems where traditional regular model checking is not applicable. Con-
sider, for example, the case where the set of initial states is not regular, so the standard
algorithms of RMC are not applicable. In the paper [8] an extension of regular model
checking is proposed, which is capable to tackle some non-regular cases. Not claiming
any kind of completeness (yet!) we show in this subsection that a case study exam-
ple from [8] can be (partially, as for now) tackled by the finite countermodel finding
method too. Consider the following string rewriting system over alphabet {0, 1}, which
is an encoding of the parameterized Paterson mutual exclusion algorithm from [8]:
 1. x01y → x10y           where x ∈ 0∗ , y ∈ (1 + 0)∗
 2. x101y → x110y         where x ∈ (1 + 0)∗ , y ∈ 1∗
 3. x001y → x010y         where x, y ∈ (1 + 0)∗
 4. x0 → 0x               where x ∈ (1 + 0)∗
    The safety condition for this rewriting system is ‘Starting from any string of the
form 0n 1n no string from the set (0 + 1)∗ 00 is reachable’ (mutual exclusion of the
original Paterson algorithm). In [8] it is shown that the extension of RMC proposed
there can successfully verify the condition.
    Following the translation from the Section 4 we encode the string rewriting system
into a first-order formula Φ. Since the set of initial states is not regular, the formula
contains a part specifying the generation of initial states by a context-free grammar:
R(e) ∧ R(x) → R((0 ∗ x) ∗ 1).
    In the experiments we failed to verify the correctness condition for the Paterson al-
gorithm, however, for the reduced string rewriting system Paterson− , containing only
the rules 1,2,4 we have verified safety condition above. Mace4 has found a finite coun-
termodel of size 8 in 0.77s. The details can be found in [18].


6 Related work
     As mentioned Section 1 the approach to verification using the modeling of pro-
tocol executions by first-order derivations and together with countermodel finding for
disproving was introduced within the research on the formal analysis of cryptographic
protocols. It can be traced back to the early papers by Weidenbach [23] and by Selinger
[22]. In [23] a decidable fragment of Horn clause logic has been identified for which
resolution-based decision procedure has been proposed (disproving by the procedure
amounts to the termination of saturation without producing a proof). It was also shown
that the fragment is expressive enough to encode cryptographic protocols and the ap-
proach has been illustrated by the automated verification of some protocols using the
SPASS theorem prover. In [22], apparently for the first time, explicit building of finite
countermodels has been proposed as a tool to establish correctness of cryptographic
protocols. It has been illustrated by an example, where a countermodel was produced
manually, and the automation of the process has not been disscussed. The later work by
Goubault-Larrecq [11] has shown how a countermodel produced during the verification
of cryptographic protocols can be converted into a formal induction proof. Also, in [11]
different approaches to model building have been discussed and it was argued that an
implicit model building procedure using alternating tree automata is more efficient in
the situations when no small countermodels exist. Very recently, in the paper [15] by
J. Jurgens and T. Weber, an extension of Horn clause logic was proposed and the sound-
ness of a countermodel finding procedure for this fragement has been shown, again in
the context of cryptographic protocol verification. Furthermore, in [15] an approach to
the verification of parameterized cryptoprotocols is proposed.

    The work we reported in this paper differs from all the approaches mentioned pre-
viously in two important aspects. Firstly, to the best of our knowledge, none of the
previous work addressed verification via countermodel finding applied outside of the
area of cryptographic protocols (that includes the most recent work [13] we are aware
of). Secondly, the (relative) completeness for the classes of verification tasks has not
been addressed in previous work.

    The encoding of infinite state systems in first-order predicate logic is used in the
MCMT deductive symbolic model checker [9,10]. While principles of encoding used
in MCMT are very much similar to these we consider in the present paper, the verifi-
cation procedure is quite different. The core algorithm of MCMT relies on a symbolic
backwards reachability procedure, in which first-order formulae are used for the sym-
bolic representation of the sets of configuration. During the execution the reachability
procedure may call the external logic engine (SMT solver) multiple times, up to several
hundreds for some examples as reported in [9]. In the FCM method we presented here
the verification procedure is much simpler and is just a reduction (or compilation) to
a single problem in logic, which then is resolved via single call to the external logic
engine (finite model builder).

    In a more general context, the work we present in this paper is related to the concepts
of proof by consistency [16], and inductionless induction [6] and can be seen as an
investigation into the power of these concepts in the particular setting of the verification
of parameterized systems via finite countermodel finding.
7 Conclusion


We have shown how to apply generic finite model finders in the parameterized verifica-
tion of linear arrays of finite automata models, have demonstrated the relative complete-
ness of the method, and have illustrated its practical efficiency. Further, we have shown
that the verification via finite countermodel finding is at least as powerful as the stan-
dard regular model checking for the verification of safety properties. Inspection of the
proofs of relative completeness reveals that the key reason for the completeness is the
existence of regular sets separating the reachable and bad (unsafe) states. We conclude
with the very general claim that, for any parameterized system, for which there exists a
regular set separating reachable and unsafe states, its correctness can be demonstrated
by a finite countermodel finding method. Formal instantiations of this claim for particu-
lar classes of problems remains a subject of ongoing and future work. In particular, the
extension of the results presented in this paper to the case of tree regular model check-
ing looks quite straightforward. More speculative and intriguing is a possibility to use
infinite model building procedures [5] for parameterized verification. Further investiga-
tion of practical efficiency and scalability of the method is also an important direction
for future work.


8 Acknowledgments

The author is grateful to Michael Fisher for the helpful suggestions on this paper.


References
 1. Parosh Aziz Abdulla, Giorgio Delzanno, Noomene Ben Henda, Ahmed Rezine. Monotonic
    Abstraction: on Efficient Verification of Parameterized Systems. Int. J. Found. Comput. Sci.
    20(5): 779-801 (2009)
 2. Parosh Aziz Abdulla, Girogio Delzanno, Ahmed Rezine. Approximated Context-Sensitive
    Analysis for Parameterized Verification. Lecture Notes in Computer Science, 2009, Volume
    5522, 41-56
 3. Parosh Aziz Abdulla, Jonsson B. Verifying programs with unreliable channels. Information
    and Computation, 127(2):91-101, June 15, 1996.
 4. Parosh Aziz Abdulla, Bengt Jonsson, Marcus Nilsson, and Mayank Saksena, A Survey of
    Regular Model Checking, In Proc. of CONCUR’04, volume 3170 of LNCS, pp 35–58, 2004.
 5. R. Caferra, A. Leitsch, N. Peltier, Automated Model Building, Applied Logic Series, 31,
    Kluwer, 2004.
 6. H. Comon. Inductionless induction. In R. David, ed. 2nd Int. Conf. in Logic for Computer
    Science: Automated Deduction. Lecture Notes, Chambery, Uni de Savoie, 1994.
 7. G. Delzanno. Constraint-based Verification of Parametrized Cache Coherence Protocols.
    Formal Methods in System Design, 23(3):257–301, 2003.
 8. Dana Fisman and Amir Pnueli, Beyond Regular Model Checking, In Proc. of FSTTCS01,
    volume 2245 of LNCS, 2001.
 9. S.Ghilardi and S.Ranise. MCMT: A Model Checker Modulo Theories. Lecture Notes in
    Computer Science, 2010, Volume 6173/2010, 22–29.
10. S.Ghilardi, E.Nikolini, S.Ranise and D.Zucchelli. Towards SMT Model-Checking of Array-
    based Systems. In IJCAR, LNCS, 2008
11. J. Goubault-Larrecq. Towards producing formally checkable security proofs, automatically.
    In: Computer Security Foundations (CSF), pp. 224-238 (2008)
12. J. Goubault-Larrecq. ”Logic Wins!”. In ASIAN’09, LNCS 5913, pages 1-16. Springer, 2009.
13. Joshua Guttman, Security Theorem via Model Theory, arXiv:0911.2036, November 2009.
14. Peter Habermehl, Tomas Vojnar, Regular Model Checking Using Inference of Regular Lan-
    guages, Electronic Notes in Theoretical Computer Science (ENTCS) , Volume 138 , Issue 3
    (December 2005) , pp 21–36, 2005
15. J. Jurjens and T. Weber, Finite Models in FOL-Based Crypto-Protocol Verification, P. Degano
    and L. Vigan‘o (Eds.): ARSPA-WITS 2009, LNCS 5511, pp. 155-172, 2009.
16. D. Kapur and D.R. Musser. Proof by consistency. Artificial Intelligence, 31:125–157, 1987.
17. A. Lisitsa Reachability as deducibility, finite countermodels and verification. In preProceed-
    ings of AVOCS 2009, Technical Report of Computer Science, Swansea University, CSR-2-
    2009, pp 241-243.
18. A. Lisitsa Verfication via countermodel finding
    http://www.csc.liv.ac.uk/˜alexei/countermodel/
19. A. Lisitsa Reachability as deducibility, finite countermodels and verification. A conference
    version of [17], 14pp, (to appear in Proc. ATVA2010)
20. W. McCune Prover9 and Mace4 http://www.cs.unm.edu/˜mccune/mace4/
21. M. Nilsson. Regular Model Checking. Acta Universitatis Upsaliensis. Uppsala Dissertations
    from the Faculty of Science and Technology 60. 149 pp. Uppsala. ISBN 91-554-6137-9,
    2005.
22. P. Selinger, Models for an adversary-centric protocol logic. Electr. Notes Theor. Comput.
    Sci. 55(1) (2001)
23. C. Weidenbach, Towards an Automatic Analysis of Security Protocols in First-Order Logic,
    in H. Ganzinger (Ed.): CADE-16, LNAI 1632, pp. 314–328, 1999.
