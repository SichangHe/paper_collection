                                               MATP-BENCH: Can MLLM Be a Good
                                        Automated Theorem Prover for Multimodal Problems?


                                                Zhitao He♠ Zongwei Lyu♠ Dazhong Chen♣ Dadi Guo♠ Yi R. (May) Fung♠
                                                            ♠
                                                              Hong Kong University of Science and Technology
                                                              ♣
                                                                Chinese University of Hong Kong (Shenzhen)
                                                                    {zhebu, yrfung}@cse.ust.hk
arXiv:2506.06034v1 [cs.CL] 6 Jun 2025




                                                                                     Abstract

                                                 Numerous theorems, such as those in geometry, are often presented in multimodal
                                                 forms (e.g., diagrams). Humans benefit from visual reasoning in such settings,
                                                 using diagrams to gain intuition and guide the proof process. Modern Multimodal
                                                 Large Language Models (MLLMs) have demonstrated remarkable capabilities in
                                                 solving a wide range of mathematical problems. However, the potential of MLLMs
                                                 as Automated Theorem Provers (ATPs), specifically in the multimodal domain,
                                                 remains underexplored. In this paper, we introduce the Multimodal Automated
                                                 Theorem Proving benchmark (MATP-BENCH), a new Multimodal, Multi-level,
                                                 and Multi-language benchmark designed to evaluate MLLMs in this role as multi-
                                                 modal automated theorem provers. MATP-BENCH consists of 1056 multimodal
                                                 theorems drawn from high school, university, and competition-level mathematics.
                                                 All these multimodal problems are accompanied by formalizations in Lean 4, Coq
                                                 and Isabelle, thus making the benchmark compatible with a wide range of theorem-
                                                 proving frameworks. MATP-BENCH requires models to integrate sophisticated
                                                 visual understanding with mastery of a broad spectrum of mathematical knowledge
                                                 and rigorous symbolic reasoning to generate formal proofs. We use MATP-BENCH
                                                 to evaluate a variety of advanced multimodal language models. Existing methods
                                                 can only solve a limited number of the MATP-BENCH problems, indicating that
                                                 this benchmark poses an open challenge for research on automated theorem proving.
                                                 The benchmark is publicly available at https://matpbench.github.io.


                                        1   Introduction
                                        In recent years, with the rapid advancement of large language models (LLMs), increasing attention
                                        has been devoted to their applications in automated theorem proving (ATP) [3; 22; 49; 53; 58; 56; 62].
                                        LLMs is trained to generate rigorous formal proofs, which are then verified by systems such as Lean
                                        4 [31], Isabelle [55], and Coq [9] to ensure the logical soundness of the reasoning process.
                                        Although substantial progress has been made in automating the theorem proving, existing studies
                                        are generally limited to text-based inputs, and their potential for handling a wide range of theorems
                                        involving multimodal information has not yet been fully explored. Many mathematical problems
                                        require presentation and solution through multimodal information, such as geometric proofs, where
                                        non-textual elements like diagrams are crucial for problem understanding and reasoning, and mere
                                        textual descriptions are often insufficient. Current mainstream datasets, such as MiniF2F [62] and
                                        ProofNet [3], mainly consist of textual theorems and lack support for multimodal theorem proving and
                                        multi-language proof verification (e.g., in Coq, Isabelle). While LeanEuclid [32] includes multimodal
                                        Euclidean geometry theorems, it primarily focuses on automatic formalization (i.e., transforming
                                        human-written natural language proofs into formal proofs in Lean4) rather than on challenging the

                                        Preprint. Under review.
        Natural language theorem statement                                    Formal theorem statement
                                                          theorem Mathd_algebra_141        (h₂ : 2 * (a + b)=54) :
   Mathd_algebra_141. For real numbers , , if ∙ =
                                                           (a b : ℝ)                       (a^2 + b^2) = 369 :=
   180, and 2 +    = 54. Prove that: 2 + 2 = 369
                                                           (h₁ : (a * b)=180)             sorry                          Lean 4

      Natural language statement with image                          Formal theorem statement in multi-language
                                                          variables (A B C D E F O : ℝ × ℝ)
   USAMO_2008. In the figure, O is the circumcenter       -- (From diagram) All points lie in the same plane (coplanarity)
   of △ABC, ∠DAB = ∠DBC and ∠DAC = ∠DCB. E                axiom all_points_coplanar : AffineIndependent ℝ ![A, B, C, D, E, F, O]
   is the midpoint of AD, and EF is drawn perpendicular   -- (From statement)
   to AD. Prove that ∠AFD = 2∠OFC.                        axiom O_is_circumcenter : IsCircumcenter O A B C
                                                          axiom angle_eq_1 : ∠ D A B = ∠ D B C
                                                          axiom angle_eq_2 : ∠ D A C = ∠ D C B
                                                          axiom E_is_midpoint : E = midpoint ℝ A D
                                                          axiom EF_perp_AD : ⟂ (E − F) (A − D)
                                                          -- (From diagram) F on extended line BC
                                                          axiom F_on_BC : Collinear ℝ ({F, B, C} : Set (ℝ × ℝ)) ∧ (¬Between ℝ F B C)
                                                          -- (From diagram) points are distinct and non-collinear
                                                          axiom angle_AFD: A ≠ F ∧ D ≠ F ∧ ¬Collinear ℝ ({A, F, D} : Set (ℝ × ℝ))
                                                          -- (From diagram) points are distinct and non-collinear
   Human proof with
                                                          axiom angle_OFC: O ≠ F ∧ C ≠ F ∧ ¬Collinear ℝ ({O, F, C} : Set (ℝ × ℝ))
   auxiliary lines
                                                          …
                                                          theorem USAMO_2008:
                                                            ∠ A F D = 2 * ∠ O F C := sorry                                  Lean 4
                                                                                                                          Isabelle
                                                                                                                              Coq


Figure 1: We illustrate the differences between traditional ATP and MATP through examples from miniF2F
(above) and MATPBENCH (below). Multimodal theorems consist of an image paired with a natural language
theorem statement, which complement each other to convey complete theorem information. Furthermore,
additional auxiliary constructions are often essential for their proof (as shown in the bottom left subfigure). In
traditional ATP, theorem formalization relies solely on textual statements (we use purple to indicate premises
derived from the original statement), whereas MATP requires the model to extract critical premises not explicitly
expressed in the text by analyzing accompanying diagrams (see From diagram on the right). We provide
formalized versions of all multimodal theorems in Lean4, Coq, and Isabelle.

model’s ability to autonomously generate formal proofs. AlphaGeometry [42], on the other hand, can
solve complex Olympiad geometry problems but is not multimodal and does not support verification
in formal proof assistant systems like Lean 4.
Humans often rely on diagrams and visual structures to support mathematical reasoning. With the
rapid progress of multimodal large language models (MLLMs), they have shown great potential in
handling a wide range of mathematical problems [28; 51; 44; 43; 54], even those at Olympiad com-
petition levels [37; 48; 41]. However, the exploration of MLLMs as automated theorem provers for
multimodal problems remains underexamined. Given their proficiency in multimodal comprehension,
investigating their application in automated theorem proving could enable the handling of intricate
proofs that rely on visual information, thereby pushing the boundaries of formal verification.
To this end, we present Multimodal Automated Theorem Proving benchmark (MATP-BENCH), a
multimodal, multi-level, and multi-language benchmark for multimodal automated theorem proving
(MATP). Our benchmark consists of 1056 multimodal theorems drawn from high school, university,
and competition-level mathematics. Each theorem is accompanied by formal theorems in Lean 4 [31],
Isabelle [55], and Coq [9], making the benchmark compatible with a wide range of theorem-proving
frameworks. As shown in Figure 1, each data sample in MATP-BENCH consists of an image, a
natural language theorem statement, and formal theorem statements in three different languages.
Compared to traditional ATP, MATP requires the integration of reasoning across both language and
visual modalities. This is particularly crucial in geometry-related mathematical problems, which
often rely on mathematical structures conveyed through images, such as topological relations, that are
typically difficult to express precisely in natural language. For humans, the reasoning process in such
tasks involves not only drawing intuitive insights from visual representations but also constructing
auxiliary diagrams and identifying implicit structural relations.
We use MATP-BENCH to evaluate a variety of multimodal language models. Our findings indicate
that even current state-of-the-art models can only solve a limited number of problems, particularly


                                                                 2
when generating proofs in the Lean 4 language, where they perform poorly even for problems of only
high school difficulty. Detailed analysis further reveals that: (1) All evaluated models commonly
exhibit issues with incomplete understanding of problem information and the generation of invalid
formal proof steps, indicating deficiencies in their visual-symbolic joint reasoning capabilities; (2)
While models demonstrate some ability in converting natural language questions and geometric
figures into formal statements, they still face significant challenges in subsequent complex logical
reasoning and the construction of correct formal proofs; (3) Models can introduce steps or concepts
involving auxiliary constructions (e.g., auxiliary lines) in proofs, but they fail to effectively utilize
these constructions to substantively advance the proof process.
In summary, our key contributions are as follows:
(1) We introduce the Multimodal Automated Theorem Proving benchmark (MATP-BENCH), which
contains 1056 multimodal theorems drawn from high school, university, and competition-level
mathematics. All these multimodal problems are accompanied by formalizations in Lean 4, Coq and
Isabelle, thus making the benchmark compatible with a wide range of theorem-proving frameworks.
(2) We conduct extensive experiments on MATP-BENCH with six advanced multimodal language
models of varying sizes. The experimental results show that even current state-of-the-art models can
only solve a limited number of problems, particularly when generating proofs in the Lean 4 language,
where they perform poorly even for problems of only high school difficulty.
(3) Our detailed analysis indicates that the primary bottleneck in current MATP task lies in symbolic
reasoning and the construction of correct formal proofs. Although models have demonstrated an
initial ability to introduce auxiliary constructions (e.g., auxiliary lines), they fail to effectively utilize
these constructions to substantively advance the proof process. These findings offer valuable insights
for future research. We release our datasets and code publicly at https://matpbench.github.io.


2    Related Work

Automated Theorem Proving. Automated theorem proving (ATP) has been a long-standing chal-
lenge in symbolic reasoning [40; 5; 62; 24], with substantial progress made in developing automated
theorem provers [35; 36; 20; 47; 4; 18; 50]. In recent years, multiple benchmarks [19; 11; 59; 22]
have been proposed for formal mathematical proof. MINIF2F [62] features a diverse collection of
488 problems, each formalized in mainstream languages such as Lean 3 and Isabelle. ProofNet [3]
comprises 371 parallel formal and natural language theorem statements with proofs, designed to
evaluate autoformalization and theorem proving. PutnamBench [49] is a multi-language benchmark
for theorem provers, featuring 1,692 formalizations of 640 Putnam Competition problems. All
problems are manually formalized in Lean 4 and Isabelle, with many in Coq. FIMO [24] contains
149 IMO Shortlisted Problems formalized in Lean, designed to advance automated theorem proving
at the Olympiad level. LeanDojo [58] is a large-scale theorem-proving dataset sourced from mathlib,
featuring a evaluation split that requires generalization to unseen premises. MATP-BENCH pushes
the boundaries of formal verification by uniquely exploring richer multimodal automated theorem
proving with diverse multi-language formalization proofs, unlike existing benchmarks that focus
exclusively on purely text-based theorem proving in single formal languages.
Multimodal Math Benchmarks. Various benchmarks have been created to assess the mathematical
reasoning capabilities of LLMs [1; 10; 30; 13; 15; 16; 23], with a growing number of specialized
evaluations for MLLMs [27; 29; 28; 51]. GeoQA+ [6], UniGeo [7], GEOS [42], and Geometry3K
[27] provide standardized benchmarks focused on plane geometry problem-solving. MMMU [60]
offers a multi-disciplinary benchmark, incorporating a small subset of mathematical problems in
multiple-choice format. MATHVERSE [61] is a visual math benchmark with 2,612 core problems,
generating 15K test samples across plane geometry, solid geometry, and functions. MATHVISTA
[28] includes 6,141 examples to assess mathematical and visual reasoning across diverse tasks.
MATH-Vision [51] consists of 3,040 carefully selected problems with visual contexts, drawn from 19
real-world math competitions and spanning 12 grade levels. CMM-Math [26] is a Chinese multimodal
math dataset with over 28,000 high-quality samples across 12 grades, covering diverse problem types
and providing detailed solutions. MV-MATH [52] is a multimodal benchmark featuring 2,009 multi-
image questions (up to 8 images per question), categorized into three question types and 11 K-12
math subjects at three difficulty levels. Although significant progress has been made in multimodal
mathematical benchmarking, the exploration of automated theorem proving in multimodal settings


                                                      3
Table 1: Comparison of existing related benchmarks. MATP-BENCH is a Multimodal, Multi-level,
and Multi-language benchmark designed to evaluate MLLMs as automated theorem provers.
                                                   Theorem     Theorem for-   Multi-   Multi-
    Benchmark                  Size   Verifiable                                                Lean   Isabelle   Coq
                                                   Proving      malization    modal    level
    miniF2F [62]               488       ✓           ✓                                  ✓        ✓       ✓
    ProofNet [3]               371       ✓           ✓                                           ✓
    Fimo [24]                  149       ✓           ✓                                           ✓
    Geometry3K-test [27]       601       ✓                                     ✓
    LeanEuclid [32]            173       ✓                         ✓           ✓        ✓        ✓
    PutnamBench [49]           640       ✓           ✓                                           ✓       ✓        ✓
    AlphaGeometry-test [48]     30       ✓           ✓                         ✓
    ProverBench [39]           325       ✓           ✓                                           ✓
    GeoTrust-test [14]         240       ✓                                     ✓        ✓
    MATP-Bench                1056       ✓           ✓             ✓           ✓        ✓        ✓       ✓        ✓



remains limited. To address this gap, we propose MATP-BENCH, a benchmark that evaluates the
ability of MLLMs to integrate visual perception, mathematical reasoning, and symbolic manipulation
to construct rigorous formal proofs. The detailed comparison between related benchmarks and
MATPBENCH is shown in Table 1.

3      Problem Formulation
Automated Theorem Proving (ATP). In the ATP task [62; 3; 49; 24], the system takes a formalized
theorem statement T as input, as shown in the upper part of Figure 1. The goal is to generate a
formal proof P such that:
                              ProverAT P (T ) → P,           where Check(T, P ) = True.
Here, Check denotes the built-in proof verifier of the formal system (such as Lean, Coq, or Isabelle),
which ensures that the generated proof P is a valid derivation of theorem T .

Multimodal Automated Theorem Proving (MATP). In the MATP task, the input to the MATP
system is a pair (I, S), where:

          • I is a multimodal input (e.g., geometric figure);
          • S is a natural language statement of the theorem (not formalized).

As shown in the bottom part of Figure 1, the natural language statement S and the information from
the multimodal input I are complementary, together forming a complete theorem. Hence, the model
must first generate the complete formal theorem T . Then, generates a valid formal proof P . The
entire MATP task can be summarized as:
                       ProverM AT P (I, S) → (T, P ),             where Check(T, P ) = True.

Preventing Modality Leakage. To avoid modality leakage, where the model could ignore visual
inputs, we provide only natural language S and image I, without the formalized theorem T . This
encourages the model to interpret and reason over multimodal inputs, as humans do when proving
multimodal theorems. Furthermore, we incorporate a formal theorem verification task in the
experimental setup to ensure that the formal theorems automatically generated by the multimodal
model are consistent with the problem statement, rather than fabricating simple theorems arbitrarily.

4      MATP-BENCH
MATP-BENCH is a new Multimodal, Multi-level, and Multi-language benchmark designed to
evaluate MLLMs as automated theorem provers. MATP-BENCH consists of 1056 multimodal
theorems drawn from high school, university, and competition-level mathematics. Each theorem is
accompanied by formalization in Lean 4, Isabelle, and Coq, making the benchmark compatible with
a wide range of theorem-proving frameworks.


                                                              4
Multimodal Context and Multi-language Theorem. Compared to previous automated theorem
proving datasets, which typically contain only plain-text theorems, MATP-BENCH introduces
concrete multimodal contexts to jointly evaluate models on visual understanding, mathematical
reasoning, and symbolic manipulation. As shown in the lower part of Figure 1, each theorem consists
of an image and a corresponding natural language description, which complement each other to
form a complete statement. MATP-BENCH provides formalizations of these multimodal theorems
in Lean 4, Isabelle, and Coq. To the best of our knowledge, MATP-BENCH is the first multimodal
automated theorem proving benchmark covering all three of these languages. MATP-BENCH
presents the following challenges: (1) Visual Understanding: The model must accurately extract
key information from theorem-related images, akin to human perception, to construct formal theorem
statements; (2) Mathematical Reasoning: It requires rigorous mathematical reasoning to derive
complete proofs based on the provided natural language descriptions and images; (3) Neural-Symbol
Proof Generation: The model must be proficient in these formal languages and capable of strictly
translating the mathematical reasoning process into verifiable formal proof.
Hierarchy and Diversity. To com-
prehensively evaluate the poten-
tial of multimodal large language Table 2: Statistics summary of MATP-BENCH. Counts and
models (MLLMs) as automated percentages are provided for each category.
theorem provers, MATP-BENCH
                                               Category                         Count Percentage
meticulously features both clear
hierarchy and rich diversity. Ex-              High School                        472      44.7%
isting widely used benchmarks Level College                                       468      44.3%
such as ProofNet [3] mainly focus              Competition                        116      11.0%
on basic mathematical problems                 Plane Geometry                     937      88.7%
from early undergraduate courses, Type 3D Geometry                                 73       6.9%
FIMO [24] is limited to high                   Analytic Geometry                   46       4.4%
school mathematics, while Put-                 Segment Relationships              355      33.6%
namBench [49] targets advanced                 Angle Relationships                282      26.7%
mathematical reasoning at the un-              Area Relationships                 222      21.0%
dergraduate level. In contrast,                Circles and Tangents                86       8.1%
as shown in Table 2, The prob- Topic Parallel and Perpendicular Lines              38       3.6%
lems in MATP-BENCH span three                  Similarity and Proportionality      25       2.4%
distinct educational stages—high               Cyclic Quads & Common Points        20       1.9%
school, university, and competi-               Other                               28       2.7%
tions—systematically covering a
wide range of difficulty levels from elementary to advanced. Specifically, the high school and univer-
sity problems are collected from publicly available multimodal math problem datasets [28; 51; 52; 27],
while the competition problems are sourced from public Mathematical Olympiad examinations. Fur-
thermore, we manually annotate the formal statements of each problem in three formal languages.
This design ensures a thorough examination of models’ reasoning capabilities across different levels
of complexity and mathematics problems. Moreover, the multimodal theorems in MATP-BENCH
are primarily centered around the domains of geometry, such as plane geometry, 3D geometry, and
analytic geometry. These theorems not only require models to demonstrate a solid grasp of funda-
mental geometric knowledge but also emphasize cross-modal understanding, complex reasoning,
spatial modeling, and multi-step logical deduction, aiming to systematically evaluate models’ overall
performance and depth of reasoning in structured mathematical tasks.
Task Formulation. As we mentioned in Section 3, we aim to achieve end-to-end multimodal
automated theorem proving (Task 1), where the input is a natural language theorem and an image,
and the output is a formal theorem and its proof, i.e. ProverMATP (I, S) → (T, P ). Furthermore,
to prevent the model from generating formal theorems that do not align with original problems,
we separately set up multimodal theorem formalization (Task 2) for verification, which aligns with
LeanEuclid [32]. Thus, we divide the task into two progressively challenging sub-tasks:
• Task 1: Multimodal Automated Theorem Proving: This task aims to achieve end-to-end multi-
  modal automated theorem proving similar to human provers, by directly generating a formalized
  theorem T and its proof P from multimodal informal input, i.e. ProverTask1 (I, S) → (T, P ).
  For example, the input of models are a natural language statement (USAMO 2008) and an image
  (geometric diagram), as shown in Figure 1. The required output is a formal theorem statement and



                                                  5
  a formalized valid proof. This presents a significant challenge as the model must first accurately
  formalize the theorem from multimodal input, and then subsequently construct a valid proof.
• Task 2: Multimodal Theorem Formalization: The prover receives the multimodal question, and
  is required to formalize it into a precise theorem T , formally denoted as ProverTask1 (I, S) → T .
  For example, the model takes a natural language statement (USAMO 2008) and its corresponding
  image as input. Unlike task 1, the required output for task 2 is only the formal theorem statement
  (as shown on the right side of Figure 1), without the proof process. This task evaluates the model’s
  ability to correctly understand and formalize information from both textual and visual modalities.
Formalization Effort and Challenges. Our formalization team consists of two doctoral students
and several undergraduate students with backgrounds in advanced mathematics, computer science,
and prior experience with formal proof assistants. The problems cover various question formats that
we manually formalized on a case-by-case basis. Specifically: (1) Multiple-choice questions: we
formalize these by using the correct answer and incorporating key information extracted from the
accompanying image, reformulating the problem as a concrete theorem; (2) Fill-in-the-blank ques-
tions: the correct answer is directly filled into the problem statement, and the theorem is formalized
by integrating relevant information present in the image; (3) Open-ended solution questions: we
transform interrogative formulations into declarative statements based on the provided answer and
combine them with visual cues from the image to construct a complete formal theorem. On average,
fully formalizing a high school problem, a university problem, and a competition problem takes
approximately 25, 30, and 15 minutes respectively (in one language). Among these, the descriptions
of high school and university problems are relatively concise, with rich information contained in
the images requiring preprocessing, while competition problems are more detailed and thus easier
to formalize. Each formalization is reviewed by at least one other team member. In contrast to
prior formalization tasks based solely on textual theorems, a central challenge in our setting lies
in the incompleteness of the original natural language descriptions. Many essential assumptions
are conveyed exclusively through diagrams. As a result, the formalization process requires manual
identification and extraction of visual information, such as geometric structures, to reconstruct a
complete and rigorous formal statement.


5     Experiments

5.1   Experimental settings

Methods: we conduct extensive experiments on a wide variety of advanced multimodal large
language models with different sizes. Specifically, the reasoning models [21; 38; 8] include
OpenAI-o1 (o1 for short) [34], Claude-3.7-Sonnet-Thinking (Claude-3.7 for short) [2], and
Gemini-2.0-Flash-Thinking (Gemini-2.0 for short) [12]; while the non-reasoning models in-
clude GPT-4.1 (GPT-4.1 for short) [33], Qwen2.5-VL-Instruct-70B (Qwen2.5-VL for short)
[46], and Llama3.2-Vision-Instruct-11B (Llama3.2-V for short) [25].
Metrics: For Task 1, which requires the model to generate both a correct formal theorem and its
proof, we follow prior studies [62; 49; 24] and adopt pass@n (n=10) as the evaluation metric. This
metric evaluates whether the prover can successfully complete a valid proof within n attempts in
the formal proof environment. For Task 2, which requires the model to formalize the multimodal
theorem, we use GPT-4o as the judge to assess whether the formal theorem generated by the model
is consistent with the our annotated ground truth. We also adopt pass@n as the evaluation metric.
Details of the prompts for different tasks and evaluation can be found in Appendix F.

5.2   Main results

Lean 4. End-to-end complete multimodal theorem formalization and proof generation (Task 1) is
an extremely challenging task. The overall average performance across the models significantly
declines with increasing theorem difficulty, dropping from 6.96% at the high school level to 3.12% at
the university level and 2.08% at the competition level, highlighting the models’ shortcomings in
handling complex geometric reasoning and generating rigorous formal proofs. Even for the currently
strongest model, o1, its overall success rate (pass@10) is only 5.68%. In contrast, Task 2 only
required models to generate Lean 4 formal theorems based on multimodal input, and its overall
success rate reached 46.81%. The significantly higher success rate of Task 2 indicates that the models’


                                                  6
Table 3: Experimental results of Multimodal Automated Theorem Proving (Task 1), which requires
model to generate both formalized theorem and proof. We adopt pass@10 as the evaluation metric.
We further present the experimental results of pass@n (n=1, n=5) in Table 5 and 6.

                                                   Method
 Task 1                                                                                         Avg.
               OpenAI-o1     Claude-3.7     Gemini-2.0 GPT-4.1       Qwen2.5-VL   Llama3.2-V
                                        Lean 4 (pass@10)
 High school       7.63         7.20           8.47          9.32       2.12         3.58       6.39
 University        4.70         3.85           2.14          2.99       1.50         1.92       2.85
 Competition       1.72         1.72           0.86          3.45       0.00         0.00       1.29
 Overall           5.68         5.11           4.82          5.87       1.61         2.46       4.26
                                          Coq (pass@10)
 High school      28.37         22.47         14.76          28.27      7.59         6.96      18.07
 University       11.75         12.39          4.27          6.62       5.34         4.91      7.55
 Competition       5.45         4.31           1.72           9.48      0.86         0.17      3.67
 Overall          19.43         16.92          8.71          16.64      3.59         7.37      12.15
                                        Isabelle (pass@10)
 High school      10.17         8.90           7.84          11.23      4.03         3.60       7.63
 University        7.48         5.34           3.63           4.49      2.78         3.21       4.49
 Competition       0.86         1.72           0.00          2.59       0.00         0.00       0.86
 Overall           6.75          5.9           4.11           6.39      2.27         2.45       4.65

Table 4: Experimental results of Multimodal Theorem Formalization (Task 2), which only require
model to generate formalized theorem. We use GPT-4o as the judge and adopt pass@10 as the
evaluation metric. We present the experimental results of pass@n (n=1, n=5) in Table 7 and 8.

                                                   Method
 Task 2                                                                                         Avg.
               OpenAI-o1     Claude-3.7     Gemini-2.0 GPT-4.1       Qwen2.5-VL   Llama3.2-V
                                        Lean 4 (pass@10)
 High school      53.12         55.07         44.02          47.58     26.84        15.50      40.36
 University       61.28         60.42         56.11          58.19     33.33        21.81      48.52
 Competition      63.32         61.64         59.40          56.03     38.66        28.58      51.27
 Overall          58.24         57.26         51.05          53.20     31.46        19.72      45.16
                                          Coq (pass@10)
 High school      42.65         39.07         27.15          37.03     16.73        11.79      29.07
 University       45.64         51.22         30.00          43.89     20.14        16.39      34.56
 Competition      63.37         65.20         54.17          68.35     38.66        31.38      53.50
 Overall          41.31         49.65         31.76          43.13     20.64        15.97      33.74
                                        Isabelle (pass@10)
 High school      51.88         49.78         35.79          42.10     21.94        17.42      36.49
 University       63.50         62.22         54.86          65.73     31.81        23.89      50.34
 Competition      63.08         58.28         42.59          44.27     25.63        19.61      42.58
 Overall          60.14         56.21         44.97          52.56     26.66        20.52      43.51



ability to convert natural language descriptions and geometric figures into Lean 4 formal statements
is relatively strong, suggesting that the primary bottleneck for Task 1 in Lean 4 is proof generation.
Coq. In the Coq language tests, the overall success rate (pass@10) for the end-to-end complete
multimodal theorem formalization and proof generation (Task 1) task is 12.86%. Compared to the
overall Task 1 success rate in Lean 4 (4.68%), the models demonstrate stronger proof generation
capability in Coq. We think that Coq’s superior performance in Task 1 can be attributed to its
more mature library of tactics, richer resources of formalized mathematics, and an imperative tactic
language style that might be more suitable for current language models to learn. Nevertheless,
the success rate still decreases with increasing theorem difficulty, although the drop appears less


                                                      7
  Claude-3.7-Sonnet-Thinking                          OpenAI-GPT4.1                          Qwen2.5-VL-Instruct-70B




      Invalid/unproven proof steps          Missing preconditions/hidden assumptions           Missing multimodal information
      Formalization-natural language mismatch         Incorrect/undeclared variables/definitions        Others
      Hallucinated/unjustified constructs

Figure 2: We perform an error analysis on the results of a reasoning model (Claude-3.7-Sonnet-Thinking) and
two non-reasoning models (GPT4.1 and Qwen2.5-VL-Instruct-70B) , all three being competitive on MATP tasks
(Lean 4), with the figure illustrating the seven most frequent error types.

severe than in Lean 4. The o1 model ranks first with an overall success rate of 19.43%, performing
particularly well at the high school level (28.37%). Task 2 (formalization only) in Coq has an overall
success rate of 35.25%, far higher than Coq’s. Simultaneously, the models’ overall performance in
generating proofs within the Coq environment is superior to that in Lean 4.
Isabelle. The overall success rate of Task 1 (4.71%) is comparable to that of Lean 4, but significantly
lower than the overall success rate of Coq, indicating that models face similarly high challenges
in performing end-to-end proof generation in the Isabelle environment as they do in Lean 4. We
hypothesize this is primarily due to two factors: firstly, while the formulation style adopted for
structured proofs in Isabelle is user-friendly for humans, its precise context management and high
degree of structural requirements, making it difficult for models to produce complex proofs fully
conforming to its syntax and logic. Secondly, although Isabelle incorporates powerful automation
tools, model success likely depends not just on invoking these tools but also on generating appropriate
intermediate steps or providing effective guidance. The o1 model ranks first at the university difficulty
level (7.48%). The performance of the Qwen2.5 and Llama3.2 models in Task 1 under the Isabelle
environment remains at the lower end. Models’ ability to convert multimodal information into Isabelle
formal statements is relatively strong, similar to Lean 4, and superior to Coq.

5.3   Analysis of Error Distribution in Multimodal Automated Theorem Proving

We analyze the types of errors generated by multimodal models in theorem proving. As shown in
Figure 2, the results indicate that different models exhibit both common errors and specific issues.
For the Claude model, the most significant errors are concentrated in invalid/unproven proof steps
(24.9%), missing preconditions/hidden assumptions (23.8%), and missing unformalized information
(underutilizing multimodal information, 23.3%); these three categories collectively account for
approximately 72% of its total errors. Similarly, the error distribution of the GPT-4.1 model is
very similar. This suggests that even for relatively better-performing models, the core challenges
lie in complex logical reasoning and identifying and utilizing all implicit and explicit information
required by the theorem. The error distribution of the Qwen2.5 model, however, differs. While
missing unformalized information (20.9%) and missing preconditions/hidden assumptions (18.7%)
are also major errors, the proportion of invalid/unproven proof steps is relatively lower (15.6%),
while more fundamental formalization errors such as missing/incorrect library imports (11.3%) and
incorrect/undeclared variables/definitions (10.6%) are more prominent. This might indicate that while
Qwen struggles with proof step errors, it also faces significant issues in generating basic code that
conforms to the formal language specification. Overall, all models commonly exhibit problems with
incomplete information understanding and broken reasoning chains.

5.4   Main Bottleneck in Multimodal Automated Theorem Proving

As shown in Figure 3, the analysis of the pass@n performance of multimodal models in the Coq
language shows that for both complete theorem formalization and proof generation (Task 1) and
formalization only (Task 2), allowing models to generate more candidates (from pass@1 to pass@10)


                                                               8
                                  High school                  University                     Competition
                  100
                  80     Task 1                                                                                  Pass@1
                  60                                                                                             Pass@5
                  40                                                                                             Pass@10
Percentage (%)

                  20
                   0
                  100
                  80     Task 2
                  60
                  40
                  20
                  0
                           Claude 3.7 GPT 4.1 Qwen 2.5   Claude 3.7 GPT 4.1 Qwen 2.5    Claude 3.7 GPT 4.1 Qwen 2.5

Figure 3: We present the performance of different MLLMs (Gemini-2.0-flash-thinking, OpenAI-GPT4.1, and
Qwen2.5-VL-Instruct-70B) on multimodal theorem automated proving (Task 1) and theorem formalization (Task
2) across varying difficulty levels, evaluated using Pass@1, Pass@5, and Pass@10 metrics.


generally increases the success rate. However, the pass@n success rate for Task 1 is significantly
lower than the pass@n success rate for Task 2 across all difficulty levels and models. For example,
at the high school difficulty level, the highest pass@10 for Task 1 reaches 28.27% for GPT-4.1,
while the pass@10 for Task 2 for the same model reaches 37.03%. Notably, the pass@n values
for Task 2, especially at the competition difficulty level, can even remain at a relatively high level
(68.35% for GPT-4.1’s pass@10). This may be attributed to the fact that the problem descriptions
for competition-level theorems are often more complete and precise, providing clearer formalization
basis for the models, even if the proof process heavily relies on complex steps like constructing
auxiliary lines (which is precisely why the Task 1 success rate is extremely low at this difficulty).
This large performance gap between Task 1 and Task 2 is consistent across all pass@n settings,
demonstrating that models have shown a certain ability in converting natural language descriptions
and geometric figures into Coq formal statements (Task 2 pass@n is relatively high), but still face
significant challenges in the subsequent complex logical reasoning and constructing formal proofs.


5.5                     Model Capability in Generating Auxiliary Constructions for Multimodal Theorems

                                                                             A characteristic distinguishing multimodal the-
   100
                                                                             orem proving from pure text theorem proving is
                                                                             that many theorems require the construction of
                                                                             auxiliary lines to aid thinking, especially prob-
    80
                                                                             lems at the competition level. Therefore, we fur-
 Percentage (%)




                                                                             ther investigate the models’ ability to construct
    60
                                                                             auxiliary lines during the proof process. As
                                                                             shown in Figure 4, with the increase in theorem
    40
                                                                             difficulty, the proportion of problems requiring
                                                                             auxiliary construction significantly rises, con-
    20
                                                                             firming the importance of auxiliary construction
                                                                             for solving high-difficulty geometric theorems.
     0
         High School                University                 Competition   Claude 3.7 and GPT 4.1, which perform best
       Proportion of Multimodal Theorems Requiring Auxiliary Construction    in Task 1 and Task 2, attempt to perform auxil-
       Claude 3.7 Attempt Rate       Claude 3.7 Success Rate (Given Attempt) iary constructions when generating proofs, and
       GPT 4.1 Attempt Rate          GPT 4.1 Success Rate (Given Attempt)    this attempt rate also increases with difficulty,
                                                                             which indicates that the models possess a certain
Figure 4: Auxiliary construction analysis by question degree of autonomous auxiliary construction ca-
difficulty level and model, evaluated using Pass@10.                         pability and awareness. However, the success
                                                                             rate of these proofs containing auxiliary con-
structions (Figure 4 blue and purple solid lines) is very low. This prominently indicates that while
models can introduce steps or concepts involving auxiliary constructions in proofs, they cannot
effectively utilize these constructions to advance the proof process. However, recent research shows
that multimodal models can be augmented by visual prompts [17; 45; 57]. For example, Visual


                                                                   9
Sketchpad [17] demonstrates this potential by providing MLLMs with a sketching interface and
drawing tools, which offers a promising direction for multimodal theorem proving.

6   Conclusion
In this paper, we introduce Multimodal Automated Theorem Proving benchmark (MATP-BENCH),
a new multimodal, multi-level, and multi-language benchmark designed to evaluate Multimodal
Large Language Models (MLLMs) as automated theorem provers. MATP-BENCH consists of 1056
multimodal theorems drawn from high school, university, and competition-level mathematics. All
these multimodal problems are accompanied by formalizations in Lean 4, Coq and Isabelle. Our
experimental results demonstrate significant variability in the performance of various mainstream
MLLMs. Our findings highlight the current capabilities and limitations of state-of-the-art MLLMs in
automated theorem proving, and indicate that the primary bottleneck in current MATP task lies in the
construction of correct formal proofs, presenting clear directions for future research.

References
 [1] Aida Amini, Saadia Gabriel, Peter Lin, Rik Koncel-Kedziorski, Yejin Choi, and Hannaneh
     Hajishirzi. Mathqa: Towards interpretable math word problem solving with operation-based
     formalisms. arXiv preprint arXiv:1905.13319, 2019. URL https://arxiv.org/abs/1905.
     13319.
 [2] Anthropic. Claude Sonnet. https://www.anthropic.com/claude/sonnet, 2024. Ac-
     cessed: 2025-04-29.
 [3] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev,
     and Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level
     mathematics. arXiv preprint arXiv:2302.12433, 2023. URL https://arxiv.org/abs/2302.
     12433.
 [4] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer,
     Albert Q Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An open language
     model for mathematics. arXiv preprint arXiv:2310.10631, 2023. URL https://arxiv.org/
     abs/2310.10631.
 [5] Wolfgang Bibel.  Automated theorem proving. Springer Science & Business Me-
     dia, 2013.      URL https://books.google.com.hk/books?hl=zh-CN&lr=&id=
     MNcACAAAQBAJ&oi=fnd&pg=PR5&dq=Automated+theorem+proving&ots=eFxi0-SoaB&
     sig=2dh8ZtPhDfhfmxFjt8ncsQ1HT1k&redir_esc=y#v=onepage&q=Automated%
     20theorem%20proving&f=false.
 [6] Jie Cao and Jing Xiao. An augmented benchmark dataset for geometric question answering
     through dual parallel text encoding. In Proceedings of the 29th international conference on
     computational linguistics, pages 1511–1520, 2022. URL https://aclanthology.org/
     2022.coling-1.130/.
 [7] Jiaqi Chen, Tong Li, Jinghui Qin, Pan Lu, Liang Lin, Chongyu Chen, and Xiaodan Liang.
     Unigeo: Unifying geometry logical reasoning via reformulating mathematical expression. arXiv
     preprint arXiv:2212.02746, 2022. URL https://arxiv.org/abs/2212.02746.
 [8] Qiguang Chen, Libo Qin, Jinhao Liu, Dengyun Peng, Jiannan Guan, Peng Wang, Mengkang
     Hu, Yuhang Zhou, Te Gao, and Wanxiang Che. Towards reasoning era: A survey of long
     chain-of-thought for reasoning large language models. arXiv preprint arXiv:2503.09567, 2025.
     URL https://arxiv.org/abs/2503.09567.
 [9] Adam Chlipala. Certified programming with dependent types: a pragmatic introduction to the
     Coq proof assistant. MIT Press, 2013. URL http://adam.chlipala.net/cpdt/.
[10] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
     Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to
     solve math word problems. arXiv preprint arXiv:2110.14168, 2021. URL https://arxiv.
     org/abs/2110.14168.


                                                10
[11] compfiles. Compfiles. https://github.com/dwrensha/compfiles, 2023. Accessed:
     [2025-04-25].
[12] Tulsee Doshi. Start building with gemini 2.5 flash. https://developers.googleblog.
     com/en/start-building-with-gemini-25-flash/, April 2025. Accessed: 2025-04-29.
[13] Simon Frieder, Luca Pinchetti, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas
     Lukasiewicz, Philipp Petersen, and Julius Berner.   Mathematical capabilities of
     chatgpt.    Advances in neural information processing systems, 36:27699–27744,
     2023.    URL https://proceedings.neurips.cc/paper_files/paper/2023/hash/
     58168e8a92994655d6da3939e7cc0918-Abstract-Datasets_and_Benchmarks.html.
[14] Daocheng Fu, Zijun Chen, Renqiu Xia, Qi Liu, Yuan Feng, Hongbin Zhou, Renrui Zhang,
     Shiyang Feng, Peng Gao, Junchi Yan, et al. Trustgeogen: Scalable and formal-verified data en-
     gine for trustworthy multi-modal geometric problem solving. arXiv preprint arXiv:2504.15780,
     2025. URL https://arxiv.org/abs/2504.15780.
[15] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and
     Jacob Steinhardt. Measuring massive multitask language understanding. arXiv preprint
     arXiv:2009.03300, 2020. URL https://arxiv.org/abs/2009.03300.
[16] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset.
     arXiv preprint arXiv:2103.03874, 2021. URL https://arxiv.org/abs/2103.03874.
[17] Yushi Hu, Weijia Shi, Xingyu Fu, Dan Roth, Mari Ostendorf, Luke Zettlemoyer, Noah A Smith,
     and Ranjay Krishna. Visual sketchpad: Sketching as a visual chain of thought for multimodal
     language models. arXiv preprint arXiv:2406.09403, 2024. URL https://arxiv.org/abs/
     2406.09403.
[18] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée
     Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal
     theorem provers with informal proofs. arXiv preprint arXiv:2210.12283, 2022. URL https:
     //arxiv.org/abs/2210.12283.
[19] Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han, and Yuhuai Wu. Lisa: Language models
     of isabelle proofs. In 6th Conference on Artificial Intelligence and Theorem Proving, pages
     378–392, 2021. URL https://aitp-conference.org/2021/abstract/paper_17.pdf.
[20] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury
     Hayat, Thibaut Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for
     neural theorem proving. Advances in neural information processing systems, 35:26337–
     26349, 2022. URL https://proceedings.neurips.cc/paper_files/paper/2022/
     hash/a8901c5e85fb8e1823bbf0f755053672-Abstract-Conference.html.
[21] Yunxin Li, Zhenyu Liu, Zitao Li, Xuanyu Zhang, Zhenran Xu, Xinyu Chen, Haoyuan Shi,
     Shenyuan Jiang, Xintong Wang, Jifang Wang, et al. Perception, reason, think, and plan: A
     survey on large multimodal reasoning models. arXiv preprint arXiv:2505.04921, 2025. URL
     https://arxiv.org/abs/2505.04921.
[22] Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
     Xia, Danqi Chen, Sanjeev Arora, et al. Goedel-prover: A frontier model for open-source
     automated theorem proving. arXiv preprint arXiv:2502.07640, 2025. URL https://arxiv.
     org/abs/2502.07640.
[23] Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. Program induction by ratio-
     nale generation: Learning to solve and explain algebraic word problems. arXiv preprint
     arXiv:1705.04146, 2017. URL https://arxiv.org/abs/1705.04146.
[24] Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
     Chuanyang Zheng, Yichun Yin, Lin Li, Ming Zhang, and Qun Liu. Fimo: A challenge formal
     dataset for automated theorem proving, 2023. URL https://arxiv.org/abs/2309.04295.


                                               11
[25] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual
     instruction tuning, 2023. URL https://openaccess.thecvf.com/content/CVPR2024/
     html/Liu_Improved_Baselines_with_Visual_Instruction_Tuning_CVPR_2024_
     paper.html.
[26] Wentao Liu, Qianjun Pan, Yi Zhang, Zhuo Liu, Ji Wu, Jie Zhou, Aimin Zhou, Qin Chen,
     Bo Jiang, and Liang He. Cmm-math: A chinese multimodal math dataset to evaluate and enhance
     the mathematics reasoning of large multimodal models. arXiv preprint arXiv:2409.02834, 2024.
     URL https://arxiv.org/abs/2409.02834.
[27] Pan Lu, Ran Gong, Shibiao Jiang, Liang Qiu, Siyuan Huang, Xiaodan Liang, and Song-Chun
     Zhu. Inter-gps: Interpretable geometry problem solving with formal language and symbolic
     reasoning. arXiv preprint arXiv:2105.04165, 2021. URL https://arxiv.org/abs/2105.
     04165.
[28] Pan Lu, Hritik Bansal, Tony Xia, Jiacheng Liu, Chunyuan Li, Hannaneh Hajishirzi, Hao
     Cheng, Kai-Wei Chang, Michel Galley, and Jianfeng Gao. Mathvista: Evaluating mathematical
     reasoning of foundation models in visual contexts. arXiv preprint arXiv:2310.02255, 2023.
     URL https://arxiv.org/abs/2310.02255.
[29] Ahmed Masry, Do Xuan Long, Jia Qing Tan, Shafiq Joty, and Enamul Hoque. Chartqa: A
     benchmark for question answering about charts with visual and logical reasoning. arXiv preprint
     arXiv:2203.10244, 2022. URL https://arxiv.org/abs/2203.10244.
[30] Swaroop Mishra, Matthew Finlayson, Pan Lu, Leonard Tang, Sean Welleck, Chitta Baral,
     Tanmay Rajpurohit, Oyvind Tafjord, Ashish Sabharwal, Peter Clark, et al. Lila: A unified
     benchmark for mathematical reasoning. arXiv preprint arXiv:2210.17517, 2022. URL https:
     //arxiv.org/abs/2210.17517.
[31] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language. In Automated Deduction–CADE 28: 28th International Conference on Automated
     Deduction, Virtual Event, July 12–15, 2021, Proceedings 28, pages 625–635. Springer, 2021.
     URL https://link.springer.com/chapter/10.1007/978-3-030-79876-5_37.
[32] Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li, Anima Anandkumar, and Xujie Si.
     Autoformalizing euclidean geometry. arXiv preprint arXiv:2405.17216, 2024. URL https:
     //arxiv.org/abs/2405.17216.
[33] OpenAI. GPT-4.1. https://openai.com/index/gpt-4-1/, 2024. Accessed: 2025-04-29.
[34] OpenAI.      Introducing o3 and o4-mini.           https://openai.com/index/
     introducing-o3-and-o4-mini/, 2024. Accessed: 2025-04-29.
[35] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
     arXiv preprint arXiv:2009.03393, 2020. URL https://arxiv.org/abs/2009.03393.
[36] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
     Sutskever. Formal mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344,
     2022. URL https://arxiv.org/abs/2202.01344.
[37] AIMO Prize. Artificial intelligence mathematical olympiad (aimo) prize, 2023. URL https:
     //aimoprize.com/.
[38] Xiaoye Qu, Yafu Li, Zhaochen Su, Weigao Sun, Jianhao Yan, Dongrui Liu, Ganqu Cui, Daizong
     Liu, Shuxian Liang, Junxian He, et al. A survey of efficient reasoning for large reasoning
     models: Language, multimodality, and beyond. arXiv preprint arXiv:2503.21614, 2025. URL
     https://arxiv.org/abs/2503.21614.
[39] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. Deepseek-prover-v2: Advancing formal
     mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
     arXiv:2504.21801, 2025. URL https://arxiv.org/abs/2504.21801.


                                                12
[40] Alan JA Robinson and Andrei Voronkov. Handbook of automated reasoning, volume 1. Elsevier,
     2001. URL https://books.google.com.hk/books?hl=zh-CN&lr=&id=HxaWA4lep_
     kC&oi=fnd&pg=PP1&dq=Handbook+of+automated+reasoning&ots=SOVKBxf0Jd&
     sig=I1BbPB9nkIm1qEsHPsux0VqxqQU&redir_esc=y#v=onepage&q=Handbook%20of%
     20automated%20reasoning&f=false.
[41] Daniel Selsam, Leonardo de Moura, Kevin Buzzard, Reid Barton, Percy Liang, Sarah Loos, and
     Freek Wiedijk. Imo grand challenge. URL https://imo-grand-challenge. github. io, 2020. URL
     https://imo-grand-challenge.github.io.
[42] Minjoon Seo, Hannaneh Hajishirzi, Ali Farhadi, Oren Etzioni, and Clint Malcolm. Solving
     geometry problems: Combining text and diagram interpretation. In Proceedings of the 2015
     conference on empirical methods in natural language processing, pages 1466–1476, 2015. URL
     https://aclanthology.org/D15-1171.pdf.
[43] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
     Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical
     reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024. URL https:
     //arxiv.org/abs/2402.03300.
[44] Wenhao Shi, Zhiqiang Hu, Yi Bin, Junhua Liu, Yang Yang, See-Kiong Ng, Lidong Bing, and
     Roy Ka-Wei Lee. Math-llava: Bootstrapping mathematical reasoning for multimodal large
     language models. arXiv preprint arXiv:2406.17294, 2024. URL https://arxiv.org/abs/
     2406.17294.
[45] Aleksandar Shtedritski, Christian Rupprecht, and Andrea Vedaldi.    What does clip
     know about a red circle? visual prompt engineering for vlms. In Proceedings of the
     IEEE/CVF International Conference on Computer Vision, pages 11987–11997, 2023. URL
     https://openaccess.thecvf.com/content/ICCV2023/html/Shtedritski_What_
     does_CLIP_know_about_a_red_circle_Visual_prompt_ICCV_2023_paper.html.
[46] Qwen Team. Qwen2.5-vl, January 2025. URL https://qwenlm.github.io/blog/qwen2.
     5-vl/.
[47] Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri. An
     in-context learning agent for formal theorem-proving. arXiv preprint arXiv:2310.04353, 2023.
     URL https://arxiv.org/abs/2310.04353.
[48] Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving olympiad geometry
     without human demonstrations. Nature, 625(7995):476–482, 2024. URL https://www.
     nature.com/articles/s41586-023-06747-5.
[49] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers
     on the putnam mathematical competition. arXiv preprint arXiv:2407.11214, 2024. URL
     https://arxiv.org/abs/2407.11214.
[50] Haiming Wang, Huajian Xin, Zhengying Liu, Wenda Li, Yinya Huang, Jianqiao Lu, Zhicheng
     Yang, Jing Tang, Jian Yin, Zhenguo Li, et al. Proving theorems recursively. arXiv preprint
     arXiv:2405.14414, 2024. URL https://arxiv.org/abs/2405.14414.
[51] Ke Wang, Junting Pan, Weikang Shi, Zimu Lu, Houxing Ren, Aojun Zhou, Mingjie
     Zhan, and Hongsheng Li. Measuring multimodal mathematical reasoning with math-
     vision dataset. Advances in Neural Information Processing Systems, 37:95095–95169,
     2024.    URL https://proceedings.neurips.cc/paper_files/paper/2024/hash/
     ad0edc7d5fa1a783f063646968b7315b-Abstract-Datasets_and_Benchmarks_Track.
     html.
[52] Peijie Wang, Zhong-Zhi Li, Fei Yin, Xin Yang, Dekang Ran, and Cheng-Lin Liu. Mv-
     math: Evaluating multimodal math reasoning in multi-visual contexts. arXiv preprint
     arXiv:2502.20808, 2025. URL https://openaccess.thecvf.com/content/CVPR2025/
     html/Wang_MV-MATH_Evaluating_Multimodal_Math_Reasoning_in_Multi-Visual_
     Contexts_CVPR_2025_paper.html.


                                               13
[53] Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang.
     Theoremllama: Transforming general-purpose llms into lean4 experts. arXiv preprint
     arXiv:2407.03203, 2024. URL https://arxiv.org/abs/2407.03203.
[54] Ruida Wang, Yuxin Li, Yi R. Fung, and Tong Zhang. Let’s reason formally: Natural-formal
     hybrid reasoning enhances llm’s math capability, 2025. URL https://arxiv.org/abs/
     2505.23703.
[55] Makarius Wenzel, Lawrence C Paulson, and Tobias Nipkow. The isabelle framework. In
     International Conference on Theorem Proving in Higher Order Logics, pages 33–38. Springer,
     2008. URL https://link.springer.com/chapter/10.1007/978-3-540-71067-7_7.
[56] Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
     Liyue Zhang, Xuan Lu, Qiushi Du, et al. Deepseek-prover-v1. 5: Harnessing proof assistant feed-
     back for reinforcement learning and monte-carlo tree search. arXiv preprint arXiv:2408.08152,
     2024. URL https://arxiv.org/abs/2408.08152.
[57] Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chunyuan Li, and Jianfeng Gao. Set-of-mark
     prompting unleashes extraordinary visual grounding in gpt-4v. arXiv preprint arXiv:2310.11441,
     2023. URL https://arxiv.org/abs/2310.11441.
[58] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with
     retrieval-augmented language models. Advances in Neural Information Processing Systems,
     36:21573–21612, 2023.        URL https://proceedings.neurips.cc/paper_files/
     paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_
     Benchmarks.html.
[59] Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean workbook:
     A large-scale lean problem set formalized from natural language math problems. arXiv preprint
     arXiv:2406.03847, 2024. URL https://arxiv.org/abs/2406.03847.
[60] Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens,
     Dongfu Jiang, Weiming Ren, Yuxuan Sun, et al. Mmmu: A massive multi-discipline multimodal
     understanding and reasoning benchmark for expert agi. In Proceedings of the IEEE/CVF
     Conference on Computer Vision and Pattern Recognition, pages 9556–9567, 2024. URL
     https://openaccess.thecvf.com/content/CVPR2024/html/Yue_MMMU_A_Massive_
     Multi-discipline_Multimodal_Understanding_and_Reasoning_Benchmark_for_
     CVPR_2024_paper.html.
[61] Renrui Zhang, Dongzhi Jiang, Yichi Zhang, Haokun Lin, Ziyu Guo, Pengshuo Qiu, Aojun
     Zhou, Pan Lu, Kai-Wei Chang, Yu Qiao, et al. Mathverse: Does your multi-modal llm truly
     see the diagrams in visual math problems? In European Conference on Computer Vision,
     pages 169–186. Springer, 2024. URL https://link.springer.com/chapter/10.1007/
     978-3-031-73242-3_10.
[62] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark
     for formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021. URL https:
     //arxiv.org/abs/2109.00110.




                                                14
A    Examples of questions at different levels

In Figure 5 and Figure 6, we show high school and university-level problems respectively, with Figure
1 featuring competition-level questions.




Figure 5: An example of a high school level mathematics problem, requiring the calculation of a triangle’s area
within a configuration of two adjacent squares (ABGH and BCDF) of differing side lengths.




Figure 6: An example of a university level mathematics problem, requiring the determination that the number
of non-repeating paths from the top to bottom vertex of a regular icosahedron, under downward or horizontal
movement constraints, is 810.


                                                      15
Table 5: Experimental results of Multimodal Automated Theorem Proving (Task 1), which requires
model to generate both formalized theorem and proof. We adopt pass@5 as the evaluation metric.

                                                   Method
  Task 1                                                                                        Avg.
                OpenAI-o1    Claude-3.7     Gemini-2.0 GPT-4.1      Qwen2.5-VL   Llama3.2-V
                                        Lean 4 (pass@5)
  High school      4.03         3.39           5.51         5.08       1.48          2.54       3.67
  University       2.78         1.71           1.50         3.38       0.86          1.72       1.99
  Competition      0.00         0.86           0.00         1.72       0.00          0.00       0.43
  Overall          3.03         2.27           3.12         3.69       1.04          1.61       2.46
                                          Coq (pass@5)
  High school     18.78         16.24          8.65         20.89      3.58          4.43       12.09
  University       6.84          8.12          3.85          4.27      2.56          3.21       4.81
  Competition      1.72          1.72          0.86          8.62      0.00          0.00       2.15
  Overall         11.63         11.08          5.67         12.19      2.65          3.40       7.78
                                        Isabelle (pass@5)
  High school      6.78         5.30           4.45         7.84       2.54          1.91       4.80
  University       4.70         3.42           2.14         3.82       1.92          2.35       3.06
  Competition      0.86         1.72           0.00         2.59       0.00          0.00       0.86
  Overall          4.11         3.48           2.2          4.97       1.49          1.42       2.94

Table 6: Experimental results of Multimodal Automated Theorem Proving (Task 1), which requires
model to generate both formalized theorem and proof. We adopt pass@1 as the evaluation metric.

                                                   Method
  Task 1                                                                                         Avg.
                OpenAI-o1    Claude-3.7     Gemini-2.0 GPT-4.1      Qwen2.5-VL    Llama3.2-V
                                          Lean 4 (pass@1)
  High school      2.75          2.54          3.18          3.39      0.85           1.48       2.36
  University       1.50          0.85          0.43          2.85      0.43           0.64       1.12
  Competition      0.00          0.86          0.00          0.00      0.00           0.00       0.14
  Overall          1.89          1.52          1.61          2.56      0.57           0.95       1.52
                                           Coq (pass@1)
  High school      10.13         6.54          3.59          6.96      1.48           3.16       5.31
  University        4.91         3.63          1.28          2.56      1.07           1.44       2.48
  Competition       0.00         0.00          0.86          7.62      0.00           0.00       1.41
  Overall           6.72         4.54          2.27          5.20      1.13           2.08       3.66
                                        Isabelle (pass@1)
  High school      4.24          3.60          2.97          4.87      1.27           0.85       2.97
  University       3.28          2.14          0.85          2.14      1.07           1.28       1.79
  Competition      0.00          1.72          0.00          0.86      0.00           0.00       0.43
  Overall          3.18          1.91          1.27          2.62      0.78           0.71       1.75


B    Multimodal Automated Theorem Proving
Tables 5 and 6 present the experimental results for Task 1, evaluating multimodal automated theorem
proving using pass@5 and pass@1 metrics, respectively, across Lean 4, Coq, and Isabelle formal
languages and three difficulty levels. Comparing the two tables, it is evident that providing models
with more attempts (pass@5 vs pass@1) generally leads to higher success rates across all models,
formal languages, and difficulty levels, highlighting the benefit of multiple decoding attempts in this
task. Analyzing the pass@5 results in Table 5, among the individual models, GPT-4.1 consistently
ranks among the top performers under pass@5, showing notable strength in handling higher difficulty
levels. Gemini-2.0, Qwen2.5-VL, and Llama3.2 generally achieve lower pass rates across most tasks
and difficulty levels under pass@5.


                                                   16
The pass@1 results in Table 6, which assesses the model’s ability to generate a correct proof on the
very first attempt, are considerably lower across the board. The relative ranking of models shifts
for some languages under this stricter metric. GPT-4.1 still demonstrates relative strength at the
competition level even at pass@1 in Coq and Isabelle, suggesting some capability for direct high-
difficulty solutions. The performance difference between pass@5 and pass@1 highlights that while
all models benefit from retries, some models, appear to leverage multiple attempts more effectively to
find a successful proof compared to their initial attempt performance, whereas others, like o1 in Coq
and Isabelle, are relatively stronger at generating a correct proof on the first try.

Table 7: Experimental results of Multimodal Theorem Formalization (Task 2), which only requires
model to generate formalized theorem. We adopt pass@5 as the evaluation metric.

                                                  Method
 Task 2                                                                                        Avg.
               OpenAI-o1     Claude-3.7    Gemini-2.0 GPT-4.1      Qwen2.5-VL    Llama3.2-V
                                       Lean 4 (pass@5)
 High school      49.64        47.58          39.36        42.92     24.70          13.58      36.29
 University       60.14        58.89          52.36        55.00     30.83          21.27      46.42
 Competition      60.52        58.84          55.47        52.11     36.42          25.90      48.21
 Overall          55.48        53.82          46.88        49.27     28.38          55.17      48.17
                                          Coq (pass@5)
 High school      38.95        31.40          23.45        31.27     13.54           9.87      24.75
 University       45.83        46.89          25.83        40.69     17.22          14.31      31.79
 Competition      63.58        60.52          53.23        65.04     35.86          30.26      51.42
 Overall          44.85        39.91          27.77        39.14     18.06          14.07      30.63
                                       Isabelle (pass@5)
 High school      43.16        42.37          30.44        45.52     19.34          15.63      32.74
 University       61.67        60.83          48.61        57.36     29.03          21.67      46.53
 Competition      57.72        54.91          37.54        38.10     21.45          16.81      37.75
 Overall          52.39        50.91          39.26        45.46     23.96          18.43      38.40




Table 8: Experimental results of Multimodal Theorem Formalization (Task 2), which only requires
model to generate formalized theorem. We adopt pass@1 as the evaluation metric.

                                                  Method
 Task 2                                                                                        Avg.
               OpenAI-o1     Claude-3.7    Gemini-2.0 GPT-4.1      Qwen2.5-VL    Llama3.2-V
                                       Lean 4 (pass@1)
 High school      33.05        30.72          24.14        26.19     13.71           7.68      24.80
 University       45.61        45.82          35.14        37.22     20.56          13.8       35.07
 Competition      43.15        39.78          36.98        33.06     24.66          19.05      35.16
 Overall          40.24        38.21          30.41        31.82     17.94          11.67      30.52
                                          Coq (pass@1)
 High school      27.66        18.92          18.10        16.46     11.38          8.68       17.73
 University       35.49        25.28          12.92        28.61      8.89          5.36       21.94
 Competition      57.26        47.63          34.18        58.72     21.85          12.61      41.72
 Overall          34.62        24.88          17.57        26.36     11.43          8.35       22.13
                                       Isabelle (pass@1)
 High school      23.68        26.31          15.77        16.73     10.97          8.78       18.29
 University       51.19        49.86          27.36        53.33     18.19          13.47      36.35
 Competition      35.66        31.70          21.85        26.34     12.89           8.95      25.46
 Overall          37.18        39.76          21.56        29.55     14.38          10.87      26.97




                                                  17
C                 Multimodal Theorem Formalization
Tables 7 and 8 present the experimental results for Multimodal Theorem Formalization (Task 2),
which evaluates models on generating formalized theorems using pass@5 and pass@1 metrics across
Lean 4, Coq, and Isabelle. As expected, pass@5 scores consistently exceed pass@1 scores, indicating
that multiple attempts improve formalization accuracy. However, compared to full proof generation
(Task 1), the relative increase from pass@1 to pass@5 appears less dramatic for Task 2, suggesting
that models capable of formalizing a theorem often do so successfully on earlier attempts. Overall,
for theorem formalization, models achieve considerably higher pass rates than for proof generation,
highlighting that generating the correct theorem statement is a less challenging task than generating
the complete proof.
Analyzing the results, o1 demonstrates particular strength in first-attempt formalization (pass@1),
frequently leading in Coq and Isabelle. Models like Claude-3.7 and GPT-4.1 show competitive
performance in specific languages or difficulty tiers, while others generally trail. These results
indicate that while current models are significantly better at theorem formalization than full proof
generation, their ability to accurately formalize theorems still varies depending on the specific formal
language and problem complexity, with o1 showing notable capabilities in this task.

                                High school                 University                   Competition
                 100
                       Lean 4                                                                           Pass@1
                 80
                                                                                                        Pass@5
                 60                                                                                     Pass@10

                 40

                 20

                  0
                 100
Percentage (%)




                       Coq
                 80

                  60

                  40

                  20

                  0
                 100
                       Isabelle
                 80

                  60

                  40

                  20

                  0
                        Claude 3.7 GPT 4.1 Qwen 2.5   Claude 3.7 GPT 4.1 Qwen 2.5   Claude 3.7 GPT 4.1 Qwen 2.5

Figure 7: We present the performance of different MLLMs (Gemini-2.0-flash-thinking, OpenAI-GPT4.1, and
Qwen2.5-VL-Instruct-70B) on multimodal automated theorem proving task across varying difficulty levels,
evaluated using Pass@1, Pass@5, and Pass@10 metrics.


D                 Performance Comparison Across Formal Languages
Figure 7 and the associated data illustrate the performance of Claude 3.7, GPT 4.1, and Qwen
2.5 on multimodal theorem proving tasks across Lean 4, Coq, and Isabelle, evaluated by Pass@1,
Pass@5, and Pass@10 metrics across varying difficulty levels. The results consistently demonstrate
that model performance significantly decreases with increasing task difficulty and improves with
a greater number of allowed attempts, with Pass@10 achieving the highest pass rates. Among the
evaluated models, GPT 4.1 generally exhibits the strongest performance across most formal languages
and difficulty levels, particularly excelling in challenging scenarios. Claude 3.7 typically ranks as


                                                             18
the second-best performer, while Qwen 2.5 consistently shows the lowest pass rates. Performance
also varies by formal language, with models often achieving higher success rates in Coq compared
to Lean 4 and Isabelle. The substantial difference between Pass@1 and Pass@10 highlights the
models’ ability to find correct proofs with multiple tries, although overall performance remains low
on complex competition-level problems for all evaluated models.

E    Limitations
This paper evaluates the capabilities of various mainstream Multimodal Large Language Mod-
els (MLLMs) in multimodal automated theorem proving. We select three different formal lan-
guages—Lean 4, Coq, and Isabelle—for testing, and compare the performance (primarily using
pass@10 as the metric) of general MLLMs including o1, Claude-3.7, Gemini-2.0, GPT-4.1, Qwen2.5-
VL, and Llama3.2-Vision on problems of varying difficulty levels. Although this study provides an
exploration into the application of MLLMs in the domain of formal proof, it also has several limita-
tions. Firstly, the testing of MLLMs in this paper primarily involves one-shot generation of formal
theorems and proofs, and does not explore multi-step or interactive proof generation capabilities.
Secondly, the analysis of the model is primarily based on its final results, without delving into its
internal mechanisms or the specific impact of different reasoning steps on performance. Future work
could consider employing more comprehensive datasets, exploring richer evaluation scenarios such
as multi-step and interactive proof generation, and conducting a more in-depth mechanistic analysis
of the models’ proof generation process.

F   Prompts
Figure 8 and 9 outlines the prompt for multimodal automated theorem proving task, which aims to
achieve end-to-end multimodal automated theorem proving similar to human provers, by directly
generating a formalized theorem and its proof from multimodal informal input. Figure 10 presents
the prompt for multimodal theorem formalization task. The prover receives the multimodal question,
and is required to formalize it into a precise theorem.




                                                 19
Figure 8: Prompt for multimodal automated theorem proving task (part1).




                                  20
Figure 9: Prompt for multimodal automated theorem proving task (part2).




                                  21
Figure 10: Prompt for multimodal theorem formalization task.




                            22
NeurIPS Paper Checklist
    1. Claims
       Question: Do the main claims made in the abstract and introduction accurately reflect the
       paper’s contributions and scope?
       Answer: [Yes]
       Justification: In this paper, we introduce MATPBENCH, a new Multimodal, Multilingual,
       and Multi-level benchmark designed to evaluate MLLMs as automated theorem provers.
       Guidelines:
          • The answer NA means that the abstract and introduction do not include the claims
             made in the paper.
          • The abstract and/or introduction should clearly state the claims made, including the
             contributions made in the paper and important assumptions and limitations. A No or
             NA answer to this question will not be perceived well by the reviewers.
          • The claims made should match theoretical and experimental results, and reflect how
             much the results can be expected to generalize to other settings.
          • It is fine to include aspirational goals as motivation as long as it is clear that these goals
             are not attained by the paper.
    2. Limitations
       Question: Does the paper discuss the limitations of the work performed by the authors?
       Answer: [Yes]
       Justification: Please refer to Section E.
       Guidelines:
          • The answer NA means that the paper has no limitation while the answer No means that
             the paper has limitations, but those are not discussed in the paper.
          • The authors are encouraged to create a separate "Limitations" section in their paper.
          • The paper should point out any strong assumptions and how robust the results are to
             violations of these assumptions (e.g., independence assumptions, noiseless settings,
             model well-specification, asymptotic approximations only holding locally). The authors
             should reflect on how these assumptions might be violated in practice and what the
             implications would be.
          • The authors should reflect on the scope of the claims made, e.g., if the approach was
             only tested on a few datasets or with a few runs. In general, empirical results often
             depend on implicit assumptions, which should be articulated.
          • The authors should reflect on the factors that influence the performance of the approach.
             For example, a facial recognition algorithm may perform poorly when image resolution
             is low or images are taken in low lighting. Or a speech-to-text system might not be
             used reliably to provide closed captions for online lectures because it fails to handle
             technical jargon.
          • The authors should discuss the computational efficiency of the proposed algorithms
             and how they scale with dataset size.
          • If applicable, the authors should discuss possible limitations of their approach to
             address problems of privacy and fairness.
          • While the authors might fear that complete honesty about limitations might be used by
             reviewers as grounds for rejection, a worse outcome might be that reviewers discover
             limitations that aren’t acknowledged in the paper. The authors should use their best
             judgment and recognize that individual actions in favor of transparency play an impor-
             tant role in developing norms that preserve the integrity of the community. Reviewers
             will be specifically instructed to not penalize honesty concerning limitations.
    3. Theory assumptions and proofs
       Question: For each theoretical result, does the paper provide the full set of assumptions and
       a complete (and correct) proof?
       Answer: [Yes]


                                                  23
   Justification: Relevant assumptions and proofs are provided in the main paper.
   Guidelines:
      • The answer NA means that the paper does not include theoretical results.
      • All the theorems, formulas, and proofs in the paper should be numbered and cross-
         referenced.
      • All assumptions should be clearly stated or referenced in the statement of any theorems.
      • The proofs can either appear in the main paper or the supplemental material, but if
         they appear in the supplemental material, the authors are encouraged to provide a short
         proof sketch to provide intuition.
      • Inversely, any informal proof provided in the core of the paper should be complemented
         by formal proofs provided in appendix or supplemental material.
      • Theorems and Lemmas that the proof relies upon should be properly referenced.
4. Experimental result reproducibility
   Question: Does the paper fully disclose all the information needed to reproduce the main ex-
   perimental results of the paper to the extent that it affects the main claims and/or conclusions
   of the paper (regardless of whether the code and data are provided or not)?
   Answer: [Yes]
   Justification: See https://github.com/Zhitao-He/MATPBench and https://
   matpbench.github.io/.
   Guidelines:
      • The answer NA means that the paper does not include experiments.
      • If the paper includes experiments, a No answer to this question will not be perceived
         well by the reviewers: Making the paper reproducible is important, regardless of
         whether the code and data are provided or not.
      • If the contribution is a dataset and/or model, the authors should describe the steps taken
         to make their results reproducible or verifiable.
      • Depending on the contribution, reproducibility can be accomplished in various ways.
         For example, if the contribution is a novel architecture, describing the architecture fully
         might suffice, or if the contribution is a specific model and empirical evaluation, it may
         be necessary to either make it possible for others to replicate the model with the same
         dataset, or provide access to the model. In general. releasing code and data is often
         one good way to accomplish this, but reproducibility can also be provided via detailed
         instructions for how to replicate the results, access to a hosted model (e.g., in the case
         of a large language model), releasing of a model checkpoint, or other means that are
         appropriate to the research performed.
      • While NeurIPS does not require releasing code, the conference does require all submis-
         sions to provide some reasonable avenue for reproducibility, which may depend on the
         nature of the contribution. For example
        (a) If the contribution is primarily a new algorithm, the paper should make it clear how
             to reproduce that algorithm.
        (b) If the contribution is primarily a new model architecture, the paper should describe
             the architecture clearly and fully.
        (c) If the contribution is a new model (e.g., a large language model), then there should
             either be a way to access this model for reproducing the results or a way to reproduce
             the model (e.g., with an open-source dataset or instructions for how to construct
             the dataset).
        (d) We recognize that reproducibility may be tricky in some cases, in which case
             authors are welcome to describe the particular way they provide for reproducibility.
             In the case of closed-source models, it may be that access to the model is limited in
             some way (e.g., to registered users), but it should be possible for other researchers
             to have some path to reproducing or verifying the results.
5. Open access to data and code
   Question: Does the paper provide open access to the data and code, with sufficient instruc-
   tions to faithfully reproduce the main experimental results, as described in supplemental
   material?


                                             24
   Answer: [Yes]
   Justification: See https://github.com/Zhitao-He/MATPBench.
   Guidelines:
      • The answer NA means that paper does not include experiments requiring code.
      • Please see the NeurIPS code and data submission guidelines (https://nips.cc/
         public/guides/CodeSubmissionPolicy) for more details.
      • While we encourage the release of code and data, we understand that this might not be
         possible, so “No” is an acceptable answer. Papers cannot be rejected simply for not
         including code, unless this is central to the contribution (e.g., for a new open-source
         benchmark).
      • The instructions should contain the exact command and environment needed to run to
         reproduce the results. See the NeurIPS code and data submission guidelines (https:
        //nips.cc/public/guides/CodeSubmissionPolicy) for more details.
      • The authors should provide instructions on data access and preparation, including how
         to access the raw data, preprocessed data, intermediate data, and generated data, etc.
      • The authors should provide scripts to reproduce all experimental results for the new
         proposed method and baselines. If only a subset of experiments are reproducible, they
         should state which ones are omitted from the script and why.
      • At submission time, to preserve anonymity, the authors should release anonymized
         versions (if applicable).
      • Providing as much information as possible in supplemental material (appended to the
         paper) is recommended, but including URLs to data and code is permitted.
6. Experimental setting/details
   Question: Does the paper specify all the training and test details (e.g., data splits, hyper-
   parameters, how they were chosen, type of optimizer, etc.) necessary to understand the
   results?
   Answer: [Yes]
   Justification: Please refer to Section 5.1.
   Guidelines:
      • The answer NA means that the paper does not include experiments.
      • The experimental setting should be presented in the core of the paper to a level of detail
         that is necessary to appreciate the results and make sense of them.
      • The full details can be provided either with the code, in appendix, or as supplemental
         material.
7. Experiment statistical significance
   Question: Does the paper report error bars suitably and correctly defined or other appropriate
   information about the statistical significance of the experiments?
   Answer: [Yes]
   Justification: Please refer to Section 5.2.
   Guidelines:
      • The answer NA means that the paper does not include experiments.
      • The authors should answer "Yes" if the results are accompanied by error bars, confi-
         dence intervals, or statistical significance tests, at least for the experiments that support
         the main claims of the paper.
      • The factors of variability that the error bars are capturing should be clearly stated (for
         example, train/test split, initialization, random drawing of some parameter, or overall
         run with given experimental conditions).
      • The method for calculating the error bars should be explained (closed form formula,
         call to a library function, bootstrap, etc.)
      • The assumptions made should be given (e.g., Normally distributed errors).
      • It should be clear whether the error bar is the standard deviation or the standard error
         of the mean.


                                              25
      • It is OK to report 1-sigma error bars, but one should state it. The authors should
        preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis
        of Normality of errors is not verified.
      • For asymmetric distributions, the authors should be careful not to show in tables or
        figures symmetric error bars that would yield results that are out of range (e.g. negative
        error rates).
      • If error bars are reported in tables or plots, The authors should explain in the text how
        they were calculated and reference the corresponding figures or tables in the text.
 8. Experiments compute resources
   Question: For each experiment, does the paper provide sufficient information on the com-
   puter resources (type of compute workers, memory, time of execution) needed to reproduce
   the experiments?
   Answer: [Yes]
   Justification: The experimental setup is detailed in Section 5.1.
   Guidelines:
      • The answer NA means that the paper does not include experiments.
      • The paper should indicate the type of compute workers CPU or GPU, internal cluster,
        or cloud provider, including relevant memory and storage.
      • The paper should provide the amount of compute required for each of the individual
        experimental runs as well as estimate the total compute.
      • The paper should disclose whether the full research project required more compute
        than the experiments reported in the paper (e.g., preliminary or failed experiments that
        didn’t make it into the paper).
 9. Code of ethics
   Question: Does the research conducted in the paper conform, in every respect, with the
   NeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?
   Answer: [Yes]
   Justification: We have reviewed the NeurIPS Code of Ethics and ensure our work aligns
   with its principles.
   Guidelines:
      • The answer NA means that the authors have not reviewed the NeurIPS Code of Ethics.
      • If the authors answer No, they should explain the special circumstances that require a
        deviation from the Code of Ethics.
      • The authors should make sure to preserve anonymity (e.g., if there is a special consid-
        eration due to laws or regulations in their jurisdiction).
10. Broader impacts
   Question: Does the paper discuss both potential positive societal impacts and negative
   societal impacts of the work performed?
   Answer: [Yes]
   Justification: Please refer to Section 1 and Section E.
   Guidelines:
      • The answer NA means that there is no societal impact of the work performed.
      • If the authors answer NA or No, they should explain why their work has no societal
        impact or why the paper does not address societal impact.
      • Examples of negative societal impacts include potential malicious or unintended uses
        (e.g., disinformation, generating fake profiles, surveillance), fairness considerations
        (e.g., deployment of technologies that could make decisions that unfairly impact specific
        groups), privacy considerations, and security considerations.


                                            26
       • The conference expects that many papers will be foundational research and not tied
         to particular applications, let alone deployments. However, if there is a direct path to
         any negative applications, the authors should point it out. For example, it is legitimate
         to point out that an improvement in the quality of generative models could be used to
         generate deepfakes for disinformation. On the other hand, it is not needed to point out
         that a generic algorithm for optimizing neural networks could enable people to train
         models that generate Deepfakes faster.
       • The authors should consider possible harms that could arise when the technology is
         being used as intended and functioning correctly, harms that could arise when the
         technology is being used as intended but gives incorrect results, and harms following
         from (intentional or unintentional) misuse of the technology.
       • If there are negative societal impacts, the authors could also discuss possible mitigation
         strategies (e.g., gated release of models, providing defenses in addition to attacks,
         mechanisms for monitoring misuse, mechanisms to monitor how a system learns from
         feedback over time, improving the efficiency and accessibility of ML).
11. Safeguards
    Question: Does the paper describe safeguards that have been put in place for responsible
    release of data or models that have a high risk for misuse (e.g., pretrained language models,
    image generators, or scraped datasets)?
    Answer: [NA]
    Justification: Our work does not involve the release of datasets or models with high risk for
    misuse.
    Guidelines:
       • The answer NA means that the paper poses no such risks.
       • Released models that have a high risk for misuse or dual-use should be released with
         necessary safeguards to allow for controlled use of the model, for example by requiring
         that users adhere to usage guidelines or restrictions to access the model or implementing
         safety filters.
       • Datasets that have been scraped from the Internet could pose safety risks. The authors
         should describe how they avoided releasing unsafe images.
       • We recognize that providing effective safeguards is challenging, and many papers do
         not require this, but we encourage authors to take this into account and make a best
         faith effort.
12. Licenses for existing assets
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in
    the paper, properly credited and are the license and terms of use explicitly mentioned and
    properly respected?
    Answer: [Yes]
    Justification: Please refer to Section 4 and Section 5.1.
    Guidelines:
       • The answer NA means that the paper does not use existing assets.
       • The authors should cite the original paper that produced the code package or dataset.
       • The authors should state which version of the asset is used and, if possible, include a
         URL.
       • The name of the license (e.g., CC-BY 4.0) should be included for each asset.
       • For scraped data from a particular source (e.g., website), the copyright and terms of
         service of that source should be provided.
       • If assets are released, the license, copyright information, and terms of use in the
         package should be provided. For popular datasets, paperswithcode.com/datasets
         has curated licenses for some datasets. Their licensing guide can help determine the
         license of a dataset.
       • For existing datasets that are re-packaged, both the original license and the license of
         the derived asset (if it has changed) should be provided.


                                             27
       • If this information is not available online, the authors are encouraged to reach out to
          the asset’s creators.
13. New assets
    Question: Are new assets introduced in the paper well documented and is the documentation
    provided alongside the assets?
    Answer: [Yes]
    Justification: See https://github.com/Zhitao-He/MATPBench.
    Guidelines:
       • The answer NA means that the paper does not release new assets.
       • Researchers should communicate the details of the dataset/code/model as part of their
          submissions via structured templates. This includes details about training, license,
          limitations, etc.
       • The paper should discuss whether and how consent was obtained from people whose
          asset is used.
       • At submission time, remember to anonymize your assets (if applicable). You can either
          create an anonymized URL or include an anonymized zip file.
14. Crowdsourcing and research with human subjects
    Question: For crowdsourcing experiments and research with human subjects, does the paper
    include the full text of instructions given to participants and screenshots, if applicable, as
    well as details about compensation (if any)?
    Answer: [Yes]
    Justification: Please refer to Section 4.
    Guidelines:
       • The answer NA means that the paper does not involve crowdsourcing nor research with
          human subjects.
       • Including this information in the supplemental material is fine, but if the main contribu-
          tion of the paper involves human subjects, then as much detail as possible should be
          included in the main paper.
       • According to the NeurIPS Code of Ethics, workers involved in data collection, curation,
          or other labor should be paid at least the minimum wage in the country of the data
          collector.
15. Institutional review board (IRB) approvals or equivalent for research with human
    subjects
    Question: Does the paper describe potential risks incurred by study participants, whether
    such risks were disclosed to the subjects, and whether Institutional Review Board (IRB)
    approvals (or an equivalent approval/review based on the requirements of your country or
    institution) were obtained?
    Answer: [Yes]
    Justification: Please refer to Section 4.
    Guidelines:
       • The answer NA means that the paper does not involve crowdsourcing nor research with
          human subjects.
       • Depending on the country in which research is conducted, IRB approval (or equivalent)
          may be required for any human subjects research. If you obtained IRB approval, you
          should clearly state this in the paper.
       • We recognize that the procedures for this may vary significantly between institutions
          and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the
          guidelines for their institution.
       • For initial submissions, do not include any information that would break anonymity (if
          applicable), such as the institution conducting the review.
16. Declaration of LLM usage


                                             28
Question: Does the paper describe the usage of LLMs if it is an important, original, or
non-standard component of the core methods in this research? Note that if the LLM is used
only for writing, editing, or formatting purposes and does not impact the core methodology,
scientific rigorousness, or originality of the research, declaration is not required.
Answer: [NA]
Justification: We only used LLM for writing, editing, or formatting.
Guidelines:
   • The answer NA means that the core method development in this research does not
      involve LLMs as any important, original, or non-standard components.
   • Please refer to our LLM policy (https://neurips.cc/Conferences/2025/LLM)
      for what should or should not be described.




                                       29
