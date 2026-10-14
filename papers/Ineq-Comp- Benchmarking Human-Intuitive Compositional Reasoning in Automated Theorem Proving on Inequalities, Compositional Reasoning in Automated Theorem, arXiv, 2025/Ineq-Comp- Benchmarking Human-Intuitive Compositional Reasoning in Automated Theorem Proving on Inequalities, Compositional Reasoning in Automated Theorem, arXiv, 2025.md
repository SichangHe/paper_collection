                                                  Ineq-Comp: Benchmarking Human-Intuitive
                                                 Compositional Reasoning in Automated Theorem
                                                            Proving on Inequalities


                                             Haoyu Zhao∗ †     Yihan Geng‡      Shange Tang†      Yong Lin†     Bohan Lyu§     Hongzhou Lin¶
arXiv:2505.12680v2 [cs.AI] 20 Oct 2025




                                                                   Chi Jin∗ †                           Sanjeev Arora∗ †



                                                                                        Abstract

                                                    LLM-based formal proof assistants (e.g., in Lean) hold great promise for automat-
                                                    ing mathematical discovery. But beyond syntactic correctness, do these systems
                                                    truly understand mathematical structure as humans do? We investigate this ques-
                                                    tion in context of mathematical inequalities—specifically the prover’s ability to
                                                    recognize that the given problem simplifies by applying a known inequality such
                                                    as AM/GM. Specifically, we are interested in their ability to do this in a composi-
                                                    tional setting where multiple inequalities must be applied as part of a solution. We
                                                    introduce Ineq-Comp, a benchmark built from elementary inequalities through
                                                    systematic transformations, including variable duplication, algebraic rewriting,
                                                    and multi-step composition. Although these problems remain easy for humans,
                                                    we find that most provers—including Goedel, STP, and Kimina-7B—struggle sig-
                                                    nificantly. DeepSeek-Prover-V2-7B shows relative robustness, but still suffers a
                                                    20% performance drop (pass@32). Even for DeepSeek-Prover-V2-671B model,
                                                    the gap between compositional variants and seed problems exists, implying that
                                                    simply scaling up the model size alone does not fully solve the compositional
                                                    weakness. Strikingly, performance remains poor for all models even when for-
                                                    mal proofs of the constituent parts are provided in context, revealing that the
                                                    source of weakness is indeed in compositional reasoning. Our results expose
                                                    a persisting gap between the generalization behavior of current AI provers and
                                                    human mathematical intuition. All data and evaluation code can be found at
                                                    https://github.com/haoyuzhao123/LeanIneqComp.


                                         1       Introduction
                                         Large language models (LLMs), like O3-mini (OpenAI, 2024) and Deepseek-R1 (Guo et al., 2025),
                                         have made huge progress in reasoning tasks. These models show outstanding performance in
                                         solving math problems, especially in natural language. However, reasoning using natural language
                                         is inherently unreliable for proofs, as subtle errors often arise in complex math derivations (Petrov
                                         et al., 2025). This shortcoming leads to increasing interest in applying LLMs to generate formal math
                                         proofs, where systems like Lean (De Moura et al., 2015; Moura and Ullrich, 2021), Isabelle (Paulson,
                                         1994), and Coq (Barras et al., 1997), provide a framework for expressing and verifying proofs.
                                             ∗
                                               Corresponding to: {haoyu,chij,arora}@princeton.edu
                                             †
                                               Princeton Language and Intelligence, Princeton University.
                                             ‡
                                               Peking University.
                                             §
                                               Tsinghua University
                                             ¶
                                               Amazon. This work is independent of and outside of the work at Amazon.


                                         39th Conference on Neural Information Processing Systems (NeurIPS 2025) Track on Datasets and Benchmarks.
Figure 1: Left: Starting from a seed problem, we apply transformations that are intuitive to humans.
Type I data are generated by duplicating the original inequality using distinct variable names and
multiplying the two resulting inequalities. Type II data are created via algebraic manipulations. These
transformed problems are trivial to solve if one has already understood the seed problem, and we
would expect minimal performance drop between solving the seed problem and its transformed
variations. Mid: Pass@32 accuracy of various models on the original seed problems and their
transformed counterparts (Type I and Type II). All models, except DeepSeek-Prover-V2, exhibit
substantial performance degradation on the transformed problems. Notably, even DeepSeek-Prover-
V2-7B experiences a drop of over 20%. Right: Average success rate (Pass@1 within 3200 attempts)
on the subset of problems each model is able to solve. While seed problems have relatively high solve
rates across models, the transformed variants become significantly more challenging. For example,
even for the strongest model—DeepSeek-Prover-V2-7B— its success rate drops from 50% on seed
problems to 25% on their transformed counterparts. The drop suggests that current provers are
sensitive to surface form rather than the underlying semantic equivalence of mathematical reasoning.


Parallel to progress in natural language reasoning, formal theorem proving with LLMs has developed
rapidly in the past years. In particular, AlphaProof6 , AlphaGeometry (Trinh et al., 2024), and
Seed-Prover (Chen et al., 2025) showed that a model could achieve silver-medal performance in the
International Math Olympiad by finding verifiable proofs. Open-source research efforts also show
significant progress through both whole-proof generation and tree-search approaches (Xin et al.,
2024; Lin et al., 2025a; Dong and Ma, 2025; Wu et al., 2024; Li et al., 2024; Xin et al., 2025; Wang
et al., 2025; Lin et al., 2025b), marking rapid advancements in formal theorem proving.
Despite rapid progress, evaluating a model’s ability to generate formal proofs remains challenging
due to lack of good benchmarks that can measure capabilities smoothly and comprehensively. The
popular MiniF2F (Zheng et al., 2021) is small and yet its problems span a wide difficulty range from
elementary to IMO level. ProofNet (Azerbayev et al., 2023) and PutnamBench (Tsoukalas et al.,
2024) focus on difficult problems where current open models can only succeed on a few examples.
Furthermore, both benchmarks are susceptible to data contamination.
We propose a new evaluation perspective: testing robustness to simple, human-intuitive transforma-
tions through compositions. We apply minor manipulations, like variable duplication or algebraic
rewrites, to existing inequalities. These compositional variants are trivial for humans and even LLMs
using natural language, yet they cause large performance drops in formal settings. This exposes
brittleness in model reasoning that current benchmarks overlook.
The core of this failure is the lack of compositional reasoning. Complex arguments emerge by linking
simpler, well-understood steps — echoing Newton’s notion of “standing on the shoulders of giants” —
which is an important skill in math reasoning. Following this insight, our benchmark leverages simple
transformations that can be composed to create multi-step problems with hierarchical structures. This
offers a natural and controllable axis for evaluating reasoning ability. Moreover, by systematically
varying the depth and abstraction of these compositions, we can generate problem sequences with
progressively increasing difficulty, allowing for more fine-grained and interpretable assessments than
current benchmarks.

   6
       https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/



                                                      2
Existing benchmarks do not explicitly test this “higher” understanding of compositional structure and
their difficulty is often uneven or opaque (Zheng et al., 2021; Azerbayev et al., 2023; Tsoukalas et al.,
2024; Wei et al.; Ren et al., 2025; Liu et al., 2025; Yu et al., 2025). Recent efforts like Yousefzadeh
et al. (2025), which annotate IMO proofs with intermediate lemmas, follow a top-down approach
that is hard to scale and may introduce subjective biases about valid solution paths. In contrast,
our bottom-up construction composes seed problems into more complex ones through controllable
transformations, enabling scalable and interpretable evaluation of formal reasoning.
Combining the above ideas, we introduce our new benchmark, Ineq-Comp, which is designed
to assess the compositional reasoning abilities of formal theorem provers in algebraic inequalities.
Using a bottom-up approach, we start from seed problems formalized in Lean 4, each solvable
via standard inequalities such as AM-GM or Cauchy, and systematically apply simple, controlled
transformations to generate more complex variants. These modifications are minimal and preserve
human accessibility; in fact, general-purpose LLMs like OpenAI O3 solve them easily in informal
natural language. Given that existing provers perform well on nontrivial problems in benchmarks like
MiniF2F (Zheng et al., 2021) and ProofNet (Azerbayev et al., 2023), we expected them to generalize
to these variants. Surprisingly, we found that most provers consistently fail to reason through
these human intuitive transformations, exposing a fundamental weakness in their understanding of
basic compositional generalization, which current benchmarks do not test for. (See Figure 1 for an
example.) We summarize our contributions and key findings below:
1. We develop Ineq-Comp, a benchmark with 75 seed problems solved using basic tools such
   as AM-GM, Cauchy, and Jensen inequalities and accompanied by a verified Lean 4 proof, and
   150 variants generated through compositional transformations (Figure 1 Left and Section 2.1).
   Ineq-Comp is designed to be fully extensible: further composed inequalities can be automatically
   generated using rule-based transformations on any seed set (Section 2.2). We also include 50
   real-world inequality problems to enhance diversity (Section 2.3).
2. We benchmark a range of LLM-based provers—from general-purpose models like R1-Distill-
   Qwen to tree-search-based systems—on Ineq-Comp. All models, except DeepSeek-Prover-V2-
   7B (Ren et al., 2025), suffer from significant performance drops even on the simplest transforma-
   tions (Section 3). Notably, DeepSeek-Prover-V2-7B also shows over 20% drop when tested under
   a limited computational budget (pass@32). These failures persist even when the model is scaled
   up (Section 4.1) or provided with the formal proof of the seed problem in-context (Section 4.2).
3. Through detailed output analysis, we identify two key limitations: (1) models rarely attempt to
   apply core inequalities such as AM-GM or Cauchy within their formal proofs, even when they
   refer to these techniques in natural language comments; and (2) most models rely heavily on a
   narrow set of tactics—particularly the sum-of-squares approach using nlinarith—indicating
   limited diversity in their proof strategies when it comes to inequalities (Section 3).
4. We find that simple fine-tuning on synthetic compositional problems fails to generalize.** While
   performance improves on problems similar to the training data, the skill does not transfer to new
   seed problems, suggesting that data augmentation alone is insufficient to teach robust composi-
   tional reasoning.

2   Dataset Curation
We introduce Ineq-Comp, a benchmark designed to evaluate the compositional reasoning ability of
formal theorem provers in the context of mathematical inequalities. The benchmark is built upon
a curated set of seed problems—introductory-level inequality problems solvable using standard
techniques such as AM-GM, Cauchy-Schwarz, or Jensen’s inequality. Each seed problem is formally
proven in Lean 4, ensuring correctness and providing high-quality human-written proofs. From these
seed problems, Ineq-Comp is extended into three components:
1. Ineq-Simp (Section 2.1): 150 problems created by applying human-intuitive transformations to
   the 75 seed problems. These include algebraic rewrites and compositional constructions (e.g.,
   duplicating variables or multiplying inequalities), as illustrated in Figure 1 (Left). Problems are
   categorized by the technique used in the seed (AM-GM, Cauchy, or Miscellaneous).
2. Ineq-Mix (Section 2.2): A rule-based, automated framework that generates new composed
   inequalities from any given seed set. This enables scalable extension of Ineq-Simp while
   preserving formal correctness.


                                                   3
3. Ineq-Real (Section 2.3): A set of 50 real-world inequality problems collected from math contests
   and educational resources to enhance benchmark diversity and assess generalization beyond
   synthetic construction.

2.1   Ineq-Simp: Simple transformations from seed inequalities
Seed problems We curate 75 seed problems based on direct applications of classical inequalities
commonly used in math Olympiads. These include 25 problems using the AM-GM inequality, 25
using Cauchy–Schwarz, and 25 others covering Jensen’s inequality (10), Schur’s inequality (5), the
sum-of-squares method (5), and induction (5). We emphasize AM-GM and Cauchy due to their
foundational role in inequality reasoning. Each problem is accompanied by a verified Lean 4 proof,
contributing to formal proof resources and ensuring correctness.

Type I variant We generate the type I variant from the seed problem by duplicating the original
inequality using distinct variable names and combine the two resulting inequalities. More precisely,
given a seed inequality defined on variables X = (x1 , . . . , xn ), with condition X ∈ C and statement
f (X) ≥ g(X). We replicate the problem with new variables Y = (y1 , . . . , yn ) under identical
conditions, yielding a second inequality: f (Y ) ≥ g(Y ), and we combine the two as follows: (1)
If g(X) ≥ 0, then we multiply two of them together, resulting in a new problem with variables
(X, Y ), with condition (X, Y ) ∈ C × C and statement f (X) · f (Y ) ≥ g(X) · g(Y ); (2) If g(X) is not
guaranteed to be non-negative, we add the inequalities: f (X)+f (Y ) ≥ g(X)+g(Y ). These variants
remain structurally identical to seed problems, and humans typically solve them by decomposing into
two identical parts. Thus, Type I serves as a minimal test of compositional reasoning: we expect any
model that can solve the seed problem to solve the variant with minimal additional reasoning.

Type II variant Type II problems apply a one-step algebraic transformation to the variables of the
seed problem. For example, each variable may be squared or square-rooted. Mathematically, given
any inequality problem defined on variables X = (x1 , . . . , xn ), with condition X ∈ C and statement
f (X) ≥ g(X), we define a transformation T : Rn → Rn , and we would like to show that with the
condition T (X) ∈ C, f (T (X)) ≥ g(T (X)). Type II problems test “low-level” compositionality.
These problems retain the structure of the seed, differing only by small and systematic substitutions,
and are typically easy for humans once the transformation is recognized.

Quality control All seed problems and Lean 4 proofs are curated by individuals with national or
international math Olympiad experience. The problems are drawn from fundamental techniques such
as AM-GM, Cauchy–Schwarz, Jensen, and Schur, and are kept at or below introductory Olympiad
difficulty. Many can be solved by a single application of a well-known inequality, making them
accessible to LLMs’ capability of informal mathematical reasoning.

2.2   Ineq-Mix: A fully expandable benchmark for composition
We introduce Ineq-Mix, an automated framework that generates a potentially unbounded set of valid
inequality problems by applying predefined transformation rules to seed problems. These rules fall
into three categories: (1) Compositional transformations (e.g., combining inequalities via addition,
multiplication, max/min); (2) Variable-level transformations (e.g., replacing variables with algebraic
expressions); (3) Problem-level transformations (e.g., applying a monotonic function like exp or
log to both sides). All generated problems are guaranteed to be mathematically valid and formally
solvable. Unlike the simpler variants in Section 2.1, Ineq-Mix produces more complex compositions
that often require nontrivial decomposition and planning. For example, proving f1 f2 ≥ g1 g2 from
f1 ≥ g1 and f2 ≥ g2 may require identifying intermediate inequalities. We generate 100 evaluation
problems using only compositional rules (Table 4), which already challenge state-of-the-art provers.
As models improve, Ineq-Mix can scale in complexity by combining multiple transformation types.
To assess whether this difficulty is inherent to formal reasoning, we test OpenAI’s O3 model,
which operates in natural language, on problems involving one transformation from each category.
O3 reliably decomposes and solves these using intuitive reasoning, with failures typically due to
mistakes on individual subproblems. This contrast highlights a key gap: informal models like
O3 handle compositionality with ease, while formal provers struggle even on problems built from
elementary components. This suggests the bottleneck lies in current formal reasoning systems, not
the mathematical content. See Section B for a full list of transformations used in Ineq-Mix.

                                                  4
2.3   Ineq-Real: real-world inequalities
The Ineq-Real subset includes 50 inequality problems sourced from real-world materials, such
as math competitions, training materials, and Chinese Gaokao exams. Each problem is manually
translated into Lean 4 and verified by individuals with IMO/CMO-level expertise.
Although the core techniques—such as AM-GM, Cauchy-Schwarz, and Schur—overlap with those
in Ineq-AMGM, Ineq-Cauchy, and Ineq-MISC, the Ineq-Real problems are generally more
complex. They often require combining multiple techniques, deeper insight, or nontrivial algebraic
manipulation, rather than straightforward application of a single inequality. Unlike the modular
problems in earlier subsets, Ineq-Real tests the application of known tools in real-world contexts
and naturally complements the synthetic, semi-structured problems in Ineq-Comp.

3     Experiments and Findings

3.1   Experiment setup

Models and methods. We evaluate three categories of models and methods: (1) General-purpose
language models, (2) Whole-proof generation models, and (3) Tree-search methods. For general-
purpose models, we test DeepSeek-R1-Distill-Qwen-32B (Guo et al., 2025) in two settings: with
and without explicit thinking steps. Without the chat-style prompt, the model directly completes the
Lean 4 proof code. In contrast, when provided with a chat template and generation prompt, the model
first performs a “thinking process” in natural language before outputting the full Lean script. For
whole-proof generation, we include DeepSeek-Prover-V1.5-RL (Xin et al., 2024), Goedel-Prover-
SFT (Lin et al., 2025a), STP (Dong and Ma, 2025), Kimina-7B (Wang et al., 2025), and the latest
state-of-the-art model DeepSeek-Prover-V2-7B (Ren et al., 2025), which achieves top performance
on the MiniF2F benchmark. For tree-search-based approaches, we evaluate DeepSeek-Prover-V1.5-
RL+RMaxTS (Xin et al., 2024) and InternLM-2.5-Step-Prover+BF (Wu et al., 2024). While recent
models such as HunyuanProver (Li et al., 2024) and BFS-Prover (Xin et al., 2025) show stronger
performance on MiniF2F, we exclude them due to the lack of publicly available code.

Budget and evaluation metric. We evaluate all methods using the standard pass@N accuracy,
where a problem is considered solved if at least one of N generated proofs is correct. For tree-search
methods, budget denotes the total number of interactions with the Lean compiler. For additional
details, see Section D, and refer to Section E for the prompt templates used in evaluation.

3.2   Main findings and discussion

The experiment results on Ineq-Simp: categorized by the natural of seed problems Ineq-AMGM,
Ineq-Cauchy, and Ineq-MISC are summarized in Table 1. The performance of different models on
Ineq-Mix (randomly generated) and Ineq-Real is shown in Figure 2.

Lack of compositional ability. Our experiments reveal a clear failure of compositional generaliza-
tion across most current theorem provers, even on problems derived from simple seed inequalities
that remain easy for humans. As shown in Table 1, top models such as Goedel-Prover-SFT (Lin
et al., 2025a), STP (Dong and Ma, 2025), and Kimina-Prover (Wang et al., 2025) show large drops in
accuracy from seed problems to their compositional variants: Type I (duplication-based) and Type II
(algebraic transformation).
For instance, Kimina-Prover-Preview-Distill-7B achieves 80% on AM-GM seed problems (budget
3200), but drops to 44% on Type I and 64% on Type II. The drop is even more dramatic for Goedel-
Prover and DeepSeek-Prover-V1.5, which struggle to exceed 5% accuracy on Ineq-AMGM Type I
problems—even with a large number of attempts. The only partial exception is DeepSeek-Prover-V2-
7B, which reduces the seed-to-Type I gap to 13% and seed-to-Type II to 18%. Its drop becomes more
pronounced at smaller budgets (e.g., pass@32), confirming that the challenge is not just probabilistic
but fundamentally hard (Figure 1, right). This is especially striking given that DeepSeek-Prover-V2
is explicitly trained using a divide-and-conquer strategy (Ren et al., 2025), which should, in principle,
help with decomposing Type I problems. Its performance gap, particularly under low-pass settings,
highlights the intrinsic difficulty of compositional reasoning in formal reasoning.


                                                   5
Table 1: Performance of different models and methods on Ineq-Simp (Ineq-AMGM, Ineq-Cauchy,
and Ineq-MISC). We report the pass@N accuracy and its standard deviation (subscript text).
                                                            Ineq-AMGM                           Ineq-Cauchy                      Ineq-MISC
              Method                   Budget
                                                  Seed        Type I        Type II   Seed        Type I    Type II    Seed       Type I     Type II
 General Purpose Models
                                         32       48.21.9     3.53.3        16.23.0   28.03.3     17.03.2   15.03.0    41.43.7    13.44.5    15.44.4
 DeepSeek-R1-Distill-Qwen-32B            64       49.01.7     6.54.1        18.42.4   30.63.2     19.52.8   16.82.7    44.53.2    17.74.0    20.24.8
 (w/o thinking)(Guo et al., 2025)        128      49.92.0     10.64.2       20.02.5   32.62.9     21.83.2   19.02.6    47.43.1    21.13.7    25.44.2
                                        3200       52.0        40.0          36.0      44.0        32.0      28.0       52.0       36.0       36.0
                                         32       48.81.6     10.93.8       21.13.1   42.92.5     27.03.4   18.42.4    50.52.3    18.94.6    22.04.0
 DeepSeek-R1-Distill-Qwen-32B            64       49.51.9     14.54.4       23.03.4   44.52.4     30.32.9   20.62.3    51.90.6    23.74.9    26.23.1
  (w thinking)(Guo et al., 2025)         128      50.92.1     19.24.1       26.14.3   46.22.3     32.62.7   22.12.0    52.00.0    28.03.9    29.42.7
                                        3200       60.0        44.0          44.0      56.0        40.0      24.0       52.0       36.0       40.0
 Whole-Proof Generation Methods
                                         32       48.13.0     0.00.4        8.21.5    14.93.2      2.91.8     4.41.4   40.22.8    12.41.1    12.22.5
   DeepSeek-Prover-V1.5-RL               64       50.62.9     0.10.6        9.01.7    17.02.7      3.71.1     5.01.9   42.12.3    12.71.7    13.82.9
       (Xin et al., 2024)                128      52.22.1     0.20.8        9.82.0    18.72.7      4.00.0     6.12.3   43.21.6    13.32.2    16.22.9
                                        3200       60.0        4.0          24.0       24.0         4.0       12.0      44.0       20.0       28.0
                                         32       48.62.9     0.41.2        14.03.2   34.82.5     12.43.5   21.53.4    47.01.7    14.43.1    24.61.9
       Goedel-Prover-SFT                 64       50.62.6     0.81.6        16.62.8   36.21.9     15.83.4   24.62.9    47.80.9    16.62.5    25.51.9
       (Lin et al., 2025a)               128      52.21.4     1.31.9        18.62.2   37.11.8     19.42.9   26.91.8    48.00.0    17.92.6    26.42.5
                                        3200       60.0        4.0           24.0      40.0        32.0      28.0       48.0       24.0       36.0
                                         32       59.11.9     14.34.4       23.24.5   35.22.4     14.62.7   16.02.6    55.61.3    12.65.0    27.63.6
    STP (w/o miniF2F valid)              64       60.10.6     18.54.1       28.24.6   36.82.4     16.72.8   17.32.7    56.00.0    17.84.9    31.04.1
     (Dong and Ma, 2025)                 128      60.31.1     24.34.1       33.03.6   37.92.6     18.43.0   18.93.3    56.00.0    24.04.4    33.94.1
                                        3200       64.0        44.0          40.0      44.0        24.0      28.0       56.0       36.0       40.0
                                         32       59.44.1     11.75.4       45.23.7   46.94.5     27.02.6   27.73.3    44.21.3    18.13.9    35.82.0
   Kimina-Prover-Preview-Distill-7B      64       64.14.6     19.45.9       48.62.4   52.74.3     28.82.5   30.22.8    44.61.4    22.32.9    36.82.0
       (Wang et al., 2025)               128      69.44.2     28.25.4       50.62.2   57.63.6     30.43.0   32.01.6    45.11.8    25.62.5    37.62.5
                                        3200       80.0        44.0          64.0      68.0        52.0      36.0       52.0       32.0       44.0
                                         32       75.04.4     58.64.0       52.54.5   64.64.1     33.02.3   35.02.3    59.12.9    49.33.4    38.84.4
    DeepSeek-Prover-V2-7B                64       80.75.3     62.14.5       57.44.0   68.33.1     34.72.7   36.62.3    61.72.5    51.62.9    43.74.2
       (Ren et al., 2025)                128      85.85.4     65.95.3       61.43.7   71.02.0     36.33.6   37.92.6    64.01.6    53.33.1    49.94.3
                                        3200       96.0        84.0          76.0      76.0        52.0      48.0       68.0       64.0       64.0
 Tree Search Methods
                                       1×3200     60.00.0     3.01.7        22.02.0   24.00.0      8.02.8   13.03.3    44.00.0    14.03.5    29.01.7
   DeepSeek-Prover-V1.5-RL
                                       2×3200     60.00.0     6.02.0        26.02.0   24.00.0     10.02.0   16.00.0    44.00.0    16.04.0    32.00.0
   +RMaxTS(Xin et al., 2024)
                                       4×3200      60.0        8.0           28.0      24.0        12.0      20.0       44.0       20.0       36.0
                                      1×32×600    30.83.1     0.00.0        2.53.1    12.00.0      0.00.0     1.21.9   34.02.0     2.22.0    17.03.9
  InternLM2.5-StepProver+BF
                                      4×32×600    38.04.5     0.00.0        9.03.3    12.00.0      0.00.0     3.01.7   36.00.0     5.01.7    21.01.7
        (Wu et al., 2024)
                                      16×32×600    44.0        0.0          24.0       12.0         0.0        4.0      36.0        8.0       24.0




Besides, tree-search methods can not easily bridge the compositional gap: both DeepSeek-Prover-
V1.5-RL+RMaxTS and InternLM-2.5-StepProver+BF struggle with even the simple Type I and
Type II variants, showing that search alone does not resolve the underlying generalization challenge.
When we evaluate more complex compositions using Ineq-Mix, where two seed problems are
combined using compositional rules, the difficulty increases further (Figure 2, left). Out of 100 such
problems, all whole-proof generation models except DeepSeek-Prover-V2-7B solve fewer than 8,
while DeepSeek-Prover-V2-7B significantly leads with 22 solves under a 128-trial budget.
These results underscore a key limitation of most LLM-based theorem provers: while they can
handle familiar or isolated problems, they fail to generalize reasoning strategies across even modest
compositions. Their inability to reuse known proofs in structured combinations highlights a major
bottleneck in formal mathematical reasoning.

Reliance on sum-of-squares and lack of high-level knowledge. A second key finding is that
LLM-based theorem provers overwhelmingly rely on low-level algebraic tactics and rarely apply
classical inequalities such as AM-GM, Cauchy-Schwarz, or Jensen’s inequality, even when those
are the most appropriate tools. Despite the benchmark being designed to encourage such techniques,
no model except Kimina-Distill-7B apply them directly. Most models default to Lean’s nlinarith
tactic with sq_nonneg, reducing problems to sum-of-squares.
Interestingly, current provers that generate informal reasoning, such as natural language comments
or the thinking drafts, often do produce correct high-level strategies in natural language, frequently
mentioning the appropriate inequality (e.g., AM-GM) or correctly describe how to decompose a


                                                                        6
Figure 2: Pass@N accuracy of various LLM-based theorem provers on the Ineq-Mix (Left) and Ineq-
Real (Right) subsets under increasing computational budgets (x-axis). Surprisingly, the automatically
generated Ineq-Mix problems—created by applying simple, human-intuitive compositional transfor-
mations to pairs of seed inequalities—are more challenging for current models than the real-world
problems in Ineq-Real. Most models, including Goedel-Prover, STP, and Kimina, solve fewer than
7% of Ineq-Mix problems even with 128 attempts, while DeepSeek-Prover-V2 achieves a modest
22%. In contrast, on Ineq-Real, the model performance are at least doubled. This result highlights a
critical weakness in formal theorem provers: reasoning compositionally across structurally simple
subproblems is harder than solving complex, real-world inequalities.

problem into parts. However, many of these strategies are abandoned in the corresponding Lean code,
and models apply brute-force algebraic manipulation instead of high-level knowledge.
This gap underscores a major limitation: while models may recognize the right approach in natural
language, they struggle to implement it in formal proof steps. See Section F for examples.

A different viewpoint from existing benchmarks. Ineq-Comp offers a complementary lens
to existing benchmarks like MiniF2F. While strong models such as DeepSeek-Prover-V2-7B and
Kimina-Distill-7B perform well on both, discrepancies emerge that reveal what each benchmark truly
measures. For example, Goedel-Prover-SFT (Lin et al., 2025a) slightly outperforms STP (without
MiniF2F validation augmentation) (Dong and Ma, 2025) on MiniF2F, but is surpassed by STP on Ineq-
Comp, which targets compositional generalization. Similarly, InternLM2.5-StepProver+BF (Wu
et al., 2024) performs comparably to both on MiniF2F, but struggles significantly on Ineq-Comp,
especially on Type I problems, revealing weak high-level compositional reasoning.
These contrasts highlight Ineq-Comp ’s focus on generalization over structured transformations,
making it a valuable complement to broader benchmarks like MiniF2F.

4     Probing and Mitigating Compositional Challenges
To better understand and potentially mitigate the compositional failures observed in Section 3, we
conduct two ablation studies. First, we explore whether our curated benchmark becomes easier
when models’ sizes are scaled up (Section 4.1), which tests if the compositional failure is unique
to relatively small models and can be easily solved by scaling up. Next, we investigate where our
benchmark becomes easier when models are provided with the formal proof of the seed problem as
part of the input (Section 4.2). This tests whether models can leverage in-context demonstrations to
generalize to the transformed variants. Building on this idea, we then construct synthetic data that
explicitly encodes compositional structure and use it to fine-tune the theorem prover. This examines
whether the lack of compositional ability can be remedied through supervised fine-tuning alone
(Section 4.3).

4.1   Scaling-up model parameters

In Section 3, we mostly test theorem provers with sizes at most 32B, and we do not test provers
with different sizes within the same family. Thus, it is natural to ask if the compositional weakness
pinpointed in Section 3 can be easily solved by scaling up model parameters.
To answer the question, we test DeepSeek-Prover-V2 7B and its 671B counterpart (Ren et al., 2025),
as well as Goedel-Prover-V2 8B and its 32B counterpart (Lin et al., 2025b), under pass@32 on


                                                 7
       Table 2: Performance of models with different sizes on Ineq-Comp under pass@32.
                        Model                                                Seed       Type I        Type II
                        DeepSeek-Prover-V2-7B (Ren et al., 2025)             66.23       46.97          42.1
                        DeepSeek-Prover-V2-671B                               88.0       68.33          70.67
                        Goedel-Prover-V2-8B (Lin et al., 2025b)                69.0        35.0         49.0
                        Goedel-Prover-V2-32B                                   90.0        68.0         83.0



Table 3: ICL-based ablation. Performance of various models on Ineq-Simp (Type I and Type II
variants) under the in-context learning (ICL) setting. For each test instance, the model is provided
with the full formal proof of the corresponding seed problem as part of the input prompt. This setup
evaluates whether models can leverage prior solutions to solve transformed variants via composi-
tional generalization. We report pass@N accuracy (with standard deviation as subscript) across
different generation budgets N . Despite access to a complete solution to the seed problem, all mod-
els—including proprietary ones—continue to struggle on both Type I and Type II variants, indicating
that the compositional gap cannot be easily closed through in-context demonstrations alone.
                                               Budget       Ineq-AMGM                 Ineq-Cauchy               Ineq-MISC
                       Models
                                              (# Proofs)
                                                           Type I    Type II      Type I     Type II       Type I    Type II
           Open-Source Models
                                                 32        11.01.7   28.04.9     34.06.0       9.03.3     39.03.3    44.07.5
            Qwen2.5-Coder-32B-Instruct
                                                 64        22.02.0   34.02.0     40.08.0      14.06.0     46.02.0    52.04.0
                (Hui et al., 2024)
                                                 128        28.0      40.0        48.0         20.0        56.0       60.0
                                                 32         6.04.5   43.03.3     52.04.9      27.04.4     31.03.3    39.05.9
           DeepSeek-R1-Distill-Qwen-32B
                                                 64        10.02.0   50.02.0     68.04.0      32.00.0     48.00.0    46.02.0
           (w/o thinking)(Guo et al., 2025)
                                                 128        16.0      56.0        76.0         44.0        64.0       56.0
                                                 32         8.04.9   39.01.7     64.02.8      28.06.3     35.07.7    45.04.4
           DeepSeek-R1-Distill-Qwen-32B
                                                 64        12.00.0   42.02.0     78.02.0      34.02.0     44.08.0    52.00.0
            (w thinking)(Guo et al., 2025)
                                                 128        16.0      44.0        84.0         40.0        56.0       60.0
           Proprietary Models
                       GPT-4o                    16         12.0      40.0        56.0         16.0        44.0       60.0
           Claude 3.7 Sonnet (w/o thinking)      16         36.0      28.0        32.0         20.0        32.0       24.0



Ineq-Comp. Table 2 summarizes the result, which shows that although scaling up the model size
improves the absolute performance, the relative gap between the Type I, II problems and the seed
problems still exists, implying that the compositional weakness in formal theorem proving is not
easily solvable by brute-force scaling up model parameters.

4.2   In-context learning

To understand whether access to the original proof helps models solve transformed inequality
problems, we conduct an in-context learning (ICL) ablation. For each Type I and Type II problem,
models are provided with the complete, verified Lean 4 proof of the corresponding seed problem in the
prompt. This setup tests whether models can leverage known solutions to generalize compositionally.
Table 3 reports the pass@N accuracy across a range of open-source and proprietary models on
Ineq-AMGM, Ineq-Cauchy, and Ineq-MISC problems under different generation budgets. Despite
having access to the seed solution, all models continue to struggle with the transformed variants. For
example, Qwen2.5-Coder-32B-Instruct achieves only 40.0% accuracy on Type II AM-GM problems
and 20.0% on Type II Cauchy–Schwarz problems at 128 attempts. DeepSeek-R1-Distill-Qwen-32B
(with thinking) performs similarly, reaching just 16.0% on Type I AM-GM problems. Proprietary
models such as GPT-4o and Claude 3.7 Sonnet show mixed results, further illustrating the challenge.
These findings suggest that simply providing the seed proof is not enough to enable compositional
generalization. Even modest transformations remain difficult, pointing to a fundamental limitation in
their ability to transfer and reuse formal reasoning strategies.

4.3   Fine-tuning

Previous studies, such as Zhao et al. (2024); Abedsoltan et al. (2025), have demonstrated that simple
skill composition can be effectively learned through naive fine-tuning, showing generalization even
in out-of-distribution (OOD) scenarios. Motivated by this, we conducted a fine-tuning experiment to


                                                              8
                                                        Seed Ineq. Problems
                                                       𝒫 = 𝒫train ∪ 𝒫held−out


                             (1) Data Generation                                     (3) Evaluation


                     In-context       Generate new problems                Generate new problems using Ineq-Mix,
                      examples           using Ineq-Mix                   or Type I, II Questions for 𝒫held−out

                    Query LLM (Qwen Coder): generate proofs                 Query Fine-tuned LLM: generate proofs
                    for problems given in-context examples.             given the problems (w/o in-context examples)


                           Verified by Lean compiler      (2) Fine-tune          Evaluated by Lean compiler
                                                        (Goedel-Prover-SFT)

                                  Training Data




Figure 3: Pipeline for evaluating if composition can be learned through naive fine-tuning. We split the
seed problems into Ptrain , which contains 25 problems utilizing AMGM, and Pheld-out , which contains
the remaining 50 problems. The pipeline consists of three steps: (1) generate data by prompting LLM
given the proof of seed problems in context and keep only the proofs that pass Lean compilation; (2)
fine-tune Goedel-Prover-SFT; (3) evaluate type I and II problems and Ineq-Mix on Pheld-out .


explore whether our composition and algebraic transformation structures could similarly enhance
model performance in formal inequality proving.
We split the seed problems into two subsets: 25 AM-GM inequality seed problems as training set and
50 other problems as held-out set. To construct training data, we use our automated framework (Ineq-
Mix) to generated 15k problems incorporating both algebraic and compositional transformations base
on the AM-GM seed problems. Then we used in-context learning (ICL) to prompt Qwen2.5-Coder-
32B-Instruct with seed problems and their verified Lean 4 proofs. We retained approximately 8k
compilable outputs and fine-tuned Goedel-Prover-SFT on this data. See Figure 3 for an overview of
the process and Section D for setup details.
Fine-tuning led to substantial in-distribution (ID) improvements, especially on Type I AM-GM
problems, where accuracy rose to 56.0% at a high generation budget. However, gains on out-of-
distribution (OOD) tasks—such as Type II or unseen algebraic transformations—were minimal. Even
with 3200 attempts, performance on these variants remained close to pre-finetuning levels.
These findings suggest that while models can learn to replicate specific compositional structures
from data, their ability to generalize this reasoning to structurally similar but unseen cases remains
limited. This highlights that compositional reasoning in formal proofs may not be easily acquired
through moderate-scale supervised fine-tuning alone. Addressing this challenge likely requires
significantly richer training signals (Ren et al., 2025). Notably, the fine-tuned model retains its
original performance on MiniF2F, confirming that the lack of OOD gains is not due to catastrophic
forgetting, but stems from fundamental limitations in current prover capabilities.


5   Related Works

Automated theorem proving (ATP) ATP has been a long-standing goal in AI (Wu, 2008). Modern
theorem provers use tactic-based proof search and premise selection within these systems (e.g. Lean’s
tactics in Mathlib environment), but they struggle with enormous search spaces and limited training
data for complex theorems (Polu and Sutskever, 2020; Yang et al., 2023). More recently, more
theorem provers came out based on large language models (Xin et al., 2024; Lin et al., 2025a; Dong
and Ma, 2025; Wang et al., 2025; Ren et al., 2025), and also possibly incorporated tree-search
techniques (Wu et al., 2024; Li et al., 2024; Xin et al., 2025).
While achieving better performance on standard benchmarks like MiniF2F, our Ineq-Comp bench-
mark shows that these models struggle with even simple composition. There are also inequality
solvers targeting much harder math Olympiad-level inequalities that best LLMs like GPT-4 cannot
solve (Wei et al.; Li et al., b). These methods are not taken into consideration since our benchmark


                                                                9
Figure 4: SFT base ablation. The performance of the fine-tuned model on different type of problems
in Ineq-AMGM (ID), Ineq-Cauchy (OOD) and Ineq-MISC (OOD). We group different types
of problems in Ineq-Cauchy and Ineq-MISC together as OOD and report the accuracy under
Pass@3200. Although fine-tuning significantly improved in-distribution (ID) Type I performance,
it did not lead to meaningful improvements on out-of-distribution (OOD) generalization tasks or
algebraic transformation problems.

focuses on general theorem provers and shows that they cannot solve the math problems trivial to
human and can be easily solved by LLMs through natural language reasoning.
Datasets and benchmarks for ATP. Formal libraries like Lean’s such as mathlib (Lean) (van
Doorn et al., 2020), the Archive of Formal Proofs (Isabelle), and the Coq Standard Library provide
large collections of high-quality formal proofs. However, these proofs tend to reflect routine rea-
soning with limited diversity in problem structure. Datasets extracted from these libraries, such as
CoqGym (Yang and Deng, 2019) and IsarStep (Li et al., a), provide goal–tactic supervision, but
they fall short in capturing the kind of creative or compositional reasoning in math competitions. To
assess generalization, several curated benchmarks have been proposed. MiniF2F (Zheng et al., 2021)
aggregates problems from math contests ranging from AMC to IMO, spanning a broad difficulty
range but lacking fine-grained structure, often mixing trivial exercises with advanced Olympiad
problems. ProofNet (Azerbayev et al., 2023) focuses on undergraduate-level mathematics, while
PutnamBench (Tsoukalas et al., 2024) targets advanced problems from the Putnam competition,
which remain unsolved by most current models.
AIPS (Wei et al.) and Li et al. (b) introduce (synthetic) datasets for inequality proving, targeting
IMO-level challenges using symbolic–neural methods. These efforts aim to push the boundary of
inequality proving abilities. While these efforts highlight the complexity and elegance of inequality
proving, they primarily aim to push the limits of problem difficulty. In contrast, Ineq-Comp takes
a bottom-up approach: starting from simple, human-solvable inequalities and applying minimal,
structured transformations to test compositional generalization. Rather than measuring raw difficulty,
we isolate a model’s ability to reuse reasoning across structurally varied but logically equivalent
problems. While AIPS probes advanced inequality solving, Ineq-Comp reveals brittleness on easy
problems, exposing a different and underexplored axis of failure.

6   Conclusion
We introduced a benchmark to evaluate compositional generalization in automated theorem proving,
centered on inequality problems. By applying simple, human-intuitive transformations to seed
problems, we revealed significant performance drops across LLM-based provers, highlighting a
core weakness in compositional reasoning. These findings point to an important frontier for formal
reasoning systems: developing models that not only learn individual proof strategies, but can reliably
compose and adapt them in a formally verifiable manner.

Acknowledgement
The authors would like to thank Danqi Chen and Kaiyu Yang for helpful discussions. HZ and SA
acknowledge support from NSF, ONR, and Schmidt Foundation. CJ acknowledge the support from
NSF-OAC-2411299 and NSF-IIS-2239297.


                                                 10
References
Amirhesam Abedsoltan, Huaqing Zhang, Kaiyue Wen, Hongzhou Lin, Jingzhao Zhang, and Mikhail
 Belkin. Task generalization with autoregressive compositional structure: Can learning from d tasks
 generalize to dt tasks? arXiv preprint arXiv:2502.08991, 2025.
Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev, and
  Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics.
  arXiv preprint arXiv:2302.12433, 2023.
Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Jean-Christophe Filliatre, Eduardo
  Gimenez, Hugo Herbelin, Gerard Huet, Cesar Munoz, Chetan Murthy, et al. The Coq proof
  assistant reference manual: Version 6.1. PhD thesis, Inria, 1997.
Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
  Xing Jin, Chenggang Li, Kaijing Ma, et al. Seed-prover: Deep and broad reasoning for automated
  theorem proving. arXiv preprint arXiv:2507.23726, 2025.
Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer. The
  lean theorem prover (system description). In Automated Deduction-CADE-25: 25th International
  Conference on Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceedings 25, pages
  378–388. Springer, 2015.
Kefan Dong and Tengyu Ma. Beyond limited data: Self-play llm theorem provers with iterative
  conjecturing and proving. arXiv preprint arXiv:2502.00212, 2025.
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
  Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
  via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,
  Bowen Yu, Kai Dang, et al. Qwen2. 5-coder technical report. arXiv preprint arXiv:2409.12186,
  2024.
Wenda Li, Lei Yu, Yuhuai Wu, and Lawrence C Paulson. Isarstep: a benchmark for high-level
 mathematical reasoning. In International Conference on Learning Representations, a.
Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang Wang, Tao Yang, and Haitao Mi. Hunyuanprover:
  A scalable data synthesis framework and guided tree search for automated theorem proving. arXiv
  preprint arXiv:2412.20735, 2024.
Zenan Li, Zhaoyu Li, Wen Tang, Xian Zhang, Yuan Yao, Xujie Si, Fan Yang, Kaiyu Yang, and
  Xiaoxing Ma. Proving olympiad inequalities by synergizing llms and symbolic reasoning. In The
  Thirteenth International Conference on Learning Representations, b.
Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou Xia,
  Danqi Chen, Sanjeev Arora, et al. Goedel-prover: A frontier model for open-source automated
  theorem proving. arXiv preprint arXiv:2502.07640, 2025a.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Jiawei Ge, Jingruo Sun, et al. Goedel-prover-v2: Scaling formal theorem proving with scaffolded
  data synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025b.
Junqi Liu, Xiaohan Lin, Jonas Bayer, Yael Dillies, Weijie Jiang, Xiaodan Liang, Roman Soletskyi,
  Haiming Wang, Yunzhou Xie, Beibei Xiong, et al. Combibench: Benchmarking llm capability for
  combinatorial mathematics. arXiv preprint arXiv:2505.03171, 2025.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In
  Automated Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual
  Event, July 12–15, 2021, Proceedings 28, pages 625–635. Springer, 2021.
OpenAI. Introducing o3: Openai’s new reasoning models, 2024. URL https://cdn.openai.com/
  o3-mini-system-card-feb10.pdf. Accessed April 2025.


                                                11
Lawrence C Paulson. Isabelle: A generic theorem prover. Springer, 1994.

Ivo Petrov, Jasper Dekoninck, Lyuben Baltadzhiev, Maria Drencheva, Kristian Minchev, Mislav
  Balunović, Nikola Jovanović, and Martin Vechev. Proof or bluff? evaluating llms on 2025 usa
  math olympiad. arXiv preprint arXiv:2503.21934, 2025.

Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
  arXiv preprint arXiv:2009.03393, 2020.

Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
   Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu,
  Wenjun Gao, Daya Guo, and Chong Ruan. Deepseek-prover-v2: Advancing formal mathematical
   reasoning via reinforcement learning for subgoal decomposition, April 2025.

Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving olympiad geometry
  without human demonstrations. Nature, 625(7995):476–482, 2024.

George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings, Ami-
  tayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers on the
  putnam mathematical competition. arXiv preprint arXiv:2407.11214, 2024.

Floris van Doorn, Gabriel Ebner, and Robert Y Lewis. Maintaining a library of formal mathematics.
  In International Conference on Intelligent Computer Mathematics, pages 251–267. Springer, 2020.

Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
  Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxc’e, Bolton Bailey,
  Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu,
  Jonas Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi Pagani,
  Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut Barroyer, Wen-Ding Li,
 Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin Yang, Zhengying Liu,
  and Jia Li. Kimina-prover preview: Towards large formal reasoning models with reinforcement
  learning. arXiv preprint arXiv:2504.11354, 2025.

Chenrui Wei, Mengzhou Sun, and Wei Wang. Proving olympiad algebraic inequalities without
  human demonstrations. In The Thirty-eight Conference on Neural Information Processing Systems
  Datasets and Benchmarks Track.

Wen-tsün Wu. On the decision problem and the mechanization of theorem-proving in elementary
 geometry. In Selected Works Of Wen-Tsun Wu, pages 117–138. World Scientific, 2008.

Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai Chen.
  Internlm2. 5-stepprover: Advancing automated theorem proving via expert iteration on large-scale
  lean problems. arXiv preprint arXiv:2410.15700, 2024.

Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
  Zhang, Xuan Lu, Qiushi Du, et al. Deepseek-prover-v1. 5: Harnessing proof assistant feedback for
  reinforcement learning and monte-carlo tree search. arXiv preprint arXiv:2408.08152, 2024.

Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Kai
  Shen. Bfs-prover: Scalable best-first tree search for llm-based automatic theorem proving. arXiv
  preprint arXiv:2502.03438, 2025.

Kaiyu Yang and Jia Deng. Learning to prove theorems via interacting with proof assistants. In
  International Conference on Machine Learning, pages 6984–6994. PMLR, 2019.

Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented
  language models. Advances in Neural Information Processing Systems, 36:21573–21612, 2023.

Roozbeh Yousefzadeh, Xuenan Cao, and Azim Ospanov. A lean dataset for international math
  olympiad: Small steps towards writing math proofs for hard problems. Transactions on Machine
  Learning Research, 2025. URL https://openreview.net/forum?id=CrKMqRAhBo.


                                               12
Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
  Zheng Yuan, Huajian Xin, Wenhao Huang, et al. Formalmath: Benchmarking formal mathematical
  reasoning of large language models. arXiv preprint arXiv:2505.02735, 2025.
Haoyu Zhao, Simran Kaur, Dingli Yu, Anirudh Goyal, and Sanjeev Arora. Can models learn
  skill composition from examples? Advances in Neural Information Processing Systems, 37:
 102393–102427, 2024.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.




                                            13
Appendix

A    Limitation
The main limitation of our work is the amount of computational resources required, which prevented
us from conducting an extensive hyperparameter search across all models. For instance, the generation
temperature was fixed at 1.0 under all generation budgets, and the maximum generation length was
set to be 16k. Our experiments cost over 10,000 H100 GPU hours in total. Despite the lack of an
extensive hyperparameter search, the observed performance differences in our results are significantly
larger than standard deviation. We therefore believe that our main conclusions would hold even if
more comprehensive hyperparameter tuning were conducted.

B    More Details on Ineq-Mix
In this section, we present the details of Ineq-Mix, including the technical requirements and all the
transformation rules for different categories.

Seed problems We first focus on the seed problems. Every seed problem takes the following form:
                         Variables:      X = {x1 , . . . , xn } ∈ Rn
               Basic assumptions:        X ≻ 0 (xi > 0, ∀i ∈ [n])
              Further assumptions:       X∈C
                        Statement:       f (x1 , . . . , xn ) ≥ g(x1 , . . . , xn )
                    Positive RHS:        if rhs g(x1 , . . . , xn ) is guaranteed to be positive.
Here, the variables need to be a set with fixed number of variables, i.e., the number of variables need
to be constant. For inequalities with infinite number of variables or with n-variables, they are not
taken into consideration as seed problems. We also assume that all the variables are real numbers.
We also add the assumption for every seed problem that xi > 0 for all i ∈ [n]. This assumption
ensures the correctness for composition and further algebraic transformations.
The seed inequality problem can have further conditions on the variables. For example, for a
3-variable inequality with variables a, b, c, a possible additional assumption is a + b + c = 1.
Finally, we also have a boolean tag to denote if the right-hand side of the statement g(x1 , . . . , xn ) is
guaranteed to be positive, under the assumption that X ≻ 0 and X ∈ C. This tag helps filter out some
composition / algebraic transformation rules to ensure the correctness of the transformed problem.
The following are two examples (famous inequalities) that violate our requirement.
Example 1: Variant of Bernoulli inequality. For any x > 0 and any n ∈ N, we have
                                           (1 + x)n ≥ 1 + nx.
This inequality does not satisfy our requirement since n is an integer taken as an input. If we change
n to a fixed constant, say 10, then it is a valid seed problem.
Example 2: Variant of n-variable Cauchy’s inequality. For any n ∈ N and variables a1 , a2 , . . . , an ,
b1 , b2 , . . . , bn with ai ∈ R+ , bi ∈ R+ , ∀i ∈ [n], we have
                                        n
                                              ! n         !     n
                                                                        !2
                                       X          X             X
                                            2           2
                                          ai           bi ≥       a i bi .
                                   i=1          i=1            i=1

This inequality does not satisfy our requirement since n is an integer taken as input, and the number
of variables is not a fixed contact (it changes with n). If we change n to a fixed constant, say 10, then
it is a valid seed problem.
Among 75 seed problems from Ineq-AMGM, Ineq-Cauchy, and Ineq-MISC, we get 65 seed
problems that satisfies the requirement after small modifications. The discarded problems include
some problems that require induction (thus involving integers) or n-variable Cauchy’s inequality, or
some problems that cannot easily add the required assumption xi > 0 for all i.


                                                      14
Table 4: (A list of composition methods for two inequality problems.) Given two inequality
problems P1 , P2 , where P1 has variables X = {x1 , . . . , xm }, with the statement: given condition
on the variables C1 (X), the following inequality holds f1 (X) ≥ g1 (X), and P2 has variables
X, with the statement: given condition on the variables C2 (X), the following inequality holds
f2 (X) ≥ g2 (X), the following list defines several composition operations to generate a new inequality
problem. If problems P1 and P2 have different set of variables, we can always lift the problems and
make sure they are defined on the same variable space. Following are the composition methods we
considered to combine P1 and P2 together. If g1 (X) and g2 (X) are both greater than 0, there are
more composition methods. We also make sure that C1 (X) ∩ C2 (X) is non-empty after composition.
                 Name                                                                  Statement of the new problem

  Without further condition on g1 (X) and g2 (X).

        Direct Addition                             Given condition C1 (X) and C2 (X), show that f1 (X) + f2 (X) ≥ g1 (X) + g2 (X).
  Weighted Sum (for µ, λ > 0)                   Given condition C1 (X) and C2 (X), show that µf1 (X) + λf2 (X) ≥ µg1 (X) + λg2 (X).
                Maxima                       Given condition C1 (X) and C2 (X), show that max{f1 (X), f2 (X)} ≥ max{g1 (X), g2 (X)}.
                Minima                        Given condition C1 (X) and C2 (X), show that min{f1 (X), f2 (X)} ≥ min{g1 (X), g2 (X)}.

  With further conditions g1 (X) > 0 and g2 (X) > 0.

        Direct Addition                          Given condition C1 (X) and C2 (X), show that f1 (X) + f2 (X) ≥ g1 (X) + g2 (X) > 0.
  Weighted Sum (for µ, λ > 0)                Given condition C1 (X) and C2 (X), show that µf1 (X) + λf2 (X) ≥ µg1 (X) + λg2 (X) > 0.
                Maxima                    Given condition C1 (X) and C2 (X), show that max{f1 (X), f2 (X)} ≥ max{g1 (X), g2 (X)} > 0.
                Minima                     Given condition C1 (X) and C2 (X), show that min{f1 (X), f2 (X)} ≥ min{g1 (X), g2 (X)} > 0.
         Multiplication                           Given condition C1 (X) and C2 (X), show that f1 (X) · f2 (X) ≥ g1 (X) · g2 (X) > 0.
                Division                                      Given condition C1 (X) and C2 (X), show that gf12 (X)
                                                                                                                (X)
                                                                                                                    ≥ gf21 (X)
                                                                                                                           (X)
                                                                                                                               > 0.
                                                                                                  1        1        1        1
              Reciprocal                          Given condition C1 (X) and C2 (X), show that g1 (X) + g2 (X) ≥ f1 (X) + f2 (X) > 0.



Table 5: (A list of algebraic transformation on variables for an inequality problem.) Given
an inequality problem P1 , where P1 has variables X = {x1 , . . . , xm }, with the statement: given
condition on the variables C1 (X), the following inequality holds f1 (X) ≥ g1 (X), the following list
defines several algebraic transformation operations on variables to generate a new inequality problem.
Most of the transformations do not have any requirement as they are one-to-one mappings on R+ .
       Name                                                                      Statement of the new problem

 Any assumption X ∈ C1 .

       shift                                Define Xnew = (x2 , x3 , . . . , xm+1 ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
        rep                            Define Xnew = (xm+1 , xm+2 , . . . , x2m ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
                                                          √          √          √
      sqrt_all                          Define Xnew = ( x1 , x2 , . . . , xm ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
                                                        √
    sqrt_random              Define Xnew = (x1 , . . . , xi , . . . , xm ) with randomly chosen i, given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
       sq_all                                Define Xnew = (x21 , x22 , . . . , x2m ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
    sq_random                 Define Xnew = (x1 , . . . , x2i , . . . , xm ) with randomly chosen i, given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
     cube_all                                Define Xnew = (x31 , x32 , . . . , x3m ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
   cube_random                Define Xnew = (x1 , . . . , x3i , . . . , xm ) with randomly chosen i, given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
   reciprocal_all                            Define Xnew = ( x11 , x12 , . . . , x1m ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
 reciprocal_random           Define Xnew = (x1 , . . . , x1i , . . . , xm ) with randomly chosen i, given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
      exp_all                       Define Xnew = (ex1 − 1, ex2 − 1, . . . , exm − 1), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
    exp_random             Define Xnew = (x1 , . . . , exi − 1, . . . , xm ) with randomly chosen i, given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
      log_all                Define Xnew = (log(1 + x1 ), log(1 + x2 ), . . . , log(1 + xm )), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
    log_random           Define Xnew = (x1 , . . . , log(1 + xi ), . . . , xm ) with randomly chosen i, given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).

 Only contains basic assumption X ≻ 0.

      cyc_add                       Define Xnew = (x1 + x2 , x2 + x3 , . . . , xm + x1 ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
     cyc_mul                             Define Xnew = (x1 x2 , x2 x3 , . . . , xm x1 ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
      cyc_div                                Define Xnew = ( xx12 , xx32 , . . . , xxm
                                                                                     1
                                                                                       ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).
    cyc_div_add                       Define Xnew = ( x1x+x
                                                          1
                                                             , x2 , . . . , xmx+x
                                                            2 x2 +x3
                                                                               m
                                                                                 1
                                                                                   ), given condition C1 (Xnew ), show that f1 (Xnew ) ≥ g1 (Xnew ).




Transformation rules Now we show the details of how to compose two inequality problems
together or add algebraic transformation to create new inequality problems in Ineq-Mix. Recalled


                                                                                   15
Table 6: (A list of algebraic transformation on statement for an inequality problem.) Given
an inequality problem P1 , where P1 has variables X = {x1 , . . . , xm }, with the statement: given
condition on the variables C1 (X), the following inequality holds f1 (X) ≥ g1 (X), the following list
defines several algebraic transformation operations on variables to generate a new inequality problem.
                       Name                      Statement of the new problem

                       Without further condition on g1 (X) and g2 (X).

                        exp     Given condition C1 (X), show that exp (f1 (X)) ≥ exp (g1 (X)).
                       cube        Given condition C1 (X), show that (f1 (X))3 ≥ (g1 (X))3 .

                       With further conditions g1 (X) > 0.
                                                                         p        p
                        sqrt       Given condition C1 (X), show that      f1 (X) ≥ g1 (X).
                        sq         Given condition C1 (X), show that (f1 (X))2 ≥ (g1 (X))2 .
                        log     Given condition C1 (X), show that log (f1 (X)) ≥ log (g1 (X)).



that as mentioned in Section 2.2, Ineq-Mix consists of transformation/composition rules from
three categories: (1) compositional transformations, where (different) inequalities are combined
through operations like addition, multiplication, or taking the maximum or minimum of both sides;
(2) variable-level algebraic transformations, where we replace variables with other algebraic
expressions; and (3) problem-level algebraic transformations, where we apply a monotone function
to both sides of an inequality, such as taking exponentials or logarithms. We now introduce them by
category.
Compositional transformations Composition transformations denote the rules that given two inequal-
ity problems, we compose them together to generate a new inequality, where the two inequality
problems serve as subparts for the new inequality problem. Table 4 shows the full list of composition
rules. Note that the rules are classified into two categories to make sure mathematical correctness: the
rules require the right-hand side to be positive, and the rules without this requirement. Also note that
if the two problems both has positive right-hand side in the statement, then after the compositions
defined in Table 4, the new problem also has a positive right-hand side.
Also, to make sure that the composed inequality problem has a feasible non-empty region (i.e.,
C1 ∩ C2 ̸= ϕ for C1 and C2 being the feasible region of the two inequality problems), we only
compose two inequality problems if:

      1. At least one inequality problem has no further assumptions (only contains the basic assump-
         tions X ≻ 0 (xi > 0, ∀i ∈ [n])
      2. or, the two inequality problems’ variables are disjointed before being lifted to the same
         variable set.

Variable-level algebraic transformations Variable-level algebraic transformations denote the rules
that apply algebraic transformations on the variables of a given inequality problem. For example,
replacing xi in the original inequality problem into x2i , for all xi ∈ X where X = {x1 , . . . , xm }
denotes the variable set. Table 5 summarizes the variable-level algebraic transformations used for
Ineq-Mix. Similar to compositional transformations, there are also two categories for variable-level
algebraic transformations. The first category includes the transformations that are “one-to-one”
mapping under the basic assumption X ≻ 0, like taking the square root of all variables, and squaring
all variables. Since these transformations are one-to-one, as long as the original problem is feasible,
the new problem that applies these rules is also feasible. We also include some transformation rules
that are not one-to-one under the basic assumption X ≻ 0 (but are also elegant transformations).
However to ensure the correctness, these rules can only be applied to problems where there is only
the basic assumption X ≻ 0 and no additional assumptions.
Problem-level algebraic transformations The final set of rules is the problem-level algebraic transfor-
mations, where the general idea is to apply a monotonic function on the statement’s left-hand side
and right-hand side. For example, for an inequality problem with statement
                                     f (x1 , . . . , xn ) ≥ g(x1 , . . . , xn ),


                                                         16
Table 7: List of models tested in Section 3 or Section 4. We use “Kimina-Distill-7B” to denote
“Kimina-Prover-Preview-Distill-7B” in the paper.
                 Name                                   Version or Huggingface Link

    Proprietary Models

                GPT-4o                                      gpt-4o-2024-11-20
            Claude 3.7 Sonnet                           claude-3-7-sonnet-20250219

    Open-Source Models

      Qwen2.5-Coder-32B-Instruct       https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct
    DeepSeek-R1-Distill-Qwen-32B   https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
        DeepSeek-Prover-V1.5-RL      https://huggingface.co/deepseek-ai/DeepSeek-Prover-V1.5-RL
           Goedel-Prover-SFT             https://huggingface.co/Goedel-LM/Goedel-Prover-SFT
         STP (w/o miniF2F valid)            https://huggingface.co/kfdong/STP_model_Lean
            Kimina-Distill-7B      https://huggingface.co/AI-MO/Kimina-Prover-Preview-Distill-7B
         DeepSeek-Prover-V2-7B        https://huggingface.co/deepseek-ai/DeepSeek-Prover-V2-7B
         InternLM2.5-StepProver        https://huggingface.co/internlm/internlm2_5-step-prover



then if h(·) is monotonically increasing on R, then we also know that
                                h(f (x1 , . . . , xn )) ≥ h(g(x1 , . . . , xn )).
If the original inequality problem also has positive right-hand side, then for any h(·) monotonically
increasing on R+ (like h(x) = x2 or h(x) = log x), we also have
                                h(f (x1 , . . . , xn )) ≥ h(g(x1 , . . . , xn )).
Table 6 summarizes all the problem-level algebraic transformations used in Ineq-Mix.

C       Detailed Model Information
The full list of models used in our experiments, including the version (for API models) and
Huggingface-link, is shown in Table 7.

D       Additional Experimental Details and Results
D.1      Lean 4 version

For evaluation on models except InternLM2.5-StepProver, we stick to the Lean 4 and Mathlib version
used in Xin et al. (2024), since Goedel-Prover-SFT (Lin et al., 2025a) and STP (Dong and Ma, 2025)
are trained based on DeepSeek-Prover-V1.5-RL (Xin et al., 2024). Besides, we also nearly recover
the reported performance of Kimina-Distill-7B (Wang et al., 2025) and DeepSeek-Prover-V2 (Ren
et al., 2025) on MiniF2F benchmark using Lean 4 and Mathlib version in Xin et al. (2024). We also
observe decent performance of DeepSeek-R1-Distill-Qwen-32B on MiniF2F.
When evaluating InternLM2.5-StepProver, we use the Lean 4 version following InternLM2.5-
StepProver (Wu et al., 2024) from the Github repository 7 traceable by LeanDojo (Yang et al.,
2023).

D.2      Computational resources

All the models’ inference can be conducted on 2 H100 (80GB) GPUs. For fine-tuning experiment,
Goedel-Prover-SFT is fine-tuned on 8 H100 (80GB) GPUs. The GPU hours depend on which model
for inference. For example, Kimina-Distill-7B and DeepSeek-Prover-V2-7B cost much more time for
1 generation, compared to other models, due to longer generation length per response. In total, we
cost more than 10K H100 GPU hours for all the evaluations.
    7
        © https://github.com/haoyuzhao123/LeanIneqComp-Dojo


                                                   17
Table 8: Performance of Goedel-Prover-SFT fine-tuned with different data on Ineq-AMGM, Ineq-
Cauchy, and Ineq-MISC.
                                             Ineq-AMGM                       Ineq-Cauchy                     Ineq-MISC
          Model           Budget
                                   Valid       Type I    Type II   Valid       Type I    Type II   Valid      Type I     Type II
                           32      48.62.9     0.41.2    14.03.2   34.82.5     12.43.5   21.53.4   47.01.7    14.43.1    24.61.9
    Goedel-Prover-SFT      64      50.62.6     0.81.6    16.62.8   36.21.9     15.83.4   24.62.9   47.80.9    16.62.5    25.51.9
    (Lin et al., 2025a)    128     52.21.4     1.31.9    18.62.2   37.11.8     19.42.9   26.91.8   48.00.0    17.92.6    26.42.5
                          3200      60.0        4.0       24.0      40.0        32.0      28.0      48.0       24.0       36.0
                           32      89.82.7     33.25.3   14.73.6   30.43.1     7.63.7    17.83.4   37.72.5     5.22.4    4.31.8
   Cont. ft on Dcomp       64      91.51.5     38.72.9   17.43.4   32.62.4     11.24.1   21.13.3   39.51.3     6.52.9    5.22.2
 +5k Goedel SFT Data       128     92.00.0     42.93.1   19.73.0   34.92.1     15.23.6   23.52.8   40.00.0     8.53.5    6.42.5
                          3200      92.0        64.0      28.0      44.0        32.0      28.0      40.0       20.0      20.0



D.3     Other hyperparameters

To make sure all the inference jobs can be completed by 2 H100 (80GB) GPUs, the max token
generation length for DeepSeek-R1-Distill-Qwen-32B (Guo et al., 2025), Kimina-Distill-7B (Wang
et al., 2025), and DeepSeek-Prover-V2 (Ren et al., 2025) are set to be 16K. There are seldom cases
that the models do not finish generating responses, but as all the evaluation metric is pass@N where
N is normally at least 16, the final performance is not much affected.

D.4     Detailed results for fine-tuning Goedel-Prover-SFT

Please refer to Figure 3 for an illustration for our fine-tuning experiments pipeline. To generate the
fine-tuning data Dcomp , we first use algebraic transformation rules (Table 5) to augment the 25 seed
AM-GM problem (Ineq-AMGM) into 100 problems built on the 25 seed problem. Then, we apply
composition rules (Table 4) to randomly generate 5000 composed problems.
After getting these 5000 problems, we query Qwen2.5-Coder-32B-Instruct model, given the whole
proof written in Lean 4 (provided for Ineq-AMGM seed problems). For each problem, we give a
budget of 64. We get 4k verified proofs in the end, and the dataset is named Dcomp .
We observe that if we directly fine-tune Goedel-Prover-SFT or STP on Dcomp , provers’ performances
degrade a lot, possibly because there is a huge distribution shift between Dcomp and the models’
training data. In order to mitigate this issue, we mix 5k training data from Goedel-Prover-SFT (Lin
et al., 2025a) and fine-tune the same model, mitigating the huge discrepancy between Dcomp and the
training data. The performance on MiniF2F after fine-tuning is retained.
The detailed evaluation results for the fine-tuning experiments is shown in Table 8.

E      Prompt Templates
In this section, we document the prompt used for evaluating different models (Section E.1), evaluating
by in-context learning (Section E.2), and generating proofs using ICL (Section E.3)

E.1     Prompt template for evaluating different models

1. Prompt template for evaluating DeepSeek-Prover-V1.5-RL, Goedel-Prover-SFT, STP, and
DeepSeek-R1-Distill-Qwen-32B (w/o thinking).

    Complete the following Lean 4 code with explanatory comments preceding each line of code:

    ‘‘‘lean4
    import Mathlib
    import Aesop

    set_option maxHeartbeats 0

    open BigOperators Real Nat Topology Rat

    {informal_prefix}{formal_statement}



                                                             18
Here {informal_prefix} denote the natural language description of the problem, if any (written in
Lean 4 comment block), and {formal_statement} is the statement of the problem written in Lean 4.
We don’t apply_chat_template after using the prompt template.

2.     Prompt template for evaluating DeepSeek-R1-Distill-Qwen-32B (w thinking)

     Give a proof for the following problem written in lean 4:

     ‘‘‘lean4
     import Mathlib
     import Aesop

     set_option maxHeartbeats 0

     open BigOperators Real Nat Topology Rat

     {informal_prefix}{formal_statement}‘‘‘.

     You should wrap your answer in the lean code block

     ‘‘‘lean4
     <You answer>
     ‘‘‘


Here {informal_prefix} denote the natural language description of the problem, if any (written in
Lean 4 comment block), and {formal_statement} is the statement of the problem written in Lean 4.
We apply_chat_template and set generation_prompt = True.

3.     Prompt template for Kimina-Distill-7B

     Think about and solve the following problem step by step in Lean 4.
     # Informal statement:
     {informal_prefix}
     # Formal statement:
     ‘‘‘lean4
     import Mathlib
     import Aesop

     set_option maxHeartbeats 0

     open BigOperators Real Nat Topology Rat

     {formal_statement}‘‘‘


Here {informal_prefix} denote the natural language description of the problem, if any (written in
Lean 4 comment block), and {formal_statement} is the statement of the problem written in Lean 4.
We apply_chat_template and set generation_prompt = True.

E.2     Prompt template for in-context learning experiments (Section 4.2)

     Give a proof for the following problem written in lean 4:

     ‘‘‘lean4
     import Mathlib
     import Aesop

     set_option maxHeartbeats 0

     open BigOperators Real Nat Topology Rat

     {informal_prefix}{formal_statement}‘‘‘.

     Following is the solution for a related problem written in Lean 4. You can fully trust the provided
     ,→ code and it has already passed the Lean 4 compilation.
     {icl_code}

     Please follow the provided code such that you don’t make more mistakes. Your code should be
     ,→ self-contained, i.e., you should first prove the provided example inside your whole proof (not as
     ,→ a separate theorem outside the proof of the problem) if you want to use the result. You should
     ,→ wrap your answer in the lean code block




                                                      19
    ‘‘‘lean4
    <You answer>
    ‘‘‘


Here {informal_prefix} denote the natural language description of the problem, if any (written in
Lean 4 comment block), {formal_statement} is the statement of the problem written in Lean 4, and
{icl_code} is the proof of the corresponding seed problem written in Lean 4. We apply_chat_template
and set generation_prompt = True for Qwen2.5-Coder-32B-Instruct and DeepSeek-R1-Distill-Qwen-
32B (w thinking). We do not apply_chat_template for DeepSeek-R1-Distill-Qwen-32B (w/o thinking).
GPT-4o and Claude-3.7-Sonnet are accessed through API calls, where we do not use the extended
thinking for Claude-3.7-Sonnet.

E.3    Prompt template for in-context generation (Section 4.3)

    Give a proof for the following problem written in lean 4:

    ‘‘‘lean4
    import Mathlib
    import Aesop

    set_option maxHeartbeats 0

    open BigOperators Real Nat Topology Rat

    {informal_prefix}{formal_statement}‘‘‘.

    Following is the solution for a related problem written in Lean 4. You can fully trust the provided
    ,→ code and it has already passed the Lean 4 compilation.
    {icl_code1}

    {icl_code2}

    Please follow the provided code such that you don’t make more mistakes. Your code should be
    ,→ self-contained, i.e., you should first prove the provided example inside your whole proof (not as
    ,→ a separate theorem outside the proof of the problem) if you want to use the result. You should
    ,→ wrap your answer in the lean code block

    ‘‘‘lean4
    <You answer>
    ‘‘‘


Here {informal_prefix} denote the natural language description of the problem, if any (written in
Lean 4 comment block), {formal_statement} is the statement of the problem written in Lean 4, and
{icl_code1} {icl_code2} are the proof of the corresponding seed problems written in Lean 4. We
apply_chat_template and set generation_prompt = True for Qwen2.5-Coder-32B-Instruct.

F     Example of Model Generations
In this section, we show some of the generations from different models that successfully prove the
problem, including Goedel-Prover-SFT (Lin et al., 2025a), STP (Dong and Ma, 2025), DeepSeek-R1-
Distill-Qwen-32B (Guo et al., 2025), Kimina-Distill-7B (Wang et al., 2025), and DeepSeek-Prover-
V2-7B (Ren et al., 2025).

F.1    Example generations from Goedel-Prover-SFT

Below is an example generation from Goedel-Prover-SFT. In this example, the prover directly uses
sum-of-square in a brute-force way, treating the problem as a whole. Even in the comment block it
does not try to decompose the problem.

    theorem cauchy_p26 (x y a b : R) (h1 : a > 0 ∧ b > 0) (h2 : x > 0 ∧ y > 0) : (
         x + y ) * ( 1 / x + 1 / y ) * ( a + b ) * ( 1 / a + 1 / b ) ≥ 16 := by
      /-
      We need to show that for any positive real numbers \( x, y, a, b \), the
         expression \((x + y) \left(\



                                                     20
  rac{1}{x} + \

  rac{1}{y}\
  ight)(a + b) \left(\

  rac{1}{a} + \

  rac{1}{b}\
  ight)\) is at least 16.
    First, we simplify the expression by clearing denominators using the fact
       that \( a, b, x, y \) are positive. This allows us to rewrite the
       expression in a more manageable form. We then use algebraic manipulations
       and inequalities to show that the simplified expression is at least 16.
    -/
    have h3 : 0 < a * b := by
      -- Since a and b are positive, their product is also positive.
      exact mul_pos h1 .1 h1 .2
    have h4 : 0 < x * y := by
      -- Since x and y are positive, their product is also positive.
      exact mul_pos h2 .1 h2 .2
    field_simp [h1 .1.ne’, h1 .2.ne’, h2 .1.ne’, h2 .2.ne’]
    -- Clear the denominators by multiplying through by x * y * a * b, which is
       valid since x, y, a, b are positive.
    rw [le_div_iff]
    -- Rewrite the inequality in a form suitable for nlinarith.
    nlinarith [sq_nonneg (x - y), sq_nonneg (a - b), sq_nonneg (x * a - y * b)]
    -- Use non-linear arithmetic to prove the inequality.
    nlinarith [sq_nonneg (x - y), sq_nonneg (a - b), sq_nonneg (x * a - y * b)]



F.2   Example generation from STP

Below is a simple code generated from STP. STP doesn’t generate intermediate natural language
comments. However from the following example, we can see that STP also has certain ability to
decompose the problem into sub-parts and solve them separately.

  theorem amgm_p36 (x y z a b c: R ) (h1 : x+ y + z = 3) (h2 : x > 0 ∧ y> 0 ∧ z>
      0) (g1 : a+ b + c = 3) (g2 : a > 0 ∧ b> 0 ∧ c> 0): x * y * z * a * b * c ≤
      1 := by
    have h3 : 0 < x*y*z := mul_pos (mul_pos h2 .1 h2 .2.1) h2 .2.2
    have h4 : 0 < a*b*c := mul_pos (mul_pos g2 .1 g2 .2.1) g2 .2.2
    have h5 : x*y*z ≤ 1 := by
      nlinarith [pow_two_nonneg (x - y), pow_two_nonneg (x - z), pow_two_nonneg
      (y - z),
        pow_two_nonneg (x + y + z)]
    have h6 : a*b*c ≤ 1 := by
      nlinarith [pow_two_nonneg (a - b), pow_two_nonneg (a - c), pow_two_nonneg
      (b - c),
        pow_two_nonneg (a + b + c)]
    nlinarith [mul_self_nonneg (x*y*z - 1), mul_self_nonneg (a*b*c - 1)]



F.3   Example generation from DeepSeek-R1-Distill-Qwen-32B

Below we show some generations from DeepSeek-R1-Distill-Qwen-32B. In general this is a decent
model, and it can decompose the type I problem into sub-parblems. For simplicity, we omit the
thinking process and only show the Lean 4 codes generated.

  theorem amgm_p36 (x y z a b c: R ) (h1 : x+ y + z = 3) (h2 : x > 0 ∧ y> 0 ∧ z>
      0) (g1 : a+ b + c = 3) (g2 : a > 0 ∧ b> 0 ∧ c> 0): x * y * z * a * b * c ≤
      1 := by



                                             21
    -- Use the AM-GM inequality to bound the product of variables.
    -- Apply AM-GM to x, y, z, a, b, c to show that their product is at most 1.
    have h3 : 0 < x * y * z := mul_pos (mul_pos h2 .1 h2 .2.1) h2 .2.2
    have h4 : 0 < a * b * c := mul_pos (mul_pos g2 .1 g2 .2.1) g2 .2.2
    have h5 : x * y * z ≤ 1 := by
      -- Apply AM-GM to x, y, z to get x * y * z ≤ (x + y + z) ^ 3 / 27.
      rw [mul_assoc]
      nlinarith [sq_nonneg (x + y + z), sq_nonneg (x - y), sq_nonneg (x - z),
      sq_nonneg (y - z)]
    have h6 : a * b * c ≤ 1 := by
      -- Apply AM-GM to a, b, c to get a * b * c ≤ (a + b + c) ^ 3 / 27.
      rw [mul_assoc]
      nlinarith [sq_nonneg (a + b + c), sq_nonneg (a - b), sq_nonneg (a - c),
      sq_nonneg (b - c)]
    -- Combine the inequalities to conclude x * y * z * a * b * c ≤ 1.
    nlinarith

However there are also cases that even this model treat the problem as a whole. Following are two
examples.

  import Mathlib
  import Aesop

  set_option maxHeartbeats 0

  open BigOperators Real Nat Topology Rat

  theorem amgm_p39 (x y z w: R ) (h : x > 0 ∧ y> 0) (g : z > 0 ∧ w> 0): ((2:R)
      / 3 * x ^ 6 + (1:R) / 3 * y ^ 6) * ((2:R) / 3 * z ^ 6 + (1:R) / 3 * w ^
      6) ≥ x^4 * y^2 * z^4 * w^2 := by
    -- Use the AM-GM inequality to prove the inequality involving variables x,
      y, z, and w.
    -- The AM-GM inequality states that for non-negative real numbers a and b,
      (a + b)/2 ≥ sqrt(ab).
    -- We apply this inequality to each pair of terms in the given expressions.
    have h1 : 0 < x := h.1
    have h2 : 0 < y := h.2
    have h3 : 0 < z := g.1
    have h4 : 0 < w := g.2
    -- Apply the AM-GM inequality to the terms (2/3)x^6 and (1/3)y^6.
    -- Similarly, apply the AM-GM inequality to the terms (2/3)z^6 and (1/3)w^6.
    calc
      ((2 / 3: R) * x ^ 6 + (1 / 3: R) * y ^ 6) * ((2 / 3: R) * z ^ 6 + (1 / 3:
      R) * w ^ 6) ≥ (x ^ 4 * y ^ 2) * (z ^ 4 * w ^ 2) := by
        -- Use the AM-GM inequality to show that the product of the sums is at
      least the product of the individual terms.
        gcongr
        -- Apply the AM-GM inequality to each pair of terms.
        <;> nlinarith [sq_nonneg (x ^ 2 - y ^ 2), sq_nonneg (z ^ 2 - w ^ 2)]
      _ = x ^ 4 * y ^ 2 * z ^ 4 * w ^ 2 := by
        -- Simplify the expression by rearranging the terms.
        ring

  theorem amgm_p49 (a b c x y z: R) (ap : a > 0) (bp : b> 0) (cp : c> 0) (xp : x
      > 0) (yp : y> 0) (zp : z> 0) : (a^3 + b^3 + c^3) * (x^3 + y^3 + z^3) ≥
      (a^2 * b + b^2 * c + c^2 * a) * (x^2 * y + y^2 * z + z^2 * x) := by
    -- Use the AM-GM inequality to prove the given inequality.
    -- AM-GM: For non-negative real numbers, the arithmetic mean is greater than
      or equal to the geometric mean.
    -- Here, we apply AM-GM to the products of terms from the left-hand side and
      right-hand side of the inequality.
    have h1 : 0 ≤ a * x := mul_nonneg ap.le xp.le
    have h2 : 0 ≤ b * y := mul_nonneg bp.le yp.le



                                               22
    have h3 : 0 ≤ c * z := mul_nonneg cp.le zp.le
    have h4 : 0 ≤ a * y := mul_nonneg ap.le yp.le
    have h5 : 0 ≤ b * z := mul_nonneg bp.le zp.le
    have h6 : 0 ≤ c * x := mul_nonneg cp.le xp.le
    have h7 : 0 ≤ a * z := mul_nonneg ap.le zp.le
    have h8 : 0 ≤ b * x := mul_nonneg bp.le xp.le
    have h9 : 0 ≤ c * y := mul_nonneg cp.le yp.le
    -- Use nlinarith to handle the inequality, leveraging the non-negativity of
      the products established above.
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x),
      sq_nonneg (a * x - b * y), sq_nonneg (b * y - c * z),
      sq_nonneg (c * z - a * x), sq_nonneg (a * y - b * z),
      sq_nonneg (b * z - c * x), sq_nonneg (c * x - a * y),
      sq_nonneg (a * z - b * x), sq_nonneg (b * x - c * y),
      sq_nonneg (c * y - a * z)]

Following is an example such that the model explicitly mentions applying AM-GM inequality in
the comment block, but still use sum-of-square technique for formal proof, which probably not
understandable for human.

  theorem amgm_p47 (x y z a b c: R ) (h : x > 0 ∧ y> 0 ∧ z> 0) (g : x * y * z =
       (1 : R)) (habc : a > 0 ∧ b> 0 ∧ c> 0) (gabc : a * b * c = (1 : R)) :
      ((4:R) / 7 * x^3 * y + (1:R) / 7 * y^3 * z + (2:R) / 7 * z^3 * x) *
      ((4:R) / 7 * a^3 * b + (1:R) / 7 * b^3 * c + (2:R) / 7 * c^3 * a) ≥ x * a
      := by
    -- Use the AM-GM inequality to establish lower bounds for the given
      expressions.
    have h1 : ((4/7 : R) * x^3 * y + (1/7 : R) * y^3 * z + (2/7 : R) * z^3 * x)
      ≥ x := by
      -- Apply the AM-GM inequality to the terms involving x, y, and z.
      nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x),
        mul_pos h.1 h.2.1, mul_pos h.2.1 h.2.2, mul_pos h.2.2 h.1]
    have h2 : ((4/7 : R) * a^3 * b + (1/7 : R) * b^3 * c + (2/7 : R) * c^3 * a)
      ≥ a := by
      -- Apply the AM-GM inequality to the terms involving a, b, and c.
      nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
        mul_pos habc.1 habc.2.1, mul_pos habc.2.1 habc.2.2, mul_pos habc.2.2
      habc.1]
    -- Combine the results of the AM-GM inequalities to prove the overall
      inequality.
    nlinarith [mul_nonneg (sub_nonneg.mpr h1 ) (sub_nonneg.mpr h2 )]

Following are two Type I problems from Ineq-Cauchy. The composition for these two problems
are simple enough that after proving two subparts (h9 and h1 0 for cauchy_p27 and h1 , h2 for
cauchy_p31), you only need a one-line command “nlinarith” to conclude the proof in Lean 4.

  theorem cauchy_p27 (x y z a b c: R) (h1 : a > 0 ∧ b > 0 ∧ c > 0) (h2 : x > 0 ∧
       y > 0 ∧ z > 0 ) : ( x + y + z ) * ( 1 / x + 1 / y + 1 / z ) * ( a + b + c
      ) * ( 1 / a + 1 / b + 1 / c ) ≥ 81 := by
    -- Use the Cauchy-Schwarz inequality to establish lower bounds for the given
      expressions.
    have h3 : 0 < x := by linarith
    have h4 : 0 < y := by linarith
    have h5 : 0 < z := by linarith
    have h6 : 0 < a := by linarith
    have h7 : 0 < b := by linarith
    have h8 : 0 < c := by linarith
    -- Apply the Cauchy-Schwarz inequality to the sums and their reciprocals.
    have h9 : (x + y + z) * (1 / x + 1 / y + 1 / z) ≥ 9 := by
      field_simp [h3 , h4 , h5 , h6 , h7 , h8 ]
      rw [le_div_iff (by positivity), ← mul_assoc]
      nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x),



                                             23
        sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
    have h10 : (a + b + c) * (1 / a + 1 / b + 1 / c) ≥ 9 := by
      field_simp [h3 , h4 , h5 , h6 , h7 , h8 ]
      rw [le_div_iff (by positivity), ← mul_assoc]
      nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x),
        sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
    -- Multiply the lower bounds to achieve the final inequality.
    nlinarith

  theorem cauchy_p31 (x y z a b c: R) (ha : a > 0) (hb : b > 0) (hc : c > 0) (hx
      : x > 0) (hy : y > 0) (hz : z > 0) : (a / (b + c) + b / (c + a) + c / (a +
      b)) * (x / (y + z) + y / (z + x) + z / (x + y)) ≥ 9 / 4 := by
    -- Use the Cauchy-Schwarz inequality to simplify the expression.
    simp [mul_comm]
    -- Apply the Cauchy-Schwarz inequality to the fractions.
    have h1 : a / (b + c) + b / (c + a) + c / (a + b) ≥ 3 / 2 := by
      -- Use the AM-GM inequality to establish the lower bound.
      field_simp [add_comm, add_left_comm]
      rw [div_le_div_iff (by positivity) (by positivity)]
      -- Apply the AM-GM inequality to the sum of fractions.
      nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
    -- Similarly, apply the Cauchy-Schwarz inequality to the other fractions.
    have h2 : x / (y + z) + y / (z + x) + z / (x + y) ≥ 3 / 2 := by
      field_simp [add_comm, add_left_comm]
      rw [div_le_div_iff (by positivity) (by positivity)]
      nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x)]
    -- Combine the results to achieve the final inequality.
    nlinarith

Following is an example from DeepSeek-R1-Distill-Qwen-32B, where in the thinking block the
model correctly identifies the sub-parts of the problem and reduces it to the seed problem, but the
model proves the problem in Lean 4 as a whole problem (does not explicitly decompose the problem
but totally rely on the “nlinarith” tactic). This example shows a mismatch between the informal
reasoning and formal proof, on the “reasoning” side, not only on the knowledge side.
  Alright, so I’ve been given this inequality to prove: (x + y)(1/x + 1/y)(a + b)(1/a + 1/b) ≥ 16,
  ,→ and I know that x, y, a, and b are all positive real numbers. Okay, so first off, I’m thinking
  ,→ about how to approach this. It seems like it’s an inequality involving multiple variables, and
  ,→ it’s a product of two expressions, each of which is a sum multiplied by the sum of reciprocals.
  ,→ Hmm.

  I remember from algebra that there’s something called the Cauchy-Schwarz inequality, which might be
  ,→ useful here. I also recall that the AM-GM inequality relates the arithmetic mean and the
  ,→ geometric mean, which could potentially be applicable. Maybe I can apply one of these
  ,→ inequalities to simplify or bound the expression.

  Let me start by looking at a simpler version of the problem. If I consider just (x + y)(1/x + 1/y),
  ,→ perhaps I can find a pattern or a lower bound for this expression. Expanding it out, I get:

  (x + y)(1/x + 1/y) = x*(1/x) + x*(1/y) + y*(1/x) + y*(1/y) = 1 + x/y + y/x + 1 = 2 + x/y + y/x.

  Okay, so that simplifies to 2 + x/y + y/x. Now, I recall that x/y + y/x is always greater than or
  ,→ equal to 2 for positive real numbers x and y, by the AM-GM inequality. Specifically, (x/y +
  ,→ y/x)/2 ≥ sqrt(x/y * y/x) = 1, so x/y + y/x ≥ 2. Therefore, (x + y)(1/x + 1/y) ≥ 2 + 2 = 4.

  Alright, so I’ve established that (x + y)(1/x + 1/y) is at least 4. That’s interesting. Similarly, I
  ,→ can apply the same logic to (a + b)(1/a + 1/b). Let’s see:

  (a + b)(1/a + 1/b) = a*(1/a) + a*(1/b) + b*(1/a) + b*(1/b) = 1 + a/b + b/a + 1 = 2 + a/b + b/a.

  Again, by AM-GM, a/b + b/a ≥ 2, so (a + b)(1/a + 1/b) ≥ 4.

  So, now I have both (x + y)(1/x + 1/y) ≥ 4 and (a + b)(1/a + 1/b) ≥ 4. Since all variables are
  ,→ positive, multiplying these two inequalities should preserve the inequality:

  (x + y)(1/x + 1/y)(a + b)(1/a + 1/b) ≥ 4 * 4 = 16.

  And that’s exactly what I needed to prove! So, by applying the AM-GM inequality to each pair of
  ,→ terms separately and then multiplying the resulting inequalities, I’ve arrived at the desired
  ,→ conclusion.




                                                   24
  Wait a minute, let me double-check that. Did I make any assumptions that aren’t valid? I assumed
  ,→ that x, y, a, and b are positive real numbers, which is given. I used the AM-GM inequality
  ,→ correctly on x/y and y/x, and similarly for a/b and b/a. Multiplying the two inequalities is
  ,→ valid because all terms are positive, so the inequality direction remains the same.

  Is there another way to approach this problem? Maybe using Cauchy-Schwarz directly on the entire
  ,→ expression? Let’s see. The Cauchy-Schwarz inequality states that for any real numbers, (Σ a_i
  ,→ b_i)^2 ≤ (Σ a_i^2)(Σ b_i^2). I’m not sure if that would be directly applicable here, but
  ,→ perhaps if I structure the terms appropriately.

  Alternatively, I could consider taking logarithms to turn the product into a sum, but that might
  ,→ complicate things more than necessary. The AM-GM approach seems straightforward and effective for
  ,→ this problem.

  So, in summary, by applying the AM-GM inequality to each pair of terms and then multiplying the
  ,→ results, I’ve successfully proven that (x + y)(1/x + 1/y)(a + b)(1/a + 1/b) ≥ 16 for all
  ,→ positive real numbers x, y, a, and b.



  theorem cauchy_p1 (x y a b : R) (h1 : a > 0 ∧ b > 0) (h2 : x > 0 ∧ y > 0) : (
      x + y ) * ( 1 / x + 1 / y ) * ( a + b ) * ( 1 / a + 1 / b ) ≥ 16 := by
    have hx : x > 0 := h2 .1
    have hy : y > 0 := h2 .2
    have ha : a > 0 := h1 .1
    have hb : b > 0 := h1 .2
    have hxy : 0 < x * y := mul_pos hx hy
    have hab : 0 < a * b := mul_pos ha hb
    field_simp [hx.ne’, hy.ne’, ha.ne’, hb.ne’]
    rw [le_div_iff (by positivity), ← mul_assoc]
    nlinarith [sq_nonneg (x - y), sq_nonneg (a - b), sq_nonneg (x + y),
      sq_nonneg (a + b)]



F.4   Example generations from Kimina-Distill-7B

Kimina-Distill-7B also first provide a thinking draft before generating the whole proof, and the formal
Lean 4 proof is aligned with the thinking draft. We omit the thinking draft here. Following is a
generation example from Kimina, which successfully decompose the problem into two sub-parts.

  theorem cauchy_p16 (x y a b z w c d : R) (hy : y ̸= 0) (hb : b ̸= 0) (hw : w ̸=
      0) (hd : d ̸= 0) (hxy : x^2 + 1 / y^2 = 1) (hab : a^2 + 1 / b^2 = 4) (hzw :
      z^2 + 1 / w^2 = 1) (hcd : c^2 + 1 / d^2 = 4) : |(a / y + x / b) * (c / w +
      z / d)| ≤ 4 := by
    have h1 : (a / y + x / b) ^ 2 ≤ 4 := by
      have h1 : (a / y + x / b) ^ 2 ≤ (a ^ 2 + 1 / b ^ 2) * (x ^ 2 + 1 / y ^ 2)
      := by
        have h2 : (a ^ 2 + 1 / b ^ 2) * (x ^ 2 + 1 / y ^ 2) - (a / y + x / b) ^
      2 = (a * x - 1 / (b * y)) ^ 2 := by
          field_simp [hb, hy]
          ring
        have h3 : (a * x - 1 / (b * y)) ^ 2 ≥ 0 := by
          exact sq_nonneg (a * x - 1 / (b * y))
        linarith
      rw [hab, hxy] at h1
      nlinarith [sq_nonneg (a / y + x / b)]
    have h2 : (c / w + z / d) ^ 2 ≤ 4 := by
      have h1 : (c / w + z / d) ^ 2 ≤ (c ^ 2 + 1 / d ^ 2) * (z ^ 2 + 1 / w ^ 2)
      := by
        have h2 : (c ^ 2 + 1 / d ^ 2) * (z ^ 2 + 1 / w ^ 2) - (c / w + z / d) ^
      2 = (c * z - 1 / (d * w)) ^ 2 := by
          field_simp [hd, hw]
          ring
        have h3 : (c * z - 1 / (d * w)) ^ 2 ≥ 0 := by
          exact sq_nonneg (c * z - 1 / (d * w))
        linarith
      rw [hcd, hzw] at h1


                                                   25
      nlinarith [sq_nonneg (c / w + z / d)]
    have h3 : |(a / y + x / b)| ≤ 2 := by
      have h3 : -2 ≤ (a / y + x / b) := by
        nlinarith [sq_nonneg (a / y + x / b - 2), h1]
      have h4 : (a / y + x / b) ≤ 2 := by
        nlinarith [sq_nonneg (a / y + x / b - 2), h1]
      apply abs_le.mpr
      constructor <;> linarith
    have h4 : |(c / w + z / d)| ≤ 2 := by
      have h3 : -2 ≤ (c / w + z / d) := by
        nlinarith [sq_nonneg (c / w + z / d - 2), h2]
      have h4 : (c / w + z / d) ≤ 2 := by
        nlinarith [sq_nonneg (c / w + z / d - 2), h2]
      apply abs_le.mpr
      constructor <;> linarith
    have h5 : |(a / y + x / b) * (c / w + z / d)| ≤ 4 := by
      have h1 : -4 ≤ (a / y + x / b) * (c / w + z / d) := by
        nlinarith [sq_nonneg ((a / y + x / b) * (c / w + z / d) + 4), h3, h4]
      have h2 : (a / y + x / b) * (c / w + z / d) ≤ 4 := by
        nlinarith [sq_nonneg ((a / y + x / b) * (c / w + z / d) - 4), h3, h4]
      apply abs_le.mpr
      constructor <;> linarith
    exact h5


Following is another example where Kimina breaks the problem into two sub-parts.

  theorem cauchy_p26 (x y a b : R) (h1 : a > 0 ∧ b > 0) (h2 : x > 0 ∧ y > 0) : (
      x + y ) * ( 1 / x + 1 / y ) * ( a + b ) * ( 1 / a + 1 / b ) ≥ 16 := by
    have h1 : (x + y) * (1 / x + 1 / y) ≥ 4 := by
      have hxy1 : x > 0 := h2 .left
      have hy1 : y > 0 := h2 .right
      have h1 : (x + y) * (1 / x + 1 / y) - 4 = (x - y) ^ 2 / (x * y) := by
        field_simp
        ring
      have h2 : (x - y) ^ 2 ≥ 0 := by
        exact sq_nonneg (x - y)
      have h3 : x * y > 0 := mul_pos hxy1 hy1
      have h4 : (x - y) ^ 2 / (x * y) ≥ 0 := by
        apply div_nonneg
        · exact h2
        · linarith [h3]
      linarith [h1, h4]
    have h2 : (a + b) * (1 / a + 1 / b) ≥ 4 := by
      have ha1 : a > 0 := h1 .left
      have hb1 : b > 0 := h1 .right
      have h1 : (a + b) * (1 / a + 1 / b) - 4 = (a - b) ^ 2 / (a * b) := by
        field_simp
        ring
      have h2 : (a - b) ^ 2 ≥ 0 := by
        exact sq_nonneg (a - b)
      have h3 : a * b > 0 := mul_pos ha1 hb1
      have h4 : (a - b) ^ 2 / (a * b) ≥ 0 := by
        apply div_nonneg
        · exact h2
        · linarith [h3]
      linarith [h1, h4]
    nlinarith [h1, h2, mul_nonneg (le_of_lt h1 .left) (le_of_lt h1 .right),
      mul_nonneg (le_of_lt h2 .left) (le_of_lt h2 .right)]


Kimina-Distill-7B still sometimes treats the problem as a whole, even if it is not so clear how to use
sum-of-square to prove the statement.


                                                 26
  theorem amgm_p49 (a b c x y z: R) (ap : a > 0) (bp : b> 0) (cp : c> 0) (xp : x
      > 0) (yp : y> 0) (zp : z> 0) : (a^3 + b^3 + c^3) * (x^3 + y^3 + z^3) ≥
      (a^2 * b + b^2 * c + c^2 * a) * (x^2 * y + y^2 * z + z^2 * x) := by
    nlinarith [sq_nonneg (a * x - b * y), sq_nonneg (a * y - b * z), sq_nonneg
      (a * z - b * x),
      sq_nonneg (b * x - c * y), sq_nonneg (b * y - c * z), sq_nonneg (b * z - c *
       x),
      sq_nonneg (c * x - a * y), sq_nonneg (c * y - a * z), sq_nonneg (c * z - a *
       x),
      sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
      sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x),
      mul_pos ap xp, mul_pos ap yp, mul_pos ap zp, mul_pos bp xp, mul_pos bp yp,
      mul_pos bp zp, mul_pos cp xp, mul_pos cp yp, mul_pos cp zp]

In the following example, the model explicitly uses the weighted AM-GM inequality with three
variables from Mathlib (Real.geom_mean_le_arith_mean3_weighted). Note that Kimina model is the
only model we tested that can correctly apply AM-GM inequality in Mathlib.
When successfully applying AM-GM, Kimina-Distill-7B can prove the statement easily.

  theorem amgm_p6 (x y z: R) (hx : x > 0) (hy : y > 0) (hz : z > 0) : (2:R)/5 *
      x + (2:R)/5 * y + (1:R)/5 * z ≥ x ^ ((2:R)/5) * y ^ ((2:R)/5) * z ^
      ((1:R)/5) := by
    have hx’ : (0:R) ≤ x := by linarith
    have hy’ : (0:R) ≤ y := by linarith
    have hz’ : (0:R) ≤ z := by linarith
    have hw1 : (0:R) ≤ (2:R)/5 := by norm_num
    have hw2 : (0:R) ≤ (2:R)/5 := by norm_num
    have hw3 : (0:R) ≤ (1:R)/5 := by norm_num
    have hw : (2:R)/5 + (2:R)/5 + (1:R)/5 = (1:R) := by norm_num
    have h3 : (2:R)/5 * x + (2:R)/5 * y + (1:R)/5 * z ≥ x ^ ((2:R)/5) * y ^
      ((2:R)/5) * z ^ ((1:R)/5) := by
      apply Real.geom_mean_le_arith_mean3_weighted
      all_goals linarith
    exact h3

F.5   Example generations from DeepSeek-Prover-V2-7B

DeepSeek-Prover-V2-7B generates code with very similar style to that of DeepSeek-R1-Distill-Qwen-
32B, but has much stronger ability. Following is an example from Ineq-Mix that DeepSeek-Prover-
V2-7B successfully solves. The problem is constructed by first composing two problems (Table 4)
and then applying an algebraic transformation on both the LHS and RHS of the inequality. We can
see that DeepSeek-Prover-V2-7B generates very structured code, and decomposes the problem into
sub-parts.

  theorem alge_whole_p70 (a b c : R) ( ha : a > 0 ) ( hb : b > 0 ) ( hc : c > 0
      ) ( h0 : a + 2 * b = 3 ): ((3:R) * (1) + (2:R) * (( a + b + c ) * ( 1 / a +
       1 / b + 1 / c )))^3 ≥ ((3:R) * (a * b^2) + (2:R) * (9))^3 := by
    have h_main_inequality : (3:R) + 2 * (a + b + c) * (1 / a + 1 / b + 1 / c) ≥
      21 := by
      have h1 : 0 < a * b := by positivity
      have h2 : 0 < a * c := by positivity
      have h3 : 0 < b * c := by positivity
      have h4 : 0 < a * b * c := by positivity
      have h5 : 0 < a * b * c * a := by positivity
      have h6 : 0 < a * b * c * b := by positivity
      have h7 : 0 < a * b * c * c := by positivity
      field_simp
      rw [le_div_iff (by positivity)]
      nlinarith [sq_nonneg (a - b), sq_nonneg (a - c), sq_nonneg (b - c),
        sq_nonneg (a - 1), sq_nonneg (b - 1), sq_nonneg (c - 1)]




                                               27
have h_rhs_bound : ((3:R) * (a * b^2) + (2:R) * (9)) ≤ 21 := by
  have h1 : a + 2 * b = 3 := h0
  have h2 : 0 < a := ha
  have h3 : 0 < b := hb
  have h4 : 0 < a * b^2 := by positivity
  have h5 : 0 < a * b := by positivity
  -- Use non-linear arithmetic to prove the inequality
  nlinarith [sq_nonneg (b - 1), sq_nonneg (a - 1), mul_nonneg h2 .le
  (sq_nonneg (b - 1)),
    mul_nonneg h3 .le (sq_nonneg (a - 1)), mul_nonneg h2 .le (sq_nonneg (a -
  1)),
    mul_nonneg h3 .le (sq_nonneg (b - 1)), sq_nonneg (a - 3 + 2 * b),
    sq_nonneg (b - 3 / 2)]

have h_final : ((3:R) * (1) + (2:R) * (( a + b + c ) * ( 1 / a + 1 / b + 1 /
  c )))^3 ≥ ((3:R) * (a * b^2) + (2:R) * (9))^3 := by
  have h1 : (3:R) + 2 * (a + b + c) * (1 / a + 1 / b + 1 / c) ≥ 21 :=
  h_main_inequality
  have h2 : ((3:R) * (1) + (2:R) * (( a + b + c ) * ( 1 / a + 1 / b + 1 / c
  ))) ≥ 21 := by
    linarith
  have h3 : ((3:R) * (a * b^2) + (2:R) * (9)) ≤ 21 := h_rhs_bound
  have h4 : ((3:R) * (1) + (2:R) * (( a + b + c ) * ( 1 / a + 1 / b + 1 / c
  ))) ≥ ((3:R) * (a * b^2) + (2:R) * (9)) := by
    nlinarith
  have h5 : ((3:R) * (1) + (2:R) * (( a + b + c ) * ( 1 / a + 1 / b + 1 / c
  )))^3 ≥ ((3:R) * (a * b^2) + (2:R) * (9))^3 := by
    exact pow_le_pow_of_le_left (by
      -- Prove that the LHS is non-negative
      have h6 : (3:R) * (1) + (2:R) * (( a + b + c ) * ( 1 / a + 1 / b + 1 /
  c )) ≥ 0 := by
        have h7 : (a + b + c) * (1 / a + 1 / b + 1 / c) ≥ 0 := by positivity
        nlinarith
      nlinarith) h4 3
  exact h5

exact h_final




                                      28
