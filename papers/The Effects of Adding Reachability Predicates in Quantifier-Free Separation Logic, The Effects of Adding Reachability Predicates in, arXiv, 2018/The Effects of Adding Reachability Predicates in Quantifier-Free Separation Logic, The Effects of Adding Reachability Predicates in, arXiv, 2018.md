                                                                                                                                                                             1

                                         The Effects of Adding Reachability Predicates in
                                         Quantifier-Free Separation Logic

                                         STÉPHANE DEMRI, Université Paris-Saclay, ENS Paris-Saclay, CNRS, LSV, 91190, Gif-sur-Yvette, France
arXiv:1810.05410v2 [cs.LO] 28 Feb 2021




                                         ETIENNE LOZES, I3S, Université Côte d’Azur, France
                                         ALESSIO MANSUTTI, Université Paris-Saclay, ENS Paris-Saclay, CNRS, LSV, 91190, Gif-sur-Yvette, France
                                         The list segment predicate ls used in separation logic for verifying programs with pointers is well-suited
                                         to express properties on singly-linked lists. We study the effects of adding ls to the full quantifier-free
                                         separation logic with the separating conjunction and implication, which is motivated by the recent design
                                         of new fragments in which all these ingredients are used indifferently and verification tools start to handle
                                         the magic wand connective. This is a very natural extension that has not been studied so far. We show that
                                         the restriction without the separating implication can be solved in polynomial space by using an appropriate
                                         abstraction for memory states whereas the full extension is shown undecidable by reduction from first-order
                                         separation logic. Many variants of the logic and fragments are also investigated from the computational point
                                         of view when ls is added, providing numerous results about adding reachability predicates to quantifier-free
                                         separation logic.

                                         CCS Concepts: • Theory of computation → Separation logic;

                                         Additional Key Words and Phrases: separation logic, reachability, decision problems, complexity, quantifier
                                         elimination.

                                         ACM Reference Format:
                                         Stéphane Demri, Etienne Lozes, and Alessio Mansutti. 2021. The Effects of Adding Reachability Predicates
                                         in Quantifier-Free Separation Logic. ACM Trans. Comput. Logic 1, 1, Article 1 (January 2021), 55 pages.
                                         https://doi.org/10.1145/3448269

                                         1    INTRODUCTION
                                         Separation logic [25, 33, 36] is a well-known assertion logic for reasoning about programs with
                                         dynamic data structures. Since the implementation of Smallfoot and the evidence that the method
                                         is scalable [3, 42], many tools supporting separation logic as an assertion language have been
                                         developed [3, 9, 10, 20, 22, 42]. Even though the first tools could handle relatively limited fragments
                                         of separation logic, like symbolic heaps [13], there is a growing interest and demand to consider
                                         extensions with richer expressive power. We can point out three particular extensions of symbolic
                                         heaps (without list predicates) that have been proved decidable.
                                              • Symbolic heaps with generalised inductive predicates, adding a fixpoint combinator to the
                                                language, is a convenient logic for specifying data structures that are more advanced than
                                                lists or trees. The entailment problem is known to be decidable by means of tree automata
                                                techniques for the bounded tree-width fragment [1, 24], whereas satisfiability is ExpTime-
                                                complete [7]. Other related results can be found in [26, 27].

                                         Authors’ addresses: Stéphane Demri, Université Paris-Saclay, ENS Paris-Saclay, CNRS, LSV, 91190, Gif-sur-Yvette, France,
                                         demri@lsv.fr; Etienne Lozes, I3S, Université Côte d’Azur, France, elozes@i3s.unice.fr; Alessio Mansutti, Université Paris-
                                         Saclay, ENS Paris-Saclay, CNRS, LSV, 91190, Gif-sur-Yvette, France, alessio.mansutti@lsv.fr.


                                         © 2009 Association for Computing Machinery.
                                         This is the author’s version of the work. It is posted here for your personal use. Not for redistribution. The definitive Version
                                         of Record was published in ACM Transactions on Computational Logic, https://doi.org/10.1145/3448269.



                                                                                 ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:2                                                   Stéphane Demri, Etienne Lozes, and Alessio Mansutti

      • List-free symbolic heaps with all classical Boolean connectives ∧ and ¬ (and with the sepa-
        rating conjunction ∗), called herein SL(∗), is a convenient extension when combinations of
        results of various analysis need to be expressed, or when the analysis requires a complemen-
        tation. This extension already is PSpace-complete [12].
      • Quantifier-free separation logic with separating implication, a.k.a. magic wand (−∗), is a
        convenient fragment (called herein SL(∗, −∗)) with decidable frame inference and abduction,
        two problems that play an important role in static analysers and provers built on top of
        separation logic. SL(∗, −∗) can be decided in PSpace thanks to a small model property [41].
   A natural question is how to combine these extensions, and which separation logic fragment
admitting Boolean connectives, magic wand and generalised recursive predicates can be decided
with some adequate restrictions. As already advocated in [8, 23, 32, 38, 40], dealing with the
separating implication −∗ is a desirable feature for program verification and several semi-automated
or automated verification tools support it in some way, see e.g. [23, 32, 38, 40].
   Besides, allowing quantifications is another direction to extend the symbolic heap fragment: in [4],
an extension of the symbolic heap fragment with quantification over locations and over arithmetic
variables for list lengths is introduced and several fragments are shown decidable (the whole
extension is undecidable). Such an extension combines shape and arithmetic specifications (see
also [14] for a theory of singly-linked lists with length combining such features) and the decidability
results are obtained by using so-called symbolic shape graphs that are finite representations of
sets of heaps. In the current paper, we consider only shape analysis (since herein, the heaps are
restricted to a single record field) but the separating implication is admitted.
   Our contribution. In this paper, we address the question of combining the magic wand and
inductive predicates in the extremely limited case where the only inductive predicate is the gentle
list segment predicate ls. The starting point of this work is this puzzling question: what is the
complexity/decidability status of quantifier-free separation logic SL(∗, −∗) enriched with the list seg-
ment predicate ls (herein called SL(∗, −∗, ls))? More precisely, we study the decidability/complexity
status of extensions of quantifier-free separation logic SL(∗, −∗) by adding one of the reachability
predicates among ls (precise predicate as usual in separation logic), reach (existence of a path,
possibly empty) and reach+ (existence of a non-empty path). At this point, it is worth noting that
in the presence of the separating conjunction ∗, ls and reach are interdefinable, and reach+ can
easily define ls and reach. Consequently, the complexity upper bounds will be stated with reach+
and the complexity lower bounds or undecidability results are sharper with ls or reach.
   First, we establish that the satisfiability problem for the quantifier-free separation logic SL(∗, −∗, ls)
is undecidable. Our proof is by reduction from the undecidability of first-order separation logic
SL(∀, −∗) [6, 16], using an encoding of the variables as heap cells (see Theorem 3.12). As a conse-
quence, we also establish that SL(∗, −∗, ls) is not finitely axiomatisable. Moreover, our reduction
requires a rather limited expressive power of the list segment predicate, and we can strengthen our
undecidability results to some fragments of SL(∗, −∗, ls). For instance, surprisingly, the extension
of SL(∗, −∗) with the atomic formulae of the form reach(x, y) = 2 and reach(x, y) = 3 (existence of
a path between x and y of respective length 2 or 3) is already undecidable, whereas the satisfiability
problem for SL(∗, −∗, reach(x, y) = 2) is known to be in PSpace [17].
   Second, we show that the satisfiability problem for SL(∗, reach+ ) is PSpace-complete, extending
the well-known result on SL(∗). The PSpace upper bound relies on a small heap property based
on the techniques of test formulae, see e.g. [5, 17, 21, 28–30], and the PSpace-hardness of SL(∗) is
inherited from [12]. The PSpace upper bound can be extended to the fragment of SL(∗, −∗, reach+ )
made of Boolean combinations of formulae from SL(∗, reach+ ) ∪ SL(∗, −∗) (see the developments
in Section 4). As a by-product of our proof technique, we obtain that the satisfiability problem for

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                1:3

     SL(∀, −∗)                    SL(∗, −∗, reach(x, y) = 2, reach(x, y) = 3)                      SL(∗, −∗, ls)
    undecidable                                   undecidable                                      undecidable
      [6, 16]                                   (Corollary 3.15)                                 (Theorem 3.12)


                           SL(∗)                 SL(∗, reach+ )
                      PSpace-complete          PSpace-complete
                            [12]                (Theorem 4.12)


                             SHF                 Bool(SHF)
                            PTime               NP-complete
                           [13, 22]       (Corollary 4.13 and [34])

                                         Fig. 1. Main contributions.


Boolean combinations of pure formulae and spatial formulae from the symbolic heap fragment,
Bool(SHF), is NP-complete via a proof different from the one in [34]. Figure 1 presents a summary
of the main results of the paper. An unlabelled arrow between two logics means that there is a
many-one reduction between the satisfiability problem of the first logic and the problem for the
second one (sometimes, the reduction is the identity in the case of syntactic fragments).
   This paper is an extended and completed version of [18].

2     PRELIMINARIES
2.1    Separation logic with the list segment predicate
Let PVAR = {x, y, . . .} be a countably infinite set of program variables and LOC = {ℓ0, ℓ1, ℓ2, . . .} be
a countable infinite set of locations. A memory state is a pair (𝑠, ℎ) such that 𝑠 : PVAR → LOC is
a variable valuation (known as the store) and ℎ : LOC →fin LOC is a partial function with finite
domain, known as the heap. We write dom(ℎ) to denote its domain and ran(ℎ) to denote its range.
Given a heap ℎ with dom(ℎ) = {ℓ1, . . . , ℓ𝑛 }, we also write {ℓ1 ↦→ ℎ(ℓ1 ), . . . , ℓ𝑛 ↦→ ℎ(ℓ𝑛 )} to denote ℎ.
Each ℓ𝑖 ↦→ ℎ(ℓ𝑖 ) is understood as a memory cell of ℎ.
   Let ℎ 1 and ℎ 2 be two heaps. ℎ 1 and ℎ 2 are said to be disjoint, written ℎ 1 ⊥ℎ 2 , whenever their
domains are disjoint, i.e. dom(ℎ 1 ) ∩ dom(ℎ 2 ) = ∅. When ℎ 1 ⊥ℎ 2 , we write ℎ 1 + ℎ 2 to denote
the heap corresponding to the disjoint union of the graphs of ℎ 1 and ℎ 2 , hence dom(ℎ 1 + ℎ 2 ) =
dom(ℎ 1 ) ⊎ dom(ℎ 2 ). If the domains of ℎ 1 and ℎ 2 are not disjoint, then the union ℎ 1 + ℎ 2 is not
defined. We say that ℎ 1 is a subheap of ℎ 2 , written ℎ 1 ⊑ ℎ 2 , if dom(ℎ 1 ) ⊆ dom(ℎ 2 ) and for all
ℓ ∈ dom(ℎ 1 ), we have ℎ 1 (ℓ) = ℎ 2 (ℓ). For instance, if ℎ 1 ⊥ℎ 2 then ℎ 1 ⊑ ℎ 1 + ℎ 2 . Given a heap ℎ, we
write ℎ𝑖 for the (partial) function obtained from 𝑖 functional composition(s) of ℎ. By definition, ℎ 0 is
                                     def                                                        def
the identity function on LOC, ℎ 1 = ℎ and for all 𝛽 ≥ 2 and ℓ ∈ LOC, we have ℎ 𝛽 (ℓ) = ℎ(ℎ 𝛽−1 (ℓ)),
assuming that ℎ (ℓ) is defined and belongs to dom(ℎ), otherwise ℎ (ℓ) is undefined.
                  𝛽−1                                                         𝛽

   The formulae 𝜑 of the separation logic SL(∗, −∗, ls) and its atomic formulae 𝜋 are built from the
grammars below (where x, y ∈ PVAR and the connectives ⇒, ⇔ and ∨ are defined as usually).
                                 𝜋 ::= emp | x = y | x ↩→ y | ls(x, y)

                                𝜑 ::= 𝜋 | ¬𝜑 | 𝜑 ∧ 𝜑 | 𝜑 ∗ 𝜑 | 𝜑 −∗ 𝜑
Models of SL(∗, −∗, ls) are memory states and the satisfaction relation |= is defined as follows:

                                  ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:4                                                   Stéphane Demri, Etienne Lozes, and Alessio Mansutti

  (𝑠, ℎ) |= emp           ⇐⇒    dom(ℎ) = ∅.
  (𝑠, ℎ) |= x = y         ⇐⇒    𝑠 (x) = 𝑠 (y).
  (𝑠, ℎ) |= x ↩→ y        ⇐⇒    𝑠 (x) ∈ dom(ℎ) and ℎ(𝑠 (x)) = 𝑠 (y).
  (𝑠, ℎ) |= ls(x, y)      ⇐⇒    either (dom(ℎ) = ∅ and 𝑠 (x) = 𝑠 (y)) or
                                ℎ = {ℓ0 ↦→ ℓ1, ℓ1 ↦→ ℓ2, . . . , ℓ𝑛−1 ↦→ ℓ𝑛 } for some 𝑛 ≥ 1,
                                ℓ0 = 𝑠 (x), ℓ𝑛 = 𝑠 (y) and for all 𝑖 ≠ 𝑗 ∈ [0, 𝑛], ℓ𝑖 ≠ ℓ 𝑗 .
  (𝑠, ℎ) |= ¬𝜑         ⇐⇒ (𝑠, ℎ) ̸ |= 𝜑.
  (𝑠, ℎ) |= 𝜑 1 ∧ 𝜑 2  ⇐⇒ (𝑠, ℎ) |= 𝜑 1 and (𝑠, ℎ) |= 𝜑 2 .
  (𝑠, ℎ) |= 𝜑 1 ∗ 𝜑 2  ⇐⇒ there are ℎ 1 and ℎ 2 such that ℎ 1 ⊥ℎ 2 , ℎ 1 + ℎ 2 = ℎ,
                                (𝑠, ℎ 1 ) |= 𝜑 1 and (𝑠, ℎ 2 ) |= 𝜑 2 .
  (𝑠, ℎ) |= 𝜑 1 −∗ 𝜑 2 ⇐⇒ for all ℎ 1 such that ℎ 1 ⊥ℎ and (𝑠, ℎ 1 ) |= 𝜑 1 , we have (𝑠, ℎ + ℎ 1 ) |= 𝜑 2 .
The semantics for ∗ (separating conjunction), −∗ (separating implication), ↩→ (points to), ls and for
all other ingredients is the usual one in separation logic, where ls(x, y) is the precise list segment
predicate stating that ℎ𝑖 (𝑠 (x)) = 𝑠 (y) for some 𝑖 ∈ N, but this property does not hold in any strict
subheap of ℎ (which excludes the presence of cycles).
                                                                         def
   In the sequel, we use the following abbreviations: size ≥ 0 = ⊤ and for all 𝛽 ≥ 0,
                        def
      • size ≥ 𝛽 + 1 = (size ≥ 𝛽) ∗ ¬emp,
                 def
      • size ≤ 𝛽 = ¬(size ≥ 𝛽 + 1) and,
                 def
      • size = 𝛽 = (size ≤ 𝛽) ∧ (size ≥ 𝛽).
It is easy to see that (𝑠, ℎ) |= size ≥ 𝛽 iff card(dom(ℎ)) ≥ 𝛽, where card(𝑋 ) denotes the cardinality
                                                                                              def
of a (finite) set 𝑋 . We introduce the septraction connective −⊛, defined as 𝜑 1 −⊛ 𝜑 2 = ¬(𝜑 1 −∗ ¬𝜑 2 ).
The connective −⊛ can be viewed as a form of dual operator for the separating implication. So,
(𝑠, ℎ) |= 𝜑 1 −⊛ 𝜑 2 iff there is some heap ℎ 1 disjoint from ℎ such that (𝑠, ℎ 1 ) |= 𝜑 1 and (𝑠, ℎ + ℎ 1 ) |= 𝜑 2 .
We introduce also the following standard abbreviations:
                              def                                         def
                alloc(x) = (x ↩→ x) −∗ ⊥                         x ↦→ y = (x ↩→ y) ∧ size = 1.
It holds that (𝑠, ℎ) |= alloc(x) iff 𝑠 (x) ∈ dom(ℎ), whereas (𝑠, ℎ) |= x ↦→ y iff dom(ℎ) = {𝑠 (x)} and
ℎ(𝑠 (x)) = 𝑠 (y). Without loss of generality, we assume that LOC = N (see also Section 3.1). We
write SL(∗, −∗) to denote the restriction of SL(∗, −∗, ls) without ls. Similarly, SL(∗) denotes the
restriction of SL(∗, −∗) without −∗ and SL(−∗) denotes its restriction without ∗. Given two formulae
𝜑, 𝜑 ′ (possibly from different logical languages), we write 𝜑 ≡ 𝜑 ′ whenever for all memory states
(𝑠, ℎ), we have (𝑠, ℎ) |= 𝜑 iff (𝑠, ℎ) |= 𝜑 ′. When 𝜑 ≡ 𝜑 ′, the formulae 𝜑 and 𝜑 ′ are said to be
equivalent.

2.2    Variants with other reachability predicates
We use two additional reachability predicates reach(x, y) and reach+ (x, y). We write SL(∗, −∗, reach)
(resp. SL(∗, −∗, reach+ )) to denote the variant of SL(∗, −∗, ls) in which ls is replaced by reach (resp.
by reach+ ). The satisfaction relation |= is extended as follows:
      • (𝑠, ℎ) |= reach(x, y) holds when there is 𝑖 ≥ 0 such that ℎ𝑖 (𝑠 (x)) = 𝑠 (y),
      • (𝑠, ℎ) |= reach+ (x, y) holds when there is 𝑖 ≥ 1 such that ℎ𝑖 (𝑠 (x)) = 𝑠 (y).
When the heap ℎ is understood as a directed graph with a finite relation, reach(x, y) corresponds
to the standard reachability predicate (differently from ls, which also imposes constraints on strict
subheaps). reach+ (x, y) corresponds instead to the reachability predicate in at least one step. For
instance, reach(x, x) always holds, whereas ls(x, x) holds only on the empty heap and reach+ (x, x)
holds on heaps such that there is 𝑖 ≥ 1 with ℎ𝑖 (𝑠 (x)) = 𝑠 (x), i.e. there is a non-empty path (cycle)
from 𝑠 (x) to itself.

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                1:5

  As ls(x, y) ≡ reach(x, y) ∧ ¬(¬emp ∗ reach(x, y)) and reach(x, y) ≡ ⊤ ∗ ls(x, y), the logics
SL(∗, −∗, reach) and SL(∗, −∗, ls) have identical decidability status. Besides, these two logics can be
seen as fragments of SL(∗, −∗, reach+ ), thanks to the equivalence below:
                                  reach(x, y) ≡ x = y ∨ reach+ (x, y).
Notice that this analysis can be carried out as soon as ∗, ¬, ∧ and emp are parts of the logic (none
of the equivalences above uses the separating implication −∗). More specifically, SL(∗, reach) and
SL(∗, ls) have the same decidability status, and can be viewed as fragments of SL(∗, reach+ ). It
is therefore stronger to establish decidability or complexity upper bounds with reach+ and to
show undecidability or complexity lower bounds with ls or reach. Herein, we provide the optimal
results.

2.3    Decision problems
Let 𝔏 be a logic defined above. As usual, the satisfiability problem for 𝔏 takes as an input a formula
𝜑 from 𝔏 and asks whether there is a memory state (𝑠, ℎ) satisfying it, i.e. (𝑠, ℎ) |= 𝜑. The validity
problem for 𝔏 asks instead whether 𝜑 is satisfied by every memory state. If 𝔏 is not closed under
negation, then it is also worth considering the entailment problem that takes as inputs two formulae 𝜑
and 𝜑 ′, and asks whether for all the memory states (𝑠, ℎ), we have (𝑠, ℎ) |= 𝜑 implies (𝑠, ℎ) |= 𝜑 ′
(written 𝜑 |= 𝜑 ′).
   The model-checking problem for 𝔏 takes as an input a formula 𝜑 from 𝔏 and a finite representation
of a memory state (𝑠, ℎ), and asks whether (𝑠, ℎ) |= 𝜑. Notice that, given a formula 𝜑, it is easy to
find a finite representation of (𝑠, ℎ): it is sufficient to restrict 𝑠 to the variables occurring in 𝜑 and to
encode ℎ as a finite directed graph such that each vertex has at most one outgoing vertex. Unless
otherwise specified, the size of a formula 𝜑 is understood as the size of its syntax tree. Moreover,
the size of the finite representation of a memory state (𝑠, ℎ) is defined naturally considering a
reasonably succinct encoding of 𝑠 (only interpreting the program variables in 𝜑) and the graph
representation of ℎ.
   Below, we recall a few complexity results about well-known strict fragments of SL(∗, −∗, ls).
  Proposition 2.1.
  (I) The satisfiability problem is PSpace-complete for both SL(∗) and SL(∗, −∗) [12].
 (II) The satisfiability and entailment problems for the symbolic heap fragment are in PTime [13].
(III) The satisfiability problem for the fragment of SL(∗, ls) restricted to formulae obtained by
      Boolean combinations of formulae from the symbolic heap fragment is NP-complete [13, 34].
   We refer the reader to [13] for a complete description of the symbolic heap fragment, or to
Section 4.3 for its definition. The main purpose of this paper is to study the decidability/complexity
status of SL(∗, −∗, ls), as well as for its fragments and variants.

3     UNDECIDABILITY OF THE SATISFIABILITY PROBLEM FOR SL(∗, −∗, ls)
In this section, we show that SL(∗, −∗, ls) has an undecidable satisfiability problem even though it
does not admit explicitly first-order quantification. We stress the word “explicitly” as we show that
SL(∗, −∗, ls) can simulate the first-order quantification from SL(∀, −∗): the first-order extension of
SL(−∗), studied in [6, 16].
   In the versions of SL(∀, −∗) defined in [6, 16], one distinguishes program variables from quantified
variables (used with the first-order quantification ∀). This distinction made by the two sets of
variables is not necessary herein and for the sake of simplicity, we adopt a version of SL(∀, −∗) with
a unique type of variables. The formulae 𝜑 of SL(∀, −∗) are built from the grammars below:
                                           𝜋 ::= x = y | x ↩→ y

                                  ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:6                                                   Stéphane Demri, Etienne Lozes, and Alessio Mansutti

                              𝜑 ::= 𝜋 | ¬𝜑 | 𝜑 ∧ 𝜑 | 𝜑 −∗ 𝜑 | ∀x 𝜑,
where x, y ∈ PVAR. Models of the logic SL(∀, −∗) are memory states and the satisfaction relation |=
is defined as for SL(−∗) with the additional clause:
                    (𝑠, ℎ) |= ∀x 𝜑 ⇐⇒ for all ℓ ∈ LOC, we have (𝑠 [x ← ℓ], ℎ) |= 𝜑,
where 𝑠 [x ← ℓ] is defined from the store 𝑠 by only changing that x takes the value ℓ. Note that emp
can be easily defined by ¬∃ x (x ↩→ x−∗ ⊥). Without any loss of generality, we can assume that
the satisfiability (resp. validity) problem for SL(∀, −∗) is defined by taking as inputs closed formulae
(i.e. without free occurrences of the variables).
   Proposition 3.1. [6, 16] The satisfiability problem for SL(∀, −∗) is undecidable and the set of valid
formulae for SL(∀, −∗) is not recursively enumerable.
   We recall that the undecidability proof of SL(∀, −∗) makes extensive use of the operator −∗,
whereas a similar result can be achieved without −∗ if we interpret the logic on heaps having
at least two record fields (i.e. ℎ is of the form LOC →fin LOC𝑘 with 𝑘 ≥ 2) [12]. In a nutshell,
we establish the undecidability of SL(∗, −∗, ls) by a reduction from the satisfiability problem for
SL(∀, −∗). The reduction is nicely decomposed in two intermediate steps: (1) the undecidability of
SL(∗, −∗) extended with a few atomic predicates, to be defined soon, and (2) a tour de force resulting
in the encoding of these atomic predicates in SL(∗, −∗, ls). In particular, Section 3.2 explains how
the additional predicates can be used to encode stores as subheaps, and how this helps to mimic
first-order quantification. Section 3.3 provides the formal presentation of the translation as well as
its correctness. Section 3.4 establishes how the additional predicates can be indeed expressed in
SL(∗, −∗, ls). Finally, Section 3.5 provides the concluding results about undecidability and refines
the results of the previous sections.

3.1    Generalised memory states
For technical convenience, in order to reduce (the satisfiability problem of) SL(∀, −∗) to SL(∗, −∗, ls)
we consider a slight alternative for the semantics of these two logics, which does not modify
the notion of satisfiability/validity and such that the set of formulae and the definition of the
satisfaction relation |= remain unchanged. So far, the memory states are pairs of the form (𝑠, ℎ) with
𝑠 : PVAR → LOC and ℎ : LOC →fin LOC for a fixed countably infinite set of locations LOC, e.g. N.
Alternatively, the models for SL(∀, −∗) and SL(∗, −∗, ls) can be defined as triples (LOC1, 𝑠 1, ℎ 1 ) such
that LOC1 is a countably infinite set, 𝑠 1 : PVAR → LOC1 and ℎ 1 : LOC1 →fin LOC1 . Most of the time,
a generalised memory state (LOC1, 𝑠 1, ℎ 1 ) shall be written (𝑠 1, ℎ 1 ) when no confusion is possible.
Given a bijection 𝔣 : LOC1 → LOC2 and a heap ℎ 1 : LOC1 →fin LOC1 that can be represented
by {ℓ1 ↦→ ℎ 1 (ℓ1 ), . . . , ℓ𝑛 ↦→ ℎ 1 (ℓ𝑛 )}, we write 𝔣(ℎ 1 ) to denote the heap ℎ 2 : LOC2 →fin LOC2 with
ℎ 2 = {𝔣(ℓ1 ) ↦→ 𝔣(ℎ 1 (ℓ1 )), . . . , 𝔣(ℓ𝑛 ) ↦→ 𝔣(ℎ 1 (ℓ𝑛 ))}.
   Definition 3.2. Let (LOC1, 𝑠 1, ℎ 1 ) and (LOC2, 𝑠 2, ℎ 2 ) be generalised memory states and 𝑋 ⊆ PVAR.
An 𝑋 -isomorphism from (LOC1, 𝑠 1, ℎ 1 ) to (LOC2, 𝑠 2, ℎ 2 ) is a bijection 𝔣 : LOC1 → LOC2 such that
ℎ 2 = 𝔣(ℎ 1 ) and for all x ∈ 𝑋 , 𝔣(𝑠 1 (x)) = 𝑠 2 (x).
   Note that if 𝔣 is an 𝑋 -isomorphism from (LOC1, 𝑠 1, ℎ 1 ) to (LOC2, 𝑠 2, ℎ 2 ), then 𝔣−1 is also an 𝑋 -
isomorphism from (LOC2, 𝑠 2, ℎ 2 ) to (LOC1, 𝑠 1, ℎ 1 ). Two generalised memory states (LOC1, 𝑠 1, ℎ 1 )
and (LOC2, 𝑠 2, ℎ 2 ) are said to be isomorphic with respect to 𝑋 , written (LOC1, 𝑠 1, ℎ 1 ) ≈𝑋 (LOC2, 𝑠 2, ℎ 2 ),
if and only if there exists an 𝑋 -isomorphism between them.
   It is easy to check that ≈𝑋 is an equivalence relation. A folklore result states that isomorphic
memory states satisfy the same formulae, which implies that considering generalised memory
states over (standard) memory states does not change the notion of satisfiability and validity. Below,

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                            1:7

we state the precise result we need in the sequel, the proof being by a standard induction on the
formula structure.
   Lemma 3.3. Let (LOC1, 𝑠 1, ℎ 1 ), (LOC2, 𝑠 2, ℎ 2 ) be generalised memory states and 𝑋 ⊆ PVAR be a
finite set of variables such that (LOC1, 𝑠 1, ℎ 1 ) ≈𝑋 (LOC2, 𝑠 2, ℎ 2 ). Given 𝜑 in SL(∗, −∗, ls) or SL(∀, −∗),
with free variables from 𝑋 , (LOC1, 𝑠 1, ℎ 1 ) |= 𝜑 iff (LOC2, 𝑠 2, ℎ 2 ) |= 𝜑.
  Proof. The proof is by induction on the tree structure of 𝜑. Let 𝑋 be a set of variables that
includes the free variables from 𝜑. To be more concise, this is done on formulae from SL(∀, ∗, −∗, ls).
Let 𝔣 : LOC1 → LOC2 be a bijection defined as in Definition 3.2. Since ≈𝑋 is an equivalence relation,
showing one direction suffices to prove the result. We start by considering the base case with
ls(x, y), the cases for x = y and x ↩→ y being omitted as this poses no difficulty.
base case: ls(x, y). If (LOC1, 𝑠 1, ℎ 1 ) |= ls(x, y), then either (dom(ℎ 1 ) = ∅ and 𝑠 1 (x) = 𝑠 1 (y)) or
       ℎ 1 = {ℓ0 ↦→ ℓ1, ℓ1 ↦→ ℓ2, . . . , ℓ𝑛−1 ↦→ ℓ𝑛 } with 𝑛 ≥ 1, ℓ0 = 𝑠 1 (x), ℓ𝑛 = 𝑠 1 (y) and for all
       𝑖 ≠ 𝑗 ∈ [0, 𝑛], ℓ𝑖 ≠ ℓ 𝑗 . Notice that since for all x ∈ 𝑋 , 𝔣(𝑠 1 (x)) = 𝑠 2 (x) (Definition 3.2),
       we have 𝑠 1 (x) = 𝑠 1 (y) if and only if 𝑠 2 (x) = 𝑠 2 (y). Moreover, again from the definition of
       𝑋 -isomorphism, dom(ℎ 1 ) and dom(ℎ 2 ) have the same cardinality. Thus, if dom(ℎ 1 ) = ∅
       and 𝑠 1 (x) = 𝑠 1 (y), we conclude that dom(ℎ 2 ) = ∅ and 𝑠 2 (x) = 𝑠 2 (y). Otherwise, let us
       consider the case where ℎ 1 = {ℓ0 ↦→ ℓ1, ℓ1 ↦→ ℓ2, . . . , ℓ𝑛−1 ↦→ ℓ𝑛 } with 𝑛 ≥ 1, ℓ0 = 𝑠 1 (x),
       ℓ𝑛 = 𝑠 1 (y) and for all 𝑖 ≠ 𝑗 ∈ [0, 𝑛] ℓ𝑖 ≠ ℓ 𝑗 . Notice that card(dom(ℎ 1 )) = 𝑛. By definition of
       𝑋 -isomorphism, 𝑠 2 (x) = 𝔣(𝑠 1 (x)) = 𝔣(ℓ0 ), 𝑠 2 (y) = 𝔣(𝑠 1 (y)) = 𝔣(ℓ𝑛 ) and given 𝑖 ∈ [0, 𝑛 − 1],
       ℎ 2 (𝔣(ℓ𝑖 )) = 𝔣(ℎ 1 (ℓ𝑖 )) = 𝔣(ℓ𝑖+1 ). So, {𝑠 2 (x) ↦→ 𝔣(ℓ1 ), 𝔣(ℓ1 ) ↦→ 𝔣(ℓ2 ), . . . , 𝔣(ℓ𝑛−1 ) ↦→ 𝑠 2 (y)} ⊆ ℎ 2 .
       Moreover, from the fact that for all 𝑖 ≠ 𝑗 ∈ [0, 𝑛], ℓ𝑖 ≠ ℓ 𝑗 , we conclude that for all 𝑖 ≠ 𝑗 ∈ [0, 𝑛],
       𝔣(ℓ𝑖 ) ≠ 𝔣(ℓ 𝑗 ). From card(dom(ℎ 1 )) = 𝑛 we derive card(dom(ℎ 2 )) = 𝑛, and therefore ℎ 2 =
       {𝑠 2 (x) ↦→ 𝔣(ℓ1 ), 𝔣(ℓ1 ) ↦→ 𝔣(ℓ2 ), . . . , 𝔣(ℓ𝑛−1 ) ↦→ 𝑠 2 (y)}, where 𝑠 2 (x), 𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛−1 ), 𝑠 2 (y) are
       𝑛 + 1 distinct locations. We conclude that (LOC2, 𝑠 2, ℎ 2 ) satisfies ls(x, y).
Concerning the cases for the induction step, we omit the obvious cases when the outermost
connective is the conjunction or the negation. We conclude the proof by considering formulae of
the form 𝜑 1 ∗ 𝜑 2 , 𝜑 1 −∗ 𝜑 2 and ∀x 𝜑 1 .
induction step: case with ∗. If (LOC1, 𝑠 1, ℎ 1 ) |= 𝜑 1 ∗ 𝜑 2 , then there are two heaps ℎ 1′ and ℎ 1′′ such
       that ℎ 1 = ℎ 1′ + ℎ 1′′, (LOC1, 𝑠 1, ℎ 1′ ) |= 𝜑 1 and (LOC1, 𝑠 1, ℎ 1′′) |= 𝜑 2 . Let ℎ 2′ = 𝔣(ℎ 1′ ) and ℎ 2′′ = 𝔣(ℎ 1′′)
       the images of ℎ 1′ and ℎ 1′′ via 𝔣. Since 𝔣 is an 𝑋 -isomorphism between ℎ 1 and ℎ 2 it holds that:
                               ℎ 2 = 𝔣(ℎ 1 ) = 𝔣(ℎ 1′ + ℎ 1′′) = 𝔣(ℎ 1′ ) + 𝔣(ℎ 1′′) = ℎ 2′ + ℎ 2′′
      and moreover ℎ 2′ ⊥ℎ 2′′. Lastly, (LOC1, 𝑠 1, ℎ 1′ ) ≈𝑋 (LOC2, 𝑠 2, ℎ 2′ ), since 𝔣 is an 𝑋 -isomorphism
      also between these structures. The same holds for ℎ 1′′ and ℎ 2′′. Therefore, by the induc-
      tion hypothesis, we get (LOC2, 𝑠 2, ℎ 2′ ) |= 𝜑 1 and (LOC2, 𝑠 2, ℎ 2′′) |= 𝜑 2 . We conclude that
      (LOC2, 𝑠 2, ℎ 2 ) |= 𝜑 1 ∗ 𝜑 2 .
induction step: case with −∗. If (LOC1, 𝑠 1, ℎ 1 ) |= 𝜑 1 −∗ 𝜑 2 , then for every heap ℎ 1′ , if ℎ 1′ ⊥ℎ 1 and
      (LOC1, 𝑠 1, ℎ 1′ ) |= 𝜑 1 then (LOC1, 𝑠 1, ℎ 1 +ℎ 1′ ) |= 𝜑 2 . We show that (LOC2, 𝑠 2, ℎ 2 ) |= 𝜑 1 −∗𝜑 2 , which
      is true whenever for all ℎ 2′ , if ℎ 2′ ⊥ℎ 2 and (LOC2, 𝑠 2, ℎ 2′ ) |= 𝜑 1 then (LOC2, 𝑠 2, ℎ 2 + ℎ 2′ ) |= 𝜑 2 .
      Consider a heap ℎ 2′ such that ℎ 2′ ⊥ℎ 2 and (LOC2, 𝑠 2, ℎ 2′ ) |= 𝜑 1 . By recalling that 𝔣 is a bijection
      from LOC1 to LOC2 , we construct the heap ℎ 1′ = 𝔣−1 (ℎ 2′ ). Directly from the fact that 𝔣 is a
      𝑋 -isomorphism between (LOC1, 𝑠 1, ℎ 1 ) and (LOC2, 𝑠 2, ℎ 2 ), it is easy to see that the following
      two properties hold:
    (1) (LOC1, 𝑠 1, ℎ 1′ ) ≈𝑋 (LOC2, 𝑠 2, ℎ 2′ ) and 𝔣 is an 𝑋 -isomorphism between the two structures.
    (2) ℎ 1′ ⊥ℎ 1 , from (1) together with (LOC1, 𝑠 1, ℎ 1′ ) ≈𝑋 (LOC2, 𝑠 2, ℎ 2′ ), ℎ 2′ ⊥ℎ 2 and 𝔣−1 (ℎ 2′ ) = ℎ 1′ .
      By the induction hypothesis, from (1) we conclude that (LOC1, 𝑠 1, ℎ 1′ ) |= 𝜑 1 . Then, from
      (2) and the initial hypothesis (LOC1, 𝑠 1, ℎ 1 ) |= 𝜑 1 −∗ 𝜑 2 , we obtain that (LOC1, 𝑠 1, ℎ 1 + ℎ 1′ )

                                        ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:8                                                   Stéphane Demri, Etienne Lozes, and Alessio Mansutti

     satisfies 𝜑 2 . By definition 𝔣(ℎ 1 + ℎ 1′ ) = 𝔣(ℎ 1 ) + 𝔣(𝔣−1 (ℎ 2′ )) = ℎ 2 + ℎ 2′ and therefore by the
     induction hypothesis, we get (LOC2, 𝑠 2, ℎ 2 + ℎ 2′ ) |= 𝜑 2 . Thus, (LOC2, 𝑠 2, ℎ 2 ) |= 𝜑 1 −∗ 𝜑 2 .
induction step: case with ∀. If (LOC1, 𝑠 1, ℎ 1 ) |= ∀x 𝜑 1 , then (LOC1, 𝑠 1 [x ← ℓ], ℎ 1 ) |= 𝜑 1 holds
     for all ℓ ∈ LOC1 . We prove that (LOC2, 𝑠 2, ℎ 2 ) |= ∀x 𝜑 1 , which is true whenever for ev-
     ery ℓ ′ ∈ LOC2 , (LOC2, 𝑠 2 [x ← ℓ ′], ℎ 2 ) |= 𝜑 1 . Notice that x ∉ 𝑋 since 𝑋 contains only
     the free variables in ∀x 𝜑 1 . Let ℓ ′ be a location in LOC2 . We have 𝔣−1 (ℓ ′) ∈ LOC1 and
     (LOC1, 𝑠 1 [x ← 𝔣−1 (ℓ ′)], ℎ 1 ) |= 𝜑 1 . From (LOC1, 𝑠 1, ℎ 1 ) ≈𝑋 (LOC2, 𝑠 2, ℎ 2 ) and x ∉ 𝑋 , we derive
     𝔣(ℎ 1 ) = ℎ 2 and for every y ∈ 𝑋 , 𝔣(𝑠 1 [x ← 𝔣−1 (ℓ ′)] (y)) = 𝔣(𝑠 1 (y)) = 𝑠 2 (y) = 𝑠 2 [x ← ℓ ′] (y).
     Thus, (LOC1, 𝑠 1 [x ← 𝔣−1 (ℓ ′)], ℎ 1 ) ≈𝑋 ∪{x} (LOC2, 𝑠 2 [x ← ℓ ′], ℎ 2 ). Using the induction hy-
     pothesis, we derive (LOC2, 𝑠 2 [x ← ℓ ′], ℎ 2 ) |= 𝜑 1 . Consequently, (LOC2, 𝑠 2, ℎ 2 ) |= ∀x 𝜑 1 . □
   As a direct consequence, satisfiability in SL(∗, −∗, ls) as defined in Section 2, is equivalent to
satisfiability with generalised memory states, the same holds for SL(∀, −∗). Indeed, suppose that
𝜑 is satisfiable in the memory state (𝑠, ℎ), then 𝜑 is satisfiable with the generalised semantics by
considering the model (N, 𝑠, ℎ). Similarly, suppose that 𝜑 is satisfiable in the generalised memory
state (LOC1, 𝑠 1, ℎ 1 ). As LOC1 is countably infinite, there is a bijection 𝔣 : LOC1 → N. Let (𝑠, ℎ) such
                                                 def
that 𝔣(ℎ 1 ) = ℎ and for every x ∈ PVAR, 𝑠 (x) = 𝔣(𝑠 1 (x)). Let 𝑋 be the set of free variables occurring
in 𝜑. By construction of (𝑠, ℎ), we have (LOC1, 𝑠 1, ℎ 1 ) ≈𝑋 (N, 𝑠, ℎ). By Lemma 3.3, we conclude
(N, 𝑠, ℎ) |= 𝜑, which is equivalent to (𝑠, ℎ) |= 𝜑.

3.2    Encoding quantified variables as cells in the heap
In this section, we introduce three additional atomic predicates that allow us to encode the first-order
quantification of SL(∀, ∗, −∗) as memory updates of SL(∗, −∗, ls):
                              alloc−1 (x),          𝑛(x) = 𝑛(y),         𝑛(x) ↩→ 𝑛(y).
The characterisation of these predicates in terms of formulae in SL(∗, −∗, ls) is given in Section 3.4.
For the time being, we simply assume that they can be defined in the logic, and work following
their semantics, given below:
          (𝑠, ℎ) |= alloc−1 (x)   ⇐⇒ 𝑠 (x) ∈ ran(ℎ).
          (𝑠, ℎ) |= 𝑛(x) = 𝑛(y)   ⇐⇒ {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ) and ℎ(𝑠 (x)) = ℎ(𝑠 (y)).
          (𝑠, ℎ) |= 𝑛(x) ↩→ 𝑛(y) ⇐⇒ {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ) and ℎ 2 (𝑠 (x)) = ℎ(𝑠 (y)).
In other words, alloc−1 (x) holds in (𝑠, ℎ) whenever 𝑠 (x) has a predecessor in ℎ. The satisfaction
of 𝑛(x) = 𝑛(y) corresponds to the existence of the following pattern in the memory state (𝑠, ℎ):
                                            𝑠 (x)                      𝑠 (y)
whereas the satisfaction of 𝑛(x) ↩→ 𝑛(y) corresponds to the existence of the following pattern:
                                                    𝑠 (x)
                                                    𝑠 (y)
As a rule of thumb, ‘𝑛(x)’ in 𝑛(x) = 𝑛(y) or in 𝑛(x) ↩→𝑛(y) refers to the “next” value of x understood
as ℎ(𝑠 (x)) – if it exists. Let us first intuitively explain how the two last predicates will help encoding
SL(∀, −∗). By definition, the satisfaction of the quantified formula ∀x 𝜓 from SL(∀, −∗) requires the
satisfaction of the formula 𝜓 for all the values ℓ in LOC assigned to x. The principle of the encoding
is to use a value 𝑠 (x) not in the domain or range of the heap to mimic the store by modifying how
𝑠 (x) is allocated: typically ‘x takes the value ℓ” is encoded by the heap {𝑠 (x) ↦→ ℓ } where 𝑠 (x) is
not in the range and domain of the heap. Figure 3 intuitively depicts this encoding, highlighting
how the store of the memory state in Figure 2 can be simulated directly by the heap. As showed in
this picture, the principle of the encoding is to use a set 𝐿 of locations initially not in the domain or

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                  1:9




                    x1                                                                      x1




                                                                    locations reserved to
                                                                      simulate the store
                    x2                                                                      x2

                           x3
                                                                                            x3




               Fig. 2. A memory state.                       Fig. 3. Simulating the store with the heap.


range of the heap to mimic the store by modifying how they are allocated. In this way, a variable
will be interpreted by a location in the heap and, instead of checking whether x ↩→ y (or x = y)
holds, we will check if 𝑛(x) ↩→ 𝑛(y) (or 𝑛(x) = 𝑛(y)) holds, where x and y correspond, after the
translation, to the locations in 𝐿 that mimic the store for those variables.
   Let 𝑋 be the finite set of variables needed for the translation. To properly encode the store,
each location in 𝐿 only mimics exactly one variable, i.e. there is a bijection between 𝑋 and 𝐿, and
cannot be reached by any location. Afterwards, the universal quantification for the quantifier ∀ is
simulated by means of the separating implication −∗: the formula ∀x 𝜓 will be encoded by a formula
of the form
                            (alloc(x) ∧ size = 1) −∗ (Safe(𝑋 ) ⇒ T(𝜓 )),
where Safe(𝑋 ) (formally defined below) checks whether the locations in 𝐿 still satisfy the auxiliary
conditions just described, i.e. locations in 𝐿 are not reached by other locations, whereas T(𝜓 ) is the
translation of 𝜓 . So, as hinted earlier, the above formula universally quantifies over the addition
of all subheaps of the form {𝑠 (x) ↦→ ℓ }. The locations in 𝐿 play a special role and this shall be
specified with the formula Safe(𝑋 ).
   The formula 𝜓 1 −∗ 𝜓 2 cannot simply be translated into T(𝜓 1 ) −∗ (Safe(𝑋 ) ⇒ T(𝜓 2 )) because
the evaluation of T(𝜓 1 ) in a disjoint heap may need the values of free variables occurring in 𝜓 1
but our encoding of the variable valuations via the heap does not allow to preserve these values
through disjoint heaps. In order to solve this problem, for each variable x in the formula, 𝑋 will
contain an auxiliary variable x, or alternatively we define on 𝑋 an involution (.). If the translated
formula has 𝑞 variables then the set 𝑋 of variables needed for the translation will have cardinality
2𝑞. Roughly speaking, in the translation of a formula whose outermost connective is the magic
wand, the locations corresponding to variables of the form x will be allocated on the left side of the
magic wand, and checked to be equal to their non-bar versions on the right side of the magic wand.
   Let us formalise the intuition of using part of the memory to mimic the store depicted in Figure 3,
by defining a suitable encoding between generalised memory states.
  Definition 3.4. Let 𝑋 ⊆ 𝑌 be finite sets of program variables. Let (LOC1, 𝑠 1, ℎ 1 ) and (LOC2, 𝑠 2, ℎ 2 )
be two (generalised) memory states. We say that (LOC1, 𝑠 1, ℎ 1 ) is encoded by (LOC2, 𝑠 2, ℎ 2 ) with
respect to 𝑋 and 𝑌 , written (LOC1, 𝑠 1, ℎ 1 ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 ), if the following conditions hold:
  (1) LOC1 = LOC2 \ {𝑠 2 (x) | x ∈ 𝑌 },
  (2) for all x ≠ y ∈ 𝑌 , 𝑠 2 (x) ≠ 𝑠 2 (y),
  (3) ℎ 2 = ℎ 1 + {𝑠 2 (x) ↦→ 𝑠 1 (x) | x ∈ 𝑋 }.

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:10                                                     Stéphane Demri, Etienne Lozes, and Alessio Mansutti

   Notice that the heap ℎ 2 is equal to the heap ℎ 1 augmented with the heap {𝑠 2 (x) ↦→ 𝑠 1 (x) | x ∈ 𝑋 }.
From the encoding, we can retrieve the initial heap by removing the memory cells corresponding
to variables in 𝑋 . By way of example, notice how the memory state in Figure 2 satisfies the formula
x3 ↩→ x2 , whereas its encoding in Figure 3 satisfies the formula 𝑛(x3 ) ↩→ 𝑛(x2 ). Furthermore, notice
that the memory state in Figure 3 satisfies the formula
Safe({x1, x2, x3 }) = x1 ≠ x2 ∧ x2 ≠ x3 ∧ x1 ≠ x3 ∧ ¬alloc−1 (x1 ) ∧ ¬alloc−1 (x2 ) ∧ ¬alloc−1 (x3 ).
This formula guarantees that the memory states are encodings of other memory states (in particular,
the one in Figure 2). In general, we write Safe(𝑌 ) for the following formula:
                                     def
                                         Û             Û
                            Safe(𝑌 ) = ( x ≠ y) ∧ ( ¬alloc−1 (x)).
                                              distinct x,y∈𝑌       x∈𝑌

3.3      The translation
We are now ready to define the translation of a first-order formula in quantifier-free separation
logic extended with the three predicates introduced at the beginning of the section. Let 𝜑 be a
closed formula of SL(∀, −∗) with quantified variables 𝑋 = {x1, . . . , x𝑞 }. Without loss of generality,
we can assume that 𝜑 is well-quantified, i.e. distinct quantifications involve distinct variables. We
consider a set 𝑌 = {x1, . . . , x2𝑞 } and (.) to be the (unique) involution on 𝑌 such that for all 𝑖 ∈ [1, 𝑞],
   def
x𝑖 = x𝑖+𝑞 . Notice that x𝑖+𝑞 = x𝑖 . We extend the involution to arbitrary subsets of 𝑌 , so that in
particular 𝑋 = {x𝑞+1, . . . , x2𝑞 } and 𝑋 = 𝑋 .
   The translation function T(𝜓, 𝑌 ) has two arguments: the formula 𝜓 in SL(∀, −∗) to be recursively
translated, and the total set of variables potentially appearing in the target formula, i.e. 𝑌 . The
translation function is given below, assuming that the variables in 𝜓 are either included in 𝑋 or
included 𝑋 .
                                       def
                       T(x𝑖 = x 𝑗 , 𝑌 ) = 𝑛(x𝑖 ) = 𝑛(x 𝑗 )
                                       def
                      T(x𝑖 ↩→ x 𝑗 , 𝑌 ) = 𝑛(x𝑖 ) ↩→ 𝑛(x 𝑗 )
                                       def
                            T(¬𝜓, 𝑌 ) = ¬T(𝜓, 𝑌 )
                                       def
                       T(𝜓 1 ∧ 𝜓 2, 𝑌 ) = T(𝜓 1, 𝑌 ) ∧ T(𝜓 2, 𝑌 )
                                       def
                         T(∀x𝑖 𝜓, 𝑌 ) = (alloc(x𝑖 ) ∧ size = 1) −∗ (Safe(𝑌 ) ⇒ T(𝜓, 𝑌 ))
Lastly, the translation T(𝜓 1 −∗ 𝜓 2, 𝑌 ) is defined as
             Û                   Û                                                
                  alloc(z)) ∧ ( ¬alloc(z)) ∧ Safe(𝑌 ) ∧ T(𝜓 1 [x ← x | x ∈ 𝑌 ], 𝑌 ) −∗
                z∈𝑍                  z∈𝑌 \𝑍
                Û                                        Û                                              
           ((       𝑛(z) = 𝑛(z)) ∧ Safe(𝑌 )) ⇒ ((              alloc(z) ∧ size = card(𝑍 )) ∗ T(𝜓 2, 𝑌 )) ,
             z∈𝑍                                         z∈𝑍
where 𝑍 is the set of free variables in 𝜓 1 , and 𝜓 1 [x ← x | x ∈ 𝑌 ] denotes the formula obtained from
𝜓 1 by replacing simultaneously all the variables x ∈ 𝑌 by x.
  Example 3.5. Assume that 𝑞 = 2, and therefore 𝑌 = {x1, x2, x3, x4 }. We have x1 = x3 and x2 = x4 .
Thus, the translation T(x1 ↩→ x2 −∗ x1 ↩→ x2, 𝑌 ) is defined as the formula below:
     
       (alloc(x3 ) ∧ alloc(x4 ) ∧ ¬alloc(x1 ) ∧ ¬alloc(x2 ) ∧ Safe(𝑌 ) ∧ 𝑛(x3 ) ↩→ 𝑛(x4 )) −∗
                                                                                                 
 (𝑛(x1 ) = 𝑛(x3 )∧𝑛(x2 ) = 𝑛(x4 )∧Safe(𝑌 )) ⇒ ((alloc(x3 )∧alloc(x4 )∧size = 2)∗𝑛(x1 ) ↩→ 𝑛(x2 )) .

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                  1:11

    Let us informally analyse the translation T(𝜓 1 −∗ 𝜓 2, 𝑌 ). It is a formula of the form 𝜓 1′ −∗ 𝜓 2′ where
𝜓 1 expresses the four constraints below (which follow the four conjuncts of 𝜓 1′, from left to right):
  ′

  (1) All the variables z with z ∈ 𝑍 are allocated.
  (2) None of the variables x with x ∈ 𝑌 \ 𝑍 is allocated.
  (3) The environment around the variables x ∈ 𝑌 is safe. In particular, none of the variables in 𝑌
      corresponds to a location that is pointed by another location.
  (4) Finally, one needs to guarantee that the translated formula T(𝜓 1, 𝑌 ) holds true when each
      variable x ∈ 𝑌 is replaced by its copy x, i.e. that T(𝜓 1 [x ← x | x ∈ 𝑌 ], 𝑌 ) holds.
Essentially, the formula 𝜓 1′ considers heaps satisfying T(𝜓 1, 𝑌 ), but with respect to the copies 𝑍 of
the free variables 𝑍 in 𝜓 1 . On these heaps, 𝜓 2′ checks whether the following two conditions hold
(antecedent of 𝜓 2′):
  (A) The values for z and z are equal for all z ∈ 𝑍 .
  (B) As in (3), the environment around the variables x ∈ 𝑌 is safe.
When these two conditions hold, 𝜓 2′ removes the assignments corresponding to the variables in 𝑍 ,
                  Ó
see subformula z∈𝑍 alloc(z) ∧ size = card(𝑍 ), and then check whether the formula T(𝜓 2, 𝑌 )
holds. Notice that freeing the variables in 𝑍 allows us to reuse them whenever a magic wand
appears in T(𝜓 2, 𝑌 ).
   Here is the main result of this section, that is the correctness of the translation T(𝜓, 𝑌 ).
  Lemma 3.6. Let 𝑌 = {x1, . . . , x2𝑞 } and 𝐸 be either {x1, . . . , x𝑞 } or {x1, . . . , x𝑞 } = {x𝑞+1, . . . , x2𝑞 }.
Let 𝑋 ⊆ 𝐸. Let 𝜓 be a well-quantified formula in SL(∀, −∗) with free variables among 𝑋 and bound
variables among 𝐸 \ 𝑋 . If (LOC1, 𝑠 1, ℎ 1 ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 ) then (𝑠 1, ℎ 1 ) |= 𝜓 iff (𝑠 2, ℎ 2 ) |= T(𝜓, 𝑌 ).

   The statement of Lemma 3.6, as well as its proof, refers to the involution (.) such that x𝑖 = x𝑖+𝑞 .
  Proof. The proof is by induction on the structure of 𝜓 . We start by proving the two base cases
with the atomic formulae x𝑖 = x 𝑗 and x𝑖 ↩→ x 𝑗 .
  (1) Let 𝜓 be x𝑖 = x 𝑗 . We have {x𝑖 , x 𝑗 } ⊆ 𝑋 ⊆ 𝑌 and T(𝜓, 𝑌 ) = 𝑛(x𝑖 ) = 𝑛(x 𝑗 ) by definition. The
      following equivalences hold.
                (𝑠 1, ℎ 1 ) |= x𝑖 = x 𝑗 ⇐⇒ 𝑠 1 (x𝑖 ) = 𝑠 1 (x 𝑗 ),
                                        ⇐⇒ ℎ 2 (𝑠 2 (x𝑖 )) = ℎ 2 (𝑠 2 (x 𝑗 )),       (Definition 3.4)
                                        ⇐⇒ (𝑠 2, ℎ 2 ) |= 𝑛(x𝑖 ) = 𝑛(x 𝑗 ).
  (2) Let 𝜓 be x𝑖 ↩→ x 𝑗 . We have {x𝑖 , x 𝑗 } ⊆ 𝑋 ⊆ 𝑌 and T(𝜓, 𝑌 ) = 𝑛(x𝑖 ) ↩→ 𝑛(x 𝑗 ) by definition.
      The following equivalences hold.
            (𝑠 1, ℎ 1 ) |= x𝑖 ↩→ x 𝑗 ⇐⇒ ℎ 1 (𝑠 1 (x𝑖 )) = 𝑠 1 (x 𝑗 ),
                                        ⇐⇒ ℎ 2 (ℎ 2 (𝑠 2 (x𝑖 ))) = ℎ 2 (𝑠 2 (x 𝑗 )),   (Definition 3.4)
                                        ⇐⇒ (𝑠 2, ℎ 2 ) |= 𝑛(x𝑖 ) ↩→ 𝑛(x 𝑗 ).
We now consider the induction step and we distinguish the different cases depending on the
outermost connective. To be precise, we assume the induction hypothesis to be the following:
   Let 𝑁 ∈ N. Let 𝐸 be either {x1, . . . , x𝑞 } or {x1, . . . , x𝑞 } = {x𝑞+1, . . . , x2𝑞 }. Let 𝑋 ⊆ 𝐸. Let 𝜑 be a
   well-quantified formula in SL(∀, −∗) with free variables among 𝑋 , bound variables among 𝐸 \𝑋 ,
   and size at most 𝑁 . If (LOC1, 𝑠 1, ℎ 1 ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 ) then (𝑠 1, ℎ 1 ) |= 𝜑 iff (𝑠 2, ℎ 2 ) |= T(𝜑, 𝑌 ).
In the induction step, we take a formula 𝜓 of size 𝑁 + 1. We omit the obvious cases for the Boolean
connectives. We now prove the result for ∀x𝑖 𝜑 and 𝜑 1 −∗ 𝜑 2 .
   (3) Let 𝜓 = ∀ x𝑖 𝜑 with x𝑖 ∈ 𝐸 \ 𝑋 and therefore by definition
                    T(∀ x𝑖 𝜑, 𝑌 ) = (alloc(x𝑖 ) ∧ size = 1) −∗ (Safe(𝑌 ) ⇒ T(𝜑, 𝑌 )).

                                     ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:12                                                    Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       By definition, (𝑠 1, ℎ 1 ) |= ∀x𝑖 𝜑 if and only if for all locations ℓ ∈ LOC1 , (𝑠 1 [x𝑖 ← ℓ], ℎ 1 ) |= 𝜑.
       Let us now consider the generalised memory state (LOC2, 𝑠 2, ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ }). Since
       x𝑖 ∉ 𝑋 , the heap ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ } is well-defined. From (LOC1, 𝑠 1, ℎ 1 ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 ) and
       by Definition 3.4, we obtain
                       (LOC1, 𝑠 1 [x𝑖 ← ℓ], ℎ 1 ) ▷𝑌𝑋 ∪{x𝑖 } (LOC2, 𝑠 2, ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ }).
       We apply the induction hypothesis, and conclude that:
                            for all ℓ ∈ LOC1 , (𝑠 1 [x𝑖 ← ℓ], ℎ 1 ) |= 𝜑,
                        iff for all ℓ ∈ LOC1 , (𝑠 2, ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ }) |= T(𝜑, 𝑌 ).
       Moreover, due to the fulfilment of the conditions in ▷𝑌𝑋 ∪{x𝑖 } , any memory state (𝑠 2, ℎ 2 +
       {𝑠 2 (x𝑖 ) ↦→ ℓ ′ }) satisfies Safe(𝑌 ) if and only if ℓ ′ ∈ LOC1 . Therefore,
                               for all ℓ ∈ LOC1 , (𝑠 2, ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ }) |= T(𝜑, 𝑌 ),
                        iff for all ℓ ∈ LOC2 , (𝑠 2, ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ }) |= Safe(𝑌 ) ⇒ T(𝜑, 𝑌 ).
       Indeed, if ℓ ∈ LOC1 then Safe(𝑌 ) and T(𝜑, 𝑌 ) are both satisfied (for Safe(𝑌 ), remember
       that all locations in {𝑠 2 (y) | y ∈ 𝑋 } ∩ dom(ℎ 2 ) already point to elements of LOC1 , due to
       the fulfilment of the conditions in ▷𝑌𝑋 ), otherwise whenever ℓ ∈ LOC2 \ LOC1 the premise
       of the implication does not hold and therefore the formula is trivially satisfied. Observe
       that a memory state (𝑠 2, ℎ ′) satisfies alloc(x𝑖 ) ∧ size = 1 if and only if ℎ ′ is of the form
       {𝑠 2 (x𝑖 ) ↦→ ℓ ′′ }, for some ℓ ′′ ∈ LOC2 . Then, we conclude that
                               for all ℓ ∈ LOC2 , (𝑠 2, ℎ 2 + {𝑠 2 (x𝑖 ) ↦→ ℓ }) |= Safe(𝑌 ) ⇒ T(𝜑, 𝑌 ),
                        iff for all ℎ ′, if (ℎ ′⊥ℎ 2 and (𝑠 2, ℎ ′) |= alloc(x𝑖 ) ∧ size = 1)
                                  then (𝑠 2, ℎ 2 + ℎ ′) |= Safe(𝑋 ) ⇒ T(𝜑, 𝑌 )
                        iff (𝑠 2, ℎ 2 ) |= (alloc(x𝑖 ) ∧ size = 1) −∗ (Safe(𝑌 ) ⇒ T(𝜑, 𝑌 )).
   (4) Let 𝜓 = 𝜑 1 −∗𝜑 2 . Let 𝑍 be the set of free variables in 𝜑 1 . Below, we assume that for every x ∈ 𝑋 ,
       𝑠 1 (x) = 𝑠 1 (x). Notice that this assumption is without loss of generality, as 𝜓 is written with
       free variables among 𝑋 , where 𝑋 ∩ 𝑋 = ∅, and the memory state (𝑠 1 [x ← 𝑠 1 (x) | x ∈ 𝑋 ], ℎ 1 )
       is 𝑋 -isomorphic to (𝑠 1, ℎ 1 ), where 𝑠 1 [x ← 𝑠 1 (x) | x ∈ 𝑋 ] is the store obtained from 𝑠 1
       by assigning 𝑠 1 (x) to every variable x ∈ 𝑋 . By Lemma 3.3, (𝑠 1, ℎ 1 ) |= 𝜓 if and only if
       (𝑠 1 [x ← 𝑠 1 (x) | x ∈ 𝑋 ], ℎ 1 ) |= 𝜓 .
       (⇒): If (𝑠 1, ℎ 1 ) |= 𝜑 1 −∗ 𝜑 2 , then by definition, for all heaps ℎ 1′ , if ℎ 1′ ⊥ℎ 1 and (𝑠 1, ℎ 1′ ) |= 𝜑 1 , then
       we have (𝑠 1, ℎ 1 +ℎ 1′ ) |= 𝜑 2 . We show that (𝑠 2, ℎ 2 ) |= T(𝜑 1 −∗𝜑 2, 𝑌 ). By definition, T(𝜑 1 −∗𝜑 2, 𝑌 ),
       holds whenever for all heaps ℎ 2′ , if
       (A1) ℎ 2′ ⊥ℎ 2 ,         Û                      Û
       (A2) (𝑠 2, ℎ 2′ ) |= (       alloc(z)) ∧ (           ¬alloc(z)) ∧ Safe(𝑌 ) ∧ T(𝜑 1 [x ← x | x ∈ 𝑌 ], 𝑌 ),
                              z∈𝑍                    z∈𝑌 \𝑍
                                      Û
       (A3) (𝑠 2, ℎ 2 + ℎ 2′ ) |= (         𝑛(z) = 𝑛(z)) ∧ Safe(𝑌 ),
                                      z∈𝑍
       then                         Û
       (C1) (𝑠 2, ℎ 2 + ℎ 2′ ) |= (   alloc(z) ∧ size = card(𝑍 )) ∗ T(𝜑 2, 𝑌 ).
                                    z∈𝑍
       Let ℎ 2′ be some heap that satisfies the premises (A1)–(A3) of the implication. From (A3)
       together with (LOC1, 𝑠 1, ℎ 1 ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 ), which implies that for all x ∈ 𝑋 ⊇ 𝑍 , we have
       ℎ 2 (𝑠 2 (x)) = 𝑠 1 (x), we conclude that for all z ∈ 𝑍 , we have ℎ 2′ (𝑠 2 (z)) = 𝑠 1 (z). Moreover, (A2)
                                                                           def
       entails that ℎ 2′ can be written as ℎ𝑍 + ℎ 1′ where ℎ𝑍 = {𝑠 2 (z) ↦→ 𝑠 1 (z) | z ∈ 𝑍 } (ℎ 1′ is then
       defined as the unique subheap satisfying ℎ 2′ = ℎ𝑍 + ℎ 1′ , once ℎ𝑍 is defined). Observe that
       the domain of ℎ𝑍 is the set of locations in LOC2 that corresponds to variables in 𝑍 , and its

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                    1:13

      codomain is included in LOC1 . For ℎ 1′ instead, both its domain and codomain are included in
      LOC1 . By Definition 3.4 and the assumption that for all x ∈ 𝑋 , 𝑠 1 (x) = 𝑠 1 (x), it holds that
                                        (LOC1, 𝑠 1, ℎ 1′ ) ▷𝑌𝑍 (LOC2, 𝑠 2, ℎ 2′ ).
      Since 𝑍 is the set of free variables in 𝜑 1 , 𝑍 is the set of free variables in 𝜑 1 [x ← x | x ∈ 𝑌 ]. From
      (𝑠 2, ℎ 2′ ) |= T(𝜑 1 [x ← x | x ∈ 𝑌 ], 𝑌 ), we apply the induction hypothesis and conclude that
      (𝑠 1, ℎ 1′ ) |= 𝜑 1 [x ← x | x ∈ 𝑌 ]. Again thanks to the assumption that for all x ∈ 𝑋 , 𝑠 1 (x) = 𝑠 1 (x),
      this allows us to conclude that (𝑠 1, ℎ 1′ ) |= 𝜑 1 . Indeed, this holds directly from the well-known
      axiom of separation logic x = y ∧ 𝜑 =⇒ 𝜑 [x ← y] (see e.g. [19]). Since ℎ 1′ ⊑ ℎ 2′ , ℎ 1 ⊑ ℎ 2 and
      ℎ 2′ ⊥ℎ 2 (A1), the property ℎ 1′ ⊥ℎ 1 holds and therefore, by the assumption (𝑠 1, ℎ 1 ) |= 𝜑 1 −∗ 𝜑 2 , we
      get (𝑠 1, ℎ 1 + ℎ 1′ ) |= 𝜑 2 . As such, since (LOC1, 𝑠 1, ℎ 1 + ℎ 1′ ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 + ℎ 1′ ) holds because
      ℎ 1′ has domain and codomain included in LOC1 and is a subset of ℎ 2′ which is disjoint from ℎ 2 ,
      we can use the induction hypothesis and obtain that (𝑠 2, ℎ 2 + ℎ 1′ ) |= T(𝜑 2, 𝑌 ). Together with
      ℎ 2′ = ℎ 1′ + ℎ𝑍 and (𝑠 2, ℎ𝑍 ) |= z∈𝑍 alloc(z) ∧ size = card(𝑍 ), this allows us to derive (C1).
                                           Ó
      (⇐): For the other direction, suppose that (𝑠 2, ℎ 2 ) |= T(𝜑 1 −∗ 𝜑 2, 𝑌 ). This means that for all
      heaps ℎ 2′ if (A1)-(A3) holds, then (C1) holds. Let us prove that (𝑠 1, ℎ 1 ) |= 𝜑 1 −∗ 𝜑 2 , which by
      definition holds whenever for all heaps ℎ 1′ , if ℎ 1′ ⊥ℎ 1 and (𝑠 1, ℎ 1′ ) |= 𝜑 1 then (𝑠 1, ℎ 1 + ℎ 1′ ) |= 𝜑 2 .
                                                                                     def
      Let ℎ 1′ be a heap disjoint from ℎ 1 satisfying (𝑠 1, ℎ 1′ ) |= 𝜑 1 . Let ℎ 2′ = ℎ 1′ +{𝑠 2 (z) ↦→ 𝑠 1 (z) | z ∈ 𝑍 }.
      By definition of ▷𝑌𝑋 together with the assumption that for all x ∈ 𝑋 , 𝑠 1 (x) = 𝑠 1 (x), we have
                                        (LOC1, 𝑠 1, ℎ 1′ ) ▷𝑌𝑍 (LOC2, 𝑠 2, ℎ 2′ ).
      By the induction hypothesis, we get (𝑠 2, ℎ 2′ ) |= T(𝜑 1 [x ← x | x ∈ 𝑌 ], 𝑌 ), whereas from the
      definition of ▷𝑌𝑍 , it holds that (𝑠 2, ℎ 2′ ) satisfies
                               Û                      Û
                              ( alloc(z)) ∧ ( ¬alloc(z)) ∧ Safe(𝑌 ).
                                z∈𝑍                     z∈𝑋 \𝑍

      Thus, (A2) holds. Besides this, ℎ 2 can be written as ℎ 1 + {𝑠 2 (y) ↦→ 𝑠 1 (y) | y ∈ 𝑋 } (condition
      (3) in Definition 3.4). Consequently, (A1) holds and the heap ℎ 2 + ℎ 2′ can be written as
                     ℎ 1 + ℎ 1′ + {𝑠 2 (x) ↦→ 𝑠 1 (x) | x ∈ 𝑋 } + {𝑠 2 (z) ↦→ 𝑠 1 (z) | z ∈ 𝑍 }.
                                                               ′                     ′
      Therefore, it holds
                    ′       Ó that for all z ∈ 𝑍 , (ℎ 2 + ℎ 2 ) (𝑠 2 (z)) = (ℎ 2 + ℎ 2 ) (𝑠 2 (z)) or, equivalently,
      (𝑠 2, ℎ 2 + ℎ 2 ) |= z∈𝑍 𝑛(z) = 𝑛(z). Indeed, 𝑍 ⊆ 𝑋 , z ∈ 𝑍 , and, 𝑠 2 (z) and 𝑠 2 (z) point to the
      same location. Furthermore, (𝑠 2, ℎ 2 + ℎ 2′ ) also satisfies Safe(𝑌 ). (A3) holds and thus so does
      (C1), i.e.
                                                 Û
                         (𝑠 2, ℎ 2 + ℎ 2′ ) |= (   alloc(z) ∧ size = card(𝑍 )) ∗ T(𝜑 2, 𝑌 ).
                                           z∈𝑍
      Again, ℎ 2 +ℎ 2′ can be written as ℎ 1 +ℎ 1′ +{𝑠 2 (x) ↦→ 𝑠 1 (x) | x ∈ 𝑋 }+{𝑠 2 (z) ↦→ 𝑠 1 (z) | z ∈ 𝑍 }, and
                     Ó
      the formula z∈𝑍 alloc(z) ∧ size = card(𝑍 ) can be only satisfied by the memory state with
      the heap {𝑠 2 (z) ↦→ 𝑠 1 (z) | z ∈ 𝑍 }. Consequently, ℎ 2 + ℎ 1′ = ℎ 1 + ℎ 1′ + {𝑠 2 (x) ↦→ 𝑠 1 (x) | y ∈ 𝑋 }
      is such that (𝑠 2, ℎ 2 + ℎ 1′ ) |= T(𝜑 2, 𝑌 ). Lastly, since (LOC1, 𝑠 1, ℎ 1 + ℎ 1′ ) ▷𝑌𝑋 (LOC2, 𝑠 2, ℎ 2 + ℎ 1′ ),
      we can use the induction hypothesis to conclude that (𝑠, ℎ 1 + ℎ 1′ ) |= 𝜑 2 .                                  □
   Let 𝜑 be a formula of SL(∀, −∗) written with variables among {x1, . . . , x𝑞 }. We define the trans-
lation TSAT (𝜑) into SL(∗, −∗, ls) augmented with the new predicates where T(𝜑, 𝑌 ) is defined
recursively as before ( 𝑌 = {x1, . . . , x2𝑞 }).
                                   def
                                          Û
                         TSAT (𝜑) = ( ¬alloc(x𝑖 )) ∧ Safe(𝑌 ) ∧ T(𝜑, 𝑌 ).
                                          𝑖 ∈ [1,2𝑞 ]


                                      ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:14                                                    Stéphane Demri, Etienne Lozes, and Alessio Mansutti

The first two conjuncts specify initial conditions, namely each variable x in 𝑌 is interpreted by a
location that is unallocated, it is not in the heap range and it is distinct from the interpretation of
all other variables; in other words, the value for x is isolated. Similarly, let TVAL (𝜑) be the formula
in SL(∗, −∗, ls) defined by
                                  def
                                       Û
                         TVAL (𝜑) = (( ¬alloc(x𝑖 )) ∧ Safe(𝑌 )) ⇒ T(𝜑, 𝑌 ).
                                          𝑖 ∈ [1,2𝑞 ]

As a consequence of Lemma 3.6, 𝜑 and TSAT (𝜑) are shown equisatisfiable, whereas 𝜑 and TVAL (𝜑)
are shown equivalid.
   Corollary 3.7. Let 𝜑 be a closed formula in SL(∀, −∗) using quantified variables among {x1, . . . , x𝑞 }.
        (I) 𝜑 and TSAT (𝜑) are equisatisfiable.           (II) 𝜑 and TVAL (𝜑) are equivalid.
    Proof. (I) First, suppose that 𝜑 is satisfiable, i.e. there is a memory state (𝑠, ℎ) such that (𝑠, ℎ) |= 𝜑.
It is then easy to define a generalised memory state (LOC\{1, . . . , 2𝑞}, 𝑠 ′, ℎ ′) isomorphic with respect
to the empty set to (𝑠, ℎ) (i.e., using the equivalence relation ≈ ∅ ) and satisfying 𝜑 by Lemma 3.3.
Typically, to define (𝑠 ′, ℎ ′) from (𝑠, ℎ), it is sufficient to shift all the values with an offset equal to 2𝑞+1.
Now, let (LOC, 𝑠 ′′, ℎ ′′) be the generalised memory state such                     ′′      ′
                                                                          Ó that ℎ = ℎ , and for all 𝑖 ∈ [1, 2𝑞],
               ′′                                           ′′   ′′
we have 𝑠 (x𝑖 ) = 𝑖. One can check that (LOC, 𝑠 , ℎ ) |= ( 𝑖 ∈ [1,2𝑞 ] ¬alloc(x𝑖 )) ∧ Safe(𝑌 ) with
𝑌 = {x1, . . . , x2𝑞 }. Moreover, (LOC \ {1, . . . , 2𝑞}, 𝑠 ′, ℎ ′) ▷𝑌∅ (LOC, 𝑠 ′′, ℎ ′′). By Lemma 3.6, we have
(𝑠 ′′, ℎ ′′) |= T(𝜑, 𝑌 ). So, (𝑠 ′′, ℎ ′′) |= TSAT (𝜑).
    Conversely, suppose that (𝑠, ℎ) |= TSAT (𝜑). Let (LOC′, 𝑠 ′, ℎ ′) be the generalised memory state
defined as follows:
    (1) LOC′ = LOC \ {𝑠 (x) | x ∈ 𝑌 },
    (2) the heap ℎ ′ is equal to the restriction of ℎ to locations in LOC′.
Since (𝑠, ℎ) |= Safe(𝑌 ) and by construction of (LOC′, 𝑠 ′, ℎ ′), we have
                                           (LOC′, 𝑠 ′, ℎ ′) ▷𝑌∅ (LOC, 𝑠, ℎ).
As (𝑠, ℎ) |= T(𝜑, 𝑌 ), by Lemma 3.6, we get (LOC′, 𝑠 ′, ℎ ′) |= 𝜑. Now, note that LOC′ ⊆ LOC and
therefore we also have (LOC, 𝑠 ′, ℎ ′) |= 𝜑, where (LOC, 𝑠 ′, ℎ ′) is understood as a standard memory
state (𝑠 ′, ℎ ′).
(II) Similar to (I).                                                                                □

3.4    Expressing the auxiliary atomic predicates
To complete the reduction, we explain how to express the formulae alloc−1 (x), 𝑛(x) = 𝑛(y) and
𝑛(x) ↩→ 𝑛(y) within SL(∗, −∗, ls). Let us introduce a few macros that shall be helpful.
    • Given 𝜑 in SL(∗, −∗, reach+ ) and 𝛾 ≥ 0, we write [𝜑]𝛾 to denote the formula (size = 𝛾 ∧ 𝜑) ∗ ⊤.
      It is easy to show that for any memory state (𝑠, ℎ), we have (𝑠, ℎ) |= [𝜑]𝛾 iff there is ℎ ′ ⊑ ℎ
      such that card(dom(ℎ ′)) = 𝛾 and (𝑠, ℎ ′) |= 𝜑. Such formulae [𝜑]𝛾 can be used to ensure that
      the minimum path between two locations interpreted by program variables is of length 𝛾.
    • We write reach(x, y) = 𝛾 to denote the formula [ls(x, y)]𝛾 , which is satisfied in any memory
      state (𝑠, ℎ) where ℎ𝛾 (𝑠 (x)) = 𝑠 (y) andÔ𝛾 is minimal (no cycles allowed). Lastly, we write
      reach(x, y) ≤ 𝛾 to denote the formula 0≤𝛾 ′ ≤𝛾 reach(x, y) = 𝛾 ′.
In order to define the existence of a predecessor (i.e. alloc−1 (x)) in SL(∗, −∗, ls), we need to take
advantage of an auxiliary variable y whose value is different from the one for x. Let alloc−1y (x) be
the formula
          x ↩→ x ∨ y ↩→ x ∨ (⊤ ∗ ((alloc(y) ∧ ¬(y ↩→ x) ∧ size = 1) −⊛ reach(y, x) = 2))

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                              1:15

  Lemma 3.8. Let x, y ∈ PVAR.
  (I) For all memory states (𝑠, ℎ), if 𝑠 (x) ≠ 𝑠 (y), then (𝑠, ℎ) |= alloc−1
                                                                          y (x) iff 𝑠 (x) ∈ ran(ℎ).
 (II) In the translation T(𝜑, 𝑌 ), alloc−1 (x) (with x ∈ 𝑌 ) can be replaced with alloc−1   x
                                                                                              (x).
  As stated in Lemma 3.8(II), we can exploit the fact that in the translation of a formula with
variables in {x1, . . . , x𝑞 }, we use 2𝑞 variables that correspond to 2𝑞 distinguished locations in the
heap in order to retain the soundness of the translation while using allocx−1 (x) as alloc−1 (x).

  Proof. For (I), (⇒): Suppose that (𝑠, ℎ) |= alloc−1
                                                   y (x). If (𝑠, ℎ) satisfies either x ↩→ x or y ↩→ x,
then obviously 𝑠 (x) ∈ ran(ℎ). Otherwise, (𝑠, ℎ) must satisfy the third conjunct of alloc−1 y (x):

                      (𝑠, ℎ) |= ⊤ ∗ ((alloc(y) ∧ size = 1) −⊛ reach(y, x) = 2).
In this case, (𝑠, ℎ ′) |= (alloc(y) ∧ size = 1) −⊛ reach(y, x) = 2 holds for some heap ℎ ′ ⊑ ℎ. From
the semantics of the septraction operator, there is a heap ℎ ′′ disjoint from ℎ ′ and such that
      (1) 𝑠 (y) ∈ dom(ℎ ′′),        (2) card(ℎ ′′) = 1,          (3) (𝑠, ℎ ′ + ℎ ′′) |= reach(y, x) = 2.
From (1) and ℎ ′′ ⊥ ℎ ′, we conclude that 𝑠 (y) ∉ dom(ℎ ′). Now, (3) implies that there is a location ℓ
such that {𝑠 (y) ↦→ ℓ ↦→ 𝑠 (x)} ⊑ ℎ ′ + ℎ ′′, and moreover ℓ must be distinct from both 𝑠 (x) and 𝑠 (y)
(which are also assumed to be distinct). From (1) and (2), it must be that ℎ ′′ = {𝑠 (y) ↦→ ℓ } and
therefore {ℓ ↦→ 𝑠 (x)} ⊑ ℎ ′. From ℎ ′ ⊑ ℎ we then conclude that 𝑠 (x) ∈ ran(ℎ).
   (⇐): Suppose there is a location ℓ ∈ dom(ℎ) such that ℎ(ℓ) = 𝑠 (x) (i.e. 𝑠 (x) ∈ ran(ℎ)). First,
suppose that ℓ = 𝑠 (x) or ℓ = 𝑠 (y). In this case, we directly derive that (𝑠, ℎ) |= x ↩→ x∨y ↩→ x, which
in turn shows that (𝑠, ℎ) |= alloc−1  y (x). Otherwise, consider the case where ℓ ≠ 𝑠 (x) and ℓ ≠ 𝑠 (y).
Let ℎ ′ ⊑ ℎ be the heap {ℓ ↦→ 𝑠 (x)}. As ℓ ≠ 𝑠 (y), the location 𝑠 (y) is not a memory cell of ℎ ′. Let
us consider the heap ℎ ′′ = {𝑠 (y) ↦→ ℓ }, so that (𝑠, ℎ ′′) |= alloc(y) ∧ size = 1. The heaps ℎ ′
and ℎ ′′ are disjoint, and from their definition we have ℎ ′ + ℎ ′′ = {𝑠 (y) ↦→ ℓ ↦→ 𝑠 (x)}. As 𝑠 (x), ℓ
and 𝑠 (y) are all distinct locations, (𝑠, ℎ ′ + ℎ ′′) |= reach(y, x) = 2 holds, which in turn allows us to
conclude that (𝑠, ℎ ′) |= (alloc(y) ∧ size = 1) −⊛ reach(y, x) = 2. As ℎ ′ ⊑ ℎ, this implies that
(𝑠, ℎ) |= ⊤ ∗ ((alloc(y) ∧ size = 1) −⊛ reach(y, x) = 2), which implies (𝑠, ℎ) |= alloc−1       y (x).
   For (II), since by definition, x and x are interpreted by different locations, they satisfy the
additional hypothesis 𝑠 (x) ≠ 𝑠 (y) (where y = x). Therefore, we can use one of these two variables
to check if the other is in ran(ℎ). As such, instead of alloc−1 (x) we can use alloc−1        x
                                                                                                 (x) in the
translation.                                                                                              □
  Moreover, alloc−1
                  y (x) allows us to express in SL(∗, −∗, ls) whether a location corresponding to
a program variable reaches itself in exactly two steps (we use this property in the definition of
𝑛(x) ↩→ 𝑛(y)). We write x ↩→2y x to denote the formula
    ¬(x ↩→ x) ∧ (x ↩→ y ⇒ y ↩→ x) ∧ [alloc(x) ∧ alloc−1
                                                     y (x) ∧ (⊤ −∗ ¬reach(x, y) = 2)] 2 .

  Lemma 3.9. For any memory state (𝑠, ℎ) such that 𝑠 (x) ≠ 𝑠 (y), we have (𝑠, ℎ) |= x ↩→2y x if and
only if ℎ 2 (𝑠 (x)) = 𝑠 (x) and ℎ(𝑠 (x)) ≠ 𝑠 (x).
   Proof. So, let (𝑠, ℎ) be a memory state such that 𝑠 (x) is distinct from 𝑠 (y).
   First, we assume that ℎ 2 (𝑠 (x)) = 𝑠 (x) and ℎ(𝑠 (x)) ≠ 𝑠 (x). So, there is a location ℓ distinct from
𝑠 (x) such that ℎ(𝑠 (x)) = ℓ and ℎ(ℓ) = 𝑠 (x). Obviously, (𝑠, ℎ) |= ¬(x ↩→ x) as ℓ is distinct from 𝑠 (x).
Below, we distinguish two cases.
Case 1: ℓ ≠ 𝑠 (y). So, (𝑠, ℎ) |= ¬x ↩→ y and therefore (𝑠, ℎ) |= x ↩→ y ⇒ y ↩→ x. Let ℎ ′ be the sub-
       heap of ℎ with dom(ℎ ′) = {𝑠 (x), ℓ }. We have (𝑠, ℎ ′) |= alloc(x) and (𝑠, ℎ ′) |= alloc−1y (x) by

                                 ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:16                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

     Lemma 3.8(I). Moreover, for all heaps ℎ ′′ such that ℎ ′ ⊑ ℎ ′′, we have (𝑠, ℎ ′′) ̸ |= reach(x, y) = 2,
     as ℓ ∈ dom(ℎ ′) and ℎ ′ ⊑ ℎ ′′.
Case 2: ℓ = 𝑠 (y). So, (𝑠, ℎ) |= x ↩→ y∧y ↩→ x and therefore (𝑠, ℎ) |= x ↩→ y ⇒ y ↩→ x. Let ℎ ′ be the
     subheap of ℎ with dom(ℎ ′) = {𝑠 (x), ℓ }. We have (𝑠, ℎ) |= alloc(x) and (𝑠, ℎ) |= alloc−1    y (x) by
     Lemma 3.8(I). Moreover, for all heaps ℎ ′′ such that ℎ ′ ⊑ ℎ ′′, we have (𝑠, ℎ ′′) ̸ |= reach(x, y) = 2
     as (𝑠, ℎ ′′) |= x ↩→ y.
   So, in both cases, (𝑠, ℎ) |= [alloc(x) ∧ alloc−1y (x) ∧ (⊤ −∗ ¬reach(x, y) = 2)] 2 and therefore
(𝑠, ℎ) |= x ↩→2y x.
   Conversely, assume that (𝑠, ℎ) |= x ↩→2y x and let us show that 𝑠 (x) can reach itself in two steps
but not in one step.
Case 1: (𝑠, ℎ) |= x ↩→ y ∧ y ↩→ x. Let ℓ = 𝑠 (y). So, ℎ(𝑠 (x)) = ℓ, ℎ(ℓ) = 𝑠 (x), and ℓ ≠ 𝑠 (x). Hence,
     we are done.
Case 2: (𝑠, ℎ) |= ¬x ↩→ y. First, note that the case x ↩→ y ∧ ¬(y ↩→ x) is rule out because the
     memory state satisfies x ↩→ y ⇒ y ↩→ x. As (𝑠, ℎ) |= [alloc(x) ∧ alloc−1              y (x) ∧ (⊤ −∗
     ¬reach(x, y) = 2)] 2 , we conclude that (𝑠, ℎ) |= alloc(x) and therefore 𝑠 (x) ∈ dom(ℎ).
     Similarly, we can conclude that (𝑠, ℎ) |= alloc−1    y (x). Let ℓ = ℎ(𝑠 (x)) and by assumption
     ℓ is distinct from 𝑠 (y) and ℓ is different from 𝑠 (x), whence ℎ(𝑠 (x)) ≠ 𝑠 (x). Ad absurdum,
     suppose that either ℓ ∉ dom(ℎ) or ℎ(ℓ) ≠ 𝑠 (x). So, there is a location ℓ ′ distinct from ℓ
     such that ℎ(ℓ ′) = 𝑠 (x) (indeed, we have (𝑠, ℎ) |= alloc−1    y (x) and then use Lemma 3.8(I)).
     As (𝑠, ℎ) |= [alloc(x) ∧ alloc−1     y (x) ∧ (⊤ −∗ ¬reach(x,    y) = 2)] 2 , the only heap ℎ ′ with
     two memory cells satisfying (𝑠, ℎ ) |= alloc(x) ∧ alloc−1
                                            ′
                                                                     y (x) is the one with dom(ℎ ) =
                                                                                                    ′
                 ′                            ′                                           ′′
     {𝑠 (x), ℓ } and therefore ℓ ∉ dom(ℎ ), which is important at this point. Let ℎ be any heap
     disjoint from ℎ ′ such that ℎ ′′ (ℓ) = 𝑠 (y). We know such a heap exists as ℓ ∉ dom(ℎ ′). As
     𝑠 (x), ℓ and 𝑠 (y) are pairwise distinct, we get that (𝑠, ℎ ′′) |= reach(x, y) = 2 and therefore,
     (𝑠, ℎ ′) ̸ |= (⊤ −∗ ¬reach(x, y) = 2), which leads to a contradiction. Consequently, ℓ ∈ dom(ℎ)
     and ℎ(ℓ) = 𝑠 (x), so ℎ 2 (𝑠 (x)) = 𝑠 (x).                                                         □

   The predicate 𝑛(x) = 𝑛(y) can be defined in SL(∗, −∗, ls) as the formula ext(𝑛(x) = 𝑛(y)) (’ext’
stands for ’extension’)

            (x ≠ y ⇒ [alloc(x) ∧ alloc(y) ∧ ((x ↩→ y ∧ y ↩→ y) ∨ (y ↩→ x ∧ x ↩→ x)∨
            Û
          (( ¬(z ↩→ z′)) ∧ (⊤ −∗ ¬(reach(x, y) = 2 ∧ reach(y, x) = 2))))] 2 ) ∧ alloc(x)
         z,z′ ∈ {x,y}

  Lemma 3.10. Let x, y ∈ PVAR. For all memory states (𝑠, ℎ), we have (𝑠, ℎ) |= ext(𝑛(x) = 𝑛(y)) iff
ℎ(𝑠 (x)) = ℎ(𝑠 (y)).

   Proof. First, suppose ℎ(𝑠 (x)) = ℎ(𝑠 (y)). Then obviously (𝑠, ℎ) |= alloc(x) ∧ alloc(y). Suppose
𝑠 (x) ≠ 𝑠 (y). We need to show that (𝑠, ℎ) satisfies the formula

                    [alloc(x) ∧ alloc(y) ∧ ((x ↩→ y ∧ y ↩→ y) ∨ (y ↩→ x ∧ x ↩→ x)∨
                       Û
                     (( ¬z ↩→ z′) ∧ (⊤ −∗ ¬(reach(x, y) = 2 ∧ reach(y, x) = 2))))] 2
                    z,z′ ∈ {x,y}

Let ℎ ′ ⊑ ℎ be the two-memory-cells heap such that ℎ ′ (𝑠 (x)) = ℎ ′ (𝑠 (y)). In particular, dom(ℎ ′) =
{𝑠 (x), 𝑠 (y)} and therefore (𝑠, ℎ ′) |= alloc(x) ∧ alloc(y). Moreover, ℎ ′ is represented by one of the
following memory states.

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                    1:17

                         x                                    y                           x        y


                     y                                    x



Each memory state above satisfies one of the three disjuncts from the third conjunct of the above
formula. The first memory state satisfies x ↩→ y ∧ y ↩→ y, the second one satisfies y ↩→ x ∧ x ↩→ x
and the third one satisfies
                    Û
                   ( ¬z ↩→ z′) ∧ (⊤ −∗ ¬(reach(x, y) = 2 ∧ reach(y, x) = 2)).
                  z,z′ ∈ {x,y}

  The first two cases are trivial. The last one represents a memory state with a location ℓ such
               ′         ′
Ó ℓ = ℎ (𝑠 (x)) =′ ℎ (𝑠 (y)) and 𝑠 (x) ′′≠ ℓ ≠ 𝑠 (y). As such,
that
                                                               ′
                                                                     this memory state trivially satisfies
                                                                           ′  ′′
  z,z′ ∈ {x,y} ¬z ↩→ z . Now, consider ℎ disjoint from ℎ and (𝑠, ℎ + ℎ ) |= reach(x, y) = 2. In
particular, it must hold that ℎ (ℓ) = 𝑠 (y). As such, (ℎ + ℎ ) (𝑠 (y)) = 𝑠 (y)Óand so (𝑠, ℎ ′ + ℎ ′′) ̸ |=
                                   ′′                        ′    ′′  2

reach(y, x) = 2. It follows that the last memory state of the picture satisfies ( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧
(⊤ −∗ ¬(reach(x, y) = 2 ∧ reach(y, x) = 2)). Thus, ℎ(𝑠 (x)) = ℎ(𝑠 (y)) implies (𝑠, ℎ) |= ext(𝑛(x) =
𝑛(y)).
  Conversely, suppose (𝑠, ℎ) |= ext(𝑛(x) = 𝑛(y)). Then (𝑠, ℎ) |= alloc(x). If 𝑠 (x) = 𝑠 (y), ℎ(𝑠 (x)) =
ℎ(𝑠 (y)) follows trivially. Instead, if 𝑠 (x) ≠ 𝑠 (y), there must exist a two-memory-cells heap ℎ ′ ⊑ ℎ
                  ′
  Ó that (𝑠, ℎ ) satisfies
such                         alloc(x) ∧ alloc(y) ∧ ((x ↩→ y ∧ y ↩→ y) ∨ (y ↩→ x ∧ x ↩→ x) ∨
(( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧ (⊤ −∗ ¬(reach(x, y) = 2 ∧ reach(y, x) = 2)))). As such, 𝑠 (x) and 𝑠 (y) are
both in dom(ℎ ′). Trivially, if (𝑠, ℎ ′) |= (x ↩→ y∧y ↩→ y)∨(y ↩→ x∧x ↩→ x) then ℎ ′ (𝑠 (x)) = ℎ ′ (𝑠 (y)).
The same holds true if (𝑠, ℎ ′) |= ( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧ (⊤−∗¬(reach(x, y) = 2∧reach(y, x) = 2)).
                                      Ó
Indeed, (𝑠, ℎ ′) |= z,z′ ∈ {x,y} ¬z ↩→ z′ leaves open only two possible memory states, that are
                     Ó
represented below.

                                   x   y                                   x          y




The last part of the formula, ⊤ −∗ ¬(reach(x, y) = 2 ∧ reach(y, x) = 2) allows to differentiate these
two cases by excluding the left heap. Indeed, that very formula holds on (𝑠, ℎ ′) if and only if there
is no heap ℎ ′′ such that ℎ ′′⊥ℎ ′ and (𝑠, ℎ ′ + ℎ ′′) |= reach(x, y) = 2 ∧ reach(y, x) = 2. This property
holds on the right heap, as already discussed in the first part of the proof, but not on the left one, as
can be shown by defining ℎ ′′ as {ℎ ′ (𝑠 (x)) ↦→ 𝑠 (y), ℎ ′ (𝑠 (y)) ↦→ 𝑠 (x)}.                          □

  Similarly to alloc−1 (x), we can show that 𝑛(x) ↩→ 𝑛(y) is definable in SL(∗, −∗, ls) by using
one additional variable z whose value is different from both x and y. Let 𝜑 ↩→ (x, y, z) be (ext(𝑛(x) =
          = (x, y, z)) ∨ (¬ext(𝑛(x) = 𝑛(y)) ∧ 𝜑 ≠ (x, y)) where 𝜑 = (x, y, z) is defined as
𝑛(y)) ∧ 𝜑 ↩→                                    ↩→                ↩→

              =              def
            𝜑 ↩→ (x, y, z) = (x ↩→ x ∧ y ↩→ x) ∨ (y ↩→ y ∧ x ↩→ y) ∨ (x ↩→ z ∧ z ↩→ z)
                                   ∨ [alloc(x) ∧ ¬alloc−1
                                                       z (x) ∧ (⊤ −∗ ¬reach(x, z) ≤ 3)] 2


                                       ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:18                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

          ≠
whereas 𝜑 ↩→ (x, y) is defined as
                   def
         ≠
       𝜑 ↩→ (x, y) = (x ↩→ y ∧ alloc(y)) ∨ (y ↩→ y ∧ reach(x, y) = 2) ∨ (y ↩→ x ∧ x ↩→2y x) ∨
                    [alloc(x) ∧ alloc(y) ∧ ( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧ ¬reach(x, y) ≤ 3
                                             Ó

                         ∧ ((size = 1 ∧ alloc−1     ⊛ (reach(x, y) = 3 ∧ y ↩→2x y))] 3
                                             x (y)) −

   Lemma 3.11. Let x, y, z ∈ PVAR.
   (I) For all memory states (𝑠, ℎ) such that 𝑠 (x) ≠ 𝑠 (z) and 𝑠 (y) ≠ 𝑠 (z), we have (𝑠, ℎ) |= 𝜑 ↩→ (x, y, z)
       iff {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ) and ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)).
  (II) In the translation T(𝜑, 𝑋 ), 𝑛(x) ↩→ 𝑛(y) can be replaced by 𝜑 ↩→ (x, y, x).

   Proof. (I) First, suppose {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ), ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)), 𝑠 (x) ≠ 𝑠 (z) and 𝑠 (y) ≠
𝑠 (z). Let us distinguish two cases.
Case 1: ℎ(𝑠 (x)) = ℎ(𝑠 (y)). Equivalently, ext(𝑛(x) = 𝑛(y)) holds from Lemma 3.10 and we must
     prove that (𝑠, ℎ) satisfies 𝜑 ↩→= (x, y, z). Consider the subheap ℎ ′ ⊑ ℎ such that dom(ℎ ′ ) =

     {𝑠 (x), 𝑠 (y), ℎ(𝑠 (x))}. There are only a bounded number of subheaps of this kind (up to
     isomorphism with respect to {x, y, z}). Remember that ℎ(𝑠 (x)) = ℎ(𝑠 (y)), ℎ(ℎ(𝑠 (x))) =
     ℎ(𝑠 (y)), 𝑠 (x) ≠ 𝑠 (z) and 𝑠 (y) ≠ 𝑠 (z).
            x=y                             x=y                              x=y                           x

                                                    z                                                          z
                                                                             z                         y
              z



                                 y                       x          y                 x       y

                                     z
                             x
                                                                    z
                                                                                          z

     We need to check that for each case, the memory state satisfies one of the disjuncts of
     the formula 𝜑 ↩→  = (x, y, z). Indeed, it is easy to see that the first and fifth memory states

     (enumerated from the top left to the bottom right) satisfy x ↩→ x ∧ y ↩→ x, the third
     and seventh memory states satisfy x ↩→ z ∧ z ↩→ z and the fourth memory state satisfies
     y ↩→ y∧x ↩→ y. Lastly, the second and sixth memory states satisfy [alloc(x)∧¬alloc−1                 z (x)∧
     (⊤ −∗ ¬reach(x, z) ≤ 3)] 2 . For these last two cases, consider the two-memory-cells heap ℎ ′′ =
     {𝑠 (x) ↦→ ℎ ′ (𝑠 (x)), ℎ ′ (𝑠 (x)) ↦→ ℎ ′ (𝑠 (x))} ⊑ ℎ ′. Trivially, (𝑠, ℎ ′′) |= alloc(x) ∧ ¬alloc−1  z (x).
     Moreover, since ℎ ′′ (ℎ ′ (𝑠 (x))) = ℎ ′ (𝑠 (x)), for any heap ℎ ′′′ such that ℎ ′′′⊥ℎ ′′, ℎ ′′ (ℎ ′ (𝑠 (x)))
     cannot be in dom(ℎ ′′′) and therefore (𝑠, ℎ ′′ + ℎ ′′′) does not satisfy reach(x, z) ≤ 3. It follows
     that (𝑠, ℎ ′′) satisfies (⊤ −∗ ¬reach(x, z) ≤ 3).
Case 2: ℎ(𝑠 (x)) ≠ ℎ(𝑠 (y)). Equivalently, from Lemma 3.10, ext(𝑛(x) = 𝑛(y)) does not hold and we
                                       ≠
     must prove that (𝑠, ℎ) |= 𝜑 ↩→      (x, y).
     Moreover, 𝑠 (x) ≠ 𝑠 (y). Consider the subheap ℎ ′ ⊑ ℎ such that dom(ℎ ′) = {𝑠 (x), 𝑠 (y), ℎ(𝑠 (x))}.
     There are only a bounded number of subheaps of this kind (up to isomorphism with respect
     to {x, y}). Remember that ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)) and ℎ(𝑠 (x)) ≠ ℎ(𝑠 (y)).

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                 1:19


       x                   x    y                     x    y                     x    y                       x     y



       y
                                                                              ≠
      Let us check that for each of the five cases, one of the disjuncts of 𝜑 ↩→ (x, y) holds. Trivially,
      the first and third memory states satisfy the first disjunct x ↩→ y ∧ alloc(y), the second one
      satisfies y ↩→ x ∧ x ↩→2y x, whereas the fourth one satisfies y ↩→ y ∧ reach(x, y) = 2. Lastly,
      the fifth one satisfies the disjunct
                 [alloc(x) ∧ alloc(y) ∧ ( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧ ¬reach(x, y) ≤ 3
                                           Ó

                         ∧((size = 1 ∧ alloc−1  x (y)) −  ⊛ (reach(x, y) = 3 ∧ y ↩→2x y))] 3

      For the fifth memory state, trivially (𝑠, ℎ ′) |= alloc(x) ∧ alloc(y) ∧ ( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧
                                                                                        Ó
      ¬reach(x, y) ≤ 3. Let ℎ ′′ = {ℎ ′ (ℎ ′ (𝑠 (x))) ↦→ 𝑠 (y)}. As ℎ ′ (ℎ ′ (𝑠 (x))) ∉ dom(ℎ ′), it holds that
      ℎ ′′⊥ℎ ′. Moreover, (𝑠, ℎ ′′) satisfies size = 1 ∧ alloc−1                                  ′   ′′
                                                                     x (y). Consider now (𝑠, ℎ + ℎ ). Since
        ′′    ′    ′
      ℎ (ℎ (ℎ (𝑠 (x)))) = 𝑠 (y), this memory state satisfies reach(x, y) = 3, whereas y ↩→2x y is
      satisfied from the hypothesis 𝑠 (x) ≠ 𝑠 (y) and ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)). Indeed, ℎ ′′ (ℎ ′ (𝑠 (y))) =
      ℎ ′′ (ℎ ′ (ℎ ′ (𝑠 (x)))) = 𝑠 (y). We derive (𝑠, ℎ ′) |= ((size = 1 ∧ alloc−1x (y)) − ⊛ (reach(x, y) = 3 ∧
      y ↩→2x y)).
  Conversely, let us suppose that (𝑠, ℎ) |= 𝜑 ↩→ (x, y, z), 𝑠 (x) ≠ 𝑠 (z) and 𝑠 (y) ≠ 𝑠 (z). Two cases are
considered.
Case 1: (𝑠, ℎ) |= ext(𝑛(x) = 𝑛(y)) ∧ 𝜑 ↩→      = (x, y, z). If one of the three first disjuncts of 𝜑 = (x, y, z)
                                                                                                     ↩→
      holds, we have immediately {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ) and ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)). Indeed, let us
      consider the three possible situations.
    (1) In the case (𝑠, ℎ) |= ext(𝑛(x) = 𝑛(y)) ∧x ↩→ x∧y ↩→ x, we get ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)) = 𝑠 (x)
         and therefore (𝑠, ℎ) |= 𝑛(x) ↩→ 𝑛(y).
    (2) In the case (𝑠, ℎ) |= ext(𝑛(x) = 𝑛(y)) ∧y ↩→ y∧x ↩→ y, we get ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)) = 𝑠 (y)
         and therefore (𝑠, ℎ) |= 𝑛(x) ↩→ 𝑛(y).
    (3) In the case (𝑠, ℎ) |= ext(𝑛(x) = 𝑛(y)) ∧x ↩→ z∧z ↩→ z, we get ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)) = 𝑠 (z)
         and therefore (𝑠, ℎ) |= 𝑛(x) ↩→ 𝑛(y).
      The remaining case is when none of the three first disjuncts holds and therefore (𝑠, ℎ) |=
      [alloc(x) ∧ ¬alloc−1                                                        ′
                                    z (x) ∧ (⊤ −∗ ¬reach(x, z) ≤ 3)] 2 . Let ℎ ⊑ ℎ be some heap with
                         ′                ′                           −1
      card(dom(ℎ )) = 2 and (𝑠, ℎ ) |= alloc(x) ∧ ¬allocz (x) ∧ (⊤ −∗ ¬reach(x, z) ≤ 3). Obvi-
      ously, 𝑠 (x) ∈ dom(ℎ ′), say ℎ ′ (𝑠 (x)) = ℓ and ℓ ∈ dom(ℎ ′) (otherwise (𝑠, ℎ ′ + {ℓ ↦→ 𝑠 (z)}) |=
      reach(x, z) = 2, which leads to a contradiction). We can assume that ℓ is distinct from
      𝑠 (x) as the first disjunct of 𝜑 ↩→    = (x, y, z) does not hold. Similarly, (𝑠, ℎ ′ ) |= ¬(x ↩→ z) ∧

      ¬(reach(x, z) = 2), otherwise we reach a contradiction with (𝑠, ℎ ′) |= ⊤ −∗ ¬reach(x, z) ≤ 3.
      To sump up, the heap ℎ ′ satisfies the following properties:
      • card(dom(ℎ ′)) = 2, 𝑠 (x) ∈ dom(ℎ ′) and ℎ ′ (𝑠 (x)) = ℓ with ℓ ≠ 𝑠 (x) and ℓ ∈ dom(ℎ ′).
      • (𝑠, ℎ ′) |= ¬alloc−1    z (x) ∧ (⊤ −∗ ¬reach(x, z) ≤ 3) ∧ ¬(x ↩→ z) ∧ ¬(reach(x, z) = 2).
      If ℎ(ℎ(𝑠 (x))) ≠ ℎ(𝑠 (x)) or ℎ(ℎ(𝑠 (x))) = 𝑠 (x), then we would have (𝑠, ℎ ′) |= alloc−1           z (x) ∨
      (⊤ −⊛ (reach(x, z) ≤ 3)), which is precisely excluded from above. Consequently, we conclude
      that necessarily ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (x)) ≠ 𝑠 (x). Moreover, by Lemma 3.10, (𝑠, ℎ) |= ext(𝑛(x) =
      𝑛(y)) implies that ℎ(𝑠 (x)) = ℎ(𝑠 (y)). ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)) and {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ)
      follows.
                                                ≠
Case 2: (𝑠, ℎ) |= ¬ext(𝑛(x) = 𝑛(y)) ∧ 𝜑 ↩→         (x, y). This implies 𝑠 (x) ≠ 𝑠 (y). If one of the three first
                           ≠
      disjuncts of 𝜑 ↩→ (x, y) holds, we have immediately {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ) and ℎ(ℎ(𝑠 (x)))

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:20                                                       Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       = ℎ(𝑠 (y)). The remaining case is when none of the three first disjuncts holds and (𝑠, ℎ)
       satisfies the fourth one. So, there is a heap ℎ ′ ⊑ ℎ with card(dom(ℎ ′)) = 3 such that (𝑠, ℎ ′)
       satisfies
                  alloc(x) ∧ alloc(y) ∧ ( z,z′ ∈ {x,y} ¬z ↩→ z′) ∧ ¬reach(x, y) ≤ 3
                                            Ó

                            ∧((size = 1 ∧ alloc−1     ⊛ (reach(x, y) = 3 ∧ y ↩→2x y)).
                                               x (y)) −
       Since (𝑠, ℎ) |= ¬ext(𝑛(x) = 𝑛(y)), the only memory states with three memory cells satisfying
       alloc(x) ∧ alloc(y) ∧ ( z,z′ ∈ {x,y} ¬z ↩→ z′) are the following (up to isomorphism with
                                 Ó
       respect to {x, y}):

        x       y                      x   y                              x       y               x       y




                x       y                      x       y                  x       y               x       y




            x       y                      x       y                          x       y                   x       y




                x       y                  x       y                          x       y               x       y




       The formula (size = 1 ∧ alloc−1              ⊛ (reach(x, y) = 3 ∧ y ↩→2x y) can only be satisfied on
                                             x (y)) −
       heaps ℎ where there exists a way of adding a one-memory-cell heap ℎ ′′ with 𝑠 (y) ∈ ran(ℎ ′′)
               ′

       and (ℎ ′ + ℎ ′′) 3 (𝑠 (x)) = 𝑠 (y). This rules out all the memory states of the figure but the first
       and last one of the last row:
                                          x y                             x y



       Typically, ℎ ′′ can only take the value {ℎ ′ (ℎ ′ (𝑠 (x))) ↦→ 𝑠 (y)}. However, only the second
       memory state is able to verify the condition (𝑠, ℎ ′ + ℎ ′′) |= y ↩→2x y. Then ℎ ′ (𝑠 (y)) =
       ℎ ′ (ℎ ′ (𝑠 (x))) and we conclude that {𝑠 (x), 𝑠 (y)} ⊆ dom(ℎ) and ℎ(ℎ(𝑠 (x))) = ℎ(𝑠 (y)).
  (II) It is easy to show that 𝑛(x) ↩→ 𝑛(x) will never occur in the translation. Indeed, by al-
ways translating formulae with variables in {x1, . . . , x𝑞 } we can only have 𝑛(x𝑖 ) ↩→ 𝑛(x 𝑗 ) or
𝑛(x𝑖 ) ↩→ 𝑛(x 𝑗 ) (the latter case due to the renaming in the translation of the left side of the magic
wand). As such, 𝜑 ↩→ (x, y, x) can be used to check whenever 𝑛(x) ↩→ 𝑛(y).                           □

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                1:21

  As for alloc−1  y (x), the properties of the translation imply the equivalence between 𝑛(x) ↩→ 𝑛(y)
and 𝜑 ↩→ (x, y, x) (as stated in Lemma 3.11(II)). By looking at the formulae herein defined, the predicate
reach only appears bounded, i.e. in the form of reach(x, y) = 2 and reach(x, y) = 3. The three new
predicates can therefore be defined in SL(∗, −∗) enriched with reach(x, y) = 2 and reach(x, y) = 3.
Observe that reach(x, y) = 0 and reach(x, y) = 1 are already definable in the logic SL(∗, −∗).

3.5   Undecidability results and non-finite axiomatization
It is time to collect the fruits of all our efforts and to conclude this part about undecidability. As
a direct consequence of Corollary 3.7 and the undecidability of SL(∀, −∗), here is one of the main
results of the paper.
  Theorem 3.12. The satisfiability problem for SL(∗, −∗, ls) is undecidable.
  As a by-product, we get the following (negative) result.
  Theorem 3.13. The set of valid formulae for SL(∗, −∗, ls) is not recursively enumerable.
   Indeed, suppose that the set of valid formulae for SL(∗, −∗, ls) were recursively enumerable, then
one can enumerate the valid formulae of the form TVAL (𝜑) as it is decidable in PTime whether
𝜓 in SL(∗, −∗, ls) is syntactically equal to TVAL (𝜑) for some SL(∀, −∗) formula 𝜑. This leads to a
contradiction since this would allow the enumeration of valid formulae in SL(∀, −∗). Note also that
the set of satisfiable formulae for SL(∗, −∗, ls) is not recursively enumerable. Indeed, suppose 𝜑 is a
formula built over 𝑉 = {x1, . . . , x𝑛 }. Given a partition 𝑋 of 𝑉 , we write 𝜓𝑋 to denote conjunctions
of equalities and inequalities that state that two variables (resp. not) in the same element of the
partition are equal (resp. are different). One can show that 𝜑 is valid iff emp ∧ 𝜓𝑋 ∧ (⊤ −∗ 𝜑) is
satisfiable, for all partitions 𝑋 . As the set of valid formulae is not r.e., the same applies to the set of
satisfiable formulae.
   Below, the essential ingredients to establish the undecidability of SL(∗, −∗, ls) allow us to propose
several refinements. For instance, the key property rests on the fact that the following properties
𝑛(x) = 𝑛(y), 𝑛(x) ↩→ 𝑛(y) and alloc−1 (x) are expressible in the logic.
  Corollary 3.14. SL(∗, −∗) augmented with formulae of the form 𝑛(x) = 𝑛(y), 𝑛(x) ↩→ 𝑛(y) and
alloc−1 (x) admits an undecidable satisfiability problem.
  Corollary 3.14 can be refined a bit further by noting in which context the reachability predicates
ls and reach are used in the formulae. This allows us to get the result below.
  Corollary 3.15. SL(∗, −∗) augmented with built-in formulae of the form reach(x, y) = 2 and
reach(x, y) = 3 admits an undecidable satisfiability problem.
  It is the addition of reach(x, y) = 3 that is crucial for undecidability since the satisfiability
problem for SL(∗, −∗, reach(x, y) = 2) is in PSpace [17].
  Following a similar analysis, let SL1(∀, ∗, −∗) (resp. SL2(∀, ∗, −∗)) be the restriction of SL(∀, ∗, −∗) (i.e.
SL(∀, −∗) plus ∗) to formulae of the form ∃x1 · · · ∃x𝑞 𝜑, where 𝑞 ≥ 1, the variables in 𝜑 are among
{x1, . . . , x𝑞+1 } (resp. are among {x1, . . . , x𝑞+2 }) and the only quantified variable in 𝜑 is x𝑞+1 (resp. and
the only quantified variables in 𝜑 are x𝑞+1 and x𝑞+2 ). Note that SL2(∀, ∗, −∗) should not be confused
with SL(∀, −∗) restricted to two quantified variables. The satisfiability problem for SL1(∀, ∗, −∗) is
PSpace-complete [17]. Observe that SL1(∀, ∗, −∗) can easily express 𝑛(x) = 𝑛(y) and alloc−1 (x).
The distance between the decidability for SL1(∀, ∗, −∗) and the undecidability for SL(∗, −∗, ls), is
best witnessed by Corollary 3.16(I) below, which solves an open problem [17, Section 6]. Below,
we state several undecidability results for the record, but we do not claim that all these variants
happen to be interesting in practice.

                                   ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:22                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

   Corollary 3.16. The satisfiability problem of the following logics is undecidable:
   (I) SL1(∀, ∗, −∗) augmented with 𝑛(x) ↩→ 𝑛(y),
  (II) SL1(∀, ∗, −∗) augmented with ls,
 (III) SL2(∀, ∗, −∗) ,
 (IV) SL(∗, −∗, ls) restricted to four program variables,
  (V) SL(−∗, 𝑛(x) = 𝑛(y), 𝑛(x) ↩→ 𝑛(y), alloc−1 (x)).
   Proof. (I) Consequence of Corollary 3.14 by observing that emp, 𝑛(x) = 𝑛(y) and alloc−1 (x)
can be expressed with one quantified variable.
   (II) Consequence of (I), as 𝑛(x) ↩→ 𝑛(y) can be expressed with ls.
   (III) Consequence of (I), as 𝑛(x) ↩→ 𝑛(y) can be expressed with two quantified variables.
   (IV) It is shown in [16] that SL(∀, −∗) restricted to two quantified variables is undecidable. The
translation provided in Section 3.3 assumes that distinct quantifications involve distinct variables.
In order to translate SL(∀, −∗) restricted to two quantified variables, it is necessary to give up that
assumption and to update the definition of T. Actually, only the clause for formulae of the form
∀x𝑖 𝜓 requires a change (𝑖 ∈ {1, 2} and the formulae to be translated contains at most two variables).
Here is the new value for T(∀x𝑖 𝜓, 𝑋 ):
((alloc(x𝑖 ) ∧ size = 1) ∨ emp) ∗ (¬alloc(x𝑖 ) ∧ (alloc(x𝑖 ) ∧ size = 1) −∗ (Safe(𝑋 ) ⇒ T(𝜓, 𝑋 ))).
The proof of Lemma 3.6 can be updated accordingly.
  (V) In the translation T to SL(∗, −∗, ls) formulae, the separating connective ∗ appears only in the
definition of T(𝜓 1 −∗ 𝜓 2, 𝑋 ), assuming that 𝑛(x) = 𝑛(y), 𝑛(x) ↩→ 𝑛(y) and alloc−1 (x) are built-in
predicates. It is easy to check that if we remove
                                     Û
                                   “( alloc(z) ∧ size = card(𝑍 )) ∗ ”
                                       z∈𝑍
from T(𝜓 1 −∗ 𝜓 2, 𝑋 ) (i.e., we disallow the recycling of variables), the proof of Lemma 3.6 can be
updated accordingly.                                                                               □

4     DECISION PROCEDURES IN PSPACE FOR SL(∗, reach+ ) AND VARIANTS
We show that the satisfiability problem for SL(∗, reach+ ) can be solved in polynomial space. Refining
the arguments used in our proof, we also show that it is possible to push further the PSpace upper
bound to the formulae expressible as a Boolean combination of formulae from the two fragments
SL(∗, reach+ ) and SL(∗, −∗). The latter logic is shown to be PSpace-complete in [28, 41]. Moreover,
as shown in Section 2, SL(∗, ls) can be understood as a fragment of SL(∗, reach+ ) and therefore
the PSpace upper bound for SL(∗, reach+ ) established here also holds for SL(∗, ls).
   Our proof relies on a small heap property: a formula 𝜑 is satisfiable if and only if it admits a model
with a polynomial amount of memory cells. The PSpace upper bound then follows by establishing
that the model-checking problem for SL(∗, reach+ ) is in PSpace too. To establish the small heap
property, an equivalence relation on memory states with finite index is designed, following the
standard approach in [11, 41] and using test formulae as in [5, 17, 21, 28, 29].

4.1    Introduction to test formulae
In order to show the PSpace upper bound for SL(∗, reach+ ), we would like to adapt the technique
introduced in [28] for SL(∗, −∗), which relies on defining a set of test formulae capturing the essential
properties expressible in SL(∗, −∗), as depicted by the following result.
   Proposition 4.1. [15, 28] Any formula 𝜑 in SL(∗, −∗) built over variables in x1 , . . . ,x𝑞 is logically
equivalent to a Boolean combination of test formulae, i.e. formulae among size ≥ 𝛽, alloc(x𝑖 ),
x𝑖 ↩→ x 𝑗 and x𝑖 = x 𝑗 , with 𝛽 ≥ 0 and 𝑖, 𝑗 ∈ [1, 𝑞].

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                     1:23

                     x𝑖                                       x𝑖             x𝑖               x𝑗         x𝑖            x𝑗


 x𝑘                                   x𝑘
                                                                              ℓ                ℓ′        ℓ             ℓ′



                     x𝑗                                       x𝑗
                                                                                     x𝑘                        x𝑘

                           Fig. 4. Memory states (𝑠 1, ℎ 1 ), . . . , (𝑠 4, ℎ 4 ) (from left to right)


   The formulae of the form size ≥ 𝛽 and alloc(x𝑖 ) are introduced in Section 2 and alloc(x𝑖 )
holds when 𝑠 (x𝑖 ) belongs to the heap domain and size ≥ 𝛽 holds when the heap has at least 𝛽
memory cells. By way of example, (¬emp ∗ ((x1 ↩→ x1 )−∗ ⊥)) is equivalent to size ≥ 2 ∧ alloc(x1 ).
As a corollary of its proof, Proposition 4.1 can be refined so that in the formulae size ≥ 𝛽, we can
enforce that 𝛽 ≤ 2× |𝜑 | (rough upper bound) where |𝜑 | is the size of 𝜑 (seen as a tree). Consequently,
for any satisfiable formula 𝜑 in SL(∗, −∗), there is a memory state with less than 2 × |𝜑 | memory
cells that satisfies it. Similar results will be shown for SL(∗, reach+ ) and for some of its extensions.
   In order to define a set of test formulae that captures the expressive power of SL(∗, reach+ ),
we need to study which basic properties on memory states can be expressed by formulae in
SL(∗, reach+ ). For example, consider the memory states from Figure 4. The memory states (𝑠 1, ℎ 1 )
and (𝑠 2, ℎ 2 ) can be distinguished by the formula
                          ⊤ ∗ (reach+ (x𝑖 , x 𝑗 ) ∧ reach+ (x 𝑗 , x𝑘 ) ∧ ¬reach+ (x𝑘 , x𝑖 )).
Indeed, (𝑠 1, ℎ 1 ) satisfies this formula (a witness is obtained by removing the only edge that leads
to 𝑠 1 (x𝑖 )), whereas (𝑠 2, ℎ 2 ) does not, as every subheap of ℎ 2 that retains the path from 𝑠 (x𝑖 ) to
𝑠 (x 𝑗 ) and the one from 𝑠 (x 𝑗 ) to 𝑠 (x𝑘 ) necessarily has a path from 𝑠 (x𝑘 ) to 𝑠 (x𝑖 ). This suggests that
SL(∗, reach+ ) can express whether, for example, any path from 𝑠 (x𝑖 ) to 𝑠 (x 𝑗 ) also contains 𝑠 (x𝑘 ).
We will introduce the test formula sees𝑞 (x𝑖 , x 𝑗 ) ≥ 𝛽 to capture this property.
   Similarly, the memory states (𝑠 3, ℎ 3 ) and (𝑠 4, ℎ 4 ) can be distinguished by the formula
                   (size = 1) ∗ reach+ (x 𝑗 , x𝑘 ) ∧ ¬reach+ (x𝑖 , x𝑘 ) ∧ ¬reach+ (x𝑘 , x𝑘 ) .
                                                                                               

The memory state (𝑠 3, ℎ 3 ) satisfies this formula by separating {ℓ ↦→ ℓ ′ } from the rest of the heap,
whereas the formula is not satisfied by (𝑠 4, ℎ 4 ). Indeed, there is no way to break the loop from
𝑠 (x𝑘 ) to itself by removing just one location from the heap while retaining the path from 𝑠 (x 𝑗 ) to
𝑠 (x𝑘 ) and loosing the path from 𝑠 (x𝑖 ) to 𝑠 (x𝑘 ). This suggests that the two locations ℓ and ℓ ′ are
particularly interesting since they are reachable from several locations corresponding to program
variables. Therefore by separating them from the rest of the heap, several paths are lost. In order to
capture this, we introduce the notion of meet-points.
   Informally, given a memory state (𝑠, ℎ), a meet-point between 𝑠 (x) and 𝑠 (y) leading to 𝑠 (z) is a
location ℓ such that ℓ reaches 𝑠 (z), both locations 𝑠 (x) and 𝑠 (y) reach ℓ, and there is no location ℓ ′
satisfying these properties and reachable from 𝑠 (x) in strictly less steps. Let us formalise this notion.
Let Terms𝑞 be the set {x1, . . . , x𝑞 } ∪ {𝑚𝑞 (x𝑖 , x 𝑗 ) | 𝑖, 𝑗 ∈ [1, 𝑞]} understood as the set of terms that
                                                                                        𝑞
are either variables or expressions denoting a meet-point. We write [[x𝑖 ]] 𝑠,ℎ to denote 𝑠 (x𝑖 ) and
                   𝑞
[[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ to denote (if it exists) the first location reachable from 𝑠 (x𝑖 ) that is also reachable
from 𝑠 (x 𝑗 ). Moreover we require that this location can reach another location corresponding to a

                                        ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:24                                                    Stéphane Demri, Etienne Lozes, and Alessio Mansutti

              x𝑖             x𝑗                   x𝑖           x𝑗                      x𝑖



       𝑚𝑞 (x𝑖 ,x 𝑗 )                       𝑚𝑞 (x𝑖 ,x 𝑗 )                                                 x𝑗
                                                                               𝑚𝑞 (x𝑖 ,x 𝑗 )
       𝑚𝑞 (x 𝑗 ,x𝑖 )                       𝑚𝑞 (x 𝑗 ,x𝑖 )
                                                                                       +          +
                       x𝑘                                                             x𝑘
                                                   +
        x𝑘 not inside a loop,                                                                          𝑚𝑞 (x 𝑗 ,x𝑖 )
         but can reach one                               x𝑘
                       (i)                              (ii)                                   (iii)

                                         Fig. 5. A taxonomy of meet-points

                                                    𝑞
program variable. Formally, [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is defined as the unique location ℓ (if it exists) such
that
    • there are 𝐿1, 𝐿2 ≥ 0 such that ℎ𝐿1 (𝑠 (x𝑖 )) = ℎ𝐿2 (𝑠 (x 𝑗 )) = ℓ, and
                                              ′              ′
    • for all 𝐿1′ < 𝐿1 and for all 𝐿2′ ≥ 0, ℎ𝐿1 𝑠 (x𝑖 ) ≠ ℎ𝐿2 𝑠 (x 𝑗 ) , and
                                                                     

    • there exist 𝑘 ∈ [1, 𝑞] and 𝐿 ≥ 0 such that ℎ𝐿 (ℓ) = 𝑠 (x𝑘 ).
                                                         𝑞
One can easily show that the notion [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is well-defined.
                                                                                                                       𝑞
   Lemma 4.2. Let 𝑖, 𝑗 ∈ [1, 𝑞]. At most one location satisfies the conditions of [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ .
  Proof. Ad absurdum, assume that there are two different locations ℓ1 and ℓ2 that satisfy the
                                 𝑞
conditions of [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ . In particular, there are 𝐿1, 𝐿2, 𝐿3, 𝐿4 ≥ 0 such that
  (A) ℎ𝐿1 (𝑠 (x𝑖 )) = ℎ𝐿2 (𝑠 (x 𝑗 )) = ℓ1 and ℎ𝐿3 (𝑠 (x𝑖 )) = ℎ𝐿4 (𝑠 (x 𝑗 )) = ℓ2 ,
                                                 ′               ′
  (B) for all 𝐿1′ < 𝐿1 and for all 𝐿2′ ≥ 0, ℎ𝐿1 𝑠 (x𝑖 ) ≠ ℎ𝐿2 𝑠 (x 𝑗 ) .
                                                                           
                                                 ′               ′
  (C) for all 𝐿3′ < 𝐿3 and for all 𝐿4′ ≥ 0, ℎ𝐿3 𝑠 (x𝑖 ) ≠ ℎ𝐿4 𝑠 (x 𝑗 ) .
                                                                           
                                                                                    𝑞
Notice that (A) corresponds to the first condition of [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ , with respect to ℓ1 and ℓ2 ,
whereas (B) and (C) correspond to the second condition for ℓ1 and ℓ2 , respectively. Let 𝐿min =
min{𝑛 | ℎ𝑛 (𝑠 (x𝑖 )) ∈ {ℓ1, ℓ2 }}. Let us assume that ℎ𝐿min (𝑠 (x𝑖 )) = ℓ1 and so, as ℓ1 ≠ ℓ2 , for all 𝐿 ≥ 0,
ℎ𝐿 (𝑠 (x𝑖 )) = ℓ2 implies 𝐿min < 𝐿. From (A) this implies that 𝐿min < 𝐿1′ and ℎ𝐿min (𝑠 (x𝑖 )) = heap𝐿2 𝑠 (ℎ 𝑗 ),
which however contradicts (C). The case where ℎ𝐿min (𝑠 (x𝑖 )) = ℓ2 is analogous, the contradiction
being reached with (B).                                                                                      □
  The notion of meet-point is quite natural for studying fragments of separation logic with ls. For
instance, a similar notion of a cut point, although satisfying different conditions, is considered for
the fragments studied in [4]. Figure 5 provides a taxonomy of meet-points, where arrows labelled
by ‘+’ represent paths of non-zero length and zig-zag arrows any path (possibly of length zero).
Symmetrical cases, obtained by swapping x𝑖 and x 𝑗 , are omitted. Following Figure 5, the taxonomy
                                                                                     𝑞
with three distinct shapes depends on the following conditions on [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and 𝑠 (x𝑘 ):
    • 𝑠 (x𝑘 ) is not inside a loop iff ℎ witnesses the shape (i) of the taxonomy.
                                                      𝑞                        𝑞
    • 𝑠 (x𝑘 ) is inside a loop and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ iff ℎ witnesses the shape (ii).
                                                      𝑞                        𝑞
    • 𝑠 (x𝑘 ) is inside a loop and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ≠ [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ iff ℎ witnesses the shape (iii).
Notice that, in the case (i), 𝑠 (x𝑘 ) can a priori be in dom(ℎ), which also means that it can reach a loop,
even though it is not inside one. The asymmetrical definition of meet-points is captured by the case

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                 1:25

(iii). Consider the memory states from Figure 4, (𝑠 3, ℎ 3 ) and (𝑠 4, ℎ 4 ) can be seen as an instance of this
case of the taxonomy and, as such, it holds that [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠3,ℎ3 = ℓ and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠3,ℎ3 = ℓ ′.
                                                                      𝑞                              𝑞
                                                                                                        𝑞
    We identify as special locations the 𝑠 (x𝑖 )’s and the meet-points of the form [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ when
it exists (𝑖, 𝑗 ∈ [1, 𝑞]). We call such locations, labelled locations and denote by Lab𝑞 (𝑠, ℎ) the set of
labelled locations. The following lemma states an important property of labelled locations: taking
subheaps can only reduce their set.
   Lemma 4.3. Let (𝑠, ℎ) be a memory state, ℎ ′ ⊑ ℎ and 𝑞 ≥ 1. We have Lab𝑞 (𝑠, ℎ ′) ⊆ Lab𝑞 (𝑠, ℎ).
    Proof. Let ℓ ∈ Lab𝑞 (𝑠, ℎ ′). We want to prove that ℓ ∈ Lab𝑞 (𝑠, ℎ). The only interesting case is
                                  𝑞                           𝑞
when ℓ ∈ {[[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ | [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ is defined, 𝑖, 𝑗 ∈ [1, 𝑞]} \ {𝑠 (x𝑖 ) | 𝑖 ∈ [1, 𝑞]} as
(𝑠, ℎ) and (𝑠, ℎ ′) share the same store and therefore the result is trivial for locations that correspond
                                                                                                 𝑞
to the interpretation of program variables. So, suppose that ℓ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ for some 𝑖, 𝑗. We
                                                                                               𝑞
just need to prove that there exist 𝑖 ★, 𝑗 ★ ∈ [1, 𝑞] such that [[𝑚𝑞 (x𝑖 ★ , x 𝑗 ★ )]] 𝑠,ℎ = ℓ.
    By definition, [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ = ℓ if and only if there exist 𝑘 ∈ [1, 𝑞] and 𝐿 such that ℎ ′𝐿 (ℓ) =
                                        𝑞

𝑠 (x𝑘 ) and there are 𝐿1, 𝐿2 such that ℎ ′𝐿1 (𝑠 (x𝑖 )) = ℎ ′𝐿2 (𝑠 (x 𝑗 )) = ℓ and for all 𝐿1′ < 𝐿1 and 𝐿2′
                 ′                  ′
it holds ℎ ′𝐿1 (𝑠 (x𝑖 )) ≠ ℎ ′𝐿2 (𝑠 (x 𝑗 )). As ℎ ′ ⊑ ℎ, each path of ℎ ′ is also a path in ℎ. In particular,
ℎ (ℓ) = 𝑠 (x𝑘 ). As such, we only need to prove that that there exist 𝑖 ★, 𝑗 ★ ∈ [1, 𝑞] such that there
  𝐿
                                                                                                      ′
are 𝐿1, 𝐿2 such that ℎ𝐿1 (𝑠 (x𝑖 ★ )) = ℎ𝐿2 (𝑠 (x 𝑗 ★ )) = ℓ and for all 𝐿1′ < 𝐿1 and 𝐿2′ it holds ℎ𝐿1 (𝑠 (x𝑖 ★ )) ≠
    ′
ℎ𝐿2 (𝑠 (x 𝑗 ★ )). We consider the taxonomy of 𝑚𝑞 (x𝑖 , x 𝑗 ) shown in Figure 5. Based on the classification,
[[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ = ℓ entails that the heap ℎ ′ witnesses one of the situations among (i)–(iii).
                   𝑞

    If the heap ℎ ′ belongs to (ii) or (iii), the locations 𝑠 (x𝑖 ) and 𝑠 (x 𝑗 ) eventually reach a location ℓ˜
belonging to a loop, i.e. ℎ ′𝐿 ( ℓ)    ˜ = ℓ˜ for some 𝐿 ≥ 1, and since ℎ ′ ⊑ ℎ, the same holds true in ℎ.
Hence, in ℎ, the location ℓ is still the first location reachable from x𝑖 that is also reachable from x 𝑗
and therefore 𝑖 ★ = 𝑖 and 𝑗 ★ = 𝑗.
    Alternatively, if ℎ ′ belongs to (i), the heap ℎ may belong to any of the three situations (i)–(iii) as
                                                                                             𝑞                   𝑞
far as ℓ is concerned. It is easy to see that in ℎ, either ℓ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ or ℓ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ ,
which guarantees that ℓ is a labelled location in ℎ. Let us justify this claim. As (i) holds, either (a)
𝑠 (x𝑘 ) can reach a location that is not in the domain of the heap ℎ ′ or (b) 𝑠 (x𝑘 ) does not reach such
a location, that is, there is a cycle after x𝑘 . If (b) holds, then a reasoning analogous to the above
cases for (ii) and (iii) works. Otherwise ((a) holds), in ℎ ′ there is a location ℓ ′ reachable from 𝑠 (x𝑘 )
that is not in dom(ℎ ′). We now consider how ℎ extends ℎ ′.
                                                                   𝑞                   𝑞
      • If ℎ belongs to (i), then ℓ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ . The same holds true if ℎ
        extends ℎ ′ by introducing a loop so that ℎ belongs to (ii).
      • If ℎ extends ℎ ′ by adding a path from ℓ ′ to a location in the path between 𝑠 (x 𝑗 ) to ℓ (ℓ
                                                    𝑞                       𝑞
        excluded), then ℓ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ and ℎ belongs to (iii).
      • Lastly, if ℎ extends ℎ ′ by adding a path from ℓ ′ to a location in the path between 𝑠 (x𝑖 )
        to ℓ (ℓ excluded), then ℎ belongs also to (iii). Unlike the previous case however, we have
                               𝑞                        𝑞
        ℓ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ′ , so ℓ is again in Lab𝑞 (𝑠, ℎ).                       □
   As shown in Proposition 4.1, the test formulae explicit what are the essential features that are
expressible in SL(∗, −∗). For SL(∗, reach+ ), these test formulae primarily speak about relationships
between labelled locations and specific shapes of the heap. In order to highlight these relationships,
below we introduce a class of abstract structures, called support graphs. The semantics for test
formulae shall be provided directly on such support graphs.
  Definition 4.4. Let 𝑞 ≥ 1 and (𝑠, ℎ) be a memory state. Its support graph SG𝑞 (𝑠, ℎ) is defined as
the tuple (V, E, Alloc, TEq, Inter, Rem) such that:

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:26                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

        def
(V) V = Lab𝑞 (𝑠, ℎ) is the set of labelled locations.
                                                                                      def
(E) E is the (functional) binary relation on V such that (ℓ, ℓ ′) ∈ E ⇔ there is 𝐿 ≥ 1 such that
                                                            ′
      ℎ𝐿 (ℓ) = ℓ ′ and for all 0 < 𝐿 ′ < 𝐿, it holds that ℎ𝐿 (ℓ) ∉ V. Informally, E(ℓ, ℓ ′) if and only if
      there is a non-empty path from ℓ to ℓ ′ whose intermediate locations are not labelled.
           def
(A) Alloc = V ∩ dom(ℎ).
(T) TEq : V → P (Terms𝑞 ) is a function such that for any labelled location ℓ ∈ V, is the (non-empty)
                                                                     def                    𝑞
       set of terms corresponding to ℓ. Formally, TEq(ℓ) = {𝑣 ∈ Terms𝑞 | [[𝑣]] 𝑠,ℎ = ℓ }.
(I) Inter : E → P (LOC) is a function such that for any (ℓ, ℓ ′) ∈ E, is the set of intermediate
       locations of the shortest path beginning in ℓ and ending with ℓ ′. Formally,
                                                                                       ′
                                  there are 𝐿, 𝐿 ′ ≥ 1, such that ℎ𝐿 (ℓ) = ℓ ′′ and ℎ𝐿 (ℓ ′′) = ℓ ′
                       (                                                                            )
                 ′ def   ′′
       Inter(ℓ, ℓ ) = ℓ ∈ LOC                                                            ′′
                                                           and for all 𝐿 ′′ ∈ [1, 𝐿], ℎ𝐿 (ℓ) ∉ 𝑉
                                                                                      ′′
     Despite the definition of E, the condition “for all 𝐿 ′′ ∈ [1, 𝐿], ℎ𝐿 (ℓ) ∉ 𝑉 ” in this definition is
     needed in order to handle the case when ℓ and ℓ ′ belongs to the same cycle. Moreover, notice
     that every location ℓ ′′ ∈ Inter(ℓ, ℓ ′) is such that ℓ ′′ ∉ 𝑉 (hence, ℓ ′′ is not a labelled location).
        def
(R) Rem = dom(ℎ) \ (Alloc ∪ (ℓ,ℓ ′ ) ∈E Inter(ℓ, ℓ ′)), i.e. the set of locations in the domain that are
                                Ð
     not labelled locations and that do not belong to paths between labelled locations.
   One can think of the support graph SG𝑞 (𝑠, ℎ) as a selection of properties from (𝑠, ℎ). Indeed, from
its definition, it is straightforward to see that {Alloc, Rem} ∪ {Inter(ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E} is a partition
of dom(ℎ). Moreover, for all 𝑖, 𝑗 ∈ [1, 𝑞] and ℓ ∈ LOC, ℓ = 𝑠 (x𝑖 ) = 𝑠 (x 𝑗 ) iff {x𝑖 , x 𝑗 } ⊆ TEq(ℓ).
   We are now ready to introduce the test formulae. Given 𝑞, 𝛼 ≥ 1, we write Test(𝑞, 𝛼) to denote
the following set of atomic test formulae:
       𝑣 = 𝑣′           alloc(𝑣)               𝑣 ↩→ 𝑣 ′         sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1      sizeR𝑞 ≥ 𝛽,
where 𝑣, 𝑣 ′ ∈ Terms𝑞 and 𝛽 ∈ [1, 𝛼]. It is worth noting that the alloc(𝑣)’s are not needed for the
logic SL(∗, reach+ ) but it is required for extensions (see Theorem 4.15). Let (𝑠, ℎ) be a memory state.
Below, we present the formal semantics for the test formulae, provided with the elements from the
support graph SG𝑞 (𝑠, ℎ) = (V, E, Alloc, TEq, Inter, Rem) of (𝑠, ℎ):
                           def
    • (𝑠, ℎ) |= 𝑣 = 𝑣 ′ ⇔ there is ℓ ∈ V such that {𝑣, 𝑣 ′ } ⊆ TEq(ℓ).
                                   def
    • (𝑠, ℎ) |= alloc(𝑣) ⇔ there is ℓ ∈ Alloc such that 𝑣 ∈ TEq(ℓ).
                             def
    • (𝑠, ℎ) |= 𝑣 ↩→ 𝑣 ′ ⇔ 𝑣 ∈ TEq(ℓ), 𝑣 ′ ∈ TEq(ℓ ′), card(Inter(ℓ, ℓ ′)) = 0 for some (ℓ, ℓ ′) ∈ E.
                                               def
    • (𝑠, ℎ) |= sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 +1 ⇔ there is (ℓ, ℓ ′) ∈ E such that 𝑣 ∈ TEq(ℓ), 𝑣 ′ ∈ TEq(ℓ ′) and
      card(Inter(ℓ, ℓ ′)) ≥ 𝛽.
                                         def
     • (𝑠, ℎ) |= sizeR𝑞 ≥ 𝛽 ⇔ card(Rem) ≥ 𝛽.
The semantics is deliberately defined with the help of support graphs but of course, the clauses could
be formulated with 𝑠 and ℎ only. For instance, the formula sees𝑞 (𝑚𝑞 (x𝑖 , x 𝑗 ), x𝑘 ) ≥ 4 is satisfied
                               𝑞
whenever [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is defined and there is a path of length at least 4 beginning in this
location, ending in 𝑠 (x𝑘 ) and whose intermediate locations are not labelled. Similarly, sizeR𝑞 ≥ 𝛽
holds true whenever the number of allocated locations that are neither between two locations
interpreted by terms nor the interpretation of a term, is at least 𝛽. Notice that there is no need for
test formulae of the form sees𝑞 (𝑣, 𝑣 ′) ≥ 1 since it is equivalent to 𝑣 ↩→ 𝑣 ′ ∨ sees𝑞 (𝑣, 𝑣 ′) ≥ 2. In the
sequel, occurrences of sees𝑞 (𝑣, 𝑣 ′) ≥ 1 are understood as abbreviations. One can check whether
                   𝑞
[[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is defined thanks to the satisfaction of the formula 𝑚𝑞 (x𝑖 , x 𝑗 ) = 𝑚𝑞 (x𝑖 , x 𝑗 ). The
satisfaction of sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1 entails the exclusion of labelled locations in the witness path,

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                 1:27

                                                                      ℎ\𝑇 ′′
which is reminiscent to atomic formulae of the form 𝑇 −−→ 𝑇 ′ in the logic GRASS [34]. Indeed,
                          ℎ\x3
by way of example, x1 −−→ x2 states that there is a path in the graph of the heap ℎ between 𝑠 (x1 )
and 𝑠 (x2 ) without passing via 𝑠 (x3 ). The satisfaction of sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1 requires to exclude
labelled locations strictly between the interpretation of the terms 𝑣 and 𝑣 ′. Our test formulae are
quite expressive since they capture the atomic formulae from SL(∗, reach+ ) and the test formulae
for SL(∗, −∗) (introduced in Proposition 4.1).
  Lemma 4.5. Let 𝛼, 𝑞 ≥ 1, 𝑖, 𝑗 ∈ [1, 𝑞]. Any atomic formula among reach+ (x𝑖 , x 𝑗 ), emp and size ≥ 𝛽
(with 𝛽 ≤ 𝛼), is equivalent to a Boolean combination of test formulae from Test(𝑞, 𝛼).
   Proof. Let 𝑞, 𝛼 ≥ 1 and consider the family of test formulae Test(𝑞, 𝛼). Let (𝑠, ℎ) be a memory
state and SG𝑞 (𝑠, ℎ) = (V, E, Alloc, TEq, Inter, Rem) be its support graph.
    • We
       Ó show that emp is equivalent to the Boolean combination of test formulae ¬sizeR𝑞 ≥ 1 ∧
         𝑖 ∈ [1,𝑞 ] ¬alloc(x𝑖 ). Suppose (𝑠, ℎ) |= emp. Then trivially, for all 𝑖 ∈ [1, 𝑞] (𝑠, ℎ) |= ¬alloc(x𝑖 )
       and (𝑠, ℎ) |= ¬sizeR𝑞 ≥ 1.                         Ó
       Conversely, suppose (𝑠, ℎ) |= ¬sizeR𝑞 ≥ 1 ∧ 𝑖 ∈ [1,𝑞 ] ¬alloc(x𝑖 ). As for all 𝑖 ∈ [1, 𝑞] x𝑖 does
       not correspond to a location in dom(ℎ), it holds that (𝑠, ℎ) |= 𝑣,𝑣′ ∈Terms𝑞 ¬sees𝑞 (𝑣, 𝑣 ′) ≥ 1.
                                                                              Ó
       Therefore, directly from its definition, Rem = dom(ℎ). The emptiness of dom(ℎ) then follows
       from (𝑠, ℎ) |= ¬sizeR𝑞 ≥ 1.
    • The formula reach+ (x𝑖 , x 𝑗 ) can be shown equivalent to
                                   def
                                       Ü            Û
                                 𝜑 =                     sees𝑞 (𝑣𝛿 , 𝑣𝛿+1 ) ≥ 1.
                               𝑣1 ,...,𝑣𝑛 ∈Terms𝑞 , 𝛿 ∈ [1,𝑛−1]
                          pairwise distinct 𝑣1 ,...,𝑣𝑛−1 ,
                                   x𝑖 =𝑣1 ,x 𝑗 =𝑣𝑛

      In the expression above, 𝑛 is arbitrary in the disjunction as soon as the other constraints
      are satisfied (whence, 𝑛 ≤ card(Terms𝑞 )). First, suppose (𝑠, ℎ) |= reach+ (x𝑖 , x 𝑗 ). Then, there
      exists 𝐿 ≥ 1 such that ℎ𝐿 (𝑠 (x𝑖 )) = 𝑠 (x 𝑗 ). Let ℓ1 = 𝑠 (x𝑖 ), ℓ𝑛 = 𝑠 (x 𝑗 ) and let ℓ2, . . . , ℓ𝑛−1 ∈
      Lab𝑞 (𝑠, ℎ) be all labelled locations in the (minimal) path witnessing (𝑠, ℎ) |= reach+ (x𝑖 , x 𝑗 ),
      such that ℎ𝐿𝛿 (ℓ𝛿 ) = ℓ𝛿+1 , where 𝐿𝛿 ≥ 1, and there are no labelled locations between ℓ𝛿
      and ℓ𝛿+1 , 1 ≤ 𝛿 ≤ 𝑛 − 1 ≤ card(Lab𝑞 (𝑠, ℎ)). The path from 𝑠 (x𝑖 ) to 𝑠 (x 𝑗 ) is therefore
      uniquely split into 𝑛 − 1 subpaths starting and ending with a labelled location and without
      labelled locations in between. Let 𝑣 1 = x𝑖 , 𝑣𝑛 = x 𝑗 and 𝑣 2, . . . , 𝑣𝑛−1 ∈ Terms𝑞 be such that
                 𝑞
      [[𝑣𝛿 ]] 𝑠,ℎ = ℓ𝛿 for 𝛿 ∈ [2, 𝑛 − 1]. From the definition of ℓ2, . . . , ℓ𝑛−1 , we conclude that (𝑠, ℎ)
                      Ó
      satisfies 1≤𝛿 ≤𝑛−1 sees𝑞 (𝑣𝛿 , 𝑣𝛿+1 ) ≥ 1. The minimality of the path is needed to guarantee
      that all the 𝑣𝑖 ’s are distinct.
      Conversely, suppose (𝑠, ℎ) |= 𝜑. Then, there are 𝑣 1, . . . , 𝑣𝑛 ∈ Terms𝑞 such that 𝑣 1 = x𝑖 , 𝑣𝑛 = x 𝑗 ,
      𝑣 1 , . . . , 𝑣𝑛−1 are pairwise distinct and for all 𝛿 ∈ [1, 𝑛 − 1] (𝑠, ℎ) |= sees𝑞 (𝑣𝛿 , 𝑣𝛿+1 ) ≥ 1. From
                                                                                                            𝑞
      the semantics of sees, this implies that there are 𝐿1, . . . , 𝐿𝑛−1 ≥ 1 such that ℎ𝐿𝛿 ( [[𝑣𝛿 ]] 𝑠,ℎ ) =
                    𝑞                                                Í                         Í
      [[𝑣𝛿+1 ]] 𝑠,ℎ for all 𝛿 ∈ [1, 𝑛 − 1]. Therefore ℎ(𝑠 (x𝑖 )) 𝛿 𝐿𝛿 = 𝑠 (x 𝑗 ), where 𝛿 𝐿𝛿 ≥ 1 and
      reach+ (x𝑖 , x 𝑗 ) is satisfied.
    • We define size ≥ 𝛽, where 𝛽 ≤ 𝛼. First of all, we introduce the formula sizeV𝑞 (𝑣) ≥ 𝛽, with
      𝑣 ∈ Terms𝑞 , below:
                                         def                                    def
                     sizeV𝑞 (𝑣) ≥ 0 = ⊤                           sizeV𝑞 (𝑣) ≥ 1 = alloc(𝑣)

                                           def
                                                 Ü
                   sizeV𝑞 (𝑣) ≥ 𝛽 + 1 =              sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1      for 𝛽 ∈ [1, 𝛼]
                                           𝑣′ ∈Terms𝑞


                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:28                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       sizeV𝑞 (𝑣) ≥ 0 is always true, sizeV𝑞 (𝑣) ≥ 1 holds in a memory state (𝑠, ℎ) if and only if
       (𝑠, ℎ) |= alloc(𝑣), whereas sizeV𝑞 (𝑣) ≥ 𝛽+1 holds if and only if there exists 𝑣 ′ ∈ Terms𝑞 such
       that (𝑠, ℎ) |= sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 +1. As such, sizeV𝑞 (𝑣) ≥ 𝛽 +1 holds whenever for all 𝐿 ∈ [0, 𝛽],
       ℎ𝐿 ( [[𝑣]] 𝑠,ℎ ) ∈ dom(ℎ), 𝐿 ≥ 1 implies ℎ𝐿 ( [[𝑣]] 𝑠,ℎ ) ∉ Lab𝑞 (𝑠, ℎ), and there is 𝐿 ′ > 𝛽 such that
                  𝑞                                            𝑞
          ′
       ℎ𝐿 ( [[𝑣]] 𝑠,ℎ ) = [[𝑣 ′]] 𝑠,ℎ , for some 𝑣 ′ ∈ Terms𝑞 . From the definition of sees and meet-points, it
                   𝑞              𝑞

       follows that the locations considered for the satisfaction of sizeV𝑞 (𝑣) ≥ 𝛽 do not play any
       role in the satisfaction of sizeV𝑞 (𝑣 ′) ≥ 𝛽 ′, where [[𝑣]] 𝑠,ℎ ≠ [[𝑣 ′]] 𝑠,ℎ . Therefore, it is easy to
                                                                         𝑞          𝑞

       prove that if (𝑠, ℎ) |= sizeV𝑞 (𝑣) ≥ 𝛽 ∧ sizeV𝑞 (𝑣 ′) ≥ 𝛽 ′ ∧ 𝑣 ≠ 𝑣 ′ then card(dom(ℎ)) ≥ 𝛽 + 𝛽 ′.
       Similarly, the locations considered for the satisfaction of this formula are not in Rem and
       therefore (𝑠, ℎ) |= sizeV𝑞 (𝑣) ≥ 𝛽 ∧ sizeR𝑞 ≥ 𝛽 ′ implies card(dom(ℎ)) ≥ 𝛽 + 𝛽 ′. We can
       then use this formula to define size ≥ 𝛽 as follows, where we write sizeR𝑞 ≥ 0 instead of
       x1 = x1 (any tautological Boolean combination of test formulae would be fine).
                       Ü                                                                   
                            sizeR𝑞 ≥ 𝛽𝑅 ∧ 𝑣 ∈𝑉 (sizeV𝑞 (𝑣) ≥ 𝛽 𝑣 ∧ 𝑣′ ∈𝑉 \{𝑣 } 𝑣 ≠ 𝑣 ′)
                                                Ó                          Ó
                   𝑉 ⊆Terms
                        Í 𝑞
                𝛽 ≤𝛽𝑅 + 𝑣∈𝑉 𝛽 𝑣
           𝛽𝑅 ∈ [0,𝛼 ] ∀𝑣 ∈𝑉 𝛽 𝑣 ∈ [0,𝛼+1]

       Suppose that this formula is satisfied by (𝑠, ℎ). Then there exists a subset of terms 𝑉 such
       that for all 𝑣, 𝑣 ′ ∈ 𝑉 , if 𝑣 ≠ 𝑣 ′ then [[𝑣]] 𝑠,ℎ ≠ [[𝑣 ′]] 𝑠,ℎ also follows (from the last conjunct of
                                                       𝑞             𝑞

       the formula). From the property just stated about sizeV𝑞 (𝑣) ≥ 𝛽, it must therefore hold that
                                  Í
       card(dom(ℎ)) ≥ 𝛽𝑅 + 𝑣 ∈𝑉 𝛽 𝑣 ≥ 𝛽.                                                      Í
       Conversely, suppose card(dom(ℎ)) ≥ 𝛽. We can define a partition ℎ𝑅 + ℓ ∈Lab𝑞 (𝑠,ℎ) ℎ ℓ = ℎ
       such that each subheap ℎ ℓ of the partition contains exactly the locations of dom(ℎ) considered
       for the satisfaction of the test formulae sizeV𝑞 (𝑣) ≥ 𝛽 ′, 𝛽 ′ ∈ [0, 𝛼 + 1], for a specific labelled
                            𝑞
       location ℓ = [[𝑣]] 𝑠,ℎ , whereas ℎ𝑅 contains all the locations considered for the satisfaction of
                      ′   ′
       sizeR𝑞 ≥ 𝛽 , 𝛽 ∈ [0, 𝛼]. Consider a representative 𝑣 ∈ Terms𝑞 for each subheap ℎ ℓ , where
             𝑞
       [[𝑣]] 𝑠,ℎ = ℓ. Let 𝑉 be the set of these representatives and let 𝛽𝑅 = min(𝛼, card(dom(ℎ𝑅 ))), 𝛽 𝑣 =
                                                                                                      Í
       min(𝛼 +1, card(dom(ℎ [[𝑣 ]]𝑞 ))). Since 𝛽 ≤ 𝛼 and card(dom(ℎ)) = card(dom(ℎ𝑅 ))+ 𝑣 ∈𝑉 ≥ 𝛽,
                              Í       𝑠,ℎ
       it follows that 𝛽𝑅 + 𝑣 ∈𝑉 𝛽 𝑣 ≥ 𝛽. Moreover, for each 𝑣 ∈ 𝑉 , 𝛽 𝑣Ó∈ [0, 𝛼 +1], whereas 𝛽𝑅 ∈ [0, 𝛼].
       From the definition of 𝑉 , it immediately holds that (𝑠, ℎ) |= 𝑣≠𝑣′ ∈𝑉 𝑣 ≠ 𝑣 ′. Lastly, from their
       definition, it holds that (𝑠, ℎ) |= sizeR𝑞 ≥ 𝛽𝑅 and for all 𝑣 ∈ 𝑉 (𝑠, ℎ) |= sizeV𝑞 (𝑣) ≥ 𝛽 𝑣 . We
       conclude that the formula defining size ≥ 𝛽 is satisfied.                                              □

4.2    Expressive power and the small heap property
Now, we show that the sets of test formulae Test(𝑞, 𝛼) are sufficient to capture the expressive power
of SL(∗, reach+ ) (as shown below, Theorem 4.10) and deduce the small heap property of this logic
                                                                  𝑞
(Theorem 4.11). We introduce an indistinguishability relation ≈𝛼 between memory states based on
test formulae, see analogous relations in [14, 17, 28].
                                                                                                            def
   Definition 4.6. Let 𝑞, 𝛼 ≥ 1 and, (𝑠, ℎ) and (𝑠 ′, ℎ ′) be memory states. (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) ⇔
                                                                                               𝑞

(𝑠, ℎ) |= 𝜓 iff (𝑠 ′, ℎ ′) |= 𝜓 , for all 𝜓 ∈ Test(𝑞, 𝛼).

   Forthcoming Theorem 4.9 states that if (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), then the two memory states cannot be
                                                             𝑞

distinguished by formulae whose syntactic resources are bounded in some way by 𝑞 and 𝛼 (details
                                                                         𝑞
will follow). The following technical lemma lifts the relationship ≈𝛼 to an equivalence between
support graphs, consolidating this idea of indistinguishable memory states.


ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                          1:29

  Lemma 4.7. Let 𝑞, 𝛼 ≥ 1, and (𝑠, ℎ), (𝑠 ′, ℎ ′) be two memory states with support graphs respectively
SG𝑞 (𝑠, ℎ) = (V, E, Alloc, TEq, Inter, Rem) and SG𝑞 (𝑠 ′, ℎ ′) = (V′, E′, Alloc′, TEq′, Inter′, Rem′). We
have (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) iff there is a map 𝔣 : V → V′ such that
             𝑞

(A1) 𝔣 is a graph isomorphism between (V, E) and (V′, E′);
(A2) for all ℓ ∈ V, we have ℓ ∈ Alloc iff 𝔣(ℓ) ∈ Alloc′;
(A3) for all ℓ ∈ V, we have TEq(ℓ) = TEq′ (𝔣(ℓ));
(A4) for all (ℓ, ℓ ′) ∈ E, we have min(𝛼, card(Inter(ℓ, ℓ ′))) = min(𝛼, card(Inter′ (𝔣(ℓ), 𝔣(ℓ ′))));
(A5) min(𝛼, card(Rem)) = min(𝛼, card(Rem′)).
     Proof. Suppose (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′). Let 𝔣 : V → V′ be the map such that for all locations ℓ ∈ V,
                                   𝑞
                     def
we have 𝔣(ℓ) = ℓ ′ if and only if there is 𝑣 ∈ Terms𝑞 such that [[𝑣]] 𝑠,ℎ = ℓ and [[𝑣]] 𝑠 ′,ℎ′ = ℓ ′. Let us
                                                                                        𝑞                     𝑞

show that 𝔣 is well-defined. To do so, assume that there are 𝑣, 𝑣 ′ such that [[𝑣]] 𝑠,ℎ = [[𝑣 ′]] 𝑠,ℎ = ℓ,
                                                                                                           𝑞               𝑞
      𝑞            ′       ′   𝑞            ′′                𝑞    ′   ′                                    ′
[[𝑣]] 𝑠 ′,ℎ′ = ℓ and [[𝑣 ]] 𝑠 ′,ℎ′ = ℓ . Since (𝑠, ℎ) ≈𝛼 (𝑠 , ℎ ), we have that (𝑠, ℎ) |= 𝑣 = 𝑣 iff (𝑠 , ℎ ) |= 𝑣 =   ′  ′

𝑣 ′. Therefore, ([[𝑣]] 𝑠,ℎ , [[𝑣 ′]] 𝑠,ℎ are defined and [[𝑣]] 𝑠,ℎ = [[𝑣 ′]] 𝑠,ℎ ) iff ([[𝑣]] 𝑠 ′,ℎ′ , [[𝑣 ′]] 𝑠 ′,ℎ′ are defined
                          𝑞               𝑞                           𝑞          𝑞              𝑞              𝑞

and [[𝑣]] 𝑠 ′,ℎ′ = [[𝑣 ′]] 𝑠 ′,ℎ′ ). Consequently, ℓ ′ = ℓ ′′ and 𝔣 is well-defined. Actually, the equivalence
              𝑞             𝑞

above induced by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) allows us to show in a similar way that 𝔣 is a bijection from V to
                                     𝑞
   ′
V and that the condition (A3) holds true. Indeed, the statements below are equivalent:
      • {𝑣, 𝑣 ′ } ⊆ TEq(ℓ),
      • (𝑠, ℎ) |= 𝑣 = 𝑣 ′ and [[𝑣]] 𝑠,ℎ = [[𝑣 ′]] 𝑠,ℎ = ℓ (by definition of |= and SG𝑞 (𝑠, ℎ)),
                                            𝑞       𝑞

      • (𝑠 ′, ℎ ′) |= 𝑣 = 𝑣 ′ and [[𝑣]] 𝑠 ′,ℎ′ = [[𝑣 ′]] 𝑠 ′,ℎ′ = ℓ ′ for some ℓ ′ (by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′)),
                                               𝑞         𝑞                                       𝑞

      • (𝑠 ′, ℎ ′) |= 𝑣 = 𝑣 ′ and [[𝑣]] 𝑠 ′,ℎ′ = [[𝑣 ′]] 𝑠 ′,ℎ′ = 𝔣(ℓ) (by definition of 𝔣),
                                               𝑞         𝑞
                          ′
      • {𝑣, 𝑣 } ⊆ TEq (𝔣(ℓ)) (by definition of SG𝑞 (𝑠 ′, ℎ ′)).
                ′

Consequently, the condition (A3) holds true. A similar reasoning allows us to establish (A2) and it
is omitted below. In order to conclude the first part of the proof, first we show (A5) and then we
focus on (A1) and (A4). Let us first establish (A5). As (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), we have (†) for all 𝛽 ∈ [1, 𝛼],
                                                                               𝑞

(𝑠, ℎ) |= sizeR𝑞 ≥ 𝛽 iff (𝑠 ′, ℎ ′) |= sizeR𝑞 ≥ 𝛽 and (†) is equivalent to the statements below:
      • for all 𝛽 ∈ [1, 𝛼], card(Rem) ≥ 𝛽 iff card(Rem′) ≥ 𝛽 (by definition of |=),
      • min(𝛼, card(Rem)) = min(𝛼, card(Rem′)) (by a simple arithmetical reasoning).
Consequently, the condition (A5) holds true. Now, let us show (A1) and (A4). First, the statements
below are equivalent:
      • (ℓ, ℓ ′) ∈ E and Inter(ℓ, ℓ ′) = ∅,
      • (𝑠, ℎ) |= 𝑣 ↩→ 𝑣 ′, [[𝑣]] 𝑠,ℎ = ℓ and [[𝑣 ′]] 𝑠,ℎ = ℓ ′ for some 𝑣, 𝑣 ′ ∈ Terms𝑞 (by definition of |=),
                                         𝑞                  𝑞

      • (𝑠 , ℎ ) |= 𝑣 ↩→ 𝑣 , [[𝑣]] 𝑠 ′,ℎ′ = ℓ and [[𝑣 ′]] 𝑠 ′,ℎ′ = ℓ ′′′ for some 𝑣, 𝑣 ′ ∈ Terms𝑞 , for some
             ′    ′                ′               ′′
                                               𝑞                      𝑞

          locations ℓ ′′, ℓ ′′′, (by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′)),
                                                 𝑞

      • (𝑠 , ℎ ) |= 𝑣 ↩→ 𝑣 , [[𝑣]] 𝑠 ′,ℎ′ = 𝔣(ℓ) and [[𝑣 ′]] 𝑠 ′,ℎ′ = 𝔣(ℓ ′) for some 𝑣, 𝑣 ′ ∈ Terms𝑞 (by definition
             ′    ′             ′          𝑞                      𝑞

          of 𝔣),
      • (𝔣(ℓ), 𝔣(ℓ ′)) ∈ E′ and Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) = ∅ (by definition of |= and SG𝑞 (𝑠 ′, ℎ ′)).
Similarly, we have the following equivalences, where 𝛽 ∈ [1, 𝛼]:
      • (ℓ, ℓ ′) ∈ E and card(Inter(ℓ, ℓ ′)) ≥ 𝛽,
      • (𝑠, ℎ) |= sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1, [[𝑣]] 𝑠,ℎ = ℓ, [[𝑣 ′]] 𝑠,ℎ = ℓ ′ for some 𝑣, 𝑣 ′ ∈ Terms𝑞 (by definition
                                                    𝑞                   𝑞

          of |=),
      • (𝑠 ′, ℎ ′) |= sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1, [[𝑣]] 𝑠 ′,ℎ′ = ℓ ′′ and [[𝑣 ′]] 𝑠 ′,ℎ′ = ℓ ′′′ for some 𝑣, 𝑣 ′ ∈ Terms𝑞 , for
                                                       𝑞                       𝑞

          some locations ℓ ′′, ℓ ′′′, (by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′)),
                                                      𝑞

      • (𝑠 , ℎ ) |= sees𝑞 (𝑣, 𝑣 ) ≥ 𝛽 +1, [[𝑣]] 𝑠 ′,ℎ′ = 𝔣(ℓ), [[𝑣 ′]] 𝑠 ′,ℎ′ = 𝔣(ℓ ′) for some 𝑣, 𝑣 ′ ∈ Terms𝑞 , (by 𝔣),
             ′    ′                    ′            𝑞                      𝑞



                                        ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:30                                                    Stéphane Demri, Etienne Lozes, and Alessio Mansutti

    • (𝔣(ℓ), 𝔣(ℓ ′)) ∈ E′ and card(Inter′ (𝔣(ℓ), 𝔣(ℓ ′))) ≥ 𝛽 (by definition of |= and SG𝑞 (𝑠 ′, ℎ ′)).
Consequently, we get (A1) and (A4).
  We omit below the proof of the other direction as it is similar to the first direction.                                   □

   Now, we state the key intermediate result of the section that can be viewed as a distributivity
lemma. The expressive power of the test formulae allows us to mimic the separation between two
                                                        𝑞
equivalent memory states with respect to the relation ≈𝛼 . Separating conjunction can therefore be
eliminated from the logic in favour of test formulae, which is essential in the proof of Theorem 4.9.
   Lemma 4.8. Let 𝑞, 𝛼, 𝛼 1, 𝛼 2 ≥ 1 with 𝛼 = 𝛼 1 + 𝛼 2 and (𝑠, ℎ), (𝑠 ′, ℎ ′) be memory states such that
(𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′). For all heaps ℎ 1 , ℎ 2 such that ℎ = ℎ 1 +ℎ 2 , there are heaps ℎ 1′ , ℎ 2′ such that ℎ ′ = ℎ 1′ +ℎ 2′ ,
          𝑞

(𝑠, ℎ 1 ) ≈𝛼 1 (𝑠 ′, ℎ 1′ ) and (𝑠, ℎ 2 ) ≈𝛼 2 (𝑠 ′, ℎ 2′ ).
           𝑞                               𝑞


  The proof of Lemma 4.8 is rather long as it first constructs the subheaps ℎ 1′ and ℎ 2′ , and then check
that (𝑠, ℎ𝑖 ) ≈𝛼𝑖 (𝑠 ′, ℎ𝑖′) holds (for both 𝑖 ∈ {1, 2}) by verifying the conditions (A1)–(A5). Moreover,
               𝑞

the verification of some of the conditions requires first to establish additional preliminary properties.
Though the principle of the proof structure is quite simple, checking carefully each property is
quite lengthy. We believe that having all the material in a single proof is helpful to emphasize
the proof structure, or alternatively to skip the proof in a first reading of the document (see also
Appendix A).

   Proof. Let 𝑞, 𝛼, 𝛼 1 , 𝛼 2 , (𝑠, ℎ), (𝑠 ′, ℎ ′), ℎ 1 and ℎ 2 be defined as in the statement. Let
    • SG𝑞 (𝑠, ℎ) = (V, E, Alloc, TEq, Inter, Rem) and
    • SG𝑞 (𝑠 ′, ℎ ′) = (V′, E′, Alloc′, TEq′, Inter′, Rem′)
be the support graphs of (𝑠, ℎ) and (𝑠 ′, ℎ ′) respectively, with respect to 𝑞. As (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), let
                                                                                                              𝑞

𝔣 : V → V′ be a map satisfying (A1)–(A5) from Lemma 4.7. Below, for the sake of conciseness, let
𝑘 ∈ {1, 2} and let SG𝑞 (𝑠, ℎ𝑘 ) = (V𝑘 , E𝑘 , Alloc𝑘 , TEq𝑘 , Inter𝑘 , Rem𝑘 ) be the support graph of (𝑠, ℎ𝑘 ).
   The proof is rather long and can be summed up with the following steps.
   (1) First, we define a strategy to split ℎ ′ into ℎ 1′ and ℎ 2′ by closely following the way that ℎ is
       split into ℎ 1 and ℎ 2 . To do this, we look at the support graphs. For instance, suppose that
       Rem is split into two sets 𝑅1 ⊆ dom(ℎ 1 ) and 𝑅2 ⊆ dom(ℎ 2 ). By definition, it is quite easy to
       see that the sets 𝑅1 and 𝑅2 must be subsets of Rem1 and Rem2 , respectively. Then, following
       Lemma 4.7, to obtain (𝑠, ℎ𝑘 ) ≈𝛼𝑘 (𝑠 ′, ℎ𝑘′ ), we are required to split Rem′ into 𝑅1′ ⊆ dom(ℎ 1′ )
                                          𝑞

       and 𝑅2′ ⊆ dom(ℎ 2′ ) so that min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ )). Indeed, otherwise the
       equisatisfaction of the test formulae of the form sizeR𝑞 ≥ 𝛽 is not ensured (details on this
       are formalised later).
   (2) After defining ℎ 1′ and ℎ 2′ , we show that (𝑠, ℎ𝑘 ) ≈𝛼𝑘 (𝑠 ′, ℎ𝑘′ ). To do so, again, we follow
                                                                 𝑞

       Lemma 4.7 and we show that we can find suitable bijections from labelled locations of ℎ𝑘 to
       the ones of ℎ𝑘′ satisfying (A1)–(A5).
According to the summary above, let us first define explicitly ℎ 1′ and ℎ 2′ via an iterative process that
consists in adding locations to dom(ℎ 1′ ) or to dom(ℎ 2′ ). Whenever we enforce that ℓ ∈ dom(ℎ𝑘′ ),
                                def
implicitly we have ℎ𝑘′ (ℓ) = ℎ ′ (ℓ) as ℎ𝑘′ is intended to be a subheap of ℎ ′.
                                                 def
(CA) For all ℓ ∈ Alloc′, ℓ ∈ dom(ℎ𝑘′ ) ⇔ 𝔣−1 (ℓ) ∈ dom(ℎ𝑘 ). This step of the construction, as well
     as its usefulness, should be self-explanatory. For example, if (𝑠, ℎ𝑘 ) |= alloc(x𝑖 ) then, by
     relying on (A3), this step allows us to conclude that (𝑠 ′, ℎ𝑘′ ) |= alloc(x𝑖 ) (independently on
     how the definition of ℎ𝑘′ will be completed in the next steps of the construction).

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                 1:31

(CR) The heaps ℎ 1′ and ℎ 2′ are further populated depending on Rem. Let 𝑅𝑘 = Rem ∩ dom(ℎ𝑘 ). By
     definition, we have 𝑅1 ⊎ 𝑅2 = Rem. Below, we partition Rem′ into two sets 𝑅1′ and 𝑅2′ so that
     by definition 𝑅𝑘′ ⊆ dom(ℎ𝑘′ ). The strategy for defining the partition is split into three cases:
                                                                                                        def
      (CR.C1) If card(𝑅1 ) < 𝛼 1 then 𝑅1′ is a set of card(𝑅1 ) locations from Rem′ and 𝑅2′ = Rem′ \𝑅1′ .
      (CR.C2) Otherwise, if card(𝑅2 ) < 𝛼 2 then 𝑅2′ is a set of card(𝑅2 ) locations of Rem′ and
            def
        𝑅1′ = Rem′ \ 𝑅2′ .
      (CR.C3) Otherwise we have card(𝑅1 ) ≥ 𝛼 1 and card(𝑅2 ) ≥ 𝛼 2 . Then, 𝑅1′ is a set of 𝛼 1
                                           def
         locations from Rem′ and 𝑅2′ = Rem′ \ 𝑅1′ .
      It is easy to show that the construction satisfies the following property (where 𝑘 ∈ {1, 2}):
                                  min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ ))                                  (CR.P1)
      The property (CR.P1) directly follows from the property (A5) satisfied by 𝔣. The proof (that
      can be applied also for the next step of the construction, see (CI.P2)), works as follows.
      First, suppose that the sets of remaining locations in the heap domain are small, i.e.
                            min(𝛼, card(Rem)) = min(𝛼, card(Rem′)) < 𝛼 1 + 𝛼 2 .
      So, card(Rem) = card(Rem′) and therefore card(𝑅1 ) + card(𝑅2 ) = card(𝑅1′ ) + card(𝑅2′ ). By
      definition, card(𝑅1 ) = card(𝑅1′ ) and card(𝑅2 ) = card(𝑅2′ ) trivially hold for the cases (CR.C1)
      and (CR.C2), whereas the case (CR.C3) (card(𝑅1 ) ≥ 𝛼 1 and card(𝑅2 ) ≥ 𝛼 2 ) can never
      be applied since card(𝑅1 ) + card(𝑅2 ) < 𝛼 1 + 𝛼 2 . We conclude that min(𝛼𝑘 , card(𝑅𝑘 )) =
      min(𝛼𝑘 , card(𝑅𝑘′ )).
      Second, suppose instead
                            min(𝛼, card(Rem)) = min(𝛼, card(Rem′)) = 𝛼 1 + 𝛼 2 .
      If the first case (CR.C1) applies, i.e. card(𝑅1 ) < 𝛼 1 , then card(𝑅2 ) ≥ 𝛼 2 and by definition
      card(𝑅1′ ) = card(𝑅1 ). Then, card(𝑅2′ ) ≥ 𝛼 2 trivially follows from card(𝑅1′ ) + card(𝑅2′ ) ≥
      𝛼 1 + 𝛼 2 . Symmetrically, min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ )) holds when the second
      case (CR.C2) applies (card(𝑅2 ) < 𝛼 2 ). Lastly, suppose card(𝑅1 ) ≥ 𝛼 1 and card(𝑅2 ) ≥ 𝛼 2 .
      Then, the third case (CR.C3) applies and by definition card(𝑅1′ ) = 𝛼 1 . Again, we con-
      clude that min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ )) since card(𝑅2′ ) ≥ 𝛼 2 trivially follows
      from card(𝑅1′ ) + card(𝑅2′ ) ≥ 𝛼 1 + 𝛼 2 .
(CI) Lastly, the heaps ℎ 1′ and ℎ 2′ are further populated with respect to the memory cells in Inter(ℓ, ℓ ′).
                                   def
      For all (ℓ, ℓ ′) ∈ E, let 𝐿𝑘 = Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ). We have 𝐿1 ⊎ 𝐿2 = Inter(ℓ, ℓ ′). Below, we
      partition Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) into 𝐿1′ and 𝐿2′ so that by definition 𝐿𝑘′ ⊆ dom(ℎ𝑘′ ):
      (CI.C1) If card(𝐿1 ) < 𝛼 1 then 𝐿1′ is a set of card(𝐿1 ) locations from Inter′ (𝔣(ℓ), 𝔣(ℓ ′)), whereas
            def
        𝐿2′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) \ 𝐿1′ .
      (CI.C2) Else, if card(𝐿2 ) < 𝛼 2 then 𝐿2′ is a set of card(𝐿2 ) locations from Inter′ (𝔣(ℓ), 𝔣(ℓ ′)),
                      def
        whereas 𝐿1′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) \ 𝐿2′ .
      (CI.C3) Otherwise, we have card(𝐿1 ) ≥ 𝛼 1 and card(𝐿2 ) ≥ 𝛼 2 . Then 𝐿1′ is a set of 𝛼 1 locations
                                                 def
         from Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) and 𝐿2′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) \ 𝐿1′ .
      It is easy to show that the construction satisfies the following properties (where 𝑘 ∈ {1, 2}):
                               if 𝐿𝑘′ = ∅ then Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ⊆ dom(ℎ 3−𝑘
                                                                             ′
                                                                                 )                            (CI.P1)

                                  min(𝛼𝑘 , card(𝐿𝑘 )) = min(𝛼𝑘 , card(𝐿𝑘′ ))                                  (CI.P2)

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:32                                                      Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       (Proof of (CI.P1)) The first property trivially holds from the cases (CI.C1) and (CI.C2) of
       the construction. Notice that given 𝑘 ∈ {1, 2}, 3 − 𝑘 corresponds to the index in {1, 2} that is
       different from 𝑘.
       (Proof of (CI.P2)) The second property directly follows from (A4) (which is satisfied by 𝔣)
       and is proved as done for (CR.P1).
   This ends the construction of ℎ 1′ and ℎ 2′ as any location in dom(ℎ ′) has been assigned to one
of the two heaps. Indeed, {Alloc′, Rem′ } ∪ {Inter′ (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E′ } is a partition of dom(ℎ ′).
As (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), the support graphs SG𝑞 (𝑠, ℎ) and SG𝑞 (𝑠 ′, ℎ ′) witness the existence of a map
             𝑞

𝔣 : V → V′ satisfying (A1)–(A5) and therefore there is an underlying isomorphism between these
structures satisfying quantitative properties up to the value 𝛼. The construction above can be
understood as a way to split ℎ ′ into ℎ 1′ and ℎ 2′ mimicking the splitting of ℎ into ℎ 1 and ℎ 2 . It remains
to show below that this is done in a way that guarantees that (𝑠, ℎ𝑘 ) ≈𝛼𝑘 (𝑠 ′, ℎ𝑘′ ) (𝑘 ∈ {1, 2}).
                                                                              𝑞

   In the following, we denote the support graphs of (𝑠, ℎ𝑘 ) and (𝑠 ′, ℎ𝑘′ ) respectively as
     • SG𝑞 (𝑠, ℎ𝑘 ) = (V𝑘 , E𝑘 , Alloc𝑘 , TEq𝑘 , Inter𝑘 , Rem𝑘 ) and,
     • SG𝑞 (𝑠 ′, ℎ𝑘′ ) = (V𝑘′ , E𝑘′ , Alloc𝑘′ , TEq𝑘′ , Inter𝑘′ , Rem𝑘′ ).
   First, let us formalise an essential property of the construction of ℎ 1′ and ℎ 2′ .
(Paths) Let 𝑘 ∈ {1, 2} and let ℓ, ℓ ′ ∈ V be two labelled locations w.r.t. (𝑠, ℎ). ℎ𝑘 witnesses a non-
       empty path from ℓ to ℓ ′ if and only if ℎ𝑘′ witnesses a non-empty path from 𝔣(ℓ) to 𝔣(ℓ ′).

(Proof of (Paths)) The proof mainly relies on the properties (CI.P1) and (CI.P2) of the construction.
      Recall that 𝔣 : V → V′ is a bijection satisfying (A1)–(A5) w.r.t. (𝑠, ℎ) and (𝑠 ′, ℎ ′).
      (⇒) Let ℓ, ℓ ′ ∈ V be such that ℎ𝑘 witnesses a non-empty path from ℓ to ℓ ′. Since ℎ𝑘 ⊑ ℎ, then
      ℎ also witnesses a non-empty path from ℓ to ℓ ′. In particular, by Definition 4.4, this path
      corresponds to a path in the support graph SG𝑞 (𝑠, ℎ):
                         ℓ         E       ℓ1    E        ℓ2          ℓ𝑛−1     E          ℓ𝑛   E        ℓ′
                                                               ...
                             def                def
       Let us define ℓ0 = ℓ and ℓ𝑛+1 = ℓ ′. In particular, following the picture above, the support
       graph SG𝑞 (𝑠, ℎ) witnesses a path {(ℓ0, ℓ1 ), . . . , (ℓ𝑛 , ℓ𝑛+1 )} ⊆ E from ℓ0 to ℓ𝑛+1 . Since 𝔣 is a graph
       isomorphism from (V, E) to (V′, E′) (by (A1)), SG𝑞 (𝑠 ′, ℎ ′) witnesses a similar structure, as
       depicted below:
                ℓ=ℓ0           E           ℓ1    E        ℓ2          ℓ𝑛−1     E       ℓ𝑛      E        ℓ ′=ℓ𝑛+1
                                                               ...

                     𝔣                 𝔣              𝔣               𝔣               𝔣             𝔣

                                                               ...
                     𝔣(ℓ)      E′      𝔣(ℓ1 )   E′    𝔣(ℓ2 )         𝔣(ℓ𝑛−1 ) E
                                                                                ′
                                                                                      𝔣(ℓ𝑛 )   E′   𝔣(ℓ ′)
       Let us consider 𝑖 ∈ [0, 𝑛]. Since the path belongs to ℎ𝑘 , it must hold that ℓ𝑖 ∈ dom(ℎ𝑘 ) and
       Inter(ℓ𝑖 , ℓ𝑖+1 ) ⊆ dom(ℎ𝑘 ). We show that then 𝔣(ℓ𝑖 ) ∈ dom(ℎ𝑘′ ) and Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ⊆
       dom(ℎ𝑘′ ), which entails that ℎ𝑘′ witnesses a path from 𝔣(ℓ) to 𝔣(ℓ ′), concluding the proof.
       • From (ℓ𝑖 , ℓ𝑖+1 ) ∈ E, by Definition 4.4 we conclude that ℓ𝑖 ∈ V. Since ℓ𝑖 ∈ dom(ℎ), again by
         Definition 4.4, we have ℓ𝑖 ∈ Alloc and therefore by (A2), 𝔣(ℓ𝑖 ) ∈ Alloc′. By (CA) together
         with the fact that ℓ𝑖 ∈ dom(ℎ𝑘 ), we then conclude that 𝔣(ℓ𝑖 ) ∈ dom(ℎ𝑘′ ).
       • If Inter(ℓ𝑖 , ℓ𝑖+1 ) is empty then by (A4) Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) is also empty and the inclusion
         w.r.t. dom(ℎ𝑘′ ) trivially holds. Suppose now Inter(ℓ𝑖 , ℓ𝑖+1 ) is non-empty. From Inter(ℓ𝑖 , ℓ𝑖+1 ) ⊆
         dom(ℎ𝑘 ) and the fact that ℎ𝑘 and ℎ 3−𝑘 are disjoint we conclude that Inter(ℓ𝑖 , ℓ𝑖+1 ) ∩

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                             1:33

         dom(ℎ 3−𝑘 ) = ∅. Hence, by (CI.P2) we conclude that Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩ dom(ℎ 3−𝑘   ′ ) = ∅

         (notice that in (CI.P2), 𝐿3−𝑘 corresponds to Inter(ℓ𝑖 , ℓ𝑖+1 ) ∩ dom(ℎ 3−𝑘 ) whereas 𝐿3−𝑘     ′   cor-
                           ′                          ′                  ′                           ′
         responds to Inter (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩ dom(ℎ 3−𝑘 )). Since Inter (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩ dom(ℎ 3−𝑘 ) = ∅,
         by (CI.P1) we then conclude that Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ⊆ dom(ℎ𝑘′ ).
       (⇐) The right-to-left direction is analogous (thanks to the fact that 𝔣−1 is a graph isomorphism
       from (V′, E′) to (V, E)).

   Here is the last step of the proof. Given 𝑘 ∈ {1, 2}, let 𝔣𝑘 be the restriction of 𝔣 to V𝑘 and V𝑘′ .
We prove that 𝔣𝑘 satisfies (A1)–(A5) w.r.t. the memory states (𝑠, ℎ𝑘 ) and (𝑠 ′, ℎ𝑘′ ) and 𝛼𝑘 . Thanks
to Lemma 4.7, this implies (𝑠, ℎ 1 ) ≈𝛼 1 (𝑠 ′, ℎ 1′ ) and (𝑠, ℎ 2 ) ≈𝛼 2 (𝑠, ℎ 2′ ), ending the proof. Because of
                                      𝑞                               𝑞

lack of space, below we prove (A3) and the proofs for (A2), (A1), (A4) and (A5) can be found in
Appendix A.

𝔣𝑘 satisfies (A3): We prove that for every ℓ ∈ V, the set of terms corresponding to ℓ in (𝑠, ℎ𝑘 ) is
      equal to the set of terms corresponding to 𝔣(ℓ) in (𝑠 ′, ℎ𝑘′ ). Formally:
             for every ℓ ∈ V,
                (a) ℓ ∈ V𝑘 iff 𝔣(ℓ) ∈ V𝑘′ ;
               (b) if ℓ ∈ V𝑘 , TEq𝑘 (ℓ) = TEq𝑘′ (𝔣(ℓ)).
       Notice that (a) implies that 𝔣𝑘 (which we recall being the restriction of 𝔣 to V𝑘 and V𝑘′ ) is
       well-defined and it is a bijection from the labelled locations of (𝑠, ℎ𝑘 ) (i.e. V𝑘 ) to the labelled
       locations of (𝑠 ′, ℎ𝑘′ ) (i.e. V𝑘′ ). This is due to the fact that 𝔣 is a bijection from V to V′ and
       by Lemma 4.3, we have V𝑘 ⊆ V and V𝑘′ ⊆ V′. Again by V𝑘 ⊆ V (Lemma 4.3), (b) is then
       equivalent to (A3).
       We prove (a) and (b) together, by showing that for every ℓ ∈ V the set of terms corresponding
       to ℓ in (𝑠, ℎ𝑘 ) is equivalent to the set of terms corresponding to 𝔣(ℓ) in (𝑠 ′, ℎ𝑘′ ). We first show
       the result for program variables, and then for meet-points.
       (Program variables) Let ℓ ∈ V and 𝑖 ∈ [1, 𝑞]. It holds that x𝑖 ∈ TEq𝑘 (ℓ) if and only if 𝑠 (x𝑖 ) = ℓ,
       or equivalently x𝑖 ∈ TEq(ℓ) which, by (A3) in Lemma 4.7, holds whenever x𝑖 ∈ TEq′ (𝔣(ℓ)).
       The latter is equivalent to 𝑠 ′ (x𝑖 ) = 𝔣(ℓ), or equivalently x𝑖 ∈ TEq𝑘′ (𝔣(ℓ)).
       (Meet-points) In order to conclude the proof, we show that for all 𝑖, 𝑗 ∈ [1, 𝑞] and ℓ ∈ V,
                            𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 (ℓ) if and only if 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣(ℓ)).
       If [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is undefined, then so is [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ (by def.) and by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), so
                           𝑞                                                    𝑞                                     𝑞
                               𝑞                            𝑞                                            𝑞
       are [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ . By Lemma 4.3, if [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is undefined, then
                                   𝑞                      𝑞                        𝑞                             𝑞
       so are [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ , [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ , [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ . Otherwise,
                                     𝑘                            𝑘                 𝑘                             𝑘
       if [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = ℓ then by definition [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = ℓ ′ for some ℓ ′ ∈ V and moreover
                           𝑞                                                    𝑞

       [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣(ℓ) and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = 𝔣(ℓ ′) by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′). Let z𝑖 (resp. z 𝑗 )
                          𝑞                                    𝑞                          𝑞

       be the program variable in {x1, . . . , x𝑞 } such that 𝑠 (z𝑖 ) is the first location corresponding
                                                                                    𝑞                          𝑞
       to a program variable that is reachable from [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ (resp. [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ ), itself
       included. The characterisation of such a program variable z𝑖 can be captured by the formula
       firstvar(𝑚𝑞 (x𝑖 , x 𝑗 ), z𝑖 ) defined as the following Boolean combination of test formulae:
                                         ÜÓ                                             Ó
              𝑚𝑞 (x𝑖 , x 𝑗 ) = z𝑖 ∨            𝛿 ∈ [1,𝑛−1] sees𝑞 (𝑣 𝛿 , 𝑣 𝛿+1 ) ≥ 1 ∧ 𝑚<𝑛 x𝑘 ≠ 𝑣𝑚
                                                                                              𝑘 ∈ [1,𝑞 ]
                                  𝑣1 ,...,𝑣𝑛 ∈Terms𝑞 ,𝑛>1
                               pairwise distinct 𝑣1 ,...,𝑣𝑛−1 ,
                                   𝑣1 =𝑚𝑞 (x𝑖 ,x 𝑗 ),𝑣𝑛 =z𝑖


                                          ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:34                                                                Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       Indeed, this formula is satisfied only by memory states where there is a (possibly empty) path
       from the location corresponding to 𝑚𝑞 (x𝑖 , x 𝑗 ) to the location ℓ corresponding to z𝑖 so that
       each labelled location in the path, apart from ℓ, does not correspond to the interpretation of
       such program variables. Now, we recall the taxonomy of meet-points, where the rightmost
       case from Figure 5 is split into three cases, highlighting additional cases depending on z𝑖 and
       z𝑗 .
                 x𝑖       x𝑗             x𝑖        x𝑗              x𝑖                                           x𝑗                     x𝑖                     x𝑗


                                                                                                                                                   z𝑖
                                                                                                                                                        +
          𝑚𝑞 (x𝑖 ,x 𝑗 )           𝑚𝑞 (x𝑖 ,x 𝑗 )                                      x𝑗        x𝑖
                                                           𝑚𝑞 (x𝑖 ,x 𝑗 )                                       𝑚𝑞 (x 𝑗 ,x𝑖 )   𝑚𝑞 (x𝑖 ,x 𝑗 )                𝑚𝑞 (x 𝑗 ,x𝑖 )
          𝑚𝑞 (x 𝑗 ,x𝑖 )           𝑚𝑞 (x 𝑗 ,x𝑖 )
                                                                   +            +                   +              +                           +
                                                                                                                                                   z𝑗
                 z𝑖 = z 𝑗                 +                z𝑖 = z 𝑗                                                z𝑖 = z 𝑗
           z𝑖 not inside a loop

                                            z𝑖 = z 𝑗                       𝑚𝑞 (x 𝑗 ,x𝑖 )       𝑚𝑞 (x𝑖 ,x 𝑗 )


                (i)               (ii)                (iii)           (iv)                    (v)
       Distinct structures satisfy different test formulae, though they all satisfy the formula
                              firstvar(𝑚𝑞 (x𝑖 , x 𝑗 ), z𝑖 ) ∧ firstvar(𝑚𝑞 (x 𝑗 , x𝑖 ), z 𝑗 ).
       For instance, (i) is the only form not satisfying reach+ (z𝑖 , z𝑖 ) (recall that this form can be
       expressed as a Boolean combination of test formulae, as shown in Lemma 4.5), whereas (ii) can
       be distinguished as the only form satisfying both reach+ (z𝑖 , z𝑖 ) and 𝑚𝑞 (x𝑖 , x 𝑗 ) = 𝑚𝑞 (x 𝑗 , x𝑖 ).
       Moreover, the last structure is the only one satisfying z𝑖 ≠ z 𝑗 whereas (iii) and (iv) can
       be distinguished with a formula, similar to firstvar(𝑚𝑞 (x𝑖 , x 𝑗 ), z𝑖 ), stating that from the
       location corresponding to z𝑖 , it is possible to reach the location corresponding to 𝑚𝑞 (x𝑖 , x 𝑗 )
       without reaching the location corresponding to 𝑚𝑞 (x 𝑗 , x𝑖 ):
                    ÜÓ                                           Ó
                           𝛿 ∈ [1,𝑛−1] sees𝑞 (𝑣 𝛿 , 𝑣 𝛿+1 ) ≥ 1 ∧ 1<𝑚<𝑛 𝑚𝑞 (x 𝑗 , x𝑖 ) ≠ 𝑣𝑚 .
               𝑣1 ,...,𝑣𝑛 ∈Terms𝑞 , 𝑛>1
            pairwise distinct 𝑣1 ,...,𝑣𝑛−1 ,
                𝑣1 =z𝑖 ,𝑣𝑛 =𝑚𝑞 (x𝑖 ,x 𝑗 )

       Differently from (iii), the structure (iv) does not satisfy this formula. Since (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′),
                                                                                                                                                        𝑞

       the heaps ℎ and ℎ ′ agree on the structure of every meet-point. The proof that for all 𝑖, 𝑗 ∈ [1, 𝑞]
       and ℓ ∈ V, 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 (ℓ) iff 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣(ℓ)), essentially relies on (Paths). To
       show the result we need to proceed by cases, according to the taxonomy.
       Case: ℎ witnesses (i), (ii) or (iv). Since the heaps ℎ and ℎ ′ agree on the structure of every
         meet-point, ℎ ′ also witnesses the same form among (i), (ii) and (iv) as ℎ. Regarding ℎ𝑘 , one
         of the following holds:
         • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are both preserved in ℎ𝑘 .
           Then ℎ𝑘 witnesses (i) (ii) or (iv). By (Paths) the same holds for ℎ𝑘′ . In every case ((i), (ii)
                                                              𝑞                     𝑞                         𝑞
           and (iv)), we conclude that [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ =
                                                                                           𝑘                                                                       𝑘
                                  𝑞                                     𝑞
              [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ). Then,
                                                                                                        𝑞
                                              𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )
                                              𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )).
                                                                                                               𝑞


          • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) or the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are not preserved in ℎ𝑘 .
            Then, again by (Paths), the same holds for ℎ𝑘′ with respect to (𝑠 ′, ℎ ′). By definition of
                                                 𝑞                          𝑞
            meet-points, both [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ are therefore not defined.
                                                                       𝑘                                               𝑘


ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                            1:35

     Case: ℎ witnesses (iii). If instead ℎ and ℎ ′ witness (iii) then one of the following holds.
                                                                                             𝑞
      • ℎ𝑘 also witnesses (iii), meaning that the path from 𝑠 (x𝑖 ) to [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ and the path
        from 𝑠 (x 𝑗 ) to [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ are both preserved in ℎ𝑘 . Then by (Paths) the heap ℎ𝑘′
                                            𝑞
                                                          𝑞                       𝑞                          𝑞
        also witnesses (iii). We have [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ =
                                                                         𝑘                                                   𝑘
                             𝑞                               𝑞
          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ). We conclude that
                                                                                   𝑞
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )
                                                                                        𝑘

                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )).
                                                                                        𝑞
                                                                                            𝑘

       • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z𝑖 ) are preserved in ℎ𝑘 , whereas
                                                     𝑞
         the path from 𝑠 (z𝑖 ) to [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is not preserved in ℎ𝑘 (i.e. at least one of its
         locations is assigned to the other heap ℎ 3−𝑘 ). Then ℎ𝑘 witnesses (i) and by definition of
         meet-points, it holds that
                                             𝑞                           𝑞                           𝑞
                           [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ
                                                 𝑘                           𝑘

          By (Paths), ℎ𝑘′ also witnesses (i). Then,
                            𝑞                            𝑞                              𝑞                           𝑞
          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ ).
                                 𝑘                           𝑘

          Then, we conclude that
                                                                                    𝑞
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )).
                                                                                        𝑞


      • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) or the path from 𝑠 (x 𝑗 ) to 𝑠 (z𝑖 ) are not preserved in ℎ𝑘 . Then,
        by (Paths), the same holds for ℎ𝑘′ with respect to (𝑠 ′, ℎ ′). By definition of meet-points,
                                    𝑞                            𝑞
        neither [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ nor [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ is defined.
                                      𝑘                             𝑘
     Case: ℎ witnesses (v). Lastly, suppose that ℎ and ℎ ′ witness (v). One of the following holds.
      • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z𝑖 ) are both preserved in
                                                                                                                      𝑞
        ℎ𝑘 . Then, depending on whether or not the path from 𝑠 (z𝑖 ) to [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ is also
        preserved, ℎ𝑘 witnesses (i) or (v). From (Paths), the same holds for ℎ𝑘 (where ℎ𝑘′ wit-           ′
                                                                                                                          𝑞
        nesses (i) iff ℎ𝑘 witnesses (i)). In both cases ((i) and (v)), it holds that [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ =
                                                                                                                            𝑘
                           𝑞                          𝑞                           𝑞                              𝑞
        [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ). Then,
                                                                 𝑘
                                                                                    𝑞
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )).
                                                                                        𝑞


       • The path from 𝑠 (x𝑖 ) to 𝑠 (z 𝑗 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are preserved in ℎ𝑘 , whereas
                                                      𝑞
         the path from 𝑠 (z 𝑗 ) to [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is not preserved in ℎ𝑘 . Then ℎ𝑘 witnesses (i) and
         by definition of meet-points, it holds that
                                             𝑞                           𝑞                          𝑞
                          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ .
                                                 𝑘                           𝑘

          By (Paths), the heap ℎ𝑘′ also witnesses (i). Then,
                             𝑞                           𝑞                              𝑞                           𝑞
          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )
                                 𝑘                               𝑘

          Then, we conclude that
                                                                                    𝑞
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )
                                     𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )).
                                                                                        𝑞



                                        ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:36                                                        Stéphane Demri, Etienne Lozes, and Alessio Mansutti

           • The path from 𝑠 (x𝑖 ) to 𝑠 (z 𝑗 ) or the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) is not preserved in ℎ𝑘 . Then,
              by (Paths), the same holds for ℎ𝑘′ with respect to (𝑠 ′, ℎ ′). By definition of meet-points,
                                         𝑞                       𝑞
              both [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ are undefined.
                                           𝑘                          𝑘
         We conclude that for every ℓ ∈ V, 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 (ℓ) if and only if 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣(ℓ)).
   This concludes the proof: for the support graphs of ℎ𝑘 and ℎ𝑘′ , 𝔣 restricted to the domain V𝑘 and
the codomain V𝑘′ satisfies all conditions of Lemma 4.7 with respect to 𝛼𝑘 . Therefore, it holds that
(𝑠, ℎ 1 ) ≈𝛼 1 (𝑠 ′, ℎ 1′ ) and (𝑠, ℎ 2 ) ≈𝛼 2 (𝑠 ′, ℎ 2′ ).
           𝑞                               𝑞
                                                                                                                 □
   Thanks to Lemma 4.8, we can now characterise every formula of SL(∗, reach+ ) by a Boolean
combination of test formulae in Test(𝑞, 𝛼), where 𝛼 is related to the memory size msize(𝜑) of a
formula 𝜑 in SL(∗, reach+ ) defined as follows (see also [41]):
                    def                                                                   def
    • msize(𝜋) = 1 for any atomic formula 𝜋,                                 • msize(¬𝜓 ) = msize(𝜓 ),
                    def                                                                       def
    • msize(𝜓 ∧𝜓 ′) = max(msize(𝜓 ), msize(𝜓 ′)),                            • msize(𝜓 ∗ 𝜓 ′) = msize(𝜓 ) + msize(𝜓 ′).
  We have 1 ≤ msize(𝜑) ≤ |𝜑 |, where |𝜑 | is the size of the syntax tree for 𝜑. Below, we establish
the characterisation of SL(∗, reach+ ) formulae in terms of test formulae.
  Theorem 4.9. Let 𝜑 be in SL(∗, reach+ ) built over the variables x1, . . . , x𝑞 . For all 𝛼 ≥ msize(𝜑)
and all memory states (𝑠, ℎ), (𝑠 ′, ℎ ′) such that (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), we have (𝑠, ℎ) |= 𝜑 iff (𝑠 ′, ℎ ′) |= 𝜑.
                                                           𝑞


   Proof. Assume that 𝜑 is a formula with msize(𝜑) ≤ 𝛼 and (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′). By structural
                                                                                                𝑞

induction we show that (𝑠, ℎ) |= 𝜑 iff (𝑠 ′, ℎ ′) |= 𝜑. It is sufficient to establish one direction of the
equivalence thanks to its symmetry. First, note that (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) implies that (𝑠, ℎ) and (𝑠 ′, ℎ ′)
                                                                   𝑞

agree on the satisfaction of Boolean combinations built over atomic formulae in Test(𝑞, 𝛼). Indeed,
at the atomic level, this is exactly what (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) means, whereas for Boolean connectives ¬
                                                   𝑞

and ∧, this is also straighforward by induction.
   The basic cases for the atomic formulae x𝑖 ↩→ x 𝑗 and x𝑖 = x 𝑗 are immediate since these are
test formulae. For emp and reach+ (x𝑖 , x 𝑗 ) we use directly Lemma 4.5. Suppose 𝜓 = emp. Then
msize(𝜓 ) = 1 ≤ 𝛼 and we can express emp with the Boolean combination of test formulae
                                                      Û
                                     ¬sizeR𝑞 ≥ 1 ∧        ¬alloc(x𝑖 ),
                                                                𝑖 ∈ [1,𝑞 ]

as shown in the proof of Lemma 4.5. Notice that all the test formulae appearing in the formula
above are from Test(𝑞, 1). Thus, from (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) we conclude that (𝑠, ℎ) |= 𝜓 iff (𝑠 ′, ℎ ′) |= 𝜓 .
                                                 𝑞
                                     +
  Similarly, suppose that 𝜓 = reach (x𝑖 , x 𝑗 ). Then msize(𝜓 ) = 1 ≤ 𝛼 and we can express 𝜓 with
the Boolean combination of test formulae:
                                ÜÓ
                                      𝛿 ∈ [1,𝑛−1] sees𝑞 (𝑣 𝛿 , 𝑣 𝛿+1 ) ≥ 1,
                                  𝑣1 ,...,𝑣𝑛 ∈Terms𝑞 ,
                             pairwise distinct 𝑣1 ,...,𝑣𝑛−1 ,
                                      x𝑖 =𝑣1 ,x 𝑗 =𝑣𝑛

as shown in the proof of Lemma 4.5. As in the case for the formula emp, notice that all the test
formulae appearing in the formula above are from Test(𝑞, 1). Again, from (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) we
                                                                                                                𝑞

conclude that (𝑠, ℎ) |= 𝜓 iff (𝑠 ′, ℎ ′) |= 𝜓 .
     We omit the obvious cases with the Boolean connectives. Let us consider the last case 𝜓 = 𝜓 1 ∗𝜓 2 .
Suppose that (𝑠, ℎ) |= 𝜓 1 ∗𝜓 2 and msize(𝜓 1 ∗𝜓 2 ) ≤ 𝛼. There are heaps ℎ 1 and ℎ 2 such that ℎ = ℎ 1 +ℎ 2 ,
(𝑠, ℎ 1 ) |= 𝜓 1 and (𝑠, ℎ 2 ) |= 𝜓 2 . As 𝛼 ≥ msize(𝜓 1 ∗𝜓 2 ) = msize(𝜓 1 ) + msize(𝜓 2 ), there exist 𝛼 1 and 𝛼 2
such that 𝛼 = 𝛼 1 + 𝛼 2 , 𝛼 1 ≥ msize(𝜓 1 ) and 𝛼 2 ≥ msize(𝜓 2 ). By Lemma 4.8, there exist heaps ℎ 1′ and
ℎ 2′ such that ℎ ′ = ℎ 1′ + ℎ 2′ , (𝑠, ℎ 1 ) ≈𝛼 1 (𝑠 ′, ℎ 1′ ) and (𝑠, ℎ 2 ) ≈𝛼 2 (𝑠 ′, ℎ 2′ ). By the induction hypothesis,
                                               𝑞                              𝑞

we get (𝑠 ′, ℎ 1′ ) |= 𝜓 1 and (𝑠 ′, ℎ 2′ ) |= 𝜓 2 . Consequently, we obtain (𝑠 ′, ℎ ′) |= 𝜓 1 ∗ 𝜓 2 .                    □

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                   1:37

   As an example, we can apply this result to the memory states from Figure 4, page 23. We have
already shown how we can distinguish (𝑠 1, ℎ 1 ) from (𝑠 2, ℎ 2 ) using a formula with only one separating
conjunction. Theorem 4.9 ensures that these two memory states do not satisfy the same set of test
formulae for 𝛼 ≥ 2. Indeed, only (𝑠 1, ℎ 1 ) satisfies sees𝑞 (x𝑖 , x 𝑗 ) ≥ 2. The same argument can be
used with (𝑠 3, ℎ 3 ) and (𝑠 4, ℎ 4 ): only (𝑠 3, ℎ 3 ) satisfies the test formula 𝑚𝑞 (x𝑖 , x 𝑗 ) ↩→ 𝑚𝑞 (x 𝑗 , x𝑖 ). As a
result, we can relate separation logic with classical logic, as advocated in the works [11, 17, 21, 29]
and shown with the following theorem.
   Theorem 4.10. Let 𝜑 be a formula in SL(∗, reach+ ) built over the variables in x1 , . . . , x𝑞 . The
formula 𝜑 is logically equivalent to a Boolean combination of test formulae from Test(𝑞, msize(𝜑)).
  Proof. The proof is rather standard. Let 𝛼 = msize(𝜑). Given a memory state (𝑠, ℎ), we write
LIT(𝑠, ℎ) to denote the following set of literals:
                {𝜓 ∈ Test(𝑞, 𝛼) | (𝑠, ℎ) |= 𝜓 } ∪ {¬𝜓 | (𝑠, ℎ) ̸ |= 𝜓 with 𝜓 ∈ Test(𝑞, 𝛼)}.
Since Test(𝑞, 𝛼) is a finite set, LIT(𝑠, ℎ) is finite too and let us consider the well-defined formula
Ó
  𝜓 ∈LIT(𝑠,ℎ) 𝜓 . We have the following equivalence:
                                              Û
                                (𝑠 ′, ℎ ′) |=   𝜓 iff (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′).
                                                                 𝑞

                                            𝜓 ∈LIT(𝑠,ℎ)
                     def Ô
The expression 𝜓 ′ = (𝑠,ℎ) |=𝜑 ( 𝜓 ∈LIT(𝑠,ℎ) 𝜓 ) is equivalent to a Boolean combination 𝜑 ′ of formulae
                                  Ó
from Test(𝑞, 𝛼) because LIT(𝑠, ℎ) ranges over the finite set of elements from Test(𝑞, 𝛼) (just select
a finite amount of disjuncts).     Though the number of memory states is infinite, the number of
formulae of the form ( 𝜓 ∈LIT(𝑠,ℎ) 𝜓 ) is finite and therefore, we understand 𝜓 ′ as a finite disjunction.
                          Ó
This is not a constructive way to define 𝜓 ′ (which can be also done by some other means) but this
is sufficient for the existence. By Theorem 4.9, the formula 𝜑 is logically equivalent                 ′
                                                                                               Ó to 𝜓 , which
concludes the proof. Indeed, suppose that (𝑠, ℎ) |= 𝜑. Obviously, we get (𝑠, ℎ) |= 𝜓 ∈LIT(𝑠,ℎ) 𝜓 and
therefore (𝑠, ℎ) |= 𝜓 ′. Conversely, supposeÓ that (𝑠, ℎ) |= 𝜓 ′. This means that there is a memory state
(𝑠 , ℎ ) such that (𝑠 , ℎ ) |= 𝜑 and (𝑠, ℎ) |= 𝜓 ∈LIT(𝑠 ′,ℎ′ ) 𝜓 . Thus (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), msize(𝜑) ≤ 𝛼 and
   ′  ′               ′   ′                                                     𝑞
          ′ ′
since (𝑠 , ℎ ) |= 𝜑, by Theorem 4.9 we get (𝑠, ℎ) |= 𝜑.                                                      □

   It is now possible to establish a small heap property of SL(∗, reach+ ) by inheriting it from the
small heap property for Boolean combinations of test formulae, which is analogous to the small
model property for other theories of singly linked lists, see e.g. [14, 35]. Indeed, following Lemma 4.7,
now it is straightforward to derive an upper bound on the size of a small model satisfying a formula
in SL(∗, reach+ ).
   Let P(𝑞, 𝑛) be the polynomial (𝑞 2 + 𝑞) · (𝑛 + 1) + 𝑛 used in the sequel.
  Theorem 4.11. Let 𝜑 be a satisfiable SL(∗, reach+ ) formula built over x1 , . . . , x𝑞 . There is (𝑠, ℎ)
such that (𝑠, ℎ) |= 𝜑 and card(dom(ℎ)) ≤ P(𝑞, |𝜑 |).
   Proof. Let 𝜑 be a formula built over x1, . . . , x𝑞 with 𝛼 = msize(𝜑) ≤ |𝜑 | and let (𝑠, ℎ) be a
memory state satisfying 𝜑. Let (V, E, Alloc, TEq, Inter, Rem) be equal to SG𝑞 (𝑠, ℎ) with respect
to 𝑞 and ℓ ∗ be an arbitrary location not in the domain of ℎ. We construct a heap ℎ ′ such that
card(dom(ℎ ′)) ≤ P(𝑞, |𝜑 |) and (𝑠, ℎ ′) |= 𝜑.
                                                                                                              def
   (1) Let 𝑅 ⊆ Rem be a set of min(𝛼, card(Rem)) locations. For all ℓ ∈ Rem, ℓ ∈ dom(ℎ ′) ⇔ ℓ ∈ 𝑅
                                          def
       and for all ℓ ∈ 𝑅, we have ℎ ′ (ℓ) = ℓ ∗ . As it will be soon clear, these locations in 𝑅 will happen
       to be the only ones in Rem′ (from ℎ ′). In that way, (𝑠, ℎ) and (𝑠, ℎ ′) shall agree on all test
       formulae of the form sizeR𝑞 ≥ 𝛽 with 𝛽 ∈ [1, 𝛼].

                                      ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:38                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

   (2) For all (ℓ, ℓ ′) ∈ E, let 𝐿 = {ℓ1, . . . , ℓ𝐴 } be a set of 𝐴 = min(𝛼, card(Inter(ℓ, ℓ ′))) locations
       in Inter(ℓ, ℓ ′). Notice that if card(Inter(ℓ, ℓ ′)) ≥ 𝛼, then 𝐴 = 𝛼, else 𝐴 = card(Inter(ℓ, ℓ ′)).
                                                            def                       def
       Then, for all ℓ¯ ∈ Inter(ℓ, ℓ ′), ℓ¯ ∈ dom(ℎ ′) ⇔ ℓ¯ ∈ 𝐿. Moreover ℎ ′ (ℓ) = ℓ1 (and therefore
                                  def                                           def
        ℓ ∈ dom(ℎ ′)), ℎ ′ (ℓ𝛼 ) = ℓ ′ and for all 𝑖 ∈ [1, 𝛼 − 1], ℎ ′ (ℓ𝑖 ) = ℓ𝑖+1 . Since all the locations in
        Inter(ℓ, ℓ ′) are not labelled locations and we preserve the existence of paths between labelled
                                                                                            𝑞          𝑞
        locations, this step guarantees that for all 𝑣 ∈ Terms𝑞 , we have [[𝑣]] 𝑠,ℎ = [[𝑣]] 𝑠,ℎ′ . This
        implies that (𝑠, ℎ) and (𝑠, ℎ ′) satisfy the same set of test formulae of the form 𝑣 = 𝑣 ′, where
       𝑣, 𝑣 ′ ∈ Terms𝑞 . Furthermore, the path from ℓ to ℓ ′ in ℎ ′ has length min(𝛼, card(Inter(ℓ, ℓ ′)))+1.
        Consequently, for all 𝛽 ∈ [1, 𝛼] and for all 𝑣, 𝑣 ′ ∈ Terms𝑞 , (𝑠, ℎ ′) |= sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1 if and
        only if (𝑠, ℎ) |= sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1, and these two memory states agree on the test formulae
        of the form 𝑣 ↩→ 𝑣 ′. As card(Terms𝑞 ) = 𝑞 2 + 𝑞, with this construction, each path between
        two labelled locations has at most length 𝛼 + 1. Additionally, the heap graphs are functional,
        and therefore (𝑠, ℎ) |= sees𝑞 (𝑣, 𝑣 1 ) ≥ 𝛽 1 + 1 ∧ sees𝑞 (𝑣, 𝑣 2 ) ≥ 𝛽 2 + 1 implies 𝑣 1 = 𝑣 2 , which
        entails that this step adds less than (𝑞 2 + 𝑞) (|𝜑 | + 1) locations to dom(ℎ ′).
                                            def
   (3) Lastly, for all ℓ ∈ Alloc, ℎ ′ (ℓ) = ℎ(ℓ) and therefore ℓ ∈ dom(ℎ ′). So, for all 𝑣 ∈ Terms𝑞
              ′
        (𝑠, ℎ ) |= alloc(𝑣) if and only if (𝑠, ℎ) |= alloc(𝑣). After this step, this implies that the two
        memory states satisfy the same set of test formulae. Note that in the computation of the
        upper bound, there is no need to take into account the location introduced in this step, since
        the upper bound mentioned in the previous step already includes this case.
It follows that ℎ ′ is a heap such that card(dom(ℎ ′)) ≤ (𝑞 2 + 𝑞) · (|𝜑 | + 1) + |𝜑 | and (𝑠, ℎ ′) |= 𝜑. □

4.3    Complexity upper bounds
Let us draw some consequences of Theorem 4.11. First, for the logic SL(∗, reach+ ), we get a PSpace
upper bound, which matches the lower bound for SL(∗) [12]. Indeed, SL(∗) is a syntactic fragment
of SL(∗, reach+ ) and the satisfiability problem for SL(∗) is shown PSpace-hard in [12].
   Theorem 4.12. The satisfiability problem for SL(∗, reach+ ) is PSpace-complete.
   Proof. Let 𝜑 be a formula in SL(∗, reach+ ) built over x1, . . . , x𝑞 . By Theorem 4.11, 𝜑 is sat-
isfiable if and only if there is a memory state satisfying 𝜑 with card(dom(ℎ)) ≤ P(𝑞, |𝜑 |). The
non-deterministic polynomial-space algorithm (leading to the PSpace upper bound by Savitch’s
Theorem [37]) works as follows. First, guess a heap ℎ with card(dom(ℎ)) ≤ P(𝑞, |𝜑 |) and dom(ℎ) ∪
ran(ℎ) ⊆ [0, 2 × P(𝑞, |𝜑 |)] and a store restricted to x1, . . . , x𝑞 such that ran(𝑠) ⊆ [0, 2 × P(𝑞, |𝜑 |) +𝑞]
(in the worst case, all the variables have different values, and the memory cells have different values
too).
   Then, checking whether (𝑠, ℎ) |= 𝜑 can be done in polynomial-space as for the standard SL(∗)
by using a recursive algorithm that internalises the semantics (see e.g. [12]): the recursive depth is
linear and at each call, the algorithm uses at most linear space in the size of (𝑠, ℎ) and 𝜑, which
is polynomial in |𝜑 |. We only need to guarantee that (𝑠, ℎ) |= reach+ (x, y) can be checked in
polynomial space, actually this can be done in polynomial time in the size of (𝑠, ℎ), that is therefore
in polynomial space in |𝜑 |.                                                                                  □

  Besides, we may consider restricting the usage of Boolean connectives. Let us briefly define the
symbolic heap fragment formulae 𝜑 as conjunctions Π ∧ Σ where Π is a pure formula and Σ is a
spatial formula Σ:
                               Π ::=⊥ | ⊤ | x𝑖 = x 𝑗 | ¬(x𝑖 = x 𝑗 ) | Π ∧ Π
                               Σ ::= emp | ⊤ | x𝑖 ↦→ x 𝑗 | ls(x𝑖 , x 𝑗 ) | Σ ∗ Σ

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                               1:39

As usual, x𝑖 ↦→ x 𝑗 is interpreted as the exact points-to relation. We write Bool(SHF) to denote the
set of Boolean combinations of formulae from the symbolic heap fragment [2]. A PTime upper
bound for the entailment/satisfiability problem for the symbolic heap fragment is successfully
solved in [13, 22], whereas the satisfiability problem for a slight variant of Bool(SHF) is shown in
NP in [34, Theorem 4]. This NP upper bound can be obtained as a by-product of Theorem 4.11.
  Corollary 4.13. The satisfiability problem for Bool(SHF) is NP-complete.
   Proof. The NP-hardness is obtained thanks to the presence of equalities and Boolean connectives.
Indeed, let us show how to simply reduce SAT to the satisfiability problem for Bool(SHF). Let 𝜑 be
a formula from the propositional calculus built over the propositional variables 𝑝 1 , . . . , 𝑝𝑛 . Let us
                                               def
define the translation T such that T(𝑝𝑖 ) = x𝑖 = y𝑖 (x𝑖 and y𝑖 are program variables dedicated to 𝑝𝑖 )
and T is homomorphic for Boolean connectives. It is easy to prove that 𝜑 is satisfiable iff T(𝜑) is
satisfiable.
   As far as the complexity upper bound is concerned, let 𝜑 be a Boolean combination of pure or
spatial formulae built over x1, . . . , x𝑞 . By Theorem 4.11, 𝜑 is satisfiable iff there is (𝑠, ℎ) satisfying 𝜑
with card(dom(ℎ)) ≤ P(𝑞, |𝜓 |), where 𝜓 is the translation of 𝜑 where
    • every occurrences of x𝑖 ↦→ x 𝑗 is rewritten as the equivalent formula x𝑖 ↩→ x 𝑗 ∧ size = 1, and
    • every ls(x𝑖 , x 𝑗 ) is rewritten as the equivalent formula
              (x𝑖 = x 𝑗 ∧ emp) ∨ (x𝑖 ≠ x 𝑗 ∧ reach+ (x𝑖 , x 𝑗 ) ∧ ¬(¬emp ∗ reach+ (x𝑖 , x 𝑗 ))).
This technicality is introduced as Theorem 4.9 requires 𝜑 to be in SL(∗, reach+ ) and, as such, the
formula 𝜓 is not then used to check for satisfiability.
   The non-deterministic polynomial-time algorithm works as follows. Similarly to the proof of
Theorem 4.12, guess a heap ℎ with card(dom(ℎ)) ≤ P(𝑞, |𝜓 |), dom(ℎ) ∪ ran(ℎ) ⊆ [0, 2 × P(𝑞, |𝜓 |)]
and a store restricted to x1, . . . , x𝑞 and such that ran(𝑠) ⊆ [0, 2 × P(𝑞, |𝜓 |) + 𝑞]. Then, confirming
that the valuation is correct can be done in PTime: checking whether a pure formula is satisfied
by (𝑠, ℎ) can be done in linear time. Similarly, checking whether a spatial formula Σ is satisfied by
(𝑠, ℎ) can be done in PTime [2, Lemma 1]. So, the satisfiability problem for Boolean combinations
of symbolic heap fragment formulae can be solved in NP.                                                 □
   We have seen that we can take advantage of the small heap property to derive complexity results
for fragments of SL(∗, reach+ ). However, it is also possible to push further the PSpace upper bound
by allowing occurrences of −∗ in a controlled way (as unrestricted use of the magic wand leads to
undecidability, see Theorem 3.12). The following result can be shown thanks to Proposition 4.1 and
Lemma 4.5.
  Lemma 4.14. Let 𝜑 be in SL(∗, −∗) built over x1 , . . . , x𝑞 . The formula 𝜑 is logically equivalent to a
Boolean combination of test formulae from Test(𝑞, 2|𝜑 |).
  Proof. First, translate 𝜑 into a Boolean combination of formulae from
               x𝑖 = x 𝑗             alloc(x𝑖 )                x𝑖 ↩→ x 𝑗                size ≥ 𝛽,
as stated in Proposition 4.1 and 𝛽 ≤ 2|𝜑 |. Then, rewrite every occurrence of size ≥ 𝛽 into the
equivalent Boolean combination of test formulae shown in Lemma 4.5. The resulting formula is in
Test(𝑞, 2|𝜑 |).                                                                               □
   Let SL(∗, reach+, 𝑞,𝛼 Test(𝑞, 𝛼)) be the extension of SL(∗, reach+ ) augmented with the test
                    Ð
formulae. The memory size function is extended as follows.




                                  ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:40                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

                              def                                                     def
    • msize(alloc(𝑣)) = 1,                                        • msize(𝑣 ↩→ 𝑣 ′) = 1,
                                    def                                                def
    • msize(sees𝑞 (𝑣, 𝑣 ′) ≥ 𝛽 + 1) = 𝛽 + 1,                      • msize(sizeR ≥ 𝛽) = 𝛽.
   When formulae are encoded as trees, we have 1 ≤ msize(𝜑) ≤ |𝜑 |𝛼Ð       𝜑 where 𝛼𝜑 is the maximal
constant in 𝜑. Theorem 4.10 admits a counterpart for SL(∗, reach+, 𝑞,𝛼 Test(𝑞, 𝛼)) and conse-
quently, any formula built over x1 , . . . , x𝑞 can be shown equivalent to a Boolean combination
of test formulae from Test(𝑞, |𝜑 |𝛼𝜑 ). By Theorem 4.11, any satisfiable formula has therefore a
model with card(dom(ℎ))     ≤ (𝑞 2 + 𝑞) · (|𝜑 |𝛼𝜑 + 1) + |𝜑 |𝛼𝜑 . Hence, the satisfiability problem for
             +
               Ð
SL(∗, reach , 𝑞,𝛼 Test(𝑞, 𝛼)) is in PSpace when the constants are encoded in unary. Then, we
conclude by stating the new PSpace upper bound for Boolean combinations of formulae from
SL(∗, −∗) ∪ SL(∗, reach+ ).
  Theorem 4.15. The satisfiability problem for Boolean combinations of formulae from SL(∗, −∗) ∪
SL(∗, reach+ ) is PSpace-complete.
   Proof. Let 𝜑 be a Boolean combination of formulae from SL(∗, −∗) ∪ SL(∗, reach+ ). First, replace
every maximal subformula 𝜓 in SL(∗, −∗) by an equivalent Boolean combination of test formulae
from Test(𝑞, 2|𝜓 |), as shown by Lemma 4.14. This replacement may require exponential time in the
worst case but this is still fine to establish the PSpace upper Ð bound as we aim at showing a small
heap property. We obtain a formula 𝜑 ′ in SL(∗, reach+, 𝑞,𝛼 Test(𝑞, 𝛼)) with 𝛼𝜑 ′ ≤ 2|𝜑 |. So, 𝜑 is
satisfiable iff 𝜑 has a model (𝑠, ℎ) with card(dom(ℎ)) ≤ P(𝑞, 2|𝜑 |𝛼𝜑 ′ ), which is still polynomial in
|𝜑 |. Again, the non-deterministic polynomial-space algorithm works as follows. First, guess a small
heap ℎ with card(dom(ℎ)) ≤ P(𝑞, 2|𝜑 |𝛼𝜑 ′ ), dom(ℎ) ∪ ran(ℎ) ⊆ [0, 2 × P(𝑞, 2|𝜑 |𝛼𝜑 ′ )] and a store
restricted to x1, . . . , x𝑞 and such that ran(𝑠) ⊆ [0, 2 × P(𝑞, 2|𝜑 |𝛼𝜑 ′ ) + 𝑞]. Since the respective model-
checking problem for SL(∗, −∗) and SL(∗, reach+ ) are both in PSpace (see [12] and Theorem 4.12)
and (𝑠, ℎ) is of polynomial size in |𝜑 |, checking whether (𝑠, ℎ) |= 𝜑 can be done in PSpace by
performing several instances of the model-checking problem with maximal subformulae 𝜓 from
either SL(∗, −∗) or SL(∗, reach+ ).                                                                         □

   The fragment from Theorem 4.15 forbids formulae with ls in the scope of the separating
implication −∗. A fragment with ls in the scope of −∗ is considered in [40] but decidability is still
open. By contrast, a recent work [30] has established a PSpace upper bound for fragments with ls
in the scope of −∗ but restrictions apply (full proofs soon available in [31]).

5   CONCLUSION
We studied the effects of adding ls to SL(∗, −∗), giving us the opportunity to consider several
variants. SL(∗, −∗, ls) is shown undecidable (Theorem 3.12) and non-finitely axiomatisable, which
remains quite unexpected since there are no first-order quantifications. This result is strengthened
to even weaker extensions of SL(∗, −∗) such as the one augmented with 𝑛(x) = 𝑛(y), 𝑛(x) ↩→ 𝑛(y)
and alloc−1 (x), or the one augmented with reach(x, y) = 2 and reach(x, y) = 3. If the magic wand
is discarded, we have established that the satisfiability problem for SL(∗, ls) is PSpace-complete
by introducing a class of test formulae that captures the expressive power of SL(∗, ls) and that
leads to a small heap property. Such a logic contains the Boolean combinations of symbolic heaps
and our proof technique allows us to get an NP upper bound for such formulae. Moreover, we
have shown that the satisfiability problem for SL(∗, −∗, reach+ ) restricted to Boolean combination
of formulae from SL(∗, −∗) and SL(∗, reach+ ) is also PSpace-complete. So, we have provided proof
techniques to establish undecidability when ∗, −∗ and ls are present and to establish decidability
based on test formulae. This paves the way to investigate the decidability status of SL(−∗, ls) as
well as of the positive fragment of SL(∗, −⊛, ls) from [39, 40].

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                        1:41

  Acknowledgments. We would like to thank the anonymous reviewers for their numerous
suggestions and remarks that help us to improve the quality of the document.


REFERENCES
 [1] T. Antonopoulos, N. Gorogiannis, C. Haase, M. Kanovich, and J. Ouaknine. 2014. Foundations for Decision Problems
     in Separation Logic with General Inductive Predicates. In FoSSaCS’14 (Lecture Notes in Computer Science), Vol. 8412.
     Springer, 411–425.
 [2] J. Berdine, C. Calcagno, and P. O’Hearn. 2004. A decidable fragment of separation logic. In FSTTCS’04 (Lecture Notes in
     Computer Science), Vol. 3328. Springer, 97–109.
 [3] J. Berdine, C. Calcagno, and P. O’Hearn. 2005. Smallfoot: Modular Automatic Assertion Checking with Separation
     Logic. In FMCO’05 (Lecture Notes in Computer Science), Vol. 4111. Springer, 115–137.
 [4] M. Bozga, R. Iosif, and S. Perarnau. 2010. Quantitative Separation Logic and Programs with Lists. Journal of Automated
     Reasoning 45, 2 (2010), 131–156.
 [5] R. Brochenin, S. Demri, and E. Lozes. 2009. Reasoning about sequences of memory states. Annals of Pure and Applied
     Logic 161, 3 (2009), 305–323.
 [6] R. Brochenin, S. Demri, and E. Lozes. 2012. On the Almighty Wand. Information and Computation 211 (2012), 106–137.
 [7] J. Brotherston, C. Fuhs, N. Gorogiannis, and J. Navarro Perez. 2014. A Decision Procedure for Satisfiability in Separation
     Logic with Inductive Predicates. In CSL-LiCS’14.
 [8] J. Brotherston and J. Villard. 2014. Parametric completeness for separation theories. In POPL’14. ACM, 453–464.
 [9] C. Calcagno and D. Distefano. 2011. Infer: An Automatic Program Verifier for Memory Safety of C Programs. In NASA
     Formal Methods (Lecture Notes in Computer Science), Vol. 6617. Springer, 459–465.
[10] C. Calcagno, D. Distefano, P.W. O’Hearn, and H. Yang. 2011. Compositional Shape Analysis by Means of Bi-Abduction.
     J. ACM 58, 6 (2011), 26:1–26:66.
[11] C. Calcagno, Ph. Gardner, and M. Hague. 2005. From separation logic to first-order logic. In FoSSaCS’05 (Lecture Notes
     in Computer Science), Vol. 3441. Springer, 395–409.
[12] C. Calcagno, P. O’Hearn, and H. Yang. 2001. Computability and Complexity Results for a Spatial Assertion Language
     for Data Structures. In FSTTCS’01 (Lecture Notes in Computer Science), Vol. 2245. Springer, 108–119.
[13] B. Cook, C. Haase, J. Ouaknine, M. Parkinson, and J. Worrell. 2011. Tractable Reasoning in a Fragment of Separation
     Logic. In CONCUR’11 (Lecture Notes in Computer Science), Vol. 6901. Springer, 235–249.
[14] C. David, D. Kroening, and M. Lewis. 2015. Propositional Reasoning about Safety and Termination of Heap-Manipulating
     Programs. In ESOP’15 (Lecture Notes in Computer Science), Vol. 9032. Springer, 661–684.
[15] S. Demri and M. Deters. 2015. Logical Investigations on Separation Logics. (Aug. 2015). http://www.lsv.ens-cachan.fr/
     Publis/PAPERS/PDF/DD-esslli15.pdf Lecture Notes, European Summer School on Logic, Language and Information
     (ESSLLI’15).
[16] S. Demri and M. Deters. 2016. Expressive Completeness of Separation Logic With Two Variables and No Separating
     Conjunction. ACM Transations on Computational Logics 17, 2 (2016), 12.
[17] S. Demri, D. Galmiche, D. Larchey-Wendling, and D. Mery. 2017. Separation Logic with One Quantified Variable.
     Theory of Computing Systems 61 (2017), 371–461.
[18] S. Demri, E. Lozes, and A. Mansutti. 2018. The Effects of Adding Reachability Predicates in Propositional Separation
     Logic. In FoSSaCS’18 (Lecture Notes in Computer Science), Vol. 10803. Springer, 476–493.
[19] S. Demri, É. Lozes, and A. Mansutti. 2020. Internal Calculi for Separation Logics. In CSL (LIPIcs), Vol. 152. Schloss
     Dagstuhl - Leibniz-Zentrum für Informatik, 19:1–19:18.
[20] D. Distefano, P. O’Hearn, and H. Yang. 2006. A Local Shape Analysis Based on Separation Logic. In TACAS’06 (Lecture
     Notes in Computer Science), Vol. 3920. Springer, 287–302.
[21] M. Echenim, R. Iosif, and N. Peltier. 2020. The Bernays-Schönfinkel-Ramsey Class of Separation Logic with Uninter-
     preted Predicates. ACM Transations on Computational Logics 21, 3 (2020), 19:1–19:46.
[22] C. Haase, S. Ishtiaq, J. Ouaknine, and M. Parkinson. 2013. SeLoger: A Tool for Graph-Based Reasoning in Separation
     Logic. In CAV’13 (Lecture Notes in Computer Science), Vol. 8044. Springer, 790–795.
[23] Z. Hou, R. Goré, and A. Tiu. 2015. Automated Theorem Proving for Assertions in Separation Logic with All Connectives.
     In CADE’15 (Lecture Notes in Computer Science), Vol. 9195. Springer, 501–516.
[24] R. Iosif, A. Rogalewicz, and J. Simacek. 2013. The Tree Width of Separation Logic with Recursive Definitions. In
     CADE’13 (Lecture Notes in Computer Science), Vol. 7898. Springer, 21–38.
[25] S. Ishtiaq and P. O’Hearn. 2001. BI as an Assertion Language for Mutable Data Structures. In POPL’01. ACM, 14–26.
[26] J. Katelaan, Ch. Matheja, and F. Zuleger. 2019. Effective Entailment Checking for Separation Logic with Inductive
     Definitions. In TACAS’19 (Lecture Notes in Computer Science), Vol. 11428. Springer, 319–336.


                                       ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:42                                                     Stéphane Demri, Etienne Lozes, and Alessio Mansutti

[27] Q.L. Le, M. Tatsuta, J. Sun, and W.-N. Chin. 2017. A Decidable Fragment in Separation Logic with Inductive Predicates
     and Arithmetic. In CAV’17 (Lecture Notes in Computer Science), Vol. 10427. Springer, 495–517.
[28] E. Lozes. 2004. Expressivité des Logiques Spatiales. PhD thesis. ENS Lyon.
[29] E. Lozes. 2004. Separation Logic preserves the expressive power of classical logic. In SPACE’04.
[30] A. Mansutti. 2018. Extending propositional separation logic for robustness properties. In FSTTCS’18 (Leibniz Interna-
     tional Proceedings in Informatics). Leibniz-Zentrum für Informatik, 42:1–42:23.
[31] A. Mansutti. 2020. Reasoning with Separation Logics: Complexity, Expressive Power, Proof Systems. Ph.D. Dissertation.
     Université Paris-Saclay.
[32] P. Müller, M. Schwerhoff, and A.J. Summers. 2016. Viper: A Verification Infrastructure for Permission-Based Reasoning.
     In VMCAI’16 (Lecture Notes in Computer Science), Vol. 9583. Springer, 41–62.
[33] P.W. O’Hearn, J.C. Reynolds, and H. Yang. 2001. Local Reasoning about Programs that Alter Data Structures. In CSL’01
     (Lecture Notes in Computer Science), Vol. 2142. Springer, 1–19.
[34] R. Piskać, Th. Wies, and D. Zufferey. 2013. Automating Separation Logic using SMT. In CAV’13 (Lecture Notes in
     Computer Science), Vol. 8044. Springer, 773–789.
[35] S. Ranise and C. Zarba. 2006. A theory of singly-linked lists and its extensible decision procedure. In SEFM’06. IEEE,
     206–215.
[36] J.C. Reynolds. 2002. Separation logic: a logic for shared mutable data structures. In LiCS’02. IEEE, 55–74.
[37] W.J. Savitch. 1970. Relationships between nondeterministic and deterministic tape complexities. J. Comput. System Sci.
     4, 2 (1970), 177–192.
[38] M. Schwerhoff and A. Summers. 2015. Lightweight support for magic wands in an automatic verifier. In ECOOP’15.
     Leibniz-Zentrum für Informatik, LIPICS, 999–1023.
[39] A. Thakur. 2014. Symbolic Abstraction: Algorithms and Applications. Ph.D. Dissertation. University of Wisconsin-
     Madison.
[40] A. Thakur, J. Breck, and T. Reps. 2014. Satisfiability modulo abstraction for separation logic with linked lists. In SPIN’14.
     ACM, 58–67.
[41] H. Yang. 2001. Local Reasoning for Stateful Programs. Ph.D. Dissertation. University of Illinois, Urbana-Champaign.
[42] H. Yang, O. Lee, J. Berdine, C. Calcagno, B. Cook, D. Distefano, and P. O’Hearn. 2008. Scalable Shape Analysis for
     Systems Code. In CAV’08 (Lecture Notes in Computer Science), Vol. 5123. Springer, 385–398.




ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                  1:43

A     ELECTRONIC APPENDIX
In this appendix, we present the full proof of Lemma 4.8. The material about the proof included in
the body of the paper is a subset of the material below.

    Proof. Let 𝑞, 𝛼, 𝛼 1 , 𝛼 2 , (𝑠, ℎ), (𝑠 ′, ℎ ′), ℎ 1 and ℎ 2 be defined as in the statement. Let
     • SG𝑞 (𝑠, ℎ) = (V, E, Alloc, TEq, Inter, Rem) and
     • SG𝑞 (𝑠 ′, ℎ ′) = (V′, E′, Alloc′, TEq′, Inter′, Rem′)
be the support graphs of (𝑠, ℎ) and (𝑠 ′, ℎ ′) respectively, with respect to 𝑞. As (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), let
                                                                                                        𝑞

𝔣 : V → V′ be a map satisfying (A1)–(A5) from Lemma 4.7. Below, for the sake of conciseness, let
𝑘 ∈ {1, 2} and SG𝑞 (𝑠, ℎ𝑘 ) = (V𝑘 , E𝑘 , Alloc𝑘 , TEq𝑘 , Inter𝑘 , Rem𝑘 ) be the support graph of (𝑠, ℎ𝑘 ).
   The proof is rather long and can be summed up with the following steps.
    (1) First, we define a strategy to split ℎ ′ into ℎ 1′ and ℎ 2′ by closely following the way that ℎ is
        split into ℎ 1 and ℎ 2 . To do this, we look at the support graphs. For instance, suppose that
        Rem is split into two sets 𝑅1 ⊆ dom(ℎ 1 ) and 𝑅2 ⊆ dom(ℎ 2 ). By definition, it is quite easy to
        see that the sets 𝑅1 and 𝑅2 must be subsets of Rem1 and Rem2 , respectively. Then, following
        Lemma 4.7, to obtain (𝑠, ℎ𝑘 ) ≈𝛼𝑘 (𝑠 ′, ℎ𝑘′ ), we are required to split Rem′ into 𝑅1′ ⊆ dom(ℎ 1′ )
                                           𝑞

        and 𝑅2′ ⊆ dom(ℎ 2′ ) so that min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ )). Indeed, otherwise the
        equisatisfaction of the test formulae of the form sizeR𝑞 ≥ 𝛽 is not ensured (details on this
        are formalised later).
    (2) After defining ℎ 1′ and ℎ 2′ , we show that (𝑠, ℎ𝑘 ) ≈𝛼𝑘 (𝑠 ′, ℎ𝑘′ ). To do so, again, we follow
                                                                  𝑞

        Lemma 4.7 and we show that we can find suitable bijections from labelled locations of ℎ𝑘 to
        the ones of ℎ𝑘′ satisfying (A1)–(A5).
According to the summary above, let us first define explicitly ℎ 1′ and ℎ 2′ via an iterative process that
consists in adding locations to dom(ℎ 1′ ) or to dom(ℎ 2′ ). Whenever we enforce that ℓ ∈ dom(ℎ𝑘′ ),
                              def
implicitly we have ℎ𝑘′ (ℓ) = ℎ ′ (ℓ) as ℎ𝑘′ is intended to be a subheap of ℎ ′.
                                                  def
(CA) For all ℓ ∈ Alloc′, ℓ ∈ dom(ℎ𝑘′ ) ⇔ 𝔣−1 (ℓ) ∈ dom(ℎ𝑘 ). This step of the construction, as well
     as its usefulness, should be self-explanatory. For example, if (𝑠, ℎ𝑘 ) |= alloc(x𝑖 ) then, by
     relying on (A3), this step allows us to conclude that (𝑠 ′, ℎ𝑘′ ) |= alloc(x𝑖 ) (independently on
     how the definition of ℎ𝑘′ will be completed in the next steps of the construction).
(CR) The heaps ℎ 1′ and ℎ 2′ are further populated depending on Rem. Let 𝑅𝑘 = Rem ∩ dom(ℎ𝑘 ). By
     definition, we have 𝑅1 ⊎ 𝑅2 = Rem. Below, we partition Rem′ into two sets 𝑅1′ and 𝑅2′ so that
     by definition 𝑅𝑘′ ⊆ dom(ℎ𝑘′ ). The strategy for defining the partition is split into three cases:
                                                                                                         def
        (CR.C1) If card(𝑅1 ) < 𝛼 1 then 𝑅1′ is a set of card(𝑅1 ) locations from Rem′ and 𝑅2′ = Rem′ \𝑅1′ .
        (CR.C2) Otherwise, if card(𝑅2 ) < 𝛼 2 then 𝑅2′ is a set of card(𝑅2 ) locations of Rem′ and
              def
          𝑅1′ = Rem′ \ 𝑅2′ .
        (CR.C3) Otherwise we have card(𝑅1 ) ≥ 𝛼 1 and card(𝑅2 ) ≥ 𝛼 2 . Then, 𝑅1′ is a set of 𝛼 1
                                            def
          locations from Rem′ and 𝑅2′ = Rem′ \ 𝑅1′ .
        It is easy to show that the construction satisfies the following property (where 𝑘 ∈ {1, 2}):
                                    min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ ))                                 (CR.P1)
        The property (CR.P1) directly follows from the property (A5) satisfied by 𝔣. The proof (that
        can be applied also for the next step of the construction, see (CI.P2)), works as follows.
        First, suppose that the sets of remaining locations in the heap domain are small, i.e.
                           min(𝛼, card(Rem)) = min(𝛼, card(Rem′)) < 𝛼 1 + 𝛼 2 .

                                     ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:44                                                  Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       So, card(Rem) = card(Rem′) and therefore card(𝑅1 ) + card(𝑅2 ) = card(𝑅1′ ) + card(𝑅2′ ). By
       definition, card(𝑅1 ) = card(𝑅1′ ) and card(𝑅2 ) = card(𝑅2′ ) trivially hold for the cases (CR.C1)
       and (CR.C2), whereas the case (CR.C3) (card(𝑅1 ) ≥ 𝛼 1 and card(𝑅2 ) ≥ 𝛼 2 ) can never
       be applied since card(𝑅1 ) + card(𝑅2 ) < 𝛼 1 + 𝛼 2 . We conclude that min(𝛼𝑘 , card(𝑅𝑘 )) =
       min(𝛼𝑘 , card(𝑅𝑘′ )).
       Second, suppose instead

                              min(𝛼, card(Rem)) = min(𝛼, card(Rem′)) = 𝛼 1 + 𝛼 2 .

      If the first case (CR.C1) applies, i.e. card(𝑅1 ) < 𝛼 1 , then card(𝑅2 ) ≥ 𝛼 2 and by definition
      card(𝑅1′ ) = card(𝑅1 ). Then, card(𝑅2′ ) ≥ 𝛼 2 trivially follows from card(𝑅1′ ) + card(𝑅2′ ) ≥
      𝛼 1 + 𝛼 2 . Symmetrically, min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ )) holds when the second
      case (CR.C2) applies (card(𝑅2 ) < 𝛼 2 ). Lastly, suppose card(𝑅1 ) ≥ 𝛼 1 and card(𝑅2 ) ≥ 𝛼 2 .
      Then, the third case (CR.C3) applies and by definition card(𝑅1′ ) = 𝛼 1 . Again, we con-
      clude that min(𝛼𝑘 , card(𝑅𝑘 )) = min(𝛼𝑘 , card(𝑅𝑘′ )) since card(𝑅2′ ) ≥ 𝛼 2 trivially follows
      from card(𝑅1′ ) + card(𝑅2′ ) ≥ 𝛼 1 + 𝛼 2 .
(CI) Lastly, the heaps ℎ 1′ and ℎ 2′ are further populated with respect to the memory cells in Inter(ℓ, ℓ ′).
                                     def
       For all (ℓ, ℓ ′) ∈ E, let 𝐿𝑘 = Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ). We have 𝐿1 ⊎ 𝐿2 = Inter(ℓ, ℓ ′). Below, we
       partition Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) into 𝐿1′ and 𝐿2′ so that by definition 𝐿𝑘′ ⊆ dom(ℎ𝑘′ ):
       (CI.C1) If card(𝐿1 ) < 𝛼 1 then 𝐿1′ is a set of card(𝐿1 ) locations from Inter′ (𝔣(ℓ), 𝔣(ℓ ′)), whereas
             def
         𝐿2′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) \ 𝐿1′ .
       (CI.C2) Else, if card(𝐿2 ) < 𝛼 2 then 𝐿2′ is a set of card(𝐿2 ) locations from Inter′ (𝔣(ℓ), 𝔣(ℓ ′)),
                        def
         whereas 𝐿1′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) \ 𝐿2′ .
       (CI.C3) Otherwise, we have card(𝐿1 ) ≥ 𝛼 1 and card(𝐿2 ) ≥ 𝛼 2 . Then 𝐿1′ is a set of 𝛼 1 locations
                                               def
          from Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) and 𝐿2′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) \ 𝐿1′ .
       It is easy to show that the construction satisfies the following properties (where 𝑘 ∈ {1, 2}):

                                 if 𝐿𝑘′ = ∅ then Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ⊆ dom(ℎ 3−𝑘
                                                                               ′
                                                                                   )                 (CI.P1)

                                    min(𝛼𝑘 , card(𝐿𝑘 )) = min(𝛼𝑘 , card(𝐿𝑘′ ))                       (CI.P2)
       (Proof of (CI.P1)) The first property trivially holds from the cases (CI.C1) and (CI.C2) of
       the construction. Notice that given 𝑘 ∈ {1, 2}, 3 − 𝑘 corresponds to the index in {1, 2} that is
       different from 𝑘.
       (Proof of (CI.P2)) The second property directly follows from (A4) (which is satisfied by 𝔣)
       and is proved as done for (CR.P1).
   This ends the construction of ℎ 1′ and ℎ 2′ as any location in dom(ℎ ′) has been assigned to one
of the two heaps. Indeed, {Alloc′, Rem′ } ∪ {Inter′ (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E′ } is a partition of dom(ℎ ′).
As (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), the support graphs SG𝑞 (𝑠, ℎ) and SG𝑞 (𝑠 ′, ℎ ′) witness the existence of a map
            𝑞
           ′
𝔣 : V → V satisfying (A1)–(A5) and therefore there is an underlying isomorphism between these
structures satisfying quantitative properties up to the value 𝛼. The construction above can be
understood as a way to split ℎ ′ into ℎ 1′ and ℎ 2′ mimicking the splitting of ℎ into ℎ 1 and ℎ 2 . It remains
to show below that this is done in a way that guarantees that (𝑠, ℎ𝑘 ) ≈𝛼𝑘 (𝑠 ′, ℎ𝑘′ ) (𝑘 ∈ {1, 2}).
                                                                               𝑞
                                                                          ′  ′
   In the following, we denote the support graphs of (𝑠, ℎ𝑘 ) and (𝑠 , ℎ𝑘 ) respectively as
    • SG𝑞 (𝑠, ℎ𝑘 ) = (V𝑘 , E𝑘 , Alloc𝑘 , TEq𝑘 , Inter𝑘 , Rem𝑘 ) and,
    • SG𝑞 (𝑠 ′, ℎ𝑘′ ) = (V𝑘′ , E𝑘′ , Alloc𝑘′ , TEq𝑘′ , Inter𝑘′ , Rem𝑘′ ).
   First, let us formalise an essential property of the construction of ℎ 1′ and ℎ 2′ .

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                       1:45

(Paths) Let 𝑘 ∈ {1, 2} and let ℓ, ℓ ′ ∈ V be two labelled locations w.r.t. (𝑠, ℎ). ℎ𝑘 witnesses a non-
     empty path from ℓ to ℓ ′ if and only if ℎ𝑘′ witnesses a non-empty path from 𝔣(ℓ) to 𝔣(ℓ ′).

(Proof of (Paths)) The proof mainly relies on the properties (CI.P1) and (CI.P2) of the construction.
      Recall that 𝔣 : V → V′ is a bijection satisfying (A1)–(A5) w.r.t. (𝑠, ℎ) and (𝑠 ′, ℎ ′).
      (⇒) Let ℓ, ℓ ′ ∈ V be such that ℎ𝑘 witnesses a non-empty path from ℓ to ℓ ′. Since ℎ𝑘 ⊑ ℎ, then
      ℎ also witnesses a non-empty path from ℓ to ℓ ′. In particular, by Definition 4.4, this path
      corresponds to a path in the support graph SG𝑞 (𝑠, ℎ):
                        ℓ         E       ℓ1      E         ℓ2          ℓ𝑛−1     E         ℓ𝑛    E         ℓ′
                                                                 ...
                            def                 def
       Let us define ℓ0 = ℓ and ℓ𝑛+1 = ℓ ′. In particular, following the picture above, the support
       graph SG𝑞 (𝑠, ℎ) witnesses a path {(ℓ0, ℓ1 ), . . . , (ℓ𝑛 , ℓ𝑛+1 )} ⊆ E from ℓ0 to ℓ𝑛+1 . Since 𝔣 is a graph
       isomorphism from (V, E) to (V′, E′) (by (A1)), SG𝑞 (𝑠 ′, ℎ ′) witnesses a similar structure, as
       depicted below:
                ℓ=ℓ0          E           ℓ1     E          ℓ2          ℓ𝑛−1     E      ℓ𝑛      E          ℓ ′=ℓ𝑛+1
                                                                 ...

                    𝔣                 𝔣                 𝔣               𝔣              𝔣               𝔣

                                                                 ...
                    𝔣(ℓ)      E′      𝔣(ℓ1 )     E′    𝔣(ℓ2 )          𝔣(ℓ𝑛−1 ) E
                                                                                  ′
                                                                                      𝔣(ℓ𝑛 )    E′    𝔣(ℓ ′)
       Let us consider 𝑖 ∈ [0, 𝑛]. Since the path belongs to ℎ𝑘 , it must hold that ℓ𝑖 ∈ dom(ℎ𝑘 ) and
       Inter(ℓ𝑖 , ℓ𝑖+1 ) ⊆ dom(ℎ𝑘 ). We show that then 𝔣(ℓ𝑖 ) ∈ dom(ℎ𝑘′ ) and Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ⊆
       dom(ℎ𝑘′ ), which entails that ℎ𝑘′ witnesses a path from 𝔣(ℓ) to 𝔣(ℓ ′), concluding the proof.
       • From (ℓ𝑖 , ℓ𝑖+1 ) ∈ E, by Definition 4.4 we conclude that ℓ𝑖 ∈ V. Since ℓ𝑖 ∈ dom(ℎ), again by
         Definition 4.4, we have ℓ𝑖 ∈ Alloc and therefore by (A2), 𝔣(ℓ𝑖 ) ∈ Alloc′. By (CA) together
         with the fact that ℓ𝑖 ∈ dom(ℎ𝑘 ), we then conclude that 𝔣(ℓ𝑖 ) ∈ dom(ℎ𝑘′ ).
       • If Inter(ℓ𝑖 , ℓ𝑖+1 ) is empty then by (A4) Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) is also empty and the inclusion
         w.r.t. dom(ℎ𝑘′ ) trivially holds. Suppose now Inter(ℓ𝑖 , ℓ𝑖+1 ) is non-empty. From Inter(ℓ𝑖 , ℓ𝑖+1 ) ⊆
         dom(ℎ𝑘 ) and the fact that ℎ𝑘 and ℎ 3−𝑘 are disjoint we conclude that Inter(ℓ𝑖 , ℓ𝑖+1 ) ∩
         dom(ℎ 3−𝑘 ) = ∅. Hence, by (CI.P2) we conclude that Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩ dom(ℎ 3−𝑘   ′ ) = ∅

         (notice that in (CI.P2), 𝐿3−𝑘 corresponds to Inter(ℓ𝑖 , ℓ𝑖+1 ) ∩ dom(ℎ 3−𝑘 ) whereas 𝐿3−𝑘     ′   cor-
                                ′                     ′                      ′                       ′
         responds to Inter (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩ dom(ℎ 3−𝑘 )). Since Inter (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩ dom(ℎ 3−𝑘 ) = ∅,
         by (CI.P1) we then conclude that Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ⊆ dom(ℎ𝑘′ ).
       (⇐) The right-to-left direction is analogous (thanks to the fact that 𝔣−1 is a graph isomorphism
       from (V′, E′) to (V, E)).

   Here is the last step of the proof. Given 𝑘 ∈ {1, 2}, let 𝔣𝑘 be the restriction of 𝔣 to V𝑘 and V𝑘′ . We
prove that 𝔣𝑘 satisfies (A1)–(A5) w.r.t. the memory states (𝑠, ℎ𝑘 ) and (𝑠 ′, ℎ𝑘′ ). Thanks to Lemma 4.7,
this implies (𝑠, ℎ 1 ) ≈𝛼 1 (𝑠 ′, ℎ 1′ ) and (𝑠, ℎ 2 ) ≈𝛼 2 (𝑠 ′, ℎ 2′ ), ending the proof. For convenience, we prove
                        𝑞                               𝑞

the five properties in the following order: (A3), (A2), (A1), (A4) and (A5) (in the body of the paper
only the proof of (A3) is provided).

𝔣𝑘 satisfies (A3): We prove that for every ℓ ∈ V, the set of terms corresponding to ℓ in (𝑠, ℎ𝑘 ) is
      equivalent to the set of terms corresponding to 𝔣(ℓ) in (𝑠 ′, ℎ𝑘′ ). Formally:

                                          ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:46                                                               Stéphane Demri, Etienne Lozes, and Alessio Mansutti

             for every ℓ ∈ V,
                (a) ℓ ∈ V𝑘 iff 𝔣(ℓ) ∈ V𝑘′ ;
               (b) if ℓ ∈ V𝑘 , TEq𝑘 (ℓ) = TEq𝑘′ (𝔣(ℓ)).
       Notice that (a) implies that 𝔣𝑘 (which we recall being the restriction of 𝔣 to V𝑘 and V𝑘′ ) is
       well-defined and it is a bijection from the labelled locations of (𝑠, ℎ𝑘 ) (i.e. V𝑘 ) to the labelled
       locations of (𝑠 ′, ℎ𝑘′ ) (i.e. V𝑘′ ). This is due to the fact that 𝔣 is a bijection from V to V′ and
       by Lemma 4.3, we have V𝑘 ⊆ V and V𝑘′ ⊆ V′. Again by V𝑘 ⊆ V (Lemma 4.3), (b) is then
       equivalent to (A3).
       We prove (a) and (b) together, by showing that for every ℓ ∈ V, the set of terms corresponding
       to ℓ in (𝑠, ℎ𝑘 ) is equivalent to the set of terms corresponding to 𝔣(ℓ) in (𝑠 ′, ℎ𝑘′ ). We first show
       the result for program variables, and then for meet-points.
       (Program variables) Let ℓ ∈ V and 𝑖 ∈ [1, 𝑞]. It holds that x𝑖 ∈ TEq𝑘 (ℓ) if and only if 𝑠 (x𝑖 ) = ℓ,
       or equivalently x𝑖 ∈ TEq(ℓ) which, by (A3) in Lemma 4.7, holds whenever x𝑖 ∈ TEq′ (𝔣(ℓ)).
       The latter is equivalent to 𝑠 ′ (x𝑖 ) = 𝔣(ℓ), or equivalently x𝑖 ∈ TEq𝑘′ (𝔣(ℓ)).
       (Meet-points) In order to conclude the proof, we show that for all 𝑖, 𝑗 ∈ [1, 𝑞] and ℓ ∈ V,
                           𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 (ℓ) if and only if 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣(ℓ)).
       If [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is undefined, then so is [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ (by def.) and by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′), so
                               𝑞                                                                𝑞                                                      𝑞
                               𝑞                            𝑞                                            𝑞
       are [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ . By Lemma 4.3, if [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is undefined, then
                                   𝑞                      𝑞                        𝑞                             𝑞
       so are [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ , [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ , [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ . Otherwise,
                                          𝑘                            𝑘                              𝑘                                            𝑘
       if [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = ℓ then by definition [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = ℓ ′ for some ℓ ′ ∈ V and moreover
                               𝑞                                                               𝑞

       [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣(ℓ) and [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = 𝔣(ℓ ′) by (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′). Let z𝑖 (resp. z 𝑗 )
                          𝑞                                    𝑞                          𝑞

       be the program variable in {x1, . . . , x𝑞 } such that 𝑠 (z𝑖 ) is the first location corresponding
                                                                                    𝑞                          𝑞
       to a program variable that is reachable from [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ (resp. [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ ), itself
       included. The characterisation of such a program variable z𝑖 can be captured by the formula
       firstvar(𝑚𝑞 (x𝑖 , x 𝑗 ), z𝑖 ) defined as the following Boolean combination of test formulae:
                                         ÜÓ                                             Ó
              𝑚𝑞 (x𝑖 , x 𝑗 ) = z𝑖 ∨            𝛿 ∈ [1,𝑛−1] sees𝑞 (𝑣 𝛿 , 𝑣 𝛿+1 ) ≥ 1 ∧ 𝑚<𝑛 x𝑘 ≠ 𝑣𝑚
                                                                                                                          𝑘 ∈ [1,𝑞 ]
                                      𝑣1 ,...,𝑣𝑛 ∈Terms𝑞 ,𝑛>1
                                   pairwise distinct 𝑣1 ,...,𝑣𝑛−1 ,
                                       𝑣1 =𝑚𝑞 (x𝑖 ,x 𝑗 ),𝑣𝑛 =z𝑖

       Indeed, this formula is satisfied only by memory states where there is a (possibly empty) path
       from the location corresponding to 𝑚𝑞 (x𝑖 , x 𝑗 ) to the location ℓ corresponding to z𝑖 so that
       each labelled location in the path, apart from ℓ, does not correspond to the interpretation of
       such program variables. Now, we recall the taxonomy of meet-points, where the rightmost
       case from Figure 5 is split into three cases, highlighting additional cases depending on z𝑖 and
       z𝑗 .
                 x𝑖       x𝑗              x𝑖         x𝑗           x𝑖                                       x𝑗                          x𝑖                        x𝑗


                                                                                                                                                   z𝑖
                                                                                                                                                           +
          𝑚𝑞 (x𝑖 ,x 𝑗 )            𝑚𝑞 (x𝑖 ,x 𝑗 )                                    x𝑗    x𝑖
                                                          𝑚𝑞 (x𝑖 ,x 𝑗 )                                   𝑚𝑞 (x 𝑗 ,x𝑖 )        𝑚𝑞 (x𝑖 ,x 𝑗 )                   𝑚𝑞 (x 𝑗 ,x𝑖 )
          𝑚𝑞 (x 𝑗 ,x𝑖 )            𝑚𝑞 (x 𝑗 ,x𝑖 )
                                                                  +            +               +            +                                  +
                                                                                                                                                   z𝑗
                 z𝑖 = z 𝑗                  +               z𝑖 = z 𝑗                                          z𝑖 = z 𝑗
           z𝑖 not inside a loop

                                              z𝑖 = z 𝑗                    𝑚𝑞 (x 𝑗 ,x𝑖 )   𝑚𝑞 (x𝑖 ,x 𝑗 )


               (i)            (ii)             (iii)             (iv)                     (v)
       Distinct structures satisfy different test formulae, though they all satisfy the formula

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                         1:47

                                  firstvar(𝑚𝑞 (x𝑖 , x 𝑗 ), z𝑖 ) ∧ firstvar(𝑚𝑞 (x 𝑗 , x𝑖 ), z 𝑗 ).
     For instance, (i) is the only form not satisfying reach+ (z𝑖 , z𝑖 ) (recall that this form can be
     expressed as a Boolean combination of test formulae, as shown in Lemma 4.5), whereas (ii) can
     be distinguished as the only form satisfying both reach+ (z𝑖 , z𝑖 ) and 𝑚𝑞 (x𝑖 , x 𝑗 ) = 𝑚𝑞 (x 𝑗 , x𝑖 ).
     Moreover, the last structure is the only one satisfying z𝑖 ≠ z 𝑗 whereas (iii) and (iv) can
     be distinguished with a formula, similar to firstvar(𝑚𝑞 (x𝑖 , x 𝑗 ), z𝑖 ), stating that from the
     location corresponding to z𝑖 , it is possible to reach the location corresponding to 𝑚𝑞 (x𝑖 , x 𝑗 )
     without reaching the location corresponding to 𝑚𝑞 (x 𝑗 , x𝑖 ):
                  ÜÓ                                           Ó
                         𝛿 ∈ [1,𝑛−1] sees𝑞 (𝑣 𝛿 , 𝑣 𝛿+1 ) ≥ 1 ∧ 1<𝑚<𝑛 𝑚𝑞 (x 𝑗 , x𝑖 ) ≠ 𝑣𝑚 .
            𝑣1 ,...,𝑣𝑛 ∈Terms𝑞 , 𝑛>1
         pairwise distinct 𝑣1 ,...,𝑣𝑛−1 ,
             𝑣1 =z𝑖 ,𝑣𝑛 =𝑚𝑞 (x𝑖 ,x 𝑗 )

     Differently from (iii), the structure (iv) does not satisfy this formula. Since (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′),
                                                                                                                   𝑞

     the heaps ℎ and ℎ ′ agree on the structure of every meet-point. The proof that for all 𝑖, 𝑗 ∈ [1, 𝑞]
     and ℓ ∈ V, 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 (ℓ) iff 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣(ℓ)), essentially relies on (Paths). To
     show the result we need to proceed by cases, according to the taxonomy.
     Case: ℎ witnesses (i), (ii) or (iv). Since the heaps ℎ and ℎ ′ agree on the structure of every
       meet-point, ℎ ′ also witnesses the same form among (i), (ii) and (iv) as ℎ. Regarding ℎ𝑘 , one
       of the following holds:
       • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are both preserved in ℎ𝑘 .
         Then ℎ𝑘 witnesses (i) (ii) or (iv). By (Paths) the same holds for ℎ𝑘′ . In every case ((i), (ii)
                                                            𝑞                     𝑞                         𝑞
         and (iv)), we conclude that [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ =
                                                                        𝑘                                                 𝑘
                              𝑞                              𝑞
          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ). Then,
                                                                                  𝑞
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )).
                                                                                      𝑞


      • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) or the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are not preserved in ℎ𝑘 .
        Then, again by (Paths), the same holds for ℎ𝑘′ with respect to (𝑠 ′, ℎ ′). By definition of
                                                 𝑞                      𝑞
        meet-points, both [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ are therefore not defined.
                                                   𝑘                         𝑘
     Case: ℎ witnesses (iii). If instead ℎ and ℎ ′ witness (iii) then one of the following holds.
                                                                                              𝑞
      • ℎ𝑘 also witnesses (iii), meaning that the path from 𝑠 (x𝑖 ) to [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ and the path
        from 𝑠 (x 𝑗 ) to [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ are both preserved in ℎ𝑘 . Then by (Paths) the heap ℎ𝑘′
                                            𝑞
                                                          𝑞                        𝑞                         𝑞
        also witnesses (iii). We have [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ =
                                                                        𝑘                                                 𝑘
                              𝑞                              𝑞
          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ). We conclude that
                                                                                  𝑞
                                      𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )
                                                                                      𝑘

                                      𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )).
                                                                                    𝑞
                                                                                       𝑘


       • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z𝑖 ) are preserved in ℎ𝑘 , whereas
                                                     𝑞
         the path from 𝑠 (z𝑖 ) to [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is not preserved in ℎ𝑘 (i.e. at least one of its
         locations is assigned to the other heap ℎ 3−𝑘 ). Then ℎ𝑘 witnesses (i) and by definition of
         meet-points, it holds that
                                                 𝑞                       𝑞                       𝑞
                            [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ
                                                     𝑘                       𝑘


                                            ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:48                                                        Stéphane Demri, Etienne Lozes, and Alessio Mansutti

            By (Paths), ℎ𝑘′ also witnesses (i). Then,
                              𝑞                            𝑞                              𝑞                           𝑞
            [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ ).
                                   𝑘                           𝑘

            Then, we conclude that
                                                                                      𝑞
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )).
                                                                                          𝑞


        • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) or the path from 𝑠 (x 𝑗 ) to 𝑠 (z𝑖 ) are not preserved in ℎ𝑘 . Then,
          by (Paths), the same holds for ℎ𝑘′ with respect to (𝑠 ′, ℎ ′). By definition of meet-points,
                                   𝑞                            𝑞
          both [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ are not defined.
                                     𝑘                             𝑘
       Case: ℎ witnesses (v). Lastly, suppose that ℎ and ℎ ′ witness (v). One of the following holds.
        • The path from 𝑠 (x𝑖 ) to 𝑠 (z𝑖 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z𝑖 ) are both preserved in
                                                                                                                        𝑞
          ℎ𝑘 . Then, depending on whether or not the path from 𝑠 (z𝑖 ) to [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ is also
          preserved, ℎ𝑘′ witnesses (i) or (v). From (Paths), the same holds for ℎ𝑘′ (where ℎ𝑘′ wit-
                                                                                                                            𝑞
          nesses (i) iff ℎ𝑘 witnesses (i)). In both cases ((i) and (v)), it holds that [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ =
                                                                                                                              𝑘
                             𝑞                          𝑞                           𝑞                              𝑞
          [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ ). Then,
                                                                   𝑘
                                                                                      𝑞
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ )).
                                                                                          𝑞


          • The path from 𝑠 (x𝑖 ) to 𝑠 (z 𝑗 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are preserved in ℎ𝑘 , whereas
                                                         𝑞
            the path from 𝑠 (z 𝑗 ) to [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ is not preserved in ℎ𝑘 . Then ℎ𝑘 witnesses (i) and
            by definition of meet-points, it holds that
                                               𝑞                           𝑞                          𝑞
                            [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ .
                                                   𝑘                           𝑘

            By (Paths), the heap ℎ𝑘′ also witnesses (i). Then,
                               𝑞                           𝑞                              𝑞                           𝑞
            [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠 ′,ℎ′ = 𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )
                                   𝑘                           𝑘

            Then, we conclude that
                                                                                      𝑞
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 ( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )
                                       𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣( [[𝑚𝑞 (x 𝑗 , x𝑖 )]] 𝑠,ℎ )).
                                                                                          𝑞


         • The path from 𝑠 (x𝑖 ) to 𝑠 (z 𝑗 ) and the path from 𝑠 (x 𝑗 ) to 𝑠 (z 𝑗 ) are not preserved in ℎ𝑘 . Then,
           by (Paths), the same holds for ℎ𝑘′ with respect to (𝑠 ′, ℎ ′). By definition of meet-points,
                                   𝑞                          𝑞
           both [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠,ℎ and [[𝑚𝑞 (x𝑖 , x 𝑗 )]] 𝑠 ′,ℎ′ are undefined.
                                      𝑘                            𝑘
      We conclude that for every ℓ ∈ V, 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘 (ℓ) if and only if 𝑚𝑞 (x𝑖 , x 𝑗 ) ∈ TEq𝑘′ (𝔣(ℓ)).
𝔣𝑘 satisfies (A2): We prove that 𝔣𝑘 is such that
                                    for every ℓ ∈ V𝑘 , ℓ ∈ Alloc𝑘 iff 𝔣𝑘 (ℓ) ∈ Alloc𝑘′ .
      From (a) in the proof that 𝔣𝑘 satisfies (A3), we know that for every ℓ ∈ V𝑘 , 𝔣𝑘 (ℓ) = 𝔣(ℓ) ∈ V𝑘′ .
      (⇒) For the left-to-right direction, let ℓ ∈ V𝑘 such that ℓ ∈ Alloc𝑘 . By definition we have
      ℓ ∈ dom(ℎ𝑘 ) and therefore ℓ ∈ dom(ℎ) (from ℎ𝑘 ⊑ ℎ). Since V𝑘 ⊆ V (Lemma 4.3) we have
      ℓ ∈ V and hence ℓ ∈ Alloc. From (𝑠, ℎ) ≈𝛼 (𝑠 ′, ℎ ′) we obtain 𝔣(ℓ) ∈ Alloc′. Hence, from the
                                                        𝑞

      construction of ℎ𝑘′ done in (CA) we have 𝔣(ℓ) ∈ dom(ℎ𝑘′ ). Moreover, since 𝔣𝑘 (ℓ) = 𝔣(ℓ) ∈ V𝑘′ ,
      we conclude 𝔣𝑘 (ℓ) ∈ Alloc𝑘′ .
      (⇐) The right-to-left direction follows by using a similar argument.

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                       1:49

𝔣𝑘 satisfies (A1): We prove that 𝔣𝑘 is a graph isomorphism between (V𝑘 , E𝑘 ) and (V𝑘′ , E𝑘′ ). From
      (a) in the proof that 𝔣𝑘 satisfies (A3) we already know that 𝔣𝑘 is a bijection from V𝑘 to V𝑘′ .
      Hence, we only need to show that for all ℓ, ℓ ′ ∈ V𝑘 , (ℓ, ℓ ′) ∈ E𝑘 ⇐⇒ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)) ∈ E𝑘′ .
      (⇒) By definition of SG𝑞 (𝑠, ℎ𝑘 ), we have that (ℓ, ℓ ′) ∈ E𝑘 if and only if ℓ, ℓ ′ ∈ V𝑘 and
      ℎ𝑘 witnesses a non-empty (minimal) path from ℓ to ℓ ′ such that none of the intermediate
      locations of this path are in V𝑘 . From (a) in the proof that 𝔣𝑘 satisfies (A3) we have
                                 ℓ ∈ V𝑘 iff 𝔣𝑘 (ℓ) ∈ V𝑘′ ;          ℓ ′ ∈ V𝑘 iff 𝔣𝑘 (ℓ ′) ∈ V𝑘′ .
      As moreover V𝑘 ⊆ V and V𝑘′ ⊆ V′ (by Lemma 4.3), by (Paths) it holds that ℎ𝑘 witnesses a
      non-empty path from ℓ to ℓ ′ if and only if ℎ𝑘′ witnesses a non-empty path from 𝔣𝑘 (ℓ) to 𝔣𝑘 (ℓ ′).
      Therefore, to conclude the proof, it remains to show that there is a non-empty path from
      𝔣𝑘 (ℓ) to 𝔣𝑘 (ℓ ′) in ℎ𝑘′ such that no intermediate locations of this path are in V𝑘′ . If this property
      is satisfied, then it is satisfied by the minimal non-empty path from 𝔣𝑘 (ℓ) to 𝔣𝑘 (ℓ ′), which
      we suppose being of length 𝐿 ≥ 1. Let us denote this path with 𝜎 (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)). If 𝐿 = 1
      then the property is trivially satisfied (as there are no intermediate locations between 𝔣𝑘 (ℓ)
      and 𝔣𝑘 (ℓ ′)). Otherwise, ad absurdum, suppose there exists ℓ ′′ ∈ V𝑘′ , different from 𝔣𝑘 (ℓ) and
      𝔣𝑘 (ℓ ′), such that for some 𝐿1, 𝐿2 ≥ 1 such that 𝐿 = 𝐿1 + 𝐿2 we have ℎ𝑘′ 𝐿1 (𝔣𝑘 (ℓ)) = ℓ ′′ and
      ℎ𝑘′ 𝐿2 (ℓ ′′) = 𝔣𝑘 (ℓ ′). Then, we show that 𝔣𝑘−1 (ℓ ′′) (which by (A3) is in V𝑘 ) is an intermediate
      location on the minimal non-empty path from ℓ to ℓ ′, in ℎ𝑘 , in contradiction with (ℓ, ℓ ′) ∈ E𝑘 .
      To do so, we start by considering the set 𝐴 of locations of V′ that belongs to the minimal
      path from 𝔣𝑘 (ℓ) to 𝔣𝑘 (ℓ ′) (excluding these two locations). Formally,
                                        there are 𝐿1′ , 𝐿2′ ≥ 1, such that 𝐿 = 𝐿1′ + 𝐿2′ ,
                                (                                                             )
                            def
                         𝐴 = ℓ˜ ∈ V′                ′                        ′
                                               ℎ𝑘′ 𝐿1 (𝔣𝑘 (ℓ)) = ℓ˜ and ℎ𝑘′ 𝐿2 ( ℓ)
                                                                                 ˜ = 𝔣𝑘 (ℓ ′)

      For simplicity, let 𝐴 = {ℓ1, . . . , ℓ𝑛 }. Since by Lemma 4.3 we have ℓ ′′ ∈ V′, we conclude ℓ ′′ ∈ 𝐴.
      Without loss of generality, we assume ℓ𝑖 and ℓ𝑖+1 (𝑖 ∈ [1, 𝑛 − 1]) to be two consecutive labelled
      locations in the minimal path from 𝔣𝑘 (ℓ) to 𝔣𝑘 (ℓ ′), i.e. none of the intermediate locations in
      the minimal path from ℓ𝑖 to ℓ𝑖+1 is labelled. Then, by minimality of 𝜎 (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)) and from
      the definition of support graph, SG𝑞 (𝑠 ′, ℎ ′) witnesses the following linear structure, where
      the arrow between two locations ℓ𝑖 and ℓ𝑖+1 labelled by E′ means that E′ (ℓ𝑖 , ℓ𝑖+1 ).
                  𝔣(ℓ)     E′      ℓ1       E′     ℓ2               ℓ𝑛−1     E′      ℓ𝑛       E′           𝔣(ℓ ′)
                                                            ...
      Since 𝔣 is a graph isomorphism from (V, E) to (V′, E′) (by (A1)), SG𝑞 (𝑠, ℎ) witnesses a similar
      structure, as depicted below:
                   𝔣(ℓ)     E′         ℓ1   E′         ℓ2            ℓ𝑛−1     E′         ℓ𝑛    E′              𝔣(ℓ ′)
                                                             ...

                 𝔣−1             𝔣−1             𝔣−1               𝔣−1             𝔣−1              𝔣−1

                                                             ...
                       ℓ    E 𝔣−1 (ℓ1 ) E 𝔣−1 (ℓ2 )                𝔣−1 (ℓ𝑛−1 ) E 𝔣−1 (ℓ𝑛 ) E              ℓ′
      Since 𝔣 is a bijection, for all distinct 𝑖, 𝑗 ∈ [1, 𝑛], we have 𝔣−1 (ℓ𝑖 ) ≠ 𝔣−1 (ℓ 𝑗 ). Thus, every 𝔣−1 (ℓ𝑖 )
      (𝑖 ∈ [1, 𝑛]) is in the minimal path from ℓ to ℓ ′ in ℎ, and therefore from (ℓ, ℓ ′) ∈ E𝑘 we obtain
      that {𝔣−1 (ℓ1 ), . . . , 𝔣−1 (ℓ𝑛 )} ⊆ Inter𝑘 (ℓ, ℓ ′). This leads to a contradiction. Indeed, from ℓ ′′ ∈ 𝐴
      we conclude 𝔣−1 (ℓ ′′) ∈ Inter𝑘 (ℓ, ℓ ′). Then, as 𝔣𝑘−1 (ℓ ′′) ∈ V𝑘 (by (A3)), we conclude that ℎ𝑘
      witnesses a labelled intermediate location in the minimal non-empty path from ℓ to ℓ ′ in

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:50                                                   Stéphane Demri, Etienne Lozes, and Alessio Mansutti

      contradiction with (ℓ, ℓ ′) ∈ E𝑘 . Hence, in ℎ𝑘′ there are no labelled locations in the minimal
      path from 𝔣𝑘 (ℓ) to 𝔣𝑘 (ℓ ′), allowing us to conclude that (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)) ∈ E′.
      (⇐) The right-to-left direction is analogous (thanks to the fact that 𝔣 and 𝔣𝑘 are bijections).
      It remains to check the satisfaction of the conditions (A4) and (A5) that involve arithmetical
      constraints.
𝔣𝑘 satisfies (A4): We show that for every (ℓ, ℓ ′) ∈ E𝑘 we have

                   min(𝛼𝑘 , card(Inter𝑘 (ℓ, ℓ ′))) = min(𝛼𝑘 , card(Inter𝑘′ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)))).

       First, we show the following intermediate result.
       (𝔣𝑘 -A4.I) Let (ℓ, ℓ ′) ∈ E𝑘 . There is a (possibly empty) set {ℓ1, . . . , ℓ𝑛 } ⊆ V such that
                                 def             def
          (a) By defining ℓ0 = ℓ and ℓ𝑛+1 = ℓ ′, we have that for every 𝑖 ∈ [0, 𝑛], (ℓ𝑖 , ℓ𝑖+1 ) ∈ E;
          (b) {ℓ1, . . . , ℓ𝑛 } = Inter𝑘 (ℓ, ℓ ′) ∩ V and {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} = Inter𝑘′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ V′;
          (c) Inter𝑘 (ℓ, ℓ ′) = {ℓ1, . . . , ℓ𝑛 } ∪ 𝑖 ∈ [0,𝑛] Inter(ℓ𝑖 , ℓ𝑖+1 );
                                                    Ð

          (d) Inter𝑘′ (𝔣(ℓ), 𝔣(ℓ ′)) = {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} ∪ 𝑖 ∈ [0,𝑛] Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )).
                                                                  Ð

       (Proof of (𝔣𝑘 -A4.I)) The proof follows rather closely the arguments used for the proof of (A1).
         Suppose (ℓ, ℓ ′) ∈ E𝑘 . Since 𝔣𝑘 satisfies (A1) we have (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)) ∈ E𝑘′ . By Lemma 4.3,
         V𝑘 ⊆ V and V𝑘′ ⊆ V′. Informally, this means that a subheap cannot contain new labelled
         locations w.r.t. the original heap. It can however be the case that the set Inter𝑘 (ℓ, ℓ ′) contains
         locations that are labelled w.r.t. (𝑠, ℎ) (i.e. locations in V) and that are not labelled for (𝑠, ℎ𝑘 )
         (by definition of Inter𝑘 (ℓ, ℓ ′)). More precisely, these locations correspond to meet-points
         of ℎ. Hence, let us consider the set {ℓ1, . . . , ℓ𝑛 } = Inter𝑘 (ℓ, ℓ ′) ∩ V (as required by (b)). Let
                           def        def
         us define ℓ0 = ℓ, ℓ𝑛+1 = ℓ ′. Since Inter𝑘 (ℓ, ℓ ′) describes the set of locations of the minimal
                                ′
         path from ℓ to ℓ in ℎ𝑘 , and moreover ℎ𝑘 ⊑ ℎ, there is an ordering on the locations ℓ1, . . . , ℓ𝑛 ,
         w.l.o.g. say ℓ1 < · · · < ℓ𝑛 such that for every 𝑖 ∈ [0, 𝑛] (ℓ𝑖 , ℓ𝑖+1 ) ∈ E (property (a) of (𝔣𝑘 -A4.I)).
         So, {ℓ1, . . . , ℓ𝑛 } is a set of locations in Inter𝑘 (ℓ, ℓ ′) that correspond to meet-points of (𝑠, ℎ).
         Now, as done in the proof of (A1), 𝔣 is a graph isomorphism from (V, E) to (V′, E′) and
         therefore these two structures witness the following correspondence
               ℓ = ℓ0             E       ℓ1    E     ℓ2             ℓ𝑛−1     E     ℓ𝑛    E       ℓ ′ = ℓ𝑛+1
                                                             ...

                      𝔣                𝔣               𝔣              𝔣               𝔣                𝔣

                                                               ...
                                    ′             ′                               ′                ′
                         𝔣(ℓ) E 𝔣(ℓ1 ) E 𝔣(ℓ2 )                       𝔣(ℓ𝑛−1 ) E 𝔣(ℓ𝑛 ) E 𝔣(ℓ ′)
          (★): where in particular for every 𝑖 ∈ [0, 𝑛], (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∈ E′. Notice that, since 𝔣 is
          a bijection, for all two distinct 𝑖, 𝑗 ∈ [1, 𝑛], we have 𝔣(ℓ𝑖 ) ≠ 𝔣(ℓ 𝑗 ). Most importantly, as
          ℓ, ℓ ′ ∉ Inter𝑘 (ℓ, ℓ ′) (this holds by definition of this set), we conclude ℓ, ℓ ′ ∉ {ℓ1, . . . , ℓ𝑛 }
          and therefore 𝔣(ℓ), 𝔣(ℓ ′) ∉ {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )}. Thanks to this property, {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} is
          the set of labelled locations in the minimal path from 𝔣(ℓ) to 𝔣(ℓ ′) in ℎ ′. Equivalently,
          {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} = Inter𝑘′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ V′ (property (b) of (𝔣𝑘 -A4.I)). Lastly, by (a) and
          (b), from the fact that heaps are functional and ℎ𝑘 witnesses a path from ℓ to ℓ ′, it fol-
          lows that for every 𝑖 ∈ [0, 𝑛] Inter(ℓ𝑖 , ℓ𝑖+1 ) ⊆ Inter𝑘 (ℓ, ℓ ′). Similarly, for every 𝑖 ∈ [0, 𝑛]
          Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ⊆ Inter𝑘′ (𝔣(ℓ), 𝔣(ℓ ′)). Therefore, we conclude that
          • Inter𝑘 (ℓ, ℓ ′) = {ℓ1, . . . , ℓ𝑛 } ∪ 𝑖 ∈ [0,𝑛] Inter(ℓ𝑖 , ℓ𝑖+1 ),
                                                 Ð
          • Inter𝑘′ (𝔣(ℓ), 𝔣(ℓ ′)) = {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} ∪ 𝑖 ∈ [0,𝑛] Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )),
                                                               Ð


ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                    1:51

       which ends the proof of (𝔣𝑘 -A4.I). Notice that the two properties (c) and (d) (now proved)
       are well depicted by the figure above, as it shows the structure of the minimal path from ℓ
       to ℓ ′ in ℎ (and ℎ𝑘 ), and the structure of the minimal path from 𝔣(ℓ) to 𝔣(ℓ ′) in ℎ ′ (and ℎ𝑘′ ).
     We are now ready to show that 𝔣𝑘 satisfies (A4). Let (ℓ, ℓ ′) ∈ E𝑘 and let {ℓ1, . . . , ℓ𝑛 } ⊆ V𝑘
                                                                    def       def
     satisfying the four properties in (𝔣𝑘 -A4.I). Let us define ℓ0 = ℓ, ℓ𝑛+1 = ℓ ′. As already stated in
     the proof of (𝔣𝑘 -A4.I), 𝔣 is a bijection and therefore for all two distinct 𝑖, 𝑗 ∈ [1, 𝑛], we have
     𝔣(ℓ𝑖 ) ≠ 𝔣(ℓ 𝑗 ). Hence,
                             card({ℓ1, . . . , ℓ𝑛 }) = card({𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )}) = 𝑛.
     Moreover, by recalling (from Definition 4.4) that
     • {Alloc, Rem} ∪ {Inter(ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E} is a partition of dom(ℎ);
     • {Alloc′, Rem′ } ∪ {Inter′ (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E′ } is a partition of dom(ℎ ′),
     we conclude that for every 𝑖 ∈ [0, 𝑛],
     • {ℓ1, . . . , ℓ𝑛 } ∩ Inter(ℓ𝑖 , ℓ𝑖+1 ) = ∅ and for all 𝑗 ∈ [0, 𝑛] \ {𝑖}, Inter(ℓ𝑖 , ℓ𝑖+1 ) ∩ Inter(ℓ 𝑗 , ℓ 𝑗+1 ) = ∅;
     • {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} ∩ Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) = ∅ and for all 𝑗 ∈ [0, 𝑛] \ {𝑖}, Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )) ∩
       Inter′ (𝔣(ℓ 𝑗 ), 𝔣(ℓ 𝑗+1 )) = ∅.
     Thus, the cardinalities of Inter𝑘 (ℓ, ℓ ′) and Inter𝑘′ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)) can be written respectively as
                                                               ∑︁
                                card(Inter𝑘 (ℓ, ℓ ′)) = 𝑛+        card(Inter(ℓ𝑖 , ℓ𝑖+1 )),
                                                           𝑖 ∈ [0,𝑛]
                                                             ∑︁
                    card(Inter𝑘′ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′))) = 𝑛+       card(Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 ))).
                                                        𝑖 ∈ [0,𝑛]

     Now, 𝔣 satisfies (A4) w.r.t. the memory states (𝑠, ℎ) and (𝑠 ′, ℎ ′), and therefore for every
     𝑖 ∈ [0, 𝑛]
                  min(𝛼, card(Inter(ℓ𝑖 , ℓ𝑖+1 ))) = min(𝛼, card(Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )))).                      (𝔣-A4)
     We distinguish two cases.
     • If there exists 𝑖 ∈ [0, 𝑛] such that card(Inter(ℓ𝑖 , ℓ𝑖+1 )) ≥ 𝛼, then by (𝔣-A4) we have
       card(Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 ))) ≥ 𝛼. Since 𝛼𝑘 ≤ 𝛼, we conclude
                    card(Inter𝑘 (ℓ, ℓ ′)) ≥ 𝛼𝑘 ;          card(Inter𝑘′ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′))) ≥ 𝛼𝑘 .
     • Otherwise (for all 𝑖 ∈ [0, 𝑛], card(Inter(ℓ𝑖 , ℓ𝑖+1 )) < 𝛼) from (𝔣-A4) we conclude that for all
       𝑖 ∈ [0, 𝑛],
                       card(Inter(ℓ𝑖 , ℓ𝑖+1 )) = card(Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 ))),
        which allows us to conclude that card(Inter𝑘 (ℓ, ℓ ′)) = card(Inter𝑘′ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′))).
      In both cases we have shown that
                 min(𝛼𝑘 , card(Inter𝑘 (ℓ, ℓ ′))) = min(𝛼𝑘 , card(Inter𝑘′ (𝔣𝑘 (ℓ), 𝔣𝑘 (ℓ ′)))),
      concluding the proof of (A4).
𝔣𝑘 satisfies (A5): Lastly, we show that
                              min(𝛼𝑘 , card(Rem𝑘 )) = min(𝛼𝑘 , card(Rem𝑘′ )).
     We take advantage of the following five intermediate results.
     (I) For every ℓ ∈ V ∩ dom(ℎ𝑘 ), ℓ ∈ Rem𝑘 if and only if 𝔣(ℓ) ∈ Rem𝑘′ .
     (Proof of (I)) (⇒) Suppose ℓ ∈ V. By Definition 4.4, it holds that ℓ ∈ Rem𝑘 if and only if
        (i) ℓ ∉ V𝑘 and ℓ ∈ dom(ℎ𝑘 );
        (ii) there is no (ℓ ′, ℓ ′′) ∈ E𝑘 such that ℓ ∈ Inter𝑘 (ℓ ′, ℓ ′′).

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:52                                                       Stéphane Demri, Etienne Lozes, and Alessio Mansutti

         From (a) in the proof that 𝔣𝑘 satisfies (A3), we have 𝔣(ℓ) = 𝔣𝑘 (ℓ) ∉ V𝑘′ . By ℓ ∈ dom(ℎ𝑘 ) and
         ℓ ∈ Rem𝑘 , from the construction step (CA) we conclude 𝔣(ℓ) ∈ dom(ℎ𝑘′ ).
         Besides, it cannot be that there is (ℓ1, ℓ2 ) ∈ E𝑘′ such that 𝔣(ℓ) ∈ Inter𝑘′ (ℓ1, ℓ2 ). Indeed, if that
         was the case, we can apply the proof ad absurdum showed in the left-to-right direction of
         the proof that 𝔣𝑘 satisfies (A1), and derive that ℓ ∈ Inter𝑘′ (𝔣𝑘−1 (ℓ1 ), 𝔣𝑘−1 (ℓ2 )), in contradiction
         with (ii). Hence, as we proved that (i) and (ii) hold for 𝔣(ℓ), by Definition 4.4, we conclude
         that 𝔣(ℓ) ∈ Rem𝑘′ .
         (⇐) The right-to-left direction follows by using similar arguments.
       (II) card(Rem𝑘 ∩ V) = card(Rem𝑘′ ∩ V′) and card(Rem𝑘 ∩ Alloc) = card(Rem𝑘′ ∩ Alloc′).
       (Proof of (II)) The first equality follows directly from (I) and the fact that 𝔣 is a bijection.
         Then, since Alloc ⊆ V, Alloc′ ⊆ V′ (by definition) and ℓ ∈ Alloc ⇔ 𝔣(ℓ) ∈ Alloc′ (from
         the property (A2) of 𝔣), the second equality also holds.
       (III) For all (ℓ, ℓ ′) ∈ E,
              Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) ⊆ Rem𝑘 if and only if Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ dom(ℎ𝑘′ ) ⊆ Rem𝑘′ .
       (Proof of (III)) Recall that (ℓ, ℓ ′) ∈ E implies (𝔣(ℓ), 𝔣(ℓ ′)) ∈ E′. From (CI.P2), we notice that
                   Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) = ∅ if and only if Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ dom(ℎ𝑘′ ) = ∅,
         as by definition 𝐿𝑘 = Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) and 𝐿𝑘′ = Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ dom(ℎ𝑘′ ) in the
         case (CI) of the construction (where we consider Inter(ℓ, ℓ ′)). Therefore, (III) trivially holds
         when Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) is empty. In the following, we assume Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 )
         and Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ dom(ℎ𝑘′ ) to be non-empty.
          (⇒) Let (ℓ, ℓ ′) ∈ E and suppose Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) ⊆ Rem𝑘 . Let us consider a location
         ℓ˜ ∈ Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ dom(ℎ𝑘′ ). We show that ℓ˜ ∈ Rem𝑘′ . As shown in the proof of (I),
         ℓ˜ ∈ Rem𝑘′ holds if and only if
         (i) ℓ˜ ∉ V𝑘′ and ℓ˜ ∈ dom(ℎ𝑘′ );
         (ii) there is no ( ℓ˜1, ℓ˜2 ) ∈ E𝑘′ such that ℓ˜ ∈ Inter𝑘′ ( ℓ˜1, ℓ˜2 ).
         The proof of (i) is straightforward: by ℓ˜ ∈ Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) ∩ dom(ℎ𝑘′ ), we directly con-
         clude that ℓ˜ ∈ dom(ℎ𝑘′ ) (first condition in (i)) and ℓ˜ ∈ Inter′ (𝔣(ℓ), 𝔣(ℓ ′)). From the latter
         membership and by Definition 4.4, we conclude ℓ˜ ∉ V′. Lastly, by Lemma 4.3, V𝑘′ ⊆ V′ and
         therefore ℓ˜ ∉ V𝑘′ (second condition in (i)). Let us now prove (ii). Ad absurdum, suppose that
         there is ( ℓ˜1, ℓ˜2 ) ∈ E𝑘′ such that ℓ˜ ∈ Inter𝑘′ ( ℓ˜1, ℓ˜2 ). Then, as we have shown that 𝔣𝑘 satisfies
         (A1), (𝔣𝑘−1 ( ℓ˜1 ), 𝔣𝑘−1 ( ℓ˜𝑛 )) ∈ E𝑘 . We apply (𝔣𝑘 -A4.I): there is a set {ℓ1, . . . , ℓ𝑛 } ⊆ V such that
                                   def                       def
          (a) by defining ℓ0 = 𝔣𝑘−1 ( ℓ˜1 ) and ℓ𝑛+1 = 𝔣𝑘−1 ( ℓ˜2 ), for every 𝑖 ∈ [0, 𝑛], (ℓ𝑖 , ℓ𝑖+1 ) ∈ E;
          (b) {ℓ1, . . . , ℓ𝑛 } = Inter𝑘 (𝔣𝑘−1 ( ℓ˜1 ), 𝔣𝑘−1 ( ℓ˜2 )) ∩ V and {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} = Inter𝑘′ ( ℓ˜1, ℓ˜2 ) ∩ V′;
          (c) Inter𝑘 (𝔣𝑘−1 ( ℓ˜1 ), 𝔣𝑘−1 ( ℓ˜2 )) = {ℓ1, . . . , ℓ𝑛 } ∪ 𝑖 ∈ [0,𝑛] Inter(ℓ𝑖 , ℓ𝑖+1 );
                                                                        Ð

          (d) Inter′ ( ℓ˜1, ℓ˜2 ) = {𝔣(ℓ1 ), . . . , 𝔣(ℓ𝑛 )} ∪ 𝑖 ∈ [0,𝑛] Inter′ (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )).
                                                                   Ð
                     𝑘
          Recalling that {Alloc′, Rem′ } ∪ {Inter′ (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E′ } is a partition of dom(ℎ ′) (by
          Definition 4.4), from (d) together with ℓ˜ ∈ Inter′ (𝔣(ℓ), 𝔣(ℓ ′)) and ℓ˜ ∈ Inter𝑘′ ( ℓ˜1, ℓ˜2 ), we con-
          clude that there is 𝑖 ∈ [0, 𝑛] such that (𝔣(ℓ), 𝔣(ℓ ′)) = (𝔣(ℓ𝑖 ), 𝔣(ℓ𝑖+1 )). From (c), we conclude
          that Inter(ℓ, ℓ ′) ⊆ Inter𝑘 (𝔣𝑘−1 ( ℓ˜1 ), 𝔣𝑘−1 ( ℓ˜2 )). Notice that, by Definition 4.4, this inclusion also
          entails Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) = Inter(ℓ, ℓ ′), i.e. every element in Inter(ℓ, ℓ ′) is a memory
          cell of ℎ𝑘 . Hence, Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) ⊆ Inter𝑘 (𝔣𝑘−1 ( ℓ˜1 ), 𝔣𝑘−1 ( ℓ˜2 )), in contradiction with
          Inter(ℓ, ℓ ′) ∩dom(ℎ𝑘 ) ⊆ Rem𝑘 . Indeed, we assumed Inter(ℓ, ℓ ′) ∩dom(ℎ𝑘 ) to be non-empty,
          and by Definition 4.4, Rem𝑘 ∩ Inter𝑘 (𝔣𝑘−1 ( ℓ˜1 ), 𝔣𝑘−1 ( ℓ˜2 )) = ∅. Therefore, it cannot be that there
          is ( ℓ˜1, ℓ˜2 ) ∈ E𝑘′ such that ℓ˜ ∈ Inter𝑘′ ( ℓ˜1, ℓ˜2 ). As (i) and (ii) hold, we conclude that ℓ˜ ∈ Rem𝑘′ .


ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                                 1:53

       (⇐) The right-to-left direction follows by using similar arguments.
     (IV) For every (ℓ, ℓ ′) ∈ E, Rem𝑘 ∩Inter(ℓ, ℓ ′) = ∅ or Inter(ℓ, ℓ ′) ∩dom(ℎ𝑘 ) ⊆ Rem𝑘 . Similarly,
       for every (ℓ, ℓ ′) ∈ E′, Rem𝑘′ ∩ Inter′ (ℓ, ℓ ′) = ∅ or Inter′ (ℓ, ℓ ′) ∩ dom(ℎ𝑘′ ) ⊆ Rem𝑘′ .
     (Proof of (IV)) Let us prove the first statement (the second one is proven analogously). By
       Definition 4.4, we have
       (a) {Alloc, Rem} ∪ {Inter(ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E} is a partition of dom(ℎ);
       (b) {Alloc𝑘 , Rem𝑘 } ∪ {Inter𝑘 (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E𝑘 } is a partition of dom(ℎ𝑘 ).
       Let (ℓ, ℓ ′) ∈ E. Ad absurdum, suppose that Rem𝑘 ∩ Inter(ℓ, ℓ ′) ≠ ∅ and there is ℓ˜ ∈
       (Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 )) \ Rem𝑘 . Since ℓ˜ ∈ Inter(ℓ, ℓ ′), by Definition 4.4, ℓ˜ is not a labelled
       location w.r.t. (𝑠, ℎ), i.e. ℓ˜ ∉ V. Moreover, from ℓ˜ ∈ dom(ℎ𝑘 ) and ℓ˜ ∉ Rem𝑘 , by (b) we
       conclude that ℓ˜ ∈ Alloc𝑘 or there is (ℓ1′, ℓ2′) ∈ E𝑘 such that ℓ˜ ∈ Inter𝑘 (ℓ1′, ℓ2′).
       • If ℓ˜ ∈ Alloc𝑘 , then ℓ˜ ∈ V𝑘 (by Definition 4.4). Recall that, by Lemma 4.3, V𝑘 ⊆ V.
         Therefore, we conclude ℓ˜ ∈ V (contradiction).
       • Otherwise, there is (ℓ1′, ℓ2′) ∈ E𝑘 such that ℓ˜ ∈ Inter𝑘 (ℓ1′, ℓ2′). By (𝔣𝑘 -A4.I), there is a set
         {ℓ1, . . . , ℓ𝑛 } ⊆ V such that
                              def                def
          (c) by defining ℓ0 = ℓ1′ and ℓ𝑛+1 = ℓ2′, we have that for every 𝑖 ∈ [0, 𝑛], (ℓ𝑖 , ℓ𝑖+1 ) ∈ E;
         (d) {ℓ1, . . . , ℓ𝑛 } = Inter𝑘 (ℓ1′, ℓ2′) ∩ V;
         (e) Inter𝑘 (ℓ1′, ℓ2′) = {ℓ1, . . . , ℓ𝑛 } ∪ 𝑖 ∈ [0,𝑛] Inter(ℓ𝑖 , ℓ𝑖+1 ).
                                                     Ð

         Since ℓ˜ ∉ V, from (e) we conclude that there is 𝑖 ∈ [0, 𝑛] such that ℓ˜ ∈ Inter(ℓ𝑖 , ℓ𝑖+1 ).
         Then, by (a) and ℓ˜ ∈ Inter(ℓ, ℓ ′), it must be that (ℓ𝑖 , ℓ𝑖+1 ) = (ℓ, ℓ ′). Hence, from (e),
         Inter(ℓ, ℓ ′) ⊆ Inter𝑘 (ℓ1′, ℓ2′). By (b) Rem𝑘 ∩ Inter𝑘 (ℓ1′, ℓ2′) = ∅ and therefore we conclude
         that Rem𝑘 ∩ Inter(ℓ, ℓ ′) = ∅, in contradiction with the hypothesis Rem𝑘 ∩ Inter(ℓ, ℓ ′) ≠ ∅.
       As in both cases we reached a contradiction, it must be that Rem𝑘 ∩ Inter(ℓ, ℓ ′) = ∅ or
       Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) ⊆ Rem𝑘 , concluding the proof.
     (V) It holds that Rem ∩ dom(ℎ𝑘 ) ⊆ Rem𝑘 and Rem′ ∩ dom(ℎ𝑘′ ) ⊆ Rem𝑘′ .
     (Proof of (V)) The proof is rather immediate. Let us prove that Rem ∩ dom(ℎ𝑘 ) ⊆ Rem𝑘 (the
       proof of Rem′ ∩ dom(ℎ𝑘′ ) ⊆ Rem𝑘′ is analogous). By Definition 4.4, we have
       (a) {Alloc, Rem} ∪ {Inter(ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E} is a partition of dom(ℎ);
       (b) {Alloc𝑘 , Rem𝑘 } ∪ {Inter𝑘 (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E𝑘 } is a partition of dom(ℎ𝑘 ).
       Suppose ℓ ∈ Rem ∩ dom(ℎ𝑘 ). Ad absurdum, suppose ℓ ∉ Rem𝑘 . Then, as ℓ ∈ dom(ℎ𝑘 ), from
       (b) it holds that ℓ ∈ Alloc𝑘 or there is (ℓ1, ℓ2 ) ∈ E𝑘 such that ℓ ∈ Inter𝑘 (ℓ1, ℓ2 ).
       • If ℓ ∈ Alloc𝑘 then ℓ ∈ V𝑘 (by Definition 4.4). By Lemma 4.3, V𝑘 ⊆ V and therefore ℓ ∈ V.
         Together with ℎ𝑘 ⊑ ℎ (hence dom(ℎ𝑘 ) ⊆ dom(ℎ)), the fact that ℓ ∈ V implies ℓ ∈ Alloc
         (again by Definition 4.4). From (a) we then obtain ℓ ∉ Rem, a contradiction.
       • Otherwise, let (ℓ1, ℓ2 ) ∈ E𝑘 such that ℓ ∈ Inter𝑘 (ℓ1, ℓ2 ). Therefore, by Definition 4.4 there
         are 𝐿1, 𝐿2 ≥ 1 such that ℎ𝑘𝐿1 (ℓ1 ) = ℓ and ℎ𝑘𝐿2 (ℓ) = ℓ2 . Since ℎ𝑘 ⊑ ℎ, we conclude that there
         are 𝐿1, 𝐿2 ≥ 1 such that ℎ𝐿1 (ℓ1 ) = ℓ and ℎ𝐿2 (ℓ) = ℓ2 . Now, notice that (ℓ1, ℓ2 ) ∈ E𝑘 implies
         ℓ1, ℓ2 ∈ V𝑘 (by Definition 4.4) and therefore ℓ1, ℓ2 ∈ V (since by Lemma 4.3 V𝑘 ⊆ V). We
         conclude that ℓ is an intermediate location in the path of ℎ from the labelled location ℓ1 to
         the labelled location ℓ2 . Hence, either ℓ ∈ Alloc or, by Definition 4.4, there is ( ℓ˜1, ℓ˜2 ) ∈ E
         such that ℓ ∈ Inter( ℓ˜1, ℓ˜2 ). In both cases, by (a) we have ℓ ∉ Rem, a contradiction.
       In both cases we conclude that ℓ ∉ Rem𝑘 cannot hold, ending the proof of (V).
     By taking advantage of (I)–(V), we are now ready to show that 𝔣𝑘 satisfies (A5), i.e.
                           min(𝛼𝑘 , card(Rem𝑘 )) = min(𝛼𝑘 , card(Rem𝑘′ )).
     First of all, we recall that by Definition 4.4 we have
     (a) {Alloc, Rem} ∪ {Inter(ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E} is a partition of dom(ℎ);

                                    ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
1:54                                                        Stéphane Demri, Etienne Lozes, and Alessio Mansutti

       (b) {Alloc′, Rem′ } ∪ {Inter′ (ℓ, ℓ ′) | (ℓ, ℓ ′) ∈ E′ } is a partition of dom(ℎ ′).
       Since Rem𝑘 ⊆ dom(ℎ𝑘 ) ⊆ dom(ℎ) and Rem𝑘′ ⊆ dom(ℎ𝑘′ ) ⊆ dom(ℎ ′), we can use (a) and (b)
       to decompose Rem𝑘 and Rem𝑘′ as follows:
       • Rem𝑘 = (Rem𝑘 ∩ Alloc) ∪ (Rem𝑘 ∩ Rem) ∪ (ℓ,ℓ ′ ) ∈E Rem𝑘 ∩ Inter(ℓ, ℓ ′) ,
                                                              Ð                                 

       • Rem𝑘′ = (Rem𝑘′ ∩ Alloc′) ∪ (Rem𝑘′ ∩ Rem′) ∪ (ℓ,ℓ ′ ) ∈E′ Ð         Rem𝑘′ ∩ Inter′ (ℓ, ℓ ′) ,
                                                                Ð                                  
       where all unions are performed on disjoint sets. By (IV), (ℓ,ℓ ′ ) ∈E (Rem𝑘 ∩ Inter(ℓ, ℓ ′)) and
       Ð                  ′          ′    ′
         (ℓ,ℓ ′ ) ∈E′ (Rem𝑘 ∩ Inter (ℓ, ℓ )) are respectively equal to
                       Ø                                                   Ø
                          Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 )                             Inter′ (ℓ, ℓ ′) ∩ dom(ℎ𝑘′ )
                                                                                                          
                     (ℓ,ℓ ′ ) ∈E                                                         (ℓ,ℓ ′ ) ∈E′
        Inter(ℓ,ℓ ′ )∩dom(ℎ𝑘 ) ⊆Rem𝑘                                       Inter′ (ℓ,ℓ ′ )∩dom(ℎ𝑘′ ) ⊆Rem𝑘′

       Since Rem𝑘 ⊆ dom(ℎ𝑘 ) and Rem𝑘′ ⊆ dom(ℎ𝑘′ ), by (V) we have Rem𝑘 ∩Rem = Rem∩dom(ℎ𝑘 )
       and Rem𝑘′ ∩ Rem′ = Rem′ ∩ dom(ℎ𝑘′ ). Hence, the previous equalities can be rewritten as
                                                         Ø
                                                             Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 )
                                                                                      
           Rem𝑘 = (Rem𝑘 ∩ Alloc) ∪ (Rem ∩ dom(ℎ𝑘 )) ∪
                                                                                (ℓ,ℓ ′ ) ∈E
                                                                   Inter(ℓ,ℓ ′ )∩dom(ℎ𝑘 ) ⊆Rem𝑘
                                                                                  Ø
            Rem𝑘′ = (Rem𝑘′ ∩ Alloc′) ∪ (Rem′ ∩ dom(ℎ𝑘′ )) ∪                              Inter′ (ℓ, ℓ ′) ∩ dom(ℎ𝑘′ ) .
                                                                                                                    
                                                                                   (ℓ,ℓ ′ ) ∈E′
                                                                     Inter′ (ℓ,ℓ ′ )∩dom(ℎ𝑘′ ) ⊆Rem𝑘′

       Since all unions are performed on disjoint sets (by (a) and (b)), we conclude that card(Rem𝑘 )
       and card(Rem𝑘′ ) satisfy the following equalities:
                                                                      ∑︁
       card(Rem𝑘 ) = card(Rem𝑘 ∩ Alloc) + card(Rem ∩ dom(ℎ𝑘 )) + card(Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ))
                                                                                             (ℓ,ℓ ′ ) ∈E
                                                                                Inter(ℓ,ℓ ′ )∩dom(ℎ𝑘 ) ⊆Rem𝑘
                                                                    ∑︁
       card(Rem𝑘′ ) = card(Rem𝑘′ ∩ Alloc′) + card(Rem′ ∩ dom(ℎ𝑘 )) + card(Inter′ (ℓ, ℓ ′)∩dom(ℎ𝑘′ ))
                                                                                               (ℓ,ℓ ′ ) ∈E′
                                                                                 Inter′ (ℓ,ℓ ′ )∩dom(ℎ𝑘′ ) ⊆Rem𝑘′

       Now, we are able to compare the values min(𝛼𝑘 , card(Rem𝑘 )) and min(𝛼𝑘 , card(Rem𝑘′ )). By
       using the two equalities above and recalling that min(𝐴, 𝐵 + 𝐶) = min(𝐴, 𝐵 + min(𝐴, 𝐶)), the
       following set of equalities holds for min(𝛼𝑘 , card(Rem𝑘 )):
       min(𝛼𝑘 , card(Rem𝑘 )) = min(𝛼𝑘 , card(Rem𝑘 ∩ Alloc) + 𝑅)
                                 𝑅 = min(𝛼𝑘 , card(Rem ∩ dom(ℎ𝑘 )) + 𝐼 )
                                              ∑︁
                                 𝐼 = min(𝛼𝑘 ,    𝐼 ℓ,ℓ ′ )
                                                     (ℓ,ℓ ′ ) ∈E
                                        Inter(ℓ,ℓ ′ )∩dom(ℎ𝑘 ) ⊆Rem𝑘
                               𝐼 ℓ,ℓ ′ = min(𝛼𝑘 , card(Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 )))                       where (ℓ, ℓ ′) ∈ E.
       The same can be done for min(𝛼𝑘 , card(Rem𝑘′ )):
       min(𝛼𝑘 , card(Rem𝑘′ )) = min(𝛼𝑘 , card(Rem𝑘′ ∩ Alloc′) + 𝑅 ′)
                               𝑅 ′ = min(𝛼𝑘 , card(Rem′ ∩ dom(ℎ𝑘′ )) + 𝐼 ′)
                                              ∑︁
                               𝐼 ′ = min(𝛼𝑘 ,      ′
                                                 𝐼 ℓ,ℓ ′)

                                                     (ℓ,ℓ ′ ) ∈E′
                                       Inter′ (ℓ,ℓ ′ )∩dom(ℎ𝑘′ ) ⊆Rem𝑘′
                                ′                          ′     ′         ′
                              𝐼 ℓ,ℓ ′ = min(𝛼𝑘 , card(Inter (ℓ, ℓ ) ∩ dom(ℎ𝑘 )))                        where (ℓ, ℓ ′) ∈ E′ .

ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
The Effects of Adding Reachability Predicates in Quantifier-Free Separation Logic                               1:55

      By (CI.P2), for every (ℓ, ℓ ′) ∈ E we have 𝐼 ℓ,ℓ ′ = 𝐼 𝔣′(ℓ),𝔣 (ℓ ′ ) . From (III) together with the fact
      that 𝔣 witnesses a graph isomorphism between (𝑠, ℎ) and (𝑠 ′, ℎ ′) we conclude that
                       {(ℓ, ℓ ′) ∈ E′ | Inter′ (ℓ, ℓ ′) ∩ dom(ℎ𝑘′ ) ⊆ Rem𝑘′ }
                    = {(𝔣(ℓ), 𝔣(ℓ ′)) | (ℓ, ℓ ′) ∈ E, Inter(ℓ, ℓ ′) ∩ dom(ℎ𝑘 ) ⊆ Rem𝑘 },
      which allows us to conclude that 𝐼 = 𝐼 ′. Furthermore, by (CR.P1), it follows also that 𝑅 = 𝑅 ′.
      Lastly, by (II) we conclude:
                            min(𝛼𝑘 , card(Rem𝑘 )) = min(𝛼𝑘 , card(Rem𝑘′ )).
   This concludes the proof: for the support graphs of ℎ𝑘 and ℎ𝑘′ , 𝔣 restricted to the domain V𝑘 and
the codomain V𝑘′ satisfies all conditions of Lemma 4.7 with respect to 𝛼𝑘 . Therefore, it holds that
(𝑠, ℎ 1 ) ≈𝛼 1 (𝑠 ′, ℎ 1′ ) and (𝑠, ℎ 2 ) ≈𝛼 2 (𝑠 ′, ℎ 2′ ).
           𝑞                               𝑞
                                                                                                    □

Received September 2020; accepted January 2021




                                  ACM Trans. Comput. Logic, Vol. 1, No. 1, Article 1. Publication date: January 2021.
