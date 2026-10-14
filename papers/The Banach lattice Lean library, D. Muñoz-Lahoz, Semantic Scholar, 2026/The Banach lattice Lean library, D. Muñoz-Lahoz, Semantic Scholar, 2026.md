                                                             The Banach lattice Lean library
                                                                             David Muñoz-Lahoz†
                                                                                August 21, 2026
arXiv:2608.07388v2 [math.FA] 20 Aug 2026




                                                                                     Abstract
                                                      We present a Lean 4 library for the theory of Banach lattices. Its purpose
                                                  is to support the systematic formalization of contemporary research in Banach
                                                  lattices and related areas. As evidence of this, we describe three research-level
                                                  formalizations built using the library. Writing the library at scale was made
                                                  possible by the use of LLMs with careful human supervision and planning.
                                                  Unlike autoformalization, this approach allows for an actual understanding
                                                  of the code. This, in turn, led to new mathematical insights that are also
                                                  discussed. Judging by the interest expressed by other researchers, we expect
                                                  the library to become a communal effort in the near future. For this reason,
                                                  we also describe several parts of the theory that could be added next.


                                           1 Introduction
                                           The Banach lattices Lean library § banlat is a Lean 4 project that contains a body
                                           of elementary results in the theory of Banach lattices. The goal of this library is
                                           to allow for the systematic formalization of research-level results in Banach lattices
                                           and nearby fields (such as stable phase retrieval, where autoformalization is already
                                           being used [7]). In fact, in Section 2 we will present three examples of research-level
                                           results in Banach lattices that have been formalized using the library. This was done
                                           by the author in a relatively short span of time; thus we expect that, as the library
                                           scales both in contributors and over time, we will be able to systematically formalize
                                           a significant part of the research in these fields.
                                              †
                                               Instituto de Ciencias Matemáticas. Universidad Autónoma de Madrid.
                                           Email: david.munnozl (at) uam (dot) es
                                               2020 Mathematics Subject Classification. Primary 46B42; Secondary 68V20.
                                               Key words and phrases. Banach lattice, Lean 4 library, locally solid topology, lattice-linear
                                           expression, positive projection, Banach lattice algebra.

                                                                                          1
“Semiautoformalization” This formalization at scale has been made possible by
the significant improvement of Large Language Models (LLMs). Even though LLMs
were used intensively in the process of writing this code, we would not consider
this an autoformalization project. Instead, it could be regarded as an exercise in
semiautoformalization: most of the code was written by LLMs, but with close human
steering and supervision. In the levels of quality of formalization introduced by T.
Tao in [20], this project would lie somewhere between levels 2 (Publication-level
formalization) and 3 (Prototype-level formalization).
     This has several implications. On the one hand, the use of generative tools
allows for suﬀicient speed and scale to verify research-level results in a reasonable
amount of time and with reasonable effort. The scientific implications of this are
well-known: the amount of literature being published is costly and diﬀicult to check;
if formalization of papers is systematized, in order to check the correctness of a paper
we would only need to check the correctness of the formalization. This may still not
be entirely trivial, but it is certainly easier. Notice that, in the process of checking
these formalized papers, having a trusted base of knowledge (a library) is critical
(for instance, in order to avoid checking the tree of definitions back to mathlib every
single time).
     On the other hand, the careful human supervision of these generative tools has
several advantages. First, it allows for a careful organization of the library. Second,
we can correct certain approaches proposed by the LLM that feel unnatural to hu-
mans, thus making the library more transparent for future users and contributors.
And third, since we have an understanding of what is going on in our code, we can
even gain some mathematical insights in the process (see Section 3). In practice,
doing this requires a certain expertise both in Banach lattices and in Lean, careful
planning of how to approach the library, and making sure that we always ask the
LLM to write definitions and results that are close and within reach, so as not to
let it make design decisions. This keeps LLM usage eﬀicient, another feature of this
approach that could become relevant if LLM token prices increase in the future.
     While working on this project, [6] announced a library in computational eco-
nomics with a similar philosophy. We also highlight [3], which is used to formalize [4].
Very recently, members of the Lean FRO and the Mathlib initiative announced Tau
Ceti [21], a “repository of formal mathematics, directed by human-written roadmaps,
implemented and maintained by AI contributors, subject to adversarial review.” We
believe the philosophy behind this new project is closely aligned with the one pre-
sented below.




                                           2
Formalization vs “Semiautoformalization” vs Autoformalization Of
course, the previous benefits are amplified in manual formalization: it is more
readable, it is properly implemented, and it provides more mathematical insights.
This is, of course, what happens with § mathlib4, the mathematics Lean library [22].
Then, what is the point of this “semiautoformalization”? The answer is scale. It is a
trade-off: we are sacrificing code quality (especially inside the proofs, since these are
generally not checked) for scale. For instance, as mentioned above, sometimes we
had to redirect the LLM’s proposed approach, but we certainly also missed several
occasions to do so because of speed and scale. (At other times it was the LLM that
taught us how to approach certain results, see Section 3.)
    We do not feel that “semiautoformalization” is better or worse in any way: it is
just a different approach, with different goals in mind. We believe that with this scale,
and proper training of our fellows, formal verification of new mathematical results
can become truly systematic in our field. How we are facing this community-level
change is addressed in more detail in [11].
    As a proof of concept, we present in Section 2 the formalization of three research-
level results that the library has made possible: the first is the construction of an
object that has sparked considerable interest in our community in recent years, the
second is the solution to an open problem recently published by the author, and the
third is a relatively simple counterexample answering an open question that is part
of an ongoing project.
    We must clarify that, once all the necessary preliminaries have been added to
the library, we expect the formalization of papers to be an actual autoformalization.
For this process, there already exist tools like LEAP [14] and LeanMarathon [26].
However, this kind of autoformalization, which assumes the necessary preliminar-
ies are already in the library, is significantly cheaper than most autoformalization
projects, and much easier to check because of the shared body of results that the
library provides.

Why Banach lattices? Banach lattices can be approached both from analysis,
as Banach spaces with some additional structure, and from order theory, as vector
lattices with a complete lattice norm. This second approach has proved to be very
apt for formalization, because it starts very close to the contents already available
in § mathlib4. Thus we could get to the elementary theory of vector and Banach
lattices without much preliminary material, progressing then to more analytic con-
cepts involving convergence, continuity, functionals, measures, compacta, and more
categorical constructions such as completions and free objects, which play a central
role in the modern theory.

                                           3
    Beyond the mathematical details, the field of Banach lattices has a cohesive
and supportive community that has been willing to join forces to contribute to this
project, and to learn the new tools needed to do so. Several researchers in Banach
lattices have already expressed their interest in contributing. This will make expand-
ing the library in a variety of directions relatively easy, leveraging the expertise of
the different researchers. A detailed account of how this process is unfolding can be
found in [11].

Future steps Short-term goals of the library include its extension (see Section 5
for some candidate directions) and the formalization of more research-level papers.
In the near future, we also expect to have our own systematic pipeline for formalizing
papers using the library. In the long term, we expect to distill from the library the
contents that could be welcome in § mathlib4, rewrite them to have the appropriate
code quality, and contribute them. Since we are building on top of the enormous
communal effort that mathlib represents, we feel that this could be an opportunity
to give back.
    Future improvements in technology (particularly, artificial intelligence) could sig-
nificantly increase the quality and scalability of the project. We are not used to this
in pure mathematics, where, unlike in other sciences, progress has been essentially
detached from technological advances. However, projects like the one presented here
are highly dependent on technology. This means that procedures and techniques
could become obsolete as technology advances.

Notation and conventions No code appears in this paper. All pieces of code
are provided as external links to GitHub repositories. This way, the code is always
presented in its full context. A link to a GitHub repository appears as § banlat; a
folder inside the repository as i BanLat; a file inside a folder as D BanLat/Basic.le
an; and a line inside a file as ∀ BanLat/Basic.lean L34. Often, instead of citing a
particular line, we want to cite a particular named Lean term (generally a theorem
or definition). In this case, the name instead of the line number will appear in the
reference, with the link pointing to the particular line where the term is introduced.
For instance, ∀ abs_eq_zero_iff_zero points to the same line as ∀ BanLat/Basic.lea
n L34.
    Most of the time we cite the repositories § banlat and § mathlib4. These are
libraries that change with time. Hence all references are to the commit tagged as
v0.1.0 in § banlat, and to the commit tagged as v4.30.0 in § mathlib4.




                                           4
2 Some use cases
In this section we present three research-level results that have been formalized using
the library. Section 2.1 presents the formalization of the free Banach lattice generated
by a Banach space; Section 2.2 the formalization of a solution to an open problem
by A. W. Wickstead recently solved by the author; and Section 2.3 the formalization
of a counterexample to an open question that is part of an ongoing project of the
author together with M. A. Taylor and P. Tradacete.

2.1 The free Banach lattice generated by a Banach space
The free Banach lattice generated by a Banach space was first constructed explicitly
by A. Avilés, J. Rodríguez, and P. Tradacete in their 2018 paper [5]. This object
has sparked a lot of research over the last decade, and has been used to solve open
problems as well as to better understand the interaction between Banach spaces and
Banach lattices (see for instance [19]). For this reason, it seemed the best candidate
to add a modern object to the library on which a significant amount of recent research
depends.
     As the name indicates, the free Banach lattice generated by a Banach space E
is a Banach lattice FBL[E] together with a canonical isometric embedding δ : E →
FBL[E] that satisfies the following universal property: for every Banach lattice X
and every bounded operator T : E → X, there exists a unique lattice homomorphism
T̂ : FBL[E] → X with ∥T̂ ∥ = ∥T ∥ satisfying T̂ δ = T . As usual, if such an object
exists, then it is unique up to a unique lattice isometry. The major accomplishment
of [5] was to provide an explicit description of FBL[E]. Next we describe this con-
struction, together with its formalization in § banlat. Throughout this section, E
will denote a Banach space.
Definition 2.1. ∀ freeNormExt Define the (extended) free norm ∥·∥FBL[E] : C(BE ∗ ) →
[0, ∞] by
                     {∑
                      n                                                  ∑
                                                                         n              }
                              ∗              ∗            ∗                  ∗
    ∥f ∥FBL[E] = sup     |f (xk )| : n ∈ N, x1 , . . . , xn ∈ BE ∗ , sup   |xk (x)| ≤ 1
                                                              x∈BE
                          k=1                                        k=1

for every f ∈ C(BE ∗ ).
Proposition 2.2. ∀ instBanachLatticeFunctionSpace The space
                          C0 = { f ∈ C(BE ∗ ) : ∥f ∥FBL[E] < ∞ },
with the order and linear structures inherited from C(BE ∗ ), and the restriction of
∥·∥FBL[E] as a norm, is a Banach lattice.

                                            5
    For every x ∈ E, define δx ∈ C0 by δx (x∗ ) = x∗ (x) for all x∗ ∈ BE ∗ (∀ dualEval).
Define FBL[E] as the closed sublattice generated by { δx : x ∈ E } in (C0 , ∥·∥FBL[E] )
(∀ FBL). Then (FBL[E], ∥·∥FBL[E] ) is certainly a Banach lattice (∀ instBanachLattice
FBL). Define also δ : E → FBL[E] by δ(x) = δx for x ∈ E (∀ of); this map is a linear
isometry (∀ ofLinearIsometry). Then FBL[E], together with δ, is the free Banach
lattice generated by E:
Theorem 2.3. ∀ exists_unique_lift Let X be a Banach lattice, and let T : E → X
be a bounded linear operator. Then there exists a unique lattice homomorphism
T̂ : FBL[E] → X with ∥T̂ ∥ = ∥T ∥ satisfying T̂ δ = T .

2.2 Non-representable Banach lattice algebras
In [25], A. W. Wickstead formulated the following question. Let X be an order
complete Banach lattice, and let P : X → X be a positive projection for which there
exists an α ≥ 0 satisfying:
  (i) α idX ≤ P , and

 (ii) whenever T is a positive operator such that both T ≤ λ idX , for some λ ≥ 0,
      and T ≤ P , then also T ≤ α idX .
Which values can α take? Wickstead conjectured that either α = 0 or α = 1/n,
for some n ∈ N, and showed this for finite-dimensional X. In [18], it was shown
that this holds for arbitrary X. In § wickstead the main results of [18] have been
formalized using the Banach lattices Lean library. More precisely, the general result
is a consequence of the C(K)-case, which can be proved without assuming order
completeness.
Theorem 2.4. ∀ main_CK Let K be a non-empty compact Hausdorff space. Let
P : C(K) → C(K) be a positive projection with P 1K = 1K . Suppose there exists
some α ≥ 0 satisfying:
  (i) α idC(K) ≤ P , and

 (ii) if 0 ≤ Mf ≤ P , then ∥f ∥∞ ≤ α.
Then either α = 0 or α = 1/n for some n ∈ N.
Corollary 2.5. ∀ main Let X be a non-zero Dedekind complete vector lattice. Let
P : X → X be a positive projection with constant diagonal α. Then either α = 0 or
α = 1/n, for some n ∈ N.

                                           6
    This question in operator theory arose while studying the representation problem
for Banach lattice algebras. A Banach lattice algebra (∀ BanachLatticeAlgebra) is a
Banach lattice together with a Banach algebra structure for which the product of
positive elements is positive. It was an open problem [23, Question 5.3] and [24,
Problem 2] whether every Banach lattice algebra is faithfully representable (as a
lattice and as an algebra) in the space of regular operators on an order complete
vector lattice. Wickstead showed in [25] that, if Theorem 2.5 is true, then there exist
unital Banach lattice algebras that are not unitarily representable. In [18], we were
able to extend this approach to show that, in fact, Theorem 2.5 implies a negative
answer to the general representation problem for Banach lattice algebras.

Proposition 2.6. ∀ non_representable Let A be a Banach lattice algebra. Suppose
there exist non-zero positive elements e, p ∈ A+ satisfying:

  (i) e2 = e, p2 = p,

 (ii) ep = pe = p, and

(iii) p = αe + x, for some x ∈ A with x ∧ e = 0, and some α ∈ R+ .

If α ̸∈ {0} ∪ {1/n : n ∈ N}, then A has no faithful representation on Lr (X), for any
order complete vector lattice X.

2.3 σ-Lebesgue locally convex-solid topologies
The following question appears in [1, Open Problem 8.1]: is the completion of a σ-
Lebesgue Hausdorff locally convex-solid vector lattice also σ-Lebesgue? The answer
turns out to be negative, and a counterexample is formalized in § SigmaLebesgueCom
pletion.

Proposition 2.7. ∀ sigmaLebesgueTopology_not_preserved_by_completion There
exists a σ-Lebesgue Hausdorff locally convex-solid vector lattice whose completion is
not σ-Lebesgue.


3 Some mathematical insights
This section collects some mathematical ideas that appeared in the process of building
the library and that we believe are relevant enough to deserve a detailed explanation.
Throughout this section, n ∈ N denotes a natural number, and X denotes a vector
lattice.

                                          7
3.1 Vanishing lattice-linear expressions
A classical result in the theory of vector lattices states that every expression involv-
ing the linear and lattice operations (i.e., sums, scalar multiplications, suprema, and
infima) that holds in R must also hold in every vector lattice. This result has impor-
tant pragmatic implications (it is relatively easy to check expressions in the reals,
because the order is total) and theoretical implications (for instance, it is key in the
concrete construction of the free vector lattice).
    When trying to formalize this result in Lean, we were expecting to do it for
Archimedean vector lattices using Kakutani’s theorem. This is the approach tradi-
tionally taken in Banach lattices monographs; see, for example, [16, Section 1.d] and
[17, Theorem 2.1.10].† We even pointed the LLM toward this approach. However,
the LLM took a different route that surprised us, providing a proof that is elemen-
tary, does not depend on the axiom of choice, and works for every vector lattice
(Archimedean or not). This is remarkable, since in the more general context of vec-
tor lattices, the result is proved using the representation of a vector lattice inside the
direct product of totally ordered vector lattices, a technique that also relies on the
axiom of choice (see, for instance, [15]).
    The result can also be seen as a consequence of the fact that the free vector
lattice can be realised as a vector lattice of real-valued functions. This was proved
by R. D. Bleier [9] using convex analysis, an approach that probably inspired the
proof presented here. Bleier’s argument is not entirely elementary, since his proof of
[9, Lemma 2.1] again relies on the representation of a vector lattice as a subdirect
product of totally ordered vector lattices; however, as observed by M. de Jeu [12,
Lemma 2.1], the use of representation theorems can be avoided, making the argument
completely elementary.‡ Nevertheless, the argument used in the library avoids free
objects altogether, which keeps it elementary and, more importantly, makes it easier
to formalize. This is particularly relevant because Bleier’s approach requires the
existence of the free vector lattice, a fact that comes from universal algebra and
whose formalization would require developing a completely different area in Lean.
    For these reasons, we believe it is worth explaining the details of this new proof,
together with its formalization. Even though the idea of the proof is very clear,
writing down all the details is cumbersome because doing so requires manipulating
formal expressions, which are defined recursively. However, since Lean is by design
   †
     This technique can be used to prove something stronger, namely, positively homogeneous func-
tion calculus, which is what the cited monographs end up proving.
   ‡
     Bleier’s result also follows from a more general theorem of M. de Jeu and X. Jiang [13, Theorem
4.5], which canonically realises the free vector lattice over a pre-ordered vector space as a vector
sublattice of a function lattice.


                                                 8
very good at dealing with recursive definitions, this is one of those rare instances
in which an argument is more elegant and direct in Lean than in written natural
language!
   To state the theorem properly, we first need the formal definition of “expressions
involving the linear and lattice operations.”

Definition 3.1. ∀ LLexpr A lattice-linear expression Φ in the formal variables
t1 , . . . , tn is a formal expression constructed inductively in the following way:

  (i) 0 is a lattice-linear expression;

 (ii) t1 , t2 , …, tn are lattice-linear expressions;

 (iii) if Φ1 and Φ2 are lattice-linear expressions in t1 , . . . , tn , then Φ1 + Φ2 , λΦ1 (for
       λ ∈ R), Φ1 ∨ Φ2 , and Φ1 ∧ Φ2 are lattice-linear expressions in t1 , . . . , tn .

Remark. To abbreviate, we denote the fact that Φ is a lattice-linear expression in
the formal variables t1 , . . . , tn by Φ[t1 , . . . , tn ]. Note that not all the variables need
appear explicitly in Φ; for example, Φ[t1 , . . . , tn ] = t1 is a lattice-linear expression in
t1 , . . . , tn . In particular, every lattice-linear expression in t1 , . . . , tn is also a lattice-
linear expression in t1 , . . . , tm for all m ≥ n.
   It should be intuitively clear that every lattice-linear expression in n variables
can be “evaluated” at n arbitrary elements of a vector lattice in the “obvious way.”
This notion is defined recursively as follows.

Definition 3.2. ∀ eval Let Φ[t1 , . . . , tn ] be a lattice-linear expression, and let
x1 , . . . , xn ∈ X. We define the evaluation of Φ at x1 , . . . , xn as the element
Φ(x1 , . . . , xn ) ∈ X defined recursively by

  (i) if Φ = 0, Φ(x1 , . . . , xn ) = 0.

 (ii) if Φ = ti , Φ(x1 , . . . , xn ) = xi .

 (iii) if Φ = Φ1 + Φ2 , for some lattice-linear expressions Φ1 and Φ2 , Φ(x1 , . . . , xn ) =
       Φ1 (x1 , . . . , xn ) + Φ2 (x1 , . . . , xn ).

 (iv) if Φ = λΦ1 , for some lattice-linear expression Φ1 and some λ ∈ R,
      Φ(x1 , . . . , xn ) = λΦ1 (x1 , . . . , xn ).

  (v) if Φ = Φ1 ∨ Φ2 , for some lattice-linear expressions Φ1 and Φ2 , Φ(x1 , . . . , xn ) =
      Φ1 (x1 , . . . , xn ) ∨ Φ2 (x1 , . . . , xn ).


                                                  9
 (vi) if Φ = Φ1 ∧ Φ2 , for some lattice-linear expressions Φ1 and Φ2 , Φ(x1 , . . . , xn ) =
      Φ1 (x1 , . . . , xn ) ∧ Φ2 (x1 , . . . , xn ).

   The above is an example of a definition that is shorter to write in Lean than in
LAT X, all thanks to Lean’s pattern matching.
   E
Definition 3.3. ∀ Vanishes We say that a lattice-linear expression Φ[t1 , . . . , tn ]
vanishes on X if Φ(x1 , . . . , xn ) = 0 for all x1 , . . . , xn ∈ X.

    We can now state the theorem.

Theorem 3.4. ∀ vanishes_of_vanishes_real A lattice-linear expression that van-
ishes on R must also vanish on every vector lattice.

     The idea of the proof is the following. Consider two arbitrary lattice-linear ex-
pressions Φ[t1 , . . . , tn ] and Ψ[t1 , . . . , tn ] that are suprema of linear expressions, that
is, that can be written as

                                     ∨
                                     m ∑
                                       n                                            ∨
                                                                                    l ∑
                                                                                      n
             Φ[t1 , . . . , tn ] =             aik tk   and Ψ[t1 , . . . , tn ] =             bik tk ,
                                     i=1 k=1                                        j=1 k=1


for some m, l ∈ N and aik , bik ∈ R. First we are going to show, using elementary
computations, that if Φ(λ1 , . . . , λn ) = Ψ(λ1 , . . . , λn ) for all λ1 , . . . , λn ∈ R, then
Φ(x1 , . . . , xn ) = Ψ(x1 , . . . , xn ) for all x1 , . . . , xn in an arbitrary vector lattice X.
    Next we are going to prove that, if now Φ[t1 , . . . , tn ] is an arbitrary lattice-linear
expression, then there exists an “equivalent” lattice-linear expression Φ̃[t1 , . . . , tn ]
(equivalent in the sense that Φ(x1 , . . . , xn ) = Φ̃(x1 , . . . , xn ) for every x1 , . . . , xn ∈ X)
of the form
                                                 ∨
                                                 m ∑   n             ∨l ∑n
                           Φ[t1 , . . . , tn ] =            aik tk −        bjk tk .
                                                   i=1 k=1           j=1 k=1

This is the step that requires working recursively on the definition of Φ, and that
is very clean in Lean but technical in written math. Once this is proved, it is easy
to conclude: if Φ vanishes on the reals, so does Φ̃, which by the previous paragraph
implies that the two suprema appearing in the expression of Φ̃ must evaluate to the
same element on every vector lattice. Thus Φ̃ vanishes on every vector lattice, and
so does Φ.
    We now turn to the actual details of the proof. We start with two elementary
lemmas. For a1 , . . . , am ∈ Rn , we denote by conv(a1 , . . . , am ) their convex hull.


                                                         10
Lemma 3.5. ∀ mem_convexHull_of_forall_le_sup                           Let m ∈ N, let ai =
(ai1 , . . . , ain ) ∈ R , for i = 1, . . . , m, and let p = (p1 , . . . , pn ) ∈ Rn . If, for every
                         n

(λ1 , . . . , λn ) ∈ Rn ,
                                     ∑ n             ∨
                                                     m ∑n
                                            λj p j ≤      λj aij ,
                                         j=1          i=1 j=1

then p ∈ conv(a1 , . . . , am ).

Proof. Since conv(a1 , . . . , am ) is compact, the result is an immediate consequence of
the hyperplane separation theorem (see, for instance, [10, Section 2.5.1]; or ∀ geomet
ric_hahn_banach_point_closed in § mathlib4).

Lemma 3.6. ∀ linearCombination_le_eval_of_mem_convexHull           ∨m ∑n Let Φ[t1 , . . . , tn ]
be a lattice-linear expression of the form Φ[t1 , . . . , tn ] = i=1 j=1 aij tj , for some
m ∈ N and aij ∈ R. Set ai = (ai1 , . . . , ain ), for i = 1, . . . , m. If p = (p1 , . . . , pn ) ∈
conv(a1 , . . . , am ), then
                               ∑n
                                   pi xi ≤ Φ(x1 , . . . , xn ),
                                     i=1

for every x1 , . . . , xn ∈ X.
                                                                                 ∑m
Proof. Since p ∈ conv(a1 , . . . , am ), there exist µ1 , . . . , µm ≥ 0 with     i=1 µi = 1 such
that
                                             ∑m
                                         p=      µi a i .
                                                    i=1

To conclude, simply compute
                                   ∑
                                   n               n (∑
                                                   ∑  m                  )
                                         pj xj =                    µi aij xj
                                   j=1             j=1        i=1
                                                   ∑m         ∑n
                                               =         µi         aij xj
                                                   i=1        j=1
                                                   ∑m         ∨m ∑n
                                               ≤         µi             aij xj
                                                   i=1        i=1 j=1

                                               = Φ(x1 , . . . , xn ).

    Now we can prove the theorem for lattice-linear expressions that are suprema of
linear expressions.

                                                     11
Lemma 3.7. ∀ eval_eq_of_forall_real_eq                             Let Φ[t1 , . . . , tn ] and Ψ[t1 , . . . , tn ] be
lattice-linear expressions of the form

                                     ∨
                                     m ∑
                                       n                                                 ∨
                                                                                         l ∑
                                                                                           n
             Φ[t1 , . . . , tn ] =             aik tk   and      Ψ[t1 , . . . , tn ] =             bjk tk ,
                                     i=1 k=1                                             j=1 k=1


for some m, l ∈ N and aik , bik ∈ R. Suppose that Φ(λ1 , . . . , λn ) = Ψ(λ1 , . . . , λn ) for
every λ1 , . . . , λn ∈ R. Then Φ(x1 , . . . , xn ) = Ψ(x1 , . . . , xn ) for every x1 , . . . , xn ∈ X.

Proof. Let x1 , . . . , xn ∈ X. Since the roles of Φ and Ψ are interchangeable, it suﬀices
to prove that
                                               ∨
                                               m ∑
                                                 n
                         Φ(x1 , . . . , xn ) =     aik xk ≤ Ψ(x1 , . . . , xn ).
                                                    i=1 k=1

This, in turn, is the same as showing that
                                        ∑
                                        n
                                               aik xk ≤ Ψ(x1 , . . . , xn )                                     (1)
                                         k=1

holds for each i = 1, . . . , m. Fix i ∈ {1, . . . , m}. By assumption, for all (λ1 , . . . , λn ) ∈
Rn ,
                        ∑ n                                  ∨
                                                             l ∑
                                                               n
                              aik λk ≤ Ψ(λ1 , . . . , λn ) =     bjk λk .
                            k=1                                        j=1 k=1

According to Theorem 3.5, this implies that ai ∈ conv(b1 , . . . , bl ), where ai =
(ai1 , . . . , ain ) and bj = (bj1 , . . . , bjn ) for j = 1, . . . , l. Now (1) follows immediately
from Theorem 3.6.

Definition 3.8. Let Φ[t1 , . . . , tn ] and Ψ[t1 , . . . , tn ] be lattice-linear expressions. We
say that Φ and Ψ are equivalent if Φ(x1 , . . . , xn ) = Ψ(x1 , . . . , xn ) for every x1 , . . . , xn
in a vector lattice X.

Definition 3.9. ∀ NormalForm We say that a lattice-linear expression Φ[t1 , . . . , tn ] is
in normal form if it is of the form

                                                    ∨
                                                    m ∑
                                                      n                  ∨
                                                                         l ∑
                                                                           n
                            Φ[t1 , . . . , tn ] =             aik tk −             bjk tk .
                                                    i=1 k=1              j=1 k=1


for some m, l ∈ N, and some aik , bjk ∈ R.

                                                         12
   The following is the last ingredient needed to complete the proof of Theorem 3.4.
The proof of the following fact in Lean is more elegant, and even shorter, than the
one provided here. Also, the computational nature of the proof makes it prone to
typos, whereas the formulas that appear in the Lean code are certainly correct.
Theorem 3.10. ∀ normalize_eval For every lattice-linear expression Φ[t1 , . . . , tn ]
there exists a lattice-linear expression Φ̃[t1 , . . . , tn ] in normal form that is equivalent
to Φ.
Proof. We prove it by induction on the definition of Φ. If Φ = 0 or Φ = ti , for some
i, then Φ is already in normal form and there is nothing to do. This proves the base
case. Now suppose that there exist lattice-linear expressions Φ1 and Φ2 such that
precisely one of the following holds:
  (i) Φ = Φ1 + Φ2 .
 (ii) Φ = λΦ1 , for some λ ∈ R.
 (iii) Φ = Φ1 ∨ Φ2 ,
 (iv) Φ = Φ1 ∧ Φ2 .
Use the induction hypothesis to obtain lattice-linear expressions Φ̃1 and Φ̃2 in normal
form equivalent to Φ1 and Φ2 , respectively. We can write, explicitly,
                                                   ∨
                                                   m1 ∑
                                                      n1                ∨
                                                                        l1 ∑
                                                                           n1
                       Φ̃1 [t1 , . . . , tn1 ] =             aik tk −             bjk tk ,
                                                   i=1 k=1              j=1 k=1

and
                                                   ∨
                                                   m2 ∑
                                                      n2                ∨
                                                                        l2 ∑
                                                                           n2
                       Φ̃2 [t1 , . . . , tn2 ] =             cik tk −             djk tk ,
                                                   i=1 k=1              j=1 k=1

for some n1 , n2 ∈ {1, . . . , n}, m1 , m2 , l1 , l2 ∈ N, and aik , bjk , cik , djk ∈ R.
    Below we give an explicit expression for Φ̃ depending on how Φ is constructed.
In each of the cases, it is clear that Φ̃ is in normal form, and it is immediate to
check that it is equivalent to Φ using the basic properties of vector lattices. Let
m = max{m1 , m2 } and l = max{l1 , l2 }. By convention, the coeﬀicients that are not
defined are set equal to 0.
  (i) If Φ = Φ1 + Φ2 , then
                                            ∨
                                            m ∑
                                              n                           ∨
                                                                          l ∑
                                                                            n
                   Φ̃[t1 , . . . , tn ] =             (aik + cik )tk −              (bjk + djk )tk .
                                            i=1 k=1                       j=1 k=1


                                                        13
 (ii) If Φ = λΦ1 , with λ ≥ 0, then
                                                    ∨
                                                    m1 ∑
                                                       n1                    ∨
                                                                             l1 ∑
                                                                                n1
                           Φ̃[t1 , . . . , tn ] =              (λaik )tk −             (λbjk )tk ,
                                                    i=1 k=1                  j=1 k=1

      whereas if λ < 0, then
                                                ∨
                                                l1 ∑
                                                   n1                        ∨
                                                                             m1 ∑
                                                                                n1
                       Φ̃[t1 , . . . , tn ] =             (−λbik )tk −                 (−λajk )tk .
                                                i=1 k=1                      j=1 k=1


 (iii) If Φ = Φ1 ∨ Φ2 , then
                                  ( max{m,l}
                                      ∨ ∑    n               ) ( max{m,l}
                                                                   ∨ ∑    n                )
           Φ̃[t1 , . . . , tn ] =              (aik + dik )tk ∨             (cik + bik )tk
                                     i=1        k=1                                 i=1      k=1
                                   ∨
                                   l ∑
                                     n
                               −             (bjk + djk )tk .
                                   j=1 k=1


 (iv) If Φ = Φ1 ∧ Φ2 , then Φ is equivalent to −((−Φ1 ) ∨ (−Φ2 )), and we can iterate
      (ii) and (iii) to obtain the desired lattice-linear expression.


Proof of Theorem 3.4. Let Φ[t1 , . . . , tn ] be a lattice-linear expression that vanishes
on R. By Theorem 3.10, there exists a lattice-linear expression Φ̃ in normal form
that is equivalent to Φ. Thus it suﬀices to show that Φ̃(x1 , . . . , xn ) = 0 for every
x1 , . . . , xn in a vector lattice X. Write
                                                    ∨
                                                    m ∑
                                                      n                   ∨
                                                                          l ∑
                                                                            n
                           Φ̃[t1 , . . . , tn ] =              aik tk −             bjk tk
                                                    i=1 k=1               j=1 k=1

for some m, l ∈ N, and some aik , bjk ∈ R. By assumption,
                 ∨
                 m ∑
                   n                    ∨
                                        l ∑
                                          n
                           aik λk =                   bjk λk    for every λ1 , . . . , λn ∈ R.
                 i=1 k=1                j=1 k=1

It follows from Theorem 3.7 that
                                     ∨
                                     m ∑
                                       n                       ∨
                                                               l ∑
                                                                 n
                                                aik xk =                 bjk xk .
                                     i=1 k=1                   j=1 k=1

Therefore Φ(x1 , . . . , xn ) = 0.

                                                          14
    This result was then used to implement ∀ llarith, a tactic that closes non-strict
inequalities in vector lattices by checking that the inequality holds in R. This in turn
is done using the linarith tactic. The tactic also supports assumptions of the type
0 ≤ x.
    We believe that this tactic could be useful in the process of autoformalizing papers
in order to manipulate lattice-linear identities quickly and conveniently. However,
for performance reasons, we try to avoid its use in the library files that are high
in the import hierarchy. This tactic was implemented using heavy LLM assistance,
and it is far from optimal; we could certainly use the advice from more experienced
metaprogrammers to improve it.

3.2 The Archimedean property
In § mathlib4, the Archimedean property is defined for ordered commutative monoids
as follows.

Definition 3.11. ∀ Archimedean An ordered commutative monoid R is said to be
Archimedean if for every two elements x, y ∈ R such that 0 < y, there exists a
natural number n ∈ N such that x ≤ ny.

    This definition, although standard in the theory of linearly ordered groups, is
stronger than the one used in the theory of lattice-ordered groups and vector lattices.
For this reason, in § banlat, we had to introduce the following alternative definition.

Definition 3.12. ∀ IsVLArchimedean      A lattice-ordered group G is said to be
Archimedean if whenever x, y ∈ G are such that ny ≤ x for all n ∈ N, then y ≤ 0.

    Definitions 3.11 and 3.12 are equivalent in linearly ordered groups. However,
Theorem 3.11 is in general stronger than Theorem 3.12: R2 , with the order defined
pointwise, satisfies Theorem 3.12 but not Theorem 3.11.
    This is not the only notational subtlety that arose when building the library.
For instance, what in ordered vector spaces and vector lattices is usually called order
completeness or Dedekind completeness, in lattice theory (and, therefore, in mathlib)
is known as conditionally completeness (∀ ConditionallyCompleteLattice).

3.3 Locally convex-solid topologies
A subset S ⊆ X is solid if [−|x|, |x|] ⊆ S holds for every x ∈ S. A linear topology
on X is locally solid if 0 has a neighbourhood basis of solid sets; X equipped with a
locally solid topology is called a locally solid vector lattice (∀ IsLocallySolidVectorLa

                                           15
ttice). Locally solid topologies abstract many of the order-topological properties of
Banach lattices. Recall that, in a vector space, a linear topology is locally convex if
0 has a neighbourhood basis of convex sets. A particularly relevant family of locally
solid topologies are the ones that are also locally convex.
Definition 3.13. ∀ IsLocallyConvexSolidVectorLattice A linear topology on a
vector lattice that is at the same time locally solid and locally convex is called a
locally convex-solid topology. A vector lattice together with a locally convex-solid
topology is called a locally convex-solid vector lattice.
    This definition is, almost verbatim, the one given in the monograph [2, Page
59]. In the same book, and without any further comment on the definition, it is
assumed that locally convex-solid topologies admit a neighbourhood basis at the
origin formed by sets that are both convex and solid. But this is not strictly what
the definition says: the definition establishes that there exist both a neighbourhood
basis of convex sets and a neighbourhood basis of solid sets. That there exists a basis
with both properties at the same time is reasonably easy, but not entirely obvious.
    This subtlety arose when trying to formalize the notion of locally convex-solid
topology in Lean. Since this is not addressed in [2], the main reference monograph
on the topic, it seems relevant to provide the mathematical details next. These ideas
can be found in much greater generality in [8, Section 2].
Definition 3.14. ∀ solidInterior Given S ⊆ X, we define its solid interior as the
subset
                     Sol Int(S) = { x ∈ S : [−|x|, |x|] ⊆ S }.
    Clearly, the solid interior of S is the largest solid set contained in S. The following
is the key fact we need about the solid interior.
Proposition 3.15. ∀ convex_solidInterior           In a vector lattice, the solid interior
of a convex set is convex.
Proof. Let C ⊆ X be a convex set. Let x, y ∈ Sol Int(C) and let λ, µ ∈ R+ be
such that λ + µ = 1. We want to show that [−|λx + µy|, |λx + µy|] ⊆ C. If
λ = 0 or µ = 0, the result is immediate, so we may assume that λ, µ > 0. Let
z ∈ X be such that |z| ≤ |λx + µy|. Then |z| ≤ λ|x| + µ|y|, and by the Riesz
decomposition theorem there exist w1 , w2 ∈ X with |w1 | ≤ λ|x| and |w2 | ≤ µ|y| such
that z = w1 + w2 . Since x, y ∈ Sol Int(C), which of course is a solid set, it follows
that λ−1 w1 , µ−1 w2 ∈ Sol Int(C) ⊆ C. Convexity of C then implies

                            z = λ(λ−1 w1 ) + µ(µ−1 w2 ) ∈ C.

                                            16
Proposition 3.16. ∀ hasBasis_convex_solid Let τ be a locally convex-solid topology
on X. Then 0 has a neighbourhood basis formed by sets that are both convex and
solid.

Proof. Let U be a neighbourhood of 0. By assumption, there exist neighbourhoods
S ′ ⊆ C ⊆ S ⊆ U of 0 such that S, S ′ are solid and C is convex. Then Sol Int(C) ⊆ U
is solid, convex by Theorem 3.15, and it is a neighbourhood of 0 because it contains
S ′.


4 Overview of the library
The following is an overview of what is currently available in the library.

  • D BanLat.lean: General import file for the whole library.

  • D BanLat/Basic.lean: Develops the basic definitions and identities of lattice-
    ordered groups and real vector lattices. Defines the Archimedean property and
    proves equivalent characterizations.

  • D BanLat/Normed.lean: Defines normed vector lattices and Banach lattices. It
    proves continuity of lattice operations, Lipschitz continuity of the modulus
    map, closedness of the positive cone and order intervals, boundedness of order-
    bounded sets, and monotone convergence facts.

  • D BanLat/Disjoint.lean: Introduces the notion of disjoint vectors in a vector
    lattice, and proves basic facts related to disjointness.

  • D BanLat/RieszDec.lean: Proves the Riesz decomposition theorem and closely
    related results.

  • D BanLat/OrderComplete.lean: Defines order and σ-order completeness, and
    proves basic characterizations (e.g., it suﬀices to check completeness for in-
    creasing positive nets).

  • D BanLat/OrderDense.lean: Defines order dense subsets, and proves some basic
    properties.

  • D BanLat/OrderUnit.lean: Defines weak and strong order units.




                                         17
• D BanLat/Pi.lean: Introduces a natural vector lattice structure in the arbitrary
  product of vector lattices. It also introduces p-sums, 1 ≤ p ≤ ∞, of normed
  and Banach lattices. Records that the ∞-sum of AM-spaces is an AM-space,
  and the 1-sum of AL-spaces is an AL-space.

• D BanLat/Atom.lean: Defines atoms in vector lattices. Defines the continuous
  and atomic part of a vector lattice. Shows that every infinite-dimensional
  Archimedean vector lattice contains a sequence of pairwise disjoint non-zero
  vectors. Shows that an Archimedean vector lattice is finite-dimensional if and
  only if it is isomorphic to Rn .

• D BanLat/QuasiInteriorPoint.lean: Defines quasi-interior points. Proves that
  every separable Banach lattice has a quasi-interior point.

• D BanLat/Quotient.lean: Constructs quotients of vector lattices by order ideals.
  Defines the quotient lattice structure, proves the canonical quotient map is a
  vector lattice homomorphism, develops inequality-lifting lemmas, factors posi-
  tive and lattice homomorphisms through quotients, characterises Archimedean
  quotients by uniform closedness of the ideal, and builds normed and Banach
  lattice quotients by closed ideals.

• D BanLat/Dual.lean: Develops the order dual of vector lattices and the norm
  dual of Banach lattices.

• D BanLat/Bidual.lean: Introduces the bidual of a Banach lattice and proves
  that the canonical embedding is a lattice homomorphism.

• D BanLat/LLexpr.lean: Defines formal lattice-linear expressions in finitely many
  variables and their evaluation in arbitrary vector lattices. It proves that lattice-
  linear identities valid over R hold in every vector lattice.

• i BanLat/Substructures: Collects definitions and basic facts about the classical
  substructures of Banach lattices: sublattices, ideals, bands, and projection
  bands.

     – D BanLat/Substructures/Sublattice.lean: Defines vector sublattices. It
       proves that closure under one lattice operation or under absolute value
       suﬀices, constructs sublattices generated by a set, describes them through
       sup/inf closures and lattice-linear combinations, and handles topological
       closures.


                                        18
     – D BanLat/Substructures/Ideal.lean: Defines order ideals in vector lat-
       tices. It develops generated and principal ideals, the induced norm on
       principal ideals, sums of ideals, closed order ideals, and the connection
       between strong order units and principal ideals.
     – D BanLat/Substructures/Band/Basic.lean: Defines bands and proves basic
       properties.
     – D BanLat/Substructures/Band/Lattice.lean: Builds the complete lattice
       structure on bands ordered by inclusion. Intersections give infima, with
       the whole space as top and the zero band as bottom.
     – D BanLat/Substructures/Band/DisjointComplement.lean: Defines the dis-
       joint complement of a set and proves its basic laws. It shows disjoint
       complements are bands, and are closed in normed vector lattices.
     – D BanLat/Substructures/Band/Generated.lean: Defines the band gener-
       ated by a set. In Archimedean lattices, the band generated by a set is its
       double disjoint complement. Relates weak order units to principal bands.
       Proves that bands are norm closed in normed lattices.
     – D BanLat/Substructures/Band/Projection.lean: Defines projection
       bands, band projections, and proves the basic properties and characteri-
       zations.
     – D BanLat/Substructures/Band/PPP.lean: Defines the projection property
       and principal projection property. It proves that order complete lattices
       have the projection property, σ-order complete lattices have the princi-
       pal projection property, projection property implies principal projection
       property, and these properties imply the Archimedean property.
     – D BanLat/Substructures/Band/Decomposition.lean: Develops infinite de-
       compositions using principal band projections under PPP.

• i BanLat/Operators: Collects operator theory in vector and Banach lattices.

     – D BanLat/Operators/Hom.lean: Defines vector lattice homomorphism,
       both as a bundled structure and as a predicate. Proves their basic
       properties. Defines a vector lattice equivalence as a bijective vector
       lattice homomorphism. Defines a Banach lattice equivalence as a vector
       lattice homomorphism that is a surjective isometry.
     – D BanLat/Operators/Positive.lean: Defines positive linear operators.
       Proves the extension lemma from additive maps defined on the positive

                                     19
        cone. Proves automatic continuity of positive operators from Banach
        lattices to normed vector lattices.
     – D BanLat/Operators/OrderBounded.lean: Defines order bounded linear
       maps. It proves positive operators are order bounded, order boundedness
       is stable under algebraic operations, order bounded maps from Banach
       lattices are continuous, and the space of order bounded operators is an
       ordered vector space.
     – D BanLat/Operators/Regular.lean: Defines regular operators. It proves
       every regular operator is order bounded.
     – D BanLat/Operators/RieszKantorovich.lean:        Proves the Riesz–
       Kantorovich formulas for order bounded operators into order complete
       vector lattices.

• i BanLat/Convergences: The various notions of convergence in a vector lattice.

     – D BanLat/Convergences/Order.lean: Defines order convergence of nets and
       its basic properties.
     – D BanLat/Convergences/Uniform.lean: Defines uniform convergence and
       uniformly complete vector lattices.
     – D BanLat/OrderContinuous/Basic.lean: Defines σ-order continuous and
       order continuous norms. Proves that every order continuous Banach lat-
       tice is order complete.
     – D BanLat/OrderContinuous/Ando.lean: Ando’s theorem: a Banach lattice
       has order continuous norm if and only if every norm-closed order ideal
       is a band, and in that situation every norm-closed ideal is a projection
       band.
     – D BanLat/OrderContinuous/Decomposition.lean: Proves a decomposition
       theorem for order continuous Banach lattices.
     – D BanLat/OrderContinuous/MeyerNieberg.lean: Formalises Meyer–
       Nieberg’s characterization of order continuous Banach lattices.
     – D BanLat/OrderContinuous/Nakano.lean: Formalises Nakano’s theorem: a
       Banach lattice is order continuous if and only if it is σ-order complete and
       σ-order continuous if and only if every increasing order bounded sequence
       converges.

• i BanLat/AMSpace: The theory of AM-spaces.

                                      20
     – D BanLat/AMSpace/Basic.lean: Defines AM-spaces and AM-spaces with
       unit. Principal ideals in Archimedean vector lattices, equipped with the
       induced norm, are AM-spaces with unit.
     – D BanLat/AMSpace/Max.lean: Proves the AM-norm formula for general
       nonnegative elements (not necessarily disjoint).
     – D BanLat/AMSpace/Maximal.lean: Proves that every proper order ideal lies
       inside a maximal proper order ideal.
     – D BanLat/AMSpace/Characters.lean: Defines characters on an AM-space
       with unit as functionals that are lattice homomorphisms and send the
       unit to 1. Proves a key fact about characters: positive elements attain
       their norm at a character.
     – D BanLat/AMSpace/Kakutani.lean: Proves Kakutani’s representation the-
       orem for AM-spaces.
     – D BanLat/AMSpace/Dual.lean: Shows that the dual of an AM-space is an
       AL-space.

• i BanLat/ALSpace: The theory of AL-spaces.

     – D BanLat/ALSpace/Basic.lean: Defines an AL-space as a Banach lattice
       whose norm is additive on disjoint positive sums.
     – D BanLat/ALSpace/Add.lean: Strengthens the definition to additivity of
       the norm on the positive cone.
     – D BanLat/ALSpace/Dual.lean: Constructs a functional on the dual that
       agrees with the norm on positive elements.
     – D BanLat/ALSpace/DualALAM.lean: Shows that the dual of an AL-space
       is an AM-space with unit. Shows that if the dual is an AL-space, the
       original space is an AM-space, and conversely.
     – D BanLat/ALSpace/OrderContinuous.lean: Shows every AL-space has or-
       der continuous norm.
     – D BanLat/ALSpace/Sublattice.lean: Proves that closed vector sublattices
       of AL-spaces are again AL-spaces with their inherited order and norm
       structure.
     – D BanLat/ALSpace/Kakutani.lean: Proves Kakutani’s representation the-
       orem for AL-spaces.

• i BanLat/Examples: Standard examples of Banach lattices.

                                    21
     – D BanLat/Examples/CofK/Basic.lean: Shows that C(K) is a Banach lat-
       tice, with the usual norm and pointwise operations.
     – D BanLat/Examples/CofK/Dual.lean: Proves that the dual of C(K), as a
       Banach lattice, is M (K).
     – D BanLat/Examples/Lp/Basic.lean: Shows that Lp (µ) is a Banach lattice,
       for all 1 ≤ p.
     – D BanLat/Examples/Lp/Sublattice.lean: Characterizes sublattices of
       Lp (µ), for µ a finite measure and 1 ≤ p < ∞, containing the constant 1
       function.
     – D BanLat/Examples/SignedMeasure/Basic.lean: Proves that finite signed
       measures on a measurable space form a Banach lattice.
     – D BanLat/Examples/MofK/Basic.lean: Defines M (K), the space of regular
       signed Borel measures on a compact Hausdorff space K, as a closed vector
       sublattice of the Banach lattice of finite signed measures on K.
     – D BanLat/Examples/MofK/ALspace.lean: Shows M (K) is an AL-space.
     – D BanLat/Examples/MofK/Atom.lean: Characterises atoms in M (K) as pos-
       itive scalar multiples of Dirac measures.
     – D BanLat/Examples/MofK/Band.lean: Describes principal bands in M (K).
     – D BanLat/Examples/MofK/Decomposition.lean: Develops the decomposi-
       tion of an element of M (K) into its atomic and discrete parts.
     – D BanLat/Examples/MofK/L1space.lean: Proves that M (K) is lattice iso-
       metric to L1 (µ), for some measure µ.

• i BanLat/Free

     – D BanLat/Free/FVL.lean: Constructs the free vector lattice on a type of
       generators α as a concrete vector sublattice of real-valued functions on
       the space α → R.
     – D BanLat/Free/FVLv.lean: Constructs the free vector lattice generated by
       a Banach space as a sublattice of continuous functions on the dual unit
       ball.
     – D BanLat/Free/FBL.lean: Constructs the free Banach lattice over a Banach
       space.

• i BanLat/LocallySolid: The theory of locally solid topologies.

                                     22
        – D BanLat/LocallySolid/Basic.lean: Defines locally solid topological vec-
          tor lattices, and proves basic properties.
        – D BanLat/LocallySolid/Completion.lean: Builds the completion of a
          Hausdorff locally solid vector lattice, endowing it with the structure of a
          Hausdorff locally solid vector lattice.
        – D BanLat/LocallySolid/Lebesgue.lean: Defines Lebesgue, σ-Lebesgue,
          and pre-Lebesgue properties for locally solid vector lattices.
        – D BanLat/LocallySolid/LocallyConvexSolid.lean: Defines locally convex-
          solid vector lattices as locally solid vector lattices with locally convex
          topology. It proves the neighbourhoods of zero admit a basis of sets that
          are at the same time solid and convex.
        – D BanLat/LocallySolid/WithSeminorms.lean: Introduces lattice semi-
          norms. Characterises locally convex-solid linear topologies as those
          induced by families of lattice seminorms.

  • i BanLat/Preliminaries: Preliminary facts required for the library. For now,
    they are only facts about measure theory.

        – D BanLat/Preliminaries/SignedMeasure.lean: Collects facts about signed
          measures. It proves that a sequence of measures that is Cauchy for the
          total variation norm converges.
        – D BanLat/Preliminaries/Regularity.lean: Defines regularity of signed
          measures on compact Hausdorff spaces by regularity of their total varia-
          tion.
        – D BanLat/Preliminaries/HasNoAtoms.lean: Proves that, if µ is a non-
          atomic measure and A is a µ-measurable set, then for every 0 ≤ λ ≤ µ(A)
          there exists B ⊆ A measurable such that µ(B) = λ.

  • i BanLat/Tactic: New tactics implemented in the library.

        – D BanLat/Tactic/LLexpr.lean: Implements the ∀ llarith tactic for lattice-
          linear identities and non-strict inequalities.


5 Extending the library
The following are some natural directions in which the library could be extended.


                                        23
Locally solid topologies Several results about convergence in Banach lattices
     (such as the Meyer-Nieberg and Andô theorems in order continuous Banach
     lattices) can be extended to the more general context of locally solid topologies.

Order continuous operators Develop the theory of (σ-)order continuous opera-
    tors. In particular, prove Ogasawara’s theorem: the families of order contin-
    uous and σ-order continuous operators are band projections on the space of
    order bounded operators, whenever the codomain is order complete.

Orthomorphisms, f-algebras, and universal completions Develop the theory
    of orthomorphisms. This will also require introducing f-algebras, and con-
    structing universal completions.

Nakano theory Define carriers, null ideals, and prove Nakano’s theorem relating
    the carrier and null ideals of disjoint order continuous functionals.

Free Banach lattices Develop further the theory of free Banach and vector lat-
     tices, proving properties about these spaces.

Atomic and order continuous Banach lattices Develop the theory of Banach
    lattices that are at the same time atomic and order continuous.

Enrich the examples Prove further properties about C(K) and Lp (µ): charac-
     terize their ideals, bands, and projection bands; characterize when C(K) is
     (σ)-order complete, etc. In general, lay down the bridges between Banach
     lattice theory and topology/measure theory.

Positively homogeneous function calculus Construct the positively homo-
     geneous function calculus on uniformly complete vector lattices. Define
     p-sums.

Convex/concave Banach lattices and operators Develop                the    theory    of
    convexity of Banach lattices and operators.


Acknowledgements
We would like to thank M. A. Taylor and P. Tradacete for their feedback and contin-
ued support. We are also indebted to J. de Dios for his feedback, and for suggesting
the idea of creating the ∀ llarith tactic. Finally, we thank E. Bilokopytov and M.
de Jeu for feedback on Section 3.


                                          24
    Research supported by an FPI–UAM 2023 contract (funded by Universidad
Autónoma de Madrid), by grants PID2024-162214NB-I00 and CEX2023-001347-S
(funded by MCIN/AEI/10.13039/501100011033), and by the CSIC cooperation grant
COOPB25033 under the i-COOP program.


AI disclosure
GPT-5.5 and Claude Opus 4.6 were used to write the code in § banlat. In the
process of writing the paper, GPT-5.5 was only used to search for typos and other
obvious errors in final versions of the text, and to generate the list of files with their
docstrings (which were later rewritten) in Section 4.


References
 [1]   C. D. Aliprantis. “On the completion of Hausdorff locally solid Riesz spaces”.
       Trans. Amer. Math. Soc., 196:105–125, 1974. MR: 350372.
 [2]   C. D. Aliprantis and O. Burkinshaw. Locally solid Riesz spaces with applications
       to economics, volume 105 of Mathematical Surveys and Monographs. American
       Mathematical Society, Providence, RI, second edition, 2003, pages xii+344.
       MR: 2011364.
 [3]   S. Armstrong. Formalizing Stochastic Homogenization in Lean. https://www.
       scottnarmstrong.com/2026/06/formalizing- stochastic- homogenization- in-
       lean/. [Accessed 03-07-2026].

 [4]   S. Armstrong and T. Kuusi. “Renormalization group and elliptic homogeniza-
       tion in high contrast”. Invent. Math., 242(3):895–1086, 2025. MR: 4978180.
 [5]   A. Avilés, J. Rodríguez, and P. Tradacete. “The free Banach lattice generated
       by a Banach space”. J. Funct. Anal., 274(10):2955–2977, 2018. MR: 3777636.
 [6]   X. Bei, J. Ma, Z. Jing, H. Fu, and Z. G. Tang. Econcslib: a lean library for
       computational economics and ai-assisted research, 2026.
 [7]   S. Bertolini, J. de Dios Pont, B. Pineau, M. A. Taylor, and J. P. G. Ramos.
       L2 -stability for stft phase retrieval, 2026.
 [8]   E. Bilokopytov. “Locally hulled topologies”. Quaest. Math., 48(12):1781–1797,
       2025. MR: 4990562.
 [9]   R. D. Bleier. “Free vector lattices”. Trans. Amer. Math. Soc., 176:73–87, 1973.
       MR: 311541.

                                           25
[10]   S. Boyd and L. Vandenberghe. Convex optimization. Cambridge University
       Press, Cambridge, 2004, pages xiv+716. MR: 2061575.
[11]   J. de Dios Pont, L. Liehr, D. Muñoz-Lahoz, M. A. Taylor, and P. Tradacete.
       “Banach lattices and phase retrieval: a case study for the use of AI in mathe-
       matics”. 2026.
[12]   M. de Jeu. “Free vector lattices over vector spaces as function lattices”. Ordered
       Structures with Applications in Economics and Finance. Proceedings of the
       Online “Conference on Ordered Structures with Applications in Economy and
       Finance”, May 3–7, 2021. Birkhäuser Trends in Mathematics, 2020. M. A. Ben
       Amor and B. A. Watson, editors. Preprint available at https://arxiv.org/
       pdf/2005.01978.pdf. In press.

[13]   M. de Jeu and X. Jiang. “Free Banach lattices over pre-ordered Banach spaces”.
       J. Math. Anal. Appl., 561(2):Paper No. 130706, 30, 2026. MR: 5061846.
[14]   P.-N. Kung, L. Song, D. Hwang, J. Yoon, C.-L. Li, S. Severini, M. Olšák, E.
       Lockhart, Q. V. Le, B. Gokturk, T. Luong, T. Pfister, and N. Peng. Leap:
       supercharging llms for formal mathematics with agentic frameworks, 2026.
[15]   C. C. A. Labuschagne and C. J. van Alten. “On the variety of Riesz spaces”.
       Indag. Math. (N.S.), 18(1):61–68, 2007. MR: 2330732.
[16]   J. Lindenstrauss and L. Tzafriri. Classical Banach spaces. II, volume 97 of
       Ergebnisse der Mathematik und ihrer Grenzgebiete [Results in Mathematics
       and Related Areas]. Springer-Verlag, Berlin-New York, 1979, pages x+243. MR:
       540367. Function spaces.

[17]   P. Meyer-Nieberg. Banach lattices. Universitext. Springer-Verlag, Berlin, 1991,
       pages xvi+395. MR: 1128093.
[18]   D. Muñoz-Lahoz. Wickstead’s conjecture on positive projections and non-
       representable banach lattice algebras, 2026.
[19]   T. Oikhberg, M. A. Taylor, P. Tradacete, and V. G. Troitsky. “Free Banach
       lattices”. J. Eur. Math. Soc. (JEMS), 28(10):4387–4514, 2026. MR: 5089359.
[20]   T. Tao. The integrated explicit analytic number theory network : a progress
       report. Conference talk at Techniques and Tools for the Formalization of Anal-
       ysis, Institute for Computational and Experimental Research in Mathematics
       (ICERM), 2026.
[21]   Tau Ceti Project. Tau ceti. 2026. url: https://github.com/TauCetiProject/
       TauCeti (visited on 07/28/2026).



                                           26
[22]   The mathlib Community. “The Lean mathematical library”. In Proceedings of
       the 9th ACM SIGPLAN International Conference on Certified Programs and
       Proofs, pages 367–381. ACM, 2020.
[23]   A. W. Wickstead. “Banach lattice algebras: some questions, but very few an-
       swers”. Positivity, 21(2):803–815, 2017. MR: 3656022.
[24]   A. W. Wickstead. “Ordered Banach algebras and multi-norms: some open prob-
       lems”. Positivity, 21(2):817–823, 2017. MR: 3656023.
[25]   A. W. Wickstead. “Two dimensional unital Riesz algebras, their representations
       and norms”. Positivity, 21(2):787–801, 2017. MR: 3656021.
[26]   Y. Zhang, Y. Sun, T. Suzuki, J. D. Lee, and F. Liu. Leanmarathon: toward re-
       liable ai co-mathematicians through long-horizon lean autoformalization, 2026.




                                         27
