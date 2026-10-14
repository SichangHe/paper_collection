                                                   Progress in Formalizing Sphere Packing in
                                                                  Dimension 8

                                                        Sidharth Hariharan1[0009−0000−8176−902X] , Christopher
                                                          2[0000−0002−7546−9028]
                                             Birkbeck                          , Seewoo Lee3[0000−0002−5710−2257] , Ho Kiu
                                                      4[0009−0008−2940−8233]
                                           Gareth Ma                          , Bhavik Mehta5[0000−0001−7892−7891] , Auguste
arXiv:2604.23468v3 [math.MG] 29 May 2026




                                                    6,7[0009−0005−7868−7185]
                                            Poiroux                          , and Maryna Viazovska7[0000−0001−7567−5254]
                                               1
                                                Carnegie Mellon University, Pittsburgh PA 15213, United States of America
                                                    2
                                                        University of East Anglia, Norwich NR4 7TJ, United Kingdom
                                            3
                                              University of California, Berkeley, Berkeley CA 94720, United States of America
                                                      4
                                                         University of Warwick, Coventry CV4 7AL, United Kingdom
                                                     5
                                                        Imperial College London, London SW7 2AZ, United Kingdom
                                                    6
                                                        Math, Inc, San Francisco CA 94107, United States of America
                                              7
                                                École Polytechnique Fédérale de Lausanne, 1015 Lausanne VD, Switzerland



                                                    Abstract. In 2016, Viazovska famously solved the sphere packing prob-
                                                    lem in dimension 8, using modular forms to construct a ‘magic’ function
                                                    satisfying optimality conditions determined by Cohn and Elkies in 2003.
                                                    In March 2024, Hariharan and Viazovska launched a project to formal-
                                                    ize this solution and related mathematical facts in the Lean Theorem
                                                    Prover. A significant milestone was achieved in February 2026: the re-
                                                    sult was formally verified, with the final stages of the verification done
                                                    by Math, Inc.’s autoformalization model ‘Gauss’. We discuss the tech-
                                                    niques used to achieve this milestone, reflect on the unique collaboration
                                                    between humans and Gauss, and discuss project objectives that remain.

                                                    Keywords: Sphere Packing · Formalization · Autoformalization · Lean


                                           1       Introduction
                                           The sphere packing problem is a notoriously difficult problem in discrete ge-
                                           ometry, asking what the densest arrangement of non-overlapping n-spheres is
                                           in Rn . When n = 1, the solution is trivial. When n = 2, the optimal packing
                                           is the A2 lattice packing. The result is often attributed to Thue [12], though
                                           many credit Toth [13] for providing the first rigorous proof. The story is more
                                           interesting when n = 3, and while the solution was originally conjectured by
                                           Kepler [8] as far back as 1611, it was not proved till the turn of the century by
                                           Tom Hales [5], who went on to formally verify [6] his heavily computer-assisted,
                                           computationally involved proof.
                                               In March 2024, Hariharan and Viazovska launched a project to investigate
                                           Viazovska’s solution in dimension 8 [14] and follow-up calculations by Lee [10] by
                                           formalizing them in the Lean Theorem Prover [11], building infrastructure along
                                           the way to support ongoing and future work in related areas to the end of creating
2        S. Hariharan et al.

a readable, maintainable, and reusable proof artifact for this remarkable result.
The work done so far by both human formalizers and the autoformalization
model ‘Gauss’ has together led to a complete, correct8 proof that the optimal
sphere packing in R8 is the E8 lattice packing. This paper discusses the project
objectives achieved with this milestone and outlines those that remain.


2     The Mathematics behind the 8-Dimensional Sphere
      Packing Problem
In this section, we give an overview of the informal argument, listing key defi-
nitions and theorem statements, both informally and in Lean. All code in this
section was written by human formalizers prior to the Gauss autoformalization.

2.1    The Road to Stating the Main Theorem
The primary data making up a sphere packing is a set X ⊆ Rd of centres and
some separation r > 0 such that for all x, y ∈ X, ∥x − y∥ ≥ r. We thus defined
SpherePacking to be the structure bundling together the following data: the set
of centres; the separation; the requirement that the separation is positive (with
infrastructure to automatically deduce this where possible); and the fact that
the separation does, indeed, separate the centres.
structure SpherePacking (d : N) where
  centers : Set (EuclideanSpace R (Fin d))
  separation : R
  separation_pos : 0 < separation := by positivity
  centers_dist : Pairwise (separation ≤ dist · · : centers → centers →
    Prop)
This definition does not actually involve the balls that make upSthe packing. We
thus defined SpherePacking.balls to be the quantity P(X) = x∈X Bd (x, r):
abbrev SpherePacking.balls
                S          (S : SpherePacking d) : Set (EuclideanSpace R
    (Fin d)) :=    x : S.centers, Metric.ball x (S.separation / 2)
The prefix SpherePacking in the above definition not only places balls in the
SpherePacking namespace (which is useful for disambiguation) but also allows
us to use dot notation, whereby if we wish to refer to the balls of a particular
sphere packing S, we can simply write S.balls.
   Next, we define the finite density9 of a sphere packing as the proportion of a
bounded ball it occupies. We further define the density of a sphere packing to be
the lim sup of all finite densities. We denote them ∆finite
                                                     P(X) and ∆P(X) respectively:

                    Vol(P(X) ∩ Bd (0, R))
     ∆finite
      P(X) (R) :=                                  ∆P(X) := lim sup ∆finite
                                                                     P(X) (R)
                        Vol(Bd (0, R))                        R→∞
8
    in the sense of being formally verified by the Lean kernel
9
    A more accurate term might be ‘bounded’ density, in the sense of being computed
    over bounded regions.
                     Progress in Formalizing Sphere Packing in Dimension 8       3

We define these in Lean as follows:
def SpherePacking.finiteDensity (S : SpherePacking d) (R : R) : R≥0∞ :=
  volume (S.balls ∩ ball 0 R) / (volume (ball 0 R))
def SpherePacking.density (S : SpherePacking d) : R≥0∞ := limsup
    S.finiteDensity atTop
A periodic sphere packing is a sphere packing that is periodic with respect
to the additive action of a lattice on the ambient space (meaning, in particular,
that it acts on the set of centres). Our Lean definition is as follows:
structure PeriodicSpherePacking (d : N) extends SpherePacking d where
  lattice : Submodule Z (EuclideanSpace R (Fin d))
  lattice_action : ∀ {|x y|}, x ∈ lattice → y ∈ centers → x + y ∈
    centers
  lattice_discrete : DiscreteTopology lattice := by infer_instance
  lattice_isZLattice : IsZLattice R lattice := by infer_instance
It is easy to see that the density of any sphere packing is at most 1. Thus, the
following supremum, known as the sphere packing constant, is finite:

                            ∆d :=     sup      ∆(P(X))
                                    P(X)⊆Rd
                                          F
It is defined in Lean as follows (where       denotes the (indexed) supremum):
def
  F SpherePackingConstant (d : N) : R≥0∞ :=
     S : SpherePacking d, S.density
The E8 lattice is the unique even, unimodular lattice in R8 , defined as follows:
               (                             8 X8
                                                                      )
                                            1
        Λ8 := (x1 , . . . , x8 ) ∈ Z8 ∪ Z +          xi ≡ 0 (mod 2)
                                            2    i=1
                                                                    √
The E8 sphere packing P(Λ8 ) is the packing of balls of radius 22 centred at
points on Λ8 . We define it in Lean as the following PeriodicSpherePacking:
noncomputable def E8Packing : PeriodicSpherePacking 8 where
                 √
  separation :=    2
  lattice := E8Lattice
  centers := E8Lattice
  centers_dist := by · · ·
Viazovska’s main result in [14] is the following:
Theorem 1 (Viazovska 2016). There is no sphere packing in R8 with density
greater than that of the E8 packing. That is,

                           ∆8 = ∆(P(Λ8 )) = π 4 /384

In Lean, our statement of the main theorem is the above equality:
theorem SpherePacking.MainTheorem : SpherePackingConstant 8 =
    E8Packing.density := · · ·
   4       S. Hariharan et al.

   The proof relies on the following linear programming bound by Cohn and Elkies.

   Theorem 2 (Cohn-Elkies 2003 [2, Theorem 3.1]). If f : Rd → R is a
   Schwartz function satisfying the conditions

(CE1) f is not identically zero.
(CE2) For all x ∈ Rd , if ∥x∥ ≥ 1 then f (x) ≤ 0.
(CE3) For all x ∈ Rd , fb(x) ≥ 0.

   then we have the following bound on the sphere packing constant ∆d :
                                                    
                                  f (0)             1
                            ∆d ≤        · Vol Bd 0,
                                  fb(0)             2

   Viazovska [14, Theorem 3] showed the existence of a ‘magic’ function g : R8 → R
   whose Cohn-Elkies bound gg(0)              1
                                                
                             b(0) · Vol Bd 0, 2    is precisely ∆(P(Λ8 )) = π 4 /384.


   2.2   Constructing Viazovska’s Magic Function in Lean

   There are deep theoretical challenges to the construction of such a function, and
   Viazovska’s ingenuity was to use quasimodular forms to circumvent them. g is de-
   fined in [14] as a linear combination of radial, Schwartz Fourier ±1-eigenfunctions
   a and b with double zeroes at lattice points, defined as follows:
           Z i                                         Z i           
                     −1                 2 πi∥x∥2 z                 −1              2      2
   a(x) :=     ϕ0             (z + 1) e            dz +      ϕ0             (z − 1) eπi∥x∥ z dz
            −1     z+1                                    1       z−1
               Z i                                Z i∞
                       −1                  2                            2
           −2     ϕ0            z 2 eπi∥x∥ z dz + 2        ϕ0 (z) eπi∥x∥ z dz
                0       z                             i
           Z i                                         Z i            
                      −1                2 πi∥x∥2 z                   −1             2       2
   b(x) :=     ψS              (z + 1) e           dz +      ψS              (z − 1) eπi∥x∥ z dz
            −1      z + 1                                 1        z − 1
               Z i                                 Z i∞
                       −1                   2                             2
           −2     ψS             z 2 eπi∥x∥ z dz − 2        ψS (z) eπi∥x∥ z dz
                0        z                             i
            πi             i                                                   Im
   g(x) :=      a(x) +          b(x)
           8640        240π
   Denote by E2 , E4 , E6 the weight 2, 4, 6 Eisenstein                    z6
                                                                         z2          z4
   Series; ∆ the discriminant form; and θ10 , θ00 , θ01      −1 + i •           •         •1 + i
                                                                                 i
   the Jacobi theta functions. Define ϕ0 and ψS in                z1      z5                  z3
   terms of these quasimodular forms as follows:                    •           •         •        Re
                                 2                                  −1          0         1
                (E2 E4 − E6 )
           ϕ0 :=
                    ∆ 4     4     4      4
                                                               Figure 1: Choosing
                     θ01  − θ10   θ10  + θ00                   contours of integration
          ψS := 128       8     −      8
                         θ00          θ01
                       Progress in Formalizing Sphere Packing in Dimension 8         5

The above informal definitions of a and b do not specify contours for the con-
stituent integrands. Since the integrands are holomorphic on the upper half-
plane, from a strictly mathematical perspective, the choice of contours is im-
material. However, since mathlib lacks sufficient contour integration machinery,
we were forced to make a choice of contour when defining a and b in Lean. A
crucial step in the proof requires the deformation of unbounded contours (see [7,
§4.4]), and we realized that the best contour shape for such a deformation is rect-
angular, because mathlib contains a proof of the Cauchy-Goursat Theorem for
rectangular contours. We therefore defined rectangular parametrizations z1 to z6
(as shown in Figure 1) and defined a = I1 +· · ·+I6 and b = J1 +· · ·+Jk , where Ik
and Jk are the integrals along zk with the same integrands as the informal defi-
nition. We successfully proved unbounded rectangular Cauchy-Goursat10 , which
was used in PR #229 to prove that a is expressible in the following form
                                       !Z
                                     2     i∞        
                               π ∥x∥               −1             2
              a(x) = −4 sin 2
                                              ϕ0        z 2 e−π∥x∥ t dz         (1)
                                  2      0         z
                            √
for all x ∈ R8 with ∥x∥ ≥ 2. Replacing ϕ0 with                     Im
ψS in (1) yields an analogous expression for b.                            1+i
The significance of these representations is that          i       •       •
when analytically continued to account for all val-
ues of x ∈ R8 , they yield a convenient expression
for g as a certain Laplace transform. A direct                     •       •   Re
                                                               0           1
computation then shows (CE1), and the proofs of
(CE2) and (CE3) can be reduced, using the facts        Figure 2: Contour needed
that ba = a and bb = −b (where b· is the Fourier       for eigenfunction property
transform), to the inequalities

                             36                                    36
              0 < ϕ0 (z) +      ψS (z)            0 < ϕ0 (z) −        ψS (z)        (2)
                             π2                                    π2
 when restricted to the positive imaginary axis [10, (3), (4)]. The informal and
 formal machinery for this was largely developed by Lee based on [10].
     Prior to the autoformalization, we did not have a formal proof that ba = a and
bb = −b. These arguments require a version of the Cauchy-Goursat Theorem for
 contours of the shape depicted in Figure 2 (see [7, §4.3]), which we had not yet
 formalized. What made this formalization particularly tricky is that the contour
 touches the real line, where the integrands, made up of quasimodular forms,
 were not defined. The saving grace is that in this instance, the integrands vanish
 because the real line is approached vertically. The Gauss formalization, which
 shall be discussed in more detail in Section 3, does include a proof that contours
 of these specific shapes can be deformed. As the project progresses, we would
 like to generalize the argument to a broader class of contours.
10
     Equivalent results were independently proven by contributors to Kontorovich and
     Tao’s open-source PrimeNumberTheoremAnd formalization project [9]
6      S. Hariharan et al.

2.3   The Theory of (Quasi)Modular Forms

The proof that the magic function satisfies the required properties depends heav-
ily on the basic theory of modular forms. Fortunately, when the Sphere packing
project began, mathlib already contained many of the definitions and proper-
ties of the Eisenstein series and Jacobi theta functions that we would require.
The main development in this area done as part of this project was construct-
ing E2 and ∆ and proving the dimension formulas in level one, which were
essential for proving identities between combinations of modular forms, such as
∆ = (E43 − E62 )/1728.
    The magic function also uses the weight 2 Eisenstein series E2 , which is
also formalized and already upstreamed to mathlib as EisensteinSeries.E2.
                                                          1 d
We also formalized the normalized derivative D := 2πi       dz and Serre deriva-
                  k
tive ∂k := D − 12 E2 . Combined with the dimension formula for level 1 modu-
lar forms, we proved Ramanujan’s identities on derivatives of Eisenstein series
and derivatives of Jacobi theta functions (see RamanujanIdentities.lean and
ThetaDerivIdentities.lean under SpherePacking/ModularForms), which are
used to prove various quasimodular form identities used in the proof of the in-
                                                                   4     4     4
equalities [10]. As a by-product, we also proved Jacobi identity θ00  = θ10 + θ01 .
    While the majority of the modular form theory required for this project
is standard (see [4] for instance), a notable obstacle was proving the dimension
formula for spaces of modular forms, which, given the lack of contour integration
machinery in mathlib, required a non-standard proof. The details of this and
other non-standard proofs will be discussed in a forthcoming paper.
    To prove the modular form inequalities (2), we first defined ResToImagAxis,
the restriction of F : H → C to R, by assigning F (it) for t > 0 and 0 otherwise:
def ResToImagAxis (F : H → C) : R → C :=
  fun t => if ht : 0 < t then F ⟨(I * t), by simp [ht]⟩ else 0

We proved basic properties on realness, positiveness, and how it interacts with
(Serre) derivatives (see SpherePacking/ModularForms/ResToImagAxis.lean).
The inequalities (2) will be proved in PR #331 as FG_inequality_1 and FG_inequality_2,
following the argument of [10].


2.4   Metaprogramming

A rather unexpected outcome of the project so far has been the development
of metaprogramming techniques to assist with computations. The first advance-
ment was the development of norm_numI, a normalization-simplification proce-
dure to bring norm_num-like functionality to the complex numbers. The tactic
recursively parses an expression in C, splits all atoms into their real and imag-
inary parts, calls norm_num on their real and imaginary parts, and recombines
them using the rules of complex arithmetic to return a normalised, simplified
expression in C. The key insight was identifying that the right ‘normal form’
for an expression in C is a + bi, where a, b ∈ R are both in normal form (in the
sense of norm_num). The second tactic developed was tendsto_cont, which uses
                     Progress in Formalizing Sphere Packing in Dimension 8         7

the continuity of the projection maps from a product of topological spaces to
prove goals of the form Tendsto (fun z => expr(f1 z, . . ., fn z)) l (nhds c)
where atomic limits Tendsto fi l (nhds ai ) are known from context and expr is
continuous in the atoms (proved via fun_prop). We use it to simplify the proof
                                                                           4     4
of the limit of quasimodular forms that are polynomials in E2 , E4 , E6 , θ10 , θ01 .


3   Autoformalization
Working from the existing blueprint and Lean development, the autoformaliza-
tion model ‘Gauss’ completed a sorry-free formalization of the main theorem in
five days, taking the project from about 20 000 lines to 80 000 lines. A subsequent
compression and refactoring pass reduced the development to 60 000 lines. This
archived artifact is available in PR #341. Interestingly, it was easier to generate
the proof than to clean up and golf the code from 80k lines to 60k. This high-
lights that the next frontier in autoformalization is not so much getting a proof
formalized as doing this while writing high-quality reusable code.
    Among the main proofs completed by Gauss were the dimension 8 contour-
deformation identities used in the Fourier eigenfunction argument, including the
wedge-set deformation based on the Poincaré lemma. In PR #341, these appear
in PermI12ContourMain.lean and PermJ12ContourDeformation.lean. Gauss
also completed the finite-dimensionality theory for modular forms on finite-index
subgroups, recorded in DimensionFormulas.lean and FiniteDimensional.lean.
This general result had already been envisaged in the blueprint as a natural
corollary of the surrounding work, although it was not strictly required for the
sphere-packing theorem itself.
    One stylistic feature of the Gauss contribution is that it introduced many
small auxiliary definitions with little or no API attached, many of which a human
formalizer would ordinarily inline directly into proofs. A human formalizer would
often pause to factor out reusable lemmas and eliminate duplication. Gauss, by
contrast, was often content to repeat local patterns. There was a great deal of
variation in the mathematical complexity of the Gauss code: it would, at times,
write very complex proofs spanning hundreds of lines, yet also prove trivial facts
(like 4 = 2 + 2) or special cases of mathlib results (like Fourier transforms of
Gaussians with specific variances). Both extremes are undesirable: long proofs
are much harder to maintain and take longer to compile, and reproving results
just adds duplication to the codebase. As we clean the Gauss code to bring it
up to mathlib standards, we are paying particular attention to these extremes.


4   A Look to the Future
As AI models and companies take on more prominent roles in formalization
projects, it is worth considering the implications for the practice of mathematics,
formal and informal. Some analysis has already been done on the role of Math,
Inc in the sphere packing effort [1,3] in which both skepticism and optimism are
expressed. Of the initial motivations for this project, Avigad writes [1, p. 3],
8       S. Hariharan et al.

    “[T]he correctness of Viazovska’s result was never in doubt. The partici-
    pants embraced the project, rather, as a way of revisiting [Viazovska’s]
    results and better understanding them, and of building libraries and in-
    frastructure to support future work.”

Gauss, on the other hand, took a more direct route to the verification, which did
not completely comply with these objectives. The skepticism on the use of such
autoformalization models stems from the initial misalignment of these objectives,
and the optimism stems from the belief that the ongoing public collaboration to
realign them will motivate the AI for mathematics industry to better consider
the objectives of large-scale formalization projects when designing their models.
    On a purely technical level, the project was not strictly set up to verify Via-
zovska’s original argument in its entirety, but rather, the modified (if only slightly
so) argument in the project blueprint, which differs from the original most no-
tably in its use of Lee’s original proof [10] of the inequalities (2). Furthermore,
given the sheer volume of the Gauss code, the exact correspondence between the
autoformalization and the intended proof path is still being investigated, and
new proofs might still be used to complete certain parts of the project.
    Nevertheless, the construction of a sorry-free proof of the sphere packing
problem represents a unique achievement for formal mathematics and machine
learning alike. Gauss directly used the human-written Lean code and blueprint,
underscoring the importance of robust definitions, detailed proof strategies, and
thoughtful design choices in any (auto)formalization workflow. The remainder of
the project promises to be immensely interesting, from the formal and informal
perspectives alike, and once the project is finished, a complete account of our
learnings, along with more technical details of the work done to finish the project,
will appear in a forthcoming paper.


Acknowledgments. The authors are deeply grateful to the many contributors, di-
rect and indirect, to the open-source formalization effort, most notably Matthew Cush-
man, Cameron Freer, Yongxi Lin, David Loeffler, Heather Macbeth, Pietro Monticone,
Aayush Rajasekaran, David Renshaw, Tito Sacchi, Utensil Song, and Yunzhou Xie. The
authors also acknowledge the invaluable support of the Lean formalization community,
most notably Jeremy Avigad, Kevin Buzzard, Leonardo de Moura, Emily Riehl, and
the maintainers of mathlib. The first author conducted significant portions of this work
as an exchange student and subsequently as a research intern at the École Polytech-
nique Fédérale de Lausanne under the supervision of the seventh author, and later for
his master’s project [7] at Imperial College London under the supervision of the fifth
author. The first author also acknowledges travel support from the Hoskinson Center
for Formal Mathematics at Carnegie Mellon University. The sixth author gratefully ac-
knowledges the support of DARPA’s expMath program for the development of Gauss.
The sixth and seventh authors acknowledge Renaissance Philanthropy’s AI for Math
Fund for supporting autoformalization research at EPFL. The authors further acknowl-
edge support from the Institute for Computer-Aided Reasoning in Mathematics on AI
policy advice and thank G-Research for sponsoring their weekly ‘packathons’.
                      Progress in Formalizing Sphere Packing in Dimension 8            9

References
 1. Avigad, J.: Mathematicians in the age of AI. arXiv preprint arXiv:2603.03684
    (2026), https://arxiv.org/abs/2603.03684
 2. Cohn, H., Elkies, N.: New Upper Bounds on Sphere Packings I. Annals of Math-
    ematics 157(2), 689–714 (2003). https://doi.org/https://doi.org/10.4007/
    annals.2003.157.689, http://www.jstor.org/stable/3597215
 3. DeDeo, S., Duede, E.: A correspondence problem for mathematical proof. arXiv
    preprint arXiv:2603.13680 (2026), https://arxiv.org/abs/2603.13680
 4. Diamond, F., Shurman, J.: A First Course in Modular Farms. No. 228 in Graduate
    Texts in Mathematics, Springer New York, NY, New York, first edn. (March 2006).
    https://doi.org/https://doi.org/10.1007/978-0-387-27226-9
 5. Hales, T.C.: A Proof of the Kepler Conjecture. Annals of Mathematics 162(3),
    1065–1185 (2005). https://doi.org/https://doi.org/10.4007/annals.2005.
    162.1065, http://www.jstor.org/stable/20159940
 6. Hales, T.C., Adams, M., Bauer, G., Dang, T.D., Harrison, J., Hoang, L.T.,
    Kaliszyk, C., Magron, V., Mclaughlin, S., Nguyen, T.T., Nguyen, Q.T., Nipkow,
    T., Obua, S., Pleso, J., Rute, J., Solovyev, A., Ta, T.H.A., Tran, N.T., Trieu, T.D.,
    Urban, J., Vu, K., Zumkeller, R.: A Formal Proof of the Kepler Conjecture. Forum
    of Mathematics, Pi 5, e2 (2017). https://doi.org/10.1017/fmp.2017.1
 7. Hariharan, S.: Viazovska’s Magic Function in Dimension 8: An At-
    tempt at Formalisation. MSci Thesis, Imperial College London (2025),
    https://thefundamentaltheor3m.github.io/M4R_Thesis/main.pdf, Supervised
    by Bhavik Mehta.
 8. Kepler, J.: Strena seu de nive sexangula. Francofurti ad Moenum : apud
    Godefridum Tampach (1611). https://doi.org/https://doi.org/10.3931/
    e-rara-478, https://www.e-rara.ch/zut/content/titleinfo/135387, ETH-
    Bibliothek Zürich, Rar 4342: 2, https://doi.org/10.3931/e-rara-478
 9. Kontorovich, A., Tao, T.: Prime Number Theorem and More (Jan 2024), https:
    //github.com/AlexKontorovich/PrimeNumberTheoremAnd
10. Lee, S.: Algebraic proof of modular form inequalities for optimal sphere packings
    (2024), https://arxiv.org/abs/2406.14659
11. de Moura, L., Kong, S., Avigad, J., van Doorn, F., von Raumer, J.: The Lean
    Theorem Prover (System Description). In: Felty, A.P., Middeldorp, A. (eds.) Au-
    tomated Deduction - CADE-25. pp. 378–388. Springer International Publishing,
    Cham (2015)
12. Thue, A.: Om nogle geometrisk-taltheoretiske Theoremer. Forhandlingerne ved de
    Skandinaviske Naturforskeres 14 (1892), zbl 24.0259.01
13. Tóth, L.F.: Über die dichteste Kugellagerung. Mathematische Zeitschrift 48(1),
    676–684 (Dec 1942). https://doi.org/10.1007/BF01180035, https://doi.org/
    10.1007/BF01180035
14. Viazovska, M.S.: The sphere packing problem in dimension 8. Annals of Math-
    ematics 185(3), 991–1015 (2017). https://doi.org/https://doi.org/10.4007/
    annals.2017.185.3.7, http://www.jstor.org/stable/26395747
