                                                Interpolation synthesis for quadratic polynomial
                                                     inequalities and combination with EUF

                                             Ting Gan1 , Liyun Dai1 , Bican Xia1 , Naijun Zhan2 , Deepak Kapur3 , and Mingshuai Chen2
                                                         1
                                                            LMAM & School of Mathematical Sciences, Peking University
                                                                   {gant,dailiyun,xbc}@pku.edu.cn,
arXiv:1601.04802v3 [cs.LO] 10 Nov 2016




                                                        2
                                                           State Key Lab. of Computer Science, Institute of Software, CAS
                                                                                znj@ios.ac.cn
                                                          3
                                                             Department of Computer Science, University of New Mexico
                                                                              kapur@cs.unm.edu



                                                 Abstract. An algorithm for generating interpolants for formulas which are con-
                                                 junctions of quadratic polynomial inequalities (both strict and nonstrict) is pro-
                                                 posed. The algorithm is based on a key observation that quadratic polynomial
                                                 inequalities can be linearized if they are concave. A generalization of Motzkin’s
                                                 transposition theorem is proved, which is used to generate an interpolant between
                                                 two mutually contradictory conjunctions of polynomial inequalities, using semi-
                                                 definite programming in time complexity O(n3 + nm)) with a given threshold,
                                                 where n is the number of variables and m is the number of inequalities. Using
                                                 the framework proposed by [21] for combining interpolants for a combination
                                                 of quantifier-free theories which have their own interpolation algorithms, a com-
                                                 bination algorithm is given for the combined theory of concave quadratic poly-
                                                 nomial inequalities and the equality theory over uninterpreted functions symbols
                                                 (EUF). The proposed approach is applicable to all existing abstract domains like
                                                 octagon, polyhedra, ellipsoid and so on, therefore it can be used to improve the
                                                 scalability of existing verification techniques for programs and hybrid systems. In
                                                 addition, we also discuss how to extend our approach to formulas beyond concave
                                                 quadratic polynomials using Gröbner basis.


                                         Keywords: Program verification, Interpolant, Concave quadratic polynomials, Motzin’s
                                         theorem, Semi-definite programming.
                                         1     Introduction
                                             Interpolants have been popularized by McMillan [15] for automatically generating
                                         invariants of programs. Since then, developing efficient algorithms for generating inter-
                                         polants for various theories has become an active area of research; in particular, methods
                                         have been developed for generating interpolants for Presburger arithmetic (both for in-
                                         tegers as well as for rationals/reals), theory of equality over uninterpreted symbols as
                                         well as their combination. Most of these methods assume the availability of a refutation
                                         proof of α ∧ β to generate a “reverse” interpolant of (α, β); calculi have been proposed
                                         to label an inference node in a refutational proof depending upon whether symbols
                                         of formulas on which the inference is applied are purely from α or β. For proposi-
                                         tional calculus, there already existed methods for generating interpolants from reso-
                                         lution proofs [11,16] prior to McMillan’s work, which generate different interpolants
from those done by McMillan’s method. This led D’Silva et al [6] to study strengths of
various interpolants.
     In Kapur, Majumdar and Zarba [10], an intimate connection between interpolants
and quantifier elimination was established. Using this connection, existence of quantifier-
free as well as interpolants with quantifiers were shown for a variety of theories over
container data structures. A CEGAR based approach was generalized for verification
of programs over container data structures using interpolants. Using this connection
between interpolant generation and quantifier elimination, Kapur [9] has shown that in-
terpolants form a lattice ordered using implication, with the interpolant generated from
α being the bottom of such a lattice and the interpolant generated from β being the top
of the lattice.
     Nonlinear polynomials inequalities have been found useful to express invariants for
software involving sophisticated number theoretic functions as well as hybrid systems;
an interested reader may see [27,28] where different controllers involving nonlinear
polynomial inequalities are discussed for some industrial applications.
     We propose an algorithm to generate interpolants for quadratic polynomial inequal-
ities (including strict inequalities). Based on the insight that for analyzing the solu-
tion space of concave quadratic polynomial (strict) inequalities, it suffices to linearize
them. We prove a generalization of Motzkin’s transposition theorem to be applicable
for quadratic polynomial inequalities (including strict as well as nonstrict). Based on
this result, we prove the existence of interpolants for two mutually contradictory con-
junctions α, β of concave quadratic polynomial inequalities and give an algorithm for
computing an interpolant using semi-definite programming. The algorithm is recur-
sive with the basis step of the algorithm relying on an additional condition on concave
quadratic polynomials appearing in nonstrict inequalities that any nonpositive constant
combination of these polynomials is never a nonzero sum of square polynomial (called
NSOSC). In this case, an interpolant output by the algorithm is either a strict in-
equality or a nonstrict inequality much like in the linear case. In case, this condition is
not satisfied by the nonstrict inequalities, i.e., there is a nonpositive constant combina-
tions of polynomials appearing as nonstrict inequalities that is a negative of a sum of
squares, then new mutually contradictory conjunctions of concave quadratic polynomi-
als in fewer variables are derived from the input augmented with the equality relation
deduced, and the algorithm is recursively invoked on the smaller problem. The out-
put of this algorithm is in general an interpolant that is a disjunction of conjunction of
polynomial nonstrict or strict inequalities. The NSOSC condition can be checked in
polynomial time using semi-definite programming.
     We also show how separating terms t− , t+ can be constructed using common sym-
bols in α, β such that α ⇒ t− ≤ x ≤ t+ and β ⇒ t+ ≤ y ≤ t− , whenever
(α ∧ β) ⇒ x = y. Similar to the construction for interpolants, this construction has
the same recursive structure with concave quadratic polynomials satisfying NSOSC as
the basis step. This result enables the use of the framework proposed in [17] based on
hierarchical theories and a combination method for generating interpolants by Yorsh
and Musuvathi, from combining equality interpolating quantifier-free theories for gen-
erating interpolants for the combined theory of quadratic polynomial inequalities and
theory of uninterpreted symbols.
    Obviously, our results are significant in program verification as all well-known ab-
stract domains, e.g. octagon, polyhedra, ellipsoid and so on, which are widely used in
the verification of programs and hybrid systems, are quadratic and concave. In addi-
tion, we also discuss the possibility to extend our results to general polynomial formu-
las by allowing polynomial equalities whose polynomials may be neither concave nor
quadratic using Gröbner basis.
    We develop a combination algorithm for generating interpolants for the combination
of concave quadratic polynomial inequalities and uninterpreted function symbols.
    In [5], Dai et al. gave an algorithm for generating interpolants for conjunctions of
mutually contradictory nonlinear polynomial inequalities based on the existence of a
witness guaranteed by Stengle’s Positivstellensatz [22] that can be computed using
semi-definite programming. Their algorithm is incomplete in general but if every vari-
ables ranges over a bounded interval (called Archimedean condition), then their algo-
rithm is complete. A major limitation of their work is that formulas α, β cannot have
uncommon variables4 . However, they do not give any combination algorithm for gener-
ating interpolants in the presence of uninterpreted function symbols appearing in α, β.
    The paper is organized as follows. After discussing some preliminaries in the next
section, Section 3 defines concave quadratic polynomials, their matrix representation
and their linearization. Section 4 presents the main contribution of the paper. A gen-
eralization of Motzkin’s transposition theorem for quadratic polynomial inequalities is
presented. Using this result, we prove the existence of interpolants for two mutually
contradictory conjunctions α, β of concave quadratic polynomial inequalities and give
an algorithm (Algorithm 2) for computing an interpolant using semi-definite program-
ming. Section 5 extends this algorithm to the combined theory of concave quadratic
inequalities and EUF using the framework used in [21,17]. Implementation and exper-
imental results using the proposed algorithms are briefly reviewed in Section 6, and we
conclude and discus future work in Section 7.

2      Preliminaries
    Let N, Q and R be the set of natural, rational and real numbers, respectively. Let
R[x] be the polynomial ring over R with variables x = (x1 , · · · , xn ). An atomic poly-
nomial formula ϕ is of the form p(x)  0, where p(x) ∈ R[x], and  can be any of
=, >, ≥, 6=; without any loss of generality, we can assume  to be any of >, ≥. An ar-
bitrary polynomial formula is constructed from atomic ones with Boolean connectives
and quantifications over real numbers. Let PT(R) be a first-order theory of polynomi-
als with real coefficient, In this paper, we are focusing on quantifier-free fragment of
PT(R).
    Later we discuss quantifier-free theory of equality of terms over uninterpreted func-
tion symbols and its combination with the quantifier-free fragment of PT(R). Let Σ
be a set of (new) function symbols. Let PT(R)Σ be the extension of the quantifier-free
theory with uninterpreted function symbols in Σ.
    For convenience, we use ⊥ to stand for false and > for true in what follows.

 4
     See however an expanded version of their paper under preparation where they propose heuris-
     tics using program analysis for eliminating uncommon variables.
Definition 1. A model M = (M, fM ) of PT(R)Σ consists of a model M of PT(R)
and a function fM : Rn → R for each f ∈ Σ with arity n.

Definition 2. Let φ and ψ be formulas of a considered theory T , then

 – φ is valid w.r.t. T , written as |=T φ, iff φ is true in all models of T ;
 – φ entails ψ w.r.t. T , written as φ |=T ψ, iff for any model of T , if ψ is true in the
   model, so is φ;
 – φ is satisfiable w.r.t. T , iff there exists a model of T such that in which φ is true;
   otherwise unsatisfiable.

Note that φ is unsatisfiable iff φ |=T ⊥.
    Craig showed that given two formulas φ and ψ in a first-order theory T such that
φ |= ψ, there always exists an interpolant I over the common symbols of φ and ψ
such that φ |= I, I |= ψ. In the verification literature, this terminology has been abused
following [15], where an reverse interpolant I over the common symbols of φ and ψ is
defined for φ ∧ ψ |= ⊥ as: φ |= I and I ∧ ψ |= ⊥.

Definition 3. Let φ and ψ be two formulas in a theory T such that φ ∧ ψ |=T ⊥. A
formula I said to be a (reverse) interpolant of φ and ψ if the following conditions hold:

  i φ |=T I;
 ii I ∧ ψ |=T ⊥; and
iii I only contains common symbols and free variables shared by φ and ψ.

    If ψ is closed, then φ |=T ψ iff φ ∧ ¬ψ |=T ⊥. Thus, I is an interpolant of φ and
ψ iff I is a reverse interpolant of φ and ¬ψ. In this paper, we just deal with reveres
interpolant, and from now on, we abuse interpolant and reverse interpolant.
2.1   Motzkin’s transposition theorem
    Motzkin’s transposition theorem [18] is one of the fundamental results about linear
inequalities; it also served as a basis of the interpolant generation algorithm for the
quantifier-free theory of linear inequalities in [17]. The theorem has several variants as
well. Below we give two of them.

Theorem 1 (Motzkin’s transposition theorem [18]). Let A and B be matrices and
let α and β be column vectors. Then there exists a vector x with Ax ≥ α and Bx > β,
iff

                  for all row vectors y, z ≥ 0 :
                  (i) if yA + zB = 0 then yα + zβ ≤ 0;
                  (ii) if yA + zB = 0 and z 6= 0 then yα + zβ < 0.

Corollary 1. Let A ∈ Rr×n and B ∈ Rs×n be matrices and α ∈ Rr and β ∈ Rs be
column vectors. Denote by Ai , i = 1, . . . , r the ith row of A and by Bj , j = 1, . . . , s
the jth row of B. Then there does not exist a vector x with Ax ≥ α and Bx > β, iff
there exist real numbers λ1 , . . . , λr ≥ 0 and η0 , η1 , . . . , ηs ≥ 0 such that
                      r
                      X                         s
                                                X
                            λi (Ai x − αi ) +         ηj (Bj x − βj ) + η0 ≡ 0,            (1)
                      i=1                       j=1
                      Xs
                            ηj > 0.                                                        (2)
                      j=0


Proof. The “if” part is obvious. Below we prove the “only if” part.
   By Theorem 1, if Ax ≥ α and Bx > β have no common solution, then there exist
two row vectors y ∈ Rr and z ∈ Rs with y ≥ 0 and z ≥ 0 such that

      (yA + zB = 0 ∧ yα + zβ > 0) ∨ (yA + zB = 0 ∧ z 6= 0 ∧ yα + zβ ≥ 0).

Let λi = yi , i = 1, . . . , r, ηj = zj , j = 1, . . . , s and η0 = yα + zβ. Then it is easy to
check that Eqs. (1) and (2) hold.                                                            t
                                                                                             u

3      Concave quadratic polynomials and their linearization
Definition 4 (Concave Quadratic). A polynomial f ∈ R[x] is called concave quadratic
(CQ), if the following two conditions hold:

 (i) f has total degree at most 2, i.e., it has the form f = xT Ax + 2αT x + a, where A
     is a real symmetric matrix, α is a column vector and a ∈ R is a constant;
(ii) the matrix A is negative semi-definite, written as A  0.5

Example 1. Let g1 = −x21 + 2x1 − x22 + 2x2 − y 2 , then it can be expressed as
                         T                 T  
                       x1      −1 0 0   x1        1    x1
                g1 =  x2   0 −1 0  x2  + 2 1  x2 .
                       y       0 0 −1   y         0    y
                                                          
                                                  −1 0 0
The degree of g1 is 2, and the corresponding A =  0 −1 0   0. Thus, g1 is CQ.
                                                   0 0 −1

    It is easy to see that if f ∈ R[x] is linear, then f is CQ because its total degree is 1
and the corresponding A is 0 which is of course negative semi-definite.
    A quadratic polynomial
                       can       also be represented as an inner product of matrices (cf.
                             1 xT
                                   
[13]), i.e., f (x) = P,                .
                             x xxT
 5
     A being negative semi-definite has many equivalent characterizations: for every vector x,
     xT Ax ≤ 0; every kth minor of A ≤ 0 if k is odd and ≥ 0 otherwise; a Hermitian matrix
     whose eigenvalues are nonpositive.
3.1     Linearization
      Consider quadratic polynomials fi and gj (i = 1, . . . , r, j = 1, . . . , s),

                                    fi = xT Ai x + 2αTi x + ai ,
                                    gj = xT Bj x + 2β Tj x + bj ,
                                                            n
where Ai, Bj are symmetric
     T
                          T
                             n × n matrices, αi , β j ∈ R , and ai , bj ∈ R; let Pi :=
  ai αi               bj β j
           , Qj :=             be (n + 1) × (n + 1) matrices, then
 α i Ai               β j Bj

                               1 xT                            1 xT
                                                              
              fi (x) = Pi ,              , gj (x)  =    Qj ,             .
                               x xxT                          x xxT

      For CQ polynomials fi s and gj s in which each Ai  0, Bj  0, define

        K = {x ∈ Rn | f1 (x) ≥ 0, . . . , fr (x) ≥ 0, g1 (x) > 0, . . . , gs (x) > 0}.    (3)

                                                    1 xT
                                                         
    Given a quadratic polynomial f (x) = P,                   , its linearization is defined
                                                    x xxT
             T                 T
                 1x                 1x
as f (x) = P,             , where               0.
                 xX                 xX
    Let

  X = (X (1,1) , X (2,1) , X (2,2) , . . . , X (k,1) , . . . , X (k,k) , . . . , X (n,1) , . . . , X (n,n) )

be the vector variable with n(n+1)
                                2   dimensions   corresponding to the matrix X. Since
                                    T
                                     
                                  1x
X is a symmetric matrix, P,               is a linear expression in x, X.
                                  xX
    Now, let
                             T                    T 
                              1x                         1x
                K1 = {x |              0, ∧ri=1 Pi ,              ≥ 0,
                              xX                         xX
                                       T 
                                        1x
                           ∧sj=1 Qj ,              > 0, for some X},              (4)
                                        xX

which is the set of all x ∈ Rn on linearizations of the above fi s and gj s.
     In [7,13], when K and K1 are defined only with fi without gj , i.e., only with non-
strict inequalities, it is proved that K = K1 . By the following Theorem 2, we show that
K = K1 also holds even in the presence of strict inequalities when fi and gj are CQ. So,
when fi and gj are CQ, the CQ polynomial inequalities can be transformed equivalently
to a set of linear inequality constraints and a positive semi-definite constraint.

Theorem 2. Let f1 , . . . , fr and g1 , . . . , gs be CQ polynomials, K and K1 as above,
then K = K1 .

Proof. For any x ∈ K, let X = xxT . Then it is easy to see that x, X satisfy (4). So
x ∈ K1 , that is K ⊆ K1 .
   Next, we prove K1 ⊆ K.         x ∈ K1 , then there exists a symmetric n × n matrix
                            LetT 
                            1x
X satisfying (4). Because            0, we have X − xxT  0. Then by the last two
                            xX
conditions in (4), we have

                       1 xT
                              T                                 
                                           1x                   0     0
      fi (x) = Pi ,               =  P i ,           +   P i ,
                       x xxT               xX                   0 xxT − X
                  T 
                       1x
             = Pi ,            + Ai , xxT − X ≥ Ai , xxT − X ,
                       xX
                        1 xT
                                       T                          
                                             1x                   0     0
      gj (x) = Qj ,               = Qj ,              + Qj ,
                        x xxT               xX                    0 xxT − X
                      T 
                        1x
             = Qj ,             + Bj , xxT − X > Bj , xxT − X .
                        xX

Since fi and gj are all CQ, Ai  0 and Bj  0. Moreover, X − xxT  0, i.e.,
xxT − X  0. Thus, Ai , xxT − X ≥ 0 and Bj , xxT − X ≥ 0. Hence, we have
fi (x) ≥ 0 and gj (x) > 0, so x ∈ K, that is K1 ⊆ K.                     t
                                                                         u

3.2   Motzkin’s theorem in Matrix Form
        T 
            1x
    If P,            is seen as a linear expression in x, X, then Corollary 1 can be
            xX
reformulated as:
Corollary 2. Let x be a column vector variable of dimension n and X be a n × n
symmetric matrix variable. Suppose P0 , P1 , . . . , Pr and Q1 , . . . , Qs are (n+1)×(n+1)
symmetric matrices. Let
                              T                                 T 
                        r         1x                    s               1x
       W ={(x,
          ˆ     X) | ∧i=1 Pi ,                  ≥ 0, ∧i=1 Qj ,                    > 0},
                                  xX                                    xX

then W = ∅ iff there exist λ0 , λ1 , . . . , λr ≥ 0 and η0 , η1 , . . . , ηs ≥ 0 such that
          r        T  X                  s         T 
         X               1x                              1x
              λ i Pi ,                +        ηj Qj ,                   + η0 ≡ 0, and
                         xX                              xX
            i=0                           j=1

           η0 + η1 + . . . + ηs > 0.

4     Algorithm for generating interpolants for Concave Quadratic Poly-
      nomial inequalities
Problem 1. Given two formulas φ and ψ on n variables with φ ∧ ψ |= ⊥, where

               φ = f1 ≥ 0 ∧ . . . ∧ fr1 ≥ 0 ∧ g1 > 0 ∧ . . . ∧ gs1 > 0,
               ψ = fr1 +1 ≥ 0 ∧ . . . ∧ fr ≥ 0 ∧ gs1 +1 > 0 ∧ . . . ∧ gs > 0,

in which f1 , . . . , fr , g1 , . . . , gs are all CQ, develop an algorithm to generate a (reverse)
Craig interpolant I for φ and ψ, on the common variables of φ and ψ, such that φ |= I
and I∧ψ |= ⊥. For convenience, we partition the variables appearing in the polynomials
above into three disjoint subsets x = (x1 , . . . , xd ) to stand for the common variables
appearing in both φ and ψ, y = (y1 , . . . , yu ) to stand for the variables appearing only in
φ and z = (z1 , . . . , zv ) to stand for the variables appearing only in ψ, where d+u+v =
n.




   Since linear inequalities are trivially concave quadratic polynomials, our algorithm
(Algorithm IGFQC in Section 4.4) can deal with the linear case too. In fact, it is a
generalization of the algorithm for linear inequalities.

     The proposed algorithm is recursive: the base case is when no sum of squares (SOS)
polynomial can be generated by a nonpositive constant combination of nonstrict in-
equalities in φ ∧ ψ. When this condition is not satisfied, i.e., an SOS polynomial can be
generated by a nonpositive constant combination of nonstrict inequalities in φ ∧ ψ, then
it is possible to identify variables which can be eliminated by replacing them by linear
expressions in terms of other variables and thus generate equisatisfiable problem with
fewer variables on which the algorithm can be recursively invoked.




                                               T 
                                                    1x
Lemma 1. Let U ∈ R(n+1)×(n+1) be a matrix. If U,            ≤ 0 for any x ∈ Rn
                                                    xX
                                    T
                                    1x
and symmetric matrix X ∈ Rn×n with           0 , then U  0.
                                    xX




Proof. Assume that U 6 0. Then there exists a column vector y = (y0 , y1 , . . . , yn )T ∈
Rn+1 such that c := yT U y = U, yyT > 0. Denote M = yyT , then M  0.

                                                                1 xT          1 xT
                                                                                      
    If y0 6= 0, then let x = ( yy01 , . . . , yyn0 )T , and X = xxT . Thus,
                                                            =           =
                                                                x xxT         xX
              T  D                                            T 
                1x                                                    1x
                              E
 1
y02
    M , and U,     = U, y12 M = yc2 > 0, which contradicts with U,       ≤
                xX         0       0                                 xX
0.
                                                   |U    |+1
   If y0 = 0, then M(1,1) = 0. Let M 0 = (1,1)   c  M , then M 0  0. Further, let
                         
              1 0 ··· 0
           0 0 · · · 0                                         T
 00      0                      00             00                  1x
M = M +  . . . . . Then M  0 and M (1,1) = 1. Let                  = M 00 , then
                         
            .. .. . . ..                                         xX
              0 0 ··· 0
                                                                   
                                            *           1 0 ··· 0 +
               T                                 0 0 · · · 0
                    1x
               U,           = hU, M 00 i = U, M 0 +  . . . . 
                                                                   
                    xX                                .. .. . . .. 
                                                        0 0 ··· 0
                                                                   
                              *                        1 0 ··· 0 +
                                   |U(1,1) | + 1     0 0 · · · 0
                            = U,                 M + . . . .
                                                                   
                                          c           .. .. . . .. 
                                                       0 0 ··· 0
                               |U(1,1) | + 1
                                   =         hU, M i + U(1,1)
                                     c
                            = |U(1,1) | + 1 + U(1,1) > 0,
                             T 
                                1x
which also contradicts with U,             ≤ 0. Thus, the assumption does not hold,
                                xX
that is U  0.                                                                   t
                                                                                 u
Lemma 2. Let A = {y ∈ Rm | Ai y − αi ≥ 0, Bj y − β j > 0, f or i = 1, . . . , r, j =
1, . . . , } be a nonempty set and B ⊆ Rm be an nonempty convex closed set. If A∩B = ∅
and there does not exist a linear form L(y) such that

                      ∀y ∈ A, L(y) > 0, and ∀y ∈ B, L(y) ≤ 0,                        (5)

then there is a linear form L0 (y) 6≡ 0 and δ1 , . . . , δr ≥ 0 such that
                             r
                             X
                  L0 (y) =         δi (Ai y − αi ) and ∀y ∈ B, L0 (y) ≤ 0.           (6)
                             i=1

Proof. Since A is defined by a set of linear inequalities, A is a convex set. Using
the separation theorem on disjoint convex sets, cf. e.g. [1], there exists a linear form
L0 (y) 6≡ 0 such that

                     ∀y ∈ A, L0 (y) ≥ 0, and ∀y ∈ B, L0 (y) ≤ 0.                     (7)

From (5) we have that

                                    ∃y0 ∈ A, L0 (y0 ) = 0.                           (8)

Since

                                       ∀y ∈ A, L0 (y) ≥ 0,                           (9)
then

                   A1 y − α1 ≥ 0 ∧ . . . ∧ Ar y − αr ≥ 0∧
                   B1 y − β1 > 0 ∧ . . . ∧ Bs y − βs > 0 ∧ −L0 (y) > 0

has no solution w.r.t. y. Using Corollary 1, there exist λ1 , . . . , λr ≥ 0, η0 , . . . , ηs ≥ 0
and η ≥ 0 such that
            r
            X                         s
                                      X
                  λi (Ai y − αi ) +         ηj (Bj y − βj ) + η(−L0 (y)) + η0 ≡ 0,          (10)
            i=1                       j=1
            Xs
                  ηj + η > 0.                                                               (11)
            j=0

Applying y0 in (8) to (10) and (11), it follows

                              η0 = η1 = . . . = ηs = 0, η > 0.

For i = 1, . . . , r, let δi = ληi ≥ 0, then
                             r
                             X
                L0 (y) =           δi (Ai y − αi ) and ∀y ∈ B, L0 (y) ≤ 0. t
                                                                           u
                             i=1

    The lemma below asserts the existence of a strict linear inequality separating A
and B defined above, for the case when any nonnegative constant combination of the
linearization of fi s is positive.
Lemma 3. Let A = {y ∈ Rm | Ai y − αi ≥ 0, Bj y − β j > 0, f or i = 1, . . . , r, j =
1, . . . , } be a nonempty set and B ⊆ Rm be an nonempty convex closed set, A ∩ B = ∅.
There exists a linear form L(x, X) such that

           ∀(x, X) ∈ A, L(x, X) > 0, and ∀(x, X) ∈ B, L(x, X) ≤ 0,
                                           Pr
whenever there does not exist λi ≥ 0, s.t., i=1 λi Pi  0.
Proof. Proof is by contradiction. Given that A is defined by a set of linear inequal-
ities and B is a closed convex nonempty set, by Lemma 2, there exist a linear form
L0 (x, X) 6≡ 0 and δ1 , . . . , δr ≥ 0 such that
                       r          T 
                     X                 1x
        L0 (x, X) =        δ i Pi ,              and ∀(x, X) ∈ B, L0 (x, X) ≤ 0.
                                       xX
                       i=1

I.e. there exists an symmetrical matrix L 6≡ 0 such that
                          T  X          r       T 
                              1x                         1x
                         L,            ≡       δ i Pi ,     ,                               (12)
                              xX                         xX
                                           i=1
                                       T 
                                             1x
                       ∀(x, X) ∈ B, L,                 ≤ 0.                                 (13)
                                            xX
                                                                Pr
Applying Lemma 1 to (13), it follows L  0. This implies that i=1 δi Pi = L 
Prwhich is in contradiction to the assumption that there does not exist λi ≥ 0, s.t.,
0,
   i=1 λi Pi  0                                                                  t
                                                                                  u

Definition 5. For given formulas φ and ψ as in Problem 1, it satisfies the non-existence
of an SOS condition (NSOSC) iff there do not exist δ1 ≥ 0, . . . , δr ≥ 0, such that
−(δ1 f1 + . . . + δr fr ) is a non-zero SOS.

    The following theorem gives a method for generating an interpolant when the con-
dition NSOSC holds by considering linearization of the problem and using Corollary
2. In that sense, this theorem is a generalization of Motzkin’s theorem to CQ polynomial
inequalities.
    The following separation lemma about a nonempty convex set A generated by linear
inequalities that is disjoint from another nonempty closed convex set B states that if
there is no strict linear inequality that holds over A and does not hold on any element
in B, then there is a hyperplane separating A and B, which is a nonnegative linear
combination of nonstrict inequalities.

Theorem 3. Let f1 , . . . , fr , g1 , . . . , gs are CQ polynomials and the K is defined as in
(3) with K = ∅. If the condition NSOSC holds, then there exist λi ≥ 0 (i = 1, · · · , r),
ηj ≥ 0 (j = 0, 1, · · · , s) and a quadratic SOS polynomial h ∈ R[x] such that
                                r
                                X                s
                                                 X
                                       λi fi +         ηj gj + η0 + h ≡ 0,                                (14)
                                 i=1             j=1

                                η0 + η1 + . . . + ηs = 1.                                                 (15)

    The proof uses the fact that if fi s satisfy the NSOSC condition, then the lineariza-
tion of fi s and gj s can be exploited to generate an interpolant expressed in terms of x.
The main issue is to decompose the result from the linearized problem into two compo-
nents giving an interpolant.

Proof. Recall from Section 3.1 that

                              1 xT                     1 xT
                                                       
                 fi = Pi ,             , gj =   Qj ,            .
                             x xxT                     x xxT

Let
                               1 xT                                            1 xT
                                                                                 
       A := {(x, X) | ∧ri=1
                          Pi ,                           ≥ 0, ∧sj=1       Qj ,               > 0},
                               xX                                              xX
                       T                                                                                (16)
                       1x
       B := {(x, X) |        0},
                       xX

be linearizations of the CQ polynomials fi s and gj s, where

  X = (X (1,1) , X (2,1) , X (2,2) , . . . , X (k,1) , . . . , X (k,k) , . . . , X (n,1) , . . . , X (n,n) ).

      By Theorem 2, A ∩ B = K1 = K = ∅.
   Since fi s satisfy the NSOSC condition, its linearization
                                                     satisfy  the condition of
                                                          1 xT
Lemma 3; thus there exists a linear form L(x, X) = L,            such that
                                                          xX

                              L(x, X) > 0, f or (x, X) ∈ A,                                  (17)
                              L(x, X) ≤ 0, f or (x, X) ∈ B.                                  (18)

   Applying Lemma 1, it follows L  0. Additionally, applying Lemma 2 to (17) and
denoting −L by P0 , there exist λ0 , λ1 , . . . , λr ≥ 0 and η0 , η1 , . . . , ηs ≥ 0 such that
             r       T  X                s            T 
            X              1x                              1x
               λ i Pi ,               +           ηj Qj ,                + η0 ≡ 0,
                           xX                              xX
               i=0                             j=1

              η0 + η1 + . . . + ηs > 0.
                               η
Let λi = Psλi ηj , ηj = Ps j ηj , then
             j=0              j=0

        T  Xr     T  X s         T 
         1x               1x              1x
 λ0 −U,       +   λi Pi ,    +   ηj Qj ,        + η0 ≡ 0,
         xX               xX              xX
                            i=1                                j=1
                                                                                             (19)
 η0 + η1 + . . . + ηs = 1.                                                                   (20)

Since for any x and symmetric matrix X, (19) holds, by setting X = xxT ,
                        r                           s
            1 xT                      1 xT                          1 xT
                 X                     X                        
λ0 −U,                +    λ i  P i ,           +     η j   Q j ,            + η0 ≡ 0,
            x xxT                     x xxT                         x xxT
                            i=1                                 j=1

which means that
                                    r
                                    X               s
                                                    X
                             h+           λi fi +         ηj gj + η0 ≡ 0,
                                    i=1             j=1

                   1 xT
                       
where h = λ0 −U,           . Since U  0, −U  0. Hence h is a quadratic SOS
                   x xxT
polynomial.                                                                t
                                                                           u
4.1   Base Case: Generating Interpolant when NSOSC is satisfied
    Using the above theorem, it is possible to generate an interpolant for φ and ψ from
the SOS polynomial h obtained using the theorem which can be split into two SOS
polynomials in the common variables of φ and ψ. This is proved in the following theo-
rem using some lemma as follows.
Lemma 4. Given a quadratic SOS polynomial h(x, y, z) ∈ R[x, y, z] on variables
x = (x1 , · · · , xd ) ∈ Rd ,y = (y1 , · · · , yu ) ∈ Ru and z = (z1 , · · · , zv ) ∈ Rv such that
the coefficients of yi zj (i = 1, · · · , u, j = 1, · · · , v) are all vanished when expanding
h(x, y, z), there exist two quadratic polynomial h1 (x, y) ∈ R[x, y] and h2 (x, z) ∈
R[x, z] such that h = h1 + h2 , moreover, h1 and h2 both are SOS.
Proof. Since h(x, y, z) is a quadratic polynomial and the coefficients of yi zj (i =
1, · · · , u, j = 1, · · · , v) are all vanished when expanding h(x, y, z), we have

       h(x, y1 , · · · , yu , z) = a1 y12 + b1 (x, y2 , · · · , yu )y1 + c1 (x, y2 , · · · , yu , z),

where a1 ∈ R, b1 (x, y2 , · · · , yu ) ∈ R[x, y2 , · · · , yu ] is a linear function and c1 (x, y2 , · · · , yu , z) ∈
R[x, y2 , · · · , yu , z] is a quadratic polynomial. Since h(x, y, z) is an SOS polynomial,
so

                  ∀(x, y1 , · · · , yu , z) ∈ Rd+u+v h(x, y1 , · · · , yu , z) ≥ 0.

Thus a1 = 0 ∧ b1 ≡ 0 or a1 > 0. If a1 = 0 ∧ b1 ≡ 0 then we denote

          p1 (x, y2 , · · · , yu , z) = c1 (x, y2 , · · · , yu , z), q1 (x, y1 , · · · , yu ) = 0;

otherwise, a1 > 0, and we denote
                                          b1                                                              b1 2
  p1 (x, y2 , · · · , yu , z) = h(x, −       , y2 , · · · , yu , z), q1 (x, y1 , · · · , yu ) = a1 (y1 +     ) .
                                         2a1                                                             2a1
Then, it is easy to see p1 (x, y2 , · · · , yu , z) is a quadratic polynomial satisfying

             h(x, y1 , · · · , yu , z) = p1 (x, y2 , · · · , yu , z) + q1 (x, y1 , · · · , yu ),

and

                ∀(x, y2 , · · · , yu , z) ∈ Rr+s−1+t p1 (x, y2 , · · · , yu , z) ≥ 0,

moreover, the coefficients of yi zj (i = 2, · · · , s, j = 1, · · · , t) are all vanished when
expanding p1 (x, y2 , · · · , yu , z), and q1 (x, y1 , · · · , yu ) ∈ R[x, y] is an SOS. With the
same reason, we can obtain p2 (x, y3 , · · · , yu , z), · · · , pu (x, z) and q2 (x, y2 , · · · , yu ),
· · · , qs (x, yu ) such that

           pi−1 (x, yi , · · · , yu , z) = pi (x, yi+1 , · · · , yu , z) + qi (x, yi , · · · , yu ),

                  ∀(x, yi+1 , · · · , yu , z) ∈ Rd+u−i+v pi (x, yi+1 , · · · , yu , z) ≥ 0,
                                                  qi (x, yi , · · · , yu ) is a SOS polynomial,

for i = 2, · · · , u. Therefore, let

         h1 (x, y) = q1 (x, y1 , · · · , yu ) + · · · + qs (x, yu ), h2 (x, z) = pu (x, z),

we have h1 (x, y) ∈ R[x, y] is an SOS and ∀(x, z) ∈ Rr+t h2 (x, z) = pu (x, z) ≥ 0.
Hence, h2 (x, z) is also an SOS, because that for the case of degree 2, a polynomial
is positive semi-definite iff it is an SOS polynomial. Thus h1 (x, y) ∈ R[x, y] and
h2 (x, z) ∈ R[x, z] are both SOS, moreover,
h1 + h2 = q1 + · · · + qu−1 + qu + pu = q1 + · · · + qu−1 + pu−1 = · · · = q1 + p1 = h. u
                                                                                        t

     The above proof of Lemma 4 gives a method to express h, h1 , h2 as sums of squares
of linear expressions and a nonnegative real number.
Lemma 5. Let h, h1 , h2 be as in the statement of Lemma 4. Then,

  (H) : h(x, y, z) =a1 (y1 − l1 (x, y2 , . . . , yu ))2 + . . . + au (yu − lu (x))2 +
                        au+1 (z1 − lu+1 (x, z2 , . . . , zv ))2 + . . . + au+v (zv − lu+v (x))2 +
                        au+v+1 (x1 − lu+v+1 (x2 , . . . , xd ))2 + . . . + au+v+d (xd − lu+v+d )2
                            + au+v+d+1 ,

 where ai ≥ 0 and lj is a linear expression in the corresponding variables, for i =
1, . . . , u + v + d + 1, j = 1, . . . , u + v + d. Further,

(H1) : h1 (x, y) = a1 (y1 − l1 (x, y2 , . . . , yu ))2 + . . . + au (yu − lu (x))2 +
       au+v+1                                                  au+v+d                   au+v+d+1
                (x1 − lu+v+1 (x2 , . . . , xd ))2 + . . . +           (xd − lu+v+d )2 +          ,
           2                                                     2                         2
(H2) : h2 (x, z) = au+1 (z1 − lu+1 (x, z2 , . . . , zv ))2 + . . . + au+v (zv − lu+v (x))2 +
       au+v+1                                               au+v+d                      au+v+d+1
                (x1 − lu+v+1 (x2 , . . . , xd ))2 + . . . +          (xd − lu+v+d )2 +           .
           2                                                    2                            2

Theorem 4. Let φ and ψ as defined in Problem 1 with φ ∧ ψ |= ⊥, which satisfy
NSOSC. Then there exist λi ≥ 0 (i = 1, · · · , r), ηj ≥ 0 (j = 0, 1, · · · , s) and two
quadratic SOS polynomial h1 ∈ R[x, y] and h2 ∈ R[x, z] such that
                             r
                             X               s
                                             X
                                   λi fi +          ηj gj + η0 + h1 + h2 ≡ 0,                                (21)
                             i=1             j=1

                             η0 + η1 + . . . + ηs = 1.                                                       (22)
            Ps1
Moreover, if j=0 η > 0, then I > 0 is an interpolant, otherwise I ≥ 0 is an inter-
                 Pjr1        Ps1
polant, where I = i=1 λi fi + j=1 ηj gj + η0 + h1 ∈ R[x].

Proof. From Theorem 3, there exist λi ≥ 0 (i = 1, · · · , r), ηj ≥ 0 (j = 0, 1, · · · , s)
and a quadratic SOS polynomial h ∈ R[x, y, z] such that
                                 r
                                 X                  s
                                                    X
                                         λ i fi +         ηj gj + η0 + h ≡ 0,                                (23)
                                   i=1              j=1

                                η0 + η1 + . . . + ηs = 1.                                                    (24)

Obviously, (23) is equivalent to the following formula
             r1
             X               s1
                             X                            r
                                                          X               s
                                                                          X
                   λi fi +         ηj gj + η0 +                λi fi +             ηj gj + h ≡ 0,
             i=1             j=1                     i=r1 +1             j=s1 +1

It’s easy to see that
      r1
      X               s1
                      X                                       r
                                                              X                  s
                                                                                 X
            λi fi +         ηj gj + η0 ∈ R[x, y],                     λi fi +             ηj gj ∈ R[x, z].
      i=1             j=1                                   i=r1 +1             j=s1 +1
Thus, for any 1 ≤ i ≤ u, 1 ≤ j ≤ v, the term yi zj does not appear in
                  r1
                  X               s1
                                  X                     r
                                                        X                   s
                                                                            X
                        λi fi +         ηj gj + η0 +             λi fi +             ηj gj .
                  i=1             j=1                  i=r1 +1             j=s1 +1

Since all the conditions in Lemma 4 are satisfied, there exist two quadratic SOS poly-
nomial h1 ∈ R[x, y] and h2 ∈ R[x, z] such that h = h1 + h2 . Thus, we have
        r1
        X               s1
                        X
              λi fi +         ηj gj + η0 + h1 ∈ R[x, y],
        i=1             j=1
         Xr                   s
                              X
                  λi fi +             ηj gj + h2 ∈ R[x, z],
        i=r1 +1             j=s1 +1
        Xr1             s1
                        X                              r
                                                       X                   s
                                                                           X
              λi fi +         ηj gj + η0 + h1 +              λi fi +              ηj gj + h2 ≡ 0
        i=1             j=1                       i=r1 +1              j=s1 +1

Besides, as
           r1
           X               s1
                           X                                r
                                                            X                    s
                                                                                 X
      I=         λi fi +         ηj gj + η0 + h1 = −(                λ i fi +             ηj gj + h2 ),
           i=1             j=1                             i=r1 +1              j=s1 +1

we have I ∈ R[x]. It is easy to see that
      Ps1
 – if j=0    ηj > 0 then φ |= I > 0 and ψ ∧ I > 0 |= ⊥, so I > 0 is an interpolation;
    andP
         s
 – if j=s1 +1 ηj > 0 then φ |= I ≥ 0 and ψ ∧ I ≥ 0 |= ⊥, hence I ≥ 0 is an
    interpolation.                                                                 t
                                                                                   u
4.2   Computing Interpolant using Semi-Definite Programming
   Below, we formulate computing λi s, ηj s and h1 and h2 as a semi-definite program-
ming problem.
   Let
                                  1 x T y T zT
                                                    
                                x xxT xyT xzT 
                          W =  y yxT yyT yzT 
                                                     

                                  z zxT zyT zzT

                                   fi = hPi , W i, gj = hQj , W i,                                        (25)
where Pi and Qj are (1 + d + u + v) × (1 + d + u + v) matrices, and

                                  h1 = hM, W i, h2 = hM̂ , W i,

where M = (Mij )4×4 , M̂ = (M̂ij )4×4 with appropriate dimensions, for example
M12 ∈ R1×d and M̂34 ∈ Ru×v . Then, with NSOSC, by Theorem 4, Problem 1 is
reduced to the following SDP feasibility problem.
   Find:
                λ1 , . . . , λr , η0 , . . . , ηs ∈ R and real symmetric matrices
                                M, M̂ ∈ R(1+d+u+v)×(1+d+u+v)
subject to
    Pr               Ps                                      Ps
          i=1 λi Pi +   j=1 ηj Qj + η0 E1,1 + M + M̂ = 0,       j=0 ηj = 1,
   
   
   
    M41 = (M14 )T = 0, M42 = (M24 )T = 0, M43 = (M34 )T = 0, M44 = 0,
   
                      T                    T                                 T
    M̂31 = (M̂13 ) = 0, M̂32 = (M̂23 ) = 0, M̂33 = 0, M̂34 = (M̂43 ) = 0,
   
   
   
      M  0, M̂  0, λi ≥ 0, ηj ≥ 0, for i = 1, . . . , r, j = 0, . . . , s,
   

where E1,1 is a (1 + d + u + v) × (1 + d + u + v) matrix, whose (1, 1) entry is 1 and
the others are 0.
    This is a standard SDP feasibility problem, which can be solved efficiently by
well known SDP solvers, e.g., CSDP [3], SDPT3 [23], SeDuMi [19], etc., with time
complexity polynomial in n = d + u + v.

Remark 1. Problem 1 is a typical quantifier elimination (QE) problem, which can be
solved symbolically. However, it is very hard to solve large problems by general QE
algorithms because of their high complexity. So, reducing Problem 1 to SDP problem
makes it possible to solve many large problems in practice. Nevertheless, one may doubt
whether we can use numerical result in verification. We think that verification must be
rigorous and numerical results should be verified first. For P example, after
                                                                            Psolving the
                                                                 r            s
above SDP problem numerically, we verify that whether −( i=1 λi fi + j=1 ηj gj +
η0 ) is an SOS by the method of Lemma 5, which is easy to do. If it is, the result is
guaranteed and output. If not, the result is unknown (in fact, some other techniques can
be employed in this case, which we do not discuss in this paper.). Thus, our algorithm
is sound but not complete.

4.3   General Case
    The case of Var(φ) ⊂ Var(ψ) is not an issue since φ serves as an interpolant of φ
and ψ. We thus assume that Var(φ) * Var(ψ). We show below how an interpolant can
be generated in the general case. If φ and ψ do not satisfy the NSOSC condition, i.e.,
an SOS polynomial h(x, y, z) can be computed from nonstrict inequalities fi s using
nonpositive constant multipliers, then by the lemma below, we can construct “simpler”
interpolation subproblems φ0 , ψ 0 from φ and ψ by constructing from h an SOS polyno-
mial f (x) such that φ |= f (x) ≥ 0 as well as ψ |= −f (x) ≥ 0. Each φ0 ψ 0 pair has
the following characteristics because of which the algorithm is recursively applied to φ0
and ψ 0 .
  (i) φ0 ∧ ψ 0 |= ⊥,
 (ii) φ0 , ψ 0 have the same form as φ, ψ, i.e., φ0 and ψ 0 are defined by some fi0 ≥ 0 and
      gj0 > 0, where fi0 and gj0 are CQ,
(iii) #(Var(φ0 )∪Var(ψ 0 )) < #(Var(φ)∪Var(ψ)) to ensure termination of the recursive
      algorithm, and
(iv) an interpolant I for φ and ψ can be computed from an interpolant I 0 for φ0 and ψ 0
      using f .
Lemma 6. If Problem 1 does not satisfy the NSOSC condition, there exists f ∈ R[x],
such that φ ⇔ φ1 ∨ φ2 and ψ ⇔ ψ1 ∨ ψ2 , where,

                        φ1 = (f > 0 ∧ φ), φ2 = (f = 0 ∧ φ),                                  (26)
                        ψ1 = (−f > 0 ∧ ψ), ψ2 = (f = 0 ∧ ψ).                                 (27)
                                                                                Pr
Proof. Since NSOSC does not hold, there exist δ1 , . . . , δr ∈ R+ such that − i=1 δi fi
              Pr1 Let h(x, y, z) denote thisP
is a nonzero SOS.                             quadratic SOS polynomial.
                                               r
     Since (− i=1    δi fi ) ∈ R[x, y] and (− i=r1 +1 δi fi ) ∈ R[x, z], the coefficient of
any term yi zj , 1 ≤ i ≤ u, 1 ≤ j ≤ v, is 0 after expanding h. By Lemma 4 there exist
two quadratic SOS polynomials h1 ∈ R[x, y] and h2 ∈ R[x, z] such that h = h1 + h2
with the following form:

(H1) : h1 (x, y) = a1 (y1 − l1 (x, y2 , . . . , yu ))2 + . . . + au (yu − lu (x))2 +
       au+v+1                                                au+v+d                    au+v+d+1
               (x1 − lu+v+1 (x2 , . . . , xd ))2 + . . . +           (xd − lu+v+d )2 +          ,
          2                                                     2                         2

(H2) : h2 (x, z) = au+1 (z1 − lu+1 (x, z2 , . . . , zv ))2 + . . . + au+v (zv − lu+v (x))2 +
       au+v+1                                              au+v+d                      au+v+d+1
               (x1 − lu+v+1 (x2 , . . . , xd ))2 + . . . +           (xd − lu+v+d )2 +          .
          2                                                    2                            2
Let
                              r1
                              X                       r
                                                      X
                        f=          δi fi + h1 = −             δi fi − h2 .                  (28)
                              i=1                    i=r1 +1


Obviously, f ∈ R[x, y] and f ∈ R[x, z], this implies f ∈ R[x].
   Since h1 , h2 are SOS, it is easy to see that φ |= f (x) ≥ 0, ψ |= −f (x) ≥ 0. Thus,
φ ⇔ φ1 ∨ φ2 , ψ ⇔ ψ1 ∨ ψ2 .                                                          t
                                                                                     u

    Using the above lemma, an interpolant I for φ and ψ can be constructed from an
interpolant I2,2 for φ2 and ψ2 .

Theorem 5. Let φ, ψ, φ1 , φ2 , ψ1 , ψ2 as defined in Lemma 6, then given an interpolant
I2,2 for φ2 and ψ2 , I := (f > 0) ∨ (f ≥ 0 ∧ I2,2 ) is an interpolant for φ and ψ.

Proof. It is easy to see that f > 0 is an interpolant for both (φ1 , ψ1 ) and (φ1 , ψ2 ), and
f ≥ 0 is an interpolant for (φ2 , ψ1 ). Thus, if I2,2 is an interpolant for (φ2 , ψ2 ), then I
is an interpolant for φ and ψ.                                                              t
                                                                                            u

    An interpolant for φ2 and ψ2 is constructedP   recursively since the new constraint
                                                     r1
included in φ2 (similarly, as well as in ψ2 ) is: i=1   δi fi + h1 = 0 with h1 being
               0       0
an SOS. Let φ and ψ stand for the formulas constructed after analyzing φ2 and ψ2
respectively. Given that δi as well as fi ≥ 0 for each i, case analysis is performed on
h1 depending upon whether it has a positive constant au+v+d+1 > 0 or not.

Theorem 6. Let φ0 =(0
                  ˆ > 0) and ψ 0 =(0ˆ > 0). In the proof of Lemma 6, if au+v+d+1 >
         0     0
0, then φ and ψ satisfy (i) − (iv).
Proof. (i), (ii) and (iii) are trivially satisfied. Since au+v+d+1 > 0, it is easy to see
that h1 > 0 and h2 > 0. From (26), (27) and (28), we have φ2 |= h1 = 0, and
ψ2 |= h2 = 0. Thus φ2 ⇔ φ0 ⇔ ⊥ and ψ2 ⇔ ψ 0 ⇔ ⊥.                                       t
                                                                                       u

    In case au+v+d+1 = 0, from the fact that h1 is an SOS and has the form (H1), each
nonzero square term in h1 is identically 0. This implies that some of the variables in
x, y can be linearly expressed in term of other variables; the same argument applies to
h2 as well. In particular, at least one variable is eliminated in both φ2 and ψ2 , reducing
the number of variables appearing in φ and ψ, which ensures the termination of the
algorithm. A detailed analysis is given in following lemmas, where it is shown how this
elimination of variables is performed, generating φ0 and ψ 0 on which the algorithm can
be recursively invoked; an a theorem is also proved to ensures this.

Lemma 7. In the proof of Lemma 6, if au+v+d+1 = 0, then x can be represented as
(x1 , x2 ), y as (y1 , y2 ) and z as (z1 , z2 ), such that
                                 2
                            1    x
                 φ2 |= ((y = Λ1      + γ1 ) ∧ (x1 = Λ3 x2 + γ3 )),
                                 y2
                                 2
                          1      x
                 ψ2 |= ((z = Λ2      + γ2 ) ∧ (x1 = Λ3 x2 + γ3 )),
                                 z2

and #(Var(x1 )+Var(y1 )+Var(z1 )) > 0, for matrixes Λ1 , Λ2 , Λ3 and vectors γ1 , γ2 , γ3 .

Proof. From (26), (27) and (28) we have

                                φ2 |= h1 = 0,     ψ2 |= h2 = 0.                       (29)

Since h1 + h2 = h is a nonzero polynomial, au+v+d+1 = 0 , then there exist some
ai 6= 0, i.e. ai > 0, for 1 ≤ i ≤ u + v + d. Let

                         N1 := {i | ai > 0 ∧ 1 ≤ i ≤ u},
                         N2 := {i | au+i > 0 ∧ 1 ≤ i ≤ v},
                         N3 := {i | au+v+i > 0 ∧ 1 ≤ i ≤ d}.

Thus, N1 , N2 and N3 cannot all be empty. In addition, h1 = 0 implies that

                       yi = li (x, yi+1 , . . . , yu ),   f or i ∈ N1 ,
                       xi = lu+v+i (xi+1 , . . . , zd ), f or i ∈ N3 .

Also, h2 = 0 implies that

                       zi = lu+i (x, zi+1 , . . . , zv ), f or i ∈ N2 ,
                       xi = lu+v+i (xi+1 , . . . , zd ), f or i ∈ N3 .
Now, let

       y1 = (yi1 , . . . , yi|N1 | ), y2 = (yj1 , . . . , yju−|N1 | ),
              where {i1 , . . . , i|N1 | } = N1 , {j1 , . . . , ju−|N1 | } = {1, . . . , u} − N1 ,
       z = (zi1 , . . . , zi|N2 | ), z2 = (zj1 , . . . , zju−|N2 | ),
        1

              where {i1 , . . . , i|N2 | } = N2 , {j1 , . . . , jv−|N2 | } = {1, . . . , v} − N2 ,
       x = (xi1 , . . . , xi|N3 | ), x2 = (xj1 , . . . , xju−|N3 | ),
         1

              where {i1 , . . . , i|N3 | } = N3 , {j1 , . . . , jd−|N3 | } = {1, . . . , d} − N3 .

Clearly, #(Var(x1 ) + Var(y1 ) + Var(z1 )) > 0. By linear algebra, there exist three
matrices Λ1 , Λ2 , Λ3 and three vectors γ1 , γ2 , γ3 s.t.
                                                 2
                                                 x
                                        y1 = Λ1      + γ1 ,
                                                 y2
                                                 2
                                                 x
                                        z1 = Λ2      + γ2 ,
                                                 z2
                                        x1 = Λ3 x2 + γ3 .

Since φ2 |= h1 = 0,         ψ2 |= h2 = 0, then,
                                    2
                                1   x
                   φ2 |= ((y = Λ1       + γ1 ) ∧ (x1 = Λ3 x2 + γ3 )),
                                    y2
                                    2
                                    x
                   ψ2 |= ((z1 = Λ2      + γ2 ) ∧ (x1 = Λ3 x2 + γ3 )).
                                    z2

                                                                                                     t
                                                                                                     u
                                                                                  2
                                                                                   x
    So, replacing (x1 , y1 ) in fi (x, y) and gj (x, y) by Λ3 x2 + γ3 Λ1                + γ1 re-
                                                                                   y2
spectively, results in new polynomials fˆi (x2 , y2 ) and gˆj (x2 , y2 ), for i = 1, . . . , r1 ,
j =1, .. . , s1 . Similarly, replacing (x1 , z1 ) in fi (x, z) and gj (x, z) by Λ3 x2 + γ3 and
       2
     x
Λ2           + γ2 respectively, derives new polynomials fˆi (x2 , z2 ) and gˆj (x2 , z2 ), for
     z2
i = r1 + 1, . . . , r, j = s1 + 1, . . . , s. Regarding the resulted polynomials above, we
have the following property.

                                                                     T  
                          m               n                            ξ        ξ
Lemma 8. Let ξ ∈ R and ζ ∈ R be two vector variables, g(ξ, ζ) =             G      +
                                                                     ζ        ζ
      ξ
aT         + α be a CQ polynomial on (ξ, ζ), i.e. G  0. Replacing ζ in g by Λξ + γ
      ζ
derives ĝ(ξ) = g(ξ, Λξ + γ), then ĝ(ξ) is a CQ polynomial in ξ.
                          T  
                           ξ         ξ
Proof. G  0 iff −              G      is an SOS. Thus, there exist li,1 ∈ Rm , li,2 ∈ Rn ,
                           ζ         ζ
                                   T  
                                   ξ        ξ       Ps
for i = 1, . . . , s, s ∈ N+ s.t.      G       = − i=1 (li,1T       T
                                                               ξ + li,2 ζ)2 . Hence,
                                   ζ        ζ
                         T                             s
                   ξ                     ξ                 X
                                                               T        T
                               G                    =−       (li,1 ξ + li,2 (Λξ + γ))2
                 Λξ + γ                Λξ + γ
                                                           i=1
                                                   s
                                                   X
                                                        T      T          T
                                                =−   ((li,1 + li,2 Λ)ξ + li,2 γ)2
                                                      i=1
                                                      s
                                                      X
                                                               T      T
                                                =−          ((li,1 + li,2 Λ)ξ)2 + l(ξ),
                                                      i=1


where l(ξ) is a linear function in ξ. Then we have
                        s                                                           
                        X
                                 T      T                                     ξ
            ĝ(ξ) = −         ((li,1 + li,2 Λ)ξ)2 + l(ξ) + αT                            + α.
                                                                            Λξ + γ
                        i=1


Obviously, there exist Ĝ  0, α̂ and α̂ such that

                                       ĝ = ξ Ĝξ T + α̂T ξ + α̂.

Therefore, ĝ is concave quadratic polynomial in ξ.                                             t
                                                                                                u

Theorem 7. In the proof of Lemma 6, if au+v+d+1 = 0, then Lemma 7 holds. So, let fˆi
and gˆj as above, and

                                   r1
                                   ^                 s1
                                                     ^
                           φ0 =          fˆi ≥ 0 ∧         gˆj > 0,
                                   i=1               j=1
                                     ^r                      s
                                                             ^
                           ψ0 =              fˆi ≥ 0 ∧               gˆj > 0.
                                   i=r1 +1                 j=s1 +1


Then φ0 and ψ 0 satisfy (i) − (iv).

Proof. From Lemma 7, we have
                                 2
                               1 x
                 φ2 |= ((y = Λ1      + γ1 ) ∧ (x1 = Λ3 x2 + γ3 )),
                                 y2
                                 2
                          1      x
                 ψ2 |= ((z = Λ2      + γ2 ) ∧ (x1 = Λ3 x2 + γ3 )).
                                 z2
Let
                                2
                                x
                φ02 := ((y1 = Λ1    + γ1 ) ∧ (x1 = Λ3 x2 + γ3 ) ∧ φ),
                                y2
                                2
                 0       1      x
                ψ2 := ((z = Λ2      + γ2 ) ∧ (x1 = Λ3 x2 + γ3 ) ∧ ψ).
                                z2



Then φ2 |= φ02 , φ2 |= φ02 and φ02 ∧ ψ20 |= ⊥. Thus any interpolant for φ02 and ψ20 is also
an interpolant of φ2 and ψ2 .
                                                                    0    0
    By the definition of φ0 and ψ 0 , it follows φ0 ∧ ψ 0 |= ⊥ iff φ2 ∧ ψ2 |= ⊥, so φ0 ∧ ψ 0 |=
⊥, (i) holds.
    Moreover, φ2 0 |= φ0 , ψ2 0 |= ψ 0 , Var(φ0 ) ⊆ Var(φ2 0 ) and Var(ψ 0 ) ⊆ Var(ψ2 0 ),
then any interpolant for φ0 and ψ 0 is also an interpolant for φ2 0 and ψ2 0 , then also an
interpolant for φ2 and ψ2 . By Theorem 5, (iii) holds.
    Since #(Var(φ) + Var(ψ)) − #(Var(φ0 ) + Var(ψ 0 )) = #(x1 , y1 , z1 ) > 0, then
(vi) holds.
    For (ii), φ0 , ψ 0 have the same form with φ, ψ, means that fˆi , i = 1, . . . , r are CQ
and gˆj , j = 1, . . . , s are CQ. This is satisfied directly by Lemma 8.                     t
                                                                                              u

      The following simple example illustrates how the above construction works.

Example 2. Let f1 = x1 , f2 = x2 , f3 = −x21 − x22 − 2x2 − z 2 , g1 = −x21 + 2x1 −
x22 + 2x2 − y 2 . Two formulas φ := (f1 ≥ 0) ∧ (f2 ≥ 0) ∧ (g1 > 0), ψ := (f3 ≥ 0).
φ ∧ ψ |= ⊥.
    The condition NSOSC does not hold, since

                −(0f1 + 2f2 + f3 ) = x21 + x22 + z 2 is a sum of square.

Then we have h = x21 + x22 + z 2 , and

                              1 2 1 2      1     1
                       h1 =    x + x , h2 = x21 + x22 + z 2 .                             (30)
                              2 1 2 2      2     2

Let f = 0f1 + 2f2 + h1 = 12 x21 + 12 x22 + 2x2 .
    For the recursive call, we have f = 0 as well as x1 = 0, x2 = 0 from h1 = 0 to
construct φ0 from φ; similarly ψ 0 is constructing by setting x1 = x2 = 0, z = 0 in ψ as
derived from h2 = 0.
                                                             0
                φ0 = 0 ≥ 0 ∧ 0 ≥ 0 ∧ −y 2 > 0 = ⊥, ψ = 0 ≥ 0 = >.

Thus, I(φ0 , ψ 0 ) := (0 > 0) is an interpolant for (φ0 , ψ 0 ).
    An interpolant for φ and ψ is thus (f (x) > 0) ∨ (f (x) = 0 ∧ I(φ0 , ψ 0 )), which is
1 2    1 2
2 x1 + 2 x2 + 2x2 > 0.
 Algorithm 1: IGFCH
      input : Two formulas φ, ψ with NSOSC and φ ∧ ψ |= ⊥, where
             φ = f1 ≥ 0 ∧ . . . ∧ fr1 ≥ 0 ∧ g1 > 0 ∧ . . . ∧ gs1 > 0,
             ψ = fr1 +1 ≥ 0 ∧ . . . ∧ fr ≥ 0 ∧ gs1 +1 > 0 ∧ . . . ∧ gs > 0,
             f1 , . . . , fr , g1 , . . . , gs are all concave quadratic polynomials,
             f1 , . . . , fr1 , g1 , . . . , gs1 ∈ R[x, y], fr1 +1 , . . . , fr , gs1 +1 , . . . , gs ∈ R[x, z]
      output: A formula I to be a Craig interpolant for φ and ψ
 1    Find λ1 , . . . , λr ≥ 0, η0 , η1 , . . . , ηs ≥ 0, h1 ∈ R[x, y], h2 ∈ R[x, z] by SDP s.t.
                                   r
                                   X               s
                                                   X
                                         λi gj +         ηj gj + η0 + h1 + h2 ≡ 0,
                                   i=1             j=1

                                   η0 + η1 + . . . + ηs = 1,
                                   h1 , h2 are SOS polynomial;

   /* This
        P 1 is essentially          a SDP problem, see Section 4.1                                                */
   f := ri=1   λi gj + sj=1
                      P1
 2                          ηj gj + η0 + h1 ;
      Ps1
 3 if   j=0 ηj > 0 then I := (f > 0); else I := (f ≥ 0);
 4 return I




4.4     Algorithms
    Algorithm IGFCH deals with the case when φ and ψ satisfy the NSOSC condi-
tion.

Theorem 8 (Soundness and Completeness of IGFCH). IGFCH computes an in-
terpolant I of mutually contradictory φ, ψ with CQ polynomial inequalities satisfying
the NSOSC condition .

Proof. It is guaranteed by Theorem 4.                                                                                  t
                                                                                                                       u

    The recursive algorithm IGFCH is given below. For the base case when φ, ψ sat-
isfy the NSOSC condition, it invokes IGFCH.

Theorem 9 (Soundness and Completeness of IGFQC). IGFQC computes an in-
terpolant I of mutually contradictory φ, ψ with CQ polynomial inequalities.

Proof. If Var(φ) ⊆ Var(ψ), IGFQC terminates at step 1, and returns φ as an inter-
polant. Otherwise, there are two cases:
    (i) If NSOSC holds, then IGFQC terminates at step 3 and returns an interpolant
for φ and ψ by calling IGFCH. Its soundness and completeness follows from the
previous theorem.
    (ii) Var(φ) * Var(ψ) and NSOSC does not hold: The proof is by induction on the
number of recursive calls to IGFQC, with the case of 0 recursive calls being (i) above.
    In the induction step, assume that for a k th -recursive call to IGFQC gives a correct
interpolant I 0 for φ0 and ψ 0 , where φ0 and ψ 0 are constructed by Theorem 6 or Theorem
7.
  Algorithm 2: IGFQC
      input : Two formulas φ, ψ with φ ∧ ψ |= ⊥, where
             φ = f1 ≥ 0 ∧ . . . ∧ fr1 ≥ 0 ∧ g1 > 0 ∧ . . . ∧ gs1 > 0,
             ψ = fr1 +1 ≥ 0 ∧ . . . ∧ fr ≥ 0 ∧ gs1 +1 > 0 ∧ . . . ∧ gs > 0,
             f1 , . . . , fr , g1 , . . . , gs are all CQ polynomials,
             f1 , . . . , fr1 , g1 , . . . , gs1 ∈ R[x, y], and fr1 +1 , . . . , fr , gs1 +1 , . . . , gs ∈ R[x, z]
      output: A formula I to be a Craig interpolant for φ and ψ
 1 if Var(φ) ⊆ Var(ψ) then I := φ; return I;
   Find δ1 , . . . , δr ≥ 0, h ∈ R[x, y, z] by SDP s.t. ri=1 δi fi + h ≡ 0 and h is SOS;
                                                       P
 2
   /* Check the condition NSOSC                                                          */
 3 if no solution then I := IGFCH(φ, ψ); return I;
   /* NSOSC holds                                                                        */
 4 Construct h1 ∈ R[x, y] and h2 ∈ R[x, z] with the forms (H1) and (H2);
         Pr1                      Pr
 5 f :=     i=1 δi fi + h1 = −      i=r1 δi fi − h2 ;
                  0       0
 6 Construct φ and ψ using Theorem 6 and Theorem 7 by eliminating variables due to
   h1 = h2 = 0;
     0                  0   0
 7 I = IGFQC(φ , ψ );
                                  0
 8 I := (f > 0) ∨ (f ≥ 0 ∧ I );
 9 return I




      By Theorem 7, the interpolant I constructed from I 0 is the correct answer for φ and
ψ.
    The recursive algorithm terminates in all three cases: (i) Var(φ) ⊆ Var(ψ), (ii)
NSOSC holds, which is achieved at most u + v + d times by Theorem 7, and (iii) the
number of variables in φ0 , ψ 0 in the recursive call is smaller than the number of variables
in φ, ψ.
                                                                                           t
                                                                                           u

4.5     Complexity analysis of IGFCH and IGFQC
   It is well known that an SDP problem can be solved in polynomial time complexity.
We analyze the complexity of the above algorithms assuming that the complexity of an
SDP problem is of time complexity g(k), where k is the input size.

Theorem 10. The complexity of IGFCH is O(g(r + s + n2 )), where r is the number
of nonstrict inequalities fi s and s is the number of strict inequalities gj s, and n is the
number of variables in fi s and gj s.

Proof. In this algorithm we first need to solve a constraint solving problem in step 1,
see Section 4.1, it is an SDP problem with size O(r+s+n2 ), so the complexity of step
1 is O(g(r + s + n2 )). Obviously, the complexity of steps 2 − 4 is linear in (r + s + n2 ),
so the complexity of IGFCH is O(g(r + s + n2 )).                                         t
                                                                                         u

Theorem 11. The complexity of IGFQC is O(n ∗ g(r + s + n2 )), where r, s, n are as
defined in the previous theorem.
Proof. The algorithm IGFQC is a recursive algorithm, which is called at most n times,
since in every recursive call, at least one variable gets eliminated. Finally, it terminates
at step 1 or step 3 with complexity O(g(r + s + n2 )).
     The complexity of each recursive call, i.e., the complexity for step 2 and steps 4 − 9,
can be analyzed as follows:
     For step 2, checking if NSOSC holds is done by solving theP        following problem:
                                                                          r
find: δ1 , . . . , δr ≥ 0, and an SOS polynomial h ∈ R[x, y, z] s.t. i=1 δi fi + h ≡ 0,
which is equivalent to the following linear matrix inequality    P(LMI),
                                                                   r
find: δ1 , . . . , δr ≥ 0, M ∈ R(n+1×(n+1) , s.t. M = − i=1 δi Pi , M  0, where
          (n+1)×(n+1)
Pi ∈ R                     is defined as (25). Clearly, this is an SDP problem with size
O(r + n2 ), so the complexity of this step is O(g(r + n2 )).
     For steps 4 − 9, by the proof of Lemma 4, it is easy to see that to represent h in the
form (H) in Lemma 5 can be done with complexity O(n2 ), h1 and h2 can be computed
with complexity O(n2 ). Thus, the complexity of step 4 is O(n2 ). Step 5 is much easy.
For step 6, using linear algebra operations, it is easy to see that the complexity is O(n2 +
r + s). So, the complexity is O(n2 + r + s) for step 4 − 9.
     In a word, the overall complexity of IGFQC is
              O(g(r + s + n2 )) + nO(n2 + r + s) = O(n ∗ g(r + s + n2 )).
                                                                                               t
                                                                                               u
5      Combination: quadratic concave polynomial inequalities with un-
       interpreted function symbols (EUF)
    This section combines the quantifier-free theory of quadratic concave polynomial
inequalities with the theory of equality over uninterpreted function symbols (EUF).
The proposed algorithm for generating interpolants for the combined theories is pre-
sented in Algorithm 6. As the reader would observe, it is patterned after the algorithm
INTERLI(Q)Σ in Figure 4 in [17] following the hierarchical reasoning and interpolation
generation framework in [21] with the following key differences6 :
 1. To generate interpolants for mutually contradictory conjunctions of CQ polynomial
    inequalities, we call IGFQC.
 2. We prove below that (i) a nonlinear equality over polynomials cannnot be generated
    from CQ polynomials, and furthermore (ii) in the base case when the NSOSC
    condition is satisfied by CQ polynomial inequalities, linear equalities are deduced
    only from the linear inequalities in a problem (i.e., nonlinear inequalities do not
    play any role); separating terms for mixed equalities are computed the same way
    as in the algorithm SEP in [17], and (iii) as shown in Lemmas 4, 5 and Theorem 7,
    during recursive calls to IGFQC, additional linear unmixed equalities are deduced
    which are local to either φ or ψ, we can use these equalities as well as those in
    (ii) for the base case to reduce the number of variables appearing in φ and ψ thus
    reducing the complexity of the algorithm; equalities relating variables of φ are also
    included in the interpolant.
 6
     The proposed algorithm andd its way of handling of combined theories do not crucially depend
     upon using algorithms in [17]; however, adopting their approach makes proofs and presenta-
     tion easier by focusing totally on the quantifier-free theory of CQ polynomial inequalities.
Other than that, the proposed algorithm reduces to INTERLI(Q)Σ if φ, ψ are purely
from LI(Q) and/or EUF.
    In order to get directly to the key concepts used, we assume the reader’s familiarity
with the basic construction of flattening and purification by introducing fresh variables
for the arguments containing uninterpreted functions.
5.1     Problem Formulation
    Let Ω = Ω1 ∪ Ω2 ∪ Ω3 be a finite set of uninterpreted function symbols in EUF;
further, denote Ω1 ∪ Ω2 by Ω12 and Ω1 ∪ Ω3 by Ω13 . Let R[x, y, z]Ω be the extension
of R[x, y, z] in which polynomials can have terms built using function symbols in Ω
and variables in x, y, z.

Problem 2. Suppose two formulas φ and ψ with φ ∧ ψ |= ⊥, where φ = f1 ≥
0 ∧ . . . ∧ fr1 ≥ 0 ∧ g1 > 0 ∧ . . . ∧ gs1 > 0, ψ = fr1 +1 ≥ 0 ∧ . . . ∧ fr ≥
0 ∧ gs1 +1 > 0 ∧ . . . ∧ gs > 0, where f1 , . . . , fr , g1 , . . . , gs are all CQ polynomial,
f1 , . . . , fr1 , g1 , . . . , gs1 ∈ R[x, y]Ω12 , fr1 +1 , . . . , fr , gs1 +1 , . . . , gs ∈ R[x, z]Ω13 , the
goal is to generate an interpolant I for φ and ψ, expressed using the common symbols
x, Ω1 , i.e., I includes only polynomials in R[x]Ω1 .

    Flatten and Purify: Purify and flatten the formulas φ and ψ by introducing fresh
variables for each term with uninterpreted symbols as well as for the terms with unin-
terpreted symbols. Keep track of new variables introduced exclusively for φ and ψ as
well as new common variables.
                  V
    Let φ ∧ ψ ∧ D be obtained from φ ∧ ψ by flattening and purification where D
consists of unit clauses of the form ω(c1 , . . . , cn ) = c, where c1 , . . . , cn are variables
and ω ∈ Ω. Following [21,17], using the axiom of an uninterpreted function symbol, a
set N of Horn clauses are generated as follows,
             n
             ^
      N ={         ck = bk → c = b | ω(c1 , . . . , cn ) = c ∈ D, ω(b1 , . . . , bn ) = b ∈ D}.
             k=1


The set N is partitioned into Nφ , Nψ , Nmix with all symbols in Nφ , Nψ appearing in φ,
ψ, respectively, and Nmix consisting of symbols from both φ, ψ.
    It is easy to see that for every Horn clause in Nmix , each of equalities in the hypoth-
esis as well as conclusion is mixed.


         φ ∧ ψ |= ⊥ iff φ ∧ ψ ∧ D |= ⊥ iff (φ ∧ Nφ ) ∧ (ψ ∧ Nψ ) ∧ Nmix |= ⊥.                            (31)

   Notice that φ ∧ ψ ∧ N |= ⊥ has no uninterpreted function symbols. An interpolant
generated for this problem7 can be used to generate an interpolant for φ, ψ after uni-
formly replacing all new symbols by their corresponding expressions from D.

 7
     after properly handling Nmix since Horn clauses have symbols both from φ and ψ.
5.2   Combination algorithm
     If Nmix is empty, implying there are no mixed Horn clauses, then the algorithm
invokes IGFQC on a finite set of subproblems generated from a disjunction of con-
junction of polynomial inequalities obtained after expanding Horn clauses in Nφ and
Nψ and applying De Morgan’s rules. The resulting interpolant is a disjunction of the
interpolants generated for each subproblem.
     The case when Nmix is nonempty is more interesting, but it has the same struc-
ture as the algorithm INTERLI(Q)Σ in [17] except that instead of INTERLI(Q) , it calls
IGFQC.
     The following lemma proves that if a conjunction of polynomial inequalities satis-
fies the NSOSC condition and an equality on variables can be deduced from it, then
it suffices to consider only linear inequalities in the conjunction. This property enables
us to use algorithms used in [17] to generate such equalities as well as separating terms
for the constants appearing in mixed equalities (algorithm SEP in [17]).
                                                                               Pr
Lemma 9. Let fi , i = 1, . . . , r be CQ polynomials, and λi ≥ 0, if i=1 λi fi ≡ 0,
then for any 1 ≤ i ≤ r, λi = 0 or fi is linear.
                                                                                 Pr
Proof. Let P fi = xT Ai x + liT x + γi , then Ai  0, for i = 1, . . . , r. Since i=1 λi fi =
                r
0, we have i=1 λi Ai = 0. Thus for any 1 ≤ i ≤ r, λi = 0 or Ai = 0.                         t
                                                                                            u

Lemma 10. Let φ and ψ be obtained as above with NSOSC. If φ ∧ ψ is satisfiable,
φ ∧ ψ |= ck = bk , then LP (φ) ∧ LP (ψ) |= ck = bk , where LP (φ) (LP (ψ)) is a
formula defined by all the linear constraints in φ (ψ).

Proof. Since φ ∧ ψ |= ck = bk , then φ ∧ ψ ∧ ck > bk |= ⊥. By Theorem 4, there
exist λi ≥ 0 (i = 1, · · · , r), ηj ≥ 0 (j = 0, 1, · · · , s), η ≥ 0 and two quadratic SOS
polynomials h1 and h2 such that
                r
                X                s
                                 X
                      λi f i +         ηj g j + η(ck − bk ) + η0 + h1 + h2 ≡ 0,          (32)
                i=1              j=1

                η0 + η1 + . . . + ηs + η = 1.                                            (33)

As φ ∧ ψ is satisfiable and φ ∧ ψ |= ck = bk , there exist x0 , y0 , z0 , a0 , b0 , c0 s.t.
φ[x/x0 , y/y0 , a/a0 , c/c0 ], ψ[x/x0 , z/z0 , b/b0 , c/c0 ], and ck = bk [a/a0 , b/b0 , c/c0 ].
Thus, it follows that η0 = η1 = . . . = ηs = 0 from (32) and η = 1 from (33). Hence,
(32) is equivalent to
                           r
                           X
                                  λi f i + (ck − bk ) + h1 + h2 ≡ 0.                     (34)
                           i=1

Similarly, we can prove that there exist λ0i ≥ 0 (i = 1, · · · , r) and two quadratic SOS
polynomials h01 and h02 such that
                           r
                           X                             0     0
                                  λ0i f i + (bk − ck ) + h1 + h2 ≡ 0.                    (35)
                           i=1
From (34) and (35), it follows
                          r
                          X                       0         0
                            (λ + λ0i )f i + h1 + h1 + h2 + h2 ≡ 0.                         (36)
                          i=1

                                            0            0
In addition, NSOSC implies h1 ≡ h1 ≡ h2 ≡ h2 ≡ 0. So
                                  r
                                  X
                                        λi f i + (ck − bk ) ≡ 0,                           (37)
                                  i=1

and
                                  r
                                  X
                                        λ0i f i + (bk − ck ) ≡ 0.                          (38)
                                  i=1

Applying Lemma 9 to (37), we have that λi = 0 or fi is linear. So

                                 LP (φ) ∧ LP (ψ) |= ck ≤ bk .

Likewise, by applying Lemma 9 to (38), we have

                 LP (φ) ∧ LP (ψ) |= ck ≥ bk .                                  t
                                                                               u

    If NSOSC is not satisfied, then the recursive call to IGFQC can generate linear
equalities as stated in Theorems 6 and 7 which can make hypotheses in a Horn clause
in Nmix true, thus deducing a mixed equality on symbols .


 Algorithm 3: IGFQCEunmixed
      input : two formulas φ, ψ, which are constructed respectively from φ and ψ by flattening
             and purification,
             Nφ : instances of functionality axioms for functions in Dφ ,
             Nψ : instances of functionality axioms for functions in Dψ ,
             where φ ∧ ψ ∧ Nφ ∧ Nψ |= ⊥,
      output: A formula I to be a Craig interpolant for φ and ψ.
 1 Transform φ ∧ Nφ to a DNF ∨i φi ;
 2 Transform ψ ∧ Nψ to a DNF ∨j ψj ;
 3 return I := ∨i ∧j IGFQC(φi , ψj )




Theorem 12. (Soundness and Completeness of IGFQCE) IGFQCE computes an
interpolant I of mutually contradictory φ, ψ with CQ polynomial inequalities and EUF.

Proof. Let φ and ψ are two formulas satisfy the conditions of the input of the Algorithm
IGFQCE, D is the set of definitions of fresh variables introduced during flattening and
 Algorithm 4: IGFQCE
     input : φ and ψ: two formulas, which are constructed respective from φ and ψ by
            flattening and purification,
            D : definitions for fresh variables introduced during flattening and purifying φ and
     ψ,
            N : instances of functionality axioms for functions in D,
            where φ ∧ ψ |= ⊥,
            φ = f1 ≥ 0 ∧ . . . ∧ fr1 ≥ 0 ∧ g1 > 0 ∧ . . . ∧ gs1 > 0,
            ψ = fr1 +1 ≥ 0 ∧ . . . ∧ fr ≥ 0 ∧ gs1 +1 > 0 ∧ . . . ∧ gs > 0, where
            f1 , . . . , fr , g1 , . . . , gs are all CQ polynomial,
            f1 , . . . , fr1 , g1 , . . . , gs1 ∈ R[x, y], and
            fr1 +1 , . . . , fr , gs1 +1 , . . . , gs ∈ R[x, z]
     output: A formula I to be a Craig interpolant for φ and ψ
 1 if NSOSC holds then
 2      L1 := LP (φ); L2 := LP (ψ);
 3      separate N to Nφ , Nψ and Nmix ;
 4      Nφ , Nψ := SEPmix(L1 , L2 , ∅, Nφ , Nψ , Nmix );
 5      I := IGFQCEunmixed(φ, ψ, Nφ , Nψ );
 6 else
        Find δ1 , . . . , δr ≥ 0 and an SOS polynomial h using SDP s.t. ri=1 δi fi + h ≡ 0,;
                                                                       P
 7
 8
              P 1h1 ∈ R[x, y] and P
        Construct                       h2 ∈ R[x, z] with form (H1) and (H2);
 9      f := ri=1       δi fi + h1 = − ri=r1 δi fi − h2 ;
10      Construct φ0 and ψ 0 by Theorem 6 and Theorem 7 by eliminating variables due to
        condition h1 = h2 = 0;
11      I 0 := IGFQCE(φ0 , ψ 0 , D, N );
12      I¯ := (f > 0) ∨ (f ≥ 0 ∧ I 0 );
13 end
14 Obtain I from I;
15 return I




purifying φ and ψ, and N is the set of instances of functionality axioms for functions
in D.
    If the condition NSOSC is satisfied, then from Lemma 10, we could deal with N
just using the linear constraints in φ and ψ, which is the same as [17]. Since N is easy
to be divided into three parts, Nφ ∧ Nψ ∧ Nmix . From the algorithm in [17], Nmix can be
divided into two parts Nφmix and Nψmix and add them to Nφ and Nψ , respectively. Thus,
we have

         φ ∧ ψ |= ⊥ ⇔ φ ∧ ψ ∧ D |= ⊥ ⇔ φ ∧ ψ ∧ Nφ ∧ Nψ ∧ Nmix |= ⊥
                        ⇔ φ ∧ Nφ ∧ Nφmix ∧ ψ ∧ Nψ ∧ Nψmix |= ⊥.

The correctness of step 4 is guaranteed by Lemma 10 and Theorem 8 in [17]. After step
4, Nφ is replaced by Nφ ∧ Nφmix , and Nψ is replaced by Nψ ∧ Nψmix . An interpolant for
φ ∧ Nφ ∧ Nφmix and ψ ∧ Nψ ∧ Nψmix is generated in step 5, the correctness of this step
is guaranteed by Theorem 9. Otherwise if the condition NSOSC is not satisfied, we
  Algorithm 5: SEPmix
    input : L1 , L2 : two sets of linear inequalities,
             W : a set of equalities,
             Nφ , Nψ , Nmix : three sets of instances of functionality axioms.
    output: Nφ , Nψ : s.t. Nmix is separated into Nφ or Nψ .
                     VK                                                        VK
  1 if there exists ( k=1 ck = bk → c = b) ∈ Nmix s.t L1 ∧ L2 ∧ W |=            k=1 ck = bk then
  2      if c is φ-local and b is ψ-local then
  3           for each k ∈ {1, . . . , K}, t−    +
                                            k , tk := SEP(L1 , L2 , ck , bk );
              α := function symbol corresponding to K
                                                        V
  4                                                       k=1 ck = bk → c = b;
  5           t := fresh variable; D := D ∪ {t = f (t+             +
                                                        1 . . . , tK )};
                                                          ,
                      VK             +                  VK +
  6           Cφ := k=1 ck = tk → c = t; Cψ := k=1 tk = bk → t = b;
  7           Nmix := Nmix − {C}; Nφ := Nφ ∪ {Cφ };
  8           Nψ := Nψ ∪ {Cψ }; W := W ∪ {c = t, t = d};
  9      else
 10           if c and b are φ-local then
 11                Nmix := Nmix − {C}; Nφ := Nφ ∪ {C}; W := W ∪ {c = b};
 12           else
 13                Nmix := Nmix − {C}; Nφ := Nφ ∪ {C}; W := W ∪ {c = b};
 14           end
 15      end
 16      call SEPmix(L1 , L2 , W, Nφ , Nψ , Nmix );
 17 else
 18      return Nφ and Nψ ;
 19 end




  Algorithm 6: SEP
     input : L1 , L2 : two sets of linear inequalities,
            ck , bk : local variables from L1 and L2 respectively.
     output: t− , t+ : expressions over common variables of L1 and L2 s.t L1 |= t− ≤ ck ≤ t+
            and L2 |= t+ ≤ bk ≤ t−
 1 rewrite L1 and L2 as constraints in matrix form a − Ax ≥ 0 and b − Bx ≥ 0;
 2 xi , xj in x is the variable ck and bk ;
    +        +        +      −      −       −
 3 e := ν A + µ B; e := ν A + µ B;
     +    +
 4 ν , µ := solution for
   ν + ≥ 0 ∧ µ+ ≥ 0 ∧ ν + a + µ+ b ≤ 0 ∧ e+            +                   +
                                                                V
                                              i = 1 ∧ ej = −1 ∧   l6=i,j el = 0;
     −    −
 5 ν , µ := solution for
   ν ≥ 0 ∧ µ− ≥ 0 ∧ ν − a + µ− b ≤ 0 ∧ e−
     −                                                   −                 −
                                                                V
                                              i = −1 ∧ ej = 1 ∧    l6=i,j el = 0;
    +        +                +
 6 t := µ Bx + xj − µ b;
    −        −               −
 7 t := ν Ax + xi − ν a;
             +       −
 8 return t and t ;




can obtain two polynomials h1 and h2 , and derive two formulas φ0 and ψ 0 . By Theorem
5, if there is an interpolant I 0 for φ0 and ψ 0 , then we can get an interpolant I for φ and
ψ at step 11. Similar to the proof of Theorem 9, it is easy to argue that this reduction
will terminate at the case when NSOSC holds in finite steps. Thus, this completes the
proof.                                                                              t
                                                                                    u

Example 3. Let two formulae φ and ψ be defined as follows,

          φ :=(f1 = −(y1 − x1 + 1)2 − x1 + x2 ≥ 0) ∧ (y2 = α(y1 ) + 1)
               ∧ (g1 = −x21 − x22 − y22 + 1 > 0),


          ψ :=(f2 = −(z1 − x2 + 1)2 + x1 − x2 ≥ 0) ∧ (z2 = α(z1 ) − 1)
               ∧ (g2 = −x21 − x22 − z22 + 1 > 0),

where α is an uninterpreted function. Then

             φ :=(f1 = −(y1 − x1 + 1)2 − x1 + x2 ≥ 0) ∧ (y2 = y + 1)
                    ∧ (g1 = −x21 − x22 − y22 + 1 > 0),
             ψ :=(f2 = −(z1 − x2 + 1)2 + x1 − x2 ≥ 0) ∧ (z2 = z − 1)
                    ∧ (g2 = −x21 − x22 − z22 + 1 > 0),
           D = (y1 = z1 → y = z).

The condition NSOSC is not satisfied, since −f1 −f2 = (y1 −x1 +1)2 +(z1 −x2 +1)2
is a SOS. It is easy to have

                     h1 = (y1 − x1 + 1)2 , h2 = (z1 − x2 + 1)2 .

Let f := f1 + h1 = −f2 − h2 = −x1 + x2 , then it is easy to see that

                               φ |= f ≥ 0 , ψ |= f ≤ 0.

Next we turn to find an interpolant for the following formulae

         ((φ ∧ f > 0) ∨ (φ ∧ f = 0)) and ((ψ ∧ −f > 0) ∨ (ψ ∧ f = 0)).

Then

                                (f > 0) ∨ (f ≥ 0 ∧ I2 )                          (39)

is an interpolant for φ and ψ, where I2 is an interpolant for φ ∧ f = 0 and ψ ∧ f = 0.
It is easy to see that

               φ ∧ f = 0 |= y1 = x1 − 1 , ψ ∧ f = 0 |= z1 = x2 − 1.

Substitute then into f1 in φ and ψ, we have

             φ0 = − x1 + x2 ≥ 0 ∧ y2 = y + 1 ∧ g1 > 0 ∧ y1 = x1 − 1,
             ψ0 =    x1 − x2 ≥ 0 ∧ z2 = z − 1 ∧ g2 > 0 ∧ z1 = x2 − 1.
Only using the linear form in φ0 and ψ 0 we deduce that y1 = z1 as

        φ0 |= t− = x1 − 1 ≤ y1 ≤ t+ = x2 − 1 , ψ 0 |= x2 − 1 ≤ z1 ≤ x1 − 1.

Let t = α(t), then separate y1 = z1 → y = z into two parts,

                            y1 = t+ → y = t, t+ = z1 → t = z.

Add them to φ0 and ψ 0 respectively, we have

φ0 1 = − x1 + x2 ≥ 0 ∧ y2 = y + 1 ∧ g1 > 0 ∧ y1 = x1 − 1 ∧ y1 = x2 − 1 → y = t,
ψ 0 1 = x1 − x2 ≥ 0 ∧ z2 = z − 1 ∧ g2 > 0 ∧ z1 = x2 − 1 ∧ x2 − 1 = z1 → t = z.

Then

          φ0 1 = − x1 + x2 ≥ 0 ∧ y2 = y + 1 ∧ g1 > 0 ∧ y1 = x1 − 1∧
                    (x2 − 1 > y1 ∨ y1 > x2 − 1 ∨ y = t),
         ψ0   1 =     x1 − x2 ≥ 0 ∧ z2 = z − 1 ∧ g2 > 0 ∧ z1 = x2 − 1 ∧ t = z.

Thus,

     φ0 1 =φ0 2 ∨ φ0 3 ∨ φ0 4 ,
     φ0 2 = − x1 + x2 ≥ 0 ∧ y2 = y + 1 ∧ g1 > 0 ∧ y1 = x1 − 1 ∧ x2 − 1 > y1 ,
     φ0 3 = − x1 + x2 ≥ 0 ∧ y2 = y + 1 ∧ g1 > 0 ∧ y1 = x1 − 1 ∧ y1 > x2 − 1,
     φ0 4 = − x1 + x2 ≥ 0 ∧ y2 = y + 1 ∧ g1 > 0 ∧ y1 = x1 − 1 ∧ y = t.

Since φ0 3 = f alse, then φ0 1 = φ0 2 ∨ φ0 4 . Then find interpolant

                                  I(φ0 2 , ψ 0 1 ),   I(φ0 4 , ψ 0 1 ).

= replace by two ≥, like, y1 = x1 − 1 replace by y1 ≥ x1 − 1 and x1 − 1 ≥ y1 .
   Then let I2 = I(φ0 2 , ψ 0 1 ) ∨ I(φ0 4 , ψ 0 1 ) an interpolant is found from (39) .

6   Proven interpolant
    Since our result is obtained by numerical calculation, it can’t guard the solution
satisfy the constraints strictly. Thus, we should verify the solution obtained from a SDP
solver to get a proven interpolant. In the end of section 4.2, the remark 1 said one can
use Lemma 5 to verify the result obtained from some SDP solver. In this section, we
illuminate how to verify the result obtained from some SDP solver to get a proven
interpolant by an example.

Example 4.
                                                              1
                    φ : = f1 = 4 − (x − 1)2 − 4y 2 ≥ 0 ∧ f2 = y −
                                                                ≥ 0,
                                                              2
                ψ : = f3 = 4 − (x + 1)2 − 4y 2 ≥ 0 ∧ f4 = x + 2y ≥ 0.
Constructing SOS constraints as following,
              λ1 ≥ 0, λ2 ≥ 0, λ3 ≥ 0, λ4 ≥ 0,
              − (λ1 f1 + λ2 f2 + λ3 f3 + λ4 f4 + 1) is a SOS polynomial
Using the SDP solver Yalmip to solve the above constraints for λ1 , λ2 , λ3 , λ4 , take two
decimal places, we obtain
                    λ1 = 3.63, λ2 = 38.39, λ3 = 0.33, λ4 = 12.70.
Then we have,
−(λ1 f1 + λ2 f2 + λ3 f3 + λ4 f4 + 1) = 3.96x2 + 6.10x + 15.84y 2 − 12.99y + 6.315.
Using Lemma 5, we have
                                                         305 2             1299 2 825383
3.96x2 + 6.10x + 15.84y 2 − 12.99y + 6.315 = 3.96(x +        ) + 15.84(y +      ) +      ,
                                                         396               3168     6336
which is a SOS polynomial obviously. Thus, I := λ1 f1 +λ2 f2 +1 > 0, i.e., −3.63X 2 −
14.52y 2 + 7.26x + 38.39y − 7.305 > 0, is a proven interpolant for φ and ψ.
7   Beyond concave quadratic polynomials
    Theoretically speaking, concave quadratic is quite restrictive. But in practice, the
results obtained above are powerful enough to scale up the existing verification tech-
niques of programs and hybrid systems, as all well-known abstract domains, e.g. oc-
tagon, polyhedra, ellipsoid, etc. are concave quadratic, which will be further demon-
strated in the case study below. Nonetheless, we now discuss how to generalize our
approach to more general formulas by allowing polynomial equalities whose polyno-
mials may be neither concave nor quadratic using Gröbner basis.
    Let’s start the discussion with the following running example.
Example 5. Let G = A ∧ B, where
                A : x2 + 2x + (α(β(a)) + 1)2 ≤ 0 ∧ β(a) = 2c + z∧
                     2c2 + 2c + y 2 + z = 0 ∧ −c2 + y + 2z = 0,
                B : x2 − 2x + (α(γ(b)) − 1)2 ≤ 0 ∧ γ(b) = d − z∧
                     d2 + d + y 2 + y + z = 0 ∧ −d2 + y + 2z = 0,
try to find an interpolant for A and B.
    It is easy to see that there exist some constraints which are not concave quadratic, as
some equations are not linear. Thus, the interpolant generation algorithm above is not
applicable directly.
    For easing discussion, in what follows, we use IEq(S), Eq(S) and LEq(S) to
stand for the sets of polynomials respectively from inequations, equations and linear
equations of S, for any polynomial formula S. E.g., in Example 5, we have
            IEq(A) = {x2 + 2x + (α(β(a)) + 1)2 },
             Eq(A) = {β(a) − 2c − z, 2c2 + 2c + y 2 + z, −c2 + y + 2z},
           LEq(A) = {β(a) − 2c − z}.
     In the following, we will use Example 5 as a running example to explain the ba-
sic idea how to apply Gröbner basis method to extend our approach to more general
polynomial formulas.
     Step 1: Flatten and purify. Similar to the concave quadratic case, we purify and
flatten A and B by introducing fresh variables a1 , a2 , b1 , b2 , and obtain

                 A0 : x2 + 2x + (a2 + 1)2 ≤ 0 ∧ a1 = 2c + z∧
                      2c2 + 2c + y 2 + z = 0 ∧ −c2 + y + 2z = 0,
                DA : a1 = β(a) ∧ a2 = α(a1 ),
                 B0 : x2 − 2x + (b2 − 1)2 ≤ 0 ∧ b1 = d − z∧
                      d2 + d + y 2 + y + 2z = 0 ∧ −d2 + y + z = 0,
                DB : b1 = γ(b) ∧ b2 = α(b1 ).

    Step 2: Hierarchical reasoning. Obviously, A ∧ B is unsatisfiable in PT(Q){α,β,γ}
if and only if A0 ∧B0 ∧N0 is unsatisfiable in PT(Q), where N0 corresponds to the con-
junction of Horn clauses constructed from DA ∧ DB using the axioms of uninterpreted
functions (see the following table).

       D                             G0                              N0
DA : a1 = β(a)∧ A0 : x2 + 2x + (a2 + 1)2 ≤ 0 ∧ a1 = 2c + z∧
     a2 = α(a1 ) 2c2 + 2c + y 2 + z = 0 ∧ −c2 + y + 2z = 0 N0 : b1 = a1 → b2 = a2

DB : b1 = γ(b)∧ B0 : x2 − 2x + (b2 − 1)2 ≤ 0 ∧ b1 = d − z∧
     b2 = α(b1 ) d2 + d + y 2 + y + 2z = 0 ∧ −d2 + y + z = 0


   To prove A0 ∧ B0 ∧ N0 |= ⊥, we compute the Grobner basis of G of Eq(A0 ) ∪
Eq(B0 ) under the order c  d  y  z  a1  b1 , and have a1 − b1 ∈ G. That is,
A0 ∧ B0 |= a1 = b1 . Thus, A0 ∧ B0 ∧ N0 entails

          a2 = b2 ∧ x2 + 2x + (a2 + 1)2 ≤ 0 ∧ x2 − 2x + (b2 − 1)2 ≤ 0.

This implies
                               2x2 + a22 + b22 + 2 ≤ 0,
which is obviously unsatisfiable in Q.
   Step 2 gives a proof of A ∧ B |= ⊥. In order to find an interpolant for A and B,
we need to divide N0 into two parts, A-part and B-part, i.e., to find a term t only with
common symbols, such that

                             A0 |= a1 = t B0 |= b1 = t.

Then we can choose a new variable αt = α(t) to be a common variable, since the term t
and the function α both are common. Thus N0 can be divided into two parts as follows,

                                 a2 = αt ∧ b2 = αt .
Finally, if we can find an interpolant I(x, y, z, αt ) for
       (IEq(A0 ) ∧ LEq(A0 ) ∧ a2 = αt ) ∧ (IEq(A0 ) ∧ LEq(A0 ) ∧ b2 = αt ),
using Algorithm IGFQC, then I(x, y, z, α(t)) will be an interpolant for A ∧ B.
    Step 3: Dividing N0 into two parts. According to the above analysis, we need to
find a witness t such that A0 |= a1 = t, B0 |= b1 = t, where t is an expression over the
common symbols of A and B. Fortunately, such t can be computed by Gröbner basis
method as follows: First, with the variable order c  a1  y  z, the Gröbner basis G1
of Eq(A0 ) is computed to be
               G1 ={y 4 + 4y 3 + 10y 2 z + 4y 2 + 20yz + 25z 2 − 4y − 8z,
                      y 2 + a1 + 2y + 4z, y 2 + 2c + 2y + 5z}.
Thus, we have
                                 A0 |= a1 = −y 2 − 2y − 4z.                                     (40)
Simiarly, with the variable order d  b1  y  z, the Gröbner basis G2 of Eq(B0 ) is
computed to be
                  G2 ={y 4 + 4y 3 + 6y 2 z + 4y 2 + 12yz + 9z 2 − y − z,
                         y 2 + b1 + 2y + 4z, y 2 + d + 2y + 3z}.
Thus, we have
                                 B0 |= b1 = −y 2 − 2y − 4z.                                     (41)
Whence, t = −y 2 − 2y − 4z is the witness. Let αt = α(−y 2 − 2y − 4z), which is an
expression constructed from the common symbols of A and B.
   Next, find an interpolant for following formula
       (IEq(A0 ) ∧ LEq(A0 ) ∧ a2 = αt ) ∧ (IEq(B0 ) ∧ LEq(B0 ) ∧ b2 = αt ).
Using IGFQC, we obtain an interpolant for the above formula as
                          I(x, y, z, αt ) = x2 + 2x + (αt + 1) ≤ 0.
Thus, x2 + 2x + (α(−y 2 − 2y − 4z) + 1) ≤ 0 is an interpolant for A ∧ B.
Problem 3. Generally, let A(x, z) and B(y, z) be
  A : f1 (x, z) ≥ 0 ∧ . . . ∧ fr1 (x, z) ≥ 0 ∧ g1 (x, z) > 0 ∧ . . . ∧ gs1 (x, z) > 0
        ∧ h1 (x, z) = 0 ∧ . . . ∧ hp1 (x, z) = 0,                                               (42)
  B : fr1 +1 (y, z) ≥ 0 ∧ . . . ∧ fr (y, z) ≥ 0 ∧ gs1 +1 (y, z) > 0 ∧ . . . ∧ gs (y, z) > 0
        ∧ hp1 +1 (y, z) = 0 ∧ . . . ∧ hp (y, z) = 0,                                            (43)
where f1 , . . . , fr and g1 , . . . , gs are concave quadratic polynomials, h1 , . . . , ht are gen-
eral polynomials, unnecessary to be concave quadratic, and
                                    A(x, z) ∧ B(y, z) |= ⊥,                                     (44)
try to find an interpolant for A(x, z) and B(y, z).
    According to the above discussion, Problem 3 can be solved by Algorithm 7 below.
    Algorithm 7: IGFQC
        input : Two formulae A, B as Problem 3 with A ∧ B |= ⊥
        output: An formula I to be a Craig interpolant for A and B
   Flattening, purification and hierarchical reasoning obtain A0 , B0 , NA , NB , Nmix ;
    1
   A0 := A0 ∧ NA , B0 := B0 ∧ NB ;
    2
 3 while (IEq(A0 ) ∧ LEq(A0 )) ∧ (IEq(B0 ) ∧ LEq(B0 )) 6|= ⊥ do
 4      if Nmix = ∅ then
 5           break
 6      end
 7      Choose a formula a1 = b1 → a2 = b2 ∈ Nmix corresponding to function α;
 8      Nmix := Nmix \ {a1 = b1 → a2 = b2 };
 9      Computing Grobner basis G1 for Eq(A0 ) under purely dictionary ordering with
        some variable ordering that other local variable  a1  common variable;
10      Computing Grobner basis G2 for Eq(B0 ) under purely dictionary ordering with
        some variable ordering that other local variable  b1  common variable;
11      if there exists a expression t with common variable s.t. a1 ∈ G1 ∧ b1 ∈ G2 then
12           introduce a new variable αt = α(t) as a common variable;
             A0 := A0 ∧ a2 = αt , B0 := B0 ∧ b2 = αt
13      end
14 end
15 if (IEq(A0 ) ∧ LEq(A0 )) ∧ (IEq(B0 ) ∧ LEq(B0 )) |= ⊥ then
16      Using IGFQC to obtain an interpolant I0 for above formula;
17      Obtain an interpolant I for A ∧ B from I0 ;
18      return I
19 end
20 else
21      return Fail
22 end




8       Implementation and experimental results
    We have implemented the presented algorithms in Mathematica to synthesize in-
terpolation for concave quadratic polynomial inequalities as well as their combination
with EUF. To deal with SOS solving and semi-definite programming, the Matlab-based
optimization tool Yalmip [14] and the SDP solver SDPT3 [23] are invoked. In what fol-
lows we demonstrate our approach by some examples, which have been evaluated on a
64-bit Linux computer with a 2.93GHz Intel Core-i7 processor and 4GB of RAM.
Example 6. Consider the example:

           φ := (f1 ≥ 0) ∧ (f2 ≥ 0) ∧ (g1 > 0),        ψ := (f3 ≥ 0).   φ ∧ ψ |= ⊥.

where f1 = x1 , f2 = x2 , f3 = −x21 − x22 − 2x2 − z 2 , g1 = −x21 + 2x1 − x22 + 2x2 − y 2 .

        The interpolant returned after 0.394 s is
                                         1 2 1 2
                                  I :=    x + x + 2x2 > 0
                                         2 1 2 2
Example 7. Consider the unsatisfiable conjunction φ ∧ ψ:
φ := f1 ≥ 0 ∧ f2 ≥ 0 ∧ f3 ≥ 0 ∧ g1 > 0,           ψ := f4 ≥ 0 ∧ f5 ≥ 0 ∧ f6 ≥ 0 ∧ g2 > 0.
where f1 = −y1 + x1 − 2, f2 = −y12 − x21 + 2x1 y1 − 2y1 + 2x1 , f3 = −y22 − y12 −
x22 − 4y1 + 2x2 − 4, f4 = −z1 + 2x2 + 1, f5 = −z12 − 4x22 + 4x2 z1 + 3z1 − 6x2 − 2,
f6 = −z22 − x21 − x22 + 2x1 + z1 − 2x2 − 1, g1 = 2x2 − x1 − 1, g2 = 2x1 − x2 − 1.
    The condition NSOSC does not hold, since
                     −(2f1 + f2 ) = (y1 − x1 + 2)2 is a sum of square.
Then we have h = (y1 − x1 + 2)2 , and
                             h1 = h = (y1 − x1 + 2)2 ,      h2 = 0.
Let f = 2f1 + f2 + h1 = 0. Then construct φ0 by setting y1 = x1 − 2 in φ, ψ 0 is ψ.
That is
       φ0 := 0 ≥ 0 ∧ 0 ≥ 0 ∧ −y22 − x21 − x22 + 2x2 ≥ 0 ∧ g1 > 0,                ψ 0 := ψ.
Then the interpolation for φ and ψ is reduced as
                    I(φ, ψ) = (f > 0) ∨ (f = 0 ∧ I(φ0 , ψ 0 )) = I(φ0 , ψ 0 ).
   For φ0 and ψ 0 , the condition NSOSC is still unsatisfied, since −f4 − f5 = (z1 −
2x2 − 1)2 is an SOS. Then we have h = h2 = (z1 − 2x2 − 1)2 , h1 = 0, and thus f = 0.
       φ00 = φ0 ,     ψ 00 = 0 ≥ 0 ∧ 0 ≥ 0 ∧ −z22 − x21 − x22 + 2x1 ≥ 0 ∧ g2 > 0.
The interpolation for φ0 and ψ 0 is further reduced by I(φ0 , ψ 0 ) = I(φ00 , ψ 00 ), where
             φ00 := (f10 = −y22 − x21 − x22 + 2x2 ≥ 0) ∧ 2x2 − x1 − 1 > 0,
             ψ 00 := (f20 = −z22 − x21 − x22 + 2x1 ≥ 0) ∧ 2x1 − x2 − 1 > 0.
    Here the condition NSOSC holds for φ00 and ψ 00 , then by SDP we find λ1 = λ2 =
0.25, η0 = 0, η1 = η2 = 0.5 and SOS polynomials h1 = 0.25 ∗ ((x1 − 1)2 + (x2 −
1)2 + y22 ) and h2 = 0.25 ∗ ((x1 − 1)2 + (x2 − 1)2 + z22 ) such that λ1 f10 + λ2 f20 +
η0 + η1 g1 + η2 g2 + h1 + h2 ≡ 0 and η0 + η1 + η2 = 1. For η0 + η1 = 0.5 > 0, the
interpolant returned after 2.089 s is f > 0, i.e. I := −x1 + x2 > 0.
Example 8. Consider the example:
           φ :=(f1 = −(y1 − x1 + 1)2 − x1 + x2 ≥ 0) ∧ (y2 = α(y1 ) + 1)
                 ∧ (g1 = −x21 − x22 − y22 + 1 > 0),
           ψ :=(f2 = −(z1 − x2 + 1)2 + x1 − x2 ≥ 0) ∧ (z2 = α(z1 ) − 1)
                 ∧ (g2 = −x21 − x22 − z22 + 1 > 0).
where α is an uninterpreted function. It takes 0.369 s in our approach to reduce the
problem to find an interpolant as I(φ0 2 , ψ 0 1 ) ∨ (φ0 4 , ψ 0 1 ), and another 2.029 s to give
the final interpolant as
                                     1
              I := (−x1 + x2 > 0) ∨ ( (−4α(x2 − 1) − x21 − x22 ) > 0)
                                     4
Example 9. Let two formulae φ and ψ be defined as
            φ :=(f1 = 4 − x2 − y 2 ≥ 0) ∧ f2 = y ≥ 0 ∧ (g = x + y − 1 > 0),
           ψ :=(f4 = x ≥ 0) ∧ (f5 = 1 − x2 − (y + 1)2 ≥ 0).

      The interpolant returned after 0.532 s is I := 21 (x2 + y 2 + 4y) > 0 8 .
Example 10. This is a linear interpolation problem adapted from [17]. Consider the
unsatisfiable conjunction φ ∧ ψ:
          φ := z − x ≥ 0 ∧ x − y ≥ 0 ∧ −z > 0,         ψ := x + y ≥ 0 ∧ −y ≥ 0.
      It takes 0.250 s for our approach to give an interpolant as I := −0.8x − 0.2y > 0.
Example 11. Consider another linear interpolation problem combined with EUF:
              φ := f (x) ≥ 0 ∧ x − y ≥ 0 ∧ y − x ≥ 0,        ψ := −f (y) > 0.
The interpolant returned after 0.236 s is I := f (y) ≥ 0.
Example 12. Consider two formulas A and B with A ∧ B |= ⊥, where

      A := − x1 2 + 4x1 + x2 − 4 ≥ 0∧
            − x1 − x2 + 3 − y 2 > 0,
     B :=−3x1 2 − x2 2 + 1 ≥ 0 ∧ x2 − z 2 ≥ 0.

Note that a concave quadratic polynomial (the bold
one) from the ellipsoid domain is involved in B. It
takes 0.388 s using our approach to give an inter-
polant as I := −3 + 2x1 + x1 2 + 21 x2 2 > 0. An
intuitive description of the interpolant is as the pur-
ple curve in the right figure, which separates A and
B in the panel of common variables x1 and x2 .
Example 13. Consider two formulas φ and ψ both are defined by an ellipse joint a
half-plane:
                                        1
 φ := 4 − (x − 1)2 − 4y 2 ≥ 0 ∧ y −       ≥ 0, ψ := 4 − (x + 1)2 − 4y 2 ≥ 0 ∧ x + 2y ≥ 0.
                                        2
The interpolant returned after 0.248 s is I := −3.63x2 − 14.52y 2 + 7.26x + 38.39y −
7.305 > 0.
Example 14. Consider two formulas φ and ψ both are defined by an octagon joint a
half-plane:
φ := −3 ≤ x ≤ 1 ∧ −2 ≤ y ≤ 2 ∧ −4 ≤ x − y ≤ 2 ∧ −4 ≤ x + y ≤ 2 ∧ x + 2y + 1 ≤ 0,
ψ := −1 ≤ x ≤ 3 ∧ −2 ≤ y ≤ 2 ∧ −2 ≤ x − y ≤ 4 ∧ −2 ≤ x + y ≤ 4 ∧ 2x − 5y + 6 ≤ 0.

The interpolant returned after 0.225 s is I := −13.42x − 29.23y − 1.7 > 0.
 8
     In order to give a more objective comparison of performance with the approach proposed in
     [5], we skip over line 1 in the previous algorithm IGFQC.
Example 15. Consider two formulas φ and ψ both are defined by an octagon joint a
half-plane:
   φ := 2 ≤ x ≤ 7 ∧ 0 ≤ y ≤ 3 ∧ 0 ≤ x − y ≤ 6 ∧ 3 ≤ x + y ≤ 9 ∧ 23 − 3x − 8y ≤ 0,
   ψ := 0 ≤ x ≤ 5 ∧ 2 ≤ y ≤ 5 ∧ −4 ≤ x − y ≤ 2 ∧ 3 ≤ x + y ≤ 9 ∧ y − 3x − 2 ≤ 0.

The interpolant returned after 0.225 s is I := 12.3x − 7.77y + 4.12 > 0.


                                                        Time (sec)
 Example       Type
                            CLP-P ROVER        F OCI     CSI SAT        AiSat    Our Approach
 Example 6 NLA                    –               –          –            –          0.394
 Example 7 NLA                    –               –          –            –          2.089
 Example 8 NLA+EUF                –               –          –            –          2.398
 Example 9 NLA                    –               –          –          0.023        0.532
 Example 10 LA                  0.023             ×       0.003           –          0.250
 Example 11 LA+EUF              0.025          0.006      0.007           –          0.236
 Example 12 Ellipsoid             –               –          –            –          0.388
 Example 13 Ellipsoid2            –               –          –          0.013        0.248
 Example 14 Octagon1            0.059             ×       0.004         0.021        0.225
 Example 15 Octagon2            0.065             ×       0.004         0.122        0.216
  – means that the interpolant generation fails, and × specifies a particularly wrong answer.

                      Table 1. Evaluation results of the presented examples

     The experimental evaluation on the above examples is illustrated in Table 1, where
we have also compared on the same platform with the performances of AiSat, a tool
for nonlinear interpolant generation proposed in [5], as well as three publicly avail-
able interpolation procedures for linear-arithmetic cases, i.e. Rybalchenko’s tool CLP-
P ROVER) in [17], McMillan’s procedure F OCI in [15], and Beyer’s tool CSI SAT in
[2]. Table 1 shows that our approach can successfully solve all the examples and it
is especially the completeness that makes it an extraordinary competitive candidate for
synthesizing interpolation. Besides, CLP-P ROVER, F OCI, and CSI SAT can handle only
linear-arithmetic expressions with an efficient optimization (and thus the performances
in linear cases are better than our raw implementation). As for AiSat, a rather limited
set of applications is acceptable because of the weakness of tackling local variables, and
whether an interpolant can be found or not depends on a pre-specified total degree. In
[5], not only all the constraints in formula φ should be considered but also some of their
products, for instance, f1 , f2 , f3 ≥ 0 are three constraints in φ, then four constraints
f1 f2 , f1 f3 , f2 f3 , f1 f2 f3 ≥ 0 are added in φ.
     Table 1 indicates the efficiency of our tool is lower than any of other tools when-
ever a considered example is solvable by both. This is mainly because our tool is im-
plemented in Mathematica, and therefore have to invoke some SDP solvers with low
efficiency. As a future work, we plan to re-implement the tool using C, thus we can
call SDP solver CSDP which is much more efficient. Once a considered problem is lin-
ear, an existing interpolation procedure will be invoked directly, thus, SDP solver is not
needed.
9   Conclusion
    The paper proposes a polynomial time algorithm for generating interpolants from
mutually contradictory conjunctions of concave quadratic polynomial inequalities over
the reals. Under a technical condition that if no nonpositive constant combination of
nonstrict inequalities is a sum of squares polynomials, then such an interpolant can
be generated essentially using the linearization of quadratic polynomials. Otherwise,
if this condition is not satisified, then the algorithm is recursively called on smaller
problems after deducing linear equalities relating variables. The resulting interpolant is
a disjunction of conjunction of polynomial inequalities.
    Using the hierarchical calculus framework proposed in [21], we give an interpo-
lation algorithm for the combined quantifier-free theory of concave quadratic polyno-
mial inequalities and equality over uninterpreted function symbols. The combination
algorithm is patterned after a combination algorithm for the combined theory of linear
inequalities and equality over uninterpreted function symbols.
    In addition, we also discuss how to extend our approach to formulas with polyno-
mial equalities whose polynomials may be neither concave nor quadratic using Gröbner
basis.
    The proposed approach is applicable to all existing abstract domains like octagon,
polyhedra, ellipsoid and so on, therefore it can be used to improve the scalability of
existing verification techniques for programs and hybrid systems.
    An interesting issue raised by the proposed framework for dealing with nonlinear
polynomial inequalities is the extent to which their linearization with some additional
conditions on the coefficients (such as concavity for quadratic polynomials) can be
exploited. We are also investigating how results reported for nonlinear polynomial in-
equalities based on positive nullstellensatz [22] in [5] and the Archimedian condition on
variables, implying that every variable ranged over a bounded interval, can be exploited
in the proposed framework for dealing with polynomial inequalities.
References
1. A. Barvinok: A course in convexity. Vol. 54. American Mathematical Soc., 2002.
2. D. Beyer, D. Zufferey, and R. Majumdar: CSIsat: Interpolation for LA+EUF. Proc. Computer
  Aided Verification (CAV), 2008, Princeton, July 07-14, 2008.
3. CSDP: http://infohost.nmt.edu/˜borchers/csdp.html.
4. L. Dai, T. Gan, B. Xia and N. Zhan: Barrier certificate revisited. To apear J. of Symbolic
  Computation. http://lcs.ios.ac.cn/∼znj/papers/jsc14.pdf.
5. L. Dai, B. Xia, and N. Zhan: Generating non-linear interpolants by semidefinite programming.
  Computer Aided Verification. Springer Berlin Heidelberg, 2013: 364-380.
6. V. D’Silva, M. Purandare, G. Weissenbacher and D. Kroening: Interpolant Strength. Verifi-
  cation, Model Checking and Abstract Interpretation (VMCAI), Springer LNCS 5944, 2010,
  129-145.
7. T. Fujie and M. Kojima: Semidefinite programming relaxation for nonconvex quadratic pro-
  grams. Journal of Global Optimization, 367–380, 1997.
8. T. Gan, L. Dai, B. Xia, N. Zhan, D. Kapur and M. Chen: Interpolation synthesis
  for quadratic polynomial inequalities and combination with EUF. In arXiv:1601.04802,
  http://arxiv.org/abs/1601.04802.
9. D. Kapur: Interpolation and Quantifier Elimination, Draft Working Paper, Department of
  Computer Science, University of New Mexico, June 2013.
10. D. Kapur, R. Majumdar and C. Zarba: Interpolation for Data Structures, Proceedings of the
  14th ACM SIGSOFT Symp. on Foundations of Software Engineering, 2006, Seattle, Washing-
  ton.
11. J. Krajíc̆ek: Interpolation theorems, lower bounds for proof systems, and independence re-
  sults for bounded arithmetic. The Journal of Symbolic Logic, 1997, 62(02): 457-486.
12. S. Kupferschmid and B. Becker: Craig interpolation in the presence of non-linear constraints.
  Formal Modeling and Analysis of Timed Systems. Springer Berlin Heidelberg, 2011: 240-255.
13. M. Laurent: Sums of squares, moment matrices and optimization over polynomials(Updated
  version) . Emerging Applications of Algebraic Geometry, Vol. 149 of IMA Volumes in Mathe-
  matics and its Applications 157–270, 2010.
14. J. Löfberg: Pre- and post-processing sum-of-squares programs in practice. J. of IEEE Trans-
  actions on Automatic Control, 54(5):1007-1011, 2009. http://users.isy.liu.se/
  johanl/yalmip/.
15. K.L. McMillan: An interpolating theorem prover. Theoretical Computer Science, 2005,
  345(1): 101-121.
16. P. Pudlák. Lower bounds for resolution and cutting plane proofs and monotone computations.
  The Journal of Symbolic Logic, 1997, 62(03): 981-998.
17. A. Rybalchenko and V. Sofronie-Stokkermans.: Constraint solving for interpolation.Journal
  of Symbolic Computation 45,1212-1233 , 2010.
18. A. Schrijver. Theory of linear and integer programming. John Wiley & Sons, 1998.
19. SeDuMi: http://sedumi.ie.lehigh.edu.
20. V. Sofornie-Stokkermans: Hierarchical reasoning in local theory extensions. Proc. of 20th
  Intl. Conf. on Automated Deduction (CADE-20), LNAI 3632, 219-234.
21. V. Sofornie-Stokkermans: Interpolation in local theory extensions. J. of Logical Methods in
  Computer Science, Vol. 4, No. 1, 2008, 1-31.
22. G. Stengle: A Nullstellensatz and a Positivstellensatz in semialgebraic geometry. Math. Ann.,
  1974, 207: 87–97.
23. R. H. Tütüncü, K. C. Toh, and M. J. Todd: Solving semidefinite-quadratic-linear programs
  using SDPT3. J. of Mathematical programming, 95(2):189-217, 2003. http://www.math.
  nus.edu.sg/˜mattohkc/sdpt3.html.
24. L. Vandenberghe, S. Boyd: Semidefinite programming[J]. SIAM review, 1996, 38(1): 49-95.
25. H. Wolkowicz, R. Saigal, and L. Vandenberghe (eds): Handbook of semidefinite program-
  ming: theory, algorithms, and applications. Vol. 27. Springer, 2000.
26. G. Yorsh, M. Musuvathi: A combination method for generating interpolants. Proc. Auto-
  mated Deduction (CADE), 2005, Springer LNCS, 2005: 353-368.
27. H. Zhao, N. Zhan, D. Kapur, and K.G. Larsen: A “Hybrid” Approach for Synthesizing Op-
  timal Controllers of Hybrid Systems: A Case Study of Oil Pump Industrial Example, Proc.
  Formal Methods (FM), 2012, LNCS, August 2012.
28. H. Zhao, N. Zhan, and D. Kapur: Synthesizing switching controllers for hybrid systems by
  generating invariants,’ Proc. Festschrift Symp. in honor of He Jifeng, Sept. 01-03, 2013.
