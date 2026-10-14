                                                   A BLUEPRINT FOR THE FORMALIZATION OF
                                              NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES FOR
                                                        COMMUTING TRANSFORMATIONS

                                                  FLORIS VAN DOORN, POLONA DURCIK, JORIS ROOS, LENKA SLAVÍKOVÁ,
                                                                      AND CHRISTOPH THIELE
arXiv:2608.27321v1 [math.DS] 27 Aug 2026




                                                  Abstract. This blueprint serves as a companion to a forthcoming, shorter traditional
                                                  mathematical paper. The purpose of this blueprint is two-fold: first, it has served as
                                                  the foundation for a formalization in Lean 4 of these results. This formalization has
                                                  been completed largely automatically, making essential use of current frontier large
                                                  language models. Second, it will serve as a resource to readers of the main paper who
                                                  are interested in further technical details of the proofs.
                                                     The main result concerns norm-variation estimates for multiple ergodic averages
                                                  associated with n ≥ 2 commuting measure preserving transformations, providing a
                                                  quantitative strengthening of Tao’s norm-convergence theorem and answering an open
                                                  question of Avigad and Rute. At the core of the analysis lies an explicit real-variable
                                                  estimate for twisted multilinear averages that is closely related to certain singular
                                                  Brascamp–Lieb inequalities.



                                                                                  1. Introduction
                                             Let n be a natural number, X a measurable space and µ a measure on X. Recall
                                           that that a map T : X → X is called a measure preserving transformation if for every
                                           measurable A ⊂ X the set T −1 (A) is measurable and has the same measure as A. For
                                           a non-negative integer n let [n) = {k ∈ N : 0 ≤ k < n}.
                                           Definition 1.1 (Multiple ergodic average ∀ ). Let f = (fj )j∈[n) be an n-tuple of complex-
                                           valued functions on X and let (Tj )j∈[n) be an n-tuple of maps X → X. For every positive
                                           integer N and every x ∈ X, define the multiple ergodic average
                                                                                          X Y
                                                                    MN (f )(x) = N −1              fj (Tji x).                  (1.1)
                                                                                             i∈[N ) j∈[n)

                                           Theorem 1.2 (Main ergodic theorem ∀ ). Let n ≥ 2 be an integer and let r > 2n−1 ,
                                           or r ≥ 2 if n = 2. Let (X, Σ, µ) be a σ-finite measure space, let (Tj )j∈[n) be an n-tuple
                                           of mutually commuting measure preserving transformations on X, and let f = (fj )j∈[n)
                                           be an n-tuple of complex-valued measurable functions on X such that ∥fj ∥L2n (X) < ∞
                                           for all j ∈ [n). Then MN (f ) is measurable with finite L2 (X) norm for every positive
                                           integer N and                                           Y
                                                                   ∥MN (f )∥Vr (L2 (X)) ≤ C1.2,n,r   ∥fj ∥2n ,                  (1.2)
                                                                                                       j∈[n)

                                             Date: August 28, 2026.
                                             2020 Mathematics Subject Classification. Primary 42B20, 37A30; Secondary 42B15, 68V20.
                                                                                            1
2                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE
                                                                                                   1/r
                                  344                                       4n+337         r
where for n = 2, C1.2,2,r = 2           , and, for n ≥ 3, C1.2,n,r = 2                   r−2n−1
                                                                                                           .

   The definition of the r-variation norm is given in Definition 4.2. Since finite variation
of a sequence implies convergence of the sequence and since L∞ (X) ⊂ L2n (X) if X is a
probability space, Theorem 1.2 immediately recovers Tao’s theorem [21, Theorem 1.1]
for n ≥ 2, which concerned qualitative norm convergence. Ergodic-theoretic proofs of
Tao’s theorem were also given by Austin [1], Host [13], and a generalization to nilpotent
groups was proved in [22]. Norm-convergence for a single ergodic average with n = 1
and r ≥ 2 was proved by Jones, Ostrovskii, and Rosenblatt [14]. Theorem 1.2 answers
a question that was stated by Avigad and Rute in the closing section of [2]. Versions of
Theorem 1.2 were proved for n = 2 in [6, 17], and for n = 3 in [9].
   Theorem 1.2 is reduced to Theorem 1.4 below by the Calderón transference principle;
see [6] and Pernegger [20], who also formalized this reduction. Theorem 1.4 is an a
priori estimate over the real numbers. The proof of this latter estimate is the heart of
the matter of this paper. It is closely related to the study of cancellation estimates for
the simplex Hilbert transform [7] and the singular Brascamp–Lieb estimates [16, 8] in
real harmonic analysis, but for more general kernels with multi-parameter features. We
also refer the reader to the survey [10].
Definition 1.3 (Twisted average ∀ , ∀ ). Let n ∈ N. For an n-tuple of real-valued
functions f = (fi )i∈[n) on Rn , a function χ : R → R and x ∈ Rn denote
                                       Z      Y                
                         A(χ, f )(x) =    χ(s)     fi (x + sei ) ds,        (1.3)
                                               R         i∈[n)

whenever the integrand is measurable and integrable. Also set At (χ, f ) = A(χ(t) , f ),
where χ(t) (x) = t−1 χ(t−1 x) for t > 0.
Theorem 1.4 (Main twisted theorem ∀ ). Let n ≥ 2 be an integer. For every J ∈ N,
positive real numbers t0 < t1 < · · · < tJ , and every n-tuple of real-valued Schwartz
functions f = (fi )i∈[n) satisfying
                                            ∥fi ∥2min(n,i+2) = 1                                               (1.4)
for i ∈ [n), we have
                                                                                         −n+2
                 X
                        ∥Atj+1 (1[0,1] , f ) − Atj (1[0,1] , f )∥2L2 (Rn ) ≤ C1.4 J 1−2         ,              (1.5)
                j∈[J)

where C1.4 = 2666 .
1.1. Use of automation. A first draft of this blueprint was entirely human-written.
In particular, all mathematical decisions about the statements, the organization of the
proof, and the dependencies are entirely human.
  At the final editing stage when all the statements and definitions, and most of the
proofs were in place, parts of the blueprint, and eventually the entire blueprint, were
given to GPT-5.6-Sol-Pro with detailed instructions. Over several automation passes
with human feedback, the present manuscript was produced. A major goal of the
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                             3

automation was to compute and optimize the explicit constants and minimize the pos-
sibility of mistakes and small inaccuracies in the arguments. Another goal was to fill in
routine arguments, or arguments by analogy that were initially left out.
   Consider for example Gaussian domination, Proposition 3.31, which features several
slightly different cases. The proofs of the different cases differ largely only in a routine
way (up to switching the function in which mean zero is exploited to obtain decay).
Once the statements and the division into cases had been fixed by the authors, there
was little value in typing out every local calculation by hand.

  For transparency, every machine-generated piece of content is tagged with () through-
out the manuscript. Everything not tagged with () is entirely human-generated, up
to possible automatic fixing of typos and minor inaccuracies, tweaking of constants and
other minor automated changes.

   Separate automation passes checked all arguments for local correctness. Neverthe-
less, the formalization still surfaced some minor discrepancies in the values of explicit
constants in statements of some intermediate propositions, which have then been fixed.
Automatically generated informal proofs () have undergone machine checks, but have
not been thoroughly hand-checked . Thus it is possible they contain harmless inaccu-
racies. This is acceptable since all proofs have been successfully formalized in Lean.
1.2. Formalization in Lean. After this blueprint was completed, its contents were
formally verified using the proof assistant Lean 4 [19] and its mathematical library
mathlib [18]. The formalization is available on GitHub at
                           https://github.com/roos-j/lean-nct
The main statements and definitions in this introduction are annotated with links to
the respective Lean statements (∀). The formalization made heavy use of emerging
autoformalization capabilities of current frontier models. The bulk of the work was
completed using OpenAI’s Codex framework with the model 5.6-terra-ultra, with
some subsequent cleanup done by Anthropic’s Claude Code framework with the model
opus-5-high. While the statements of Theorem 1.2 and Theorem 1.4 and its associ-
ated definitions have been carefully formalized by hand, virtually all of the remaining
formalization was machine-generated across many extended sessions during a one-week
period, with a custom instruction set and human supervision. The timeline and re-
quired amount of human effort are in striking contrast to those of previous large for-
malization projects in analysis such as the Carleson project [4], [5], which was predom-
inantly human-generated and concluded its main goals before the current set of highly
formalization-capable models was made publicly available. Both the instruction set and
the structure of the blueprint were designed with autoformalization in mind and to mit-
igate some of the problems with current Codex models during long formalization tasks,
such as drifting away from target, avoiding the actual task in favor of creating more and
more trivial wrappers, and creating an opaque zoo of auxiliary statements and files.
1.3. Blueprint choices. Several convention choices were crucial in guiding both the
structure and the content of this blueprint.
4                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

     • Strict forward reasoning. After the introduction, all theorems and definitions
       must exclusively use theorems that were either previously stated and proved, or
       are standard theorems. The proof of a theorem must directly follow the corre-
       sponding statement (with the exception of the theorems in the introduction).
       This naturally aligns the blueprint with the structure of the formalization.
     • Mathlib awareness. Generally, only facts that are currently available in mathlib
       in some shape or form can pass as ‘standard theorems’ that require no proof.
       We make two exceptions to this rule: an instance of the Calderón transfer-
       ence principle (Theorem 5.5), and a multilinear complex interpolation theorem
       (Theorem 5.2). These were essentially already formalized prior to this formal-
       ization project: the Calderón transference principle was first hand-formalized by
       Pernegger [20]; complex interpolation was autoformalized by one of the authors.
     • Explicit dependencies. Whenever a named theorem is used in a proof it must
       be referred to explicitly. The parameters of the theorem should also usually be
       made explicit, unless it is clear from context (including proofs of hypotheses).
       This allows for reliable automatic generation of dependency graph metadata.
     • Treatment of constants. Every claimed inequality must come with an explicitly
       defined constant, rather than a constant introduced by an existential quantifier.
       Every constant must be named after the corresponding statement, e.g. C3.29
       for the constant of Proposition 3.29. All dependencies on parameters must be
       explicitly specified and all constants must be recursively defined in terms of pre-
       viously introduced constants. Most statements with such constants also have
       a separate lemma following it that unravels the recursion and provides an ex-
       plicit estimate not depending on any other constants. The latter are exclusively
       automatically generated.
  In this blueprint we also make use of a somewhat unconventional test function space,
the Wiener space W0 (see §2.2). This space enjoys convenient invariance properties with
respect to the fiberwise constructions common in this project (see e.g. Proposition 2.8),
and contains certain bump functions lacking rapid decay that play an important role in
the argument (see Proposition 2.53).
Acknowledgments. FvD and CT were supported by ERC Synergy Grant 101224275
and Germany’s Excellence Strategy grant EXC-2047/1 - 390685813. PD, JR, and LS
acknowledge support by the ERC Synergy Grant 101224275 during research stays at
Bonn. PD was supported in part by NSF grant DMS-2554859 and a grant from the
Simons Foundation. JR was supported in part by NSF grant DMS-2154835 and a grant
from the Simons Foundation. LS was partially supported by the grant no. 26-21107S of
the Czech Science Foundation.

                                   2. Preliminaries
2.1. Notation. We use indexing starting at zero rather than starting at one. For
example, if x is a vector in Rn we write x = (x0 , . . . , xn−1 ). By N we always denote the
natural numbers including zero. For n ∈ N recall that
                                   [n) = {0, . . . , n − 1}.                           (2.1)
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                 5

For a vector x ∈ Rn we denote by |x| its standard Euclidean norm. For a multiindex
m ∈ Nn we denote                          X
                                  |m| =      mi .                             (2.2)
                                                 i∈[n)
  For a subset I ⊂ [n) (which inherits the natural order on [n)) and x ∈ Rn we use the
notation
                                  xI = (xi )i∈I ∈ R|I|                              (2.3)
and when I ⊂ [n) and i ∈ [n) we also write I \ i for the set I without the index i.
  For x ∈ Rn let                             X
                                    Σ(x) =       xi .                               (2.4)
                                                  i∈[n)
               2 n
  For y ∈ (R )       we write y = (yim )i∈[n),m∈[2) , y m = (yim )i∈[n) and similarly if h ∈ [2)n ,
then write
                                        y h = (yihi )i∈[n) .                                 (2.5)
                                           h  m
Note there is no ambiguity in having y , y mean different things, because the variables
m, h have different types.
   For i ∈ [n) we denote by ei the ith standard unit vector in Rn , i.e. the vector with
(ei )i′ = 1 if i = i′ and = 0 otherwise. Similarly, for i ∈ [n), j ∈ [2) denote by eji ∈ (R2 )n
                                      ′
the standard unit vector with (eji )ji′ = 1 if i = i′ , j = j ′ and = 0 otherwise.
   The Fourier transform of an L1 function on Rn will be defined by
                                               Z
                             Ff (ξ) = f (ξ) =
                                        b            f (x)e−2πix·ξ dx.                       (2.6)
                                                 R n

Here x · ξ = i∈[n) xi ξi denotes the standard inner product on Rn . We have the usual
                 P

properties of the Fourier transform. For example, f[         ∗ g = fb · gb. The Fourier transform
extends to an isometry on L : we have ∥f ∥2 = ∥f ∥2 for f ∈ L2 . The inverse Fourier
                                2              b
transform of an L1 function on Rn is defined by
                                                  Z
                               −1
                             F g(x) = gq(x) =           g(ξ)e2πix·ξ dξ.                      (2.7)
                                                    Rn
           n                m
  If ϕ : R → C, ψ : R           → C are functions, then ϕ ⊗ ψ : Rn+m → C denotes their
tensor product
                             (ϕ ⊗ ψ)(x, y) = ϕ(x)ψ(y),                                       (2.8)
where we have identified Rn+m with Rn × Rm . For d ∈ N also define
                                       χ⊗d = χ ⊗ · · · ⊗ χ .                                 (2.9)
                                             |   {z      }
                                                  d times

  () For r, R > 0 we use the notation
                           Ann1 (r, R) = {ξ ∈ R : R−1 r ≤ |ξ| ≤ Rr}.                        (2.10)
Definition 2.1. For n ∈ N and r > 0 and x ∈ Rn denote
                                Bn (x, r) = {ξ ∈ Rn : |ξ − x| ≤ r}                          (2.11)
                                        Bn (r) = Bn (0, r)                                  (2.12)
6                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Definition 2.2. The standard Gaussian on R is defined by
                                                       2
                                         g(x) = e−πx                              (2.13)
                                    R
for x ∈ R. This is chosen so that    R
                                         g = 1.
    For t > 0 and a function ψ on Rn define the rescaled function
                                 ψ(t) (x) = t−n ψ(t−1 x).                         (2.14)
                      R          R
This is chosen so that Rn ψ(t) = Rn ψ.
   Denote by S(Rn ) the space of Schwartz functions on Rn and by S ′ (Rn ) the space of
tempered distributions. The Fourier transform of a distribution T ∈ S ′ (Rn ) is defined
as
                          F(T )(ϕ) = T (Fϕ) for ϕ ∈ S(Rn ).                       (2.15)
   Unless otherwise specified, all functions can be assumed real-valued. We shall use
freely the fact that if a function, or distribution f on Rn is real-valued and even, then
Ff is also real-valued.
Definition 2.3 (bracket bump). Define
                                     ⟨x⟩ = (1 + |x|)−1 .                          (2.16)
We agree on the following parsing, which interprets the power first:
                        ⟨x⟩N         N            −1      −1
                           (s) = (⟨.⟩ )(s) (x) = s (1 + |s x|)
                                                              −N
                                                                 .                (2.17)
2.2. The Wiener space W0 . Let K be R or C. Functions in this section are K-valued.
  The Wiener space W is a space which locally behaves like L∞ and globally like L1
[23, 11]. In this paper we will only use the space W0 , which is the closed subspace of
continuous functions in W . The exact definition follows below.
Proposition 2.4. Let d ∈ N and f : Rd → K be continuous. Then for r ∈ (0, ∞), the
function g : Rd → [0, ∞] defined by
                                    g(x) = sup |f (y)|                            (2.18)
                                             |x−y|≤r

is finite and upper semi continuous and measurable.
Proof. Pick x ∈ Rd . Let r > 0. The function f is continuous on the compact ball
Bd (x, 2r) (Definition 2.1) and thus bounded and uniformly continuous on that ball. It
follows that g is finite. By uniform continuity, for every λ > g(x) there is an ϵ such
that for y ∈ Bd (x, r) and z ∈ Bd (x, 2r) with |y − z| ≤ ϵ we have |f (z)| < λ. For
z ∈ Bd (x, r + ϵ) there is y ∈ Bd (x, r) on the same ray emanating from x as z such that
|y − z| ≤ ϵ. Hence
                                       sup |f (y)| ≤ λ .                          (2.19)
                                    |y−x|≤r+ϵ

Hence, for every y ∈ Bd (x, ϵ), we have g(y) ≤ λ. Upper semicontinuity of g follows and
then also measurability.                                                              □
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                              7

Definition 2.5. Let d ∈ N. By Proposition 2.4, the integrand in the following definition
is finite and measurable. Define
                                          Z
                            ∥f ∥W0 ,d,r =   sup |f (y)| dx.                       (2.20)
                                               Rd |x−y|≤r

As d can be inferred from the type of f , we will omit it from the notation. We also set
                                     ∥f ∥W0 = ∥f ∥W0 ,1 .                             (2.21)
Write W0 (Rd ) or W0 (d) for the set of continuous functions f : Rd → K so that
                                        ∥f ∥W0 < ∞ .                                  (2.22)
We also say that f is in W0 as again the type of f determines d.
Proposition 2.6. Let d ∈ N. Let 0 < r, s < ∞ and set
                               C2.6,d,r,s = max(1, (3s/r)d ) .                        (2.23)
  Then for all continuous f : Rd → K we have
                                ∥f ∥W0 ,s ≤ C2.6,d,r,s ∥f ∥W0 ,r .                    (2.24)
In particular, for every 0 < r < ∞, a continuous f : Rd → K is in W0 if and only if
∥f ∥W0 ,r < ∞.
Proof. By Proposition 2.4, all local suprema integrated below are measurable. If 0 <
s ≤ r < ∞, the statement (2.24) follows with factor 1 by nesting of the suprema. Now
assume 0 < r < s < ∞. Let X be a set of points in Bd (s) of mutual distance at least
r. As the open balls of radius r/2 about these points are disjoint and contained in
Bd (3s/2), volume comparison shows there are at most (3s/r)d many points in X. We
may therefore pick a maximal set X of such points. The closed balls of radius r about
these points cover Bd (s), because any uncovered point would contradict maximality of
X.
  By translation, for every x ∈ Rd , the closed ball Bd (x, s) is covered by the closed balls
Bd (x + z, r) with z ∈ X. It follows that
                                    Z                         !
                        ∥f ∥W0 ,s ≤    sup      sup |f (y)| dx .
                                      Rd z∈X     |x+z−y|≤r

Estimating the supremum in X by the sum in X and pulling the sum out of the integral,
we estimate the last display using translation invariance of the integral by
        XZ                           XZ
                   sup |f (y)| dx ≤           sup |f (y)| dx ≤ (3s/r)d ∥f ∥W0 ,r .
         z∈X   Rd |x+z−y|≤r             z∈X    Rd |x−y|≤r

This completes the proof of (2.24).
  The characterization of W0 (X) by arbitrary r follows.
                                                                                           □
8                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proposition 2.7. Let d ∈ N be given and set
                                C2.7,d = π d/2 Γ(d/2 + 1)−1 .                        (2.25)
If f ∈ W0 (d) and 1 ≤ p ≤ ∞, then
                                            1
                                              −1
                                            p
                                   ∥f ∥p ≤ C2.7,d ∥f ∥W0 .                           (2.26)
Proof. Let f ∈ W0 (d). As |f (x)| ≤ sup|x−y|≤1 |f (y)| for every x ∈ Rd , integration yields
                                         ∥f ∥1 ≤ ∥f ∥W0 .                            (2.27)
Moreover, for every λ < ∥f ∥∞ there is a point x with |f (x)| ≥ λ. For every y in Bd (x, 1)
(Definition 2.1), we have
                                    sup |f (z)| ≥ λ .
                                        |z−y|≤1

With C2.7,d the volume of Bd (x, 1), we obtain by integration
                                        λC2.7,d ≤ ∥f ∥W0 .                           (2.28)
Taking supremum over all λ < ∥f ∥∞ gives
                                           −1
                                  ∥f ∥∞ ≤ C2.7,d ∥f ∥W0 .                            (2.29)
Inequality (2.26) follows by logarithmic convexity of the Lp norms.                       □
Proposition 2.8. For every injective linear map π : Rm × Rl → Rn with m, l ∈ N,
1 ≤ m + l ≤ n there are 0 < C2.8,π,1 , C2.8,π,2 < ∞ such that the following holds. For
every f ∈ W0 (n) and u ∈ Rm , the function hu defined by
                                    hu (v) = f (π(u, v))                             (2.30)
is in W0 (l) with
                            ∥hu ∥W0 ≤ C2.8,π,1 ∥f ∥W0 .                              (2.31)
                    m
The function g : R → C defined by
                             Z                    Z
                     g(u) =     f (π(u, v)) dv =     hu (v) dv                       (2.32)
                                   Rl                        Rl
is in W0 (m) with
                                 ∥g∥W0 ≤ C2.8,π,2 ∥f ∥W0 .                           (2.33)
  Note that l, m, n are determined through the type of π, thus the two constants in the
theorem may in particular depend on l, m, n.
Proof (). By Proposition 2.4, the local suprema of the continuous functions occurring
below are measurable. Choose a linear map τ : Rn−m−l → Rn such that
                                 (u, v, z) 7−→ π(u, v) + τ z
is an isomorphism from Rm × Rl × Rn−m−l onto Rn . Let D > 0 be the absolute value
of its determinant and set           √
                                 R = 2∥π∥ + ∥τ ∥.
We use the convention that the volume of the unit ball in R0 is 1.
                        NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                     9

  Fix u ∈ Rm . If |v − v ′ | ≤ 1, |u − u′ | ≤ 1, and |z| ≤ 1, then
                                      |π(u, v ′ ) − (π(u′ , v) + τ z)| ≤ R.
Averaging first over the unit balls in the u′ and z variables, integrating in v, and applying
the change of variables above therefore gives
                                                        −1
                             ∥hu ∥W0 ,l,1 ≤ D−1 C2.7,m
                                                 −1
                                                       C2.7,n−m−l ∥f ∥W0 ,n,R .
Proposition 2.6 gives (2.31) with
                                                       −1
                                C2.8,π,1 = D−1 C2.7,m
                                                −1
                                                      C2.7,n−m−l C2.6,n,1,R .
   The same estimate, before integration in u′ , supplies an integrable majorant when
u′ ranges in a neighborhood of u. Dominated convergence therefore shows that g is
continuous. Moreover,
                   Z
                                                  −1
                        sup |g(u′ )| du ≤ D−1 C2.7,n−m−l  ∥f ∥W0 ,n,R .
                            Rm |u−u′ |≤1

A second application of Proposition 2.6 proves (2.33) with
                                                      −1
                                      C2.8,π,2 = D−1 C2.7,n−m−l C2.6,n,1,R .
                                                                                                                       □
Proposition 2.9. Let J ∈ N S  with J ≥ 1. For j ∈ [J), let Ij ⊂ N and assume the Ij
are pairwise disjoint. Set I = j∈[J) Ij . Let fj : R|Ij | → K in W0 (|Ij |) and define
                                            Y
                                f (xI ) =       fj (xIj ) .                            (2.34)
                                                              j∈[J)

Then f ∈ W0 (|I|) and
                                                               Y
                                               ∥f ∥W0 ≤               ∥fj ∥W0 .                                    (2.35)
                                                              j∈[J)

Proof. Define gj (xI ) = fj (xIj ). Then gj is continuous as composition of the continuous
projection xI → xIj and the continuous map fj . The function f as product of continuous
functions is also continuous. We have
                                         sup |xIj − yIj | ≤ |xI − yI | ,                                           (2.36)
                                         j∈[J)

and hence
                                     Y                                      Y
            sup        |f (yI )| ≤              sup        |fj (yIj )| ≤               sup         |fj (yIj )| .   (2.37)
         |xI −yI |≤1                         |xI −yI |≤1                           |xIj −yIj |≤1
                                     j∈[J)                                 j∈[J)

By Proposition 2.4, each factor on the right is measurable. It follows by Tonelli that
             Z                           YZ
                     sup |f (yI )|dxI ≤              sup |fj (yIj )|dxIj ,        (2.38)
                   R|I| |xI −yI |≤1                         j∈[J)     R|Ij | |xIj −yIj |≤1

where each factor is finite by assumption and we have f ∈ W0 and (2.35).                                               □
10                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proposition 2.10. Let m, l ∈ N, m + l ≤ n and assume l ̸= 0. Let J ∈ N with J ≥ 1.
For j ∈ [J), let lj ∈ N and let Πj : Rm × Rl → Rlj be a linear map such that
                                     \
                                        kerΠj = {0} .                        (2.39)
                                             j∈[J)

Then there is C > 0 such that the following holds. For j ∈ [J), let fj ∈ W0 (Rlj ). Then
for each u ∈ Rm , the function
                                      Y
                                v→        fj (Πj (u, v))                           (2.40)
                                                  j∈[J)

is in W0 (Rl ) and with f defined by
                                              Z        Y
                                 f (u) =                   fj (Πj (u, v)) dv ,     (2.41)
                                               Rl j∈[J)

we have f ∈ W0 (Rm ) and
                                                           Y
                                     ∥f ∥W0 ≤ C                    ∥fj ∥W0 .       (2.42)
                                                           j∈[J)

     Note that m = 0 is a case in the above proposition.
Proof. Let
                                                X          X
                                          Ij = [  lh ) \ [   lh )                  (2.43)
                                                   h≤j             h<j
                                         m         l        |I|
            P
and I = [       h<J lh ). Define Π : R       ×R →R                by
                                     (Π(u, v))Ij = (Πj (u, v)) .                  (2.44)
Then Π is injective by (2.39).
  Define g : R|I| → C by
                                                          Y
                                          g(xI ) =               fj (xIj ) .      (2.45)
                                                         j∈[J)
                                   |I|
By Proposition 2.9, g ∈ W0 (R ) with
                                                          Y
                                         ∥g∥W0 ≤                 ∥fj ∥W0 .        (2.46)
                                                         j∈[J)

By Proposition 2.8, f ∈ W0 with
                                         ∥f ∥W0 ≤ C2.8,Π,2 ∥g∥W0 .                (2.47)
     This proves Proposition 2.10 with
                                                  C = C2.8,Π,2 .
                                                                                       □
Proposition 2.11. We have S(Rn ) ⊂ W0 (Rn ).
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                               11

Proof (). Let f ∈ S(Rn ). Choose N > n. There is a finite constant C such that
                                        |f (y)| ≤ C(1 + |y|)−N
for every y ∈ Rn . If |x − y| ≤ 1, then 1 + |x| ≤ 2(1 + |y|), and hence
                                       |f (y)| ≤ 2N C(1 + |x|)−N .
Proposition 2.4 shows that the local supremum is measurable. The right-hand side is
integrable in x, so f ∈ W0 (Rn ).                                                □
2.2.1. Convolution along a vector.
Definition 2.12 (Convolution along a vector). For ρ ∈ W0 (Rn ), φ ∈ W0 (R) and a
vector α ∈ Rn define for x ∈ Rn ,
                                        Z
                          (ρ ∗α φ)(x) =   ρ(x − pα)φ(p) dp                 (2.48)
                                                     R

Proposition 2.13 (Properties of convolution along a vector). For ρ ∈ W0 (Rn ), φ ∈
W0 (R), α, ξ ∈ Rn we have ρ ∗α φ ∈ W0 (Rn ) and
                                        ∗α φ(ξ) = ρb(ξ)φ(α
                                       ρ\              b · ξ).                           (2.49)
Proof. Apply Proposition 2.10. The left-hand side equals
            Z                            Z Z
                            −2πix·ξ
               (ρ ∗α φ)(x)e         dx =      ρ(x − pα)φ(p) dp e−2πix·ξ dx
               Rn                                    Rn   R
                                   Z    Z
                               =             ρ(x)φ(p)e−2πi(x+pα)·ξ dp dx,
                                   Rn    R
which equals the right-hand side.                                                            □
2.3. K kernels.
Definition 2.14 (normalized function tuples). Let F be the set of tuples F = (Fi )i∈[n)
of real-valued functions in S(Rn )
   satisfying for i ∈ [n) the normalization
                                            ∥Fi ∥2i+min(n−i,2) = 1.                      (2.50)
In other words,
                        ∥Fi ∥2i+2 = 1 if i ≤ n − 2 and ∥Fn−1 ∥2n = 1 .                   (2.51)
  The word cube in the following definition stands for the parameter set [2)k , which
can be interpreted as a k dimensional cube.
Definition 2.15 (cube Brascamp–Lieb form). Define for k ∈ N with 1 ≤ k ≤ n and
L ∈ W0 (Rk ) and F ∈ W0 (Rn )
                    Z  Z                    Y                   2min(n−k,1)
 Θcube (k, L)(F ) =           L(y 1 − y 0 )    F (y h , x[k,n) )              dx[k,n) dy. (2.52)
                      (R2 )k   Rn−k
                                                      h∈[2)k

  Note that the integrand in Θcube (k, L)(F ) is in W0 by Proposition 2.10.
12                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proposition 2.16 (cube BL inequality). Let k ∈ N satisfy 1 ≤ k ≤ n. Let L ∈ W0 (Rk ).
Then, for all F ∈ W0 (Rn ) with ∥F ∥2k+min(n−k,1) = 1,
                                          |Θcube (k, L)(F )| ≤ ∥L∥1 .                                     (2.53)
Proof. This follows from Hölder’s inequality. Changing variables y 1 7→ y 0 + u we have
yih = yi0 + hi ui , so
                      Z     Z Z       Y                                     2min(n−k,1)             
Θcube (k, L)(F ) =      L(u)                  F ((yi0 +hi ui )i∈[k) , x[k,n) )             dx[k,n) dy 0 du
                         Rk          Rk      Rn−k
                                                    h∈[2)k

By the triangle inequality, |Θcube (k, L)(F )| is no greater than ∥L∥1 times the supremum
over u ∈ Rk of             Z  Y                    2min(n−k,1)
                                        |F (πh (x))|             dx,
                                   Rn
                                          h∈[2)k

where we have renamed y 0 to x[0,k−1] and set πh (x) = (xi + hi ui )i∈[k) , x[k,n) . By Hölder’s
inequality this is
                          Y                             2min(n−k,1)
                     ≤            ∥F ◦ πh ∥2k+min(n−k,1)              ,
                                    h∈[2)k

which is equal to 1 because each πh is an isometry and ∥F ∥2k+min(n−k,1) = 1.                                  □
  The word prism in what follows stands for the Cartesian product of a cube with a
simplex. The 2k corners of the k dimensional cubes are parameterized by [2)k , while the
n − k + 1 corners of the simplex are parameterized by integers in the interval [k − 1, n).
Note that the simplex with two corners is an interval, hence both cases k = n − 1 and
k = n can be identified with a cube.
Definition 2.17 (prism Brascamp–Lieb form). Define for integers 1 ≤ k ≤ n and
K ∈ W0 (Rk+1 ) and F ∈ F,
               Z         Z                                                Y
Θk (K)(F) =                        K(y 1 −y 0 , Σ(y 0 )+Σ(x[k−1,n) ))               Fi (y h , x[k−1,n)\i ) dx[k−1,n) dy
                (R2 )k    Rn−k+1
                                                                         h∈[2)k ,
                                                                        i∈[k−1,n)
                                                                                                          (2.54)
  Note that the integrand in Θk (K)(F) is in W0 by Proposition 2.10. The argument of
K in this definition is split as Rk × R while the argument of Fi−1 is split as Rk × Rn−k .
Recall that superscripts 0 and 1 as in y 0 and y 1 are not powers but just superscripts.
Proposition 2.18 (prism BL inequality). Let k ∈ N satisfy 1 ≤ k ≤ n and K ∈
W0 (Rk+1 ) and F ∈ F. Then
                            |Θk (K)(F)| ≤ ∥K∥1 .                       (2.55)
Proof. This follows from Hölder’s inequality. Changing variables (y 1 , xk−1 ) 7→ (u, s),
where
                    y 1 = y 0 + u,    xk−1 = s − Σ(y 0 ) − Σ(x[k,n) ),
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                    13

we have yih = yi0 + hi ui and Σ(y 0 ) + Σ(x[k−1,n) ) = s. For fixed (u, s), rename (y 0 , x[k,n) )
as x ∈ Rn and set
                                                                          
                  πh,i (x) = (xl + hl ul )l∈[k) , s − Σ(x), x[k,n) [k−1,n)\i .
Then                               Z                     Z          Y
                Θk (K)(F) =                    K(u, s)                        Fi (πh,i (x)) dx du ds.
                                      Rk+1                   Rn
                                                                    h∈[2)k
                                                                  i∈[k−1,n)

By the triangle inequality, |Θk (K)(F)| is no greater than ∥K∥1 times the supremum
over (u, s) ∈ Rk+1 of         Z     Y
                                          |Fi (πh,i (x))| dx.
                                          Rn
                                                   h∈[2)k
                                                 i∈[k−1,n)

By Hölder’s inequality this is no greater than
                                 Y
                                       ∥Fi ◦ πh,i ∥2i+min(n−i,2) .
                                         h∈[2)k
                                       i∈[k−1,n)

Each πh,i is invertible and measure preserving, so this is equal to one by the definition
of F.                                                                                   □
  The following proposition concerns the special case k = n.
Proposition 2.19 (simplification 1 prism). Let K ∈ W0 (Rn+1 ). If for all z ∈ Rn+1 we
have                           Z
                                                   K(z + qen ) dq = 0 ,                                        (2.56)
                                               R
then for all F ∈ F,
                                                   Θn (K)(F) = 0 .                                             (2.57)
Proof. The form is
                           Z          Z                                           Y
           Θn (K)(F) =                      K(y 1 − y 0 , Σ(y 0 ) + xn )                 Fn−1 (y h ) dxn dy.
                             (R2 )n     R                                       h∈[2)n

                                             h
                     Q
Since the product        h∈[2)k Fn−1 (y
                                      ) does not depend on xn , this is equal to
                       Z           Y           Z                              
                                             h          1   0       0
       Θn (K)(F) =                    Fn−1 (y )     K(y − y , Σ(y ) + xn ) dxn dy.
                         (R2 )n    h∈[2)n                          R


Setting z = (y 1 − y 0 , Σ(y 0 )) ∈ Rn+1 for every fixed y ∈ (R2 )n , we see that the inner
integral over xn is equal to zero by the assumption (2.56).                              □
   In the next proposition we apply the Cauchy-Schwarz inequality as in the proof of
Proposition 2.18, but this time carefully preserving in one of the terms on the right-hand
side a cancellation if the function ϕj has integral zero.
14                      VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proposition 2.20 (singly cancellative Cauchy-Schwarz). Let J ≥ 1 and 1 ≤ k < n be
integers. For (ρj )j∈[J) ⊂ W0 (Rk+1 ), and (ϕj )j∈[J) ⊂ W0 (R), define, for u ∈ Rk+1 ,
                                  XZ
                          K(u) =          ρj (u[k) , uk − q)ϕj (q) dq .                (2.58)
                                                j∈[J)     R

     Then K ∈ W0 (Rk+1 ) by Proposition 2.10. For u ∈ Rk+2 , define
                           XZ
                  K̃(u) =        |ρj |(u[k) , uk+1 − q)ϕj (uk + q)ϕj (q) dq .                          (2.59)
                                    j∈[J)      R

Then K̃ ∈ W0 (Rk+2 ). Moreover, for all F ∈ F,
                                                                             X
                                   |Θk (K)(F)|2 ≤ Θk+1 (K̃)(F)                       ∥ρj ∥1 .          (2.60)
                                                                             j∈[J)

Proof. We compute, substituting xk−1 by xk−1 +q and then q by r −xk−1 in combination
with suitable orders of integration in dxk−1 and dq, Θk (K)(F) equals
                           XZ        Z
            Θk (K)(F) =                      ρj (y 1 − y 0 , Σ(y 0 ) + Σ(x[k−1,n) )) (2.61)
                                     j∈[J)     (R2 )k    Rn−k+1
                               Z  Y                                                          
                           ×                          Fi (y h , r, x[k,n)\i ) ϕj (r − xk−1 ) dr
                                    R
                                            h∈[2)k
                                            i∈[k,n)
                                         Y                             
                                                              h
                                    ×                 Fk−1 (y , x[k,n) ) dx[k−1,n) dy .
                                            h∈[2)k
We estimate ρj by |ρj | and also the term in outmost brackets in (2.61) by its absolute
value A and the last bracket in (2.61) by its absolute value B. We interpret the resulting
expression as a pairing ⟨A, B⟩ with respect to a positive measure. Applying Cauchy-
Schwarz, we estimate the modulus squared of (2.61) by the product of two terms. The
first term ⟨A, A⟩ is no greater than
                    XZ        Z
                                      |ρj |(y 1 − y 0 , Σ(y 0 ) + Σ(x[k−1,n) ))
                         j∈[J)     (R2 )k    Rn−k+1
                        Z  Y                                                  2
                                                h
                  ×                      Fi (y , r, x[k,n)\i ) ϕj (r − xk−1 ) dr dx[k−1,n) dy,
                         R
                               h∈[2)k
                               i∈[k,n)
Using that the Fi are real and renaming the integration variables r, which appear twice
through the square, once yk0 and once yk1 ,
            XZ          Z     Z
                                 |ρj |((y 1 − y 0 )[k) , Σ(y[k)
                                                            0
                                                                ) + xk−1 + Σ(x[k,n) ))
                j∈[J)   (R2 )k+1    Rn−k       R
                 Y                              
            ×                Fi (y h , x[k,n)\i ) ϕj (yk1 − xk−1 )ϕj (yk0 − xk−1 ) dxk−1 dx[k,n) dy.
                 h∈[2)k+1
                  i∈[k,n)
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                          15

This is equal to Θk+1 (K̃)(F). In the second identity, we substitute xk−1 by xk−1 + yk0
and then name the variable xk−1 as −q.
  The second term ⟨B, B⟩, in Cauchy-Schwarz, after integrating the variable xk−1 which
only appears in the last argument of ρj , is identified as
                                 X
                                    Θcube (k, Lj )(Fk−1 )                        (2.62)
                                       j∈[J)

with                                                Z
                                       Lj (u) =          |ρj (u, q)| dq              (2.63)
                                                    R
and estimated by Proposition 2.16.                                                       □
   If k = n−1, one may do an even more careful Cauchy-Schwarz, preserving cancellation
in both terms on the right-hand-side.
Proposition 2.21 (doubly cancellative Cauchy-Schwarz, k = n − 1). Let J ≥ 1 be an
integer. For (ρj )j∈[J) ⊂ W0 (Rn ) and (ϕj )j∈[J) ⊂ W0 (R) define for u ∈ Rn ,
                          XZ
                 K(u) =            ρj (u[n−1) , un−1 − r − s)ϕj (r)ϕj (s) dsdr . (2.64)
                          j∈[J)   R2


Then K ∈ W0 (Rn ). For u ∈ Rn+1 let
                       XZ
              K̃(u) =        |ρj |(u[n−1) , un − q)ϕj (un−1 + q)ϕj (q) dq .          (2.65)
                          j∈[J)   R


Then K̃ ∈ W0 (Rn+1 ) and for all F ∈ F,
                             |Θn−1 (K)(F)| ≤ sup |Θn (K̃)(F̃)|.                      (2.66)
                                                         F̃∈F

Proof. We expand Θn−1 (K)(F), replacing xn−2 by xn−2 + r and xn−1 by xn−1 + s and
then r by r − xn−2 and s by s − xn−1 . We obtain that Θn−1 (K)(F) equals
                           XZ          Z
            Θn−1 (K)(F) =                  ρj (y 1 − y 0 , Σ(y 0 ) + Σ(x[n−2,n) )) (2.67)
                              j∈[J)     (R2 )n−1    R2

                          Z  Y                                               
                      ×                        Fn−1 (y h , r) ϕj (r − xn−2 ) dr
                             R    h∈[2)n−1
                    Z  Y                                         
                                                h
                ×                     Fn−2 (y , s) ϕj (s − xn−1 ) ds dx[n−2,n) dy.
                      R   h∈[2)n−1

We estimate ρj by |ρj | and also the two bracketed terms in (2.67) by their absolute
values. We interpret the resulting expression as a pairing with respect to a positive
measure. Applying Cauchy-Schwarz, we estimate the modulus squared of (2.67) by the
product of two terms.
16                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

     The first term is no greater than
                       XZ          Z
                                                    |ρj |(y 1 − y 0 , Σ(y 0 ) + Σ(x[n−2,n) ))
                          j∈[J)     (R2 )n−1   R2

                          Z  Y                                           2
                                                       h
                  ×                          Fn−1 (y , r) ϕj (r − xn−2 ) dr dx[n−2,n) dy.
                           R      h∈[2)n−1

Using that the Fi are real and renaming the integration variables r, which appear twice
                            0                  1
through the square, once yn−1   and once yn−1      , this is equal to
               XZ         Z
                              |ρj |((y 1 − y 0 )[n−1) , Σ(y[n−1)
                                                           0
                                                                 ) + xn−2 + xn−1 )
                  j∈[J)    (R2 )n     R2

                  Y                 
             ×            Fn−1 (y h ) ϕj (yn−1
                                           1                0
                                               − xn−2 )ϕj (yn−1 − xn−2 ) dxn−2 dxn−1 dy.
                 h∈[2)n
                                                      0
In this identity, we substitute xn−2 by xn−2 + yn−1       and then name the variable xn−2 as
−q. This identifies the last display as Θn (K̃)(F).
  The second term is no greater than
                     XZ          Z
                                     |ρj |(y 1 − y 0 , Σ(y 0 ) + Σ(x[n−2,n) ))
                          j∈[J)     (R2 )n−1   R2

                          Z  Y                                           2
                                                       h
                  ×                          Fn−2 (y , s) ϕj (s − xn−1 ) ds dx[n−2,n) dy.
                           R      h∈[2)n−1

Proceeding analogously, using that the Fi are real and renaming the integration variables
                                                        0                1
s, which appear twice through the square, once yn−1          and once yn−1  , this becomes
              X   Z      Z
                             |ρj |((y 1 − y 0 )[n−1) , Σ(y[n−1)
                                                          0
                                                                ) + xn−2 + xn−1 )
                  j∈[J)    (R2 )n     R2

                  Y                 
             ×            Fn−2 (y h ) ϕj (yn−1
                                           1                0
                                               − xn−1 )ϕj (yn−1 − xn−1 ) dxn−2 dxn−1 dy.
                 h∈[2)n
                                                   0
In this identity, we substitute xn−1 by xn−1 + yn−1    and then name the variable xn−1 as
−q. This identifies the last display as Θn (K̃)(F̃), where F̃ arises from F by interchanging
the functions Fn−2 and Fn−1 . Thus
                                  |Θn−1 (K)(F)|2 ≤ Θn (K̃)(F)Θn (K̃)(F̃),                       (2.68)
which implies the claim since F̃ is again in F.                                                     □

  The terms on the right-hand-side of Cauchy-Schwarz are by nature positive. This is
stated independently in the following proposition.
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                 17

Proposition 2.22 (Positivity). Let 1 ≤ k ≤ n − 1. Let ρ ∈ W0 (Rk+1 ) be non-negative
and ϕ ∈ W0 (R). Set for u ∈ Rk+2 and i ∈ [k + 1)
                           Z
                  K(u) =      ρ(u[k+1)\i , uk+1 − q)ϕ(ui + q)ϕ(q) dq .        (2.69)
                                         R
                  k+2
Then K ∈ W0 (R            ) and for all F ∈ F
                                                  Θk+1 (K)(F) ≥ 0 .                                           (2.70)
Proof. We have
                              Z              Z      Z
        Θk+1 (K)(F) =                                     ρ((y 1 − y 0 )[k+1)\i , Σ(y 0 ) + Σ(x[k,n) ) − q)
                               (R2 )k+1      Rn−k     R
                                                          Y
                  × ϕ(yi1 − yi0 + q)ϕ(q)                        Fj (y h , x[k,n)\j ) dq dx[k,n) dy.
                                                     h∈[2)k+1
                                                      j∈[k,n)

  Substituting q by yi0 − q and integrating first in yi0 , yi1 , this is equal to
              Z     Z     Z
                             ρ((y 1 − y 0 )[k+1)\i , Σ(y[k+1)\i
                                                        0
                                                                ) + q + Σ(x[k,n) ))
                 (R2 )k    Rn−k      R
                 Z  Y                                                2
             ×                       Fj (y , x[k,n)\j ) ϕ(yi0 − q) dyi0 dq dx[k,n) dy[k+1)\i ,
                                             h
                  R
                          h∈[2)k+1
                            hi =0
                           j∈[k,n)
which is non-negative.                                                                                            □
Proposition 2.23 (Monotonicity). In the situation of Proposition 2.22, in particular,
if ρ ≤ ρ̃ and             Z
                           Kρ (u) =              ρ(u[k) , uk+1 − q)ϕ(uk + q)ϕ(q) dq                           (2.71)
                                             R
then
                                         Θk+1 (Kρ )(F) ≤ Θk+1 (Kρ̃ )(F)                                       (2.72)
Proof. Apply Proposition 2.22 to Kρ̃−ρ and use linearity.                                                         □
2.4. M kernels.
Proposition 2.24 (M to K). Let k ∈ N satisfy 1 ≤ k ≤ n. Let M ∈ W0 ((R2 )k ).
Define for z ∈ Rk+1 ,
                  Z
     Kk (M )(z) =     M ((zl + pl , pl )l∈[k−1) , zk−1 + zk − Σ(p), zk − Σ(p)) dp. (2.73)
                       Rk−1

The integrand is in W0 (Rk−1 ) for every z ∈ Rk+1 . The argument of M is identified with
an element of (R2 )k . Then Kk (M ) ∈ W0 (Rk+1 ) and
                                                 ∥Kk (M )∥1 ≤ ∥M ∥1 .                                         (2.74)
Proof. The claims on membership in W0 follow from Proposition 2.10. The claimed
inequality follows by the triangle inequality and Fubini-Tonelli’s theorem.  □
18                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Remark 2.1. For example, for k = 1,
                               K1 (M )(z) = M (z0 + z1 , z1 ).                              (2.75)
Remark 2.2. Note that Kk (M ) can also be written as
                             Z
                Kk (M )(z) =     M ((zl + pl , pl )l∈[k) )δ(zk − Σ(p)) dp.                  (2.76)
                                  Rk

Definition 2.25 (prism form). Let 1 ≤ k ≤ n. By Proposition 2.24, Kk (M ) ∈
W0 (Rk+1 ) for every M ∈ W0 ((R2 )k ). We define for such M and F ∈ F,
                              Λk (M )(F) = Θk (Kk (M ))(F).                                 (2.77)
Proposition 2.26 (Positivity). Let 1 ≤ k ≤ n and i ∈ [k). Let M̃ ∈ W0 ((R2 )k−1 ) be
nonnegative and let ϕ ∈ W0 (R) be real valued. Define for y ∈ (R2 )k ,
                                 M (y) = M̃ (y[k)\i )ϕ⊗2 (yi ).                             (2.78)
Then M ∈ W0 ((R2 )k ) and for all F ∈ F,
                                       Λk (M )(F) ≥ 0.                                      (2.79)
Proof. Apply Proposition 2.9 and Proposition 2.22 after a change of variables.                  □
Proposition 2.27 (Cauchy-Schwarz at k). Let k, J ∈ N with 1 ≤ k < n − 1 and J ≥ 1.
For j ∈ [J), let ρj ∈ W0 ((R2 )k ) and let φj ∈ W0 (R) be real valued. Let i ∈ [k). Let
M ∈ W0 ((R2 )k ) and M
                     f ∈ W0 ((R2 )k+1 ) be defined by
                                       X
                                  M=        ρj ∗e0i +e1i φj ,                    (2.80)
                                            j∈[J)

and, for y ∈ (R2 )k+1 ,
                                           X
                              M
                              f(y) =               |ρj (y[k) )|φ⊗2
                                                                j (yk ).                    (2.81)
                                           j∈[J)

Then for all F ∈ F,
                                                              X                 1/2
                                            f)(F)|1/2
                      |Λk (M )(F)| ≤ |Λk+1 (M                           ∥ρj ∥1          .   (2.82)
                                                                j∈[J)

Proof. Without loss of generality we may set i = k − 1 by applying the coordinate
permutation which switches the ith pair with the (k − 1)st pair and preserves the order
inside each pair. Then
                                XZ
                   Kk (M )(z) =        Kk (ρj )(z[k) , zk − q)φj (q) dq.
                                   j∈[J)    R

Apply Proposition 2.20 with Kk (ρj ) in place of ρj , and then Proposition 2.23 with
Kk (|ρj |) in place of |Kk (ρj )|. Proposition 2.24 gives
                                    ∥Kk (ρj )∥1 ≤ ∥ρj ∥1 .
                         NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                         19

The resulting kernel is
                   XZ
                                             Kk (|ρj |)(z[k) , zk+1 − q)φj (zk + q)φj (q) dq,
                             j∈[J)       R


which equals Kk+1 (M
                   f)(z). This proves (2.82).                                                                □
Proposition 2.28 (Cauchy-Schwarz at n − 1). Let J ∈ N with J ≥ 1 and, for j ∈ [J),
let ρj ∈ W0 ((R2 )n−1 ) and φj ∈ W0 (R) be real valued. Let i ∈ [n − 1). Define
                                     X
                               M=        ρj ∗e0i +e1i (φj ∗ φj ),               (2.83)
                                                         j∈[J)

and for y ∈ (R2 )n ,
                                                         X
                                             M̃ (y) =            |ρj (y[n−1) )|φ⊗2
                                                                                j (yn−1 ).               (2.84)
                                                         j∈[J)

Then M ∈ W0 ((R2 )n−1 ) and M̃ ∈ W0 ((R2 )n ) and for all F ∈ F
                                             |Λn−1 (M )(F)| ≤ sup |Λn (M̃ )(F̃)|.                        (2.85)
                                                                      F̃∈F

Proof. Without loss of generality we may set i = n − 2 (replace ρj with ρj ◦ σ where
σ : (R2 )n−1 → (R2 )n−1 is the coordinate permutation switching the ith pair with the
(n − 2)th pair, keeping the order inside the pair unchanged). Recall
                    Z
     Kn−1 (M )(z) =       M ((zl + pl , pl )l∈[n−2) , zn−2 + zn−1 − Σ(p), zn−1 − Σ(p)) dp.
                                 Rn−2
For z ∈ Rn ,
  Kn−1 (M )(z) equals
XZ       Z Z
                ρj ((zl +pl , pl )l∈[n−2) , zn−2 +zn−1 −Σ(p)−q, zn−1 −Σ(p)−q)φj (q−r)φj (r) dr dq dp.
j∈[J)   Rn−2   R   R

  Changing variables q 7→ q + r this is equal to
               XZ
                        Kn−1 (ρj )(z[n−1) , zn−1 − q − r)φj (q)φj (r) d(q, r).
                       j∈[J)      R2

  Applying Proposition 2.21 with Kn−1 (ρj ) in place of ρj gives
                                             |Λn−1 (M )(F)| ≤ sup |Θn (K̃)(F̃)|,
                                                                      F̃∈F
                       n+1
where for u ∈ R              ,
                                 XZ
               K̃(u) =                           |Kn−1 (ρj )|(u[n−1) , un − q)|φj (un−1 + q)φj (q) dq.
                                 j∈[J)       R


By Proposition 2.23 we may replace |Kn−1 (ρj )| by Kn−1 (|ρj |) and then recover Kn (M̃ )(u).
                                                                                          □
20                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

2.5. Multiplicatively spaced monotone sequences.
Definition 2.29 (Multiplicatively spaced monotone sequences). A sequence a : Z → R
with a(j) > 0 for every j ∈ Z is called multiplicatively spaced if, for each j ∈ Z
                                      2a(j) ≤ a(j + 1) .                          (2.86)
Let A be the set of such sequences.
Proposition 2.30 (Extension of sequences). Let J ∈ N with J ≥ 1 and let a : [J) → R
satisfy a(j) > 0 for every j ∈ [J) and, for all j ∈ [J − 1), we have a(j + 1) ≥ 2a(j).
Then there is a unique b ∈ A such that for all j ∈ [J) we have a(j) = b(j) and for j ≥ J
we have b(j) = 2j−J+1 a(J − 1) and for j < 0 we have b(j) = 2j a(0) .
Proof (). Define b : Z → R by
                                b(j) = 2j a(0)      (j < 0),
                                 b(j) = a(j)      (j ∈ [J)),
and
                          b(j) = 2j−J+1 a(J − 1)    (j ≥ J).
Then clearly b(j) = a(j) for every j ∈ [J), while the desired formulas for j < 0 and
j ≥ J hold by definition.
  It remains to check that b ∈ A. Let j ∈ Z. If j < −1, then
                               b(j + 1) = 2j+1 a(0) = 2b(j).
If j = −1, then
                           b(0) = a(0) = 2 · 2−1 a(0) = 2b(−1).
If j ∈ [J − 1), then by assumption
                           b(j + 1) = a(j + 1) ≥ 2a(j) = 2b(j).
If j = J − 1, then
                              b(J) = 2a(J − 1) = 2b(J − 1).
Finally, if j ≥ J, then
                           b(j + 1) = 2j+1−J+1 a(J − 1) = 2b(j).
Thus for every j ∈ Z we have 2b(j) ≤ b(j + 1), so b ∈ A.
  The conditions in the statement prescribe the value of b(j) for every j ∈ Z, since the
three ranges j < 0, j ∈ [J), and j ≥ J cover Z and are disjoint. Hence such a b is
unique.                                                                               □
Proposition 2.31 (Operations on spaced sequences). Let a, b ∈ A. Then the following
hold:
  (i) max(a, b) ∈ A
  (ii) t · a ∈ A for every t > 0.
  (iii) Let n ∈ Z. If c : Z → (0, ∞) is defined by c(j) = a(j + n) for all j ∈ Z, then
c ∈ A.                                       p
  (iv) If c : Z → (0, ∞) is defined by c(j) = a(j)2 + b(j)2 for all j ∈ Z, then c ∈ A.
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                21

Proof (). For (i), let j ∈ Z. If max(a, b)(j) = a(j), then
                   2 max(a, b)(j) = 2a(j) ≤ a(j + 1) ≤ max(a, b)(j + 1).
The case max(a, b)(j) = b(j) is identical.
  For (ii), for every j ∈ Z,
                       2(ta)(j) = t(2a(j)) ≤ ta(j + 1) = (ta)(j + 1).
  For (iii), for every j ∈ Z,
                       2c(j) = 2a(j + n) ≤ a(j + n + 1) = c(j + 1).
  For (iv), for every j ∈ Z,
                   p                   p
          2c(j) = (2a(j))2 + (2b(j))2 ≤ a(j + 1)2 + b(j + 1)2 = c(j + 1).
Thus each sequence belongs to A.                                                               □
Definition 2.32 (Distance of spaced sequences). Given a, b ∈ A, define
                dist(a, b) = min{k ∈ Z≥0 : ∀j, a(j − k) ≤ b(j) ≤ a(j + k)}                 (2.87)
with the understanding that the value is ∞ if there is no such k.
Proposition 2.33 (Properties of distance of sequences). Let a, b, c ∈ A. Then
  (i) If dist(a, b) = 0, then a = b.
  (ii) dist(a, b) = dist(b, a)
  (iii) dist(a, c) ≤ dist(a, b) + dist(b, c)
  (iv) If c(j) = b(j + 1), then dist(a, c) ≤ dist(a, b) + 1.
  (v) For all t > 0, dist(t · a, t · b) = dist(a, b)
  (vi) For all h ∈ Z, dist(a, 2h a) ≤ |h|.
Proof (). For (i), if dist(a, b) = 0, then for every j ∈ Z,
                                      a(j) ≤ b(j) ≤ a(j),
and hence a(j) = b(j).
  For (ii), suppose first that dist(a, b) ≤ k < ∞. Then for every j ∈ Z,
                                 a(j − k) ≤ b(j) ≤ a(j + k).
Applying this with j − k in place of j gives
                                        b(j − k) ≤ a(j),
and applying it with j + k in place of j gives
                                        a(j) ≤ b(j + k).
Therefore
                                    b(j − k) ≤ a(j) ≤ b(j + k)
for every j ∈ Z, so dist(b, a) ≤ k. By symmetry, dist(a, b) = dist(b, a).
   For (iii), if either dist(a, b) or dist(b, c) is infinite, there is nothing to prove. Otherwise
let
                                 dist(a, b) ≤ k,        dist(b, c) ≤ l.
22                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Then for every j ∈ Z,
                               b(j − l) ≤ c(j) ≤ b(j + l).
Using the inequalities for a and b on the two outside terms gives
                   a(j − l − k) ≤ b(j − l) ≤ c(j) ≤ b(j + l) ≤ a(j + l + k).
Hence
                                dist(a, c) ≤ k + l.
Taking the minimum over admissible k and l gives
                               dist(a, c) ≤ dist(a, b) + dist(b, c).
  For (iv), if dist(a, b) is infinite, there is nothing to prove. Otherwise let dist(a, b) ≤ k.
Since c(j) = b(j + 1), for every j ∈ Z,
                             a(j + 1 − k) ≤ c(j) ≤ a(j + 1 + k).
Because a ∈ A is increasing, we have
                                 a(j − k − 1) ≤ a(j + 1 − k)
and
                                 a(j + 1 + k) = a(j + k + 1).
Therefore
                         a(j − (k + 1)) ≤ c(j) ≤ a(j + (k + 1)),
so dist(a, c) ≤ k + 1. Taking the minimum over admissible k gives
                                   dist(a, c) ≤ dist(a, b) + 1.
     For (v), for every k ∈ Z≥0 , the inequalities
                                  a(j − k) ≤ b(j) ≤ a(j + k)
hold for every j ∈ Z if and only if
                                 ta(j − k) ≤ tb(j) ≤ ta(j + k)
hold for every j ∈ Z. Hence
                                  dist(t · a, t · b) = dist(a, b).
     For (vi), first suppose h ≥ 0. Iterating the defining inequality for a ∈ A gives
                                       2h a(j) ≤ a(j + h)
for every j ∈ Z. Also, since a is increasing,
                                  a(j − h) ≤ a(j) ≤ 2h a(j).
Thus
                                a(j − h) ≤ 2h a(j) ≤ a(j + h),
so dist(a, 2h a) ≤ h = |h|.
  If h < 0, write −h > 0. Iterating the defining inequality gives
                                      2−h a(j + h) ≤ a(j),
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                        23

and hence
                                     a(j + h) ≤ 2h a(j).
Also, since a is increasing,
                                 2h a(j) ≤ a(j) ≤ a(j − h).
Therefore
                          a(j − (−h)) ≤ 2h a(j) ≤ a(j + (−h)),
so dist(a, 2h a) ≤ −h = |h|.
                                                                                      □
Definition 2.34 (Closed balls in A). For a ∈ A and r > 0 denote
                           Bdist (a, r) = {b ∈ A : dist(a, b) ≤ r}.               (2.88)
                                               2
2.6. Gaussians. Recall that g(x) = e−πx for x ∈ R.
Proposition 2.35. The function
                                               p
                                     f (x) =    1 − g(x)                          (2.89)
is well-defined using the nonnegative square root and is continuous on R. For |x| ≤ 12 ,
we have
                                      f (x) ≥ 12 |x|                            (2.90)
and for |x| ≥ 12 we have
                                   1 − g(x) ≤ f (x) ≤ 1.                          (2.91)
Proof (). For every x ∈ R we have 0 < g(x) ≤ 1, and hence 1 − g(x) ≥ 0. Thus f is
well defined using the nonnegative square root. Since g is continuous and the square
root is continuous on [0, ∞), the function f is continuous.
  Let |x| ≤ 1/2 and put u = πx2 . Then 0 ≤ u ≤ π/4 < 1. Using e−u ≤ 1 − u + u2 /2,
we get
                                                 2
                                 1 − e−u ≥ u − u2 ≥ u2 .
Therefore
                                              2      2   2
                             f (x)2 = 1 − e−πx ≥ πx2 ≥ x4 ,
and hence f (x) ≥ 21 |x|.
                                                                                √
  Finally, if |x| ≥ 1/2, then 0 ≤ 1 − g(x) ≤ 1. For every a ∈ [0, 1] we have a ≤ a ≤ 1,
so with a = 1 − g(x) this gives
                                   1 − g(x) ≤ f (x) ≤ 1.
                                                                                      □
Proposition 2.36. For every x ∈ R, m, N ∈ N,
                                 |g(m) (x)| ≤ C2.36,m,N ⟨x⟩N ,                    (2.92)
where                                              m/2           N/2
                       C2.36,m,N = 64(m + 1)              4(N + 1)     .          (2.93)
24                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof (). We first prove that, for every m ∈ N and x ∈ R,
                                                 m/2 −πx2 /2
                          |g(m) (x)| ≤ 64(m + 1)     e        .
For m = 0 this is immediate. For m ≥ 1, repeated differentiation gives
                                                             2
                                   g(m) (x) = Pm (x)e−πx ,
where
                                        ⌊m/2⌋
                                        X (−1)m+j 2m−2j πm−j xm−2j
                          Pm (x) = m!                  j!(m−2j)!
                                                                                .
                                         j=0

Indeed, one proves this using induction and Pm+1 (x) = Pm′ (x) − 2πxPm (x). Set d =
m − 2j. We use
                                         2         d/2
                                |x|d e−πx /2 ≤ d+1
                                                πe
with the convention that the right hand side is 1 when d = 0. Also,
                                       
                                       m (2j)!
                               m!
                               j!d!
                                    =          ≤ 2m mj .
                                       d j!
                                                                            2
Hence, using π < 4 and e > 2, each summand in |Pm (x)|e−πx /2 is at most
                                       d/2             m/2
                       m      j 4π(d+1)
                      2 (πm)        e
                                             ≤ 32(m + 1)      .

Since there are at most 2m/2 summands, we get
                                          2                      m/2
                              |Pm (x)|e−πx /2 ≤ 64(m + 1)               .
This proves the displayed Gaussian derivative bound.
  Next, for every N ∈ N,
                               2                        2             N/2
                (1 + |x|)N e−πx /2 ≤ 2N max 1, |x|N e−πx /2 ≤ 4(N + 1)
                                                           
                                                                           .
Equivalently,
                                   2             N/2 N
                               e−πx /2 ≤ 4(N + 1)    ⟨x⟩ .
Therefore
                                                m/2           N/2 N
                      |g(m) (x)| ≤ 64(m + 1)           4(N + 1)    ⟨x⟩ .
This proves the claim.                                                                  □
Proposition 2.37 (Elementary Gaussian properties). (i) g ∈ S(R) ⊂ W0 (R)
  (ii) b
       g = g.
  (iii) We have for λ, µ > 0
                                   g(λ) ∗ g(µ) = g(√λ2 +µ2 ) .                      (2.94)

     (iv) We have for λ > 0
                                        (λ) (ξ) = g(λξ)
                                       gd                                           (2.95)
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                      25

Proof (). By Proposition 2.36, every derivative of g decays faster than any polynomial.
Hence g ∈ S(R), and therefore g ∈ W0 (R).
  We next prove the Fourier transform identity. Set
                                      Z
                                             2
                              I(ξ) =     e−πx e−2πixξ dx.
                                                  R
Differentiation under the integral and integration by parts give
                                 Z
                        I (ξ) = i g′ (x)e−2πixξ dx = −2πξI(ξ).
                         ′
                                            R
The standard Gaussian integral gives I(0) = 1. Hence the unique solution of this
                                    2
differential equation is I(ξ) = e−πξ , and therefore b
                                                     g = g.
   Let λ > 0 and write
                                  g(λ) (x) = λ−1 g(x/λ).
Then, by the change of variables x = λy,
                         Z                        Z
                            −1        −2πixξ
             gd(λ) (ξ) =   λ g(x/λ)e         dx =   g(y)e−2πiy(λξ) dy = g(λξ).
                          R                                  R
This proves (2.95).
  Finally, using (2.95) and b
                            g = g, we have
                                                                   −π(λ +µ )ξ       2   2   2
               g(λ)
                 \  ∗ g(µ) (ξ) = gd
                                  (λ) (ξ)g
                                         d (µ) (ξ) = g(λξ)g(µξ) = e           .
Since
                      e−π(λ +µ )ξ = g( λ2 + µ2 ξ) = g(√
                           2  2 2
                                      p
                                                      \λ2 +µ2 )
                                                                (ξ),
Fourier inversion gives
                                          g(λ) ∗ g(µ) = g(√λ2 +µ2 ) .
                                                                                                    □
Proposition 2.38. Let
                                          p(x) = 2(1 + (2πx)2 )−1 .                             (2.96)
Then
                                                pb(ξ) = e−|ξ| .                                 (2.97)
Proof of Proposition 2.38. For a ∈ R, set
                       Z ∞                                         Z ∞
               I(a) =       e−t cos(at) dt,               J(a) =            e−t sin(at) dt.
                              0                                         0
Integration by parts, differentiating the trigonometric functions and integrating the
exponential function gives
                                  I(a) = 1 − aJ(a),          J(a) = aI(a).
Hence
                                                         1
                                                I(a) = 1+a 2.

Using this for a = 2πx for x ∈ R
                             Z ∞                  Z
                                  −ξ
                    p(x) = 2     e cos(2πxξ) dξ =   e−|ξ| e2πixξ dξ                             (2.98)
                                      0                            R
26                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

The Fourier inversion formula gives (2.97). Namely, it is applicable because both p and
the right hand side of (2.97) are continuous and integrable.
                                                                                      □
Proposition 2.39. With p as in Proposition 2.38, define B : R → R by
                                   p               √
                       B(ξ) = 1 − 1 − g(ξ) − pb( πξ) .                                        (2.99)
                                                                                         ′
Then B is smooth on R \ {0} and continuous on R. The function B has a continuous
extension to R which is integrable and the function B ′′ , extended to be 0 at 0, is Borel
measurable and integrable on R. Moreover,
                       ∥B∥1 ≤ 6,        ∥B ′ ∥1 ≤ 12,           ∥B ′′ ∥1 ≤ 68.               (2.100)
Proof (). Set
                        √                                                 p
                   α=    π,        E(ξ) = e−α|ξ| ,         s(ξ) =          1 − g(ξ).
Then B = 1 − s − E. By Proposition 2.35, the function s is continuous. Hence B is
smooth on R \ {0}, even, and continuous on R, since s(0) = 0 and E(0) = 1.
  We first control the origin. For ξ ≥ 0, put u = αξ. Since
                                              Z 1
                                     −u2              2
                                1−e      =u 2
                                                  e−tu dt,
                                                     0
we can write
                                                         Z 1                1/2
                                                                    −tu2
                      s(ξ) = uR(u),         R(u) =              e          dt     .
                                                            0
For 0 ≤ u ≤ 1, elementary differentiation under the integral sign gives
                     1
                     2
                       ≤ R(u) ≤ 1,         |R′ (u)| ≤ 1,                |R′′ (u)| ≤ 5.
Thus, with
                              F (u) = 1 − uR(u) − e−u ,
we have B(ξ) = F (αξ) for ξ ≥ 0, F (0) = F ′ (0) = 0, and
               |F ′′ (u)| = | − 2R′ (u) − uR′′ (u) − e−u | ≤ 8               (0 ≤ u ≤ 1).
Since α−1 > 1/2, it follows that
                      |B ′′ (ξ)| ≤ 8α2 = 8π < 32           (0 < |ξ| ≤ 1/2),
and B ′ extends continuously to 0 by setting B ′ (0) = 0.
  It remains to estimate the tails. By Proposition 2.35, s(ξ) ≥ 1 − g(ξ) when |ξ| ≥ 1/2.
Since π > 3 and                                  2
                            e3/4 > 1 + 43 + 12 43 = 6532
                                                         > 2,
we have g(ξ) ≤ e−π/4 < 1/2, and hence s(ξ) ≥ 1/2. For ξ > 0,
                                  B ′ (ξ) = − πξg(ξ)
                                               s(ξ)
                                                     + αe−αξ ,
and
                                            2 2           2 2       2
                        B ′′ (ξ) = −πg(ξ)+2π
                                         s(ξ)
                                              ξ g(ξ)
                                                     + π s(ξ)
                                                         ξ g(ξ)
                                                              3 − πe−αξ .
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                            27

By evenness, the same absolute value bounds hold on the negative half-line. Hence, for
|ξ| ≥ 1/2,
                                |B(ξ)| ≤ g(ξ) + E(ξ),
                               |B ′ (ξ)| ≤ 2π|ξ|g(ξ) + αE(ξ),
and
                      |B ′′ (ξ)| ≤ 2πg(ξ) + 12π 2 ξ 2 g(ξ) + πE(ξ).
   We now integrate. On |ξ| ≤ 1/2, the trivial bound |B| ≤ 3 gives contribution at most
3. On the complement,            Z
                                      (g + E) = 1 + α2 ≤ 3.
                                  R
Thus ∥B∥1 ≤ 6.
   For B ′ , the local bound |B ′ (ξ)| < 32|ξ| on |ξ| ≤ 1/2 gives local contribution at most
8. The tail contributes at most
                           Z                  Z
                         2π |ξ|g(ξ) dξ + α E(ξ) dξ = 2 + 2 = 4.
                           R                  R
          ′
Thus ∥B ∥1 ≤ 12.
  Finally, for B ′′ , the local contribution is at most 32. The tail contributes at most
                                                                             √
     Z
         2πg(ξ) + 12π 2 ξ 2 g(ξ) + πE(ξ) dξ = 2π + 12π 2 2π 1
                                                              + π α2 = 8π + 2 π < 36.
                                          
      R
Therefore
                                  ∥B ′′ ∥1 ≤ 32 + 36 = 68.
This proves the claimed integrability and the explicit estimates. The stated Borel
measurability of the extension of B ′′ is immediate from continuity on each half-line and
the definition at the single point 0.                                                   □
Proposition 2.40 (square root of Gaussian decay). For x ∈ R let
                                           p
                      ρ(x) = F −1 (ξ 7→ 1 − 1 − g(ξ))(x).                           (2.101)
This is a well-defined function in W0 (R) satisfying for all x ∈ R,
                                  0 ≤ ρ(x) ≤ C2.40 ⟨x⟩2 ,                           (2.102)
where C2.40 = 17.
Proof (). Set                                 p
                               m(ξ) = 1 −          1 − g(ξ).
We first construct ρ. By Proposition 2.39,
                                                      √
                                 m(ξ) = B(ξ) + e− π|ξ| .
Both terms on the right-hand side are integrable, so m ∈ L1 (R). Define
                                           ρ = m.
                                               q
We will prove that ρ ∈ W0 (R), that it satisfies the claimed decay estimate, and that
ρb = m.
28                      VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE
               √
     Let α =       π and Eα (ξ) = e−α|ξ| . By Proposition 2.38,
                                           Eα (ξ) = pb(αξ).
By the scaling rule for the Fourier transform,
                                                                         √
                             |α (x) = α−1 p(x/α) = 2 2α 2 = 2/ π2 .
                             E                    α +(2πx)  1+4πx

In particular, since π > 3,
                              2 (1 + |x|)2   7 (1 + |x|)2   7 13   3
                             √             <              ≤      <   .
                               π 1 + 4πx2    6 1 + 12x2     6 12   2
Here the middle inequality follows from 12(1 + |x|)2 ≤ 13(1 + 12x2 ). Thus
                                           |α (x) ≤ 3 ⟨x⟩2 .
                                         0≤E                                  (2.103)
                                                    2

     It remains to estimate B.
                            q By Proposition 2.39,
                                    ∥B∥1 ≤ 6,        ∥B ′′ ∥1 ≤ 68.
Therefore
                                 |B(x)|
                                  q     ≤6     (x ∈ R).
For x ̸= 0, integration by parts twice and π > 3 give
                                                     ′′
                                        |B(x)|
                                         q     ≤ ∥B   ∥1
                                                 4π 2 x2
                                                            17
                                                         < 9x 2.


If |x| ≤ 5/9, then 6(1 + |x|)2 ≤ 6(14/9)2 < 15. If |x| > 5/9, then
                                   17
                                  9x2
                                      (1 + |x|)2 < 17
                                                   9
                                                      (14/5)2 < 15.
Thus
                                 |B(x)|
                                  q     ≤ 15⟨x⟩2 .                            (2.104)
Combining these estimates, we obtain
                                     |ρ(x)| ≤ 33
                                              2
                                                 ⟨x⟩2 < 17⟨x⟩2 .
The function ρ is continuous because m ∈ L1 . The preceding decay estimate implies
ρ ∈ W0 (R): indeed, for |x| ≤ 2 the local W0 -supremum is bounded, while for |x| > 2
and |x − y| ≤ 1 we have |y| ≥ |x|/2, so the local supremum is bounded by a constant
multiple of ⟨x⟩2 , which is integrable on R. It remains to prove non-negativity. For
0 ≤ t ≤ 1, the binomial series gives
                                 ∞
                      √
                                                          
                                                      k+1 1/2
                                X
                                        k
                  1− 1−t=           ak t ,   ak = (−1)          > 0.
                                k=1
                                                           k
Moreover ∞
          P
             k=1 ak = 1. Hence, for every ξ ∈ R,
                                        ∞                  ∞
                                        X                  X          √
                               m(ξ) =         ak g(ξ)k =         ak g( kξ).
                                        k=1                k=1

By Proposition 2.37,                       √
                                         g( kξ) = g[√
                                                   ( k) (ξ).
                  NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                           29

The series                              ∞
                                        X
                                              ak g(√k) (x)
                                     k=1
converges in L1 (R), because ∥g(√k) ∥1 = 1 and k ak = 1. Its Fourier transform is m.
                                                P

Since both this series and ρ = m q are in L1 , Fourier inversion and injectivity of the
Fourier transform give
                                         ∞
                                         X
                                ρ(x) =      ak g(√k) (x).
                                             k=1
Every term on the right-hand side is non-negative, so ρ(x) ≥ 0 for every x ∈ R.         □
2.7. Bumps and their estimates.
Lemma 2.41. Let N ≥ 2 be an integer. Let ζ : R → C be an N times continuously
differentiable function with compact support. Then the function ϕ = F −1 ζ belongs to
W0 (R) and we have for all x ∈ R, x ̸= 0, the estimate

                                      b 1 , ∥ϕb(N ) ∥1 (2π)−N |x|−N ).
                        |ϕ(x)| ≤ min(∥ϕ∥                                           (2.105)
Proof. By the assumptions on ζ, we deduce that ζ ∈ L1 (R). Thus, ϕ is a well-defined
continuous function.
  By definition,                     Z
                              ϕ(x) =    ζ(ξ)e2πixξ dξ,                       (2.106)
                                               R
and by the triangle inequality
                           Z                   Z
                                    2πixξ
                 |ϕ(x)| =      ζ(ξ)e      dξ ≤   |ζ(ξ)e2πixξ |dξ ≤ ∥ζ∥1 .          (2.107)
                              R                         R
  For the second estimate we integrate by parts in (2.106) to obtain
                                          Z
                                       −N
                         ϕ(x) = (2πix)      ζ (N ) (ξ)e2πixξ dξ,
                                                   R
and thus by the triangle inequality,
                                                    Z
                                        −N     −N
                        |ϕ(x)| ≤ (2π)        |x|           |ζ (N ) (ξ)e2πixξ |dξ
                                                       R
                                          −N       −N
                               ≤ (2π) |x| ∥ζ (N ) ∥1 .                         (2.108)
Combining (2.107) and (2.108) gives that ϕ ∈ W0 (R). By the Fourier inversion formula,
we then conclude that ζ = ϕ.
                          b                                                         □
Lemma 2.42. Let N ≥ 1 be an integer, then
                                  min(1, |x|−N ) ≤ 2N ⟨x⟩N .                       (2.109)
Proof. We have, using that the mean is less than the maximum
             min(1, |x|−N ) = max(1, |x|)−N ≤ (2−1 (1 + |x|))−N = 2N ⟨x⟩N .
                                                                                        □
30                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

  We will mainly use these lemmas when we have control on the L∞ norm and compact
support of the Fourier transform, so we state this case separately.
Lemma 2.43. Let N ≥ 2 be an integer. Let ζ : R → C be an N times continuously
differentiable function with compact support. Then the function ϕ = F −1 ζ belongs to
W0 (R) and we have for all x ∈ R the estimate
                                       b ∞ , (2π)−N ∥ϕb(N ) ∥∞ )| supp(ϕ)|⟨x⟩
                 |ϕ(x)| ≤ C2.43,N max(∥ϕ∥                              b     N
                                                                                        (2.110)
with C2.43,N = 2N .
Proof. The fact that ϕ ∈ W0 (R) and ϕb = ζ follows from Lemma 2.41. We have for any
compactly supported bounded function f : R → C
                                    ∥f ∥1 ≤ ∥f ∥∞ |supp(f )|.
Using this twice and Lemma 2.41 estimates |ϕ(x)| by
            b 1 , ∥ϕb(N ) ∥1 (2π)−N |x|−N ) ≤ | supp(ϕ)|
     ≤ min(∥ϕ∥                                              b ∞ , ∥ϕb(N ) ∥∞ (2π)−N |x|−N ) .
                                                     b min(∥ϕ∥
The claim now follows from Lemma 2.42.                                                          □
Proposition 2.44 (mean value bump estimate). Let N ∈ N with N ≥ 1 and let
ρ be a W0 (1) function with ρb supported in [−1, 1] and ρb being N times continuously
differentiable.
   Then for all x, y ∈ R
 |ρ(x + y) − ρ(x)| ≤ C2.44,N max ∥(2π)−ν ρb(ν) ∥∞ min(1, 2π|y|)(⟨x + y⟩N + ⟨x⟩N ). (2.111)
                               0≤ν≤N

where
                             C2.44,N = 2N max(2, (1 + (2π)−1 )N ).                      (2.112)
Proof (). For N = 1, Fourier inversion and one integration by parts show directly that
the pointwise estimate in Lemma 2.43, with coefficient 2, remains valid for functions
whose Fourier transform is supported in [−1, 1]. Indeed, if ζ has this support and
                                B = max(∥ζ∥∞ , (2π)−1 ∥ζ ′ ∥∞ ),
then, by Lemma 2.42,
                           |F −1 ζ(x)| ≤ 2B min(1, |x|−1 ) ≤ 4B⟨x⟩.
Thus the pointwise estimate from that lemma may be used below for every N ≥ 1.
  Set
                       δ = 2π|y|,   B = max ∥(2π)−ν ρb(ν) ∥∞ .
                                                0≤ν≤N
If δ > 1, the triangle inequality and the pointwise estimate just discussed give
                        |ρ(x + y) − ρ(x)| ≤ 2N +1 B(⟨x + y⟩N + ⟨x⟩N ),
which is bounded by the right-hand side of (2.111).
  Assume now that δ ≤ 1 and set ρe(x) = ρ(x + y) − ρ(x). Then
                                    ρe(ξ) = ρb(ξ)(e2πiξy − 1)
                                    b
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                       31

and
                                                           N −1      
             (N )                                          X        N (ν)
            ρe
            b              (N )
                    (ξ) = ρb      (ξ)(e   2πiξy
                                                  − 1) +               ρb (ξ)(2πiy)N −ν e2πiξy .
                                                           ν=0
                                                                    ν
                                              N −ν
Since |ξ| ≤ 1 on the support and δ                   ≤ δ for ν < N , these identities give
                                                   ∥b
                                                    ρe∥∞ ≤ Bδ
and
                                              (N )
                        (2π)−N ∥b
                                ρe                   ∥∞ ≤ Bδ(1 + (2π)−1 )N .
The pointwise estimate gives
                                ρ(x)| ≤ 2N +1 Bδ(1 + (2π)−1 )N ⟨x⟩N .
                               |e
Applying the same estimate with −y in place of y, at the point x + y, gives the same
bound with ⟨x + y⟩N in place of ⟨x⟩N . Averaging the two bounds yields
                 |ρ(x + y) − ρ(x)| ≤ 2N Bδ(1 + (2π)−1 )N (⟨x + y⟩N + ⟨x⟩N ),
and (2.111) follows.                                                                                    □
Definition 2.45 (standard bump). Define, for l ∈ N with l ≥ 1,
                                        Y
                       Φl = 1[−3/4,3/4]
                              \           2i+2 1[−2\
                                                   −i−3 ,2−i−3 ] .                                 (2.113)
                                                       i∈[l)

For x ∈ R, define
                                              Φ(x) = lim Φl (x).                                   (2.114)
                                                          l→∞
(The limit exists for every x ∈ R.)
Proposition 2.46 (standard bump). The limit liml→∞ Φl exists in L∞ and L1 sense
and is a Schwartz function Φ whose Fourier transform takes values in [0, 1], is supported
in [−1, 1], and constant 1 on [−1/2, 1/2].
  It satisfies for every m, N ∈ N and every x ∈ R,
                                   (m) )(N ) ∥
                                ∥(Φd           ≤ C̃                               (2.115)
                                                           ∞        2.46,m,N

and
                                      |Φ(m) (x)| ≤ C2.46,m,N ⟨x⟩N ,                                (2.116)
                       4m+2N 2 +5N                               4m+2N 2 +6N +2
where C̃2.46,m,N = 2                  and C2.46,m,N = 2                           .
Proof (). Let                                X
                                     al =             2−i−3 = 14 − 2−l−2 .
                                              i∈[l)
The Fourier transform of Φl is the convolution of 1[−3/4,3/4] with probability densities
supported on the intervals [−2−i−3 , 2−i−3 ], i ∈ [l). Hence it takes values in [0, 1], is
supported in
                    [−3/4 − al , 3/4 + al ] = [−1 + 2−l−2 , 1 − 2−l−2 ],
and is equal to one on
                     [−3/4 + al , 3/4 − al ] = [−1/2 − 2−l−2 , 1/2 + 2−l−2 ].
32                VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

  Every factor in the product defining Φl has modulus at most one. Thus |Φl | decreases
pointwise in l. For l ≥ 2, |Φl | ≤ |Φ2 |, and Φ2 ∈ L1 (R). Dominated convergence gives
convergence in L1 , while convergence in L∞ follows by uniform convergence on compact
sets together with the uniform decay supplied by the two first factors. Denote the limit
by Φ. The preceding support and plateau statements pass to the limit.
  For r ∈ N, differentiating the first r convolution factors gives
                                         Y
                             b (r) ∥∞ ≤
                            ∥Φ              2i+3 = 2r(r−1)/2+3r .
                                           i∈[r)

Since
                                     (m) (ξ) = (2πiξ)m Φ(ξ),
                                    Φd                 b
the Leibniz rule gives
                                   min(m,N )      
                 (m) )(N ) (ξ) =
                                     X        N                            b (N −q) (ξ).
               (Φd                                       m!
                                                       (m−q)!
                                                              (2πi)m ξ m−q Φ
                                     q=0
                                              q

Using |ξ| ≤ 1 on the support, the preceding derivative estimate, and the elementary
bounds for the binomial coefficients and factorial quotients, we obtain
                                                                 2
                                   (m) )(N ) ∥
                                ∥(Φd                4m+2N +5N
                                               ∞ ≤ 2          .
In particular, Φ
               b is smooth and compactly supported, so Φ is a Schwartz function.
Applying Lemma 2.43 when N ≥ 2, and the same integration-by-parts estimate directly
when N ∈ [2), yields
                                             2                 2
          |Φ(m) (x)| ≤ 2N +2 max 24m , 24m+2N +5N ⟨x⟩N ≤ 24m+2N +6N +2 ⟨x⟩N .
                                                 

                                                                                                □
Proposition 2.47. Let 0 < λ ≤ µ with 1 ≤ µ and let λ|y| ≤ µ|x|. Then for every
s, N > 0,
                            µ−N ⟨x⟩N
                                   (s) ≤ λ
                                          −N
                                             ⟨y⟩N
                                                (s) .                  (2.117)
Proof. We have, lowering both summands in the bracket on the left-hand side,
                         s−1 (µ + s−1 µ|x|)−N ≤ s−1 (λ + s−1 |λy|)−N .
Pulling out the factors µ and λ proves the proposition.                                         □
Proposition 2.48 (two bump estimate). Consider real numbers xi and si > 0 and
ni > 1 for i = 0, 1. Assume s0 ≥ s1 and define
                   C2.48,n0 ,n1 = 21+min(n0 ,n1 ) [1 + (min(n0 , n1 ) − 1)−1 ]             (2.118)
Then
                   1
                 Z Y
                                                                  min(n ,n )
                | ( ⟨xi − p⟩n(sii ) )dp| ≤ C2.48,n0 ,n1 ⟨x0 − x1 ⟩(s0 ) 0 1 .              (2.119)
                   R i=0
                          NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                        33

Proof. Let us prove (2.119). By translating p we may assume x0 = −x1 .
  If |x0 − x1 | ≤ 2s0 , we estimate the the first bump by its L∞ norm, which is s−1  i ,
and the second bump by its L norm. The latter is equal to the L norm of ⟨x⟩n1 ,
                                  1                                     1

which in turn is estimated by splitting the integral at |x| < 1 and |x| > 1 and thus by
2 + 2(n1 − 1)−1 . This gives the desired estimate.
  If |x0 − x1 | > 2s0 , we split the integral into positive and negative axis and do the
favorable L1 - L∞ estimate on either side. The L1 norm is estimated as above, possibly
with n0 in place of n1 if needed. The L∞ norm is bounded by
                                          s−1  −1
                                           i (si |x0 − x1 |/2)
                                                              − min(n0 ,n1 )
                                                                                                                     (2.120)
for suitable i, which is however maximized by i = 0.                                                                         □
Proposition 2.49. Let α0 , α1 ∈ R2 be linearly independent unit vectors. Then for every
x ∈ R2 we have
                            |x · α0⊥ | ≤ 2|α0 · α1⊥ |−1 |x · α1 |               (2.121)
or
                            |x · α1⊥ | ≤ 2|α0 · α1⊥ |−1 |x · α0 |               (2.122)
Proof (). Put
                             s = |α0 · α1⊥ |, c = |α0 · α1 |.
                2    2
Then s > 0 and s + c = 1. Suppose that the first asserted inequality fails. Writing α1
in the orthonormal basis α0 , α0⊥ gives
                         s|x · α0⊥ | ≤ |x · α1 | + c|x · α0 | < 2s |x · α0⊥ | + c|x · α0 |.
Consequently,
                                |x · α0⊥ | < 2cs−1 |x · α0 |.
Writing α1⊥ in the same basis, we obtain
              |x · α1⊥ | ≤ s|x · α0 | + c|x · α0⊥ | < (s2 + 2c2 )s−1 |x · α0 | ≤ 2s−1 |x · α0 |.
Thus the second asserted inequality holds.                                                                                   □
Proposition 2.50 (orthogonal decay). Let α0 , α1 ∈ R2 be linearly independent unit
              ⊥
vectors. Let αm be unit vectors orthogonal to αm and note that α0 · α1⊥ ̸= 0. Setting
                      C2.50,α0 ,α1 ,n0 ,n1 = max((2|α0 · α1⊥ |−1 )n0 , (2|α0 · α1⊥ |−1 )n1 ) ,                       (2.123)
then for all n0 , n1 , s0 , s1 > 0 and x ∈ R2 ,
 ⟨x·α0 ⟩n(s00 ) ⟨x·α1 ⟩n(s11 ) ≤ C2.50,α0 ,α1 ,n0 ,n1 (⟨x·α0 ⟩n(s00 ) ⟨x·α0⊥ ⟩n(s11 ) +⟨x·α1⊥ ⟩n(s00 ) ⟨x·α1 ⟩n(s11 ) ). (2.124)
Proof. This follows from Propositions 2.47 and 2.49                                                                          □
Proposition 2.51 (bump triangle). Let α0 , α1 ∈ R2 and let α2 = c0 α0 + c1 α1 be a
non-trivial linear combination of α0 , α1 , i.e. c0 ̸= 0, c1 ̸= 0. Let
                            C̃2.51,c0 ,c1 = max(2|c0 |, (2|c0 |)−1 , 2|c1 |, (2|c1 |)−1 ),                           (2.125)
                                                             n0              n1
                                C2.51,c0 ,c1 ,n0 ,n1 = max(C̃2.51,c0 ,c1
                                                                         , C̃2.51,c0 ,c1
                                                                                         ).                          (2.126)
Then
 ⟨x·α0 ⟩n(s00 ) ⟨x·α1 ⟩n(s11 ) ≤ C2.51,c0 ,c1 ,n0 ,n1 (⟨x·α0 ⟩n(s00 ) ⟨x·α2 ⟩n(s11 ) +⟨x·α2 ⟩n(s00 ) ⟨x·α1 ⟩n(s11 ) ). (2.127)
34                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Remark 2.3. It is not needed that α0 , α1 are linearly independent, but in the linearly
dependent case the proposition becomes trivial.
Proof. We have by the triangle inequality and estimating the sum by twice the maximum
                              |x · α2 | ≤ max(2|c0 ||x · α0 |, 2|c1 ||x · α1 |) .   (2.128)
Assume the maximum is attained by one of the terms with index i. If 2|ci | ≥ 1, apply
Proposition 2.47 with λ = 1 and µ = 2|ci |. If 2|ci | < 1, apply Proposition 2.47 with
λ = 2|ci | and µ = 1.                                                               □
                                            2
     Recall the Gaussian g(x) = e−πx for x ∈ R.
Proposition 2.52 (Gaussian domination). Let N, s ∈ R, N > 1, and s > 0. Then
                                        X
                     ⟨x⟩N(s) ≤ C2.52 2N
                                          2(1−N )m g(2m s) (x),          (2.129)
                                                    m∈N
                  π
where C2.52 = e .
Proof. The case for general s follows from the case s = 1 by scaling. Consider s = 1.
For |x| ≤ 1, the summand m = 0 on the right hand side suffices as it is at least 1.
  For |x| > 1 there is m ∈ N with 2m−1 < |x| ≤ 2m , and we estimate
                            ⟨x⟩N ≤ (2m−1 )−N ≤ (2m−1 )−N 2m eπ g(2m ) (x) .         (2.130)
which is the m-th term on the right hand side.                                           □
Proposition 2.53 (diagonal square root). For t0 , t1 ∈ R with 0 < 2t0 ≤ t1 define
                                      p
                        s = F −1 (ξ 7→ g(t0 ξ) − g(t1 ξ)),                     (2.131)
where the function under the square root is nonnegative. Then s ∈ W0 (R). For all
N ∈ N with N ≥ 1 and x ∈ R, the following estimate holds:
                                  |s(x)| ≤ C2.53,N (⟨x⟩N          2
                                                       (t0 ) + ⟨x⟩(t1 ) ),          (2.132)
                   √
where C2.53,N =        2 max(C2.36,0,N , C2.36,0,2 C2.40 C2.48,2,2 ).
Proof. The function s is real-valued because it is the inverse Fourier transform of an
even real-valued function. By algebra, we obtain,
                                             1 p
                             sb(ξ) = g(t0 2− 2 ξ) 1 − g(rξ),                    (2.133)
                        1
where r = (t21 − t20 ) 2 . Let ρ be the function from Proposition 2.40 satisfying
                                                p
                                     ρb(ξ) = 1 − 1 − g(ξ).                          (2.134)
Then
                                        sb(ξ) = g(σξ)(1 − ρb(rξ)),                  (2.135)
                − 12
where σ = t0 2 .
  By Proposition 2.40,
                                            ρ(x) ≤ C2.40 ⟨x⟩2 .                     (2.136)
It follows
                                          s = g(σ) − g(σ) ∗ ρ(r) .                  (2.137)
                            NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                            35

We use Proposition 2.36 to obtain
                                            |g(σ) (x)| ≤ C2.36,0,N ⟨x⟩N
                                                                      (σ)

and Proposition 2.48, using r > σ by assumptions on ti , i = 0, 1, to obtain
                                |(g(σ) ∗ ρ(r) )(x)| ≤ C2.36,0,2 C2.40 C2.48,2,2 ⟨x⟩2(r) .
This gives
             |s(x)| ≤ max(C2.36,0,N , C2.36,0,2 C2.40 C2.48,2,2 )(⟨x⟩N        2
                                                                     (σ) + ⟨x⟩(r) ) .       (2.138)
                        1
                                  √
     Since σ = t0 2− 2 and          3
                                   2 1
                                      t ≤ r ≤ t1 , we obtain (2.132). In particular, s ∈ W0 (R).   □
Lemma 2.54 (constant C2.53,N ()). For every N ≥ 1,
                                                                           2
                                           C2.53,N ≤ 21+max((N +1) ,12) .                   (2.139)
Moreover,                                                    √
                                            C2.53,2 = 51 · 26 2 < 213 .                     (2.140)
Proof (). Using the defining maximum in Proposition 2.53, and by (2.93),
                                                                                  2
                                      C2.36,0,N = (4(N + 1))N/2 ≤ 2(N +1) .
Also
                                        C2.36,0,2 = 12,         C2.48,2,2 = 16,
so
                           C2.36,0,2 C2.40 C2.48,2,2 = 3264 < 212 .
Substitution in the defining maximum proves the first estimate. At N = 2, the second
entry in the maximum is the larger one, which gives the stated exact value.        □
Proposition 2.55 (derivative of diagonal square root). Let t0 , t1 , s be as in Proposition
2.53. Then for all N ∈ N with N ≥ 1 and all x ∈ R:
                                                      N           2
                      |s′ (x)| ≤ C2.55,N (t−1                 −1
                                             0 ⟨x⟩(t0 ) + t1 ⟨x⟩(t1 ) ),                    (2.141)
                                                               
where C2.55,N = 2 max C2.36,1,N , C2.36,0,2 C2.36,1,2 C2.48,2,2 .
Proof (). By algebra, we obtain
                                                           1
                                         sb(ξ) = g(t0 2− 2 ξ)
                                                                p
                                                                 1 − g(rξ),
                            1
where r = (t21 − t20 ) 2 . Let ρ be the function from Proposition 2.40 satisfying
                                                p
                                     ρb(ξ) = 1 − 1 − g(ξ).
Then
                                            sb(ξ) = g(σξ)(1 − ρb(rξ)),
                 − 12
where σ = t0 2 .
  The power series identity
                                                         ∞
                                           √
                                                                           
                                                         X
                                                                 1        2k −k k
                                      1−       1−z =           2k−1
                                                                              4 z
                                                         k=1
                                                                          k
36                      VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

has nonnegative coefficients whose sum is 1. Since
                                     √             1
                                  ∥g( k ·)∥1 = k − 2 ,
Proposition 2.37 gives
                                             ∞             
                                             X
                                                     1     2k −k √
                                   ρ(x) =          2k−1
                                                              4 g( k) (x).
                                             k=1
                                                            k
The series and its differentiated series converge uniformly by Proposition 2.36. Hence
                                     ∞         
                             ′
                                    X
                                           1   2k −k ′ √
                            ρ (x) =      2k−1
                                                  4 g( k) (x).
                                    k=1
                                               k
By Proposition 2.36,
                                      1                       √
           g′(√k) (x) ≤ C2.36,1,2 k − 2 ⟨x⟩2(√k) = C2.36,1,2 ( k + |x|)−2 ≤ C2.36,1,2 ⟨x⟩2 .
It follows that
                                           |ρ′ (x)| ≤ C2.36,1,2 ⟨x⟩2 .
Consequently,
                                      |(ρ(r) )′ (x)| ≤ C2.36,1,2 r−1 ⟨x⟩2(r) .
     We have
                                            s = g(σ) − g(σ) ∗ ρ(r)
and therefore
                               s′ = g′(σ) − g(σ) ∗ (ρ(r) )′ .
We use Proposition 2.36 to obtain
                                       |g′(σ) (x)| ≤ C2.36,1,N σ −1 ⟨x⟩N
                                                                       (σ)

and Proposition 2.48, using r > σ by the assumptions on ti , i = 0, 1, to obtain
                      |(g(σ) ∗ (ρ(r) )′ )(x)| ≤ C2.36,0,2 C2.36,1,2 C2.48,2,2 × r−1 ⟨x⟩2(r) .
This gives
        |s′ (x)| ≤ max C2.36,1,N , C2.36,0,2 C2.36,1,2 C2.48,2,2 × σ −1 ⟨x⟩N      −1  2
                                                                                        
                                                                           (σ) + r ⟨x⟩(r) .
                  1
                            √
Since σ = t0 2− 2 and         3
                             2 1
                                t ≤ r ≤ t1 , we have
                                          σ −1 ⟨x⟩N       −1   N
                                                  (σ) ≤ 2t0 ⟨x⟩(t0 )

and
                                          r−1 ⟨x⟩2(r) ≤ 2t−1   2
                                                          1 ⟨x⟩(t1 ) .
The desired estimate follows.                                                                        □
Lemma 2.56 (constant C2.55,N ()). For every N ≥ 1,
                                                                    2
                                       C2.55,N ≤ 21+max((N +1) +4,15) .                         (2.142)
Moreover,                                                 √
                                         C2.55,2 = 9 · 212 2 < 216 .                            (2.143)
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                             37

Proof (). By (2.93),
                                      √                        2
                         C2.36,1,N = 8 2(4(N + 1))N/2 ≤ 2(N +1) +4 .
Furthermore,
                                                        √
                  C2.36,0,2 = 12,         C2.36,1,2 = 96 2,
                                                          C2.48,2,2 = 16.
                                                                  √
The second entry in the defining maximum is therefore 18432 2 < 215 . Substitution
proves the first estimate. At N = 2, this entry is the larger one; multiplication by the
outer factor 2 gives the stated exact value.                                          □
Lemma 2.57. Let N ∈ N. Then for ξ ∈ R, |ξ| ≤ 1, we have
                                       |(g−1 )(N ) (ξ)| ≤ C2.57,N ,                    (2.144)
                  P⌊N/2⌋
where C2.57,N = eπ l=0 l!(NN−2l)!
                             !
                                  2N −2l π N −l .
                                   2
Proof. We have g−1 (ξ) = eπξ . The desired estimate then follows from the equality
                                                       ⌊N/2⌋
                       −1 (N )
                                        √       2
                                                     X N −2l √
                   (g )          (ξ) = ( π)N eπξ N !    2
                                                      l!(N −2l)!
                                                                 ( πξ)N −2l .
                                                        l=0
                                                                                            □
Lemma 2.58. Let c > 0, N ∈ N and assume that ϕ is a W0 (R) function such that ϕb is
supported in [−1, 1], ϕb is N times continuously differentiable and max0≤m≤N ∥ϕb(m) ∥∞ ≤
c. For µ ∈ (0, 1] and ξ ∈ R, we define
                                  Q(ξ) = (g(µξ))−1 ϕ(ξ).
                                                    b                            (2.145)
Then Q is N times continously differentiable and
                          ∥(2π)−N Q(N ) ∥∞ ≤ cC2.58,N ,                                (2.146)
where C2.58,N = (2π)−N N   N
                      P      
                       l=0 l C2.57,l .

Proof. This follows from the Leibniz rule, Lemma 2.57 and from the facts that µ ≤ 1
and ϕb is supported in the set where |ξ| ≤ 1.                                    □
Lemma 2.59 (constant C2.58,N ()). For every N ∈ N,
                                                               2
                                         C2.58,N ≤ 28(N +1) .                          (2.147)
For 0 ≤ N ≤ 3,
       C2.58,0 < 81,       C2.58,1 < 95,          C2.58,2 < 124,      C2.58,3 < 176.   (2.148)
Proof (). Since π < 4 and e < 3, we have eπ < e4 < 34 = 81 < 27 . For 0 ≤ l ≤ N , the
defining formula in Lemma 2.57 then gives
                                                               2
                                          C2.57,l ≤ 27(N +1) .
Here the case N = 0 is immediate, and for N ≥ 1 we use that the sum has at most
N + 1 terms, l! ≤ (N + 1)N , 2l ≤ 2N , and π l < 22N . The binomial coefficients in the
definition of C2.58,N sum to 2N , and (2π)−N ≤ 1, which proves the first estimate.
38                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

  The exact formulas for N = 0, 1, 2, 3 give, respectively,
                                                                   
     π      π       1          π         3     1            π   3  3  1
    e ,    e 1+         ,    e 1+          +        ,     e 1+ + 2 + 3 .
                   2π                   2π 4π 2                 π 2π 8π
Using eπ < 81 and π > 3, these four expressions are smaller than
                                               189         495           1407
                                   81,          2
                                                   ,        4
                                                               ,          8
                                                                              ,
which gives the four displayed bounds.                                                    □
Lemma 2.60. Let N ∈ N, ν ∈ [−1, 0) and let H(x) = (1 − x)ν − 1 for x ∈ [0, 1). Then
for x ∈ [0, e−3π/16 ], we have
                                  |H (N ) (x)| ≤ C2.60,N ,                   (2.149)
                                 −(N +1)
where C2.60,N = N ! 1 − e−3π/16
                                
                                         .
Proof. Assume that N > 0. Then
                                                Y
                                H (N ) (x) =           (|ν| + l)(1 − x)ν−N ,
                                               l∈[N )

and so                                                               −(N +1)
                               |H (N ) (x)| ≤ N ! 1 − e−3π/16                         .
Also,
                                                                          −1
                                           x
                                 |H(x)| ≤ 1−x ≤ 1 − e−3π/16                       .
This yields the claim.                                                          □
                                                 √
Lemma 2.61. Let N ∈ N, ν ∈ [−1, 0), t ≥ 3/2, and let S(ξ) = (1 − g(tξ))ν − 1 for
ξ ̸= 0. For |ξ| ≥ 1/2,
                                |S (N ) (ξ)| ≤ C2.61,N |ξ|−2 ,             (2.150)
where
                                C2.61,0 = 2C2.60,0 C2.36,0,2 ,             (2.151)
and, for N ≥ 1,                          X             Y
                       C2.61,N = 2N +1       C2.60,|p|    C2.36,|B|,N +2 . (2.152)
                                                p∈Π            B∈p
Here p runs through the partitions of [N ), B through the blocks of p, |p| is the number
of blocks, and |B| is the size of B.
Proof. Let H be as in Lemma 2.60. If N = 0, then, since H(0) = 0, Lemmas 2.60 and
2.36 give
                     |S(ξ)| ≤ C2.60,0 g(tξ) ≤ 2C2.60,0 C2.36,0,2 |ξ|−2 .
  Assume N ≥ 1. For t = 1, the Faà di Bruno formula gives
                                    X                  Y
                       S (N ) (ξ) =     H (|p|) (g(ξ))   g(|B|) (ξ).
                                           p∈Π                     B∈p
            √
For |ξ| ≥       3/4, Lemma 2.60 and Proposition 2.36 yield
                                       X           Y
                        |S (N ) (ξ)| ≤   C2.60,|p|   C2.36,|B|,N +2 ⟨ξ⟩N +2 .
                                         p∈Π             B∈p
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                           39
                  √
For general t ≥       3/2 and |ξ| ≥ 1/2, rescaling gives an additional factor tN , and
                             tN ⟨tξ⟩N +2 ≤ t−2 |ξ|−N −2 ≤ 2N +1 |ξ|−2 .
This proves (2.150).                                                                        □
Lemma 2.62 (constant C2.61,N ()). For every N ∈ N,
                                                              3
                                       C2.61,N ≤ 210(N +1) .                           (2.153)
Moreover,
       C2.61,0 ≤ 72,        C2.61,1 < 215 ,        C2.61,2 < 234 ,   C2.61,3 < 258 .   (2.154)
Proof (). Since π > 3, we have 3π/16 > 9/16. The estimate ex ≥ 1 + x for x ≥ 0 gives
                                                     9  1
                         1 − e−3π/16 > 1 − e−9/16 ≥    > .
                                                    25  3
Consequently, Lemma 2.60 gives
                                         C2.60,q ≤ q!3q+1 .
Together with Proposition 2.36, the fact that a partition of [N ) has at most N blocks,
and the bound N N for the number of partitions, this proves the first estimate by sub-
stitution in the defining sum of Lemma 2.61.
   For N = 0, the defining formula gives
                                              C2.61,0 ≤ 72.
For N = 1, it gives                   √
                      C2.61,1 ≤ 18432 2 < 27648 < 215 ,
     √
where 2 < 3/2. For N = 2, direct substitution gives
                                  C2.61,2 ≤ 8852889600 < 234 .
For N = 3, the defining sum is
                      √                √                      √
           679477248 6 + 31701690482688 2 + 146081389744226304 3.
      √         √              √
Using 6 < 5/2, 2 < 3/2, and 3 < 7/4, this is smaller than
                                  255689986286813184 < 258 .
                                                                                            □
Lemma 2.63. Let c > 0, N ∈ N and assume that ϕ is a W0 (R) function such that
ϕb is supported in [−1, 1] and equal to 1 on [−1/2, 1/2] and ϕb is N times continuously
                                                                                  √
differentiable and max0≤m≤N ∥ϕb(m) ∥∞ ≤ c. Assume that 0 < µ ≤ λ ≤ 1/2, t ≥ 3/2
and ν ∈ [−1, 0). For ξ ∈ R, we define
                                                 
                                 −1 b
                  R(ξ) = (g(µξ))      ϕ(λξ) − ϕ(ξ) ((1 − g(tξ))ν − 1) .
                                              b                                 (2.155)
Then R is N times continuously differentiable and
                    (2π)−N max(∥R(N ) ∥1 , ∥R(N ) ∥∞ ) ≤ cC2.63,N ,                    (2.156)
where C2.63,N = 8 N   N
                 P         l−N
                  l=0 l (2π)    C2.58,l C2.61,N −l .
40                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof. Let                                                
                             Q(ξ)
                             e    = (g(µξ))−1 ϕ(λξ)
                                               b    − ϕ(ξ)
                                                      b      .
     By Lemma 2.58 and by the fact that µ ≤ λ ≤ 1, we obtain for any l ∈ N, l ≤ N ,
                              ∥(2π)−l Q
                                      e(l) ∥∞ ≤ 2cC2.58,l .                    (2.157)
We observe that R is supported where 1/2 ≤ |ξ| ≤ 1/λ. Using (2.157), Lemma 2.61
and the Leibniz rule, we obtain for |ξ| ≥ 1/2,
                                   N  
                                  X     N
                      (N )
                   |R (ξ)| ≤ 2c             (2π)l C2.58,l C2.61,N −l |ξ|−2 .
                                  l=0
                                         l
This yields (2.156).                                                                      □
Lemma 2.64 (constant C2.63,N ()). For every N ∈ N,
                                                          3
                                     C2.63,N ≤ 220(N +1) .                          (2.158)
Moreover,
                               C2.63,0 < 216 ,      C2.63,1 < 222 ,                 (2.159)
                               C2.63,2 < 238 ,      C2.63,3 < 260 .                 (2.160)
Proof (). Using the defining sum in Lemma 2.63, substitute the estimates from the
defining formulas of Lemmas 2.58 and 2.61. Bounding the N + 1 summands and the
binomial coefficients gives the first estimate. For N = 0, 1, 2, 3, use the finite estimates
in Lemmas 2.59 and 2.62, together with (2π)−1 < 1/6. Direct substitution in the four
finite sums gives, respectively,
             46656,      3040704,      159359088384,          767070519557262336,
which proves the displayed estimates.                                                     □
Lemma 2.65. Let ϕ be a W0 (R) function such that ϕb is supported in [−1, 1] and equal
to 1 on [−1/2, 1/2]. Let µ± , λ± ∈ R be positive and satisfy
                                    2µ− ≤ 2λ− ≤ λ+ ≤ µ+ ,                           (2.161)
and let ν ∈ [−1, 0).
  Define a function ρ by
                                                                  
                ρ = F −1 ξ 7→ (ϕ(λ      b + ξ))(g(µ− ξ) − g(µ+ ξ))ν .
                               b − ξ) − ϕ(λ                                         (2.162)
Also, for ξ ∈ R we define
                              ϱ0 (ξ) = (g(µ− |ν|1/2 ξ))−1 ϕ(λ
                                                           b − ξ)                   (2.163)
                            ϱ1 (ξ) = −(g(µ− |ν|1/2 ξ))−1 ϕ(λb ξ)                    (2.164)
                                                          +
        ϱ2 (ξ) = (g(µ− |ν|1/2 ξ))−1 ϕ(λ          b + ξ) ((1 − g(tξ))ν − 1)
                                       b − ξ) − ϕ(λ                                 (2.165)
        p
with t = µ2+ − µ2− . Then ρ is a well-defined continuous function and
                                          X
                                       ρ=      F −1 (ϱl ).                          (2.166)
                                            l∈[3)
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                          41

Proof. Applying Lemmas 2.57 and 2.63 with N = 0, we obtain that ϱl , l ∈ [3), are
continuous compactly supported functions. Therefore, their inverse Fourier transform
is well-defined and continuous. The decomposition (2.166) follows by algebra and ele-
mentary properties of g. Thus, ρ is a well defined continuous function. Additionally,
ρ is real-valued because it is the inverse Fourier transform of an even real-valued func-
tion.                                                                                  □
Proposition 2.66 (four scale Gaussian kernel estimate). Let c > 0, N ∈ N with N ≥ 2
and assume that ϕ is a W0 (R) function such that ϕb is supported in [−1, 1] and equal to 1
on [−1/2, 1/2] and ϕb is N times continuously differentiable and max0≤m≤N ∥ϕb(m) ∥∞ ≤ c.
Let µ± , λ± ∈ R be positive and satisfy (2.161), let ν ∈ [−1, 0) and let ρ be defined
by (2.162). Then ρ ∈ W0 (R) and for every x ∈ R,
                            |ρ(x)| ≤ cC2.66,N (⟨x⟩N          N
                                                  (λ− ) + ⟨x⟩(λ+ ) ),              (2.167)
where
        C2.66,N = 2C2.43,N max(C2.58,0 , C2.58,N ) + 2N max(C2.63,0 , C2.63,N ).   (2.168)
Proof. Let ϱl , l ∈ [3), be as in Lemma 2.65. Rescaling the functions ϱ0 and ϱ1 so that
λ− = 1 or λ+ = 1, respectively, applying Lemmas 2.43 and 2.58 and then rescaling
back, we obtain
                  |F −1 (ϱ0 )(x)| ≤ 2cC2.43,N max(C2.58,0 , C2.58,N ) ⟨x⟩N
                                                                         (λ− )

and
                  |F −1 (ϱ1 )(x)| ≤ 2cC2.43,N max(C2.58,0 , C2.58,N ) ⟨x⟩N
                                                                         (λ+ ) .
Also, rescaling the function ϱ2 so that λ+ = 1, applying Lemmas 2.41, 2.42 and 2.63
and then rescaling back, we obtain
                     |F −1 (ϱ2 )(x)| ≤ 2N c max(C2.63,0 , C2.63,N ) ⟨x⟩N
                                                                       (λ+ ) .

Applying the decomposition (2.166), we get the desired estimate. In particular, since
N ≥ 2, we get ρ ∈ W0 (R).                                                          □
Lemma 2.67 (constant C2.66,N ()). For every N ∈ N,
                                                           3
                                      C2.66,N ≤ 225(N +1) .                        (2.169)
Moreover,
                               C2.66,2 < 240 ,      C2.66,3 < 263 .                (2.170)
Proof (). Using the defining formula in Proposition 2.66, substitute C2.43,N = 2N and
the defining estimates from Lemmas 2.58 and 2.63. This proves the first estimate. For
N = 2, Lemmas 2.59 and 2.64 give
                        C2.58,2 < 124,        C2.63,2 < 159359088384.
For N = 3, use
                    C2.58,3 < 176,        C2.63,3 < 767070519557262336.
42                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Substitution in (2.168) gives the two upper bounds
                     637436354528         and       6136564156458101504,
respectively.                                                                                  □
Proposition 2.68 (mean value four scale Gaussian kernel estimate). Let c > 0, N ∈
N with N ≥ 2 and assume that ϕ is a W0 (R) function such that ϕb is supported in
[−1, 1] and equal to 1 on [−1/2, 1/2] and ϕb is N times continuously differentiable and
max0≤m≤N ∥ϕb(m) ∥∞ ≤ c. Let µ± , λ± ∈ R be positive and satisfy (2.161). Assume, in
addition, that λ+ = 2λ− . Let ν ∈ [−1, 0) and let ρ be defined by (2.162). Then for all
x, y ∈ R,
        |ρ(x + y) − ρ(x)| ≤ cC2.68,N min(1, 2πλ−1            N          N
                                               + |y|)(⟨x + y⟩(λ+ ) + ⟨x⟩(λ+ ) ),          (2.171)
where                                                              
                                                            l
                   C2.68,N = C2.44,N 5 max C2.58,l + 4 max 2 C2.63,l .                    (2.172)
                                          0≤l≤N                   0≤l≤N

Proof. By homogeneity, we may assume λ+ = 1. Then λ− = 1/2. Let ϱl , l ∈ [3), be
as in Lemma 2.65. Rescaling the function ϱ0 so that λ− = 1, applying Lemmas 2.44
and 2.58 and then rescaling back, we obtain
|F −1 (ϱ0 )(x + y) − F −1 (ϱ0 )(x)| ≤ cC2.44,N max C2.58,l min(1, 4π|y|)(⟨x + y⟩N          N
                                                                                (1/2) + ⟨x⟩(1/2) )
                                              0≤l≤N


                  ≤ c4C2.44,N max C2.58,l min(1, 2π|y|)(⟨x + y⟩N + ⟨x⟩N ).
                               0≤l≤N

Similarly, applying Proposition 2.44 and Lemma 2.58 to the function ϱ1 , we obtain
 |F −1 (ϱ1 )(x + y) − F −1 (ϱ1 )(x)| ≤ cC2.44,N max C2.58,l min(1, 2π|y|)(⟨x + y⟩N + ⟨x⟩N ).
                                                0≤l≤N

   To estimate ϱ2 , we first consider its rescaled version ϱe2 = ϱ2 (2·), which is supported
in [−1, 1]. By Lemma 2.63, we have for l ∈ N, l ≤ N ,
                                                        (l)
                       ∥(2π)−l ϱe2 (l) ∥∞ = 2l ∥(2π)−l ϱ2 ∥∞ ≤ c2l C2.63,l .
By Proposition 2.44,
|F −1 (ϱ2 )(x + y) − F −1 (ϱ2 )(x)| ≤ c4C2.44,N max 2l C2.63,l min(1, 2π|y|)(⟨x + y⟩N + ⟨x⟩N ).
                                                0≤l≤N

Using the decomposition (2.166), we get (2.171).                                               □
Lemma 2.69 (constant C2.68,N ()). For every N ∈ N,
                                                              3
                                       C2.68,N ≤ 230(N +1) .                              (2.173)
Moreover,
                                          C2.68,2 < 245 .                                 (2.174)
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                  43

Proof (). By (2.112), C2.44,N ≤ 22N +1 . Substitution of the defining estimates from
Lemmas 2.58 and 2.63 proves the first bound. For N = 2, the inequality π > 3 gives
(1 + (2π)−1 )2 < 2, so C2.44,2 = 23 , exactly as in the preceding value. Use the finite
estimates in Lemmas 2.59 and 2.64. In the second maximum in (2.172), the term with
l = 2 is the largest. Substitution gives
                              C2.68,2 < 20397963318112 < 245 .
                                                                                                □
                                 3. The main argument
  The main theorem of this section is Theorem 3.48 below.
3.1. The sandwich kernel. We first introduce and discuss some geometric parameters
useful to describe a family of kernels in Definition 3.6.
Definition 3.1 (geometric parameters). Let Γ be the set of triples (k, u, a) with k ∈ N,
1 ≤ k ≤ n, u ∈ [2)k , a ∈ (A2 )k so that dist(a0i , a1i ) < ∞ for all i ∈ [k). For a sequence
pair α = (α0 , α1 ) ∈ A2 we write ∆(α) = dist(α0 , α1 ) and for γ ∈ Γ let
                                             X
                                  ∆γ = 1 +          ∆(ai ).                              (3.1)
                                                  i∈[k)

Definition 3.2 (two unitary matrices). For u ∈ [2) define unitary
                                                                 matrices
                                                                          Wu ∈ R2×2
                                                               1 1
as follows: Let W0 be the 2 × 2 identity matrix and W1 = √12         .
                                                              −1 1
  Next, we introduce some functions and functional concepts involved in the family of
kernels of Definition 3.6.
Definition 3.3 (double sequence of 2D functions). For 1 ≤ k ≤ n, let Xk be the set of
double sequences
                                X = (Xi,j )i∈[k),j∈Z                            (3.2)
with Xi,j ∈ W0 (R2 ).
 The kernels of interest in Definition 3.6 will be partial sums over a sequence of kernels.
We introduce this concept of kernel sequences.
Definition 3.4 (kernel sequences). Let k ∈ N with 1 ≤ k ≤ n. Let M(k) be the space
of sequences M = (Mj )j∈Z such that for j ∈ Z we have Mj ∈ W0 ((R2 )k ). Define
                                                 k−n+1
                                                              X
             ∥M∥M(k) =      sup     min(1, J −1+2      )|Λk (   Mj )(F)| .      (3.3)
                           J∈N, J≥1, F∈F
                                                                        j∈[J)

                              −1+2k−n+1                   −1+2k−n+1
Remark 3.1. Note min(1, J                  ) equals J                 if k ≤ n − 1 and equals 1 if
k = n.
Definition 3.5 (2D Gaussians). For q ∈ R2 with q0 , q1 > 0, u ∈ [2), and v ∈ R2 , define
                           Gq,u (v) = g(q0 ) ((Wu v)0 )g(q1 ) ((Wu v)1 ).                    (3.4)
For γ = (k, u, a) ∈ Γ, define
                                      (Gγ )i,j = Gai (j),u(i) .                              (3.5)
44                VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

   A sandwich kernel is a product, most factors of which are two dimensional Gaussians
differently scaled and oriented using the data γ, while one factor, which is sandwiched
between these Gaussians, is different and determined by an element of Xk .
Definition 3.6 (sandwich kernel). Let γ = (k, u, a) ∈ Γ, X ∈ Xk , and i ∈ [k). Define
for j ∈ Z and y ∈ (R2 )k ,
                             Y                               k−1
                                                                Y                   
      (M(γ, X, i))j (y) =           (Gγ )m,j (ym ) Xi,j (yi )       (Gγ )m,j−1 (ym ) .   (3.6)
                            m∈[i)                            m=i+1

Remark 3.2. When k = 1, i = 0, M(γ, X, 0) doesn’t depend on u, a. Generally,
M(γ, X, i) does not depend on ui , ai .
Definition 3.7 (difference of 2D Gaussians). Let γ = (k, u, a) ∈ Γ. For i ∈ [k), j ∈ Z,
define
                             (Yγ )i,j = (Gγ )i,j−1 − (Gγ )i,j .                    (3.7)
Proposition 3.8 (telescoping terms). Let γ = (k, u, a) ∈ Γ. Then Yγ ∈ Xk and
                              X
                            ∥    M(γ, Yγ , i)∥M(k) ≤ 2.                                  (3.8)
                                    i∈[k)

Proof. The fact that Yγ ∈ Xk follows from Proposition 2.11 since (Yγ )i,j ∈ S(R2 ) for
i ∈ [k), j ∈ Z. For a given J ∈ N with J ≥ 1:
                                 XX
                                         (M(γ, Yγ , i))j
                                     j∈[J) i∈[k)

telescopes into a difference of two boundary terms
                          Y                    Y
                             (Gγ )m,−1 (ym ) −   (Gγ )m,J−1 (ym ).
                        m∈[k)                      m∈[k)

Estimate each with Propositions 2.18 and 2.24 and then make use of the fact that the
L1 norm of both these terms equals 1.                                             □
Proposition 3.9 (positive terms). Let γ = (k, u, a) ∈ Γ. Let X ∈ Xk and assume
for each i ∈ [k) and j ∈ Z we have Xi,j (u, v) = fi,j (u)fi,j (v) for some real valued
fi,j ∈ W0 (R). Then for each i ∈ [k), j ∈ Z, and for all F ∈ F,
                                  Λk (M(γ, X, i)j )(F) ≥ 0.                              (3.9)
Proof. This follows from Proposition 2.26.                                                  □

3.2. Multipliers H, L, N .
Definition 3.10 (square root Gaussian difference). Let a ∈ A and j ∈ Z. Define the
function s(a, j) : R → R by
                                         p
                     s(a, j) = F −1 (ξ 7→ g(a(j − 1)ξ) − g(a(j)ξ)).         (3.10)
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                        45

Definition 3.11 (s multiplier). Let γ = (k, u, a) ∈ Γ. Let i ∈ [k) and j ∈ Z. Define
(sγ )i,j : R → R by
                                   (sγ )i,j = s(b, j)                         (3.11)
with                                 q
                              b(j) = a0i (j)2 + a1i (j)2                      (3.12)
if ui = 0, and by                                   √
                                       (sγ )i,j = s( 2a1i , j)                   (3.13)
if ui = 1.
Proposition 3.12. For every a ∈ A and j ∈ Z we have that s(a, j) is a well-defined
function in W0 (R). Consequently, if γ ∈ Γ and i ∈ [k), j ∈ Z, then (sγ )i,j is a well-
defined function in W0 (R).
Proof. The first part follows from Proposition 2.53. The second part follows from the
first part and Proposition 2.31.                                                   □
              \
  Note that s(a,  j) is not smooth at the origin, due to the square root. The function
s(a, j) only decays with second power.
Definition 3.13 (H multiplier). Let γ = (k, u, a) ∈ Γ. Define Hγ = (Hγ )i∈[k),j∈Z by
                             (Hγ )i,j = (sγ )i,j ⊗ (sγ )i,j − (Yγ )i,j           (3.14)
for every i ∈ [k), j ∈ Z.
Proposition 3.14. Let γ = (k, u, a) ∈ Γ. Then Hγ ∈ Xk .
Proof. This follows from Propositions 2.9, 3.8 and 3.12.                               □
Proposition 3.15 (H vanishing). For γ = (k, u, a) ∈ Γ, i ∈ [k), j ∈ Z, and ξ ∈ R,
                                         \
                                        (Hγ )i,j (ξ, −ξ) = 0 .                   (3.15)
Proof. Recall
                               (Yγ )i,j = (Gγ )i,j−1 − (Gγ )i,j
and with (2.94) and (2.95), if ui = 0, then
                                            q
                     (Gγ )i,j (ξ, −ξ) = g( (a0i (j))2 + (a1i (j))2 · ξ)
                       c

and if ui = 1, then                               √
                              cγ )i,j (ξ, −ξ) = g( 2a1i (j)ξ).
                             (G
The formulas above use Proposition 2.37. The proposition now follows with Definition
3.10 of sγ and Proposition 3.12.                                                   □
Proposition 3.16 (H vanishing integral). For γ = (k, u, a) ∈ Γ, i ∈ [k), j ∈ Z, and
z ∈ R,                     Z
                                       (Hγ )i,j (z + p, p) dp = 0.               (3.16)
                                   R

Proof. This follows from Proposition 3.15.                                             □
46                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Definition 3.17. Let γ = (k, u, a) ∈ Γ, i ∈ [k), j ∈ Z. For t > 0, we set
                                         (Lγ,t )i,j = (Hγ )i,j ∗(1,1) Φ(t) .                            (3.17)
Lemma 3.18. Let γ = (k, u, a) ∈ Γ and t > 0. Then Lγ,t ∈ Xk and for i ∈ [k), j ∈ Z,
we have
                          lim (Lγ,t )i,j = (Hγ )i,j in L1 .                  (3.18)
                                        t→0+

Proof. Lγ,t ∈ Xk by Propositions
                          R           2.11, 2.13 and 3.14.
  Using the fact that R Φ(t) (p) dp = 1, we write
                                    Z
    (Lγ,t )i,j (v) − (Hγ )i,j (v) =   Φ(t) (p)((Hγ )i,j (v1 − p, v2 − p) − (Hγ )i,j (v1 , v2 )) dp.
                                             R
  Applying the previous expression and Fubini’s theorem, we see that the L1 norm of
(Lγ,t )i,j − (Hγ )i,j is bounded by
                             Z                     Z
                               |Φ(t) (p)|ω(p) dp =   |Φ(q)|ω(tq) dq
                                   R                             R
where                          Z
                   ω(p) =              |(Hγ )i,j (v1 − p, v2 − p) − (Hγ )i,j (v1 , v2 )| dv.
                               R2
                                 1
By the continuity of the L norm, we have limt→0+ ω(tq) = 0 for every q ∈ R. Addi-
tionally, ω(tq) ≤ 2∥(Hγ )i,j ∥1 . Applying the Lebesgue dominated convergence theorem
finishes the proof.                                                                 □
Lemma 3.19. Let γ = (k, u, a) ∈ Γ, i ∈ [k), j ∈ Z, t > 0. Then
                                             lim (Lγ,t )i,j = 0       in L1 .                           (3.19)
                                             t→∞

Proof. Let t > 0. We have
                 Z                              Z                 Z
∥(Lγ,t )i,j ∥1 =   |(Lγ,t )i,j (x+y, y)| dxdy =                          Φ(t) (p)(Hγ )i,j (x+y−p, y−p) dp dxdy.
                 R2                                         R2       R
                                                                             (3.20)
By Proposition 3.16, H has integral zero in the diagonal direction. Using this and
making the change of variables q = y − p, (3.20) becomes
               Z    Z
                      (Φ(t) (y − q) − Φ(t) (y))(Hγ )i,j (x + q, q) dq dxdy.  (3.21)
                      R2   R
Performing a further change of variables z = y/t and using the triangle inequality, (3.21)
is bounded by              Z      
                               ω qt |(Hγ )i,j (x + q, q)| dxdq,
                                        R2
where                                            Z
                                       ω(p) =          |Φ(z − p) − Φ(z)| dz.
                                                   R
By the continuity of the L1 norm, we have limt→∞ ω(q/t) = 0 for every q ∈ R. Addition-
ally, ω(q/t) ≤ 2∥Φ∥1 . Applying the Lebesgue dominated convergence theorem finishes
the proof.                                                                          □
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                     47

Definition 3.20 (L multiplier). Let γ = (k, u, a) ∈ Γ.
 Define the index set
                Iγ = {(m, 0) : m ∈ Z, m ̸= 0} ∪ {(0, l) : |l| ≤ ∆γ } ⊂ Z2 .                      (3.22)
  For every ι ∈ Iγ , we define Lγ,ι = (Lγ,ι )i∈[k),j∈Z such that for |l| ≤ ∆γ ,
                     (Lγ,(0,l) )i,j = (Hγ )i,j ∗(1,1) (Φ(a1i (j+l−1)) − Φ(a1i (j+l)) ) ,         (3.23)
  if h > 0, then
               (Lγ,(h,0) )i,j = (Hγ )i,j ∗(1,1) (Φ(2h−1 a1i (j+∆γ )) − Φ(2h a1i (j+∆γ )) ) ,     (3.24)
and if h < 0, then
             (Lγ,(h,0) )i,j = (Hγ )i,j ∗(1,1) (Φ(2h a1i (j−∆γ −1)) − Φ(2h+1 a1i (j−∆γ −1)) ) .   (3.25)
Remark 3.3. Note that we could have equivalently used a0i in place of a1i .
Definition 3.21 (Summation over Iγ ). Let X be a normed R-vector space. Let γ =
(k, u, a) ∈ Γ and let Dι ∈ X for ι ∈ Iγ . We define
                              X                 X
                                   Dι = lim         Dι ,                  (3.26)
                                                N →∞
                                    ι∈Iγ                 ι∈Iγ , |ι|≤N

where the limit is taken in X.
Proposition 3.22 (Properties of L multipliers). Let γ = (k, u, a) ∈ Γ and ι ∈ Iγ . Then
Lγ,ι is a well-defined element of Xk . In addition, if i ∈ [k) and j ∈ Z then
                                             X
                                  (Hγ )i,j =    (Lγ,ι )i,j ,                      (3.27)
                                                       ι∈Iγ

where the sum on the right converges in L1 .
Proof. Each (Lγ,ι )i,j belongs to W0 (R2 ) by Propositions 2.11, 2.13 and 3.14. Thus,
Lγ,ι ∈ Xk .
  Let N ∈ N be such that N > ∆γ . Then
                X
                        (Lγ,ι )i,j = (Lγ,2−N a1i (j−∆γ −1) )i,j − (Lγ,2N a1i (j+∆γ ) )i,j .
              ι∈Iγ , |ι|≤N

An application of Lemmas 3.18 and 3.19 yields (3.27).                                                □
Lemma 3.23. Let γ = (k, u,  Pa) ∈ Γ. Assume X, Xι ∈ Xk for ι ∈ Iγ are such that for
every i ∈ [k), j ∈ Z, Xi,j = ι∈Iγ (Xι )i,j holds in L1 . Then for every i ∈ [k), j ∈ Z,
                                        X
                          M(γ, X, i)j =     M(γ, Xι , i)j in L1 .                    (3.28)
                                                ι∈Iγ

Proof. For N ∈ N and y ∈ (R2 )k ,
                                                       X
                              M(γ, X, i)j (y) −                M(γ, Xι , i)j (y)
                                                        ι∈Iγ
                                                       |ι|≤N
48                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

            Y                                X                k−1
                                                                   Y                   
       =            (Gγ )m,j (ym ) Xi,j (yi ) −   (Xι )i,j (yi )       (Gγ )m,j−1 (ym ) .
            m∈[i)                                  ι∈Iγ                  m=i+1
                                                  |ι|≤N

The Gaussian factors have finite L1 norms independent of N . The assumed L1 conver-
gence of the middle factor therefore gives the asserted L1 convergence.             □
                                                                         1
                                                    P
Lemma 3.24. Let γ = (k, u, a) ∈ Γ. If M =              ι∈Iγ Mι holds in L for M, Mι ∈
W0 ((R2 )k ), then for every F ∈ F,
                                               X
                            |Λk (M )(F)| ≤ sup    |Λk (Mι )(F)|.                (3.29)
                                                  N ∈N
                                                          ι∈Iγ
                                                         |ι|≤N

Here the supremum is taken in the extended half-line [0, ∞].
Proof. For N ∈ N, set
                                                          X
                                         EN = M −                 Mι .
                                                           ι∈Iγ
                                                          |ι|≤N

Then ∥EN ∥1 → 0. By the triangle inequality,
                                 X
                  |Λk (M )(F)| ≤     |Λk (Mι )(F)| + |Λk (EN )(F)|.
                                           ι∈Iγ
                                          |ι|≤N

Propositions 2.18 and 2.24 give
                                       |Λk (EN )(F)| ≤ ∥EN ∥1 .
Letting N → ∞ proves the claim.                                                                 □
Definition 3.25 (N multiplier). Let γ = (k, u, a) ∈ Γ and assume k ≤ n − 1. Let ν = 1
if k < n − 1 and ν = 2 if k = n − 1 and let i ∈ [k), j ∈ Z. For ι ∈ Iγ define functions
σγ,ι,i,j : R → R so that if |l| ≤ ∆γ ,
                                      σγ,(0,l),i,j = s(a1i (· + l), j)                      (3.30)
and for h > 0,
                                   σγ,(h,0),i,j = s(2h a1i (· + ∆γ ), j)                    (3.31)
and for h < 0,
                                  σγ,(h,0),i,j = s(2h a1i (· − ∆γ ), j).                    (3.32)
For every ι ∈ Iγ we define Nγ,ι = (Nγ,ι )i∈[k),j∈Z such that

                    (Nγ,ι )i,j = F −1 ((ξ, η) 7→ σ
                                                 \                −ν \
                                                   γ,ι,i,j (ξ + η) (Lγ,ι )i,j (ξ, η)) .     (3.33)
Proposition 3.26. Let γ = (k, u, a) ∈ Γ and assume k ≤ n − 1. Then for every ι ∈ Iγ ,
the double sequence Nγ,ι is well-defined and belongs to Xk .
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                               49

Proof. Each (Nγ,ι )i,j is real-valued because it is the inverse Fourier transform of an even
real-valued function. Additionally, (Nγ,ι )i,j can be written in the form
                                    (Nγ,ι )i,j = (Hγ )i,j ∗(1,1) ρ
for some function ρ : R → R. Thanks to Proposition 2.66, we have ρ ∈ W0 (R). Propo-
sition 3.14 yields that (Hγ )i,j ∈ W0 (R2 ). Thus, (Nγ,ι )i,j ∈ W0 (R2 ) by Proposition 2.13,
i.e. Nγ,ι ∈ Xk .                                                                           □
3.3. Gaussian domination.
Proposition 3.27 (Kernel estimate for Gaussian domination). Let γ = (k, u, a) ∈ Γ
and let i ∈ [k). There exists a finite multiset P ⊂ Bdist (a1i , ∆γ )2 × [2) with #P = 6 and
for every v ∈ R2 and j ∈ Z,
                                        X
                 |(Hγ )i,j |(v) ≤ C3.27       ⟨(Wu v)0 ⟩2(t0 (j)) ⟨(Wu v)1 ⟩2(t1 (j)) , (3.34)
                                        (t0 ,t1 ,u)∈P
                 2         2
where C3.27 = 4C2.53,2 + C2.36,0,2 .
Proof. For m, ℓ ∈ [2), j ∈ Z, let tm,ℓ (j) = aℓi (j + m − 1). Thus t0,ℓ (j) = aℓi (j − 1) and
t1,ℓ (j) = aℓi (j). By Propositions 2.31 and 2.33, we have tm,ℓ ∈ A and dist(a1i , tm,ℓ ) ≤ ∆γ .
   Assume first that u(i) = 0. For m ∈ [2), let t+    m = max(tm,0 , tm,1 ) ∈ A, and set

                   P = (tm , tm′ , 0) : m, m′ ∈ [2) ∪ {(tm,0 , tm,1 , 0) : m ∈ [2)} .
                        + +

By Proposition 2.31 and Proposition 2.33, if t is one of t+
                                                          m , tm,0 , tm,1 ∈ A, then

                                 dist(a1i , t) ≤ 1 + ∆(ai ) ≤ ∆γ ,
                      2
so P ⊂ Bdist (a1i , ∆γ ) × [2). Also by definition #P = 6.
  Fix j ∈ Z, and write s = (sγ )i,j and H = (Hγ )i,j . If b is the sequence in (3.11), then
                                                      √ +
                              t+
                               m (j) ≤ b(j + m − 1) ≤   2 tm (j).
  By Definitions 3.13 and 3.5, and the nonnegativity of the Gaussians,
                                                  1
                                                  X
                    |H(v)| ≤ |s(v0 )s(v1 )| +           g(tm,0 (j)) (v0 )g(tm,1 (j)) (v1 ).
                                                  m=0

Proposition 2.53, applied with N = 2, gives
                           |s(x)| ≤ 2C2.53,2 (⟨x⟩2(t+ (j)) + ⟨x⟩2(t+ (j)) ).
                                                        0               1

By Proposition 2.36 and scaling, g(r) (x) ≤ C2.36,0,2 ⟨x⟩2(r) . The claim follows.
  Assume now that u(i) = 1, and set
              P = {(tm,1 , tm′ ,1 , 0) : m, m′ ∈ [2)} ∪ {(tm,0 , tm,1 , 1) : m ∈ [2)} .
Again, #P = 6, and the required √ 1distance condition holds.
  In this case s = (sγ )i,j = s( 2ai , j). Moreover,
                                          1
                                          X                                           
              |H(v)| ≤ |s(v0 )s(v1 )| +         g(tm,0 (j)) (W1 v)0 g(tm,1 (j)) (W1 v)1 .
                                          m=0
50                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE
                          √
Comparing the scales          2tm,1 (j) with tm,1 (j) and applying Proposition 2.53 with N = 2,
we get
                       |s(x)| ≤ 2C2.53,2 (⟨x⟩2(t0,1 (j)) + ⟨x⟩2(t1,1 (j)) ).
Together Proposition 2.36 we obtain the claim.                                                         □
Lemma 3.28 (constant C3.27 ()).
                                   C3.27 = 512 · 215 + 122 < 227 .              (3.35)
                                                                  √
Proof (). Lemma 2.54, in particular (2.140), gives C2.53,2 = 3264 2, while C2.36,0,2 =
12. Substitution in the defining sum gives
                                    √
                      C3.27 = 4(3264 2)2 + 122 = 85229712 < 227 .
                                                                                                       □
Proposition 3.29 (Kernel derivative estimate for Gaussian domination). Let γ =
(k, u, a) ∈ Γ and let i ∈ [k). There exists a finite multiset P ⊂ Bdist (a1i , ∆γ )2 × [2)
with #P ≤ 6 and for every v ∈ R2 and j ∈ Z,
                                   X
  |(∂0 + ∂1 )(Hγ )i,j (v)| ≤ C3.29   (t0 (j)−1 + t1 (j)−1 )⟨(Wu v)0 ⟩2(t0 (j)) ⟨(Wu v)1 ⟩2(t1 (j)) ,
                                    (t0 ,t1 ,u)∈P
                                                                                                  (3.36)
where C3.29 = 4C2.53,2 C2.55,2 + 2C2.36,0,2 C2.36,1,2 .
Proof (). Let P be the multiset constructed in the proof of Proposition 3.27; it has
the required cardinality and distance properties. Fix j ∈ Z, and write s = (sγ )i,j and
H = (Hγ )i,j .
  The same scale comparisons used there, together with Propositions 2.53 and 2.55,
give
                                             X
   |(∂0 + ∂1 )(s ⊗ s)(v)| ≤ 4C2.53,2 C2.55,2   (t0 (j)−1 + t1 (j)−1 )⟨v0 ⟩2(t0 (j)) ⟨v1 ⟩2(t1 (j)) .
                                                    (t0 ,t1 ,0)∈P

By Proposition 2.36, scaling, and the chain rule,
                                               X
|(∂0 +∂1 )(Yγ )i,j (v)| ≤ 2C2.36,0,2 C2.36,1,2   (t0 (j)−1 +t1 (j)−1 )⟨(Wu v)0 ⟩2(t0 (j)) ⟨(Wu v)1 ⟩2(t1 (j)) .
                                               (t0 ,t1 ,u)∈P
                                        √
Here the factor 2 also covers the factor 2 arising when u = 1, since
                                       √
                   (∂0 + ∂1 )(W1 v)0 = 2,      (∂0 + ∂1 )(W1 v)1 = 0.
The claim follows from Definition 3.13.                                                                □
Lemma 3.30 (constant C3.29 ()).
                                                C3.29 < 230 .                                     (3.37)
Proof (). Lemmas 2.54 and 2.56, in particular (2.140) and (2.143), give
                                   √                       √
                     C2.53,2 = 3264 2,      C2.55,2 = 36864 2.
Also                                                                     √
                                C2.36,0,2 = 12,            C2.36,1,2 = 96 2.
                       NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                   51
         √
Using        2 < 3/2, the defining sum in Proposition 3.29 is smaller than
                       8 · 3264 · 36864 + 2 · 12 · 96 · 23 = 962596224 < 230 .
                                                                                                                     □
Proposition 3.31 (Gaussian domination, combined). Set
                         C3.31,0 = 36,           C3.31,1 = 2,           C3.31,2 = 2153 .                         (3.38)
 Let γ = (k, u, a) ∈ Γ and assume k ≤ n − 1. Let i ∈ [k). For every ι ∈ Iγ there exists
a finite set B = Bγ,i,ι with
                                    #B ≤ C3.31,0 ,                               (3.39)
                                                                         2
and, for every b ∈ B, an element ub ∈ [2), and, for every (b, m) ∈ B × N , a sequence
pair pb,m ∈ A2 , such that
                                    ∆(pb,m ) ≤ C3.31,1 (∆γ + |ι0 | + |m|)                                        (3.40)
and, for every j ∈ Z and v ∈ R2 ,
                                                       X                X
                      |(Nγ,ι )i,j (v)| ≤ C2−|ι0 |/2           2−|m|/2             Gpb,m (j),ub (v)               (3.41)
                                                       m∈N2             b∈B

holds with C = C3.31,2 . The nonnegative series on the right converges for every v ∈ R2
and has finite L1 norm.
  The proof of this proposition is split into three cases: Propositions 3.32, 3.33, and
3.34, below. Their common constant is verified in Lemma 3.35.
Proposition 3.32 (Gaussian domination, near case). The conclusion of Proposition
3.31 holds in the case ι = (h, 0), h > 0, with the constant in (3.41) equal to
   C3.32 = 28 πe2π C̃2.46,0,2 C2.68,2 C3.27 max C2.48, 3 , 3 + 4, 4C2.51,− 1 , 1 , 3 , 3 C2.48, 3 , 3 . (3.42)
                                                                                                     
                                                              2 2                        2 2 2 2         2 2
Proof.
    C = C3.32 = 28 πe2π C̃2.46,0,2 C2.68,2 C3.27 max(C2.48, 3 , 3 + 4, 4C2.51,− 1 , 1 , 3 , 3 C2.48, 3 , 3 ).
                                                                    2 2                        2 2 2 2         2 2
Let ι = (h, 0) ∈ Iγ with h > 0. Let ρ be the Schwartz function defined as

                                                 a1 (j+∆ )) − Φ(2h a1 (j+∆ ))
                                         Φ(2h−1
                                              \                  \            
                             ρ = F −1              i     γ                i          γ
                                                                              ν           .
                                                 s(2h a1i \
                                                          (· + ∆γ ), j)
Let λ = λ(j) = 2h a1i (j + ∆γ ). Note λ ∈ A by Proposition 2.31. We will omit the
argument j where clear from context. Moreover, letting F = (Nγ,ι )i,j and H = (Hγ )i,j ,
we have for v ∈ R2 ,              Z
                          F (v) =   ρ(p)H(v0 − p, v1 − p) dp.
                                             R
By Proposition 3.16, H has mean zero in the diagonal direction. Setting v0 = w0 − w1
                                 1
and v1 = w0 + w1 (then wm = 2− 2 (W1 v)m ) and changing variables in the integral and
subtracting zero gives
                        Z                    
                F (v) =     ρ(w0 + p) − ρ(w0 ) H(−w1 − p, w1 − p) dp.          (3.43)
                                R
52                           VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

By Proposition 2.68 and Proposition 2.46 (each applied with N = 2),
     |ρ(w0 + p) − ρ(w0 )| ≤ 2π C̃2.46,0,2 C2.68,2 min(1, λ−1 |p|)(⟨w0 + p⟩2(λ) + ⟨w0 ⟩2(λ) )                                       (3.44)
By Proposition 3.27 we obtain P ⊂ Bdist (a1i , ∆γ )2 × [2) with #P ≤ 6 such that for all
v ∈ R2 ,                          X
                   |H(v)| ≤ C3.27         ⟨(Wu v)0 ⟩2(t0 ) ⟨(Wu v)1 ⟩2(t1 ) ,
                                                        (t0 ,t1 ,u)∈P

where we omitted the argument j. Note that by Proposition 2.33, if t ∈ Bdist (a1i , ∆γ ),
then
                                    t
                                    λ
                                      ≤ 2−h .                                    (3.45)
                                                                                      1
In the following we will use the inequality min(1, a) ≤ a 2 , valid for all a ≥ 0. For every
p, w1 ∈ R we have
                               X                             X                 1
             min(1, λ−1 |p|) ≤    min(1, 12 λ−1 |p ± w1 |) ≤   (λ−1 |p ± w1 |) 2
                                                  ±                                         ±

and if t satisfies (3.45), then the right-hand side is
                                     h X                      1
                                ≤ 2− 2    (1 + t−1 |p ± w1 |) 2 .                                                                  (3.46)
                                                             ±

Altogether, the integrand in (3.43) is no greater than
       h X                   X                3             3                                           X            3                  
 C1 2− 2    ⟨w0 + αp⟩2(λ) 2         ⟨−w1 − p⟩(t2 0 ) ⟨w1 − p⟩(t2 1 ) +                                             ⟨p⟩(t2 0 ) ⟨w1 ⟩2(t1 ) ,
          α∈[2)                            (t0 ,t1 ,0)∈P                                           (t0 ,t1 ,1)∈P
                                                                                                                        h                     1
where we have used (3.46) for the terms with u = 0 and min(1, λ−1 |p|) ≤ 2− 2 (1+t−1 0 |p|)
                                                                                            2

for the terms with u = 1, and C1 = 2π C̃2.46,0,2 C2.68,2 C3.27 . Integrating over p ∈ R we
                                               h
obtain that |F (v)| is no greater than 2C1 2− 2 times
                               X                       Z   3
                                         2        2
                                    ⟨w0 ⟩(λ) ⟨w1 ⟩(t1 ) ⟨p⟩(t2 0 ) dp                 (3.47)
                                          (t0 ,t1 ,1)∈P                       R

                X            Z            3             3                     X                          Z                  3
+⟨w0 ⟩2(λ)                        ⟨w1 + p⟩(t0 ) ⟨w1 − p⟩(t2 1 ) dp +
                                          2
                                                                                           ⟨w1 ⟩2(t1 )               2      2
                                                                                                             ⟨w0 + p⟩(λ) ⟨p⟩(t0 ) dp
             (t0 ,t1 ,0)∈P    R                                            (t0 ,t1 ,1)∈P                 R

                                                                                                                                   (3.48)
                                     X            Z                        3               3
                             +                        ⟨w0 + p⟩2(λ) ⟨w1 + p⟩(t2 0 ) ⟨w1 − p⟩(t2 1 ) dp                              (3.49)
                                  (t0 ,t1 ,0)∈P   R

     By the two bump estimate, Proposition 2.48, we may bound (3.47) and (3.48) by
                                X            3             3
                                             2             2
                            C2     ⟨(W1 v)0 ⟩(λ) ⟨(W1 v)1 ⟩(r) ,
                                                      r∈M1

where M1 = {max(t    R 0 , t31 ) : (t0 , t1 , 0) ∈ P} ∪ {t1 : (t0 , t1 , 1) ∈ P} as multiset, and
C2 = 4(C2.48, 3 , 3 + R ⟨p⟩ 2 dp).
                  2 2
                             NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                     53

  To estimate (3.49) we first use Proposition 2.51 to obtain
                 3                  3                                      3                3              3         3
   ⟨w1 + p⟩(t2 0 ) ⟨w1 − p⟩(t2 1 ) ≤ C2.51,− 1 , 1 , 3 , 3 (⟨w1 ⟩(t2 0 ) ⟨w1 − p⟩(t2 1 ) + ⟨w1 + p⟩(t2 0 ) ⟨w1 ⟩(t2 1 ) ).
                                                       2 2 2 2

Together with Proposition 2.48 this allows us to bound (3.49) by
                     X                3       3                   3        3
                                      2
               C3          ⟨w0 + w1 ⟩(λ) ⟨w1 ⟩(t2 0 ) + ⟨w0 − w1 ⟩(λ)
                                                                  2
                                                                      ⟨w1 ⟩(t2 1 ) ,
                               (t0 ,t1 ,0)∈P

where C3 = C2.51,− 1 , 1 , 3 , 3 C2.48, 3 , 3 . By Proposition 2.50 the previous is no greater than
                              2 2 2 2           2 2

          X                 3            3         3        3                  3             3                  3             3
16C3                   ⟨v0 ⟩(t2 0 ) ⟨v1 ⟩(λ)
                                         2         2
                                             +⟨v0 ⟩(λ) ⟨v1 ⟩(t2 1 ) +⟨(W1 v)0 ⟩(λ)
                                                                               2
                                                                                   ⟨(W1 v)1 ⟩(t2 0 ) +⟨(W1 v)0 ⟩(λ)
                                                                                                                2
                                                                                                                    ⟨(W1 v)1 ⟩(t2 1 )
       (t0 ,t1 ,0)∈P

which we can write as
                                                      X                        3                3
                                     16C3                       ⟨(Wu v)0 ⟩(r2 0 ) ⟨(Wu v)1 ⟩(r2 1 )
                                               (r0 ,r1 ,u)∈M2

with M2 = {(t0 , λ, 0) : (t0 , t1 , 0) ∈ P} ∪ {(λ, t1 , 0) : (t0 , t1 , 0) ∈ P} ∪ {(λ, t0 , 1) :
(t0 , t1 , 0) ∈ P} ∪ {(λ, t1 , 1) : (t0 , t1 , 0) ∈ P} as a multiset. To summarize, we showed
that
                                           h X               3                    3
                       |F (v)| ≤ C4 2− 2                     2
                                                  ⟨(Wub v)0 ⟩(p b,0 )
                                                                      ⟨(Wub
                                                                            v)1 ⟩ 2
                                                                                 (pb,1 ) ,
                                                          b∈B
where B is a finite set in bijection with the multiset M1 ⊔ M2 and ub = 1, pb = (λ, r) ∈
A2 when b corresponds to r ∈ M1 , and ub = u, pb = (r0 , r1 ) when b corresponds to
(r0 , r1 , u) ∈ M2 , and C4 = 2C1 max(C2 , 16C3 ). Finally we use Gaussian domination,
Proposition 2.52, to estimate the right hand side of the previous display by
                            h X X     |m|
                 2
                      C4 2− 2       2− 2 g(2m0 pb,0 ) (Wub v)0 g(2m1 pb,1 ) (Wub v)1 .
                                                                                   
               8C2.52
                                        b∈B m∈N2

For b ∈ B and m ∈ N2 , set
                                                  pb,m = (2m0 pb,0 , 2m1 pb,1 ).
The explicit multisets M1 and M2 contain at most 6 and 24 elements, respectively, so
#B ≤ 30. Propositions 2.31 and 2.33 give
                                               ∆(pb,m ) ≤ 2(∆γ + h + |m|).
The series converges pointwise and in L1 by comparison with the product of two geo-
metric series.
                                                                                                                             □
Proposition 3.33 (Gaussian domination, far case). The conclusion of Proposition 3.31
holds in the case ι = (h, 0), h < 0, with the constant in (3.41) equal to
                             C3.33 = 3 · 27 e2π C̃2.46,0,3 C2.66,3 C3.29 C2.51,1,1,2,2 C2.48,2,2 .                       (3.50)
54                       VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof ().
                      C = C3.33 = 3 · 27 e2π C̃2.46,0,3 C2.66,3 C3.29 C2.51,1,1,2,2 C2.48,2,2
Let ι = (h, 0) ∈ Iγ with h < 0, and let
                                                                                            !
                                                     1 (j−∆ −1)) − Φ(2h+1\
                                               Φ(2h a\                   a1i (j−∆γ −1))
                            ρ = F −1                 i     γ
                                                                                 ν              .
                                                         s(2h a1i \
                                                                  (· − ∆γ ), j)
Set λ(j) = 2h+1 a1i (j − ∆γ − 1). Then λ ∈ A by Proposition 2.31. As before, write
F = (Nγ,ι )i,j and H = (Hγ )i,j , so that
                                     Z
                          F (v) =       ρ(p)H(v0 − p, v1 − p) dp.
                                                     R
     By Propositions 2.66 and 2.46, applied with N = 3,
             |ρ(p)| ≤ C̃2.46,0,3 C2.66,3 ⟨p⟩3(λ/2) + ⟨p⟩3(λ) ≤ 3C̃2.46,0,3 C2.66,3 ⟨p⟩3(λ) .
                                                            
                                                                                                             R
The multiplier defining ρ vanishes in a neighborhood of the origin, hence                                     R
                                                                                                                  ρ = 0.
Consequently,           Z              p
                                               ρ(q) dq ≤ 32 C̃2.46,0,3 C2.66,3 λ⟨p⟩2(λ) .
                                       −∞
Integration by parts gives
                        Z Z p        
                F (v) =        ρ(q) dq (∂0 + ∂1 )H(v0 − p, v1 − p) dp.
                                   R        −∞
   Let P be the multiset from Proposition 3.29, and omit the argument j from the scales.
Setting v0 = w0 − w1 and v1 = w0 + w1 , Propositions 2.51, 2.48, and 2.50 bound, for
(t0 , t1 , 0) ∈ P,          Z
                                               ⟨p⟩2(λ) ⟨v0 − p⟩2(t0 ) ⟨v1 − p⟩2(t1 ) dp
                                           R
by
                                                                                                                                
9C2.51,1,1,2,2 C2.48,2,2 ⟨v0 ⟩2(t0 ) ⟨v1 ⟩2(max(λ,t1 )) +⟨v0 ⟩2(λ) ⟨v1 ⟩2(max(t0 ,t1 )) +⟨(W1 v)0 ⟩2(λ) ⟨(W1 v)1 ⟩2(max(t0 ,t1 )) .
For (t0 , t1 , 1) ∈ P, the corresponding integral is bounded by
                                  4C2.48,2,2 ⟨(W1 v)0 ⟩2(max(λ,t0 )) ⟨(W1 v)1 ⟩2(t1 ) .
     If t ∈ Bdist (a1i , ∆γ ), then
                                                            λ
                                                            t
                                                              ≤ 2h .
Thus
                                        λ(t−1        −1
                                            0 + t1 ) ≤ 2
                                                                h+1
                                                                    .
Let B index the bracket products displayed above, after collecting repetitions, and let
ub and pb denote their orientations and sequence pairs. Using the explicit multiset P
constructed in the proof of Proposition 3.27, we have #B ≤ 30. We obtain
                                                                    X
  |F (v)| ≤ 27C̃2.46,0,3 C2.66,3 C3.29 C2.51,1,1,2,2 C2.48,2,2 2h/2   ⟨(Wub v)0 ⟩2(pb,0 ) ⟨(Wub v)1 ⟩2(pb,1 ) .
                                                                              b∈B
                         NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                    55

   For m ∈ N2 , set
                                            pb,m = (2m0 pb,0 , 2m1 pb,1 ).
Propositions 2.31 and 2.33 give
                                         ∆(pb,m ) ≤ 2(∆γ + |h| + |m|).
Finally, Proposition 2.52, applied with N = 2 to both factors, gives
                                      |h| X    |m| X
                    |F (v)| ≤ C3.33 2− 2    2− 2     Gpb,m (j),ub (v).
                                                       m∈N2            b∈B
                                                                  1
The series converges pointwise and has finite L norm by comparison with the product
of two geometric series.
                                                                                                                        □
Proposition 3.34 (Gaussian domination, intermediate case). The conclusion of Propo-
sition 3.31 holds in the case ι = (0, l), |l| ≤ ∆γ , with the constant in (3.41) equal to
                           C3.34 = 27 e2π C̃2.46,0,2 C2.66,2 C3.27 C2.51,1,1,2,2 C2.48,2,2 .                      (3.51)
Proof ().
                  C = C3.34 = 27 e2π C̃2.46,0,2 C2.66,2 C3.27 C2.51,1,1,2,2 C2.48,2,2
Let ι = (0, l) ∈ Iγ with |l| ≤ ∆γ , and let
                                                                       !
                                       Φ   \1
                                          (ai (j+l−1)) − Φ  \ 1
                                                            (ai (j+l))
                            ρ = F −1                           ν        .
                                                  1\
                                              s(ai (· + l), j)
Set
                      λ− (j) = a1i (j + l − 1),        λ+ (j) = a1i (j + l).
Then λ− , λ+ ∈ A by Proposition 2.31. Writing F = (Nγ,ι )i,j and H = (Hγ )i,j , we have
                                     Z
                            F (v) =     ρ(p)H(v0 − p, v1 − p) dp.
                                                 R
By Propositions 2.66 and 2.46, applied with N = 2,
                                |ρ(p)| ≤ C̃2.46,0,2 C2.66,2 ⟨p⟩2(λ− ) + ⟨p⟩2(λ+ ) .
                                                                                 

  Let P be the multiset from Proposition 3.27, and omit the argument j from the
scales. Set v0 = w0 − w1 and v1 = w0 + w1 . For each λ ∈ {λ− , λ+ } and (t0 , t1 , 0) ∈ P,
Propositions 2.51, 2.48, and 2.50 bound
                            Z
                              ⟨p⟩2(λ) ⟨v0 − p⟩2(t0 ) ⟨v1 − p⟩2(t1 ) dp
                                        R
by
                                                                                                                                
9C2.51,1,1,2,2 C2.48,2,2 ⟨v0 ⟩2(t0 ) ⟨v1 ⟩2(max(λ,t1 )) +⟨v0 ⟩2(λ) ⟨v1 ⟩2(max(t0 ,t1 )) +⟨(W1 v)0 ⟩2(λ) ⟨(W1 v)1 ⟩2(max(t0 ,t1 )) .
For (t0 , t1 , 1) ∈ P, the corresponding integral is bounded by
                                  4C2.48,2,2 ⟨(W1 v)0 ⟩2(max(λ,t0 )) ⟨(W1 v)1 ⟩2(t1 ) .
56                      VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

   Let B index the resulting bracket products after collecting repetitions, and let ub and
pb denote their orientations and sequence pairs. From the explicit form of P in the proof
of Proposition 3.27, the resulting multiset has at most 36 elements. Hence
                                                   #B ≤ 36.
We obtain
                                                                       X
       |F (v)| ≤ 9C̃2.46,0,2 C2.66,2 C3.27 C2.51,1,1,2,2 C2.48,2,2      ⟨(Wub v)0 ⟩2(pb,0 ) ⟨(Wub v)1 ⟩2(pb,1 ) .
                                                                       b∈B
                 2
     For m ∈ N , set
                               pb,m = (2m0 pb,0 , 2m1 pb,1 ).
Propositions 2.31 and 2.33, together with |l| ≤ ∆γ , give
                                          ∆(pb,m ) ≤ 2(∆γ + |m|).
Finally, Proposition 2.52, applied with N = 2 to both factors, gives
                                       X − |m| X
                       |F (v)| ≤ C3.34    2 2      Gpb,m (j),ub (v).
                                                m∈N2           b∈B
                                                              1
The series converges pointwise and has finite L norm by comparison with the product
of two geometric series.
                                                                                                                    □
Lemma 3.35 (constant C3.31,2 ()). We have
                                                 C3.32 < 2117 ,                                                (3.52)
                                                             153
                                                 C3.33 < 2         ,                                           (3.53)
and
                                                 C3.34 < 2110 .                                                (3.54)
In particular,                                     
                          max C3.32 , C3.33 , C3.34 ≤ C3.31,2 .                                                (3.55)
Thus Proposition 3.31 holds with the claimed constant in (3.41).
Proof (). We have
                                                e2.46,0,2 = 218 ,
                                                C                                                              (3.56)
and
                                                e2.46,0,3 = 233 .
                                                C                                                              (3.57)
Lemmas 2.67 and 2.69 give
                                     C2.66,2 < 637436354528 < 35 240 ,                                         (3.58)
                               C2.66,3 < 6136564156458101504 < 11
                                                               16
                                                                  263 ,                                        (3.59)
and
                         C2.68,2 < 20397963318112 < 35 245 .                                                   (3.60)
Lemmas 3.28 and 3.30 give
                                            41 27
                                    C3.27 < 64 2 ,                                                             (3.61)
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                         57

and
                                               C3.29 < 29
                                                       32
                                                          230 .                                     (3.62)
Furthermore,                                              √
                                         C2.48, 3 , 3 = 12 2 < 17,                                  (3.63)
                                               2 2
and
                                     C2.48,2,2 = 16.                           (3.64)
By Proposition 2.51, the bump triangle constants in Propositions 3.32, 3.33, and 3.34
are respectively 1, 4, 4. Thus the maximum in (3.42) is smaller than 68. Since π < 4
and e2π < 3025, substitution gives
                     C3.32 < 2 · 27 · 4 · 3025 · 218 · 35 245 · 41
                                                                64
                                                                   227 · 17
                                                                         32
                                                                            27 < 2117 ,
                    C3.33 < 43 22 · 27 · 16
                                         13 13
                                            2 · 233 · 11
                                                      16
                                                         263 · 29
                                                               32
                                                                  230 · 22 · 24 < 2153 ,
and
                       C3.34 < 27 · 13
                                    16
                                       213 · 218 · 35 240 · 41
                                                            64
                                                               227 · 22 · 24 < 2110 .
                                                                                                          □
3.4. Main induction.
Definition 3.36 (induct positive terms). Let k ∈ N with 1 ≤ k ≤ n and C ∈ [1, ∞).
We say that InductPositiveTerms(k, C) holds if
 for all γ = (k, u, a) ∈ Γ, i ∈ [k),
                                                                       k−n+1
                                ∥M(γ, sγ ⊗ sγ , i)∥M(k) ≤ C∆2−2
                                                            γ                   .                   (3.65)
Definition 3.37 (vanishing diagonal). Let k ∈ N with 1 ≤ k ≤ n and C ∈ [1, ∞). We
say that VanishingDiagonal(k, C) holds if
  for all γ = (k, u, a) ∈ Γ, i ∈ [k),
                                                                    k−n+1
                                   ∥M(γ, Hγ , i)∥M(k) ≤ C∆2−2
                                                          γ                 .                       (3.66)
Definition 3.38 (diagonal band). Let k ∈ N with 1 ≤ k ≤ n − 1 and C ∈ [1, ∞). We
say that DiagonalBand(k, C) holds if
  for all γ = (k, u, a) ∈ Γ, i ∈ [k),
                                                           k−n+1
                          X
                               ∥M(γ, Lγ,ι , i)∥M(k) ≤ C∆2−2
                                                        γ        .         (3.67)
                                ι∈Iγ

Definition 3.39 (increase data). Let k ∈ N with 1 ≤ k ≤ n − 1 and C ∈ [1, ∞). We
say that IncreaseData(k, C) holds if
  the following holds.
  Let γ = (k, u, a) ∈ Γ, let i ∈ [k), and let ι ∈ Iγ . For j ∈ Z and y ∈ (R2 )k+1 define
                     Y                                        k−1
                                                                 Y                   
                                                                                       ⊗2
                                                                                               
   (Mi,ι )j (y) =             (Gγ )m,j (ym ) |(Nγ,ι )i,j (yi )|      (Gγ )m,j−1 (ym ) σγ,ι,i,j   (yk ).
                      m∈[i)                                    m=i+1
                                                                                                    (3.68)
58                      VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Then Mi,ι ∈ M(k + 1) and
                                                    |ι0 |                   k−n+2
                            ∥Mi,ι ∥M(k+1) ≤ C2− 2 (1 + |ι0 |)2 ∆2−2
                                                                γ                   .                   (3.69)
     We will prove that for 1 ≤ k ≤ n − 1 the following implications hold:
       InductPositiveTerms(k + 1) =⇒ IncreaseData(k) =⇒ DiagonalBand(k)                                 (3.70)
                =⇒ VanishingDiagonal(k) =⇒ InductPositiveTerms(k)              (3.71)
(Here we have omitted the explicit constants for clarity.) The last implication also
holds for k = n. After observing that VanishingDiagonal(n) holds, Theorem 3.48 below
follows by induction on k.
Proposition 3.40. Let k ∈ N with 1 ≤ k ≤ n and C ∈ [1, ∞). If VanishingDiagonal(k, C)
holds, then InductPositiveTerms(k, kC + 2) holds.
Proof. Fix γ. Let C ′ = kC + 2. By positivity, Proposition 3.9, it suffices to prove
                                                            k−n+1
                         X
                       ∥   M(γ, sγ ⊗ sγ , i)∥M(k) ≤ C ′ ∆2−2
                                                         γ        .                (3.72)
                              i∈[k)

Adding and subtracting M(γ, Yγ , i) and using the triangle inequality, the left-hand side
is                  X                          X
                 ≤     ∥M(γ, Hγ , i)∥M(k) +         M(γ, Yγ , i)    ,
                                                                                 M(k)
                           i∈[k)                            i∈[k)
                                                                                            k−n+1
which by VanishingDiagonal(k, C) and Proposition 3.8 is ≤ (kC + 2)∆2−2
                                                                   γ                                .       □
Proposition 3.41. Let k ∈ N with 1 ≤ k ≤ n−1 and C ∈ [1, ∞). If DiagonalBand(k, C)
holds, then VanishingDiagonal(k, C) holds.
Proof. By Proposition 3.22,
                                                            X
                         ∥M(γ, Hγ , i)∥M(k) ≤ sup               ∥M(γ, Lγ,ι , i)∥M(k) ,
                                                 N ∈N
                                                         ι∈Iγ
                                                        |ι|≤N
                                                                                                        1
                                                                            P
where we used Lemma 3.24, Lemma 3.23 and that Hγ =                              ι∈Iγ Lγ,ι converges in L .
The claim follows from DiagonalBand(k, C).                                                                  □
Proposition 3.42 (vanishing kernel integral). Let γ = (n, w, a) ∈ Γ. For every i ∈ [n),
                                          ∥M(γ, Hγ , i)∥M(n) = 0.                                       (3.73)
In particular, VanishingDiagonal(n, 1) holds.
Proof. The claim follows by Proposition 2.19 if we can verify the assumption (2.56).
Using the formula for Kn in Proposition 2.24, for z ∈ Rn+1 ,
                          Z
                             Kn ((M(γ, Hγ , i))j )(z + qen ) dq               (3.74)
                                      R
         Z Z
     =              M ((zl + pl , pl )l∈[n−1) , zn−1 + zn + q − Σ(p), zn + q − Σ(p)) dp dq,             (3.75)
         R   Rn−1
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                            59

where we abbreviated M = (M(γ, Hγ , i))j . By Fubini’s theorem, changing variables
q 7→ q − zn + Σ(p) and renaming q to pn−1 , this is equal to
                             Z
                                 M ((zl + pl , pl )l∈[n) ) dp.              (3.76)
                                        Rn
We claim that this integral vanishes. This follows by unpacking the definition of M ,
separating the ith integral and observing by Proposition 3.16 that
                              Z
                                (Hγ )i,j (zi + pi , pi ) dpi = 0.              (3.77)
                                        R
                                                                                                          □
Proposition 3.43. Let k ∈ N with 1 ≤ k ≤ n − 1 and C ∈ [1, ∞). Suppose that
IncreaseData(k, C) holds. Then:
  (i) If k < n − 1, then
                                                                 1/2
                                   DiagonalBand(k, 215 C3.31,2 C 1/2 )                                (3.78)
holds.
  (ii) If k = n − 1, then DiagonalBand(n − 1, 210 C) holds.
Proof. Fix γ, i, ι. By definition,
                                                                    ∗ν
                                    (Lγ,ι )i,j = (Nγ,ι )i,j ∗(1,1) σγ,ι,i,j .
Let
                         Y                                       k−1
                                                                    Y                   
             ρj (y) =             (Gγ )m,j (ym ) (Nγ,ι )i,j (yi )       (Gγ )m,j−1 (ym ) .
                          m∈[i)                                        m=i+1
                                    1
The Gaussian factors have L norm one. Proposition 3.31 therefore gives
                                             X
                    ∥ρj ∥1 ≤ C3.31,2 C3.31,0   2−|m|/2 ≤ 29 C3.31,2 .
                                                      m∈N2

  If k < n − 1, Proposition 2.27 gives
                                    
                 X                                 1/2
            Λk      M(γ, Lγ,ι , i)j  (F) ≤ 29/2 C3.31,2 J 1/2 |Λk+1 (M
                                                                       fι )(F)|1/2 .
                  j∈[J)

If k = n − 1, Proposition 2.28 gives
                                             
                          X
                  Λn−1       M(γ, Lγ,ι , i)j  (F) ≤ sup |Λn (M
                                                               fι )(F)|.
                                                                    e
                             j∈[J)                                     F∈F
                                                                       e

Here in either case                                  X
                                             M
                                             fι =         (Mi,ι )j
                                                     j∈[J)

with Mi,ι as in Definition 3.39. Hence IncreaseData(k, C) gives
                                                       k−n+2                              k−n+2
                   fι )(F)| ≤ C max(1, J 1−2
            |Λk+1 (M                                           )2−|ι0 |/2 (1 + |ι0 |)2 ∆2−2
                                                                                        γ         .
60                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

It follows in the case k < n − 1 that
                             
                                                              k−n+1 −|ι |/4           k−n+1
          X                                 1/2
    Λk       M(γ, Lγ,ι , i)j  (F) ≤ 29/2 C3.31,2 C 1/2 J 1−2     2 0 (1 + |ι0 |)∆1−2
                                                                                   γ        ,
         j∈[J)

and in the case k = n − 1 that
                                           
                        X
                 Λn−1      M(γ, Lγ,ι , i)j  (F) ≤ C2−|ι0 |/2 (1 + |ι0 |)2 .
                                  j∈[J)

There are 2∆γ + 1 ≤ 3∆γ indices with ι0 = 0. Moreover,
                       ∞
                       X                                                     ∞
                                                                             X
                 3+2         2−h/4 (1 + h) ≤ 210 ,                3+2              2−h/2 (1 + h)2 ≤ 210 .
                       h=1                                                   h=1
                                              9/2 10         15
Summing in ι proves (i), since 2                   2     ≤ 2 , and proves (ii).                                 □
Proposition 3.44. Let k ∈ N with 1 ≤ k ≤ n − 1 and C ∈ [1, ∞). Assume that
InductPositiveTerms(k + 1, C) holds. Then IncreaseData(k, C · C3.44 ) holds, where
                                   C3.44 = 210 C3.31,0 (1 + C3.31,1 )2 C3.31,2 .                            (3.79)
Proof. Estimating the functions |Nγ,ι | by Gaussian domination using Propositions 3.31,
Proposition 2.23 and applying the dominated convergence theorem,
                                      X         X
    ∥Mi,ι ∥M(k+1) ≤ C3.31,2 2−|ι0 |/2   2−|m|/2     ∥M(eγb,m , s⊗2
                                                                eb,m , k)∥M(k+1) ,
                                                                γ                  (3.80)
                                                  m∈N2            b∈Bi,γ,ι

and for each (b, m) ∈ B × N2 the new data γ
                                          eb,m is (k + 1, u    ab,m ) ∈ Γ where
                                                          eb , e
                                           eb (i′ ) = u(i′ )
                                           u                         (i′ ∈ [i)),
                                                         u
                                                         eb (i) = ub ,
                                          eb (i ) = u(i′ )
                                          u   ′
                                                                   (i < i′ < k),
                                                         u
                                                         eb (k) = 0,
and
                                            (e
                                             ab,m )i′ = ai′          (i′ ∈ [i)),
                                                       (e
                                                        ab,m )i = pb,m ,
                                    ab,m )i′ = ai′ (· − 1)
                                   (e                                    (i < i′ < k),
                                                       (e
                                                        ab,m )k = αι,i .
Here ub ∈ [2), pb,m ∈ A is produced by Proposition 3.31 and αι,i ∈ A2 can be inferred.
                              2

To be explicit, α(h,0),i (j) = (2h−1/2 a1i (j + ∆γ ), 2h−1/2 a1i (j + ∆γ )) if h > 0, α(h,0),i (j) =
(2h−1/2 a1i (j−∆γ ), 2h−1/2 a1i (j−∆γ )) if h < 0 and α(0,l),i (j) = (2−1/2 a1i (j+l), 2−1/2 a1i (j+l))
if |l| ≤ ∆γ . In particular, ∆(αι,i ) = 0 and
              ∆γeb,m = ∆γ − ∆(ai ) + ∆(pb,m ) ≤ (1 + C3.31,1 )(∆γ + |ι0 | + |m|).
                        NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                         61

Also note (sγeb,m )k,j = σγ,ι,i,j . We may apply InductPositiveTerms(k + 1, C) and sum
over b ∈ Bi,γ,ι to obtain for each ι ∈ Iγ :
                                                     |ι0 | X   |m|                     k−n+2
 ∥Mi,ι ∥M(k+1) ≤ C C3.31,0 (1 + C3.31,1 )2 C3.31,2 2− 2      2− 2 (∆γ + |ι0 | + |m|)2−2      .
                                                                  m∈N2

Summing over m we obtain the claim. Indeed, estimate
X − |m|                  k−n+2       k−n+2
                                                             X − |m|
                                                    2−2k−n+2                k−n+2
   2 2 (∆γ +|ι0 |+|m|)2−2      ≤ ∆2−2
                                  γ        (1+|ι0 |)          2 2 (1+|m|)2−2
m∈N2                                                                         m∈N2

                                    k−n+2
                                                           X        |m|
                            ≤ ∆2−2
                               γ            (1 + |ι0 |)2          2− 2 (1 + |m|)2
                                                           m∈N2
                 |m|
                − 2
                       (1 + |m|)2 ≤ 210 .
       P
and        m∈N2 2                                                                           □
Lemma 3.45 (constant C3.44 ()).
                                               C3.44 < 2172 .                          (3.81)
Proof (). Using the defining product in Proposition 3.44 and Proposition 3.31, in par-
ticular (3.38), we obtain
                                210 · 36 · 9 · 2153 = 324 · 2163 < 2172 .
                                                                                            □
Proposition 3.46. For every k ∈ N with 1 ≤ k ≤ n, InductPositiveTerms(k, Ck ) holds,
where
                                  Cn = 2 + n,                                 (3.82)
                                             10
                          Cn−1 = 2 + (n − 1)2 C3.44 Cn ,                      (3.83)
and, for 1 ≤ k ≤ n − 2,
                                                     1/2
                                Ck = 2 + k215 C3.31,2 (C3.44 Ck+1 )1/2 .               (3.84)
Proof. This is proved by (reverse) induction on k with the base case being k = n.
The claim holds for k = n by Proposition 3.40 with k = n and Proposition 3.42.
Next assume 1 ≤ k ≤ n − 1 and assume that InductPositiveTerms(k + 1, Ck+1 ) holds.
Then InductPositiveTerms(k, Ck ) follows by applying Proposition 3.44, Proposition
3.43, Proposition 3.41 and finally Proposition 3.40.                             □
Lemma 3.47 (constant Ck ()). For every k ∈ N with 1 ≤ k ≤ n − 1,
                         InductPositiveTerms(k, (18 · 2173 (k + 2) + 21/2 )2 )         (3.85)
holds.
Proof (). Let Ck be the constant from Proposition 3.46. It suffices to prove
                                                        2
                           Ck ≤ 18 · 2173 (k + 2) + 21/2 .                             (3.86)
We argue by reverse induction. For k = n − 1, Proposition 3.46 and Cn = n + 2 give
                                Cn−1 = 2 + (n − 1)(n + 2)210 C3.44 ,
62                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

which is bounded by the right-hand side of (3.86).
  Assume 1 ≤ k ≤ n − 2 and that (3.86) holds with k + 1 in place of k. Since
                                215 (C3.31,2 C3.44 )1/2 = 18 · 2173 ,
Proposition 3.46 gives
                        Ck ≤ 2 + k · 18 · 2173 18 · 2173 (k + 3) + 21/2 .
                                                                       

This is bounded by the right-hand side of (3.86), which proves the claim.             □
Remark 3.4. We only need to use the previous proposition for k = 2. The result then
holds with a constant independent of n.
Theorem 3.48. InductPositiveTerms(2, C3.48 ) holds, where
                                                           2
                     C3.48 = 217 (C3.31,2 C3.44 )1/2 + 21/2 .                     (3.87)
Proof. This follows from Proposition 3.47 if n ≥ 3 and from Proposition 3.46 if n =
2.                                                                                □
Lemma 3.49 (constant C3.48 ()).
                                          C3.48 < 2359 .                          (3.88)
Proof (). Since
                                     C3.44 = 324 · 2163
and C3.31,2 = 2153 , the first summand in (3.87) is
                                             18 · 2175 .
Its square is 324 · 2350 . The remaining two terms in the expanded square are smaller
than 2182 . Therefore
                                      C3.48 < 2359 .
                                                                                   □

                        4. Reduction to the main argument
     In this section we prove Theorem 1.4 from Theorem 3.48.
4.1. Further preliminaries for the reduction.
4.1.1. A to Λ1 .
Lemma 4.1 (A to Λ1 ). Let ϕ ∈ S(R). Let f = (f0 , . . . , fn−1 ) be functions in S(Rn ).
Then
                               ∥A(ϕ, f )∥22 = Λ1 (ϕ⊗2 )(F),                        (4.1)
                                 n
where for every i ∈ [n) and x ∈ R ,
                            Fi (x) = fi (−x[1,i+1) , Σ(x), −x[i+1,n) ).            (4.2)
Moreover, Fi ∈ S(Rn ) and
                                         ∥Fi ∥p = ∥fi ∥p                           (4.3)
for every p ∈ [1, ∞].
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                             63

Proof. The linear map in the definition of Fi has determinant of modulus one. Hence
Fi ∈ S(Rn ) and ∥Fi ∥p = ∥fi ∥p for every p ∈ [1, ∞].
  Expanding the L2 norm and the square inside the L2 integral, the left hand side
equals              Z Z          Y                     
                                         fi (u + yh ei ) (ϕ⊗2 )(y) dy du.
                           Rn     R2    (i,h)∈[n)×[2)

Changing variables u = −x, this becomes
                  Z Z        Y                     
                                    fi (−x + yh ei ) (ϕ⊗2 )(y) dy dx.
                           Rn   R2     (i,h)∈[n)×[2)

Now change variables yh 7→ yh + Σ(x) for h ∈ [2). We obtain
    Z Z         Y                               
                         fi (−x + (yh + Σ(x))ei ) ϕ(y0 + Σ(x))ϕ(y1 + Σ(x)) dy dx.
       Rn   R2    (i,h)∈[n)×[2)

By the definition of Fi , for every i ∈ [n) and h ∈ [2),
                                                                
     Fi (yh , x[n)\i ) = fi −x[0,i) , yh + Σ(x) − xi , −x[i+1,n) = fi (−x + (yh + Σ(x))ei ).
Hence the last display is equal to
            Z Z                                                        Y
                    (ϕ⊗2 )(y1 + Σ(x), y0 + Σ(x))                                   Fi (yh , x[n)\i ) dx dy,
                 R2   Rn                                            h∈[2), i∈[n)

which is Λ1 (ϕ⊗2 )(F).                                                                                        □

4.1.2. Variation seminorms. Let B be a seminormed space, I ⊂ R a subset and a : I →
B and J ∈ N, r ≥ 1. The r-variation seminorm (with at most J jumps) is
                                              X                        1/r
                                                                      r
          ∥a∥Vr,J (I;B) = sup      sup             ∥a(tj+1 ) − a(tj )∥       . (4.4)
                                0≤M ≤J           t0 <···<tM ,
                                           tj ∈I for all j∈[M +1)     j∈[M )

  Also define
                                        ∥a∥Vr (I;B) = sup ∥a∥Vr,J (I;B) .
                                                          J≥1

   In particular, when I is omitted we understand that it equals N≥1 , the set of positive
integers:
Definition 4.2 (r-variation seminorms for sequences on the positive integers). Define
                                            X                         1/r
                                                                     r
           ∥a∥Vr (B) = sup        sup             ∥a(tj+1 ) − a(tj )∥       .
                                J∈N          t0 <···<tJ ,
                                       tj ∈N≥1 for all j∈[J+1)      j∈[J)

Note we will only use this for r ≥ 1.
  The k-th short variation can be expressed as ∥a∥Vr,J ([2k ,2k+1 ];B) and long variations as
∥a∥Vr,J (2Z ;B) . For more on variation (semi)norms see [15].
64                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Lemma 4.3. For every increasing sequence of positive real numbers (tj )j∈[J+1) ,
   X                       1/r   X                         1/r
                          r               r
       ∥a(tj+1 ) − a(tj )∥       ≤2   ∥a∥Vr,J ([2k ,2k+1 ];B)      + ∥a∥Vr,J (2Z ;B) ,                       (4.5)
       j∈[J)                                         k∈κ

where κ is the set of k ∈ Z such that 2k ≤ tj < 2k+1 for some j ∈ [J + 1). Consequently,
                                   X                           1/r
              ∥a∥Vr,J ((0,∞);B) ≤ 2    ∥a∥rVr,J ([2k ,2k+1 ];B)      + ∥a∥Vr,J (2Z ;B) . (4.6)
                                              k∈Z

Proof (). Group the points tj according to the dyadic intervals [2k , 2k+1 ). The jumps
whose two endpoints lie in the same interval are kept unchanged. If a jump goes from
the last point in [2k , 2k+1 ) to the first point in a later occupied interval [2l , 2l+1 ), write
it as the sum of
                     a(tj+1 ) − a(2l ),             a(2l ) − a(2k ),             a(2k ) − a(tj ).
The internal jumps in an occupied interval, together with the first of these boundary
terms when it occurs, form an increasing sequence in [2k , 2k+1 ] with at most J jumps.
Their combined ℓr norm, summed over the occupied intervals, is therefore at most
                             X                            1/r
                                  ∥a∥rVr,J ([2k ,2k+1 ];B)      .
                                           k∈κ

The third boundary terms are bounded by the same expression. The middle terms use
the lower endpoints 2k , and hence form an increasing sequence on 2Z after repeated
endpoints are deleted, so their ℓr norm is at most ∥a∥Vr,J (2Z ;B) . Minkowski’s inequality
gives the first estimate. Taking the supremum over the sequence (tj ) gives the second.
                                                                                         □
Lemma 4.4. Let 0 < α < β and a : [α, β] → R be continuously differentiable. Then
                          ∥a∥V2,J ([α,β];R) ≤ ( β−α
                                                 α
                                                    )1/2 ∥ta′ (t)∥ 2                        dt ,             (4.7)
                                                                              L (t∈[α,β],     )
                                                                                            t
                                                                        ′
                      ∥a∥2V2,J ([α,β];R) ≤ 8∥a∥ 2                 dt ∥ta (t)∥ 2         dt .                 (4.8)
                                                      L ([α,β],     )        L (t∈[α,β], )
                                                                  t                      t

Proof (). Let α ≤ t0 < · · · < tJ ≤ β. For every j ∈ [J), the fundamental theorem of
calculus and Cauchy–Schwarz with respect to Lebesgue measure give
                                                       Z tj+1
                                       2
                    |a(tj+1 ) − a(tj )| ≤ (tj+1 − tj )        |a′ (t)|2 dt
                                                                         tj
                                                     Z tj+1
                                          ≤ β−α
                                             α
                                                              |ta′ (t)|2 dtt .
                                                      tj
Summing in j and taking the supremum proves (4.7).
  For (4.8), first let b be a nonnegative absolutely continuous function. Then
                                |b(tj+1 ) − b(tj )|2 ≤ |b(tj+1 )2 − b(tj )2 |
                    Z tj+1
               ≤2            |b(t)||tb′ (t)| dtt ≤ 2∥b∥L2 ([tj ,tj+1 ],dt/t) ∥tb′ ∥L2 ([tj ,tj+1 ],dt/t) .
                     tj
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                     65

Summing and applying Cauchy–Schwarz in j gives
                       ∥b∥2V2,J ([α,β];R) ≤ 2∥b∥L2 ([α,β],dt/t) ∥tb′ ∥L2 ([α,β],dt/t) .
Apply this to a+ = max(a, 0) and a− = − min(a, 0). Their derivatives have modulus
at most |a′ | almost everywhere. The triangle inequality for the variation seminorm
therefore gives
                                                     1/2                  1/2
                     ∥a∥V2,J ([α,β];R) ≤ 23/2 ∥a∥L2 ([α,β],dt/t) ∥ta′ ∥L2 ([α,β],dt/t) .
Squaring proves (4.8).                                                                              □

4.1.3. Bump functions.
                                                               d
Lemma 4.5. For a Schwartz function ϕ : R → C let T ϕ(x) = dx     (xϕ(x))|x . Then for
every m ≥ 0,
                 (Tcϕ)(m) (ξ) = −(m(ϕ)
                                    b (m) (ξ) + ξ(ϕ)
                                                  b (m+1) (ξ)).                 (4.9)
Proof. We proceed by induction on m. For m = 0 this follows from the rule for taking
the Fourier transform of a derivative and vice versa: Tcϕ(ξ) = 2πiξ Φ(ξ),
                                                                    b     where Φ(x) =
                          −1 d b
xϕ(x) and Φ(ξ) = −(2πi) dξ ϕ(ξ). Suppose the claim holds for m. Then by inductive
           b
hypothesis and the product rule,
                     (Tcϕ)(m+1) (ξ) = dξ
                                      d       b (m) (ξ) + ξ(ϕ)
                                         (−(m(ϕ)            b (m+1) (ξ)))

                                       b (m+1) (ξ) + ξ(ϕ)
                           = −((m + 1)(ϕ)              b (m+2) (ξ)).
                                                                                                    □
Lemma 4.6. Let k ≤ 2, t ∈ [21−k , 22−k ]. Then for every u ∈ R and N ≥ 0,
                                   ⟨u − t⟩N ≤ C4.6,N 2−kN ⟨u⟩N ,                            (4.10)
where C4.6,N = 23N .
Proof. The triangle inequality gives
                       1 + |u| ≤ 1 + |u − t| + t ≤ (1 + |u − t|)(1 + t).
Since k ≤ 2 and t ≤ 22−k ,
                                              1 + t ≤ 23−k .
Taking reciprocal N th powers proves the claim.                                                     □
Lemma 4.7. Let k ≤ −1. Then for every v ∈ R2 ,
      Z 2
  k/2
          ⟨v0 − t2−k ⟩2 ⟨v1 − t2−k ⟩2 dt ≤ C4.7 ⟨v0 ⟩3/2 ⟨v1 ⟩3/2 + ⟨v0 + v1 ⟩3/2 ⟨v0 − v1 ⟩3/2 ,
                                                                                               
 2
        1
                                                                                            (4.11)
where
                                               C4.7 = 133.                                  (4.12)
66                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof (). Put R = 2−k . We distinguish three cases. Suppose first that |v0 |, |v1 | ≥ 3R.
For t ∈ [1, 2] and i ∈ [2),
                             1 + |vi | ≤ 3(1 + |vi − tR|).
               −k 1−k
Since tR ∈ [2 , 2 ], Lemma 4.6, applied with k + 1 and N = 1/2, gives
                                         R−1/2 ⟨v0 − tR⟩1/2 ≤ 2⟨v0 ⟩1/2 .
Consequently the integrand, including the factor R−1/2 , is at most
                                 2 · 33/2 · 9⟨v0 ⟩2 ⟨v1 ⟩2 < 94⟨v0 ⟩3/2 ⟨v1 ⟩3/2 .
Integration over t ∈ [1, 2] proves the required bound in this case.
  Suppose next that exactly one of |v0 |, |v1 | is smaller than 3R; by symmetry, assume
that |v0 | < 3R. As above,
                                   ⟨v1 − tR⟩2 ≤ 9⟨v1 ⟩3/2 .
Moreover,           Z       2                Z               2R
                                ⟨v0 − tR⟩2 dt = R−1               ⟨v0 − q⟩2 dq ≤ 2R−1 .
                        1                                   R
Since 1 + |v0 | ≤ 27 R, the left-hand side of (4.11) is at most
                                         3/2
                18R−3/2 ⟨v1 ⟩3/2 ≤ 18 72      ⟨v0 ⟩3/2 ⟨v1 ⟩3/2 < 118⟨v0 ⟩3/2 ⟨v1 ⟩3/2 .
  It remains to consider |v0 |, |v1 | < 3R. Put w = v0 − v1 . The triangle inequality and
(a + b)2 ≤ 2(a2 + b2 ) give
                   ⟨v0 − q⟩2 ⟨v1 − q⟩2 ≤ 2⟨w⟩2 ⟨v0 − q⟩2 + ⟨v1 − q⟩2 .
                                                                     

Hence                              Z 2R
                                           ⟨v0 − q⟩2 ⟨v1 − q⟩2 dq ≤ 8⟨w⟩2 .
                                     R
Since 1 + |v0 + v1 | ≤ 13
                       2
                          R, the left-hand side of (4.11) is at most
                                 3/2
           8R−3/2 ⟨w⟩2 ≤ 8 13  2
                                      ⟨v0 + v1 ⟩3/2 ⟨w⟩3/2 < 133⟨v0 + v1 ⟩3/2 ⟨w⟩3/2 .
This proves (4.11).                                                                            □
Lemma 4.8 (constant C4.7 ()).
                                                  C4.7 ≤ 133.                              (4.13)
Proof (). This is the defining value in Lemma 4.7.                                            □
     For a function ϕ we define
                                               (Xϕ)(u) = uϕ(u).                            (4.14)
Lemma 4.9. Let ψ : R → R be a Schwartz function and assume that
                             b ⊂ [−1, −2−2 ] ∪ [2−2 , 1]
                       supp(ψ)                                                             (4.15)
           2
Let Ψ : R → R be defined as
                                                     Z 2
                                         Ψ(u, v) =         ψ(t) (u)ψ(t) (v) dtt            (4.16)
                                                      1
and let ℓ ∈ Z. Then
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                            67

   (1) For all (u, v) ∈ R2 , Ψ(2ℓ ) (u, v) = Ψ(2ℓ ) (v, u)
   (2) For all bounded functions f : R → R,
                             Z
                                 f (u)f (v)Ψ(2ℓ ) (u, v) dudv ≥ 0                      (4.17)
                                R2
                           −ℓ   −3−ℓ
   (3) supp(Ψ
            [(2ℓ ) ) ⊂ ([−2 , −2     ] ∪ [2−3−ℓ , 2−ℓ ])2 ⊂ Ann1 (2−ℓ , 23 )2
Proof. The symmetry (1) is immediate from the definition. The claim (2) follows from
          Z                                  Z 2 Z                    2
             f (u)f (v)Ψ(2ℓ ) (u, v) du dv =        f (u)ψ(2ℓ t) (u) du dtt ≥ 0.
            R2                                      1     R

To see (3), we use the assumption (4.15) and 1 ≤ t ≤ 2. Thus, if ψ      d(t) (ξ) = ψ(tξ) is
                                                                                   b
non-zero, then necessarily 2−2 t−1 ≤ |ξ| ≤ t−1 , so 2−3 ≤ |ξ| ≤ 1 and thus
                                           −3     −3                3
                      supp(ψ(t) ) ⊂ [−1, −2 ] ∪ [2 , 1] ⊂ Ann1 (1, 2 )
                           d
By rescaling,
                                     −ℓ   −3−ℓ
                     [
                supp(ψ (2ℓ t) ) ⊂ [−2 , −2     ] ∪ [2−3−ℓ , 2−ℓ ] ⊂ Ann1 (2−ℓ , 23 )
Then the bound (3) follows.                                                                □
Lemma 4.10. Let Ψ : R2 → R be such that Ψ(u0 , u1 ) = Ψ(u1 , u0 ) for all (u0 , u1 ) ∈ R2
and such that for all bounded functions g : R → R,
                               Z
                                  g(u0 )g(u1 )Ψ(u) du ≥ 0                           (4.18)
                                     R2
Then for all ξ ∈ R,
                                              b −ξ) ≥ 0.
                                              Ψ(ξ,                                     (4.19)
Proof (). By symmetry,
                                          Z
                         b −ξ) =
                         Ψ(ξ,                  Ψ(u) cos(2πξ(u1 − u0 )) du.
                                          R2
Since
          cos(2πξ(u1 − u0 )) = cos(2πξu0 ) cos(2πξu1 ) + sin(2πξu0 ) sin(2πξu1 ),
the right-hand side is the sum of the two expressions in (4.18) obtained by taking
g(u) = cos(2πξu) and g(u) = sin(2πξu). Both are nonnegative.                    □
4.1.4. Windows and pairs.
Definition 4.11 ((c, N )-window). Let c > 0, N ∈ N. A (c, N )-window is a Schwartz
function ϕ : R → R such that
   (1) For all ξ ∈ R, ϕb is real and
                                     0 ≤ ϕ(ξ)
                                         b ≤ 1.                              (4.20)
   (2) For all ξ ∈ R \ [−1, 1] we have
                                               ϕ(ξ)
                                               b = 0.                                  (4.21)
68                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

      (3) For all ξ ∈ [− 12 , 12 ] we have
                                                  ϕ(ξ)
                                                  b = 1.                          (4.22)
      (4) For all ξ ∈ [−1, 1] and all m ≤ N ,
                                                |ϕb(m) (ξ)| ≤ c.                  (4.23)
Definition 4.12 ((c, N )-pair). Let c > 0, N ∈ N. A pair (ϕ0 , ϕ1 ) of (c, N )-windows is
a (c, N )-pair if
                                (ϕb0 )2 + (1 − ϕb1 )2 = 1.                         (4.24)
     If (ϕ0 , ϕ1 ) is a (c, N )-pair, then we write
                                                ϕi,k = (ϕi )(2k )                 (4.25)
for i ∈ [2), k ∈ Z
   Existence of (c, N )-pairs is shown in Lemma 4.15.
Definition 4.13 (Universal pair). Set
                                                  N4.13 = 3,                      (4.26)
and
                                          C4.13 = 215 .                           (4.27)
A universal pair is a (C4.13 , N4.13 )-pair.
Definition 4.14 (Windows). A function is a window if it is one of the two components
of a universal pair.
Lemma 4.15 (Existence of a universal pair). There exists a universal pair.
Proof (). Let h = 1 − Φ,   b where Φ is the standard bump from Proposition 2.46, and
define
                          ϕb0 = cos(πh/2),        ϕb1 = 1 − sin(πh/2).
Both functions are smooth, real, and even. On [−1/2, 1/2] we have h = 0, so both equal
1. Outside [−1, 1] we have h = 1, so both vanish. Since 0 ≤ h ≤ 1, both take values in
[0, 1], and
                    (ϕb0 )2 + (1 − ϕb1 )2 = cos2 (πh/2) + sin2 (πh/2) = 1.
Their inverse Fourier transforms are real-valued Schwartz functions.
   It remains to verify the derivative bound. The proof of Proposition 2.46 gives
                                        ∥h(q) ∥∞ ≤ 2q(q−1)/2+3q
for 1 ≤ q ≤ 3. Applying the Faà di Bruno formula to the two trigonometric composi-
tions, using π/2 < 2, and grouping terms by their block sizes gives the following bounds
for derivatives of orders 1, 2, 3:
                                         24 ,         29 ,      215 .
Before rounding to powers of two, the corresponding Faà di Bruno sums are
                                                     2 · 23 ,
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                         69

                                               2 · 2 7 + 22 · 2 6 ,
and
                                      2 · 212 + 3 · 22 · 210 + 23 · 29 .
These are bounded by the three displayed powers of two. Thus every derivative of order
at most N4.13 is bounded by C4.13 . The order-zero bound is at most 1, so (ϕ0 , ϕ1 ) is a
(C4.13 , N4.13 )-pair.                                                                 □

4.1.5. A smoothing decomposition. In this section we decompose the characteristic func-
tion 1[0,1) into smoother functions.
Definition 4.16 (Window-based bump functions). Let (ϕ0 , ϕ1 ) be a universal pair.
Define
                              θ = ϕ0 − (ϕ0 )(2) .                           (4.28)
Define for k ∈ Z,
                                     φ0,k = (1[0,1) ∗ ϕ0 − ϕ0 ) ∗ θ(2k )                            (4.29)
                                            φ1,k = 1[0,∞) ∗ θ(2k )                                  (4.30)
                                           φ2,k = −1[1,∞) ∗ θ(2k )                                  (4.31)
                                            φ3,k = 2k (φ0,k )(2−k )                                 (4.32)
Let
                                                      e − 2−k ),
                                        φ4,k (u) = 2k θ(u                                           (4.33)
where θe = 1[0,∞) ∗ θ (a primitive of θ).
Lemma 4.17. Let θ be as in (4.28).

  (i) We have
                                 supp θb ⊂ [−1, −2−2 ] ∪ [2−2 , 1]                                  (4.34)
  (ii) For every m ∈ Z
                                            ∞
                                            X
                                                  θ(2ℓ ) = (ϕ0 )(2m )                               (4.35)
                                            ℓ=m
and the series converges uniformly.
Proof. (i) This is immediate from the support of windows. (ii) For N ≥ m and write
                    N
                    X                N
                                     X
             SN =         θ(2ℓ ) =         (ϕ0 )(2ℓ ) − (ϕ0 )(2ℓ+1 ) = (ϕ0 )(2m ) − (ϕ0 )(2N +1 )
                    ℓ=m              ℓ=m

For any x ∈ R we bound
             |SN (x) − (ϕ0 )(2m ) (x)| = |(ϕ0 )(2N +1 ) (x)| ≤ 2−N −1 ∥ϕ0 ∥∞ ≤ 2−N
Since 2−N converges to 0 as N → ∞, the conclusion follows.                                              □
70                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Lemma 4.18. With ϕ0 , θ defined as in (4.28), the identity
                                                         −1
                                                         X
                            1[0,1] = 1[0,1] ∗ ϕ0 +              1[0,1] ∗ θ(2ℓ )            (4.36)
                                                        ℓ=−∞

holds in L2 .
Remark 4.1. This identity also holds pointwise a.e., which can be shown using the
weak L2 boundedness of the maximally truncated convolution-type singular integrals.
However, norm convergence suffices for our proof.
Proof (). For N > 1, the definition of θ gives
                                          −1
                                          X
                                 ϕ0 +            θ(2ℓ ) = (ϕ0 )(2−N ) .
                                         ℓ=−N

By Plancherel’s identity, the L2 norm of the difference between the two sides of the
asserted partial sum identity is
                                              b −N ξ)
                                                      
                              1d[0,1] (ξ) 1 − ϕ0 (2      .
                                                                    L2 (ξ)

The second factor vanishes when |ξ| ≤ 2N −1 and has modulus at most one. Moreover,
                                                            −1
                                |1d
                                  [0,1] (ξ)| ≤ min(1, (π|ξ|) ).

Consequently the preceding norm is at most
                             Z ∞           1/2
                                       dξ          1−N/2
                              2       π2 ξ2
                                                 =2 π ,
                                         2N −1
which tends to zero.                                                                           □
Lemma 4.19 (Smoothing decomposition). The identity
                                       ∞
                                       X                −1
                                                        X                 −1
                                                                          X
                       1[0,1] = ϕ0 +          φ0,k +          φ1,k +              φ2,k .   (4.37)
                                       k=−2            k=−∞             k=−∞
                2
holds in the L sense.
Proof. By Lemma 4.18 we have
                                                        −1
                                                        X
                            1[0,1] = 1[0,1] ∗ ϕ0 +              1[0,1] ∗ θ(2k )            (4.38)
                                                        k=−∞
                                2
where the identity holds in L . Denoting φ = 1[0,1] ∗ ϕ0 and splitting
                                       1[0,1] = 1[0,∞) − 1[1,∞)
we thus have
                                                 −1
                                                 X               −1
                                                                 X
                             1[0,1] = φ +              φ1,k +          φ2,k ,
                                              k=−∞              k=−∞
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                               71

where the sums converge in L2 . It remains to decompose φ. We write φ = ϕ0 + (φ − ϕ0 )
and
                             φ − ϕ0 = (φ − ϕ0 ) ∗ (ϕ0 )(2−2 ) ,
where the last identity holds due to
                              − ϕ0 (ξ)(ϕ\
                             φ\         0 )(2−2 ) (ξ) = φ − ϕ0 (ξ)
                                                        \

for each ξ ∈ R. Indeed, the function φ\        − ϕ0 (ξ) = 0 for |ξ| ≥ 1 and (ϕ\  0 )(2−2 ) (ξ) =
      −2
ϕb0 (2 ξ) = 1 for |ξ| ≤ 2. By part (ii) of Lemma 4.17 we obtain
                                             ∞
                                            X          ∞
                                                         X                       ∞
                                                                                 X
      (φ − ϕ0 ) ∗ (ϕ0 )(2−2 ) = (φ − ϕ0 ) ∗    θ(2k ) =     (φ − ϕ0 ) ∗ θ(2k ) =      φ0,k .
                                          k=−2           k=−2                     k=−2

The second equality is justified, for example, by uniform convergence.                       □
Lemma 4.20. Let 1 ≤ N ≤ 3. Then
                                    |θ(u)| ≤ C4.20,N ⟨u⟩N ,                              (4.39)
where
                                    C4.20,N = 22N +2 C4.13 .                             (4.40)
Proof (). We have
                                    b = ϕb0 (ξ) − ϕb0 (2ξ)
                                    θ(ξ)
and, for m ≤ N ,
                           ∥θb(m) ∥∞ ≤ (1 + 2m )C4.13 ≤ 2m+1 C4.13 .
The support of θb has measure at most two. If N = 1, Fourier inversion and one
integration by parts, followed by Lemma 2.42, give
                  |θ(u)| ≤ 4C4.13 min(1, |u|−1 ) ≤ 23 C4.13 ⟨u⟩ ≤ 24 C4.13 ⟨u⟩.
If N ∈ {2, 3}, Lemma 2.43, applied with m = N , gives
                      |θ(u)| ≤ 2N 2N +1 C4.13 2⟨u⟩N = 22N +2 C4.13 ⟨u⟩N .
                                                                                             □
Lemma 4.21 (constant C4.20,N ()). For 1 ≤ N ≤ 3,
                                      C4.20,N ≤ 22N +17 .                                (4.41)
Proof (). Substitute C4.13 = 215 in (4.40).                                                 □
Lemma 4.22. For k ∈ Z and ξ ∈ R,
                               k d            −k b −k b
                   φ
                   d3,k (ξ) = 2 (1[0,1) − 1)(2 ξ)ϕ0 (2 ξ)θ(ξ)                            (4.42)
Proof. By definition,
                            φ3,k = 2k (1[0,1) ∗ ϕ0 − ϕ0 )(2−k ) ∗ θ.
By the convolution theorem,
                                   k [             −k    b −k b
                     φd3,k (ξ) = 2 (1  [0,1) − 1)(2 ξ)ϕ0 (2 ξ)θ(ξ).

                                                                                             □
72                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Lemma 4.23. Let m ∈ [4), k ∈ Z, and |ξ| ≤ 1. Then
                                       φ3,k (m) (ξ)| ≤ C4.23,m ,
                                      |d                                                 (4.43)
where for m = 0,
                                             C4.23,0 = 4,                                (4.44)
for m = 1,
                                       C4.23,1 = 28C4.13 + 4,                            (4.45)
for m = 2,
                                            2
                               C4.23,2 = 96C4.13 + 140C4.13 + 86,                        (4.46)
and, for m = 3,
                          C4.23,3 = 69 · 24 C4.13
                                             2
                                                  + 47 · 2 · 52 C4.13 + 211 .            (4.47)
Proof (). By Lemma 4.22,
                                      k [ −k              b −k b
                                                        
                          φ
                          d3,k (ξ) = 2 1 [0,1) (2 ξ) − 1 ϕ0 (2 ξ)θ(ξ).

On the support of θb we have |ξ| ≥ 1/4. If k < −2, then |2−k ξ| > 1, so the middle factor
vanishes. We may therefore assume k ≥ −2.
  For q = 0,
                                               −k
                                2k |1
                                    [ [0,1) (2 ξ) − 1| ≤ π|ξ| < 4.

For 1 ≤ q ≤ 3, differentiation under the defining integral for 1     [ [0,1) gives
                                                                      q
                         dq
                                2k 1           −k
                                                         ≤ 22(q−1) (2π)
                                                      
                                       [0,1) (2 ξ) − 1                    .
                                    [
                         dξ q                                       q+1

Using π < 4, these bounds for q = 1, 2, 3, respectively, are
                                       4,      86,       2048.
Moreover, the zeroth derivatives of the second and third factors are at most 1, while for
1 ≤ q ≤ 3,
                  dq b
                     ϕ (2−k ξ) ≤ 22q C4.13 ,
                 dξ q 0
                                               |θb(q) (ξ)| ≤ (1 + 2q )C4.13 .
Substitution in the three-factor Leibniz rule gives, for m = 0, 1, 2, 3, respectively,
                                                        2
                     4,        28C4.13 + 4,          96C4.13 + 140C4.13 + 86,
and
                                  2
                             1104C4.13 + 2350C4.13 + 2048.
These are the defining values.                                                               □
Lemma 4.24 (constant C4.23,m ()). For m = 0,
                                            C4.23,0 = 22 .                               (4.48)
For m = 1,
                                            C4.23,1 < 220 .                              (4.49)
For m = 2,
                                            C4.23,2 < 237 .                              (4.50)
For m = 3,
                                            C4.23,3 < 241 .                              (4.51)
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                       73

Proof (). Substitute C4.13 = 215 in the four defining values.                       □
Lemma 4.25. Let m ∈ [3), k ∈ Z, and |ξ| ≤ 1. Then
                                               (m)
                                     |T[
                                       φ3,k          (ξ)| ≤ C4.25,m ,            (4.52)
where
                               C4.25,m = mC4.23,m + C4.23,m+1 .                  (4.53)
More explicitly,
                                      C4.25,0 = 28C4.13 + 4,                     (4.54)
                                           2
                              C4.25,1 = 96C4.13 + 168C4.13 + 90,                 (4.55)
and
                      C4.25,2 = 81 · 24 C4.13
                                         2
                                              + 263 · 2 · 5C4.13 + 555 · 22 .    (4.56)
Proof (). Lemma 4.5 and Lemma 4.23 give
                                     (m)
                            |T[
                              φ3,k         (ξ)| ≤ mC4.23,m + C4.23,m+1 .
Substitution of the defining values from Lemma 4.23 gives the three stated polynomials.
                                                                                     □
Lemma 4.26 (constant C4.25,m ()). For m = 0,
                                              C4.25,0 < 220 .                    (4.57)
For m = 1,
                                              C4.25,1 < 237 .                    (4.58)
For m = 2,
                                              C4.25,2 < 241 .                    (4.59)
Proof (). Substitute C4.13 = 215 in the three exact values from Lemma 4.25.         □

Lemma 4.27. Let θe be the primitive of θ fixed above. Then

                      supp(θ) ⊂ [−1, −2−2 ] ∪ [2−2 , 1] ⊂ Ann1 (1, 22 ),         (4.60)
                           be


                      supp(T θ) ⊂ [−1, −2−2 ] ∪ [2−2 , 1] ⊂ Ann1 (1, 22 ).       (4.61)
                           ce

For 2 ≤ N < N4.13 ,
                                      |θ(u)|
                                       e     ≤ C4.27,N ⟨u⟩N ,                    (4.62)

                                      |T θ(u)|
                                         e     ≤ C4.27,N ⟨u⟩N ,                  (4.63)
where
                                      C4.27,N = 25N +6 C4.13 .                   (4.64)
74                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

                             b = 0 and θe′ = θ,
                     R
Proof (). Since         θ = θ(0)

                                           θ(ξ) = (2πiξ)−1 θ(ξ).
                                           be              b
This proves (4.60). Also
                                                        b′
                                             T θ(ξ) = −ξ θe (ξ),
                                             ce
which proves (4.61).
  For m ≤ 3, the product rule gives
                                          m  
                         be(m)        −1
                                         X   m
                         θ (ξ) = (2πi)         (−1)q q!ξ −q−1 θb(m−q) (ξ).
                                         q=0
                                             q

On the support, |ξ|−q−1 ≤ 22q+2 , while ∥θb(m−q) ∥∞ ≤ 2m−q+1 C4.13 . For m = 0, 1, 2, 3,
direct substitution in this finite sum gives upper bounds
                           23 C4.13 ,      26 C4.13 ,    29 C4.13 ,   213 C4.13 ,
respectively. Furthermore,
                                         ce (m)     b(m+1)    b(m)
                                        (T θ)   = −ξ θe    − mθe .
Lemma 2.43, the support bound, and the preceding finite estimates give
                        |θ(u)|
                         e     + |T θ(u)|
                                    e     ≤ 25N +6 C4.13 ⟨u⟩N
for 2 ≤ N < N4.13 . This proves (4.62) and (4.63).                                             □
Lemma 4.28 (constant C4.27,N ()). For 2 ≤ N < N4.13 ,
                                             C4.27,N ≤ 25N +21 .                           (4.65)
In particular,
                                                C4.27,2 ≤ 231 .                            (4.66)
Proof (). Substitute C4.13 = 215 in (4.64).                                                   □
                             φ4,k ) ⊂ [−1, −2−2 ] ∪ [2−2 , 1]
Lemma 4.29. We have (a) supp(d

               φ4,k ) ⊂ [−1, −2−2 ] ∪ [2−2 , 1]
     (b) supp(T[
Proof. (a) By Lemma 4.27,

                                    supp(θ) ⊂ [−1, −2−2 ] ∪ [2−2 , 1]
                                         be

The claim follows since
                                               k −2πi2−k ξ b
                                  φ
                                  d 4,k (ξ) = 2 e          θ(ξ).
                                                           e
                                                 −2       −2
  (b) By (a), φd 4,k is supported in [−1, −2 ] ∪ [2 , 1]. By Lemma 4.5 applied with
m = 0,
                                   T[φ4,k (ξ) = −ξ(dφ4,k )′ (ξ)
The support of (d φ4,k )′ is contained in the support of φ    d 4,k , and thus the last display is
non-zero only if |ξ| ≤ 1. The claim follows.                                                    □
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                          75

4.1.6. Miscellany. Let f = (f0 , . . . , fn−1 ) be real-valued Schwartz functions satisfying
(1.4).
Lemma 4.30 (Rescaling). Let ϕ ∈ L1 (R). For all r, q, λ > 0,
                     ∥At (ϕ(λ) )∥Vr,J (t∈(0,∞);Lq ) = ∥At (ϕ)∥Vr,J (t∈(0,∞);Lq ) .                  (4.67)
Proof. By replacing tj λ 7→ tj in the supremum defining the variation seminorm.                         □
Lemma 4.31. If ϕ = ∞                       2       2
                       P
                          j=1 ϕj holds in L (with L functions ϕ, ϕj ), then
                                                       ∞
                                                       X
                             ∥A(ϕ, f )∥L2 (Rn ) ≤             ∥A(ϕj , f )∥L2 (Rn ) .                (4.68)
                                                        j=1
                              PN
Proof (). Let EN = ϕ −            j=1 ϕj . By the triangle inequality,

                                            N
                                            X
                       ∥A(ϕ, f )∥2 ≤              ∥A(ϕj , f )∥2 + ∥A(EN , f )∥2 .
                                            j=1

Cauchy–Schwarz in s gives
                                                                      2          1/2
                                       Z       Y
              ∥A(EN , f )∥2 ≤                         fi (x + sei )       d(x, s)      ∥EN ∥2 .
                                       Rn+1    i∈[n)

The first factor is finite. Indeed, write x = (x0 , x′ ). Since the fi are Schwartz and n ≥ 2,
there is a finite C such that
              |f1 (x + se1 )| ≤ C⟨x0 ⟩2 ,           |f0 (x + se0 )| ≤ C⟨x0 + s⟩2 ⟨x′ ⟩2n ,
and |fi | ≤ C for i ≥ 2. After the change of variables y = x0 + s, the resulting majorant
is integrable in x0 , y, x′ . Since ∥EN ∥2 → 0, letting N → ∞ proves the claim.        □
Lemma 4.32. (i) Let Ψ ∈ W0 (R2 ) be real-valued and assume that
                          Z
                              g(u0 )g(u1 )Ψ(u) du ≥ 0                                               (4.69)
                                       R2

for every bounded measurable g : R → R. Then, for every F ∈ F,
                                              Λ1 (Ψ)(F) ≥ 0.                                        (4.70)
  (ii) In particular, for every real-valued ψ ∈ W0 (R) and every F ∈ F,
                                            Λ1 (ψ ⊗2 )(F) ≥ 0.                                      (4.71)
Proof (). By Definitions 2.17 and 2.25, Proposition 2.24, and the explicit formula
(2.75),
                    Z Z                  Y
        Λ1 (Ψ)(F) =        Ψ(y 1 , y 0 )    Fi (y h − Σ(x), x[n)\i ) dy dx.   (4.72)
                        Rn    R2               h∈[2), i∈[n)
76                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

The integral is absolutely convergent by Propositions 2.24 and 2.18. For x ∈ Rn , set
                                     Y
                            gx (y) =    Fi (y − Σ(x), x[n)\i ).                  (4.73)
                                               i∈[n)

This is a bounded measurable real-valued function. Fubini’s theorem and the change of
variables interchanging y 0 and y 1 show that (4.72) equals
                           Z Z
                                    Ψ(y 0 , y 1 )gx (y 0 )gx (y 1 ) dy dx,     (4.74)
                                Rn     R2
which is nonnegative by (4.69). This proves (i).
  For (ii), take Ψ = ψ ⊗2 . Then, for every bounded measurable real-valued g,
                 Z                                Z            2
                    g(u0 )g(u1 )ψ(u0 )ψ(u1 ) du =    g(u)ψ(u) du ≥ 0.                            (4.75)
                   R2                                                   R
Part (i) gives the result.                                                                           □
Lemma 4.33. Let x ∈ Rn , ϕ a Schwartz function, t ∈ [2k , 2k+1 ], k ∈ Z. Let a(t) =
At (ϕ)(x). Then                         Z                          2
                        ∥ta′ (t)∥2 2        k k+1 dt
                                                     =                 |A2k t (T ϕ)(x)|2 dtt .   (4.76)
                                 L (t∈[2 ,2       ],       )   1
                                                       t
Proof. Note that
                                ∂
                              t ∂t (ϕ(t) (s)) = −(T ϕ)(t) (s),                                   (4.77)
                      ′
where T ϕ(s) = (sϕ(s)) . By this and (1.3),
                            Z Y                  
                ′        ∂
              ta (t) = t ∂t          fi (x + sei ) ϕ(t) (s) ds = −At (T ϕ)(x).
                                 R     i∈[n)

Integrating in t over [2 , 2 ] and changing variables t 7→ 2k t in the t-integration on
                           k   k+1

the right-hand side, the claim follows.                                               □
Lemma 4.34. Let Ψ : R2 → R be a non-zero Schwartz function such that for all
u = (u0 , u1 ) ∈ R2 ,
                               Ψ(u0 , u1 ) = Ψ(u1 , u0 ).             (4.78)
Assume also that for every bounded measurable g : R → R,
                             Z
                                g(u0 )g(u1 )Ψ(u) du ≥ 0,              (4.79)
                                       R2
and that
                                            b ⊂ Ann1 (1, 23 )2
                                       supp(Ψ)                                                   (4.80)
and, for a ∈ [3) and ξ ∈ R,
                                               da b
                                               dξ a
                                                    Ψ(ξ, −ξ)       ≤ 1.                          (4.81)
Let (ϕ0 , ϕ1 ) be a universal pair. There exists a real even smooth function ψ : R → R
such that
   (1) For all ξ ∈ R,
                            b 2 = 2(ϕ[
                            ψ(ξ)            d        2
                                     0,−5 − ϕ1,5 )(ξ) − Ψ(ξ, −ξ).
                                                        b                                        (4.82)
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                77

   (2) ψb is supported in Ann1 (1, 26 ).
   (3) For all a ∈ [3) and ξ ∈ R,
                                        |ψb(a) (ξ)| ≤ C4.34 ,                              (4.83)
         where
                                        C4.34 = 212 C4.13 .                                (4.84)
Proof (). Put
                              ϑ(ξ) = ϕb0 (2−5 ξ) − ϕb1 (25 ξ).
The function ϑ is nonnegative, supported in Ann1 (1, 26 ), and equal to 1 on Ann1 (1, 24 ).
By Lemma 4.10 and (4.81),
                                  0 ≤ Ψ(ξ,
                                       b −ξ) ≤ 1.
      b −ξ) is supported in Ann1 (1, 23 ), it follows that
Since Ψ(ξ,
                                        b −ξ) ≤ ϑ(ξ)2 .
                                    0 ≤ Ψ(ξ,                                               (4.85)
Define
                                            b −ξ) 1/2 .
                               b = 2ϑ(ξ)2 − Ψ(ξ,
                                                 
                               ψ(ξ)                                                        (4.86)
On the complement of Ann1 (1, 2 ) this is 2 ϑ, while on the interior of Ann1 (1, 24 ) the
                                    3            1/2

expression under the square root is 2 − Ψ(ξ,
                                          b −ξ) ≥ 1. These two open sets cover R, so ψb
is smooth. It is real and even, and its support is contained in Ann1 (1, 26 ). This proves
the first two assertions.
   For a ∈ [3),
                              |ϑ(a) (ξ)| ≤ (2−5a + 25a )C4.13 .
Thus, outside Ann1 (1, 23 ),
                 |ψ(ξ)|
                  b     ≤ 2,      |ψb′ (ξ)| ≤ 27 C4.13 ,        |ψb′′ (ξ)| ≤ 212 C4.13 .
On the interior of Ann1 (1, 24 ), set f (ξ) = 2 − Ψ(ξ,b −ξ). Then 1 ≤ f ≤ 2 and |f ′ |, |f ′′ | ≤
1, whence
                    |f 1/2 | ≤ 2,       |(f 1/2 )′ | ≤ 21 , |(f 1/2 )′′ | ≤ 34 .
The derivative estimate follows.                                                                □
Lemma 4.35 (constant C4.34 ()).
                                           C4.34 = 227 .                                   (4.87)
Proof (). This follows from (4.84) and C4.13 = 215 .                                          □
Lemma 4.36 (Bootstrapping). Let ϕ : R → R be a Schwartz function. Then
                                                     X
                 ∥At (ϕ)∥2V2,J (t∈2Z ;L2 ) ≤ 4 · sup   ∥A2kℓ (ϕ)∥22                        (4.88)
                                                           ℓ∈[J)

where the supremum is over all sequences of integers k0 < · · · < kJ−1 .
  Note: This lemma will only be applied to mean zero bump functions.
78                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof. Let k0 < · · · < kJ be integers. For ℓ ∈ [J) we write
                      ∥A2kℓ+1 (ϕ) − A2kℓ (ϕ)∥22 = ∥A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )∥22          (4.89)
                      Z
                    =     A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )(x)A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )(x)dx
                          Rn
     where k0 < . . . < kJ is any increasing sequence of integers.
     By the distributive law,
                                   X
                                       ∥A2kℓ+1 (ϕ) − A2kℓ (ϕ)∥22
                                        ℓ∈[J)
                          XZ
                      =                 A(ϕ(2kℓ+1 ) )(x)A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )(x)dx
                          ℓ∈[J)    Rn

                             XZ
                       −                 A(ϕ(2kℓ ) )(x)A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )(x)dx
                           ℓ∈[J)   Rn

By the Cauchy-Schwarz inequality in x and in the summation, this is
               X                    1/2  X                            1/2
                                   2                                   2
            ≤       ∥A(ϕ(2kℓ+1 ) )∥2          ∥A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )∥2
                     ℓ∈[J)                            ℓ∈[J)
                   X                 1/2  X                             1/2
                  +   ∥A(ϕ(2kℓ ) )∥22          ∥A(ϕ(2kℓ+1 ) − ϕ(2kℓ ) )∥22
                      ℓ∈[J)                          ℓ∈[J)

And thus, with V = ∥At (ϕ)∥V2,J (t∈2Z ;L2 ) ,
                     X                      1/2  X                 1/2 
            V2 ≤V ·         ∥A(ϕ(2kℓ+1 ) )∥22     +    ∥A(ϕ(2kℓ ) )∥22
                               ℓ∈[J)                              ℓ∈[J)

We may assume V ̸= 0 as otherwise the claim holds trivially. Dividing by V and esti-
mating the terms on the right-hand side by the supremum over all increasing sequences
of integers gives
                                       X                   1/2
                          V ≤ 2 · sup       ∥A(ϕ(2kℓ ) )∥22
                                                   ℓ∈[J)
Squaring both sides gives the desired estimate.                                            □
4.2. On-diagonal from main argument. Throughout this section, let ν = 1 if n > 2
and ν = 2 if n = 2.
Lemma 4.37 (ρ kernels - reduction variant). Let a ∈ A. For h ∈ N with h ≥ 1 and
j ∈ Z, define
                                λ−
                                 h,j = 2
                                        h−1
                                            a(j),                         (4.90)
and, for j ∈ Z, define
                                λ−
                                 0,j = a(j − 1).                          (4.91)
For h ∈ N and j ∈ Z, define
                                 λ+      h
                                  h,j = 2 a(j).                           (4.92)
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                   79

For h ∈ N and j ∈ Z, also define
                            µ−      h
                             h,j = 2 a(j − 1),          µ+      h
                                                         h,j = 2 a(j).                        (4.93)
Let ρh,j be the function whose Fourier transform is
                                                                       −ν/2
                            b −         b +          −           +
                                                 
                  h,j (ζ) = Φ(λh,j ζ) − Φ(λh,j ζ) g(µh,j ζ) − g(µh,j ζ)
                 ρd                                                          .                (4.94)
  Then ρh,j ∈ W0 (R). Moreover, if h ≥ 1, then, with λ = 2h a(j),
         |ρh,j (x + p) − ρh,j (x)| ≤ C4.37 min(1, λ−1 |p|) ⟨x + p⟩2(λ) + ⟨x⟩2(λ) ,
                                                                                
                                                                                              (4.95)
and if h ∈ N, then
                            |ρh,j (x)| ≤ C4.37 ⟨x⟩2(λ− ) + ⟨x⟩2(λ+ ) ,
                                                                    
                                                                                              (4.96)
                                                       h,j          h,j

where C4.37 = 221 (C2.68,2 + C2.66,2 ).
Proof. If h ≥ 1, the parameters satisfy
                                  2µ−       −      +      +
                                    h,j ≤ 2λh,j = λh,j = µh,j ,

because 2a(j − 1) ≤ a(j). If h = 0, we have
                                  2µ−       −      +      +
                                    0,j = 2λ0,j ≤ λ0,j = µ0,j .

  Now, if h ≥ 1, we use Proposition 2.68 with N = 2, which gives
         |ρh,j (x + p) − ρh,j (x)| ≤ 218 C2.68,2 min(1, 2πλ−1 |p|)(⟨x + p⟩2(λ) + ⟨x⟩2(λ) ),
which gives (4.95). Here we also used that by Proposition 2.46,
                                           b (m) ∥∞ ≤ 218 .
                                     max ∥(Φ)
                                    0≤m≤2

If h ∈ N, we use Proposition 2.66 with N = 2, which gives ρh,j ∈ W0 (R) and
                          |ρh,j (x)| ≤ 218 C2.66,2 (⟨x⟩2(λ− ) + ⟨x⟩2(λ+ ) ).
                                                             h,j          h,j

                                                                                                  □
Lemma 4.38 (constant C4.37 ()).
                                            C4.37 < 266 .                                     (4.97)
Proof (). Lemmas 2.69 and 2.67, at N = 2, give
                    C2.68,2 + C2.66,2 < 20397963318112 + 637436354528.
Multiplication by the defining factor 221 gives
                           C4.37 < 44114430494276321280 < 35 266 .
                                                                                                  □
Remark 4.2. The value of ρd h,j at the origin is understood through the continuous ex-
tension supplied by Proposition 2.66.
80                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Lemma 4.39 (affine diagonal cancellation - reduction variant). Let M ∈ W0 (R2 ) satisfy
for every ξ ∈ R
                                   c(ξ, −ξ) = 0
                                   M                                            (4.98)
Then for every x ∈ R,         Z
                                                 M (x + q, q) dq = 0                             (4.99)
                                             R

Proof. Define                                      Z
                                     G(x) =               M (x + q, q) dq.
                                                      R
By Proposition 2.8, G ∈ W0 (R). By Fubini’s theorem and the change of variables
u = x + q, v = q, we have
         Z                                Z
                           −2πixξ
  G(ξ) =
  b          M (x + q, q)e        dq dx =   M (u, v)e−2πi(u−v)ξ du dv = M
                                                                        c(ξ, −ξ) = 0.
              R2                                          R2

Injectivity of the Fourier transform on L1 and continuity of G give G = 0 everywhere.
                                                                                   □
Proposition 4.40 (bracket domination - reduction variant). Let a ∈ A, and let P ⊂
Bdist (a, 1)2 × [2) be such that #P ≤ 5. Assume additionally that
                                     t0 (j) ≤ a(j),            t1 (j) ≤ a(j)                    (4.100)
for every (t0 , t1 , u) ∈ P and j ∈ Z. Suppose that Mj ∈ W0 (R2 ) satisfies
                                                 cj (ξ, −ξ) = 0
                                                 M                                              (4.101)
and                                      X                       3/2                3/2
                        |Mj (v)| ≤                   ⟨(Wu v)0 ⟩(t0 (j)) ⟨(Wu v)1 ⟩(t1 (j)) .    (4.102)
                                     (t0 ,t1 ,u)∈P

     Let λ−      +                                                                  h
          h,j , λh,j be as in Lemma 4.37. For h ∈ N, j ∈ Z, we define σh,j = s(2 a, j) and
                                                                               
        Nh,j = F −1 (ξ, η) 7→ (Φ \  −
                                  (λ ) − Φ
                                         \   + )(ξ + η)d
                                           (λ )        σ h,j (ξ + η)−ν c
                                                                      M j (ξ, η)  ,   (4.103)
                                       h,j             h,j

     Then for every h ∈ N, there exist a finite set Bh , numbers uh,b ∈ [2), and pairs
                                       0      1
                              βh,b = (βh,b , βh,b ) ∈ A2 ,               b ∈ Bh ,               (4.104)
satisfying
                                                 #Bh ≤ C4.40,0 ,                                (4.105)
                                                  ℓ
                                         dist(a, βh,b ) ≤ (1 + h)                               (4.106)
for every b ∈ Bh and ℓ ∈ [2), and
                                    X              7/6                    7/6
         |Nh,j (v)| ≤ C4.40,1 2−h/3   ⟨(Wuh,b v)0 ⟩(β 0 (j)) ⟨(Wuh,b v)1 ⟩(β 1 (j))             (4.107)
                                                                  h,b                     h,b
                                        b∈Bh
                   6              10
where C4.40,0 = 2 , C4.40,1 = 2 C4.37 . In particular,
                                             ∆(βh,b ) ≤ 2(1 + h).                               (4.108)
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                             81

Proof (). Set
                                     r = 76 ,          Cρ = C4.37 ,
and, for s > 0, define
                                              ωs (x) = ⟨x⟩r(s) .
  We first record several elementary estimates that will be used throughout the proof.
Since
                                      r = 76 < 32 < 2,
we have
                                              3/2
                                ⟨x⟩2(s) ≤ ⟨x⟩(s) ≤ ωs (x).                     (4.109)
Moreover,                                 Z ∞
                             ∥ωs ∥1 = 2         (1 + x)−7/6 dx = 12 ≤ 24 .             (4.110)
                                          0
Directly from the definition of the bracket bumps,
                            √                      √
                      ωs (x/ 2) ≤ 2ωs (x),     ωs ( 2x) ≤ ωs (x).                      (4.111)
  Proposition 2.48, applied with both exponents equal to r, gives
                     Z
                       ωs (x − p)ωt (y − p) dp ≤ 26 ωmax(s,t) (x − y).                 (4.112)
                         R
Indeed,
                      C2.48,r,r = 21+r 1 + (r − 1)−1 = 7 · 213/6 < 26 .
                                                       

  We will also use the following consequence of Propositions 2.51 and 2.50. Suppose
that
                               v0 = w0 − w1 ,       v1 = w0 + w1 .
Then                                           √      √
                                    W1 v = ( 2w0 , 2w1 ).
Let
                                  e0 = (1, 0),      e1 = (0, 1),
and
                          θ0 = 2−1/2 (1, 1),       θ1 = 2−1/2 (−1, 1).
Thus
               v · θ0 = (W1 v)0 ,       v · θ1 = (W1 v)1 ,     w1 = 2−1/2 v · θ1 .
For either i = 0 or i = 1, the constant in Proposition 2.50, applied to ei and θ1 , is
                                                 √
                           (2|ei · θ0 |−1 )r = (2 2)7/6 = 27/4 < 22 .
Combining this with (4.111), we obtain
                                                                              
                                 3
             ωs (v0 )ωt (w1 ) ≤ 2 ωs (v0 )ωt (v1 ) + ωs ((W1 v)0 )ωt ((W1 v)1 )        (4.113)
and                                                                              
               ωs (v1 )ωt (w1 ) ≤ 23 ωt (v0 )ωs (v1 ) + ωs ((W1 v)0 )ωt ((W1 v)1 ) .   (4.114)
82                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

   We next express Nh,j as a convolution. Let ρh,j be as in Lemma 4.37. By the definition
of σh,j = s(2h a, j),
                                     h                 h
                                                               1/2
                      σ
                      d h,j (ζ) = g(2 a(j − 1)ζ) − g(2 a(j)ζ)       .
It follows from Proposition 2.13 that
                                             Nh,j = Mj ∗(1,1) ρh,j .                  (4.115)
     Fix h ∈ N, j ∈ Z, and v ∈ R2 , and write
                                   v0 = w0 − w1 ,           v1 = w0 + w1 .
Changing variables in (4.115), we obtain
                             Z
                  Nh,j (v) =    ρh,j (w0 + p)Mj (−w1 − p, w1 − p) dp.                 (4.116)
                                         R
     We first treat the case h ≥ 1. Set
                                                  λ = 2h a(j).
By Lemma 4.39, applied with x = −2w1 ,
                         Z
                            Mj (−w1 − p, w1 − p) dp = 0.
                                     R
Consequently,
                        Z
                                                         
           Nh,j (v) =          ρh,j (w0 + p) − ρh,j (w0 ) Mj (−w1 − p, w1 − p) dp.    (4.117)
                           R

Lemma 4.37, together with (4.109), gives
                 XZ
 |Nh,j (v)| ≤ Cρ      min(1, λ−1 |p|)ωλ (w0 + αp) × |Mj (−w1 − p, w1 − p)| dp. (4.118)
                   α∈[2)       R

     Fix
                                    (t0 , t1 , u) ∈ P,
and suppress the argument j in t0 (j) and t1 (j). The additional one-sided assumption
(4.100) implies
                         tℓ ≤ a(j) ≤ 2h a(j) = λ,      ℓ ∈ [2).                (4.119)
  Suppose first that u = 0. Then
                                    3/2               3/2              3/2    3/2
                   ⟨(−w1 − p)⟩(t0 ) ⟨(w1 − p)⟩(t1 ) = ⟨w1 + p⟩(t0 ) ⟨w1 − p⟩(t1 ) .
Since
                                         2|p| ≤ |w1 + p| + |w1 − p|
                    1/3
and min(1, s) ≤ s         , we have
                   min(1, λ−1 |p|) ≤ 2−1/3 λ−1/3 |w1 + p|1/3 + |w1 − p|1/3 .
                                                                          

Since
                                                  tℓ /λ ≤ 2−h ,
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                         83

it follows that
            min(1, λ−1 |p|) ≤ 2−h/3 (1 + t−1          1/3
                                                          + (1 + t−1          1/3
                                                                                  
                                          0 |w1 + p|)             1 |w1 − p|)       .
Multiplying by the two 3/2-bumps and using
                                             3
                                             2
                                               − 13 = 67 = r,
we obtain
                               3/2          3/2
  min(1, λ−1 |p|)⟨w1 + p⟩(t0 ) ⟨w1 − p⟩(t1 )           ≤ 2 · 2−h/3 ωt0 (w1 + p)ωt1 (w1 − p).    (4.120)
  Suppose now that u = 1. Since
                                                       √ √
                              W1 (−w1 − p, w1 − p) = (− 2p, 2w1 ),
we have
                                                          √                            √
  min(1, λ−1 |p|) ≤ (λ−1 |p|)1/3 = 2−1/6 (t0 /λ)1/3 (t−1
                                                      0  |  2p|)1/3
                                                                    ≤ 2−h/3
                                                                            (1 + t −1
                                                                                   0  |  2p|)1/3 .
It follows that
                       √ 3/2 √          3/2
                                                                        √        √
       min(1, λ−1 |p|)⟨ 2p⟩(t0 ) ⟨ 2w1 ⟩(t1 )          ≤ 2 · 2−h/3 ωt0 ( 2p)ωt1 ( 2w1 ).        (4.121)
  We now integrate the expressions resulting from (4.120) and (4.121).
  Assume first that u = 0. For α = 0, let
                                            τ = max(t0 , t1 ).
By (4.112),
                          Z
               ωλ (w0 )       ωt0 (w1 + p)ωt1 (w1 − p) dp          ≤ 26 ωλ (w0 )ωτ (2w1 ).
                          R
Using                                      √                           √
                         (W1 v)0 =             2w0 ,      (W1 v)1 =        2w1
and (4.111), this is at most
                                      27 ωλ ((W1 v)0 )ωτ ((W1 v)1 ).                            (4.122)
  For α = 1, Proposition 2.51, applied with
                                     w1 = 12 (w1 + p) + 21 (w1 − p),
has constant one and gives
    ωt0 (w1 + p)ωt1 (w1 − p)            ≤ ωt0 (w1 + p)ωt1 (w1 ) + ωt0 (w1 )ωt1 (w1 − p).        (4.123)
Since λ ≥ t0 , t1 , Proposition 2.48 gives
  Z                                                                                                
     ωλ (w0 + p)ωt0 (w1 + p)ωt1 (w1 − p) dp               ≤ 26 ωλ (v0 )ωt1 (w1 ) + ωλ (v1 )ωt0 (w1 ) .
   R

Applying (4.113) and (4.114), the last expression is at most
                                 29 ωλ (v0 )ωt1 (v1 ) + 29 ωt0 (v0 )ωλ (v1 )                    (4.124)
                          + 29 ωλ ((W1 v)0 ) (ωt1 ((W1 v)1 ) + ωt0 ((W1 v)1 )) .
84                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

     Suppose next that u = 1. For α = 0, (4.110) gives
                         Z     √            √                        √
                 ωλ (w0 ) ωt0 ( 2p) dp ωt1 ( 2w1 ) ≤ 24 ωλ (w0 )ωt1 ( 2w1 ).
                               R
By (4.111), this is at most
                                        25 ωλ ((W1 v)0 )ωt1 ((W1 v)1 ).
For α = 1, we use                      √
                                  ωt0 ( 2p) ≤ ωt0 (p)
and Proposition 2.48. Since λ ≥ t0 , we obtain
             Z                  √            √                        √
                ωλ (w0 + p)ωt0 ( 2p) dp ωt1 ( 2w1 ) ≤ 26 ωλ (w0 )ωt1 ( 2w1 ).
                   R
By (4.111), this is at most
                                        27 ωλ ((W1 v)0 )ωt1 ((W1 v)1 ).
Thus, for both α ∈ [2),
    Z                   √        √
       ωλ (w0 + αp)ωt0 ( 2p)ωt1 ( 2w1 ) dp                      ≤ 27 ωλ ((W1 v)0 )ωt1 ((W1 v)1 ).       (4.125)
        R
  Combining (4.118), (4.120), (4.121), (4.122), (4.124), and (4.125), we conclude that,
when h ≥ 1, every resulting product of two r-bumps occurs with coefficient at most
                                       2 · 29 Cρ 2−h/3 = 210 Cρ 2−h/3 .
Every such product is in either the W0 - or the W1 -coordinates. Its two scale sequences
are among
                          2h a,    t0 ,    t1 ,   max(t0 , t1 ).
  It remains to treat h = 0. Define the two sequences
                                   d0 (j) = a(j − 1),             d1 (j) = a(j).
By Lemma 4.37, (4.116), and (4.109),
                       XZ
       |N0,j (v)| ≤ Cρ       ωdϵ (j) (w0 + p)|Mj (−w1 − p, w1 − p)| dp.                                 (4.126)
                               ϵ∈[2)   R

     Fix again (t0 , t1 , u) ∈ P, and define
                                    rϵ,ℓ = max(dϵ , tℓ ),            ϵ, ℓ ∈ [2).
If u = 0, then Proposition 2.51, followed by Proposition 2.48, gives
                    Z
                        ωdϵ (j) (w0 + p)ωt0 (j) (w1 + p)ωt1 (j) (w1 − p) dp
                      R
                                                                                  
                   ≤ 26 ωrϵ,0 (j) (v0 )ωt1 (j) (w1 ) + ωrϵ,1 (j) (v1 )ωt0 (j) (w1 ) .
Using (4.113) and (4.114), this is bounded by
                           29 ωrϵ,0 (j) (v0 )ωt1 (j) (v1 ) + 29 ωt0 (j) (v0 )ωrϵ,1 (j) (v1 )            (4.127)
             + 29 ωrϵ,0 (j) ((W1 v)0 )ωt1 (j) ((W1 v)1 ) + 29 ωrϵ,1 (j) ((W1 v)0 )ωt0 (j) ((W1 v)1 ).
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                            85

  If u = 1, then                            √
                                   ωt0 (j) ( 2p) ≤ ωt0 (j) (p).
Proposition 2.48 and (4.111) therefore give
  Z                          √            √
    ωdϵ (j) (w0 + p)ωt0 (j) ( 2p)ωt1 (j) ( 2w1 ) dp      ≤ 27 ωrϵ,0 (j) ((W1 v)0 )ωt1 (j) ((W1 v)1 ).
    R
                                                                                                       (4.128)
Thus every product produced in the case h = 0 has coefficient at most
                                           29 Cρ ≤ 210 Cρ .
   We now collect all products obtained above, retaining multiplicities. Each product
has the form
                              ωβ 0 (j) ((Wu v)0 )ωβ 1 (j) ((Wu v)1 )
for some u ∈ [2) and some β = (β 0 , β 1 ) ∈ A2 . For every such product introduce one
label b, and denote the resulting index set by Bh . Set
                                      uh,b = u,           βh,b = β.
Since
                                          210 Cρ = C4.40,1 ,
the preceding estimates prove
                                              X                    7/6                    7/6
           |Nh,j (v)| ≤ C4.40,1 2−h/3     ×          ⟨(Wuh,b v)0 ⟩(β 0 (j)) ⟨(Wuh,b v)1 ⟩(β 1 (j)) .
                                                                     h,b                    h,b
                                              b∈Bh

   We verify the cardinality bound. When h ≥ 1, a summand of the pointwise majorant
for Mj with u = 0 produces one term from α = 0 and four terms from α = 1, hence at
most five terms. A summand with u = 1 produces at most two terms. Therefore,
                                         #Bh ≤ 5#P ≤ 25
when h ≥ 1. When h = 0, a summand with u = 0 produces four terms for each ϵ ∈ [2),
hence at most eight terms, while a summand with u = 1 produces at most two terms.
Thus
                                     #B0 ≤ 8#P ≤ 40.
Consequently,
                                  #Bh ≤ 40 ≤ 26 = C4.40,0 .
   Finally, we verify the distance bound. If h ≥ 1, every scale sequence occurring above
is one of
                            2h a,     t0 ,    t1 ,      max(t0 , t1 ).
By Proposition 2.33,
                                      dist(a, 2h a) ≤ h.
By hypothesis,
                                        dist(a, tℓ ) ≤ 1.
Moreover, since
                                 a(j − 1) ≤ tℓ (j) ≤ a(j + 1),
86                    VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

we also have
                            a(j − 1) ≤ max(t0 (j), t1 (j)) ≤ a(j + 1),
and hence
                                 dist(a, max(t0 , t1 )) ≤ 1.
     When h = 0, every scale sequence occurring above is one of
                                    t0 ,        t1 ,         max(dϵ , tℓ ).
The sequence d0 = a( · − 1) satisfies
                                              dist(a, d0 ) ≤ 1,
while d1 = a. Since both dϵ and tℓ belong to Bdist (a, 1), their pointwise maximum also
belongs to Bdist (a, 1). All these sequences belong to A by Proposition 2.31.
  It follows in all cases that
                                              ℓ
                                     dist(a, βh,b )≤1+h
Finally, by symmetry and the triangle inequality for dist,
                              0      1             0                   1
             ∆(βh,b ) = dist(βh,b , βh,b ) ≤ dist(βh,b , a) + dist(a, βh,b ) ≤ 2(1 + h),
which is (4.108).                                                                                    □
Lemma 4.41 (constant C4.40,1 ()).
                                           C4.40,1 < 53 276 < 276 .                             (4.129)
Proof (). Use C4.40,1 = 210 C4.37 and Lemma 4.38.                                                   □
Proposition 4.42 (Gaussian domination - reduction variant). Let the notation and
conclusions of Proposition 4.40 hold. For b ∈ Bh and m = (m0 , m1 ) ∈ N2 , define
                           ph,b,m = 2m0 βh,b
                                          0
                                             , 2m1 βh,b
                                                    1
                                                          ∈ A2 .
                                                        
                                                                                (4.130)
Then
                                   ∆(ph,b,m ) ≤ 2(1 + h) + |m|,                                 (4.131)
and                                              X X
                     |Nh,j (v)| ≤ C4.42 2−h/3                   2−|m|/6 Gph,b,m (j),uh,b (v).   (4.132)
                                           b∈Bh         m∈N2
where C4.42 = 2 C2.52 C4.40,1 . The series on the right-hand side converges for every v ∈ R2
                 3
                 2
        1   2
and in L (R ).
Proof (). Set
                        CG = C2.52                     and       CB = C4.40,1 .
We prove the proposition with
                                            C4.42 = 23 CG2 CB .                                 (4.133)
   Fix h ∈ N, b ∈ Bh , and m = (m0 , m1 ) ∈ N2 . Since βh,b  ℓ
                                                                 ∈ A for ℓ ∈ [2), Proposi-
tion 2.31 implies that
                                    2mℓ βh,b
                                         ℓ
                                               ∈ A.
Consequently,
                           ph,b,m = 2m0 βh,b
                                         0
                                             , 2m1 βh,b
                                                    1
                                                          ∈ A2 .
                                                        
                        NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                       87

  We first prove the distance estimate. By the triangle inequality for dist, followed by
Proposition 2.33,
                            ∆(ph,b,m ) = dist 2m0 βh,b0         1
                                                        , 2m1 βh,b
                                                                   
                                                                     .
                                       0
              ∆(ph,b,m ) ≤ dist 2m0 βh,b          1
                                         , 2m0 βh,b   + dist 2m0 βh,b 1         1
                                                                        , 2m1 βh,b
                                                                                  
                                                                                     .
                                       0    1               1
                                                              , 2m1 −m0 βh,b
                                                                           1
                                                                             
                  ∆(ph,b,m ) = dist βh,b , βh,b   + dist βh,b                   .
                ∆(ph,b,m ) ≤ ∆(βh,b ) + |m1 − m0 | ≤ ∆(βh,b ) + m0 + m1 .
Here the equality in the fourth line follows by multiplying both sequences in the first
distance by 2−m0 , and the subsequent inequality follows from
                                  dist(c, 2q c) ≤ |q|,          q ∈ Z.
Since |m| = m0 + m1 , estimate (4.108) now gives
                                  ∆(ph,b,m ) ≤ 2(1 + h) + |m|,
which is (4.131).
  We next prove the Gaussian majorant. Fix j ∈ Z and v ∈ R2 . Proposition 2.52,
applied with
                                   ℓ
                    N = 67 ,  s = βh,b (j),  x = (Wuh,b v)ℓ ,
gives, for each ℓ ∈ [2),
                        7/6
                                                 X
                                  ≤ CG 27/6             2−mℓ /6 g(2mℓ βh,b
                                                                                        
        (Wuh,b v)ℓ (β ℓ (j))                                           ℓ (j)) (Wu
                                                                                 h,b
                                                                                     v)ℓ .          (4.134)
                         h,b
                                                mℓ ∈N

All terms in these series are nonnegative. Multiplying (4.134) for ℓ = 0 and ℓ = 1, we
obtain The resulting upper bound is
                    X
           CG2 27/3     2−|m|/6 g(2m0 βh,b
                                                                                
                                       0 (j)) (Wu    v)0 g(2m1 βh,b
                                                                1 (j)) (Wu    v)1 .
                                                 h,b                      h,b
                        m∈N2

By Definition 3.5, the product of Gaussians on the right-hand side is
                                            Gph,b,m (j),uh,b (v).
Since
                                                27/3 ≤ 23 ,
it follows that
               7/6                  7/6
                                                                    X
   (Wuh,b v)0 (β 0 (j)) (Wuh,b v)1 (β 1 (j))         ≤ 23 CG2           2−|m|/6 Gph,b,m (j),uh,b (v). (4.135)
                  h,b                 h,b
                                                                m∈N2

  Applying (4.135) to every summand in (4.107), we conclude that
                                           X X
            |Nh,j (v)| ≤ 23 CG2 CB 2−h/3 ×       2−|m|/6 Gph,b,m (j),uh,b (v).
                                                     b∈Bh m∈N2

In view of (4.133), this is (4.132).
  It remains to verify the two convergence assertions. Fix h ∈ N and j ∈ Z. Since
                                0 ≤ g(s) (x) = s−1 g(s−1 x) ≤ s−1 ,
88                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

we have, for every b ∈ Bh , m ∈ N2 , and v ∈ R2 ,
                                                                                   −|m|
                    Gph,b,m (j),uh,b (v) ≤ 2m0 β10 (j) 2m1 β11 (j) = β 0 2(j)β 1 (j) .
                                                  h,b          h,b           h,b     h,b

Therefore,
                 X                                               1         X
                        2−|m|/6 Gph,b,m (j),uh,b (v) ≤     0       1
                                                                              2−7|m|/6 .
                                                          βh,b (j)βh,b (j)
                 m∈N2                                                       2 m∈N
The sum on the right is the square of a geometric series, and hence
                                                    !2
                          X                X
                              2−7|m|/6 =     2−7q/6     ≤ 22 .
                               m∈N2                     q∈N

Consequently,
                          X                                                 22
                                2−|m|/6 Gph,b,m (j),uh,b (v) ≤        0        1
                                                                                      .
                                                                     βh,b (j)βh,b (j)
                         m∈N2
where in the final line we used
                                                                X
                              2−7q/6 ≤ 2−q        and                   2−q = 2.
                                                                q∈N

Since Bh is finite, the full nonnegative series converges for every v ∈ R2 .
  Finally, since Wuh,b is unitary and every rescaled one-dimensional Gaussian has inte-
gral one,
                                      Gph,b,m (j),uh,b 1 = 1.
Consequently,
                                                                        !2
                X X                                             X
                           2−|m|/6 Gph,b,m (j),uh,b 1     = #Bh    2−q/6 .
                b∈Bh m∈N2                                                          q∈N

Writing q = 6d + r, where d ∈ N and r ∈ [6), gives
                    X          X        X
                       2−q/6 =    2−r/6     2−d ≤ 6 · 2 = 12 ≤ 24 .
                        q∈N           r∈[6)       d∈N

Thus         X X
                          2−|m|/6 Gph,b,m (j),uh,b 1          ≤ 28 #Bh ≤ 28 C4.40,0 < ∞.
             b∈Bh m∈N2
The series therefore converges absolutely in L1 (R2 ), completing the proof.                    □
Lemma 4.43 (constant C4.42 ()).
                                                123 91
                                        C4.42 < 128 2 < 291 .                              (4.136)
Proof (). Since C2.52 = eπ , the estimates e < 3 and π < 4 give
                                       e2π < e8 < 38 = 6561.
Proposition 4.40 gives C4.40,1 = 210 C4.37 . Using the exact upper bound from Lemma
4.38, and hence the bound in Lemma 4.41, the defining product is smaller than
                        23 · 6561 · 210 · 44114430494276321280 < 128
                                                                 123 91
                                                                     2 .
                    NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                        89

                                                                                       □
Lemma 4.44. Let a ∈ A and let P, (Mj )j∈Z , and (Nh,j )h∈N,j∈Z , be as in Proposi-
tion 4.40. Then for each h ∈ N and j ∈ Z, Nh,j ∈ W0 (R2 ) and
                                          ∥Nh,j ∥1 ≤ C4.44                        (4.137)
with C4.44 = 29 C4.37
Proof. Let ρh,j be as in Lemma 4.37. Then,
                                        Nh,j = Mj ∗(1,1) ρh,j .
Indeed, this follows from
                      ∗(1,1) ρh,j (ξ, η) = M
                   Mj \                    cj (ξ, η)d
                                                    ρh,j (ξ + η) = N
                                                                   dh,j (ξ, η).

using Proposition 2.13.
  By the pointwise bound on Mj , the fact that each Wu is measure preserving, and
                                  Z
                                        3/2
                                    ⟨x⟩(t) dx = 4,
                                           R
we have
                                   ∥Mj ∥1 ≤ 5 · 42 = 80.                          (4.138)
To estimate ρh,j we apply Proposition 4.37, which gives
                                                               
                        |ρh,j (x)| ≤ C4.37 ⟨x⟩2(λ− ) + ⟨x⟩2(λ+ ) .
                                                         h,j       h,j

Since                                     Z
                                                ⟨x⟩2(t) dx = 2,
                                            R
it follows that
                                   ∥ρh,j ∥1 ≤ 4C4.37
Combining this last estimate with (4.138) and the L1 convolution inequality proves
                                 ∥Nh,j ∥1 ≤ 80 · 4C4.37 ≤ C4.44 .
                                                                                       □
Lemma 4.45 (constant C4.44 ()).
                                        C4.44 < 53 275 < 275 .                    (4.139)
Proof (). Use C4.44 = 29 C4.37 and Lemma 4.38.                                        □
Proposition 4.46 (increase data - reduction variant). Let a ∈ A and let P, (Mj )j∈Z ,
and (Nh,j )h∈N,j∈Z be as in Proposition 4.40. For j ∈ Z and y ∈ (R2 )2 let
                                                          ⊗2
                                M̃h,j (y) = |Nh,j (y0 )|(σh,j )(y1 ).             (4.140)
  Then with M̃h = (M̃h,j )j∈Z ,
                                    ∥M̃h ∥M(2) ≤ C4.46 2−h/4                      (4.141)
where C4.46 = 222 C3.48 C4.42 C4.40,0
90                     VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof. By Lemma 4.44, Nh,j ∈ W0 (R2 ) and consequently |Nh,j | ∈ W0 (R2 ). Together
with Propositions 3.12 and 2.9, this gives
                                           M̃h,j ∈ W0 ((R2 )2 ).
Let Bh , uh,b , and ph,b,m be given by Lemma 4.42. For b ∈ Bh and m ∈ N2 , define
                                 αh = 2h−1/2 a, 2h−1/2 a ∈ A2
                                                        

and
                               γh,b,m = (2, (uh,b , 0), (ph,b,m , αh )) ∈ Γ.
     Since the second orientation is zero, Definition 3.11 gives
                                                             1/2 
              (sγh,b,m )1,j = s (2h−1/2 a)2 + (2h−1/2 a)2          , j = s(2h a, j) = σh,j .
Consequently,
                                                                               ⊗2
                                                                                  
             M(γh,b,m , sγh,b,m ⊗ sγh,b,m , 1) j (y) = Gph,b,m (j),uh,b (y0 ) σh,j  (y1 ).     (4.142)
Moreover, ∆(αh ) = 0 and therefore
                                        ∆γh,b,m = 1 + ∆(ph,b,m ).
     Set qn = 2 − 23−n ∈ [0, 2). By Theorem 3.48, applied with i = 1,
                                                                                 qn
                    M(γh,b,m , sγh,b,m ⊗ sγh,b,m , 1) M(2) ≤ C3.48 1 + ∆(ph,b,m ) .
     Using Lemma 4.42, Proposition 2.23, we obtain
                                  X X
         ∥M̃h ∥M(2) ≤ C4.42 2−h/3      2−|m|/6 M(γh,b,m , sγh,b,m ⊗ sγh,b,m , 1) M(2) .
                                     b∈Bh m∈N2

(first sum partial sums of the Gaussian series, then pass to the full series by Proposi-
tion 2.18 and dominated convergence). Hence, together with the estimate on #B and
(1 + ∆(ph,b,m ))qn ≤ 24 (1 + h + |m|)2 ,
                                                       X
             ∥M̃h ∥M(2) ≤ C3.48 C4.42 C4.40,0 24 2−h/3   2−|m|/6 (1 + h + |m|)2 .
                                                             m∈N2
Since                                     X
                            sup 2−h/12          2−|m|/6 (1 + h + |m|)2 ≤ 218
                             h∈N
                                         m∈N2
     it follows that
                                        ∥M̃h ∥M(2) ≤ C4.46 2−h/4 ,
as desired.                                                                                         □
Lemma 4.47 (constant C4.46 ()).
                                                 31 477
                                         C4.46 < 32 2 < 2477 .                                 (4.143)
Proof (). Use Lemmas 3.49, 4.43, and 4.38 in the defining product, together with
C4.40,0 = 26 and eπ < 56. This gives
         C4.46 < 222 · 2359 · 23 · 562 · (210 · 44114430494276321280) · 26 < 31 2477 .
                                                                     
                                                                             32
                                                                                                    □
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                91

4.3. On-diagonal from off-diagonal estimates.
Proposition 4.48 (diagonal band - reduction variant). Let a ∈ A and let P, (Mj )j∈Z
be as in Proposition 4.46. For h ∈ N with h ≥ 1 and j ∈ Z, define
                              Lh,j = Mj ∗(1,1) (Φ(2h−1 a(j)) − Φ(2h a(j)) ),               (4.144)
and for j ∈ Z,
                                L0,j = Mj ∗(1,1) (Φ(a(j−1)) − Φ(a(j)) ).                   (4.145)
Let Lh = (Lh,j )j∈Z . Then
                                            X
                                                     ∥Lh ∥M(1) ≤ C4.48                     (4.146)
                                               h∈N
               4                1/2        3
with C4.48 = 2 (C4.44 C4.46 )          + 2 C4.46 .
Proof (). Assume first that n > 2. Since n > 2 we have ν = 1. Let σh,j and Nh,j be
as Proposition 4.46. We have
                                           Lh,j = Nh,j ∗(1,1) σh,j .                       (4.147)
Indeed, by Proposition 2.13,
                       ∗(1,1) σh,j (ξ, η) = N
                   Nh,j\                    dh,j (ξ, η)d
                                                       σh,j (ξ + η) = L
                                                                      dh,j (ξ, η).

  Fix J ∈ N with J > 0 and F ∈ F. Proposition 2.27 with k = 1, applied to
                                             −1
                                       ρj = C4.44 Nh,j ,          φj = σh,j ,
gives
                               X                     2                    X
                        Λ1 (           Lh,j )(F)         ≤ C4.44 J Λ2 (       M̃h,j )(F)
                               j∈[J)                                  j∈[J)

Here
                                                             ⊗2
                                                                 
                                   M̃h,j (y) = |Nh,j (y0 )| σh,j   (y1 ),
as in Proposition 4.46.
  Proposition 4.46 and the definition of the M(2)-norm give
                                                              3−n
                             X
                        Λ2 (    M̃h,j )(F) ≤ C4.46 2−h/4 J 1−2 .
                                   j∈[J)

It follows that               X                                      1/2 −h/8 1−22−n
                       Λ1 (        Lh,j )(F) ≤ C4.44 C4.46               2    J       ,
                           j∈[J)

since 21 + 12 (1 − 23−n ) = 1 − 22−n . Taking the supremum over J and F therefore gives
                                                                    1/2 −h/8
                                  ∥Lh ∥M(1) ≤ C4.44 C4.46               2     .            (4.148)
Summing over h ∈ N finishes the proof.
  Assume now that n = 2. Now ν = 2 and
                                       Lh,j = Nh,j ∗(1,1) (σh,j ∗ σh,j )
92                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

where σh,j and Nh,j are as in Proposition 4.46. Proposition 2.28 gives
                            X                       X
                       Λ1 (    Lh,j )(F) ≤ sup Λ2 (    M̃h,j )(F̃)
                            j∈[J)                    F∈F
                                                     e
                                                                j∈[J)

with M̃h,j as in Proposition 4.46. Proposition 4.46 now gives
                                    ∥Lh ∥M(1) ≤ C4.46 2−h/4 .                          (4.149)
Summing in h ∈ N finishes the proof.                                                         □
Lemma 4.49 (constant C4.48 ()).
                                             63 480
                                     C4.48 < 64 2 < 2480 .                             (4.150)
Proof (). Using the defining sum in Proposition 4.48, Lemmas 4.45 and 4.47 bound
its first term by
                                                1/2
                              24 35 275 31
                                        32
                                           2477      < 2280 .
The second term is smaller than
                                          31 480
                                          32
                                             2 .
Since 2280 < 2−6 2480 , their sum is smaller than
                                                   63 480
                                                   64
                                                      2 .
                                                                                             □
Lemma 4.50. Let a ∈ A and suppose that (Mj )j∈Z ⊂ W0 (R2 ) satisfies for all ξ ∈ R
and j ∈ Z
                              Mcj (ξ, −ξ) = 0.                              (4.151)
Then
                          lim ∥Mj ∗(1,1) Φ(t) ∥1 = 0                        (4.152)
                                    t→∞

Proof. By Lemma 4.39,               Z
                                          Mj (x + q, q) dq = 0                         (4.153)
                                     R
for every x ∈ R. Let
                                    Rt,j = Mj ∗(1,1) Φ(t) .
Using (4.153) and changing variables q = y − p, we obtain
                  Z                                Z
                                                                             
Rt,j (x + y, y) =   Φ(t) (y − q)Mj (x + q, q) dq =    Φ(t) (y − q) − Φ(t) (y) Mj (x + q, q) dq.
                  R                                         R
It follows from the triangle inequality and Fubini’s theorem that
                                   Z
                        ∥Rt,j ∥1 ≤     ω(q/t) |Mj (x + q, q)| dx dq,
                                        R2
where                                     Z
                              ω(s) =             |Φ(z − s) − Φ(z)| dz.
                                             R
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                93

By continuity of translations and the L1 norm, ω(q/t) → 0 as t → ∞ for q ∈ R. Also,
                                             0 ≤ ω(q/t) ≤ 2∥Φ∥1 .
The claim now follows by the dominated convergence theorem.                                                      □
Proposition 4.51 (vanishing diagonal - reduction variant). Let a ∈ A and let P,
(Mj )j∈Z be as in Proposition 4.46. In addition, assume that M
                                                             cj (ξ, η) is supported in the
                     −1           −1
set where |ξ + η| ≤ 2 (a(j − 1)) . Let M = (Mj )j∈Z . Then
                                                 ∥M∥M(1) ≤ C4.48                                            (4.154)
Proof. Since |ξ + η| ≤ 2−1 (a(j − 1))−1 and Φ
                                            b = 1 on [−1/2, 1/2],
                                            Mj ∗(1,1) Φ(a(j−1)) = Mj
Let Lh,j be as in Proposition 4.48. For H ∈ N we telescope
          H
          X                                                     H
                                                                 X                             
                Lh,j = Mj ∗(1,1)           Φ(a(j−1)) − Φ(a(j)) +   (Φ(2h−1 a(j)) − Φ(2h a(j)) )
          h=0                                                            h=1

                          = Mj ∗(1,1) (Φ(a(j−1)) − Φ(2H a(j)) )
                     = Mj − Mj ∗(1,1) Φ(2H a(j)) =: Mj − RH,j .
Let J ≥ 1 and F ∈ F. By linearity and the triangle inequality,

                     X                      H
                                            X              X                            X
             |Λ1 (           Mj )(F)| ≤            |Λ1 (           Lh,j )(F)| + |Λ1 (          RH,j )(F)|
                     j∈[J)                   h=0           j∈[J)                       j∈[J)
By Propositions 2.18 and 2.24,
                        X                X           X
                  |Λ1 (   RH,j )(F)| ≤ ∥   RH,j ∥1 ≤   ∥RH,j ∥1 ,
                              j∈[J)                         j∈[J)              j∈[J)

which tends to zero as H → ∞ by Proposition 4.50.
                                        2−n
  Therefore, setting cJ = min(1, J −1+2 ),
                  X            X            X              X
         cJ |Λ1 (   Mj )(F)| ≤     cJ |Λ1 (   Lh,j )(F)| ≤   ∥Lh ∥M(1) ≤ C4.48
                  j∈[J)                    h∈N             j∈[J)                 h∈N

where the last inequality is by Proposition 4.48. Taking the supremum over J and
F ∈ F yields the claim.                                                        □
  Fix a universal pair (ϕ0 , ϕ1 ). For λ > 0 and i ∈ [2) write
                                                   ϕi,λ = (ϕi )(λ) .                                        (4.155)
Proposition 4.52. Let a ∈ A. For j ∈ Z, we set
                                      Mj = (ϕ0,a(j−1) )⊗2 − (ϕ0,a(j) )⊗2                                    (4.156)
and M = (Mj )j∈Z . Then
                                                 ∥M∥M(1) ≤ C4.52 ,                                          (4.157)
                 9
                 2
where C4.52 = 2 C4.13 .
94                   VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof. For a given J ∈ N with J > 0,
                        X
                            Mj = (ϕ0,a(−1) )⊗2 − (ϕ0,a(J−1) )⊗2 .                       (4.158)
                             j∈[J)

Let λ ∈ {a(−1), a(J − 1)}. A combination of Propositions 2.18 and 2.24 yields for any
F ∈ F,
            |Λ1 ((ϕ0,λ )⊗2 )(F)| ≤ ∥K1 ((ϕ0,λ )⊗2 )∥1 ≤ ∥(ϕ0,λ )⊗2 ∥1 = ∥ϕ0 ∥21 .       (4.159)
By Definition 4.11 and Lemma 2.43,
                            |ϕ0 (x)| ≤ 2C2.43,2 C4.13 ⟨x⟩2 = 8C4.13 ⟨x⟩2 .              (4.160)
      R
Since R ⟨x⟩2 dx = 2, we have ∥ϕ0 ∥1 ≤ 16C4.13 . Combining this with (4.158) and (4.159)
yields (4.157).                                                                      □
Lemma 4.53 (constant C4.52 ()).
                                               C4.52 = 239 .                            (4.161)
Proof (). Substitute C4.13 = 215 in the defining value 29 C4.13
                                                            2
                                                                 from Proposition 4.52. □
Lemma 4.54. Let a ∈ A. Then for any j ∈ Z,
                        F(ϕ0,a(j−1) − ϕ1,a(j) )2 = (ϕ\         2   \ 2
                                                     0,a(j−1) ) − (ϕ0,a(j) ) .          (4.162)
Proof. We have
          F(ϕ0,a(j−1) − ϕ1,a(j) )2 = (ϕ\         2                        \ 2
                                       0,a(j−1) ) − 2ϕ0,a(j−1) ϕ1,a(j) + (ϕ1,a(j) ) .
                                                      \ \                               (4.163)

Using (4.21), (4.22) and the fact that 2a(j − 1) ≤ a(j), we see that ϕ\    0,a(j−1) (ξ) = 1

           1,a(j) (ξ) ̸= 0. Thus, the right-hand side of (4.163) can be rewritten as
whenever ϕ\
                                             2       \ 2
                                   0,a(j−1) ) + (1 − ϕ1,a(j) ) − 1.
                                 (ϕ\
The conclusion follows by applying (4.24).                                                   □
Lemma 4.55. For any x ∈ R and λ, s > 0,
                                     ⟨x⟩2(λs) ≤ max{λ, λ−1 }⟨x⟩2(s)                     (4.164)
Proof. Let r = |x|/s. Then
                                         ⟨x⟩2(λs)
                                                                    2
                                                     −1       1+r
                                         ⟨x⟩2(s)
                                                    =λ        1+
                                                                 r
                                                                 λ
If λ ≥ 1, then                                          
                                         1 + r ≤ λ 1 + λr ,
so the quotient is at most λ. If 0 < λ < 1, then
                                             1 + λr ≥ 1 + r,
so the quotient is at most λ−1 .                                                             □
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                         95

Proposition 4.56 (induct positive terms - reduction variant, non-Whitney). Let a ∈ A
and let
                             Mj = (ϕ0,a(j−1) − ϕ1,a(j) )⊗2 .                 (4.165)
Then with M = (Mj )j∈Z ,
                                   ∥M∥M(1) ≤ C4.56 ,                         (4.166)
where C4.56 = C4.52 + 128 max(1, (C4.13 /2π)4 )C2.43,2
                                                2
                                                       C4.48 .
Proof. For j ∈ Z, we write Mj = M0,j + M1,j , where
                                  M0,j = (ϕ0,a(j−1) )⊗2 − (ϕ0,a(j) )⊗2
and
                M1,j = (ϕ0,a(j−1) − ϕ1,a(j) )⊗2 + (ϕ0,a(j) )⊗2 − (ϕ0,a(j−1) )⊗2 .
For i ∈ [2), we also set Mi = (Mi,j )j∈Z . By Proposition 4.52,
                                          ∥M0 ∥M(1) ≤ C4.52 .
  We proceed by estimating M1 . Using Lemma 4.54 and the fact that ϕ0 is an even
function, we deduce that for every ξ ∈ R,
                                           M1,j (ξ, −ξ) = 0.
                                           d

Let b = a/4, then b ∈ A by Proposition 2.31. If (ξ, η) ∈ R2 is such that M
                                                                         d1,j (ξ, η) ̸= 0
                                      −1  −1           −1
then |ξ + η| ≤ |ξ| + |η| ≤ 2(a(j − 1)) = 2 (b(j − 1)) .
  By Lemma 2.43, we get for i ∈ [2) and x ∈ R,
                            |ϕi (x)| ≤ 2C2.43,2 max(1, (C4.13 /2π)2 )⟨x⟩2 .
Thus, for v ∈ R2 ,
                                                h
               2
|M1,j (v)| ≤ 4C2.43,2 max(1, (C4.13 /2π)4 ) (⟨v0 ⟩2(a(j−1)) + ⟨v0 ⟩2(a(j)) )(⟨v1 ⟩2(a(j−1)) + ⟨v1 ⟩2(a(j)) )
                                                                                i
                        +⟨v0 ⟩2a(j) ⟨v1 ⟩2(a(j)) + ⟨v0 ⟩2(a(j−1)) ⟨v1 ⟩2(a(j−1)) .
Applying Lemma 4.55 and lowering all exponents to 3/2, each of the two diagonal scale
pairs occurs twice in the preceding bracket, while each off-diagonal pair occurs once.
Thus the expression is bounded by
                                           X             3/2                3/2
               2
          128C2.43,2 max(1, (C4.13 /2π)4 )     ⟨(Wu v)0 ⟩(t0 (j)) ⟨(Wu v)1 ⟩(t1 (j)) ,
                                                 (t0 ,t1 ,u)∈P

where P consists of all triples of the form (t0 , t1 , 0), where for each i ∈ [2) either
ti (j) = b(j − 1) for all j ∈ Z, or ti (j) = b(j) for all j ∈ Z. In particular, #P = 4.
Applying Proposition 4.51, we thus get
                        ∥M1 ∥M(1) ≤ 128 max(1, (C4.13 /2π)4 )C2.43,2
                                                              2
                                                                     C4.48 .
                                                                                                          □
Lemma 4.57 (constant C4.56 ()).
                                         C4.56 < 89 2541 < 2541 .                                  (4.167)
96                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof (). Use Lemma 4.53, C4.13 = 215 , C2.43,2 = 22 , and Lemma 4.49, which unfolds
the constant from Proposition 4.48. Since π > 3, the second term in the defining sum
is smaller than                                      4
                                                215
                                         211     6
                                                           63 480
                                                           64
                                                              2 = 79 2541 .
The first term is 239 < 91 2541 , which proves the claim.                                    □
Proposition 4.58 (induct positive terms - reduction variant, non-Whitney, skip terms).
Let a ∈ A and let
                           M̃j = (ϕ0,a(2j) − ϕ1,a(2j+1) )⊗2 .                  (4.168)
Then with M̃ = (M̃j )j∈Z ,
                                               ∥M̃∥M(1) ≤ C4.58 ,                       (4.169)
                1−22−n
where C4.58 = 2          C4.56 .
Proof. Let γ = (1, 0, (a, a)), then γ ∈ Γ. For j ∈ Z, we set
                                    X0,j = (ϕ0,a(2j−1) − ϕ1,a(2j) )⊗2 .
Then X = (Xi,j )i∈[1),j∈Z ∈ X1 . By Proposition 3.9, we deduce that for any j ∈ Z and
F ∈ F,
                                    Λ1 (X0,j )(F) ≥ 0.                         (4.170)
The same proposition, applied with X e0,j = M fj , also gives
                                                   fj )(F) ≥ 0.
                                               Λ1 (M
Let (Mj )j∈Z be as in Proposition 4.56 and let J ∈ N with J ≥ 1. By linearity, (4.170),
and Proposition 4.56, we get that for every F ∈ F,
                                                                2−n   2−n
                      X                  X
             0 ≤ Λ1 (    M̃j )(F) ≤ Λ1 (    Mj )(F) ≤ C4.56 21−2 J 1−2 .
                       j∈[J)                          j∈[2J)

This yields (4.169).                                                                         □
Lemma 4.59 (constant C4.58 ()).
                                           C4.58 < 98 2542 < 2542 .                     (4.171)
                                   2−n
Proof (). The factor 21−2               is at most 2. Lemma 4.57 therefore gives the displayed
estimate.                                                                                    □
Proposition 4.60 (induct positive terms - reduction variant, Whitney, with gap). Let
a ∈ A satisfy a(j) ≥ 211 a(j − 1) for every j ∈ Z. Let Mj : R2 → R be of the form
                                                 Mj = Ψ(a(j))                           (4.172)
for every j ∈ Z, where Ψ : R2 → R is a Schwartz function satisfying Ψ(v0 , v1 ) =
Ψ(v1 , v0 ) for all v = (v0 , v1 ) ∈ R2 ,
                                     Z
                                          g(v0 )g(v1 )Ψ(v) dv ≥ 0       (4.173)
                                          R2
                   NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                         97

for all bounded measurable g : R → R,
                                       b ⊂ Ann1 (1, 23 )2 ,
                                  supp(Ψ)                                         (4.174)
for m ∈ [3) and ξ ∈ R,
                                      dm b
                                      dξ m
                                           Ψ(ξ, −ξ)    ≤ 1,                       (4.175)
and for all v ∈ R2 ,
                                    1
                                    X
                           |Ψ(v)| ≤   ⟨(Wu v)0 ⟩3/2 ⟨(Wu v)1 ⟩3/2 .               (4.176)
                                      u=0
Then with M = (Mj )j∈Z ,
                                      ∥M∥M(1) ≤ C4.60 .                           (4.177)
where
                          C4.60 = 2C4.58 + 219 (C4.13
                                                 2       2
                                                      + C4.34 )C4.48 .            (4.178)
Proof (). Use Lemma 4.34 to obtain a function ψ satisfying (4.82) and (4.83). Define
α(2j) = 2−5 a(j) and α(2j + 1) = 25 a(j). Then α ∈ A. By (4.82), for each j ∈ Z,
                            2                              2
                  (a(j)) (ξ) = 2(ϕ0,α(2j) − ϕ1,α(2j+1) )(ξ) − Ψ(a(j)) (ξ, −ξ).
                 \
                 ψ               \           \                \                   (4.179)
Decompose Mj = M0,j − M1,j with
                  M0,j = Ψ(a(j)) + (ψ(a(j)) )⊗2 , M1,j = (ψ(a(j)) )⊗2 .
                P
Let J ≥ 1, M = j∈[J) Mj , and F ∈ F. The condition (4.173) and Lemma 4.32, applied
term by term, give
                                               X      
                     Λ1 (M )(F) ≥ 0,        Λ1    M1,j (F) ≥ 0.
                                                   j∈[J)

Therefore,                                       X           
                             |Λ1 (M )(F)| ≤ Λ1            M0,j (F).               (4.180)
                                                  j∈[J)

  Write M0,j = M2,j + M3,j , where
                M2,j = 2(ϕ0,α(2j) − ϕ1,α(2j+1) )⊗2 ,       M3,j = M0,j − M2,j .
Proposition 4.58 gives
                                ∥(M2,j )j∈Z ∥M(1) ≤ 2C4.58 .
It remains to estimate (M3,j )j∈Z by Proposition 4.51.
   By (4.179),
                                    M  3,j (ξ, −ξ) = 0.
                                     d
The Fourier supports of
                            Ψ,       ψ ⊗2 ,     (ϕ0,2−5 − ϕ1,25 )⊗2
are contained in Ann1 (1, 26 )2 . Hence, on the support of M
                                                           d3,j ,

                           |ξ + η| ≤ 27 a(j)−1 ≤ 2−1 a(j − 1)−1 .                 (4.181)
98                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

     Lemma 2.43 with N = 2 gives
                                      |ϕi (x)| ≤ 23 C4.13 ⟨x⟩2
for i ∈ [2). Thus, by Lemma 4.55,
                        |(ϕ0,2−5 − ϕ1,25 )⊗2 (v)| ≤ 218 C4.13
                                                         2
                                                              ⟨v0 ⟩2 ⟨v1 ⟩2 .
Using (4.83), the support bound for ψ,
                                    b and Lemma 2.43 with N = 2, we also have
                                |ψ ⊗2 (v)| ≤ 218 C4.34
                                                  2
                                                       ⟨v0 ⟩2 ⟨v1 ⟩2 .                   (4.182)
Together with (4.176), rescaling, and ⟨·⟩2 ≤ ⟨·⟩3/2 , this gives
                                             3/2             3/2         3/2     3/2
                c−1 |M3,j (v)| ≤ ⟨(W1 v)0 ⟩a(j) ⟨(W1 v)1 ⟩a(j) + ⟨v0 ⟩a(j) ⟨v1 ⟩a(j) ,
where
                                     c = 219 (C4.13
                                               2       2
                                                    + C4.34 ).
Proposition 4.51 now yields
                         ∥(M3,j )j∈Z ∥M(1) ≤ 219 (C4.13
                                                   2       2
                                                        + C4.34 )C4.48 ,
which proves the claim.                                                                       □
Lemma 4.61 (constant C4.60 ()).
                                             127 553
                                     C4.60 < 128 2 < 2553 .                              (4.183)
Proof (). Lemma 4.59 bounds the first term in (4.178) by
                                               8 543
                                               9
                                                 2 .
Lemmas 4.35 and 4.49, together with C4.13 = 215 , bound the second term by
                                      219 (230 + 254 ) 63
                                                       64
                                                          2480 .
                                            127 553
The sum of these two bounds is smaller than 128 2 .                                           □
Proposition 4.62 (induct positive terms - reduction variant, Whitney). Let a ∈ A.
Let Mj : R2 → R be of the form
                                          Mj = Ψ(a(j))                              (4.184)
                                    2
for every j ∈ Z, where Ψ : R → R is a Schwartz function satisfying Ψ(u0 , u1 ) =
Ψ(u1 , u0 ) for all u = (u0 , u1 ) ∈ R2 , and (4.173), (4.174), (4.175), (4.176). Then with
M = (Mj )j∈Z ,
                                       ∥M∥M(1) ≤ C4.62 ,                            (4.185)
where
                                         C4.62 = 11C4.60 .                          (4.186)
Proof (). For s ∈ [11), define
                                                            (s)
                         a(s) (k) = a(11k + s),          Mk = M11k+s .
Since a ∈ A,
                                                              (s)
                      a(s) (k) ≥ 211 a(s) (k − 1),        Mk = Ψ(a(s) (k)) .
                  NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                          99

Split any finite sum into these eleven residue classes and apply Proposition 4.60 to each
class. The triangle inequality gives
                               ∥M∥M(1) ≤ 11C4.60 = C4.62 .
                                                                                       □
Lemma 4.63 (constant C4.62 ()).
                                        C4.62 < 2557 .                           (4.187)
Proof (). The defining factor is 11. Lemma 4.61 gives
                                          127 553
                             C4.62 < 11 · 128 2 = 1397
                                                  2048
                                                       2557 .
                                                                                       □
Proposition 4.64 (induct positive terms - reduction variant, Whitney, product-type).
Let a ∈ A and let
                                      Mj = (ψ(a(j)) )⊗2                          (4.188)
for j ∈ Z, where ψ : R → R is a Schwartz function satisfying
                                      b ⊂ Ann1 (1, 23 ),
                                 supp(ψ)                                         (4.189)

                          |ψb(m) (ξ)| ≤ 1,      m ∈ [3),      ξ ∈ R.             (4.190)
Then, with M = (Mj )j∈Z ,
                                     ∥M∥M(1) ≤ C4.64 ,                           (4.191)
where
                                      C4.64 = 212 C4.62 .                        (4.192)
Proof (). The support in (4.189) has measure smaller than 16. Hence Lemma 2.43,
with N = 2, and (4.190) give
                                      |ψ(x)| ≤ 26 ⟨x⟩2                           (4.193)
for every x ∈ R. Set Ψ = 2−12 ψ ⊗ ψ. Then Ψ is symmetric and satisfies (4.173) and
(4.174). By (4.190), the zeroth, first, and second derivatives of ψ(ξ)
                                                                  b ψ(−ξ)
                                                                       b    are bounded
by 1, 2, and 4, respectively, so (4.175) holds for Ψ. Moreover, (4.193) gives

                          |Ψ(v)| ≤ ⟨v0 ⟩2 ⟨v1 ⟩2 ≤ ⟨v0 ⟩3/2 ⟨v1 ⟩3/2 ,
so (4.176) holds. Proposition 4.62 applied to 2−12 Mj proves the claim.                □
Lemma 4.65 (constant C4.64 ()).
                                        C4.64 < 2569 .                           (4.194)
Proof (). Use (4.192) and Lemma 4.63.                                                 □
100                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

4.4. Final reduction: proof of main theorem. In this section we prove Theorem 1.4
using Propositions 4.62, 4.64 and 4.58. Let n ≥ 2. Let f = (f0 , . . . , fn−1 ) be Schwartz
functions. Throughout this section we abbreviate
                                         A(χ) = A(χ, f ).                                (4.195)
since f will not change. We will also write
                                        At (χ) = A(χ(t) ),                               (4.196)
  Let (ϕ0 , ϕ1 ) be a universal pair and let θ, φ0,k , φ1,k , φ2,k , φ3,k , φ4,k be defined as in
(4.28)-(4.33). In what follows we denote
                                        α(n) = 1 − 2−n+2 .                               (4.197)
Lemma 4.66. Suppose that ψ : R → R is a Schwartz function with
                                 b ⊂ Ann1 (1, 22 ),
                            supp(ψ)                                                      (4.198)
and
                        |ψb(m) (ξ)| ≤ 1,       m ∈ [3), ξ ∈ R.               (4.199)
Then for every t ∈ [1, 2], J ≥ 1, and every strictly increasing sequence of integers
(kj )j∈[J) ,
                            X
                                  ∥A2kj t (ψ)∥22 ≤ C4.66 J α(n) ,            (4.200)
                                j∈[J)
where
                                         C4.66 = 24 C4.64 .                              (4.201)
Proof (). By Proposition 2.30, the finite sequence (2kj )j∈[J) extends to a sequence
a ∈ A. By Lemma 4.1 and linearity, the left-hand side equals Λ1 (Mt )(F), where
                                      X
                               Mt =       (ψ(a(j)t) )⊗2 .
                                            j∈[J)

Apply Proposition 4.64 to the corresponding initial partial sum, with 2−2 ψ(t) in place
of ψ, and multiply the resulting estimate by 24 . The Fourier support condition follows
from (4.198) and t ∈ [1, 2]. Finally,
                                              
                               dm      −2 b
                               dξ m
                                      2  ψ(tξ)   ≤ 2m−2 ≤ 1
for m ∈ [3), which verifies (4.190).                                                          □
Lemma 4.67 (constant C4.66 ()).
                                          C4.66 < 2573 .                                 (4.202)
Proof (). Use Lemma 4.65 in (4.201).                                                         □
Lemma 4.68 (Long and short variation). Let J ≥ 1 and ϕ a Schwartz function. Assume
that the function T ϕ(s) = (sϕ(s))′ satisfies (4.198) and (4.199). Suppose that A ∈
(0, ∞) is such that
                              ∥At (ϕ)∥2V2,J (t∈2Z ;L2 ) ≤ A                  (4.203)
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                       101

Then
                           ∥At (ϕ)∥2V2,J (t∈(0,∞);L2 ) ≤ 24 C4.66 J α(n) + 2A.                    (4.204)
Proof. Let (tj )j∈[J+1) be an increasing sequence of positive real numbers. By Lemma
4.3 with r = 2, a(t) = At (ϕ), and B = L2 ,
      X                            1/2   X                                    1/2
                                  2                     2
            ∥Atj+1 (ϕ) − Atj (ϕ)∥2       ≤2     ∥At (ϕ)∥V2,J (t∈[2k ,2k+1 ];L2 )      (4.205)
         j∈[J)                                          k∈κ

                                          +∥At (ϕ)∥V2,J (t∈2Z ;L2 ) ,                             (4.206)
where κ is the set of k ∈ Z such that 2k ≤ tj < 2k+1 for some j ∈ [J + 1). Fix x ∈ Rn
and k ∈ Z. Set a(t) = At (ϕ)(x) and use Lemma 4.4, specifically (4.7), to estimate
                      ∥At (ϕ)(x)∥2V2,J (t∈[2k ,2k+1 ]) ≤ ∥ta′ (t)∥2L2 (t∈[2k ,2k+1 ],dt/t) .
By Lemma 4.33,
                                                             Z 2
                             ′
                        ∥ta (t)∥2L2 (t∈[2k ,2k+1 ],dt/t) =              |A2k t (T ϕ)(x)|2 dtt .
                                                                1
Thus                                                          Z 2
                       ∥At (ϕ)(x)∥2V2,J (t∈[2k ,2k+1 ]) ≤               |A2k t (T ϕ)(x)|2 dtt .
                                                                1
Integrating over x ∈ Rn gives
                                                                Z 2
                          ∥At (ϕ)∥2V2,J (t∈[2k ,2k+1 ];L2 ) ≤             ∥A2k t (T ϕ)∥22 dtt .
                                                                    1
Using this to estimate the sum on the right in (4.205) and interchanging the sum with
the integral,
                  X                                     Z 2X
                             2
                     ∥At (ϕ)∥V2,J (t∈[2k ,2k+1 ];L2 ) ≤      ∥A2k t (T ϕ)∥22 dtt .
                    k∈κ                                             1     k∈κ
For each fixed t ∈ [1, 2], Lemma 4.66 applies because T ϕ satisfies both of its assumptions.
Since #κ ≤ J + 1,             X
                                 ∥A2k t (T ϕ)∥22 ≤ 2C4.66 J α(n) .
                                    k∈κ
The claim now follows from
    X                               X
        ∥Atj+1 (ϕ) − Atj (ϕ)∥22 ≤ 8   ∥At (ϕ)∥2V2,J (t∈[2k ,2k+1 ];L2 ) + 2∥At (ϕ)∥2V2,J (t∈2Z ;L2 )
    j∈[J)                                  k∈κ

                                          ≤ 24 C4.66 J α(n) + 2A.
                                                                                                       □
Lemma 4.69. For every J ≥ 1 and every strictly increasing sequence of integers
(kj )j∈[J) ,
                  X
                      ∥A2kj (ϕ0 ) − A2kj (ϕ1 )∥22 ≤ C4.69 J α(n) ,     (4.207)
                            j∈[J)
102                VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

where
                                        C4.69 = (2C4.13 )2 C4.66 .               (4.208)
Proof (). Apply Lemma 4.66 with t = 1 and c−1
                                            1 (ϕ0 − ϕ1 ) in place of ψ, where

                                               c1 = 2C4.13 .
The Fourier transform of ϕ0 − ϕ1 is supported in Ann1 (1, 2). By (4.23), its derivatives
through order 2 have modulus at most 2C4.13 . After division by c1 , both assumptions
of Lemma 4.66 hold, and the result follows.                                           □
Lemma 4.70 (constant C4.69 ()).
                                              C4.69 < 2605 .                     (4.209)
Proof (). Use C4.13 = 215 and Lemma 4.67 in (4.208). The squared factor is 232 , which
gives the displayed estimate.                                                        □
Lemma 4.71. For every J ≥ 1 and every strictly increasing sequence of integers
(mj )j∈[J+1) ,
                 X
                     ∥A2mj (ϕ0 ) − A2mj+1 (ϕ1 )∥22 ≤ C4.71 J α(n) ,    (4.210)
                         j∈[J)

where C4.71 = 2C4.58 .
Proof (). By Proposition 2.30, the finite sequence (2mj )j∈[J+1) extends to a sequence
a ∈ A. By Lemma 4.1, the left-hand side is
                                                          
                             X
                        Λ1       (ϕ0,a(j) − ϕ1,a(j+1) )⊗2  (F).
                                     j∈[J)

Split this sum according to the parity of j. The even terms are an initial partial sum of
the sequence in Proposition 4.58 for a, while the odd terms are such a partial sum for
the shifted sequence a(· + 1), which belongs to A by Proposition 2.31. Proposition 4.58
and the triangle inequality therefore give
                      X
                          ∥A2mj (ϕ0 ) − A2mj+1 (ϕ1 )∥22 ≤ 2C4.58 J α(n) .
                         j∈[J)

                                                                                       □
Lemma 4.72 (constant C4.71 ()).
                                         C4.71 < 98 2543 < 2543 .                (4.211)
Proof (). The defining constant is twice the constant in Proposition 4.58. Apply
Lemma 4.59.                                                                    □
Lemma 4.73. Let J ≥ 1. Then
                                 ∥At (ϕ0 )∥2V2,J (t∈2Z ;L2 ) ≤ C4.73 J α(n) ,    (4.212)
where C4.73 = 2(C4.71 + C4.69 ).
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                103

Proof. Let (kj )j∈[J+1) be a strictly increasing sequence of integers. By the triangle
inequality,
                           X                                  1/2
                                 ∥A2kj+1 (ϕ0 ) − A2kj (ϕ0 )∥22
                                  j∈[J)
         X                                      1/2       X                                        1/2
     ≤           ∥A2kj (ϕ0 ) − A2kj+1 (ϕ1 )∥22          +           ∥A2kj+1 (ϕ0 ) − A2kj+1 (ϕ1 )∥22          .
         j∈[J)                                              j∈[J)
By Lemma 4.71 and Lemma 4.69 this is
                                  1       α(n) 1    α(n) 1    α(n)
                                2          2 +C2 J 2 ≤ C2 J 2 .
                             ≤ C4.71 J         4.69      4.73

                                                                                                                 □
Lemma 4.74 (constant C4.73 ()).
                                                  11 606
                                          C4.73 < 16 2 < 2606 .                                         (4.213)
Proof (). Use Lemmas 4.70 and 4.72 in the defining sum. The first contribution after
                                    1397 606
multiplication by 2 is smaller than 2048 2 , while the second is smaller than 89 2544 . Their
                      11 606
sum is smaller than 16  2 .                                                                □
Lemma 4.75. Let J ≥ 1. Then
                               ∥At (ϕ0 )∥2V2,J (t∈(0,∞);L2 ) ≤ C4.75 J α(n) ,                           (4.214)
where
                                 C4.75 = 24 (3C4.13 )2 C4.66 + 2C4.73 .                                 (4.215)
Proof (). Let
                                   c1 = 3C4.13 .
                       −1
Apply Lemma 4.68 with c1 ϕ0 in place of ϕ and
                                           A = c−2
                                                1 C4.73 J
                                                          α(n)
                                                               .
The long variation assumption follows from Lemma 4.73. It remains to verify the two
assumptions on c−11 T ϕ0 .
   By Lemma 4.5, Td  ϕ0 is supported in Ann1 (1, 2). The identity (4.9) and (4.23) bound
all Fourier derivatives of T ϕ0 through order 2 by 3C4.13 . Hence both assumptions of
Lemma 4.68 hold after division by c1 , and that lemma gives the stated constant.       □
Lemma 4.76 (constant C4.75 ()).
                                          C4.75 < 87 2610 < 2610 .                                      (4.216)
Proof (). Use C4.13 = 215 and Lemma 4.67 in the first term of (4.215). It is smaller
than
                                    12573 610
                                    16384
                                          2 .
Lemma 4.74 bounds the second term by
                                                   11 607
                                                   16
                                                      2 .
The sum is smaller than 87 2610 .                                                                                □
104                VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Lemma 4.77. Let ψ satisfy (4.198) and (4.199). Assume also that
                                    (m)
                             |Tcψ         (ξ)| ≤ 1,      m ∈ [3),        ξ ∈ R.                (4.217)
Then
                               ∥At (ψ)∥2V2,J (t∈(0,∞);L2 ) ≤ C4.77 J α(n) ,                    (4.218)
where C4.77 = 24C4.66 .
Proof. We apply Lemma 4.68 with ϕ = ψ. The support of Tcψ is contained in the
support of ψ,
           b and the other assumption on T ψ is (4.217).
  We will show that (4.203) holds with A = 4C4.66 J α(n) , that is,
                                ∥At (ψ)∥2V2,J (t∈2Z ;L2 ) ≤ 4C4.66 J α(n) .                    (4.219)
Lemma 4.68 then gives
          ∥At (ψ)∥2V2,J (t∈(0,∞);L2 ) ≤ 24 C4.66 J α(n) + 23 C4.66 J α(n) = 24C4.66 J α(n) .
By Lemma 4.36,                                                   X
                          ∥At (ψ)∥2V2,J (t∈2Z ;L2 ) ≤ 4 sup           ∥A2kℓ (ψ)∥22 .
                                                              ℓ∈[J)
Lemma 4.66, applied with t = 1, gives (4.219) because ψ satisfies both of its assump-
tions.                                                                             □
Lemma 4.78 (constant C4.77 ()).
                                                C4.77 < 2578 .                                 (4.220)
Proof (). Lemma 4.67 and the defining factor 24 give
                                              1397 573
                                 C4.77 < 24 · 2048 2 = 4191
                                                       8192
                                                            2578 .
                                                                                                    □
Lemma 4.79. For all k ≥ −2,
                           ∥At (φ0,k )∥2V2,J (t∈(0,∞);L2 ) ≤ C4.79 2−2k J α(n) ,               (4.221)
where
                                                           2
                                            C4.79 = C4.77 C4.25,2 .                            (4.222)
Proof (). By Lemma 4.30, it suffices to prove
                             ∥At (φ3,k )∥2V2,J (t∈(0,∞);L2 ) ≤ C4.79 J α(n) .                  (4.223)
Apply Lemma 4.77 with c−1
                       1 φ3,k in place of ψ, where
                                                c1 = C4.25,2 .
By Lemma 4.22,
                          φ3,k ) ⊂ [−1, −2−2 ] ∪ [2−2 , 1] ⊂ Ann1 (1, 22 ).
                     supp(d                                                                    (4.224)
The support of T[
                φ3,k is contained in the same annulus by Lemma 4.5. Lemmas 4.23 and
4.25 show that, after division by c1 , the Fourier derivatives of both functions through
order 2 are bounded by 1. Thus all assumptions of Lemma 4.77 hold.                     □
                  NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                        105

Lemma 4.80 (constant C4.79 ()).
                                    C4.79 < 27
                                            32
                                               2658 < 2658 .                    (4.225)
Proof (). Use Lemma 4.78. Lemma 4.26 gives the exact value
                          2                                         41 41
           C4.25,2 = 1296C4.13 + 2630C4.13 + 2220 = 1391655585964 < 64 2
with C4.13 = 215 in (4.222). Hence
                                                41 2 660
                             C4.79 < 4191            2 < 27 2658 .
                                                   
                                     8192       64       32

                                                                                      □
Lemma 4.81. For every k ≤ −1,
                        ∥At (φ1,k )∥2V2,J (t∈(0,∞);L2 ) ≤ C4.81 22k J α(n) ,    (4.226)
where
                                  C4.81 = C4.77 (214 C4.13 )2 .                 (4.227)
Proof (). We have
                                          φ1,k = 2k θe(2k ) .
By Lemma 4.30, it suffices to apply Lemma 4.77 to (214 C4.13 )−1 θ. e The support as-
sumptions are (4.60) and (4.61). The finite Fourier-derivative estimates in the proof of
Lemma 4.27, together with
                               ce (m)     b(m+1)    b(m)
                              (T θ)   = −ξ θe    − mθe ,
bound the Fourier derivatives of both functions through order 2 by 214 C4.13 . Thus both
Fourier-derivative assumptions hold after the stated normalization.                   □
Lemma 4.82 (constant C4.81 ()).
                                    C4.81 < 33
                                            64
                                               2636 < 2636 .                    (4.228)
Proof (). Use Lemma 4.78 and C4.13 = 215 in (4.227). This gives
                                         4191 636
                                 C4.81 < 8192 2 < 33
                                                  64
                                                     2636 .
                                                                                      □
Lemma 4.83. Let γ = 12 . For every k ≤ −1 and every strictly increasing sequence of
integers (kj )j∈[J) ,
                      X          Z 2
                         −(1+γ)k
                        2            ∥A2kj t (φ4,k )∥22 dtt ≤ C4.83 J α(n) , (4.229)
                     j∈[J)            1


where
                                 C4.83 = 22 C4.62 C4.27,2
                                                   2
                                                          C4.7 .                (4.230)
106               VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof (). By Proposition 2.30, the finite sequence (2kj )j∈[J) extends to a sequence
a ∈ A. By Lemma 4.1 and linearity, the left-hand side equals Λ1 (M )(F), where
                        X                             Z 2
                 M=        Ψ(a(j)) ,   Ψ=2    −(1+γ)k
                                                          (φ4,k )⊗2  dt
                                                                 (t) t .
                            j∈[J)                                    1

Put
                                          c1 = 22 C4.27,2
                                                   2
                                                          C4.7 .
We apply Proposition 4.62 to c−1 1 Ψ. Symmetry, positivity, and the Fourier support
condition follow from Lemmas 4.9 and 4.29.
  By Lemma 4.27, for t ∈ [1, 2],
                            |(φ4,k )(t) (u)| ≤ 2k+1 C4.27,2 ⟨u − t2−k ⟩2 .
Lemma 4.7 therefore gives
                  |Ψ(u, v)| ≤ c1 ⟨u⟩3/2 ⟨v⟩3/2 + ⟨u + v⟩3/2 ⟨u − v⟩3/2 .
                                                                      

This proves (4.176) for c−1
                         1 Ψ.

  Write h = θ. By Lemma 4.29,
             be
                                                k −2πi2    −k ξ
                                    φ
                                    d4,k (ξ) = 2 e                h(ξ).
   b −ξ) the two translation phases cancel. Differentiating the remaining product
In Ψ(ξ,
through order 2, using t ∈ [1, 2] and the Fourier-derivative estimates in the proof of
Lemma 4.27, gives, for m ∈ [3),
                             dm b
                             dξ m
                                  Ψ(ξ, −ξ)     ≤ 24 C4.27,2
                                                     2
                                                            2(1−γ)k ≤ c1 .
Thus (4.175) holds. Proposition 4.62 proves the result.                             □
Lemma 4.84 (constant C4.83 ()).
                                             C4.83 < 2628 .                    (4.231)
Proof (). Use Lemmas 4.63, 4.28, and 4.8 in (4.230). This gives
                                            185801 628 23 628
                                    C4.83 < 262144 2 < 32 2 .
                                                                                    □
Lemma 4.85. Let γ = 12 . For every k ≤ −1 and every strictly increasing sequence of
integers (kj )j∈[J) ,
                      X         Z 2
                         (1−γ)k
                        2           ∥A2kj t (T φ4,k )∥22 dtt ≤ C4.85 J α(n) , (4.232)
                    j∈[J)             1

where, with                                                       
                               C = max C4.27,2 , C4.20,2 , C4.20,3 ,           (4.233)
we have
                                      C4.85 = 24 C4.62 C4.7 C 2 .              (4.234)
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                    107

Proof (). By Proposition 2.30, the finite sequence (2kj )j∈[J) extends to a sequence
a ∈ A. By Lemma 4.1 and linearity, the left-hand side equals Λ1 (M )(F), where
                       X                            Z 2
                 M=        Ψ(a(j)) ,   Ψ=2   (1−γ)k
                                                        (T φ4,k )⊗2  dt
                                                                 (t) t .
                            j∈[J)                              1

Let C be as in (4.233) and put
                                      c1 = 24 C 2 C4.7 .
We apply Proposition 4.62 to c−1   1 Ψ. Symmetry, positivity, and the Fourier support
condition follow from Lemmas 4.9 and 4.29.
  Directly from the definitions,
                               e − 2−k ) + 2k (Xθ)(u − 2−k ) + θ(u − 2−k ).
               T φ4,k (u) = 2k θ(u
Use order 2 in Lemmas 4.27 and 4.20 for the first and third terms, and order 3 in Lemma
4.20 for the second. Since |x|⟨x⟩3 ≤ ⟨x⟩2 , for t ∈ [1, 2] this gives
                               |(T φ4,k )(t) (u)| ≤ 22 C⟨u − t2−k ⟩2 .
Lemma 4.7 now gives
                     |Ψ(u, v)| ≤ c1 ⟨u⟩3/2 ⟨v⟩3/2 + ⟨u + v⟩3/2 ⟨u − v⟩3/2 .
                                                                         

Thus (4.176) holds for c−1
                        1 Ψ.

  Writing again h = θ,  Lemma 4.29 and Lemma 4.5 give
                     be
                                           −k
                          φ4,k (ξ) = e−2πi2 ξ 2πiξh(ξ) − 2k ξh′ (ξ) .
                                                                   
                         T[
                     b −ξ). Differentiating the remaining amplitudes through order
The phases cancel in Ψ(ξ,
2 uses h only through order 3. The finite estimates in the proof of Lemma 4.27 bound
each of those amplitude derivatives by C, and hence, for m ∈ [3),
                               dm b
                               dξ m
                                    Ψ(ξ, −ξ)   ≤ 24 C 2 2(1−γ)k ≤ c1 .
Thus (4.175) holds, and Proposition 4.62 completes the proof.                        □
Lemma 4.86 (constant C4.85 ()).
                                           C4.85 < 2630 .                      (4.235)
Proof (). Lemmas 4.28 and 4.21 give
                                        C ≤ C4.27,2 ≤ 231 .
Use this and Lemmas 4.63 and 4.8 in (4.234). The result is
                                    C4.85 < 185801
                                            262144
                                                   2630 < 32
                                                          23 630
                                                             2 .
                                                                                     □
Lemma 4.87. Let γ = 21 . For every k ≤ −1,
                      ∥At (φ4,k )∥2V2,J (t∈2Z ;L2 ) ≤ C4.87 2γk J α(n) ,       (4.236)
where
                                      C4.87 = 26 C4.62 C4.27,2
                                                        2
                                                               .               (4.237)
108                 VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Proof (). By Lemma 4.36, it suffices to estimate
                                    X
                              4 sup      ∥A2kj (φ4,k )∥22 .
                                            j∈[J)

By Proposition 2.30, the finite sequence (2kj )j∈[J) extends to a sequence a ∈ A. By
Lemma 4.1, the sum is Λ1 (M )(F) with
                                      X
                                 M=       (φ4,k )⊗2
                                                 (a(j)) .
                                                j∈[J)

Set
                                 Ψ = 2−γk φ⊗2
                                           4,k ,        c1 = 24 C4.27,2
                                                                 2
                                                                        .
We apply Proposition 4.62 to c−11 Ψ. Symmetry, positivity, and the Fourier support
condition follow from Lemmas 4.29 and 4.32.
  Put R = 2−k . We claim that
           R−3/2 ⟨u − R⟩2 ⟨v − R⟩2 ≤ 24 ⟨u⟩3/2 ⟨v⟩3/2 + ⟨u + v⟩3/2 ⟨u − v⟩3/2 .
                                                                             

If |u − R|, |v − R| < R/2, then
                                    R−3/2 ≤ (7/2)3/2 ⟨u + v⟩3/2
and
                            ⟨u − R⟩2 ⟨v − R⟩2 ≤ ⟨u − v⟩3/2 ,
so the claim follows. Otherwise, by symmetry suppose |u − R| ≥ R/2. Then
                                       ⟨u − R⟩2 ≤ 33/2 ⟨u⟩3/2
and
                           R−3/2 ⟨v − R⟩2 ≤ (3/2)3/2 ⟨v⟩3/2 .
Their product is smaller than 24 ⟨u⟩3/2 ⟨v⟩3/2 , proving the claim.
  Lemma 4.27 and the claim prove (4.176) for c−1    1 Ψ. Moreover,

                                            k −2πi2−k ξ b
                              φd4,k (ξ) = 2 e           θ(ξ).
                                                        e
                       b −ξ). Differentiating the remaining amplitudes through order
The phases cancel in Ψ(ξ,
2, and using the finite estimates in the proof of Lemma 4.27, gives, for m ∈ [3),
                                dm b
                                dξ m
                                     Ψ(ξ, −ξ)   ≤ 22 C4.27,2
                                                      2
                                                             2(2−γ)k ≤ c1 .
Thus (4.175) holds. Proposition 4.62, followed by Lemma 4.36, proves the result.      □
Lemma 4.88 (constant C4.87 ()).
                                            C4.87 < 2625 .                       (4.238)
Proof (). Use Lemmas 4.63 and 4.28 in (4.237). This gives the displayed estimate. □
Lemma 4.89. Let γ = 21 . For every k ≤ −1,
                          ∥At (φ2,k )∥2V2,J (t∈(0,∞);L2 ) ≤ C4.89 2γk J α(n) ,   (4.239)
                    1/2   1/2
where C4.89 = 27 C4.83 C4.85 + 2C4.87 .
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                                                 109

Proof. We have
                               φ2,k (u) = −(φ4,k )(2k ) (u),
so by Lemma 4.30 (rescaling) it suffices to show
                                    ∥At (φ4,k )∥2V2,J (t∈(0,∞);L2 ) ≤ C4.89 2γk J α(n)                                        (4.240)
  Let (tj )j∈[J+1) be an increasing sequence of positive real numbers. By Lemma 4.3
(with r = 2, a(t) = At (φ4,k ) and B = L2 ),
  X                                     1/2   X                                       1/2
         ∥Atj+1 (φ4,k ) − Atj (φ4,k )∥22      ≤2   ∥At (φ4,k )∥2V2,J (t∈[2ℓ ,2ℓ+1 ];L2 )      (4.241)
     j∈[J)                                                             ℓ∈L

                                               +∥At (φ4,k )∥V2,J (t∈2Z ;L2 ) .                                                (4.242)
                                                            ℓ                ℓ+1
where L is the set of ℓ ∈ Z such that 2 ≤ tj < 2        for some j ∈ [J + 1). Squaring and
             2       2     2
using (a + b) ≤ 2(a + b ) we obtain
        X                                        X
            ∥Atj+1 (φ4,k ) − Atj (φ4,k )∥22 ≤ 23   ∥At (φ4,k )∥2V2,J (t∈[2ℓ ,2ℓ+1 ];L2 ) (4.243)
         j∈[J)                                                     ℓ∈L

                                              +2∥At (φ4,k )∥2V2,J (t∈2Z ;L2 ) .                                               (4.244)
  Now we use Lemma 4.87 to estimate
                                     ∥At (φ4,k )∥2V2,J (t∈2Z ;L2 ) ≤ C4.87 2γk J α(n)                                         (4.245)
We will also show
                 X                                                                   1/2      1/2
                            ∥At (φ4,k )∥2V2,J (t∈[2ℓ ,2ℓ+1 ];L2 ) ≤ 24 C4.83 C4.85 2γk J α(n)                                 (4.246)
                      ℓ∈L

The estimates (4.246), (4.245), and (4.244) together give
                                                            1/2   1/2
         ∥At (φ4,k )∥2V2,J (t∈(0,∞);L2 ) ≤ (27 C4.83 C4.85 + 2C4.87 )2γk J α(n) = C4.89 2γk J α(n)
as desired. To see (4.246), for each ℓ ∈ Z we estimate
                                                    Z
                         2
             ∥At (φ4,k )∥V2,J (t∈[2ℓ ,2ℓ+1 ];L2 ) ≤   ∥At (φ4,k )(x)∥2V2,J (t∈[2ℓ ,2ℓ+1 ]) dx.
                                                                  Rn
             n
Fix x ∈ R and ℓ ∈ Z. Set a(t) = At (φ4,k )(x) and use Lemma 4.4 (specifically, (4.8))
to estimate for each x
                                                                                                 ′
        ∥At (φ4,k )(x)∥2V2,J (t∈[2ℓ ,2ℓ+1 ]) ≤ 23 ∥a(t)∥ 2                                 dt ∥ta (t)∥ 2               dt .
                                                                       L (t∈[2ℓ ,2ℓ+1 ],     )        L (t∈[2ℓ ,2ℓ+1 ], )
                                                                                           t                            t
By Lemma 4.33,
                                                                   Z 2
                                ′       2
                        ∥ta (t)∥ 2                          dt =             |A2ℓ t (T φ4,k )(x)|2 dtt .
                                        L (t∈[2ℓ ,2ℓ+1 ],     )         1
                                                            t
                            n
Thus for every x ∈ R and ℓ ∈ Z,
                                   ∥At (φ4,k )(x)∥2V2,J (t∈[2ℓ ,2ℓ+1 ])
                     Z 2                        1/2  Z 2                               1/2
               3   −k                       2 dt         k                           2 dt
             ≤2 2         |A2ℓ t (φ4,k )(x)| t         2         |A2ℓ t (T φ4,k )(x)| t        .
                            1                                                   1
110                       VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

We integrate over x ∈ Rn and sum in ℓ ∈ L. Then we apply the Cauchy-Schwarz
inequality in x and in the summation. We also interchange the integrals over x with
the integrals t and the summation. This gives
                             X
                                ∥At (φ4,k )∥2V2,J (t∈[2ℓ ,2ℓ+1 ];L2 )
                                           ℓ∈L

                             Z 2X                              1/2        Z 2X                                1/2
                 3       −k
           ≤2 2                         ∥A2ℓ t (φ4,k )∥22 dtt            k
                                                                         2             ∥A2ℓ t (T φ4,k )∥22 dtt          .
                              1   ℓ∈L                                        1   ℓ∈L
Order the elements of L increasingly and apply Lemmas 4.83 and 4.85 directly to the
two integrated sums. We also use #L ≤ J + 1.
                                       1/2 1/2
  This bounds the last display by 24 C4.83 C4.85 2γk J α(n) , where we used (J + 1)α(n) ≤
2J α(n) . This shows (4.246).                                                           □
Lemma 4.90 (constant C4.89 ()).
                                                 C4.89 < 23
                                                         32
                                                            2636 < 2636 .                                                   (4.247)
Proof (). The proofs of Lemmas 4.84 and 4.86 give the common factor
                                                            185801
                                                            262144
                                                                   .
Hence the first term in the defining sum is smaller than
                                                         185801 636
                                                         262144
                                                                2 .
Lemma 4.88 bounds the second term by
                                                          1397
                                                         2097152
                                                                 2636 .
Their sum is smaller than 23
                          32
                             2636 .                                                                                              □

4.4.1. Proof of Theorem 1.4.
Proof (). Fix j ∈ [J). By Lemma 4.19, ∥Atj+1 (1[0,1] ) − Atj (1[0,1] )∥L2 (Rn ) is no larger
than
                                              ∞
                                              X
          ∥Atj+1 (ϕ0 ) − Atj (ϕ0 )∥L2 (Rn ) +   ∥Atj+1 (φ0,k ) − Atj (φ0,k )∥L2 (Rn ) +
                                                           k=−2

          −1
          X                                                            −1
                                                                       X
      +          ∥Atj+1 (φ1,k ) − Atj (φ1,k )∥L2 (Rn ) +                      ∥Atj+1 (φ2,k ) − Atj (φ2,k )∥L2 (Rn ) .
          k=−∞                                                      k=−∞
Here we have also applied Lemma 4.31 to interchange series and integrals. Applying
the triangle inequality in ℓ2 ([J)) and then Lemmas 4.75, 4.79, 4.81, and 4.89, we obtain
                          X                                          1/2
                                  ∥Atj+1 (1[0,1] ) − Atj (1[0,1] )∥22
                                        j∈[J)
                                                                           
                                              1/2      1/2     1/2      1/2
                                  ≤ J α(n)/2 C4.75 + 8C4.79 + C4.81 + 8C4.89 ,
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                       111

where we used
                       ∞
                       X                         −1
                                                 X                         −1
                                                                           X
                              −k                         k
                              2     = 8,               2 = 1,                      2k/4 ≤ 8.
                       k=−2                     k=−∞                       k=−∞

Consequently,             X
                                  ∥Atj+1 (1[0,1] ) − Atj (1[0,1] )∥22 ≤ Cfinal J α(n) ,
                          j∈[J)
where                                                                   
                          Cfinal = 22 C4.75 + 26 C4.79 + C4.81 + 26 C4.89 .
Lemmas 4.76, 4.80, 4.82, and 4.90 give
               Cfinal < 78 2612 + 27
                                  32
                                     2666 + 33
                                            64
                                               2638 + 32
                                                      23 644
                                                         2 < 78 2666 < 2666 = C1.4 .
                                                                                                         □

                                      5. From real to ergodic
   The purpose of this section is to prove Theorem 1.2 from Theorem 1.4. This section
is the only place in the blueprint where we invoke two external theorems, i.e. theorems
that are not proved in this blueprint. These are Theorem 5.2 (multilinear complex in-
terpolation) and Theorem 5.5 (Calderón transference principle). The latter was recently
formalized in Lean by Pernegger [20].
Proposition 5.1 (Permutation of the endpoint estimate). Let n ≥ 2, let π be a permu-
tation of [n), and let J ≥ 1 and 0 < t0 < · · · < tJ . For real-valued Schwartz functions
(fi )i∈[n) ,
                                                                     2−n
       X                                                                 Y
             ∥Atj+1 (1[0,1] , f ) − Atj (1[0,1] , f )∥22 ≤ C1.4 J 1−2      ∥fi ∥22π(i)+min(n−π(i),2) . (5.1)
     j∈[J)                                                                 i∈[n)

Proof (). Apply Theorem 1.4 after permuting the coordinate axes by π and permuting
the functions by the same permutation. Lebesgue measure, the L2 norm, and the kernel
1[0,1] are unchanged by this coordinate permutation. The normalization in Theorem
1.4 becomes the product on the right-hand side of (5.1); homogeneity gives the stated
form.                                                                              □
External Theorem 5.2 (Multilinear interpolation). Let m, n ≥ 1 be integers, let
(Xi , µi ) and (Y, ν) be measure spaces, let p ∈ [1, ∞], and let T be an n-linear map on
n-tuples of complex-valued simple functions with values in Lp (Y ). For a ∈ [m) and
i ∈ [n), let qa,i ∈ [1, ∞], and assume
                                                              Y
                         ∥T (f0 , . . . , fn−1 )∥Lp (Y ) ≤ Aa   ∥fi ∥Lqa,i (Xi ) .  (5.2)
                                                                   i∈[n)
                      P
Let θa ≥ 0 satisfy       a∈[m) θa = 1, and define pi ∈ [1, ∞] by
                                                       X
                                                1               θa
                                                pi
                                                   =           qa,i
                                                                    .                                 (5.3)
                                                       a∈[m)
112                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

                                                                           pi
                                                             (Xi ) to Lp (Y ) and
                                                             Q
Then T extends to an n-linear map from                           i∈[n) L
                                                        Y      Y
                      ∥T (f0 , . . . , fn−1 )∥Lp (Y ) ≤   Aθaa      ∥fi ∥Lpi (Xi ) .                            (5.4)
                                                                 a∈[m)          i∈[n)

  This is a standard result in interpolation theory, see e.g. [3].
Proposition 5.3 (Range of exponents). Let pi ∈ [1, ∞] for i ∈ [n). The vector (p−1
                                                                                i )i∈[n)
belongs to the convex hull of the permutations of
                                          (2−2 , 2−3 , . . . , 2−n , 2−n )                                      (5.5)
if and only if
                                                     X
                                                             p−1  1
                                                              i = 2                                             (5.6)
                                                     i∈[n)

and, for every nonempty I ⊂ [n),
                                              X
                                                     p−1
                                                      i ≥ 2
                                                           |I|−n−1
                                                                   .                                            (5.7)
                                               i∈I

Proof (). Every permutation of (5.5) satisfies (5.6). The sum of its |I| smallest coor-
dinates is 2|I|−n−1 , so every convex combination satisfies (5.7).
  Conversely, put xi = p−1   i   and let b0 ≥ · · · ≥ bn−1 be the coordinates in (5.5) in
decreasing order. Applying (5.7) to complements gives, for every I ⊂ [n),
                                                                 |I|−1
                                                X                 X
                                                       xi ≤              bi .                                   (5.8)
                                                i∈I               i=0

Let c ∈ Rn and simultaneously relabel the coordinates of c and x so that c0 ≥ · · · ≥ cn−1 .
By summation by parts, (5.6), and (5.8),
                      X                        X                  X                           m
                                                                                              X
                             ci xi = cn−1             xi +                 (cm − cm+1 )               xi
                     i∈[n)                    i∈[n)           m∈[n−1)                          i=0


                               X               X                                m
                                                                                X            X
                     ≤ cn−1            bi +             (cm − cm+1 )                  bi =           c i bi .
                               i∈[n)          m∈[n−1)                           i=0          i∈[n)
                                                        P
The last expression is the maximum of i ci yi over the permutations y of (5.5). The
finite-dimensional separation theorem therefore places x in their convex hull.   □
Proposition 5.4 (Interpolated real-variable estimate). Let n ≥ 2, and let (pi )i∈[n)
satisfy (5.6) and (5.7). For every J ≥ 1, every 0 < t0 < · · · < tJ , and every n-tuple of
complex-valued measurable functions fi ∈ Lpi (Rn ),
                                                                             2−n
             X                                                                   Y
                 ∥Atj+1 (1[0,1] , f ) − Atj (1[0,1] , f )∥22 ≤ 22n C1.4 J 1−2      ∥fi ∥2pi . (5.9)
             j∈[J)                                                                               i∈[n)
                      NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                           113

Proof (). For fixed J and (tj )j∈[J+1) , consider the n-linear map whose value is
                                                                  
                           Atj+1 (1[0,1] , f ) − Atj (1[0,1] , f ) j∈[J)
in L2 (Rn ; ℓ2 ([J))). Proposition 5.1 gives its endpoint norm at every permutation of
(5.5). Since all endpoint exponents are finite, approximation by Schwartz functions and
the endpoint estimate extend this map uniquely to the corresponding products of real
Lp spaces. For complex inputs, expand each fi into real and imaginary parts and use
the triangle inequality. This multiplies every endpoint norm by at most 2n . Proposition
5.3 and Theorem 5.2 give (5.9) for complex-valued simple functions. Since (5.7) for
singleton sets gives pi < ∞, approximation by simple functions and the interpolated
estimate extend the map to all fi ∈ Lpi (Rn ).                                         □

       P Theorem 5.5 (Calderón transference principle). Let n ≥ 2, let pi ∈ (1, ∞)
External
satisfy i∈[n) p−1
               i  = 1/2, and let g : N → [1, ∞). Assume that for some C > 0, every
J ≥ 1, every 0 < t0 < · · · < tJ , and every real-valued fi ∈ Lpi (Rn ) satisfy
                 X                                                      Y
                    ∥Atj+1 (1[0,1] , f ) − Atj (1[0,1] , f )∥22 ≤ Cg(J)   ∥fi ∥2pi . (5.10)
                 j∈[J)                                                 i∈[n)

Then, for every measure space (X, Σ, µ), every family of mutually commuting measure
preserving transformations (Ti )i∈[n) , every real-valued fi ∈ Lpi (X), every J ≥ 1, and
every positive integers N0 < · · · < NJ ,
                  X                                             Y
                      ∥MNj+1 (f ) − MNj (f )∥22 ≤ C C5.5,n g(J)    ∥fi ∥2pi ,      (5.11)
                  j∈[J)                                               i∈[n)

where
                                           C5.5,n = 24n+6 .                             (5.12)
  This is a standard result and can be found e.g. as Theorem 2.5 of [20], up to slight
restatement with an explicit constant and the specific real-variable averages and ergodic
averages used here.
Theorem 5.6 (Ergodic jump estimate with general exponents). Let n ≥ 2, and let
(pi )i∈[n) satisfy (5.6) and (5.7). Let (X, Σ, µ) be a measure space, let (Ti )i∈[n) be mutu-
ally commuting measure preserving transformations, and let (fi )i∈[n) be complex-valued
functions with fi ∈ Lpi (X). For every J ≥ 1 and positive integers N0 < · · · < NJ ,
                                                                        2−n
                 X                                                          Y
                     ∥MNj+1 (f ) − MNj (f )∥22 ≤ C5.6,n,(pi )i∈[n) J 1−2      ∥fi ∥2pi , (5.13)
              j∈[J)                                                       i∈[n)

where
                          C5.6,n,(pi )i∈[n) = 22n C5.5,n 22n C1.4 = 28n+672 .
                                                                 
                                                                                        (5.14)
Proof (). Apply Proposition 5.4 to real-valued inputs and then Theorem 5.5 with
            2−n
g(J) = J 1−2 . This gives the factor C5.5,n in addition to the constant 22n C1.4 from
Proposition 5.4. For complex inputs, expand every fi into real and imaginary parts.
The triangle inequality in L2 (X; ℓ2 ([J))) contributes at most another factor 2n to the
operator norm. Squaring gives the factor 22n in (5.14).                               □
114                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

Theorem 5.7 (Symmetric ergodic jump estimate). Let n ≥ 2. Let (X, Σ, µ) be a
measure space, let (Ti )i∈[n) be mutually commuting measure preserving transformations,
and let (fi )i∈[n) be complex-valued functions in L2n (X). For every J ≥ 1 and positive
integers N0 < · · · < NJ ,
                                                                2−n
                    X                                               Y
                        ∥MNj+1 (f ) − MNj (f )∥22 ≤ C5.7,n J 1−2      ∥fi ∥22n , (5.15)
                   j∈[J)                                                       i∈[n)

where
                                              C5.7,n = 28n+672 .                        (5.16)
                                     −1
                           P
Proof (). We have         i∈[n) (2n)   = 1/2. If I ⊂ [n) has m ≥ 1 elements, then
                                       X
                                             (2n)−1 = 2n
                                                      m
                                                         ≥ 2m−n−1 ,
                                       i∈I
             n−m
because m2         ≥ n for 1 ≤ m ≤ n. Thus Theorem 5.6 applies.                             □
Lemma 5.8 (From jump estimates to variation). Let B be a seminormed space, let
a : N → B, let r0 ≥ 2, and let D > 0. Assume that, for every J ≥ 1 and every
0 < N0 < · · · < NJ , X
                         ∥a(Nj+1 ) − a(Nj )∥2 ≤ DJ 1−2/r0 .            (5.17)
                               j∈[J)
If r > r0 , then
                                                                       1/r
                           ∥a∥Vr (N ∈N, N ≥1;B) ≤ 21−1/r0         r
                                                                 r−r0
                                                                               D1/2 .   (5.18)
If r0 = 2, then
                                       ∥a∥V2 (N ∈N, N ≥1;B) ≤ D1/2 .                    (5.19)
Proof (). Fix 0 < N0 < · · · < NJ and write dj = ∥a(Nj+1 )−a(Nj )∥. Let d∗1 ≥ · · · ≥ d∗J
be the decreasing rearrangement. Choose the indices of the m largest dj and split them
according to the parity of j. Within either parity class the selected intervals [Nj , Nj+1 ]
are disjoint and nonadjacent. Listing their endpoints in increasing order and applying
(5.17) gives
                                 X
                                    d2j ≤ D(2|E|)1−2/r0
                                        j∈E
for either class E. Hence
                                       m(d∗m )2 ≤ 2D(2m)1−2/r0 ,
so
                                       d∗m ≤ 21−1/r0 D1/2 m−1/r0 .
Therefore, when r > r0 ,
               X                        ∞
                                        X
                    r
                   dj ≤ 2r(1−1/r0 ) r/2
                                   D      m−r/r0 ≤ 2r(1−1/r0 ) Dr/2 r−r
                                                                     r
                                                                        0
                                                                          .
                   j∈[J)                          m=1

Taking the rth root and then the supremum gives (5.18). If r0 = 2, (5.17) itself is
uniform in J and gives (5.19) directly.                                          □
                     NORM-VARIATION OF MULTIPLE ERGODIC AVERAGES                                    115

Proof of Theorem 1.2 (). Put
                                                    Y
                                       D = C5.7,n           ∥fi ∥22n .
                                                    i∈[n)

Theorem 5.7 gives (5.17) with r0 = 2n−1 . If n = 2, Lemma 5.8 gives the result for r = 2,
and the monotonicity of finite ℓr norms gives it for every r ≥ 2. If n ≥ 3 and r > 2n−1 ,
the same lemma gives
                                                 1−n         1/r 1/2 Y
           ∥MN (f )∥Vr (N ∈N, N ≥1;L2 (X)) ≤ 21−2      r
                                                     r−2 n−1     C5.7,n ∥fi ∥2n .
                                                                             i∈[n)

                                                                                                     □

                                           References
 [1] T. Austin, On the norm convergence of non-conventional ergodic averages, Ergodic Theory Dynam.
     Systems 30 (2010), 321–338.
 [2] J. Avigad and J. Rute, Oscillation and the mean ergodic theorem for uniformly convex Banach
     spaces, Ergodic Theory Dynam. Systems 35 (2015), 1009–1027.
 [3] J. Bergh and J. Löfström, Interpolation Spaces: An Introduction, Springer-Verlag, Berlin, 1976.
 [4] L. Becker, M. I. de Frutos-Fernández, L. Diedering, F. van Doorn, S. Gouëzel, A. Jamneshan,
     E. Karunus, E. van de Meent, P. Monticone, J. Mulder-Sohn, J. Portegies, J. Roos, M. Rothgang,
     R. Srivastava, J. Sundstrom, J. Tan, and C. Thiele, A blueprint for the formalization of Carleson’s
     theorem on convergence of Fourier series, arXiv:2405.06423v2, 2025.
 [5] L. Becker, F. van Doorn, A. Jamneshan, R. Srivastava, and C. Thiele, Carleson operators on
     doubling metric measure spaces, arXiv:2508.05563, 2025.
 [6] P. Durcik, V. Kovač, K. A. Škreb, and C. Thiele, Norm variation of ergodic averages with respect
     to two commuting transformations, Ergodic Theory Dynam. Systems 39 (2019), 658–688.
 [7] P. Durcik, V. Kovač, and C. Thiele, Power-type cancellation for the simplex Hilbert transform, J.
     Anal. Math. 139 (2019), 67–82.
 [8] P. Durcik, L. Slavı́ková, and C. Thiele, Local bounds for singular Brascamp–Lieb forms with
     cubical structure, Math. Z. 302 (2022), 2375–2405.
 [9] P. Durcik, L. Slavı́ková, and C. Thiele, Norm-variation of triple ergodic averages for commuting
     transformations, Anal. PDE 19 (2026), 539–586.
[10] P. Durcik and C. Thiele, Singular Brascamp–Lieb: a survey, in Geometric Aspects of Harmonic
     Analysis, Springer INdAM Ser. 45, Springer, Cham, 2021, 321–349.
[11] K. Gröchenig, Foundations of Time-Frequency Analysis, Birkhäuser, 2001.
[12] L. Hörmander, The Analysis of Linear Partial Differential Operators I: Distribution Theory and
     Fourier Analysis, second edition, Springer-Verlag, Berlin, 1990.
[13] B. Host, Ergodic seminorms for commuting transformations and applications, Studia Math. 195
     (2009), 31–49.
[14] R. L. Jones, I. V. Ostrovskii, and J. M. Rosenblatt, Square functions in ergodic theory, Ergodic
     Theory Dynam. Systems 16 (1996), 267–305.
[15] R. L. Jones, A. Seeger, and J. Wright, Strong variational and jump inequalities in harmonic
     analysis, Trans. Amer. Math. Soc. 360 (2008), 6711–6742.
[16] V. Kovač, Boundedness of the twisted paraproduct, Rev. Mat. Iberoam. 28 (2012), 1143–1164.
[17] V. Kovač, Quantitative norm convergence of double ergodic averages associated with two com-
     muting group actions, Ergodic Theory Dynam. Systems 36 (2016), 860–874.
[18] The mathlib Community, The Lean mathematical library, in Proceedings of the 9th ACM SIG-
     PLAN International Conference on Certified Programs and Proofs (CPP 2020), Association for
     Computing Machinery, New York, 2020, pp. 367–381, doi:10.1145/3372885.3373824.
116                  VAN DOORN, DURCIK, ROOS, SLAVÍKOVÁ, AND THIELE

[19] L. de Moura and S. Ullrich, The Lean 4 theorem prover and programming language, in Automated
     Deduction – CADE 28, Lecture Notes in Computer Science, vol. 12699, Springer, 2021, pp. 625–
     635.
[20] F. Pernegger, Formalisation of the Calderón Transference Principle in Ergodic Theory, Bachelor’s
     thesis, Rheinische Friedrich-Wilhelms-Universität Bonn, September 2025.
[21] T. Tao, Norm convergence of multiple ergodic averages for commuting transformations, Ergodic
     Theory Dynam. Systems 28 (2008), 657–688.
[22] M. N. Walsh, Norm convergence of nilpotent ergodic averages, Ann. of Math. 175 (2012), 1667–
     1688.
[23] N. Wiener, Tauberian theorems, Ann. of Math. 33 (1932), 1–100.

  Mathematical Institute,
University of Bonn, Endenicher Allee 60, 53115 Bonn, Germany
  Email address: vdoorn@math.uni-bonn.de

  Schmid College of Science and Technology,
Chapman University, One University Drive, Orange, CA 92866, USA
  Email address: durcik@chapman.edu

  Department of Mathematics and Statistics,
University of Massachusetts Lowell, 1 University Ave, Lowell, MA 01854, USA
  Email address: joris roos@uml.edu

  Department of Mathematical Analysis, Faculty of Mathematics and Physics,
Charles University, Sokolovská 83, 186 75 Praha 8, Czech Republic
  Email address: slavikova@karlin.mff.cuni.cz

  Mathematical Institute,
University of Bonn, Endenicher Allee 60, 53115 Bonn, Germany
  Email address: thiele@math.uni-bonn.de
