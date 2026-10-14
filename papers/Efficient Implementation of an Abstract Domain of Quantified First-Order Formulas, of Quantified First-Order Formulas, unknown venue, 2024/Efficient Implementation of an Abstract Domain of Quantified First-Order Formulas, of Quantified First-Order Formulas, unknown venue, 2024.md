                                          Efficient Implementation of an Abstract Domain
                                                  of Quantified First-Order Formulas

                                             Eden Frenkel1 , Tej Chajed2 , Oded Padon3 , and Sharon Shoham1

                                             CAV                     Tel Aviv University, Tel Aviv, Israel                CAV
                                                                  1

                                           Artifact
                                                        2
                                                            University of Wisconsin-Madison, Madison, WI, USA            Artifact
arXiv:2405.10308v4 [cs.LO] 19 Aug 2024




                                          Evaluation            3
                                                                  VMware Research, Palo Alto, CA, USA                   Evaluation


                                          Available                                                                     Reusable


                                                Abstract. This paper lays a practical foundation for using abstract in-
                                                terpretation with an abstract domain that consists of sets of quantified
                                                first-order logic formulas. This abstract domain seems infeasible at first
                                                sight due to the complexity of the formulas involved and the enormous
                                                size of sets of formulas (abstract elements). We introduce an efficient rep-
                                                resentation of abstract elements, which eliminates redundancies based on
                                                a novel syntactic subsumption relation that under-approximates seman-
                                                tic entailment. We develop algorithms and data structures to efficiently
                                                compute the join of an abstract element with the abstraction of a concrete
                                                state, operating on the representation of abstract elements. To demon-
                                                strate feasibility of the domain, we use our data structures and algorithms
                                                to implement a symbolic abstraction algorithm that computes the least
                                                fixpoint of the best abstract transformer of a transition system, which
                                                corresponds to the strongest inductive invariant. We succeed at finding,
                                                for example, the least fixpoint for Paxos (which in our representation
                                                has 1,438 formulas with ∀∗ ∃∗ ∀∗ quantification) in time comparable to
                                                state-of-the-art property-directed approaches.

                                                Keywords: Abstract interpretation · First-order logic · Symbolic ab-
                                                straction · Invariant inference · Quantifier alternation · Least fixpoint.


                                         1    Introduction

                                         Recent years have seen significant progress in automated verification based on
                                         first-order logic. In particular, quantified first-order formulas have been used to
                                         model many systems, their properties and their inductive invariants [1, 6, 8–10,
                                         12–17,19,21,23,25,27,29,30]. Automatic verification in this domain is challenging
                                         because of the combination of the complexity of first-order reasoning performed
                                         by solvers and the enormous search space of formulas, especially due to the use
                                         of quantifiers. Despite these challenges, there are impressive success stories of
                                         automatically inferring quantified inductive invariants for complex distributed
                                         and concurrent algorithms [8–10, 13, 14, 16, 25, 29, 30].
                                             Previous works on invariant inference for first-order logic search for invariants
                                         in the form of sets of formulas (interpreted conjunctively) from some language
                                         of quantified first-order formulas. Each approach fixes some restricted, typically
finite (but extremely large) language L, and searches for a set of L-formulas
that form an inductive invariant using sophisticated heuristics and algorithmic
techniques, such as property-directed reachability (IC3) [13, 14], incremental in-
duction [10, 25], generalization from finite instances [8, 16], and clever forms of
pruning and exploration [29, 30]. While prior techniques can successfully handle
some challenging examples, the accumulation of specially-tailored techniques
makes the results computed by these techniques unpredictable, and makes it
hard to extend or improve them.
     Abstract interpretation [4, 5] suggests a more systematic approach for the
development of verification algorithms based on logical languages, where we
consider sets of L-formulas as elements in an abstract domain. The abstraction
of a set of states S in this domain is given by α(S) = {φ ∈ L | ∀s ∈ S. s |= φ},
i.e., the formulas that are satisfied by all states in the set. Algorithms based on
abstract interpretation are better understood and are easier to combine, extend,
and improve. However, an abstract domain of quantified first-order formulas
seems infeasible: for interesting systems, the abstract elements involved in proofs
would contain an astronomical number of formulas.
    The main contribution of this work is to develop algorithms and data struc-
tures that make an abstract domain based on quantified first-order formulas
feasible. Working with this abstract domain introduces two main challenges:
(i) efficiently storing and manipulating abstract elements comprising of many
formulas, and (ii) overcoming solver limitations when reasoning over them. This
work focuses on the first challenge and adopts ideas from prior work [14] to deal
with the second. Our techniques lay a practical foundation for using an abstract
interpretation approach to develop new analyses in the domain of quantified first-
order formulas. We demonstrate feasibility of the abstract domain by applying
it to an analysis of several intricate distributed protocols.
    Our first key idea is to design a subsumption relation for quantified first-
order formulas and use it to represent abstract elements (sets of formulas) more
compactly, pruning away some formulas that are redundant since they are equiv-
alent to or are entailed by another formula. Subsumption over propositional
clauses (disjunctions of literals) is traditionally used for similar pruning pur-
poses (e.g., [18]), but the generalization to first-order formulas, which include
disjunction, conjunction, and quantification, is novel.
    The second key ingredient of our approach is a way to manipulate abstract
elements in our representation. Rather than implementing the standard opera-
tions of α (abstraction) and ⊔ (abstract join), we observe that our subsumption-
based representation makes it more natural to directly implement an operation
that computes the join of an abstract element a with the abstraction of a given
concrete state s, i.e., a ⊔ α({s}). This operation can be used to compute the
abstraction of a set of states, and can also be used to compute the least fixpoint
of the best abstract transformer (in the style of symbolic abstraction [26]). The
crux of computing a ⊔ α({s}) is to weaken the formulas in the representation of
a to formulas that are subsumed by them and that s satisfies.

                                        2
    Finally, the third key ingredient of our approach is a data structure for storing
a set of formulas, with efficient filters for (i) formulas that a given state does not
satisfy, and (ii) formulas that subsume a given formula. This data structure is
then used to store abstract elements, and the filters make the implementation
of a ⊔ α({s}) more efficient.

    While the paper presents the ingredients of our approach (subsumption,
weakening, and the data structure) sequentially, they are interconnected; they all
affect each other in subtle ways, and must be designed and understood together.
Specifically, there is an intricate tradeoff between the precision of subsump-
tion, which determines the extent of pruning (and therefore the compactness
of the representation), and the complexity of abstract domain operations such
as weakening (e.g., for computing a ⊔ α({s})). The definitions, algorithms, and
data structures we present are carefully crafted to balance these considerations.
Our subsumption relation, which approximates entailment, is cheap to compute,
eliminates enough redundancy to keep the representation of abstract elements
compact, and enables an efficient implementation of the weakening operation.

    To evaluate our implementation of the abstract domain, we use it to imple-
ment a symbolic abstraction [26] procedure that computes the least fixpoint of
the best abstract transformer of a transition system (i.e., the strongest inductive
invariant for the transition system in the given language). Our evaluation uses
benchmarks from the literature, mostly from safety verification of distributed
protocols. While our fixpoint computation algorithm is not fully competitive
with property-directed invariant inference approaches that exploit various so-
phisticated heuristics and optimizations, it does demonstrate that fixpoint com-
putation in our abstract domain is feasible, which is quite surprising given the
amount of quantified formulas the domain considers. Our approach successfully
computes the least fixpoint for transition systems that previously could only be
analyzed using property-directed, heuristic techniques (which do not compute
the least fixpoint, but an unpredictable heuristic fixpoint). For example, we suc-
ceed at finding the strongest inductive invariant of Paxos as modeled in [23]
(which in our representation has 1,438 formulas with ∀∗ ∃∗ ∀∗ quantification, rep-
resenting orders of magnitude more subsumed formulas).

   In summary, this paper makes the following contributions:

 1. We develop a compact representation of sets of formulas based on a novel
    syntactic subsumption relation. We make a tradeoff here between the extent
    of pruning and efficiency, accepting some redundant formulas in exchange
    for practical algorithms. (Sec. 3)
 2. We show how to implement a key operation of weakening a formula to be
    satisfied by a given state, and leverage it to compute the join of an ab-
    stract element and the abstraction of a state, when abstract elements are
    represented using our subsumption-based representation. (Sec. 4)
 3. We present a data structure that provides an efficient implementation of
    operations used in the join computation described above. (Sec. 5)

                                          3
 4. We evaluate the approach by applying it to compute the least fixpoint of the
    best abstract transformer for several distributed and concurrent protocols
    from the literature, demonstrating the promise of our approach. (Sec. 6)
    The rest of this paper is organized as follows: Sec. 2 introduces definitions
and notation, Secs. 3 to 6 present the main contributions outlined above, Sec. 7
discusses related work, and Sec. 8 concludes. The proofs of all theorems stated in
the paper are given in App. B. An extended running example appears in App. A.


2     Background

First-order logic. For simplicity of the presentation, we present our approach
for single-sorted first-order logic, although in practice we consider many-sorted
logic. The generalization of our methods to many-sorted logic is straightforward.
    Given a first-order signature Σ that consists of constant, function and relation
symbols, the sets of terms and formulas are defined in the usual way: a term t
is either a variable x, a constant c or a function application f (t1 , . . . , tn ) on
simpler terms; a formula is either an equality between terms t1 = t2 , a relation
application r(t1 , . . . , tn ) on terms, or the result of applying Boolean connectives
or quantification. We also include ⊥ as a formula (that is never satisfied).
    Terms and formulas are interpreted over first-order structures and assign-
ments to the (free) variables. Given a first-order signature Σ, a structure σ =
(U, I) consists of a universe U and an interpretation I to the symbols in Σ.
We denote by structs[Σ] the set of structures of Σ whose universe is a finite
set.1 When considering formulas with free variables V , and given some structure
σ = (U, I), an assignment µ : V → U maps each variable to an element of
the structure’s universe. We write (σ, µ) |= φ to mean that a structure σ with
an assignment µ satisfies a formula φ, and ψ |= φ to mean that a formula ψ
semantically entails φ, i.e., (σ, µ) |= ψ whenever (σ, µ) |= φ.

Abstract interpretation. Abstract interpretation [4,5] is a framework for approx-
imating the semantics of systems. It assumes a concrete domain and an abstract
domain, each given by a partially ordered set, (C, ⊑C ) and (A, ⊑A ), respectively.
These are related via a Galois connection consisting of a monotone abstraction
function α : C → A and a monotone concretization function γ : A → C satisfying
α(c) ⊑A a ⇐⇒ c ⊑C γ(a) for all a ∈ A and c ∈ C.
    In this work we consider logical abstract domains parameterized by a fi-
nite first-order language L of closed formulas over signature Σ. In this context,
concrete elements are sets of states from S = structs[Σ],2 i.e., C = P(S), or-
dered by ⊑C =⊆ (set inclusion). Abstract elements are sets of formulas from
L, i.e., A = P(L), ordered by ⊑A =⊇, and the Galois connection is given by
α(S) = {φ ∈ L | ∀s ∈ S. s |= φ} and γ(F ) = {s ∈ S | ∀φ ∈ F. s |= φ}. That
is, abstraction in this domain consists of all L-formulas that hold on a given
1
    We restrict our attention to FOL fragments that have a finite-model property.
2
    Later we consider non-closed formulas and let S denote structures with assignments.


                                           4
concrete set, and concretization consists of all states that satisfy a given set of
formulas. Note that sets of formulas are interpreted conjunctively in this context.
   This logical abstract domain forms a join-semilattice (meaning every two
elements have a least upper bound) with a least element. The least element,
denoted ⊥A (not to be confused with the formula ⊥), is L, and join, denoted ⊔,
corresponds to set intersection. For example, F ⊔ α({s}) = F ∩ {φ ∈ L | s |=
φ} = {φ ∈ F | s |= φ}, and can be understood as weakening F by eliminating
from it all formulas that are not satisfied by s.


3     Subsumption-Based Representation of Sets of Formulas

In this section we develop an efficient representation for elements in the abstract
domain A = P(L) induced by a finite first-order language L. The abstract
elements are sets of formulas, interpreted conjunctively, which may be extremely
large (albeit finite). Our idea is to reduce the size and complexity of such sets
by avoiding redundancies that result from semantic equivalence and entailment.
For example, when representing a set of formulas we would like to avoid storing
both φ and ψ when they are semantically equivalent (φ ≡ ψ). Similarly, if φ |= ψ
then instead of keeping both φ and ψ we would like to keep only φ.
    In practice, it is not possible to remove all such redundancies based on se-
mantic equivalence and entailment, since, as we shall see in Sec. 4, performing
operations over the reduced representation of abstract elements involves recov-
ering certain subsumed formulas, and finding these in the case of entailment
essentially requires checking all formulas in the language. This is clearly infeasi-
ble for complex languages such as the ones used in our benchmarks (see Table 1),
and is exacerbated by the fact that merely checking entailment is expensive for
formulas with quantifiers. Instead, our key idea is to remove redundancies based
on a cheap-to-compute subsumption relation, which approximates semantic en-
tailment, and enables efficient operations over abstract elements such as joining
them with an abstraction of a concrete state.
    We start the section with an inductive definition of a family of finite first-
order languages that underlies all of our developments (Sec. 3.1). We then intro-
duce a syntactic subsumption relation for first-order formulas (Sec. 3.2), which
we leverage to develop an efficient canonicalization of formulas, effectively de-
termining a single representative formula for each subsumption-equivalence class
(Sec. 3.3). We then use antichains of canonical formulas, i.e., sets of canonical
formulas where no formula is subsumed by another, to represent sets of formulas
(Sec. 3.4). Secs. 4 and 5 develop ways to effectively manipulate this representa-
tion in order to accommodate important operations for abstract interpretation
algorithms, such as weakening an abstraction to include a given concrete state.


3.1   Bounded First-Order Languages

At core of our approach is an inductively-defined family of first-order languages,
termed bounded first-order languages. These languages are all finite and bound

                                         5
various syntactic measures of formulas (e.g., number of quantifiers, size of the
Boolean structure), which, in turn, determine the precision of the abstract do-
main. The inductive definition of bounded languages facilitates efficient recursive
implementations of our developments.
    We fix a signature Σ and a variable set V . Def. 1 provides the inductive
definition of the family of bounded first-order languages (over Σ and V ), where
each language L is also equipped with a bottom element ⊥L (equivalent to false).
We use SX to denote the set of permutations over a set of variables X, and use
φπ to denote the formula obtained by substituting free variables in a formula
φ according to π ∈ SX . A set of formulas F is SX -closed if φπ ∈ F for every
φ ∈ F , π ∈ SX . All bounded first-order languages will be SV -closed; this will be
important for canonicalization. We use φ̄ = ⟨φ1 , . . . , φn ⟩ to denote a sequence of
formulas, φ−i to denote the formula φn−i+1 in the sequence, |φ̄| for the length
of φ̄, and [φ̄] for its set of indices {1, . . . , |φ̄|}. We use L∗ for the set of all (finite)
sequences of formulas from L, and ϵ for the empty sequence (|ϵ| = 0).
Definition 1 (Bounded First-Order Languages). A bounded first-order
language is one of the following, where X ⊆ V denotes a finite set of variables,
and L, L1 and L2 denote bounded first-order languages:
       LA = A ∪ {⊥} with ⊥LA = ⊥, where A is any finite SV -closed set of formulas
∨[L1 , L2 ] = {φ1 ∨ φ2 | φ1 ∈ L1 , φ2 ∈ L2 } with ⊥∨[L1 ,L2 ] = ⊥L1 ∨ ⊥L2
∧[L1 , L2 ] = {φ1 ∧ φ2 | φ1 ∈ L1 , φ2 ∈ L2 } with ⊥∧[L1 ,L2 ] = ⊥L1 ∧ ⊥L2
               _                                            _
   ∨k [L] = { φ̄ | φ̄ ∈ L∗ and |φ̄| ≤ k} with ⊥∨k [L] =        ϵ, where k ∈ N
               ^                                  ^
   ∧ω [L] = { φ̄ | ϵ ̸= φ̄ ∈ L∗ } with ⊥∧ω [L] = ⟨⊥L ⟩
    ∃X [L] = {∃X.φ | φ ∈ L} with ⊥∃X [L] = ∃X.⊥L
    ∀X [L] = {∀X.φ | φ ∈ L} with ⊥∀X [L] = ∀X.⊥L
   ∃∀X [L] = {QX.φ | φ ∈ L, Q ∈ {∃, ∀}} with ⊥∃∀X [L] = ∀X.⊥L
    The base case is any finite set of formulas (over Σ and V ) that is closed un-
der variable permutations, augmented by ⊥ (denoting false). Typical examples
include the set of all literals over Σ and V with a bounded depth of function
applications. We introduce binary language constructors for disjunction and con-
junction, each operating on two possibly different languages. We also introduce
constructors for homogeneous disjunction of at most k disjuncts, as well as un-
bounded non-empty conjunction, over any single language. Finally, we introduce
constructors for quantification (∃ or ∀) over a finite set of variables and a lan-
guage, as well as a constructor that includes both quantifiers for languages where
both options are desired. Note that for the construction of a logical abstract do-
main, we are interested in languages where all formulas are closed (have no free
variables), but the inductive definition includes languages with free variables.
    The semantics of formulas in each language is defined w.r.t. states S that
consist of first-order structures and assignments to the free variables, following
the standard first-order semantics, extendedW to conjunctions and disjunctions
                                                                         V       of
finite sequences in the natural way, where ϵ ≡ ⊥. (We do not allow ϵ, which
would have been equivalent to “true”, since it is not useful for our developments.)

                                              6
W Observe that for a fixed language L, the formulas φ1 ∨ φ2 ∈ ∨[L, L] and
  ⟨φ1 , φ2 ⟩ ∈ ∨2 [L] are syntactically different but semantically equivalent (and
similarly for conjunctions). Nonetheless, we introduce homogeneous disjunction
and conjunction since they admit a more precise subsumption relation, yielding
a more efficient representation of sets of formulas. Also note that we consider
bounded disjunction but unbounded conjunction; Sec. 4.3 explains this choice.

Example 1. L = ∀{x,y} [∨2 [LA ]] with A = {p(x), ¬p(x), p(y), ¬p(y)} is a bounded
first-order language over signature Σ that has one unary predicate p and vari-
ables V = {x, y}. Formulas in this language are universally quantified homoge-W
neous disjunctions of at most two literals.
                                      W                W L includes ∀{x, y}. ϵ,
                                            For instance,
which is also ⊥L , as well as ∀{x, y}. ⟨p(x)⟩, ∀{x, y}. ⟨p(x), ¬p(y)⟩, etc.

3.2   Syntactic Subsumption
Next, we define a subsumption relation for each bounded first-order language.
The subsumption relation serves as an easy-to-compute under-approximation for
entailment between formulas from the same language. We use ⊑L to denote the
subsumption relation for language L, or simply ⊑ when L is clear from context.
When φ ⊑ ψ we say φ subsumes ψ, and then we will also have φ |= ψ.
Definition 2 (Subsumption). We define ⊑L inductively, following the def-
inition of bounded first-order languages, as follows, where ◦ ∈ {∨, ∧}, k ∈ N,
Q, Q′ ∈ {∃, ∀}, X is a finite set of variables, and L, L1 and L2 are bounded
first-order languages:
                   φ ⊑LA ψ iff φ = ⊥ or φ = ψ
  φ1 ◦ φ2 ⊑◦[L1 ,L2 ] ψ1 ◦ ψ2 iff φ1 ⊑L1 ψ1 and φ2 ⊑L2 ψ2 (pointwise extension)
          _             _
            φ̄ ⊑∨k [L]      ψ̄ iff ∃m : [φ̄] → [ψ̄]. ∀i ∈ [φ̄]. φi ⊑ ψm(i) and m is injective
          ^             ^
            φ̄ ⊑∧ω [L]      ψ̄ iff ∃m : [ψ̄] → [φ̄]. ∀i ∈ [ψ̄]. φm(i) ⊑ ψi
  (QX.φ) ⊑QX [L] (QX.ψ) iff ∃π ∈ SX . φ ⊑L ψπ
 (QX.φ) ⊑∃∀X [L] (Q′ X.ψ) iff ∃π ∈ SX . φ ⊑L ψπ, and Q = ∀ or Q′ = ∃

    The subsumption relation of a bounded first-order language L is composed,
hierarchically, from the subsumption relations of the bounded first-order lan-
guages that L is composed from. For example, the languages participating in
the composition of L = ∀{x,y} [∨2 [LA ]] defined in Ex. 1 are LA , ∨2 [LA ], and
∀{x,y} [∨2 [LA ]], and each is equipped with its own subsumption relation.
    In the base case, formulas in LA are only subsumed by themselves or by ⊥. For
example, considering Ex. 1, p(x) ̸⊑LA p(y). Subsumption is lifted to languages
obtained by binary conjunctions and disjunctions in a pointwise manner. For the
languages obtained by homogeneous constructors, a mapping over indices deter-
mines which element of one sequence subsumes which element of the other. To
approximate
   W           entailment,
                    W       the mapping in the disjunctive case maps each element
of φ̄ to oneV    in   ψ̄ that
                           V it subsumes, and in the conjunctive case maps each
element of ψ̄ to one in φ̄ that subsumes it. As a result, subsumption is more


                                              7
precise in the homogeneous case than in the binary one. For example, considering
A from Ex. 1, p(x) ∨ p(y) ̸⊑∨[LA ,LA ] p(y) ∨ p(x),
                                              W     even though the W formulas are
semantically equivalent. On the other hand, ⟨p(x), p(y)⟩ ⊑∨2 [LA ] ⟨p(y), p(x)⟩
    In the case of quantifiers, subsumption is lifted from the language of the
body while considering
                    W permutations over   W the quantified variables. For example,
in Ex. 1, ∀{x,W y}.   ⟨p(x)⟩ ⊑ LW∀{x, y}.   ⟨p(y)⟩ due to variable permutations,
even though ⟨p(x)⟩ ̸⊑∨2 [LA ] ⟨p(y)⟩. When both quantifiers are considered, a
universal quantifier can subsume an existential one.
    The injectivity requirement for ⊑∨k [L] can be dropped without damaging any
of the definitions or theorems in this section, but it enables a simpler definition
of the weakening operator in Sec. 4 (as discussed further in Sec. 4.3).
    The following theorem establishes the properties of ⊑L .

Theorem 1 (Properties of ⊑L ). For any bounded first-order language L, ⊑L
is a preorder (i.e., reflexive and transitive) such that for any φ, ψ ∈ L, if φ ⊑ ψ
then φ |= ψ. Moreover, ⊥L ⊑L φ for any φ ∈ L.

    As with entailment, where two distinct formulas can entail each other (i.e.,
be semantically equivalent), there can be distinct formulas φ, ψ ∈ L with φ ⊑L ψ
and ψ ⊑L φ (since ⊑L is not always a partial order, i.e., not antisymmetric).
We call such formulas subsumption-equivalent, and denote this by φ ≡⊑L ψ.
(≡⊑L is clearly an equivalence relation.) The existence of subsumption-equivalent
formulas is a positive sign, indicating that our subsumption relation manages
to capture nontrivial semantic equivalences. This is thanks to the definition
of subsumption for homogeneous W       disjunction
                                             W      and conjunction, as well as for
quantification. For example,
                    V            ⟨φ,
                                  V  ψ⟩ ≡  ⊑   ⟨ψ, φ⟩ (and similarly for conjunction),
and if φ ⊑ ψ then ⟨φ, ψ⟩ ≡⊑ ⟨φ⟩. For quantifiers, QX.φ ≡⊑ QX.φπ for any
π ∈ SX and Q ∈ {∃, ∀}. (In contrast, ⊑LA is always antisymmetric, and the
definitions of ∨[L1 , L2 ] and ∧[L1 , L2 ] preserve antisymmetry.)


3.3   Canonicalization

As a first step towards an efficient representation of sets of formulas, we use a
canonicalization of formulas w.r.t. ≡⊑ , which allows us to only store canonical
formulas as unique representatives of their (subsumption-) equivalence class. In
general, a canonicalization w.r.t. an equivalence relation ≡ over a set S is a
function c : S → S such that ∀x ∈ S. c(x) ≡ x (representativeness) and ∀x, y ∈
S. x ≡ y ⇐⇒ c(x) = c(y) (decisiveness). We say that x is canonical if c(x) = x.
When the equivalence relation is derived from a preorder (as ≡⊑ is derived from
⊑) then the preorder is a partial order over the set of canonical elements. For our
case, that means that ⊑L is a partial order over the set of canonical L-formulas.
    It is useful, both for the algorithms developed in the sequel and for the def-
inition of canonicalization for QX [L] (Q ∈ {∃, ∀, ∃∀}), to define a total order
≤L over canonical L-formulas that extends ⊑L . We thus define the canonical-
ization function cL and the total order ≤L over canonical L-formulas by mutual
induction. For a set of canonical L-formulas F , we use min⊑L F to denote the


                                          8
set of formulas in F not subsumed by others, i.e., min⊑L F = {φ ∈ F | ∀ψ ∈
F \{φ}. ψ ̸⊑ φ}, and use min≤L F to denote the minimal element of a non-empty
set F w.r.t. the total order ≤L . Finally, we use ⟨φ̄⟩≤ for the sequence obtained by
sorting φ̄ according to ≤ in ascending order, and similarly ⟨F ⟩≤ for the sequence
obtained by sorting the elements of a set F .

Definition 3 (Canonicalization). For every bounded first-order language L,
we define the canonicalization function cL : L → L and a total order ≤L over
canonical L-formulas by mutual induction (where ◦ ∈ {∨, ∧} and Q ∈ {∃, ∀}):
                             cLA (φ) = φ
              c◦[L1 ,L2 ] (φ1 ◦ φ2 ) = cL1 (φ1 ) ◦ cL2 (φ2 ) (pointwise)
                              _        _
                     c∨k [L] ( φ̄) =      ⟨cL (φ1 ), . . . , cL (φ|φ̄| )⟩≤
                                                                          L
                              ^        ^
                    c∧ω [L] ( φ̄) =       ⟨min ⊑L {cL (φ1 ), . . . , cL (φ|φ̄| )}⟩≤
                                                                                   L
                                                      
                 cQX [L] (QX.φ) = QX. min ≤L cL (φπ) π ∈ SX
                 c∃∀X [L] (QX.φ) = cQX [L] (QX.φ)

and
                         ≤LA is an arbitrary total order extending ⊑LA
 φ1 ◦ φ2 ≤◦[L1 ,L2 ] ψ1 ◦ ψ2 ⇐⇒ φ1 <L1 ψ1 , or φ1 = ψ1 and φ2 ≤L2 ψ2
         _             _
           φ̄ ≤∨k [L]      ψ̄ ⇐⇒ φ̄ is a suffix of ψ̄,
                                       or ∃i ∈ [φ̄] ∩ [ψ̄]. φ−i <L ψ−i ∧ ∀j < i. φ−j = ψ−j
        ^                ^
            φ̄ ≤∧ω [L]       ψ̄ ⇐⇒ ψ̄ is a prefix of φ̄,
                                       or ∃i ∈ [φ̄] ∩ [ψ̄]. φi <L ψi ∧ ∀j < i. φj = ψj
      QX.φ ≤QX [L] QX.ψ ⇐⇒ φ ≤L ψ
    QX.φ ≤∃∀X [L] Q′ X.ψ ⇐⇒ Q = Q′ and φ ≤L ψ, or Q = ∀ and Q′ = ∃

 where φ <L ψ is shorthand for “φ ≤L ψ and φ ̸= ψ”.

    Our inductive definition of canonicalization in Def. 3 recognizes the only
possible sources of nontrivial subsumption-equivalence in our construction: non-
canonicity of subformulas, ordering of sequences, internal subsumption in ∧ω [·]-
sequences, and permuting of quantified variables. To address these, we canonical-
ize all subformulas, order their sequences w.r.t ≤L in ∨k [L] and ∧ω [L], minimize
∧ω [L]-sequences w.r.t ⊑L , and in QX [L], Q ∈ {∃, ∀, ∃∀}, choose the permuta-
tion yielding the ≤L -least (canonical) body. For the total order in the cases of
Boolean connectives, we use lexicographic-like orderings carefully designed to
extend their associated subsumption relations (e.g., homogeneous disjunction
uses a right-to-left lexicographic ordering). For quantification, the total order is
directly lifted from the total order for canonical bodies.
    As an example, consider L = ∀{x,y} [∨2 [LA ]] from Ex. 1. To obtain a canoni-
calization for L, we provide an arbitrary total order ≤LA , say p(x) <LA ¬p(x) <LA
p(y) <LA ¬p(y) (recall that ⊥ ∈ LA is least). This uniquely determines the


                                                9
total order and canonicalization of L Wand all of its sub-languages.   W          For exam-
ple, canonicalization of both  W   ∀{x,  y}.   ⟨p(x)⟩  and  ∀{x,  y}.     ⟨p(y)⟩, which are
⊑L -equivalent,
            W      is ∀{x,
                        W  y}.   ⟨p(x)⟩.   This
                                              W  is because   p(x)    < L
                                                                       WA   p(y),  and thus
cW∨2 [LA ] ( ⟨p(x)⟩)
                 W    =    ⟨p(x)⟩  < ∨2 [LA ]   ⟨p(y)⟩  = c ∨2 [LA ] (  ⟨p(y)⟩).  Note  that
   ⟨p(x)⟩ and ⟨p(y)⟩ are both canonical, but adding quantifiers merges the
 two formulas into the same subsumption-equivalence class, necessarily making
 the quantified version W of one of themWnon-canonical. Similarly, the ⊑∨2 [LA ] -
 equivalent
 W            formulas   ⟨p(x), p(y)⟩ and ⟨p(y), p(x)⟩ are both canonicalized into
   ⟨p(x), p(y)⟩ (by sorting the sequences of literals according to ≤LA ).
     The properties of cL and ≤L defined above are established by the following
 theorem, which ensures that Def. 3 is well-defined (e.g., that whenever min≤L is
 used, ≤L is a total order).
Theorem 2. For any bounded language L, cL is a canonicalization w.r.t. ≡⊑L ,
that is, it is representative (cL (φ) ≡⊑L φ) and decisive (φ ≡⊑L ψ ⇐⇒ cL (φ) =
cL (ψ)); ⊑L is a partial order over canonical L-formulas; and ≤L is a total order
over canonical L-formulas that extends ⊑L .
Corollary 1. For any φ, ψ ∈ L, if φ ⊑L ψ then cL (φ) ≤L cL (ψ).
      Henceforth, we use L to denote the set of canonical L-formulas.

3.4     Representing Sets of Formulas
We utilize the subsumption relation and canonicalization to efficiently represent
sets of formulas which are interpreted conjunctively as antichains of canonical
formulas, where an antichain is a set of formulas incomparable by subsumption.
Definition 4 (Set Representation). Given a set of formulas F ⊆ L, we
define its representation as the set RF = min ⊑L {c(φ) | φ ∈ F }.
     The representation combines two forms of redundancy elimination: the use
of canonical formulas eliminates redundancies due to subsumption-equivalence,
and the use of ⊑L -minimal elements reduces the size of the set by ignoring
subsumed formulas. Observe that the more permissive the subsumption relation
is, the smaller the set representations are, because more formulas will belong to
the same equivalence class and more formulas will be dropped by min⊑L .
     This representation preserves the semantics of a set of formulas (interpreted
conjunctively). For sets that are upward-closed w.r.t. subsumption (e.g., α(S)
for some set of states S), the representation is lossless as a set can be recovered
by taking the upward closure of its representation. For a set F ⊆ L, we use ↑F to
denote its upward closure (w.r.t. ⊑L ), given by ↑F = {φ ∈ L | ∃ψ ∈ F. ψ ⊑L φ}.
Theorem 3 (Antichain Representation).
                           V    V       For F ⊆ L and RF = min ⊑L {c(φ) |
φ ∈ F } its representation, RF ≡ F and ↑RF = ↑F .
Corollary 2. If F ⊆ L is upward closed w.r.t. ⊑L then F = ↑RF .
      In particular, Cor. 2 applies to any set that is closed under entailment.


                                            10
4     The Weaken Operator

This section develops an algorithm that computes a weaken operator, which takes
a representation of an upward-closed set F ⊆ L and a state s and computes a
representation of F ∩ α({s}) = {φ ∈ F | s |= φ}. When F is viewed as an
abstract element, this operation corresponds to computing F ⊔ α({s}). While
it is not a general abstract join operator, joining an abstract element with the
abstraction of a single concrete state is a powerful building block that can be
used, for example, to compute the abstraction of a set of states or even the least
fixpoint of the best abstract transformer (á la symbolic abstraction [26]).
    In an explicit representation of F , computing F ⊔ α({s}) would amount
to removing from F all the formulas that are not satisfied by s. However, in
the subsumption-based representation RF , simply removing said formulas is not
enough. Instead, we must weaken them, i.e., replace them by formulas they
subsume that are satisfied by s. To this end, Sec. 4.1 develops an appropriate
weakening operator for a single formula, and Sec. 4.2 then lifts it to antichains
used as representations.


4.1   Weakening a Single Canonical Formula

Given a canonical formula φ and a state s such that s ̸|= φ, the weaken operator
computes the set of minimal canonical formulas that are subsumed by φ and
satisfied by s, which can be understood as a representation of ↑{φ} ∩ α({s}).

Definition 5 (The Weaken Operator). The weaken operator of L is the
function WL : L × S → P(L) defined as follows:

            WL (φ, s) = min ⊑L {cL (ψ) | ψ ∈ L, φ ⊑ ψ, and s |= ψ} .

    Note that WL (φ, s) returns a set of formulas, since there may be different
incomparable ways to weaken φ such that it is satisfied by s.
    While Def. 5 does not suggest a way to compute WL (φ, s), the following
theorem provides a recursive implementation of WL (φ, s) that follows the in-
ductive structure of bounded languages. For the quantification cases, we weaken
according to all assignments of variables in X ⊆ V . Recall that a state can be
unpacked as s = ((U, I), µ) where (U, I) is a first-order structure (universe and
interpretation) and µ is an assignment to variables (into U). For assignments
                   ←−
µ and ν, we use µ ∪ ν to denote the assignment obtained from µ by updating
(possibly extending) it according to ν.

Theorem 4 (Implementation of Weaken). Let φ ∈ L be a canonical for-
mula in a bounded first-order language L and s ∈ S a state. If s |= φ then
WL (φ, s) = {φ}. If s ̸|= φ, then WL (φ, s) is given by:

                             (
                                 {ψ ∈ A | s |= ψ},   if φ = ⊥
              WLA (φ, s) =
                                 ∅,                  if φ ̸= ⊥


                                           11
    W∨[L1 ,L2 ] (φ1 ∨ φ2 , s) = {ψ ∨ φ2 | ψ ∈ WL1 (φ1 , s)} ∪ {φ1 ∨ ψ | ψ ∈ WL2 (φ2 , s)}
   W∧[L1 ,L2 ] (φ1 ∧ φ2 , s) = {ψ1 ∧ ψ2 | ψ1 ∈ WL1 (φ1 , s), ψ2 ∈ WL2 (φ2 , s)}
                 _                                                 
         W∨k [L]      φ̄, s = min ⊑∨ [L] W|φ̄| ∪ W|φ̄|+1 where
                                            k
            n_                                                                              o
    W|φ̄| =      ⟨φ1 , . . . , φi−1 , ψ, φi+1 , . . . , φ|φ̄| ⟩≤ | i ∈ [φ̄], ψ ∈ WL (φi , s) and
                                                                L
               n_                                                                  o
    W|φ̄|+1 =       ⟨φ1 , . . . , φ|φ̄| , ψ⟩≤ | ψ ∈ WL (⊥L , s) and |φ̄| < k
                                             L
                 ^           n^                                                           o
         W∧ω [L]      φ̄, s =             ⟨min ⊑L WL (φ1 , s) ∪ · · · ∪ WL φ|φ̄| , s ⟩≤
                                                                                           L

                                                                                                 ←
                                                                                                 −
                                                                                                  
W∃X [L] (∃X.φ, ((U, I), µ)) = min ⊑∃X [L] {c(∃X.ψ) | ν : X → U , ψ ∈ WL φ, ((U, I), µ ∪ ν) }
                                                                                      ←
                                                                                      −
                                                                                                  
W∀X [L] (∀X.φ, ((U, I), µ)) = min ⊑∀X [L] {c(∀X.ψ) | ψ ∈ Ωφ {((U, I), µ ∪ ν) | ν : X → U} }
        where Ωφ0 ({s1 , . . . , sn }) = {φn | φ1 ∈ WL (φ0 , s1 ), . . . , φn ∈ WL (φn−1 , sn )}
         W∃∀X [L] (∃X.φ, s) = W∃X [L] (∃X.φ, s)
                                                                                
         W∃∀X [L] (∀X.φ, s) = min ⊑∃∀X [L] W∃X [L] (∃X.φ, s) ∪ W∀X [L] (∀X.φ, s)

    When s |= φ, no weakening of φ is needed for s to satisfy it. In the case of
LA , only ⊥ can be weakened to make s satisfy it, yielding the set of formulas
from A that are satisfied by s. (For LA , weakening anything except ⊥ that is not
satisfied by s yields the empty set.) In the case of disjunction, it suffices for one of
the disjuncts to be satisfied by s. Therefore, weakening is done by (i) weakening
exactly one of the existing disjuncts, which applies to both ∨[L1 , L2W    ] and ∨k [L];
or by (ii) adding a disjunct that weakens ⊥L , which applies only to φ̄ ∈ ∨k [L]
when |φ̄| < k. In the case of homogeneous disjunction, each resulting disjunc-
tion needs to be sorted to restore canonicity; moreover, some of the resulting
disjunctions may be subsumed by others, so min ⊑∨k [L] is applied to the set
of weakened disjunctions. In the case of conjunction, all conjuncts need to be
weakened to be satisfied by s. In the binary case, this leads to all pairs that
combine weakened conjuncts. But in the homogeneous case a single conjunction
can accumulate all weakened conjuncts, so weakening always yields a singleton
set; filtering the weakened conjuncts using min ⊑L is required to ensure canonic-
ity, as one weakened conjunct may subsume another. To satisfy an existentially
quantified formula, it suffices for the body to be satisfied by a single assignment.
Therefore, each possible assignment ν contributes to the result of weakening.
In contrast, for a universally quantified formula the body must be satisfied by
all assignments. Therefore, the body of the formula is iteratively weakened by
all assignments. In both cases, formulas are re-canonicalized and non-minimal
elements are removed. The case of ∃∀X [L] combines the two quantified cases.

Example 2. Consider applying the weaken operator   W      of L = ∀{x,y} [∨2 [LA ]] from
Ex. 1 to the bottom element ⊥L = ∀{x, y}. ϵ, with the state s = ((U, I), µ)
where U = {a, b}, pI = {a, b}, and µ is an empty assignment. To weaken W             the
universally quantified formula, we first iteratively weaken its body, φ0 = ϵ,
with the states s1 , . . . , s4 , each of which extends s with one of the 4 possible
assignments to x, y. Since all of these states satisfy p(x) and p(y), the first


                                               12
  Algorithm 1: In-place Weaken for LSet[L]
      Input: An antichain of canonical L-formulas R stored in the LSet[L] data
             structure and a state s ∈ S
      Output: R modified in place to store WL (R, s)
 1 U := R|̸=|s ;
 2 for φ ∈SU do R.remove(φ);
 3 W :=    φ∈U WL (φ, s);
 4 for φ ∈ W sorted by ≤L do
 5     if R|⊑φ = ∅ then R.insert(φ);


                                   W        W
weakening (with s1 ) results in { ⟨p(x)⟩, ⟨p(y)⟩}, and no formula is weakened
further in later iterations (since both of them are already satisfied by s2 , s3 , s4 ).
As we have seen in Sec. 3.3, both formulas are canonical; however, they become
subsumption-equivalent when the quantifier prefix is added, demonstrating the
need for additional canonicalization in the computation of   W weaken for ∀X [·].
The result is the antichain of canonical formulas {∀{x, y}. ⟨p(x)⟩}. Note that
the weakened formula ⊥L has 21 formulas in its ⊑L -upward closure, and its
weakening has 14 formulas (see App. A.4 for the lists of formulas); yet throughout
the weakening process we only dealt with at most two formulas.

4.2     Weakening Sets of Formulas

                        S to sets of canonical formulas. For a set R ⊆ L, we
We lift the weaken operator
define WL (R, s) = min ⊑ φ∈R WL (φ, s), motivated by the following theorem.

Theorem 5 (From Weaken to Join). Let F ⊆ L be upward-closed w.r.t.
⊑, RF its representation (RF = min ⊑ {c(φ) | φ ∈ F }), and  S s a state. The
representation of F ⊔ α({s}) is given by WL (RF , s) = min ⊑ φ∈RF WL (φ, s).

Corollary 3 (Weaken for a Set of States). Let F ⊆ L be upward-closed
w.r.t. ⊑, RF its representation, and s1 , . . . , sn states. The representation of F ⊔
α({s1 , . . . , sn }) is given by WL (WL (· · · WL (WL (RF , s1 ), s2 ), · · · sn−1 ), sn ).

Corollary 4 (Abstraction of a Set of States). The representation of
α({s1 , . . . , sn }) is given by WL (WL (· · · WL (WL ({⊥L }, s1 ), s2 ), · · · sn−1 ), sn ).

    Thm. 5 and Cor. 3 show that weakening of a single formula can be lifted to
compute join between an upward-closed set of formulas (represented using its
minimal elements w.r.t. ⊑) and the abstraction of one or more states.
    Next, we observe that we can implement WL (R, s) by (i) focusing only on
formulas that actually need weakening, i.e., formulas in R that are not satisfied
by s, without iterating over formulas that s satisfies; and (ii) leveraging the ≤L
total order to accumulate the set of minimal elements more efficiently.
    Alg. 1 presents our implementation of WL (R, s) for an antichain R of canon-
ical formulas and a state s. It updates R to WL (R, s) in place, which is useful for


                                              13
computing an abstraction of a set of states (Cor. 3) or even for fixpoint computa-
tion (Sec. 6). The algorithm uses a data structure LSet[L] (whose implementation
is explained in Sec. 5) that stores a set of canonical L-formulas and supports
two efficient filters: one for formulas that are not satisfied by a given state s,
denoted by R|̸=|s ; and one for formulas that subsume a given formula φ, denoted
by R|⊑φ . Formally: R|̸=|s = {ψ ∈ R | s ̸|= ψ} and R|⊑φ = {ψ ∈ R | φ ⊒ ψ}.
    To weaken R, Alg. 1 first identifies all formulas that need weakening using
the R|̸=|s filter. It then removes these formulas, weakens them, and adds the
weakened formulas back to the set, while filtering out formulas that are not ⊑L -
minimal. For the minimality filtering, we leverage ≤L to ensure that if φ ⊑L ψ
then φ is added before ψ. As a result, when inserting a formula φ we only need to
check that it is not already subsumed by another formula in the set, which is done
by checking if R|⊑φ is empty3 . Importantly, a formula φ ∈ R \ R|̸=|s cannot be
subsumed by a formula from WL (ψ, s) for ψ ∈ R|̸=|s . (If we assume the contrary
we easily get that ψ ⊑ φ, contradicting the fact that R is an antichain.)


4.3    Design Consideration and Tradeoffs

We are now in a position to discuss the tradeoffs and considerations that arise
in our framework in the design of languages and their subsumption relations,
explaining the design choices behind Defs. 1 and 2.
     There is a tradeoff between the precision of the subsumption relation ⊑L and
the complexity of implementing the weaken operator WL . From a representation
perspective, a more precise ⊑L is desirable (i.e., relating more formulas), since
it means that the upward closure ↑{φ} of a formula φ is larger, and (upward-
closed) sets of formulas can be represented using less minimal formulas. On
the other hand, when ↑{φ} is larger, computing WL (φ, s) is generally more
complicated. As an extreme case, if ⊑L is trivial (i.e., a formula only subsumes
itself), we get no pruning in the representation, but computing WL (φ, s) is
very easy, since it is either {φ} or ∅. As another example, compare ∨[L, L]
with ∨2 [L]. The subsumption relation of ∨[L, L] is a pointwise extension, while
W of ∨2 [L] allows
that              W     swapping the two formulas, which is more precise. (E.g.,
  ⟨φ, ψ⟩ ⊑∨2 [L] ⟨ψ, φ⟩ always holds but we might have φ ∨ ψ ̸⊑∨[L,L] ψ ∨ φ.)
Accordingly, weakening of ∨2 [L]-formulas is slightly more involved.
     As opposed to reordering of disjuncts,
                                       W      ⊑∨k [L] does
                                                        W not allow multiple dis-
juncts to subsume the same one, e.g., ⟨φ, ψ⟩ ̸⊑∨k [L] ⟨ψ⟩ even if φ ⊑L ψ (recall
that the mapping between disjuncts must be injective). This choice makes the
computation of W∨k [L] simpler, as it only needs to consider individually weak-
ening each disjunct or adding a new one, but not merging of disjuncts   W (to “make
space” for a new disjunct). For example, when computing W    W∨ 2 [L] (  ⟨φ1 , φ2 ⟩, s),
we do not have to consider formulas of the form ⟨φ, ψ⟩ where s |= ψ and
φ1 , φ2 ⊑L φ, which we would need to include if the mapping was not required to
3
    While the implementation of the weaken operator only checks the emptiness of R|⊑φ ,
    the full set is used in the recursive implementation of R|⊑φ (Sec. 5).


                                           14
be injective. One seemingly undesirable consequence of the injectivity Wrequire-
ment is that canonicalWformulas may contain redundant disjuncts, e.g., ⟨φ, ψ⟩
when φ ⊑ ψ (or even ⟨φ, φ⟩). However, when formulas are obtained by itera-
tive weakening, as in the computation of the representation of α(S) for a set of
concrete states S, formulas with such redundancies will be eliminated as they
are always subsumed by a canonical formula without redundancies.
    Our design of bounded first-order languages uses bounded disjunction but
unbounded conjunction. The reason is that we obtain formulas by weakening
other formulas, starting from ⊥L . In this scenario, bounding the size of con-
junctions would have replaced one conjunction by all of its subsets smaller than
the bound, causing an exponential blowup in the number of formulas, without
contributing much to generalization. On the other hand, bounding the size of
disjunctions yields generalization without blowing up the number of formulas (in
fact, it reduces the number of formulas compared to unbounded disjunction).


5   Data Structure for Sets of Formulas

The implementation of WL (R, s) presented in Alg. 1 uses the filters R|̸=|s and
R|⊑φ . Since the sets may be very large, a naive implementation that iterates over
R to find formulas that are not satisfied by s (R|̸=|s ) or formulas that subsume
φ (R|⊑φ ) may become inefficient. We therefore introduce a data structure for
bounded first-order languages, which we call LSet[L], that stores a set of canoni-
cal L-formulas R (not necessarily an antichain), and implements R|̸=|s and R|⊑φ
without iterating over all formulas in R. The key idea is to define the LSet[L]
data structure recursively, following the structure of L, and to use auxiliary data
to implement the R|̸=|s and R|⊑φ filters more efficiently.
    For example, to implement LSet[∨[L1 , L2 ]], we store a set of ∨[L1 , L2 ]-
formulas and two auxiliary data fields: an LSet L : LSet[L1 ] and a map M :
Map[L1 , LSet[L2 ]]. We maintain the invariant that φ1 ∨ φ2 is in the set iff
φ2 ∈ M [φ1 ], and that L contains the same L1 -formulas as the keys of M . Then,
to find formulas that are not satisfied by a state s, i.e., formulas where both dis-
juncts are not satisfied by s, we first query L to find φ1 ’s that are not satisfied
by s, and for each such φ1 we query the LSet M [φ1 ] to find φ2 ’s that are not
satisfied by s. Implementing the subsumption filter follows a similar logic.
    Our implementation of LSet[∨k [L]] uses a trie data structure that generalizes
the binary case. Each edge is labeled by an L-formula, and each node represents
an ∨k [L]-formula that is the disjunction of the edge labels along the path from
the root to the node. The outgoing edges of each node are stored using an
LSet[L] that can be used to filter only the edges whose label is not satisfied by a
given state, or subsumes a given formula. Then, the R|̸=|s and R|⊑W φ̄ filters are
implemented by recursive traversals of the tree that only traverse filtered edges.
    The recursive implementation for the other language constructors is simpler,
and follows a similar intuition to that of the cases presented above. The base
case LSet[LA ] is implemented without any auxiliary data using straightforward
iteration. The full details of the LSet[L] data structure appear in App. C.


                                        15
6     Implementation and Evaluation

To evaluate our abstract domain implementation, we used it to implement a sym-
bolic abstraction [26, 28] algorithm that computes the least fixpoint of the best
abstract transformer of a transition system. We evaluated our implementation
on 19 distributed protocols commonly used as benchmarks in safety verification
and obtained promising results.


6.1     Implementation

We implemented our abstract domain and the symbolic abstraction algorithm in
Flyvy,4 an open-source verification tool written in Rust, whose implementation
leverages parallelism and the optimizations detailed below. The implementation
and benchmarks used, as well as the log files and raw results from the experiments
reported, are publicly available in this paper’s artifact [7].
     Our implementation receives as input (i) a first-order transition system (ι, τ )
over signature Σ, where ι is a closed first-order formula over Σ specifying the
initial states and τ is a closed first-order formula over two copies of Σ specifying
the transitions, and (ii) a specification of a bounded first-order language L over
Σ that defines the abstract domain P(L). The reachable states of the system
are the least fixpoint of a concrete transformer T : P(S) → P(S) given by
T (S) = {s′ ∈ S | s′ |= ι ∨ ∃s ∈ S. ⟨s, s′ ⟩ |= τ }, where ⟨s, s′ ⟩ |= τ indicates
that the pair of states satisfies the two-vocabulary formula τ , i.e., that s′ is a
successor of s w.r.t the transition relation defined by τ . For more details on this
style of modeling distributed systems in first-order logic, see [22–24].
     The Galois connection (α, γ) between P(S) and P(L) induces a best abstract
transformer T ♯ : P(L) → P(L) defined by T ♯ = α ◦ T ◦ γ. Any fixpoint of T ♯ ,
i.e., a set F ⊆ L such that T ♯ (F ) = F , is an inductive invariant of (ι, τ ) (when
sets are interpreted conjunctively), and the least fixpoint, lfpT ♯ , is the strongest
inductive invariant in L. The strongest inductive invariant is useful for verifying
safety properties of the system, or showing that they cannot be proven in L (if
the strongest inductive invariant in L cannot prove safety, neither can any other
inductive invariant expressible in L).
     Symbolic abstraction computes lfpT ♯ without computing T ♯ explicitly: be-
ginning with F = L (the least element in P(L)), and as long as F ̸= V        T ♯ (F ), a
                                                                         ′
counterexample to induction (CTI) of F is sampled, i.e., a state  V s ̸|= F that
is either an initial state or the successor of a state s with s |= F , and F is up-
dated to F ⊔ α({s′ }). Our implementation uses the representation RF and Alg. 1
to compute the join (more details in App. E). To find CTIs or determine that
none exist we use SMT solvers (Z3 [20] and cvc5 [2]), with queries restricted to
the EPR fragment (following [23]), which ensures decidability and the existence
of finite counterexamples. Solvers still struggle in some challenging benchmarks,
and we employ several optimizations detailed in App. F to avoid solver timeouts.
4
    Flyvy’s code is available at https://github.com/flyvy-verifier/flyvy.


                                            16
6.2     Experiments
To evaluate our techniques, we computed the least fixpoints (strongest inductive
invariants) of 19 distributed protocols commonly used as benchmarks in safety
verification, in a language expressive enough to capture their human-written
safety invariants. We used all EPR benchmarks from [14], except for universally
quantified Paxos variants. To evaluate the utility of the LSet data structure
described in Sec. 5, we ran each experiment twice, once using LSet and once
using a naive (but parallelized) implementation for the filters R|̸=|s and R|⊑φ .
    To specify the bounded first-order language for each example, we provide the
tool with a quantifier prefix (using ∃X [·], ∀X [·], and ∃∀X [·]) composed on top of
a quantifier-free bounded language that captures k-pDNF (following [14]). A k-
pDNF formula has the structure c1 → (c2 ∨· · ·∨ck ), where c1 , c2 , . . . , ck are cubes
(conjunctions of literals). We specify such formulas as ∨[∨n [LA1 ], ∨k−1 [∧ω [LA2 ]]],
where k and n are parameters, and A1 and A2 are sets of literals. Inspired by [29],
we observe that we can restrict the variables used in A1 and A2 to reduce the
size of the language without losing precision.5 For additional details see App. D.
The list of examples with their language parameters appears in Table 1. For each
example, we report the quantifier structure, the k and n parameters of the k-
pDNF quantifier-free matrix, and the approximate size of the language L. Recall
that the size of the abstract domain is 2|L| .
    All experiments were performed on a 48-threaded machine with 384 GiB of
RAM (AWS’s z1d.metal) and a three-hour time limit. For each example we
also provide runtimes of two state-of-the-art safety verification tools, DuoAI [29]
and P-FOL-IC3 [14]. Note that, unlike our technique, these tools look for some
inductive invariant proving safety, not necessarily the strongest, but are also
given fewer explicit language constraints. Moreover, the runtimes of DuoAI and
P-FOL-IC3 are sourced from their respective papers, and reflect different archi-
tectures and time limits. Thus, the inclusion of their results is not intended as a
precise comparison to our tool, but as a reference for the difficulty of the invariant
inference task of each example, as evidenced by state-of-the-art techniques.

6.3     Results
The results of the symbolic abstraction computation are presented in Table 1. For
each experiment we report the runtime of our tool and the following statistics:
the percentage of time spent weakening formulas (as opposed to searching for
CTIs), the number of formulas in the representation of the fixpoint (if reached),
and the maximal number of formulas in the representation of an abstract element
throughout the run. Each experiment was run five times, unless it timed out, in
which case it was run only once. We aggregate the results of each statistic across
multiple runs as median ± deviation, where deviation is the maximal distance
between the median value and the value of the statistic in any given run.
5
    One of the language reductions used by [29] relies on an overly generalized lemma [29,
    Lemma 6]; we confirmed this with the authors of [29]. We prove and use a correct
    (but less general) variant of this lemma, see App. D for details.


                                            17
Table 1. Symbolic abstraction over invariant inference benchmarks with a time limit of
3 hours (10800s). We describe the bounded language underlying the abstract domain of
each example, including its approximate size, and report the runtime of our technique—
with and without using LSet—along with some statistics. For reference, we provide
runtimes of two state-of-the-art safety-verification tools. ‘T/O’ indicates a timeout,
and ‘N/A’ indicates that the example was not reported by the respective tool.

                   Language            Runtime                                                  Safety (sec)
  Example                                            LSet % in W Lfp. Size    Max. Size
                quant. k n size           (sec)                                              P-FOL-IC3 DuoAI
                                        0.4 ± 0.1     ✓    6±1 %                 28 ± 7
    lockserv       ∀2     1 3 104                                      12                         19       1.9
                                        0.5 ± 0.1     –   6±1 %                  29 ± 3
toy-consensus-                          0.2 ± 0.0     ✓    9±2 %                 18 ± 5
                   ∀3     1 3 103                                       5                         4        1.9
      forall                            0.2 ± 0.0     –   7±1 %                  18 ± 4
                                        1.6 ± 0.1     ✓ 16 ± 1 %                182 ± 22
     ring-id       ∀ 3
                          1 3 10 5
                                                                       97                         7        3.5
                                        1.9 ± 0.1     – 20 ± 1 %               189 ± 22
                                        0.5 ± 0.1     ✓    8±0 %                 26 ± 2
  sharded-kv       ∀5     1 3 104                                      20                         8        1.9
                                        0.5 ± 0.0     –   8±1 %                  26 ± 4
                                       32.6 ± 3.3     ✓ 43 ± 7 %              8531 ± 119
      ticket       ∀ 4
                          1 5 10 9
                                                                      2621                        23      23.9
                                      862.2 ± 21.9    – 97 ± 0 %              8533 ± 121
   learning-                              T/O         ✓      98 %               9576194
                   ∀4     1 4 1011                                      –                         76      52.4
     switch                               T/O         –     100 %                 5998
  consensus-                            3.0 ± 0.2     ✓ 19 ± 1 %               717 ± 109
                   ∀ 3
                          1 3 10 6
                                                                       41                         50       3.9
   wo-decide                            4.0 ± 0.6     – 38 ± 4 %               724 ± 43
  consensus-                            3.5 ± 0.4     ✓ 21 ± 2 %               740 ± 114
                   ∀4     1 3 106                                      51                       1980      11.9
      forall                            5.1 ± 0.9     – 40 ± 6 %               708 ± 82
                                   4029.4   ±  220.7  ✓   30  ±  2 %        271255  ±  13081
      cache        ∀6     1 5 1011                                   106348                     2492      N/A
                                          T/O         – 100 ± 0 %            19183 ± 9466
 sharded-kv-                            0.3 ± 0.0     ✓   3±0 %                   4±0
                ∀1 (∃∀)2 1 2 102                                        4                         4        2.1
 no-lost-keys                           0.3 ± 0.0     –   2±0 %                   4±0
toy-consensus- 2                        0.3 ± 0.0     ✓    9 ±  1  %             18 ±  4
               ∀ (∃∀)1 ∀1 1 3 104                                       5                         4        2.6
        epr                             0.3 ± 0.0     –   7±1 %                  19 ± 3
  consensus-                            5.1 ± 0.7     ✓ 17 ± 2 %               800 ± 137
                (∃∀)1 ∀4 1 3 106                                       51                         37       4.8
        epr                             8.8 ± 1.7     – 46 ± 8 %               783 ± 88
     client-                            0.2 ± 0.0     ✓   4  ±  1  %              5 ± 0
                ∀2 (∃∀)1 2 1 103                                        2                         4        1.5
   server-ae                            0.2 ± 0.1     –   3±1 %                   5±0
                                    621.5 ± 246.8 ✓       1±1 %               1693 ± 203
   paxos-epr    ∀4 (∃∀)2 2 3 1011                                     1438                       920      60.4
                                     789.6 ± 285.5    – 11 ± 3 %              1737 ± 168
    flexible-                       166.7   ±  29.3   ✓   4  ±  1  %          1622  ±  177
                ∀4 (∃∀)2 2 3 1011                                     964                        418      78.7
   paxos-epr                          235.6 ± 31.7    – 35 ± 8 %              1575 ± 196
     multi-                               T/O         ✓       2%                 27508
                ∀5 (∃∀)3 2 3 1030                                       –                       4272      1549
   paxos-epr                              T/O         –     100 %                 6400
       fast-                              T/O         ✓       1 %                16290
                ∀4 (∃∀)3 2 4 1014                                       –                       9630     26979
   paxos-epr                              T/O         –      99 %                13683
  stoppable-                              T/O         ✓     100 %                37529
                ∀7 (∃∀)3 2 5 10155                                      –                     >18297     4051
   paxos-epr                              T/O         –     100 %                 3331
    vertical-                             T/O         ✓     100  %               112990
                ∀4 (∃∀)3 3 5 1054                                       –                       T/O      T/O
   paxos-epr                              T/O         –     100 %                 2576




   For simple examples, the fixpoint computation terminates very quickly, of-
ten faster than the other tools, and maintains only tens or hundreds of formulas
throughout its run. Some of the larger examples, such as ticket, paxos-epr,
flexible-paxos-epr, and cache also terminate after similar times to the other
tools. In fact, this is the first work to compute least fixpoints for any Paxos vari-
ant or cache. (DuoAI, for instance, has a component that attempts to compute
a precise fixpoint, but [29] reports that it times out on all Paxos variants.)


                                                     18
    Unsurprisingly, there is a significant gap between the runtimes of examples
with and without quantifier alternation, mostly due to the time spent in SMT
solvers. For example, in ticket we spend about 43% of the runtime perform-
ing weakenings, but this percentage drops to 1% and 4% for paxos-epr and
flexible-paxos-epr, respectively. This causes the runtime of paxos-epr to
exceed that of ticket by more than an order of magnitude, although its fix-
point computation considers fewer formulas and actually spends less time weak-
ening. Similarly, in cache we manage to prove a fixpoint of a hundred thousand
formulas in about an hour and spend a third of it weakening formulas, while
multi-paxos-epr and fast-paxos-epr time out, although they consider far
fewer formulas and spend a negligible amount of time weakening.
    Next, we observe that the use of LSet significantly reduces time spent in weak-
ening, leading to more than an order of magnitude difference even in moderate
examples, e.g., ticket and paxos-epr. In terms of the total fixpoint computa-
tion time, in examples where the runtime is small or dominated by the SMT
solvers, the effect might be negligible, but otherwise the speedup is significant.
For example, cache is not solved within the 3-hour limit with a naive data struc-
ture; it gets stuck after reaching ∼ 20,000 formulas in the abstraction, whereas
using LSet it is solved in about an hour while handling more than ten times
the number of formulas. Similarly, in the two unsolved examples where SMT
calls seem to be the bottleneck (multi-paxos-epr and fast-paxos-epr), using
a naive data structure causes weakening to become the bottleneck and time out.
    Finally, the remaining timeouts, learning-switch, stoppable-paxos-epr,
and vertical-paxos-epr, are the only examples where the weakening pro-
cess itself is the bottleneck. These are cases where the language induced by
the human-written invariant, using the constraining parameters of bounded lan-
guages, create a inefficient weakening process. The cause for this is either a
profusion of literals in the basis language (> 600 in learning-switch and
stoppable-paxos-epr, less than 200 in all other examples), or a very expressive
language (e.g., vertical-paxos-epr uses 3-pDNF, whereas all other examples
use 1- and 2-pDNF). For these examples, it might be necessary to restrict the
languages in additional ways, e.g., as was done in [29]. Our experience, however,
is that the more significant bottleneck for computing least fixpoints for the most
complicated examples is the SMT queries.


7   Related Work

Many recent works tackle invariant inference in first-order logic [8–10, 13, 14, 16,
25,29,30]. These works are all property-guided and employ sophisticated heuris-
tics to guide the search for invariants. Of these works, the most closely related
to ours are [29, 30]. DistAI [30] is restricted to universally quantified invariants,
while DuoAI [29] infers invariants with quantifier alternations. DuoAI defines a
“minimum implication graph” enumerating all formulas in a first-order logical
language, whose transitive closure can be understood as a specific subsump-
tion relation, and where replacing a node with its successors can be understood

                                         19
as a form of weakening. DuoAI’s “top-down refinement” precisely computes the
strongest invariant in the logical domain. However, this computation does not
scale to complex examples such as all Paxos variants, in which case “bottom-
up refinement” is used—a property-guided process that does not compute the
strongest invariant. Our approach based on a generic subsumption relation is
both more principled and more scalable, as it succeeds in computing the least
fixpoint for some Paxos variants.
     Another work concerning a least-fixpoint in a logical domain is [18], which
computes the set of propositional clauses up to length k implied by a given for-
mula, minimized by the subsumption relation ⊑=⊆; a trie-based data structure
is used to maintain the formulas, weaken them, and check subsumption of a for-
mula by the entire set. Both that data structure and LSet[∨k [·]] bear similarity
to UBTrees [11], also employed in [3], which store sets and implement filters
for subsets and supersets. However, while UBTrees and LSets always maintain
ordered tree paths, these are unordered in [18], which allows [18] to perform
weakening directly on the data structure, whereas we need to remove the un-
satisfied disjunctions, weaken, and insert them. On the other hand, this makes
filtering for subsets in UBTrees and LSets more efficient. Also note that LSet is
more general than both, since it supports a more general subsumption relation.


8   Conclusion
We have developed key algorithms and data structures for working with a logi-
cal abstract domain of quantified first-order formulas. Our fundamental idea is
using a well-defined subsumption relation and a weaken operator induced by it.
This idea makes the abstract domain feasible, and it is also extensible: while we
explored one possible subsumption relation and its associated weaken operator,
future work may explore others, representing different tradeoffs between pruning
and weakening. We demonstrated the feasibility of our approach by computing
the least abstract fixpoint for several distributed protocols modeled in first-order
logic—a challenging application domain where previously only property-directed
heuristics have been successful. For some of the examples in our evaluation, the
computation still times out. In some of these cases, SMT queries (for comput-
ing CTIs) become the bottleneck. Dealing with this bottleneck is an orthogonal
problem that we leave for future work. For the examples with the largest log-
ical languages, abstract domain operations remain the bottleneck, and future
work may either scale the abstract domain implementation to such languages or
explore combinations with property-directed approaches.

Acknowledgments. We thank Alex Fischman and James R. Wilcox for their contri-
butions to the Flyvy verification tool. We thank Raz Lotan, Kenneth McMillan, and
the anonymous reviewers for their helpful and insightful comments.
    The research leading to these results has received funding from the European Re-
search Council under the European Union’s Horizon 2020 research and innovation pro-
gramme (grant agreement No [759102-SVIS]). This research was partially supported
by the Israeli Science Foundation (ISF) grant No. 2117/23.


                                        20
References
 1. Ball, T., Bjørner, N.S., Gember, A., Itzhaky, S., Karbyshev, A., Sagiv, M.,
    Schapira, M., Valadarsky, A.: Vericon: towards verifying controller programs
    in software-defined networks. In: O’Boyle, M.F.P., Pingali, K. (eds.) ACM
    SIGPLAN Conference on Programming Language Design and Implementation,
    PLDI ’14, Edinburgh, United Kingdom - June 09 - 11, 2014. pp. 282–293.
    ACM (2014). https://doi.org/10.1145/2594291.2594317, https://doi.org/
    10.1145/2594291.2594317
 2. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: Fisman, D., Rosu, G. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 13243, pp. 415–442. Springer (2022).
    https://doi.org/10.1007/978-3-030-99524-9_24, https://doi.org/10.1007/
    978-3-030-99524-9_24
 3. Cadar, C., Dunbar, D., Engler, D.R., et al.: Klee: Unassisted and automatic gen-
    eration of high-coverage tests for complex systems programs. In: OSDI. vol. 8, pp.
    209–224 (2008)
 4. Cousot, P., Cousot, R.: Abstract interpretation: A unified lattice model for static
    analysis of programs by construction or approximation of fixpoints. In: Gra-
    ham, R.M., Harrison, M.A., Sethi, R. (eds.) Conference Record of the Fourth
    ACM Symposium on Principles of Programming Languages, Los Angeles, Califor-
    nia, USA, January 1977. pp. 238–252. ACM (1977). https://doi.org/10.1145/
    512950.512973, https://doi.org/10.1145/512950.512973
 5. Cousot, P., Cousot, R.: Systematic design of program analysis frameworks. In:
    Aho, A.V., Zilles, S.N., Rosen, B.K. (eds.) Conference Record of the Sixth Annual
    ACM Symposium on Principles of Programming Languages, San Antonio, Texas,
    USA, January 1979. pp. 269–282. ACM Press (1979). https://doi.org/10.1145/
    567752.567778, https://doi.org/10.1145/567752.567778
 6. Feldman, Y.M.Y., Padon, O., Immerman, N., Sagiv, M., Shoham, S.: Bounded
    quantifier instantiation for checking inductive invariants. In: TACAS (1). Lecture
    Notes in Computer Science, vol. 10205, pp. 76–95 (2017). https://doi.org/10.
    1007/978-3-662-54577-5_5
 7. Frenkel, E., Chajed, T., Padon, O., Shoham, S.: Efficient implementation
    of an abstract domain of quantified first-order formulas (artifact) (Apr
    2024). https://doi.org/10.5281/zenodo.10938367, https://doi.org/10.5281/
    zenodo.10938367
 8. Goel, A., Sakallah, K.A.: On symmetry and quantification: A new approach to ver-
    ify distributed protocols. In: NFM. Lecture Notes in Computer Science, vol. 12673,
    pp. 131–150. Springer (2021). https://doi.org/10.1007/978-3-030-76384-8_9
 9. Goel, A., Sakallah, K.A.: Towards an automatic proof of lamport’s paxos. In:
    FMCAD. pp. 112–122. IEEE (2021). https://doi.org/10.34727/2021/isbn.
    978-3-85448-046-4_20
10. Hance, T., Heule, M., Martins, R., Parno, B.: Finding invariants of distributed
    systems: It’s a small (enough) world after all. In: Mickens, J., Teixeira, R. (eds.)
    18th USENIX Symposium on Networked Systems Design and Implementation,


                                          21
    NSDI 2021, April 12-14, 2021. pp. 115–131. USENIX Association (2021), https:
    //www.usenix.org/conference/nsdi21/presentation/hance
11. Hoffmann, J., Koehler, J.: A new method to index and query sets. In: IJCAI.
    vol. 99, pp. 462–467 (1999)
12. Itzhaky, S., Banerjee, A., Immerman, N., Nanevski, A., Sagiv, M.: Effectively-
    propositional reasoning about reachability in linked data structures. In: CAV.
    Lecture Notes in Computer Science, vol. 8044, pp. 756–772. Springer (2013).
    https://doi.org/10.1007/978-3-642-39799-8_53
13. Karbyshev, A., Bjørner, N.S., Itzhaky, S., Rinetzky, N., Shoham, S.: Property-
    directed inference of universal invariants or proving their absence. J. ACM 64(1),
    7:1–7:33 (2017). https://doi.org/10.1145/3022187, https://doi.org/10.1145/
    3022187
14. Koenig, J.R., Padon, O., Shoham, S., Aiken, A.: Inferring invariants with quantifier
    alternations: Taming the search space explosion. In: Fisman, D., Rosu, G. (eds.)
    Tools and Algorithms for the Construction and Analysis of Systems - 28th Interna-
    tional Conference, TACAS 2022, Held as Part of the European Joint Conferences
    on Theory and Practice of Software, ETAPS 2022, Munich, Germany, April 2-7,
    2022, Proceedings, Part I. Lecture Notes in Computer Science, vol. 13243, pp. 338–
    356. Springer (2022). https://doi.org/10.1007/978-3-030-99524-9_18, https:
    //doi.org/10.1007/978-3-030-99524-9_18
15. Löding, C., Madhusudan, P., Peña, L.: Foundations for natural proofs and quan-
    tifier instantiation. Proc. ACM Program. Lang. 2(POPL), 10:1–10:30 (2018).
    https://doi.org/10.1145/3158098, https://doi.org/10.1145/3158098
16. Ma, H., Goel, A., Jeannin, J., Kapritsos, M., Kasikci, B., Sakallah, K.A.: I4: incre-
    mental inference of inductive invariants for verification of distributed protocols. In:
    SOSP. pp. 370–384. ACM (2019). https://doi.org/10.1145/3341301.3359651
17. Mathur, U., Madhusudan, P., Viswanathan, M.: What’s decidable about pro-
    gram verification modulo axioms? In: TACAS (2). Lecture Notes in Computer
    Science, vol. 12079, pp. 158–177. Springer (2020). https://doi.org/10.1007/
    978-3-030-45237-7_10
18. McMillan, K.: Don’t-care computation using k-clause approximation. Proc.
    IWLS’05 pp. 153–160 (2005)
19. McMillan, K.L., Padon, O.: Deductive verification in decidable fragments with
    ivy. In: SAS. Lecture Notes in Computer Science, vol. 11002, pp. 43–55. Springer
    (2018). https://doi.org/10.1007/978-3-319-99725-4_4
20. de Moura, L.M., Bjørner, N.S.: Z3: an efficient SMT solver. In: Ramakrishnan,
    C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems, 14th International Conference, TACAS 2008, Held as Part of the
    Joint European Conferences on Theory and Practice of Software, ETAPS 2008,
    Budapest, Hungary, March 29-April 6, 2008. Proceedings. Lecture Notes in Com-
    puter Science, vol. 4963, pp. 337–340. Springer (2008). https://doi.org/10.1007/
    978-3-540-78800-3_24, https://doi.org/10.1007/978-3-540-78800-3_24
21. Murali, A., Peña, L., Blanchard, E., Löding, C., Madhusudan, P.: Model-
    guided synthesis of inductive lemmas for FOL with least fixpoints. Proc. ACM
    Program. Lang. 6(OOPSLA2), 1873–1902 (2022). https://doi.org/10.1145/
    3563354, https://doi.org/10.1145/3563354
22. Padon, O.: Deductive Verification of Distributed Protocols in First-Order Logic.
    Ph.D. thesis, Tel Aviv University (2019)
23. Padon, O., Losa, G., Sagiv, M., Shoham, S.: Paxos made EPR: decidable reason-
    ing about distributed protocols. Proc. ACM Program. Lang. 1(OOPSLA), 108:1–


                                            22
    108:31 (2017). https://doi.org/10.1145/3140568, https://doi.org/10.1145/
    3140568
24. Padon, O., McMillan, K.L., Panda, A., Sagiv, M., Shoham, S.: Ivy: safety verifi-
    cation by interactive generalization. In: PLDI. pp. 614–630. ACM (2016). https:
    //doi.org/10.1145/2908080.2908118
25. Padon, O., Wilcox, J.R., Koenig, J.R., McMillan, K.L., Aiken, A.: Induction dual-
    ity: primal-dual search for invariants. Proc. ACM Program. Lang. 6(POPL), 1–29
    (2022). https://doi.org/10.1145/3498712
26. Reps, T.W., Sagiv, S., Yorsh, G.: Symbolic implementation of the best transformer.
    In: Steffen, B., Levi, G. (eds.) Verification, Model Checking, and Abstract In-
    terpretation, 5th International Conference, VMCAI 2004, Venice, Italy, January
    11-13, 2004, Proceedings. Lecture Notes in Computer Science, vol. 2937, pp. 252–
    266. Springer (2004). https://doi.org/10.1007/978-3-540-24622-0_21, https:
    //doi.org/10.1007/978-3-540-24622-0_21
27. Taube, M., Losa, G., McMillan, K.L., Padon, O., Sagiv, M., Shoham, S., Wilcox,
    J.R., Woos, D.: Modularity for decidability of deductive verification with ap-
    plications to distributed systems. In: PLDI. pp. 662–677. ACM (2018). https:
    //doi.org/10.1145/3192366.3192414
28. Thakur, A.V.: Symbolic abstraction: Algorithms and applications. Ph.D. thesis,
    The University of Wisconsin-Madison (2014)
29. Yao, J., Tao, R., Gu, R., Nieh, J.: DuoAI: Fast, automated inference of induc-
    tive invariants for verifying distributed protocols. In: Aguilera, M.K., Weather-
    spoon, H. (eds.) 16th USENIX Symposium on Operating Systems Design and
    Implementation, OSDI 2022, Carlsbad, CA, USA, July 11-13, 2022. pp. 485–
    501. USENIX Association (2022), https://www.usenix.org/conference/osdi22/
    presentation/yao
30. Yao, J., Tao, R., Gu, R., Nieh, J., Jana, S., Ryan, G.: Distai: Data-driven auto-
    mated invariant learning for distributed protocols. In: OSDI. pp. 405–421. USENIX
    Association (2021)




                                         23
A     Running Example

A.1    Bounded First-Order Language

Consider the signature Σ with one unary predicate p, and variables V = {x, y}.
These induce the set of first-order literals A = {p(x), ¬p(x), p(y), ¬p(y)}, which
can be used to define, for example, the bounded language L = ∀{x,y} [∨2 [LA ]].
Formulas in this language are universally quantified (homogeneous) disjunctions
of at most two literals. For instance, L includes
            W
 – ∀{x, y}. W ϵ, which is also ⊥L ,
 – ∀{x, y}. W⟨p(x)⟩,
 – ∀{x, y}. W⟨p(y), p(x)⟩,
 – ∀{x, y}. W⟨p(x), ¬p(y)⟩,
 – ∀{x, y}. ⟨p(x), p(x)⟩,
 – etc.


A.2    Subsumption

The language L = ∀{x,y} [∨2 [LA ]] defined in App. A.1 is composed, hierarchi-
cally, using three bounded first-order languages: LA , ∨2 [LA ], and ∀{x,y} [∨2 [LA ]].
Each is equipped with its own subsumption  W   relation as Wdefined inductively in
Def. 2. Observe that p(x) ̸⊑LA p(y) and ⟨p(x)⟩ ̸⊑∨2 [LA ] ⟨p(y)⟩, but
                               _                            _
                    ∀{x, y}.       ⟨p(x)⟩   ⊑L   ∀{x, y}.    ⟨p(y)⟩,
                                                           W       W
because by permuting x and y we can infer the above from ⟨p(x)⟩ ⊑ ⟨p(x)⟩.
Thus, one source of subsumption is due to permutation of variables in ways
that do not change the semantics of a formula. Another is due to reordering
subformulas in a homogeneous connective, for example,
                  _                         _
                    ⟨p(x), p(y)⟩ ⊑∨2 [LA ]     ⟨p(y), p(x)⟩.

   What the above demonstrates is that subsumption approximates semantic
entailment by utilizing the local semantic characteristics of each language. It is
indeed not the case that p(x) |= p(y), but when both are quantified universally,
or when both are put in a disjunction and then reordered, we can infer something
useful about their semantics using simple facts like p(x) |= p(x) and p(y) |= p(y),
which are trivial and thus assumed by the basis subsumption of LA .


A.3    Canonicalization

In order to have a canonicalization w.r.t ≡⊑L for L = ∀{x,y} [∨2 [LA ]] defined in
App. A.1, we need to provide an arbitrary total order ≤LA . Say we choose

                      p(x) <LA ¬p(x) <LA p(y) <LA ¬p(y),


                                            24
and recall that ⊥ ∈ LA is least. Def. 3, together with Thm. 2, show that the
above induces a canonicalization cL , as well as a total order ≤L over canonical
L-formulas which extends ⊑L .
    To see how the canonicalization cL eliminates subsumption equivalence, con-
sider the two subsumption-equivalent formulas presented in App. A.2:
                         _                            _
                 ∀{x, y}. ⟨p(x)⟩ ≡⊑L ∀{x, y}. ⟨p(y)⟩.
                                          W
The canonicalization of both is ∀{x, y}. ⟨p(x)⟩, since cL selects the minimal
canonical body after applying            W permutations over x, y (Def. 3), and
                            W all variable
p(x) <LA p(y). Note that ⟨p(x)⟩ and ⟨p(y)⟩ are both canonical, but adding
quantifiers merges the two formulas into the same subsumption-equivalence class,
necessarily making the quantified version of one of them non-canonical.
   Similarly, at the level of ∨2 [LA ],
                     _                                  _
                      ⟨p(x), p(y)⟩        ≡⊑∨2 [LA ]        ⟨p(y), p(x)⟩,

and canonicalizationWis achieved by sorting the sequences of literals, so both
are canonicalizedWas ⟨p(x), p(y)⟩. Interestingly, observe that for the quantified
formula ∀{x, y}. ⟨p(x), p(y)⟩, any variable permutation applied the    W quantifier-
free body, after canonicalization w.r.t ∨2 [LA ], i.e., sorting, yields ⟨p(x), p(y)⟩.
Thus, for the subsumption-equivalence class of this formula, canonicalization
w.r.t ∨2 [LA ] also eliminates any subsumption-equivalence due to quantification.
This is not entirely surprising, since in this case, permuting the variables and
permuting the literals in the disjunction has the same effect.


A.4    Weakening

As an example,W let us weaken the bottom element ⊥L for L = ∀{x,y} [∨2 [LA ]],
i.e., ∀{x, y}. ϵ, with the state s = ((U, I), µ) where U = {a, b}, I(p) = {a, b},
and µ is an arbitrary assignment. At the topmost level, the weakening procedure
for L = ∀{x,y} [∨2 [LA ]], detailed in Thm. 4, requires us to first compute

Ωφ0 ({s1 , . . . , sn }) = {φn | φ1 ∈ W∨2 [LA ] (φ0 , s1 ), . . . , φn ∈ W∨2 [LA ] (φn−1 , sn )}
           W
where φ0 = ϵ, and s1 , . . . , sn are all updates of s with assignments to x, y. The
above can be computed iteratively as follows:
           W
 – R0 := S{ ϵ};
 – R1 := φ∈R0 W∨2 [LA ] (φ, s1 );
 – ···    S
 – Rn := φ∈Rn−1 W∨2 [LA ] (φ, sn ).

InWour caseWn = 4, and all updated states satisfy p(x) and p(y). Therefore, R1 =
{ ⟨p(x)⟩, ⟨p(y)⟩}, and no formula is weakened further, since both formulas in
R1 are satisfied by the remaining s2 , s3 , s4 . Thus, R1 = · · · = Rn . As expected,


                                              25
at the end of this process we are guaranteed to get formulas satisfying all possible
updates of s with assignments to x, y.
    As we saw in App. A.3, both of the resulting formulas are canonical; however,
adding the requisite quantification results in one non-canonical formula. This
demonstrates the need for additional canonicalization for ∀X [·].
    Note the savings the subsumption-based representation affords us even for
this simple language. The singleton {⊥L }, which we effectively weakened per
Alg. 1, represents the following abstract element containing 21 formulas:
     n              _                 _          _                 _                 _
L=       ∀{x, y}.       ϵ, ∀{x, y}.
                                 ⟨p(x)⟩, ∀{x, y}. ⟨¬p(x)⟩, ∀{x, y}. ⟨p(y)⟩, ∀{x, y}. ⟨¬p(y)⟩,
                 _                       _                     _                       _
         ∀{x, y}. ⟨p(x), p(x)⟩, ∀{x, y}. ⟨p(x), p(y)⟩, ∀{x, y}. ⟨p(x), ¬p(x)⟩, ∀{x, y}. ⟨p(x), ¬p(y)⟩,
                 _                        _                      _                        _
         ∀{x, y}. ⟨¬p(x), p(x)⟩, ∀{x, y}. ⟨¬p(x), p(y)⟩, ∀{x, y}. ⟨¬p(x), ¬p(x)⟩, ∀{x, y}. ⟨¬p(x), ¬p(y)⟩
                 _                       _                     _                       _
         ∀{x, y}. ⟨p(y), p(x)⟩, ∀{x, y}. ⟨p(y), p(y)⟩, ∀{x, y}. ⟨p(y), ¬p(x)⟩, ∀{x, y}. ⟨p(y), ¬p(y)⟩,
                 _                        _                      _                        _               o
         ∀{x, y}. ⟨¬p(y), p(x)⟩, ∀{x, y}. ⟨¬p(y), p(y)⟩, ∀{x, y}. ⟨¬p(y), ¬p(x)⟩, ∀{x, y}. ⟨¬p(y), ¬p(y)⟩ .

                                   W
Moreover, the singleton {∀{x, y}. ⟨p(x)⟩} we got from the weakening process
represents the following abstract element containing 14 formulas:
     n           _                _
         ∀{x, y}. ⟨p(x)⟩, ∀{x, y}. ⟨p(y)⟩,
                 _                      _                      _                       _
         ∀{x, y}. ⟨p(x), p(x)⟩, ∀{x, y}. ⟨p(x), p(y)⟩, ∀{x, y}. ⟨p(x), ¬p(x)⟩, ∀{x, y}. ⟨p(x), ¬p(y)⟩,
                 _                       _
         ∀{x, y}. ⟨¬p(x), p(x)⟩, ∀{x, y}. ⟨¬p(x), p(y)⟩,
                 _                      _                      _                       _
         ∀{x, y}. ⟨p(y), p(x)⟩, ∀{x, y}. ⟨p(y), p(y)⟩, ∀{x, y}. ⟨p(y), ¬p(x)⟩, ∀{x, y}. ⟨p(y), ¬p(y)⟩,
                 _                       _               o
         ∀{x, y}. ⟨¬p(y), p(x)⟩, ∀{x, y}. ⟨¬p(y), p(y)⟩ ,


but throughout the weakening process we only dealt with at most two formulas.


B        Proofs for Subsumption-Based Representation
B.1       Correctness of Subsumption
Proof (Thm. 1). The proof follows the inductive definition of subsumption in
Def. 2. The semantic claim, that for each φ, ψ ∈ L if φ ⊑ ψ then φ |= ψ, is
straightforward to verify using the definition of φ ⊑ ψ for each case: For the
base case we have φ = ⊥ or φ = ψ, which implies φ |= ψ. For both disjunction
cases, if each disjunct of φ has a disjunct of ψ that it subsumes, and therefore
entails, then any state satisfying φ, which therefore satisfies one of its disjuncts,
also satisfies some disjunct of ψ. For both conjunction cases, if each conjunct
of ψ has a conjunct of φ that subsumes it, and therefore entails it, than any
state satisfying φ, which therefore satisfies all of its conjuncts, must also sat-
isfy all of the conjuncts of ψ. These conditions for disjunction and conjunction,
respectively, are ensured by the respective subsumption relations. For the case
of quantifiers, adding the same quantification to any φ and ψ, or quantifying
φ universally and ψ existentially, as well as permuting quantified variables, all
maintain entailment, so the semantic property of subsumption can be directly
lifted from the induction hypothesis.

                                                26
     Next, we prove by induction that ⊑L is a preorder for all L; i.e., that it is
reflexive and transitive. For the base case of ⊑LA the claim clearly holds. For L1 ◦
L2 where ◦ ∈ {∨, ∧}, ⊑L1 ◦L2 is the standard preorder resulting from pointwise
extension, which maintains reflexivity and transitivity. For ∨k [L], reflexivity is
shown by choosing the mapping    W m(i)        W ¯using the reflexivity of ⊑L (i.h.);
                                        W = i and
regarding transitivity, given φ̄ ⊑ ψ̄ ⊑ ξ,           there exist injective m1 : [φ̄] →
                        ¯ so m2 ◦ m1 : [φ̄] → [ξ]
[ψ̄] and m2 : [ψ̄] → [ξ],                       ¯ is injective and guarantees φi ⊑L
ψm1 (i) ⊑L ξ(m2 ◦m1 )(i) , and using the transitivity of ⊑L (i.h.), φi ⊑L ξ(m2 ◦m1 )(i) .
The cases of ∧ω [L] and QX [L] for Q ∈ {∃, ∀} are proven in a similar manner, by
choosing the identity mapping or permutation, respectively, to show reflexivity,
and composing mappings or permutations to show transitivity. For ∃∀X [L], the
subsumption relation extends the subsumption relations of QX [L] for Q ∈ {∃, ∀},
and reflexivity and transitivity can easily be lifted from them.
     Lastly, the fact that ⊥L ⊑L φ for any φ ∈ L easily follows from its definition,
using a similar inductive argument over the structure of bounded languages.

B.2    Correctness of Canonicalization
Proof (Thm. 2). The proof follows the mutually inductive definitions of the
canonicalization and the total order in Def. 3. To avoid confusion, we write c(·),
⊑, and ≤ to refer to the canonicalization and orders of the language for which
the claim is proven in the induction step (omitting the subscript).
   The fact that c is representative, i.e., that c(φ) ≡⊑ φ for all φ, is apparent in
almost all cases, since they simply canonicalize subformulas in ways which, given
the induction hypothesis, clearly result in subsumption-equivalent formulas. The
only interesting case is ∧ω [L], where
                       ^       ^
              c∧ω [L] ( φ̄) =     ⟨min ⊑L {cL (φ1 ), . . . , cL (φ|φ̄| )}⟩≤ ,
                                                                       L


since there might be fewer formulas in φ̄c = ⟨min ⊑L {cL (φ1 ), . . . , cL (φ|φ̄| )}⟩≤
                                                                                       L
than in φ̄, due to minimization, and the mappings from [φ̄] to [φ̄c ] and from
[φ̄c ] to [φ̄] necessary to show mutual subsumption are not obvious. However, due
to cL being representative and decisive (i.h.), any formula in φ̄ has a formula
subsuming it in φ̄c ; and any formula in φ̄c has a subsumption-equivalent formula
in φ̄. These facts precisely prove the existence of the required mappings.
      For the decisiveness of c, we need to show that φ ≡⊑ ψ ⇐⇒ c(φ) = c(ψ). We
begin with the “ ⇐= ” direction. This  V is again straightforward
                                                      V        V in all cases V    aside
from ∧ω [L]. V   For thisVcase, denote φ̄c = c∧ω [L] ( φ̄) and ψ̄c = c∧ω [L] ( ψ̄),
and assume φ̄c = ψ̄c . Every formula in φ̄ has a formula in φ̄c subsuming it,
which is therefore also in ψ̄c , and has a subsumption-equivalent
                                                      V      V        formula in ψ̄.
Thus, there is a mapping m : [φ̄] → [ψ̄] showing ψ̄ ⊑ φ̄, and the existence
of a mapping for the other direction is symmetrical.
      Next, we recognize that the “ =⇒ ” direction of decisiveness for c is implied
by its representativeness together with ⊑ being a partial order (i.e., an anti-
symmetric preorder) over canonical formulas, since then
             φ ≡⊑ ψ       =⇒      c(φ) ≡⊑ c(ψ)       =⇒      c(φ) = c(ψ).


                                           27
We have already dealt with c being representative, and ⊑ being a partial order is
implied by ≤ being a total order over canonical formulas that extends ⊑, which
we also need to prove. Therefore, it suffices to prove the last claim.
    The fact that ≤ is a total order can easily proven by observing that the induc-
tive definitions either lift total orders in pointwise manners (∨[·, ·], ∧[·, ·], ∃X [·],
∀X [·]), in lexicographic manners (∨k [·], ∧ω [·]), or by chaining them (∃∀X [·]).
Showing that ≤ extends ⊑ is more subtle. In the base case this holds by defini-
tion. For ◦[L1 , L2 ] where ◦ ∈ {∨, ∧}, given canonical φ1 ◦ φ2 ⊑ ψ1 ◦ ψ2 it holds
that φ1 ⊑L1 ψ1 and φ2 ⊑L2 ψ2 , and therefore (i.h.) φ1 ≤L1 ψ1 and φ2 ≤L2 ψ2 ,
which implies φ1 ◦ φ2 ≤ ψ1 ◦ ψW    2.    W
    For ∨k [L], given canonical φ̄ ⊑ ψ̄, there exists an injective m : [φ̄] → [ψ̄]
such that for all i ∈ [φ̄], φi ⊑L ψm(i) , and thus φi ≤L ψm(i) . Since φ̄ and ψ̄ are
canonical, they are ordered by ≤L . Consider the following cases:

  – There exists i ≥ 1 such that φ  W−i ̸= ψ
                                           W−i . Let this i be minimal. By definition
    of the total order for ∨k [L], φ̄ ≤ ψ̄ if φ−i <L ψ−i . Assume for the sake
    of contradiction that φ−i >L ψ−i (we already know they are not equal).
    Observe that every j ∈ {|φ̄|−i+1, . . . , |φ̄|} must have m(j) > |ψ̄|−i+1, since
    otherwise φj ≥L φ−i >L ψ−i ≥L ψm(j) , contradicting φj ⊑L ψm(j) . But this
    is a contradiction, since it means m is not injective. Thus, φ−i <L ψ−i .
  – Otherwise, φ̄ is a suffix of ψ̄. (φ̄ cannot be longer        ψ̄, since there is an
                                                          W than W
    injection from [φ̄] to [ψ̄].) This case also implies φ̄ ≤ ψ̄.
                                   V      V
    For ∧ω [L], given canonical φ̄ ⊑ ψ̄, there exists m : [ψ̄] → [φ̄] such that
for all i ∈ [ψ̄], φm(i) ⊑L ψi , and thus φm(i) ≤L ψi . Since φ̄ and ψ̄ are canonical,
they are antichains w.r.t ⊑L ordered by ≤L . Consider the following cases:

 – There exists i ≥ 1 such thatVφi ̸= ψ   Vi . Let this i be minimal. By definition
   of the total order for ∧ω [L], φ̄ ≤ ψ̄ if φi <L ψi . Assume for the sake of
   contradiction that φi >L ψi (we already know they are not equal). Observe
   that every j ∈ {1, ..., i} must have m(j) < i, since otherwise φm(j) ≥L φi >L
   ψi ≥L ψj , contradicting φm(j) ⊑L ψj . But this means that there are distinct
   1 ≤ j1 < j2 ≤ i with m(j1 ) = m(j2 ). Since j1 < i, we also know φj1 = ψj1 .
            V m(j1 ) = m(j2 ) = j1 , which means that ψj1 = φj1 = φm(j2 ) ⊑L
   Thus, either
   ψj2 and ψ̄ is not canonical;V     or m(j1 ) = m(j2 ) ̸= j1 , which
                                                                 V     means
                                                                         V     that
   φm(j1 ) ⊑L ψj1 = φj1 and φ̄ is not canonical. Therefore, φ̄ ≤ ψ̄.
 – Otherwise, ψ̄ is a prefix of φ̄. (φ̄ cannot be a strict prefix of ψ̄, since then
   there would be an element in φ̄, which is also in ψ̄, subsuming two W distinct
                                                                               W
   elements in ψ̄, making ψ̄ non-canonical.) This case also implies φ̄ ≤ ψ̄.

   For QX [L] where Q ∈ {∃, ∀}, given canonical QX.φ ⊑ QX.ψ, there exists
π ∈ SX such that φπ ⊑L ψ. Since QX.φ is QX [L]-canonical,

            φ = min ≤L {cL (φθ) | θ ∈ SX } ≤L cL (φπ) ≡⊑L φπ ⊑L ψ,

and since ψ is L-canonical, φ ≤L ψ and therefore QX.φ ≤ QX.ψ as well. The
case for ∃∀X [L] uses the two single-quantifier cases in a straightforward way.


                                           28
B.3    Correctness of Set Representation
Proof (Thm. 3). Let F ⊆ L and RF = min ⊑ {c(φ) | φ ∈ F } its represen-
tation. Using the definition of min ⊑ , and due to ⊑ being antisymmetric and
well-founded over canonical formulas, for all φ ∈ F there exists ψ ∈ RF such
that ψ ⊑ c(φ). Due to c being representative, c(φ) ≡⊑ φ.
    The above implies that for all φ ∈ F there exists ψ ∈ RF suchVthat ψ V ⊑ φ,
and thus ψ |= φ; from this is it easy to deduce that ↑RF ⊇ ↑F and RF |= F .
Next, by definition, any ψ ∈ RF has some φ ∈ F such V       that ψ V= c(φ), and
therefore ψ ≡⊑ φ and ψ ≡ φ. This impliesV    ↑F  ⊇
                                                 V ↑R F and   F |= RF .
    Taken together, we conclude that RF ≡ F and ↑RF = ↑F .

B.4    Correctness of Weaken
Proof (Thm. 4). In order to prove that the implementation in Thm. 4 satisfies
the specification in Def. 5, it suffices to show that for all φ ∈ L and s ∈ S,
(i) WL (φ, s) is an antichain w.r.t ⊑L of canonical formulas, (ii) all formulas in
WL (φ, s) are subsumed by φ and satisfied by s, and (iii) for all ψ ∈ L with
φ ⊑ ψ and s |= ψ, there exists ξ ∈ WL (φ, s) such that ξ ⊑ ψ.
    The above suffices for the proof since item (ii) shows that
                                                                      
           WL (φ, s) ⊆ ↑ min ⊑L {cL (ψ) | ψ ∈ L, φ ⊑ ψ, and s |= ψ} ,

item (iii) shows that

            ↑WL (φ, s) ⊇ min ⊑L {cL (ψ) | ψ ∈ L, φ ⊑ ψ, and s |= ψ} ,

and because item (i) tells us WL (φ, s) is an antichain of canonical formulas,

             WL (φ, s) = min ⊑L {cL (ψ) | ψ ∈ L, φ ⊑ ψ, and s |= ψ} .

     As usual, we shall prove (i)–(iii) by induction on the recursive implementa-
tion. These clearly hold for any case where s |= φ, where the implementation
always returns {φ}. We therefore restrict our discussion to cases where s ̸|= φ.
Claim (i) can be easily verified by going case by case and using claim (i) of the
induction hypothesis. Claim (ii) is likewise easy to prove using claim (ii) of the
induction hypothesis, together with the definition of subsumption (Def. 2), and
the fact that a disjunction is satisfied if one of its disjuncts is satisfied, a con-
junction is satsified if all of its conjuncts are satisfied, an existentially quantified
formula is satisfied if there exists a state updated with an assignment to quan-
tified variables which satisfies its body, and a universally quantified formula is
satisfied if all such updated states satisfy its body.
     Thus, it remains to inductively prove claim (iii), which we do case by case.
Keep in mind that we assume s ̸|= φ.
     For LA , if φ = ⊥, WLA (φ, s) contains all ψ ∈ LA with s |= ψ, so (iii) holds
due to reflexivity of ⊑. If φ ̸= ⊥, nothing satisfying s is subsumed by it.
     For ∨[L1 , L2 ], assume φ1 ∨ φ2 ⊑ ψ1 ∨ ψ2 and s |= ψ1 ∨ ψ2 . Either s |= ψ1 ,
in which case there exists ξ1 ∈ WL1 (φ1 , s) such that ξ1 ⊑L1 ψ1 (i.h.), and


                                          29
then ξ1 ∨ φ2 ⊑ ψ1 ∨ ψ2 and ξ1 ∨ φ2 ∈ W∨[L1 ,L2 ] (φ1 ∨ φ2 , s); or s |= ψ2 , in
which case there exists ξ2 ∈ WL2 (φ2 , s) such that ξ2 ⊑L2 ψ2 (i.h.), and then
φ1 ∨ ξ2 ⊑ ψ1 ∨ ψ2 and φ1 ∨ ξ2 ∈ W∨[L1 ,L2 ] (φ1 ∨ φ2 , s).
    For ∧[L1 , L2 ], assume φ1 ∧φ2 ⊑ ψ1 ∧ψ2 and s |= ψ1 ∧ψ2 . Then s |= ψ1 and s |=
ψ2 . So there exist ξ1 ∈ WL1 (φ1 , s) and ξ2 ∈ WL2 (φ2 , s) with ξ1 ⊑ ψ1 and ξ2 ⊑
ψ2 (i.h.) (meaning ξ1 ∧ W ξ2 ⊑ ψ1W ∧ ψ2 ) such that
                                                  Wξ1 ∧ ξ2 ∈ W∧[L1 ,L2 ] (φ1 ∧ φ2 , s).
    For ∨k [L], assume φ̄ ⊑ ψ̄ and s |= ψ̄. So there exists an injective
m : [φ̄] → [ψ̄] such that for all i ∈ [φ̄], φi ⊑ ψm(i) ; and there exists some j ∈ [ψ̄]
such that s |= ψj . Consider the following cases:

 – There exists i ∈ [φ̄] such that m(i) = j. Since φi ⊑ ψj and s |= ψj , there
   exists some ξ ∈ WL (φi , s) such that ξ ⊑ ψj (i.h.), and
                   _          _
                       ξ¯ =       ⟨φ1 , . . . , φi−1 , ξ, φi+1 , . . . , φ|φ̄| ⟩≤ ⊑ ψ̄,
                                                                               L


   and ξ¯ ∈ W∨k [L] ( φ̄, s), (specifically, ξ¯ ∈ W|φ̄| ; see Thm. 4).
        W             W                     W
 – Otherwise, m(i) ̸= j for all i ∈ [φ̄]. Therefore, φ̄ must be strictly shorter
   than ψ̄, and therefore |φ̄| < k. Note that this is only the case because we
   required m to be injective when defining the subsumption relation. This is
   crucial for weakening disjunctions in this way. Since ⊥L ⊑ ψj and s |= ψj ,
   there exists some ξ ∈ WL (⊥L , s) such that ξ ⊑ ψj (i.h.), and
                              _          _
                                  ξ¯ =       ⟨φ1 , . . . , φ|φ̄| , ξ⟩≤ ⊑ ψ̄,
                                                                   L


    and ξ¯ ∈ W∨k [L] ( φ̄, s), (specifically, ξ¯ ∈ W|φ̄|+1 ; see Thm. 4).
           W              W                     W

                          V        V             V
    For ∧ω [L], assume φ̄ ⊑ ψ̄ and s |= ψ̄. So there exists m : [ψ̄] → [φ̄]
such that for all i ∈ [ψ̄], φm(i) ⊑ ψi and s |= ψi . Therefore, for any i ∈ [ψ̄] there
exists ξi′ ∈ WL φm(i) , s such that ξi′ ⊑ φm(i) ⊑ ψi (i.h.); and if we denote

                  ξ¯ = ⟨min ⊑L WL (φ1 , s) ∪ · · · ∪ WL φ|φ̄| , s ⟩≤
                                                                 
                                                                                   L


                       ¯ such that ξj ⊑ ξ ′ . Thus, any i ∈ [ψ̄] has j ∈ [ξ]
then each ξi′ has jV∈ [ξ]                                                 ¯ such that
                                          i V
                     ¯    V                     ¯
ξj ⊑ ψi , proving ξ ⊑ ψ̄; and indeed, { ξ} = W∧ω [L] ( φ̄, s).
                                                               V
    For ∃X [L], assume ∃X.φ ⊑ ∃X.ψ and ((U, I), µ) |= ∃X.ψ. So there ex-
ists π ∈ SX such that φ ⊑ ψπ; and since ((U, I), µ) |= ∃X.ψπ as well, there
                                             ←−
exists ν : X → U such that      ((U, I), µ ∪ ν) |= ψπ. Thus, there exists some
                        ←
                        −
                            
ξ ∈ WL φ, ((U, I), µ ∪ ν) such that ξ ⊑ ψπ, and therefore ∃X.ξ ⊑ ∃X.ψ;
the rest of the proof follows due to canonicalization being representative.
    The case for ∀X [L], where we assume ∀X.φ ⊑ ∀X.ψ and s |= ∀X.ψ, is similar,
but instead of weakening φ according to any one assignment we weaken it via

     Ωφ0 ({s1 , . . . , sn }) = {φn | φ1 ∈ WL (φ0 , s1 ), . . . , φn ∈ WL (φn−1 , sn )}

where we set φ0 = φ and the states s1 , . . . , sn to be all updates of s with
assignments to X. The proof proceeds inductively and shows that for all i =


                                                 30
1, ..., n, there exist φ0 ∈ {φ}, φ1 ∈ WL (φ0 , s1 ), ..., φi ∈ WL (φi−1 , si ) subsuming
ψπ, where π ∈ SX is the permutation for which φ ⊑ ψπ. The induction step is
similar to the case for ∃X [L], and holds since ψ satisfies all updated states.
     The case for ∃∀X [L], where we assume QX.φ ⊑ Q′ X.ψ and s |= Q′ X.ψ,
follows from the weakening procedure for ∃X [L] when Q = Q′ = ∃, from the
weakening procedure for ∀X [L] when Q = Q′ = ∀, and handles the case Q =
∀, Q′ = ∃ by including the result of weakening ∃X.φ as well if Q = ∀.


C    The LSet[L] Data Structure

We introduce the LSet[L] data structure for storing sets of canonical L-formulas
(the sets are not necessarily antichains, see discussion below), and implementing
the ·|̸=|s and ·|⊑ψ filters.
      We explain the implementation of LSet[L] assuming standard data structures
for sets and maps. In each case we construct the data structure LSet[L] by
augmenting a standard set data structure, e.g., a hash-set, denoted S : Set[L],
with additional fields intended to facilitate the desired operations. Table 2 lists
the fields used in the LSet[L] data structure for each language constructor, the
invariants maintained, and the implementation of ·|̸=|s and ·|⊑ψ .
      For the base case, LSet[LA ] is implemented without any auxiliary fields, using
straightforward iteration over the elements of S for computing ·|̸=|s and ·|⊑ψ .
      For ∨[L1 , L2 ], the data structure has—in addition to S—two auxiliary data
fields: L : LSet[L1 ], which holds the set of first-position disjuncts present in
S, and a map M : Map[L1 , LSet[L2 ]], which maps each first-position disjunct
to the set of its corresponding second-position disjuncts (in our implementation
Map[·, ·] is a hash-map). That is, the data structure maintains the invariants that
a formula φ1 ∨ φ2 is in the set S iff φ2 ∈ M [φ1 ], and that L contains the same
formulas as the domain (the set of keys) of M , which we denote dom(M ). For
·|̸=|s , both disjuncts of a formula must not be satisfied by s; therefore, this filter
can be computed by using L|̸=|s to get all first-position disjuncts that are not
satisfied by s, and for each φ1 of them computing M [φ1 ]|̸=|s to get the relevant
second-position disjuncts. Similarly, to get all formulas subsuming ψ1 ∨ ψ2 , both
disjuncts need to be subsumed; therefore, L|⊑ψ1 is used to get all first-position
disjuncts that subsume ψ1 , and for each φ1 of them M [φ1 ]|⊑ψ2 is used to get
the relevant second-position disjuncts subsuming ψ2 . Note that L may not be
an antichain, even if S is. For example, if S = {φ1 ∨ φ2 , ψ1 ∨ ψ2 } with φ1 ⊑L1 ψ1
but φ2 ̸⊑L2 ψ2 , then S is an antichain but L (which holds {φ1 , ψ1 }) is not.
      The implementation for ∧[L1 , L2 ] is similar to the binary disjunction case
for ·|⊑ψ1 ∧ψ2 , since the subsumption relation is defined identically. However, ·|̸=|s
requires only one of the conjuncts to be unsatisfied by s. We therefore hold two
set-map pairs as above: L1 : LSet[L1 ], M1 : Map[L1 , LSet[L2 ]] and L2 : LSet[L2 ],
M2 : Map[L2 , LSet[L1 ]]. All first-position conjuncts that do not satisfy s can
be retrieved using L1 |̸=|s , and collecting for each such φ1 all φ1 ∧ φ2 where
φ2 ∈ M1 [φ1 ] results exactly in all formulas in the set where the first conjunct is
not satisfied by s. In a symmetrical manner we find all formulas in the set where


                                          31
                                         Table 2. The LSet[L] data structure.

              Fields:                                        Invariants:
              S : Set[LA ]                                   ⊤
LA




              Implementing |̸=|s :                           Implementing |⊑ψ :
              {φ ∈ S | s ̸|= φ}                              {⊥, ψ} ∩ S
              Fields:                                        Invariants:
              S : Set[∨[L1 , L2 ]]                           φ1 ∈ L ⇔ φ1 ∈ dom(M ) ⇔ ∃φ2 . φ1 ∨ φ2 ∈ S
∨[L1 , L2 ]




              L : LSet[L1 ]                                  φ2 ∈ M [φ1 ] ⇔ φ1 ∨ φ2 ∈ S
              M : Map[L1 , LSet[L2 ]]
              Implementing |̸=|s :                           Implementing |⊑ψ1 ∨ψ2 :
              {φ1 ∨ φ2 | φ1 ∈ L|̸=|s , φ2 ∈ M [φ1 ]|̸=|s }   {φ1 ∨ φ2 | φ1 ∈ L|⊑ψ1 , φ2 ∈ M [φ1 ]|⊑ψ2 }
              Fields:                                        Invariants:
              S : Set[∧[L1 , L2 ]]                           φ1 ∈ L1 ⇔ φ1 ∈ dom(M1 ) ⇔ ∃φ2 . φ1 ∧ φ2 ∈ S
              L1 : LSet[L1 ]                                 φ2 ∈ M1 [φ1 ] ⇔ φ1 ∧ φ2 ∈ S
              L2 : LSet[L2 ]
∧[L1 , L2 ]




                                                             φ2 ∈ L2 ⇔ φ2 ∈ dom(M2 ) ⇔ ∃φ1 . φ1 ∧ φ2 ∈ S
              M1 : Map[L1 , LSet[L2 ]]                       φ1 ∈ M2 [φ2 ] ⇔ φ1 ∧ φ2 ∈ S
              M2 : Map[L2 , LSet[L1 ]]
              Implementing |̸=|s :                           Implementing |⊑ψ1 ∧ψ2 :
              {φ1 ∧ φ2 | φ1 ∈ L1 |̸=|s , φ2 ∈ M1 [φ1 ]} ∪    {φ1 ∧ φ2 | φ1 ∈ L|⊑ψ1 , φ2 ∈ M [φ1 ]|⊑ψ2 }
              {φ1 ∧ φ2 | φ2 ∈ L2 |̸=|s , φ1 ∈ M2 [φ2 ]}
              Fields:                                        Invariants:
              S : Set[∨k [L]]                                collect(r) = {ϵ} ∪ {φ̄ | ∃ψ̄. ( (φ̄ + ψ̄)) ∈ S}
                                                                                            W
              r : TreeNode where TreeNode is                 (L, M ) : TreeNode ⇒ (φ ∈ L ⇔ φ ∈ dom(M ))
                  (LSet[L], Map[L, TreeNode])                (L, M ) : TreeNode ∧ (L′ , M ′ ) = M [φ] ∧ ψ ∈ L′ ⇒ φ ≤L ψ
∨k [L]




              Implementing      |̸=|s :                      Implementing      |⊑W ψ̄ :
              { φ̄ | φ̄ ∈ collect̸=| (r, s) and              { φ̄ | φ̄ ∈ collect⊑ (r, ψ̄) and
               W                                W             W                               W
                                                  φ̄ ∈ S}                                       φ̄ ∈ S}
              Recursive functions:
              collect((L, M )) = {ϵ} ∪ {⟨φ⟩ + φ̄ | φ ∈ L, φ̄ ∈ collect(M [φ])}
              collect̸=| ((L, M ), s) = {ϵ} ∪ {⟨φ⟩ + φ̄ | φ ∈ L|̸=|s , φ̄ ∈ collect̸=| (M [φ], s)}
                                                                                                                           |ψ̄|
              collect⊑ ((L, M ), ψ̄) = {ϵ} ∪ {⟨φ⟩ + φ̄ | i ∈ [ψ̄], φ ∈ L|⊑ψi , φ̄ ∈ collect⊑ (M [φ], ⟨ψj | j ̸= i ∧ ψj ≥ φ⟩j=1 )}
              Fields:                                        Invariants:
              S : Set[∧ω [L]]
                                                                                     V
                                                             ψ ∈ L ⇔ ∃φ̄, i ∈ [φ̄]. ( φ̄) ∈ S ∧ ψ = φi
∧ω [L]




              L : LSet[L]
              Implementing
               V               |̸=|s :                       Implementing
                                                              V               |⊑V ψ̄ :
              { φ̄ ∈ S | ∃i ∈ [φ̄]. φi ∈ L|̸=|s }            { φ̄ ∈ S | ∀i ∈ [ψ̄]. ∃j ∈ [φ̄]. φj ∈ L|⊑ψi }
              Fields:                                        Invariants:
              S : Set[∃X [L]]                                φ ∈ L ⇔ (∃X.φ) ∈ S
∃X [L]




              L : LSet[L]

                         T |̸=|((U ,I),µ) :
              Implementing                                   Implementing    |⊑∃X.ψ :
                                                               π∈SX {∃X.φ | φ ∈ L|⊑ψπ } where ψπ = cL (ψπ)
                                                             S
              {∃X.φ | φ ∈ ν:X→U L|̸=|((U ,I),µ←
                                              ∪ ν) }
                                              −

              Fields:                                        Invariants:
              S : Set[∀X [L]]                                φ ∈ L ⇔ (∀X.φ) ∈ S
∀X [L]




              L : LSet[L]

                         S |̸=|((U ,I),µ) :
              Implementing                                   Implementing    |⊑∀X.ψ :
                                                               π∈SX {∀X.φ | φ ∈ L|⊑ψπ } where ψπ = cL (ψπ)
                                                             S
              {∀X.φ | φ ∈ ν:X→U L|̸=|((U ,I),µ←
                                              ∪ν}
                                              −

              Fields:                                        Invariants:
              S : Set[∃∀X [L]]                               ∃X.φ ∈ L∃ ⇔ (∃X.φ) ∈ S
              L∃ : LSet[L] L∀ : LSet[L]                      ∀X.φ ∈ L∀ ⇔ (∀X.φ) ∈ S
∃∀X [L]




              Implementing |̸=|s :                           Implementing
                                                             (                |⊑QX.ψ :
              L∃ |̸=|s ∪ L∀ |̸=|s                              L∀ |⊑∀X.ψ ∪ L∃ |⊑∃X.ψ if Q = ∃
                                                               L∀ |⊑∀X.ψ               if Q = ∀




                                                                  32
the second conjunct is not satisfied by s. As mentioned above, the ·|⊑ψ1 ∧ψ2 filter
is implemented identically to the ∨[L1 , L2 ] case using L1 , M1 .
    The case of LSet[∨k [L]] generalizes the case of ∨[L1 , L2 ], in the sense that all
disjuncts need to be unsatisfied by s in ·|̸=|s ; and all disjuncts need to subsume
a (distinct) disjunct in ·|⊑W ψ̄ . Therefore, these operations are implemented by
computing them for all disjuncts iteratively. We use a tree structure whose edges
are labeled with L-formulas, and whose paths W     are understood as the sequences
of disjuncts as they appear in formulas φ̄ ∈ S. Since we consider canonical
formulas, we are ensured that disjuncts are ordered according to ≤L along paths
in the tree. Each node in the tree has an LSet[L] that stores the L-formulas
labeling its outgoing edges, which represent the next possible disjuncts in the
sequence of L-formulas from the root to the node. This generalizes the L field
in the binary case, which maintains the possible first-position disjuncts, i.e., the
next disjuncts w.r.t the empty sequence. Using this construction, ·|̸=|s and ·|⊑W ψ̄
are implemented by tree traversals, with recursive applications of L|̸=|s and L|⊑ψi
for the sets L : LSet[L] in the nodes, which are used to retrieve the next possible
disjuncts
   W      not satified by s, or the next possible disjuncts subsuming some disjunct
in ψ̄, respectively. In the case of ·|⊑W ψ̄ , since each resulting disjunct needs to
subsume a distinct formula in ψ̄, we remove ψi from ψ̄ during the recursive
traversal if it caused us to go down that edge. As an optimization, when going
down an edge labeled φ, we also remove from ψ̄ all formulas ψi <L φ, since such
formulas cannot be subsumed by formulas greater or equal to φ.
      The case of LSet[∧ω [L]] is simpler. In addition to the standard S : Set[∧ω [L]],
we maintain a V   field L : LSet[L] aggregating all conjuncts from all formulas in S.
The formulas φ̄ whichVare not satisfied      V by s are those with some conjunct in
L|̸=|s ; and the formulas
                   V          φ̄ subsuming     ψ̄ are those where for all i ∈ [ψ̄] there
is a conjunct of φ̄ in L|⊑ψi . These checks are implemented in a straightforward
way. An alternative approach is to store conjunctions in a tree structure similar
to the LSet implementation for ∨k [L], and perform ·|̸=|s and ·|⊑V ψ̄ using appro-
priate traversals of the tree (analoguously to the way UBTrees [11] are used for
finding both subsets and super sets). However, observe that the savings in the
∧ω [L] case would be much more modest. For example, the implementation of
·|̸=|s for ∨k [L] uses a recursive traversal of the tree that prunes away subtrees if
the formula leading to them is satisfied by s (since any disjunction containing
that formula is satisfied by s). For ∧k [L], discarding these paths is not possible,
since it suffices for some conjunct to be violated by s for the entire conjunction
to be unsatisfied by it. Thus, ·|̸=|s would require recursively traversing the entire
tree, and our experience is that the overhead of maintaining the tree structure
makes this approach inefficient overall. We note, however, that the implementa-
tion of LSet for unbounded conjunction is the least optimized component of our
approach, and might be improved further in future work.
   The cases of QX [L] for Q ∈ {∃, ∀} are each implemented using an LSet L
over L to store the bodies of formulas, which is used to perform ·|̸=|s and ·|⊑QX.ψ
by iterating over all assignments to the variables, or over all permutations of


                                          33
variables, respectively, and using the corresponding operations for LSet[L]. The
case of ∃∀X [L] then uses these two data structures in a straightforward way.
     Table 2 explained above relies heavily on maps that use formulas as keys.
However, computing hashes of formulas can be expensive, and therefore an ef-
ficient implementation of LSet[L] requires an additional optimization. Rather
than using formulas as keys, in our implementation each LSet[L] maintains a
bidirectional mapping between formulas and integer IDs, and uses the IDs when-
ever possible, converting back to formulas only when producing the externally-
facing output. For example, the filters applied to L in the implementation of
LSet[∨[L1 , L2 ]] return a set of IDs that are then used as keys for M , avoid-
ing unnecessary hash computations. (Other approaches, such as memoization of
hashes or hash consing, can alternatively be used.)


D     Language Optimizations
 [29] uses several techniques for reducing the size of first-order languages without
losing precision. [29, Lemma 6], for example, implies the equivalence
           Q̄x̄. φ(x̄∀ , x̄∃ ) ∨ (ψ1 (x̄∀ , x̄∃ ) ∧ ψ2 (x̄∀ ))
               h                                    i h                              i
            ≡ Q̄x̄. φ(x̄∀ , x̄∃ ) ∨ ψ1 (x̄∀ , x̄∃ ) ∧ Q̄x̄. φ(x̄∀ , x̄∃ ) ∨ ψ2 (x̄∀ ) .

where Q̄x̄ is some quantifier prefix, x̄∀ are the universally quantified variables in
x̄ and x̄∃ are the the existentially quantified variables in x̄. This allows [29] to sig-
nificantly reduce the number of formulas considered, since any formula that can
be equivalently decomposed in this way is semantically redundant throughout
the search for an inductive invariant.
    However, as we have confirmed with the authors of [29], the proof of [29,
Lemma 6] contains an over-generalization, and the lemma in its general form
does not hold. For example, consider the formula
                              ∃x.∀y. (x ̸= y) ∨ (p(y) ∧ q(x))
and the structure (U, I) where U = {a, b} and I(p) = {a}, I(q) = {b}. It is easy
to verify that (U, I) ̸|= ∃x.∀y. (x ̸= y) ∨ (p(y) ∧ q(x)), but
     (U, I) |= ∃x.∀y. (x ̸= y) ∨ p(y) and (U, I) |= ∃x.∀y. (x ̸= y) ∨ q(x).
The problem with [29, Lemma 6] is that it might not work when some of the
universally quantified variables are quantified after existentially quantified ones.
Nonetheless, the reduction afforded by this kind of observation is significant, so
it is desirable to amend it, which we do as follows.
Lemma 1. For any quantification sequence ∀x̄ Q̄ȳ and formulas φ(x̄, ȳ), ψ1 (x̄, ȳ),
and ψ2 (x̄), the following semantic equivalence holds
           ∀x̄.Q̄ȳ. φ(x̄, ȳ) ∨ (ψ1 (x̄, ȳ) ∧ ψ2 (x̄))
               h                                i h                           i
           ≡ ∀x̄.Q̄ȳ. φ(x̄, ȳ) ∨ ψ1 (x̄, ȳ) ∧ ∀x̄.Q̄ȳ. φ(x̄, ȳ) ∨ ψ2 (x̄) .


                                               34
    Before providing a proof for this lemma, we demonstrate how it allows us
to reduce the languages we are dealing with without losing expressive power. In
Sec. 6.2 we choose k-pDNF as our quantifier-free language, specified as

                                    ∨[∨n [·], ∨k−1 [∧ω [·]]].

This permits us to select different base languages of first-order literals for the
k-pDNF clause (∨n [·]) and for the k-pDNF cubes (∨k−1 [∧ω [·]]). Lemma 1 shows
that for a bounded language with a quantifier structure starting with ∀x̄, includ-
ing literals containing only variables from x̄ in the cubes does not add to the
expressive power of k-pDNF—since the decomposition described in Lemma 1
is able to substitute them with a conjunction of k-pDNF formulas where cubes
contain no such literals. Note, however, that this decomposition may replace one
k-pDNF formula with k-pDNF formulas that have extra literals in their k-pDNF
clause, so this restriction may be a tradeoff between the parameter n and the size
of the base language for the cubes. However, we find that in practice, using this
restriction captures the languages necessary to prove safety much more precisely.
    The proof for Lemma 1 is presented below.

Proof (Lemma 1). We prove an equivalent second-order formulation of the claim,
where existentially quantified variables in ȳ are replaced by existential quantifi-
cation over fresh function variables f¯, similarly to the process of Skolemization:

 ∃f¯.∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ1 (x̄, f¯(x̄, z̄)) ∧ ψ2 (x̄)
                                                               
     h                                                  i h                                       i
 ≡ ∃f¯.∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ1 (x̄, f¯(x̄, z̄)) ∧ ∃f¯.∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ2 (x̄) .

Specifically, z̄ consists of the universally quantified variables in ȳ, and for all
i ∈ [f¯], fi (v̄) replaces the i-th existentially quantified variable in ȳ, where v̄
are all the universally quantified variables in x̄, z̄ preceding that existentially
quantified variable in the quantifier prefix. To simplify the notation we denote
these function applications by f¯(x̄, z̄), even though each of them may only depend
on some of the variables in z̄ (but note that all of them are dependent on x̄).
   Using distributivity, the left-hand side of the above is equivalent to
         h                                               i h                                    i
    ∃f¯. ∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ1 (x̄, f¯(x̄, z̄)) ∧ ∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ2 (x̄) ,

which entails the right-hand side of the claim, since if there exists an assign-
ment to f¯ satisfying both conjuncts, for each of the conjuncts there exists an
assignment satisfying it.
    It is left to show entailment in the other direction. Let σ = (U, I) be a
structure and µ1 , µ2 two assignments to f¯ such that
                           h                                                i
                (σ, µ1 ) |= ∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ1 (x̄, f¯(x̄, z̄)) , and
                           h                                     i
                (σ, µ2 ) |= ∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ2 (x̄) .


                                                35
Define the assignment µ to f¯ which for all ā ∈ U |x̄| and b̄ ∈ U |z̄| satisfies
                               (
                                µ1 (f¯)(ā, b̄) if (σ, [x̄ 7→ ā]) |= ψ2 (x̄),
               µ(f¯)(ā, b̄) =
                                µ2 (f¯)(ā, b̄) otherwise.
Note that this is only possible because, as we have explained, all function ap-
plications in f¯(x̄, z̄) are dependent on x̄. If that were not the case, whether
(σ, [x̄ 7→ ā]) |= ψ2 (x̄) could not be used to determine µ(f¯)(ā, b̄) in this way. Sim-
ilarly, we cannot condition the value of µ(f¯)(ā, b̄) on b̄ (other than in the way
f¯(x̄, z̄) depends on z̄), since functions may partially depend on it. In part, this
is why this lemma cannot be generalized to [29, Lemma 6].
     The assignment µ shows that σ satisfies the left-hand of the equivalence, i.e.,
                         h                                      i h                           i
      (σ, µ) |= ∀x̄, z̄. φ(x̄, f¯(x̄, z̄)) ∨ ψ1 (x̄, f¯(x̄, z̄)) ∧ φ(x̄, f¯(x̄, z̄)) ∨ ψ2 (x̄) ,

because for all ā ∈ U |x̄| and b̄ ∈ U |z̄| , if (σ, µ[x̄ 7→ ā, z̄ 7→ b̄]) |= ψ2 (x̄) then the
right-hand conjunct is satisfied, and the left-hand conjunct is satisfied because
                                 µ(f¯)(ā, b̄) = µ1 (f¯)(ā, b̄).
Otherwise, (σ, µ[x̄ 7→ ā, z̄ 7→ b̄]) ̸|= ψ2 (x̄), which together with
                                  µ(f¯)(ā, b̄) = µ2 (f¯)(ā, b̄)
implies (σ, µ[x̄, 7→ ā, z̄ 7→ b̄]) |= φ(x̄, f¯(x̄, z̄)), so both conjuncts are satisfied.
   Thus, entailment holds in both directions, and the equivalence is established.

E     Least Fixpoint Computation via Symbolic Abstraction
Alg. 2 presents our implementation of the symbolic abstraction algorithm [26,28]
for computing the least fixpoint of the best abstract transformer of a transition
system (ι, τ ) in the abstract domain P(L) ordered by ⊇.

Background and Notation. The transition relation τ of a transition system over
signature Σ is a formula over signature Σ ∪ Σ ′ , where Σ ′ is the primed copy of
Σ (in which each symbol is replaced with a fresh primed duplicate). The set of
transitions consists of the pairs of states (structures over Σ) that jointly satisfy
τ . More precisely, given (U, I), (U ′ , I ′ ) ∈ structs[Σ] with U = U ′ , we denote by
⟨(U, I), (U ′ , I ′ )⟩ ∈ structs[Σ ∪ Σ ′ ] the structure with the same universe U = U ′ ,
where I determines the interpretation of symbols from Σ and I ′ determines the
interpretation of symbols from Σ ′ . The set of transitions consists of ⟨s, s′ ⟩ such
that ⟨s, s′ ⟩ |= τ . The semantics of the transition system (ι, τ ) is described by a
(concrete) transformer T : P(S) → P(S) defined by
                    T (S) = {s′ ∈ S | s′ |= ι ∨ ∃s ∈ S. ⟨s, s′ ⟩ |= τ }.
The least fixpoint of T , denoted lfpT , is the set of reachable states of (ι, τ ).
The abstract domain P(L) induces an abstract transformer T ♯ : P(L) → P(L)
defined by T ♯ = α ◦ T ◦ γ, which over-approximates the semantics of (ι, τ ) in the
sense that lfpT ⊆ γ(lfpT ♯ ).


                                               36
 Algorithm 2: Least Fixpoint Computation of T ♯
     Input: Transition system (ι, τ ), bounded first-order language L
     Output: R such that ↑R = lfpT ♯ where T ♯ is the best abstract transformer
              for (ι, τ ) in the abstract domain P(L)
 1 R : LSet[L] := {⊥L }; V
   while ∃s′ . s′ |= ι ∧ ¬( R) or ∃s, s′ . ⟨s, s′ ⟩ |= R ∧ τ ∧ ¬( R)′ do
                                                      V          V
 2
                                          ♯
       /* loop invariant: ↑R ⊇ lfpT                                           */
 3     weaken(R, s′ ) ;                                   // according to Alg. 1
 4 return R;




  Given (ι, τ ) and L, Alg. 2 computes the representation of lfpT ♯ . To do so, it
stores and updates a set R, which is the representation of the corresponding
abstract element computed by symbolic abstraction. Alg. 2 initializes the set R
to the representation of L (the least element in the abstract domain P(L)), which
is {⊥L }. Note that ↑R = L. In each iteration, a CTI s′ is found and R is updated
to a representation of ↑R ⊔ α({s′ }) by applying weaken (Alg. 1). The algorithm
therefore maintains the invariant that in each iteration, R is the representation
of α(S), where S is the set of CTIs obtained so far, i.e., ↑R = α(S).
                                             s′ such Vthat either s′ |=
                                                                              V
    A CTI is computed by finding a state                                ι ∧ ¬( R),
or there exists s such that ⟨s, s′ ⟩ |= R ∧ τ ∧V¬( R)′ , where ( R)′ denotes
                                        V                             V
the formula over signature Σ ′ obtained from ( R) by replacing every symbol
from Σ with its primed copy. Recall that a CTI V shouldV in fact be found for the
abstract element represented by R, but since R ≡ ↑R, it suffices to compute
a CTI based on the representation R.


F     Optimizing the Search for CTIs

The symbolic abstraction algorithm described in App. E and used in Sec. 6
requires performing SMT queries in order to check the inductiveness of a set of
formulas R. Since solvers often struggle when given even tens of formulas (with
quantifier alternations, but still in EPR), we employ
                                                    V several optimizations. First,
instead of directly checking the inductiveness of VR, we can separately check
that each formula φ ∈ R is relatively inductive w.r.t R. Second, before checking
the relative inductiveness of a formula, we check if it is implied by formulas
that were already proven relatively inductive (implication queries are in general
cheaper than inductiveness queries since they involve only a single copy of the
signature). The above can also be parallelized across formulas. Third, we use
incremental SMT queries, as described in [14]. Lastly, in parallel to the SMT
queries, we attempt to find CTIs via simulations from previous CTIs.




                                         37
