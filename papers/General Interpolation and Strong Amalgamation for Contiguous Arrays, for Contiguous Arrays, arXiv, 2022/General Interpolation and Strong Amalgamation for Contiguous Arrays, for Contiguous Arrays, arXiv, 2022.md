                                         General Interpolation and Strong Amalgamation
                                                      for Contiguous Arrays

                                             Silvio Ghilardi1 , Alessandro Gianola2 , Deepak Kapur3 , and Chiara Naso1
arXiv:2204.11771v1 [cs.LO] 25 Apr 2022




                                                1
                                                      Dipartimento di Matematica, Università degli Studi di Milano (Italy)
                                                2
                                                     Faculty of Computer Science, Free University of Bozen-Bolzano (Italy)
                                                                          gianola@inf.unibz.it
                                                    3
                                                      Department of Computer Science, University of New Mexico (USA)



                                                Abstract. Interpolation is an essential tool in software verification,
                                                where first-order theories are used to constrain datatypes manipulated
                                                by programs. In this paper, we introduce the datatype theory of con-
                                                tiguous arrays with maxdiff, where arrays are completely defined in their
                                                allocation memory and for which maxdiff returns the max index where
                                                they differ. This theory is strictly more expressive than the array theories
                                                previously studied. By showing via an algebraic analysis that its mod-
                                                els strongly amalgamate, we prove that this theory admits quantifier-free
                                                interpolants and, notably, that interpolation transfers to theory combi-
                                                nations. Finally, we provide an algorithm that significantly improves the
                                                ones for related array theories: it relies on a polysize reduction to general
                                                interpolation in linear arithmetics, thus avoiding impractical full terms
                                                instantiations and unbounded loops.


                                         1    Introduction
                                         Craig Interpolation Theorem [13] is a well-known result in first logic that, given
                                         an entailment between two logical formulae α and β, establishes the existence of
                                         a third formula γ that shares its non-logical symbols with both α and β and such
                                         that it is entailed by α and entails β. Studying interpolation has a long-standing
                                         tradition in non-classical logics and in algebraic logic. Nevertheless, interpolation
                                         has been obtaining an increasing attention in automated reasoning and formal
                                         verification since the seminal works by McMillan [23,24]. Indeed, specifically
                                         in infinite-state model checking, where an exhaustive, explicit exploration of the
                                         state space is not possible, computing interpolants has been proven to be a useful
                                         method for practical and efficient approximations of preimage computation. In
                                         the context of software verification, the initial configurations and the transitions
                                         relation are usually represented symbolically by means of logical formulae, which
                                         gives the possibility of implicitly encoding the execution traces of the system.
                                         More precisely, if T is the first order theory that constraints the state space,
                                         one can symbolically express via a suitable T -inconsistent formula the fact that
                                         the system, starting from its initial configuration, cannot reach in n-steps an
                                         error configuration. Through this inconsistency, interpolants are then extracted
                                         from the symbolic representations of these ‘error’ traces with the goal of helping
2       S. Ghilardi et al.

the search of (safety) invariants of the modeled system: interpolants can be
successfully used to refine and improve the construction of the candidate safety
invariants.
    Model-checking applications usually require that such computed interpolants
are not arbitrary but present specific shapes so as to guarantee their concrete
usability. Since in many cases studied in software verification the underlying the-
ories have a decidable quantifier-free fragment (but are undecidable or have pro-
hibitive complexity outside), the most naturale choice is to consider quantifier-
free interpolants. However, even in case α and β are quantifier-free, Craig’s The-
orem does not guarantee that an interpolant γ is quantifier-free too. Indeed, this
property, called ’quantifier-free interpolation’, does not hold in general for arbi-
trary first order theories. It is then a non-trivial (and, very often, challenging)
problem to prove that useful theories admit quantifier-free interpolation.
    In this paper, we are interested in studying the problem of quantifier-free
interpolation for an expressive datatype theory that strictly extends the well-
studied McCarthy’s theory of arrays with extensionality. The original theory was
introduced by McCarthy in [22]: however, in [20] it is shown that quantifier-free
interpolation fails for this theory. Moreover, although its quantifier-free fragment
is decidable, it is well-known that this theory in its full generality is undecid-
able [5]: nonetheless, in the same paper, the authors studied a significant de-
cidable fragment, the so-called ‘array property fragment’, which strictly extends
the quantifier-free one. The array property fragment is expressive enough to for-
malize several benchmarks; however, as proved in [19], it is not closed under
interpolation. Thus, a particularly challenging but interesting problem is that of
identifying expressive extensions of the quantifier-free fragment of arrays that
are still decidable but also enjoy interpolation: this is what we attack in this
contribution.
    A first attempt in this direction is in [7], where a variant of McCarthy’s theory
was introduced by Skolemizing the axioms of extensionality. This variant turned
out to enjoy quantifier-free interpolation [7],[35]. However, this Skolem function
diff is generic because its semantic interpretation is undetermined. Moreover,
all the array theories mentioned so far allow unlimited out-of-bound write op-
erations and so cannot express the notion of array length, which is fundamental
when formalizing the real behavior of programs. In this respect, there are two
possible variants that can be considered: (i) the weak length |−|    ˜ formalizes the
                       ˜ of indexes outside which the array a is undefined (a can
minimal interval [0, |a|]
be undefined also in some location inside [0, |a|]);˜     (ii) the (strong) length |−|
represents the exact interval [0, |a|] where the array a is fully defined. Strong
length is essential for the faithful logical formalization of benchmarks coming
from software verification, such as C programs included in the SV-COMP com-
petition [4].
    These are the main reasons why in [17] the theory has been further enriched.
There, the semantics of diff, called maxdiff, is uniquely determined in the mod-
els of the theory and is more informative: it returns the biggest index where two
different arrays differ. In this theory, weak length can be defined: this is no-
      General Interpolation and Strong Amalgamation for Contiguous Arrays        3

table, since it represents a first step toward capturing real program arrays. The
main contribution of [17] is to show that this enriched theory has quantifier-free
interpolants and its quantifier-free fragment is decidable. Still, some expressive
limitations (shared with the previous literature) persist: arrays are not forced
to be completely defined inside their allocation interval (when an array satis-
fies this property, we call it ‘contiguous’), because they might contain undefined
values in some location. Hence, strong length cannot be defined. Moreover, al-
though in [17] a complete terminating procedure for computing interpolants is
provided, a complexity upper bound is given only in the simple basic case where
indexes are just linear orders: for more complex arithmetical theories of indexes,
no complexity analysis is carried out and the algorithm becomes quite imprac-
tical, since it requires to fully instantiate universal quantifiers coming from the
theory axioms with index terms of arbitrarily large size.
    In this paper, we overcome all those limitations. For that purpose, we intro-
duce the very expressive theory of contiguous arrays with maxdiff CARD(TI )
(parameterized over an index theory TI ), which improves and strictly extends
the theory presented in [17] by requiring arrays to be all contiguous. This makes
the theory more adequate to represent arrays used in common programming
languages: for instance, strong length is now definable. Moreover, in contrast
to [17] where only amalgamation is shown, we prove here a strong amalgama-
tion result, when CARD(TI ) is enriched with ‘constant arrays’ of a fixed length
with a default value in all their locations. Notably, this not only yields that
quantifier-free interpolants exist, but also that interpolation is preserved under
disjoint signatures combinations and holds in presence of free function symbols
(see the definition of ‘general interpolation’ below). This result is completely
novel and particularly challenging to be proven, since it requires a sophisticated
model-theoretic machinery and a careful algebraic analysis of the class of all
models. We also radically re-design the interpolation algorithm, avoiding the
use of unbounded loops and of impractical full instantiation routines. Our new
algorithm reduces the computation of interpolants of a jointly unsatisfiable pair
of constraints to a polynomial size instance of the same problem in the un-
derlying index theory enriched with unary function symbols. As such, the new
algorithm becomes part of the hierarchical interpolation algorithms family [31]
and in particular formally resembles the algorithm presented in [35] for array
theory enriched with the basic diff symbol. We underline that one aspect mak-
ing our problems technically more challenging than similar problems investigated
in the literature is the fact that we handle a combination with very expressive
index theories: such a combination is non-disjoint because the total orderings on
indexes enter into the specification of the maxdiff and length axioms for arrays.

1.1   Plan of the paper
In the following, we call EUF the theory of equality and uninterpreted sym-
bols. We introduce two novel theories in Section 3: CARD(TI ), i.e., the theory
of contiguous arrays with maxdiff, and CARDC(TI ), which is an extension of
CARD(TI ) also containing ‘constant arrays’ of a fixed length with a default
4        S. Ghilardi et al.

value (called ‘el’) in all locations. The main technical results are that, for every
index theory TI :
 (i) CARDC(TI ) has general quantifier-free interpolation;
(ii) CARD(TI ) enjoys quantifier-free interpolation and such interpolants can be
     computed hierarchically by relying on a black-box interpolation algorithm for
     the weaker theory TI ∪ EUF (which has quantifier free interpolation because
     TI is strongly amalgamable, see Theorem 1).
     Result (i) is proved semantically, i.e., we show the equivalent strong amalga-
mation property (see Section 2 for the definitions). The semantic proof requires
dedicated constructions (Section 5), relying on some important facts about mod-
els and their embeddings (Section 4).
     The fact that CARD(TI ) has interpolants follows from the results in Section 5
(where we prove that this theory is amalgamable). Result (ii) is proved last (Sec-
tion 7); we first need an investigation on the solvability of the SM T (CARD(TI ))
problem (Section 6).
     We supply here some intuitions about our interpolation algorithm from Sec-
tion 7. The algorithm computes an interpolant out of a pair of (suitably prepro-
cessed) mutually unsatisfiable quantifier-free formulæ A0 , B 0 . We call common
the variables occurring in both A0 and B 0 . The existence of quantifier-free inter-
polants intuitively means that there are two reasoners, one for A0 and one for B 0 ,
the first (the second, resp.) of which operates on formulae involving only vari-
ables from A0 (B0 , resp.). The reasoners discover the inconsistency of A0 ∧B 0 by
exchanging information on the common language, i.e., by communicating each
other only the entailed quantifier-free formulae over the common variables. The
information exchange is hierarchical, i.e., it is limited to TI ∪EUF -formulæ: liter-
als from the richer language of CARD(TI ) and outside the language of TI ∪ EUF
can contribute to the information exchange only via instantiation of the univer-
sal quantifiers in suitable TI ∪ EUF -formulæ given in Section 3: these formulae,
as proved in Lemmas 2 and 4, supply equivalent definitions of such literals. In
contrast to [17], instantiations of universal quantifiers is limited to variables and
constants for efficiency.
     The main problem is to show that the above limited information exchange
is sufficient. This is the case thanks to the fact that the the algorithm manipu-
lates iterated diff operators [35],[17] (formally defined in Section 3) and it gives
names to all such operators when applied to common array variables. Both the
production of names for iterated diff-terms and the variable instantiations of
the universal quantifiers in the equivalent universal TI ∪ EUF -formulæ need in
principle to be repeated infinitely many times; what we prove (this is the content
of our main Theorem 7 below) is that a pre-determined polynomial size subset
of such manipulations is sufficient for the TI ∪ EUF -interpolation module to
produce the interpolant we are looking for.4
4
    One could reformulate this fact using the W -separability framework from [35]; how-
    ever, using this framework would not sensibly modify the proof of Theorem 7, so
    we preferred for space reasons and for simplicity to supply proofs within standard
    direct terminology.
     General Interpolation and Strong Amalgamation for Contiguous Arrays            5

Related work. We already mentioned the related work on first-order theories
axiomatizing arrays [22,20,7,17], which our theories of contiguous arrays strictly
extend. Since we adopt a hierarchical approach, our method is closely related
to hierarchical interpolation, where interpolants are computed by reduction to a
base theory treated as black-box. A non-exhaustive summary of this literature is
given by the approach in [28,29], where in the context of linear arithmetic general
interpolation is reduced to constraint solving, the one based on local extensions
in [30,31,32,31] and the one based on W -compatibility and finite instantiations
of [34,35].


2    Formal Preliminaries

We assume the usual syntactic (e.g., signature, variable, term, atom, literal, for-
mula, and sentence) and semantic (e.g., structure, sub-structure, truth) notions
of first-order logic. The equality symbol “=” is in all signatures. Notations like
E(x) mean that the expression (term, literal, formula, etc.) E contains free vari-
ables only from the tuple x. A ‘tuple of variables’ is a list of variables without
repetitions and a ‘tuple of terms’ is a list of terms (possibly with repetitions).
These conventions are useful for substitutions: we use them when denoting with
φ(t/x) (or simply with φ(t)) the formula obtained from φ(x) by simultaneous
replacement of the ‘tuple of variables’ x with the ‘tuple of terms’ t. A constraint
is a conjunction of literals. A formula is universal (existential ) iff it is obtained
from a quantifier-free formula by prefixing it with a string of universal (existen-
tial, resp.) quantifiers.

Theories and satisfiability modulo theory. A theory T is a pair (Σ, AxT ), where
Σ is a signature and AxT is a set of Σ-sentences, called the axioms of T (we shall
sometimes write directly T for AxT ). The models of T are those Σ-structures
in which all the sentences in AxT are true. A Σ-formula φ is T -satisfiable (or
T -consistent) if there exists a model M of T such that φ is true in M under
a suitable assignment a to the free variables of φ (in symbols, (M, a) |= φ); it
is T -valid (in symbols, T ⊢ ϕ) if its negation is T -unsatisfiable or, equivalently,
ϕ is provable from the axioms of T in a complete calculus for first-order logic.
A theory T = (Σ, AxT ) is universal iff all sentences in AxT are universal. A
formula ϕ1 T -entails a formula ϕ2 if ϕ1 → ϕ2 is T -valid (in symbols, ϕ1 ⊢T ϕ2
or simply ϕ1 ⊢ ϕ2 when T is clear from the context). If Γ is a set of formulæ and
φ a formula, Γ ⊢T φ means that there are γ1 , . . . , γn ∈ Γ such that γ1 ∧ · · · ∧
γn ⊢T φ. The satisfiability modulo the theory T (SMT(T )) problem amounts to
establishing the T -satisfiability of quantifier-free Σ-formulæ (equivalently, the
T -satisfiability of Σ-constraints). Some theories have special names, which are
becoming standard in SMT-literature, we shall recall some of them during the
paper. As already mentioned, we shall call EUF (Σ) (or just EUF ) the pure
equality theory in the signature Σ. A theory T admits quantifier-elimination iff
for every formula φ(x) there is a quantifier-free formula φ′ (x) such that T ⊢ φ ↔
φ′ .
6         S. Ghilardi et al.

Embeddings and sub-structures The support of a structure M is denoted with
|M|. For a (sort, constant, function, relation) symbol σ, we denote as σ M the
interpretation of σ in M. Let M and N be two Σ-structures; a Σ-embedding (or,
simply, an embedding) µ : M −→ N is an injective function from |M| into |N |
that preserves and reflects the interpretation of functions and relation symbols
(see, e.g., [10] for the formal definition). If such an embedding is a set-theoretical
inclusion, we say that M is a substructure of N or that N is a superstructure
of M. As it is known, the truth of a universal (resp. existential) sentence is
preserved through substructures (resp. superstructures).
    Given a signature Σ and a Σ-structure M, we indicate with ∆Σ (M) the
diagram of M: this is the set of sentences obtained by first expanding Σ with a
fresh constant ā for every element a from |M| and then taking the set of ground
Σ ∪ |M|-literals which are true in M (under the natural expanded interpreta-
tion mapping ā to a). An easy but nevertheless important basic result (to be
frequently used in our proofs), called Robinson Diagram Lemma [10], says that,
given any Σ-structure N , there is an embedding µ : M −→ N iff N can be
expanded to a Σ ∪ |M|-structure in such a way that it becomes a model of
∆Σ (M).

Combinations of theories. A theory T is stably infinite iff every T -satisfiable
quantifier-free formula (from the signature of T ) is satisfiable in an infinite model
of T . By compactness, it is possible to show that T is stably infinite iff every
model of T embeds into an infinite one (see, e.g., [16]). Let Ti be a stably-infinite
theory over the signature Σi such that the SM T (Ti ) problem is decidable for
i = 1, 2 and Σ1 and Σ2 are disjoint (i.e., the only shared symbol is equality).
Under these assumptions, the Nelson-Oppen combination result [26] says that the
SMT problem for the combination T1 ∪ T2 of the theories T1 and T2 is decidable.
Nelson-Oppen result trivially extends to many-sorted languages.

Interpolation properties. In the introduction, we roughly stated Craig’s interpo-
lation theorem [10]. In this paper, we are interested to specialize this result to the
computation of quantifier-free interpolants modulo (combinations of) theories.
Definition 1. [Plain quantifier-free interpolation] A theory T admits (plain)
quantifier-free interpolation iff for every pair of quantifier-free formulae φ, ψ
such that ψ ∧ φ is T -unsatisfiable, there exists a quantifier-free formula θ, called
an interpolant, such that: (i) ψ T -entails θ, (ii) θ ∧ φ is T -unsatisfiable, and
(iii) only the variables occurring in both ψ and φ occur in θ.
  In verification, the following extension of the above definition is considered
more useful.
Definition 2. [General quantifier-free interpolation] Let T be a theory in a sig-
nature Σ; we say that T has the general quantifier-free interpolation property
iff for every signature Σ ′ (disjoint from Σ) and for every pair of ground Σ ∪ Σ ′ -
formulæ φ, ψ such that φ∧ψ is T -unsatisfiable,5 there is a ground formula θ such
5
    By this (and similar notions) we mean that φ ∧ ψ is unsatisfiable in all Σ ′ -structures
    whose Σ-reduct is a model of T .
     General Interpolation and Strong Amalgamation for Contiguous Arrays             7

that: (i) φ T -entails θ; (ii) θ ∧ ψ is T -unsatisfiable; (iv) all relations, constants
and function symbols from Σ ′ occurring in θ also occur in φ and ψ.
By replacing free variables with free constants, it is easily seen that the general
quantifier-free interpolation property (Definition 2) implies the plain quantifier-
free interpolation property (Definition 1); the converse implication does not hold,
however (a counterexample can be found in this paper too, see Example 1 below).

Amalgamation and strong amalgamation. Interpolation can be characterized se-
mantically via amalgamation.
Definition 3. A universal theory T has the amalgamation property iff, given
models M1 and M2 of T and a common submodel A of them, there exists a
further model M of T (called T -amalgam) endowed with embeddings µ1 : M1 −→
M and µ2 : M2 −→ M whose restrictions to |A| coincide.
    A universal theory T has the strong amalgamation property [21] if the
above embeddings µ1 , µ2 and the above model M can be chosen so to satisfy
the following additional condition: if for some m1 ∈ |M1 |, m2 ∈ |M2 | we have
µ1 (m1 ) = µ2 (m2 ), then there exists an element a in |A| such that m1 = a = m2 .
   The first point of the following theorem is an old result due to [3]; the second
point is proved in [8] (where it is also suitably reformulated for theories which
are not universal):

Theorem 1. Let T be a universal theory. Then

(i) T has the amalgamation property iff it admits quantifier-free interpolants;
(ii) T has the strong amalgamation property iff it has the general quantifier-free
     interpolation property.

   We underline that, in presence of stable infiniteness, strong amalgamation is
a modular property (in the sense that it transfers to signature-disjoint unions of
theories), whereas amalgamation is not (see again [8] for details). As a special
case, since EUF has strong amalgamation and is stably infinite, the following
result follows:

Theorem 2. If T is stably infinite and has strong amalgamation, so does T ∪
EUF .


3    Arrays with MaxDiff

The McCarthy theory of arrays [22] has three sorts ARRAY, ELEM, INDEX (called
“array”, “element”, and “index” sort, respectively) and two function symbols rd
(“read”) and wr (“write”) of appropriate arities; its axioms are:

                    ∀y, i, e. rd(wr(y, i, e), i) = e
                  ∀y, i, j, e. i 6= j → rd(wr(y, i, e), j) = rd(y, j).
8        S. Ghilardi et al.

Arrays with extensionality have the further axiom

                       ∀x, y.x 6= y → (∃i. rd(x, i) 6= rd(y, i)),                   (1)

called the ‘extensionality’ axiom. This theory is not universal and does not have
quantifier-free interpolants. Here, we want to introduce a variant of this theory
where Axiom (1) is skolemized via a function diff with a precise semantic
interpretation: it returns the biggest index where two different arrays differ. We
first need the notion of index theory.
Definition 4. [17] An index theory TI is a mono-sorted theory (INDEX is its
sort) satisfying the following conditions:
  - TI is universal, stably infinite and has the general quantifier-free interpola-
    tion property (i.e., it is strongly amalgamable, see Theorem 1);
  - SM T (TI ) is decidable;
  - TI extends the theory T O of linear orderings with a distinguished element 0.
We recall that T O is the theory whose only proper symbols (beside equality) are
a binary predicate ≤ and a constant 0 subject to the axioms saying that ≤ is
reflexive, transitive, antisymmetric and total. Thus, the signature of TI contains
at least the binary relation symbol ≤ and the constant 0. In the paper, when we
speak of a TI -term, TI -atom, TI -formula, etc. we mean a term, atom, formula in
the signature of TI . Below, we use the abbreviation i < j for i ≤ j ∧ i 6= j. The
constant 0 is used to separate ‘positive’ indexes - those satisfying 0 ≤ i - from
the remaining ‘negative’ ones.
    Examples of index theories are T O itself, integer difference logic IDL, integer
linear arithmetic LIA, and real linear arithmetics LRA. In order to match the
requirements of Definition 4, one need however to make a careful choice of the
language (see [8] for details): most importantly, notice that integer (resp., real)
division by all positive integers should be added to the language of LIA (resp.
LRA). For most applications, IDL (which is the theory of integer numbers
with 0, ordering, successor and predecessor) is sufficient as in this theory one
can model counters for scanning arrays.
    Given an index theory TI , we can now introduce our contiguous array theory
with maxdiff CARD(TI ) (parameterized by TI ) as follows. We still have three
sorts ARRAY, ELEM, INDEX; the language includes the symbols of TI , the read and
write operations wr, rd, a binary function diff of type ARRAY × ARRAY → INDEX,
a unary function |−| of type ARRAY → INDEX, as well as constant ⊥, el of sort
ELEM. The constant ⊥ models an undefined value; the term diff(x, y) returns
the maximum index where x and y differ and returns 0 if x and y are equal. 6
The term |a| indicates the (strong) length of a, meaning that a is allocated in
the interval [0, |a|] and undefined outside. Formally, the axioms of CARD(TI )
include, besides the axioms of TI , the following ones:

                               ∀y, i, e, |wr(y, i, e)| = |y|                        (2)
6
    Notice that it might well be the case that diff(x, y) = 0 for different x, y, but in
    that case 0 is the only index where x, y differ.
     General Interpolation and Strong Amalgamation for Contiguous Arrays            9

                               ∀y, i, wr(y, i, ⊥) = y                             (3)
              ∀y, i, e, (e 6= ⊥ ∧ 0 ≤ i ≤ |y|) → rd(wr(y, i, e), i) = e           (4)
                  ∀y, i, j, e, i 6= j → rd(wr(y, i, e), j) = rd(y, j)             (5)
                         ∀y, i, rd(y, i) 6= ⊥ ↔ 0 ≤ i ≤ |y|                       (6)
                                     ∀y, |y| ≥ 0                                  (7)
                                 ∀y, diff(y, y) = 0                               (8)
              ∀x, y, x 6= y → rd(x, diff(x, y)) 6= rd(y, diff(x, y)).             (9)
                   ∀x, y, i, diff(x, y) < i → rd(x, i) = rd(y, i).               (10)
                                       ⊥ 6= el.                                  (11)
    Axiom (11) prevents the ELEM sort to contain just ⊥ (thus trivializing a
model). Since an array a is fully allocated only in the interval [0, |a|], any reading
or writing attempt outside that interval should produce some runtime error;
similarly, it should be impossible to overwrite ⊥ inside that interval. In our
declarative context, there is nothing like a ‘runtime error’, so we assume that
such illegal operations simply do not produce any effect. However, when applying
the theory to code annotations, the verification conditions should include that
no memory violation like the above ones occur (that is, when, e.g., a term like
rd(b, i) occurs, it should be accompanied by the proviso annotation 0 ≤ i ≤ |a|,
etc.).
    As we shall see the above theory enjoys amalgamation (i.e., plain quantifier-
free interpolation) but not strong amalgamation (i.e., it lacks the general
quantifier-free interpolation). To restore it, it is sufficient to add some (even
limited) support for constant arrays: we call the related theory CARDC(TI ).
The extension is interesting by itself, because it increases the expressivity of the
language: in CARDC(TI ), applying the wr operation to terms Const(i), one can
encode all finite lists (if TI has a reduct to IDL). Formally, CARDC(TI ) has an
additional unary function Const : INDEX → ARRAY, constrained by the following
axioms:
                               ∀i, |Const(i)| = max(i, 0).                        (12)
              ∀i, j, (0 ≤ j ∧ j ≤ |Const(i)| → rd(Const(i), j) = el).            (13)
(we assume without loss of generality that max is a symbol of TI - in fact it is
definable in it).
    The following easy facts will be often used in our proofs:

Lemma 1. The following formulæ are CARD(TI )-valid

                      |a| 6= |b| → diff(a, b) = max(|a|, |b|)                    (14)

                    max(diff(a, b), diff(b, c)) ≥ diff(a, c) .                   (15)

   The next lemma follows from the axioms of CARD(TI ):
10      S. Ghilardi et al.

Lemma 2. An atom like a = b is equivalent (modulo CARD(TI )) to

                        diff(a, b) = 0 ∧ rd(a, 0) = rd(b, 0) .                   (16)

An atom like a = wr(b, i, e) is equivalent (modulo CARD) to the conjunction of
the following formulae

                             (e 6= ⊥ ∧ 0 ≤ i ≤ |b|) → rd(a, i) = e
                   (i < 0 ∨ i > |b| ∨ e = ⊥) → rd(a, i) = rd(b, i)               (17)
                               ∀h (h 6= i → rd(a, h) = rd(b, h)).

An atom of the kind |a| = i is equivalent to:

                     i ≥ 0 ∧ ∀h (rd(a, h) 6= ⊥ ↔ 0 ≤ h ≤ i).                     (18)


Lemma 3. An atom like Const(i) = a is equivalent (modulo CARDC(TI )) to

                     |a| = i ∧ ∀h (0 ≤ h ≤ i → rd(a, h) = el) .                  (19)


    Similarly to [35] and [17], we now introduce iterated diff operations, that
will be used in our interpolation algorithm. In fact, in addition to diff := diff1
we need an operator diff2 that returns the last-but-one index where a, b differ
(0 if a, b differ in at most one index), an operator diff3 that returns the last-
but-two index where a, b differ (0 is they differ in at most two indexes), etc. Our
language is already sufficiently expressive for that. Indeed, given array variables
a, b, we define by mutual recursion the sequence of array terms b1 , b2 , . . . and of
index terms diff1 (a, b), diff2 (a, b), . . . :

                       b1 := b; diff1 (a, b) := diff(a, b1 );
                bk+1 := wr(bk , diffk (a, b), rd(a, diffk (a, b)));
                                  diffk+1 (a, b) := diff(a, bk+1 );

                                       V
    A useful fact is that formulae like j<l diffj (a, b) = kj can be eliminated in
favor of universal clauses in a language whose only symbol for array variables is
rd. In detail:


Lemma 4. A formula like

                    diff1 (a, b) = k1 ∧ · · · · · · ∧ diffl (a, b) = kl          (20)
     General Interpolation and Strong Amalgamation for Contiguous Arrays           11

is equivalent modulo CARD(TI ) to the conjunction of the following seven for-
mulae:
                                         k1 ≥ k2 ∧ ... ∧ kl−1 ≥ kl ∧ kl ≥ 0
                                 ^
                                       (kj > kj+1 → rd(a, kj ) 6= rd(b, kj ))
                                 j<l
                                       ^
                                             (|a| = |b| ∧ kj = kj+1 ) → kj = 0
                                       j<l
                                       ^                                          (21)
                                             (rd(a, kj ) = rd(b, kj ) → kj = 0)
                                       j≤l

           ∀h (h > kl → rd(a, h) = rd(b, h) ∨ h = k1 ∨ ... ∨ h = kl−1 )
                                      |a| > |b| → (k1 = kl ∧ kl = |a|)
                                              |b| > |a| → (k1 = kl ∧ kl = |b|).

4   Embeddings
In this section we present some useful facts about embeddings that will be crucial
in the proofs throughout the paper.
    We first introduce the third array theory ARext (TI ), which is weaker than
CARD(TI ), lacks the diff symbol and axiom (10) is replaced by the following
extensionality axiom:
                     ∀x, y, x 6= y → (∃i, rd(x, i) 6= rd(y, i)).                  (22)
Notice that ARext (TI ) ⊆ CARD(TI ) ⊆ CARDC(TI ) (the inclusion holds both
for signatures and for axioms). To simplify the statements of some lemmas be-
low, let us also introduce the theory CARC ext (TI ): this theory is obtained from
ARext (TI ) by adding the function symbol Const to the signature and the sen-
tences (12),(13) to the axioms.
     We now discuss the class of models of ARext (TI ) and we clarify the impor-
tant features of embeddings between such models. A model M of ARext (TI ) is
functional when the following conditions are satisfied:
 (i) ARRAYM is a subset of the set of all positive-support functions from INDEXM
     to ELEMM (a function a is positive-support iff there exists an index |a| such
     that |a| ≥ 0 and, for every j, a(j) 6= ⊥ iff j ∈ [0, |a|]);
(ii) rd is function application;
(iii) wr is the point-wise update operation inside the interval [0, |a|] (i.e., func-
     tion wr(a, i, e) returns the same values as function a, except at the index i
     and only in case i ∈ [0, |a|]: in this case it returns the element e);
(iv) if M is also a model of CARC ext (TI ), then the set ARRAYM contains the
     positive-support functions with value elM inside their support.
Because of the extensionality axiom (22), it can be shown that every model of
ARext (TI ) or of CARC ext (TI ) is isomorphic to a functional one. For an array
a ∈ INDEXM in a functional model M and for i ∈ INDEXM , since a is a function,
we interchangeably use the notations a(i) and rd(a, i).
12      S. Ghilardi et al.

    Let a, b be elements of ARRAYM in a model M. We say that a and b are
cardinality equivalent iff |a| = |b| and {i ∈ INDEXM | M |= rd(a, i) 6= rd(b, i)} is
finite. This relation in M is an equivalence, that we denote as ∼M or simply as
∼. We also write M |= a ∼ b to say that a ∼M b holds.

Lemma 5. Let N , M be models of ARext (TI ) such that M is a substructure
of N . For every a, b ∈ ARRAYM , we have that

                             M |= a ∼ b iff N |= a ∼ b.

    In a functional model M of ARext (TI ), we say that diff(a, b) is defined iff
there is a maximum index where a, b differ (or if a = b). If in the model M the
index sort INDEX is interpreted as the set of the integers, with standard order-
ing, then for any two positive-support functions a, b, we have that diff(a, b) is
defined. However, this will not be the case if the index sort INDEX is interpreted,
e.g., in some non-standard model of the integers. We must take into considera-
tions these models too, since we want to prove amalgamation. For this purpose,
we need to build amalgams for all models of the theory (only in that case in
fact, amalgamation turns out to be equivalent to quantifier-free interpolation).
Thus, we are forced to take into consideration below also phenomena that might
arise only in non-standard models.
    An embedding µ : M −→ N between ARext (TI )-models (or of CARC ext (TI )-
models) is said to be diff-faithful iff, whenever diff(a, b) is defined, so is
diff(µ(a), µ(b)) and it is equal to µ(diff(a, b)). Since there might not be a
maximum index where a, b differ, in principle it is not always possible to expand
a functional model of ARext (TI ) to a functional model of CARD(TI ), if the set
of indexes remains unchanged. Indeed, in order to do that in a diff-faithful way,
one needs to explicitly add to INDEXM new indexes including at least the ones
representing the missing maximum indexes where two given array differ. This
idea leads to Theorem 3 below, which is the main result of the current section.

Theorem 3. For every index theory TI , every model M of ARext (TI ) (resp. of
CARC ext (TI )) has a diff-faithful embedding into a model of CARD(TI ) (resp.
of CARDC(TI )).

Proof. It is sufficient to well-order the pairs a, b ∈ INDEXM such that diff(a, b)
is not defined in M, apply to each pair the contruction of the next lemma (taking
unions at limit ordinals), and then repeat the whole construction ω times, taking
union again.

Lemma 6. Let M be a model of ARext (TI ) (resp. of CARC ext (TI )) and let
a, b ∈ ARRAYM be such that diffM (a, b) is not defined. Then there are a model N
of ARext (TI ) (resp. of CARC ext (TI )) and a diff-faithful embedding µ : M → N
such that diffN (a, b) is defined.

Proof. We can assume that ELEMM has at least an element e, different from
⊥M , elM (for details, see Lemma 10 in the appendix). We must have |a| = |b|,
otherwise diff(a, b) is defined and it is max(|a|, |b|) according to Lemma 1.
      General Interpolation and Strong Amalgamation for Contiguous Arrays    13

   Let I = {i ∈ INDEXM | a(i) 6= b(i)} be the set of indices without maximum
element (hence infinite) where they differ. Let ↓ I := {j ∈ INDEXM | ∃i ∈ I, j ≤
i} ⊇ I. The condition

                    (+) “∃i ∈ I ∀j ∈ I (j ≥ i → x(j) = el)”

cannot be satisfied both for x = a and x = b (see the appendix). In case one of
them satisfies it, we assume it is b.
   Let ∆ be the Robinson diagram of the TI -reduct of M and let k0 be a new
constant; let us introduce the set

           ∆′ := ∆ ∪ {i < k0 | i ∈ ↓ I} ∪ {k0 < i | i ∈ INDEXM \ ↓ I}.

By compactness theorem and since I is infinite, the set ∆′ turns out to be
consistent (see again the appendix for details).
    By Robinson Diagram Lemma, there exists a model A of TI extending the
TI -reduct of M; such A contains in its support an element k0 such that

                                ∀i ∈ ↓ I, i < k0 ,

                           ∀i ∈ INDEXM \ ↓ I, k0 < i.
    We now take ELEMN = ELEMM , INDEXN = INDEXA ; we let also ARRAYN to be
the set of all positive-support functions from INDEXN into ELEMN (notice that
this N is trivially also a model of CARC ext (TI )). We observe that k0 < |a|M
and recall that |a|M = |b|M .
    Let us now define the embedding µ : M → N ; at the level of the sorts INDEX
and ELEM, we use inclusions. For the ARRAY sort, we need to specify the value
µ(c)(k) for c ∈ ARRAYM and k ∈ INDEXN \ INDEXM (for the other indices we
keep the old M-value to preserve the read operation). Our definition for µ must
preserve the maxdiff index (whenever already defined in M) and must guarantee
that diffN (µ(a), µ(b)) = k0 (by construction, we have k0 > 0). For a generic
array c ∈ ARRAYM , we operate as follows:
 1. if |c|M < k0 we put µ(c)(k0 ) = ⊥M , otherwise:
 2. if the condition (⋆) below holds, we put µ(c)(k0 ) = e,
 3. if such condition does not hold, we put µ(c)(k0 ) = elM .
The condition (⋆) is specified as follows:
(⋆)   there is i ∈ I such that for all j ∈ I, j ≥ i we have c(j) = a(j).
For all the remaining indexes k ∈ INDEXN \ (INDEXM ∪ {k0 }):
                                 (
                                   ⊥M , if k ∈
                                             / [0, |c|M ]
                       µ(c)(k) =                                            (23)
                                   el , if k ∈ [0, |c|M ].
                                     M


Notice that we have µ(a)(k0 ) = e 6= elM = µ(b)(k0 ) (because I is infinite and
does not have maximum, hence condition (⋆) holds for a but not for b). In
addition:
14     S. Ghilardi et al.

• for all i ∈ INDEXM such that k0 < i, we have i ∈      / ↓ I (according to the
  construction of k0 ) and consequently i ∈
                                          / I, that is a(i) = b(i);
• for all i ∈ INDEXN \ (INDEXM ∪ {k0 }) such that k0 < i, since we have |a|M =
  |b|M , we get
                         µ(a)(i) = ⊥M iff µ(b)(i) = ⊥M ,

                            µ(a)(i) = elM iff µ(b)(i) = elM .
Hence, we can conclude that diffN (µ(a), µ(b)) is defined and equal to k0 .
    We only need to check that our µ preserves rd, |−|, wr, constant arrays and
diff (whenever defined). For preservation of constant arrays, we need to prove
only that µ(Const(i))(k0 ) = elM in case k0 < i: this is clear, because a does not
satisfy (+), hence (⋆) does not hold for Const(i). The other cases are proved in
the appendix.


5     Strong Amalgamation for CARDC(TI )

In this section, we prove that the most expressive theory of the paper
CARDC(TI ) has strong amalgamation. However, we also show that this is not
the case for CARD(TI ) (even if it is amalgamable). We recall that strong amal-
gamation holds for models of TI (see Definition 4): this observation is crucial for
the following.
    Strong amalgamation of CARDC(TI ) will be proved in two steps. First, we
provide the amalgam construction for CARDC(TI ), where we also notice that
the same arguments can be used to prove that CARD(TI ) has amalgamation too.
Then, after exhibiting a counterexample showing that the strong amalgamation
fails for CARD(TI ), we check that the amalgam construction for CARDC(TI )
satisfies the condition for being a CARDC(TI )-strong amalgam.


5.1   Amalgam constructions

Let M1 and M2 be two models of CARDC(TI ) (resp. of CARD(TI )); we want to
amalgamate them over their common substructure A and let fi be the embedding
of A into Mi (we assume that fi is just inclusion for the INDEX and ELEM
components). We can assume w.l.o.g. that our models are all functional and, by
applying renaming, that

              (INDEXM1 \ INDEXA ) ∩ (INDEXM2 \ INDEXA ) = ∅

                 (ELEMM1 \ ELEMA ) ∩ (ELEMM2 \ ELEMA ) = ∅.
We build the amalgamated model in two steps. We first embed M1 and M2 , via
the embeddings µi (i=1,2), into a model M of CARC ext (TI ) (resp., of ARext (TI ))
in a diff-faithful way. Then M is embedded, via another diff-faithful embed-
ding µ′ into a model M̂ of CARDC(TI ) (resp., of CARD(TI )): µ′ is guaranteed
       General Interpolation and Strong Amalgamation for Contiguous Arrays              15

to exist by Theorem 3.

                                        M1
                               f1                 µ1

                                                           µ′
                        A                              M         M̂
                                             µ2
                               f2
                                        M2


Construction of µi
We build the model M and the two diff-faithful embeddings µi : Mi → M
such that µ1 ◦ f1 = µ2 ◦ f2 .
We let INDEXM be a strong amalgam of INDEXM1 and INDEXM2 (TI enjoys strong
amalgamation), whereas we let ELEMM = ELEMM1 ∪ ELEMM2 . Let ARRAYM be
the set of all positive-support functions from INDEXM into ELEMM .
The INDEX and ELEM components of the embeddings µi will be inclusions. The
definition of the value of µi (a)(k), for a ∈ ARRAYMi and k ∈ INDEXM , is given
by cases as follows:
• if k ∈ INDEXMi , we put µi (a)(k) = a(k);
• if k ∈ INDEXM3−i \ INDEXA : let (2⋆) be the relation7
                         ′′
                              there exist c ∈ ARRAYA , b ∈ ARRAYMi
                               s.t. b ∼Mi a, k > diffMi (b, fi (c))′′ ,
                              
                              f3−i (c)(k), if (2⋆) holds
             µi (a)(k) =        ⊥M ,                                    / [0, |a|Mi ]
                                              if (2⋆) does not hold & k ∈
                                elM ,         if (2⋆) does not hold & k ∈ [0, |a|Mi ]
                              

       / INDEXMi ∪ INDEXM3−i , we put
• if k ∈
                                    (
                                      ⊥M ,                  / [0, |a|Mi ]
                                                       if k ∈
                        µi (a)(k) =
                                      elM ,            if k ∈ [0, |a|Mi ].

     We need to prove that the functions µi : (i) are well-defined, (ii) are injective,
(iii) preserve |−|, (iv) preserve rd and wr, (v) preserve diff, (vi) satisfy the
condition µ1 ◦ f1 = µ2 ◦ f2 , (vii) preserve constant arrays (this point is not
needed for CARD(TI )). These checks require a careful analysis of all the cases:
all the details can be found in the appendix.
     As a consequence of these constructions, we get the following result for both
CARDC(TI ) and CARD(TI ).
Theorem 4. CARD(TI ) and CARDC(TI ) enjoy the amalgamation property.
7
    When we write k > diffMi (b, fi (c)) we mean in fact that k > µi (diffMi (b, fi (c)))
    (this relation is meant to hold in M). Our simplified notation is justified by the fact
    that µi is inclusion for INDEX sort.
16       S. Ghilardi et al.

5.2     The CARDC(TI )-amalgam is strong
We now prove the main result of the section, i.e., strong amalgamation for
CARDC(TI ). Unfortunately, this property does not hold for CARD(TI ): as it
is shown in the example below, we need constant arrays in the language (recall
that strong amalgamation is equivalent to general quantifier-free interpolation,
see Theorem 1(ii)).
Example 1. Consider the following two formulae (where P is a free predicate
symbol):
                         (A)   |a| = 0 ∧ rd(a, 0) = e ∧ P (a)
                        (B)    |b| = 0 ∧ rd(b, 0) = e ∧ ¬P (b).
The conjunction (A) ∧ (B) is inconsistent because a and b are in fact the same
array (because of Axioms 6 and 9). However, the only common variable is e; to
get the interpolant, we can use P (wr(Const(0), 0, e)), but then it is clear that
the language lacking constant arrays does not suffice.                          ⊣
Theorem 5. CARDC(TI ) has strong amalgamation.
Proof. We keep the same notation and construction as in the proof of Theorem 4.
However, it can be proved (for details, see Lemma 12 in the appendix) that all
arrays a ∈ ARRAYMi (for i = 1, 2) whose length belongs to INDEXA can be
assumed to be s.t. one of the following two conditions are satisfied:
 1. there exists c ∈ ARRAYA with fi (c) ∼Mi a;
 2. there exists ka ∈ INDEXMi \ INDEXA such that a(ka ) is an element from
    ELEMMi \ ELEMA different from all the fi (c)(ka ), varying c ∈ ARRAYA .
      Let ai ∈ ARRAYMi (i = 1, 2) be s. t. ∀k ∈ INDEXM we have
                               µ1 (a1 )(k) = µ2 (a2 )(k).                       (24)
Notice that, since TI has the strong amalgamation property and the µi preserve
length, this can only happen if |a1 | = |a2 | belongs to INDEXA . We look for some
c ∈ ARRAYA such that a1 = f1 (c); since µ2 is injective this would entail a2 = f2 (c)
because µ2 (a2 ) = µ1 (a1 ) = µ1 (f1 (c)) = µ2 (f2 (c)), implying that M̂ is a strong
amalgam, as requested.
     We separate two cases: (i) one of the arrays a1 , a2 satisfy condition 2; (ii)
both arrays a1 , a2 satisfy condition 1.
 (i) This case is impossible: this is proved in the appendix, by exploiting condi-
     tion 2 and the definition of µ2 via rule (2⋆).
(ii) Hence, we have µ1 (a1 ) = µ2 (a2 ) only when both a1 , a2 satisfy condition 1.
     Let ci ∈ ARRAYA (i = 1, 2) be the arrays s.t. fi (ci ) ∼Mi ai . In the appendix,
     we prove how to build, from c2 , a c ∈ ARRAYA such that f1 (c) = a1 .
   Strong amalgamation corresponds to general quantifier-free interpolation
(Theorem 1), hence we obtain that:
Corollary 1. The theory CARDC(TI ) has the general quantifier-free interpola-
tion property.
      General Interpolation and Strong Amalgamation for Contiguous Arrays               17

6    Satisfiability

We now address the problem of checking satisfiability of quantifier-free formulæ
in our theories. Decidability of the SM T (CARD(TI ))- and SM T (CARDC(TI ))-
problems, at least in the relevant case where TI is any fragment of Presburger
arithmetics, can be solved by reduction to the satisfiability problem for the
so-called ‘array-property fragment’ of [5]: the reduction can be obtained by
eliminating the wr, |−|, diff and Const symbols in favor of universally quantified
formulæ belonging to that fragment (see Lemmas 2,3,4). However, we now supply
a decision procedure for quantifier-free formulæ, since this will be useful for the
interpolation algorithm in Section 7.
    A flat literal L is a formula of the kind x0 = f (x1 , . . . , xn ) or x1 6= x2
or R(x1 , . . . , xn ) or ¬R(x1 , . . . , xn ), where the xi are variables, R is a relation
symbol, and f is a function symbol. If I is a set of TI -terms, an I-instance of a
universal formula of the kind ∀i φ is a formula of the kind φ(t/i) for some t ∈ I.

Definition 5. A pair of sets of quantifier-free CARD(TI )-formulæ Φ = (Φ1 , Φ2 )
is a separated pair iff
(1) Φ1 contains equalities of the form |a| = i, diffk (a, b) = i and a = wr(b, i, e);
    moreover if it contains the equality diffk (a, b) = i, it must also contain
    an equality of the form diffl (a, b) = j for every l < k; finally, if Φ1 ∪ Φ2
    contains occurrences of an array variable a, Φ1 must contain also an equality
    of the form |a| = i;
(2) Φ2 contains Boolean combinations of TI -atoms and of atoms of the forms:

                       rd(a, i) = rd(b, j), rd(a, i) = e, e1 = e2 ,                   (25)

    where a, b, i, j, e, e1, e2 are variables or constants of the appropriate sorts.
Φ is said to be finite iff Φ1 and Φ2 are both finite.

    Notably, in a separated pair Φ = (Φ1 , Φ2 ), if we introduce a unary function
symbol fa for every array variable a and rewrite rd(a, i) as fa (i), it turns out that
the formulæ from Φ2 can be seen as formulæ of the combined theory TI ∪ EUF .
TI ∪ EUF is decidable in its quantifier-free fragment and admits quantifier-free
interpolation because TI is an index theory (see Nelson-Oppen results [26] and
Theorems 1,2): we adopt a hierarchical approach (similarly to [31,33]) and we
rely on satisfiability and interpolation algorithms for such a theory as black boxes.

Definition 6. Let I be a set of TI -terms and let Φ = (Φ1 , Φ2 ) be a separated
pair; Φ(I) = (Φ1 (I), Φ2 (I)) is the smallest separated pair satisfying the following
conditions:
  - Φ1 (I) is equal to Φ1 and Φ2 (I) contains Φ2 ;
  - if Φ1 contains the atom a = wr(b, i, e) then Φ2 (I) contains all the I-instances
    of the formulae (17) (with the terms |a|, |b| replaced by the index constants
    i, j such that |a| = i, |b| = j ∈ Φ1 , respectively);
  - if Φ1 contains the atom |a| = i, then Φ2 (I) contains all the I-instances of
    the formulae (18);
18      S. Ghilardi et al.

  - if Φ1 contains the conjunction li=1 diffi (a, b) = kl , then Φ2 (I) contains
                                        V
    the formulae (21) (with the terms |a|, |b| replaced by the index constants i, j
    such that |a| = i, |b| = j ∈ Φ1 , respectively).
A separated pair Φ is 0-instantiated iff Φ = Φ(I), where I is the set of index
variables occurring in I.

                        V pair Φ = (Φ1 , Φ2 ) is is CARD(TI )-satisfiable iff so
     We say that aVseparated
it is the formula Φ1 ∧ Φ2 .

Lemma 7. Let φ be a quantifier-free formula; then it is possible to compute
in linear time a finite separation pair Φ = (Φ1 , Φ2 ) such that φ is CARD(TI )-
satisfiable iff so is Φ.

Lemma 8. The following conditions are equivalent for a finite 0-instantiated
separation pair Φ = (Φ1 , Φ2 ):
(i) ΦV is CARD(TI )-satisfiable;
(ii)   Φ2 is TI ∪ EUF -satisfiable.

     From Lemmas 7 and 8, we get the following result:

Theorem 6. The SM T (CARD(TI )) problem is decidable for every index theory
TI .

    Regarding complexity for the SM T (CARD(TI )) problem, notice that the
satisfiability of the quantifier-free fragment of common index theories (like IDL,
LIA, LRA) is decidable in NP; hence, for such index theories, an NP bound
for our SM T (CARD(TI ))-problems is easily obtained, because 0-instantiation is
clearly finite and polynomial (all strings of universal quantifiers to be instantiated
have length one).
    The above decidability and complexity results apply also to CARDC(TI ): one
only simply has to allow the Φ1 -component of a separation pair to contain also
atoms of the form Const(i) = a and Definition 6 to require that Φ2 (I) contains
all the I-instances of the formulae (19) in case Const(i) = a ∈ Φ1 .


7     The interpolation algorithm

Since amalgamation is equivalent to quantifier-free interpolation for universal
theories such as CARD(TI ) and CARDC(TI ) (thanks to Theorem 1), Theorem 4
guarantees that CARD(TI ) and CARDC(TI ) admit quantifier-free interpolation.
However, the proof of Theorem 4 is not constructive: hence, in order to compute
an interpolant for an unsatisfiable conjunction like ψ(x, y) ∧ φ(y, z), one needs in
principle to enumerate all quantifier-free formulæ θ(y) that are consequences of
φ and are inconsistent with ψ. Since the quantifier-free fragments of CARD(TI )
and CARDC(TI ) are decidable, this is an effective procedure and, considering
the fact that interpolants of jointly unsatisfiable pairs of formulæ exist, it also
terminates. However, this type of algorithm is not practical. In this section, we
      General Interpolation and Strong Amalgamation for Contiguous Arrays        19

provide a better and more practical algorithm that relies on a hierarchical re-
duction to TI ∪EUF . Our algorithm works for CARD(TI ) only; for CARDC(TI ),
we make some comments in Section 8.
     Our problem is the following: given two quantifier-free formulae A0 and B 0
such that A0 ∧B 0 is not satisfiable (modulo CARD(TI )), to compute a quantifier-
free formula C such that
   (i) CARD(TI ) |= A0 → C;
  (ii) CARD(TI ) |= C ∧ B 0 → ⊥;
 (iii) C contains only the variables (of sort INDEX, ARRAY, ELEM) which occur
       both in A0 and in B 0 .
     Below, we work with ground formulae over signatures expanded with free
constants instead of quantifier-free formulae. We use letters A, B, . . . for finite
sets of ground formulae; the logical reading of a set of formulae is the conjunction
of its elements. For a signature Σ and a set A of formulae, Σ A denotes the
signature Σ expanded with the free constants occurring in A. Let A and B
be two finite sets of ground formulae in the signatures Σ A and Σ B , resp., and
Σ C := Σ A ∩ Σ B . We ‘color’ a term, a literal, or a formula ϕ by calling it:
• AB-common iff it is defined over Σ C ;
• A-local (resp. B-local) if it is defined over Σ A (resp. Σ B );
• A-strict (resp. B-strict) iff it is A-local (resp. B-local) but not AB-common;
• strict if it is either A-strict or B-strict.
     There are a number of manipulations that can be freely applied to a jointly
unsatisfiable pair A, B without compromising the possibility of extracting an
interpolant out of them. A list of such manipulations (called ‘metarules’) is
supplied in [7], [8]. Here we need to introduce only some of them:
   (i) we can add to A an A-local quantifier-free formula entailed by A (similarly
       we can add to B a B-local quantifier-free formula entailed by B): the
       interpolant computed after such a transformation is trivially an interpolant
       for the original pair too;
  (ii) we can pick an A-local term t and a fresh constant x (to be considered A-
       strict from now on) and add to A the equality x = t: again, the interpolant
       computed after such a transformation is trivially an interpolant for the
       original pair too (the same observation extends to B);
 (iii) we can pick an AB-common term t and a fresh constant x (to be considered
       AB-common from now on) and add to both A and B the equality x = t:
       in this case, if θ is the interpolant computed after such a transformation,
       then θ(t/x) is an interpolant for the original pair.
     We shall often apply the above metarules (i)-(ii)-(iii) in the sequel.

7.1   The Algorithm
We reduce the problem of finding an interpolant of an unsatifiable pair (A0 , B 0 )
to an analogous polynomial size problem in the weaker theory TI ∪ EUF .
    Our unsatisfiable pair (A0 , B 0 ) needs to be preprocessed. Using the procedure
in the proof of Lemma 7, we can suppose that both A0 and B 0 are given in the
form of finite separated pairs. In fact, the procedure of Lemma 7 just introduces
20      S. Ghilardi et al.

constants in order to explicitly name terms, so that it fits within the above
explained remarks (see metarules (ii)-(iii)). The newly introduced constants are
colored A-strict, B-strict or AB-common depending on the color of the terms
they name. Notice that because of this preprocessing, for every A-strict (resp.
B-strict, AB-common) array constant a, in A0 (resp. B0 , A0 ∩ B 0 ) there is an
atom of the kind |a| = la .
     To sum up, A0 is of the form A01 ∧ A02 and B 0 is of the form B10 ∧ B20 ,
                                    V        V                       V     V
for separated pairs (A01 , A02 ) and (B10 , B20 ).
     Our interpolation algorithm consists of three transformation steps (all of
them fit our metarules (i)-(ii)-(iii)). We let NA (resp. NB ) be the number of A-
local (resp. B-local) index constants occurring within a wr symbol in A0 (resp.
B 0 ); we let also N be equal to 1 + max(NA , NB ).
 Step 1. This transformation must be applied for every pair of distinct AB-
common ARRAY-constants c1 , c2 . The transformation picks fresh INDEX constants
k1 , . . . , kN (to be colored AB-common) and adds the atoms diffn (c1 , c2 ) = kn
(for all n = 1, . . . , N ) to both sets A1 and B1 . This transformation fits metarule
(iii).
 Step 2. We apply 0-instantiation, that is we replace A with A(IA ) and B with
B(IB ), where IA is the set of A-local index constants and B is the set of B-local
index constants (see Definition 6). This transformation fits metarule (i).
 Step 3. As proved in Theorem 7 below, at this step A2 ∧ B2 is TI ∪ EUF -
inconsistent; since TI ∪ EUF has quantifier-free interpolation by Theorem 2, we
can compute an interpolant θ of the jointly unsatisfiable pair A2 , B2 . To get our
desired CARD(TI )-interpolant, we only have to replace back in it the fresh AB-
common constants introduced by our trasformations by the AB-common terms
they name.
Example 2. We let

         A0 ≡ {diff(a1 , a2 ) = j, diff(a1 , c1 ) = j1 , diff(a2 , c2 ) = j2 }
                   B 0 ≡ {j < l, j1 < l, j2 < l, rd(c1 , l) 6= rd(c2 , l)}

In the preprocessing step, we must add the atoms |a1 | = la1 , |a2 | = la2 to A01
and |c1 | = lc1 , |c2 | = lc2 to both A01 and B10 . Since NA = NB = 0, we have
N = 1; Step 1 adds the AB-common atom diff(c1 , c2 ) = k1 . Step 2 makes
the required 0-instantiations producing the 0-instantiated separated pair (A, B).
From such instantiations, we can conclude that A1 entails k1 ≤ max(j1 , j2 , j);
this is TI ∪ EUF -inconsistent with B1 as B1 contains, in addition to j < l, j1 <
l, j2 < l, rd(c1 , l) 6= rd(c2 , l), also

                             k1 < l → rd(c1 , l) = rd(c2 , l)

by (21). Thus k1 ≤ max(j1 , j2 , j) is a TI ∪EUF -interpolant. Using the recover in-
struction of meta-rule (iii), we get diff(c1 , c2 ) ≤ max(j1 , j2 , j) as an CARD(TI )-
interpolant.
      General Interpolation and Strong Amalgamation for Contiguous Arrays                 21

Example 3. Let A0 be
                       {diff(a, c1 ) = i1 , diff(b, c2 ) = i1 , a1 = wr(b, i1 , e1 ), |a| = k,
a = wr(a1 , i3 , e3 ), |a1 | = k, |b1 | = k, |c1 | = k, |c2 | = k}
and let B 0 be {rd(c1 , i1 ) 6= rd(c2 , i2 ), i1 < i2 , i2 < i3 ,
i3 < k, |c1 | = k, |c2 | = k}.
    We do not need any preprocessing here; since N = 3, Step 1 adds the AB-
common atoms
           diff1 (c1 , c2 ) = k1 , diff2 (c1 , c2 ) = k2 , diff3 (c1 , c2 ) = k3 .
Step 2 produces a separated pair (A, B) such that A2 ∧ B2 is TI ∪ EUF -incon-
sistent (inconsistency can be tested via an SMT-solver like z3 [14] or Math-
Sat [6]). The related TI ∪ EUF -interpolant (once k1 , k2 and k3 are replaced by
diff1 (c1 , c2 ), diff2 (c1 , c2 ) and diff3 (c1 , c2 ), respectively) gives our CARD(TI )-
interpolant.
Example 4. This is the classical example (due to R. Jhala) showing that ARext
does not have quantifier-free interpolation (one needs diff in the signature to
recover it). Let A0 be {c1 = wr(c2 , i, e)} and B 0 be {i1 6= i2 , rd(c1 , i1 ) 6=
rd(c2 , i1 ), rd(c1 , i2 ) 6= rd(c2 , i2 )}. Preprocessing adds the AB-common literals
|c1 | = lc1 , |c2 | = lc2 to both A01 and B10 . Step 1 introduces the AB-common
atoms
                           diff1 (c1 , c2 ) = k1 , diff2 (c1 , c2 ) = k2 .
In the 0-instantiated separated pair (A, B) produced by Step 2, from (17)
and (21), we realize that
                    k2 = 0 ∧ (k1 = k2 ∨ rd(c1 , k2 ) = rd(c2 , k2 ))                    (26)
is TI ∪ EUF -implied by A1 and TI ∪ EUF -inconsistent with B1 . To get
an CARD(TI )-interpolant, it is enough to replace k1 , k2 respectively by
diff1 (c1 , c2 ), diff2 (c1 , c2 ) in (26).
Theorem 7. The above rule-based algorithm computes a quantifier-free inter-
polant for every CARD(TI )-mutually unsatifiable pair A0 , B 0 of quantifier-free
formulae.
Proof. We only need to prove that Step 3 really applies.
    Suppose not; let A = (A1 , A2 ) and B = (B1 , B2 ) be the separated pairs
obtained after applications of Steps 1 and 2. If Step 3 does not apply, then
A2 ∧ B2 is TI ∪ EUF -consistent. We claim that (A, B) is CARD(TI )-consistent
(contradicting that (A0 , B 0 ) ⊆ (A, B) was CARD(TI )-inconsistent).
    Let M be a TI ∪ EUF -model of A2 ∧ B2 . M is a two-sorted structure (the
sorts are INDEX and ELEM) endowed for every array constant d occurring in A∪B
of a function dM : INDEXM −→ ELEMM . In addition, INDEXM is a model of TI .
We list the properties of M that comes from the fact that our Steps 1-2 have
been applied; below, we denote by k M the element of INDEXM assigned to an
index constant k (thus, if, e.g., k, l are index constants, M |= k = l is the same
as k M = lM ):
22        S. Ghilardi et al.

                          V
(a) we have V that M |= A1 (IA ) (where IA is the set of A-local constants) and
    M |= B1 (IB ) (where IA is the set of B-local constants): this is because
    (A1 , A2 ) and (B1 , B2 ) are 0-instantiated by Step 2;
(b) for AB-common array variables c1 , c2 , we have that A1 ∩B1 contains a literal
    of the kind diffn (c1 , c2 ) = kn for n ≤ N ; suppose that M |= lc1 = lc2 8 and
    that k is an index constant such that M |= k 6= l for all AB-common index
    constant l; then, we can have M |= c1 (k) 6= c2 (k) only when M |= k < kN :
    this is because Step 1 has been applied and because of (a).
    We expand M to an ARext (TI )-structure N and endow it with an assign-
ment to our A-local and B-local variables, in such a way that all diff operators
mentioned in A1 , B1 are defined and all formulae in A, B are true. In view of The-
orem 3, this structure can be expanded to the desired full model of CARD(TI ).
We take INDEXN and ELEMN to be equal to INDEXM and ELEMM ; the TI -reduct
of N will be equal to the TI -reduct of M and we let xN = xM for all index and
element constants occurring in A ∪ B. ARRAYN is the set of all positive support
functions from INDEXN into ELEMN . The interpretation of A-local and B-local
constants of sort ARRAY is more subtle. We need a détour to introduce it.
    Let k be an index constant s.t. M |= k 6= l for all A-local index constant
l; we introduce an equivalence relation ≡k on the set of A-local array variables
as follows: ≡k is the smallest equivalence relation that contains all pairs (a1 , a2 )
such that M |= la1 = la2 and moreover an atom of one of the following two
kinds belongs to A01 : (I) a1 = wr(a2 , i, e); (II) diff(a1 , a2 ) = l, for an l such
that M |= l < k.
Claim: if c1 , c2 are AB-common and c1 ≡k c2 , then cM             M       M M
                                                              1 (k ) = c2 (k ). The
claim is proved by preventively showing, for every A-local constants a1 , a2 such
that a1 ≡k a2 , that the number of the A-local constants j such that M |= k < j
and aM        M        M M
        1 (j ) 6= a2 (j ) is less or equal to NA < N . In the proof (see the
appendix for details), properties (a) and (b) above and the fact that N :=
1 + max(NA , NB ) play a crucial role.
     In order to interpret A-local constants of sort ARRAY, we assign to an A-local
constant a of sort ARRAY the function aN defined as follows for every i ∈ INDEXN :
   (†-i) if i is equal to k M , where k is an A-local constant, then aN (i) := aM (k M );
  (†-ii) if i is different from k M for every A-local constant k, but i is equal to
         k M for some (necessarily B-strict) index constant k and there is an AB-
         common array variable c such that c ≡k a, then aN (i) is equal to cM (k M )
         (this is well-defined thanks to the claim);
 (†-iii) in the remaining cases, aN (i) is equal to elM or ⊥M depending whether
         M |= 0 ≤ i ∧ i ≤ la holds or not.
     It can be now shown that
(∗-A) all aN are positive-support functions and all formulæ from A1 ∪ A2 are
      true in N .
In fact, formulæ in A2 are Boolean combinations of A-local atoms of the
kind (25): these are TI ∪ EUF -atoms and, due to their shape, each of them
8
     Recall that lc1 , lc2 are the AB-common constants such that the literals |c1 | =
     lc1 , |c2 | = lc2 belongs to A1 ∩ B1 .
     General Interpolation and Strong Amalgamation for Contiguous Arrays         23

is true in M iff it is true in N . Moreover, formulæ in A1 are all wr, diff and
|−|-atoms. They are true in N because of the 0-instantiation performed by Step
2 (see (a) above). Full details are in the appendix.
    The assignments to the B-local array variables b are defined analogously, so
that
(∗-B) all bN are positive-support functions and all formulæ from B1 ∪ B2 are
     true in N .
    There is however one important point to notice. For all AB-common con-
stants c of sort ARRAY, our specification of cM does not depend on the fact that
we use the above definition for A-local or for B-local array constants: to see
this, notice that c ≡k c holds in case (†-ii) is applied. This remark concludes the
proof.

   It is not difficult to see that the quantifier-free TI ∪ EUF -interpolation prob-
lem generated by our algorithm is of polynomial size. Notice however that
TI ∪ EUF -interpolation is at least exponential.


8   Further Related Work and Conclusions

We introduced two theories of arrays, namely the theory CARD(TI ) of con-
tiguous arrays with maxdiff and its extension CARDC(TI ) that also supports
‘constant’ arrays’. These theories are strictly more expressive than McCarthy’s
theory and the other variants studied in the literature: notably, strong length
of arrays is definable, and inside it arrays are fully defined in every memory
location. We proved that CARDC(TI ) admits general interpolation by showing
that its models are strongly amalgamable; the existence of (plain) amalgams
also implies that CARD(TI ) has (plain) interpolants. We also studied the SMT
problem for CARD(TI ) and showed through instantiations techniques that it is
decidable. Finally, we provided a general algorithm for computing CARD(TI )
quantifier-free interpolants that relies on a polynomial reduction to the problem
of computing general interpolants for the index theory. Differently from previous
algorithms, this procedure avoids full instantiation of terms.
     One future research direction regards the implementation of this procedure,
which is still missing. In the last decade, some implemented approaches have been
introduced to compute interpolants for different theories, by relying on different
techniques. For the significant theory of EUF , in [15] the DPT prover, which
implements a method that exploits colored congruence graphs for extracting in-
terpolants, has been shown to produce simpler and smaller interpolants than
other solvers. For more complex theories, in [25] McMillan proposed an inter-
polating proof calculus to compute interpolants via refutational proofs obtained
from the z3 SMT-solver. It is worth mentioning his approach because it takes
advantages from the flexibility of the z3 solver to deal with several theories and
their combination: it makes use of a secondary interpolation engine in order to
‘fill the gaps’ of refutational proofs introduced by theory lemmas, which are spe-
cific formulæ derived by the satellites theories encoded in z3. This secondary
24      S. Ghilardi et al.

engine only needs an interpolation algorithm for QF_UFLIA. This approach can
be used to computes interpolants for array theories, but since they use quantified
formulæ, the method can generate quantified formulæ.
    Concerning in particular array theories, another notable approach for com-
puting interpolants is due to the authors of [18], which exploited the proof tree
preserving interpolation scheme from [12] to construct interpolants via a reso-
lution proof. This approach is capable of handling, following the nomenclature
of our paper, AB-common literals but not AB-common terms: for this reason,
weakly equivalences between arrays are there introduced in order to cope with
those cases. This method supports the use of the diff operation between arrays
in order to compute quantifier-free interpolants, but its semantic interpretation
is undetermined as in [7].
    In [9], the authors presented AXDInterpolator [1], an implementation of the
interpolation algorithm from [17], which allows the user to choose z3, Mathsat,
or SMTInterpol ([11]) as the underlying interpolation engines. In order to
show its feasibility, it was tested against a benchmark based on C programs
from the ReachSafety-Arrays and MemSafety-Arrays tracks of SV-COMP [4].
Since many C programs from [4] require the usage of array length (and, in
particular, strong length) we plan to develop a tool that implements the new
algorithm for contiguous arrays presented in this paper.
    There is still a question concerning our interpolation algorithm that needs to
be investigated: extending the algorithm to the theory CARDC(TI ) (with con-
stant arrays in the language). In order to handle constant arrays, the construction
of Theorem 7 is still appropriate, except for the fact that condition (†-ii) should
not be applied to define Const(i)N when i is an A-strict constant such that
iM is equal to j M for some AB-common j. To avoid this, one could introduce
right after Step 1 some form of guessing for equalities between index constants:
however, such a guessing (based on colorings) would create branches and conse-
quently would not produce a polynomial instance of a TI ∪ EUF -interpolation
problem in Step 3. This issue needs further analysis.
    Finally, although quite challenging, it would be interesting to extend our
interpolation results also to array theories combined with cardinality constraints,
similar to those introduced, e.g., in [2],[27].


References

 1. AXDInterpolator, 2021. Accessed: 2021-10-12.
 2. Francesco Alberti, Silvio Ghilardi, and Elena Pagani. Cardinality constraints for ar-
    rays (decidability results and applications). Formal Methods Syst. Des., 51(3):545–
    574, 2017.
 3. Paul D. Bacsich. Amalgamation properties and interpolation theorems for equa-
    tional theories. Algebra Universalis, 5:45–55, 1975.
 4. Dirk Beyer. Software Verification: 10th Comparative Evaluation (SV-COMP 2021).
    In Proc. of TACAS 2021, volume 12652 of LNCS, pages 401–422, Berlin, Heidel-
    berg, 2021. Springer.
     General Interpolation and Strong Amalgamation for Contiguous Arrays            25

 5. Aaron R. Bradley, Zohar Manna, and Henny B. Sipma. What’s decidable about
    arrays? In Proc. of VMCAI 2006, volume 3855 of LNCS, pages 427–442, Berlin,
    Heidelberg, 2006. Springer.
 6. Roberto Bruttomesso, Alessandro Cimatti, Anders Franzén, Alberto Griggio, and
    Roberto Sebastiani. The MathSAT 4 SMT solver. In Proc. of CAV 2008, volume
    5123 of LNCS, pages 299–303, Berlin, Heidelberg, 2008. Springer.
 7. Roberto Bruttomesso, Silvio Ghilardi, and Silvio Ranise. Quantifier-free interpo-
    lation of a theory of arrays. Log. Methods Comput. Sci., 8(2), 2012.
 8. Roberto Bruttomesso, Silvio Ghilardi, and Silvio Ranise. Quantifier-free interpo-
    lation in combinations of equality interpolating theories. ACM Trans. Comput.
    Log., 15(1):5:1–5:34, 2014.
 9. José Abel Castellanos Joo, Silvio Ghilardi, Alessandro Gianola, and Deepak Kapur.
    Axdinterpolator: A tool for computing interpolants for arrays with maxdiff. In
    Proc. of SMT 2021, volume 2908, pages 40–52. CEUR Workshop Proceedings,
    2021.
10. C. C. Chang and H. Jerome Keisler. Model Theory. North-Holland, Amsterdam-
    London, third edition, 1990.
11. Jürgen Christ, Jochen Hoenicke, and Alexander Nutz. SMTInterpol: An interpo-
    lating SMT solver. In Proc. of SPIN 2012, volume 7385 of LNCS, pages 248–254,
    Berlin, Heidelberg, 2012. Springer.
12. Jürgen Christ, Jochen Hoenicke, and Alexander Nutz. Proof tree preserving inter-
    polation. In Proc. of TACAS 2013, volume 7795 of LNCS, pages 124–138, Berlin,
    Heidelberg, 2013. Springer.
13. William Craig. Three uses of the Herbrand-Gentzen theorem in relating model
    theory and proof theory. J. Symbolic Logic, 22:269–285, 1957.
14. Leonardo De Moura and Nikolaj Bjørner. Z3: An Efficient SMT Solver. In Proc. of
    the TACAS 2008, volume 4963 of LNCS, pages 337–340, Berlin, Heidelberg, 2008.
    Springer.
15. Alexander Fuchs, Amit Goel, Jim Grundy, Sava Krstic, and Cesare Tinelli. Ground
    interpolation for the theory of equality. Log. Methods Comput. Sci., 8(1), 2012.
16. Silvio Ghilardi. Model theoretic methods in combined constraint satisfiability. J.
    Autom. Reasoning, 33(3-4):221–249, 2004.
17. Silvio Ghilardi, Alessandro Gianola, and Deepak Kapur. Interpolation and amal-
    gamation for arrays with maxdiff. In Proc. of FOSSACS 2021, volume 12650 of
    LNCS, pages 268–288, Berlin, Heidelberg, 2021. Springer.
18. Jochen Hoenicke and Tanja Schindler. Efficient interpolation for the theory of
    arrays. In Proc. of IJCAR 2018, volume 10900 of LNCS, pages 549–565, Berlin,
    Heidelberg, 2018. Springer.
19. Jochen Hoenicke and Tanja Schindler. Interpolation and the array property frag-
    ment. CoRR, abs/1904.11381, 2019.
20. Deepak Kapur, Rupak Majumdar, and Calogero G. Zarba. Interpolation for Data
    Structures. In Proc. of SIGSOFT/FSE 2006, pages 105–116. ACM, 2006.
21. Emil W. Kiss, László Márki, Péter Pröhle, and Walter Tholen. Categorical alge-
    braic properties. A compendium on amalgamation, congruence extension, epimor-
    phisms, residual smallness, and injectivity. Studia Sci. Math. Hungar., 18(1):79–
    140, 1982.
22. John McCarthy. Towards a Mathematical Science of Computation. In Proc. of
    IFIP Congress 1962, pages 21–28. North-Holland, 1962.
23. Kenneth L. McMillan. Interpolation and sat-based model checking. In Proc. of
    CAV 2003, volume 2725 of LNCS, pages 1–13, Berlin, Heidelberg, 2003. Springer.
26      S. Ghilardi et al.

24. Kenneth L. McMillan. Lazy abstraction with interpolants. In Proc. of CAV 2006,
    volume 4144 of LNCS, pages 123–136, Berlin, Heidelberg, 2006. Springer.
25. Kenneth L. McMillan. Interpolants from Z3 proofs. In Proc. of FMCAD 2011,
    pages 19–27. FMCAD Inc., 2011.
26. Greg Nelson and Derek C. Oppen. Simplification by Cooperating Decision Proce-
    dures. ACM Trans. Program. Lang. Syst., 1(2):245–257, 1979.
27. Rodrigo Raya and Viktor Kunkak. Np satisfiability for arrays as powers. In Proc.
    of VMCAI 2022, volume 13182 of LNCS, pages 301–318, Berlin, Heidelberg, 2022.
    Springer.
28. Andrey Rybalchenko and Viorica Sofronie-Stokkermans. Constraint solving for
    interpolation. In Proc. of VMCAI 2007, volume 4349 of LNCS, pages 346–362,
    Berlin, Heidelberg, 2007. Springer.
29. Andrey Rybalchenko and Viorica Sofronie-Stokkermans. Constraint solving for
    interpolation. J. Symb. Comput., 45(11):1212–1233, 2010.
30. Viorica Sofronie-Stokkermans. Interpolation in local theory extensions. In Proc.
    of IJCAR 2006, volume 4130 of LNCS, pages 235–250, Berlin, Heidelberg, 2006.
    Springer.
31. Viorica Sofronie-Stokkermans. Interpolation in local theory extensions. Log. Meth-
    ods Comput. Sci., 4(4), 2008.
32. Viorica Sofronie-Stokkermans. On interpolation and symbol elimination in theory
    extensions. In Proc. of IJCAR 2016, volume 9706 of LNCS, pages 273–289, Berlin,
    Heidelberg, 2016. Springer.
33. Viorica Sofronie-Stokkermans. On interpolation and symbol elimination in theory
    extensions. Log. Methods Comput. Sci., 14(3), 2018.
34. Nishant Totla and Thomas Wies. Complete instantiation-based interpolation. In
    Proc. of POPL 2013, pages 537–548. ACM, 2013.
35. Nishant Totla and Thomas Wies. Complete instantiation-based interpolation. J.
    Autom. Reasoning, 57(1):37–65, 2016.
      General Interpolation and Strong Amalgamation for Contiguous Arrays              27

A     Proofs of results from Section 4

Lemma 5 Let N , M be models of ARext (TI ) such that M is a substructure of
N . For every a, b ∈ ARRAYM , we have that

                             M |= a ∼ b iff N |= a ∼ b.



Proof. The left-to-right side is trivial because if M |= a ∼ b then a and b have
equal length in M and in N too because length is preserved; moreover, M |=
a = wr(b, I, E), where I ≡ i1 , . . . , in is a list of costants (naming elements of M)
of sort INDEX, E ≡ e1 , . . . , en is a list of costants (naming elements of M) of sort
ELEM, and wr(b, I, E) abbreviates the term wr(wr(· · · wr(b, i1 , e1 ) · · · ), in , en ).
Thus, also N |= a = wr(b, I, E) because M is a substructure of N . Vice versa,
suppose that M 6|= a ∼ b. This means that either |a| 6= |b| or that there are
infinitely many i ∈ INDEXM such that rdM (a, i) 6= rdM (b, i). Since M is a
substructure of N , these conditions holds in N too.

Lemma 9. Let M be a model of ARext (TI ) and let a, a′ , b, b′ ∈ ARRAYM ; if
a ∼M a′ , b ∼M b′ and diffk (a′ , b′ ) is defined for every k, then diff(a, b) is also
defined.

Proof. Notice first that, from a ∼ a′ and b ∼ b′ , it follows that |a| = |a′ | and
|b| = |b′ |. In case |a| 6= |b|, we have that diff(a, b) = max{|a|, |b|} (see Lemma 1),
which implies that diff(a, b) is defined. Hence, the relevant case is when we have
l = |a| = |b| = |a′ | = |b′ | and a′ 6∼ b′ (if a′ ∼ b′ , then we have also a ∼ b and
the maximum of the finitely many indexes where a, b differ is diff(a, b)). Then
for the infinitely many indexes jk = diffk (a′ , b′ ) we have a′ (jk ) 6= b′ (jk ); for at
least one of such jk we must also have a(jk ) 6= b(jk ) because a ∼ a′ and b ∼ b′ .
Consider now the indexes in [jk , l]: in this interval, the pair of arrays a, b differs
on at least one but at most finitely many indices (because a, a′ differs on finitely
many indices there and so do the pairs b, b′ and a′ , b′ ), so the biggest one such
index will be diff(a, b).

Lemma 10. Let M be a model of ARext (TI ). There exist a model N of
ARext (TI ) and a diff-faithful embedding µ : M → N such that the restric-
tion of µ to the sort ELEM is not surjective. In addition, if M is a model of
CARC ext (TI ), CARD(TI ) or of CARDC(TI ), so it is N .

Proof. To build N it is sufficient to put:

 – INDEXN = INDEXM ,
 – ELEMN = ELEMM ∪ {e} where e ∈   / ELEMM ,
 – ARRAY consists of the positive-support functions a : INDEXN −→ ELEMN
         N

   for which there exist a′ ∈ ARRAYM such that a ∼ a′ .
28      S. Ghilardi et al.

Now notice that if diff is totally defined in M, so it is in N . In fact, this follows
from the definition of ARRAYN and Lemma 9: if a ∼ a′ , b ∼ b′ and diffk (a′ , b′ )
is defined for every k, then diff(a, b) is also defined by the previous lemma.
The claim is proved in the same way for all the above mentioned array theories
(notice that in case the signature includes the Const symbol, µ trivially preserves
it).

Lemma 6 Let M be a model of ARext (TI ) (resp. of CARC ext (TI )) and let
a, b ∈ ARRAYM be such that diffM (a, b) is not defined. Then there are a model N
of ARext (TI ) (resp. of CARC ext (TI )) and a diff-faithful embedding µ : M → N
such that diffN (a, b) is defined.

Proof. Thanks to Lemma 10, we can assume that ELEMM has at least an ele-
ment e (different from ⊥M , elM ). Notice that we must have |a| = |b|, otherwise
diff(a, b) is defined and it is max(|a|, |b|) according to Lemma 1.
   Let I = {i ∈ INDEXM | a(i) 6= b(i)} be the set of indices without maximum
element (hence infinite) where they differ. Let ↓ I := {j ∈ INDEXM | ∃i ∈ I, j ≤
i} ⊇ I. Notice that the condition

                      (+) “∃i ∈ I ∀j ∈ I (j ≥ i → x(j) = el)”

cannot be satisfied both for x = a and x = b: indeed, if this were the case,
assuming w.l.o.g. that ia ≤ ib (where ia and ib are the witnesses for the existen-
tially quantified index i in (+) for x = a and x = b respectively), we would have
that a(j) = elM = b(j) for all j ≥ ib , j ∈ I, which is a contradiction with the
definition of I. In case one of them satisfies it, we assume it is b.
    Let ∆ be the Robinson diagram of the TI -reduct of M and let k0 be a new
constant; let us introduce the set

            ∆′ := ∆ ∪ {i < k0 | i ∈↓ I} ∪ {k0 < i | i ∈ INDEXM \ ↓ I}.

By the compactness theorem for first order logic and since I is infinite, the set
∆′ turns out to be consistent. In fact, if ∆′ were inconsistent, then there would
exist a finite subset of it not admitting a model. However, a finite subset of ∆′
can contain constraints only for a finite number of index constants d occurring
in ∆, i ∈↓ I, i′ ∈ INDEXM \ ↓ and k0 . Such constraints can be verified inside
the TI -reduct of M itself: to interpret the additional constant k0 , it is sufficient
to use the fact that I contains arbitrarily large indexes and the fact that the
definition of ↓ I implies that

                        ∀i ∈↓ I, ∀j ∈ INDEXM \ ↓ I,     i < j.

    By Robinson Diagram Lemma, there exists a model A of TI extending the
TI -reduct of M; such A contains in its support an element k0 such that

                                  ∀i ∈↓ I, i < k0 ,

                             ∀i ∈ INDEXM \ ↓ I, k0 < i.
      General Interpolation and Strong Amalgamation for Contiguous Arrays    29

    We now take ELEMN = ELEMM , INDEXN = INDEXA ; we let also ARRAYN to be
the set of all positive-support functions from INDEXN into ELEMN (notice that
this N is trivially also a model of CARC ext (TI )). We observe that k0 < |a|M
and recall that |a|M = |b|M .
    Let us now define the embedding µ : M → N ; at the level of the sorts INDEX
and ELEM, we use inclusions. For the ARRAY sort, we need to specify the value
µ(c)(k) for c ∈ ARRAYM and k ∈ INDEXN \ INDEXM (for the other indices we
keep the old M-value to preserve the read operation). Our definition for µ must
preserve the maxdiff index (whenever already defined in M) and must guarantee
that diffN (µ(a), µ(b)) = k0 (by construction, we have k0 > 0). For a generic
array c ∈ ARRAYM , we operate as follows:
 1. if |c|M < k0 we put µ(c)(k0 ) = ⊥M , otherwise:
 2. if the condition (⋆) below holds, we put µ(c)(k0 ) = e,
 3. if such condition does not hold, we put µ(c)(k0 ) = elM .
The condition (⋆) is specified as follows:
(⋆)   there is i ∈ I such that for all j ∈ I, j ≥ i we have c(j) = a(j).
For all the remaining indexes k ∈ INDEXN \ (INDEXM ∪ {k0 }) we put
                           (
                             ⊥M , if k ∈/ [0, |c|M ]
                 µ(c)(k) =                             (23)
                             elM , if k ∈ [0, |c|M ]

Notice that we have µ(a)(k0 ) = e 6= elM = µ(b)(k0 ) (the last equality holds
because I is infinite and does not have maximum, hence condition (⋆) holds for
a but not for b). In addition:
 – for all i ∈ INDEXM such that k0 < i, we have i ∈     / ↓ I, according to the
   construction of k0 and consequently i ∈
                                         / I, that is a(i) = b(i);
 – for all i ∈ INDEXN \ (INDEXM ∪ {k0 }) such that k0 < i, since we have
   |a|M = |b|M , we get
                          µ(a)(i) = ⊥M iff µ(b)(i) = ⊥M ,
                          µ(a)(i) = elM iff µ(b)(i) = elM .
Hence, we can conclude that diffN (µ(a), µ(b)) is defined and equal to k0 .
   We only need to check that our µ preserves rd, |−|, wr, constant arrays and
diff (whenever defined).
   The operation rd is preserved because µ acts as an inclusion for indexes and
elements and because we have µ(c)(k) = c(k) if k ∈ INDEXM .
   Concerning length, we have |µ(c)|N = |c|M because of (23) and because of
the above definition of µ(c)(k0 ) (recall that k0 > 0).
     Concerning write operation, we prove that for all c ∈ ARRAYM , i ∈ INDEXM ∩
[0, |c|] and e′ ∈ ELEMM \ {⊥M } we have
                         µ(wr(c, i, e′ )) = wr(µ(c), i, e′ ).
Remember that we have |wr(c, i, e′ )| = |c| = |µ(c)|.
30      S. Ghilardi et al.

 – For k 6= i in INDEXM

                        µ(wr(c, i, e′ ))(k) = wr(c, i, e′ )(k) = c(k)

                              wr(µ(c), i, e′ )(k) = µ(c)(k) = c(k);
 – For k = i
                             µ(wr(c, i, e′ ))(i) = wr(c, i, e′ )(i) = e′
                                     wr(µ(c), i, e′ )(i) = e′ ;
 – For k = k0 > |c| the claim follows immediately from the definition;
 – For k = k0 < |c|, (⋆) holds for c iff it holds for wr(c, i, e′ ), because I is
   infinite. Hence we have
                        µ(wr(c, i, e′ ))(k0 ) = e iff µ(c)(k0 ) = e.
 – For k ∈ INDEXN \ (INDEXM ∪ {k0 }), the claim is clear from the definition
   and from the fact that wr preserves length.

   For constant arrays, we must show only that µ(Const(i))(k0 ) = elM in case
k0 < i: this is clear, because a does not satisfy (+), hence (⋆) does not hold for
Const(i).
   Let us now finally consider the diff operation and let us prove that if
diffM (c1 , c2 ) is defined, then diffN (µ(c1 ), µ(c2 )) is also defined and equal to it.
Assume that diffM (c1 , c2 ) is defined; since µ preserve length, the only relevant
case, in view of Lemma 1, is when we have |c1 | = |c2 |; since the values of c1 , c2
on indexes from M are preserved, taking in mind (23) (in particular, that for
k ∈ INDEXN \ (INDEXM ∪ {k0 }) we have µ(c1 )(k) = µ(c2 )(k)), we only have to
exclude that we have

                  diffM (c1 , c2 ) < k0 and µ(c1 )(k0 ) 6= µ(c2 )(k0 )

If this is the case, we have, e.g., µ(c1 )(k0 ) = e 6= elM = µ(c2 )(k0 ) (k0 < |c1 | =
|c2 |), which implies that (⋆) holds for c1 but not for c2 . However, it cannot be
that (⋆) holds for only one among c1 , c2 . The reason for this is as follows. Indeed,
if i ∈ I is the index that witnesses (⋆) for c1 , then c1 (j) = a(j) for all indexes
j ∈ I such that j ≥ i (which are infinitely many). Since I is infinite and without
maximum and since diffM (c1 , c2 ) < k0 , we must have diffM (c1 , c2 ) ∈ ↓ I by
the definition of ∆, so there must be infinitely many indices in I bigger than
diffM (c1 , c2 ) and arbitrarily large, which means in particular that there exists
an index i′ ∈ I such that i′ ≥ i and i′ > diff(c1 , c2 ). This i′ witnesses (⋆) for
c2 , as wanted. This concludes the proof.                                            ⊣


B    Proofs of results from Section 5
We prove here that the model M introduced in Section 5 is a CARDC(TI )-
amalgam (and also a CARD(TI )-amalgam) for the models M1 and M2 with
the common substructure A.
     General Interpolation and Strong Amalgamation for Contiguous Arrays           31

Requirements check for the amalgamated model
Proof. We need to prove that the functions µi : (i) are well-defined, (ii) are in-
jective, (iii) preserve |−|, (iv) preserve rd and wr, (v) preserve diff, (vi) satisfy
the condition µ1 ◦ f1 = µ2 ◦ f2 , (vii) preserve constant arrays (for the statement
about CARDC(TI )).
(i) Since INDEXM is a strong amalgam of INDEXM1 and INDEXM2 , the case dis-
    tinctions we made for defining µi (a)(k) are non-overlapping and exhaustive.
    We now show that if, for i = 1, 2 and k ∈ INDEXM3−i \ INDEXA and
    a ∈ ARRAYMi , the relation (2⋆) holds relatively to two different pairs of
    arrays (c1 , b1 ), (c2 , b2 ) from ARRAYA × ARRAYMi , then we nevertheless have
    f3−i (c1 )(k) = f3−i (c2 )(k) (this proves the consistency of the definition). For
    symmetry, let us consider only the case i = 1. Since the index ordering is
    total, let us suppose that we have for instance
                    k > diffM1 (b1 , f1 (c1 )) ≥ diffM1 (b2 , f1 (c2 )).         (27)
    By the transitivity of ∼M1 , b1 and b2 differ on finitely many indices, hence
    we can consider the finite sets
             J := {j ∈ INDEXA | b1 (j) 6= b2 (j), j > diffM1 (b1 , f1 (c1 ))}
                            E := {b1 (j) | j ∈ J} ⊆ ELEMA .
    Let now pick c := wr(c2 , J, E); then c ∼A c2 . Since f2 is an embedding, we
    have f2 (c)(k) = f2 (c2 )(k) for all k ∈ INDEXM2 \ INDEXA . Suppose we have
    also
                          diffA (c1 , c) ≤ diffM1 (f1 (c1 ), b1 ).          (28)
    Then
                        diffA (c1 , c) ≤ diffM1 (f1 (c1 ), b1 ) < k
    and consequently also the desired equality
                           f2 (c1 )(k) = f2 (c)(k) = f2 (c2 )(k)
    follows.
    In order to prove (28), we consider j ∈ INDEXA with j > diffM1 (f1 (c1 ), b1 )
    and show that we have c(j) = c1 (j). Suppose not, i.e. that c(j) 6= c1 (j);
    then we cannot have j ∈ J otherwise, by definition of c and E, we would
    have c(j) = b1 (j) = f1 (c1 )(j) = c1 (j) (f1 is inclusion for indexes and J ⊆
    INDEXA ), contradiction. Hence, we have j ∈   / J, so c(j) = c2 (j) and b1 (j) =
    b2 (j). Now remember that
                    j > diffM1 (b1 , f1 (c1 )) ≥ diffM1 (b2 , f1 (c2 )),
    hence
                              c1 (j) = b1 (j), c2 (j) = b2 (j)
                         c(j) = c2 (j) = b2 (j) = b1 (j) = c1 (j)
    thus getting an absurdity.
 32        S. Ghilardi et al.

 (ii) Injectivity of µ1 and µ2 is immediate.
(iii) In order to prove that |−| is preserved, it is sufficient to show that for every
      a ∈ ARRAYM1 and for all k ∈ INDEXM , we have

                                  µ1 (a)(k) 6= ⊥ ↔ 0 ≤ k ≤ |a|M1 .

     The only relevant case is when k ∈ INDEXM2 \ INDEXA and (2⋆) holds. In
     such a case, we have two possibilities:
     |b|M1 = |c|A : in this case, since b ∼M1 a, we have |a|M1 = |b|M1 = |c|A =
           |f2 (c)|M2 (f2 is an embedding), thus getting what we need for k;
         M1
     |b|     6= |c|A : in this case k > diffM1 (b, f1 (c)) = max{|b|M1 , |c|A } by
           Lemma 1. Since a ∼ b implies |a| = |b|, the definition of µ1 produces
           µ1 (a)(k) = f2 (c)(k) = ⊥ (the last identity holds because k > |c|A ),
           which is as desired because k > |b|M1 = |a|M1 too.
(iv) The fact that rd and wr operations are preserved is easy (notice in particular
     that, if (2⋆) holds for a via the pair (c, b), then the same pair guarantees (2⋆)
     for arrays of the kind wr(a, i, e)).
 (v) Again we limit to the case of µ1 for symmetry. We need to show that for every
     a1 , a2 ∈ ARRAYM1 , we have µ1 (diffM1 (a1 , a2 )) = diffM (µ1 (a1 ), µ1 (a2 )).
     Notice that, if we call j the index diff(a1 , a2 ) ∈ INDEXM1 , by definition
     of µ1 on array applied to indexes in INDEXM1 , we have that µ1 (a1 )(j) =
     a1 (j) 6= a2 (j) = µ1 (a2 )(j). Hence, in order to conclude, it is sufficient to
     show that, given k ∈ INDEXM such that k > diffM1 (a1 , a2 ), the equality
     µ1 (a1 )(k) = µ1 (a2 )(k) holds. Notice first that we can always reduce to one
     of the following three cases
     (a) |a1 | < |a2 | = diffM1 (a1 , a2 );
     (b) diffM1 (a1 , a2 ) < |a1 | = |a2 |;
     (c) |a1 | = |a2 | = diffM1 (a1 , a2 ).
     We now show that µ1 (a1 )(k) = µ1 (a2 )(k).
       – If k ∈ INDEXM1 :

                                µ1 (a1 )(k) = a1 (k) = a2 (k) = µ1 (a2 )(k).

             / INDEXM1 ∪ INDEXM2 , we analyze the three cases separately:
      – If k ∈
    Case(a) : then k ∈
                     / [0, |ai |] for i = 1, 2. We have µ1 (a1 )(k) = ⊥ = µ1 (a2 )(k);
   Case (b) : we have
                                  µ1 (a1 )(k) = ⊥ ⇔ µ1 (a2 )(k) = ⊥

                                     µ1 (a1 )(k) = el ⇔ µ1 (a2 )(k) = el;
      Case (c) : similarly to (a), we have k ∈ / [0, |ai |] for i = 1, 2.
        – If k ∈ INDEXM2 \ INDEXA and (2⋆) does not hold neither for a1 nor for
           a2 , the argument is the same as in the previous case.
           Otherwise, suppose that (2⋆) holds for, say, a1 as witnessed by the pair
           (c1 , b1 ). Then we get µ1 (a1 )(k) = f2 (c1 )(k). We prove that (2⋆) holds
           for a2 too and that we have µ1 (a1 )(k) = f2 (c1 )(k) = µ1 (a2 )(k).
      General Interpolation and Strong Amalgamation for Contiguous Arrays           33

         Since b1 and a1 differ on finitely many indices inside M1 , we can consider
         the finite sets

                 I := {i ∈ INDEXM1 | b1 (i) 6= a1 (i), i > diffM1 (a1 , a2 )},

                               E := {b1 (i) | i ∈ I} ⊆ ELEMM1
         and the array b̂ := wr(a2 , I, E); for this array, we obviously have a2 ∼M1
         b̂. If we also have

                              diffM1 (b1 , b̂) ≤ diffM1 (a1 , a2 )                (29)

         then we get: k > diffM1 (a1 , a2 ) e k > diffM1 (b1 , f1 (c1 )) (the latter is
         from (2⋆)). Hence:

                      k > max{diffM1 (a1 , a2 ), diffM1 (b1 , f1 (c1 ))} ≥

                       ≥ max{diffM1 (b1 , b̂), diffM1 (b1 , f1 (c1 ))} ≥

                                       ≥ diff(b̂, f1 (c1 ))
         (the last disequality holds because of the ‘triangular disequality’ (15) of
         Lemma 1). Hence we obtain (2⋆) for a2 via the pair given by c := c1
         and b := b̂ (because we have a2 ∼M1 b̂ and k > diff(b̂, f1 (c1 ))) and
         consequently µ1 (a2 )(k) = f2 (c1 )(k).
         It remains to prove (29); to this aim, let us pick j ∈ INDEXM1 such that
         j > diff(a1 , a2 ) and let us show that b1 (j) = b̂(j). If this is not the
         case, i.e., if b1 (j) 6= b̂(j), then according to the definition of b̂ we have
         b̂(j) = a2 (j) and j ∈   / I. Hence b̂(j) = a2 (j) = a1 (j) = b1 (j) (the last
         identity holds because j ∈     / I and j > diff(a1 , a2 )), absurd.
(vi) In order to prove µ1 ◦ f1 = µ2 ◦ f2 , let us consider c ∈ ARRAYA ; let us put
     ai = fi (c) for i = 1, 2 and let us check that

                                  µ1 (a1 )(k) = µ2 (a2 )(k)

     holds for all k ∈ INDEXM .
      – Case k ∈ INDEXA : we have

                            µ1 (a1 )(k) = a1 (k) = f1 (c)(k) = c(k)

                            µ2 (a2 )(k) = a2 (k) = f2 (c)(k) = c(k).
      – Case k ∈ INDEXM1 \ INDEXA : clearly (2⋆) holds for a2 with c := c and
        b := a2 , consequently

                                µ1 (a1 )(k) = a1 (k) = f1 (c)(k)

                                    µ2 (a2 )(k) = f1 (c)(k).
 34      S. Ghilardi et al.

       – Case k ∈ INDEXM2 \ INDEXA : clearly (2⋆) holds for a1 with c := c and
         b := a1 , consequently

                                    µ1 (a1 )(k) = f2 (c)(k)

                               µ2 (a2 )(k) = a2 (k) = f2 (c)(k).
                / (INDEXM1 ∪ INDEXM2 ) and k ∈ [0, |c|]: we have
       – Case k ∈

                                µ1 (a1 )(k) = el = µ2 (a2 )(k).

              / (INDEXM1 ∪ INDEXM2 ) and k ∈
       – se k ∈                            / [0, |c|]: we have

                                µ1 (a1 )(k) = ⊥ = µ2 (a2 )(k).

      This completes our case analysis.
(vii) Here we assume that M1 , M2 are models of CARDC(TI ); we need to show,
      e.g., that µ1 (ConstM1 (i))(k) = el for every k such that 0 ≤ k ≤ i. Now,
      if i ∈ INDEXA this is obvious, because ConstM1 (i) = f1 (ConstA (i)). Hence
      suppose that i ∈ INDEXM1 \ INDEXA ; the only possibly problematic case is
      when k ∈ INDEXM2 \INDEXA and (2⋆) applies, as witnessed by a pair (b, c) for
      ConstM1 (i). But we have |b| = |ConstM1 (i)| = i and |f1 (c)| 6= i (because
      |f1 (c)| = |c| ∈ INDEXA ). Then, according to (2⋆) and recalling Lemma 1,
      we have k > diffMi (b, fi (c)) = max{|b|, |f1 (c)|} = max{i, |f1 (c)|} ≥ i,
      contradicting the choice of k.

      To prove strong amalgamation for CARDC(TI ) we need a couple of lemmas.
 Lemma 11. Every model M of CARDC(TI ) can be embedded into a model N
 such that INDEXN is infinite.
 Proof. This is basically due to the fact that TI is stably infinite. So let us first
 embed the TI -reduct of M into an infinite model A of TI . We define N as follows.
 We let ELEMN be equal to ELEMM and the TI -reduct of INDEXN be equal to A.
 We let ARRAYN be the set of positive support functions from INDEXN to ELEMN
 (the model so built will then be embedded into a full model of CARDC(TI )
 using Theorem 3). We only need to define the embedding µ : M −→ N . This
 emebdding will be the identity for INDEX and ELEM sorts; for arrays, we let
 µ(a)(k) be equal to a(k) for k ∈ INDEXM and for k 6∈ INDEXM , we put µ(a)(k)
 equal to elM or ⊥M depending whether we have k ∈ [0, |a|] or not. The proof
 that µ preserves all operations is easy.
    Let us call an element i ∈ INDEXM of a model M of CARDC(TI ) finite iff
 the set {j ∈ INDEXM | 0 ≤ j ≤ i} is finite. F in(M) denotes the set of finite
 elements of M.
 Lemma 12. Let A, M be models of CARDC(TI ) and let f : A −→ M be an
 embedding. Then there exist a third model N of CARDC(TI ) and an embedding
 ν : M → N , such that for every a ∈ ARRAYN with |a|N ∈ ν(f (INDEXA )) one of
 the following conditions hold:
       General Interpolation and Strong Amalgamation for Contiguous Arrays       35

1. there exists c ∈ ARRAYA such that ν(f (c)) ∼N a;
2. there exists ka ∈ INDEXN \ ν(INDEXM ) with a(ka ) 6∈ ν(f (ELEMA )) such that
   for every c ∈ ARRAYA we have a(ka ) 6= ν(f (c))(ka ).

Proof. Because of Lemma 11, we can freely assume that INDEXM is infinite. If
for all a ∈ ARRAYM whose length comes from A, there is c ∈ ARRAYA such that
f (c) ∼M a then it is sufficient to take N = M and the identity as ν. Otherwise,
one take a well ordering of the arrays, apply the construction below by tranfinite
induction and repeat it ω-times. The union of the chain so built will have the
required properties.
    Let a ∈ ARRAYM be such that |a| is from A (i.e. such that |a| = f (i) for some
i ∈ INDEXA ) and such that there does not exist c ∈ ARRAYA such that f (c) ∼M a.
Then |a| is not finite, because otherwise we would have that a ∼M f (Const(i)).9
Consider the diagram ∆ of the TI -reduct of M and let ka a fresh constant; the
set
                         ∆′ := ∆ ∪ {i < ka | i ∈ F in(M)}∪
                                                                               (30)
                         ∪{i > ka | i ∈ INDEXM \ F in(M)}.
is consistent. Suppose that ∆′ is inconsistent. By compactness, we would have
that there exists a finite subset ∆′0 of ∆′ which is inconsistent too. ∆′0 would
involve finitely many finite indexes i1 < · · · < in and finitely many infinite
indexes j1 < · · · < jm and a finite subset ∆0 of ∆.
    If m = 0, since INDEXM is infinite, there exist an element i′ ∈ INDEXM
large enough, so as to get i1 < · · · < in < i′ in M. If m > 0, then already in
INDEXM there exists an element i′ such that i1 < · · · < in < i′ and such that
i′ < j1 < · · · < jm hold in M, otherwise j1 would be a finite index. This element
i′ can interpret the constant ka . In both cases, we conclude that ∆′0 would be
consistent, which is a contradiction.
By Robinson Diagram Lemma, ∆ has a model B extending the TI -reduct of M.
    We let now ELEMN = ELEMM , INDEXN = INDEXB and we let ARRAYN to be
the set of positive-support functions from INDEXN into ELEMN (then, in view of
Theorem 3, N can be embedded into a full model of CARDC(TI )). This model
contains an element ka such that for all i ∈ INDEXM we have that ka 6= i and
i < ka iff i ∈ F in(M). In particular, ka < |a| (because |a| is infinite).
    Thanks to Lemma 10, we can freely suppose that ELEMN = ELEMM has an
element e not belonging to f (ELEMA ) (in particular e 6= f (elA ) = elN = elM ).
We build µ as required by the statement of the lemma (more precisely, the ν
required by the lemma will be a chain unions of the µ’s built at each transfinite
step as shown below). The INDEX- and ELEM-components of µ will be inclusions.
We define µ(b)(k) for all b ∈ ARRAYM . If k ∈ INDEXM , we obviously put µ(b)(k) =
b(k); in the other cases, the definition is as follows:
 1. if b 6∼M a, then µ(b)(k) = elN or µ(b)(k) = ⊥N , depending on whether
    k ∈ [0, |b|] or not;
9
    Notice that this is the only argument in the whole strong amalgamation proof re-
    quiring the fact that we have Const in the language.
36      S. Ghilardi et al.

 2. if b ∼M a and k 6= ka , then again µ(b)(k) = elN or µ(b)(k) = ⊥M , depending
    on whether k ∈ [0, |b|] or not;
 3. if b ∼M a and k = ka , then µ(b)(k) = e.
    We need to show that µ preserves rd, wr, |−|, constant arrays and diff.
Preservation of rd, wr, |−| are easy; constant arrays are preserved, because we
cannot have ConstM (i) ∼M a, otherwise |a| = i, which cannot be because |a| is
an element from INDEXA by hypothesis, so that we would have f (ConstA (i)) =
ConstM (i) ∼M a, contradiction. For preservation of diff, the problematic case
would be the case in which we have ka > diff(b1 , b2 ), b1 ∼M a and b2 6∼M a.
However, this is impossible because diff(b1 , b2 ) ∈ INDEXM and the fact that
we have ka > diff(b1 , b2 ) implies that diff(b1 , b2 ) is finite, which would entail
either b1 ∼M b2 or |b1 | 6= |b2 |: in the former case, we would have b2 ∼M a and
in the latter ka > diff(b1 , b2 ) = max(|b1 |, |b2 |) = max(|a|, |b2 |) ≥ |a|.
    We finally notice that ka satisfies the requirements of the lemma. First,
ka 6∈ µ(INDEXM ) and µ(a)(ka ) = e 6∈ µ(f (ELEMA )) hold by construction. More-
over, since for every c ∈ ARRAYA we have µ(f (c))(ka ) = elN or µ(f (c))(ka ) =
⊥N (depending whether ka ∈ [0, |c|] holds or not), in any case we see that
µ(f (c))(ka ) 6= µ(a)(ka ).

Theorem 5 CARDC(TI ) enjoys the strong amalgamation property.

Proof. We keep the same notation and construction as in the proof of Theorem 4.
However, thanks to Lemma 12 we can now suppose (for i = 1, 2) that all arrays
a ∈ ARRAYMi whose length belongs to INDEXA are such that one of the following
two conditions are satisfied:
 1. there exists c ∈ ARRAYA with fi (c) ∼Mi a;
 2. there exists ka ∈ INDEXMi \ INDEXA such that a(ka ) is an element from
    ELEMMi \ ELEMA different from all the fi (c)(ka ), varying c ∈ ARRAYA .
     Let ai ∈ ARRAYMi (i = 1, 2) be such that ∀k ∈ INDEXM we have

                             µ1 (a1 )(k) = µ2 (a2 )(k)   (24)

Notice that, since TI has the strong amalgamation property and the µi preserve
length, this can only happen if |a1 | = |a2 | belongs to INDEXA . We look for some
c ∈ ARRAYA such that a1 = f1 (c); since µ2 is injective this would entail a2 = f2 (c)
because
                    µ2 (a2 ) = µ1 (a1 ) = µ1 (f1 (c)) = µ2 (f2 (c)),
implying that M̂ is a strong amalgam, as requested.
    We separate two cases: (i) one of the arrays a1 , a2 satisfy the above condition
2; (ii) both arrays a1 , a2 satisfy the above condition 1.

(i) We show that this case is impossible. Suppose, e.g., that a1 satisfies condition
    2 in M1 . Then there exists an index ka1 in INDEXM1 \INDEXA such that a(ka1 )
    is an element from ELEMM1 \ ELEMA which is different from all the f1 (c)(ka1 ),
        General Interpolation and Strong Amalgamation for Contiguous Arrays                37

      varying c ∈ ARRAYA . Since we must have µ1 (a1 )(ka1 ) = µ2 (a2 )(ka1 ) and
      µ1 (a1 )(ka1 ) does not belong to ELEMM2 (recall that ELEMM1 ∩ ELEMM2 =
      ELEMA ), the value of a2 for the index ka1 (0 < ka1 < |a1 | = |a2 |) is built
      according to the rule (2⋆), because otherwise µ2 (a2 )(ka1 ) would be equal to
      some element in ELEMM2 . Let (c, b) the pair such that

              c ∈ ARRAYA , b ∈ ARRAYM2 , b ∼M2 a2 , ka1 > diffM2 (b, f2 (c))

                                   µ2 (a2 )(ka1 ) = f1 (c)(ka1 ).
      Then we have

                     µ1 (a1 )(ka1 ) = a1 (ka1 ) 6= f1 (c)(ka1 ) = µ2 (a2 )(ka1 )

     contradiction.
(ii) Hence we can have µ1 (a1 ) = µ2 (a2 ) only when both a1 , a2 satisfy condition 1
     above. Let us call ci ∈ ARRAYA (i = 1, 2) the arrays such that fi (ci ) ∼Mi ai .
     Then, the pair (c1 , f1 (c1 )) witnesses (2⋆) for a1 and for every positive 10
     index k ∈ INDEXM1 \ INDEXA (and similarly for a2 ). We look for c ∈ ARRAYA
     such that f1 (c) = a1 . Let us consider the following relations coming from
     (24) and from the definition of µi :

                                          ∀k ∈ INDEXA , a1 (k) = a2 (k)
                         ∀k ∈ INDEXM1 \ INDEXA , a1 (k) = f1 (c2 )(k)                 (31)
                        ∀k ∈ INDEXM2 \ INDEXA , f2 (c1 )(k) = a2 (k).

      where we used that µ2 (a2 )(k) = f1 (c2 )(k) if k ∈ INDEXM1 \ INDEXA , and
      µ1 (a1 )(k) = f2 (c1 )(k) if k ∈ INDEXM2 \ INDEXA .
      Let us now consider the sets (they are finite because f2 (c2 ) ∼M2 a2 )

                       J = {j ∈ INDEXA | c2 (j) 6= a2 (j)} ⊆ INDEXA

                                E = {a2 (j) | j ∈ J} ⊆ ELEMA ,
      and let us put c = wr(c2 , J, E); we check that c is such that f1 (c) = a1 .
       – If k ∈ INDEXA :

                       f1 (c)(k) = c(k) = wr(c2 , J, E)(k) = a2 (k) = a1 (k)

          because f1 preserves rd, by the definition of J and because of the equal-
          ities (31);
        – If k ∈ INDEXM1 \ INDEXA :

           f1 (c)(k) = f1 (wr(c2 , J, E))(k) = wr(f1 (c2 ), J, E)(k) = f1 (c2 )(k) = a1 (k)

           by the definition of c, the fact that f1 is an embedding, because J ⊆
           INDEXA (hence k ∈ / J) and because of the equalities (31).
10
     Notice that if k ∈ INDEXM1 \ INDEXA is positive, then k > diff(f1 (c), f1 (c)) = 0.
38        S. Ghilardi et al.

C       Proofs from Section 6

Lemma 7 Let φ be a quantifier-free formula; then it is possible to compute in
linear time a finite separation pair Φ = (Φ1 , Φ2 ) such that φ is CARD(TI )-
satisfiable iff so is Φ.

Proof. We first flatten all atoms from φ by repeatedly abstracting out subterms
(to abstract out a subterm t, we introduce a fresh variable x and update φ to
x = t ∧ φ(x/t)); then we remove all atoms of the kind a = b occurring in φ by
replacing them by the equivalent formula (16), namely

                          diff(a, b) = 0 ∧ rd(a, 0) = rd(b, 0) .

Then we abstract out all terms of the kind wr(b, i, e), diff(a, b) and |a|, so that
φ has now the form Φ1 ∧ Φ2 , where Φ2 does not contain wr, diff, |−|-symbols
and Φ1 is a conjunction of atoms of the form a = wr(b, i, e), i = diff(a, b), j =
|a|. Finally, we add to Φ1 the missing atoms of the kind |a| = i required by
Definition 5.11

Lemma 8 The following conditions are equivalent for a finite 0-instantiated
separation pair Φ = (Φ1 , Φ2 ):
(i) ΦV is CARD(TI )-satisfiable;
(ii)   Φ2 is TI ∪ EUF -satisfiable.

Proof. (i) ⇒ (ii) is clear.                                                   V
To prove (ii) ⇒ (i), let A be the model witnessing the satisfiability of Φ2 in
TI ∪EUF and let I be the set of all index variables occurring in Φ1 ∪Φ2 . According
to the definition of a separated pair, for every array variable a occurring in Φ1 ∪Φ2
there is an index variable la such that:

                               A |= fa (i) 6= ⊥ ↔ 0 ≤ i ≤ la .

for all i ∈ I (here fa is the unary function symbol replacing a in TI ∪ EUF ).
    The standardization A′ of A is the TI ∪ EUF -model obtained from A by
modifying the values a(k) (for all array variables a occurring in Φ2 and for all
indexes k ∈ INDEXA different from the elements assigned in A to the variables
in I) in such a way that we have

                          A′ |= fa (k) = ⊥ ↔ (la < k ∨ k < 0),

                         A′ |= fa (k) = el ↔ 0 ≤ k ≤ la .
The standardization A′ of A is still a model of Φ2 . However, in A′ now also
                                                  V
the formulae (18), (21) and (17) hold: this is because the I-instantiations of the
11
     The transformation of Lemma 7 does not introduce in Φ1 any formula of the kind
     diffn (a, b) = kn (for n > 1). These formulæ will however be introduced by the Step
     1 of the interpolation algorithm of Section 7.
     General Interpolation and Strong Amalgamation for Contiguous Arrays         39

universal index quantifiers occurring in such formulae were taken care in A and
their truth value is not modified passing to A′ , whereas the construction of A′
takes care of the instantiations outside I.
Let us now define an CARD(TI )-model M satisfying Φ. We first build a structure
                                                                             ′
N where diff may not be totally defined. We let INDEXN = INDEXA and
                 ′
ELEMN = ELEMA ; we take as ARRAYN the set of all positive-support functions
            N            N
from
  Vl INDEX into ELEM : this includes all functions of the form fa . In addition,
if n=1 diffn (a1 , a2 ) = kn ∈ Φ1 , then the related iterated maxdiff’s are defined
                           Vl
in N and we have N |= n=1 diffn (a1 , a2 ) = kn by the above construction.
Thus Φ holds in N and in order to obtain our final M we only need to apply
Theorem 3.


D    Proofs from Section 7

Theorem 7 The above rule-based algorithm computes a quantifier-free inter-
polant for every CARD(TI )-mutually unsatifiable pair A0 , B 0 of quantifier-free
formulae.

Proof. We only need to prove that Step 3 really applies.
    Suppose not; let A = (A1 , A2 ) and B = (B1 , B2 ) be the separated pairs
obtained after applications of Steps 1 and 2. If Step 3 does not apply, then
A2 ∧ B2 is TI ∪ EUF -consistent. We claim that (A, B) is CARD(TI )-consistent
(contradicting that (A0 , B 0 ) ⊆ (A, B) was CARD(TI )-inconsistent).
    Let M be a TI ∪ EUF -model of A2 ∧ B2 . M is a two-sorted structure (the
sorts are INDEX and ELEM) endowed for every array constant d occurring in A∪B
of a function dM : INDEXM −→ ELEMM . In addition, INDEXM is a model of TI .
We list the properties of M that comes from the fact that our Steps 1-2 have
been applied (below, we denote by k M the element of INDEXM assigned to an
index constant k):12
                          V
(a) we have V that M |= A1 (IA ) (where IA is the set of A-local constants) and
    M |= B1 (IB ) (where IA is the set of B-local constants): this is because
    (A1 , A2 ) and (B1 , B2 ) are 0-instantiated by Step 2;13
(b) for AB-common array variables c1 , c2 , we have that A1 ∩B1 contains a literal
    of the kind diffn (c1 , c2 ) = kn for n ≤ N ; suppose that M |= lc1 = lc2 14 and
    that k is an index constant such that M |= k 6= l for all AB-common index
    constant l; then, we can have M |= c1 (k) 6= c2 (k) only when M |= k < kN :
    this is because Step 1 has been applied and because of (a).

  We expand M to an ARext (TI )-structure N and endow it with an assign-
ment to our A-local and B-local variables, in such a way that all diff operators
12
   Thus if e.g. k, l are index constants, M |= k = l is the same as kM = lM .
13
   The sets A1 (IA ), B1 (IB ) are introduced in Definition 6.
14
   Recall that lc1 , lc2 are the AB-common constants such that the literals |c1 | =
   lc1 , |c2 | = lc2 belongs to A1 ∩ B1 .
40         S. Ghilardi et al.

mentioned in A1 , B1 are defined and all formulae in A, B are true. In view of The-
orem 3, this structure can be expanded to the desired full model of CARD(TI ).
We take INDEXN and ELEMN to be equal to INDEXM and ELEMM ; the TI -reduct
of N will be equal to the TI -reduct of M and we let xN = xM for all index and
element constants occurring in A ∪ B. ARRAYN is the set of all positive support
functions from INDEXN into ELEMN . The interpretation of A-local and B-local
constants of sort ARRAY is more subtle. We need a détour to explain it.
     Let k be an index constant such that M |= k 6= l for all A-local index
constant l; we introduce an equivalence relation ≡k on the set of A-local array
variables as follows: ≡k is the smallest equivalence relation that contains all pairs
(a1 , a2 ) such that M |= la1 = la2 and moreover an atom of one of the following
two kinds belongs to A01 : (I) a1 = wr(a2 , i, e); (II) diff(a1 , a2 ) = l, for an l such
that M |= l < k.
Claim: if c1 , c2 are AB-common and c1 ≡k c2 , then cM               M       M M
                                                              1 (k ) = c2 (k ).
Proof of the Claim. The claim is proved by preventively showing, for every A-local
constants a1 , a2 such that a1 ≡k a2 , that the number of the A-local constants j
such that M |= k < j and aM          M      M M
                                 1 (j ) 6= a2 (j ) is less or equal to NA < N . This
is easily shown by induction on the length of the finite sequence witnessing a1 ≡k
a2 .15 We apply this observation to the AB-common array variables c1 , c2 and
let us consider the atoms diff1 (c1 , c2 ) = k1 , . . . , diffn (c1 , c2 ) = kN ∈ A1 . Now
k1 , . . . , kN are all AB-common (hence also A-local) constants, moreover N > NA
and the number of the A-local constants above k M where c1 , c2 differ is at most
NA . According to (b) above, if for absurdity cM           M      M M
                                                   1 (k ) = c2 (k ) does not hold,
then we have M |= k < kN . Since M |= k ≥ 0 (otherwise cM                   M      M M
                                                                       1 (k ) = c2 (k )
follows), this means by Lemma 4 that we have M |= k1 > · · · > kN > 0. However
k1 , . . . , kN are all A-local constants above k, their number is bigger than NA ,
hence we must have M |= cM           M      M M
                                 1 (ki ) = c2 (ki ) for some i = 1, . . . , N ; the latter
implies M |= ki = · · · = kN = 0 by Lemma 4, absurd.                                     ⊣
    In order to interpret A-local constants of sort ARRAY, we assign to an A-local
constant a of sort ARRAY the function aN defined as follows for every i ∈ INDEXN :
  (†-i) if i is equal to k M , where k is an A-local constant, then aN (i) := aM (k M );
 (†-ii) if i is different from k M for every A-local constant k, but nevertherless i
        is equal to k M for some (necessarily B-strict) index constant k and there
15
     According to the definition of reflexive-symmetric-transitive closure, if a1 ≡k a2
     holds then there are d0 , . . . , dn such that d0 = a1 , dn = a2 and for each j < n, we
     have that either (dj , dj+1 ) or (dj+1 , dj ) satifies the above requirements: the induction
     is on such n. Notice that the statement is not entirely obvious because the number of
     the A-local index constants is much bigger than NA (for instance, it includes the AB-
     common constants introduced in Step 1). However induction is easy: it goes through
     the atoms occurring in the input set A01 and uses (a). The required observations are
     the following: if dj = wr(dj+1 , i, e) ∈ A01 , then the only A-local constant where dM     j
     and dM                                                     0
            j+1 can differ is i; if diff(dj , dj+1 ) = l ∈ A1 and M |= l < k, then dj
                                                                                           M
                                                                                              and
     dMj+1 cannot differ on any A-local constant above k
                                                                  M
                                                                    . Iterating these observations
     during induction, the claim is clear: we can collect at most the set of the A-local
     constants occurring in A01 within a wr symbol.
        General Interpolation and Strong Amalgamation for Contiguous Arrays              41

         is an AB-common array variable c such that c ≡k a, then aN (i) is equal
         to cM (k M );
 (†-iii) in the remaining cases, aN (i) is equal to elM or ⊥M depending whether
         M |= 0 ≤ i ∧ i ≤ la holds or not.
    Notice that aN (i) is univocally specified in case (†-ii) because of the above
claim. We now show that
(*) all aN are positive-support functions and all formulæ from A1 ∪ A2 are true
    in N .
Recall in fact that formulæ in A2 are Boolean combinations of A-local atoms of
the kind (25): these are TI ∪ EUF -atoms and, due to their shape, each of them is
true in M iff it is true in A (this is because rd functions are applied only to A-
local index constants, so that the modifications we introduced for passing from
aM to aN does not affect truth of these atoms). Concerning formulæ in A1 , these
are all wr, diff and |−|-atoms.16 The reason why they are true in N is the 0-
instantiation performed by Step 2 (see (a) above). For example, consider an atom
of the kind |a| = la appearing in A1 : since formulae (18) have been instantiated
with all the A-local index constants via Step 2, for all A-local index constant
h, we have M |= rd(a, h) 6= ⊥ iff M |= 0 ≤ h ≤ i. Now, thanks to definition
(†), for all the elements h ∈ INDEXN we have an analogous result: in case h is
equal to k M for some A-local constant k, we employ definition (†-i), otherwise
we use (†-ii) or (†-iii) (for (†-ii), notice that a ≡k c implies that M |= la = lc and
0-instantiation guarantees that cM (k M ) is equal to ⊥M or to elM depending
whether M |= 0 ≤ k ∧ k ≤ lc holds or not). Hence we get that A satisfies
formula (18), since the universal quantifier has been instantiated in all possible
ways. Thus A |= |a| = la , by Lemma 2. The other cases are similar: notice in
particular that if a = wr(a′ , i, e) ∈ A1 then a ≡k a′ . If diff(a, a′ ) = i ∈ A1 , the
relevant case is when M |= i < k and M |= la1 = la2 , but in this case we have
a ≡k a′ too.
    The assignments to the B-local array variables b are defined analogously, so
that
(*) all bN are positive-support functions and all formulæ from B1 ∪ B2 are true
    in N .
    There is however one important point to notice: for all AB-common constants
c of sort ARRAY, our specification of cM does not depend on the fact that we use
the above definition for A-local or for B-local array variables: to see this, we only
have to notice that c ≡k c holds in case (†-ii) is applied. This remark concludes
our proof.


16
     In addition, we have diffn -atoms for n > 1, but these are all AB-common atoms
     that were not part of the initial pair A0 , B 0 . In fact they are also true in N , but
     strictly speaking we do not need to check this fact to get the absurdity that A0 ∧ B 0
     is CARD(TI )-consistent.
