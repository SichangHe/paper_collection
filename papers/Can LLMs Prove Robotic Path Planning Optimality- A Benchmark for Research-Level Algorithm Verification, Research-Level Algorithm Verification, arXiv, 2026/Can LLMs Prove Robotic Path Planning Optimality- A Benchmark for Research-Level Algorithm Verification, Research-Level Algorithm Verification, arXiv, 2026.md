                                         Can LLMs Prove Robotic Path Planning Optimality? A Benchmark for
                                                      Research-Level Algorithm Verification
                                                              Zhengbang Yang1 , Md. Tasin Tazwar2 , Minghan Wei2 , Zhuangdi Zhu1


                                            Abstract— Robotic path planning problems are often NP-           algorithms with stronger optimality guarantees. One might
                                         hard, and practical solutions typically rely on approximation       expect LLMs to transfer their mathematical competency to
                                         algorithms with provable performance guarantees for general         this domain, particularly given their advanced performance
                                         cases. While designing such algorithms is challenging, formally
                                         proving their approximation optimality is even more demand-         on math reasoning benchmarks such as GMS8K [7] and
                                         ing, which requires domain-specific geometric insights and          MATH [8]. However, the task we investigate is fundamen-
                                         multi-step mathematical reasoning over complex operational          tally distinct, where the planning optimality proofs operate at
                                         constraints. Recent Large Language Models (LLMs) have               a research level, involving complex optimization constraints
                                         demonstrated strong performance on mathematical reasoning           arising from operational requirements, such as cost budgets
                                         benchmarks, yet their ability to assist with research-level opti-
                                         mality proofs in robotic path planning remains under-explored.      and terrain or operational restrictions [9], [10]. They demand
                                         In this work, we introduce the first benchmark for evaluating       task-specific knowledge of domain lemmas and theorems,
                                         LLMs on approximation-ratio proofs of robotic path planning         and reasoning over long problem formulations that jointly
arXiv:2603.19464v3 [cs.RO] 17 Jul 2026




                                         algorithms. The benchmark consists of 34 research-grade proof       describe the algorithm, the environment, and the optimal-
                                         tasks spanning diverse planning problem types and complexity        ity objective. Furthermore, a valid proof typically requires
                                         levels, each requiring structured reasoning over algorithm
                                         descriptions, problem constraints, and theoretical guarantees.      multi-step deduction to connect concrete task descriptions
                                         Our evaluation of state-of-the-art proprietary and open-source      to abstract mathematical conditions. For instance, proving
                                         LLMs reveals that even the strongest models struggle to             the 3/2-approximation guarantee for the metric Traveling
                                         produce fully valid proofs without external domain knowledge.       Salesman Problem (TSP) requires mapping the tour-planning
                                         However, providing LLMs with task-specific in-context lemmas        objective to combinatorial structures (minimum spanning
                                         substantially improves reasoning quality, a factor that is more
                                         effective than generic chain-of-thought prompting or supplying      trees (MST), odd-degree vertex sets, and minimum-weight
                                         the ground-truth approximation ratio as posterior knowledge.        perfect matchings) and then chaining multiple lemmas, e.g.,
                                         We further provide fine-grained error analysis to characterize      MST ≤ OPT, MWPM ≤ OPT/2, and triangle-inequality
                                         common logical failures and hallucinations, and demonstrate         shortcutting to convert an Eulerian walk into a Hamiltonian
                                         how each error type can be mitigated through targeted context       tour without increasing cost. These characteristics place
                                         augmentation.
                                                                                                             our investigation well beyond the scope of standard math
                                                                  I. I NTRODUCTION                           reasoning.
                                                                                                                To systematically study this challenge, we introduce a
                                            Robotic path planning problems are usually NP-hard [1],          benchmark comprising 34 robotic constrained planning prob-
                                         [2], and this field has long relied on approximation algo-          lems from 11 peer-reviewed, published robotic papers. Each
                                         rithms as practical solutions. Even marginal improvements           instance includes the original problem formulation, algorithm
                                         in approximation ratios can yield substantial real-world ben-       description, and formal performance guarantee as presented
                                         efits in deployment time, energy consumption, and mission           in the source work. The tasks are curated from representative
                                         reliability in varying high-stake domains [1], [2]. Therefore,      constrained path-planning formulations motivated by real
                                         the quality of proposed algorithms plays significant role.          robotic deployment settings, including energy-aware naviga-
                                         Yet while proposing a new planning algorithm is relatively          tion, perception-constrained routing, time-critical missions,
                                         tractable, formally proving its approximation optimality is         and multi-robot workload balancing. Each selected paper
                                         far more demanding, often requiring human experts days or           establishes formal approximation guarantees, enabling us to
                                         weeks of careful mathematical and geometric reasoning.              assess whether LLMs can reason about algorithmic perfor-
                                            The recent emergence of large language models (LLMs)             mance bounds rather than merely solving isolated planning
                                         with strong performance in mathematical reasoning [3], [4],         instances. Our evaluation reveals several key findings: (1)
                                         [5], [6] raises a natural question: can LLMs expedite the           Current LLMs differ substantially in performance, yet even
                                         formal verification of approximation optimality for robotic         the strongest models struggle to produce valid optimality
                                         path planning algorithms? Such a capability would lay               proofs without given expert domain knowledge (setting 1,
                                         the groundwork for automated algorithm validation, and              Sec IV-C). (2) Augmenting prompts with task-relevant in-
                                         ultimately for the cost-effective discovery of new planning         context knowledge, specifically, lemmas and prior knowledge
                                                                                                             tailored to the target problem, leads to notable improvements
                                           1 George Mason University. 2 Florida Atlantic University.
                                                                                                             in proof accuracy. (3) Providing the ground-truth approxi-
                                           Email: {zyang30,zzhu24}@gmu.edu, {mtazwar2023,weim}@fau.edu.
                                           This work was supported by NSF Award No. 2452203.                 mation ratio as posterior knowledge also improves reasoning
                                           Source code: https://github.com/Zhengbang-Yang/RoboticsBench      quality, though it contributes less than in-context lemmas. (4)
Generic chain-of-thought (CoT) [11] or deduction-inducing          geometry or mathematical question-solving ability of LLMs
prompting alone does not meaningfully reduce task difficulty,      [22], [3].
though it provides complementary benefit when combined             LLM for inequality proof: Our work draws a close con-
with posterior knowledge. (5) Notably, we find that open-          nection to those that investigate LLM’s ability to prove
source models such as Qwen 3.5 [12] respond strongly to in-        inequalities. IneqMath [23] evaluated LLMs on Olympiad-
context augmentation, with performance gains that can sur-         level inequality proving with a neutral language formulation
pass those achieved by counterpart LLMs. We further provide        and step-wise judges. Open Proof Corpus [24] provided a
a fine-grained error analysis (Sec IV-D) to characterize where     dataset of human-evaluated LLM-generated Olympiad-level
LLMs typically fail and how each error type can be miti-           proofs. However, the complexity of these existing works falls
gated. Our benchmark also introduces a granular evaluation         short of research-level standards, and they lack a detailed
metric that jointly assesses the correctness of the final proof,   analysis of the errors in model-generated proofs. Our work
the quality of the reasoning chain, and the alignment with         differs from the above efforts along three critical dimensions:
ground-truth proofs from the original research papers. We          domain specificity, task type and complexity, and evaluation
releases an automated pipeline for extracting and formalizing      granularity. It targets research-level proofs of approximation
path planning algorithms from research papers to facilitate        optimality for robotic path-planning algorithms, which re-
future work in this domain.                                        quire simultaneous mastery of domain-specific lemmas, long-
                                                                   context algorithm descriptions with operational constraints,
                    II. R ELATED W ORK                             and multi-step deductive reasoning, all of which are lacking
                                                                   in existing LLM reasoning benchmarks.
LLM assisted path planning: Work along this line explores          LLM as Judge for scientific reasoning: As LLMs have
using LLMs directly as planning agents or algorithm ex-            become more powerful in reasoning, a common evaluation
ecutors. NLGraph benchmark [13] demonstrated that LLMs             strategy is to reuse them as automatic graders, reducing
possess preliminary abilities to trace shortest paths on simple    the cost of assessing open-ended generations while retaining
classic topologies. LLM+P [14] integrated language models          meaningful signal about quality [25], [26], [27]. Building
with classical planners, utilizing the LLM to translate natural    on this line, multiple studies have explored LLM-based
language problem descriptions into formal specifications that      judging for mathematical solutions and proofs, reporting
symbolic solvers can process. LLM-A* [15] integrated               that with appropriately scoped rubrics, LLM graders can be
language models into the A* search procedure to heuristi-          sufficiently consistent for certain proof-style tasks and can
cally navigate planning spaces. Similarly, GraphArena [16]         also support feedback-oriented educational use cases [23],
benchmarked LLMs on their ability to act as algorithmic            [28], [29]. Specifically, for inequality proofs, IneqMath [23]
executors for graph computation tasks, testing their step-by-      validated that LLM judging can echo human judgments
step traversal on complex routing challenges like the Trav-        when the evaluation is decomposed appropriately. In parallel,
eling Salesman Problem. In practical domains, frameworks           OPC [24] shows that top LLM judges achieve near-human
like TravelPlanner [17] and Personal Travel Solver [18]            judging accuracy on proof correctness via a large-scale study,
deployed LLMs as autonomous solvers for real-world routing         reinforcing that LLM-as-judge can be highly consistent with
and planning instances, assessing their ability to satisfy         expert human assessment in proof settings. Built upon this
multifaceted constraints. They evaluate LLMs as solvers of         prior work, we adopt LLM-as-Judge for the first-round
planning instances rather than investigating whether LLMs          evaluation and error analysis, followed by human researcher
can reason about the optimality of proposed algorithms.            verifications.
LLM on scientific or mathematical reasoning: A paral-
lel thread evaluates LLMs on scientific and mathematical                          III. DATASET C OMPOSITION
reasoning more broadly. Datasets such as GMS8K [7],
                                                                   A. Task Definition
MATH [8], PRM800K [19] provided mathematical prob-
lems ranging from elementary to undergraduate-level diffi-            Each task in our benchmark requires establishing the
culty. State-of-the-art LLMs tend to saturate on these math        theoretical performance guarantees of a provided algorithm
benchmarks with (near-) expert performance. More advanced          A for a robotics path planning problem T , namely, proving
benchmarks include ARB [20], OmniMATH [4], Olympiad-               that the cost of the provided algorithm is at most α times
bench [5], Matharena [6]. They target general mathematical         the cost of the optimal solution, where α is referred to as
competitions where problems are mostly self-contained and          the approximation ratio. As illustrated in Figure 1, each task
drawn from established Olympiad corpora. While Frontier-           consists of a problem description T , the given algorithm A
Math [21] remains a formidable challenge for state-of-the-         to sovle T , an optional set of in-context lemmas C, and
art models, it merely evaluates final answers rather than          an optional posterior approximation ratio α, which together
demanding complete proofs or granular reasoning steps.             form the input provided to the LLM under evaluation; the
Furthermore, its closed-source nature limits community-            model is then asked to produce a proof ŷ. We also provide an
driven research, both of which are essential for advancing         optional Chain-of-Thought style reasoning template to assist
the field. Some other work focused on training or inference        the LLM in generating legit proofs. Figure 1 overviews the
time optimization instead of benchmarking to improve the           proof generation process of the LLMs under investigation.
                                                                                Data Extraction and Standardization. To scale and stan-
                                                                                dardize the paper, especially math notations and tables, we
                                                                                designed an automated extraction pipeline that uses GPT-
                                                                                5.2 as an agent to process of the PDF files of papers. Given
                                                                                each paper PDF, the pipeline first converts the contents into a
                                                                                structured LaTeX document; we also developed a conversion
                                                                                pipeline that explicitly emphasizes faithful reproduction of
                                                                                mathematical expressions and tables to maximize the data
                                                                                quality. Based on the resulting LaTeX document, the agent
Fig. 1. LLM proof generation pipeline. The LLM receives a path-planning         then extracts (i) the formal problem definition(s) T , (ii) the
problem T and algorithm A, along with optional in-context lemmas and            algorithm definition A, (iii) the ground-truth approximation
theorems C. It is then prompted (optionally) with a Chain-of-Thought style
instruction) to generate the approximation ratio α̂ and a corresponding proof   ratio α and its corresponding proof, and (iv) the key lemmas
ŷ, both evaluated against ground-truth references. When ground-truth α∗ is     invoked by the ground truth proof C. This structured repre-
also provided as part of the input, the task reduces to generating reasoning    sentation supports downstream evaluation in various settings.
ŷ proving how the given α∗ is derived.

                                                                                Problem and Algorithm Anonymization. Notably, we ob-
  For comparison, Figure 2 compares a mathematical in-                          served that providing the name of a classic algorithm or
equality proof drawn from an existing benchmark [23] and                        problem, such as the k-TSP [32], can illicitly prompt an LLM
proof of robotic path planning optimality. Such inequality                      to produce a fluent proof, likely due to data contamination,
proofs are typically simpler in structure, relying on standard                  where the algorithm name serves as a retrieval cue that
lemmas and algebraic manipulation with few operational                          triggers verbatim reproduction of memorized content rather
constraints. In contrast, path planning optimality proofs are                   than genuine reasoning. To prevent this, we have anonymized
multi-lemma, long-context, and constraint-coupled.                              all problem and algorithm names in our benchmark.
                                                                                Human verification. 4 human annotators (faculty and gradu-
B. Task Distribution                                                            ate students) have manually verified the quality of extracted
   We collected 34 robotic path planning research methods                       data from each research paper, and the evaluation quality
from 11 papers which cover research-level robotic path-                         of the LLM-as-judge, which helped refine the evaluation
planning and routing problems that require jointly reasoning                    instructions prompt iteratively.
about (i) operational constraints (e.g., energy/distance bud-
gets, charging, pickups/deliveries, regret or lateness costs),
(ii) structured environments (e.g., grid/polygon/contour-                                             IV. E VALUATION
connected spaces, tree metrics, general metrics, and 3D
visibility-cone geometry), and (iii) approximation optimality                   A. Experimental Settings
proofs that combine algorithmic decomposition with non-
trivial inequalities and geometric arguments. Concretely, the                   Task Difficulty: We evaluated LLMs under four settings of
collected methods cluster into: (A) energy-constrained cover-                   varying information availability. In Setting-1 (no context),
age path planning (unit grid/polygon/contour-connected en-                      the LLM receives only the task definition and algorithm
vironments with charging constraints), (B) distance/capacity-                   description A. In Setting-2 (context-augmented), the LLM
constrained vehicle routing and its variants (DVRP [30],                        additionally receives context C containing key lemmas ex-
CVRP-on-tree [31], kTSP [2], [32] objectives such as                            tracted from the ground-truth research paper. In Setting-3
min–max and min–sum, and regret-bounded routing), and                           (posterior-augmented), the LLM is provided with the ground-
(C) geometric neighborhood touring such as Cone TSPN [33]                       truth approximation ratio α but no supporting lemmas.
in 3D (visibility cones, intersecting vs disjoint neigh-                        Specifically, setting-3 allows us to investigate whether this
borhoods). These categories emphasize domain specificity                        posterior information alone can guide the model to recon-
(robotic coverage + routing constraints), research-level task                   struct a correct reasoning path in retrospect. In Setting-4
complexity (long-context algorithm descriptions and multi-                      (context and posterior-augmented), the LLM is provided with
lemma proofs), and evaluation granularity (proof-step cor-                      both context C and the ground-truth approximation ratio α.
rectness rather than final answers alone).                                      Models Under Evaluation include Grok 4.1 [34], Gem-
                                                                                ini 3 Pro [35], GPT 5.2 [36], and Qwen3.5 [12] (397B-
C. Data Preparation                                                             A17B), covering a broad slice of today’s state-of-the-art
Paper Data Collection. We collected the raw corpus of                           LLMs across both closed-source commercial systems and
papers through an expert-driven selection process: domain                       strong open-source releases. For all models, we enabled
experts in robotic path planning actively searched for and                      their reasoning mode to reflect best-effort performance on
shortlisted suitable research papers that are representative of                 these proof-intensive questions. Claude 4.6 was also tested,
real-world planning and routing settings, and that contain                      but it frequently timed out on these questions, making its
non-trivial algorithmic designs and approximation-optimality                    results non-informative and therefore excluded from further
proofs appropriate for inclusion in our benchmark.                              analysis.
  Task Example: Path Planning Optimality Proof vs. Math Inequality Proof
  Example-1: Math Inequality Proof Task
    • Problem formulation: Find the maximal constant C such that for all real a, b, c,
                                     p                 p                   p
                                       a2 + (1 − b)2 + b2 + (1 − c)2 + c2 + (1 − a)2 ≥ C.
         Helpful Lemmas: Minkowsky’s Inequality Theorem: ...
     •   Key Proof Steps:
          1) Apply Minkowski (or a norm/triangle inequality) to lower bound a sum of square-roots by a single square-root of
              aggregated terms.
          2) Reduce the expression to a 1D quadratic in x = a + b + c and take the minimum.
          3) Conclude the best constant C and give a tightness witness (equality case).
  Example-2: Path Planning Optimality Proof Task Christofides Algorithm for TSP (as a simplest case):
    • Problem formulation: For any metric TSP instance with optimal tour cost OPT, prove the approximation ratio of the Christofides
      algorithm.
        – TSP problem definition: ...
        – Constraints of the problem: Hamiltonian cycle · · ·
        – Christofides algorithm definition: ...
        – Helpful Lemmas (Optional Information): Lemma 1 (MST bound): ..., Lemma 2 (matching bound): ..., ...
        – Ground truth approximation ratio α (Optional Information)
    • Key Proof Steps:
        1) Algorithm structure: build an MST T ; let O be odd-degree vertices in T ; compute a minimum-weight perfect matching
            M on O; combine T ∪ M to get an Eulerian multigraph; take an Euler tour and shortcut repeated vertices to obtain a
            Hamiltonian cycle.
        2) Lemma 1 (MST bound): cost(T ) ≤ OPT (MST no more expensive than removing one edge from an optimal tour).
        3) Lemma 2 (matching bound): cost(M ) ≤ 12 OPT (odd-degree set has even size; the optimal tour restricted to O can be
            decomposed into two perfect matchings, so the minimum one is at most half).
        4) Lemma 3 (Euler → tour feasibility): T ∪ M is Eulerian; the Euler walk can be shortcut to a Hamiltonian cycle without
            increasing cost only because the instance is metric (triangle inequality).
        5) Combine: cost(A) ≤ cost(T ) + cost(M ) ≤ OPT + 21 OPT = 32 OPT.

                   Fig. 2.   An Example Comparison of a Path Planning Optimality Proof vs. a Generic Math Inequality Proof.



B. Evaluation Metrics                                                    provided context; 6-8 reflects partial alignment with some
   We used the ground-truth proof of each task to guide an               loosely connected segments; and scores below 6 indicate
LLM-as-judge (GPT-5.2) in evaluating the model-generated                 weak alignment or reliance on fabricated steps.
proof ŷ against the ground-truth y along the following three
                                                                         C. Main Results
dimensions, each scored on a scale of 1 to 10:
Final answer measures how accurately the predicted ap-                      State-of-the-art LLMs broadly struggle with algorithmic
proximation ratio matches the ground-truth, accounting for               proof reasoning: without external domain knowledge (Table
exactness of constants, asymptotic order, and parameter                  I, Setting-1), only up to 26.47% of the path planning algo-
dependence. A score of 9-10 indicates the ratio is exact or              rithms in our benchmark are successfully addressed, where
differs only in minor presentation; 6-8 reflects the correct             success is defined as a score of ≥ 7 for both the final answer
asymptotic order with nontrivial mismatches in constants                 and the reasoning steps in Setting-1 and 2, and a reasoning
or parameter dependence; and scores below 6 indicate an                  score ≥ 7 in Setting-3 and 4. Beyond this headline finding,
incorrect approximation ratio.                                           our benchmark also surfaces answers to several intriguing
The reasoning correctness score assesses the logical validity            questions.
of the derivation, which penalizes unjustified steps, incorrect          Can providing external information help LLMs get back
inequalities, and missing feasibility arguments. A score of 9-           on the right track? Yes, we found that both providing in-
10 indicates a fully valid proof with all key steps justified; 6-        context lemma (Setting-2) and an oracle posterior (Setting-
8 reflects a proof whose main strategy is sound but contains             3) help LLMs in terms of general performance, where in-
repairable gaps; and scores below 6 indicate significant or              context lemma (Setting-2) plays a more important role than
fatal logical errors.                                                    providing posterior or CoT. This is supported by results in
The proof relevance score captures how well the generated                Table I, where the best performance in Setting-2 consistently
proof is grounded in the provided problem context. It rewards            surpasses those in Setting-3.
precise use of supplied lemmas and definitions while penal-              Is oracle posterior information useful when in-context
izing reliance on invented or irrelevant reasoning. A score of           lemmas are already provided? Yes. While posterior-only
9-10 indicates the proof directly and correctly references the           guidance (Setting-3) yields limited benefit in recovering
                                                               TABLE I
M AIN RESULTS UNDER FOUR EVALUATION SETTINGS : SCORES (1–10) FOR Final Answer, Reasoning, AND Relevance, EVALUATED with AND without
    A CRAFTED GENERIC REASONING TEMPLATE . F INAL - ANSWER SCORES ARE OMITTED ( INDICATED WITH ’-’) FOR S ETTING -3 AND 4, SINCE THE
ORACLE FINAL APPROXIMATION RATIO IS GIVEN IN THESE SETTINGS . I N CASE OF A CONSISTENT TIMEOUT ISSUE IN LLM REASONING , WE ASSIGNED
1 ( THE LOWEST SCORE ) FOR EACH EVALUATION METRIC . S UCCESS R ATE IS THE PERCENTAGE RATIO OF SUCCESS , WHERE SUCCESS IS DEFINED AS A
SCORE OF ≥ 7 FOR BOTH THE FINAL ANSWER AND THE REASONING STEPS IN S ETTING -1 AND 2, AND A REASONING SCORE ≥ 7 IN S ETTING -3 AND 4.


       Model          Final Answer ↑ Final Answer ↑   Reasoning ↑      Reasoning ↑      Relevance ↑   Relevance ↑   Success Rate ↑
                         (w/o CoT)      (w/ CoT)       (w/o CoT)        (w/ CoT)         (w/o CoT)     (w/ CoT)     (%) (w/o CoT)
                                                           Setting-1 (no-context)
       GPT 5.2             4.15           3.35           4.62              4.47               4.88       4.12           26.47
       Gemini 3 Pro        3.71           3.59           3.47              3.53               3.94       4.18           11.76
       Grok 4.1            2.88           2.76           3.24              3.00               3.59       3.41           14.71
       Qwen3.5             3.53           3.03           3.32              3.53               4.09       3.85           8.82
                                                          Setting-2 (with context)
       GPT 5.2             4.44           4.32           4.94              4.82               4.91       4.88           32.35
       Gemini 3 Pro        5.62           5.50           5.06              5.03               6.32       6.44           35.29
       Grok 4.1            4.62           4.56           4.26              4.09               5.56       5.41           29.41
       Qwen3.5             5.97           6.06           5.32              5.35               6.68       6.35           44.12
                                                        Setting-3 (with oracle ratio)
       GPT 5.2              –              –             4.04              4.22               4.46       4.26           32.35
       Gemini 3 Pro         –              –             4.68              4.87               5.82       6.34           32.35
       Grok 4.1             –              –             3.59              4.10               4.63       5.35           17.65
       Qwen3.5              –              –             4.38              4.50               5.97       5.65           23.53
                                                  Setting-4 (with context and oracle ratio)
       GPT 5.2              –              –             5.26              5.01               5.59       5.50           50.00
       Gemini 3 Pro         –              –             5.46              6.32               7.21       7.56           38.24
       Grok 4.1             –              –             4.66              5.24               5.85       6.44           41.18
       Qwen3.5              –              –             5.15              5.25               7.12       7.01           32.35



a correct proof strategy, Setting-4 shows that α becomes                 Grok 4.1 ), as shown in Table I. Notably, however, the open-
helpful once the model is anchored by domain lemmas                      source model Qwen 3.5 shows great potential when task-
C. Concretely, when supplied with both C and α, models                   tailored in-context information is provided (Setting-2), which
achieve higher reasoning-correctness and relevance scores                outperforms other LLM counterparts, suggesting the strong
than with C alone (Setting-2), indicating that the oracle                latent capacity of this open-sourced model that benefits from
ratio can serve as an effective consistency check that nudges            domain-specific guidance.
the model toward the intended proof target and discourages
drifting to alternative ratios. This suggests that posterior in-         D. Error Analysis.
formation is not a substitute for domain knowledge; instead,
it acts as a complementary signal that refines and stabilizes               To understand where reasoning breaks down, we devel-
the derivation after the proof skeleton has been grounded by             oped an error analysis pipeline to attribute the reasoning
the provided lemmas.                                                     errors in an unsuccessful proof. We define two classes of
                                                                         errors in the model’s reasoning process: 1) logical errors,
Does generic CoT prompting help LLM achieve better                       which reflect breakdowns within the reasoning chain itself,
performance? Comparing results with and without CoT in                   including a) overgeneralization, b) oversimplification, c)
Table I, generic deduction-inducing prompting alone does not             missing edge cases, d) skipped computations, e) uncited non-
meaningfully reduce task difficulty across settings. However,            standard results, f) incorrect inequality directions, and g)
when combined with posterior knowledge (Settings-3 and 4),               unsupported inferences, and 2) hallucination errors, which
CoT provides a complementary benefit on the Reasoning                    may be manifested as a) unsupported inserted assumptions,
score across most LLMs. This indicates that while CoT                    b) reasoning about an irrelevant or narrower problem, and
is insufficient as a standalone strategy, it can reinforce               c) omission or contradiction of given constraints. Note that
structured reasoning when the model is already anchored by               multiple errors may exist in one LLM-generated proof.
correct posterior information.                                           What types of mistakes do LLMs typically make? With-
Which LLMs are most capable on these tasks? In the                       out external knowledge (Setting-1), logical errors are the
strictest setting, i.e. no in-context lemmas, no posterior,              dominant failure mode across all models, with unsupported
proprietary models lead, with GPT 5.2 outperforming open-                inference being the most frequent error type (e.g. an inference
source alternatives ( GPT 5.2 > Gemini 3 Pro > Qwen 3.5 >                error of the form “since A, therefore B”, where A is not
                                                       Fig. 3.        Distribution of the reasoning errors occurring in Setting 1.

                                                                    TABLE II
                            T OTAL COUNTS OF ERROR TYPES MADE BY THE EVALUATED LLM S UNDER EACH EVALUATION SETTING .

                         Overgene- Oversim-      Missing    Skipping   Non-Standard Result Incorrect Inequality Unsupported Logic Error                        Omission/    Hallucination
    Evaluation Setting                                                                                                                  Insertion Irrelevance                             Other
                         ralization plification Edge Cases Computation  Without Citation        Direction        Inference    Total↓                          Contradiction    Total↓

   Setting 1 (w/o CoT)       9         42         24             26               12               17             160          272         61         56          106           216           1
   Setting 1 (w/ CoT)       13         21         25             32               13                5             145          239         65         71          111           244           1
   Setting 2 (w/o CoT)      14         31         19             25                8                7             136          230         45         31           82           154           0
   Setting 2 (w/ CoT)        6         43         27             26                7               14             142          255         44         36           84           162           1
   Setting 3 (w/o CoT)      12         22         32             43               22                7             166          285         57         19           69           137           4
   Setting 3 (w/ CoT)       16         32         37             31               21               15             172          293         53         13           71           129           1
   Setting 4 (w/o CoT)      11         24         29             28                8                9             129          222         45          9           57           103           2
   Setting 4 (w/ CoT)       15         16         17             22                7               10             123          198         33          5           46            81           1


                                                             TABLE III
   AVERAGE F IRST E RROR P LACE (%): THE AVERAGE POSITION AT WHICH THE FIRST ERROR APPEARS IN THE GENERATED PROOF. VALUES ARE
                   REPORTED AS PERCENTAGES OF THE PROOF LENGTH ( HIGHER MEANS THE FIRST ERROR OCCURS LATER ).


                                                   GPT 5.2             GPT 5.2         Gemini 3 Pro      Gemini 3 Pro           Grok 4.1        Grok 4.1         Qwen3.5          Qwen3.5
             Evaluation Setting
                                                  (w/o CoT)            (w/ CoT)         (w/o CoT)          (w/ CoT)            (w/o CoT)        (w/ CoT)        (w/o CoT)         (w/ CoT)
    Setting 1 (no-context)                             17.93             22.73            25.07                25.35              24.41            24.77            19.53             29.66
    Setting 2 (with context)                           24.55             21.98            22.50                36.64              31.22            32.14            36.02             32.38
    Setting 3 (with oracle ratio)                      20.98             15.33            33.17                35.97              27.76            25.05            34.87             31.47
    Setting 4 (context + oracle ratio)                 27.53             18.83            35.89                30.88              35.89            26.32            43.34             32.25



sufficient to establish B). Figure 3 overviews the distribution                                     supporting lemmas (Setting-4) further improves proof quality
of proof errors across LLM models for Setting-1.                                                    over Setting-3, suggesting that the ground-truth ratio is most
                                                                                                    useful when it is grounded by relevant in-domain lemmas
Can these mistakes be mitigated, and how? As shown                                                  rather than presented in isolation.
in Table II, Setting-1, introducing generic CoT instructions
partially reduces logical errors, yet simultaneously increases                                      Does proof quality correlate with where errors first appear?
hallucination rates. This indicates that a domain-agnostic                                          Yes. For proofs of overall lower reasoning quality, errors
reasoning template is insufficient to anchor proofs without in-                                     tend to emerge earlier in the reasoning chain. As shown
domain knowledge. In contrast, task-specific in-context lem-                                        in Table III, we tracked the relative position of the first
mas curated by human researchers (Setting-2) yield dramatic                                         error in each LLM-generated proof on a normalized scale
improvements, which reduced both logical errors and hallu-                                          from 0% to 100%. We reported the average reasoning score
cinations (Table I). Furthermore, posterior information alone                                       and the first error position of each setting across models
without in-context lemma (Setting-3) provides additional                                            and discovered that the overall score of LLM proof is
but secondary benefit. Taken together, these results suggest                                        positively correlated with the first-error position (Table IV).
that solving rigorous robotic planning algorithmic proof                                            This suggests that early errors tend to propagate downstream
tasks fundamentally requires in-domain expertise, where the                                         and compound into incorrect deductions. Notably, providing
relevance and quality of in-context knowledge matters far                                           in-context lemmas not only reduces the frequency of logical
more than prompting strategy alone. Consistent with our                                             errors, but also pushes the point of first error later into the
evaluation section, combining posterior information with                                            proof. This implies that domain-relevant knowledge helps
                           TABLE IV                                                  the model has been anchored by domain lemmas, acting as a
       AVERAGE R EASONING SCORE VS . F IRST E RROR P OSITION .                       consistency target that stabilizes the proof trajectory. Finally,
 Evaluation Setting                        Average                Average            we presented fine-grained error analysis that separates logical
                                      Reasoning Score ↑   First Error Position (%)   failures from hallucinations and quantifies where the first
 Setting 1 (no-context)                     3.65                   23.68             error occurs, offering actionable signals for diagnosing and
 Setting 2 (with context)                   4.86                   29.68
 Setting 3 (with oracle ratio)              4.30                   28.08             improving algorithmic-proof generation.
 Setting 4 (context + oracle ratio)         5.29                   31.37
                                                                                        There are several promising directions for future work. (1)
                                                                                     Geometric visualization with VLMs. Many planning proofs
LLMs sustain coherent reasoning for longer before going
                                                                                     hinge on geometric or spatial invariants (e.g., visibility cones,
astray.
                                                                                     tours in metric spaces, feasibility under charging/pickup con-
E. Structural Failure and Success Patterns in LLM Gener-                             straints). Incorporating multimodal geometric visualization,
ated Proofs                                                                          such as automatically rendering key structures (graphs, tours,
   Beyond the quantitative counts in Table II, qualitative                           regions, cones) and allowing a vision-language model to
inspection reveals recurring structural reasoning patterns that                      verify or refine intermediate claims, may reduce early logical
explain both failure and success:                                                    slips and improve the grounding of feasibility arguments. (2)
   Failures often stem from misinterpreting the problem                              A reusable library of in-context knowledge. Our findings
definition (i.e., Oversimplification in Table II), including                         indicate that proof success depends heavily on the availability
conflating related routing variants (e.g., implicitly reducing a                     and quality of domain lemmas. A natural next step is to build
constrained formulation to classical TSP), misusing notation,                        a standardized, compositional library of contexts (lemmas,
or assuming structural properties such as completeness or                            proof schemas, and constraint-check templates) that can
metric conditions that are not guaranteed. Such misunder-                            be retrieved and adapted across families of computational-
standings typically occur early and propagate, leading to                            geometry and robot-planning problems, enabling stronger
invalid bounds. A second failure mode concerns improper                              generalization beyond paper-specific cues. (3) Proof-aware
application of provided lemmas (i.e., unsupported inference                          training and evaluation. The error taxonomy and first-error-
or overgeneralization in Table II): models frequently invoke                         position metrics invite targeted interventions: training or
relevant propositions without verifying their preconditions.                         decoding-time methods that explicitly penalize unsupported
For instance, a proposition [37] may be treated as implying                          inferences, missing feasibility checks, and constraint con-
that each consecutive segment contributes at least B/2 new                           tradictions, and that reward citing provided lemmas at the
distinctPcells, leading to an unjustified aggregation such as                        right step. On the evaluation side, a promising direction is
N =                                                                                  to integrate an LLM-as-judge as an online verifier during
          j Cj . This reflects surface-level lemma matching
without condition-aware validation.                                                  proof generation: the model periodically externalizes key
   In contrast, LLMs usually succeed when the proof admits                           intermediate subclaims, which are then checked for validity
a clear modular decomposition aligned with the algorith-                             and support. When a subclaim is flagged, the generator
mic structure. For example, in contour-connectivity–based                            can revise the local step before continuing, reducing er-
coverage planning, the correct reasoning decomposes the                              ror propagation and enabling more reliable long-horizon
environment into contour-connected components and then                               deductive chains. This also opens the door to subclaim-
applies established properties to each component. When                               level supervision signals and evaluation, aligning training
intermediate guarantees are explicitly stated and assumption-                        objectives with the specific failure modes observed in our
consistent, LLMs can correctly compose them into a valid                             benchmark.
global approximation bound. These results suggest that per-
formance depends less on algebraic manipulation and more                                                         R EFERENCES
on the clarity of structural abstraction and the compatibility                        [1] P. Duan, Z. Yu, K. Gao, L. Meng, Y. Han, and F. Ye,
between (provided in-context) lemmas.                                                     “Solving the multi-objective path planning problem for mobile robot
                                                                                          using an improved nsga-ii algorithm,” Swarm and Evolutionary
             V. C ONCLUSION & F UTURE W ORK                                               Computation, vol. 87, p. 101576, 2024. [Online]. Available: https:
                                                                                          //www.sciencedirect.com/science/article/pii/S2210650224001147
   We introduced the first benchmark that evaluates the
                                                                                      [2] C. Bazgan, R. Hassin, and J. Monnot, “Approximation algorithms
state-of-the-art LLMs’ ability to produce research-level                                  for some vehicle routing problems,” Discrete Applied Mathematics,
approximation-ratio proofs for robotic path-planning algo-                                vol. 146, no. 1, pp. 27–42, 2005. [Online]. Available: https:
rithms. Across 34 proof tasks curated from peer-reviewed                                  //www.sciencedirect.com/science/article/pii/S0166218X04002860
                                                                                      [3] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang,
robotics papers, our experiments show that even state-of-the-                             M. Zhang, Y. K. Li, Y. Wu, and D. Guo, “Deepseekmath: Pushing
art models struggle to generate fully valid proofs when given                             the limits of mathematical reasoning in open language models,” 2024.
only problem and algorithm descriptions. In contrast, pro-                                [Online]. Available: https://arxiv.org/abs/2402.03300
                                                                                      [4] B. Gao, F. Song, Z. Yang, Z. Cai, Y. Miao, Q. Dong, L. Li,
viding task-specific in-context lemmas consistently improves                              C. Ma, L. Chen, R. Xu, Z. Tang, B. Wang, D. Zan, S. Quan,
both reasoning correctness and proof relevance, outperform-                               G. Zhang, L. Sha, Y. Zhang, X. Ren, T. Liu, and B. Chang,
ing generic chain-of-thought prompting and posterior access                               “Omni-MATH: A universal olympiad level mathematic benchmark
                                                                                          for large language models,” in The Thirteenth International
to the ground-truth ratio. Moreover, our results suggest that                             Conference on Learning Representations, 2025. [Online]. Available:
providing an oracle posterior information is most useful after                            https://openreview.net/forum?id=yaqPf0KAlN
 [5] C. He, R. Luo, Y. Bai, S. Hu, Z. Thai, J. Shen, J. Hu, X. Han,           [19] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee,
     Y. Huang, Y. Zhang, J. Liu, L. Qi, Z. Liu, and M. Sun,                        J. Leike, J. Schulman, I. Sutskever, and K. Cobbe, “Let’s verify
     “OlympiadBench: A challenging benchmark for promoting AGI                     step by step,” in The twelfth international conference on learning
     with olympiad-level bilingual multimodal scientific problems,” in             representations, 2023.
     Proceedings of the 62nd Annual Meeting of the Association for            [20] T. Sawada, D. Paleka, A. Havrilla, P. Tadepalli, P. Vidas, A. P.
     Computational Linguistics (Volume 1: Long Papers), L.-W. Ku,                  Kranias, J. J. Nay, K. Gupta, and A. Komatsuzaki, “ARB: Advanced
     A. Martins, and V. Srikumar, Eds. Bangkok, Thailand: Association              reasoning benchmark for large language models,” 2024. [Online].
     for Computational Linguistics, Aug. 2024, pp. 3828–3850. [Online].            Available: https://openreview.net/forum?id=gsZAtAdzkY
     Available: https://aclanthology.org/2024.acl-long.211/                   [21] E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning,
 [6] M. Balunovic, J. Dekoninck, I. Petrov, N. Jovanović, and M. Vechev,          C. F. Olsson, J.-S. Denain, A. Ho, E. de Oliveira Santos,
     “Matharena: Evaluating LLMs on uncontaminated math competitions,”             O. Järviniemi, M. Barnett, R. Sandler, M. Vrzala, J. Sevilla, Q. Ren,
     in The Thirty-ninth Annual Conference on Neural Information                   E. Pratt, L. Levine, G. Barkley, N. Stewart, B. Grechuk, T. Grechuk,
     Processing Systems Datasets and Benchmarks Track, 2025. [Online].             S. V. Enugandla, and M. Wildon, “Frontiermath: A benchmark for
     Available: https://openreview.net/forum?id=y0zL9IZxZ7                         evaluating advanced mathematical reasoning in ai,” 2025. [Online].
 [7] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser,               Available: https://arxiv.org/abs/2411.04872
     M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and              [22] Y. Chervonyi, T. H. Trinh, M. Olšák, X. Yang, H. Nguyen,
     J. Schulman, “Training verifiers to solve math word problems,” 2021.          M. Menegali, J. Jung, J. Kim, V. Verma, Q. V. Le, and T. Luong,
     [Online]. Available: https://arxiv.org/abs/2110.14168                         “Gold-medalist performance in solving olympiad geometry with
 [8] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang,            alphageometry2,” 2025. [Online]. Available: https://arxiv.org/abs/
     D. Song, and J. Steinhardt, “Measuring mathematical problem                   2502.03544
     solving with the MATH dataset,” in Thirty-fifth Conference on Neural     [23] J. Sheng, L. Lyu, J. Jin, T. Xia, A. Gu, J. Zou, and P. Lu,
     Information Processing Systems Datasets and Benchmarks Track                  “Solving inequality proofs with large language models,” in The
     (Round 2), 2021. [Online]. Available: https://openreview.net/forum?           Thirty-ninth Annual Conference on Neural Information Processing
     id=7Bywt2mQsCe                                                                Systems Datasets and Benchmarks Track, 2025. [Online]. Available:
 [9] M. Wei and V. Isler, “A log-approximation for coverage path                   https://openreview.net/forum?id=ZaKGh4wP87
     planning with the energy constraint,” Proceedings of the International   [24] J. Dekoninck, I. Petrov, K. Minchev, M. Marinov, M. Drencheva,
     Conference on Automated Planning and Scheduling, vol. 28,                     L. Konova, M. M. Shumanov, K. Tsvetkov, N. Drenchev, L. D.
     no. 1, pp. 532–539, Jun. 2018. [Online]. Available: https:                    Todorov, K. Nikolova, N. Georgiev, V. Kalinkova, M. Ismoldayev,
     //ojs.aaai.org/index.php/ICAPS/article/view/13929                             M. Balunovic, and M. Vechev, “The open proof corpus: A large-scale
[10] N. Katoh and T. Yano, “An approximation algorithm for the                     study of LLM-generated mathematical proofs,” in The Fourteenth
     pickup and delivery vehicle routing problem on trees,” Discrete               International Conference on Learning Representations, 2026.
     Applied Mathematics, vol. 154, no. 16, pp. 2335–2349, 2006, discrete          [Online]. Available: https://openreview.net/forum?id=a2XmC7rHIU
     Algorithms and Optimization, in Honor of Professor Toshihide Ibaraki     [25] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang,
     at His Retirement from Kyoto University. [Online]. Available: https:          Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica,
     //www.sciencedirect.com/science/article/pii/S0166218X06001892                 “Judging llm-as-a-judge with mt-bench and chatbot arena,” in Pro-
[11] J. Wei, X. Wang, D. Schuurmans, M. Bosma, brian ichter,                       ceedings of the 37th International Conference on Neural Information
     F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, “Chain of thought                   Processing Systems, ser. NIPS ’23. Red Hook, NY, USA: Curran
     prompting elicits reasoning in large language models,” in Advances            Associates Inc., 2023.
     in Neural Information Processing Systems, A. H. Oh, A. Agarwal,          [26] J. Gu, X. Jiang, Z. Shi, H. Tan, X. Zhai, C. Xu, W. Li, Y. Shen, S. Ma,
     D. Belgrave, and K. Cho, Eds., 2022. [Online]. Available:                     H. Liu et al., “A survey on llm-as-a-judge,” The Innovation, 2024.
     https://openreview.net/forum?id= VjQlMeSB J                              [27] A. Chevalier, J. Geng, A. Wettig, H. Chen, S. Mizera, T. Annala, M. J.
[12] Qwen Team, “Qwen3.5: Towards native multimodal agents,” February              Aragon, A. R. Fanlo, S. Frieder, S. Machado et al., “Language models
     2026. [Online]. Available: https://qwen.ai/blog?id=qwen3.5                    as science tutors,” arXiv preprint arXiv:2402.11111, 2024.
[13] H. Wang, S. Feng, T. He, Z. Tan, X. Han, and Y. Tsvetkov, “Can           [28] C. Zhao, M. Silva, and S. Poulsen, “Autograding mathematical induc-
     language models solve graph problems in natural language?” in Thirty-         tion proofs with natural language processing,” International Journal
     seventh Conference on Neural Information Processing Systems, 2023.            of Artificial Intelligence in Education, pp. 1–31, 2025.
     [Online]. Available: https://openreview.net/forum?id=UDqHhbqYJV          [29] ——, “Language models are few-shot graders,” in International Con-
                                                                                   ference on Artificial Intelligence in Education. Springer, 2025, pp.
[14] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas,
                                                                                   3–16.
     and P. Stone, “Llm+p: Empowering large language models with
                                                                              [30] V. Nagarajan and R. Ravi, “Approximation algorithms for distance
     optimal planning proficiency,” 2023. [Online]. Available: https:
                                                                                   constrained vehicle routing problems,” Networks, vol. 59, no. 2, pp.
     //arxiv.org/abs/2304.11477
                                                                                   209–214, 2012. [Online]. Available: https://onlinelibrary.wiley.com/
[15] S. Meng, Y. Wang, C.-F. Yang, N. Peng, and K.-W. Chang,
                                                                                   doi/abs/10.1002/net.20435
     “LLM-a*: Large language model enhanced incremental heuristic
                                                                              [31] T. Asano, N. Katoh, and K. Kawashima, “A new approximation
     search on path planning,” in Findings of the Association for
                                                                                   algorithm for the capacitated vehicle routing problem on a
     Computational Linguistics: EMNLP 2024, Y. Al-Onaizan, M. Bansal,
                                                                                   tree,” Journal of Combinatorial Optimization, vol. 5, no. 2, p.
     and Y.-N. Chen, Eds. Miami, Florida, USA: Association for
                                                                                   213–231, Jun. 2001. [Online]. Available: http://dx.doi.org/10.1023/A:
     Computational Linguistics, Nov. 2024, pp. 1087–1102. [Online].
                                                                                   1011461300596
     Available: https://aclanthology.org/2024.findings-emnlp.60/
                                                                              [32] G. N. Frederickson, M. S. Hecht, and C. E. Kim, “Approximation
[16] J. Tang, Q. Zhang, Y. Li, N. Chen, and J. Li, “Grapharena:                    algorithms for some routing problems,” in 17th Annual Symposium on
     Evaluating and exploring large language models on graph                       Foundations of Computer Science (sfcs 1976), 1976, pp. 216–227.
     computation,” in The Thirteenth International Conference on              [33] P. A. Plonski and V. Isler, “Approximation algorithms for tours of
     Learning Representations, 2025. [Online]. Available: https:                   height-varying view cones,” The International Journal of Robotics
     //openreview.net/forum?id=Y1r9yCMzeA                                          Research, vol. 38, no. 2-3, pp. 224–235, 2019. [Online]. Available:
[17] J. Xie, K. Zhang, J. Chen, T. Zhu, R. Lou, Y. Tian, Y. Xiao, and              https://doi.org/10.1177/0278364918784353
     Y. Su, “Travelplanner: a benchmark for real-world planning with          [34] xAI, “Grok 4.1 model card,” November 2025. [Online]. Available:
     language agents,” in Proceedings of the 41st International Conference         https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf
     on Machine Learning, ser. ICML’24. JMLR.org, 2024.                       [35] Google DeepMind, “Gemini 3 pro model card,” November 2025.
[18] Z. Shao, J. Wu, W. Chen, and X. Wang, “Personal travel solver:                [Online]. Available: https://storage.googleapis.com/deepmind-media/
     A preference-driven LLM-solver system for travel planning,” in                Model-Cards/Gemini-3-Pro-Model-Card.pdf
     Proceedings of the 63rd Annual Meeting of the Association for            [36] OpenAI, “Introducing gpt-5.2,” December 2025. [Online]. Available:
     Computational Linguistics (Volume 1: Long Papers), W. Che,                    https://openai.com/index/introducing-gpt-5-2
     J. Nabende, E. Shutova, and M. T. Pilehvar, Eds. Vienna, Austria:        [37] M. Wei and V. Isler, “Coverage path planning under the energy
     Association for Computational Linguistics, Jul. 2025, pp. 27 622–             constraint,” in 2018 IEEE international conference on robotics and
     27 642. [Online]. Available: https://aclanthology.org/2025.acl-long.          automation (ICRA). IEEE, 2018, pp. 368–373.
     1339/
