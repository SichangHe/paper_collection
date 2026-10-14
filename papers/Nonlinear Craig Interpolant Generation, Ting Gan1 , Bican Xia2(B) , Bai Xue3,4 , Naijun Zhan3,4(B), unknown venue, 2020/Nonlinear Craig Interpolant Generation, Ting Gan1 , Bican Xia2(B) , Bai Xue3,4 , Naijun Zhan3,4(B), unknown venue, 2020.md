        Nonlinear Craig Interpolant Generation

       Ting Gan1 , Bican Xia2(B) , Bai Xue3,4 , Naijun Zhan3,4(B) ,
                            and Liyun Dai5
           1
             School of Computer Science, Wuhan University, Wuhan, China
                                ganting@whu.edu.cn
    2
       LMAM, School of Mathematical Sciences, Peking University, Beijing, China
                                xbc@math.pku.edu.cn
       3
         State Key Laboratory of Computer Science, Institute of Software, CAS,
                                    Beijing, China
                              {xuebai,znj}@ios.ac.cn
             4
               University of Chinese Academy of Sciences, Beijing, China
     5
        RISE, School of Computer and Information Science, Southwest University,
                                  Chongqing, China
                                dailiyun@swu.edu.cn



       Abstract. Craig interpolant generation for non-linear theory and
       its combination with other theories are still in infancy, although
       interpolation-based techniques have become popular in the veriﬁcation
       of programs and hybrid systems where non-linear expressions are very
       common. In this paper, we ﬁrst prove that a polynomial interpolant of
       the form h(x) > 0 exists for two mutually contradictory polynomial for-
       mulas φ(x, y) and ψ(x, z), with the form f1 ≥ 0 ∧ · · · ∧ fn ≥ 0, where
       fi are polynomials in x, y or x, z, and the quadratic module generated
       by fi is Archimedean. Then, we show that synthesizing such interpolant
       can be reduced to solving a semi-deﬁnite programming problem (SDP).
       In addition, we propose a veriﬁcation approach to assure the validity
       of the synthesized interpolant and consequently avoid the unsoundness
       caused by numerical error in SDP solving. Besides, we discuss how to
       generalize our approach to general semi-algebraic formulas. Finally, as
       an application, we demonstrate how to apply our approach to invariant
       generation in program veriﬁcation.


       Keywords: Craig interpolant · Archimedean condition · Semi-deﬁnite
       programming · Program veriﬁcation · Sum of squares


1    Introduction
Interpolation-based techniques have become popular in recent years because of
their inherently modular and local reasoning, which can scale up existing formal
veriﬁcation techniques like theorem proving, model-checking, abstract interpre-
tation, and so on, while the scalability is the bottleneck of these techniques. The
study of interpolation was pioneered by Krajíc̆ek [20] and Pudlák [30] in con-
nection with theorem proving, by McMillan in connection with model-checking
c The Author(s) 2020
S. K. Lahiri and C. Wang (Eds.): CAV 2020, LNCS 12224, pp. 415–438, 2020.
https://doi.org/10.1007/978-3-030-53288-8_20
416     T. Gan et al.

[25], by Graf and Saı̈di [14], Henzinger et al. [16] and McMillan [26] in con-
nection with abstraction like CEGAR, by Wang et al. [17] in connection with
machine-learning based program veriﬁcation.
    Craig interpolant generation plays a central role in interpolation-based tech-
niques, and therefore has drawn increasing attention. In the literature, there
are various eﬃcient algorithms proposed for automatically synthesizing inter-
polants for decidable fragments of ﬁrst-order logic, linear arithmetic, array logic,
equality logic with uninterpreted functions (EUF), etc., and their combinations,
and their use in veriﬁcation, e.g., [6,16,18,19,26,27,33,33,37] and the references
therein. Additionally, how to compare the strength of diﬀerent interpolants is
investigated in [9]. However, interpolant generation for non-linear theory and its
combination with the aforementioned theories is still in infancy, although non-
linear polynomials inequalities are quite common in safety-critical software and
embedded systems [38,39].
    In [7], Dai et al. had a ﬁrst try and gave an algorithm for generating
interpolants for conjunctions of mutually contradictory nonlinear polynomial
inequalities based on the existence of a witness guaranteed by Stengle’s Posi-
tivstellensatz [36], which is computable using semi-deﬁnite programming (SDP).
Their algorithm is incomplete in general but if all variables are bounded (called
Archimedean condition), then it becomes complete. A major limitation of their
work is that two mutually contradictory formulas φ and ψ must have the same
set of variables. In [10], Gan et al. proposed an algorithm to generate inter-
polants for quadratic polynomial inequalities. The basic idea is based on the
insight that for analyzing the solution space of concave quadratic polynomial
inequalities, it suﬃces to linearize them by proving a generalization of Motzkin’s
transposition theorem for concave quadratic polynomial inequalities. Moreover,
they also discussed how to generate interpolants for the combination of the
theory of quadratic concave polynomial inequalities and EUF based on the hier-
archical calculus proposed in [34] and used in [33]. Obviously, quadratic con-
cave polynomial inequalities is a very restrictive class of polynomial formulas,
although most of existing abstract domains fall within it as argued in [10]. Mean-
while, in [13], Gao and Zuﬀerey presented an approach to extract interpolants for
non-linear formulas possibly containing transcendental functions and diﬀerential
equations from proofs of unsatisﬁability generated by δ-decision procedure [12]
based on interval constraint propagation (ICP) [1] by transforming proof traces
from δ-complete decision procedures into interpolants that consist of Boolean
combinations of linear constraints. Thus, their approach can only ﬁnd the inter-
polants between two formulas whenever their conjunction is not δ-satisﬁable.
Similar idea was also reported in [21]. In [5], Chen et al. proposed an app-
roach for synthesizing non-linear interpolants based on counterexample-guided
and machine-learning, but it relies on quantiﬁer elimination in order to guar-
antee the completeness and convergence, which gives rise to the low eﬃciency
of their approach theoretically. In [35], Srikanth et al. presented an approach
called CAMPY to exploit non-linear interpolant generation, which is achieved
by abstracting non-linear formulas (possibly with non-polynomial expressions)
                                         Nonlinear Craig Interpolant Generation   417

to the theory of linear arithmetic with uninterpreted functions, i.e., EUFLIA,
to prove and/or disprove if a given program satisﬁes a given property, that may
contain nonlinear expressions.
Example 1. In order to compare the approach proposed in this paper and the
ones aforementioned, consider
φ = −2xy 2 + x2 − 3xz − y 2 − yz + z 2 − 1 ≥ 0 ∧ 100 − x2 − y 2 ≥ 0 ∧
                                 1                         1
    x2 z 2 + y 2 z 2 − x2 − y 2 + (x4 + 2x2 y 2 + y 4 ) −     (x6 + y 6 ) − 4 ≤ 0;
                                 6                        120
ψ = 4(x − y)4 + (x + y)2 + w2 − 133.097 ≤ 0 ∧ 100(x + y)2 − w2 (x − y)4 − 3000 ≥ 0.

 It can be checked that φ ∧ ψ |= ⊥.
    Obviously, synthesizing interpolants for φ and ψ in this example is beyond
the ability of the above approaches reported in [7,10]. Using the method in [13]
implemented in dReal3 it would return “SAT” with δ = 0.001, i.e., φ ∧ ψ is δ-
satisﬁable, and hence it cannot synthesize any interpolant using [12]’s approach
with any precision greater than 0.0011 . While, using our method, an interpolant
h > 0 with degree 10 can be found as shown in Fig. 12 . Additionally, using
the symbolic procedure REDUCE, it can be proved that h > 0 is indeed an
interpolant of φ and ψ.
    In this paper, we investigate this
issue and consider how to synthesize an
interpolant for two polynomial formu-
las φ(x, y) and ψ(x, z) with φ(x, y) ∧
ψ(x, z) |= ⊥, where
φ(x, y) : f1 (x, y) ≥ 0∧· · ·∧fm (x, y) ≥ 0,
ψ(x, z) : g1 (x, z) ≥ 0 ∧ · · · ∧ gn (x, z) ≥ 0,
x ∈ Rr , y ∈ Rs , z ∈ Rt are
variable vectors, r, s, t ∈ N, and
f1 , . . . , fm , g1 , . . . , gn are polynomials. In
addition, Mx,y {f1 (x, y), . . . , fm (x, y)}
and Mx,z {g1 (x, z), . . ., gn (x, z)} are two
Archimedean quadratic modules. Here
we allow uncommon variables, that are Fig. 1. Example 1. (Green region: the
not allowed in [7], and drop the con- projection of φ(x, y, z) onto x and y;
straint that polynomials must be concave red region: the projection of ψ(x, y, w)
and quadratic, which is assumed in [10]. onto x and y; gray region plus the
The Archimedean condition amounts to green region: the synthesized inter-
that all the variables are bounded, which polant {(x, y) | h(x, y) > 0}.) (Color
is reasonable in program veriﬁcation, as ﬁgure online)
only bounded numbers can be repre-
sented in computer in practice. We ﬁrst prove that there exists a polynomial
1
  Alternatively, if we try the formula with the latest version of dReal4, it does not
  produce any output after 20 h.
2
  The mathematical representation of h is given in the full version [11].
418     T. Gan et al.

h(x) such that h(x) = 0 separates the state space of x deﬁned by φ(x, y) from
the one deﬁned by ψ(x, z) theoretically, and then propose an algorithm to com-
pute such h(x) based on SDP. Furthermore, we propose a veriﬁcation approach
to assure the validity of the synthesized interpolant and consequently avoid the
unsoundness caused by numerical error in SDP solving. Finally, we also discuss
how to extend our results to general semi-algebraic constraints.
    Another contribution of this paper is that as an application, we illustrate
how to apply our approach to invariant generation in program veriﬁcation by
revising Lin et al.’s framework proposed in [22] for invariant generation based
on weakest precondition, strongest postcondition and interpolation by allowing
to generate nonlinear invariants.
    The paper is organized as follows. Some preliminaries and the problem of
interest are introduced in Sect. 2. Section 3 shows the existence of an interpolant
for two mutually contradictory polynomial formulas only containing conjunction,
and Sect. 4 presents SDP-based methods to compute it. In Sect. 5, we discuss how
to avoid unsoundness caused by numerical error in SDP. Section 6 extends our
approach to general polynomial formulas. Section 7 demonstrates how to apply
our approach to invariant generation in program veriﬁcation. We conclude this
paper in Sect. 8.


2     Preliminaries
In this section, we ﬁrst give a brief introduction on some notions used throughout
this paper and then describe the problem of interest.

2.1   Quadratic Module
N, Q and R are the sets of integers, rational numbers and real numbers, respec-
tively. Q[x] and R[x] denotes the polynomial ring over rational numbers and
real numbers in r ≥ 1 indeterminatesx : (x1 , . . . , xr ). We use R[x]2 := {p2 |
p ∈ R[x]} for the set of squares and      R[x]2 for the set of sums of squares of
polynomials in x. Vectors are denoted by boldface letters. ⊥ and  stand for
false and true, respectively.

Definition 1 (Quadratic Module [24]). A subset M of R[x] is called a
quadratic module if it contains 1 and is closed under addition and multiplication
with squares, i.e., 1 ∈ M, M + M ⊆ M, and p2 M ⊆ M for all p ∈ R[x].
     Let p := {p1 , . . . , ps } be a ﬁnite subset of R[x], the quadratic module Mx (p)
or simply M(p) generated
                       s          by p (i.e.the smallest quadratic module containing all
pi s) is Mx (p) = { i=0 δi pi | δi ∈ R[x]2 }, where p0 = 1.

    Archimedean condition plays a key role in the study of polynomial optimiza-
tion.

Definition 2 (Archimedean). Let M be a quadratic module       of R[x]. M is
                                                                 r
said to be Archimedean if there exists some a > 0 such that a − i=1 x2i ∈ M.
                                         Nonlinear Craig Interpolant Generation          419

2.2     Problem Description
Craig showed that given two formulas φ and ψ in a ﬁrst-order theory T , if
φ |= ψ, then there always exists an interpolant I over the common symbols of φ
and ψ s.t. φ |= I and I |= ψ. In the veriﬁcation literature, this terminology has
been abused following [26], where a reverse interpolant (coined by Kovács and
Voronkov in [19]) I over the common symbols of φ and ψ is deﬁned by
Definition 3 (Interpolant). Given two formulas φ and ψ in a theory T s.t.
φ ∧ ψ |=T ⊥, a formula I is an interpolant of φ and ψ if (i) φ |=T I; (ii)
I ∧ ψ |= ⊥; and (iii) I only contains common symbols and free variables shared
by φ and ψ.
                                                          s
Definition 4. A basic semi-algebraic set {x ∈ Rn | i=1 pi (x) ≥ 0} is called
a set of the Archimedean form if Mx {p1 (x), . . . , ps (x)} is Archimedean, where
pi (x) ∈ R[x], i = 1, . . . , s.
      The interpolant synthesis problem of interest in this paper is given in Problem 1.
Problem 1. Let φ(x, y) and ψ(x, z) be two polynomial formulas of the form
                      φ(x, y) : f1 (x, y) ≥ 0 ∧ · · · ∧ fm (x, y) ≥ 0,
                       ψ(x, z) : g1 (x, z) ≥ 0 ∧ · · · ∧ gn (x, z) ≥ 0,
where, x ∈ Rr , y ∈ Rs , z ∈ Rt are variable vectors, r, s, t ∈ N, and f1 , . . . , fm , g1 ,
. . . , gn are polynomials in the corresponding variables. Suppose φ ∧ ψ |= ⊥,
and {(x, y) | φ(x, y)} and {(x, z) | ψ(x, z)} are semi-algebraic sets of the
Archimedean form. Find a polynomial h(x) such that h(x) > 0 is an interpolant
for φ and ψ.

3      Existence of Interpolants
The basic idea and steps of proving the existence of interpolants are as follows:
Because an interpolant of φ and ψ contains only the common symbols in φ and
ψ, it is natural to consider the projections of the sets deﬁned by φ and ψ on x,
i.e. Px (φ(x, y))={x
                 ˆ    | ∃y. φ(x, y)} and Px (ψ(x, z))={x
                                                     ˆ    | ∃z. ψ(x, z)}, which are
obviously disjoint. We therefore prove that, if h(x) = 0 separates Px (φ(x, y))
and Px (ψ(x, z)), then h(x) solves Problem 1 (see Proposition 1). Thus, we only
need to prove the existence of such h(x) through the following steps: First, we
prove that Px (φ(x, y)) and Px (ψ(x, z)) are compact semi-algebraic sets which are
unions of ﬁnitely many basic closed semi-algebraic sets (see Lemma 1). Second,
using Putinar’s Positivstellensatz, we prove that, for two disjoint basic closed
semi-algebraic sets S1 and S2 of the Archimedean form, there exists a polynomial
h1 (x) such that h1 (x) = 0 separates S1 and S2 (see Lemma 2). This result is then
extended to the case that S2 is a ﬁnite union of basic closed semi-algebraic sets
(see Lemma 3). Finally, by generalizing Lemma 3 to the case that two compact
semi-algebraic sets both are unions of ﬁnitely many basic closed semi-algebraic
sets and together with Proposition 1, we prove the existence of interpolant in
Theorem 2 and Corollary 1.
420     T. Gan et al.

Proposition 1. If h(x) ∈ R[x] satisﬁes the following constraints

          ∀x ∈ Px (φ(x, y)).h(x) > 0        and    ∀x ∈ Px (ψ(x, z)).h(x) < 0,            (1)

then h(x) > 0 is an interpolant for φ(x, y) and ψ(x, z), where φ(x, y) and ψ(x, z)
are deﬁned as in Problem 1.
Proof. According to Deﬁnition 3, it is enough to prove that φ(x, y) |= h(x) > 0
and ψ(x, z) |= h(x) ≤ 0.
   Since any (x0 , y0 ) satisfying φ(x, y) must imply x0 ∈ Px (φ(x, y)), it follows
that h(x0 ) > 0 from (1) and φ(x, y) |= h(x) > 0. Similarly, we can prove
ψ(x, z) |= h(x) < 0, implying that ψ(x, z) |= h(x) ≤ 0. Therefore, h(x) > 0 is
an interpolant for φ(x, y) and ψ(x, z).
    In order to synthesize such h(x) in Proposition 1, we ﬁrst dig deeper into
the two sets Px (φ(x, y)) and Px (ψ(x, z)). As shown later, i.e. in Lemma 1, we
will ﬁnd that these two sets are compact semi-algebraic sets of the form {x |
c Ji
  i=1   j=1 αi,j (x) ≥ 0}. Before this lemma, we introduce Finiteness theorem
pertinent to a basic closed semi-algebraic subset of Rn , which will be used in the
proof of Lemma 1, where a basic closed semi-algebraic subset of Rn is a set of
the form {x ∈ Rn | α1 (x) ≥ 0, . . . , αk (x) ≥ 0} with α1 , . . . , αk ∈ R[x].
Theorem 1 (Finiteness Theorem, Theorem 2.7.2 in [3]). Let A ⊂ Rn be a
closed semi-algebraic set. Then A is a ﬁnite union of basic closed semi-algebraic
sets.
Lemma 1. The set Px (φ(x, y)) is compact semi-algebraic set of the following
form

                                               
                                               c 
                                                 Ji
                        Px (φ(x, y)) := {x |             αi,j (x) ≥ 0},
                                               i=1 j=1

where αi,j (x) ∈ R[x], i = 1, . . . , c, j = 1, . . . , Ji . The same claim applies to the
set Px (ψ(x, z)) as well.
Proof. For the sake of simplicity, we denote {(x, y) | φ(x, y)} and Px (φ(x, y))
by S and π(S), respectively.
     Because S is a compact set and π is a continuous map that maps compact
set to compact set, π(S), which is the image of a compact set under a continuous
map, is compact. Moreover, as S is a semi-algebraic set and the projection of
a semi-algebraic set is also a semi-algebraic set by Tarski-Seidenberg theorem
[2], this implies that π(S) is a semi-algebraic set. Thus, π(S) is a compact semi-
algebraic set.
     Since π(S) is a compact semi-algebraic set, and also a closed semi-
algebraic set, we have that π(S) is a ﬁnite union of basic closed semi-
algebraic sets from Theorem 1. Hence, there exist a series of polynomi-              c
als α1,1 (x), . . . , α1,J1 (x), . . . , αc,1 (x), . . . , αc,Jc (x) such that π(S) = i=1 {x |
Ji                              c Ji
  j=1 αi,j (x) ≥ 0} = {x |           i=1 j=1 αi,j (x) ≥ 0}. This concludes this lemma.
                                          Nonlinear Craig Interpolant Generation      421

    After knowing the structure of Px (φ(x, y)) and Px (ψ(x, z)) being a union
of some basic semialgebraic sets as illustrated in Lemma 1, we next prove the
existence of h(x) ∈ R[x] satisfying (1), as formally stated in Theorem 2.
Theorem 2. Suppose that φ(x, y) and ψ(x, z) are deﬁned as in Problem 1, then
there exists a polynomial h(x) satisfying (1).
    As pointed out by an anonymous reviewer that Theorem 2 can be obtained by
some properties of the ring of Nash functions proved in [29]. In what follows, we
give a simpler and more intuitive proof. To the end, it requires some preliminaries
ﬁrst. The main tool in our proof is Putinar’s Positivstellensatz, as formulated in
Theorem 3.

Theorem 3 (Putinar’s Positivstellensatz [31]). Let p1 , . . . , pk ∈ R[x] and
S1 = {x | p1 (x) ≥ 0, . . . , pk (x) ≥ 0}. Assume that the quadratic mod-
ule M(p1 , . . . , pk ) is Archimedean. For q ∈ R[x], if q > 0 on S1 then q ∈
M(p1 , . . . , pk ).

    With Putinar’s Positivstellensatz we can draw a conclusion that there exists
a polynomial such that its zero level set3 separates two compact semi-algebraic
sets of the Archimedean form, as claimed in Lemmas 2 and 3.

Lemma 2. Let S1 = {x | p1 (x) ≥ 0, . . . , pJ (x) ≥ 0}, S2 = {x | q1 (x) ≥
0, . . . , qK (x) ≥ 0} be semi-algebraic sets of the Archimedean form and S1 ∩ S2 =
∅, then there exists a polynomial h1 (x) such that

                      ∀x ∈ S1 . h1 (x) > 0,       ∀x ∈ S2 . h1 (x) < 0.               (2)

Proof. Since S1 ∩ S2 = ∅, it follows

              p2 ≥ 0 ∧ · · · ∧ pJ ≥ 0 ∧ q1 ≥ 0 ∧ · · · ∧ qK ≥ 0 |= −p1 > 0.

Let S3 = {x | p2 ≥ 0 ∧ · · · ∧ pJ ≥ 0 ∧ q1 ≥ 0 ∧ · · · ∧ qK ≥ 0}, then −p1 > 0
on S3 . Since S1 and S2 are semi-algebraic sets of the Archimedean form, it
follows Mx (p2 (x), . . . , pJ (x), q1 (x), . . . , qK (x)) is also Archimedean. Hence, S3
is
compact.    From −p1 > 0 on S3 , we further have that there exists some u1 ∈
    R[x]2 such that −u1 p1 − 1 > 0 on S3 . Using Theorem 3, we have that

                −u1 p1 − 1 ∈ Mx (p2 (x), . . . , pJ (x), q1 (x), . . . , qK (x)),

implying that there exists a set of sums of squares polynomials u2 , . . . , uJ and
v0 ,v1 , . . . , vK ∈ R[x], such that

             −u1 p1 − 1 ≡ u2 p2 + · · · + uJ pJ + v0 + v1 q1 + · · · + vK qK .

Let h1 = 12 + u1 p1 + · · · + uJ pJ , i.e., −h1 = 12 + v0 + v1 q1 + · · · + vK qK . It is
easy to check that (2) holds.
3
    The zero level set of an n-variate polynomial h(x) is deﬁned as {x ∈ Rn | h(x) = 0}.
422       T. Gan et al.

Lemma 3 generalizes the result of Lemma 2 to more general compact semi-
algebraic sets of the Archimedean form, which is the union of multiple basic
semi-algebraic sets.
Lemma 3. Assume S0 = {x | p1 (x) ≥ 0, . . . , pJ (x) ≥ 0} and Si = {x |
qi,1 (x) ≥ 0, . . . , qi,Ki (x) ≥ 0}, i = 1, . . . , b, are semi-algebraic sets of the
                                    b
Archimedean form, and S0 ∩ i=1 Si = ∅, then there exists a polynomial h0 (x)
such that
                                                    b
                      ∀x ∈ S0 . h0 (x) > 0, ∀x ∈        Si . h0 (x) < 0.           (3)
                                                           i=1

      In order to prove this lemma, we prove the following lemma ﬁrst.
Lemma 4. Let c, d ∈ R with 0 < c < d and U0 = [c, d]r . There exists a polyno-
mial ĥ(x) such that
                                                            
                                                            r
                                x ∈ U0 |= ĥ(x) > 0 |=            xi > 0,             (4)
                                                            i=1

where x = (x1 , . . . , xr ).

Proof. We show that there exists k ∈ N such that ĥ(x) = ( d2 )2k − (x1 − c+d      2 ) −
                                                                                      2k
                                                                        r
· · · − (xr − c+d2 )
                    2k
                       satisﬁes (4). It is evident that ĥ(x) > 0 |= i=1 xi > 0 holds.
                                                   r
In the following we just need to verify that i=1 c ≤ xi ≤ d |= ĥ(x)          > 0 holds.
                                                                                 r
Since c ≤ xi ≤ d, we have (xi − c+d         2 )2k
                                                  ≤  ( d−c 2k
                                                        2  )  and   ( d 2k
                                                                      2 )   −    i=1 (xi −
c+d 2k
   2 )    ≥ ( 2 ) − r( 2 ) . Obviously, if an integer k satisﬁes ( d−c ) > r, then
              d 2k      d−c 2k                                             d 2k
          r
( d2 )2k − i=1 (xi − c+d 2 )
                            2k
                               > 0. The existence of such k satisfying ( d−c d 2k
                                                                                ) > r is
                 d
assured by d−c > 1.
      Now we give a proof for Lemma 3 as follows.
Proof (of Lemma 3). For any i with 1 ≤ i ≤ b, according to Lemma 2, there exists
a polynomial hi ∈ R[x], satisfying ∀x ∈ S0 . hi (x) > 0 and ∀x ∈ Si . hi (x) < 0.
    Next, we construct h0 (x) ∈ R[x] from h1 (x), . . . , hb (x). Since S0 is a semi-
algebraic set of the Archimedean form, S0 is compact and thus hi (x) has min-
imum value and maximum value on S0 , denoted by ci and di respectively. Let
c = min(c1 , . . . , cb ) and d = max(d1 , . . . , db ). Clearly, 0 < c < d.
   From Lemma 4 there must exist a polynomial ĥ(w1 , . . . , wb ) such that

                           
                           b
                                 c ≤ wi ≤ d |= ĥ(w1 , . . . , wb ) > 0,              (5)
                           i=1
                                                                
                                                                b
                                  ĥ(w1 , . . . , wb ) > 0 |=         wi > 0.         (6)
                                                                i=1

Let h0 (x) = ĥ(h1 (x), . . . , hb (x)). Obviously, h0 (x) ∈ R[x]. We next prove that
h0 (x) satisﬁes (3) in Lemma 3.
                                           Nonlinear Craig Interpolant Generation           423

    For all x0 ∈ S0 , c ≤ hi (x0 ) ≤ d, i = 1, . . . , b, h0 (x0 ) =
ĥ(h1 (x0 ), . . . , hb (x0 )) > 0 by (5). Therefore, the ﬁrst constraint in (3), i.e.
∀x0 ∈ S0 .h0 (x0 ) > 0, holds.
                         b
    For any x0 ∈ i=1 Si , there must exist some i such that x0 ∈ Si , implying
that hi (x0 ) < 0. By (6) we have h0 (x0 ) = ĥ(h1 (x0 ), . . . , hb (x0 )) ≤ 0.
    Thus, we obtain the conclusion that there exists a polynomial h0 (x) such
                                             b
that ∀x ∈ S0 . h0 (x) > 0, and ∀x ∈ i=1 Si . h0 (x) ≤ 0. Also, since S0 is a
compact set, and h0 (x) > 0 on S0 , there must exist some positive number  > 0
                                                                        b
such that h0 (x) −  > 0 over S0 . Then h0 (x) −  < 0 on i=1 Si . Therefore,
setting h0 (x) := h0 (x) − , Lemma 3 is proved.
    In Lemma 3 we proved that there exists a polynomial h(x) ∈ R[x] such that
its zero level set is a barrier between two semi-algebraic sets of the Archimedean
form, of which one set is a union of ﬁnitely many basic semi-algebraic sets. In
the following we will give a formal proof of Theorem 2, which is a generalization
of Lemma 3.
Proof (of Theorem 2). According to Lemma 1 we have that Px (φ(x, y)) and
Px (ψ(x, z)) are compact sets, and there respectively exists a set of polynomials
pi,j (x) ∈ R[x], i = 1, . . . , a, j = 1, . . . , Ji , and ql,k (x) ∈ R[x], l = 1, . . . , b,
k = 1, . . . , Ki , such that
                       
                       a 
                         Ji                                             
                                                                        b 
                                                                          Kl
Px (φ(x, y)) = {x |              pi,j (x) ≥ 0},   Px (ψ(x, z)) = {x |             ql,k (x) ≥ 0}.
                       i=1 j=1                                          l=1 k=1

Since Px (φ(x, y)) and Px (ψ(x,z))   are compact sets, there exists a positive
                                  r
N ∈ R such that f = N − i=1 x2i ≥ 0 over Px (φ(x, y)) and Px (ψ(x, z)).
For each i = 1, . . . , a and each l = 1, . . . , b, set pi,0 = ql,0 = f . Denote
        a  Ji                       a           Ji
{x |     i=1 j=0 pi,j (x) ≥ 0} =        i=1 {x |         pi,j (x) ≥ 0} by P1 and
      b Kl                      b          Kl j=0
{x | l=1 k=0 ql,k (x) ≥ 0} = l=1 {x | k=0 ql,k (x) ≥ 0} by P2 . It is easy
to see that P1 = Px (φ(x, y), P2 = Px (ψ(x, z)).
    Since φ ∧ ψ |= ⊥, there does not exist (x, y, z) ∈ Rr+s+t that satisﬁes φ ∧ ψ,
implying that Px (φ(x, y)) ∩ Px (ψ(x, z)) = ∅ and thus P1 ∩ P2 = ∅. Also, since
      Ji1                                                         Ji1
{x | j=0    pi1 ,j (x) ≥ 0} ⊆ P1 , for each i1 = 1, . . . , a, {x | j=0 pi1 ,j (x) ≥
0} ∩ P2 = ∅ holds. By Lemma 3 there exists hi1 (x) ∈ R[x] such that
                       Ji1
                       
           ∀x ∈ {x |         pi1 ,j (x) ≥ 0}.hi1 (x) > 0,   ∀x ∈ P2 .hi1 (x) < 0.
                       j=0
                                                    r
Let S  = {x | −h1 (x) ≥ 0, . . . , −ha (x) ≥ 0, N − i=1 x2i ≥ 0}. Obviously,
S  is a semialgebraic set of the Archimedean form, P2 ⊂ S  and P1 ∩ S  = ∅.
Therefore, according to Lemma 2, there exists a polynomial h(x) ∈ R[x] such
that ∀x ∈ S  . h(x) > 0 and ∀x ∈ P1 . h(x) < 0. Let h(x) = −h(x), then
we have ∀x ∈ P1 . h(x) > 0 and ∀x ∈ P2 . h(x) < 0, implying that ∀x ∈
Px (φ(x, y)).h(x) > 0 and ∀x ∈ Px (ψ(x, z)).h(x) < 0. Thus, this completes the
proof of Theorem 2.
424       T. Gan et al.

      Consequently, we immediately have the following conclusion.
Corollary 1. Let φ(x, y) and ψ(x, z) be deﬁned as in Problem 1. There must
exist a polynomial h(x) ∈ R[x] such that h(x) > 0 is an interpolant for φ and ψ.
    Actually, since Px (φ(x, y)) and Px (ψ(x, z)) both are compact set by Lemma
1, and h(x) > 0 on Px (φ(x, y)) and h(x) < 0 on Px (ψ(x, z)), we can obtain h (x)
by giving a small perturbation to the coeﬃcients of h(x) such that h (x) has the
property of h(x). Hence, there should exist a h(x) ∈ Q[x] such that h(x) > 0 is
an interpolant for φ and ψ, intuitively.
Theorem 4. Let φ(x, y) and ψ(x, z) be deﬁned as in Problem 1. There must
exist a polynomial h(x) ∈ Q[x] such that h(x) > 0 is an interpolant for φ and
ψ.
Proof. We just need to prove there exists a polynomial h(x) ∈ Q[x] satisfying
(1).
    By Theorem 2, there exists a polynomial h (x) ∈ R[x] satisfying (1). Since
Px (φ(x, y)) and Px (ψ(x, z)) are compact sets, h (x) > 0 on Px (φ(x, y)) and
h (x) < 0 on Px (ψ(x, z)), there exist η1 > 0 and η2 > 0 such that

        ∀x ∈ Px (φ(x, y)).h (x) − η1 ≥ 0, ∀x ∈ Px (ψ(x, z)).h (x) + η2 ≤ 0.
                                                                         
Let η = min( η21 , η22 ). Suppose h (x) ∈ R[x] has the form h (x) = α∈Ω cα xα ,
where α ∈ N , Ω ⊂ N is a ﬁnite set of indices, r is the dimension of x, xα is
              r            r

the monomial xα  1 · · · xr , and 0 = cα ∈ R is the coeﬃcient of monomial x . Let
                  1         αr                                                  α

N = |Ω| be the cardinality of Ω. Since Px (φ(x, y)) and Px (ψ(x, z)) are compact
sets, for any α ∈ Ω, there exists Mα > 0 such that Mα = max{|xα | | x ∈
                                                                         
Px (φ(x, y)) ∪ Px (ψ(x, z))}. Then for any ﬁxed polynomial ĥ(x) = α∈Ω dα xα ,
with dα ∈ [cα − N M   η
                         α
                                    η
                           , cα + N M α
                                        ], and any x ∈ Px (φ(x, y)) ∪ Px (ψ(x, z)), we
have
                                                                                    η
  |ĥ(x) − h (x)| = |         (dα − cα )xα | ≤         |(dα − cα )| · |xα | ≤             · Mα = η.
                         α∈Ω                      α∈Ω                            α∈Ω
                                                                                     N M α



Since η = min( η21 , η22 ), hence
                                      η1                                                η2
      ∀x ∈ Px (φ(x, y)).ĥ(x) ≥          > 0,      ∀x ∈ Px (ψ(x, z)).ĥ(x) ≤ −             < 0.    (7)
                                      2                                                 2
Since for any dα ∈ [cα − N M η
                               α
                                          η
                                 , cα + N M α
                                              ] (7) holds, there must exist some
rational number rα ∈ Q in [cα − N Mα , cα + N M
                                     η           η
                                                   
                                                   α
                                                     ] satisfying (7) because of the
density of rational numbers. Thus, let h(x) = α∈Ω rα xα . Clearly, it follows
that h(x) ∈ Q[x] and (1) holds.
    So, the existence of h(x) ∈ Q[x] is guaranteed. Moreover, from the proof of
Theorem 4, we know that a small perturbation of h(x) is permitted, which is a
good property for computing h(x) in a numeric way. In the subsequent subsec-
tion, we recast the problem of ﬁnding such h(x) as a semi-deﬁnite programming
problem.
                                         Nonlinear Craig Interpolant Generation        425

4    SOS Formulation
Similar to [7], in this section, we discuss how to reduce the problem of ﬁnding
h(x) satisfying (1) to a sum of squares programming problem.
Theorem 5. Let φ(x, y) and ψ(x, z) be deﬁned as in the Problem 1. Then there
exist m + n + 2 SOS (sum of squares) polynomials ui (x, y) (i = 1, . . . , m + 1),
vj (x, z) (j = 1, . . . , n + 1) and a polynomial h(x) such that
                         m                                 n
              h−1=            ui fi + um+1 ,   −h − 1 =         vj gj + vn+1 ,         (8)
                        i=1                               j=1

and h(x) > 0 is an interpolant for φ(x, y) and ψ(x, z).
Proof. By Theorem 2 there exists a polynomial ĥ(x) such that

             ∀x ∈ Px (φ(x, y)).ĥ(x) > 0,      ∀x ∈ Px (ψ(x, z)).ĥ(x) < 0.
Set S1 = {(x, y) | f1 ≥ 0, . . . , fm ≥ 0} and S2 = {(x, z) | g1 ≥ 0, . . . , gn ≥
0}. Since ĥ(x) > 0 on S1 , which is compact, there exist 1 > 0 such that
ĥ(x) − 1 > 0 on S1 . Similarly, there exist 2 > 0 such that −ĥ(x) − 2 > 0
on S2 . Let  = min(1 , 2 ), and h(x) = ĥ(x)       , then h(x) − 1 > 0 on S1 and
−h(x) − 1 > 0 on S2 . Since Mx,y (f1 (x, y), . . . , fm (x, y)) is Archimedean, from
Theorem 3, we have h(x) − 1 ∈ Mx,y (f1 (x, y), . . . , fm (x, y)). Similarly, −h(x) −
1 ∈ Mx,z (g1 (x, z), . . . , gn (x, z)). That is, there exist m + n + 2 SOS polynomials
ui , vj satisfying the following semi-deﬁnite constraints:
                         m                                      n
           h(x) − 1 =         ui fi + um+1 ,   −h(x) − 1 =           vj gj + vn+1 .
                        i=1                                    j=1
   According to Theorem 5, the problem of ﬁnding h(x) ∈ R[x] solving
Problem 1 can be equivalently reformulated as the problem of searching for
SOS polynomials u1 (x, y), . . . , um (x, y), v1 (x, z), . . . , vn (x, z) and a polynomial
h(x) with appropriate degrees such that
                   ⎧                   m
                   ⎪
                   ⎪
                   ⎪
                   ⎪  h(x)   −   1  −     ui fi ∈        R[x, y]2 ,
                   ⎪
                   ⎪
                   ⎪
                   ⎪                  i=1
                   ⎪
                   ⎪
                   ⎪
                   ⎨
                                          n
                      − h(x) − 1 −             vj gj ∈        R[x, z]2 ,                (9)
                   ⎪
                   ⎪                     j=1
                   ⎪
                   ⎪
                   ⎪
                   ⎪
                   ⎪ ui ∈
                   ⎪               R[x, y]2 , i = 1, . . . , m,
                   ⎪
                   ⎪
                   ⎪
                   ⎩v ∈
                       j           R[x, z]2 , j = 1, . . . , n.

(9) is SOS constraints over SOS multipliers u1 (x, y), . . . , um (x, y), v1 (x, z),
. . . , vn (x, z), polynomial h(x), which is convex and could be solved by many
existing semi-deﬁnite programming solvers such as the optimization library
AiSat [7] built on CSDP [4]. Therefore, according to Theorem 5, h(x) > 0 is
an interpolant for φ and ψ, which is formulated in Theorem 6.
426       T. Gan et al.

Theorem 6 (Soundness). Suppose that φ(x, y) and ψ(x, z) are deﬁned as in
Problem 1, and h(x) is a feasible solution to (9), then h(x) solves Problem 1,
i.e. h(x) > 0 is an interpolant for φ and ψ.

     Moreover, we have the following completeness           theorem stating
                                                                            that 2if the
degrees of h(x) ∈ R[x] and ui (x, y) ∈              R[x, y]2 , vj (x, z) ∈  R[x, z] , i =
1, . . . , m, j = 1, . . . , n, are large enough, h(x) can be synthesized deﬁnitely via
solving (9).
Theorem 7 (Completeness). For Problem 1, there must be polynomials
ui (x, y) ∈ RN [x, y] (i = 1, . . . , m), vj (x, z) ∈ RN [x, z] (j = 1, . . . , n) and
h(x) ∈ RN [x] satisfying (11) for some positive integer N , where Rk [·] stands
for the family of polynomials of degree no more than k.

Proof. This is an immediate result of Theorem 5.

Example 2. Consider two contradictory formulas φ and ψ deﬁned by
f1 (x, y, z, a1 , b1 , c1 , d1 ) ≥ 0 ∧ f2 (x, y, z, a1 , b1 , c1 , d1 ) ≥ 0 ∧ f3 (x, y, z, a1 , b1 , c1 , d1 ) ≥ 0,
g1 (x, y, z, a2 , b2 , c2 , d2 ) ≥ 0 ∧ g2 (x, y, z, a2 , b2 , c2 , d2 ) ≥ 0 ∧ g3 (x, y, z, a2 , b2 , c2 , d2 ) ≥ 0,

respectively, where
f1 = 4 − x2 − y 2 − z 2 − a21 − b21 − c21 − d21 ,          f2 = −y 4 + 2x4 − a41 − 1/100,
f3 = z 2 − b21 − c21 − d21 − x − 1,                        g1 = 4 − x2 − y 2 − z 2 − a22 − b22 − c22 − d22 ,
g2 = x2 − y − a2 − b2 − d22 − 3,                           g3 = x.

  It is easy to observe that φ and ψ satisfy the conditions in Problem 1. Since
there are local variables in φ and ψ and the degree of f2 is 4, the interpolant
generation methods in [7] and [10] are not applicable. We get a concrete SDP
problem of the form (9) by setting the degree of the polynomial h(x, y, z) in (9)
to be 2. Using the MATLAB package YALMIP [23] and Mosek [28], we obtain
      h(x, y, z) = − 416.7204 − 914.7840x + 472.6184y + 199.8985x2 + 190.2252y 2
                      + 690.4208z 2 − 187.1592xy.


    Pictorially, we plot Px,y,z (φ(x, y, z, a1 , b1 , c1 , d1 )), Px,y,z (ψ(x, y, z, a2 , b2 , c2 ,
d2 )) and {(x, y, z) | h(x, y, z) > 0} in Fig. 2. It is evident that h(x, y, z) as
presented above for dh = 2 is a real interpolant for φ(x, y, z, a, b, c, d) and
ψ(x, y, z, a, b, c, d).
                                          Nonlinear Craig Interpolant Generation         427

5    Avoidance of the Unsoundness Due to Numerical Error
     in SDP

In this section, we discuss how to
avoid the unsoundness of our app-
roach caused by numerical error in
SDP based on the work in [32].
   A square matrix A is positive
semideﬁnite if A is real symmetric
and all its eigenvalues are nonnegative,
denote by A  0.
   In order to solve formula (9) to
obtain h(x), we ﬁrst need to ﬁx a
degree bound of ui , vj and h, say
2d, d ∈N. It is well-known that any
u(x) ∈ R[x]2 with degree 2d can be
represented by

     u(x) ≡ Ed (x)T Cu Ed (x),           (10)
                 r+d  r+d
                                                 Fig. 2. Example 2. (Red region: Px,y,z
where Cu ∈ R( d )×( d ) with Cu  (φ(x, y, z, a1 , b1 , c1 , d1 )); green region:
0, Ed (x) is a column vector with all Px,y,z (ψ(x, y, z, a2 , b2 , c2 , d2 )); gray region:
monomials in x, whose total degree is {(x, y, z) | h(x, y, z) > 0}.) (Color ﬁgure
not greater than d, and Ed (x)T stands online)
for the transposition of Ed (x). Equaling the corresponding coeﬃcient of each
monomial whose degree is less than or equal to 2d at the two sides of (10), we
can get a linear equation system as

                          tr(Au,k Cu ) = bu,k , k = 1, . . . , Ku ,                      (11)
                  r+d     r+d
where Au,k ∈ R( d )×( d ) is constant matrix, bu,k ∈ R is constant, tr(A) stands
for the trace of matrix A. Thus, searching for ui , vj and h satisfying (9) can be
reduced to the following SDP problem:

            find : Cu1 , . . . , Cum , Cv1 , . . . , Cvn , Ch ,
              s.t. tr(Aui ,k Cui ) = bui ,k , i = 1, . . . , m, k = 1, . . . , Kui ,
                     tr(Avj ,k Cvj ) = bvj ,k , j = 1, . . . , n, k = 1, . . . , Kvj ,   (12)
                     tr(Ah,k Ch ) = bh,k , k = 1, . . . , Kh ,
            diag(Cu1 , . . . , Cum , Cv1 , . . . , Cvn , Ch−1−uf , C−h−1−vg )  0,
                                                                              m
where Ch−1−uf is the matrix corresponding to polynomial h − 1 − i=1 ui fi ,
which is a linear combination of Cu1 , . . . , Cum andCh ; similarly, C−h−1−vg is
                                                          n
the matrix corresponding to polynomial −h − 1 − j=1 vj gj , which is a linear
combination of Cv1 , . . . , Cvn and Ch ; and diag(C1 , . . . , Ck ) is a block-diagonal
matrix of C1 , . . . , Ck .
428     T. Gan et al.

    Let D be the dimension of C = diag(Cu1 , . . . , C−h−1−vg ), i.e.,
diag(Cu1 , . . . , C−h−1−vg ) ∈ RD×D and C    be the approximate solution to (12)
returned by calling a numerical SDP solver, the following theorem is proved in
[32].
Theorem 8 ([32], Theorem 3). C  0 if there exists C               ∈ FD×D such that
the following conditions hold: 1. C                                  ii ≤ Cii − α, for
                                      ij = Cij , for any i = j; 2. C
any i; and 3. the Cholesky algorithm implemented in ﬂoating-point arithmetic
can conclude that C    is positive semi-deﬁnite, where F is a ﬂoating-point format,
       (D+1)κ
α = 1−(2D+2)κ tr(C) + 4(D + 1)(2(D + 2) + maxi {Cii })η, in which κ is the unit
roundoﬀ of F and η is the underﬂow unit of F.
Corollary 2. Let C      ∈ FD×D . Suppose that (D+1)Dκ + 4(D + 1)η ≤ 1 , β =
                                            1−(2D+2)κ                   2
  (D+1)κ
          tr(  + 4(D + 1)(2(D + 2) + maxi {C
             C)                              ii })η > 0, where F is a ﬂoating-
1−(2D+2)κ
point format. Then C +2βI  0 if the Cholesky algorithm based on ﬂoating-point
                        i.e., concludes that C
arithmetic succeeds on C,                      is positive semi-deﬁnite.
    According to Remark 5 in [32], for IEEE 754 binary64 format with rounding
to nearest, κ = 2−53 ( 10−16 ) and η = 2−1075 ( 10−323 ). In this case, the order
of magnitude of β is 10−10 and 1−(2D+2)κ
                                      (D+1)Dκ
                                                  +4(D +1)η is 10−13 , much less than 12 .
Obviously, β becomes smaller when the length of binary format becomes longer.
W.l.o.g., we suppose that the Cholesky algorithm succeed in computing C             the
solution of (12), which is reasonable as if an SDP solver returns a solution C,       
then C should be considered to be positive semi-deﬁnite in the sense of numeric
computation.
    So, by Corollary 2, we have C     + 2βI  0 holds, where I is the identity matrix
with the corresponding dimension. Then we have
        diag(C             u , C
              u , . . . , C    v , . . . , C
                                             v , C
                                                  h−1−uf , C
                                                            −h−1−vg ) + 2βI  0.
                 1             m    1         n


     Let  = maxp∈P,1≤i≤Kp |tr(Ap,i C           p ) − bp,i |, where P = {u1 , . . . , um ,
v1 , . . . , vn , h}, which can be regarded as the tolerance of the SDP solver. Since
|tr(Ap,i Cp ) − bp,i | is the error term for each monomial of p, i.e.,  can be con-
sidered as the error bound on the coeﬃcients of polynomials ui , vj and h, for
any polynomial ûi ( vˆj and ĥ), computed from (11) by replacing Cu with the
corresponding C       u , there exists a corresponding remainder term Ru (resp. Rv
                                                                         i               j
and Rh ) with degree not greater than 2d, whose coeﬃcients are bounded by .
Hence, we have
       ui + Rui + 2βEd (x, y)T Ed (x, y) ∈           R[x, y]2 , i = 1, . . . , m,

       vj + Rvj + 2βEd (x, z)T Ed (x, z) ∈          R[x, z]2 , j = 1, . . . , n,
                        m
       
       h + Rh − 1 −           (ui + Ru i )fi + 2βEd (x, y)T Ed (x, y) ∈           R[x, y]2 , (13)
                        i=1
                         m
      −
       h + Rh − 1 −          (vj + Rv j )gj + 2βEd (x, z)T Ed (x, z) ∈           R[x, z]2 .
                        j=1
                                                Nonlinear Craig Interpolant Generation              429

    Now, in order to avoid unsoundness of our approach caused by the numerical
issue due to SDP, we have to prove
                                 f1 ≥ 0 ∧ · · · ∧ fm ≥ 0 ⇒ 
                                                           h > 0,                                  (14)
                                 g1 ≥ 0 ∧ · · · ∧ gn ≥ 0 ⇒ 
                                                           h < 0.                                  (15)
   Regarding (14), let R2d,x be a polynomial in R[|x|], whose total degree is 2d,
and all coeﬃcients are 1, e.g., R2,x,y = 1 + |x| + |y| + |x2 | + |xy| + |y 2 |. Since
S = {(x, y) | f1 ≥ 0 ∧ · · · ∧ fm ≥ 0} is a compact set, then for any polynomial
p ∈ R[x, y], |p| is bounded on S. Let M1 be an upper bound of R2d,x,y on S,
M2 an upper bound of Ed (x, y)T Ed (x, y), and Mfi an upper bound of fi on S.
Then, |Rui |, |Ru i | and |Rh | are bounded by M1 . Let Exy = Ed (x, y)T Ed (x, y).
So for any (x0 , y0 ) ∈ S, considering the polynomials below at (x0 , y0 ) ∈ S, by
the ﬁrst and third line in (13),
                      m

h ≥ 1 − Rh +              (ui + Ru i )fi − 2βExy
                      i=1
                        m
     ≥ 1 − M1 +             (ui + Rui + 2βExy + Ru i − Rui − 2βExy )fi − 2βM2
                       i=1
                                   m                                   m
     = 1 − M1 − 2βM2 +                 (ui + Rui + 2βExy )fi +            (Ru i − Rui − 2βExy )fi
                                  i=1                                 i=1
                                         m
     ≥ 1 − M1 − 2βM2 + 0 −                   (M1 + M1 + 2βM2 )Mfi
                                        i=1
                m                              m
     = 1 − (2         Mfi + 1)M1  − 2(              Mfi + 1)M2 β.
                i=1                            i=1

Whence,
                                                      m                         m
     f1 ≥ 0 ∧ · · · ∧ fm ≥ 0 ⇒ 
                               h ≥ 1 − (2                   Mfi + 1)M1  − 2(           Mfi + 1)M2 β.
                                                      i=1                       i=1

    Let S  = {(x, z) | g1 ≥ 0 ∧ · · · ∧ gn ≥ 0}, M3 be an upper bound of R2d,x,z on
S , M4 an upper bound of Ed (x, z)T Ed (x, z) on S  , and Mgj an upper bound of
 

gj on S  . Similarly, it follows
                                                        n                           n
g1 ≥ 0 ∧ · · · ∧ gn ≥ 0 ⇒          −
                                    h ≥ 1 − (2               Mgj + 1)M3  − 2(           Mgj + 1)M4 β.
                                                       j=1                       j=1

      So, the following proposition is immediately.
Proposition 2. There exist two positive constants γ1 and γ2 such that
                           f1 ≥ 0 ∧ · · · ∧ fm ≥ 0 ⇒ 
                                                     h ≥ 1 − γ1  − γ2 β,                          (16)
                          g1 ≥ 0 ∧ · · · ∧ gn ≥ 0 ⇒ −
                                                     h ≥ 1 − γ1  − γ2 β.                          (17)
430     T. Gan et al.

   Since  and β heavily rely on the numerical tolerance and the ﬂoating point
representation, it is easy to see that  and β become small enough with γ1  < 12
and γ2 β < 12 , if the numerical tolerance is small enough and the length of the
ﬂoating point representation is long enough. This implies

       f1 ≥ 0 ∧ · · · ∧ fm ≥ 0 ⇒ 
                                 h > 0,       g1 ≥ 0 ∧ · · · ∧ gn ≥ 0 ⇒ −
                                                                         h > 0.

If so, any numerical result 
                            h > 0 returned by calling an SDP solver to (12)
is guaranteed to be a real interpolant for φ and ψ, i.e., a correct solution to
Problem 1.

Example 3. Consider the numerical result for Example 2 in Sect. 4. Let Mf1 ,
Mf2 , Mf3 , Mg1 , Mg2 , Mg3 , M1 , M2 , M3 , M4 are deﬁned as above. It is easy to
see that

 f1 ≥ 0 ⇒|x| ≤ 2 ∧ |y| ≤ 2 ∧ |z| ≤ 2 ∧ |a1 | ≤ 2 ∧ |b1 | ≤ 2 ∧ |c1 | ≤ 2 ∧ |d1 | ≤ 2.

Then, by simple calculations, we obtain Mf1 = 4, Mf2 = 32, Mf3 = 3, M1 =
83, M2 = 29. Thus,
                   m                                m
              (2         Mfi + 1)M1 = 6557,   2(         Mfi + 1)M2 = 2320.
                   i=1                             i=1

Also, since

  g1 ≥ 0 ⇒|x| ≤ 2 ∧ |y| ≤ 2 ∧ |z| ≤ 2 ∧ |a2 | ≤ 2 ∧ |b2 | ≤ 2 ∧ |c2 | ≤ 2 ∧ |d2 | ≤ 2,

we obtain Mg1 = 4, Mg2 = 7, Mg3 = 2, M3 = 83, M4 = 29. Thus,
                    m                               m
              (2         Mgi + 1)M3 = 2241,    2(         Mgi + 1)M4 = 812.
                   i=1                              i=1

Consequently, we have γ1 = 6557 and γ2 = 2320 in Proposition 2.
   Due to the fact that the default error tolerance is 10−8 in the SDP solver
                                                             −4
Mosek and h is rounding to 4 decimal places, we have  = 102 . In addition, as
                                       is less than 103 , and the dimension of
the absolute value of each element in C
                 3
D is less than 10 , we obtain
             (D + 1)κ        + 4(D + 1)(2(D + 2) + max(C
                                                        ii ))η ≤ 10−6 .
      β=                 tr(C)
           1 − (2D + 2)κ                             i

                                  −4
Consequently, γ1  ≤ 6557 · 102 < 12 , γ2 β ≤ 2320 · 10−6 < 12 , which imply that
h(x, y, z) > 0 presented in Example 2 is indeed a real interpolant.

Remark 1. Besides, the result could be veriﬁed by the following symbolic com-
putation procedure instead: computing Px (φ) and Px (ψ) ﬁrst by some sym-
bolic tools, such as Redlog [8] which is a package that extends the com-
puter algebra system REDUCE to a computer logic system; then verifying
                                                     Nonlinear Craig Interpolant Generation                          431

x ∈ Px (φ) ⇒ h(x) > 0 and x ∈ Px (ψ) ⇒ h(x) < 0. For this example, Px,y,z (φ)
and Px,y,z (ψ) obtained by Redlog are too complicated and therefore not pre-
sented here. The symbolic computation can verify that h(x, y, z) in this example
is exactly an interpolant, which conﬁrms our conclusion. Alternatively, we can
also solve the SDP in (9) using a SDP solver with inﬁnite precision [15], and
obtain an exact result. But this only works for problems with small size because
a SDP solver with inﬁnite precision is essentially based on symbolic computation
as commented in [15].

6    Generalizing to General Polynomial Formulas
Problem 2. Let φ(x, y) and ψ(x, z) be two polynomial formulas deﬁned as fol-
lows,
                 m                 Ki                                    n                  Sj
                                                                                         
     φ(x, y) :         φi , φi =         fi,k (x, y) ≥ 0;   ψ(x, z) :          ψj , ψ j =         gj,s (x, z) ≥ 0,
                 i=1               k=1                                   j=1                s=1


where all fi,k and gj,s are polynomials. Suppose φ ∧ ψ |= ⊥, and for i = 1, . . . , m,
j = 1, . . . , n, {(x, y) | φi (x, y)} and {(x, z) | ψj (x, z)} are all semi-algebraic sets
of the Archimedean form. Find a polynomial h(x) such that h(x) > 0 is an
interpolant for φ and ψ.
Theorem 9. For Problem 2, there exists a polynomial h(x) satisfying
              ∀x ∈ Px (φ(x, y)).h(x) > 0,                   ∀x ∈ Px (ψ(x, z)).h(x) < 0.
Proof. We just need to prove that Lemma 1 holds for Problem 2 as well. Since
{(x, y) | φi (x, y)} and {(x, z) | ψj (x, z)} are all semi-algebraic sets of the
Archimedean form, then {(x, y) | φ(x, y)} and {(x, z) | ψ(x, z)} both are com-
pact. See {(x, y) | φ(x, y)} or {(x, z) | ψ(x, z)} as S in the proof of Lemma
1, then Lemma 1 holds for Problem 2. Thus, the rest of proof is same as that
forTheorem 2.
Corollary 3. Let φ(x, y) and ψ(x, z) be deﬁned as in Problem 2. There must
exist a polynomial h(x) such that h(x) > 0 is an interpolant for φ and ψ.
Theorem 10. Let φ(x, y) and            ψ(x, z) be deﬁnedas in Problem 2. Then there
                                         m                   n
exists a polynomial h(x) and             i=1 (Ki + 1) +      j=1 (Sj + 1) sum of squares
polynomials ui,k (x, y) (i = 1, . . . , m, k = 1, . . . , Ki + 1), vj,s (x, z) (j = 1, . . . , n,
s = 1, . . . , Sj ) satisfying the following semi-deﬁnite constraints such that h(x) >
0 is an interpolant for φ(x, y) and ψ(x, z):
                                     Ki
                        h−1=               ui,k fi,k + ui,Ki +1 ,        i = 1, . . . , m;                           (18)
                                    k=1
                                           Sj
                        −h−1=                   vj,s gj,s + vj,Sj +1 ,       j = 1, . . . , n.                       (19)
                                          s=1

Proof. By the property of Archimedean, the proof is same as that for T
heorem 5.
432       T. Gan et al.

   Similarly, Problem 2 can be equivalently reformulated as the problem of
searching for sum of squares polynomials satisfying
             ⎧
             ⎪
             ⎪
                            Ki
             ⎪
             ⎪       −   −      ui,k fi,k ∈        R[x, y]2 , i = 1, . . . , m;
             ⎪
             ⎪
                h(x)   1
             ⎪
             ⎪
             ⎪
             ⎪
                           k=1
             ⎪
             ⎪
             ⎨                  Sj
                − h(x) − 1 −       vj,s gj,s ∈        R[x, z]2 , j = 1, . . . , n; (20)
             ⎪
             ⎪
             ⎪
             ⎪
                               s=1
             ⎪
             ⎪
             ⎪
             ⎪  ui,k ∈    R[x, y]2 , i = 1, . . . , m, k = 1, . . . , Ki ;
             ⎪
             ⎪
             ⎪
             ⎪
             ⎩ vj,s ∈     R[x, z]2 , j = 1, . . . , n, s = 1, . . . , Sj .

Example 4. Consider
             φ(x, y, a1 , a2 , b1 , b2 ) : (f1 ≥ 0 ∧ f2 ≥ 0) ∨ (f3 ≥ 0 ∧ f4 ≥ 0),
             ψ(x, y, c1 , c2 , d1 , d2 ) : (g1 ≥ 0 ∧ g2 ≥ 0) ∨ (g3 ≥ 0 ∧ g4 ≥ 0),


where


   f1 = 16 − (x + y − 4)2 − 16(x − y)2 − a21 ,           f2 = x + y − a22 − (2 − a2 )2 ,
      f3 = 16 − (x + y + 4)2 − 16(x − y)2 − b21 ,      f4 = −x − y − b22 − (2 − b2 )2 ,
      g1 = 16 − 16(x + y)2 − (x − y + 4)2 − c21 ,        g2 = y − x − c22 − (1 − c2 )2 ,
   g3 = 16 − 16(x + y)2 − (x − y − 4)2 − d21 ,           g4 = x − y − d22 − (1 − d2 )2 .
 We get a concrete SDP problem of the form (20) by setting the degree of h(x, y)
in (20) to be 2. Using the MATLAB package YALMIP and Mosek, we obtain
                h(x, y) = −2.3238 + 0.6957x2 + 0.6957y 2 + 7.6524xy.
The result is plotted in Fig. 3, and can be veriﬁed either by numerical error
analysis as in Example 2 or by a symbolic procedure like REDUCE as described
in Remark 1.

Example 5 (Ultimate). Consider the following example taken from [5], which is
a challenging benchmark to existing approaches for nonlinear interpolant gener-
ation.
              φ = (f1 ≥ 0 ∧ f2 ≥ 0 ∨ f3 ≥ 0) ∧ f4 ≥ 0 ∧ f5 ≥ 0 ∨ f6 ≥ 0,
              ψ = (g1 ≥ 0 ∧ g2 ≥ 0 ∨ g3 ≥ 0) ∧ g4 ≥ 0 ∧ g5 ≥ 0 ∨ g6 ≥ 0,
where
                f1 = 3.8025 − x2 − y 2 ,          f2 = y,
                f3 = 0.9025 − (x − 1)2 − y 2 ,    f4 = (x − 1)2 + y 2 − 0.09,
                f5 = (x + 1)2 + y 2 − 1.1025,     f6 = 0.04 − (x + 1)2 − y 2 ,
                g1 = 3.8025 − x2 − y 2 ,          g2 = −y,
                g3 = 0.9025 − (x + 1)2 − y 2 ,    g4 = (x + 1)2 + y 2 − 0.09,
                g5 = (x − 1)2 + y 2 − 1.1025,     g6 = 0.04 − (x − 1)2 − y 2 .
                                             Nonlinear Craig Interpolant Generation     433




Fig. 3. Example 4. (Red region: Px,y                Fig. 4. Example 5. (Red region: Px,y
(φ(x, y, a1 , a2 , b1 , b2 )); green region:        (φ(x, y)); green region: Px,y (ψ(x, y));
Px,y (ψ(x, y, c1 , c2 , d1 , d2 )); gray region:    gray region: {(x, y) | h(x, y) > 0}.)
{(x, y) | h(x, y) > 0}.) (Color ﬁgure               (Color ﬁgure online)
online)


We ﬁrst convert φ and ψ to the disjunction normal form as:

φ =(f1 ≥ 0 ∧ f2 ≥ 0 ∧ f4 ≥ 0 ∧ f5 ≥ 0) ∨ (f3 ≥ 0 ∧ f4 ≥ 0 ∧ f5 ≥ 0) ∨ (f6 ≥ 0),
ψ =(g1 ≥ 0 ∧ g2 ≥ 0 ∧ g4 ≥ 0 ∧ g5 ≥ 0) ∨ (g3 ≥ 0 ∧ g4 ≥ 0 ∧ g5 ≥ 0) ∨ (g6 ≥ 0).

We get a concrete SDP problem of the form (20) by setting the degree of h(x, y)
in (20) to be 7. Using the MATLAB package YALMIP and Mosek, keeping the
decimal to four, we obtain
    h(x, y) = 1297.5980x + 191.3260y − 3172.9653x3 + 196.5763x2 y + 2168.1739xy 2
     + 1045.7373y 3 + 1885.8986x5 − 1009.6275x4 y + 3205.3793x3 y 2 − 1403.5431x2 y 3
     + 1842.0669xy 4 + 1075.2003y 5 − 222.0698x7 + 547.9542x6 y − 704.7474x5 y 2
     + 1724.7008x4 y 3 − 728.2229x3 y 4 + 1775.7548x2 y 5 − 413.3771xy 6 + 1210.2617y 7 .

 The result is plotted in Fig. 4, and can be veriﬁed either by numerical error
analysis as in Example 2 or by a symbolic procedure like REDUCE as described
in Remark 1.


7      Application to Invariant Generation
In this section, as an application, we sketch how to apply our approach to invari-
ant generation in program veriﬁcation, the details can be found in [11].
    In [22], Lin et al. proposed a framework for invariant generation using weakest
precondition, strongest postcondition and interpolation, which consists of two pro-
cedures, i.e., synthesizing invariants by forward interpolation based on strongest
434     T. Gan et al.

postcondition and interpolant generation, and by backward interpolation based
on weakest precondition and interpolant generation. In [22], only linear invari-
ants can be synthesized as no powerful approaches are available to synthesize
nonlinear interpolants. Obviously, our results can strengthen their framework by
allowing to generate nonlinear invariants. For example, we can revise the proce-
dure Squeezing Invariant - Forward in their framework and obtain Algorithm 1.
    The major revisions include:

– ﬁrstly, we exploit our method to synthesize interpolants see line 4 in Algo-
  rithm 1;
– secondly, we add a conditional statement for Ai+1 at line 7–10 in Algorithm 1
  in order to make Ai+1 to be Archimedean.

The procedure Squeezing Invariant - backward can be revised similarly.


Algorithm 1. Revised Squeezing Invariant - Forward
Input: An annotated loop: {P } while ρ do C {Q}, where P and Q are Archimedean
Output: (yes/no, I), where I is a loop invariant
 1: A0 ← P ; B0 ← (¬ρ ∧ ¬Q); i ← 0; j ← 0;
 2: while do                                
 3:   if ( ik=0 Ai ) ∧ Bj is not satisﬁable, ( ik=0 Ai ) and Bj are Archimedean then
                                                             
 4:      call our method to synthesize an interpolant for ( ik=0 Ai ) and Bj , say Ii ;
         {Use our method to generate interpolant}
 5:      if {Ii ∧ ρ} C {Ii } then
 6:         return (yes, Ii );
 7:      else if Ii is Archimedean then
 8:         Ai+1 ← sp(Ii ∧ ρ, C);
 9:      else
10:         Ai+1 ← sp(Ai ∧ ρ, C);
11:      end if
         {sp: a predicate transformer to compute the strongest postcondition of C w.r.t.
         Ii ∧ ρ}
12:      i ← i + 1; Bj+1 ← B0 ∨ (ρ ∧ wp(C, Bj ));
         {wp: a predicate transformer to compute the weakest precondition of C w.r.t.
         Bj }
13:      j ← j + 1;
14:   else if Ai is concrete then
15:      return (no, ⊥);
16:   else
17:      while Ai is not concrete do
18:         i ← i − 1;
19:      end while
20:      Ai+1 ← sp(Ai ∧ ρ, C); i ← i + 1;
21:   end if
22: end while
                                     Nonlinear Craig Interpolant Generation      435

Example 6. Consider a loop program given in Algorithm 2 for controlling the
acceleration of a car adapted from [21]. Suppose we know that vc is in [0, 40] at
the beginning of the loop, we would like to prove that vc < 49.61 holds after the
loop. Since the loop guard is unknown, it means that the loop may terminate
after any number of iterations.
    We apply Algorithm 1 to the computation of an invariant to ensure that
vc < 49.61 holds. Since vc is the velocity of car, 0 ≤ vc < 49.61 is required to hold
in order to maintain safety. Via Algorithm 1, we have A0 = {vc | vc(40−vc) ≥ 0}
and B = {vc | vc < 0} ∪ {vc | vc ≥ 49.61}. Here, we replace B with B  =
[−2, −1]∪[49.61, 55]), i.e., B  = {vc | (vc+2)(−1−vc) ≥ 0∨(vc−49.61)(55−vc) ≥
0}, in order to make it with Archimedean form.
    Firstly, it is evident that A0 : vc(40 − vc) ≥ 0 implies A0 ∧ B  |= ⊥. By
applying our approach, we obtain an interpolant

                    I0 : 1.4378 + 3.3947 ∗ vc − 0.083 ∗ vc2 > 0

for A0 and B  . It can be veriﬁed that {I0 } C {I0 } (line 5) does not hold, where
C stands for the loop body.
    Secondly, by setting A1 = sp(I0 , C) (line 8) and re-calling our approach, we
obtain an interpolant

                   I1 : 2.0673 + 3.0744 ∗ vc − 0.0734 ∗ vc2 > 0

for A0 ∪ A1 and B  . Likewise, it can be veriﬁed that {I1 } C {I1 } (line 5) does
not hold.


Algorithm 2. Control code for accelerating a car
1: /* Pre: vc ∈ [0, 40] */
2: while unknown do
3:   fa ← 0.5418 ∗ vc ∗ vc;
4:   f r ← 1000 − fa;
5:   ac ← 0.0005 ∗ f r;
6:   vc ← vc + ac;
7: end while
8: /* Post: vc < 49.61 */



   Thirdly, repeating the above procedure again, we obtain an interpolant

                   I2 : 2.2505 + 2.7267 ∗ vc − 0.063 ∗ vc2 > 0,

and it can be veriﬁed that {I2 } C {I2 } holds, implying that I2 is an invariant.
Moreover, it is trivial to verify that I2 ⇒ vc < 49.61.
   Consequently, we have the conclusion that I2 is an inductive invariant which
witnesses the correctness of the loop.
436     T. Gan et al.

8     Conclusion
In this paper we propose a sound and complete method to synthesize Craig inter-
polants for mutually contradictory polynomial formulas φ(x, y) and ψ(x, z), with
the form f1 ≥ 0 ∧ · · · ∧ fn ≥ 0, where fi ’s are polynomials in x, y or x, z and the
quadratic module generated by fi ’s is Archimedean. The interpolant is generated
by solving a semi-deﬁnite programming problem, which is a generalization of the
method in [7] dealing with mutually contradictory formulas with the same set of
variables and the method in [10] dealing with mutually contradictory formulas
with concave quadratic polynomial inequalities. As an application, we apply our
approach to invariant generation in program veriﬁcation.
    As a future work, we would like to consider interpolant synthesizing for for-
mulas with strict polynomial inequalities. Also, it deserves to consider how to
synthesize interpolants for the combination of non-linear formulas and other
theories based on our approach and other existing ones, as well as further appli-
cations to the veriﬁcation of programs and hybrid systems.

Acknowledgments. We thank Dr. Sicun Gao, Dr. Damien Zuﬀerey and Dr. Ming-
shuai Chen for their help on using dReal. We are indebted to anonymous reviewers for
their detailed and constructive criticisms and comments on the preliminary version,
which help to improve the presentation of this paper very much. This work is ﬁnan-
cially supported by NSFC under grants 61902284 (the ﬁrst author), 61732001 (the sec-
ond and fourth authors), 61532019 (the second author), 61836005 (the third author),
61625206 (the fourth author) and 61802318 (the ﬁfth author), and the third author is
also in part supported by Hundred Talents Program under grant No. Y8YC235015.


References
 1. Benhamou, F., Granvilliers, L.: Continuous and interval constraints. In: Handbook
    of Constraint Programming. Foundations of Artiﬁcial Intelligence, vol. 2, pp. 571–
    603 (2006)
 2. Bierstone, E., Milman, P.D.: Semianalytic and subanalytic sets. Publications Math-
    ematiques de l’IHÉS 67, 5–42 (1988)
 3. Bochnak, J., Coste, M., Roy, M.: Real Algebraic Geometry. Springer, Heidelberg
    (1998). https://doi.org/10.1007/978-3-662-03718-8
 4. Borchers, B.: CSDP, a C library for semideﬁnite programming. Optim. Methods
    Softw. 11(1–4), 613–623 (1999). http://projects.coin-or.org/csdp/
 5. Chen, M., Wang, J., An, J., Zhan, B., Kapur, D., Zhan, N.: NIL: learning nonlinear
    interpolants. In: Fontaine, P. (ed.) CADE 2019. LNCS (LNAI), vol. 11716, pp. 178–
    196. Springer, Cham (2019). https://doi.org/10.1007/978-3-030-29436-6 11
 6. Cimatti, A., Griggio, A., Sebastiani, R.: Eﬃcient interpolant generation in satis-
    ﬁability modulo theories. In: Ramakrishnan, C.R., Rehof, J. (eds.) TACAS 2008.
    LNCS, vol. 4963, pp. 397–412. Springer, Heidelberg (2008). https://doi.org/10.
    1007/978-3-540-78800-3 30
 7. Dai, L., Xia, B., Zhan, N.: Generating non-linear interpolants by semideﬁnite pro-
    gramming. In: Sharygina, N., Veith, H. (eds.) CAV 2013. LNCS, vol. 8044, pp.
    364–380. Springer, Heidelberg (2013). https://doi.org/10.1007/978-3-642-39799-
    8 25
                                       Nonlinear Craig Interpolant Generation        437

 8. Dolzmann, A., Sturm, T.: REDLOG: computer algebra meets computer logic. ACM
    SIGSAM Bull. 31(2), 2–9 (1997)
 9. D’Silva, V., Kroening, D., Purandare, M., Weissenbacher, G.: Interpolant strength.
    In: Barthe, G., Hermenegildo, M. (eds.) VMCAI 2010. LNCS, vol. 5944, pp. 129–
    145. Springer, Heidelberg (2010). https://doi.org/10.1007/978-3-642-11319-2 12
10. Gan, T., Dai, L., Xia, B., Zhan, N., Kapur, D., Chen, M.: Interpolant synthesis
    for quadratic polynomial inequalities and combination with EUF. In: Olivetti, N.,
    Tiwari, A. (eds.) IJCAR 2016. LNCS (LNAI), vol. 9706, pp. 195–212. Springer,
    Cham (2016). https://doi.org/10.1007/978-3-319-40229-1 14
11. Gan, T., Xia, B., Xue, B., Zhan, N.: Nonlinear Craig interpolant generation. CoRR,
    abs/1903.01297 (2019)
12. Gao, S., Kong, S., Clarke, E.: Proof generation from delta-decisions. In: SYNASC
    2014, pp. 156–163 (2014)
13. Gao, S., Zuﬀerey, D.: Interpolants in nonlinear theories over the reals. In: Chechik,
    M., Raskin, J.-F. (eds.) TACAS 2016. LNCS, vol. 9636, pp. 625–641. Springer,
    Heidelberg (2016). https://doi.org/10.1007/978-3-662-49674-9 41
14. Graf, S., Saidi, H.: Construction of abstract state graphs with PVS. In: Grum-
    berg, O. (ed.) CAV 1997. LNCS, vol. 1254, pp. 72–83. Springer, Heidelberg (1997).
    https://doi.org/10.1007/3-540-63166-6 10
15. Henrion, D., Naldi, S., Safey El Din, M.: Exact algorithms for semideﬁnite pro-
    grams with degenerate feasible set. In: ISSAC 2018, pp. 191–198 (2018)
16. Henzinger, T., Jhala, R., Majumdar, R., McMillan, K.: Abstractions from proofs.
    In: POPL 2004, pp. 232–244 (2004)
17. Jung, Y., Lee, W., Wang, B.-Y., Yi, K.: Predicate generation for learning-based
    quantiﬁer-free loop invariant inference. In: Abdulla, P.A., Leino, K.R.M. (eds.)
    TACAS 2011. LNCS, vol. 6605, pp. 205–219. Springer, Heidelberg (2011). https://
    doi.org/10.1007/978-3-642-19835-9 17
18. Kapur, D., Majumdar, R., Zarba, C.: Interpolation for data structures. In: FSE
    2006, pp. 105–116 (2006)
19. Kovács, L., Voronkov, A.: Interpolation and symbol elimination. In: Schmidt, R.A.
    (ed.) CADE 2009. LNCS (LNAI), vol. 5663, pp. 199–213. Springer, Heidelberg
    (2009). https://doi.org/10.1007/978-3-642-02959-2 17
20. Krajı́ček, J.: Interpolation theorems, lower bounds for proof systems, and indepen-
    dence results for bounded arithmetic. J. Symbol. Logic 62(2), 457–486 (1997)
21. Kupferschmid, S., Becker, B.: Craig interpolation in the presence of non-linear
    constraints. In: Fahrenberg, U., Tripakis, S. (eds.) FORMATS 2011. LNCS, vol.
    6919, pp. 240–255. Springer, Heidelberg (2011). https://doi.org/10.1007/978-3-
    642-24310-3 17
22. Lin, S., Sun, J., Xiao, H., Sanán, D., Hansen, H.: FiB: squeezing loop invariants
    by interpolation between forward/backward predicate transformers. In: ASE 2017,
    pp. 793–803 (2017)
23. Lofberg., J.: YALMIP: a toolbox for modeling and optimization in MATLAB. In:
    CACSD 2004, pp. 284–289. IEEE (2004)
24. Marshall, M.: Positive Polynomials and Sums of Squares. American Mathematical
    Society, Providence (2008)
25. McMillan, K.L.: Interpolation and SAT-based model checking. In: Hunt, W.A.,
    Somenzi, F. (eds.) CAV 2003. LNCS, vol. 2725, pp. 1–13. Springer, Heidelberg
    (2003). https://doi.org/10.1007/978-3-540-45069-6 1
26. McMillan, K.: An interpolating theorem prover. Theoret. Comput. Sci. 345(1),
    101–121 (2005)
438     T. Gan et al.

27. McMillan, K.L.: Quantiﬁed invariant generation using an interpolating saturation
    prover. In: Ramakrishnan, C.R., Rehof, J. (eds.) TACAS 2008. LNCS, vol. 4963, pp.
    413–427. Springer, Heidelberg (2008). https://doi.org/10.1007/978-3-540-78800-
    3 31
28. Mosek, A.: The MOSEK optimization toolbox for MATLAB manual. Version 7.1
    (Revision 28), p. 17 (2015)
29. Mostowski, T.: Some properties of the ring of nash functions. Annali della Scuola
    Normale Superiore di Pisa 3(2), 245–266 (1976)
30. Pudlǎk, P.: Lower bounds for resolution and cutting plane proofs and monotone
    computations. J. Symbol. Logic 62(3), 981–998 (1997)
31. Putinar, M.: Positive polynomials on compact semi-algebraic sets. Indiana Univ.
    Math. J. 42(3), 969–984 (1993)
32. Roux, P., Voronin, Y.-L., Sankaranarayanan, S.: Validating numerical semideﬁnite
    programming solvers for polynomial invariants. Formal Methods Syst. Des. 53(2),
    286–312 (2017). https://doi.org/10.1007/s10703-017-0302-y
33. Rybalchenko, A., Sofronie-Stokkermans, V.: Constraint solving for interpolation.
    J. Symb. Comput. 45(11), 1212–1233 (2010)
34. Sofronie-Stokkermans, V.: Interpolation in local theory extensions. In: Logical
    Methods in Computer Science, vol. 4, no. 4 (2008)
35. Srikanth, A., Sahin, B., Harris, W.: Complexity veriﬁcation using guided theorem
    enumeration. In: POPL 2017, pp. 639–652 (2017)
36. Stengle, G.: A nullstellensatz and a positivstellensatz in semialgebraic geometry.
    Ann. Math. 207, 87–97 (1974)
37. Yorsh, G., Musuvathi, M.: A combination method for generating interpolants. In:
    Nieuwenhuis, R. (ed.) CADE 2005. LNCS (LNAI), vol. 3632, pp. 353–368. Springer,
    Heidelberg (2005). https://doi.org/10.1007/11532231 26
38. Zhan, N., Wang, S., Zhao, H.: Formal Veriﬁcation of Simulink/Stateﬂow Diagrams.
    Springer, Cham (2017). https://doi.org/10.1007/978-3-319-47016-0
39. Zhao, H., Zhan, N., Kapur, D., Larsen, K.G.: A “hybrid” approach for synthesizing
    optimal controllers of hybrid systems: a case study of the oil pump industrial
    example. In: Giannakopoulou, D., Méry, D. (eds.) FM 2012. LNCS, vol. 7436, pp.
    471–485. Springer, Heidelberg (2012). https://doi.org/10.1007/978-3-642-32759-
    9 38



Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
     The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
