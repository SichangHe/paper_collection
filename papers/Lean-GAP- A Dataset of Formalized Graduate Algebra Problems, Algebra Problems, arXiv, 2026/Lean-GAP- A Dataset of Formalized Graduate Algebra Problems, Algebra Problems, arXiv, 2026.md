                                                 L EAN-GAP: A Dataset of Formalized Graduate
                                                             Algebra Problems


                                                     Seewoo Lee∗               Byung-Hak Hwang∗                 Hyojae Lim                Jihoon Hyun
                                                seewoo5@berkeley.edu              bhwang@kias.re.kr             hlim@kias.re.kr        qawbecrdtey@kaist.ac.kr
arXiv:2606.02588v1 [cs.LO] 20 May 2026




                                              Ilkyoo Choi             Yeachan Park           Jineon Baek           Hyukpyo Hong               Keewoo Lee
                                             ilkyoo@hufs.ac.kr       ychpark@sejong.ac.kr   jineon@kias.re.kr       hhong78@wisc.edu      keewoo.lee@ethereum.org



                                                  Jaeseong Heo                 Hyungryul Baik              Chul-hee Lee†                 Kyu-Hwan Lee
                                                  hjs@hanyang.ac.kr             hrbaik@kaist.ac.kr         chlee@kias.re.kr             khlee@math.uconn.edu




                                                                                                Abstract
                                                      We present L EAN-GAP (Lean-Graduate Algebra Problems)3 , 430 formalized
                                                      graduate-level algebra problems from the textbook Abstract Algebra by Dum-
                                                      mit and Foote. We develop a scalable pipeline consisting of PDF-to-LATEX pre-
                                                      processing, autoformalization into Lean 4, and verification of informal–formal
                                                      correspondence. While the preprocessing and autoformalization stages can be
                                                      largely automated, we find that verification remains the most subtle and labor-
                                                      intensive component, requiring careful human oversight. Our contributions include
                                                      (i) the construction of a structured dataset of formalized exercises, (ii) a systematic
                                                      methodology for formalizing textbook mathematics, and (iii) an analysis of recur-
                                                      ring challenges in the formalization process. We also compare the performance
                                                      of different autoformalization models and highlight key bottlenecks in translating
                                                      informal statements into formal language.


                                         1      Introduction
                                         In recent years, the use of proof assistants, particularly Lean 4, for formalizing mathematics has drawn
                                         considerable attention from both the mathematics and artificial intelligence (AI) research communities.
                                         This interest has been driven in part by large-scale formalization efforts such as the Liquid Tensor
                                         Experiment [23], the Prime Number Theorem [18], and Fermat’s Last Theorem [3], and by advances
                                         in automated reasoning and theorem proving exemplified by systems such as AlphaProof [8]. At
                                         the same time, the rapid development of large language models (LLMs) has brought the problem of
                                         autoformalization to the forefront, with recent successes demonstrating the feasibility of translating
                                         informal mathematical arguments into fully formal proofs. In this context, large-scale formal libraries,
                                         most notably Lean’s Mathlib [10], play a central role, serving as extensive repositories of rigorously
                                         formalized mathematics and providing the foundational infrastructure upon which both human-driven
                                         and AI-assisted formalization efforts rely on.
                                         Despite these advances, a substantial gap remains between informal mathematics and its formal
                                         counterparts. First, the volume of formalized mathematics remains small relative to the vast corpus of
                                         informal mathematical knowledge. Second, much of the recent progress has focused on competition-
                                         style or highly specialized benchmark problems, rather than standard, high-level material, particularly
                                              ∗ Equal contribution
                                              † Corresponding author
                                              3 Dataset available at Kaggle.




                                         Preprint.
at the graduate level, that forms the foundation of mathematical training. This latter issue presents a
significant obstacle for the development of automated reasoning systems, as it reflects a scarcity of
representative and structured datasets. An instructive analogy is that of attempting to train a student
using only challenging problems, without first guiding them through the standard curriculum typically
covered in the first years of graduate study. Such an approach neglects the systematic development of
conceptual understanding and technical fluency.
The present work is motivated by the need to address this gap. Specifically, we initiate a systematic
effort to formalize exercise problems from a widely used graduate-level textbook Abstract Algebra
by Dummit and Foote [4]. By doing so, we aim to construct a corpus of formalized mathematics that
reflects standard mathematical practice, thereby providing both a foundation for training AI systems
and a bridge between informal exposition and formal reasoning in research and education. We carried
out the project in several stages: (1) preprocessing a scanned PDF copy of the textbook into LATEX
exercise statements, (2) translating the LATEX statements into Lean code via autoformalization, and (3)
verifying the correctness of the resulting informal–formal pairs. Once the necessary infrastructure was
in place, the first two steps required little human intervention. Moreover, the availability of multiple
LLM-based autoformalization systems allowed us to compare the performance of different models
within a unified pipeline. Perhaps surprisingly to non-experts, the third step, i.e., verification, proved
to be the most time-consuming, technical, and subtle. At present, there is no reliable automated
method for checking whether a formal statement faithfully captures its informal counterpart. In
particular, the mere fact that a piece of Lean code compiles successfully does not guarantee that it
correctly represents the intended mathematical meaning of the original informal statement. As a result,
this stage required careful human oversight. The authors, mathematicians with PhDs and advanced
graduate students, engaged in extensive cross-checking to identify errors, refine formulations, and
resolve subtle ambiguities arising in the formalization process. It was striking to observe that even
for standard graduate-level material, formalization demands complete understanding of the subject
with a high degree of precision and sustained attention. This highlights both the current limitations
of autoformalization systems and the importance of developing more robust methods for validating
informal–formal correspondence.
Our contributions are threefold. First, we construct a dataset of formalized exercises drawn from a
widely used textbook, naturally organized by topic, difficulty, and structural features; we name the
dataset L EAN-GAP. Second, we develop a systematic pipeline for formalizing textbook exercises.
Third, we analyze recurring patterns and bottlenecks in the formalization process. In the main body
of the paper, we describe our methodology in detail. We compare the performance of different
autoformalization models and analyze the types of difficulties and subtleties that arise in the faithful
translation of informal statements into formal language. Representative examples are presented to
illustrate these challenges, providing insights into both formalizing graduate-level mathematics and
the development of AI-assisted theorem proving systems.


2   Dummit–Foote exercises

The textbook Abstract Algebra by Dummit and Foote [4] is one of the most widely adopted texts for
graduate-level algebra courses. Designed to support a full-year course while containing substantially
more material than is typically covered in that time, it offers a broad and carefully structured
introduction to group theory, ring theory, module theory, field theory, Galois theory, homological
algebra, commutative algebra, representation theory, and related advanced topics. Its breadth makes
it both a foundational resource for students and a natural bridge to further study and research.
A distinguishing characteristic of the textbook is its extensive collection of exercises, which is
an integral part of the exposition rather than merely supplementary problems. Many important
ideas and results are introduced, developed, or foreshadowed through exercises, sometimes in
carefully organized sequences that form a parallel narrative to the main text. From the perspective of
formalization, this makes the exercises a natural and structured dataset for graduate-level algebra,
but also presents challenges: their diversity in style and difficulty, their frequent reliance on implicit
assumptions, and the informal introduction of concepts across sequences of problems all require
careful interpretation when translating them into formal language.
Our goal is to formalize all exercises from the textbook. In total, it contains 1,966 exercises. At
the time of writing, we have formalized 430 problems, more than 20% of these problems. As the


                                                    2
project progresses, we plan to invite broader community participation to complete the remaining
formalizations. The resulting dataset will be made publicly available; permission from the copyright
holder has already been granted.


3     Formalization pipeline

3.1    PDF-to-LATEX preprocessing

The first stage of the pipeline is converting exercises from a scanned PDF copy of the textbook into
LATEX statements, since LATEX preserves mathematical notation in a human-readable format. We
rendered the relevant pages as images using the pdftoppm utility from the Poppler PDF rendering
library4 and cropped out extraneous elements in the bottom margin, including running section titles
and page numbers. The cropped images were then processed using the Mathpix Convert API5 , a
third-party OCR service for STEM documents, to obtain initial LATEX transcriptions.

3.2    LATEX-to-Lean autoformalization

The LATEX statements from the preprocessing stage are translated into formal specifications in Lean 4.
We used a prompt-based approach with a large language model to convert structured mathematical
language into syntactically correct Lean declarations while preserving their semantics. The prompt
enforces consistent naming, avoids unnecessary auxiliary definitions, and ensures compatibility with
Mathlib. The outputs are concise theorem statements with sorry placeholders, serving as formal
problem statements for subsequent verification and completion.

      Prompt for autoformalization
    Give a Lean 4 code that formalizes the statement of the following algebra exercise.
    Leave proof as `by sorry` and do not attempt to complete it.
    Do not define extra variables, include them as statement of the formalized codes.
    Assume `import Mathlib` is already in place and you do NOT need to import other
    submodules.
    Keep your response short.
    The theorem name has to be `DF_{sec}_{subsec}_{exercise_num}`.
    If it consists of subproblems as (a), (b), (c), ..., then formalize each of them as `
    theorem DF_{sec}_{subsec}_{exercise_num}_a`, `theorem DF_{sec}_{subsec}_{exercise_num
    }_b`, etc.

    Here's a statement of the exercise: {exercise_statement}

    ONLY give Lean formalization WITHOUT any detailed explanations.



3.3    Verification of informal–formal correspondence

LLM-based autoformalization is not guaranteed to be correct: a generated Lean file may elaborate
successfully yet encode a statement that differs from the original exercise. Formalizing a statement
without a proof is also harder than it may look, because without a proof obligation we cannot rely on
the elaborator to expose a mismatch in meaning. We therefore require every exercise in L EAN-GAP
to pass a two-stage human review before incorporating it into the dataset. Each exercise is checked
by at least two authors, a contributor who prepares it and a maintainer who reviews it, so every single
statement in the released benchmark carries a mathematician’s sign-off.
Per-exercise workflow. Contributors work on exercises one at a time through the following steps,
illustrated in Figure 1:

        1. Selection. The contributor picks an exercise that has not yet been formalized from the Git
           repository.
    4 https://poppler.freedesktop.org
    5 https://mathpix.com/convert




                                                  3
                                                                    revise



     Human                        2. Informal   3. Formalize
                    1. Select                                   4. Open PR
 Contributor                        rewrite       (Lean 4)


 Automated                                                     5a. Elaboration
(GitHub CI)                                                         check


       Human                                                                     5b. Semantic   6. Merge
    Maintainer                                                                      review

Figure 1: Per-exercise verification workflow. Each exercise is prepared by a contributor (top lane),
passes an automated elaboration check via GitHub CI (middle lane), and is reviewed for semantic
correspondence by an independent maintainer (bottom lane) before being merged. The dashed arrow
indicates a revision request by the maintainer that is returned to the contributor.


        2. Informal rewrite. The exercise is rephrased as a self-contained theorem statement rather than
           an instruction. For example, “Show that GL2 (F2 ) is non-abelian.” is rewritten as “GL2 (F2 )
           is non-abelian.” Any notation or hypotheses inherited from the surrounding section is inlined
           so that the statement can be read without the textbook at hand.
        3. Formalization. The contributor produces a Lean 4 statement of the rewritten theorem, either
           by writing it directly or by starting from an LLM-generated candidate and editing it. In
           either case, the contributor is responsible for verifying that the final Lean statement is in
           exact correspondence with the informal rewrite.
        4. Pull request. The informal rewrite and the Lean statement are submitted together as a pull
           request to the project’s repository. Each pull request (PR) contains at most ten exercises,
           which will be examined by a maintainer.
        5. Independent review. Every PR is first checked automatically by a GitHub Actions workflow
           that elaborates each Lean declaration against the pinned Mathlib revision; a PR is only
           eligible for human review once this elaboration check passes. A maintainer then reads
           the informal–formal pair and focuses on semantic correspondence, verifying that the Lean
           declaration captures the mathematical content of the informal statement. Disagreements are
           resolved on the PR thread before merging.
        6. Merge. Once the maintainer approves, the PR is merged. The Lean declaration, together
           with the informal rewrite that was checked against it, becomes part of the released dataset.

The repository is kept current with Lean and Mathlib updates: when a new Lean version is released,
or when Mathlib renames or refactors a definition the dataset depends on, the affected declarations
are updated through the same PR-and-review process, so the human sign-off is preserved across
toolchain changes.

4      Evaluation of autoformalization systems
We evaluated autoformalization on L EAN-GAP from two angles: whether the generated Lean
elaborates, and whether the resulting statement matches the informal exercise. Because no single
model is reliable on both axes, we ran six systems in parallel: five single-shot baselines (GPT-5,
Gemma4-31B (think), Goedel-Formalizer-V2-32B, Qwen3.6-35B-A3B, and DeepSeek-R1-Distill-
Qwen-32B) and Codex, OpenAI’s coding agent (GPT-5 backbone) wrapped in an autoformalization
loop.6 The single-shot systems use one API call per exercise with the prompt from Section 3.2.
Codex instead retries each exercise with the failed code and Lean error message supplied as additional
context, until elaboration succeeds or its iteration budget is exhausted, with no human intervention
inside the loop. Because of compiler-grounded retries, Codex is not directly comparable to the
     6 Snapshots used: gpt-5-2025-08-07, gemma4:31b-it-q4_K_M, kdavis/goedel-formalizer-v2:32b, qwen3.6:35b,

deepseek-r1:32b.


                                                      4
Table 1: Per-exercise elaboration outcomes over all 1,966 exercises (column definitions in text).
Codex is listed as a reference rather than a directly comparable baseline.

          Model                                       any_pass    all_pass    fail   missing
          GPT-5                                 867 (44.1%)           577     942       157
          Gemma4-31B (think)                    233 (11.9%)           132    1733         0
          Goedel-Formalizer-V2-32B              711 (36.2%)           658    1253         2
          Qwen3.6-35B-A3B                       422 (21.5%)           306    1306       238
          DeepSeek-R1-Distill-Qwen-32B           106 (5.4%)            80     820      1040
          Codex (agent loop)                   1877 (95.5%)          1857      89          0


Table 2: Elaboration error distribution by Lean category. Counts are failing declarations per category.
  Category                          GPT-5     Gemma-31B think      Goedel    Qwen3.6   DeepSeek-R1
  lean.unknownIdentifier               243                  321       152        206             104
  lean.synthInstanceFailed             237                  218       334        212             138
  lean.invalidField                     53                   90        82         81              38
  lean.dependsOnNoncomputable            1                    3         0          4               0
  other                                  1                    1         0          0               0


single-shot baselines, but we include it as a reference point for what such loops can achieve on
L EAN-GAP.

4.1   Elaboration check

Successful elaboration is necessary but not sufficient: a statement can elaborate yet be mathemat-
ically vacuous (e.g., conclusion True, placeholder hypotheses (h : True), empty typeclasses, or
an existential over True) or fail to express the informal exercise. We complement it with eleven
suspicious-statement patterns C1–C11 (Appendix A.1, per-model and per-pattern counts in Table 4)
and an LLM-based semantic check (Section 4.2). Every generated .lean file was elaborated inde-
pendently against the pinned Lean toolchain leanprover/lean4:v4.29.1 and Mathlib revision
5e932f9. We report outcomes per exercise, marking it all_pass if every declaration elaborates,
any_pass if at least one does, fail if all attempts fail, and missing if the model produces no
declaration. sorry is allowed in proof position but counted as failure when used in a def body or
inside the statement itself.
Results. Table 1 reports per-exercise elaboration outcomes over all 1,966 exercises. GPT-5 leads
the single-shot systems with 44.1%, followed by Goedel-Formalizer-V2-32B at 36.2%, reflecting
the benefit of autoformalization-specific fine-tuning. The reasoning-trained Qwen3.6-35B-A3B
and DeepSeek-R1-Distill-Qwen-32B underperformed at 21.5% and 5.4%; DeepSeek-R1 failed to
emit any declaration for 1,040 exercises, suggesting that chain-of-thought traces consume most of
its output budget before a clean Lean formalization is produced. Gemma4-31B (think) landed at
11.9%. Codex reached 95.5% any-pass, showing that compiler-grounded retries close most of the
gap left by single-shot generation. Failures are dominated by unknownIdentifier (hallucinated
names), synthInstanceFailed (missing typeclasses), and invalidField; per-category counts are
in Table 2.
Cross-model behaviour and ceilings. Models disagreed on which exercises they could handle:
among the 1,966 exercises, only 7 were solved by every system and 654 by exactly one, a strong
argument for running models in parallel rather than picking one. The 60 universally failed exercises
cluster in advanced chapters (39 of 60 in Chapters 10–18, with Ch. 12 and Ch. 17 alone contributing
13 and 7, respectively), reflecting gaps in Mathlib’s coverage rather than model-specific weakness:
when the relevant definitions are missing, every model falls back on guessing names Lean does not
recognize. Even Codex’s agent loop ceilings at 95.5%. Many of the remaining 89 failures stem
not from missing mathematics but from Mathlib drift since training (renamed lemmas, restructured
instances, definitions made noncomputable); it is a structural limit for any pipeline whose LLM is
fixed.


                                                  5
Table 3: Per-file LLM-judge semantic evaluation. Mean score is 0–5 (5 = perfect, 3 = main idea
captured but some conditions missing, 0 = vacuous or unrelated). N may exceed 1,966 when a model
splits an exercise across files, or fall below when files are missing.

    Model                                            N     Mean       Faithful       Partial     Unfaithful       Vacuous
    GPT-5                                        1808        3.45      45.1%        46.8%             5.9%           2.2%
    Gemma4-31B (think)                           1965        2.67      21.3%        61.6%            15.8%           1.3%
    Goedel-Formalizer-V2-32B                     1962        2.59      24.3%        47.9%            22.5%           5.3%
    Qwen3.6-35B-A3B                              1727        2.76      25.8%        54.7%            17.3%           2.3%
    DeepSeek-R1-Distill-Qwen-32B                  926        1.15       2.7%        28.8%            48.3%          20.2%
    Codex (agent loop)                           1989        3.56       51.2%        38.4%             5.8%           4.6%


4.2     Semantic check via LLM

Elaboration and the C1–C11 patterns do not catch a statement that elaborates, avoids every pattern,
and still encodes the wrong mathematics: a quantifier flipped, a wrong group named, a hypothesis
silently weakened. We therefore judged each generated .lean file with Claude Opus 4.7 against a five-
axis rubric: mathematical objects (S1), hypotheses (S2), conclusion (S3), structure (S4: quantifiers
and connectives), and specificity (S5: concrete objects vs. arbitrary parameters). The judge returns
a faithfulness label (faithful/partial/unfaithful/vacuous), an integer score from 0 (unrelated)
to 5 (perfect), and zero or more issue codes from a closed vocabulary. Every emitted file is judged
regardless of elaboration, so a faithful statement with a broken proof still receives a score. The full
prompt and code list are in Appendix A.2.
Results. Per-file outcomes are in Table 3. GPT-5 leads the single-shot models, consistent with its
elaboration ranking. However, its mean score is still far from perfect, indicating that many outputs
only partially capture the target statement or omit important conditions. The results also show that
syntactic success is not equivalent to semantic correctness: Goedel-Formalizer-V2-32B has the
highest all-pass count among single-shot models, but a lower semantic mean and higher unfaithful
rate than GPT-5 and Qwen3.6-35B-A3B.
Limitations. The judge is itself an LLM: its absolute scores are not calibrated against expert review,
and it can mis-rate edge cases. We therefore read Table 3 as a relative signal across models, not
as a verdict on individual exercises. Human review by a contributor and a maintainer (Section 3.3)
remains the reference for the released benchmark.

5     Challenges in verifying informal–formal correspondence
The maintainer review described in this section is where verification was performed, and it is the step
we found most labor-intensive. Two kinds of difficulty recurred during this stage. The first is intrinsic
to the exercise: some problems rely on mathematical content that resists clean translation into Lean.
The second is detection: a Lean file may elaborate, avoid every suspicious pattern of Section 4.1, and
still encode the wrong mathematics; we found recent AI assistants useful as second readers in this
case.

5.1     Examples of exercises that are hard to formalize

5.1.1     Exercises with geometric arguments
There are several exercises that include geometry, which are hard to formalize in Lean in general. For
example, Exercises 13–18 of Chapter 14.5 are on a construction of a regular 17-gon. The first two
exercises (13 and 14) are purely algebraic problems, while the next exercises are on plane geometry
and the actual construction of a regular 17-gon, including several figures of intermediate steps. It is
not easy to formalize the notion of a straightedge and compass construction in Lean, which would
require a significant amount of effort to do it properly7 .
    7 There is a partial formalization of the notion of constructible numbers by Barroero, Bishop, Brasca, and Zilberberg, which

can be found at github.com/riccardobrasca/constructible. They defined IsConstructible K L for given fields K ⊆ L as


                                                               6
5.1.2   Exercises requiring answer-embedded formalization
Some exercises require the solver to determine all possible answers or to enumerate all
(counter)examples satisfying a given condition. Such problems pose a subtle challenge in for-
malization, as the statement of the exercise may need to incorporate aspects of the solution itself.
For instance, Exercise 11 of Chapter 1.1 asks for the order of each element in Z/12Z, and GPT-5
formalized it as follows. Here we show only the first three elements:
theorem DF_1_1_11 :
    addOrderOf (0 : ZMod 12) = 1 ∧
    addOrderOf (1 : ZMod 12) = 12 ∧
    addOrderOf (2 : ZMod 12) = 6 ∧
    ...

This formalized statement already incorporates the answers for each element and asks the solver only
to prove their correctness. This approach is also adopted by several existing benchmarks, including
MiniF2F [31], FIMO [13], Lean-Workbook [29], and DeepSeek-ProverBench [22]. However, for
benchmarking purposes, this formulation does not assess a model’s ability to “discover” answers;
rather, it evaluates only whether the model can verify that a given answer is correct.
Instead, we decided to leave the answers as definitions with sorrys to be filled in, as follows:
def DF_1_1_11_ans : Fin 12 → N
    | 0 => sorry
    | 1 => sorry
    | 2 => sorry
    ...

theorem DF_1_1_11 : ∀ i : ZMod 12, addOrderOf i = answer i := by

This is better than the previous formalization in the sense that it asks the model to both fill in the
answers and prove that they are correct, and some of the previous benchmarks including Putnam-
Bench [26] follow this convention. However, one can easily hack the task by defining answer i as
addOrderOf (i : ZMod 12) instead of providing the expected numerical answers. Then the exer-
cise can be proved simply by intro i; rfl, which is far from what we intended to test. To mitigate
this issue, we wrote a Python script that checks whether a submitted answer satisfies problem-specific
specifications. If the check passes, then the script replaces the sorrys with the submitted answers and
verifies that the resulting proof is valid. Note that some previous datasets use different approaches,
such as SymPy-based checks [11, 6] or formal verification with restricted tactics [15].

5.1.3   Exercises requiring definitions not yet in Mathlib
Some of the exercises require definitions that are not yet formalized in Mathlib. Exercise 6 of
Chapter 14.8 asks to prove that the Galois group of x5 + 15x + 12 (over Q) is F20 , the Frobenius
group of order 20, and F20 is not formalized yet in Mathlib. So we define it via generators and
relations following the definition in Chapter 5.3 and state the exercise against this construction:
inductive Generators | u | v deriving DecidableEq, Repr

open FreeGroup in
def F20 := PresentedGroup {
  (of Generators.u)^4,
  (of Generators.v)^5,
  (of Generators.u) * (of Generators.v) * (of Generators.u)^(-1 : Z) * (of Generators.v)^(-2 : Z)
}

deriving instance Group for F20

theorem DF_14_8_6 : Nonempty ((X ^ 5 + 15 * X + 12 : Q[X]).Gal ≃* F20 ) := by

There are several other exercises that are hard to formalize; these can be found in Appendix A.4.

an inductive type, but did not show the correspondence between this notion of constructibility and geometric moves by a
straightedge and compass.


                                                          7
5.2   Finding and fixing misformalized exercises with AI

We also used Claude Opus 4.7 and Aristotle [1] to help with correcting autoformalized statements,
or even human-formalized statements that contained errors. We first illustrate an example with a
                                                                                          −1       −1
semantic error. Exercise 15 of Chapter 1.1 asks to prove (a1 a2 · · · an )−1 = a−1   n an−1 · · · a1 for
elements a1 , a2 , . . . , an of a group G. The initial hand-crafted formalization was the following:
theorem DF_1_1_15 {G : Type*} [Group G] (l : List G) :
    (l.foldl (· * ·) 1)−1 = (l.map (·−1 )).foldr (· * ·) 1 := by


Claude Opus 4.7 found that the right-hand side gives a−1 −1       −1
                                                      1 a2 · · · an instead, and also suggested
correcting it to
theorem DF_1_1_15 {G : Type*} [Group G] (l : List G) :
    (l.foldl (· * ·) 1)−1 = (l.reverse.map (·−1 )).foldl (· * ·) 1 := by

Notably, we found a subtle case where an autoformalized statement had neither a syntax nor a
semantic error, but an original informal statement was faulty. Exercise 21 of Chapter 2.3 is the
following:

 Let p be an odd prime and let n be a positive integer. Use the binomial theorem to show that
          n−1                              n−2
 (1 + p)p      ≡ 1 (mod pn ) but (1 + p)p       ̸≡ 1 (mod pn ). Deduce that 1 + p is an element of
 order p n−1
              in the multiplicative group (Z/p Z)× .
                                               n


The original statement above requires an additional constraint: n ≥ 2 is necessary in order for pn−2
to be well-defined as an integer. Also, this additional constraint is crucial to make the statement true
in Lean. The following initial formalization closely followed the original statement:
theorem DF_2_3_21_1 {p n : N} (hp : p.Prime) (hodd : Odd p) (hn : 0 < n) :
    (1 + p) ^ (p ^ (n - 1)) ≡ 1 [ZMOD (p ^ n)] ∧
    ¬ (1 + p) ^ (p ^ (n - 2)) ≡ 1 [ZMOD (p ^ n)] := by

Aristotle [1] was able to find a counterexample, namely (n, p) = (1, 3), showing that the statement
above is false. In Lean, for natural numbers a, b with a < b, the expression a − b is defined to be 0.
Hence 1 − 2 = 0, and the pair (n, p) = (1, 3) indeed gives a counterexample, which is not aligned
with the original intent of the problem. It is now corrected with hn : 2 ≤ n.

6     Related work
6.1   Autoformalization

Autoformalization is the task of automatically translating informal mathematical statements into
formal representations in interactive theorem provers such as Lean. Recent advances in large language
models have led to notable progress, with approaches broadly falling into sequence-to-sequence
translation, retrieval-augmented generation, and compiler- or process-guided methods [2, 14, 17].
In addition, large-scale synthetic data generation has been shown to improve performance and
scalability [28]. Domain-specific studies further demonstrate that structural constraints can make
autoformalization more tractable, while also highlighting the importance of domain knowledge and
dataset design [20].
Verification of informal–formal correspondence (i.e., semantic verification) remains a fundamental
challenge in autoformalization, due to the ambiguity and implicit assumptions in informal mathemat-
ics and the lack of reliable evaluation metrics. FormalMATH [30] reports that 60.7% of syntactically
valid Lean 4 statements were rejected at the semantic verification stage, revealing a substantial
gap between syntactic correctness and semantic fidelity. Prior works have proposed proxy metrics
including type-check rate [2], back-translation-based semantic consistency and symbolic equiva-
lence [12], cross-provability-based metrics [14], and operator-tree structural similarity [16]. Poiroux
et al. [21] provided a more systematic treatment via BEq+ and accompanying benchmarks. Despite
these efforts, reliable semantic evaluation remains an open problem [14, 21]. Furthermore, scaling
autoformalization beyond isolated statements to textbook- or project-level settings further compounds
these challenges through dependency management and global consistency requirements [7, 27].


                                                   8
6.2   Datasets and benchmarks for formal mathematics

Datasets for formal mathematics span a range from high-school Olympiad benchmarks such
as miniF2F [31] and FIMO [13] to (under)graduate and research-oriented challenges including
ProofNet [2], TaoBench [25], PutnamBench [26], FormalQualBench [19], and the FATE series
[9, 24]. Notably, both ProofNet [2] and FATE-M [24] specifically target Dummit–Foote [4] as a
primary source to represent the core (under)graduate algebra curriculum. ProofNet formalizes 87
problems from this textbook through expert-led manual formalization in Lean 3. In contrast, FATE-M
consists of 141 problems in total, curated from 12 leading textbooks including Dummit–Foote, and
employs student-led formalization in Lean 4 followed by rigorous PhD-level review to provide
compiler-verified formal proofs. Recent benchmarks have expanded in both mathematical scope
and system support. For instance, PutnamBench provides a multi-language collegiate competition
benchmark supporting Lean 4, Isabelle, and Coq, while FATE-X [9] addresses advanced commutative
algebra at PhD qualifying exam levels that can exceed current library coverage.
To address data scarcity, construction methodologies have shifted from manual formalization to
large-scale automated pipelines. DeepSeek-Prover [28] and Lean Workbook [29] utilize synthetic
generation and active learning to generate large-scale corpora of formal statements and proofs.
Complementary efforts such as HERALD [5] and FORML4 [17] augment formal libraries with
natural language annotations and leverage compiler feedback for process-driven autoformalization.
These approaches aim to improve semantic alignment between informal reasoning and formal proof
steps.

7     Conclusion
In this work, we have initiated a systematic effort to bridge the gap between informal mathematical
practice and its formal counterparts by focusing on standard graduate-level material in abstract
algebra. Through the formalization of exercises from Abstract Algebra by Dummit and Foote [4],
we have constructed a dataset of graduate algebra problems, called L EAN-GAP, that reflects the
structure, breadth, and level of difficulty typical of mainstream mathematical training. While recent
advances in autoformalization and LLMs have enabled substantial automation in the early stages of
the pipeline, current LLMs cannot be relied upon as end-to-end autoformalizers, even for standard
graduate-level material: a model can elaborate against Mathlib at a high rate yet still omit hypotheses
or capture only part of the informal claim. Verification of informal–formal correspondence therefore
remains a fundamental bottleneck, requiring careful human oversight and adequate mathematical
understanding throughout the pipeline.
Rather than treating autoformalization as a problem to be solved end-to-end by a single LLM, our
pipeline is built around productive human–AI collaboration. AI assistants serve as useful second
readers during verification, identifying subtle errors in hand-crafted formalizations and surfacing
unstated hypothesis in the textbook itself. Our pipeline thus offers an efficient template for deploying
AI as collaborators within a human-in-the-loop process, rather than as standalone formalizers.
Beyond the construction of a dataset, our work develops a systematic methodology for formalizing
textbook mathematics and provides a detailed analysis of the challenges that arise in this process.
The insights gained from this study, ranging from ambiguities in informal statements to structural
mismatches between human reasoning and formal systems, suggest that progress depends on the
joint evolution of the original mathematics material, the underlying formal library, the evaluation
infrastructure, and the model itself, with implications for both formalization of standard graduate-level
mathematics and the development of AI-assisted theorem proving tools.
Looking ahead, we plan to complete the formalization of the remaining exercises through broader
community participation, creating a comprehensive benchmark for graduate-level mathematics.
We also plan to use L EAN-GAP to generate informal–formal pairs of solutions via automated
theorem provers, offering a complementary evaluation framework to existing benchmarks focused
on competition-style problems. By focusing on standard mathematical training, this direction may
be viewed as a step toward developing an “AI mathematics student,” if not yet an “AI mathematics
researcher.” L EAN-GAP will also serve as an educational resource: making formalized versions of
standard exercises widely available can support learning, curriculum development, the integration
of formal methods into mainstream mathematical practice, and deeper interactions between the
mathematics and AI communities.


                                                   9
Acknowledgments and Disclosure of Funding
We are grateful to John Wiley & Sons, Inc. for granting us permission to use material from Abstract
Algebra by Dummit and Foote [4] in this work, in the form of transformed representations as
computer code, for non-commercial research and educational purposes. We thank Wyatt Thompson
from OpenAI, who generously provided credits for GPT-5 to the first-named author. We also thank
Nayeong Kim for contributions to formalizing problems in the dataset. Ilkyoo Choi was supported
by the Hankuk University of Foreign Studies Research Fund, the National Research Foundation
of Korea (NRF) grant funded by the Korea government (MSIT) (RS-2025-23324220), Institute for
Basic Science (IBS-R029-C1), and the Korea Institute for Advanced Study (KIAS) grant funded
by the Korea government. Hyungryul Baik was supported by the National Research Foundation of
Korea (NRF) grant funded by the Korean government (MSIT) (No. RS-2025-00513595). Byung-Hak
Hwang and Hyojae Lim were supported by KIAS Individual Grant (AP098201, AP109701) via the
Center for Artificial Intelligence and Natural Sciences at Korea Institute for Advanced Study (KIAS).
This work was supported by the Center for Advanced Computation (CAC) at Korea Institute for
Advanced Study (KIAS).

References
 [1] Achim, T., Best, A., Bietti, A., Der, K., Fédérico, M., Gukov, S., Halpern-Leistner, D., Hen-
     ningsgard, K., Kudryashov, Y., Meiburg, A., Michelsen, M., Patterson, R., Rodriguez, E.,
     Scharff, L., Shanker, V., Sicca, V., Sowrirajan, H., Swope, A., Tamas, M., Tenev, V., Thomm,
     J., Williams, H., and Wu, L. Aristotle: IMO-level automated theorem proving, 2025. URL
     https://arxiv.org/abs/2510.01346.

 [2] Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W., Radev, D., and Avigad, J. ProofNet:
     Autoformalizing and formally proving undergraduate-level mathematics, 2023. URL https:
     //arxiv.org/abs/2302.12433.

 [3] Buzzard, K.     Fermat’s Last Theorem formalization project.                      URL https://
     imperialcollegelondon.github.io/FLT/.

 [4] Dummit, D. S. and Foote, R. M. Abstract Algebra. John Wiley & Sons, 3rd edition, 2003.

 [5] Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and Dong, B. Herald: A natural language
     annotated Lean 4 dataset. In The 13th International Conference on Learning Representations,
     2025. URL https://openreview.net/forum?id=Se6MgCtRhz.

 [6] Glazer, E., Erdil, E., Besiroglu, T., Chicharro, D., Chen, E., Gunning, A., Olsson, C. F., Denain,
     J.-S., Ho, A., de Oliveira Santos, E., Järviniemi, O., Barnett, M., Sandler, R., Vrzala, M., Sevilla,
     J., Ren, Q., Pratt, E., Levine, L., Barkley, G., Stewart, N., Grechuk, B., Grechuk, T., Enugandla,
     S. V., and Wildon, M. FrontierMath: A benchmark for evaluating advanced mathematical
     reasoning in AI, 2025. URL https://arxiv.org/abs/2411.04872.

 [7] Gloeckle, F., Rammal, A., Arnal, C., Munos, R., Cabannes, V., Synnaeve, G., and Hayat, A.
     Automatic textbook formalization, 2026. URL https://arxiv.org/abs/2604.03071.

 [8] Hubert, T., Mehta, R., Sartran, L., Horváth, M. Z., Žužić, G., Wieser, E., Huang, A.,
     Schrittwieser, J., Schroecker, Y., Masoom, H., Bertolli, O., Zahavy, T., Mandhane, A.,
     Yung, J., Beloshapka, I., Ibarz, B., Veeriah, V., Yu, L., Nash, O., Lezeau, P., Mercuri, S.,
     Sönne, C., Mehta, B., Davies, A., Zheng, D., Pedregosa, F., Li, Y., von Glehn, I., Row-
     land, M., Albanie, S., Velingker, A., Schmitt, S., Lockhart, E., Hughes, E., Michalewski,
     H., Sonnerat, N., Hassabis, D., Kohli, P., and Silver, D. Olympiad-level formal mathe-
     matical reasoning with reinforcement learning. Nature, 651(8106):607–613, 2026. URL
     https://doi.org/10.1038/s41586-025-09833-y.

 [9] Jiang, J., He, W., Yuefeng, W., Gao, G., Hu, Y., Wang, J., Guan, N., Wu, P., Dai, B., Xiao,
     L., and Dong, B. FATE: A formal benchmark series for frontier algebra of multiple difficulty
     levels. In The 14th International Conference on Learning Representations, 2026. URL
     https://openreview.net/forum?id=3bD19r4jqh.


                                                   10
[10] Lean Prover Community. Mathlib4: The Lean mathematical library. URL https://github.
     com/leanprover-community/mathlib4.

[11] Lewkowycz, A., Andreassen, A., Dohan, D., Dyer, E., Michalewski, H., Ramasesh, V., Slone,
     A., Anil, C., Schlag, I., Gutman-Solo, T., Wu, Y., Neyshabur, B., Gur-Ari, G., and Misra,
     V. Solving quantitative reasoning problems with language models. In Proceedings of the
     36th International Conference on Neural Information Processing Systems, 2022. URL https:
     //openreview.net/forum?id=IFXTZERXdM7.

[12] Li, Z., Wu, Y., Li, Z., Wei, X., Yang, F., Zhang, X., and Ma, X. Autoformalize mathematical
     statements by symbolic equivalence and semantic consistency. In Proceedings of the 38th
     International Conference on Neural Information Processing Systems, 2024. URL https:
     //openreview.net/forum?id=8ihVBYpMV4.

[13] Liu, C., Shen, J., Xin, H., Liu, Z., Yuan, Y., Wang, H., Ju, W., Zheng, C., Yin, Y., Li, L., Zhang,
     M., and Liu, Q. FIMO: A challenge formal dataset for automated theorem proving, 2023. URL
     https://arxiv.org/abs/2309.04295.

[14] Liu, Q., Zheng, X., Lu, X., Cao, Q., and Yan, J. Rethinking and improving autoformalization:
     Towards a faithful metric and a dependency retrieval-based approach. In The 13th International
     Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=
     hUb2At2DsQ.

[15] Liu, Q., Zheng, X., Xia, R., Qi, X., Cao, Q., and Yan, J. Beyond theorem proving: Formulation,
     framework and benchmark for formal problem-solving, 2025. URL https://arxiv.org/abs/
     2505.04528.

[16] Liu, X., Zhu, T., Dong, Z., Liu, Y., qingfeng, G., ZhaoXuan, L., Chen, Y., and Luo, T.
     ASSESS: A semantic and structural evaluation framework for statement similarity. In The 14th
     International Conference on Learning Representations, 2026. URL https://openreview.
     net/forum?id=avwNGWtiHF.

[17] Lu, J., Wan, Y., Liu, Z., Huang, Y., Xiong, J., Liu, C., Shen, J., Jin, H., Zhang, J., Wang,
     H., Yang, Z., Tang, J., and Guo, Z. Process-driven autoformalization in Lean 4, 2024. URL
     https://doi.org/10.48550/arXiv.2406.01940.

[18] Math Inc. StrongPNT: Formalizing the Prime Number Theorem. https://math-inc.github.
     io/strongpnt/.

[19] Math Inc. FormalQualBench. https://github.com/math-inc/FormalQualBench, 2026.

[20] Murphy, L., Yang, K., Sun, J., Li, Z., Anandkumar, A., and Si, X. Autoformalizing Euclidean
     geometry. In Proceedings of the 41st International Conference on Machine Learning, 2024.
     URL https://dl.acm.org/doi/10.5555/3692070.3693567.

[21] Poiroux, A., Weiss, G., Kunčak, V., and Bosselut, A. Reliable evaluation and benchmarks for
     statement autoformalization. In Proceedings of the 2025 Conference on Empirical Methods in
     Natural Language Processing, pp. 17947–17969, 2025. URL https://aclanthology.org/
     2025.emnlp-main.907/.

[22] Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W., Zhang, L., Fu, Z., Zhu, Q., Yang,
     D., Wu, Z. F., Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D., and Ruan, C. DeepSeek-
     Prover-V2: Advancing formal mathematical reasoning via reinforcement learning for subgoal
     decomposition, 2025. URL https://arxiv.org/abs/2504.21801.

[23] Scholze, P. Liquid tensor experiment, 2020. Available at https://xenaproject.wordpress.
     com/2020/12/05/liquid-tensor-experiment/.

[24] Shen, Z., Huang, N., Yang, F., Wang, Y., Gao, G., Xu, T., Jiang, J., He, W., Yang, P., Sun, M.,
     Ju, H., Wu, P., Dai, B., and Dong, B. REAL-Prover: Retrieval augmented Lean prover for
     mathematical reasoning, 2025. URL https://arxiv.org/abs/2505.20613.


                                                  11
[25] Taylor, A. K., Zhang, J., Ji, E., Sahai, V., Deng, H., Chen, Y., Yuan, Y., Wu, D., Gu, J.-C.,
     Chang, K.-W., Peng, N., Sahai, A., and Wang, W. TaoBench: Do automated theorem prover
     LLMs generalize beyond Mathlib?, 2026. URL https://arxiv.org/abs/2603.12744.

[26] Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jennings, M., Thakur, A., and Chaudhuri,
     S. PutnamBench: Evaluating neural theorem-provers on the Putnam mathematical competition.
     In Proceedings of the 38th Conference on Neural Information Processing Systems Datasets and
     Benchmarks Track, 2024. URL https://openreview.net/forum?id=ChKCF75Ocd.

[27] Wang, Z., Ma, W., Ming, Z., Zhang, G., Yuan, K., and Wen, Z. M2F: Automated formalization
     of mathematical literature at scale, 2026. URL https://arxiv.org/abs/2602.17016.

[28] Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan, C., Li, W., and Liang, X.
     Advancing theorem proving in LLMs through large-scale synthetic data. In The 4th Workshop
     on Mathematical Reasoning and AI at NeurIPS’24, 2024. URL https://openreview.net/
     forum?id=TPtXLihkny.

[29] Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and Chen, K. Lean Workbook: A large-scale
     Lean problem set formalized from natural language math problems. In Proceedings of the 38th
     Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2024.
     URL https://openreview.net/forum?id=Vcw3vzjHDb.

[30] Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M., Zhang, Y., Yuan, Z., Xin, H., Huang, W.,
     Wen, Y., Zhang, G., and Liu, W. FormalMATH: Benchmarking formal mathematical reasoning
     of large language models, 2025. URL https://arxiv.org/abs/2505.02735.

[31] Zheng, K., Han, J. M., and Polu, S. miniF2F: a cross-system benchmark for formal Olympiad-
     level mathematics. In International Conference on Learning Representations, 2022. URL
     https://openreview.net/forum?id=9ZPegFuFTFv.


A     Appendix
A.1   Suspicious-statement patterns

Successful Lean elaboration is a necessary but not a sufficient condition for a correct autoformaliza-
tion: a file can type-check and still encode a mathematically vacuous statement. We therefore pair
the elaboration check of Section 4.1 with the eleven suspicious-statement patterns (C1–C11) defined
below. Each pattern is detected with simple checks on the generated .lean files: regular expressions
on the source together with a few queries on the parsed declaration. A declaration that elaborates
but matches at least one pattern is deducted from the strict pass rate. Patterns C1, C2, C4–C8 pass
elaboration silently because Lean has no reason to reject a trivially-true statement, so unless we check
for them they would be counted as successes. Patterns C3 and C9–C11 usually make elaboration
fail, but a few files still slip past it (for example, by hiding sorry inside a def whose declared type
happens to match), so we list them as well. The pattern list was calibrated against the human-curated
reference set (Section 4.1) and the full classification is released with the dataset.

C1. Trivial conclusion : True: the theorem claims True and preserves none of the informal content.
C2. Answer-as-free-parameter: a parameter named answer, cond, result, etc. appears on both sides
     of a biconditional ((answer : Prop) : M ∈ B ↔ answer); vacuously true under answer
     := M ∈ B.
C3. Placeholder text: tokens such as some_condition, /* conditions here */, _to_be_filled,
     or Please replace remain in the code.
C4. Placeholder hypothesis (h : True): a condition from the informal statement is encoded as a
     True hypothesis, weakening “if X then Y ” into an unconditional claim.
C5. by trivial on : True: a C1-style conclusion is paired with a completed trivial proof, so the
     declaration carries no sorry warning.
C6. def ... : Prop := True: the central concept is defined as True; every theorem mentioning
     it is vacuously satisfied, with the failure hidden one layer below the theorem.


                                                  12
Table 4: Suspicious-pattern statistics by single-shot model. Upper block: per-pattern occurrences (a
single declaration matching two patterns contributes to both rows). Lower block: total declarations
submitted by the model and the share matching at least one of C1–C11. Codex is omitted because its
agent loop changes the baseline at which pattern-level comparisons are meaningful.
 ID        Pattern                             GPT-5   Gemma-31B    Goedel   Qwen3.6    DeepSeek-R1
 C1        trivial conclusion : True              12            3        0          5             85
 C2        answer-as-free-parameter                0            0        0          1              0
 C3        placeholder text                        0            1        0          0              5
 C4        placeholder hypothesis (h : True)       7            1        1          1              0
 C5        by trivial on : True                    5            0        0          0             37
 C6        def ... : Prop := True                 14            0        0          0              0
 C7        vacuous existential                    54            6       66         27              2
 C8        excluded middle as conclusion           1            0        0          0              0
 C9        def X := sorry                          0           12        8          0              0
 C10/11    sorry inside statement                  0            1        1          3              0
 Total occurrences                                93           24       76         37            129
 Total declarations                             4679         3858     2334       3340           2009
 Flag rate                                      1.9%         0.6%     3.3%       1.1%           4.6%


C7. Vacuous existential: a statement of the form ∃ x, True (or ∃ x, x = x, or an existential over
     an unconstrained Prop binder) with no additional constraint on the witness.
C8. Excluded middle as conclusion: the conclusion is a disjunction P ∨ ¬P, always provable in
     classical logic regardless of P .
C9. def X := sorry: a helper definition is skipped entirely; dependent theorems elaborate but have
     no mathematical content.
C10. sorry inside a statement’s let: a let-binding within the theorem statement has := sorry as
     the defined value.
C11. sorry as right-hand side of ↔: the statement includes ... ↔ sorry; one side of the bicondi-
     tional is literally absent.

Per-model distribution. Profiles differ across models (Table 4): DeepSeek-R1 falls back on trivial
: True conclusions (C1) and proofs (C5), Goedel and GPT-5 concentrate on vacuous existentials
(C7), and Gemma4-31B’s few flags are mostly def ... := sorry (C9).

A.2     The LLM judge prompt

The verbatim prompt used by the judge of Section 4.2. Each (exercise, model) pair is sent this text as
the system message, followed by the informal LATEX statement and the generated Lean file.
      Prompt for LLM-judge semantic check
 You are an expert mathematician evaluating Lean 4 formalizations of exercises from
 Dummit & Foote's "Abstract Algebra". Your task is to judge whether each Lean
 statement faithfully represents the original exercise.

 IMPORTANT RULES:
 - Focus on the STATEMENT only. `sorry` in proof bodies is expected -- ignore it.
 - `sorry` in definition bodies (def X := sorry) or let bindings IS a problem -- it
 means the definition wasn't provided.
 - `: True` as a conclusion means the formalization gave up -- it's vacuous (score 0).
 - `def X : Prop := True` is a vacuous definition that makes any theorem using X
 meaningless.
 - Helper definitions (def, class, instance) before the main theorem are part of the
 formalization. Evaluate them together.
 - Sub-part theorems (DF_X_Y_Z_a, _b, _c, _1, _2) together cover one exercise --
 evaluate them as a group.
 - Docstrings (/-- ... -/) are just comments, ignore them for evaluation.



                                                  13
 For each exercise, evaluate on these 5 criteria:

 S1. Mathematical Objects: Are the structures (groups, rings, matrices, etc.)
 correctly represented?
 S2. Hypotheses: Are all conditions from the original captured? Any missing or extra?
 S3. Conclusion: Does the Lean conclusion match what the exercise asks to prove/
 determine?
 S4. Structure: Are quantifiers (forall / exists), connectives (-> / <-> / and / or)
 used correctly?
 S5. Specificity: If the exercise names concrete objects (S_3, Z/nZ, etc.), are they
 concrete in the formalization (not arbitrary parameters)?

 Return a JSON array of objects, one per exercise. Each object:
 {
   "id": "<exercise_id__model>",
   "faithfulness": "faithful" | "partial" | "unfaithful" | "vacuous",
   "score": <0-5>,
   "issues": [<list of issue codes>],
   "reasoning": "<1-3 sentences>"
 }

 Score guide:
   5 = perfect formalization (possibly with minor style differences)
   4 = minor issue (equivalent but unusual formulation)
   3 = main idea captured but missing some conditions
   2 = partially correct, significant issues
   1 = barely related to original
   0 = vacuous / completely wrong / unrelated

 Issue codes (closed vocabulary):
   missing_hypothesis       -- a condition from the original is absent
   extra_hypothesis         -- hypothesis not in the original is added
   wrong_conclusion         -- the conclusion doesn't match the exercise
   free_variable_distortion -- concrete objects replaced by arbitrary parameters
   vacuous_statement        -- conclusion is trivially true (e.g., True)
   wrong_structure          -- structural encoding is inappropriate
   wrong_quantifier         -- forall / exists direction is wrong
   missing_typeclass        -- required typeclass (e.g., [Group G]) is missing
   conclusion_too_weak      -- conclusion is weaker than what the exercise asks
   conclusion_too_strong    -- conclusion is stronger than what the exercise asks
   wrong_object             -- wrong mathematical object used
   answer_as_parameter      -- answer is left as a free parameter instead of being
 determined
   def_body_sorry           -- definition body uses sorry (not proof body)
   wrong_hypothesis         -- a hypothesis is stated incorrectly

 Return ONLY the JSON array, no other text.



A.3   Per-model issue distribution

Table 5 reports the per-model count of each issue code emitted by the judge of Section 4.2 across all
judged files. Rows are sorted by total occurrences. A single file can carry multiple issue codes, so
column counts can exceed the per-model file counts N in Table 3.
The profiles differ noticeably across models: for example, Gemma-31B leans heavily on
wrong_structure and wrong_object while Codex concentrates on conclusion_too_weak and
missing_hypothesis, reflecting the distinct ways each model fails.

A.4   Additional exercise examples

Exercises depending on other statements


                                                 14
Table 5: Issue-code occurrences per model. A judged file matching multiple codes contributes to
each row independently.
  Issue code                           GPT-5      Gemma-31B          Goedel      Qwen3.6       DeepSeek-R1   Codex
  wrong_structure                          331               899         649           536             409     215
  wrong_object                             253               725         564           696             378     120
  wrong_conclusion                         235               370         505           390             500     176
  missing_hypothesis                       174               223         304           242             391     305
  conclusion_too_weak                      189               103         207           102              45     338
  vacuous_statement                        137                45         133            53             205     110
  free_variable_distortion                  95                64          91            93             174     154
  wrong_hypothesis                          90               120         167           129              53      77
  missing_typeclass                         31               143          74            73             107      28
  extra_hypothesis                          52                32          41            68              44      49
  answer_as_parameter                       28                38          96            51              19      45
  def_body_sorry                            34                43          60            42              13      21
  wrong_quantifier                           5                17          15             6              11       5
  conclusion_too_strong                      7                 2           9             7               0       4


Several exercises depend on, or explicitly refer to, other exercises. For example, Exercise 16 of
Chapter 3.2 asks the reader to prove Fermat’s little theorem, i.e. ap ≡ a (mod p) for all prime p and
integer a, using Lagrange’s theorem. If one ignores the reference to Lagrange’s theorem, the exercise
can be formalized as follows:
theorem DF_3_2_16 {p : N} (hp : p.Prime) (a : Z) : a ^ p ≡ a [ZMOD p] := by
  sorry

However, another possibility is to formalize Lagrange’s theorem separately and include it as an
assumption in the statement of the exercise:
def DF_3_2_16_Lagrange : Prop := ∀ (G : Type*) [Group G] [Finite G], ∀ (H : Subgroup G),
    Nat.card H | Nat.card G

theorem DF_3_2_16' (h : DF_3_2_16_Lagrange) {p : N} (hp : p.Prime) (a : Z) :
    a ^ p ≡ a [ZMOD p] := by
  sorry

The intended solution is to apply Lagrange’s theorem to the multiplicative group (Z/pZ)× and the
subgroup generated by a (and consider the a ≡ 0 (mod p) case separately), and an AI system may
follow this approach when proving DF_3_2_16'. However, there are also multiple proofs of Fermat’s
little theorem that do not use Lagrange’s theorem, such as proofs using the binomial theorem or a
combinatorial argument. Thus, it is possible to prove DF_3_2_16 without using such a hypothesis; in
fact, this result already exists in Mathlib as Nat.ModEq.pow_card_sub_one_eq_one. We therefore
include both versions of the formalization, one with the Lagrange theorem hypothesis and one without
it.
Another example is Exercise 5 of Chapter 4.4, which asks the reader to prove that the automorphism
group of the dihedral group D4 of order 8 is isomorphic to D4 , using the fact that D4 ⊴ D8 .8 The
intended solution is as follows: if D4 is known to be a normal subgroup of D8 , then D8 acts on
D4 by conjugation, giving a homomorphism D8 → Aut(D4 ). Computing its kernel, which is the
centralizer of D4 in D8 , and its image then gives the desired isomorphism.
However, it is unclear whether the mere existence of an embedding ϕ : D4 → D8 with normal image
is sufficient for the intended formalization, or whether one must give an explicit description of ϕ in
terms of generators. Therefore, we decided to formalize only the version without the hint, as follows:
theorem DF_4_4_5 : Nonempty ((MulAut (DihedralGroup 4)) ≃* (DihedralGroup 4)) := by
  sorry

Exercises with diagrams
   8 Dummit–Foote denote the order-8 dihedral group by D . Here we follow the convention in which D denotes the
                                                        8                                          n
dihedral group of order 2n, rather than D2n ; this also agrees with the convention used in Mathlib.


                                                            15
Some exercises include diagrams, such as subgroup lattices or commutative diagrams. For example,
Exercise 14 of Chapter 2.5 concerns the modular group of order 16, defined by the presentation
M := ⟨u, v | u2 = v 8 = 1, vu = uv 5 ⟩. In particular, it asks the reader to show that the lattice of
subgroups of M is the same as the lattice of subgroups of Z/2Z × Z/8Z. The Subgroup type in
Mathlib is already an instance of CompleteLattice, so this can be formalized as follows:
inductive MGen | u | v deriving DecidableEq, Repr

open FreeGroup in
def M := PresentedGroup {
  (of MGen.u)^2,
  (of MGen.v)^8,
  (of MGen.u) * (of MGen.v)^5 * (of MGen.u)^(-1 : Z) * (of MGen.v)^(-1 : Z)
}

deriving instance Group for M

theorem DF_2_5_14_4 : Nonempty ((Subgroup M) ≃o AddSubgroup ((ZMod 2) × (ZMod 8))) := by
  sorry

Here ≃o denotes OrderIso, an order-preserving isomorphism.
A similar but more complicated example is Exercise 11 of the same chapter, which concerns the
subgroup lattice of the quasidihedral group of order 16,
                           G = QD = ⟨σ, τ | σ 8 = τ 2 = 1, στ = τ σ 3 ⟩.
The exercise provides a subgroup lattice diagram with six missing vertices, shown in Figure 2,
and asks the reader to identify suitable subgroups A0 , A1 , . . . , A5 , each generated by at most two
elements.
                                                                  G




                                G0 = ⟨σ 2 , τ ⟩               G1 = ⟨σ⟩        G2 = ⟨σ 2 , τ σ⟩




                A0              H0 = ⟨σ 4 , τ ⟩                   A1                A2              A3




H1 = ⟨τ σ 2 ⟩         A4             A5           H2 = ⟨τ ⟩   H3 = ⟨σ 4 ⟩




                                                                  1
                      Figure 2: Subgroup lattice for Exercise 11, Chapter 2.5


As with other problems that ask for explicit answers, we define DF_2_5_11_ans using sorrys. These
answers have type Set QD, and DF_2_5_11_groups is defined to be the corresponding collection of
subgroups of QD generated by the sets in DF_2_5_11_ans. In other words, a solution must provide
generating sets for the missing groups A0 , . . . , A5 . A complete formalization is given below:
inductive QDGen | σ | τ deriving DecidableEq, Repr

open FreeGroup in
def QD := PresentedGroup {
  (of QDGen.σ)^8,
  (of QDGen.τ )^2,
  (of QDGen.σ) * (of QDGen.τ ) * (of QDGen.σ)^(-3 : Z) * (of QDGen.τ )^(-1 : Z)
}


                                                     16
deriving instance Group for QD


abbrev QD.of (x : QDGen) : QD := PresentedGroup.of x

abbrev σ : QD := PresentedGroup.of QDGen.σ
abbrev τ : QD := PresentedGroup.of QDGen.τ

def DF_2_5_11_ans : Fin 6 → Set QD
  | 0 => sorry
  | 1 => sorry
  | 2 => sorry
  | 3 => sorry
  | 4 => sorry
  | 5 => sorry

def DF_2_5_11_groups : Fin 6 → Subgroup QD := fun i 7→ Subgroup.closure (DF_2_5_11_ans i)

def G0 := Subgroup.closure {σ ^ 2, τ }

def G1 := Subgroup.closure {σ}

def G2 := Subgroup.closure {σ ^ 2, τ * σ}

def H0 := Subgroup.closure {σ ^ 4, τ }

def H1 := Subgroup.closure {τ * σ ^ 2}

def H2 := Subgroup.closure {τ }

def H3 := Subgroup.closure {σ ^ 4}

theorem DF_2_5_11_1 : ∀ i : Fin 6, Finite (DF_2_5_11_ans i) ∧ (DF_2_5_11_ans i).ncard ≤ 2 := by
  sorry

theorem DF_2_5_11_2 :
    DF_2_5_11_groups 0 < G0 ∧
    H1 < DF_2_5_11_groups 0 ∧
    H3 < DF_2_5_11_groups 0 ∧
    DF_2_5_11_groups 1 < G0 ∧
    DF_2_5_11_groups 1 < G1 ∧
    DF_2_5_11_groups 1 < G2 ∧
    H3 < DF_2_5_11_groups 1 ∧
    DF_2_5_11_groups 2 < G2 ∧
    H3 < DF_2_5_11_groups 2 ∧
    DF_2_5_11_groups 3 < G2 ∧
    H3 < DF_2_5_11_groups 3 ∧
    DF_2_5_11_groups 2 ̸= DF_2_5_11_groups 3 ∧
    DF_2_5_11_groups 4 < DF_2_5_11_groups 0 ∧
    ⊥ < DF_2_5_11_groups 4 ∧
    DF_2_5_11_groups 5 < H0 ∧
    ⊥ < DF_2_5_11_groups 5 := by
  sorry



The theorem DF_2_5_11_1 asserts that the proposed generating sets have at most two generators,
while DF_2_5_11_2 asserts the inclusion relations among the subgroups described in Figure 2. Since
A2 and A3 are both subgroups of G2 and both contain H3 , we also require a proof that the two
proposed subgroups are distinct, namely DF_2_5_11_groups 2 ̸= DF_2_5_11_groups 3.
Exercises beyond current autoformalization
Some exercises lie outside what current autoformalization systems can handle. Despite running
a wide range of systems, from frontier single-shot models to recent open-weight models and a
compiler-grounded agent loop (Section 4.1), producing a usable Lean file without human curation
remained out of reach for a non-trivial fraction of exercises, and the difficulty grows quickly as the


                                                 17
Table 6: Per-run wall-clock time and Ollama-reported token counts for the four open-weight single-
shot runs in Section 4.1. All runs use Q4_K_M quantization except Goedel-Formalizer-V2, which is
only available at Q8_0 from its public Ollama upload.

 Run                                         GPU           Wall-clock     Prompt / Output tokens (M)
 Gemma4-31B (think)                     H200 NVL                43.9 h                     0.67 / 7.56
 Goedel-Formalizer-V2-32B               H200 NVL                10.3 h                     0.65 / 1.83
 Qwen3.6-35B-A3B                      H100/H200 NVL             64.4 h                    0.67 / 17.54
 DeepSeek-R1-Distill-Qwen-32B           H200 NVL                46.6 h                     0.64 / 5.26
 Subtotal                                                      165.2 h                    2.63 / 32.19


underlying mathematics becomes more advanced. Exercise 2 of Chapter 16.2 illustrates that even
short, self-contained statements can fall into this category:

 Suppose R is a discrete valuation ring with unique maximal ideal M and quotient F = R/M .
 For any n ≥ 0, show that M n /M n+1 is a vector space over F and that dimF (M n /M n+1 ) = 1.

The exercise does not require any answer to be supplied, and every ingredient needed for its for-
malization (discrete valuation rings, the residue field, and the quotient M n /M n+1 as an F -module)
is already available in Mathlib. Nevertheless, all of our single-shot models failed to elaborate on
this exercise. Codex did produce a file that elaborates, but the resulting statement encoded neither
the defining property of a discrete valuation ring nor the correct quantifier structure of the informal
problem, so the formalization does not match the original.
This points to a more general limitation: when an autoformalizer does not understand the mathematics
behind a statement, it tends to copy the words rather than produce a faithful formalization, even when
the problem looks routine and the needed ingredients are already in Mathlib. We expect this gap to
persist, if not widen, as topics become more advanced. Human curation is therefore essential, not
an optional safety net: without it, even a model that elaborates well can silently produce a wrong
statement on an exercise that looks easy at first glance. Our manual formalization is as follows:
theorem DF_16_2_2'
    {R : Type*} [CommRing R] [IsDomain R] [IsDiscreteValuationRing R] (n : N) :
    let M := IsLocalRing.maximalIdeal R
    let F := IsLocalRing.ResidueField R
    let V := (M ^ n : Ideal R) / (Submodule.comap (M^n).subtype (M^(n+1)))
    ∃ _ : Module F V, Module.finrank F V = 1 := by
  sorry


A.5    Compute resources

All open-weight autoformalization runs were performed on a single NVIDIA H100 NVL (96 GB)
or H200 NVL (144 GB) GPU on an internal academic HPC cluster; no multi-GPU or distributed
inference was used. Models were served through Ollama with each model’s default sampling
parameters, and we performed no training, fine-tuning, or weight modification. Lean elaboration of
the generated files was performed post-hoc on a CPU host using leanprover/lean4:v4.29.1 and
the Mathlib revision 5e932f9, and is not GPU-bound.
The closed-source GPT-5, Codex (agent loop with GPT-5 backbone), and Claude Opus 4.7 (LLM
judge, Section 4.2) were accessed through provider APIs; their compute is provider-side and is not
included in the cluster totals above. Exploratory open-weight runs that did not appear in our final
comparison consumed approximately 80 additional GPU-hours on the same hardware.




                                                  18
