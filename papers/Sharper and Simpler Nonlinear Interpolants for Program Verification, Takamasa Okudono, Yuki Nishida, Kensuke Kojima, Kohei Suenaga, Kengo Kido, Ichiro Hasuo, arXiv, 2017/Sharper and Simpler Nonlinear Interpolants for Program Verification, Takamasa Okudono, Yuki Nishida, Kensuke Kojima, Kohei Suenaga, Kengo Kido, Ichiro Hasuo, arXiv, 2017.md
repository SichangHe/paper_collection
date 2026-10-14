                                                 Sharper and Simpler Nonlinear Interpolants
                                                          for Program Verification

                                                        Takamasa Okudono1 , Yuki Nishida2 , Kensuke Kojima2 ,
                                                         Kohei Suenaga2,3 , Kengo Kido1,4 , and Ichiro Hasuo5
                                                                     1
                                                                      University of Tokyo, Tokyo, Japan
                                                                 tokudono@is.s.u-tokyo.ac.jp
arXiv:1709.00314v1 [cs.LO] 1 Sep 2017




                                                                     2
                                                                        Kyoto University, Kyoto, Japan
                                                                       3
                                                                         JST PRESTO, Kyoto, Japan
                                                                  4
                                                                     JSPS Research Fellow, Tokyo, Japan
                                                              5
                                                                National Institute of Informatics, Tokyo, Japan




                                               Abstract. Interpolation of jointly infeasible predicates plays important roles in
                                               various program verification techniques such as invariant synthesis and CEGAR.
                                               Intrigued by the recent result by Dai et al. that combines real algebraic geometry
                                               and SDP optimization in synthesis of polynomial interpolants, the current pa-
                                               per contributes its enhancement that yields sharper and simpler interpolants. The
                                               enhancement is made possible by: theoretical observations in real algebraic ge-
                                               ometry; and our continued fraction-based algorithm that rounds off (potentially
                                               erroneous) numerical solutions of SDP solvers. Experiment results support our
                                               tool’s effectiveness; we also demonstrate the benefit of sharp and simple inter-
                                               polants in program verification examples.

                                               Keywords: program verification · interpolation · nonlinear interpolant · polyno-
                                               mial · real algebraic geometry · SDP optimization · numerical optimization



                                        1   Introduction

                                        Interpolation for Program Verification Interpolation in logic is a classic problem.
                                        Given formulas ϕ and ψ that are jointly unsatisfiable (meaning |= ϕ∧ψ ⇒ ⊥), one asks
                                        for a “simple” formula ξ such that |= ϕ ⇒ ξ and |= ξ ∧ ψ ⇒ ⊥. The simplicity require-
                                        ment on ξ can be a formal one (like the common variable condition, see Def. 2.6) but it
                                        can also be informal, like “ξ is desirably much simpler than ϕ and ψ (that are gigantic).”
                                        Anyway the intention is that ξ should be a simple witness for the joint unsatisfiability
                                        of ϕ and ψ, that is, an “essential reason” why ϕ and ψ cannot coexist.
                                            This classic problem of interpolation has found various applications in static anal-
                                        ysis and program verification [11, 13, 15, 21–23]. This is particularly the case with
                                        techniques based on automated reasoning, where one relies on symbolic predicate ab-
                                        straction in order to deal with infinite-state systems like (behaviors of) programs. It
                                        is crucial for the success of such techniques that we discover “good” predicates that
                                        capture the essence of the systems’ properties. Interpolants—as simple witnesses of
                                        incompatibility—have proved to be potent candidates for these “good” predicates.
2

Interpolation via Optimization and Real Algebraic Geometry A lot of research
efforts have been made towards efficient interpolation algorithms. One of the earliest
is [5]: it relies on Farkas’ lemma for synthesizing linear interpolants (i.e. interpolants
expressed by linear inequalities). This work and subsequent ones have signified the roles
of optimization problems and their algorithms in efficient synthesis of interpolants.
    In this line of research we find the recent contribution by Dai et al. [8] remarkable,
from both theoretical and implementation viewpoints. Towards synthesis of nonlin-
ear interpolants (that are expressed by polynomial inequalities), their framework in [8]
works as follows.
    – On the theory side it relies on Stengle’s Positivstellensatz—a fundamental result
      in real algebraic geometry [3, 33]—and relaxes the interpolation problem to the
      problem of finding a suitable “disjointness certificate.” The latter consists of a few
      polynomials subject to certain conditions.
    – On the implementation side it relies on state-of-the-art SDP solvers to efficiently
      solve the SDP problem that results from the above relaxation.
In [8] it is reported that the above framework successfully synthesizes nontrivial nonlin-
ear interpolants, where some examples are taken from program verification scenarios.
Contribution The current work contributes an enhancement of the framework from [8].
Our specific concerns are in sharpness and simplicity of interpolants.
Example 1.1 (sharp interpolant) Let T := (y > x ∧ x > −y) and
T 0 := (y ≤ −x2 ). These designate the blue and red areas in the figure,
respectively. We would like an interpolant S so that T implies S and
S is disjoint from T 0 . Note however that such an interpolant S must
be “sharp.” The areas of T and T 0 almost intersect with each other at
(x, y) = (0, 0). That is, the conditions T and T 0 are barely disjoint
in the sense that, once we replace > with ≥ in T , they are no longer
disjoint. (See Def. 3.1 for formal definitions.)
     The original framework in [8] fails to synthesize such “sharp” interpolants; and
this failure is theoretically guaranteed (see §3.1). In contrast our modification of the
framework succeeds: it yields an interpolant 8y + 4x2 > 0 (the green hatched area).

Example 1.2 (simple interpolant) Let T := (y ≥ x2 + 1) and T 0 :=
(y ≤ −x2 − 1). The implementation aiSat [6] of the workflow in [8]
succeeds and synthesizes an interpolant 284.3340y + 0.0012x2 y > 0.
In contrast our tool synthesizes 5y + 2 > 0 that is much simpler.

    The last two examples demonstrate two issues that we found in the original frame-
work in [8]. Our enhanced framework shall address these issues of sharpness and sim-
plicity, employing the following two main technical pieces.
    The first piece is sharpened Positivstellensatz-inspired relaxation (§3). We start with
the relaxation in [8] that reduces interpolation to finding polynomial certificates. We de-
vise its “sharp” variant that features: use of strict inequalities > (instead of disequalities
6=); and a corresponding adaptation of Positivstellensatz that uses a notion we call strict
cone. Our sharpened relaxation allows encoding to SDP problems, much like in [8].
                                                                                                 3

    The second technical piece that we rely on is our continued fraction-based round-
ing algorithm. We employ the algorithm in what we call the rounding-validation loop
(see §4), a workflow from [12] that addresses the challenge of numerical errors.
    Numerical relaxation of problems in automated reasoning—such as the SDP relax-
ation in [8] and in the current work—is nowadays common, because of potential per-
formance improvement brought by numerical solvers. However a numerical solution is
subject to numerical errors, and due to those errors, the solution may not satisfy the
original constraint. This challenge is identified by many authors [2, 12, 17, 26, 27, 29].
    Moreover, even if a numerical solution satisfies the original constraint, the solution
often involves floating-point numbers and thus is not simple. See Example 1.2, where
one may wonder if the coefficient 0.0012 should be simply 0. Such complication is
a disadvantage in applications in program verification, where we use interpolants as
candidates for “useful” predicates. These predicates should grasp essence and reflect
insights of programmers; it is our hypothesis that such predicates should be simple.
Similar arguments have been made in previous works such as [16, 34].
    To cope with the last challenges of potential unsoundness and lack of simplicity, we
employ a workflow that we call the rounding-validation loop. The workflow has been
used e.g. in [12]; see Fig. 1 (pp. 14) for a schematic overview. In the “rounding” phase
we apply our continued fraction-based rounding algorithm to a candidate obtained as a
numerical solution of an SDP solver. In the “validation” phase the rounded candidate is
fed back to the original constraints and their satisfaction is checked by purely symbolic
means. If validation fails, we increment the depth of rounding—so that the candidate
becomes less simple but closer to the original candidate—and we run the loop again.
Example 1.3 (invalid interpolant candicate) Let T = (y ≤ −1), T 0 =
(x2 + y 2 < 1), as shown in the figure. These are barely disjoint and
hence the algorithm in [8] does not apply to it. In our workflow, the first
interpolant candidate that an SDP solver yields is f (x, y) ≥ 0, where
               −3.370437975 + 8.1145 × 10−14 x − 2.2469y + 1.1235y 2 − 2.2607 × 10−10 y 3 +
                                                                                          
   f (x, y) = 9.5379 × 10−11 x2 − 2.2607 × 10−10 x2 y − 4.8497 × 10−11 x2 y 2 − 1.1519 ×
                 −14 3              −11 4                −11 4
                                                                                             .
                10    x + 4.8935 × 10     x − 9.7433 × 10     y

Being the output of a numerical solver the coefficients are far from simple integers.
Here coefficients in very different scales coexist—for example one may wonder if the
coefficient 8.1145×10−14 for x could just have been 0. Worse, the above candidate is in
fact not an interpolant: x = 0, y = −1 is in the region of T but we have f (0, −1) < 0.
     By subsequently applying our rounding-validation loop, we eventually obtain a can-
didate 34y 2 − 68y − 102 ≥ 0, and its validity is guaranteed by our tool.
     This workflow of the rounding-validation loop is adopted from [12]. Our technical
contribution lies in the rounding algorithm that we use therein. It can be seen an ex-
tension of the well-known rounding procedure by continued fraction expansion. The
original procedure, employed e.g. in [26], rounds a real number into a rational number
(i.e. a ratio k1 : k2 between two integers). In contrast, our current extension rounds a
ratio r1 : · · · : rn between n real numbers into a simpler ratio k1 : · · · : kn .
     We have implemented our enhancement of [8]; we call our tool SSI NT (Sharp and
Simple Interpolants). Our experiment results support its effectiveness: the tool succeeds
in synthesizing sharp interpolants (while the workflow in [8] is guaranteed to fail);
4

and our program verification examples demonstrate the benefit of sharp and simple
interpolants (synthesized by our tool) in verification. The latter benefit is demonstrated
by the following example; the example is discussed in further detail later in §5.

Example 1.4 (program verification) Consider the imperative program in Listing 1.1
(pp. 17). Let us verify its assertion (the last line) by counterexample-guided abstraction
refinement (CEGAR) [4], in which we try to synthesize suitable predicates that separate
the reachable region (that is under-approximated by finitely many samples of execution
traces) and the unsafe region ((xa) + 2(ya) < 0). The use of interpolants as candidates
for such separating predicates has been advocated by many authors, including [13].
    Let us say that the first execution trace we sampled is the one in which the while
loop is not executed at all (1 → 2 → 3 → 4 → 16 in line numbers). Following the
workflow of CEGAR by interpolation, we are now required to compute an interpolant
of T := (xa = 0 ∧ ya = 0) and T 0 := ((xa) + 2(ya) < 0). Because T and T 0
are “barely disjoint” (in the sense of Example 1.1, that is, the closures of T and T 0 are
no longer disjoint), the procedure in [8] cannot generate any interpolant. In contrast,
our implementation—based on our refined use of Stengle’s positivstellensatz, see §3—
successfully discovers an interpolant (xa) + 2(ya) ≥ 0. This interpolant happens to be
an invariant of the program and proves the safety of the program.
    Later in §5 we explain this example in further detail.

Related Work Aside from the work by Dai et al. [8] on which we are based, there are
several approaches to polynomial interpolation in the literature. Gan et al. [9] consider
interpolation for polynomial inequalities that involve uninterpreted functions, with the
restriction that the degree of polynomials is quadratic. An earlier work with a similar
aim is [18] by Kupferschmid et al. Gao and Zufferey [10] study nonlinear interpolant
synthesis over real numbers. Their method can handle transcendental functions as well
as polynomials. Interpolants are generated from refutation, and represented as union
of rectangular regions. Because of this representation, although their method enjoys
δ-completeness (a notion of approximate completeness), it cannot synthesize sharp in-
terpolants like Example 1.1. Their interpolants tend to be fairly complicated formulas,
too, and therefore would not necessarily be suitable for applications like program veri-
fication (where we seek simple predicates; see §5).
    Putinar’s positivstellensatz [28] is a well-known variation of Stengle’s positivstel-
lensatz; it is known to allow simpler SDP relaxation than Stengle’s. However it does not
suit the purpose of the current paper because: 1) it does not allow mixture of strict and
non-strict inequalities; and 2) it requires a compactness condition. There is a common
trick to force strict inequalities in a framework that only allows non-strict inequalities,
namely to add a small perturbation. We find that this trick does not work in our program
verification examples; see §5.
    The problem with numerical errors in SDP solving has been discussed in the lit-
erature. Harrison [12] is one of the first to tackle the problem: the work introduces
the workflow of the rounding-validation loop; the rounding algorithm used there incre-
ments a denominator at each step and thus is simpler than our continued fraction-based
one. The same rounding algorithm is used in [2], as we observe in the code. Peyrl &
Parrilo [26], towards the goal of sum-of-square decomposition in rational coefficients,
                                                                                       5

employs a rounding algorithm by continued fractions. The difference from our current
algorithm is that they apply continued fraction expansion to each of the coefficients,
while our generalized algorithm simplifies the ratio between the coefficients altogether.
The main technical novelty of [26] lies in identification of a condition for validity of
a rounded candidate. This framework is further extended in Kaltofen et al. [17] for a
different optimization problem, combined with the Gauss–Newton iteration.
    More recently, an approach using a simultaneous Diophantine approximation algorithm—
that computes the best approximation within a given bound of denominator—is consid-
ered by Lin et al. [20]. They focus on finding a rational fine approximation to the output
of SDP solvers, and do not aim at simpler certificates. Roux et al. [29] proposes meth-
ods that guarantee existence of a solution relying on numerical solutions of SDP solvers.
They mainly focus on strictly feasible problems, and therefore some of our examples
in §5 are out of their scope. Dai et al. [7] address the same problem of numerical er-
rors in the context of barrier-certificate synthesis. They use quantifier elimination (QE)
for validation, while our validation method relies on a well-known characterization of
positive semidefiniteness (whose check is less expensive than QE; see §4.2).
Future Work The workflow of the rounding-validation loop [12] is simple but poten-
tially effective: in combination with our rounding algorithm based on continued frac-
tions, we speculate that the workflow can offer a general methodology for coping with
numerical errors in verification and in symbolic reasoning. Certainly our current imple-
mentation is not the best of the workflow: for example, the validation phase of §4 could
be further improved by techniques from interval arithmetic, e.g. from [30].
     Collaboration between numerical and symbolic computation in general (like in [1])
interests us, too. For example in our workflow (Fig. 1, pp. 14) there is a disconnection
between the SDP phase and later: passing additional information (such as gradients)
from the SDP phase can make the rounding-validation loop more effective.
     Our current examples are rather simple and small. While they serve as a feasibility
study of the proposed interpolation method, practical applicability of the method in
the context of program verification is yet to be confirmed. We plan to conduct more
extensive case studies, using common program verification benchmarks such as in [32],
making comparison with other methods, and further refining our method in its course.
Organization of the Paper In §2 we review the framework in [8]. Its lack of sharp-
ness is established in §3.1; this motivates our sharpened Positivstellensatz-inspired re-
laxation of interpolation in §3.2. In §4 we describe our whole workflow and its im-
plementation, describing the rounding-validation loop and the continued fraction-based
algorithm used therein. In §5 we present experimental results and discuss the benefits
in program verification. Some proofs and details are deferred to appendices.



2   Preliminaries

Here we review the previous interpolation algorithm by Dai et al. [8]. It is preceded by
its mathematical bedrock, namely Stengle’s Positivstellensatz [33].
6

2.1    Real Algebraic Geometry and Stengle’s Positivstellensatz

We write X for a sequence X1 , X2 , . . . , Xk of variables, and R[X] for the set of poly-
nomials in X1 , . . . , Xk over R. We sometimes write f (X) for a polynomial f ∈ R[X]
in order to signify that the variables in f are restricted to those in X.

Definition 2.1 (SAS6= ) A semialgebraic system with disequalities (SAS6= ) T , in vari-
ables X1 , X2 , . . . , Xk , is a sequence
                                                                                            
                 f1 (X) ≥ 0 , . . . , fs (X) ≥ 0 ,     g1 (X) 6= 0 , . . . , gt (X) 6= 0 ,
       T =                                                                                       (1)
                 h1 (X) = 0 , . . . , hu (X) = 0

of inequalities fi (X) ≥ 0, disequalities gj (X) 6= 0 and equalities hk (X) = 0. Here
fi , gj , hk ∈ R[X] are polynomials, for i ∈ [1, s], j ∈ [1, t] and k ∈ [1, u].
     For the SAS6= T in (1) in k variables, we say x ∈ Rk satisfies T if fi (x) ≥ 0,
gj (x) 6= 0 and hk (x) = 0 hold for all i, j, k. We let JT K ⊆ Rk denote the set of all
such x, that is, JT K := { x ∈ Rk | x satisfies T }.

Definition 2.2 (cone, multiplicative monoid, ideal) A set C ⊆ R[X] is a cone if it
satisfies the following closure properties: 1) f, g ∈ C implies f + g ∈ C; 2) f, g ∈ C
implies f g ∈ C; and 3) f 2 ∈ C for any f ∈ R[X].
    A set M ⊆ R[X] is a multiplicative monoid if it satisfies the following: 1) 1 ∈ M ;
and 2) f, g ∈ M implies f g ∈ M .
    A set I ⊆ R[X] is an ideal if it satisfies: 1) 0 ∈ I; 2) f, g ∈ I implies f + g ∈ I;
and 3) f g ∈ I for any f ∈ R[X] and g ∈ I.
    For a subset A of R[X], we write: C(A), M(A), and I(A) for the smallest cone,
multiplicative monoid, and ideal, respectively, that includes A.

The last notions encapsulate closure properties of inequality/disequality/equality pred-
icates, respectively, in the following sense. The definition of JT K ⊆ Rk is in Def. 2.1.

Lemma 2.3 Let x ∈ Rk and fi , gj , hk ∈ R[X].

 1. If x ∈ Jf1 ≥ 0, . . . , fs ≥ 0K, then f (x) ≥ 0 for all f ∈ C(f1 , . . . , fs ).
 2. If x ∈ Jg1 6= 0, . . . , gt 6= 0K, then g(x) 6= 0 for all g ∈ M(g1 , . . . , gt ).
 3. If x ∈ Jh1 = 0, . . . , hu = 0K, then h(x) = 0 for all h ∈ I(h1 , . . . , hu ).               t
                                                                                                  u

      The following theorem is commonly attributed to [33]. See also [3].

Theorem 2.4 (Stengle’s Positivstellensatz) Let T be the SAS6= in (1) (Def. 2.1). It
is infeasible (meaning JT K = ∅) if and only if there exist f ∈ C(f1 , . . . , fs ), g ∈
M(g1 , . . . , gt ) and h ∈ I(h1 , . . . , hu ) such that f + g 2 + h = 0.             t
                                                                                       u

The polynomials f, g, h can be seen as an infeasible certificate of the SAS6= T . The
“if” direction is shown easily: if x ∈ JT K then we have f (x) ≥ 0, g(x)2 > 0 and
h(x) = 0 (by Lem. 2.3), leading to a contradiction. The “only if” direction is nontrivial
and remarkable; it is however not used in the algorithm of [8] nor in this paper.
    SOS polynomials play important roles, both theoretically and in implementation.
                                                                                                            7

Definition 2.5 (sum of squares (SOS)) A polynomial is called a sum of squares (SOS)
if it can be written in the form p21 + · · · + p2N (for some polynomials p1 , . . . , pN ). Note
that C(∅) is exactly the set of sums of squares (Def. 2.2).


2.2     The Interpolation Algorithm by Dai et al.

Definition 2.6 (interpolant) Let T and T 0 be SAS6= ’s, in variables X, Y and in X, Z,
respectively, given in the following form. Here we assume that each variable in X
occurs both in T and T 0 , and that Y ∩ Z = ∅.
                                                                                      
     f1 (X, Y ) ≥ 0, . . . , fs (X, Y ) ≥ 0, g1 (X, Y ) 6= 0, . . . , gt (X, Y ) 6= 0,
T =
    h10(X, Y ) = 0, . . . , hu0 (X, Y ) = 0                                                               (2)
      f1 (X, Z) ≥ 0, . . . , fs0 (X, Z) ≥ 0, g10 (X, Z) 6= 0, . . . , gt0 0 (X, Z) 6= 0,
                                                                                         
 0
T =
      h01 (X, Z) = 0, . . . , h0u0 (X, Z) = 0

      Assume further that T and T 0 are disjoint, that is, JT K ∩ JT 0 K = ∅.
      An SAS6= S is an interpolant of T and T 0 if it satisfies the following:

 1. JT K ⊆ JSK;
 2. JSK ∩ JT 0 K = ∅; and
 3. (the common variable condition) the SAS6= S is in the variables X, that is, S
    contains only those variables which occur both in T and T 0 .

   Towards efficient synthesis of nonlinear interpolants Dai et al. [8] introduced a
workflow that hinges on the following variation of Positivstellensatz.

Theorem 2.7 (disjointness certificate in [8, §4]) Let T , T 0 be the SAS6= ’s in (2). As-
sume there exist

      fe ∈ C(f1 , . . . , fs , f10 , . . . , fs0 0 ) , g ∈ M(g1 , . . . , gt , g10 , . . . , gt0 0 ) and
                                                                                                           (3)
      h ∈ I(h1 , . . . , hu , h01 , . . . , h0u0 ) , such that 1 + fe + g 2 + e
      e                                                                                      h = 0 .

Assume further that fe allows a decomposition fe = f +f 0 , with some f ∈ C(f1 , . . . , fs )
and f 0 ∈ C(f10 , . . . , fs0 0 ). (An element e
                                               h in the ideal always allows a decomposition
h = h + h such that h ∈ I(h1 , . . . , hu ) and h0 ∈ I(h01 , . . . , h0u0 ).)
e         0

   Under the assumptions T and T 0 are disjoint. Moreover the SAS6=
                                                                 
                                   S := 1/2 + f + g 2 + h > 0                            (4)
satisfies the conditions of an interpolant of T and T 0 (Def. 2.6), except for Cond. 3. (the
common variable condition).

Proof. The proof is much like the “if” part of Thm. 2.4. It suffices to show that S is an
interpolant; then the disjointness of T and T 0 follows.
    To see JT K ⊆ JSK, assume x ∈ JT K. Then we have f (x) ≥ 0 and h(x) = 0 by
                               2                                          2
Lem. 2.3; additionally g(x) ≥ 0 holds too. Thus 1/2 + f (x) + g(x) + h(x) ≥
1/2 > 0 and we have x ∈ JSK.
8

Algorithm 1 The interpolation algorithm by Dai et al. [8]. Here 2 = {0, 1}
1: input: SAS6= ’s T , T 0 in (2), and b ∈ N (the maximum degree)
2: output: either an interpolant S of T and T 0 , or FAIL
                    Q0
3: h := ( ti=1 gi )( ti0 =1 gi00 ) ; g := hbb/2 deg(h)c
         Q
                                                          {g is roughly of degree b/2}
                  SOS             −
                                  →  −
                                     →0 −→ − →0
4: Solve PDioph        to find ( α , α , β , β ). Here:
                                                                   0
     – αi ∈ C(∅)≤b (for i ∈ 2s ) and αi0 0 ∈ C(∅)≤b (for i0 ∈ 2s ) are SOSs,
     – βj ∈ R[X]≤b (for j ∈ [1, u]) and βj0 0 ∈ R[X]≤b (for j 0 ∈ [1, u0 ]) are polynomials,
     – and they are subject to the constraint                          u         u0
            X                        X 0 0 i0              i0 0        X         X
       1+       αi f1i1 · · · fsis +    αi0 f 11 · · · f 0 ss0 + g 2 +   βj hj +    βj0 0 h0j 0 = 0 .
            i∈2s                   i0 ∈2s
                                            0                          j=1       j 0 =1
              −
              → − → −  →                                                                         (6)
   (SuchP(−
          →
          α , α0 , β , β 0 ) may not be found,
                                          P in which case return FAIL)
5: f := i∈2s αi f1i1 · · · fsis ; h := uj=1 βj hj
6: return S := 1/2 + f + g 2 + h > 0
                                           




    To see JSK ∩ JT 0 K = ∅, we firstly observe that the following holds for any x.
                                        2
         0 = 1 + f (x) + f 0 (x) + g(x) + h(x)    + h0 (x) by (3)
                                                                                (5)
           = 1/2 + f (x) + (g(x)) + h(x) + 1/2 + f 0 (x) + h0 (x) .
                                    2
                                                                       

   Assume x ∈ JSK∩JT 0 K. By x ∈ JSK we have 1/2+f (x)+(g(x))2 +h(x) > 0; and
by x ∈ JT 0 K we have f 0 (x) ≥ 0 and h0 (x) = 0 (Lem. 2.3), hence 1/2+f 0 (x)+h0 (x) ≥
1/2 > 0. Thus the right-hand side of (5) is strictly positive, a contradiction.       t
                                                                                      u
Note that we no longer have completeness: existence of an interpolant like (4) is not
guaranteed. Nevertheless Thm. 2.7 offers a sound method to construct an interpolant,
namely by finding a suitable disjointness certificate f, f 0 , g, h, h0 .
    The interpolation algorithm in [8] is shown in Algorithm 1, where search for a
disjointness certificate f, f 0 , g, h, h0 is relaxed to the following problem.

Definition 2.8 (PDiophSOS ) Let PDiophSOS stand for the following problem.

      Input:        polynomials ϕ1 , . . . , ϕn , ψ1 , . . . , ψm , ξ ∈ R[X], and
                    maximum degrees d1 , . . . , dn , e1 , . . . , em ∈ N
      Output:       SOSs s1 ∈ C(∅)≤d1 , . . . , sn ∈ C(∅)≤dn and
                    polynomials t1 ∈ R[X]≤e1 , . . . , tm ∈ R[X]≤em
                    such that s1 ϕ1 + · · · + sn ϕn + t1 ψ1 + · · · + tm ψm + ξ = 0

Here R[X]≤e denotes the set of polynomials in X whose degree is no bigger than e.
Similarly C(∅)≤d is the set of SOSs with degree ≤ d.
                        SOS
The
P problem    P PDioph        is principally about finding polynomials si , tj subject to
   i si ϕi +   j tj ψj + ξ = 0; this problem is known as polynomial Diophantine equa-
tions. In PDiophSOS SOS requirements are additionally imposed on part of a solution
(namely si ); degrees are bounded, too, for algorithmic purposes.
     In Algorithm 1 we rely on Thm. 2.7 to generate an interpolant: roughly speaking,
one looks for a disjointness certificate f, f 0 , g, h, h0 within a predetermined maximum
                                                                                                 9

degree b. This search is relaxed to an instance of PDiophSOS (Def. 2.8), with n =
         0
2s + 2s , m = u + u0 , and ξ = 1 + g 2 , as in Line 4. The last relaxation, introduced
                                                                                    − →
                                                                                    → −
in [8], is derived from the following representation of elements of the cone C( f , f 0 ),
                                     →
                                     −                     →
                                                           −    →
                                                                −
the multiplicative monoid M(→   −g , g 0 ) and the ideal I( h , h0 ), respectively.
                             − →
                             →   −                         Pu             Pu0
    – Each element h of I( h , h0 ) is of the form h = j=1 βj hj + j 0 =1 βj0 0 h0j 0 , where
      βj , βj 0 ∈ R[X]. This is a standard fact in ring theory.
                                 →
                                 −
    – Each element of M(→   −g , g 0 ) is given by the product of finitely many elements from
      →
      −    →
           −
      g , g 0 (here multiplicity matters). In Algorithm 1 a polynomial g is fixed to a “big”
      one. This is justified as follows: in case the constraint (6) is satisfiable using a
      smaller polynomial g 0 instead of g, by multiplying the whole equality (6) by 1 +
      (g/g 0 )2 we see that (6) is satisfiable using g, too.
                        − →
                        →   −
    – For the cone C( f , f 0 ) we use the following fact (here 2 = {0, 1}). The lemma
      seems to be widely known but we present a proof in Appendix A.1 for the record.

Lemma 2.9 An arbitrary element f of the cone C(f1 , . . . , fs ) can be expressed as f =
P          i1       is                            s
  i∈2s αi f1 . . . fs , using SOSs αi (where i ∈ 2 ).                                  t
                                                                                       u

The last representation justifies the definition of f and h in Algorithm 1 (Line 5). We
also observe that Line 6 of Algorithm 1 corresponds to (4) of Thm. 2.7.
    In implementing Algorithm 1 the following fact is crucial (see [8, §3.5] and also [24,
25] for details): the problem PDiophSOS (Def. 2.8) can be reduced to an SDP problem,
the latter allowing an efficient solution by state-of-the-art SDP solvers. It should be
noted, however, that numerical errors (inevitable in interior point methods) can pose a
serious issue for our application: the constraint (6) is an equality and hence fragile.


3     Positivstellensatz and Interpolation, Revisited

3.1     Analysis of the Interpolation Algorithm by Dai et al.

Intrigued by its solid mathematical foundation in real algebraic geometry as well as
its efficient implementation that exploits state-of-the-art SDP solvers, we studied the
framework by Dai et al. [8] (it was sketched in §2.2). In its course we obtained the
following observations that motivate our current technical contributions.
    We first observed that Algorithm 1 from [8] fails to find “sharp” interpolants for
“barely disjoint” predicates (see Example 1.1). This turns out to be a general phe-
nomenon (see Prop. 3.3).

Definition 3.1 (symbolic closure) Let T be the SAS6= ’s in (1). The symbolic closure
T• of T is the SAS6= that is obtained by dropping all the disequality constraints gj (x) 6=
0 in T .
                                                                                             
    T• = f1 (X, Y ) ≥ 0 , . . . , fs (X, Y ) ≥ 0 , h1 (X, Y ) = 0 , . . . , hu (X, Y ) = 0
                                                                                             (7)
10

The intuition of symbolic closure of T is to replace all strict inequalities gj0 (X, Y ) > 0
in T with the corresponding non-strict ones gj0 (X, Y ) ≥ 0. Since only ≥, 6= and =
are allowed in SAS6= ’s, strict inequalities gj0 (X, Y ) > 0 are presented in the SAS6= T
by using both gj0 (X, Y ) ≥ 0 and gj0 (X, Y ) 6= 0. The last definition drops the latter
disequality (6=) requirement.
    The notion of symbolic closure most of the time coincides with closure with respect
to the usual Euclidean topology, but not in some singular cases. See Appendix B.

Definition 3.2 (bare disjointness) Let T and T 0 be SAS6= ’s. T and T 0 are barely dis-
joint if JT K ∩ JT 0 K = ∅ and JT• K ∩ JT•0 K 6= ∅.
    An interpolant S of barely disjoint SAS6= ’s T and T 0 shall be said to be sharp.

    An example of barely disjoint SAS6= ’s is in Example 1.1: (0, 0) ∈ JT• K ∩ JT•0 K 6= ∅.
    Algorithm 1 does not work if the SAS6= ’s T and T 0 are only barely disjoint. In
fact, such failure is theoretically guaranteed, as the following result states. Its proof (in
Appendix A.2) is much like for Thm. 2.7.

Proposition 3.3 Let T and T 0 be the SAS6= ’s in (2). If T and T 0 are barely disjoint (in
                                                               − →
                                                               →    −                  →
                                                                                       −
the sense of Def. 3.2), there do not exist polynomials fe ∈ C( f , f 0 ), g ∈ M(→ −g , g0 )
           − →
           →    −
and eh ∈ I( h , h0 ) such that 1 + fe + g 2 + e
                                              h = 0.                                    t
                                                                                        u

The conditions in Prop. 3.3 on the polynomials fe, g, e
                                                      h are those for disjointness cer-
tificates for T and T 0 (Thm. 2.7). As a consequence: if T and T 0 are only barely dis-
joint, interpolation relying on Thm. 2.7—that underlies the framework in [8]—never
succeeds.


3.2    Interpolation via Positivstellensatz, Sharpened

The last observation motivates our “sharper” variant of Thm. 2.7—a technical contri-
bution that we shall present shortly in Thm. 3.8. We switch input formats by replacing
disequalities 6= (Def. 2.1) with <. This small change turns out to be useful when we
formulate our main result (Thm. 3.8).

Definition 3.4 (SAS< ) A semialgebraic system with strict inequalities (SAS< ) T , in
variables X1 , X2 , . . . , Xk , is a sequence
                                                                                       
                f1 (X) ≥ 0 , . . . , fs (X) ≥ 0 ,   g1 (X) > 0 , . . . , gt (X) > 0 ,
      T =                                                                                   (8)
                h1 (X) = 0 , . . . , hu (X) = 0

of inequalities fi (X) ≥ 0, strict inequalities gj (X) > 0 and equalities hk (X) = 0.
Here fi , gj , hk ∈ R[X] are polynomials; JT K ⊆ Rk is defined like in Def. 2.1.

    SAS< ’s have the same expressive power as SAS6= ’s, as witnessed by the following
mutual translation. For the SAS6= T in (1), the SAS< Te := fi (X) ≥ 0, gj2 (X) >
               
0, hk (X) = 0 i,j,k satisfies JT K = JTe K. Conversely, for the SAS< T in (8), the SAS6=
                                                             
Tb := fi (X) ≥ 0, g 2 (X) ≥ 0, g 2 (X) 6= 0, hk (X) = 0
                          j             j                         satisfies JT K = JTb K.
                                                                 i,j,k
                                                                                                            11

   One crucial piece for Positivstellensatz was the closure properties of inequalities/dis-
equalities/equalities encapsulated in the notions of cone/multiplicative monoid/ideal
(Lem. 2.3). We devise a counterpart for strict inequalities.
Definition 3.5 (strict cone) A set S ⊆ R[X] is a strict cone if it satisfies the following
closure properties: 1) f, g ∈ S implies f + g ∈ S; 2) f, g ∈ S implies f g ∈ S; and 3)
r ∈ S for any positive real r ∈ R>0 . For a subset A of R[X], we write SC(A) for the
smallest strict cone that includes A.
Lemma 3.6 Let x ∈ Rk and gj ∈ R[X]. If x ∈ Jg1 > 0, . . . , gt > 0K, then g(x) > 0
for all g ∈ SC(g1 , . . . , gt ).                                                        t
                                                                                         u
    We can now formulate adaptation of Positivstellensatz. Its proof is in Appendix A.3.
Theorem 3.7 (Positivstellensatz for SAS< ) Let T be the SAS< in (8). It is infeasi-
ble (i.e. JT K = ∅) if and only if there exist f ∈ C(f1 , . . . , fs , g1 , . . . , gt ), g ∈
SC(g1 , . . . , gt ) and h ∈ I(h1 , . . . , hu ) such that f + g + h = 0.                   t
                                                                                            u
From this we derive the following adaptation of Thm. 2.7 that allows to synthesize sharp
interpolants. The idea is as follows. In Thm. 2.7, the constants 1 (in (3)) and 1/2 (in (4))
are there to enforce strict positivity. This is a useful trick but sometimes too “dull”: one
can get rid of these constants and still make the proof of Thm. 2.7 work, for example
when g(x) happens to belong to M(g1 , . . . , gt ) instead of M(g1 , . . . , gt , g10 , . . . , gt0 0 ).

Theorem 3.8 (disjointness certificate from strict cones) Let T and T 0 be the follow-
ing SAS< ’s, where X denotes the variables that occur in both of T , T 0 .
                                                                                                           
           f1 (X, Y ) ≥ 0 , . . . , fs (X, Y ) ≥ 0 ,        g1 (X, Y ) > 0 , . . . , gt (X, Y ) > 0 ,
T =                                                                                                      ,
           h1 (X, Y ) = 0 , . . . , hu (X, Y ) = 0
           f10 (X, Z) ≥ 0 , . . . , fs0 0 (X, Z) ≥ 0 ,      g10 (X, Z) > 0 , . . . , gt0 0 (X, Z) > 0 ,
                                                                                                       
T0 =                                                                                                      .
           h01 (X, Z) = 0 , . . . , h0u0 (X, Z) = 0
                                                                                                            (9)

    Assume there exist

       f ∈ C(f1 , . . . , fs , g1 , . . . , gt ) , f 0 ∈ C(f10 , . . . , fs0 0 , g10 , . . . , gt0 0 ) ,
       g ∈ SC(g1 , . . . , gt ) , h ∈ I(h1 , . . . , hu ) , and h0 ∈ I(h01 , . . . , h0u0 )
           such that f + f 0 + g + h + h0 = 0 .                                                            (10)

Then the SAS< ’s T and T 0 are disjoint. Moreover the SAS<

                                       S := (f + g + h > 0)                                                (11)

satisfies the conditions of an interpolant of T and T 0 (Def. 2.6), except for Cond. 3. (the
common variable condition).                                                                t
                                                                                           u

    The proof is like for Thm. 2.7. We also have the following symmetric variant.
Theorem 3.9 Assume the conditions of Thm. 3.8, but let us now require g ∈
SC(g10 , . . . , gt0 0 ) (instead of g ∈ SC(g1 , . . . , gt )). Then S = (f + h ≥ 0) is an in-
terpolant of T and T 0 (except for the common variable condition).                          t
                                                                                            u
12

Algorithm 2 Our interpolation algorithm based on Thm. 3.8. Here 2 = {0, 1} and
σ(b) = {(k1 , . . . , kt ) ∈ Nt | k1 + · · · + kt ≤ b + 1}
 1: input: SAS< ’s T , T 0 in (9), and b ∈ N (the maximum degree)
 2: output: either an interpolant S of T and T 0 , or FAIL
                                                       −
                                                       → − → −  → →
 3: Solve (an extension of) PDiophSOS to find (−   →
                                                   α , α0 , β , β 0 , −
                                                                      γ ). Here:
                                                                                                                0         0
        – αij ∈ C(∅)≤b (for i ∈ 2s , j ∈ 2t ) and αi0 0 ,j 0 ∈ C(∅)≤b (for i0 ∈ 2s , j 0 ∈ 2t ) are
          SOSs,
        – βj ∈ R[X]≤b (for j ∈ [1, u]) and βj0 0 ∈ R[X]≤b (for j 0 ∈ [1, u0 ]) are polynomials,
        – and γk ∈ R≥0 (for k ∈ σ(b)) are nonnegative real numbers,

     that are subject to the constraints
               P                      i1       is j1             jt
                  i∈2s , j∈2t αij f1 · · · fs g1 · · · gt
                                                                0
                                         0
                                                   0
                                                0 i1           i 0 j0               j 00
                                                     · · · f 0 ss0 g 0 11 · · · g 0 t0t
                   P
               +     i0 ∈2s , j 0 ∈2t αi0 j 0 f1
                           0         0                                                                                        (12)
                   P                k1        kt        Pu                         Pu0           0    0
               +     k∈σ(b) γk g1 · · · gt         +        j=1 βj hj +                  j 0 =1 βj 0 hj 0   =       0 ,
               P
                  k∈σ(b) γk ≥ 1 ,          and                                                                                (13)
                 some equality constraints that forces the common variable condition.                                         (14)
               −
               → − → −  → →
    (SuchP(−
           →
           α , α0 , β , β 0 , −
                              γ ) may not be found, in which   P case return FAIL)
 4: f := i∈2s , j∈2t αij f1i1 · · · fsis g1j1 · · · gtjt ; g := k∈σ(b) γk g1k1 · · · gtkt ; h := uj=1 βj hj
                                                                                                P

 5: return S := (f + g + h > 0)



Example 3.10 Let us apply Thm. 3.8 to T = (−y > 0) and T 0 = (y − x ≥ 0, y + x ≥
0) (these are only barely disjoint). There exists a disjointness certificate f, f 0 , g, h, h0 :
indeed, we can take f = 0 ∈ C(−y), f 0 = 2y = (y − x) + (y + x) ∈ C(y − x, y + x),
g = 2(−y) ∈ SC(−y), and h = h0 = 0 ∈ I(∅); for these we have f +f 0 +g +h+h0 =
0. This way an interpolant S = (f + g + h > 0) = (−2y > 0) is derived.
Remark 3.11 Our use of strict cones allows to use a polynomial g in (11). This is in
contrast with g 2 in (4) and yields an interpolant of a potentially smaller degree.
    We derive an interpolation algorithm from Thm. 3.8; see Algorithm 2. An algorithm
based on Thm. 3.9 can be derived similarly, too.
    Algorithm 2 reduces search for a disjointness certificate f, f 0 , g, h, h0 (from Thm. 3.8)
to a problem similar to PDiophSOS (Line 3). Unlike the original definition of PDiophSOS
(Def. 2.8), here we impose additional constraints (13–14) other than the equality (12)
that comes from (10). It turns out that, much like PDiophSOS allows relaxation to SDP
problems [8, 24, 25], the problem in Line 3 can also be reduced to an SDP problem.
                                                   P        k1       kt
    The constraint (13) is there to force g = k∈bt γk gP    1 · · · gt (see (4)) to belong to
the strict cone SC(g1 , . . . , gt ). A natural requirement k∈bt γk > 0 for that purpose
does
P not allow encodingP       to an SDP constraint so we do not use it. Our relaxation from
   k∈b t γ k > 0 to   k∈b γk ≥ 1 is inspired by [31]; it does not lead to loss of generality
                          t

in our current task of finding polynomial certificates.
    The constraints (14) are extracted in the following straightforward manner: we look
at the coefficient of each monomial in f + g + h (see Line 5); and for each monomial
                                                                                          13

that involves variables other than X we require the coefficient to be equal to 0. The
constraint is linear in the SDP variables, that we can roughly consider as the coefficients
                            →
                            − → − →  − −
of the monomials in →  −α , α0 , β , β 0 , →
                                           γ.
    Derivation of Algorithm 2 from Thm. 3.9 also relies on the following analogue of
Lem. 2.9. Its proof is in Appendix A.4.


   P 3.12 An arbitrary element of the strict cone SC(f1 , . . . , fs ) can be expressed
Lemma
as i∈Ns αi f1i1 · · · fsis , where αi ∈ R≥0 are nonnegative reals (for i ∈ Ns ) such that:
there exists i such that αi > 0; and αi 6= 0 for only finitely many i.                  t
                                                                                        u

     To summarize: our analysis of the framework of [8] has led to a new algorithm (Al-
gorithm 2) that allows “sharp” interpolation of barely disjoint SASs. This algorithm is
based on strict inequalities (>) instead of disequalities (6=); we introduced the corre-
sponding notion of strict cone. The algorithm allows solution by numeric SDP solvers.
Moreover we observe that the common variable condition—that seems to be only par-
tially addressed in [8]—allows encoding as SDP constraints.
     We conclude by noting that our algorithm (Algorithm 2) generalizes Algorithm 1
from [8]. More specifically, given SAS6= ’s T and T 0 that are disjoint, if Algorithm 1
finds an interpolant, then Algorithm 2 also finds an interpolant after suitable translation
of T and T 0 to SAS< ’s. See Appendix C.


4     Implementation: Numerical Errors and Rounding

Our implementation, that we named SSI NT (Sharp and Simple Interpolants), is essen-
tially Algorithm 2; in it we use an SDP solver to solve Line 3. Specifically we use the
SDP solver SDPT3 [35] via YALMIP as the backend.
     The biggest issue in the course of implementation is numerical errors—they are
inevitable due to (numerical) interior point methods that underlie most state-of-the-art
SDP solvers. For one thing, we often get incorrect interpolants due to numerical errors
(Example 1.3). For another, in the context of program verification simpler interpolants
are often more useful, reflecting simplicity of human insights (see §1). Numerical solu-
tions, on the contrary, do not very often provide humans with clear-cut understanding.
     In our implementation we cope with numerical errors by rounding numbers. More
specifically we round ratios x1 : x2 : · · · : xn because our goal is to simplify a
polynomial inequality f + g + h > 0 (imagine the ratio between coefficients). For
this purpose we employ an extension of continued fraction expansion, a procedure used
e.g. for the purpose of Diophantine approximation [19] (i.e. finding the best rational
approximation k1 /k2 of a given real r). Concretely, our extension takes a ratio x1 : · · · :
xn of natural numbers (and a parameter d that we call depth), and returns a simplified
ratio y1 : · · · : yn .
     Overall the workflow of our tool SSI NT is as in Fig. 1.

    – We first run Algorithm 2. Its output—more precisely the solution of the SDP prob-
      lem in Line 3—may not yield an interpolant, due to numerical errors. The output is
      therefore called a candidate v.
14

                            original                rounded
          0                candidate               candidate
      T ,T ,b                                          vd                      pass
                / Alg. 2       v     / rounding              /   validation             / interpolant
                (SDP)       d := 1         O
                                                                       fail    yes
                                                      no
                                                                 v d = v?                  / FAIL
                                                  d := d + 1

                              Fig. 1. The workflow of our tool SSI NT


 – We then round the candidate v iteratively, starting with the depth d = 1 (the coars-
   est approximation that yields the simplest candidate v 1 ) and incrementing the depth
   d. The bigger the depth d is, the less simple and the closer to the original v the
   rounded candidate v d becomes.
 – In each iteration we check if the candidate v d yields a valid interpolant. This vali-
   dation phase is conducted purely symbolically, ensuring soundness of our tool.
 – Our rounding algorithm eventually converges and we have v d = v for a sufficiently
   large d (Lem. 4.1). In case we do not succeed by then we return FAIL.
In other words, we try candidates v 1 , v 2 , . . . , from simpler to more complex, until we
obtain a symbolically certified interpolant (or fail). This is the rounding and validation
workflow that we adopted from [12].
     Our workflow involves another parameter c ∈ N that we call precision. It is used in
an empirical implementation trick that we apply to the original candidate v: we round
it off to c decimal places.
     The tool SSI NT is implemented in OCaml. When run with SAS< ’s T , T 0 (and a
parameter b ∈ N for the maximum degree, see Algorithm 2) as input, the tool generates
MATLAB code that conducts the workflow in Fig. 1. The latter relies on the SDP solver
SDPT3 [35] via YALMIP as the backend.
                                                                                d        CFE(x, d)
                                                                                1         (15, 1, 6)
4.1    Rounding                                                                 2        (31, 2, 13)
                                                                                3       (172, 11, 71)
Continued fraction expansion is a well-known method for rounding                4       (204, 13, 84)
                                                                                5    (11515, 735, 4747)
a real number to a rational; it is known to satisfy an optimality con-          6 (81389, 5195, 33552)
                                                                                7 (174293, 11125, 71851)
dition called Diophantine approximation. One can think of it as a               8 (174293, 11125, 71851)
procedure that simplifies ratios x1 : x2 of two numbers.                        x (871465, 55625, 359255)
     In our tool we use our extension of the procedure that simplifies ratios x1 : · · · : xn .
It is the algorithm CFE in Algorithm 3. An example is in the above table, where x =
(871465, 55625, 359255). One sees that the ratio gets more complicated as the depth d
becomes bigger. For the depth d = 7, 8 the output is equivalent to the input x.
     Our algorithm CFE enjoys the following pleasant properties. Their proofs are in
Appendix A.5.
Lemma 4.1 1. (Convergence) The output CFE(x, d) stabilizes for sufficiently large
    d; moreover the limit coincides with the input ratio x. That is: for each x there
    exists M such that CFE(x, M ) = CFE(x, M + 1) = · · · = x (as ratios).
 2. (Well-definedness) CFE respects equivalence of ratios. That is, if x, x0 ∈ Nn repre-
    sent the same ratio, then CFE(x, d) = CFE(x0 , d) (as ratios) for each d.         t
                                                                                      u
                                                                                                     15

Algorithm 3 Extended continued fraction expansion CFE
1: input: x = (x1 , . . . , xn ) ∈ Nn (at least one of x1 , . . . , xn is nonzero), and depth d ∈ N>0
2: Pick p so that xp is the smallest among the nonzero elements in x1 , . . . , xn
   (say the smallest among such p’s)
3: a := (bx1 /xp c, . . . , bxn /xp c)
4: if d = 1 then
5:    y := a/ gcd(a)
6:    return y
7: else
                                           p−1            p          p+1
                                            ∨             ∨           ∨
8:       r := (x1 − a1 xp , . . . , xp−1 − ap−1 xp , xp , xp+1 − ap+1 xp , . . . , xn − an xp )
9:       r0 := CFE(r, d − 1)              {a recursive call}
                                          p−1         p         p+1
                                            ∨        ∨            ∨
10:      y := (a1 rp + r1 , . . . , ap−1 rp + rp−1 , rp , ap+1 rp0 + rp+1
                   0    0                 0    0       0              0
                                                                          , . . . , an rp0 + rn0 )
11:   return y/ gcd(y)
12: end if



     The algorithm CFE takes a positive ratio x as input. In the workflow in Fig. 1 CFE
is applied to ratios with both positive and negative numbers; we deal with such input by
first taking absolute values and later adjusting signs.


4.2     Validation

Potential unsoundness of verification methods due to numerical errors has been identi-
fied as a major challenge (see e.g. [2,12,17,26,27,29]). In our tool we enforce soundness
(i.e. that the output is indeed an interpolant) by the validation phase in Fig. 1.
     There the candidate v d in question is fed back to the constraints in (the SDP problem
that is solved in) Algorithm 2,6 and we check the constraints are satisfied. The check
must be symbolic. For equality constraints such symbolic check is easy. For semidefi-
niteness constraints, we rely on the following well-known fact: a symmetric real matrix
M is positive semidefinite if and only if all the principal minors of M are nonnegative.
This characterization allows us to check semidefiniteness using only addition and mul-
tiplication. We find no computation in our validation phase to be overly expensive. This
is in contrast with QE-based validation methods employed e.g. in [7]: while symbolic
and exact, the CAD algorithm for QE is known to be limited in scalability.


5      Experiments

We now present some experiment results. In the first part we present some simple ge-
ometric examples that call for “sharp” interpolants; in the second we discuss some
program verification scenarios. These examples demonstrate our tool’s capability of
 6                                              P
                P 2 we introduced the constraint k∈bt γk ≥ 1 in (13) as a relaxation of a natural
     In Algorithm
     constraint k∈bt γP k > 0; see §3.2. In the validation phase of our implementation we wind
     back the relaxation k∈bt γk ≥ 1 to the original constraint with > 0.
16

producing simple and sharp interpolants, together the benefits of such interpolants in
program verification techniques.
    The experiments were done on Apple MacBook Pro with 2.7 GHz Intel Core i5
CPU and 16 GB memory. As we described in §4, our tool SSI NT consists of OCaml
code that generates MATLAB code; the latter runs the workflow in Fig. 1. Running
the OCaml code finishes in milliseconds; running the resulting MATLAB code takes
longer, typically for seconds. The execution time shown here is the average of 10 runs.
    Our tool has two parameters: the maximum degree b and precision c (§4). In all our
examples the common variable condition (in Def. 2.6) is successfully enforced.
Geometric Examples Table 1 summarizes the performance of our tool on interpola-
tion problems. For the input 6, we tried parameters (b, c) = (1, 1), (1, 2), . . . , (1, 5) and
(2, 5) but all failed, leading to FAIL in Fig. 1. The input 9 contains disjunction, which
is not allowed in SAS< ’s. It is dealt W  V using the technique described in [8, §3.1]: an
                                        with
interpolant of T and T 0 is given by i j Sij , where Sij is an interpolant of each pair
of disjuncts Ti and Tj0 of T and T 0 , respectively.
Program Verification Example I: Infeasibility Checking Consider the code in List-
ing 1.1; this is from [8, §7]. We shall solve Subproblem 1 in [8, §7]: if the prop-
erty (xa) + 2(ya) ≥ 0 holds at Line 5, then it holds too after the execution along
5 → 6 → 7 → 8 → 9 → 13 → 14. The execution is expressed as the SAS T in Fig. 3.
Then our goal is to show that the negation T 0 = ((xa1 ) + 2(ya1 ) < 0) of the desired
property is disjoint from T .
                                                        
    Our tool yields S = 8 − 14(ya1 ) − 7(xa1 ) ≥ 0 as an interpolant of these T and
T 0 (in 14.1 seconds, with parameters b = 0, c = 3 and depth d = 11). The interpolant
witnesses disjointness. Our interpolant is far simpler than the interpolant given in [8].7
    Here the simplicity of our interpolant brings robustness as its benefit. Consider the
other path 5 → · · · → 8 → 11 → 13 → 14 of execution from Line 5 to 14, and let T0 be
the SAS that expresses the execution. It turns out that our interpolant S in the above is at
the same time an interpolant of T0 and T 0 . Thus our algorithm has managed, aiming at
simpler interpolants, to automatically discover −14(ya) − 7(xa) (that is, (xa) + 2(ya))
as a value that is significant regardless of the choice made in Line 8.
Program Verification Example II: CEGAR This is the example we discussed in
Example 1.4. Here we provide further details, aiming at readers familiar with CEGAR.
    One of the most important applications of interpolation in verification is in counterexample-
guided abstraction refinement (CEGAR) [4]. There an interpolant S is used as (a candi-
date for) the “essential reason” to distinguish positive examples T from negative coun-
terexamples T 0 .
    As an example let us verify Listing 1.1 by CEGAR. Starting from the empty set of
abstraction predicates, CEGAR would find the path p1 := (1 → 2 → 3 → 4 → 16) as

 7
     An interpolant 716.77 + 1326.74(ya) + 1.33(ya)2 + 433.90(ya)3 + 668.16(xa) −
     155.86(xa)(ya) + 317.29(xa)(ya)2 + 222.00(xa)2 + 592.39(xa)2 (ya) + 271.11(xa)3 > 0
     is given in [8]. We note that, to show disjointness of T and T 0 , an interpolant of any splitting
     of T ∪ T 0 would suffice. It is not specified [8] which splitting they used.
                                                                                                                                        17

     Table 1. Experiment results. T and T 0 are inputs, and S is our output (see Fig. 2 too). The “time”
     column shows the execution time (in seconds) of the generated MATLAB code, b and c show the
     successful choice of parameters, and d is the depth for which the workflow in Fig. 1 terminated.

                      T                 T0                                         S                                  time [s] b c d
            1 y > x, x > −y            0≥y                                      4y > 0                                  2.19 0 5 1
            2       y≤0               y > x2                                   −2y ≥ 0                                  5.68 2 3 1
            3 y > x, x > −y      y ≤ x, x ≤ −y                                  4y > 0                                  2.67 0 5 1
            4 y > x, x > −y         y ≤ −x2                                  8y + 4x2 > 0                               5.09 2 1 1
            5      y ≤ −1          x + y2 < 1
                                    2
                                                                        34y 2 − 68y − 102 ≥ 0                           7.58 2 5 3
            6 x2 + (y − 1)2 ≤ 1 x2 + (y − 2)2 > 4                                FAIL                                   14.0 2 5 8
                                                                    18x2 y − 14x2 y 2 − 144y
            7 x2 + (y + 1)2 ≤ 1 x2 + (y − 1)2 < 1                                                                      6.45 2 2 2
                                                                    +28y 2 − 7x4 + 18y 3 − 7y 4 ≥ 0
            8      x ≥ z2           x < −y 2                                    2x ≥ 0                                 7.67 2 3 1
              (y ≥ (x − 1) ) ∨ (y < −(x − 1)2 ) ∨
                          2
                                                                  ((586x + 293y + 119 > 0) ∧ (333y ≥ 0)) ∨
            9                                                                                                          43.7 2 3 3
              (y > (x + 1)2 )  (y ≤ −(x + 1)2 )                   ((333y > 0) ∧ (374y − 748x − 117 ≥ 0))




             Input 1                Input 2                       Input 3                         Input 4                     Input 5




                                                   � ≥ ��                         � < - ��                    �� ≥�




                                  Input 8, T                   Input 8, T 0                      Input 8, S                   Input 9
             Input 7

     Fig. 2. Interpolants from Table 1. The blue, orange and green areas are for T , T 0 , S, respectively.


     Listing 1.1. Code 1.3 of [8]                                         Listing 1.2. Constant Acceleration
 1   real x ,y;                                1            real x ,v;
 2   r e a l xa = 0 ;                          2            (x , v) = (0 , 0);
 3   r e a l ya = 0 ;                          3            while ( nondet ( ) ) {
 4   while ( nondet ( ) ) {                    4              ( x , v ) = ( x+2∗v , v + 2 ) ;
 5     x = xa + 2∗ ya ;                        5            }
 6     y = −2∗xa + ya ;                        6              a s s e r t ( x >= 0 ) ;
 7     x ++;
 8     i f ( nondet ( ) ) {
 9       y = y + x;
                                                                        (xa) + 2(ya) ≥ 0, x = (xa) + 2(ya),
                                                                                                           
10     }else{
11       y = y − x;                                                    y = −2(xa) + (ya), x1 = x + 1,
                                                                   T =
                                                                                                            
12     }                                                                y = x + y, (xa ) = x − 2y ,
                                                                              1              1          1
                                                                                                            
                                                                                                                 1        1
13     xa = x − 2∗y ;                                                        (ya1 ) = 2x1 + y1
14     ya = 2∗x + y ;                                       Fig. 3. The SAS for an execution of the code in Listing 1.1
15   }
16   a s s e r t ( xa + 2∗ ya >= 0 ) ;
18

a counterexample.8 This counterexample path turns out to be spurious: let T := (xa =
0, ya = 0) express the path and T 0 := ((xa) + 2(ya) < 0) express the negation of the
assertion; our tool SSI NT yields 189346(xa)+378692(ya) ≥ 0 (i.e. (xa)+2(ya) ≥ 0)
as an interpolant, proving their disjointness. For the interpolation the tool SSI NT took
4.32 seconds; we used the parameters b = 0 and c = 5.
    Consequently we add (xa) + 2(ya) ≥ 0 as a new abstraction predicate and run the
CEGAR loop again. This second run succeeds, since (xa) + 2(ya) ≥ 0 turns out to be
a suitable invariant for the loop in Line 4. We conclude safety of Listing 1.1.
    We tried to do the same with the tool aiSat [6, 8] instead of our SSI NT. It does not
succeed in interpolating T = (xa = 0, ya = 0) and T 0 = ((xa) + 2(ya) < 0), since
sharpness is required here (Prop. 3.3). As a workaround we tried strengthening T 0 =
((xa) + 2(ya) < 0) into T00 = ((xa) + 2(ya) ≤ −10−7 ); aiSat then succeeded and
yielded an interpolant S = (137.3430+5493721088(ya)+2746860544(xa) > 0). This
predicate, however, cannot exclude the spurious path p1 because S and the negation
(xa) + 2(ya) < 0 of the assertion are satisfiable with xa = 0 and ya = −1.25 × 10−8 .
Program Verification Example III: CEGAR Here is another CEGAR example.
Consider the code in Listing 1.2 that models movement with constant acceleration. We
initially have the empty set of abstraction predicates. After the first run of the CEGAR
loop we would obtain a counterexample path p1 := (1 → 2 → 3 → 6); note that, since
there are no predicates yet, x can be anything and thus the assertion may fail.
     We let T1 := (x = 0, v = 0) express the counterexample p1 and T10 := (x < 0)
express the negation of the assertion. For these T1 , T10 our tool SSI NT synthesizes S1 :=
(2x ≥ 0) as their interpolant (in 1.92 seconds, with b = 0, c = 5, and d = 1).
     Thus we add 2x ≥ 0 as an abstraction predicate and run the CEGAR loop again. We
would then find the path p2 := (1 → 2 → 3 → 4 → 5 → 6) as a counterexample—
note that the previous counterexample p1 is successfully excluded by the new predicate
2x ≥ 0. Much like before, we let T2 := (v1 = 0) express an initial segment of the
path p2 and let T20 := (x1 = 0, v2 = v1 + 2, x2 = x1 + 2v1 , x2 < 0) express the rest
of the path p2 (together with the negation of the assertion), and we shall look for their
interpolant S2 as the witness of infeasibility of the path p2 . SSI NT succeeds, yielding
S2 := (8v1 ≥ 0) in 2.87 seconds with b = 0, c = 5, d = 1.
     In the third run of the CEGAR loop we use both 2x ≥ 0 and 8v ≥ 0 (from S1 , S2 ) as
abstraction predicates. The proof then succeeds and we conclude safety of Listing 1.2.
     We did not succeed in doing the same with aiSat. In the first CEGAR loop an
interpolant of T1 and T10 cannot be computed because it has to be sharp. As we did
in the previous example we could strengthen T10 to T100 := (x ≤ 10−7 ) and use an
interpolant of T1 and T100 instead for the next iteration. aiSat generated an interpolant
3790.1050 + 75802091520.0000x > 0 of T1 and T100 ; however this fails to exclude the
spurious counterexample path p1 .
     Overall this example demonstrates that sharpness of interpolants can be a decisive
issue in their application in program verification.
 8
     Here we use a path-based CEGAR workflow that uses an execution path as a counterexample.
     Since we do not have any abstraction predicates, xa and ya can be any integer; in this case the
     assertion in Line 16 can potentially fail.
                                                                                                19

Acknowledgments Thanks are due to Eugenia Sironi, Gidon Ernst and the anonymous
referees for their useful comments. T.O., K. Kido and I.H. are supported by JST ERATO
HASUO Metamathematics for Systems Design Project (No. JPMJER1603), and JSPS
Grants-in-Aid No. 15KT0012 & 15K11984. K. Kojima is supported by JST CREST.
K.S. is supported by JST PRESTO No. JPMJPR15E5 and JSPS Grants-in-Aid No.
15KT0012. K. Kido is supported by JSPS Grant-in-Aid for JSPS Research Fellows
No. 15J05580.


References
 1. Anai, H., Parrilo, P.A.: Convex quantifier elimination for semidefinite programming. In:
    Proceedings of the International Workshop on Computer Algebra in Scientific Computing,
    CASC (2003)
 2. Besson, F.: Fast reflexive arithmetic tactics the linear case and beyond. In: Altenkirch,
    T., McBride, C. (eds.) Types for Proofs and Programs, International Workshop, TYPES
    2006, Nottingham, UK, April 18-21, 2006, Revised Selected Papers. Lecture Notes in Com-
    puter Science, vol. 4502, pp. 48–62. Springer (2006), https://doi.org/10.1007/
    978-3-540-74464-1_4
 3. Bochnak, J., Coste, M., Roy, M.F.: Real algebraic geometry. Springer (1999)
 4. Clarke, E.M., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided abstraction
    refinement for symbolic model checking. J. ACM 50(5), 752–794 (2003), http://doi.
    acm.org/10.1145/876638.876643
 5. Colón, M., Sankaranarayanan, S., Sipma, H.: Linear invariant generation using non-linear
    constraint solving. In: Hunt Jr. and Somenzi [14], pp. 420–432
 6. Dai, L.: The tool aiSat, github.com/djuanbei/aiSat, cloned on January 17th,
    2017.
 7. Dai, L., Gan, T., Xia, B., Zhan, N.: Barrier certificates revisited. J. Symb. Comput. 80, 62–86
    (2017), http://dx.doi.org/10.1016/j.jsc.2016.07.010
 8. Dai, L., Xia, B., Zhan, N.: Generating non-linear interpolants by semidefinite programming.
    In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification - 25th International Confer-
    ence, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013. Proceedings. Lecture Notes in
    Computer Science, vol. 8044, pp. 364–380. Springer (2013), http://dx.doi.org/10.
    1007/978-3-642-39799-8_25
 9. Gan, T., Dai, L., Xia, B., Zhan, N., Kapur, D., Chen, M.: Interpolant synthesis for quadratic
    polynomial inequalities and combination with EUF. In: Olivetti, N., Tiwari, A. (eds.) Auto-
    mated Reasoning - 8th International Joint Conference, IJCAR 2016, Coimbra, Portugal, June
    27 - July 2, 2016, Proceedings. Lecture Notes in Computer Science, vol. 9706, pp. 195–212.
    Springer (2016), https://doi.org/10.1007/978-3-319-40229-1_14
10. Gao, S., Zufferey, D.: Interpolants in nonlinear theories over the reals. In: Chechik, M.,
    Raskin, J. (eds.) Tools and Algorithms for the Construction and Analysis of Systems - 22nd
    International Conference, TACAS 2016, Held as Part of the European Joint Conferences
    on Theory and Practice of Software, ETAPS 2016, Eindhoven, The Netherlands, April 2-8,
    2016, Proceedings. Lecture Notes in Computer Science, vol. 9636, pp. 625–641. Springer
    (2016), https://doi.org/10.1007/978-3-662-49674-9_41
11. Gurfinkel, A., Rollini, S.F., Sharygina, N.: Interpolation properties and sat-based model
    checking. In: Hung, D.V., Ogawa, M. (eds.) Automated Technology for Verification and
    Analysis - 11th International Symposium, ATVA 2013, Hanoi, Vietnam, October 15-18,
    2013. Proceedings. Lecture Notes in Computer Science, vol. 8172, pp. 255–271. Springer
    (2013)
20

12. Harrison, J.: Verifying nonlinear real formulas via sums of squares. In: Schneider, K., Brandt,
    J. (eds.) Theorem Proving in Higher Order Logics, 20th International Conference, TPHOLs
    2007, Kaiserslautern, Germany, September 10-13, 2007, Proceedings. Lecture Notes in Com-
    puter Science, vol. 4732, pp. 102–118. Springer (2007), https://doi.org/10.1007/
    978-3-540-74591-4_9
13. Henzinger, T.A., Jhala, R., Majumdar, R., McMillan, K.L.: Abstractions from proofs. In:
    Jones, N.D., Leroy, X. (eds.) Proceedings of the 31st ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages, POPL 2004, Venice, Italy, January 14-16, 2004.
    pp. 232–244. ACM (2004), http://dl.acm.org/citation.cfm?id=964001
14. Hunt Jr., W.A., Somenzi, F. (eds.): Computer Aided Verification, 15th International Con-
    ference, CAV 2003, Boulder, CO, USA, July 8-12, 2003, Proceedings, Lecture Notes in
    Computer Science, vol. 2725. Springer (2003)
15. Jhala, R., McMillan, K.L.: Interpolant-based transition relation approximation. In: Etessami,
    K., Rajamani, S.K. (eds.) Computer Aided Verification, 17th International Conference, CAV
    2005, Edinburgh, Scotland, UK, July 6-10, 2005, Proceedings. Lecture Notes in Computer
    Science, vol. 3576, pp. 39–51. Springer (2005)
16. Jhala, R., McMillan, K.L.: A practical and complete approach to predicate refinement. In:
    Hermanns, H., Palsberg, J. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems, 12th International Conference, TACAS 2006 Held as Part of the Joint European
    Conferences on Theory and Practice of Software, ETAPS 2006, Vienna, Austria, March 25
    - April 2, 2006, Proceedings. Lecture Notes in Computer Science, vol. 3920, pp. 459–473.
    Springer (2006), https://doi.org/10.1007/11691372_33
17. Kaltofen, E., Li, B., Yang, Z., Zhi, L.: Exact certification of global optimality of approximate
    factorizations via rationalizing sums-of-squares with floating point scalars. In: Sendra, J.R.,
    González-Vega, L. (eds.) Symbolic and Algebraic Computation, International Symposium,
    ISSAC 2008, Linz/Hagenberg, Austria, July 20-23, 2008, Proceedings. pp. 155–164. ACM
    (2008), http://doi.acm.org/10.1145/1390768.1390792
18. Kupferschmid, S., Becker, B.: Craig interpolation in the presence of non-linear constraints.
    In: Fahrenberg, U., Tripakis, S. (eds.) Formal Modeling and Analysis of Timed Systems -
    9th International Conference, FORMATS 2011, Aalborg, Denmark, September 21-23, 2011.
    Proceedings. Lecture Notes in Computer Science, vol. 6919, pp. 240–255. Springer (2011)
19. Lang, S.: Introduction to Diophantine Approximations. Springer books on elementary math-
    ematics, Springer (1995), http://dx.doi.org/10.1007/978-1-4612-4220-8
20. Lin, W., Wu, M., Yang, Z., Zeng, Z.: Proving total correctness and generating
    preconditions for loop programs via symbolic-numeric computation methods. Fron-
    tiers of Computer Science 8(2), 192–202 (2014), http://dx.doi.org/10.1007/
    s11704-014-3150-6
21. McMillan, K.L.: Interpolation and sat-based model checking. In: Hunt Jr. and Somenzi [14],
    pp. 1–13
22. McMillan, K.L.: Applications of craig interpolants in model checking. In: Halbwachs, N.,
    Zuck, L.D. (eds.) Tools and Algorithms for the Construction and Analysis of Systems,
    11th International Conference, TACAS 2005, Held as Part of the Joint European Confer-
    ences on Theory and Practice of Software, ETAPS 2005, Edinburgh, UK, April 4-8, 2005,
    Proceedings. Lecture Notes in Computer Science, vol. 3440, pp. 1–12. Springer (2005),
    http://dx.doi.org/10.1007/978-3-540-31980-1_1
23. McMillan, K.L.: Lazy abstraction with interpolants. In: Ball, T., Jones, R.B. (eds.) Computer
    Aided Verification, 18th International Conference, CAV 2006, Seattle, WA, USA, August 17-
    20, 2006, Proceedings. Lecture Notes in Computer Science, vol. 4144, pp. 123–136. Springer
    (2006), https://doi.org/10.1007/11817963_14
24. Parrilo, P.: Structured semidefinite programs and semialgebraic geometry methods in robust-
    ness and optimization. Ph.D. thesis, California Inst. of Tech. (2000)
                                                                                               21

25. Parrilo, P.A.: Semidefinite programming relaxations for semialgebraic problems. Math-
    ematical Programming 96(2), 293–320 (2003), http://dx.doi.org/10.1007/
    s10107-003-0387-5
26. Peyrl, H., Parrilo, P.A.: Computing sum of squares decompositions with rational coefficients.
    Theor. Comput. Sci. 409(2), 269–281 (2008), https://doi.org/10.1016/j.tcs.
    2008.09.025
27. Platzer, A., Quesel, J., Rümmer, P.: Real world verification. In: Schmidt, R.A. (ed.) Au-
    tomated Deduction - CADE-22, 22nd International Conference on Automated Deduction,
    Montreal, Canada, August 2-7, 2009. Proceedings. Lecture Notes in Computer Science, vol.
    5663, pp. 485–501. Springer (2009)
28. Putinar, M.: Positive polynomials on compact semi-algebraic sets. Indiana Univ. Math. Journ.
    42(3), 969–984 (1993)
29. Roux, P., Voronin, Y., Sankaranarayanan, S.: Validating numerical semidefinite programming
    solvers for polynomial invariants. In: Rival, X. (ed.) Static Analysis - 23rd International
    Symposium, SAS 2016, Edinburgh, UK, September 8-10, 2016, Proceedings. Lecture Notes
    in Computer Science, vol. 9837, pp. 424–446. Springer (2016), http://dx.doi.org/
    10.1007/978-3-662-53413-7_21
30. Rump, S.: Verification of positive definiteness. BIT Numerical Mathematics 46(2), 433–452
    (2006), http://dx.doi.org/10.1007/s10543-006-0056-1
31. Rybalchenko, A., Sofronie-Stokkermans, V.: Constraint solving for interpolation. In: Cook,
    B., Podelski, A. (eds.) Verification, Model Checking, and Abstract Interpretation, 8th In-
    ternational Conference, VMCAI 2007, Nice, France, January 14-16, 2007, Proceedings.
    Lecture Notes in Computer Science, vol. 4349, pp. 346–362. Springer (2007), https:
    //doi.org/10.1007/978-3-540-69738-1_25
32. Sharma, R., Gupta, S., Hariharan, B., Aiken, A., Liang, P., Nori, A.V.: A data driven approach
    for algebraic loop invariants. In: Felleisen, M., Gardner, P. (eds.) Programming Languages
    and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as Part of the
    European Joint Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy,
    March 16-24, 2013. Proceedings. Lecture Notes in Computer Science, vol. 7792, pp. 574–
    592. Springer (2013), https://doi.org/10.1007/978-3-642-37036-6_31
33. Stengle, G.: A Nullstellensatz and a Positivstellensatz in semialgebraic geometry. Mathema-
    tische Annalen 207(2), 87–97 (1974), http://dx.doi.org/10.1007/BF01362149
34. Terauchi, T.: Explaining the effectiveness of small refinement heuristics in program ver-
    ification with CEGAR. In: Blazy, S., Jensen, T. (eds.) Static Analysis - 22nd Interna-
    tional Symposium, SAS 2015, Saint-Malo, France, September 9-11, 2015, Proceedings.
    Lecture Notes in Computer Science, vol. 9291, pp. 128–144. Springer (2015), https:
    //doi.org/10.1007/978-3-662-48288-9_8
35. Toh, K.C., Todd, M., Tütüncü, R.H.: Sdpt3 – a matlab software package for semidefinite
    programming. OPTIMIZATION METHODS AND SOFTWARE 11, 545–581 (1999)
22

A      Omitted Proofs
A.1     Proof of Lem. 2.9
Definition A.1 (quadratic module) A quadratic module generated by M = (mλ )λ∈Λ ∈
R[X]Λ (Λ is an index set) is the set
                  (                                                      )
                         X           q ∈ C(∅), (qλ )λ∈Λ ∈ C(∅)Λ , and
     QM(M ) := q +            qλ mλ                                        . (15)
                        λ∈Λ
                                     qλ = 0 except for finitely many λ’s

      Lem. 2.9 is an immediate consequence of the following lemma.

Lemma A.2 Let f1 , . . . , fs ∈ R[X]. Then,
                           C(f1 , . . . , fs ) = QM(f1i1 · · · fsis | i ∈ 2s )                      (16)
where i = (i1 , . . . , is ).
Proof. The left-to-right direction is proved by induction on the construction of C(f1 , . . . , fs ).
Let f ∈ C(f1 , . . . , fs ).
 1. Case: f = fλ for some λ = 1, . . . , s.

                      f = fλ = f10 · · · fλ1 · · · fs0 ∈ QM(f1i1 · · · fsis | i ∈ 2s ).             (17)
 2. Case: f = g 2 for some g ∈ R[X].

                                  f = g 2 ∈ QM(f1i1 · · · fsis | i ∈ 2s ).                          (18)

 3. Case: f = g + h for some g, h ∈ C(f1 , . . . , fs ) ∩ QM(f1i1 · · · fsis | i ∈ 2s ). Obvi-
    ous, because QM(f1i1 · · · fsis | i ∈ 2s ) is closed under addition.
 4. Case: f = gh for some g, h ∈ C(f1 , . . . , fs ) ∩ QM(f1i1 · · · fsis | i ∈ 2s ). g and h
    have the form
                         X                              X
                    g=         qi f1i1 · · · fsis , h =    rj f1j1 · · · fsjs ,           (19)
                                 i∈2s                             j∈2s
                                              P
      where qi , rj ∈ C(∅). Let pλ = i+j=λ qi rj ∈ C(∅). Then
                       X X
                 gh =            qi rj f1i1 +j1 · · · fsis +js                                      (20)
                          i∈2s j∈2s
                          X X
                      =                   qi rj f1λ1 · · · fsλs                                     (21)
                          λ∈2s i+j=λ
                          X
                      =          pλ f1λ1 · · · fsλs                                                 (22)
                          λ∈2s
                          X            2bλ1 /2c
                                                                   
                      =           pλ f1            · · · fs2bλs /2c f1λ1 mod 2 · · · fsλs mod 2 .   (23)
                          λ∈2s

                      2bλ /2c         2bλs /2c
      Because pλ f1 1 · · · fs                     ∈ C(∅) for each λ ∈ 2s , we have f = gh ∈
      QM(f1i1 · · · fsis | i ∈ 2s ).
                                                                                            23


P For thei1converse,       let f ∈ QM(f1i1 · · · fsis | i ∈ 2s ). Then f has the form f =
                        is
  i∈2s qi f1 · · · fs where qi ∈ C(∅) ⊆ C(f1 , . . . , fs ). Then f indeed belongs to
C(f1 , . . . , fs ), because cones are closed under addition and multiplication.        t
                                                                                        u


A.2     Proof of Prop. 3.3

We argue by contradiction. Assume that there exist polynomials fe, g, e  h that satisfy the
conditions in the proposition. By the feasibility assumption there exists some r ∈ JT• K∩
JT•0 K. For this r we have fe(r) + e
                                   h(r) ≥ 0 by Lem. 2.3, while by 1 + fe + g 2 + e   h=0
                                       2
we have f (r) + h(r) = −1 − g(r) < 0. Contradiction.
           e       e


A.3     Proof of Thm. 3.7

The “if” direction is easy. Suppose there exist such polynomials f, g, h as required.
Assume r ∈ JT K; then we have f (r) ≥ 0, g(r) > 0, and h(r) = 0 by Lem. 2.3
and 3.6. Thus we have f (r) + g(r) + h(r) > 0, which contradicts with f + g + h = 0.
Therefore JT K = ∅.
    For the “only if” direction we rely on Thm. 2.4, via the translation of SAS< ’s
to SAS6= ’s that we described after Def. 3.4, and use the fact that M(g1 , . . . , gt ) ⊆
SC(g1 , . . . , gt ).                                                                   t
                                                                                        u


A.4     Proof of Lem. 3.12

We introduce a notion similar to quadratic module to represent strict cones.

Definition A.3 (positive module) An positive module generated by M = (mλ )λ∈Λ ∈
R[X]Λ (Λ is an index set) is the set

                                     r ∈ R≥0 , (rλ )λ∈Λ ∈ RΛ
                                                                               
               
                      X                                     ≥0 ,               
                                                                                
  PM(M )    :=    r+       rλ mλ rλ = 0 except for finitely many λ’s, and . (24)
                                                                               
                       λ∈Λ
                                     either rλ > 0 for at least one λ, or r > 0
                                                                               

      Then Lem. 3.12 is an immediate consequence of the following lemma.

Lemma A.4 Let f1 , . . . , fs ∈ R[X]. Then,

                      SC(f1 , . . . , fs ) = PM(f1i1 · · · fsis | i ∈ Ns ).               (25)

Proof. The left-to-right direction is proved by induction on the construction of SC(f1 , . . . , fs ).
Let f ∈ SC(f1 , . . . , fs ).

 1. Case: f = fλ for some λ = 1, . . . , s.

                   f = fλ = f10 · · · fλ1 · · · fs0 ∈ PM(f1i1 · · · fsis | i ∈ Ns ).      (26)
24

 2. Case: f = r for some r ∈ R>0 .

                              f = r ∈ PM(f1i1 · · · fsis | i ∈ Ns ).                        (27)

 3. Case: f = g + h for some g, h ∈ SC(f1 , . . . , fs ) ∩ PM(f1i1 · · · fsis | i ∈ Ns ). Ob-
    vious, because PM(f1i1 . . . fsis | i ∈ Ns ) is closed under addition.
 4. Case: f = gh for some g, h ∈ SC(f1 , . . . , fs ) ∩ PM(f1i1 · · · fsis | i ∈ Ns ). g and
    h have the form of
                         X                             X
                    g=        ri f1i1 · · · fsis , h =      rj0 f1j1 · · · fsjs ,        (28)
                             i∈Ns                                j∈Ns

      where ri , rj0 ∈ R≥0 . Let qλ = i+j=λ ri rj0 . Then obviously there are only finitely
                                       P
      many λ such that qλ > 0. Moreover, there exists λ such that qλ > 0. Indeed, for i
      and j such that ri , rj0 > 0, we have
                                             X
                              qi+j =                   ri0 rj0 0 ≥ ri rj0 > 0.              (29)
                                        i0 +j 0 =i+j

      Therefore,
                                     X X
                             gh =                ri rj0 f1i1 +j1 · · · fsis +js             (30)
                                     i∈Ns j∈Ns
                                     X X
                                 =                  ri rj0 f1i1 +j1 · · · fsis +js          (31)
                                     λ∈Ns i+j=λ
                                     X
                                 =          qλ f1λ1 · · · fsλs                              (32)
                                     λ∈Ns

                                 ∈ PM(f1i1 · · · fsis | i ∈ Ns ).                           (33)

For the converse, let us consider f = r + i ri f1i1 · · · fsis ∈ PM(f1i1 · · · fsis | i ∈
                                               P

Ns ). For each i such that ri > 0, we have ri , f1i1 , . . . , fsis ∈ SC(f1 , . . . , fs ). More-
over, either r > 0 or there exists at least one such i. Therefore we conclude that
f ∈ SC(f1 , . . . , fs ), because strict cones are closed under addition and multiplica-
tion.                                                                                          t
                                                                                               u

A.5    Proof of Lem. 4.1
We first notice that in case where the output of CFE(r, d − 1) in Line 10 equals r, then
we can check that the value of y at Line 11 equals x by a straightforward calculation.
    We can prove the lemma by induction on max{xi | 1 ≤ i ≤ n}. We check several
cases in turn.
 1. In the case where there is only one nonzero element in x, set M = 1. For simplicity,
    we consider the case x = (k, 0, 0). Then p = 1 and a = (1, 0, 0). Therefore if
    d = 1, then y = a = x (as ratios). If d > 1, then r = (k, 0, 0), so by induction on
    d we obtain r0 = r, and thus y = x by the remark above.
                                                                                       25

 2. In the case where there are more than one nonzero elements, and all of them are
    the same, set M = 2. For simplicity, we consider the case x = (k, k, k, 0, 0).
    Then p = 1 and a = (1, 1, 1, 0, 0). If d ≥ M = 2, then else-branch is taken, and
    r = (k, 0, 0, 0, 0). By the previous case, we have r0 = r. Therefore y = x by the
    remark.
 3. In other cases, let r as in Line 9, and M be the depth d for which CFE(r, d) sta-
    bilizes (such M exists by the induction hypothesis). Then for any d ≥ M + 1 we
    have r0 = r, and thus y = x by the remark.

    The second claim is obvious from the construction of the algorithm.


B    Topological and Algebraic Closure

Let us consider the difference between topological closure and algebraic closure, that
is, the difference between JT• K ⊆ Rk (where T• is from Def. 3.1) and JT K ⊆ Rk . Here
( ) refers to the closure with respect to the Euclidean topology of Rk .
     They coincide in many cases but do not always. For example, for T = (x3 − 2x2 +
x ≤ 0, x3 − 2x2 + x 6= 0), we have JT• K = Jx3 − 2x2 + x ≤ 0K = (−∞, 0] ∪ { 1 },
but JT K = (−∞, 0) = (−∞, 0].
     We can show the following inclusion in general.

Proposition B.1 Let A = (f1 .1 0, . . . , fn .n 0) be an SAS6= , where .i ∈ {≥, 6=, =}.
Then

                                     JAK ⊆ JA• K.                                  (34)

Proof. The proof is by induction on n.

 – Base cases: The cases .1 = (=) and .1 = (≥) are easy because f1 is continuous
   and both { 0 } and [0, ∞) are closed in R. For the remaining case where .1 = (6=),
   we have Jf1 6= 0K ⊆ Rk = J()K = JA• K.
 – Step case: Let B = (f1 .1 0, . . . , fn .n 0).

       JAK = JB, fn+1 .n+1 0K
           = JBK ∩ Jfn+1 .n+1 0K
           ⊆ JBK ∩ Jfn+1 .n+1 0K
           ⊆ JB• K ∩ J(fn+1 .n+1 0)• K
                (by the induction hypothesis and arguments similar to the base case)
           = JA• K.                                                                    t
                                                                                       u

It follows that JT K ∩ JT 0 K ⊆ JT• K ∩ JT•0 K. The opposite inclusion fails in general:
for T = (x3 − 2x2 + x ≤ 0, x3 − 2x2 + x 6= 0), T 0 = (x ≥ 0), JT K ∩ JT 0 K =
(−∞, 0) ∩ [0, ∞) = ∅ and JT• K ∩ JT•0 K = ((−∞, 0) ∪ { 1 }) ∩ [0, ∞) = { 1 }.
26

C      Relationship of the Two Algorithms

We show that if Algorithm 1 generates an interpolant for two SAS6= ’s, then Algorithm 2
generates an interpolant for two SAS< ’s that are equivalent to those two SAS6= ’s.

Proposition C.1 Let T and T 0 be the SAS6= ’s in (2). Let U and U 0 be the following
SAS< ’s.

                                                                   g12 (X, Y ) > 0 , . . . , gt2 (X, Y ) > 0 ,
                                                                                                                        
           f1 (X, Y ) ≥ 0 , . . . , fs (X, Y ) ≥ 0 ,
U=                                                                                                                           ,
           h1 (X, Y ) = 0 , . . . , hu (X, Y ) = 0
                                                                      2                               2
           f10 (X, Z) ≥ 0 , . . . , fs0 0 (X, Z) ≥ 0 ,             g 0 1 (X, Z) > 0 , . . . , g 0 t0 (X, Z) > 0 ,
                                                                                                                           
U0 =                                                                                                                             .
           h01 (X, Z) = 0 , . . . , h0u0 (X, Z) = 0
                                                                                                                       (35)

Obviously we have JT K = JUK and JT 0 K = JU 0 K.
     Assume there exist polynomials f, f 0 , g, h, h0 that satisfy the following conditions
(cf. Thm. 2.7).
  – f ∈ C(f1 , . . . , fs ), f 0 ∈ C(f10 , . . . , fs0 0 ), g ∈ M(g1 , . . . , gt , g10 , . . . , gt0 0 ), h ∈ I(h1 , . . . , hu ),
    h0 ∈ I(h01 , . . . , h0u0 ), and
  – 1 + f + f 0 + g 2 + h + h0 = 0.
Then there exist polynomials fe, fe0 , ge, e  h0 that satisfy the following (cf. Thm. 3.8).
                                           h, e
                                                                                  2               2
  – fe ∈ C(f1 , . . . , fs , g12 , . . . , gt2 ), fe0 ∈ C(f10 , . . . , fs0 , g 0 1 , . . . , g 0 t ), ge ∈ SC(g12 , . . . , gt2 ), e
                                                                                                                                    h∈
                           0            0            0
    I(h1 , . . . , hu ), h ∈ I(h1 , . . . , hu0 ) and
                         e
  – fe + fe0 + ge + e  h+e   h0 = 0.

Proof. Set

                  fe = g 2 + f ,          fe0 = f 0 ,       ge = 1 ,        h=h ,
                                                                            e               h0 = h0 .
                                                                                            e                          (36)

The equality fe+fe0 +e    g +e  h+e    h0 = 0 is easy. Because g 2 is an SOS and f ∈ C(f1 , . . . , fs ),
                                                                                   2               2
fe ∈ C(f1 , . . . , fs , g12 , . . . , gt2 ) hold. fe0 ∈ C(f10 , . . . , fs0 , g 0 1 , . . . , g 0 t ) is obvious. By
the definition of strict cone, ge = 1 ∈ SC(g1 , . . . , gt ). e                   h ∈ I(h1 , . . . , hu ), e    h0 ∈
    0           0
I(h1 , . . . , hu0 ) are obvious.                                                                                   t
                                                                                                                    u

    Recall that Algorithm 1 generates an interpolant based on Thm. 2.7, and that Algo-
rithm 2 is based on Thm. 3.8. Therefore by Prop. C.1, if the former succeeds, so does
the latter.
