                                         AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


                                                                                 Yuanhe Zhang 1 Jason D. Lee 2 Fanghui Liu 3


                                                                    Abstract                                    benign overfitting (Bartlett et al., 2020; Tsigler & Bartlett,
                                                                                                                2023), and single/multi-index model (Montanari & Urbani,
                                                 We present the first comprehensive Lean 4 for-
                                                                                                                2025; Abbe et al., 2022; Bruna & Hsu, 2025).
                                                 malization of statistical learning theory (SLT)
                                                 grounded in empirical process theory. Our end-                 However, as models become increasingly complex, contem-
arXiv:2602.02285v2 [cs.LG] 10 Jun 2026




                                                 to-end formal infrastructure implement the miss-               porary theoretical analyses have grown substantially longer
                                                 ing contents in latest Lean library, including a               and more intricate. Modern proofs often rely on a wide
                                                 complete development of Gaussian Lipschitz con-                range of advanced mathematical tools or inspired by sta-
                                                 centration, Dudley’s entropy integral theorem                  tistical physics. This broad techniques place significant
                                                 for sub-Gaussian processes, and an application                 strain on human review (i.e., verification at scale): it be-
                                                 to least-squares (sparse) regression with a sharp              comes difficult to verify intermediate lemmas, track logical
                                                 rate. The project was carried out using a human-               dependencies, and clearly identify which techniques are ap-
                                                 AI collaborative workflow, in which humans de-                 plicable at each stage of the argument. Besides, some core
                                                 sign proof strategies and AI agents execute tac-               techniques in SLT, e.g., concentration inequalities, covering,
                                                 tical proof construction, leading to the human-                are without a structured, machine-readable library, leading
                                                 verified Lean 4 toolbox for SLT. Beyond im-                    to untapped reusability.
                                                 plementation, the formalization process exposes
                                                                                                                Formalization in interactive theorem provers such as Lean
                                                 and resolves implicit assumptions and missing
                                                                                                                4 (Moura & Ullrich, 2021) addresses both challenges and
                                                 details in standard SLT textbooks, enforcing a
                                                                                                                is rapidly gaining traction in the math community. By en-
                                                 granular, line-by-line understanding of the theory.
                                                                                                                coding proofs in a formal language, we obtain machine-
                                                 This work establishes a reusable formal founda-
                                                                                                                checkable correctness guarantees while simultaneously cre-
                                                 tion and opens the door for future developments
                                                                                                                ating a structured, queryable library of results. We argue
                                                 in machine learning theory. The code is pro-
                                                                                                                that formalizing SLT is not merely an exercise in rigor, but
                                                 vided in https://github.com/YuanheZ/
                                                                                                                a foundation for scalable, automated theoretical analysis of
                                                 lean-stat-learning-theory.
                                                                                                                machine learning systems. Current Lean 4 implementation
                                                                                                                in machine learning includes reinforcement learning theory
                                                                                                                (Zhang, 2025), optimization (Li et al., 2024; 2025a;b). The
                                         1. Introduction
                                                                                                                most close to our work is conducted by Sonoda et al. (2025)
                                         Statistical learning theory (SLT), and more generally, ma-             on generalization bounds via Rademacher complexity, but
                                         chine learning theory, successfully guided the progress of             limited to simple settings, see the discussion in Section 2.2.
                                         machine learning over the past two decades, informing foun-            Unlike more self-contained mathematical areas such as num-
                                         dational concepts such as bias-variance trade-offs, regular-           ber theory or algebra, where formalization has flourished
                                         ization, and cross-validation (Hastie et al., 2009). Now it            thanks to clean axiomatic foundations, SLT lies at the inter-
                                         tries to capture the picture for complex architectures such            section of multiple disciplines, related to empirical process
                                         as deep neural networks (LeCun et al., 2015) and large lan-            theory (Van Der Vaart & Wellner, 1996). To be specific,
                                         guage models (Brown et al., 2020) at some points, e.g., dou-           as shown in Figure 1, the excess risk of a learning algo-
                                         ble descent (Belkin et al., 2019; Mei & Montanari, 2022),              rithm is governed by the supremum of an empirical process
                                             1
                                              Department of Statistics, University of Warwick, UK               indexed by the loss class. Controlling this supremum re-
                                         (yuanhe.zhang@warwick.ac.uk). 2 EECS and Statistics, University        quires two interlocking components: concentration inequal-
                                         of California, Berkeley, USA (jasondlee@berkeley.edu). 3 School        ities (Boucheron et al., 2013) that convert high-probability
                                         of Mathematical Sciences, Institute of Natural Sciences and MOE-       bounds into link to complexity measure, and capacity con-
                                         LSC, Shanghai Jiao Tong University, China. Part of work was
                                         done at Department of Computer Science, University of Warwick,         trol that quantifies the effective size of localized function
                                         UK. Correspondence to: Fanghui Liu <fanghui.liu@sjtu.edu.cn>.          classes via complexity measure and metric entropy. Each
                                                                                                                tool demands careful treatment of measurability, integrabil-


                                                                                                            1
                          AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

                                                                           full generality of sub-Gaussian processes. The development
                                                                           required formalizing the sophisticated chaining technique
                                                                           that decomposes a stochastic process into a telescoping sum
                                                                           over dyadic approximations, along with rigorous treatment
                                                                           of covering and packing numbers in metric spaces.
                                                                           3. Application: Least-Squares Framework via Localized
                                                                           Empirical Process: We demonstrate the practical utility of
                                                                           our formalizations by developing a unified framework for
                                                                           least-squares regression based on the localized empirical
                                                                           process. We further test the functionability of our formal
                                                                           unified framework on linear regression and ℓ1 -constrained
                                                                           regression to obtain sharp rates up to minimax-level.
                                                                           4. Human-AI Collaborative Formalization Paradiagm:
                                                                           Our formalization is completed through structured collab-
                                                                           oration between human mathematicians and Claude Code
                                                                           (Anthropic, 2025a) with Opus-4.5 (Anthropic, 2025b). Hu-
                                                                           mans analyze Mathlib’s infrastructure, design proof strate-
                                                                           gies, and decompose complex theorems into manageable
Figure 1. Lean formulation for Localized Empirical Process Frame-          lemmas; the AI agent executes these plans and constructs
work. It includes the blue part for the capacity control and the red       formal proofs. The entire process totals ∼500 hours of
part for concentration. The colored zone indicates the major results       supervised development, with all formalizations compiled
in the chapters of Wainwright (2019) (High Dimensional Statistics,
                                                                           without sorry or axiom. This provides one realization of
HDS) and Boucheron et al. (2013) (Concentration Inequality, CI).
                                                                           how large-scale formalization projects can be substantially
                                                                           accelerated through well-designed human–AI collaboration.
ity, and topological assumptions that textbooks routinely
leave implicit. More importantly, these tools remain ex-                   The scale of our contribution is substantial: the project
tremely undeveloped in Lean 4.                                             comprises approximately 30,000 lines of Lean 4 code. We
                                                                           provide a list of our major formalizations in Section A. Cru-
In this work, we rise to this challenge by formalizing all in-             cially, this effort goes far beyond implementation. Achiev-
frastructures for SLT in Lean 4 from scratch via a human–AI                ing a complete formalization requires a granular, line-by-
collaboration system. Starting from basic measure-theoretic                line understanding of SLT: every definition, assumption,
probability and analysis, we systematically develop the full               inequality, and logical dependency must be explicitly identi-
stack of tools required for modern generalization analysis.                fied, verified, and composed into a coherent proof structure.
The dependency structure, illustrated in Figure 1, reveals
our formalization path, including several key parts of repre-              This makes the project particularly valuable for student
sentative books (Wainwright, 2019; Boucheron et al., 2013).                training in theoretical machine learning. Engaging with the
Our contributions are:                                                     formalization demands mastery of the full technical stack of
                                                                           SLT rather than superficial familiarity. By providing a rigor-
1. Implementation on Gaussian Lipschitz Concentration:                     ous, end-to-end formal infrastructure for SLT grounded in
We construct a complete formal development of Gaussian                     the empirical process, this work offers a principled training
Lipschitz concentration which requires building a substan-                 ground and opens the door for students seeking to develop
tial infrastructure across Efron-Stein inequality, Gaussian                deep theoretical competence in modern machine learning.
Poincaré inequality, Density argument, and Gaussian log-
arithmic Sobolev inequality (LSI). The Gaussian LSI, in
particular, is a foundational tool in high-dimensional proba-
                                                                           2. SLT from Natural Language to Lean 4
bility with far-reaching applications beyond learning theory.              In this section, we take an overview of the structure of SLT
To our knowledge, this constitutes the first formalization of              in natural language and diagnose what are missing or should
the complete Gaussian analysis tools in any theorem prover.                be built in Lean 4.

2. Implementation on Dudley’s Entropy Integral: We                         2.1. Statistical learning theory for generalization
provide the first formalization of Dudley’s entropy integral
theorem for sub-Gaussian processes in Lean 4. This is a cor-               Empirical process theory provides a unified uniform conver-
nerstone result in empirical process theory that bounds the                gence framework for generalization guarantees of learning
expected supremum of a stochastic process by an integral in-               algorithms by exploiting the geometry of function classes.
volving metric entropy. Our formalization encompasses the

                                                                       2
                          AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

As shown in Figure 1, formally, let F be a hypothesis class          First, the required concentration machinery in this project
and ℓf (z) be a loss function associated with f ∈ F. For a           is substantially more advanced. While McDiarmid-type in-
broad class of empirical risk minimization and regularized           equalities suffice under boundedness assumptions, localized
learning procedures, the excess risk of an estimator fˆ admits       analysis relies on Gaussian Lipschitz concentration, whose
                                                                     proof draws on a deep chain of results from functional anal-
R(fˆ) − R(f ⋆ ) ≲ sup (P̂ − P)(ℓf − ℓf ⋆ ) +(confidence) ,           ysis and probability theory, that requires formulation or
                   f ∈F
                   |               {z                  }             significant changes in Lean 4.
                       empirical process fluctuation
                                                                     Second, the capacity control has quite limited formulation
where P and P̂ denote the population and empirical mea-              in latest Lean library. Formalizing localization requires de-
sures, respectively. This decomposition highlights that gen-         veloping covering numbers, chaining arguments underlying
eralization is governed by the uniform deviation of an em-           Dudley’s integral, localized complexity measures, and the
pirical process indexed by the excess loss class. The global         fixed-point analysis that determines the critical radius.
structure of this framework includes two main parts via
several probabilistic toolbox (see Figure 1).                        Our work bridges precisely this gap via the comprehen-
                                                                     sive Lean 4 formalization. Importantly, this effort goes far
Concentration: High-probability bounds on the empirical              beyond mechanical translation. Natural-language proofs
process fluctuation can be obtained via concentration in-            routinely suppress measurability and topological assump-
equalities, such as Gaussian Lipschitz concentration (Wain-          tions, conflate almost-sure and pointwise statements, and
wright, 2019, Corollary 14.15). These yield bounds in the            compress multi-step arguments into informal phrases. For-
form of critical radius δ⋆ .                                         malization forces each of these gaps to be made explicit
Capacity Control: The key to obtain δ⋆ is localization:              and resolved. Moreover, Lean demands careful proof en-
rather than controlling the empirical process over the entire        gineering: for example, formulazation of Dudley’s entropy
class F, one restricts attention to a localized class F(δ) =         integral requires systematic coordination between different
{f ∈ F : d(f, f ⋆ ) ≤ δ} consisting of functions within              notions of integration (e.g., Bochner and interval integrals),
radius δ of the optimum with respect to a suitable metric d.         which are distinct in Lean but mixed in language proofs.

The effective size of F(δ) is quantified by localized com-
plexity measures, e.g., Gaussian complexity Gn (F(δ))
                                                                     3. Formulation details and challenges
and Rademacher complexity Rn (F(δ)). Their connec-                   In this section, we present the details of our formalization
tion to geometry is made explicit through metric entropy,            (see Figure 2), covering Gaussian Lipschitz concentration
log N (F(δ), ϵ, d) defined via covering numbers: how many            in Section 3.1 and Dudley’s entropy integral bound in Sec-
balls of radius ϵ are needed to cover F(δ). In particular,           tion 3.2. For clarity, we first state each result in natural-
chaining arguments, most notably Dudley’s entropy inte-              language theorem form, followed by the corresponding Lean
gral, relate localized Gaussian complexity to metric entropy:        4 formalization, where we explicitly discuss the key model-
                          Z 2δ p                                     ing and proof-engineering challenges.
                        1
      Gn (F(δ)) ≲ √               log N (ϵ, F(δ), d) dϵ .
                         n 0                                         3.1. High-Dimensional Gaussian Analysis Toolbox
This characterization reveals how complexity accumulates             Gaussian functional inequalities are the backbone of HDS
across scales and leads to a solution set whose smallest so-         and SLT. However, the complete proofs form a long chain
lution defines the critical radius δ⋆ . The resulting bounds         of disparate methods. Each link relies on a different piece
recover sharp minimax rates in parametric settings and ex-           of analysis, and each is nontrivial to formalize. We build a
tend naturally to nonparametric models.                              reusable, deliberately end-to-end formal toolbox that sup-
                                                                     ports the full analytic pipeline from scratch, see the red part
2.2. Formalization Gaps                                              of Figure 2 with the following steps.

Despite the theoretical maturity of the above framework, its         Theorem 3.1 (i. Efron-Stein’s Inequality, Theorem 3.20
formalization in Lean 4 remains in its infancy. Recent work          in Boucheron et al. (2013)). Let X = (X1 , ... , Xn )
by Sonoda et al. (2025) formalizes generalization bounds             be a vector of n independent random variables and
via Rademacher complexity, including basic tools such as             Z = f (X) be a square-integrable function of X. De-
McDiarmid’s inequality and Hoeffding’s lemma. However,               note E (i) as the conditional expectation conditioned on
their analysis controls the empirical process over the entire        (X1 , ... , Xi−1 , Xi+1 , ... , Xn ). Then,
function class, leading to loose rates and limited applica-                                n             2 
tions. The sharper localized empirical process frame-
                                                                                           X
                                                                                Var(Z) ≤     E Z − E(i) [Z]     .
work goes beyond this in two folds:                                                         i=1

                                                                 3
                                 AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


                                          Sub-Gaussian Process                                                                     Application
    Covering Number
                                                                         Dudley
                                                                                                     Gaussian Complexity            Linear
                                                                                                                                   Covering
                                                        Metric Entropy
                              Chaining


                                                                                                                                     Linear
                                                                                                                                    Entropy
                                                                                                                                    Integral
     Efron-Stein          Gaussian Poincaré              Gaussian LSI
                                                                                                      Master Error Bound
                                                                         Gaussian Lipschitz
                                                                          Concentration                                            Sharp Rate


                      Density Arguments
                                                                                                                                Linear Regression




  Figure 2. The dependency graph of our formalizations. All the contents in the graph have not been implemented in Lean 4 before.


We start with formalizing E (i) as follows:                                           measure-theoretic tracking through bounded continuous
noncomputable def condExpExceptCoord (i :
                                                                                      function wrappers and coordinate-permutation symmetry.
    Fin n) (f : (Fin n → Ω) → R) : (Fin                                               Notice that such machinery is frequent in Gaussian analysis.
    n → Ω) R→ R :=
                                                                                      We formalize Corollary 3.2 as:
  fun x =>   y, f (Function.update x i y) ∂
    (µs i)                                                                            theorem gaussianPoincare {f : R → R} (hf
                                                                                          : CompactlySupportedSmooth f) :
Implementation challenge: Theorem 3.1 allows each Xi to                                   variance (fun x => f x)
                                                                                          stdGaussian.toMeasure ≤
have a distinct distribution µi , which complicates measure-                              R
                                                                                            x, (deriv f x)ˆ2 ∂
theoretic arguments for coordinate-wise updates. We ad-                                   stdGaussian.toMeasure := by
dress this by formalizing a universal transfer lemma: re-
sampling one coordinate with a fresh independent sample
preserves the joint distribution. Though requiring extra for-                         iii. Density Arguments: The density arguments provide
malization of measure-theoretic machinery (measure rectan-                            an efficient tool which let people prove inequalities for
gles), this lemma powers 20+ usages across tower properties,                          smooth and compactly supported function class Cc∞ (easier
Fubini-style swapping, and slice integrability.                                       to apply convergence theorems) then extend to general class
                                                                                      by such argument. This is the key to: 1) extend Gaussian
Then, we can formalize Theorem 3.1 as:
                                                                                      LSI from Cc∞ to C 1 , and 2) extend Gaussian Lipschitz con-
theorem efronStein (f : (Fin n → Ω) → R)                                              centration from Cc∞ to the general Lipschitz class. Such
    (hf : MemLp f 2 µs ) :                                                            arguments are often skipped in textbooks (Boucheron et al.,
    variance f µs ≤ Σ i : Fin n,
                                  R
                                    x, (f x                                           2013) due to the complexity. We start with defining the
    - condExpExceptCoord (µs := µs) i f
    x)ˆ2 ∂µs := by                                                                    membership of Gaussian Sobolev space1 W 1,2 (γ ⊗n ) as:
                                                                                      def MemW12Gaussian (n : N) (f : E n → R)
                                                                                          (γ : Measure (E n)) : Prop :=
ii. Gaussian Poincaré Inequality: To formalize Gaussian                                MemLp f 2 γ ∧ MemLp (fun x 7→ fderiv R f
Poincaré inequality, we need to use Efron-Stein’s infrastruc-                            x) 2 γ
tures and require a series of results as below.
                                                                                      and the squared Gaussian Sobolev norm as:
Corollary 3.2. Let X be a standard Gaussian random vari-
able and f ∈ Cc∞ (R). Then, Var[f (X)] ≤ E f ′ (X)2 .                                 noncomputable def GaussianSobolevNormSq (n
                                                                                          : N) (f : E n → R) (γ : Measure (E
Notice that Corollary 3.2 is not directly used to derive the                              n)) : R≥0∞ :=
                                                                                        eLpNorm f 2 γ ˆ 2 + eLpNorm (fun x 7→ ∥
Gaussian LSI, instead its intermediate proof is re-used.
                                                                                          fderiv R f x∥) 2 γ ˆ 2
Implementation challenge: Formalizing the Corollary 3.2
combines Taylor expansion bounds with weak convergence                                    1
                                                                                            Here f should be continuously differentiable which ensures
of Rademacher sums to Gaussian, which needs careful                                   the derivative is well-defined so we can use fderiv from Lean 4.

                                                                                  4
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

The main density theorem is provided by:                            By defining the entropy Ent(f ) as
Theorem 3.3. The space of smooth compactly supported
                                                                     Ent(f ) = E [f (X) log f (X)] − E[f (X)] log E[f (X)] ,
functions Cc∞ is dense in W 1,2 (γ ⊗n ), where γ is the stan-
dard Gaussian measure.                                              with its formulation,
This can be used to extend Gaussian LSI to C 1 class with           def entropy (µ : Measure Ω) (f : Ω → R) :
the following Lean 4 formulation.                                     R R :=                      R
                                                                        ω, f ω R* log (f ω) ∂µ - ( ω, f ω ∂µ)
theorem                                                                 * log ( ω, f ω ∂µ)
dense_smooth_compactSupport_W12Gaussian :
  ∀ f : E n → R, MemW12Gaussian n f                                 now we formalize Theorem 3.5 as:
    (stdGaussianE n) →
  Differentiable R f →                                              theorem gaussian_logSobolev_W12_pi {n : N}
  Continuous (fun x => fderiv R f x) →                                  {g : (Fin n → R) → R}
  ∀ ε > 0, ∃ g : E n → R, ContDiff R (⊤ :                             (hg : MemW12GaussianPi n g
    N∞) g ∧ HasCompactSupport g ∧                                       (stdGaussianPi n)) (hg_diff :
    GaussianSobolevNormSq n (f - g)                                     Differentiable R g) (hg_grad_cont : ∀
    (stdGaussianE n) < ENNReal.ofReal ε :=                              i, Continuous (fun x => partialDeriv i
    by                                                                  g x)) (hg_log_int : Integrable (fun x =
                                                                        > (g x)ˆ2 * log ((g x)ˆ2))
Remark: stdGaussianPi is the product measure of                         (stdGaussianPi n)) :
                                                                      entropy (stdGaussianPi n) (fun x => (g
n independent standard Gaussians, with its pushforward                              R
                                                                        x)ˆ2) ≤ 2 *   x, gradNormSq n g x ∂
stdGaussianE to Euclidean space via the equivalence.                    (stdGaussianPi n) := by
To extend the concentration theorem, we need a specialized
density lemma based on the Lipschitz mollification tech-            where gradNormSq is the squared norm of gradients.
nique. In our formalization, we pick a nonnegative mollifier        In the next, we briefly present the high-level proof strat-
ρ ∈ Cc∞ (Rn ) with ρ(x) dx = 1 then define a smooth
                     R
                                                                    egy for formalization. We first formalize one-dimensional
approximation to Lipschitz function f via                           case and generalize to dimension-free via tensorization later.
                                                                    Now let ε1 , ... , εn be n independent Rademacher random
          ρϵ (x) = ϵ−n ρ(x/ϵ) ,     fϵ := f ∗ ρϵ .       (1)
                                                                    variables and Pfix f ∈ Cc2 (R). Define the Rademacher sum
                                                                             −1/2      n
Notice that fϵ lives within Cc∞ (Rn ) and preserves the Lips-       Sn := n            k=1 εk , building upon the infrastructures in
chitz constant of f . The lemma is presented as:                    Theorem 3.1, we use Taylor’s limit and CLT to obtain
Lemma 3.4. Let f :RRn → R be a Lipschitz function, there                   X n     
                                                                                                1 − εk
                                                                                                             
                                                                                                                       1 + εk
                                                                                                                              2
is a constant Cρ := ∥u∥2 ρ(u) du < ∞ such that                        lim       E f Sn + √                − f Sn − √
                                                                     n→∞                            n                      n
                                                                           k=1
               sup |fϵ (x) − f (x)| ≤ LCρ ϵ .                                ′      2
                                                                                       
                                                                      = 4E f (X) , X ∼ N (0, 1) .                                (2)
              x∈Rn

Hence, fϵ → f uniformly as ϵ ↓ 0.                                   For f ∈ Cc2 (R), by CLT, we can obtain

                                                                                lim Ent f 2 (Sn ) = Ent[f (X)2 ] .
                                                                                                
Our formalization of Lemma 3.4 is:                                                                                              (3)
                                                                                n→∞
theorem mollify_tendsto_of_lipschitz {f :
    E n → R} {L : R≥0} (hf :
                                                                    We then bridge Eq. (2) and Eq. (3) by formalizing the
    LipschitzWith L f) (x : E n) :                                  Bernoulli logarithmic Sobolev inequality (LSI) (Boucheron
  Filter.Tendsto (fun ε => mollify ε f x)                           et al., 2013, Theorem 5.1) then taking limit to both sides,
    (nhdsWithin 0 (Set.Ioi 0)) (nhds (f                             we can derive the 1D Gaussian   LSI for f ∈ Cc2 (R), i.e.
    x)) := by                                                                         ′
                                                                            2              2
                                                                                             
                                                                    Ent(f ) ≤ 2E f (X) .

Implementation challenge: We formalize a large amount               Remark: For the proof of Gaussian Lipschitz concentra-
of smooth approximation and convolutions in this part,              tion, we can directly tensorize this Cc2 (R) version to be
which is an integration of functional analysis with measure-        dimension-free. We further use Theorem 3.3 to extend the
theoretic probability theory.                                       above inequality from to C 1 (R) for a general toolbox.
Theorem 3.5 (iv. Gaussian LSI, Theorem 5.4 of                       Since Gaussian LSI is a direct consequence of entropy
(Boucheron et al., 2013)). Let X = (X1 , ... , Xn ) be a vec-       subadditivity and one-dimensional case of LSI, we need
tor of n independent standard Gaussian random variables             the formulation of the subadditivity of entropy theorem
and f : Rn → R be a continuously differentiable     function        (Boucheron et al., 2013, Theorem 4.22), the key technique
with E[f ′ (X)] < ∞. Then,Ent(f 2 ) ≤ 2E ∥∇f (X)∥22 .
                                                        
                                                                    of tensorization.

                                                                5
                          AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

Theorem 3.6 (subadditivity, Theorem 4.22 of (Boucheron                3.2. Dudley’s Entropy Integral Bound
et al., 2013)). Let X = (X1 , ... , Xn ) be a vector of n inde-
                                                                      Dudley’s bound is the canonical bridge to link covering
pendent random variables and Y = f (X) be a nonnegative
                                                                      number with complexity measures. A formal proof of the
measurable function of X such that Φ(Y ) = Y log Y is in-
                                                                      general Dudley’s bound thus supplies a foundational, widely
tegrable. Define Ent(i) (Y ) as the conditional entropy given
                                                                      reusable theorem that supports a broad range of theoreti-
(X1 , ... , Xi−1 , Xi+1 , ... , Xn ). Then,
                                " n              #                    cal results. Textbook statements (Boucheron et al., 2013;
                                 X                                    Vershynin, 2018; Wainwright, 2019) typically have incom-
               Ent(Y ) ≤ E            Ent(i) (Y ) .                   plete hypotheses such as skipping integrability or hiding the
                               i=1                                    constant. Our formalization uses the following statement.
The formalization follows from similar telescoping strategy           Theorem 3.8 (Dudley’s Entropy Integral Bound). Let
in Theorem 3.1 and our formalization of duality formula               (A, d) be a pseudo-metric space and s ⊆ A a totally
                                                                      bounded set with diameter at most D > 0. Let {Xt }t∈s be
        Ent(Y ) = sup E [Y (log T − log E(T ))] ,                     a normalized sub-Gaussian process with parameter σ > 0,
                      T
                                                                      which has integrable exponential-moment for increments
where the supremum is over all integrable and nonnegative
                                                                      and continuous sample paths on s, assume that the entropy
random variables.
                                                                      integral is finite. Then,
theorem entropy_subadditive (f : (Fin n →
                                                                                               √   Z Dp
                                                                                       
    Ω) → R) (hf_meas : Measurable f)
    (hf_nn : 0 ≤m [µs ] f) (hf_int :                                       E sup Xt ≤ 12 2σ ·              log N (ε, s, d) dε ,
                                                                              t∈s                    0
    Integrable f µs ) (hf_log_int :
    Integrable (fun x => f x * log (f x)) µs                          where N (ε, s) denotes the ε-covering number of s.
    ) :
  LogSobolev.entropy µs f ≤ Σ i : Fin n,
                                          R
                                                                      The formalization of Theorem 3.8 is given by:
    x, condEntExceptCoord (µs := µs) i f x
    ∂µs := by                                                         theorem dudley {µ : Measure Ω}
                                                                          [IsProbabilityMeasure µ] {X : A → Ω →
Theorem 3.7 (v. Gaussian Lipschitz Concentration,                         R} {σ : R} (hσ : 0 < σ) (hX :
Theorem 5.6 of (Boucheron et al., 2013)). Let X =                         IsSubGaussianProcess µ X σ) {s : Set
                                                                          A} (hs : TotallyBounded s) {D : R} (hD
(X1 , ... , Xn ) be a vector of n independent standard Gaus-              : 0 < D) (hdiam : Metric.diam s ≤ D)
sian random variables and f : Rn → R be a L-Lipschitz                     (t0 : A) (ht0 : t0 ∈ s) (hcenter : ∀ ω,
function. Then, for any t > 0,                                            X t0 ω = 0) (hX_meas : ∀ t, Measurable
                                                                          (X t)) (hX_int_exp : ∀ t s : A, ∀ l : R
                                                  t2
                                                    
     P (|f (X) − E [f (X)]| ≥ t) ≤ 2 exp − 2 .                            , Integrable (fun ω => Real.exp (l *
                                                 2L                       (X t ω - X s ω))) µ) (hfinite :
                                                                          entropyIntegralENNReal s D ̸= ⊤) (hcont
We formalize Theorem 3.7 as:                                              : ∀ ω, Continuous (fun (t : ↾s) => X
theorem gaussian_lipschitz_concentration                                R t.1 ω)) :
                                                                          ω, ⊔ t ∈ s, X t ω ∂µ ≤ (12 *
    {f : (EuclideanSpace R (Fin n)) → R}
                                                                          Real.sqrt 2) * σ * entropyIntegral s D
    {L : R≥0} (hn : 0 < n) (hL : 0 < L)
                                                                          := by
    (hf : LipschitzWith L f) (t : R) (ht :
    0 < t) :
  let µ := stdGaussianE                                               We build dudley totally from scratch. We start with ϵ-nets:
                      R n
  (µ {x | t ≤ |f x -    y, f y ∂µ                                     def IsENet {A : Type*} [PseudoMetricSpace
    |}).toReal ≤ 2 * exp (-tˆ2 / (2 * (L :                                A] (t : Finset A) (eps : R) (s : Set
    R)ˆ2)) := by                                                          A) S
                                                                             : Prop :=
                                                                        s ⊆    x ∈ t, closedBall x eps
We briefly describe the proof strategy. We formalize the
Herbst argument for fϵ defined in Eq. (1). For any λ ∈ R,             We then define the covering number N (ϵ , s , d) as the
we apply the Theorem 3.5 to the function eλfϵ (X)/2                   minimal cardinality of an ϵ-net:
                                 2   λ2 L2 h λfϵ (X) i                def coveringNumber {A : Type*}
 Ent(eλfϵ ) ≤ 2E ∇eλfϵ (X)/2 ≤             E e         .                  [PseudoMetricSpace A] (eps : R) (s :
                                 2     2                                  Set A) : WithTop Nat :=
By differential inequality (we formalize as Gronwall-type               sInf {n : WithTop Nat | ∃ t : Finset A,
ratio bound) and taking limit by Lemma 3.4, we can obtain                 IsENet t eps s ∧ (t.card : WithTop
                                       λ2                               Nat) = n}
        log E exp λ(f (X) − Ef (X)) ≤          L2 ,
                                             2                        We then define the metric entropy as the logarithm of the
completing the proof of Theorem 3.7 via Chernoff’s bound.             covering number, with appropriate handling of edge cases:

                                                                  6
                        AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

def metricEntropy (eps : R) (s : Set A) : R                            Dudley’s bound with entropyIntegral for user-friendly
     :=                                                                downstream use without loss of generality.
  match coveringNumber eps s with
  | ⊤ => 0
  | (n : N) => if n ≤ 1 then 0 else                                    4. Application: Least Squares Framework
    Real.log n
                                                                       In this section, building on Wainwright (2019, Chapter 13),
Taking the square root of entropy, denoted sqrtEntropy                 we present our formalization of the least-squares framework,
from metricEntropy, we formulate the entropy integral                  including linear regression (Section 4.1) and ℓ1 -constrained
via a two-level design. The canonical definition uses ex-              regression following Raskutti et al. (2011) (Section 4.2).
tended non-negative reals:                                             Both rely on localized capacity control via covering num-
                                                                       bers, leveraging the infrastructure developed in Section 3.
def entropyIntegralENNReal (s : Set A) (D
                                                                       To present clearly, we follow Wainwright’s approach to
  R −: R) : R≥0∞ :=
       eps in Set.Ioc 0 D, ENNReal.ofReal                              focus on the prediction error, which has a direct translation
     (sqrtEntropy eps s)                                               to excess risk via Wainwright (2019, Corollary 14.15).

A real-valued wrapper entropyIntegral extracts the                     Problem Setup. Consider the nonparametric regression
toReal component under finiteness hypothesis.                          model yi = f ∗ (xi ) + σwi for i = 1, . . . , n, where
                                                                          i.i.d.
Next, we formalize sub-Gaussian processes via moment                   wi ∼ N (0, 1). Given a hypothesis class F, the empirical
                                                                                                             Pn
generating function bounds, i.e.                                       risk minimizer is fˆ := argminf ∈F n1 i=1 (f (xi ) − yi )2 .
                                                                       Our goal is to control the prediction error ∥fˆ − f ∗ ∥2n :=
def IsSubGaussianProcess (µ : Measure Ω)                               1
                                                                          Pn ˆ              ∗      2
    (X : A → Ω → R) (σ : R) : Prop :=                                  n    i=1 (f (xi ) − f (xi )) .
  ∀ s t : A, ∀ l : R, µ[fun ω => exp (l *
    (X s ω - X t ω))] ≤
                                                                       We encapsulate this setup in a RegressionModel structure
    exp (lˆ2 * σˆ2 * (dist s t)ˆ2 / 2)                                 and formalize the ERM property:
                                                                       structure RegressionModel (n : N) (X :
The chaining argument constructs a hierarchy of ε-nets                     Type*) where
at dyadic scales εk = D · 2−k , encapsulated in our                      x : Fin n → X; f_star : X → R; σ : R;
                                                                           hσ_pos : 0 < σ
DyadicNets structure. The key technique is a tele-                       noiseDistribution : Measure (Fin n → R)
scoping decomposition: for any u ∈ TK , we write                           := stdGaussianPi n
Xu − Xt0 as a base term from the coarsest net plus in-
          PK−1
crements k=0 (Xπk+1 (u) − Xπk (u) ) through successive                 def isLeastSquaresEstimator (y : Fin n → R
projections πk . Applying finite maximum bounds for                        ) (F : Set (X → R)) (x : Fin n → X)
                                                                           (f_hat : X → R) : Prop :=
sub-Gaussian processes to each increment and summing
                                                                         f_hat ∈ F ∧ ∀ f ∈ F, Σ i, (y i - f_hat
yields a bound  in terms of the dyadic sum RK (s, D) :=                    (x i))ˆ2 ≤ Σ i, (y i - f (x i))ˆ2
PK−1 p
   k=0 kε   log N (εk , s, d).
The proof then proceeds through two limit arguments. First,            Localization. We define the shifted class F ∗ := {f − f ∗ :
we extend from finite nets to a countable dense sequence via           f ∈ F } and assume it is star-shaped: 0 ∈ F ∗ and αh ∈ F ∗
Fatou’s lemma. Since Fatou requires nonnegative integrands             for all h ∈ F ∗ and α ∈ [0, 1]. The localized Gaussian
but the supremum may be negative, we introduce a shift                 complexity at radius δ is
function that cancels in expectation. Second, we extend to
the uncountable set s by exploiting path continuity which
                                                                                                                         
                                                                                                             n
concludes the target. We present a detailed formalization                                                 1X
                                                                              Gn (F(δ)) := Ew  sup             wi g(xi )  . (4)
                                                                                                                         
proof in three stages at Section B.                                                                g∈F ∗ n i=1
                                                                                                  ∥g∥n ≤δ
Implementation challenge: Lean 4 has two integration        for-
malisms: the nonnegative improper integral − for
                                                R
                                                      R≥0∞
                                                                       Main Results. The central bridge to link prediction error
and the interval integral for real-valued functions. − is tech-
                                                    R

nically convenient for measure-theoretic arguments such as             with Eq. (4) is the critical inequality Gn (Fδ (δ)) ≤ 2σ
                                                                                                                              δ
                                                                                                                                . Next,
Fubini above, but it lives in R≥0∞, so every real-valued               we use Theorem 3.7 to formalize the master error bound
bound requires ofReal/toReal conversions and extra side                (Wainwright, 2019, Theorem 13.5).
conditions. Real-valued inequalities are far smoother in               Theorem 4.1 (Master error bound, Theorem 13.5 of (Wain-
R, such as taking limit and integration. Hence we de-                  wright, 2019)). Suppose F ∗ is star-shaped, let δ∗ be the
fine the entropy integral canonically in ENNReal, but state            smallest positive solution to critical inequality which is the

                                                                   7
                        AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

critical radius. Then, for any t ≥ δ∗ , we have                     our goal is to upper bound the covering number. Then, we
                                                                    formalize the following Euclidean reduction
       P ∥f − f ∗ ∥2n ≥ 16tδ∗ ≤ exp(−ntδ∗ /2σ 2 ) .
                               
                                                                         log N (ϵ, F (δ), ∥ · ∥n ) ≤ log N (ϵ, B2r (δ), ∥ · ∥2 ) ,
To obtain δ∗ , we need to derive an upper bound on Eq. (4),         where B2r (δ) is the ℓ2 ball of radius δ on Rr . We then
then the critical inequality in terms of entropy integral be-       formalize the covering number bound on ℓ2 ball (Vershynin,
comes solvable. Therefore, we make use of Theorem 3.8 to            2018, Corollary 4.2.11).
formalize the following capacity control:
                                                                    Theorem 4.4. The covering numbers of ℓ2 ball of radius R
Theorem 4.2. For any star-shaped class F ∗ , we have                on Rι satisfy for any ϵ > 0:
                √ Z
              24 2 2δ p                                                                                 
                                                                                                             2R
                                                                                                                ι
  Gn (F(δ)) ≤ √             log N (ϵ, F(δ), ∥ · ∥n ) dϵ .                      N (ϵ, B2ι (R), ∥ · ∥2 ) ≤ 1 +       .
                 n 0                                                                                          ϵ

Remark: Due to the page limit, we present the Lean details          theorem coveringNumber_euclideanBall_le
of Theorems 4.1 and 4.2 in Section C.                                 {R eps : R} (hR : 0 ≤ R)
                                                                      (heps : 0 < eps) :
This reduces the problem to bounding covering numbers,                ((coveringNumber eps (euclideanBall R :
which we demonstrate in two applications to verify the                  Set (EuclideanSpace R ι))).untop
functionality of our framework and shape the formalization              (ne_top_of_lt
standard for covering calculus.                                         (coveringNumber_lt_top_of_totallyBounded
                                                                        heps (euclideanBall_totallyBounded
                                                                        R))) : R) ≤ (1 + 2 * R / eps) ˆ
4.1. Linear Regression                                                  Fintype.card ι := by
We consider the linear regression case (n ≥ d) where the                                           p
                                                                    Therefore, we can get δ∗ = O( r/n) then apply Theo-
ground truth model is yi = ⟨θ, xi ⟩ + σwi associated with
                                                                    rem 4.1 to conclude Theorem 4.3.
the linear predictor class F = {f (·) = ⟨θ, ·⟩ : θ ∈ Rd }
formalized as linearPredictorClass. We apply the
general framework to obtain the following rate theorem.             4.2. High-Dimensional ℓ1 Regression
Theorem 4.3. Let X ∈ Rn×d be the design matrix, define              We consider the ℓ1 -constrained regression (equivalent to
r := rank(X). Then, for the linear predictor class F,               Lasso), which allows for d > n case. The function class is
                                                                    FR = {f (·) = ⟨θ, ·⟩ : θ ∈ B1d (R)} where B1d (R) is ℓ1 -ball
                          σ2 r
                              
     P ∥fˆ − f ∗ ∥2n ≤ C1        ≥ 1 − exp (−C2 r) ,                of radius R on Rd . Following the setting in Raskutti et al.
                           n                                        (2011), the key of deriving rate is the Euclidean covering of
                                                                    ℓ1 -convex hull. We formalize this bound as:
for some constants C1 , C2 > 0.
                                                                    Lemma 4.5. Assume√X is normalized column-wise to have
Our formalization is:                                               ℓ2 norm bounded by n. For any ϵ > 0.
theorem linear_minimax_rate_rank (hn : 0 <                                             √                          2  2
                                                                     N ϵ, absconv1 (X/ n; R), ∥ · ∥2 ≤ (2d + 1)⌈R /ϵ ⌉ ,
                                                                                                    
    n)
  (M : RegressionModel n (EuclideanSpace R                                            √                √
    (Fin d))) (hf_star : M.f_star ∈                                 where absconv1 (X/ n; R) := {Xθ/ n : ∥θ∥1 ≤ R}.
    linearPredictorClass d) (hr : 0 <
    designMatrixRank M.x) (f_hat : (Fin n →                         The empirical covering follows log N (ϵ, FR (δ), ∥ · ∥n ) ≲
                                                                    R2
                                                                                                       p
     R) → (EuclideanSpace R (Fin d) → R
                                                                     ϵ2 log d, which can admit the O(R log d/n)-rate. The
    )) (hf_hat : ∀ w,                                               implementation challenge of Lemma 4.5 arises from the
    isLeastSquaresEstimator (M.response w)
    (linearPredictorClass d) M.x (f_hat
                                                                    need of Maurey’s argument, see more details in Section D.
    w)) :
  ∃ C1 C2 : R, C1 > 0 ∧ C2 > 0 ∧                                    5. Human-AI Collaborative Formalization
    (stdGaussianPi n {w | (empiricalNorm n
    (fun i => f_hat w (M.x i) - M.f_star                            In this section, we distill three transferable methodological
    (M.x i)))ˆ2 ≤ C1 * M.σˆ2 *
    (designMatrixRank M.x) / n}).toReal ≥                           contributions and one critical observation from ∼500 hours
    1 - exp (-C2 * (designMatrixRank M.x))                          of supervised development, supported by ∼60 preserved
    := by                                                           task specifications. We further classify the declarations in
                                                                    our library by the degree of human intervention required
where designMatrixRank is r. We briefly present the                 and provide a quantitative breakdown. A self-contained
formalization strategy. We apply Theorem 4.2 to F then              practical recipe is provided in Section E.

                                                                8
                            AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

5.1. Structured Specification Protocol                                      Table 1. Percentage of formalized declarations by level of human
                                                                            intervention.
We empirically find that unstructured instructions without
explicit infrastructure pointers fail roughly 70% of the time.
                                                                             Level                      Description             Percentage
We reduce the first-attempt failure rate to roughly 15%via a
structured TASK.md document with four components:                            Autonomous               AI proves alone             ∼15%
                                                                             Sketch-Guided          AI fills tactic details       ∼30%
                                                                             Specified         AI proves under full NL proof      ∼40%
  1. Target statement. Besides the exact Lean signature to                   Human-critical          Human intervenes             ∼15%
     be proved, we also need to provide the self-contained
     natural language.

  2. Infrastructure pointers. Names and file paths of lo-
     cally available lemmas the proof is expected to invoke2 .              5.3. Verification of Statement’s Consistency
                                                                            The most dangerous failure mode we encountered is not a
  3. Formalization-oriented proof plan. A detailed step-
                                                                            failed proof but a successful proof of a false statement: a
     by-step plan phrased in tactic-level language rather
                                                                            Lean term that type-checks against a misformalized goal. In
     than purely informal mathematics.
                                                                            our library we caught three such cases that had survived mul-
  4. Hard boundaries. Soft boundaries for agent to follow.                  tiple rounds of AI’s self-judgment: (i) A false “gap” bound
     See details in Section E.                                              requiring control of N (ε)/N (2ε), which is not implied by
                                                                            TotallyBounded; (ii) An impossible disjunction false
                                                                            for specific parameter ranges; (iii) A Riemann rectangle
5.2. Iterative Specification Evolution                                      used as an upper bound on a non-monotone integrand.
A single structured TASK.md is rarely correct on the first                  In each case the agent persistently reported sorry and
attempt for nontrivial proofs. We consistently observe that                 proposed progressively more aggressive structural rewrites;
retrying with the same spec essentially never succeeds; each                only a human, by constructing explicit counterexamples,
failure surfaces a distinct ambiguity left implicit by the                  detected that the statement was wrong. We therefore rec-
human, and the productive response is to refine the spec.                   ommend: (i) human review of every target statement before
We illustrate this on the density extension of the Gaussian                 proof attempts, (ii) counterexample checking for any non-
logarithmic Sobolev inequality (GLSI) from Cc∞ to W 1,2 ,                   trivial inequality, and (iii) treating a persistent sorry as a
which required four spec iterations:                                        signal to re-verify the statement, not merely the proof.

   • v1 (vague strategy). Hand-waves entropy lower-                         5.4. Quantitative Breakdown
     semicontinuity as “a Fatou-type argument”. The agent
     fails because Mathlib’s Fatou demands nonnegative                      By tracing each formalized declaration back to its author-
     integrands, while t log t goes negative on (0, 1).                     ing specification, we partition our library into four levels
                                                                            of human intervention (Table 1). The Specified tier dom-
   • v2 (dependencies). Adds infrastructure pointers to the                 inates: in our experience the bottleneck is rarely tactical
     relevant convergence lemmas but leaves the negativity                  proof construction (which the agent handles well) but rather
     issue unresolved. persistently reports sorry.                          the explicit articulation of a proof that textbooks compress
                                                                            into a single sentence. The Human-critical tier captures the
   • v3 (decomposition). Factors out the gradient conver-                   non-delegable verification cases above and a small number
     gence sub-argument into its own lemma, narrowing the                   of theorems whose initial mathematical strategy was flawed
     remaining obstacle to entropy convergence alone.                       and required human-driven re-architecture.

   • v4 (trick, domain, API). Closes the argument with the                  6. Conclusion
     shift trick and type domain switch. The agent succeeds
     on the first attempt.                                                  We present the first large-scale Lean 4 formalization of SLT-
                                                                            approximately 30,000 lines of verified code building all
More details of each specification can be found in Section F.               infrastructures from scratch through human-AI collabora-
The agent’s failures are informative: they precisely localize               tion. The developed Lean 4 formulation framework includes
what the human left implicit, rendering the collaboration                   the high-dimensional Gaussian analysis toolbox and Dud-
convergent rather than open-ended.                                          ley’s entropy integral toolbox, which deepens mathematical
                                                                            understanding and open the door to formulation of modern
   2
       This part might not be needed for the current frontier models.       machine learning theory.

                                                                        9
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

Acknowledgment                                                        In Advances in Neural Information Processing Systems,
                                                                      pp. 1877–1901, 2020.
Y. Z. was supported by Warwick Chancellor’s International
Scholarship. JDL acknowledges support of Open Philan-               Bruna, J. and Hsu, D. Survey on algorithms for multi-index
thropy, NSF IIS 2107304, NSF CCF 2212262, ONR Young                   models. arXiv preprint arXiv:2504.05426, 2025.
Investigator Award, NSF CAREER Award 2144994, and
NSF CCF 2019844. F. L. was supported by Warwick-SJTU                Daras, G., Dean, J., Jalal, A., and Dimakis, A. Intermedi-
seed fund. We thank Zulip3 for the project organization tool          ate layer optimization for inverse problems using deep
and Sulis4 for computation resources.                                 generative models. In Meila, M. and Zhang, T. (eds.),
                                                                      Proceedings of the 38th International Conference on Ma-
Impact Statement                                                      chine Learning, volume 139 of Proceedings of Machine
                                                                      Learning Research, pp. 2421–2432. PMLR, 18-24 Jul
This paper presents work whose goal is to advance the field           2021. URL https://proceedings.mlr.press/
of Lean 4 for Machine Learning Theory. There might be                 v139/daras21a.html.
some potential societal consequences of our work, none
which we feel must be specifically highlighted here.                Hastie, T., Tibshirani, R., and Friedman, J. The Elements of
                                                                      Statistical Learning: Data Mining, Inference, and Predic-
                                                                      tion. Springer Series in Statistics. Springer, New York,
References
                                                                      2nd edition, 2009.
Abbe, E., Adsera, E. B., and Misiakiewicz, T. The merged-
  staircase property: a necessary and nearly sufficient con-        LeCun, Y., Bengio, Y., and Hinton, G. Deep learning. nature,
  dition for sgd learning of sparse functions on two-layer            521(7553):436–444, 2015.
  neural networks. In Conference on Learning Theory, pp.
 4782–4887. PMLR, 2022.                                             Li, C., Wang, Z., He, W., Wu, Y., Xu, S., and Wen, Z.
                                                                      Formalization of complexity analysis of the first-order
Anthropic. Claude code, 2025a. URL https://                           optimization algorithms. CoRR, 2024.
  github.com/anthropics/claude-code. Ac-
  cessed: 2026-01-27.                                               Li, C., Wang, Z., Bai, Y., Duan, Y., Gao, Y., Hao, P., and
                                                                      Wen, Z. Formalization of algorithms for optimization
Anthropic.     System Card: Claude Opus 4.5,                          with block structures. arXiv preprint arXiv:2503.18806,
  2025b.     URL http://www.anthropic.com/                            2025a.
  claude-opus-4-5-system-card.      Accessed:
  2026-01-27.                                                       Li, C., Xu, S., Sun, C., Zhou, L., and Wen, Z. Formal-
                                                                      ization of optimality conditions for smooth constrained
Bartlett, P. L., Long, P. M., Lugosi, G., and Tsigler, A.             optimization problems. arXiv preprint arXiv:2503.18821,
  Benign overfitting in linear regression. Proceedings of             2025b.
  the National Academy of Sciences, 117(48):30063–30070,
  2020.                                                             Mei, S. and Montanari, A. The generalization error of
                                                                     random features regression: Precise asymptotics and the
Belkin, M., Hsu, D., Ma, S., and Mandal, S. Reconciling              double descent curve. Communications on Pure and
  modern machine-learning practice and the classical bias–           Applied Mathematics, 75(4):667–766, 2022.
  variance trade-off. Proceedings of the National Academy
  of Sciences, 116(32):15849–15854, 2019.                           Montanari, A. and Urbani, P. Dynamical decoupling of
                                                                     generalization and overfitting in large two-layer networks.
Boucheron, S., Lugosi, G., and Massart, P. Concen-                   In The Thirty-ninth Annual Conference on Neural Infor-
  tration Inequalities: A Nonasymptotic Theory of                    mation Processing Systems, 2025.
  Independence. Oxford University Press, 02 2013.
  URL       https://doi.org/10.1093/acprof:                         Moura, L. d. and Ullrich, S. The lean 4 theorem prover and
  oso/9780199535255.001.0001.                                        programming language. In International Conference on
                                                                     Automated Deduction, pp. 625–635. Springer, 2021.
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D.,
  Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,             Pisier, G. Probabilistic methods in the geometry of banach
  Askell, A., et al. Language models are few-shot learners.           spaces. In Probability and Analysis: Lectures given at the
   3
   https://zulip.com/                                                 1st 1985 Session of the Centro Internazionale Matematico
   4
   https://warwick.ac.uk/research/rtp/sc/                             Estivo (CIME) held at Varenna (Como), Italy May 31–
sulis/                                                                June 8, 1985, pp. 167–241. Springer, 2006.

                                                               10
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

Raskutti, G., Wainwright, M. J., and Yu, B. Minimax rates
  of estimation for high-dimensional linear regression over
  ℓq -balls. IEEE transactions on information theory, 57
  (10):6976–6994, 2011.
Sonoda, S., Kasaura, K., Mizuno, Y., Tsukamoto, K., and
  Onda, N. Lean Formalization of Generalization Er-
  ror Bound by Rademacher Complexity. arXiv preprint
  arXiv:2503.19605, 2025.
Tsigler, A. and Bartlett, P. L. Benign overfitting in ridge
  regression. Journal of Machine Learning Research, 24
  (123):1–76, 2023.

van der vaart, A. and Wellner, J. Weak Convergence
  and Empirical Processes: With Applications to Statis-
  tics. Springer Series in Statistics. Springer New York,
  2013. URL https://books.google.co.uk/
  books?id=zdDkBwAAQBAJ.
Van Der Vaart, A. W. and Wellner, J. A. Weak conver-
  gence. In Weak convergence and empirical processes:
  with applications to statistics, pp. 16–28. Springer, 1996.
Vershynin, R. High-Dimensional Probability: An Introduc-
  tion with Applications in Data Science. Cambridge Series
  in Statistical and Probabilistic Mathematics. Cambridge
  University Press, 2018.
Wainwright, M. J. High-Dimensional Statistics: A Non-
 Asymptotic Viewpoint. Cambridge Series in Statistical
 and Probabilistic Mathematics. Cambridge University
 Press, 2019.

Zhang, S. Towards formalizing reinforcement learning the-
  ory. arXiv preprint arXiv:2511.03618, 2025.




                                                                11
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

A. List of Key Results
Our formalization library contains more than 1000 theorems/lemmas. In this section, we aim to present the major results of
our formalizations and provide an exact reference to locate the statement. The list is shown in Table 2.
                        Table 2. List of our key formalization results with exact reference from textbooks.

                                     Name                                    Reference
            coveringNumber_lt_top_of_totallyBounded                          Vershynin (2018, Remark 4.2.3)
                          isENet_of_maximal                                  Vershynin (2018, Lemma 4.2.6)
                coveringNumber_euclideanBall_le                              Vershynin (2018, Corollary 4.2.13)
                     coveringNumber_l1Ball_le                                Daras et al. (2021, Theorem 2)
                  subGaussian_finite_max_bound                               Wainwright (2019, Exercise 2.12)
                                 dudley                                      Boucheron et al. (2013, Corollary 13.2)
                               efronStein                                    Boucheron et al. (2013, Theorem 3.1)
                           gaussianPoincare                                  Boucheron et al. (2013, Theorem 3.20)
                             han_inequality                                  Boucheron et al. (2013, Theorem 4.1)
                            entropy_duality                                  Boucheron et al. (2013, Theorem 4.13)
                          entropy_duality_T                                  Boucheron et al. (2013, Remark 4.4)
                        entropy_subadditive                                  Boucheron et al. (2013, Theorem 4.22)
                       bernoulli_logSobolev                                  Boucheron et al. (2013, Theorem 5.1)
                    gaussian_logSobolev_W12_pi                               Boucheron et al. (2013, Theorem 5.4)
                        lipschitz_cgf_bound                                  Boucheron et al. (2013, Theorem 5.5)
               gaussian_lipschitz_concentration                              Boucheron et al. (2013, Theorem 5.6)
                local_gaussian_complexity_bound                              Wainwright (2019, (5.48) Gaussian Case)
                         master_error_bound                                  Wainwright (2019, Theorem 13.5)
                  gaussian_complexity_monotone                               Wainwright (2019, Lemma 13.6)
                     linear_minimax_rate_rank                                Wainwright (2019, Example 13.8)
                   bad_event_probability_bound                               Wainwright (2019, Lemma 13.12)
                 l1BallImage_coveringNumber_le                               Raskutti et al. (2011, Lemma 4, q = 1)


B. Dudley’s Formalization Proof Details
The chaining argument requires constructing a hierarchy of ε-nets at geometrically decreasing scales. We encapsulate this in
the DyadicNets structure, which provides for each level k a finite set Tk ⊆ s that is an εk -net of s, where εk = D · 2−k
is the dyadic scale at level k. For the proof to succeed, we need “good” dyadic nets satisfying the cardinality bound
|Tk | ≤ N (εk+1 , s, d). This relates the net size at level k to the covering number at the finer scale εk+1 = εk /2, which is
essential for bounding the expected maximum of sub-Gaussian increments at each level later.
Another critical chaining is the dyadic approximation of the entropy integral. Define the dyadic sum
                                                          K−1
                                                          X            p
                                          RK (s, D) :=          εk ·       log N (εk , s, d) .
                                                          k=0

This sum approximates the entropy integral via a Riemann-like discretization at geometrically spaced points.
Furthermore, the chaining argument requires defining a sequence of approximations π0 (u), π1 (u), . . . , πK (u) = u through
the net hierarchy for each point u in the finest net TK . There are two natural approaches:
Direct projection: Standard presentations (Boucheron et al., 2013; Vershynin, 2018) define πk (u) as the nearest point in Tk
to the original point u. The triangle inequality then gives
                                                                                                     3
                        d(πk (u), πk+1 (u)) ≤ d(πk (u), u) + d(u, πk+1 (u)) ≤ εk + εk+1 =              εk .
                                                                                                     2

Recursive projection: An alternative, used in van der vaart & Wellner (2013); Wainwright (2019), defines πk (u) as the
nearest point in Tk to πk+1 (u), i.e. the coarser approximation is chosen to approximate the finer one, not the original point.

                                                                12
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

For u ∈ TK :                                     (
                                                      u                                     if k = K
                                    πk (u) =
                                                      nearest point in Tk to πk+1 (u)       if k < K

Our formalization uses the recursive projection, which yields a tighter constant. Since πk+1 (u) ∈ Tk+1 ⊆ s and Tk is
an εk -net of s, we have d(πk (u), πk+1 (u)) ≤ εk directly, without the factor of 3/2. This improvement from 32 εk to εk
propagates through the proof. While modest at each level, it accumulates to a noticeable reduction in the final constant.
Then, the formal proof of dudley proceeds in three stages:

B.1. Stage 1
The first stage establishes a bound for the expected supremum over a finite net. For the net TK at level K, our target is to
prove
                                                               √
                                                         
                                      E sup (Xu − Xt0 ) ≤ 6 2σ · RK+1 (s, D) .
                                              u∈TK

For any u ∈ TK , we write
                                                                          K−1
                                                                          X
                               Xu − Xt0 = (Xπ0 (u) − Xt0 ) +                      (Xπk+1 (u) − Xπk (u) ) ,
                                                                          k=0

where πk denotes the recursive projection to level k. The first term is the base term from the coarsest net, and the sum
captures the increments as we move through finer nets.
For the base term, using the finite maximum bound for sub-Gaussian processes, we have
                                                           
                                                                     p
                                      E sup (Xπ0 (u) − Xt0 ) ≤ σϵ0 · 2 log |T0 | ,
                                              u∈TK


                                                   √ D of t0 . The cardinality bound |T0 | ≤ N (ε1 , s) allows us to express
since all points in the level-0 net are within distance
this as the first term of RK+1 (s, D) scaled by 2 2σ.
For the increment terms, the key observations are that these increments have distance at most εk by the recursive projection
bound, and that the number of distinct pairs (πk (u), πk+1 (u)) is at most |Tk+1 | since πk+1 (u) ∈ Tk+1 determines the pair.
Applying the finite maximum bound produces a bound of the form:
                                                                
                                                                            p
                                 E sup (Xπk+1 (u) − Xπk (u) ) ≤ σεk · 2 log |Tk+1 | .
                                        u∈TK


By the cardinality boundness of “good” nets, we sum over k and re-index to obtain
                                   "          K−1
                                                                              #
                                              X
                               E       sup           (Xπk+1 (u) − Xπk (u) )
                                    u∈TK
                                              k=0
                                    K−1
                                    X                p                            √
                                ≤            σεk ·       2 log N (εk+2 , s, d) ≤ 4 2σ · RK+1 (s, D) .
                                       k=0


B.2. Stage 2
This stage extends the bound from finite nets to the countable supremum over a dense sequence (tn )n∈N in s, where Fatou’s
lemma enters. For convenience, we work in normalized sub-Gaussian settings (Xt0 ≡ 0) without loss of generality. The
central challenge is that Fatou’s lemma requires nonnegative integrands, but the supremum YK := supu∈TK Xu may be
negative. We resolve this by introducing a shift function

                                                          g(ω) := inf XπK (t0 ) (ω)
                                                                  K∈N


                                                                     13
                        AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

where πK (t0 ) denotes the projection of t0 onto TK . With shift function in hand, we define ZK := YK − g ≥ 0. Fatou’s
lemma gives                                    h          i
                                             E lim inf ZK ≤ lim inf E[ZK ].
                                                  K→∞              K→∞

By path continuity and sequence density, lim inf K ZK = supn∈N Xtn − g. Since E[ZK ] = E[YK ] − E[g], the E[g] cancels:
                                                          √                 
                                   E sup Xtn ≤ lim inf 6 2σ · RK+1 (s, D) .
                                           n∈N          K→∞


The final step shows
                                                                Z Dp
                                    lim inf RK+1 (s, D) ≤ 2 ·           log N (ε, s, d) dε .
                                       K                           0
                                                                                                p
The approximation RK (s, D) ≤ 2 · (entropy integral) + 2 · (tail) holds, where the tail is εK    log N (εK , s) → 0 as K → ∞.
Taking lim inf eliminates the tail, yielding:
                                                         √ Z Dp
                                                
                                        E sup Xtn ≤ 12 2 ·              log N (ε, s, d) .
                                            n∈N                    0


B.3. Stage 3
This stage converts the supremum over the uncountable set s to the countable supremum over the dense sequence. Since s
is totally bounded in (A , d), it is separable, so there exists a countable dense sequence (tn )n∈N ⊆ s. By the sample path
continuity, for each ω the map t 7→ Xt (ω) is continuous on s. Since the supremum of a continuous function over a set
equals its supremum over any dense subset, we have

                                                  sup Xt (ω) = sup Xtn (ω) .
                                                  t∈s           n∈N


Combining this with the bound from the second stage gives
                                                    √     Z Dp
                                            
                                  E sup Xt ≤ 12 2σ ·          log N (ε, s, d) dε
                                           t∈s                     0

completing the proof.

C. Lean 4 Formalization of Least Squares
In this section, we present more implementation details of Theorem 4.1 and Theorem 4.2. We aim to show that the
formalization exposes and resolves implicit assumptions missed in standard textbooks, enforcing a granular understanding
of the theory.

C.1. Master Error Bound
First, the complete formalization of Theorem 4.1 is:
theorem master_error_bound (hn : 0 < n)
  (M : RegressionModel n X) (F : Set (X → R)) (hF_star : M.f_star ∈ F) (δ_star : R) (hδ
    : 0 < δ_star)
  (hCI : satisfiesCriticalInequality n M.σ δ_star (shiftedClass F M.f_star) M.x)
  (hH_star : IsStarShaped (shiftedClass F M.f_star))
  (t : R) (ht : δ_star ≤ t) (f_hat : (Fin n → R) → (X → R))
  (hf_hat : ∀ w, isLeastSquaresEstimator (M.response w) F M.x (f_hat w))
  (hne : (empiricalSphere n (shiftedClass F M.f_star) (Real.sqrt (t * δ_star))
    M.x).Nonempty)
  (hint_u : Integrable (fun w => ⊔ h ∈ localizedBall (shiftedClass F M.f_star) (Real.sqrt
    (t * δ_star)) M.x, |(n : R)−1 * Σ i, w i * h (M.x i)|) (stdGaussianPi n))
  (hint_δ : Integrable (fun w => ⊔ h ∈ localizedBall (shiftedClass F M.f_star) δ_star
    M.x, |(n : R)−1 * Σ i, w i * h (M.x i)|) (stdGaussianPi n))

                                                              14
                        AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

  (hbdd : ∀ w : Fin n → R, BddAbove {y | ∃ h ∈ localizedBall (shiftedClass F M.f_star)
    (Real.sqrt (t * δ_star)) M.x, y = |(n : R)−1 * Σ i, w i * h (M.x i)|}) :
  (stdGaussianPi n {w | (empiricalNorm n (fun i => f_hat w (M.x i) - M.f_star (M.x i)))ˆ2
    ≤ 16 * t * δ_star}).toReal ≥ 1 - exp (-n * t * δ_star / (2 * M.σˆ2)) := by

Now we will introduce the technical hypotheses:

hCI: The chosen radius δ > 0 should satisfy the critical inequality. This is used to control the probability of the bad event
in bad_event_probability_bound, which is a standard proof need as Wainwright (2019, Lemma 13.2).

hH_star:     The shifted class is star-shaped. The need follows similar reason to hCI.

hne:    The empirical sphere is non-empty. The bad event is defined in terms of a supremum over the empirical sphere at
certain radius. If this sphere is empty, the supremum would be vacuously −∞ or ill-defined. In practice, for most function
classes (e.g., linear or constrained class), this holds automatically. But in a formal proof, this must be stated explicitly.
                                                                                                                     √
hint_u:    Integrability at scale u, i.e. the supremum of the empirical process over the localized ball at radius u = tδ is
integrable with respect to the Gaussian measure. The bad_event_probability_bound uses this. The proof involves
computing or bounding the expectation of supremum and then applying sub-Gaussian concentration. Both steps require that
the supremum random variable is integrable. In the formal proof, Lean’s measure theory requires it as an explicit hypothesis.

hint_δ : Integrability at scale δ, same as hint_u, but at the radius δ instead of u. The proof bounds the expectation of
supremum by relating it to the local Gaussian complexity, which is itself an expectation at scale δ.

hbdd: Boundedness above of the process, which is another technical measure-theoretic condition. The proof takes suprema
(⊔) over localized balls. In Lean 4, ⊔ over an unbounded set can give meaningless results (default to 0 or ⊥). The BddAbove
condition ensures the iSup is a genuine supremum.

C.2. Localized Gaussian Complexity via Dudley
The complete formalization of Theorem 4.2 is:
lemma local_gaussian_complexity_bound (n : N) (hn : 0 < n) (H : Set (X → R)) (δ : R) (hδ
    : 0 < δ) (x : Fin n → X) (hH_star : IsStarShaped H)
  (hH_tb : TotallyBounded (empiricalMetricImage n x ’’ localizedBall H δ x))
  (hfinite : entropyIntegralENNReal (empiricalMetricImage n x ’’ localizedBall H δ x)
    (2*δ) ̸= ⊤)
  (hcont : ∀ w, Continuous (fun (v : ↾(empiricalMetricImage n x ’’ localizedBall H δ x)) =
    > innerProductProcess n v.1 w))
  (hint_pos : Integrable (fun w => ⊔ g ∈ localizedBall H δ x, empiricalProcess n x g w)
    (stdGaussianPi n))
  (hint_neg : Integrable (fun w => ⊔ g ∈ localizedBall H δ x, -empiricalProcess n x g w)
    (stdGaussianPi n)) :
  LocalGaussianComplexity n H δ x ≤ (24 * Real.sqrt 2) / Real.sqrt n * entropyIntegral
    (empiricalMetricImage n x ’’ localizedBall H δ x) (2*δ) := by

Now we will introduce the technical hypotheses:

hfinite:     The entropy integral is finite. If the entropy integral is infinite, the bound is vacuous. The finiteness in ENNReal
ensures the real-valued entropyIntegral is well-defined and the bound is meaningful. This is a formalization concern:
the external dudley theorem needs to know the integral converges.

hcont:    Pathwise continuity of the process. This is also a formalization need for the external dudley theorem. This
should hold automatically in finite dimensions, but in a formal proof in Lean, the continuity needs to be stated with respect
to the subspace topology on the image set.

                                                              15
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

hint_pos:     Integrability of the positive supremum. The proof manipulates integrals (uses linearity of expectation,
comparison of integrands), which requires the functions being integrated to be integrable. Lean 4’s integral of a non-
integrable function is defined to be 0, which would make the bound vacuously useless.

hint_neg:      Same measure-theoretic regularity as above, but for the negative side of the process. The negative version
is needed separately because the supremum of negative function is not simply negative infimum of function in terms of
integrability.

C.3. Observation
The hypotheses hint_u, hint_δ , hint_pos, hint_neg, and hne are typically missed in standard textbook treatments but
act as essential roles to make the statement hold rigorously. The formalization makes precise exactly what must be verified
when extending the theory to new settings.

D. Lean 4 Formalization of Covering of ℓ1 -Convex Hull
In this section, we present more implementation details of Lemma 4.5. Our formalized statement of Lemma 4.5 is:
def l1BallImage (x : Fin n → EuclideanSpace R (Fin d)) (R : R) : Set (EmpiricalSpace n)
    :=
  {v | ∃ θ : EuclideanSpace R (Fin d), l1norm θ ≤ R ∧ v = fun i => (1 / Real.sqrt n) *
    @inner R _ _ θ (x i)}

theorem l1BallImage_coveringNumber_le {R ε : R} (hR : 0 ≤ R) (hε : 0 < ε) (x : Fin n →
    EuclideanSpace R (Fin d)) (hcol : columnNormBound x) (hn : 0 < n) :
  coveringNumber ε (l1BallImage x R) ≤ (2 * d + 1) ˆ ⌈R ˆ 2 / ε ˆ 2⌉+ := by

The major challenge is that the formalization strategy used in Theorem 4.4 can only obtain combinatorial complexity grows
exponentially with d. So we need to formalize the probabilistic rather than combinatorial methods.
In general, our formalization mirrors the Maurey’s Empirical Method (Pisier, 2006).
                                                             √                    √
Step 1: Probabilistic Representation Any point v = Xθ/ n in absconv1 (X/ n; R) can be written as an expected
value:
                                                      v = E[Z]
                                                                  √
where Z is a random variable taking values in {0} ∪ {±R · X[:,j] / n} with probabilities proportional to |θj |.
Step 2: Variance Control The random variable Z has bounded second moment:

                                                E[∥Z∥2 ] ≤ R · ∥θ∥1
                                               √
This uses the column normalization ∥X[:,j] ∥2 ≤ n.
                                                                                                Pk
Step 3: Averaging Reduces Variance For k i.i.d. copies Z1 , . . . , Zk , the average Z̄k = k1    ℓ=1 Zℓ satisfies:

                                                                R · ∥θ∥1   R2
                                             E[∥Z̄k − v∥2 ] ≤            ≤
                                                                    k      k

Step 4: Existence via Pigeonhole Since the expected squared distance is at most R2 /k, there exists a specific sample
achieving this bound. Setting k = ⌈R2 /ε2 ⌉ ensures distance ≤ ε.
Step 5: Finite Net Construction The set of all possible k-averages forms a finite net Nk with:

                                                     |Nk | ≤ (2d + 1)k

since each sample comes from a space of size 2d + 1.

E. Practical Recipe for Human-AI Collaborative Formalization
This section complements Section 5 with the practical workflow recipe.

                                                             16
                        AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

E.1. Decomposition Strategy
Our central operational principle is to decompose every proof so that each leaf-level lemma can be completed by the agent
within a single context window without triggering auto-compaction. Empirically, Claude Opus 4.5 handles up to ∼300 lines
of newly authored Lean per turn before output quality degrades. We thus target ≤ 300 lines per lemma and prefer many
small lemmas over a few large ones. The benefits compound:

   • Higher per-token reasoning budget. Smaller surface area means the agent spends more of its computation on proof
     search and less on parsing context.
   • Bounded blast radius. A failed lemma can be reattempted in isolation without re-instantiating the entire surrounding
     development.
   • Reusability. Small lemmas tend to be reusable across the library; large monolithic proofs tend not to be.
   • Reviewability. Human verification of statements (Section 5.3) is far cheaper at the granularity of small lemmas.

E.2. Anti-rewrite Instruction
The agent’s default response to a large error volume is to abandon the proof. We include the following sentence verbatim in
every TASK.md:

     DO NOT FREQUENTLY CHANGE THE PROOF. ONLY DO SO WHEN YOU ARE CONFIDENT IT IS WRONG.
     FIX ERRORS ONE-BY-ONE.

This single instruction was responsible for the largest qualitative improvement we observed during the project.

E.3. Iterative Cleanup Loop
After a lemma compiles, the resulting code typically contains two classes of artifacts: compiler warnings (unused variables,
shadowed binders, deprecated lemmas) and dead have statements introduced during exploratory proof search. Both are
addressed by dedicated cleanup passes, run in a loop until both report no further changes.

E.3.1. WARNING C LEANUP
We use the following prompt:

     Please modify the formalization code to eliminate the warning messages.
     **IMPORTANT:** For unused variables, you need to directly remove them instead of
     adding ‘ ‘, then correct the downstream call of modified results in [LIBRARYNAME].
     Please use MCP tools to diagnose. The target file to modify is [FILENAME]

The explicit instruction to remove rather than underscore-prefix is critical: Claude Opus 4.5 strongly prefers the latter, which
masks genuine API design issues (e.g. a hypothesis that should never have been added) behind syntactically-clean code.

E.3.2. R EMOVING U NUSED H A V E S TATEMENTS
Unused have statements accumulate during exploratory proof search and bloat the final development without affecting
correctness. We implement the #check unused have command together with the following operational prompt:

     Clean up unused have statements from the target Lean file. First, use the MCP
     tool mcp lean-lsp lean file outline with the absolute file path to get the file
     outline and identify all theorem/lemma declarations in the file. Then, update
     @TestUnusedHave.lean to include #check unused have command for each declaration
     you want to analyze (replace instead of adding). Run lake build TestUnusedHave
     to identify which theorems have unused have statements and note their names. For
     each unused statement reported, use Grep to find its exact location in the file,
     then use Edit to remove the entire have statement including any multi-line proof
     body. Work from bottom to top (highest line numbers first) to preserve line

                                                              17
                      AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

    number accuracy during edits. For have statements on the same line as other
    tactics (like have hX := rfl; linarith), either inline the fact into the tactic
    (e.g., linarith [show X from rfl]) or just keep the tactic if it doesn’t need the
    fact. After removing all identified statements, run lake build [FILENAME] to
    verify compilation succeeds. Then re-run lake build TestUnusedHave to check for
    any cascading unused statements that were exposed (statements that were only used
    by the ones you just removed). Repeat the removal and verification cycle until
    all theorems in the file report "No unused have statements found". Track progress
    and provide a summary of total statements removed when complete. The target Lean
    file is [FILENAME].

Run to fixpoint. Warning cleanup and unused-have cleanup interact: removing a dead have can expose a new unused-
variable warning, and vice versa. We run both passes in alternation until neither produces edits.

F. Example Task Specifications
v1: Extension to Strong Gaussian Sobolev Space via Density Argument

  Your task is to extend the one-dimensional Gaussian logarithmic Sobolev inequality from twice-differentiable functions
  with compact support to strong Gaussian Sobolev function class (f ∈ W 1,2 (γ) with f ∈ C 1 (R)).
  STRONG MEANS THE FUNCTION IS CONTINUOUSLY DIFFERENTIABLE
  Target Theorem Statement. For any continuously differentiable (f ∈ C 1 ) function f : R → R with f ∈ W 1,2 (γ),
  we have
                                       Ent(f 2 ) ≤ 2E ∥∇f (X)∥2 .
                                                                  

  What We Have Formalized.
  FoML/GaussianSobolevDense/Density.lean.                       We have formalized:

     • strong Gaussian Sobolev function class (1D specialized version):
       def MemW12GaussianReal (f : R → R) (γ : Measure R) : Prop :=
         MemLp f 2 γ ∧ MemLp (fun x 7→ fderiv R f x) 2 γ

     • strong Gaussian Sobolev norm squared
       noncomputable def GaussianSobolevNormSqReal (f : R → R) (γ : Measure R) : R≥0∞
           :=
         eLpNorm f 2 γ ˆ 2 + eLpNorm (fun x 7→ ∥fderiv R f x∥) 2 γ ˆ 2

     • existence of a sequence of smooth compactly supported functions converging to any continuously differentiable
       f ∈ W 1,2 (γ) in the 1D Gaussian Sobolev norm
       theorem exists_smooth_compactSupport_seq_tendsto_real (f : R → R)
           (hf : MemW12GaussianReal f (gaussianReal 0 1))
           (hf_diff : Differentiable R f) (hf_grad_cont : Continuous (fun x => fderiv R
           f x)) :
           ∃ g : N → (R → R),
             (∀ k, ContDiff R (⊤ : N∞) (g k)) ∧
             (∀ k, HasCompactSupport (g k)) ∧
             Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) (gaussianReal 0 1))
           atTop (nhds 0) := by

  FoML/GaussianLSI/OneDimGLSI.lean. We have formalized the one-dimensional Gaussian logarithmic
  Sobolev inequality from twice-differentiable functions with compact support
  theorem gaussian_logSobolev_CompSmo {f : R → R} (hf : CompactlySupportedSmooth f) :
      LogSobolev.entropy
          R              stdGaussianMeasure (fun x => (f x)ˆ2) ≤
      2 *   x, (deriv f x)ˆ2 ∂stdGaussianMeasure := by



                                                           18
                     AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


Optimal Proof for Formalization.
Step 1: Approximating Sequence. By the formalized density theorem
exists smooth compactSupport seq tendsto real in
FoML/GaussianSobolevDense/Density.lean, there exists a sequence {gk }∞      ∞   n
                                                                     k=1 ⊂ Cc (R ) such that

                                          ∥f − gk ∥W 1,2 (γ) → 0     as k → ∞,

where f ∈ W 1,2 (γ) with f ∈ C 1 (R).
This means (by MemW12GaussianReal and GaussianSobolevNormSqReal):
   • ∥f − gk ∥L2 (γ) → 0, i.e., E[(f (X) − gk (X))2 ] → 0
   • ∥∇f − ∇gk ∥L2 (γ) → 0, i.e., E[∥∇f (X) − ∇gk (X)∥2 ] → 0
Step 2: Convergence of the Gradient Term.          Since ∇gk → ∇f in L2 (γ), we have

                                    E[∥∇gk (X)∥2 ] → E[∥∇f (X)∥2 ]          as k → ∞.

Proof: By the triangle inequality in L2 (γ),

                                ∥∇gk ∥L2 (γ) − ∥∇f ∥L2 (γ) ≤ ∥∇gk − ∇f ∥L2 (γ) → 0.

Step 3: Convergence of gk2 to f 2 in L1 (γ). We show that gk2 → f 2 in L1 (γ).
Note that
                                          |gk2 − f 2 | = |gk − f | · |gk + f |.
By Cauchy–Schwarz:
                                    E[|gk2 − f 2 |] ≤ ∥gk − f ∥L2 (γ) · ∥gk + f ∥L2 (γ) .
Since gk → f in L2 (γ), the sequence {∥gk ∥L2 (γ) } is bounded, so ∥gk + f ∥L2 (γ) is bounded. Therefore,

                                                    E[|gk2 − f 2 |] → 0.

Step 4: Lower Semicontinuity of Entropy. The entropy functional is lower semicontinuous with respect to L1 (γ)
convergence. That is, if hk → h in L1 (γ) with hk , h ≥ 0, then

                                               Ent(h) ≤ lim inf Ent(hk ).
                                                            k→∞

Proof of lower semicontinuity: This follows from the convexity of ϕ(t) = t log t and Fatou-type arguments. Specifically,
since gk2 → f 2 in L1 (γ), by passing to a subsequence we may assume gk2 → f 2 almost surely. The function
ϕ(t) = t log t (extended to be 0 at t = 0) is bounded below, and by a refined version of Fatou’s lemma for entropy (or
by direct convexity arguments), we obtain the lower semicontinuity.
Step 5: Completing the Proof. By gaussian logSobolev CompSmo in
FoML/GaussianLSI/1dGLSI.lean, for each gk ∈ Cc∞ (Rn ), the log-Sobolev inequality holds:

                                               Ent(gk2 ) ≤ 2E[∥∇gk (X)∥2 ].

Taking lim inf as k → ∞:

                           lim inf Ent(gk2 ) ≤ lim inf 2E[∥∇gk (X)∥2 ] = 2E[∥∇f (X)∥2 ],
                            k→∞                  k→∞

where the equality uses Step 2.
By lower semicontinuity (Step 4):
                                               Ent(f 2 ) ≤ lim inf Ent(gk2 ).
                                                             k→∞
Combining these:
                                               Ent(f 2 ) ≤ 2E[∥∇f (X)∥2 ].
                                                                                                                     □


                                                             19
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


  Rules.
    1. Write all formalization code in FoML/GaussianLSI/OneDimGLSI.lean.
    2. Success = lake build passes + zero sorries + zero custom axioms. Theorems with sorries/axioms are
       scaffolding, not results.

    3. Make proper use of MCP Tools.
    4. DO NOT BE AFRAID OF COMPLEXITY OR LACK OF INFRASTRUCTURES. IF COMPLEX, TRY TO
       USE A LEMMA-BASED MODULAR APPROACH, DECOMPOSE THE PROOF INTO LEMMAS THEN
       SOLVE ONE-BY-ONE. IF LACK OF INFRASTRUCTURES, BUILD REQUIRED INFRASTRUCTURES
       ONE-BY-ONE.

v2: Lower Semicontinuity of Entropy

  What We Have Formalized.
  FoML/GaussianSobolevDense/Density.lean. We have formalized:
    • strong Gaussian Sobolev function class (1D specialized version):
      def MemW12GaussianReal (f : R → R) (γ : Measure R) : Prop :=
        MemLp f 2 γ ∧ MemLp (fun x 7→ fderiv R f x) 2 γ

    • strong Gaussian Sobolev norm squared
      noncomputable def GaussianSobolevNormSqReal (f : R → R) (γ : Measure R) : R≥0∞
          :=
        eLpNorm f 2 γ ˆ 2 + eLpNorm (fun x 7→ ∥fderiv R f x∥) 2 γ ˆ 2

    • existence of a sequence of smooth compactly supported functions converging to any continuously differentiable
      f ∈ W 1,2 (γ) in the 1D Gaussian Sobolev norm
      theorem exists_smooth_compactSupport_seq_tendsto_real (f : R → R)
          (hf : MemW12GaussianReal f (gaussianReal 0 1))
          (hf_diff : Differentiable R f) (hf_grad_cont : Continuous (fun x => fderiv R
          f x)) :
          ∃ g : N → (R → R),
            (∀ k, ContDiff R (⊤ : N∞) (g k)) ∧
            (∀ k, HasCompactSupport (g k)) ∧
            Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) (gaussianReal 0 1))
          atTop (nhds 0) := by

  FoML/GaussianLSI/Entropy.lean.                 We have formalized:
    • definition of entropy
        R entropy (µ : Measure Ω) (fR : Ω → R) : R := R
      def
          ω, f ω * log (f ω) ∂µ - ( ω, f ω ∂µ) * log ( ω, f ω ∂µ)

    • entropy of f 2 with respect to the normalization
      def entropySquare (µ : Measure Ω) (f : Ω → R) : R :=
        entropy µ (fun ω => (f ω)ˆ2)

    • properties of entropy (please read carefully and use properly):
           1. entropy const: Entropy of a constant function is zero.
           2. entropy congr: If f = g a.e., then their entropies are equal.
           3. jensen mul log: Jensen’s inequality for the convex function x · log(x).


                                                           20
                    AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


      4. entropy nonneg: Entropy is nonnegative for probability measures and nonnegative integrands.
      5. entropySquare eq: The entropy of f 2 is always well-defined in the sense that the integrand f 2 ·
         log(f 2 ) = 2 · f 2 · log |f | is measurable when f is.
      6. entropy sq normalized, log sq eq two mul log abs.
      7. entropy sq abs log: Entropy of f 2 in terms of 2 · f 2 · log |f |.
FoML/FatouReal.lean. Fatou’s Lemma for Nonnegative Real Functions: For a sequence of nonnegative
measurable integrable functions with integrable liminf:
theorem integral_liminf_le_of_nonneg
    {f : N → Ω → R}
    (hf_meas : ∀ n, Measurable (f n))
    (hf_nonneg : ∀ n ω, 0 ≤ f n ω)
    (hf_int : ∀ n, Integrable (f n) µ)
    (h_liminf_int : Integrable (fun ω => liminf (fun n =>R f n ω) atTop) µ)
    (h_cobdd
    R        : IsCoboundedUnder  (· ≥ ·) atTop (fun n =>   ω, f n ω ∂µ)) :
      ω, liminf (fun Rn => f n ω) atTop ∂µ ≤
    liminf (fun n =>    ω, f n ω ∂µ) atTop := by
This is derived from the ENNReal Fatou lemma via the transformation:
 1. Embed via ENNReal.ofReal.
 2. Apply lintegral liminf le.
 3. Convert back using integral–lintegral relationships.
Note: The h cobdd assumption ensures the real-valued liminf is well-defined (not the junk value 0 from an unbounded
sequence). This holds automatically when integrals are bounded above.
FoML/ConvergenceL1Subseq.lean.                Convergence in L1 (µ) yields an a.e.-convergent subsequence
theorem exists_seq_tendsto_ae_of_tendsto_eLpNorm_one
    [NormedAddCommGroup E] {f : N → α → E} {g : α → E}
    (hf : ∀ n, AEStronglyMeasurable (f n) mu)
    (hg : AEStronglyMeasurable g mu)
    (hfg : Tendsto (fun n => eLpNorm (f n - g) (1 : ENNReal) mu) atTop (nhds 0)) :
    ∃ ns : N → N, StrictMono ns ∧
      ∀m x ∂mu, Tendsto (fun i => f (ns i) x) atTop (nhds (g x)) := by

Target Theorem Statement. By exists smooth compactSupport seq tendsto real, we can construct
a sequence of smooth compactly supported functions {gk }∞      ∞
                                                        k=1 ⊂ Cc (R) converging to any f in the strong Gaussian
                                1,2               1
Sobolev function class (f ∈ W (γ) with f ∈ C (R)) in the 1D Gaussian Sobolev norm.
STRONG MEANS THE FUNCTION IS CONTINUOUSLY DIFFERENTIABLE
Therefore, our target theorem is a consequent result:

                                           Ent(f 2 ) ≤ lim inf Ent(gk2 ).
                                                           k→∞

Optimal Proof for Formalization.
Step 1: Approximating Sequence. By the formalized density theorem
exists smooth compactSupport seq tendsto real in
FoML/GaussianSobolevDense/Density.lean, there exists a sequence {gk }∞      ∞
                                                                     k=1 ⊂ Cc (R) such that

                                        ∥f − gk ∥W 1,2 (γ) → 0   as k → ∞,

where f ∈ W 1,2 (γ) with f ∈ C 1 (R).
By MemW12GaussianReal and GaussianSobolevNormSqReal, we can obtain:

                              ∥f − gk ∥L2 (γ) → 0,   i.e., E[(f (X) − gk (X))2 ] → 0.


                                                           21
                      AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


  Step 2: Convergence of gk2 to f 2 in L1 (γ). We show that gk2 → f 2 in L1 (γ).
  Note that
                                            |gk2 − f 2 | = |gk − f | · |gk + f |.
  By Cauchy-Schwarz (Use LeanSearch MCP Tool to search for the Holder’s inequality and use proper conjugate
  pair p and q):
                              E[|gk2 − f 2 |] ≤ ∥gk − f ∥L2 (γ) · ∥gk + f ∥L2 (γ) .
  Since gk → f in L2 (γ), the sequence {∥gk ∥L2 (γ) } is bounded, so ∥gk + f ∥L2 (γ) is bounded. Therefore,

                                                   E[|gk2 − f 2 |] → 0.

  Step 3: Lower Semicontinuity of Entropy. The entropy functional is lower semicontinuous with respect to L1 (γ)
  convergence. That is, if hk → h in L1 (γ) with hk , h ≥ 0, then

                                              Ent(h) ≤ lim inf Ent(hk ).
                                                          k→∞

    1. Take hk = gk2 and h = f 2 .
    2. Proof needs a series of integrability, remember all integrabilities can be proven by the compactness of
       {gk }∞       ∞    n                                                         2         ′    2
            k=1 ⊂ Cc (R ) and f belongs to strong Gaussian Sobolev space (f ∈ L (γ) and f ∈ L (γ)).

    3. Following from the convexity of ϕ(t)              =      t log t and real-valued Fatou lemma
       integral liminf le of nonneg.             Specifically, since gk2    →       f 2 in L1 (γ), by
       exists seq tendsto ae of tendsto eLpNorm one, there exists a subsequence gk2′ → f 2
       almost surely. The function ϕ(t) = t log t (extended to be 0 at t = 0) is bounded below, and by
       integral liminf le of nonneg for entropy, we obtain the lower semicontinuity.
  Rules.

    1. Create a file in FoML/GaussianSobolevDense/ named LiminfContEnt.lean and write all formal-
       ization code in this file.
    2. Success = lake build passes + zero sorries + zero custom axioms. Theorems with sorries/axioms are
       scaffolding, not results.
    3. Make proper use of MCP Tools.

    4. DO NOT BE AFRAID OF COMPLEXITY OR LACK OF INFRASTRUCTURES. IF COMPLEX, TRY TO
       USE A LEMMA-BASED MODULAR APPROACH, DECOMPOSE THE PROOF INTO LEMMAS THEN
       SOLVE ONE-BY-ONE. IF LACK OF INFRASTRUCTURES, BUILD REQUIRED INFRASTRUCTURES
       ONE-BY-ONE.


v3: Convergence of the Gradient Term in L2 (γ)

  What We Have Formalized.
  FoML/GaussianSobolevDense/Density.lean. We have formalized:
    • strong Gaussian Sobolev function class (1D specialized version):
       def MemW12GaussianReal (f : R → R) (γ : Measure R) : Prop :=
         MemLp f 2 γ ∧ MemLp (fun x 7→ fderiv R f x) 2 γ

     • strong Gaussian Sobolev norm squared
       noncomputable def GaussianSobolevNormSqReal (f : R → R) (γ : Measure R) : R≥0∞
           :=
         eLpNorm f 2 γ ˆ 2 + eLpNorm (fun x 7→ ∥fderiv R f x∥) 2 γ ˆ 2



                                                           22
                   AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


  • existence of a sequence of smooth compactly supported functions converging to any continuously differentiable
    f ∈ W 1,2 (γ) in the 1D Gaussian Sobolev norm
    theorem exists_smooth_compactSupport_seq_tendsto_real (f : R → R)
        (hf : MemW12GaussianReal f (gaussianReal 0 1))
        (hf_diff : Differentiable R f) (hf_grad_cont : Continuous (fun x => fderiv R
        f x)) :
        ∃ g : N → (R → R),
          (∀ k, ContDiff R (⊤ : N∞) (g k)) ∧
          (∀ k, HasCompactSupport (g k)) ∧
          Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) (gaussianReal 0 1))
        atTop (nhds 0) := by

FoML/GaussianLSI/Entropy.lean.                We have formalized:
  • definition of entropy
      R entropy (µ : Measure Ω) (fR : Ω → R) : R := R
    def
        ω, f ω * log (f ω) ∂µ - ( ω, f ω ∂µ) * log ( ω, f ω ∂µ)

  • entropy of f 2 with respect to the normalization
    def entropySquare (µ : Measure Ω) (f : Ω → R) : R :=
      entropy µ (fun ω => (f ω)ˆ2)

  • properties of entropy (please read carefully and use properly):
      1. entropy const: Entropy of a constant function is zero.
      2. entropy congr: If f = g a.e., then their entropies are equal.
      3. jensen mul log: Jensen’s inequality for the convex function x · log(x).
      4. entropy nonneg: Entropy is nonnegative for probability measures and nonnegative integrands.
      5. entropySquare eq: The entropy of f 2 is always well-defined in the sense that the integrand f 2 ·
         log(f 2 ) = 2 · f 2 · log |f | is measurable when f is.
      6. entropy sq normalized, log sq eq two mul log abs.
      7. entropy sq abs log: Entropy of f 2 in terms of 2 · f 2 · log |f |.
FoML/GaussianSobolevDense/LiminfContEnt.lean.                         We have formalized:
  • convergence in Gaussian Sobolev norm (squared) implies convergence in L2 (γ):
    lemma tendsto_eLpNorm_sub_of_sobolev (f : R → R) (g : N → R → R) (µ : Measure R
        )
        (h_tend : Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) µ) atTop
        (nhds 0)) :
        Tendsto (fun k => eLpNorm (f - g k) 2 µ) atTop (nhds 0) := by

  • convergence in L2 (γ) of real-valued functions implies convergence in L1 (γ) of their pointwise squares:
    lemma tendsto_eLpNorm_sub_of_sobolev (f : R → R) (g : N → R → R) (µ : Measure R
        )
        (h_tend : Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) µ) atTop
        (nhds 0)) :
        Tendsto (fun k => eLpNorm (f - g k) 2 µ) atTop (nhds 0) := by

Target Theorem Statement. By exists smooth compactSupport seq tendsto real, we can construct
a sequence of smooth compactly supported functions {gk }∞        ∞
                                                          k=1 ⊂ Cc (R) converging to any f in the strong Gaussian
                                1,2               1
Sobolev function class (f ∈ W (γ) with f ∈ C (R)) in the 1D Gaussian Sobolev norm.
STRONG MEANS THE FUNCTION IS CONTINUOUSLY DIFFERENTIABLE
Therefore, our target formalizations (as a lemma) are:
                                          Z                  Z
                                             ∥∇gk ∥22 dγ −→    ∥∇f ∥22 dγ.


                                                        23
                       AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


  Optimal Proof for Formalization.
  Step 1: Approximating Sequence. By the formalized density theorem
  exists smooth compactSupport seq tendsto real in
  FoML/GaussianSobolevDense/Density.lean, there exists a sequence {gk }∞      ∞
                                                                       k=1 ⊂ Cc (R) such that

                                           ∥f − gk ∥W 1,2 (γ) → 0     as k → ∞,

  where f ∈ W 1,2 (γ) with f ∈ C 1 (R).
  By MemW12GaussianReal and GaussianSobolevNormSqReal, we can obtain:

                            ∥∇f − ∇gk ∥L2 (γ) → 0,      i.e.,    E[∥∇f (X) − ∇gk (X)∥2 ] → 0.

  Step 2: Convergence of the Gradient Term.        Since ∇gk → ∇f in L2 (γ), we have

                                     E[∥∇gk (X)∥2 ] → E[∥∇f (X)∥2 ]        as k → ∞.

  Proof sketch: By the triangle inequality in L2 (γ),

                                  ∥∇gk ∥L2 (γ) − ∥∇f ∥L2 (γ) ≤ ∥∇gk − ∇f ∥L2 (γ) → 0.

  Rules.
    1. Write all formalization code in LiminfContEnt.lean.

    2. Success = lake build passes + zero sorries + zero custom axioms. Theorems with sorries/axioms are
       scaffolding, not results.
    3. Make proper use of MCP Tools.
    4. DO NOT BE AFRAID OF COMPLEXITY OR LACK OF INFRASTRUCTURES. IF COMPLEX, TRY TO
       USE A LEMMA-BASED MODULAR APPROACH, DECOMPOSE THE PROOF INTO LEMMAS THEN
       SOLVE ONE-BY-ONE. IF LACK OF INFRASTRUCTURES, BUILD REQUIRED INFRASTRUCTURES
       ONE-BY-ONE.

v4: GLSI Extension to Strong Gaussian Sobolev Space

  What We Have Formalized.
  FoML/GaussianSobolevDense/Density.lean. We have formalized:
    • strong Gaussian Sobolev function class (1D specialized version):
       def MemW12GaussianReal (f : R → R) (γ : Measure R) : Prop :=
         MemLp f 2 γ ∧ MemLp (fun x 7→ fderiv R f x) 2 γ

       NOTICE THAT YOU CAN PROVE MOST INTEGRABILITY OR FINITENESS FROM
       MemW12GaussianReal.
     • strong Gaussian Sobolev norm squared
       noncomputable def GaussianSobolevNormSqReal (f : R → R) (γ : Measure R) : R≥0∞
           :=
         eLpNorm f 2 γ ˆ 2 + eLpNorm (fun x 7→ ∥fderiv R f x∥) 2 γ ˆ 2

     • existence of a sequence of smooth compactly supported functions converging to any continuously differentiable
       f ∈ W 1,2 (γ) in the 1D Gaussian Sobolev norm
       theorem exists_smooth_compactSupport_seq_tendsto_real (f : R → R)
           (hf : MemW12GaussianReal f (gaussianReal 0 1))



                                                                24
                  AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


        (hf_diff : Differentiable R f) (hf_grad_cont : Continuous (fun x => fderiv R
        f x)) :
        ∃ g : N → (R → R),
          (∀ k, ContDiff R (⊤ : N∞) (g k)) ∧
          (∀ k, HasCompactSupport (g k)) ∧
          Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) (gaussianReal 0 1))
        atTop (nhds 0) := by

FoML/GaussianLSI/Entropy.lean.               We have formalized:

 • definition of entropy
     R entropy (µ : Measure Ω) (fR : Ω → R) : R := R
   def
       ω, f ω * log (f ω) ∂µ - ( ω, f ω ∂µ) * log ( ω, f ω ∂µ)

 • entropy of f 2 with respect to the normalization
   def entropySquare (µ : Measure Ω) (f : Ω → R) : R :=
     entropy µ (fun ω => (f ω)ˆ2)

 • properties of entropy (please read carefully and use properly):
     1. entropy const: Entropy of a constant function is zero.
     2. entropy congr: If f = g a.e., then their entropies are equal.
     3. jensen mul log: Jensen’s inequality for the convex function x · log(x).
     4. entropy nonneg: Entropy is nonnegative for probability measures and nonnegative integrands.
     5. entropySquare eq: The entropy of f 2 is always well-defined in the sense that the integrand f 2 ·
        log(f 2 ) = 2 · f 2 · log |f | is measurable when f is.
     6. entropy sq normalized, log sq eq two mul log abs.
     7. entropy sq abs log: Entropy of f 2 in terms of 2 · f 2 · log |f |.
FoML/GaussianSobolevDense/LiminfContEnt.lean.                        We have formalized:
 • ϕ(t) = t · log(t) is bounded below by −1/e for t ≥ 0:
   lemma mul_log_ge_neg_inv_exp (t : R) (ht : 0 ≤ t) : -(1 / Real.exp 1) ≤ t *
       Real.log t := by

 • convergence in Gaussian Sobolev norm (squared) implies convergence in L2 (γ):
   lemma tendsto_eLpNorm_sub_of_sobolev (f : R → R) (g : N → R → R) (µ : Measure R
       )
       (h_tend : Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) µ) atTop
       (nhds 0)) :
       Tendsto (fun k => eLpNorm (f - g k) 2 µ) atTop (nhds 0) := by

 • convergence in L2 (γ) of real-valued functions implies convergence in L1 (γ) of their pointwise squares:
   lemma tendsto_eLpNorm_sub_of_sobolev (f : R → R) (g : N → R → R) (µ : Measure R
       )
       (h_tend : Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) µ) atTop
       (nhds 0)) :
       Tendsto (fun k => eLpNorm (f - g k) 2 µ) atTop (nhds 0) := by

 • convergence in Gaussian Sobolev norm (squared) implies convergence of gradient in L2 (γ):




                                                       25
                    AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


     lemma tendsto_integral_norm_fderiv_sq_of_sobolev (f : R → R) (g : N → R → R)
         (µ : Measure R)
         (hf_diff : Differentiable R f) (hf_grad_cont : Continuous (fun x => fderiv R
         f x))
         (hg_diff : ∀ k, Differentiable R (g k))
         (hg_grad_cont : ∀ k, Continuous (fun x => fderiv R (g k) x))
         (hf_mem : MemLp (fun x => ∥fderiv R f x∥) 2 µ)
         (hg_mem : ∀ k, MemLp (fun x => ∥fderiv R (g k) x∥) 2 µ)
         (h_tend : Tendsto (fun k => GaussianSobolevNormSqReal (f - g k) µ) atTop
         (nhds 0)) :       R
         Tendsto (fun
                  R   k =>   x, ∥fderiv R (g k) x∥ˆ2 ∂µ) atTop
           (nhds ( x, ∥fderiv R f x∥ˆ2 ∂µ)) := by

FoML/GaussianLSI/OneDimGLSI.lean. We have formalized the one-dimensional Gaussian logarithmic
Sobolev inequality for twice-differentiable functions with compact support
theorem gaussian_logSobolev_CompSmo_fderiv {f : R → R} (hf :
    CompactlySupportedSmooth f) :
    LogSobolev.entropy
        R              stdGaussianMeasure (fun x => (f x)ˆ2) ≤
    2 *   x, ∥fderiv R f x∥ˆ2 ∂stdGaussianMeasure := by

FoML/ConvergenceL1Subseq.lean.                 Convergence in L1 (µ) yields an a.e.-convergent subsequence
theorem exists_seq_tendsto_ae_of_tendsto_eLpNorm_one
    [NormedAddCommGroup E] {f : N → α → E} {g : α → E}
    (hf : ∀ n, AEStronglyMeasurable (f n) mu)
    (hg : AEStronglyMeasurable g mu)
    (hfg : Tendsto (fun n => eLpNorm (f n - g) (1 : ENNReal) mu) atTop (nhds 0)) :
    ∃ ns : N → N, StrictMono ns ∧
      ∀m x ∂mu, Tendsto (fun i => f (ns i) x) atTop (nhds (g x)) := by

Target Theorem Statement. By exists smooth compactSupport seq tendsto real, we can construct
a sequence of smooth compactly supported functions {gk }∞          ∞
                                                           k=1 ⊂ Cc (R) converging to any f in the strong Gaussian
                                 1,2              1
Sobolev function class (f ∈ W (γ) with f ∈ C (R)) in the 1D Gaussian Sobolev norm.
Your task is to extend the one-dimensional Gaussian logarithmic Sobolev inequality from twice-differentiable functions
with compact support to strong Gaussian Sobolev function class (f ∈ W 1,2 (γ) with f ∈ C 1 (R)).
STRONG MEANS THE FUNCTION IS CONTINUOUSLY DIFFERENTIABLE
Therefore, our TARGET THEOREM is:

     For any continuously differentiable (f ∈ C 1 ) function f : R → R with f ∈ W 1,2 (γ), we have

                                           Ent(f 2 ) ≤ 2E ∥∇f (X)∥2 .
                                                                      


Optimal Proof for Formalization.
Step 1: Preliminaries about (x log x), WELL-FORMALIZED. Define ϕ : [0, ∞) → R by ϕ(x) = x log x (has
been formalized as def phi).
Fact 1 (continuity). ϕ is continuous on [0, ∞). This has been formalized as phi continuous.
Fact 2 (bounded below).
                                                                1
                                                 inf ϕ(x) = − .
                                                 x≥0            e
Hence
                                             1
                                               ≥ 0 for all x ≥ 0.
                                           ϕ(x) +                                                  (1)
                                             e
This “shift to nonnegativity” is what makes Fatou immediately applicable, which has been formalized in
mul log ge neg inv exp.




                                                         26
                    AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


Step 2: A subsequence lemma (from L1 to a.e.), WELL-FORMALIZED. Lemma (a.e. conver-
gent subsequence). Convergence in L1 (µ) yields an a.e.-convergent subsequence, has been formalized as
exists seq tendsto ae of tendsto eLpNorm one in FoML/ConvergenceL1Subseq.lean.
                                R
Step 3: Lower semicontinuity of g log g via Fatou’s lemma. IMPORTANT: FROM HERE, WE WORK IN
ENNREAL!!!
Proposition (lower semicontinuity). Assume qk ≥ 0 and qk → q in L1 (γ). Then
                Z                   Z                  Z                      Z
                   ϕ(q) dγ ≤ lim inf ϕ(qk ) dγ, i.e.      q log q dγ ≤ lim inf qk log qk dγ,       (3)
                                k→∞                                                 k→∞


allowing the value +∞ on either side. (We will set qk = gk2 , q = f 2 later.)
Proof. Let                                       Z
                                          L := lim inf        ϕ(qk ) dγ ∈ [−1/e, ∞].
                                                k→∞

Choose a subsequence (still denoted qk for simplicity) such that
                                                Z
                                                    ϕ(qk ) dγ → L.                                        (4)

(4) can be proven via: set
                                      Z                   
                                                       1
                              ak :=       ϕ(qk ) dµ ∈ − , ∞              where ϕ(x) = x log x.
                                                       e

Let                                                                 
                                                                 1
                                              L := lim inf ak ∈ − , ∞ .
                                                    k→∞          e
If L < ∞, then there exists a subsequence (a∗kj )j≥1 such that

                                                             a∗kj → L.

If L = ∞, then there is nothing to choose: “≤ lim inf” is automatic whenever the right-hand side is +∞.
Define the tail infima
                                                   bj := inf ak .
                                                                k≥j

Then (bj ) is nondecreasing and bj ↑ L by definition of lim inf.
For each j, by the definition of infimum, there exists some index kj ≥ j such that

                                                                1
                                                      akj ≤ bj + .
                                                                j
Then,
                                                                  1
                                                   bj ≤ akj ≤ bj + ,
                                                                  j
so as j → ∞,
                                                             akj → L.
This is the subsequence you used. It is a standard “almost minimizer of tail infimum” construction.
Given qk → q in L1 (γ), apply the lemma exists seq tendsto ae of tendsto eLpNorm one to extract a
subsequence such that qk → q a.e.
By continuity of ϕ (Fact 1), we have ϕ(qk ) → ϕ(q) a.e., hence

                                               ϕ(q) ≤ lim inf ϕ(qk )        a.e.                          (5)
                                                             k→∞




                                                                27
                     AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


Now shift to nonnegativity using (1): define
                                                     1                                  1
                                   hk := ϕ(qk ) +      ≥ 0,            h := ϕ(q) +        ≥ 0.
                                                     e                                  e
From (5),
                                                  h ≤ lim inf hk           a.e.
                                                             k
Fatou’s lemma for nonnegative functions (lintegral liminf le!!!) gives
                                          Z               Z
                                            h dγ ≤ lim inf hk dγ.
                                                                k→∞

Subtract 1/e from both sides (note γ is a probability measure, so 1e dγ = 1e ) to get
                                                                 R
                                          Z                    Z
                                             ϕ(q) dγ ≤ lim inf ϕ(qk ) dγ.
                                                                k→∞
                                                           R
Using (4), the right-hand side equals L, which is lim inf k ϕ(gk ). This proves (3).                         ■
Integrability remarks.
   • We did not assume ϕ(gk ) ∈ L1 . If ϕ(gk ) = +∞ along a subsequence, Fatou still applies because hk ≥ 0 and
                                         R

     the integrals are allowed to be +∞.
   • The negative part is never a problem because ϕ ≥ −1/e; that is exactly why the shift works.
Step 4: Lower semicontinuity of entropy. Define, for q ≥ 0,
                                      Z                                                    Z
                            Ent(q) = q log q dγ − m log m,                        m :=         q dγ.

Corollary. If qk ≥ 0 and qk → q in L1 (γ), then
                                               Ent(q) ≤ lim inf Ent(qk ).                                             (6)
                                                                k→∞

Proof. From L1 -convergence, mk :=
                                       R             R
                                           qk dγ →       q dγ = m. The map x 7→ x log x is continuous on [0, ∞), so
                                                 mk log mk → m log m.                                                 (7)
From the proposition,                   Z                              Z
                                            q log q dγ ≤ lim inf           qk log qk dγ.                              (8)
                                                             k→∞
Combine (7)–(8):
                    Z                                       Z
         Ent(q) =       q log q dγ − m log m ≤ lim inf           qk log qk dγ − lim mk log mk = lim inf Ent(qk ).
                                                     k                              k                  k

                                                                                                                       ■
Step 5: Application in Our Case.       Take qk = fk2 and q = f 2 . So the corollary gives
                                               Ent(f 2 ) ≤ lim inf Ent(gk2 ),
                                                                 k→∞

which is the exact lower semicontinuity.
Step 6:   Back to Real Space. By tendsto integral norm fderiv sq of sobolev                                           and
gaussian logSobolev CompSmo fderiv, we can obtain
                                              Z             Z
                  lim inf Ent(gk ) ≤ lim inf 2 |∇gk | dγ = 2 |∇f |2 dγ < ∞.
                                                     2
                                                                                                                      (∗)
                            k→∞                 k→∞

Now combine (∗) with
                                               Ent(f 2 ) ≤ lim inf Ent(gk2 ),
                                                                 k→∞
to get all finiteness, then we can convert back to real space.


                                                                 28
                    AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory


Conclude the Limit.
                                           Ent(f 2 ) ≤ 2E ∥∇f (X)∥2 .
                                                                  

follows from results formalized, add the proof by yourself.
Rules.
 1. Write all formalization code in LiminfContEnt.lean.

 2. Success = lake build passes + zero sorries + zero custom axioms. Theorems with sorries/axioms are
    scaffolding, not results.
 3. Make proper use of MCP Tools.
 4. DO NOT BE AFRAID OF COMPLEXITY OR LACK OF INFRASTRUCTURES. IF COMPLEX, TRY TO
    USE A LEMMA-BASED MODULAR APPROACH, DECOMPOSE THE PROOF INTO LEMMAS THEN
    SOLVE ONE-BY-ONE. IF LACK OF INFRASTRUCTURES, BUILD REQUIRED INFRASTRUCTURES
    ONE-BY-ONE.




                                                         29
