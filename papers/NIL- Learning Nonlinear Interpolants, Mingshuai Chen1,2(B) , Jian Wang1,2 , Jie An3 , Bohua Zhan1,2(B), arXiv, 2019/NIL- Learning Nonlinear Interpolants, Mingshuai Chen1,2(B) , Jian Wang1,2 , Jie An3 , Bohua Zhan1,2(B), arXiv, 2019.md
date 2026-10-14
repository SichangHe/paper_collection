                                                       NIL: Learning Nonlinear Interpolants?

                                                     Mingshuai Chen1,2(B) , Jian Wang1,2 , Jie An3 , Bohua Zhan1,2(B) ,
                                                                Deepak Kapur4 , and Naijun Zhan1,2(B)
                                                1
                                                 State Key Lab. of Computer Science, Institute of Software, CAS, Beijing, China
                                                        2
                                                           University of Chinese Academy of Sciences, Beijing, China
arXiv:1905.11625v5 [cs.LO] 28 Aug 2019




                                                                   {chenms,bzhan,znj}@ios.ac.cn
                                                    3
                                                       School of Software Engineering, Tongji University, Shanghai, China
                                               4
                                                 Department of Computer Science, University of New Mexico, Albuquerque, USA



                                                 Abstract. Nonlinear interpolants have been shown useful for the verification of
                                                 programs and hybrid systems in contexts of theorem proving, model checking,
                                                 abstract interpretation, etc. The underlying synthesis problem, however, is chal-
                                                 lenging and existing methods have limitations on the form of formulae to be
                                                 interpolated. We leverage classification techniques with space transformations
                                                 and kernel tricks as established in the realm of machine learning, and present
                                                 a counterexample-guided method named NIL for synthesizing polynomial inter-
                                                 polants, thereby yielding a unified framework tackling the interpolation problem
                                                 for the general quantifier-free theory of nonlinear arithmetic, possibly involv-
                                                 ing transcendental functions. We prove the soundness of NIL and propose suf-
                                                 ficient conditions under which NIL is guaranteed to converge, i.e., the derived
                                                 sequence of candidate interpolants converges to an actual interpolant, and is com-
                                                 plete, namely the algorithm terminates by producing an interpolant if there exists
                                                 one. The applicability and effectiveness of our technique are demonstrated exper-
                                                 imentally on a collection of representative benchmarks from the literature, where
                                                 in particular, our method suffices to address more interpolation tasks, including
                                                 those with perturbations in parameters, and in many cases synthesizes simpler
                                                 interpolants compared with existing approaches.

                                                 Keywords: Nonlinear Craig interpolant · Counterexample-guided learning · Pro-
                                                 gram verification · Support vector machines (SVMs)


                                         1    Introduction
                                         Interpolation-based technique provides a powerful mechanism for local and modular
                                         reasoning, thereby improving scalability of various verification techniques, e.g., theo-
                                         rem proving, model checking and abstract interpretation, to name just a few. The study
                                         of interpolation was pioneered by Krajı́ček [26] and Pudlák [34] in connection with
                                         theorem proving, by McMillan [29] in the context of model checking, by Graf and
                                         Saı̈di [16], McMillan [30] and Henzinger et al. [19] pertaining to abstraction like CE-
                                         GAR [7], and by Wang et al. [23] in the context of learning-based invariant generation.
                                         ?
                                             This work has been supported through grants by NSFC under grant No. 61625206 and
                                             61732001, by the CAS Pioneer Hundred Talents Program under grant No. Y9RC585036, and
                                             by the National Science Foundation Award DMS-1217054.
2       M. Chen et al.

Developing efficient algorithms for generating interpolants for various theories and their
combination has become an active research area, see e.g., [6, 24, 25, 30, 31, 35, 45].
    Though established methods addressing interpolant generation for Presburger arith-
metic, decidable fragments of first-order logic, theory of equality over uninterpreted
functions (EUFs) as well as their combination have been extensively studied in the lit-
erature, there appears to be little work on synthesizing nonlinear interpolants. Dai et
al. proposed an algorithm in [10] for generating interpolants for nonlinear polynomial
inequalities based on the existence of a witness guaranteed by Stengle’s Positivstellen-
satz [15] that can be computed using semi-definite programming (SDP). A major limi-
tation of this method is that the two mutually contradictory formulas to be interpolated
must share the same set of variables. Okudono et al. extended [10] in [32] to cater for the
so-called sharper and simpler interpolants by developing a continuous fraction-based
algorithm that rounds off numerical solutions. In [13], Gan et al. considered the inter-
polation for inequalities combined with EUFs by employing the hierarchical calculus
framework proposed in [37] (and its extension [38]), while the inequalities are limited
to be of the concave quadratic form. In [14], Gao and Zufferey transformed proof traces
from δ-complete decision procedures into interpolants, composed of Boolean combina-
tions of linear constraints, which can deal with certain transcendental functions beyond
polynomials. The techniques of encoding interpolants as logical combinations of linear
constraints, including [14], [27] and [36], however, yield potentially large interpolants
(requiring even an infinite length in the worst case) and their usage thus becomes diffi-
cult in practical applications (cf. Example 1).
    Interpolants can be viewed as classifiers that distinguish, in the context of program
verification for instance, positive program states from negative ones (unreachable/error
states) and consequently the state-of-the-art classification algorithms can be leveraged
for synthesizing interpolants. The universal applicability of classification techniques
substantially extends the scope of theories admitting interpolant generation. This idea
was first employed by Sharma et al. in [36], which infers linear interpolants through
hyperplane-classifiers generated by support vector machines (SVMs) [3,44] whilst han-
dles superficial nonlinearities by assembling interpolants in the form purely of conjunc-
tions (or dually, disjunctions) of linear half-spaces, which addresses only a limited cat-
egory of formulae featuring nonlinearities. The learning-based paradigm has also been
exploited in the context of nonlinear constraint solving, see e.g., [11].
    In this paper, we present a classification-based learning method for the synthe-
sis of polynomial interpolants for the quantifier-free theory of nonlinear arithmetic.
Our approach is based on techniques of space transformations and kernel tricks per-
tinent to SVMs that have been well-developed in the realm of machine learning. Our
method is described by an algorithm called NIL (and its several variants) that adopts the
counterexample-guided inductive synthesis framework [21, 39]. We prove the sound-
ness of NIL and propose sufficient conditions under which NIL is guaranteed to con-
verge, that is, the derived sequence of classifiers (candidate interpolants) converges to
an actual interpolant, and is complete, i.e., if an interpolant exists, the method termi-
nates with an actual interpolant. In contrast to related work on generation of nonlin-
ear interpolants, which restrict the input formulae, our technique provides a uniform
framework, tackling the interpolation problem for the general quantifier-free theory of
                                               NIL: Learning Nonlinear Interpolants        3

nonlinear arithmetic, possibly involving transcendental functions. The applicability and
effectiveness of NIL are demonstrated experimentally on a collection of representative
benchmarks from the literature; as is evident from experimental results, our method is
able to address more demands on the nature of interpolants, including those with per-
turbations in parameters (due to the robustness inherited from SVMs); in many cases,
it synthesizes simpler interpolants compared with other approaches, as shown by the
following example.

Example 1 ( [14]). Consider two mutually contradictory inequalities φ =   b y ≥ x2 and
ψ =b y ≤ − cos(x) + 0.8. Our NIL algorithm constructs a single polynomial inequality
I =b 15x2 < 4 + 20y as the interpolant, namely, φ |= I and I ∧ ψ is unsatisfiable; while
the interpolant generated by the approach in [14], only when provided with sufficiently
large finite domains, e.g., x ∈ [−π, π] and y ∈ [−0.2, π 2 ], is y > 1.8 ∨ (0.59 ≤ y ≤
1.8 ∧ −1.35 ≤ x ≤ 1.35) ∨ (0.09 ≤ y < 0.59 ∧ −0.77 ≤ x ≤ 0.77) ∨ (y ≥ 0 ∧ −0.3 ≤
x ≤ 0.3). As will be discussed later, we do not need to provide a priori information to
our algorithm such as bounds on variables.

    The rest of the paper is organized as follows. Sect. 2 introduces some preliminaries
on Craig interpolants and SVMs. In Sect. 3, we present the NIL algorithm dedicated to
synthesizing nonlinear interpolants, followed by the analysis of its soundness, condi-
tional completeness and convergence in Sect. 4. Sect. 5 reports several implementation
issues and experimental results on a collection of benchmarks (with the robustness dis-
cussed in Sect. 6). The paper is then concluded in Sect. 7.

2   Preliminaries
Let N, Q and R be the set of natural, rational and real numbers, respectively. We denote
by R[x] the polynomial ring over R with variables x = (x1 , . . . , xn ), and kxk denotes
the `2 -norm [4]. For a set X ⊆ Rn , its convex hull is denoted by conv(X). For x, x0 ∈
X, dist(x, x0 ) = kx − x0 k denotes the Euclidean distance between two points, which
generalizes to dist(x, X 0 ) = minx0 ∈X 0 dist(x, x0 ). Given δ ≥ 0, define B(x, δ) =
{x0 ∈ Rn |kx0 − xk ≤ δ} as the closed ball of radius δ centered at x. Consider the
quantifier-free fragment of a first-order theory of polynomials over the reals, denoted
by TP , in which a formula ϕ is of the form

                           b p(x)  0 | ϕ ∧ ϕ | ϕ ∨ ϕ | ¬ϕ
                         ϕ =

where p(x) ∈ R[x] and  ∈ {<, >, ≤, ≥, =}. A natural extension of our method to
cater for more general nonlinearities involving transcendental functions will be demon-
strated in subsequent sections. In the sequel, we use ⊥ to stand for false and > for true.
Let R[x]m consist of all polynomials p(x) of degree ≤ m ∈ N. We abuse the notation
ϕ ∈ R[x]m to abbreviate ϕ =   b p(x)  0 and p(x) ∈ R[x]m if no ambiguity arises.
    Given formulas φ and ψ in a theory T , φ is valid w.r.t. T , written as |=T φ, iff φ is
true in all models of T ; φ entails ψ w.r.t. T , written as φ |=T ψ, iff every model of T
that makes φ true makes ψ also true; φ is satisfiable w.r.t. T , iff there is a model of T in
which φ is true; otherwise unsatisfiable. It follows that φ is unsatisfiable iff φ |=T ⊥.
The set of all the models that make φ true is denoted by JφKT .
4        M. Chen et al.

2.1   Craig Interpolant
Craig showed in [9] that given two formulas φ and ψ in a first-order logic T s.t. φ |=T
ψ, there always exists an interpolant I over the common symbols of φ and ψ s.t. φ |=T I
and I |=T ψ. In the verification literature, this terminology has been abused by [30],
which defined an interpolant over the common symbols of φ and ψ as

Definition 1 (Interpolant). Given φ and ψ in a theory T s.t. φ ∧ ψ |=T ⊥, a formula
I is a (reverse) interpolant of φ and ψ if (i) φ |=T I; (ii) I ∧ ψ |=T ⊥; and (iii) I
contains only common symbols shared by φ and ψ.

    It is immediately obvious that φ |=T ψ iff φ∧¬ψ |=T ⊥, namely, I is an interpolant
of φ and ψ iff I is a reverse interpolant in McMillan’s sense of φ and ¬ψ. We follow
McMillan in continuing to abuse the terminology.
2.2   Support Vector Machines
In machine learning, support vector machines [3,44] are supervised learning models for
effective classification based on convex optimization. In a binary setting, we are given a
training dataset X = X + ] X − of n sample points {(x1 , y1 ), (x2 , y2 ), . . . , (xn , yn )},
where xi ∈ Rd , and yi is either 1, indicating a positive sample xi ∈ X + , or -1, indi-
cating a negative one in X − . The goal of classification here is to find a potential hyper-
plane (a.k.a. linear classifier) to separate the positive samples from the negative ones.
There however might be various or even infinite number of separating hyperplanes,
and an SVM aims to construct a separating hyperplane that yields the largest distance
(so-called functional margin) to the nearest positive and negative samples. Such a clas-
sification hyperplane is called the optimal-margin classifier while the samples closest
to it are called the support vectors.
Linear SVMs. Assume that X + and X − are linearly separable, meaning that there
exists a linear separating hyperplane wT x + b = 0 such that yi (wT xi + b) > 0, for
all (xi , yi ) ∈ X. Then the functional margin can be formulated as

                            b 2 min1≤i≤n 1/kwk|wT xi + b|.
                          γ =

Linear SVMs are committed to finding appropriate parameters (w, b) that maximize
the functional margin while adhering to the constraints of separability, which reduces
equivalently to the following convex quadratic optimization problem [2] that can be
efficiently solved by off-the-shelf packages for quadratic programming:
                     1 T
         minimize      w w      subject to yi (wT xi + b) ≥ 1, i = 1, 2, . . . , n.        (1)
             w,b     2

Lemma 1 (Correctness of SVMs [36]). Given positive samples X + which are linearly
separable from negative samples X − , SVMs produce, under computations of infinite
precision, a half-space h s.t. ∀x ∈ X + . h(x) > 0 and ∀x ∈ X − . h(x) < 0.

Corollary 1 (Separation of Convex Hulls [1]). The half-space h in Lemma 1 satisfies
that ∀x ∈ conv(X + ). h(x) > 0 and ∀x ∈ conv(X − ). h(x) < 0.
                                                              NIL: Learning Nonlinear Interpolants                      5


                                                            Φ




Fig. 1: Mapping from a two-dimensional input space into a three-dimensional feature space with linear separation thereof.


Nonlinear SVMs. When φ and ψ are formulas over nonlinear arithmetic, often after
sampling X, it is not possible to find a linearly separable hyperplane in the common
variables. However, a nonlinear surface that can be described as a linear hyperplane
in the space of monomials of bounded degree may separate X + and X − . The above
                                                                              ˜
construction is generalized by introducing a transformation from Rd to Rd , the vec-
tor space of monomials in the common variables up to some bounded degree, with
yi (wT xi + b) ≥ 1 in (1) replaced by yi (wT Φ(xi ) + b) ≥ 1, where Φ is a linear expres-
sion in monomials in the common variables up to a bounded degree. Here, the vectors
Φ(x) span the feature space.
    Consider the Lagrangian dual [3] of the modified optimization problem:

                         1 Xn Xn                                     Xn
               minimize                 αi αj yi yj Φ(xi )T Φ(xj ) −          αi
                  α      2  i=1     j=1                                   i=1
                         Xn
              subject to      αi yi = 0, and αi ≥ 0 for i = 1, 2, . . . , n.
                                   i=1

A kernel function κ : Rd × Rd 7→ R is defined as κ(x, x0 ) =b Φ(x)T Φ(x0 ). The intro-
duction of the dual problem and the kernel function [3] reduces the computational com-
                           ˜ down to O(d). For the sake of post-verifying a candidate
plexity essentially from O(d)
interpolant given by SVMs, we adopt an inhomogeneous polynomial kernel function of
the form
                             κ(x, x0 ) =
                                       b (βxT x0 + θ)m ,
where m is the polynomial degree describing complexity of the feature space, θ ≥ 0
is a parameter trading off the influence of higher-order versus lower-order terms in the
polynomial, and β is a scalar parameter. Henceforth,Pn the optimal-margin classifier (if
there exists one) can be derived as wT Φ(x) = i=1 αi κ(xi , x) = 0, with xi being a
support vector iff αi > 0. In practice, usually a large amount of αi s turn out to be zero
and this leads to a simple representation of a classifier. Fig. 1 illustrates the intuitive idea
of the transformation from the original input space to the feature space. We will show
in the sequel that the resulting classifier can be viewed as a candidate interpolant, while
its optimal-margin feature contributes to a certain “medium” logical strength of the
interpolant, which is thus robust to perturbations (in the feature space) in the formulae
to be interpolated.

3    Learning Interpolants
In this section, we present the NIL algorithm for synthesizing nontrivial (reverse) Craig
interpolants for the quantifier-free theory of nonlinear arithmetic. It takes as input a
6       M. Chen et al.

pair hφ, ψi of formulas in TP as well as a positive integer m, and aims to generate an
interpolant I of maximum degree m, i.e., I ∈ R[x]m , if it exists, such that φ |=TP I
and I ∧ ψ |=TP ⊥. Here, hφ, ψi can be decorated as hφ(x, y), ψ(x, z)i with variables
involved in the predicates, and thus x denotes variables that are common to φ and ψ.
In the sequel, we drop the subscript TP in |=TP and J·KTP wherever the context is
unambiguous.
     Due to the decidability of the first-order theory of real-closed fields established by
Tarski [43], TP admits quantifier elimination (QE). This means that the satisfiability of
any formula in TP can be decided (in doubly exponential time in the number of vari-
ables for the worst case). If the formula is satisfiable, models satisfying the formula can
also be constructed algorithmically (following the same time complexity). Though the
introduction of general forms of transcendental functions renders the underlying theory
undecidable, there does exist certain extension of TP with transcendental functions (in-
volving exponential functions, logarithms and trigonometric functions), e.g. that identi-
fied by Strzeboński in [42] and references therein, which still admits QE. This allows a
straightforward extension of NIL to such a decidable fragment involving transcenden-
tal functions. Specifically, the decidability remains when the transcendental functions
involved are real univariate exp-log functions [40] or tame elementary functions [41]
which admit a real root isolation algorithm.

3.1   The Core Algorithm

The basic idea of NIL is to view interpolants as classifiers and use SVMs with the
kernel trick to perform effective classification. The algorithm is based on the sampling-
guessing-refining technique: in each iteration, it is fed with a classifier (candidate in-
terpolant) for a finite set of sample points from JφK and JψK (line 5), and verify the
candidate (line 10) by checking the entailment problem that defines an interpolant (as
in Def. 1). If the verification succeeds, the interpolant is returned as the final result.
Otherwise, a set of counterexamples is obtained (line 13 and 14) as new sample points
to further refine the classifier. In what follows, we explain the steps of the interpolation
procedure in more detail.
Initial sampling. The algorithm begins by checking the satisfiability of φ ∧ ψ. If the
formula is satisfiable, it is then impossible to find an interpolant, and the algorithm stops
declaring no interpolant exists.
    Next, the algorithm attempts to sample points from both JφK and JψK. This initial
sampling stage can usually be done efficiently using the Monte Carlo method, e.g. by
(uniformly) scattering a number of random points over certain bounded range and then
selecting those fall in JφK and JψK respectively. However, this method fails when one
or both of the predicates is very unlikely to be satisfied. One common example is when
the predicate involves equalities. For such situations, solving the satisfiability problem
using QE is guaranted to succeed in producing the sample points.
    To meet the condition that the generated interpolant can only involve symbols that
are common to φ and ψ, we can project the points sampled from JφK (resp. JψK) to the
space of x by simply dropping the components that pertain to y (resp. z) and thereby
obtain sample points in X + (resp. X − ).
                                                         NIL: Learning Nonlinear Interpolants                  7

 Algorithm NIL: Learning nonlinear interpolant
      input : φ and ψ in TP over common variables x;
              m, degree of the polynomial kernel, and hence                    JφK                  JψK

                  maximum degree of the interpolant.
      /* checking unsatisfiability */
 1    if φ ∧ ψ 6|= ⊥ then
           /* no interpolant exists */
 2         abort;
      /* generating initial sample points */
 3    hX + , X − i ← Sampling(φ, ψ);                                   Fig. 2: In NIL, a candidate interpolant
      /* counterexample-guided learning */                             (black line as its boundary) is refined to
 4    while > do                                                       an actual one (red line as its boundary)
           /* generating a classifier by SVMs */                       by adding a counterexample (red dot).
 5         C ← SVM(X + , X − , m);
           /* checking classification result */
  6        if C = Failed then
                /* no interpolant exists in R[x]m */
                                                                                 JφK              JψK

 7              abort;
                                                                                       δ
          /* classifier as candidate interpolant */
 8        else
 9             I ← C;
          /* valid interpolant found */
 10       if φ |= I and I ∧ ψ |= ⊥ then
                                                                       Fig. 3: In NILδ , a counterexample (red
 11             return I;
                                                                       dot) stays at least a distance of δ away
          /* adding counterexamples */                                 from the candidate interpolant (black line
 12       else                                                         as its boundary) to be refined, leading to
 13            X + ← X + ] FindInstance(φ ∧ ¬I);                       an interpolant (red line as its boundary)
 14            X − ← X − ] FindInstance(I ∧ ψ);                        with tolerance δ.



Entailment checking. The correctness of SVM given in Lemma 1 only guarantees
that the candidate interpolant separates the finite set of points sampled from JφK and
JψK, not necessarily the entirety of the two sets. Hence, post-verification by checking
the entailment problem (line 10) is needed for the candidate to be claimed as an in-
terpolant of φ and ψ. This can be achieved by solving the equivalent QE problems
∀x. φ(x, y)|x =⇒ I(x) and ∀x. I(x) ∧ ψ(x, z)|x =⇒ ⊥, where ·|x is the projection
to the common space over x. The candidate will be returned as an actual interpolant if
both formulae reduce to > after eliminating the universal quantifiers. The satisfiability
checking at line 1 can be solved analogously. Granted, the entailment checking can also
be encoded in SMT techniques by asking the satisfiability of the negation of the uni-
versally quantified predicates, however, limitations of current SMT solvers in nonlinear
arithmetic hinders them from being practically used in our framework, as demonstrated
later in Sect. 5.

Counterexample generation. If a candidate interpolant cannot be verified as an actual
one, then at least one witness can be found as a counterexample to that candidate, which
can be added to the set of sample points in the next iteration to refine further candidates
(cf. Fig. 2). Multiple counterexamples can be obtained at a time thereby effectively
reducing the number of future iterations.
    In general, we have little control over which counterexample will be returned by QE.
In the worst case, the counterexample can lie almost exactly on the hyperplane found
by SVM. This poses issues for the termination of the algorithm. We will address this
theoretical issue by slightly modifying the algorithm, as explained in Sect. 3.3 and 4.
8       M. Chen et al.

3.2   Comparison with the Naı̈ve QE-Based Method
Simply performing QE on ∃y. φ(x, y) yields already an interpolant for mutually contra-
dictory φ and ψ. Such an interpolant is actually the strongest in the sense of [12], which
presents an ordered family of interpolation systems due to the logical strength of the
synthesized interpolants. Dually, the negation of the result when performing QE over
∃z. ψ(x, z) is the weakest interpolant. However, as argued by D’Silva et al. in [12],
a good interpolant (approximation of φ or ψ) –when computing invariants of transi-
tion systems using interpolation-based model checking– should be coarse enough to
enable rapid convergence but strong enough to be contained within the weakest induc-
tive invariant. In contrast, the advantages of NIL are two-fold: first, it produces better
interpolants (in the above sense) featuring “medium” strength (due to the way optimal-
margin classifier is defined) which are thus more effective in practical use and further-
more resilient to perturbations in φ and ψ (i.e., the robustness shown later in Sect. 6);
second, NIL always returns a single polynomial inequality as the interpolant which is
often simpler than that derived from the naı̈ve QE-based method, where the direct pro-
jection of φ(x, y) onto the common space over x can be as complex as the original
φ.
    These issues can be avoided by combining this method with a template-based ap-
proach, which in turn introduces fresh quantifiers over unknown parameters to be elim-
inated. Note that in NIL the candidate interpolants I ∈ R[x]m under verification are
polynomials without unknown parameters, and therefore, in contrast to performing QE
over an assumed template, the learning-based technique can practically generate poly-
nomial interpolants of higher degrees (with acceptable rounds of iterations). For exam-
ple, NIL is able to synthesize an interpolant of degree 7 over 2 variables
                                                                         (depicted later
in Fig. 4(b)), which would require a polynomial template with 7+2     2    = 36 unknown
parameters that goes far beyond the capability of QE procedures.
    On the other hand, performing QE within every iteration of the learning process,
for entailment checking and generating counterexamples, limits the efficiency of the
proposed method, thereby confining NIL currently to applications only of small scales.
Potential solutions to the efficiency bottleneck will be discussed in Sect. 5.
3.3   Variants of NIL
While the above basic algorithm is already effective in practice (as demonstrated in
Sect. 5), it is guaranteed to terminate only when there is an interpolant with positive
functional margin between JφK and JψK. In this section, we present two variants of the
algorithm that have nicer theoretical properties in cases where the two sets are only
separated by an interpolant with zero functional margin, e.g., cases where JφK and JψK
share adjacent or even coincident boundaries.
Entailment checking with tolerance δ. When performing entailment checking for a
candidate interpolant I, instead of using, e.g., the formula p(x) ≥ 0 for I, we can
introduce a tolerance of δ. That is, we check the satisfiability of φ ∧ (p(x) < −δ) and
(p(x) ≥ δ) ∧ ψ instead of the original φ ∧ (p(x) < 0) and (p(x) ≥ 0) ∧ ψ. This
means that a candidate that is an interpolant “up to a tolerance of δ” will be returned
as a true interpolant, which may be acceptable in some applications. If the candidate
interpolant is still not verified, the counterexample is guaranteed to be at least a distance
                                              NIL: Learning Nonlinear Interpolants       9

of δ away from the separating hyperplane. Note the distance δ is taken in the feature
        ˜
space Rd , not in the original space. We let NILδ (φ,ψ,m) denote the version of NIL with
this modification (cf. Fig. 3). In the next section, we show NILδ (φ,ψ,m) terminates as
long as JφK and JψK are bounded, including the case where they are separated only by
interpolants of functional margin zero.
Varying tolerance during the execution. A further refinement of the algorithm can be
made by varying the tolerance δ during the execution. We also introduce a bounding box
B of the varying size to handle unbounded cases. Define algorithm NIL∗δ,B (φ, ψ, m)
as follows. Let δ1 = δ and B1 = B. For each iteration i, execute the core algorithm,
except that the counterexample must be a distance of at least δi away from the separating
                                                                             ˜
boundary, and have absolute value in each dimension at most B (both in Rd ). After the
termination of iteration i, begin iteration i + 1 with δi+1 = δi /2 and Bi+1 = 2Bi . This
continues until an interpolant is found or until a pre-specified cutoff. For any JφK and
JψK (without the boundedness condition), this variant of the algorithm converges to an
interpolant in the limit, which will be made precise in the next section.

4   Soundness, Completeness and Convergence
In this section, we present theoretical results obtained for the basic NIL algorithm and
its variants. Proofs are included in Appx. A due to the lack of space.
     First, the basic algorithm is sound, as captured by Theorem 1.
Theorem 1 (Soundness of NIL). If NIL(φ,ψ,m) terminates and returns I, then I is an
interpolant in R[x]m of φ and ψ.
    Under certain conditions, the algorithm is also terminating (and hence complete).
We prove two such situations below. In both cases, we require boundedness of the two
sets that we want to separate. In the first case, there exists an interpolant with positive
functional margin between the two sets.
Theorem 2 (Conditional Completeness of NIL). If JφK and JψK are bounded and
there exists an interpolant in R[x]m of φ and ψ with positive functional margin γ when
              ˜
mapped to Rd , then NIL(φ,ψ,m) terminates and returns an interpolant I of φ and ψ.
   The standard algorithm is not guaranteed to terminate when JφK and JψK are only
separated by interpolants of functional margin zero. However, the modified algorithm
NILδ (φ,ψ,m) does terminate (with the cost that the resulting answer is an interpolant
with tolerance δ).
Theorem 3 (Completeness of NILδ with zero margin). If JφK and JψK are bounded,
and δ > 0, then NILδ (φ,ψ,m) terminates. It returns an interpolant I of φ and ψ with
tolerance δ whenever such an interpolant exists.
    By iteratively decreasing δ during the execution of the algorithm, as well as intro-
ducing an iteratively increasing bounding box, as in NIL∗δ,B (φ, ψ, m), we can obtain
more and more accurate candidate interpolants. We now show that this algorithm con-
verges to an interpolant without restrictions on φ and ψ. We first make this convergence
property precise in the following definition.
10       M. Chen et al.

Definition 2 (Convergence of a sequence of equations to an interpolant). Given
two sets JφK and JψK that we want to separate, and an infinite sequence of equations
I1 , I2 , . . . , we say the sequence In converges to an interpolant of φ and ψ if, for each
point p in the interior of JφK or JψK, there exists some integer Kp such that Ik classifies
p correctly for all k ≥ Kp .

Theorem 4 (Convergence of NIL∗δ,B ). Given two regions JφK and JψK. Suppose there
exists an interpolant of φ and ψ, then the infinite sequence of candidates produced by
NIL∗δ,B (φ, ψ, m) converges to an interpolant in the sense of Definition 2.

5     Implementation and Experiments
5.1    Implementation Issues
We have implemented the core algorithm NIL as a prototype1 in Wolfram Mathemat-
ica with LIBSVM [5] being integrated as an engine to perform SVM classifications.
Despite featuring no completeness for adjacent JφK and JψK nor convergence for un-
bounded JφK or JψK, the standard NIL algorithm yields already promising results as
shown later in the experiments. Key Mathematica functions that are utilized include
R EDUCE, for entailment checking, e.g., the unsatisfiability checking of φ ∧ ψ and the
post-verification of a candidate interpolant, and F IND I NSTANCE, for generating coun-
terexamples and sampling initial points (when the random sampling strategy fails). The
R EDUCE command implements a decision procedure for TP and its appropriate exten-
sion to catering for transcendental functions (cf. [42]) based on cylindrical algebraic
decomposition (CAD), due to Collins [8]. The underlying quantifier-elimination proce-
dure, albeit inducing rather high computation complexity, cannot in practice be replaced
by SMT-solving techniques (by checking the negation of a universally quantified pred-
icate) as in the linear arithmetic. For instance, the off-the-shelf SMT solver Z3 fails
to accomplish our tasks particularly when the coefficients occurring in the entailment
problem to be checked get larger2 .
Numerical errors and rounding. LIBSVM conducts floating-point computations for
solving the optimization problems induced by SVMs and consequently yields numeri-
cal errors occurring in the candidate interpolants. Such numerical errors may block an
otherwise valid interpolant from being verified as an actual one and additionally bring
down the simplicity and thereby the effectiveness of the synthesized interpolant, thus
not very often proving humans with clear-cut understanding. This is a common issue for
approaches that reduce the interpolation problem to numerical solving techniques, e.g.
SDP solvers exploited in [10, 13, 32], while an established method to tackle it is known
as rational recovery [28, 46], which retrieves the nearest rational number from the con-
tinued fraction representation of its floating-point approximation at any given accuracy
(see e.g. [46] for theoretical guarantees and [32] for applications in interpolation). The
algorithm implementing rational recovery has been integrated in our implementation
and the consequent benefits are two-fold: (i) NIL can now cope with interpolation tasks
 1
     Available at http://lcs.ios.ac.cn/˜chenms/tools/NIL.tar.bz2
 2
     As can be also observed at https://github.com/Z3Prover/z3/issues/1765
                                              NIL: Learning Nonlinear Interpolants      11

where only exact coefficients suffice to constitute an actual interpolant while any numer-
ical error therein will render the interpolant invalid, e.g., cases where JφK and JψK share
parallel, adjacent, or even coincident boundaries, as demonstrated later by examples
with ID 10–17 in Table 1; (ii) rationalizing coefficients moreover facilitates simplifi-
cations over all of the candidate interpolants and therefore practically accelerating the
entailment checking and counterexample generation processes, which in return yields
simpler interpolants, as shown in Table 2 in the following section.
5.2   Benchmark and Experimental Results
Table 1 collects a group of benchmark examples from the literature on synthesizing non-
linear interpolants as well as some geometrically contrived ones. All of the experiments
have been evaluated on a 3.6GHz Intel Core-i7 processor with 8GB RAM running 64-
bit Ubuntu 16.04.
    In Table 1, we group the set of examples into four categories comprising 20 cases
in total. For each example, ID numbers the case, φ, ψ and I represent the two formulas
to be interpolated and the synthesized interpolant by our method respectively, while
Time/s indicates the total time in seconds for interpolation. The categories are described
as follows, and the visualization of a selected set of typical examples thereof is further
depicted in Fig. 4.
Cat. I: with/without rounding. This category includes 9 cases, for which our method
generates the polynomial interpolants correctly with or without the rounding operation.
Cat. II: with rounding. For cases 10 to 17 in this category, where JφK and JψK share
parallel, adjacent, or even coincident boundaries, our method produces interpolants suc-
cessfully with the rouding process based on rational recovery.
Cat. III: beyond polynomials. This category encloses two cases beyond the theory
TP of polynomials: for case 18, a verified polynomial interpolant is obtained in spite of
the transcendental term in ψ; while for case 19, the SVM classification fails since JφK
and JψK are not linearly separable in any finite-dimensional feature space and hence no
polynomial interpolant exists for this example. Note that our counterexample-guided
learning framework admits a straightforward extension to a decidable fragment of more
general nonlinear theories involving transcendental functions, as investigated in [42].
Cat. IV: unbalanced. The case 20, called Unbalanced, instantiates a particular sce-
nario where φ and ψ have extraordinary “unbalanced” number of models that make
them true respectively. For this example, there are an infinite number of models satis-
fying φ yet one single model (i.e., x = 0) satisfying ψ. The training process in SVMs
may fail when encountering extremely unbalanced number of positive/negative sam-
ples. This is solved by specifying a weight factor for the positive set of samples as the
number of negative ones, and dually for the other way around, to balance biased num-
ber of training samples before triggering the classification. Such a balancing trick is
supported in LIBSVM.
Remark that examples named CAV13-1/3/4 are taken from [10] (and the latter two orig-
inally from [27] and [17] respectively), where interpolation is applied to discovering
inductive invariants in the verification of programs and hybrid systems. For instance,
CAV13-3 is a program fragment describing an accelerating car and the synthesized in-
terpolant by NIL suffices to prove the safety property of the car concerning its velocity.
                                                                                          Table 1: Benckmark examples for synthesizing nonlinear interpolants.
                 Category     ID Name              φ                                                    ψ                                                  I                                                                                  Time/s
                              1   Dummy            x < −1                                               x ≥ 1                                              x < 0                                                                              0.11
                              2   Necklace         y − x2 − 1 = 0                                       y + x2 + 1 = 0                                     −y < 0                                                                             0.21
                                                                                                                                                            x4          x3 y   2 y
                                                                                                                                                                                   2                            y         2
                                                                                                                                                                   −         +x (    −                               −        )+
                                                                                                            2        2                                     223          356                    45           170           9
                                                                                                        x       +y       − 64 ≤ 0∧
                                                              2        2
                                                   (x + 4)        +y       − 1 ≤ 0∨
                                                                                                                     2        2                                 y3          y2            y            1            y4
                              3   Face                                                                  (x + 4)          +y       − 9 ≥ 0∧                 x(          +         −             −            )+            +                   0.33
                                                              2        2
                                                   (x − 4)        +y       −1 ≤ 0                                                                               89          68           74            55           146
                                                                                                               2   2
                                                                                                        (x − 4) + y − 9 ≥ 0
                                                                                                                                                           y3           y2           y
                                                                                                                                                                   +         +                +1 < 0
                                                                                                                                                           95           37           366
                                                    2     2          2
                                                   x − 2xy + 3xz − y
                                                           2
                                                                                                                                                                                                              
                                                   − yz + z − 1 ≥ 0∧                                                                                          x4    3
                                                                                                                                                                        y      1   
                                                                                                                                                                                         2     y 2     y    2
                                                                                                                                                           −      +x         −        + x −        +    +     +
                                                    1     6   6
                                                                 
                                                                      2 2                                   2             4         2                        160        170    113            225     76    27
                                                        −x − y     +x z −                               w       + 4(x − y) + (x + y) − 80 ≤ 0∧
                              4   Twisted                                                                                                                                                                               140.62
                                                   120                                                      2       4            2
                                                                                                                                                                                    
                                                                                                         − w (x − y) + 100(x + y) − 3000 ≥ 0                  y3    y2    5y      1       y4     y3     y2     y
                                                    2   1  4     2 2     4
                                                                            
                                                                                                                                                           x     +    +      −      −       −      +     +     −1 < 0
                                                   x +     x + 2x y + y       +                                                                               259   63     51   316       183     94    14   255
                                                        6
                                                    2 2    2
                                                   y z −y −4 ≤ 0
                                                                                                                                                           x7    6   y   1     5 2y
                                                                                                                                                                                    2    y   1
                                                                                                                                                              + x (−   −    )+x (     −    − )+
                                                                                                                                                           27        5   96        9    32   2
                                                     2   2                                                                    2        2                          3                 4
                                                   (x + y − 3.8025 ≤ 0 ∧ y ≥ 0∨                         (−3.8025 + x              +y       ≤ 0 ∧ −y ≥ 0∨    4   2y    y   1     3 y     y3   10y 2   y    15
                                                                                                                                                           x (−              +
                                                                                                                                                                             )+x (    +  + −       +    +    )+
                                                              2        2                                                    2   2                                       9          113  10    31
                                                                                                                                                                                               13    18   16
                                                   (x − 1)        +y       − 0.9025 ≤ 0)∧                − 0.9025 + (−1 − x) + y ≤ 0)∧
                 with/without                                                                                                                                   y       5        y4            y3           y2            1
                                                              2        2                                                  2   2                             2
                              5   Ultimate         (x − 1)        +y       − 0.09 > 0∧                   − 0.09 + (−1 − x) + y > 0∧                        x (−              −            −            +            −         )+              48.82
                 rounding
                                                              2        2                                                   2   2                                       25        18            3            10           32
                                                   (x + 1)        +y       − 1.1025 ≥ 0∨                 − 1.1025 + (1 − x) + y ≥ 0∨                                                                                              
                                                                                                                                                                   y6        2y 4             y3            2        y         3
                                                              2        2       1                                1          2   2                           x           +                −          −y          −         −        +
                                                   (x + 1)        +y       −        ≤ 0                  −        + (1 − x) + y ≤ 0                                71        11               25                     45        8
                                                                               25                               25
                                                                                                                                                           y6           y5           y4        y3            y2           y        1
                                                                                                                                                                   −         +             −            −           −          +        < 0
                                                                                                                                                           48           7            6             2            6         59       85
                                                       2
                                                   − x1 + 4x1 + x2 − 4 ≥ 0∧                                                                                        3x1  x
                              6   IJCAR16-1 [13]                                                           2 − x2 + 1 ≥ 0 ∧ x − z 2 ≥ 0
                                                                                                        −3x1                                               1−          − 2 < 0                                                                0.16
                                                                    2                                           2            2                                      4    2
                                                   − x1 − x2 + 3 − y > 0
                                                        2   2        2
                                                   1 − a − b > 0 ∧ a + b − 1 − x = 0∧                                                                             2 y   xy   y2
                              7   CAV13-1 [10]                                                          x2 − 2y 2 − 4 > 0                                  −1 + x −   +    −    < 0                                                           3.25
                                                                                                                                                                 2  3    3    4
                                                   b + bx + 1 − y = 0
                                                                                                                                                               4   2     2
                                                                                                                                                           105x + x (140y + 24y(5z + 7) + 35z(3z + 8))+
                                                    2   2   2                                                  2    3     2                                     3      2    2                    3    2
                                                   x + y + z − 2 ≥ 0∧                                   20 − 3x − 4y − 10z ≥ 0∧                            2(70y z + 5y (12z + 21z + 28) − 14y(6z + 5z +
                              8   CAV13-2 [10]                                                                                                                                                                                                3857.89
                                                          2        2                                     2  2                                                                    4            2                        2
                                                   1.2x       +y       + xz = 0                         x +y −z−1 = 0                                      10) − 35(3z               + 8z          + 4z − 9)) < 14x(20x (z + 1)+
                                                                                                                                                              2               2                 2
                                                                                                                                                           10y (z + 2) − 3y(4z − 5z + 4) − 20z(z + 2))
                                                                              2
                                                   vc < 49.61 ∧ f a = 0.5418vc ∧
                                                                                                                                                                       2vc1
                              9   CAV13-3 [10]     f r = 1000 − f a ∧ ac = 0.0005f r∧                   vc1 ≥ 49.61                                        −1 +             < 0                                                               40.63
                                                                                                                                                                        99
                                                   vc1 = vc + ac
M. Chen et al.




                              10 Parallel parabola y − x2 − 1 ≥ 0                                       y − x2 < 0                                         1 + x2 < y                                                                         4.50
                                                                                                                                                           2
                              11 Parallel halfplane y − x − 1 ≥ 0                                       y−x+1 < 0                                          x < y                                                                              2.46
                              12 Sharper-1 [32]     y+1 < 0                                             x2 + y 2 − 1 ≤ 0                                   2 + y < y2                                                                         2.19
                              13 Sharper-2 [32]     y−x > 0∧x+y > 0                                     y + x2 <= 0                                        y > 0                                                                              2.38
                              14 Coincident         x+y > 0∨x+y < 0                                     x+y = 0                                            (x + y)2 > 0                                                                       0.18
                              15 Adjacent           y − x2 > 0                                          y − x2 <= 0                                        x2 < y                                                                             0.25
                 with                              − y1 + x1 − 2 ≥ 0 ∧ 2x2 − x1 − 1 > 0∧                 − z1 + 2x2 + 1 ≥ 0 ∧ 2x1 − x2 − 1 > 0∧
                 rounding
                                                       2   2                                                2     2
                              16 IJCAR16-2 [13]    − y1 − x1 + 2x1 y1 − 2y1 + 2x1 ≥ 0∧                   − z1 − 4x2 + 4x2 z1 + 3z1 − 6x2 − 2 ≥ 0∧ x1 < x2                                                                                     12.33
                                                       2   2    2                                           2    2    2
                                                   − y2 − y1 − x2 − 4y1 + 2x2 − 4 ≥ 0                    − z2 − x1 − x2 + 2x1 + z1 − 2x2 − 1 ≥ 0
                                                   xa1 + 2ya1 ≥ 0 ∧ xa1 + 2ya1 − x1 = 0∧
                              17 CAV13-4 [10]      − 2xa1 + ya1 − y1 = 0 ∧ x − x1 − 1 = 0∧ xa + 2ya < 0                                                    2xa + 4ya > 5                                                                      3.10
                                                   y = y1 + x ∧ xa = x − 2y ∧ ya = 2x + y
12


                 beyond      18 TACAS16 [14]       y − x2 ≥ 0                                           y + cos x − 0.8 ≤ 0                                15x2 < 4 + 20y                                                                     12.71
                 polynomials 19 Transcendental     sin x ≥ 0.6                                          sin x ≤ 0.4                                        SVM failed                                                                         –
                 unbalanced   20 Unbalanced        x > 0∨x < 0                                          x = 0                                              x2 > 0                                                                             0.11
                                                                                                          NIL: Learning Nonlinear Interpolants                                        13


                                                                       3
      3                                                                                                                              10




                                                                       2
      2



                                                                                                                                     5



      1                                                                1




x2    0                                                            y   0                                                        y    0




     -1                                                                -1



                                                                                                                                    -5



     -2                                                                -2




     -3                                                                -3                                                           -10
          -3        -2         -1   0      1           2       3            -3        -2         -1   0     1       2       3             -10        -5          0            5        10
                                    x1                                                                x                                                          x




                          (a) Adjacent                                                     (b) Ultimate                                                    (c) Twisted


     4                                                                 4                                                             4




     2                                                                 2                                                             2




y    0                                                             y   0                                                        y    0




     -2                                                                -2                                                           -2




     -4                                                                -4                                                           -4




               -4         -2        0          2           4                     -4         -2        0         2       4                       -4        -2     0        2       4
                                    x                                                                 x                                                          x




                    (d) Parallel parabola                                                  (e) Coincident                                                 (f) Sharper-2


                                                                                                                                     4



     5




                                                                                                                                     2




y    0                                                                                                                          y    0




                                                                                                                                    -2




     -5



                                                                                                                                    -4




                     -5             0              5                                                                                            -4        -2     0        2       4
                                    x                                                                                                                            x




                                (g) Face                                                         (h) CAV13-2                                              (i) TACAS16

     Fig. 4: Visualization in NIL on a selected set of examples. Legends: gray region: JφK, blue region: JψK, pink region: JIK with
     a valid interpolant I, red dots: X + , blue dots: X − , circled dots: support vectors. Sample points are hidden in 3D-graphics
     for a clear presentation.


     Applicability and comparison with existing approaches. As shown in Table 1, our
     learning-based technique succeeds in all of the benchmark examples that admit poly-
     nomial interpolants. Due to theoretical limitations of existing approaches as elaborated
     in Sect. 1, none of the aforementioned methods can cope with as many cases in Table 1
     as NIL can. For instances, the Twisted example as depicted in Fig. 4(c) falls beyond
     the scope of concave quadratic formulas and thus cannot be addressed by the approach
     in [13], while the Parallel parabola example as shown in Fig. 4(d) needs an infinite com-
     bination of linear constraints as an interpolant when performing the technique in [14]
     and hence not of practical use, to name just a few. Moreover, we list in Table 2 a com-
     parison of the synthesized interpolants against works where the benchmark examples
     are collected from. As being immediately obvious from Table 2, our technique often
14               M. Chen et al.


                                                Table 2: Comparison of the synthesized interpolants.

Name             Interpolants by NIL                                              Interpolants from the sources

                    3x1  x
IJCAR16-1 [13]   1−     − 2 < 0                                                   −3 + 2x1 + x2   1 2
                                                                                              1 + 2 x2 > 0
                     4    2
                        2 y   xy   y2
CAV13-1 [10]     −1 + x −   +    −    < 0                                         436.45(x2 − 2y 2 − 4) + 1 ≤ 0
                       2  3    3    4                                                                     2
                                                                                                                       2
                                                                                   − 14629.26 + 2983.44x3 + 10972.97x3 +
                                                                                                                    2           2
                                                                                   297.62x2 + 297.64x2 x3 + 0.02x2 x3 + 9625.61x2 −
                                                                                           2           2 2           3
                                                                                   1161.80x2 x3 + 0.01x2 x3 + 811.93x2 +
                         4      2     2                                                    4
                  105x       + x (140y + 24y(5z + 7) + 35z(3z + 8))+               2745.14x2 − 10648.11x1 + 3101.42x1 x3 +
                       3      2    2                    3    2                                 2
                  2(70y z + 5y (12z + 21z + 28) − 14y(6z + 5z +                    8646.17x1 x3 + 511.84x1 x2 − 1034x1 x2 x3 +
CAV13-2 [10]
                                 4          2                         2                       2              2              2
                  10) − 35(3z        + 8z       + 4z − 9)) < 14x(20x (z + 1)+      0.02x1 x2 x3 + 9233.66x1 x2 + 1342.55x1 x2 x3 −
                     2               2                 2                                      3            2            2
                  10y (z + 2) − 3y(4z − 5z + 4) − 20z(z + 2))                      138.70x1 x2 + 11476.61x1 − 3737.70x1 x3 +
                                                                                            2 2                           2
                                                                                   4071.65x1 x3 − 2153.00x12 x2 + 373.14x1 x2 x3 +
                                                                                            2 2           3           3
                                                                                   7616.18x1 x2 + 8950.77x1 + 1937.92x1 x3 −
                                                                                         3              4
                                                                                   64.07x1 x2 + 4827.25x1 > 0

                         2vc1
CAV13-3 [10]     −1 +         < 0                                                 −1.3983vc1 + 69.358 > 0
                          99

Sharper-1 [32]   2 + y < y2                                                       34y 2 − 68y − 102 ≥ 0

Sharper-2 [32]   y > 0                                                            8y + 4x2 > 0

IJCAR16-2 [13]   x1 < x2                                                          −x1 + x2 > 0

                                                                                                                  2            3
                                                                                   716.77 + 1326.74(ya) + 1.33(ya) + 433.90(ya) +
CAV13-4 [10]     2xa + 4ya > 5                                                                                                 2
                                                                                   668.16(xa) − 155.86(xa)(ya) + 317.29(xa)(ya) +
                                                                                             2            2                 3
                                                                                   222.00(xa) + 592.39(xa) (ya) + 271.11(xa) > 0

                                                                                   y > 1.8 ∨ (0.59 ≤ y ≤ 1.8 ∧ −1.35 ≤ x ≤ 1.35)∨
TACAS16 [14]     15x2 < 4 + 20y                                                    (0.09 ≤ y < 0.59 ∧ −0.77 ≤ x ≤ 0.77)∨
                                                                                   (y ≥ 0 ∧ −0.3 ≤ x ≤ 0.3)




produces interpolants of simpler forms, particularly for examples CAV13-2, CAV13-4
and TACAS16. Such a simplicity benefits from both the rounding effect and the form
of interpolant (i.e., a single polynomial inequality) that we tend to construct.
Bottleneck of efficiency and potential solutions. The current implementation of NIL
works promisingly for small examples; it does not scale to interpolation problems with
large numbers of common variables, as reported in Table 1. The bottleneck stems from
quantifier eliminations performed within every iteration of the learning process, for
entailment checking and generating counterexamples. We pose here several potential
solutions that are expected to significantly reduce computational efforts: (i) substitute
general purpose QE procedure that perform CAD by the so-called variant quantifier-
elimination (VQE) algorithm [20], which features singly-exponential complexity in the
number of variables. This however requires a careful inspection of whether our problem
meets the geometric conditions imposed by VQE; (ii) incorporate relaxation schemes,
e.g., Lagrangian relaxation and sum-of-squares decompositions [33], and complement
with QE only when the relaxation fails to produce desired results.

6        Taming Perturbations in Parameters.
An interpolant synthesized by the SVM-based technique features inherent robustness
due to the way optimal-margin classifier is defined (Sect. 2). That is, the validity of such
an interpolant is not easily perturbed by changes (in the feature space) in the formulae
                                                                     NIL: Learning Nonlinear Interpolants                       15




                   5                                                      5




                                                            
                                                 
                                                     
               y   0                                                  y   0




                   -5                                                     -5




                             -5               0           5                         -5          0            5
                                              x                                                 x



                        (a) -perturbations in the radii                   (b) Interpolant resilient to perturbations

Fig. 5: -Face: introducing perturbations (with  up to 0.5) in the Face example. The synthesized interpolant is resilient to
any -perturbation in the radii satisfying −0.5 ≤  ≤ 0.5.


to be interpolated. It is straightforward in NIL to deal with interpolation problems under
explicitly specified perturbations, which are treated as constraints over fresh variables.
An example named -Face is depicted in Fig. 5, which perturbs hφ, ψi in the Face
example as φ = b − 0.5 ≤ 1 ≤ 0.5 ∧ ((x + 4)2 + y 2 − (1 + 1 )2 ≤ 0 ∨ (x − 4)2 + y 2 −
        2
(1+1 ) ≤ 0) and ψ =    b −0.5 ≤ 2 ≤ 0.5∧x2 +y 2 −64 ≤ 0∧(x+4)2 +y 2 −(3+2 )2 ≥
0 ∧ (x − 4) + y − (3 + 2 )2 ≥ 0. The synthesized
            2     2
                                                       interpolant over common
                                                                                 variables
                                          3
                        4                         y2                            3        2                              4   3
              x
of φ and ψ is 139 + x268y + x2                         11
                                                  39 − 36          + x − y52 − 157
                                                                               y     y
                                                                                   − 52    1
                                                                                        − 116 + y25 − 182
                                                                                                      y
                                                                                                          +
2y 2   y
 19 − 218 + 1 < 0 which is hence resilient to any -perturbation in the radii satisfying
−0.5 ≤  ≤ 0.5, as illustrated in Fig. 5(b).

7     Conclusions
We have presented a unified, counterexample-guided method named NIL for generating
polynomial interpolants over the general quantifier-free theory of nonlinear arithmetic.
Our method is based on classification techniques with space transformations and kernel
tricks as established in the community of machine-learning. We proved the soundness
of NIL and proposed sufficient conditions for its completeness and convergence. The
applicability and effectiveness of our technique are demonstrated experimentally on a
collection of representative benchmarks from the literature, including those extracted
from program verification. Experimental results indicated that our method suffices to
address more interpolation tasks, including those with perturbations in parameters, and
in many cases synthesizes simpler interpolants compared with existing approaches.
    For future work, we would like to improve the efficiency of NIL by substituting the
general purpose quantifier-elimination procedure with alternative methods previously
discussed in Sect. 5. An extension of our approach to cater for the combination of non-
linear arithmetic with EUFs, by resorting to predicate-abstraction techniques [22], will
be of particular interest. Additionally, we plan to investigate the performance of NIL
over different classification techniques, e.g., the widespread regression-based meth-
ods [18], though SVMs are expected to be more competent concerning the robustness
and predictability, as also observed in [36].
16       M. Chen et al.

References
 1. K. P. Bennett and E. J. Bredensteiner. Duality and geometry in SVM classifiers. In ICML’00,
    pages 57–64, 2000.
 2. C. M. Bishop. Pattern recognition and machine learning, pages 326–328. Springer, 2006.
 3. B. E. Boser, I. Guyon, and V. Vapnik. A training algorithm for optimal margin classifiers. In
    COLT’92, pages 144–152, 1992.
 4. N. Bourbaki. Topological Vector Spaces. Elements of Mathematics. Springer-Verlag, 1987.
 5. C. Chang and C. Lin. LIBSVM: A library for support vector machines. ACM TIST,
    2(3):27:1–27:27, 2011.
 6. A. Cimatti, A. Griggio, and R. Sebastiani. Efficient interpolant generation in satisfiability
    modulo theories. In TACAS’08, pages 397–412, 2008.
 7. E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. Counterexample-guided abstraction
    refinement. In CAV’00, pages 154–169, 2000.
 8. G. E. Collins. Quantifier elimination for real closed fields by cylindrical algebraic decom-
    postion. In H. Brakhage, editor, Automata Theory and Formal Languages 2nd GI Conference
    Kaiserslautern, pages 134–183, Berlin, Heidelberg, 1975. Springer Berlin Heidelberg.
 9. W. Craig. Linear reasoning. A new form of the herbrand-gentzen theorem. J. Symb. Log.,
    22(3):250–268, 1957.
10. L. Dai, B. Xia, and N. Zhan. Generating non-linear interpolants by semidefinite program-
    ming. In CAV’13, pages 364–380, 2013.
11. S. Dathathri, N. Arechiga, S. Gao, and R. M. Murray. Learning-based abstractions for non-
    linear constraint solving. In IJCAI’17, pages 592–599, 2017.
12. V. D’Silva, D. Kroening, M. Purandare, and G. Weissenbacher. Interpolant strength. In
    VMCAI’10, pages 129–145, 2010.
13. T. Gan, L. Dai, B. Xia, N. Zhan, D. Kapur, and M. Chen. Interpolant synthesis for quadratic
    polynomial inequalities and combination with EUF. In IJCAR’16, pages 195–212, 2016.
14. S. Gao and D. Zufferey. Interpolants in nonlinear theories over the reals. In TACAS’16, pages
    625–641, 2016.
15. S. Gilbert. A nullstellensatz and a positivstellensatz in semialgebraic geometry. Mathema-
    tische Annalen, 207(2):87–97, 1974.
16. S. Graf and H. Saı̈di. Construction of abstract state graphs with PVS. In CAV’97, pages
    72–83, 1997.
17. B. S. Gulavani, S. Chakraborty, A. V. Nori, and S. K. Rajamani. Automatically refining
    abstract interpretations. In TACAS’08, pages 443–458, 2008.
18. T. Hastie, R. Tibshirani, and J. H. Friedman. The elements of statistical learning: data
    mining, inference, and prediction, 2nd Edition. Springer series in statistics. Springer, 2009.
19. T. A. Henzinger, R. Jhala, R. Majumdar, and K. L. McMillan. Abstractions from proofs. In
    POPL’04, pages 232–244, 2004.
20. H. Hong and M. S. E. Din. Variant quantifier elimination. J. Symb. Comput., 47(7):883–901,
    2012.
21. S. Jha, S. Gulwani, S. A. Seshia, and A. Tiwari. Oracle-guided component-based program
    synthesis. In ICSE’10, pages 215–224, 2010.
22. R. Jhala, A. Podelski, and A. Rybalchenko. Predicate abstraction for program verification.
    In Handbook of Model Checking., pages 447–491. 2018.
23. Y. Jung, W. Lee, B. Wang, and K. Yi. Predicate generation for learning-based quantifier-free
    loop invariant inference. In TACAS’11, pages 205–219, 2011.
24. D. Kapur, R. Majumdar, and C. G. Zarba. Interpolation for data structures. In FSE’06, pages
    105–116, 2006.
25. L. Kovács and A. Voronkov. Interpolation and symbol elimination. In CADE’09, pages
    199–213, 2009.
                                                  NIL: Learning Nonlinear Interpolants          17

26. J. Krajı́ček. Interpolation theorems, lower bounds for proof systems, and independence re-
    sults for bounded arithmetic. J. Symb. Log., 62(2):457–486, 1997.
27. S. Kupferschmid and B. Becker. Craig interpolation in the presence of non-linear constraints.
    In FORMATS’11, pages 240–255, 2011.
28. S. Lang. Introduction to Diophantine Approximations: New Expanded Edition. Springer
    New York, 2012.
29. K. L. McMillan. Interpolation and sat-based model checking. In CAV’03, pages 1–13, 2003.
30. K. L. McMillan. An interpolating theorem prover. In TACAS’04, pages 16–30, 2004.
31. K. L. McMillan. Quantified invariant generation using an interpolating saturation prover. In
    TACAS’08, pages 413–427, 2008.
32. T. Okudono, Y. Nishida, K. Kojima, K. Suenaga, K. Kido, and I. Hasuo. Sharper and simpler
    nonlinear interpolants for program verification. In APLAS’17, pages 491–513, 2017.
33. P. A. Parrilo. Semidefinite programming relaxations for semialgebraic problems. Math.
    Program., 96(2):293–320, 2003.
34. P. Pudlák. Lower bounds for resolution and cutting plane proofs and monotone computations.
    J. Symb. Log., 62(3):981–998, 1997.
35. A. Rybalchenko and V. Sofronie-Stokkermans. Constraint solving for interpolation. In VM-
    CAI’07, pages 346–362, 2007.
36. R. Sharma, A. V. Nori, and A. Aiken. Interpolants as classifiers. In CAV’12, pages 71–87,
    2012.
37. V. Sofronie-Stokkermans. Interpolation in local theory extensions. In IJCAR’06, pages 235–
    250, 2006.
38. V. Sofronie-Stokkermans. On interpolation and symbol elimination in theory extensions. In
    IJCAR’16, pages 273–289, 2016.
39. A. Solar-Lezama, R. M. Rabbah, R. Bodı́k, and K. Ebcioglu. Programming by sketching for
    bit-streaming programs. In PLDI’05, pages 281–294, 2005.
40. A. W. Strzeboński. Real root isolation for exp-log functions. In ISSAC’08, pages 303–314,
    2008.
41. A. W. Strzeboński. Real root isolation for tame elementary functions. In ISSAC’09, pages
    341–350, 2009.
42. A. W. Strzeboński. Cylindrical decomposition for systems transcendental in the first variable.
    J. Symb. Comput., 46(11):1284–1290, 2011.
43. A. Tarski. A Decision Method for Elementary Algebra and Geometry. University of Califor-
    nia Press, Berkeley, 1951.
44. V. Vladimir. Pattern recognition using generalized portrait method. Automation and remote
    control, 24:774–780, 1963.
45. G. Yorsh and M. Musuvathi. A combination method for generating interpolants. In
    CADE’05, pages 353–368, 2005.
46. J. Zhang and Y. Feng. Obtaining exact value by approximate computations. Science in China
    Series A: Mathematics, 50(9):1361, 2007.
18       M. Chen et al.

Appendix A          Proofs of Theorems
Proof (of Theorem 1). The argument follows immediately from the checking, done in
line 10, of the definition of interpolant (Def. 1), and the fact that any candidate inter-
polant is of maximum degree m.                                                          t
                                                                                        u
Proof (of Theorem 2). Suppose the algorithm does not terminate. Then there must be
an infinite sequence of counterexamples. In particular, the sequence of counterexamples
added to either X + or X − must be infinite. Without loss of generality, we assume an
infinite sequence of counterexamples x1 , x2 , . . . are added to X + , whose initial set of
points is X0+ .
                                              ˜
     Let γi be the functional margin in Rd for the separating hyperplane Pi before the
counterexample xi is found. We claim that γi ≥ γ. This is because the convex hull of
X + and X − are subsets of JφK and JψK, respectively. Since there exists a hyperplane
separating JφK and JψK with functional margin γ, the same hyperplane also separates
conv(X + ) and conv(X − ). Since SVM maximizes the functional margin, the actual
hyperplane found by SVM must have functional margin at least γ.
     Next, we claim dist(xi , xj ) ≥ γ/2 for any i < j. Since xj is a counterexample
found when X + contains x1 , . . . , xj−1 , it lies on the other side of the hyperplane Pi
from x1 , . . . , xj−1 . Since the distance between any point on Pi and the convex hull of
X0+ ∪ {x1 , . . . , xj−1 } is at least γi /2 ≥ γ/2, the same holds for xj . In particular, the
distance between xj and each of the points x1 , . . . , xj−1 is at least γ/2.
     In other words, the balls B(xi , γ/4) are disjoint from each other. Their total volume
is infinite. However, they are contained in the set of points whose distance to JφK is at
most γ/4. This contradicts with the assumption that JφK is bounded.                          t
                                                                                             u
Proof (of Theorem 3). The proof is analogous to that of Theorem 2. Again, we assume
an infinite sequence of counterexamples x1 , x2 , . . . added to X + . Since the entailment
checking is performed with tolerance δ, each counterexample must have a distance of
at least δ away from the separating hyperplane. This means that the distance between a
counterexample xn and each existing one x1 , . . . , xn−1 is at least δ. Hence, the balls
B(xi , δ/2) are disjoint from each other and their total volume is infinite. However, they
are contained in the set of points whose distance to JφK is at most δ/2, which contradicts
the fact that JφK is bounded.                                                            t
                                                                                         u
Proof (of Theorem 4). Each iteration of NIL∗δ,B (φ, ψ, m) can be considered as a run
of algorithm NILδ with tolerance δ = δi , where the two regions are replaced by JφK ∩
          ˜                     ˜
[−B, B]d and JψK∩[−B, B]d . The two regions are clearly bounded, hence by Theorem
3, each iteration of NIL∗δ,B (φ, ψ, m) terminates. Given any point p in the interior of
either JφK or JψK, we need to show that there exists some integer Kp such that Ik
classifies p correctly for all k ≥ Kp . Since each iteration of the algorithm terminates,
it suffices to show the existence of an integer i such that p is classified correctly after
the i-th iteration. We take i sufficiently large so that the open ball B(p, δi ) lies entirely
in the region containing p (which is possible since p is in the interior and δi converges
to 0), and the absolute value of p in each dimension is at most Bi (which is possible
since Bi tends to infinity). It is then clear that p will be correctly classified after the i-th
iteration.                                                                                    t
                                                                                              u
