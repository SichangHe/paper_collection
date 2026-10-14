                                                              Strong-Separation Logic

                                                                  Jens Pagel and Florian Zuleger

                                                                        TU Wien, Austria
                                                              pagel@forsyte.at, zuleger@forsyte.at
arXiv:2001.06235v2 [cs.LO] 11 Mar 2021




                                               Abstract. Most automated verifiers for separation logic are based on
                                               the symbolic-heap fragment, which disallows both the magic-wand opera-
                                               tor and the application of classical Boolean operators to spatial formulas.
                                               This is not surprising, as support for the magic wand quickly leads to un-
                                               decidability, especially when combined with inductive predicates for rea-
                                               soning about data structures. To circumvent these undecidability results,
                                               we propose assigning a more restrictive semantics to the separating con-
                                               junction. We argue that the resulting logic, strong-separation logic, can
                                               be used for symbolic execution and abductive reasoning just like “stan-
                                               dard” separation logic, while remaining decidable even in the presence
                                               of both the magic wand and the list-segment predicate—a combination
                                               of features that leads to undecidability for the standard semantics.


                                         1   Introduction
                                         Separation logic [40] is one of the most successful formalisms for the analysis
                                         and verification of programs making use of dynamic resources such as heap
                                         memory and access permissions [7,30,10,5,17,24,9]. At the heart of the success
                                         of separation logic (SL) is the separating conjunction, ∗, which supports concise
                                         statements about the disjointness of resources. In this article, we will focus on
                                         separation logic for describing the heap in single-threaded heap-manipulating
                                         programs. In this setting, the formula ϕ ∗ ψ can be read as “the heap can be
                                         split into two disjoint parts, such that ϕ holds for one part and ψ for the other.”
                                             Our article starts from the following observation: The standard semantics of
                                         ∗ allows splitting a heap into two arbitrary sub-heaps. The magic-wand operator
                                         −∗, which is the adjoint of ∗, then allows adding arbitrary heaps. This arbitrary
                                         splitting and adding of heaps makes reasoning about SL formulas difficult, and
                                         quickly renders separation logic undecidable when inductive predicates for data
                                         structures are considered. For example, Demri et al. recently showed that adding
                                         only the singly-linked list-segment predicate to propositional separation logic
                                         (i.e., with ∗, −∗ and classical connectives ∧, ∨, ¬) leads to undecidability [16].
                                             Most SL specifications used in automated verification do not, however, make
                                         use of arbitrary heap compositions. For example, the widely used symbolic-heap
                                         fragments of separation logic considered, e.g., in [3,4,13,21,22], have the following
                                         property: a symbolic heap satisfies a separating conjunction, if and only if one
                                         can split the model at locations that are the values of some program variables.
                                             Motivated by this observation, we propose a more restrictive separating con-
                                         junction that allows splitting the heap only at location that are the values of some
2

    x        y           nil   =   x         y   +   y       nil

(a) A model of ls(x, y) ∗ ls(y, nil) in both the standard semantics and our semantics.
    x        nil     =   x             nil

                         +


                   (b) A model of ls(x, nil) ∗ t in the standard semantics.

Fig. 1: Two models and their decomposition into disjoint submodels. Dangling
arrows represent dangling pointers.

program variables. We call the resulting logic strong-separation logic. Strong-
separation logic (SSL) shares many properties with standard separation-logic
semantics; for example, the models of our logic form a separation algebra. Be-
cause the frame rule and other standard SL inference rules continue to hold for
SSL, SSL is suitable for deductive Hoare-style verification à la [23,40], symbolic
execution [4], as well as abductive reasoning [10,9]. At the same time, SSL
has much better computational properties than standard SL—especially when
formulas contain expressive features such as the magic wand, −∗, or negation.
   We now give a more detailed introduction to the contributions of this article.

The standard semantics of the separating conjunction. To be able to justify our
changed semantics of ∗, we need to introduce a bit of terminology. As standard
in separation logic, we interpret SL formulas over stack–heap pairs. A stack is
a mapping of the program variables to memory locations. A heap is a finite
partial function between memory locations; if a memory location l is mapped to
location l0 , we say the heap contains a pointer from l to l0 . A memory location
l is allocated if there is a pointer of the heap from l to some location l0 . We call
a location dangling if it is the target of a pointer but not allocated; a pointer is
dangling if its target location is dangling.
     Dangling pointers arise naturally in compositional specifications, i.e., in for-
mulas that employ the separating conjunction ∗: In the standard semantics of
separation logic, a stack–heap pair (s, h) satisfies a formula ϕ ∗ ψ, if it is possible
to split the heap h into two disjoint parts h1 and h2 such that (s, h1 ) satisfies
ϕ and (s, h2 ) satisfies ψ. Here, disjoint means that the allocated locations of h1
and h2 are disjoint; however, the targets of the pointers of h1 and h2 do not have
to be disjoint.
     We illustrate this in Fig. 1a, where we show a graphical representation of
a stack–heap pair (s, h) that satisfies the formula ls(x, y) ∗ ls(y, nil). Here, ls
denotes the list-segment predicate. As shown in Fig. 1a, h can be split into two
disjoint parts h1 and h2 such that (s, h1 ) is a model of ls(x, y) and (s, h2 ) is a
model of ls(y, nil). Now, h1 has a dangling pointer with target s(y) (displayed
with an orange background), while no pointer is dangling in the heap h.

In what sense is the standard semantics too permissive? The standard semantics
of ∗ allows splitting a heap into two arbitrary sub-heaps, which may result in the
introduction of arbitrary dangling pointers into the sub-heaps. We note, however,
                                                                                   3

that the introduction of dangling pointers is not arbitrary when splitting the
models of ls(x, y) ∗ ls(y, nil); there is only one way of splitting the models of
this formula, namely at the location of program variable y. The formula ls(x, y)∗
ls(y, nil) belongs to a certain variant of the symbolic-heap fragment of separation
logic, and all formulas of this fragment have the property that their models can
only be split at locations that are the values of some variables.
    Standard SL semantics also allows the introduction of dangling pointers with-
out the use of variables. Fig. 1b shows a model of ls(x, nil) ∗ t—assuming the
standard semantics. Here, the formula t (for true) stands for any arbitrary heap.
In particular, this includes heaps with arbitrary dangling pointers into the list
segment ls(x, nil). This power of introducing arbitrary dangling pointers is what
is used by Demri et al. for their undecidability proof of propositional separation
logic with the singly-linked list-segment predicate [16].
Strong-separation logic. In this article, we want to explicitly disallow the implicit
sharing of dangling locations when composing heaps. We propose to parameterize
the separating conjunction by the stack and exclusively allow the union of heaps
that only share locations that are pointed to by the stack. For example, the
model in Fig. 1b is not a model of ls(x, nil) ∗ t in our semantics because of the
dangling pointers in the sub-heap that satisfies t. Strong-separation logic (SSL)
is the logic resulting from this restricted definition of the separating conjunction.
Why should I care? We argue that SSL is a promising proposal for automated
program verification:
    1) We show that the memory models of strong-separation logic form a sepa-
ration algebra [11], which guarantees the soundness of the standard frame rule of
SL [40]. Consequently, SSL can be potentially be used instead of standard SL in
a wide variety of (semi-)automated analyzers and verifiers, including Hoare-style
verification [40], symbolic execution [4], and bi-abductive shape analysis [10].
    2) To date, most automated reasoners for separation logic have been de-
veloped for symbolic-heap separation logic [3,4,10,21,22,26,32,27]. In these frag-
ments of separation logic, assertions about the heap can exclusively be combined
via ∗; neither the magic wand −∗ nor classical Boolean connectives are permitted.
We show that the strong semantics agrees with the standard semantics on sym-
bolic heaps. For this reason, symbolic-heap SL specifications remain unchanged
when switching to strong-separation logic.
    3) We establish that the satisfiability and entailment problem for full propo-
sitional separation logic with the singly-linked list-segment predicate is decidable
in our semantics (in PSpace)—in stark contrast to the aforementioned unde-
cidability result obtained by Demri et al. [16] assuming the standard semantics.
    4) The standard Hoare-style approach to verification requires discharging
verification conditions (VCs), which amounts to proving for loop-free pieces of
code that a pre-condition implies some post-condition. Discharging VCs can be
automated by calculi that symbolically execute the pre-condition forward resp.
the post-condition backward, and then using an entailment checker for proving
the implication. For SL, symbolic execution calculi can be formulated using
the magic wand resp. the septraction operator. However, these operators have
4

proven to be difficult for automated procedures: “VC-generators do not work
especially well with separation logic, as they introduce magic-wand −∗ operators
which are difficult to eliminate.” [2, p. 131] In contrast, we demonstrate that
SSL can overcome the described difficulties. We formulate a forward symbolic
execution calculus for a simple heap-manipulating programming language using
SSL. In conjunction with our entailment checker, see 3), our calculus gives rise
to a fully-automated procedure for discharging VCs of loop-free code segments.
    5) Computing solutions to the abduction problem is an integral building block
of Facebook’s Infer analyzer [9], required for a scalable and fully-automated
shape analysis [10]. We show how to compute explicit representations of op-
timal, i.e., logically weakest and spatially minimal, solutions to the abduction
problem for the separation logic considered in this paper. The result is of theo-
retical interest, as explicit representations for optimal solutions to the abduction
problem are hard to obtain [10,19].

Contributions. Our main contributions are as follows:

 1. We propose and motivate strong-separation logic (SSL), a new semantics for
    separation logic.
 2. We present a PSpace decision procedure for strong-separation logic with
    points-to assertions, the list-segment predicate ls(x, y), and spatial and clas-
    sical operators, i.e., ∗, −∗, ∧, ∨, ¬—a logic that is undecidable when assuming
    the standard semantics [16].
 3. We present symbolic execution rules for SSL, which allow us to discharge
    verification conditions fully automatically.
 4. We show how to compute explicit representations of optimal solutions to the
    abduction problem for the SSL considered in (2).

We strongly believe that these results motivate further research on SSL (e.g.,
going beyond the singly-linked list-segment predicate, implementing our decision
procedure and integrating it into fully-automated analyzers).

Related work. The undecidability of separation logic was established already
in [12]. Since then, decision problems for a large number of fragments and
variants of separation logic have been studied. Most of this work has been on
symbolic-heap separation logic or other variants of the logic that neither sup-
port the magic wand nor the use of negation below the ∗ operator. While entail-
ment in the symbolic-heap fragment with inductive definitions is undecidable in
general [1], there are decision procedures for variants with built-in lists and/or
trees [3,13,34,35,36], support for defining variants of linear structures [20] or tree
structures [42,22] or graphs of bounded tree width [21,26]. The expressive heap
logics Strand [29] and Dryad [37] also have decidable fragments, as have some
other separation logics that allow combining shape and data constraints. Besides
the already mentioned work [35,36], these include [28,25].
    Among the aforementioned works, the graph-based decision procedures of [13]
and [25] are most closely related to our approach. Note however, that neither
                                                                                      5

of these works supports reasoning about magic wands or negation below the
separating conjunction.
     In contrast to symbolic-heap SL, separation logics with the magic wand
quickly become undecidable. Propositional separation logic with the magic wand,
but without inductive data structures, was shown to be decidable in PSpace
in the early days of SL research [12]. Support for this fragment was added to
CVC4 a few years ago [39]. Some tools have “lightweight” support for the magic
wand involving heuristics and user annotations, in part motivated by the lack of
decision procedures [6,41].
     There is a significant body of work studying first-order SL with the magic
wand and unary points-to assertions, but without a list predicate. This logic
was first shown to be undecidable in [8]; a result that has since been refined,
showing e.g. that while satisfiability is still in PSpace if we allow one quan-
tified variable [15], two variables already lead to undecidability, even without
the separating conjunction [14]. Echenim et al. [18] have recently addressed the
satisfiability problem of SL with ∃∗ ∀∗ quantifier prefix, separating conjunction,
magic wand, and full Boolean closure, but no inductive definitions. The logic
was shown to be undecidable in general (contradicting an earlier claim [38]), but
decidable in PSpace under certain restrictions.

Outline. In Section 2, we introduce two semantics of propositional separation
logic, the standard semantics and our new strong-separation semantics. We show
the decidability of the satisfiability and entailment problems of SSL with lists in
Section 3. We present symbolic execution rules for SSL in Section 4. We show
how to compute explicit representations of optimal solutions to the abduction
problem in Section 5. We conclude in Section 6. All missing proofs are given in
the extended version [33] for space reasons.


2     Strong- and Weak-Separation Logic

2.1   Preliminaries

We denote by |X| the cardinality of the set X. Let f be a (partial) function. Then,
dom(f ) and img(f ) denote the domain and image of f , respectively. We write
|f | := |dom(f )| and f (x) = ⊥ for x 6∈ dom(f ). We frequently use set notation
to define and reason about partial functions: f := {x1 7→ y1 , . . . , xk 7→ yk } is the
partial function that maps xi to yi , 1 ≤ i ≤ k, and is undefined on all other
values; f −1 (b) is the set of all elements a with f (a) = b; we write f ∪ g resp.
f ∩ g for the union resp. intersection of partial functions f and g, provided that
f (a) = g(a) for all a ∈ dom(f ) ∩ dom(g); similarly, f ⊆ g holds if dom(f ) ⊆
dom(g). Given a partial function f , we denote by f [x/v] the updated partial
function in which x maps to v, i.e.,
                                        (
                                          v,    if y = x,
                           f [x/v](y) =
                                          f (y) otherwise,
6


                       τ ::= emp | x 7→ y | ls(x, y) | x = y | x 6= y
                       ϕ ::= τ | ϕ ∗ ϕ | ϕ−~ϕ | ϕ ∧ ϕ | ϕ ∨ ϕ | ¬ϕ

            Fig. 2: The syntax of separation logic with list segments.

(s, h) |= emp      iff dom(h) = ∅
(s, h) |= x = y iff dom(h) = ∅ and s(x) = s(y)
(s, h) |= x 6= y iff dom(h) = ∅ and s(x) 6= s(y)
(s, h) |= x 7→ y iff h = {s(x) 7→ s(y)}
(s, h) |= ls(x, y) iff dom(h) = ∅ and s(x) = s(y) or there exist n ≥ 1, `0 , . . . , `n with
                        h = {`0 7→ `1 , . . . , `n−1 7→ `n } , s(x) = `0 and s(y) = `n
(s, h) |= ϕ1 ∧ ϕ2 iff (s, h) |= ϕ1 and (s, h) |= ϕ2
(s, h) |= ¬ϕ       iff (s, h) 6|= ϕ
        wk                                                                 wk               wk
(s, h) |= ϕ1 ∗ ϕ2 iff there exist h1 , h2 with h = h1 + h2 , (s, h1 ) |= ϕ1 , and (s, h2 ) |= ϕ2
        wk                                          wk                                 wk
(s, h) |= ϕ1 −~ϕ2 iff exist h1 , with (s, h1 ) |= ϕ1 , h + h1 6= ⊥ and (s, h + h1 ) |= ϕ2
        st                                                                   st               st
(s, h) |= ϕ1 ∗ ϕ2 iff there exists h1 , h2 with h = h1 ]s h2 , (s, h1 ) |= ϕ1 , and (s, h2 ) |= ϕ2
        st                                         st                                   st
(s, h) |= ϕ1 −~ϕ2 iff exists h1 with (s, h1 ) |= ϕ1 , h ]s h1 6= ⊥ and (s, h ]s h1 ) |= ϕ2
                                                                        wk
Fig. 3: The standard, “weak” semantics of separation logic, |=, and the “strong”
            st                                                   wk     st
semantics, |=. We write |= when there is no difference between |= and |=.

where we use v = ⊥ to express that the updated function f [x/v] is undefined
for x.
    Sets and ordered sequences are denoted in boldface, e.g., x. To list the ele-
ments of a sequence, we write hx1 , . . . , xk i.
    We assume a linearly-ordered infinite set of variables Var with nil ∈ Var and
denote by max(v) the maximal variable among a set of variables v according
to this order. In Fig. 2, we define the syntax of the separation-logic fragment
we study in this article. The atomic formulas of our logic are the empty-heap
predicate emp, points-to assertions x 7→ y, the list-segment predicate ls(x, y),
equalities x = y and disequalities x 6= y 1 ; in all these cases, x, y ∈ Var. For-
mulas are closed under the classical Boolean operators ∧, ∨, ¬ as well as under
the separating conjunction ∗ and the existential magic wand, also called sep-
traction, −~ (see e.g. [8]). We collect the set of all SL formulas in SL. We also
consider derived operators and formulas, in particular the separating implication
(or magic wand ), −∗, defined by ϕ−∗ψ := ¬(ϕ−~¬ψ).2 We also use true, defined
as t := emp∨¬emp. Finally, for Φ = {ϕ1 , . . . , ϕn }, we set ∗ Φ := ϕ1 ∗ϕ2 ∗· · ·∗ϕn ,
if n > 1, and ∗ Φ := emp, if n = 0. By fvs(ϕ) we denote the set of (free) vari-
ables of ϕ. We define the size of the formula ϕ as |ϕ| = 1 for atomic formulas ϕ,
|ϕ1 × ϕ2 | := |ϕ1 | + |ϕ2 | + 1 for × ∈ {∧, ∨, ∗, −~} and |¬ϕ1 | := |ϕ1 | + 1.

1
  As our logic contains negation, x 6= y can be expressed as ¬(x = y). However, we
  treat disequalities as atomic to be able to use them in the positive fragment of our
  logic, defined later, which precludes the use of negation.
2
  As −∗ can be defined via −~ and ¬ and vice-versa, the expressivity of our logic does
  not depend on which operator we choose. We have chosen −~ because we can include
  this operator in the positive fragment considered later on.
                                                                                         7

2.2     Two Semantics of Separation Logic

Memory model. Loc is an infinite set of heap locations. A stack is a partial
function s : Var * Loc. A heap is a partial function h : Loc * Loc. A model is
a stack–heap pair (s, h) with nil ∈ dom(s) and s(nil) ∈/ dom(h). We let locs(h) :=
dom(h) ∪ img(h). A location ` is dangling if ` ∈ img(h) \ dom(h). We write S
for the set of all stacks and H for the set of all heaps.

Two notions of disjoint union of heaps. We write h1 +h2 for the union of disjoint
heaps, i.e.,              
              h1 + h2 := h1 ∪ h2 , if dom(h1 ) ∩ dom(h2 ) = ∅
                            ⊥,        otherwise.
This standard notion of disjoint union is commonly used to assign semantics
to the separating conjunction and magic wand. It requires that h1 and h2 are
domain-disjoint, but does not impose any restrictions on the images of the heaps.
In particular, the dangling pointers of h1 may alias arbitrarily with the domain
and image of h2 and vice-versa.
    Let s be a stack. We write h1 ]s h2 for the disjoint union of h1 and h2 that
restricts aliasing of dangling pointers to the locations in stack s. This yields an
infinite family of union operators: one for each stack. Formally,
                          
              h1 ]s h2 := h1 + h2 , if locs(h1 ) ∩ locs(h2 ) ⊆ img(s)
                            ⊥,         otherwise.
Intuitively, h1 ]s h2 is the (disjoint) union of heaps that share only locations
that are in the image of the stack s. Note that if h1 ]s h2 is defined then h1 + h2
is defined, but not vice-versa.
    Just like the standard disjoint union +, the operator ]s gives rise to a sepa-
ration algebra, i.e., a cancellative, commutative partial monoid [11]:

Lemma 1. Let s be a stack and let u be the empty heap (i.e., dom(u) = ∅). The
triple (H, ]s , u) is a separation algebra.

Weak- and strong-separation logic. Both + and ]s can be used to give a seman-
tics to the separating conjunction and septraction. We denote the corresponding
                  wk      st
model relations |= and |= and define them in Fig. 3. Where the two semantics
agree, we simply write |=.
    In both semantics, emp only holds for the empty heap, and x = y holds for
the empty heap when x and y are interpreted by the same location3 . Points-to
assertions x 7→ y are precise, i.e., only hold in singleton heaps. (It is, of course,
possible to express intuitionistic points-to assertions by x 7→ y ∗ t.) The list
segment predicate ls(x, y) holds in possibly-empty lists of pointers from s(x) to
3
    Usually x = y is defined to hold for all heaps, not just the empty heap, when x
    and y are interpreted by the same location; however, this choice does not change the
    expressivity of the logic: the formula (x = y) ∗ t expresses the standard semantics.
    Our choice is needed for the results on the positive fragment considered in Section 2.3
8

          a                    nil            a              c     nil


          b      nil                          b

Fig. 4: Two models of (ls(a, nil) ∗ t) ∧ (ls(b, nil) ∗ t) for a stack with domain a, b
and a stack with domain a, b, c.

s(y). The semantics of Boolean connectives are standard. The semantics of the
separating conjunction, ∗, and septraction, −~, differ based on the choice of +
                                                                    wk
vs. ]s for combining disjoint heaps. In the former case, denoted |=, we get the
                                                                                st
standard semantics of separation logic (cf. [40]). In the latter case, denoted |=,
we get a semantics that imposes stronger requirements on sub-heap composition:
Sub-heaps may only overlap at locations that are stored in the stack.
                            st
    Because the semantics |= imposes stronger constraints, we will refer to the
                     wk
standard semantics |= as the weak semantics of separation logic and to the se-
          st
mantics |= as the strong semantics of separation logic. Moreover, we use the
terms weak-separation logic (WSL) and strong-separation logic (SSL) to distin-
                                       wk      st
guish between SL with the semantics |= and |=.

Example 1. Let ϕ := a 6= b ∗ (ls(a, nil) ∗ t) ∧ (ls(b, nil) ∗ t). In Fig. 4, we show
two models of ϕ. On the left, we assume that a, b are the only program variables,
whereas on the right, we assume that there is a third program variable c.
    Note that the latter model, where the two lists overlap, is possible in SSL
only because the lists come together at the location labeled by c. If we removed
variable c from the stack, the model would no longer satisfy ϕ according to the
strong semantics, because ]s would no longer allow splitting the heap at that
location. Conversely, the model would still satisfy ϕ with standard semantics.
    This is a feature rather than a bug of SSL: By demanding that the user of
SSL specify aliasing explicitly—for example by using the specification ls(a, c) ∗
ls(b, c) ∗ ls(c, nil) ∧ c 6= nil—we rule out unintended aliasing effects.          4

Satisfiability and Semantic Consequence. We define the notions of satisfiability
and semantic consequence parameterized by a finite set of variables x ⊆ Var.
For a formula ϕ with fvs(ϕ) ⊆ x, we say that ϕ is satisfiable w.r.t. x if there is
                                                      st
a model (s, h) with dom(s) = x such that (s, h) |= ϕ. We say that ϕ entails ψ
                      st               st                    st
w.r.t. x, in signs ϕ |=x ψ, if (s, h) |= ϕ then also (s, h) |= ψ for all models (s, h)
with dom(s) = x.


2.3   Correspondence of Strong and Weak Semantics on Positive
      Formulas

We call an SL formula ϕ positive if it does not contain ¬. Note that, in particular,
this implies that ϕ does not contain the magic wand −∗ or the atom t.
    In models of positive formulas, all dangling locations are labeled by variables:
                                                                                         9

                                              wk
Lemma 2. Let ϕ be positive and (s, h) |= ϕ. Then, (img(h)\dom(h)) ⊆ img(s).

   As every location shared by heaps h1 and h2 in h1 + h2 is either dangling in
h1 or in h2 (or in both), the operations + and ]s coincide on models of positive
formulas:
                             wk                    wk
Lemma 3. Let (s, h1 ) |= ϕ1 and (s, h2 ) |= ϕ2 for positive formulas ϕ1 , ϕ2 .
Then h1 + h2 6= ⊥ iff h1 ]s h2 6= ⊥.

   Since the semantics coincide on atomic formulas by definition and on ∗ by
Lemma 2, we can easily show that they coincide on all positive formulas:
                                                                                         wk
Lemma 4. Let ϕ be a positive formula and let (s, h) be a model. Then, (s, h) |=
              st
ϕ iff (s, h) |= ϕ.

Lemma 4 implies that the two semantics coincide on the popular symbolic-heap
fragment of separation nlogic.4 Further, by   o negating Lemma 4, we have that
                  wk                       st
{(s, h) | (s, h) |= ϕ} 6= (s, h) | (s, h) |= ϕ implies that ϕ contains negation,
either explicitly or in the form of a magic wand or t.
    We remark that formula ϕ in Example 1 only employs t but not ¬, −∗. Hence,
even if only t would be added to the positive fragment, Lemma 4 would no
longer hold. Likewise, Lemma 4 does not hold under intuitionistic semantics: as
the intuitionistic semantics of a predicate p is equivalent to p ∗ t under classic
semantics, it is sufficient to consider ϕ := a 6= b ∗ (ls(a, nil) ∧ (ls(b, nil)).


3     Deciding the SSL Satisfiability Problem
The goal of this section is to develop a decision procedure for SSL:

Theorem 1. Let ϕ ∈ SL and let x ⊆ Var be a finite set of variables with
fvs(ϕ) ⊆ x. It is decidable in PSpace (in |ϕ| and |x|) whether there exists a
                                         st
model (s, h) with dom(s) = x and (s, h) |= ϕ.

Our approach is based on abstracting stack–heap models by abstract memory
states (AMS), which have two key properties, which together imply Theorem 1:
Refinement (Theorem 2). If (s1 , h1 ) and (s2 , h2 ) abstract to the same AMS,
   then they satisfy the same formulas. That is, the AMS abstraction refines
   the satisfaction relation of SSL.
Computability (Theorem 5, Lemmas 20 and 22). For every formula ϕ, we
   can compute (in PSpace) the set of all AMSs of all models of ϕ; then, ϕ is
   satisfiable if this set is nonempty.
4
    Strictly speaking, Lemma 4 implies this only for the symbolic-heap fragment of the
    separation logic studied in this paper, i.e., with the list predicate but no other data
    structures. The result can, however, be generalized to symbolic heaps with trees (see
    the dissertation of the first author [31]). Symbolic heaps of bounded treewidth as
    proposed in [21] are an interesting direction for future work.
10

      The AMS abstraction is motivated by the following insights.

 1. The operator ]s induces a unique decomposition of the heap into at most
    |s| minimal chunks of memory that cannot be further decomposed.
                                st
 2. To decide whether (s, h) |= ϕ holds, it is sufficient to know for each chunk
    of (s, h) a) which atomic formulas the chunk satisfies and b) which variables
    (if any) are allocated in the chunk.

    We proceed as follows. In Sec 3.1, we make precise the notion of memory
chunks. In Sec. 3.2, we define abstract memory states (AMS), an abstraction
of models that retains for every chunk precisely the information from point
(2) above. We will prove the refinement theorem in 3.3. We will show in Sec-
tions 3.4–3.6 that we can compute the AMS of the models of a given formula ϕ,
which allows us to decide satisfiability and entailment problems for SSL. Finally,
we prove the PSpace-completeness result in Sec. 3.7.


3.1     Memory Chunks

We will abstract a model (s, h) by abstracting every chunk of h, which is a
minimal nonempty sub-heap of (s, h) that can be split off of h according to the
strong-separation semantics.

Definition 1 (Sub-heap). Let (s, h) be a model. We say that h1 is a sub-heap
of h, in signs h1 v h, if there is some heap h2 such that h = h1 ]s h2 . We collect
all sub-heaps in the set subHeaps(s, h).                                         4

The following proposition is an immediate consequence of the above definition:
Proposition 1. Let (s, h) be a model. Then, (subHeaps(s, h), v, t, u, ¬) is a
Boolean algebra with greatest element h and smallest element ∅, where

 – (s, h1 ) t (s, h2 ) := (s, h1 ∪ h2 ),
 – (s, h1 ) u (s, h2 ) := (s, h1 ∩ h2 ), and
 – ¬(s, h1 ) := (s, h01 ), where h01 ∈ subHeaps(s, h) is the unique sub-heap with
   h = h1 ]s h01 .

    The fact that the sub-models form a Boolean algebra allows us to make the
following definition5 :

Definition 2 (Chunk). Let (s, h) be a model. A chunk of (s, h) is an atom of
the Boolean algebra (subHeaps(s, h), v, t, u, ¬). We collect all chunks of (s, h)
in the set chunks(s, h).                                                       4

   Because every element of a Boolean algebra can be uniquely decomposed into
atoms, we obtain that every heap can be fully decomposed into its chunks:

Proposition 2. Let (s, h) be a model and let chunks(s, h) = {h1 , . . . , hn } be its
chunks. Then, h = h1 ]s h2 ]s · · · ]s hn .
                                                                                      11



            1: x          2       3 : y, z    8          ≥2
                                                     x        y, z

                      5: u        6          9: v        =1
                                                               v

                   7: w       4       10     11     {{{w} , {u}} , {{y, z}}}   1


Fig. 5: Graphical representation of a model consisting of five chunks (left, see
Ex. 2) and its induced AMS (right, see Ex. 5).

Example 2. Let s = {x 7→ 1, y 7→ 3, u 7→ 5, z 7→ 3, w 7→ 7, v 7→ 9} and h =
{1 7→ 2, 2 7→ 3, 3 7→ 8, 4 7→ 6, 5 7→ 6, 6 7→ 3, 7 7→ 6, 9 7→ 9, 10 7→ 11, 11 7→ 10}.
The model (s, h) is illustrated in Fig. 5. This time, we include the identities of
the locations in the graphical representation; e.g., 3 : y, z represents location 3,
s(y) = 3, s(z) = 3. The model consists of five chunks, h1 := {1 7→ 2, 2 7→ 3},
h2 := {9 7→ 9}, h3 := {4 7→ 6, 5 7→ 6, 6 7→ 3, 7 7→ 6}, h4 := {3 7→ 8}, and
h5 := {10 7→ 11, 11 7→ 10}.                                                        4

   We distinguish two types of chunks: those that satisfy SSL atoms and those
that don’t.

Definition 3 (Positive and Negative chunk). Let hc ⊆ h be a chunk of
(s, h). hc is a positive chunk if there exists an atomic formula τ such that
          st
(s, hc ) |= τ . Otherwise, hc is a negative chunk. We collect the respective chunks
in chunks+ (s, h) and chunks− (s, h).

Example 3. Recall the chunks h1 through h5 from Ex. 2. h1 and h2 are positive
chunks (blue in Fig. 5), h3 to h5 are negative chunks (orange).            4

     Negative chunks fall into three (not mutually-exclusive) categories:

Garbage. Chunks with locations that are inaccessible via stack variables.
Unlabeled dangling pointers. Chunks with an unlabeled sink, i.e., a dan-
   gling location that is not in img(s) and thus cannot be “made non-dangling”
   via composition using ]s .
Overlaid list segments. Overlaid list segments that cannot be separated via
   ]s because they are joined at locations that are not in img(s).

Example 4 (Negative chunks). The chunk h3 from Example 2 contains garbage,
namely the location 4 that cannot be reached via stack variables, and two over-
laid list segments (from 5 to 3 and 7 to 3). The chunk h4 has an unlabeled
dangling pointer. The chunk h5 contains only garbage.
5
    It is an interesting question for future work to relate the chunks considered in this
    paper to the atomic building blocks used in SL symbolic executions engines. Likewise,
    it would be interesting to build a symbolic execution engine based on the chunks
    resp. on the AMS abstraction proposed in this paper.
12

3.2      Abstract Memory States
In abstract memory states (AMSs), we retain for every chunk enough information
to (1) determine which atomic formulas the chunk satisfies, and (2) keep track
of which variables are allocated within each chunk.

Definition 4. A quadruple A = hV, E, ρ, γi is an abstract memory state, if
1. V is a partition of some finite set of variables, i.e., V = {v1 , . . . , vn } for
   some non-empty disjoint finite sets vi ⊆ Var,
2. E : V * V ×{= 1, ≥ 2} is a partial function such that there is no v ∈ dom(E)
   with nil ∈ v6 ,
3. ρ consists of disjoint subsets of V such that every R ∈ ρ is disjoint from
   dom(E) and there is no v ∈ R with nil ∈ v,
4. γ is a natural number, i.e., γ ∈ N.
We call V the nodes, E the edges, ρ the negative-allocation constraint and γ
the garbage-chunk count of A. We call the AMS A = hV, E, ρ, γi garbage-free
if ρ = ∅ and γ = ∅.
     We collect the set of all AMSs in AMS. The size of A is given by |A| :=
|V | + γ. Finally,
           S       the allocated variables of an AMS are given by alloc(A) :=
dom(E) ∪ ρ.                                                                 4

    Every model induces an AMS, defined in terms of the following auxiliary defi-
                                                                  s
nitions. The equivalence class of variable x w.r.t. stack s is [x]= := {y | s(y) = s(x)};
                                                                 s
the set of all equivalence classes of s is cls= (s) := {[x]= | x ∈ dom(s)}. We
now define the edges induced by a model (s, h): For every equivalence class
   s
[x]= ∈ cls= (s), we set
                       s
                      
                       h[y]= , = 1i there are y ∈ dom(s) and hc ∈ chunks+ (s, h)
                                                    st
                                      with (s, hc ) |= x 7→ y
                      
                      
                      
                      
                s
edges(s, h)([x]= ) := h[y]s= , ≥ 2i there are y ∈ dom(s) and hc ∈ chunks+ (s, h)
                                                     st
                      
                                      with (s, hc ) |= ls(x, y) ∧ ¬x 7→ y
                      
                      
                      
                      
                      
                        ⊥,           otherwise.
                      

Finally, we denote the sets of variables allocated in negative chunks by
                              s
         alloc− (s, h) := {{[x]= | s(x) ∈ dom(hc )} | hc ∈ chunks− (s, h)} \ {∅},

where (equivalence classes of) variables that are allocated in the same negative
chunk are grouped together in a set.
   Now we are ready to define the induced AMS of a model.
Definition 5. Let (s, h) be a model. Let V := cls= (s), E := edges(s, h), ρ :=
alloc− (s, h) and γ := chunks− (s, h) − alloc− (s, h) . Then ams(s, h) := hV, E, ρ, γi
is the induced AMS of (s, h).                                                     4
6
     The edges of an AMS represent either a single pointer (case “= 1”) or a list segment
     of at least length two (case “≥ 2”).
                                                                                     13

Example 5. The induced AMS of the model (s, h) from Ex. 2 is illustrated on
the right-hand side of Fig. 5. The blue box depicts the graph (V, E) induced
by the positive chunks h1 , h2 ; the negative chunks that allocate variables are
abstracted to the set ρ = {{{w} , {u}} , {{y, z}}} (note that the variables w and
u are allocated in the chunk h3 and the aliasing variables y, z are allocated in
h4 ); and the garbage-chunk count is 1, because h5 is the only negative chunk
that does not allocate stack variables.                                        4

      Observe that the induced AMS is indeed an AMS:

Proposition 3. Let (s, h) be a model. Then ams(s, h) ∈ AMS.
    The reverse also holds: Every AMS is the induced AMS of at least one model;
in fact, even of a model of linear size.

Lemma 5 (Realizability of AMS). Let A = hV, E, ρ, γi be an AMS. There
exists a model (s, h) with ams(s, h) = A whose size is linear in the size of A.
    The following lemma demonstrates that we only need the ρ and γ components
in order to be able to deal with negation and/or the magic wand:

Lemma 6 (Models of Positive Formulas Abstract to Garbage-free AMS).
Let (s, h) be a model. If (s, h) |= ϕ for a positive formula ϕ, then ams(s, h) is
garbage-free.

      We abstract SL formulas by the set of AMS of their models:

Definition 6. Let s be a stack. The SL abstraction w.r.t. s, αs : SL → 2AMS ,
is given by
                                                               st
                  αs (ϕ) := {ams(s, h) | h ∈ H, and (s, h) |= ϕ}.                    4

    Because AMSs do not retain any information about heap locations, just about
aliasing, abstractions do not differ for stacks with the same equivalence classes:

Lemma 7. Let s, s0 be stacks with cls= (s) = cls= (s0 ). Then αs (ϕ) = αs0 (ϕ) for
all formulas ϕ.


3.3     The Refinement Theorem for SSL

The main goal of this section is to show the following refinement theorem:

Theorem 2 (Refinement Theorem). Let ϕ be a formula and let (s, h1 ),
                                                                  st                st
(s, h2 ) be models with ams(s, h1 ) = ams(s, h2 ). Then (s, h1 ) |= ϕ iff (s, h2 ) |= ϕ.

    We will prove this theorem step by step, characterizing the AMS abstraction
of all atomic formulas and of the composed models before proving the refinement
theorem. In the remainder of this section, we fix some model (s, h).
14

Abstract Memory States of Atomic Formulas The empty-heap predicate emp is
only satisfied by the empty heap, i.e., by a heap that consists of zero chunks:

Lemma 8. (s, h) |= emp iff ams(s, h) = hcls= (s), ∅, ∅, 0i
                                                                               s       s
Lemma 9. 1. (s, h) |= x = y iff ams(s, h) = hcls= (s), ∅, ∅, 0i and [x]= = [y]= .
                                                                s       s
 2. (s, h) |= x 6= y iff ams(s, h) = hcls= (s), ∅, ∅, 0i and [x]= 6= [y]= .

     Models of points-to assertions consist of a single positive chunk of size 1:
                               s          s
Lemma 10. Let E = {[x]= 7→ h[y]= , = 1i}. (s, h) |= x 7→ y iff ams(s, h) =
hcls= (s), E, ∅, 0i.

    Intuitively, the list segment ls(x, y) is satisfied by models (s, h) that consist
of zero or more positive chunks, corresponding to a (possibly empty) list from
                                   s      s
some equivalence class [x]= to [y]= via (zero or more) intermediate equivalence
             s                s
classes [x1 ]= , . . . , [xn ]= . We will use this intuition to define abstract lists; this
notion allows us to characterize the AMSs arising from abstracting lists.
Definition 7. Let A = hV, E, ρ, γi ∈ AMS, s be a stack and x, y ∈ Var. We
say A is an abstract list w.r.t. x and y, in signs A ∈ AbstLists(x, y), iff

 1. V = cls= (s),
 2. ρ = ∅ and γ = 0, and
 3. we can pick nodes v1 , . . . , vn ∈ V and labels ι1 , . . . , ιn−1 ∈ {= 1, ≥ 2} such
    that x ∈ v1 , y ∈ vn and E = {vi 7→ hvi+1 , ιi i | 1 ≤ i < n}.                    4

Lemma 11. (s, h) |= ls(x, y) iff ams(s, h) ∈ AbstLists(x, y).

Abstract Memory States of Models composed by the Union Operator Our next
goal is to lift the union operator ]s to the abstract domain AMS. We will define
an operator • with the following property:

           if h1 ]s h2 6= ⊥ then ams(s, h1 ]s h2 ) = ams(s, h1 ) • (s, h2 ).

    AMS composition is a partial operation defined only on compatible AMS.
Compatibility enforces (1) that the AMSs were obtained for equivalent stacks
(i.e., for stacks s, s0 with cls= (s) = cls= (s0 )), and (2) that there is no double
allocation.

Definition 8 (Compatibility of AMSs). AMSs A1 = hV1 , E1 , ρ1 , γ1 i and
A2 = hV2 , E2 , ρ2 , γ2 i are compatible iff (1) V1 = V2 and (2) alloc(A1 ) ∩
alloc(A2 ) = ∅.

   Note that if h1 ]s h2 is defined, then ams(s, h1 ) and ams(s, h2 ) are compatible.
The converse is not true, because ams(s, h1 ) and ams(s, h2 ) may be compatible
even if dom(h1 ) ∩ dom(h2 ) 6= ∅.
   AMS composition is defined in a point-wise manner on compatible AMSs
and undefined otherwise.
                                                                                 15

Definition 9 (AMS composition). Let A1 = hV1 , E1 , ρ1 , γ1 i and A2 = hV2 , E2 , ρ2 , γ2 i
be two AMS. The composition of A1 , A2 is then given by
                 (
                  hV1 , E1 ∪ E2 , ρ1 ∪ ρ2 , γ1 + γ2 i , if A1 , A2 compatible
      A1 • A2 :=
                  ⊥,                                    otherwise.

Lemma 12. Let s be a stack and let h1 , h2 be heaps. If h1 ]s h2 6= ⊥ then
ams(s, h1 ) • ams(s, h2 ) 6= ⊥.
    We next show that ams(s, h1 ]s h2 ) = ams(s, h1 ) • ams(s, h2 ) whenever h1 ]s
h2 is defined:
Lemma 13 (Homomorphism of composition). Let (s, h1 ), (s, h2 ) be models
with h1 ]s h2 6= ⊥. Then, ams(s, h1 ]s h2 ) = ams(s, h1 ) • ams(s, h2 ).
     To show the refinement theorem, we need one additional property of AMS
composition. If an AMS A of a model (s, h) can be decomposed into two smaller
AMS A = A1 • A2 , it is also possible to decompose the heap h into smaller heaps
h1 , h2 with ams(s, hi ) = Ai :
Lemma 14 (Decomposability of AMS). Let ams(s, h) = A1 • A2 . There
exist h1 , h2 with h = h1 ]s h2 , ams(s, h1 ) = A1 and ams(s, h2 ) = A2 .
    These results suffice to prove the Refinement Theorem stated at the beginning
of this section (see the extended version [33] for a proof).
                                                                   st
Corollary 1. Let (s, h) be a model and ϕ be a formula. (s, h) |= ϕ iff ams(s, h) ∈
αs (ϕ).

3.4   Recursive Equations for Abstract Memory States
In this section, we derive recursive equations that reduce the set of AMS αs (ϕ) for
arbitrary compound formulas to the set of AMS of the constituent formulas of ϕ.
In the next sections, we will show that we can actually evaluate these equations,
thus obtaining an algorithm for computing the abstraction of arbitrary formulas.
Lemma 15. αs (ϕ1 ∧ ϕ2 ) = αs (ϕ1 ) ∩ αs (ϕ2 ).
Lemma 16. αs (ϕ1 ∨ ϕ2 ) = αs (ϕ1 ) ∪ αs (ϕ2 ).
Lemma 17. αs (¬ϕ1 ) = {ams(s, h) | h ∈ H} \ αs (ϕ1 ).

The Separating Conjunction In Section 3.3, we defined the composition opera-
tion, •, on pairs of AMS. We now lift this operation to sets of AMS A1 , A2 :

           A1 • A2 := {A1 • A2 | A1 ∈ A1 , A2 ∈ A2 , A1 • A2 6= ⊥} .

   Lemma 13 implies that αs is a homomorphism from formulas and ∗ to sets
of AMS and •:
Lemma 18. For all ϕ1 , ϕ2 , αs (ϕ1 ∗ ϕ2 ) = αs (ϕ1 ) • αs (ϕ2 ).
16

The septraction operator. We next define an abstract septraction operator −•
that relates to • in the same way that −~ relates to ∗. For two sets of AMS
A1 , A2 we set:
         A1 −•A2 := {A ∈ AMS | there exists A1 ∈ A1 s.t. A • A1 ∈ A2 }
      Then, αs is a homomorphism from formulas and −~ to sets of AMS and −•:
Lemma 19. For all ϕ1 , ϕ2 , αs (ϕ1 −~ϕ2 ) = αs (ϕ1 )−•αs (ϕ2 ).

3.5     Refining the Refinement Theorem: Bounding Garbage
Even though we have now characterized the set αs (ϕ) for every formula ϕ, we
do not yet have a way to implement AMS computation: While αs (ϕ) is finite
if ϕ is a spatial atom, the set is infinite in general; see the cases αs (¬ϕ) and
αs (ϕ1 −~ϕ2 ). However, we note that for a fixed stack s only the garbage-chunk
count γ of an AMS hV, E, ρ, γi ∈ αs (ϕ) can be of arbitrary size, while the size
of the nodes V , the edges E and the negative-allocation constraint ρ is bounded
by |s|. Fortunately, to decide the satisfiability of any fixed formula ϕ, it is not
necessary to keep track of arbitrarily large garbage-chunk counts.
    We introduce the chunk size dϕe of a formula ϕ, which provides an upper
bound on the number of chunks that may be necessary to satisfy and/or falsify
the formula; dϕe is defined as follows:
 – dempe = dx 7→ ye = dls(x, y)e = dx = ye = dx 6= ye := 1
 – dϕ ∗ ψe := dϕe + dψe
 – dϕ−~ψe := dψe
 – dϕ ∧ ψe = dϕ ∨ ψe := max(dϕe, dψe)
 – d¬ϕe := dϕe.
Observe that dϕe ≤ |ϕ| for all ϕ. Intuitively, dϕe − 1 is an upper bound on the
number of times the operation ]s needs to be applied when checking whether
        st
(s, h) |= ϕ. For example, let ψ := x 7→ y ∗ ((b 7→ c)−~(ls(a, c)). Then dψe = 2,
and to verify that ψ holds in a model that consists of a pointer from x to y and
a list segment from a to b, it suffices to split this model dϕe − 1 = 1 many times
using ]s (into the pointer and the list segment).
    We generalize the refinement theorem, Theorem 2, to models whose AMS
differ in their garbage-chunk count, provided both garbage-chunk counts exceed
the chunk size of the formula:
Theorem 3 (Refined Refinement Theorem). Let ϕ be a formula with dϕe =
k. Let m ≥ k, n ≥ k and let (s, h1 ), (s, h2 ) be models with ams(s, h1 ) = hV, E, ρ, mi,
                                            st                st
ams(s, h2 ) = hV, E, ρ, ni. Then, (s, h1 ) |= ϕ iff (s, h2 ) |= ϕ.
   This implies that ϕ is satisfiable over stack s iff ϕ is satisfiable by a heap
that contains at most dϕe garbage chunks:
Corollary 2. Let ϕ be an formula with dϕe = k. Then ϕ is satisfiable over stack
s iff there exists a heap h such that (1) ams(s, h) = (V, E, ρ, γ) for some γ ≤ k
                st
and (2) (s, h) |= ϕ.
                                                                                                 17


   absts (emp) := {hcls= (s), ∅, ∅, 0i}
  absts (x = y) := if s(x) = s(y) then {hcls= (s), ∅, ∅, 0i} else ∅
 absts (x 6= y) := if s(x) 6= s(y) then {hcls= (s), ∅, ∅, 0i} else ∅
 absts (x 7→ y) := cls= (s), [x]s= 7→ [y]s= , ∅, 0
                              

absts (ls(x, y)) := AbstLists(x, y) ∩ AMS0,s
absts (ϕ1 ∗ ϕ2 ) := AMSdϕ1 ∗ϕ2 e,s ∩ (liftdϕ1 e%dϕ1 ∗ϕ2 e (absts (ϕ1 )) • liftdϕ2 e%dϕ1 ∗ϕ2 e (absts (ϕ2 )))
absts (ϕ1 −~ϕ2 ) := AMSdϕ1 −~ϕ2 e,s ∩ (absts (ϕ1 )−•liftdϕ2 e%dϕ1 ∗ϕ2 e (absts (ϕ2 )))
absts (ϕ1 ∧ ϕ2 ) := liftdϕ1 e%dϕ1 ∧ϕ2 e (absts (ϕ1 )) ∩ liftdϕ2 e%dϕ1 ∧ϕ2 e (absts (ϕ2 ))
absts (ϕ1 ∨ ϕ2 ) := liftdϕ1 e%dϕ1 ∨ϕ2 e (absts (ϕ1 )) ∪ liftdϕ2 e%dϕ1 ∨ϕ2 e (absts (ϕ2 ))
      absts (¬ϕ1 ) := AMSdϕ1 e,s \ absts (ϕ1 )

Fig. 6: Computing the abstract memory states of the models of ϕ with stack s.

3.6     Deciding SSL by AMS Computation
In light of Cor. 2, we can decide the SSL satisfiability problem by means of a func-
tion absts (ϕ) that computes the (finite) intersection of the (possibly infinite) set
αs (ϕ) and the (finite) set AMSk,s := {hV, E, ρ, γi ∈ AMS | V = cls= (s) and γ ≤ k}
for k = dϕe. We define absts (ϕ) in Fig. 6. For atomic predicates we only need to
consider garbage-chunk-count 0, whereas the cases ∗, −~, ∧ and ∨ require lifting
the bound on the garbage-chunk count from m to n ≥ m.
Definition 10. Let m, n ∈ N with m ≤ n and let A = hV, E, ρ, γi ∈ AMS. The
bound-lifting of A from m to n is
                            (
                              {A}                         if γ < m
             liftm%n (A) :=
                              {hV, E, ρ, ki | m ≤ k ≤ n} if γ = m.
                                                            S
We generalize bound-lifting to sets of AMS: liftm%n (A) := A∈A liftm%n (A). 4
      As a consequence of Theorem 3, bound-lifting is sound for all n ≥ dϕe, i.e.,

                    liftdϕe%n (αs (ϕ) ∩ AMSdϕe ) = αs (ϕ) ∩ AMSn .

By combining this observation with the lemmas characterizing αs (Lemmas 8,9,10,
11,15, 16,17, 18 and 19), we obtain the correctness of absts (ϕ):
Theorem 4. Let s be a stack and ϕ be a formula. Then, absts (ϕ) = αs (ϕ) ∩
AMSdϕe,s .

Computability of absts (ϕ). We note that the operators •, −•, ∩, ∪ and \ are all
computable as the sets that occur in the definition of absts (ϕ) are all finite. It
remains to argue that we can compute the set of AMS for all atomic formulas.
This is trivial for emp, (dis-)equalities, and points-to assertions. For the list-
segment predicate, we note that the set absts (ls(x, y)) = AbstLists(x, y) ∩
AMSd0e,s can be easily computed as there are only finitely many abstract lists
w.r.t. the set of nodes V = cls= (s). We obtain the following results:
18
                                 V
        qbf to sl(F ) := emp ∧       pairwise different QBF variables x,y x 6= y ∧ aux(F )


      aux(x) := (x 7→ nil) ∗ t                        aux(¬x) := ¬aux(x)
 aux(F ∧ G) := aux(F ) ∧ aux(G)                   aux(F ∨ G) := aux(F ) ∨ aux(G)
 aux(∃x. F ) := (x 7→ nil ∨ emp)−~aux(F )          aux(∀x. F ) := (x 7→ nil ∨ emp)−∗aux(F )

Fig. 7: Translation qbf to sl(F ) from closed QBF formula F (in negation normal
form) to a formula that is satisfiable iff F is true.

Corollary 3. Let s be a (finite) stack. Then absts (ϕ) is computable for all for-
mulas ϕ.

Theorem 5. Let ϕ ∈ SL and let x ⊆ Var be a finite set of variables with
fvs(ϕ) ⊆ x. It is decidable whether there exists a model (s, h) with dom(s) = x
            st
and (s, h) |= ϕ.
                    st
Corollary 4. ϕ |=x ψ is decidable for all finite sets of variables x ⊆ Var and
ϕ, ψ ∈ SL with fvs(ϕ) ⊆ x and fvs(ψ) ⊆ x.


3.7   Complexity of the SSL Satisfiability Problem

It is easy to see that the algorithm absts (ϕ) runs in exponential time. We con-
clude this section with a proof that SSL satisfiability and entailment are actually
PSpace-complete.

PSpace-hardness. An easy reduction from quantified Boolean formulas (QBF)
shows that the SSL satisfiability problem is PSpace-hard. The reduction is
presented in Fig. 7. We encode positive literals x by (x 7→ nil) ∗ t (the heap
contains the pointer x 7→ nil) and negative literals by ¬((x 7→ nil) ∗ t) (the heap
does not contain the pointer x 7→ nil). The magic wand is used to simulate
universals (i.e., to enforce that we consider both the case x 7→ nil and the case
emp, setting x both to true and to false). Analogously, septraction is used to
simulate existentials. Similar reductions can be found (for standard SL) in [12].

Lemma 20. The SSL satisfiability problem is PSpace-hard (even without the
ls predicate).

    Note that this reduction simultaneously proves the PSpace-hardness of SSL
model checking: If F is a QBF formula over variables x1 , . . . , xk , then qbf to sl(F )
                                                 st
is satisfiable iff ({xi 7→ li | 1 ≤ i ≤ n} , ∅) |= qbf to sl(F ) for some locations `i
with `i 6= `j for i 6= j.

PSpace-membership. For every stack s and every bound on the garbage-chunk
count of the AMS we consider, it is possible to encode every AMS by a string of
polynomial length.
                                                                                       19


     {x 7→ z} x.next := y {x 7→ y}            {emp} malloc(x) {x 7→ m}

     {x 7→ z} free(x) {emp}                   {emp} x := y {x = y}
                                                        x different from y
                {y 7→ z} x := y.next {y 7→ z ∗ x = z}
                                               ϕ is x = y or x 6= y
                       {emp} assume(ϕ) {ϕ}

Fig. 8: Local proof rules of program statements for forward symbolic execution.

                              {P } c {Q}
         Frame rule                                x = modifiedVars(c), x0 fresh
                       {A ∗ P } c {A[x0 /x] ∗ Q}
                                  {P } c {Q}             st
    Materialization                                   Q |= ¬((x 7→ nil)−~t), z fresh
                      {P } c {x 7→ z ∗ ((x 7→ z)−~Q)}

Fig. 9: The frame and the materialization rule for forward symbolic execution.

Lemma 21. Let k ∈ N, let s be a stack and n := k+|s|. There exists an injective
                                 ∗
function encode : AMSk,s → {0, 1} such that

                |encode(A)| ∈ O(n log(n))          for all A ∈ AMSk,s .

   An enumeration-based implementation of the algorithm in Fig. 6 (that has
to keep in memory at most one AMS per subformula at any point in the com-
putation) therefore runs in PSpace:

Lemma 22. Let ϕ ∈ SL and let x ⊆ Var be a finite set of variables with
fvs(ϕ) ⊆ x. It is decidable in PSpace (in |ϕ| and |x|) whether there exists a
                                         st
model (s, h) with dom(s) = x and (s, h) |= ϕ.

  The PSpace-completeness result, Theorem 1, follows by combining Lem-
mas 20 and 22.


4    Program Verification with Strong-Separation Logic
Our main practical motivation behind SSL is to obtain a decidable logic that can
be used for fully automatically discharging verification conditions in a Hoare-
style verification proof. Discharging VCs can be automated by calculi that sym-
bolically execute pre-conditions forward resp. post-conditions backward, and
then invoking an entailment checker. Symbolic execution calculi typically either
introduce first-order quantifiers or fresh variables in order to deal with updates
to the program variables. We leave the extension of SSL to support for quan-
tifiers for future work and in this paper develop a forward symbolic execution
calculus based on fresh variables.
     We target the usual Hoare-style setting where a verification engineer anno-
tates the pre- and post-condition of a function and provides loop invariants. We
20

               x.next:=y
        (s, h) −−−−−−→ (s0 , h0 )          if s(x) ∈ dom(h), with s0 = s
                                                 and h0 = h[s(x)/s(y)]
               x.next:=y
        (s, h) −−−−−−→ error               if s(x) 6∈ dom(h)
               x:=y.next
        (s, h) −−−−−−→ (s0 , h0 )          if s(y) ∈ dom(h), with s0 = s[x/h(s(y))]
                                                 and h0 = h
               x:=y.next
        (s, h) −−−−−−→ error               if s(y) 6∈ dom(h)
               free(x)
        (s, h) −−−−→ (s0 , h0 )            if s(x) ∈ dom(h), with s0 = s
                                                 and h0 = h[s(x)/⊥]
               free(x)
        (s, h) −−−−→ error                 if s(x) 6∈ dom(h)
               malloc(x)
        (s, h) −−−−−→ (s0 , h0 )           with s0 = s[x/l][m/k] and h0 = h[l/k]
                                                for some l ∈ Loc \ dom(h), k ∈ Loc
               x:=y
        (s, h) −−−→ (s0 , h0 )             with s0 = s[x/s(y)] and h0 = h
               assume(ϕ)
        (s, h) −−−−−−→ (s0 , h0 ),        if s(x) = s(y) resp. s(x) 6= s(y),
               where ϕ is x = y or x 6= y       with s0 = s and h0 = h
                           Fig. 10: Semantics of program statements.

exemplify two annotated functions in Fig. 11; the left function reverses a list
and the right function copies a list. In addition to the program variables, our
annotations may contain logical variables (also known as ghost variables); for
example, the annotations of list reverse only contain program variables, while
the annotations of list copy also contain the logical variable u (which is assumed
to be equal to x in the pre-condition)7 .

A simple heap-manipulating programming language. We consider the six pro-
gram statements x.next := y, x := y.next (where x is different from y), free(x),
malloc(x), x := y and assume(ϕ), where ϕ is x = y or x 6= y. We remark that
we do not include a statement x := x.next for ease of exposition; however, this is
w.l.o.g. because x := x.next can be simulated by the statements y := x.next; x := y
at the expense of introducing an additional program variable y. We specify the
semantics of the considered program statements via a small-step operational se-
                                                                               c
mantics. We state the semantics in Fig. 10, where we write (s, h) →            − (s0 , h0 ),
with the meaning that executing c in state (s, h) leads to state (s , h0 ), and0
          c
(s, h) → − error , when executing c leads to an error. Our only non-standard choice
is the modelling of the malloc statement: we assume a special program variable
m, which is never referenced by any program statement and only used in the
modelling; the malloc statement updates the value of the variable m to the target
of the newly allocated memory cell; we include m in order to have a name for
the target of the newly allocated memory cell. We say program statement c is
                                                                          c
safe for a stack-heap pair (s, h) if there is no transition (s, h) →     − error . Given
                                                                             c
a sequence of program statements c = c1 · · · ck , we write (s, h) −        → (s0 , h0 ), if
there are stack-heap pairs (si , hi ), with (s0 , h0 ) = (s, h), (sk , hk ) = (s0 , h0 ) and
            ci
(si , hi ) −→  (si+1 , hi+1 ) for all 1 ≤ i ≤ k.
7
     m is a special program variable introduced for modelling malloc.
                                                                                     21

Forward Symbolic Execution Rules. The rules for the program statements in
Fig. 8 are local in the sense that they only deal with a single pointer or the
empty heap. The rules in Fig. 9 are the main rules of our forward symbolic
execution calculus. The frame rule is essential for lifting the local proof rules to
larger heaps. The materialization rule ensures that the frame rule can be applied
whenever the pre-condition of a local proof rule can be met. We now give more
details. For a sequence of program statements c = c1 · · · ck and a pre-condition
Pstart , the symbolic execution calculus derives triples {Pstart } c1 · · · ci {Qi } for
all 1 ≤ i ≤ k. In order to proceed from i to i + 1, either 1) only the frame rule is
applied or 2) the materialization rule is applied first followed by an application
of the frame rule. The frame rule can be applied if the formula Qi has the shape
Qi = A ∗ P , where A is suitably chosen and P is the pre-condition of the local
proof rule for statement ci . Then, Qi+1 is given by Qi+1 = A[x0 /x] ∗ Q, where
x = modifiedVars(c), x0 are fresh copies of the variables x and Q is the right hand
side of the local proof rule for statement ci , i.e., we have {P } ci {Q}. Note that the
frame rule requires substituting the modified program variables with fresh copies:
We set modifiedVars(c) := {x, m} for c = malloc(x), modifiedVars(c) := {x}
for c = x := y.next and c = x := y, and modifiedVars(c) := ∅, otherwise. The
materialization rule may be applied in order to ensure that Qi has the shape
Qi = A ∗ P . This is not needed in case P = emp but may be necessary for
points-to assertions such as P = x 7→ y. We note that Qi guarantees that a
                                 st
pointer x is allocated iff Qi |= ¬((x 7→ nil)−~t). Under this condition, the rule
allows introducing a name z for the target of the pointer x. We remark that
while backward-symbolic execution calculi typically employ the magic wand,
our forward calculus makes use of the dual septraction operator: this operator
allowed us to design a general rule that guarantees a predicate of shape Qi =
A ∗ P without the need of coming up with dedicated rules for, e.g., unfolding list
predicates.


Applying the forward symbolic execution calculus for verification. We now ex-
plain how the proof rules presented in Fig. 8 and 9 can be used for program
verification. Our goal is to verify that the pre-condition P of a loop-free piece
of code c (in our case, a sequence of program statements) implies the post-
condition Q. For this, we apply the symbolic execution calculus and derive a
triple {P } c {Q0 }. It then remains to verify that the final state of the symbolic
execution Q0 implies the post-condition Q. Here, we face the difficulty that the
symbolic execution introduces additional variables: Let us assume that all anno-
tations are over a set of variables x, which includes the program variables and
the logical variables. Further assume that the symbolic execution {P } c {Q0 } in-
troduced the fresh variables y. With the results of Section 3 we can then verify
                      st
the entailment Q0 |=x∪y Q. However, we need to guarantee that all models (s, h)
of Q with dom(s) = x ∪ y are also models when we restrict dom(s) to x (note
that the variables y are implicitly existentially quantified; we make this state-
ment precise in Lemma 26 below). In order to deal with this issue, we require
annotations to be robust:
22

Definition 11 (Robust Formula). We call a formula ϕ ∈ SL robust, if for
all models (s1 , h) and (s2 , h) with fvs(ϕ) ⊆ dom(s1 ) and fvs(ϕ) ⊆ dom(s2 ) and
                                                           st                st
s1 (x) = s2 (x) for all x ∈ fvs(ϕ), we have that (s1 , h) |= ϕ iff (s2 , h) |= ϕ.

   We identify a fragment of robust formulas in the next lemma. In particular,
we obtain that the annotations in Fig. 11 are robust.

Lemma 23. Let ϕ ∈ SL be a positive formula. Then, ϕ is robust.

   The following lemma allows us to construct robust formulas from known
robust formulas:

Lemma 24. Let ϕ ∈ SL be formula. If ϕ is robust, then ϕ ∗ x 7→ y and x 7→
y−~ϕ are robust.

   Not all formulas are robust, e.g., consider ϕ from Example 1. On the other
hand, Lemma 4 does not cover all robust formulas, e.g., t is robust. We leave the
identification of further robust formulas for future work.

Soundness of Forward Symbolic Execution. We adapt the notion of a local action
from [11] to contracts:

Definition 12 (Local Contract). Given some program statement c and SL
formulae P, Q, we say the triple {P } c {Q} is a local contract, if for every stack-
                              st
heap pair (s, h) with (s, h) |= P , every stack t with s ⊆ t and every heap h◦ with
h ]t h◦ 6= ⊥, we have that

1) c is safe for (t, h ]t h◦ ), and
                                                           c
2) for every stack-heap pair (t0 , h0 ) with (t, h ]t h◦ ) →
                                                           − (t0 , h0 ) there is some heap
                   0                        st
   h# with h# ]t h◦ = h0 and (t0 , h# ) |= Q.

      We now state that our local proofs rules specify local contracts:

Lemma 25. Let c be a program statement, and let {P } c {Q} be the triple from
its local proof rule as stated in Fig. 8. Then, {P } c {Q} is a local contract.

    We are now ready to state the soundness of our symbolic execution calculus
(we assume robust formulas A in the frame rule, which can be ensured by the
materialization rule8 ); we note that the statement makes precise the implicitly
existentially quantified variables, stating that there is an extension of the stack
to the variables V introduced by the symbolic execution such that Q holds:
8
     Assume that Q is the robust formula currently derived by the symbolic execution,
     that c is the next program statement, that {Pc } c {Qc } is the triple from the local
     proof rule of program statement c, and that Q is of shape Q = A ∗ Pc . In case A
     is not robust (note that this is only possible if Pc = x 7→ z for some variables x
     and z), then one can first apply the materialization rule in order to derive formula
     Q0 = x 7→ z ∗ ((x 7→ z)−~Q). Then, A0 = (x 7→ z)−~Q is robust by Lemma 24.
                                                                                        23

                              % list copy
                              {ls(x, nil) ∗ u = x}
% list reverse
                                  malloc(s);
{ls(x, nil)}
                                  r := s;
    a := nil;
                                  while(x 6= nil)
    while(x 6= nil)
                                  {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s) ∗ s 7→ m}
    {ls(x, nil) ∗ ls(a, nil)}
                                  {
    {
                                      malloc(t);
        b := x.next;
                                      % t.data := x.data; not modelled
        x.next := a;
                                      s.next := t;
        a := x;
                                      s := t;
        w := b;
                                      y := x.next;
    }
                                      x := y;
    x := w;
                                  }
{ls(x, nil)}
                                  s.next := nil;
                              {ls(u, nil) ∗ ls(r, nil)}


Fig. 11: List reverse (left) and list copy (right) annotated pre- and post-condition
and loop invariants.


Lemma 26 (Soundness of Forward Symbolic Execution). Let c be a se-
quence of program statements, let P be a robust formula, let {P } c {Q} be the
triple obtained from symbolic execution, and let V be the fresh variables intro-
                                                                                c
duced during symbolic execution. Then, Q is robust and for all (s, h) −        → (s0 , h0 )
             st                                                                        st
with (s, h) |= P , there is a stack s00 with s0 ⊆ s00 , V ⊆ dom(s00 ) and (s00 , h0 ) |= Q.




Automation. We note that the presented approach can fully-automatically verify
that the pre-condition of a loop-free piece of code guarantees its post-condition:
For every program statement, we apply its local proof rule using the frame rule
(and in addition the materialization rule in case the existence of a pointer target
must be guaranteed). We then discharge the entailment query using our decision
procedure from Section 3. We now illustrate this approach on the programs from
Fig. 11. For both programs we verify that the loop invariant is inductive (in both
cases the loop-invariant P is propagated forward through the loop body; it is
then checked that the obtained formula Q again implies the loop invariant P ;
for verifying the implication we apply our decision procedure from Corollary 4):
24

Example 6. Verifying the loop invariant of list reverse:
       {ls(x, nil) ∗ ls(a, nil)} (=: P )
         assume(x 6= nil)
       {ls(x, nil) ∗ ls(a, nil) ∗ x 6= nil}
         # materialization
       {x 7→ z−~(ls(x, nil) ∗ ls(a, nil) ∗ x 6= nil) ∗ x 7→ z}
         b := x.next
       {x 7→ z−~(ls(x, nil) ∗ ls(a, nil) ∗ x 6= nil) ∗ x 7→ z ∗ b = z}
         x.next := a
       {x 7→ z−~(ls(x, nil) ∗ ls(a, nil) ∗ x 6= nil) ∗ x 7→ a ∗ b = z}
         a := x
       {x 7→ z−~(ls(x, nil) ∗ ls(a0 , nil) ∗ x 6= nil) ∗ x 7→ a0 ∗ b = z ∗ a = x}
         x := b
       {x0 7→ z−~(ls(x0 , nil) ∗ ls(a0 , nil) ∗ x0 6= nil) ∗ x0 7→ a0 ∗ b = z ∗
                                                                     a = x0 ∗ x = b}(=: Q)
       {ls(x, nil) ∗ ls(a, nil)} (=: P )
Example 7. Verifying the loop invariant of list copy:
     {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s) ∗ s 7→ m} (=: P )
       assume(x 6= nil)
     {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s) ∗ s 7→ m ∗ x 6= nil}
       malloc(t)
     {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s) ∗ s 7→ m0 ∗ x 6= nil ∗ t 7→ m}
       s.next := t
     {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s) ∗ s 7→ t ∗ x 6= nil ∗ t 7→ m}
       s := t
     {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s0 ) ∗ s0 7→ t ∗ x 6= nil ∗ t 7→ m ∗ s = t}
       # materialization
     {x 7→ z−~(ls(u, x) ∗ ls(x, nil) ∗ ls(r, s0 ) ∗ s0 7→ t ∗ x 6= nil ∗ t 7→ m ∗ s = t) ∗
                                                                                  x 7→ z}
       y := x.next
     {x 7→ z−~(ls(u, x) ∗ ls(x, nil) ∗ ls(r, s0 ) ∗ s0 7→ t ∗ x 6= nil ∗ t 7→ m ∗ s = t) ∗
                                                                           x 7→ z ∗ y = z}
       x := y
     {x0 7→ z−~(ls(u, x0 ) ∗ ls(x0 , nil) ∗ ls(r, s0 ) ∗ s0 7→ t ∗
                        x0 6= nil ∗ t 7→ m ∗ s = t) ∗ x0 7→ z ∗ y = z ∗ x = y}(=: Q)
     {ls(u, x) ∗ ls(x, nil) ∗ ls(r, s) ∗ s 7→ m} (=: P )
                                                                                   25

    While our decision procedure can automatically discharge the entailments
in both of the above examples, we give a short direct argument for the ben-
efit of the reader for the entailment check of Example 6 (a direct argument
could similarly be worked out for Example 7): We note that Q0 simplifies to
Q00 = {a 7→ x−~(ls(a, nil) ∗ ls(a0 , nil)) ∗ a 7→ a0 }. Every model (s, h) of Q00 must
consist of a pointer a 7→ a0 , a list segment ls(a0 , nil) and a heap h0 to which the
pointer a 7→ x can be added in order to obtain the list segment ls(a, nil); by
looking at the semantics of the list segment predicate we see that h0 in fact must
be the list segment ls(x, nil). Further, the pointer a 7→ a0 can be composed with
the list segment ls(a0 , nil) in order to obtain ls(a, nil).


5    Normal Forms and the Abduction Problem

In this section, we discuss how every AMS can be expressed by a formula, which
in turn makes it possible to compute a normal form for every formula. We then
discuss how the normal form transformation has applications to the abduction
problem.

Normal Form. We lift the abstraction functions from stacks to sets of variables:
Let x ⊆ Var be a finite set of variables and ϕ ∈ SL be a formula with fvs(ϕ) ⊆ x.
We set αx (ϕ) := {αs (ϕ) | dom(s) = x} and   S abstx (ϕ) := αx (ϕ) ∩ AMSdϕe,x ,
where AMSk,x := {hV, E, ρ, γi ∈ AMS | V = x and γ ≤ k}. (We note that
αx (ϕ) is computable by the same argument as in the proof of Theorem 5.)

Definition 13 (Normal Form). Let NFx (ϕ) := A∈αx (ϕ) AMS2SLdϕe (A) the
                                               W

normal form of ϕ, where AMS2SLm (A) is defined as in Fig. 12.       4

   The definition of AMS2SLm (A) represents a straightforward encoding of the
AMS A: aliasing encodes the aliasing between the stack variables as implied
by V ; graph encodes the points-to assertions and lists of length at least two
corresponding to the edges E; negalloc encodes that the negative chunks R ∈ ρ
precisely allocate the variables v ∈ R; garbage ensures that there are either
exactly γ additional non-empty memory chunks that do not allocate any stack
variable (if γ < m) or at least γ such chunks (if γ = m); negalloc and garbage
use the formula negchunk which precisely encodes the definition of a negative
chunk. We have the following result about normal forms:

                        st            st
Theorem 6. NFx (ϕ) |=x ϕ and ϕ |=x NFx (ϕ).



The abduction problem. We consider the following relaxation of the entailment
problem: The abduction problem is to replace the question mark in the entailment
         st
ϕ ∗ [?] |=x ψ by a formula such that the entailment becomes true. This problem
26


AMS2SLm (A) :=aliasing(A) ∗ graph(A) ∗ negalloc(A) ∗ garbagem (A)
                                                               
  aliasing(A) :=     ∗
                   v∈V,x,y∈v
                             x = y  ∗     ∗
                                       v,w∈V,v6=w
                                                  max(v) 6
                                                         = max(w)
                                                 
    graph(A) :=       ∗        max(v) 7→ max(v0 ) ∗
                     E(v)=hv0 ,=1i
                                                                              
                                            ∗
                                         E(v)=hv0 ,≥2i
                                                         ls≥2 (max(v), max(v ))0



     negalloc(A) := ∗ negchunk(A) ∧
                                             ^                        ^
                                                   alloc(max(v)) ∧            ¬alloc(max(v))
                    R∈ρ
                                             v∈R                     v∈V \R
                    (
          m             garbage(A, γ)                                               if γ < m
 garbage (A) :=                                 V
                        garbage(A, m − 1) ∗ ¬emp v∈V ¬alloc(max(v))                 otherwise
                    (
                        emp                                                                if k = 0
garbage(A, k) :=                                         V
                        garbage(A, k − 1) ∗ negchunk(A) ∧ v∈V ¬alloc(max(v))               otherwise
 negchunk(A) :=¬emp ∧ ¬(¬emp ∗ ¬emp)∧
                                                              ^
                                                                                      ¬ϕ
                                     v,w∈V,ϕ∈{max(v)7→max(w),ls(max(v),max(w))}

        alloc(x) :=¬((x 7→ nil)−~t)
      ls≥2 (x, y) :=ls(x, y) ∧ ¬(x 7→ y)


Fig. 12: The induced formula AMS2SLm (A) of AMS A = hV, E, ρ, γi with γ ≤ m.


is central for obtaining a scalable program analyzer as discussed in [10] 9 . The
abduction problem does in general not have a unique solution. Following [10],
we thus consider optimization versions of the abduction problem, looking for
logically weakest and spatially minimal solutions:
Definition 14. Let ϕ, ψ ∈ SL and x ⊆ Var be a finite set of variables. A
                                                                        st
formula ζ is the weakest solution to the abduction problem ϕ ∗ [?] |=x ψ if it
                                                st
holds for all abduction solutions ζ 0 that ζ 0 |=x ζ. An abduction solution is ζ
                                                       st
minimal, if there is no abduction solution ζ 0 with ζ |=x ζ 0 ∗ (¬emp).
Lemma 27. Let ϕ, ψ be formulas and let x ⊆ Var be a finite set of variables.
                                                                st
Then, 1) the weakest solution to the abduction problem ϕ ∗ [?] |=x ψ is given by
the formula ϕ−∗ψ, and the 2) weakest minimal solution is given by the formula
ϕ−∗ψ ∧ ¬((ϕ−∗ψ) ∗ ¬emp).
9
     While the program analyzer proposed in [10] employs bi-abductive reasoning, the
     suggested bi-abduction procedure in fact proceeds in two separate abduction and
     frame-inference steps, where the main technical challenge is the abduction step, as
     frame inference can be incorporated into entailment checking. We believe that the
     situation for SSL is similar, i.e., solving abduction is the key to implementing a
     bi-abductive prover for SSL; hence, our focus on the abduction problem.
                                                                                 27

     We now explain how the normal form has applications to the abduction
problem. According to Lemma 27, the best solutions to the abduction problem
are given by the formulas ζ := ϕ−∗ψ and ζ 0 := ϕ−∗ψ ∧ ¬((ϕ−∗ψ) ∗ ¬emp). While
it is great that the existence of these solutions is guaranteed, we a-priori do not
have a means to compute an explicit representation of these solutions nor to
further analyze their structure. However, the normal form operator allows us to
obtain the explicit representations NFx (ζ) and NFx (ζ 0 ). We believe that using
these explicit representations in a program analyzer or studying their properties
is an interesting topic for further research. Here, we establish one concrete result
on solutions to the abduction problem based on normal forms:
     We can compute the weakest resp. the weakest minimal solution to the abduc-
tion problem from the positive fragment. Observe that among the sub-formulas of
aliasing and graph, only the formula ls≥2 is negative. To be able to use ls≥2 (x, y)
in a positive formula, we first need to add a new spatial atom ls≥2 (x, y) to SSL
with the following semantics: ls≥2 (x, y) holds in a model iff the model is a list
segment of length at least 2 from x to y. (The whole development in Sections 2
and 3 can be extended by this predicate.) We can then simplify the formula
graph(A) in AMS2SLm (A) by directly translating edges E(v) = hv0 , ≥ 2i to the
atom ls≥2 (max(v), max(v0 )). Then, hV,E,ρ,γi∈αx (ζ) with ρ=∅,γ=0 AMS2SLdϕe (A)
                                        W

for ζ = ϕ−∗ψ or ζ = ϕ−∗ψ ∧ ¬((ϕ−∗ψ) ∗ ¬emp) is the weakest resp. the weakest
minimal solution to the abduction problem from the positive fragment.



6   Conclusion


We have shown that the satisfiability problem for “strong” separation logic with
lists is in the same complexity class as the satisfiability problem for standard
“weak” separation logic without any data structures: PSpace-complete. This is
in stark contrast to the undecidability result for standard (weak) SL semantics,
as shown in [16].
    We have demonstrated the potential of SSL for program verification: 1) We
have provided symbolic execution rules that, in conjunction with our result on
the decidability of entailment, can be used for fully-automatically discharging
verification conditions. 2) We have discussed how to compute explicit represen-
tations to optimal solutions of the abduction problem. This constitutes the first
work that addresses the abduction problem for a separation logic closed under
Boolean operators and the magic wand.
    We consider the above results just the first steps in examining strong-separation
logic, motivated by the desire to circumvent the undecidability result of [16]. Fu-
ture work is concerned with the practical evaluation of our decision procedures,
with extending the symbolic execution calculus to a full Hoare logic as well as
extending the results of this paper to richer separation logics (SL) such as SL
with nested data structures or SL with limited support for arithmetic reasoning.
28

References
 1. T. Antonopoulos, N. Gorogiannis, C. Haase, M. I. Kanovich, and J. Ouaknine.
    Foundations for decision problems in separation logic with general inductive pred-
    icates. In Foundations of Software Science and Computation Structures - 17th
    International Conference, FOSSACS 2014, Held as Part of the European Joint
    Conferences on Theory and Practice of Software, ETAPS 2014, Grenoble, France,
    April 5-13, 2014, Proceedings, pages 411–425. Springer Berlin Heidelberg, 2014.
 2. A. W. Appel. Program Logics - for Certified Compilers. Cambridge University
    Press, 2014.
 3. J. Berdine, C. Calcagno, and P. W. O’Hearn. A decidable fragment of separa-
    tion logic. In FSTTCS 2004: Foundations of Software Technology and Theoretical
    Computer Science, 24th International Conference, Chennai, India, December 16-
    18, 2004, Proceedings, pages 97–109. Springer, 2004.
 4. J. Berdine, C. Calcagno, and P. W. O’Hearn. Symbolic execution with separation
    logic. In Programming Languages and Systems, Third Asian Symposium, APLAS
    2005, Tsukuba, Japan, November 2-5, 2005, Proceedings, pages 52–68. 2005.
 5. J. Berdine, B. Cook, and S. Ishtiaq. Slayer: Memory safety for systems-level code.
    In Computer Aided Verification - 23rd International Conference, CAV 2011, Snow-
    bird, UT, USA, July 14-20, 2011. Proceedings, pages 178–183, 2011.
 6. S. Blom and M. Huisman. Witnessing the elimination of magic wands. Interna-
    tional Journal on Software Tools for Technology Transfer, 17(6):757–781, 2015.
 7. R. Bornat, C. Calcagno, P. W. O’Hearn, and M. J. Parkinson. Permission ac-
    counting in separation logic. In Proceedings of the 32nd ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, POPL 2005, Long Beach,
    California, USA, January 12-14, 2005, pages 259–270, 2005.
 8. R. Brochenin, S. Demri, and E. Lozes. On the almighty wand. Information and
    Computation, 211:106 – 137, 2012.
 9. C. Calcagno, D. Distefano, J. Dubreil, D. Gabi, P. Hooimeijer, M. Luca,
    P. O’Hearn, I. Papakonstantinou, J. Purbrick, and D. Rodriguez. Moving fast
    with software verification. In K. Havelund, G. Holzmann, and R. Joshi, editors,
    NASA Formal Methods: 7th International Symposium, NFM 2015, Pasadena, CA,
    USA, April 27-29, 2015, Proceedings, pages 3–11, Cham, 2015. Springer Interna-
    tional Publishing.
10. C. Calcagno, D. Distefano, P. W. O’Hearn, and H. Yang. Compositional shape
    analysis by means of bi-abduction. J. ACM, 58(6):26:1–26:66, Dec. 2011.
11. C. Calcagno, P. O’Hearn, and H. Yang. Local action and abstract separation logic.
    In Logic in Computer Science, 2007. LICS 2007. 22nd Annual IEEE Symposium
    on, pages 366–378, July 2007.
12. C. Calcagno, H. Yang, and P. O’Hearn. Computability and complexity results
    for a spatial assertion language for data structures. In R. Hariharan, V. Vinay,
    and M. Mukund, editors, FST TCS 2001: Foundations of Software Technology and
    Theoretical Computer Science, volume 2245 of Lecture Notes in Computer Science,
    pages 108–119. Springer Berlin Heidelberg, 2001.
13. B. Cook, C. Haase, J. Ouaknine, M. J. Parkinson, and J. Worrell. Tractable rea-
    soning in a fragment of separation logic. In CONCUR 2011 - Concurrency Theory
    - 22nd International Conference, CONCUR 2011, Aachen, Germany, September
    6-9, 2011. Proceedings, pages 235–249, 2011.
14. S. Demri and M. Deters. Expressive completeness of separation logic with two
    variables and no separating conjunction. In Proceedings of the Joint Meeting of the
                                                                                      29

    Twenty-Third EACSL Annual Conference on Computer Science Logic (CSL) and
    the Twenty-Ninth Annual ACM/IEEE Symposium on Logic in Computer Science
    (LICS), CSL-LICS ’14, pages 37:1–37:10, New York, NY, USA, 2014. ACM.
15. S. Demri, D. Galmiche, D. Larchey-Wendling, and D. Méry. Separation logic with
    one quantified variable. In E. Hirsch, S. Kuznetsov, J.-É. Pin, and N. Vereshchagin,
    editors, Computer Science - Theory and Applications, volume 8476 of Lecture Notes
    in Computer Science, pages 125–138. Springer International Publishing, 2014.
16. S. Demri, É. Lozes, and A. Mansutti. The effects of adding reachability predicates
    in propositional separation logic. In C. Baier and U. Dal Lago, editors, Foun-
    dations of Software Science and Computation Structures, pages 476–493, Cham,
    2018. Springer International Publishing.
17. K. Dudka, P. Peringer, and T. Vojnar. Predator: A practical tool for checking
    manipulation of dynamic data structures using separation logic. In Computer Aided
    Verification - 23rd International Conference, CAV 2011, Snowbird, UT, USA, July
    14-20, 2011. Proceedings, pages 372–378, 2011.
18. M. Echenim, R. Iosif, and N. Peltier. The bernays-schönfinkel-ramsey class of sepa-
    ration logic on arbitrary domains. In M. Bojańczyk and A. Simpson, editors, Foun-
    dations of Software Science and Computation Structures, pages 242–259, Cham,
    2019. Springer International Publishing.
19. N. Gorogiannis, M. Kanovich, and P. W. O’Hearn. The complexity of abduction
    for separated heap abstractions. In E. Yahav, editor, Static Analysis: 18th Interna-
    tional Symposium, SAS 2011, Venice, Italy, September 14-16, 2011. Proceedings,
    pages 25–42, Berlin, Heidelberg, 2011. Springer Berlin Heidelberg.
20. X. Gu, T. Chen, and Z. Wu. A complete decision procedure for linearly com-
    positional separation logic with data constraints. In Automated Reasoning - 8th
    International Joint Conference, IJCAR 2016, Coimbra, Portugal, June 27 - July
    2, 2016, Proceedings, pages 532–549, 2016.
21. R. Iosif, A. Rogalewicz, and J. Simácek. The tree width of separation logic with
    recursive definitions. In Automated Deduction - CADE-24 - 24th International
    Conference on Automated Deduction, Lake Placid, NY, USA, June 9-14, 2013.
    Proceedings, pages 21–38, 2013.
22. R. Iosif, A. Rogalewicz, and T. Vojnar. Deciding entailments in inductive sep-
    aration logic with tree automata. In Automated Technology for Verification and
    Analysis - 12th International Symposium, ATVA 2014, Sydney, NSW, Australia,
    November 3-7, 2014, Proceedings, pages 201–218, 2014.
23. S. S. Ishtiaq and P. W. O’Hearn. BI as an assertion language for mutable data struc-
    tures. In Conference Record of POPL 2001: The 28th ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, London, UK, January 17-
    19, 2001, pages 14–26, 2001.
24. B. Jacobs, J. Smans, P. Philippaerts, F. Vogels, W. Penninckx, and F. Piessens.
    Verifast: A powerful, sound, predictable, fast verifier for C and java. In NASA
    Formal Methods - Third International Symposium, NFM 2011, Pasadena, CA,
    USA, April 18-20, 2011. Proceedings, pages 41–55, 2011.
25. J. Katelaan, D. Jovanović, and G. Weissenbacher. A separation logic with data:
    Small models and automation. In D. Galmiche, S. Schulz, and R. Sebastiani,
    editors, Automated Reasoning, pages 455–471, Cham, 2018. Springer International
    Publishing.
26. J. Katelaan, C. Matheja, and F. Zuleger. Effective entailment checking for sep-
    aration logic with inductive definitions. In Tools and Algorithms for the Con-
    struction and Analysis of Systems - 25th International Conference, TACAS 2019,
30

    Held as Part of the European Joint Conferences on Theory and Practice of Soft-
    ware, ETAPS 2019, Prague, Czech Republic, April 6-11, 2019, Proceedings, Part
    II, pages 319–336, 2019.
27. J. Katelaan and F. Zuleger. Beyond symbolic heaps: Deciding separation logic with
    inductive definitions. In E. Albert and L. Kovács, editors, LPAR 2020: 23rd Inter-
    national Conference on Logic for Programming, Artificial Intelligence and Reason-
    ing, Alicante, Spain, May 22-27, 2020, volume 73 of EPiC Series in Computing,
    pages 390–408. EasyChair, 2020.
28. Q. L. Le, M. Tatsuta, J. Sun, and W. Chin. A decidable fragment in separation
    logic with inductive predicates and arithmetic. In Computer Aided Verification -
    29th International Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017,
    Proceedings, Part II, pages 495–517, 2017.
29. P. Madhusudan, G. Parlato, and X. Qiu. Decidable logics combining heap struc-
    tures and data. In Proceedings of the 38th Annual ACM SIGPLAN-SIGACT Sym-
    posium on Principles of Programming Languages, POPL ’11, pages 611–622, New
    York, NY, USA, 2011. ACM.
30. P. W. O’Hearn. Resources, concurrency, and local reasoning. Theor. Comput. Sci.,
    375(1-3):271–307, 2007.
31. J. Pagel. Decision Procedures for Separation Logic: Beyond Symbolic Heaps. PhD
    thesis, TU Wien, 2020. https://repositum.tuwien.at/handle/20.500.12708/
    16333.
32. J. Pagel, C. Matheja, and F. Zuleger. Complete entailment checking for separation
    logic with inductive definitions. CoRR, abs/2002.01202, 2020.
33. J. Pagel and F. Zuleger. Strong-separation logic. CoRR, abs/2001.06235, 2020.
34. J. A. N. Pérez and A. Rybalchenko. Separation logic modulo theories. In Program-
    ming Languages and Systems - 11th Asian Symposium, APLAS 2013, Melbourne,
    VIC, Australia, December 9-11, 2013. Proceedings, pages 90–106. 2013.
35. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic using SMT. In
    N. Sharygina and H. Veith, editors, Computer Aided Verification, volume 8044 of
    Lecture Notes in Computer Science, pages 773–789. Springer Berlin Heidelberg,
    2013.
36. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic with trees and
    data. In Computer Aided Verification - 26th International Conference, CAV 2014,
    Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna, Austria, July
    18-22, 2014. Proceedings, pages 711–728, 2014.
37. X. Qiu, P. Garg, A. Stefanescu, and P. Madhusudan. Natural proofs for structure,
    data, and separation. In ACM SIGPLAN Conference on Programming Language
    Design and Implementation, PLDI ’13, Seattle, WA, USA, June 16-19, 2013, pages
    231–242, 2013.
38. A. Reynolds, R. Iosif, and C. Serban. Reasoning in the bernays-schönfinkel-ramsey
    fragment of separation logic. In Verification, Model Checking, and Abstract Inter-
    pretation - 18th International Conference, VMCAI 2017, Paris, France, January
    15-17, 2017, Proceedings, pages 462–482, 2017.
39. A. Reynolds, R. Iosif, C. Serban, and T. King. A decision procedure for separation
    logic in smt. In C. Artho, A. Legay, and D. Peled, editors, Automated Technology
    for Verification and Analysis, pages 244–261, Cham, 2016. Springer International
    Publishing.
40. J. C. Reynolds. Separation logic: A logic for shared mutable data structures. In
    17th IEEE Symposium on Logic in Computer Science (LICS 2002), 22-25 July
    2002, Copenhagen, Denmark, Proceedings, pages 55–74, 2002.
                                                                                               31

41. M. Schwerhoff and A. J. Summers. Lightweight support for magic wands in an
    automatic verifier. In 29th European Conference on Object-Oriented Programming,
    ECOOP 2015, July 5-10, 2015, Prague, Czech Republic, pages 614–638, 2015.
42. M. Tatsuta and D. Kimura. Separation logic with monadic inductive definitions
    and implicit existentials. In Programming Languages and Systems - 13th Asian
    Symposium, APLAS 2015, Pohang, South Korea, November 30 - December 2, 2015,
    Proceedings, pages 69–89, 2015.


Appendix
Isomorphism. SL formulas cannot distinguish isomorphic models:

Definition 15. Let (s, h), (s0 , h0 ) be models. (s, h) and (s0 , h0 ) are isomorphic,
(s, h) ∼
       = (s0 , h0 ), if there exists a bijection σ : (locs(h) ∪ img(s)) → (locs(h0 ) ∪
img(s )) such that (1) for all x, s0 (x) = σ(s(x)) and (2) h0 = {σ(l) 7→ σ(h(l)) |
      0

l ∈ dom(h)}.                                                                        4

Lemma 28. Let (s, h), (s0 , h0 ) be models with (s, h) ∼
                                                       = (s0 , h0 ) and let ϕ ∈ SL.
             st        0   0 st
Then (s, h) |= ϕ iff (s , h ) |= ϕ.

Proof. We prove the claim by induction on the structure of the formula ϕ.
Clearly, the claim holds for the base cases emp, x 7→ y, ls(x, y), x = y and
x 6= y. Further, the claim immediately follows from the induction assumption
for the cases ϕ1 ∧ ϕ2 , ϕ1 ∨ ϕ2 and ¬ϕ. It remains to consider the cases ϕ1 ∗ ϕ2
and ϕ1 −~ϕ2 . Let (s, h) and (s0 , h0 ) be two stack-heap pairs with (s, h) ∼        = (s0 , h0 ).
                                      st                         0    0     st
    We will show that (s, h) |= ϕ1 ∗ ϕ2 implies (s , h ) |= ϕ1 ∗ ϕ2 ; the other
                                                                           st
direction is completely symmetric. We assume that (s, h) |= ϕ1 ∗ ϕ2 . Then, there
                                                     st
are h1 , h2 with h1 ]s h2 = h and (s, hi ) |= ϕi for i = 1, 2. We consider the
bijection σ that witnesses the isomorphism between (s, h) and (s0 , h0 ). Let h01
resp. h02 be the sub-heap of h0 restricted to σ(dom(h1 )) resp. σ(dom(h2 )). It is
easy to verify that h01 ]s h02 = h0 and (s, hi ) ∼   = (s0 , h0i ) for i = 1, 2. Hence, we can
                                                                    st
apply the induction assumption and get that (s0 , h0i ) |= ϕi for i = 1, 2. Because
                                         st
of h01 ]s h02 = h0 we get (s0 , h0 ) |= ϕ1 ∗ ϕ2 .
                                     st                                     st
    We will show that (s, h) |= ϕ1 −~ϕ2 implies (s0 , h0 ) |= ϕ1 −~ϕ2 ; the other
                                                                        st
direction is completely symmetric. We assume that (s, h) |= ϕ1 −~ϕ2 . Hence there
                               st                       st
is a heap h0 with (s, h0 ) |= ϕ1 and (s, h0 ]s h) |= ϕ2 . We note that in particular
     s
h0 ] h 6= ⊥. We consider the bijection σ that witnesses the isomorphism between
(s, h) and (s0 , h0 ). Let L ⊆ Loc be some subset of locations with L ∩ (locs(h0 ) ∪
img(s0 )) = ∅ and |L| = locs(h0 ) \ (locs(h) ∪ img(s)). We can extend σ to some
bijective function σ 0 : (locs(h0 ) ∪ locs(h) ∪ img(s)) → (L ∪ locs(h0 ) ∪ img(s0 )).
Then, σ 0 induces a heap h00 such that (s, h0 ) ∼          = (s0 , h00 ), h00 ]s h0 6= ⊥ and
(s, h0 ]s h) ∼
                                                                                          st
               = (s0 , h00 ]s h0 ). By induction assumption we get that (s0 , h00 ) |= ϕ1
                       st                        st
and (s0 , h00 ]s h0 ) |= ϕ2 . Hence, (s0 , h0 ) |= ϕ1 −~ϕ2 .
32

A    Proofs for Section 2 (Strong- and Weak-Separation
     Logic)

Proof. (Lemma 1.) Trivially, the operation ]s is commutative and associative
with unit u. Let h ∈ H. Consider h1 , h2 ∈ H such that h ]s h1 = h ]s h2 6= ⊥.
Since the domain of h is disjoint from the domains of h1 and h2 , it follows that
for all x, h1 (x) = h2 (x) and thus h1 = h2 . As h1 and h2 were chosen arbitrarily,
we obtain that the function h ]s (·) is injective. Consequently, the monoid is
cancellative.

Proof. (Lemma 2.) We prove the following stronger statement by structural
                                        wk
induction on ϕ: For every model (s, h) |= ϕ we have that

 1. (img(h) \ dom(h)) ⊆ img(s),
 2. every join point is labelled by a variable, i.e., h−1 (`) ≥ 2 implies that
    ` ∈ img(s), and
 3. every source is labelled by a variable, i.e., h(`) 6= ⊥ and h−1 (`) = 0 imply
    that ` ∈ img(s).
                                                                          wk
The proof is straightforward except for the −~ case: Assume (s, h) |= ϕ1 −~ϕ2 .
                                  wk                    wk
Then there is a h0 with (s, h0 ) |= ϕ1 and (s, h0 + h) |= ϕ2 . By induction assump-
tion the claim holds for (s, h0 ) and (s, h0 + h). We note that every join point of
h is also a join point of h0 + h and hence labelled by a variable. We now verify
that every pointer that is dangling in h is either also dangling in h0 + h or is a
join point in h0 + h or is pointing to a source of h0 ; in all cases the target of the
dangling pointer is labelled by a variable. Finally, a source of h is either also a
source of h0 + h or is pointed to by a dangling pointer of h0 ; in both cases the
source is labelled by a variable.

Proof. (Lemma 3.) If h1 ]s h2 6= ⊥, then h1 + h2 6= ⊥ by definition.
   Conversely, assume h1 + h2 6= ⊥. We need to show that locs(h1 ) ∩ locs(h2 ) ⊆
img(s). To this end, let l ∈ locs(h1 ) ∩ locs(h2 ). Then there exists an i ∈ {1, 2}
such that i ∈ img(hi ) \ dom(hi )—otherwise l would be in dom(h1 ) ∩ dom(h2 )
and h1 + h2 = ⊥. By Lemma 2, we thus have l ∈ img(s).

Proof. (Lemma 4.) We proceed by structural induction on ϕ. If ϕ is atomic,
there is nothing to show. For ϕ = ϕ1 ∗ ϕ2 and ϕ = ϕ1 −~ϕ2 , the claim follows
from the induction hypotheses and Lemma 3. For ϕ = ϕ1 ∧ ϕ2 and ϕ = ϕ1 ∨ ϕ2 ,
the claim follows immediately from the induction hypotheses and the semantics
of ∧, ∨.


B    Proofs for Section 3 (Deciding the SSL Satisfiability
     Problem)

Proof. (Lemma 5.) For simplicity, we assume Loc = N; this allows us to add
locations.
                                                                                               33

   Let n := |V |. We fix some injective
                                S       function t : V → {1, . . . , n} from nodes to
natural numbers. We set s := x∈v,v∈V {x 7→ t(v)} and define h as the (disjoint)
union of
 – E(v)=hv0 ,=1i {t(v) 7→ t(v 0 )}
    S

 – E(v)=hv0 ,≥2i {t(v) 7→ n + t(v), n + t(v) 7→ t(v 0 )}
    S
    S
 – Sv∈r,r∈ρ {t(v) 7→ 2n + t(max(r))}
 – l∈{3n+1,...,3n+γ} {l 7→ l}

It is easy to verify that ams(s, h) = A and that |h| ∈ O(|A|).

Proof. (Lemma 6.) The lemma can be proved by a straight-forward induction
on ϕ, using that every heap fully decomposes into its chunks.

Proof. (Lemma 7.) Let A ∈ αs (ϕ). Then there exists a heap h such that
ams(s, h) = A and (s, h) |= ϕ. Let h0 be such that (s, h) ∼
                          st
                                                          = (s0 , h0 ). By Lemma 28,
  0   0   st                   0  0
(s , h ) |= ϕ. Moreover, ams(s , h ) = A. Consequently, A ∈ αs0 (ϕ). The other
direction is proved analogously.
                                 st
Proof. (Lemma 8.) (s, h) |= emp iff h = ∅ iff chunks(s, h) = ∅ iff ams(s, h) =
hcls= (s), ∅, ∅, 0i.

Proof. (Lemma 9.) We only show the first claim, as the proof of the second
claim is completely analogous. (s, h) |= x = y iff (s(x) = s(y) and h = ∅) iff
    s         s                                       s     s
([x]= = [y]= and (s, h) |= emp) iff, by Lemma 8, ([x]= = [y]= and ams(s, h) =
hcls= (s), ∅, ∅, 0i).
                                      st
Proof. (Lemma 10.) If (s, h) |= x 7→ y then h = {s(x) 7→ s(y)}. In particular, it
then holds that h is a positive chunk. Consequently, edges(s, h) = E. It follows
that ams(s, h) = hcls= (s), E, ∅, 0i.
    Conversely, assume ams(s, h) = hcls= (s), E, ∅, 0i. Then, (s, h) consists of
a single positive chunk and no negative chunks. Further, by the definition of
edges(s, h) we have that this single positive chunk satisfies (s, h) |= x 7→ y.

Proof. (Lemma 11.) Assume (s, h) |= ls(x, y). By the semantics, there ex-
ist locations `0 , . . . , `n , n ≥ 1, with s(x) = `0 , s(y) = `n and h = {`0 7→
`1 , . . . , `n−1 7→ `n }. Let j1 , . . . , jk those indices among 1, . . . , n with `ji ∈ img(s).
(In particular, j1 = 1 and jk = n.) Then for each ji , the restriction of h to
`ji , `ji +1 , . . . , `ji+1 −1 is a positive chunk that either satisfies a points-to asser-
tion or a list-segment predicate. Hence, edges(s, h)(s−1 (`ji )) = s−1 (`ji+1 ), ιi
for all 1 ≤ i < k, for some ιi ∈ {= 1, ≥ 2}. Thus, ams(s, h) ∈ AbstLists(x, y).
      Assume ams(s, h) ∈ AbstLists(x, y). Then, there are equivalence classes
      s                 s
[x1 ]= , . . . , [xn ]= ∈ cls= (s) and labels ι1 , . . . , ιn−1 ∈ {= 1, ≥ 2} such that x ∈
      s                   s                             s           s
[x1 ]= , y ∈ [xn ]= and edges(s, h) = {[xi ]= 7→ h[xi+1 ]= , ιi i | 1 ≤ i < n}. By
the definition of edges(s, h), we have that there are positive chunks hi of h
                              st                            st
such that (s, hi ) |= xi 7→ xi+1 or (s, hi ) |= ls(xi , xi+1 ). In particular, we
have hi = {`i,1 7→ `i,2 , . . . , `i,ki −1 7→ `i,ki } , s(xi ) = `i,1 and s(xi+1 ) = `i,ki for
34

some locations `i,j Because h does not have negative chunks, we get that h
fully decomposes into its positive chunks. Hence, the locations `i,j witness that
(s, h) |= ls(x, y).

Proof. (Lemma 12.) Since the same stack s underlies both abstractions, we
have V1 = V2 . Furthermore, dom(h1 ) ∩ dom(h2 ) = ∅ implies that alloc(A1 ) ∩
alloc(A2 ) = ∅.

Proof. (Lemma 13.) The result follows easily from the observation that

               chunks(s, h1 ]s h2 ) = chunks(s, h1 ) ∪ chunks(s, h2 ),

which, in turn, is an immediate consequence of Proposition 2.

Proof. (Lemma 14.) It can be verified from the definition of AMS and the def-
inition of the composition operator • that the following property holds: Let
hc ∈ chunks(s, h) be a chunk. Then, either there exists an A01 such that A1 =
ams(s, hc ) • A01 or there exists an A02 such that A2 = ams(s, hc ) • A02 .
    The claim can then by proven an induction of the number of chunks |chunks(s, h)|.

Proof. (Theorem 2.) Let A = hV, E, ρ, γi be the AMS with ams(s, h1 ) = A =
ams(s, h2 ). We proceed by induction on the structure of ϕ. We only prove that
          st                         st
(s, h1 ) |= ϕ implies that (s, h2 ) |= ϕ, as the other direction is completely analo-
gous.
    Assume that the claim holds for all subformulas of ϕ and assume that
          st
(s, h1 ) |= ϕ.

Case emp, x = y, x 6= y, x 7→ y, ls(x, y). Immediate consequence of Lemmas 8, 9, 10
   and 11.
Case ϕ1 ∗ ϕ2 . By the semantics of ∗, there exist h1,1 , h1,2 with h1 = h1,1 ]s
                      st                     st
   h1,2 , (s, h1,1 ) |= ϕ1 , and (s, h1,2 ) |= ϕ2 . Let A1 := ams(s, h1,1 ) and A2 :=
   ams(s, h1,2 ). By Lemma 13, ams(s, h1 ) = A1 • A2 = ams(s, h2 ). We can
   thus apply Lemma 14 to ams(s, h2 ), A1 , and A2 to obtain heaps h2,1 , h2,2
   with h2 = h2,1 ]s h2,2 , ams(s, h2,1 ) = A1 and ams(s, h2,2 ) = A2 . We can
   now apply the induction hypotheses for 1 ≤ i ≤ 2, ϕi , h1,i and h2,i , and
                               st
   obtain that (s, h2,i ) |= ϕi . By the semantics of ∗, we then have (s, h2 ) =
                         st
   (s, h2,1 ]s h2,2 ) |= ϕ1 ∗ ϕ2 .
                                     st                                           st
Case ϕ1 −~ϕ2 . Since (s, h1 ) |= ϕ1 −~ϕ2 , there exists a heap h0 with (s, h0 ) |= ϕ1
                            st
   and (s, h1 ]s h0 ) |= ϕ2 . We can assume w.l.o.g. that h2 ]s h0 6= ⊥—if this
   is not the case, simply replace h0 with a heap h00 with (s, h0 ) ∼        = (s, h00 ),
                                                             st
   h1 ]s h00 6= ⊥ and h2 ]s h00 6= ⊥; then, (s, h1 ]s h00 ) |= ϕ2 by Lemma 28. We have
   that ams(s, h1 ]s h0 ) = ams(s, h1 ) • ams(s, h0 ) = ams(s, h2 ) • ams(s, h0 ) =
   ams(s, h2 ]s h0 ) (by assumption and Lemma 13). It therefore follows from
   the induction hypothesis for ϕ2 , (s, h1 ]s h0 ), and (s, h2 ]s h0 ) that (s, h2 ]s
         st                       st
   h0 ) |= ϕ2 . Thus, (s, h2 ) |= ϕ1 −~ϕ2 .
                                                                                      35

                                                                                 st
Case ϕ1 ∧ ϕ2 , ϕ1 ∨ ϕ2 . By the semantics of ∧ resp. ∨, we have (s, h1 ) |= ϕ1
                       st
   and/or (s, h1 ) |= ϕ2 . We apply the induction hypotheses for ϕ1 and ϕ2 to
                     st                   st
   obtain (s, h2 ) |= ϕ1 and/or (s, h2 ) |= ϕ2 . By the semantics of ∧ resp. ∨, we
                          st                     st
   then have (s, h2 ) |= ϕ1 ∧ ϕ2 resp. (s, h2 ) |= ϕ1 ∨ ϕ2 .
                                                           st
Case ¬ϕ1 . By the semantics of ¬, we have (s, h1 ) |=     6 ϕ1 . By the induction
                                                    st
   hypothesis for ϕ1 we then obtain (s, h2 ) |=   6 ϕ1 . By the semantics of ¬, we
                  st
   have (s, h2 ) |= ¬ϕ1 .

Proof. (Corollary 1.) Assume A := ams(s, h) ∈ αs (ϕ). By definition of αs there
                                   st
is a model (s, h0 ) with (s, h0 ) |= ϕ and ams(s, h0 ) = A. By applying Theorem 2
                                                    st
to ϕ, (s, h) and (s, h0 ), we then get that (s, h) |= ϕ.
                                                         st                      st
Proof. (Lemma 15.) Let (s, h) be a model. (s, h) |= ϕ1 ∧ ϕ2 iff (s, h) |= ϕ1
             st
and (s, h) |= ϕ2 iff ams(s, h) ∈ αs (ϕ1 ) and ams(s, h) ∈ αs (ϕ2 ) iff ams(s, h) ∈
αs (ϕ1 ) ∩ αs (ϕ2 ).
                                                         st                      st
Proof. (Lemma 16.) Let (s, h) be a model. (s, h) |= ϕ1 ∧ ϕ2 iff ((s, h) |= ϕ1
           st
or (s, h) |= ϕ2 ) iff (ams(s, h) ∈ αs (ϕ1 ) or ams(s, h) ∈ αs (ϕ2 )) iff ams(s, h) ∈
αs (ϕ1 ) ∪ αs (ϕ2 ).
                                                    st
Proof. Lemma 17. Let (s, h) be a model. (s, h) |= ¬ϕ1 iff it is not the case that
        st
(s, h) |= ϕ1 iff it is not the case that ams(s, h) ∈ αs (ϕ1 ) iff it is the case that
ams(s, h) ∈ {ams(s, h) | h ∈ H} \ αs (ϕ1 ).

Proof. (Lemma 18.) Let A ∈ αs (ϕ1 ∗ ϕ2 ). There then exists a heap h such that
         st
(s, h) |= ϕ1 ∗ ϕ2 and ams(s, h) = A. By the semantics of ∗, we can split h
                             st
into h1 ]s h2 with (s, hi ) |= ϕi (and thus ams(s, hi ) ∈ αs (ϕi )). By Lemma 13,
A = ams(s, h1 )•ams(s, h2 ) for h1 , h2 as above. Consequently, A ∈ αs (ϕ1 )•αs (ϕ2 )
by definition of •.
    Conversely, let A ∈ αs (ϕ1 ) • αs (ϕ2 ). By definition of •, there then exist Ai ∈
                                                                                   st
αs (ϕi ) such that A = A1 • A2 . Let h1 , h2 be witnesses of that, i.e., (s, hi ) |= ϕi
with ams(s, hi ) = Ai . Assume w.l.o.g. that h1 ]s h2 6= ⊥. (Otherwise, replace h2
with an h02 such that (s, h2 ) ∼= (s, h02 ) and h1 ]s h02 6= ⊥; by Lemma 28 we then
            0   st                                               st
have (s, h2 ) |= ϕ2 .) By the semantics of ∗, (s, h1 ]s h2 ) |= ϕ1 ∗ ϕ2 . Therefore,
ams(s, h1 ] h2 ) ∈ αs (ϕ1 ∗ ϕ2 ). By Lemma 13, ams(s, h1 ]s h2 ) = A. The claim
              s

follows.

Proof. (Lemma 19.) Let A ∈ αs (ϕ1 −~ϕ2 ). Then there exists a model (s, h) with
                           st
ams(s, h) = A and (s, h) |= ϕ1 −~ϕ2 . Consequently, there exists a heap h1 such
                              st                      st
that h ]s h1 6= ⊥, (s, h1 ) |= ϕ1 and (s, h ]s h1 ) |= ϕ2 . By definition of αs ,
                                                   s
we then have ams(s, h1 ) ∈ αs (ϕ1 ) and ams(s, h ] h1 ) ∈ αs (ϕ2 ). By Lemma 13,
ams(s, h]s h1 ) = ams(s, h)•ams(s, h1 ). In other words, we have for A = ams(s, h)
and A1 := ams(s, h1 ) that A1 ∈ αs (ϕ1 ) and A • A1 ∈ αs (ϕ2 ). By definition of
−•, we hence have A ∈ αs (ϕ1 )−•αs (ϕ2 ).
36

    Conversely, let A ∈ αs (ϕ1 )−•αs (ϕ2 ). Then there exists an A1 ∈ αs (ϕ1 ) such
that A • A1 ∈ αs (ϕ2 ). Let h, h1 be heaps with ams(s, h) = A, ams(s, h1 ) = A1
              st
and (s, h1 ) |= ϕ1 . Assume w.l.o.g. that h ]s h1 6= ⊥. (Otherwise, replace h1 with
an h01 such that (s, h1 ) ∼
                          = (s, h01 ) and h ]s h01 6= ⊥; by Lemma 28 we then have
     0    st
(s, h1 ) |= ϕ1 .)
    By Lemma 13, we then have ams(s, h ]s h1 ) = A • A1 . By Cor. 1, this allows
                                     st                         st
us to conclude that (s, h ]s h1 ) |= ϕ2 . Consequently, (s, h) |= ϕ1 −~ϕ2 , implying
A ∈ αs (ϕ1 −~ϕ2 ).

Proof. (Theorem 3.) We proceed by structural induction on ϕ. We only prove
               st                    st
that (s, h1 ) |= ϕ implies (s, h2 ) |= ϕ, as the proof of the other direction is very
similar.

Case emp, x = y, x 6= y, x 7→ y, ls(x, y). By Lemmas 8, 9, 10 and 11 we have
   that the AMS of all models of ϕ have a garbage-chunk count of 0. Thus,
              st                 st
   (s, h1 ) 6|= ϕ and (s, h2 ) 6|= ϕ.
                                       st
Case ϕ1 ∗ ϕ2 . Assume (s, h1 ) |= ϕ1 ∗ ϕ2 . Let h1,1 , h1,2 be such that h1 =
                              st                     st
   h1,1 ]s h1,2 , (s, h1,1 ) |= ϕ1 , and (s, h1,2 ) |= ϕ2 . Let A1 = hV1 , E1 , ρ1 , m1 i :=
   ams(h1,1 ) and A2 = hV2 , E2 , ρ2 , m2 i := ams(h1,2 ). Since k = dϕ1 e + dϕ2 e, it
   follows that, either m1 ≥ dϕ1 e or m2 ≥ dϕ2 e (or both). Assume w.l.o.g. that
   m1 ≥ dϕ1 e and let A01 := hV1 , E1 , ρ1 , n − min{dϕ2 e, m2 }i. Observe that
   ams(s, h2 ) = A01 • A2 . There thus exist by Lemma 14 heaps h2,1 , h2,2 such
   that (s, h2 ) = h2,1 ]s h2,2 , ams(s, h2,1 ) = A01 and ams(s, h2,1 ) = A2 . As both
   m1 ≥ dϕ1 e and n − min{dϕ2 e, m2 } ≥ k − min{dϕ2 e, m2 } ≥ dϕ1 e, we have by
                                                            st
   the induction hypothesis for ϕ1 that (s, h2,1 ) |= ϕ1 . Additionally, we have
         st
   h2,2 |= ϕ2 by Theorem 2 (for m2 < dϕ2 e) or by the induction hypothesis (for
                                             st
   m2 ≥ dϕ2 e). Consequently, (s, h2 ) |= ϕ1 ∗ ϕ2 .
                                       st                                             st
Case ϕ1 −~ϕ2 . Assume (s, h1 ) |= ϕ1 −~ϕ2 . Let h0 be such that (s, h0 ) |= ϕ1
                         st
   and (s, h1 ]s h0 ) |= ϕ2 . We can assume w.l.o.g. that h2 ]s h0 6= ⊥—if this
   is not the case, simply replace h0 with a heap h00 with (s, h0 ) ∼           = (s, h00 ),
        s 0                       s 0                          s 0    st
   h1 ] h0 6= ⊥ and h2 ] h0 6= ⊥; then, (s, h1 ] h0 ) |= ϕ2 by Lemma 28.
   We set A2 = ams(s, h1 ]s h0 ) and A02 = ams(s, h2 ]s h0 ). By Lemma 13
   we have ams(s, h1 ]s h0 ) = ams(s, h1 ) • ams(s, h0 ) and ams(s, h2 ]s h0 ) =
   ams(s, h2 )•ams(s, h0 ). Hence, A2 = hV2 , E2 , ρ2 , m0 i and A02 = hV2 , E2 , ρ2 , n0 i
   for some V2 , E2 , ρ2 and m0 , n0 ≥ k = dϕ1 −~ϕ2 e = dϕ2 e. It thus follows from
                                                                st
   the induction hypothesis for ϕ2 that (s, h0 ]s h2 ) |= ϕ2 .
                                                        st                   st
Case ϕ1 ∧ ϕ2 , ϕ1 ∨ ϕ2 . We then have (s, h1 ) |= ϕ1 and/or (s, h1 ) |= ϕ2 . By def-
   inition of dϕ1 ∧ ϕ2 e resp. dϕ1 ∨ ϕ2 e, it follows that n, m ≥ max(dϕ1 e, dϕ2 e) ≥
                                                                                       st
   dϕi e. We therefore conclude from the induction hypothesis that (s, h2 ) |= ϕ1
                     st                      st                           st
   and/or (s, h2 ) |= ϕ2 . Thus, (s, h2 ) |= ϕ1 ∧ ϕ2 resp. (s, h2 ) |= ϕ1 ∨ ϕ2 .
                                    st                                 st
Case ¬ϕ1 . Assume (s, h1 ) |= ¬ϕ1 . Consequently, (s, h1 ) 6|= ϕ1 . Since m, n ≥
                                                                   st                      st
   d¬ϕ1 e = dϕ1 e, it follows by induction that (s, h2 ) 6|= ϕ1 . Then, (s, h2 ) |=
   ¬ϕ1 .
                                                                                      37

Proof. (Corollary 2.) Assume ϕ is satisfiable and let (s, h) be a model with
        st
(s, h) |= ϕ. Let A = hV, E, ρ, γi := ams(s, h). If γ ≤ k, there is nothing to show.
Otherwise, let A0 := hV, E, ρ, ki. By Lemma 5, we can choose a heap h0 with
                                           st
ams(s, h0 ) = A0 . By Theorem 3, (s, h0 ) |= ϕ.

Proof. (Theorem 4.) We proceed by induction on the structure of ϕ:
Case emp, x = y, x 6= y, x 7→ y, ls(x, y). By Lemmas 8, 9, 10 and 11 and the
   observation that all models of ϕ have garbage-chunk count of 0.
Case ϕ1 ∗ ϕ2 . By the induction hypotheses, we have for 1 ≤ i ≤ 2 that absts (ϕi ) =
   αs (ϕi ) ∩ AMSdϕi e,s Let Ai := liftdϕ1 e%dϕ1 ∗ϕ2 e (absts (ϕi )). By Theorem 3, it
   follows that Ai = αs (ϕi )∩AMSdϕ1 ∗ϕ2 e,s . By Lemma 18, it thus follows that
   A1 • A2 contains all AMS in αs (ϕ1 ∗ ϕ2 ) that can be obtained by composing
   AMS with a garbage-chunk count of at most dϕi ∗ ϕ2 e. Thus, in particular,
   (1) A1 • A2 ⊆ αs (ϕ1 ∗ ϕ2 ) and (2) A1 • A2 ⊇ αs (ϕ1 ∗ ϕ2 ) ∩ AMSdϕ1 ∗ϕ2 e,s .
   The claim follows.
Case ϕ1 −~ϕ2 . By the induction hypotheses, we have for 1 ≤ i ≤ 2 that absts (ϕi ) =
   αs (ϕi ) ∩ AMSdϕi e,s . Let A2 := liftdϕ2 e%dϕ1 ∗ϕ2 e (absts (ϕ2 )). By Theorem 3,
   it follows that A2 = αs (ϕ2 ) ∩ AMSdϕ1 ∗ϕ2 e,s . Thus, in particular, A2 con-
   tains every AMS in αs (ϕ2 ) that can be obtained by composing an AMS in
   AMSdϕ1 −~ϕ2 e = AMSdϕ2 e with an AMS from αs (ϕ1 ) ∩ AMSdϕ1 e,s . With
   Lemma 19 we then get that (absts (ϕ1 )−•A2 ) ∩ AMSdϕ1 −~ϕ2 e is precisely the
   set of AMS αs (ϕ1 −~ϕ2 ) ∩ AMSdϕ1 −~ϕ2 e .
Case ϕ1 ∧ ϕ2 , ϕ1 ∨ ϕ2 . By the induction hypotheses, we have for 1 ≤ i ≤ 2 that
   absts (ϕi ) = αs (ϕi )∩AMSdϕi e,s . For 1 ≤ i ≤ 2, let Ai := liftdϕ1 e%dϕe (absts (ϕi )).
   By Theorem 3, we have Ai = αs (ϕi ) ∩ AMSdϕe,s . The claim thus follows
   from Lemma 15 resp. Lemma 16.
Case ¬ϕ1 . By the induction hypothesis, we have that absts (ϕ1 ) = αs (ϕ1 ) ∩
   AMSdϕ1 e,s . From Lemma 17, it follows that αs (¬ϕ1 ) ∩ AMSd¬ϕ1 e,s =
   AMSd¬ϕ1 e,s \ αs (ϕ1 ) = AMSd¬ϕ1 e,s \ (αs (ϕ1 ) ∩ AMSdϕ1 e,s ). The claim
   follows.

Proof. (Theorem 5.) We consider stacks s with dom(s) = x; we observe that
C := {cls= (s) | dom(s) ⊆ x} is finite; and that all stacks s, s0 with cls= (s) =
cls= (s0 ) have the same abstractions by Lemma 7. Consequently, we can compute
the set {absts (ϕ) | dom(s) ⊆ x} by picking for each element V ∈ C one stack s
with cls= (s) = V , and calculating absts (ϕ) for this stack. By Cor. 3, absts (ϕ)
is computable for every such stack. By Theorem 4 and Cor. 2, ϕ is satisfiable
over stack s iff absts (ϕ) is nonempty. Putting all this together, we obtain ϕ is
satisfiable in stacks of size n if and only if any of finitely many computable sets
absts (ϕ) is nonempty.
                           st
Proof. (Corollary 4.) ϕ |=x ψ iff ϕ ∧ ¬ψ is unsatisfiable w.r.t. x, which is decid-
able by Theorem 5.

Proof. (Lemma 21.) Let A = hV, E, ρ, γi ∈ AMSk,s . Each of the |s| ≤ n vari-
ables that occur in A can be encoded by a logarithmic number of bits. Observe
38

that |V | ≤ |s|, so V can be encoded by at most O(n log(n) + n) symbols (using
a constant-length delimiter between the nodes). Each of the at most |V | edges
can be encoded by O(log(n)) bits, encoding the position of the source and tar-
get nodes in the encoding of V by O(log(n)) bits each and expending another
bit to differentiate between = 1 and ≥ 2 edges. ρ can be encoded like V . Since
γ ≤ k ≤ n, γ can be encoded by at most log(n) bits. In total, we thus have an
encoding of length O(n log(n)).

Proof. (Lemma 22.) A simple induction on the structure of ϕ shows that it is
possible to enumerate the set absts (ϕ) using at most |ϕ| registers (each storing
an AMS). The most interesting case is ϕ1 −~ϕ2 . Assume we can enumerate the
sets absts (ϕ1 ) = {A1 , . . . , Am } and absts (ϕ2 ) = {B1 , . . . , Bn } in polynomial
space. We then use a new register in which we successively enumerate all A ∈
AMSdϕ1 −~ϕ2 e,s . This is done as follows: we enumerate all pairs of AMS (Ai , Bj ),
1 ≤ i ≤ m, 1 ≤ j ≤ n; we recognize that A ∈ AMSdϕ1 −~ϕ2 e,s iff Bj = Ai • A for
any of these pairs (Ai , Bj ).


C    Proofs for Section 4 (Program Verification with
     Strong-Separation Logic)

Proof. (Lemma 23.) Let (s1 , h) and (s2 , h) be two models with s1 (x) = s2 (x)
                                                            st                wk
for all x ∈ fvs(ϕ). Then, by Lemma 4 we have that (s1 , h) |= ϕ iff (s1 , h) |= ϕ iff
          wk                st
(s2 , h) |= ϕ iff (s2 , h) |= ϕ.

Proof. (Lemma 24.) Immediate from the definition of a robust formula.

Proof. (Lemma 25.) The requirements 1) and 2) of local contracts can be directly
verified from the semantics of the program statements.

Proof. (Lemma 26.) We prove the claim by induction on the number of appli-
cations of the frame rule and materialization rule. We consider a sequence of
program statements c = c1 · · · cn for which the triple {P } c {Q} was derived by
symbolic execution, introducing some fresh variables V . We then assume that
the claim holds for {P } c {Q} (for the base case we allow c to be the empty
sequence, i.e, c = , and consider {P }  {P }) and prove the claim for one more
application of the frame rule or the materialization rule.
      We first consider an application of the materialization rule. Then, we have
     st
Q |= ¬((x 7→ nil)−~t) (*) and we infer the triple {P } c {x 7→ z ∗ ((x 7→ z)−~Q)},
                                                                                  c
where z is some fresh variable. We now consider some stack-heap pairs (s, h) −    →
                        st
(s0 , h0 ) with (s, h) |= P . Because the claim holds for {P } c {Q} and V , there
                                                                 st
is some stack s00 with s0 ⊆ s00 , V ⊆ dom(s00 ) and (s00 , h0 ) |= Q. Because of (*)
                     st
we have (s00 , h0 ) |= ¬((x 7→ nil)−~t). Hence, there is some ` ∈ Loc such that
h0 (s00 (x)) = `. We now consider the stack s000 = s00 [z/`]. Note that s0 ⊆ s000 .
                                                                             st
Because Q is robust by induction assumption, we then have that (s000 , h0 ) |= x 7→
                                                                                            39

z ∗ ((x 7→ z)−~Q). Moreover, we get from Lemma 24 that x 7→ z ∗ ((x 7→ z)−~Q)
is robust. Thus, the claim is satisfied for the set of variables V 0 = V ∪ {z}.
    We now consider an application of the frame rule, i.e., we need to prove
the claim for the sequence c0 = cc, which extends c by some statement c. Let
{Pc } c {Qc } be the triple from the local proof rule for c. Because the frame
rule is applied, we have by assumption that there is some robust SL formula
A with Q = A ∗ Pc . From the application of the frame rule we then obtain
{P } c0 {A[x0 /x] ∗ Qc }, where x = modifiedVars(c) and x0 fresh. We now consider
                                   c0                          st
some stack-heap pairs (s, h) −→ (s0 , h0 ) with (s, h) |= P . Then, there is some
                                            c                              c
stack-heap pair (s00 , h00 ) with (s, h) −→ (s00 , h00 ) and (s00 , h00 ) →
                                                                          − (s0 , h0 ). Because
the claim holds for {P } c {Q} and V , there is some stack t with s00 ⊆ t, V ⊆
                        st
dom(t) and (t, h00 ) |= Q. Because of Q = A ∗ Pc , we have that there are some
                                                           st                   st
heaps h1 , h2 with h1 ]t h2 = h00 such that (t, h1 ) |= Pc and (t, h2 ) |= A. Because
    00              00  00 c    0    0                      00 c
of s ⊆ t and (s , h ) →     − (s , h ), we get that (t, h ) →  − (t , h ) for some s0 ⊆ t0 .
                                                                     0    0

Because {Pc } c {Qc } is a local contract by Lemma 25, we get that there is a heap
                 0                       st
h01 with h01 ]t h2 = h0 and (t0 , h01 ) |= Qc . We now consider the stack t00 defined
by t00 (x) = t0 (x) for all x ∈ dom(t0 ) and t00 (x0 ) = t(x) for all x ∈ modifiedVars(c),
where x0 ∈ x0 is the fresh copy created for x. Note that t0 ⊆ t00 . We recall that A
                                                 st
is robust by assumption. Hence, (t00 , h2 ) |= A[x0 /x]. Moreover, Qc is robust by
                                  st                       st
Lemma 23. Hence, (t00 , h1 ) |= Qc . Thus, (t00 , h0 ) |= A[x0 /x] ∗ Qc . Moreover, we
get from Lemma 24 that A[x0 /x] ∗ Qc is robust. Hence, the claim is satisfied for
the set of variables V 0 = V ∪ x0 .


D     Proofs for Section 5 (Normal Forms and the Abduction
      Problem)
Proof. (Lemma 27.) 1) follows directly from the definition of the abduction
problem and the semantics of −∗.
     For 2), we introduce the shorthand ζ := ϕ−∗ψ ∧ ¬((ϕ−∗ψ) ∗ ¬emp). We
              st
note that ζ |=x ϕ−∗ψ, and hence ζ is a solution to the abduction problem by 1).
                                                               st
Assume further that there is an abduction solution ζ 0 with ζ |=x ζ 0 ∗(¬emp). By
                 st                st
1) we have ζ 0 |=x ϕ−∗ψ. Hence, ζ |=x ϕ−∗ψ ∗ (¬emp). However, this contradicts
   st
ζ |=x ¬((ϕ−∗ψ) ∗ ¬emp). Thus, ζ is minimal. Now, consider another minimal
                                                            st
solution ζ 0 to the abduction problem. By 1), we have ζ 0 |=x ϕ−∗ψ. Because ζ 0
                                       st                                   st
is minimal, we have as above that ζ 0 |=x ¬((ϕ−∗ψ) ∗ ¬emp). Hence, ζ 0 |=x ζ.
Thus, ζ is the weakest minimal solution to the abduction problem.
