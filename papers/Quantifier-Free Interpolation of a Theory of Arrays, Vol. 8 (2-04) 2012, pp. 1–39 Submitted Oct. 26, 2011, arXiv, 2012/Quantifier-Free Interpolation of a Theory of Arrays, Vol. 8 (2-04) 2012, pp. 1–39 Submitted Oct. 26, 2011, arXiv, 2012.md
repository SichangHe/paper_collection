Logical Methods in Computer Science
Vol. 8 (2:04) 2012, pp. 1–39                                                                  Submitted        Oct. 26, 2011
www.lmcs-online.org                                                                           Published        Apr. 27, 2012




  QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS

               ROBERTO BRUTTOMESSO a , SILVIO GHILARDI b , AND SILVIO RANISE c
   a
       Dipartimento di Scienze dell’Informazione, Università degli Studi di Milano (Italy)
       e-mail address: bruttomesso@dsi.unimi.it
   b
       Dipartimento di Matematica, Università degli Studi di Milano (Italy)
       e-mail address: ghilardi@dsi.unimi.it
   c
       FBK-Irst, Trento (Italy)
       e-mail address: ranise@fbk.eu


           Abstract. The use of interpolants in model checking is becoming an enabling technology
           to allow fast and robust verification of hardware and software. The application of encodings
           based on the theory of arrays, however, is limited by the impossibility of deriving quantifier-
           free interpolants in general.
               In this paper, we show that it is possible to obtain quantifier-free interpolants for a
           Skolemized version of the extensional theory of arrays. We prove this in two ways:
             (1) non-constructively, by using the model theoretic notion of amalgamation, which is
                  known to be equivalent to admit quantifier-free interpolation for universal theories;
                  and
             (2) constructively, by designing an interpolating procedure, based on solving equations
                  between array updates. (Interestingly, rewriting techniques are used in the key steps
                  of the solver and its proof of correctness.)
           To the best of our knowledge, this is the first successful attempt of computing quantifier-
           free interpolants for a variant of the theory of arrays with extensionality.




       1998 ACM Subject Classification: F.4.1, F.3.1.
       Key words and phrases: Amalgamation, Modular constraints, Interpolating metarules.
       This paper is a substantially extended version of [17].



l      LOGICAL METHODS
       IN COMPUTER SCIENCE               DOI:10.2168/LMCS-8 (2:04) 2012
                                                                                  c
                                                                                  CC
                                                                                       R. Bruttomesso, S. Ghilardi, and S. Ranise
                                                                                       Creative Commons
2                       R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




                                       Contents
    1. Introduction                                                       3
    1.1. Contributions                                                    4
    1.2. Plan of the paper                                                5
    2. Formal preliminaries                                               5
    2.1. Theories, constraints, interpolants                              5
    2.2. Some model theoretic concepts and results                        6
    2.3. Some term rewriting concepts and results                         7
    3. Theories of Arrays and Quantifier-free Interpolation               8
    3.1. A semantic argument for quantifier-free interpolation            9
    4. Modular constraints for Arrays with diff and their combinations   12
    4.1. Modular constraints in AX diff                                  13
    4.2. Combining modular constraints                                   17
    5. A Solver for Arrays with diff                                     18
    5.1. Preprocessing                                                   19
    5.2. Completion                                                      19
    6. The Interpolation Algorithm for Arrays with diff                  22
    6.1. Interpolating Metarules                                         22
    6.2. The Interpolating Solver                                        23
    6.3. An Example                                                      28
    7. Related work and Conclusions                                      30
    7.1. Satisfiability                                                  30
    7.2. Interpolation                                                   32
    7.3. Conclusions and Future Work                                     34
    References                                                           35
    Appendix A. Proof of Theorem 2.3                                     38
                  QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                        3




                                           1. Introduction
Craig’s interpolation theorem [24] applies to first order logic formulæ and states that when-
ever the sequent A ∧ B ⇒ ⊥ is valid, then it is possible to derive a formula I such that
(i) A ⇒ I is valid , (ii) I ∧ B ⇒ ⊥ is valid, and (iii) I is defined over the common
symbols of A and B.1 After the seminal work of McMillan (see, e.g., [48]), Craig’s inter-
polation has become an important technique in verification. Intuitively, the interpolant I
can be seen as an over-approximation of A with respect to B. This observation is cru-
cial for several applications of interpolation in verification. For example, the importance
of computing quantifier-free interpolants (as several symbolic verification procedures rep-
resent sets of states and transitions as quantifier-free formulae) to over-approximate the
set of reachable states for model checking has been observed. Unfortunately, Craig’s in-
terpolation theorem does not guarantee that it is always possible to compute quantifier-
free interpolants. Even worse, for certain first-order theories, it is known that quanti-
fiers must occur in interpolants of quantifier-free formulae [37]. As a consequence, several
papers [11, 21, 22, 34, 37, 40, 42, 46, 50, 52, 54, 56] focused on the efficient computation of
quantifier-free interpolants for first-order theories which are relevant for verification such
as uninterpreted functions, (fragments of) Presburger arithmetic, theories of some data-
structures, and their combination. Despite the ongoing efforts, so far, only the negative
result in [37] is available for the computation of interpolants in the theory of arrays with
extensionality, axiomatized by the following three sentences:
                              ∀y, i, e.rd(wr(y, i, e), i) = e
                              ∀y, i, j, e.i 6= j ⇒ rd(wr(y, i, e), j) = rd(y, j)
                              ∀x, y.x 6= y ⇒ (∃i. rd(x, i) 6= rd(y, i))
where rd and wr are the usual operations for reading or updating arrays, respectively. For
instance, there is no quantifier-free interpolant for the pair of quantifier-free formulae
                    A ≡ x = wr(y, i, e)
                    B ≡ rd(x, j) 6= rd(y, j) ∧ rd(x, k) 6= rd(y, k) ∧ j 6= k.
This theory is important for both hardware and software verification, and a procedure for
computing quantifier-free interpolants “would extend the utility of interpolant extraction as
a tool in the verifier’s toolkit” [48]. Indeed, the endeavour of designing such a procedure
would be bound to fail (according to [37]) if we restrict ourselves to the original theory.
To circumvent the problem, we add the (binary) function diff to rd and wr. Intuitively,
diff(a, b) is an index at which the elements stored in the arrays a and b are different
(diff(a, b) is defined arbitrarily in case a and b coincide). Formally, this is characterized
by Skolemizing the third axiom above (also called the extensionality axiom) to obtain
                    ∀x, y.x 6= y ⇒ rd(x, diff(x, y)) 6= rd(y, diff(x, y))).
This axiom is sufficient to ensure that the theory of arrays with diff admits quantifier-free
interpolants for quantifier-free formulae or, equivalently, that the quantifier-free fragment
of the theory is closed under interpolation. For example, a quantifier-free interpolant for A
   1To be precise, the original formulation of [24] is slightly different, and it states that whenever A ⇒ B is
valid, then it is possible to derive an I such that A ⇒ I ⇒ B are valid, and I is over the common symbols
of A and B. Clearly, the two formulations are equivalent.
4                       R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




and B above is
                      I ≡ x = wr(y, diff(x, y), rd(x, diff(x, y))).
Notice how diff permits to represent indexes in the quantifier-free interpolant I by men-
tioning only the array constants a and b that are common to A and B. As we will see in the
rest of the paper, this is crucial to compute quantifier-free interpolants. One may wonder
how useful it is to be able to compute quantifier-free interpolants in the Skolemized variant
of the theory of arrays with extensionality considered here. The answer lies in the obser-
vation that this variant is sufficient whenever there is a need to check the unsatisfiability
of formulae as it is the case of many applications; one of the most important is in model
checking procedures for infinite state systems (see, e.g., [34]).

1.1. Contributions. The paper presents two main contributions, that are strictly related
but completely independent.
     First, we prove non-constructively that given two quantifier-free formulae in the the
theory of arrays with diff, it is possible to compute a quantifier-free interpolant. We
do this by using the notion of amalgamation [20, 32]. Intuitively, a first-order theory has
the amalgamation property if any two structures in its class of models sharing a common
sub-model can be regarded as sub-structures of a larger model. A well-known result (see,
e.g., [7]) states that if the class of models of a universal theory T (namely, a theory axiom-
atized by sentences obtained by prefixing a quantifier-free formula with a block of universal
quantifiers) have the amalgamation property, then T admits quantifier-free interpolants for
quantifier-free formulae in the theory and vice versa. Since the theory of arrays with diff is
universal, we consider the problem of showing that its class of models has the amalgamation
property. We provide a first, non-constructive, proof of this result by using model-theoretic
notions only.
     The second contribution of the paper is an algorithm for the generation of quantifier-
free interpolants from finite sets (intended conjunctively) of literals in the theory of arrays
with diff. Our algorithm uses as a sub-module a satisfiability procedure for sets of literals
of the theory. Such a module is based on a sequence of syntactic manipulations organized
in groups of syntactic transformations. The most important group of transformations is
a Knuth-Bendix completion procedure (see, e.g., [4]) extended in such a way to solve an
equation a = wr(b, i, e) for b when this is required by the ordering defined on terms. (We call
Gaussian completion this extended procedure because of its similarity with the techniques
to handle Gaussian theories [3].) The goal of these transformations is to produce what we
call a “modular” constraint for which it is trivial to establish satisfiability. Given two sets
A and B of literals, the satisfiability procedure is invoked on A and B. While running,
the two instances of the procedure exchange literals on the common signature of A and B
(similarly to the Nelson and Oppen combination method, see, e.g., [51]) and perform some
additional actions. At the end of the computation, the execution trace is examined and
the desired interpolant is built by simple rules whose goal is to produce a set of literals on
the common signature of A and B. In fact, the problem during the execution of Gaussian
completion is to avoid the generation of equalities containing terms built out of non-shared
symbols. Notice that our approach seems to be quite different from the standard method
of extracting interpolants from an unsatisfiability proof of A and B in a given calculus
(e.g., [11, 46]). Theoretically, it is not difficult to refine our proof of termination to show
that the proposed algorithm is in NP, which is optimal since the satisfiability problem of
                 QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                  5




quantifier-free formulae in the theory of arrays with extensionality is NP-complete (see,
e.g., [10]).

1.2. Plan of the paper. In Section 2, we recall some background notions about theories,
model-theoretic notions, and rewriting. In Section 3, we define the theory of arrays with
diff, characterize its models, and show non-constructively that it admits quantifier-free
interpolation. The rest of the paper is devoted to prove the same result constructively. In
Section 4, we introduce modular constraints (which will be manipulated by the interpola-
tion procedure) and state (and prove) their key properties. In Section 5, we describe the
satisfiability solver for the theory of arrays with diff based on syntactic transformations
of modular constraints. Then, in Section 6, we extend such as solver to produce quantifier-
free interpolants by using a carefully designed set of meta-rules for interpolation. Finally,
in Section 7, we extensively discuss the related work and conclude.
     The appendix contains a proof of the result in [7] to make the paper self-contained.

                                   2. Formal preliminaries
We assume the usual syntactic (e.g., signature, variable, term, atom, literal, formula, and
sentence) and semantic (e.g., structure, truth, satisfiability, and validity) notions of first-
order logic. The equality symbol “=” is included in all signatures considered below. For
clarity, we shall use “≡” in the meta-theory to express the syntactic identity between two
symbols or two strings of symbols, or to introduce a new definition.

2.1. Theories, constraints, interpolants. A theory T is a pair (Σ, AxT ), where Σ is
a signature and AxT is a set of Σ-sentences, called the axioms of T (we shall sometimes
write directly T for AxT ). The Σ-structures in which all sentences from AxT are true
are the models of T . A universal (resp. existential) sentence is obtained by prefixing a
string of universal (resp. existential) quantifiers to a quantifier-free formula. A theory T
is universal iff AxT consists of universal sentences. A Σ-formula φ is T -satisfiable if there
exists a model M of T such that φ is true in M under a suitable assignment a to the free
variables of φ (in symbols, (M, a) |= φ); it is T -valid (in symbols, T ⊢ ϕ) if its negation
is T -unsatisfiable or, equivalently, iff ϕ is provable from the axioms of T in a complete
calculus for first-order logic. A formula ϕ1 T -entails a formula ϕ2 if ϕ1 → ϕ2 is T -valid; the
notation used for such T -entailment is ϕ1 ⊢T ϕ2 or simply ϕ1 ⊢ ϕ2 , if T is clear from the
context. The satisfiability modulo the theory T (SM T (T )) problem amounts to establishing
the T -satisfiability of quantifier-free Σ-formulae.
     Let T be a theory in a signature Σ; a T -constraint (or, simply, a constraint) A is a set of
ground literals in a signature Σ′ obtained from Σ by adding a set of free constants. Taking
conjunction, we can consider a finite constraint A as a single formula; thus, when we say that
a constraint A is T -satisfiable (or just “satisfiable” if T is clear from the context), we mean
that the associated formula (also called A) is satisfiable in a Σ′ -structure which is a model of
T . Let a1 , . . . , an be the tuple of free constants occurring in a sentence A and x1 , . . . , xn be
a tuple of fresh distinct individual variables, the formula A∃ is obtained from A by replacing
each ai with xi (for i = 1, ..., n) and then existentially quantifying x1 , . . . , xn , i.e. A∃ denotes
the formula ∃x1 · · · ∃xn A(x1 /a1 , . . . , xn /an ). We have two notions of equivalence between
constraints, which are summarized in the next definition.
6                          R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




Definition 2.1. Let A and B be finite constraints (or, more generally, first order sentences)
in an expanded signature. We say that A and B are logically equivalent (modulo T ) iff T ⊢
A ↔ B; on the other hand, we say that they are ∃-equivalent (modulo T ) iff T ⊢ A∃ ↔ B ∃ .
     Logical equivalence means that the constraints have the same semantic content (modulo
T ); ∃-equivalence is also useful because we are mainly interested in T -satisfiability of con-
straints and it is trivial to see that ∃-equivalence implies equisatisfiability (again, modulo
T ). As an example, if we take a constraint A, we replace all occurrences of a certain term t
in it by a fresh constant a and add the equality a = t, called the (explicit) definition (of t),
the constraint A′ we obtain in this way is ∃-equivalent to A. As another example, suppose
that A ⊢T a = t, that a does not occur in t, and that A′ is obtained from A by replacing a
by t everywhere; then the following four constraints are ∃-equivalent
                               A,    A ∪ {a = t},     A′ ∪ {a = t},      A′
(the first three are also pairwise logically equivalent). The above examples show how explicit
definitions can be introduced and removed from constraints while preserving ∃-equivalence.
     A theory T is said to admit quantifier-free interpolation (or, equivalently, to have
quantifier-free interpolants) iff for every pair of quantifier free formulae φ, ψ such that ψ ∧ φ
is not T satisfiable, there exists a quantifier free formula θ, called an interpolant, such that:
(i) ψ T -entails θ; (ii) θ ∧ φ is not T -satisfiable: (iii) only variables occurring both in ψ and
in φ occur in θ.

2.2. Some model theoretic concepts and results. We recall some basic model-theoretic
notions that will be used in the paper (for more details, the interested reader is pointed to
standard textbooks in model theory, such as [20]).
     If Σ is a signature, we use the notation M = (M, I) for a Σ-structure, meaning that
M is the support of M and I is the related interpretation function for Σ-symbols (in a
many-sorted framework, the support is the disjoint union of the interpretations of the sorts
symbols of Σ).
     Roughly, an embedding is a homomorphism that preserves and reflects relations and
operations. Formally, a Σ-embedding (or, simply, an embedding) between two Σ-structures
M = (M, I) and N = (N, J ) is any mapping µ : M −→ N among the corresponding
support sets satisfying the following three conditions: (a) µ is a (sort-preserving) injective
function; (b) µ is an algebraic homomorphism, that is for every n-ary function symbol f
and for every a1 , . . . , an ∈ M , we have f N (µ(a1 ), . . . , µ(an )) = µ(f M (a1 , . . . , an )); (c) µ
preserve and reflects interpreted predicates, i.e. for every n-ary predicate symbol P , we
have (a1 , . . . , an ) ∈ P M iff (µ(a1 ), . . . , µ(an )) ∈ P N . By using simple set-theory, it possible
to show that every embedding can be factored in an isomorphism and an inclusion. This
means that if µ is an embedding from M to N , it is possible to assume that —up to an
isomorphism—M is a substructure of N , in the sense defined below.
     If M ⊆ N and the embedding µ : M −→ N is just the identity inclusion M ⊆ N ,
we say that M is a substructure of N or that N is an superstructure of M. Notice that
a substructure of N is nothing but a subset of the carrier set of N which is closed under
the Σ-operations and whose Σ-structure is inherited from N by restriction. In fact, given
N = (N, J ) and G ⊆ N , there exists the smallest substructure of N containing G in
its carrier set. This is called the substructure generated by G and its carrier set can be
characterized as the set of the elements b ∈ N such that tN (a) = b for some Σ-term t and
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                             7




some finite tuple a from G (when we write tN (a) = b, we mean that (N , a) |= t(x) = y for
an assignment a mapping the a to the x and b to y). An easy—but fundamental—fact is
that the truth of a universal (resp. existential) sentence is preserved through substructures
(resp. through superstructures).
     Let M = (M, I) be a Σ-structure which is generated by G ⊆ M . Let us expand Σ
with a set of fresh free constants in such a way that in the expanded signature ΣG there is
a fresh free constant cg for every g ∈ G (write cg directly with g for simplicity). Let MG be
the ΣG -structure obtained from M by interpreting each cg as g. The ΣG -diagram δM (G)
of M is the set of all ground ΣG -literals L such MG |= L. When we speak of the diagram
of M tout court, we mean the ΣM -diagram δM (M ).
     The following celebrated result [20] is simple, but nevertheless very powerful and it will
be used in the rest of the paper.
Lemma 2.2 (Robinson Diagram Lemma). Let M = (M, I) be a Σ-structure which is
generated by G ⊆ M and N = (N, J ) be another Σ-structure. Then, there is a bijective
correspondence between Σ-embeddings µ : M −→ N and ΣG -expansions N (G) = (N, J (G) )
of N such that N (G) |= δM (G). The correspondence associates with µ the extension of J
to ΣG given by J (G) (cg ) ≡ µ(g).
    Notice that an embedding µ : M −→ N is uniquely determined, in case it exists, by
the image of the set of generators G: this is because the fact that G generates M implies
(and is equivalent to) the fact that every c ∈ M is of the kind tM (g), for some term t and
some g from G.
    Intuitively, amalgamation is a property of collections of structures that guarantees that
two structures in the collection can be glued into substructures of a larger one. Formally, a
theory T is said to have the amalgamation property iff whenever we are given embeddings
                          µ1 : N −→ M1 ,         µ2 : N −→ M2
among the models N , M1 , M2 of T , then there exists a further model M of T endowed
with embeddings
                          ν1 : M1 −→ M,          ν2 : M2 −→ M
such that ν1 ◦ µ1 = ν2 ◦ µ2 . Notice that, up to isomorphism, we can limit ourselves in the
above definition to the case in which µ1 , µ2 are inclusions, i.e. to the case in which N is just
a substructure of both M1 , M2 ; in this case, M is said to be a T -amalgam of M1 and M2
over N . (When the signature does not have ground terms of some sort, models N having
empty domain(s) must be included in the definition of amalgamation property.)
Theorem 2.3 ( [7]). Let T be universal; then T admits quantifier free interpolants iff T
has the amalgamation property.
    We emphasize that the hypothesis for T to be universal is necessary for the above result
to hold. To make the paper self-contained, we include the proof of this result in Appendix A.

2.3. Some term rewriting concepts and results. We shall need basic term rewriting
system notions and results (see, e.g., [4]). In the following, we recall some of the most
important ones for this paper.
     The reflexive and transitive closure of a binary relation → is denoted with →∗ and
its transitive closure by →+ . A binary relation → over a set E is terminating if there
8                             R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




are no infinite sequence e0 , e1 , ... of elements of E such that (ei , ei+1 ) ∈→, also written as
ei → ei+1 , for every i ≥ 0. The relation →⊆ E × E is confluent if there exists v ∈ E such
that s →∗ v and t →∗ v whenever u →∗ s and u →∗ t, for s, t, u ∈ E. The relation → is
convergent if it is both terminating and confluent.
       A rewrite rule is an ordered pair of terms l and r, written as l → r (intuitively, the
rule is used to replace instances of l with instances of r).2 A (term-)rewriting system is a
set R of rewrite rules, which induces a rewrite relation →R (or simply → when R is clear
from the context) on terms as follows: →R is the relation that contains the pairs of terms
(t, t′ ) such that (for some l → r in R) the term t has a sub-term of the form lσ for some
substitution σ (in symbols t ≡ t[lσ]), and t′ is obtained by replacing that subterm lσ by
rσ in t (in symbols t′ ≡ t[rσ]). Let s and t terms; we say that s and t are joinable w.r.t.
a rewrite relation → (in symbols, s ↓ t) when there exists a term u such that s →∗ u and
t →∗ u. A term t is reducible w.r.t. a rewrite relation → if there exists a term u such that
t → u; otherwise, t is irreducible. A term u is a normal form of t w.r.t. a rewrite relation →
if t →∗ u and u is irreducible. A rewrite relation is ground convergent when it is convergent
once restricted to the set of ground terms. Convergent rewrite relations are interesting
because they have unique normal forms. KnuthBendix completion is a procedure, based on
superposition of critical pairs, for transforming a rewrite system into a confluent one (see,
e.g., [4] for details). Termination of rewrite systems is undecidable.
       A quasi-ordering is a reflexive and transitive relation. The lexicographic path ordering
≻ on a set of terms induced by a quasi-ordering >, called precedence relation, on the
set of constant and function symbols on which the terms are built is defined as follows:
s = f (sl , . . . , sm ) ≻ g(tl , . . . , tn ) = t iff
(1) sk ≻ t or sk ≡ t for some k ∈ {1, . . . , m}, or
(2) f > g and s ≻ tl for each l ∈ {1, . . . , n}, or
(3) f ≡ g, s1 ≡ t1 , ..., sj−1 ≡ tj−1 , sj ≻ tj , s ≻ tj+1 , ..., s ≻ tn for some j ∈ {1, . . . , n}.
If the precedence relation > is also total, then so is ≻ once restricted to ground terms.

             3. Theories of Arrays and Quantifier-free Interpolation
The McCarthy theory of arrays AX [43] has three sorts ARRAY, ELEM, INDEX (called “ar-
ray”, “element”, and “index” sort, respectively) and two function symbols rd and wr of
appropriate arities; its axioms are:
                           ∀y, i, e.      rd(wr(y, i, e), i) = e                                     (3.1)
                         ∀y, i, j, e.     i 6= j ⇒ rd(wr(y, i, e), j) = rd(y, j).                    (3.2)
The theory of arrays with extensionality AX ext has the further axiom
                              ∀x, y.x 6= y ⇒ (∃i. rd(x, i) 6= rd(y, i)),
called the ‘extensionality’ axiom. In this paper, we consider a variant of the McCarthy
theory of arrays with extensionality, obtained by Skolemizing the axioms of extensional-
ity. Formally, we define the theory of arrays with diff AX diff by adding the additional
(Skolem) function diff to the signature of AX diff and replace the extensionality axiom by
its Skolemization, namely
                     ∀x, y.      x 6= y ⇒ rd(x, diff(x, y)) 6= rd(y, diff(x, y)).                    (3.3)
    2To avoid pathological cases, it is assumed that all variables occurring in r occur also in l.
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                          9




The new symbol diff is binary and takes two arguments of sort ARRAY and returns an
element of sort INDEX. The new axiom (3.3) constrains diff to return an index at which
the two arrays in input store different values, whereas it returns an arbitrary value when
input arrays are equal.

3.1. A semantic argument for quantifier-free interpolation. Here, we show that
AX diff does admit quantifier-free interpolation, contrary to AX ext [37]. We do so by using
a model-theoretic argument based on the equivalence between amalgamation of the models
and admitting quantifier-free interpolation for universal theories (recall Theorem 2.3 in
Section 2.2). Notice that AX diff is universal whereas AX ext is not.
     Since amalgamation is a property of the models of a theory, we preliminarily discuss
the class of models of AX diff . A model of AX ext or AX diff is standard when ARRAY is
interpreted as the set of all functions from indexes to elements. In a standard model of
AX ext or AX diff , arrays are interpreted as functions, rd as function application, and wr
as the point-wise update operation (i.e. the interpretation of wr(a, i, e) returns the same
values of the interpretation of a, except at the interpretation of index i where it returns
the interpretation of e). Indeed, the class of models of AX ext or AX diff contains also non-
standard models. This is because the axioms of both AX ext and AX diff , being first-order
formulae, do not constrain the interpretation of the sort ARRAY to contain all mappings from
indexes to elements. (This is similar to the interpretation of function variables according
to the Henkin semantics of second order logic; see, e.g., [27].) Fortunately, because of
the extensionality axiom, it is easy to show (see below) that every model of such theories
embeds into a standard one (recall the definition of embedding in Section 2.2). This means
that any model is isomorphic to a sub-structure of a standard model in which arrays are
interpreted as functions, although it might happen that not all functions are part of the
interpretation of ARRAY in the model. As a consequence, whenever we want to test the
validity of universal formulae or the satisfiability of constraints, we can—w.l.o.g.—consider
only standard models. (This fact will be used in the proofs of some results in later sections,
such as the proof of Lemma 4.3 where a standard model is built to show the satisfiability
of a certain class of constraints of AX diff .)
     We show that the universal theory AX diff has the amalgamation properties so that, by
Theorem 2.3, we are entitled to conclude that it admits quantifier-free interpolation. Recall
from Section 2.2 that a universal theory has the amalgamation property if two of its models
can be glued as substructures of a third model. Thus, we need to consider arbitrary models
of AX diff , not only the standard ones. This is why we need more insight into arbitrary
models of our theories and their relationship to standard ones.
     Let us choose an arbitrary model M of AX ext . We can build the standard model
std(M) such that INDEXstd(M) = INDEXM and ELEMstd(M) = ELEMM . To embed M into
std(M) is sufficient to associate with every a ∈ ARRAYM the function mapping i to rdM (a, i)
(this is an embedding because of the extensionality axiom). In this way, we can identify
ARRAYM with a subset of the set of all functions ARRAYstd(M) . If we call functional a model
M in which ARRAYM is a subset of the set of functions from INDEXM to ELEMM (and in
which rdM , wr M have the standard meaning), we have just shown that every model is
isomorphic to a functional one. (The argument extends to models of AX diff although—in
a standard model—the interpretation of diff is not fixed as the interpretations of rd and
wr.) In this respect, the crucial question is the following: which subsets of the set ARRAYM̄
10                         R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




in a standard model M̄ can be in the support ARRAYM of a functional model M (with
INDEXM = INDEXM̄ , ELEMM = ELEMM̄ ) that is a substructure of M̄? We shall answer the
question by using the notion of “closure under cardinality dependence,” that we formally
define next.
    Let a, b be elements of ARRAYM in a model M of AX diff . We say that a and b are
cardinality dependent (in symbols, M |= |a − b| < ω) iff {i ∈ INDEXM | M |= rd(a, i) 6=
rd(b, i)} is finite. Cardinality dependency is obviously an equivalence relation.
Lemma 3.1. Let N , M be models of AX diff such that M is a substructure of N . For
every a, b ∈ ARRAYM , we have that
                            M |= |a − b| < ω      iff   N |= |a − b| < ω.
Proof. The right-to-left side is trivial because if M |= |a−b| < ω then M |= a = wr(b, I, E),
where I ≡ i1 , . . . , in is a list of terms of sort INDEX, E ≡ e1 , . . . , en is a list of terms of
sort ELEM, and wr(b, I, E) abbreviates the term wr(wr(· · · wr(a, i1 , e1 ) · · · ), in , en ) (this and
similar notations will be discussed in more details in Section 4). Thus, also N |= a =
wr(b, I, E) because M is a substructure of N . Vice versa, suppose that M 6|= |a − b| < ω.
This means that there are infinitely many i ∈ INDEXM such that rdM (a, i) 6= rdM (b, i).
Since M is a substructure of N , there are also infinitely many i ∈ INDEXN such that
rdN (a, i) 6= rdN (b, i), i.e. N 6|= |a − b| < ω.
     We are now in the position to show how any functional model M of AX diff (i.e. up
to isomorphism, any model whatsoever) can be obtained from a standard one. In order to
produce any such M, it is sufficient to take a standard model M̄, to let INDEXM ≡ INDEXM̄ ,
ELEMM ≡ ELEMM̄ , and to let ARRAYM to be equal to any subset of ARRAYM̄ that is closed
under cardinality dependence, i.e. such that if a ∈ ARRAYM and M̄ |= |a − b| < ω, then b is
also in ARRAYM . In other words, functional substructures M of M̄ with INDEXM = INDEXM̄
and ELEMM = ELEMM̄ are in bijective correspondence with subsets of ARRAYM̄ closed under
cardinality dependence.
     A similar remark holds for embeddings. Suppose that µ : N −→ M is an embedding
that restricts to an inclusion INDEXN ⊆ INDEXM , ELEMN ⊆ ELEMM for M and N func-
tional models of AX diff . The action of the embedding µ on ARRAYN can be characterized
as follows: take an element a for each cardinality dependence equivalence class, extend
arbitrarily a to the set INDEXM \ INDEXN to produce µ(a) and then define µ(b) for non
representative b in the only possible way for wr to be preserved; i.e. if N |= b = wr(a, I, E)
for a representative a, let µ(b) be wr M (µ(a), I, E).
     By using the observation above, we are ready to show that AX diff has the amalgama-
tion property.
Theorem 3.2. The theory AX diff has the amalgamation property.
Proof. Take two embeddings µ0 : N −→ M0 and µ1 : N −→ M1 . As observed above,
we can suppose—w.l.o.g.—that N , M0 , M1 are functional models, that µ0 , µ1 restricts to
inclusions for the sorts INDEX and ELEM, and that (ELEMM0 \ELEMN )∩(ELEMM1 \ELEMN ) = ∅,
(INDEXM0 \INDEXN )∩(INDEXM1 \INDEXN ) = ∅. To simplify our task, we can also suppose—
again w.l.o.g.—that there exists some ei ∈ (ELEMMi \ ELEMN ) and some ji ∈ (INDEXMi \
INDEXN ) (i.e. that these sets are not empty), for i = 0, 1. (If this additional condition is
not satisfied, it is sufficient to enlarge M1 , M2 so that they satisfy it.) The amalgamated
model M will be the standard model over INDEXM0 ∪ INDEXM1 and ELEMM0 ∪ ELEMM1 . We
                  QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                             11




need to define νi : Mi −→ M (i = 0, 1) in such a way that ν0 ◦ µ0 = ν1 ◦ µ1 . The only
relevant point is the action of νi on ARRAYMi : as observed above, in order to define it, it is
sufficient to extend any a ∈ ARRAYMi to the indexes k ∈ (INDEXM1−i \ INDEXN ):
    (I) we let the value νi (a)(k) be ei in case there is no c such that Mi |= |a − µi (c)| < ω;
  (II) otherwise, we can do the following: take any such c such that Mi |= |a − µi (c)| < ω
          and put νi (a)(k) ≡ µ1−i (c)(k).
Because of Lemma 3.1 the choice of c in (II) above is immaterial. In fact, any other c′
differs from c only w.r.t. a finite set of indices in Mi . This also holds in N (by Lemma 3.1)
and thus we have N |= c′ = wr(c, I, E) for some I ⊆ INDEXN . The latter implies that
µ1−i (c) and µ1−i (c′ ) cannot differ at any k ∈ (ELEMM1−i \ ELEMN ). This guarantees that
ν1 ◦ µ 1 = ν2 ◦ µ 2 .
      In order to define diffM we can simply extend diffM1 ∪ diffM2 in such a way that
axiom 3.3 holds. More precisely, we define diffM (a, b) as follows: (i) if for some i = 0, 1,
we have that a = νi (a′ ) and b = νi (b′ ), then diffM (a, b) is taken to be diffMi (a′ , b′ ); (ii)
otherwise it is defined to be any i such that a(i) 6= b(i) (it is arbitrary whenever a = b).
For this definition of diffM to be correct, it is sufficient to show that
Claim: if a = ν0 (a0 ) = ν1 (a1 ), then there exists c such that a0 = µ0 (c) and a1 = µ1 (c).
To prove the claim, suppose that a = ν0 (a0 ) = ν1 (a1 ). Then ν0 (a0 ) and ν1 (a1 ) must have
been defined as in (II) above (otherwise they cannot coincide with each other at indexes
j0 , j1 ),3 which means that there exists ci such that for i = 0, 1 we have Mi |= |ai − µi (ci )| <
ω. Since ν0 (a0 ) = a = ν1 (a1 ), this means that ν0 (µ0 (c0 )) = ν1 (µ1 (c0 )) and a differ only at
finitely many indexes; the same is true for ν1 (µ1 (c1 )) and a, which in turns implies that
ν1 (µ1 (c0 )) and ν1 (µ1 (c1 )) differ only at finitely many indexes too. The same consequently
holds for c0 , c1 in N too, for µ0 (c0 ) and µ0 (c1 ) in M0 and for µ1 (c0 ) and µ1 (c1 ) in M1 .
Thus, since the choice of c in (II) is immaterial, we can suppose—w.l.o.g.—that c0 = c1
(let us use just c to name it). Then, by (II) applied to the definition of ν1 (a1 ), we have
that ν0 (µ0 (c)) = ν1 (µ1 (c)) and a = ν1 (a1 ) cannot differ at any k ∈ (ELEMM0 \ ELEMN ).
Similarly, ν0 (µ0 (c)) = ν1 (µ1 (c)) and a cannot differ at any k ∈ (ELEMM1 \ ELEMN ). Thus
a and ν0 (µ0 (c)) = ν1 (µ1 (c)) possibly differ only for k ∈ INDEXN and actually only for
finitely many such k. But a = ν0 (a0 ) = ν1 (a1 ), so the values of a at any k ∈ INDEXN
belongs ELEMM0 ∩ELEMM1 = ELEMN , which means that a is equal to wr M (ν0 (µ0 (c)), I, E) =
ν0 (µ0 (wr N (c, I, E))) for I ⊆ INDEXN and E ⊆ ELEMN . In conclusion, we have that a is
of the kind ν0 (µ0 (c̃)) = ν1 (µ1 (c̃)) and from a = ν0 (a0 ) = ν1 (a1 ), we get a0 = µ0 (c̃) and
a1 = µ1 (c̃) because ν0 , ν1 are injective.
     Before stating the main result of the paper which immediately follows from Theo-
rems 2.3 and 3.2, it is interesting to observe the following about the Claim used in the proof
of Theorem 3.2. The property mentioned in the Claim is known as strong amalgamability
property in Universal Algebra and is key to derive quantifier-free interpolation in combi-
nation of theories [19]. The fact that AX diff enjoys strong amalgamability is crucial to
transfer quantifier-free interpolation to combinations of AX diff with other important theo-
ries, like equality with uninterpreted symbols, difference logic, real arithmetic, appropriate
variants of integer linear arithmetic, etc. We refer the reader to [19] for details.
Theorem 3.3. The theory AX diff admits quantifier-free interpolation.
   3The Claim might be false in case INDEXM1 = INDEXN = INDEXM2 , this is the reason why we enlarged
INDEXM1 , INDEXM2 by adding the extra indexes j0 , j1 .
12                         R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




     We conclude this section with some observations concerning the theories AX ext and AX .
Lemma 3.1 holds also for the theory AX ext and the proof of Theorem 3.2 goes through also
for AX ext . However, according to Theorem 2.3 in Section 2.2, amalgamation alone is not
sufficient for establishing quantifier-free interpolation for theories like AX ext which are not
universal (for non universal theories one needs sub-amalgamability, not just amalgamability,
see [19]). Indeed, AX ext is amalgamable but does not admit quantifier-free interpolation.
     Despite being universal, AX is not amalgamable and thus it does not admit quantifier-
free interpolation. Indeed, the left-to-right implication of Lemma 3.1 does not hold for
AX as the arguments in the proof of Theorem 3.2. To get a formal counterexample to
the amalgamability of AX , consider the following situation. Let N be the AX -model in
which ELEMN and INDEXN are empty and ARRAYM contains two distinct elements, say a
and b. As already observed, empty supports must be taken into account when showing the
amalgamation property and, for AX , the axiom of extensionality needs not be satisfied.
Extend N to two standard models M1 and M2 , where ELEMM1 = {e, e′ }, INDEXM1 = {i}
and ELEMM2 = {d1 , d2 }, INDEXM2 = {j1 , j2 }. Then, embed N into M1 by letting a, b differ
at i (thus, e.g., M1 |= a = wr(b, i, e) ∧ rd(b, i) = e′ ) and embed N into M2 by letting a, b
differ at both j1 and j2 . Now, observe that amalgamation fails because we should have
       M |= a = wr(b, i, e) ∧ rd(a, j1 ) 6= rd(b, j1 ) ∧ rd(a, j2 ) 6= rd(b, j2 ) ∧ j1 6= j2
in any amalgamated model M and this is in contradiction with the two axioms of AX .

     4. Modular constraints for Arrays with diff and their combinations
Theorem 3.3 is proved by semantic arguments, hence it does not give an interpolation al-
gorithm; it only guarantees that, by enumerating quantifier free formulae, one can find
sooner or later the desired interpolant. In the rest of the paper, we develop (indepen-
dently of the results of Section 3) techniques based on rewriting and constraint solving to
construct an algorithm computing quantifier-free interpolants for conjunctions of ground lit-
erals in AX diff . Here, we introduce the notion of “modular constraint,” which is the main
data structure manipulated by the quantifier-free interpolation procedure and we prove two
key properties. First, we show that the satisfiability of modular constraints can be easily
detected (Lemma 4.3). Second, we prove that they can be combined in a modular way
(Proposition 4.5).
       Preliminarily, we introduce some notational conventions which are specific for con-
straints in the theory AX diff . We use a, b, . . . to denote free constants of sort ARRAY,
i, j, . . . for free constants of sort INDEX, and d, e, . . . for free constants of sort ELEM; α, β, . . .
stand for free constants of any sort. Below, we shall introduce non-ground rewriting rules
involving (universally quantified) variables of sort ARRAY: for these variables, we shall use
the symbols x, y, z, . . . . We make use of the following abbreviations.
 - [Nested write terms] By wr(a, I, E) we indicate a nested write on the array variable
    a, where indexes are represented by the free constants list I ≡ i1 , . . . , in and elements
    by the free constants list E ≡ e1 , . . . , en ; more precisely, wr(a, I, E) abbreviates the
    term wr(wr(· · · wr(a, i1 , e1 ) · · · ), in , en ). Notice that, whenever the notation wr(a, I, E)
    is used, the lists I and E must have the same length; for empty I, E, the term wr(a, I, E)
    conventionally stands for a.
                   QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                        13




    Refl     wr(a, I, E) = a ↔ rd(a, I) = E
             Proviso: Distinct(I)
 Symm        (wr(a, I, E) = b ∧ rd(a, I) = D) ↔ (wr(b, I, D) = a ∧ rd(b, I) = E)
             Proviso: Distinct(I)
  Trans      (a = wr(b, I, E) ∧ b = wr(c, J, D)) ↔ (a = wr(c, J · I, D · E) ∧ b = wr(c, J, D))
  Confl      b = wr(a, I · J, E · D) ∧ b = wr(a, I · H, E ′ · F ) ↔
             ↔ (b = wr(a, I, E) ∧ E = E ′ ∧ rd(a, J) = D ∧ rd(a, H) = F )
             Proviso: Distinct(I · J · H)
    Red      (a = wr(b, I, E) ∧ rd(b, ik ) = ek ) ↔ (a = wr(b, I −k, E −k) ∧ rd(b, ik ) = ek )
             Proviso: Distinct(I)
  Legenda: a and b are constants of sort ARRAY; I ≡ i1 , . . . , in , J ≡ j1 , . . . , jm and
  H ≡ h1 , . . . , hl are lists of constants of sort INDEX; E ≡ e1 , . . . , en , E ′ ≡ e′1 , . . . , e′n ,
  D ≡ d1 , . . . , dm , and F ≡ f1 , . . . , fl are lists of constants of sort ELEM.
                              Figure 1: Key properties of write terms

 - [Multiple read literals] Let a be a constant of sort ARRAY, I ≡ i1 , . . . , in and E ≡ e1 , . . . , en
   be lists of free constants of sort INDEX and ELEM, respectively; rd(a, I) = E abbreviates
   the formula rd(a, i1 ) = e1 ∧ · · · ∧ rd(a, in ) = en .
 - [Multiple equalities] If L ≡ α1 , . . . , αn and L′ V     ≡ α′1 , . . . , α′n are lists of constants of the
   same sort, by L = L we indicate the formula ni=1 αi = α′i .
                              ′

 - [Multiple distinctions] If L ≡ α1 , . . . , α       Vn is a list of constants of the same sort, by
   Distinct(L) we abbreviate the formula i6=j αi 6= αj .
 - [Juxtaposition and subtraction] If L ≡ α1 , . . . , αn and L′ ≡ α′1 , . . . , α′m are lists of con-
   stants, by L · L′ we indicate the list α1 , . . . , αn , α′1 , . . . , α′m ; for 1 ≤ k ≤ n, the list L − k
   is the list α1 , . . . , αk−1 , αk+1 , . . . , αn .
Some key properties of equalities involving write terms are stated in the following lemma
(see also Figure 1).
Lemma 4.1 (Key properties of write terms). The formulae in Figure 1 are all AX diff -valid
under the assumption that their provisoes - if any - hold (when we say that a formula φ is
AX diff -valid under the proviso π, we just mean that π ⊢AX diff φ).
Proof. The properties in Figure 1 are all straightforward to derive. Here, we just sketch the
proof of Transitivity, as an example: one side is by replacement of equals; for the-right-to-
left side, notice that the equalities a = wr(c, J · I, D · E) and b = wr(c, J, D) can be used
as rewrite rules to rewrite both members of a = wr(b, I, E) to the same term.


4.1. Modular constraints in AX diff . A (ground) flat literal is a literal of the form
a = wr(b, I, E), rd(a, i) = e, diff(a, b) = i, α = β, α 6= β. Notice that replacing a sub-term
t with a fresh constant α in a constraint A and adding the corresponding defining equation
α = t to A always produces an ∃-equivalent constraint; by repeatedly applying this method,
one can show that every constraint is ∃-equivalent to a flat constraint, i.e., to one containing
only flat literals. We split a flat constraint A into two parts, the index part AI and the
main part AM : AI contains the literals of the form i = j, i 6= j, diff(a, b) = i, whereas AM
contains the remaining literals, i.e., those of the form a = wr(b, I, E), a 6= b, rd(a, i) = e, e =
d, e 6= d (atoms a = b are identified with literals a = wr(b, ∅, ∅)). We write A =< AI , AM >
14                          R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




to indicate the two parts of the constraint A. In the main part of a constraint, positive
literals will be treated as rewrite rules; to get a suitable orientation, we use a lexicographic
path ordering with a total precedence > such that a > wr > rd > diff > i > e, for all
a, i, e of the corresponding sorts. This choice orients equalities a = wr(b, I, E) from left to
right when a > b; equalities like a = wr(b, I, E) for a < b or a ≡ b will be called badly
orientable equalities.
Definition 4.2. A constraint A =< AI , AM > is said to be modular iff it is flat and the
                                            ˜ Ẽ be the sets of free constants of sort INDEX and
following conditions are satisfied (we let I,
ELEM occurring in A):
 (o) no positive index literal i = j occurs in AI ;
  (i) no negative array literal a 6= b occurs in AM ;
 (ii) AM does not contain badly orientable equalities;
(iii) the rewriting system AR given by the oriented positive literals of AM joined with the
    rewriting rules
                       rd(wr(x, i, e), j) → rd(x, j)                   ˜ e ∈ Ẽ, i 6≡ j
                                                            for i, j ∈ I,                   (4.1)
                                 rd(wr(x, i, e), i) → e                       ˜ e ∈ Ẽ
                                                                      for i ∈ I,                   (4.2)
          wr(wr(x, i, e), j, d) → wr(wr(x, j, d), i, e)                    ˜ e, d ∈ Ẽ, i > j
                                                               for i, j ∈ I,                       (4.3)
                   wr(wr(x, i, e), i, d) → wr(x, i, d).                     ˜ e, d ∈ Ẽ
                                                                    for i ∈ I,                     (4.4)
   is confluent and ground irreducible;4
(iv) if a = wr(b, I, E) ∈ AM and i, e are in the same position in the lists I, E, respectively,
   then rd(b, i) 6↓AR e;
 (v) {diff(a, b) = i, diff(a′ , b′ ) = i′ } ⊆ AI and a ↓AR a′ and b ↓AR b′ imply i ≡ i′ ;
(vi) diff(a, b) = i ∈ AI and rd(a, i) ↓AR rd(b, i) imply a ↓AR b.
     Condition (o) means that the index constants occurring in a modular constraint are
implicitly assumed to denote distinct objects. This is supported also by the statement of
Lemma 4.3 below, from which, it is evident that the addition of all the negative literals i 6= j
            ˜ with i 6≡ j) does not compromise the satisfiability of a modular constraint,
(for i, j ∈ I,
precisely because such negative literals are implicitly (already) part of the constraint. In
Condition (i), negative array literals a 6= b are not allowed because they can be replaced by
suitable literals involving fresh constants and the diff operation (see axiom (3.3)). Rules
(4.1) and (4.2) mentioned in condition (iii) reduce read-over-writes and rules (4.3) and
(4.4) sort indexes in flat terms wr(a, I, E) in ascending order. In addition, condition (iv)
prevents further redundancies in our rules. Finally, conditions (v) and (vi) deal with diff.
In particular, (v) says that diff is “well defined” and (vi) is a “conditional” translation of
the contraposition of axiom (3.3).
     The non-ground rules from Definition 4.2(iii) form a convergent rewrite system (critical
pairs are confluent): this can be checked manually (and can be confirmed also by tools like
     4The latter means that no rule can be used to reduce the left-hand or the right-hand side of another
ground rule. Notice that ground rules from AR are precisely the rules obtained by orienting an equality
from AM (rules (4.1)-(4.4) are not ground as they contain one variable, namely the array variable x).
                 QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                           15




SPASS or MAUDE). Ground rules from AR are of the form
                                          a → wr(b, I, E),                                 (4.5)
                                           rd(a, i) → e,                                   (4.6)
                                              e → d.                                       (4.7)
Only rules of the form (4.7) can overlap with the non-ground rules (4.1)-(4.4), but the
resulting critical pairs are trivially confluent. Thus, in order to check confluence of AM , only
overlaps between ground rules (4.5)-(4.7) need to be considered (this is the main advantage
of our choice to orient equalities a = wr(b, I, E) from left to right instead of right to left).
Lemma 4.3. Suppose that A is modular. Then A is AX diff -satisfiable iff there is no
element inequality e 6= d in AM such that e ↓AR d. Moreover, A is AX diff -satisfiable iff
                                                ˜ i 6≡ j} ∪ {α 6= β}α,β
                           A ∪ {i 6= j | i, j ∈ I,
(varying α, β among the different pairs of element and array constants in normal form
occurring in A) is AX diff -satisfiable.
Proof. Clearly, the satisfiability of A implies that for no negative index literal e 6= d from
AM , we have that e ↓AR d. Assume conversely that this is the case: our aim is to build a
model for A ∪ {α 6= β}α,β ∪ {i 6= j}i,j (varying α, β and i, j as indicated in the statement
of the Lemma). We can freely make the following further assumption: if a, i occur in A
and a is in normal form, there is some e such that rd(a, i) = e belongs to A (in fact, if this
does not hold, it is sufficient to add a further equality rd(a, i) = e - with fresh e - without
destroying the modular property of the constraint).
    Let I ∗ be the set of constants of sort INDEX occurring in A and let E ∗ be the set of
constants of sort ELEM in normal form occurring in A (we have I ∗ = I˜ and E ∗ ⊆ Ẽ). Finally,
we let X be the set of free constants of sort ARRAY occurring in A which are in normal form.
    We build a model M as follows (the symbol + denotes disjoint union):
• INDEXM ≡ I ∗ + {∗};
• ELEMM ≡ E ∗ + X;
• ARRAYM is the set of total functions from INDEXM to ELEMM , rdM and wr M are the
  standard read and write operations (i.e. rdM is function application and wr M is the
  operation of modifying the first argument function by giving it the third argument as a
  value for the second argument input);5
• for a constant i of sort INDEX, iM ≡ i for all i ∈ I ∗ ;
• for a constant e of sort ELEM, eM is the normal form of e;
• for a constant a of sort ARRAY in normal form and i ∈ I ∗ , we put aM (i) to be equal to
  the normal form of rd(a, i) (this is some e ∈ ELEMM by our further assumption above);
  we also put aM (∗) ≡ a (notice that ELEMM ≡ E ∗ + X, hence a ∈ ELEMM ).
• for a constant a of sort ARRAY not in normal form, let wr(c, I, E) be the normal form of a:
  we let aM to be equal to wr M (cM , I M , E M ) (This definition is correct because a and c
  cannot coincide; in fact, since a < wr(a, I, E), the term wr(a, I, E) cannot be the normal
  form of a.)
• we shall define diffM later on.
   5In the terminology used in Section 3.1, this means that M is a standard model.
16                        R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




It is clear that in this way we have that all constants α of sort ELEM or ARRAY are interpreted
in such a way that, if α̂ is the normal form of α, then
                                           αM = α̂M .                                         (4.8)
Also notice that, by the definition of aM , if e is the normal form of rd(a, i), then we have
                                         rd(a, i)M = eM                                       (4.9)
in any case (whether a is in normal form or not). Finally, if wr(c, I, E) is the normal form
of a, then
                             aM = cM ⇒ (I = ∅ and E = ∅);                                   (4.10)
this is because the only rule that can reduce a must have a as left-hand side and wr(c, I, E)
as right-hand side (rules are ground irreducible), thus in the rule a → wr(c, I, E) ∈ AM we
must have I = ∅, E = ∅ in case aM = cM (recall Definition 4.2(iv)). In more details, sup-
pose that I and E are not empty and take i ∈ I and e ∈ E in corresponding positions. We
have that rd(c, i)M = rdM (cM , iM ) = cM (iM ) = aM (iM ) = rdM (aM , iM ) = rd(a, i)M
(we used the definition of interpretation of a ground term, the fact that rdM is interpreted
as functional application and that aM = cM ). Now, since rd(a, i) normalizes to e, apply-
ing (4.9), we get that rd(c, i)M = eM , which means, again by (4.9), that rd(c, i) normalizes
to e too (e is in normal form, thus if ẽ is the normal form of rd(c, i), we have that ẽM = eM
implies e ≡ ẽ). This is contrary to Definition 4.2(iv).
     Since A is modular, literals in A are flat. It is clear that all negative literals from A are
true: in fact, a modular constraint does not contain inequalities between array constants,
inequalities between index constants are true by construction and inequalities between ele-
ment constants are true by the hypothesis of the Lemma. Also, if α, β are either element
or array constants in normal form, we have αM 6= β M by construction (in particular, the
interpretation of different array constants both in normal form differ at index ∗). Let us
now consider positive literals in A: those from AM are equalities of terms of sort ELEM or
ARRAY and consequently are of the kind
                           e = d,      a = wr(c, I, E),    rd(a, i) = e.
Since ground rules are irreducible, d is the normal form of e and wr(c, I, E) is the normal
form of a, hence we have eM = dM and aM = wr(c, I, E)M by (4.8) above. For the
same reason a and e are in normal form in rd(a, i) = e, hence rd(a, i)M = eM follows by
construction.
     It remains to define diffM in such a way that flat literals diff(a, b) = i from AI are
true and the axiom (3.3) is satisfied. Before doing that, let us observe that for all free
constants a, b occurring in A, we have that aM = bM is equivalent to a ↓AR b. In fact, one
side is by (4.8); for the other side, suppose that aM = bM and that wr(c, I, E), wr(c′ , I ′ , E ′ )
are the normal forms of a and b, respectively. Then c must be equal to c′ , otherwise aM and
bM would differ at index ∗. If either a or b is equal to c, trivially a ↓AR b follows from (4.10).
Otherwise, a and b are both reducible in AR and since ground rules are irreducible and the
only rules that can reduce an array constant have the left-hand side equal to that array
constant, we have that a → wr(c, I, E) and b → wr(c, I ′ , E ′ ) are both rules in AR : as such,
they are subject to Condition (iv) from Definition 4.2. First observe that we must have
that I ≡ I ′ : otherwise, if there is i ∈ I \ I ′ , we could infer the following: (i) by (4.8),
bM (i) = cM (i); (ii) cM (i) is the normal form of rd(c, i) by construction; (iii) by aM = bM ,
cM (i) is also equal to the normal form of the e having in the list E the same position as i in
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                             17




the list I, contrary to Condition (iv) from Definition 4.2. Since terms are normalized with
respect to rule (4.3), I and I ′ coincide not only as sets, but also as lists; this means that the
lists E and E ′ coincide too (the terms wr(c, I, E), wr(c, I, E ′ ) are in normal form and we
have wr(c, I, E)M = wr(c, I, E ′ )M ). In more details, let i, e, ẽ be in the k-th positions in
the lists I, E, E ′ , respectively. From wr(c, I, E)M = wr(c, I, E ′ )M , applying rdM (−, iM ),
we get eM = ẽM , i.e. e ↓AR ẽ, which means e ≡ ẽ because wr(c, I, E), wr(c, I, E ′ ) are in
normal form (in particular, their sub-terms e, ẽ are not reducible). In conclusion, a ↓AR b
holds.
     Among the elements of ARRAYM , some of them are of the kind aM for some free constant
a of sort ARRAY occurring in A and some are not of this kind: we call the former ‘definable’
arrays. In principle, it could be that aM = bM for different a, b, but we have shown that
this is possible only when a and b have the same normal form.
     We are ready to define diffM : we must assign a value diffM (a, b) to all pairs of arrays
a, b ∈ ARRAYM . If a or b is not definable or if there are no a, b defining them such that
diff(a, b) occurs in AI , we can easily find diffM (a, b) so that axiom (3.3) is true for a, b:
one picks an index where they differ if they are not identical, otherwise the definition can be
arbitrary. So let us concentrate into the case in which a, b are defined by constants a, b such
that the literal diff(a, b) = i occurs in AI : in this case, we define diffM (aM , bM ) to be i:
Condition (v) from Definition 4.2 (together with the above observation that two constants
defining the same array in M must have an identical normal form) ensures that the definition
is correct and that all literals diff(a, b) = i ∈ AI becomes true. Finally, axiom (3.3) is
satisfied by Condition (vi) from Definition 4.2 and the fact that rd(a, i)M = rd(b, i)M is
equivalent to rd(a, i) ↓AR rd(b, i) (to see the latter, just recall (4.9)).
Remark 4.4. As we said, the importance of Definition 4.2 lies in Lemma 4.3 and in
Proposition 4.5 below. On the other hand, it is not true that if A is modular, then A entails
(modulo AX diff ) a positive literal t = v iff t ↓AR v, even in case t, v are ground flat terms.
As a counterexample, consider A = {rd(a, i) → e}; we have A ⊢AX diff a = wr(a, i, e) but
a 6↓AR wr(a, i, e). However, the proof of Lemma 4.3 shows that the following weaker—but
still important—property holds: if A is modular and t, v are terms of the same sort occurring
in A, then A ⊢AX diff t = v iff t ↓AR v. This may look unusual, however recall that our
aim is not to decide equality by normalization but to have algorithms for satisfiability and
interpolation.


4.2. Combining modular constraints. Let A, B be two constraints in the signatures
ΣA , ΣB obtained from the signature Σ by adding some free constants and let ΣC ≡ ΣA ∩ΣB .
Given a term, a literal or a formula ϕ we call it:
• AB-common iff it is defined over ΣC ;
• A-local (resp. B-local) if it is defined over ΣA (resp. ΣB );
• A-strict (resp. B-strict) iff it is A-local (resp. B-local) but not AB-common;
• AB-mixed if it contains symbols in both (ΣA \ ΣC ) and (ΣB \ ΣC );
• AB-pure if it does not contain symbols in both (ΣA \ ΣC ) and (ΣB \ ΣC ).
(Notice that, sometimes in the literature about interpolation, “A-local” and “B-local” are
used to denote what we call here “A-strict” and “B-strict”). The following modularity
result is crucial to justify our interpolation algorithm for AX diff .
18                       R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




Proposition 4.5. Let A = hAI , AM i and B = hBI , BM i be constraints in expanded signa-
tures ΣA , ΣB as above (here Σ is the signature of AX diff ); let A, B be both consistent and
modular. Then A ∪ B is consistent and modular, in case all the following conditions hold:
 (O) an AB-common literal belongs to A iff it belongs to B;
  (I) every rewrite rule in AM ∪ BM whose left-hand side is AB-common has also an AB-
   common right-hand side;
 (II) if a, b are both AB-common and diff(a, b) = i ∈ AI ∪ BI , then i is AB-common too;
(III) if a rewrite rule of the kind a → wr(c, I, E) is in AM ∪ BM and the term wr(c, I, E)
   is AB-common, so is the constant a.
Proof. Since we cannot rewrite AB-common terms to terms which are not, it is easy to
see that AM ∪ BM is still convergent and ground irreducible; the other conditions from
Definition 4.2 are trivial, except condition (v). The latter is guaranteed by the hypotheses
(II)-(III) as follows: the relevant case is when, say diff(a, b) = i ∈ AI is A-local and
diff(a′ , b′ ) = i′ ∈ BI is B-local. If a ↓ a′ , since AM and BM are ground irreducible, we
have that a single rewrite step reduces both a and a′ to their normal form, that is we have
                                     a → wr(c, I, E) ← a′ .
Now wr(c, I, E) is AB-common, because the rules a → wr(c, I, E), a′ → wr(c, I, E) are in
AM and in BM , respectively. By hypothesis (III), we have that a and a′ are AB-common
too; the same applies to b, b′ and hence to i, i′ by (II). Thus diff(a′ , b′ ) = i′ is AB-common
and belongs to AI , hence i ≡ i′ because A is modular.
    Since all conditions from Definition 4.2 are satisfied, A ∪ B is modular. Lemma 4.3
applies, thus yielding consistency.
     The above proof is so easy mainly because ground rewrite rules cannot superpose with
the non ground rewrite rules (4.1)-(4.4) (with the exception of the rewrite rules e → d, that
may superpose but with trivially confluent critical pairs): this is the main benefit of our
choice of orienting equalities a = wr(b, I, E) from left-to-right (and not from right-to-left).
     We conclude this section with a remark about the combination of modular constraints
in AX diff with constraints in other theories. The theory AX diff is stably infinite (in all
its sorts) but non-convex: this means that it is suitable for Nelson-Oppen combination, but
that disjunctions of equalities (not just equalities) need to be propagated from an AX diff -
constraint, in case it is involved in a combined problem. Actually, this does not happen
for modular constraints, as it is shown by the statement of Lemma 4.3. In other words,
no disjunction of equalities needs to be propagated from a modular constraint A and only
equalities that can be syntactically extracted from A need to be propagated.

                           5. A Solver for Arrays with diff
The first step towards the quantifier-free interpolation procedure for AX diff is the design
of a satisfiability solver. Although a solver for this theory can be easily derived from
existing solvers for AX or AX ext , we need a specific algorithm from which interpolants
can be extracted. To do this, Lemma 4.3 will play an important role by allowing for the
design of ∃-equivalence preserving transformations that, once successively applied to a given
constraint A, will bring it to a consistent modular constraint (if possible). Failure of applying
these transformations implies that A is unsatisfiable. In other words, the ∃-equivalence
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                           19




preserving transformations will determine whether a finite constraint A is satisfiable or not
by transforming it into a modular ∃-equivalent constraint.
     One of the key design choice underlying our transformations is to separate the “index”
part, that will be handled by guessing, of a constraint from the “array” and “elem” parts,
that will be subject to rewriting. Another important design decision is to distinguish a
preprocessing and a completion phase. In the preprocessing phase, besides flattening (see,
e.g., [2]) and similar operations, a complete guessing of equalities/inequalities among index
constants will be performed. Indeed, this guessing will be realized by backtracking: if
the completion phase will terminate in a failure, another guessing has to be tried and
unsatisfiability can only be declared when all guessing fail. The completion phase will
guarantee the confluence of the current rewriting system AR , recall Definition 4.2. The
confluence of AR is the main requirement for a constraint to be modular.

5.1. Preprocessing. The preprocessing phase consists of the following sequential steps
applied to our initial constraint A:
 Step 1 Flatten A, by replacing sub-terms with fresh constants and by adding the related
   defining equalities.
 Step 2 Replace array inequalities a 6= b by the following literals (i, e, d are fresh)
                    diff(a, b) = i,   rd(b, i) = e,   rd(a, i) = d,   d 6= e.
 Step 3 Guess a partition of index constants, i.e., for any pair of indexes i, j add either
   i = j or i 6= j (but not both of them); then remove the positive literals i = j by replacing
   i by j everywhere (if i > j according to the symbol precedence, otherwise replace j by
   i); if an inconsistent literal i 6= i is produced, try with another guess (and if all guesses
   fail, report unsat).
 Step 4 For all a, i such that rd(a, i) = e does not occur in the constraint, add such a literal
   rd(a, i) = e with fresh e.
At the end of the preprocessing phase, we get a finite set of flat constraints; the disjunction
of these constraints is ∃-equivalent to the original constraint. For each of these constraints,
go to the completion phase: if the transformations below can be exhaustively applied (without
failure) to at least one of the constraints, report sat, otherwise report unsat. Failure can
be caused by instructions (V) below.
     The reason for inserting Step 4 above is just to simplify Orientation and Gaussian
completion below. Notice that, even if rules rd(a, i) → e can be removed during completion,
the following invariant is maintained: terms rd(a, i) always reduce to constants of sort
ELEM.

5.2. Completion. The completion phase consists in various transformations that should
be non-deterministically executed until no rule or a failure instruction applies. For clarity,
we divide the transformations into five groups.
(I) Orientation. This group contains a single instruction: get rid of badly orientable
equalities, by using the equivalences Reflexivity and Symmetry of Figure 1; a badly ori-
entable equality a = wr(b, I, E) (with a < b), after normalization of the term wr(b, I, E)
with respect to the non-grund rules (4.3) − (4.4), is replaced by an equality of the form
b = wr(a, I, D) and by the equalities rd(a, I) = E (all “read literals” required by the
20                          R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




left-hand side of Symm comes from the above invariant). A badly orientable equality
a = wr(a, I, E) is removed and replaced by read literals only (or by nothing if I, E are
empty).
(II) Gaussian completion. We now take care of the confluence of AR (i.e., point (iii)
of Definition 4.2). To this end, we consider all the critical pairs that may arise among our
rewriting rules (4.5)-(4.7) (recall that there is no need to examine overlaps involving the non
ground rules (4.1)-(4.4)). To treat the relevant critical pairs, we combine standard Knuth-
Bendix completion for congruence closure with a specific method (“Gaussian completion”)
based on equivalences Symmetry, Transitivity and Conflict of Figure 1. The critical pairs
are listed below. Two preliminary observations are in order. First, we normalize a critical
pair by using →∗ before recovering convergence by adding a suitably oriented equality and
removing the parent equalities (the symbol →∗ denotes the reflexive and transitive closure
of the rewrite relation → induced by the rewrite rules AR ∪ {(4.1) − (4.4)}). Second, the
provisos of all the equivalences in Figure 1 used below (i.e., Symm, Trans, and Confl) are
satisfied because of the pre-processing Step 3 above.
(C1): wr(b1 , I1 , E1 ) ∗← wr(b′1 , I1′ , E1′ ) ← a → wr(b′2 , I2′ , E2′ ) →∗ wr(b2 , I2 , E2 )
     with b1 > b2 . We proceed in two steps. First, we use Symm (from right to left) to
     replace the parent rule a → wr(b′1 , I1′ , E1′ ) with
                                wr(a, I1 , F ) = b1 ∧ rd(a, I1 ) = E1
     for a suitable list F of constants of sort ELEM (notice that the equalities rd(b1 , I1 ) = F ,
     which are required to apply Symm, are already available because terms of the form
     rd(b1 , j) for j in I1 always reduce to constants of sort ELEM by the invariant resulting
     from the application of Step 4 in the pre-processing phase). Then, we apply Trans to
     the previously derived equality b1 = wr(a, I1 , F ) and to the normalized second equality
     of the critical pair (i.e., a = wr(b2 , I2 , E2 )) and we derive
                        b1 = wr(b2 , I2 · I1 , E2 · F ) ∧ a = wr(b2 , I2 , E2 ).                  (5.1)
     Hence, we are entitled to replace b1 = wr(a, I1 , F ) with the rule b1 → wr(b2 , J, D), where
     J and D are lists obtained by normalizing the right-hand-side of the first equality of (5.1)
     with respect to the non-ground rules (4.3) and (4.4). To summarize: the parent rules are
     removed and replaced by the rules
                               b1 → wr(b2 , J, D),      a → wr(b2 , I2 , E2 )
  and a bunch of new equalities of the form rd(a, i) = e, giving rise, in turn, to rules of the
  form rd(b2 , i) → e or to rewrite rules of the form (4.7) after normalization of their left
  members (normalization of terms rd(a, i) is indeed needed for the termination argument
  of Theorem 5.1 below to work).
(C2): wr(b, I1 , E1 ) ∗← wr(b′1 , I1′ , E1′ ) ← a → wr(b′2 , I2′ , E2′ ) →∗ wr(b, I2 , E2 )
     Since identities like wr(c, H, G) = wr(c, π(H), π(G)) are AX diff -valid for every permu-
     tation π (under the proviso Distinct(H)), it is harmless to suppose that the set of index
     variables I ≡ I1 ∩ I2 coincides with the common prefix of the lists I1 and I2 ; hence we
     have I1 ≡ I · J and I2 ≡ I · H for suitable disjoint lists J and H. Then, let E and E ′ be
     the prefixes of E1 and E2 , respectively, of length equal to that of I; and let E1 ≡ E · D
     and E2 ≡ E ′ · F for suitable lists D and F . At this point, we can apply Confl to replace
                 QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                             21




  both parent rules forming the critical pair with
                a = wr(b, I, E) ∧ E = E ′ ∧ rd(b, J) = D ∧ rd(b, H) = F,
   where the first equality is oriented from left to right (i.e., a → wr(b, I, E)).
(III) Knuth-Bendix completion. The remaining critical pairs are treated by standard
completion methods for congruence closure.
(C3): d ∗← rd(wr(b, I, E), i) ← rd(a, i) → e′ →∗ e
  Remove the parent rule rd(a, i) → e′ and, depending on whether d > e, e > d, or d ≡ e,
  add the rule d → e, e → d, or do nothing. (Notice that terms of the form rd(b, j) are
  always reducible because of the invariant of Step 4 in the pre-processing phase; hence,
  rd(wr(b, I, E), i) always reduces to some constant of sort ELEM.)
(C4): e ∗← e′ ← rd(a, i) → d′ →∗ d
  Orient the critical pair (if e and d are not identical), add it as a new rule and remove
  one parent rule.
(C5): d ∗← d′ ← e → d′1 →∗ d1
  Orient the critical pair (if d and d1 are not identical), add it as a new rule and remove
  one parent rule.
(IV) Reduction. The instructions in this group simplify the current rewrite rules.
(R1): If the right-hand side of a current ground rewrite rule can be reduced, reduce it as
  much as possible, remove the old rule, and replace it with the newly obtained reduced
  rule. Redundant equalities like t = t are also removed.
(R2): For every rule a → wr(b, I, E) ∈ AM , after normalization of the term wr(b, I, E) with
  respect to the non-grund rules (4.3) − (4.4), exhaustively apply Reduction in Figure 1
  from left to right (this amounts to do the following: if there are i, e in the same position k
  in the lists I, E such that rd(b, i) ↓AR e, replace a = wr(b, I, E) with a = wr(b, I−k, E−k)).
(R3): If diff(a, b) = i ∈ AI , rd(a, i) ↓AR rd(b, i) and a > b, add the rule a → b; replace
  also diff(a, b) = i by diff(b, b) = i (this is needed for termination, it prevents the rule
  for being indefinitely applied).
(V) Failure. The instructions in this group aim at detecting inconsistency.
(U1): If for some negative literal e 6= d ∈ AM we have e ↓AR d, report failure and
  backtrack to Step 3 of the pre-processing phase.
(U2): If {diff(a, b) = i, diff(a′ , b′ ) = i′ } ⊆ AI and a ↓AR a′ and b ↓AR b′ for i 6≡ i′ , report
  failure and backtrack to Step 3 of the pre-processing phase.
Notice that the instructions in the last two groups may require a confluence test α ↓AR β
that can be effectively performed in case the instructions from groups (II)-(III) have been
exhaustively applied, because then all critical pairs have been examined and the rewrite
system AR is confluent. If this is not the case, one may pragmatically compute and compare
any normal form of α and β, keeping in mind that the test has to be repeated when all
completion instructions (II)-(III) have been exhaustively applied.
Theorem 5.1. The above procedure decides constraint satisfiability in AX diff .
Proof. Correctness and completeness of the solver are clear: since all steps and instructions
from Section 5 manipulate the constraint up to ∃-equivalence, it follows that if all guessings
originated by Step 3 fail, the input constraint is unsatisfiable and, if one of them succeed,
22                         R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




the exhaustive application of the completion instructions leads to a modular constraint
which is satisfiable by Lemma 4.3.
    We must only consider termination; to show that any sequence of our instructions
terminates, we use a standard technique. With every positive literal l = r we associate
the multi-set of terms {l, r}; with every negative literal l 6= r, we associate the multi-set
of terms {l, l, r, r}. Finally, with a constraint A we associate the multi-set M (A) of the
multi-sets associated with every literal from A. Now it is easy to see that such multi-set
decreases after the application of any instruction.
    The termination analysis in the proof of Theorem 5.1 can be refined so as to show that
our algorithm is in NP, which is optimal because satisfiability of quantifier free formulae in
AX ext is already NP-complete [10].

               6. The Interpolation Algorithm for Arrays with diff
In the literature one can roughly distinguish two approaches to the problem of computing
interpolants. In the former (see e.g. [11, 47]), an interpolating calculus is obtained from
a standard calculus by adding decorations so as to enable the recursive construction of
an interpolating formula from a proof; in the latter (see, e.g., [22, 28, 56]), the focus is on
how to extend an available decision procedure to return interpolants. Our methodology is
similar to the second approach, since we add the capability of computing interpolants to
the satisfiability procedure in Section 5. However, we do this by designing a flexible and
abstract framework, relying on the identification of basic operations that can be performed
independently from the method used by the underlying satisfiability procedure to derive a
refutation.

6.1. Interpolating Metarules. Let now A, B be constraints in signatures ΣA , ΣB ex-
panded with free constants and ΣC ≡ ΣA ∩ ΣB ; we shall refer to the definitions of AB-
common, A-local, B-local, A-strict, B-strict, AB-mixed, AB-pure terms, literals and for-
mulae given in Section 4. Our goal is to produce, in case A ∧ B is AX diff -unsatisfiable, a
ground AB-common sentence φ such that A ⊢AX diff φ and φ ∧ B is AX diff -unsatisfiable.
     Let us examine some of the transformations to be applied to A, B. Suppose for instance
that the literal ψ is AB-common and such that A ⊢AX diff ψ; then we can transform B into
B ′ ≡ B ∪ {ψ}. Suppose now that we got an interpolant φ for the pair A, B ′ : clearly,
we can derive an interpolant for the original pair A, B by taking φ ∧ ψ. The idea is to
collect some useful transformations of this kind. Notice that these transformations can also
modify the signatures ΣA , ΣB , in the sense that the signature of the pair A′ , B ′ obtained
after applying a single transformation to a pair A, B might be different from the signature
of A, B (typically, the signature of A′ , B ′ may contain extra fresh constants). For instance,
suppose that t is an AB-common term and that c is a fresh constant; then we can put
A′ ≡ A∪{c = t}, B ′ ≡ B ∪{c = t}: in fact, if φ is an interpolant for A′ , B ′ , then φ(t/c) is an
interpolant for A, B. (Notice that the fresh constant c is now a shared symbol, because ΣA is
enlarged to ΣA ∪{c}, ΣB is enlarged to ΣB ∪{c} and hence (ΣA ∪{c})∩(ΣB ∪{c}) = ΣC ∪{c}.)
The transformations we need are called metarules and are listed in Table 1 below (in the
Table and more generally in this Subsection, we use the notation φ ⊢ ψ for φ ⊢AX diff ψ).6
   6Rules Redplus1, Redplus2 can be seen as instances of Rules Disjunction1, Disjunction2 (for n = 1),
thus they are redundant. In Rule Propagate1, one can change the proviso to the weaker requirement ‘ψ ∈ A
                 QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                              23




    An interpolating metarules refutation for A, B is a labelled tree having the following
properties: (i) nodes are labelled by pairs of finite sets of constraints; (ii) the root is labelled
by A, B; (iii) the leaves are labelled by a pair A, B such that ⊥ ∈ A ∪ B; (iv) each non-leaf
node is the conclusion of a rule from Table 1 and its successors are the premises of that rule.
The crucial properties of the metarules are summarized in the following two Propositions.
Proposition 6.1. The unary metarules AA′ || B
                                            B
                                              ′ from Table 1 have the property that A ∧ B

is ∃-equivalent to A′ ∧ B ′ ; similarly, the n-ary metarules A1 | B1A ···| BAn | Bn from Table 1
                                                  W
have the property that A ∧ B is ∃-equivalent to nk=1 (Ak ∧ Bk ).
Proposition 6.2. If there exists an interpolating metarules refutation for A, B then there
is a quantifier-free interpolant for A, B (namely there exists a quantifier-free AB-common
sentence φ such that A ⊢ φ and B ∧ φ ⊢ ⊥). The interpolant φ is recursively computed
applying the relevant interpolating instructions from Table 1.
     The proofs of both Propositions 6.1 and 6.2 are straightforward. The following obser-
vations are the basis of such proofs. The metarules are applied bottom-up whereas inter-
polants are computed (from an interpolating refutation) in a top-down manner. We should
have labelled nodes in an interpolating metarules refutation by 4-tuples (ΣA , A, ΣB , B),
where ΣA , ΣB are signatures expanded with free constants, A is a ΣA -constraint and B is
a ΣB -constraint. The shared signature of the node labelled (ΣA , A, ΣB , B) (i.e. the signa-
ture where interpolants are recursively computed) is taken to be ΣC ≡ ΣA ∩ ΣB ; the root
signature pair is the pair of signatures comprising all symbols occurring in the original pair
of constraints. We did not make all this explicit in order to avoid notation overhead. No-
tice that the only metarules that modify the signatures are (Define0), (Define1), (Define2)
(which add a to ΣA ∩ ΣB , ΣA , ΣB , respectively). Some other rules like (ConstElim0), (Con-
stElim1), (ConstElim2) could in principle restrict the signature, but signature restriction
is not relevant for the computation of interpolants: there is no need that all AB-common
symbols occur in the interpolants, but we certainly do not want extra symbols to occur in
them, so only bottom-up signature expansion must be tracked.

6.2. The Interpolating Solver. The metarules are complete, i.e. if A ∧ B is AX diff -
unsatisfiable, then (since we know that an interpolant exists) a single application of (Prop-
agate1) and (Close2) gives an interpolating metarules refutation. This observation shows
that metarules are by no means better than the brute force enumeration of formulae to
find interpolants. However, metarules are useful to design an algorithm manipulating pairs
of constraints based on transformation instructions. In fact, each of the transformation
instructions can be justified by a metarule (or by a sequence of metarules): in this way, if
our instructions form a complete and terminating algorithm, we can use Proposition 6.2 to
get the desired interpolants. The main advantage of using metarules as justifications is that
we just need to take care of the completeness and termination of the algorithm, and not
about interpolants anymore. Here “completeness” means that our transformations should
be able to bring a pair (A, B) of constraints into a pair (A′ , B ′ ) that either matches the
requirements of Proposition 4.5 or is explicitly inconsistent, in the sense that ⊥ ∈ A′ ∪ B ′ .
and ψ is AB-common’ (the case A ⊢ ψ could be obtained by applying Redplus1); a similar observation
applies to Propagate2. We thank an anonymous referee for these remarks.
24                                R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




               Close1                             Close2                        Propagate1                          Propagate2

                                                                                A | B ∪ {ψ}                         A ∪ {ψ} | B
                 A|B                               A|B                             A|B                                 A|B

      Prv.:      A is unsat.             Prv.:     B is unsat.             Prv.: A ⊢ ψ and                     Prv.: B ⊢ ψ and
      Int.:      φ′ ≡ ⊥.                 Int.:     φ′ ≡ ⊤.                       ψ is AB-common.                     ψ is AB-common.
                                                                           Int.: φ′ ≡ φ ∧ ψ.                   Int.: φ′ ≡ ψ → φ.

                   Define0                                       Define1                                       Define2

      A ∪ {a = t} | B ∪ {a = t}                             A ∪ {a = t} | B                                A | B ∪ {a = t}
               A|B                                               A|B                                            A|B

     Prv.: t is AB-common, a fresh.                Prv.: t is A-local and a is fresh.              Prv.:   t is B-local and a is fresh.
     Int.: φ′ ≡ φ(t/a).                            Int.: φ′ ≡ φ.                                   Int.:   φ′ ≡ φ.

                           Disjunction1                                                           Disjunction2

                      · · · A ∪ {ψk } | B · · ·                                               · · · A | B ∪ {ψk } · · ·
                                A|B                                                                     A|B
                   Wn                             Wn                                     Wn                             Wn
         Prv.:          ψk is A-local and A ⊢
                     k=1W                           k=1 ψk .                   Prv.:          ψk is B-local and B ⊢
                                                                                           k=1V                           k=1 ψk .
                          n                                                                     n
         Int.:     φ′ ≡   k=1 φk .                                             Int.:     φ′ ≡   k=1 φk .


              Redplus1                           Redplus2                       Redminus1                           Redminus2

          A ∪ {ψ} | B                        A | B ∪ {ψ}                           A|B                                 A|B
             A|B                                A|B                             A ∪ {ψ} | B                         A | B ∪ {ψ}

     Prv.:     A ⊢ ψ and                 Prv.:    B ⊢ ψ and                 Prv.:     A ⊢ ψ and                 Prv.:   B ⊢ ψ and
               ψ is A-local.                      ψ is B-local.                       ψ is A-local.                     ψ is B-local.
      Int.:    φ′ ≡ φ.                   Int.:    φ′ ≡ φ.                    Int.:    φ′ ≡ φ.                   Int.:   φ′ ≡ φ.

                ConstElim1                                     ConstElim2                                   ConstElim0

                    A|B                                          A|B                                           A|B
               A ∪ {a = t} | B                              A | B ∪ {b = t}                           A ∪ {c = t} | B ∪ {c = t}

     Prv.:     a is A-strict and                   Prv.:    b is B-strict and                     Prv.: c, t are AB-common,
               does not occur in A, t.                      does not occur in B, t.                     c does not occur in A, B, t.
      Int.:    φ′ ≡ φ.                              Int.:   φ′ ≡ φ.                               Int.: φ′ ≡ φ.




Table 1: Interpolating Metarules: each rule has a proviso P rv. and an instruction Int. for recursively
              computing the new interpolant φ′ from the old one(s) φ, φ1 , . . . , φk .


The latter is obviously the case whenever the original pair (A, B) is AX diff -unsatisfiable
and it is precisely the case leading to an interpolating metarules refutation.
    The basic idea is that of invoking the algorithm of Section 5 on A and B separately
and to propagate equalities involving AB-common terms. We shall assume an ordering
precedence making AB-common constants smaller than A-strict or B-strict constants of
the same sort. However, this is not sufficient to prevent the algorithm of Section 5 from
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                         25




generating literals and rules violating one or more of the hypotheses of Proposition 4.5: this
is why the extra correcting instructions of group (γ) below are needed. Our interpolating
algorithm has a pre-processing and a completion phase, like the algorithm from Section 5.
Pre-processing. In this phase the four Steps of Section 5.1 are performed on both A
and B; to justify these steps we need metarules (Define0,1,2), (Redplus1,2), (Redminus1,2),
(Disjunction1,2), (ConstElim0,1,2), and (Propagate1,2)—the latter because if i, j are AB-
common, the guessing of i = j versus i 6= j in Step 3 can be done, say, in the A-component
and then propagated to the B-component. At the end of the preprocessing phase, the
following properties (to be maintained as invariants afterwards) hold:
(i1): A (resp. B) contains i 6= j for all A-local (resp. B-local) constants i, j of sort INDEX
      occurring in A (resp. in B);
(i2): if a, i occur in A (resp. in B), then rd(a, i) reduces to an A-local (resp. B-local)
      constant of sort ELEM.
Completion. Some groups of instructions to be executed non-deterministically constitute
the completion phase. There is however an important difference here with respect to the
completion phase of Section 5.2: it may happen that we need some guessing also inside the
completion phase (only the instructions from group (γ) below may need such guessings).
Each instruction can be easily justified by suitable metarules (we omit the straightforward
details). The groups of instructions are the following:
(α) Apply to A or to B any instruction from the completion phase of Section 5.2.
(β) If there is an AB-common literal that belongs to A but not to B (or vice versa), copy
     it in B (resp. in A).
(γ) Replace undesired literals, i.e., those violating conditions (I)-(II)-(III) from Proposi-
     tion 4.5.
To avoid trivial infinite loops with the (β) instructions, rules in (α) deleting an AB-common
literal should be performed simultaneously in the A- and in the B-components (it can be
easily checked - see the proof of Theorem 6.3 below - that this is always possible, if rules
in (β) and (γ) are given higher priority).
     Instructions (γ) need to be described in more details. Preliminarily, we introduce a
technique that we call Term Sharing. Suppose that the A-component contains a literal
α = t, where the term t is AB-common but the free constant α is only A-local. Then it
is possible to “make α AB-common” in the following way. First, introduce a fresh AB-
common constant α′ with the explicit definition α′ = t (to be inserted both in A and in B,
as justified by metarule (Define0)); then replace the literal α = t by α = α′ and replace α
by α′ everywhere else in A; finally, delete α = α′ too. The result is a pair (A, B) where
basically nothing has changed but α has been renamed to an AB-common constant α′ .
Notice that the above transformations can be justified by metarules (Define0), (Redplus1),
(Redminus1), (ConstElim1). We are now ready to explain instructions (γ) in details. First,
consider undesired literals corresponding to the rewrite rules of the form
                                        rd(c, i) → d                                     (6.1)
in which the left-hand side is AB-common and the right-hand side is, say, A-strict. If we
apply Term Sharing, we can solve the problem by renaming d to an AB-common fresh
constant d′ . We can apply a similar procedure to the rewrite rules
                                       a → wr(c, I, E)                                   (6.2)
26                           R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




in case the right-hand side is AB-common and the left-hand side is not; when we rename
a to some fresh AB-common constant c′ , we must arrange the precedence so that c′ > c to
orient the renamed literal as c′ → wr(c, I, E). Then, consider the literals of the form
                                                diff(a, b) = k                                         (6.3)
in which the left-hand side is AB-common and the right-hand side is, say, A-strict. Again,
we can rename k to some AB-common constant k′ by Term Sharing. Notice that k′ is
AB-common, whereas k was only A-local: this implies that we might need to perform
some guessing to maintain the invariant (i1). Basically, we need to repeat Step 3 from
Section 5.1 till invariant (i1) is restored (k′ must be compared for equality with the other
B-local constants of sort INDEX). The last undesired literals to take care of are the rules of
the form
                                         c → wr(c′ , I, E)                                        (6.4)
having an AB-common left-hand side but, say, only an A-local right-hand side (literals of
the form d = e are automatically oriented in the right way by our choice of the precedence).
Notice that from the fact that c is AB-common, it follows (by our choice of the precedence)
that c′ is AB-common too. We can freely suppose that I and E are split into sub-lists
I1 , I2 and E1 , E2 , respectively, such that I ≡ I1 · I2 and E ≡ E1 · E2 , where I1 , E1 are
AB-common, I2 ≡ i1 , . . . , in , E2 ≡ e1 , . . . , en and for each k = 1, . . . , n at least one from
ik , ek is not AB-common. This n (measuring essentially the number of non AB-common
symbols in (6.4)) is called the degree of the undesired literal (6.4): in the following, we shall
see how to eliminate (6.4) or to replace it with a smaller degree literal. We first make a
guess (see metarule (Disjunction1)) about the truth value of the literal c = wr(c′ , I1 , E1 ). In
the first case, we add the positive literal to the current constraint; as a consequence, we get
that the literal (6.4) is equivalent to c = wr(c, I2 , E2 ) and also to rd(c, I2 ) = E2 (see Red
in Figure 1). In conclusion, in this case, the literal (6.4) is replaced by the AB-common
rewrite rule c → wr(c′ , I1 , E1 ) and by the literals rd(c, I2 ) = E2 . In the second case, we
guess that the negative literal c 6= wr(c′ , I1 , E1 ) holds; we introduce a fresh AB-common
constant c′′ together with the defining AB-common literal7
                                             c′′ → wr(c′ , I1 , E1 )                                   (6.5)
(see metarule (Define0)). The literal (6.4) is replaced by the literal
                                             c → wr(c′′ , I2 , E2 ).                                   (6.6)
We show how to make the degree of (6.6) smaller than n. In addition, we eliminate the
negative literal c 6= c′′ coming from our guessing (notice that, according to (6.5), c′′ renames
wr(c′ , I1 , E1 )). This is done as follows: we introduce fresh AB-common constants i, d, d′′
together with the AB-common defining literals
                           diff(c, c′′ ) = i,     rd(c, i) → d,        rd(c′′ , i) → d′′               (6.7)
(see metarule (Define0)).        Now it is possible to replace c 6= c′′ by the literal d 6= d′′ (see
axiom (3.3)). Under the assumption Distinct(I2 ), the following statement is AX diff valid:
                                                                            _
                                                                            n
     c = wr(c′′ , I2 , E2 ) ∧ rd(c′′ , i) = d′′ ∧ rd(c, i) = d ∧ d 6= d′′ →   (i = ik ∧ d = ek ).
                                                                                   k=1

     7We put c > c′′ > c′ in the precedence. Notice that invariant (i2) is maintained, because all terms
rd(c′′ , h) normalize to an element constant. In case I1 is empty, one can directly take c′ as c′′ .
                 QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                              27




Thus, we get n alternatives (see metarule (Disjunction1)). In the k-th alternative, we
can remove the constants ik , ek from the constraint, by replacing them with the AB-
common terms i, d respectively (see metarules (Redplus1), (Redplus2), (Redminus1), (Red-
minus2),(ConstElim1),(ConstElim0)); notice that it might be necessary to complete the
index partition. In this way, the degree of (6.6) is now smaller than n.
     In conclusion, if we apply exhaustively Pre-Processing and Completion instructions
above, starting from an initial pair of constraints (A, B), we can produce a tree, whose
nodes are labelled by pairs of constraints (the successor nodes of a node labelled (Ã, B̃) are
labelled by pairs of constraints that are obtained from (Ã, B̃) by applying an instruction).
Notice that the branching in the tree is due to instructions that need guessing and that
Pre-Processing instructions are applied only in the initial segment of a branch. We call
such a tree an interpolating tree for (A, B). The following result shows that we obtained an
interpolation algorithm for AX diff .
Theorem 6.3. Any interpolation tree for (A, B) is finite; moreover, it is an interpolating
metarules refutation (from which an interpolant can be recursively computed according to
Proposition 6.2) precisely iff A ∧ B is AX diff -unsatisfiable.
Proof. Since all instructions can be justified by metarules and since our instructions bring
any pair of constraints into constraints which are either manifestly inconsistent (i.e. contain
⊥) or satisfy the requirements of Proposition 4.5, the second part of the claim is clear. We
only have to show that all branches are finite (then König lemma applies).
    A complication that we may face here is due to the fact that during instructions (γ),
the signature is enlarged. However, notice that our instructions may introduce genuinely
new AB-common array constants, however they can only rename index constants, element
constants and non AB-common array constants. Moreover: (1) Term Sharing decreases the
number of the constants which are not AB-common; (2) each call in the recursive procedure
for the elimination of literals (6.4), either (2.i) renames to AB-common constants some
constants which were not AB-common before, or (2.ii) just replaces a literal of the kind
c = wr(c′ , I1 · I2 , E1 · E2 ) by the literals
                             c = wr(c′ , I1 , E1 ),   rd(c′ , I2 ) = E2
(see the first alternative following the guessing about truth of the literal c = wr(c′ , I1 , E1 )).
Since there are only finitely many non AB-common constants at all, after finitely many
steps neither Term Sharing nor (2.i) apply anymore. We finally show that instructions (α),
(β) and (2.ii) (that do not enlarge the signature) cannot be executed infinitely many times
either. To this aim, it is sufficient to associate with each pair of constraints (Ã, B̃) the
complexity measure given by the multi-set of pairs (ordered lexicographically) hm(L), NL i
(varying L ∈ Ã ∪ B̃), where m(L) is the multi-set of terms associated with the literal L and
NL is 1 if L ∈ Ã \ B̃, 2 if L ∈ B̃ \ Ã, and 0 if L ∈ Ã ∩ B̃. In fact, the second component
in the above pairs takes care of instructions (β), whereas the first component covers all the
remaining instructions. Notice that it is important that, whenever an AB-common literal
is deleted, the deletion happens simultaneously in both components (otherwise, the (β)
instruction could re-introduce it, causing an infinite loop; our complexity measure does not
decrease if an AB-common literal is replaced by smaller literals only in the A- or in the
B-component): in fact, it can be shown (by inspecting the instructions from the completion
phase of Subsection 5.2) that whenever an AB-common literal is deleted, the instruction
28                           R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




that removes it involves only AB-common literals, if undesired literals are removed first.8
Thus, if instructions in (β) and (γ) have priority (as required by our specifications above),
AB-common literal deletions caused by (α) can be performed both in the A- and in the B-
component (notice also that the instructions from (β) and (2ii) do not remove AB-common
literals).
    From the theorem above it immediately follows Theorem 3.3, that we have already
proved in Section 3.1 by using model-theoretic notions (thus in a non-constructive way).

6.3. An Example. To illustrate our method, we describe the computation of an interpolant
for the problem
                                    Π ≡ (A0 , B0 )
where
                    A0 ≡ { a = wr(b, i, d) }
                    B0 ≡ { rd(a, j) 6= rd(b, j), rd(a, k) 6= rd(b, k), j 6= k }.
    Notice that i, d are A-strict constants, j, k are B-strict constants, and a, b are AB-
common constants with precedence a > b. The computation of the interpolant in our
framework can be represented with a tree, growing upward from Π, in which each step can
be identified with a set of appropriate metarules application.
    To begin with we first apply Pre-Processing instructions to obtain
A1 ≡ { a = wr(b, i, d), rd(a, i) = e5 , rd(b, i) = e6 }
B1 ≡ { rd(a, j) = e1 , rd(b, j) = e2 , rd(a, k) = e3 , rd(b, k) = e4 , e1 6= e2 , e3 6= e4 , j 6= k }.
Since a = wr(b, i, d) is an undesired literal of the kind (6.4), we generate the two sub-
problems
                           Π1 ≡ (A1 ∪ { rd(b, i) = d, a = b }, B1 ), and
                           Π2 ≡ (A1 ∪ { a 6= b }, B1 )
(this is precisely the case in which there is no need of an extra AB-common constant c′′ ).
     Let us consider Π1 first. Notice that A ⊢ a = b, and a = b is AB-common. Therefore
we send a = b to B1 , and we may derive the new equality e1 = e2 from the critical pair
(C3) e1 ← rd(a, j) → rd(b, j) → e2 , thus obtaining
A2 ≡ { rd(b, i) = d, a = b, rd(a, i) = e5 , rd(b, i) = e6 }
B2 ≡ { rd(b, j) = e2 , rd(a, k) = e3 , rd(b, k) = e4 , e1 6= e2 , e3 6= e4 , j 6= k, a = b, e1 = e2 }.
Now B is inconsistent (as it contains both e1 6= e2 and e1 = e2 ). The interpolant for Π1
can be computed with the interpolating instructions of the metarules (Close2, Redplus2,
Redmius2, Propagate1) resulting in
                                                ϕ1 ≡ a = b
as shown in Figure 2.
     8Let us see an example by considering instruction (C3). This instruction removes a literal rd(a, i) → e′
using a literal a → wr(b, I, E) (and possibly rewrite rules rd(b, i) → d′ as well as rewrite rules that might
reduce some of the e′ , d′ , E). Now, if rd(a, i) → e′ is AB-common and all the other involved rules are not
undesired literals, the instruction as a whole manipulates AB-common literals. As such, if (β) has been
conveniently applied, the instruction can be performed simultaneously in the A- and in the B-component
and our specification is precisely to do that.
                    QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                            29




                                  Close2                                                       ⊤
                                                     ...          | B1′ ∪ { a = b, e1 = e2 }
                               Redminus2                                                       ⊤
                                                     ...          | B1 ∪ { a = b, e1 = e2 }
                                Redplus2                                                       ⊤
                                                     ...          | B1 ∪ { a = b }
                        Propagate1                                                    a=b
                                      A1 ∪ { rd(b, i) = d, a = b } | B1
 where
 B1′ ≡ B1 \ {rd(b, j) = e2 }


Figure 2: Interpolant derivation for Π1 using metarules. The derivation is to be read
          bottom-up. The labels for the rules are shown on the left, while the partial
          interpolants, computed top-down, are shown on the right.

     Then, let us consider branch Π2 . Recall that this branch originates from the attempt
of removing the undesired rule a → wr(b, i, d). We introduce, in both A and B, the AB-
common defining literals diff(a, b) = l, rd(a, l) = f1 , rd(b, l) = f2 . In order to remove
a 6= b, we introduce f1 6= f2 in A, which is propagated to B, thus obtaining:
               A3 ≡ { a = wr(b, i, d),
                      diff(a, b) = l, rd(a, l) = f1 , rd(b, l) = f2 , f1 6= f2 }
               B3 ≡ { rd(a, j) = e1 , rd(b, j) = e2 , rd(a, k) = e3 , rd(b, k) = e4 ,
                      e1 6= e2 , e3 6= e4 , j 6= k,
                      diff(a, b) = l, rd(a, l) = f1 , rd(b, l) = f2 , f1 6= f2 }.
Since a = wr(b, i, d) contains only the index i, we do not have a real case split. Therefore we
replace i with l, and d with f1 . At last, we propagate the AB-common literal a = wr(b, l, f1 )
to B. After all these steps we obtain:
               A4 ≡ { a = wr(b, l, f1 ),
                      diff(a, b) = l, rd(a, l) = f1 , rd(b, l) = f2 , f1 6= f2 }
               B4 ≡ { rd(a, j) = e1 , rd(b, j) = e2 , rd(a, k) = e3 , rd(b, k) = e4 ,
                      e1 6= e2 , e3 6= e4 , j 6= k,
                      diff(a, b) = l, rd(a, l) = f1 , rd(b, l) = f2 , f1 6= f2 ,
                      a = wr(b, l, f1 ) }.
Since we have one more AB-common index constant l, we complete the current index
constant partition, namely {k} and {j}: we have three alternatives, to let l stay alone
in a new class, or to add l to one of the two existing classes. In the first alternative,
because of the following critical pair (C3) e1 ← rd(a, j) → rd(wr(b, l, f1 ), j) → e2 , we add
e1 = e2 to B, which becomes trivially unsatisfiable. The other two alternatives yield similar
outcomes. For each sub-problem the interpolant is ⊤. The partial interpolant for Π2 has
to be reconstructed by the reverse application of the interpolanting instructions of (Define0)
and (Propagate1), as shown in Figure 3, which yield
    ϕ2 ≡ (a = wr(b, diff(a, b), rd(a, diff(a, b))) ∧ rd(a, diff(a, b)) 6= rd(b, diff(a, b))).
30                               R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




                           Close2                                                          ⊤
                                      . . . | B1′′ ∪ C ∪ {l 6= k, l 6= j, e1 = e2 }
                      Redminus2                                                            ⊤
                                      . . . | B1′ ∪ C ∪ {l 6= k, l 6= j, e1 = e2 }
                        Redplus2                                                           ⊤     .         .
                                      . . . | B1′ ∪ C ∪ {l 6= k, l 6= j}                         ..        ..
                    Disjunction2                                                                                ⊤
                                                                . . . | B1′ ∪ C
         Propagate1                                                                                   a = wr(b, l, f1 )
                         A′1 ∪ {f1 6= f2 , a = wr(b, l, f1 ) } ∪ C | B1 ∪ C ∪ {f1 6= f2 }
         Redminus1                                                                                    a = wr(b, l, f1 )
                         A1 ∪ { f1 6= f2 , a = wr(b, l, f1 ) } ∪ C | B1 ∪ C ∪ {f1 6= f2 }
           Redplus1                                                                                   a = wr(b, l, f1 )
                                          A1 ∪ { f1 6= f2 } ∪ C | B1 ∪ C ∪ {f1 6= f2 }
                          Propagate1                                                                  a = wr(b, l, f1 ) ∧ f1 6= f2
                                          A1 ∪ { f1 6= f2 } ∪ C | B1 ∪ C
                   Redminus1                                                          a = wr(b, l, f1 ) ∧ f1 6= f2
                                    A1 ∪ { a 6= b, f1 6= f2 } ∪ C | B1 ∪ C
                      Redplus1                                                        a = wr(b, l, f1 ) ∧ f1 6= f2
                                             A1 ∪ { a 6= b } ∪ C | B1 ∪ C
                               Define0*                                               ϕ2
                                                  A1 ∪ { a 6= b } | B1
 where
 C ≡ {diff(a, b) = l, rd(a, l) = f1 , rd(b, l) = f2 }
 A′1 ≡ A1 \ { a = wr(b, i, d) }
 B1′ ≡ B1 ∪ { f1 6= f2 , a = wr(b, l, f1 ) }
 B1′′ ≡ B1′ \ { rd(a, j) = e1 }
 ϕ2 ≡ (a = wr(b, diff(a, b), rd(a, diff(a, b))) ∧ rd(a, diff(a, b)) 6= rd(b, diff(a, b)))


Figure 3: Interpolant derivation for Π2 using metarules. The derivation is to be read
          bottom-up. The labels for the rules are shown on the left, while the partial
          interpolants, computed top-down, are shown on the right.

   The final interpolant is computed by combining the interpolants for Π1 and Π2 by
means of (Disjunction1), yielding
                      ϕ ≡ ϕ1 ∨ ϕ2 ≡
                        ≡ (a = b ∨ (a = wr(b, diff(a, b), rd(a, diff(a, b))) ∧
                          ∧ rd(a, diff(a, b)) 6= rd(b, diff(a, b)))
which can be simplified to ϕ ≡ (a = wr(b, diff(a, b), rd(a, diff(a, b)))).

                                  7. Related work and Conclusions
There are two main lines of work in the literature which is relevant for our paper: satisfiabil-
ity procedures for variants and extensions of the theory of arrays and interpolation methods
related to the theory of arrays. Below, we discuss the works which are more closely related
to our approach in some details.

7.1. Satisfiability. Since its introduction by McCarthy in [43], the theory of arrays have
received a lot of attention in automated theorem proving and verification because of its
importance in modelling fundamental mechanisms of hardware and software systems such
as memory read and write operations. For example, a lot of papers have been devoted
to design, prove correct, and build decision procedures for the satisfiability problem of
                   QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                     31




quantifier-free and selected classes of quantified formulae in (various extensions of) the
theory of arrays; e.g., [2, 8, 14, 25, 29–31, 38, 41, 55]. The interested reader is pointed to
the ‘related work’ sections of [25, 30] for a comprehensive overview. Here, we notice that
many of them are based on instantiating the axioms of the theory so that rd and wr can
be considered as uninterpreted functions and state-of-the-art procedures for the theory of
equality can be used. Notable exceptions are [2,41,55] where techniques based on rewriting
or constraint solving are used.
     In [2], the standard superposition calculus [5] is proven to terminate on the union of
the theory of arrays and a set of ground literals; thereby, providing a decision procedure
for the quantifier-free satisfiability problem because of the refutation completeness of the
calculus. (The efficiency of the approach is explored in [1].) While the saturation (roughly,
the exhaustive application of the rules of the superposition calculus) can be seen as a gen-
eralization of completion where clauses, and not only equalities, are handled, our Gaussian
completion9 has some distinctive features. In fact, while the three critical pairs (C3), (C4),
and (C5) in Section 5.2 can be regarded as instances of the inference rules of a superposition
calculus (see [2] for details), the critical pairs (C1) and (C2), exploiting the equivalences in
Figure 1, are impossible to recast in any standard completion procedure (see, e.g., [4]). In
fact, the way in which the critical pairs (C1) and (C2) are eliminated involves the addition
of equalities containing rd’s (in order to constrain the values stored at certain locations in
the arrays mentioned in the rules of the critical pair) besides the replacement of one or both
the parent rewrite rules by an equality. Only in this way, we were able to eliminate badly
orientable rules. It seems difficult to adapt the approach in [2] to the problem under con-
sideration mainly because of the chosen order > over terms. In fact, we orient the equality
a → wr(b, i, e) from left to right if a > b, and use the equivalences in Figure 1 when b > a
(or a and b are identical). This allows us to eliminate all critical pairs with rules (4.1)–(4.4)
in Definition 4.2 since such rules contain just one variable of sort ARRAY and, trivially, no
critical pairs involving the variable should be considered. If we choose the other way of ori-
enting the equalities of the form a = wr(b, i, e), several critical pairs would arise. Although
the completion of these pairs terminate under suitable assumptions (as shown in [2]), this
creates serious problems when considering the computation of interpolants.
     In [41], a satisfiability procedure for the theory of arrays with extensionality is designed
so as to be easily combined with other procedures by the Shostak combination method (see,
e.g., [51]). Two interface functionalities are required by the Shostak combination method:
(i) normalizing terms and (ii) solving equalities. We consider each activity in details.
  (i) In Chapter 5 of [41], a canonical form for terms built out by using a single rd or
       several wr’s is defined by using a simplification ordering. The canonical terms are
       similar to those occurring in a modular constraint according to Definition 4.2 above.
       A major difference is the use of if-then-else’s to normalize read-terms in [41] while our
       procedure does not use them because item (i) of Definition 4.2 implies that any two
       indexes in a constraint in normal form are known to be distinct. This choice makes the
       proof of the correctness of our procedure much easier with respect to the argument for
       the correctness proposed in [41] which “has proved elusive to the authors” of [55]. So
       called ‘lazy’ SMT solvers, based on the integration of a SAT solver and a satisfiability
    9The Gauss elimination procedure for systems of linear equalities has been lifted to elementary theories
in [3] and, since the theory of arrays is close to being Gaussian [15], we show that ‘Gaussian-like’ steps can
be exploited during completion phase.
32                       R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




      procedures for conjunction of literals, seem to be able to easily implement the case-
      splitting required to derive a complete partition by resorting to the available SAT
      solver as explained, e.g., in [9].
 (ii) To compare with the activity of solving equalities in [41], let us preliminarily observe
      that the logical equivalences in Figure 1 can be considered as rewrite rules (either from
      left to right or viceversa) that help us replace badly orientable equalities (recall the
      definition at the beginning of Section 4) with equalities which are oriented from left
      to right. This is precisely how the equivalences in Figure 1 are used in the Gaussian
      completion procedure (of Section 5.2) to eliminate critical pairs. Similarly, in order to
      provide one of the basic functionalities required by the Shostak combination frame-
      work, [41] designs a solver for equalities involving wr operations. For example, the
      procedure in [41] allows one to solve the equality a = wr(b, i, e) for b. We can adapt
      our procedure (in particular, by using the equivalences Symm and Refl of Figure 1)
      to do the same. The main difference is that our normalization is done off-line, i.e.
      the signature is fixed since all terms appearing in the constraint are given, while the
      procedure in [41] must be on-line since is to be integrated in a Shostak combination
      algorithm which requires that to process equalities one at a time, as soon as they
      become available. Because of this, the completion algorithm can be simplified (since
      there is no need to compute intermediate normal forms) and standard techniques to
      show its termination can be used. In contrast, [41] gives only a brief sketch of the
      termination of his procedure. For a more comprehensive comparison of on-line and
      off-line completion algorithms revisiting the Shostak congruence closure algorithm, the
      reader is pointed to [6, 36].
The procedure in [55] share with [41] and ours the key activity of solving equalities. The
main difference is that no canonical forms for terms or constraints are defined in [55]; rather
a special form of equality over arrays is introduced, called partial equality, which compares
the content of two arrays only at a (finite) set of indexes. Formally, this is defined as
follows: a =I b iff for every index i not in the set I, the content of a at i is equal to that
of b at the same index I. Thus, an equality of the form wr(a, i, e) = b can be rewritten as
a ={i} b ∧ rd(b, i) = e. The key insight of [55] is that it is possible to eliminate all wr’s,
so that arrays can be considered as uninterpreted functions and rd as function application,
and a slightly modified congruence closure (to cope with partial equality) can be used to
check satisfiability. While no standard rewriting techniques are used in [55], it is interesting
to notice that two arrays a and b are cardinality dependent iff there exists a finite set I
of indexes such that a =I b. We do not introduce a new predicate symbol and use it
in designing a satisfiability procedure, however we nevertheless exploit this notion and its
preservation through embeddings (see Lemma 3.1) during our semantic interpolation proofs.

7.2. Interpolation. After McMillan’s seminal work on interpolation for model checking [45,
48], several papers [11, 21, 22, 34, 37, 39, 42, 46, 52, 54, 56] appeared whose aim was to design
techniques for the efficient computation of interpolants in first-order theories of interest
for verification, mainly uninterpreted function symbols, fragments of Linear Arithmetic, or
their combination. An interpolating theorem prover is described in [47], where a sequent-
like calculus is used to derive interpolants from proofs in propositional logic, equality with
uninterpreted functions, linear rational arithmetic, and their combinations. The method
described in [56] proposes a framework suitable for lazy SMT-solvers, in which the theory
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                          33




solver is required to derive partial interpolants for each theory lemmata it produces. The
global interpolant can then be computed at the propositional level. The paper also illus-
trates a method to derive interpolants in a Nelson-Oppen combination procedure, under
certain restrictions on the theories to combine. More recently, in [22] the ideas of [56] are
adapted to cope with state-of-the-art SMT-solving strategies for combinations of the theo-
ries of uninterpreted functions and a fragment of Linear Arithmetic (called difference logic).
In [37], a method to compute interpolants in data structures theories, such as sets and arrays
(with extensionality), by axiom instantiation and interpolant computation in the theory of
uninterpreted functions is described. It is also shown that the theory of arrays with exten-
sionality does not admit quantifier-free interpolation. The “split” prover in [34] applies a
sequent calculus for the synthesis of interpolants along the lines of that in [47] and is tuned
for predicate abstraction [53]. In particular, the method is shown to be complete in the
sense that the computed interpolants are guaranteed to provide the “right” level abstraction
to prove a certain property, if one exists. The “split” prover can handle a combination of
theories among which also the theory of arrays without extensionality is considered. In [34],
it is pointed out that the theory of arrays poses serious problems in deriving quantifier-free
interpolants because it entails an infinite set of quantifier-free formulae, which is indeed
problematic when interpolants are to be used for predicate abstraction. To overcome the
problem, [34] suggests to constrain array valued terms to occur in equalities of the form
a = wr(a, I, E) in the notation of this paper. It is observed that this corresponds to the
way in which arrays are used in imperative programs. Further limitations are imposed on
the symbols in the equalities in order to obtain a complete predicate abstraction procedure.
In [35], the method described in [34] is specialized to apply CEGAR techniques [23] for
the verification of properties of programs manipulating arrays. The method of [34] is ex-
tended to cope with range predicates which allow one to describe unbounded array segments
which permit to formalize typical programming idioms of arrays, yielding property-sensitive
abstractions. In [54], it is shown how to extend satisfiability procedures based on axiom
instantiation to compute interpolants. However, the theory of arrays is not considered.
In [52], the approach of [54] is specialized to compute interpolants in the combination of
Linear Rational Arithmetic and the theory of uninterpreted function symbols; again, the
theory of arrays is not considered. A method for deriving interpolants in the theory of
equality with uninterpreted functions is also given in [28] by extending a congruence clo-
sure algorithm. In [39], a method to derive quantified invariants for programs manipulating
arrays and integer variables is described. A resolution-based prover is used to handle an
ad hoc axiomatization of arrays by using predicates. Neither McCarthy’s theory of arrays
nor one of its extensions are considered in [39]. The invariant synthesis method is based on
the computation of interpolants derived from the proofs of the resolution-based prover and
constraint solving techniques to handle the arithmetic part of the problem. The resulting
interpolants may contain even alternation of quantifiers.
      Latest research on interpolating procedures has been focusing on (extensions of) Linear
Integer Arithmetic. An interpolating procedure for linear Diophantine equalities is outlined
in [33]. A procedure for full Linear Integer Arithmetic based on a sequent calculus can
be found in [11]. In [12], the procedure in [11] is extended to cope with the theory of
arrays without extensionality by axiom instantiation and interpolation in the combination of
Presburger Arithmetic and uninterpreted function. Quantifiers can occur in the interpolants
returned by the procedure. Recently [16], we have proposed a quantifier-free interpolation
solver for AX diff when combined with integer difference logic over indexes.
34                       R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




7.3. Conclusions and Future Work. We believe that the procedure proposed in this
paper is a significant step forward to make model-checking more widely applicable to pro-
grams whose properties depend crucially on the manipulations of arrays. To the best of
our knowledge, in fact, our interpolation procedure is the first to compute quantifier-free
interpolants for a natural variant of the theory of arrays with extensionality obtained by
replacing the extensionality axiom with its Skolemization. This variant is ‘natural’ in the
sense that it is sufficient to detect unsatisfiability of formulae as it is usually the case in
standard model checking methods for infinite state systems.
     Despite the work reported in this paper is a significant step forward in widening the
scope of applicability of interpolation in model checking of array manipulating programs,
we discuss some interesting directions for further work.
     The implementation of the interpolating procedure proposed here is crucial for showing
the practical viability of our approach. In this respect, the first step is to implement the
satisfiability solver in Section 5. Recall that this requires guessing, a pre-processing phase,
and Gaussian completion phase. Guessing, as already observed in Section 7.1 item (i)
when discussing the relationship with the solver of [41], can be implemented by adapting
the mechanism to handle arrangements when combining satisfiability procedures in the
Delayed Theory Combination approach of [9]. The main advantage of this approach is
to use state-of-the-art SAT techniques to efficiently enumerate all possible partitions of
indexes. The pre-processing phase can be implemented by using the data structures and
basic expression manipulating procedures available in many state-of-the-art SMT solvers.
The Gaussian completion phase requires more effort but it can adapt and reuse well-known
techniques developed in rewriting for completion procedures (see, e.g., [4]). The second
step to build the interpolating procedure of Section 6 is to implement the interpolating
metarules of Table 1. This is relatively simple and does not require much ingenuity and can
be done on top of the existing infrastructure for proof generation that is available in many
state-of-the-art SMT solvers.
     We are currently developing an implementation of the procedure presented here in the
SMT-solver OpenSMT [18]. Preliminary experiments are encouraging although a more ex-
tensive experimental evaluation is needed. In fact, it is well-known that the convergence
of interpolation based model checking procedures crucially depends on the “quality” of the
computed interpolants. There have been attempts (see, e.g., [34, 49]) to build interpolating
procedures that return “high quality” interpolants that guarantee the convergence of model
checking for valid properties. Recently, it has been observed [26, 44] that a certain degree
of flexibility for tuning the computation of interpolants in interpolation procedures would
be desirable to facilate their integration in model checking. In this respect, it would be
particularly interesting to investigate how the order in which the interpolating metarules of
Table 1 are applied, particularly those on AB-common terms, may influence the “quality” of
the interpolants. An interesting alternative to investigate the flexibility of generating inter-
polants (suggested in [44]) would be to use the procedure presented here in the framework
for computing quantified interpolants of [44].
     Finally, there are two more interesting points that deserve further investigations. First,
it would be interesting to study the size of the interpolating metarules refutations and
compare them with interpolating procedures based on a proof calculus. The preliminary
experiments with our implementation of the procedure in Open SMT show that our refuta-
tions are quite compact but a more systematic comparison with available procedures based
                  QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                   35




on a proof calculus, e.g., [47] is needed to clarify this issue. Second, since in model check-
ing it is useful to compute interpolants for several partitions of the same (unsatisfiable)
formula, it would be interesting to design a method that permit the partial reuse of the
interpolants returned for a partition to compute the interpolant for the next one so as to
permit reuse and avoid degradation of performances due to partial recomputation of parts
of interpolating metarules refutation. In this respect, it seems possible to adapt techniques
developed for computing chains of interpolants in [13].


Acknowledgements. We wish to thank two anonymous referees for their comments on a draft
of this paper and an anonymous referee of RTA’11 for the criticisms that helped improving
the presentation.
     The work of the third author was partially supported by the “Automated Security
Analysis of Identity and Access Management Systems (SIAM)” project funded by Provincia
Autonoma di Trento in the context of the “team 2009 - Incoming” COFUND action of the
European Commission (FP7) and the FP7-ICT-2007-1 Project no. 216471.

                                             References
 [1] A. Armando, M. P. Bonacina, S. Ranise, and S. Schulz. New results on rewrite-based satisfiability
     procedures. ACM Trans. Comput. Log., 10(1), 2009.
 [2] Alessandro Armando, Silvio Ranise, and Michaël Rusinowitch. A rewriting approach to satisfiability
     procedures. Inform. and Comput., 183(2):140–164, 2003. RTA 2001 (Utrecht).
 [3] F. Baader, S. Ghilardi, and C. Tinelli. A new combination procedure for the word problem that gener-
     alizes fusion decidability results in modal logics. Inform. and Comput., 204(10):1413–1452, 2006.
 [4] F. Baader and T. Nipkow. Term rewriting and all that. Cambridge University Press, Cambridge, 1998.
 [5] L. Bachmair and H. Ganzinger. Rewrite-Based Equational Theorem Proving with Selection and Sim-
     plification. J. Log. Comput., 4(3):217–247, 1994.
 [6] L. Bachmair and A. Tiwari. Abstract Congruence Closure and Specializations. In Conference on Auto-
     mated Deduction, CADE ’2000, volume 1831 of LNCS, pages 64–78. Springer-Verlag, 2000.
 [7] P. D. Bacsich. Amalgamation properties and interpolation theorems for equational theories. Algebra
     Universalis, 5:45–55, 1975.
 [8] M. Bofill, R. Nieuwenhuis, A. Oliveras, E. Rodrguez-Carbonell, and A. Rubio. A Write-Based Solver
     for SAT Modulo the Theory of Arrays. In FMCAD, pages 101–108, 2008.
 [9] M. Bozzano, R. Bruttomesso, A. Cimatti, T. Junttila, P. Van Rossum, S. Ranise, and R. Sebastiani.
     Efficient Satisfiability Modulo Theories via Delayed Theory Combination. In CAV’05, pages 335–349,
     2005.
[10] Aaron R. Bradley and Zohar Manna. The Calculus of Computation. Springer, 2007.
[11] A. Brillout, D. Kroening, P. Rümmer, and W. Thomas. An Interpolating Sequent Calculus for
     Quantifier-Free Presburger Arithmetic . In IJCAR, 2010.
[12] A. Brillout, D. Kroening, P. Rümmer, and T. Wahl. Program Verification via Craig Interpolation for
     Presburger Arithmetic with Arrays. In Verification Workshop at FLoC, 2010.
[13] A. Brillout, D. Kroening, P. Rümmer, and T. Wahl. An Interpolating Sequent Calculus for Quantifier-
     Free Presburger Arithmetic. Journal of Automated Reasoning, 47:341–367, 2011.
[14] R. Brummayer and A. Biere. Lemmas on Demand for the Extensional Theory of Arrays. JSAT, 2009.
[15] R. Bruttomesso. Problemi di combinazione nella dimostrazione automatica e nella verifica del software.
     Università degli Studi di Milano, 2004. Master Thesis.
[16] R. Bruttomesso, S. Ghilardi, and S. Ranise. A Combination of Rewriting and Constraint Solving for
     the Quantifier-free Interpolation of Arrays with Integer Difference Constraints. In FroCoS, 2011.
[17] R. Bruttomesso, S. Ghilardi, and S. Ranise. Rewriting-based Quantifier-free Interpolation for a Theory
     of Arrays. In RTA, 2011.
36                           R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




[18] R. Bruttomesso, E. Pek, N. Sharygina, and A. Tsitovich. The OpenSMT Solver. In TACAS, pages
     150–153, 2010.
[19] Roberto Bruttomesso, Silvio Ghilardi, and Silvio Ranise. From Strong Amalgamability to Modularity of
     Quantifier-Free Interpolation. Technical Report RI 337-12, Dipartimento di Scienze dell’Informazione,
     Università degli Studi di Milano, 2012.
[20] C. Chang and J. H. Keisler. Model Theory. North-Holland, Amsterdam-London, third edition, 1990.
[21] A. Cimatti, A. Griggio, and R. Sebastiani. Efficient Interpolant Generation in Satisfiability Modulo
     Theories. In TACAS, pages 397–412, 2008.
[22] A. Cimatti, A. Griggio, and R. Sebastiani. Efficient Interpolation Generation in Satisfiability Modulo
     Theories. ACM Trans. Comput. Logic, 12:1–54, 2010.
[23] E. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. Counterexample-Guided Abstraction Refinement.
     In CAV, pages 154–169, 2000.
[24] W. Craig. Three uses of the Herbrand-Gentzen theorem in relating model theory and proof theory. J.
     Symb. Log., pages 269–285, 1957.
[25] L. de Moura and N. Bjørner. Generalized, Efficient Array Decision Procedures. In FMCAD, pages 45–52,
     2009.
[26] V. D’Silva, M. Purandare, G. Weissenbacher, and D. Kroening. Interpolant Strength. In Proceedings of
     VMCAI 2010, volume 5944 of LNCS, pages 129–145. Springer, 2010.
[27] H. B. Enderton. A Mathematical Introduction to Logic. Academic Press, Inc., 1972.
[28] A. Fuchs, A. Goel, J. Grundy, S. Krstić, and C. Tinelli. Ground Interpolation for the Theory of Equality.
     In TACAS, pages 413–427, 2009.
[29] V. Ganesh and D. L. Dill. A Decision Procedure for Bit-Vectors and Arrays. In CAV, pages 519–531,
     2007.
[30] S. Ghilardi, E. Nicolini, S. Ranise, and D. Zucchelli. Decision procedures for extensions of the theory
     of arrays. Annals of Mathematics and Artificial Intelligence, 50:231–254, 2007.
[31] A. Goel, S. Krstić, and A. Fuchs. Deciding Array Formulas with Frugal Axiom Instantiation. In SMT,
     2008.
[32] W. Hodges. Model Theory, volume 42 of Encyclopedia of Mathematics and its Applications. Cambridge
     University Press, Cambridge, 1993.
[33] H. Jain, E. Clarke, and O. Grumberg. Efficient craig interpolation for linear diophantine (dis)equations
     and linear modular equations. Form. Methods Syst. Des., 35(1):6–39, 2009.
[34] R. Jhala and K. L. McMillan. A Practical and Complete Approach to Predicate Refinement. In TACAS,
     pages 459–473, 2006.
[35] R. Jhala and K. L. McMillan. Array Abstractions from Proofs. In CAV, pages 193–206, 2007.
[36] D. Kapur. Shostak’s Congruence Closure as Completion. In 8th Int. Conf. on Rewriting Techniques and
     Applications, volume 1232 of LNCS, pages 23–37. Springer-Verlag, 1997.
[37] D. Kapur, R. Majumdar, and C. Zarba. Interpolation for Data Structures. In SIGSOFT’06/FSE-14,
     pages 105–116, 2006.
[38] D. Kapur and C. G. Zarba. A reduction approach to decision procedures. Technical report, Computer
     Science Dep., University of New Mexico, USA, 2005.
[39] L. Kovács and A. Voronkov. Finding Loop Invariants for Programs over Arrays Using a Theorem Prover.
     In FASE, pages 470–485, 2009.
[40] J. Krajı́cek. Interpolation Theorems, Lower Bounds for Proof Systems, and Independence Results for
     Bounded Arithmetic. J. Symb. Log., 62(2):457–486, 1997.
[41] J. Levitt. Formal Verification Thechniques for Digital Systems. PhD thesis, Department of Computer
     Science, Stanford University, 1996.
[42] C. Lynch and Y. Tang. Interpolants for Linear Arithmetic in SMT. In ATVA, LNCS, 2010.
[43] J. McCarthy. Towards a Mathematical Science of Computation. In IFIP Congress, pages 21–28, 1962.
[44] K. McMillan. Interpolants from Z3 proofs. In Proc. of FMCAD, 2011.
[45] K. L. McMillan. Interpolation and SAT-Based Model Checking. In CAV, pages 1–13, 2003.
[46] K. L. McMillan. An Interpolating Theorem Prover. In TACAS, pages 16–30, 2004.
[47] K. L. McMillan. An Interpolating Theorem Prover. Theor. Comput. Sci., 345(1):101–121, 2005.
[48] K. L. McMillan. Applications of Craig Interpolation to Model Checking. In TACAS, pages 1–12, 2005.
[49] K. L. McMillan. Quantified invariant generation using an interpolating saturation prover. In TACAS,
     pages 413–427, 2008.
                  QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                    37




[50] P. Pudlák. Lower Bounds for Resolution and Cutting Plane Proofs and Monotone Computations. J.
     Symb. Log., 62(3):981–998, 1997.
[51] S. Ranise, C. Ringeissen, and D. Tran. Nelson-Oppen, Shostak and the Extended Canonizer: A Family
     Picture with a Newborn. In ICTAC, pages 372–386, 2004.
[52] A. Rybalchenko and V. Sofronie-Stokkermans. Constraint Solving for Interpolation. In VMCAI, 2007.
[53] H. Saidi and S. Graf. Construction of abstract state graphs with PVS. In CAV, pages 72–83, 1997.
[54] V. Sofronie-Stokkermans. Interpolation in Local Theory Extensions. In IJCAR’06: Int. Conf. on Au-
     tomated Reasoning, volume 4130 of LNCS, pages 235–250, 2006.
[55] A. Stump, C. Barrett, D. Dill, and J. Levitt. A Decision Procedure for an Extensional Theory of Arrays.
     In IEEE Symposium on Logic in Computer Science, 2001.
[56] G. Yorsh and M. Musuvathi. A Combination Method for Generating Interpolants. In CADE, pages
     353–368, 2005.
38                               R. BRUTTOMESSO, S. GHILARDI, AND S. RANISE




                                  Appendix A. Proof of Theorem 2.3



Theorem 2.3 [7] Let T be universal. Then, T admits quantifier-free interpolation iff T
has the amalgamation property.
Proof. Suppose first that T has amalgamation; let A, B be quantifier-free formulae such that
A ∧ B is not T -satisfiable. Let us replace variables with free constants in A, B; let us call
ΣA the signature Σ of T expanded with the free constants from A and ΣB the signature Σ
expanded with the free constants from B (we put ΣC ≡ ΣA ∩ ΣB ). For reductio, suppose
that there is no ground formula C such that: (a) A T -entails C; (b) C ∧B is T -unsatisfiable;
(c) only free constants from ΣC occur in C.
     As a first step, we build a maximal T -consistent set Γ of ground ΣA -formulae and
a maximal T -consistent set ∆ of ground ΣB -formulae such that A ∈ Γ, B ∈ ∆, and
Γ ∩ ΣC = ∆ ∩ ΣC .10 For simplicity11 let us assume that Σ is at most countable, so that we
can fix two enumerations
                                  A1 , A2 , . . .  B1 , B2 , . . .
             A         B
of ground Σ - and Σ -formulae, respectively. We build inductively Γn , ∆n such that for
every n (i) Γn contains either An or ¬An ; (ii) ∆n contains either Bn or ¬Bn ; (iii) there is
no ground ΣC -formula C such that Γn ∪ S       {¬C} and ∆n ∪S{C} are not T -consistent. Once
this is done, we can get our Γ, ∆ as Γ := Γn and ∆ := ∆n .
     We let Γ0 be {A} and ∆0 be {B} (notice that (iii) holds by (a)-(b)-(c) above). To build
Γn+1 we have two possibilities, namely Γn ∪ {An } and Γn ∪ {¬An }. Suppose they are both
unsuitable because there are C1 , C2 ∈ ΣC such that the sets
                     Γn ∪ {An , ¬C1 },     ∆n ∪ {C1 },      Γn ∪ {¬An , ¬C2 },      ∆n ∪ {C2 }
are all T -inconsistent. If we put C := C1 ∨ C2 , we get that Γn ∪ {¬C} and ∆n ∪ {C} are
not T -consistent, contrary to induction hypothesis. A similar argument shows that we can
also build ∆n .
     Let now M1 be a model of Γ and M2 be a model of ∆. Consider the substructures
N1 , N2 of M1 , M2 generated by the interpretations of the constants from ΣC : since the
related diagrams are the same (because Γ ∩ ΣC = ∆ ∩ ΣC ), we have that N1 and N2 are ΣC -
isomorphic. Up to renaming, we can suppose that N1 and N2 are just the same substructure
(let us call it N for short). Since the theory T is universal and truth of universal sentences is
preserved by substructures, we have that N is a model of T . By the amalgamation property,
there is a T -amalgam M of M1 and M2 over N . Now A, B are ground formulae true in
M1 and M2 , respectively, hence they are both true in M, which is impossible because
A ∧ B was assumed to be T -inconsistent.
     Suppose now that T has quantifier free interpolants. Take two models M1 = (M1 , I1 )
and M2 = (M2 , I2 ) of T sharing a substructure N = (N, J ). In order to show that a
T -amalgam of M1 , M2 over N exists, it is sufficient (by Robinson Diagram Lemma 2.2) to
show that δM1 (M1 ) ∪ δM2 (M2 ) is T -consistent. If it is not, by the compactness theorem of
first order logic, there exist a Σ ∪ M1 -ground sentence A and a Σ ∪ M2 -ground sentence B
     10By abuse, we use ΣC to indicate not only the signature ΣC but also the set of formulae in the signature
 C
Σ .
     11
          This is just to avoid a (straightforward indeed) transfinite induction argument.
                QUANTIFIER-FREE INTERPOLATION OF A THEORY OF ARRAYS                                                         39




such that (i) A∧ B is T -inconsistent; (ii) A is a conjunction of literals from δM1 (M1 ); (iii) B
is a conjunction of literals from δM2 (M2 ). By the existence of quantifier-free interpolants,
taking free constants instead of variables, we get that there exists a ground Σ ∪ N -sentence
C such that A T -entails C and B ∧ C is T -inconsistent. The former fact yields that C is
true in M1 and hence also in N and in M2 , because C is ground. However, the fact that
C is true in M2 contradicts the fact that B ∧ C is T -inconsistent.




                                          This work is licensed under the Creative Commons Attribution-NoDerivs License. To view
                                          a copy of this license, visit http://creativecommons.org/licenses/by-nd/2.0/ or
                                          send a letter to Creative Commons, 171 Second St, Suite 300, San Francisco, CA 94105,
                                          USA, or Eisenacher Strasse 2, 10777 Berlin, Germany
