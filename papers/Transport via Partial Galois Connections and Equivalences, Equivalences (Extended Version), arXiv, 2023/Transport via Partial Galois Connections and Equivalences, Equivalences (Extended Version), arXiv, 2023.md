                                              Transport via Partial Galois Connections and
                                                    Equivalences (Extended Version)

                                                                Kevin Kappelmann[0000−0003−1421−6497]
arXiv:2303.05244v6 [cs.PL] 18 Mar 2025




                                             Technical University of Munich, Boltzmannstrasse 3, Garching 85748, Germany,
                                                                       kevin.kappelmann@tum.de




                                                 Abstract. Multiple types can represent the same concept. For example,
                                                 lists and trees can both represent sets. Unfortunately, this easily leads to
                                                 incomplete libraries: some set-operations may only be available on lists,
                                                 others only on trees. Similarly, subtypes and quotients are commonly
                                                 used to construct new type abstractions in formal veriﬁcation. In such
                                                 cases, one often wishes to reuse operations on the representation type for
                                                 the new type abstraction, but to no avail: the types are not the same.
                                                 To address these problems, we present a new framework that transports
                                                 programs via equivalences. Existing transport frameworks are either de-
                                                 signed for dependently typed, constructive proof assistants, use univa-
                                                 lence, or are restricted to partial quotient types. Our framework (1) is de-
                                                 signed for simple type theory, (2) generalises previous approaches work-
                                                 ing on partial quotient types, and (3) is based on standard mathematical
                                                 concepts, particularly Galois connections and equivalences. We introduce
                                                 the notions of partial Galois connection and equivalence and prove their
                                                 closure properties under (dependent) function relators, (co)datatypes,
                                                 and compositions. We formalised the framework in Isabelle/HOL and
                                                 provide a prototype.1

                                                 Keywords: Galois connections · Equivalences · Relational parametricity



                                         1     Introduction

                                         Computer scientists often write programs and proofs in terms of representation
                                         types but provide their libraries in terms of diﬀerent, though related, type ab-
                                         stractions. For example, the abstract type of ﬁnite sets may be represented by
                                         the type of lists: every ﬁnite set is related to every list containing the same ele-
                                         ments and, conversely, every list is related to its set of elements. As such, every
                                         function on lists respecting this relation may be reused for a library on ﬁnite
                                         sets. To be more explicit, consider the following example in simple type theory:
                                         1
                                             Non-peer reviewed, extended version of “Transport via Partial Galois Connections
                                             and Equivalences”, 21st Asian Symposium on Programming Languages and Systems
                                             (APLAS), 2023 [15]
2       Kevin Kappelmann

A Simple Example Take the types of lists, α list, and ﬁnite sets, α fset. There is
a function to_fset : α list ⇒ α fset that turns a list into its set of elements. This
allows us to deﬁne the relation LFS xs s := to_fset xs = s that identiﬁes lists and
ﬁnite sets, e.g. LFS [1, 2, 3] {1, 2, 3} and LFS [3, 1, 2] {1, 2, 3}. Our goal is to use
this identiﬁcation to transport programs between these two types.
    For instance, take the function max_list xs := foldr max xs 0 of type N list ⇒ N
that returns the maximum natural number contained in a list. After some think-
ing, one recognises that max_list respects the relation LFS in the following sense:
if two lists correspond to the same set, then applying max_list to these lists re-
turns equal results. Formally,

          ∀xs ys. to_fset xs = to_fset ys −→ max_list xs = max_list ys.             (1)

Despite this insight, we still cannot directly compute the maximum of a ﬁnite
set s : N fset using max_list; the term max_list s does not even typecheck (for
good reasons). But there is an indirect way if we are also given an “inverse” of
to_fset, call it to_listfin : α fset ⇒ α list, that returns an arbitrary list containing
the same elements as the given set. The functions to_fset and to_listfin form an
equivalence between α list and α fset that respects the relation LFS:

            ∀xs. LFS xs (to_fset xs)       and      ∀s. LFS (to_listfin s) s.       (2)

Thanks to this equivalence, we can compute the maximum of s by simply trans-
porting s along the equivalence:

                        max_fset s := max_list (to_listfin s).                      (3)

The correctness of this transport is guaranteed by (1)–(3):

                   ∀xs s. LFS xs s −→ max_list xs = max_fset s.                     (4)

We can now readily replace any occurrence of max_fset s by max_list (to_listfin s)
and, vice versa, any occurrence of max_list xs by max_fset (to_fset xs). This pro-
cess can be extended to many other functions, such as map, filter, intersect, by
introducing new terms map_fset, filter_fset, intersect_fset and proving their re-
spectfulness theorems. Indeed, it is a very repetitive task begging for automation.

State of the Art There are various frameworks to automate the transport of terms
along equivalences. Most of them are designed for dependently typed, construc-
tive proof assistants and are based on type equivalences [8, 9, 26, 28, 29], which
play a central role in homotopy type theory. In a nutshell, type equivalences are
pairs of functions f, g that are mutually inverse (i.e. g (f x) = x and f (g y) = y)
together with a compatibility condition. They cannot solve our problem since
to_fset and to_listfin are not mutually inverse.
    Angiuli et al. [1] note and address this issue in Cubical Agda [32]. Essentially,
they ﬁrst quotient both types and then obtain a type equivalence between the
quotiented types. Their approach supports a restricted variant of quasi-partial
                   Transport via Partial Galois Connections and Equivalences       3

equivalence relations [16] but also uses univalence [33], which is unavailable in
major proof assistants like Isabelle/HOL [24] and Lean 3 [22]/Lean 4 [23].
   Another existing framework is Isabelle’s Lifting package [13], which trans-
ports terms via partial quotient types:
Definition 1. A partial quotient type (T, Abs, Rep) is given by a right-unique
and right-total relation T and two functions Abs, Rep respecting T , that is
T x y −→ Abs x = y and T (Rep y) y, for all x, y.
    In fact, (LFS, to_fset, to_listfin ) forms a partial quotient type. The Lifting
package can thus transport our list library to ﬁnite sets2 . However, the package
also has its limitations:

Limitations of the Lifting Package Consider the previous example with one
modiﬁcation: rather than transporting max_list to ﬁnite sets, we want to trans-
port it to the type of (potentially inﬁnite) sets, α set. We cannot build a partial
quotient type from α list to α set because the required relation T : α list ⇒
α set ⇒ bool is not right-total (we can only relate ﬁnite sets to lists). The Lift-
ing package is stuck. But in theory, we can (almost) repeat the previous pro-
cess: There is again a function to_set : α list ⇒ α set. We can deﬁne a relation
LS xs s := to_set xs = s. We can again prove that max_list respects LS:

           ∀xs ys. to_set xs = to_set ys −→ max_list xs = max_list ys.           (5)

There is a function to_list : α set ⇒ α list, and we obtain a partial equivalence:

         ∀xs. LS xs (to_set xs)     and      ∀s. finite s −→ LS (to_list s) s.   (6)

We can deﬁne the function max_set s := max_list (to_list s). And we again ob-
tain a correctness theorem: ∀xs s. LS xs s −→ max_list xs = max_set s. While
this process looks rather similar, there is one subtle change: the second part
of Eq. (6) only holds conditionally. As a contribution of this paper, we show
that these conditions are not showstoppers, and that we can transport via such
partial equivalences in general.
     Now one may argue that we could still use partial quotient types to transport
from lists to sets: First obtain a right-unique, right-total relation T by building a
subtype of the target type. Then transport to the new subtype and then inject to
the original type. In spirit, this is close to the approach suggested by Angiuli et
al. [1]. But the author ﬁnds this unsatisfactory from a practical and a conceptual
perspective: From a practical perspective, it introduces unnecessary subtypes to
our theory. And conceptually, the process for sets and lists was almost identical
to the one for ﬁnite sets and lists – there was no detour via subtypes.
     A second limitation of the Lifting package is that it does not support inter-
argument dependencies. For example, take the types of natural numbers, N,
2
    The Lifting package is indeed used pervasively for such purposes. At the time of
    writing, Isabelle/HOL and the Archive of Formal Proofs (www.isa-afp.org) contain
    more than 2800 invocations of the package.
4       Kevin Kappelmann

and integers, Z. We can construct a partial quotient type (ZN, to_nat, to_int),
where to_int : N ⇒ Z is the standard embedding, to_nat : Z ⇒ N is its inverse
(a partial function), and ZN i n := i = to_int n. It then seems straightforward
to transport subtraction (−Z ) : Z ⇒ Z ⇒ Z from integers to natural numbers in
the following way:
                                                             
                  n1 −N n2 := to_nat to_int n1 −Z to_int n2 .               (7)
And of course, we expect a correctness theorem:
          ∀i1 n1 i2 n2 . ZN i1 n1 ∧ ZN i2 n2 −→ ZN (i1 −Z i2 ) (n1 −N n2 ).       (8)
But alas, the theorem does not hold: we need an extra dependency between the
arguments of the respective subtractions, e.g. i1 ≥ i2 or n1 ≥ n2 . Unfortunately,
the Lifting package’s theory [13] cannot account for such dependencies, and as
such, the transport attempt for (−Z ) fails.
   In a similar way, the list index operator (!!) : α list ⇒ N ⇒ α can only be
transported to the type of arrays for indices that are in bounds (cf. Section 5,
Example 2). While solutions for dependently typed environments [1,8,9,26,28,29]
typically handle such examples by encoding the dependencies in a type, e.g.
(xs : α list) ⇒ {0, . . . , length xs − 1} ⇒ α, it is unclear how to support this in a
simply typed environment. As a contribution of this paper, we show how to
account for such dependencies with the help of dependent function relators.

Contributions and Outline We introduce a new transport framework – simply
called Transport. Our framework (1) is applicable to simple type theory, (2) is
richer than previous approaches working on partial quotient types, and (3) is
based on standard mathematical notions, particularly Galois connections and
equivalences. In Section 2, we distil the essence of what we expect when we
transport terms via equivalences. The derived set of minimal expectations mo-
tivates us to base our framework on Galois connections.
    To meet these expectations, we introduce the notion of partial Galois connec-
tions, which generalise (standard) Galois connections and partial quotient types,
in Section 3.4. We also introduce a generalisation of the well-known function re-
lator that allows for dependent relations in Section 3.2.
    Section 4 builds the technical core of the paper. We derive closure conditions
for partial Galois connections and equivalences as well as typical order proper-
ties (reﬂexivity, transitivity, etc.). Speciﬁcally, we show closure properties under
(dependent) function relators, relators for (co)datatypes, and composition. All
these results are novel and formalised in Isabelle/HOL.
    Based on our theory, we implemented a prototype for automated transports
in Isabelle/HOL and illustrate its usage in Section 5. We conclude with related
work in Section 6 and future work in Section 7.
    This article’s supplementary material3 includes the formalisation and a guide
linking all deﬁnitions, results, and examples to their formal counterpart in Is-
abelle/HOL.
3
    https://www.isa-afp.org/entries/Transport.html
                    Transport via Partial Galois Connections and Equivalences           5

         =
         ˆ (=)                   =
                                 ˆ (=)                 =
                                                       ˆ (≈)                  =
                                                                              ˆ (=)
                    f                                           Abs
     t                             t′              t                            t′
                    g

                                                                  Rep




(a) Example of a type equivalence. Left (b) Example of a partial quotient type.
and right-hand side relation are restricted The left relation can be an arbitrary par-
to be equality.                             tial equivalence relation. The right relation
                                            is restricted to be equality.

Fig. 1: Examples of equivalences used in prior work. Types are drawn solid, black.
Transport functions are drawn dashed. Each equivalence gives rise to a number
of equivalence classes on the left and right-hand side of the equivalence, which
are drawn dotted. Arrows inside equivalence classes are omitted.


2     The Essence of Transport

Existing frameworks, although beneﬁcial in practical contexts, are unapplica-
ble to our introductory examples. We hence ﬁrst want to ﬁnd the essence of
transport 4 . To ﬁnd this essence, we have to answer the following question:

What are the minimum expectations when we transport terms via equivalences?

In this section, we argue that Galois connections are the right notion to cover
this essence. Let us examine prior work to identify some guiding principles.

Type Equivalences Much recent work is based on type equivalences [1, 8, 9, 26,
28, 29]. We denote a type equivalence between α and β with mutual inverses
f : α ⇒ β and g : β ⇒ α by (α ≃ β) f g. Then, on a high level, given a set of
equivalences (αi ≃ βi ) fi gi for 1 ≤ i ≤ n and two target types α, β that may
include αi , βi , one tries to build an equivalence (α ≃ β) f g. Given a term t : α,
we can then deﬁne t′ := f t, satisfying t = g t′ . Symmetrically, for a term t′ : β,
we can deﬁne t := g t′ , satisfying f t = t′ . This situation is depicted in Fig. 1(a).
4
    To avoid confusion, our work is not about the transport map from homotopy type
    theory [31, Chapter 2]. We focus on the general task of transporting a term t to
    another term t′ along some notion of equivalence (not necessarily a type equivalence).
6         Kevin Kappelmann

Partial Quotient Types The Lifting package [13] is based on partial quotient
types (T, Abs, Rep) (see Def. 1). Every partial quotient type induces a relation
(≈) : α ⇒ α ⇒ bool that identiﬁes values in α that map to the same value in β:

                       x1 ≈ x2 := in_dom T x1 ∧ Abs x1 = Abs x2 .                              (9)

Given a set of partial quotient types (Ti : αi ⇒ βi ⇒ bool, Absi , Repi ) for
1 ≤ i ≤ n and two target types α, β that may include αi , βi , the Lifting package
tries to build a partial quotient type (T : α ⇒ β ⇒ bool, Abs, Rep). Given a
term t in the domain of (≈), we can then deﬁne t′ := Abs t, satisfying t ≈ Rep t′ .
Symmetrically, for a term t′ : β, we can deﬁne t := Rep t′ , satisfying Abs t = t′ .
This situation is depicted in Fig. 1(b).

The Essence Abstracting from these approaches, we note some commonalities:
    • As input, they take base equivalences, which are then used to build more
      complex equivalences.
    • The equivalences include a left transport function l : α ⇒ β and a right
      transport function r : β ⇒ α. They can be used to move terms from one side
      of the equivalence to a “similar” term on the other side of the equivalence.
    • Terms t : α and t′ : β that are “similar” stand in particular relations: in the
      case of type equivalences, t = r t′ and l t = t′ ; in the case of Lifting, t ≈ r t′
      and l t = t′ . More abstractly, L t (r t′ ) and R (l t) t′ for some left relation
      L : α ⇒ α ⇒ bool and right relation R : β ⇒ β ⇒ bool.5
    • More generally, L and R specify how terms ought to be related in α and β
      and determine which terms can be meaningfully transported using l and r.
    • L, R, l, r are compatible: if terms are related on one side (e.g. L t1 t2 ), their
      transports are related on the other side (e.g. R (l t1 ) (l t2 )).
Based on these commonalities, we can formulate six minimum expectations:
 (1) We want to specify how terms in α and β are related using relations L, R.
 (2) Transports should be possible by means of functions l : α ⇒ β, r : β ⇒ α.
 (3) The notion of equivalence should be closed under common relators, par-
     ticularly those for functions and (co)datatypes.
 (4) Terms related on one side have transports that are related on the other side.
 (5) Transporting a term should result in a term that is “similar” to its input.
 (6) “Similar” terms t : α and t′ : β are related with each other’s transports,
     i.e. L t (r t′ ) and R (l t) t′ .
Applying Expectation (6) to Expectation (5) then yields the requirements
 (a) L t (r (l t)),                       (b) R (l (r t′ )) t′ .
5
    The choice of L t (r t′ ), R (l t) t′ may seem arbitrary – why not pick L t (r t′ ), R t′ (l t)
    instead? In the end, the choice does not matter: While the former leads us to (mono-
    tone) Galois connections, the latter leads us to antitone Galois connections. Using
    that L, R form a Galois connection if and only if L, R−1 form an antitone Galois
    connection, every result in this paper can be transformed to its corresponding result
    on antitone Galois connections by an appropriate instantiation of the framework.
                    Transport via Partial Galois Connections and Equivalences           7

At this point, one may notice the similarity to Galois connections. A Galois
connection between two preorders (≤L ) and (≤R ) consists of two functions l
and r such that

    • l is monotone, that is x1 ≤L x2 −→ l x1 ≤R l x2 for all x1 , x2 ,
    • r is monotone, that is y1 ≤R y2 −→ r y1 ≤L r y2 for all y1 , y2 , and
    • x ≤L r (l x) and l (r y) ≤R y for all x, y.6

The ﬁnal conditions correspond to Requirements (a) and (b) above, while the
monotonicity conditions on l and r correspond to Expectation (4).

Other Motivations A second motivation to base our framework on Galois connec-
tions comes from category theory. There, an equivalence between two categories
L, R is given by two functors l : L → R and r : R → L and two natural isomor-
phisms η : IdL → r ◦ l and ǫ : l ◦ r → IdR . Applied to preorders (≤L ), (≤R ) and
monotone functions l, r, this translates to the four conditions
    (a) x ≤L r (l x),    (b) l (r y) ≤R y,    (c) r (l x) ≤L x,     (d) y ≤R l (r y).
A related categorical concept is that of an adjunction. When applied to preorders
and monotone functions, an adjunction is similar to an equivalence but is only
required to satisfy Conditions (a) and (b). In fact, while Galois connections
are not categorical equivalences, they are adjunctions. From this perspective, a
Galois connection can be seen as a weak form of an (order) equivalence.
    A ﬁnal motivation is the applicability and wide-spread use of Galois connec-
tions. They are fundamental in the closely related ﬁeld of abstract interpreta-
tion [5,7], where they are used to relate concrete to abstract domains. Moreover,
they are pervasive throughout mathematics. In the words of Saunders Mac Lane:

      The slogan is “Adjoint functors arise everywhere”.
                                 (Categories for the Working Mathematician)

    We hope our exposition convinced the reader that Galois connections are a
suitable notion to cover the essence of transport. The remaining challenges are

    • to bring the notion of Galois connections to a partial world – the relations
      L, R may only be deﬁned on a subset of α, β – and
    • to check the closure properties of our deﬁnitions under common relators.


3      Partial Galois Connections, Equivalences, and Relators

In the previous section, we singled out Galois connections as a promising can-
didate for Transport. Now we want to bring our ideas to the formal world of
proof assistants. In this section, we introduce the required background theory
for this endeavour. In the following, we ﬁx two relations L : α ⇒ α ⇒ bool,
R : β ⇒ β ⇒ bool and two functions l : α ⇒ β, r : β ⇒ α.
6
    These two conditions are equivalent to requiring x ≤L r y ←→ l x ≤R y for all x, y.
8       Kevin Kappelmann

3.1   (Order) Basics

We work in a polymorphic, simple type theory [3], as employed, for example, in
Isabelle/HOL [24]. In particular, our formalisation uses function extensionality.
We assume basic familiarity with Isabelle’s syntax. Here, we only recap the most
important concepts for our work. A complete list of deﬁnitions can be found
in Appendix A.1.
    A predicate on a type α is a function of type α ⇒ bool. A relation on α and β
is a function of type α ⇒ β ⇒ bool. Composition of two relations R, S is deﬁned
as (R ◦ S) x y := ∃z. R x z ∧ S z y. A relation R is finer than a relation S, written
R ≤ S, if ∀x y. R x y −→ S x y. It will be convenient to interpret relations as inﬁx
operators. For every relation R, we hence introduce an inﬁx operator (≤R ) := R,
that is x ≤R y ←→ R x y. We also write (≥R ) := (≤R )−1 . The field predicate on
a relation is deﬁned as in_field R x := in_dom R x ∨ in_codom R x.
    We use relativised versions of well-known order-theoretic concepts. For exam-
ple, given a predicate P , we deﬁne reflexivity on P and R as reflexive_on P R :=
∀x. P x −→ R x x. We proceed analogously for other standard order-theoretic
concepts, such as transitivity, preorders, etc. (see Appendix A.1).


3.2   Function Relators and Monotonicity

We introduce a generalisation of the well-known function relator (see e.g. [25]).
The slogan of the function relator is “related functions map related inputs to
related outputs”. Our generalisation – the dependent function relator – addition-
ally allows its target relation to depend on both inputs:
                                
                 [x y :: R] ⇛ S f g := ∀x y. R x y −→ S (f x) (g y),         (10)

where x, y may occur freely in S. The well-known (non-dependent)
                                                                    function
relator is given as a special case: (R ⇛ S) := [_ _ :: R] ⇛ S . A function is
monotone from R to S if it maps R-related inputs to S-related outputs:
                                                       
                     [x y :: R] ⇛m S f := [x y :: R] ⇛ S f f,            (11)

where x, y may occur freely in S. A monotone function relator is like a function
relator but additionally requires its members to be monotone:

      [x y :: R] ⇛⊕ S f g := [x y :: R] ⇛ S f g
                                          
                                                                          (12)
                             ∧ [x y :: R] ⇛m S f ∧ [x y :: R] ⇛m S g,

where x, y may occur freely in S. In some examples, we have to include condition-
als in our relators. For this, we deﬁne the relational if conditional rel_if B S x y :=
B −→ S x y and set the following notation:
                                                                   
                   [x y :: R | B] ⇛ S := [x y :: R] ⇛ rel_if B S ,                 (13)

where x, y may occur freely in B, S.
                  Transport via Partial Galois Connections and Equivalences        9

3.3   Galois Relator

In Expectation (6) of Section 2, we noted that “similar” terms t, t′ are related with
each other’s transports, i.e. L t (r t′ ) and R (l t) t′ . We now deﬁne this relation
formally, calling it the Galois relator :

              Galois (≤L ) (≤R ) r x y := in_codom(≤R ) y ∧ x ≤L r y            (14)

When the parameters are clear from the context, we will use the inﬁx notation
(L /) := Galois (≤L ) (≤R ) r. It is easy to show that Galois relators generalise the
transport relations of partial quotient types:

Lemma 1. For every partial quotient type (T, l, r) with induced left relation
(≤L ), we have T = Galois (≤L ) (=) r.


3.4   Partial Galois Connections and Equivalences

In their standard form, Galois connections are deﬁned on preorders (≤L ), (≤R ),
where every x : α is in the domain of (≤L ) and every y : β is in the domain of
(≤R ). But as we have seen, this is not generally the case when transporting terms.
    We hence lift the notion of Galois connections to a partial setting. We also
do not assume any order axioms on (≤L ), (≤R ) a priori but add them as needed.
In our formalisation, we moreover break the concept of Galois connections down
into smaller pieces that, to our knowledge, do not appear as such in the literature.
This allows us to obtain very precise results when deriving the closure properties
for our deﬁnitions (Section 4). But for reasons of brevity, we only state the main
deﬁnitions and results here. Details can be found in Appendix A.4.
    The (partial) Galois property is deﬁned as:
                     
       (≤L ) E (≤R ) l r :=∀x y. in_dom (≤L ) x ∧ in_codom(≤R ) y −→
                                                                                (15)
                            (x ≤L r y ←→ l x ≤R y).

If l and r are also monotone, we obtain a (partial) Galois connection:
                                           
          (≤L ) ⊣ (≤R ) l r := (≤L ) E (≤R ) l r
                                                                              (16)
                              ∧ (≤L ) ⇛m (≤R ) l ∧ (≤R ) ⇛m (≤L ) r.

We omit the qualiﬁer “partial” when referring to these deﬁnitions, unless we want
to avoid ambiguity. An example Galois connection can be found in Fig. 2(a).
    As mentioned in Section 2, Galois connections can be seen as a weak form of
an equivalence. Unfortunately, they are not in general closed under compositions
(cf. Section 4.3), where we need a stronger form of an equivalence. We can obtain
a suitable strengthening by requiring a two-sided Galois connection, which we
call a (partial) Galois equivalence:
                                                                  
            (≤L ) ≡G (≤R ) l r := (≤L ) ⊣ (≤R ) l r ∧ (≤R ) ⊣ (≤L ) r l      (17)
10      Kevin Kappelmann

      =
      ˆ (≤L )                 =
                              ˆ (≤R )             =
                                                  ˆ (≤L )                 =
                                                                          ˆ (≤R )

                  l                                           l




                  r                                           r


(a) A partial Galois connection. Note that (b) A partial Galois equivalence. The rela-
unlike in Fig. 1, the relations may not de- tions decompose into “strongly connected
compose into equivalence classes.           components”, drawn as dotted circles. Any
                                            two members in such a component are con-
                                            nected. These arrows are omitted.

Fig. 2: Examples of partial equivalences as deﬁned in (16),(17). Types are drawn
solid, black, transport functions dashed, and left and right relations dotted.


An example of a Galois equivalence can be found in Fig. 2(b). It can be shown
that Galois equivalences are, under mild conditions, equivalent to the traditional
notion of (partial) order equivalences (see Appendix A.4).
    In practice, the relations (≤L ), (≤R ) are often preorders or partial equiva-
lence relations (PERs). Given
                             some (≤L ) ≡G (≤R ) lr, we hence introduce the
notations (≤L ) ≡pre (≤R ) l r and (≤L ) ≡PER (≤R ) l r in case both relations
(≤L ), (≤R ) are preorders and PERs on their domain, respectively. It is easy to
show that Galois equivalences generalise partial quotient types:

Lemma 2. (T, l, r) is a partial
                               quotient type with induced left relation (≤L ) if
and only if (≤L ) ≡PER (=) l r.


4    Closure Properties

We now explore the closure properties of partial Galois connections and equiva-
lences, as well as standard order properties, such as reﬂexivity and transitivity.
We will derive closure conditions for the dependent function relator, relators for
(co)datatypes, and composition. In each case, we will also derive conditions under
which the Galois relator aligns with the context-dependent notion of “similarity”.
    For reasons of brevity, we only show that our framework is robust under Ga-
lois equivalences on preorders and PERs here. The results for Galois connections
(and proof sketches) can be found in Appendix B.1.
                   Transport via Partial Galois Connections and Equivalences            11

4.1   (Dependent) Function Relator

In the ﬁeld of abstract interpretation, it is well-known that Galois connections, as
usually deﬁned in the literature, are closed under the non-dependent, monotone
function relator (see for example [7]). We generalise this result to partial Galois
connections and to dependent function relators.

Remark 1. The relations and functions we use are often non-dependent in prac-
tice. The following deﬁnitions and theorems are considerably simpler in this case.
The reader hence might ﬁnd instructive to ﬁrst consult the results for this special
case in Appendix B.1.

The Setup In Section 1, we highlighted the need of inter-argument dependencies
when transporting functions. For example, we may only transport the index
operator (!!) : α list ⇒ N ⇒ α if a given index is not out of bounds for a given
list. We can realise such dependencies with the help of the dependent function
relator from Section 3.2. For this, we ﬁx the following variables:

        L1 : α1 ⇒ α1 ⇒ bool,                         l1 : α1 ⇒ α2 ,
       R1 : α2 ⇒ α2 ⇒ bool,                          r1 : α2 ⇒ α1 ,
       L2 : α1 ⇒ α1 ⇒ β1 ⇒ β1 ⇒ bool,                l2 : α2 ⇒ α1 ⇒ β1 ⇒ β2 ,
       R2 : α2 ⇒ α2 ⇒ β2 ⇒ β2 ⇒ bool,                r2 : α1 ⇒ α2 ⇒ β2 ⇒ β1 .

Each variable L2 , R2 , l2 , r2 takes parameters from α1 , α2 . These parameters en-
able the expression of inter-argument dependencies (cf. Section 5, Example 2).
We hence call L2 , R2 , l2 , r2 the dependent variables. Intuitively, we are in a situ-
ation where

(1) we are given an equivalence between (≤L1 ) and (≤R1 ), using l1 and r1 ,
(2) whenever x L1 / x′ , we are given an equivalence between (≤L2 x (r1 x′ ) ) and
    (≤R1 (l1 x) x′ ), using the transport functions l2 x′ x and r2 x x′ , and
(3) we want to construct an equivalence     for functions between              
     [x1 x2 :: (≤L1 )] ⇛⊕ (≤L2 x1 x2 ) and [x′1 x′2 :: (≤R1 )] ⇛⊕ (≤R2 x′1 x′2 ) .

To deﬁne suitable transport functions, we use the dependent function mapper :
                                      
                         [x :: f ] → g h x := g (f x) (h (f x)),                       (18)

where x may occur freely in g. We can now deﬁne the target relations and
transport functions:

     L := [x1 x2 :: (≤L1 )] ⇛⊕ (≤L2 x1 x2 ) ,     l := [x′ :: r1 ] → l2 x′ ,
                                                                         
                                                                             (19)
     R := [x′1 x′2 :: (≤R1 )] ⇛⊕ (≤R2 x′1 x′2 ) ,
                                                                       
                                                  r := [x :: l1 ] → r2 x .
                                                                                 
In particular, l f x′ = l2 x′ (r1 x′ ) f (r1 x′ ) and r g x = r2 x (l1 x) g (l1 x) .
12      Kevin Kappelmann

Closure Theorems Checking the closure of order-theoretic concepts, such as
reﬂexivity, transitivity, and symmetry, is fairly straightforward. Verifying the
closure of Galois connections and equivalences, however, is nuanced, requiring
careful alignment of the dependent variables’ parameters. These alignments re-
quire the following monotonicity conditions, which, broadly speaking, say that
(1) L2 , R2 are antimonotone in their ﬁrst and monotone in their second param-
eter, and (2) l2 , r2 are monotone in both parameters:
    (i) If x1 ≤L1 x2 ≤L1 x3 ≤L1 x4 then (≤L2 x2 x3 ) ≤ (≤L2 x1 x4 ).
   (ii) If x′1 ≤R1 x′2 ≤R1 x′3 ≤R1 x′4 then (≤R2 x′2 x′3 ) ≤ (≤R2 x′1 x′4 ).
 (iii) If x1 ≤L1 x2 L1 / x′1 ≤R1 x′2 and in_field (≤L2 x1 (r1 x′2 ) ) y then
                                                
         l2 x′1 x1 y ≤R2 (l1 x1 ) x′2 l2 x′2 x2 y .
  (iv) If x1 ≤L1 x2 L1 / x′1 ≤R1 x′2 and in_field (≤R2 (l1 x1 ) x′2 ) y ′ then
                                                    
         r2 x1 x′1 y ′ ≤L2 x1 (r1 x′2 ) r2 x2 x′2 y ′ .
We are now ready to state our main result for Galois equivalences on preorders
and PERs. The result for Galois connections (and a proof sketch) can be found
in Appendix B.1. All other results can be found in our formalisation.
Theorem 1. Let ⋆ ∈ {≡pre , ≡PER } and assume
                     
 (1) (≤L1 ) ⋆ (≤R1 ) l r,                                  
 (2) if x L1 / x′ then (≤L2 x (r1 x′ ) ) ⋆ (≤R2 (l1 x) x′ ) (l2 x′ x) (r2 x x′ ),
 (3) Monotonicity Conditions (i)–(iv).
                   
Then (≤L ) ⋆ (≤R ) l r.

“Similarity” Given the closure theorem, we can readily transport a function
f from (≤L ) to a function g in (≤R ). Due to Expectations (4) and (6), we
                                                            ⊕
also know that f L / g, that is     [x1 x2 :: (≤L1 )] ⇛ (≤L2 x1 x2 ) f (r g) and
   ′ ′              ⊕
 [x1 x2 :: (≤R1 )] ⇛ (≤R2 x′1 x′2 ) (l f ) r. But arguably, this is not quite enough:
    Remember the slogan of the function relator: “related functions map related
inputs to related outputs”. We know how to relate terms between (≤L1 ) and
(≤R1 ): we can use (L1 /). Whenever x L1 / x′ , we also know how to relate terms
between (≤L2 x (r1 x′ ) ) and (≤R2 (l1 x) x′ ): we can use
               (L2 x x′ /) := Galois (≤L2 x (r1 x′ ) ) (≤R2 (l1 x) x′ ) (r2 x x′ ).    (20)
So when we say that “f and g are similar”, we may actually desire that
                        ′                        
                        x x :: (L1 /) ⇛ (L2 x x′ /) f g.                               (21)
The following theorem answers when (L /) aligns with this deﬁnition of similarity
for preordered Galois equivalences. Preciser results can be found in Appendix B.1
and the formalisation.
Theorem 2. Assume
                        
 (1) (≤L1 ) ≡pre (≤R1 ) l1 r1 ,
                                                              
 (2) if x L1 / x′ then (≤L2 x (r1 x′ ) ) ≡pre (≤R2 (l1 x) x′ ) (l2 x′ x) (r2 x x′ ),
 (3) Monotonicity Conditions (i) and (iv),
 (4) in_dom (≤L ) f , and in_codom (≤R ) g.
                                                 
Then f L / g ←→ [x x′ :: (L1 /)] ⇛ (L2 x x′ /) f g.
                   Transport via Partial Galois Connections and Equivalences              13

4.2    (Co)datatypes

Diﬀerent proof assistants ground (co)datatypes in diﬀerent ways. For instance,
Coq and Lean introduce them axiomatically, whereas Isabelle/HOL proves their
existence using the theory of bounded natural functors [30]. As our formalisation
takes place in Isabelle/HOL, we use the latter theory. Nonetheless, the results
presented in this section are relatively straightforward and can likely be adapted
to other “reasonable” deﬁnitions of (co)datatypes.
    In this section, we derive closure properties for arbitrary natural functors.
A natural functor is a bounded natural functor without cardinality constraints.
The exact axioms can be found elsewhere [30]. For our purposes, it suﬃces to say
that natural functors are equipped with a mapper and a relator. More precisely,
for every n-ary natural functor (α1 , . . . , αn ) F , there are two functions:

   mapF : (α1 ⇒ β1 ) ⇒ · · · ⇒ (αn ⇒ βn ) ⇒ (α1 , . . . , αn ) F ⇒ (β1 , . . . , βn ) F
      relF : (α1 ⇒ β1 ⇒ bool) ⇒ · · · ⇒ (αn ⇒ βn ⇒ bool) ⇒
             (α1 , . . . , αn ) F ⇒ (β1 , . . . , βn ) F ⇒ bool

The former lifts functions on the functor’s type arguments to the functorial
structure, the latter lifts relations on the functor’s type arguments to the func-
torial structure. Using the mapper and relator, it is straightforward to deﬁne
appropriate target relations and transport functions. First we ﬁx the following
variables for 1 ≤ i ≤ n:

   Li : αi ⇒ αi ⇒ bool,      li : αi ⇒ βi ,   Ri : βi ⇒ βi ⇒ bool,       ri : βi ⇒ αi .

Then we deﬁne the new target relations and transport functions as follows:

            L := relF (≤L1 ) . . . (≤Ln ),             l := mapF l1 . . . ln ,
                                                                                      (22)
            R := relF (≤R1 ) . . . (≤Rn ),             r := mapF r1 . . . rn .

The closure properties follow without any diﬃculty:
                                                                    
Theorem 3. Let ⋆ ∈ {⊣, ≡G ,≡pre , ≡PER } and assume (≤Li ) ⋆ (≤Ri ) li ri for
1 ≤ i ≤ n. Then (≤L ) ⋆ (≤R ) l r.
    As in the previous section, we can ponder whether the relation (L /) ade-
quately captures our desired notion of “similarity”. Again, we already know how
to relate terms between (≤Li ) and (≤Ri ) for 1 ≤ i ≤ n: we can use (Li /). We
also know how to relate two functors: we can use relF . We thus may desire that
“t and t′ are similar” when relF (L1 /) . . . (Ln /) t t′ . It is easy to show that (L /)
aligns with this desire:
Theorem 4. (L /) = relF (L1 /) . . . (Ln /).
    Proof details for this section can be found in our formalisation. The formal-
isation includes tactic scripts that are applicable to functors of arbitrary arity.
Integrating them into Isabelle/HOL’s datatype package is left as future work.
14       Kevin Kappelmann

4.3    Compositions
It is well-known that Galois connections, as deﬁned in the literature, are closed
under composition in the following sense: given Galois connections between
(≤L1 ), (≤R1 ) and (≤L2 ), (≤R2 ) with (≤R1 ) = (≤L2 ), we can build a Galois
connection between (≤L1 ), (≤R2 ). This result readily generalises to our partial
setting (see Appendix B.2). However, (≤R1 ) and (≤L2 ) usually do not coincide
in our context. We need a more general result.

The Setup Our goal is to deﬁne a notion of composition that works even if (≤R1 )
and (≤L2 ) do not coincide. For this, we ﬁx the variables
     L1 : α ⇒ α ⇒ bool,      l1 : α ⇒ β, R1 : β ⇒ β ⇒ bool,          r1 : β ⇒ α,
     L2 : β ⇒ β ⇒ bool,      l2 : β ⇒ γ, R2 : γ ⇒ γ ⇒ bool,          r2 : γ ⇒ β.
Intuitively, we are in a situation where
(1) we are given an equivalence between (≤L1 ) and (≤R1 ), using l1 and r1 ,
(2) we are given an equivalence between (≤L2 ) and (≤R2 ), using l2 and r2 , and
(3) we want to construct an equivalence with transport functions l2 ◦l1 and r1 ◦r2
    between those parts of (≤L1 ) and (≤R2 ) that can be made “compatible” with
    respect to these functions. This particularly means that we can apply the
    transport functions on these parts without leaving the domains of the input
    equivalences.
The question is: how do we ﬁnd those parts and how can we make them com-
patible? The solution we propose is inspired by and generalises the approach of
Huﬀman and Kunčar [13]. We provide details and intuitions for the construc-
tions in Appendix B.2. The resulting target relations and transport functions
are deﬁned as follows (where (Ri /) := Galois (≤Ri ) (≤Li ) li ):
              L := (L1 /) ◦ (≤L2 ) ◦ (R1 /),            l := l2 ◦ l1 ,
                                                                              (23)
              R := (R2 /) ◦ (≤R1 ) ◦ (L2 /),            r := r1 ◦ r2 .

Closure Theorems Again, we only state our main result for Galois equivalences
on preorders and PERs. Preciser results can be found in Appendix B.2 (including
a proof sketch) and in our formalisation.
Theorem 5. Let ⋆ ∈ {≡pre , ≡PER } and assume
                                                                         
 (1) ∀i ∈ {1, 2}. (≤Li ) ⋆ (≤Ri ) li ri , (2) (≤R1 )◦(≤L2 ) = (≤L2 )◦(≤R1 ) .
                   
Then (≤L ) ⋆ (≤R ) l r.

“Similarity” For a ﬁnal time, we can ponder whether the relation (L /) is suﬃ-
cient to capture our desired notion of “similarity”: Again, we already know how
to relate terms between (≤Li ) and (≤Ri ) for i ∈ {1, 2}: we can use (Li /). We
also have a natural way to combine these relations, namely composition.
                                                                        We thus
may desire that “t and t′ are similar” when (L1 /) ◦ (L2 /) t t′ . The next theo-
rem answers when (L /) aligns with this desire for Galois equivalences. Preciser
results can be found in Appendix B.2 and the formalisation.
                  Transport via Partial Galois Connections and Equivalences       15

Theorem 6. Assume
                                                                            
 (1) ∀i ∈ {1, 2}. (≤Li ) ≡pre (≤Ri ) li ri , (2) (≤R1 )◦(≤L2 ) = (≤L2 )◦(≤R1 ) .
                             
Then (L /) = (L1 /) ◦ (L2 /) .


5   Application Examples

As all our results are formalised in Isabelle/HOL, we can directly use them to
manually transport terms in said environment. But that would be rather tire-
some. We thus implemented a prototype in Isabelle/ML to automate transports.

The Prototype The method trprover uses registered base equivalences, along
with the closure theorems from Section 4, to construct more complex equiva-
lences. The prototype is currently restricted to equivalences on partial equiva-
lence relations (PERs) for pragmatic reasons: their closure theorems have fewer
assumptions and are hence simpler to apply. Providing automation for weaker
equivalences is future work. The current prototype also does not build composi-
tion closures (Section 4.3) and automates only a fragment of dependent function
relators for simplicity reasons. Again, these extensions are future work.
    The prototype provides a command trp. As input, it takes a term t : α (the
term to be transported) and two optional target relations L : α ⇒ α ⇒ bool,
R : β ⇒ β ⇒ bool. This is unlike other transport frameworks [9,13,26,29], which
only take the term t : α and a target type β. This design decision is crucial
since we can neither assume a unique correspondence between types and target
relations in practice (cf. Example 3), nor can we express dependencies in types,
but we express them using dependent relators (cf. Example 2). The command        
then opens two goals. The ﬁrst one asks for an equivalence (≤L ) ≡PER (≤R ) l r,
the second one for a proof that in_dom (≤L ) t. On success, it registers a new term
t′ and a theorem that t L / t′ . It also registers a second theorem where the relator
(L /) has been rewritten to its desired form as described in Theorems 2, 4, and 6.
    The following examples are best explored interactively in our formalisation.
We deﬁne the restricted equality relation on predicates as x =P y := P x ∧ x = y
and the restricted equality relation on sets as x =S y := x ∈ S ∧ x = y.

Example 1. It is easy to transport the list and set examples from Section 1. We
just have to prove the equivalence between LFSL xs xs′ := LFS xs (to_fset xs′ )
and (=) : N fset ⇒ N fset ⇒ bool and invoke our prototype on max_list:

          lemma [per_intro]: (LFSL ≡PER (=)) to_fset to_listfin
          trp max_fset : N fset ⇒ N where t = max_list by trprover

The [per_intro] tag is used by trprover to discharge the closure theorems’ side
conditions. trp registers the theorem LFS ⇛ (=) max_list max_fset and the
deﬁnition max_fset s := max_list (to_listfin s) as a result. We can also readily
transport in the opposite direction or use sets rather than fsets if we deﬁne
16      Kevin Kappelmann

LSL xs xs′ := LS xs (to_set xs′ ):

           trp max_list′ : N list ⇒ N where t = max_fset by trprover
           lemma [per_intro]: (LSL ≡PER (=finite )) to_set to_list
           trp max_set : N set ⇒ N where t = max_list by trprover

Example 2. As noted in Section 1, transporting subtractions i1 −Z i2 from Z to
N requires a dependency i1 ≥ i2 . We model this dependency using dependent
function relators. We ﬁrst deﬁne Zpos := (=(≤)0 ) and then proceed as usual:

     lemma [per_intro]: (Zpos ≡PER (=)) to_nat to_int
     trp (−N ) : N ⇒ N ⇒ N where t = (−Z )                      
       and L = [i1 _ :: Zpos] ⇛ [i2 _ :: Zpos | i1 ≥ i2 ] ⇛ Zpos
                                                               
       and R = [n1 _ :: (=)] ⇛ [n2 _ :: (=) | n1 ≥ n2 ] ⇛ (=) by trprover

Similarly, operations on datatypes may only conditionally be transportable. For
example, we may only transport the index operator (!!) : α list ⇒ N ⇒ α to
the type of immutable arrays (α iarray) if the index is not out of bounds. In the
following, let S be an arbitrary partial equivalence relation:

     lemma [per_intro]: (ListRel S ≡PER IArrRel S) to_iarr to_list
     trp iarr_ind : α iarray ⇒ N ⇒ α where t = (!!)                   
       and L = [xs _ :: ListRel S] ⇛ [i _ :: (=) | i < length xs] ⇛ S        
       and R = [arr _ :: IArrRel S] ⇛ [i _ :: (=) | i < iarr_length arr] ⇛ S
       by trprover

Example 3. Isabelle/Set [14] is a set-theoretic environment in Isabelle/HOL. Its
type of sets is called set. Isabelle/Set provides a set-extension mechanism: As
input, it takes two sets A : set and B : set and an injection from A to B. It
then creates a new set B ′ ⊇ A together with a bijection between B and B ′
with mutual inverses l, r : set ⇒ set. This mechanism is used to enforce subset
relationships. For instance, it ﬁrst uses a construction of the integers Z : set
where N 6⊆ Z. It then uses the set-extension mechanism to create a copy Z′ ⊇ N
with inverses l, r. Doing so necessitates a manual transport of all deﬁnitions from
Z to Z′ . Using Transport, it is possible to automate this process:

           lemma [per_intro]: ((=Z ) ≡PER (=Z′ )) l r
                                                                    
           trp (+Z′ ) where t = (+Z ) and L = (=Z ) ⇛ (=Z ) ⇛ (=Z )
                                              
             and R = (=Z′ ) ⇛ (=Z′ ) ⇛ (=Z′ ) by trprover
                                                                    
           trp (−Z′ ) where t = (−Z ) and L = (=Z ) ⇛ (=Z ) ⇛ (=Z )
             and R = (=Z′ ) ⇛ (=Z′ ) ⇛ (=Z′ ) by trprover

Note that all constants (+Z ), (+Z′ ), (−Z ), (−Z′ ) are of the same type set ⇒ set ⇒
set. This stresses the point that users must be able to specify target relations
and not just target types.
                  Transport via Partial Galois Connections and Equivalences      17

6   Related Work

Transport in Proof Assistants Our work was chieﬂy inspired by Isabelle’s Lifting
package [13, 17], which transports terms via partial quotient types. All closure
theorems in this work generalise the ones in [13]. Besides this source of inspira-
tion, the theory of automated transports has seen proliﬁc work in recent years:
    Tabareau et al. [28] proved a strengthened relational parametricity result,
called univalent parametricity, for the Calculus of Inductive Constructions. Their
approach ensures that all relations are compatible with type equivalences. One
can then use univalence [33] to seamlessly transport terms between related types.
The framework is implemented using Coq’s typeclass mechanism [27].
    Tabareau et al. [29] extended their work to integrate what they call “white-
box transports”. White-box transports structurally rewrite a term t to t′ using
user-speciﬁed correspondences. In contrast, “black-box transports” transport t
without looking at its syntactic structure. For instance, given an equivalence
between unary and binary numbers (N ≃ Bin) l r, black-box transporting the
term 0 +N 0 results in l (0 +N 0). In contrast, given correspondences between the
functions (+)N , (+)Bin and constants 0, 0Bin , white-box transporting the term re-
sults in 0Bin +Bin 0Bin . These modes can also be mixed: given just the equivalence
(N ≃ Bin) l r and correspondence between (+)N , (+)Bin , we obtain (l 0) +Bin (l 0).
Isabelle’s Lifting package also supports white-box transports via the transfer
method [17]. While our work is concerned with black-box transports, our proto-
type also contains experimental support for white-box transports. This integra-
tion will be further polished in future work.
    Angiuli et al. [1] establish representation independence results in Cubical
Agda [32]. Their approach applies to a restricted variant of quasi-partial equiv-
alence relations [16]. Essentially, they quotient two types by a given correspon-
dence to obtain a type equivalence between the quotiented types.
    Dagand et al. [8,9] introduce what they call “type-theoretic partial Galois con-
nections”, which are essentially partial type equivalences on an enriched α option
type. They allow for partiality on one side of the equivalence but not the other.
Their framework is designed for eﬀective program extraction and implemented
using Coq’s typeclass mechanism.
    Ringer et al. [26] developed a Coq plugin to transport proof terms via type
equivalences for inductive types. Their theory shares similarities with [28, 29],
but it directly transforms proof terms. This way, one can remove all references to
the old datatype once the proof terms have been transported to the new target
type. This is not readily achievable using other mentioned frameworks, including
ours.
    Type equivalences enjoy the property of having total and mutually inverse
transport functions. This is not the case for partial Galois connections, which
makes the transport of proofs    harder. For example, the parametricity law for
equality T ⇛ T ⇛ (←→) (=) (=) holds only if T is left-unique and injective.
This is the case if T is described by a type equivalence but not in general by
a Galois connection. Kunčar [17] provides parametricity rules for all prominent
18     Kevin Kappelmann

logical connectives. These rules also apply to our setting and will be crucial when
we polish the integration of white-box transports in our prototype.
    The works mentioned above all transport terms via certain notions of equiv-
alences. But there are also other approaches, particularly in the ﬁeld of data re-
ﬁnement. An example is the CoqEAL framework [4], which automatically derives
parametricity results using typeclass search. Another one is Isabelle’s Autoref
framework [18], which derives relational parametricity results using white-box
transports. The core inspiration in both cases goes back to [21, 25, 34]. A com-
prehensive comparison of these frameworks can be found in [19].

Galois Connections in Computer Science Galois connections are fundamental in
the ﬁeld of abstract interpretation. Cousot and Cousot’s recent book [5] provides
an overview of their applications. The closure of Galois connections under non-
dependent function relators goes back to at least [6]. We generalised this result
to partial Galois connections and dependent function relators in Section 4.1.
Most work in abstract interpretation does not consider partially deﬁned Galois
connections and assumes partial orderings on relations. The work of Miné [20]
is an exception, allowing for partiality on one side of the connection but not
the other. Darais and Van Horn [10] formalise Galois connections constructively
and apply it to tasks in abstract interpretation. An early application of Galois
connections was by Hartmanis and Stearns [12]. Though they did not use Galois
connections, they introduced an equivalent notion of pair algebras [11]. Our
Galois relator indeed describes the pair algebra induced by a Galois connection.


7    Conclusion and Future Work

We explored existing notions of equivalences used for automatic transport. Based
on this exploration, we identiﬁed a set of minimal expectations when transport-
ing terms via equivalences. This essence led us to introduce a new class of equiv-
alences, namely partial Galois connections. Partial Galois connections generalise
(standard) Galois connections and apply to relations that are only deﬁned on
subsets of their types. We derived closure conditions for partial Galois connec-
tions and equivalences, and typical order properties under (dependent) function
relators, relators for (co)datatypes, and composition. Our framework applies to
simple type theory and – unlike prior solutions for simple type theory – can han-
dle inter-argument dependencies. We implemented a prototype in Isabelle/HOL
based on our results. The prototype needs to be further polished, but it can
already handle relevant examples that are out of scope for existing tools.

Future work As our theory subsumes the one of Isabelle’s Lifting package, one
goal is to replace the package by a more general tool. To this end, we have
to integrate our results into Isabelle’s (co)datatypes package [2], extend our
prototype to automate the construction of compositions, and polish the support
of white-box transports (cf. Section 6).
                  Transport via Partial Galois Connections and Equivalences        19

    Finally, based on our formalisation insights, we conjecture that one can adopt
our theory to constructive logics, but only a formalisation in a constructive prover
will give a deﬁnite answer.


Acknowledgements The author thanks the anonymous reviewers of this and a
previous submission for their valuable feedback and Mohammad Abdulaziz and
Tobias Nipkow for their comments on a draft of this paper.


References

 1. Angiuli, C., Cavallo, E., Mörtberg, A., Zeuner, M.: Internalizing Representation
    Independence with Univalence. Proc. ACM Program. Lang. 5(POPL) (jan 2021).
    https://doi.org/10.1145/3434293
 2. Blanchette, J.C., Hölzl, J., Lochbihler, A., Panny, L., Popescu, A., Traytel, D.:
    Truly Modular (Co)datatypes for Isabelle/HOL. In: Klein, G., Gamboa, R. (eds.)
    Interactive Theorem Proving. pp. 93–110. Springer International Publishing, Cham
    (2014). https://doi.org/10.1007/978-3-319-08970-6_7
 3. Church, A.: A Formulation of the Simple Theory of Types. The Journal of Symbolic
    Logic 5(2), 56–68 (1940). https://doi.org/10.2307/2266170
 4. Cohen, C., Dénès, M., Mörtberg, A.: Reﬁnements for Free! In: Gonthier, G., Nor-
    rish, M. (eds.) Certiﬁed Programs and Proofs. pp. 147–162. Springer International
    Publishing, Cham (2013). https://doi.org/10.1007/978-3-319-03545-1_10
 5. Cousot, P.: Principles of Abstract Interpretation. MIT Press (2021)
 6. Cousot, P., Cousot, R.: Static Determination of Dynamic Properties of Recursive
    Procedures. In: Neuhold, E. (ed.) IFIP Conf. on Formal Description of Program-
    ming Concepts, St-Andrews, N.B., CA. pp. 237–277. North-Holland (1977)
 7. Cousot,      P.,    Cousot,    R.:    Abstract     Interpretation    Frameworks.
    Journal     of   Logic    and    Computation      2(4),   511–547   (08     1992).
    https://doi.org/10.1093/logcom/2.4.511
 8. Dagand, P.E., Tabareau, N., Tanter, E.: Partial Type Equivalences for Ver-
    iﬁed Dependent Interoperability. SIGPLAN Not. 51(9), 298–310 (sep 2016).
    https://doi.org/10.1145/3022670.2951933
 9. Dagand, P.E., Tabareau, N., Tanter, E.: Foundations of Depen-
    dent Interoperability. Journal of Functional Programming 28 (2018).
    https://doi.org/10.1017/S0956796818000011
10. Darais, D., Van Horn, D.: Constructive Galois Connections. Journal of Functional
    Programming 29 (2019). https://doi.org/10.1017/S0956796819000066
11. Derderian, J.C.: Galois Connections and Pair Algebras. Canadian Journal of Math-
    ematics 21, 498–501 (1969). https://doi.org/10.4153/CJM-1969-056-x
12. Hartmanis, J., Stearns, R.: Pair Algebra and Its Application to
    Automata Theory. Information and Control 7(4), 485–507 (1964).
    https://doi.org/https://doi.org/10.1016/S0019-9958(64)90181-0
13. Huﬀman, B., Kunčar, O.: Lifting and Transfer: A Modular Design for Quotients in
    Isabelle/HOL. In: Gonthier, G., Norrish, M. (eds.) Certiﬁed Programs and Proofs -
    Third International Conference, CPP 2013, Melbourne, VIC, Australia, December
    11-13, 2013, Proceedings. Lecture Notes in Computer Science, vol. 8307, pp. 131–
    146. Springer (2013). https://doi.org/10.1007/978-3-319-03545-1_9
20      Kevin Kappelmann

14. Kappelmann,       K.,    Josh,    C.,   Krauss,     A.:    Isabelle/Set   (2023),
    https://github.com/kappelmann/Isabelle-Set
15. Kappelmann, Kevin: Transport via Partial Galois Connections and Equiv-
    alences. In: Hur, Chung-Kil (ed.) Asian Symposium on Program-
    ming Languages and Systems. pp. 225–245. Springer, Singapore (2023).
    https://doi.org/10.1007/978-981-99-8311-7_11
16. Krishnaswami, N.R., Dreyer, D.: Internalizing Relational Parametricity in the Ex-
    tensional Calculus of Constructions. In: Rocca, S.R.D. (ed.) Computer Science
    Logic 2013 (CSL 2013). Leibniz International Proceedings in Informatics (LIPIcs),
    vol. 23, pp. 432–451. Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik, Dagstuhl,
    Germany (2013). https://doi.org/10.4230/LIPIcs.CSL.2013.432
17. Kunčar, O.: Types, Abstraction and Parametric Polymorphism in Higher-Order
    Logic. Ph.D. thesis, Technische Universität München (2016)
18. Lammich, P.: Automatic Data Reﬁnement. In: Blazy, S., Paulin-
    Mohring,      C.,  Pichardie,    D.   (eds.)   Interactive   Theorem     Proving.
    pp. 84–99. Springer Berlin Heidelberg, Berlin, Heidelberg (2013).
    https://doi.org/10.1007/978-3-642-39634-2_9
19. Lammich, P., Lochbihler, A.: Automatic Reﬁnement to Eﬃcient Data Structures:
    A Comparison of Two Approaches. Journal of Automated Reasoning 63(1), 53–94
    (Jun 2019). https://doi.org/10.1007/s10817-018-9461-9
20. Miné, A.: Weakly Relational Numerical Abstract Domains. Theses, Ecole Poly-
    technique X (Dec 2004), https://pastel.archives-ouvertes.fr/tel-00136630
21. Mitchell, J.C.: Representation Independence and Data Abstraction. In: Proceed-
    ings of the 13th ACM SIGACT-SIGPLAN Symposium on Principles of Program-
    ming Languages. p. 263–276. POPL ’86, Association for Computing Machinery,
    New York, NY, USA (1986). https://doi.org/10.1145/512644.512669
22. Moura, L.d., Kong, S., Avigad, J., van Doorn, F., von Raumer, J.: The Lean
    Theorem Prover (System Description). In: Felty, A.P., Middeldorp, A. (eds.) Au-
    tomated Deduction - CADE-25. pp. 378–388. Springer International Publishing,
    Cham (2015). https://doi.org/10.1007/978-3-319-21401-6_26
23. Moura, L.d., Ullrich, S.: The Lean 4 Theorem Prover and Programming
    Language. In: Platzer, A., Sutcliﬀe, G. (eds.) Automated Deduction –
    CADE 28. pp. 625–635. Springer International Publishing, Cham (2021).
    https://doi.org/10.1007/978-3-030-79876-5_37
24. Nipkow, T., Wenzel, M., Paulson, L.C.: Isabelle/HOL: A Proof Assis-
    tant for Higher-Order Logic. Springer-Verlag, Berlin, Heidelberg (2002).
    https://doi.org/10.1007/3-540-45949-9
25. Reynolds, J.C.: Types, Abstraction and Parametric Polymorphism. In: Mason,
    R.E.A. (ed.) Information Processing 83, Proceedings of the IFIP 9th World
    Computer Congress, Paris, France, September 19-23, 1983. pp. 513–523. North-
    Holland/IFIP (1983)
26. Ringer, T., Porter, R., Yazdani, N., Leo, J., Grossman, D.: Proof Repair across
    Type Equivalences. In: Proceedings of the 42nd ACM SIGPLAN International
    Conference on Programming Language Design and Implementation. p. 112–127.
    PLDI 2021, Association for Computing Machinery, New York, NY, USA (2021).
    https://doi.org/10.1145/3453483.3454033
27. Sozeau, M., Oury, N.: First-Class Type Classes. In: Mohamed, O.A.,
    Muñoz, C., Tahar, S. (eds.) Theorem Proving in Higher Order Log-
    ics. pp. 278–293. Springer Berlin Heidelberg, Berlin, Heidelberg (2008).
    https://doi.org/10.1007/978-3-540-71067-7_23
                  Transport via Partial Galois Connections and Equivalences          21

28. Tabareau, N., Tanter, E., Sozeau, M.: Equivalences for Free: Univalent Para-
    metricity for Eﬀective Transport. Proc. ACM Program. Lang. 2(ICFP) (jul 2018).
    https://doi.org/10.1145/3236787
29. Tabareau, N., Tanter, E., Sozeau, M.: The Marriage of Univalence and Parametric-
    ity. J. ACM 68(1) (jan 2021). https://doi.org/10.1145/3429979
30. Traytel, D., Popescu, A., Blanchette, J.C.: Foundational, Compositional
    (Co)datatypes for Higher-Order Logic: Category Theory Applied to Theorem Prov-
    ing. In: 2012 27th Annual IEEE Symposium on Logic in Computer Science. pp.
    596–605 (2012). https://doi.org/10.1109/LICS.2012.75
31. Univalent Foundations Program, T.: Homotopy Type Theory: Univalent Founda-
    tions of Mathematics. https://homotopytypetheory.org/book, Institute for Ad-
    vanced Study (2013)
32. Vezzosi, A., Mörtberg, A., Abel, A.: Cubical Agda: A Dependently Typed Pro-
    gramming Language with Univalence and Higher Inductive Types. Proc. ACM
    Program. Lang. 3(ICFP) (jul 2019). https://doi.org/10.1145/3341691
33. Voevodsky, V.: The equivalence axiom and univalent models of type theory (2010).
    https://doi.org/10.48550/ARXIV.1402.5556
34. Wadler, P.: Theorems for free! In: Proceedings of the Fourth International Con-
    ference on Functional Programming Languages and Computer Architecture. p.
    347–359. FPCA ’89, Association for Computing Machinery, New York, NY, USA
    (1989). https://doi.org/10.1145/99370.99404


A     Partial Galois Connections, Equivalences, and Relators

A.1    (Order) Basics

Given types α and β, the type of functions from α to β is written α ⇒ β.
    The composition of functions is deﬁned as (f ◦ g) x := f (g x).
    A predicate on a type α is a function of type α ⇒ bool.
    The predicate mapping all inputs to True is denoted by ⊤ := λ _. True.
    A relation on α and β is a function of type α ⇒ β ⇒ bool.
    For every relation R, we introduce an inﬁx operator (≤R ) := R, that is
x ≤R y ←→ R x y.
    The inverse of a relation is deﬁned as R−1 x y := R y x.
    The composition of two relations R, S is deﬁned as (R ◦ S) x y := ∃z. R x z ∧
S z y.
    A relation R is finer than another relation S, written R ≤ S, if ∀x y. R x y −→
S x y.
    The domain, codomain, and field predicates on a relation R are deﬁned as

                     in_dom R x := ∃y. R x y
                   in_codom R y := ∃x. R x y
                     in_field R x := in_dom R x ∨ in_codom R x

   A relation R is right-total if ∀y. ∃x. R x y and right-unique if ∀x, y, y ′ . R x y ∧
R x y′ → y = y′.
22       Kevin Kappelmann

   Given a predicate P and relation R, we deﬁne reflexivity, transitivity, and
symmetry on P and R as follows:

         reflexive_on P R := ∀x. P x −→ R x x
        transitive_on P R := ∀x y z. P x ∧ P y ∧ P z ∧ R x y ∧ R y z −→ R x z
       symmetric_on P R := ∀x y. P x ∧ P y ∧ R x y −→ R y x

Preorders and partial equivalence relations (PERs) are then deﬁned in the ex-
pected way:

                     preorder_on P R := transitive_on P R ∧ reflexive_on P R
     partial_equivalence_rel_on P R := transitive_on P R ∧ symmetric_on P R

For all relativised concepts, we introduce their unrelativised analogue:

                            reflexive R := reflexive_on ⊤ R
                          transitive R :=.. transitive_on ⊤ R
                                          .
            partial_equivalence_rel R := partial_equivalence_rel_on ⊤ R

    Given a predicate P and relation R, we say that f is inflationary (sometimes
also called extensive) on P and R, written inflationary_on P R f , if ∀x. P x −→
x ≤R f x. Similarly, we say that f is deflationary on P and R, written as
deflationary_on P R f , if ∀x. P x −→ f x ≤R x. If f is inﬂationary and deﬂation-
ary on P and R, it is a relational equivalence on P and R:

     rel_equivalence_on P R f := inflationary_on P R f ∧ deflationary_on P R f.


A.2     Function Relators and Monotonicity

The dependent function relator is deﬁned as
                             
               [x y :: R] ⇛ S f g := ∀x y. R x y −→ S (f x) (g y),

where x, y may occur freely in S. The (non-dependent)
                                                       function relator is given
as a special case: (R ⇛ S) := [_ _ :: R] ⇛ S . A function is monotone from R
to S if it maps R-related inputs to S-related outputs:
                                                       
                     [x y :: R] ⇛m S f := [x y :: R] ⇛ S f f,

where x, y may occur freely in S. The non-dependent
                                                    variant is given as a special
case: (R ⇛m S) := [_ _ :: R] ⇛m S . A monotone function relator is like a
function relator but additionally requires its members to be monotone:

        [x y :: R] ⇛⊕ S f g := [x y :: R] ⇛ S f g
                                             
                                                                      
                               ∧ [x y :: R] ⇛m S f ∧ [x y :: R] ⇛m S g,
                  Transport via Partial Galois Connections and Equivalences      23

where x, y may occur freely in S. The non-dependent
                                                   variant is given as a special
case: (R ⇛⊕ S) := [_ _ :: R] ⇛⊕ S . We deﬁne the relational if conditional
and the following notation:

                         rel_if B S x y := B −→ S x y,
                                                              
                  [x y :: R | B] ⇛ S := [x y :: R] ⇛ rel_if B S ,

where in the latter two cases, x, y may occur freely in B, S.


A.3    Galois Relator

We deﬁne the dual of (L /) as (/R ) := Galois (≥R ) (≥L ) l, that is x /R y ←→
in_dom (≤L ) x ∧ l x ≤R y.
                                 
Lemma 3. Assume (≤L ) E (≤R ) l r. Then x L / y ←→ x /R y.


A.4    Partial Galois Connections and Equivalences

Typically, Galois connections are deﬁned on preorders, distinguished by the char-
acteristic property x ≤L r y ←→ l x ≤R y for all x, y. We break the concept
down into smaller pieces and lift it to a partial setting. The (partial) half Galois
property on the left is deﬁned as
                                 
                  (≤L ) h E (≤R ) l r := ∀x y. x L / y −→ l x ≤R y

and dually, the (partial) half Galois property on the right as
                                
                 (≤L ) Eh (≤R ) l r := ∀x y. x /R y −→ x ≤L r y,

Both halves combined constitute the (partial) Galois property:
                                                                
         (≤L ) E (≤R ) l r := (≤L ) h E (≤R ) l r ∧ (≤L ) Eh (≤R ) l r.

If l and r are also monotone, we obtain a (partial) Galois connection:
                                                                      
 (≤L ) ⊣ (≤R ) l r := (≤L ) ⇛m (≤R ) l ∧ (≤R ) ⇛m (≤L ) r ∧ (≤L ) E (≤R ) l r.

Note that we neither require (≤L ), (≤R ) to be transitive nor reﬂexive. An exam-
ple Galois connection can be found in Fig. 2(a).
    By requiring a two-sided Galois connection, we obtain a (partial) Galois
equivalence:
                                                                  
           (≤L ) ≡G (≤R ) l r := (≤L ) ⊣ (≤R ) l r ∧ (≤R ) ⊣ (≤L ) r l

An example of a Galois equivalence can be found in Fig. 2(b). It can be shown
that Galois equivalences are, in many circumstances, equivalent to the traditional
notion of (partial) order equivalences (see Appendix A.4).
24      Kevin Kappelmann

   Since the relations (≤L ), (≤R ) are preorders or partial equivalence relations
in many practical cases, we introduce two more deﬁnitions for convenience:
                                          
    (≤L ) ≡pre (≤R ) l r := (≤L ) ≡G (≤R ) l r
                            ∧ preorder_on (in_field (≤L )) (≤L )
                            ∧ preorder_on (in_field (≤R )) (≤R )
                                          
     (≤L ) ≡PER (≤R ) l r := (≤L ) ≡G (≤R ) l r
                              ∧ partial_equivalence_rel_on (in_field (≤L )) (≤L )
                              ∧ partial_equivalence_rel_on (in_field (≤R )) (≤R )


Order Equivalences To deﬁne the concept of an order equivalence, we ﬁrst
deﬁne the unit and counit functions:

                   unit l r := r ◦ l              counit l r := l ◦ r

When l and r are clear from the context, we will write η := unit l r and ǫ :=
counit l r. A (partial) order equivalence is then deﬁned as
                                                              
         (≤L ) ≡o (≤R ) l r := (≤L ) ⇛m (≤R ) l ∧ (≤R ) ⇛m (≤L ) r
                                ∧ rel_equivalence_on (in_field (≤L )) (≤L ) η
                                ∧ rel_equivalence_on (in_field (≤R )) (≤R ) ǫ.

In practice, we will commonly work with preorders, where the notions of Galois
equivalences and order equivalences coincide:
Lemma 4. Assume
                   
 (1) (≤L ) ≡o (≤R ) l r,       (2) transitive (≤L ),         (3) transitive (≤R ).
                   
Then (≤L ) ≡G (≤R ) l r.

Lemma 5. Assume
                     
 (1) (≤L ) ≡G (≤R ) l r,                     (2) reflexive_on (in_field (≤L )) (≤L ),
 (3) reflexive_on (in_field (≤R )) (≤R ).
                     
Then (≤L ) ≡o (≤R ) l r.


B     Closure Properties

B.1    (Dependent) Function Relator

In Section 4.1, we only stated our results for Galois equivalences on preorders
and partial equivalence relations and the dependent function relator. In this
section, we show the more general results for Galois connections for both the
(non-dependent) and dependent function relator. We also clarify the need of the
monotone function relator.
                    Transport via Partial Galois Connections and Equivalences          25

Function Relator In practice, the relations and functions we use are often non-
dependent. The deﬁnitions in (19) then simplify to the standard, non-dependent
function relator and mapper. Moreover, the closure theorems will have consid-
erably simpler assumptions. We hence ﬁnd it instructive to present the results
for this special case. Let us ﬁx the following variables:

                  L1 : α1 ⇒ α1 ⇒ bool,                    l1 : α1 ⇒ α2 ,
                  R1 : α2 ⇒ α2 ⇒ bool,                    r1 : α2 ⇒ α1 ,
                  L2 : β1 ⇒ β1 ⇒ bool,                    l 2 : β1 ⇒ β2 ,
                  R2 : β2 ⇒ β2 ⇒ bool,                    r2 : β2 ⇒ β1 .

Compared to Eq. (19), the target relations and transport functions then simplify
to
        L := (≤L1 ) ⇛⊕ (≤L2 ) ,              R := (≤R1 ) ⇛⊕ (≤R2 ) ,
                                                                   
                                                          
         l := r1 → l2 ,                      r := l1 → r2 ,

where (f → g) := ([_ :: f ] → g) is the (non-dependent) function mapper. In
other words: (f → g) h = g ◦ h ◦ f .

Lemma 6. Assume
 (1) ((≤L1 ) ⊣ (≤R1 )) l1 r1 ,              (2) reflexive_on (in_field (≤L1 )) (≤L1 ),
 (3) reflexive_on (in_field (≤R1 )) (≤R1 ), (4) ((≤L2 ) ⊣ (≤R2 )) l2 r2 ,
 (5) transitive (≤L2 ),                     (6) transitive (≤R2 ).
                    
Then (≤L ) ⊣ (≤R ) l r.

Proof. The theorem is a direct consequence of Theorem 7, but it is instructive
to consider the proof of this simpler theorem ﬁrst. We only show the case for
 (≤L ) h E (≤R ) l r. The other cases are similar. Assume
  (a) in_codom (≤R ) g,           (b) f ≤L r g,                 (c) x′1 ≤R1 x′2 .
Our goal is l f x′1 ≤R2 g x′2 . Due to monotonicity of r1 (Assumption (1)), we get
r1 x′1 ≤L1 r1 x′2 . Due to Assumption (b), we get

                       f (r1 x′1 ) ≤L2 r g (r1 x′2 ) = r2 g (ǫ1 x′2 ) .
                                                                     

                          
Since (≤L2 ) h E (≤R2 ) l2 r2 (Assumption (4)), we get

                         l2 f (r1 x′1 ) = l f x′1 ≤R2 g (ǫ1 x′2 ).7
                                       

Due to transitivity (Assumption (6)), it remains to show that g (ǫ1 x′2 ) ≤R2 g x′2 .
This follows from the ﬁrst Galois connection, reﬂexivity of (≤R1 ), monotonicity
of g, and in_codom (≤R1 ) x′2 (Assumptions (1), (2), (a), and (c)).
     Specialising Theorem 8 to the non-dependent function relator yields:
7
                                                                            
    Strictly speaking, we ﬁrst need to show that in_codom (≤R2 ) g (ǫ1 x′2 ) , but we omit
    that technical step here.
26      Kevin Kappelmann

Lemma 7. Assume
  (1) ((≤L1 ) ⊣ (≤R1 )) l1 r1 ,                  (2) reflexive_on (in_field (≤L1 )) (≤L1 ),
                          
  (3) (≤R2 ) ⇛m (≤L2 ) r2 ,                      (4) transitive (≤L2 ),
  (5) in_dom (≤L ) f ,                           (6) in_codom (≤R ) g.
                               
Then f L / g ←→ (L1 /) ⇛ (L2 /) f g.


Dependent Function Relator As in Theorem 1, the closure theorem requires
monotonicity conditions for each of the dependent variables (Assumptions (7)–
(10) below). Morally speaking, these assumptions say that (1) L2 is antimono-
tone in its ﬁrst and restricted antimonotone in its second parameter, (2) R2 is re-
stricted monotone in its ﬁrst and monotone in its second parameter, and (3) l2 , r2
are monotone in both parameters.

Theorem 7. Define η1 := unit l1 r1 and ǫ1 := counit l1 r1 . Assume
 (1) ((≤L1 ) ⊣ (≤R1 )) l1 r1 ,
 (2) reflexive_on (in_field (≤L1 )) (≤L1 ),
 (3) reflexive_on (in_field (≤R1 )) (≤R1 ),
 (4) if x L1 / x′ then ((≤L2 x (r1 x′ ) ) ⊣ (≤R2 (l1 x) x′ )) (l2 x′ x) (r2 x x′ ),
 (5) if x1 ≤L1 x2 then transitive (≤L2 x1 x2 ),
 (6) if x′1 ≤R1 x′2 then transitive (≤R2 x′1 x′2 ),
 (7) if x1 ≤L1 x2 ≤L1 x3 ≤L1 x4 ≤L1 η1 x3 then (≤L2 x2 x4 ) ≤ (≤L2 x1 x3 ),
 (8) if ǫ1 x′2 ≤R1 x′1 ≤R1 x′2 ≤R1 x′3 ≤R1 x′4 then (≤R2 x′1 x′3 ) ≤ (≤R2 x′2 x′4 ),
 (9) if x1 ≤L1 x2 L1 / x′1 ≤R1 x′2 and in_field (≤L2 x1 (r1 x′2 ) ) y then
                                              
       l2 x′1 x1 y ≤R2 (l1 x1 ) x′2 l2 x′2 x2 y ,
(10) if x1 ≤L1 x2 L1 / x′1 ≤R1 x′2 and in_field (≤R2 (l1 x1 ) x′2 ) y ′ then
                                                  
       r2 x1 x′1 y ′ ≤L2 x1 (r1 x′2 ) r2 x2 x′2 y ′ .
                      
Then (≤L ) ⊣ (≤R ) l r.

Proof. We will only prove that ((≤L ) h E (≤R )) l r. This should primarily illus-
trate how the monotonicity requirements arise as part of the proof. The rest of
the proof can be found in our formalisation. It is also instructive to ﬁrst consider
the proof for the non-dependent function relator as it uses the same core ideas
(see Lemma 6).
    A visualisation of the following proof can be found in Fig. 3. Assume
  (a) in_codom (≤R ) g,    (b) f ≤L r g,                (c) x′1 ≤R1 x′2 .
                                             
We have to show that l f x′1 ≤R2 x′1 x′2 g x′2 , which unfolds to

                        l2 x′1 (r1 x′1 ) f (r1 x′1 ) ≤R2 x′1 x′2 g x′2 .
                                                                    


First we apply reﬂexivity of (≤R1 ) to obtain x′1 ≤R1 x′1 . With monotonicity of
r1 (Assumption (1)), we get r1 x′1 ≤L1 r1 x′1 . Due to Assumption (b), we get

      f (r1 x′1 ) ≤L2 (r1 x′1 ) (r1 x′1 ) r g (r1 x′1 ) = r2 (r1 x′1 ) (ǫ1 x′1 ) g (ǫ1 x′1 ) .
                                                                                          
                           Transport via Partial Galois Connections and Equivalences                        27

                ˆ (≤L1 )
                =                            =
                                             ˆ (≤L2 (r1 x′1 ) (r1 x′1 ) )


                                     f           f (r1 x′1 )

            r1 x′1
                                     rg
                                                        r2 (r1 x′1 ) (ǫ1 x′1 ) (g (ǫ1 x′1 ))

                                                        r2 (r1 x′1 ) x′1 (g (ǫ1 x′1 ))


      r1
                                 Asm. (4)
                ˆ (≤R1 )
                =                               =
                                                ˆ (≤R2 (ǫ1 x′1 ) x′1 )                   =
                                                                                         ˆ (≤R2 x′1 x′2 )


                                                                     Asm. (8)
                                                   l f x′1                                 l f x′1
                     x′1

                                                        g(ǫ1 x′1 )
                                                                                                g x′1
                     x′2                                             Asm. (8)
                                                    g x′1
                                     g
                                                                                           g x′2



Fig. 3: Proof of ((≤L ) h E (≤R )) l r as explained in Theorem 7. Types are drawn
solid, black, transport functions dashed, relations dotted and dashed-dotted.


Now unlike in Lemma 6, we cannot directly apply Assumption (4): the param-
eters of (≤L2 (r1 x′1 ) (r1 x′1 ) ) and r2 (r1 x′1 ) (ǫ1 x′1 ) do not match up. We ﬁrst have
to use monotonicity of r2 (Assumption (10)) to obtain

      r2 (r1 x′1 ) (ǫ1 x′1 ) g (ǫ1 x′1 ) ≤L2 (r1 x′1 ) (r1 x′1 ) r2 (r1 x′1 ) x′1 g (ǫ1 x′1 ) .
                                                                                           

With transitivity (Assumption (5)), we then get

              f (r1 x′1 ) ≤L2 (r1 x′1 ) (r1 x′1 ) r2 (r1 x′1 ) x′1 g (ǫ1 x′1 ) .
                                                                             

Now we apply Assumption (4) to obtain

         l2 x′1 (r1 x′1 ) f (r1 x′1 ) = (l f x′1 ) ≤R2 (ǫ1 x′1 ) x′1 g (ǫ1 x′1 ) .8
                                                                               

With monotonicity of g and Assumption (1), one can show that

                        g (ǫ1 x′1 ) ≤R2 (ǫ1 x′1 ) x′1 (g x′1 ).
                                   

8
                                                                                  
    Again, we omit the step showing that in_codom (≤R2 (ǫ1 x′1 ) x′1 ) g (ǫ1 x′2 ) .
28       Kevin Kappelmann

Thus with transitivity (Assumption (6)), (l f x′1 ) ≤R2 (ǫ1 x′1 ) x′1 (g x′1 ). Using mono-
tonicity of R2 (Assumption (8)), we can adapt the parameters of R2 and obtain
(l f x′1 ) ≤R2 x′1 x′2 (g x′1 ). Finally, we obtain (g x′1 ) ≤R2 x′1 x′2 (g x′2 ) from x′1 ≤R1 x′2
and monotonicity of g. We can conclude using transitivity.

     We can also prove a generalisation of Theorem 2:

Theorem 8. Assume
 (1) ((≤L1 ) ⊣ (≤R1 )) l1 r1 ,
 (2) reflexive_on (in_field (≤L1 )) (≤L1 ),                 
 (3) if x L1 / x′ then (≤R2 (l1 x) x′ ) ⇛m (≤L2 x (r1 x′ ) ) (r2 x x′ ),
 (4) if x1 ≤L1 x2 then transitive (≤L2 x1 x2 ),
 (5) if x1 ≤L1 x2 ≤L1 x3 then (≤L2 x1 x2 ) ≤ (≤L2 x1 x3 ),
 (6) if x1 ≤L1 x2 ≤L1 x3 ≤L1 η1 x2 then (≤L2 x1 x3 ) ≤ (≤L2 x1 x2 ),
 (7) if x1 ≤L1 x2 L1 / x′1 ≤R1 x′2 and in_field (≤R2 (l1 x1 ) x′2 ) y ′ then
                                                  
       r2 x1 x′1 y ′ ≤L2 x1 (r1 x′2 ) r2 x2 x′2 y ′ ,
 (8) in_dom (≤L ) f , and in_codom (≤R ) g.
                                                      
Then f L / g ←→ [x x′ :: (L1 /)] ⇛ (L2 x x′ /) f g.


Regarding Monotonicity Finally, we want to mention a subtlety: while work
in abstract interpretation points out the necessity to use monotone function
relators, for example [7], related work dealing with the concept of transports in
proof assistants does not talk about any such monotonicity restriction [1, 8, 9,
13,26,28,29]. The reason is not that the monotonicity restriction is unnecessary,
but rather that the function relators in latter works are monotone by default.
This can be made precise with the following lemma:

Lemma 8. Assume
 (1) reflexive_on (in_field (≤L1 )) (≤L1 ),
 (2) if x1 ≤L1 x2 then (≤L2 x2 x2 ) ≤ (≤L2 x1 x2 ),
 (3) if x1 ≤L1 x2 then (≤L2 x1 x1 ) ≤ (≤L2 x1 x2 ),
 (4) if x1 ≤L1 x2 then partial_equivalence_rel (≤L2 x1 x2 ).
                                                                        
Then [x1 x2 :: (≤L1 )] ⇛⊕ (≤L2 x1 x2 ) = [x1 x2 :: (≤L1 )] ⇛ (≤L2 x1 x2 ) .

     Again, we can specialise this to the non-dependent function relator:

Lemma 9. Assume
 (1) reflexive_on (in_field (≤L1 )) (≤L1 ),
 (2) partial_equivalence_rel (≤L2 ).
                                           
Then (≤L1 ) ⇛⊕ (≤L2 ) = (≤L1 ) ⇛ (≤L2 ) .

   It is easy to check that these assumptions are met by type equivalences and
partial quotient types.
                    Transport via Partial Galois Connections and Equivalences           29

B.2     Compositions

In this section, we provide some intuition for the constructions from Section 4.3,
provide preciser results, and compare the construction with Isabelle’s Lifting
package.


Closure for Coinciding Relations

Theorem 9. Let ⋆ ∈ {⊣, ≡G , ≡o , ≡pre , ≡PER } and assume
                                               
 (1) (≤L1 )⋆(≤R1 ) l1 r1 , (2) (≤R1 )⋆(≤R2 ) l2 r2 , (3) (≤R1 ) = (≤L2 ).
                    
Then (≤L1 ) ⋆ (≤R2 ) (l2 ◦ l1 ) (r1 ◦ r2 ).

Proof. The proof can be found in the formalisation9 .


Construction Idea As mentioned in Section 4.3, our construction is inspired
by Huﬀman and and Kunčar’s construction in [13]. Unfortunately, they do not
provide any intuition about their constructions, nor does Kunčar [17] in his
thesis. We try our best to ﬁll this gap: In the following, we call (≤L1 ) the leftmost
relation, (≤R1 ), (≤L2 ) the middle relations, and (≤R2 ) the rightmost relation. We
will explain the deﬁnition of (≤L ). The case for (≤R ) is symmetric.
    Fix some x : α of the leftmost type. We want to (a) make sure that apply-
ing l = l2 ◦ l1 on x does not leave the domain/codomain of our equivalences,
and (b) ﬁnd all elements x′ : α that are greater or equal than x while doing so.
We make a ﬁrst approximation to satisfy these conditions using three “chase”
steps:
    (1) check whether in_dom (≤L1 ) x and ﬁnd some y such that l1 x ≤R1 y,
    (2) ﬁnd some y ′ such that y ≤L2 y ′ , and
    (3) check whether in_dom (≤R1 ) y ′ and ﬁnd some x′ such that r1 y ′ ≤L1 x′ .
These steps are not enough: we may have l1 x ≤R1 y ≤L2 y ′ but not necessarily
l1 x ≤L2 y ≤L2 y ′ , as required for Property (a) and Step (3). But if we further
require that (≤R1 ) and (≤L2 ) commute, that is (≤R1 ) ◦ (≤L2 ) = (≤L2 ) ◦
(≤R1 ) , the steps become suﬃcient. Finally note that

  • x L1 / y ←→ in_dom (≤L1 ) x ∧ l1 x ≤R1 y whenever ((≤L1 ) E (≤R1 )) l1 r1 ,
    and
  • y ′ R1 / x′ ←→ in_dom (≤R1 ) y ′ ∧ r1 y ′ ≤L1 x′ whenever ((≤R1 ) E (≤L1 )) r1 l1
                                                                 
due to Lemma 3. For Galois equivalences (≤L1 ) ≡G (≤R1 ) l1 r1 , it is thus
suﬃcient to search for a chain x L1 / y ≤L2 y ′ R1 / x′ , which is equivalent to
 (L1 /) ◦ (≤L2 ) ◦ (R1 /) x x′ . Hence the deﬁnition of (≤L ).
9
    We actually prove a more general result where the right and left relations of the input
    Galois connections need not be equal but only need to “agree whenever required”.
    But we suspect that such an agreement rarely holds in practice and hence omit it.
30      Kevin Kappelmann
                                                     
Remark 2. A Galois connection (≤L1 ) ⊣ (≤R1 ) l1 r1 would not be suﬃcient due
to Step (3): We are given some y ′ : β and x′ : α and need to check whether y ′
is “smaller” than x′ . We may check this by either transporting y ′ to the left (i.e.
r1 y ′ ≤L1 x′ ) or x′ to the right (i.e. y ′ ≤R1 l1 x′ ). However, right adjoints only
preserve inﬁma while left adjoints only preserve suprema. Hence the need for
 (≤R1 ) ⊣ (≤L1 ) r1 l1 .
    Now it is not to be excluded that there is an alternative way that avoids the
need of a Galois equivalence. But at least thus far, it has eluded the author.

Remark 3. As noted, the relations (≤L ) and (≤R ) may not be equal to (≤L1 )
and (≤R2 ), but, in some sense, describe those parts that were made “compatible”
with respect to l and r. While our formalisation includes conditions under which
we can obtain an equality, they do not apply to all practical examples. It is indeed
a challenge on its own to ﬁnd particular conditions under which the relations
(≤L ) and (≤R ) may be rewritten to a simpler form. In this direction, the thesis
of Kunčar [17] includes ideas applicable to total quotients and partial subtypes.


Closure and Similarity Theorems The next result generalises Theorem 5.
Theorem 10. Assume
                     
 (1) (≤Li ) ≡G (≤Ri ) li ri for i ∈ {1, 2}, (2) preorder_on (in_field (≤R1 )) (≤R1 ),
                                                                                
 (3) preorder_on (in_field (≤L2 )) (≤L2 ), (4) (≤R1 )◦(≤L2 ) = (≤L2 )◦(≤R1 ) .
                   
Then (≤L ) ⊣ (≤R ) l r.

Proof. We will only show that ((≤L ) h E (≤R )) l r to illustrate the usage of the
compatibility condition (Assumption (4)). The rest of the proof can be found in
our formalisation. A visualisation of the following proof can be found in Fig. 4.
   Assume that
  (a) in_codom (≤R ) z,                      (b) x ≤L r z.
                                                                    
We have to show that l x ≤R z, which unfolds to (R2 /)◦(≤R1 )◦(L2 /) (l2 (l1 x)) z.
From Assumption (b), we obtain y, y ′ such that

                     l1 x ≤R1 y ≤L2 y ′ ≤R1 l1 (r z) = ǫ1 (r2 z),

where ǫ1 := counit l1 r1 . We wish to obtain ǫ1 (r2 z) ≤R1 r2 z; this only holds if
in_codom (≤R1 )(r2 z), however. For this purpose, take Assumptions (1) and (a).
We obtain w, w′ such that w ≤R1 w′ ≤L2 r2 z. Thus, by Assumption (4), there
is w′′ such that w ≤L2 w′′ ≤R1 r2 z. Hence, in_codom (≤R1 )(r2 z).
    Then by transitivity, we get y ≤L2 y ′ ≤R1 r2 z. Thus, by Assumption (4),
there is y ′′ such that y ≤R1 y ′′ ≤L2 r2 z. From y ′′ ≤L2 r2 z and Assumption (a),
we get y ′′ L2 / z. From l1 x ≤R1 y ≤R1 y ′′ and transitivity, we get l1 x ≤R1 y ′′ . It
remains to show that l x R2 / l1 x, that is l x ≤R2 l x and in_codom (≤L2 ) (l1 x).
    From l1 x ≤R1 y ≤L2 y ′ and Assumption (4), we obtain u such that l1 x ≤L2
u ≤R1 y ′ . Thus, in_dom (≤L2 ) (l1 x). Then by reﬂexivity (Assumption (3)),
l1 x ≤L2 l1 x. Finally, l x ≤R2 l x by monotonicity of l2 (Assumption (1)).
                           Transport via Partial Galois Connections and Equivalences                                    31

                           =
                           ˆ (≤R1 )                                                   =
                                                                                      ˆ (≤R1 )
  =
  ˆ (≤L1 )                 =
                           ˆ (≤L2 )             =
                                                ˆ (≤R2 )     =
                                                             ˆ (≤L1 )                 =
                                                                                      ˆ (≤L2 )                  =
                                                                                                                ˆ (≤R2 )

    x        l1     l1 x                                      x         l1     l1 x


                   y                 w                                        y                 w

                  y′                 w′                                      y′                 w′
                                                                                                     w′′
                                                   z                                                               z
   rz             ǫ1 (r2 z) r2 z           r2                 rz             ǫ1 (r2 z) r2 z           r2


    (a) The initial setup of the proof.                    (b) Applying the compatibility condition
                                                           to obtain w′′ .

                           =
                           ˆ (≤R1 )                                                   =
                                                                                      ˆ (≤R1 )
  =
  ˆ (≤L1 )                 =
                           ˆ (≤L2 )             =
                                                ˆ (≤R2 )     =
                                                             ˆ (≤L1 )                 =
                                                                                      ˆ (≤L2 )                  =
                                                                                                                ˆ (≤R2 )

    x        l1     l1 x                                      x         l1     l1 x                        l2
                                                                                                                   lx

                   y                 w                                        y                 w
                                                                         u
                                ′′                                                         ′′
                            y                                                          y
                  y′                 w′                                      y′                 w′
                                          w′′                                                        w′′
                                                   z                                                               z
   rz             ǫ1 (r2 z) r2 z           r2                 rz             ǫ1 (r2 z) r2 z           r2


(c) Applying the compatibility condition (d) Applying the compatibility condition
to obtain y ′′ .                         to show in_dom (≤L2 ) (l1 x). Then apply
                                         reﬂexivity of (≤L2 ) and monotonicity of l2
                                         to ﬁnish.

Fig. 4: Proof of ((≤L ) h E (≤R )) l r as explained in Theorem 10. Types are drawn
solid, black, transport functions dashed, relations dotted and dashed-dotted.


   We can also prove a generalisation of Theorem 6:
Theorem 11. Assume
                                                              
 (1) (≤R1 ) ⇛m (≤L1 ) r1 ,                (2) (≤L1 ) E (≤R1 ) l1 r1 ,
                      
 (3) (≤R1 ) h E (≤L1 ) r1 l1 ,           (4) preorder_on (in_field
                                                                    (≤R1 )) (≤R1 ),
 (5) (≤L2 ) ⇛m (≤R2 ) l2 ,                (6) (≤R2 ) h E (≤L2 ) r2 l2 ,        
 (7) reflexive_on (in_dom (≤L2 )) (≤L2 ), (8) (≤R1 )◦(≤L2 ) = (≤L2 )◦(≤R1 ) .
                                
Then (L /) = (L1 /) ◦ (L2 /)) .

Comparison To Isabelle’s Lifting Package As mentioned, our deﬁnitions
are inspired by [13]: Let (T1 , l1 , r1 ) and (T2 , l2 , r2 ) be two partial quotient types
with induced left relations (≤L1 ) and (≤L2 ). Huﬀman and and Kunčar then
32     Kevin Kappelmann

construct the composition (T1 ◦ T2 , l2 ◦ l1 , r1 ◦ r2 ). Moreover, they prove that
the induced left relation (≤L ) of this composed partial quotient type satisﬁes
(≤L ) = T1 ◦ (≤L2 ) ◦ T1−1 . This insight sparked the idea of our deﬁnitions.
   Indeed, we can show that our deﬁnitions faithfully generalise their work.
Just as Lemma 1 shows that T1 = Galois (≤L1 ) (=) r1 , we can show that T1−1 =
Galois (=) (≤L1 ) l1 . It then follows that

      T1 ◦ (≤L2 ) ◦ T1−1 = Galois (≤L1 ) (=) r1 ◦ (≤L2 ) ◦ Galois (=) (≤L1 ) l1 .
                                                                              


Moreover, it is easy to show that the compatibility condition is vacuously true
for partial quotient types.
