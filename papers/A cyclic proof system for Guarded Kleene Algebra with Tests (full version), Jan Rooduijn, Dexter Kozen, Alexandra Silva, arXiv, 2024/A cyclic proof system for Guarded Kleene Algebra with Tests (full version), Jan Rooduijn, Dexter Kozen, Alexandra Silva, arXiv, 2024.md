                                                  A cyclic proof system for Guarded Kleene
                                                      Algebra with Tests (full version)⋆

                                                         Jan Rooduijn1 , Dexter Kozen2 , and Alexandra Silva2
arXiv:2405.07505v1 [cs.LO] 13 May 2024




                                             1
                                                 Institute of Logic, Language and Computation, University of Amsterdam, The
                                                                      Netherlands janrooduijn@gmail.com
                                                                     2
                                                                       Cornell University, Ithaca, NY, USA



                                                   Abstract. Guarded Kleene Algebra with Tests (GKAT for short) is an
                                                   efficient fragment of Kleene Algebra with Tests, suitable for reasoning
                                                   about simple imperative while-programs. Following earlier work by Das
                                                   and Pous on Kleene Algebra, we study GKAT from a proof-theoretical per-
                                                   spective. The deterministic nature of GKAT allows for a non-well-founded
                                                   sequent system whose set of regular proofs is complete with respect to
                                                   the guarded language model. This is unlike the situation with Kleene
                                                   Algebra, where hypersequents are required. Moreover, the decision pro-
                                                   cedure induced by proof search runs in NLOGSPACE, whereas that of
                                                   Kleene Algebra is in PSPACE.

                                                   Keywords: Kleene Algebra · Guarded Kleene Algebra with Tests ·
                                                   Cyclic proofs


                                         1       Introduction
                                         Guarded Kleene Algebra with Test (GKAT) is the fragment of Kleene Algebra
                                         with Tests (KAT) comprised of the deterministic while programs. Those are the
                                         programs built up from sequential composition (e · f ), conditional branching
                                         (if-b-then-e-else-f ) and loops (while b do e). For an introduction to KAT
                                         we refer the reader to [10]. The ﬁrst papers focusing on the fragment of KAT that
                                         is nowadays called GKAT are Kozen’s [11] and Kozen & Tseng’s [12], where it is
                                         used to study the relative power of several programming constructs.
                                             As GKAT is a fragment of KAT, it directly inherits a rich theory. It admits a lan-
                                         guage semantics in the form of guarded strings and for every expression there is
                                         a corresponding KAT-automaton. Already in [12] it was argued that GKAT expres-
                                         sions are more closely related to so-called strictly deterministic automata, where
                                         every state transition executes a primitive program. Smolka et al. signiﬁcantly
                                         advanced the theory of GKAT in [22], by studying various additional semantics,
                                         identifying the precise class of strictly deterministic automata corresponding
                                         to GKAT-expressions (proving a Kleene theorem), giving a nearly linear decision
                                         procedure of the equivalence of GKAT-expressions, and studying its equational
                                         ⋆
                                             The research of Jan Rooduijn has been made possible by a grant from the Dutch
                                             Research Council NWO, project number 617.001.857.
2       J. Rooduijn et al.

axiomatisation. Since then GKAT has received considerable further attention, e.g.
in [20,17,24,21].
    One of the most challenging and intriguing aspects of GKAT is its proof theory.
The standard equational axiomatisation of KAT from [10] does not simply restrict
to GKAT, since a derivation of an expression that lies within the GKAT-fragment
might very well contain expressions that lie outside of it. Moreover, the axioma-
tisation of KAT contains a least ﬁxed point rule that relies on the equational
deﬁnability of inclusion, which does not seem to be available in GKAT.
    In [22], this problem is circumvented by introducing a custom equational
axiomatisation for GKAT that uses a unique ﬁxed point rule. While a notable
result, this solution is still not entirely satisfactory. First, completeness is only
proven under the inclusion of a variant of the unique ﬁxed point rule that op-
erates on entire systems of equations (this problem was recently addressed for
the so-called skip-free fragment of GKAT in [21]). Moreover, even the ordinary,
single-equation, unique ﬁxed point rule contains a non-algebraic side-condition,
analogous to the empty word property in Salomaa’s axiomatisation of Kleene
Algebra [18]. Because of this, a proper deﬁnition of ‘a GKAT’ is still lacking.
    In recent years the proof theory of logic with ﬁxed point operators (such
as while-b-do-e) has seen increasing interest in non-well-founded proofs. In
such proofs, branches need not to be closed by axioms, but may alternatively
be inﬁnitely deep. To preserve soundness, a progress condition is often imposed
on each inﬁnite branch, facilitating a soundness proof by inﬁnite descent. In
some cases non-well-founded proofs can be represented by ﬁnite trees with back-
edges, which are then called cyclic proofs. See e.g. [5,13,4,2,8] for a variety
of such approaches. Often, the non-well-founded proof theory of some logic is
closely related to its corresponding automata theory. Taking the proof-theoretical
perspective, however, can be advantageous because it is more ﬁne-grained and
provides a natural setting for establishing results such as interpolation [14,3],
cut elimination [19,1], and completeness by proof transformation [23,6].
    In [7], Das & Pous study the non-well-founded proof theory of Kleene Al-
gebra, a close relative of GKAT (for background on Kleene Algebra we refer the
reader to [9]). They show that a natural non-well-founded sequent system for
Kleene Algebra is not complete when restricting to the subset of cyclic proofs.
To remedy this, they introduce a hypersequent calculus, whose cyclic proofs are
complete. They give a proof-search procedure for this calculus and show that it
runs in PSPACE. Since deciding Kleene Algebra expressions is PSPACE-complete,
their proof-search procedure induces an optimal decision procedure for this prob-
lem. In a follow-up paper together with Doumane, left-handed completeness of
Kleene Algebra is proven by translating cyclic proofs in the hypersequent calcu-
lus to well-founded proofs in left-handed Kleene Algebra [6].
    The goal of the present paper is to study the non-well-founded proof theory
of GKAT. This is interesting in its own right, for instance because, as we will
see, it has some striking diﬀerences with Kleene Algebra. Moreover, we hope it
opens up new avenues for exploring the completeness of algebraic proof systems
for GKAT, through the translation of our cyclic proofs.
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)       3

Outline Our paper is structured as follows.

 – In Section 2 we introduce preliminary material: the syntax of GKAT and its
   language semantics.
 – Section 3 introduces our non-well-founded proof system SGKAT for GKAT.
 – In Section 4 we show that (possibly inﬁnitary) proofs in SGKAT are sound.
   That is, the interpretation of each derivable sequent - a GKAT-inequality - is
   true in the language model (which means that a certain inclusion of lan-
   guages holds).
 – In Section 5 we show that proofs are finite-state: each proof contains only
   ﬁnitely many distinct sequents. More precisely, by employing a more ﬁne-
   grained analysis than in [7], we give a quadratic bound on the number of
   distinct sequents occurring in a proof, in terms of the size of its endsequent.
   It follows that the subset of cyclic proofs proves exactly the same sequents
   as the set of all non-well-founded proofs.
 – Section 6 deals with completeness and complexity. We ﬁrst use a proof-search
   procedure to show that SGKAT is complete: every sequent whose interpreta-
   tion is valid in the language model, can be derived. We then show that this
   proof-search procedure runs in coNLOGSPACE. This gives an NLOGSPACE
   upper bound on the complexity of the language inclusion problem for GKAT-
   expressions.


Our contributions Our paper closely follows the treatment of Kleene Algebra
in [7]. Nevertheless, we make the following original contributions:

 – Structure of sequents: we devise a form of sequents bespoke to GKAT, by la-
   belling the sequents by sets of atoms. This is similar to how the appropriate
   automata for GKAT are not simply KAT-automata. In contrast to Kleene Alge-
   bra, it turns out that we do not need to extend our sequents to hypersequents
   in order to obtain completeness for the fragment of cyclic proofs.
 – Soundness argument: our modest contribution here is the notion of priority of
   rules and the fact that our rules are all invertible when they have priority. The
   soundness argument for ﬁnite proofs is, of course, slightly diﬀerent, because
   our rules are diﬀerent. (The step from the soundness of ﬁnite proofs, towards
   the soundness of inﬁnite proofs, is completely analogous to that of [7].)
 – Regularity: this concerns showing that every proof contains only ﬁnitely
   many distinct sequents. As in [7], our argument views each expression in
   a proof as a subexpression of an expression in the proof’s root. A modest
   contribution is that our argument is made more formal by considering these
   expressions as nodes in a syntax tree. More importantly, the bound on the
   number of distinct cedents we obtain is sharper: where in [7] it is exponential
   in the size of the syntax tree, our bound is linear (yielding a quadratic bound
   on the number of sequents).
 – Completeness: the structure of the argument is identical to that in [7], but
   the details diﬀer due to the diﬀerent rules and diﬀerent type of sequents.
   This for instance shows in our proof of Lemma 9 (which is analogous to
4        J. Rooduijn et al.

      Lemma 20 in [7]), where we make crucial use of the set of atoms annotating
      a sequent.
    – Complexity: our complexity argument is necessarily diﬀerent because it ap-
      plies to a diﬀerent system and is designed to give a diﬀerent upper bound.

Due to space limitations several proofs are only sketched or omitted entirely. Full
versions of these proofs can be found in the extended version of this paper [15].


2      Preliminaries

2.1     Syntax

The language of GKAT has two sorts, namely programs and a subset thereof
consisting of tests. It is built from a ﬁnite and non-empty set T of primitive tests
and a non-empty set Σ of primitive programs, where T and Σ are disjoint. For
the rest of this paper we ﬁx such sets T and Σ. We reserve the letters t and p to
refer, respectively, to arbitrary primitive tests and primitive programs. The ﬁrst
of the following grammars deﬁnes the tests, and the second the expressions.

        b, c ::= 0 | 1 | t | b | b ∨ c | b · c   e, f ::= b | p | e · f | e +b f | e(b) ,

where t ∈ T and p ∈ Σ. Intuitively, the operator +b stands for the if-then-else
construct, and the operator (−)(b) stands for the while loop. Note that the
tests are simply propositional formulas. It is convention to use · instead of ∧
for conjunction. As usual, we often omit · for syntactical convenience, e.g. by
writing pq instead of p · q.
Example 1. The idea of GKAT is to model imperative programs. For instance, the
expression (p +b q)(a) represents the following imperative program:
                               while a do (if b then p else q)

Remark 1. As mentioned in the introduction, GKAT is a fragment of Kleene Al-
gebra with Tests, or KAT [10]. The syntax of KAT is the same as that of GKAT, but
with unrestricted union + instead of guarded union +b , and unrestricted itera-
tion (−)∗ instead of the while loop operator (−)(b) . The embedding ϕ of GKAT
into KAT acts on guarded union and guarded iteration as follows, and commutes
with all other operators: ϕ(e +b f ) = b · ϕ(e) + b · ϕ(f ), and ϕ(e(b) ) = (b · ϕ(e))∗ · b.


2.2     Semantics

There are several kinds of semantics for GKAT. In [22], a language semantics, a
relational semantics, and a probabilistic semantics are given. In this paper we
are only concerned with the language semantics, which we shall now describe.
    We denote by At the set of atoms of the free Boolean algebra generated
by T = {t1 , . . . tn }. That is, At consists of all tests of the form c1 · · · cn , where
ci ∈ {ti , ti } for each 1 ≤ i ≤ n. Lowercase Greek letters (α, β, γ, . . .) will be
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)              5

used to denote elements of At. A guarded string is an element of the regular
set At · (Σ · At)∗ . That is, a string of the form α1 p1 α2 p2 · · · αn pn αn+1 . We will
interpret expressions as languages (formally just sets) of guarded strings. The
sequential composition operator · is interpreted by the fusion product ⋄, given
by L ⋄ K := {xαy | xα ∈ L and αy ∈ K}. For the interpretation of +b , we
deﬁne for every set of atoms B ⊆ At the following operation of guarded union on
languages: L +B K := (B ⋄ L) ∪ (B ⋄ K), where B is At \ B. For the interpretation
of (−)(b) , we stipulate:
                                                             [
          L0 := At          Ln+1 := Ln ⋄ L          LB :=         (B ⋄ L)n ⋄ B
                                                             n≥0

Finally, the semantics of GKAT is inductively deﬁned as follows:
    JbK := {α ∈ At : α ≤ b}      JpK := {αpβ : α, β ∈ At}       Je · f K := JeK ⋄ Jf K
                                      (b)          JbK
    Je +b f K := JeK +JbK Jf K   Je         K := JeK
Note that the interpretation of · between tests is the same whether they are
regarded as tests or as programs, i.e. JbK ∩ JcK = JbK ⋄ JcK.
Remark 2. While the semantics of expressions is explicitly deﬁned, the semantics
of tests is derived implicitly through the free Boolean algebra generated by T . It
is standard in the GKAT literature to address the Boolean content in this manner.
Example 2. In a guarded string, atoms can be thought of as states of a machine,
and programs as executions. For instance, in case of the guarded string αpβ,
the machine starts in state α, then executes program p, and ends in state β.
Let us brieﬂy check which guarded strings of, say, the form αpβqγ belong to the
interpretation J(p +b q)(a) K of the program of Example 1. First, we must have
α ≤ a, for otherwise we would not enter the loop. Moreover, we have α ≤ b, for
otherwise q rather than p would be executed. Similarly, we ﬁnd that β ≤ a, b.
Since the loop is exited after two iterations, we must have γ ≤ a. Hence, we ﬁnd
            αpβqγ ∈ J(p +b q)(a) K ⇔ α ≤ a, b and β ≤ a, b and γ ≤ a.
We state two simple facts that will be useful later on.
Lemma 1. For any two languages L, K of guarded strings, and primitive pro-
gram p, we have:
(i) Ln+1 = L ⋄ Ln ;       (ii) JpK ⋄ L = JpK ⋄ K implies L = K.
Remark 3. The fact that GKAT models deterministic programs is reﬂected in the
fact that sets of guarded strings arising as interpretations of GKAT-expressions
satisfy a certain determinacy property. Namely, for every xαy and xαz in L,
either y and z are both empty, or both begin with the same primitive program.
We refer the reader to [22] for more details.
Remark 4. The language semantics of GKAT is the same as that of KAT (see [10]),
in the sense that JeK = Jϕ(e)K, where ϕ is the embedding from Remark 1, the
semantic brackets on the right-hand side denote the standard interpretation in
KAT, and e is any GKAT-expression.
6        J. Rooduijn et al.

3     The non-well-founded proof system SGKAT∞

In this section we commence our proof-theoretical study of GKAT. We will present
a cyclic sequent system for GKAT, inspired by the cyclic sequent system for Kleene
Algebra presented in [7]. In passing, we will compare our system to the latter.
Definition 1 (Sequent). A sequent is a triple (Γ, A, ∆), written Γ ⇒A ∆,
where A ⊆ At and Γ and ∆ are (possibly empty) lists of GKAT-expressions.
The list on the left-hand side of a sequent is called its antecedent , and the list
on the right-hand side its succedent . In general we refer to lists of expressions as
cedents. The symbol ǫ refers to the empty cedent.
Remark 5. As the system in [7] only deals with Kleene Algebra, it does not
include tests. We choose the deal with the tests present in GKAT by augmenting
each sequent by a set of atoms. This tucks away the Boolean content, as is usual
in the GKAT literature, allowing us to omit propositional rules.
Definition 2 (Validity). We say that a sequent e1 , . . . , en ⇒A f1 , . . . , fm is
valid whenever A ⋄ Je1 · · · en K ⊆ Jf1 · · · fn K.
We often abuse notation writing JΓ K instead of Je1 · · · en K, where Γ = e1 , . . . , en .


         Left logical rules

                  Γ ⇒A↾b ∆                 e, Γ ⇒A↾b ∆         f, Γ ⇒A↾b ∆
                            b-l                                                +b -l
                  b, Γ ⇒A ∆                        e +b f, Γ ⇒A ∆


                e, g, Γ ⇒A ∆              e, e(b) , Γ ⇒A↾b ∆       Γ ⇒A↾b ∆
                              ·-l                                                (b)-l
                e · g, Γ ⇒A ∆                        e(b) , Γ ⇒A ∆

         Right logical rules

                      Γ ⇒A ∆                  Γ ⇒A↾b e, ∆       Γ ⇒A↾b f, ∆
               (†)             b-r                                               +b -r
                     Γ ⇒A b, ∆                      Γ ⇒A e +b f, ∆


                Γ ⇒A e, f, ∆              Γ ⇒A↾b e, e(b) , ∆       Γ ⇒A↾b ∆
                              ·-r                                                (b)-r
                Γ ⇒A e · f, ∆                        Γ ⇒A e(b) , ∆

         Axioms and modal rules

                                          ⊥         Γ ⇒At ∆             Γ ⇒At 0
              ǫ ⇒A ǫ id       Γ ⇒∅ ∆                          k                  k0
                                                 p, Γ ⇒A p, ∆          p, Γ ⇒A ∆

    Fig. 1: The rules of SGKAT. The side condition (†) requires that A ↾ b = A.
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)         7

Example 3. An example of a valid sequent is given by (cp)(b) ⇒At (p(cp +b 1))(b) .
The antecedent denotes guarded strings α1 pα2 p · · · αn pαn+1 where αi ≤ b, c for
each 1 ≤ i ≤ n, and αn+1 ≤ b. The succedent denotes such strings where αi ≤ c
is only required for those 1 ≤ i ≤ n where i is even.
Remark 6. Like the sequents for Kleene Algebra in [7], our sequents express
language inclusion, rather than language equivalence. For Kleene Algebra this
diﬀerence is insigniﬁcant, as the two notions are interdeﬁnable using unrestricted
union: JeK ⊆ Jf K ⇔ Je + f K = Jf K. For GKAT, however, it is not clear how to deﬁne
language inclusion in terms of language equivalence. As a result, an advantage
of axiomatising language inclusion rather than language equivalence, is that the
while-operator can be axiomatised as a least ﬁxed point, eliminating the need
for a strict productivity requirement as is present in the axiomatisation in [22].
Given a set of atoms A and a test b, we write A ↾ b for A ⋄ JbK, i.e. the set of
atoms {α ∈ A : α ≤ b}. The rules of SGKAT are given in Figure 1. Importantly,
the rules are always applied to the leftmost expression in a cedent. As a result,
we have the following lemma, that later will be used in the completeness proof.
Lemma 2. Let Γ ⇒A ∆ be a sequent, and let r be any rule of SGKAT. Then
there is at most one rule instance of r with conclusion Γ ⇒A ∆.
Remark 7. Following [7], we call k a ‘modal’ rule. The reason is simply that it
looks like the rule k (sometimes called K or ) in the standard sequent calculus
for basic modal logic. Our system also features a second modal rule, called k0 .
Like k, this rule adds a primitive program p to the antecedent of the sequent.
Since the premiss of k0 entails that JΓ K = J0K, the antecedent of its conclusion
will denote the empty language, and is therefore included in any succedent ∆.
Remark 8. Note that the rules of SGKAT are highly symmetric. Indeed, the only
rules that behave diﬀerently on the left than on the right, are the b-rules and
k0 . Note that b-l changes the set of atoms, while b-r uses a side condition. The
asymmetry of k0 is clear: the succedent of the premiss has a 0, whereas the
antecedent does not. A third asymmetry will be introduced in Deﬁnition 3, with
a condition on inﬁnite branches that is sensitive to (b)-l but not to (b)-r.
Remark 9. The authors of [20] study a variant of GKAT that omits the so-called
early termination axiom, which equates all programs that eventually fail. They
give a denotational model of this variant in the form of certain kinds of trees.
We conjecture that omitting the rule k0 from our system will make it sound and
complete with respect to this denotational model.
An SGKAT∞ -derivation is a (possibly inﬁnite) tree generated by the rules of
SGKAT. Such a derivation is said to be closed if every leaf is an axiom.
Definition 3 (Proof ). A closed SGKAT∞ -derivation is said to be an SGKAT∞ -
proof if every infinite branch is fair for (b)-l, i.e. contains infinitely many appli-
cations of the rule (b)-l.
We write SGKAT ⊢∞ Γ ⇒A ∆ if there is an SGKAT∞ -proof of Γ ⇒A ∆.
8         J. Rooduijn et al.

Example 4. Not every SGKAT∞ -derivation is a proof. Consider for instance the
following derivation, where (•) indicates that the derivation repeat itself.


                        p ⇒At↾b 1, 1(b) , p (•)             p ⇒∅ p ⊥
               (b)-r
                                        p ⇒At↾b 1(b) , p
                          1-r                                                   ǫ ⇒At ǫ id
                                   p ⇒At↾b 1, 1(b) , p (•)                     p ⇒At↾b p k
                                                                                         (b)-r
                                                        p ⇒At 1(b) , p
                                                                         ·-r
                                                      p ⇒At 1(b) · p

                        Fig. 2: An SGKAT∞ -derivation that is not a proof.

Example 5. Let ∆1 := (p(cp +b 1))(b) and ∆2 := cp +b 1, ∆1 . The following proof
Π1 is an example SGKAT∞ -proof of the sequent of Example 3. We again use (•)
to indicate that the proof repeats itself at this leaf and, for the sake of readability,
omit branches that can be closed immediately by an application of ⊥.

                  (cp)(b) ⇒At ∆1 (•)
           k
                 p, (cp)(b) ⇒At↾bc p, ∆1
        c-r
                p, (cp)(b) ⇒At↾bc c, p, ∆1
        ·-r
                p, (cp)(b) ⇒At↾bc cp, ∆1                  ǫ ⇒At↾b ǫ id
       +b -r                                                          (b)-r
                            (b)
                  p, (cp)         ⇒At↾bc ∆2              ǫ ⇒At↾b ∆1
          c-l                   (b)                                    1-r
                 c, p, (cp)           ⇒At↾b ∆2          ǫ ⇒At↾b 1, ∆1
          ·-l                (b)                                       +b -r
                  cp, (cp)            ⇒At↾b ∆2           ǫ ⇒At↾b ∆2
                                                                      (b)-l
                                       (cp)(b) ⇒At ∆2
                   k
                         p, (cp)(b) ⇒At↾bc p, (cp +b 1), ∆1
                 ·-r
                         p, (cp)(b) ⇒At↾bc p(cp +b 1), ∆1
                (b)-r
                                   p, (cp)(b) ⇒At↾bc ∆1
                          c-l
                                  c, p, (cp)(b) ⇒At↾b ∆1                           ǫ ⇒At↾b ǫ id
                          ·-l                                                                 (b)-r
                                   cp, (cp)(b) ⇒At↾b ∆1                           ǫ ⇒At↾b ∆1
                                                                                              (b)-l
                                                      (cp)(b) ⇒At ∆1 (•)

                                        Fig. 3: The SGKAT∞ -proof Π1 .

   To illustrate the omission of branches that can be immediately closed by an
application of ⊥, let us write out the two applications of +b -r in Π1 .
                                                  ⊥        ⊥
    ǫ ⇒At↾bc cp, ∆1     ǫ ⇒∅ 1, ∆1                             ǫ ⇒∅ cp, ∆1         ǫ ⇒At↾b 1, ∆1
                                   +b -r                                                              +b -r
              ǫ ⇒At↾bc ∆2                                                  ǫ ⇒At↾b ∆2
It can also be helpful to think of the set of atoms as selecting one of the premisses.
  A cyclic proof system for Guarded Kleene Algebra with Tests (full version)       9

We close this section with a useful deﬁnition and a lemma.
Definition 4 (Exposure). A list Γ of expressions is said to be exposed if it
is either empty or begins with a primitive program.
Recall that the sets of primitive tests and primitive programs are disjoint. Hence
an exposed list Γ cannot start with a test. The following easy lemma will be
useful later on.
Lemma 3. Let Γ and ∆ be exposed lists of expressions. Then:
 (i) αx ∈ JΓ K ⇔ βx ∈ JΓ K for all α, β ∈ At
(ii) Γ ⇒At ∆ is valid if and only if Γ ⇒A ∆ is valid for some A 6= ∅.


4    Soundness
In this section we prove that SGKAT∞ is sound. We will ﬁrst prove that well-
founded (that is, ﬁnite) SGKAT∞ -proofs are sound. The following straightfor-
ward facts will be useful in the soundness proof.
Lemma 4. For any set A of atoms, test b, and cedent Θ, we have:
 (i) Je +b f, ΘK = (JbK ⋄ Je, ΘK) ∪ (JbK ⋄ Jf, ΘK);
(ii) Je(b) , ΘK = (JbK ⋄ Je, e(b) , ΘK) ∪ (JbK ⋄ JΘK).
We prioritise the rules of SGKAT in order of occurrence in Figure 1, reading left-
to-right, top-to-bottom. Hence, each left logical rule is of higher priority than
each right logical rule, which is of higher priority than each axiom or modal rule.
Recall that a rule is sound if the validity of all its premisses implies the validity
of its conclusion. Conversely, a rule is invertible if the validity of its conclusion
implies the validity of all of its premisses.
    We say that a rule application has priority of there is no higher-priority rule
with the same conclusion. Conveniently, the following proposition entails that
every rule instance which has priority is invertible. This will aid our proof search
procedure in Section 6 .
Proposition 1. Every rule of SGKAT is sound. Moreover, every rule is invert-
ible except for k and k0 , which are invertible whenever they have priority.

Proof (sketch). We treat two illustrative cases. For the rule +b -r, we ﬁnd

                     A ⋄ JΓ K ⊆ Je +b f K ⋄ J∆K
                       ⇔ A ⋄ JΓ K ⊆ (JbK ⋄ Je, ∆K) ∪ (JbK ⋄ Jf, ∆K)
                         ⇔ A ↾ b ⋄ JΓ K ⊆ Je, ∆K or A ↾ b ⊆ Jf, ∆K,

where the ﬁrst equivalence holds due to Lemma 4.(ii), and the second due to
A ⋄ JΓ K = (JbK ⋄ A ⋄ JΓ K) ∪ (JbK ⋄ A ⋄ JΓ K) and Lemma 4.(i).
   The other rule we will treat is k. Suppose ﬁrst that some application of k
does not have priority. The only rule of higher priority than k which can have
10      J. Rooduijn et al.

a conclusion of the form p, Γ ⇒A p, ∆ is ⊥. In this case A = ∅, which means
that the conlusion must be valid. Hence any application of k that does not have
priority is vacuously sound. It need, however, not be invertible, as the following
rule instance demonstrates
                                      1 ⇒At 0
                                 k
                                    p, 1 ⇒∅ p, 0
   Next, suppose that some application of k does have priority. This means that
the set A of atoms in the conclusion p, Γ ⇒A p, ∆ is not empty. We will show
that under this restriction the rule is both sound and invertible. Let α ∈ A. We
have

      A ⋄ Jp, Γ K ⊆ Jp, ∆K ⇔ A ⋄ JpK ⋄ JΓ K ⊆ JpK ⋄ J∆K               (seq. int.)
                           ⇔ α ⋄ JpK ⋄ JΓ K ⊆ JpK ⋄ J∆K         (α ∈ A, Lem. 3)
                             ⇔ JpK ⋄ JΓ K ⊆ JpK ⋄ J∆K                   (Lem. 3)
                             ⇔ JΓ K ⊆ J∆K,                                   (†)

as required. The step marked by † is the following property of guarded languages:
JpK ⋄ L = JpK ⋄ K implies L = K.

Proposition 1 entails that all ﬁnite proofs are sound. We will now extend this
result to non-well-founded proofs, closely following the treatment in [7]. We ﬁrst
recursively deﬁne a syntactic abbreviation: [e(b) ]0 := b and [e(b) ]n+1 := be[e(b) ]n .


Lemma 5. For every n ∈ N: if we have SGKAT ⊢∞ e(b) , Γ ⇒A ∆, then we also
have SGKAT ⊢∞ [e(b) ]n , Γ ⇒A ∆.
We let the while-height wh(e) be the maximal nesting of while loops in a given
expression e. Formally,
 – wh(b) = wh(p) = 0;               − wh(e · f ) = wh(e +b f ) = max{wh(e), wh(f )};
 – wh(e(b) ) = wh(e) + 1.
Given a list Γ , the weighted while-height wwh(Γ ) of Γ is deﬁned to be the
multiset [wh(e) : e ∈ Γ ]. We order such multisets using the Dershowitz–Manna
ordering (for linear orders): we say that N < M if and only if N 6= M and for
the greatest n such that N (n) 6= M (n), it holds that N (n) < M (n).
    Note that in any SGKAT-derivation the weighted while-height of the an-
tecedent does not increase when reading bottom-up. Moreover, we have:
Lemma 6. wwh([e(b) ]n , Γ ) < wwh(e(b) , Γ ) for every n ∈ N.
Finally, we can prove the soundness theorem using induction on wwh(Γ ).
Theorem 1 (Soundness). If SGKAT ⊢∞ Γ ⇒A ∆, then A ⋄ JΓ K ⊆ J∆K.

Proof. We prove this by induction on wwh(Γ ). Given a proof π of Γ ⇒A ∆, let
B contain for each inﬁnite branch of π the node of least depth to which a rule
(b)-l is applied. Note that B must be ﬁnite, for otherwise, by Kőnig’s Lemma,
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)            11

the proof π cut oﬀ along B would have an inﬁnite branch that does not satisfy
the fairness condition.
    Note that Proposition 1 entails that of every ﬁnite derivation with valid leaves
the conclusion is valid. Hence, it suﬃces to show that each of the nodes in B is
valid. To that end, consider an arbitrary such node labelled e(b) , Γ ′ ⇒A′ ∆′ and
the subproof π ′ it generates. By Lemma 5, we have that [e(b) ]n , Γ ′ ⇒A′ ∆′ is
provable for every n. Lemma 6 gives wwh([e(b) ]n , Γ ′ ) < wwh(e(b) , Γ ′ ) ≤ wwh(Γ ),
and thus we may apply the induction hypothesis to obtain

                               A′ ⋄ J[e(b) ]n K ⋄ JΓ K ⊆ J∆K

for every n ∈ N. Then by
       [                                 [
         (A′ ⋄ J[e(b) ]n K ⋄ JΓ K) = A′ ⋄ (J[e(b) ]n K) ⋄ JΓ K = A′ ⋄ JeKJbK ⋄ JΓ K,
       n                                  n

we obtain that e(b) , Γ ′ ⇒A′ ∆′ is valid, as required.


5    Regularity
Before we show that SGKAT∞ is not only sound, but also complete, we will
ﬁrst show that every SGKAT∞ -proof is finite-state, i.e. that it contains at most
ﬁnitely many distinct sequents.
    The results of this section crucially depend on the fact that we are only
applying rules to the leftmost expressions of cedents. Indeed, otherwise one could
easily create inﬁnitely many distinct sequents by simply unravelling the same
while loop e(b) inﬁnitely often.
    Our treatment diﬀers from that in [7] in two major ways. First, we formalise
the notion of (sub)occurrence using the standard notion of a syntax tree. Sec-
ondly, and more importantly, we obtain a quadratic bound on the number of
distinct sequents occurring in a proof, rather than an exponential one. In fact,
we will show that the number of distinct antecedents (succedents) is linear in
the size of the syntax tree of the antecedent (succedent) of the root. We will do
this by showing that each leftmost expression of a cedent in the proof (given
as node of the syntax tree of a root cedent) can only occur in the proof as the
leftmost expresson of that unique cedent.
Definition 5. The syntax tree (Te , le ) of an expression e is a well-founded,
labelled and ordered tree, defined by the following induction on e.
 – If e is a test or primitive program, its syntax tree only has a root node ρ,
   with label le (ρ) := e.
 – If e = f1 ◦ f2 where ◦ = · or ◦ = +b , its syntax tree again has a root node ρ
   with label le (ρ) = e, and with two outgoing edges. The first edge connects ρ
   to (Tf1 , lf1 ), the second edge connects it to (Tf2 , lf2 ).
 – If e = f (b) , its syntax tree again has a root node ρ with label le (ρ) = e, but
   now with just one outgoing edge. This edge connects ρ to (Tf , lf ).
12        J. Rooduijn et al.

Definition 6. An e-cedent is a list of nodes in the syntax tree of e. The reali-
sation of an e-cedent u1 , . . . , un is the cedent le (u1 ), . . . , le (un ).

Given the leftmost expression of a cedent, we will now explicitly deﬁne the cedent
that it must be the leftmost expression of.

Definition 7. Let u be a node in the syntax tree of e. We define the e-cedent
tail(u) inductively as follows:

 – For the root ρ of Te , we set tail(ρ) to be the empty list ǫ.
 – For every node u of Te , we define tail on its children by a case distinction
   on the main connective mc of u:
    • if mc = ·, let u1 and u2 be, respectively, the first and second child of u.
       We set tail(u1 ) := u2 , tail(u) and tail(u2 ) := tail(u).
    • if mc = +b , let u1 and u2 again be its first and second child. We set
       tail(u1 ) := tail(u2 ) := tail(u).
    • if mc = (−)(b) , let v be the single child of u. We set tail(v) := u, tail(u).

An e-cedent is called tail-generated if it is empty or of the form u, tail(u) for
some node u in the syntax tree of e.

Example 6. Below is the syntax tree of (p(p+b 1))(b) and a calculation of tail(u3 ).

            u5         u6


                               l(u1 ) = (p(p +b 1))(b)
     u3          u4
                               l(u2 ) = p(p +b 1)
                                                         tail(u3 ) = u4 , tail(u2 )
                               l(u3 ) = p
                                                                  = u4 , u1 , tail(u1 )
                               l(u4 ) = p +b 1
            u2                                                    = u4 , u1
                               l(u5 ) = p
                               l(u6 ) = 1
            u1

The following lemma embodies the key idea for the main result of this section:
every leftmost expression is the leftmost expression of a unique cedent.

Lemma 7. Let π be an SGKAT∞ -derivation of a sequent of the form e ⇒A f .
Then every antecedent in π is the realisation of a tail-generated e-sequent, and
every succedent is the realisation of a tail-generated f -sequent or 0-sequent.

Proof. We ﬁrst prove the following claim.

     Let e be an expression and let u be a node in its syntax tree. Then tail(u)
     is a tail-generated e-sequent.
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)            13

We prove this by induction on the syntax tree of e. For the root ρ, we have
tail(ρ) = ǫ, which is tail-generated by deﬁnition. Now suppose that the thesis
holds for some arbitrary node u in the syntax tree of e. We will show that the
thesis holds for the children of u by a case distinction on the main connective
mc of u.

 – mc = ·. Let u1 and u2 be the ﬁrst and second child of u, respectively. We
   have tail(u1 ) = u2 , tail(u) = u2 , tail(u2 ), which is tail-generated by deﬁnition.
   Moreover, we have that tail(u2 ) = tail(u) is tail-generated by the induction
   hypothesis.
 – mc = +b . Then for each child v of u, we have tail(v) = tail(u) and thus we
   can again invoke the induction hypothesis.
 – mc = (−)(b) . Then for the single child v of u, it holds that tail(v) = u, tail(u),
   which is tail-generated by deﬁnition.

Using this claim, the lemma follows by bottom-up induction on π. For the base
case, note that e and f are realisations of the roots of their respective syntax
trees. Such a root ρ is tail-generated, since ρ = ρ, ǫ = ρ, tail(ρ). The induction
step follows by direct inspection of the rules of SGKAT.

The number of realisations of tail-generated e-sequents is clearly linear in the
size of the syntax tree of e, for every expression e. Hence we obtain:
Corollary 1. The number of distinct sequents in an SGKAT∞ -proof of e ⇒A f
is quadratic in |Te | + |Tf |.
Note that the above lemma and corollary can easily be generalised to arbitrary
(rather than singleton) cedents, by rewriting each cedent e1 , . . . , en as e1 · · · en .
    Recall that a non-well-founded tree is regular if it contains only ﬁnitely many
pairwise non-isomorphic subtrees. The following corollary follows by a standard
argument in the literature (see e.g [16, Corollary I.2.23]).
Corollary 2. If Γ ⇒A ∆ has an SGKAT∞ -proof, then it has a regular one.
We deﬁne a cyclic SGKAT-proof as a regular SGKAT∞ -proof. Cyclic proofs can
be equivalently described using ﬁnite trees with back edges, but this is not needed
for the purposes of the present paper.


6    Completeness and complexity

In this section we prove the completeness of SGKAT∞ . Our argument uses a
proof search procedure, which we will show to induce a NLOGSPACE decision
procedure for the language inclusion problem of GKAT expressions. The material
in this section is again inspired by [7], but requires several modiﬁcations to treat
the tests present in GKAT.
    First note the following fact.
Lemma 8. Any valid sequent is the conclusion of some rule application.
14      J. Rooduijn et al.

Note that in the following lemma A and B may be distinct.
Lemma 9. Let π be a derivation using only right logical rules and containing a
branch of the form:
                            Γ ⇒B e(b) , ∆
                                  ..                                       (*)
                                   .      (b)-r
                            Γ ⇒A e(b) , ∆
such that (1) Γ ⇒A e(b) , ∆ is valid, and (2) every succedent on the branch has
e(b) , ∆ as a final segment. Then Γ ⇒B 0 is valid.
Proof. We claim that e(b) ⇒B 0 is provable. We will show this by exploiting the
symmetry of the left and right logical rules of SGKAT (cf. Remark 8). Since on the
branch (*) every rule is a right logical rule, and e(b) , ∆ is preserved throughout,
we can construct a derivation π ′ of e(b) ⇒B 0 from π by applying the analogous
left logical rules to e(b) . Note that the set of atoms B precisely determines the
branch (*), in the sense that for every leaf Γ ⇒C Θ of π it holds that C ∩ B = ∅.
Hence, as the root of π ′ is e(b) ⇒B 0, every branch of π ′ except for the one
corresponding to (*) can be closed directly by an application of ⊥. The branch
corresponding to (*) is of the form

                                     e(b) ⇒B 0
                                          ..                                    (*)
                                           .   (b)-l
                                     e(b) ⇒B 0
and can thus be closed by a back edge. The resulting ﬁnite tree with back edges
clearly represents an SGKAT∞ -proof.
    Now by soundness, we have B ⋄ Je(b) K = ∅. Moreover, by the invertibility of
the right logical rules and hypothesis (1), we get

                             B ⋄ JΓ K ⊆ B ⋄ Je(b) K ⋄ J∆K = ∅,

as required.
Lemma 10. Let (Γn ⇒An ∆n )n∈ω be an infinite branch of some SGKAT∞ -
derivation on which the rule (b)-r is applied infinitely often. Then there are n, m
with n < m such that the following hold:
  (i) the sequents Γn ⇒An ∆n and Γm ⇒Am ∆m are equal;
 (ii) the sequent Γn ⇒An ∆n is the conclusion of (b)-r in π;
(iii) for every i ∈ [n, m) it holds that ∆n is a final segment of ∆i .
Proof. First note that k0 is not applied on this branch, because if it were then
there could not be inﬁnitely many applications of (b)-r.
   Since the proof is ﬁnite-state (cf. Corollary 1), there must be a k ≥ 0 be such
that every ∆i with i ≥ k occurs inﬁnitely often on the branch above. Denote by
|∆| the length of a given list ∆ and let l be minimum of {|∆i | : i ≥ k}. In other
words, l is the minimal length of the ∆i with i ≥ k.
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)        15

    To prove the lemma, we ﬁrst claim that there is an n ≥ k such that |∆n | = l
and the leftmost expression in ∆n is of the form e(b) for some e. Suppose, towards
a contradiction, that this is not the case. Then there must be a u ≥ k such that
|∆u | = l and the leftmost expression in ∆u is not of the form e(b) for any e.
Note that (b)-r is the only rule apart from k0 that can increase the length of
the succedent (when read bottom-up). It follows that for no w ≥ u the leftmost
expression in ∆w is of the form e(b) , contradicting the fact that (b)-r is applied
inﬁnitely often.
    Now let n ≥ k be such that |∆n | = l and the leftmost expression of ∆n
is e(b) . Since the rule (b)-r must at some point after ∆n be applied to e(b) , we
may assume without loss of generality that Γn ⇒An ∆n is the conclusion of an
application of (b)-r. By the pigeonhole principle, there must be an m > n such
that Γn ⇒An ∆n and Γm ⇒Am ∆m are the same sequents. We claim that these
sequents satisfy the three properties above. Properties (i) and (ii) directly hold
by construction. Property (iii) follows from the fact that ∆n is of minimal length
and has e(b) as leftmost expression.
With the above lemmas in place, we are ready for the completeness proof.
Theorem 2 (Completeness). Every valid sequent is provable in SGKAT∞ .
Proof. Given a valid sequent, we do a bottom-up proof search with the following
strategy. Throughout the procedure all leaves remain valid, in most cases by an
appeal to invertibility.
 1. Apply left logical rules as long as possible. If this stage terminates, it will be
    at a leaf of the form Γ ⇒A ∆, where Γ is exposed. We then go to stage (2).
    If left logical rules remain applicable, we stay in this stage (1) forever and
    create an inﬁnite branch.
 2. Apply right logical rules until one of the following happens:
    (a) We reach a leaf at which no right logical rule can be applied. This means
         that the leaf must be a valid sequent of the form Γ ⇒A ∆ such that Γ is
         exposed, and ∆ is either exposed or begins with a test b such A ↾ b 6= A.
         We go to stage (4).
    (b) If (a) does not happen, then at some point we must reach a valid sequent
         of the Γ ⇒A e(b) , ∆ which together with an ancestor satisﬁes properties
         (i) - (iii) of Lemma 10. In this case Lemma 9 is applicable. Hence we
         must be at a leaf of the form Γ ⇒A e(b) , ∆ such that e(b) ⇒A 0 is valid.
         We then go to stage (3).
    Since at some point either (a) or (b) must be the case, stage (2) always
    terminates.
 3. We are at a valid leaf of the form Γ ⇒A e(b) , ∆, where Γ is exposed. If
    A = ∅, we apply ⊥. Otherwise, if A 6= ∅, we use the validity of Γ ⇒A e(b) , ∆
    and e(b) ⇒A 0 to ﬁnd:
                            A ⋄ JΓ K ⊆ A ⋄ Je(b) K ⋄ J∆K = ∅.
    We claim that JΓ K = ∅. Indeed, suppose towards a contradiction that αx ∈
    JΓ K. By the exposedness of Γ and item (i) of Lemma 3, we would have
16      J. Rooduijn et al.

    βx ∈ JΓ K for some β ∈ A, contradicting the statement above. Therefore, the
    sequent Γ ⇒At 0 is valid. We apply the rule k0 and loop back to stage (1).
    Stage (3) only comprises a single step and thus always terminates.
 4. Let Γ ⇒A ∆ be the current leaf. By construction Γ ⇒A ∆ is valid, Γ is
    exposed, and ∆ is either exposed or begins with a test b such that A ↾ b 6= A.
    Note that only rules id, ⊥, k, and k0 can be applicable. By Lemma 8, at least
    one of them must be applicable. If id is applicable, apply id. If ⊥ is applicable,
    apply ⊥. If k is applicable, apply k and loop back to stage (1). Note that
    this application of k will have priority and is therefore invertible.
    Finally, suppose that only k0 is applicable. We claim that, by validity, the
    list Γ is not ǫ. Indeed, since A is non-empty, and ∆ either begins with a
    primitive program p or a test b such that A ↾ b 6= A, the sequent

                                        ǫ ⇒A ∆

     must be invalid. Hence Γ must be of the form p, Θ. We apply k0 , which has
     priority and thus is invertible, and loop back to stage (1).
     Similarly to stage (3), stage (4) only comprises a single step and thus always
     terminates.

     We claim that the constructed derivation is fair for (b)-l. Indeed, every stage
except stage (1) terminates. Therefore, every inﬁnite branch must either eventu-
ally remain in stage (1), or pass through stages (3) or (4) inﬁnitely often. Since k
and k0 shorten the antecedent, and no left logical rule other than (b)-l lengthens
it, such branches must be fair.

By Corollary 2 we obtain that the subset of cyclic SGKAT-proofs is also complete.


Corollary 3. Every valid sequent has a regular SGKAT∞ -proof.

Proposition 2. The proof search procedure of Theorem 2 runs in coNLOGSPACE.
Hence proof search, and thus also the language inclusion problem for GKAT-
expressions, is in NLOGSPACE.

Proof (sketch). Assume without loss of generality that the initial sequent is of
the form e ⇒A f . We non-deterministically search for a failing branch, at each
iteration storing only the last sequent. By Lemma 7 this can be done by storing
two pointers to, respectively, the syntax trees Te and Tf , together with a set of
atoms. The loop check of stage (2) can be replaced by a counter. Indeed, stage
(2) must always hit a repetition after |At| · |Tf | steps, where m is the number
of nodes in the syntax tree. After this repetition there must be a continuation
that reaches a repetition to which Lemma 9 applies before this stage has taken
2 ·|At|·|Tf | steps in total. Finally, a global counter can be used to limit the depth
of the search. Indeed, a failing branch needs at most one repetition (in stage (2),
to which k0 is applied) and all other repetitions can be cut out. Hence if there
is a failing branch, there must be one of size at most 4 · |Te | · |At| · |Tf |.
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)           17

7    Conclusion and future work

In this paper we have presented a non-well-founded proof system SGKAT∞ for
GKAT. We have shown that the system is sound and complete with respect to
the language model. In fact, the fragment of regular proofs is already complete,
which means one can view SGKAT as a cyclic proof system. Our system is similar
to the system for Kleene Algebra in [7], but the deterministic nature of GKAT
allows us to use ordinary sequents rather than hypersequents. To deal with
the tests of GKAT every sequent is annotated by a set of atoms. Like in [7],
our completeness argument makes use of a proof search procedure. Here again
the relative simplicity of GKAT pays oﬀ: the proof search procedure induces an
NLOGSPACE decision procedure, whereas that of Kleene Algebra is in PSPACE.
    The most natural question for future work is whether our system could be
used to prove the completeness of some (ordered)-algebraic axiomatisation of
GKAT. We envision using the original GKAT axioms (see [22, Figure 1]), but basing
it on inequational logic rather than equational logic. This would allow one to
use a least ﬁxed point rule of the form
                                     eg +b f ≤ g
                                       e(b) f ≤ g
eliminating the need for a Salomaa-style side condition. We hope to be able
to prove the completeness of such an inequational system by translating cyclic
SGKAT-proofs into well-founded proofs in the inequational system. This is in-
spired by the paper [6], where a similar strategy is used to give an alternative
proof of the left-handed completeness of Kleene Algebra.
    Another relevant question is the exact complexity of the language inclusion
problem for GKAT-expressions. We have obtained an upper bound of NLOGSPACE,
but do not know whether it is optimal.
    Finally, it would be interesting to verify the conjecture in Remark 9 above.

    Acknowledgments. Jan Rooduijn thanks Anupam Das, Tobias Kappé, Johannes
Marti and Yde Venema for insightful discussions on the topic of this paper. Alexandra
Silva wants to acknowledge Sonia Marin, who some years ago proposed a similar mas-
ter project at UCL. We moreover thank the reviewers for their helpful comments, in
particular for pointing out that our complexity result could be sharpened. Lastly, Jan
Rooduijn is grateful for the inspiring four-week research visit at the Computer Science
department of Cornell in the summer of 2022.


References
 1. Acclavio, M., Curzi, G., Guerrieri, G.: Infinitary cut-elimination via finite approx-
    imations. In: 32nd Annual Conference on Computer Science Logic, CSL. LIPIcs,
    vol. 288, pp. 8:1–8:19. Schloss Dagstuhl (2024)
 2. Afshari, B., Enqvist, S., Leigh, G.E.: Cyclic proofs for the first-order µ-calculus.
    Logic Journal of the IGPL (2022)
18      J. Rooduijn et al.

 3. Afshari, B., Leigh, G.E., Turata, G.M.: Uniform interpolation from cyclic proofs:
    The case of modal mu-calculus. In: 30th International Conference on Automated
    Reasoning with Analytic Tableaux and Related Methods, TABLEAUX. Lecture
    Notes in Computer Science, vol. 12842, pp. 335–353. Springer (2021)
 4. Afshari, B., Wehr, D.: Abstract cyclic proofs. In: 28th International Workshop
    on Logic, Language, Information, and Computation, WoLLIC. Lecture Notes in
    Computer Science, vol. 13468, pp. 309–325. Springer (2022)
 5. Brotherston, J.: Cyclic proofs for first-order logic with inductive definitions. In:
    14th International Conference on Automated Reasoning with Analytic Tableaux
    and Related Methods, TABLEAUX. Lecture Notes in Computer Science, vol. 3702,
    pp. 78–92. Springer (2005)
 6. Das, A., Doumane, A., Pous, D.: Left-handed completeness for Kleene algebra,
    via cyclic proofs. In: 22nd International Conference on Logic for Programming,
    Artificial Intelligence and Reasoning, LPAR. EPiC Series in Computing, vol. 57,
    pp. 271–289 (2018)
 7. Das, A., Pous, D.: A cut-free cyclic proof system for Kleene algebra. In: 26th
    International Conference on Automated Reasoning with Analytic Tableaux and
    Related Methods, TABLEAUX. Lecture Notes in Computer Science, vol. 10501,
    pp. 261–277. Springer (2017)
 8. Dekker, M., Kloibhofer, J., Marti, J., Venema, Y.: Proof systems for the modal
    µ-calculus obtained by determinizing automata. In: 32nd International Confer-
    ence on Automated Reasoning with Analytic Tableaux and Related Methods,
    TABLEAUX. pp. 242–259. Springer (2023)
 9. Kozen, D.: A completeness theorem for Kleene algebras and the algebra of regular
    events. Information and Computation 110(2), 366–390 (1994)
10. Kozen, D.: Kleene algebra with tests. ACM Transactions on Programming Lan-
    guages and Systems 19(3), 427–443 (1997)
11. Kozen, D.: Nonlocal flow of control and Kleene algebra with tests. In: 23rd Annual
    Symposium on Logic in Computer Science, LICS. pp. 105–117. IEEE (2008)
12. Kozen, D., Tseng, W.D.: The Böhm-Jacopini theorem is false, propositionally. In:
    9th International Conference on Mathematics of Program Construction, MPC.
    Lecture Notes in Computer Science, vol. 5133, pp. 177–192. Springer (2008)
13. Kuperberg, D., Pinault, L., Pous, D.: Cyclic proofs, system T, and the power of
    contraction. 48th Annual Symposium on Principles of Programming Languages,
    POPL pp. 1–28 (2021)
14. Marti, J., Venema, Y.: Focus-style proof systems and interpolation for the
    alternation-free µ-calculus (2021), arXiv preprint 2103.01671
15. Rooduijn, J., Kozen, D., Silva, A.: A cyclic proof system for
    Guarded Kleene Algebra with Tests (full version) (2024), available at
    alexandrasilva.org/files/ijcar24-full.pdf
16. Rooduijn, J.: Fragments & Frame Classes. Ph.D. thesis, University of Amsterdam
    (2024)
17. Rozowski, W., Kappé, T., Kozen, D., Schmid, T., Silva, A.: Probabilistic guarded
    KAT modulo bisimilarity: Completeness and complexity. In: 50th International
    Colloquium on Automata, Languages, and Programming, ICALP. LIPIcs, vol. 261,
    pp. 136:1–136:20. Schloss Dagstuhl (2023)
18. Salomaa, A.: Two complete axiom systems for the algebra of regular events. Journal
    of the ACM 13(1), 158–169 (1966)
19. Savateev, Y., Shamkanov, D.S.: Cut-elimination for the modal Grzegorczyk logic
    via non-well-founded proofs. In: 24th International Workshop on Logic, Language,
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)         19

    Information, and Computation WoLLIC. Lecture Notes in Computer Science, vol.
    10388, pp. 321–335. Springer (2017)
20. Schmid, T., Kappé, T., Kozen, D., Silva, A.: Guarded Kleene algebra with tests:
    Coequations, coinduction, and completeness. In: 48th International Colloquium
    on Automata, Languages, and Programming, ICALP. LIPIcs, vol. 198, pp. 142:1–
    142:14. Schloss Dagstuhl (2021)
21. Schmid, T., Kappé, T., Silva, A.: A complete inference system for skip-free guarded
    Kleene algebra with tests. In: 32nd European Symposium on Programming, ESOP.
    Lecture Notes in Computer Science, vol. 13990, pp. 309–336. Springer (2023)
22. Smolka, S., Foster, N., Hsu, J., Kappé, T., Kozen, D., Silva, A.: Guarded Kleene
    algebra with tests: verification of uninterpreted programs in nearly linear time.
    47th Annual Symposium on Principles of Programming Languages, POPL pp.
    61:1–61:28 (2020)
23. Sprenger, C., Dam, M.: On the structure of inductive reasoning: Circular and tree-
    shaped proofs in the µ-calculus. In: 6th International Conference on Foundations
    of Software Science and Computation Structures, FOSSACS. Lecture Notes in
    Computer Science, vol. 2620, pp. 425–440. Springer (2003)
24. Zetzsche, S., Silva, A., Sammartino, M.: Guarded Kleene algebra with tests: Au-
    tomata learning. In: Proceedings of the 38th Conference on the Mathematical Foun-
    dations of Programming Semantics, MFPS. EPTICS, vol. 1. EpiSciences (2022)
20      J. Rooduijn et al.

A     Full proofs

This appendix contains full versions of all the proofs that were either omitted
or sketched in the body of the paper.


A.2    ... of Section 2

Lemma 1. For any two languages L, K of guarded strings, and primitive pro-
gram p, we have:

(i) Ln+1 = L ⋄ Ln ;        (ii) JpK ⋄ L = JpK ⋄ K implies L = K.

Proof. (i). Since At is the identity element for the fusion operator, we have

               Ln+1 = At ⋄ |L ⋄ ·{z                          · · ⋄ L} = L ⋄ Ln ,
                                  · · ⋄ L} = L ⋄ At ⋄ |L ⋄ ·{z
                              n + 1 times                 n times


as required.
    (ii). Since JpK = {αpβ : α, β ∈ At}, we have

               γy ∈ L ⇔ γpγy ∈ JpK ⋄ L ⇔ γpγy ∈ JpK ⋄ K ⇔ γy ∈ K,

as required.


A.3    ... of Section 3

Lemma 3. Let Γ and ∆ be exposed lists of expressions. Then:

 (i) αx ∈ JΓ K ⇔ βx ∈ JΓ K for all α, β ∈ At
(ii) Γ ⇒At ∆ is valid if and only if Γ ⇒A ∆ is valid for some A 6= ∅.

Proof. For item (i), we make a case distinction on whether Γ = ǫ or Γ = p, Θ for
some list Θ. If Γ = ǫ, the result follows immediately from the fact that JǫK = At.
If Γ = p, Θ, we have JΓ K = JpK ⋄ JΘK = {γpδy : γ ∈ At, δy ∈ JΘK}, which also
suﬃces.
    For item (ii), the only non-trivial implication is the one from right to left. So
suppose Γ ⇒A ∆ for some A 6= ∅. Let α ∈ At and let β ∈ A be arbitrary. We
ﬁnd the required:

               αx ∈ JΓ K ⇒ βx ∈ JΓ K                                (item (i))
                          ⇒ βx ∈ J∆K                    (β ∈ A, hypothesis)
                          ⇒ αx ∈ J∆K.                             (item (i))
  A cyclic proof system for Guarded Kleene Algebra with Tests (full version)                21

A.4     ... of Section 4

Lemma 4. Let A be a set of atoms, let b be a test, and let Θ be a list of expres-
sions. We have:

 (i) Je +b f, ΘK = (JbK ⋄ Je, ΘK) ∪ (JbK ⋄ Jf, ΘK);
(ii) Je(b) , ΘK = (JbK ⋄ Je, e(b) , ΘK) ∪ (JbK ⋄ JΘK).

Proof. Both items are shown by simply unfolding the deﬁnitions. We will use
the fact ⋄ distributes over ∪. Note that ∪ is not the same as guarded union, over
which ⋄ is merely right-distributive.
   For the ﬁrst item, we calculate

   Je +b f, ΘK = Je +b f K ⋄ JΘK                               (sequent interpretation)
                 = ((JbK ⋄ JeK) ∪ (JbK ⋄ Jf K)) ⋄ JΘK            (interpretation of +b )
                 = (JbK ⋄ JeK ⋄ JΘK) ∪ (JbK ⋄ Jf K ⋄ JΘK)        (⋄ distributes over ∪)
                 = (JbK ⋄ JeK ⋄ JΘK) ∪ (JbK ⋄ Jf K ⋄ JΘK)                   (JbK = JbK)
                 = (JbK ⋄ Je, ΘK) ∪ (JbK ⋄ Jf, ΘK).            (sequent interpretation)

For the second item, we have

  Je(b) , ΘK = Je(b) K ⋄ JΘK                                               (sequent int.)
                [
             =     (JbK ⋄ JeK)n ⋄ JbK ⋄ JΘK                                   (int. −(b) )
               n≥0
                 [                                                                      [
            =(       (JbK ⋄ JeK)n ∪ At) ⋄ JbK ⋄ JΘK                            (split       )
                n≥1
                 [
            =(       (JbK ⋄ JeK)n ⋄ JbK ⋄ JΘK) ∪ (At ⋄ JbK ⋄ JΘK)             (⋄ dist. ∪)
                n≥1
                 [
            =(       (JbK ⋄ JeK)n ⋄ JbK ⋄ JΘK) ∪ (JbK ⋄ JΘK)                  (JbK = JbK)
                n≥1
                 [
            =(       JbK ⋄ JeK ⋄ (JbK ⋄ JeK)n ⋄ JbK ⋄ JΘK) ∪ (JbK ⋄ JΘK)    (Lem. 1.(i))
                n≥0
                             [                                                          [
            = (JbK ⋄ JeK ⋄       (JbK ⋄ JeK)n ⋄ JbK ⋄ JΘK) ∪ (JbK ⋄ JΘK)     (⋄ dist.       )
                             n≥0

            = (JbK ⋄ JeK ⋄ Je(b) K ⋄ JΘK) ∪ (JbK ⋄ JΘK)                       (int. −(b) )
            = (JbK ⋄ Je, e(b) , ΘK) ∪ (JbK ⋄ JΘK),                         (sequent int.)

as required.

Proposition 1. Every rule of SGKAT is sound. Moreover, every rule is invert-
ible except for k and k0 , which are invertible whenever they have priority.

Proof. We will cover the rules of SGKAT one-by-one.
22        J. Rooduijn et al.

     (b-l) This is immediate by Lemma 4.1.
     (b-r) We have:

                A ⋄ JΓ K ⊆ Jb, ∆K ⇔ A ⋄ JΓ K ⊆ JbK ⋄ J∆K                      (sequent int.)
                                  ⇔ A ↾ b ⋄ JΓ K ⊆ JbK ⋄ J∆K                       (by (†))
                                     ⇔ A ↾ b ⋄ JΓ K ⊆ J∆K                         (A ↾ b ⊆ JbK)
                                     ⇔ A ⋄ JΓ K ⊆ J∆K                                  (by (†))

  (·-l) Immediate, since A ⋄ Je · f, Γ K = A ⋄ Je, f, Γ K.
 (·-r) Likewise, but by Je · f, ∆K = Je, f, ∆K.
(+b -l) This follows directly from the fact that

            A ⋄ Je +b f, Γ K = A ⋄ Je +b f K ⋄ JΓ K                                  (sequent int.)
                               = A ⋄ ((JbK ⋄ Je, Γ K) ∪ (JbK ⋄ Jf, Γ K))              (Lem. 4.(ii))
                               = (A ⋄ JbK ⋄ Je, Γ K) ∪ (A ⋄ JbK ⋄ Jf, Γ K)               (distrib.)
                               = (A ↾ b ⋄ Je, Γ K) ∪ (A ↾ b ⋄ Jf, Γ K)                (Lem. 4.(i))

(+b -r) We ﬁnd

                           A ⋄ JΓ K ⊆ Je +b f K ⋄ J∆K
                               ⇔ A ⋄ JΓ K ⊆ (JbK ⋄ Je, ∆K) ∪ (JbK ⋄ Jf, ∆K)
                                ⇔ A ↾ b ⋄ JΓ K ⊆ Je, ∆K or A ↾ b ⊆ Jf, ∆K,

        where the ﬁrst equivalence holds due to Lemma 4.(ii), and the second
        due to A ⋄ JΓ K = (JbK ⋄ A ⋄ JΓ K) ∪ (JbK ⋄ A ⋄ JΓ K) and Lemma 4.(i).
((b)-l) This follows directly from the fact that

           A ⋄ Je(b) , Γ K = A ⋄ Je(b) K ⋄ JΓ K                                       (sequent int.)
                                                (b)
                          = A ⋄ ((JbK ⋄ Je, e         , Γ K) ∪ (JbK ⋄ Jf, Γ K))       (Lem. 4.(iii))
                                               (b)
                          = (A ⋄ JbK ⋄ Je, e         , Γ K) ∪ (A ⋄ JbK ⋄ Jf, Γ K)         (distrib.)
                          = (A ↾ b ⋄ Je, e(b) , Γ K) ∪ (A ↾ b ⋄ Jf, Γ K)               (Lem. 4.(i))

((b)-r) We ﬁnd

                  A ⋄ JΓ K ⊆ Je(b) , ∆K
                    ⇔ A ⋄ JΓ K ⊆ (JbK ⋄ Je, e(b) , ∆K) ∪ (JbK ⋄ J∆K)
                      ⇔ A ↾ b ⋄ JΓ K ⊆ JbK ⋄ Je, e(b) , ∆K and A ↾ b ⊆ JbK ⋄ J∆K,

           where the ﬁrst equivalence holds due to Lemma 4.3, and the second due
           to A ⋄ JΓ K = (JbK ⋄ A ⋄ JΓ K) ∪ (JbK ⋄ A ⋄ JΓ K) and Lemma 4.1.
      (id) This follows from A ⋄ J1K = A ⋄ At = A ⊆ At = J1K.
      (⊥) We have ∅ ⋄ JΓ K = ∅ ⊆ J∆K.
A cyclic proof system for Guarded Kleene Algebra with Tests (full version)              23

  (k) Suppose ﬁrst that some application of k does not have priority. The
      only rule of higher priority than k which can have a conclusion of the
      form p, Γ ⇒A p, ∆ is ⊥, whence we must have A = ∅. As shown in the
      previous case, this conclusion must be valid. Hence under this restriction
      the rule application is vacuously sound. It is, however, not invertible, as
      the following rule instance demonstrates
                                            1 ⇒At 0
                                      k
                                          p, 1 ⇒∅ p, 0
      Next, suppose that some application of k does have priority. This means
      that the set A of atoms in the conclusion p, Γ ⇒A p, ∆ is not empty. We
      will show that under this restriction the rule is both sound and invertible.
      Let α ∈ A. We have

         A ⋄ Jp, Γ K ⊆ Jp, ∆K ⇔ A ⋄ JpK ⋄ JΓ K ⊆ JpK ⋄ J∆K                (seq. int.)
                               ⇔ α ⋄ JpK ⋄ JΓ K ⊆ JpK ⋄ J∆K       (α ∈ A, Lem. 3)
                               ⇔ JpK ⋄ JΓ K ⊆ JpK ⋄ J∆K                  (Lem. 3)
                               ⇔ JΓ K ⊆ J∆K,                           (Lem. 1.(ii))

       as required.
 (k0 ) For the ﬁnal rule k0 , we will ﬁrst show the soundness of all instances,
       and then the invertibility of those instances which have priority. For
       soundness, suppose that the premiss is valid. Since

                                JΓ K = At ⋄ JΓ K ⊆ J0K = ∅,

      it follows that JΓ K = ∅. Hence

                  A ⋄ Jp, Γ K = A ⋄ JpK ⋄ JΓ K = A ⋄ JpK ⋄ ∅ = ∅ ⊆ J∆K,

      as required.
      For invertibility, suppose that some instance of k0 has priority. Then
      the conclusion p, Γ ⇒A ∆ cannot be the conclusion of any other rule
      application.
      Suppose that p, Γ ⇒A ∆ is valid. We wish to show that Γ ⇒At 0 is valid,
      or, in other words, that JΓ K = ∅.
      First note that, as in the previous case, from the assumption that our
      instance of k0 has priority, it follows that A 6= ∅.
      We now make a case distinction on the shape of ∆. Suppose ﬁrst that
      ∆ = ǫ. Then
                            A ⋄ Jp, Γ K ⊆ J∆K = JǫK = At.
      As A ⋄ Jp, Γ K = {αpβx : α ∈ A and βx ∈ JΓ K}, we must have JΓ K = ∅.
      Next, suppose that ∆ has a leftmost expression e. By the assumption
      that the rule instance has priority, we know that e is not of the form
      e0 · e1 , e0 +b e1 , or e(b) , for otherwise a right logical rule could be applied.
      Hence, the expression e must either be a test or a primitive program.
24      J. Rooduijn et al.

        If e is a test, say b, we know that A ↾ b 6= A, for otherwise b-r could
        be applied. Recall that it suﬃces to show that JΓ K = ∅. So suppose,
        towards a contradiction, that there is some βx ∈ JΓ K. Let α ∈ A such
        that α 6≤ b. Then αpβx ∈ Jp, Γ K ⊆ J∆K. But this contradicts the fact
        that J∆K ⊆ {αy : α ≤ b}.
        Finally, suppose that e is a primitive program, say q. Write ∆ = q, Θ.
        First note that assumption that the rule instance has priority implies
        p 6= q, for otherwise the rule k could be applied. We have:

                             A ⋄ Jp, Γ K ⊆ J∆K = {αqβx : βx ∈ JΘK},

        As A ⋄ Jp, Γ K = {αpβx : α ∈ A and βx ∈ JΓ K} and p 6= q, we again ﬁnd
        that JΓ K = ∅.
This ﬁnishes the proof.

Lemma 5. For every n ∈ N: if we have SGKAT ⊢∞ e(b) , Γ ⇒A ∆, then we also
have SGKAT ⊢∞ [e(b) ]n , Γ ⇒A ∆.

Proof. We assume that A 6= ∅, for otherwise the lemma is trivial. Let π be
the assumed SGKAT∞ -proof of e(b) , Γ ⇒A ∆. Note that, since all succedents
referred to in the lemma are equal to ∆, it suﬃces to prove the lemma under the
assumption that the last rule applied in π is not a right logical rule. Hence, we
may assume that the last rule applied in π is (b)-l, for that is the only remaining
rule with a sequent of this shape as conclusion. This means that π is of the form:
                                     π1                  π2
                              (b)
                       e, e         , Γ ⇒A↾b ∆        Γ ⇒A↾b ∆
                                                                 (b)-l
                                          e(b) , Γ ⇒A ∆
We show the lemma by induction on n. For the induction base, we take the
following proof:
                                π2
                             Γ ⇒A↾b ∆
                                                           b-l
                                       [e(b) ]0 , Γ ⇒A ∆
For the inductive step n + 1, we construct from π1 a proof τ of e, [e(b) ]n , Γ ⇒A↾b
∆. To that end, we ﬁrst replace in π1 every occurrence of e(b) , Γ as a ﬁnal
segment of the antecedent by e(b) , Γ and cut oﬀ all branches at sequents of the
                                  n


       (b) n
form [e ] , Γ ⇒B Θ. This may be depicted as follows, where to the left of the
arrow     we have a branch of π1 , and to right the resulting branch of τ .

                               ..
                                .
                        (b)
                      e , Γ ⇒B Θ                      [e(b) ]n , Γ ⇒B Θ
                                ..                               ..
                                 .                                .
                    e, e(b) , Γ ⇒A↾b ∆                   (b) n
                                                    e, [e ] , Γ ⇒A↾b ∆
 A cyclic proof system for Guarded Kleene Algebra with Tests (full version)        25

Note that every remaining inﬁnite branch in the resulting derivation τ satisﬁes
the fairness condition. Therefore, to turn τ into a proper SGKAT∞ -proof, we only
need to close each open leaf, which by construction is of the form [e(b) ]n , Γ ⇒B ∆.
Note that π1 must contain a proof of e(b) , Γ ⇒B ∆, whence by the induction
hypothesis the sequent [e(b) ]n , Γ ⇒B ∆ is provable. We can thus close the leaf
by simply appending the witnessing proof.
   Letting τ be the resulting proof, we ﬁnish the induction step by taking:
                                            τ
                                      (b) n
                              e, [e     ] , Γ ⇒A↾b ∆
                                                       b-l
                               [e(b) ]n+1 , Γ ⇒A ∆

which gives us the required SGKAT∞ -proof.

Lemma 6. wwh([e(b) ]n , Γ ) < wwh(e(b) , Γ ) for every n ∈ N.

Proof. Let k := wh(e(b) ). Note that the maximum while-height in [e(b) ]n is that
of e. Hence, we have wwh([e(b) ]n )(k) = 0 < 1 = wwh(e(b) )(k). Therefore:

       wwh([e(b) ]n , Γ )(k) = wwh([e(b) ]n )(k) + wwh(Γ )(k)
                           < wwh(e(b) )(k) + wwh(Γ )(k) = wwh(e(b) , Γ )(k).

Hence wwh([e(b) ]n , Γ ) 6= wwh(e(b) , Γ ). Now suppose that for some l ∈ N we have
wwh([e(b) ]n , Γ )(l) > wwh(e(b) , Γ )(l). We leave it to the reader to verify that in
this case we must have l < k. As wwh([e(b) ]n , Γ )(k) < wwh(e(b) , Γ )(k), we ﬁnd
wwh([e(b) ]n , Γ ) < wwh(e(b) , Γ ).


A.6    ... of Section 6

Lemma 8. Any valid sequent is the conclusion of some rule application.

Proof. We prove this lemma by contraposition. So suppose Γ ⇒A ∆ is not the
conclusion of any rule application. We make a few observations:

 – Both Γ and ∆ are exposed, for otherwise Γ ⇒A ∆ would be the conclusion
   of an application of a left, respectively right, logical rule.
 – A is non-empty, for otherwise Γ ⇒A ∆ would be the conclusion of an appli-
   cation of ⊥.
 – The leftmost expression of Γ is not a primitive program, for otherwise our
   sequent Γ ⇒A ∆ would be the conclusion of an application of k0 .
 – The leftmost expression of ∆ is a primitive program, for otherwise, by the
   previous items, the sequent Γ ⇒A ∆ would be the conclusion of an applica-
   tion of id.

Hence Γ ⇒A ∆ is of the form ǫ ⇒A p, Θ. Let α ∈ A. Then α ∈ A ⋄ JǫK. However,
since α is not of the form βpγy, we have α ∈
                                           / Jp, ΘK. This shows that Γ ⇒A ∆
is not valid, as required.
26      J. Rooduijn et al.

Proposition 2. The proof search procedure of Theorem 2 runs in coNLOGSPACE.
Hence proof search, and thus also the language inclusion problem for GKAT-
expressions, is in NLOGSPACE.

Proof. The exact coNLOGSPACE procedure goes as follows. Without loss of gen-
erality we assume that the input is a sequent of the form e ⇒A f , given as a
triple consisting of the syntax tree Te of e, the set of atoms A, and the syntax
tree of Tf of f . During the procedure we store:
 – One pointer to Te , initialised at the root.
 – One pointer to Tf , initialised at the root.
 – A set of atoms, initially A.
Note that by Lemma 7 these data suﬃce to completely describe a sequent.
Moreover, we store:
 – A counter keeping track of how many steps are taken, initially 1.
 – A variable s ∈ {1, 2, 3, 4} indicating at which of the four stages of the pro-
   cedure we currently are.
The idea is to non-deterministically apply the proof search procedure of Theorem
2. Note, however, that the fact that we are only storing a single sequent prevents
us from performing the loop check that happens in stage (2). As a remedy, we
additionally store
 – A second counter, keeping track of how many steps are taken in stage (2)
   (always resetting at the beginning of stage (2)).
At each iteration we apply the rule dictated by the proof search procedure, non-
deterministically choosing a premiss and updating the data accordingly. Our
non-deterministic procedure searches for a failing branch (i.e. one to which no
rule can be applied). Whenever the ﬁrst counter reaches 4 · |Te | · |At| · |Tf |, it
gives up the search. Moreover, whenever the second counter reaches 2 · |At| · |Tf |,
it applies k0 (this replaces the loop check of stage (2)).
    We claim that this procedure succeeds in ﬁnding a failing branch if it exists.
We ﬁrst justify the application of k0 when the second counter hits its limit.
Consider a list of sequents Γ ⇒A0 ∆0 , . . . , Γ ⇒An ∆n in stage (2), where n =
|At| · |Tf |. By the pidgeonhole principle, this list must repeat some sequent.
Moreover, because the only rule that grows succedents is (b)-r, the segment
between the two repetitions must contain a succedent of the form e(b) , ∆ of
minimal length. But then there is a variant of this branch, of length at most 2n,
where the succedent e(b) , ∆ is repeated and satisﬁes the conditions of Lemma 9.
    Finally, we argue that if there is a failing branch, then there is one of length
smaller than the limit of the ﬁrst counter. This follows from the fact that the
second counter can only hit its limit once (because afterwards the succedent
becomes trivial) and every repetition that happens before or after the corre-
sponding stage (2) can be cut out of the branch.
