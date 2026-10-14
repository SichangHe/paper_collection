                                                      A Spectral Proof of Khachiyan’s Ellipsoid Conjecture
                                                                  Zhou Longfei∗           Haijun Zou†            Tianhao Liu‡

                                                                                     September 23, 2026


                                                                                             Abstract
                                                       For a convex body K ⊂ Rn , let w(K) denote the volume of its maximum-volume inscribed
arXiv:2609.28447v1 [math.MG] 23 Sep 2026




                                                   ellipsoid. We prove that every closed halfspace H whose boundary passes through the center
                                                   of the maximizing ellipsoid satisfies
                                                                                                   √
                                                                                                     e
                                                                                      w(K ∩ H) ≤       w(K).
                                                                                                    2
                                                   The constant is optimal uniformly over all dimensions, as witnessed by a family of circular
                                                   cones, thereby establishing Khachiyan’s conjecture.
                                                   The proof converts containment, maximality, and the central-cut condition into algebraic
                                                   constraints on positive definite matrices. Two complementary spectral bounds from a diagonal
                                                   model extend to arbitrary center displacements through a directional rank-one estimate
                                                   for fractional trace powers. Concavity determines their joint optimum. We also derive
                                                   finite-dimensional bounds and a necessary condition for near equality, with self-contained
                                                   supporting proofs and an alternative resolvent argument. An AI language model discovered
                                                   the proof in a human-directed research process. Lean 4 with mathlib verifies the main
                                                   theorem, sharpness, and supporting results (GitHub source).

                                           Keywords: maximum-volume inscribed ellipsoid; Khachiyan’s conjecture; convex body; cutting
                                           plane; fractional trace power.


                                           1       Main result and proof strategy
                                           A hyperplane through the center of a body’s maximum-volume inscribed ellipsoid determines two
                                           closed half-bodies. We prove that the maximum-volume ellipsoid inscribed in either half-body
                                                                    √
                                           has volume at most r∗ = e/2 = 0.8243606353 . . . times that of the original maximizing ellipsoid,
                                           and that this dimension-independent constant is optimal.
                                               To state the result precisely, let K ⊂ Rn be compact and convex with nonempty interior,
                                           and write
                                                                  w(K) = max{vol(E) : E ⊂ K, E is an ellipsoid}.                       (1.1)
                                           The maximizing ellipsoid is unique. Denote it by J(K) and its center by c(K); we use the
                                           customary name John ellipsoid. Existence and uniqueness are proved in section A.
                                           Theorem 1.1. Let n ≥ 1, let K ⊂ Rn be a convex body, and let H be a closed halfspace whose
                                           boundary contains c(K). Then
                                                                                                      √
                                                                                                        e
                                                                        w(K ∩ H) ≤ r∗ w(K),      r∗ =     .                       (1.2)
                                                                                                       2
                                           Moreover, r∗ is the smallest constant for which this inequality holds simultaneously for all
                                           dimensions, convex bodies, and such halfspaces.
                                               ∗
                                               longfei.gabriel.zhou@gmail.com
                                               †
                                               Academy of Mathematics and Systems Science, Chinese Academy of Sciences, Beijing, China; University of
                                           Chinese Academy of Sciences, Beijing, China; zouhaijun24@mails.ucas.ac.cn
                                             ‡
                                               Antai College of Economics and Management, Shanghai Jiao Tong University; tianhao.liu@sjtu.edu.cn


                                                                                                1
    Let H + and H − be the two closed halfspaces determined by the cutting hyperplane. The
theorem bounds w(K ∩ H + ) and w(K ∩ H − ) separately. The functional w is not generally
additive under this decomposition: the identity w(K ∩ H + ) + w(K ∩ H − ) = w(K) does not
hold for arbitrary convex bodies. The proof must account for both center displacement and
changes in the semiaxes of the new maximizing ellipsoids.
    The constant was conjectured by Khachiyan [11], who proved a bound of 0.844 . . .. The
earlier inscribed-ellipsoid method of Tarasov et al. [17] introduced an intermediate-ellipsoid
                                                                                        √
construction, its recursive application, and the cone example with limiting ratio e/2. The
sharp estimate below follows from retaining two complementary constraints supplied by that
construction. A diagonal model makes their relationship explicit.
    After normalizing J(K) to the unit ball, a candidate ellipsoid has the form a + AB2n and its
relative volume is det A. If its center lies along a shortest principal axis, the two intermediate
ellipsoids admit explicit diagonal representations. Each yields an upper bound on det A in
terms of the same smallest semiaxis α. Neither bound alone gives the optimal constant, but the
maximum of their pointwise minimum does. For an arbitrary displacement, the intermediate
matrices need not be simultaneously diagonalizable. A rank-one matrix inequality nevertheless
establishes the same trace estimates, which suffice for the determinant argument.
    The argument thus converts geometric feasibility into algebraic constraints: containment
supplies feasible shape matrices, maximality bounds their traces, and a common spectral
parameter relates the two estimates. Concavity certifies the final optimization, while the cone
family establishes optimality. A Lean 4 formalization verifies the main theorem and its supporting
results; section D records the scope and reproducibility of the verification.

Organization of the proof. Section 2 derives the two scalar bounds in the diagonal model.
Section 3 establishes the trace comparison needed for arbitrary displacements, and section 4
proves sharpness. Together, these sections present the complete argument for the main result.
Supporting lemmas are stated at their first use, with proofs collected in section 6. Further
consequences appear in section 5, and related work and open questions in section 7. The
appendices supply the standard matrix and ellipsoid facts and an alternative proof of the
rank-one estimate.


2     Two spectral bounds from a diagonal model
2.1   Affine normalization and the determinant ratio
An invertible affine change of coordinates takes J(K) to the Euclidean unit ball B2n and its
center to 0. It preserves containment and multiplies every volume by the same factor. We may
therefore assume J(K) = B2n and write a candidate ellipsoid as

                             E(a, A) = a + AB2n ,      A = A⊤ ≻ 0.

Every nonsingular ellipsoid admits this representation: CB2n = (CC ⊤ )1/2 B2n for any nonsingular
C. The eigenvalues of A are its semiaxis lengths, so

                                      vol(E(a, A))
                                                   = det A.
                                         w(K)

We use the Loewner order for symmetric matrices and spectral calculus for their powers. Thus
tr(Ap ) means the trace after taking the matrix power.
    The central-cut condition has an equivalent algebraic formulation. An ellipsoid contained in
a closed halfspace whose boundary passes through 0 cannot contain 0 in its interior. In ellipsoid
coordinates, this condition is ∥A−1 a∥ ≥ 1.


                                                2
Proposition 2.1 (Center-exclusion formulation). The upper bound in theorem 1.1 is equivalent
to the implication

                E(a, A) ⊂ K,      J(K) = B2n ,       ∥A−1 a∥ ≥ 1        =⇒     det A ≤ r∗ .   (2.1)

    The equivalence is proved in section 6.1. It expresses the geometric restriction through a
displacement norm, eliminating the cutting normal from the subsequent estimates.

2.2     Two geometric ingredients
The construction uses two consequences of geometric feasibility. First, maximality of the unit
ball bounds the trace of every feasible shape matrix.

Lemma 2.2 (Trace constraint). If J(K) = B2n and E(b, S) ⊂ K with S ≻ 0, then tr S ≤ n.

    The second constructs a new feasible ellipsoid from the unit ball and any other ellipsoid
inside K.

Lemma 2.3 (Intermediate ellipsoid). If B2n ⊂ K and E(b, S) ⊂ K, where S ≻ 0, then
                                                          1/2 !
                                        b      1
                                            
                                      E   , S + bb⊤                ⊂ K.                       (2.2)
                                        2      4

    Proofs appear in sections 6.1 and 6.2. The construction is the normalized form of that in
Khachiyan [11], Tarasov et al. [17]. The rank-one term bb⊤ /4 encodes the center displacement
in the new shape matrix, to which the trace constraint can then be applied.
    Apply the construction first to E(a, A), and then to the resulting ellipsoid, always pairing it
with the same unit ball. The new centers are a/2 and a/4, and their shape matrices are

                       T1 = (A + aa⊤ /4)1/2 ,            T2 = (T1 + aa⊤ /16)1/2 .             (2.3)

The coefficient 1/16 in the second expression results from applying the construction to the center
a/2. Since both ellipsoids remain in K, theorem 2.2 gives two necessary conditions:

                                       tr T1 ≤ n,         tr T2 ≤ n.                          (2.4)

   The auxiliary ellipsoids may intersect both sides of the cutting hyperplane. Their role is to
provide consequences of maximality of the original ball, so only containment in K is required.
Figure 1 shows this distinction in dimension two.

2.3     The aligned model
First consider a feasible candidate satisfying

                    A = diag(α, λ2 , . . . , λn ),       a = αe1 ,        α = λmin (A).       (2.5)

The normalized displacement has length one: ∥A−1 a∥ = 1. Both intermediate matrices are
diagonal, and the rank-one perturbation affects only their first diagonal entry. The remaining
entries are obtained by successive square roots. Consequently,
                                                          1/2
                                  T1 = diag f1 (α), λ2 , . . . , λ1/2
                                                                          
                                                                  n   ,
                                                          1/4
                                  T2 = diag f2 (α), λ2 , . . . , λ1/4
                                                                          
                                                                  n   ,                       (2.6)

where                             q                             q
                       f1 (α) =     α + α2 /4,       f2 (α) =        f1 (α) + α2 /16.         (2.7)

                                                     3
                 A cone, its John ball, and a cut                                            The auxiliary ellipsoids may cross the cut
                                      Cut through the origin                                                           Cut through the origin
                                      John ball B                                                                      John ball B
      1.5                             Ellipsoid E in the retained half                 1.5                             First midpoint: center a/2
                                                                                                                       Second midpoint: center a/4

      1.0                                                                              1.0

      0.5                                                                              0.5

      0.0                                                                              0.0
y




                                                                                  y
    −0.5                                                                              −0.5

    −1.0                                                                              −1.0

    −1.5                                                                              −1.5

             −1.0 −0.5   0.0    0.5         1.0       1.5        2.0                         −1.0 −0.5    0.0    0.5      1.0       1.5       2.0
                                t                                                                                t



Figure 1: The construction for the two-dimensional cone used in section 4. Left: the unit ball
and an ellipsoid in the retained half. Right: the two intermediate ellipsoids remain in the cone
even though they cross the cut. Their purpose is to supply the trace constraints (2.4).


    Substituting these diagonal representations into the trace constraints gives
                                                                  n
                                                                  X 1/2j
                                                fj (α) +                 λi       ≤ n,       j = 1, 2.                                                (2.8)
                                                                  i=2

These constraints have so far been established for the aligned model. Section 3 proves them for
arbitrary center displacements. The following determinant calculation depends only on these
spectral sums and therefore applies in either setting.

2.4         From trace constraints to volume bounds
The volume ratio is a product of relative semiaxes, whereas the trace constraints bound sums of
their fractional powers. Taking logarithms and using log z ≤ z − 1 yields
                                                                                  n
                                                                                  X          1/2j
                                      log det A = log α + 2j                          log(λi        )
                                                                                  i=2
                                                                                     n
                                                                                                            !
                                                                              j
                                                                                    X     1/2j
                                                            ≤ log α + 2                  λi    − (n − 1)
                                                                                   i=2
                                                                              j
                                                            ≤ log α + 2 (1 − fj (α)).                                                                 (2.9)

The contribution of the n − 1 remaining semiaxes cancels the dimensional term in the trace
bound. The resulting estimate depends only on α:

                                                                                   Rj (α) = α exp 2j (1 − fj (α)) .
                                                                                                                             
                      det A ≤ min{R1 (α), R2 (α)},                                                                                                   (2.10)

    Both bounds constrain the same ellipsoid and therefore the same value of α. The maximum
of R1 alone is 0.8442948676 . . ., the constant in Khachiyan’s 1990 argument. The maximum of
R2 alone is approximately 0.8248795633. Both exceed the sharp constant. The improvement
follows from bounding their pointwise minimum, as illustrated in figure 2, rather than optimizing
the two bounds separately.



                                                                              4
                                First bound R1(α)
                         0.84   Second bound R2(α)
                                Joint bound min{R1, R2}

                         0.82
    Volume-ratio bound




                         0.80

                                                                   α = 1/2, R1 = R2 = √ e /2
                         0.78

                         0.76

                                 0.3          0.4         0.5         0.6         0.7          0.8      0.9   1.0
                                                                 Smallest semiaxis α

Figure 2: The pointwise minimum of R1 and R2 attains its maximum at α = 1/2, although neither
function individually attains its maximum there. The global bound is proved in section 6.4.


            At α = 1/2, the distinguished semiaxes and the two bounds have the exact values
                                                                                 √
                                   3                7                              e
                         f1 (1/2) = ,     f2 (1/2) = ,     R1 (1/2) = R2 (1/2) =     .
                                   4                8                            2
The following lemma gives the required global conclusion. Its proof in section 6.4 uses concavity
in the variable log α; the plot is only an illustration.

Lemma 2.4 (Joint scalar bound). For the functions defined in (2.10),
                                                       √
                                                         e
                            max min{R1 (α), R2 (α)} =      ,                                                   (2.11)
                            α>0                         2
with the maximum attained at α = 1/2.

    This establishes the upper-bound argument for the diagonal model, subject to the supporting
lemmas proved in section 6. Extending the argument requires only the spectral constraints (2.8)
for arbitrary center displacements; the subsequent determinant calculation is unchanged.


3                    Extension to arbitrary center displacements
The determinant calculation in the preceding section depends only on the eigenvalues of A.
For a general displacement, however, diagonalizing A need not diagonalize aa⊤ . The explicit
eigenvalue expressions for T1 and T2 in the aligned model therefore need not apply.
    The required spectral constraints concern only the two sums in (2.8). They can be established
by trace comparisons, without determining the individual eigenvalues of either intermediate
matrix.

3.1                      Displacement normalization and matrix comparison
Fix an arbitrary feasible candidate satisfying the hypotheses in (2.1). Put

                                    ρ = ∥A−1 a∥ ≥ 1,            u = ρ−1 A−1 a,        b = Au = ρ−1 a.           (3.1)

                                                                     5
Then ∥u∥ = 1 and bb⊤ ⪯ aa⊤ . Shortening the displacement in this way gives comparison
matrices
                  M1 = (A + bb⊤ /4)1/2 ,  M2 = (M1 + bb⊤ /16)1/2 .               (3.2)
Square-root monotonicity gives M1 ⪯ T1 and then M2 ⪯ T2 . Therefore the trace bounds for the
actual intermediate ellipsoids imply
                                       tr M1 ≤ n,         tr M2 ≤ n.                           (3.3)
The reduction uses matrix order alone and makes no feasibility claim for an ellipsoid obtained
by replacing a with b. Its purpose is to express the displacement as b = Au with u a unit vector,
as required by the next lemma.

3.2   A directional trace estimate
For 0 < p < 1 and fixed h > 0, the increment (z + h)p − z p decreases with z > 0. The
following matrix estimate retains quantitative dependence on both the baseline matrix and the
perturbation direction.
Lemma 3.1 (Directional rank-one estimate). Let A ≻ 0, α = λmin (A), ∥u∥ = 1, and b = Au.
If M ≻ 0 and m > 0 satisfy
                                           m
                                     M ⪯ 2 A2 ,                                     (3.4)
                                          α
then, for 0 < p < 1 and t ≥ 0,
                         tr (M + tbb⊤ )p − tr(M p ) ≥ (m + tα2 )p − mp .
                                            
                                                                                               (3.5)
    The proof is in section 6.3, with another proof in section C. Its mechanism is the operator
antitonicity of the derivatives of fractional power functions, which also underlies the trace-
increment inequalities in Bouhtou et al. [4], Sagnol [15]. The additional comparison with A2
gives the explicit scalar lower bound needed here. The lemma applies without requiring A, M ,
and bb⊤ to commute.
    Three applications suffice. The first bounds the trace of M1 ; the other two combine through
cancellation of intermediate terms to bound the trace of M2 .
Proposition 3.2 (Trace bounds for arbitrary displacements). For the comparison matrices
in (3.2) and α = λmin (A),
                                  tr M1 ≥ tr(A1/2 ) + f1 (α) − α1/2 ,                          (3.6)
                                  tr M2 ≥ tr(A1/4 ) + f2 (α) − α1/4 .                          (3.7)
Proof. First iterate. Since A ⪰ αI, spectral calculus gives A ⪯ A2 /α. In theorem 3.1, take
                                     (M, m, p, t) = (A, α, 1/2, 1/4).
The left-hand side is tr M1 − tr(A1/2 ), and the scalar term on the right is f1 (α) − α1/2 . This is
the first trace bound (3.6).
   Second iterate. To apply the lemma with baseline M1 , observe that bb⊤ ⪯ A2 implies
                                                1/2
                                     1 2 1 2                  f1 (α)    f1 (α) 2
                                 
                         M1 ⪯          A + A              =          A⪯       A .              (3.8)
                                     α    4                     α        α2
We can therefore apply theorem 3.1 both with (A, α, 1/4, 1/4) and with (M1 , f1 (α), 1/2, 1/16).
The two conclusions are
                                     1/2
                             tr(M1 ) − tr(A1/4 ) ≥ f1 (α)1/2 − α1/4 ,
                                                1/2
                                 tr M2 − tr(M1 ) ≥ f2 (α) − f1 (α)1/2 .
                           1/2
Adding them cancels tr(M1 ) on the left and f1 (α)1/2 on the right. The remaining inequality is
precisely the second trace bound (3.7).

                                                      6
   The cancellation relates the two intermediate constructions. A fourth-root comparison with
the original matrix and a square-root comparison with the first iterate yield exactly the scalar
expression obtained in the diagonal model.

3.3   Completion of the upper bound
Combine theorem 3.2 with the upper trace bounds (3.3). If λ1 = α, λ2 , . . . , λn are the eigenvalues
of A, the result is
                                           n
                                           X 1/2j
                                fj (α) +         λi   ≤ n,          j = 1, 2.
                                           i=2
These are precisely the constraints in (2.8), established for arbitrary displacements. The
determinant calculation (2.9) thus applies unchanged and gives
                                                            √
                                                              e
                              det A ≤ min{R1 (α), R2 (α)} ≤
                                                             2
by theorem 2.4. The convention of an empty sum covers n = 1. The argument also permits a
repeated smallest eigenvalue, since only one occurrence of α is separated from the sum.
    This proves the upper bound in theorem 1.1 through the center-exclusion formulation. The
diagonal model identifies the sufficient spectral constraints, and the trace comparison establishes
them in general. The next section proves optimality of the constant.


4     Sharpness via circular cones
The sharpness construction combines a factor 1/2 in the semiaxis parallel to the cutting normal
                                           √
with a transverse volume factor tending to e. Both features are realized by an explicit family
of circular cones.
    For n ≥ 2, write x = (t, y) ∈ R × Rn−1 and set
                                                                p
                         Kn = {(t, y) : t ≥ −1,           t+     n2 − 1 ∥y∥ ≤ n}.               (4.1)

Its vertex is (n, 0). Cut at t = 0 and retain Kn− = Kn ∩ {t ≤ 0}. Consider the ellipsoid
                              1          1                 n               n
                                                     r               r         
                        En = − e1 + diag ,                    ,...,           B2n .             (4.2)
                              2          2                n−1             n−1
The left panel of figure 1 is this example for n = 2.
Lemma 4.1 (Normalization and feasibility for the cone family). For the body and ellipsoid just
defined, J(Kn ) = B2n and En ⊂ Kn− .
   The proof in section 6.5 gives explicit contact weights for the first assertion and checks the
supporting halfspaces for the second. No maximality assertion about En inside the half-cone is
needed.
   The semiaxes give the explicit volume-ratio lower bound
                                                                      √
                       w(Kn− )
                                                       (n−1)/2
                                  vol(En )    1    n                    e
                                                
                                ≥           =                   −→        .                 (4.3)
                        w(Kn )    vol(B2n )   2 n−1                    2
Indeed, with m = n − 1, the logarithm of the transverse product is
                                      m         1                 1
                                                           
                                        log 1 +                 −→ .
                                      2         m                 2
                                                                        √
Each transverse semiaxis tends to one, whereas their product tends to e. This accumulated
transverse contribution compensates for part of the contraction in the cutting direction.

                                                      7
Completion of the proof of theorem 1.1. Section 3, using the lemmas proved in section 6, es-
tablishes the upper bound for every convex body and central cut. For any smaller constant
    √
r < e/2, the lower bound in (4.3) exceeds r in sufficiently large dimension. Hence no smaller
constant is valid simultaneously in all dimensions.

    The cone example and its limiting value already appear in Khachiyan [11], Tarasov et al.
[17]. The role of the construction here is to match the upper bound with an explicit normalized
witness. Uniform sharpness is a statement over all dimensions; it does not imply equality in any
fixed dimension. In dimension one, a body is an interval and the central cut halves its length, so
the optimal ratio is 1/2.


5     Consequences of the spectral bounds
The spectral constraints also yield a finite-dimensional estimate, strictness of the universal bound
in finite dimension, and a necessary condition for near equality. We establish these consequences
before presenting the supporting proofs. Throughout this section, E(a, A) satisfies the normalized
hypotheses in (2.1) and α = λmin (A).

5.1   Dimension-dependent estimates
The estimate based on log z ≤ z − 1 eliminates the dimension dependence. Applying the
arithmetic–geometric mean inequality directly to the same spectral constraints instead yields an
explicit dependence on n. For n ≥ 2,
                                                        2j (n−1)
                                           n − fj (α)
                                       
                           det A ≤ α                                ,    j = 1, 2.              (5.1)
                                             n−1
The bases are positive for a feasible nonsingular ellipsoid. These are useful bounds for a prescribed
dimension, but we do not claim that optimizing them determines that dimension’s best possible
constant.

5.2   Nonattainment and near equality
For these conclusions it is useful to record the quantitative certificate proved in section 6.4.
Define
                                                 1
            x = log α,     x0 = − log 2,    C = − log 2,       Fj (x) = log Rj (ex ).
                                                 2
The global tangent bounds are
                                           x − x0                          x − x0
                         F1 (x) ≤ C +             ,        F2 (x) ≤ C −           .             (5.2)
                                             6                               42
For x < x0 , the first upper bound is strictly below C; for x > x0 , the second is strictly below C.
These inequalities establish nonattainment away from α = 1/2 and quantitatively constrain the
smallest semiaxis of a near-extremizer.
Corollary 5.1. In finite dimension, every nonsingular ellipsoid satisfying the assumptions
                    √
in (2.1) has det A < e/2.
Proof. If α ̸= 1/2, the relevant tangent bound in (5.2) is strictly below C. If α = 1/2 and n ≥ 2,
use j = 1 in the finite-dimensional bound (5.1):
                                                            2(n−1)
                                    1       1                            1
                                           
                            det A ≤   1+                                < e1/2 .
                                    2    4(n − 1)                        2
For n = 1 and α = 1/2, the determinant is 1/2.

                                                      8
Corollary 5.2. Under the same assumptions,
                                            1    1
                                  r∗         log
                                                   ,       0 < α ≤ 12 ,
                             log      ≥ 61     2α                                           (5.3)
                                 det A 
                                           log(2α),        α ≥ 12 .
                                         42
In particular, if det A ≥ r∗ e−ε for ε ≥ 0, then
                                        1 −6ε      1
                                          e   ≤ α ≤ e42ε .                                  (5.4)
                                        2          2
Proof. Combine log det A ≤ Fj (x) with the first tangent bound when x ≤ x0 and the second
when x ≥ x0 . Subtracting from C gives inequality (5.3); solving for α gives the bounds (5.4).

    This necessary condition controls only the smallest semiaxis. A geometric stability theorem
would additionally require control of the remaining semiaxes, the center displacement, and the
surrounding body.

5.3   Repeated exact central cuts
For an idealized sequence

                               Kk+1 = Kk ∩ Hk ,          c(Kk ) ∈ ∂Hk ,

successive applications of the main theorem give

                                                       w(K0 )             1
                                                                          
                     w(KN ) ≤ r∗N w(K0 ),      log            ≥ N log 2 −   .               (5.5)
                                                       w(KN )             2

This is the optimal universal one-step factor for the exact-center volume measure. An algorithmic
complexity claim would also have to account for finding the centers, numerical accuracy, and
separation costs. The geometric inequality alone does not provide those additional estimates.


6     Proofs of the supporting results
This section proves the results used in the preceding argument: the geometric reduction, the
directional rank-one estimate, the joint scalar bound, and the cone certificate. The proofs are
independent of the main theorem, so the deferred presentation introduces no circular dependence.

6.1   Center exclusion and first-order maximality
Proof of theorem 2.1. The equation 0 = a + Ay has the unique solution y = −A−1 a. Thus
0∈/ int E(a, A) is equivalent to ∥A−1 a∥ ≥ 1. Any ellipsoid in a halfspace through 0 has this
property, so the implication (2.1) suffices for the central-cut theorem.
   Conversely, suppose ρ = ∥A−1 a∥ ≥ 1 and set v = A−2 a =      ̸ 0. The minimum of the linear
functional v ⊤ x on the ellipsoid is

                              min v ⊤ x = v ⊤ a − ∥Av∥ = ρ2 − ρ ≥ 0.
                            x∈E(a,A)


Hence the ellipsoid lies in the closed halfspace v ⊤ x ≥ 0. A central-cut upper bound applied to
that halfspace implies (2.1), proving equivalence.




                                                   9
Proof of theorem 2.2. Convexity provides a feasible path from the unit ball toward E(b, S):

                            tb + ((1 − t)I + tS)B2n ⊂ K,       0 ≤ t ≤ 1.

Indeed, the point associated with y ∈ B2n is the convex combination (1 − t)y + t(b + Sy). Its
shape matrix stays positive definite. Since the unit ball has maximum volume,

                                     log det((1 − t)I + tS) ≤ 0.

The right derivative at t = 0 is tr(S − I) and cannot be positive. Therefore tr S ≤ n.

6.2    Containment of the intermediate ellipsoid
Containment can be checked one supporting direction at a time. For an ellipsoid, the support
function is
                                hE(b,S) (v) = v ⊤ b + ∥Sv∥,                             (6.1)
obtained by maximizing (Sv)⊤ y over y ∈ B2n . This identity provides an algebraic criterion for
the required containment.

Proof of theorem 2.3. Fix v ̸= 0 and put h = hK (v) and s = v ⊤ b. The assumed containments
give
                                  ∥v∥ ≤ h,    ∥Sv∥ ≤ h − s.
In particular h > 0 and s ≤ h. Cauchy–Schwarz therefore implies

                                   v ⊤ Sv ≤ ∥v∥ ∥Sv∥ ≤ h(h − s).

Adding the rank-one term completes a square:

                         v ⊤ (S + bb⊤ /4)v ≤ h2 − hs + s2 /4 = (h − s/2)2 .

Since h − s/2 > 0, the support function of the proposed ellipsoid is at most
                                    s q ⊤
                                      + v (S + bb⊤ /4)v ≤ h.
                                    2
It satisfies every support-function bound of K, which proves the containment in (2.2).

6.3    The directional rank-one estimate
The matrix facts needed here are proved in section B: inverse and negative fractional powers
reverse the positive definite order, and differentiation after taking the trace gives D[tr(X p )](H) =
p tr(X p−1 H). These facts hold without commuting matrices.

Proof of theorem 3.1. Since ∥u∥ = 1, we have uu⊤ ⪯ I and therefore bb⊤ ⪯ A2 . Combining this
with the assumed baseline comparison gives, for s ≥ 0,
                                                    m + sα2 2
                                     M + sbb⊤ ⪯            A .                                   (6.2)
                                                      α2
The exponent p − 1 belongs to (−1, 0). Its operator antitonicity reverses the comparison:
                                                             !p−1
                                       ⊤ p−1       m + sα2
                             (M + sbb )        ⪰                    A2p−2 .
                                                     α2

Evaluate both sides on b = Au. Since u⊤ A2p u ≥ α2p ,

                              b⊤ (M + sbb⊤ )p−1 b ≥ α2 (m + sα2 )p−1 .                           (6.3)

                                                   10
On the other hand, the trace derivative is
                           d
                              tr (M + sbb⊤ )p = p b⊤ (M + sbb⊤ )p−1 b.
                                             
                           ds
Multiply inequality (6.3) by p and integrate from 0 to t. The resulting scalar integral is
(m + tα2 )p − mp , proving inequality (3.5).

   The matrix A both bounds the baseline from above and parametrizes the displacement through
b = Au. The eigenvalue estimate concerns only a power of A; simultaneous diagonalization of
M and bb⊤ is not required. Likewise, the derivative formula is for the trace; it does not assert
that the full matrix derivative of X p is multiplication by pX p−1 .
Remark 6.1 (Exactness in the shortest-axis case). If u is a unit eigenvector of A for α and
M = (m/α2 )A2 , the perturbation changes only the eigenvalue m in that direction. Equality
then holds in (3.5). This is the equality case underlying the scalar functions f1 and f2 .

6.4   The joint scalar bound
Proof of theorem 2.4 and the tangent bounds (5.2). Put

                            Fj (x) = log Rj (ex ) = x + 2j (1 − fj (ex )).

The required concavity holds in this logarithmic coordinate. To verify it, write
                                           1
                             log f1 (ex ) =  log(ex + e2x /4),
                                           2
                                           1              x
                             log f2 (ex ) = log elog f1 (e ) + e2x /16 .
                                                                      
                                           2
The function (s, t) 7→ log(es + et ) is convex and nondecreasing in both variables. The first
displayed expression is therefore convex, and composition gives convexity of the second. Hence
fj (ex ) are positive log-convex functions, in particular convex functions. It follows that F1 , F2
are concave.
     At x0 = − log 2, direct calculation gives
                                            3                    7
                                  f1 (1/2) = ,         f2 (1/2) = ,                           (6.4)
                                            4                    8
                                   ′        5           ′        43
                                 f1 (1/2) = ,         f2 (1/2) = .                            (6.5)
                                            6                    84
With C = 1/2 − log 2, this means
                                                            1                      1
                    F1 (x0 ) = F2 (x0 ) = C,     F1′ (x0 ) = ,    F2′ (x0 ) = −      .        (6.6)
                                                            6                     42
Each concave function lies below its tangent at x0 , proving both bounds in (5.2). If x ≤ x0 , the
first tangent is at most C; if x ≥ x0 , the second is at most C. Thus

                               min{F1 (x), F2 (x)} ≤ C        (x ∈ R).

At x = x0 both functions equal C. Exponentiating proves the exact maximum in (2.11).

   The two parameter ranges in figure 2 are therefore controlled by different constraints. The
tangent inequalities determine and certify the joint maximum analytically.




                                                 11
Remark 6.2 (An equivalent weighted certificate). An equivalent certificate combines the two
tangent inequalities. The weights 1/8 and 7/8 cancel the slopes in (6.6), so the concave function
                                              1        7
                                        G(x) = F1 (x) + F2 (x)
                                              8        8
has derivative zero at x0 and global maximum C. Since min(F1 , F2 ) ≤ G, this also proves the
bound. The weights follow from θ/6 − (1 − θ)/42 = 0, rather than numerical fitting.
   For comparison with the 1990 estimate, substituting α = d−2 into R1 gives
                                                        p                   !
                                    −2           2 1 + 1/(4d2 )
                                   d     exp 2 −                .
                                                      d

This is Khachiyan’s final expression. Its maximizer satisfies 4d6 − 3d4 − 4d2 − 1 = 0. The
additional bound R2 is restrictive near that maximizer, while R1 is restrictive near the maximizer
of R2 . Their complementarity is the improvement used here.

6.5   The cone certificate
Proof of theorem 4.1. Every point (t, y) ∈ B2n satisfies t ≥ −1, and Cauchy–Schwarz gives
                                    p                        q
                               t+       n2 − 1 ∥y∥ ≤ n t2 + ∥y∥2 ≤ n

on the ball. Hence B2n ⊂ Kn . The base contact is u0 = −e1 , and the side contacts are
                                               r             !
                                         1            1
                              uv =         ,       1− 2 v ,           ∥v∥ = 1.
                                         n           n

Choose v among the signed coordinate vectors of Rn−1 . Give u0 weight c0 = n/(n + 1) and each
of the 2(n − 1) chosen side contacts weight

                                                          n2
                                               cv =              .
                                                       2(n2 − 1)

The total side weight is n2 /(n + 1), so the first-coordinate mean is −n/(n + 1) + n/(n + 1) = 0.
Transverse means and mixed second moments vanish in signed pairs. The first-coordinate second
moment is n/(n + 1) + 1/(n + 1) = 1, and each transverse second moment is 2cv (1 − 1/n2 ) = 1.
Thus
                                                       ci ui u⊤
                                 X                  X
                                     ci ui = 0,               i = I.                        (6.7)
                                    i                        i

These are supporting directions for Kn . The sufficient contact certificate in theorem A.2 therefore
gives J(Kn ) = B2n .
    For the second assertion, the first coordinate of En lies in [−1, 0]. At every side normal uv ,
its support function is
                              s
                        1          1      n     1                          1      1
                                                                
                     −    +          2
                                       +     1− 2                    =−      +1+    = 1.
                       2n         4n     n−1   n                          2n     2n

It therefore satisfies the base, cut, and all side inequalities, proving En ⊂ Kn− .

   This completes the proofs of the supporting results used in sections 2 to 4. The standard
matrix facts and the contact-certificate argument are supplied in the appendices.




                                                        12
7     Related work and further directions
The diagonal model identifies the spectral constraints required for the determinant estimate, and
the trace comparison extends them to arbitrary displacements. The corresponding geometric
construction, center-computation methods, and matrix inequalities belong to distinct strands of
the literature.

7.1   Geometric foundations
Extremal ellipsoids were studied well before their use in cutting-plane methods. Behrend treated
the smallest circumscribed and largest inscribed ellipses in the plane [2]. John’s variational
approach [10] and subsequent work, including that of Danzer, Laugwitz, and Lenz [5], underlie
the modern theory. Güler and Gürtuna [9] give an account of existence, uniqueness, contact
conditions, symmetry, and examples, together with a discussion of the terminology.
    The argument uses three ingredients from this theory. The maximum-volume ellipsoid
provides a normalization, its maximality provides a trace constraint, and a sufficient contact
certificate verifies the cone. The necessity part of the full John contact-point characterization is
not used. This permits the elementary, self-contained treatment in section A.

Ordinary volume and centroid cuts. For ordinary volume, Grünbaum [8, Theorem 2 and
its proof] establishes a sharp inequality for cuts through the centroid g(K). Applying it to the
two closed halfspaces determined by a hyperplane through g(K) gives
                                                                           n
                             vol(K ∩ H)                               n
                                                                 
                        γn ≤            ≤ 1 − γn ,        γn =                  .
                               vol(K)                                n+1

The upper bound follows from the lower bound for the opposite halfspace, and both dimension-
dependent constants are sharp. Since γn > e−1 and γn → e−1 , the optimal dimension-independent
upper factor for these ordinary-volume ratios is 1 − e−1 . This result controls vol(K ∩ H)/ vol(K)
at the centroid, whereas theorem 1.1 controls w(K ∩ H)/w(K) at the center c(K) of the
maximum-volume inscribed ellipsoid. The two centers need not coincide; the constants therefore
concern different volume functionals and cutting rules.

7.2   Cutting-plane geometry and center computation
The method of inscribed ellipsoids of Tarasov et al. [17] uses exact or sufficiently accurate
approximate centers to localize solutions of convex optimization problems. Their Russian
original states the central-cut factor 0.843, displays a recursive estimate 0.8429 . . ., and gives
               √
the cone limit e/2. It also proves the weaker 8/9 bound as an intermediate step. Khachiyan’s
1990 paper gives its own 0.844 . . . proof and explicitly proposes the sharp-constant conjecture
[11]. The intermediate construction and its recursive use therefore have established precedents.
The result here comes from the quantitative trace comparison and the simultaneous use of the
two resulting bounds.
    The contraction factor depends on the position of the cutting hyperplane. Primak and
Kheyfets [14] obtain a factor 1/2 in a modified method using a cut tangent to the current
maximum-volume ellipsoid. Its hypothesis differs from the central-cut condition of theorem 1.1.
That smaller factor is therefore not a bound for the problem considered here.
    Computing the center is a separate optimization task. Khachiyan and Todd [12] analyze
approximation through a sequence of maximal-inscribed-paraboloid problems. Anstreicher [1]
improves the complexity of inscribed-ellipsoid approximation, and Zhang and Gao [20] study
numerical formulations and practical primal-dual methods. More recently, Sun [16] analyzes




                                                13
a polarity iteration using minimum-volume covering ellipsoids of shifted polars, with instance-
dependent convergence. These works address the cost or convergence of finding an ellipsoid; the
present theorem addresses the geometric effect of a cut after an exact center is known.
   For approximate centers, Wada and Fujisaki [19, Lemma 1] use a factor 8/(9η 2 ) when the
available ellipsoid has volume at least an η fraction of the optimum. Our trace constraint uses
                                                                                          √
exact maximality. Replacing that approximate-center factor by an expression involving e/2
would require a separate argument. Broader accounts of Khachiyan’s geometric and algorithmic
contributions are given by Boros and Gurvich [3] and Elbassioni and Dumitrescu [7].

7.3   Trace inequalities and the directional estimate
For suitable trace functions, the dependence of an increment on the matrix baseline admits a
noncommutative monotonicity principle. Bouhtou et al. [4] use strong subadditivity of fractional
trace powers in experimental design. Sagnol [15, Proposition 2.3] proves, for a continuous f on
[0, ∞) with operator-antitone derivative on (0, ∞),

                    tr f (X + Y + Z) + tr f (Z) ≤ tr f (X + Z) + tr f (Y + Z)                  (7.1)

for positive semidefinite arguments. For f (x) = xp , 0 < p < 1, the derivative pxp−1 is operator
antitone. Recent discussion and further examples appear in Niculescu [13]; the fractional-power
statement is proved here in section B.
     Theorem 3.1 uses this antitonicity and trace-calculus mechanism in a quantitative directional
setting. The baseline comparison with A2 and the correlated vector b = Au preserve the displace-
ment information needed by the geometric application. The estimate is stated independently of
ellipsoids, so it may be studied as a matrix tool in other problems. Its application here is precise:
one square-root estimate and two telescoping estimates yield the pair of constraints that the
diagonal model suggested.

7.4   Further directions
The dimension-independent question is settled by the matching upper bound and cone limit.
The best constant for each prescribed dimension remains undetermined by this argument. The
near-equality condition in theorem 5.2 controls only the smallest semiaxis; a geometric stability
result would also need information about the other axes, the displacement, and the body. A
robust analogue for approximate centers would connect the exact theorem more directly to
implementations of cutting-plane methods.
    The argument relies on the interaction of two spectral constraints. The diagonal model
identifies their form, matrix analysis establishes them for arbitrary displacements, and convex
analysis determines the parameter range controlled by each bound. Their combination yields
the dimension-independent constant.

Proof provenance and use of AI. The proof was discovered by an AI language model in
response to a research problem posed by the first author. The development included the matrix
estimates, literature comparisons, exact scalar calculations, and numerical error checks. AI
assistance was also used to develop the Lean 4 formalization. The resulting formal proofs have
been checked by Lean’s kernel, with the scope and audit described in section D. The human
authors are responsible for the mathematical interpretation, literature attribution, and final
submitted manuscript.




                                                 14
A     Basic facts on maximal inscribed ellipsoids
This appendix supplies the existence, uniqueness, and certificate facts used in the main text. It
does not require the necessity part of the general contact-point characterization.

Proposition A.1. Every convex body K ⊂ Rn contains a unique maximum-volume ellipsoid.

Proof. Consider pairs (a, A) with A ⪰ 0 and a + AB2n ⊂ K. This set is closed. Moreover,
a ∈ K, and for every unit vector u, the two points a ± Au lie in K, so 2∥Au∥ ≤ diam K. Thus
the feasible pairs form a compact set. The determinant attains a maximum, which is positive
because K contains a ball of positive radius. A maximizing matrix is therefore positive definite.
    The feasible set of pairs is convex, as follows by taking pointwise convex combinations with
the same y ∈ B2n . Suppose (a0 , A0 ) and (a1 , A1 ) both maximize the determinant. Strict concavity
of log det on the positive definite cone implies A0 = A1 . For completeness, along S(t) = A0 + tD,
with D = A1 − A0 ̸= 0,

                          d2
                               log det S(t) = − tr S(t)−1 DS(t)−1 D < 0,
                                                                   
                          dt 2


since the trace on the right is the squared Frobenius norm of S(t)−1/2 DS(t)−1/2 .
    If the centers were distinct, an affine normalization would give two maximizing ellipsoids
B2n and b + B2n , with b =
                         ̸ 0, inside the transformed body. Theorem 2.3, whichpdoes not assume
                                                    ⊤   1/2
maximality, produces an ellipsoid with shape (I + bb /4) . Its determinant is 1 + ∥b∥2 /4 > 1,
a contradiction. Thus the centers agree as well.

Lemma A.2 (Sufficient contact certificate). Suppose B2n ⊂ K and there are unit vectors ui and
positive weights ci such that

              K ⊂ {x : u⊤                                                       ci ui u⊤
                                                          X                 X
                        i x ≤ 1}     for every i,              ci ui = 0,              i = I.
                                                           i                i

Then J(K) = B2n .

Proof. For every E(a, A) ⊂ K,

                             u⊤
                              i a + ∥Aui ∥ ≤ 1,          u⊤
                                                          i Aui ≤ ∥Aui ∥.

Multiply by ci and sum. The assumed identities give tr A ≤ i ci = n. The arithmetic–geometric
                                                                   P

mean inequality yields det A ≤ (tr A/n)n ≤ 1. Since the ball is feasible, it is maximizing, and
uniqueness follows from theorem A.1.

   This is the sufficient direction of the standard contact certificate used in extremal-ellipsoid
theory; see Güler and Gürtuna [9]. In section 6.5, all supporting directions and weights are given
explicitly.


B     Fractional trace powers and diminishing increments
We give the matrix facts used in section 6. They are classical; integral proofs are included to
specify the order and differentiability assertions without a commutativity assumption.

Lemma B.1. If 0 ≺ X ⪯ Y , then Y −1 ⪯ X −1 . For 0 < θ < 1,

                                   Xθ ⪯ Y θ,           X −θ ⪰ Y −θ .




                                                  15
Proof. Write Y = X 1/2 CX 1/2 with C ⪰ I. Then C −1 ⪯ I and Y −1 = X −1/2 C −1 X −1/2 ⪯ X −1 .
    The scalar beta integral, transferred to positive definite matrices by orthogonal diagonalization,
gives
                                 sin(πθ) ∞ θ−1
                                                           Z
                                  Xθ =     s X(X + sI)−1 ds,                                         (B.1)
                                    π    0
                                 sin(πθ) ∞ −θ
                                        Z
                              −θ
                             X =           s (X + sI)−1 ds.                                          (B.2)
                                    π    0
These integrals converge in norm in finite dimension. The negative-power comparison follows
immediately from the inverse comparison. For positive powers, use X(X +sI)−1 = I −s(X +sI)−1
and integrate the resulting order inequality with positive weights.
Lemma B.2 (Trace differentiation). Let 0 < p < 1, X ≻ 0, and let H be symmetric. Then
                                      D tr(X p ) (H) = p tr(X p−1 H).
                                                      
                                                                                                     (B.3)
Proof. Take the trace in the integral representation (B.1) and differentiate in the direction H.
With Rs = (X + sI)−1 , differentiation of I − sRs and cyclicity of the trace give
                                                                      Z ∞
                                                           sin(πp)
                            D tr(X p ) (H) =                                sp tr(Rs2 H) ds.
                                              
                                                              π       0
Differentiation under the integral is valid locally uniformly on the positive definite cone: the
integrand is bounded by an integrable multiple of sp near zero and sp−2 at infinity. In an
eigenbasis of X, the scalar identity
                                                                  sp
                                                   Z ∞
                                      sin(πp)
                                                                        ds = pλp−1
                                         π         0           (λ + s)2
proves the trace identity (B.3). The scalar identity follows by integration by parts from the
negative-power integral. Repeated eigenvalues cause no difficulty.
    In particular, setting H = bb⊤ proves the derivative formula used in theorem 3.1. This trace
identity does not imply that the full derivative of X p is multiplication by pX p−1 .
Proposition B.3 (Diminishing trace increments). Let 0 < p < 1, 0 ≺ X ⪯ Y , and H ⪰ 0.
Then
                   tr((X + H)p ) − tr(X p ) ≥ tr((Y + H)p ) − tr(Y p ).         (B.4)
Equivalently, for U, V, W ⪰ 0,
                 tr((U + V + W )p ) + tr(W p ) ≤ tr((U + W )p ) + tr((V + W )p ).                    (B.5)
Proof. Put Z = Y − X ⪰ 0 and
                   g(t) = tr((X + tZ + H)p ) − tr((X + tZ)p ),                          0 ≤ t ≤ 1.
By theorems B.1 and B.2,
                                                                                       
                     g ′ (t) = p tr     (X + tZ + H)p−1 − (X + tZ)p−1 Z ≤ 0.
Indeed, the bracket is negative semidefinite, so its product with Z has nonpositive trace, as is
seen by conjugating with Z 1/2 . Hence g(0) ≥ g(1), proving inequality (B.4). Taking X = W ,
Y = V + W , H = U proves inequality (B.5) for W ≻ 0. Replacing W by W + εI and letting
ε ↓ 0 extends it to the stated semidefinite case. The reverse implication follows from the same
substitutions.
    The proposition is the fractional-power case of the established strong-subadditivity principle
in Bouhtou et al. [4], Sagnol [15]; see also Niculescu [13, Corollary 4]. Its proof is included
for self-containment, not as a separate novelty claim. The explicit lower bound in theorem 3.1
additionally uses the comparison with A2 and the correlated vector b = Au.

                                                                 16
C     A resolvent proof of the directional estimate
An alternative proof of theorem 3.1 separates the quantitative directional comparison from a
general rank-one integral identity.
    Under the assumptions of that lemma, adding sI to the matrix comparison (3.4) and then
inverting gives, for s > 0,
                                                                              −1
                                                                  m 2
                                                              
                              b⊤ (M + sI)−1 b ≥ u⊤ A2                A + sI         u
                                                                  α2
                                                         α2
                                                    ≥       .                                            (C.1)
                                                        m+s
For the second inequality, diagonalize A and use monotonicity of

                                                        λ2
                                           λ 7−→
                                                    (m/α2 )λ2 + s

on (0, ∞). Every eigenvalue of A is at least α, and ∥u∥ = 1. The first comparison makes no
assumption that M commutes with A.
   Let N = M + tbb⊤ . For 0 < p < 1, the rank-one identity is
                                                    Z ∞
                                        p sin(πp)                                          
                tr(N p ) − tr(M p ) =                     sp−1 log 1 + t b⊤ (M + sI)−1 b ds.             (C.2)
                                            π       0

To establish this identity, take the trace difference in the integral representation (B.1). Writing

                              L(s) = log det(N + sI) − log det(M + sI),

the result is                                                       Z ∞
                                                 sin(πp)
                                  p           p
                             tr(N ) − tr(M ) = −                          sp L′ (s) ds.
                                                    π                0
                                                                                          R ∞ p−1
Integration by parts replaces the right-hand side by p sin(πp)/π times                     0 s    L(s) ds. The
determinant lemma identifies
                                                                            
                                  L(s) = log 1 + t b⊤ (M + sI)−1 b ,

which proves identity (C.2). All boundary terms vanish: L(s) is bounded as s ↓ 0, while
L(s) = O(s−1 ) as s → ∞, and 0 < p < 1.
   Finally insert the resolvent bound (C.1) into the integral identity (C.2). The resulting lower
bound is                                            !
                   p sin(πp) ∞ p−1             tα2
                             Z
                                 s   log 1 +           ds = (m + tα2 )p − mp ,
                       π      0               m+s
where the equality is the scalar case of the same integral identity. This proves inequality (3.5)
without differentiating along the perturbation path.




                                                         17
D     Formal verification
The main theorem and the supporting mathematical results have been formalized in Lean 4 [6]
using mathlib [18]. The development covers actual ellipsoids in Euclidean space and Lebesgue
volume, including existence and uniqueness of the maximal ellipsoid, affine normalization, the
central-cut bound in every positive dimension, and the cone construction proving uniform
optimality. It also verifies the finite-dimensional estimates, nonattainment, the exact one-
dimensional ratio, the near-equality constraints, and the iteration bounds.

Statements and representations. The geometric space is EuclideanSpace over R with
coordinates indexed by Fin n. Shape matrices are real and positive definite, matrix comparisons
use the Loewner order, and fractional powers use continuous functional calculus. The volume
functional is the supremum of the Lebesgue volumes of feasible ellipsoids; positivity, finiteness,
and attainment are proved. Thus the final geometric theorem has the hypotheses of theorem 1.1,
without additional trace constraints or commutativity assumptions. Selected declaration names
are listed below; each belongs to the namespace Khachiyan.

Result                                       Lean declaration
Geometric upper bound                        t01
Uniform optimality                           sharp_constant
Existence and uniqueness                     existsUnique_isMaxDet
Directional estimate: trace proof            RankOne.trace_increment_lower_bound
Directional estimate: resolvent proof        Resolvent.trace_increment_lower_bound
Finite-dimensional nonattainment             normalized_det_lt_rStar, t03
Near equality and repeated cuts              t04, t05


Independent routes and verification scope. Both proofs of theorem 3.1 are formalized for
every 0 < p < 1, every t ≥ 0, and arbitrary unit directions. The resolvent route shares spectral
and order foundations with the trace route. Its actual import closure and transitive proof
dependencies exclude the trace-derivative and primary rank-one modules, and its final theorem
has the same hypotheses and conclusion. The formalization uses equivalent implementations
of some intermediate calculations: a spectral midpoint
                                                   R ∞ p−1
                                                           argument proves uniqueness, and the
integral formulas use the positive normalization ( 0 s /(1 + s) ds)−1 . The explicit evaluation
of this normalization as sin(πp)/π is not a separate verified theorem. The verification claim
concerns the mathematical statements and their proofs, rather than a line-by-line transcription
of every displayed calculation or the historical survey.

Reproducibility and trusted foundations. The development fixes Lean v4.35.0-rc2
and mathlib commit 0a6c8e0355da0405d616f80b9f8232c4fab2cc5b. A fresh verification on
September 23, 2026 rebuilt the project and its pinned library dependencies from source in a clean
checkout, using the installed Lean toolchain. The complete audit checked 598 declarations; a
separate audit checked all 43 public declarations of the resolvent route. Their axiom dependencies
contain only Lean’s standard foundational axioms propext, Classical.choice, and Quot.sound.
No proof placeholder, project-specific axiom, or external numerical oracle occurs in the certified
chain.

Source availability. The formal-verification source is publicly available at https://github.
com/DrZhouKarl/KhachiyanEllipsoidConjecture. The repository includes the Lean sources,
pinned version files, a statement map, and scripts/verify.py, which reruns the build, the
axiom and independence audits, and the comparison of the two rank-one theorem statements.
The published sources and version files match the audited development byte for byte.


                                               18
References
 [1] Kurt M. Anstreicher. Improved complexity for maximum volume inscribed ellipsoids. SIAM Journal
     on Optimization, 13(2):309–320, 2002.
 [2] F. Behrend. Über die kleinste umbeschriebene und die größte einbeschriebene Ellipse eines konvexen
     Bereichs. Mathematische Annalen, 115:379–411, 1938.
 [3] Endre Boros and Vladimir Gurvich. Scientific contributions of Leo Khachiyan (a short overview).
     Discrete Applied Mathematics, 156:2232–2240, 2008. doi: 10.1016/j.dam.2008.04.023.
 [4] Mustapha Bouhtou, Stéphane Gaubert, and Guillaume Sagnol. Submodularity and randomized
     rounding techniques for optimal experimental design. Electronic Notes in Discrete Mathematics, 36:
     679–686, 2010.
 [5] L. Danzer, D. Laugwitz, and H. Lenz. Über das Löwnersche Ellipsoid und sein Analogon unter den
     einem Eikörper einbeschriebenen Ellipsoiden. Archiv der Mathematik, 8:214–219, 1957.
 [6] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language.
     In Automated Deduction – CADE 28, volume 12699 of Lecture Notes in Computer Science, pages
     625–635. Springer, 2021. doi: 10.1007/978-3-030-79876-5_37.
 [7] Khaled Elbassioni and Adrian Dumitrescu. Computational geometry column 66. ACM SIGACT
     News, 48(4):57–74, 2017. doi: 10.1145/3173127.3173138.
 [8] Branko Grünbaum. Partitions of mass-distributions and of convex bodies by hyperplanes. Pacific
     Journal of Mathematics, 10(4):1257–1261, 1960. doi: 10.2140/pjm.1960.10.1257.
 [9] Osman Güler and Filiz Gürtuna. The extremal volume ellipsoids of convex bodies, their symmetry
     properties, and their determination in some special cases. arXiv:0709.0707, 2007. URL https:
     //arxiv.org/abs/0709.0707. Version 1.
[10] Fritz John. Extremum problems with inequalities as subsidiary conditions. In Studies and Essays
     Presented to R. Courant on His 60th Birthday, pages 187–204. Interscience, New York, 1948.
[11] L. G. Khachiyan. An inequality for the volume of inscribed ellipsoids. Discrete & Computational
     Geometry, 5:219–222, 1990. doi: 10.1007/BF02187786.
[12] Leonid G. Khachiyan and Michael J. Todd. On the complexity of approximating the maximal inscribed
     ellipsoid for a polytope. Mathematical Programming, 61:137–159, 1993. doi: 10.1007/BF01582144.
[13] Constantin P. Niculescu. Old and new on strongly subadditive/superadditive functions. Analysis
     and Mathematical Physics, 15:100, 2025. doi: 10.1007/s13324-025-01095-1.
[14] M. E. Primak and B. L. Kheyfets. A modification of the inscribed ellipsoid method. Mathematical
     and Computer Modelling, 21(11):69–76, 1995.
[15] Guillaume Sagnol. Approximation of a maximum-submodular-coverage problem involving spectral
     functions, with application to experimental designs. Discrete Applied Mathematics, 161:258–276,
     2013. doi: 10.1016/j.dam.2012.07.016.
[16] Kaizhao Sun. The polarity process for the maximum-volume inscribed ellipsoid problem.
     arXiv:2609.10888, 2026. URL https://arxiv.org/abs/2609.10888. Version 1.
[17] S. P. Tarasov, L. G. Khachiyan, and I. I. Erlikh. The method of inscribed ellipsoids. Doklady
     Akademii Nauk SSSR, 298(5):1081–1085, 1988. In Russian. English translation: Soviet Mathematics
     Doklady 37 (1988), 226–230.
[18] The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
     International Conference on Certified Programs and Proofs, CPP 2020. ACM, 2020. doi: 10.1145/
     3372885.3373824.
[19] Takayuki Wada and Yasumasa Fujisaki. Sequential randomized algorithms: A probabilistic cutting
     plane technique based on maximum volume ellipsoid center. In 2010 IEEE International Symposium
     on Computer-Aided Control System Design, pages 1533–1538, Yokohama, Japan, 2010.
[20] Yin Zhang and Liyan Gao. On numerical solution of the maximum volume ellipsoid problem. SIAM
     Journal on Optimization, 14(1):53–76, 2003. doi: 10.1137/S1052623401397230.




                                                  19
