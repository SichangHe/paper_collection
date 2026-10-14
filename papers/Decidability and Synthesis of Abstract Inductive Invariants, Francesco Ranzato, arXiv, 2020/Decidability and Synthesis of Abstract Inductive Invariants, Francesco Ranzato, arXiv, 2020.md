                                                  Decidability and Synthesis of Abstract Inductive Invariants

                                                                                          Francesco Ranzato

                                                                         Dipartimento di Matematica, University of Padova, Italy
arXiv:2004.03170v2 [cs.PL] 9 Apr 2020




                                               Abstract. Decidability and synthesis of inductive invariants ranging in a given domain play an important
                                               role in many software and hardware verification systems. We consider here inductive invariants belonging
                                               to an abstract domain A as defined in abstract interpretation, namely, ensuring the existence of the best
                                               approximation in A of any system property. In this setting, we study the decidability of the existence of
                                               abstract inductive invariants in A of transition systems and their corresponding algorithmic synthesis. Our
                                               model relies on some general results which relate the existence of abstract inductive invariants with least
                                               fixed points of best correct approximations in A of the transfer functions of transition systems and their
                                               completeness properties. This approach allows us to derive decidability and synthesis results for abstract
                                               inductive invariants which are applied to the well-known Kildall’s constant propagation and Karr’s affine
                                               equalities abstract domains. Moreover, we show that a recent general algorithm for synthesizing inductive
                                               invariants in domains of logical formulae can be systematically derived from our results and generalized to
                                               a range of algorithms for computing abstract inductive invariants.


                                        1 Introduction

                                        Proof and inference methods based on inductive invariants are widespread in automatic (or semi-automatic)
                                        program and system verification (see, e.g., [1, 3, 6, 9, 10, 11, 12, 18, 21, 22, 23, 26, 29, 32]). The inductive invariant
                                        proof method roots at the works of Floyd [14], Park [33, 34], Naur [31], Manna et al. [24] back to Turing [38].
                                        Given a transition system T = hΣ, τ, Σ0 i, e.g. representing a program, where τ is a transition relation on states
                                        ranging in Σ and Σ0 ⊆ Σ is a set of initial states, together with a safety property P ⊆ Σ to check, let us recall
                                        that a state property I ⊆ Σ is an inductive invariant for hT, P i when: Σ0 ⊆ I, i.e. the initial states satisfy I;
                                        I ⊆ P , i.e. I entails the safety property P ; τ (I) ⊆ I, i.e. I is inductive. The inductive invariant principle states
                                        that P holds for all the reachable states of T iff there exists an inductive invariant I for hT, P i. In this explicit
                                        form this principle has been probably first formulated by Cousot and Cousot [6, Section 5] in 1982 and called
                                        “induction principle for invariance proofs”. In most cases, verification and inference methods rely on inductive
                                        invariants I that range in some restricted domain A ⊆ ℘(Σ), such as a domain of logical formulae (e.g., some
                                        separation logic or some fragment of first-order logic [32]) or a domain of abstract interpretation [4, 5] (e.g.,
                                        numerical abstract domains of affine relations or convex polyhedra). In this scenario, if an inductive invariant I
                                        belongs to A then I is here called an abstract inductive invariant.

                                        Main Contributions. Our primary goal was to investigate whether and how the inductive invariant principle
                                        can be adapted when inductive invariants are restricted to range in an abstract domain A. We formulate this
                                        problem in general order-theoretical terms and we make the following working assumption: A ⊆ ℘(Σ) is an
                                        abstract domain as defined in abstract interpretation [4, 5]. This means that each state property X ∈ ℘(Σ)
                                        has a best over-approximation (w.r.t. ⊆) αA (X) in A and each state transition relation τ has a best correct
                                        approximation τ A on the abstract domain A. Under these hypotheses, we prove an abstract inductive invariant
                                        principle stating that there exists an abstract inductive invariant in A proving a property P of a transition system
                                        T iff the best abstraction T A in A of the system T allows us to prove P . The decidability/undecidability question
                                        of the existence of abstract inductive invariants in some abstract domain A for some class of transition systems
                                        has been recently investigated in a few significant cases [13, 17, 28, 37]. We show how the abstract inductive
invariant principle allows us to derive a general decidability result on the existence of inductive invariants in
some abstract domain A and to design a general algorithm for synthesizing the least (w.r.t. the order of A)
abstract inductive invariant in A, when this exists, by a least fixpoint computation in A.
     We also show a related result which is of independent interest in abstract interpretation: the (concrete)
inductive invariant principle for a system T is equivalent to the abstract inductive invariant principle for T on
an abstract domain A iff fixpoint completeness of T on A holds, i.e., the best abstraction in A of the reachable
states of T coincides with the reachable states of the best abstraction T A of T on A.
     The decidability/synthesis of abstract inductive invariants in a domain A for some class C of systems essen-
tially boils down to prove that the best correct approximation τ A in A of the transition relation τ of systems in
the class C is computable. As case studies, we provide two such results for Kildall’s constant propagation [20]
and Karr’s affine equalities [19] domains, which are well-known and widely used abstract domains in numerical
program analysis [25]. As a second application, we design an inductive invariant synthesis algorithm which,
by generalizing a recent algorithm by Padon et al. [32] tailored for logical invariants, outputs the most abstract
(i.e., weakest) inductive invariant in a domain A which satisfies some suitable hypotheses. In particular, we
show that this synthesis algorithm is obtained by instantiating a concrete co-inductive (i.e., based on a greatest
fixpoint computation) fixpoint checking algorithm by Cousot [2] to a domain A of abstract invariants which is
disjunctive, i.e., the abstract least upper bound of A does not lose precision. This generalization allows us to
design further related co-inductive algorithms for synthesizing abstract inductive invariants.


2 Background

2.1 Order Theory

If X is a subset of some universe set U then ¬X denotes the complement of X with respect to U when U is
implicitly given by the context. If f : X → Y is a function between sets and S ∈ ℘(X) then f (S) , {f (x) ∈
Y | x ∈ S} denotes the image of f on S. A composition of two functions f and g is denoted both by f g
or f ◦ g. If ~x ∈ X n is a vector in a product domain, j ∈ [1, n] and y ∈ X then ~x[xj /y] denotes the vector
obtained from ~x by replacing its j-th component xj with y. To keep the notation simple and compact, we use
the same symbol for a function/relation and its componentwise (i.e. pointwise) extension on product domains,
         ~ T~ ∈ ℘(X)n then S
e.g., if S,                   ~ ⊆ T~ denotes that for all i ∈ [1, n], S
                                                                      ~i ⊆ T~i . Sometimes, to emphasize a pointwise
                                                          ˙
definition, a dotted notation can be used such as in f ≤ g for the pointwise ordering between functions.
    A quasiordered set hD, ≤i (qoset), compactly denoted by D≤ , is a set D endowed with a quasiorder (qo)
relation ≤ on D, i.e. a reflexive and transitive binary relation. A qoset D≤ satisfies the ascending (resp. de-
scending) chain condition (ACC, resp. DCC) if D contains no countably infinite sequence of distinct elements
{xi }i∈N such that, for all i ∈ N, xi ≤ xi+1 (resp. xi+1 ≤ xi ). An antichain in a qoset D is a subset X ⊆ D such
that any two distinct elements in X are incomparable for the qo ≤. A qoset D≤ is a partially ordered set (poset)
when ≤ is antisymmetric. A subset X ⊆ D of a poset is directed if X is nonempty and every pair of elements
in X has an upper bound in X. A poset is a directed-complete partial order (CPO) if it has the least upper bound
(lub) of all its directed subsets. A complete lattice is a poset having the lub of all its arbitrary (possibly empty)
subsets (and therefore also having arbitrary glb’s). In a complete lattice (or CPO), ∨ (or ⊔) and ∧ (or ⊓) denote,
resp., lub and glb, and ⊥ and ⊤ denote, resp., least and greatest element.
    Let P≤ be a poset and f : P → P . Then, Fix(f ) , {x ∈ P | f (x) = x}, Fix≤ (f ) , {x ∈ P | f (x) ≤ x},
Fix (f ) , {x ∈ P | f (x) ≥ x}, and lfp(f ), gfp(f ) denote, resp., the least and greatest fixpoint in Fix(f ),
    ≥


when they exist. Let us recall Knaster-Tarski fixpoint theorem: if hC, ≤, ∨, ∧i is a complete lattice and f : C →
C is monotonic (i.e., x ≤ y implies f (x) ≤ f (y)) then hFix(f ), ≤i is a complete lattice, lfp(f ) = ∧ Fix≤ (f )
and gfp(f ) = ∨ Fix≥ (f ). Also, Knaster-Tarski-Kleene fixpoint theorem states that if hC, ≤, ∨, ⊥i is a CPO and
f : C → C is Scott-continuous (i.e., f preserves lub of directed subsets) then lfp(f ) = ∨i∈N f i (⊥), where, for
all x ∈ C and i ∈ N, f 0 (x) , x and f i+1 (x) , f (f i (x)); dually, if hC, ≤, ∧, ⊤i is a dual-CPO and f : C → C

                                                         2
is Scott-co-continuous then gfp(f ) = ∧i∈N f i (⊤). A function f : C → C on a complete lattice is additive when
it preserves arbitrary lubs.

2.2 Abstract Domains
Let us recall some basic notions on closures and Galois connections which are commonly used in abstract
interpretation [4,5] to define abstract domains (see, e.g., [25,36]). Closure operators and Galois connections are
equivalent notions and are both used for defining the notion of approximation in abstract interpretation, where
closure operators bring the advantage of defining abstract domains independently of a specific representation
which is required by Galois connections.
    An upper closure operator (uco), or simply upper closure, on a poset C≤ is a function µ : C → C which
is: monotonic, idempotent and extensive, i.e., x ≤ µ(x) for all x ∈ C. Dually, a lower closure operator (lco)
η : C → C is monotonic, idempotent and reductive, i.e., η(x) ≤ x for all x ∈ C. The set of all upper/lower
closures on C≤ is denoted by uco(C≤ )/lco(C≤ ). We write c ∈ µ(C), or simply c ∈ µ, to denote that there
exists c′ ∈ C such that c = µ(c′ ), and we recall that this happens iff µ(c) = c. Let us also recall that hµ(C), ≤i
is closed under glb of arbitrary subsets and, conversely, X ⊆ C is the image of some µ ∈ uco(C) iff X
is closed under glb of all its subsets, and in this case µ(c) = ∧{c′ ∈ X | c ≤ c′ } holds. Dually, X ⊆ C
is closed under arbitrary lub of its subsets iff X is the image a lower closure η ∈ lco(C), and in this case
η(c) = ∨{c′ ∈ X | c′ ≤ c}. In abstract interpretation, a closure µ ∈ uco(C≤ ) on a concrete domain C≤
plays the role of an abstract domain having best approximations: c ∈ C is approximated by any µ(c′ ) such that
c ≤ µ(c′ ) and µ(c) is the best approximation of c in µ because µ(c) = ∧{µ(c′ ) | c′ ∈ C, c ≤ µ(c′ )}.
    A Galois Connection (GC) (also called adjunction) between two posets hC, ≤C i, called concrete domain,
and hA, ≤A i, called abstract domain, consists of two maps α : C → A and γ : A → C such that α(c) ≤A a ⇔
c ≤C γ(a) holds. A GC is called Galois insertion (GI) when α is surjective or, equivalently, γ is injective. Any
GC can be transformed into a GI simply by removing useless elements in A r α(C) from the abstract domain
A. A GC/GI is denoted by (C≤C , α, γ, A≤A ). The function α is called the left-adjoint of γ, and, dually, γ is
called the right-adjoint of α. This terminology is justified by the fact that if α : C → A admits a right-adjoint
γ : A → C then this is unique, and this dually holds for left-adjoints. GCs and ucos are equivalent notions
because any GC G = (C, α, γ, A) induces a closure µG , γ ◦ α ∈ uco(C), any µ ∈ uco(C) induces a GI
Gµ , (C, µ, λx.x, µ(C)), and these two transforms are inverse of each other.

2.3 Transition Systems
Let T = hΣ, τ i be a transition system where Σ is a set of states and τ ⊆ Σ × Σ is a transition relation. As usual,
a transition relation can be equivalently defined by one of the following transformers of type ℘(Σ) → ℘(Σ):

          pre(X) , {s ∈ Σ | ∃s′ ∈ X.(s, s′ ) ∈ τ } pre(X)
                                                   f      , {s ∈ Σ | ∀s′ .(s, s′ ) ∈ τ ⇒ s′ ∈ X}
          post(X) , {s′ ∈ Σ | ∃s ∈ X.(s, s′ ) ∈ τ } post(X)
                                                    g       , {s′ ∈ Σ | ∀s.(s, s′ ) ∈ τ ⇒ s ∈ X}

We will equivalently specify a transition system by one of the above transformers (typically post) in place of
                                                                         g and hpost, prei
the transition relation τ . Let us also recall (see e.g. [7]) that hpre, posti        f are pairs of adjoint
functions. The set of reachable states of T from a set of initial states Σ0 ⊆ Σ is given by Reach[T, Σ0 ] ,
lfp(λX.Σ0 ∪ post(X)), and T satisfies a safety property P ⊆ Σ when Reach[T, Σ0 ] ⊆ P holds.

2.4 Inductive Invariant Principle
Given a transition system T = hΣ, τ i, a set of states I ∈ ℘(Σ) is an inductive invariant for T w.r.t. hΣ0 , P i ∈
℘(Σ)2 when: (i) Σ0 ⊆ I; (ii) post(I) ⊆ I; (iii) I ⊆ P . An inductive invariant I allows us to prove that T is safe,

                                                        3
i.e. Reach[T, Σ0 ] ⊆ P , by the inductive invariant principle (a.k.a. fixpoint induction principle), a consequence
of Knaster-Tarski fixpoint theorem: If C≤ is a complete lattice, c′ ∈ C and f : C → C is monotonic then

                                      lfp(f ) ≤ c′ ⇔ ∃i ∈ C.f (i) ≤ i ∧ i ≤ c′                                 (1)

In particular, given c, c′ ∈ C, since c ∨C f (i) ≤ i iff c ≤ i ∧ f (i) ≤ i, it turns out that:

                           lfp(λx.c ∨C f (x)) ≤ c′ ⇔ ∃i ∈ C.c ≤ i ∧ f (i) ≤ i ∧ i ≤ c′                         (2)

One such i ∈ C such that c ≤ i ∧ f (i) ≤ i ∧ i ≤ c is called an inductive invariant of f for hc, c′ i. Hence,
(2) is applied to the function λX.Σ0 ∪ post(X) : ℘(Σ) → ℘(Σ), which is monotonic on the complete lattice
℘(Σ)⊆ , so that lfp(λX.Σ0 ∪ post(X)) ⊆ P holds iff there exists an inductive invariant I for T w.r.t. hΣ0 , P i. In
most interesting contexts for defining transition systems, the decision problem of the existence of a (concrete)
inductive invariant for a class of transition systems w.r.t. a set of initial states and some safety property is
undecidable.


3 Abstract Inductive Invariants

Padon et al. [32], Hrushovski et al. [17], Fijalkow et al. [13], Monniaux [28], Shoham [37], among the others,
consider a notion of abstract inductive invariant and study the corresponding decidability/undecidability and
synthesis problems. The common approach of this stream of works consists in restricting the range of inductive
invariants from a concrete domain C to some abstraction AC of C. In a basic and general form, a domain AC
of abstract invariants is simply a subset of C. Let us formalize abstract inductive invariants in general order-
theoretic terms. Given a class C of complete lattices and, for all C ∈ C, a class of functions FC ⊆ C → C, a
set of initial properties InitC ⊆ C, a set of safety properties SafeC ⊆ C, and some abstract domain AC ⊆ C, a
first problem is the decidability of the following decision question:

                ∀C ∈ C.∀f ∈ FC .∀c ∈ InitC .∀c′ ∈ SafeC .∃i ∈?AC . c ≤ i ∧ f (i) ≤ i ∧ i ≤ c′                  (3)

where one such i ∈ AC is called an abstract inductive invariant for f and hc, c′ i ∈ C 2 . On the other hand, the
synthesis problem consists in designing algorithms which output abstract inductive invariants in AC or notify
that no inductive invariant in AC exists.
    Given a transition system T = hΣ, τ i whose successor transformer is post, the problem (3) is instantiated
to C≤ = ℘(Σ)⊆ , f = post(X), c = Σ0 ∈ ℘(Σ) set of initial states and c′ = P ∈ ℘(Σ) safety property.
When the transition system is generated by some imperative program, Σ0 are the states of some initial control
node and P is a safety property given by the states which are not in some bad control node, abstract inductive
invariants are called separating invariants and the decision problem (3) is called Monniaux problem by Fijalkow
et al. [13], because this was first formulated by Monniaux [27, 28].


3.1 Abstract Inductive Invariant Principle

Our working assumption is that in problem (3) invariants i range in an abstract domain A as defined in abstract
interpretation [4, 5].
Assumption 3.1. hA, ≤A i is an abstract domain of the complete lattice hC, ≤C i which has best approxima-
tions, i.e., one of these two equivalent assumptions is satisfied:

  (i) (C≤C , α, γ, A≤A ) is a Galois insertion;
 (ii) hA, ≤A i = hµ(C), ≤C i for some upper closure µ ∈ uco(C≤C ).                                               ⊓
                                                                                                                 ⊔

                                                           4
    Under Assumption 3.1, let us recall that if f : C → C is a concrete monotonic function then the mappings
αf γ : A → A, for the case of GIs, and µf : µ(C) → µ(C), for the case of ucos, are called best correct
approximation (bca) in A of f . This is justified by the observation that an abstract function f ♯ : A → A (or
f ♯ : µ(C) → µ(C) for ucos) is a correct (or sound) approximation of f when αf γ ≤         ˙ A f ♯ (or µf ≤˙ C f♯
for ucos) holds. Our first result is an abstract inductive invariant principle which restricts the invariants of f
in (1) to those ranging in an abstract domain A: when the abstract domain A is specified by a GI, this means
that a ∈ A is an abstract invariant of f when f γ(a) ≤C γ(a) holds; when the abstract domain is a closure
µ ∈ uco(C), this means that a ∈ µ ⊆ C is an abstract invariant of f when f a ≤C a holds.

Lemma 3.2 (Abstract Inductive Invariant Principle). Let (C≤C , α, γ, A≤A ) be a GI. For all c′ ∈ C and
a′ ∈ A:
(a) γ(lfp(αf γ)) ≤C c′ ⇔ ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C c′ ;
(b) lfp(αf γ) ≤A a′ ⇔ ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C γ(a′ ).

Proof. Let us first recall that in a GI, for all a, a′ ∈ A, a ≤A a′ ⇔ γ(a) ≤C γ(a′ ) holds.
(a) (⇐) We have that:

                       ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C c′ ⇔           [by GC]
                        ∃a ∈ A. αf γ(a) ≤A a ∧ γ(a) ≤C c′ ⇒            [by F x ≤ x ⇒ lfp(F ) ≤ x]
                     ∃a ∈ A. lfp(αf γ) ≤A a ∧ γ(a) ≤C c′ ⇔             [by GI]
                ∃a ∈ A. γ(lfp(αf γ)) ≤C γ(a) ∧ γ(a) ≤C c′ ⇒            [by transitivity]
                                           γ(lfp(αf γ)) ≤C c′

(⇒) Define a , lfp(αf γ) ∈ A. It turns out that αf γ(a) ≤A a so that, by GC, f γ(a) ≤C γ(a), and, by
hypothesis, γ(a) ≤C c′ .
(b) It turns out that:

                      ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C γ(a′ ) ⇔          [By Lemma 3.2 (a)]
                                        γ(lfp(αf γ)) ≤C γ(a′ ) ⇔         [by GI]
                                                  lfp(αf γ) ≤A a′                                                  ⊓
                                                                                                                   ⊔

It is worth stating Lemma 3.2 (a) in an equivalent form for an abstract domain represented by a closure µ ∈
uco(C): lfp(µf ) ≤C c′ ⇔ ∃a ∈ µ. f a ≤C a ∧ a ≤C c′ .
     Let us observe that point (b) is an easy consequence of point (a), because, by surjectivity of α in GIs, for all
a′ ∈ A, there exists some c′ ∈ C such that a′ = α(c′ ), and γ(lfp(αf γ)) ≤C γ(α(c′ )) ⇔ lfp(αf γ) ≤A α(c′ )
holds. Moreover, point (b) easily follows from the inductive invariant principle (1) for the bca αf γ : A → A.
On the other hand, point (a) cannot be obtained from (b), i.e. (a) is strictly stronger than (b), because (a) allows
us to prove concrete properties c′ ∈ C which are not exactly represented by A (i.e., c′ 6∈ γ(A)) by abstract
inductive invariants in A. This is shown by the following tiny example.

Example 3.3. Consider a 4-point chain C = {1 < 2 < 3 < 4}, the function f : C → C defined by {1 7→
1; 2 7→ 2; 3 7→ 4; 4 7→ 4}, and the abstraction A = {2, 4} with γ = id and α = {1 7→ 2; 2 7→ 2; 3 7→ 4; 4 7→ 4}.
Here, we have that αf γ = {2 7→ 2; 4 7→ 4} and lfp(αf γ) = 2. In this case, Lemma 3.2 (b) allows us to prove
all the abstract properties a′ ∈ A by abstract inductive invariants, while Lemma 3.2 (a) allows us to prove an
additional concrete property 3 ∈ C r γ(A), which is not exactly represented by A, by an abstract inductive
invariant, and this would not be possible by resorting to Lemma 3.2 (b). Also, γ(lfp(αf γ)) 6≤ 1 holds, thus,
by Lemma 3.2 (a), the concrete property 1 cannot be proved by an abstract inductive invariant in A, whereas
Lemma 3.2 (b) does not allow us to infer this.                                                                ⊓
                                                                                                              ⊔

                                                         5
    Lemma 3.2 (b) tells us that the existence of an abstract inductive invariant of f proving an abstract property
a′ ∈ A is equivalent to the fact that the least fixpoint of the best correct approximation αf γ entails a′ . This
formalizes for an abstract domain satisfying Assumption 3.1 an observation in [13, Section 1] stating that “the
existence of some abstract inductive invariant for αf γ proving a′ is equivalent to whether the strongest abstract
invariant lfp(αf γ) entails a′ ”, i.e. is inductive. If, instead, we aim at proving any concrete property c′ ∈ C,
possibly not in γ(A), by an abstract inductive invariant then Lemma 3.2 (a) states that this is equivalent to the
stronger condition γ(lfp(αf γ)) ≤C c′ .
    As a consequence of Lemma 3.2 (a) we derive the following characterization of the problem (3).
Corollary 3.4. Let F ⊆ C → C and Init, Safe ⊆ C. The Monniaux decision problem ∀f ∈ F.∀c ∈ Init .∀c′ ∈
Safe .∃a ∈? A. c ≤C γ(a) ∧ f γ(a) ≤C γ(a) ∧ γ(a) ≤C c′ is decidable iff the decision problem ∀f ∈ F.∀c ∈
Init .∀c′ ∈ Safe .γ(lfp(λx ∈ A.α(c) ∨A αf γ(x))) ≤?C c′ is decidable.
Proof. By Lemma 3.2 (a), because λx ∈ A.α(c) ∨A αf γ(x) = λx ∈ A.α(c ∨C f γ(x)) is the best correct
approximation of λx ∈ C.c ∨C f (x).                                                              ⊓
                                                                                                 ⊔
    Moreover, as a consequence of Lemma 3.2 (b) we obtain the following abstract invariant synthesis algorithm.
Corollary 3.5. Assume that the lub ∨A : A × A → A and the bca αf γ : A → A are computable, the partial
order ≤?A is decidable and A is an ACC CPO. For all c ∈ C such that α(c) is computable and a′ ∈ A, the
following procedure AI NV(f, A, c, a′ ):
                        i := α(c);
                        while i ≤A a′ do { if αf γ(i) ≤A i return i; else i := αf γ(i); }
                        return no abstract inductive invariant for f and hc, γ(a′ )i;

is a terminating algorithm which outputs the least abstract inductive invariant for f and hc, γ(a′ )i, when one
such abstract inductive invariant exists, otherwise outputs “no abstract inductive invariant”.
Proof. The hypotheses guarantee that the procedure AI NV is a terminating algorithm, in particular because
the sequence of computed iterates i is an ascending chain in A. If the algorithm AI NV outputs i then i =
lfp(λa.α(c) ∨A αf γ(a)) ≤A a′ , so that i = ∧{a ∈ A | α(c) ≤A i, αf γ(i) ≤A i, i ≤A a′ }, that is, i is
the least inductive invariant in A for f and hc, γ(a′ )i. If the algorithm AI NV outputs “no abstract inductive
invariant for f and hc, γ(a′ )i” then there exists j ∈ N such that (λa.α(c) ∨A αf γ(a))j (⊥A ) 6≤A a′ , so that
lfp(λa.α(c) ∨A αf γ(a)) 6≤A a′ , that is, there exists no inductive invariant in A for f and hc, γ(a′ )i.    ⊓
                                                                                                             ⊔

3.2 Fixpoint Completeness in Abstract Interpretation
Soundness in abstract interpretation (more in general, in static analysis) is a mandatory requirement stating
that no false negative can occur, that is, abstract fixpoint computations correctly (over-)approximate the cor-
responding concrete semantics: if f : C → C and f ♯ : A → A are the concrete and abstract monotonic
transformers then fixpoint soundness means that α(lfp(f )) ≤A lfp(f ♯ ) holds, so that a positive abstract check
lfp(f ♯ ) ≤A a′ entails that γ(a′ ) concretely holds, i.e., lfp(f ) ≤C γ(a′ ). Fixpoint soundness is usually obtained
as a consequence of pointwise soundness: if f ♯ is a pointwise correct approximation of f , i.e. αf ≤     ˙ A f ♯ α, then
                      ♯
α(lfp(f )) ≤A lfp(f ) holds.
    While soundness is indispensable, completeness in abstract interpretation encodes an ideal situation where
no false positives (also called false alarms) arise: fixpoint completeness means that α(lfp(f )) = lfp(f ♯ ) holds,
so that lfp(f ♯ ) 6≤A a′ entails lfp(f ) 6≤C γ(a′ ). One can also consider a strong fixpoint completeness requiring
that lfp(f ) = γ(lfp(f ♯ )), so that lfp(f ♯ ) 6≤A α(c′ ) entails lfp(f ) 6≤C c′ . However, it should be remarked that
lfp(f ) = γ(lfp(f ♯ )) is much stronger than α(lfp(f )) = lfp(f ♯ ) since it means that the concrete lfp is precisely
represented by the abstract lfp.

                                                           6
    It is important to remark that if f ♯ is a pointwise correct approximation of f and fixpoint completeness
for f ♯ holds then since α(lfp(f )) ≤A lfp(αf γ) ≤A lfp(f ♯ ) always holds, one also obtains that α(lfp(f )) =
lfp(αf γ) = lfp(f ♯ ) holds, namely, the best correct approximation αf γ is fixpoint complete as well. This means
that the possibility (or impossibility) of defining an approximate transformer f ♯ : A → A on A which is fixpoint
complete does not depend on the specific definition of f ♯ but is instead an intrisic property of the abstract domain
A w.r.t. the concrete transformer f , as formalized by the equation α(lfp(f )) = lfp(αf γ). Moreover, fixpoint
completeness is typically proved as a by-product of pointwise completeness αf = f ♯ α, and if f ♯ is pointwise
complete then it turns out that f ♯ = αf γ, that is, f ♯ actually is the bca of f . This justifies why, without loss of
generality, we can consider fixpoint and pointwise completeness of bca’s αf γ only, i.e., a property of abstract
domains.

3.3 Characterizing Fixpoint Completeness by Abstract Inductive Invariants
We show that the abstract inductive invariant principle is closely related to fixpoint completeness. More pre-
cisely, we provide an answer to the following question: in the abstract inductive invariant principle as stated by
Lemma 3.2, can we replace lfp(αf γ) with α(lfp(f ))? This question is settled by the following result.
Theorem 3.6. Let (C≤C , α, γ, A≤A ) be a GI.
                                                                                           
(a) lfp(f ) = γ(lfp(αf γ)) iff ∀c′ ∈ C. lfp(f ) ≤C c′ ⇔ ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C c′ ;      
(b) α(lfp(f )) = lfp(αf γ) iff ∀a′ ∈ A. lfp(f ) ≤C γ(a′ ) ⇔ ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C γ(a′ ) .
Proof. (a) (⇒): By Lemma 3.2 (a).
(⇐): Since lfp(f ) ≤C lfp(f ) holds, we have that ∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C lfp(f ). Thus, by
Lemma 3.2 (a), γ(lfp(αf γ)) ≤C lfp(f ) follows. On the other hand, lfp(f ) ≤ γ(lfp(αf γ)) always holds because
the pointwise correctness of αf γ implies α(lfp(f )) ≤A lfp(αf γ), hence, by GC, lfp(f ) ≤ γ(lfp(αf γ)) follows.
(b) (⇒): By Lemma 3.2 (b) because lfp(αf γ) ≤A a′ ⇔ α(lfp(f )) ≤ a′ ⇔ lfp(f ) ≤C γ(a′ ).
(⇐): We consider a′ , α(lfp(f )), so that, lfp(f ) ≤C γ(a′ ) holds and by the equivalence of the hypothesis,
∃a ∈ A. f γ(a) ≤C γ(a) ∧ γ(a) ≤C γα(lfp(f )) holds. This implies, by GI, that ∃a ∈ A. αf γ(a) ≤C a ∧ a ≤A
α(lfp(f )). By the inductive invariant principle (1), this implies that (actually, is equivalent to) lfp(αf γ) ≤
α(lfp(f )). Furthermore, α(lfp(f )) ≤A lfp(αf γ) always holds, therefore proving that α(lfp(f )) = lfp(αf γ).
                                                                                                               ⊓
                                                                                                               ⊔
Theorem 3.6 (b) can be stated by means of ucos as follows: if µ ∈ uco(C) then µ(lfp(f )) = lfp(µf ) iff
∀a′ ∈ µ.(lfp(f ) ≤C a′ ⇔ ∃a ∈ µ. f a ≤C a ∧ a ≤C a′ ).
    The above result can be read as follows. Since, by the inductive invariant principle (1), lfp(f ) ≤C c′ iff there
exists a (concrete) inductive invariant proving c′ , it turns out that Theorem 3.6 (a) states that, for all c′ ∈ C,
the existence of an abstract inductive invariant proving c′ is equivalent to the existence of any inductive in-
variant proving c′ iff fixpoint completeness holds. In other terms, the (concrete) inductive invariant principle is
equivalent to the abstract inductive invariant principle iff fixpoint completeness holds. This result is of indepen-
dent interest in abstract interpretation, since it provides a new characterization of the key property of fixpoint
completeness of abstract domains [15].
    A further interesting characterization of fixpoint completeness is as follows.
Lemma 3.7. α(lfp(f )) = lfp(αf γ) ⇔ ∃a ∈ A.f γ(a) ≤C γ(a) ∧ γ(a) ≤C γα(lfp(f )).
Proof.
               ∃a ∈ A.f γ(a) ≤C γ(a) ∧ γ(a) ≤C γα(lfp(f )) ⇔ [by GI]
                    ∃a ∈ A.αf γ(a) ≤A a ∧ a ≤A α(lfp(f )) ⇔ [by (1) for αf γ]
                                         lfp(αf γ) ≤A α(lfp(f )) ⇔ [as α(lfp(f )) ≤A lfp(αf γ)]
                                           α(lfp(f )) = lfp(αf γ)                                                    ⊓
                                                                                                                     ⊔

                                                          7
As a consequence, fixpoint completeness for f does not hold in A iff the abstract property α(lfp(f )) ∈ A cannot
be proved by an abstract inductive invariant in A

Example 3.8. Consider the finite chain C , {1 < 2 < 3} and the monotonic concrete function f : C → C
defined by f , {1 7→ 1; 2 7→ 3; 3 7→ 3}.
Consider the uco µ , {2, 3}, i.e., µ = {1 7→ 2; 2 7→ 2; 3 7→ 3}. Hence, µf = {1 7→ 2; 2 7→ 3; 3 7→ 3} so that
fixpoint completeness does not hold because µ(lfp(f )) = µ(1) = 2 < 3 = lfp(µf ). Thus, in accordance with
Lemma 3.7, it turns out that µ(lfp(f )) = 2 cannot be inductively proved in the abstraction µ. In fact, f (2) 6≤ 2,
while f (3) ≤ 3 but 3 6≤ µ(lfp(f )).
Consider instead the uco µ , {1, 3}, i.e., µ = {1 7→ 1; 2 7→ 3; 3 7→ 3}, so that µf = {1 7→ 1; 2 7→ 3; 3 7→ 3}.
Here, µ(lfp(f )) = µ(1) = 1 = lfp(µf ), therefore fixpoint completeness holds. Thus, by the uco version of
Theorem 3.6 (b), any valid abstract invariant of f can be inductively proved: in fact, 1, 3 ∈ µ are valid abstract
invariants of f and are both inductive.                                                                          ⊓
                                                                                                                 ⊔

3.4 When Safety = Abstract Invariance?
Padon et al. [32, Section 9] in their investigation on the decidability of inferring inductive invariants state that
“Usually completeness for abstract interpretation means that the abstract domain is precise enough to prove all
interesting safety properties, e.g., [15]. In our terms, this means that SAFE = INV , that is, that all safe programs
have an inductive invariant expressible in the abstract domain.” As a by-product of the results in Section 3.3,
we are able to give a formal justification and statement of this informal characterization of completeness.
    Let F ⊆ C → C be a class of monotonic functions, S ⊆ C be some set of safety properties and A ⊆ C be
an abstract domain of program properties. Let us define:

                         SAFE [F, S] , {hf, si ∈ F × S | lfp(f ) ≤C s}

                         INV [F, S, A] , {hf, si ∈ F × S | ∃a ∈ A. f a ≤C a ∧ a ≤C s}

so that in our model SAFE[F, S] and INV [F, S, A] play the role of, resp., “safe programs” and “programs having
an inductive invariant expressible in A”. As a consequence of Theorem 3.6, we derive the following characteri-
zation.

Corollary 3.9. Assume that A satisfies Assumption 3.1 for some GI hC, α, γ, Ai.
(a) Assume that S ⊆ A. Then, SAFE[F, S] = INV[F, S, A] iff ∀f ∈ F.α(lfp(f )) = lfp(αf γ).
(b) SAFE[F, S] = INV[F, S, A] iff ∀f ∈ F. lfp(f ) = γ(lfp(αf γ)).

Proof. (a) follows by Theorem 3.6 (a), since S ⊆ A is assumed to hold. (b) follows by Theorem 3.6 (b).             ⊓
                                                                                                                   ⊔

     Corollary 3.9 therefore provides a precise equivalence of the SAFE =? INV problem, as stated by Padon et
al. [32], with fixpoint completeness (strong fixpoint completeness, in case (b)) in abstract interpretation.


4 Abstract Inductive Invariants of Programs
We consider transition systems as represented by a finite control flow graph (CFG) of an imperative program.
A program is a tuple P = hQ, n, V, T, i where Q is a finite set of control nodes (or program points), n ∈ N is
the number of program variables of type V (e.g., V = Z, Q, R), T is a finite set of (possibly nondeterministic)
transfer functions of type Vn → ℘(Vn ),  ⊆ Q × T × Q is a (possibly nondeterministic) control flow relation,
          t
where q → q ′ denotes a flow transition with transfer function t ∈ T. A program P therefore defines a transition
system TP = hΣ, τ i where Σ , Q × Vn is the set of states and the transition relation τ ⊆ Σ × Σ is defined by

                                                         8
                       △              t
h(q, ~v ), (q ′ , ~v ′ )i ∈ τ ⇔ ∃t ∈ T. q → q ′ ∧ ~v ′ ∈ t(~v ). The transfer functions in T include imperative assignments
and Boolean guards: if b ∈ ℘(Vn ) is a deterministic Boolean predicate (such as x1 + 2x2 − 1 = 0) then the
corresponding transfer function tb : Vn → ℘(Vn ) is tb (~v ) , if ~v ∈ b then {~v } else ∅. Examples of transfer
functions include: affine, polynomial, nondeterministic assignments and affine equalities guards.
    The next value transformer posthq,q′ i : ℘(Vn ) → ℘(Vn ) for a pair hq, q ′ i ∈ Q × Q of control nodes is
                                                          t                                    t
posthq,q′ i (X) , ∪{t(X) ∈ ℘(Vn ) | ∃t ∈ T.q → q ′ }. Hence, if, for all t ∈ T, q →           6 q ′ then posthq,q′ i = λX.∅.
The complete lattice h℘(Σ), ⊆i of sets of states can be equivalently represented by the Q-indexed product lattice
h℘(Vn )|Q| , ⊆i.    ˙ Hence, the successor transformer postP : ℘(Vn )|Q| → ℘(Vn )|Q| and the set of reachable states
of a program P from initial states in Σ0 ∈ ℘(Vn )|Q| are defined as follows:

                               postP (hXq iq∈Q ) , h∪q∈Q posthq,q′ i (Xq )iq′ ∈Q
                                                    ~ 0 ∪ postP (X))
                               Reach[P, Σ0 ] , lfp(λX.Σ          ~ ∈ ℘(Vn )|Q|

For all control nodes q ∈ Q and vector X ~ ∈ ℘(Vn )|Q| , we will also use πq (X)
                                                                               ~ and X  ~ q to denote the q-indexed
component of X, ~ e.g., Reach[P, Σ0 ]q ∈ ℘(V ) will be the set of reachable values at control node q.
                                               n

    We are interested in decidability and synthesis of abstract inductive invariants ranging in an abstract domain
A as specified by a GI (℘(Vn )⊆ , α, γ, A≤A ) parametric on n ∈ N. By Corollary 3.4, for a given class C
of programs, a class Init of sets of initial states and a class Safe of sets of safety properties, the Monniaux
problem (3) is decidable iff for all P = hQ, n, V, T, i ∈ C, Σ0 ∈ Init and P ∈ Safe,
                                                                                      ?
                                                                                    ˙ P
                               γ̇(lfp(λ~a ∈ A|Q|. α̇(Σ0 ) ∨˙ A α̇(postP (γ̇(~a))))) ⊆                                   (4)

is decidable. Moreover, Corollary 3.5 provides an abstract inductive invariant synthesis algorithm AI NV for
safety properties represented by A (i.e., P ∈ γ(A)) when A, C, Init and Safe satisfy the hypotheses of Corol-
lary 3.5.
    In the following, we consider the decidability/synthesis problem (3) for Kildall’s constant propagation [20]
and Karr’s affine equalities [19] abstract domains.

4.1 Kildall’s Constant Propagation Domain
Kildall’s constant propagation [20] is a well-known and simple program analysis widely used in compiler opti-
mization for detecting whether a variable at some program point always stores a constant value for all possible
program executions. Constant propagation relies on the abstract domain C ONST, which, for simplicity, is here
given for program variables assuming integer values in Z (Q and R would be analogous). For a single variable
C ONST , hZ ∪ {⊥, ⊤}, ≤i, where ≤ is the standard flat partial order: for any a ∈ Z ∪ {⊥, ⊤}, ⊥ ≤ a ≤ ⊤ (and
a ≤ a), which makes C ONST an infinite complete lattice with height 2. C ONST is straightforwardly specified
by a GI (℘(Z)⊆ , αC , γC , C ONST≤ ) where:
                                                                       
                                 
                                 ⊥ if X = ∅                            
                                                                        ∅      if a = ⊥
                       αC (X) , z if X = {z}                 γC (a) , {a} if a ∈ Z
                                 
                                                                       
                                                                        
                                    ⊤ otherwise                           Z     if a = ⊤

For n ≥ 1 variables, the product constant domain is C ONSTn , (C ONST⊥ )n ∪ {⊥}, where C ONST⊥ ,
C ONST r{⊥}, so as to have a unique bottom element representing the empty set, while αCONST : ℘(Zn ) →
C ONST and γCONST : C ONST → ℘(Zn ) are defined as pointwise lifting of, resp., αC and γC . hC ONST n , ≤i   ˙ is a
complete lattice of finite height 2n, where lub and glb are defined pointwise. Finally, for a finite set of control
nodes Q, α̇CONST : ℘(Zn )|Q| → C ONST|Q| and γ̇ CONST : C ONST |Q| → ℘(Zn )|Q| are the Q-indexed pointwise
lifting of, resp., αCONST and γCONST .

                                                             9
    It is known since [16,35] that the constant propagation problem is undecidable, meaning that for any program
P with n variables, set Σ0 of initial states, node q of P, vector of constants (or ⊤) ~k ∈ C ONST n r{⊥}, the
problem αCONST (Reach[P, Σ0 ]q ) ≤? ~k is undecidable. This undecidability is obtained by a simple reduction
from the undecidable Post correspondence problem and holds even if the interpretation of program branches is
neglected, that is, in CFGs with unguarded nondeterministic branching.
    By Corollary 3.4, the existence of abstract inductive invariants in C ONST for a given class C of programs,
Init of sets of initial states and Safe of sets of safety properties, is a decidable problem iff for all P ∈ C with n
variables and control nodes in Q, for all Σ0 ∈ InitP ⊆ ℘(Vn )|Q| and for all P ∈ SafeP ⊆ ℘(Vn )|Q| ,
                                                                                                     ?
             γ̇CONST (lfp(λ~a ∈ C ONST|Q|              ˙
                                      n .α̇C ONST (Σ0 )∨C ONST nα̇C ONST (postP (γ̇C ONST (~
                                                                                                  ˙ P
                                                                                           a))))) ⊆                (5)

is decidable. We observe that:
  (i) if P is a recursive set and ~a ∈ C ONST|Q|
                                               n then γ̇C ONST (~
                                                                a) ⊆˙ ? P is clearly decidable, because for all q ∈ Q,
      i ∈ [1, n] and k ∈ Z, k ∈? πi (πq (P )) is decidable (and any γ̇CONST (~a′ ) is trivially recursive);
 (ii) if Σ0 is a recursively enumerable (r.e.) set then α̇CONST (Σ0 ) is clearly computable, because since Σ0 is
      r.e., for all q ∈ Q and i ∈ [1, n], a (double) projection πi (πq (Σ0 )) is r.e., so that an algorithm enumerating
      πi (πq (Σ0 )) allows us to compute its abstraction αC in C ONST ;
(iii) the binary lub ~a ∨CONST n ~a′ in C ONSTn is clearly (pointwise) computable, thus, in turn, the Q-indexed lub
      ∨˙ CONST n is computable.

     Therefore, since C ONST|Q|
                             n has finite height, a sufficient condition for the decidability of the problem (5) is
that the best correct approximation α̇CONST ◦ postP ◦ γ̇CONST : C ONST|Q|             |Q|
                                                                       n → C ONST n is computable, where for
                |Q|
all ~a ∈ C ONSTn :
                                                                  α̇CONST (postP (γ̇CONST (~a))) =
                                 h∨CONST {αCONST (postq,q′ (πq (γ̇CONST (~a)))) | q ∈ Q}iq′ ∈Q =
                     h∨CONST {αCONST (t(πq (γ̇CONST (~a)))) | ∃q ∈ Q, ∃t ∈ T.q → q ′ }iq′ ∈Q
                                                                                   t
                                                                                                                   (6)

Because in (6) we have a finite lub, it is enough that for all the transfer functions t ∈ T and a ∈ C ONSTn ,
the bca αCONST (t(γCONST (a))) is computable. It turns out that the best correct approximations in C ONST of
affine assignments and linear Boolean guards are computable. Some simple cases are described, e.g., in [25,
Section P4.3], in the following we provide the algorithm of the bca’s in full generality and detail.
           n
    Let i=1 mi xi + b ∈ LExpn be a linear expression for n integer variables   Pnranging in Varn , {x1 , ..., xn },
where hmi ini=1 ∈ Zn is a vector of integer coefficients and b ∈ Z, and let J i=1 mi xi + bK : ℘(Zn ) → ℘(Z)
                                           Pn                       Pn
denote its collecting semantics, that is, J i=1 mi xi + bKX , { i=1 mi vi + b ∈ Z | ~v ∈ X}. Then, we
                                                                           △         Pn
consider the transfer functions given by a single affine assignment tja ≡ xj := i=1 mi xi + b and a linear
                    △ Pn
Boolean guard tb ≡ i=1 mi xi + b ⊲⊳ 0 with ⊲⊳ ∈ {=, 6=, <, ≤, >, ≥}, where for all Y ∈ ℘(Zn ):
                                                                      P
                         tja (Y ) , {~y[yj /vj ] ∈ Zn | ~y ∈ Y, vj ∈ J ni=1 mi xi + bK{~y}},
                                                 Pn
                         tb (Y ) , {~y ∈ Y | J i=1 mi xi + bK{~y} ⊲⊳ 0}.

These transfer functions can be easily extended to include parallel affine assignments of the shape ~x := M ~x +~b,
where M ∈ Zn×n is a n × n integer matrix and ~b ∈ Zn , which simply performs n parallel single affine
assignments, and P conjunctive (disjunctive) linear Boolean guards M ~x + ~b ⊲⊳ 0, which holds iff, for all (there
                     n
exists) j ∈ [1, n], i=1 Mji xi + bj ⊲⊳ 0 holds.
                                  j
                        Pnbca of ta and tb in C ONSTn are both computable. Let us first observe that if ~a ∈
    It turns out that the
C ONSTn r{⊥} then J i=1 mi xi + bK(γCONST (~a)) = {k} for some k ∈ Z iff for all l ∈ [1, n] either ml = 0

                                                          10
                                                                Pn
or al ∈ Z. Thus, for all a ∈ C ONSTn , the problem ∃k ∈? Z. J i=1 m    Pi x i + bK(γC ONST (a)) = {k} is decidable,
                                                                          n
and in a positive
              Pn    case the constant k is  computable. Moreover,  if J   i=1 mi xi + bK(γC ONST (~
                                                                                                  a)) 6= {k} then
necessarily J i=1 mi xi + bK(γCONST (~a)) = Z. As a consequence of these observations, we derive the following
definition: for all a ∈ C ONST n ,
                                        
                                        
                                        ⊥           if a = ⊥
                                                                 P
             αCONST (ta (γCONST (a))) = ~a[aj /k] if a = ~a, J ni=1 mi xi + bK(γCONST (~a)) = {k}
                       j
                                        
                                                                Pn
                                           ~a[aj /⊤] if a = ~a, J i=1 mi xi + bK(γCONST (~a)) = Z

which shows that αCONST (tja (γCONST (a))) is computable and, in turn, bca’s of parallel affine assignments are
computable. The proof of computability of bca’s of linear Boolean guards tb follows the same lines. We dis-
tinguish two cases: ⊲⊳ ∈ {6=, <, ≤, >, ≥}, whose transfer function is denoted by t⊲⊳  b , and ⊲⊳ ∈ {=}, i.e. affine
equalities, denoted by t=
                        b . The corresponding  algorithms are as follows: for all a ∈ C ONST n :
                                        
                                        
                                         ⊥    if a = ⊥
                                        
                                        ~a                Pn
                                               if a = ~a, J i=1 mi xi + bK(γCONST (~a)) = {k}, k ⊲⊳ 0
            αCONST (t⊲⊳
                     b (γC ONST (a))) =                    Pn
                                        
                                         ⊥    if a = ~a, J i=1 mi xi + bK(γCONST (~a)) = {k}, k 6⊲⊳ 0
                                        
                                                          Pn
                                         ~a    if a = ~a, J i=1 mi xi + bK(γCONST (~a)) = Z

  αCONST (t=
           b (γC ONST (a))) =
                   
                   
                     ⊥          if a = ⊥
                   
                                            P
                   
                                if a 6= ⊥, J ni=1 mi xi + bK(γCONST (a)) = {k}, k = 0
                   a                        Pn
                      ⊥          if a 6= ⊥, J i=1 mi xi + bK(γCONST (a)) = {k}, k 6= 0
                   
                                                                         P
                   
                    ~a[aj /k]   if a 6= ⊥, ∃j ∈ [1, n].mj 6= 0, aj = ⊤, J i6=j mi xi + bK(γCONST (a)) = {k}
                   
                   
                   a            otherwise

    Summing up, by Corollaries 3.4 and 3.5 we have shown the following result for the class CCONST of nonde-
terministic programs with (possibly parallel) affine assignments and (conjunctive or disjunctive) linear Boolean
guards.

Theorem 4.1 (Decidability and Synthesis of Inductive Invariants in C ONST ). The Monniaux problem (5)
on C ONST for programs in CCONST , r.e. sets of initial states and recursive sets of state properties is decidable.
Moreover, the algorithm AI NV of Corollary 3.5 instantiated to postP for programs P ∈ CCONST , r.e. sets of
initial states and safety properties P ∈ γ̇CONST (C ONST |QP | ) synthesizes the least inductive invariant of P in
C ONST, when this exists.

    This result could be easily extended to polynomial assignments and Boolean guards. We do not discuss the
details of these extensions since our main goal here was to illustrate on the simple example of C ONST how the
abstract inductive invariant principle can be applied to derive decidability results and synthesis algorithms for
abstract inductive invariants.

Example 4.2. Let us consider the program P represented in Fig. 1 with Σ0 = {q1 } × Z2 and the valid property
                                                                             |Q|
P ♯ = hq1 , (⊤, ⊤)i,hq2 , (⊤, 2)i,hq3 , (⊤, ⊤)i, hq4 , (⊤, ⊤)i ∈ C ONST2 representing that the variable x2 is
constantly equal to 2 at the program point q2 . It is easy to check that the algorithm AI NV of Corollary 3.5 yields

                                                        11
                                                                       q1
                                                                           x1 := 0;
                                                                           x2 := 2;
                                                                       q2
                                                                              x1 ≥ 9
                                     x1 := x1 − x2 ;    x1 := x1 + 2x2 ;       q4
                                      x2 := x2 + 1;       x2 := x2 − 1;

                                                                       q3


                               Fig. 1. A CFG representing a nondeterministic program P.


                                                                                                 |Q|
the following sequence of abstract values J k+1 = α̇CONST (postP (γ̇CONST (J k ))) ∈ C ONST2 :

                  J 0 = α̇CONST (Σ0 ) = hq1 , (⊤, ⊤)i, hq2 , (⊥, ⊥)i, hq3 , (⊥, ⊥)i, hq4 , (⊥, ⊥)i
                  J 1 = hq1 , (⊤, ⊤)i, hq2 , (0, 2)i, hq3 , (⊥, ⊥)i, hq4 , (⊥, ⊥)i
                  J 2 = hq1 , (⊤, ⊤)i, hq2 , (0, 2)i, hq3 , (4, 1)i, hq4 , (⊥, ⊥)i
                  J 3 = hq1 , (⊤, ⊤)i, hq2 , (⊤, 2)i, hq3 , (4, 1)i, hq4 , (⊥, ⊥)i
                  J 4 = hq1 , (⊤, ⊤)i, hq2 , (⊤, 2)i, hq3 , (⊤, 1)i, hq4 , (⊤, 2)i =
                                                        ˙ CONST P ♯
                      = α̇CONST (postP (γ̇CONST (J 4 )))≤

Thus, the output J 4 is the least (i.e. strongest) inductive invariant in C ONST which allows us to prove P ♯ .   ⊓
                                                                                                                  ⊔

Relationship with Completeness. It is easy to check that all the transfer functions ta of affine assignments are
pointwise complete, namely, αCONST ◦ ta = αCONST ◦ ta ◦ γCONST ◦ αCONST holds. Consequently, as recalled in
Section 3.2, from pointwise completeness one obtains fixpoint completeness, that is, for all unguarded programs
P with (parallel) affine assignments,
                       ~ 0 ∪ postP (X)))
         α̇CONST (lfp(λX.Σ          ~    = lfp(λ~a.α̇CONST (Σ0 ) ⊔˙ CONST α̇CONST (postP (γ̇CONST (~a)))).

However, fixpoint completeness is lost as soon as affine linear Boolean guards are taken into account, because,
in general, linear guards are not pointwise complete: for example, with n = 2, we have that:

                αCONST (tx1 =0 ({(1, 0), (−1, 0)})) = αCONST (∅) = ⊥ while
                 αCONST (tx1 =0 (γCONST (αCONST ({(1, 0), (−1, 0)}))) = αCONST (tx1 =0 (Z × {0}))
                                                                           = αCONST ({(0, 0)}) = h0, 0i

It is therefore worth remarking that the decidability result in C ONST for the programs in CCONST of Theorem 4.1
holds even if fixpoint completeness on C ONST for all the programs in CCONST does not hold.


4.2 Karr’s Affine Equalities Domain

Program analysis on the domain of affine equalities has been introduced in 1976 by Karr [19] who designed
some algorithms which compute for each program point the valid affine equalities between program variables.
This abstract domain, here denoted by A FF, is relatively simple, precise and is widely used in numerical program
analysis (see, e.g., [25, 36]). Müller-Olm and Seidl [30] put forward simpler and more efficient algorithms for
the transfer functions of A FF and proved that Karr’s analysis algorithm is fixpoint complete for unguarded

                                                           12
nondeterministic affine programs, while for linearly guarded nondeterministic affine programs it is undecidable
whether a given affine equality holds at a program point or not.
    Let us briefly recall the definition of the abstract domain A FF, where here the n program variables assume
rational values, that is, V = Q. The abstract invariants in A FF are finite (possibly empty) conjunctions of affine
                                                  Vk Pn
equalities between variables in Varn , namely, j=1 ( i=1 mi,j xi + bj = 0). The geometric view of A FF is
based on the affine hull of a subset X ∈ ℘(Qn ) which is defined by:
                                Pm                                               Pm
                    aff(X) , { j=0 λj ~xj ∈ Qn | m ∈ N, λj ∈ Q, ~xj ∈ X, j=0 λj = 1}.

This map aff : ℘(Qn ) → ℘(Qn ) is an upper closure on h℘(Qn ), ⊆i whose fixpoints are the affine subspaces in
Qn and therefore defines the affine equalities domain A FF , haff(℘(Qn )), ⊆i. Thus, any conjunction of affine
equalities can be represented by an affine subspace, and vice versa. haff(℘(Qn )), ⊆i is closed under arbitrary
intersections, because aff is a uco, but not under unions, i.e., aff is not an additive uco. The lub in A FF of a set
of affine subspaces X ⊆ A FF is given by ⊔AFF X , aff(∪X∈X X). A complex algorithm for computing a binary
lub A ⊔AFF A′ of two affine subspaces A, A′ ∈ A FF was given by Karr [19, Section 5.2], a simpler and more
efficient version is described by Miné [25, Section 5.2.2]. hA FF, ⊆i is a complete lattice of finite height n + 1,
because if A, A′ ∈ A FF and A ( A′ then dim(A) < dim(A′ ), where dim(∅) = −1 and dim(Qn ) = n.
                                                                                                            j
PnKarr gave already in [19, Section 4.2] an algorithm for computing the bca of an affine assignment ta ≡ xj :=
   i=1 mi xi + b, with j ∈ [1, n]. Karr’s algorithm is based on representing affine subspaces by kernels of affine
transformations (i.e., matrices) and distinguishes between invertible (such as xi := xi + k) and noninvertible
(such as xi := xj + k) affine assignments. Müller-Olm and Seidl [30] put forward a more efficient algorithm
which is based on representing affine subspaces by affine bases. It is worth remarking that [30, Lemma 2] also
observes that the bca of tja is pointwise complete, namely aff ◦tja ◦aff = aff ◦tja holds. We are not interested here
in the details and complexities of these algorithms which implement the best abstraction in A FF of the affine
assignments tja , since here we just exploit the fact that the best correct approximation aff ◦ tja : A FF → A FF is
computable. In turn, computability of parallel affine assignments ~x := M ~x + ~b easily follows.
                                                                                                    △
    Müller-Olm and Seidl [30] also show that the bca of a nondeterministic assignments tja? ≡ xj :=? is com-
putable, where for all Y ∈ ℘(Qn ), the corresponding transfer function is defined by: txj :=? (Y ) , {~y[yj /v] ∈
Qn | ~y ∈ Y, v ∈ Q}. An observation in [30, Lemma 4] states that aff(txj :=? (aff(Y )) = aff(txj :=0 (aff(Y ))⊔AFF
aff(txj :=1 (aff(Y )), thus reducing the computation of aff(txj :=? (aff(Y )) to computing the lub of the bca’s of
the transfer functions of two single affine assignments xj := 0 and xj := 1.
    As already shown by Karr [19, Section 4.1] (see also [25, Section 5.2.3] for a modern       approach), it turns out
                                                                                           △ Pn
that best correct approximations of affine equalities Boolean guards of the shape t=       ≡    i=1 mi xi + b = 0 are
                                                                                            △ P
                                                                                       b
computable. However, no algorithm for computing the bca of a generic negation t6=        b  ≡    n
                                                                                                 i=1 mi xi + b 6= 0 is
known in literature. Both Karr [19, Section 4.1] and Miné [25, Section 5.2.3] propose to soundly approximate a
negated affine equality guard t6=                                                            6=
                                 b simply by the identity transfer function, meaning that tb is replaced by the true
predicate. Karr [19, Section 4.1] mentions that “a general study of how best to handle decision nodes which are
not of the simple form t=  b is in preparation”, but this document never appeared. To the best of our knowledge,
the literature provides no algorithm for computing the bca of t6=   b in A FF , and we conjecture that, in general, it
could not be computable.
    Summing up, as a consequence of Corollaries 3.4 and 3.5 we therefore obtain the following result for the
class CAFF of nondeterministic programs with (possibly parallel) affine assignments, (possibly parallel) nonde-
terministic assignments and (conjunctive or disjunctive) positive linear equalities guards.
Theorem 4.3 (Decidability and Synthesis of Inductive Invariants in A FF). The Monniaux problem (5) on
A FF for programs in CAFF , r.e. sets of initial states and recursive sets of state properties is decidable. Moreover,
the algorithm AI NV of Corollary 3.5 instantiated to postP for programs P ∈ CAFF , r.e. sets of initial states and
safety properties P ∈ A FF synthesizes the least inductive invariant of P in A FF, when this exists.


                                                          13
                                                       q1
                                                            x1 := −2;
                                                            x2 := 1;
                                                            x3 := 1;
                                                       q2
                                    x1 := −2x2 − 2;           x1 := 2x1 + 4;
                                    x2 := x2 + x3 ;           x2 := −x1 − 2x3 ;
                                                       q3

                                                         x1 + 2x3 = 0

                                                       q4


                                         Fig. 2. A nondeterministic program R.


Example 4.4. Let us consider the nondeterministic program R in Fig. 2 with Σ0 = {q1 } × Q3 and the property
P ♯ = hq1 , ⊤i, hq2 , ⊤i, hq3 , ⊤i, hq4 , x1 + x2 + 1 = 0i ∈ A FF|Q| . The algorithm AI NV of Corollary 3.5 yields
the following sequence of abstract values I j ∈ A FF|Q| :

            I 0 = α̇AFF (Σ0 ) = hq1 , ⊤i, hq2 , ⊥i, hq3 , ⊥i, hq4 , ⊥i
            I 1 = hq1 , ⊤i, hq2 , x1 + 2 = 0 ∧ x2 − 1 = 0 ∧ x3 − 1 = 0i, hq3 , ⊥i, hq4 , ⊥i
            I 2 = hq1 , ⊤i, hq2 , x1 + 2 = 0 ∧ x2 − 1 = 0 ∧ x3 − 1 = 0i,
                             hq3 , x1 + 2x2 = 0 ∧ x3 = 1i, hq4 , ⊥i
             3
            I = hq1 , ⊤i, hq2 , x1 + 2x2 = 0 ∧ x3 = 1i, hq3 , x1 + 2x2 = 0 ∧ x3 = 1i,
                                                                                               ˙ AFF P ♯
                             hq4 , x1 + x2 + 1 = 0 ∧ x3 = 1, ⊥i = α̇AFF (postR (γ̇AFF (I 3 ))) ≤
The output I 3 is the analysis of R with the bca’s of its transfer functions in A FF, i.e., it is the least inductive
invariant in A FF which allows us to prove that P ♯ holds.                                                         ⊓
                                                                                                                   ⊔

Relationship with Completeness. Müller-Olm and Seidl [30] implicitly show that the transfer functions of
affine assignments ta and of nondeterministic assignments txj :=? are pointwise complete. In fact, [30, Lemma 2]
shows that for all X ∈ ℘(Qn ), ta (aff(X)) = aff(ta (X)), from which we easily obtain:
                 aff(ta (X)) = aff(aff(ta (X))) = aff(ta (aff(X)))
             aff(txj :=? (X)) = aff(∪z∈Q txj :=z (X)) = aff(∪z∈Q aff(txj :=z (X))) =
               = aff(∪z∈Q aff(txj :=z (aff(X))) = aff(∪z∈Q txj :=z (aff(X)) = aff(txj :=? (aff(X)))
Thus, since pointwise completeness entails fixpoint completeness, similarly to Section 4.1, for all unguarded
programs P with affine and nondeterministic assignments, α̇AFF (lfp(λX.Σ   ~ 0 ∪postP (X)))
                                                                                          ~    = lfp(λ~a.α̇AFF (Σ0 )⊔˙ AFF
α̇AFF (postP (γ̇AFF (~a)))) holds. Here, fixpoint completeness is lost as soon as affine equality guards are included
(these programs still belong to CAFF ), because they are not pointwise complete, e.g.:
              aff(tx1 =0 ({(1, 0), (−1, 0)})) = aff(∅) = ∅ while
              aff(tx1 =0 (aff({(1, 0), (−1, 0)}))) = aff(tx1 =0 (x2 = 0)) = aff({(0, 0)}) = {(0, 0)}
Moreover, a result in [30, Section 7] proves that once affine equality guards are added to nondeterministic affine
programs it becomes undecidable whether a given affine equality holds in some program point or not. This
undecidability does not prevent the decidability result of Theorem 4.3, since these two decision problems are
orthogonal.

                                                            14
5 Co-Inductive Synthesis of Abstract Inductive Invariants
In the following we design a synthesis algorithm which, by generalizing a recent algorithm by Padon et al. [32],
outputs the most abstract inductive invariant in an abstract domain, when this exists. This algorithm is obtained
by dualizing the procedure AI NV in Corollary 3.5 to a co-inductive greatest fixpoint computation and will
require that the abstract domain is equipped with a suitable well-quasiorder relation. Let us recall that a qoset
D≤ is a well-quasiordered set (wqoset), and ≤ is called well-quasiorder (wqo), when for every countably infinite
sequence of elements {xi }i∈N in D there exist i, j ∈ N such that i < j and xi ≤ xj . Equivalently, D is a wqoset
iff D is DCC (also called well-founded) and D has no infinite antichain.
    Let T = hΣ, τ i be a transition system whose successor transformer is post, so that lfp(λX.Σ0 ∪post(X)) ∈
℘(Σ) are the reachable states of T from some set of initial states Σ0 ∈ ℘(Σ). [32] considers abstract invariants
ranging in a set (of semantics of logical formulae) L ⊆ ℘(Σ) and assumes (in [32, Theorem 4.2]) that hL, ⊆i is
closed under finite intersections (i.e., logical conjunctions). Accordingly to Assumption 3.1, we ask that hL, ⊆i
satisfies the requirement of being an abstract domain of the concrete domain h℘(Σ), ⊆i, which corresponds
to ask that hL, ⊆i is closed under arbitrary, rather than finite, intersections. Thus, L is the image of an upper
closure µ̌L ∈ uco(℘(Σ)⊆ ) defined by: µ̌L (X) , ∩{φ ∈ L | X ⊆ φ}.
    The three key definitions and related assumptions of the synthesis algorithm defined in [32, Theorem 4.2]
concern a quasi-order ⊑L ⊆ Σ × Σ between states, a function Av L : Σ → ℘(Σ) called Avoid, and an abstract
transition relation τ L ⊆ Σ × Σ:
                       △
         (1) s ⊑L s′ ⇔ ∀φ ∈ L.s′ ∈ φ ⇒ s ∈ φ                   Assumption (A1 ): hΣ, ⊑L i is a wqoset
         (2) Av L (s) , ∪{φ ∈ L | φ ⊆ ¬{s}}                    Assumption (A2 ): ∀s ∈ Σ. Av L (s) ∈ L
                           △
         (3) (s, s′ ) ∈ τ L ⇔ (s, s′ ) ∈ τ ∨ s′ ⊑L s           Abstract Transition System T L , hΣ, τ L i

   Correspondingly, we define the down-closure δL : ℘(Σ) → ℘(Σ) of ⊑L , we generalize Av L : ℘(Σ) →
℘(Σ) to sets of states and we define the successor transformer postL : ℘(Σ) → ℘(Σ) of T L as follows:

              (1) δL (X) , {s ∈ Σ | ∃s′ ∈ X.s ⊑L s′ }                   Down-closure of the qo ⊑L
              (2) Av L (X) , ∪{φ ∈ L | φ ⊆ ¬X}                          Av L for any set X of states
                       L
              (3) post (X) , post(X) ∪ δL (X)                           Successor transformer of T L

Lemma 5.1. The following properties hold:
(a) s ⊑L s′ iff µ̌L ({s}) ⊆ µ̌L ({s′ }).
(b) (A1 ) holds iff hL, ⊆i is a well-quasi order.
(c) (A2 ) holds iff L is closed under arbitrary unions.
(d) If (A2 ) holds then δL = µ̌L and both are additive ucos (and δL (φ) = φ ⇔ φ ∈ L).
(e) For all Σ0 ∈ ℘(Σ), lfp(λX.Σ0 ∪ postL (X)) = lfp(λX.µ̌L (Σ0 ∪ post(X))).

Proof. (a) If s ⊑L s′ and t ∈ µ̌L ({s}) then t ∈ µ̌L ({s′ }) = ∩{φ ∈ L | s′ ∈ φ}: if φ ∈ L and s′ ∈ φ then
s ∈ φ, so that, since t ∈ µ̌L ({s}), t ∈ φ. Conversely, if µ̌L ({s}) ⊆ µ̌L ({s′ }), φ ∈ L and s′ ∈ φ, then, since
s ∈ µ̌L ({s′ }), s ∈ φ.
(b) By (a), we equivalently prove that h{µ̌L ({s}) | s ∈ Σ}, ⊆i is a wqo iff hL, ⊆i is a wqo.
(⇒): [32, Lemma 4.6] proves hL, ⊆i is well-founded, we additionally show that it does not contain infinite
antichains. By contradiction, assume that {φi }i∈N is an infinite antichain in hL, ⊆i. Thus, for all i 6= j, φi 6⊆ φj
and φj 6⊆ φi , so that there exist si,j ∈ φi r φj and sj,i ∈ φj r φi . From sj,i ∈ φj we obtain that µ̌L ({sj,i }) ⊆
µ̌L (φj ) = φj . From si,j 6∈ φj , we obtain that si,j ∈ µ̌L ({si,j }) 6⊆ φj,i . It turns out that µ̌L ({si,j }) 6⊆
µ̌L ({sj,i }), otherwise from si,j ∈ µ̌L ({si,j }) ⊆ µ̌L ({sj,i }) ⊆ φj we would obtain the contradiction si,j ∈ φj .

                                                         15
Dually, µ̌L ({sj,i }) 6⊆ µ̌L ({si,j }) holds. Thus, for any i ∈ N, {µ̌L ({si,j }) | j ∈ N, j 6= i} is an infinite antichain
in h{µ̌L ({s}) | s ∈ Σ}, ⊆i, which is a contradiction.
(⇐): h{µ̌L ({s}) | s ∈ Σ}, ⊆i is trivially a wqo because {µ̌L ({s}) | s ∈ Σ} ⊆ L and L is a wqo.
(c) Assume that for all s ∈ Σ, Av L (s) ∈ L. Let us show that for all S ∈ ℘(Σ), ∩s∈S Av L (s) = Av L (S).
(⊇): Let t ∈ φ for some φ ∈ L such that φ ⊆ ¬S. Then, for all s ∈ S, φ ⊆ Av L (s), so that t ∈ ∩s∈S Av L (s).
(⊆): Let t ∈ ∩s∈S Av L (s). For all s ∈ S, there exists φs ∈ L such that φs ⊆ ¬{s} and t ∈ φs . Thus,
∩s∈S φs ∈ L and t ∈ ∩s∈S φs ⊆ ¬S, meaning that t ∈ Av L (S).
Thus, since L is assumed to be closed under arbitrary intersections we obtain that Av L (S) = ∩s∈S Av L (s) ∈ L.
Consider now Φ ⊆ L. Then, Av L (¬(∪Φ)) = ∪{φ ∈ L | φ ⊆ ¬¬(∪Φ)} = ∪{φ ∈ L | φ ⊆ ∪Φ} = ∪Φ, so that
∪Φ ∈ L.
Conversely, if L is closed under arbitrary unions then Av L (s) = ∪{φ ∈ L | φ ⊆ ¬{s}} ∈ L.
(d) Since ⊑L is a quasi-order relation, its down-closure δL is an upper closure on h℘(Σ), ⊆i. By (a), δL (X) =
{s ∈ Σ | ∃s′ ∈ X.s ⊑L s′ } = {s ∈ Σ | ∃s′ ∈ X.µ̌L ({s}) ⊆ µ̌L ({s′ })} = {s ∈ Σ | ∃s′ ∈ X.s ∈
µ̌L ({s′ })} = ∪s∈X µ̌L ({s}). By (c), since L is closed under arbitrary unions, the upper closure µ̌L is additive,
so that ∪s∈X µ̌L ({s}) = µ̌L (∪s∈X {s}) = µ̌L (X), consequently δL (X) = µ̌L (X). In particular, δL (φ) = φ ⇔
µ̌L (φ) = φ ⇔ φ ∈ L.
(e) By Lemma 5.1 (d), lfp(λX. post(X) ∪ δL (X) ∪ Σ0 ) = lfp(λX. post(X) ∪ µ̌L (X) ∪ Σ0 ). It turns out that

                                       Σ0 ∪ post(X) ∪ δL (X) ⊆ X ⇔             [by Lemma 5.1 (d)]
                                       Σ0 ∪ post(X) ∪ µ̌L (X) ⊆ X ⇔            [by set theory]
                          Σ0 ⊆ X ∧ post(X) ⊆ X ∧ µ̌L (X) ⊆ X ⇔                 [as µ̌L is a uco]
                          Σ0 ⊆ X ∧ post(X) ⊆ X ∧ µ̌L (X) = X ⇔                 [as µ̌L (X) = X]
                     Σ0 ⊆ X ∧ post(µ̌L (X)) ⊆ X ∧ µ̌L (X) = X ⇔                [by set theory]
                              Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X) ⊆ X

Thus, by Knaster-Tarski theorem, lfp(λX.Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X)) = lfp(λX.Σ0 ∪ post(X) ∪ δL (X)).
We also have that:

                            Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X) ⊆ X ⇔            [by the equivalences above]
                 Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X) ⊆ X = µ̌L (X) ⇔             [by set theory]
                          Σ0 ∪ post(µ̌L (X)) ⊆ X = µ̌L (X) ⇔              [as µ̌L (X) = X]
                                 Σ0 ∪ post(X) ⊆ X = µ̌L (X) ⇔             [as µ̌L is a uco]
                            µ̌L (Σ0 ∪ post(X)) ⊆ X = µ̌L (X) ⇔            [by set theory]
                                        µ̌L (Σ0 ∪ post(X)) ⊆ X

Thus, by Knaster-Tarski theorem, lfp(µ̌L (Σ0 ∪ post(X))) ⊆ lfp(λX.Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X)) follows.
Moreover, if F , lfp(µ̌L (Σ0 ∪ post(X))), so that F = µ̌L (F ) = Σ0 ∪ post(F ), then Σ0 ∪ post(µ̌L (F )) ∪
µ̌L (F ) = Σ0 ∪post(F )∪µ̌L (F ) = F , and this implies that lfp(λX.Σ0 ∪post(µ̌L (X))∪µ̌L (X)) ⊆ lfp(µ̌L (Σ0 ∪
post(X))). Therefore, lfp(λX.Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X)) = lfp(µ̌L (Σ0 ∪ post(X))).                        ⊓
                                                                                                             ⊔
    In particular, Lemma 5.1 (e) states that the set of reachable states in the abstract transition system T L
coincides with the set of reachable states of the abstract transition system T µ̌L , hΣ, µ̌L ◦ postT i obtained by
considering the best correct approximation of postT in the abstract domain µ̌L . As a direct consequence of the
abstract inductive invariant principle Lemma 3.2 (a), we obtain the following characterization of the abstract
inductive invariants ranging in L of the transition system T which relies on the reachable states of its best
abstraction T µ̌L in the domain µ̌L .
Corollary 5.2. Let Σ0 , P ∈ ℘(Σ). Then, ∃φ ∈ L.Σ0 ⊆ φ ∧ post(φ) ⊆ φ ∧ φ ⊆ P iff Reach[T µ̌L , Σ0 ] ⊆ P .

                                                            16
Proof. It turns out that

                             lfp(λX.µ̌L (Σ0 ∪ post(X))) ⊆ P ⇔         [by Lemma 3.2 (a) for ucos]
                ∃φ ∈ µ̌L (℘(Σ)).Σ0 ∪ post(φ) ⊆ φ ∧ φ ⊆ P ⇔            [as µ̌L (℘(Σ)) = L]
                   ∃φ ∈ L.Σ0 ⊆ φ ∧ post(φ) ⊆ φ ∧ φ ⊆ P                                                             ⊓
                                                                                                                   ⊔


5.1 Co-Inductive Invariants

Following [32], in the following we make assumption (A2 ), that is, by Lemma 5.1 (c), we assume that L ⊆ ℘(Σ)
is closed under arbitrary unions. This means that µ̌L is an additive uco on ℘(Σ)⊆ , i.e., in abstract interpretation
terminology, µ̌L is a disjunctive abstract domain whose abstract lub does not lose precision (see, e.g., [25, Sec-
tion 6.3]). Furthermore, we also have that L is the image of a co-additive (i.e., preserving arbitrary intersections)
lower closure µ̂L : ℘(Σ) → ℘(Σ) defined by µ̂L (X) , ∪{φ ∈ L | φ ⊆ X}. It turns out that the uco µ̌L is ad-
joint to the lco µ̂L (this is called abstract adjoinedness in [2, Section 3.5]), namely, µ̌L (X) ⊆ Y ⇔ X ⊆ µ̂L (Y ).
In fact, if µ̌L (X) ⊆ Y then, by applying µ̂L , X ⊆ µ̌L (X) = µ̂L (µ̌L (X)) ⊆ µ̂L (Y ); the converse is dual.
     As observed in [2, Theorem 4], the inductive invariant principle (2) can be dualized when f admits right-
adjoint fe : C → C (this happens iff f is additive): in this case,

                                 lfp(λx.c ∨ f (x)) ≤ c′ ⇔ c ≤ gfp(λx.c′ ∧ fe(x))                                 (7)

holds and one obtains a co-inductive invariant principle:

                           c ≤ gfp(λx.fe(x) ∧ c′ ) ⇔ ∃j ∈ C. c ≤ j ∧ j ≤ fe(j) ∧ j ≤ c′                          (8)

One such j ∈ C is therefore called a co-inductive invariant of f for hc, c′ i.
    The co-inductive invariant proof method (8) can be applied to safety verification of any transition system
T because post is additive and therefore it always admits right adjoint pre   f (cf. Section 2). Hence, we obtain
that lfp(λX.Σ0 ∪ post(X)) ⊆ P iff Σ0 ⊆ gfp(λX. pre(X)   f        ∩ P ) iff there exists a co-inductive invariant for
f for hΣ0 , P i. By (2) and (8), it turns out that I is an inductive invariant of post for hΣ0 , P i iff I is a co-
pre
                        f for hΣ0 , P i. Also, while lfp(λX.Σ0 ∪ post(X)) is the least, i.e. logically strongest,
inductive invariant of pre
                                            f
inductive invariant, we have that gfp(λX. pre(X)   ∩ P ) is the greatest, i.e. logically weakest, inductive invariant
[2, Theorem 6].
    We show how the co-inductive invariant principle (8) applied to the best abstract transition system T µ̌L =
(Σ, µ̌L ◦ postT ) provides exactly the synthesis algorithm by Padon et al. [32, Algorithm 1]. In order to do this,
we first observe the following alternative characterization of the reachable states of T µ̌L .

Lemma 5.3. lfp(λX.Σ0 ∪ µ̌L (post(X))) = lfp(λX.Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X)).

Proof. The proof of Lemma 5.1 (e) shows that lfp(λX.Σ0 ∪post(µ̌L (X))∪ µ̌L (X)) = lfp(µ̌L (Σ0 ∪post(X))).
Moreover, since µ̌L is additive and µ̌L (Σ0 ) = Σ0 , we also have that µ̌L (Σ0 ∪ post(X)) = µ̌L (Σ0 ) ∪
µ̌L (post(X)) = Σ0 ∪ µ̌L (post(X)), and this allows us to conclude.                                    ⊓
                                                                                                       ⊔

    Consequently, lfp(λX.Σ0 ∪ µ̌L (post(X))) ⊆ P ⇔ lfp(λX.Σ0 ∪ post(µ̌L (X)) ∪ µ̌L (X)) ⊆ P holds. Since
λX. post(µ̌L (X)) ∪ µ̌L (X) is additive, we can apply the co-inductive invariant principle (8) by considering its
adjoint function, which is as follows:

                      post(µ̌L (X)) ∪ µ̌L (X) ⊆ Y ⇔ post(µ̌L (X)) ⊆ Y ∧ µ̌L (X) ⊆ Y ⇔
                            f )) ∧ X ⊆ µ̂L (Y ) ⇔ X ⊆ µ̂L (pre(Y
                   X ⊆ µ̂L (pre(Y                             f )) ∩ µ̂L (Y )


                                                         17
Thus, by Lemma 5.3 and (7), we obtain:
                                                                             f
             lfp(λX.µ̌L (Σ0 ) ∪ µ̌L (post(X))) ⊆ P ⇔ µ̌L (Σ0 ) ⊆ gfp(λX.µ̂L (pre(X) ∩ X ∩ P ))
                                                                       f
                                                   ⇔ Σ0 ⊆ gfp(λX.µ̂L (pre(X)    ∩ X ∩ P ))
and, in turn, by the abstract inductive invariant principle (Lemma 3.2 (a) for ucos) applied to µ̌L ◦ (λX.Σ0 ∪
post(X)) = λX.µ̌L (Σ0 ) ∪ µ̌L (post(X)) we get:
                                                                     f
              ∃φ ∈ L.Σ0 ⊆ φ ∧ post(φ) ⊆ φ ∧ φ ⊆ P ⇔ Σ0 ⊆ gfp(λX.µ̂L (pre(X) ∩ X ∩ P )).
This leads us to use the algorithm introduced by Cousot [2, Algorithm 2] which synthesizes an inductive invari-
ant by using a co-inductive method that applies Knaster-Tarski theorem to compute the iterates of the greatest
                    f
fixpoint of λX.µ̂L (pre(X)   ∩X ∩ P ) as long as the current iterate I1 contains the initial states in Σ0 :

 Algorithm 1: Co-inductive backward abstract inductive invariant synthesis.
   I1 := Σ;
   while Σ0 ⊆ I1 do // Loop invariant: I1 ∈ L
                     f 1 ) ∩ I1 ∩ P )) then return I1 is an inductive invariant in L;
       if (I1 = µ̂L (pre(I
                        f 1 ) ∩ I1 ∩ P );
       I1 := I1 ∩ µ̂L (pre(I
   return no inductive invariant in L;

       f is computable and, by Lemma 5.1, hµ̂L , ⊆i = hL, ⊆i is a wqo, we immediately obtain that Algo-
Since, pre
rithm 1 is correct and terminating. Furthermore, if Algorithm 1 outputs an inductive invariant I1 proving the
property P then I1 is the greatest inductive invariant proving P . It turns out that Algorithm 1 exactly coincides
with the synthesis algorithm by Padon et al. [32], which is replicated below as Algorithm 2.

 Algorithm 2: Inductive invariant algorithm by [32].
   I2 := Σ;
   while I2 is not an inductive invariant do // Loop invariant: I2 ∈ L
       if Σ0 6⊆ I2 then return no inductive invariant in L;
       choose s ∈ Σ as a counterexample to inductiveness of I2 ;
       I2 := I2 ∩ Av L (s);
   return I2 is an inductive invariant in L;

Lemma 5.4. Let I ∈ L and Σ0 ⊆ I.
                                                                 f
(a) there exists a counterexample to inductiveness of I iff I 6⊆ pre(I)                   f
                                                                        ∩ P iff I 6= µ̂L (pre(I) ∩ I ∩ P ).
                                                                  f
(b) If s ∈ Σ is a counterexample to inductiveness of I then µ̂L (pre(I)  ∩ I ∩ P ) ⊆ Av L (s).
Proof. (a) Under the assumption that Σ0 ⊆ I, s is a counterexample to inductiveness of I iff (s ∈ I ∧post(s) 6⊆
                                                     f
I) ∨ s ∈ I ∩ ¬P . Observe that post(s) 6⊆ I iff s 6∈ pre(I),                                              f
                                                             so that ∃s ∈ Σ.s ∈ I ∧ post(s) 6⊆ I iff I 6⊆ pre(I).
                                                               f
Hence, ∃s ∈ Σ.(s ∈ I ∧ post(s) 6⊆ I) ∨ s ∈ I ∩ ¬P iff I 6⊆ pre(I)     ∩ P . Also:
                                           f
                                  I = µ̂L (pre(I) ∩ I ∩ P) ⇔             [as I ∈ L]
                                           f
                        I = µ̂L (I) = µ̂L (pre(I) ∩ I ∩ P) ⇔                 f
                                                                         [as pre(I) ∩ I ∩ P ⊆ I]
                                           f
                        I = µ̂L (I) ⊆ µ̂L (pre(I) ∩ I ∩ P ) ⇔            [as µ̂L is a lco]
                                            f
                            I = µ̂L (I) ⊆ pre(I)   ∩I ∩P ⇔
                                                 f
                                             I ⊆ pre(I) ∩P
(b) The proof of point (a) shows that if s ∈ Σ is a counterexample to inductiveness of I then s ∈ I and
     f
s 6∈ pre(I)              f
             ∩ P . Then, pre(I)                                                    f
                                ∩ P ⊆ ¬{s}, so that, by monotonicity of µ̂L , µ̂L (pre(I) ∩ P ) ⊆ µ̂L (¬{s}) and,
              f
in turn, µ̂L (pre(I) ∩ I ∩ P ) ⊆ µ̂L (¬{s}) = Av L (s).                                                        ⊓
                                                                                                               ⊔

                                                           18
Theorem 5.5. Algorithm 1 = Algorithm 2.
Proof. Consider the following variation of Algorithm 1:

  Algorithm 3: A modification of Algorithm 1.
    I4 := Σ;
    while Σ0 ⊆ I4 do // Invariant: I4 ∈ L
                  f 4 ) ∩ P ) = ∅) then return I4 is an inductive invariant in L;
        if (I4 r (pre(I
                           f 4 ) ∩ P );
        choose s ∈ I4 r (pre(I
        I4 := I4 ∩ µ̂L ({s});
    return no inductive invariant in L;

Algorithm 1 returns I1 ∈ L iff I1 = gfp(λX.µ̂L (pre(X)  f      ∩ X ∩ P )). In this case, by Lemma 5.4 (a), since
Σ0 ⊆ I1 holds, I1 is an (actually, the greatest) inductive invariant in L. Otherwise, Algorithm 1 returns “no
inductive invariant in L”. By Lemma 5.4 (a), Algorithm 3 returns I4 ∈ L iff I4 ⊆ pre(I       f 4 ) ∩ P iff I4 =
     f 4 ) ∩ I4 ∩ P ), otherwise it returns “no inductive invariant in L”. Algorithm 2 returns I2 ∈ L iff I2 is an
µ̂L (pre(I
inductive invariant, otherwise it returns “no inductive invariant in L”. Let Ikn be the current candidate invariant
of Algorithm k ∈ {1, 2, 4} at its n-th iteration and Ik be the output invariant of Algorithm k. By Lemma 5.4 (b),
I1n ⊆ I4n = I2n , so that I1 ⊆ I4 = I2 . Since Ik are fixpoints of λX.µ̂L (pre(X)
                                                                           f       ∩ X ∩ P ) and I1 is the greatest
fixpoint, it turns out that I1 = I4 = I2 .                                                                       ⊓
                                                                                                                 ⊔
    This shows that Algorithm 2 in [32] for a disjunctive GC-based abstract domain A amounts to a backward
                                   f using the best correct approximations in A of the transfer functions, as
static analysis (i.e., propagating pre)
long as the ordering of A guarantees its termination, e.g., because A is well-founded.
Example 5.6. It turns out that C ONST, as defined in Section 4.1, is a disjunctive abstract domain with finite
height and its bca’s of affine assignments and linear Boolean guards are computable. Thus, C ONST satisfies the
hypotheses guaranteeing the correctness and termination of Algorithm 1 (and 2). Let us apply Algorithm 1 to
the program P of Example 4.2 in Fig. 1, still with Σ0 = {q1 } × Z2 such that αCONST (Σ0 ) = hq1 , (⊤, ⊤)i,
hq2 , (⊥, ⊥)i, hq3 , (⊥, ⊥)i, hq4 , (⊥, ⊥)i and for the valid property P ♯ = hq1 , (⊤, ⊤)i, hq2 , (⊤, 2)i,hq3 , (⊤, ⊤)i,
                           |Q|
hq4 , (⊤, ⊤)i ∈ C ONST2 . It is easy to check that Algorithm 1 computes the following sequence I k+1 =
                                                               |Q|
        f P (γCONST (I k ))) ⊓CONST I k ⊓CONST P ♯ in C ONST 2 :
αCONST (pre
                   I 0 = α̇CONST (Σ) = hq1 , (⊤, ⊤)i, hq2 , (⊤, ⊤)i, hq3 , (⊤, ⊤)i, hq4 , (⊤, ⊤)i
                   I 1 = hq1 , (⊤, ⊤)i, hq2 , (⊤, 2)i, hq3 , (⊤, ⊤)i, hq4 , (⊤, ⊤)i
                   I 2 = hq1 , (⊤, ⊤)i, hq2 , (⊤, 2)i, hq3 , (⊤, 1)i, hq4 , (⊤, ⊤)i =
                                                        ˙ CONST α̇CONST (Σ0 )
                                  f P (γ̇CONST (I 3 ))) ≥
                       = α̇CONST (pre
The computation of I 2 derives from pre({q f 2 } × Z × {2} ∪ {q1 , q3 , q4 } × Z2 ) = {q1 , q2 , q4 } × Z2 ∪ {q3 } ×
Z × {1}, so γCONST (I ) ∩ γCONST (αCONST ({q1 , q2 , q4 } × Z2 ∪ {q3 } × Z × {1})) = {q1 , q4 } × Z2 ∪ {q2 } ×
                         1

Z × {2} ∪ {q3 } × Z × {1}. Thus, I 2 is returned by Alg. 1 and is the greatest inductive invariant in C ONST
which proves P ♯ . In particular, the abstract inductive invariant I 2 is strictly weaker than the inductive invariant
 hq1 , (⊤, ⊤)i, hq2 , (⊤, 2)i, hq3 , (⊤, 1)i, hq4 , (⊤, 2)i computed in Example 4.2 for proving the same property
P ♯ by the algorithm AI NV of Corollary 3.5.                                                                        ⊓
                                                                                                                    ⊔

5.2 Backward and Forward Algorithms
                                                          f for termination it requires that the abstract domain
We have that Algorithm 1 is backward because it applies pre,
hµ̌L , ⊆i is DCC and turns out to be the dual of the forward algorithm AI NV provided by Corollary 3.5 for post

                                                          19
and requiring that hµ̌L , ⊆i is ACC. This latter assumption would be satisfied by dualizing the wqo ⊑L , i.e., by
requiring that hΣ, ⊒L i is a wqo.
    A different gfp-based forward algorithm based can be designed by observing (as in [7, Section 3]) that
lfp(λX.Σ0 ∪post(X)) ⊆ P iff lfp(λX.¬P ∪pre(X)) ⊆ ¬Σ0 . Here, the dualization provided by the equivalence
(7) yields:

                                                                 g
              lfp(λX.¬P ∪ µ̌L (pre(X))) ⊆ ¬Σ0 ⇔ ¬P ⊆ gfp(λX.µ̂L (post(X) ∩ X ∩ ¬Σ0 )).

                                                                                                g and is
This induces the following co-inductive forward algorithm which relies on the state transformer post
terminating when hµ̌L , ⊆i is assumed to be DCC:

 Algorithm 4: Co-inductive forward abstract inductive invariant synthesis.
   I := Σ;
   while ¬P ⊆ I do // Loop invariant: I ∈ L
                    g
       if (I = µ̂L (post(I) ∩ I ∩ ¬Σ0 )) then return I is an inductive invariant in L;
                      g
       I := I ∩ µ̂L (post(I) ∩ I ∩ ¬Σ0 );
   return no inductive invariant in L;

   Furthermore, by dualizing the technique and the algorithm described in [7, Section 4.3] for post and pre,
one could also design a more efficient combined forward/backward synthesis algorithm which simultaneously
                                         g steps.
                    f and forward, by post,
make backward, by pre,


6 Future Work

As hinted by Monniaux [28], results of undecidability to the question (3) for some abstract domain A display
a foundational trait since they “vindicate” (often years of intense) research on precise and efficient algorithms
for approximate static program analysis on A. To the best of our knowledge, few undecidability results are
available: an undecidability result by Monniaux [28, Theorem 1] for the abstraction of convex polyhedra [8]
and by Fijalkow et al. [13, Theorem 1] for semilinear sets, i.e. finite unions of convex polyhedra. However,
convex polyhedra and semilinear sets cannot be defined by a Galois connection and therefore do not satisfy
our Assumption 3.1. As an interesting and stimulating future work we plan to investigate whether the abstract
inductive invariant principle could be exploited to provide a reduction of the undecidability of the question (3)
for abstract domains which satisfy Assumption 3.1 and, in view of the characterization of fixpoint completeness
given in Section 3.3, for transfer functions which are not fixpoint complete.
    We also plan to study whether complete abstractions can play a role in the decidability result by Hrushovski
et al. [17] on the computation of the strongest polynomial invariant of an affine program. This hard result in [17]
relies on the Zariski closure, which is continuous for affine functions. The observation here is that the Zariski
closure is pointwise complete for the transfer functions of affine programs, therefore fixpoint completeness for
affine programs holds, and one could investigate whether the algorithm given in [17] may be viewed as a least
fixpoint computation of a best correct approximation on the Zariski abstraction.


References

 1. S. Chatterjee and M. Kishinevsky. Automatic generation of inductive invariants from high-level microarchitectural
    models of communication fabrics. In Proc. 22nd International Conference on Computer Aided Verification (CAV’10),
    volume 6174 of Lecture Notes in Computer Science, pages 321–338. Springer, 2010.


                                                         20
 2. P. Cousot. Partial completeness of abstract fixpoint checking. In Proceedings of the 4th International Symposium on
    Abstraction, Reformulation, and Approximation (SARA’02), volume 1864 of Lecture Notes in Computer Science, pages
    1–25. Springer-Verlag, 2000.
 3. P. Cousot. On fixpoint/iteration/variant induction principles for proving total correctness of programs with denotational
    semantics. In Proc. 29th International Symposium on Logic-based Program Synthesis and Transformation (LOP-
    STR’19), volume to appear of Lecture Notes in Computer Science. Springer, 2019.
 4. P. Cousot and R. Cousot. Abstract interpretation: a unified lattice model for static analysis of programs by construc-
    tion or approximation of fixpoints. In Proceedings of the 4th ACM SIGACT-SIGPLAN Symposium on Principles of
    Programming Languages (POPL’77), pages 238–252. ACM Press, 1977.
 5. P. Cousot and R. Cousot. Systematic design of program analysis frameworks. In Proceedings of the 6th ACM SIGACT-
    SIGPLAN Symposium on Principles of Programming Languages (POPL’79), pages 269–282, New York, NY, USA,
    1979. ACM.
 6. P. Cousot and R. Cousot. Induction principles for proving invariance properties of programs. In D. Néel, editor, Tools
    & Notions for Program Construction: an Advanced Course, pages 75–119. Cambridge University Press, Cambridge,
    UK, Aug. 1982.
 7. P. Cousot and R. Cousot. Refining model checking by abstract interpretation. Automated Software Engineering,
    6(1):69–95, 1999.
 8. P. Cousot and N. Halbwachs. Automatic discovery of linear restraints among variables of a program. In Proceedings
    of the 5th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL’78), pages 84–96.
    ACM, 1978.
 9. I. Dillig, T. Dillig, B. Li, and K. L. McMillan. Inductive invariant generation via abductive inference. In Proceed-
    ings of the 2013 ACM SIGPLAN International Conference on Object Oriented Programming Systems Languages &
    Applications, (OOPSLA’13), pages 443–456. ACM, 2013.
10. Y. M. Y. Feldman, N. Immerman, M. Sagiv, and S. Shoham. Complexity and information in invariant inference. Proc.
    ACM Program. Lang., 4(POPL), 2019.
11. Y. M. Y. Feldman, O. Padon, N. Immerman, M. Sagiv, and S. Shoham. Bounded Quantifier Instantiation for Checking
    Inductive Invariants. Logical Methods in Computer Science, Volume 15, Issue 3, 2019.
12. Y. M. Y. Feldman, J. R. Wilcox, S. Shoham, and M. Sagiv. Inferring inductive invariants from phase structures. In Proc.
    31st International Conference on Computer Aided Verification (CAV’19), volume 11562 of Lecture Notes in Computer
    Science, pages 405–425. Springer, 2019.
13. N. Fijalkow, E. Lefaucheux, P. Ohlmann, J. Ouaknine, A. Pouly, and J. Worrell. On the Monniaux problem in abstract
    interpretation. In Proc. 26th International Static Analysis Symposium (SAS’19), volume 11822 of Lecture Notes in
    Computer Science, pages 162–180. Springer, 2019.
14. R. W. Floyd. Assigning meanings to programs. Proceedings of Symposium on Applied Mathematics, 19:19–32, 1967.
15. R. Giacobazzi, F. Ranzato, and F. Scozzari. Making abstract interpretations complete. J. ACM, 47(2):361–416, 2000.
16. M. Hecht. Flow Analysis of Computer Programs. North Holland, 1977.
17. E. Hrushovski, J. Ouaknine, A. Pouly, and J. Worrell. Polynomial invariants for affine programs. In Proceedings of the
    33rd Annual ACM/IEEE Symposium on Logic in Computer Science, (LICS’18), pages 530–539. ACM, 2018.
18. A. Ivrii, A. Gurfinkel, and A. Belov. Small inductive safe invariants. In Proc. Formal Methods in Computer-Aided
    Design (FMCAD’14), pages 115–122. IEEE, 2014.
19. M. Karr. Affine relationships among variables of a program. Acta Inf., 6:133–151, 1976.
20. G. A. Kildall. A unified approach to global program optimization. In Proceedings of the ACM Symposium on Principles
    of Programming Languages (POPL’73), pages 194–206. ACM, 1973.
21. Z. Kincaid, J. Cyphert, J. Breck, and T. Reps. Non-linear reasoning for invariant synthesis. Proc. ACM Program. Lang.,
    2(POPL), 2018.
22. K. R. M. Leino. Dafny: An automatic program verifier for functional correctness. In Proc. International Conference
    on Logic for Programming, Artificial Intelligence, and Reasoning (LPAR-16), Revised Selected Papers, volume 6355 of
    Lecture Notes in Computer Science, pages 348–370. Springer, 2010.
23. H. Ma, A. Goel, J. Jeannin, M. Kapritsos, B. Kasikci, and K. A. Sakallah. Towards automatic inference of inductive
    invariants. In Proceedings of the Workshop on Hot Topics in Operating Systems, (HotOS’19), pages 30–36. ACM, 2019.
24. Z. Manna, S. Nes, and J. Vuillemin. Inductive methods for proving properties of programs. Commun. ACM, 16(8):491–
    502, 1973.


                                                             21
25. A. Miné. Tutorial on static inference of numeric invariants by abstract interpretation. Foundations and Trends in
    Programming Languages, 4(3-4):120–372, 2017.
26. A. Miné, J. Breck, and T. W. Reps. An algorithm inspired by constraint solvers to infer inductive invariants in numeric
    programs. In Proc. 25th European Symposium on Programming (ESOP’16), volume 9632 of Lecture Notes in Computer
    Science, pages 560–588. Springer, 2016.
27. D. Monniaux. On the decidability of the existence of polyhedral invariants in transition systems. arXiv CoRR,
    abs/1709.04382, 2017.
28. D. Monniaux. On the decidability of the existence of polyhedral invariants in transition systems. Acta Inf., 56(4):385–
    389, 2019.
29. C. Müller, H. Seidl, and E. Zalinescu. Inductive invariants for noninterference in multi-agent workflows. In Proc. 31st
    IEEE Computer Security Foundations Symposium (CSF’18), pages 247–261. IEEE Computer Society, 2018.
30. M. Müller-Olm and H. Seidl. A note on Karr’s algorithm. In Proceedings 31st International Colloquium on Automata,
    Languages and Programming (ICALP’04), volume 3142 of Lecture Notes in Computer Science, pages 1016–1028.
    Springer, 2004.
31. P. Naur. Proof of algorithms by general snapshots. BIT Numerical Mathematics, 6(4):310–316, 1966.
32. O. Padon, N. Immerman, S. Shoham, A. Karbyshev, and M. Sagiv. Decidability of inferring inductive invariants.
    In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages
    (POPL’16), pages 217–231. ACM, 2016.
33. D. Park. Fixpoint induction and proofs of program properties. Machine Intelligence, 5, 1969.
34. D. Park. On the semantics of fair parallelism. In D. Bjøorner, editor, Abstract Software Specifications, pages 504–526.
    Springer Berlin Heidelberg, 1980.
35. J. H. Reif and H. R. Lewis. Symbolic evaluation and the global value graph. In Proceedings of the 4th ACM SIGACT-
    SIGPLAN Symposium on Principles of Programming Languages, POPL’77, pages 104–118, New York, NY, USA, 1977.
    ACM.
36. X. Rival and K. Yi. Introduction to Static Analysis: An Abstract Interpretation Perspective. The MIT Press, 2020.
37. S. Shoham. Undecidability of inferring linear integer invariants. arXiv CoRR, abs/1812.01069, 2018.
38. A. M. Turing. Checking a large routine. In Report of a Conference on High Speed Automatic Calculating Machines, Uni-
    versity of Cambridge Mathematical Laboratory, Cambridge, UK, http://www.turingarchive.org/browse.php/b/8, pages
    67–69, 1949.




                                                            22
