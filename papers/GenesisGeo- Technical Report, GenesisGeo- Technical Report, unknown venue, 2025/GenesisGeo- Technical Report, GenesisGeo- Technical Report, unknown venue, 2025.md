                                                   ZJUVAI
                                                   VISUAL ANALYTICS AND INTELLIGENCE GROUP



                                                                 GenesisGeo: Technical Report
                                         Minfeng Zhu1 , Zi Wang1 , Sizhe Ji1 , Zhengtong Du1 , Shengqiang Tai2 , Junming
                                         Ke3 , Xiao Deng3 , Zanlang Yin4 , Xiuqi Huang1 , Heyu Wang5 , and Wei Chen1
                                                             1
                                                          State Key Lab of CAD&CG, Zhejiang University
                                                             2
                                                               Polytechnic Institute, Zhejiang University
                                                 3
                                                   Hangzhou Research Institute of AI and Holographic Technology
arXiv:2509.21896v2 [cs.AI] 22 Feb 2026




                                                                   4
                                                                     Volkswagen Group Innovation
                                                      5
                                                        School of Mathematical Science, Zhejiang University
                                             {minfeng_zhu, zi_wang, sizhe_ji, zhengtongdu, shengqiangtai,
                                                        huangxiuqi, wangheyu, chenvis}@zju.edu.cn
                                                {junmingke, xiaodeng}@zjuqx.com, zanlang.yin@gmail.com

                                                                                      Abstract
                                                  Recent neuro-symbolic geometry theorem provers have made significant progress
                                                  on Euclidean problems by coupling neural guidance with symbolic verification.
                                                  However, most existing systems operate almost exclusively in a symbolic space,
                                                  leaving diagram-based intuition largely unused during reasoning. For humans,
                                                  geometric diagrams provide essential heuristics for identifying non-trivial auxiliary
                                                  constructions. Meanwhile, visual language models (VLMs) still struggle with ge-
                                                  ometry due to the lack of high-quality data with geometric diagrams and reasoning
                                                  supervision. In this paper, we introduce G ENESIS G EO -1M, a large-scale synthetic
                                                  dataset for visual geometric reasoning that contains 1M multimodal geometry
                                                  problems paired with machine-checkable proof traces. Building on this dataset,
                                                  we formulate geometric learning as a multi-task training paradigm that jointly
                                                  optimizes text-based proof generation and diagram-grounded proof generation,
                                                  encouraging models to learn visual grounding and symbolic deduction. Extensive
                                                  experiments show that our G ENESIS G EO -2B model achieves gold-medal-level per-
                                                  formance on Olympiad geometry benchmarks, solving 29/30 problems on IMO-30,
                                                  63/95 on IMO-95, and 278/409 on HAGeo-409.


                                         1   Introduction
                                         Automated theorem proving in Euclidean geometry has made remarkable progress in recent
                                         years Trinh et al. (2024); Duan et al. (2025); Chen et al. (2025). Neuro-symbolic systems such
                                         as AlphaGeometry2 can reach gold-medal-level performance Chervonyi et al. (2025). These systems
                                         show that combining language-guided auxiliary construction search with symbolic deduction can
                                         support long-horizon geometric proofs. However, most existing methods solve problems primarily
                                         in a textual space. They encode the problem in a formal language, guide auxiliary construction
                                         search using language- or heuristic-based priors, and verify conclusions via symbolic deduction. This
                                         workflow overlooks visual cues (e.g., symmetry, alignment, concurrency, and cyclic patterns) that
                                         often suggest the correct auxiliary construction in Olympiad geometry.
                                         In human problem-solving, diagrams serve as a perceptual workspace for forming hypotheses,
                                         checking constraints, and identifying useful auxiliary constructions. Experienced mathematicians
                                         often use visual cues to choose auxiliary constructions before writing a proof. This visual intuition is
                                         central to Olympiad geometry, where a solution often depends on adding the right auxiliary point, line,
                                         or circle. In contrast, current VLMs remain unreliable on geometry problems with diagrams Pan et al.
(2025); Lu et al. (2024). One reason is the lack of large-scale multimodal geometry data that pairs
diagrams with machine-checkable proof traces. Existing multimodal datasets rarely expose models to
the full reasoning pipeline required for Olympiad geometry, from perceptual pattern recognition to
auxiliary construction and formal verification. This disconnect prevents models from learning how
visual evidence informs symbolic planning in long-horizon proofs. As a result, current systems often
fail to discover non-obvious auxiliary constructions that are critical for solving competition-level
problems.
To address this gap, we introduce G ENESIS G EO -1M, a large-scale synthetic dataset for visual
geometric reasoning with verified proof supervision. We enable this scale by reimplementing the
symbolic deduction engine in C++ and equipping it with a carefully curated rule set (e.g., the
secant theorem) that improves both deductive capability and runtime efficiency. Building on this
engine, we develop an automated synthesis pipeline that generates challenging Olympiad-style
problems. The pipeline samples construction-based problems, performs symbolic reasoning to obtain
a formally checkable proof trace with the necessary auxiliary constructions, and renders the geometry
constructions into a diagram with deterministic grounding of symbolic objects in the visual space.
Each example includes a problem statement, a diagram, and a step-by-step symbolic proof trace.
This design tightly aligns visual representations, symbolic premises, auxiliary constructions, and
proof steps, enabling models to learn how perceptual cues inform formal deduction. Compared to
prior datasets Gao et al. (2025); Wu et al. (2025), G ENESIS G EO -1M provides large-scale multimodal
geometry problems that enable long-horizon, diagram-grounded geometric reasoning.
In addition, we introduce G ENESIS G EO -2B, a multimodal geometry model trained with a multi-task
learning strategy, including text-based proof generation, and diagram-grounded proof generation.
These tasks share the same underlying geometry but provide complementary supervision signals:
text-based proof generation strengthens symbolic rigor without relying on visual shortcuts, and
diagram-grounded proof generation teaches the model to use visual evidence when proposing auxiliary
constructions. We fine-tune strong vision-language backbones on G ENESIS G EO -1M under this multi-
task training strategy. Experiments show consistent gains on established geometry benchmarks. In
particular, G ENESIS G EO -2B solves 29/30 problems on IMO-30, 63/95 on IMO-95, and 278/409 on
HAGeo-409, suggesting that large-scale multimodal supervision improves diagram understanding
and symbolic reasoning.
In summary, our contributions are fourfold:
• We release G ENESIS G EO -1M, a multimodal geometry dataset with diagrams and machine-
  checkable proof traces for visual geometric reasoning.
• We propose a multi-task training strategy that jointly learns diagram understanding, text-based
  proof generation, and diagram-grounded proof generation.
• We conduct extensive experiments on established geometry benchmarks and demonstrate substan-
  tial gains after fine-tuning on G ENESIS G EO -1M.
• We provide a new solution to IMO 2008 Problem 6 that requires only two auxiliary points,
  simplifying AlphaGeometry-based solutions.


2     Related Work

2.1   Geometry Problem Solving

Automated geometric reasoning has a long history, progressing from algebraic elimination to symbolic
proof systems and, more recently, neuro-symbolic approaches.
Algebraic and symbolic solvers. Early works on automated geometry translate geometric con-
straints into algebraic elimination, including Wu’s method and related mechanical theorem-proving
systems Wu (1978); Chou (1988), as well as Gröbner-basis procedures Kapur (1986). These algebraic
approaches can be computationally efficient, but the resulting proofs are often difficult for humans
to interpret. Alternative lines of work aimed to produce human-readable proofs, notably the area
method Chou et al. (1993) and deductive databases Chou et al. (2000). Recent work shows that hand-
crafted symbolic heuristics can outperform classic methods on Olympiad-level benchmarks Duan
et al. (2025). However, purely symbolic search can become inefficient when auxiliary constructions
rapidly expand the search space.


                                                 2
Neuro-symbolic solvers. Recent approaches address search explosion by integrating deep neural
networks for auxiliary construction proposal. AlphaGeometry couples a deductive database with
an algebraic engine and trains a language model on synthetic textual corpora to suggest auxiliary
points Trinh et al. (2024). Subsequent systems enhance the symbolic engine and data construction
(e.g., TongGeometry Zhang et al. (2026), SeedProver Chen et al. (2025), and AlphaGeometry2 Cher-
vonyi et al. (2025)), solving the full IMO-30 set and achieving high success rates over broader
collections of IMO problems. For example, TongGeometry applies tree search to explore auxiliary
constructions Zhang et al. (2026). AlphaGeometry2 extends the domain-specific language with
dynamic point moves and linear relations, achieving an 84% success rate on IMO problems from
2000–2024 Chervonyi et al. (2025). Despite these advances, most approaches still operate on sym-
bolic inputs, without exploiting rich visual cues. We aim to learn construction-relevant auxiliary
proposals from visual diagram evidence.

2.2   Multimodal Geometric Reasoning

Multimodal models such as ChatGPT and Gemini perform well on general vision tasks but remain
unreliable at parsing geometric diagrams and performing multi-step reasoning Wang et al. (2024).
Specialized models aim to close this gap by improving either understanding or reasoning.
Understanding-oriented work improves the mapping from pixels to geometric primitives and
relations. G-LLaVA Gao et al. (2025) synthesizes geometric vision-language data to provide MLLMs
with fundamental geometric knowledge. GeoVLMath uses cross-modal rewards to better ground
auxiliary-line descriptions in the diagram Guo et al. (2025). MathMathCoder-VL, trained with
ImgCode-8.6M, leverages code as supervision for cross-modal alignment and understanding Wang
et al. (2025).
Reasoning-oriented work introduces step-by-step supervision to encourage multi-step deduction.
Datasets such as GeoThought and GPSM4K provide intermediate reasoning traces and improve
performance under chain-of-thought style training Shi et al. (2025); Jaiswal et al. (2024). Ge-
oGen highlights hallucination issues in direct multimodal reasoning and proposes neuro-symbolic
integration with translation and verification components Pan et al. (2025).
In contrast to prior work, we aim to push multimodal geometric reasoning to IMO-level difficulty by
leveraging a multi-task training strategy that learns geometric visual cues while a symbolic engine
verifies logical soundness.

2.3   Geometry Datasets

Geometry datasets broadly fall into (1) textural datasets that teach symbolic deduction and (2)
multimodal datasets that pair diagrams with questions and proof traces.
Textural datasets. Large synthetic corpora have been central to recent neuro-symbolic provers.
AlphaGeometry trains language models on 100M problems to learn auxiliary-construction priors
and guide symbolic search Trinh et al. (2024). Follow-up systems scale the generation pipeline and
search procedure (e.g., TongGeometry Zhang et al. (2026) and GeoGen Bak et al. (2020)) to further
improve coverage and robustness. These corpora are effective for geometric reasoning in symbolic
space, but they omit diagrams and therefore cannot teach the perceptual cues that humans rely on
when selecting constructions.
Multimodal datasets. Human-curated benchmarks such as Geometry3K and GeoQA provide
diagrams paired with formal annotations or executable programs Lu et al. (2021); Chen et al. (2021).
Further, UniGeo unifies calculation and proving tasks with proving and program sequences that
shares the same format Chen et al. (2022). AuxSolidMath curates exam-style problems with paired
diagrams and aligned text for auxiliary-line reasoning Guo et al. (2025). For scaling multimodal
training, Geo170K supplies diagram-text pairs Gao et al. (2025) and GeoThought further provide
detailed thinking processes during problem-solving Shi et al. (2025). Recently, researchers employ a
neuro-symbolic framework for generating geometric reasoning data (e.g., NeSyGeo Wu et al. (2025),
GeoGen Pan et al. (2025), TrustGeoGen Fu et al. (2025)).
Despite rapid progress, the field still lacks large-scale multimodal training data at IMO-level difficulty.
We introduce G ENESIS G EO -1M dataset with diagram-text pairs and machine-checkable proof traces,
which enables gold-medal-level performance on Olympiad geometry benchmarks.


                                                    3
3   Preliminary of Symbolic Engine
This section introduces our symbolic engine, which operates over two geometry-specific DSLs, and
performs forward closure via a Deductive Database and Algebraic Reasoning (DDAR) procedure.
We also apply several accelerations to support large-scale generation.
Geometry–specific languages. A symbolic geometry engine requires explicit formal languages for
geometric constructions and predicate descriptions. The construction language defines geometric
elements (e.g., points, lines, and circles) with commands such as rectangle A B C D and circle
O A B C. The predicate language describes geometric facts over points, such as congruence (cong
O A O C) and parallelism (para A B C D).
DDAR engine. DDAR combines a rule-based deductive database Chou et al. (2000) with an algebraic
reasoning module. The DD component applies rules of the form P1 , . . . , Pm → Pnew to derive
new predicates, repeating rule matching until no new predicates can be inferred. The AR module
maintains quantitative constraints (e.g., lengths and ratios) as linear equations and uses Gaussian
elimination to derive additional equalities. Together, DDAR can compute a complete closure of
deducible facts.
Engine enhancement. We enhance the symbolic engine to increase its reasoning capacity through
refined deductive rules and an improved arithmetic equation solver.
Rule Reduction. The primary motivation for pruning the baseline rule set is to optimize computational
efficiency during rule matching. In automated theorem proving, an excessive number of candidate
rules at each step can exponentially inflate the search space. Therefore, we eliminate redundant rules
that are compositional (i.e., derivable from other rules) or logically trivial (e.g., describing simple
algebraic symmetries already implemented by the AR engine).
Rule Expansion. Conversely, the introduction of new rules (marked with * in Table 1) is driven by the
need to enhance geometric expressivity. The baseline rule set treats some metric facts, such as equal
distances, in a purely algebraic way. Our new constructive rules (e.g., Circumcenter Definition) serve
as semantic bridges that convert these metric constraints into explicit geometric objects (e.g., circles).
We also incorporate hierarchical reasoning shortcuts, such as promoting similarity to congruence
when a unit scale factor is detected. These rules bypass redundant searches for elementary congruence
conditions, such as SSS (Side-Side-Side) and SAS (Side-Angle-Side). Finally, axiomatic rules like
Unique Intersection ensure rigorous handling of point-identity scenarios. Table 1 shows the full rule
set used in our GenesisGeo engine.
Notation. We use the following notation in the deductive rules:

       • ⊙(ABCD): Points A, B, C, D are cyclic.
       • ⊙(O; A): Circle with center O and radius OA.
       • ABC: True if Points A, B, C are collinear.
       • Mid(M, AB): Point M is the midpoint of segment AB.
       • AB : CD: The ratio of the length of segment AB to the length of segment CD.
       • A ⇒ B: Means if A is true then B is true.
       • O(ABC): Represents the winding order of points A, B, C, used to distinguish between
         direct and reflective symmetry.
       • △ABC ∼ △DEF : Two triangles are similar and have the same orientation.
                   R
       • △ABC ∼ △DEF : Two triangles are similar as mirror images (opposite orientation).
       • △ABC ∼
              = △DEF : Two triangles are congruent and have the same orientation.
                   R
       • △ABC ∼
              = △DEF : Two triangles are congruent as mirror images (opposite orientation).
       • ∠ABC = ∠DEF : The directed angle from line AB to BC is congruent to the one from
         line DE to EF modulo π.
       • ∧: Logical AND, true only if all connected conditions are true.
       • ¬: Logical NOT, reverses the truth value of a statement.


                                                    4
Table 1: The full set of deductive rules used in GenesisGeo. Newly introduced rules are marked with
an asterisk (*)
 Rule Name                                    Logical Implication

 I. Fundamental Incidence, Lines & Parallelism

 Line Definition by Parallelism               ABC ⇒ AB ∥ BC
 Collinearity of Parallel Lines               AB ∥ AC ⇒ ABC
 * Line Intersection Axiom                    P AB ∧ QAB ∧ P CD ∧ QCD ∧ ¬ABD ⇒ P = Q
 Pappus’s Hexagon Theorem                     ABC ∧ PQR ∧ XAQ ∧ XP B ∧ Y AR ∧ Y P C ∧ ZBR ∧ ZCQ ⇒ XY Z
 Intercept Theorem                            AB ∥ CD ∧ OAC ∧ OBD ⇒ OA:OC = OB :OD
 Converse of Intercept Theorem                OA:OC = OB :OD ∧ OAC ∧ OBD ∧ ¬ABC ⇒ AB ∥ CD
 Intercept Theorem (Trapezoid)                AB ∥ CD ∧ M AD ∧ N BC ∧ MA:MD = NB :NC ⇒ MN ∥ AB
 Proportional Transversals Theorem            AB ∥ CD ∧ M AD ∧ N BC ∧ MN ∥ AB ⇒ MA:MD = NB :NC

 II. Metric Relations & Circles

 Definition of Midpoint                       AM = BM ∧ M AB ⇒ Mid(M, AB)
 Property of Midpoint                         Mid(M, AB) ⇒ M AB
 Midpoint Ratio Property                      Mid(M, AB) ⇒ AM :AB = 1:2
 * Segment Ratio Property                     ABC ∧ DEF ∧ AB :AC = DE :DF ⇒ AB :BC = DE :EF
 * Radii of Circle                            A, B, C ∈ ⊙(O; A) ⇒ OA = OB = OC
 * Definition of Circumcenter                 OA = OB = OC ⇒ A, B, C ∈ ⊙(O; A)
 Concyclic Equidistance Property              A, B, C ∈ ⊙(O; A) ∧ ⊙(ABCD) ⇒ OA = OD
 Equidistance Criterion                       OA = OB ∧ OC = OD ∧ ⊙(ABCD) ∧ AB ∦ CD ⇒ OA = OC
 Inscribed Angle Theorem                      ⊙(ABPQ) ⇒ ∠APB = ∠AQB
 Converse of Inscribed Angle Theorem ∠APB = ∠AQB ∧ ¬ABP ⇒ ⊙(ABPQ)
 * Definition of Secant Line                  PAB ∧ OA = OB ⇒ PAB is a secant of ⊙ (O; A)

 III. Triangle Properties

 Angle Bisector Theorem                       DB :DC = AB :AC ∧ DBC ∧ ¬ABC ⇒ ∠BAD = ∠DAC
 Converse of Angle Bisector Theorem           ∠BAD = ∠DAC ∧ DBC ∧ ¬ABC ⇒ DB :DC = AB :AC
 Median to Hypotenuse Theorem                 AB ⊥ BC ∧ Mid(M, AC) ⇒ AM = BM
 Concurrency of Altitudes                     AB ⊥ CD ∧ AC ⊥ BD ⇒ AD ⊥ BC
 Concurrency of Angle Bisectors               ∠BAX = ∠XAC ∧ ∠ABX = ∠XBC ∧ ¬ABC ⇒ ∠BCX = ∠XCA

 IV. Similarity & Congruence

 Definition of Similarity      Direct         △ABC ∼ △PQR ⇒ ∠ABC = ∠PQR ∧ AB :BC = PQ:QR
                                                      R
                               Reflective     △ABC ∼ △PQR ⇒ ∠ABC = ∠PQR ∧ AB :BC = PQ:QR
 * Unit Ratio Similarity     Direct           △ABC ∼ △PQR ∧ AB = PQ ⇒ △ABC ∼
                                                                           = △PQR
                                                                                   R
                                              △ABC ∼ △PQR ∧ AB = PQ ⇒ △ABC ∼
                                                      R
                             Reflective                                    = △PQR
 * CPCTC                       Direct              ∼ △PQR ⇒ AB = PQ ∧ △ABC ∼ △PQR
                                              △ABC =
                                                      R
                                              △ABC ∼
                                                                                   R
                               Reflective          = △PQR ⇒ AB = PQ ∧ △ABC ∼ △PQR
 AA Similarity Criterion       Direct         ∠ABC = ∠PQR ∧ ∠ACB = ∠PQR ∧ ¬ABC ∧ O(ABC ) = O(PQR) ⇒ △ABC ∼ △PQR
                                                                                                           R
                               Reflective     ∠ABC = ∠PQR ∧ ∠ACB = ∠PQR ∧ ¬ABC ∧ O(ABC ) ̸= O(PQR) ⇒ △ABC ∼ △PQR
 SSS Similarity Criterion      Direct         AB :BC = PQ:QR ∧ AC :BC = PR:QR ∧ ¬ABC ∧ O(ABC ) = O(PQR) ⇒ △ABC ∼ △PQR
                                                                                                                   R
                               Reflective     AB :BC = PQ:QR ∧ AC :BC = PR:QR ∧ ¬ABC ∧ O(ABC ) ̸= O(PQR) ⇒ △ABC ∼ △PQR
 SAS Similarity Criterion      Direct         AB :BC = PQ:QR ∧ ∠ABC = ∠PQR ∧ ¬ABC ∧ O(ABC ) = O(PQR) ⇒ △ABC ∼ △PQR
                                                                                                               R
                               Reflective     AB :BC = PQ:QR ∧ ∠ABC = ∠PQR ∧ ¬ABC ∧ O(ABC ) ̸= O(PQR) ⇒ △ABC ∼ △PQR




Arithmetic Rules. While the deductive engine handles qualitative geometric logic, the Algebraic
Reasoning (AR) engine provides a quantitative foundation by converting geometric constraints into
canonical arithmetic forms. This section details the mapping logic in Table 2 and the computational
optimizations employed to maintain efficiency within the joint deduction loop.
To bridge the gap between symbolic predicates and numerical constraints, we define a mapping M
that translates high-level geometric relations into algebraic equations (Table 2).

         • Linear Constraints: Predicates such as coll (collinearity) and para (parallelism) are
           linearized using the concept of directed angles. For example, an angle equality ∠(l1 , l2 ) =
           ∠(l3 , l4 ) is transformed into:
                                            dir(l1 ) + dir(l4 ) − dir(l2 ) − dir(l3 ) = 0     (mod π)


                                                                     5
       • Metric and Complex Constraints: Distance-based predicates (cong, eqratio) and complex
         relations (secant) are mapped to logarithmic equations or polynomial identities (e.g., Power
         of a Point Theorem).

Together, these enhancements keep the engine symbolic and efficient, while expanding its deductive
closure to cover exponential constraints.

                                Table 2: Catalog of Arithmetic Equations

 Predicate                  Equation
 coll A B C              ∠(AB) = ∠(AC) = ∠(BC)
                         AB + BC = AC       (if B lies on segment AC)
 aconst A B C D r        ∠(CD) − ∠(AB) = r
 cong A B C D            AB = CD
                         log(AB) = log(CD)
                         ∠(AB) + ∠(AD) = 2 · ∠(BD)     (if C equals to A)
 eqangle A B C D E F G H ∠(AB) − ∠(cD) = ∠(EF ) − ∠(GH)
 eqratio A B C D E F G H AB · GH = CD · EF
                         log(AB) − log(CD) = log(EF ) − log(GH)
 para A B C D            ∠(AB) = ∠(CD)
 perp A B C D            ∠(AB) − ∠(CD) = π/2
                         AB 2 + AD2 = BD2      (if C equals to A)
 rconst A B C D r        AB = CD · r
 secant O A B P          P A · P B − P O2 = OA2 = OB 2    (if P lies on segment AB)
                         P O2 − P A · P B = OA2 = OB 2
                         (if P does not lie on segment AB)


Engine acceleration. A naive implementation of rule matching suffers from poor scalability due to
the combinatorial explosion of rule arguments. To improve scalability, we exploit two acceleration
strategies.
Numeric pre-identification. Predicates such as eqangle and eqratio require searching over 8-
point tuples. We precompute directions for all candidate segments, then keep only tuples that are
numerically equal. This step prunes the candidate set before symbolic matching.
Partial-matching pruning. The DD engine matches a rule’s predicates sequentially. If any intermediate
predicate cannot be satisfied, we stop matching the remaining predicates. This early-failure pruning
avoids exploring impossible combinations and reduces matching cost.
Finally, our optimized symbolic engine is roughly 20× faster than the AlphaGeometry engine. This
speed-up allows us to perform large-scale symbolic deduction within tight time budgets, supporting
both dataset generation and downstream search-based proving.

4     Automated Geometry Data Synthesis
In this section, we build a fully automated synthesis pipeline to create multimodal training data for
IMO-level geometry reasoning. Figure 1 summarizes the workflow. Given a sampled construction,
the pipeline runs DDAR to compute a closure of deducible statements, selects non-trivial goals
through predicate-aware filtering, traces back the dependency graph to extract minimal premises and
auxiliary constructions, and renders a diagram consistent with the underlying construction.

4.1   Geometry Problem Sampling

We generate candidate problems by sampling action sequences in a constructive DSL adapted from
AlphaGeometry Trinh et al. (2024). We organize construction actions into three groups. BASIC
initializes an anchor configuration using elementary primitives (e.g., segment, triangle, and rectangle).
INTERSECT introduces a new line or circle; pairing two such actions yields a uniquely defined
intersection point. OTHERS covers the remaining constructions (e.g., foot, incenter, and excenter).


                                                   6
      (1) Geometric     (2) Symbolic                 (3) Subproblem Extraction                            (4) Final Output
       Construction      Deduction
                                                                                                              <problem> a :; b :; c :perp
                                                                                Generate      Predicate DSL   a b a c [000] cong a b a c
                                                                              Predicate DSL                   [001] ; d :cyclic a b ...
                            Symbolic                Extract Minimal
      Random Sampling
                        Engine Deduction             Constructions


                          Conclusions                                         Draw Geometry     Geometry
                                                    Minimal Premises             Diagram        Diagram
                         coll a c f,
                         eqangle a c a
                         d b c b d,
                         cong a c c d                                           Auxiliary       Auxiliary     <aux> x00 g :perp a g b g
         Problem
                         ...                      Dependency Analysis   Aux   Constructions                   [008] cong c g d g [009] ;
                                                                                              Constructions
                                                                              Doublecheck                     </aux>
      a b c = risos a
      b c; d =                                        All Premises
      on circum d c b                                                                                         <proof> coll a c f [017]
      a, on pline d b                                                                                         r56 [007] ; eqangle a c a d
                            Filtering      Pass     Proof Traceback             Proof             Proof
      c a; e = on dia                                                                                         b c b d [018] r03 [002] ;
      e a b ...                                                                                               eqangle a d a f c f b c ...




Figure 1: Data synthesis pipeline. We first sample a construction program in our DSL to instantiate a
consistent geometric configuration. Then, our symbolic engine performs forward deduction from the
construction predicates to obtain a closure of conclusions. From this closure, we select non-trivial
targets via predicate-specific filtering and equivalence deduplication. For each selected goal, we
trace back the proof to extract minimal premises and candidate auxiliary constructions, followed
by a backward double-check that removes fake auxiliary points. Finally, we export each problem
in a unified multimodal format, including the construction DSL and geometry diagram <img>, the
predicate DSL <problem> , a refined auxiliary block <aux> , and a verifiable proof trace <proof> .


Procedure. We first sample a BASIC construction to form an initial backbone. Then, we grow
the backbone by adding constructions that introduce new lines or circles and their intersections.
Concretely, we repeatedly choose either (i) two INTERSECT actions that together determine a new
point, or (ii) one OTHERS construction that yields a new object. Finally, we optionally add intersections
among existing geometric objects (e.g., midpoints, feet, reflections, and circle interactions) to increase
structural dependency. Note that, before committing each construction, we run dependency checks to
ensure prerequisites are available and numerical checks to ensure a consistent coordinate realization
exists. These checks prevent invalid actions from propagating and improve generation throughput.

4.2     Symbolic Deduction and Filtering

Given a valid problem, we run the symbolic engine to compute a closure of conclusions. This closure
contains many predicates that are trivial or equivalent. To ensure that synthesized goals provide
meaningful learning signals, we apply a predicate-aware goal filtering procedure.
Predicate-specific filtering. The symbolic closure contains many candidate goals that are invalid
for training. We filter them with simple, predicate-dependent rules. We drop trivial statements that
hold by definition, such as self-relations (e.g., AB = AB and AB ∥ AB). We also remove goals
that can be directly rewritten into a simpler predicate. For example, ∠(AB, CD) = 0◦ is equivalent
to AB ∥ CD, and some ratio forms reduce to segment equality. Table 3 lists the exact patterns we
exclude for each predicate.
Equivalence filtering. We further deduplicate high-frequency predicates such as eqangle and
eqratio. Two eqangle goals are treated as equivalent when all corresponding line pairs are parallel.
Two eqratio goals are treated as equivalent when all corresponding segment pairs are congruent.
Through two-stage filtering process, we retain meaningful and non-redundant conclusions, ensuring
that the resulting problems are both challenging and valuable.

4.3     Subproblem Extraction

Given a goal, we employ a trace-back algorithm to identify the premises and auxiliary constructions
used in the proof.


                                                                        7
                         Table 3: Filtering criteria for geometric conclusions
 Predicate          Filtered Conclusion Type                            Reason for Filtering
 aconst             ∠(AB, CD) = 0◦                                      Reducible to AB ∥ CD
 rconst             AB : CD = 1                                         Reducible to AB = CD
 cong                  ∼ AB
                    AB =                                                Trivial self-congruence
 para               AB ∥ AB                                             Trivial self-parallelism
                    AB ∥ AC                                             Reducible to A, B, C are collinear
 eqratio            AB/CD = AB/CD                                       Trivial identical ratio
                    AB/CD = CD/AB                                       Reducible to AB = CD
                    AB/AB = CD/EF                                       Reducible to CD = EF
                    AB/CD = EF/GH where AB = CD                         Reducible to EF = GH
                    AB/CD = EF/GH where AB = EF                         Reducible to CD = GH
 eqangle            ∠(AB, CD) = ∠(AB, CD)                               Trivial identical angle
                    ∠(AB, CD) = ∠(CD, AB)                               Reducible to AB ⊥ CD
                    ∠(AB, AB) = ∠(CD, EF )                              Reducible to CD ∥ EF
                    Cases involving parallel lines                      Reducible to parallel relations
                    ∠(AB, CD) = ∠(EF, GH) where AB ⊥ CD                 Reducible to EF ⊥ GH
                    Cases involving triangle similarity                 Reducible to similarity relations
 simtri, simtrir    △ABC ∼ △ABC                                         Trivial self-similarity
 contri, contrir    △ABC ∼
                         = △ABC                                         Trivial self-congruence



Premise minimization. Starting from the goal node, we recursively collect only the parent predicates
required by each applied rule until reaching construction-derived facts. The resulting leaf set forms
the final premise set.
Auxiliaries minimization. An auxiliary construction is a construction step that is not required to
build the geometry problem, but is required by the proof. Concretely, during traceback we identify
objects that appear in the proof but cannot be uniquely determined from the extracted premise set.
We serialize the construction steps that introduce these objects in the <aux> block, enabling learning
settings that predict or verify auxiliary points.
The initial <aux> set may still contain redundant information, because the symbolic engine searches
for a shortest deductive path, which may temporarily introduce constructions that are not strictly
necessary for proving the target conclusion. To obtain a minimal auxiliary set, AlphaGeometry Trinh
et al. (2024) applies a provability check that repeatedly removes points and reruns DDAR, but an
exhaustive search over all subsets is exponential and infeasible at scale. AlphaGeometry2 Chervonyi
et al. (2025) discards points in a reverse-topological order, which requires only a linear number of
checks.
We follow the same pipeline and further improve efficiency by exploiting the fact that many syn-
thesized problems share the same premises and auxiliary candidates but differ only in their target
conclusions. Instead of checking each problem independently, we group problems with identical
premises and auxiliary sets and perform provability checks jointly. In practice, this batching strategy
accelerates the auxiliary revalidation process by approximately 5×, enabling efficient backward
verification at dataset scale.

4.4     Multimodal Data Format

Each synthesized example is stored as a single multimodal record that pairs a rendered diagram
with formal symbolic annotations and a verifiable derivation. In practice, one problem consists
of four parts: (1) a predicate DSL description that encodes the symbolic premises in a structured
<problem> block; (2) a <img> diagram that visualizes the geometric configuration; (3) an <aux>
block that lists auxiliary constructions required by the proof but not by the original problem; and (4) a
<proof> block that records the full proof trace, including an optional <numerical_check> section
with numerically obtained facts. Together, these fields provide aligned supervision for diagram
understanding, symbolic reasoning, auxiliary construction prediction, and proof generation.
For rendering, we assign Cartesian coordinates to all points during synthesis and draw the diagram
from these coordinates. The predicate-based Newclid rendering backend Sicca et al. (2024) fails


                                                   8
        20000


        17500


        15000


        12500
Count




        10000


         7500


         5000


         2500


            0
             1-4         20               40             60           80             100         120            140     160    180     >200
                                                                       Proof Steps
                   midp            coll, cyclic   coll, perp   cong, perp      cong             perp, perp     para, para       cong, para
                   cong, cong      coll, cong     coll, coll   cong, eqangle   cyclic, cyclic   cong, cyclic   eqangle, perp    others




                                Figure 2: Proof length distribution with auxiliary point types.



to visualize certain geometric objects, resulting in diagrams that are not aligned with the symbolic
constructions. For instance, the triangle construction defines vertices without predicates to render
connecting edges, while a circle is often defined only by two cong predicates (radius equality)
without triggering a circle object. To address this, we develop a construction-based rendering system
and optimize annotation sizing and color schemes for readability. Finally, we obtain a diagram with
precise pixel-level correspondence between symbolic objects and visual elements.



4.5       Dataset Statistics

We summarize corpus-level statistics of GenesisGeo-1M in Figure 2, which reports the distribution of
proof lengths and the composition of the top-15 auxiliary point types. A problem example is provided
in Figure 3. Overall, we highlight three properties of the dataset.
• Large-scale. The dataset contains 1 million synthesized problems that require auxiliary construc-
  tions, generated with 50 CPU threads over 28 hours.
• Multimodal and verifiable supervision. Each instance pairs a rendered diagram with formal
  construction DSL and predicate DSL descriptions, optional auxiliary constructions, and a complete
  DDAR proof trace. This format supports joint learning of perception, symbolic reasoning, and
  proof generation.
• High-difficulty signals. Problems are selected from DDAR-derivable but non-trivial goals after
  predicate-aware filtering and equivalence deduplication. We report difficulty proxies such as the
  number of premises, proof length and the fraction of instances that require auxiliary constructions,
  which correlate with longer dependency chains and Olympiad-style reasoning.


                                                                        9
      Problem in Constructions                     Problem
      a b c = r_triangle a b c;                    <problem>
      d = eqdistance d c b a, on_circum d a b c;   a: ;b: ;
      f g h e = excenter2 f g h e d a b            c : perp a b a c [000] ;
      ? cong b g e f                               d : cong a b c d [001] cyclic a b c d [002] ;
                                                   e : eqangle a d d e d e b d [003] eqangle a b b e b e b d [004] ;
                                                   f : coll a b f [005] perp a b e f [006] ;
                                                   g : coll b d g [007] perp b d e g [008] ;
      Image                                        h : coll a d h [009] perp a d e h [010]
                                                   ? cong b g e f
                                                   </problem>



                                                   Aux
                                                   <aux> x00 i : cong a i b i [011] cong b i c i [012] ; </aux>



                                                   Proof
                                                   <numerical_check> sameclock b f g f e g [013] ; sameclock a b i c i d [014] ; </numerical_check>
                                                   <trivial> cong f g f g [015] ; </trivial>
                                                   <proof>
                                                   cong a i c i [016] AR [011] [012] ;
                                                   coll b c i [017] AR [011] [016] [000] ;
                                                   midp i b c [018] r54 [017] [012] ;
                                                   eqangle a b a c b d c d [019] r03 [002] ;
                                                   perp b d c d [020] AR [019] [000] ;
                                                   cong c i d i [021] r19 [018] [020] ;
                                                   eqratio a b b i c d d i [022] AR [001] [012] [021] ;
                                                   eqratio a i b i c i d i [023] AR [011] [021] ;
                                                   simtrir a b i c d i [024] r61 [022] [023] [014] ;
                                                   eqangle a i b i d i c i [025] r53 [014] [024] ;
                                                   eqangle b f b g g e f e [026] AR [005] [007] [011] [016] [021] [019] [025] [000] [027] [028] ;
                                                   eqangle b g f g f e f g [029] AR [007] [011] [016] [021] [019] [025] [000] [027] ;
                                                   simtri b f g e g f [030] r34 [026] [029] [013] ;
                                                   contri b f g e g f [031] r101 [015] [030] ;
                                                   cong b g f e [032] r103 [031] ;
                                                   </proof>




Figure 3: An example of the synthetic data. The Problem in Construction section provides
the problem description in the construction DSL, upon which the Image is rendered. The Problem
section contains the problem translated into the predicate DSL, detailing the specific geometric
properties of each point. The <aux> section specifies the necessary auxiliary constructions. Finally,
the Proof block represents the entire deduction process: the <numerical_check> section contains
numerically obtained information and the <proof> session presents the complete sequence of proof
steps.


5     GenesisGeo: Multimodal Geometry Prover

We introduce GenesisGeo-2B, a multimodal neuro-symbolic prover that couples a VLM with a
symbolic engine.

5.1     Multi-Task Multimodal Learning

Our objective is to train the VLM to reliably propose auxiliary constructions that support symbolic
deduction across diverse geometric contexts. We adopt a multi-stage, multi-task learning framework,
as illustrated in Figure 4.
Stage I: Alignment-oriented continued pre-training. We first perform continued pre-training
on complete solution records generated by the symbolic engine. We frame learning over complete
solution records, where the rendered diagram <img>, the formal problem statement <problem>,
the auxiliary constructions <aux>, and the corresponding proof trace <proof> jointly serve as both
conditioning context and supervision. During this stage, all components are serialized into a unified
sequence and jointly modeled. This allows the VLM to learn the syntax of predicate-level geometry,
the structural patterns of auxiliary constructions, and the global organization of symbolic proofs.
Because all supervision is derived from a single symbolic engine, the model observes consistent
reasoning trajectories and avoids learning from heterogeneous or noisy explanations.
Stage II: Multi-task supervised fine-tuning. We fine-tune the VLM with instruction-tuning tasks
that enhance the capabilities needed for auxiliary construction, including text-based and vision-
grounded proof generation.
• Text-based auxiliary construction. Given predicate-level premises and a goal in <problem>, the
  model predicts a compact <aux> block. This task enforces symbolic planning without visual cues
  and trains the model to propose auxiliaries that facilitate symbolic deduction.
• Vision-grounded auxiliary construction. Conditioned on both <img> and <problem>, the
  model proposes a <aux> block that leverages geometric cues in the diagram while respecting the


                                                         10
                                 (1) Pre-Training Stage                                                                               (2) Multi-task SFT Stage
      ... </img>    <prob>   a    :   ... </prob>    <aux>    ...   <proof>   coll   a   ... </proof>   <end>
                                                                                                                                        <problem> a :; b
                                                                                                                                        :; c :perp a b a c
                                                                                                                                                                                     <aux> x00 g :perp
                                                                                                                   text-based proof     [000] cong a b a c
                                                                                                                                        [001] ; d :cyclic
                                                                                                                                                                                     a g b g [008] cong
                                                                                                                                                                                     c g d g [009] ;
                                                                                                                         generation
                                             Qwen3-VL                                                                                   a b c d [002] para
                                                                                                                                        a c b d [003] ; e
                                                                                                                                        :perp a e b e ...              Pre-trained
                                                                                                                                                                                     </aux>


                                                                                                                                                                          VLM




      Image Tokenizer                                         Text Tokenizer


                                 <problem> a :; b             <aux> x00        <proof> coll a c f                                                                                    <aux> x00 g :perp
                                                                                                                  vision-grounded                                                    a g b g [008] cong
                                 :; c :perp a b a c           g :perp a        [017] r56 [007] ;                                                                                     c g d g [009] ;
                                                                                                                  proof generation                                                   </aux>
                                 [000] cong a b a c           g b g            eqangle a c a d b c b                                    <problem> a :; b
                                                                                                                                        :; c :perp a b a c             Pre-trained
                                 [001] ; d :cyclic            [008]            d [018] r03 [002] ;                                      [000] cong a b a c                VLM
                                                                                                                                        [001] ; d :cyclic
                                 a b c d [002] para           cong c g         eqangle a d a f c f b                                    a b c d [002] para
                                 a c b d [003] ; e            d g [009]        c [019] AR [017]                                         a c b d [003] ; e
                                                                                                                                        :perp a e b e ...
                                 :perp a e b e ...            ; </aux>         [018] [003] ...




Figure 4: Multi-stage and multi-task learning framework. We first conduct proof-oriented continued
pre-training on complete solution records to align visual diagrams with the predicate language. Then,
we perform supervised multi-task fine-tuning for auxiliary construction, including text-based and
vision-grounded settings, enabling robust proposals that integrate symbolic planning with visual
grounding.


  symbolic constraints. This task combines visual grounding with symbolic planning for auxiliary
  construction.

5.2     Neuro-Symbolic Inference

GenesisGeo follows an iterative propose-and-verify loop for geometry problem solving. The process
begins with the formalized geometry problem. Initially, the symbolic engine attempts to derive the
target conclusion directly from the premises. If the goal is not reachable, the system invokes the
visual language model (VLM) to bridge the deductive gap.



                   Problem
                                                                                                            Problem
                                                                            Auxiliary                         with                                                            Yes
                    draw                                                                                                         DDAR                        Solved?                 Done
                                                                          Constructions                     Auxiliary
                                                                                                          Constructions
                                                    VLM
                   Image
                                                                                                                                                                 No




                                                             Figure 5: Proving Pipeline of VLM Prover.

As illustrated in Figure 5, our pipeline first renders the problem into a pixel-aligned diagram. The
VLM processes both the symbolic problem statement and the generated image, grounding abstract
logical constraints in visual features to propose candidate auxiliary constructions. These visually
informed candidates are then incorporated into the premise set, and the symbolic engine resumes
deduction. This cycle repeats iteratively, allowing the VLM to apply learned perceptual heuristics to
guide the symbolic solver through the search space of auxiliary constructions. Once the goal becomes
deducible, the proof is accepted.
In our training corpus, about 90% of problems require only one auxiliary point, whereas difficult
instances demand a deeper search to discover effective constructions. Simply accumulating all
proposed auxiliaries in <aux> can deviate from the training distribution. Thus, we adopt an alternative
prompting strategy: once an auxiliary point is validated, we fold it into <problem> and re-prompt
the VLM to propose the next auxiliary. This keeps <aux> lightweight while improving performance
on difficult problems.
To improve efficiency, we employ a parallel beam search strategy in which the language model
proposes multiple candidate constructions per iteration, retaining the highest-scoring options for
subsequent deduction. Furthermore, we leverage Ray to establish an asynchronous resource pool:


                                                                                                        11
CPU resources occupied by completed problems are dynamically released and reassigned to pending
problems, enabling highly parallelized and resource-efficient proof search across large batches.


6      Experiments

Training configuration. Our GenesisGeo prover is built on the Qwen3-VL-2B architecture Bai et al.
(2025) and fine-tuned on G ENESIS G EO -1M with multi-task training. Training runs for one epoch
with batch size 256 and learning rate 1 × 10−4 using AdamW Loshchilov and Hutter (2019). All
experiments are conducted on a 64-core CPU machine with eight NVIDIA A100 GPUs.
Benchmarks. We evaluate our approach on three Euclidean-geometry benchmarks. IMO-30 from
AlphaGeometry Trinh et al. (2024) contains 30 Olympiad problems. IMO-95 is a subset sourced from
the Newclid repository Sicca et al. (2024), containing formalized IMO problems whose constructions
are supported by AlphaGeometry. HAGeo-409 is a larger benchmark of 409 problems covering high-
school and Olympiad-level geometry. For a fair comparison across provers, we exclude five problems
whose constructions are unsupported by AlphaGeometry, while keeping the original benchmark
name.
Evaluation configuration. We report the number of problems solved under multiple search bud-
gets. Following HAGeo Duan et al. (2025), we report three budgets for symbolic engines: Low
(Pass@2048), Medium (Pass@4096), and High (Pass@8192). At each attempt, the solver samples
auxiliary points using HAGeo’s heuristic, runs the symbolic engine once, and repeats for a fixed
number of engine calls. In addition, we evaluate a tree-search setting for the neuro-symbolic solver,
where a large model proposes auxiliary constructions to expand the search tree. Here, 32×512×4
denotes batch size 32, beam size 512, and proof depth 4, jointly controlling the number of tree-search
expansions. These two budgets are not directly comparable: Pass@K counts engine calls with
heuristic sampling, while 32 × 512 × 4 controls the number of model-proposed expansions in a
depth-4 tree search. Each solver is allotted a 60-minute time limit per problem.


Table 4: Performance comparison on IMO and HAGeo benchmarks under different search budgets.
      Method                       Model Size   Search Budget   IMO-30      IMO-95      HAGeo-409
 Symbolic Engines
      AG2 (Engine)                     -              0           15           1            87
                                       -            2048          25          41           228
                                       -            4096          25          41           231
                                       -            8192          25          42           231
      Newclid 3.0                      -              0           16           2           104
                                       -            2048          23          47           241
                                       -            4096          23          50           245
                                       -            8192          23          51           249
      HAGeo                            -            4096          28           -             -
                                       -            8192           -           -           287
      GenesisGeo (Engine)              -              0           16           2           103
                                       -            2048          26          56           264
                                       -            4096          26          59           268
                                       -            8192          26          59           270
 Model-based Provers
      AG1                            151M        32×512×4         25          11           112
      AG2                            3.3B           N/A           30           -            -
      TongGeometry                   1.3B           N/A           30           -            -
      SeedProver                      N/A           N/A           30           -            -
      GenesisGeo (Text)               2B         32×512×4         28          59           270
      GenesisGeo (Vision + Text)      2B         32×512×4         29          63           278




6.1     Main Results

Table 4 reports the number of solved problems under multiple search budgets. We analyze the results
from three perspectives: (1) symbolic engines, (2) neuro-symbolic provers, and (3) failure modes on
hard problems.


                                                   12
Symbolic engines. First, we compare pure symbolic engines without auxiliary sampling. Our engine
matches Newclid, and both outperform AlphaGeometry2, indicating that our deductive engine is
competitive even without search. We also reimplement HAGeo-style heuristic sampling, where each
sampling contains 6 potential auxiliary points. As we increase the sampling budget from Low to
Medium to High, all engines solve more problems. With heuristic sampling enabled, our engine
consistently solves more problems across Low/Medium/High budgets on IMO-30, IMO-95, and
HAGeo-409. This gain is mainly driven by a stronger deductive and arithmetic rule set (Table 1).
For example, on IMO-30, our engine solves 26 problems under the High budget, compared to 25
for AlphaGeometry2 and 23 for Newclid. On HAGeo-409, our engine solves 270 problems under
the High budget, compared to 231 for AlphaGeometry2 and 249 for Newclid. However, we cannot
directly compare with HAGeo’s engine because its code is not publicly available.
Neuro-symbolic provers. Our solver achieves 29/30 on IMO-30 (Table 5) and maintains strong
performance on larger benchmarks. We evaluate two variants of our model: GenesisGeo (Text), which
is fine-tuned only on text-based proof generation tasks, and GenesisGeo (Vision + Text), which is
further fine-tuned on both text-based and diagram-grounded tasks. The result indicates that diagrams
provide useful geometric cues, enabling the model to propose more valid auxiliary constructions
and thereby improving tree search efficiency. AlphaGeometry2 and SeedProver do not release their
model checkpoints, which prevents a direct comparison.
Failure cases. The remaining unsolved problems often require deeper auxiliary-construction chains
than our current search depth. For example, AlphaGeometry2 reports that IMO 2008 Problem 6 and
IMO 2021 Problem 3 require more than ten auxiliary points, far beyond our default search depth.
We also observe failures when the required construction is rare in the training data or when a small
number of early mistakes leads the search into invalid branches. During development, we found an
alternative solution for IMO 2008 Problem 6 that uses only two auxiliary points. The correctness of
the proof is confirmed by an IMO gold medalist. To the best of our knowledge, this solution differs
from the official solution, the AlphaGeometry2 solution, and other publicly reported solutions. We
include the full proof in the appendix (Section A).

Table 5: Performance comparison of AlphaGeometry 1 (AG1) and GenesisGeo (Genesis) on IMO-30.

 ID          AG1     Genesis          ID          AG1    Genesis           ID        AG1     Genesis
 2000 P1      ✓        ✓              2008 P1b     ×       ✓               2015 P3    ✓        ✓
 2000 P6      ✓        ✓              2008 P6      ×       ✓               2015 P4    ✓        ✓
 2002 P2a     ✓        ✓              2009 P2      ✓       ✓               2016 P1    ✓        ✓
 2002 P2b     ✓        ✓              2010 P2      ✓       ✓               2017 P4    ✓        ✓
 2003 P4      ✓        ✓              2010 P4      ✓       ✓               2018 P1    ✓        ✓
 2004 P1      ✓        ✓              2011 P6      ×       ✓               2019 P2    ×        ✓
 2004 P5      ✓        ✓              2012 P1      ✓       ✓               2019 P6    ✓        ✓
 2005 P5      ✓        ✓              2012 P5      ✓       ✓               2020 P1    ✓        ✓
 2007 P4      ✓        ✓              2013 P4      ✓       ✓               2021 P3    ×        ×
 2008 P1a     ✓        ✓              2014 P4      ✓       ✓               2022 P4    ✓        ✓


6.2   Ablation Studies

To understand the contribution of each component, we conduct a series of ablation studies on IMO-30
and IMO-95.
Multi-task learning. Our multi-task objective includes diagram understanding, text-based proof
generation, and diagram-grounded proof generation. To assess each task’s contribution, we train
models using single tasks and two-task combinations. Excluding diagram understanding reduces
success rates, while removing text-based tasks leads to less precise auxiliary construction suggestions.
The full task setting consistently performs best.
Training strategy. We investigate whether pre-training on G ENESIS G EO is necessary. We compare
(1) models trained only with pre-training (no SFT), (2) models trained from scratch on supervised
fine-tuning data only, and (3) models pre-trained on synthetic proofs and then fine-tuned. The results
demonstrate that combining pre-training and SFT yields the highest success rates.
Search budget. We vary the search budget of the neuro-symbolic solver to quantify the trade-off
between exploration and compute. Increasing the budget consistently improves the solve rate because


                                                  13
                                             Table 6: Ablation on multi-task training.

                                        Task mixture                              IMO-30 IMO-95
                                        Pre-trained Backbone                        27           52
                                        Text-based proof generation                 28           59
                                        Diagram-based proof generation              27           57
                                        All tasks                                   29           63

                                              Table 7: Ablation on training strategy.

                                                  Training               IMO-30 IMO-95
                                                  Pre-training only          27          52
                                                  SFT only                   27          57
                                                  Pre-training + SFT         29          63


the solver can test more candidate auxiliary constructions. Beyond 32 × 512 × 4, increasing the
search budget yields only marginal gains.


                             IMO-30
                 60
                             IMO-95
Problem Solved




                 50
                 40
                 30
                 20
                 10
                         2                     4                       8×4                         2×4        2×4
                   8×32×                  8×64×                  16×12                        32×51      64×51
                                                                 Search Budget


                                 Figure 6: Number of problem solved for different search budgets.


7                Conclusion
We present G ENESIS G EO -1M, a large-scale synthetic dataset for visual geometric reasoning that pairs
a rendered diagram with a verifiable symbolic proof trace. Our data-generation pipeline synthesizes
problems that require auxiliary constructions and aligns the symbolic objects used in proofs with
the corresponding visual elements, enabling models to exploit diagram evidence while producing
checkable proofs. Building on G ENESIS G EO -1M, we train multimodal G ENESIS G EO -2B model
with a multi-task learning strategy that combines text-based proof generation and diagram-grounded
proof generation. Experiments observe consistent improvements on standard geometry benchmarks.
Overall, our results suggest that large-scale multimodal supervision with unified objectives provides
a practical path toward connecting diagram understanding with verifiable deduction. We hope
G ENESIS G EO -1M will support future work on stronger geometry solvers, improved auxiliary-
construction search, and more reliable diagram-based reasoning. We will release the dataset, training
pipeline, and model checkpoints to the research community.




                                                                       14
References
Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding,
  Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui,
  Shutong Jiang, Zhaohai Li, Mingsheng Li, Mei Li, Kaixin Li, Zicheng Lin, Junyang Lin, Xuejing Liu,
  Jiawei Liu, Chenglong Liu, Yang Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui
  Men, Lingchen Meng, Xuancheng Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu,
  Jianqiang Wan, Peng Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang
  Xu, Jin Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang, Xi
  Zhang, Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou, Yuanzhi Zhu, and Ke Zhu. Qwen3-vl
  technical report. arXiv preprint arXiv:2511.21631, 2025.
Patrick Bak, RNDr Stanislav Krajči, and Mgr Michal Rolínek. Automated generation of planar geometry
  Olympiad problems. PhD thesis, Master Thesis, 2020.
Jiaqi Chen, Jianheng Tang, Jinghui Qin, Xiaodan Liang, Lingbo Liu, Eric Xing, and Liang Lin. GeoQA:
   A geometric question answering benchmark towards multimodal numerical reasoning. In Findings of the
   Association for Computational Linguistics: ACL-IJCNLP, pages 513–523, 2021.
Jiaqi Chen, Tong Li, Jinghui Qin, Pan Lu, Liang Lin, Chongyu Chen, and Xiaodan Liang. UniGeo: Unifying
   geometry logical reasoning via reformulating mathematical expression. In Proceedings of the Conference on
   Empirical Methods in Natural Language Processing, pages 3313–3323, Abu Dhabi, United Arab Emirates,
   2022. Association for Computational Linguistics.
Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin,
  Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun, Jiahui Wang, Siran
  Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu, Yihang Xia, Huajian Xin, Fan
  Yang, Huaiyuan Ying, Hongyi Yuan, Zheng Yuan, Tianyang Zhan, Chi Zhang, Yue Zhang, Ge Zhang, Tianyun
  Zhao, Jianqiu Zhao, Yichi Zhou, and Thomas Hanwen Zhu. Seed-prover: Deep and broad reasoning for
  automated theorem proving, 2025.
Yuri Chervonyi, Trieu H. Trinh, Miroslav Olsak, Xiaomeng Yang, Hoang Nguyen, Marcelo Menegali, Junehyuk
  Jung, Junsu Kim, Vikas Verma, Quoc V. Le, and Thang Luong. Gold-medalist performance in solving
  olympiad geometry with alphageometry2. arXiv preprint arXiv:2502.03544, 2025.
Shang-Ching Chou. Mechanical Geometry Theorem Proving. Springer, 1988.
S.-C. Chou, X.-S. Gao, and J.-Z. Zhang. Automated production of traditional proofs for constructive geometry
   theorems. In Proceedings of Annual IEEE Symposium on Logic in Computer Science, pages 48–56, 1993.
Shang-Ching Chou, Xiao-Shan Gao, and Jing-Zhong Zhang. A deductive database approach to automated
  geometry theorem proving and discovering. Journal of Automated Reasoning, 25(3):219–246, 2000.
Boyan Duan, Xiao Liang, Shuai Lu, Yaoxiang Wang, Yelong Shen, Kai-Wei Chang, Ying Nian Wu, Mao
  Yang, Weizhu Chen, and Yeyun Gong. Gold-medal-level olympiad geometry solving with efficient heuristic
  auxiliary constructions. arXiv preprint arXiv:2512.00097, 2025.
Daocheng Fu, Jianlong Chen, Renqiu Xia, Zijun Chen, Qi Liu, Yuan Feng, Hongbin Zhou, Renrui Zhang, Shiyang
  Feng, Peng Gao, Hongyuan Zha, Junchi Yan, Botian Shi, Yu Qiao, and Bo Zhang. Trustgeogen: Formal-
  verified data engine for trustworthy multi-modal geometric problem solving. arXiv preprint arXiv:2504.15780,
  2025.
Jiahui Gao, Renjie Pi, Jipeng Zhang, Jiacheng Ye, Wanjun Zhong, Yufei Wang, Lanqing HONG, Jianhua Han,
   Hang Xu, Zhenguo Li, and Lingpeng Kong. G-LLaVA: Solving geometric problem with multi-modal large
   language model. In The Thirteenth International Conference on Learning Representations, 2025.
Shasha Guo, Liang Pang, Xi Wang, Yanling Wang, Huawei Shen, and Jing Zhang. Geovlmath: Enhancing
  geometry reasoning in vision-language models via cross-modal reward for auxiliary line creation. arXiv
  preprint arXiv:2510.11020, 2025.
Raj Jaiswal, Avinash Anand, and Rajiv Ratn Shah. Advancing multimodal llms: A focus on geometry problem
  solving reasoning and sequential scoring. In Proceedings of the ACM International Conference on Multimedia
  in Asia, 2024.
Deepak Kapur. Using gröbner bases to reason about geometry problems. Journal of Symbolic Computation, 2
  (4):399–408, 1986.
Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In International Conference on
   Learning Representations, 2019.


                                                     15
Pan Lu, Ran Gong, Shibiao Jiang, Liang Qiu, Siyuan Huang, Xiaodan Liang, and Song-Chun Zhu. Inter-GPS:
  Interpretable geometry problem solving with formal language and symbolic reasoning. In Proceedings of the
  Annual Meeting of the Association for Computational Linguistics and the International Joint Conference on
  Natural Language Processing, pages 6774–6786, 2021.
Pan Lu, Hritik Bansal, Tony Xia, Jiacheng Liu, Chunyuan Li, Hannaneh Hajishirzi, Hao Cheng, Kai-Wei Chang,
  Michel Galley, and Jianfeng Gao. Mathvista: Evaluating mathematical reasoning of foundation models in
  visual contexts. In The Twelfth International Conference on Learning Representations, 2024.
Yicheng Pan, Zhenrong Zhang, Pengfei Hu, Jiefeng Ma, Jun Du, Jianshu Zhang, Quan Liu, Jianqing Gao,
  and Feng Ma. Enhancing the geometric problem-solving ability of multimodal llms via symbolic-neural
  integration. In Proceedings of the ACM International Conference on Multimedia, page 5394–5403, 2025.
Ying Shi, Man Luo, et al. Geothought: A dataset for enhancing mathematical geometry reasoning in vision-
  language models. arXiv preprint arXiv:2510.21881, 2025.

Vladmir Sicca, Tianxiang Xia, Mathïs Fédérico, Philip John Gorinski, Simon Frieder, and Shangling Jui. Newclid:
  A user-friendly replacement for alphageometry with agentic support. arXiv preprint arXiv:2411.11938, 2024.

Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong. Solving olympiad geometry without human
   demonstrations. Nature, 625:476–482, 2024.

Ke Wang, Junting Pan, Weikang Shi, Zimu Lu, Houxing Ren, Aojun Zhou, Mingjie Zhan, and Hongsheng
  Li. Measuring multimodal mathematical reasoning with the math-vision dataset. In Proceedings of the
  International Conference on Neural Information Processing Systems, 2024.

Ke Wang, Junting Pan, Linda Wei, Aojun Zhou, Weikang Shi, Zimu Lu, Han Xiao, Yunqiao Yang, Houxing
  Ren, Mingjie Zhan, and Hongsheng Li. MathCoder-VL: Bridging vision and code for enhanced multimodal
  mathematical reasoning. In Findings of the Association for Computational Linguistics: ACL, pages 2505–2534,
  2025.
Weiming Wu, Jin Ye, Zi kang Wang, Zhi Zhou, Yu-Feng Li, and Lan-Zhe Guo. Nesygeo: A neuro-symbolic
  framework for multimodal geometric reasoning data generation. arXiv preprint arXiv:2505.17121, 2025.

Wen-Tsün Wu. On the decision problem and the mechanization of theorem-proving in elementary geometry.
 Scientia Sinica, 21(2):159–172, 1978.

Chi Zhang, Jiajun Song, Siyu Li, Yitao Liang, Yuxi Ma, Wei Wang, Yixin Zhu, and Song-Chun Zhu. Proposing
  and solving olympiad geometry with guided tree search. Nature Machine Intelligence, 2026.




                                                     16
A        Featured GenesisGeo Solutions


During development, we discovered a new solution to IMO 2008 Problem 6, and its correctness was
confirmed by an IMO gold medalist. To the best of our knowledge, this solution is different from
both the official solution and the one produced by AlphaGeometry2. Notably, AlphaGeometry21
requires introducing 13 auxiliary points to complete the proof, whereas our solution only requires
two auxiliary points.



        IMO 2008 P6 (Converted following AlphaGeometry)

        Let XY Z be a triangle. Define point O as the circumcenter of triangle XY Z. Define ⊙O
        as the circle centered at O passing through X. Let W be any point on ⊙O. Define lines
        l1 , l2 , l3 , l4 as the tangent lines at X, Y, Z, W on ⊙O, point A as the intersection of l1 and l3 ,
        point B as the intersection of l3 and l4 , point C as the intersection of l2 and l4 , point D as
        the intersection of l1 and l2 .
        Define point I1 as the incenter of triangle ABC, point I2 as the incenter of triangle ACD,
        point F1 as the foot of I1 on line AC, point F2 as the foot of I2 on line AC. Define ⊙I1 as the
        circle centered at I1 passing through F1 , ⊙I2 as the circle centered at I2 passing through F2 ,
        lines m1 , m2 as the external common tangents of ⊙I1 and ⊙I2 . Define P, Q as the tangency
        points of m1 , m2 with ⊙I1 , S, T as the tangency points of m1 , m2 with ⊙I2 , point K as the
        intersection of lines m1 and m2 . Prove that: OK is equal to OX (i.e. K lies on ⊙O).




                       Figure 7: Illustration of the problem statement for IMO 2008 P6




    1
        https://github.com/google-deepmind/alphageometry2


                                                         17
   Formal Specification

   Problem Description:
   x y z = triangle x y z; o = circle o x y z; w = on_circle w o x; a = on_tline
    a z o z, on_tline a x o x; b = on_tline b z o z, on_tline b w o w; c =
   on_tline c y o y, on_tline c w o w; d = on_tline d x o x, on_tline d y o y;
   i1 = incenter i1 a b c; i2 = incenter i2 a c d; f1 = foot f1 i1 a c; f2 =
   foot f2 i2 a c; q t p s = cc_tangent q t p s i1 f1 i2 f2; k = on_line k q t,
   on_line k p s ? cong o k o x

   Our Auxiliary Constructions:
   n1 = on_line n1 c i1, on_circum n1 o w c; n2 = on_line n2 o b, on_circum n2 o
    w c


The following trace details the complete derivation process generated by the automated proving
engine. It proceeds from the initial premises and auxiliary constructions to the final conclusion
through 97 logical steps.

  Full Proof Trace: IMO 2008 P6

  * From theorem premises:
  Points: A, B, C, D, F1 , F2 , I1 , I2 , K, O, P, Q, S, T, W, X, Y, Z
   (Premise)⇒ OW = OX [0]
   (Premise)⇒ OX = OY [1]
   (Premise)⇒ OY = OZ [2]
   (Premise)⇒ BW ⊥ OW [3]
   (Premise)⇒ CW ⊥ OW [4]
   (Premise)⇒ CY ⊥ OY [5]
   (Premise)⇒ DY ⊥ OY [6]
   (Premise)⇒ ∠(AC,CI1 ) = ∠(CI1 ,BC) [7]
   (Premise)⇒ ∠(AC,AI2 ) = ∠(AI2 ,AD) [8]
   (Premise)⇒ ∠(AD,DI2 ) = ∠(DI2 ,CD) [9]
   (Premise)⇒ K, P, S are collinear [10]
   (Premise)⇒ PI1 = F1 I1 [11]
   (Premise)⇒ QI1 = F1 I1 [12]
   (Premise)⇒ SI2 = F2 I2 [13]
   (Premise)⇒ TI2 = F2 I2 [14]
   (Premise)⇒ K, Q, T are collinear [15]
   (Premise)⇒ PS ⊥ PI1 [16]
   (Premise)⇒ QT ⊥ QI1 [17]
   (Premise)⇒ PS ⊥ SI2 [18]
   (Premise)⇒ QT ⊥ TI2 [19]
   (Premise)⇒ AZ ⊥ OZ [20]
   (Premise)⇒ BZ ⊥ OZ [21]
   (Premise)⇒ A, C, F1 are collinear [22]
   (Premise)⇒ ∠(AB,AI1 ) = ∠(AI1 ,AC) [23]
   (Premise)⇒ AC ⊥ F1 I1 [24]
   (Premise)⇒ AX ⊥ OX [25]
   (Premise)⇒ DX ⊥ OX [26]
   (Premise)⇒ A, C, F2 are collinear [27]
   (Premise)⇒ AC ⊥ F2 I2 [28]
   (Numerical Check)⇒ A, C, D are not collinear [29]
   (Numerical Check)⇒ O, W, Y are not collinear [30]
   (Numerical Check)⇒ P, Q, I1 are not collinear [31]
   (Numerical Check)⇒ S, T, I2 are not collinear [32]
   (Numerical Check)⇒ O, W, Z are not collinear [33]
   (Numerical Check)⇒ A, B, C are not collinear [34]
   (Numerical Check)⇒ AOI1 are sameclock to CI2 O [35]
   (Numerical Check)⇒ DOX are sameclock to DYO [36]
   (Numerical Check)⇒ A, X, Z are not collinear [37]
   (Numerical Check)⇒ S, I1 , I2 are not collinear [38]
   (Numerical Check)⇒ KPQ are sameclock to KST [39]
   (Numerical Check)⇒ PQI1 are sameclock to STI2 [40]
   (Numerical Check)⇒ K, W, Z are not collinear [41]

  * Auxiliary Constructions:
  Points: N1 , N2
   (Premise)⇒ C, I1 , N1 are collinear [42]
   (Premise)⇒ COWN1 are cyclic [43]
   (Premise)⇒ B, O, N2 are collinear [44]
   (Premise)⇒ COWN2 are cyclic [45]
   (Numerical Check)⇒ C, Y, N1 are not collinear [46]




                                                      18
 (Numerical Check)⇒ AF1 I1 are sameclock to CI1 N2 [47]
 (Numerical Check)⇒ COI1 are sameclock to I1 N1 N2 [48]
 (Numerical Check)⇒ C, O, N1 are not collinear [49]
 (Numerical Check)⇒ CON1 are sameclock to CF2 I2 [50]
 (Numerical Check)⇒ K, N1 , I2 are not collinear [51]
 (Numerical Check)⇒ I1 is to the same side of C→N1 as I1 is to K→I2 [52]
 (Numerical Check)⇒ C, Y, N2 are not collinear [53]
 (Numerical Check)⇒ ACI1 are sameclock to WN1 N2 [54]
 (Numerical Check)⇒ CI1 I2 are sameclock to KN1 I1 [55]

Reverse proof steps:
097. KO = OX (by AR with Dist)
⌊-- 096. KO = OZ [152] (by circumcenter property r49)
|   |-- 001. O is circumcenter of WYZ [57] (by r72)
|   |   ⌊-- 000. OW = OZ [56] (by AR with Dist)
|   |       ⌊-- [Premise] OW=OX, OX=OY, OY=OZ
|   ⌊-- 095. KWYZ are cyclic [151] (by concyclic check r04)
|       ⌊-- 094. ∠(KW,KY) = ∠(WZ,YZ) [150] (by AR with Slope)
|           |-- 093. KN1 = WN1 [149] (by AR with Dist)
|           |   ⌊-- 092. KN1 :WN1 = WN2 :ZN2 [148] (by AR with Distlog "The Grand Ratio")
|           |       |-- 023. KP = KQ [79] (by AR with Slope)
|           |       |-- 024. KS = KT [80] (by AR with Slope)
|           |       |-- 081. WN2 = ZN2 [137] (by AR with Slope)
|           |       |   ⌊-- 080. Y, Z, N2 collinear [136] (by AR with Slope)
|           |       |       ⌊-- 079. ∠(CO,CY) = ∠(ON2 ,YN2 ) [135] (by cyclic angles)
|           |       |            ⌊-- 078. COYN2 cyclic [134] (by concyclic check)
|           |       |-- 036. AI1 :CI1 = F1 I1 :I1 N2 [92] (by Similar Triangles r53)
|           |       |   ⌊-- 035. △AF1 I1 ∼  = △CN2 I1 [91] (by Congruence r35)
|           |       |       |-- 034. ∠(AF1 ,F1 I1 ) = ∠(I1 N2 ,CN2 ) [90] (by AR with Slope)
|           |       |       |-- 031. ∠(AF1 ,AI1 ) = ∠(CI1 ,CN2 ) [87] (by AR with Slope)
|           |       |       ⌊-- 047. [Check] Orientation check
|           |       |-- 085. AI1 :CI1 = WN1 :N1 N2 [141] (by Similar Triangles r53)
|           |       |   ⌊-- 084. △ACI1 ∼   = △WN2 N1 [140] (by Congruence r35)
|           |       |       |-- 083. ∠(AI1 ,CI1 ) = ∠(N1 N2 ,WN1 ) [139] (by AR with Slope)
|           |       |       |-- 082. ∠(AC,CI1 ) = ∠(N1 N2 ,WN2 ) [138] (by AR with Slope)
|           |       |       ⌊-- 054. [Check] Orientation check
|           |       |-- 086. CI1 :CN1 = I1 I2 :KI2 [142] (by AR with Dist)
|           |       |   ⌊-- 074. CN1 :KI2 = I1 N1 :KI1 [130] (by AR with Distlog "The Bridge Ratio")
|           |       |       |-- 065. KP:KS = KI1 :KI2 [121] (by Thales r07)
|           |       |       |   ⌊-- 064. PI1 ∥ SI2 [120] (by AR with Slope)
|           |       |       |        ⌊-- [16, 18] PS⊥PI1 , PS⊥SI2
|           |       |       |-- 052. AI1 :CI2 = OI1 :CO [108] (by Similar Triangles r52)
|           |       |       |   ⌊-- 051. △AOI1 ∼   = △I2 OC [107] (by Congruence r34)
|           |       |       |        |-- 050. ∠(AO,OI1 ) = ∠(OI2 ,CO) [106] (by AR with Slope)
|           |       |       |        |-- 048. ∠(AO,AI1 ) = ∠(OI2 ,CI2 ) [104] (by AR with Slope)
|           |       |       |        ⌊-- 035. [Check] Orientation check
|           |       |       |-- 059. CI1 :OI1 = I1 N2 :I1 N1 [115] (by Similar Triangles r53)
|           |       |       |   ⌊-- 058. △COI1 ∼   = △N2 N1 I1 [114] (by Congruence r35)
|           |       |       |        |-- 057. ∠(CO,OI1 ) = ∠(I1 N1 ,N1 N2 ) [113] (by AR with Slope)
|           |       |       |        |-- 056. ∠(CO,CI1 ) = ∠(I1 N2 ,N1 N2 ) [112] (by AR with Slope)
|           |       |       |        ⌊-- 048. [Check] Orientation check
|           |       |       |-- 063. CO:CN1 = CI2 :F2 I2 [119] (by Similar Triangles r52)
|           |       |       |   ⌊-- 062. △CON1 ∼   = △I2 CF2 [118] (by Congruence r34)
|           |       |       |        |-- 061. ∠(CO,CI2 ) = ∠(ON1 ,CF2 ) [117] (by AR with Slope)
|           |       |       |        |-- 060. ∠(CN1 ,ON1 ) = ∠(F2 I2 ,CF2 ) [116] (by AR with Slope)
|           |       |       |        ⌊-- 050. [Check] Orientation check
|           |       |       |-- 069. KQ:KT = PQ:ST [125] (by Similar Triangles r52)
|           |       |       |   ⌊-- 068. △KPQ ∼   = △KST [124] (by Congruence r62)
|           |       |       |        |-- 067. KP:KQ = KS:KT [123] (by AR with Dist)
|           |       |       |        |    ⌊-- [79, 80] KP=KQ, KS=KT
|           |       |       |        |-- 066. ∠(KP,KQ) = ∠(KS,KT) [122] (by AR with Slope)
|           |       |       |        ⌊-- 039. [Check] Orientation check
|           |       |       ⌊-- 073. PQ:PI1 = ST:TI2 [129] (by Similar Triangles r53)
|           |       |            ⌊-- 072. △PQI1 ∼   = △TSI2 [128] (by Congruence r63)
|           |       |                 |-- 071. PI1 :QI1 = TI2 :SI2 [127] (by AR with Dist)
|           |       |                 |   ⌊-- [11, 12, 13, 14] Radii equalities
|           |       |                 |-- 070. ∠(PI1 ,QI1 ) = ∠(SI2 ,TI2 ) [126] (by AR with Slope)
|           |       |                 ⌊-- 040. [Check] Orientation check
|           |       |-- 090. CI2 :KN1 = I1 I2 :KI1 [146] (by Similar Triangles r52)
|           |       |   ⌊-- 089. △CI1 I2 ∼  = △N1 I1 K [145] (by Congruence r62)
|           |       |       |-- 088. CI1 :I1 N1 = I1 I2 :KI1 [144] (by AR with Dist)
|           |       |       |   ⌊-- 074. CN1 :KI2 = I1 N1 :KI1 [130] (See branch 074 above)
|           |       |       |-- 087. ∠(CI1 ,I1 N1 ) = ∠(I1 I2 ,KI1 ) [143] (by AR with Slope)
|           |       |       ⌊-- 055. [Check] Orientation check
|           |       |-- 091. CO:CI1 = N1 N2 :I1 N2 [147] (by Similar Triangles r53)
|           |       |   ⌊-- 058. △COI1 ∼   = △N2 N1 I1 [114] (See branch 059 above)
|           |       |-- 119. [Using Step 063 result]
|           |       |-- 121. [Using Step 065 result]
|           |       |-- 125. [Using Step 069 result]




                                                   19
|           |        ⌊-- 129. [Using Step 073 result]
|           |-- 076. K, Y, N1 collinear [132] (by AR with Slope)
|           |   |-- 075. CI2 ∥ KN1 [131] (by Parallel check r27)
|           |   |   |-- 074. CN1 :KI2 = I1 N1 :KI1 [130] (See branch 074 above)
|           |   |   |-- 052. [Check] Orientation check
|           |   |   ⌊-- 051. K, N1 , I2 not collinear [Check]
|           |   |-- 042. C, I1 , N1 collinear [Premise]
|           |   |-- 058. B, C, W collinear [Step 002]
|           |   |-- 059. C, D, Y collinear [Step 003]
|           |   ⌊-- [Premises] BW⊥OW, CW⊥OW, CY⊥OY
|           |-- 012. COYN1 cyclic [68] (by concyclic check r04)
|           |   ⌊-- 011. ∠(CY,CN1 ) = ∠(OY,ON1 ) [67] (by AR with Slope)
|           |        |-- 007. ∠(CO,CW) = ∠(ON1 ,WN1 ) [63] (by cyclic angles)
|           |        |   ⌊-- 006. COWN1 cyclic [Premise 43]
|           |        ⌊-- 006. ∠(CO,CN1 ) = ∠(OW,WN1 ) [62] (by cyclic angles)
|           |            ⌊-- 006. COWN1 cyclic [Premise 43]
|           |-- 010. ∠(CO,CW) = ∠(OY,WY) [66] (by cyclic angles)
|           |   ⌊-- 009. COWY cyclic [65] (by concyclic check r04)
|           |        ⌊-- 008. ∠(CW,CY) = ∠(OW,OY) [64] (by AR with Slope)
|           |            ⌊-- [Premises] CW⊥OW, CY⊥OY
|           ⌊-- 005. ∠(AC,CI2 ) = ∠(CI2 ,CD) [61] (by AR with Slope)
|                ⌊-- [Premises] Angle bisectors AI2 , DI2
⌊-- 004. OW = OY [60] (by AR with Dist)
    ⌊-- [Premise] OW=OX, OX=OY




                                                    20
Human-Readable Mathematical Proof of IMO 2008 Problem 6 (GenesisGeo Reconstruction)

Let ⊙O be the circumcircle of △XY Z with center O and radius R. Let W ∈ ⊙O be an arbitrary
point. Define:
       • l1 , l2 , l3 , l4 : tangent lines to ⊙O at X, Y, Z, W respectively
       • A = l1 ∩ l3 , B = l3 ∩ l4 , C = l2 ∩ l4 , D = l1 ∩ l2
       • I1 : incenter of △ABC, I2 : incenter of △ACD
       • F1 : foot of perpendicular from I1 to AC, F2 : foot of perpendicular from I2 to AC
       • ⊙I1 : incircle of △ABC (center I1 , radius r1 = I1 F1 ), ⊙I2 : incircle of △ACD (center
         I2 , radius r2 = I2 F2 )
       • m1 , m2 : external common tangents of ⊙I1 and ⊙I2
       • P, Q: tangent points of m1 , m2 with ⊙I1 ; S, T : tangent points of m1 , m2 with ⊙I2
       • K = m1 ∩ m 2
       • N1 : second intersection of ray CI1 with ⊙O
       • N2 : second intersection of ray BI1 with ⊙O

Lemma 1. (The Parallelism Bridge) CI2 ∥ KN1
Proof. We establish the ratio equality:
                                        CN1   I 1 N1
                                            =                                                (⋆)
                                        KI2   KI1
Since K is the intersection of external common tangents m1 , m2 of ⊙I1 and ⊙I2 , there exists
a homothety hK centered at K mapping ⊙I1 to ⊙I2 . The tangent points satisfy I1 P ⊥ m1 ,
I2 S ⊥ m1 , I1 Q ⊥ m2 , I2 T ⊥ m2 .
Since I1 P ∥ I2 S (both perpendicular to m1 ):
                                                     KI1   KP   r1
                        △KP I1 ∼ △KSI2 =⇒                =    =                              (1)
                                                     KI2   KS   r2
From tangent properties: P I1 = QI1 = r1 , SI2 = T I2 = r2 , and KP = KQ, KS = KT
(tangent segments from external point). The homothety implies:
                                    K, I1 , I2 are collinear                                 (2)
Define N2 as the second intersection of line BI1 with ⊙O. By the angle bisector property of I1
in △ABC:
                                 ∠(AB, BI1 ) = ∠(BI1 , BC)                                  (3)
Since A, B ∈ l3 (tangent at Z) and B, C ∈ l4 (tangent at W ), combined with the inscribed angle
theorem on ⊙O, we establish:
                    B, I1 , N2 are collinear   and   O, I1 , N2 are collinear                (4)
From perpendicularity conditions:
                   CW ⊥ OW, CY ⊥ OY =⇒ C, O, W, Y are cyclic                                 (5)
                    Similarly, C, O, Y, N1 are cyclic                                        (6)
We establish four key ratios through triangle congruences:
(i) From △AF1 I1 ∼ △CN2 I1 (proven via angle chasing using (4) and tangent properties):
                                    AI1   F1 I 1     r1
                                        =        =                                           (7)
                                    CI1   I 1 N2   I 1 N2
(ii) From △AOI1 ∼ △I2 OC (proven via angle matching using perpendicularity and (4)):
                                          AI1   OI1
                                              =                                              (8)
                                          CI2   CO



                                               21
(iii) From △COI1 ∼ △N2 N1 I1 (using cyclic quadrilateral CON1 N2 from (6)):
                                          CI1   I 1 N2
                                              =                                                (9)
                                          OI1   I 1 N1
(iv) From △CON1 ∼ △I2 CF2 (using angle bisector properties and (6)):
                                          CO    CI2
                                              =                                              (10)
                                          CN1   r2
Multiplying (7) through (10):
                    AI1 CI1 CO AI1     r1    I1 N2 CI2 OI1
                       ·   ·   ·    =      ·      ·   ·                                      (11)
                    CI1 OI1 CN1 CI2   I1 N2 I1 N1 r2 CO
Simplifying the left side:
                                AI12 · CO       r1 · CI2 · OI1
                                              =                                              (12)
                              OI1 · CN1 · CI2   I1 N1 · r2 · CO
Cross-multiplying and using (1):
                                    AI12 · CO2    r1 · CI2
                                               =                                             (13)
                                    CN1 · CI2    I 1 N1 · r 2
From (8): AI1 · CO = CI2 · OI1 . Substituting and simplifying:
                                CN1      KI2
                                       =        (using (2) and (1))                          (14)
                                I 1 N1   KI1
Since C, I1 , N1 are collinear and K, I1 , I2 are collinear, by Thales’ theorem:

                                           CI2 ∥ KN1                                         (15)
                                                                                               □
Lemma 2. (The Isosceles Property) KN1 = W N1
Proof. From the cyclic quadrilaterals C, O, Y, N2 (proven similarly to (6)):
                                 ∠(CO, CY ) = ∠(ON2 , Y N2 )                                 (16)
Combined with the tangent properties and the fact that D, O, I2 are collinear (from angle bisector
of △ACD), the inscribed angle theorem implies:
                                      Y, Z, N2 are collinear                                 (17)
Since Y, Z, N2 are collinear, the chord Y Z passes through N2 . From the cyclic quadrilateral
B, O, W, Z (proven via perpendicularity):
                                  ∠(BW, W Z) = ∠(BO, OZ)                                     (18)
The configuration exhibits symmetry with respect to the perpendicular bisector of chord W Z.
Since N2 lies on line Y Z and B, O, N2 are collinear, this symmetry yields:
                                          W N2 = ZN2                                         (19)
From the congruence chain:
                    △ACI1 ∼ = △W N2 N1 (via angle matching)                                  (20)
                            ∼
                    △CI1 I2 = △N1 I1 K (via Lemma 1 and collinearity)                        (21)
We derive:
                               AI1   W N1     CI2       I1 I2
                                   =       ,         =                                  (22)
                               CI1   N1 N2    KN1       KI1
Combining these with ratios from Lemma 1 and using the distlog (distance-logarithm) algebra:
                                         KN1    W N2
                                              =                                              (23)
                                         W N1   ZN2



                                                22
Substituting (19) into (23):
                                 KN1
                                      = 1 =⇒ KN1 = W N1                                 (24)
                                 W N1
                                                                                             □
Lemma 3. (Angle Convergence) ∠(KW, KY ) = ∠(ZW, ZY ), hence K ∈ ⊙O
Proof. From Lemma 1: CI2 ∥ KN1 . Since C, I1 , N1 are collinear and C, O, Y, N1 are cyclic:
                   ∠(CI2 , CY ) = ∠(KN1 , N1 Y )      (corresponding angles)            (25)
From the parallelism:
                        ∠(CI2 , CY ) = ∠(KN1 , KY )     (alternate angles)              (26)
Therefore: ∠(KN1 , N1 Y ) = ∠(KN1 , KY ), which implies:
                                     K, Y, N1 are collinear                             (27)
From Lemma 2: KN1 = W N1 . Therefore, △KW N1 is isosceles:
                               ∠(W K, KN1 ) = ∠(KW, W N1 ) = α                          (28)
Since K, Y, N1 are collinear by (27):
                               ∠(KW, KY ) = ∠(KW, KN1 ) = α                             (29)
Since W, N1 , Y, Z ∈ ⊙O and Y, N1 are collinear with K, the inscribed angle theorem gives:
                ∠(ZW, ZN1 ) = ∠(ZW, ZY )         (since Y, N1 collinear with K)         (30)
From the isosceles property of △KW N1 and the fact that K lies on line Y N1 :
                                  ∠(W N1 , N1 K) = 180◦ − 2α                            (31)
By the inscribed angle theorem (angles subtending the same arc W Y ):
                                  ∠(KW, KY ) = ∠(ZW, ZY )                               (32)
By the converse of the inscribed angle theorem: if ∠(KW, KY ) = ∠(ZW, ZY ), then K lies
on the circle through W, Y, Z.
Since W, Y, Z ∈ ⊙O:
                                          K ∈ ⊙O                                  (33)
                                                                                             □
Main Theorem. OK = OX
Proof. From Lemma 3, K ∈ ⊙O. Since ⊙O is the circumcircle of △XY Z with center O and
radius R:
                          OX = OY = OZ = OW = R                                  (34)
Since K ∈ ⊙O:
                                 OK = R = OX                                     (35)
Therefore:
                                   OK = OX                                       (36)
                                                                                   ■




                                              23
