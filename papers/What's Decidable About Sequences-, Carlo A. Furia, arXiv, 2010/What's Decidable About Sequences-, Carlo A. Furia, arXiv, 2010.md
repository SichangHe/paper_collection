                                        What’s Decidable About Sequences?
                                                                    Carlo A. Furia
                                                                    January 2010
arXiv:1001.2100v2 [cs.LO] 10 Feb 2011




                                                                        Abstract
                                             We present a first-order theory of sequences with integer elements,
                                         Presburger arithmetic, and regular constraints, which can model signif-
                                         icant properties of data structures such as arrays and lists. We give a
                                         decision procedure for the quantifier-free fragment, based on an encoding
                                         into the first-order theory of concatenation; the procedure has PSPACE
                                         complexity. The quantifier-free fragment of the theory of sequences can
                                         express properties such as sortedness and injectivity, as well as Boolean
                                         combinations of periodic and arithmetic facts relating the elements of
                                         the sequence and their positions (e.g., “for all even i’s, the element at
                                         position i has value i + 3 or 2i”). The resulting expressive power is or-
                                         thogonal to that of the most expressive decidable logics for arrays. Some
                                         examples demonstrate that the fragment is also suitable to reason about
                                         sequence-manipulating programs within the standard framework of ax-
                                         iomatic semantics.




                                                                            1
Contents
1 Introduction                                                                3

2 The Theory of Concatenation                                                 4
  2.1 Sequences and Concatenation . . . . . . . . . . . . . . . . . . . .     4
  2.2 Decidability in the Theory of Concatenation . . . . . . . . . . . .     5
      2.2.1 Syntax and Semantics . . . . . . . . . . . . . . . . . . . .      5
      2.2.2 (Un)Decidable Fragments . . . . . . . . . . . . . . . . . .       5

3 A Theory of Sequences                                                       7
  3.1 A Theory of Integer Sequences . . . . . . . . . . . . . . . . . . .     7
      3.1.1 Syntax and Semantics . . . . . . . . . . . . . . . . . . . .      7
      3.1.2 Examples . . . . . . . . . . . . . . . . . . . . . . . . . . .    9
  3.2 Deciding Properties of Integer Sequences . . . . . . . . . . . . . .   10
      3.2.1 Dseq(Z) : A Decision Procedure for Tseq(Z) . . . . . . . . . .   10
      3.2.2 Correctness and Complexity . . . . . . . . . . . . . . . . .     12
  3.3 Undecidable Extensions . . . . . . . . . . . . . . . . . . . . . . .   13

4 Verifying Sequence-Manipulating Programs                                   14

5 Related Work                                                               16

6 Future Work                                                                18




                                      2
1    Introduction
Verification is undecidable already for simple programs, but modern program-
ming languages support a variety of sophisticated features that make it all the
more complicated. These advanced features — such as arrays, pointers, dynamic
allocation of resources, and object-oriented abstract data types — are needed
because they raise the level of abstraction thus making programmers more pro-
ductive and programs less buggy. Verification techniques have also progressed
rapidly over the years, in an attempt to keep the pace with the development of
programming languages.
    Automated verification requires expressive program logics and powerful de-
cision procedures. In response to the evolution of modern programming lan-
guages, new decidable program logic fragments and combination techniques for
different fragments have mushroomed especially in recent years. Many of the
most successful contributions have focused on verifying relatively restricted as-
pects of a program’s behavior, for example by decoupling pointer structure and
functional properties in the formal analysis of a dynamic data structure. This
narrowing choice, partly deliberate and partly required by the formidable dif-
ficulty of the various problems, is effective because different aspects are often
sufficiently decoupled so that each of them can be analyzed in isolation with the
most appropriate, specific technique.
    This paper contributes to the growing repertory of special program logics by
exploring the decidability of properties of sequences of elements of homogeneous
type. These can abstract fundamental features of several data structures: arrays
imprimis, but also the sequence of values stored in a dynamically allocated list,
or the content of a stack or a queue.
    We take a new angle on reasoning about sequences, based on the theory of
concatenation: a first-order theory where variables are interpreted as words (or
sequences) over a finite alphabet and can be composed by concatenating them.
Makanin’s algorithm for solving word equations [32] implies the decidability of
the quantifier-free fragment of the theory of concatenation. Based on this, we
introduce a first-order theory of sequences Tseq(Z) whose elements are integers.
Section 3.2 presents a decision procedure for the quantifier-free fragment of
Tseq(Z) , which encodes the validity problem into the quantifier-free theory of
concatenation. The decision procedure is in PSPACE; it is known, however,
that Makanin’s algorithm is reasonably efficient in practice [1].
    The theory of sequences Tseq(Z) allows concatenating sequences to build new
ones, and it includes Presburger arithmetic over elements of a sequence. On the
other hand, it forbids explicit indexed access to elements, which differentiates it
from the theory of arrays and extensions thereof (see Section 5). The resulting
quantifier-free fragment has significant expressiveness, in spite of its limitations
in representing subsequences of variable length. In particular, we show some
interesting properties that are inexpressible in powerful decidable array logics
(such as those in [8, 16, 22, 21]) but are expressible in our theory of sequences.
Conversely, there exist decidable properties of extensions of the theory of arrays
that are inexpressible in Tseq(Z) . These results support our claim that the theory
of sequences provides a fresh angle on reasoning about sequences, orthogonal to
most approaches that model sequences as arrays.
    In order to better assess the limits of our theory of sequences, we also prove
that several natural extensions of the quantifier-free fragment of Tseq(Z) are


                                         3
undecidable. Finally, we demonstrate reasoning about sequence-manipulating
programs with annotations written in the quantifier-free fragment of Tseq(Z) . A
couple of examples in Section 4 illustrate the usage of Tseq(Z) formulas with the
standard machinery of axiomatic semantics and backward reasoning.

Paper outline. Section 2 presents the theory of concatenation and summa-
rizes a few decidability and undecidability results about it. Section 3 introduces
our theory of integer sequences Tseq(Z) , demonstrates its expressiveness, provides
a decision procedure for its quantifier-free fragment, and shows undecidable ex-
tensions of the theory. Section 4 illustrates how to use the theory Tseq(Z) to
reason about programs in the standard axiomatic semantics framework. Finally,
Section 5 reviews related work and Section 6 concludes by outlining future work.


2     The Theory of Concatenation
This section introduces some basic notation (Section 2.1) and summarizes some
results about the first-order theory of concatenation (Section 2.2) that we will
use in the remainder of the paper.
    In the rest of the paper, we assume familiarity with the standard syntax
and terminology of first-order theories (e.g., [7]); in particular, we assume the
standard abbreviations and symbols of first-order theories with the following
operator precedence ¬, ∧, ∨, ⇒, ⇔, ∀ and ∃.
    F V (φ) denotes the set of free variables of a formula φ. With standard
terminology, a formula φ is a sentence iff it is closed iff F V (φ) = ∅. Given a
regular expression Q over {∃, ∀}, the Q-fragment of a first-order theory is the set
of all formulas of the theory in the form Q • ψ, where ψ is quantifier-free. The
universal and existential fragments are synonyms for the ∀∗ - and ∃∗ -fragment
respectively. A fragment is decidable iff the validity problem is decidable for
its sentences. It is customary to define the validity and satisfiability problems
for a quantifier-free formula ψ as follows: ψ is valid iff the universal closure
of ψ is valid, and ψ is satisfiable iff the existential closure of ψ is valid. As
a consequence of this definition, the decidability of a quantifier-free fragment
whose formulas are closed under negation is tantamount to the decidability of
the universal or existential fragments. Correspondingly, in the paper we will
allow some freedom in picking the terminology that is most appropriate to the
context.

2.1    Sequences and Concatenation
Z denotes the set of integer numbers and N denotes the set of nonnegative
integers.
    Given a set A = {a, b, c, . . .} of constants, a sequence over A is any word
v = v(1)v(2) · · · v(n) for some n ∈ N where v(i) ∈ A for all 1 ≤ i ≤ n. The
symbol  denotes the empty sequence, for which n = 0. |v| = n denotes the
length of v. A∗ denotes the set of all finite sequences over A including  6∈ A.
It is also convenient to introduce the shorthand v(k1 , k2 ) with k1 , k2 ∈ Z to




                                        4
describe subsequences of a given sequence v; it is defined as follows.
                       
                       
                       v(k1 )v(k1 + 1) · · · v(k2 ) 1 ≤ k1 ≤ k2 ≤ |v|
                       
                       v(k , |v| + k )
                           1           2             k1 − |v| ≤ k2 < 1 ≤ k1
         v(k1 , k2 ) ,
                       
                       
                       v(|v| + k 1 , |v| + k2 )     1 − |v| ≤ k1 ≤ k2 < 1
                                                    otherwise
                       

For two sequences v1 , v2 ∈ A∗ , v1 ? v2 denotes their concatenation: the sequence
v1 (1) · · · v1 (|v1 |)v2 (1) · · · v2 (|v2 |). We will drop the concatenation symbol when-
ever unambiguous.
    The structure hA∗ , ?, i is also referred to as the free monoid with generators
in A and neutral element . The size |A| is called rank of the free monoid and
it can be finite or infinite.

2.2     Decidability in the Theory of Concatenation
2.2.1    Syntax and Semantics
The theory of concatenation is the first-order theory Tcat with signature
                                                  .
                                 Σcat    ,       {=, ◦, R}
         .
where = is the equality predicate,1 ◦ is the binary concatenation function and
R , {R1 , R2 , . . .} is a set of unary (monadic) predicate symbols called regularity
                                                                        .
constraints. We sometimes write Ri (x) as x ∈ Ri and α =               6 β abbreviates
      .
¬(α = β).
    An interpretation of a formula in the theory of concatenation is a structure
hA∗ , ?, , R, evi where hA∗ , ?, i is a free monoid, R = {R1 , R2 , . . .} is a collection
of regular subsets of A∗ , and ev is a mapping from variables to values in A∗ .
The satisfaction relation hA∗ , ?, , R, evi |= φ for formulas in Tcat is defined in a
standard fashion with the following assumptions.
    • any variable x takes the value ev(x) ∈ A∗ ;
    • the concatenation x ◦ y of two variables x, y takes the value ev(x) ? ev(y);
    • for each Ri ∈ R, the corresponding Ri ∈ R defines the set of sequences
      x ∈ Ri for which Ri (x) holds (this also subsumes the usage of constants).

2.2.2    (Un)Decidable Fragments
The following propositions summarize some decidability results about fragments
of the theory of concatenation; they all are known results, or corollaries of them.
The standard presentation of these results focuses on solving equations over
sequences with free variables and, correspondingly, on existential fragments of
the equational theory. On the contrary, in this paper we will mostly focus on
the universal fragment, given its aptness for annotating sequence-manipulating
programs (see Section 4). It is straightforward, however, to rephrase the results
in terms of the dual existential fragments, given the availability of negation in
the language.
                       .
   1 We use the symbol = to distinguish it from the standard arithmetic equality symbol =
used later in the paper.


                                             5
Proposition 1 (Decidability [32, 13, 38]). The universal and existential frag-
ments of the theory of concatenation over free monoids with finite rank are
decidable in PSPACE.

Proof. Decidability is a consequence of Makanin’s seminal result on word equa-
tions [32] and its extensions to the full existential (and universal) fragments
[10, 13]. PSPACE complexity is a consequence of Plandowski’s recent results
[38, 39] and the fact that transforming first-order formulas into a single word
equation introduces only a polynomial blow-up.
    The only catch is that the standard presentation assumes formulas in the
canonical form ∀x1 ∈ R1 , x2 ∈ R2 , . . . , xv ∈ Rv • ρ where regularity constraints
do not appear in ρ. This is, however, without loss of generality as we can put
any universal formula ∀x • ψ in canonical form: first rewrite ψ into
                          ^          .            . −
                               (xi = h+    j ∨ xi = hj ) ⇒ ψ
                        1≤i≤|x|
                        1≤j≤|R|

                         −
for fresh h+                    ∗
           j ∈ Rj and hj ∈ A \ Rj . Then, put ψ in negated normal form
and eliminate occurrences of regularity predicates by applying exhaustively the
rules:
                         ψ[Rm (xn )]      ψ[¬Rm (xn )]
                               . +              .
                        ψ[xn = hm ]       ψ[xn = h− m]

It is not difficult to see that this transformation preserves satisfiability and
introduces a blow-up which is quadratic at most.
Proposition 2 (Undecidability).      • [14] The ∀∗ ∃∗ and ∃∗ ∀∗ fragments of
    the theory of concatenation are undecidable; in particular the ∀∃3 -fragment
    is undecidable already for negation-free formulas.

   • [11] The existential and universal fragments of the extension of the the-
     ory of concatenation over the free monoid {a, b}∗ with: (1) two length
     functions |x|a , {y ∈ a∗ | y has the same number of a’s as x} and |x|b ,
     {y ∈ b∗ | y has the same number of b’s as x}; or (2) the function Sp(x) ,
     |x|a ? |x|b are undecidable.

    A set of sequences S ⊆ A∗ is universally (resp. existentially) definable
from concatenation iff there is a universal (resp. existential) formula ϕ[x] with
F V (ϕ[x]) = {x} such that S = {y ∈ A∗ | ϕ[y]}.
Proposition 3 (Definability [11]).     • The set S = , {an bn | n ∈ N} is nei-
    ther universally nor existentially definable from concatenation.

   • The equal length predicate Elg(x, y) , |x| = |y| is not definable in the
     existential and universal fragments of concatenation.
Proof. Büchi and Senger prove in [11, Corollary 3] that S = is not existentially
definable. A very similar argument shows that S < , {am bn | 0 ≤ m < n}
is also not existentially definable (using the terminology of [11, Corollary 3],
the spacers of ai−1 bi relative to the atom a are ha, abi i and there are only
i − 1 words in S < with these spacers). The existential non-definability of S <
entails the existential non-definability of the set S 6= , {an bm | 0 ≤ n 6= m}


                                         6
by contradiction as follows. Assume that S 6= were existentially definable; then
x ∈ S < could be defined as x ∈ S 6= ∧∃u, v, p(u ∈ a∗ ∧v ∈ b∗ ∧p ∈ a+ ∧upv 6∈ S 6= )
(that is, |u|+|p| = |v|), a contradiction. Finally, S = is universally definable from
concatenation iff S 6= is existentially definable from concatenation. In fact, the
complement set {a, b} \ S = is S ∼ ∪ S 6= with S ∼ , {a, b}∗ b{a, b}∗ a{a, b}∗ clearly
existentially and universally definable from concatenation. This concludes the
proof of the first part of the proposition.
    The second part is proved in [11, Theorem 1] for the existential fragment
and it is straightforward to adapt that proof to universal definability.
    It is currently unknown whether the extension of the existential or universal
fragment of concatenation with Elg is decidable, while allowing membership
constraints over deterministic context-free language gives an undecidable theory
[13].


3       A Theory of Sequences
This section introduces a first-order theory of sequences (Section 3.1) with arith-
metic, gives a decision procedure for its universal fragment (Section 3.2), and
shows that “natural” larger fragments are undecidable (Section 3.3).

3.1      A Theory of Integer Sequences
We present an arithmetic theory of sequences whose elements are integers. It
would be possible to make the theory parametric with respect to the element
type. Focusing on integers, however, makes the presentation clearer and more
concrete, with minimal loss of generality as one can introduce any theory defin-
able in the integer arithmetic fragment.

3.1.1     Syntax and Semantics
Syntax. Properties of integers are expressed in Presburger arithmetic whose
signature is:
                       ΣZ , {0, 1, +, −, =, <}
Then, our theory Tseq(Z) of sequences with integer values has signature

                                     , Σcat ∪ ΣZ
                               Σseq(Z)
                                     .
Operator precedence is: ◦; + and −; =, = and < followed by logic connectives
and quantifiers with the previously defined precedence.
   We will generally consider formulas in prenex normal form
                                         Q • ψ
where Q is a quantifier prefix and ψ is quantifier-free written in the grammar:
         seq    ::=    var | int | seq ◦ seq
          int   ::=    0 | 1 | seq | int + int | int − int
                            .
        f mla   ::=    seq = seq | R(seq) | int = int | int < int
                      | ¬f mla | f mla ∨ f mla | f mla ∧ f mla | f mla ⇒ f mla
with var ranging over variable names.


                                           7
Semantics. An interpretation of a sentence of Tseq(Z) is a structure hZ∗ , ?, , R,
evi with the following assumptions.2

   • hZ∗ , ?, , R, evi have the same meaning as in the theory of concatenation.
   • As far as arithmetic is concerned:
        – The interpretation of a sequence v1 v2 · · · ∈ Z∗ of integers is the first
          integer in the sequence v1 , with the convention that the interpretation
          of the empty sequence is 0.
        – Conversely, the interpretation of an integer value v ∈ Z is the single-
          ton sequence v.
        – Addition, subtraction, equality, and less than are interpreted accord-
          ingly.

The satisfaction relation is then defined in a standard fashion.

Shorthands. We introduce several shorthands to simplify the writing of com-
plex formulas.
   • A symbol for every constant k ∈ Z, defined as obvious.
   • α 6= β, α ≤ β, α ≥ β, and α > β defined respectively as ¬(α = β),
     α < β ∨ α = β, ¬(α < β), and α ≥ β ∧ α 6= β.

   • Shorthands such as α ≤ β < γ or β ∈ [α, γ) for α ≤ β ∧ β < γ.
   • Bounded length predicates such as |x| < k for a variable x and a constant
     k ∈ ZSabbreviating R b <k (x) with R
                                        b <k a regular constraint interpreted as
                     i
     {} ∪ 0<i<k Z . The definition of derived expressions such as k1 ≤ |x| <
     k2 is also as obvious.
   • Subsequence functions such as x(k1 , k2 ) for a variable x and two constants
     k1 , k2 ∈ Z with the intended semantics (see Section 2.1). We define these
     functions in the theory Tseq(Z) by the following rewriting rules, defined on
     formulas in prenex normal form with quantifier prefix Q:
                                         Q • ψ[x(k1 , k2 )]
                               .                                              
                         κ1 ∧ x = uvw ∧ |u| = k1 − 1 ∧ |v| = k2 − k1 + 1
                        ∨ κ2 ∧ x =.
                                     uvw ∧ |u| = k1 − 1 ∧ |w| = −k2            
           Q∀u, v, w • 
                        ∨ κ3 ∧ x =.                                            ⇒ ψ[v]
                                     uvw ∧ |v| = −k1 + k2 + 1 ∧ |w| = −k2      
                                                 .   .     .
                         ∨ ¬(κ1 ∨ κ2 ∨ κ3 ) ∧ u = v = w = 

      where:

                              κ1    ,     1 ≤ k1 ≤ k2 ≤ |x|
                              κ2    ,     k1 − |x| ≤ k2 < 1 ≤ k1
                              κ3    ,     1 − |x| ≤ k1 ≤ k2 < 1

   • fst(x) and lst(x) for the first x(1, 1) and last element x(0, 0) of x, respec-
     tively.
  2 The presentation of the semantics of the theory is informal and implicit for brevity.




                                             8
3.1.2   Examples
A few examples demonstrate the expressiveness of the universal fragment of
Tseq(Z) to specify properties of sequences.
  1. Equality: sequences u and v are equal.
                                       .
                                     u=v                                            (1)

  2. Bounded equality: sequences u and v are equal in the constant interval
     [l, u] for l, u ∈ Z.
                                      .
                              u(l, u) = v(l, u)                         (2)
  3. Boundedness: no element in sequence u is greater than value v.
                                    .
                         ∀h, t • u = ht ⇒ t ≤ v                                     (3)

  4. Sortedness: sequence u is sorted (strictly increasing).
                            .
               ∀h, m, t • u = hmt ∧ |m| = 1 ∧ |t| > 0 ⇒ m < t                       (4)

  5. Injectivity: u has no repeated elements.
                                 .
          ∀h, v1 , m, v2 , t • u = hv1 mv2 t ∧ |v1 | = 1 ∧ |v2 | = 1 ⇒ v1 6= v2     (5)

  6. Partitioning: sequence u is partitioned at constant position k > 0.
                                             .              
                                     u(1, k) = h1 t1
                                                     .
              ∀h1 , t1 , h2 , t2 •  ∧ u(k + 1, 0) = h2 t2  ⇒ t1 < t2   (6)
                                     ∧ |t1 | > 0 ∧ |t2 | > 0

  7. Membership: constant element k ∈ Z occurs in sequence u.
                                       u ∈ (Z∗ kZ∗ )                                (7)

  8. Non-membership: no element in sequence u has value v.
                              .
                    ∀h, t • u = ht ∧ |t| > 0 ⇒ t 6= v                               (8)

  9. Periodicity: in non-empty sequence u, elements on even positions have
     value 0 and elements on odd positions have value 1 (notice that lst(h) = 0
     if h is empty).
                                                                    
                       .                  lst(h) = 1       lst(h) = 0
             ∀h, t • u = ht ∧ |t| > 0 ⇒               ∧                     (9)
                                           ⇒t=0             ⇒t=1

 10. Comparison between indices and values: for every index i, element at
     position i in the non-empty sequence u has value i + 3.
                             .
      u = 1+3∧∀h, t, v • u = ht∧|h| > 0∧|t| > 0∧lst(h) = v ⇒ t = v +1 (10)

 11. Disjunction of value constraints: for every pair of positions i < j in
     the sequence u, either u(i, i) ≤ u(j, j) or u(i, i) ≥ 2u(j, j).
                            .
     ∀h, v1 , m, v2 , t • u = hv1 mv2 t ∧ |v1 | > 0 ∧ |v2 | > 0 ⇒ v1 ≤ v2 ∨ v1 ≥ v2 + v2
                                                                                    (11)


                                          9
Comparison with theories of arrays. Properties such as strict sortedness
(4), periodicity (9), and comparisons between indices and values (10) are inex-
pressible in the array logic of Bradley et al. [8]. The latter is inexpressible also
in the logic of Ghilardi et al. [16] because Presburger arithmetic is restricted to
indices. Properties such as (11) are inexpressible both in the SIL array logic
of [21] — because quantification on multiple array indices is disallowed — and
in the related LIA logic of [22] — because disjunctions of comparisons of array
elements are disallowed. Extensions of each of these logics to accommodate the
required features would be undecidable.
    Conversely, properties such as permutation, bounded equality for an interval
specified by indices, length constraints for a variable value, membership for a
variable value, and the subsequence relation, are inexpressible in the universal
fragment of Tseq(Z) . Notice that membership and the subsequence relation are
expressible in the dual existential fragment of Tseq(Z) , while the other properties
seem to entail undecidability of the corresponding Tseq(Z) fragment (see Section
3.3). Bounded equality, length constraints, and membership, on the other hand,
are expressible in all the logics of [8, 16, 21, 22], and [16] outlines a decidable
extension which supports the subsequence relation (see Section 5).

3.2      Deciding Properties of Integer Sequences
This section presents a decision procedure Dseq(Z) for the universal fragment of
Tseq(Z) . The procedure transforms any universal Tseq(Z) formula into an equi-
satisfiable universal formula in the theory of concatenation over the free monoid
{a, b, c, d}∗ . The basic idea is to encode integers as sequences over the four sym-
bols {a, b, c, d}: the sequence acbk1 a encodes a nonnegative integer k1 , while the
sequence adb−k2 a encodes a negative integer k2 . Suitable rewrite rules encode all
quantifier-free Presburger arithmetic in accordance with this convention. The
next subsection 3.2.1 outlines the decision procedure Dseq(Z) , while subsection
3.2.2 illustrates its correctness and discusses its complexity.

3.2.1     Dseq(Z) : A Decision Procedure for Tseq(Z)
Consider a universal formula of Tseq(Z) in prenex normal form:

                                     ∀x1 , . . . , xv • ψ                         (12)

where ψ is quantifier-free. Modify (12) by application of the following steps.

  1. Introduce fresh variables to normalize formulas into the following form:
                        .            .
     f mla ::= var = var | var = var ◦ var | R(var) | var = 0 | var = 1
                       | var = var | var = var + var | var = var − var | var < var
                       | ¬f mla | f mla ∨ f mla | f mla ∧ f mla | f mla ⇒ f mla
        Clearly, we can achieve this by applying exhaustively rewrite rules that
        operate on ψ such as:
                               ψ[x ◦ y]                  ψ[x + y]
                             .
                           e = x ◦ y ⇒ ψ[e]          f = x + y ⇒ ψ[f ]
        for fresh variables e, f .


                                             10
   2. For each variable xi ∈ F V (ψ) = {x1 , . . . , xv }, introduce the fresh variables
      hi , ti , si , mi (for head, tail, sign, modulus) and rewrite ψ as:
                           .                               .            
                          xi = h i t i                      xi = 
                                .                                 .
                     ∧ hi = asi mi a
            ^                                      ∧ hi = asi mi a 
                     ∧ si ∈ {c, d}
                                                    
                                                    ∨  ∧ si =  .          
                                                                             ⇒ ψ
                                                                      c
                                     ∗
                                                                  .       
          1≤i≤v         ∧ mi ∈ b                        ∧ mi =         
                                         ∗     + ∗               .
                          ∧ ti ∈ (acb a ∪ adb a)            ∧ ti = 

   3. Apply the following rule exhaustively to remove arithmetic equalities:

                           ψ[xi = xj ]      ψ[xi = 0]       ψ[xi = 1]
                                .
                           ψ[hi = hj ]      ψ[hi ∈ 0]       ψ[hi ∈ 1]

   4. Apply the following rule exhaustively to remove differences:

                                         ψ[xk = xi − xj ]
                                         ψ[xi = xk + xj ]

   5. Apply the following rule exhaustively to remove comparisons:

                                           ψ[xi < xj ]
                                               .         .        
                                            si = d ∧ sj = c
                     .             
                   mi = mj                          ∨             
                        .
                  ∨ mi =
                                         .       .         .      
                          mj p  ⇒ ψ  si = s j =   c ∧ mj  = mi p 
                        .                                         
                   ∨ mj = mi p                      ∨             
                                          .      .          .
                                       si = sj = d ∧ mi = mj p

      for fresh p ∈ b+ .
   6. Apply the following rule exhaustively to remove sums:

                               ψ[x
                                 k = xi .+ xj ]            .                     
                                          si = sj ∧ xk = asi mi mj a
                                                          ∨                      
                .                        .            .               .        
              mi = mj            si =    6    sj ∧ m i  =  m   j ∧ x k =  aca    
                   .
             ∨ mi =
                                                                                 
                     mj p  ⇒ ψ                           ∨                      
                   .                   .              .                .         
              ∨ mj = mi p        si =
                                     6     s j ∧ m i =  m   j p  ∧ x k =  asi pa 
                                                                                  
                                                          ∨                      
                                        .              .                .
                                     6 sj ∧ mj = mi p ∧ xk = asj pa
                                  si =
      for fresh p ∈ b+ .

   7. Modify the meaning of regularity constraints as follows: let Ri be defined
      by a regular expression with constants in Z. Substitute every occurrence
      of a nonnegative constant k ∈ Z by acbk a; every occurrence of a negative
      constant k ∈ Z by adb−k a; every occurrence of set Z by acb∗ a ∪ adb+ a.

   The resulting formula is again in form (12) where ψ is now a quantifier-free
formula in the theory of concatenation over {a, b, c, d}∗ ; its validity is decidable
by Proposition 1.


                                            11
3.2.2   Correctness and Complexity
Let us sketch the correctness argument for the decision procedure Dseq(Z) , which
shows that the transformed formula is equi-satisfiable with the original one.
    The justification for step 1 is straightforward. After applying it a series of
substitutions eliminates arithmetic by reducing it to equations over the theory
of concatenation with the unary encoding of integers defined above.
    Step 2 requires that any variable xi is a sequence of the form (acb∗ a∪adb+ a)∗
and introduces fresh variables to denote significant parts of the sequence: hi
aliases the first element of the sequence which is further split into its sign si
(c for nonnegative and d for negative) and its absolute value mi encoded as a
unary string in b∗ . The second term of the disjunction deals with the case of xi
being , which has the same encoding as 0.
    The following steps replace elements of the signature of Presburger arith-
metic by rewriting them as equations over sequences with the given encoding.
Step 3 reduces the arithmetic equality of two sequences of integers to equiva-
lence of the sequences encoding their first elements. Step 4 rewrites equations
involving differences with equations involving sums.
    Step 5 reduces arithmetic comparisons of two sequences of integers to a case
discussion over the sequences hi , hj encoding their first elements. Let p be a
sequence in b+ encoding the difference between the absolute values correspond-
ing to hi and hj ; obviously such a p always exists unless the absolute values are
equal. Then, hi encodes an integer strictly less than hj iff one of the following
holds: (1) hi is a negative value and hj is a nonnegative one; (2) both hi and hj
are a nonnegative value and the sequence of b’s in hj is longer than the sequence
of b’s in hi ; or (3) both hi and hj are a negative value and the sequence of b’s
in hi is longer than the sequence of b’s in hj .
    Step 6 reduces the comparison between the value of a sum of two variables
and a third variable to an analysis of the three sequences hi , hj , hk encoding the
first elements of the three variables. As in step 6, the unary sequence p encodes
the difference between the absolute values corresponding to hi and hj . Then,
hk encodes the sum of the values encoded by hi and hj iff one of the following
holds: (1) hi and hj have the same sign and hk contains a sequence of b’s which
adds up the sequences of b’s of hi and hj , still with the same sign; (2) hi and
hj have opposite sign but same absolute value, so hk must encode 0; (3) hi and
hj have opposite sign and the absolute value of hi is greater than the absolute
value of hj , so hk has the same sign as hi and the difference of absolute values
as its absolute value; or (4) hi and hj have opposite sign and the absolute value
of hj is greater than the absolute value of hi , so hk has the same sign as hj and
the difference of absolute values as its absolute value.
    Finally, step 7 details how to translate the interpretation of the regular
constraints over Z into the corresponding regularity constraints over {a, b, c, d}
with the given integer encoding.
    It is not difficult to see that all rewriting steps in the decision procedure
Dseq(Z) increase the size of ψ at most quadratically (this accounts for fresh
variables as well). Hence, the PSPACE complexity of the universal fragment of
the theory of concatenation (Proposition 1) carries over to Dseq(Z) .
Theorem 4. The universal fragment of Tseq(Z) is decidable in PSPACE with
the decision procedure Dseq(Z) .


                                        12
3.3     Undecidable Extensions
Theorem 5. The following extensions of the universal fragment of Tseq(Z) are
undecidable.
   1. The ∀∗ ∃∗ and ∃∗ ∀∗ fragments.
   2. For any pair of integer constants k1 , k2 , the extension with the two length
      functions |x|k1 , |x|k2 counting the number of occurrences of k1 and k2 in
      x.
   3. The extension with an equal length predicate Elg(x, y) , |x| = |y|.
                                                 P|x|
   4. The extension with a sum function σ(x) , i=1 x(i, i).

Proof.     1. Sentences with one quantifier alternation are undecidable already
      for the theory of concatenation without arithmetic and over a monoid
      of finite rank (Proposition 2). Notice that the set of sentences that are
      expressible both in the ∀∗ ∃∗ and in the ∃∗ ∀∗ fragment is decidable [40,
      Th. 4.4]; however, this set lacks a simple syntactic characterization.

   2. Corollary of Proposition 2.
   3. We encode the universal theory of Π = hN, 0, 1, +, πi — where π(x, y) ,
      x2y — in the universal fragment of Tseq(Z) extended by the Elg predicate;
      undecidability follows from the undecidability of the existential and uni-
      versal theories of Π [11, Corollary 5]. All we have to do is showing that
      π(x, y) = p is universally definable in Tseq(Z) with Elg. To this end, first
      define ly as a sequence that begins with value y, ends with value 1, and
      where every element is the successor of the element that follows.
                                               .
      ∀h, t • fst(ly ) = y ∧ lst(ly ) = 1 ∧ ly = ht ∧ |h| > 0 ∧ |t| > 0 ⇒ lst(h) = t + 1

      As a result ly is in the form y, y − 1, . . . , 1 and hence has length y.3 Then,
      π(x, y) is universally definable as the sequence p with the same length
      as ly , whose last element is x, and where every element is obtained by
      doubling the value of the element that follows:
                                           .
      ∀g, u • Elg(p, ly ) ∧ lst(p) = x ∧ p = gu ∧ |g| > 0 ∧ |u| > 0 ⇒ lst(g) = u + u

      Hence p has the form 2y x, 2y−1 x, . . . , 22 x, 2x, x which encodes the desired
      value x2y in Tseq(Z) . (Notice that the two universal definitions of ly and
      p can be combined into a single universal definition by conjoining the
      definition of p to the consequent in the definition of ly ).

   4. For any sequence x over {0, 1} define Sp(x) = y as y ∈ 0∗ 1∗ ∧ σ(y) =
      σ(x). Then, Proposition 2 implies undecidability because this extension
      of Tseq(Z) can define universal sentences over the free monoid {a, b}∗ with
      the function Sp.
  3 This technique would allow the definition of the length function |x| and full index arith-

metic as well.




                                             13
 1 merge sort (a: ARRAY): ARRAY
 2 local l , r : ARRAY
 3 do
 4    if |a| ≤ 1 then
 5       { sorted(a) }                                                    1 reverse (a: LIST): LIST
 6       Result := a                                                      2 local v: INTEGER ; s: STACK
 7    else                                                                3 do
 8       l , r := a [1:| a|/2] , a [| a|/2+1: |a |]                       4    from s := 
 9       { l ?r=a}                                                        5    { invariant s ◦ a = old a }
10       l , r := merge sort (l ) , merge sort (r)                        6    until a = 
11       { sorted( l ) ∧ sorted(r) }                                      7    loop
12       from Result :=                                                  8       s .push (a. first )
13       { invariant sorted(Result) ∧ sorted(l) ∧ sorted(r) ∧             9       a := a. rest
14                         lst(Result) ≤ fst(l) ∧ lst(Result) ≤ fst(r) } 10    end
15       until | l | = 0 ∨ |r| = 0                                       11    from Result := 
16       loop                                                            12    { invariant
17             if l . first > r. first then
                                                                         13          s ◦ ResultR = old a }
18               Result := Result ? r.first ; r := r. rest
                                                                         14    until s = 
19            else
                                                                         15    loop
20               Result := Result ? l.first ; l := l . rest
                                                                         16       v := s.top
21            end
                                                                         17       s .pop ; Result.extend (v)
22       end
                                                                         18    end
23       if | l | > 0 then
24            { |r| = 0 } Result := Result ? l                           19 { ensure ResultR = old a}
25       else
26            { | l | = 0 } Result := Result ? r
27       end
28 { ensure sorted(Result) }




          Table 1: Annotated Mergesort (left) and Array Reversal (right).


     The decidability of the following is instead currently unknown: the extension
 of the universal fragment with a function x ⊕ 1 defined as the sequence x(1) +
 1, x(2)+1, . . . , x(|x|)+1. The fragment allows the definition of the set S = {0n 1n |
                                                                 .
 n ∈ N} as the sequences x such that x ∈ 0∗ 1∗ ∧ ∀u, v • x = uv ∧ u ∈ 0∗ ∧ v ∈
                 .
 1∗ ⇒ u ⊕ 1 = v. This is inexpressible in the universal fragment of the theory
 of concatenation, but the decidability of the resulting fragment is currently
 unknown (see Proposition 3).


 4      Verifying Sequence-Manipulating Programs
 This section outlines a couple of examples that demonstrate using formulas in
 the theory Tseq(Z) to reason about sequence-manipulating programs. An imple-
 mentation of the decision procedure Dseq(Z) is needed to tackle more extensive
 examples; it is currently underway. The examples are in Eiffel-like pseudo-code
 [36]; it is not difficult to detail an axiomatic semantics and a backward substi-
 tution calculus, using the universal fragment of Tseq(Z) , for the portions of this
 language used in the examples.

 Reversal. In Table 1 (right), a program reverses a sequence of integers, given
 as a list a, using a stack s. The query “first” returns the first element in a
 list, and the command “extend” adds an element to the right of a list; the
 query “top” and the commands “pop” and “push” for a stack have the usual
 semantics. In the annotations, s is modeled by a sequence whose first element
 is the bottom of the stack, whereas the expression old a denotes the value of a
 upon entering the routine.


                                                   14
   The superscript R denotes the reversal of a sequence. We do not know if the
extension of Tseq(Z) by a reversal function is decidable. However, the following
two simple update axioms are sufficient to handle any program which builds
the reverse uR of a sequence u starting from an empty sequence and adding one
element at a time:

             uR =  ⇔ u =                   |x| = 1 ⇒ (ux)R = xuR

    Consider, for instance, the verification condition that checks if the invariant
of the second loop (lines 11–18) is indeed inductive:

  s ◦ ResultR = old a ∧ s 6=      ⇒     s(1, −1) ◦ (Result ◦ s(0, 0))R = old a

After rewriting (Result ◦ s(0, 0))R into s(0, 0) ◦ ResultR the implication is
straightforward to check for validity. The rest of the program is also simple
to check with standard backward reasoning techniques.

Mergesort. Consider a straightforward recursive implementation of the Merge-
sort algorithm; Table 1 (left) shows an annotated version, where ? denotes the
concatenation operator in the programming language (whose semantics is cap-
tured by the corresponding logic operator ◦). The annotations specify that the
routine produces a sorted array, where predicate sorted(u) is defined as:
                                      .
       sorted(u)    ,    ∀h, m, t • u = hmt ∧ |m| > 1 ∧ |t| > 0 ⇒ m ≤ t

It is impossible to express in Tseq(Z) another component of the full functional
specification: the output is a permutation of the input. This condition is inex-
pressible in most of the expressive decidable extensions of the theory of arrays
that are currently known, such as [8, 21] (see also Section 5). Complementary
automated verification techniques — using different abstractions such as the
multiset [37] — can, however, verify this orthogonal aspect.
    We must also abstract away the precise splitting of array a into two halves
in line 8. The way in which a is partitioned into l and r is however irrelevant
as far as correctness if concerned (it only influences the complexity of the al-
gorithm), hence we can simply over-approximate the instruction on line 8 by a
nonderministic splitting in two continuous non-empty parts.
    From the annotated program, we can generate verification conditions by
standard backward reasoning. Universal sentences of Tseq(Z) can express the
verification conditions, hence the verification process can be automated. Let us
see an example on the non-trivial part of the process, namely checking that the
formula on lines 13–14 is indeed an inductive invariant. Consider the “then”
branch on line 18. Backward substitution of the invariant yields:

            sorted(Result ∗ fst(r)) ∧ sorted(l) ∧ sorted(r(2, 0)) ∧
      lst(Result ∗ fst(r)) ≤ fst(l) ∧ lst(Result ∗ fst(r)) ≤ fst(r(2, 0))     (13)

   This condition must be discharged by the corresponding loop invariant hy-
pothesis:

         fst(l) > fst(r) ∧ sorted(Result) ∧ sorted(l) ∧ sorted(r) ∧           (14)
        lst(Result) ≤ fst(l) ∧ lst(Result) ≤ fst(r) ∧ |l| =
                                                          6 0 ∧ |r| =
                                                                    6 0


                                        15
Checking that (14) entails (13) discharges the corresponding verification con-
dition. Elements of this condition can be encoded in the universal fragment
of Tseq(Z) and proven using the decision procedure of Section 3.2; for instance,
the fact that lst(Result) ≤ fst(l), |l| 6= 0, |r| 6= 0, and fst(l) > fst(r) imply
lst(Result ∗ fst(r)) ≤ fst(l) corresponds to the validity of (all free variables are
implicitly universally quantified):
                    .                                  
                  r = hr mr tr ∧ |hr | = 1 ∧ |r| = 6 0
                       .
                ∧ l = hl ml tl ∧ |hl | = 1 ∧ |l| = 6 0 
                                                         ⇒ t ≤ hl
               
                ∧ Result ◦ hr =    .
                                      hmt ∧ |t| = 1     
                  ∧ hl > hr

5    Related Work
Pioneering efforts on automated program verification focused on very simple
data types — in most cases just scalar variables — as the inherent difficul-
ties were already egregious. As verification techniques progressed and matured,
more complex data types were considered, such as lists (usually à la Lisp), ar-
rays, maps, and pointers, up to complex dynamic data structures. Arrays in
particular received a lot of attention, both for historical reasons (programming
languages have been offering them natively for decades), and because they often
serve as the basis for implementing more complex data structures. More gener-
ally, a renewed interest in developing decision procedures for new theories and
in integrating existing ones has blossomed over the last few years. A review of
this staggering amount of work is beyond the scope of this paper; for a partial
account and further references we refer the reader to e.g., [43, 30] (and [24, 28]
for applications). In this section, we review approaches that are most similar
to ours and in particular which yield decidable logics that can be compared
directly to our theory of sequences (see Section 3.1.2). This is the case with
several of the works on the theory of arrays and extensions thereof.

The theory of arrays. McCarthy initiated the research on formal reasoning
about arrays [34]. His theory of arrays defines the axiomatization of the ba-
sic access operations of read and write for quantifier-free formulas and without
arithmetic or extensionality (i.e., the property that if all elements of two arrays
are equal then the arrays themselves are equal). McCarthy’s work has usually
been the kernel of every theory of arrays: most works on (automated) reasoning
about arrays extend McCarthy’s theory with more complex (decidable) proper-
ties or efficiently automate reasoning within an existing theory.
    Thus, a series of work extended the theory of arrays with arithmetic [42, 25]
and with sorting predicates on array segments [33]; automated reasoning within
these theories is possible only for restricted classes of programs. Extensionality
is another very significant extension to the theory of arrays [41], which has now
become standard as it is decidable.
    The fast technological advances in automated theorem proving over the last
years have paved the way for efficient implementations of the theory of arrays
(usually with extensionality). These implementations use a variety of techniques
such as SMT solving [3, 15, 5, 17, 18], saturation theorem proving [31, 2], and
abstraction [9, 26, 27]. Automated invariant inference is an important appli-


                                        16
cation of these decision procedures, which originated a specialized line of work
[4, 35, 29].

Decidable extensions of the theory of arrays. The last few years have
seen an acceleration in the development of decidable extensions of the exten-
sional theory of arrays with more expressive predicates and functions.
    Bradley et al. [8] develop the array property fragment, a decidable subset
of the ∃∗ ∀∗ fragment of the theory of arrays. An array property is a formula
of the form ∃∗ ∀∗ • ι ⇒ ν, where the universal quantification is restricted to
index variables, ι is a guard on index variables with arithmetic (restricted to
existentially quantified variables), and ν is a constraint on array values without
arithmetic or nested reads, and where no universally quantified index variable
is used to select an element that is written to. The array property fragment
is decidable with a decision procedure that eliminates universal quantification
on index variables by reducing it to conjunctions on a suitable finite set of
index values. Extensions of the array property fragment that relax any of the
restrictions on the form of array properties are undecidable. Bradley et al. also
show how to adapt their theory of arrays to reason about maps.
    Ghilardi et al. [16] develop “semantic” techniques to integrate decision pro-
cedures into a decidable extension of the theory of arrays. Their ADP the-
ory merges the quantifier-free extensional theory of arrays with dimension and
Presburger arithmetic over indices into a decidable logic. Two extensions of the
ADP theory are still decidable: one with a unary predicate that determines if
an array is injective (i.e., it has no repeated elements); and one with a function
that returns the domain of an array (i.e., the set of indices that correspond
to definite values). Ghilardi et al. suggest that these extensions might be the
basis for automated reasoning on Separation Logic models. The framework of
[16] also supports other decidable extensions, such as the prefix, and sorting
predicates, as well as the map combinator also discussed in [12].
    De Moura and Bjørner [12] introduce combinatory array logic, a decidable
extension of the quantifier-free extensional theory of arrays with the map and
constant-value combinators (i.e., array functors). The constant-value combina-
tor defines an array with all values equal to a constant; the map combinator
applies a k-ary function to the elements at position i in k arrays a1 , . . . , ak .
De Moura and Bjørner define a decision procedure for their combinatory array
logic, which is implemented in the Z3 SMT solver.
    Habermehl et al. introduce powerful logics to reason about arrays with in-
teger values [22, 21, 6]; unlike most related work, the decidability of their logic
relies on automata-theoretic techniques for a special class of counter automata.
More precisely, [22] defines the Logic of Integer Arrays LIA, whose formulas are
in the ∃∗ ∀∗ fragment and allow Presburger arithmetic on existentially quantified
variables, difference and modulo constraints on index variables, and difference
constraints on array values. Forbidding disjunctions of difference constraints
on array values is necessary to ensure decidability. The resulting fragment is
quite expressive, and in particular it includes practically useful formulas that are
inexpressible in other decidable expressive fragments such as [8]. The compan-
ion work [21] introduces the Single Index Logic SIL, consisting of existentially
quantified Boolean combinations of formulas of the form ∀∗ • ι ⇒ ν, where the
universal quantification is restricted to index variables, ι is a positive Boolean



                                        17
combination of bound and modulo constraints on index variables, and ν is a
conjunction of difference constraints on array values. Again, the restrictions
on quantifier alternations and Boolean combinations are tight in that relaxing
one of them leads to undecidability. The expressiveness of SIL is very close
to that of LIA, and the two logics can be considered two variants of the same
basic kernel. The other work [6] shows how to use SIL to annotate and reason
automatically about array-manipulating programs; the tight correspondence be-
tween SIL and a class of counter automata allows the automatic generation of
loop invariants and hence the automation of the full verification process.

Other approaches. Static analysis and abstract interpretation techniques
have also been successfully applied to the analysis of array operations, especially
with the goal of inferring invariants automatically (e.g., [19, 20, 23]).


6    Future Work
Future work will investigate the decidability of the universal fragment of Tseq(Z)
extended with “weak” predicates or functions that slightly increase its expres-
siveness (such as that outlined at the end of Section 3.3). We will study to
what extent the decision procedure for the universal fragment of Tseq(Z) can
be integrated with other decidable logic fragments (and possibly with the dual
existential fragment). We will investigate how to automate the generation of
inductive invariants for sequence-manipulating programs by leveraging the de-
cidability of the universal fragment of Tseq(Z) . Finally, we will implement the
decision procedure, integrate it within a verification environment, and assess its
empirical effectiveness on real programs.


References
 [1] Habib Abdulrab and Jean-Pierre Pécuchet. Solving word equations. Jour-
     nal of Symbolic Computation, 8(5):499–521, 1989.
 [2] Alessandro Armando, Maria Paola Bonacina, Silvio Ranise, and Stephan
     Schulz. New results on rewrite-based satisfiability procedures. ACM Trans-
     actions on Compututational Logic, 10(1), 2009.
 [3] Alessandro Armando, Silvio Ranise, and Michaël Rusinowitch. Uniform
     derivation of decision procedures by superposition. In Proceedings of the
     15th International Workshop on Computer Science Logic (CSL’01), volume
     2142 of Lecture Notes in Computer Science, pages 513–527. Springer, 2001.
 [4] Dirk Beyer, Thomas A. Henzinger, Rupak Majumdar, and Andrey Ry-
     balchenko. Invariant synthesis for combined theories. In Proceedings of the
     8th International Conference on Verification, Model Checking, and Abstract
     Interpretation (VMCAI’07), volume 4349 of Lecture Notes in Computer
     Science, pages 378–394. Springer, 2007.
 [5] Miquel Bofill, Robert Nieuwenhuis, Albert Oliveras, Enric Rodrı́guez-
     Carbonell, and Albert Rubio. A write-based solver for SAT modulo the



                                        18
    theory of arrays. In Proceedings of 8th Conference on Formal Methods in
    Computer Aided Design (FMCAD’08), pages 1–8. IEEE, 2008.

 [6] Marius Bozga, Peter Habermehl, Radu Iosif, Filip Konecný, and Tomás
     Vojnar. Automatic verification of integer array programs. In Proceed-
     ings of the 21st International Conference on Computer Aided Verification
     (CAV’09), volume 5643 of Lecture Notes in Computer Science, pages 157–
     172. Springer, 2009.

 [7] Aaron R. Bradley and Zohar Manna.         The Calculus of Computation.
     Springer, 2007.
 [8] Aaron R. Bradley, Zohar Manna, and Henny B. Sipma. What’s decidable
     about arrays? In Proceedings of the 7th International Conference on Verifi-
     cation, Model Checking, and Abstract Interpretation (VMCAI’06), volume
     3855 of Lecture Notes in Computer Science, pages 427–442. Springer, 2006.
 [9] Robert Brummayer and Armin Biere. Lemmas on demand for the exten-
     sional theory of arrays. In Proceedings of the 6th International Workshop
     on Satisfiability Modulo Theories (SMT’08), 2008.
[10] J. Richard Büchi and Steven Senger. Coding in the existential theory of
     concatenation. Archive for Mathematical Logic, 26(1):101–106, 1987.
[11] J. Richard Büchi and Steven Senger. Definability in the existential theory
     of concatenation and undecidable extensions of this theory. Zeitschrift fur
     Mathematische Logik und Grundlagen der Mathematik, 34:337–342, 1988.

[12] Leonardo de Moura and Nikolaj Bjørner. Generalized, efficient array deci-
     sion procedures. In Proceedings of 9th Conference on Formal Methods in
     Computer Aided Design (FMCAD’09), pages 45–52, 2009.
[13] Volker Diekert. Makanin’s algorithm. In M. Lothaire, editor, Algebraic
     Combinatorics on Words. Cambridge University Press, 2002.

[14] Valery G. Durnev. Unsolvability of the positive ∀∃3 -theory of a free semi-
     group. Sibirskiı̆ Matematicheskiı̆ Zhurnal, 36(5):1067–1080, 1995.
[15] Vijay Ganesh and David L. Dill. A decision procedure for bit-vectors and
     arrays. In Proceedings of the 19th International Conference on Computer
     Aided Verification (CAV’07), volume 4590 of Lecture Notes in Computer
     Science, pages 519–531. Springer, 2007.
[16] Silvio Ghilardi, Enrica Nicolini, Silvio Ranise, and Daniele Zucchelli. De-
     cision procedures for extensions of the theory of arrays. Annals of Mathe-
     matics and Artificial Intelligence, 50(3-4):231–254, 2007.
[17] Silvio Ghilardi, Enrica Nicolini, Silvio Ranise, and Daniele Zucchelli. To-
     wards SMT model checking of array-based systems. In Proceedings of the
     4th International Joint Conference on Automated Reasoning (IJCAR’08),
     volume 5195 of Lecture Notes in Computer Science, pages 67–82. Springer,
     2008.




                                      19
[18] Amit Goel, Sava Krstic, and Alexander Fuchs. Deciding array formula
     with frugal axiom instantiation. In Proceedings of the 6th International
     Workshop on Satisfiability Modulo Theories (SMT’08), 2008.

[19] Denis Gopan, Thomas W. Reps, and Shmuel Sagiv. A framework for
     numeric analysis of array operations. In Proceedings of the 32nd ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages
     (POPL’05), pages 338–350. ACM, 2005.

[20] Sumit Gulwani, Bill McCloskey, and Ashish Tiwari. Lifting abstract in-
     terpreters to quantified logical domains. In Proceedings of the 35th ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages
     (POPL’08), pages 235–246. ACM, 2008.
[21] Peter Habermehl, Radu Iosif, and Tomás Vojnar. A logic of singly indexed
     arrays. In Proceedings of the 15th International Conference on Logic for
     Programming, Artificial Intelligence, and Reasoning (LPAR’08), volume
     5330 of Lecture Notes in Computer Science, pages 558–573. Springer, 2008.
[22] Peter Habermehl, Radu Iosif, and Tomás Vojnar. What else is decidable
     about integer arrays? In Proceedings of the 11th International Confer-
     ence on Foundations of Software Science and Computational Structures
     (FOSSACS’08), volume 4962 of Lecture Notes in Computer Science, pages
     474–489. Springer, 2008.
[23] Nicolas Halbwachs and Mathias Péron. Discovering properties about arrays
     in simple programs. In Proceedings of the ACM SIGPLAN 2008 Conference
     on Programming Language Design and Implementation (PLDI’08), pages
     339–348. ACM, 2008.
[24] Pieter Hooimeijer and Westley Weimer. A decision procedure for subset
     constraints over regular languages. In Proceedings of the 2009 ACM SIG-
     PLAN Conference on Programming Language Design and Implementation
     (PLDI’09), pages 188–198. ACM, 2009.

[25] Joxan Jaffar. Presburger arithmetic with array segments. Information
     Processing Letters, 12(2):79–82, 1981.
[26] Ranjit Jhala and Kenneth L. McMillan. Array abstractions from proofs.
     In Proceedings of the 19th International Conference on Computer Aided
     Verification (CAV’07), volume 4590 of Lecture Notes in Computer Science,
     pages 193–206. Springer, 2007.
[27] Deepak Kapur, Rupak Majumdar, and Calogero G. Zarba. Interpolation for
     data structures. In Proceedings of the 14th ACM SIGSOFT International
     Symposium on Foundations of Software Engineering (FSE’05), pages 105–
     116, 2006.
[28] Adam Kiezun, Vijay Ganesh, Philip J. Guo, Pieter Hooimeijer, and
     Michael D. Ernst. HAMPI: a solver for string constraints. In Proceed-
     ings of the 18th International Symposium on Software Testing and Analysis
     (ISSTA’09), pages 105–116. ACM, 2009.



                                     20
[29] Laura Kovács and Andrei Voronkov. Finding loop invariants for programs
     over arrays using a theorem prover. In Proceedings of the 12th Interna-
     tional Conference on Fundamental Approaches to Software Engineering
     (FASE’09), volume 5503 of Lecture Notes in Computer Science, pages 470–
     485. Springer, 2009.
[30] Viktor Kuncak, Ruzica Piskac, Philippe Suter, and Thomas Wies. Build-
     ing a calculus of data structures. In Proceedings of the 11th International
     Conference on Verification, Model Checking, and Abstract Interpretation
     (VMCAI’10), Lecture Notes in Computer Science. Springer, 2010.
[31] Christopher Lynch and Barbara Morawska. Automatic decidability. In
     Proceedings of the 17th IEEE Symposium on Logic in Computer Science
     (LICS’02), page 7. IEEE Computer Society, 2002.
[32] G. S. Makanin. The problem of solvability of equations in a free semi-
     group. Rossiı̆skaya Akademiya Nauk. Matematicheskiı̆ Sbornik (Translated
     in Sbornik Mathematics), 103(2):147–236, 1977.
[33] Prabhaker Mateti. A decision procedure for the correctness of a class of
     programs. Journal of the ACM, 28(2):215–232, 1981.
[34] John McCarthy. Towards a mathematical science of computation. In IFIP
     Congress, pages 21–28, 1962.
[35] Kenneth L. McMillan. Quantified invariant generation using an interpolat-
     ing saturation prover. In Proceedings of the 14th International Conference
     on Tools and Algorithms for the Construction and Analysis of Systems
     (TACAS’08), volume 4963 of Lecture Notes in Computer Science, pages
     413–427. Springer, 2008.
[36] Bertrand Meyer. Object-oriented software construction. Prentice Hall, 2nd
     edition, 1997.
[37] Ruzica Piskac and Viktor Kuncak. Decision procedures for multisets with
     cardinality constraints. In Proceedings of the 9th International Confer-
     ence on Verification, Model Checking, and Abstract Interpretation (VM-
     CAI’08), volume 4905 of Lecture Notes in Computer Science, pages 218–
     232. Springer, 2008.
[38] Wojciech Plandowski. Satisfiability of word equations with constants is in
     PSPACE. Journal of the ACM, 51(3):483–496, 2004.
[39] Wojciech Plandowski. An efficient algorithm for solving word equations. In
     Proceedings of the 38th Annual ACM Symposium on Theory of Computing
     (STOC’06), pages 467–476. ACM, 2006.
[40] Sebastian Seibert. Quantifier hierarchies over word relations. In Proceedings
     of the 5th Workshop on Computer Science Logic (CSL’91), volume 626 of
     Lecture Notes in Computer Science, pages 329–352. Springer, 1992.
[41] Aaron Stump, Clark W. Barrett, David L. Dill, and Jeremy R. Levitt. A
     decision procedure for an extensional theory of arrays. In Proceedings of
     the 16th Annual IEEE Symposium on Logic in Computer Science, pages
     29–37. IEEE Computer Society, 2001.

                                       21
[42] Norihisa Suzuki and David Jefferson. Verification decidability of presburger
     array programs. Journal of the ACM, 27(1):191–205, 1980.

[43] Karen Zee, Viktor Kuncak, and Martin C. Rinard. Full functional veri-
     fication of linked data structures. In Proceedings of the ACM SIGPLAN
     2008 Conference on Programming Language Design and Implementation
     (PLDI’08), pages 349–361. ACM, 2008.




                                       22
