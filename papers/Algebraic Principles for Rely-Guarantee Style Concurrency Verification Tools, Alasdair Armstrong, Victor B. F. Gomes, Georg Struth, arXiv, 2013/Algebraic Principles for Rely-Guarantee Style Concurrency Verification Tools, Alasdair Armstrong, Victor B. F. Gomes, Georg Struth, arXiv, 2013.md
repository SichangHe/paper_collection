                                           Algebraic Principles for Rely-Guarantee Style
                                                  Concurrency Verification Tools

                                                 Alasdair Armstrong, Victor B. F. Gomes, and Georg Struth

                                                   Department of Computer Science, University of Sheffield, UK
arXiv:1312.1225v1 [cs.LO] 4 Dec 2013




                                                      {a.armstrong,v.gomes,g.struth}@dcs.shef.ac.uk



                                              Abstract. We provide simple equational principles for deriving rely-
                                              guarantee-style inference rules and refinement laws based on idempotent
                                              semirings. We link the algebraic layer with concrete models of programs
                                              based on languages and execution traces. We have implemented the ap-
                                              proach in Isabelle/HOL as a lightweight concurrency verification tool
                                              that supports reasoning about the control and data flow of concurrent
                                              programs with shared variables at different levels of abstraction. This is
                                              illustrated on two simple verification examples.


                                       1    Introduction

                                       Extensions of Hoare logics are becoming increasingly important for the verifi-
                                       cation and development of concurrent and multiprocessor programs. One of the
                                       most popular extensions is Jones’ rely-guarantee method [17]. A main benefit
                                       of this method is compositionality: the verification of large concurrent programs
                                       can be reduced to the independent verification of individual subprograms. The
                                       effect of interactions or interference between subprograms is captured by rely
                                       and guarantee conditions. Rely conditions describe the effect of the environment
                                       on an individual subprogram. Guarantee conditions, in turn, describe the effect
                                       of an individual subprogram on the environment. By constraining a subprogram
                                       by a rely condition, the global effect of interactions is captured locally.
                                           To make this method applicable to concrete program development and verifi-
                                       cation tasks, its integration into tools is essential. To capture the flexibility of the
                                       method, a number of features seem desirable. First, we need to implement solid
                                       mathematical models for fine-grained program behaviour. Second, we would like
                                       an abstract layer at which inference rules and refinement laws can be derived
                                       easily. Third, a high degree of proof automation is mandatory for the analysis
                                       of concrete programs. In the context of the rely-guarantee method, tools with
                                       these important features are currently missing.
                                           This paper presents a novel approach for providing such a tool integration in
                                       the interactive theorem proving environment Isabelle/HOL. At the most abstract
                                       level, we use algebras to reason about the control flow of programs as well as for
                                       deriving inference rules and refinement laws. At the most concrete level, detailed
                                       models of program stores support fine-grained reasoning about program data
                                       flow and interference. These models are then linked with the algebras. Isabelle
allows us to implement these layers in a modular way and relate them formally
with one another. It not only provides us with a high degree of confidence in
the correctness of our development, it also supports the construction of custom
proof tactics and procedures for program verification and refinement tasks.
    For sequential programs, the applicability of algebra, and Kleene algebra in
particular, has been known for decades. Kleene algebra provides operations for
non-deterministic choice, sequential composition and finite iteration, in addi-
tion to skip and abort. With appropriate extensions, Kleene algebras support
Hoare-style verification of sequential programs, and allow the derivation of pro-
gram equivalences and refinement rules [20,16]. Kleene algebras have been used
in applications including compiler optimisation, program construction, transfor-
mation and termination analysis, and static analysis. Formalisations and tools
are available in interactive theorem provers such as Coq [26] and Isabelle [2,3,1].
A first step towards an algebraic description of rely-guarantee based reasoning
has recently been undertaken [16].
    The main contributions of this paper are as follows. First, we investigate alge-
braic principles for rely-guarantee style reasoning. Starting from [16] we extract a
basic minimal set of axioms for rely and guarantee conditions which suffice to de-
rive the standard rely-guarantee inference rules. These axioms provide valuable
insights into the conceptual and operational role of these constraints. However,
algebra is inherently compositional, so it turns out that these axioms do not fully
capture the semantics of interference in execution traces. We therefore explore
how the compositionality of these axioms can be broken in the right way, so as
to capture the intended trace semantics.
    Second, we link our rely-guarantee algebras with a simple trace based se-
mantics which so far is restricted to finite executions and disregards termination
and synchronisation. Despite the simplicity of this model, we demonstrate and
evaluate our prototypical verification tool implemented in Isabelle by verifying
two simple examples from the literature. Beyond that our approach provides
a coherent framework from which more complex and detailed models can be
implemented in the future.
    Third, we derive the usual inference rules of the rely-guarantee method with
the exception of assignment axioms directly from the algebra, and obtain assign-
ment axioms from our models. Our formalisation in Isabelle allows us to reason
seamlessly across these layers, which includes the data flow and the control flow
of concurrent programs.
    Taken together, our Isabelle implementation constitutes a tool prototype for
the verification and construction of concurrent programs. We illustrate the tool
with two simple examples from the literature. The complete Isabelle code can be
found online1 . A previous Isabelle implementation of rely-guarantee reasoning is
due to Prensa Nieto [24]. Our implementation differs both by making the link
between concrete programs and algebras explicit, which increases modularity,
and by allowing arbitrary nested parallelism.

1
    www.dcs.shef.ac.uk/~ alasdair/rg


                                         2
2    Algebraic Preliminaries

Rely-guarantee algebras, which are introduced in the following section, are based
on dioids and Kleene algebras. A semiring is a structure (S, +, ·, 0, 1) such that
(S, +, 0) is a commutative monoid, (S, ·, 1) is a monoid and the distributivity
laws x · (y + z) = x · z + y · z and (x + y) · z = x · z + y · z as well as the
annihilation laws x · 0 = 0 and 0 · x = 0 hold. A dioid is a semiring in which
addition is idempotent: x + x = x. Hence (S, +, 0) forms a join semilattice with
least element 0 and partial order defined, as usual, as x ≤ y ⇔ x + y = y. The
operations of addition and multiplication are isotone with respect to the order,
that is, x ≤ y implies z + x ≤ z + y, z · x ≤ z · y and x · z ≤ y · z. A dioid is
commutative if multiplication is: x · y = y · x.
    In the context of sequential programs, one typically thinks of · as sequential
composition, + as nondeterministic choice, 0 as the abortive action and 1 as skip.
In this context it is essential that multiplication is not commutative. Often we
use ; for sequential composition when discussing programs. More formally, it is
well known that (regular) languages with language union as +, language product
as ·, the empty language as 0 and the empty word language {ε} as 1 form dioids.
Another model is formed by binary relations with the union of relations as +,
the product of relations as ·, the empty relation as 0 and the identity relation
as 1. A model of commutative dioids is formed by sets of (finite) multisets or
Parikh vectors with multiset addition as multiplication.
    It is well known that commutative dioids can be used for modelling the in-
teraction between concurrent composition and nondeterministic choice. The fol-
lowing definition serves as a basis for models of concurrency in which sequential
and concurrent composition interact.
    A trioid is a structure (S, +, ·, ||, 0, 1) such that (S, +, ·, 0, 1) is a dioid and
(S, +, ||, 0, 1) a commutative dioid. In a trioid there is no interaction between
the sequential composition · and the parallel composition ||. On the one hand,
Gischer has shown that trioids are sound and complete for the equational theory
of series-parallel pomset languages [13], which form a well studied model of true
concurrency. On the other hand, he has also obtained a completeness result
with respect to a notion of pomset subsumption for trioids with the additional
interchange axiom (wkx) · (ykz) ≤ (w · y)k(x · z) and it is well known that this
additional axiom also holds for (regular) languages in which || is interpreted as
the shuffle or interleaving operation [12].
    Formally, the shuffle k of two finite words is defined inductively as ǫks = {s},
skǫ = {s}, and askbt = a(skbt) ∪ b(askt), which is then lifted to the shuffle
product of languages X and Y as XkY = {xky : x ∈ X ∧ x ∈ Y }.
    For programming, notions of iteration are essential. A Kleene algebra is a
dioid expanded with a star operation which satisfies both the left unfold axiom
1 + x · x⋆ ≤ x⋆ and left and right induction axioms z + x · y ≤ y ⇒ x⋆ · z ≤ y
and z + y · x ≤ y ⇒ z · x⋆ ≤ y. It follows that 1 + x · x⋆ = x⋆ and that the right
unfold axiom 1 + x⋆ · x ≤ x⋆ is derivable as well. Thus iteration x∗ is modelled
as the least fixpoint of the function λy.1 + x · y, which is the same as the least

                                           3
fixpoint of λy.1 + y · x. A commutative Kleene algebra is a Kleene algebra in
which multiplication is commutative.
    It is well known that (regular) languages form Kleene algebras and that (regu-
lar) sets of multisets form commutative Kleene algebras. In fact, Kleene algebras
are complete with respect to the equational theory of regular languages as well
as the equational theory of binary relations with the reflexive transitive closure
operation as the star [19]. Moreover, commutative Kleene algebras are complete
with respect to the equational theory of regular languages over multisets [7]. It
follows that equations in (commutative) Kleene algebras are decidable.
    A bi-Kleene algebra is a structure (K, +, ·, ||, 0, 1, ⋆ , (⋆) ) where (K, +, ·, 0, 1, ⋆ )
is a Kleene algebra and (K, +, ||, 0, 1, (⋆)) is a commutative Kleene algebra. Bi-
Kleene algebras are sound and complete with respect to the equational theory
of regular series-parallel pomset languages, and the equational theory is again
decidable [21]. A concurrent Kleene algebra is a bi-Kleene algebra which satisfies
the interchange law [16]. It can be shown that shuffle languages and regular
series-parallel pomset languages with a suitable notion of pomset subsumption
form concurrent Kleene algebras.
    In some contexts, it is also useful to add a meet operation ⊓ to a bi-Kleene
algebra, such that (K, +, ⊓) is a distributive lattice. This is particularly needed
in the context of refinement, where we typically want to represent specifications
as well as programs.


3    Generalised Hoare Logics in Kleene Algebra

It is well known that the inference rules of sequential Hoare logic (except the as-
signment axiom) can be derived in expansions of Kleene algebras. One approach
is as follows [23]. Suppose a suitable Boolean algebra B of tests has been em-
bedded into a Kleene algebra K such that 0 and 1 are the minimal and maximal
element of B, + corresponds to join and · to meet. Complements − are defined
only on B. Suppose further that a backward diamond operator hx|p has been de-
fined for each x ∈ K and p ∈ B, which models the set of all states to which each
terminating execution of program x may lead from states q. Finally suppose that
a forward box operator |x]p has been defined which models the (largest) set of
states from which every terminating execution of x must end in states p and that
boxes and diamonds are adjoints of the Galois connection hx|p ≤ q ⇔ p ≤ |x]q,
for all x ∈ K and p, q ∈ B. It is then evident from the above explanations that
validity of a Hoare triple ⊢ {p}x{q} can be encoded as hx|p ≤ q and the weakest
liberal precondition operator wlp(x, q) as |x]p. Hence the relationship between
the proof theory and the semantics of Hoare logic is captured by the Galois
connection ⊢ {p}x{q} ⇔ p ≤ wlp(x, q). It has been shown that the relational
semantics of sequential while-programs can be encoded in these modal Kleene
algebras and that the inference rules of Hoare logic can be derived [23].
    In the context of concurrency, this relational approach is no longer appropri-
ate; the following approach by Tarlecki [28] can be used instead. One can now

                                              4
encode validity of a Hoare triple as

                               ⊢ {x}y{z} ⇔ x · y ≤ z

for arbitrary elements of a Kleene algebra. Nevertheless all the rules of sequential
Hoare logic except the assignment axiom can still be derived [16]. Tarlecki’s
motivating explanations carry over to the algebraic approach.
    As an example we show the derivation of a generalised while rule. Suppose
x · t · y ≤ x. Then x · (t · y)∗ ≤ x by the right induction axiom of Kleene
algebra and therefore x · (t · y)∗ t′ ≤ x · t′ for arbitrary element t′ by isotonicity
of multiplication. This derives the while rule
                                    ⊢ {x · t}y{x}
                                 ⊢ {x}(t · y)∗ {t′ · x}

for a generalised while loop (t · y)∗ · t′ , which specialises to the conventional rule
when t and t′ are, in some sense, complements.
    The correspondence to a wlp-style semantics, as in modal Kleene algebra,
now requires a generalisation of the Galois connection for boxes and diamonds
to multiplication and an upper adjoint in the form of residuation. This can be
achieved in the context of action algebras [27], which expand Kleene algebras by
operations of left and right residuation defined by the Galois connections

               x · y ≤ z ⇔ x ≤ z ← y,          x · y ≤ z ⇔ y ≤ x → z.

These residuals, and now even the Kleene star, can be axiomatised equationally
in action algebras. For a comprehensive list of the properties of action algebras
and their most important models see [2], including the language and the rela-
tional model. In analogy to the development in modal Kleene algebra we can
now stipulate wlp(x, y) = y ← x and obtain the Galois connection

                            ⊢ {x}y{z} ⇔ x ≤ wlp(y, z)

with ⊢ {wlp(y, z)}y{z} and x ≤ wlp(y, z) ⇒ ⊢ {x}y{z} as characteristic proper-
ties. Moreover, if the action
                            Palgebra is also a quantale, and infinite sums exist,
it follows that wlp(y, z) = {x : ⊢ {x}y{z}}. It is obvious that this definition
makes sense in all models of action algebras and quantales. Intuitively, suppose
p stands for the set of all behaviours of a system, for instance the set of all
execution traces, that end in state p, and likewise for q. Then {p}x{q} states
that all executions ending in p can be extended by x to executions ending in q.
wlp(x, q) is the most general behaviour, that is the set of all executions p after
which all executions of x must end in q.
    A residuation for concurrent composition can be considered as well:

                                xky ≤ z ⇔ y ≤ x/z.

The residual x/z represents the weakest program such that when placed in par-
allel with x, the parallel composition behaves as z.

                                           5
4    A Rely-Guarantee Algebra
We now show how bi-Kleene algebras can be expanded into a simple algebra that
supports the derivation of rely-guarantee style inference rules. This development
does not use the interchange law for several reasons. First, this law fails for fair
parallel composition x kf y in models with possibly infinite, or non-terminating
programs. In this model, x · y 6≤ x kf y whenever x is non-terminating. Secondly,
it is not needed for deriving the usual rules of rely-guarantee.
     A rely-guarantee algebra is a structure (K, I, +, ⊓, ·, k, ⋆ , 0, 1), where (K, +, ⊓)
is a distributive lattice, (K, +, ·, k, 0, 1) is a trioid and (K, +, ⊓, ·, k, ⋆ , 0, 1) is a
bi-Kleene algebra where we do not consider the parallel star. I is a distinguished
subset of rely and guarantee conditions or interference constraints which satisfy
the following axioms
                                     rkr ≤ r,                                           (1)
                                       r ≤ rkr′ ,                                       (2)
                                rk(x · y) = (rkx) · (rky),                              (3)
                                       +            +
                                   rkx ≤ (rkx) .                                        (4)
By convention, we use r and g to refer to elements of I, depending on whether
they are used as relies or guarantees, and x, y, z for arbitrary elements of K. The
operations k and ⊓ must be closed with respect to I.
    The general idea is to constrain a program by a rely condition by executing
the two in parallel. Axiom (1) states that interference from a constraint being
run twice in parallel is no different from just the interference from that constraint
begin run once in parallel. Axiom (2) states that interference from a single con-
straint is less than interference from itself and another interference constraint.
Axiom (3) allows an interference constraint to be split across sequential pro-
grams. Axiom (4) is similar to Axiom (3) in intent, except it deals with finite
iteration.
    Some elementary consequences of these rules are
                1 ≤ r,      r⋆ = r · r = r = rkr,         rkx+ = (rkx)+ .
Theorem 1 Axioms (1), (2) and (3) are independent.
Proof. We have used Isabelle’s Nitpick [4] counterexample generator to construct
models which violate each particular axiom while satisfying all others.       ⊓
                                                                              ⊔
Theorem 2 Axiom (3) implies (4) in a quantale where k distributes over arbi-
trary suprema.
                                                                  P
Proof. In a quantale x+ can be defined as a sum of powers x+ = i≥1 xi where
x1 = x and xi+1 = x · xi . By induction on i we get rkxi = (rkx)i , hence
                          X       X          X
              rkx+ = rk      xi =     rkxi =     (rkx)i = (rkx)+ .
                             i≥1       i≥1          i≥1

                                                                                          ⊓
                                                                                          ⊔

                                             6
    In first-order Kleene algebras (3) and (4) are independent, but it is impossible
to find a counterexample with Nitpick because it generates only finite counterex-
amples, and all finite Kleene algebras are a forteriori quantales.
    Jones quintuples can be encoded in this setting as

                      r, g ⊢ {p}x{q} ⇐⇒ p · (rkx) ≤ q ∧ x ≤ g.                                   (5)

This means that program x when constrained by a rely r, and executed after p,
behaves as q. Moreover, all behaviours of x are included in its guarantee.

Theorem 3 The standard rely-guarantee inference rules can be derived with the
above encoding, as shown in Figure 1.



                                         p·r ≤p
                                                          Skip
                                     r, g ⊢ {p}1{p}

     r′ ≤ r       g ≤ g′        p ≤ p′      r ′ , g ′ ⊢ {p′ }x{q ′ }      q′ ≤ q
                                                                                   Weakening
                                 r, g ⊢ {p}x{q}

                       r, g ⊢ {p}x{q}       r, g ⊢ {q}y{s}
                                                                   Sequential
                                r, g ⊢ {q}x · y{s}

     r1 , g2 ⊢ {p1 }x{q1 }       g1 ≤ r2       r1 , g2 ⊢ {p2 }y{q2 }        g2 ≤ r1
                                                                                      Parallel
                      r1 ⊓ r2 , g1 kg2 ⊢ {p1 ⊓ q2 }xky{q1 ⊓ q2 }

                         r, g ⊢ {p}x{q}       r, g ⊢ {p}y{q}
                                                                       Choice
                                  r, g ⊢ {p}x + y{q}

                             p·r ≤p       r, g ⊢ {p}x{p}
                                                                   Star
                                  r, g ⊢ {p}x⋆ {p}


                           Fig. 1. Rely-guarantee inference rules


   Thus (1) to (4), which are all necessary to derive these rules, represent a
minimal set of axioms from which these inference rules can be derived.
   If we add residuals to our algebra quintuples can be encoded in the following
way, which is equivalent to the encoding in Equation (5).

                        r, g ⊢ {p}c{q} ⇐⇒ c ≤ r/(p → q) ⊓ g.                                     (6)

This encoding allows us to think in terms of program refinement, as in [14], since
r/(p → q) ⊓ g defines the weakest program that when placed in parallel with
interference from r, and guaranteeing interference at most g, goes from p to q—a
generic specification for a concurrent program.

                                                 7
5    Breaking Compositionality
While the algebra in the previous section is adequate for deriving the standard
inference rules, its equality is too strong to capture many interesting statements
about concurrent programs. Consider the congruence rule for parallel composi-
tion, which is inherent in the algebraic approach:

                               x = y =⇒ xkz = ykz.

This can be read as follows; if x and y are equal, then they must be equal under
all possible interferences from an arbitrary z. At first, this might seem to preclude
any fine-grained reasoning about interference using purely algebra. This is not
the case, but breaking such inherent compositionality in just the right way to
capture interesting properties of interference requires extra work.
    The obvious way of achieving this is to expand our rely-guarantee algebra
with an additional function π : K → K and redefining our quintuples as,

                    r, g ⊢ {p}x{q} ⇐⇒ p · (rkc) ≤π q ∧ x ≤ g.

Where x ≤π y is π(x) ≤ π(y). Since for any operator • it is not required that

                       π(x) = π(y) =⇒ π(x • z) = π(y • z),

we can break compositionality in just the right way, provided we chose appropri-
ate properties for π. These properties are extracted from properties of the trace
model, which will be explained in detail in the next section. Many of those can
be derived from the fact that, in our model, π = λx. x ⊓ c, where c is healthiness
condition which filters out ill-defined traces. We do not list these properties here.
In addition π must satisfy the properties

                                       x⋆ ≤π π(x)⋆ ,                                (7)
                                     x · y ≤π π(x) · π(y),                          (8)
                          z + x · y ≤π y =⇒ x⋆ · z ≤π y,                            (9)
                          z + y · x ≤π y =⇒ z · x⋆ ≤π y.                           (10)

   For any operator •, we write x •π y for the operator π(x • y), and we write
xπ for π(x⋆ ).
Theorem 4 (π(K), +π , ·π , π , 0, 1) is a Kleene algebra.
Proof. It can be shown that π is a retraction, that is, π 2 = π. Therefore,
x ∈ π(K) iff π(x) = x. This condition can then be used to check the closure
conditions for all operations.                                           ⊓
                                                                         ⊔
   We redefine our rely-guarantee algebra as a structure (K, I, +, ⊓, ·, k, ⋆ , π, 0, 1)
which, in addition to the rules in Section 4, satisfies (7) to (10).
Theorem 5 All rules in Figure 1 can be derived in this algebra.
Moreover their proofs remain the same, mutatis mutandis.

                                           8
6    Finite Language Model

We now construct a finite language model satisfying the axioms in Section 4
and 5. Restricting our attention to finite languages means we do not need to
concern ourselves with termination side-conditions, nor do we need to worry
about additional restrictions on parallel composition, e.g. fairness. However, all
the results in this section can be adapted to potentially infinite languages, and
our Isabelle/HOL formalisation already includes general definitions by using
coinductively defined lazy lists to represent words, and having a weakly-fair
shuffle operator for such infinite languages.
    We consider languages where the alphabet contains state pairs of the form
(σ1 , σ2 ) ∈ Σ 2 . A word in such a language is consistent if every such pair in
a word has the same first state as the previous transition’s second state. For
example, (σ1 , σ2 )(σ2 , σ3 ) is consistent, while (σ1 , σ2 )(σ3 , σ3 ) is inconsistent. Sets
of consistent words are essentially Aczel traces [9], but lack the usual process
labels. We denote the set of all consistent words by C and define the function π
from the previous section as λX. X ∩ C in our model.
    Sequential composition in this model is language product, as per usual. Con-
current composition is the shuffle product defined in Section 2. The shuffle prod-
uct is associative, commutative, and distributes over arbitrary joins. Both prod-
ucts share the same unit, {ǫ} and zero, ∅. In Isabelle proving properties of shuffle
is surprisingly tricky (especially if one considers infinite words). For a in-depth
treatment of the shuffle product see [22].

Theorem 6 (P((Σ 2 )⋆ ), ∪, ·, k, ∅, {ǫ}) forms a trioid.

   The rely-guarantee elements in this model are sets containing all the words
which can be built from some set of state pairs in Σ 2 . We define a function hRi
which lifts a relation R to a language containing words of length one for each pair
in R. The set of rely-guarantee conditions I is then defined as {r. ∃R.r = hRi⋆ }.

Theorem 7 (P((Σ 2 )⋆ ), I, ∪, ·, k, ⋆ , π, ∅, {ǫ}) is a rely-guarantee algebra.

Since hRi is atomic, it satisfies several useful properties, such as,

            hRi⋆ khSi = hRi⋆ ; hSi; hRi⋆ ,       hRi⋆ khSi⋆ = (hRi⋆ ; hSi⋆ )⋆ .

    To demonstrate how this model works, consider the graphical representation
of a language shown below.

                          σ1         σ1          σ1         σ1

                          σ2         σ2          σ2         σ2

                          σ3         σ3          σ3         σ3


                                             9
The language contains the following six words

               (σ1 , σ1 )(σ1 , σ2 )(σ2 , σ3 ),        (σ1 , σ2 )(σ1 , σ2 )(σ2 , σ3 ),
               (σ2 , σ2 )(σ1 , σ2 )(σ2 , σ3 ),        (σ1 , σ1 )(σ3 , σ2 )(σ2 , σ3 ),
               (σ1 , σ2 )(σ3 , σ2 )(σ2 , σ3 ),        (σ2 , σ2 )(σ3 , σ2 )(σ2 , σ3 ),

where only the first, (σ1 , σ1 )(σ1 , σ2 )(σ2 , σ3 ) is consistent. This word is high-
lighted with solid arrows in the diagram above. Now if we shuffle the single state
pair (σ2 , σ3 ) into the above language, we might end up with a language as below:

                   σ1           σ1           σ1             σ1           σ1

                   σ2           σ2           σ2             σ2           σ2

                   σ3           σ3           σ3             σ3           σ3


    By performing this shuffle action, we no longer have a consistent word from
σ1 to σ3 , but instead a consistent word from σ2 to σ3 and σ1 to σ3 . These
new consistent words were constructed from previously inconsistent words—the
shuffle operator can generate many consistent words from two inconsistent words.
If we only considered consistent words, à la Aczel traces, we would be unable
to define such a shuffle operator directly on the traces themselves, and would
instead have to rely on some operational semantics to generate traces.


7    Enriching the Model
To model and verify programs we need additional concepts such as tests and as-
signment axioms. A test is any language P where P ≤ hIdi. We write test(P ) for
hIdP i. In Kleene algebra the sequential composition of two tests should be equal
to their intersection. However, the traces test(P ); test(Q) and test(P ∩ Q) are
incomparable, as all words in the former have length two, while all the words in
the latter have length one. To overcome this problem, we use the concepts of stut-
tering and mumbling, following [5] and [11]. We inductively generate the mumble
language w† for a word w in a language over Σ 2 as follows: Assume σ1 , σ2 , σ3 ∈ Σ
and u, v, w ∈ (Σ 2 )⋆ . First, w ∈ w† . Secondly, if u(σ1 , σ2 )(σ2 , σ3 )v ∈ w† then
u(σ1 , σ3 )v ∈ w† . This operation is lifted to languages in the obvious way as
                                       [
                                X † = {x† . x ∈ X}.

Stuttering is represented as a rely condition hIdi⋆ where Id is the identity relation.
Two languages X and Y are equal under stuttering if hIdi⋆ kX =π hIdi⋆ kY .
   With mumbling we now have that

                            test(P ∩ Q) ≤π test(P ); test(Q)


                                                 10
as the longer words in test(P ); test(Q) can be mumbled down into the shorter
words of test(P ∩ Q), whereas stuttering gives us the opposite direction,

                 hIdi⋆ k(test(P ); test(Q)) ≤π hIdi⋆ ktest(P ∩ Q).

We henceforth assume that all languages are implicitly mumble closed.
  Using tests, we can encode if statements and while loops

               if P { X } else { Y } = test(P ); X + test(−P ); Y,
                      while P { X } = (test(P ); X)⋆ ; test(−P ).

Next, we define the operator end(P ) which contains all the words which end in
a state satisfying P . Some useful properties of end include

             end(P ); testQ ≤π end(P ∩ Q),          test(P ) ≤ end(Q),
               range(IdP ◦ R) ≤ P =⇒ end(P ); hRi⋆ ≤π end(P ).

   In this model, assignment is defined as
                             [
                 x := e =        v. test{σ. eval(σ, e) = v} · x ← v

where x ← v denotes the atomic command which assigns the value v to x. The
eval function evaluates an expression e in the state σ. Using this definition we
derive the assignment rule

             unchanged(vars(e)) ∩ preserves(P ) ∩ preserves(P [x/e]),
             unchanged(−{x})
              ⊢ {end(P )} x := e {end(P [x/e])}.

   The rely condition states the following: First, the environment is not allowed
to modify any of the variables used when evaluating e, i.e. those variables must
remain unchanged. Second, the environment must preserve the precondition.
Third, the postcondition of the assignment statement is also preserved. In turn,
the assignment statement itself guarantees that it leaves every variable other
than x unchanged. Preserves and unchanged are defined as

                preserves(P ) = h{(σ, σ ′ ). P (σ) =⇒ P (σ ′ )}i⋆ ,
              unchanged(X) = h{(σ, σ ′ ). ∀v ∈ X. σ(v) = σ ′ (v)}i⋆ .

We also defined two futher rely conditions, increasing and decreasing, which are
defined much like unchanged except they only require that variables increase or
decrease, rather than stay the same. We can easily define other useful assignment
rules—if we know properties about P and e, we can make stronger guarantees
about what x := e can do. For example the assignment x := x − 2 can also
guarantee that x will always decrease.

                                         11
8   Examples

To demonstrate how the parallel rule behaves, consider the following simple
statement, which simply assigns two variables in parallel:

                    hIdi⋆ , h⊤i⋆ ⊢ {end(x = 2 ∧ y = 2 ∧ z = 5)}
                        x := x + 2 k y := z
                    {end(x = 4 ∧ y = 5 ∧ z = 5)}.

The environment hIdi⋆ is only giving us stuttering interference. Since we are
considering this program in isolation, we make no guarantees about how this
affects the environment. To apply the parallel rule from Figure 1, we weaken
or strengthen the interference constrains and pre/postcondition as needed to fit
the form of the parallel rule.
    First, we weaken the rely condition to unchanged{x} ⊓ unchanged{y, z}. Sec-
ond we strengthen the guarantee condition to unchanged{y, z} k unchanged{x}.
When we apply the parallel rule each assignment’s rely will become the other as-
signment’s guarantee. Finally, we split the precondition and postcondition into
end(x = 2) ⊓ end(y = 2 ∧ z = 5) and end(x = 4) ⊓ end(y = 5 ∧ z = 5)
respectively. Upon applying the parallel rule, we obtain two trivial goals

 hunchanged{x}i⋆ , hunchanged{y, z}i⋆ ⊢ {end(x = 2)} x := x + 2 {end(x = 4)},
 hunchanged{y, z}i⋆, hunchanged{x}i⋆ ⊢ {end(y = 2 ∧ z = 5)}
     y := z
 {end(y = 5 ∧ z = 5)}.

     Figure 2 shows the FINDP program, which has been used by numerous au-
thors e.g. [25,17,10,14]. The program finds the least element of an array satisfying
a predicate P . The index of the first element satisfying p is placed in the variable
f . If no element of the array satisfies P then f will be set to the length of the
array. The program has two subprograms, A and B, running in parallel, one
of which searches the even indices while the other searches the odd indices. A
speedup over a sequential implementation is achieved as A will terminate when
B finds an element of the array satisfying P which is less than iA .
     Here, we only sketch the correctness proof, and comment on its implemen-
tation in Isabelle. We do not attempt to give a detailed proof, as this has been
done many times previously.
     To prove the correctness of FINDP, we must show that

                FINDP ≤π end(leastP(f )) + end(f = len(array)),

where leastP(f) is the set of states where f is the least index satisfying P , and
f = len(array) is the set of states where f is the length of the array. In other
words, either we find the least element, or no elements in the array satisfy P , in
which case f remains the same as the length of the array.

                                         12
            fA := len(array);
            fB := len(array);
                                                                  
              iA = 0                       iB = 1
             while iA < fA ∧ iA < fB {    while iB < fA ∧ iB < fB {
                                                                   
                                                                   
            
                  if P (array[iA ]) {          if P (array[iB ]) { 
                                                                    
                         fA := iA                     fB := iB
                                                                   
                                                                   
                                                                   ;
            
                  } else {                     } else {            
                                                                    
                                                                   
            
                        iA := iA + 2                 iB := iB + 2  
                                                                    
                   }                            }
                                                                   
                                                                   
              }                            }
            f = min(fA , fB )

                                Fig. 2. FINDP Program


    To prove the parallel part of the program, subprogram A guarantees that
it does not modify any of the variables used by subprogram B, except for fA ,
which it guarantees will only ever decrease. Subprogram B makes effectively the
same guarantee to A. Under these interference constraints we then prove that
A or B will find the lowest even or odd index which satisfies P respectively—or
they do not find it, in which case fA or fB will remain equal to the length of
the array.
    Despite the seemingly straightforward nature of this proof, it turns out to be
surprisingly difficult in Isabelle. Each atomic step needs to be shown to satisfy
the guarantee of its containing subprogram, as well as any goals relating to its
pre and post conditions. This invariably leads to a proliferation of many small
proof goals, even for such a simple program. More work must be done to manage
the complexity of such proofs within interactive theorem provers.


9   Conclusion
We have introduced variants of semirings and Kleene algebras intended to model
rely-guarantee and interference based reasoning. We have developed an inter-
leaving model for these algebras which uses familiar concepts from traces and
language theory. This theory has been implemented in the Isabelle/HOL theo-
rem prover, providing a solid mathematical basis on which to build a tool for
mechanised refinement and verification tasks. In line with this aim, we have
applied our formalisation to two simple examples.
    This implementation serves as a basis from which further interesting aspects
of concurrent programs, such as non-termination and synchronisation can be
explored. As mentioned in Section 6, some of the work needed to implement this
we have already done in Isabelle.
    Algebra plays an important role in our development. First, it allowed us to
derive inference rules rapidly and with little proof effort. Second, it yields an

                                         13
abstract layer at which many properties that would be difficult to prove in con-
crete models can be verified with relative ease by equational reasoning. Third,
as pointed out in Section 2, some fragments of the algebras considered are decid-
able. Therefore, decision procedures for some aspects of rely-guarantee reasoning
can be implemented in interactive theorem proving tools such as Isabelle.
    The examples from Section 8 confirm previous evidence [24] that even seem-
ingly straightforward concurrency verification tasks can be tedious and complex.
It is too early to draw informed conclusions, but while part of this complexity
may be unavoidable, more advanced models and proof automation are needed to
overcome such difficulties. Existing work on combining rely-guarantee with sepa-
ration logic [29] may prove useful here. Our language model is sufficiently generic
such that arbitrary models of stores may be used, including those common in
separation logic, which have already been implemented in Isabelle [18].
    In addition, algebraic approaches to separation logic have already been in-
troduced. Examples are the separation algebras in [6], and algebraic separation
logic [8]. More recently, concurrent Kleene algebras have given an algebraic ac-
count of some aspects of concurrent separation logic [16,15].

Acknowledgements. The authors would like to thank Brijesh Dongol and Ian
Hayes for inspiring discussions on concurrency verification and the rely-guarantee
method. The first author acknowledges funding from an EPSRC doctoral fel-
lowship. The second author is supported by CNPq Brazil. The third author
acknowledges funding by EPSRC grant EP/J003727/1.

References
 1. A. Armstrong, V. B. F. Gomes, and G. Struth. Algebras for program correctness
    in Isabelle/HOL. In RAMiCS 2014 (under review), 2014.
 2. A. Armstrong, G. Struth, and T. Weber. Kleene algebra. Archive of Formal Proofs,
    2013.
 3. A. Armstrong, G. Struth, and T. Weber. Program analysis and verification
    based on Kleene algebra in Isabelle/HOL. In S. Blazy, C. Paulin-Mohring, and
    D. Pichardie, editors, ITP 2013, number 7998 in LNCS, pages 197–212. Springer,
    2013.
 4. J. C. Blanchette and T. Nipkow. Nitpick: A counterexample generator for higher-
    order logic based on a relational model finder. In M. Kaufmann and L. C. Paulson,
    editors, ITP 2010, number 6172 in LNCS, pages 131–146. Springer, 2010.
 5. S. Brookes. Full abstraction for a shared variable parallel language. In M. Okada
    and P Panangaden, editors, LICS 93, page 98–109, 1993.
 6. C. Calcagno, P. W. O’Hearn, and H. Yang. Local action and abstract separation
    logic. In L. Ong, editor, LICS 07, page 366–378, 2007.
 7. J. H. Conway. Regular algebra and finite machines. Chapman and Hall, 1971.
 8. H.-H. Dang, P. Höfner, and B. Möller. Algebraic separation logic. J. Log. Algebr.
    Program., 80(6):221–247, 2011.
 9. F. S. de Boer, U. Hannemann, and W.-P. de Roever. Formal justification of the
    rely-guarantee paradigm for shared-variable concurrency: a semantic approach. In
    J. M. Wing, J. Woodcock, and J. Davies, editors, FM’99 — Formal Methods,
    number 1709 in LNCS, pages 1245–1265. Springer, 1999.


                                          14
10. W.-P. de Roever, F. de Boer, U. Hanneman, J. Hooman, Y. Lakhnech, M. Poel,
    and J. Zwiers. Concurrency verification: an introduction to state-based methods.
    Cambridge University Press, Cambridge, 2001.
11. J. Dingel. A refinement calculus for shared-variable parallel and distributed pro-
    gramming. Formal Aspects of Computing, 14(2):123–197, 2002.
12. J. L. Gischer. Shuffle languages, petri nets, and context-sensitive grammars. Com-
    mun. ACM, 24(9):597–605, 1981.
13. J. L. Gischer. The equational theory of pomsets. Theoretical Computer Science,
    61(2–3):199–224, 1988.
14. I. J. Hayes, C. B. Jones, and R. J. Colvin. Refining rely-guarantee thinking.
    (unpublished), 2013.
15. C. A. R. Hoare, A. Hussain, B. Möller, P. W. O’Hearn, R. L. Petersen, and
    G. Struth. On locality and the exchange law for concurrent processes. In J.-
    P. Katoen and B. König, editors, CONCUR 2011, number 6901 in LNCS, pages
    250–264. Springer, 2011.
16. T. Hoare, B. Möller, G. Struth, and I. Wehrman. Concurrent kleene algebra and
    its foundations. J. Log. Algebr. Program., 80(6):266–296, 2011.
17. C. B. Jones. Development methods for computer programs including a notion of
    interference. PhD thesis, Oxford University, 1981.
18. G. Klein, R. Kolanski, and A. Boyton. Mechanised separation algebra. In
    L. Beringer and A. Felty, editors, ITP 2012, volume 7406 of LNCS, pages 332–
    337. Springer, 2012.
19. D. Kozen. A completeness theorem for kleene algebras and the algebra of regular
    events. Information and Computation, 110(2):366–390, 1994.
20. D. Kozen. Kleene algebra with tests. ACM Trans. Program. Lang. Syst.,
    19(3):427–443, 1997.
21. M. R. Laurence and G. Struth. Completeness results for bi-Kleene algebras and
    regular pomset languages, 2013. (submitted).
22. A. Mateescu, G. D. Mateescu, G. Rozenberg, and A. Salomaa. Shuffle-like oper-
    ations on ω-words. In G. Păun and A. Salomaa, editors, New Trends in Formal
    Languages, number 1218 in LNCS, pages 395–411. Springer, 1997.
23. B. Möller and G. Struth. Algebras of modal operators and partial correctness.
    Theoretical Computer Science, 351(2):221–239, 2006.
24. L. P. Nieto. The rely-guarantee method in Isabelle/HOL. In P. Degano, edi-
    tor, Programming Languages and Systems, number 2618 in LNCS, pages 348–362.
    Springer, 2003.
25. S. Owicki. Axiomatic Proof Techniques for Parallel Programs. PhD thesis, Cornell
    University, 1975.
26. D. Pous. Kleene algebra with tests and Coq tools for while programs. In S. Blazy,
    C. Paulin-Mohring, and D. Pichardie, editors, ITP 2013, number 7998 in LNCS,
    pages 180–196. Springer B, 2013.
27. V. R. Pratt. Action logic and pure induction. In J. van Eijck, editor, JELIA ’90,
    volume 478 of LNCS, page 97–120. Springer, 1990.
28. A. Tarlecki. A language of specified programs. Science of Computer Programming,
    5:59–81, 1985.
29. Viktor Vafeiadis. Modular fine-grained concurrency verification. PhD thesis, Uni-
    versity of Cambridge, 2008.




                                         15
