                                                   Proving differential privacy in Hoare logic
                                        Gilles Barthe∗ , Marco Gaboardi‡, Emilio Jesús Gallego Arias† , Justin Hsu†, César Kunz∗, and Pierre-Yves Strub∗
                                          ∗ IMDEA Software Institute, Spain                 ‡ University of Dundee, Scotland                    † University of Pennsylvania, USA




                                           Abstract—Differential privacy is a rigorous, worst-case notion         A close relative of self-composition is the synchronized
                                        of privacy-preserving computation. Informally, a probabilistic         product construction [38]. This transformation also produces
                                        program is differentially private if the participation of a single     a program which emulates two executions of the original
                                        individual in the input database has a limited effect on the
                                                                                                               program, but while self-composition performs the executions
arXiv:1407.2988v1 [cs.LO] 10 Jul 2014




                                        program’s distribution on outputs. More technically, differential
                                        privacy is a quantitative 2-safety property that bounds the            in sequence, synchronized products perform the executions
                                        distance between the output distributions of a probabilistic           in lockstep, dramatically simplifying the verification task for
                                        program on adjacent inputs. Like many 2-safety properties, dif-        certain properties. This transformation is an instance of the
                                        ferential privacy lies outside the scope of traditional verification   more general class of product transformations, as studied by
                                        techniques. Existing approaches to enforce privacy are based on
                                        intricate, non-conventional type systems, or customized relational     Zaks and Pnueli [38], and recently by Barthe et al. [4], [5].
                                        logics. These approaches are difficult to implement and often             While there has been much research on combining prod-
                                        cumbersome to use.                                                     uct constructions and deductive verification to reason about
                                           We present an alternative approach that verifies differen-          2-safety for deterministic programs, this approach remains
                                        tial privacy by standard, non-relational reasoning on non-             largely unexplored for probabilistic programs. This is not
                                        probabilistic programs. Our approach transforms a probabilistic
                                        program into a non-probabilistic program which simulates two           for lack of interesting use cases—many security notions of
                                        executions of the original program. We prove that if the target        probabilistic computation are naturally 2-safety properties.
                                        program is correct with respect to a Hoare specification, then               Verifying differential privacy: In this paper, we con-
                                        the original probabilistic program is differentially private. We       sider on one such property: differential privacy, which pro-
                                        provide a variety of examples from the differential privacy
                                        literature to demonstrate the utility of our approach. Finally,
                                                                                                               vides strong guarantees for privacy-preserving probabilistic
                                        we compare our approach with existing verification techniques          computation. Formally, a probabilistic program c is (ǫ, δ)-
                                        for privacy.                                                           differentially private with respect to ǫ > 0, δ ≥ 0, and a
                                                                                                               relation1 Φ on the initial memories of c if for every two initial
                                                               I. I NTRODUCTION                                memories m1 and m2 related by Φ, and every subset A of
                                           Program verification provides a rich array of techniques            output memories,
                                        and tools for analyzing program properties. However, they
                                        typically reason about single program executions or trace                         Pr [c, m1 : A] ≤ exp(ǫ) Pr [c, m2 : A] + δ.
                                        properties. In contrast, many security properties—such as non-
                                                                                                               Here Pr [c, m : A] denotes the probability of the output mem-
                                        interference in information flow systems—require reasoning
                                                                                                               ory landing in A according to distribution JcK m, where JcK
                                        about multiple program executions. These hyperproperties [17]
                                                                                                               maps an initial memory m to a distribution JcK m of output
                                        encompass many standard security analyses, and lie outside the
                                                                                                               memories. Since this definition concerns two runs of the same
                                        scope of standard verification tools—to date, there is no gen-
                                                                                                               probabilistic program, differential privacy is a probabilistic 2-
                                        erally applicable method or tool for verifying hyperproperties.
                                                                                                               safety property.
                                        Instead, ad hoc enforcement methods based on type systems,
                                        customized program logics, and finite state automata analyses             Differentially private algorithms are typically built from two
                                        have been applied to specific hyperproperties. While these             constructions: private mechanisms, which add probabilistic
                                                                                                               noise to their input, and composition, which combines dif-
                                        approaches are effective, their design and implementation
                                        often require significant effort.                                      ferentially private operations into a single one. This composi-
                                                                                                               tional behavior makes differential privacy an attractive target
                                           A promising alternative is to reduce verification of a hy-
                                        perproperty of a program c to verification of a standard               for program verification efforts.
                                        property of a transformed program T (c). For instance, self-              Existing methods for proving differential privacy have been
                                        composition [7], [18] is a general method for reducing 2-safety        based on type systems, automata analyses, and customized
                                        properties of a program c—which reason about two runs of c—            program logics. For instance, Fuzz [33], DFuzz [25] and
                                        to safety properties of the sequential composition c; c′ , where       related systems [24] enforce differential privacy using linear
                                        c′ is a renaming of c. Self-composition is sound, complete,            type systems. This approach is expressive enough to type many
                                        and applies to many programming languages and verification             examples, but it is currently limited to pure differential privacy
                                        settings. For instance, it has been used to verify information            1 We are here taking a generalization of Differential Privacy with respect
                                        flow properties using standard deductive methods like Hoare            to an arbitrary relation Φ. The usual definition is obtained by considering an
                                        logic.                                                                 adjacency relation between databases.
(where δ = 0), and cannot handle more advanced examples.             to an abstract procedure that returns equal outputs, at the cost
Alternatively, Tschantz et al. [37] consider a verification          of consuming some privacy budget—roughly, being at distance
technique based on I/O automata; again, this approach is             0 in the probabilistic setting is equivalent to being equal in the
limited to pure differential privacy. Finally, CertiPriv [11] and    non-probabilistic setting. To keep track of the privacy cost, we
EasyCrypt [6] use an approximate relational Hoare logic for          use ghost variables vǫ and vδ which are incremented after each
probabilistic programs to verify differential privacy. This ap-      mechanism is executed, in terms of the distance between their
proach is very expressive and can accommodate approximate            two inputs.
differential privacy (when δ 6= 0), but relies on a custom and          Note that the second step leverages the synchronized prod-
complex logic. For instance, ad hoc rules for loops are required     uct construction: since the two executions are simulated in
for many advanced examples. Finally, a common weakness of            lockstep, corresponding calls to a mechanism are next to each
all of the above approaches is that their implementation is          other in the product program. Since mechanisms are the only
non-trivial.                                                         probabilistic parts of our source program, our output program
      Self-products for differential privacy: To avoid these         is now non-probabilistic.
drawbacks, we investigate a new approach where proving                  To illustrate our approach, consider the following simple
(ǫ, δ)-differential privacy of a program c is reduced to proving     program c:
a safety property of a transformed program T (c). In view of                            s; x ← Lapǫ (e); return x
previous work verifying 2-safety properties, a natural choice
for T is some notion of product program. However, the trans-         where s is a deterministic computation and Lap is the Laplace
formed programs would then be probabilistic, and there are           mechanism—a probabilistic operator that achieves differential
few tools for deductive verification of probabilistic programs.      privacy by adding noise to its input. The synchronized product
Targeting a non-probabilistic language is more appealing in          T (c) of the program c is
this regard, as there are many established tools for deductive
                                                                        T (s); x1 ← Lapǫ (e1 ); x2 ← Lapǫ (e2 ); return (x1 , x2 )
verification of non-probabilistic programs. Since the original
program is a probabilistic program, a key part of our approach       where T (s) is the synchronized product of s. Then, we make
is to remove the probabilistic behavior from the target.             the program non-probabilistic by replacing the two calls to the
   To define the transformation, we proceed in two steps.            Laplace mechanism with a call to an abstract procedure Lap⋄ ,
Starting from a probabilistic program c, we first construct the      giving the following transformed program T (c).
synchronized product of c with itself. Using the synchronized
product instead of self-composition is essential for our second              T (s); (x1 , x2 ) ← Lap⋄ (e1 , e2 ); return (x1 , x2 )
step, in which the probabilistic product program is transformed
                                                                     Roughly, the specification of the procedure invocation Lap⋄
into a non-probabilistic program.
                                                                     states that the same value is assigned to x1 and x2 . Also, as
   For this step, we rely on specific features of the differential
                                                                     side effect, the variable vǫ is updated to increment the privacy
privacy property. First, we observe that differential privacy
                                                                     cost, which depends on the distance between the inputs (e1 , e2 )
bounds the ratio—hereafter called the privacy cost—between
                                                                     to the Laplace mechanism.
the probabilities of producing the same output on two exe-
cutions on nearby databases. Second, we recall that there are           Our main result (Theorem 5 in §III) states that once we
two main tools for building differentially private computations:     perform this transformation, we can use plain Hoare logic to
private mechanisms, and composition. Private mechanisms and          complete the verification. More concretely, for the example
composition interact with the privacy cost in different ways;        above, we represent the relation on memories Φ as a predicate
we consider each in turn.                                            Φ̂ on pairs of memories, and prove that c is (ǫ, 0)-differentially
   A private mechanism run over two different inputs returns         private if the following Hoare specification is valid.
two closely related distributions, at the cost of consuming                   ⊢ T (c) : Φ̂ ∧ vǫ = 0 =⇒ x1 = x2 ∧ vǫ ≤ ǫ0
some privacy budget. The privacy cost depends on the distance
between the inputs: as the two inputs become farther apart,          In the remainder of this article we use the same representation
the privacy cost also grows. One fundamental insight (due to         for a relation and its representation as a predicate on memories.
Barthe et al. [10]) we use is that the property of being “closely          Contributions: The main contribution of the paper (§III)
related” can be understood as being at distance 0 for a suitable     is a program transformation that operates on programs built
notion of distance on distributions.                                 from sequential, non-probabilistic constructs and differentially
   Composition takes a set of differentially private operations      private, probabilistic primitives—such as the Laplace and
and returns the sequential composition of the operations, which      Exponential mechanisms. The transformed program is non-
is also differentially private. By a property of differential        probabilistic, and differential privacy of the original program
privacy, the privacy cost of the composition is upper bounded        can be reduced to a safety property of the transformed pro-
by the sum of the privacy costs of the individual operations.        gram. Then we show in §IV that our approach subsumes the
   We build this reasoning directly into our verification system.    core apRHL logic of Barthe et al. [11], in the sense that every
First, we apply the synchronized product construction. Then,         algorithm provable with core apRHL is also provable with our
we replace two corresponding calls to a mechanism with a call        approach.
   We illustrate the expressiveness of our approach in §V               Theorem 1 ([19]): Suppose ǫ > 0. The Laplace mechanism
by verifying differential privacy of several probabilistic algo-     is defined by
rithms, including a recent algorithm that produces synthetic                              Lapǫ (t) = t + v,
datasets using a combination of the multiplicative weights
update rule and the exponential mechanism [29], [28], and            where v is drawn from the Laplace distribution L(1/ǫ), i.e.
the Propose-Test-Release (PTR) framework [21], [36], which           with probability density function
achieves approximate differential privacy without relying on
                                                                                             P (v) = exp(−ǫ|v|).
output perturbation. Finally, we discuss the example of vertex
cover, which is provable apRHL, but cannot be handled                If F is k-sensitive with respect to Φ, then the probabilistic
directly by our approach.                                            function that maps t to Lapǫ (F (t)) is (kǫ, 0)-differentially
         II. A PRIMER ON DIFFERENTIAL PRIVACY                        private with respect to Φ.
                                                                        Additionally, the Laplace mechanism satisfies a simple
   Let us begin by recalling the basic definitions of differential
                                                                     accuracy bound.
privacy.
                                                                        Lemma 1: Let ǫ, δ > 0 and let T = log(2/δ)/(2ǫ). Then
   Definition 1: Let ǫ, δ ≥ 0, and let Φ ⊆ S × S be a
                                                                     for every x, Lapǫ (x) ∈ (x − T, x + T ) with probability at least
relation on S. A randomized algorithm K taking inputs in
                                                                     1 − δ.
S and returning outputs in R is (ǫ, δ)-differentially private
                                                                        Another mechanism that is fundamental for differential
with respect to Φ if for every two inputs s1 , s2 ∈ S such that
                                                                     privacy is the Exponential mechanism [31]. Let T be the set of
s1 Φ s2 and every subset of outputs A ⊆ R,
                                                                     inputs, typically thought of as the private information. Let R
         Pr [K(s1 ) : A] ≤ exp(ǫ) Pr [K(s2 ) : A] + δ.               be a set of outputs, and consider a function F : T × R → R,
                                                                     typically called the score function. We first extend the defini-
When δ = 0, we will call this ǫ-differential privacy.                tion of sensitivity to this function.
   Our definition is a variant of the original definition of
                                                                        Definition 3: Assume F : T × R → R and let c > 0. We
differential privacy, [22] where input memories are considered
                                                                     say that F is k-sensitive on T with respect to Φ if |F (t1 , r) −
to be databases and Φ relates databases that differ in a
                                                                     F (t2 , r)| ≤ k for all t1 , t2 ∈ T such that t1 Φ t2 and r ∈ R.
single individual’s data; let us briefly explain the intuition
                                                                        Then, the Exponential mechanism can be used to output
of differential privacy in this setting. Recall that differential
                                                                     an element of R that approximately maximizes the score
privacy aims to conceal the participation of individuals in
                                                                     function, if the score function is k-sensitive.
a study. To distinguish between the participation or non-
                                                                        Theorem 2 ([31]): Let ǫ, c > 0. Suppose that F is k-
participation of an individual, we think of two databases D
                                                                     sensitive in T with respect to Φ. The Exponential mechanism2
and D′ are adjacent or neighboring if they differ only in the
                                                                     Expǫ (F, t) takes as input t ∈ T , and returns r ∈ R with
presence or absence of a single record; note that the adjacency
                                                                     probability equal to
relation is necessarily symmetric.
   Differential privacy then states that the two distributions                                   exp(ǫF (t, r)/2)
                                                                                                                      .
output by K on a pair of adjacent databases are close. In the                                                   ′
                                                                                          P
                                                                                             r ′ ∈R exp(ǫF (t, r )/2)
simple case where δ = 0, the definition above requires that the
probability of any output changes by at most a exp(ǫ) factor         This mechanism is (kǫ, 0)-differentially private with respect
when moving from one input to an adjacent input. When δ > 0          to Φ.
these bounds are still valid except with probability δ. In other        A powerful feature of differential privacy is that by com-
words, ǫ controls the strength of the privacy bound, and δ is        posing differentially private mechanisms, we can construct
the probability of failure in ensuring the privacy bound.            new mechanisms that satisfy differential privacy. However, the
      Building private programs: Let F be a deterministic            privacy guarantee will degrade: more operations on a database
computation with inputs in T and outputs in R. Suppose that          will lead to more privacy loss. In light of this composition
we want to make the computation of F (ǫ, δ)-differentially           property, we will often think of the privacy parameters ǫ and
private with respect to some relation Φ. A natural way to            δ of a program as privacy budgets that are consumed by sub-
achieve this goal is to add random noise to the evaluation           operations. This is formalized by the following composition
of F on an input. In general, the noise that we need to add          theorem.
depends not only on the ǫ and δ parameters (which control the           Theorem 3 ([30]): Let q1 be a (ǫ1 , δ1 )-differentially private
strength of the privacy guarantee), but also on the sensitivity      query and let q2 be a (ǫ2 , δ2 )-differentially private query. Then,
of F , a quantity that is closely related to Lipschitz continuity    their composition q(t) = (q1 (t), q2 (t)) is (ǫ1 + ǫ2 , δ1 + δ2 )-
for functions.                                                       differentially private.
   Definition 2: Assume that F is real-valued, i.e. R = R,              Finally, differential privacy is closed under post-
and let k > 0. We say that F is k-sensitive with respect to Φ        processing—an output of a private algorithm can be
if |F (t1 ) − F (t2 )| ≤ k for all t1 , t2 ∈ T such that t1 Φ t2 .
                                                                       2 The Exponential mechanism as first introduced by McSherry and Tal-
   A typical mechanism for privately releasing a k-sensitive
                                                                     war [31] is parameterized by a prior distribution µ on R. We consider the
function is the Laplace mechanism.                                   special case where µ is uniform; this suffices for typical applications.
arbitrarily transformed, so long as this processing does not          Here, V is a set of variables and E is a set of expressions. We
involve the private database.                                         consider expressions including simply typed lambda terms and
   Theorem 4: Let q be (ǫ, δ)-differentially private mapping          basic operations on booleans, lists and integers. (pW HILE is
databases to some output range R, and let f : R → R′ be               equipped with a standard type system; we omit the typing
an arbitrary function. Then, the post-processing f ◦ q is also        rules.)
(ǫ, δ)-differentially private.                                           The probabilistic assignments involving Lapǫ (E) and
                     III. S ELF - PRODUCTS                            Expǫ (E, E) internalize the (discrete version of the) mechanisms
                                                                      of Theorem 1 and Theorem 2 respectively. Note that for exam-
   In this section, we formalize the verification of differential-    ples based on the exponential mechanism we allow function
privacy using traditional Hoare logic. We start with some             types for representing the score functions; alternatively these
preliminary definitions and the pW HILE programming lan-              score functions can be modeled as finite maps if their domain
guage, which will serve as our source language. Then, given a         is finite (as will be the case in our examples).
probabilistic pW HILE program c, we show how to build a non-             The semantics of a well-typed pW HILE program is defined
probabilistic program T (c) that simulates two executions of c        by its (probabilistic) action on memories; we denote the set
on different inputs and tracks the privacy cost via two ghost         of memories by M. A program memory m ∈ M is a partial
variables vǫ and vδ . We show that the verification of T (c)          assignment of values to variables. Formally, the semantics of
with respect to a particular Hoare logic specification ensures        a return-free pW HILE program c is a function JcK : M →
differential privacy of the original program c.                       D(M) mapping a memory m ∈ M to a distribution JcK m ∈
A. Distributions                                                      D(M), as defined in Fig. 1.
   We define the set D(A) of sub-distributions over a set A as           For simplicity, we only consider programs of the form
the set of functions µ : AP → [0, 1] with discrete support(µ) =       c; return e in the rest of this paper. Then, the semantics of
{x | µ x 6= 0}, such that x∈A µ x ≤ 1; when equality holds,           a program c; return e is simply defined as
µ is a true distribution. (We will often refer to sub-distributions                               def
                                                                                  Jc; return eK m =   λu. 1⋆JeKu (JcK m).
as distributions when there is no confusion.) Sub-distributions
can be given the structure of a complete partial order: for all       C. Target Language
µ1 , µ2 ∈ D(A),                                                         To define the target language of our transformation, we re-
                         def
              µ1 ⊑ µ2 = ∀a ∈ A. µ1 a ≤ µ2 a.                          move probabilistic assignments and add an assert instruction,
                                                                      giving the following grammar:
  Moreover, sub-distributions can be given the structure of
a monad: for any function g : A → D(B) and distribution                C ::= skip
µ : D(A), we define g ⋆ µ : D(B) to be the sub-distribution                 | C; C                          sequencing
                             X                                              |V←E                            deterministic assignment
               g ⋆ µ (b) =
                         def
                                (g a b)(µ a),                               | assert (ϕ)                    assert
                               a∈A
                                                                            | (V, V) ← Lap⋄ǫ (E, E)         Laplace invocation
for every b ∈ B. Given an element a ∈ A, let 1a be the                      | (V, V) ← Exp⋄ǫ (E, E, E, E)   Exponential invocation
probability distribution that assigns all mass to the value a.              | if E then C else C            conditional
   We will use a normalization construction (·)# that takes as              | while E do C                  while loop
input a function f : B → R≥0 over a discrete set B and                      | return E                      return expression
returns (f )# ∈ D(B) such that the probability mass of f # at
b is given by                                                         The semantics of this non-deterministic target language is
                                      fb                              defined in Figure 2 as a function from a memory to a set of
                    (f )# b =def
                                 P           ′
                                               .                      memories. The assert (ϕ) statement checks at runtime whether
                                   b′ ∈B f b
                                                                      the predicate ϕ is valid, and stops the execution if not. In
Intuitively, sampling from the distribution (f )# is equivalent       order to distinguish the failure of assert statements from non-
to sampling “with probability proportional to” f .
                                                                                      S loops, we lift the domain P(M) with a ⊥
                                                                      terminating while
B. pW HILE Language                                                   element: where m∈⊥ f m is defined as ⊥ for any f . We defer
  pW HILE programs will serve as our source language, and             the presentation of the abstract procedures Lap⋄ and Exp⋄ until
are defined by the following grammar:                                 the definition of the self-product construction in §III-E.
                                                                         The enforcement of safety properties over this target lan-
    C ::= skip                                                        guage is formalized by a standard Hoare logic, with judgments
         | C; C                    sequencing                         of the form
         | V ←E                    deterministic assignment                                    ⊢ c : Ψ =⇒ Φ.
         | V←  $ Lap (E)
                    ǫ              Laplace assignment
         | V←  $ Exp (E, E)
                    ǫ              Exponential assignment             Here the pre- and post-conditions Ψ and Φ are standard
         | if E then C else C      conditional                        unary predicates over memories. Hoare logic judgments can
         | while E do C            while loop                         be derived using the rules in Fig. 3; by the standard soundness
         | return E                return expression                  of Hoare logic, the derivability of a judgment ⊢ c : Ψ =⇒ Φ
                         JskipK m                  = 1m
                         Jc1 ; c2 K m              = Jc2 K⋆ (Jc1 K m)
                         Jx ← eK m                 = 1m{JeKE m/x}
                                                                        ⋆              #
                            $ Lap (e)K m
                         Jx ←    ǫ                 = λv. 1m{v/x}      λr.exp − ǫ|r−JeK
                                                                                   2
                                                                                       m|


                                                                 ⋆                      #
                            $ Exp (s, e)K m
                         Jx ←    ǫ                 = λv. 1m{v/x}      λr.exp ǫJsKm(JeKm,r)
                                                                                   2

                         Jif e then c1 else c2 K m = if (JeKE m = true) then (Jc1 K m) else (Jc2 K m)
                                                     F
                         Jwhile e do cK m          =    wi m
                              where w0 m          = ⊥
                                       wi+1 m = if (JeKE m = true) then wi⋆ (JcK m) else unit m

                                                   Fig. 1: pW HILE semantics


                   JskipK m                              = {m}
                                                           S
                   Jc1 ; c2 K m                          = m′ ∈Jc1 K m Jc2 K m
                   Jx ← eK m                             = 1m{JeKE m/x}
                   Jassert (ϕ)K m                        = if (JϕKE m) then {m} else ⊥
                   J(x1 , x2 ) ← Lap⋄ǫ (e1 , e2 )K m
                                                                S
                                                               = v m {v/x1 } {v/x2 } {vǫ + |e1 − e2 |ǫ/vǫ}
                   J(x1 , x2 ) ← Exp⋄ǫ (s1 , e1 , s2 , e2 )K m = if (Js1 = s2 KE m = true) then
                                                                  S
                                                                   v m {v/x1 } {v/x2 } {vǫ + |e1 − e2 |ǫ/vǫ }
                                                             else ⊥
                   Jif e then c1 else c2 K m             = if (JeKE m = true) then (Jc1 K m) else (Jc2 K m)
                                                           F
                   Jwhile e do cK m                      =     ŵi m
                          where ŵ0 m          = ∅
                                               = if (JeKE m = true) then m′ ∈(JcK m) ŵi m′ else {m}
                                                                        S
                                  ŵi+1 m

                                            Fig. 2: Semantics of the target language


entails the correctness of c with respect to its specification        rable if they manipulate disjoint sets of program variables. In
Ψ, Φ.                                                                 order to achieve separability in the construction of the product
                                                                      of a program with itself, program variables are duplicated and
D. Product Construction
                                                                      marked with a left (−1 ) or right (−2 ) tag. For any program
   Before we define the product transformation from pW HILE           expression e or predicate ϕ, we let ei and ϕi stand for the
to our target language, let us first review some preliminaries        result of renaming every program variable with the tag −i .
about product programs.
   Product programs have been successfully used to verify 2-             Similarly, we say that two memories are disjoint when their
safety properties like information-flow, program equivalence,         domains (the sets of variables on which they are defined) are
and program robustness. As mentioned in in the introduction,          disjoint. Given two disjoint memories m1 and m2 , we can
a synchronized product program can be used to simulate two            build a memory m = m1 ⊕ m2 representing their (disjoint)
runs of the same program, interleaving the two executions             union. In the following, we exploit separability and use
and often simplifying the verification effort. This technique,        predicates to represent binary relations over disjoint memories
however, has been mostly used in the verification of non-             m1 and m2 . We will suggestively write m1 Φ m2 to denote
probabilistic programs. In the rest of this section we provide        the unary predicate Φ(m1 ⊕ m2 ) over the combined memory
a brief introduction to relational verification by product con-       m1 ⊕ m2 .
struction and then extend the approach to handle quantitative           Given two deterministic programs c1 and c2 , a general
reasoning over probabilistic programs.                                product program c1 ×c2 is a syntactic construction that merges
   A simple but necessary concept for the product construction        the executions of c1 and c2 ; this construction is required to
is memory separability: we say that two programs are sepa-            correctly represent every pair of executions of c1 and c2 .
                       ⊢ skip : Ψ =⇒ Ψ         ⊢ x ← e : Φ {e/x} =⇒ Φ           ⊢ assert (ϕ) : Φ ∧ ϕ =⇒ Φ
                    ⊢ c1 : Ψ =⇒ ϕ         ⊢ c2 : ϕ =⇒ Φ         ⊢ c1 : Ψ ∧ b =⇒ Φ         ⊢ c2 : Ψ ∧ ¬b =⇒ Φ
                            ⊢ c1 ; c2 : Ψ =⇒ Φ                         ⊢ if b then c1 else c2 : Ψ =⇒ Φ
           Ψ ∧ v ≤ 0 ⇒ ¬b      ⊢ c : Ψ ∧ b ∧ v = k =⇒ Ψ ∧ v < k              ⊢ c : Ψ′ =⇒ Φ′     Ψ ⇒ Ψ′             Φ′ ⇒ Φ
                      ⊢ while b do c : Ψ =⇒ Ψ ∧ ¬b                                       ⊢ c : Ψ =⇒ Φ

                                       Fig. 3: Hoare logic for non-probabilistic programs


Traditional program verification techniques can then be used           ⌈skip⌉              = skip
to enforce a relational property over c1 and c2 .
                                                                       ⌈c1 ; c2 ⌉          = ⌈c1 ⌉; ⌈c2 ⌉
   In self-composition [7], [18], the product construction c1 ×
                                                                       ⌈x ← e⌉             = x1 ← e1 ; x2 ← e2
c2 is defined simply by the sequential composition c1 ; c2 .
An inconvenience of self-composition is that the verification          ⌈x ← $ Lap (e)⌉
                                                                                  ǫ        = (x1 , x2 ) ← Lap⋄ (e1 , e2 )
of c1 ; c2 usually requires independent functional reasoning           ⌈x ← $ Exp (s, e)⌉
                                                                                  ǫ        = (x1 , x2 ) ← Exp⋄ (s1 , e1 , s2 , e2 )
over c1 and c2 . The synchronized product construction solves          ⌈if b then c else d⌉= assert (b1 = b2 );
this problem by interleaving execution of two runs of the                                    if b1 then ⌈c⌉ else ⌈d⌉
same program—by placing corresponding pieces of the two                ⌈while b do c⌉      = assert (b1 = b2 );
executions of a program close together, synchronized product                                 while b1 do
programs can more easily maintain inductive invariants relat-                                   ⌈c⌉; assert (b1 = b2 )
ing the two runs. Not only does synchronization reduce the
verification effort, we will soon see that synchronization is                      Fig. 5: Self-product construction
the key feature that enables our verification approach.

                                                                    F. An alternative characterization of privacy
E. Building the Product                                                For the proof of soundness, we will use an alternative char-
                                                                    acterization of (ǫ, δ)-differential privacy based on the notion of
   We embed the quantitative reasoning on probabilistic pro-        ǫ-distance. This notion is adapted from the asymmetric notion
grams by introducing the special program variables vǫ and           of distance used by Barthe et al. [11].
vδ , which serve to accumulate the privacy cost. For every             Definition 4 (ǫ-distance): The ǫ-distance ∆ǫ is defined as
statement c, the self-product ⌈c⌉ is formally defined by the                                 def
rules shown in Fig. 5. In a nutshell, the deterministic fragment              ∆ǫ (µ1 , µ2 ) =    max (µ1 S − exp(ǫ) µ2 S),
                                                                                                 S⊆A
of the code is duplicated with appropriate variable renaming                      def
                                                                                      P
with the flags −1 and −2 , and the control flow is fully            where µ S =          a∈S µ a. We define max over an empty set
synchronized, i.e., the two executions of the same program          to be 0, so ∆ǫ (µ1 , µ2 ) ≥ 0.
must take all the same branches—we use the assert statements           By the definition of ǫ-distance, a probabilistic program c
to enforce this property.                                           is (ǫ, δ)-differentially private with respect to ǫ > 0, δ ≥ 0,
                                                                    and a relation Φ on the initial memories of c if for every two
   Moreover, for the self-product of a program c to correctly
                                                                    memories m1 and m2 related by Φ, we have
represent two executions of itself, we require that loop guards
do not depend on probabilistically sampled values; we assume                           ∆ǫ (JcK m1 , JcK m2 ) ≤ δ.
in the remainder of this work that the programs under veri-
fication satisfy this condition. Additionally, the soundness of        The proof of our main theorem relies on a lifting oper-
the method relies on the fact that all verified programs are        ator that turns a relation on memories into a relation on
terminating, which is enforced by the Hoare logic rules in          distributions over memory. Given a relation on memories Φ,
Fig. 3.                                                             and real values ǫ, δ we define the lifted relation on memory
                                                                    distributions Φhǫ,δi as follows.
   The probabilistic constructions are mapped to invocations
                                                                       Definition 5: For all memory distributions µ1 , µ2 ,
to the abstract procedures Lap⋄ and Exp⋄ . The semantics of
                                                                    µ1 Φhǫ,δi µ2 if there exists µ such that:
these procedures is non-deterministic, in order to simulate
sampling from a probability distribution. We axiomatize these          1) πi µ ≤ µi ,
abstract procedures with Hoare specifications: Figure 4 gives          2) ∀m1 , m2 . µ(m1 ⊕ m2 ) ⇒ m1 Φ m2 , and
the new specifications. Notice that both abstract procedures           3) ∆ǫ (µi , πi µ) ≤ δ,
have a side effect: they increment the privacy budget variable      where
                                                                                        P
                                                                       • (π1 µ) m1 =
vǫ . In Section V-C, we introduce a alternative specification for                       Pm2 ∈M µ (m1 , m2 ), and
Lap⋄ that also increments the budget variable vδ .                     • (π2 µ) m2 =      m1 ∈M µ (m1 , m2 ).
                    ⊢ (x1 , x2 ) ← Lap⋄ǫ (e1 , e2 ) : vǫ = ǫ0 ∧ vδ = δ0 =⇒ x1 = x2 ∧ vǫ = ǫ0 + |e1 − e2 |ǫ ∧ vδ = δ0

   ⊢ (x1 , x2 ) ← Exp⋄ǫ (s1 , e1 , s2 , e2 ) : s1 = s2 ∧ vǫ = ǫ0 ∧ vδ = δ0 =⇒ x1 = x2 ∧ vǫ = ǫ0 + ǫ maxr |s1 (x1 , r) − s2 (x2 , r)|

                                                 Fig. 4: Hoare specification for Lap⋄ and Exp⋄


Notice that ǫ-distance between distributions is closely related                to the fragment consisting of the first and third set of rules
to the lifting of the equality relation, i.e.,                                 as core apRHL; its rules are displayed in Fig. 6. Note that
                                                                               the, in contrast with [11], the rule for sequential composition
              µ1 =hǫ,δi µ2      ⇐⇒       ∆ǫ (µ1 , µ2 ) ≤ δ.             (1)
                                                                               does not have any side condition; this is due to the fact that
Note that the second equation is precisely the condition on                    the rule for random assignments in [11] allows sampling from
output distributions needed for (ǫ, δ)-differential privacy.                   strict sub-distributions, whereas we only allow sampling using
                                                                               the Laplace and Exponential mechanisms.
G. Soundness of the self-product technique                                        The following lemma shows that our approach subsumes
   We can now state the soundness theorem for our approach.                    core apRHL, in the sense that every probabilistic program c
Recall that we consider only programs with a single return                     verified (ǫ, δ)-differentially private using core apRHL can be
statement; we will label this returned value out1 and out2 in                  verified using our self-product technique.
the first and second runs, respectively.                                          Lemma 3: For every probabilistic program c, memory re-
   Theorem 5: If the following Hoare judgment is valid                         lations Ψ, Φ and real expressions ǫ, δ such that the following
⊢ ⌈c⌉ : Ψ ∧ vǫ = 0 ∧ vδ = 0 =⇒ out1 = out2 ∧ vǫ ≤ ǫ ∧ vδ ≤ δ                   core apRHL judgment is derivable

then c satisfies (ǫ, δ)-differential privacy.                                                      ⊢ c ∼hǫ,δi c : Ψ =⇒ Φ
The proof of Theorem 5 follows from the next lemma.                            we have
  Lemma 2: Let Φ be a relation on memories, and suppose
                                                                                            ⊢ ⌈c⌉ : Ψ =⇒ Φ ∧ vǫ ≤ ǫ ∧ vδ ≤ δ.
    ⊢ ⌈c⌉ : Ψ ∧ vǫ = 0 ∧ vδ = 0 =⇒ Φ ∧ vǫ ≤ ǫ ∧ vδ ≤ δ.
                                                                               The proof of this result is straightforward, by induction on the
Then, for all memories m1 , m2 such that m1 Ψ m2 , we have                     derivation of the apRHL judgement.
                       (JcK m1 ) Φhǫ,δi (JcK m2 ).                                The embedding is more expressive than core apRHL in
                                                                               its treatment of loops. This is because privacy consumption
The lemma is proved by structural induction on c; we provide                   in core apRHL is tracked by an accumulator which is part
technical details in the full version of the paper.                            of the judgment itself, independent of the pre-condition and
                 IV. C OMPARISON WITH apRHL                                    the initial memory. Using self-products, reasoning about the
                                                                               privacy budget is carried out in the Hoare specification and
  Now that we have defined our transformation, we com-                         consequently inherits the full expressivity of the Hoare logic.
pare our approach to a custom logic for verifying privacy.                     On the other hand, we have not been able to capture the
apRHL [11] is a quantitative, probabilistic and relational                     generalized rule for loops from apRHL, which is given in
program logic for reasoning about differential privacy, with                   Fig. 7, with self-products. In the following section, we provide
judgments of the form3                                                         a more detailed comparison with apRHL based on examples.
                      ⊢ c1 ∼hα,δi c2 : Ψ =⇒ Φ,                                    We conclude with a broader perspective on the two for-
                                                                               malisms. The primary goal of our approach is to strike a good
where c1 and c2 are probabilistic programs, Ψ and Φ are                        balance between expressivity and simplicity, including for the
memory relations, and ǫ, δ are real values. The main result of                 latter ease of use and ease of implementation. In contrast to
apRHL states that if ⊢ c1 ∼hǫ,δi c2 : Ψ =⇒ out1 = out2 is                      apRHL, which requires a relational verification infrastructure,
derivable, where c1 and c2 are the result of renaming variables                our approach reuses a very standard verification technology,
in c to make them separable, then c is (ǫ, δ)-differentially                   namely Hoare logic, and can be directly implemented by
private with respect to the relation Ψ on initial memories.                    defining the appropriate program transformation, and using
   The original presentation of the apRHL logic [11] is or-                    off-the-shelf tools for Hoare logic or even invariant generation.
ganized in three sets of rules: the first set includes a set of                We believe this latter approach is simpler to deploy for
core rules, the second set includes a generalized rule for loops               programming languages for which verification environments
(see Fig. 7), and the third set includes rules for mechanisms                  based on Hoare logic are already available.
such as the Laplace and Exponential Mechanism. We refer
                                                                                                       V. E XAMPLES
  3 The original apRHL rules are based on a multiplicative privacy budget.
We adapt the rules to an additive privacy parameter for consistency with the     In this section, we apply our method to four examples.
rest of the article.                                                           The first example (smart sum) is an algorithm for computing
                                                                                                       [assn]
                                    ⊢ x1 ← e1 ∼h0,0i x2 ← e2 : Φ {e1 /x1 } {e2 /x2 } =⇒ Φ

                                                                                                               [lap]
                                    $ Lap (e ) ∼
                               ⊢ y1 ←    ǫ 1    h|e1 −e2 |ǫ,0i y2 ← Lapǫ (e2 ) : true =⇒ y1 = y2
                                                                  $




                                                                                                                                [exp]
                     $ Exp (s , e ) ∼
                ⊢ y1 ←    ǫ 1 1      hǫ maxr |s1 (x1 ,r)−s2 (x2 ,r)|,0i y2 ← Expǫ,s (s2 , e2 ) : s1 = s2 =⇒ y1 = y2
                                                                           $




                                                                                     [skip]
                                                     ⊢ skip ∼h0,0i skip : Ψ =⇒ Ψ

                               ⊢ c1 ∼hǫ,δi c2 : Ψ ∧ b1 =⇒ Φ        ⊢ d1 ∼hǫ,δi d2 : Ψ ∧ ¬b1 =⇒ Φ
                                                                                                                 [cond]
                          ⊢ if b1 then c1 else d1 ∼hǫ,δi if b2 then c2 else d2 : Ψ ∧ b1 = b2 =⇒ Φ

                                        ⊢ c1 ∼hǫ,δi c2 : Θ ∧ b1 ∧ k = e =⇒ Θ ∧ k < e
                                        Θ ∧ n ≤ e =⇒ ¬b1           Θ =⇒ b1 = b2
                                                                                                               [while]
                             ⊢ while b1 do c1 ∼hnǫ,nδi while b2 do c2 : Θ ∧ 0 ≤ e =⇒ Θ ∧ ¬b1

                                     ⊢ c1 ∼hǫ,δi c2 : Ψ =⇒ Φ′         ⊢ c′1 ∼hǫ′ ,δ′ i c′2 : Φ′ =⇒ Φ
                                                                                                       [seq]
                                              ⊢ c1 ; c′1 ∼hǫ+ǫ′ ,δ+δ′ i c2 ; c′2 : Ψ =⇒ Φ

                        ⊢ c1 ∼hǫ′ ,δ′ i c2 : Ψ′ =⇒ Φ′       Ψ ⇒ Ψ′          Φ′ ⇒ Φ            ǫ′ ≤ ǫ         δ′ ≤ δ
                                                                                                                      [weak]
                                                      ⊢ c1 ∼hǫ,δi c2 : Ψ =⇒ Φ
                                Fig. 6: Core proof rules of the approximate relational Hoare logic


               Θ =⇒ b1 h1i ≡ b2 h2i ∧ P h1i ≡ P h2i ∧ ih1i = ih2i             Θ ∧ n ≤ ih1i =⇒ ¬b1 h1i
               ⊢ c1 ; assert (¬P ) ∼hǫj ,0i c2 ; assert (¬P ) : Θ ∧ (b1 ∧ i = j ∧ ¬P )h1i =⇒ Θ ∧ ih1i = j +1
               ⊢ c1 ; assert (P ) ∼hǫ,0i c2 ; assert (P ) : Θ ∧ (b1 ∧ i = j ∧ ¬P )h1i =⇒ Θ ∧ ih1i = j +1
               ⊢ c1 ∼h0,0i c2 : Θ ∧ (b1 ∧ i = j ∧ P )h1i =⇒ Θ ∧ (i = j +1 ∧ P )h1i
                                                                                                                           [gwhile]
                     ⊢ while b1 do c1 ∼hǫ+Pn−1 ǫi ,0i while b2 do c2 : Θ ∧ ih1i = 0 =⇒ Θ ∧ ¬b1 h1i
                                               i=0


                                                  Fig. 7: Generalized rule for loops



statistics; it involves intricate applications of the composition       are the same length T , at most one entry differs between the
theorem, and is thus an interesting test case. The second               two databases, and that entry differs by at most 1.
example (Iterative Database Construction, or more precisely                Suppose we want to release private sums of the first i
the Multiplicative Weights Exponential Mechanism) is an                 entries, simultaneously for every i ∈ [1 . . . T ]: that is, given
algorithm that computes a synthetic database; it combines the           [r1 , r2 , r3 , r4 , . . . , rT ] we want to privately release
Laplace and the Exponential mechanisms, and has not been                                 "          2       3      4              T
                                                                                                                                      #
                                                                                                  X         X      X              X
verified in earlier work using relational logic. The third exam-                            r1 ,       ri ,   ri ,   ri , . . . ,   ri .
ple (Propose-Test-Release) is an algorithm that only achieves                                 i=1      i=1      i=1            i=1
approximate differential privacy (i.e., (ǫ, δ)-differential privacy        An interesting sophisticated differentially private algorithm
with δ > 0) using both the privacy and accuracy properties              for this problem is the two-level counter from Chan, et al. [14];
of the Laplace distribution. To best of our knowledge, we               we call this algorithm smartsum.
provide the first machine-checked proof of this mechanism.                 At a high level, this algorithm groups the input list into
Finally, our last example (vertex cover) is an algorithm that           blocks of length q, and adds Laplace noise to the sum for
achieves differential privacy by carefully adding noise to              each block. More concretely, to compute a running sum from
sampled values; this example can only be verified partially             1 to t with t a multiple of q, we simply add together the first
using our method, and illustrates the differences with apRHL.           t/q block sums. If t is not a multiple of q, say t = qs + r
                                                                        with r < q, we take the first s block sums and add a noised
A. Smart sum
                                                                        version of each of the r remaining elements.
   In this example, a database db is a list of real numbers                For an example, suppose we take q = 3 and T is a multiple
[r1 , . . . , rT ] and we consider two databases adjacent if they       of 3. For brevity, let us use the notation L(r) to describe the
result of the application of Laplace, for a fixed value ǫ to r.                                   next ← 0; n ← 0; c ← 0;
Then, the output of smartsum is                                                                   while 0 < length l do
                                                                                                     if length l mod q = 0 then
  "                                       3
                                                      !                                                 x ← Lap ǫ (c + hd l);
                                                                                                        n ← x + n;
                                          X
    L (r1 ) , L (r1 ) + L (r2 ) , L              ri       ,
                                           i=1                                                          next ← n;
                 3
                            !                         T /3        3
                                                                             !                         c ← 0;
                                                                                                        out ← next :: out;
                 X                                    X           X
             L         ri       + L (r4 ) , . . . ,           L         r3j+i  .
                 i=1                                  j=0         i=1                              else
                                                                                                        x ← Lap ǫ (hd l);
   To informally argue privacy, observe that if we run the                                              next ← next + x;
Laplace mechanism on each individual entry, there is no pri-                                            c ← c + hd l;
vacy cost for the indices where the adjacent databases are the                                          out ← next :: out;
same. So, the privacy analysis for smartsum is straightforward:                                      l ← tl l;
changing an input element will change exactly two noisy                                           return out;
sums—the sum for the block containing i, and the noisy
version of i—and each noisy sum that can change requires                                         (a) Original probabilistic algorithm
ǫ privacy budget, since we are using the Laplace mechanism                          vǫ ← 0; next1 ← 0; next2 ← 0;
with parameter ǫ. Thus, smartsum is 2ǫ-private.                                     n1 ← 0; n2 ← 0; c1 ← 0; c2 ← 0;
   The full program, together with the transformation into a                        assert ((0 < length l1 ) ⇔ (0 < length l2 ));
synchronized product program, is presented in Fig. 8. The                           while 0 < length l1 do
formal verification of the 2ǫ-differential privacy follows the                         assert ((length l1 mod q = 0) ⇔ (length l2 mod q = 0));
argument above. The pre-condition states that the two input                            if length l1 mod q = 0 then
databases are adjacent, while the post-condition requires equal-                          (x1 , x2 ) ← Lap⋄ǫ (c1 + hd l1 , c2 + hd l2 ));
ity on the outputs and bounds the accumulated privacy budget                              n1 ← x1 + n1 ; n2 ← x2 + n2 ;
by 2ǫ.                                                                                    next1 ← n1 ; next2 ← n2 ;
   The interesting part for our verification is the while loop.                           c1 ← 0; c2 ← 0;
Indeed, this requires a loop invariant to keep track of the                               out1 ← next1 :: out1 ; out2 ← next2 :: out2 ;
privacy budget, which depends on whether the differing entry                         else
has been processed or not. Note that this invariant does not fit                          (x1 , x2 ) ← Lap⋄ǫ (hd l1 , hd l2 ));
the core apRHL while rule of Fig. 6: to deal with this example,                           next1 ← next1 + x1 ; next2 ← next2 + x2 ;
Barthe et al. [11] use the generalized while rule from Fig. 7.                            c1 ← c1 + hd l1 ; c2 ← c2 + hd l2 ;
This rule is able to perform a refined analysis depending on                              out1 ← next1 :: out1 ; out2 ← next2 :: out2 ;
a predicate that is preserved across the first iterations, until                       l1 ← tl l1 ; l2 ← tl l2 ;
some critical iteration is reached. In contrast, here we do not                     return (out1 , out2 );
require any special verification rule: the standard while rule
from Hoare logic suffices.                                                                   (b) Synchronized non-probabilistic product
   More precisely, we apply the Hoare while rule with the                                          Fig. 8: smartsum algorithm
invariant:

  adjacent(l1 , l2 ) ∧ out1 = out2 ∧ next1 = next2 ∧ n1 = n2 ∧
  |c1 − c2 | ≤ 1 ∧ (l1 6= l2 ⇒ vǫ = 0)∧                          B. Multiplicative Weights Exponential Mechanism
  (c1 6= c2 ⇒ l1 = l2 ∧ vǫ ≤ ǫ) ∧ (l1 = l2 → vǫ ≤ 2 ǫ)
                                                                    While answering queries on a database with the Laplace
Notice from the invariant that if the accumulators c1 and c2 mechanism is a simple way to guarantee privacy, the added
differ we have l1 = l2 . This corresponds to the fact that noise quickly renders the results useless as the number of
the differing entry has been processed and so the remaining queries grows. To handle larger collections of queries, there
database entries coincide. Also, if this is the case then the has been much research on sophisticated algorithms based on
privacy budget of 2 ǫ has been already consumed.                 learning theory.
   The verification of this invariant proceeds by case analysis.    One such scheme is Iterative Database Construction (IDC),
We have three cases: a) the differing entry has not been due to Gupta et al. [27]. The basic idea is simple: given a
processed yet and will not be processed in the following database d,       ˆ the algorithm gradually builds a synthetic database
iteration, b) the differing entry has not been processed yet that approximates the original database. The synthetic database
but is going to be processed in the next iteration, and c) the is built over several rounds; after some fixed number of rounds,
differing entry has already been processed, in which case there the synthetic database is released and used to answer all
is no more privacy budget consumption.                           queries.
   The essence of the algorithm is the computation that it                          i ← 0;
performs at each round. Let Q be a collection of queries                            d0 ← def;
that we want to answer and let di be the synthetic database                         while i < T do
computed at round i. During round i + 1, the algorithm selects                         si ← λD Q. |Q(di ) − Q(D)|
                                                                                                        ˆ
                                                                                       q i ← Expǫ (si , d);
a query q ∈ Q with high error; that is, a query where the
                                                                                         i          i ˆ
current approximate database di and the true database dˆ give                          a ← Lapǫ (q d);
very different answers. This selection is done in a differentially                     di+1 ← update (di , ai , q i );
private way. Next, the algorithm computes a noisy version                              i ← i + 1;
v of q evaluated on the true database d.     ˆ Again, this step                     return dT ;
must be differentially private. Finally, q, v and the current
database di approximation are fed into an update algorithm,                         (a) Original probabilistic algorithm
which generates the next approximation di+1 of the synthetic
                                                                                  vǫ ← 0; i1 ← 0; i2 ← 0;
database (hopefully performing better on q).
                                                                                  d01 ← def; d02 ← def;
   The idea is that in many cases, this iterative procedure
                                                                                  assert (i1 < T ⇔ i2 < T );
will provably find an approximation with low error on all
                                                                                  while i1 < T do
queries in Q in a small number of steps. Hence, we can
                                                                                     si1 ← λD Q. |Q(di1 ) − Q(D)|;
run IDC for a small number of steps, and release the final
                                                                                     si2 ← λD Q. |Q(di2 ) − Q(D)|;
database approximation as the output. Queries in Q can then
be evaluated on this output for an accurate estimate of the true                     (q1i , q2i ) ← Exp⋄ǫ (si1 , dˆ1 , si2 , dˆ2 );
answer to the query.                                                                 (ai1 , ai2 ) ← Lap⋄ǫ (q1i (dˆ1 ), q2i (dˆ2 ));
   IDC is actually a family of algorithms parameterized by                           di+1
                                                                                       1     ← update (di1 , ai1 , q1i );
                                                                                       i+1
an algorithm to privately find a high-error query (called the                        d2 ← update (di2 , ai2 , q2i );
private distinguisher), and the update function (called the                          i1 ← i1 + 1;
database update algorithm). For concreteness, let us consider                        i2 ← i2 + 1;
one well-studied instantiation, the Multiplicative Weights Ex-                       assert (i1 < T ⇔ i2 < T );
ponential Mechanism (MWEM) algorithm originally due to                            return (dT1 , dT2 );
Hardt and Rothblum [29] and experimentally evaluated by
Hardt et al. [28].                                                               (b) Synchronized non-probabilistic product
   MWEM uses the exponential mechanism to privately select                              Fig. 9: MWEM algorithm
a query with high error—the quality score of a query q to
be maximized is the error of the query, i.e., the absolute
difference between q evaluated on the approximate database           composition theorem, it is sufficient to analyze the privacy
di and q evaluated on the true database d. ˆ The update function     budget consumed by each iteration. Each iteration, we select a
applies the multiplicative weights update [3] to adjust the          query with the exponential mechanism with privacy parameter
approximation to perform better on the mishandled query. This        ǫ, and we estimate the true answer of this query with the
step is non-private: it does not touch the private data directly.    Laplace mechanism, parameter ǫ. By the composition theorem
Hence, we do not concern ourselves with the details here, and        (Theorem 3), the whole algorithm is private with parameter
treat the update step as a black box. (The reader can find           2 · T · ǫ = 2T ǫ, as desired. The proof can be transcripted
further details in Hardt et al. [28].) The full program, together    directly into Hoare logic using self-products; we take as pre-
with the transformation into a synchronized product program,         condition adjacency of the two databases, and use adjacency
is presented in Fig. 9.                                              to conclude that the sensitivity of the score function si is 1 at
   We briefly comment on the program. We let di denote the           each iteration.
i-th iteration of the synthetic database, and dˆ denote the true
database. Initially the synthetic database d0 is set to some         C. Propose-Test-Release
default value def. Then we define the score function si that           The examples we have considered so far all rely on the
takes as inputs a database D and a query Q and returns               composition theorem. While this is a quite powerful and
the error of the query Q on the current approximation di             useful theorem, not all algorithms use composition. In this
compared to D. We then apply the exponential mechanism               section, we consider one such example: the Propose-Test-
to the true database dˆ with the score function si , and we call     Release (PTR) framework [21], [36]. PTR is also an example
the result q i . We then evaluate q i on the real database, and      of an (ǫ, δ)-differentially private mechanism for δ > 0.
add Laplace noise; we call the result ai . Finally, we apply           The motivation comes from private release of statistics that
the update function to obtain the next iteration di+1 of the         are sometimes, but not always, very sensitive. For example,
synthetic database. Once the number of rounds is exhausted,          suppose our database is an ordered list of numbers between 0
we return the last computed synthetic databases.                     and 1000, and suppose we want to release the median element
   For the privacy proof, we assume that all queries in Q are        of the database. This can be highly sensitive: consider the
1-sensitive. Note that we run T iterations of MWEM; by the           database [0, 0, 1000] with median 0. Adding a record 1000
                 x ← DistToInstability (q, d);
                 y ← Lap ǫ x;
                                                                       {∆(d1 , d2 ) ≤ 1}
                 if (|y| > log(2/δ)/(2ǫ))
                                                                       vǫ ← 0;
                    return (q d);
                                                                       vδ ← 0;
                 else
                                                                       x1 ← DistToInstability (q, d1 );
                    return (⊥);
                                                                       x2 ← DistToInstability (q, d2 );
                                                                                                            
                                                                           (q(d1 ) = q(d2 ) ∨ x1 = x2 = 0)
                    Fig. 10: PTR algorithm
                                                                           ∧vǫ = 0 ∧ vδ = 0
                                                                                         ⋄
                                                                        , y2 ) ← Lapǫ (x1 , x2 );
                                                                       (y 1                                   
                                                                        (q(d1 ) = q(d2 )) ∨ (x1 = x2 = 0 
to the database would lead to a large change in the median                  ∧|y1 − x1 | ≤ log(2/δ)/(2ǫ))
(now 500, if we average the two elements closest to the                
                                                                            ∧y1 = y2 ∧ vǫ ≤ ǫ ∧ vδ ≤ δ
                                                                                                              
median when the database has even size). However, many                    assert (|y1 | > log(2/δ)/(2ǫ) ⇔ |y2 | > log(2/δ)/(2ǫ));
other databases have low sensitivities: for [0, 10, 10, 1000],
the median will remain unchanged (at 10) no matter what                    1 | > log(2/δ)/(2ǫ))
                                                                       if (|y
                                                                              q(d1 ) = q(d2 ) ∧ vǫ ≤ ǫ ∧ vδ ≤ δ
element we add or remove from the database. We may hope                   return  (q(d1 ), q(d2 ));
that we can privately compute the median in this second case              
                                                                              out1 = out2 ∧ vǫ ≤ ǫ ∧ vδ ≤ δ
with much less noise than needed for the first case. More              else
generally, the second database is quite stable—all adjacent                   vǫ ≤ ǫ ∧ vδ ≤ δ
databases have the same median value. In contrast, the first              return  (⊥, ⊥);
database is instable—adjacent databases may have wildly                   
                                                                              out1 = out2 ∧ vǫ ≤ ǫ ∧ vδ ≤ δ
different median values. With this example in mind, we now
explain the general PTR framework.
                                                                                Fig. 11: Proof of Propose-Test-Release
   Suppose we want to privately release the result of a query q
evaluated on a database d. We assume that databases are taken
from a set D and that there exists a notion of distance ∆ on            More formally, the proof of (ǫ, δ)-differential privacy for
D, such that pairs of input memory related by Φ correspond           PTR rests on two properties of the Laplace mechanism: the
to databases at distance at most 1 under ∆. First, we estimate       privacy property captured by Theorem 1 and the accuracy
the distance to instability—that is, the largest distance x such     property captured by Lemma 1.
that q(d) = q(d′ ) for all databases d′ at distance x or less from      Fig. 11 presents the proof of PTR using the synchronized
d. Since this a 1-sensitive function (moving to a neighboring        product program—the code is interleaved with some of the
database can change the distance to instability by at most           pre- and post-conditions. The proof uses the accuracy property
1), we can release this distance privately using the Laplace         of the Laplace mechanism and the properties of the distance
mechanism (say, with parameter ǫ). Call the result y. Now,           to instability that we give as specifications in Fig. 12. For
we compare y to a threshold t (to be specified later). If y is       simplicity, we treat distance to instability as an abstract
less than the threshold, we output q(d) with no noise. If y is       procedure; however, it can be implemented as a loop over
greater than the threshold, we output a default value ⊥. The         all databases, in which case the specification can be proved.
program is given in Fig. 10.                                         The soundness of the accuracy specification for the Laplace
   The privacy of the algorithm can be informally justified in       mechanism follows by Lemma 1.
two parts. First, suppose that instead of outputting q(d) or
⊥, we simply output which branch the program took. This is           D. Vertex cover
ǫ-differentially private: computing y is ǫ-differentially private       A vertex cover for a graph g = (N, E) is a set S of nodes
(via the Laplace mechanism), and the resulting branch is a           such that for every edge (t, u) ∈ E, either t ∈ S or u ∈ S.
post-processing of y. Hence, we can assume that the same             The minimum vertex cover is the problem of finding a vertex
branch is taken in both executions.                                  cover of a minimum size. Gupta et al. [26] study the problem
   Second, we can conclude that the original program (out-           of privately computing a minimum vertex cover in a setting
putting q(d) or ⊥) is (ǫ, δ)-differentially private if for any       where the nodes of the graph are public, but its edges are
adjacent databases d and d′ with q(d) 6= q(d′ ), the first           private. Since a vertex cover leaks information about vertices
branch is taken with probability at most δ. By properties of the     (for instance, any two nodes that are not in the vertex cover are
Laplace mechanism, we can set the threshold t large enough           certainly not connected by an edge), their algorithm outputs
so that with probability at least 1 − δ, the first branch is only    an enumeration of the nodes of the graph, from which a vertex
taken if x is strictly positive. In this case we can conclude        cover can be recomputed efficiently from the knowledge of the
q(d) = q(d′ ), since q(d) 6= q(d′ ) implies that x is 0 on both      set E. Their algorithm is challenging to verify because rather
executions. So, we can safely release q(d) = q(d′ ) with no          than relying on mechanisms, it achieves privacy by sampling
noise. Of course, if the second branch is taken, then it is also     according to a suitable noisy distribution choose. The code of
safe to release ⊥ in both runs.                                      the algorithm is shown in Fig. 13.
            ⊢ (y1 , y2 ) ← Lap⋄ǫ (x1 , x2 ) : x1 = x2 ∧ vδ = δ̂ =⇒ y1 = y2 ∧ |y1 − x1 | ≤ log(2/δ)/(2ǫ) ∧ vδ = δ̂ + δ
      ⊢ x1 ← DistToInstability (q, d1 ); x2 ← DistToInstability (q, d2 ) : ∆(d1 , d2 ) ≤ 1 =⇒ q(d1 ) = q(d2 ) ∨ x1 = x2 = 0

           Fig. 12: Accuracy specification for the Laplace mechanism, and specification for distance to instability.


                     n ← |E|;                                      offered by the self-product construction. The code for these
                     out ← [ ];                                    examples (and others) is available online [1].
                     while g 6= ∅ do
                        v ← chooseǫ,n (g);                                              VI. R ELATED WORK
                        out ← v :: out;
                        g ← g \ {v};                                  Differential privacy, first proposed by Blum et al. [13] and
                     return out;                                   formally defined by Dwork et al. [22], has been an area
                                                                   of intensive research in the last decade. We have touched
                                                                   on a handful of private algorithms, including algorithms for
               Fig. 13: Minimum vertex cover
                                                                   computing running sums [14], [23] (part of a broader literature
                                                                   on streaming privacy), answering large classes of queries [29],
                                                                   [28] (part of a broader literature on learning-theoretic ap-
   We say that two graphs g1 and g2 are adjacent if they differ
                                                                   proaches to data privacy), the Propose-Test-Release framework
at most in one edge ht, ui. By defining choose as
                                                                   for answering stable queries in a noiseless way [21], [36],
                                                          
                                                    4   n          and private combinatorial optimization [26]. We refer readers
                                                      r
  Pr [v ← chooseǫ,n (g) : v = v ′ ] ∝ dE,V (v ′ ) +                interested in a more comprehensive treatment to the excellent
                                                    ǫ |E|
                                                                   surveys by Dwork [19], [20].
where g = (E, V ) and n is a given parameter, one obtains                Verifying differential privacy: Several tools have been
an (ǫ, 0)-differentially private algorithm with respect to the     proposed for providing formal verification of the differen-
adjacency relation as defined above.                               tial privacy guarantee; we can roughly classify them by
   In [11], Barthe et al prove differential privacy of vertex      the verification approach they use. PINQ [30] provides an
cover in apRHL. The proof uses the generalized rule for            encapsulation for LINQ —an SQL-like language embedded
loops, a code motion rule that allows to swap independent          in C#—tracking at runtime the privacy budget consumption,
statements, and a rule for dealing with statements of the form     and aborting the computation when the budget is exhausted.
x←  $ µ; assert (φ). It also relies on apRHL specifications of
                                                                   Airavat [34] combines a similar runtime monitor with access
choose, that are proven correct in the Coq proof assistant         control in a MapReduce framework. While PINQ is restricted
from the definition of choose.                                     to ǫ-differential privacy, Airavat can handle also approximate
   We now consider the formal verification of the vertex cover     differential privacy using a runtime monitor for δ.
algorithm using self-products. We first extend the definition of      Another approach is based on linear type systems.
self-product to choose. Then, there are two cases to consider:     Fuzz [33] and DFuzz [25] use a type-based approach for
g2 = g1 ∪ {hu, ti} and g1 = g2 ∪ {hu, ti}. In the first case,      inferring and checking the sensitivity of functional programs.
we can use the first Hoare specification from Fig. 14. In the      This sensitivity analysis combined with the use of trusted prob-
second case, we use the second and third specifications from       abilistic primitives provides the differential privacy guarantee.
Fig. 14. Using these specifications, it is possible to verify      Interestingly, this type-based approach can be combined with
that the self-product of the vertex cover algorithm satisfies      type systems for cryptographic protocols to verify differential
the Hoare specification of Theorem 5. However, we have not         privacy for distributed protocols [24]. All these systems pro-
yet been able to extend the proof of Theorem 5 to deal with        vide automatic verification of differential privacy. However,
the choose self-product.                                           they fail to verify all the examples that we can handle, like
                                                                   advanced sum statistics [14] and the Propose-Test-Release
E. Formal verification of the examples                             framework [21]. Moreover, so far they can address only pure
   The examples above (with the exception of vertex cover)         differential privacy, where δ = 0.
have been formally verified. For each example, we have built          Tschantz, et al. [37] consider a verification framework for
the corresponding self-product program, and verified this result   interactive private programs, where the algorithm can receive
using the non-probabilistic and non-relational Hoare logic         new input and produce multiple outputs over a series of steps.
rules available in the EasyCrypt [6] framework. As described       They follow an approach similar to ours by verifying the
above, we have used non-probabilistic axiomatic specifications     correct use of differentially private primitives. However, their
for the primitives. Apart from the axiomatic specification, and    programs are well-modeled by probabilistic I/O-automata,
the code for the program and the self-product construction, the    and they provide a proof technique based on probabilistic
longest Hoare logic verification proof (for MWEM) consists         bisimulation. Also, their method is currently limited to pure
of about 50 lines of code. This demonstrates the simplicity        differential privacy.
                                                                                                         √ p 
           ⊢ (v1 , v2 ) ← choose⋄ǫ,n (g1 , g2 ) : g1 ∪ {hu, ti} = g2 ∧ vǫ = ǫ0 =⇒ v1 = v2 ∧ vǫ = ǫ0 + ǫ/ 2 n |g1 |

                 ⊢ (v1 , v2 ) ← choose⋄ǫ,n (g1 , g2 ) : g1 = g2 ∪ {hu, ti} ∧ vǫ = ǫ0 =⇒ (v 6= t ∧ v 6= u) ∧ vǫ = ǫ0
              ⊢ (v1 , v2 ) ← choose⋄ǫ,n (g1 , g2 ) : g1 = g2 ∪ {hu, ti} ∧ vǫ = ǫ0 =⇒ (v = t ∨ v = u) ∧ vǫ = ǫ0 + ǫ/4

                                             Fig. 14: Hoare specifications for choose⋄


   Finally, CertiPriv [11] and EasyCrypt [6] use custom                                       VII. C ONCLUSION
relational logics to verify differential privacy. These systems         We have proposed a program transformation that reduces
are very expressive: they supports general (ǫ, δ)-differential       proving (ǫ, δ)-differential privacy of a probabilistic program
privacy, they can verify privacy for mechanisms like the             to proving a safety property of a deterministic transformed
Laplace and the Exponential mechanism, and they can capture          program. The method applies to all standard examples where
advanced examples that go beyond mechanisms and compo-               privacy is achieved through mechanisms and composition
sition, like the private vertex cover algorithm of Gupta et          theorems; on the other hand, differentially private algorithms
al. [26]. The difficulty with their approach is that it relies       based on ad hoc output perturbation, such as the differentially
on a customized and complex logic. Moreover, ad hoc rules            private vertex cover algorithm [26], are more difficult to
for loops are required for many advanced examples.                   handle. In particular, they fall outside the scope of Theorem 5
      Verifying 2-safety properties: Beyond differential privacy,    which proves the soundness of our approach. Our method is
there is a large body of literature on verifying 2-safety prop-      particularly suited for reasoning about differential privacy, be-
erties. Our work is most closely related to deductive methods        cause the transformed program can be analyzed with standard
based on program logics; more precisely, approaches that             verification tools. Our method can also be extended to reason
reduce 2-safety of a program c to safety of a program c′ built       about probabilistic non-interference, at the cost of targeting an
from c. Such approaches include self-composition [7], prod-          assertion language that supports existential quantification over
uct programs [38], and type-directed product programs [35].          functions. Directions for further work include extending the
These approaches are subsumed by work by Barthe et al. [4],          scope of Theorem 5 to deal with more complex examples, like
[5].                                                                 vertex cover. On a more practical side, it would be interesting
                                                                     to implement our transformation for a realistic setting, for
   Another alternative is to reason directly on two programs         instance modeling the PINQ language [30].
(or two executions of the same program) using relational
program logics such as Benton’s relational Hoare logic [12],         Acknowledgments
or specialized relational logics, e.g., for information flow [2].      We thank the anonymous reviewers for their close read-
CertiCrypt [9], and EasyCrypt [8], [6], are computer-aided           ing and suggestions. This research is partially supported
tools that support relational reasoning about probabilistic          by European project FP7-291803 AMAROUT II, Spanish
programs and have been used to prove security of crypto-             projects TIN2009-14599 DESAFIOS 10, TIN2012-39391-
graphic constructions and computational differential privacy of      C04-01 Strongsoft, and Madrid regional project S2009TIC-
protocols. For such applications, reasoning about structurally       1465 PROMETIDOS. Marco Gaboardi has been supported by
different programs is essential.                                     the European Community’s Seventh Framework Programme
   Chaudhuri et al. [15] develop an automated method for             FP7/2007-2013 under grant agreement No. 272487. Justin Hsu
analyzing the continuity and the robustness of programs.             has been supported by NSF grant CNS-1054229.
Robustness is a 2-safety property that is very similar to                                         R EFERENCES
sensitivity as used in differential privacy. An interesting aspect
                                                                      [1] Proving differential privacy in hoare logic; supplementary
of their work is that their analysis is able to reason about two          code     for   the    examples    verified    in    EasyCrypt,  2014.
unsynchronized pairs of executions; that is, pairs of executions          http://www.easycrypt.info/selfproduct/selfproduct.tar.gz.
that may have different control flow.                                 [2] Torben Amtoft and Anindya Banerjee. Information flow analysis in
                                                                          logical form. In 11th International Symposium on Static Analysis, SAS
                                                                          2004, volume 3148 of Lecture Notes in Computer Science, pages 100–
      Verification of hyperproperties: Developing general veri-           115, Heidelberg, 2004. Springer.
fication methods for hyperproperties remains a challenge; how-        [3] Sanjeev Arora, Elad Hazan, and Satyen Kale. The multiplicative
ever, there have been some recent proposals in this direction             weights update method: a meta-algorithm and applications. Theory of
                                                                          Computing, 8(6):121–164, 2012.
(e.g., [16], [32]).                                                   [4] Gilles Barthe, Juan Manuel Crespo, and César Kunz. Relational verifi-
                                                                          cation using product programs. In Michael Butler and Wolfram Schulte,
     Other work: There is an extensive body of work on                    editors, FM, volume 6664 of Lecture Notes in Computer Science, pages
deductive verification of non-probabilistic and probabilistic             200–214. Springer, 2011.
programs, as well as many works that consider product con-            [5] Gilles Barthe, Juan Manuel Crespo, and César Kunz. Beyond 2-safety:
                                                                          Asymmetric product programs for relational program verification. In
structions of Labeled Transition Systems; summarizing this                Sergei N. Artëmov and Anil Nerode, editors, LFCS, volume 7734 of
large literature is beyond the scope of this paper.                       Lecture Notes in Computer Science, pages 29–43. Springer, 2013.
 [6] Gilles Barthe, George Danezis, Benjamin Grégoire, César Kunz, and                Symposium on Discrete Algorithms (SODA), Austin, Texas, pages 1106–
     Santiago Zanella Béguelin. Verified computational differential privacy            1125, 2010.
     with applications to smart metering. In CSF, pages 287–301. IEEE,             [27] Anupam Gupta, Aaron Roth, and Jonathan Ullman. Iterative con-
     2013.                                                                              structions and private data release. In IACR Theory of Cryptography
 [7] Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. Secure informa-                Conference (TCC), Taormina, Italy, pages 339–356, 2012.
     tion flow by self-composition. In Jonathan Herzog, editor, CSFW, pages        [28] Moritz Hardt, Katrina Ligett, and Frank McSherry. A simple and
     100–114. IEEE Computer Society, 2004.                                              practical algorithm for differentially private data release. In Peter L.
 [8] Gilles Barthe, Benjamin Grégoire, Sylvain Heraud, and Santiago Zanella            Bartlett, Fernando C. N. Pereira, Christopher J. C. Burges, Léon Bottou,
     Béguelin. Computer-aided security proofs for the working cryptogra-               and Kilian Q. Weinberger, editors, NIPS, pages 2348–2356, 2012.
     pher. In Phillip Rogaway, editor, CRYPTO, volume 6841 of Lecture              [29] Moritz Hardt and Guy N. Rothblum. A multiplicative weights mecha-
     Notes in Computer Science, pages 71–90. Springer, 2011.                            nism for privacy-preserving data analysis. In FOCS, pages 61–70. IEEE
 [9] Gilles Barthe, Benjamin Grégoire, and Santiago Zanella-Béguelin. For-            Computer Society, 2010.
     mal certification of code-based cryptographic proofs. In 36th ACM             [30] Frank McSherry. Privacy integrated queries: an extensible platform for
     SIGPLAN-SIGACT Symposium on Principles of Programming Lan-                         privacy-preserving data analysis. In Proc. SIGMOD, 2009.
     guages, POPL 2009, pages 90–101, New York, 2009. ACM.                         [31] Frank McSherry and Kunal Talwar. Mechanism design via differential
[10] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella                  privacy. In FOCS, pages 94–103. IEEE Computer Society, 2007.
     Béguelin. Probabilistic relational reasoning for differential privacy. In    [32] Dimiter Milushev and Dave Clarke. Incremental hyperproperty model
     John Field and Michael Hicks, editors, POPL, pages 97–110. ACM,                    checking via games. In Hanne Riis Nielson and Dieter Gollmann,
     2012.                                                                              editors, NordSec, volume 8208 of Lecture Notes in Computer Science,
[11] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella                  pages 247–262. Springer, 2013.
     Béguelin. Probabilistic relational reasoning for differential privacy. ACM   [33] Jason Reed and Benjamin C. Pierce. Distance makes the types grow
     Trans. Program. Lang. Syst., 35(3):9, 2013.                                        stronger: a calculus for differential privacy. In Paul Hudak and Stephanie
[12] Nick Benton. Simple relational correctness proofs for static analyses and          Weirich, editors, ICFP, pages 157–168. ACM, 2010.
     program transformations. In 31st ACM SIGPLAN-SIGACT Symposium                 [34] Indrajit Roy, Srinath Setty, Ann Kilzer, Vitaly Shmatikov, and Emmett
     on Principles of Programming Languages, POPL 2004, pages 14–25,                    Witchel. Airavat: Security and privacy for MapReduce. In USENIX
     New York, 2004. ACM.                                                               Symposium on Networked Systems Design and Implementation (NDSI),
[13] Avrim Blum, Cynthia Dwork, Frank McSherry, and Kobbi Nissim.                       San Jose, California, 2010.
     Practical privacy: the SuLQ framework. In ACM SIGACT–SIGMOD–                  [35] Tachio Terauchi and Alex Aiken. Secure information flow as a safety
     SIGART Symposium on Principles of Database Systems (PODS), Balti-                  problem. In 12th International Symposium on Static Analysis, SAS 2005,
     more, Maryland, pages 128–138, 2005.                                               volume 3672 of Lecture Notes in Computer Science, pages 352–367,
[14] T.-H. Hubert Chan, Elaine Shi, and Dawn Song. Private and continual                Heidelberg, 2005. Springer.
     release of statistics. ACM Transactions on Information and System             [36] Abhradeep Thakurta and Adam Smith. Differentially private feature
     Security, 14(3):26, 2011.                                                          selection via stability arguments, and the robustness of the lasso. In
[15] Swarat Chaudhuri, Sumit Gulwani, and Roberto Lublinerman. Continu-                 Shai Shalev-Shwartz and Ingo Steinwart, editors, COLT, volume 30 of
     ity analysis of programs. In Manuel V. Hermenegildo and Jens Palsberg,             JMLR Proceedings, pages 819–850. JMLR.org, 2013.
     editors, POPL, pages 57–70. ACM, 2010.                                        [37] Michael Carl Tschantz, Dilsun Kaynar, and Anupam Datta. Formal
[16] Michael R. Clarkson, Bernd Finkbeiner, Masoud Koleini, Kristopher K.               verification of differential privacy for interactive systems (extended
     Micinski, Markus N. Rabe, and César Sánchez. Temporal logics for                 abstract). Electronic Notes in Theoretical Computer Science, 276(0):61 –
     hyperproperties. In Martı́n Abadi and Steve Kremer, editors, POST,                 79, 2011. Twenty-seventh Conference on the Mathematical Foundations
     volume 8414 of Lecture Notes in Computer Science, pages 265–284.                   of Programming Semantics (MFPS XXVII).
     Springer, 2014.                                                               [38] Anna Zaks and Amir Pnueli. Covac: Compiler validation by program
[17] Michael R. Clarkson and Fred B. Schneider. Hyperproperties. In 21st                analysis of the cross-product. In 15th International Symposium on
     IEEE Computer Security Foundations Symposium, CSF 2008, pages 51–                  Formal Methods, FM 2008, volume 5014 of Lecture Notes in Computer
     65, Los Alamitos, 2008. IEEE Computer Society.                                     Science, pages 35–51, Heidelberg, 2008. Springer.
[18] Ádám Darvas, Reiner Hähnle, and David Sands. A theorem proving
     approach to analysis of secure information flow. In Dieter Hutter
     and Markus Ullmann, editors, SPC, volume 3450 of Lecture Notes in
     Computer Science, pages 193–209. Springer, 2005.
[19] Cynthia Dwork. Differential privacy. In Michele Bugliesi, Bart Preneel,
     Vladimiro Sassone, and Ingo Wegener, editors, ICALP (2), volume 4052
     of Lecture Notes in Computer Science, pages 1–12. Springer, 2006.
[20] Cynthia Dwork. Differential privacy: A survey of results. In Manindra
     Agrawal, Dingzhu Du, Zhenhua Duan, and Angsheng Li, editors, Theory
     and Applications of Models of Computation, volume 4978 of Lecture
     Notes in Computer Science, pages 1–19. Springer Berlin Heidelberg,
     2008.
[21] Cynthia Dwork and Jing Lei. Differential privacy and robust statistics.
     In Michael Mitzenmacher, editor, STOC, pages 371–380. ACM, 2009.
[22] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith.
     Calibrating noise to sensitivity in private data analysis. In IACR Theory
     of Cryptography Conference (TCC), New York, New York, pages 265–
     284, 2006.
[23] Cynthia Dwork, Moni Naor, Toniann Pitassi, and Guy N. Rothblum.
     Differential privacy under continual observation. In ACM SIGACT Sym-
     posium on Theory of Computing (STOC), Cambridge, Massachusetts,
     pages 715–724, 2010.
[24] Fabienne Eigner and Matteo Maffei. Differential privacy by typing in
     security protocols. In CSF, pages 272–286. IEEE, 2013.
[25] Marco Gaboardi, Andreas Haeberlen, Justin Hsu, Arjun Narayan, and
     Benjamin C. Pierce. Linear dependent types for differential privacy. In
     Roberto Giacobazzi and Radhia Cousot, editors, POPL, pages 357–370.
     ACM, 2013.
[26] Anupam Gupta, Katrina Ligett, Frank McSherry, Aaron Roth, and Kunal
     Talwar. Differentially private combinatorial optimization. In ACM–SIAM
                                                           A PPENDIX A
                                                        AUXILIARY LEMMAS
   The following is an auxiliary result used in the proof of correctness of the method based on self-products.
   Lemma 4: Suppose that for all memories m1 , m2 such that m1 Ψ m2 we have that c is terminating in m1 and m2 , and
(JcK m1 ) Φhǫ,δi (JcK m2 ). Then, for every memory distributions µ1 , µ2 such that µ1 Ψhǫ′ ,δ′ i µ2 we have
                                                   (JcK⋆ µ1 ) Φhǫ+ǫ′ ,δ+δ′ i (JcK⋆ µ2 )
     The following is another auxiliary result used in the proof of correctness.
     Lemma 5: For all memories m1 , m2 such that m1 Ψ m2 we have that 1m1 Ψh0,0i 1m2 .
       Proof: We can take as witness µ̂ = 1m1 ,m2 .
     Lemma 6: Suppose that for m1 , m2 such that m1 Ψ m2 we have that (µ1 m1 ) Φhǫ,δi (µ2 m2 ). Then,
                                          ((λv.1m1 {v/x} )⋆ µ1 ) Φhǫ,δi ((λv.1m2 {v/x} )⋆ µ2 )
       Proof: By Lemma 5 and Lemma 4.
     The proof of the next two auxiliary lemmas are presented in the work in apRHL [11].
     Lemma 7: Given a relation S that is preserved by c, i.e. such that:
                   ∀m1 , m2 . (m1 , m2 ) ∈ S ⇒ (∀m′1 , m′2 .(JcK m1 m′1 6= 0 ∧ JcK m2 m′2 6= 0 ⇒ (m′1 , m′2 ) ∈ S))
If
                                        ∀m1 , m2 . (m1 , m2 ) ∈ R ⇒ (JcK m1 ) Qhǫ,δi (JcK m2 )
then
                                 ∀m1 , m2 . (m1 , m2 ) ∈ (R ∩ S) ⇒ (JcK m1 ) (Q ∩ S)hǫ,δi (JcK m2 )
     Lemma 8: For all distribution expressions µ1 , µ2 , if
                                                     ∆ǫ (Jµ1 K m1 , Jµ2 K m2 ) ≤ δ
then
                                                    $ µ Km )Q
                                                (Jx ←  1  1  hǫ,δi (Jx ← µ2 K m2 )
                                                                       $



where Q = {(m1 , m2 ) | m1 x = m2 x}.
                                                          A PPENDIX B
                                                  P ROOF OF THE MAIN THEOREM
     Theorem 5 is a corollary of the following lemma:
     Lemma 9:
                                      ⊢ ⌈c⌉ : Ψ ∧ vǫ = 0 ∧ vδ = 0 =⇒ Φ ∧ vǫ ≤ ǫ ∧ vδ ≤ δ
implies
                                           ∀m1 , m2 . m1 Ψ m2 ⇒ (JcK m1 ) Φhǫ,δi (JcK m2 )
    Proof: We first introduce some new notation. For any disjoint memories m1 , m2 and real values ǫ, δ, m1 ⊕ǫ,δ m2 denotes the
memory m such that m x = m1 x for every x ∈ dom(m1 ), m x = m2 x for every x ∈ dom(m2 ), and m vǫ = ǫ and m vδ = δ.
Given a memory relation R ⊆ M × M, we let R̂hǫ,δi stand for the set {m1 ⊕ǫ′ ,δ′ m2 | (m1 , m2 ) ∈ R ∧ ǫ′ ≤ ǫ ∧ δ ′ ≤ δ}. The
proof follows by structural induction on c, proving the following lemma: let R, Q ⊆ M × M be relations on memories, then
                                                                                            
                                    ∀m. m ∈ R̂ǫ,δ ⇒ ∀m′ . m′ ∈ (J⌈c⌉K m) ⇒ m′ ∈ Q̂ǫ′ ,δ′
                                  =⇒
                                  ∀m1 , m2 . (m1 , m2 ) ∈ R ⇒ (JcK m1 ) Qhǫ′ −ǫ,δ′ −δi (JcK m2 )
Indeed, by setting ǫ = 0 and ǫ′ = ǫ, we get the statement of Lemma 9.
                                                                                                     ′   ′′            ′ ′′
  • Sequential composition: Let (m1 , m2 ) ∈ R. By definition, m1 ⊕ǫ,δ m2 ∈ R̂ǫ,δ . Since m vǫ = m vǫ for all m , m ∈
    J⌈c1 ⌉K (m1 ⊕ǫ,δ m2 ), then there are ǫ0 , δ0 and S ⊆ M × M such that Ŝǫ0 .δ0 = J⌈c1 ⌉K m1 ⊕ǫ,δ m2 . Also, from the
    hypotheses, for all m ∈ Ŝǫ,δ we have that ∀m′ ∈ (J⌈c2 ⌉K m). m′ ∈ Q̂ǫ′ ,δ′ . By inductive hypothesis we have thus
      1) (Jc1 K m1 ) Shǫ0 −ǫ,δ0 −δi (Jc1 K m2 )
      2) for all m′ , m′′ such that (m′ , m′′ ) ∈ S, we have (Jc2 K m′ )Qǫ′ −ǫ0 ,δ′ −δ0 (Jc2 K m′′ )
  It follows from Lemma 4 that (Jc2 K⋆ (Jc1 K m1 )) Qhǫ−ǫ,δ′ −δi (Jc2 K⋆ (Jc1 K m2 )).
• While loop: We start by proving the following auxiliary result:

                            (∀m. m ∈ R̂ǫ,δ ⇒ (b1 = b2 ) m ∧ ŵi m 6= ⊥ ∧ ∀m′ ∈ (ŵi m). m′ ∈ Q̂ǫ′ ,δ′ )
                            =⇒
                            ∀m1 m2 . (m1 , m2 ) ∈ R ⇒ (wi m1 ) Qhǫ′ −ǫ,δ′ −δi (wi m2 )
    The proof follows by natural induction on i. The case i = 0 is trivial. For the inductive step, let m1 , m2 ∈ R. Since
    m1 ⊕ǫ,δ m2 ∈ R̂ǫ,δ , by hypothesis we have m1 b1 ⇔ m2 b2 . We proceed by case analysis on m1 b1 .
     – In the case ¬m1 b1 , by definition of ŵi+1 , ŵi+1 m1 ⊕ǫ,δ m2 = m1 ⊕ǫ,δ m2 , and thus by hypothesis m1 ⊕ǫ,δ m2 ∈ Q̂ǫ′ ,δ′ ,
        which implies ǫ = ǫ′ and δ = δ ′ . By Lemma 5, 1m1 Qh0,0i 1m2 , which concludes the proof case since we have as
        well wi+1 m1 = 1m1 and wi+1 m2 = 1m2 .
     – If m1 b1 holds, then                                           [
                                                 ŵi+1 m =                       wi m′
                                                                m′ ∈J⌈c⌉; assert (b1 ⇔b2 )K

        Since b1 ⇔ b2 is deterministic in J⌈c⌉K m and ŵi+1 m 6= ∅ by hypothesis, then
                                                                  [
                                                     ŵi+1 m =         wi m′
                                                                        m′ ∈J⌈c⌉K

        By the same reasoning as with sequential composition, there is then S, ǫ0 , and δ0 such that Ŝǫ,δ = J⌈c⌉K m1 ⊕ǫ,δ m2 .
        Then, by the structural inductive hypothesis we have (JcK m1 ) Shǫ0 −ǫ,δ0 −δi (JcK m2 ), and by the natural induction
        hypothesis
                                    ∀m1 m2 . (m1 , m2 ) ∈ S ⇒ (wi m1 ) Qhǫ′ −ǫ0 ,δ′ −δ0 i (wi m2 )
        We can conclude from Lemma 4 that
                                                  (wi+1 m1 ) Qhǫ′ −ǫ,δ′ −δi (wi+1 m2 )
                                                                                    F           F
    It remains to show that the property holds as well when considering the lubs        ŵi and   wi :
                                (∀m. m ∈ R̂ǫ,δ ⇒ (b1 = b2 ) m ∧ ∀m′ ∈ ( ŵi m). m′ ∈ Q̂ǫ′ ,δ′ )
                                                                             F
                                =⇒                           F                         F
                                ∀m1 m2 . (m1 , m2 ) ∈ R ⇒ ( wi m1 ) Qhǫ′ −ǫ,δ′ −δi ( wi m2 )

    Let m1 and m2 such that (m1 , m2 ) ∈ R. Since m1 ⊕ǫ,δ m2 then ∀m′ ∈ ( ŵi m). m′ ∈ Q̂ǫ′ ,δ′ . Since we are considering
                                                                                F
    terminating program loops, there exists k such that for all j ≥ k:
                                                          ŵj (m1 ⊕ ǫ, δm2 ) 6= ∅
    and furthermore                                                    G
                                              ŵj (m1 ⊕ ǫ, δm2 ) =         ŵi (m1 ⊕ ǫ, δm2 )

    From the auxiliary lemma above we have thus
                                                       (wj m1 ) Qhǫ−ǫ′ ,δ−δ′ i (wj m2 )
                                                                                                                         F
    for all j ≥ k. F
                   Since the loop termination condition is deterministic by assumption then it also holds that wj m1 =     i wi m1
    and wj m2 = i wi m2 for all j ≥ k. Then we can conclude:
                                                  G                        G
                                                 ( wi m1 ) Qhǫ−ǫ′ ,δ−δ′ i ( wi m2 )
                                                   i                              i

•   Laplace mechanism: We consider the case x ← Lapǫ (e). Let m1 and m2 such that (m1 , m2 ) ∈ R. Then m1 ⊕ǫ0 ,δ0 m2 ∈
                                                    $

    R̂ǫ0 ,δ0 . From the hypothesis J⌈c⌉K m ⊆ Q̂ǫ′ ,δ′ and the semantics of the target language, we get
                                     [
                                         (m1 {v/x}) ⊕ǫ0 +|JeK m1 −JeK m2 |ǫ,δ0 (m2 {v/x}) ⊆ Q̂ǫ′ ,δ′
                                   v∈R

    From this, we can conclude δ ′ = δ0 , ǫ′ = ǫ0 + |JeK m1 − JeK m2 |ǫ and
                      Q ⊇ {(m1 , m2 ) | ∃v1 , v2 . (m1 {v1 /x} , m2 {v2 /x}) ∈ R} ∩ {(m1 , m2 ) | m1 x = m2 x}
    Since the first term in the intersection above is preserved by any assignment to the x variable, by Lemma 7 it is enough
    to consider the case Q = {(m1 , m2 ) | m1 x = m2 x}, and prove (JcK m1 ) Qh|JeK m1 −JeK m2 |ǫ,0i (JcK m2 ). To verify this, by
    Lemma 8, it is sufficient to show that
                                              ∆|JeK m1 −JeK m2 |ǫ (Lapǫ (JeK m1 ), Lapǫ (JeK m2 )) ≤ 0
    We need to show that for every r we have
                                       Lapǫ (JeK m1 ) r − exp(|JeK m1 − JeK m2 |ǫ)Lapǫ (JeK m2 ) r ≤ 0
    Then, it is enough to prove:
                                                                                                        
                        exp − ǫ|r−JeK  2
                                          m1 |
                                                                                      exp   −  ǫ|r−JeK m2 |
                                                                                                      2
                   P                               − exp(|JeK m1 − JeK m2 |ǫ)  P                             ≤ 0
                                   ǫ|r ′ −JeK m1 |                                                ǫ|r ′ −JeK m2 |
                        r′ exp   −        2                                           r′ exp  −          2

    This is equivalent to prove
                                              P              ′
                                                                           
                           exp − ǫ|r−JeK
                                      2
                                         m1 |
                                               · r′ ∈R exp − ǫ|r −JeK
                                                                  2
                                                                      m2 |

                                              P              ′
                                                                            ≤ exp(|JeK m1 − JeK m2 |ǫ)
                           exp − ǫ|r−JeK
                                      2
                                         m2 |
                                               · r′ ∈R exp − ǫ|r −JeK
                                                                  2
                                                                      m1 |


    The first term can be bound by
                                                                                                            
                                                                             P ′ exp − ǫ|r′ −JeK m2 |
                                              ǫ|JeK m2 − JeK m1 |               r ∈R                2
                                          exp                                 ·P                            
                                                       2                                     ǫ|r ′ −JeK m1 |
                                                                                r ′ ∈R exp −        2

    For every r′ ∈ R, we know |r′ − JeK m2 | ≥ |r′ − JeK m1 | − |JeK m2 − JeK m1 |. So, the above can be bound by
                                                                                                  
                                                    P ′ exp − ǫ(|r′−JeK m1 |−|JeK m2 −JeK m1 |)
                                ǫ|JeK m2 − JeK m1 |       r ∈R                        2
                          exp                         ·                                       
                                         2                      P
                                                                    ′   exp −  ǫ|r ′ −JeK m1 |
                                                                                        r ∈R                2

    that is equivalent to
                                                                                                                           
                                                                                       P ′ exp − ǫ|r′ −JeK m1 |
                                  ǫ|JeK m2 − JeK m1 |                ǫ|JeK m2 − JeK m1 |     r   ∈R                2
                        exp                                    · exp                      ·P                               
                                           2                                  2                ′    exp   − ǫ|r ′ −JeK m1 |
                                                                                             r ∈R                  2

    and simplifying                                                                                          
                                               ǫ|JeK m2 − JeK m1 |                      ǫ|JeK m2 − JeK m1 |
                                           exp                                    · exp
                                                        2                                        2
    that is what we need.
•   Exponential mechanism: Following a similar reasoning to the Laplace mechanism case, we need to prove that for every
    r we have
                             Expǫ (JsK m1 , JeK m1 ) r − exp(ǫ1 − ǫ0 )Expǫ (JsK m2 , JeK m2 ) r ≤ 0
    where Expǫ (s, x) stands for the distribution
                                                                                              
                                                                                     ǫs(x,r)
                                                                           exp          2
                                                                  λr. P                                
                                                                                           ǫs(x,r ′ )
                                                                          r ′ ∈R exp          2

    By Lemma 6 and the fact that JsKm1 = JsKm2 = ŝ it is then enough to prove:
                                                                                                  
                                exp ǫŝ(JeKm
                                          2
                                              1 ,r)
                                                                                 exp ǫŝ(JeKm
                                                                                           2
                                                                                               2 ,r)

                                                          − exp(ǫ1 − ǫ0 ) P                             ) ≤ 0
                         P               ǫŝ(JeKm1 ,r ′ )                                 ǫŝ(JeKm2 ,r ′ )
                            r ′ ∈R exp           2                           r ′ ∈R exp           2

    This is equivalent to prove
                                                           P                         ′
                                                                                            
                                                  ǫŝ(JeKm1 ,r)
                                        exp             2   · r′ ∈R exp ǫŝ(JeKm  2
                                                                                    2 ,r )

                                                           P                              ≤ exp(ǫ1 − ǫ0 )
                                                                           ǫŝ(JeKm1 ,r ′ )
                                        exp ǫŝ(JeKm
                                                  2
                                                     2 ,r)
                                                            · r ′ ∈R exp          2
     Continuing we have
                                                                                                 
                                                                  P ′ exp ǫŝ(JeKm2 ,r′ )
                                 ǫ(ŝ(JeKm1 , r) − ŝ(JeKm2 , r))     r ∈R              2
                             exp                                   ·P                             ≤ exp(ǫ1 − ǫ0 )
                                                 2                     ′   exp   ǫŝ(JeKm1 ,r ′ )
                                                                      r ∈R              2

     Using the fact that maxr∈R |ŝ(e1 , r) − ŝ(e2 , r)|ǫ ≤ ǫ1 − ǫ0 we have:
                                                                                      
                                                    P ′ exp ǫŝ(JeKm2 ,r′ )
                                           ǫ1 − ǫ0          r ∈R              2
                                    exp                ·P                              ≤ exp(ǫ1 − ǫ0 )
                                              2              ′   exp   ǫŝ(JeKm     ′
                                                                                1 ,r )
                                                                       r ∈R                  2

     Using the same fact we also know that for every r′ ∈ R we have ŝ(e2 , r) ≤ ǫ1 −ǫ      ǫ
                                                                                              0
                                                                                                + ŝ(e1 , r). So,we have:
                                                                                      ′
                                                                                         
                                                 P             (ǫ1 −ǫ0 )+ǫŝ(JeKm1 ,r )
                                                  r ′ ∈R exp
                                            
                                     ǫ1 − ǫ0                               2
                               exp             ·                                         ≤ exp(ǫ1 − ǫ0 )
                                        2            P
                                                         ′   exp    ǫŝ(JeKm1 ,r ′ )
                                                                       r ∈R                  2

     that is equivalent to
                                                                                                   
                                                                   P ′ exp ǫŝ(JeKm1 ,r′ )
                                         ǫ1 − ǫ0             ǫ1 − ǫ0    r ∈R              2
                               exp                     · exp          ·P                            ≤ exp(ǫ1 − ǫ0 )
                                            2                   2        ′   exp   ǫŝ(JeKm1 ,r ′ )
                                                                        r ∈R              2

     and simplifying                                                                          
                                                             ǫ1 − ǫ0                   ǫ1 − ǫ0
                                                   exp                     · exp                     ≤ exp(ǫ1 − ǫ0 )
                                                                2                         2

  Lemma 10 (Proof of the accuracy specification):
                         ∀m1 , m2 . JeK m1 = JeK m2 ⇒ (Jx ← Lapǫ (e)K m1 ) Qh0,δi (Jx ← Lapǫ (e)K m2 )
where
                                  .
                                Q = {(m1 , m2 ) | m1 x = m2 x ∧ |m1 x − JeK m1 | ≤ log(2/δ)/(2ǫ)}
    Proof: We need to prove:
                                                  $ Lap (e)K m ) Q
                                              (Jx ←    ǫ      1   h0,δi (Jx ← Lapǫ (e)K m2 )
                                                                            $



By the assumption e1 = e2 we have that Jx ←   $ Lap (e)K m
                                                       ǫ      1 and Jx ← Lapǫ (e)K m2 are the same distribution µ̂. Now, consider
                                                                        $

the set S = {z : R | |z − Je1 K m1 | < log(2/δ)/(2ǫ)} and the distribution µ ∈ D(R × R), parametrized on S defined as:
                                                          
                                                            µ̂ z1 if z1 = z2 ∧ z1 ∈ S
                                           µ(z1 , z2 ) :=
                                                            0      otherwise.
Notice that by definition of µ̂ we have π1 µ ≤ Jx ←
                                                  $ Lap (e)Km
                                                       ǫ      1 and π2 µ ≤ Jx ← Lapǫ (e)Km2 . Moreover, by definition of S
                                                                                $

we also have that for every m, µ m 6= 0 ⇒ Φ m. Since clearly π1 µ = π2 µ, the only thing left to prove is that ∆0 (µ̂, π1 µ) ≤ δ.
This means that we need to prove
                                                  max{µ̂ R − π1 µ R} ≤ δ
                                                                 R⊆R

It is easy to see that on values in R ∩ S the two distribution coincide. So we can instead consider
                                                                 max {µ̂ R − π1 µ R} ≤ δ
                                                              R⊆(R/S)

Now, notice that for every R ⊆ (R/S) we have π1 µ = 0, so we can just consider
                                                                       max {µ̂ R} ≤ δ
                                                                   R⊆(R/S)
                               P
and since by definition µ̂ R = a∈R µ̂ a where every value is non-negative, we can just consider µ̂ (R/S) ≤ δ. Now, recall
that S corresponds to the interval:
                                            [−(log(2/δ)/(2ǫ)) + JeK m1 , JeK m1 + (log(1/δ)/ǫ)]
                 $ Lap (e)K m . So, we can apply a tail bound on the Laplace distribution:
and that µ̂ = Jx ←    ǫ      1

                                    {µ̂ z | z ∈ (R/S)} = {µ̂ z | |z − JeK m1 | ≥ log(2/δ)/(2ǫ)} < δ.
and conclude
                                                                      µ̂ (R/S) ≤ δ
that is what we need.
   Lemma 11 (Tail bound for the discrete version of Laplace): Let x be drawn from the discrete version of the Laplace
distribution with mean 0 and parameter b > 0, i.e., with probability
                                                                       
                                                              exp − |x|
                                                                     2b
                                                Lb (x) = P                  .
                                                                         |z|
                                                             z∈Z exp  −  2b

Then, for T ∈ N and T > 0:                                                              
                                                                                      T
                                                     Pr [x : |Lb (x)| > T ] ≤ 2 exp −      .
                                                                                      2b
In particular, if b = 1/ǫ (like in Lap ǫ (x)) and T = log(2/δ)/(2ǫ), we have Lemma 1.
     Proof: We have
                                                                               
                                                     exp − |x| 2b
              Pr [x : |Lb (x)| > T ] = Pr x : P                       > T
                                                                   |z|
                                                    z∈Z exp − 2b
                                                                                                                         
                                                    exp − |x| 2b                                       exp   − |x|
                                                                                                               2b
                                     = Pr x : P                      > T  + Pr x : P                               < −T 
                                                                  |z|                                               |z|
                                                   z∈Z  exp    −  2b                                  z∈Z exp   −   2b
                                                                                             
                                                        |x|                                 |x|
                                       X∞       exp − 2b                −∞
                                                                        X         exp − 2b
                                     =                            +                               
                                            P                |z|              P                  |z|
                                       x=T     z∈Z exp − 2b             −T       z∈Z exp − 2b
                                       P∞              x
                                                           P−∞                  x
                                                                                   
                                          x=T exp − 2b +            −T exp 2b
                                     =                                
                                                 P                 |z|
                                                    z∈Z exp − 2b
                                       P∞             x+T
                                                             P∞
                                                               + x=0 exp −x−T
                                                                                           
                                          x=0 exp − 2b                               2b
                                     =                                    
                                                    P                  |z|
                                                       z∈Z exp − 2b
                                               T
                                                  P∞                  x
                                                                                        T
                                                                                                     P∞                 x
                                                                                                                           
                                       exp − 2b       x=0 exp − 2b + exp − 2b                   1 + x=1 exp − 2b
                                     =                                                     
                                                                     P                  |z|
                                                                         z∈Z exp − 2b
                                                   P∞                    x
                                                                                       P∞                 x
                                                                                                             
                                                         x=0 exp − 2b + 1 +                 x=1 exp − 2b
                                           
                                               T
                                     = exp −                                                 
                                               2b                      P                  |z|
                                                                           z∈Z exp − 2b
                                                                                                                                     
                                                                                       P∞                  x
                                                                                                              P∞                 x
                                                                                                        −      +                −
                                                 
                                               T                   1                       x=0   exp                       exp
                                     = exp −                                   +                        2b       x=1          2b    
                                               2b       P                   |z|                       P                 |z|
                                                            z∈Z exp − 2b                                 z∈Z exp − 2b
                                                                                      
                                                 
                                               T                   1
                                     = exp −                                    + 1
                                               2b       P                   |z|
                                                            z∈Z exp − 2b
                                                   
                                                 T
                                     ≤ 2 exp −
                                                 2b

                                                       A PPENDIX C
                                             V ERIFICATION OF VERTEX COVER
   The extended logic used to prove the vertex cover in apRHL features a more precise rule for while loops, that allows the
privacy budget to vary at each iteration
                                            Θ =⇒ b1 ≡ b2 ∧ i1 = i2            Θ ∧ n ≤ i1 =⇒ ¬b1
                                            ⊢ c1 ∼hǫj ,δj i c2 : Θ ∧ b1 ∧ i1 = j =⇒ Θ ∧ i1 = j +1
                            ⊢ while b1 do c1 ∼hPn−1 ǫi ,Pn−1 δi i while b2 do c2 : Θ ∧ i1 = 0 =⇒ Θ ∧ ¬b1
                                                       i=0      i=0
and a code motion rule that allows to swap statements c1 and c2 provided they satisfy some independence condition:
                                    ⊢ c1 ; c2 ∼h0,0i c2 ; c1 : ∀x ∈ X.x1 = x2 =⇒ ∀x ∈ X.x1 = x2
In addition, the extended logic features a transitivity rule that allows to compose apRHL judgments. These rules can be readily
encoded in our setting, provided we allow for more general forms of products as considered in [4], [5].
   However, the extended logic also considers a probabilistic programming language with assert statements, and ad hoc rules
for random assignments and while loops:
                                    Θ =⇒ b1 ≡ b2 ∧ P1 ≡ P2
                                    ⊢ c1 ; assert (P1 ) ∼hǫ,δi c2 ; assert (P2 ) : Θ ∧ b1 ∧ ¬P1 =⇒ Θ
                                    ⊢ c1 ∼h0,0i c2 : Θ ∧ b1 =⇒ Θ
                                    ⊢ c1 ∼h0,0i c2 : Θ ∧ b1 ∧ P1 =⇒ Θ ∧ P1
                                       ⊢ while b1 do c1 ∼hǫ,δi while b2 do c2 : Θ =⇒ Θ ∧ ¬b1
These rules are not captured by our approach.
  For comparison, we briefly describe the proof in apRHL and the relational specifications of choose that are required for
completing the proof. For the first case, the apRHL proof uses the first generalized loop rule, and the following property of
choose:
              ⊢ v1 ← chooseǫ,n (g1 ) ∼Dǫ/2√n√|g |,0E v2 ← chooseǫ,n (g2 ) : g1 ∪ {hu1 , t1 i} = g2 =⇒ v1 = v2
                                                            1


In the second case, the apRHL uses the second generalized loop rule, and the following properties of choose:
                                                                                              
                  v1 ← chooseǫ,n (g1 );                            v2 ← chooseǫ,n (g2 );
       ⊢                                           ∼h0,0i                                            : g1 = g2 ∪ {hu2 , t2 i} =⇒ v1 = v2 ,
               assert (v1 6= u1 ∧ v1 6= t1 )                    assert (v2 6= u2 ∧ v2 6= t2 )

                                                                                              
                    v1 ← chooseǫ,n (g1 );                             v2 ← chooseǫ,n (g2 );
         ⊢                                          ∼h ǫ ,0i                                         : g1 = g2 ∪ {hu2 , t2 i} =⇒ v1 = v2 .
                 assert (v1 = u1 ∨ v1 = t1 )           4            assert (v2 = qu2 ∨ v2 t2 )
