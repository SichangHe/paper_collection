                                           WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER

                                                                                          COLIN DEFANT


                                                 Abstract. Let Mac(W ) be the MacNeille completion of the Bruhat order of a Coxeter group W .
                                                 We introduce an action of the 0-Hecke monoid of type W on Mac(W ), which allows us to define a
                                                 weak order and a descent set statistic on Mac(W ). When W is of type A, we recover constructions
                                                 of Hamaker and Reiner, which were originally formulated in terms of monotone triangles and
                                                 alternating sign matrices. Using this action, we prove that certain unions of Knutson–Miller subword
arXiv:2605.08033v2 [math.CO] 6 Sep 2026




                                                 complexes are vertex-decomposable. By specializing to type A, we prove a conjecture of Escobar,
                                                 Klein, and Weigandt regarding Cohen–Macaulay ASM varieties. Along the way, we also exhibit a
                                                 counterexample to a conjecture of Hamaker and Reiner regarding the poset topology of intervals in
                                                 the ASM weak order. When W is finite, our action also gives rise to a Boolean cell complex with
                                                 one facet for each element of Mac(W ). We prove that this is an abstract simplicial complex and
                                                 that every linear extension of the weak order on Mac(W ) is a shelling order for its facets. Finally,
                                                 when W is finite and irreducible, we use our 0-Hecke action to introduce a noninvertible dynamical
                                                 system on Mac(W ) that we call the MacNeille pop-stack operator, and we prove that the maximum
                                                 number of iterations of this operator needed to reach the bottom state is h − 1, where h is the
                                                 Coxeter number of W .
                                                    This article is meant to serve as a case study in using large language models to automate the
                                                 workflow of mathematical research. The proof of the conjecture of Escobar–Klein–Weigandt and
                                                 the disproof of the conjecture of Hamaker–Reiner were obtained autonomously by ChatGPT 5.4
                                                 Pro. Other aspects of the paper were obtained mostly by the author, but ChatGPT expedited the
                                                 process. We provide a detailed account of this interaction.




                                                                                        1. Introduction
                                          1.1. MacNeille Completions. Let P be a poset. An order filter of P is a subset F ⊆ P such
                                          that if x ≤ y and x ∈ F , then y ∈ F . For X ⊆ P , let us write
                                                 U(X) = {p ∈ P : p ≥ x for all x ∈ X} and                D(X) = {p ∈ P : p ≤ x for all x ∈ X}.
                                          The MacNeille completion of P , denoted Mac(P ), is the set of all order filters F of P such that
                                          F = U(D(F )). We view Mac(P ) as a poset under the reverse containment order. That is, for
                                          F, F ′ ∈ Mac(P ), we write F ≤ F ′ if F ⊇ F ′ . There is a natural poset embedding ι : P → Mac(P )
                                          given by ι(x) = U({x}).
                                             A complete lattice is a poset in which any subset has a greatest lower bound and a least upper
                                          bound. It is well known that Mac(P ) is the smallest complete lattice (up to isomorphism) containing
                                          a subposet isomorphic to P .
                                          1.2. Coxeter Systems and 0-Hecke Monoids. Let (W, S) be a Coxeter system, and let e be
                                          the identity element of W . For w ∈ W , let ℓ(w) denote the Coxeter length of w, and let
                                                                               Des(w) = {s ∈ S : ℓ(sw) < ℓ(w)}
                                          denote the set of (left) descents of w.
                                            For each s ∈ S, define πs : W → W by
                                                                                          (
                                                                                           sw         if s ∈ Des(w)
                                          (1)                                    πs (w) =
                                                                                           w          if s ̸∈ Des(w).



                                                                                                  1
2                                               COLIN DEFANT


The monoid HW (0) generated by {πs : s ∈ S} is the 0-Hecke monoid of type W . For each w ∈ W ,
we can define πw = πs1 · · · πsk , where s1 · · · sk is a reduced word for w; this is well defined. The
map w 7→ πw is a bijection from W to HW (0).
  We view W as a poset under the (strong) Bruhat order, which we denote by ≤B . For X ⊆ W
and u ∈ W , let
(2)                                      πu (X) = {πu (x) : x ∈ X},
and let
(3)                            ∇(X) = {w ∈ W : x ≤B w for some x ∈ X}.
    Our first theorem is the following.
Theorem 1.1. Let F ∈ Mac(W ) and u ∈ W . We have ∇(πu (F )) ∈ Mac(W ). Moreover, for every
set Y ⊆ W , we have ∇(πu (∇(Y ))) = ∇(πu (Y )).
    The importance of Theorem 1.1 is that it allows us to make the following definition.1
Definition 1.2. Let W be a Coxeter group equipped with the Bruhat order. For each u ∈ W ,
define τu : Mac(W ) → Mac(W ) by
                                        τu (F ) = ∇(πu (F )).
Let the (left) weak order on Mac(W ) be the partial order ≤L defined so that F ≤L F ′ if there exists
u ∈ W such that F = τu (F ′ ). Define the descent set of an order filter F ∈ Mac(W ) to be the set
                                       Des(F ) = {s ∈ S : τs (F ) ̸= F }.
   It follows from Theorem 1.1 that the set {τu : u ∈ W } is a monoid isomorphic to the 0-Hecke
monoid of type W . Thus, the operators τu define an action of the 0-Hecke monoid of W on Mac(W ).
   We will prove that the poset embedding ι : W → Mac(W ) satisfies ι(πu (w)) = τu (ι(w)) for all
u, w ∈ W . This ensures that the weak order and descent set statistic on Mac(W ) introduced in
Definition 1.2 extend the usual weak order and descent set statistics on W .
1.3. The ASM Weak Order. An n × n alternating sign matrix (ASM) is an n × n matrix with
entries in {−1, 0, 1} such that the nonzero entries within each row or column alternate in sign and
sum to 1. Let ASMn be the set of n × n alternating sign matrices. For A = (Aa,b )a,b∈[n] ∈ ASMn
and i, j ∈ [n], define                              XX
                                       rkA (i, j) =       Aa,b .
                                                        a≤i b≤j
We write A ≤B A′ if and only if rkA (i, j) ≥ rkA′ (i, j) for all i, j ∈ [n]. The partial order ≤B is the
Bruhat order on ASMn .
   We can view the symmetric group Sn as a subset of ASMn by identifying each permutation with
its permutation matrix. The restriction of the Bruhat order on ASMn to Sn is the usual Bruhat
order on Sn . It is well known that the map Ψ : ASMn → Mac(Sn ) given by
                                         Ψ(A) = {w ∈ Sn : A ≤B w}
is a poset isomorphism.
   There is a classical bijection between ASMn and a set MTn of combinatorial objects known
as monotone triangles of order n. Hamaker and Reiner [HR20] defined an action of the 0-Hecke
monoid of Sn on MTn , which then allowed them to define a weak order and a descent set statistic on
MTn . By translating from monotone triangles to alternating sign matrices, this produces a 0-Hecke
action, a weak order, and a descent set statistic on ASMn . It is straightforward to verify that their
  1The author thanks Zach Hamaker for originally suggesting this definition, which he formulated together with Vic
Reiner.
                  WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                                      3


definitions agree with those in Definition 1.2 when W = Sn .2 The weak order that Hamaker and
Reiner defined on ASMn , which we also denote by ≤L , is now known as the ASM weak order .
   Given a set J of simple reflections of Sn , we let w◦ (J) denote the long element of the para-
bolic subgroup generated by J. For A, A′ ∈ ASMn with A′ ≤L A, let [A′ , A]L be the interval
between A′ and A in the ASM weak order. Let ∆L (A′ , A) denote the order complex of the open
interval [A′ , A]L \ {A′ , A}. Hamaker and Reiner conjectured that ∆L (A′ , A) is contractible unless
A′ = τw◦ (J) (A) for some J ⊆ Des(A), in which case the order complex is homotopy equivalent to a
(|J| − 2)-dimensional sphere. In Figure 1, we exhibit a counterexample to this conjecture, which
we discovered using ChatGPT 5.4 Pro. The figure shows an interval [A′ , A]L in the ASM weak
order on ASM6 such that ∆L (A′ , A) is not contractible even though A′ is not of the form τw◦ (J) (A).
To see that ∆L (A′ , A) is not contractible, note that µL (A′ , A) = 1 ̸= 0, where µL is the Möbius
function of the ASM weak order.
1.4. ASM Varieties. Fix a field K, and let Matn be the set of n × n matrices with entries in K.
Associated to each alternating sign matrix A ∈ ASMn is the ASM variety
                    XA = {M ∈ Matn : rank(M[i],[j] ) ≤ rkA (i, j) for all i, j ∈ [n]},
where M[i],[j] denotes the restriction of M to its first i rows and its first j columns.
   Let Z = (zi,j )i,j∈[n] be an n×n matrix of variables. Let Rn = K[zi,j : i, j ∈ [n]] be the polynomial
ring in these variables. Let Ik (Z[i],[j] ) be the ideal of Rn generated by the k-minors of the restricted
matrix Z[i],[j] . For A ∈ ASMn , we define the ASM ideal
                                                X
                                        IA =         IrkA (i,j)+1 (Z[i],[j] ).
                                             i,j∈[n]

Then XA is the vanishing locus of IA .
   When A ∈ Sn , the ASM variety XA is called a matrix Schubert variety, and IA is called a
Schubert determinantal ideal . Fulton introduced matrix Schubert varieties [Ful92] and proved that
they are irreducible and Cohen–Macaulay. He also proved that for A ∈ Sn , the codimension of
XA is ℓ(A). One of the primary motivations for studying ASM varieties comes from a result of
Weigandt, which states that they are exactly the intersections of matrix Schubert varieties [Wei17].
   Cohen–Macaulayness is a central homological regularity condition in commutative algebra and
algebraic geometry. It is weak enough to hold for many singular spaces, but strong enough to
rule out several pathologies: Cohen–Macaulay varieties with standard graded coordinate rings are
equidimensional and have well-behaved local cohomology and duality theory. One of our main
results is as follows.
Theorem 1.3. Let A ∈ ASMn . The following are equivalent:
  (i) The ASM weak order interval [e, A]L is graded.
 (ii) For every B ∈ [e, A]L , the permutations in min(Ψ(B)) all have the same Coxeter length.
(iii) For every B ∈ [e, A]L , the ASM variety XB is equidimensional.
(iv) For every B ∈ [e, A]L , the ASM variety XB is Cohen–Macaulay.
   Escobar, Klein, and Weigandt proved the equivalence of (i), (ii), and (iii) in Theorem 1.3, and
they conjectured the equivalence of these conditions to (iv) [EKW, Conjecture 3.21]. In general,
it is still open to fully characterize Cohen–Macaulay ASM varieties. Axelrod–Freed, Hao, Kendall,
Klein, and Luo made some additional progress toward this goal [AFHKKL].
   Our proof of Theorem 1.3 was obtained autonomously by ChatGPT 5.4 Pro.
  2Technically, one must take inverses because Hamaker and Reiner use the right weak order while we use the left
weak order.
4                                         COLIN DEFANT




       Figure 1. An interval [A′ , A]L in the ASM weak order on ASM6 such that the order
       complex ∆L (A′ , A) is not contractible. Below each alternating sign matrix B is the
       set min(Ψ(B)) ⊆ S6 .

1.5. Subword Complexes. Let (W, S) be a Coxeter system. Given a finite word Q over the
alphabet S and an element w ∈ W , we consider the subword complex ∆(Q, w), the abstract
simplicial complex whose faces are the complements of the index sets of the subwords of Q that
contain reduced words for w. Knutson and Miller introduced subword complexes [KM04, KM05],
which have been studied extensively ever since [BC17, EM18, PS15, STW25]. For F ∈ Mac(W ), we
                   WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                                          5


consider the simplicial complex
                                                          [
                                         ∆(Q, F ) =               ∆(Q, w),
                                                      w∈min(F )

where min(F ) is the set of minimal elements of F (in Bruhat order).
  One of the main intermediary steps needed for the proof of Theorem 1.3 is as follows.
Theorem 1.4. Let F ∈ Mac(W ). Assume that for every F ′ ∈ Mac(W ) with F ′ ≤L F , the minimal
elements of F ′ all have the same Coxeter length. Then ∆(Q, F ) is vertex-decomposable for every
finite word Q over S.
1.6. MacNeille Pop-Stack Operators. Let us now assume that the Coxeter system (W, S) is
finite and irreducible. Let w◦ denote the long element of W . For J ⊆ S, let WJ be the parabolic
subgroup generated by J, and let w◦ (J) be the long element of WJ .
Definition 1.5. Let (W, S) be a finite irreducible Coxeter system. Define the MacNeille pop-stack
operator MacPop : Mac(W ) → Mac(W ) by
                                         MacPop(F ) = τw◦ (Des(F )) (F ).
   In a previous article [Def22B], the author introduced the pop-stack operator of W , which is the
map Pop : W → W defined by Pop(x) = πw◦ (Des(x)) (x). When W = Sn , this is the classical pop-
stack sorting map from enumerative combinatorics and computer science [CG19, CGP23, EG21].
We will show that
(4)                                       ι(Pop(x)) = MacPop(ι(x))
for every x ∈ W , so the MacNeille pop-stack operator extends the pop-stack operator.3
   We view MacPop : Mac(W ) → Mac(W ) as a noninvertible dynamical system. If we start at an
arbitrary element F ∈ Mac(W ) and then repeatedly apply MacPop, we will eventually reach the
order filter W = ι(e), which is the minimum element of Mac(W ). Thus, it is natural to define
                             gMacPop (F ) = min{t ∈ Z≥0 : MacPopt (F ) = W }.
We are interested in the quantity
                                      GMac(W ) =       max       gMacPop (F ).
                                                    F ∈Mac(W )

Similarly, for x ∈ W , we can define
                                   gPop (x) = min{t ∈ Z≥0 : Popt (x) = e}
and consider the quantity
                                              GW = max gPop (x).
                                                       x∈W
The author proved that GW = h − 1, where h is the Coxeter number of W [Def22B, Theorem 1.3].
It follows from (4) that gPop (x) = gMacPop (ι(x)) for every x ∈ W . Thus,
(5)                                        h − 1 = GW ≤ GMac(W ) .
  The following result shows that the maximum orbit lengths of the MacNeille pop-stack operator
can be obtained by starting at an element of ι(W ).
Theorem 1.6. Let (W, S) be a finite irreducible Coxeter system with Coxeter number h. We have
                                               GMac(W ) = h − 1.
  3The author has introduced a pop-stack operator on any finite lattice [Def22A]. This definition agrees with the
Coxeter-theoretic definition from [Def22B] when the lattice is the weak order on W . Since Mac(W ) is also a lattice,
we can consider the lattice-theoretic pop-stack operator on Mac(W ). This operator, however, is generally not the
same as the MacNeille pop-stack operator.
6                                         COLIN DEFANT


1.7. MacNeille Complexes. Assume that (W, S) is finite. For J ⊆ S, let w◦ (J) be the long
element of the parabolic subgroup generated by J, and define
                                        pJ (F ) = τw◦ (J) (F )
for F ∈ Mac(W ). Following a suggestion of Hamaker and Reiner, one can use these parabolic
projections to glue together simplices indexed by the elements of Mac(W ). The resulting Boolean
cell complex, which we call the MacNeille complex of (W, S), has facets naturally indexed by
Mac(W ). When W = Sn , it agrees with the complex that Hamaker and Reiner constructed from
partial monotone triangles. A Boolean cell complex need not be an abstract simplicial complex
because distinct faces can have the same set of vertices. Our next result shows that this pathology
never occurs for MacNeille complexes.
Theorem 1.7. Let (W, S) be a finite Coxeter system. The MacNeille complex of (W, S) is a pure
(|S| − 1)-dimensional abstract simplicial complex. Moreover, every linear extension of the weak
order on Mac(W ) is a shelling order for its facets.
1.8. Outline. In Section 2, we prove Theorem 1.1, showing that the notions in Definition 1.2 are
well defined. In Section 3, we discuss subword complexes and prove Theorem 1.4. Section 4 discusses
Stanley–Reisner rings and Cohen–Macaulayness and proves Theorem 1.3. We prove Theorem 1.6
in Section 5. In Section 6, we define the MacNeille complex and prove Theorem 1.7.
   In Section 7, we discuss the use of ChatGPT in producing this manuscript, especially for proving
Theorem 1.3. We provide a table summarizing several conversations the author had with ChatGPT
in an attempt to see which types of prompt led to success.

                                  2. Defining Weak Order
   The purpose of this section is to prove Theorem 1.1. We begin with some lemmas that pertain
to an arbitrary poset P .
Lemma 2.1. Let P be a poset. For each subset X ⊆ P , we have X ⊆ U(D(X)) and X ⊆ D(U(X)).
Proof. We will only prove that X ⊆ U(D(X)) since the proof of the other containment is completely
analogous. Choose x ∈ X. We wish to show that x ∈ U(D(X)), so we need to show that x ≥ x′
for every x′ ∈ D(X). This is immediate from the definition of D(X).                            □
Lemma 2.2. Let P be a poset. If X ⊆ P , then U(X) = U(D(U(X))).
Proof. Let Y = U(X). We know by Lemma 2.1 that Y ⊆ U(D(Y )), so U(X) ⊆ U(D(U(X))). On
the other hand, because X ⊆ D(U(X)) by Lemma 2.1, we must have U(X) ⊇ U(D(U(X))).   □
Corollary 2.3. An order filter F of P is in Mac(P ) if and only if F = U(X) for some X ⊆ P .
Proof. If F ∈ Mac(P ), then F = U(D(F )) by the definition of Mac(P ). Conversely, if F = U(X)
for some X ⊆ P , then it follows from Lemma 2.2 that F = U(D(F )), so F ∈ Mac(P ).           □
  We now specialize our attention to the case where P is a Coxeter group W endowed with the
Bruhat order. Let S be the set of simple reflections of W . Recall the definitions from (1), (2),
and (3). We say a map φ : W → W is order-preserving if for all x, y ∈ W with x ≤B y, we
have φ(x) ≤B φ(y). For each s ∈ S, it follows from the Lifting Property of the Bruhat order
[BB05, Proposition 2.2.7] that the map πs : W → W is order-preserving. As a consequence, for
every u ∈ W , the map πu : W → W is order-preserving.
Lemma 2.4. For X ⊆ W and s ∈ S, we have U(πs (X)) = ∇(πs (U(X))).
Proof. We first show that U(πs (X)) ⊆ ∇(πs (U(X))). Choose u ∈ U(πs (X)). Our goal is to show
that there exists w ∈ U(X) such that πs (w) ≤B u.
                 WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                             7


  First, suppose s ∈ Des(u). If x ∈ X, then πs (x) ≤B u by the choice of u. Since s ∈ Des(u), we
must actually have x ≤B u. This shows that u ∈ U(X), so we can put w = u.
  Next, suppose s ̸∈ Des(u). For every x ∈ X, we have πs (x) ≤B u, so x ≤B su. This shows that
su ∈ U (X), so we can put w = su.
  We now need to prove the reverse containment ∇(πs (U(X))) ⊆ U(πs (X)). The map πs is order-
preserving. It follows that if v ∈ U(X), then πs (x) ≤B πs (v) for all x ∈ X, so πs (v) ∈ U(πs (X)).
This shows that πs (U(X)) ⊆ U(πs (X)). Because U(πs (X)) is an order filter, we must have
∇(πs (U(X))) ⊆ U(πs (X)).                                                                         □
  We are now in a position to prove Theorem 1.1, which states that for F ∈ Mac(W ), u ∈ W , and
Y ⊆ W , we have ∇(πu (F )) ∈ Mac(W ) and ∇(πu (∇(Y ))) = ∇(πu (Y )).
Proof of Theorem 1.1. Choose F ∈ Mac(W ), u ∈ W , and Y ⊆ W . We proceed by induction
on ℓ(u), noting that the case where ℓ(u) = 0 is trivial since πe is the identity operator. Let us
first assume that u = s ∈ S. Let X = D(F ). We have F = U(X), so Lemma 2.4 implies that
∇(πs (F )) = U(πs (X)). It follows from Corollary 2.3 that ∇(πs (F )) ∈ Mac(W ). The containment
∇(πs (∇(Y ))) ⊇ ∇(πs (Y )) is immediate, so we must prove the reverse containment. To do so,
it suffices to show that πs (∇(Y )) ⊆ ∇(πs (Y )). Choose x ∈ πs (∇(Y )), and write x = πs (z) for
some z ∈ ∇(Y ). There exists y ∈ Y such that y ≤B z. Since πs is order-preserving, we have
πs (y) ≤B πs (z) = x. Since πs (y) ∈ πs (Y ), this shows that x ∈ ∇(πs (Y )), as desired.
   Now suppose ℓ(u) > 1, and write u = sv for some s ∈ Des(u). We know by induction that
∇(πv (F )) ∈ Mac(W ), so it follows from the preceding paragraph that
                            ∇(πu (F )) = ∇(πs (πv (F )))
                                       = ∇(πs (∇(πv (F )))) ∈ Mac(W ).
By repeated application of the induction hypothesis, we find that
                               ∇(πu (∇(Y ))) = ∇(πs (πv (∇(Y ))))
                                             = ∇(πs (∇(πv (∇(Y )))))
                                             = ∇(πs (∇(πv (Y ))))
                                             = ∇(πs (πv (Y )))
                                             = ∇(πu (Y )),
as desired.                                                                                        □
  Recall that ι : W → Mac(W ) is the poset embedding defined by ι(x) = U({x}). For all u, w ∈ W ,
the fact that πu : W → W is order-preserving implies that
(6)                                     ι(πu (w)) = τu (ι(w)).

                                    3. Subword Complexes
   Let V be a finite set. Let ∆ be an abstract simplicial complex with vertex set V . That is, ∆ is
a collection of subsets of V such that if D ∈ ∆ and D′ ⊆ D, then D′ ∈ ∆. The sets in ∆ are called
faces, and the inclusion-maximal faces are called facets. For v ∈ V , the deletion of v from ∆ is the
abstract simplicial complex
                                    delv (∆) = {D ∈ ∆ : v ̸∈ D},
and the link of v in ∆ is the abstract simplicial complex
                             lkv (∆) = {D ∈ delv (∆) : (D ∪ {v}) ∈ ∆}.
We say ∆ is vertex-decomposable if either of the following hold:
     • ∆ is a simplex (i.e., has a unique facet) or is empty;
8                                             COLIN DEFANT


      • there exists a vertex v such that delv (∆) and lkv (∆) are both vertex-decomposable and
        every facet of delv (∆) is a facet of ∆.
   A reduced word for an element w ∈ W is a word of length ℓ(w) over S whose product is w.
Let Q be a finite word over S. Formally, we view Q as a function from a set V ⊂ Z to S. If
V = {k1 < · · · < kt }, then we can write Q = (sk1 , . . . , skt ), where ski is the image of ki under this
function. For V ′ ⊆ V , we write Q|V ′ for the restriction of Q to V ′ . The subword complex ∆(Q, w)
is the abstract simplicial complex with vertex set V whose faces are the sets D such that Q|V \D
contains a reduced word for w. For F ∈ Mac(W ), we are interested in the abstract simplicial
complex                                             [
                                     ∆(Q, F ) :=              ∆(Q, w).
                                                  w∈min(F )
  Our aim in this section is to prove Theorem 1.4. The key point is the following lemma, which
makes use of the 0-Hecke action on Mac(W ).
Lemma 3.1. Fix F ∈ Mac(W ) and a nonempty finite word Q over S with index set V . Write
V = {k1 < · · · < kt }, and let V ′ = V \ {k1 }. Write Q = sQ′ , where s ∈ S and Q′ = Q|V ′ . We have
                                    delk1 (∆(Q, F )) = ∆(Q′ , τs (F )).
Proof. Observe that a set D ⊆ V ′ is a face of delk1 (∆(Q, F )) if and only if sQ′ |V ′ \D contains a
reduced word for an element of min(F ). In addition, note that because πs is order-preserving, we
have
                                  min(τs (F )) ⊆ {πs (w) : w ∈ min(F )}.
    Suppose D is a face of delk1 (∆(Q, F )). Then sQ′ |V ′ \D contains a reduced word w for an element w
of min(F ). If w uses the initial s in sQ′ |V ′ \D , then s ∈ Des(w), so sw = πs (w) ∈ τs (F ). Deleting the
initial s from w yields a reduced word v for πs (w) contained in Q′ |V ′ \D . There exists y ∈ min(τs (F ))
such that y ≤B πs (w), and v contains a reduced word for y, so D ∈ ∆(Q′ , τs (F )). On the other
hand, if w does not use the initial s, then sQ′ |V ′ \D already contains w, which in turn contains a
reduced word for πs (w) since πs (w) ≤B w. In this case, we again conclude that D ∈ ∆(Q′ , τs (F )).
This shows that delk1 (∆(Q, F )) ⊆ ∆(Q′ , τs (F )).
    To prove the reverse containment, assume now that D ∈ ∆(Q′ , τs (F )). Then Q′ |V ′ \D contains a
reduced word u for an element u ∈ min(τs (F )). We have u = πs (u′ ) for some u′ ∈ min(F ). Since
the word su contains a reduced word for u′ , it follows that sQ′ |V ′ \D contains a reduced word for
u′ . Hence, D ∈ delk1 (∆(Q, F )).                                                                         □
Proof of Theorem 1.4. Fix F ∈ Mac(W ) and a finite word Q over S with index set V ⊂ Z. Assume
that for every F ′ ∈ Mac(W ) with F ′ ≤L F , all elements of min(F ′ ) have the same Coxeter length.
Our goal is to prove that ∆(Q, F ) is vertex-decomposable. We proceed by induction on |V |.
   Write V = {k1 < · · · < kt }, and let V ′ = V \ {k1 }. Write Q = sQ′ , where s ∈ S and Q′ = Q|V ′ .
It is immediate from the definitions that
                                       lkk1 (∆(Q, F )) = ∆(Q′ , F ),
so we know by induction that lkk1 (∆(Q, F )) is vertex-decomposable. Lemma 3.1 tells us that
                                    delk1 (∆(Q, F )) = ∆(Q′ , τs (F )).
For every F ′ ∈ Mac(W ) with F ′ ≤L τs (F ), we have F ′ ≤L F , so all elements of min(F ′ ) have
the same Coxeter length. Thus, we can apply induction to deduce that delk1 (∆(Q, F )) is vertex-
decomposable.
  If s ̸∈ Des(F ), then τs (F ) = F , so delk1 (∆(Q, F )) = ∆(Q′ , F ) = lkk1 (∆(Q, F )). This says that
every face in ∆(Q′ , F ) can be extended to a face of ∆(Q, F ) by adding k1 , so ∆(Q, F ) is a cone
over ∆(Q′ , F ). It is a standard fact that a cone over a vertex-decomposable simplicial complex is
vertex-decomposable; hence, ∆(Q, F ) is vertex-decomposable in this case.
                 WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                               9


    Now assume s ∈ Des(F ) so that τs (F ) ̸= F . Let D ⊆ V ′ be a facet of ∆(Q′ , τs (F )); we aim
to show that D is also a facet of ∆(Q, F ). Note that Q′ |V ′ \D is a reduced word w for an element
w ∈ min(τs (F )). All minimal elements of τs (F ) have the same Coxeter length, say m. Similarly, all
minimal elements of F have the same Coxeter length. Since min(τs (F )) ⊆ {πs (u) : u ∈ min(F )} and
τs (F ) ̸= F , the minimal elements of F all have Coxeter length m + 1. Consequently, w = πs (sw),
where sw ∈ min(F ). It follows that Q|V \D = sw is a reduced word for sw, so D is a facet of
∆(Q, F ).                                                                                          □
   The preceding inductive proof of Theorem 1.4 is somewhat routine. A similar argument appears
in Jahn’s thesis [Jah22], which is a precursor for studying unions of subword complexes.

                              4. Cohen–Macaulay ASM Varieties
  In this section, we will prove Theorem 1.3. We first need a few more definitions.
  Let XV = {xv : v ∈ V } be a set of variables indexed by a finite set
                                                                     Q V , and let K[XV ] be the
corresponding polynomial ring over the field K. For D ⊆ V , let xD = v∈D xv . Given a simplicial
complex ∆ with vertex set V , we define the Stanley–Reisner ideal to be the ideal
                                     I∆ := (xD : D ̸∈ ∆) ⊆ K[XV ]
generated by the monomials indexed by the non-faces of ∆. The Stanley–Reisner ring of ∆ is
                                           K[∆] := K[XV ]/I∆ .
We say ∆ is pure if all of its facets have the same cardinality.
   A Noetherian ring is Cohen–Macaulay if each of its localizations at a prime ideal has depth equal
to its Krull dimension. A simplicial complex ∆ is Cohen–Macaulay over K if its Stanley–Reisner
ring K[∆] is Cohen–Macaulay. We will use the standard fact that a pure vertex-decomposable
simplicial complex is Cohen–Macaulay over every field.
   If ⪯ is a term order on a polynomial ring and I is an ideal, then in⪯ (I) denotes the initial ideal
of I, which is the ideal generated by the initial monomials of the elements of I. An antidiagonal
term order on the polynomial ring Rn := K[zi,j : i, j ∈ [n]] is a term order with the property that
the initial monomial of each minor of the matrix Z = (zi,j )i,j∈[n] is the product of the entries on
its antidiagonal. Explicitly, if the minor uses rows a1 < · · · < ar and columns b1 < · · · < br , then
its antidiagonal monomial is
                                        za1 ,br za2 ,br−1 · · · zar ,b1 .
Proof of Theorem 1.3. Let A ∈ ASMn . Escobar, Klein, and Weigandt already proved the equiva-
lence of the statements (i), (ii), and (iii) (see [EKW, Propositions 2.4 & 3.20]). They also noted
that (iv) implies (iii) because Cohen–Macaulay varieties with standard graded coordinate rings are
always equidimensional. Thus, we just need to show that (ii) implies (iv).
   Suppose that for every B ∈ [e, A]L , all minimal elements of the order filter Ψ(B) have the same
Coxeter length. Fix B ∈ [e, A]L , and let F = Ψ(B). It follows from Theorem 1.4 that ∆(Q, F ) is
vertex-decomposable for every finite word Q over the simple reflections of Sn . We will prove that
XB is Cohen–Macaulay.
   Let
                                  Λn = {(i, j) ∈ [n] × [n] : i + j ≤ n}
be the staircase Young diagram (in English conventions), where (i, j) represents the box in row i
and column j. Order Λn by reading rows from top to bottom and, within each row, from right to
left. Mapping each pair (i, j) to the simple reflection si+j−1 yields the word
                         Qn = (sn−1 sn−2 · · · s1 )(sn−1 sn−2 · · · s2 ) · · · (sn−1 ).
This word Qn is a reduced word for the long element of Sn , so every permutation in Sn has a
reduced word appearing as a subword of Qn . By assumption, all elements of min(F ) have the same
10                                         COLIN DEFANT


Coxeter length, say m. Every facet of ∆(Qn , F ) is the complement of a reduced word for some
element of min(F ), so every facet has cardinality n2 − m. Thus, ∆(Qn , F ) is pure. We view the
Stanley–Reisner ideal I∆(Qn ,F ) as an ideal of R′n := K[zi,j : (i, j) ∈ Λn ], which is contained in
the polynomial ring Rn = K[zi,j : i, j ∈ [n]]. Since ∆(Qn , F ) is vertex-decomposable, its Stanley–
Reisner ring R′n /I∆(Qn ,F ) = K[∆(Qn , F )] is Cohen–Macaulay.
   We now relate the Stanley–Reisner ring K[∆(Qn , F )] to the ASM ideal IB . Weigandt [Wei17,
Proposition 5.4] proved that the minimal prime decomposition of IB is given by
                                                    \
                                           IB =         Iw .
                                                  w∈min(F )

Let ⪯ be an antidiagonal term order on Rn .           Axelrod–Freed, Hao, Kendall, Klein, and Luo
[AFHKKL, Proposition 3.8] proved that
                                                     \
                                    in⪯ (IB ) =               in⪯ (Iw ).
                                                  w∈min(F )

For each w ∈ Sn , Knutson and Miller’s pipe-dream degeneration theorem [KM05, Theorem B]
identifies in⪯ (Iw ) with the Stanley–Reisner ideal of the subword complex ∆(Qn , w). Hence,
                                          \
                             in⪯ (IB ) =        I∆(Qn ,w) Rn = I∆(Qn ,F ) Rn .
                                      w∈min(F )

It follows that Rn / in⪯ (IB ) is a polynomial extension of K[∆(Qn , F )]. Therefore Rn / in⪯ (IB )
is Cohen–Macaulay. Axelrod–Freed, Hao, Kendall, Klein, and Luo [AFHKKL, Proposition 3.10]
proved that Rn /IB is Cohen–Macaulay if and only if Rn / in⪯ (IB ) is Cohen–Macaulay. This shows
that Rn /IB is Cohen–Macaulay, so XB is Cohen–Macaulay.                                         □

                             5. MacNeille Pop-Stack Operators
  Let us now assume that the Coxeter system (W, S) is finite and irreducible. For J ⊆ S, let WJ
be the parabolic subgroup generated by J, and let w◦ (J) be the long element of WJ . Recall from
Definition 1.5 that we define the MacNeille pop-stack operator MacPop : Mac(W ) → Mac(W ) by
                                   MacPop(F ) = τw◦ (Des(F )) (F ).
The pop-stack operator of W is the map Pop : W → W defined by
                                      Pop(x) = πw◦ (Des(x)) (x).
For each u ∈ W , the fact that πu is order-preserving implies that ι(πu (x)) = τu (ι(x)) for every
x ∈ W . In particular,
                                  ι(Pop(x)) = MacPop(ι(x))
for every x ∈ W .
   Let W J denote the set of minimum-length representatives of the left cosets in W/WJ . Every
element w ∈ W has a unique factorization of the form w = wJ wJ , where wJ ∈ W J and wJ ∈ WJ .
Lemma 5.1. Fix s ∈ S, and let J = S\{s}. For every integer t ≥ 0, the elements of Des(Popt (w◦J ))
commute pairwise.
Proof. First suppose that the Coxeter number h of W is even. The desired statement then follows
from [Def22B, Proposition 3.4] after applying inversion to switch from right descents and right
weak order to left descents and left weak order.
   Now suppose that h is odd. By the classification of finite irreducible Coxeter systems, W is
either of type Ah−1 or of type I2 (h). First assume W is of type Ah−1 so that we may identify W
with Sh and write S = {s1 , . . . , sh−1 }, where si = (i i + 1). Say s = si . The set W J is an order
ideal in left weak order, and Pop(v) ≤L v for every v ∈ W . Hence, if v = Popt (w◦J ), then v ∈ W J .
                  WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                                  11


Consequently, we have v(1) < · · · < v(i) and v(i + 1) < · · · < v(h). If sm and sm+1 were both left
descents of v, then we would have
                                 v −1 (m) > v −1 (m + 1) > v −1 (m + 2).
Among the three entries m, m + 1, m + 2, two would lie in the same one of the two increasing blocks
displayed above, which is impossible. Thus, no two elements of Des(v) are adjacent in the Coxeter
diagram, so they commute pairwise.
   Finally, suppose that W is of type I2 (h). The element w◦ is the only element of W with both
simple reflections as left descents. Since w◦J ̸= w◦ and Popt (w◦J ) ≤L w◦J , the descent set of Popt (w◦J )
has at most one element. Hence, its elements commute pairwise.                                           □
Lemma 5.2. Let F ∈ Mac(W ). Fix s ∈ S, and let J = S \ {s}. For each integer t ≥ 0, there
exists a minimal element b of the order filter MacPopt (F ) such that bJ ≤B Popt (w◦J ).
Proof. We proceed by induction on t. If t = 0, then the result is immediate because F is nonempty
and w◦J is the maximum element of W J .
  Now assume t ≥ 1, and let
                            Ft−1 = MacPopt−1 (F )      and K = Des(Ft−1 ).
By the induction hypothesis, there exists a minimal element a of Ft−1 such that
                                           aJ ≤B Popt−1 (w◦J ).
By Lemma 5.1, all of the left descents of Popt−1 (w◦J ) commute with each other. Therefore, the
left-handed version of [Def22B, Lemma 3.5], obtained by applying inversion, yields that
                                         Pop(aJ ) ≤B Popt (w◦J ).
  Now let x = πw◦ (K) (a). Since a ∈ Ft−1 , we have
               x ∈ πw◦ (K) (Ft−1 ) ⊆ ∇(πw◦ (K) (Ft−1 )) = MacPop(Ft−1 ) = MacPopt (F ).
Choose a minimal element b of the order filter MacPopt (F ) such that b ≤B x.
   We claim that bJ ≤B Pop(aJ ). To prove this, we first show that Des(a) ⊆ K. Indeed, let
r ∈ Des(a). Then πr (a) = ra ≤B a. Because a is a minimal element of the order filter Ft−1 , it
follows that ra ∈
                / Ft−1 . On the other hand,
                          ra = πr (a) ∈ πr (Ft−1 ) ⊆ ∇(πr (Ft−1 )) = τr (Ft−1 ).
Thus, τr (Ft−1 ) ̸= Ft−1 , so r ∈ Des(Ft−1 ) = K, as desired.
  Since Des(a) ⊆ K, we have
                                          w◦ (Des(a)) ≤L w◦ (K).
Consequently,
                                x = πw◦ (K) (a) ≤L πw◦ (Des(a)) (a) = Pop(a).
Applying the parabolic projection w 7→ wJ , which is order-preserving for left weak order, we find
that xJ ≤L (Pop(a))J . It follows from [Def22B, Lemma 3.6] that (Pop(a))J ≤L Pop(aJ ). Hence,
                                             xJ ≤L Pop(aJ ).
Since weak order refines Bruhat order, it follows that
                                             xJ ≤B Pop(aJ ).
Finally, because b ≤B x and the map w 7→ wJ is order-preserving for Bruhat order, we have
                                  bJ ≤B xJ ≤B Pop(aJ ) ≤B Popt (w◦J ),
as desired.                                                                                               □
12                                         COLIN DEFANT


  We are now in a position to prove Theorem 1.6, which states that GMac(W ) = h − 1, where
GMac(W ) is the maximum number of iterations of MacPop needed to send elements of Mac(W ) to
the bottom element W and h is the Coxeter number of W .
Proof of Theorem 1.6. We already saw in (5) that h − 1 ≤ GMac(W ) , so we just need to prove the
reverse inequality. Fix F ∈ Mac(W ); our goal is to show that MacPoph−1 (F ) = W .
   For each s ∈ S, we know by Lemma 5.2 that there exists an element bs ∈ MacPoph−1 (F ) such
       S\{s}               S\{s}                                 S\{s}
that bs      ≤B Poph−1 (w◦       ). We also know that Poph−1 (w◦       ) = e since it is known that
GW = h − 1 [Def22B, Theorem 1.3]. It follows that bs ∈ WS\{s} for every s ∈ S. Thus, for every
s ∈ S, the order filter MacPoph−1 (F ) contains an element of WS\{s} . Each parabolic subgroup
WS\{s} is an order ideal in the Bruhat order, so every element of D(MacPoph−1 (F )) belongs to the
intersection s∈S WS\{s} . However, this intersection is {e}, so D(MacPoph−1 (F )) = {e}. Finally,
             T

                     MacPoph−1 (F ) = U(D(MacPoph−1 (F ))) = U({e}) = W,
as desired.                                                                                         □

                                    6. MacNeille Complexes
  Throughout this section, assume that (W, S) is finite. For J ⊆ S, let WJ be the parabolic
subgroup generated by J, let w◦ (J) be the long element of WJ , and define pJ = τw◦ (J) : Mac(W ) →
Mac(W ). The 0-Hecke relations imply that
(7)                           pK ◦ pJ = pK      whenever J ⊆ K ⊆ S.
In particular, each pJ is idempotent.
   Let
                         FMac (W, S) = {(J, E) : J ⊆ S and E ∈ pJ (Mac(W ))}.
We partially order FMac (W, S) by declaring that (J ′ , E ′ ) ≤ (J, E) if and only if J ′ ⊇ J and
E ′ = pJ ′ (E). It follows from (7) that this is indeed a partial order. Because πw◦ (w) = e for every
w ∈ W , we have pS (F ) = W for every F ∈ Mac(W ). Hence, the unique minimum element is
(S, W ), while the maximal elements are the pairs (∅, F ) with F ∈ Mac(W ). Moreover, the interval
below (J, E) is {(K, pK (E)) : J ⊆ K ⊆ S}, which is isomorphic to the Boolean lattice 2S\J . Thus,
FMac (W, S) is a simplicial poset. We call its associated Boolean cell complex the MacNeille complex
of (W, S) and denote it by ∆Mac (W, S).
   For s ∈ S and a facet F ∈ Mac(W ), let vs (F ) = (S \ {s}, pS\{s} (F )). Let
                                       CF = {vs (F ) : s ∈ S}.
Then CF is the vertex set of F . By (6), we have
                                      pJ (ι(w)) = ι(πw◦ (J) (w))
for all J ⊆ S and w ∈ W . Consequently, the facets indexed by the principal filters ι(w) form a
subcomplex naturally isomorphic to the Coxeter complex of (W, S).
   When W = Sn , the complex ∆Mac (W, S) recovers the complex studied by Hamaker and Reiner.
Indeed, under the identification of Mac(Sn ) with monotone triangles mentioned in Section 1.3,
[HR20, Proposition 4.1] states that pJ fixes the rows corresponding to the simple reflections outside
of J and replaces the other rows by their unique componentwise-minimal completion. Hence, the
face (J, pJ (F )) records the partial monotone triangle obtained by deleting the rows corresponding
to the elements of J.
   We now prove the identity that will allow us to recover each face from its vertices. For I ⊆ S,
let
                                        ρI = πw◦ (I) : W → I W,
                 WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                              13


where I W is the set of minimum-length representatives of the cosets in WI \W . Thus, ρI (w) is the
minimum-length element of the coset WI w.
Lemma 6.1. For every F ∈ Mac(W ) and J ⊆ S, we have
                                        \
                              pJ (F ) =     pS\{s} (F ),
                                                s∈S\J

where the intersection on the right is understood to be W when J = S.
Proof. Iterating Lemma 2.4 along a reduced word for w◦ (I), we find that pI (F ) = U(ρI (D(F ))) for
every I ⊆ S. Consequently,
(8)                   y ∈ pI (F ) if and only if ρI (d) ≤B y for every d ∈ D(F ).
  Suppose first that y ∈ pJ (F ), and fix s ∈ S \ J. For each d ∈ D(F ), we have ρJ (d) ≤B y. Because
J ⊆ S \ {s}, we also have ρS\{s} ◦ ρJ = ρS\{s} . It follows that
                              ρS\{s} (d) = ρS\{s} (ρJ (d)) ≤B ρJ (d) ≤B y.
Hence, y ∈ pS\{s} (F ) by (8). This proves one containment.
   Conversely, suppose that y ∈ pS\{s} (F ) for every s ∈ S \ J. Fix d ∈ D(F ). By (8), we have
ρS\{s} (d) ≤B y for every s ∈ S \ J. Applying the order-preserving map ρS\{s} to each of these
inequalities and using idempotence, we obtain that ρS\{s} (d) ≤B ρS\{s} (y) for every s ∈ S \ J.
Using ρS\{s} ◦ ρJ = ρS\{s} , we can rewrite these inequalities as
                                   ρS\{s} (ρJ (d)) ≤B ρS\{s} (ρJ (y))
for every s ∈ S \ J. Both ρJ (d) and ρJ (y) belong to J W . It follows from [Ste05, Corollary 1.4] that
                                        ρJ (d) ≤B ρJ (y) ≤B y.
Since this holds for every d ∈ D(F ), (8) implies that y ∈ pJ (F ).                                  □
  We are now in a position to prove Theorem 1.7.
Proof of Theorem 1.7. Consider a face (J, E) of ∆Mac (W, S). Its vertices are
                                  {(S \ {s}, pS\{s} (E)) : s ∈ S \ J}.
These vertices determine J. Because E ∈ im(pJ ), we have pJ (E) = E, so Lemma 6.1 gives
                                          \
                                     E=         pS\{s} (E).
                                              s∈S\J

Thus, every face is determined by its set of vertices. It follows that the Boolean cell complex
∆Mac (W, S) is an abstract simplicial complex. Each facet has one vertex of type S \ {s} for every
s ∈ S, so this complex is pure of dimension |S| − 1.
   It remains to prove shellability. We follow the argument in [HR20, Section 4]. Let F1 , . . . , FN
be a linear extension of the weak order on Mac(W ), and write Ci = CFi . A standard criterion
for shellings states that it suffices to prove that whenever i < j, there exists k < j such that
Ci ∩ Cj ⊆ Ck ∩ Cj and Ck ∩ Cj is a ridge of Cj .
   Fix i < j, and let J = {s ∈ S : vs (Fi ) ̸= vs (Fj )}. We claim that J ∩ Des(Fj ) is nonempty.
Suppose otherwise. Then τs (Fj ) = Fj for every s ∈ J, so pJ (Fj ) = Fj . On the other hand,
Lemma 6.1 and the definition of J imply that
                               \                    \
                    pJ (Fi ) =       pS\{s} (Fi ) =    pS\{s} (Fj ) = pJ (Fj ) = Fj .
                              s∈S\J               s∈S\J

Hence, Fj ≤L Fi , contradicting the fact that Fi appears before Fj in a linear extension.
14                                          COLIN DEFANT


  Choose s ∈ J ∩ Des(Fj ), and let Fk = τs (Fj ). Then Fk <L Fj , so k < j. If t ̸= s, then s ∈ S \ {t},
and (7) gives
                             pS\{t} (Fk ) = pS\{t} (τs (Fj )) = pS\{t} (Fj ).
Thus, Ck and Cj have the same vertex of type S \ {t} for every t ̸= s. Since Fk ̸= Fj and facets
are determined by their vertex sets, their vertices of type S \ {s} are different. Therefore,
                                      Ck ∩ Cj = Cj \ {vs (Fj )},
which is a ridge of Cj . Since s ∈ J, we also have Ci ∩ Cj ⊆ Ck ∩ Cj . This proves that C1 , . . . , CN
is a shelling.                                                                                        □

                                            7. AI Usage
   The initial seed of this project was planted in 2022, when Zach Hamaker told the author about
an idea he and Vic Reiner had discussed that did not make it into their paper. He explained how
one could extend the ASM weak order to the setting of arbitrary Coxeter groups, provided one
could prove Theorem 1.1. The author found a proof, which he kept as a note on his computer.
In 2023, an undergraduate at MIT asked to do research with the author, who suggested trying to
prove Theorem 1.6 in type A using the combinatorics of alternating sign matrices and monotone
triangles. It turns out this was the wrong approach; the author later realized how to give a type-
uniform proof using a subtle inductive argument that passes back and forth between the weak order
and the Bruhat order. By that time, the student had pivoted to a different project, so the author
added a sketch of the proof of Theorem 1.6 to his earlier notes.
   In May of 2026, the author uploaded the LATEX file of his notes to ChatGPT 5.4 Pro and asked
it to fill in the gaps. Not only did it add in the details perfectly, but it also caught numerous
typos. It rewrote the notes in a matter of minutes. At this point, the author asked ChatGPT to
suggest other directions to explore related to the weak order on MacNeille completions. ChatGPT
suggested proving the conjecture of Hamaker and Reiner regarding the poset topology of open
intervals in the ASM weak order. The author asked ChatGPT to prove this conjecture. Instead, it
returned the counterexample shown in Figure 1.
   At this point, the author opened a new conversation with ChatGPT and uploaded his newly
polished notes and the article of Escobar, Klein, and Weigandt [EKW]. He asked, “Could some
of the ideas from the paper of Escobar, Klein, and Weigandt generalize to other Coxeter groups
using my notion of weak order on Mac(W )? Could we define analogues of ASM varieties in other
types?” ChatGPT responded by suggesting definitions of ASM varieties for other Weyl groups
using unions of opposite Schubert varieties in the flag variety G/B. The author then asked, “Can
you find a counterexample to Conjecture 3.21 in the EKW paper?” After thinking for around 50
minutes, ChatGPT responded by saying it had not found a counterexample and that it verified the
conjecture for all n ≤ 7. The author asked, “In that case, can you prove Conjecture 3.21?” After
thinking for around 19 minutes, ChatGPT responded with the main ingredients of the proof. The
proof of Theorem 1.3 presented in Section 4 is essentially the one that ChatGPT found, although
the author massaged the writing style and added several details. In the end, this proof is not
terribly intricate, and several of the steps are somewhat routine. Probably the most significant
advance is Lemma 3.1.
   After the first version of this paper appeared, Vic Reiner sent the author an earlier draft of
[HR20] containing the MacNeille complex construction and asked when the resulting Boolean cell
complex is simplicial. The author discussed this question with ChatGPT. Its initial attempts at a
proof incorrectly treated ∇(X) as the set of common upper bounds of X, rather than the order filter
generated by X; the author pointed out this error. The corrected discussion led to the maximal-
parabolic identity in Lemma 6.1, which proves simpliciality. Once this identity was in place, the
shelling argument from [HR20, Section 4] carried over essentially verbatim, yielding Theorem 1.7.
                  WEAK ORDER ON THE MACNEILLE COMPLETION OF BRUHAT ORDER                                     15


                                           Acknowledgments
   The author thanks Zach Hamaker and Vic Reiner for suggesting the Coxeter-theoretic definition
of weak order on Mac(W ), and he thanks Vic Reiner for bringing the MacNeille complex construc-
tion to his attention. He thanks Katherine Tung for pointing him to Jahn’s thesis. He thanks an
anonymous referee for helpful comments. He also thanks OpenAI for providing unlimited access to
ChatGPT 5.4 Pro.

                                                References
[AFHKKL] I. Axelrod-Freed, H. Hao, M. Kendall, P. Klein, and Y. Luo. Some algebraic properties of ASM varieties.
         Glasg. Math. J., 68 (2026), 440–459.
[BB05]   A. Björner and F. Brenti. Combinatorics of Coxeter groups, vol. 231 of Graduate Texts in Mathematics.
         Springer, 2005.
[BC17]   N. Bergeron and C. Ceballos. A Hopf algebra of subword complexes. Adv. Math., 305 (2017), 1163–1201.
[CG19]   A. Claesson and B.Á. Guðmundsson. Enumerating permutations sortable by k passes through a pop-
         stack. Adv. Appl. Math., 108 (2019), 79–96.
[CGP23]  A. Claesson, B. Á. Guðmundsson, and J. Pantone. Counting pop-stacked permutations in polynomial
         time. Exp. Math., 32 (2023), 97–104.
[Def22A] C. Defant. Meeting covered elements in ν-Tamari lattices. Adv. Appl. Math., 134 (2022).
[Def22B] C. Defant. Pop-stack-sorting for Coxeter groups. Comb. Theory, 2 (2022).
[EG21]   M. Elder and Y. K. Goh. k-pop stack sortable permutations and 2-avoidance. Electron. J. Combin., 28
         (2021).
[EKW]    L. Escobar, P. Klein, and A. Weigandt. Algebra and geometry of ASM weak order. arXiv:2502.19266.
[EM18]   L. Escobar and K. Mészáros. Subword complexes via triangulations of root polytopes. Algebr. Comb., 1
         (2018), 395–414.
[Ful92]  W. Fulton. Flags, Schubert polynomials, degeneracy loci, and determinantal formulas. Duke Math. J.,
         65 (1992), 381–420.
[HR20]   Z. Hamaker and V. Reiner. Weak order and descents for monotone triangles. European J. Combin., 86
         (2020).
[Jah22]  D. Jahn. Combinatorics of subword complexes for finite type Coxeter systems. Ph.D. thesis, Ruhr-
         Universität Bochum, 2022.
[KM04]   A. Knutson and E. Miller. Subword complexes in Coxeter groups. Adv. Math., 184 (2004), 161–176.
[KM05]   A. Knutson and E. Miller. Gröbner geometry of Schubert polynomials. Ann. of Math., 161 (2005),
         1245–1318.
[PS15]   V. Pilaud and C. Stump. Brick polytopes of spherical subword complexes and generalized associahedra.
         Adv. Math., 276 (2015), 1–61.
[STW25]  C. Stump, H. Thomas, and N. Williams. Cataland: why the Fuß? Mem. Amer. Math. Soc., 305 (2025).
[Ste05]  J. R. Stembridge. Tight quotients and double quotients in the Bruhat order. Electron. J. Combin., 11
         (2004/06), no. 2, Research Paper 14.
[Wei17]  A. Weigandt. Prism tableaux for alternating sign matrix varieties. arXiv:1708.07236.
