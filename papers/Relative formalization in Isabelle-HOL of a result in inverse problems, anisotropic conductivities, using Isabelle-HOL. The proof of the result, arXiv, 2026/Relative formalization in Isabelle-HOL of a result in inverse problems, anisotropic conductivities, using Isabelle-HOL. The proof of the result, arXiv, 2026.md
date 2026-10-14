                                             RELATIVE FORMALIZATION IN ISABELLE/HOL OF A
                                                     RESULT IN INVERSE PROBLEMS

                                                                          CĂTĂLIN I. CÂRSTEA
arXiv:2608.23659v1 [math.AP] 24 Aug 2026




                                                   Abstract. This reports on an experiment in autoformalization of
                                                   arxiv:2606.15977, an inverse problems result for piecewise polynomial
                                                   anisotropic conductivities, using Isabelle/HOL. The proof of the result
                                                   is relative to a number of external results which were deemed to be well
                                                   known and generally accepted to be true. The formalization files are
                                                   made available at a GitHub repository. Translation issues are discussed.




                                                                           1. Introduction
                                              It has been observed [2, 10, 8] that AI generated mathematical prose may,
                                           at times, be harder to read and to check than more traditionally written
                                           books and papers. This leads to the justified concern that false results
                                           may now enter the published record at higher rates than in the past [2].
                                           One of the solutions that are beginning to arise in response is the use of
                                           formalization, which is now more accessible to more researchers, also thanks
                                           to the availability of AI tools [2, 14]. Most recent reports use Lean, including
                                           formalizations of modern PDE results [3, 9], AI-assisted work on Erdős
                                           problems [11, 12], and collections of formalized research papers in other areas
                                           [13]; see also the survey [14]. Isabelle/HOL has also been used [15, 18, 4, 7],
                                           as well as other systems such as Coq/Rocq [6, 17].
                                              As an experiment and learning exercise I have attempted to formalize one
                                           of my recent preprints [1]. Anecdotally, formalization in Lean appears to be
                                           somewhat expensive in terms of both time and money. For this experiment
                                           I have opted for Isabelle/HOL as the formalization language, and have used
                                           Codex and ChatGPT 5.6 Sol with a $200/month subscription to produce
                                           the formalization. The final result was produced in under a week, which
                                           would put the monetary cost of the exercise at about $50. At these costs
                                           formalizing a paper becomes more feasible as a routine additional verification
                                           step.
                                              This paper and the experiment it reports on is meant as a proof of concept.
                                           It undoubtedly has many weaknesses. I gladly welcome any constructive
                                           criticism and suggestions.


                                             Date: August 26, 2026.
                                                                                      1
2                            CĂTĂLIN I. CÂRSTEA

                            2. What was done
    The formalization translates the main theorem, with its hypotheses and
relevant definitions into Isabelle/HOL, then reconstructs the proof as a se-
quence of machine-checked lemmas. One key decision taken was to assume,
rather than prove, certain results taken from literature. Without this mea-
sure the formalization work would have probably taken considerably more
time. Each cited result is also translated into Isabelle and appears within
an Isabelle “locale”. These assumptions are visible in the dependency struc-
ture. The final theorem records that the claimed conclusion follows from
Isabelle’s logical foundations and libraries, together with this explicitly iden-
tified literature base. The formalization was considered complete when Is-
abelle checked the exact intended theorem (the Isabelle language version!)
from beginning to end, with no omitted proofs or provisional assumptions,
and when every dependency belonged either to the checked Isabelle libraries,
to a proved component of the project, or to one of the declared literature
interfaces.
    The workflow used treats the formalization as a single, extended, long
running project. Codex provided the general ability to read the mathe-
matical source, search the Isabelle libraries, write and check formal proofs,
and use available tools. I supplemented this with a project-specific harness,
consisting mainly of a library of reusable instructions and a collection of
project files specifying rules of operation, available tools, templates, and
the mathematical context that was to be preserved. A useful feature of the
setup is that it can be given relatively long tasks and be allowed to work
on them with little supervision. The surrounding harness provided continu-
ity and discipline for these longer runs, including instructions about what
information was to be treated as fixed and when a question should be left
for human review. This made it possible to carry out a substantial amount
of formalization and checking without continuous interaction, while leaving
the resulting Isabelle files and a record of the intermediate work available
for later inspection.
    The formalization code can be found at https://github.com/catalin-carstea/
arxiv-2606.15977-formalization.


                      3. The translation problem
   Besides the possibility of bugs in the Isabelle kernel, the approach taken
here has a clear weakness: translation. The total size of the Isabelle code for
the theorem proven, the definitions and imported literature results is about
50KB, or about 1,400 lines of code. This would be hard to check for a human
reader in a reasonable amount of time, even with perfect understanding of
Isabelle language. I have instead resorted to a number of other approaches
which may not lead to perfect confidence in the accuracy of what was done,
but may at least suggest that the effort has some significance.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     3

   It may be worth noting that a small mistake in translating the main
theorem, unless it reduces it to a known result or a trivial one, might be
less serious if it only means that the English language theorem is slightly
misstated. A small mistake in translating a known result from a monograph,
on the other hand, could in principle invalidate the whole project, as such
results are often optimal or nearly optimal.
Translation testing approaches.

1. All translations have been checked and approved by both ChatGPT 5.6
Sol Pro (in the chat, outside the Codex context where they were produced)
and by Claude Opus 5.

2. The translation of the main theorem was done first, before any of the
other formalization work, and was kept fixed throughout. This measure was
intended to prevent the LLM from independently altering the statement
until it got something that would allow it to more quickly finish its task
[16, 5]. Translations of cited results were also frozen after being made, for the
same reason. Incidentally, in this particular experiment, it became necessary
to revise the translations once during the formalization process. The version
of the paper that was given to Codex was imprecise regarding what is meant
by a “Lipschitz domain”, and the initial translation took it in a sense that
was different from what one of the cited results used.

3. In order to check the translations of the literature results, I have asked
ChatGPT 5.6 Sol in Codex (effort: extra high) to try for 24 hours to derive
a contradiction between the translated statements and the Isabelle libraries1.
It found none.

4. Finally, I have had Codex translate the Isabelle code versions of the defi-
nitions and statements of the main theorem and imported literature results
back into English, using subagents that were not given access to the original
manuscripts. Though not perfect, this method does should give a degree
of confidence in the accuracy of translations, as two translation errors can-
celing each other should be a unlikely To make the approach more robust,
this was done twice, independently. The results of this effort are included
as Appendices A and B, in the form of interlinear translations with Isabelle
code and its English translation for definitions, and English original, Isabelle
code, and translation back to English for theorem statements.

                         4. Provisional conclusions
   In a strict mathematical sense, without perfect confidence in the cor-
respondence between natural language mathematical statements and their
corresponding Isabelle code translations this experiment proves little. It is
my personal impression however that, together with a sufficient number of
  1I would like to thank Matti Lassas for this idea.
4                           CĂTĂLIN I. CÂRSTEA

varied translation tests, the existence of a formalization that checks does
raise the level of confidence in the result somewhat. To be sure, even a
traditionally written and peer reviewed paper may on occasion turn out to
contain errors. A question one may ask, even though it is probably ill-posed,
is then: can formalization raise the confidence level at least to match what
would usually be assigned to traditional work? This seems to require more
reflection and experimentation.
   On the practical side, the experiment does show that relative formaliza-
tion in Isabelle/HOL is achievable at least in some cases. With more future
attempts we may end up in a better position to answer the more philosoph-
ical questions above.

Acknowledgements. I am grateful to Lauri Oksanen for many constructive
discussions. This work was supported by NSTC grant 113-2115-M-A49-018-
MY3.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     5

            Appendix A. Independent back-translation A

Definitions

cgu_point
Isabelle code

 type_synonym ’n cgu_point = "real ^ ’n"


English mathematical translation
Mathematical role: Euclidean vector type Rn
   For any index type ’n, cgu point is the type of real-valued vectors indexed by
’n, namely real ^ ’n.
cgu_monomial
Isabelle code

 type_synonym ’n cgu_monomial = "’n \<Rightarrow>\<^sub>0 nat"


English mathematical translation
Mathematical role: finitely supported multi-index α
   For any type ’n, cgu monomial is the type of finitely supported mappings from
’n to natural numbers.
cgu_polynomial
Isabelle code

 type_synonym ’n cgu_polynomial = "’n cgu_monomial \<Rightarrow>\<^sub>0 real"


English mathematical translation
Mathematical role: finitely supported scalar coefficient family (pα )
   For any type ’n, cgu polynomial is the type of finitely supported mappings
from objects of type cgu monomial to real numbers.
cgu_matrix_polynomial
Isabelle code

 type_synonym ’n cgu_matrix_polynomial = "’n cgu_polynomial ^ ’n ^ ’n"


English mathematical translation
Mathematical role: coefficient-represented matrix polynomial P = (pij )
   For any type ’n, cgu matrix polynomial is an ’n-by-’n vector-of-vectors whose
entries have type cgu polynomial.
cgu_monomial_total_degree
Isabelle code
6                                 CĂTĂLIN I. CÂRSTEA


    definition cgu_monomial_total_degree :: "’n cgu_monomial \<Rightarrow> nat"
    where
      "cgu_monomial_total_degree m =
        (\<Sum>i\<in>Poly_Mapping.keys m. Poly_Mapping.lookup m i)"


English mathematical translation
Mathematical role: total degree of a multi-index
  For m : cgu monomial, cgu monomial total degree m is the natural-number
sum, over all keys in the finite support of m, of the value looked up at that key.
cgu_poly_degree_le
Isabelle code
    definition cgu_poly_degree_le :: "nat \<Rightarrow> ’n cgu_polynomial \<Rightarrow>
          bool"
    where
      "cgu_poly_degree_le d p \<longleftrightarrow>
        (\<forall>m\<in>Poly_Mapping.keys p. cgu_monomial_total_degree m \<le> d)"


English mathematical translation
Mathematical role: stored degree predicate deg∗ p ≤ d
  cgu poly degree le d p holds exactly when every m in the finite support of p
: cgu polynomial satisfies cgu monomial total degree m <= d. The universal
condition is vacuous when the support of p is empty.
cgu_monomial_eval
Isabelle code
    definition cgu_monomial_eval ::
      "’n cgu_monomial \<Rightarrow> ’n::finite cgu_point \<Rightarrow> real"
    where
      "cgu_monomial_eval m x =
        (\<Prod>i\<in>Poly_Mapping.keys m. x $ i ^ Poly_Mapping.lookup m i)"


English mathematical translation
Mathematical role: monomial xα
   For a finite index type ’n, cgu monomial eval m x is the product over all indices
i in the finite support of m of (x i)^(m(i)).
cgu_poly_eval
Isabelle code
    definition cgu_poly_eval ::
      "’n cgu_polynomial \<Rightarrow> ’n::finite cgu_point \<Rightarrow> real"
    where
      "cgu_poly_eval p x =
        (\<Sum>m\<in>Poly_Mapping.keys p.
          Poly_Mapping.lookup p m * cgu_monomial_eval m x)"


English mathematical translation
Mathematical role: polynomial evaluation pb(x)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     7

   For finite ’n, cgu poly eval p x is the finite sum over every m in the support
of p of the coefficient p(m) times cgu monomial eval m x.
cgu_matrix_poly_eval
Isabelle code

 definition cgu_matrix_poly_eval ::
   "’n::finite cgu_matrix_polynomial \<Rightarrow> ’n cgu_point \<Rightarrow>
     real ^ ’n ^ ’n"
 where
   "cgu_matrix_poly_eval P x = (\<chi> i j. cgu_poly_eval (P $ i $ j) x)"


English mathematical translation
Mathematical role: matrix evaluation Pb(x)
  For finite ’n, cgu matrix poly eval P x is the real ’n-by-’n matrix whose
(i,j) entry is cgu poly eval (P[i,j]) x.
cgu_matrix_poly_degree_le
Isabelle code

 definition cgu_matrix_poly_degree_le ::
   "nat \<Rightarrow> ’n::finite cgu_matrix_polynomial \<Rightarrow> bool"
 where
   "cgu_matrix_poly_degree_le d P \<longleftrightarrow>
     (\<forall>i j. cgu_poly_degree_le d (P $ i $ j))"


English mathematical translation
Mathematical role: entrywise stored degree bound
   For finite ’n, cgu matrix poly degree le d P holds exactly when, for every
pair of indices i,j, every supported exponent mapping of the entry P[i,j] has
total cgu monomial total degree value at most d.
cgu_symmetric_matrix_polynomial
Isabelle code

 definition cgu_symmetric_matrix_polynomial ::
   "’n::finite cgu_matrix_polynomial \<Rightarrow> bool"
 where
   "cgu_symmetric_matrix_polynomial P \<longleftrightarrow>
     (\<forall>i j. P $ i $ j = P $ j $ i)"


English mathematical translation
Mathematical role: coefficient symmetry
  For finite ’n, cgu symmetric matrix polynomial P holds exactly when P[i,j]
= P[j,i] for every i,j.
cgu_matrix_bilinear
Isabelle code
8                                 CĂTĂLIN I. CÂRSTEA


    definition cgu_matrix_bilinear ::
      "(real ^ ’n::finite ^ ’n) \<Rightarrow> real ^ ’n \<Rightarrow>
        real ^ ’n \<Rightarrow> real"
    where
      "cgu_matrix_bilinear A x y = inner x (A *v y)"


English mathematical translation
Mathematical role: bilinear value x · Ay
   For a real square matrix A and real vectors x,y of the same finite coordinate
type, cgu matrix bilinear A x y is the inner product of x with the matrix-vector
product A*y.
cgu_symmetric_positive_definite_matrix
Isabelle code
    definition cgu_symmetric_positive_definite_matrix ::
      "(real ^ ’n::finite ^ ’n) \<Rightarrow> bool"
    where
      "cgu_symmetric_positive_definite_matrix A \<longleftrightarrow>
        transpose A = A \<and>
        (\<forall>x. x \<noteq> 0 \<longrightarrow> 0 < cgu_matrix_bilinear A x x)"


English mathematical translation
Mathematical role: symmetric positive-definite matrix
  cgu symmetric positive definite matrix A holds exactly when both:
      • transpose A = A; and
      • for every vector x, if x != 0, then 0 < cgu matrix bilinear A x x.
  Thus the second conjunct is strict positivity only on nonzero vectors.
cgu_uniformly_positive_definite_on
Isabelle code
    definition cgu_uniformly_positive_definite_on ::
      "’n::finite cgu_point set \<Rightarrow> ’n cgu_matrix_polynomial \<Rightarrow>
         bool"
    where
      "cgu_uniformly_positive_definite_on D P \<longleftrightarrow>
        (\<exists>k>0. \<forall>x\<in>D. \<forall>xi.
          k * norm xi ^ 2 \<le>
            cgu_matrix_bilinear (cgu_matrix_poly_eval P x) xi xi)"


English mathematical translation
Mathematical role: uniform ellipticity on a set
   For finite ’n, cgu uniformly positive definite on D P holds exactly when
there exists one real k > 0 such that, for every x in D and every vector xi, k *
||xi||^2 <= cgu matrix bilinear (cgu matrix poly eval P x) xi xi. The
same k must work for all x and xi.
cgu_model
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     9


 record (’n, ’c, ’h) cgu_model =
   cgu_domain :: "’n cgu_point set"
   cgu_measured :: "’n cgu_point set"
   cgu_cell :: "’c \<Rightarrow> ’n cgu_point set"
   cgu_degree :: "’c \<Rightarrow> nat"
   cgu_order :: "nat \<Rightarrow> ’c"
   cgu_faces :: "’c \<Rightarrow> ’h set"
   cgu_normal :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point"
   cgu_offset :: "’c \<Rightarrow> ’h \<Rightarrow> real"
   cgu_face_patch :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point set"
   cgu_witness_faces :: "’c \<Rightarrow> ’h \<Rightarrow> ’h set"
   cgu_triple_region :: "’c \<Rightarrow> ’h \<Rightarrow> ’h \<Rightarrow> ’h \<
      Rightarrow>
     ’n cgu_point set"
   cgu_step_interface_pieces :: "’c \<Rightarrow> ’h set"
   cgu_step_interface_patch :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point set"
   cgu_step_interface_normal :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point"
   cgu_step_interface_offset :: "’c \<Rightarrow> ’h \<Rightarrow> real"
   cgu_step_outer_patch :: "’c \<Rightarrow> ’n cgu_point set"
   cgu_step_adjacent_cell :: "’c \<Rightarrow> ’c"
   cgu_step_center :: "’c \<Rightarrow> ’n cgu_point"
   cgu_step_interior_normal :: "’c \<Rightarrow> ’n cgu_point"
   cgu_step_radius :: "’c \<Rightarrow> real"


English mathematical translation
Mathematical role: geometric record M ; its 20 fields map as follows: cgu domain Ω,
cgu measured Γ, cgu cell Ωc , cgu degree Nc , cgu order σ, cgu faces Ic , cgu
normal νc,i , cgu offset bc,i , cgu face patch γc,i , cgu witness faces Jc,i , cgu
triple region Wc,i,j,k , cgu step interface pieces auxiliary label set, cgu step
interface patch auxiliary patch, cgu step interface normal auxiliary normal,
cgu step interface offset auxiliary offset, cgu step outer patch Λc , cgu
step adjacent cell a(c), cgu step center qc , cgu step interior normal µc ,
cgu step radius rc
    cgu model is a record with type parameters ’n, ’c, and ’h and the following
fields, with no class restrictions imposed by the record declaration itself:
      • cgu domain: a set of ’n-indexed real vectors;
      • cgu measured: another such set;
      • cgu cell: from each ’c to such a set;
      • cgu degree: from each ’c to a natural number;
      • cgu order: from natural numbers to ’c;
      • cgu faces: from each ’c to a set of ’h values;
      • cgu normal: from ’c and ’h to an ’n-indexed real vector;
      • cgu offset: from ’c and ’h to a real number;
      • cgu face patch: from ’c and ’h to a set of ’n-indexed real vectors;
      • cgu witness faces: from ’c and ’h to a set of ’h values;
      • cgu triple region: from ’c and three ’h values to a set of ’n-indexed
        real vectors;
      • cgu step interface pieces: from each ’c to a set of ’h values;
      • cgu step interface patch: from ’c and ’h to a set of ’n-indexed real
        vectors;
      • cgu step interface normal: from ’c and ’h to an ’n-indexed real vector;
10                             CĂTĂLIN I. CÂRSTEA

      • cgu step interface offset: from ’c and ’h to a real number;
      • cgu step outer patch: from each ’c to a set of ’n-indexed real vectors;
      • cgu step adjacent cell: from ’c to ’c;
      • cgu step center: from ’c to an ’n-indexed real vector;
      • cgu step interior normal: from ’c to an ’n-indexed real vector; and
      • cgu step radius: from ’c to a real number.

cgu_piecewise_polynomial_class
Isabelle code

 definition cgu_piecewise_polynomial_class ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> bool"
 where
   "cgu_piecewise_polynomial_class M P \<longleftrightarrow>
     (\<forall>c.
       cgu_matrix_poly_degree_le (cgu_degree M c) (P c) \<and>
       cgu_symmetric_matrix_polynomial (P c) \<and>
       cgu_uniformly_positive_definite_on (cgu_cell M c) (P c))"


English mathematical translation
Mathematical role: admissible coefficient family
  For finite ’n and finite ’c, cgu piecewise polynomial class M P holds exactly
when, for every c, all three conditions hold: P c satisfies cgu matrix poly degree
le with bound cgu degree M c; P c satisfies cgu symmetric matrix polynomial;
and P c satisfies cgu uniformly positive definite on on cgu cell M c.
cgu_affine_hyperplane
Isabelle code

 definition cgu_affine_hyperplane ::
   "’n::finite cgu_point \<Rightarrow> real \<Rightarrow> ’n cgu_point set"
 where
   "cgu_affine_hyperplane normal offset = {x. inner normal x = offset}"


English mathematical translation
Mathematical role: hyperplane H(ν, b)
   For finite ’n, cgu affine hyperplane normal offset is the set of all vectors x
satisfying inner normal x = offset.
cgu_coordinate_hyperplane_projection_v5
Isabelle code

 definition cgu_coordinate_hyperplane_projection_v5 ::
   "’i::finite \<Rightarrow> ’i cgu_point \<Rightarrow> ’i cgu_point"
 where
   "cgu_coordinate_hyperplane_projection_v5 i y =
     (\<chi> j. if j = i then 0 else y $ j)"


English mathematical translation
Mathematical role: coordinate-deleted vector y (i)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     11

  For finite ’i, cgu coordinate hyperplane projection v5 i y is the vector
whose jth coordinate is zero if j=i, and is y j otherwise.
cgu_local_lipschitz_boundary_at
Isabelle code
 definition cgu_local_lipschitz_boundary_at ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> bool"
 where
   "cgu_local_lipschitz_boundary_at D x \<longleftrightarrow>
     (\<exists>(U :: ’n cgu_point set)
        (f :: ’n cgu_point \<Rightarrow> ’n cgu_point)
        (g :: ’n cgu_point \<Rightarrow> ’n cgu_point) (i :: ’n) L M.
       open U \<and> x \<in> U \<and> 0 < L \<and> 0 < M \<and>
       homeomorphism U (f ‘ U) f g \<and>
       lipschitz_on L U f \<and> lipschitz_on M (f ‘ U) g \<and>
       f ‘ (D \<inter> U) = (f ‘ U) \<inter> {y. 0 < y $ i})"


English mathematical translation
Mathematical role: local bi-Lipschitz half-space chart
   For finite ’n, cgu local lipschitz boundary at D x holds exactly when there
exist a set U, functions f,g, an index i, and real constants L,M such that:
       • U is open and contains x;
       • L>0 and M>0;
       • f and g give a homeomorphism between U and f(U);
       • f is L-Lipschitz on U, and g is M-Lipschitz on f(U); and
       • f(D intersect U) is exactly f(U) intersect {y | 0 < y i}.
   All witnesses are inside one existential scope.
cgu_lipschitz_domain
Isabelle code
 definition cgu_lipschitz_domain ::
   "’n::finite cgu_point set \<Rightarrow> bool"
 where
   "cgu_lipschitz_domain D \<longleftrightarrow>
     D \<noteq> {} \<and> open D \<and> connected D \<and> bounded D \<and>
     (\<forall>x\<in>frontier D. cgu_local_lipschitz_boundary_at D x)"


English mathematical translation
Mathematical role: bi-Lipschitz half-space domain
  cgu lipschitz domain D holds exactly when D is nonempty, open, connected,
and bounded, and every x in frontier D satisfies cgu local lipschitz boundary
at D x.
cgu_rigid_motion_v5
Isabelle code
 definition cgu_rigid_motion_v5 ::
   "(’n::finite cgu_point \<Rightarrow> ’n cgu_point) \<Rightarrow> bool"
 where
   "cgu_rigid_motion_v5 R \<longleftrightarrow>
12                             CĂTĂLIN I. CÂRSTEA

     (\<exists>A b.
       linear A \<and>
       surj A \<and>
       (\<forall>u v. inner (A u) (A v) = inner u v) \<and>
       R = (\<lambda>x. A x + b))"


English mathematical translation
Mathematical role: rigid motion
   cgu rigid motion v5 R holds exactly when there exist a function A and vector
b such that A is linear and surjective, preserves all inner products (inner (A u)
(A v) = inner u v for every u,v), and R x = A x + b for every x.
cgu_local_graph_boundary_at_v5
Isabelle code

 definition cgu_local_graph_boundary_at_v5 ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> bool"
 where
   "cgu_local_graph_boundary_at_v5 D x \<longleftrightarrow>
     (\<exists>U R i zeta L.
       open U \<and>
       x \<in> U \<and>
       cgu_rigid_motion_v5 R \<and>
       0 < L \<and>
       lipschitz_on L UNIV zeta \<and>
       R ‘ (D \<inter> U) =
         R ‘ U \<inter>
           {y. y $ i < zeta (cgu_coordinate_hyperplane_projection_v5 i y)} \<and>
       R ‘ (frontier D \<inter> U) =
         R ‘ U \<inter>
           {y. y $ i = zeta (cgu_coordinate_hyperplane_projection_v5 i y)})"


English mathematical translation
Mathematical role: local Lipschitz graph condition
   For finite ’n, cgu local graph boundary at v5 D x holds exactly when there
exist U,R,i,zeta,L such that:
       • U is open and contains x;
       • cgu rigid motion v5 R holds;
       • L>0, and zeta is L-Lipschitz on the whole vector space;
       • R(D intersect U) = R(U) intersect {y | y i < zeta(cgu
         coordinate hyperplane projection v5 i y)}; and
       • R(frontier D intersect U) = R(U) intersect {y | y i =
         zeta(cgu coordinate hyperplane projection v5 i y)}.
   The same witnesses serve both displayed equalities.
cgu_graph_lipschitz_domain_v5
Isabelle code

 definition cgu_graph_lipschitz_domain_v5 ::
   "’n::finite cgu_point set \<Rightarrow> bool"
 where
   "cgu_graph_lipschitz_domain_v5 D \<longleftrightarrow>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     13

    cgu_lipschitz_domain D \<and>
    (\<forall>x\<in>frontier D. cgu_local_graph_boundary_at_v5 D x)"


English mathematical translation
Mathematical role: Lipschitz-graph domain
   cgu graph lipschitz domain v5 D holds exactly when cgu lipschitz domain
D holds and every point x of frontier D satisfies cgu local graph boundary at
v5 D x.
cgu_locally_flat_boundary_point
Isabelle code
 definition cgu_locally_flat_boundary_point ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> bool"
 where
   "cgu_locally_flat_boundary_point D x \<longleftrightarrow>
     x \<in> frontier D \<and>
     (\<exists>normal offset U.
       normal \<noteq> 0 \<and> open U \<and> x \<in> U \<and>
       U \<inter> frontier D =
         U \<inter> cgu_affine_hyperplane normal offset)"


English mathematical translation
Mathematical role: locally flat boundary point
  cgu locally flat boundary point D x holds exactly when x belongs to
frontier D and there exist normal, offset, and an open set U containing x, with
normal != 0, such that U intersect frontier D = U intersect cgu affine
hyperplane normal offset.
cgu_relative_frontier
Isabelle code
 definition cgu_relative_frontier ::
   "’a::topological_space set \<Rightarrow> ’a set \<Rightarrow> ’a set"
 where
   "cgu_relative_frontier X A = closure A \<inter> closure (X - A)"


English mathematical translation
Mathematical role: A ∩ X \ A
   In any topological space,     cgu relative frontier X A = closure A
intersect closure (X - A). Both closures are the ambient closures appearing
in the code.
cgu_subdivision_edge_corner_set
Isabelle code
 definition cgu_subdivision_edge_corner_set ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> ’n cgu_point set"
 where
   "cgu_subdivision_edge_corner_set M =
     (\<Union>c.
       let X = frontier (cgu_cell M c);
14                             CĂTĂLIN I. CÂRSTEA

          F = {x\<in>X. cgu_locally_flat_boundary_point (cgu_cell M c) x}
      in cgu_relative_frontier X F)"

English mathematical translation
Mathematical role: singular flatness set ΣM
   For each c, let X = frontier (cgu cell M c) and let F be the points x in
X satisfying cgu locally flat boundary point (cgu cell M c) x. Then cgu
subdivision edge corner set M is the union over all c of closure F intersect
closure (X-F).
cgu_graph_subdivision_core_v7
Isabelle code
 definition cgu_graph_subdivision_core_v7 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow> bool"
 where
   "cgu_graph_subdivision_core_v7 M \<longleftrightarrow>
     cgu_lipschitz_domain (cgu_domain M) \<and>
     cgu_measured M \<noteq> {} \<and>
     openin (top_of_set (frontier (cgu_domain M))) (cgu_measured M) \<and>
     cgu_measured M \<subseteq> frontier (cgu_domain M) \<and>
     (\<forall>c. cgu_cell M c \<subseteq> cgu_domain M \<and>
       cgu_lipschitz_domain (cgu_cell M c)) \<and>
     (\<forall>c d. c \<noteq> d \<longrightarrow> cgu_cell M c \<inter> cgu_cell M
       d = {}) \<and>
     closure (cgu_domain M) = (\<Union>c. closure (cgu_cell M c)) \<and>
     cgu_graph_lipschitz_domain_v5 (cgu_domain M) \<and>
     (\<forall>c. cgu_graph_lipschitz_domain_v5 (cgu_cell M c))"

English mathematical translation
Mathematical role: regular cell decomposition
   For finite ’n, ’c, and ’h, cgu graph subdivision core v7 M holds exactly when
all of the following conjuncts hold:
       • cgu lipschitz domain (cgu domain M);
       • cgu measured M is nonempty, is open in the subspace topology on
         frontier (cgu domain M), and is a subset of that frontier;
       • for every c, cgu cell M c is a subset of cgu domain M and satisfies cgu
         lipschitz domain;
       • for every distinct c,d, the sets cgu cell M c and cgu cell M d are dis-
         joint;
       • closure (cgu domain M) equals the union, over all c, of closure (cgu
         cell M c);
       • cgu graph lipschitz domain v5 (cgu domain M); and
       • for every c, cgu graph lipschitz domain v5 (cgu cell M c).
cgu_graph_boundary_regularities_imply_lipschitz_domain
Isabelle code
 theorem cgu_graph_boundary_regularities_imply_lipschitz_domain:
   shows \<open>D \<noteq> {} \<and> open D \<and> connected D \<and> bounded D \<
      and>
     (\<forall>x\<in>frontier D. cgu_local_graph_boundary_at_v5 D x)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     15

     \<longrightarrow> cgu_lipschitz_domain D\<close>


English mathematical translation
Mathematical role: graph-condition-to-half-space-domain proposition
    D is an implicitly generalized schematic term parameter whose finite-dimensional
vector-set type is forced by the referenced constants. The single object-level propo-
sition shown by the theorem is:
    If D is nonempty, open, connected, and bounded, and every x in frontier
D satisfies cgu local graph boundary at v5 D x, then cgu lipschitz domain D
holds.
    The entire five-part conjunction is the antecedent of that object-level implication.
The displayed proposition itself contains no object-level universal quantifier over D.
cgu_share_flat_face_in
Isabelle code

 definition cgu_share_flat_face_in ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_point set \<Rightarrow> bool"
 where
   "cgu_share_flat_face_in G E F \<longleftrightarrow>
     (\<exists>normal offset U.
       normal \<noteq> 0 \<and> open U \<and>
       U \<inter> cgu_affine_hyperplane normal offset \<noteq> {} \<and>
       U \<inter> cgu_affine_hyperplane normal offset
         \<subseteq> G \<inter> frontier E \<inter> frontier F)"


English mathematical translation
Mathematical role: flat common facet visible in G
  cgu share flat face in G E F holds exactly when there exist normal, offset,
and an open set U such that normal != 0, the set U intersect cgu affine
hyperplane normal offset is nonempty, and this set is contained in G intersect
frontier E intersect frontier F.
cgu_linearly_independent3
Isabelle code

 definition cgu_linearly_independent3 ::
   "real ^ ’n::finite \<Rightarrow> real ^ ’n \<Rightarrow> real ^ ’n \<Rightarrow>
       bool"
 where
   "cgu_linearly_independent3 a b c \<longleftrightarrow>
     (\<forall>x y z::real.
       x *\<^sub>R a + y *\<^sub>R b + z *\<^sub>R c = 0
       \<longrightarrow> x = 0 \<and> y = 0 \<and> z = 0)"


English mathematical translation
Mathematical role: linear independence of three normals
   cgu linearly independent3 a b c holds exactly when, for every real x,y,z,
the equality x*a + y*b + z*c = 0 implies x=0, y=0, and z=0. The conclusion is a
three-way conjunction.
16                             CĂTĂLIN I. CÂRSTEA

cgu_n_generic_on
Isabelle code
 definition cgu_n_generic_on ::
   "nat \<Rightarrow> ’h::finite set \<Rightarrow>
     (’h \<Rightarrow> real ^ ’n::finite) \<Rightarrow> (’h \<Rightarrow> real) \<
      Rightarrow>
     (’h \<Rightarrow> ’h set) \<Rightarrow> bool"
 where
   "cgu_n_generic_on N I normal offset J \<longleftrightarrow>
     inj_on (\<lambda>i. cgu_affine_hyperplane (normal i) (offset i)) I \<and>
     (\<forall>i\<in>I.
       J i \<subseteq> I - {i} \<and> card (J i) = N + 2 \<and>
       (\<forall>j\<in>J i. \<forall>k\<in>J i. j \<noteq> k \<longrightarrow>
         cgu_linearly_independent3 (normal i) (normal j) (normal k) \<and>
         aff_dim
           (cgu_affine_hyperplane (normal i) (offset i) \<inter>
            cgu_affine_hyperplane (normal j) (offset j) \<inter>
            cgu_affine_hyperplane (normal k) (offset k))
         = int (CARD(’n)) - 3) \<and>
       (\<forall>j\<in>J i. \<forall>k\<in>J i. \<forall>l\<in>J i.
         j \<noteq> k \<and> l \<noteq> j \<and> l \<noteq> k \<longrightarrow>
         \<not> cgu_affine_hyperplane (normal i) (offset i) \<inter>
              cgu_affine_hyperplane (normal j) (offset j) \<inter>
              cgu_affine_hyperplane (normal k) (offset k)
            \<subseteq> cgu_affine_hyperplane (normal l) (offset l)))"


English mathematical translation
Mathematical role: hyperplane general-position system (I, J, N )
   For finite ’h and finite ’n, cgu n generic on N I normal offset J holds ex-
actly when:
      • the map i |-> cgu affine hyperplane (normal i) (offset i) is in-
         jective on I; and
      • for every i in I:
      • J i is a subset of I-{i} and has cardinality exactly N+2;
      • for every j,k in J i with j != k, the three vectors normal i, normal
         j, and normal k satisfy cgu linearly independent3, and the affine di-
         mension of the intersection of their three corresponding cgu affine
         hyperplane sets is int(CARD(’n))-3; and
      • for every j,k,l in J i with j != k, l != j, and l != k, the intersection
         of the i, j, and k corresponding cgu affine hyperplane sets is not a
         subset of the l corresponding cgu affine hyperplane set.
cgu_triple_region_geometry
Isabelle code
 definition cgu_triple_region_geometry ::
   "’n::finite cgu_point set \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> ’n cgu_point \<Rightarrow> real
      \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> bool"
 where
   "cgu_triple_region_geometry W ni oi nj oj nk ok \<longleftrightarrow>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     17

     W \<noteq> {} \<and>
     openin
       (top_of_set
         (cgu_affine_hyperplane ni oi \<inter>
          cgu_affine_hyperplane nj oj \<inter>
          cgu_affine_hyperplane nk ok)) W \<and>
     W \<subseteq>
       cgu_affine_hyperplane ni oi \<inter>
       cgu_affine_hyperplane nj oj \<inter>
       cgu_affine_hyperplane nk ok"


English mathematical translation
Mathematical role: relatively open triple-intersection window
  cgu triple region geometry W ni oi nj oj nk ok holds exactly when W is
nonempty, is open in the subspace topology of the intersection of the three displayed
cgu affine hyperplane sets, and is a subset of that triple intersection.
cgu_polynomial_positive_on
Isabelle code

 definition cgu_polynomial_positive_on ::
   "’n::finite cgu_matrix_polynomial \<Rightarrow> ’n cgu_point set \<Rightarrow>
      bool"
 where
   "cgu_polynomial_positive_on P W \<longleftrightarrow>
     (\<forall>x\<in>W.
       cgu_symmetric_positive_definite_matrix (cgu_matrix_poly_eval P x))"


English mathematical translation
Mathematical role: pointwise positive definiteness on a window
   cgu polynomial positive on P W holds exactly when, for every x in W, the
evaluated matrix cgu matrix poly eval P x satisfies cgu symmetric positive
definite matrix.
cgu_order_valid
Isabelle code

 definition cgu_order_valid ::
   "(’n, ’c::finite, ’h) cgu_model \<Rightarrow> bool"
 where
   "cgu_order_valid M \<longleftrightarrow>
     bij_betw (cgu_order M) {..<CARD(’c)} UNIV"


English mathematical translation
Mathematical role: bijective recovery enumeration σ
   For finite ’c, cgu order valid M holds exactly when cgu order M is a bijection
from the natural-number interval {0,...,CARD(’c)-1} onto all values of type ’c.
cgu_before_indices
Isabelle code
18                             CĂTĂLIN I. CÂRSTEA


 definition cgu_before_indices ::
   "(’n, ’c, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> ’c set"
 where
   "cgu_before_indices M r = cgu_order M ‘ {..<r}"


English mathematical translation
Mathematical role: recovered-label set Cs−
  cgu before indices M r is the image under cgu order M of the natural num-
bers strictly less than r.
cgu_after_indices
Isabelle code

 definition cgu_after_indices ::
   "(’n, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> ’c set"
 where
   "cgu_after_indices M r = cgu_order M ‘ {r..<CARD(’c)}"


English mathematical translation
Mathematical role: remaining-label set Cs+
  For finite ’c, cgu after indices M r is the image under cgu order M of the
natural numbers q satisfying r <= q < CARD(’c).
cgu_remaining_domain
Isabelle code

 definition cgu_remaining_domain ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow>
     ’n cgu_point set"
 where
   "cgu_remaining_domain M r =
     interior (\<Union>c\<in>cgu_after_indices M r. closure (cgu_cell M c))"


English mathematical translation
Mathematical role: remaining region Rs
  cgu remaining domain M r is the interior of the union, over c in cgu after
indices M r, of closure (cgu cell M c).
cgu_recovered_region
Isabelle code

 definition cgu_recovered_region ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow>
     ’n cgu_point set"
 where
   "cgu_recovered_region M r =
     cgu_domain M - closure (cgu_remaining_domain M r)"


English mathematical translation
Mathematical role: recovered region Ks
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     19

  cgu recovered region M r = cgu domain M - closure (cgu remaining
domain M r).
cgu_face_connected
Isabelle code
 definition cgu_face_connected ::
   "’n::finite cgu_point set \<Rightarrow> ’c set \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_point set) \<Rightarrow> bool"
 where
   "cgu_face_connected G I cell \<longleftrightarrow>
     (\<forall>i\<in>I. \<forall>j\<in>I.
       rtranclp
         (\<lambda>a b. a \<in> I \<and> b \<in> I \<and>
           cgu_share_flat_face_in G (cell a) (cell b)) i j)"


English mathematical translation
Mathematical role: connectivity through flat common facets
   cgu face connected G I cell holds exactly when, for every i,j in I, j is
reachable from i by the reflexive-transitive closure of the relation that sends a to b
when a in I, b in I, and cgu share flat face in G (cell a) (cell b) holds.
cgu_flat_face_patch
Isabelle code
 definition cgu_flat_face_patch ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> real \<
      Rightarrow>
     ’n cgu_point set \<Rightarrow> bool"
 where
   "cgu_flat_face_patch D normal offset gamma \<longleftrightarrow>
     norm normal = 1 \<and>
     gamma \<noteq> {} \<and>
     openin (top_of_set (cgu_affine_hyperplane normal offset)) gamma \<and>
     gamma \<subseteq> frontier D \<inter> cgu_affine_hyperplane normal offset \<
      and>
     (\<exists>U. open U \<and> gamma \<subseteq> U \<and>
       U \<inter> frontier D = U \<inter> cgu_affine_hyperplane normal offset \<and>

       (D \<inter> U \<subseteq> {x. inner normal x < offset} \<or>
        D \<inter> U \<subseteq> {x. offset < inner normal x}))"


English mathematical translation
Mathematical role: one-sided planar boundary patch
  cgu flat face patch D normal offset gamma holds exactly when:
      • ||normal||=1;
      • gamma is nonempty, is open in the subspace topology on cgu affine
        hyperplane normal offset, and is contained in frontier D intersect
        cgu affine hyperplane normal offset; and
      • there exists an open U containing gamma such that U intersect frontier
        D = U intersect cgu affine hyperplane normal offset, and either
        all of D intersect U satisfies inner normal x < offset, or all of it sat-
        isfies offset < inner normal x.
20                                CĂTĂLIN I. CÂRSTEA

     The final disjunction is inside the scope of the one existential U.
cgu_clipped_recovery_interface_v6
Isabelle code

 definition cgu_clipped_recovery_interface_v6 ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> ’n
      cgu_point set"
 where
   "cgu_clipped_recovery_interface_v6 M r =
     cgu_domain M \<inter>
       frontier (cgu_recovered_region M r) \<inter>
       frontier (cgu_remaining_domain M r)"


English mathematical translation
Mathematical role: stored interface Ω ∩ ∂Ks ∩ ∂Rs
  cgu clipped recovery interface v6 M r   is   cgu domain M intersect
frontier (cgu recovered region M r) intersect frontier (cgu
remaining domain M r).
cgu_active_pde_face_route_v4
Isabelle code

 definition cgu_active_pde_face_route_v4 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     nat \<Rightarrow> ’c \<Rightarrow> ’h \<Rightarrow> bool"
 where
   "cgu_active_pde_face_route_v4 M r c i \<longleftrightarrow>
     (let remaining = cgu_remaining_domain M r;
          recovered = cgu_recovered_region M r;
          interface = frontier recovered \<inter> frontier remaining;
          patch = cgu_face_patch M c i;
          normal = cgu_normal M c i;
          offset = cgu_offset M c i
      in if r = 0 then
           patch \<subseteq> cgu_measured M \<and>
           cgu_flat_face_patch (cgu_domain M) normal offset patch
         else
           (patch \<subseteq> cgu_measured M \<and>
            cgu_flat_face_patch (cgu_domain M) normal offset patch) \<or>
           (patch \<subseteq> cgu_domain M \<inter> interface \<and>
            cgu_flat_face_patch remaining normal offset patch))"


English mathematical translation
Mathematical role: stage source-patch eligibility
  Let remaining=cgu remaining domain M r,     recovered=cgu recovered
region M r, interface=frontier recovered intersect frontier remaining,
patch=cgu face patch M c i, normal=cgu normal M c i, and offset=cgu
offset M c i. Then:
        • if r=0, cgu active pde face route v4 M r c i holds exactly when patch
          is a subset of cgu measured M and cgu flat face patch (cgu domain M)
          normal offset patch holds;
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     21

      • if r!=0, it holds exactly when either that same two-part condition holds, or
        patch is a subset of cgu domain M intersect interface and cgu flat
        face patch remaining normal offset patch holds.
cgu_normal_height
Isabelle code
 definition cgu_normal_height ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow>
     ’n cgu_point \<Rightarrow> real"
 where
   "cgu_normal_height center normal x = inner normal (x - center)"


English mathematical translation
Mathematical role: signed normal coordinate τc
  cgu normal height center normal x is inner normal (x-center).
cgu_tangent_part
Isabelle code
 definition cgu_tangent_part ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow>
     ’n cgu_point \<Rightarrow> ’n cgu_point"
 where
   "cgu_tangent_part center normal x =
     (x - center) - cgu_normal_height center normal x *\<^sub>R normal"


English mathematical translation
Mathematical role: tangential displacement πc
   cgu tangent part center normal x is (x-center) - cgu normal height
center normal x * normal, where the multiplication of the real scalar by normal
is scalar multiplication.
cgu_flat_disc
Isabelle code
 definition cgu_flat_disc ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow> real \<Rightarrow>

     ’n cgu_point set"
 where
   "cgu_flat_disc center normal r =
     {x. cgu_normal_height center normal x = 0 \<and>
       norm (cgu_tangent_part center normal x) < r}"


English mathematical translation
Mathematical role: planar disk ∆c
   cgu flat disc center normal r is the set of all x such that cgu normal
height center normal x = 0 and ||cgu tangent part center normal x|| <
r.
cgu_exterior_half_ball
22                             CĂTĂLIN I. CÂRSTEA

Isabelle code

 definition cgu_exterior_half_ball ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow> real \<Rightarrow>

     ’n cgu_point set"
 where
   "cgu_exterior_half_ball center normal r =
     ball center r \<inter> {x. cgu_normal_height center normal x < 0}"


English mathematical translation
Mathematical role: exterior half-ball Bc−
   cgu exterior half ball center normal r is the intersection of the open ball
of radius r about center with {x | cgu normal height center normal x < 0}.

cgu_auxiliary_half_ball_geometry_step

Isabelle code

 definition cgu_auxiliary_half_ball_geometry_step ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> bool"
 where
   "cgu_auxiliary_half_ball_geometry_step M r \<longleftrightarrow>
     (let c = cgu_order M r;
           recovered = cgu_recovered_region M r;
           center = cgu_step_center M c;
           normal = cgu_step_interior_normal M c;
           rad = cgu_step_radius M c;
           patch = cgu_step_outer_patch M c;
           adjacent = cgu_step_adjacent_cell M c
      in norm normal = 1 \<and> 0 < rad \<and>
         patch \<noteq> {} \<and>
         openin (top_of_set (frontier (cgu_domain M))) patch \<and>
         patch \<subseteq> cgu_measured M \<inter> frontier recovered \<and>
         closure (cgu_flat_disc center normal rad)
            \<subseteq> patch - cgu_subdivision_edge_corner_set M \<and>
         cgu_domain M \<inter> ball center rad =
            ball center rad \<inter> {x. 0 < cgu_normal_height center normal x} \<
      and>
         adjacent \<in> cgu_before_indices M r \<and>
         cgu_flat_disc center normal rad
            \<subseteq> frontier (cgu_domain M) \<inter> frontier (cgu_cell M
      adjacent))"


English mathematical translation
Mathematical role: exterior visibility configuration
  Let c=cgu order M r, recovered=cgu recovered region M r, center=cgu
step center M c,      normal=cgu step interior normal M c, rad=cgu step
radius M c, patch=cgu step outer patch M c, and adjacent=cgu step
adjacent cell M c. Then cgu auxiliary half ball geometry step M r holds
exactly when all of the following hold:
      • ||normal||=1 and rad>0;
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     23

      • patch is nonempty, is open in the subspace topology on frontier (cgu
        domain M), and is contained in cgu measured M intersect frontier
        recovered;
      • closure (cgu flat disc center normal rad) is contained in patch -
        cgu subdivision edge corner set M;
      • cgu domain M intersect ball center rad equals ball center rad
        intersect {x | 0 < cgu normal height center normal x};
      • adjacent in cgu before indices M r; and
      • cgu flat disc center normal rad is contained in frontier (cgu
        domain M) intersect frontier (cgu cell M adjacent).
cgu_recovery_geometry_operational_v6
Isabelle code
 definition cgu_recovery_geometry_operational_v6 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow> bool"
 where
   "cgu_recovery_geometry_operational_v6 M \<longleftrightarrow>
     cgu_order_valid M \<and>
     (\<forall>r<CARD(’c).
       let c = cgu_order M r;
            remaining = cgu_remaining_domain M r;
            recovered = cgu_recovered_region M r;
            I = cgu_faces M c
       in cgu_lipschitz_domain remaining \<and>
           (r = 0 \<or>
            (recovered \<noteq> {} \<and>
             cgu_lipschitz_domain recovered \<and>
             cgu_face_connected recovered (cgu_before_indices M r) (cgu_cell M) \<
      and>
             cgu_auxiliary_half_ball_geometry_step M r)) \<and>
           (\<forall>i\<in>I.
             cgu_flat_face_patch (cgu_cell M c)
               (cgu_normal M c i) (cgu_offset M c i) (cgu_face_patch M c i) \<and>
             cgu_face_patch M c i \<subseteq>
               - cgu_subdivision_edge_corner_set M \<and>
             cgu_face_patch M c i \<subseteq> frontier remaining \<and>
             cgu_active_pde_face_route_v4 M r c i) \<and>
           cgu_degree M c + 3 \<le> card I \<and>
           cgu_n_generic_on (cgu_degree M c) I
             (cgu_normal M c) (cgu_offset M c) (cgu_witness_faces M c) \<and>
           (\<forall>i\<in>I. \<forall>j\<in>cgu_witness_faces M c i.
             \<forall>k\<in>cgu_witness_faces M c i. j \<noteq> k \<longrightarrow>
             cgu_triple_region_geometry (cgu_triple_region M c i j k)
               (cgu_normal M c i) (cgu_offset M c i)
               (cgu_normal M c j) (cgu_offset M c j)
               (cgu_normal M c k) (cgu_offset M c k))) \<and>
     (\<forall>r<CARD(’c).
       let remaining = cgu_remaining_domain M r;
            recovered = cgu_recovered_region M r
       in cgu_graph_lipschitz_domain_v5 remaining \<and>
           (r = 0 \<or> cgu_graph_lipschitz_domain_v5 recovered))"


English mathematical translation
Mathematical role: full recovery geometry
24                              CĂTĂLIN I. CÂRSTEA

   For finite ’n, ’c, and ’h, cgu recovery geometry operational v6 M is the
conjunction of cgu order valid M and the following two universally quantified
stage conditions.
   First, for every natural r < CARD(’c), set c=cgu order M r, remaining=cgu
remaining domain M r, recovered=cgu recovered region M r, and I=cgu
faces M c. Then all of these must hold:
      • cgu lipschitz domain remaining;
      • either r=0, or recovered is nonempty, satisfies cgu lipschitz
        domain, satisfies cgu face connected recovered (cgu before indices
        M r) (cgu cell M), and cgu auxiliary half ball geometry step M r
        holds;
      • every i in I has cgu flat face patch (cgu cell M c) (cgu normal
        M c i) (cgu offset M c i) (cgu face patch M c i), has cgu face
        patch M c i contained in the complement of cgu subdivision edge
        corner set M, has it contained in frontier remaining, and satisfies cgu
        active pde face route v4 M r c i;
      • cgu degree M c + 3 <= card I;
      • cgu n generic on (cgu degree M c) I (cgu normal M c) (cgu
        offset M c) (cgu witness faces M c); and
      • for every i in I, every j,k in cgu witness faces M c i with j !=
        k, the set cgu triple region M c i j k satisfies cgu triple region
        geometry for the three normal/offset pairs belonging to i,j,k.
  Second, for every r < CARD(’c), with the same definitions of remaining and
recovered, cgu graph lipschitz domain v5 remaining holds and either r=0 or
cgu graph lipschitz domain v5 recovered holds.
cgu_auxiliary_extension_elliptic
Isabelle code

 definition cgu_auxiliary_extension_elliptic ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> nat \<Rightarrow>
      bool"
 where
   "cgu_auxiliary_extension_elliptic M P r \<longleftrightarrow>
     (let c = cgu_order M r;
          adjacent = cgu_step_adjacent_cell M c
      in cgu_uniformly_positive_definite_on
            (cgu_exterior_half_ball (cgu_step_center M c)
              (cgu_step_interior_normal M c) (cgu_step_radius M c))
            (P adjacent))"


English mathematical translation
Mathematical role: exterior-half-ball ellipticity condition
  Let c=cgu order M r and adjacent=cgu step adjacent cell M c. Then cgu
auxiliary extension elliptic M P r is cgu uniformly positive definite
on (cgu exterior half ball (cgu step center M c) (cgu step interior
normal M c) (cgu step radius M c)) (P adjacent).
cgu_recovery_extension_admissible
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     25

Isabelle code

 definition cgu_recovery_extension_admissible ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> bool"
 where
   "cgu_recovery_extension_admissible M P \<longleftrightarrow>
     (\<forall>r<CARD(’c).
       let c = cgu_order M r;
           I = cgu_faces M c
       in (r = 0 \<or> cgu_auxiliary_extension_elliptic M P r) \<and>
          (\<forall>i\<in>I. \<forall>j\<in>cgu_witness_faces M c i.
            \<forall>k\<in>cgu_witness_faces M c i. j \<noteq> k \<longrightarrow>
              cgu_polynomial_positive_on (P c)
               (cgu_triple_region M c i j k)))"


English mathematical translation
Mathematical role: coefficient compatibility with recovery
  For every natural r < CARD(’c), let c=cgu order M r and I=cgu faces M c.
Then cgu recovery extension admissible M P requires both:
      • r=0 or cgu auxiliary extension elliptic M P r; and
      • for every i in I and every j,k in cgu witness faces M c i with j
        != k, cgu polynomial positive on (P c) (cgu triple region M c i
        j k).
  The two requirements are within the scope of the universal quantifier over r.
cgu_potential
Isabelle code

 type_synonym ’n cgu_potential = "’n cgu_point \<Rightarrow> real"


English mathematical translation
Mathematical role: scalar functions on Rn
   For any ’n, cgu potential is the type of real-valued functions on cgu point
vectors.
cgu_gradient
Isabelle code

 type_synonym ’n cgu_gradient = "’n cgu_point \<Rightarrow> ’n cgu_point"


English mathematical translation
Mathematical role: vector functions on Rn
  For any ’n, cgu gradient is the type of functions from cgu point vectors to
cgu point vectors.
cgu_partial_derivative
Isabelle code
26                             CĂTĂLIN I. CÂRSTEA


 definition cgu_partial_derivative ::
   "(’n::finite cgu_potential) \<Rightarrow> ’n \<Rightarrow> ’n cgu_point \<
      Rightarrow> real"
 where
   "cgu_partial_derivative phi i x =
     frechet_derivative phi (at x) (axis i 1)"


English mathematical translation
Mathematical role: coordinate derivative operator ∂i ϕ
   For finite ’n, cgu partial derivative phi i x is the Fréchet derivative se-
lected by Isabelle’s frechet derivative operator for phi at x, applied to the
coordinate-axis vector axis i 1. The definition itself does not add a differentiabil-
ity premise.
cgu_classical_gradient
Isabelle code
 definition cgu_classical_gradient ::
   "’n::finite cgu_potential \<Rightarrow> ’n cgu_gradient"
 where
   "cgu_classical_gradient phi x =
     (\<chi> i. cgu_partial_derivative phi i x)"


English mathematical translation
Mathematical role: gradient vector ∇ϕ
   For finite ’n, cgu classical gradient phi x is the vector whose coordinate i
is cgu partial derivative phi i x.
cgu_test_function_on
Isabelle code
 definition cgu_test_function_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow> bool"
 where
   "cgu_test_function_on U phi \<longleftrightarrow>
     smooth_on UNIV phi \<and>
     compact (closure {x. phi x \<noteq> 0}) \<and>
     closure {x. phi x \<noteq> 0} \<subseteq> U"


English mathematical translation
Mathematical role: test class D(U )
   cgu test function on U phi holds exactly when phi is smooth on the entire
vector space, the closure of {x | phi x != 0} is compact, and that closure is
contained in U.
cgu_weak_gradient_on
Isabelle code
 definition cgu_weak_gradient_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     27

   "cgu_weak_gradient_on U u Du \<longleftrightarrow>
     (\<forall>phi. cgu_test_function_on U phi \<longrightarrow>
       (\<forall>i.
         set_integrable lborel U
           (\<lambda>x. u x * cgu_partial_derivative phi i x) \<and>
         set_integrable lborel U (\<lambda>x. Du x $ i * phi x) \<and>
         set_lebesgue_integral lborel U
           (\<lambda>x. u x * cgu_partial_derivative phi i x) =
         - set_lebesgue_integral lborel U (\<lambda>x. Du x $ i * phi x)))"


English mathematical translation
Mathematical role: weak-gradient integration-by-parts identity
  cgu weak gradient on U u Du holds exactly when, for every phi satisfying cgu
test function on U phi, and for every coordinate i:
      • x |-> u x * cgu partial derivative phi i x is Lebesgue-integrable
        on U;
      • x |-> (Du x) i * phi x is Lebesgue-integrable on U; and
      • the integral over U of the first function is the negative of the integral over
        U of the second.
  The quantifier over i lies inside the implication whose antecedent is cgu test
function on U phi.
cgu_h1_pair_on
Isabelle code

 definition cgu_h1_pair_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_h1_pair_on U u Du \<longleftrightarrow>
     u \<in> borel_measurable (restrict_space lborel U) \<and>
     Du \<in> borel_measurable (restrict_space lborel U) \<and>
     cgu_weak_gradient_on U u Du \<and>
     set_integrable lborel U (\<lambda>x. u x ^ 2) \<and>
     set_integrable lborel U (\<lambda>x. norm (Du x) ^ 2)"


English mathematical translation
Mathematical role: weak H 1 pair H1 (U )
   cgu h1 pair on U u Du holds exactly when u and Du are Borel-measurable
with respect to Lebesgue measure restricted to U, cgu weak gradient on U u Du
holds, and the functions x |-> (u x)^2 and x |-> ||Du x||^2 are each Lebesgue-
integrable on U.
cgu_h1_squared_distance
Isabelle code

 definition cgu_h1_squared_distance ::
   "’n::finite cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> real"
 where
   "cgu_h1_squared_distance U u Du v Dv =
28                               CĂTĂLIN I. CÂRSTEA

       set_lebesgue_integral lborel U
         (\<lambda>x. (u x - v x) ^ 2 + norm (Du x - Dv x) ^ 2)"


English mathematical translation
Mathematical role: squared pair-distance d2U
  cgu h1 squared distance U u Du v Dv is the Lebesgue integral over U of (u
x-v x)^2 + ||Du x-Dv x||^2.
cgu_h1_zero_pair_on
Isabelle code

 definition cgu_h1_zero_pair_on ::
   "(real ^ ’n::finite) set \<Rightarrow>
     ((real ^ ’n) \<Rightarrow> real) \<Rightarrow>
     ((real ^ ’n) \<Rightarrow> (real ^ ’n)) \<Rightarrow> bool"
 where
   "cgu_h1_zero_pair_on U u Du \<longleftrightarrow>
     cgu_h1_pair_on U u Du \<and>
     (\<exists>(seq :: nat \<Rightarrow> ’n cgu_potential).
       (\<forall>m. cgu_test_function_on U (seq m) \<and>
         cgu_h1_pair_on U (seq m) (cgu_classical_gradient (seq m))) \<and>
       (\<forall>epsilon>0. \<exists>N. \<forall>m\<ge>N.
         cgu_h1_squared_distance U (seq m)
           (cgu_classical_gradient (seq m)) u Du < epsilon))"


English mathematical translation
Mathematical role: closure-defined H01 (U )
  cgu h1 zero pair on U u Du holds exactly when cgu h1 pair on U u Du holds
and there exists a sequence seq of real-valued functions such that:
        • for every natural m, both cgu test function on U (seq m) and cgu h1
          pair on U (seq m) (cgu classical gradient (seq m)) hold; and
        • for every real epsilon>0, there exists N such that for every
          m>=N, cgu h1 squared distance U (seq m) (cgu classical gradient
          (seq m)) u Du < epsilon.
     The same sequence must satisfy both conditions.
cgu_cellwise_coefficient
Isabelle code

 definition cgu_cellwise_coefficient ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point \<Rightarrow> real ^ ’n ^ ’n"
 where
   "cgu_cellwise_coefficient M P x =
     (if \<exists>c. x \<in> cgu_cell M c
      then cgu_matrix_poly_eval (P (SOME c. x \<in> cgu_cell M c)) x
      else 0)"


English mathematical translation
Mathematical role: assembled coefficient field AM,P
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     29

    cgu cellwise coefficient M P x is defined by cases. If there exists a c with x
in cgu cell M c, it is cgu matrix poly eval (P c*) x, where c* is an Isabelle
Hilbert-choice witness selected by SOME c. x in cgu cell M c. If there is no such
c, it is the zero matrix. The definition itself neither asserts uniqueness of the witness
nor fixes which witness is chosen when several exist.
cgu_boundary_test_on
Isabelle code

 definition cgu_boundary_test_on ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> bool"
 where
   "cgu_boundary_test_on M U gamma f \<longleftrightarrow>
     smooth_on UNIV f \<and>
     compact (closure {x. f x \<noteq> 0}) \<and>
     closure {x. x \<in> frontier U \<and> f x \<noteq> 0}
       \<subseteq> gamma - cgu_subdivision_edge_corner_set M \<and>
     cgu_h1_pair_on U f (cgu_classical_gradient f)"


English mathematical translation
Mathematical role: boundary-supported smooth datum
  cgu boundary test on M U gamma f holds exactly when:
      • f is smooth on the entire vector space;
      • closure {x | f x != 0} is compact;
      • closure {x | x in frontier U and f x != 0} is contained in gamma -
        cgu subdivision edge corner set M; and
      • cgu h1 pair on U f (cgu classical gradient f) holds.

cgu_local_trace_pair_on
Isabelle code

 definition cgu_local_trace_pair_on ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_local_trace_pair_on M U gamma f Df \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     (\<exists>(seq :: nat \<Rightarrow> ’n cgu_potential).
       (\<forall>m. cgu_boundary_test_on M U gamma (seq m)) \<and>
       (\<forall>epsilon>0. \<exists>N. \<forall>m\<ge>N.
         \<exists>z Dz. cgu_h1_zero_pair_on U z Dz \<and>
           cgu_h1_squared_distance U (seq m)
             (cgu_classical_gradient (seq m))
             (\<lambda>x. f x + z x) (\<lambda>x. Df x + Dz x) < epsilon))"


English mathematical translation
Mathematical role: boundary-data closure predicate TM (U, γ)
  cgu local trace pair on M U gamma f Df holds exactly when cgu h1 pair
on U f Df holds and there exists a sequence seq such that:
30                             CĂTĂLIN I. CÂRSTEA

      • every seq m satisfies cgu boundary test on M U gamma; and
      • for every epsilon>0, there is N such that for every m>=N there exist z,Dz
         satisfying cgu h1 zero pair on U z Dz and cgu h1 squared distance
         U (seq m) (cgu classical gradient (seq m)) (x |-> f x+z x) (x
         |-> Df x+Dz x) < epsilon.
  The witnesses z,Dz may depend on epsilon and m because their existential
quantifier is inside both eventual quantifiers.
cgu_weak_solution_on
Isabelle code
 definition cgu_weak_solution_on ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_weak_solution_on M P U u Du \<longleftrightarrow>
     cgu_h1_pair_on U u Du \<and>
     (\<forall>phi. cgu_test_function_on U phi \<longrightarrow>
       set_integrable lborel U
         (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
           (cgu_classical_gradient phi x)) \<and>
       set_lebesgue_integral lborel U
         (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
           (cgu_classical_gradient phi x)) = 0)"


English mathematical translation
Mathematical role: AM,P -harmonic weak pair
   cgu weak solution on M P U u Du holds exactly when cgu h1 pair on U
u Du holds and, for every phi satisfying cgu test function on U phi,
the function x |-> inner (cgu cellwise coefficient M P x * Du x) (cgu
classical gradient phi x) is Lebesgue-integrable on U and has integral zero
there.
cgu_dirichlet_solution_for
Isabelle code
 definition cgu_dirichlet_solution_for ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_dirichlet_solution_for M P U f Df u Du \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     cgu_weak_solution_on M P U u Du \<and>
     cgu_h1_zero_pair_on U (\<lambda>x. u x - f x)
       (\<lambda>x. Du x - Df x)"


English mathematical translation
Mathematical role: variational Dirichlet solution
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     31

  cgu dirichlet solution for M P U f Df u Du holds exactly when cgu h1
pair on U f Df, cgu weak solution on M P U u Du, and cgu h1 zero pair on
U (u-f) (Du-Df) all hold, where both subtractions are pointwise.
cgu_dn_energy
Isabelle code
 definition cgu_dn_energy ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> real"
 where
   "cgu_dn_energy M P U Du Dh =
     set_lebesgue_integral lborel U
       (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
         (Dh x))"


English mathematical translation
Mathematical role: boundary-energy pairing value
  cgu dn energy M P U Du Dh is the Lebesgue integral over U of inner (cgu
cellwise coefficient M P x * Du x) (Dh x).
cgu_dn_energy_integrable
Isabelle code
 definition cgu_dn_energy_integrable ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_dn_energy_integrable M P U Du Dh \<longleftrightarrow>
     set_integrable lborel U
       (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
         (Dh x))"


English mathematical translation
Mathematical role: boundary-energy integrability predicate
   cgu dn energy integrable M P U Du Dh holds exactly when the integrand
used in cgu dn energy M P U Du Dh is Lebesgue-integrable on U.
cgu_local_dn_equal
Isabelle code
 definition cgu_local_dn_equal ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow> bool"
 where
   "cgu_local_dn_equal M P1 P2 U gamma \<longleftrightarrow>
     (\<forall>f Df. cgu_local_trace_pair_on M U gamma f Df \<longrightarrow>
       (\<exists>u Du. cgu_dirichlet_solution_for M P1 U f Df u Du) \<and>
32                             CĂTĂLIN I. CÂRSTEA

       (\<exists>u Du. cgu_dirichlet_solution_for M P2 U f Df u Du)) \<and>
     (\<forall>f Df h Dh u1 Du1 u2 Du2.
       cgu_local_trace_pair_on M U gamma f Df \<and>
       cgu_local_trace_pair_on M U gamma h Dh \<and>
       cgu_dirichlet_solution_for M P1 U f Df u1 Du1 \<and>
       cgu_dirichlet_solution_for M P2 U f Df u2 Du2
       \<longrightarrow>
       cgu_dn_energy_integrable M P1 U Du1 Dh \<and>
       cgu_dn_energy_integrable M P2 U Du2 Dh \<and>
       cgu_dn_energy M P1 U Du1 Dh = cgu_dn_energy M P2 U Du2 Dh)"

English mathematical translation
Mathematical role: equality of local boundary-energy data
   cgu local dn equal M P1 P2 U gamma is the conjunction of two clauses.
   First, for every f,Df, if cgu local trace pair on M U gamma f Df, then there
exist u,Du satisfying cgu dirichlet solution for M P1 U f Df u Du, and there
also exist (not necessarily the same) u,Du satisfying the analogous predicate for P2.
   Second, for every f,Df,h,Dh,u1,Du1,u2,Du2, if f,Df and h,Dh each sat-
isfy cgu local trace pair on M U gamma, and u1,Du1 satisfies cgu dirichlet
solution for for P1,f,Df while u2,Du2 satisfies it for P2,f,Df, then both integra-
bility predicates cgu dn energy integrable M P1 U Du1 Dh and cgu dn energy
integrable M P2 U Du2 Dh hold and the two corresponding values of cgu dn
energy are equal.
lu_metric
Isabelle code
 type_synonym ’n lu_metric = "’n cgu_point \<Rightarrow> real ^ ’n ^ ’n"

English mathematical translation
Mathematical role: matrix-field function type
   For any ’n, lu metric is the type of functions from cgu point vectors to real
’n-by-’n matrices.
lu_density
Isabelle code
 type_synonym ’n lu_density = "’n cgu_point \<Rightarrow> real"

English mathematical translation
Mathematical role: scalar-field function type
  For any ’n, lu density is the type of real-valued functions on cgu point vectors.
lu_smooth_metric_density_data_on
Isabelle code
 definition lu_smooth_metric_density_data_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_density \<Rightarrow> bool"
 where
   "lu_smooth_metric_density_data_on V g a rho \<longleftrightarrow>
     open V \<and>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     33

    (\<forall>i j. smooth_on V (\<lambda>x. g x $ i $ j)) \<and>
    (\<forall>i j. smooth_on V (\<lambda>x. a x $ i $ j)) \<and>
    smooth_on V rho \<and>
    (\<forall>x\<in>V.
      cgu_symmetric_positive_definite_matrix (g x) \<and>
      cgu_symmetric_positive_definite_matrix (a x) \<and>
      0 < rho x \<and>
      rho x ^ 2 = det (g x) \<and>
      (\<forall>v. a x *v (g x *v v) = rho x *\<^sub>R v))"


English mathematical translation
Mathematical role: metric/conductivity representation on V
  lu smooth metric density data on V g a rho holds exactly when:
      • V is open;
      • for every i,j, the scalar functions x |-> g(x) {ij} and x |-> a(x) {ij}
        are smooth on V;
      • rho is smooth on V; and
      • for every x in V, both g x and a x satisfy cgu symmetric positive
        definite matrix, rho x>0, (rho x)^2 = det(g x), and for every vector
        v, a x * (g x * v) = rho x * v.
lu_smooth_metric_extension_near
Isabelle code
 definition lu_smooth_metric_extension_near ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_density \<Rightarrow> bool"
 where
   "lu_smooth_metric_extension_near M P U gamma g a rho \<longleftrightarrow>
     (\<exists>V. gamma \<subseteq> V \<and>
       lu_smooth_metric_density_data_on V g a rho \<and>
       (\<forall>x\<in>U \<inter> V. a x = cgu_cellwise_coefficient M P x))"


English mathematical translation
Mathematical role: local representation of AM,P
   lu smooth metric extension near M P U gamma g a rho holds exactly when
there exists a set V containing gamma such that lu smooth metric density data
on V g a rho holds and, for every x in U intersect V, a x = cgu cellwise
coefficient M P x. Openness of V follows only through lu smooth metric
density data on; no separate relation between g and cgu cellwise coefficient
is asserted beyond the equations inside lu smooth metric density data on.
lu_induced_boundary_metrics_equal_on
Isabelle code
 definition lu_induced_boundary_metrics_equal_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow> bool"
 where
34                               CĂTĂLIN I. CÂRSTEA

     "lu_induced_boundary_metrics_equal_on gamma normal g1 g2 \<longleftrightarrow>
       (\<forall>x\<in>gamma. \<forall>xi eta.
         inner normal xi = 0 \<and> inner normal eta = 0
         \<longrightarrow>
         inner xi (g1 x *v eta) = inner xi (g2 x *v eta))"


English mathematical translation
Mathematical role: tangential bilinear-pairing agreement
  lu induced boundary metrics equal on gamma normal g1 g2 holds exactly
when, for every x in gamma and all vectors xi,eta, if both are orthogonal to
normal, then inner xi (g1 x * eta) = inner xi (g2 x * eta).
mclean_coefficient
Isabelle code
 type_synonym ’n mclean_coefficient =
   "’n cgu_point \<Rightarrow> real ^ ’n ^ ’n"


English mathematical translation
Mathematical role: general matrix coefficient field type
   For any ’n, mclean coefficient is the same function shape as lu metric: func-
tions from cgu point vectors to real ’n-by-’n matrices.
mclean_source
Isabelle code
 type_synonym ’n mclean_source =
   "’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> real"


English mathematical translation
Mathematical role: two-argument functional type F (u, G)
   For any ’n, mclean source is the type of two-argument real-valued functionals
taking first an cgu potential function and then an cgu gradient function.
mclean_h1_norm
Isabelle code
 definition mclean_h1_norm ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> real"
 where
   "mclean_h1_norm U u Du =
     sqrt (cgu_h1_squared_distance U u Du (\<lambda>_. 0) (\<lambda>_. 0))"


English mathematical translation
Mathematical role: pair norm ∥(u, G)∥U
  mclean h1 norm U u Du is the square root of cgu h1 squared distance U u
Du 0 0, where both zero arguments are the pointwise zero functions.
mclean_same_trace_on
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     35


 definition mclean_same_trace_on ::
   "’n::finite cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_same_trace_on U f Df g Dg \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     cgu_h1_pair_on U g Dg \<and>
     cgu_h1_zero_pair_on U (\<lambda>x. f x - g x) (\<lambda>x. Df x - Dg x)"


English mathematical translation
Mathematical role: one-sided zero-boundary-difference relation RU
    mclean same trace on U f Df g Dg holds exactly when both (f,Df) and
(g,Dg) satisfy cgu h1 pair on U, and their pointwise difference (f-g,Df-Dg) sat-
isfies cgu h1 zero pair on U.
mclean_trace_norm
Isabelle code
 definition mclean_trace_norm ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> real"
 where
   "mclean_trace_norm U f Df =
     Inf {r. \<exists>g Dg. mclean_same_trace_on U f Df g Dg \<and>
       r = mclean_h1_norm U g Dg}"


English mathematical translation
Mathematical role: raw trace-size infimum qU
   mclean trace norm U f Df is the real infimum of the set of all r for which there
exist g,Dg with mclean same trace on U f Df g Dg and r=mclean h1 norm U g
Dg. The definition does not separately assert that this set is nonempty or bounded
below.
mclean_energy
Isabelle code
 definition mclean_energy ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> ’n cgu_gradient \<Rightarrow> real"
 where
   "mclean_energy U a Du Dv =
     set_lebesgue_integral lborel U (\<lambda>x. inner (a x *v Du x) (Dv x))"


English mathematical translation
Mathematical role: bilinear energy BU,a
  mclean energy U a Du Dv is the Lebesgue integral over U of inner (a x * Du
x) (Dv x).
mclean_energy_integrable
Isabelle code
36                             CĂTĂLIN I. CÂRSTEA


 definition mclean_energy_integrable ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_energy_integrable U a Du Dv \<longleftrightarrow>
     set_integrable lborel U (\<lambda>x. inner (a x *v Du x) (Dv x))"


English mathematical translation
Mathematical role: energy-integrability predicate
  mclean energy integrable U a Du Dv holds exactly when the integrand used
by mclean energy U a Du Dv is Lebesgue-integrable on U.
mclean_variational_form_on
Isabelle code
 definition mclean_variational_form_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "mclean_variational_form_on U a \<longleftrightarrow>
     (\<exists>coercive continuous. 0 < coercive \<and> 0 \<le> continuous \<and>
       (\<forall>u Du v Dv.
         cgu_h1_pair_on U u Du \<and> cgu_h1_pair_on U v Dv
         \<longrightarrow>
         mclean_energy_integrable U a Du Dv \<and>
         abs (mclean_energy U a Du Dv) \<le>
           continuous * mclean_h1_norm U u Du * mclean_h1_norm U v Dv) \<and>
       (\<forall>z Dz. cgu_h1_zero_pair_on U z Dz \<longrightarrow>
         coercive * mclean_h1_norm U z Dz ^ 2 \<le>
           mclean_energy U a Dz Dz))"


English mathematical translation
Mathematical role: stable bounded/coercive form
   mclean variational form on U a holds exactly when there exist real con-
stants coercive,continuous with coercive>0 and continuous>=0 such that both
clauses below hold:
      • for every u,Du,v,Dv, if both pairs satisfy cgu h1 pair on U, then mclean
         energy integrable U a Du Dv and abs(mclean energy U a Du Dv) <=
         continuous * mclean h1 norm U u Du * mclean h1 norm U v Dv;
      • for every z,Dz satisfying cgu h1 zero pair on U, coercive * (mclean
         h1 norm U z Dz)^2 <= mclean energy U a Dz Dz.
   The same two constants work for all quantified functions.
mclean_weak_solution_on
Isabelle code
 definition mclean_weak_solution_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_weak_solution_on U a u Du \<longleftrightarrow>
     cgu_h1_pair_on U u Du \<and>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     37

    (\<forall>phi. cgu_test_function_on U phi \<longrightarrow>
      mclean_energy_integrable U a Du (cgu_classical_gradient phi) \<and>
      mclean_energy U a Du (cgu_classical_gradient phi) = 0)"


English mathematical translation
Mathematical role: weak a-harmonic pair
  mclean weak solution on U a u Du holds exactly when cgu h1 pair on U
u Du and, for every phi satisfying cgu test function on U phi, both mclean
energy integrable U a Du (cgu classical gradient phi)        and    mclean
energy U a Du (cgu classical gradient phi)=0 hold.
mclean_dirichlet_solution_for
Isabelle code

 definition mclean_dirichlet_solution_for ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_dirichlet_solution_for U a f Df u Du \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     mclean_weak_solution_on U a u Du \<and>
     mclean_same_trace_on U f Df u Du"


English mathematical translation
Mathematical role: abstract Dirichlet solution
  mclean dirichlet solution for U a f Df u Du holds exactly when cgu h1
pair on U f Df, mclean weak solution on U a u Du, and mclean same trace
on U f Df u Du all hold.
mclean_green_solution_for
Isabelle code

 definition mclean_green_solution_for ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n mclean_source \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_green_solution_for U a F u Du \<longleftrightarrow>
     cgu_h1_zero_pair_on U u Du \<and>
     (\<forall>v Dv. cgu_h1_zero_pair_on U v Dv \<longrightarrow>
       mclean_energy_integrable U a Du Dv \<and>
       mclean_energy U a Du Dv = F v Dv)"


English mathematical translation
Mathematical role: source solution
  mclean green solution for U a F u Du holds exactly when cgu h1 zero
pair on U u Du and, for every v,Dv satisfying cgu h1 zero pair on U, both
mclean energy integrable U a Du Dv and mclean energy U a Du Dv = F v
Dv hold.
mclean_source_bound_on
38                               CĂTĂLIN I. CÂRSTEA

Isabelle code

 definition mclean_source_bound_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_source \<Rightarrow> real \<
      Rightarrow> bool"
 where
   "mclean_source_bound_on U F K \<longleftrightarrow>
     0 \<le> K \<and> F (\<lambda>_. 0) (\<lambda>_. 0) = 0 \<and>
     (\<forall>u Du v Dv.
       cgu_h1_zero_pair_on U u Du \<and> cgu_h1_zero_pair_on U v Dv
       \<longrightarrow>
       F (\<lambda>x. u x + v x) (\<lambda>x. Du x + Dv x) = F u Du + F v Dv) \<and>

       (\<forall>r u Du. cgu_h1_zero_pair_on U u Du \<longrightarrow>
         F (\<lambda>x. r * u x) (\<lambda>x. r *\<^sub>R Du x) = r * F u Du) \<and>
       (\<forall>u Du. cgu_h1_zero_pair_on U u Du \<longrightarrow>
         abs (F u Du) \<le> K * mclean_h1_norm U u Du)"


English mathematical translation
Mathematical role: bounded linear functional with bound K
     mclean source bound on U F K holds exactly when:
        • K>=0 and F 0 0 = 0;
        • for all (u,Du) and (v,Dv) satisfying cgu h1 zero pair on U,
          F(u+v,Du+Dv)=F(u,Du)+F(v,Dv);
        • for every real r and every (u,Du) satisfying cgu h1 zero pair on U,
          F(r*u,r*Du)=r*F(u,Du); and
        • for every (u,Du) satisfying cgu h1 zero pair on U, abs(F u Du) <= K *
          mclean h1 norm U u Du.
  The equations constrain F only on arguments covered by the stated cgu h1 zero
pair on premises, apart from the explicit value at the zero pair.
mclean_flat_chart
Isabelle code

 definition mclean_flat_chart ::
   "(’m::finite cgu_point \<Rightarrow> ’n::finite cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> bool"
 where
   "mclean_flat_chart chart normal \<longleftrightarrow>
     norm normal = 1 \<and>
     (\<forall>x y. norm (chart x - chart y) = norm (x - y)) \<and>
     (\<forall>x y. inner normal (chart x - chart y) = 0)"


English mathematical translation
Mathematical role: isometric hyperplane chart condition
   mclean flat chart chart normal holds exactly when ||normal||=1, chart
preserves every pairwise distance, and every displacement chart x-chart y is or-
thogonal to normal.
mclean_flat_offset_action
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     39


 definition mclean_flat_offset_action ::
   "(’m::finite cgu_point \<Rightarrow> ’n::finite cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> ’m cgu_potential \<Rightarrow>
     ’n cgu_potential \<Rightarrow> real"
 where
   "mclean_flat_offset_action chart normal t g phi =
     integral\<^sup>L lborel
       (\<lambda>x. g x * phi (chart x + t *\<^sub>R normal))"


English mathematical translation
Mathematical role: moving-layer integral
   mclean flat offset action chart normal t g phi is the Lebesgue integral
over the entire ’m-coordinate space of g x * phi(chart x + t*normal).
mclean_source_extends_flat_offset_action
Isabelle code
 definition mclean_source_extends_flat_offset_action ::
   "’n::finite cgu_point set \<Rightarrow>
     (’m::finite cgu_point \<Rightarrow> ’n cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> ’m cgu_potential \<Rightarrow>
     ’n mclean_source \<Rightarrow> bool"
 where
   "mclean_source_extends_flat_offset_action Omega chart normal t g F \<
      longleftrightarrow>
     (\<forall>phi. cgu_test_function_on Omega phi \<longrightarrow>
       F phi (cgu_classical_gradient phi) =
         mclean_flat_offset_action chart normal t g phi)"


English mathematical translation
Mathematical role: functional agreement with a layer source
   mclean source extends flat offset action Omega chart normal t g F
holds exactly when, for every phi satisfying cgu test function on Omega phi,
F phi (cgu classical gradient phi) = mclean flat offset action chart
normal t g phi.
mclean_flat_offset_cylinder_inside
Isabelle code
 definition mclean_flat_offset_cylinder_inside ::
   "’n::finite cgu_point set \<Rightarrow>
     (’m::finite cgu_point \<Rightarrow> ’n cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> ’m cgu_potential \<Rightarrow> real \<Rightarrow>
      bool"
 where
   "mclean_flat_offset_cylinder_inside Omega chart normal g delta \<
      longleftrightarrow>
     {chart x + t *\<^sub>R normal |x t.
       x \<in> closure {y. g y \<noteq> 0} \<and> 0 \<le> t \<and> t \<le> delta}
       \<subseteq> Omega"


English mathematical translation
Mathematical role: tubular support containment
40                             CĂTĂLIN I. CÂRSTEA

   mclean flat offset cylinder inside Omega chart normal g delta holds
exactly when every point chart x + t*normal with x in closure {y | g y !=
0} and 0<=t<=delta belongs to Omega.
mclean_source_real_subspace
Isabelle code

 definition mclean_source_real_subspace ::
   "’n::finite mclean_source set \<Rightarrow> bool"
 where
   "mclean_source_real_subspace E \<longleftrightarrow>
     0 \<in> E \<and>
     (\<forall>F\<in>E. \<forall>G\<in>E. F + G \<in> E) \<and>
     (\<forall>r F. F \<in> E \<longrightarrow> r *\<^sub>R F \<in> E)"


English mathematical translation
Mathematical role: vector-space closure of E
   mclean source real subspace E holds exactly when the zero functional belongs
to E, E is closed under addition of any two of its members, and E is closed under
multiplication of any member by any real scalar.
mclean_source_linear_on
Isabelle code

 definition mclean_source_linear_on ::
   "’n::finite mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_source_linear_on E g \<longleftrightarrow>
     g 0 = 0 \<and>
     (\<forall>F\<in>E. \<forall>G\<in>E. g (F + G) = g F + g G) \<and>
     (\<forall>r F. F \<in> E \<longrightarrow> g (r *\<^sub>R F) = r * g F)"


English mathematical translation
Mathematical role: linearity of g : E → R
   mclean source linear on E g holds exactly when g 0=0, g(F+G)=g F+g G for
all F,G in E, and g(r*F)=r*g F for every real r and every F in E.
mclean_source_seminorm_on
Isabelle code

 definition mclean_source_seminorm_on ::
   "’n::finite mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_source_seminorm_on E p \<longleftrightarrow>
     p 0 = 0 \<and>
     (\<forall>F\<in>E. 0 \<le> p F) \<and>
     (\<forall>F\<in>E. \<forall>G\<in>E. p (F + G) \<le> p F + p G) \<and>
     (\<forall>r F. F \<in> E \<longrightarrow> p (r *\<^sub>R F) = \<bar>r\<bar> *
       p F)"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     41

English mathematical translation
Mathematical role: seminorm axioms for p
   mclean source seminorm on E p holds exactly when p 0=0; p F>=0 for every F
in E; p(F+G)<=p F+p G for all F,G in E; and p(r*F)=abs(r)*p F for every real
r and every F in E.
mclean_h1_zero_source_bidual_functional_on_v2
Isabelle code

 definition mclean_h1_zero_source_bidual_functional_on_v2 ::
   "’n::finite mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_h1_zero_source_bidual_functional_on_v2 E p g \<longleftrightarrow>
     mclean_source_linear_on E g \<and>
     (\<exists>C\<ge>0. \<forall>F\<in>E. \<bar>g F\<bar> \<le> C * p F)"


English mathematical translation
Mathematical role: p-bounded linear functional on E
  mclean h1 zero source bidual functional on v2 E p g holds exactly when
mclean source linear on E g and there exists one real C>=0 such that abs(g F)
<= C*p F for every F in E.
mclean_h1_zero_bidual_realization_on_v2
Isabelle code

 definition mclean_h1_zero_bidual_realization_on_v2 ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_h1_zero_bidual_realization_on_v2 U E p \<longleftrightarrow>
     mclean_source_real_subspace E \<and>
     mclean_source_seminorm_on E p \<and>
     (\<forall>F. F \<in> E \<longleftrightarrow>
       (\<exists>K. mclean_source_bound_on U F K)) \<and>
     (\<forall>F\<in>E.
       mclean_source_bound_on U F (p F) \<and>
       (\<forall>K. mclean_source_bound_on U F K \<longrightarrow> p F \<le> K)) \<
      and>
     (\<forall>g.
       mclean_h1_zero_source_bidual_functional_on_v2 E p g
       \<longrightarrow>
       (\<exists>u Du.
         cgu_h1_zero_pair_on U u Du \<and>
         (\<forall>F\<in>E. g F = F u Du)))"


English mathematical translation
Mathematical role: total-functional representation package (E, p)
   mclean h1 zero bidual realization on v2 U E p holds exactly when all of
the following hold:
      • mclean source real subspace E and mclean source seminorm on E p;
42                             CĂTĂLIN I. CÂRSTEA

       • for every functional F, F in E if and only if there exists a real K with
          mclean source bound on U F K;
       • for every F in E, mclean source bound on U F (p F), and p F <= K for
          every K satisfying mclean source bound on U F K; and
       • for every g, if mclean h1 zero source bidual functional on v2 E p g,
          then there exist u,Du satisfying cgu h1 zero pair on U u Du such that g
          F = F u Du for every F in E.
     The final representing pair is existential; uniqueness is not asserted.
mclean_zero_extension_on
Isabelle code
 definition mclean_zero_extension_on ::
   "’n::finite cgu_point set \<Rightarrow> (’n cgu_point \<Rightarrow> ’a::zero) \<
      Rightarrow>
     ’n cgu_point \<Rightarrow> ’a"
 where
   "mclean_zero_extension_on U f x = (if x \<in> U then f x else 0)"


English mathematical translation
Mathematical role: pointwise zero extension
  For a codomain with a zero, mclean zero extension on U f x equals f x when
x in U and equals zero otherwise.
ucp_point
Isabelle code
 type_synonym ’n ucp_point = "real ^ ’n"


English mathematical translation
Mathematical role: second Euclidean-vector alias
  For any ’n, ucp point is the type of real-valued vectors indexed by ’n.
ucp_coefficient
Isabelle code
 type_synonym ’n ucp_coefficient =
   "’n ucp_point \<Rightarrow> (real ^ ’n ^ ’n)"


English mathematical translation
Mathematical role: local matrix-field function type
   For any ’n, ucp coefficient is the type of functions from ucp point vectors
to real ’n-by-’n matrices.
ucp_symmetric_matrix
Isabelle code
 definition ucp_symmetric_matrix ::
   "(real ^ ’n::finite ^ ’n) \<Rightarrow> bool"
 where
   "ucp_symmetric_matrix A \<longleftrightarrow> transpose A = A"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     43

English mathematical translation
Mathematical role: matrix symmetry
  ucp symmetric matrix A holds exactly when transpose A = A.
ucp_matrix_polynomial
Isabelle code
 definition ucp_matrix_polynomial ::
   "’n::finite ucp_coefficient \<Rightarrow> bool"
 where
   "ucp_matrix_polynomial P \<longleftrightarrow>
     (\<forall>i j. polynomial_function (\<lambda>x. P x $ i $ j))"


English mathematical translation
Mathematical role: entrywise polynomial field
  ucp matrix polynomial P holds exactly when, for every i,j, the scalar compo-
nent function x |-> P(x) {ij} is a polynomial function.
ucp_uniformly_elliptic_near
Isabelle code
 definition ucp_uniformly_elliptic_near ::
   "’n::finite ucp_point set \<Rightarrow> ’n ucp_coefficient \<Rightarrow> bool"
 where
   "ucp_uniformly_elliptic_near E P \<longleftrightarrow>
     (\<exists>V k. open V \<and> closure E \<subseteq> V \<and> 0 < k \<and>
       (\<forall>x\<in>V. \<forall>xi. k * norm xi ^ 2 \<le> inner xi (P x *v xi)))"



English mathematical translation
Mathematical role: ellipticity on a neighborhood of X
  ucp uniformly elliptic near E P holds exactly when there exist an open set
V and a real k>0 such that closure E is contained in V and, for every x in V
and every vector xi, k*||xi||^2 <= inner xi (P x * xi). The same V,k work
uniformly for all x,xi.
ucp_partial_derivative
Isabelle code
 definition ucp_partial_derivative ::
   "(’n::finite ucp_point \<Rightarrow> real) \<Rightarrow> ’n \<Rightarrow>
    ’n ucp_point \<Rightarrow> real"
 where
   "ucp_partial_derivative phi i x =
     frechet_derivative phi (at x) (axis i 1)"


English mathematical translation
Mathematical role: local coordinate derivative operator
   ucp partial derivative phi i x is the Fréchet derivative selected by Is-
abelle’s frechet derivative operator for phi at x, applied to axis i 1. The
definition itself supplies no differentiability premise.
44                             CĂTĂLIN I. CÂRSTEA

ucp_test_function_on
Isabelle code

 definition ucp_test_function_on ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow> bool"
 where
   "ucp_test_function_on G phi \<longleftrightarrow>
     smooth_on UNIV phi \<and>
     compact (closure {x. phi x \<noteq> 0}) \<and>
     closure {x. phi x \<noteq> 0} \<subseteq> G"


English mathematical translation
Mathematical role: local test class D(X)
   ucp test function on G phi holds exactly when phi is smooth on the entire
vector space, closure {x | phi x != 0} is compact, and that closure is contained
in G.
ucp_locally_square_integrable_on
Isabelle code

 definition ucp_locally_square_integrable_on ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> ’a::euclidean_space) \<Rightarrow> bool"
 where
   "ucp_locally_square_integrable_on G f \<longleftrightarrow>
     (\<forall>K. compact K \<and> K \<subseteq> G \<longrightarrow>
       set_integrable lborel K (\<lambda>x. norm (f x) ^ 2))"


English mathematical translation
Mathematical role: local square integrability
   ucp locally square integrable on G f holds exactly when, for every compact
set K contained in G, the function x |-> ||f x||^2 is Lebesgue-integrable on K.
ucp_weak_gradient_on
Isabelle code

 definition ucp_weak_gradient_on ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow>
    (’n ucp_point \<Rightarrow> ’n ucp_point) \<Rightarrow> bool"
 where
   "ucp_weak_gradient_on G u Du \<longleftrightarrow>
     (\<forall>phi. ucp_test_function_on G phi \<longrightarrow>
       (\<forall>i.
         set_integrable lborel G
           (\<lambda>x. u x * ucp_partial_derivative phi i x) \<and>
         set_integrable lborel G (\<lambda>x. Du x $ i * phi x) \<and>
         set_lebesgue_integral lborel G
           (\<lambda>x. u x * ucp_partial_derivative phi i x) =
         - set_lebesgue_integral lborel G (\<lambda>x. Du x $ i * phi x)))"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     45

English mathematical translation
Mathematical role: local weak-gradient identity
   ucp weak gradient on G u Du holds exactly when, for every phi satisfy-
ing ucp test function on G phi and every coordinate i, both x |-> u x *
ucp partial derivative phi i x and x |-> (Du x) i * phi x are Lebesgue-
integrable on G, and the integral of the first over G equals the negative of the
integral of the second.
ucp_test_gradient
Isabelle code
 definition ucp_test_gradient ::
   "(’n::finite ucp_point \<Rightarrow> real) \<Rightarrow>
    ’n ucp_point \<Rightarrow> ’n ucp_point"
 where
   "ucp_test_gradient phi x =
     (\<chi> i. ucp_partial_derivative phi i x)"


English mathematical translation
Mathematical role: local gradient vector
  ucp test gradient phi x is the vector whose coordinate i is ucp partial
derivative phi i x.
ucp_weak_solution_on
Isabelle code
 definition ucp_weak_solution_on ::
   "’n::finite ucp_point set \<Rightarrow> ’n ucp_coefficient \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow> bool"
 where
   "ucp_weak_solution_on G a0 u \<longleftrightarrow>
     (\<exists>Du.
       ucp_locally_square_integrable_on G u \<and>
       ucp_locally_square_integrable_on G Du \<and>
       ucp_weak_gradient_on G u Du \<and>
       (\<forall>phi. ucp_test_function_on G phi \<longrightarrow>
         set_integrable lborel G
           (\<lambda>x. inner (a0 x *v Du x) (ucp_test_gradient phi x)) \<and>
         set_lebesgue_integral lborel G
           (\<lambda>x. inner (a0 x *v Du x) (ucp_test_gradient phi x)) = 0))"


English mathematical translation
Mathematical role: locally weak solution of div(P ∇u) = 0
   ucp weak solution on G a0 u holds exactly when there exists a vector-valued
function Du such that ucp locally square integrable on G u, ucp locally
square integrable on G Du, and ucp weak gradient on G u Du hold, and for ev-
ery phi satisfying ucp test function on G phi, the function x |-> inner (a0 x
* Du x) (ucp test gradient phi x) is Lebesgue-integrable on G and has integral
zero there.
hormander_regular_distribution_test_zero_on
Isabelle code
46                             CĂTĂLIN I. CÂRSTEA


 definition hormander_regular_distribution_test_zero_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow> bool"
 where
   "hormander_regular_distribution_test_zero_on X u \<longleftrightarrow>
     set_integrable lborel X u \<and>
     (\<forall>phi. cgu_test_function_on X phi \<longrightarrow>
       set_integrable lborel X (\<lambda>x. u x * phi x) \<and>
       set_lebesgue_integral lborel X (\<lambda>x. u x * phi x) = 0)"


English mathematical translation
Mathematical role: integrable distributional-zero predicate
   hormander regular distribution test zero on X u holds exactly when u is
Lebesgue-integrable on X and, for every phi satisfying cgu test function on X
phi, the product x |-> u x*phi x is Lebesgue-integrable on X and has integral
zero there.
evans_bounded_domain
Isabelle code

 definition evans_bounded_domain ::
   "’n::finite cgu_point set \<Rightarrow> bool"
 where
   "evans_bounded_domain U \<longleftrightarrow> bounded U"


English mathematical translation
Mathematical role: boundedness of U
     evans bounded domain U holds exactly when U is bounded.
evans_elliptic_coefficient_on
Isabelle code

 definition evans_elliptic_coefficient_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "evans_elliptic_coefficient_on U a \<longleftrightarrow>
     a \<in> borel_measurable (restrict_space lborel U) \<and>
     (\<exists>B\<ge>0. \<forall>x\<in>U. norm (a x) \<le> B) \<and>
     (\<forall>x\<in>U. transpose (a x) = a x) \<and>
     (\<exists>theta>0. \<forall>x\<in>U. \<forall>xi.
       theta * norm xi ^ 2 \<le> inner (a x *v xi) xi)"


English mathematical translation
Mathematical role: measurable, bounded, symmetric, uniformly elliptic coefficient
     evans elliptic coefficient on U a holds exactly when:
        • a is Borel-measurable with respect to Lebesgue measure restricted to U;
        • there exists B>=0 such that ||a x||<=B for every x in U;
        • transpose(a x)=a x for every x in U; and
        • there exists theta>0 such that, for every x in U and every vector xi,
          theta*||xi||^2 <= inner (a x * xi) xi.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     47

evans_poincare_elliptic_green
Isabelle code
 locale evans_poincare_elliptic_green =
   fixes dimension_type :: "’n::finite itself"
   assumes evans_poincare_elliptic_green:
     "\<forall>U a. evans_poincare_elliptic_green_claim
       (U :: ’n cgu_point set) a"


English mathematical translation
Mathematical role: An atomic dimension-indexed universal assumption about
evans poincare elliptic green claim.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name evans poincare elliptic green, that for every U and every a,
   evans poincare elliptic green claim U a
   holds, where U is explicitly a set of objects of type ’n cgu point. The quantifiers
range over all well-typed U and a; no further restriction on either variable is stated.
mclean_smooth_test_h1_zero
Isabelle code
 locale mclean_smooth_test_h1_zero =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_smooth_test_h1_zero:
     "mclean_smooth_test_h1_zero_claim dimension_type"

English mathematical translation
Mathematical role: An atomic dimension-indexed assumption asserting mclean
smooth test h1 zero claim.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name mclean smooth test h1 zero, the proposition
  mclean smooth test h1 zero claim dimension type.
hormander_analytic_elliptic_ucp
Isabelle code
 locale hormander_analytic_elliptic_ucp =
   fixes dimension_type :: "’n::finite itself"
   assumes hormander_analytic_elliptic_ucp:
     "\<forall>X P u.
       hormander_analytic_elliptic_ucp_claim
         (X :: ’n ucp_point set) P u"


English mathematical translation
Mathematical role: An atomic dimension-indexed universal assumption about
hormander analytic elliptic ucp claim.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name hormander analytic elliptic ucp, that for every X, every P, and every u,
48                             CĂTĂLIN I. CÂRSTEA

   hormander analytic elliptic ucp claim X P u
   holds, where X is explicitly a set of objects of type ’n ucp point. The argument
order is X, then P, then u. No further restriction on these universally quantified
variables is stated.
hormander_weak_gradient_locality
Isabelle code

 locale hormander_weak_gradient_locality =
   fixes dimension_type :: "’n::finite itself"
   assumes hormander_weak_gradient_locality:
     "\<forall>X u Du.
       hormander_weak_gradient_locality_claim
         (X :: ’n ucp_point set) u Du"


English mathematical translation
Mathematical role: An atomic dimension-indexed universal locality assumption
about hormander weak gradient locality claim.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name hormander weak gradient locality, that for every X, every u, and every
Du,
   hormander weak gradient locality claim X u Du
   holds, where X is explicitly a set of objects of type ’n ucp point. The argument
order is X, then u, then Du. No further restriction on these universally quantified
variables is stated.
mclean_h1_zero_extension_localization
Isabelle code

 locale mclean_h1_zero_extension_localization =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_h1_zero_extension_localization:
     "mclean_h1_zero_extension_localization_claim dimension_type"


English mathematical translation
Mathematical role: An atomic dimension-indexed assumption asserting mclean h1
zero extension localization claim.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name mclean h1 zero extension localization, the proposition
  mclean h1 zero extension localization claim dimension type.
mclean_trace_dirichlet_green_v3
Isabelle code

 locale mclean_trace_dirichlet_green_v3 =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_trace_dirichlet_green_v3:
     "\<forall>U a. mclean_trace_dirichlet_green_claim_v3
       (U :: ’n cgu_point set) a"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     49

English mathematical translation
Mathematical role: An atomic dimension-indexed universal trace assumption about
mclean trace dirichlet green claim v3.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name mclean trace dirichlet green v3, that for every U and every a,
   mclean trace dirichlet green claim v3 U a
   holds, where U is explicitly a set of objects of type ’n cgu point. The argument
order is U, then a. No further restriction on these universally quantified variables
is stated.
hormander_regular_distribution_injectivity
Isabelle code

 locale hormander_regular_distribution_injectivity =
   fixes dimension_type :: "’n::finite itself"
   assumes hormander_regular_distribution_injectivity:
     "hormander_regular_distribution_injectivity_claim dimension_type"


English mathematical translation
Mathematical role: An atomic dimension-indexed injectivity assumption asserting
hormander regular distribution injectivity claim.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name hormander regular distribution injectivity, the proposition
  hormander regular distribution injectivity claim dimension type.
mclean_graph_supported_h1_zero
Isabelle code

 locale mclean_graph_supported_h1_zero =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_graph_supported_h1_zero:
     "mclean_graph_supported_h1_zero_claim dimension_type"


English mathematical translation
Mathematical role: An atomic dimension-indexed graph-support assumption assert-
ing mclean graph supported h1 zero claim.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name mclean graph supported h1 zero, the proposition
   mclean graph supported h1 zero claim dimension type.
mclean_h1_zero_bidual_representation_v2
Isabelle code

 locale mclean_h1_zero_bidual_representation_v2 =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_h1_zero_bidual_representation_v2:
     "mclean_h1_zero_bidual_representation_claim_v2 dimension_type"
50                             CĂTĂLIN I. CÂRSTEA

English mathematical translation
Mathematical role: An atomic dimension-indexed bidual assumption asserting
mclean h1 zero bidual representation claim v2.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name mclean h1 zero bidual representation v2, the proposition
  mclean h1 zero bidual representation claim v2 dimension type.
mclean_smooth_generator_ambient_lift_v2
Isabelle code
 locale mclean_smooth_generator_ambient_lift_v2 =
   assumes mclean_smooth_generator_ambient_lift_v2:
     "mclean_smooth_generator_ambient_lift_claim_v2
       TYPE(’n::finite) TYPE(’c::finite) TYPE(’h::finite)"

English mathematical translation
Mathematical role: An atomic assumption involving three independently selected
finite-dimensional carrier types.
   Assume, under the name mclean smooth generator ambient lift v2, the
proposition
   mclean smooth generator ambient lift claim v2 TYPE(’n::finite)
TYPE(’c::finite) TYPE(’h::finite).
   Here the three arguments, in order, select the finite-dimensional carrier types
’n, ’c, and ’h. No dimension is specified for any of them, and no equality or
relationship among the three carrier types is assumed.
mclean_hyperplane_offset_source
Isabelle code
 locale mclean_hyperplane_offset_source =
   assumes mclean_hyperplane_offset_source:
     "mclean_hyperplane_offset_source_claim
       TYPE(’m::finite) TYPE(’n::finite)"

English mathematical translation
Mathematical role: An atomic assumption involving two independently selected
finite-dimensional carrier types.
   Assume, under the name mclean hyperplane offset source, the proposition
   mclean hyperplane offset source claim TYPE(’m::finite)
TYPE(’n::finite).
   Here the two arguments, in order, select the finite-dimensional carrier types ’m
and ’n. No dimension is specified for either, and no equality or relationship between
the two carrier types is assumed.
kang_yun_ltu_local_boundary_metric_v6
Isabelle code
 locale kang_yun_ltu_local_boundary_metric_v6 =
   fixes dimension_type :: "’n::finite itself"
   assumes kang_yun_ltu_local_boundary_metric_v6:
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     51

     "\<forall>M P1 P2 U gamma normal offset g1 g2 a1 a2 rho1 rho2.
       kang_yun_ltu_local_boundary_metric_claim_v6
         (M :: (’n, ’c::finite, ’h::finite) cgu_model)
         P1 P2 U gamma normal offset g1 g2 a1 a2 rho1 rho2"


English mathematical translation
Mathematical role: An atomic dimension-indexed universal boundary-metric as-
sumption about kang yun ltu local boundary metric claim v6.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. Assume, under the
name kang yun ltu local boundary metric v6, that for every
   M, P1, P2, U, gamma, normal, offset, g1, g2, a1, a2, rho1, and rho2,
   the proposition
   kang yun ltu local boundary metric claim v6 M P1 P2 U gamma normal
offset g1 g2 a1 a2 rho1 rho2
   holds. The variable M is explicitly of type (’n, ’c::finite, ’h::finite) cgu
model: its first type parameter is the finite carrier type ’n selected by dimension
type, while ’c and ’h are also finite carrier types; no dimension is specified for any
of them. The arguments occur in exactly the displayed order. All thirteen variables
are universally quantified, and no further restriction on them is stated.
piecewise_polynomial_ucp_literature
Isabelle code

 locale piecewise_polynomial_ucp_literature =
   analytic: hormander_analytic_elliptic_ucp dimension_type +
   locality: hormander_weak_gradient_locality dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed package combining named analytic and
locality packages.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension.  The locale
piecewise polynomial ucp literature assumes exactly these two parent pack-
ages:
    (1) hormander analytic elliptic ucp, instantiated with dimension type
        and included as the named component analytic.
    (2) hormander weak gradient locality, instantiated with dimension type
        and included as the named component locality.
  No additional assumption is stated.
cgu_volume_annihilator_literature_base
Isabelle code

 locale cgu_volume_annihilator_literature_base =
   smooth: mclean_smooth_test_h1_zero dimension_type +
   injectivity: hormander_regular_distribution_injectivity dimension_type
   for dimension_type :: "’n::finite itself"
52                               CĂTĂLIN I. CÂRSTEA

English mathematical translation
Mathematical role: A dimension-indexed volume package combining smoothness
and injectivity packages.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu
volume annihilator literature base assumes exactly these two parent packages:
      (1) mclean smooth test h1 zero, instantiated with dimension type and in-
          cluded as the named component smooth.
      (2) hormander regular distribution injectivity,       instantiated with
          dimension type and included as the named component injectivity.
     No additional assumption is stated.
cgu_volume_gradient_annihilator_literature_base
Isabelle code

 locale cgu_volume_gradient_annihilator_literature_base =
   volume: cgu_volume_annihilator_literature_base dimension_type +
   locality: hormander_weak_gradient_locality dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed package combining named volume and
locality packages.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu
volume gradient annihilator literature base assumes exactly these two par-
ent packages:
      (1) cgu volume annihilator literature base,        instantiated   with
          dimension type and included as the named component volume.
      (2) hormander weak gradient locality, instantiated with dimension type
          and included as the named component locality.
     No additional assumption is stated.
cgu_graph_interface_annihilator_literature_base
Isabelle code

 locale cgu_graph_interface_annihilator_literature_base =
   volume_gradient: cgu_volume_gradient_annihilator_literature_base dimension_type +

     localization: mclean_h1_zero_extension_localization dimension_type +
     graph_support: mclean_graph_supported_h1_zero dimension_type
     for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed package combining volume-gradient, lo-
calization, and graph-support packages.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     53

graph interface annihilator literature base assumes exactly these three par-
ent packages:
    (1) cgu volume gradient annihilator literature base, instantiated with
        dimension type and included as the named component volume gradient.
    (2) mclean h1 zero extension localization, instantiated with dimension
        type and included as the named component localization.
    (3) mclean graph supported h1 zero, instantiated with dimension type and
        included as the named component graph support.
   No additional assumption is stated.
cgu_graph_interface_source_approximation_literature_base
Isabelle code
 locale cgu_graph_interface_source_approximation_literature_base =
   annihilator: cgu_graph_interface_annihilator_literature_base dimension_type +
   bidual: mclean_h1_zero_bidual_representation_v2 dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed graph-source package combining named
annihilator and bidual packages.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu graph
interface source approximation literature base assumes exactly these two
parent packages:
    (1) cgu graph interface annihilator literature base, instantiated with
        dimension type and included as the named component annihilator.
    (2) mclean h1 zero bidual representation v2,              instantiated     with
        dimension type and included as the named component bidual.
  No additional assumption is stated.
cgu_runge_literature_base
Isabelle code
 locale cgu_runge_literature_base =
   evans: evans_poincare_elliptic_green dimension_type +
   smooth: mclean_smooth_test_h1_zero dimension_type +
   ucp: piecewise_polynomial_ucp_literature dimension_type +
   localization: mclean_h1_zero_extension_localization dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed package assembling four named assump-
tion packages.
   Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu
runge literature base assumes exactly these four parent packages:
    (1) evans poincare elliptic green, instantiated with dimension type and
        included as the named component evans.
54                             CĂTĂLIN I. CÂRSTEA

      (2) mclean smooth test h1 zero, instantiated with dimension type and in-
          cluded as the named component smooth.
      (3) piecewise polynomial ucp literature, instantiated with dimension
          type and included as the named component ucp.
      (4) mclean h1 zero extension localization, instantiated with dimension
          type and included as the named component localization.
     No additional assumption is stated.
cgu_graph_dirichlet_literature_base_v3
Isabelle code
 locale cgu_graph_dirichlet_literature_base_v3 =
   cgu_runge_literature_base dimension_type +
   trace: mclean_trace_dirichlet_green_v3 dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed package combining a base package with a
named trace package.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu graph
dirichlet literature base v3 assumes exactly these two parent packages:
    (1) cgu runge literature base, instantiated with dimension type.
    (2) mclean trace dirichlet green v3, instantiated with dimension type
        and included as the named component trace.
  No additional assumption is stated.
cgu_graph_interface_conormal_context
Isabelle code
 locale cgu_graph_interface_conormal_context =
   cgu_graph_dirichlet_literature_base_v3 dimension_type +
   graph_source: cgu_graph_interface_source_approximation_literature_base
      dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: A dimension-indexed package combining a base package with a
named graph-source package.
  Fix dimension type of type ’n::finite itself, selecting the finite-
dimensional carrier type ’n without specifying its dimension. The locale cgu
graph interface conormal context assumes exactly these two parent packages:
    (1) cgu graph dirichlet literature base v3,           instantiated   with
        dimension type.
    (2) cgu graph interface source approximation literature base, instan-
        tiated with dimension type and included as the named component graph
        source.
  No additional assumption is stated.
cgu_selected_face_dn_context
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     55

Isabelle code
 locale cgu_selected_face_dn_context =
   cgu_graph_interface_conormal_context dimension_type +
   mclean_smooth_generator_ambient_lift_v2
   for dimension_type :: "’n::finite itself"

English mathematical translation
Mathematical role: A dimension-indexed package combining a structural package
with an additional unparameterized package.
   Fix dimension type of type ’n::finite itself; that is, dimension type se-
lects the finite-dimensional carrier type ’n, without specifying its dimension. The
locale cgu selected face dn context assumes exactly these two parent packages:
     (1) cgu graph interface conormal context, instantiated with dimension
         type.
     (2) mclean smooth generator ambient lift v2.
   No additional assumption is stated.
cgu_terminal_recovery_context_v7
Isabelle code
 locale cgu_terminal_recovery_context_v7 =
   cgu_selected_face_dn_context "TYPE(’n::finite)" +
   offset: mclean_hyperplane_offset_source +
   boundary_metric: kang_yun_ltu_local_boundary_metric_v6 "TYPE(’n)"

English mathematical translation
Mathematical role: A top-level package combining three assumption packages.
   The locale cgu terminal recovery context v7 assumes exactly the following
three parent packages:
    (1) cgu selected face dn context, instantiated at TYPE(’n::finite). Here
        TYPE(’n::finite) selects the finite-dimensional carrier type ’n; it does
        not specify or imply any particular dimension.
    (2) mclean hyperplane offset source, included as the named component
        offset.
    (3) kang yun ltu local boundary metric v6, instantiated at TYPE(’n) and
        included as the named component boundary metric; this selects the same
        finite-dimensional carrier type ’n, without specifying its dimension.
   No additional parameters or assumptions are stated in this locale.
56                             CĂTĂLIN I. CÂRSTEA

Statements

Manuscript conclusions

MAIN-001: cgu_global_uniqueness_claim_v7
English original and manuscript locator
    Theorem thm:main of [1] states:
    Let n ≥ 3, let Ω ⊂ Rn be a bounded Lipschitz domain, and let D = {Dα }α∈A
be a known finite Lipschitz subdivision of Ω that is internally flat up to a skeleton.
Let Nα ≥ 0. Suppose that σ (1) , σ (2) ∈ P(D, {Nα }), and assume that, at every
recovery step and for j = 1, 2, the polynomial extension of σ (j) |Dαr is positive
definite on the triple-intersection sets Wr,ijk appearing in Definition [source refer-
ence: def:stripping-order]. We also assume that, for j = 1, 2, the polynomial
extensions in the recovered cells adjacent to the auxiliary exterior half-balls remain
elliptic in those half-balls whenever the half-balls are used.
    Let Σ ⊂ ∂Ω be a nonempty relatively open measured set. Assume that the
subdivision admits an admissible flat-face recovery order relative to Σ, in the sense
of Definition [source reference: def:stripping-order]. If
                                 ΛΩ           Ω
                                  σ (1) ,Σ = Λσ (2) ,Σ ,

then
                                 σ (1) = σ (2)   in Ω.
Equivalently, the polynomial matrices defining the two conductivities agree on every
cell of the subdivision.
Isabelle code

 definition cgu_global_uniqueness_claim_v7 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> bool"
 where
   "cgu_global_uniqueness_claim_v7 M P1 P2 \<longleftrightarrow>
     (3 \<le> CARD(’n) \<and>
      cgu_graph_subdivision_core_v7 M \<and>
      cgu_piecewise_polynomial_class M P1 \<and>
      cgu_piecewise_polynomial_class M P2 \<and>
      cgu_recovery_geometry_operational_v6 M \<and>
      cgu_recovery_extension_admissible M P1 \<and>
      cgu_recovery_extension_admissible M P2 \<and>
      cgu_local_dn_equal M P1 P2 (cgu_domain M) (cgu_measured M))
     \<longrightarrow> P1 = P2"


English mathematical translation of the Isabelle code
   Let n ≥ 3. If M is a regular cell decomposition with the full recovery geometry
of Section 2, if P1 , P2 are admissible coefficient families compatible with recovery,
and if they have the same local boundary-energy data on (Ω, Γ), then

                                      P1 = P2 .
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     57

   This is equality of the entire coefficient families as finite coefficient representa-
tions, not merely almost-everywhere or pointwise equality of their evaluated matri-
ces.
MAIN-002: cgu_uniform_degree_admissible_injectivity_claim_v7
English original and manuscript locator
    The corollary of [1] states:
    Suppose Nα ≤ N for all cells. If the subdivision admits an admissible flat-
face recovery order relative to Σ in which each cell is accessible through at least
N + 3 flat faces whose supporting hyperplanes satisfy the corresponding genericity
and triple-intersection geometry, and the recovered regions satisfy the stated face-
connectedness assumptions, then the following holds. For any σ (1) , σ (2) ∈ P(D, N )
that satisfy the coefficient-dependent triple-region positivity and auxiliary half-ball
ellipticity hypotheses of Theorem [source reference: thm:main] for this recovery
order, equality of their local DN maps on Σ implies σ (1) = σ (2) . Equivalently, the
local DN map is injective on the subclass of P(D, N ) satisfying those coefficient-
dependent admissibility conditions.
Isabelle code
 definition cgu_uniform_degree_admissible_injectivity_claim_v7 ::
   "nat \<Rightarrow> (’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
      bool"
 where
   "cgu_uniform_degree_admissible_injectivity_claim_v7 N M \<longleftrightarrow>
     (3 \<le> CARD(’n) \<and>
      cgu_graph_subdivision_core_v7 M \<and>
      (\<forall>c. cgu_degree M c = N) \<and>
      cgu_recovery_geometry_operational_v6 M)
     \<longrightarrow>
     (\<forall>P1 P2.
       cgu_piecewise_polynomial_class M P1 \<and>
       cgu_piecewise_polynomial_class M P2 \<and>
       cgu_recovery_extension_admissible M P1 \<and>
       cgu_recovery_extension_admissible M P2 \<and>
       cgu_local_dn_equal M P1 P2 (cgu_domain M) (cgu_measured M)
       \<longrightarrow> P1 = P2)"

English mathematical translation of the Isabelle code
   Fix N ∈ N. Let n ≥ 3, let M be a regular cell decomposition with full recovery
geometry, and assume Nc = N for every cell. Then for every P1 , P2 , if both are
admissible and recovery-compatible and have the same local boundary-energy data
on (Ω, Γ), one has P1 = P2 as coefficient families.
58                              CĂTĂLIN I. CÂRSTEA

Cited results
ANALYTIC-ELLIPTIC
Formal identifier: hormander_analytic_elliptic_ucp_claim
Relationship to source: derived.
Source attribution and locator
   Hörmander [19], Section 8.3, printed p. 271, equations (8.3.1)–(8.3.4) and Corol-
lary 8.3.2.
Complete source theorem statement (faithful mathematical restatement)
                                a (x)Dα , the principal symbol is the homogeneous
                      P
   For P (x, D) =        |α|≤mPα
degree-m part pm (x, ξ) = |α|=m aα (x)ξ α . The characteristic set consists of the
nonzero covectors (x, ξ) for which pm (x, ξ) = 0. The operator is elliptic precisely
when this set is empty, equivalently when pm (x, ξ) ̸= 0 for every ξ ̸= 0.
Source attribution and locator
   Hörmander [19], Theorem 8.6.1, printed p. 306.
Complete source theorem statement (faithful mathematical restatement)
   If the coefficients of a differential operator P are real analytic, then an analytic
singularity of a distribution u which is not already an analytic singularity of P u
can occur only at a characteristic covector; in standard notation,

                          WFA (u) ⊆ WFA (P u) ∪ Char P.
Source attribution and locator
    Hörmander [19], Theorem 8.6.5 and its stated elliptic consequence, printed p.
309.
Complete source theorem statement (faithful mathematical restatement)
    If u is a distribution on an open set X and P u = 0, then every exterior conormal
to supp u is characteristic for P . Hence, if P is elliptic, the support of u has
no boundary point in X. Consequently, when X is connected, a solution which
vanishes in a neighborhood of one point vanishes throughout X.
Source attribution and locator
    Hörmander [19], Theorem 1.2.5, printed p. 15.
Complete source theorem statement (faithful mathematical restatement)
    If f, g ∈ L1loc (X) and X f ϕ = X gϕ for every ϕ ∈ Cc∞ (X), then f = g almost
                            R        R

everywhere on X.
Source attribution and locator
    Hörmander [19], regular-distribution identification on printed p. 37 and Defini-
tion 3.1.1 on printed p. 55.
Complete source theorem statement (faithful mathematical restatement)
    Printed p. 37 identifies L1loc (X) Rmodulo almost-everywhere equality injectively
with the regular distributions ϕ 7→ X f ϕ. Definition 3.1.1, printed p. 55, defines
(∂i u)(ϕ) = −u(∂i ϕ) and multiplication of a distribution by a smooth function.
Exact derived mathematical result formalized
    Let X ⊂ Rn , n ≥ 1, be open and connected. Let A(x) be a symmetric ma-
trix polynomial which is uniformly positive definite on an open neighborhood of
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     59

X. If a real locally square-integrable regular distribution u is a weak solution of
− div(A∇u) = 0 on X, and u = 0 almost everywhere on some nonempty open
subset of X, then u = 0 almost everywhere on X. This is the exact mathematical
content of the formal interface.
    For the notation correspondence, polynomial entries are real analytic and the
principal symbol of − div(A∇·), in Hörmander’s Dj = (1/i)∂j convention, is
ξ T A(x)ξ. Uniform positive definiteness makes it nonzero for ξ ̸= 0. The weak
variational identity is the distribution equation, and the regular-distribution re-
sults convert distributional vanishing to almost-everywhere vanishing. Polynomial-
ity and uniform ellipticity near the closure are conservative strengthenings of local
analyticity and ellipticity.
Isabelle code

 definition hormander_analytic_elliptic_ucp_claim ::
   "’n::finite ucp_point set \<Rightarrow> ’n ucp_coefficient \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow> bool"
 where
   "hormander_analytic_elliptic_ucp_claim X P u \<longleftrightarrow>
     ((0 < CARD(’n) \<and> open X \<and> connected X \<and>
       ucp_matrix_polynomial P \<and>
       (\<forall>x. ucp_symmetric_matrix (P x)) \<and>
       ucp_uniformly_elliptic_near X P \<and>
       ucp_weak_solution_on X P u \<and>
       (\<exists>V. V \<noteq> {} \<and> open V \<and> V \<subseteq> X \<and>
         (AE x in lborel. x \<in> V \<longrightarrow> u x = 0)))
      \<longrightarrow> (AE x in lborel. x \<in> X \<longrightarrow> u x = 0))"


English mathematical translation of the Isabelle code
  Let n > 0, let X ⊂ Rn be open and connected, and let P : Rn → Rn×n have
polynomial entries, be symmetric at every ambient point, and be uniformly elliptic
on an open neighborhood of X. If u is a locally weak solution of div(P ∇u) = 0 in
X, and there exists a nonempty open V ⊂ X such that

                     u=0     for Lebesgue-a.e. ambient x ∈ V,
  then

                     u=0     for Lebesgue-a.e. ambient x ∈ X.

WEAK-GRADIENT-LOCALITY
Formal identifier: hormander_weak_gradient_locality_claim
Relationship to source: derived.
Source attribution and locator
   Hörmander [19], Definitions 1.2.1–1.2.2, the following zero-extension observation,
and Lemma 1.2.3, printed p. 14.
Complete source theorem statement (faithful mathematical restatement)
   The test space on an open set X is Cc∞ (X), with support defined as the closure
of the nonzero set; its members extend smoothly by zero to the ambient Euclidean
space. The lemma constructs a nonnegative compactly supported smooth bump
positive at a prescribed point. Translation, scaling, a finite compact subcover, and
60                              CĂTĂLIN I. CÂRSTEA

summation therefore give, for every compact K ⋐ X, a nonnegative test function
which is strictly positive on K.
Source attribution and locator
   Hörmander [19], Theorem 1.2.5, printed p. 15.
Complete source theorem statement (faithful mathematical restatement)
   Two locally integrable functions with identical pairings against every member of
Cc∞ (X) are equal almost everywhere.
Source attribution and locator
   Hörmander [19], regular-distribution identification on printed p. 37 and Defini-
tion 3.1.1 on printed p. 55.
Complete source theorem statement (faithful mathematical restatement)
   Printed p. 37 identifies locally integrable functions modulo almost-everywhere
equality with their regular distributions. Definition 3.1.1, printed p. 55, defines the
distributional derivative by (∂i u)(ϕ) = −u(∂i ϕ).
Exact derived mathematical result formalized
   Let X be open. Suppose real u and real vector field Du satisfy the project’s
local-square-integrability and weak-gradient predicates on X, and suppose u = 0
almost everywhere on X. Then Du = 0 almost    R everywhereR on X.
   Coordinatewise, the weak identity gives X u ∂i ϕ = − X (Du)i ϕ; the left side
is zero. The weak-gradient product-integrability clause, combined with a positive
localized test, proves (Du)i ∈ L1loc (X). Theorem 1.2.5 then makes each component
zero almost everywhere, and finite dimensionality combines the component conclu-
sions. The formal real test class is a conservative specialization of Hörmander’s
complex convention: real and imaginary parts recover all complex pairings.
Isabelle code

 definition hormander_weak_gradient_locality_claim ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow>
    (’n ucp_point \<Rightarrow> ’n ucp_point) \<Rightarrow> bool"
 where
   "hormander_weak_gradient_locality_claim X u Du \<longleftrightarrow>
     ((open X \<and>
       ucp_locally_square_integrable_on X u \<and>
       ucp_locally_square_integrable_on X Du \<and>
       ucp_weak_gradient_on X u Du \<and>
       (AE x in lborel. x \<in> X \<longrightarrow> u x = 0))
      \<longrightarrow> (AE x in lborel. x \<in> X \<longrightarrow> Du x = 0))"


English mathematical translation of the Isabelle code
                                      1
  Let X be open and let (u, G) ∈ Hloc,pair (X). If u(x) = 0 for Lebesgue-a.e.
ambient x ∈ X, then G(x) = 0 for Lebesgue-a.e. ambient x ∈ X.
HORMANDER-REGULAR-DISTRIBUTION-INJECTIVITY
Formal identifier: hormander_regular_distribution_injectivity_claim
Relationship to source: direct.
Source attribution and locator
  Hörmander [19], Definitions 1.2.1–1.2.2 and Lemma 1.2.3, printed p. 14.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     61

Complete source theorem statement (faithful mathematical restatement)
   These results define the smooth compactly supported tests on an open set, their
support, and the localized smooth bumps used to separate a nonzero locally inte-
grable function from the zero distribution.
Source attribution and locator
   Hörmander [19], Theorem 1.2.5, printed p. 15.
Complete source theorem statement (faithful mathematical restatement)
   For an open X ⊂ Rn , if f, g ∈ L1loc (X) satisfy X f ϕ = X gϕ for every ϕ ∈
                                                       R         R

Cc∞ (X), then f = g almost everywhere on X.
Source attribution and locator
   Hörmander [19], regular-distribution identification on printed p. 37.
Complete source theorem statement (faithful mathematical restatement)
   The source expresses the preceding result as injectivity of the regular-distribution
embedding of L1loc (X) modulo almost-everywhere equality.
   Direct formal specialization.
   For every open X and real u ∈ L1 (X), if uϕ is integrable and X uϕ = 0 for
                                                                        R

every project smooth compact test ϕ, then u = 0 almost everywhere on X. Global
L1 (X) is stronger than the source’s local integrability, the comparison function
is specialized to zero, and the project test predicate is the globally zero-extended
realization of Cc∞ (X). The explicit product-integrability premise prevents use of
Isabelle’s totalized integral outside the ordinary integrable case.
Isabelle code
 definition hormander_regular_distribution_injectivity_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "hormander_regular_distribution_injectivity_claim dimension_type \<
      longleftrightarrow>
     (\<forall>X :: ’n cgu_point set. \<forall>u.
       open X \<and> hormander_regular_distribution_test_zero_on X u
       \<longrightarrow>
       (AE x in restrict_space lborel X. u x = 0))"


English mathematical translation of the Isabelle code
  In every finite dimension, for every open X and every Lebesgue-integrable u on
X, if for every ϕ ∈ D(X) the product uϕ is integrable and
                                    Z
                                        uϕ = 0,
                                      X
     then u = 0 almost everywhere with respect to Lebesgue measure restricted to
X.
EVANS-POINCARE-ELLIPTIC-GREEN
Formal identifier: evans_poincare_elliptic_green_claim
Relationship to source: derived.
Source attribution and locator
  Evans [20], Section 5.6.1, Theorem 3 and its separately displayed particular
consequence, printed pp. 279–280.
62                             CĂTĂLIN I. CÂRSTEA

Complete source theorem statement (faithful mathematical restatement)
   If U ⊂ Rn is bounded and open and u ∈ W01,p (U ), 1 ≤ p < ∞, then ∥u∥Lp (U ) ≤
C∥Du∥Lp (U ) , with C depending on U, n, p. The interface uses only p = 2.
Source attribution and locator
   Evans [20], Section 5.9.1, Theorem 1, printed pp. 299–300.
Complete source theorem statement (faithful mathematical restatement)
   The negative Sobolev space H −1 (U ) is the bounded dual of H01 (U ).
                                                                       PEquivalently,
                                                                         n
every such functional has a representation by L2 functions f = f 0 − i=1 ∂i f i , and
conversely every such expression defines a bounded functional on H01 (U ).
Source attribution and locator
   Evans [20], Sections 6.1.1–6.1.2, printed pp. 311–315.
Complete source theorem statement (faithful mathematical restatement)
   On a bounded open domain, a divergence-form operator with bounded measur-
able leading coefficients, uniformly elliptic almost everywhere (and symmetric in the
symmetric case), gives the bilinear energy form on H01 (U ). A weak zero-Dirichlet
solution is an element u ∈ H01 (U ) satisfying that bilinear identity against every
v ∈ H01 (U ).
Source attribution and locator
   Evans [20], Section 6.2.1, Theorem 1 (Lax–Milgram), printed pp. 315–317.
Complete source theorem statement (faithful mathematical restatement)
   If H is a real Hilbert space and a bilinear form B : H × H → R is bounded and
coercive, |B[u, v]| ≤ M ∥u∥∥v∥ and B[u, u] ≥ β∥u∥2 with β > 0, then every f ∈ H ∗
has a unique u ∈ H satisfying B[u, v] = f (v) for all v ∈ H, and ∥u∥ ≤ ∥f ∥/β.
Source attribution and locator
   Evans [20], Section 6.2.2, Theorem 2, printed pp. 317–318.
Complete source theorem statement (faithful mathematical restatement)
   Under the elliptic coefficient hypotheses, the weak bilinear form satisfies
|B[u, v]| ≤ C∥u∥H01 (U ) ∥v∥H01 (U ) and a Gårding bound B[u, u] ≥ β∥u∥2H 1 (U ) −
                                                                               0
γ∥u∥2L2 (U ) for constants C, β > 0 and γ ≥ 0. Thus the leading elliptic part controls
the gradient norm, while lower-order terms cost only an L2 term.
Source attribution and locator
   Evans [20], Section 6.2.2, Theorem 3, printed pp. 318–319.
Complete source theorem statement (faithful mathematical restatement)
   There is γ ≥ 0 such that, for f ∈ L2 (U ) and every µ ≥ γ, the shifted zero-
Dirichlet weak problem Lu + µu = f has a unique solution in H01 (U ), with the
corresponding energy estimate. This theorem does not itself state the unshifted
arbitrary-H −1 result below.
Exact derived mathematical result formalized
   Let U ̸= ∅ be bounded and open, and let a(x) be a chosen restricted-Borel mea-
surable, pointwise bounded, pointwise symmetric matrix with one positive point-
wise uniform ellipticity constant. Then the pure leading energy form is bounded
and strictly coercive on the project’s H01 (U ) quotient. Moreover, one constant
C ≥ 0, depending only on U, a, works for every bounded real linear source F with
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     63

bound K: there is a zero-boundary weak solution of − div(a∇u) = F , it satisfies
∥u∥H 1 (U ) ≤ CK, and it is unique modulo zero H 1Rdistance.
   The derivation takes H = H01 (U ) and B[u, v] = U (aDu)·Dv. Coefficient bound-
edness gives continuity; ellipticity plus the p = 2 Poincaré inequality gives coercivity
in the full project H 1 norm; Section 5.9.1 identifies the source with an element of
H ∗ ; Lax–Milgram gives the unshifted solution, uniqueness, and the uniform esti-
mate. The pointwise representative assumptions conservatively strengthen Evans’s
almost-everywhere coefficient assumptions.
Isabelle code

 definition evans_poincare_elliptic_green_claim ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "evans_poincare_elliptic_green_claim U a \<longleftrightarrow>
     (0 < CARD(’n) \<and> U \<noteq> {} \<and> open U \<and>
       evans_bounded_domain U \<and> evans_elliptic_coefficient_on U a)
     \<longrightarrow>
     (mclean_variational_form_on U a \<and>
       (\<exists>C. 0 \<le> C \<and>
         (\<forall>F K. mclean_source_bound_on U F K \<longrightarrow>
           (\<exists>u Du. mclean_green_solution_for U a F u Du \<and>
             mclean_h1_norm U u Du \<le> C * K \<and>
             (\<forall>v Dv. mclean_green_solution_for U a F v Dv
               \<longrightarrow>
               cgu_h1_squared_distance U u Du v Dv = 0)))))"


English mathematical translation of the Isabelle code
   Let n > 0, let U ̸= ∅ be open and bounded, and let a be Borel measurable on
U , pointwise bounded there by one constant B ≥ 0, symmetric at every point of U ,
and uniformly elliptic there: for some θ > 0,

                         θ∥ξ∥2 ≤ ξ · a(x)ξ   (x ∈ U, ξ ∈ Rn ).
   Then the energy form BU,a is stable, and there exists C ≥ 0, independent of F
and K, such that whenever F is bounded linear on H01 (U ) with bound K, there is
a source solution (u, G) satisfying

                                   ∥(u, G)∥U ≤ CK.
  Every other source solution (v, H) has

                                d2U ((u, G), (v, H)) = 0.

KANG-YUN-LTU-LOCAL-BOUNDARY-METRIC
Formal identifier: kang_yun_ltu_local_boundary_metric_claim_v6
Relationship to source: derived.
Source attribution and locator
   Kang–Yun [21], weak energy pairing on printed p. 719 and localized-DN defini-
tion on printed p. 723.
Complete source theorem statement (faithful mathematical restatement)
64                              CĂTĂLIN I. CÂRSTEA

  For an open connected measured boundary patch Γ, the localized Dirichlet-to-
Neumann map takes H 1/2 boundary data supported in Γ, solves the conductivity/-
metric equation, and restricts the Neumann response to Γ. Its weak form is the
boundary energy pairing of an input solution with an arbitrary lift of the test trace.
Source attribution and locator
     Kang–Yun [21], Theorem 1.3, printed p. 723.
Complete source theorem statement (faithful mathematical restatement)
   Let two uniformly elliptic Riemannian metrics have C m,p regularity near a con-
nected open boundary patch Γ, with m ≥ 1 and p > 0. For every compact K ⋐ Γ,
the local DN maps stably determine the metrics near K, modulo a local diffeo-
morphism which fixes the boundary: after the appropriate pullback, the metric
difference is bounded by a positive power of the local-DN operator-norm difference.
In particular, equality of the local maps gives equality up to that boundary-fixing
gauge on K.
Source attribution and locator
     Kang–Yun [21], Lemmas 2.1 and 2.2, printed pp. 724–727.
Complete source theorem statement (faithful mathematical restatement)
   In boundary-normal coordinates and for a boundary point and tangential fre-
quency, the authors construct high-frequency boundary packets supported in an
arbitrarily small part of Γ, extend them into a shrinking boundary box DN , and
establish the packet, trace, and Sobolev norm bounds used in the asymptotic energy
calculation.
Source attribution and locator
  Kang–Yun [21], Section 3, equations (3.7)–(3.9) and the intervening Hardy in-
equality, printed pp. 728–731.
Complete source theorem statement (faithful mathematical restatement)
   Writing the exact solution as the explicit packet plus a correction, the source
proves the local correction estimate (3.7), the artificial-top trace estimate (3.8), the
displayed Hardy inequality before (3.9), and the weighted residual estimate (3.9).
In the notation used by the reviewed derivation, the local estimate is ∥sN ∥H 1 (DN ) ≤
CN 1−|α|/2 , with the subsequent estimates making the correction terms negligible
at the normalization used in the DN limit.
Source attribution and locator
     Kang–Yun [21], Theorem 4.1 and equations (4.5)–(4.8), printed pp. 731–733.
Complete source theorem statement (faithful mathematical restatement)
   The normalized high-frequency local-DN energy limit at a chosen boundary point
determines the tangential metric quadratic form there. Varying the tangential
covector and polarizing determines the complete tangential bilinear form.
Source attribution and locator
   Kang–Yun [21], boundary-normal-coordinate and diffeomorphism reduction,
printed pp. 733–734.
Complete source theorem statement (faithful mathematical restatement)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     65

    A smooth positive metric near the observed patch can be put into the boundary-
normal form used by the packet computation. The comparison of the two normal-
coordinate charts is a local diffeomorphism whose restriction to the boundary is the
identity; hence its differential is the identity on tangent vectors.
Source attribution and locator
    Lassas–Taylor–Uhlmann [22], remote rough-boundary setting on printed p. 209
and local-symbol discussion in Section 2, printed pp. 210–211.
Complete source theorem statement (faithful mathematical restatement)
    In their analytic, Wiener-regular complete-manifold setting, boundary roughness
is allowed away from the measured analytic patch, and the boundary symbol is
obtained locally from the DN map. This is corroboration of locality in a different
setting, not a theorem proving the graph-domain corollary below.
Exact derived mathematical result formalized
    In dimension at least three, let U be a bounded connected graph-Lipschitz do-
main contained in the fixed subdivision model. Let γ be a nonempty relatively open
flat boundary patch with a full one-sided collar, disjoint from the subdivision skele-
ton. Suppose each of two globally bounded uniformly elliptic piecewise-polynomial
coefficients agrees
                  p on an open collar of γ with a smooth positive metric-density
realization aj = det gj gj−1 . If the completed real weak local-DN energy pairings
agree for every supported input/test trace, with solutions existing for those data,
then for every x ∈ γ and every pair of vectors tangent to the supporting hyperplane,
g1 (x)(v, w) = g2 (x)(v, w). No normal component or remote coefficient is identified.
    The derivation localizes the Kang–Yun packet with a fixed smooth collar cut-
off. Cutoff derivatives occur a fixed positive normal distance from the boundary
and are exponentially small; graph-domain trace lifting, Poincaré, and global el-
lipticity give the correction bound without remote smoothness. Four real bilinear
pairings reconstruct the complex packet pairing. The boundary-fixing gauge has
identity tangential differential, so equality after pullback gives the stated covariant
tangential equality. Pointwise shrinking handles a disconnected formal patch. Nei-
ther paper prints this exact graph-domain implication verbatim, and LTU supplies
corroboration only.
Isabelle code

 definition kang_yun_ltu_local_boundary_metric_claim_v6 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_density \<Rightarrow> ’n lu_density \<Rightarrow> bool"
 where
   "kang_yun_ltu_local_boundary_metric_claim_v6 M P1 P2 U gamma normal offset
       g1 g2 a1 a2 rho1 rho2 \<longleftrightarrow>
     (3 \<le> CARD(’n) \<and>
      cgu_graph_subdivision_core_v7 M \<and>
      cgu_piecewise_polynomial_class M P1 \<and>
      cgu_piecewise_polynomial_class M P2 \<and>
      cgu_graph_lipschitz_domain_v5 U \<and>
66                                 CĂTĂLIN I. CÂRSTEA

        U \<subseteq> cgu_domain M \<and>
        cgu_flat_face_patch U normal offset gamma \<and>
        gamma \<inter> cgu_subdivision_edge_corner_set M = {} \<and>
        lu_smooth_metric_extension_near M P1 U gamma g1 a1 rho1 \<and>
        lu_smooth_metric_extension_near M P2 U gamma g2 a2 rho2 \<and>
        cgu_local_dn_equal M P1 P2 U gamma)
       \<longrightarrow> lu_induced_boundary_metrics_equal_on gamma normal g1 g2"


English mathematical translation of the Isabelle code
  Let n ≥ 3. Suppose M is a regular cell decomposition, P1 , P2 are admissible,
U is a Lipschitz-graph domain with U ⊂ Ω, and γ is a one-sided planar boundary
patch of U with unit normal ν and offset b. Assume

                                    γ ∩ ΣM = ∅,
   each Pi is realized near γ by a metric/conductivity package (gi , ai , ρi ), and P1 , P2
have the same local boundary-energy data on (U, γ). Then g1 and g2 agree tangen-
tially on γ:

                                 ξ · g1 (x)η = ξ · g2 (x)η
     for every x ∈ γ and every ξ, η ⊥ ν.
MCLEAN-GRAPH-SUPPORTED-H1-ZERO
Formal identifier: mclean_graph_supported_h1_zero_claim
Relationship to source: direct.
Source attribution and locator
   McLean [23], Definition 3.28, printed pp. 89–90.
Complete source theorem statement (faithful mathematical restatement)
   A Lipschitz domain has compact boundary and a finite cover by rigid Cartesian-
coordinate neighborhoods in which the domain is a Lipschitz hypograph. Replacing
the local Lipschitz graph functions by continuous functions gives the book’s C 0 -
domain class; every Definition 3.28 Lipschitz domain is therefore a C 0 domain.
Source attribution and locator
   McLean [23], Theorem 3.29(ii), printed pp. 91–92.
Complete source theorem statement (faithful mathematical restatement)
   For a C 0 domain Ω and every real Sobolev order s, the smooth compactly sup-
ported class D(Ω) is dense, in the ambient H s (Rn ) norm, in the global Sobolev space
consisting of distributions supported in Ω. Equivalently, the ambient compact-test
closure equals that supported global Sobolev space.
   Direct formal specialization.
   At real scalar order s = 1, suppose U is a bounded graph-Lipschitz domain and
(u, Du) is a global project H 1 (Rn ) pair whose potential and selected weak gradient
vanish almost everywhere outside U . Then (u, Du) belongs to the project’s sequen-
tial H01 (U ) compact-test closure. The graph-Lipschitz premise is stronger than the
source’s C 0 hypothesis, the gradient-support premise is an additional compatible re-
striction, and source global convergence is stronger than the conclusion’s restricted
U -distance convergence.
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     67


 definition mclean_graph_supported_h1_zero_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_graph_supported_h1_zero_claim dimension_type \<longleftrightarrow>
     0 < CARD(’n) \<and>
     (\<forall>(U :: ’n cgu_point set) u Du.
       cgu_graph_lipschitz_domain_v5 U \<and>
       cgu_h1_pair_on UNIV u Du \<and>
       (AE x in lborel.
         x \<notin> closure U \<longrightarrow> u x = 0 \<and> Du x = 0)
       \<longrightarrow> cgu_h1_zero_pair_on U u Du)"


English mathematical translation of the Isabelle code
   This condition is the conjunction of n > 0 and the following assertion: for every
U, u, G, if U is a Lipschitz-graph domain, (u, G) ∈ H1 (Rn ), and, for Lebesgue-a.e.
ambient x,

                         x∈
                          / U =⇒ u(x) = 0 and G(x) = 0,
   then (u, G) ∈ H01 (U ).
MCLEAN-H1-ZERO-BIDUAL-REPRESENTATION
Formal identifier: mclean_h1_zero_bidual_representation_claim_v2
Relationship to source: derived.
Source attribution and locator
   McLean [23], weak-derivative Sobolev construction and Hilbert conclusion,
printed pp. 73–75.
Complete source theorem statement (faithful mathematical restatement)
   On every nonempty open U , Wpr (U ) consists of Lp functions possessing all weak
derivatives through order r in Lp , with the derivative graph norm. For p = 2, the
sum of the L2 inner products of the weak derivatives induces that norm, and W s (U )
is a Hilbert space for every real s ≥ 0.
Source attribution and locator
   McLean [23], zero-boundary closure notation, printed p. 77.
Complete source theorem statement (faithful mathematical restatement)
   The source defines the conventional zero-boundary space as the closure of D(U )
in the relevant Sobolev norm. For this interface the cited page supplies nomen-
clature only; no equality with a distinct supported Bessel-potential space on an
arbitrary open set is used.
Source attribution and locator
   McLean [23], Hilbert reflexivity statement, printed p. 79.
Complete source theorem statement (faithful mathematical restatement)
   Every Hilbert space is reflexive: the canonical isometric embedding J : H → H ∗∗ ,
(Ju)(F ) = F (u), is onto. Thus every bounded linear functional on H ∗ is evaluation
at some u ∈ H.
Exact derived mathematical result formalized
   For every nonempty open U , let H be the quotient Hilbert space represented by
project H01 (U ) potential/weak-gradient pairs. There exist a set E and seminorm p
68                              CĂTĂLIN I. CÂRSTEA

such that E is exactly the set of total raw functions inducing bounded real linear
functionals on H, and p(F ) is the least valid source bound, hence the operator
seminorm. Every carrier-relative real-linear g : E → R bounded by p is of the form
g(F ) = F (u, Du) for some project H01 (U ) pair.
   The project’s potential-plus-gradient norm is the order-one graph norm, and the
compact-test closure is a closed Hilbert subspace after quotienting zero distance.
Bounded raw sources descend to its continuous dual; the least bound is the dual
norm. A p-bounded g vanishes on the seminorm kernel, descends to the genuine
bidual, and reflexivity represents it by evaluation. The raw carrier E, least-bound
plumbing, and displayed evaluation formula are standard consequences, not state-
ments printed verbatim by McLean.
Isabelle code

 definition mclean_h1_zero_bidual_representation_claim_v2 ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_h1_zero_bidual_representation_claim_v2 dimension_type \<
      longleftrightarrow>
     (\<forall>U :: ’n cgu_point set.
       U \<noteq> {} \<and> open U
       \<longrightarrow>
       (\<exists>E p. mclean_h1_zero_bidual_realization_on_v2 U E p))"


English mathematical translation of the Isabelle code
    In every finite dimension, every nonempty open U ⊂ Rn admits a pair (E, p) with
all properties of the total-functional representation package in Section 5: E consists
exactly of the everywhere-defined functionals having some stipulated zero-boundary
bound, p is their least-bound seminorm, and every p-bounded linear map on E has
an existential pair representation. No quotienting or uniqueness is asserted.
MCLEAN-H1-ZERO-EXTENSION-LOCALIZATION
Formal identifier: mclean_h1_zero_extension_localization_claim
Relationship to source: derived.
Source attribution and locator
   McLean [23], smooth compact tests and the two compact-test closures, printed
pp. 61, 65, and 77–78.
Complete source theorem statement (faithful mathematical restatement)
   The test class is D(Ω) = Cc∞ (Ω). H0s (Ω) is its closure in the intrinsic/restriction
  s                     e s (Ω) is its closure in the ambient H s (Rn ) norm. These two
H (Ω) norm, whereas H
spaces are not identified on an arbitrary open set in this interface.
Source attribution and locator
   McLean [23], Theorem 3.6, printed p. 64.
Complete source theorem statement (faithful mathematical restatement)
   Given a closed set and an open neighborhood (equivalently, an arbitrarily small
prescribed neighborhood), there is a smooth cutoff taking values between zero and
one, equal to one on the closed set and zero outside the prescribed neighborhood.
For a compact set contained in an open set, the cutoff may be chosen compactly
supported in that open set.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     69

Source attribution and locator
  McLean [23], Theorem 3.16, printed p. 80.
Complete source theorem statement (faithful mathematical restatement)
   For every nonnegative integer m, the global weak-derivative space W m (Rn ) and
the Bessel-potential space H m (Rn ) are the same set with equivalent norms.
Source attribution and locator
  McLean [23], Theorem 3.20, printed p. 83.
Complete source theorem statement (faithful mathematical restatement)
   Multiplication by a smooth compactly supported cutoff is a bounded linear oper-
ator on H s (Ω) and, separately, on H
                                    e s (Ω). The theorem does not state a multiplier
             s
clause for H0 (Ω) under that name.
Exact derived mathematical result formalized
   Two order-one representative statements are formalized. First, if ∅ ̸= U ⊆ W
are open and (u, Du) is in the project H01 (U ) closure, then the zero extensions of
both representatives form a project H01 (W ) pair. Second, if nonempty open V ⊆ W ,
compact K ⊆ V , and a project H01 (W ) pair vanishes almost everywhere together
with its gradient off K, then the same representatives form a project H01 (V ) pair.
   For extension, each compact test in U is also a compact test in W , and zero
extension turns intrinsic order-one convergence into global W 1 convergence; Theo-
rem 3.16 supplies the ambient H 1 bridge. For localization, choose the Theorem 3.6
cutoff equal to one near K; Theorem 3.20 gives continuity on the ambient compact-
test closure, and the product equals the original pair because both representatives
vanish off K. If K = ∅, the conclusion is the zero class. No arbitrary-domain
identity H01 = He 1 is used.
Isabelle code

 definition mclean_h1_zero_extension_localization_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_h1_zero_extension_localization_claim dimension_type \<longleftrightarrow>

     ((\<forall>(U :: ’n cgu_point set) W u Du.
         U \<noteq> {} \<and> open U \<and> open W \<and> U \<subseteq> W \<and>
         cgu_h1_zero_pair_on U u Du
         \<longrightarrow>
         cgu_h1_zero_pair_on W
           (mclean_zero_extension_on U u)
           (mclean_zero_extension_on U Du)) \<and>
      (\<forall>(W :: ’n cgu_point set) V K u Du.
         W \<noteq> {} \<and> V \<noteq> {} \<and> open W \<and> open V \<and> V \<
      subseteq> W \<and>
         compact K \<and> K \<subseteq> V \<and>
         cgu_h1_zero_pair_on W u Du \<and>
         (AE x in restrict_space lborel W.
           x \<notin> K \<longrightarrow> u x = 0 \<and> Du x = 0)
         \<longrightarrow> cgu_h1_zero_pair_on V u Du))"


English mathematical translation of the Isabelle code
  In every finite dimension, both statements hold.
70                               CĂTĂLIN I. CÂRSTEA

     (1) If U ̸= ∅ and U, W are open with U ⊂ W , then the pointwise zero extension
         to W of every (u, G) ∈ H01 (U ) belongs to H01 (W ).
     (2) If W, V ̸= ∅ are open, V ⊂ W , K ⊂ V is compact, (u, G) ∈ H01 (W ), and

                      x∈/ K =⇒ u(x) = 0 and G(x) = 0
   for almost every x with respect to Lebesgue measure restricted to W , then
(u, G) ∈ H01 (V ).
MCLEAN-HYPERPLANE-OFFSET-SOURCE
Formal identifier: mclean_hyperplane_offset_source_claim
Relationship to source: derived.
Source attribution and locator
   McLean [23], Theorems 3.37–3.38, printed pp. 102–104.
Complete source theorem statement (faithful mathematical restatement)
   At the order used here, the trace is a bounded surjection H 1 → H 1/2 on a Lip-
schitz boundary, has a bounded right inverse, and agrees with ordinary restriction
for smooth functions. By duality, H −1/2 boundary distributions act continuously
on H 1 traces. These statements provide the trace and Fourier-estimate setting for
the flat-hyperplane specialization.
Source attribution and locator
   McLean [23], Lemma 3.39, printed pp. 104–105.
Complete source theorem statement (faithful mathematical restatement)
   A distribution supported on the hyperplane {xn = 0} has a finite representation
by
P tangential     distributions tensored with normal derivatives of the Dirac mass,
           j                                  s
   j vj ⊗Dn δ0 . For membership in ambient H , each occurring order satisfies s+j <
−1/2 and the tangential coefficient has order vj ∈ H s+j+1/2 (Rn−1 ).
Source attribution and locator
   McLean [23], equation (3.33), printed pp. 104–105.
Complete source theorem statement (faithful mathematical restatement)
   For an admissible term,

                    ∥v ⊗ Dnj δ0 ∥2H s (Rn ) = Cs,j ∥v∥2H s+j+1/2 (Rn−1 ) ,
   with the finite positive constant given by the normal-frequency integral. In
particular, at s = −1, j = 0, every v ∈ H −1/2 (Rn−1 ) defines an ambient H −1
source.
Exact derived mathematical result formalized
   Let the ambient dimension be one larger than a positive tangential dimension.
Fix an isometric affine hyperplane chart, a unit normal, a smooth compactly sup-
ported tangential density g, and δ > 0 such that the full swept support cylinder for
offsets 0 ≤ t ≤ δ lies in an open set Ω. Then there are bounded quotient-compatible
sources St and one C ≥ 0 such that, on every smooth test ϕ,
                                   Z
                           St (ϕ) = g(y)ϕ(chart(y) + tν) dy,
                                                     √
   with ∥St ∥H −1 (Ω) ≤ C and ∥St − S0 ∥H −1 (Ω) ≤ C t.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     71

   Translation in the normal variable multiplies the Fourier transform by e−2πiξn t .
In the integral underlying (3.33), bounding |e−2πiξn t − 1| by min(2, C|ξn |t) and
splitting at |ξn | = 1/t gives a squared H −1 bound of order t, hence the displayed
√
  t norm bound. That difference estimate is an elementary consequence of (3.33),
not a numbered theorem. The formal source is an abstract bounded extension on
the H01 quotient; only its action on smooth tests is given pointwise.
Isabelle code

 definition mclean_hyperplane_offset_source_claim ::
   "(’m::finite itself) \<Rightarrow> (’n::finite itself) \<Rightarrow> bool"
 where
   "mclean_hyperplane_offset_source_claim tangential_type ambient_type \<
      longleftrightarrow>
     (1 \<le> CARD(’m) \<and> CARD(’n) = Suc (CARD(’m))) \<longrightarrow>
     (\<forall>(Omega :: ’n cgu_point set)
       (chart :: ’m cgu_point \<Rightarrow> ’n cgu_point) normal g delta.
       open Omega \<and> cgu_test_function_on UNIV g \<and>
       mclean_flat_chart chart normal \<and> 0 < delta \<and>
       mclean_flat_offset_cylinder_inside Omega chart normal g delta
       \<longrightarrow>
       (\<exists>source_at C. 0 \<le> C \<and>
         (\<forall>t. 0 \<le> t \<and> t \<le> delta \<longrightarrow>
           mclean_source_extends_flat_offset_action
             Omega chart normal t g (source_at t) \<and>
           mclean_source_bound_on Omega
             (source_at t) C \<and>
           mclean_source_bound_on Omega
             (\<lambda>u Du.
               source_at t u Du - source_at 0 u Du)
             (C * sqrt t))))"


English mathematical translation of the Isabelle code
   Let m ≥ 1 and n = m + 1. Let Ω ⊂ Rn be open, let g ∈ D(Rm ), let ν ∈ Rn be
a unit vector, and let χ : Rm → Rn satisfy

                ∥χ(x) − χ(y)∥ = ∥x − y∥,       ν · (χ(x) − χ(y)) = 0
  for all x, y. Let δ > 0, and assume

                    {χ(x) + tν : x ∈ {g ̸= 0}, 0 ≤ t ≤ δ} ⊂ Ω.
  Then there exist functionals Ft and a single C ≥ 0 such that, for every 0 ≤ t ≤ δ,
                            Z
              Ft (ϕ, ∇ϕ) =      g(x)ϕ(χ(x) + tν) dx (ϕ ∈ D(Ω)),
                        Rm
                        1
  Ft is bounded linear
                  √ on H0 (Ω) with bound C, and Ft − F0 is bounded linear
there with bound C t. The same family and constant work for all t.
MCLEAN-SMOOTH-GENERATOR-AMBIENT-LIFT
Formal identifier: mclean_smooth_generator_ambient_lift_claim_v2
Relationship to source: derived.
Source attribution and locator
  McLean [23], Theorem 3.6, printed p. 64.
72                              CĂTĂLIN I. CÂRSTEA

Complete source theorem statement (faithful mathematical restatement)
   A closed set contained in a prescribed open neighborhood admits a smooth cutoff
equal to one on the closed set and supported in that neighborhood; for a compact
set in an open set the cutoff can be compactly supported there.
Source attribution and locator
     McLean [23], Theorems 3.37–3.38, printed pp. 102–104.
Complete source theorem statement (faithful mathematical restatement)
   At order one on a Lipschitz domain, the trace H 1 (U ) → H 1/2 (∂U ) is bounded
and surjective, has a continuous right inverse, and agrees with classical boundary
restriction on smooth functions.
Source attribution and locator
     McLean [23], Theorem 3.40, printed pp. 105–106.
Complete source theorem statement (faithful mathematical restatement)
   On a C k−1,1 domain, H0s (U ) = H s (U ) for 0 ≤ s ≤ 1/2; for 1/2 < s ≤ k, the zero-
boundary space is characterized by vanishing of the applicable boundary traces. At
the used specialization s = k = 1, the boundary hypothesis is C 0,1 (Lipschitz), and
H01 (U ) = ker(γ : H 1 (U ) → H 1/2 (∂U )).
Exact derived mathematical result formalized
   Let Ω1 and U ⊆ Ω1 be graph-Lipschitz domains in dimension at least two, let
γ ⊆ Ω1 ∩ ∂U , and fix one globally smooth compactly supported boundary generator
p whose boundary support lies in γ. Then there is a project H01 (Ω1 ) pair (z, Dz)
whose quotient trace on U equals the trace of (p, ∇p).
   Let K be the compact closure of the nonzero boundary support of p. If K ̸= ∅,
choose a generator-dependent cutoff χ ∈ Cc∞ (Ω1 ), χ = 1 near K, and set z = χp.
The difference (1 − χ)p has zero boundary trace on U , so Theorem 3.40 puts it in
H01 (U ). If K = ∅, use the zero ambient pair and apply the same kernel theorem
directly. The witness is chosen after the single generator; no linear, bounded, or
simultaneous lift operator is asserted.
Isabelle code

 definition mclean_smooth_generator_ambient_lift_claim_v2 ::
   "’n::finite itself \<Rightarrow> ’c::finite itself \<Rightarrow>
     ’h::finite itself \<Rightarrow> bool"
 where
   "mclean_smooth_generator_ambient_lift_claim_v2 ambient_type cell_type
       hyperplane_type \<longleftrightarrow>
     2 \<le> CARD(’n) \<longrightarrow>
     (\<forall>(M :: (’n, ’c, ’h) cgu_model)
       (Omega1 :: ’n cgu_point set) U gamma p.
       cgu_graph_lipschitz_domain_v5 Omega1 \<and>
       cgu_graph_lipschitz_domain_v5 U \<and>
       U \<subseteq> Omega1 \<and>
       gamma \<subseteq> Omega1 \<inter> frontier U \<and>
       cgu_boundary_test_on M U gamma p
       \<longrightarrow>
       (\<exists>z Dz.
         cgu_h1_zero_pair_on Omega1 z Dz \<and>
         mclean_same_trace_on U p (cgu_classical_gradient p) z Dz))"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     73

English mathematical translation of the Isabelle code
  Let n ≥ 2. For every geometric record M , every pair of Lipschitz-graph domains
U ⊂ Ω1 , every

                                     γ ⊂ Ω1 ∩ ∂U,
   and every globally smooth compactly supported p which is boundary-supported
in (U, γ) relative to M , there exists (z, Z) ∈ H01 (Ω1 ) such that
                                                   
                                 RU (p, ∇p), (z, Z) .
  In particular, this one-sided relation itself includes that both restricted pairs are
weak H 1 pairs on U .
MCLEAN-SMOOTH-TEST-H1-ZERO
Formal identifier: mclean_smooth_test_h1_zero_claim
Relationship to source: derived.
Source attribution and locator
   McLean [23], test class, derivative convention, and first-order Sobolev definition,
printed pp. 65, 68, and 73–74.
Complete source theorem statement (faithful mathematical restatement)
   D(U ) = Cc∞ (U ). Distributional derivatives use the integration-by-parts sign,
and W21 (U ) consists of square-integrable functions whose first distributional deriva-
tives are square-integrable. A smooth compactly supported function and its classi-
cal first derivatives are square-integrable, and its distributional and classical deriva-
tives agree; Hence every test belongs to W21 (U ) with its classical gradient.
Source attribution and locator
   McLean [23], zero-boundary closure definition, printed p. 77.
Complete source theorem statement (faithful mathematical restatement)
   The zero-boundary Sobolev space is the norm closure of D(U ). In particular
every generator is in that closure, witnessed by the constant sequence.
Source attribution and locator
   McLean [23], Theorem 3.16, printed p. 80.
Complete source theorem statement (faithful mathematical restatement)
   On Rn , the integer-order weak-derivative and Bessel-potential spaces coincide
with equivalent norms. The theorem is used only for the globally smooth compactly
supported representative; no equality of full spaces on an arbitrary open set is
asserted.
Exact derived mathematical result formalized
   For every open U and every globally smooth real ϕ with compact closed nonzero
support contained in U , the pair (ϕ, ∇ϕ) is a project H01 (U ) pair. Smoothness
and compact support give measurability and square integrability; integration by
parts identifies the classical gradient with the weak gradient; the constant sequence
ϕ proves membership in the project’s compact-test closure. McLean states the
definitions for nonempty open sets. When U is empty, the formal support condition
forces ϕ = 0, so the conclusion is an elementary zero-function extension, not a source
attribution.
74                              CĂTĂLIN I. CÂRSTEA

Isabelle code
 definition mclean_smooth_test_h1_zero_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_smooth_test_h1_zero_claim dimension_type \<longleftrightarrow>
     (\<forall>(U :: ’n cgu_point set) phi.
       open U \<longrightarrow>
       cgu_test_function_on U phi \<longrightarrow>
       cgu_h1_zero_pair_on U phi (cgu_classical_gradient phi))"


English mathematical translation of the Isabelle code
   In every finite dimension, for every U and every ϕ, if U is open, then if ϕ ∈ D(U ),
the pair (ϕ, ∇ϕ) lies in the zero-boundary closure:

                 U open =⇒ ϕ ∈ D(U ) =⇒ (ϕ, ∇ϕ) ∈ H01 (U ) .
                                                                

   The two implications are right-associated; for a non-open U , the outer implica-
tion is true without testing the inner one.
MCLEAN-TRACE-DIRICHLET-GREEN
Formal identifier: mclean_trace_dirichlet_green_claim_v3
Relationship to source: derived.
Source attribution and locator
    McLean [23], Definition 3.28, printed pp. 89–90.
Complete source theorem statement (faithful mathematical restatement)
    The relevant C 0,1 geometry is a domain whose compact boundary is locally a
Lipschitz graph after a rigid change of Cartesian coordinates. The project uses the
bounded connected subclass.
Source attribution and locator
    McLean [23], Theorem 3.37, printed p. 102.
Complete source theorem statement (faithful mathematical restatement)
    On a Lipschitz domain, at order one the trace γ : H 1 (U ) → H 1/2 (∂U ) is bounded
and surjective and has a continuous right inverse. Consequently the boundary space
is isomorphic, with equivalent norm, to the quotient of H 1 (U ) by the trace kernel.
Source attribution and locator
    McLean [23], Theorem 3.40, printed pp. 105–106.
Complete source theorem statement (faithful mathematical restatement)
    On a C k−1,1 domain the zero-boundary space equals all of H s for 0 ≤ s ≤ 1/2,
while for 1/2 < s ≤ k it is characterized by vanishing of the relevant boundary
traces. At s = k = 1, used here, the domain is Lipschitz C 0,1 and H01 (U ) = ker γ.
Source attribution and locator
    McLean [23], Lemma 4.3, printed pp. 116–117.
Complete source theorem statement (faithful mathematical restatement)
    Once the right-hand side of a weak elliptic equation is fixed, a weak solution has
a unique conormal boundary distribution in H −1/2 (∂U ) satisfying the variational
Green formula. Its norm is bounded in terms of the solution and source norms; the
proof uses a continuous trace right inverse.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     75

Source attribution and locator
    McLean [23], Theorem 4.4, printed p. 118.
Complete source theorem statement (faithful mathematical restatement)
    The first Green identity expresses the variational form as the interior source
pairing plus the conormal/trace boundary pairing. Applying it in both orders
gives the second Green identity. For a homogeneous solution, its energy against an
arbitrary H 1 lift therefore depends only on the lift’s boundary trace.
Source attribution and locator
    McLean [23], Theorem 4.10, printed pp. 128–130, with the pure Dirichlet spe-
cialization on printed p. 131.
Complete source theorem statement (faithful mathematical restatement)
    The mixed variational boundary problem on a bounded Lipschitz domain sat-
isfies a Fredholm alternative: in the trivial-kernel branch every admissible datum
has a unique solution; otherwise solvability is subject to the stated orthogonality
conditions against the adjoint homogeneous kernel. For pure Dirichlet data the
energy space is V = H01 (U ) and V ∗ = H −1 (U ), so arbitrary bounded dual sources
are allowed. The formal strict-coercivity premise forces the trivial-kernel branch.
Source attribution and locator
    McLean [23], equations (4.35)–(4.38), printed p. 145.
Complete source theorem statement (faithful mathematical restatement)
    The solution operators furnished by the variational problem are bounded, and
the Steklov–Poincaré/Dirichlet-to-Neumann operator obtained from the conormal
pairing is a bounded operator between the trace space and its dual.
Exact derived mathematical result formalized
    Let U be a bounded graph-Lipschitz domain in dimension at least two, and let a
define an integrable bilinear energy form which is bounded on project H 1 (U ) pairs
and strictly coercive on project H01 (U ). Then:
     (1) every project quotient trace has a weak homogeneous Dirichlet solution,
          unique modulo zero H 1 distance;
     (2) one constant bounds the homogeneous solution’s energy pairing by the
          product of the two quotient trace norms, so the pairing is a bounded DN
          form; and
     (3) one constant gives, for every bounded real-linear source on H01 (U ), a zero-
          boundary Green solution with an H 1 -norm estimate proportional to the
          source bound, unique modulo zero distance.
    The project trace is the quotient H 1 (U )/H01 (U ), with norm the infimum of the
norms of its lifts. Theorems 3.37 and 3.40 identify this with the source trace space;
Lemma 4.3 and Theorem 4.4 make homogeneous energy depend only on quotient
traces; strict coercivity places Theorem 4.10 in its unique pure-Dirichlet branch and
yields the solution bounds. The graph-domain premise is a conservative bounded
subclass of McLean’s C 0,1 geometry.
Isabelle code
 definition mclean_trace_dirichlet_green_claim_v3 ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"
76                               CĂTĂLIN I. CÂRSTEA

 where
   "mclean_trace_dirichlet_green_claim_v3 U a \<longleftrightarrow>
     (2 \<le> CARD(’n) \<and> cgu_graph_lipschitz_domain_v5 U \<and>
       mclean_variational_form_on U a)
     \<longrightarrow>
     ((\<forall>f Df. cgu_h1_pair_on U f Df \<longrightarrow>
       (\<exists>u Du. mclean_dirichlet_solution_for U a f Df u Du \<and>
         (\<forall>v Dv. mclean_dirichlet_solution_for U a f Df v Dv
           \<longrightarrow> cgu_h1_squared_distance U u Du v Dv = 0))) \<and>
      (\<exists>C. 0 \<le> C \<and>
       (\<forall>f Df u Du h Dh.
         mclean_dirichlet_solution_for U a f Df u Du \<and>
         cgu_h1_pair_on U h Dh
         \<longrightarrow>
         mclean_energy_integrable U a Du Dh \<and>
         abs (mclean_energy U a Du Dh) \<le>
           C * mclean_trace_norm U f Df * mclean_trace_norm U h Dh)) \<and>
      (\<exists>C. 0 \<le> C \<and>
       (\<forall>F K. mclean_source_bound_on U F K \<longrightarrow>
         (\<exists>u Du. mclean_green_solution_for U a F u Du \<and>
           mclean_h1_norm U u Du \<le> C * K \<and>
           (\<forall>v Dv. mclean_green_solution_for U a F v Dv
             \<longrightarrow> cgu_h1_squared_distance U u Du v Dv = 0)))))"

English mathematical translation of the Isabelle code
   Let n ≥ 2, let U be a Lipschitz-graph domain, and suppose BU,a is stable. Then
all three conclusions hold.
     (1) For every (f, F ) ∈ H1 (U ), there is a variational Dirichlet solution (u, G),
         and every other such solution (v, H) satisfies

                                d2U ((u, G), (v, H)) = 0.
      (2) There exists C1 ≥ 0 such that for every Dirichlet solution (u, G) with
          boundary representative (f, F ), and every (h, H) ∈ H1 (U ), the energy
          density aG · H is integrable and

                         |BU,a (G, H)| ≤ C1 qU (f, F ) qU (h, H).
      (3) There exists an independently quantified C2 ≥ 0 such that every functional
          F bounded linear with bound K has a source solution (u, G) with

                                  ∥(u, G)∥U ≤ C2 K,
     and every other source solution is at squared pair-distance zero from it.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     77

                Appendix B. Independent back-translation B

Definitions
cgu_point
Isabelle code
 type_synonym ’n cgu_point = "real ^ ’n"


English mathematical translation
Mathematical role: Euclidean coordinate space VI
   For every type ’n, ’n cgu point is exactly the vector type real ^ ’n. There
are no term arguments, quantifiers, hypotheses, or conclusion.
cgu_monomial
Isabelle code
 type_synonym ’n cgu_monomial = "’n \<Rightarrow>\<^sub>0 nat"


English mathematical translation
Mathematical role: finitely supported multi-index type
   For every type ’n, ’n cgu monomial is exactly the finite-support mapping type
’n \<Rightarrow>\<^sub>0 nat. There are no term arguments or logical condi-
tions.
cgu_polynomial
Isabelle code
 type_synonym ’n cgu_polynomial = "’n cgu_monomial \<Rightarrow>\<^sub>0 real"


English mathematical translation
Mathematical role: finitely supported scalar polynomial-representation type
   For every type ’n, ’n cgu polynomial is exactly the finite-support mapping
type from ’n cgu monomial to real. There are no term arguments or logical
conditions.
cgu_matrix_polynomial
Isabelle code
 type_synonym ’n cgu_matrix_polynomial = "’n cgu_polynomial ^ ’n ^ ’n"


English mathematical translation
Mathematical role: polynomial-matrix representation type
  For every type ’n, ’n cgu matrix polynomial is exactly ’n cgu polynomial
^ ’n ^ ’n. There are no term arguments or logical conditions.
cgu_monomial_total_degree
Isabelle code
78                             CĂTĂLIN I. CÂRSTEA


 definition cgu_monomial_total_degree :: "’n cgu_monomial \<Rightarrow> nat"
 where
   "cgu_monomial_total_degree m =
     (\<Sum>i\<in>Poly_Mapping.keys m. Poly_Mapping.lookup m i)"


English mathematical translation
Mathematical role: total size of a multi-index
  Typed arguments/result: m :: ’n cgu monomial; result nat. cgu monomial
total degree m equals the finite sum, over every i in Poly Mapping.keys m, of
Poly Mapping.lookup m i. There are no hypotheses.
cgu_poly_degree_le
Isabelle code
 definition cgu_poly_degree_le :: "nat \<Rightarrow> ’n cgu_polynomial \<Rightarrow>
       bool"
 where
   "cgu_poly_degree_le d p \<longleftrightarrow>
     (\<forall>m\<in>Poly_Mapping.keys p. cgu_monomial_total_degree m \<le> d)"


English mathematical translation
Mathematical role: stored scalar degree predicate
  Typed arguments/result: d :: nat, p :: ’n cgu polynomial; result bool.
cgu poly degree le d p holds exactly when, for every m restricted by m \<in>
Poly Mapping.keys p, cgu monomial total degree m \<le> d.
cgu_monomial_eval
Isabelle code
 definition cgu_monomial_eval ::
   "’n cgu_monomial \<Rightarrow> ’n::finite cgu_point \<Rightarrow> real"
 where
   "cgu_monomial_eval m x =
     (\<Prod>i\<in>Poly_Mapping.keys m. x $ i ^ Poly_Mapping.lookup m i)"


English mathematical translation
Mathematical role: monomial xα
   Typed arguments/result: m :: ’n cgu monomial, x :: ’n cgu point, with
’n::finite; result real. cgu monomial eval m x equals the finite product, over
every i \<in> Poly Mapping.keys m, of (x $ i) raised to Poly Mapping.lookup
m i. There are no hypotheses.
cgu_poly_eval
Isabelle code
 definition cgu_poly_eval ::
   "’n cgu_polynomial \<Rightarrow> ’n::finite cgu_point \<Rightarrow> real"
 where
   "cgu_poly_eval p x =
     (\<Sum>m\<in>Poly_Mapping.keys p.
       Poly_Mapping.lookup p m * cgu_monomial_eval m x)"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     79

English mathematical translation
Mathematical role: scalar polynomial evaluation pb(x)
   Typed arguments/result: p :: ’n cgu polynomial, x :: ’n cgu point, with
’n::finite; result real. It equals the finite sum over m \<in> Poly Mapping.
keys p of Poly Mapping.lookup p m * cgu monomial eval m x.
cgu_matrix_poly_eval
Isabelle code
 definition cgu_matrix_poly_eval ::
   "’n::finite cgu_matrix_polynomial \<Rightarrow> ’n cgu_point \<Rightarrow>
     real ^ ’n ^ ’n"
 where
   "cgu_matrix_poly_eval P x = (\<chi> i j. cgu_poly_eval (P $ i $ j) x)"

English mathematical translation
Mathematical role: matrix evaluation Pb(x)
   Typed arguments/result: P :: ’n cgu matrix polynomial, x :: ’n cgu
point, with ’n::finite; result real ^ ’n ^ ’n. The result is the indexed vec-
tor/matrix \<chi> i j. cgu poly eval (P $ i $ j) x; thus every indices i,j
:: ’n select that entry.
cgu_matrix_poly_degree_le
Isabelle code
 definition cgu_matrix_poly_degree_le ::
   "nat \<Rightarrow> ’n::finite cgu_matrix_polynomial \<Rightarrow> bool"
 where
   "cgu_matrix_poly_degree_le d P \<longleftrightarrow>
     (\<forall>i j. cgu_poly_degree_le d (P $ i $ j))"

English mathematical translation
Mathematical role: componentwise coefficient-representation degree predicate
   Typed arguments/result: d :: nat, P :: ’n cgu matrix polynomial, with
’n::finite; result bool. It holds exactly when for every unrestricted i,j :: ’n,
cgu poly degree le d (P $ i $ j) holds.
cgu_symmetric_matrix_polynomial
Isabelle code
 definition cgu_symmetric_matrix_polynomial ::
   "’n::finite cgu_matrix_polynomial \<Rightarrow> bool"
 where
   "cgu_symmetric_matrix_polynomial P \<longleftrightarrow>
     (\<forall>i j. P $ i $ j = P $ j $ i)"

English mathematical translation
Mathematical role: symbolic matrix symmetry
   Typed argument/result: P :: ’n cgu matrix polynomial, with ’n::finite;
result bool. It holds exactly when for all i,j :: ’n, P $ i $ j = P $ j $ i.
cgu_matrix_bilinear
80                             CĂTĂLIN I. CÂRSTEA

Isabelle code
 definition cgu_matrix_bilinear ::
   "(real ^ ’n::finite ^ ’n) \<Rightarrow> real ^ ’n \<Rightarrow>
     real ^ ’n \<Rightarrow> real"
 where
   "cgu_matrix_bilinear A x y = inner x (A *v y)"


English mathematical translation
Mathematical role: bilinear expression bA
   Typed arguments/result: A :: real ^ ’n ^ ’n, x,y :: real ^ ’n, with
’n::finite; result real. cgu matrix bilinear A x y = inner x (A *v y).
cgu_symmetric_positive_definite_matrix
Isabelle code
 definition cgu_symmetric_positive_definite_matrix ::
   "(real ^ ’n::finite ^ ’n) \<Rightarrow> bool"
 where
   "cgu_symmetric_positive_definite_matrix A \<longleftrightarrow>
     transpose A = A \<and>
     (\<forall>x. x \<noteq> 0 \<longrightarrow> 0 < cgu_matrix_bilinear A x x)"


English mathematical translation
Mathematical role: symmetric positive definiteness
   Typed argument/result: A :: real ^ ’n ^ ’n, with ’n::finite; result bool.
It holds exactly when both transpose A = A and, for every x :: real ^ ’n, the
hypothesis x \<noteq> 0 implies the conclusion 0 < cgu matrix bilinear A x
x.
cgu_uniformly_positive_definite_on
Isabelle code
 definition cgu_uniformly_positive_definite_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_matrix_polynomial \<Rightarrow>
      bool"
 where
   "cgu_uniformly_positive_definite_on D P \<longleftrightarrow>
     (\<exists>k>0. \<forall>x\<in>D. \<forall>xi.
       k * norm xi ^ 2 \<le>
         cgu_matrix_bilinear (cgu_matrix_poly_eval P x) xi xi)"


English mathematical translation
Mathematical role: uniform ellipticity on a set
  Typed arguments/result:       D :: ’n cgu point set, P :: ’n cgu matrix
polynomial, with ’n::finite; result bool. It holds exactly when there exists k ::
real restricted by k > 0 such that for every x \<in> D and every unrestricted xi
:: ’n cgu point, k * norm xi ^ 2 \<le> cgu matrix bilinear (cgu matrix
poly eval P x) xi xi.
cgu_model
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     81


 record (’n, ’c, ’h) cgu_model =
   cgu_domain :: "’n cgu_point set"
   cgu_measured :: "’n cgu_point set"
   cgu_cell :: "’c \<Rightarrow> ’n cgu_point set"
   cgu_degree :: "’c \<Rightarrow> nat"
   cgu_order :: "nat \<Rightarrow> ’c"
   cgu_faces :: "’c \<Rightarrow> ’h set"
   cgu_normal :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point"
   cgu_offset :: "’c \<Rightarrow> ’h \<Rightarrow> real"
   cgu_face_patch :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point set"
   cgu_witness_faces :: "’c \<Rightarrow> ’h \<Rightarrow> ’h set"
   cgu_triple_region :: "’c \<Rightarrow> ’h \<Rightarrow> ’h \<Rightarrow> ’h \<
      Rightarrow>
     ’n cgu_point set"
   cgu_step_interface_pieces :: "’c \<Rightarrow> ’h set"
   cgu_step_interface_patch :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point set"
   cgu_step_interface_normal :: "’c \<Rightarrow> ’h \<Rightarrow> ’n cgu_point"
   cgu_step_interface_offset :: "’c \<Rightarrow> ’h \<Rightarrow> real"
   cgu_step_outer_patch :: "’c \<Rightarrow> ’n cgu_point set"
   cgu_step_adjacent_cell :: "’c \<Rightarrow> ’c"
   cgu_step_center :: "’c \<Rightarrow> ’n cgu_point"
   cgu_step_interior_normal :: "’c \<Rightarrow> ’n cgu_point"
   cgu_step_radius :: "’c \<Rightarrow> real"


English mathematical translation
Mathematical role: geometric datum M , with twenty fields
   Type parameters: (’n,’c,’h). The record has exactly these typed se-
lectors: cgu domain, cgu measured :: ’n cgu point set; cgu cell :: ’c
\<Rightarrow> ’n cgu point set;        cgu degree :: ’c \<Rightarrow> nat;
cgu order :: nat \<Rightarrow> ’c;           cgu faces, cgu step interface
pieces :: ’c \<Rightarrow> ’h set;          cgu normal, cgu step interface
normal :: ’c \<Rightarrow> ’h \<Rightarrow> ’n cgu point; cgu offset,
cgu step interface offset :: ’c \<Rightarrow> ’h \<Rightarrow> real;
cgu face patch, cgu step interface patch :: ’c \<Rightarrow> ’h
\<Rightarrow> ’n cgu point set; cgu witness faces :: ’c \<Rightarrow>
’h \<Rightarrow> ’h set;         cgu triple region :: ’c \<Rightarrow> ’h
\<Rightarrow> ’h \<Rightarrow> ’h \<Rightarrow> ’n cgu point set;
cgu step outer patch :: ’c \<Rightarrow> ’n cgu point set;         cgu step
adjacent cell :: ’c \<Rightarrow> ’c;             cgu step center, cgu step
interior normal :: ’c \<Rightarrow> ’n cgu point; and cgu step radius
:: ’c \<Rightarrow> real. This is a record composition, not a proposition.
cgu_piecewise_polynomial_class
Isabelle code

 definition cgu_piecewise_polynomial_class ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> bool"
 where
   "cgu_piecewise_polynomial_class M P \<longleftrightarrow>
     (\<forall>c.
       cgu_matrix_poly_degree_le (cgu_degree M c) (P c) \<and>
       cgu_symmetric_matrix_polynomial (P c) \<and>
82                             CĂTĂLIN I. CÂRSTEA

       cgu_uniformly_positive_definite_on (cgu_cell M c) (P c))"


English mathematical translation
Mathematical role: admissible cellwise coefficient family
   Typed     arguments/result:         M :: (’n,’c,’h) cgu model,       P :: ’c
\<Rightarrow> ’n cgu matrix polynomial, with ’n,’c::finite; result bool.
It holds exactly when, for every c :: ’c, all three conjuncts hold: cgu matrix
poly degree le (cgu degree M c) (P c), cgu symmetric matrix polynomial
(P c), and cgu uniformly positive definite on (cgu cell M c) (P c).
cgu_affine_hyperplane
Isabelle code
 definition cgu_affine_hyperplane ::
   "’n::finite cgu_point \<Rightarrow> real \<Rightarrow> ’n cgu_point set"
 where
   "cgu_affine_hyperplane normal offset = {x. inner normal x = offset}"


English mathematical translation
Mathematical role: affine hyperplane H(ν, b)
   Typed arguments/result: normal :: ’n cgu point, offset :: real, with
’n::finite; result ’n cgu point set. It is {x. inner normal x = offset},
with x :: ’n cgu point.
cgu_coordinate_hyperplane_projection_v5
Isabelle code
 definition cgu_coordinate_hyperplane_projection_v5 ::
   "’i::finite \<Rightarrow> ’i cgu_point \<Rightarrow> ’i cgu_point"
 where
   "cgu_coordinate_hyperplane_projection_v5 i y =
     (\<chi> j. if j = i then 0 else y $ j)"


English mathematical translation
Mathematical role: coordinate-deletion map πi
   Typed arguments/result: i :: ’i, y :: ’i cgu point, with ’i::finite; re-
sult ’i cgu point. The result has coordinate j :: ’i equal to 0 if j=i, and
otherwise equal to y $ j.
cgu_local_lipschitz_boundary_at
Isabelle code
 definition cgu_local_lipschitz_boundary_at ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> bool"
 where
   "cgu_local_lipschitz_boundary_at D x \<longleftrightarrow>
     (\<exists>(U :: ’n cgu_point set)
        (f :: ’n cgu_point \<Rightarrow> ’n cgu_point)
        (g :: ’n cgu_point \<Rightarrow> ’n cgu_point) (i :: ’n) L M.
       open U \<and> x \<in> U \<and> 0 < L \<and> 0 < M \<and>
       homeomorphism U (f ‘ U) f g \<and>
       lipschitz_on L U f \<and> lipschitz_on M (f ‘ U) g \<and>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     83

      f ‘ (D \<inter> U) = (f ‘ U) \<inter> {y. 0 < y $ i})"


English mathematical translation
Mathematical role: bi-Lipschitz half-space point
   Typed arguments/result: D :: ’n cgu point set, x :: ’n cgu point, with
’n::finite; result bool. It holds exactly when there exist U :: ’n cgu point
set, f,g :: ’n cgu point \<Rightarrow> ’n cgu point, i :: ’n, and L,M ::
real such that: open U; x \<in> U; 0<L; 0<M; homeomorphism U (f ‘ U) f g;
lipschitz on L U f; lipschitz on M (f ‘ U) g; and f ‘ (D \<inter> U) =
(f ‘ U) \<inter> {y. 0 < y $ i}.
cgu_lipschitz_domain
Isabelle code

 definition cgu_lipschitz_domain ::
   "’n::finite cgu_point set \<Rightarrow> bool"
 where
   "cgu_lipschitz_domain D \<longleftrightarrow>
     D \<noteq> {} \<and> open D \<and> connected D \<and> bounded D \<and>
     (\<forall>x\<in>frontier D. cgu_local_lipschitz_boundary_at D x)"


English mathematical translation
Mathematical role: admissible bounded domain
   Typed argument/result: D :: ’n cgu point set, with ’n::finite; result
bool. It holds exactly when D \<noteq> {}, open D, connected D, and bounded
D, and for every x \<in> frontier D, cgu local lipschitz boundary at D x.
cgu_rigid_motion_v5
Isabelle code

 definition cgu_rigid_motion_v5 ::
   "(’n::finite cgu_point \<Rightarrow> ’n cgu_point) \<Rightarrow> bool"
 where
   "cgu_rigid_motion_v5 R \<longleftrightarrow>
     (\<exists>A b.
       linear A \<and>
       surj A \<and>
       (\<forall>u v. inner (A u) (A v) = inner u v) \<and>
       R = (\<lambda>x. A x + b))"


English mathematical translation
Mathematical role: rigid motion
   Typed argument/result: R :: ’n cgu point \<Rightarrow> ’n cgu point,
with ’n::finite; result bool. It holds exactly when there exist A :: ’n cgu
point \<Rightarrow> ’n cgu point and b :: ’n cgu point such that linear
A, surj A, for all u,v :: ’n cgu point, inner (A u) (A v) = inner u v, and
R = (\<lambda>x. A x + b).
cgu_local_graph_boundary_at_v5
Isabelle code
84                             CĂTĂLIN I. CÂRSTEA


 definition cgu_local_graph_boundary_at_v5 ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> bool"
 where
   "cgu_local_graph_boundary_at_v5 D x \<longleftrightarrow>
     (\<exists>U R i zeta L.
       open U \<and>
       x \<in> U \<and>
       cgu_rigid_motion_v5 R \<and>
       0 < L \<and>
       lipschitz_on L UNIV zeta \<and>
       R ‘ (D \<inter> U) =
         R ‘ U \<inter>
           {y. y $ i < zeta (cgu_coordinate_hyperplane_projection_v5 i y)} \<and>
       R ‘ (frontier D \<inter> U) =
         R ‘ U \<inter>
           {y. y $ i = zeta (cgu_coordinate_hyperplane_projection_v5 i y)})"


English mathematical translation
Mathematical role: Lipschitz graph point
   Typed arguments/result:       D :: ’n cgu point set, x :: ’n cgu point,
with ’n::finite; result bool. It holds exactly when there exist U :: ’n
cgu point set, R :: ’n cgu point \<Rightarrow> ’n cgu point, i :: ’n,
zeta :: ’n cgu point \<Rightarrow> real, and L :: real such that open
U, x \<in> U, cgu rigid motion v5 R, 0<L, lipschitz on L UNIV zeta, R
‘ (D \<inter> U) = R ‘ U \<inter> {y. y $ i < zeta (cgu coordinate
hyperplane projection v5 i y)}, and R ‘ (frontier D \<inter> U) = R ‘
U \<inter> {y. y $ i = zeta (cgu coordinate hyperplane projection v5
i y)}.
cgu_graph_lipschitz_domain_v5
Isabelle code

 definition cgu_graph_lipschitz_domain_v5 ::
   "’n::finite cgu_point set \<Rightarrow> bool"
 where
   "cgu_graph_lipschitz_domain_v5 D \<longleftrightarrow>
     cgu_lipschitz_domain D \<and>
     (\<forall>x\<in>frontier D. cgu_local_graph_boundary_at_v5 D x)"


English mathematical translation
Mathematical role: Lipschitz admissible domain
  Typed argument/result: D :: ’n cgu point set, with ’n::finite; result
bool. It holds exactly when cgu lipschitz domain D and, for every x \<in>
frontier D, cgu local graph boundary at v5 D x.
cgu_locally_flat_boundary_point
Isabelle code

 definition cgu_locally_flat_boundary_point ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> bool"
 where
   "cgu_locally_flat_boundary_point D x \<longleftrightarrow>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     85

     x \<in> frontier D \<and>
     (\<exists>normal offset U.
       normal \<noteq> 0 \<and> open U \<and> x \<in> U \<and>
       U \<inter> frontier D =
         U \<inter> cgu_affine_hyperplane normal offset)"


English mathematical translation
Mathematical role: flat frontier point
    Typed arguments/result: D :: ’n cgu point set, x :: ’n cgu point, with
’n::finite; result bool. It holds exactly when x \<in> frontier D and there ex-
ist normal :: ’n cgu point, offset :: real, and U :: ’n cgu point set such
that normal \<noteq> 0, open U, x \<in> U, and U \<inter> frontier D = U
\<inter> cgu affine hyperplane normal offset.
cgu_relative_frontier
Isabelle code

 definition cgu_relative_frontier ::
   "’a::topological_space set \<Rightarrow> ’a set \<Rightarrow> ’a set"
 where
   "cgu_relative_frontier X A = closure A \<inter> closure (X - A)"


English mathematical translation
Mathematical role: ambient two-sided edge edgeX (A)
   Typed arguments/result: X,A :: ’a set, with ’a::topological space; re-
sult ’a set. cgu relative frontier X A = closure A \<inter> closure (X
- A).
cgu_subdivision_edge_corner_set
Isabelle code

 definition cgu_subdivision_edge_corner_set ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> ’n cgu_point set"
 where
   "cgu_subdivision_edge_corner_set M =
     (\<Union>c.
       let X = frontier (cgu_cell M c);
           F = {x\<in>X. cgu_locally_flat_boundary_point (cgu_cell M c) x}
       in cgu_relative_frontier X F)"


English mathematical translation
Mathematical role: transition set ΣM
   Typed argument/result: M :: (’n,’c,’h) cgu model, with ’n,’c::finite;
result ’n cgu point set.      It is the union over every c :: ’c of the fol-
lowing: let X = frontier (cgu cell M c) and F = {x \<in> X. cgu locally
flat boundary point (cgu cell M c) x}; then take cgu relative frontier X
F.
cgu_graph_subdivision_core_v7
Isabelle code
86                             CĂTĂLIN I. CÂRSTEA


 definition cgu_graph_subdivision_core_v7 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow> bool"
 where
   "cgu_graph_subdivision_core_v7 M \<longleftrightarrow>
     cgu_lipschitz_domain (cgu_domain M) \<and>
     cgu_measured M \<noteq> {} \<and>
     openin (top_of_set (frontier (cgu_domain M))) (cgu_measured M) \<and>
     cgu_measured M \<subseteq> frontier (cgu_domain M) \<and>
     (\<forall>c. cgu_cell M c \<subseteq> cgu_domain M \<and>
       cgu_lipschitz_domain (cgu_cell M c)) \<and>
     (\<forall>c d. c \<noteq> d \<longrightarrow> cgu_cell M c \<inter> cgu_cell M
       d = {}) \<and>
     closure (cgu_domain M) = (\<Union>c. closure (cgu_cell M c)) \<and>
     cgu_graph_lipschitz_domain_v5 (cgu_domain M) \<and>
     (\<forall>c. cgu_graph_lipschitz_domain_v5 (cgu_cell M c))"


English mathematical translation
Mathematical role: admissible subdivision
   Typed      argument/result:        M :: (’n,’c,’h) cgu model,     with
’n,’c,’h::finite; result bool.     It holds exactly when: cgu lipschitz
domain (cgu domain M); cgu measured M \<noteq> {}; cgu measured M is
open in top of set (frontier (cgu domain M)); cgu measured M \<subseteq>
frontier (cgu domain M); for every c :: ’c, cgu cell M c \<subseteq> cgu
domain M and cgu lipschitz domain (cgu cell M c); for every c,d :: ’c,
the hypothesis c \<noteq> d implies cgu cell M c \<inter> cgu cell M d
= {};     closure (cgu domain M) = (\<Union>c. closure (cgu cell M c));
cgu graph lipschitz domain v5 (cgu domain M); and for every c :: ’c, cgu
graph lipschitz domain v5 (cgu cell M c).
cgu_graph_boundary_regularities_imply_lipschitz_domain
Isabelle code

 theorem cgu_graph_boundary_regularities_imply_lipschitz_domain:
   shows \<open>D \<noteq> {} \<and> open D \<and> connected D \<and> bounded D \<
      and>
     (\<forall>x\<in>frontier D. cgu_local_graph_boundary_at_v5 D x)
     \<longrightarrow> cgu_lipschitz_domain D\<close>


English mathematical translation
Mathematical role: Lipschitz-graph boundary-chart lemma
  Implicit typed variable: D :: ’n cgu point set with ’n::finite as forced by
cgu local graph boundary at v5/cgu lipschitz domain. There are no separate
meta-level assumes; the single shown object-level proposition is: the conjunction D
\<noteq> {}, open D, connected D, bounded D, and \<forall>x\<in>frontier
D. cgu local graph boundary at v5 D x implies the conclusion cgu lipschitz
domain D. The quantifier over x is restricted to frontier D; D and its type are
implicit schematic parameters of the theorem.
cgu_share_flat_face_in
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     87


 definition cgu_share_flat_face_in ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_point set \<Rightarrow> bool"
 where
   "cgu_share_flat_face_in G E F \<longleftrightarrow>
     (\<exists>normal offset U.
       normal \<noteq> 0 \<and> open U \<and>
       U \<inter> cgu_affine_hyperplane normal offset \<noteq> {} \<and>
       U \<inter> cgu_affine_hyperplane normal offset
         \<subseteq> G \<inter> frontier E \<inter> frontier F)"


English mathematical translation
Mathematical role: planar adjacency E ∼G F
   Typed arguments/result: G,E,F :: ’n cgu point set, with ’n::finite;
result bool. It holds exactly when there exist normal :: ’n cgu point, offset
:: real, and U :: ’n cgu point set such that normal \<noteq> 0, open
U, U \<inter> cgu affine hyperplane normal offset \<noteq> {}, and U
\<inter> cgu affine hyperplane normal offset \<subseteq> G \<inter>
frontier E \<inter> frontier F.
cgu_linearly_independent3
Isabelle code
 definition cgu_linearly_independent3 ::
   "real ^ ’n::finite \<Rightarrow> real ^ ’n \<Rightarrow> real ^ ’n \<Rightarrow>
       bool"
 where
   "cgu_linearly_independent3 a b c \<longleftrightarrow>
     (\<forall>x y z::real.
       x *\<^sub>R a + y *\<^sub>R b + z *\<^sub>R c = 0
       \<longrightarrow> x = 0 \<and> y = 0 \<and> z = 0)"


English mathematical translation
Mathematical role: independence of three normals
   Typed arguments/result: a,b,c :: real ^ ’n, with ’n::finite; result bool.
It holds exactly when, for every x,y,z :: real, the hypothesis x *\<^sub>R
a + y *\<^sub>R b + z *\<^sub>R c = 0 implies the three-part conclusion x=0
\<and> y=0 \<and> z=0.
cgu_n_generic_on
Isabelle code
 definition cgu_n_generic_on ::
   "nat \<Rightarrow> ’h::finite set \<Rightarrow>
     (’h \<Rightarrow> real ^ ’n::finite) \<Rightarrow> (’h \<Rightarrow> real) \<
      Rightarrow>
     (’h \<Rightarrow> ’h set) \<Rightarrow> bool"
 where
   "cgu_n_generic_on N I normal offset J \<longleftrightarrow>
     inj_on (\<lambda>i. cgu_affine_hyperplane (normal i) (offset i)) I \<and>
     (\<forall>i\<in>I.
       J i \<subseteq> I - {i} \<and> card (J i) = N + 2 \<and>
       (\<forall>j\<in>J i. \<forall>k\<in>J i. j \<noteq> k \<longrightarrow>
88                             CĂTĂLIN I. CÂRSTEA

         cgu_linearly_independent3 (normal i) (normal j) (normal k) \<and>
         aff_dim
           (cgu_affine_hyperplane (normal i) (offset i) \<inter>
            cgu_affine_hyperplane (normal j) (offset j) \<inter>
            cgu_affine_hyperplane (normal k) (offset k))
         = int (CARD(’n)) - 3) \<and>
       (\<forall>j\<in>J i. \<forall>k\<in>J i. \<forall>l\<in>J i.
         j \<noteq> k \<and> l \<noteq> j \<and> l \<noteq> k \<longrightarrow>
         \<not> cgu_affine_hyperplane (normal i) (offset i) \<inter>
              cgu_affine_hyperplane (normal j) (offset j) \<inter>
              cgu_affine_hyperplane (normal k) (offset k)
            \<subseteq> cgu_affine_hyperplane (normal l) (offset l)))"


English mathematical translation
Mathematical role: N -hyperplane configuration
   Typed arguments/result:            N :: nat,   I :: ’h set,    normal :: ’h
\<Rightarrow> real ^ ’n,         offset :: ’h \<Rightarrow> real,       J :: ’h
\<Rightarrow> ’h set, with ’h,’n::finite; result bool. It holds exactly
when the map i \<mapsto> cgu affine hyperplane (normal i) (offset i)
is injective on I, and for every i \<in> I: (a) J i \<subseteq> I - {i} and
card (J i) = N+2; (b) for every j \<in> J i and k \<in> J i, if j \<noteq>
k, then cgu linearly independent3 (normal i) (normal j) (normal k) and
the affine dimension of the intersection of the three corresponding cgu affine
hyperplane sets is int (CARD(’n)) - 3; and (c) for every j,k,l \<in> J i, if j
\<noteq> k, l \<noteq> j, and l \<noteq> k, then the intersection of the sets
for i,j,k is not a subset of the set for l.
cgu_triple_region_geometry
Isabelle code
 definition cgu_triple_region_geometry ::
   "’n::finite cgu_point set \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> ’n cgu_point \<Rightarrow> real
      \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> bool"
 where
   "cgu_triple_region_geometry W ni oi nj oj nk ok \<longleftrightarrow>
     W \<noteq> {} \<and>
     openin
       (top_of_set
         (cgu_affine_hyperplane ni oi \<inter>
          cgu_affine_hyperplane nj oj \<inter>
          cgu_affine_hyperplane nk ok)) W \<and>
     W \<subseteq>
       cgu_affine_hyperplane ni oi \<inter>
       cgu_affine_hyperplane nj oj \<inter>
       cgu_affine_hyperplane nk ok"


English mathematical translation
Mathematical role: relatively open triple window
  Typed arguments/result: W :: ’n cgu point set; ni,nj,nk :: ’n cgu
point; oi,oj,ok :: real; with ’n::finite; result bool. It holds exactly when
W \<noteq> {}, W is open in the subspace on cgu affine hyperplane ni oi
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     89

\<inter> cgu affine hyperplane nj oj \<inter> cgu affine hyperplane
nk ok, and W is a subset of that same intersection.
cgu_polynomial_positive_on
Isabelle code

 definition cgu_polynomial_positive_on ::
   "’n::finite cgu_matrix_polynomial \<Rightarrow> ’n cgu_point set \<Rightarrow>
      bool"
 where
   "cgu_polynomial_positive_on P W \<longleftrightarrow>
     (\<forall>x\<in>W.
       cgu_symmetric_positive_definite_matrix (cgu_matrix_poly_eval P x))"


English mathematical translation
Mathematical role: pointwise positive definiteness on a window
   Typed arguments/result: P :: ’n cgu matrix polynomial, W :: ’n cgu
point set, with ’n::finite; result bool. It holds exactly when for every x \<in>
W, cgu symmetric positive definite matrix (cgu matrix poly eval P x).
cgu_order_valid
Isabelle code

 definition cgu_order_valid ::
   "(’n, ’c::finite, ’h) cgu_model \<Rightarrow> bool"
 where
   "cgu_order_valid M \<longleftrightarrow>
     bij_betw (cgu_order M) {..<CARD(’c)} UNIV"


English mathematical translation
Mathematical role: bijective recovery enumeration
  Typed argument/result: M :: (’n,’c,’h) cgu model, with ’c::finite; result
bool. It holds exactly when cgu order M is a bijection from {..<CARD(’c)} to
UNIV.
cgu_before_indices
Isabelle code

 definition cgu_before_indices ::
   "(’n, ’c, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> ’c set"
 where
   "cgu_before_indices M r = cgu_order M ‘ {..<r}"


English mathematical translation
Mathematical role: earlier-cell set C<s
  Typed arguments/result: M :: (’n,’c,’h) cgu model, r :: nat; result ’c
set. It is the image cgu order M ‘ {..<r}.
cgu_after_indices
Isabelle code
90                             CĂTĂLIN I. CÂRSTEA


 definition cgu_after_indices ::
   "(’n, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> ’c set"
 where
   "cgu_after_indices M r = cgu_order M ‘ {r..<CARD(’c)}"


English mathematical translation
Mathematical role: future-cell set C≥s
   Typed arguments/result:       M :: (’n,’c,’h) cgu model, r :: nat, with
’c::finite; result ’c set. It is the image cgu order M ‘ {r..<CARD(’c)}.
cgu_remaining_domain
Isabelle code
 definition cgu_remaining_domain ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow>
     ’n cgu_point set"
 where
   "cgu_remaining_domain M r =
     interior (\<Union>c\<in>cgu_after_indices M r. closure (cgu_cell M c))"


English mathematical translation
Mathematical role: remaining region Rs
   Typed arguments/result:     M :: (’n,’c,’h) cgu model, r :: nat, with
’n,’c::finite; result ’n cgu point set. It is the interior of the union, over
c \<in> cgu after indices M r, of closure (cgu cell M c).
cgu_recovered_region
Isabelle code
 definition cgu_recovered_region ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow>
     ’n cgu_point set"
 where
   "cgu_recovered_region M r =
     cgu_domain M - closure (cgu_remaining_domain M r)"


English mathematical translation
Mathematical role: recovered region Ks
   Typed arguments/result:      M :: (’n,’c,’h) cgu model, r :: nat, with
’n,’c::finite; result ’n cgu point set. It is cgu domain M - closure (cgu
remaining domain M r).
cgu_face_connected
Isabelle code
 definition cgu_face_connected ::
   "’n::finite cgu_point set \<Rightarrow> ’c set \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_point set) \<Rightarrow> bool"
 where
   "cgu_face_connected G I cell \<longleftrightarrow>
     (\<forall>i\<in>I. \<forall>j\<in>I.
       rtranclp
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     91

        (\<lambda>a b. a \<in> I \<and> b \<in> I \<and>
          cgu_share_flat_face_in G (cell a) (cell b)) i j)"


English mathematical translation
Mathematical role: connectivity through planar adjacency
   Typed arguments/result: G :: ’n cgu point set, I :: ’c set, cell :: ’c
\<Rightarrow> ’n cgu point set, with ’n::finite; result bool. It holds ex-
actly when for every i \<in> I and j \<in> I, rtranclp R i j, where R a b is
the conjunction a \<in> I, b \<in> I, and cgu share flat face in G (cell a)
(cell b).
cgu_flat_face_patch
Isabelle code
 definition cgu_flat_face_patch ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow> real \<
      Rightarrow>
     ’n cgu_point set \<Rightarrow> bool"
 where
   "cgu_flat_face_patch D normal offset gamma \<longleftrightarrow>
     norm normal = 1 \<and>
     gamma \<noteq> {} \<and>
     openin (top_of_set (cgu_affine_hyperplane normal offset)) gamma \<and>
     gamma \<subseteq> frontier D \<inter> cgu_affine_hyperplane normal offset \<
      and>
     (\<exists>U. open U \<and> gamma \<subseteq> U \<and>
       U \<inter> frontier D = U \<inter> cgu_affine_hyperplane normal offset \<and>

      (D \<inter> U \<subseteq> {x. inner normal x < offset} \<or>
       D \<inter> U \<subseteq> {x. offset < inner normal x}))"


English mathematical translation
Mathematical role: oriented flat boundary patch
   Typed arguments/result: D :: ’n cgu point set, normal :: ’n cgu point,
offset :: real, gamma :: ’n cgu point set, with ’n::finite; result bool.
It holds exactly when norm normal = 1, gamma \<noteq> {}, gamma is open
in the subspace on cgu affine hyperplane normal offset, gamma \<subseteq>
frontier D \<inter> cgu affine hyperplane normal offset, and there exists
U :: ’n cgu point set such that open U, gamma \<subseteq> U, U \<inter>
frontier D = U \<inter> cgu affine hyperplane normal offset, and either
D \<inter> U \<subseteq> {x. inner normal x < offset} or D \<inter> U
\<subseteq> {x. offset < inner normal x}.
cgu_clipped_recovery_interface_v6
Isabelle code
 definition cgu_clipped_recovery_interface_v6 ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> ’n
      cgu_point set"
 where
   "cgu_clipped_recovery_interface_v6 M r =
     cgu_domain M \<inter>
       frontier (cgu_recovered_region M r) \<inter>
92                             CĂTĂLIN I. CÂRSTEA

       frontier (cgu_remaining_domain M r)"


English mathematical translation
Mathematical role: recovery interface Υs
   Typed arguments/result:      M :: (’n,’c,’h) cgu model, r :: nat, with
’n,’c::finite; result ’n cgu point set.        It is cgu domain M \<inter>
frontier (cgu recovered region M r) \<inter> frontier (cgu remaining
domain M r).
cgu_active_pde_face_route_v4
Isabelle code

 definition cgu_active_pde_face_route_v4 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     nat \<Rightarrow> ’c \<Rightarrow> ’h \<Rightarrow> bool"
 where
   "cgu_active_pde_face_route_v4 M r c i \<longleftrightarrow>
     (let remaining = cgu_remaining_domain M r;
          recovered = cgu_recovered_region M r;
          interface = frontier recovered \<inter> frontier remaining;
          patch = cgu_face_patch M c i;
          normal = cgu_normal M c i;
          offset = cgu_offset M c i
      in if r = 0 then
           patch \<subseteq> cgu_measured M \<and>
           cgu_flat_face_patch (cgu_domain M) normal offset patch
         else
           (patch \<subseteq> cgu_measured M \<and>
            cgu_flat_face_patch (cgu_domain M) normal offset patch) \<or>
           (patch \<subseteq> cgu_domain M \<inter> interface \<and>
            cgu_flat_face_patch remaining normal offset patch))"


English mathematical translation
Mathematical role: stagewise face visibility
   Typed arguments/result: M :: (’n,’c,’h) cgu model, r :: nat, c :: ’c,
i :: ’h, with ’n,’c,’h::finite; result bool. Let remaining=cgu remaining
domain M r,    recovered=cgu recovered region M r,     interface=frontier
recovered \<inter> frontier remaining,        patch=cgu face patch M c i,
normal=cgu normal M c i, and offset=cgu offset M c i. If r=0, the condition
is    patch \<subseteq> cgu measured M \<and> cgu flat face patch (cgu
domain M) normal offset patch. Otherwise it is the disjunction of that same
condition and patch \<subseteq> cgu domain M \<inter> interface \<and>
cgu flat face patch remaining normal offset patch.
cgu_normal_height
Isabelle code

 definition cgu_normal_height ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow>
     ’n cgu_point \<Rightarrow> real"
 where
   "cgu_normal_height center normal x = inner normal (x - center)"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     93

English mathematical translation
Mathematical role: signed height hq,µ
   Typed arguments/result:          center,normal,x :: ’n cgu point,           with
’n::finite; result real. It equals inner normal (x - center).
cgu_tangent_part
Isabelle code

 definition cgu_tangent_part ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow>
     ’n cgu_point \<Rightarrow> ’n cgu_point"
 where
   "cgu_tangent_part center normal x =
     (x - center) - cgu_normal_height center normal x *\<^sub>R normal"


English mathematical translation
Mathematical role: tangential remainder τq,µ
   Typed arguments/result:       center,normal,x :: ’n cgu point,    with
’n::finite; result ’n cgu point. It equals (x-center) - cgu normal height
center normal x *\<^sub>R normal.
cgu_flat_disc
Isabelle code

 definition cgu_flat_disc ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow> real \<Rightarrow>

     ’n cgu_point set"
 where
   "cgu_flat_disc center normal r =
     {x. cgu_normal_height center normal x = 0 \<and>
       norm (cgu_tangent_part center normal x) < r}"


English mathematical translation
Mathematical role: flat disk D(q, µ, r)
   Typed arguments/result: center,normal :: ’n cgu point, r :: real, with
’n::finite; result ’n cgu point set. It is the set of all x :: ’n cgu point
such that cgu normal height center normal x = 0 and norm (cgu tangent
part center normal x) < r.
cgu_exterior_half_ball
Isabelle code

 definition cgu_exterior_half_ball ::
   "’n::finite cgu_point \<Rightarrow> ’n cgu_point \<Rightarrow> real \<Rightarrow>

     ’n cgu_point set"
 where
   "cgu_exterior_half_ball center normal r =
     ball center r \<inter> {x. cgu_normal_height center normal x < 0}"
94                             CĂTĂLIN I. CÂRSTEA

English mathematical translation
Mathematical role: lower half-ball B − (q, µ, r)
   Typed arguments/result: center,normal :: ’n cgu point, r :: real, with
’n::finite; result ’n cgu point set. It is ball center r \<inter> {x. cgu
normal height center normal x < 0}.
cgu_auxiliary_half_ball_geometry_step
Isabelle code

 definition cgu_auxiliary_half_ball_geometry_step ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow> nat \<Rightarrow> bool"
 where
   "cgu_auxiliary_half_ball_geometry_step M r \<longleftrightarrow>
     (let c = cgu_order M r;
           recovered = cgu_recovered_region M r;
           center = cgu_step_center M c;
           normal = cgu_step_interior_normal M c;
           rad = cgu_step_radius M c;
           patch = cgu_step_outer_patch M c;
           adjacent = cgu_step_adjacent_cell M c
      in norm normal = 1 \<and> 0 < rad \<and>
         patch \<noteq> {} \<and>
         openin (top_of_set (frontier (cgu_domain M))) patch \<and>
         patch \<subseteq> cgu_measured M \<inter> frontier recovered \<and>
         closure (cgu_flat_disc center normal rad)
            \<subseteq> patch - cgu_subdivision_edge_corner_set M \<and>
         cgu_domain M \<inter> ball center rad =
            ball center rad \<inter> {x. 0 < cgu_normal_height center normal x} \<
      and>
         adjacent \<in> cgu_before_indices M r \<and>
         cgu_flat_disc center normal rad
            \<subseteq> frontier (cgu_domain M) \<inter> frontier (cgu_cell M
      adjacent))"


English mathematical translation
Mathematical role: exterior recovery-ball condition
   Typed arguments/result:      M :: (’n,’c,’h) cgu model, r :: nat, with
’n,’c::finite; result bool. Let c=cgu order M r, recovered=cgu recovered
region M r,      center=cgu step center M c,         normal=cgu step interior
normal M c,      rad=cgu step radius M c,         patch=cgu step outer patch M
c, and adjacent=cgu step adjacent cell M c.           The condition is the con-
junction: norm normal=1; 0<rad; patch\<noteq>{}; patch is open in the
subspace on frontier (cgu domain M); patch \<subseteq> cgu measured
M \<inter> frontier recovered;         closure (cgu flat disc center normal
rad) \<subseteq> patch - cgu subdivision edge corner set M; cgu domain
M \<inter> ball center rad = ball center rad \<inter> {x. 0 < cgu
normal height center normal x}; adjacent \<in> cgu before indices M r;
and cgu flat disc center normal rad \<subseteq> frontier (cgu domain
M) \<inter> frontier (cgu cell M adjacent).
cgu_recovery_geometry_operational_v6
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     95


 definition cgu_recovery_geometry_operational_v6 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow> bool"
 where
   "cgu_recovery_geometry_operational_v6 M \<longleftrightarrow>
     cgu_order_valid M \<and>
     (\<forall>r<CARD(’c).
       let c = cgu_order M r;
            remaining = cgu_remaining_domain M r;
            recovered = cgu_recovered_region M r;
            I = cgu_faces M c
       in cgu_lipschitz_domain remaining \<and>
           (r = 0 \<or>
            (recovered \<noteq> {} \<and>
             cgu_lipschitz_domain recovered \<and>
             cgu_face_connected recovered (cgu_before_indices M r) (cgu_cell M) \<
      and>
             cgu_auxiliary_half_ball_geometry_step M r)) \<and>
           (\<forall>i\<in>I.
             cgu_flat_face_patch (cgu_cell M c)
               (cgu_normal M c i) (cgu_offset M c i) (cgu_face_patch M c i) \<and>
             cgu_face_patch M c i \<subseteq>
               - cgu_subdivision_edge_corner_set M \<and>
             cgu_face_patch M c i \<subseteq> frontier remaining \<and>
             cgu_active_pde_face_route_v4 M r c i) \<and>
           cgu_degree M c + 3 \<le> card I \<and>
           cgu_n_generic_on (cgu_degree M c) I
             (cgu_normal M c) (cgu_offset M c) (cgu_witness_faces M c) \<and>
           (\<forall>i\<in>I. \<forall>j\<in>cgu_witness_faces M c i.
             \<forall>k\<in>cgu_witness_faces M c i. j \<noteq> k \<longrightarrow>
             cgu_triple_region_geometry (cgu_triple_region M c i j k)
               (cgu_normal M c i) (cgu_offset M c i)
               (cgu_normal M c j) (cgu_offset M c j)
               (cgu_normal M c k) (cgu_offset M c k))) \<and>
     (\<forall>r<CARD(’c).
       let remaining = cgu_remaining_domain M r;
            recovered = cgu_recovered_region M r
       in cgu_graph_lipschitz_domain_v5 remaining \<and>
           (r = 0 \<or> cgu_graph_lipschitz_domain_v5 recovered))"


English mathematical translation
Mathematical role: admissible recovery order
   Typed       argument/result:          M :: (’n,’c,’h) cgu model,      with
’n,’c,’h::finite; result bool. It holds exactly when cgu order valid M
and both following universally quantified blocks hold.
   First, for every r :: nat restricted by r < CARD(’c), let c=cgu order M r,
remaining=cgu remaining domain M r, recovered=cgu recovered region M r,
and I=cgu faces M c. Then: cgu lipschitz domain remaining; either r=0 or
all of recovered \<noteq> {}, cgu lipschitz domain recovered, cgu face
connected recovered (cgu before indices M r) (cgu cell M), and cgu
auxiliary half ball geometry step M r; for every i \<in> I, all of cgu flat
face patch (cgu cell M c) (cgu normal M c i) (cgu offset M c i) (cgu
face patch M c i), cgu face patch M c i \<subseteq> - cgu subdivision
edge corner set M, cgu face patch M c i \<subseteq> frontier remaining,
and cgu active pde face route v4 M r c i; cgu degree M c + 3 \<le> card
96                             CĂTĂLIN I. CÂRSTEA

I;     cgu n generic on (cgu degree M c) I (cgu normal M c) (cgu offset
M c) (cgu witness faces M c); and for every i \<in> I, j \<in> cgu
witness faces M c i, and k \<in> cgu witness faces M c i, the hypothesis
j \<noteq> k implies cgu triple region geometry (cgu triple region M c
i j k) (cgu normal M c i) (cgu offset M c i) (cgu normal M c j) (cgu
offset M c j) (cgu normal M c k) (cgu offset M c k).
   Second, for every r :: nat restricted by r<CARD(’c), let remaining=cgu
remaining domain M r and recovered=cgu recovered region M r; then cgu
graph lipschitz domain v5 remaining and either r=0 or cgu graph lipschitz
domain v5 recovered.
cgu_auxiliary_extension_elliptic
Isabelle code

 definition cgu_auxiliary_extension_elliptic ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> nat \<Rightarrow>
      bool"
 where
   "cgu_auxiliary_extension_elliptic M P r \<longleftrightarrow>
     (let c = cgu_order M r;
          adjacent = cgu_step_adjacent_cell M c
      in cgu_uniformly_positive_definite_on
            (cgu_exterior_half_ball (cgu_step_center M c)
              (cgu_step_interior_normal M c) (cgu_step_radius M c))
            (P adjacent))"


English mathematical translation
Mathematical role: adjacent-coefficient ellipticity on the recovery half-ball
   Typed     arguments/result:     M :: (’n,’c,’h) cgu model,    P :: ’c
\<Rightarrow> ’n cgu matrix polynomial, r :: nat, with ’n,’c::finite;
result bool. Let c=cgu order M r and adjacent=cgu step adjacent cell M c.
The condition is cgu uniformly positive definite on (cgu exterior half
ball (cgu step center M c) (cgu step interior normal M c) (cgu step
radius M c)) (P adjacent).
cgu_recovery_extension_admissible
Isabelle code

 definition cgu_recovery_extension_admissible ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> bool"
 where
   "cgu_recovery_extension_admissible M P \<longleftrightarrow>
     (\<forall>r<CARD(’c).
       let c = cgu_order M r;
           I = cgu_faces M c
       in (r = 0 \<or> cgu_auxiliary_extension_elliptic M P r) \<and>
          (\<forall>i\<in>I. \<forall>j\<in>cgu_witness_faces M c i.
            \<forall>k\<in>cgu_witness_faces M c i. j \<noteq> k \<longrightarrow>
              cgu_polynomial_positive_on (P c)
               (cgu_triple_region M c i j k)))"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     97

English mathematical translation
Mathematical role: coefficient-access condition
   Typed    arguments/result:           M :: (’n,’c,’h) cgu model, P :: ’c
\<Rightarrow> ’n cgu matrix polynomial, with ’n,’c,’h::finite; result
bool. It holds exactly when, for every r :: nat restricted by r<CARD(’c),
let c=cgu order M r and I=cgu faces M c; then (r=0 \<or> cgu auxiliary
extension elliptic M P r) and, for every i \<in> I, j \<in> cgu witness
faces M c i, and k \<in> cgu witness faces M c i, the hypothesis j
\<noteq> k implies cgu polynomial positive on (P c) (cgu triple region M
c i j k).
cgu_potential
Isabelle code

 type_synonym ’n cgu_potential = "’n cgu_point \<Rightarrow> real"


English mathematical translation
Mathematical role: scalar-function type FI
  For every type ’n, ’n cgu potential is exactly the function type ’n cgu point
\<Rightarrow> real.
cgu_gradient
Isabelle code

 type_synonym ’n cgu_gradient = "’n cgu_point \<Rightarrow> ’n cgu_point"


English mathematical translation
Mathematical role: vector-field type VI
  For every type ’n, ’n cgu gradient is exactly the function type ’n cgu point
\<Rightarrow> ’n cgu point.
cgu_partial_derivative
Isabelle code

 definition cgu_partial_derivative ::
   "(’n::finite cgu_potential) \<Rightarrow> ’n \<Rightarrow> ’n cgu_point \<
      Rightarrow> real"
 where
   "cgu_partial_derivative phi i x =
     frechet_derivative phi (at x) (axis i 1)"


English mathematical translation
Mathematical role: selected coordinate derivative ∂i ϕ
  Typed arguments/result: phi :: ’n cgu potential, i :: ’n, x :: ’n cgu
point, with ’n::finite; result real. It equals frechet derivative phi (at x)
(axis i 1).
cgu_classical_gradient
Isabelle code
98                             CĂTĂLIN I. CÂRSTEA


 definition cgu_classical_gradient ::
   "’n::finite cgu_potential \<Rightarrow> ’n cgu_gradient"
 where
   "cgu_classical_gradient phi x =
     (\<chi> i. cgu_partial_derivative phi i x)"


English mathematical translation
Mathematical role: gradient vector ∇ϕ
   Typed argument/result: phi :: ’n cgu potential, with ’n::finite; result
’n cgu gradient. For every x :: ’n cgu point, its value is the indexed vector
\<chi> i. cgu partial derivative phi i x, with i :: ’n.
cgu_test_function_on
Isabelle code
 definition cgu_test_function_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow> bool"
 where
   "cgu_test_function_on U phi \<longleftrightarrow>
     smooth_on UNIV phi \<and>
     compact (closure {x. phi x \<noteq> 0}) \<and>
     closure {x. phi x \<noteq> 0} \<subseteq> U"


English mathematical translation
Mathematical role: test class D(U )
   Typed arguments/result: U :: ’n cgu point set, phi :: ’n cgu potential,
with ’n::finite; result bool.       It holds exactly when smooth on UNIV
phi, compact (closure {x. phi x \<noteq> 0}), and closure {x. phi x
\<noteq> 0} \<subseteq> U.
cgu_weak_gradient_on
Isabelle code
 definition cgu_weak_gradient_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_weak_gradient_on U u Du \<longleftrightarrow>
     (\<forall>phi. cgu_test_function_on U phi \<longrightarrow>
       (\<forall>i.
         set_integrable lborel U
           (\<lambda>x. u x * cgu_partial_derivative phi i x) \<and>
         set_integrable lborel U (\<lambda>x. Du x $ i * phi x) \<and>
         set_lebesgue_integral lborel U
           (\<lambda>x. u x * cgu_partial_derivative phi i x) =
         - set_lebesgue_integral lborel U (\<lambda>x. Du x $ i * phi x)))"


English mathematical translation
Mathematical role: weak-gradient integration-by-parts relation
   Typed arguments/result: U :: ’n cgu point set, u :: ’n cgu potential,
Du :: ’n cgu gradient, with ’n::finite; result bool. It holds exactly when, for
every phi :: ’n cgu potential, the hypothesis cgu test function on U phi
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                     99

implies that for every i :: ’n: both functions x \<mapsto> u x * cgu partial
derivative phi i x and x \<mapsto> Du x $ i * phi x are set-integrable with
respect to lborel on U, and their set Lebesgue integrals satisfy integral U (u*cgu
partial derivative phi i) = - integral U ((Du coordinate i)*phi).
cgu_h1_pair_on
Isabelle code
 definition cgu_h1_pair_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_h1_pair_on U u Du \<longleftrightarrow>
     u \<in> borel_measurable (restrict_space lborel U) \<and>
     Du \<in> borel_measurable (restrict_space lborel U) \<and>
     cgu_weak_gradient_on U u Du \<and>
     set_integrable lborel U (\<lambda>x. u x ^ 2) \<and>
     set_integrable lborel U (\<lambda>x. norm (Du x) ^ 2)"


English mathematical translation
                               1
Mathematical role: pair class Hpair (U )
   Typed arguments/result: U :: ’n cgu point set, u :: ’n cgu potential,
Du :: ’n cgu gradient, with ’n::finite; result bool. It holds exactly when
u \<in> borel measurable (restrict space lborel U),       Du \<in> borel
measurable (restrict space lborel U), cgu weak gradient on U u Du, x
\<mapsto> u x^2 is set-integrable on U, and x \<mapsto> norm (Du x)^2 is
set-integrable on U.
cgu_h1_squared_distance
Isabelle code
 definition cgu_h1_squared_distance ::
   "’n::finite cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> real"
 where
   "cgu_h1_squared_distance U u Du v Dv =
     set_lebesgue_integral lborel U
       (\<lambda>x. (u x - v x) ^ 2 + norm (Du x - Dv x) ^ 2)"


English mathematical translation
Mathematical role: squared pair distance d2U
  Typed arguments/result: U :: ’n cgu point set; u,v :: ’n cgu potential;
Du,Dv :: ’n cgu gradient; with ’n::finite; result real. It equals the set
Lebesgue integral over U of x \<mapsto> (u x-v x)^2 + norm (Du x-Dv x)^2.
cgu_h1_zero_pair_on
Isabelle code
 definition cgu_h1_zero_pair_on ::
   "(real ^ ’n::finite) set \<Rightarrow>
     ((real ^ ’n) \<Rightarrow> real) \<Rightarrow>
     ((real ^ ’n) \<Rightarrow> (real ^ ’n)) \<Rightarrow> bool"
100                            CĂTĂLIN I. CÂRSTEA

 where
   "cgu_h1_zero_pair_on U u Du \<longleftrightarrow>
     cgu_h1_pair_on U u Du \<and>
     (\<exists>(seq :: nat \<Rightarrow> ’n cgu_potential).
       (\<forall>m. cgu_test_function_on U (seq m) \<and>
         cgu_h1_pair_on U (seq m) (cgu_classical_gradient (seq m))) \<and>
       (\<forall>epsilon>0. \<exists>N. \<forall>m\<ge>N.
         cgu_h1_squared_distance U (seq m)
           (cgu_classical_gradient (seq m)) u Du < epsilon))"


English mathematical translation
                                             1
Mathematical role: zero-boundary pair class H0,pair (U )
   Typed    arguments/result:       U :: (real ^ ’n) set,      u :: real ^ ’n
\<Rightarrow> real,       Du :: real ^ ’n \<Rightarrow> real ^ ’n,        with
’n::finite; result bool. It holds exactly when cgu h1 pair on U u Du and there
exists seq :: nat \<Rightarrow> ’n cgu potential such that: for every m
:: nat, both cgu test function on U (seq m) and cgu h1 pair on U (seq m)
(cgu classical gradient (seq m)); and for every epsilon :: real restricted
by epsilon>0, there exists N :: nat such that for every m :: nat restricted
by m\<ge>N, cgu h1 squared distance U (seq m) (cgu classical gradient
(seq m)) u Du < epsilon.
cgu_cellwise_coefficient
Isabelle code

 definition cgu_cellwise_coefficient ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point \<Rightarrow> real ^ ’n ^ ’n"
 where
   "cgu_cellwise_coefficient M P x =
     (if \<exists>c. x \<in> cgu_cell M c
      then cgu_matrix_poly_eval (P (SOME c. x \<in> cgu_cell M c)) x
      else 0)"


English mathematical translation
Mathematical role: everywhere-defined selected-cell field AM,P
   Typed      arguments/result:       M :: (’n,’c,’h) cgu model,           P :: ’c
\<Rightarrow> ’n cgu matrix polynomial,            x :: ’n cgu point,           with
’n,’c::finite; result real ^ ’n ^ ’n. If there exists c :: ’c with x \<in>
cgu cell M c, the result is cgu matrix poly eval (P (SOME c. x \<in> cgu
cell M c)) x; otherwise it is 0. SOME makes a Hilbert-choice selection from the
stated existence condition; no uniqueness condition appears in this definition.
cgu_boundary_test_on
Isabelle code

 definition cgu_boundary_test_on ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> bool"
 where
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    101

   "cgu_boundary_test_on M U gamma f \<longleftrightarrow>
     smooth_on UNIV f \<and>
     compact (closure {x. f x \<noteq> 0}) \<and>
     closure {x. x \<in> frontier U \<and> f x \<noteq> 0}
       \<subseteq> gamma - cgu_subdivision_edge_corner_set M \<and>
     cgu_h1_pair_on U f (cgu_classical_gradient f)"


English mathematical translation
Mathematical role: smooth boundary-supported datum
   Typed arguments/result: M :: (’n,’c,’h) cgu model, U,gamma :: ’n cgu
point set, f :: ’n cgu potential, with ’n,’c,’h::finite; result bool. It
holds exactly when smooth on UNIV f, compact (closure {x. f x \<noteq>
0}), closure {x. x \<in> frontier U \<and> f x \<noteq> 0} \<subseteq>
gamma - cgu subdivision edge corner set M, and cgu h1 pair on U f (cgu
classical gradient f).
cgu_local_trace_pair_on
Isabelle code

 definition cgu_local_trace_pair_on ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_local_trace_pair_on M U gamma f Df \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     (\<exists>(seq :: nat \<Rightarrow> ’n cgu_potential).
       (\<forall>m. cgu_boundary_test_on M U gamma (seq m)) \<and>
       (\<forall>epsilon>0. \<exists>N. \<forall>m\<ge>N.
         \<exists>z Dz. cgu_h1_zero_pair_on U z Dz \<and>
           cgu_h1_squared_distance U (seq m)
             (cgu_classical_gradient (seq m))
             (\<lambda>x. f x + z x) (\<lambda>x. Df x + Dz x) < epsilon))"


English mathematical translation
Mathematical role: boundary-data closure predicate TM (U, γ)
   Typed arguments/result:     M :: (’n,’c,’h) cgu model, U,gamma :: ’n
cgu point set,     f :: ’n cgu potential,      Df :: ’n cgu gradient,      with
’n,’c,’h::finite; result bool. It holds exactly when cgu h1 pair on U f
Df and there exists seq :: nat \<Rightarrow> ’n cgu potential such that
every m satisfies cgu boundary test on M U gamma (seq m), and for every
epsilon>0 there exists N :: nat such that for every m\<ge>N there exist z :: ’n
cgu potential and Dz :: ’n cgu gradient with cgu h1 zero pair on U z Dz
and cgu h1 squared distance U (seq m) (cgu classical gradient (seq m))
(\<lambda>x. f x+z x) (\<lambda>x. Df x+Dz x) < epsilon.
cgu_weak_solution_on
Isabelle code

 definition cgu_weak_solution_on ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
102                            CĂTĂLIN I. CÂRSTEA

     ’n cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_weak_solution_on M P U u Du \<longleftrightarrow>
     cgu_h1_pair_on U u Du \<and>
     (\<forall>phi. cgu_test_function_on U phi \<longrightarrow>
       set_integrable lborel U
         (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
           (cgu_classical_gradient phi x)) \<and>
       set_lebesgue_integral lborel U
         (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
           (cgu_classical_gradient phi x)) = 0)"


English mathematical translation
Mathematical role: AM,P -harmonic pair
   Typed    arguments/result:     M :: (’n,’c,’h) cgu model,          P :: ’c
\<Rightarrow> ’n cgu matrix polynomial,      U :: ’n cgu point set,        u ::
’n cgu potential, Du :: ’n cgu gradient, with ’n,’c::finite; result
bool. It holds exactly when cgu h1 pair on U u Du and, for every phi, the
hypothesis cgu test function on U phi implies both set-integrability on U
of    x \<mapsto> inner (cgu cellwise coefficient M P x *v Du x) (cgu
classical gradient phi x) and equality of that function’s set Lebesgue integral
to 0.
cgu_dirichlet_solution_for
Isabelle code

 definition cgu_dirichlet_solution_for ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_dirichlet_solution_for M P U f Df u Du \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     cgu_weak_solution_on M P U u Du \<and>
     cgu_h1_zero_pair_on U (\<lambda>x. u x - f x)
       (\<lambda>x. Du x - Df x)"


English mathematical translation
Mathematical role: AM,P -Dirichlet pair
  Typed      arguments/result:       M :: (’n,’c,’h) cgu model,     P :: ’c
\<Rightarrow> ’n cgu matrix polynomial,       U :: ’n cgu point set,    f,u
:: ’n cgu potential, Df,Du :: ’n cgu gradient, with ’n,’c::finite; result
bool. It holds exactly when cgu h1 pair on U f Df, cgu weak solution on M P
U u Du, and cgu h1 zero pair on U (\<lambda>x. u x-f x) (\<lambda>x. Du
x-Df x).
cgu_dn_energy
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    103


 definition cgu_dn_energy ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> real"
 where
   "cgu_dn_energy M P U Du Dh =
     set_lebesgue_integral lborel U
       (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
         (Dh x))"


English mathematical translation
Mathematical role: local energy pairing EM,P,U
   Typed     arguments/result:        M :: (’n,’c,’h) cgu model,     P :: ’c
\<Rightarrow> ’n cgu matrix polynomial, U :: ’n cgu point set, Du,Dh ::
’n cgu gradient, with ’n,’c::finite; result real. It equals the set Lebesgue
integral on U of x \<mapsto> inner (cgu cellwise coefficient M P x *v Du
x) (Dh x).
cgu_dn_energy_integrable
Isabelle code
 definition cgu_dn_energy_integrable ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "cgu_dn_energy_integrable M P U Du Dh \<longleftrightarrow>
     set_integrable lborel U
       (\<lambda>x. inner (cgu_cellwise_coefficient M P x *v Du x)
         (Dh x))"


English mathematical translation
Mathematical role: local energy-integrability predicate
  Typed arguments/result: the same argument types as declaration 065; result
bool. It holds exactly when x \<mapsto> inner (cgu cellwise coefficient M
P x *v Du x) (Dh x) is set-integrable with respect to lborel on U.
cgu_local_dn_equal
Isabelle code
 definition cgu_local_dn_equal ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow> bool"
 where
   "cgu_local_dn_equal M P1 P2 U gamma \<longleftrightarrow>
     (\<forall>f Df. cgu_local_trace_pair_on M U gamma f Df \<longrightarrow>
       (\<exists>u Du. cgu_dirichlet_solution_for M P1 U f Df u Du) \<and>
       (\<exists>u Du. cgu_dirichlet_solution_for M P2 U f Df u Du)) \<and>
     (\<forall>f Df h Dh u1 Du1 u2 Du2.
104                            CĂTĂLIN I. CÂRSTEA

       cgu_local_trace_pair_on M U gamma f Df \<and>
       cgu_local_trace_pair_on M U gamma h Dh \<and>
       cgu_dirichlet_solution_for M P1 U f Df u1 Du1 \<and>
       cgu_dirichlet_solution_for M P2 U f Df u2 Du2
       \<longrightarrow>
       cgu_dn_energy_integrable M P1 U Du1 Dh \<and>
       cgu_dn_energy_integrable M P2 U Du2 Dh \<and>
       cgu_dn_energy M P1 U Du1 Dh = cgu_dn_energy M P2 U Du2 Dh)"


English mathematical translation
Mathematical role: stipulated local boundary-energy comparison
   Typed arguments/result:       M :: (’n,’c,’h) cgu model,        P1,P2 :: ’c
\<Rightarrow> ’n cgu matrix polynomial,         U,gamma :: ’n cgu point set,
with ’n,’c,’h::finite; result bool. It is a conjunction of two blocks.
   First, for every f :: ’n cgu potential and Df :: ’n cgu gradient, the
hypothesis cgu local trace pair on M U gamma f Df implies both an ex-
istence \<exists>u Du. cgu dirichlet solution for M P1 U f Df u Du and,
separately, an existence \<exists>u Du. cgu dirichlet solution for M P2 U
f Df u Du.
   Second, for every f,Df,h,Dh,u1,Du1,u2,Du2 of their forced scalar-
function/vector-function types, the conjunction cgu local trace pair on M
U gamma f Df, cgu local trace pair on M U gamma h Dh, cgu dirichlet
solution for M P1 U f Df u1 Du1, and cgu dirichlet solution for M P2 U
f Df u2 Du2 implies all three conclusions: cgu dn energy integrable M P1 U
Du1 Dh; cgu dn energy integrable M P2 U Du2 Dh; and cgu dn energy M P1 U
Du1 Dh = cgu dn energy M P2 U Du2 Dh.
lu_metric
Isabelle code

 type_synonym ’n lu_metric = "’n cgu_point \<Rightarrow> real ^ ’n ^ ’n"


English mathematical translation
Mathematical role: matrix-field function type
   For every ’n, ’n lu metric is exactly ’n cgu point \<Rightarrow> real ^
’n ^ ’n.
lu_density
Isabelle code

 type_synonym ’n lu_density = "’n cgu_point \<Rightarrow> real"


English mathematical translation
Mathematical role: scalar-field function type
  For every ’n, ’n lu density is exactly ’n cgu point \<Rightarrow> real.
lu_smooth_metric_density_data_on
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    105


 definition lu_smooth_metric_density_data_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_density \<Rightarrow> bool"
 where
   "lu_smooth_metric_density_data_on V g a rho \<longleftrightarrow>
     open V \<and>
     (\<forall>i j. smooth_on V (\<lambda>x. g x $ i $ j)) \<and>
     (\<forall>i j. smooth_on V (\<lambda>x. a x $ i $ j)) \<and>
     smooth_on V rho \<and>
     (\<forall>x\<in>V.
       cgu_symmetric_positive_definite_matrix (g x) \<and>
       cgu_symmetric_positive_definite_matrix (a x) \<and>
       0 < rho x \<and>
       rho x ^ 2 = det (g x) \<and>
       (\<forall>v. a x *v (g x *v v) = rho x *\<^sub>R v))"


English mathematical translation
Mathematical role: metric–conductivity package
   Typed arguments/result: V :: ’n cgu point set, g,a :: ’n lu metric, rho
:: ’n lu density, with ’n::finite; result bool. It holds exactly when: open
V; for every i,j :: ’n, smooth on V (\<lambda>x. g x $ i $ j); for every
i,j, smooth on V (\<lambda>x. a x $ i $ j); smooth on V rho; and for ev-
ery x \<in> V, all of cgu symmetric positive definite matrix (g x), cgu
symmetric positive definite matrix (a x), 0<rho x, rho x^2 = det (g x),
and, for every v :: ’n cgu point, a x *v (g x *v v) = rho x *\<^sub>R v.
lu_smooth_metric_extension_near
Isabelle code
 definition lu_smooth_metric_extension_near ::
   "(’n::finite, ’c::finite, ’h) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_density \<Rightarrow> bool"
 where
   "lu_smooth_metric_extension_near M P U gamma g a rho \<longleftrightarrow>
     (\<exists>V. gamma \<subseteq> V \<and>
       lu_smooth_metric_density_data_on V g a rho \<and>
       (\<forall>x\<in>U \<inter> V. a x = cgu_cellwise_coefficient M P x))"


English mathematical translation
Mathematical role: package realization predicate for arbitrary U, γ
   Typed    arguments/result:         M :: (’n,’c,’h) cgu model,      P :: ’c
\<Rightarrow> ’n cgu matrix polynomial,           U,gamma :: ’n cgu point set,
g,a :: ’n lu metric, rho :: ’n lu density, with ’n,’c::finite; result bool.
It holds exactly when there exists V :: ’n cgu point set such that gamma
\<subseteq> V, lu smooth metric density data on V g a rho, and for every x
\<in> U \<inter> V, a x = cgu cellwise coefficient M P x.
lu_induced_boundary_metrics_equal_on
Isabelle code
106                            CĂTĂLIN I. CÂRSTEA


 definition lu_induced_boundary_metrics_equal_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_point \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow> bool"
 where
   "lu_induced_boundary_metrics_equal_on gamma normal g1 g2 \<longleftrightarrow>
     (\<forall>x\<in>gamma. \<forall>xi eta.
       inner normal xi = 0 \<and> inner normal eta = 0
       \<longrightarrow>
       inner xi (g1 x *v eta) = inner xi (g2 x *v eta))"


English mathematical translation
Mathematical role: tangential bilinear-pairing agreement
   Typed arguments/result: gamma :: ’n cgu point set, normal :: ’n cgu
point, g1,g2 :: ’n lu metric, with ’n::finite; result bool. It holds exactly
when for every x \<in> gamma and every unrestricted xi,eta :: ’n cgu point,
the hypotheses inner normal xi=0 and inner normal eta=0 imply inner xi
(g1 x *v eta) = inner xi (g2 x *v eta).
mclean_coefficient
Isabelle code

 type_synonym ’n mclean_coefficient =
   "’n cgu_point \<Rightarrow> real ^ ’n ^ ’n"


English mathematical translation
Mathematical role: matrix-field function type
  For every ’n, ’n mclean coefficient is exactly ’n cgu point \<Rightarrow>
real ^ ’n ^ ’n.
mclean_source
Isabelle code

 type_synonym ’n mclean_source =
   "’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> real"


English mathematical translation
Mathematical role: total curried two-argument functional type
  For every ’n, ’n mclean source is exactly the curried functional type ’n cgu
potential \<Rightarrow> ’n cgu gradient \<Rightarrow> real.
mclean_h1_norm
Isabelle code

 definition mclean_h1_norm ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> real"
 where
   "mclean_h1_norm U u Du =
     sqrt (cgu_h1_squared_distance U u Du (\<lambda>_. 0) (\<lambda>_. 0))"
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    107

English mathematical translation
Mathematical role: Sobolev pair norm
  Typed arguments/result: U :: ’n cgu point set, u :: ’n cgu potential,
Du :: ’n cgu gradient, with ’n::finite; result real. It equals sqrt (cgu
h1 squared distance U u Du (\<lambda> .0) (\<lambda> .0)).
mclean_same_trace_on
Isabelle code
 definition mclean_same_trace_on ::
   "’n::finite cgu_point set \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_same_trace_on U f Df g Dg \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     cgu_h1_pair_on U g Dg \<and>
     cgu_h1_zero_pair_on U (\<lambda>x. f x - g x) (\<lambda>x. Df x - Dg x)"


English mathematical translation
Mathematical role: oriented difference-in-zero-boundary relation RU
  Typed arguments/result: U :: ’n cgu point set; f,g :: ’n cgu potential;
Df,Dg :: ’n cgu gradient; with ’n::finite; result bool. It holds exactly
when cgu h1 pair on U f Df, cgu h1 pair on U g Dg, and cgu h1 zero pair on
U (\<lambda>x. f x-g x) (\<lambda>x. Df x-Dg x).
mclean_trace_norm
Isabelle code
 definition mclean_trace_norm ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> real"
 where
   "mclean_trace_norm U f Df =
     Inf {r. \<exists>g Dg. mclean_same_trace_on U f Df g Dg \<and>
       r = mclean_h1_norm U g Dg}"


English mathematical translation
Mathematical role: raw infimum qU
   Typed arguments/result: U :: ’n cgu point set, f :: ’n cgu potential,
Df :: ’n cgu gradient, with ’n::finite; result real.           It is the in-
fimum of {r :: real. \<exists>g Dg. mclean same trace on U f Df g Dg
\<and> r=mclean h1 norm U g Dg}. The existential variables have types g :: ’n
cgu potential and Dg :: ’n cgu gradient.
mclean_energy
Isabelle code
 definition mclean_energy ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> ’n cgu_gradient \<Rightarrow> real"
 where
108                               CĂTĂLIN I. CÂRSTEA

      "mclean_energy U a Du Dv =
        set_lebesgue_integral lborel U (\<lambda>x. inner (a x *v Du x) (Dv x))"


English mathematical translation
Mathematical role: variational form Ba,U
   Typed arguments/result:          U :: ’n cgu point set,    a :: ’n mclean
coefficient, Du,Dv :: ’n cgu gradient, with ’n::finite; result real.
It equals the set Lebesgue integral over U of x \<mapsto> inner (a x *v Du x)
(Dv x).
mclean_energy_integrable
Isabelle code
 definition mclean_energy_integrable ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_energy_integrable U a Du Dv \<longleftrightarrow>
     set_integrable lborel U (\<lambda>x. inner (a x *v Du x) (Dv x))"


English mathematical translation
Mathematical role: variational-form integrability
   Typed arguments/result: the same argument types as declaration 078; result
bool. It holds exactly when x \<mapsto> inner (a x *v Du x) (Dv x) is set-
integrable with respect to lborel on U.
mclean_variational_form_on
Isabelle code
 definition mclean_variational_form_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "mclean_variational_form_on U a \<longleftrightarrow>
     (\<exists>coercive continuous. 0 < coercive \<and> 0 \<le> continuous \<and>
       (\<forall>u Du v Dv.
         cgu_h1_pair_on U u Du \<and> cgu_h1_pair_on U v Dv
         \<longrightarrow>
         mclean_energy_integrable U a Du Dv \<and>
         abs (mclean_energy U a Du Dv) \<le>
           continuous * mclean_h1_norm U u Du * mclean_h1_norm U v Dv) \<and>
       (\<forall>z Dz. cgu_h1_zero_pair_on U z Dz \<longrightarrow>
         coercive * mclean_h1_norm U z Dz ^ 2 \<le>
           mclean_energy U a Dz Dz))"


English mathematical translation
Mathematical role: bounded/coercive pair property
   Typed arguments/result:       U :: ’n cgu point set,    a :: ’n mclean
coefficient, with ’n::finite; result bool. It holds exactly when there exist
reals named coercive and continuous with 0<coercive and 0\<le>continuous
such that: for every u,v :: ’n cgu potential and Du,Dv :: ’n cgu gradient,
the hypotheses cgu h1 pair on U u Du and cgu h1 pair on U v Dv imply
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    109

mclean energy integrable U a Du Dv and abs (mclean energy U a Du Dv)
\<le> continuous * mclean h1 norm U u Du * mclean h1 norm U v Dv; and
for every z :: ’n cgu potential, Dz :: ’n cgu gradient, the hypothesis cgu
h1 zero pair on U z Dz implies coercive * mclean h1 norm U z Dz^2 \<le>
mclean energy U a Dz Dz. The bound variable continuous is a real variable
here, not the imported predicate of that spelling.
mclean_weak_solution_on
Isabelle code

 definition mclean_weak_solution_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_weak_solution_on U a u Du \<longleftrightarrow>
     cgu_h1_pair_on U u Du \<and>
     (\<forall>phi. cgu_test_function_on U phi \<longrightarrow>
       mclean_energy_integrable U a Du (cgu_classical_gradient phi) \<and>
       mclean_energy U a Du (cgu_classical_gradient phi) = 0)"


English mathematical translation
Mathematical role: a-harmonic pair
   Typed arguments/result:         U :: ’n cgu point set,  a :: ’n mclean
coefficient,      u :: ’n cgu potential,     Du :: ’n cgu gradient,   with
’n::finite; result bool.      It holds exactly when cgu h1 pair on U u Du
and, for every phi :: ’n cgu potential, the hypothesis cgu test function
on U phi implies both mclean energy integrable U a Du (cgu classical
gradient phi) and mclean energy U a Du (cgu classical gradient phi)=0.
mclean_dirichlet_solution_for
Isabelle code

 definition mclean_dirichlet_solution_for ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow>
     ’n cgu_potential \<Rightarrow> ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_dirichlet_solution_for U a f Df u Du \<longleftrightarrow>
     cgu_h1_pair_on U f Df \<and>
     mclean_weak_solution_on U a u Du \<and>
     mclean_same_trace_on U f Df u Du"


English mathematical translation
Mathematical role: a-Dirichlet pair
   Typed arguments/result:          U :: ’n cgu point set,   a :: ’n mclean
coefficient, f,u :: ’n cgu potential, Df,Du :: ’n cgu gradient, with
’n::finite; result bool. It holds exactly when cgu h1 pair on U f Df, mclean
weak solution on U a u Du, and mclean same trace on U f Df u Du.
mclean_green_solution_for
Isabelle code
110                             CĂTĂLIN I. CÂRSTEA


 definition mclean_green_solution_for ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow>
     ’n mclean_source \<Rightarrow> ’n cgu_potential \<Rightarrow>
     ’n cgu_gradient \<Rightarrow> bool"
 where
   "mclean_green_solution_for U a F u Du \<longleftrightarrow>
     cgu_h1_zero_pair_on U u Du \<and>
     (\<forall>v Dv. cgu_h1_zero_pair_on U v Dv \<longrightarrow>
       mclean_energy_integrable U a Du Dv \<and>
       mclean_energy U a Du Dv = F v Dv)"


English mathematical translation
Mathematical role: source-driven variational solution
  Typed arguments/result:          U :: ’n cgu point set,  a :: ’n mclean
coefficient, F :: ’n mclean source, u :: ’n cgu potential, Du :: ’n
cgu gradient, with ’n::finite; result bool. It holds exactly when cgu h1
zero pair on U u Du and, for every v :: ’n cgu potential and Dv :: ’n cgu
gradient, the hypothesis cgu h1 zero pair on U v Dv implies both mclean
energy integrable U a Du Dv and mclean energy U a Du Dv = F v Dv.
mclean_source_bound_on
Isabelle code
 definition mclean_source_bound_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_source \<Rightarrow> real \<
      Rightarrow> bool"
 where
   "mclean_source_bound_on U F K \<longleftrightarrow>
     0 \<le> K \<and> F (\<lambda>_. 0) (\<lambda>_. 0) = 0 \<and>
     (\<forall>u Du v Dv.
       cgu_h1_zero_pair_on U u Du \<and> cgu_h1_zero_pair_on U v Dv
       \<longrightarrow>
       F (\<lambda>x. u x + v x) (\<lambda>x. Du x + Dv x) = F u Du + F v Dv) \<and>

      (\<forall>r u Du. cgu_h1_zero_pair_on U u Du \<longrightarrow>
        F (\<lambda>x. r * u x) (\<lambda>x. r *\<^sub>R Du x) = r * F u Du) \<and>
      (\<forall>u Du. cgu_h1_zero_pair_on U u Du \<longrightarrow>
        abs (F u Du) \<le> K * mclean_h1_norm U u Du)"


English mathematical translation
Mathematical role: K-bounded-linear total functional on zero-boundary pairs
   Typed arguments/result: U :: ’n cgu point set, F :: ’n mclean source,
K :: real, with ’n::finite; result bool. It holds exactly when: 0\<le>K;
F (\<lambda> .0) (\<lambda> .0)=0; for all u,Du,v,Dv, if cgu h1 zero pair
on U u Du and cgu h1 zero pair on U v Dv, then F (\<lambda>x. u x+v x)
(\<lambda>x. Du x+Dv x)=F u Du+F v Dv; for every r :: real, u, and Du,
if cgu h1 zero pair on U u Du, then F (\<lambda>x. r*u x) (\<lambda>x. r
*\<^sub>R Du x)=r*F u Du; and for every u,Du, if cgu h1 zero pair on U u Du,
then abs(F u Du) \<le> K*mclean h1 norm U u Du.
mclean_flat_chart
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    111


 definition mclean_flat_chart ::
   "(’m::finite cgu_point \<Rightarrow> ’n::finite cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> bool"
 where
   "mclean_flat_chart chart normal \<longleftrightarrow>
     norm normal = 1 \<and>
     (\<forall>x y. norm (chart x - chart y) = norm (x - y)) \<and>
     (\<forall>x y. inner normal (chart x - chart y) = 0)"


English mathematical translation
Mathematical role: flat isometric chart
  Typed arguments/result: chart :: ’m cgu point \<Rightarrow> ’n cgu
point, normal :: ’n cgu point, with ’m,’n::finite; result bool. It holds
exactly when norm normal=1; for every x,y :: ’m cgu point, norm (chart x-
chart y)=norm (x-y); and for every such x,y, inner normal (chart x-chart
y)=0.
mclean_flat_offset_action
Isabelle code

 definition mclean_flat_offset_action ::
   "(’m::finite cgu_point \<Rightarrow> ’n::finite cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> ’m cgu_potential \<Rightarrow>
     ’n cgu_potential \<Rightarrow> real"
 where
   "mclean_flat_offset_action chart normal t g phi =
     integral\<^sup>L lborel
       (\<lambda>x. g x * phi (chart x + t *\<^sub>R normal))"


English mathematical translation
Mathematical role: translated source action Stg
   Typed arguments/result: chart :: ’m cgu point \<Rightarrow> ’n cgu
point, normal :: ’n cgu point, t :: real, g :: ’m cgu potential, phi ::
’n cgu potential, with ’m,’n::finite; result real. It equals the Lebesgue
integral with respect to lborel of x \<mapsto> g x * phi (chart x + t
*\<^sub>R normal).
mclean_source_extends_flat_offset_action
Isabelle code

 definition mclean_source_extends_flat_offset_action ::
   "’n::finite cgu_point set \<Rightarrow>
     (’m::finite cgu_point \<Rightarrow> ’n cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow> ’m cgu_potential \<Rightarrow>
     ’n mclean_source \<Rightarrow> bool"
 where
   "mclean_source_extends_flat_offset_action Omega chart normal t g F \<
      longleftrightarrow>
     (\<forall>phi. cgu_test_function_on Omega phi \<longrightarrow>
       F phi (cgu_classical_gradient phi) =
         mclean_flat_offset_action chart normal t g phi)"
112                            CĂTĂLIN I. CÂRSTEA

English mathematical translation
Mathematical role: representation of the translated source action
   Typed arguments/result: Omega :: ’n cgu point set, chart :: ’m cgu
point \<Rightarrow> ’n cgu point, normal :: ’n cgu point, t :: real, g
:: ’m cgu potential, F :: ’n mclean source, with ’m,’n::finite; result
bool. It holds exactly when for every phi :: ’n cgu potential, the hypoth-
esis cgu test function on Omega phi implies F phi (cgu classical gradient
phi) = mclean flat offset action chart normal t g phi.
mclean_flat_offset_cylinder_inside
Isabelle code
 definition mclean_flat_offset_cylinder_inside ::
   "’n::finite cgu_point set \<Rightarrow>
     (’m::finite cgu_point \<Rightarrow> ’n cgu_point) \<Rightarrow>
     ’n cgu_point \<Rightarrow> ’m cgu_potential \<Rightarrow> real \<Rightarrow>
      bool"
 where
   "mclean_flat_offset_cylinder_inside Omega chart normal g delta \<
      longleftrightarrow>
     {chart x + t *\<^sub>R normal |x t.
       x \<in> closure {y. g y \<noteq> 0} \<and> 0 \<le> t \<and> t \<le> delta}
       \<subseteq> Omega"

English mathematical translation
Mathematical role: support-tube condition
  Typed arguments/result: Omega :: ’n cgu point set, chart :: ’m cgu
point \<Rightarrow> ’n cgu point, normal :: ’n cgu point, g :: ’m cgu
potential, delta :: real, with ’m,’n::finite; result bool. It holds exactly
when every point of the form chart x + t *\<^sub>R normal, where x \<in>
closure {y. g y \<noteq>0} and 0\<le>t\<le>delta, belongs to Omega.
mclean_source_real_subspace
Isabelle code
 definition mclean_source_real_subspace ::
   "’n::finite mclean_source set \<Rightarrow> bool"
 where
   "mclean_source_real_subspace E \<longleftrightarrow>
     0 \<in> E \<and>
     (\<forall>F\<in>E. \<forall>G\<in>E. F + G \<in> E) \<and>
     (\<forall>r F. F \<in> E \<longrightarrow> r *\<^sub>R F \<in> E)"

English mathematical translation
Mathematical role: vector-operation closure of E
   Typed argument/result: E :: ’n mclean source set, with ’n::finite; result
bool. It holds exactly when 0 \<in> E, for every F \<in> E and G \<in> E one
has F+G \<in> E, and for every real scalar r and every F, the hypothesis F \<in>
E implies r *\<^sub>R F \<in> E.
mclean_source_linear_on
Isabelle code
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    113


 definition mclean_source_linear_on ::
   "’n::finite mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_source_linear_on E g \<longleftrightarrow>
     g 0 = 0 \<and>
     (\<forall>F\<in>E. \<forall>G\<in>E. g (F + G) = g F + g G) \<and>
     (\<forall>r F. F \<in> E \<longrightarrow> g (r *\<^sub>R F) = r * g F)"


English mathematical translation
Mathematical role: linear map on E
  Typed arguments/result: E :: ’n mclean source set, g :: ’n mclean
source \<Rightarrow> real, with ’n::finite; result bool. It holds exactly
when g 0=0; for every F,G \<in> E, g(F+G)=g F+g G; and for every r :: real
and F, the hypothesis F\<in>E implies g(r *\<^sub>R F)=r*g F.
mclean_source_seminorm_on
Isabelle code
 definition mclean_source_seminorm_on ::
   "’n::finite mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_source_seminorm_on E p \<longleftrightarrow>
     p 0 = 0 \<and>
     (\<forall>F\<in>E. 0 \<le> p F) \<and>
     (\<forall>F\<in>E. \<forall>G\<in>E. p (F + G) \<le> p F + p G) \<and>
     (\<forall>r F. F \<in> E \<longrightarrow> p (r *\<^sub>R F) = \<bar>r\<bar> *
       p F)"


English mathematical translation
Mathematical role: seminorm on E
  Typed arguments/result: E :: ’n mclean source set, p :: ’n mclean
source \<Rightarrow> real, with ’n::finite; result bool. It holds exactly
when p 0=0; for every F\<in>E, 0\<le>p F; for every F,G\<in>E, p(F+G)\<le>p
F+p G; and for every real r and F, the hypothesis F\<in>E implies p(r *\<^sub>R
F)=|r|*p F.
mclean_h1_zero_source_bidual_functional_on_v2
Isabelle code
 definition mclean_h1_zero_source_bidual_functional_on_v2 ::
   "’n::finite mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_h1_zero_source_bidual_functional_on_v2 E p g \<longleftrightarrow>
     mclean_source_linear_on E g \<and>
     (\<exists>C\<ge>0. \<forall>F\<in>E. \<bar>g F\<bar> \<le> C * p F)"


English mathematical translation
Mathematical role: p-dominated linear functional
114                            CĂTĂLIN I. CÂRSTEA

  Typed arguments/result: E :: ’n mclean source set, p,g :: ’n mclean
source \<Rightarrow> real, with ’n::finite; result bool. It holds exactly
when mclean source linear on E g and there exists C :: real restricted by
C\<ge>0 such that for every F\<in>E, |g F| \<le> C*p F.
mclean_h1_zero_bidual_realization_on_v2
Isabelle code

 definition mclean_h1_zero_bidual_realization_on_v2 ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_source set \<Rightarrow>
     (’n mclean_source \<Rightarrow> real) \<Rightarrow> bool"
 where
   "mclean_h1_zero_bidual_realization_on_v2 U E p \<longleftrightarrow>
     mclean_source_real_subspace E \<and>
     mclean_source_seminorm_on E p \<and>
     (\<forall>F. F \<in> E \<longleftrightarrow>
       (\<exists>K. mclean_source_bound_on U F K)) \<and>
     (\<forall>F\<in>E.
       mclean_source_bound_on U F (p F) \<and>
       (\<forall>K. mclean_source_bound_on U F K \<longrightarrow> p F \<le> K)) \<
      and>
     (\<forall>g.
       mclean_h1_zero_source_bidual_functional_on_v2 E p g
       \<longrightarrow>
       (\<exists>u Du.
         cgu_h1_zero_pair_on U u Du \<and>
         (\<forall>F\<in>E. g F = F u Du)))"


English mathematical translation
Mathematical role: total-functional representation package
   Typed arguments/result: U :: ’n cgu point set, E :: ’n mclean source
set, p :: ’n mclean source \<Rightarrow> real, with ’n::finite; result
bool.    It holds exactly when all of the following hold: mclean source
real subspace E; mclean source seminorm on E p; for every F :: ’n mclean
source, F\<in>E iff there exists K :: real with mclean source bound on U F
K; for every F\<in>E, both mclean source bound on U F (p F) and, for ev-
ery K, mclean source bound on U F K implies p F\<le>K; and for every g ::
’n mclean source \<Rightarrow> real, the hypothesis mclean h1 zero source
bidual functional on v2 E p g implies that there exist u :: ’n cgu potential
and Du :: ’n cgu gradient such that cgu h1 zero pair on U u Du and, for ev-
ery F\<in>E, g F=F u Du.
mclean_zero_extension_on
Isabelle code

 definition mclean_zero_extension_on ::
   "’n::finite cgu_point set \<Rightarrow> (’n cgu_point \<Rightarrow> ’a::zero) \<
      Rightarrow>
     ’n cgu_point \<Rightarrow> ’a"
 where
   "mclean_zero_extension_on U f x = (if x \<in> U then f x else 0)"


English mathematical translation
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    115

Mathematical role: zero extension ExtU
   Typed arguments/result:        U :: ’n cgu point set, f :: ’n cgu point
\<Rightarrow> ’a, x :: ’n cgu point, with ’n::finite and ’a::zero; result
’a. It equals f x if x\<in>U, and 0 otherwise.
ucp_point
Isabelle code

 type_synonym ’n ucp_point = "real ^ ’n"


English mathematical translation
Mathematical role: local Euclidean coordinate-space type
  For every type ’n, ’n ucp point is exactly real ^ ’n.
ucp_coefficient
Isabelle code

 type_synonym ’n ucp_coefficient =
   "’n ucp_point \<Rightarrow> (real ^ ’n ^ ’n)"


English mathematical translation
Mathematical role: local matrix-field function type
  For every type ’n, ’n ucp coefficient                is   exactly   ’n ucp point
\<Rightarrow> real ^ ’n ^ ’n.
ucp_symmetric_matrix
Isabelle code

 definition ucp_symmetric_matrix ::
   "(real ^ ’n::finite ^ ’n) \<Rightarrow> bool"
 where
   "ucp_symmetric_matrix A \<longleftrightarrow> transpose A = A"


English mathematical translation
Mathematical role: pointwise matrix symmetry
   Typed argument/result: A :: real ^ ’n ^ ’n, with ’n::finite; result bool.
It holds exactly when transpose A=A.
ucp_matrix_polynomial
Isabelle code

 definition ucp_matrix_polynomial ::
   "’n::finite ucp_coefficient \<Rightarrow> bool"
 where
   "ucp_matrix_polynomial P \<longleftrightarrow>
     (\<forall>i j. polynomial_function (\<lambda>x. P x $ i $ j))"


English mathematical translation
Mathematical role: entrywise-polynomial matrix field
116                            CĂTĂLIN I. CÂRSTEA

   Typed argument/result: P :: ’n ucp coefficient, with ’n::finite; re-
sult bool. It holds exactly when for all i,j :: ’n, polynomial function
(\<lambda>x. P x $ i $ j).
ucp_uniformly_elliptic_near
Isabelle code
 definition ucp_uniformly_elliptic_near ::
   "’n::finite ucp_point set \<Rightarrow> ’n ucp_coefficient \<Rightarrow> bool"
 where
   "ucp_uniformly_elliptic_near E P \<longleftrightarrow>
     (\<exists>V k. open V \<and> closure E \<subseteq> V \<and> 0 < k \<and>
       (\<forall>x\<in>V. \<forall>xi. k * norm xi ^ 2 \<le> inner xi (P x *v xi)))"



English mathematical translation
Mathematical role: ellipticity on a neighborhood of E
   Typed arguments/result: E :: ’n ucp point set, P :: ’n ucp coefficient,
with ’n::finite; result bool. It holds exactly when there exist V :: ’n ucp
point set and k :: real such that open V, closure E \<subseteq> V, 0<k, and
for every x\<in>V and every xi :: ’n ucp point, k*norm xi^2 \<le> inner xi
(P x *v xi).
ucp_partial_derivative
Isabelle code
 definition ucp_partial_derivative ::
   "(’n::finite ucp_point \<Rightarrow> real) \<Rightarrow> ’n \<Rightarrow>
    ’n ucp_point \<Rightarrow> real"
 where
   "ucp_partial_derivative phi i x =
     frechet_derivative phi (at x) (axis i 1)"

English mathematical translation
Mathematical role: local selected coordinate derivative
   Typed arguments/result: phi :: ’n ucp point \<Rightarrow> real, i ::
’n, x :: ’n ucp point, with ’n::finite; result real. It equals frechet
derivative phi (at x) (axis i 1).
ucp_test_function_on
Isabelle code
 definition ucp_test_function_on ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow> bool"
 where
   "ucp_test_function_on G phi \<longleftrightarrow>
     smooth_on UNIV phi \<and>
     compact (closure {x. phi x \<noteq> 0}) \<and>
     closure {x. phi x \<noteq> 0} \<subseteq> G"

English mathematical translation
Mathematical role: local test-function predicate
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    117

  Typed arguments/result: G :: ’n ucp point set, phi :: ’n ucp point
\<Rightarrow> real, with ’n::finite; result bool. It holds exactly when
smooth on UNIV phi, compact (closure {x. phi x \<noteq>0}), and closure
{x. phi x \<noteq>0} \<subseteq> G.
ucp_locally_square_integrable_on
Isabelle code
 definition ucp_locally_square_integrable_on ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> ’a::euclidean_space) \<Rightarrow> bool"
 where
   "ucp_locally_square_integrable_on G f \<longleftrightarrow>
     (\<forall>K. compact K \<and> K \<subseteq> G \<longrightarrow>
       set_integrable lborel K (\<lambda>x. norm (f x) ^ 2))"


English mathematical translation
Mathematical role: stipulated local square integrability
   Typed arguments/result:        G :: ’n ucp point set, f :: ’n ucp point
\<Rightarrow> ’a, with ’n::finite and ’a::euclidean space; result bool. It
holds exactly when, for every K :: ’n ucp point set, the hypotheses compact K
and K\<subseteq>G imply that x \<mapsto> norm (f x)^2 is set-integrable with
respect to lborel on K.
ucp_weak_gradient_on
Isabelle code
 definition ucp_weak_gradient_on ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow>
    (’n ucp_point \<Rightarrow> ’n ucp_point) \<Rightarrow> bool"
 where
   "ucp_weak_gradient_on G u Du \<longleftrightarrow>
     (\<forall>phi. ucp_test_function_on G phi \<longrightarrow>
       (\<forall>i.
         set_integrable lborel G
           (\<lambda>x. u x * ucp_partial_derivative phi i x) \<and>
         set_integrable lborel G (\<lambda>x. Du x $ i * phi x) \<and>
         set_lebesgue_integral lborel G
           (\<lambda>x. u x * ucp_partial_derivative phi i x) =
         - set_lebesgue_integral lborel G (\<lambda>x. Du x $ i * phi x)))"


English mathematical translation
Mathematical role: local weak-gradient relation
   Typed arguments/result:        G :: ’n ucp point set, u :: ’n ucp point
\<Rightarrow> real, Du :: ’n ucp point \<Rightarrow> ’n ucp point, with
’n::finite; result bool. It holds exactly when, for every phi, the hypothesis
ucp test function on G phi implies that for every i :: ’n: both x \<mapsto>
u x*ucp partial derivative phi i x and x \<mapsto> Du x $ i*phi x are
set-integrable on G, and their set Lebesgue integrals satisfy integral G (u*ucp
partial derivative phi i) = - integral G ((Du coordinate i)*phi).
ucp_test_gradient
118                            CĂTĂLIN I. CÂRSTEA

Isabelle code

 definition ucp_test_gradient ::
   "(’n::finite ucp_point \<Rightarrow> real) \<Rightarrow>
    ’n ucp_point \<Rightarrow> ’n ucp_point"
 where
   "ucp_test_gradient phi x =
     (\<chi> i. ucp_partial_derivative phi i x)"


English mathematical translation
Mathematical role: local gradient vector
   Typed arguments/result: phi :: ’n ucp point \<Rightarrow> real, x ::
’n ucp point, with ’n::finite; result ’n ucp point. It is the indexed vector
\<chi> i. ucp partial derivative phi i x, for i :: ’n.
ucp_weak_solution_on
Isabelle code

 definition ucp_weak_solution_on ::
   "’n::finite ucp_point set \<Rightarrow> ’n ucp_coefficient \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow> bool"
 where
   "ucp_weak_solution_on G a0 u \<longleftrightarrow>
     (\<exists>Du.
       ucp_locally_square_integrable_on G u \<and>
       ucp_locally_square_integrable_on G Du \<and>
       ucp_weak_gradient_on G u Du \<and>
       (\<forall>phi. ucp_test_function_on G phi \<longrightarrow>
         set_integrable lborel G
           (\<lambda>x. inner (a0 x *v Du x) (ucp_test_gradient phi x)) \<and>
         set_lebesgue_integral lborel G
           (\<lambda>x. inner (a0 x *v Du x) (ucp_test_gradient phi x)) = 0))"


English mathematical translation
Mathematical role: local weak solution for a matrix field
   Typed     arguments/result:        G :: ’n ucp point set,     a0 :: ’n ucp
coefficient, u :: ’n ucp point \<Rightarrow> real, with ’n::finite; re-
sult bool. It holds exactly when there exists Du :: ’n ucp point \<Rightarrow>
’n ucp point such that ucp locally square integrable on G u, ucp locally
square integrable on G Du, ucp weak gradient on G u Du, and for every phi,
the hypothesis ucp test function on G phi implies both set-integrability on G of
x \<mapsto> inner (a0 x *v Du x) (ucp test gradient phi x) and equality
of that function’s set Lebesgue integral to 0.
hormander_regular_distribution_test_zero_on
Isabelle code
 definition hormander_regular_distribution_test_zero_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n cgu_potential \<Rightarrow> bool"
 where
   "hormander_regular_distribution_test_zero_on X u \<longleftrightarrow>
     set_integrable lborel X u \<and>
     (\<forall>phi. cgu_test_function_on X phi \<longrightarrow>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    119

       set_integrable lborel X (\<lambda>x. u x * phi x) \<and>
       set_lebesgue_integral lborel X (\<lambda>x. u x * phi x) = 0)"


English mathematical translation
Mathematical role: zero-test property
   Typed arguments/result: X :: ’n cgu point set, u :: ’n cgu potential,
with ’n::finite; result bool. It holds exactly when u is set-integrable with respect
to lborel on X, and for every phi, the hypothesis cgu test function on X phi
implies both set-integrability on X of x \<mapsto> u x*phi x and equality of that
function’s set Lebesgue integral to 0.
evans_bounded_domain
Isabelle code

 definition evans_bounded_domain ::
   "’n::finite cgu_point set \<Rightarrow> bool"
 where
   "evans_bounded_domain U \<longleftrightarrow> bounded U"


English mathematical translation
Mathematical role: boundedness predicate
  Typed argument/result: U :: ’n cgu point set, with ’n::finite; result
bool. It holds exactly when bounded U.
evans_elliptic_coefficient_on
Isabelle code

 definition evans_elliptic_coefficient_on ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "evans_elliptic_coefficient_on U a \<longleftrightarrow>
     a \<in> borel_measurable (restrict_space lborel U) \<and>
     (\<exists>B\<ge>0. \<forall>x\<in>U. norm (a x) \<le> B) \<and>
     (\<forall>x\<in>U. transpose (a x) = a x) \<and>
     (\<exists>theta>0. \<forall>x\<in>U. \<forall>xi.
       theta * norm xi ^ 2 \<le> inner (a x *v xi) xi)"


English mathematical translation
Mathematical role: bounded symmetric uniformly elliptic measurable field
   Typed arguments/result:        U :: ’n cgu point set,      a :: ’n mclean
coefficient, with ’n::finite; result bool. It holds exactly when: a \<in>
borel measurable (restrict space lborel U); there exists B :: real re-
stricted by B\<ge>0 such that for every x\<in>U, norm(a x)\<le>B; for every
x\<in>U, transpose(a x)=a x; and there exists theta :: real restricted by
theta>0 such that for every x\<in>U and every xi :: ’n cgu point, theta*norm
xi^2 \<le> inner (a x *v xi) xi.
evans_poincare_elliptic_green
Isabelle code
120                            CĂTĂLIN I. CÂRSTEA


 locale evans_poincare_elliptic_green =
   fixes dimension_type :: "’n::finite itself"
   assumes evans_poincare_elliptic_green:
     "\<forall>U a. evans_poincare_elliptic_green_claim
       (U :: ’n cgu_point set) a"


English mathematical translation
Mathematical role: Atomic universally quantified assumption on typed sets.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale evans poincare elliptic green postulates the assump-
tion named evans poincare elliptic green: for every U and every a,
   evans poincare elliptic green claim (U :: ’n cgu point set) a
   holds. The annotation requires U to be a set of objects of type ’n cgu point;
both U and a lie within the scope of the universal quantifier. The fixed token remains
part of the locale even though it is not an explicit argument of this proposition.
mclean_smooth_test_h1_zero
Isabelle code
 locale mclean_smooth_test_h1_zero =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_smooth_test_h1_zero:
     "mclean_smooth_test_h1_zero_claim dimension_type"


English mathematical translation
Mathematical role: Atomic assumption parameterized by a finite carrier token.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale mclean smooth test h1 zero postulates the assumption
named mclean smooth test h1 zero:
   mclean smooth test h1 zero claim dimension type.
hormander_analytic_elliptic_ucp
Isabelle code
 locale hormander_analytic_elliptic_ucp =
   fixes dimension_type :: "’n::finite itself"
   assumes hormander_analytic_elliptic_ucp:
     "\<forall>X P u.
       hormander_analytic_elliptic_ucp_claim
         (X :: ’n ucp_point set) P u"


English mathematical translation
Mathematical role: Atomic universally quantified analytic assumption.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale hormander analytic elliptic ucp postulates the as-
sumption named hormander analytic elliptic ucp: for every X, every P, and
every u,
   hormander analytic elliptic ucp claim (X :: ’n ucp point set) P u
   holds. The annotation requires X to be a set of objects of type ’n ucp point,
and all three displayed variables lie within the universal quantifier’s scope. The
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    121

fixed token remains part of the locale even though it is not an explicit argument of
this proposition.
hormander_weak_gradient_locality
Isabelle code
 locale hormander_weak_gradient_locality =
   fixes dimension_type :: "’n::finite itself"
   assumes hormander_weak_gradient_locality:
     "\<forall>X u Du.
       hormander_weak_gradient_locality_claim
         (X :: ’n ucp_point set) u Du"

English mathematical translation
Mathematical role: Atomic universally quantified locality assumption.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale hormander weak gradient locality postulates the as-
sumption named hormander weak gradient locality: for every X, every u, and
every Du,
   hormander weak gradient locality claim (X :: ’n ucp point set) u Du
   holds. The annotation requires X to be a set of objects of type ’n ucp point,
and all three displayed variables lie within the universal quantifier’s scope. The
fixed token remains part of the locale even though it is not an explicit argument of
this proposition.
mclean_h1_zero_extension_localization
Isabelle code
 locale mclean_h1_zero_extension_localization =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_h1_zero_extension_localization:
     "mclean_h1_zero_extension_localization_claim dimension_type"

English mathematical translation
Mathematical role: Atomic localization assumption parameterized by a finite carrier
token.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale mclean h1 zero extension localization postulates the
assumption named mclean h1 zero extension localization:
   mclean h1 zero extension localization claim dimension type.
mclean_trace_dirichlet_green_v3
Isabelle code
 locale mclean_trace_dirichlet_green_v3 =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_trace_dirichlet_green_v3:
     "\<forall>U a. mclean_trace_dirichlet_green_claim_v3
       (U :: ’n cgu_point set) a"

English mathematical translation
Mathematical role: Atomic universally quantified trace assumption on typed sets.
122                            CĂTĂLIN I. CÂRSTEA

   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale mclean trace dirichlet green v3 postulates the assump-
tion named mclean trace dirichlet green v3: for every U and every a,
   mclean trace dirichlet green claim v3 (U :: ’n cgu point set) a
   holds. The annotation requires U to be a set of objects of type ’n cgu point;
both U and a lie within the scope of the universal quantifier. The fixed token remains
part of the locale even though it is not an explicit argument of this proposition.
hormander_regular_distribution_injectivity
Isabelle code
 locale hormander_regular_distribution_injectivity =
   fixes dimension_type :: "’n::finite itself"
   assumes hormander_regular_distribution_injectivity:
     "hormander_regular_distribution_injectivity_claim dimension_type"


English mathematical translation
Mathematical role: Atomic injectivity assumption parameterized by a finite carrier
token.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale hormander regular distribution injectivity postu-
lates the assumption named hormander regular distribution injectivity:
   hormander regular distribution injectivity claim dimension type.
mclean_graph_supported_h1_zero
Isabelle code
 locale mclean_graph_supported_h1_zero =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_graph_supported_h1_zero:
     "mclean_graph_supported_h1_zero_claim dimension_type"


English mathematical translation
Mathematical role: Atomic graph-support assumption parameterized by a finite
carrier token.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale mclean graph supported h1 zero postulates the assump-
tion named mclean graph supported h1 zero:
   mclean graph supported h1 zero claim dimension type.
mclean_h1_zero_bidual_representation_v2
Isabelle code
 locale mclean_h1_zero_bidual_representation_v2 =
   fixes dimension_type :: "’n::finite itself"
   assumes mclean_h1_zero_bidual_representation_v2:
     "mclean_h1_zero_bidual_representation_claim_v2 dimension_type"


English mathematical translation
Mathematical role: Atomic bidual assumption parameterized by a finite carrier
token.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    123

   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale mclean h1 zero bidual representation v2 postulates
the assumption named mclean h1 zero bidual representation v2:
   mclean h1 zero bidual representation claim v2 dimension type.
mclean_smooth_generator_ambient_lift_v2
Isabelle code

 locale mclean_smooth_generator_ambient_lift_v2 =
   assumes mclean_smooth_generator_ambient_lift_v2:
     "mclean_smooth_generator_ambient_lift_claim_v2
       TYPE(’n::finite) TYPE(’c::finite) TYPE(’h::finite)"


English mathematical translation
Mathematical role: Atomic ordered three-carrier assumption.
   The locale mclean smooth generator ambient lift v2 postulates the assump-
tion named mclean smooth generator ambient lift v2:
   mclean smooth generator ambient lift claim v2 TYPE(’n::finite)
TYPE(’c::finite) TYPE(’h::finite).
   The three arguments, in precisely that order, are the selected finite carrier types
’n, ’c, and ’h. No numerical dimension or further mathematical property is as-
signed to any of them.
mclean_hyperplane_offset_source
Isabelle code

 locale mclean_hyperplane_offset_source =
   assumes mclean_hyperplane_offset_source:
     "mclean_hyperplane_offset_source_claim
       TYPE(’m::finite) TYPE(’n::finite)"


English mathematical translation
Mathematical role: Atomic ordered two-carrier offset assumption.
   The locale mclean hyperplane offset source postulates the assumption
named mclean hyperplane offset source:
   mclean hyperplane offset source claim TYPE(’m::finite)
TYPE(’n::finite).
   The two arguments, in precisely that order, are the selected finite carrier types
’m and ’n. No numerical dimension or further mathematical property is assigned
to either of them.
kang_yun_ltu_local_boundary_metric_v6
Isabelle code

 locale kang_yun_ltu_local_boundary_metric_v6 =
   fixes dimension_type :: "’n::finite itself"
   assumes kang_yun_ltu_local_boundary_metric_v6:
     "\<forall>M P1 P2 U gamma normal offset g1 g2 a1 a2 rho1 rho2.
       kang_yun_ltu_local_boundary_metric_claim_v6
         (M :: (’n, ’c::finite, ’h::finite) cgu_model)
         P1 P2 U gamma normal offset g1 g2 a1 a2 rho1 rho2"
124                             CĂTĂLIN I. CÂRSTEA

English mathematical translation
Mathematical role: Atomic fully quantified boundary-metric assumption with a
typed leading argument.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale kang yun ltu local boundary metric v6 postulates the
assumption named kang yun ltu local boundary metric v6: for every M, every
P1, every P2, every U, every gamma, every normal, every offset, every g1, every
g2, every a1, every a2, every rho1, and every rho2,
   kang yun ltu local boundary metric claim v6 (M :: (’n, ’c::finite,
’h::finite) cgu model) P1 P2 U gamma normal offset g1 g2 a1 a2 rho1
rho2
   holds. The annotation requires M to have type (’n, ’c::finite, ’h::finite)
cgu model; the finite type-class constraints on ’n, ’c, and ’h, the order of all thir-
teen arguments, and the scope of the universal quantifier are exactly as displayed.
The fixed token remains part of the locale even though it is not an explicit argument
of this proposition.
piecewise_polynomial_ucp_literature
Isabelle code

 locale piecewise_polynomial_ucp_literature =
   analytic: hormander_analytic_elliptic_ucp dimension_type +
   locality: hormander_weak_gradient_locality dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Conjunction of named analytic and locality packages.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale piecewise polynomial ucp literature is the conjunction
of the named parents analytic: hormander analytic elliptic ucp dimension
type and locality: hormander weak gradient locality dimension type. Its
complete assumptions are:
       • analytic.hormander analytic elliptic ucp: for every X, every P, and
         every u, hormander analytic elliptic ucp claim (X :: ’n ucp point
         set) P u holds.
       • locality.hormander weak gradient locality:        for every X, every
         u, and every Du, hormander weak gradient locality claim (X :: ’n
         ucp point set) u Du holds.

cgu_volume_annihilator_literature_base
Isabelle code

 locale cgu_volume_annihilator_literature_base =
   smooth: mclean_smooth_test_h1_zero dimension_type +
   injectivity: hormander_regular_distribution_injectivity dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Conjunction of named smoothness and injectivity packages.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    125

   Fix dimension type :: "’n::finite itself", a token selecting the fi-
nite carrier type ’n.     The locale cgu volume annihilator literature
base is the conjunction of the named parents smooth: mclean smooth test
h1 zero dimension type and injectivity: hormander regular distribution
injectivity dimension type. Its complete assumptions are:
      • smooth.mclean smooth test h1 zero:    mclean smooth test h1 zero
        claim dimension type holds.
      • injectivity.hormander regular distribution injectivity:
        hormander regular distribution injectivity claim dimension
        type holds.
cgu_volume_gradient_annihilator_literature_base
Isabelle code
 locale cgu_volume_gradient_annihilator_literature_base =
   volume: cgu_volume_annihilator_literature_base dimension_type +
   locality: hormander_weak_gradient_locality dimension_type
   for dimension_type :: "’n::finite itself"

English mathematical translation
Mathematical role: Conjunction of named volume and locality packages.
   Fix dimension type :: "’n::finite itself", a token selecting the finite
carrier type ’n. The locale cgu volume gradient annihilator literature
base is the conjunction of the named parents volume: cgu volume annihilator
literature base dimension type and locality: hormander weak gradient
locality dimension type. Its complete inherited assumptions are:
       • volume.smooth: mclean smooth test h1 zero:      mclean smooth test
         h1 zero claim dimension type holds.
       • volume.injectivity: hormander regular distribution injectivity:
         hormander regular distribution injectivity claim dimension type
         holds.
       • locality.hormander weak gradient locality:       for every X, every
         u, and every Du, hormander weak gradient locality claim (X :: ’n
         ucp point set) u Du holds.
cgu_graph_interface_annihilator_literature_base
Isabelle code
 locale cgu_graph_interface_annihilator_literature_base =
   volume_gradient: cgu_volume_gradient_annihilator_literature_base dimension_type +

   localization: mclean_h1_zero_extension_localization dimension_type +
   graph_support: mclean_graph_supported_h1_zero dimension_type
   for dimension_type :: "’n::finite itself"

English mathematical translation
Mathematical role: Conjunction of volume-gradient, localization, and graph-
support packages.
   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale cgu graph interface annihilator literature base is
126                            CĂTĂLIN I. CÂRSTEA

the conjunction of the named parents volume gradient: cgu volume gradient
annihilator literature base dimension type,       localization: mclean h1
zero extension localization dimension type, and graph support: mclean
graph supported h1 zero dimension type. Its complete inherited assumptions
are:
      • volume gradient.volume.smooth: mclean smooth test h1 zero:
        mclean smooth test h1 zero claim dimension type holds.
      • volume gradient.volume.injectivity: hormander regular
        distribution injectivity:         hormander regular distribution
        injectivity claim dimension type holds.
      • volume gradient.locality: hormander weak gradient locality: for
        every X, every u, and every Du, hormander weak gradient locality
        claim (X :: ’n ucp point set) u Du holds.
      • localization.mclean h1 zero extension localization: mclean h1
        zero extension localization claim dimension type holds.
      • graph support.mclean graph supported h1 zero:       mclean graph
        supported h1 zero claim dimension type holds.

cgu_graph_interface_source_approximation_literature_base

Isabelle code

 locale cgu_graph_interface_source_approximation_literature_base =
   annihilator: cgu_graph_interface_annihilator_literature_base dimension_type +
   bidual: mclean_h1_zero_bidual_representation_v2 dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Conjunction of named annihilator and bidual packages.
   Fix dimension type :: "’n::finite itself", a token selecting the finite
carrier type ’n.    The locale cgu graph interface source approximation
literature base is the conjunction of the named parents annihilator: cgu
graph interface annihilator literature base dimension type and bidual:
mclean h1 zero bidual representation v2 dimension type.
   The complete annihilator package is:
      • annihilator.volume gradient.volume.smooth: mclean smooth test
        h1 zero: mclean smooth test h1 zero claim dimension type holds.
      • annihilator.volume gradient.volume.injectivity: hormander
        regular distribution injectivity:                   hormander regular
        distribution injectivity claim dimension type holds.
      • annihilator.volume gradient.locality: hormander weak gradient
        locality: for every X, every u, and every Du, hormander weak gradient
        locality claim (X :: ’n ucp point set) u Du holds.
      • annihilator.localization: mclean h1 zero extension
        localization:           mclean h1 zero extension localization claim
        dimension type holds.
      • annihilator.graph support: mclean graph supported h1 zero:
        mclean graph supported h1 zero claim dimension type holds.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    127

  The conjoined bidual package contributes bidual.mclean h1 zero bidual
representation v2:        mclean h1 zero bidual representation claim v2
dimension type holds.

cgu_runge_literature_base

Isabelle code

 locale cgu_runge_literature_base =
   evans: evans_poincare_elliptic_green dimension_type +
   smooth: mclean_smooth_test_h1_zero dimension_type +
   ucp: piecewise_polynomial_ucp_literature dimension_type +
   localization: mclean_h1_zero_extension_localization dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Four-way conjunction of base, smoothness, UCP, and localiza-
tion packages.
   Fix dimension type :: "’n::finite itself", a token selecting the finite
carrier type ’n. The locale cgu runge literature base is the conjunction
of four named parent components: evans: evans poincare elliptic green
dimension type, smooth: mclean smooth test h1 zero dimension type, ucp:
piecewise polynomial ucp literature dimension type, and localization:
mclean h1 zero extension localization dimension type.
   Their complete assumption packages are:
      • evans.evans poincare elliptic green: for every U and every a, evans
        poincare elliptic green claim (U :: ’n cgu point set) a holds.
      • smooth.mclean smooth test h1 zero:    mclean smooth test h1 zero
        claim dimension type holds.
      • ucp.analytic.hormander analytic elliptic ucp: for every X, every P,
        and every u, hormander analytic elliptic ucp claim (X :: ’n ucp
        point set) P u holds.
      • ucp.locality.hormander weak gradient locality: for every X, every
        u, and every Du, hormander weak gradient locality claim (X :: ’n
        ucp point set) u Du holds.
      • localization.mclean h1 zero extension localization: mclean h1
        zero extension localization claim dimension type holds.

cgu_graph_dirichlet_literature_base_v3

Isabelle code

 locale cgu_graph_dirichlet_literature_base_v3 =
   cgu_runge_literature_base dimension_type +
   trace: mclean_trace_dirichlet_green_v3 dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Conjunction of the core package and a named trace assumption.
128                            CĂTĂLIN I. CÂRSTEA

   Fix dimension type :: "’n::finite itself", a token selecting the finite car-
rier type ’n. The locale cgu graph dirichlet literature base v3 is the conjunc-
tion of the unnamed parent cgu runge literature base dimension type and the
named component trace: mclean trace dirichlet green v3 dimension type.
   The complete inherited assumptions are:
       • evans: evans poincare elliptic green: for every U and every a, evans
         poincare elliptic green claim (U :: ’n cgu point set) a holds.
       • smooth: mclean smooth test h1 zero: mclean smooth test h1 zero
         claim dimension type holds.
       • ucp.analytic: hormander analytic elliptic ucp: for every X, every P,
         and every u, hormander analytic elliptic ucp claim (X :: ’n ucp
         point set) P u holds.
       • ucp.locality: hormander weak gradient locality: for every X, every
         u, and every Du, hormander weak gradient locality claim (X :: ’n
         ucp point set) u Du holds.
       • localization: mclean h1 zero extension localization: mclean h1
         zero extension localization claim dimension type holds.
       • trace.mclean trace dirichlet green v3:     for every U and every
         a, mclean trace dirichlet green claim v3 (U :: ’n cgu point set)
         a holds.
cgu_graph_interface_conormal_context
Isabelle code
 locale cgu_graph_interface_conormal_context =
   cgu_graph_dirichlet_literature_base_v3 dimension_type +
   graph_source: cgu_graph_interface_source_approximation_literature_base
      dimension_type
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Conjunction of the base analytic package and a named graph-
source package.
   Fix dimension type :: "’n::finite itself", a token selecting the fi-
nite carrier type ’n.    The locale cgu graph interface conormal context
is the conjunction of the unnamed parent cgu graph dirichlet literature
base v3 dimension type and the named component graph source: cgu graph
interface source approximation literature base dimension type.
   The unnamed cgu graph dirichlet literature base v3 package contributes:
      • evans: evans poincare elliptic green: for every U and every a, evans
        poincare elliptic green claim (U :: ’n cgu point set) a holds.
      • smooth: mclean smooth test h1 zero: mclean smooth test h1 zero
        claim dimension type holds.
      • ucp.analytic: hormander analytic elliptic ucp: for every X, every P,
        and every u, hormander analytic elliptic ucp claim (X :: ’n ucp
        point set) P u holds.
      • ucp.locality: hormander weak gradient locality: for every X, every
        u, and every Du, hormander weak gradient locality claim (X :: ’n
        ucp point set) u Du holds.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    129

      • localization: mclean h1 zero extension localization: mclean h1
        zero extension localization claim dimension type holds.
      • trace: mclean trace dirichlet green v3: for every U and every
        a, mclean trace dirichlet green claim v3 (U :: ’n cgu point set)
        a holds.
  The named graph source package contributes:
      • graph source.annihilator.volume gradient.volume.smooth:
        mclean smooth test h1 zero:       mclean smooth test h1 zero claim
        dimension type holds.
      • graph source.annihilator.volume gradient.volume.injectivity:
        hormander regular distribution injectivity: hormander regular
        distribution injectivity claim dimension type holds.
      • graph source.annihilator.volume gradient.locality: hormander
        weak gradient locality: for every X, every u, and every Du, hormander
        weak gradient locality claim (X :: ’n ucp point set) u Du holds.
      • graph source.annihilator.localization: mclean h1 zero
        extension localization: mclean h1 zero extension localization
        claim dimension type holds.
      • graph source.annihilator.graph support: mclean graph supported
        h1 zero:     mclean graph supported h1 zero claim dimension type
        holds.
      • graph source.bidual: mclean h1 zero bidual representation v2:
        mclean h1 zero bidual representation claim v2 dimension type
        holds.

cgu_selected_face_dn_context
Isabelle code

 locale cgu_selected_face_dn_context =
   cgu_graph_interface_conormal_context dimension_type +
   mclean_smooth_generator_ambient_lift_v2
   for dimension_type :: "’n::finite itself"


English mathematical translation
Mathematical role: Conjunction of the main dimension-token package and a three-
carrier assumption.
   Fix dimension type :: "’n::finite itself"; this is a token selecting the fi-
nite carrier type ’n, not a claim about its numerical dimension. The locale cgu
selected face dn context is the conjunction of the unnamed parents cgu graph
interface conormal context dimension type and mclean smooth generator
ambient lift v2.
   The complete package inherited from cgu graph interface conormal context
dimension type is:
      • evans: evans poincare elliptic green: for every U and every a, evans
        poincare elliptic green claim (U :: ’n cgu point set) a holds.
      • smooth: mclean smooth test h1 zero: mclean smooth test h1 zero
        claim dimension type holds.
130                            CĂTĂLIN I. CÂRSTEA

       • ucp.analytic: hormander analytic elliptic ucp: for every X, every P,
         and every u, hormander analytic elliptic ucp claim (X :: ’n ucp
         point set) P u holds.
       • ucp.locality: hormander weak gradient locality: for every X, every
         u, and every Du, hormander weak gradient locality claim (X :: ’n
         ucp point set) u Du holds.
       • localization: mclean h1 zero extension localization: mclean h1
         zero extension localization claim dimension type holds.
       • trace: mclean trace dirichlet green v3: for every U and every
         a, mclean trace dirichlet green claim v3 (U :: ’n cgu point set)
         a holds.
       • graph source.annihilator.volume gradient.volume.smooth:
         mclean smooth test h1 zero:            mclean smooth test h1 zero claim
         dimension type holds.
       • graph source.annihilator.volume gradient.volume.injectivity:
         hormander regular distribution injectivity: hormander regular
         distribution injectivity claim dimension type holds.
       • graph source.annihilator.volume gradient.locality: hormander
         weak gradient locality: for every X, every u, and every Du, hormander
         weak gradient locality claim (X :: ’n ucp point set) u Du holds.
       • graph source.annihilator.localization: mclean h1 zero
         extension localization: mclean h1 zero extension localization
         claim dimension type holds.
       • graph source.annihilator.graph support: mclean graph supported
         h1 zero:        mclean graph supported h1 zero claim dimension type
         holds.
       • graph source.bidual: mclean h1 zero bidual representation v2:
         mclean h1 zero bidual representation claim v2 dimension type
         holds.
   The conjoined mclean smooth generator ambient lift v2 package ad-
ditionally      postulates      mclean smooth generator ambient lift claim v2
TYPE(’n::finite) TYPE(’c::finite) TYPE(’h::finite), with the three
selected finite carrier types in exactly this order and with no assigned numerical
dimensions.
cgu_terminal_recovery_context_v7
Isabelle code

 locale cgu_terminal_recovery_context_v7 =
   cgu_selected_face_dn_context "TYPE(’n::finite)" +
   offset: mclean_hyperplane_offset_source +
   boundary_metric: kang_yun_ltu_local_boundary_metric_v6 "TYPE(’n)"


English mathematical translation
Mathematical role: Top-level conjunction of the complete anonymous hypothesis
package, an offset package, and a boundary-metric package.
   The locale cgu terminal recovery context v7 is the conjunction of
three parent locales: the unnamed parent cgu selected face dn context
"TYPE(’n::finite)", the named component offset: mclean hyperplane
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    131

offset source, and the named component boundary metric: kang yun ltu
local boundary metric v6 "TYPE(’n)". Here TYPE(’n::finite) is only the se-
lected finite carrier type passed to cgu selected face dn context, and TYPE(’n)
is that carrier token passed to boundary metric; no numerical dimension is
asserted.
   The complete inherited package is as follows. In the cgu selected face dn
context component, its fixed token dimension type :: "’n::finite itself" is
instantiated by TYPE(’n::finite), and the component is itself the conjunction of
cgu graph interface conormal context dimension type and mclean smooth
generator ambient lift v2. The cgu graph interface conormal context part
contributes all of these assumptions, with the displayed prefix paths retained:

     • evans: evans poincare elliptic green: for every U and every a, evans
       poincare elliptic green claim (U :: ’n cgu point set) a holds.
     • smooth: mclean smooth test h1 zero: mclean smooth test h1 zero
       claim TYPE(’n::finite) holds.
     • ucp.analytic: hormander analytic elliptic ucp: for every X, every P,
       and every u, hormander analytic elliptic ucp claim (X :: ’n ucp
       point set) P u holds.
     • ucp.locality: hormander weak gradient locality: for every X, every
       u, and every Du, hormander weak gradient locality claim (X :: ’n
       ucp point set) u Du holds.
     • localization: mclean h1 zero extension localization: mclean h1
       zero extension localization claim TYPE(’n::finite) holds.
     • trace: mclean trace dirichlet green v3: for every U and every
       a, mclean trace dirichlet green claim v3 (U :: ’n cgu point set)
       a holds.
     • graph source.annihilator.volume gradient.volume.smooth:
       mclean smooth test h1 zero:       mclean smooth test h1 zero claim
       TYPE(’n::finite) holds.
     • graph source.annihilator.volume gradient.volume.injectivity:
       hormander regular distribution injectivity: hormander regular
       distribution injectivity claim TYPE(’n::finite) holds.
     • graph source.annihilator.volume gradient.locality: hormander
       weak gradient locality: for every X, every u, and every Du, hormander
       weak gradient locality claim (X :: ’n ucp point set) u Du holds.
     • graph source.annihilator.localization: mclean h1 zero
       extension localization: mclean h1 zero extension localization
       claim TYPE(’n::finite) holds.
     • graph source.annihilator.graph support: mclean graph supported
       h1 zero:   mclean graph supported h1 zero claim TYPE(’n::finite)
       holds.
     • graph source.bidual: mclean h1 zero bidual representation v2:
       mclean h1 zero bidual representation claim v2 TYPE(’n::finite)
       holds.

   The accompanying mclean smooth generator ambient lift v2 part pos-
tulates mclean smooth generator ambient lift claim v2 TYPE(’n::finite)
132                           CĂTĂLIN I. CÂRSTEA

TYPE(’c::finite) TYPE(’h::finite), where each TYPE(...) expression de-
notes only its selected finite carrier type and the arguments occur in exactly the
displayed order.
   The named offset component contributes offset.mclean hyperplane
offset source: mclean hyperplane offset source claim TYPE(’m::finite)
TYPE(’n::finite) holds, with these two selected finite carrier types in that
order. The named boundary metric component fixes its dimension type ::
"’n::finite itself" at TYPE(’n) and contributes boundary metric.kang yun
ltu local boundary metric v6: for every M, P1, P2, U, gamma, normal, offset, g1,
g2, a1, a2, rho1, and rho2,
   kang yun ltu local boundary metric claim v6 (M :: (’n, ’c::finite,
’h::finite) cgu model) P1 P2 U gamma normal offset g1 g2 a1 a2 rho1
rho2
   holds, with exactly this type annotation, argument order, and quantifier scope.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    133

Statements

Manuscript conclusions
MAIN-001: cgu_global_uniqueness_claim_v7
English original and manuscript locator
    Theorem thm:main of [1] states:
    Let n ≥ 3, let Ω ⊂ Rn be a bounded Lipschitz domain, and let D = {Dα }α∈A
be a known finite Lipschitz subdivision of Ω that is internally flat up to a skeleton.
Let Nα ≥ 0. Suppose that σ (1) , σ (2) ∈ P(D, {Nα }), and assume that, at every
recovery step and for j = 1, 2, the polynomial extension of σ (j) |Dαr is positive
definite on the triple-intersection sets Wr,ijk appearing in Definition [source refer-
ence: def:stripping-order]. We also assume that, for j = 1, 2, the polynomial
extensions in the recovered cells adjacent to the auxiliary exterior half-balls remain
elliptic in those half-balls whenever the half-balls are used.
    Let Σ ⊂ ∂Ω be a nonempty relatively open measured set. Assume that the
subdivision admits an admissible flat-face recovery order relative to Σ, in the sense
of Definition [source reference: def:stripping-order]. If
                                   ΛΩ           Ω
                                    σ (1) ,Σ = Λσ (2) ,Σ ,

then
                               σ (1) = σ (2) in Ω.
Equivalently, the polynomial matrices defining the two conductivities agree on every
cell of the subdivision.
Isabelle code
 definition cgu_global_uniqueness_claim_v7 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow> bool"
 where
   "cgu_global_uniqueness_claim_v7 M P1 P2 \<longleftrightarrow>
     (3 \<le> CARD(’n) \<and>
      cgu_graph_subdivision_core_v7 M \<and>
      cgu_piecewise_polynomial_class M P1 \<and>
      cgu_piecewise_polynomial_class M P2 \<and>
      cgu_recovery_geometry_operational_v6 M \<and>
      cgu_recovery_extension_admissible M P1 \<and>
      cgu_recovery_extension_admissible M P2 \<and>
      cgu_local_dn_equal M P1 P2 (cgu_domain M) (cgu_measured M))
     \<longrightarrow> P1 = P2"


English mathematical translation of the Isabelle code
   For finite I, C, H, geometric data M , and coefficient families P (1) , P (2) , the fol-
lowing implication holds. If
      • n ≥ 3;
      • M is an admissible subdivision;
      • P (1) and P (2) are admissible coefficient families;
      • M has an admissible recovery order;
      • both families satisfy the coefficient-access condition;
134                                CĂTĂLIN I. CÂRSTEA

     • the two families have the same stipulated local boundary-energy data on
       (Ω, Γ);
  then

                                  P (1) = P (2)
  as cell-indexed polynomial representations.
MAIN-002: cgu_uniform_degree_admissible_injectivity_claim_v7
English original and manuscript locator
    The corollary of [1] states:
    Suppose Nα ≤ N for all cells. If the subdivision admits an admissible flat-
face recovery order relative to Σ in which each cell is accessible through at least
N + 3 flat faces whose supporting hyperplanes satisfy the corresponding genericity
and triple-intersection geometry, and the recovered regions satisfy the stated face-
connectedness assumptions, then the following holds. For any σ (1) , σ (2) ∈ P(D, N )
that satisfy the coefficient-dependent triple-region positivity and auxiliary half-ball
ellipticity hypotheses of Theorem [source reference: thm:main] for this recovery
order, equality of their local DN maps on Σ implies σ (1) = σ (2) . Equivalently, the
local DN map is injective on the subclass of P(D, N ) satisfying those coefficient-
dependent admissibility conditions.
Isabelle code
 definition cgu_uniform_degree_admissible_injectivity_claim_v7 ::
   "nat \<Rightarrow> (’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
      bool"
 where
   "cgu_uniform_degree_admissible_injectivity_claim_v7 N M \<longleftrightarrow>
     (3 \<le> CARD(’n) \<and>
      cgu_graph_subdivision_core_v7 M \<and>
      (\<forall>c. cgu_degree M c = N) \<and>
      cgu_recovery_geometry_operational_v6 M)
     \<longrightarrow>
     (\<forall>P1 P2.
       cgu_piecewise_polynomial_class M P1 \<and>
       cgu_piecewise_polynomial_class M P2 \<and>
       cgu_recovery_extension_admissible M P1 \<and>
       cgu_recovery_extension_admissible M P2 \<and>
       cgu_local_dn_equal M P1 P2 (cgu_domain M) (cgu_measured M)
       \<longrightarrow> P1 = P2)"

English mathematical translation of the Isabelle code
  Fix N ∈ N. If
                    n ≥ 3,         M is an admissible subdivision,
             dc = N (c ∈ C),         M has an admissible recovery order,
                     (1)     (2)
  then, for every P , P , admissibility of both families, coefficient access for
both, and equality of their stipulated local boundary-energy data on (Ω, Γ) imply

                                       P (1) = P (2) .
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    135

Cited results
ANALYTIC-ELLIPTIC
Formal identifier: hormander_analytic_elliptic_ucp_claim
Relationship to source: derived.
Source attribution and locator
   Hörmander [19], Section 8.3, printed p. 271, equations (8.3.1)–(8.3.4) and Corol-
lary 8.3.2.
Complete source theorem statement (faithful mathematical restatement)
                                a (x)Dα , the principal symbol is the homogeneous
                      P
   For P (x, D) =        |α|≤mPα
degree-m part pm (x, ξ) = |α|=m aα (x)ξ α . The characteristic set consists of the
nonzero covectors (x, ξ) for which pm (x, ξ) = 0. The operator is elliptic precisely
when this set is empty, equivalently when pm (x, ξ) ̸= 0 for every ξ ̸= 0.
Source attribution and locator
   Hörmander [19], Theorem 8.6.1, printed p. 306.
Complete source theorem statement (faithful mathematical restatement)
   If the coefficients of a differential operator P are real analytic, then an analytic
singularity of a distribution u which is not already an analytic singularity of P u
can occur only at a characteristic covector; in standard notation,

                          WFA (u) ⊆ WFA (P u) ∪ Char P.
Source attribution and locator
    Hörmander [19], Theorem 8.6.5 and its stated elliptic consequence, printed p.
309.
Complete source theorem statement (faithful mathematical restatement)
    If u is a distribution on an open set X and P u = 0, then every exterior conormal
to supp u is characteristic for P . Hence, if P is elliptic, the support of u has
no boundary point in X. Consequently, when X is connected, a solution which
vanishes in a neighborhood of one point vanishes throughout X.
Source attribution and locator
    Hörmander [19], Theorem 1.2.5, printed p. 15.
Complete source theorem statement (faithful mathematical restatement)
    If f, g ∈ L1loc (X) and X f ϕ = X gϕ for every ϕ ∈ Cc∞ (X), then f = g almost
                            R        R

everywhere on X.
Source attribution and locator
    Hörmander [19], regular-distribution identification on printed p. 37 and Defini-
tion 3.1.1 on printed p. 55.
Complete source theorem statement (faithful mathematical restatement)
    Printed p. 37 identifies L1loc (X) Rmodulo almost-everywhere equality injectively
with the regular distributions ϕ 7→ X f ϕ. Definition 3.1.1, printed p. 55, defines
(∂i u)(ϕ) = −u(∂i ϕ) and multiplication of a distribution by a smooth function.
Exact derived mathematical result formalized
    Let X ⊂ Rn , n ≥ 1, be open and connected. Let A(x) be a symmetric ma-
trix polynomial which is uniformly positive definite on an open neighborhood of
136                            CĂTĂLIN I. CÂRSTEA

X. If a real locally square-integrable regular distribution u is a weak solution of
− div(A∇u) = 0 on X, and u = 0 almost everywhere on some nonempty open
subset of X, then u = 0 almost everywhere on X. This is the exact mathematical
content of the formal interface.
    For the notation correspondence, polynomial entries are real analytic and the
principal symbol of − div(A∇·), in Hörmander’s Dj = (1/i)∂j convention, is
ξ T A(x)ξ. Uniform positive definiteness makes it nonzero for ξ ̸= 0. The weak
variational identity is the distribution equation, and the regular-distribution re-
sults convert distributional vanishing to almost-everywhere vanishing. Polynomial-
ity and uniform ellipticity near the closure are conservative strengthenings of local
analyticity and ellipticity.
Isabelle code

 definition hormander_analytic_elliptic_ucp_claim ::
   "’n::finite ucp_point set \<Rightarrow> ’n ucp_coefficient \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow> bool"
 where
   "hormander_analytic_elliptic_ucp_claim X P u \<longleftrightarrow>
     ((0 < CARD(’n) \<and> open X \<and> connected X \<and>
       ucp_matrix_polynomial P \<and>
       (\<forall>x. ucp_symmetric_matrix (P x)) \<and>
       ucp_uniformly_elliptic_near X P \<and>
       ucp_weak_solution_on X P u \<and>
       (\<exists>V. V \<noteq> {} \<and> open V \<and> V \<subseteq> X \<and>
         (AE x in lborel. x \<in> V \<longrightarrow> u x = 0)))
      \<longrightarrow> (AE x in lborel. x \<in> X \<longrightarrow> u x = 0))"


English mathematical translation of the Isabelle code
  Let X ⊆ VI , P : VI → RI×I , and u : VI → R. If
      • n > 0;
      • X is open and connected;
      • P is entrywise polynomial and pointwise symmetric;
      • P is elliptic around X;
      • u is a local weak solution for P on X;
      • there exists a nonempty open V ⊆ X such that, for ambient-a.e. x,

                                x ∈ V =⇒ u(x) = 0;
  then, for ambient-a.e. x,

                               x ∈ X =⇒ u(x) = 0.

WEAK-GRADIENT-LOCALITY
Formal identifier: hormander_weak_gradient_locality_claim
Relationship to source: derived.
Source attribution and locator
  Hörmander [19], Definitions 1.2.1–1.2.2, the following zero-extension observation,
and Lemma 1.2.3, printed p. 14.
Complete source theorem statement (faithful mathematical restatement)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    137

   The test space on an open set X is Cc∞ (X), with support defined as the closure
of the nonzero set; its members extend smoothly by zero to the ambient Euclidean
space. The lemma constructs a nonnegative compactly supported smooth bump
positive at a prescribed point. Translation, scaling, a finite compact subcover, and
summation therefore give, for every compact K ⋐ X, a nonnegative test function
which is strictly positive on K.
Source attribution and locator
   Hörmander [19], Theorem 1.2.5, printed p. 15.
Complete source theorem statement (faithful mathematical restatement)
   Two locally integrable functions with identical pairings against every member of
Cc∞ (X) are equal almost everywhere.
Source attribution and locator
   Hörmander [19], regular-distribution identification on printed p. 37 and Defini-
tion 3.1.1 on printed p. 55.
Complete source theorem statement (faithful mathematical restatement)
   Printed p. 37 identifies locally integrable functions modulo almost-everywhere
equality with their regular distributions. Definition 3.1.1, printed p. 55, defines the
distributional derivative by (∂i u)(ϕ) = −u(∂i ϕ).
Exact derived mathematical result formalized
   Let X be open. Suppose real u and real vector field Du satisfy the project’s
local-square-integrability and weak-gradient predicates on X, and suppose u = 0
almost everywhere on X. Then Du = 0 almost    R everywhereR on X.
   Coordinatewise, the weak identity gives X u ∂i ϕ = − X (Du)i ϕ; the left side
is zero. The weak-gradient product-integrability clause, combined with a positive
localized test, proves (Du)i ∈ L1loc (X). Theorem 1.2.5 then makes each component
zero almost everywhere, and finite dimensionality combines the component conclu-
sions. The formal real test class is a conservative specialization of Hörmander’s
complex convention: real and imaginary parts recover all complex pairings.
Isabelle code

 definition hormander_weak_gradient_locality_claim ::
   "’n::finite ucp_point set \<Rightarrow>
    (’n ucp_point \<Rightarrow> real) \<Rightarrow>
    (’n ucp_point \<Rightarrow> ’n ucp_point) \<Rightarrow> bool"
 where
   "hormander_weak_gradient_locality_claim X u Du \<longleftrightarrow>
     ((open X \<and>
       ucp_locally_square_integrable_on X u \<and>
       ucp_locally_square_integrable_on X Du \<and>
       ucp_weak_gradient_on X u Du \<and>
       (AE x in lborel. x \<in> X \<longrightarrow> u x = 0))
      \<longrightarrow> (AE x in lborel. x \<in> X \<longrightarrow> Du x = 0))"


English mathematical translation of the Isabelle code
  If X is open, u and G are locally square integrable in the stipulated sense on X,
G satisfies the weak-gradient relation for u, and, for ambient-a.e. x,

                                x ∈ X =⇒ u(x) = 0,
138                             CĂTĂLIN I. CÂRSTEA

  then, for ambient-a.e. x,

                                x ∈ X =⇒ G(x) = 0.
HORMANDER-REGULAR-DISTRIBUTION-INJECTIVITY
Formal identifier: hormander_regular_distribution_injectivity_claim
Relationship to source: direct.
Source attribution and locator
   Hörmander [19], Definitions 1.2.1–1.2.2 and Lemma 1.2.3, printed p. 14.
Complete source theorem statement (faithful mathematical restatement)
   These results define the smooth compactly supported tests on an open set, their
support, and the localized smooth bumps used to separate a nonzero locally inte-
grable function from the zero distribution.
Source attribution and locator
   Hörmander [19], Theorem 1.2.5, printed p. 15.
Complete source theorem statement (faithful mathematical restatement)
   For an open X ⊂ Rn , if f, g ∈ L1loc (X) satisfy X f ϕ = X gϕ for every ϕ ∈
                                                       R         R

Cc∞ (X), then f = g almost everywhere on X.
Source attribution and locator
   Hörmander [19], regular-distribution identification on printed p. 37.
Complete source theorem statement (faithful mathematical restatement)
   The source expresses the preceding result as injectivity of the regular-distribution
embedding of L1loc (X) modulo almost-everywhere equality.
   Direct formal specialization.
   For every open X and real u ∈ L1 (X), if uϕ is integrable and X uϕ = 0 for
                                                                        R

every project smooth compact test ϕ, then u = 0 almost everywhere on X. Global
L1 (X) is stronger than the source’s local integrability, the comparison function
is specialized to zero, and the project test predicate is the globally zero-extended
realization of Cc∞ (X). The explicit product-integrability premise prevents use of
Isabelle’s totalized integral outside the ordinary integrable case.
Isabelle code
 definition hormander_regular_distribution_injectivity_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "hormander_regular_distribution_injectivity_claim dimension_type \<
      longleftrightarrow>
     (\<forall>X :: ’n cgu_point set. \<forall>u.
       open X \<and> hormander_regular_distribution_test_zero_on X u
       \<longrightarrow>
       (AE x in restrict_space lborel X. u x = 0))"


English mathematical translation of the Isabelle code
  For every X ⊆ VI and u : VI → R, if X is open, u is integrable on X, and every
ϕ ∈ D(X) has uϕ integrable with
                                Z
                                    uϕ dx = 0,
                                     X
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    139

  then

     u(x) = 0    for a.e. x with respect to Lebesgue measure restricted to X.

EVANS-POINCARE-ELLIPTIC-GREEN
Formal identifier: evans_poincare_elliptic_green_claim
Relationship to source: derived.
Source attribution and locator
  Evans [20], Section 5.6.1, Theorem 3 and its separately displayed particular
consequence, printed pp. 279–280.
Complete source theorem statement (faithful mathematical restatement)
   If U ⊂ Rn is bounded and open and u ∈ W01,p (U ), 1 ≤ p < ∞, then ∥u∥Lp (U ) ≤
C∥Du∥Lp (U ) , with C depending on U, n, p. The interface uses only p = 2.
Source attribution and locator
   Evans [20], Section 5.9.1, Theorem 1, printed pp. 299–300.
Complete source theorem statement (faithful mathematical restatement)
   The negative Sobolev space H −1 (U ) is the bounded dual of H01 (U ).
                                                                       PEquivalently,
                                                                         n
every such functional has a representation by L2 functions f = f 0 − i=1 ∂i f i , and
                                                                       1
conversely every such expression defines a bounded functional on H0 (U ).
Source attribution and locator
   Evans [20], Sections 6.1.1–6.1.2, printed pp. 311–315.
Complete source theorem statement (faithful mathematical restatement)
   On a bounded open domain, a divergence-form operator with bounded measur-
able leading coefficients, uniformly elliptic almost everywhere (and symmetric in the
symmetric case), gives the bilinear energy form on H01 (U ). A weak zero-Dirichlet
solution is an element u ∈ H01 (U ) satisfying that bilinear identity against every
v ∈ H01 (U ).
Source attribution and locator
   Evans [20], Section 6.2.1, Theorem 1 (Lax–Milgram), printed pp. 315–317.
Complete source theorem statement (faithful mathematical restatement)
   If H is a real Hilbert space and a bilinear form B : H × H → R is bounded and
coercive, |B[u, v]| ≤ M ∥u∥∥v∥ and B[u, u] ≥ β∥u∥2 with β > 0, then every f ∈ H ∗
has a unique u ∈ H satisfying B[u, v] = f (v) for all v ∈ H, and ∥u∥ ≤ ∥f ∥/β.
Source attribution and locator
   Evans [20], Section 6.2.2, Theorem 2, printed pp. 317–318.
Complete source theorem statement (faithful mathematical restatement)
   Under the elliptic coefficient hypotheses, the weak bilinear form satisfies
|B[u, v]| ≤ C∥u∥H01 (U ) ∥v∥H01 (U ) and a Gårding bound B[u, u] ≥ β∥u∥2H 1 (U ) −
                                                                               0
γ∥u∥2L2 (U ) for constants C, β > 0 and γ ≥ 0. Thus the leading elliptic part controls
the gradient norm, while lower-order terms cost only an L2 term.
Source attribution and locator
   Evans [20], Section 6.2.2, Theorem 3, printed pp. 318–319.
Complete source theorem statement (faithful mathematical restatement)
140                             CĂTĂLIN I. CÂRSTEA

   There is γ ≥ 0 such that, for f ∈ L2 (U ) and every µ ≥ γ, the shifted zero-
Dirichlet weak problem Lu + µu = f has a unique solution in H01 (U ), with the
corresponding energy estimate. This theorem does not itself state the unshifted
arbitrary-H −1 result below.
Exact derived mathematical result formalized
   Let U ̸= ∅ be bounded and open, and let a(x) be a chosen restricted-Borel mea-
surable, pointwise bounded, pointwise symmetric matrix with one positive point-
wise uniform ellipticity constant. Then the pure leading energy form is bounded
and strictly coercive on the project’s H01 (U ) quotient. Moreover, one constant
C ≥ 0, depending only on U, a, works for every bounded real linear source F with
bound K: there is a zero-boundary weak solution of − div(a∇u) = F , it satisfies
∥u∥H 1 (U ) ≤ CK, and it is unique modulo zero H 1Rdistance.
   The derivation takes H = H01 (U ) and B[u, v] = U (aDu)·Dv. Coefficient bound-
edness gives continuity; ellipticity plus the p = 2 Poincaré inequality gives coercivity
in the full project H 1 norm; Section 5.9.1 identifies the source with an element of
H ∗ ; Lax–Milgram gives the unshifted solution, uniqueness, and the uniform esti-
mate. The pointwise representative assumptions conservatively strengthen Evans’s
almost-everywhere coefficient assumptions.
Isabelle code
 definition evans_poincare_elliptic_green_claim ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "evans_poincare_elliptic_green_claim U a \<longleftrightarrow>
     (0 < CARD(’n) \<and> U \<noteq> {} \<and> open U \<and>
       evans_bounded_domain U \<and> evans_elliptic_coefficient_on U a)
     \<longrightarrow>
     (mclean_variational_form_on U a \<and>
       (\<exists>C. 0 \<le> C \<and>
         (\<forall>F K. mclean_source_bound_on U F K \<longrightarrow>
           (\<exists>u Du. mclean_green_solution_for U a F u Du \<and>
             mclean_h1_norm U u Du \<le> C * K \<and>
             (\<forall>v Dv. mclean_green_solution_for U a F v Dv
               \<longrightarrow>
               cgu_h1_squared_distance U u Du v Dv = 0)))))"


English mathematical translation of the Isabelle code
  Let U ⊆ VI and let a be a matrix field. If

                 n > 0,     U ̸= ∅,      U is open and bounded,
   and a has the bounded symmetric uniformly elliptic property on U , then:
    (1) Ba,U has the bounded/coercive pair property;
    (2) there is one C ≥ 0 such that, whenever F is K-bounded-linear on zero-
        boundary pairs, a variational solution (u, G) exists with

                                 ∥(u, G)∥U ≤ CK,
   and every other variational solution (v, H) satisfies

                                d2U (u, G), (v, H) = 0.
                                                  
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    141

   The second clause is existence plus zero-distance uniqueness, not literal equality
of representatives.
KANG-YUN-LTU-LOCAL-BOUNDARY-METRIC
Formal identifier: kang_yun_ltu_local_boundary_metric_claim_v6
Relationship to source: derived.
Source attribution and locator
   Kang–Yun [21], weak energy pairing on printed p. 719 and localized-DN defini-
tion on printed p. 723.
Complete source theorem statement (faithful mathematical restatement)
   For an open connected measured boundary patch Γ, the localized Dirichlet-to-
Neumann map takes H 1/2 boundary data supported in Γ, solves the conductivity/-
metric equation, and restricts the Neumann response to Γ. Its weak form is the
boundary energy pairing of an input solution with an arbitrary lift of the test trace.
Source attribution and locator
   Kang–Yun [21], Theorem 1.3, printed p. 723.
Complete source theorem statement (faithful mathematical restatement)
   Let two uniformly elliptic Riemannian metrics have C m,p regularity near a con-
nected open boundary patch Γ, with m ≥ 1 and p > 0. For every compact K ⋐ Γ,
the local DN maps stably determine the metrics near K, modulo a local diffeo-
morphism which fixes the boundary: after the appropriate pullback, the metric
difference is bounded by a positive power of the local-DN operator-norm difference.
In particular, equality of the local maps gives equality up to that boundary-fixing
gauge on K.
Source attribution and locator
   Kang–Yun [21], Lemmas 2.1 and 2.2, printed pp. 724–727.
Complete source theorem statement (faithful mathematical restatement)
   In boundary-normal coordinates and for a boundary point and tangential fre-
quency, the authors construct high-frequency boundary packets supported in an
arbitrarily small part of Γ, extend them into a shrinking boundary box DN , and
establish the packet, trace, and Sobolev norm bounds used in the asymptotic energy
calculation.
Source attribution and locator
   Kang–Yun [21], Section 3, equations (3.7)–(3.9) and the intervening Hardy in-
equality, printed pp. 728–731.
Complete source theorem statement (faithful mathematical restatement)
   Writing the exact solution as the explicit packet plus a correction, the source
proves the local correction estimate (3.7), the artificial-top trace estimate (3.8), the
displayed Hardy inequality before (3.9), and the weighted residual estimate (3.9).
In the notation used by the reviewed derivation, the local estimate is ∥sN ∥H 1 (DN ) ≤
CN 1−|α|/2 , with the subsequent estimates making the correction terms negligible
at the normalization used in the DN limit.
Source attribution and locator
   Kang–Yun [21], Theorem 4.1 and equations (4.5)–(4.8), printed pp. 731–733.
Complete source theorem statement (faithful mathematical restatement)
142                             CĂTĂLIN I. CÂRSTEA

    The normalized high-frequency local-DN energy limit at a chosen boundary point
determines the tangential metric quadratic form there. Varying the tangential
covector and polarizing determines the complete tangential bilinear form.
Source attribution and locator
    Kang–Yun [21], boundary-normal-coordinate and diffeomorphism reduction,
printed pp. 733–734.
Complete source theorem statement (faithful mathematical restatement)
    A smooth positive metric near the observed patch can be put into the boundary-
normal form used by the packet computation. The comparison of the two normal-
coordinate charts is a local diffeomorphism whose restriction to the boundary is the
identity; hence its differential is the identity on tangent vectors.
Source attribution and locator
    Lassas–Taylor–Uhlmann [22], remote rough-boundary setting on printed p. 209
and local-symbol discussion in Section 2, printed pp. 210–211.
Complete source theorem statement (faithful mathematical restatement)
    In their analytic, Wiener-regular complete-manifold setting, boundary roughness
is allowed away from the measured analytic patch, and the boundary symbol is
obtained locally from the DN map. This is corroboration of locality in a different
setting, not a theorem proving the graph-domain corollary below.
Exact derived mathematical result formalized
    In dimension at least three, let U be a bounded connected graph-Lipschitz do-
main contained in the fixed subdivision model. Let γ be a nonempty relatively open
flat boundary patch with a full one-sided collar, disjoint from the subdivision skele-
ton. Suppose each of two globally bounded uniformly elliptic piecewise-polynomial
coefficients agrees
                  p on an open collar of γ with a smooth positive metric-density
realization aj = det gj gj−1 . If the completed real weak local-DN energy pairings
agree for every supported input/test trace, with solutions existing for those data,
then for every x ∈ γ and every pair of vectors tangent to the supporting hyperplane,
g1 (x)(v, w) = g2 (x)(v, w). No normal component or remote coefficient is identified.
    The derivation localizes the Kang–Yun packet with a fixed smooth collar cut-
off. Cutoff derivatives occur a fixed positive normal distance from the boundary
and are exponentially small; graph-domain trace lifting, Poincaré, and global el-
lipticity give the correction bound without remote smoothness. Four real bilinear
pairings reconstruct the complex packet pairing. The boundary-fixing gauge has
identity tangential differential, so equality after pullback gives the stated covariant
tangential equality. Pointwise shrinking handles a disconnected formal patch. Nei-
ther paper prints this exact graph-domain implication verbatim, and LTU supplies
corroboration only.
Isabelle code
 definition kang_yun_ltu_local_boundary_metric_claim_v6 ::
   "(’n::finite, ’c::finite, ’h::finite) cgu_model \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     (’c \<Rightarrow> ’n cgu_matrix_polynomial) \<Rightarrow>
     ’n cgu_point set \<Rightarrow> ’n cgu_point set \<Rightarrow>
     ’n cgu_point \<Rightarrow> real \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow>
     ’n lu_metric \<Rightarrow> ’n lu_metric \<Rightarrow>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    143

     ’n lu_density \<Rightarrow> ’n lu_density \<Rightarrow> bool"
 where
   "kang_yun_ltu_local_boundary_metric_claim_v6 M P1 P2 U gamma normal offset
       g1 g2 a1 a2 rho1 rho2 \<longleftrightarrow>
     (3 \<le> CARD(’n) \<and>
      cgu_graph_subdivision_core_v7 M \<and>
      cgu_piecewise_polynomial_class M P1 \<and>
      cgu_piecewise_polynomial_class M P2 \<and>
      cgu_graph_lipschitz_domain_v5 U \<and>
      U \<subseteq> cgu_domain M \<and>
      cgu_flat_face_patch U normal offset gamma \<and>
      gamma \<inter> cgu_subdivision_edge_corner_set M = {} \<and>
      lu_smooth_metric_extension_near M P1 U gamma g1 a1 rho1 \<and>
      lu_smooth_metric_extension_near M P2 U gamma g2 a2 rho2 \<and>
      cgu_local_dn_equal M P1 P2 U gamma)
     \<longrightarrow> lu_induced_boundary_metrics_equal_on gamma normal g1 g2"


English mathematical translation of the Isabelle code
  Suppose
      • n ≥ 3;
      • M is an admissible subdivision;
      • P (1) , P (2) are admissible coefficient families;
      • U is Lipschitz admissible and U ⊆ Ω;
      • (U ; ν, b; γ) is an oriented flat boundary patch;
      • γ ∩ ΣM = ∅;
      • packages (gs , as , ρs ) realize (M, P (s) , U, γ), s = 1, 2;
      • the two families have the same stipulated local boundary-energy data on
        (U, γ).
  Then g1 and g2 have the same tangential bilinear pairing along (γ, ν).
MCLEAN-GRAPH-SUPPORTED-H1-ZERO
Formal identifier: mclean_graph_supported_h1_zero_claim
Relationship to source: direct.
Source attribution and locator
  McLean [23], Definition 3.28, printed pp. 89–90.
Complete source theorem statement (faithful mathematical restatement)
   A Lipschitz domain has compact boundary and a finite cover by rigid Cartesian-
coordinate neighborhoods in which the domain is a Lipschitz hypograph. Replacing
the local Lipschitz graph functions by continuous functions gives the book’s C 0 -
domain class; every Definition 3.28 Lipschitz domain is therefore a C 0 domain.
Source attribution and locator
  McLean [23], Theorem 3.29(ii), printed pp. 91–92.
Complete source theorem statement (faithful mathematical restatement)
   For a C 0 domain Ω and every real Sobolev order s, the smooth compactly sup-
ported class D(Ω) is dense, in the ambient H s (Rn ) norm, in the global Sobolev space
consisting of distributions supported in Ω. Equivalently, the ambient compact-test
closure equals that supported global Sobolev space.
   Direct formal specialization.
144                            CĂTĂLIN I. CÂRSTEA

   At real scalar order s = 1, suppose U is a bounded graph-Lipschitz domain and
(u, Du) is a global project H 1 (Rn ) pair whose potential and selected weak gradient
vanish almost everywhere outside U . Then (u, Du) belongs to the project’s sequen-
tial H01 (U ) compact-test closure. The graph-Lipschitz premise is stronger than the
source’s C 0 hypothesis, the gradient-support premise is an additional compatible re-
striction, and source global convergence is stronger than the conclusion’s restricted
U -distance convergence.
Isabelle code
 definition mclean_graph_supported_h1_zero_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_graph_supported_h1_zero_claim dimension_type \<longleftrightarrow>
     0 < CARD(’n) \<and>
     (\<forall>(U :: ’n cgu_point set) u Du.
       cgu_graph_lipschitz_domain_v5 U \<and>
       cgu_h1_pair_on UNIV u Du \<and>
       (AE x in lborel.
         x \<notin> closure U \<longrightarrow> u x = 0 \<and> Du x = 0)
       \<longrightarrow> cgu_h1_zero_pair_on U u Du)"


English mathematical translation of the Isabelle code
  This condition is the conjunction of:
   (1) n > 0;
                                                      1
   (2) for every U ⊆ VI and every pair (u, G) ∈ Hpair   (VI ), if U is Lipschitz
        admissible and, for ambient-a.e. x,

                        x∈
                         / U =⇒ u(x) = 0 and G(x) = 0,
   then

                                         1
                               (u, G) ∈ H0,pair (U ).
   The support premise is almost-everywhere, not a literal compact-support asser-
tion about the stored representatives.
MCLEAN-H1-ZERO-BIDUAL-REPRESENTATION
Formal identifier: mclean_h1_zero_bidual_representation_claim_v2
Relationship to source: derived.
Source attribution and locator
   McLean [23], weak-derivative Sobolev construction and Hilbert conclusion,
printed pp. 73–75.
Complete source theorem statement (faithful mathematical restatement)
   On every nonempty open U , Wpr (U ) consists of Lp functions possessing all weak
derivatives through order r in Lp , with the derivative graph norm. For p = 2, the
sum of the L2 inner products of the weak derivatives induces that norm, and W s (U )
is a Hilbert space for every real s ≥ 0.
Source attribution and locator
   McLean [23], zero-boundary closure notation, printed p. 77.
Complete source theorem statement (faithful mathematical restatement)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    145

   The source defines the conventional zero-boundary space as the closure of D(U )
in the relevant Sobolev norm. For this interface the cited page supplies nomen-
clature only; no equality with a distinct supported Bessel-potential space on an
arbitrary open set is used.
Source attribution and locator
   McLean [23], Hilbert reflexivity statement, printed p. 79.
Complete source theorem statement (faithful mathematical restatement)
   Every Hilbert space is reflexive: the canonical isometric embedding J : H → H ∗∗ ,
(Ju)(F ) = F (u), is onto. Thus every bounded linear functional on H ∗ is evaluation
at some u ∈ H.
Exact derived mathematical result formalized
   For every nonempty open U , let H be the quotient Hilbert space represented by
project H01 (U ) potential/weak-gradient pairs. There exist a set E and seminorm p
such that E is exactly the set of total raw functions inducing bounded real linear
functionals on H, and p(F ) is the least valid source bound, hence the operator
seminorm. Every carrier-relative real-linear g : E → R bounded by p is of the form
g(F ) = F (u, Du) for some project H01 (U ) pair.
   The project’s potential-plus-gradient norm is the order-one graph norm, and the
compact-test closure is a closed Hilbert subspace after quotienting zero distance.
Bounded raw sources descend to its continuous dual; the least bound is the dual
norm. A p-bounded g vanishes on the seminorm kernel, descends to the genuine
bidual, and reflexivity represents it by evaluation. The raw carrier E, least-bound
plumbing, and displayed evaluation formula are standard consequences, not state-
ments printed verbatim by McLean.
Isabelle code

 definition mclean_h1_zero_bidual_representation_claim_v2 ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_h1_zero_bidual_representation_claim_v2 dimension_type \<
      longleftrightarrow>
     (\<forall>U :: ’n cgu_point set.
       U \<noteq> {} \<and> open U
       \<longrightarrow>
       (\<exists>E p. mclean_h1_zero_bidual_realization_on_v2 U E p))"


English mathematical translation of the Isabelle code
   For every U ⊆ VI , if U ̸= ∅ and U is open, then there exist E and p such that:
    (1) E is precisely the total two-argument functionals that are K-bounded-
                     1
        linear on H0,pair (U ) for some K, and E is closed under the stated vector
        operations;
    (2) p is the stipulated seminorm, p(F) is an admissible bound for every F ∈ E,
        and it is no larger than every other admissible bound;
    (3) every p-dominated linear ℓ : E → R has a representing pair (u, G) ∈
           1
        H0,pair (U ) with


                           ℓ(F) = F(u, G)       (F ∈ E).
146                             CĂTĂLIN I. CÂRSTEA

   No quotient identifies total functionals that agree only on the zero-boundary pair
class, and uniqueness of the representing pair is not asserted.
MCLEAN-H1-ZERO-EXTENSION-LOCALIZATION
Formal identifier: mclean_h1_zero_extension_localization_claim
Relationship to source: derived.
Source attribution and locator
   McLean [23], smooth compact tests and the two compact-test closures, printed
pp. 61, 65, and 77–78.
Complete source theorem statement (faithful mathematical restatement)
   The test class is D(Ω) = Cc∞ (Ω). H0s (Ω) is its closure in the intrinsic/restriction
  s                      e s (Ω) is its closure in the ambient H s (Rn ) norm. These two
H (Ω) norm, whereas H
spaces are not identified on an arbitrary open set in this interface.
Source attribution and locator
   McLean [23], Theorem 3.6, printed p. 64.
Complete source theorem statement (faithful mathematical restatement)
   Given a closed set and an open neighborhood (equivalently, an arbitrarily small
prescribed neighborhood), there is a smooth cutoff taking values between zero and
one, equal to one on the closed set and zero outside the prescribed neighborhood.
For a compact set contained in an open set, the cutoff may be chosen compactly
supported in that open set.
Source attribution and locator
   McLean [23], Theorem 3.16, printed p. 80.
Complete source theorem statement (faithful mathematical restatement)
   For every nonnegative integer m, the global weak-derivative space W m (Rn ) and
the Bessel-potential space H m (Rn ) are the same set with equivalent norms.
Source attribution and locator
   McLean [23], Theorem 3.20, printed p. 83.
Complete source theorem statement (faithful mathematical restatement)
   Multiplication by a smooth compactly supported cutoff is a bounded linear oper-
ator on H s (Ω) and, separately, on H    e s (Ω). The theorem does not state a multiplier
             s
clause for H0 (Ω) under that name.
Exact derived mathematical result formalized
   Two order-one representative statements are formalized. First, if ∅ ̸= U ⊆ W
are open and (u, Du) is in the project H01 (U ) closure, then the zero extensions of
both representatives form a project H01 (W ) pair. Second, if nonempty open V ⊆ W ,
compact K ⊆ V , and a project H01 (W ) pair vanishes almost everywhere together
with its gradient off K, then the same representatives form a project H01 (V ) pair.
   For extension, each compact test in U is also a compact test in W , and zero
extension turns intrinsic order-one convergence into global W 1 convergence; Theo-
rem 3.16 supplies the ambient H 1 bridge. For localization, choose the Theorem 3.6
cutoff equal to one near K; Theorem 3.20 gives continuity on the ambient compact-
test closure, and the product equals the original pair because both representatives
vanish off K. If K = ∅, the conclusion is the zero class. No arbitrary-domain
identity H01 = He 1 is used.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    147

Isabelle code
 definition mclean_h1_zero_extension_localization_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_h1_zero_extension_localization_claim dimension_type \<longleftrightarrow>

     ((\<forall>(U :: ’n cgu_point set) W u Du.
         U \<noteq> {} \<and> open U \<and> open W \<and> U \<subseteq> W \<and>
         cgu_h1_zero_pair_on U u Du
         \<longrightarrow>
         cgu_h1_zero_pair_on W
           (mclean_zero_extension_on U u)
           (mclean_zero_extension_on U Du)) \<and>
      (\<forall>(W :: ’n cgu_point set) V K u Du.
         W \<noteq> {} \<and> V \<noteq> {} \<and> open W \<and> open V \<and> V \<
      subseteq> W \<and>
         compact K \<and> K \<subseteq> V \<and>
         cgu_h1_zero_pair_on W u Du \<and>
         (AE x in restrict_space lborel W.
           x \<notin> K \<longrightarrow> u x = 0 \<and> Du x = 0)
         \<longrightarrow> cgu_h1_zero_pair_on V u Du))"


English mathematical translation of the Isabelle code
  Both of the following universally quantified implications hold.
                                                          1
   (1) If U ̸= ∅, U, W are open, U ⊆ W , and (u, G) ∈ H0,pair  (U ), then

                                                 1
                                            
                            ExtU u, ExtU G ∈ H0,pair   (W ).
    (2) If W, V ̸= ∅, W, V are open, V ⊆ W , K ⊆ V is compact, (u, G) ∈
          1
        H0,pair (W ), and, for a.e. x with respect to Lebesgue measure restricted to
        W,

                        x∈
                         / K =⇒ u(x) = 0 and G(x) = 0,
  then

                                          1
                                (u, G) ∈ H0,pair (V ).
MCLEAN-HYPERPLANE-OFFSET-SOURCE
Formal identifier: mclean_hyperplane_offset_source_claim
Relationship to source: derived.
Source attribution and locator
   McLean [23], Theorems 3.37–3.38, printed pp. 102–104.
Complete source theorem statement (faithful mathematical restatement)
   At the order used here, the trace is a bounded surjection H 1 → H 1/2 on a Lip-
schitz boundary, has a bounded right inverse, and agrees with ordinary restriction
for smooth functions. By duality, H −1/2 boundary distributions act continuously
on H 1 traces. These statements provide the trace and Fourier-estimate setting for
the flat-hyperplane specialization.
Source attribution and locator
   McLean [23], Lemma 3.39, printed pp. 104–105.
148                              CĂTĂLIN I. CÂRSTEA

Complete source theorem statement (faithful mathematical restatement)
   A distribution supported on the hyperplane {xn = 0} has a finite representation
by
P tangential     distributions tensored with normal derivatives of the Dirac mass,
          j                                   s
   j vj ⊗Dn δ0 . For membership in ambient H , each occurring order satisfies s+j <
−1/2 and the tangential coefficient has order vj ∈ H s+j+1/2 (Rn−1 ).
Source attribution and locator
   McLean [23], equation (3.33), printed pp. 104–105.
Complete source theorem statement (faithful mathematical restatement)
   For an admissible term,

                    ∥v ⊗ Dnj δ0 ∥2H s (Rn ) = Cs,j ∥v∥2H s+j+1/2 (Rn−1 ) ,
   with the finite positive constant given by the normal-frequency integral. In
particular, at s = −1, j = 0, every v ∈ H −1/2 (Rn−1 ) defines an ambient H −1
source.
Exact derived mathematical result formalized
   Let the ambient dimension be one larger than a positive tangential dimension.
Fix an isometric affine hyperplane chart, a unit normal, a smooth compactly sup-
ported tangential density g, and δ > 0 such that the full swept support cylinder for
offsets 0 ≤ t ≤ δ lies in an open set Ω. Then there are bounded quotient-compatible
sources St and one C ≥ 0 such that, on every smooth test ϕ,
                                   Z
                           St (ϕ) = g(y)ϕ(chart(y) + tν) dy,
                                                     √
   with ∥St ∥H −1 (Ω) ≤ C and ∥St − S0 ∥H −1 (Ω) ≤ C t.
   Translation in the normal variable multiplies the Fourier transform by e−2πiξn t .
In the integral underlying (3.33), bounding |e−2πiξn t − 1| by min(2, C|ξn |t) and
splitting at |ξn | = 1/t gives a squared H −1 bound of order t, hence the displayed
√
  t norm bound. That difference estimate is an elementary consequence of (3.33),
not a numbered theorem. The formal source is an abstract bounded extension on
the H01 quotient; only its action on smooth tests is given pointwise.
Isabelle code
 definition mclean_hyperplane_offset_source_claim ::
   "(’m::finite itself) \<Rightarrow> (’n::finite itself) \<Rightarrow> bool"
 where
   "mclean_hyperplane_offset_source_claim tangential_type ambient_type \<
      longleftrightarrow>
     (1 \<le> CARD(’m) \<and> CARD(’n) = Suc (CARD(’m))) \<longrightarrow>
     (\<forall>(Omega :: ’n cgu_point set)
       (chart :: ’m cgu_point \<Rightarrow> ’n cgu_point) normal g delta.
       open Omega \<and> cgu_test_function_on UNIV g \<and>
       mclean_flat_chart chart normal \<and> 0 < delta \<and>
       mclean_flat_offset_cylinder_inside Omega chart normal g delta
       \<longrightarrow>
       (\<exists>source_at C. 0 \<le> C \<and>
         (\<forall>t. 0 \<le> t \<and> t \<le> delta \<longrightarrow>
           mclean_source_extends_flat_offset_action
             Omega chart normal t g (source_at t) \<and>
           mclean_source_bound_on Omega
             (source_at t) C \<and>
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    149

           mclean_source_bound_on Omega
             (\<lambda>u Du.
               source_at t u Du - source_at 0 u Du)
             (C * sqrt t))))"


English mathematical translation of the Isabelle code
  If

                              |J| ≥ 1,    |I| = |J| + 1,
   then the following holds. Let Ω ⊆ VI be open, let (χ, ν) be a flat isometric chart,
let g ∈ D(VJ ), let δ > 0, and assume the support-tube condition. There exist a
family (Ft )t∈R and one C ≥ 0 such that, for every 0 ≤ t ≤ δ,
                             Z
                Ft (ϕ, ∇ϕ) =      g(x)ϕ(χ(x) + tν) dx    (ϕ ∈ D(Ω)),
                              VJ
                             1
  Ft is C-bounded-linear on H0,pair (Ω), and the total functional

                        (u, G) 7−→ Ft (u, G) − F0 (u, G)
       √
   is C t-bounded-linear there. The same family and the same C serve every
t ∈ [0, δ].
MCLEAN-SMOOTH-GENERATOR-AMBIENT-LIFT
Formal identifier: mclean_smooth_generator_ambient_lift_claim_v2
Relationship to source: derived.
Source attribution and locator
   McLean [23], Theorem 3.6, printed p. 64.
Complete source theorem statement (faithful mathematical restatement)
   A closed set contained in a prescribed open neighborhood admits a smooth cutoff
equal to one on the closed set and supported in that neighborhood; for a compact
set in an open set the cutoff can be compactly supported there.
Source attribution and locator
   McLean [23], Theorems 3.37–3.38, printed pp. 102–104.
Complete source theorem statement (faithful mathematical restatement)
   At order one on a Lipschitz domain, the trace H 1 (U ) → H 1/2 (∂U ) is bounded
and surjective, has a continuous right inverse, and agrees with classical boundary
restriction on smooth functions.
Source attribution and locator
   McLean [23], Theorem 3.40, printed pp. 105–106.
Complete source theorem statement (faithful mathematical restatement)
   On a C k−1,1 domain, H0s (U ) = H s (U ) for 0 ≤ s ≤ 1/2; for 1/2 < s ≤ k, the zero-
boundary space is characterized by vanishing of the applicable boundary traces. At
the used specialization s = k = 1, the boundary hypothesis is C 0,1 (Lipschitz), and
H01 (U ) = ker(γ : H 1 (U ) → H 1/2 (∂U )).
Exact derived mathematical result formalized
   Let Ω1 and U ⊆ Ω1 be graph-Lipschitz domains in dimension at least two, let
γ ⊆ Ω1 ∩ ∂U , and fix one globally smooth compactly supported boundary generator
150                            CĂTĂLIN I. CÂRSTEA

p whose boundary support lies in γ. Then there is a project H01 (Ω1 ) pair (z, Dz)
whose quotient trace on U equals the trace of (p, ∇p).
   Let K be the compact closure of the nonzero boundary support of p. If K ̸= ∅,
choose a generator-dependent cutoff χ ∈ Cc∞ (Ω1 ), χ = 1 near K, and set z = χp.
The difference (1 − χ)p has zero boundary trace on U , so Theorem 3.40 puts it in
H01 (U ). If K = ∅, use the zero ambient pair and apply the same kernel theorem
directly. The witness is chosen after the single generator; no linear, bounded, or
simultaneous lift operator is asserted.
Isabelle code

 definition mclean_smooth_generator_ambient_lift_claim_v2 ::
   "’n::finite itself \<Rightarrow> ’c::finite itself \<Rightarrow>
     ’h::finite itself \<Rightarrow> bool"
 where
   "mclean_smooth_generator_ambient_lift_claim_v2 ambient_type cell_type
       hyperplane_type \<longleftrightarrow>
     2 \<le> CARD(’n) \<longrightarrow>
     (\<forall>(M :: (’n, ’c, ’h) cgu_model)
       (Omega1 :: ’n cgu_point set) U gamma p.
       cgu_graph_lipschitz_domain_v5 Omega1 \<and>
       cgu_graph_lipschitz_domain_v5 U \<and>
       U \<subseteq> Omega1 \<and>
       gamma \<subseteq> Omega1 \<inter> frontier U \<and>
       cgu_boundary_test_on M U gamma p
       \<longrightarrow>
       (\<exists>z Dz.
         cgu_h1_zero_pair_on Omega1 z Dz \<and>
         mclean_same_trace_on U p (cgu_classical_gradient p) z Dz))"


English mathematical translation of the Isabelle code
  If n ≥ 2, then for every finite cell and hyperplane types, every geometric datum
M , and all Ω1 , U, γ, p, the following implication holds. If
      • Ω1 and U are Lipschitz admissible;
      • U ⊆ Ω1 ;
      • γ ⊆ Ω1 ∩ ∂U ;
      • p is boundary-supported relative to (M, U, γ);
                              1
  then there exists (z, Z) ∈ H0,pair (Ω1 ) such that

                                                  
                                RU (p, ∇p), (z, Z) .

MCLEAN-SMOOTH-TEST-H1-ZERO
Formal identifier: mclean_smooth_test_h1_zero_claim
Relationship to source: derived.

Source attribution and locator
   McLean [23], test class, derivative convention, and first-order Sobolev definition,
printed pp. 65, 68, and 73–74.
Complete source theorem statement (faithful mathematical restatement)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    151

   D(U ) = Cc∞ (U ). Distributional derivatives use the integration-by-parts sign,
and W21 (U ) consists of square-integrable functions whose first distributional deriva-
tives are square-integrable. A smooth compactly supported function and its classi-
cal first derivatives are square-integrable, and its distributional and classical deriva-
tives agree; Hence every test belongs to W21 (U ) with its classical gradient.
Source attribution and locator
   McLean [23], zero-boundary closure definition, printed p. 77.
Complete source theorem statement (faithful mathematical restatement)
   The zero-boundary Sobolev space is the norm closure of D(U ). In particular
every generator is in that closure, witnessed by the constant sequence.
Source attribution and locator
   McLean [23], Theorem 3.16, printed p. 80.
Complete source theorem statement (faithful mathematical restatement)
   On Rn , the integer-order weak-derivative and Bessel-potential spaces coincide
with equivalent norms. The theorem is used only for the globally smooth compactly
supported representative; no equality of full spaces on an arbitrary open set is
asserted.
Exact derived mathematical result formalized
   For every open U and every globally smooth real ϕ with compact closed nonzero
support contained in U , the pair (ϕ, ∇ϕ) is a project H01 (U ) pair. Smoothness
and compact support give measurability and square integrability; integration by
parts identifies the classical gradient with the weak gradient; the constant sequence
ϕ proves membership in the project’s compact-test closure. McLean states the
definitions for nonempty open sets. When U is empty, the formal support condition
forces ϕ = 0, so the conclusion is an elementary zero-function extension, not a source
attribution.
Isabelle code

 definition mclean_smooth_test_h1_zero_claim ::
   "’n::finite itself \<Rightarrow> bool"
 where
   "mclean_smooth_test_h1_zero_claim dimension_type \<longleftrightarrow>
     (\<forall>(U :: ’n cgu_point set) phi.
       open U \<longrightarrow>
       cgu_test_function_on U phi \<longrightarrow>
       cgu_h1_zero_pair_on U phi (cgu_classical_gradient phi))"


English mathematical translation of the Isabelle code
  For every U ⊆ VI and every ϕ, the literal right-associated implication is

                                                   1
                                                              
                 U open =⇒ ϕ ∈ D(U ) =⇒ (ϕ, ∇ϕ) ∈ H0,pair (U ) .

MCLEAN-TRACE-DIRICHLET-GREEN
Formal identifier: mclean_trace_dirichlet_green_claim_v3
Relationship to source: derived.
Source attribution and locator
  McLean [23], Definition 3.28, printed pp. 89–90.
152                             CĂTĂLIN I. CÂRSTEA

Complete source theorem statement (faithful mathematical restatement)
   The relevant C 0,1 geometry is a domain whose compact boundary is locally a
Lipschitz graph after a rigid change of Cartesian coordinates. The project uses the
bounded connected subclass.
Source attribution and locator
   McLean [23], Theorem 3.37, printed p. 102.
Complete source theorem statement (faithful mathematical restatement)
    On a Lipschitz domain, at order one the trace γ : H 1 (U ) → H 1/2 (∂U ) is bounded
and surjective and has a continuous right inverse. Consequently the boundary space
is isomorphic, with equivalent norm, to the quotient of H 1 (U ) by the trace kernel.
Source attribution and locator
    McLean [23], Theorem 3.40, printed pp. 105–106.
Complete source theorem statement (faithful mathematical restatement)
    On a C k−1,1 domain the zero-boundary space equals all of H s for 0 ≤ s ≤ 1/2,
while for 1/2 < s ≤ k it is characterized by vanishing of the relevant boundary
traces. At s = k = 1, used here, the domain is Lipschitz C 0,1 and H01 (U ) = ker γ.
Source attribution and locator
    McLean [23], Lemma 4.3, printed pp. 116–117.
Complete source theorem statement (faithful mathematical restatement)
    Once the right-hand side of a weak elliptic equation is fixed, a weak solution has
a unique conormal boundary distribution in H −1/2 (∂U ) satisfying the variational
Green formula. Its norm is bounded in terms of the solution and source norms; the
proof uses a continuous trace right inverse.
Source attribution and locator
    McLean [23], Theorem 4.4, printed p. 118.
Complete source theorem statement (faithful mathematical restatement)
    The first Green identity expresses the variational form as the interior source
pairing plus the conormal/trace boundary pairing. Applying it in both orders
gives the second Green identity. For a homogeneous solution, its energy against an
arbitrary H 1 lift therefore depends only on the lift’s boundary trace.
Source attribution and locator
    McLean [23], Theorem 4.10, printed pp. 128–130, with the pure Dirichlet spe-
cialization on printed p. 131.
Complete source theorem statement (faithful mathematical restatement)
    The mixed variational boundary problem on a bounded Lipschitz domain sat-
isfies a Fredholm alternative: in the trivial-kernel branch every admissible datum
has a unique solution; otherwise solvability is subject to the stated orthogonality
conditions against the adjoint homogeneous kernel. For pure Dirichlet data the
energy space is V = H01 (U ) and V ∗ = H −1 (U ), so arbitrary bounded dual sources
are allowed. The formal strict-coercivity premise forces the trivial-kernel branch.
Source attribution and locator
    McLean [23], equations (4.35)–(4.38), printed p. 145.
Complete source theorem statement (faithful mathematical restatement)
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    153

   The solution operators furnished by the variational problem are bounded, and
the Steklov–Poincaré/Dirichlet-to-Neumann operator obtained from the conormal
pairing is a bounded operator between the trace space and its dual.
Exact derived mathematical result formalized
   Let U be a bounded graph-Lipschitz domain in dimension at least two, and let a
define an integrable bilinear energy form which is bounded on project H 1 (U ) pairs
and strictly coercive on project H01 (U ). Then:
     (1) every project quotient trace has a weak homogeneous Dirichlet solution,
         unique modulo zero H 1 distance;
     (2) one constant bounds the homogeneous solution’s energy pairing by the
         product of the two quotient trace norms, so the pairing is a bounded DN
         form; and
     (3) one constant gives, for every bounded real-linear source on H01 (U ), a zero-
         boundary Green solution with an H 1 -norm estimate proportional to the
         source bound, unique modulo zero distance.
   The project trace is the quotient H 1 (U )/H01 (U ), with norm the infimum of the
norms of its lifts. Theorems 3.37 and 3.40 identify this with the source trace space;
Lemma 4.3 and Theorem 4.4 make homogeneous energy depend only on quotient
traces; strict coercivity places Theorem 4.10 in its unique pure-Dirichlet branch and
yields the solution bounds. The graph-domain premise is a conservative bounded
subclass of McLean’s C 0,1 geometry.
Isabelle code
 definition mclean_trace_dirichlet_green_claim_v3 ::
   "’n::finite cgu_point set \<Rightarrow> ’n mclean_coefficient \<Rightarrow> bool"

 where
   "mclean_trace_dirichlet_green_claim_v3 U a \<longleftrightarrow>
     (2 \<le> CARD(’n) \<and> cgu_graph_lipschitz_domain_v5 U \<and>
       mclean_variational_form_on U a)
     \<longrightarrow>
     ((\<forall>f Df. cgu_h1_pair_on U f Df \<longrightarrow>
       (\<exists>u Du. mclean_dirichlet_solution_for U a f Df u Du \<and>
         (\<forall>v Dv. mclean_dirichlet_solution_for U a f Df v Dv
           \<longrightarrow> cgu_h1_squared_distance U u Du v Dv = 0))) \<and>
      (\<exists>C. 0 \<le> C \<and>
       (\<forall>f Df u Du h Dh.
         mclean_dirichlet_solution_for U a f Df u Du \<and>
         cgu_h1_pair_on U h Dh
         \<longrightarrow>
         mclean_energy_integrable U a Du Dh \<and>
         abs (mclean_energy U a Du Dh) \<le>
           C * mclean_trace_norm U f Df * mclean_trace_norm U h Dh)) \<and>
      (\<exists>C. 0 \<le> C \<and>
       (\<forall>F K. mclean_source_bound_on U F K \<longrightarrow>
         (\<exists>u Du. mclean_green_solution_for U a F u Du \<and>
           mclean_h1_norm U u Du \<le> C * K \<and>
           (\<forall>v Dv. mclean_green_solution_for U a F v Dv
             \<longrightarrow> cgu_h1_squared_distance U u Du v Dv = 0)))))"


English mathematical translation of the Isabelle code
  If
154                              CĂTĂLIN I. CÂRSTEA


                        n ≥ 2,      U is Lipschitz admissible,
                  Ba,U has the bounded/coercive pair property,
  then all three conclusions hold.
                          1
    (1) Every (f, F ) ∈ Hpair (U ) has an a-Dirichlet pair (u, G), and every other
        such pair (v, H) satisfies

                                 d2U (u, G), (v, H) = 0.
                                                    

      (2) There exists one C2 ≥ 0 such that, whenever (u, G) is an a-Dirichlet pair
                                     1
          for (f, F ) and (h, H) ∈ Hpair (U ), the energy integrand is integrable and

                         |Ba,U (G, H)| ≤ C2 qU (f, F ) qU (h, H).
      (3) There exists a separately quantified C3 ≥ 0 such that every K-bounded-
          linear total functional F has a variational solution (u, G) with

                                ∥(u, G)∥U ≤ C3 K,
  and every other variational solution (v, H) satisfies

                               d2U (u, G), (v, H) = 0.
                                                 

   The constants C2 and C3 are independent existential witnesses. Both uniqueness
clauses assert zero distance rather than literal equality.
RELATIVE FORMALIZATION IN ISABELLE/HOL OF A RESULT IN INVERSE PROBLEMS
                                                                    155

                                     References
 [1] C. I. Cârstea, On the Calderón problem with piecewise polynomial anisotropic con-
     ductivities and many-flat-face interfaces, arXiv:2606.15977, 2026.
 [2] T. Tao, Mathematics in the age of AI, arXiv:2608.16753, 2026.
 [3] S. Armstrong and J. Kempe, Formalization of De Giorgi–Nash–Moser theory in Lean,
     arXiv:2604.05984, 2026.
 [4] D. Bryant, J. J. Huerta y Munive, C. Kaliszyk, and J. Urban, Munkres’ General
     Topology Autoformalized in Isabelle/HOL, arXiv:2604.07455, 2026.
 [5] R. Cornish, I. Ghinassi, P.-H. Yeh, S. Liu, Q. Xu, H. Yin, D. Wagner, W. Li,
     Y. W. Teh, and L. Ong, FaithformBench: Benchmarking Faithfulness of Mathematical
     Chain-of-Thought Autoformalisation, arXiv:2608.10916, 2026.
 [6] G. Cunningham, R. Bunescu, and D. Juedes, Towards Autoformalization of Mathe-
     matics and Code Correctness: Experiments with Elementary Proofs, in Proceedings
     of the 1st Workshop on Mathematical Natural Language Processing, pp. 25–32, Asso-
     ciation for Computational Linguistics, 2022.
 [7] K. Kappelmann, M. Schäffeler, L. Stevens, M. Abdulaziz, A. Popescu, and D. Traytel,
     Just Type It in Isabelle! AI Agents Drafting, Mechanizing, and Generalizing from
     Human Hints, arXiv:2604.15713, 2026.
 [8] W. Ma, A. Cojocaru, N. Kolhe, H. Zhang, V. Zhuang, M. Zaharia, and S. Min,
     Reliable Fine-Grained Evaluation of Natural Language Math Proofs, in International
     Conference on Learning Representations (ICLR), 2026.
 [9] J. K. Miller, A Formalization of the Mean-Field Derivation of the Vlasov Equation:
     AI-Assisted Lean Formalization as a Strategy Game, arXiv:2607.08986, 2026.
[10] I. Petrov, J. Dekoninck, D. I. Dimitrov, and M. Vechev, Not All Proofs Are Equal:
     Evaluating LLM Proof Quality Beyond Correctness, arXiv:2605.10379, 2026.
[11] N. Sothanaphan, Resolution of Erdős Problem #728: a writeup of Aristotle’s Lean
     proof, arXiv:2601.07421, 2026.
[12] Y. Zhang, Y. Sun, T. Suzuki, J. D. Lee, and F. Liu, LeanMarathon: To-
     ward Reliable AI Co-Mathematicians through Long-Horizon Lean Autoformalization,
     arXiv:2606.05400, 2026.
[13] N. Garg, EconCSLib: AI-Assisted Lean Formalization for Economics & Computation
     Research, arXiv:2606.13306, 2026.
[14] K. Weng, L. Du, S. Li, W. Lu, H. Sun, H. Liu, and T. Zhang, Autoformalization in
     the Era of Large Language Models: A Survey, arXiv:2505.23486, 2025.
[15] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jamnik, and C. Szegedy,
     Autoformalization with Large Language Models, in Advances in Neural Information
     Processing Systems, vol. 35, pp. 32353–32368, 2022.
[16] K. Zhang, P. Gallardo Candela, S. Murthy, Y. Xie, Z. Wang, and M. Raissi, Beyond
     Compilation: Evaluating Faithful Natural-Language-to-Lean Statement Formalization,
     arXiv:2606.31002, 2026.
[17] J. Zhang, C. Zhong, H. Xu, Q. Li, and Y. Zhou, KELPS: A Framework
     for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment,
     arXiv:2507.08665, 2025.
[18] L. Zhang, M. Valentino, and A. Freitas, Autoformalization in the Wild: Assessing
     LLMs on Real-World Mathematical Definitions, in Proceedings of the 2025 Conference
     on Empirical Methods in Natural Language Processing, pp. 1720–1738, Association for
     Computational Linguistics, 2025.
[19] L. Hörmander, The Analysis of Linear Partial Differential Operators I: Distribu-
     tion Theory and Fourier Analysis, Grundlehren der mathematischen Wissenschaften,
     vol. 256, Springer-Verlag, Berlin–Heidelberg–New York–Tokyo, 1983.
[20] L. C. Evans, Partial Differential Equations, 2nd ed., Graduate Studies in Mathemat-
     ics, vol. 19, American Mathematical Society, Providence, RI, 2010.
156                            CĂTĂLIN I. CÂRSTEA

[21] H. Kang and K. Yun, Boundary determination of conductivities and Riemannian
     metrics via local Dirichlet-to-Neumann operator, SIAM J. Math. Anal. 34 (2003),
     no. 3, 719–735. doi:10.1137/S0036141001395042.
[22] M. Lassas, M. Taylor, and G. Uhlmann, The Dirichlet-to-Neumann map for complete
     Riemannian manifolds with boundary, Comm. Anal. Geom. 11 (2003), no. 2, 207–221.
     doi:10.4310/CAG.2003.v11.n2.a2.
[23] W. McLean, Strongly Elliptic Systems and Boundary Integral Equations, Cambridge
     University Press, Cambridge, 2000.

  Department of Applied Mathematics, National Yang Ming Chiao Tung Uni-
versity, Hsinchu 30050, Taiwan
  Email address: catalin.carstea@gmail.com
