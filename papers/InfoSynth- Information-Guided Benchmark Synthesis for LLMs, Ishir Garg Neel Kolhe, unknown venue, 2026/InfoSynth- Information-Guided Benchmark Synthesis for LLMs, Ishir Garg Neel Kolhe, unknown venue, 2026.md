                                                InfoSynth: Information-Guided Benchmark Synthesis for LLMs
                                                              Ishir Garg                                    Neel Kolhe
                                                              UC Berkeley                                   UC Berkeley
                                                        ishirgarg@berkeley.edu                        neelkolhe@berkeley.edu

                                                            Xuandong Zhao                                  Dawn Song
                                                             UC Berkeley                                   UC Berkeley
                                                      xuandongzhao@berkeley.edu                     dawnsong@cs.berkeley.edu


                                                             Project Page: https://ishirgarg.github.io/infosynth_web/
arXiv:2601.00575v2 [cs.CL] 26 May 2026




                                                              Abstract                          et al., 2021; Cobbe et al., 2021; Liu et al., 2024a),
                                                                                                their development often demands considerable hu-
                                             Large language models (LLMs) have demon-
                                             strated significant advancements in reasoning      man labor or extensive computational resources for
                                             and code generation, but efficiently creating      problem and solution validation. Some existing
                                             new benchmarks to evaluate these capabilities      approaches utilize a judge LLM to generate and
                                             remains a challenge. Traditional benchmark         verify new problems (Majumdar et al., 2024; Li
                                             creation relies on manual human effort, which      et al., 2025b; Ding et al., 2024). However, this
                                             is expensive and time-consuming. Furthermore,      method can yield erroneous benchmarks, as the
                                             existing benchmarks often contaminate LLM
                                                                                                judge LLM may not reliably solve the generated
                                             training data, necessitating novel and diverse
                                             benchmarks to accurately assess their genuine
                                                                                                problems. This paper focuses on Python coding
                                             capabilities. This work introduces InfoSynth, a    problems, whose solutions can be verified by ex-
                                             novel framework for automatically generating       ecuting them in a code environment. Our novel
                                             and evaluating reasoning benchmarks guided         pipeline leverages this executability to ensure the
                                             by information-theoretic principles. We pro-       robustness of the generated problems.
                                             pose metrics based on KL-divergence and en-           Beyond the challenge of ensuring robustness,
                                             tropy to quantify benchmark novelty and di-        state-of-the-art (SOTA) reasoning models often
                                             versity without relying on costly model evalua-
                                                                                                overfit to their training data, leading to poor per-
                                             tions. Building on this framework, we develop
                                             an end-to-end pipeline that synthesizes robust     formance on out-of-distribution problems (Huang
                                             Python coding problems from seed datasets          et al., 2025). Furthermore, recent studies have re-
                                             using genetic algorithms and iterative code        vealed that LLM training data is frequently contam-
                                             feedback. Our method generates accurate test       inated by existing evaluation benchmarks, which
                                             cases and solutions to new problems 97% of         can artificially inflate reported performance (Deng
                                             the time, and the synthesized benchmarks con-      et al., 2024a; Golchin and Surdeanu, 2023; Deng
                                             sistently exhibit higher difficulty compared to
                                                                                                et al., 2024b). For instance, Zhang et al. (2024)
                                             prior works. Moreover, our algorithm provides
                                             a method for controlling the novelty/diversity
                                                                                                show that LLMs experience accuracy drops of
                                             and difficulty of generated problems. InfoS-       up to 8% on their novel GSM1k dataset, de-
                                             ynth offers a scalable, self-verifying pipeline    spite its similarity in difficulty to the widely used
                                             for constructing high-quality, challenging cod-    GSM8k. This underscores the critical need for new,
                                             ing benchmarks for LLMs.                           contamination-free reasoning benchmarks to gen-
                                                                                                uinely assess the capabilities of different models.
                                         1   Introduction
                                                                                                   To address these pressing issues, our work em-
                                         Large language models (LLMs) have demonstrated         phasizes two crucial benchmark properties: nov-
                                         impressive capabilities in code generation and rea-    elty and diversity. While this work does not di-
                                         soning. However, rigorously evaluating these rea-      rectly address the task of creating contamination-
                                         soning abilities remains a significant challenge.      free benchmarks, we provide an improved method
                                         While substantial effort has been invested in creat-   of generating benchmarks that cover more diverse
                                         ing robust math and coding benchmarks (Jain et al.,    and novel coding tasks. A novel benchmark should
                                         2024; Zhuo et al., 2024; Austin et al., 2021; Chen     comprise problems distinct from existing datasets,
thereby preventing models from achieving high           selection of novel problems to reduce evaluation
scores through mere memorization of previously          cost (Truong et al., 2025; Xie et al., 2025), and
seen examples. Conversely, a diverse benchmark          develops similarity and difficulty scores for cod-
should encompass a broad spectrum of dissimilar         ing tasks (Tambon et al., 2024). A key limitation
problems, enhancing its resilience against model        is reliance on SOTA model performance, making
overfitting and providing a more comprehensive          these methods accurate but computationally expen-
evaluation. Clearly, robust, novel, and diverse         sive. Our approach analyzes novelty and diversity
benchmarks are essential for the reliable evalua-       without requiring costly model evaluations.
tion of LLM reasoning abilities. Our work seeks to
answer two fundamental questions: (1) How can           3     Desirable Benchmark Properties
we effectively measure the novelty and diversity of
                                                        We propose a framework for characterizing the nov-
benchmarks? (2) How can we efficiently generate
                                                        elty and diversity of benchmarks. Our new novelty
benchmarks that possess these desirable properties
                                                        metric uses the KL-divergence to capture how dif-
while ensuring their correctness and robustness?
                                                        ferent the benchmark is from existing datasets, with
    Our main contributions can be summarized as:        the broader goal of creating benchmarks that are
• We introduce an information-theoretic frame-          contamination-free. Similarly, our proposed diver-
  work to quantify and compare the novelty and          sity metric uses Shannon entropy to capture how
   diversity of benchmarks, offering a principled       much variety exists among the problems.
   approach to benchmark assessment without re-
   liance on model evaluations.                         3.1    An Information-Theory Based
• We propose and validate an end-to-end pipeline,              Framework for Benchmark Analysis
   InfoSynth, for efficiently synthesizing novel, di-
                                                        Formally, a baseline dataset can be modeled as
  verse, and verifiably correct Python coding prob-
                                                        samples X = {xi } ⊆ Rd drawn from some true
   lems from seed datasets with genetic algorithms
                                                        distribution p(x), and the new dataset that we want
   and iterative code feedback.
                                                        to compare against the baseline can be modeled as
• Through extensive experiments, we demonstrate
                                                        samples Y = {yi } ⊆ Rd drawn from a distribution
   that InfoSynth exhibits superior robustness
                                                        q(x). Here, xi , yi represent the embedding vectors
   and difficulty compared to existing data genera-
                                                        of the problem statements in an embedding space
   tion methods. Our pipeline provides a method for
                                                        Rd . We define the novelty of the new dataset Y to
   increasing the novelty and diversity of generated
                                                        be the KL-divergence between the distributions
   problems and controlling their difficulty.
                                                                                         
                                                              Novelty(Y |X) = DKL q ∥ p
2   Related Work                                                              Z
                                                                                           q(x)
                                                                            =     q(x) log      dx      (1)
Synthetic Problem Generation. Previous work                                    Rd          p(x)
has explored generating novel synthetic datasets
                                                        Note that we take the KL-divergence of p with q as
from high-quality seed benchmarks. Wang et al.
                                                        the reference distribution to reward datasets where
(2023); Majumdar et al. (2024); Zhao et al. (2025);
                                                        q(x) is large and p(x) is small, indicating that the
Xu et al. (2024); Ahmad et al. (2025) show that
                                                        dataset contains problems not in the distribution of
LLMs can generate new instructions from exist-
                                                        the seed dataset. Given a dataset X = {xi }, xi ∼
ing ones. Xu et al. (2025); Liu et al. (2024b,
                                                        p(x), we define the diversity of the dataset to be
2023); Chen et al. (2023); Zeng et al. (2025); Chou
                                                        the differential entropy of its distribution.
et al. (2025) successfully used LLMs to generate
unit tests for solution verification. Our end-to-                               Z
end pipeline extends existing methods with code-            Diversity(X) = −         p(x) log p(x) dx (2)
                                                                                 Rd
execution environments to ensure robustness, nov-
elty, and diversity.                                    Intuitively, the KL-divergence captures the fact
   Benchmark Quality Assessment. Efficient,             that novel datasets should have different embed-
concrete analysis of benchmark quality remains          dings from existing datasets. Similarly, diverse
an open problem. Prior work defines metrics for         datasets should have embeddings that are fairly
novelty, separability, and difficulty via test-taker    spread out, as clusters indicate problems that are
performance (Li et al., 2025a,b), proposes adaptive     likely to be similar and not diverse. A “perfectly
diverse” dataset should resemble a uniform distri-         “Graph” (160), and “String” (786). We also use
bution over the embedding space so that it covers a        the MBPP test set (374) (Austin et al., 2021), Hu-
large class of problems. Since the uniform distri-         manEval (164), and 500 randomly chosen APPS
bution maximizes entropy, our metric captures this         problems (Chen et al., 2021; Hendrycks et al.,
intuitive characterization of diversity.                   2021). UMAP uses 80 neighbors and min-distance
   In practice, obtaining the full distribution            0.1, averaged over 10 independent runs with k = 4
of the embedding space is intractable.              In-    for the novelty estimator.
stead, we use statistical estimators for the KL-              Figure 1 shows our results align with intuition,
divergence and differential entropy. Given sam-            confirming KL-divergence as a measure of bench-
ples x1 , ..., xn , y1 , ..., ym ∈ Rd where x and y are    mark novelty. The middle plot’s estimator goes neg-
drawn from p(x), q(x) respectively, we use the k-          ative despite KL being theoretically nonnegative:
NN based estimator by Wang et al. (2009)                   comparing a subset against its superset yields small
                      m                                    subset–superset distances but large intra-subset dis-
                 d X     νk (i)        n                   tances. In practice this never occurs in useful com-
 DKL (q||p) =        log        + log     (3)
                 m       ρk (i)       m−1                  parisons; we include it only to show that the metric
                     i=1
                                                           still tracks human intuition, since we only care
where νk (i) is the distance from yi to its k-th near-     about relative differences between datasets.
est neighbor in {xj } and ρk (i) is the distance from
yi to its k-th nearest neighbor in {yj | j ̸= i}; k is a   3.2.2    Differential Entropy Metric Validation
hyperparameter. Similarly, we can estimate the en-         We add 4,000 random Codeforces problems (open-
tropy of a dataset. Given samples x1 , ..., xN ∈ Rd ,      r1, 2024) to the previous datasets, running UMAP
the Kozachenko-Leonenko estimator is                       with 80 neighbors and min-distance 0.1 over 10
                                                           trials. Because the Kozachenko–Leonenko esti-
  h(X) = ψ(N ) − ψ(k) + log Vd                             mator’s k-NN distances shrink with dataset size,
                                    N                      larger datasets yield artificially lower entropy; we
                                 d X
                             +       log ρk (i) (4)        therefore sample N points per dataset without re-
                                 N
                                   i=1                     placement many times and take the average.
where ψ is the digamma function, Vd is the volume             We use N =150 over 250 trials (k=4) for Leet-
of the unit ball in Rd , and ρk (i) is the distance        code vs. MBPP and N =800 over 250 trials (k=21)
between xi and its k-th nearest neighbor in {xj |          for Codeforces. “Diversity relative to X” is plotted
j ̸= i}; k is a hyperparameter.                            as a difference for visualization only; diversity it-
   Computing embeddings, KL-divergence, and en-            self is unary. Figure 2 shows that datasets expected
tropy for a text dataset is significantly faster and       to be more diverse exhibit higher entropy.
cheaper than computing test-taker statistics. Hence,
we provide a way to cheaply estimate the quality           3.3     Choosing k and d
of new benchmarks.                                         Kraskov et al. (2004) show that the bias–variance
                                                           tradeoff for dataset size N depends on k/N : larger
3.2   Empirical Validation                                 k increases bias but reduces variance and captures
We empirically verify our metrics on existing              global structure. For KL-divergence, we use k ≈ 4
datasets, embedding questions in R768 with all-            to emphasize local differences; for entropy, larger
mpnet-base-v2 (Song et al., 2020). Since entropy           k better captures global diversity, especially with
estimation suffers from the curse of dimensional-          scattered clusters; we find k/N ∈ [0.02, 0.04] ef-
ity, we project down via UMAP (McInnes et al.,             fective. Overall, diversity and entropy rankings are
2018); any datasets to be compared must share a            consistent across dimensions, and we recommend
single UMAP call to preserve their relative geom-          projecting to d ∈ [8, 12] for dataset comparison. We
etry. We renormalize after projection so distances         present ablations for all hyper-parameters used to
correspond to cosine similarity.                           compute these metrics in Appendix A.
3.2.1 KL-divergence Metric Validation
                                                           4     A Novel Benchmark Synthesis Pipeline
We use 3511 Leetcode problems with per-problem
concept labels (kaysss, 2025), from which we ex-           We introduce an end-to-end genetic algorithm for
tract three subsets by tag: “Hash Map” (686),              generating novel and diverse datasets from a seed
                                            12
                                                                                              Leetcode (with no String) against String                                                                                              15
                                                                                              Graph against String                                                                                                                                                                                                                                                                                         40
                                                                                                                                                                                                                                                                                                                                                                                                                            LeetCode (500 random problems)
                                                                                              Hash Table against String                                                                                                                                                                                                                                                                                                     HumanEval




                                                                                                                                                                                   Novelty Relative to Leetcode
                                                                                                                                                                                                                                                                                                                                                                                                           35




               Novelty Relative to String
                                            10                                                                                                                                                                                      10                                                                                                                                                                                      APPS




                                                                                                                                                                                                                                                                                                                                                                                Novelty Relative to MBPP
                                                                                                                                                                                                                                                                                                                                                                                                           30
                                            8                                                                                                                                                                                                                          Graph against Leetcode                                                                                                              25
                                                                                                                                                                                                                                    5                                  Hash Table against Leetcode
                                            6                                                                                                                                                                                                                          String against Leetcode                                                                                                             20
                                                                                                                                                                                                                                                                       MBPP against Leetcode
                                            4                                                                                                                                                                                       0                                                                                                                                                                      15

                                                                                                                                                                                                                                                                                                                                                                                                           10
                                            2
                                                                                                                                                                                                                                     5
                                                                                                                                                                                                                                                                                                                                                                                                           5
                                            0
                                                                                                                                                                                                                                                                                                                                                                                                           0
                                                                                2         3     4     5     6         7       8       9       10        11        12    13    14                                                           2       3     4   5     6       7       8       9        10        11        12    13    14                                                                              2       3       4       5       6       7       8    9    10    11   12   13   14
                                                                                                          Projection Dimension                                                                                                                                   Projection Dimension                                                                                                                                                           Projection Dimension


Figure 1: Left: Leetcode has higher novelty than its Hash Table and String subsets. Middle: MBPP has high novelty
against Leetcode, while Leetcode subsets have low relative novelty. Right: Leetcode and APPS have high novelty
against MBPP (harder, dissimilar problems); HumanEval is low (known to be MBPP-similar). 95% CIs.

                                                                                                    MBPP                                                                                                                                                                                                                                                                    8
                                                                                                                                                                                                                                                                                                                                                                                                                MBPP


                                                                                                                                                                                      Differential Entropy Relative to Codeforces
                                                                                                                                                                                                                                     0.0
                                                                                                    Leetcode                                                                                                                                                                                                                                                                                                    LeetCode (500 random problems)
                                             Differential Entropy Relative to MBPP




                                                                                                                                                                                                                                                                                                                                    Differential Entropy Relative to MBPP
                                                                                     10
                                                                                                                                                                                                                                                                                                                                                                            7
                                                                                                    String                                                                                                                           0.2                                                                                                                                                                        HumanEval
                                                                                     8              Hash Table                                                                                                                                                                                                                                                              6                                   APPS
                                                                                                    Graph                                                                                                                            0.4
                                                                                                                                                                                                                                                                                                                                                                            5
                                                                                     6
                                                                                                                                                                                                                                     0.6                                                                                                                                    4

                                                                                     4                                                                                                                                                                 Codeforces                                                                                                           3
                                                                                                                                                                                                                                     0.8               DP
                                                                                     2
                                                                                                                                                                                                                                                       Greedy                                                                                                               2

                                                                                                                                                                                                                                     1.0               Math                                                                                                                 1
                                                                                                                                                                                                                                                       Greedy and DP
                                                                                     0
                                                                                                                                                                                                                                     1.2
                                                                                                                                                                                                                                                       Greedy, DP, and Math                                                                                                 0
                                                                                          2     3     4    5      6       7       8       9        10        11    12    13   14                                                               2   3     4   5     6   7       8       9       10        11        12    13    14                                                                 2             3       4       5       6       7       8       9       10   11    12    13   14
                                                                                                                Projection Dimension                                                                                                                             Projection Dimension                                                                                                                                                   Projection Dimension

Figure 2: Left: Leetcode vs. MBPP entropy; MBPP is lower due to simpler, repetitive problems. Middle: Codeforces
vs. subsets; full datasets exceed topic-specific subsets, except Math, which overlaps others (e.g., DP, Greedy) and
appears highly dispersed when isolated. Right: Leetcode and APPS span many CS topics (high diversity);
HumanEval is lower (easier, MBPP-similar). 95% CIs.


dataset. The detailed algorithm is given in Ap-                                                                                                                                                                                                                                                          Seed Questions: 1. Write a function to rotate a
pendix C, but we describe the main ideas here. Fig-                                                                                                                                                                                                                                                      given list by a specified number of items to the
ure 3 provides a visual outline of the pipeline.                                                                                                                                                                                                                                                         right direction. 2. Write a function to find the
                                                                                                                                                                                                                                                                                                         maximum sum that can be formed which has no
                                                                                                                                                                                                                                                                                                         three consecutive elements present. Crossover
                                                                                                                                                                                                                                                                                                     Variant: Write a function to rotate a list by a
                                                                                                                                                                                                                                                                                                     specified number of steps to the right, ensuring
4.1   Data Generation Pipeline
                                                                                                                                                                                                                                                                                                     that the sum of any three consecutive elements
                                                                                                                                                                                                                                                                                                     in the newly rotated list does not exceed a given
                                                                                                                                                                                                                                                                                                     threshold.
Mutation and Crossover. We randomly apply
either crossover or mutation to the existing data                                                                                                                                                                                                                                              Appendix H contains more examples of problems.
at each iteration to generate new coding instruc-                                                                                                                                                                                                                                              Prompts are given in Appendix F.1, F.2.
tions (Majumdar et al., 2024). A key change from                                                                                                                                                                                                                                                  k-Farthest Neighbor Selection. A key improve-
previous work is that our mutation modifies an ex-                                                                                                                                                                                                                                             ment of InfoSynth is that in order to increase nov-
isting problem in three difficulty variations: easier,                                                                                                                                                                                                                                         elty and diversity, we filter problems by cosine sim-
equally difficult, and harder, encouraging diversity.                                                                                                                                                                                                                                          ilarity to those already generated. In mutation, we
We demonstrate the benefit of this in Section 5.2.                                                                                                                                                                                                                                             produce easy, medium, and hard variants, retaining
Crossover prompts combine existing questions into                                                                                                                                                                                                                                              the two of three with lowest similarity to the seed
new ones. The examples below show how mutation                                                                                                                                                                                                                                                 and generated set. In crossover, we likewise gener-
and crossover produce problems.                                                                                                                                                                                                                                                                ate three problems and keep the two least similar
                                                                                                                                                                                                                                                                                               to the dataset.
                                                                                                                                                                                                                                                                                                  Iterative Code Feedback. For each new prob-
                                                                                                                                                                                                                                                                                               lem, the model generates a Python solution and
                                                                                                                                                                                                                                                                                               test cases (prompts in Appendix F.3, F.4). Candi-
 Seed Question: Write a Python function to find
                                                                                                                                                                                                                                                                                               date solutions are executed in an isolated environ-
 the sum of an array. Hard Mutation Variant:
                                                                                                                                                                                                                                                                                               ment, and the results are fed back to the model,
 Write a Python function to find the sum of an                                                                                                                                                                                                                                                 which iteratively refines its solution and tests until
 array, where the array may contain nested lists                                                                                                                                                                                                                                               all tests pass or a maximum number of iterations
 of integers at any depth.                                                                                                                                                                                                                                                                     is reached. A key improvement of InfoSynth over
                                                               Generation for 1 Colony
                                                                   Append to seed data

                             Colony                 p = 0.5 Generate new
                               1                              problems
                                      Prompt LLM             (Crossover)
                                                                             K-Farthest       Generate
                                      to generate                            Neighbor                       Deduplication
                                                                                              Solutions
                                          new                                 Filtering                    (MinHash+LSH)                   Final
                                                            Generate new                      and Tests                     Deduplicate
                             Colony                                                                                                       Dataset
                    Seed               problems               problems
                               2
                  problems                          p = 0.5  (Mutation)

                                                                                    Repeat for N iterations
                             Colony
                               3                                            Run solution              LLM Modifies
                                                                           against tests in          Solution Based
                                                                            Python env                 On Output
                                                                                 Code Feedback Iteration




Figure 3: Generation Pipeline. Each colony processes a subset of seeds via mutation or crossover per iteration,
generates solutions/tests refined through iterative testing, then deduplicates similar problems within the colony.
Survivors seed the next iteration; colony outputs are merged and deduplicated into the final dataset.


prior methods is feeding the entire feedback history                               5           Results and Analysis
at each step, giving the model richer context; Sec-
tion 5.3 explains how this induces chain-of-thought                               We categorize generated problems as: (1) Pass-
reasoning (Wei et al., 2022). Importantly, prob-                                  ing (solution passes all tests), (2) Failing (fails ≥
lems failing self-verification are excluded from the                              1 test), (3) Erroring (syntax/runtime error), and
final dataset but still serve as seeds for the next                               (4) Unparsable (malformed, e.g., missing [solu-
generation round to encourage diversity.                                          tion]/[test] tags, more common for smaller mod-
                                                                                  els). Table 1 reports benchmark statistics: test
   Deduplication. We use the MinHash + LSH al-
                                                                                  cases equal the number of assert statements, and
gorithm with 250 permutations and a 0.75 similar-
                                                                                  test coverage is the fraction of code lines executed
ity threshold to remove textually similar problems,
                                                                                  when all tests are run. We also evaluate SOTA
similar to that done by Majumdar et al. (2024).
                                                                                  models on all datasets (Table 2); Qwen2.5 mod-
   Postprocessing. Generated problem descrip-                                     els use 4-bit quantization. Since MBPP contains
tions are not always well-aligned with their test                                 vague/misleading problems (Austin et al., 2021),
cases. For example, a problem may not describe                                    we post-processed it for fairer comparison. Thus,
how to handle edge-cases such as null inputs or                                   Table 2 focuses on post-processed results as these
empty arrays. In some problems, it is unreasonable                                provide the fairest comparison, omitting filtered
to expect a test-taker to infer the desired behavior                              versions (see Section 5.5). For each benchmark, we
(e.g., should we return None or -1 on an empty                                    randomly sample 100 problems and manually ver-
array input?). An example of such a problem is                                    ify that their solutions and test cases are fully cor-
given in Appendix G. For each problem-test pair,                                  rect and consistent with their problem statements.
the model is prompted to rephrase the question to
incorporate details on handling obscure edge-cases.                                5.1            Novelty and Diversity Analysis
The prompt is given in Appendix F.5.
                                                                                   Figure 4a presents the novelty and diversity of
                                                                                   MBPP-New and MBPP-Hard relative to MBPP-
4.2   Experimental Setup
                                                                                   Original, while Figure 4b shows the same com-
We generate six Python coding datasets in English                                  parison for Leetcode-New relative to Leetcode-
using GPT-4o (Hurst et al., 2024) as the generator.                                Original. Overall, our pipeline produces datasets
The first dataset, called MBPP-Guided, is seeded                                   that are more novel and diverse than the original
with MBPP. The second dataset, MBPP-Hard-                                          seeds. However, filtering and post-processing re-
Guided, is also seeded with MBPP, but during muta-                                 duce novelty compared to the initial generation. We
tion, the model is prompted to only make the ques-                                 attribute this to LLM memorization (Huang et al.,
tions more difficult. The third dataset, Leetcode-                                 2025; Kiyomaru et al., 2024), since more novel
Guided, is seeded with a Leetcode dataset devel-                                   problems are often out-of-distribution and harder
oped by Xia et al. (2025). For each of these three                                 for the model to solve. All UMAP simulations use
datasets, we perform the generation process again,                                 80 neighbors and a minimum distance of 0.1, ex-
but without using k-farthest neighbor selection, re-                               cept for Figure 4d, which uses 30 neighbors due to
sulting in a total of six datasets. These additional                               smaller dataset size. In general, our results are not
datasets are referred to as MBPP-New, MBPP-                                        sensitive to UMAP hyperparameters.
Hard, and Leetcode-New, respectively.                                                 Figures 4c and 4d show that k-farthest-neighbor
Table 1: Dataset statistics and quality measures. Gen. Size: Initial generation size; Filtered: Problems removed via
filtering; Avg. Tests: Avg. # test cases per problem; Human Correct: Human-verified correctness (%); Coverage:
Test coverage (%); Hours: Person-hours spent generating.

    Dataset                Gen. Size     # Filtered   Avg. Tests   % Human Correct      % Coverage      Hours
    MBPP-New                 1002           539          8.30           97%                99%           13
    MBPP-Guided               992           570          8.86           98%                99%           14
    MBPP-Hard                1007           219         10.35           96%               100%           14
    MBPP-Hard-Guided          994           468          8.86           96%               100%           15
    Leetcode-New             997            163          8.22           98%                99%           25
    Leetcode-Guided           991           177          8.66           97%               100%           27



                                   Table 2: Test-taker performance on datasets

                                                               Filtered                 Postprocessed
       Model                   Dataset
                                                       %Pass    %Fail     %Err    %Pass %Fail        %Err
                               MBPP-Original           52.67    45.99      1.34   60.43     37.70     1.87
                               MBPP-New                34.32    61.60     4.08    45.83     51.58     2.60
       Qwen2.5-7b-Instruct     MBPP-Guided               -         -         -    54.04     44.39     1.58
                               MBPP-Hard               19.82    72.52     7.66    30.14     63.01     6.85
                               MBPP-Hard-Guided          -         -         -    39.10     56.84     4.06
                               Leetcode-Original         -         -         -    11.84     83.77     4.39
                               Leetcode-New            25.29    74.12      0.59   22.70     75.46     1.84
                               Leetcode-Guided           -         -         -    28.25     71.19     0.56
                               MBPP-Original           46.79    48.93      4.28   52.41     42.51     5.08
                               MBPP-New                31.35    55.47     13.17   38.78     49.54    11.69
       Qwen2.5-3b-Coder        MBPP-Guided               -         -         -    40.53     49.30    10.18
                               MBPP-Hard               21.62    54.95     23.42   24.20     53.88    21.92
                               MBPP-Hard-Guided          -         -         -    29.06     58.12    12.82
                               Leetcode-Original         -         -         -     2.63     85.53    11.84
                               Leetcode-New            18.24    62.94     18.82   20.25     66.87    12.88
                               Leetcode-Guided           -         -         -    14.12     76.27     9.60
                               MBPP-Original           58.02    36.10      5.88   66.04     30.48     0.00
                               MBPP-New                56.96    40.63     2.41    67.35     29.68     2.97
       GPT-4.1-Mini            MBPP-Guided               -         -         -    71.93     22.46     5.61
                               MBPP-Hard               44.14    50.45     5.41    55.25     38.81     5.94
                               MBPP-Hard-Guided          -         -         -    68.38     27.78     3.85
                               Leetcode-Original         -         -         -    32.89     54.82    12.28
                               Leetcode-New            45.28    38.24     16.47   48.47     42.33     9.20
                               Leetcode-Guided           -         -         -    48.02     46.89     5.08
                               MBPP-Original           64.97    35.03      0.00   68.72     31.02     0.26
                               MBPP-New                53.99    45.64     0.37    63.64     36.18     0.19
       Gemini-2.0-Flash        MBPP-Guided               -         -         -    71.93     27.02     1.05
                               MBPP-Hard               44.59    52.25     3.15    49.32     45.66     5.02
                               MBPP-Hard-Guided          -         -         -    62.39     35.04     2.56
                               Leetcode-Original         -         -         -    32.46     64.47     3.07
                               Leetcode-New            44.71    54.12      1.18   49.08     48.47     2.45
                               Leetcode-Guided           -         -         -    45.76     50.85     3.39
                               MBPP-Original           63.37    36.63      0.00   70.86     29.14     0.00
                               MBPP-New                55.29    44.71     0.00    64.75     35.25     0.00
       Claude 3.7 Sonnet       MBPP-Guided               -         -         -    74.74     24.91     0.35
                               MBPP-Hard               45.05    52.25     2.70    56.62     40.64     2.74
                               MBPP-Hard-Guided          -         -         -    66.03     33.33     0.64
                               Leetcode-Original         -         -         -    31.14     67.11     1.75
                               Leetcode-New            44.71    54.71      0.59   42.33     57.67     0.00
                               Leetcode-Guided           -         -         -    48.02     51.98     0.00
                               MBPP-Original           66.58    33.42      0.00   70.05     29.68     0.27
                               MBPP-New                58.26    41.19     0.56    70.13     29.68     0.19
       o4-mini                 MBPP-Guided               -         -         -    77.19     22.63     0.18
                               MBPP-Hard               47.75    49.55     2.70    62.56     33.33     4.11
                               MBPP-Hard-Guided          -         -         -    72.44     26.28     1.28
                               Leetcode-Original         -         -         -    38.60     58.77     2.63
                               Leetcode-New            40.59    58.82      0.59   48.47     49.08     2.45
                               Leetcode-Guided           -         -         -    46.33     52.54     1.13
                                                                MBPP Original                                                                                                                                                          MBPP-New (Original)
                                          5
                                                                MBPP-New (Original)                                                                                                                       20
                                                                                                                                                                                                                                       MBPP-New (Filtered)                                             post-processing reliably improve diversity.
                                                                MBPP-New (Filtered)                                                                                                                                                    MBPP-New (Postprocessed)
Diversity Relative to MBPP

                                          4
                                                                MBPP-New (Postprocessed)                                                                                                                                               MBPP-Hard (Original)




                                                                                                                                                                  Novelty Relative to MBPP
                                                                MBPP-Hard (Original)                                                                                                                      15                           MBPP-Hard (Filtered)
                                          3                     MBPP-Hard (Filtered)
                                                                MBPP-Hard (Postprocessed)
                                                                                                                                                                                                                                       MBPP-Hard (Postprocessed)                                       5.2   Effect of Varying Mutation Difficulties
                                                                                                                                                                                                          10
                                          2
                                                                                                                                                                                                                                                                                                       Table 2 shows MBPP-Hard scores are 8%-15%
                                                                                                                                                                                                              5
                                          1
                                                                                                                                                                                                                                                                                                       lower than MBPP-Original across most models,
                                          0
                                                    2       3       4       5       6       7       8       9       10        11        12        13        14
                                                                                                                                                                                                              0
                                                                                                                                                                                                                           2       3        4       5         6   7   8   9   10   11   12   13   14
                                                                                                                                                                                                                                                                                                       suggesting hard mutations effectively raise diffi-
                                                                                Projection Dimension                                                                                                                                                        Projection Dimension
                                                                                                                                                                                                                                                                                                       culty. This comes with a tradeoff of the dataset hav-
     (a) Novelty and diversity in MBPP-New and MBPP-Hard.                                                                                                                                                                                                                                              ing reduced diversity and novelty as the problems
     Using all three mutation types boosts novelty. MBPP-Hard
     has higher diversity than MBPP-Original.                                                                                                                                                                                                                                                          tend to be concentrated around fewer, but more
                                          6
                                                                Leetcode Original                                                                                                                         14                           Leetcode-New (Original)                                         challenging topics. Hence, the set of mutation dif-
Diversity Relative to Leetcode Original




                                                                                                                                                                  Novelty Relative to Leetcode Original




                                          5
                                                                Leetcode-New (Original)                                                                                                                                                Leetcode-New (Filtered)
                                                                Leetcode-New (Filtered)
                                                                Leetcode-New (Postprocessed)
                                                                                                                                                                                                          12                           Leetcode-New (Postprocessed)                                    ficulties can be chosen to control the difficulty of
                                          4                                                                                                                                                               10
                                                                                                                                                                                                                                                                                                       the produced benchmark.
                                          3                                                                                                                                                                   8

                                                                                                                                                                                                              6
                                          2
                                                                                                                                                                                                              4                                                                                        5.3   Effect of Iterative Code Feedback
                                          1
                                                                                                                                                                                                              2

                                          0                                                                                                                                                                   0
                                                                                                                                                                                                                                                                                                       We find that passing solution-test pairs increase
                                                    2       3       4       5       6       7       8       9       10        11        12        13        14                                                             2       3        4       5         6   7   8   9   10   11   12   13   14
                                                                                Projection Dimension                                                                                                                                                        Projection Dimension                       by 20% over 5 feedback iterations, showing the
     (b) Leetcode-New shows greater diversity compared to the                                                                                                                                                                                                                                          effectiveness of code iteration in producing robust
     original Leetcode.                                                                                                                                                                                                                                                                                problems. Error rates drop as the LLM fixes syn-
                                                                                                                                                                                                                 12
                                                                    MBPP Original                                                                                                                                                          MBPP-New (Reformatted)
                                              3.0
                                                                    MBPP-New (Reformatted)                                                                                                                                                 MBPP-Guided (Reformatted)                                   tax/runtime issues, though the unparsable rate rises
                                              2.5
                                                                    MBPP-Guided (Reformatted)                                                                                                                    10
Diversity Relative to MBPP




                                                                                                                                                                            Novelty Relative to MBPP




                                              2.0                                                                                                                                                                      8
                                                                                                                                                                                                                                                                                                       slightly due to occasional formatting failures. Ap-
                                              1.5
                                                                                                                                                                                                                       6
                                                                                                                                                                                                                                                                                                       pendix D shows feedback curves. Three iterations
                                              1.0

                                              0.5                                                                                                                                                                      4
                                                                                                                                                                                                                                                                                                       are typically ideal; further iterations yield marginal
                                              0.0
                                                                                                                                                                                                                       2
                                                                                                                                                                                                                                                                                                       gains not worth the extra inference cost. We also
                                              0.5

                                                        2       3       4       5       6       7       8       9    10        11        12        13        14                                                                2       3        4       5     6   7   8   9   10   11   12   13   14
                                                                                                                                                                                                                                                                                                       find that iterative feedback acts as chain-of-thought
                                                                                    Projection Dimension                                                                                                                                                    Projection Dimension
                                                                                                                                                                                                                                                                                                       (CoT) reasoning (Wei et al., 2022), as the model
     (c) MBPP-Guided exhibits higher diversity but reduced nov-                                                                                                                                                                                                                                        leverages the full feedback history to refine solu-
     elty compared to MBPP-New.
                                                                                                                                                                                                                                                                                                       tions/tests, lowering both error and failure rates.
                                                                                                                                                                                                                                           Leetcode-New (Reformatted)
Diversity Relative to Leetcode Original




                                              0.4
                                                                                                                                                                                                                                           Leetcode-Guided (Reformatted)
                                                                                                                                                                               Novelty Relative to Leetcode Original




                                                                                                                                                                                                                       4                                                                               An example of this is in Appendix I.
                                              0.2


                                              0.0                                                                                                                                                                      3


                                              0.2
                                                                                                                                                                                                                                                                                                       5.4   Analysis of Filtered-Out Problems
                                                                                                                                                                                                                       2
                                              0.4

                                                                                                                                                                                                                       1
                                                                                                                                                                                                                                                                                                       We include an analysis of the types of problems
                                              0.6
                                                                    Leetcode Original
                                              0.8
                                                                    Leetcode-New (Reformatted)
                                                                    Leetcode-Guided (Reformatted)
                                                                                                                                                                                                                                                                                                       filtered out in InfoSynth and the insights it provides
                                                                                                                                                                                                                       0
                                                        2       3       4       5       6       7
                                                                                    Projection Dimension
                                                                                                        8       9        10        11        12        13    14                                                            2       3         4      5         6   7   8   9   10
                                                                                                                                                                                                                                                            Projection Dimension
                                                                                                                                                                                                                                                                                   11   12   13   14   in Appendix E. InfoSynth reveals that current mod-
     (d) Leetcode-Guided exhibits higher diversity but reduced
                                                                                                                                                                                                                                                                                                       els struggle when handling interacting constraints
     novelty compared to Leetcode-New.                                                                                                                                                                                                                                                                 and maintaining global consistency, get stuck in
                                                                                                                                                                                                                                                                                                       superficial debugging loops focused on local fixes
      Figure 4: Novelty and diversity analysis across MBPP                                                                                                                                                                                                                                             without revisiting higher-level structure, and fail to
      and Leetcode variants.
                                                                                                                                                                                                                                                                                                       produce numerical test cases even when they derive
                                                                                                                                                                                                                                                                                                       correct symbolic solutions.
    filtering improves dataset novelty and diversity.
    This comes at the cost of generating easier prob-                                                                                                                                                                                                                                                  5.5   Effect of the Postprocessing Step
    lems (Table 2), highlighting the ability of InfoSynth                                                                                                                                                                                                                                              Appendix G shows two post-processed examples,
    to control the novelty–diversity–difficulty trade-                                                                                                                                                                                                                                                 where the model resolves ambiguous edge cases
    off. Empirically, this arises because the gener-                                                                                                                                                                                                                                                   and sometimes rephrases statements more con-
    ator struggles to produce difficult problems that                                                                                                                                                                                                                                                  cisely without losing information. Table 2 shows 5–
    are not conceptually aligned with the seeds. We                                                                                                                                                                                                                                                    15% accuracy gains across most test-taker models,
    also observe a tradeoff between novelty and di-                                                                                                                                                                                                                                                    confirming that post-processing reduces ambiguity.
    versity: highly novel datasets tend to concentrate                                                                                                                                                                                                                                                 Manual verification of 100 problems per dataset
    around low-density regions in the seed-embedding                                                                                                                                                                                                                                                   further shows 100% of post-processed problems
    distribution, which increases novelty but reduces                                                                                                                                                                                                                                                  are correctly reformatted without altering the core
    diversity. Our results also show that filtering and                                                                                                                                                                                                                                                question.
        Model                            InfoSynth (ours)                      KodCode                 GeneticInstruct   AutoCodeBench      OpenCodeInstruct
        o4-mini                              48.47%                             75.15%                    61.00%             72.00%             63.85%
        gpt-4.1-mini                         48.47%                             69.00%                     59.5%             64.44%             72.59%
        gemini-2.0-flash                     49.08%                             55.50%                    51.00%             63.57%             80.00%
        claude-3.7-sonnet                    42.33%                             53.00%                    56.00%             78.29%             76.92%

Table 3: Comparison of model pass rates across different synthetic instruction generation methods. Lower means
harder problems.


5.6              Relating Diversity and Topic Coverage                                                     coverage rather than difficulty, applying only a ba-
For each problem in MBPP-Original, MBPP-New,                                                               sic filter that removes problems solvable 10 times
and MBPP-Guided, we prompted GPT-4o-mini                                                                   in a row by a test-taker; InfoSynth instead com-
(Hurst et al., 2024) to list up to 3 topics describing                                                     bines mutation/crossover, iterative feedback, and
the problem mimicking Zhao et al. (2025). The                                                              novelty-based filtering.
list of allowed topics was taken from the Leetcode
                                                                                                           Token Efficiency Comparison. Let N denote
dataset (kaysss, 2025). The prompt is given in
                                                                                                           the token length of a full problem instance (state-
Appendix J.
                                                                                                           ment, solution, and tests). Table 4 summarizes per-
                                        Top 10 Topics (Normalized by Dataset Totals)                       instance token costs and their sources. InfoSynth
             Number Theory                                                             MBPP-Original
        Dynamic Programming                                                            MBPP-New            uses iterative, execution-driven refinement: each
                   Simulation                                                          MBPP-Guided
             String Matching                                                                               problem runs multiple feedback rounds where the
                     Counting
Topic




                      Sorting                                                                              model generates a solution, executes it in a sand-
                   Hash Table
                        Math
                       String                                                                              box, and refines on errors (≈ 7N input). KodCode
                        Array
                            0.0   0.1             0.2              0.3         0.4         0.5             samples K independent solution attempts without
                                                        Normalized Frequency
                                                                                                           feedback, yielding lower input but similar output
Figure 5: Fraction of problems relating to each topic for                                                  cost (≈ 4N across attempts). GeneticInstruct uses
the 10 most common topics                                                                                  a fixed four-step pipeline (generate, solve, LLM-
                                                                                                           judge, deduplicate) with ≈ 4N input, relying on
  Figure 5 shows that InfoSynth increases the num-                                                         LLM-based evaluation rather than execution. Au-
ber of problems that use each concept for most                                                             toCodeBench adds four generation stages (prob-
topics, creating more diverse problems. We find                                                            lem, solution, test integration, quality control) plus
that for topics with lesser coverage in the original                                                       up to 10 test-taker solve attempts per problem,
MBPP dataset, our pipeline produces many more                                                              scaling to ≈ 14N . OpenCodeInstruct mirrors Ge-
problems covering those topics.                                                                            neticInstruct’s generate–solve–judge–deduplicate
                                                                                                           pipeline but with extra judging/deduplication over-
5.7              Comparison to Previous Methods                                                            head, pushing output beyond 2N . Overall, InfoS-
We compare InfoSynth to GeneticInstruct (Ma-                                                               ynth uses more cheap input tokens but a compara-
jumdar et al., 2024), KodCode (Xu et al., 2025),                                                           ble count of expensive output tokens to prior work.
OpenCodeInstruct (Ahmad et al., 2025), and Au-
                                                                                                            Method              Input Tokens    Output Tokens
toCodeBench (Chou et al., 2025). Note that all of                                                           InfoSynth                7N               4N
pipelines have used Leetcode-based seed datasets.                                                           KodCode                  4N               4N
                                                                                                            GeneticInstruct          4N         N + judge/dedup
                                                                                                            AutoCodeBench           14N              14N
Difficulty Comparison. Table 3 shows InfoS-                                                                 OpenCodeInstruct         4N        2N + judge/dedup
ynth generates more challenging problems than
prior works.        The high pass rates on Au-                                                             Table 4: Per-instance token cost comparison of bench-
                                                                                                           mark generation pipelines.
toCodeBench and OpenCodeInstruct partly reflect
quality issues: a large fraction of OpenCodeInstruct
lacks correct solutions/tests, so we filter using its
                                                                                                           5.8   Choosing an embedding model
provided correctness labels. This itself highlights
an InfoSynth advantage: although OpenCodeIn-                                                               We test various embedding models on our datasets
struct uses a simpler mutation/crossover, it omits it-                                                     in Appendix B. Across models, the relative novelty
erative feedback, which we find essential for raising                                                      and diversity between datasets remains the same
difficulty. AutoCodeBench targets multi-language                                                           despite some fluctuations in their magnitudes.
6   Conclusion                                          surrogate measures for relative comparison rather
                                                        than absolute Shannon entropy or KL-divergence
In this paper, we introduced InfoSynth, a novel
                                                        in the original space. While we do not have for-
framework to calculate the diversity and novelty of
                                                        mal theoretical guarantees, we observe empirically
new benchmarks in an efficient and cost-effective
                                                        that rankings induced by these metrics remain sta-
manner. Using the ideas behind this framework, we
                                                        ble across embedding choices and hyperparameter
propose a new coding problem generation pipeline
                                                        settings, supporting their practical utility.
that produces more challenging and robust prob-
                                                           Finally, because of its filtration step, InfoSynth
lems from seed data than previous works. We hope
                                                        is biased toward short-horizon reasoning problems.
that future work will leverage our ideas to create
                                                        Despite this constraint, we find that the resulting
robust, novel, and diverse benchmarks.
                                                        tasks remain challenging for frontier models, indi-
7   Limitations                                         cating that short-horizon difficulty is still a mean-
                                                        ingful evaluation axis. Extending the framework to
InfoSynth has several limitations, which we explic-     promote longer horizon tasks is a promising direc-
itly acknowledge.                                       tion for expanding beyond this regime.
    In a small number of cases, LLMs may generate
correct solutions but fail to strictly conform to the   8   Ethical considerations
required output format (e.g., function signatures or
structured test specifications). Our execution-based    This paper presents work whose goal is to advance
validation pipeline mitigates most of these cases       the field of machine learning by enabling scal-
by enforcing deterministic programmatic checks,         able, information-guided synthesis of novel bench-
though improving semantic parsing is a natural          marks for LLMs, addressing data creation chal-
extension. Our evaluation also focuses on Python        lenges. Potential societal consequences include
problems; however, InfoSynth is language-agnostic       improved, unbiased evaluations of LLM capabil-
and we believe the framework can be extended to         ities in reasoning and code generation, fostering
other languages with executable verification.           reliable AI deployment in applications like soft-
    Additionally, a significant fraction of candidate   ware development and scientific discovery. This
problems fail self-verification, including some that    work does not involve human subjects, person-
are otherwise novel or non-trivial. We believe that     ally identifiable data, or sensitive attributes. All
this filtering is an intentional design choice that     datasets used (MBPP, Leetcode, and Codeforces)
prioritizes correctness and evaluability over raw       are publicly available, and our generated bench-
generation volume. Importantly, we observe that         marks were produced through synthetic problem
higher rejection rates correlate with increased final   generation and automated verification. We have
benchmark difficulty, suggesting the filtering step     carefully ensured that no private or proprietary code
is not merely discarding noise but actively shap-       was included. Potential risks include the misuse
ing a more challenging problem distribution. For        of generated benchmarks for unfair evaluation or
example, 28.2% of problems generated by Open-           dataset contamination in future model training; to
CodeInstruct have failing solutions/tests, and up       mitigate this, we document our pipeline in detail
to 60% of problems generated by KodCode are             and encourage responsible use. We used a few
filtered out. However, as shown in Table 3, these       open-source datasets: MBPP (Austin et al., 2021)
problems are substantially easier than those gen-       which uses a CC-BY-4.0 license, a Leetcode dataset
erated by InfoSynth. Future improvements could          by (Xia et al., 2025) which uses Apache 2.0, a
incorporate stronger verifier models or multi-model     dataset by (kaysss, 2025) which uses an MIT li-
consensus to further reduce false rejections while      cense, the APPS dataset (Hendrycks et al., 2021)
preserving this difficulty signal.                      which uses CC-BY-SA-3.0, a Codeforces dataset
    Moreover, our novelty and diversity metrics         (open-r1, 2024) which uses CC-BY-4.0, and Hu-
are computed using k-NN estimators in a UMAP-           manEval (Chen et al., 2021) which uses the MIT li-
projected embedding space. While UMAP does              cense. We have open-sourced all code and datasets
not preserve global geometry exactly, it is designed    for InfoSynth under the Apache 2.0 license. Our
to maintain local neighborhood structure, which is      work has used the datasets above only for research
the primary signal used by k-NN estimators. As a        purposes, and is fully compatible with their access
result, the metrics should be interpreted as stable     conditions. We also acknowledge that there was
some usage of AI assistants for this work; however,       8706–8719, Mexico City, Mexico. Association for
they were used only to make minor grammatical             Computational Linguistics.
improvements to the manuscript.
                                                        Yuyang Ding, Xinyu Shi, Xiaobo Liang, Juntao Li,
                                                          Qiaoming Zhu, and Min Zhang. 2024. Unleash-
                                                          ing Reasoning Capability of LLMs via Scalable
References                                                Question Synthesis from Scratch. ArXiv preprint,
Wasi Uddin Ahmad, Aleksander Ficek, Mehrzad               abs/2410.18693.
 Samadi, Jocelyn Huang, Vahid Noroozi, Somshubra
 Majumdar, and Boris Ginsburg. 2025. Opencodein-        Shahriar Golchin and Mihai Surdeanu. 2023. Data Con-
 struct: A large-scale instruction tuning dataset for     tamination Quiz: A Tool to Detect and Estimate
 code llms. arXiv preprint.                               Contamination in Large Language Models. ArXiv
                                                          preprint, abs/2311.06233.
Jacob Austin, Augustus Odena, Maxwell I. Nye,
   Maarten Bosma, Henryk Michalewski, David Dohan,      Dan Hendrycks, Steven Basart, Saurav Kadavath, Man-
   Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V.     tas Mazeika, Akul Arora, Ethan Guo, Collin Burns,
   Le, and Charles Sutton. 2021. Program Synthe-          Samir Puranik, Horace He, Dawn Song, and Jacob
   sis with Large Language Models. ArXiv preprint,        Steinhardt. 2021. Measuring coding challenge com-
   abs/2108.07732.                                        petence with apps. ArXiv preprint, abs/2105.09938.
Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan,       Kaixuan Huang, Jiacheng Guo, Zihao Li, Xiang Ji, Ji-
  Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2023.        awei Ge, Wenzhe Li, Yingqing Guo, Tianle Cai, Hui
  Codet: Code generation with generated tests. In         Yuan, Runzhe Wang, Yue Wu, Ming Yin, Shange
  The Eleventh International Conference on Learning       Tang, Yangsibo Huang, Chi Jin, Xinyun Chen,
  Representations, ICLR 2023, Kigali, Rwanda, May         Chiyuan Zhang, and Mengdi Wang. 2025. MATH-
  1-5, 2023. OpenReview.net.                              Perturb: Benchmarking LLMs’ Math Reasoning
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,         Abilities against Hard Perturbations. ArXiv preprint,
 Henrique Ponde De Oliveira Pinto, Jared Kaplan,          abs/2502.06453.
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
 Brockman, and 1 others. 2021. Evaluating Large         Aaron Hurst, Adam Lerer, Adam P Goucher, Adam
 Language Models Trained on Code. ArXiv preprint,         Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow,
 abs/2107.03374.                                          Akila Welihinda, Alan Hayes, Alec Radford, and 1
                                                          others. 2024. Gpt-4o system card.
Jason Chou, Ao Liu, Yuchi Deng, Zhiying Zeng,
   Tao Zhang, Haotian Zhu, Jianwei Cai, Yue Mao,        Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia
   Chenchen Zhang, Lingyun Tan, Ziyan Xu, Bohui           Yan, Tianjun Zhang, Sida Wang, Armando Solar-
   Zhai, Hengyi Liu, Speed Zhu, Wiggin Zhou, and          Lezama, Koushik Sen, and Ion Stoica. 2024. Live-
   Fengzong Lian. 2025. Autocodebench: Large lan-         CodeBench: Holistic and Contamination Free Eval-
   guage models are automatic code benchmark genera-      uation of Large Language Models for Code. ArXiv
   tors. arXiv preprint.                                  preprint, abs/2403.07974.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,         kaysss. 2025.   leetcode-problem-set.   https:
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias          //huggingface.co/datasets/kaysss/
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro         leetcode-problem-set.     Accessed: 2025-05-
  Nakano, Christopher Hesse, and John Schulman.           11.
  2021. Training Verifiers to Solve Math Word Prob-
  lems. ArXiv preprint, abs/2110.14168.                 Hirokazu Kiyomaru, Issa Sugiura, Daisuke Kawahara,
Chunyuan Deng, Yilun Zhao, Xiangru Tang, Mark Ger-        and Sadao Kurohashi. 2024. A Comprehensive Anal-
  stein, and Arman Cohan. 2024a. Investigating data       ysis of Memorization in Large Language Models. In
  contamination in modern benchmarks for large lan-       Proceedings of the 17th International Natural Lan-
  guage models. In Proceedings of the 2024 Confer-        guage Generation Conference, INLG 2024, Tokyo,
  ence of the North American Chapter of the Associ-       Japan, September 23 - 27, 2024, pages 584–596. As-
  ation for Computational Linguistics: Human Lan-         sociation for Computational Linguistics.
  guage Technologies (Volume 1: Long Papers), pages
  8706–8719, Mexico City, Mexico. Association for       Alexander Kraskov, Harald Stögbauer, and Peter Grass-
  Computational Linguistics.                              berger. 2004. Estimating mutual information. Physi-
                                                          cal Review E, 69(6).
Chunyuan Deng, Yilun Zhao, Xiangru Tang, Mark Ger-
  stein, and Arman Cohan. 2024b. Investigating data     Xiang Lisa Li, Farzaan Kaiyom, Evan Zheran Liu, Yifan
  contamination in modern benchmarks for large lan-       Mai, Percy Liang, and Tatsunori Hashimoto. 2025a.
  guage models. In Proceedings of the 2024 Confer-        AutoBencher: Towards Declarative Benchmark Con-
  ence of the North American Chapter of the Associ-       struction. In The Thirteenth International Confer-
  ation for Computational Linguistics: Human Lan-         ence on Learning Representations, ICLR 2025, Sin-
  guage Technologies (Volume 1: Long Papers), pages       gapore, April 24-28, 2025. OpenReview.net.
Yisen Li, Lingfeng Yang, Wenxuan Shen, Pan Zhou,             pages 13484–13508, Toronto, Canada. Association
  Yao Wan, Weiwei Lin, and Dongping Chen. 2025b.             for Computational Linguistics.
  CrowdSelect: Synthetic Instruction Data Selec-
  tion with Multi-LLM Wisdom. ArXiv preprint,              Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  abs/2503.01836.                                             Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
                                                              and Denny Zhou. 2022. Chain-of-thought prompting
Jiate Liu, Yiqin Zhu, Kaiwen Xiao, Qiang Fu, Xiao             elicits reasoning in large language models. In Ad-
   Han, Wei Yang, and Deheng Ye. 2023. RLTF: Rein-            vances in Neural Information Processing Systems 35:
   forcement Learning from Unit Test Feedback. ArXiv         Annual Conference on Neural Information Process-
   preprint, abs/2307.04349.                                  ing Systems 2022, NeurIPS 2022, New Orleans, LA,
                                                              USA, November 28 - December 9, 2022.
Jiawei Liu, Thanh Nguyen, Mingyue Shang, Hantian
   Ding, Xiaopeng Li, Yu Yu, Varun Kumar, and Zijian       Yunhui Xia, Wei Shen, Yan Wang, Jason Klein Liu,
   Wang. 2024a. Learning Code Preference via Syn-            Huifeng Sun, Siyue Wu, Jian Hu, and Xiaolong Xu.
   thetic Evolution. ArXiv preprint, abs/2410.03837.         2025. LeetCodeDataset: A Temporal Dataset for
                                                             Robust Evaluation and Efficient Training of Code
Zhihan Liu, Shenao Zhang, and Zhaoran Wang. 2024b.           LLMs. ArXiv preprint, abs/2504.14655.
  DSTC: Direct Preference Learning with Only Self-
  generated Tests and Code to Improve Code LMs.            Jingxu Xie, Dylan Xu, Xuandong Zhao, and Dawn
  ArXiv preprint, abs/2411.13611.                             Song. 2025. Agentsynth: Scalable task generation
                                                              for generalist computer-use agents. arXiv preprint
Somshubra Majumdar, Vahid Noroozi, Sean Narenthi-             arXiv:2506.14205.
  ran, Aleksander Ficek, Jagadeesh Balam, and Boris
                                                           Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng,
  Ginsburg. 2024. Genetic Instruct: Scaling up Syn-
                                                             Pu Zhao, Jiazhan Feng, Chongyang Tao, Qingwei
  thetic Generation of Coding Instructions for Large
                                                             Lin, and Daxin Jiang. 2024. Wizardlm: Empow-
  Language Models. ArXiv preprint, abs/2407.21077.
                                                             ering large pre-trained language models to follow
Leland McInnes, John Healy, Nathaniel Saul, and Lukas        complex instructions. In The Twelfth International
  Großberger. 2018. UMAP: Uniform Manifold Ap-               Conference on Learning Representations, ICLR 2024,
  proximation and Projection. J. Open Source Softw.,         Vienna, Austria, May 7-11, 2024. OpenReview.net.
  3(29):861.                                               Zhangchen Xu, Yang Liu, Yueqin Yin, Mingyuan Zhou,
open-r1. 2024.    Codeforces Problems Dataset.               and Radha Poovendran. 2025. KodCode: A Diverse,
  https://huggingface.co/datasets/open-r1/                   Challenging, and Verifiable Synthetic Dataset for
  codeforces. Accessed: 2025-05-11.                          Coding. ArXiv preprint, abs/2503.02951.
                                                           Huaye Zeng, Dongfu Jiang, Haozhe Wang, Ping Nie, Xi-
Kaitao Song, Xu Tan, Tao Qin, Jianfeng Lu, and Tie-          aotong Chen, and Wenhu Chen. 2025. ACECODER:
  Yan Liu. 2020. Mpnet: Masked and permuted pre-             Acing Coder RL via Automated Test-case Synthesis.
  training for language understanding. In Advances           ArXiv preprint, abs/2502.01718.
  in Neural Information Processing Systems 33: An-
  nual Conference on Neural Information Processing         Hugh Zhang, Jeff Da, Dean Lee, Vaughn Robinson,
  Systems 2020, NeurIPS 2020, December 6-12, 2020,           Catherine Wu, William Song, Tiffany Zhao, Pranav
  virtual.                                                   Raja, Charlotte Zhuang, Dylan Slack, Qin Lyu, Sean
                                                             Hendryx, Russell Kaplan, Michele Lunati, and Sum-
Florian Tambon, Amin Nikanjam, Cyrine Zid, Foutse            mer Yue. 2024. A careful examination of large lan-
  Khomh, and Giuliano Antoniol. 2024. TaskE-                 guage model performance on grade school arithmetic.
  val: Assessing Difficulty of Code Generation Tasks         In Advances in Neural Information Processing Sys-
  for Large Language Models.         ArXiv preprint,         tems 38: Annual Conference on Neural Information
  abs/2407.21227.                                            Processing Systems 2024, NeurIPS 2024, Vancouver,
                                                             BC, Canada, December 10 - 15, 2024.
Sang T. Truong, Yuheng Tu, Percy Liang, Bo Li,
  and Sanmi Koyejo. 2025. Reliable and Efficient           Xueliang Zhao, Wei Wu, Jian Guan, and Lingpeng
  Amortized Model-based Evaluation. ArXiv preprint,          Kong. 2025. PromptCoT: Synthesizing Olympiad-
  abs/2503.13335.                                            level Problems for Mathematical Reasoning in Large
                                                             Language Models. ArXiv preprint, abs/2503.02324.
Qing Wang, Sanjeev R. Kulkarni, and Sergio Verdú.
  2009. Divergence estimation for multidimensional         Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu,
  densities via k-nearest-neighbor distances. IEEE           Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani
  Trans. Inf. Theory, 55(5):2392–2405.                       Yusuf, Haolan Zhan, Junda He, Indraneil Paul, Simon
                                                             Brunner, Chen Gong, Thong Hoang, Armel Randy
Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa           Zebaze, Xiaoheng Hong, Wen-Ding Li, Jean Kad-
  Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh          dour, Ming Xu, Zhihan Zhang, and 14 others. 2024.
  Hajishirzi. 2023. Self-instruct: Aligning language         BigCodeBench: Benchmarking Code Generation
  models with self-generated instructions. In Proceed-       with Diverse Function Calls and Complex Instruc-
  ings of the 61st Annual Meeting of the Association for     tions. ArXiv preprint, abs/2406.15877.
  Computational Linguistics (Volume 1: Long Papers),
A    Sensitivity Analysis for k and UMAP
     Parameters
We present ablations for hyper-parameters used in
our experiments. In general, our results generalize
robustly across a wide range of hyper-parameters.
Note that in the cases where changing a hyperpa-
rameter affects the novelty or diversity, it affects
all datasets by roughly the same amount. Since
                                                        Algorithm 1 Problem Generation with Evolution-
our analysis looks at relative differences between
                                                        ary Strategies
benchmarks, our conclusions are still robust.
                                                         Input: N : total number of problems; Nc : number of
   Specifically, we ablate three hyperparameters in      colonies; Bs : seed batch size; C: problems per crossover;
Figure 6:                                                Bc : crossover batch size; Nit : iterations

    • k: the number of k-NN neighbors considered         procedure G ENERATE(seedData, numSamples)
                                                         Initialize problems ← ∅
      in the estimators                                  for colony = 1 to Nc do
                                                            Ns ← N/Nc
    • n_neighbors: the number of neighbors used in          colonySeedData ← Random sample of size Bs from
      the UMAP algorithm                                    seedData
                                                            problems       ←      problems  ∪      E VOLVE -
    • min_dist: the minimum distance used in the            C OLONY(colonySeedData, Ns )
                                                            deduplicate(problems)
      UMAP algorithm                                     end for
                                                         return problems

B    Choice of Embedding Model                           procedure E VOLVE C OLONY(seedData, Ns )
                                                         newProblems ← ∅
We test various embedding models on our datasets.        repeat
Figures 7a, 7b show that the relative novelty and          operation ← “mutation” w.p. 0.5, “crossover” w.p. 0.5
                                                           if operation == “mutation” then
diversity of datasets remains similar across em-              problem ← random sample from seedData
bedding models despite some fluctuations in the               problems ← problems ∪ mutate(problem)
magnitudes of those differences.                           end if
                                                           if operation == “crossover” then
                                                              batch ← random sample of size Bc from seedData
C    Algorithm For Problem Generation                         problems ← problems ∪ crossover(C, batch)
                                                           end if
For MBPP-New we used N = 1000, Nc = 10,                    if k-farthest-neighbor-filtering enabled then
Bs = 30, C = 2, Bc = 5, Nit = 5. For MBPP-                    U ← newProblems ∪ seedData
                                                              problems ← select K with least cosine similarity to U
Hard we used N = 500, Nc = 10, Bs = 15,                    end if
C = 1, Bc = 4, Nit = 5. For Leetcode-New                   newProblems ← newProblems ∪ problems
we used N = 1000, Nc = 10, Bs = 30, C = 2,                 deduplicate(newProblems)
                                                           seedData ← seedData ∪ problems
Bc = 4, Nit = 5.                                         until |newProblems| ≥ Ns
  For MBPP-Guided we used N = 1000, Nc =                 return newProblems
10, Bs = 30, C = 3, Bc = 5, Nit = 3. For
                                                         procedure G ENERATE S OLS T ESTS(problem)
MBPP-Hard-Guided we used N = 500, Nc = 10,               GenerateTests(problem)
Bs = 15, C = 3, Bc = 4, Nit = 3. For Leetcode-           GenerateSolutions(problem)
                                                         for i = 1 to Nit do
Guided we used N = 1000, Nc = 10, Bs = 30,                 Run tests against solutions
C = 3, Bc = 4, Nit = 3.                                    Feed output to LLM to modify tests and solution
  The algorithm is given in Algorithm 1                  end for

D    Code-Feedback Results
Figures 8, 9 show how the proportion of problems
that pass, fail, error, and are unparsable changes
as a function of the number of code feedback it-
erations. The results shown are consistent across
all datasets; in general, more than 3 feedback itera-
tions provide minimal gains in pass rate.
                                                                                       MBPP-New                                                                              7
                                                                                                                                                                                                               MBPP-New (Filtered)                                                                                       7
                                                                                                                                                                                                                                                                                                                                                      MBPP-New (Reformatted)
                                    6




Entropy Relative to MBPP-Original




                                                                                                                                         Entropy Relative to MBPP-Original




                                                                                                                                                                                                                                                                                     Entropy Relative to MBPP-Original
                                                              k=2                                                                                                                                          k=2                                                                                                                                      k=2
                                    5                         k=3                                                                                                            6                             k=3                                                                                                           6                          k=3
                                                              k=4                                                                                                            5
                                                                                                                                                                                                           k=4                                                                                                           5
                                                                                                                                                                                                                                                                                                                                                    k=4
                                    4                         k=5                                                                                                                                          k=5                                                                                                                                      k=5
                                                              k=6                                                                                                            4                             k=6                                                                                                           4                          k=6
                                    3                         k=8                                                                                                                                          k=8                                                                                                                                      k=8
                                                              k=10                                                                                                           3
                                                                                                                                                                                                           k=10                                                                                                          3                          k=10
                                    2
                                                                                                                                                                             2                                                                                                                                           2
                                    1                                                                                                                                        1                                                                                                                                           1

                                              2       3       4        5       6        7       8       9       10   11   12   13   14                                                     2       3        4       5       6       7       8       9       10   11   12   13   14                                                  2       3       4        5       6       7   8   9   10   11   12   13   14
                                                                       Projection Dimension                                                                                                                         Projection Dimension                                                                                                                     Projection Dimension

                                                      (a) Diversity changes by a similar amount for all benchmarks as k changes
                                                                                       MBPP-New                                                                                                                MBPP-New (Filtered)                                                                                                                    MBPP-New (Reformatted)
Novelty Relative to MBPP-Original




                                                                                                                                             Novelty Relative to MBPP-Original




                                                                                                                                                                                                                                                                                       Novelty Relative to MBPP-Original
                                                                                                                                                                                                                                                                                                                            9
                                                              k=2                                                                                                                                          k=2                                                                                                                                      k=2
                                    12
                                                              k=3                                                                                                                8                         k=3                                                                                                              8                       k=3
                                    10
                                                              k=4                                                                                                                                          k=4                                                                                                              7                       k=4
                                                              k=5                                                                                                                6
                                                                                                                                                                                                           k=5                                                                                                              6                       k=5
                                        8                     k=6                                                                                                                                          k=6                                                                                                              5
                                                                                                                                                                                                                                                                                                                                                    k=6
                                                              k=8                                                                                                                                          k=8                                                                                                                                      k=8
                                        6                     k=10                                                                                                               4                         k=10                                                                                                             4                       k=10
                                                                                                                                                                                                                                                                                                                            3
                                        4
                                                                                                                                                                                 2                                                                                                                                          2
                                        2                                                                                                                                                                                                                                                                                   1
                                              2       3        4       5       6        7       8       9       10 11 12 13 14                                                             2       3        4       5       6       7       8       9       10 11 12 13 14                                                          2       3        4       5       6       7   8   9   10 11 12 13 14
                                                                       Projection Dimension                                                                                                                         Projection Dimension                                                                                                                     Projection Dimension

                                                                                                        (b) Novelty is almost invariant to fluctuations in k
                                                                                       MBPP-New                                                                                                                         MBPP-New (Filtered)                                                                                                              MBPP-New (Reformatted)
Entropy Relative to MBPP-Original




                                                                                                                                               Entropy Relative to MBPP-Original




                                                                                                                                                                                                                                                                                        Entropy Relative to MBPP-Original
                                    4.0

                                    3.5                                                                                                                                            4                                                                                                                                        4
                                    3.0

                                    2.5                                                                                                                                            3                                                                                                                                        3
                                                                                                                 min_dist=0.0                                                                                                                               min_dist=0.0                                                                                                                 min_dist=0.0
                                    2.0
                                                                                                                 min_dist=0.05                                                     2
                                                                                                                                                                                                                                                            min_dist=0.05                                                   2
                                                                                                                                                                                                                                                                                                                                                                                         min_dist=0.05
                                    1.5                                                                          min_dist=0.1                                                                                                                               min_dist=0.1                                                                                                                 min_dist=0.1
                                    1.0                                                                          min_dist=0.2                                                                                                                               min_dist=0.2                                                                                                                 min_dist=0.2
                                                                                                                 min_dist=0.3                                                      1                                                                        min_dist=0.3                                                    1                                                            min_dist=0.3
                                    0.5
                                                                                                                 min_dist=0.5                                                                                                                               min_dist=0.5                                                                                                                 min_dist=0.5
                                                  2       3       4        5       6        7       8       9    10 11 12 13 14                                                            2       3        4       5       6       7       8       9       10 11 12 13 14                                                          2       3        4       5       6       7   8   9   10 11 12 13 14
                                                                           Projection Dimension                                                                                                                     Projection Dimension                                                                                                                     Projection Dimension

                                                                               (c) Diversity is almost invariant to fluctuations in n_neighbors
                                                                       MBPP-New                                                                                                                                MBPP-New (Filtered)                                                                                                                   MBPP-New (Reformatted)
                                                                                                                                                                                                                                                                                                                         10
Novelty Relative to MBPP Original




                                                                                                                                         Novelty Relative to MBPP Original




                                                                                                                                                                                                                                                                                     Novelty Relative to MBPP Original




                                    14
                                                              min_dist=0.0                                                                                                   10
                                                                                                                                                                                                           min_dist=0.0                                                                                                                             min_dist=0.0
                                                              min_dist=0.05                                                                                                                                min_dist=0.05                                                                                                     8
                                                                                                                                                                                                                                                                                                                                                    min_dist=0.05
                                    12                        min_dist=0.1                                                                                                         8                       min_dist=0.1                                                                                                                             min_dist=0.1
                                    10                        min_dist=0.2                                                                                                                                 min_dist=0.2                                                                                                                             min_dist=0.2
                                                              min_dist=0.3                                                                                                         6                       min_dist=0.3                                                                                                      6
                                                                                                                                                                                                                                                                                                                                                    min_dist=0.3
                                        8                     min_dist=0.5                                                                                                                                 min_dist=0.5                                                                                                                             min_dist=0.5
                                                                                                                                                                                   4                                                                                                                                         4
                                        6

                                        4
                                                                                                                                                                                   2                                                                                                                                         2
                                        2

                                              2       3        4       5       6        7       8       9       10 11 12 13 14                                                                 2   3        4       5       6       7       8       9       10 11 12 13 14                                                              2   3        4       5       6       7   8   9   10 11 12 13 14
                                                                       Projection Dimension                                                                                                                         Projection Dimension                                                                                                                     Projection Dimension

    (d) The novelty changes by a similar amount for all benchmarks as n_neighbors
    changes
                                                                       MBPP-New                                                                                                                                 MBPP-New (Filtered)                                                                                                                   MBPP-New (Reformatted)
Entropy Relative to MBPP-Original




                                                                                                                                         Entropy Relative to MBPP-Original




                                                                                                                                                                                                                                                                                     Entropy Relative to MBPP-Original




                                                                                                                                                                                                                                                                                                                         8
                                    6
                                                              n_neighbors=15                                                                                                 8                             n_neighbors=15                                                                                                                           n_neighbors=15
                                                              n_neighbors=30                                                                                                 7                             n_neighbors=30                                                                                                7                          n_neighbors=30
                                    5                         n_neighbors=50                                                                                                 6
                                                                                                                                                                                                           n_neighbors=50                                                                                                6                          n_neighbors=50
                                                              n_neighbors=80                                                                                                                               n_neighbors=80                                                                                                5
                                                                                                                                                                                                                                                                                                                                                    n_neighbors=80
                                    4
                                                              n_neighbors=100                                                                                                5
                                                                                                                                                                                                           n_neighbors=100                                                                                                                          n_neighbors=100
                                    3                         n_neighbors=150                                                                                                4                             n_neighbors=150                                                                                               4                          n_neighbors=150
                                                                                                                                                                             3                                                                                                                                           3
                                    2
                                                                                                                                                                             2                                                                                                                                           2
                                    1
                                                                                                                                                                             1                                                                                                                                           1

                                              2       3       4        5       6        7       8       9       10   11   12   13   14                                                     2       3        4       5       6       7       8       9       10   11   12   13   14                                                  2       3        4       5       6       7   8   9   10   11   12   13   14
                                                                       Projection Dimension                                                                                                                         Projection Dimension                                                                                                                     Projection Dimension

                          (e) Diversity changes by a similar amount for all benchmarks as min_dist changes
                                                                          MBPP-New                                                                                                                              MBPP-New (Filtered)                                                                                                                    MBPP-New (Reformatted)
                                    20.0
Novelty Relative to MBPP Original




                                                                                                                                               Novelty Relative to MBPP Original




                                                                                                                                                                                                                                                                                        Novelty Relative to MBPP Original




                                                                  n_neighbors=15                                                                                                   12                       n_neighbors=15                                                                                                  12                       n_neighbors=15
                                    17.5                          n_neighbors=30                                                                                                                            n_neighbors=30                                                                                                                           n_neighbors=30
                                    15.0                          n_neighbors=50                                                                                                   10                       n_neighbors=50                                                                                                  10                       n_neighbors=50
                                    12.5
                                                                  n_neighbors=80                                                                                                       8
                                                                                                                                                                                                            n_neighbors=80                                                                                                                           n_neighbors=80
                                                                                                                                                                                                                                                                                                                                8
                                                                  n_neighbors=100                                                                                                                           n_neighbors=100                                                                                                                          n_neighbors=100
                                    10.0                          n_neighbors=150                                                                                                      6                    n_neighbors=150                                                                                                     6                    n_neighbors=150
                                        7.5
                                                                                                                                                                                       4                                                                                                                                        4
                                        5.0
                                                                                                                                                                                       2                                                                                                                                        2
                                        2.5

                                                  2       3        4       5       6        7       8       9    10 11 12 13 14                                                                2       3        4       5       6       7       8       9    10 11 12 13 14                                                             2       3        4       5       6   7   8   9   10 11 12 13 14
                                                                           Projection Dimension                                                                                                                         Projection Dimension                                                                                                                 Projection Dimension

                                    (f) Novelty changes by a similar amount for all benchmarks as min_dist changes

                                                                               Figure 6: Sensitivity analysis across all hyperparameters.
Novelty Relative to LeetCode Original                                                    all-mpnet-base-v2                                                         multi-qa-mpnet-base-dot-v1                                      nli-mpnet-base-v2
                                                                        MBPP-New (Reformatted)                                                     MBPP-New (Reformatted)                                         MBPP-New (Reformatted)
                                        8                               MBPP-Hard (Reformatted)                                                    MBPP-Hard (Reformatted)                                        MBPP-Hard (Reformatted)
                                        6

                                        4

                                        2

                                        0
                                                            2               4        6            8          10        12            14    2           4           6           8           10      12    14   2       4        6          8            10   12   14
                                                                                             Dimension                                                                     Dimension                                                  Dimension

                                                                                                                            (a) Novelty of datasets for various embedding models
                                                                                             all-mpnet-base-v2                                                      multi-qa-mpnet-base-dot-v1                                     nli-mpnet-base-v2
                                                                          MBPP-New (Reformatted)                                                    MBPP-New (Reformatted)                                        MBPP-New (Reformatted)
Diversity Relative to MBPP Original




                                            2.0
                                                                          MBPP-Hard (Reformatted)                                                   MBPP-Hard (Reformatted)                                       MBPP-Hard (Reformatted)
                                            1.5

                                            1.0

                                            0.5

                                            0.0

                                            0.5
                                                                    2           4        6            8           10        12        14       2           4           6           8        10      12   14   2       4        6           8           10   12   14
                                                                                                 Dimension                                                                  Dimension                                                  Dimension

                                                                                                                        (b) Diversity of datasets for various embedding models


                                                                                         Figure 7: Embedding model invariance analysis for novelty and diversity metrics


                                                                                                                                                                                       E        Analysis of Filtered-Out Problems
                                                                                                                                                                                   In general, we do not observe strong systematic
                                                                                                                                                                                   biases in the topics that survive the filtering stage.
                              Percentage of Generated Dataset (%)




                                                                    70
                                                                                                                                                                                   The retained dataset continues to cover the ma-
                                                                    60
                                                                    50
                                                                                                                                                                                   jor categories present in the seed distribution, sug-
                                                                    40                                                                                                             gesting that the filtering process primarily removes
                                                                    30                                                                                                             invalid or inconsistent generations rather than col-
                                                                     5                                                                                                             lapsing the underlying problem space. However,
                                                                     4               % Passed
                                                                                     % Failed                                                                                      we observe that certain classes of generated prob-
                                                                     3
                                                                     2               % Erred                                                                                       lems are disproportionately filtered out, and these
                                                                     1               % Unparsable                                                                                  cases also provide additional insight into model
                                                                     0                                                                                                             behavior under compositional generation and veri-
                                                                            0                1               2                   3         4                   5
                                                                                    Number of Code Feedback Iterations                                                             fication constraints.
                                                                                                                                                                                      The first such category consists of deep
                                                                        Figure 8: Self-verification for MBPP-                                                                      crossover compositions, where crossover is re-
                                                                        New
                                                                                                                                                                                   peatedly applied to previously crossover-generated
                              Percentage of Generated Dataset (%)




                                                                    100                                                                                                            tasks. These produce highly compositional prob-
                                                                                                                                                                                   lems with tightly interacting constraints, which are
                                                                    80
                                                                                                                                                                                   difficult for the generator model to satisfy jointly
                                                                    60               % Passed                                                                                      while also producing consistent test cases. A sec-
                                                                    20               % Failed
                                                                                     % Erred                                                                                       ond category involves numerically sensitive prob-
                                                                    10
                                                                                     % Unparsable                                                                                  lems, such as recurrence-based or combinatorial
                                                                     6                                                                                                             computation tasks (e.g., computing the nth Delan-
                                                                     4
                                                                                                                                                                                   noy number), where models often produce correct
                                                                     2
                                                                                                                                                                                   symbolic solutions but struggle to construct test
                                                                     0
                                                                            0                1               2                   3         4                   5                   cases with exact ground-truth values.
                                                                                    Number of Code Feedback Iterations
                                                                                                                                                                                      Across these filtered categories, we identify
                                                                        Figure 9: Self-verification for Leetcode-                                                                  three recurring patterns that characterize model
                                                                        New                                                                                                        behavior:
                                                                                                                                                                                      Generation Outpacing Verification: To pass
                                                                                                                                                                                   InfoSynth’s pipeline, models must generate both
                                                                                                                                                                                   code and test cases. In failed crossover problems, a
frequent failure mode is that the LLM generates a           solutions
correct solution but fails to generate tests with the       o r o u t p u t s . Only one new
correct input-output relationship. This reveals an          i n s t r u c t i o n i s allowed .
asymmetry in capability: models can often reason            Original Question : { i n s t r u c t i o n }
abstractly about a class of solutions, but struggle         New Q u e s t i o n :
to instantiate that reasoning into precise, verifiable
test cases.                                                 % medium
   Failure to Holistically Reason: Crossover prob-          P l e a s e c r e a t e a new programming
lems introduce multiple interacting constraints. We         p r o b l e m o f t h e same d i f f i c u l t y a s
find that models frequently attempt to satisfy these          the
sequentially rather than jointly. While this strategy       g i v e n programming t e s t q u e s t i o n .
can work for simpler tasks, it becomes brittle when         The new p r o b l e m s h o u l d be
constraints interact, as locally consistent decisions       conceptually
do not guarantee global correctness. This behavior          s i m i l a r to the given question ,
is a key contributor to failure in deep crossover           but should not simply paraphrase
settings.                                                   it .
   Superficial Debugging Loops: Although iter-              Do n o t p r o v i d e any h i n t s ,
ative execution feedback (Section 5.3) generally            s o l u t i o n s o r o u t p u t s . Only one
improves performance, it can stall on deeply nested         new i n s t r u c t i o n i s a l l o w e d .
crossover problems. The model often becomes                 Original Question : { i n s t r u c t i o n }
trapped in a “local minimum” where it focuses on            New Q u e s t i o n :
surface-level corrections such as syntax, format-
ting, or minor edge-case fixes. Even with multiple          % hard
feedback iterations and access to its full interac-         Please i n c r e a s e the d i f f i c u l t y of
tion history, it fails to reliably revisit or reframe the     t h e g i v e n programming t e s t
underlying solution strategy. This suggests a limi-         question a bit .
tation in stepping back to higher-level abstraction         Do n o t p r o v i d e any h i n t s ,
once an initial solution trajectory is committed.           s o l u t i o n s o r o u t p u t s . Only one
   In summary, the filtering process not only shapes        new i n s t r u c t i o n i s a l l o w e d .
the final dataset but also highlights systematic            Original Question : { i n s t r u c t i o n }
stress points in current LLMs. These observations           New Q u e s t i o n :
suggest that the most frequently filtered problems
are precisely those that require tightly coupled rea-       F.2   Crossover Prompt
soning across solution generation and executable
verification, providing a structured view into where        I w i l l p r o v i d e you w i t h a s e t o f
current models remain fragile.                              c o d i n g q u e s t i o n s . P l e a s e g i v e me
                                                            a new c o d i n g
F     Problem Generation Pipeline Prompts                   q u e s t i o n t h a t combines core
                                                            c o n c e p t s from two o r more o f t h e
We note that our prompts share some similarity
                                                            given questions .
with those used by Majumdar et al. (2024).
                                                            P l e a s e e n s u r e t h a t t h e new
F.1   Mutation Prompts                                      q u e s t i o n i s n o v e l and d o e s n o t
                                                            simply paraphrase
% easy                                                      any o f t h e p r o b l e m s I am g i v i n g
Please decrease the d i f f i c u l t y of                  you . Do n o t i n c l u d e any e x t r a
  t h e g i v e n programming t e s t                       information
question a bit .                                            t h a t would h e l p a t e s t − t a k e r
The new p r o b l e m s h o u l d be                        o t h e r than t h e problem s t a t e m e n t
conceptually s i m i l a r to the given                     itself .
  question ,
but should not simply paraphrase                            Question 1:
i t . Do n o t p r o v i d e any h i n t s ,                { i n s t r u c t i o n 1}
                                                            d e f add ( a , b ) :
Question 2:                                                         ' ' ' R e t u r n s t h e sum o f a and b
{ i n s t r u c t i o n 2}                                         . ' ' '
...                                                                return a + b
                                                            < | S o l u t i o n End | >
New Q u e s t i o n :
                                                            <| T e s t Begin | >
F.3   Solution & Test Generation Prompt                     from s o l u t i o n i m p o r t add
                                                            def test_add_positive_numbers ( ) :
We note that our prompts are similar to those used
                                                                   a s s e r t add ( 2 , 3 ) == 5
by Xu et al. (2025).
                                                            def test_add_with_zero ( ) :
You a r e an e x p e r t i n P y t h o n                           a s s e r t add ( 0 , 5 ) == 5
coding .                                                           a s s e r t add ( 5 , 0 ) == 5
## Task :                                                   def test_add_negative_numbers ( ) :
P l e a s e a n s w e r t h e q u e s t i o n and                  a s s e r t add ( − 1 , −1) == −2
generate unit t e s t s to verify                           def test_add_mixed_sign_numbers ( )
your answer .                                               :
                                                                   a s s e r t add ( − 1 , 3 ) == 2
## O u t p u t F o r m a t :                                < | T e s t End | >
Your s o l u t i o n and u n i t t e s t s
s h o u l d be p r e s e n t e d i n t h e f o r m a t      ## Q u e s t i o n :
  within the                                                { problem }
s p e c i f i e d s e c t i o n s below . E n s u r e
your code i s w i t h i n code b l o c k s .                F.4   Solution & Test Generation with Iterative
For t h e                                                         Feedback Prompt
t e s t s , u s e p y t e s t s t y l e by
defining individual test                                    You a r e an e x p e r t i n P y t h o n
functions ( without                                         coding .
c l a s s e s ) and u s i n g a s s e r t                   ## Task :
s t a t e m e n t s . Your t e s t s s h o u l d be         P l e a s e a n s w e r t h e q u e s t i o n and
implementation                                              generate unit t e s t s to verify
i n d e p e n d e n t . E n s u r e t h a t you             y o u r a n s w e r . The
i n c l u d e t h e <| S o l u t i o n Begin | > ,          e n t i r e c ha t h i s t o r y of your
< | S o l u t i o n End | > , < | T e s t B e g i n | > ,   previous attempts to generate
  and < | T e s t End | > t a g s a s                       q u e s t i o n s and u n i t
d e p i c t e d . The                                       t e s t s i s p r e s e n t e d below i n t h e "
s o l u t i o n f u n c t i o n must be named               Chat H i s t o r y " s e c t i o n , along with
solution .                                                    the output
                                                            of running your s o l u t i o n a g a i n s t
<| S o l u t i o n Begin | >                                your t e s t s i n a code e x e c u t i o n
{ S o l u t i o n Code i n P y t h o n }                    environment .
< | S o l u t i o n End | >                                 P l e a s e m o d i f y o n l y y o u r t e s t s and
                                                            / o r s o l u t i o n t o be more c o r r e c t .
<| T e s t Begin | >
{ U n i t T e s t Code i n P y t h o n }                    ## O u t p u t F o r m a t :
< | T e s t End | >                                         <Same a s " O u t p u t F o r m a t " s e c t i o n
                                                            above >
## Example
Below i s an e x a m p l e o u t p u t f o r m a t          ## C h a t H i s t o r y :
 implementing a simple a + b                                Attempt 1 S o l u t i o n :
function .                                                  { attempt 1 solution }
<| S o l u t i o n Begin | >
A t t e m p t 1 Code E x e c u t i o n O u t p u t :      an empty l i s t when t h e r e a r e no
{ a t t e m p t 1 code o u t p u t }                      s t u d e n t s o r when t h e i n p u t
                                                          d i c t i o n a r y i s empty .
Attempt 2 S o l u t i o n :
                                                          Leetcode-New Dataset Original Problem:
{ Attempt 2 s o l u t i o n }
                                                          A l i c e and Bob a r e e n g a g e d i n a
A t t e m p t 2 Code E x e c u t i o n O u t p u t :      s t r a t e g i c game on an i n f i n i t e 2D
{ a t t e m p t 2 code o u t p u t }                      p l a n e w i t h n p o i n t s p r o v i d e d by
...                                                       t h e i r c o o r d i n a t e s i n two i n t e g e r
                                                          a r r a y s , xCoord and yCoord . They
## Q u e s t i o n :                                      take turns , s t a r t i n g with Alice ,
{ problem }                                               a t t a c k i n g a p o i n t on t h e p l a n e t o
                                                            capture it , with the c o n d i t i o n
F.5   Postprocessing Prompts                              t h a t once a p o i n t i s a t t a c k e d , i t
                                                            i s removed p e r m a n e n t l y from t h e
You a r e an e x p e r t i n P y t h o n                  game , and t h e y h a v e t o remove
c o d i n g . Here i s a c o d i n g p r o b l e m        exactly 1 point per turn .
with a s s o c i a t e d t e s t cases .
P l e a s e r e p h r a s e t h e q u e s t i o n so      The w i n n e r i s t h e p l a y e r who
i t d e s c r i b e s what t h e u s e r s h o u l d      e i t h e r removes t h e p o i n t t h a t
  o u t p u t f o r edge − c a s e s w i t h o u t        l e a v e s no r e c t a n g l e c a p a b l e o f
changing the essence of the                               being formed u s i n g t h e r e m a i n i n g
p r o b l e m . Add a s l i t t l e                       p o i n t s on t h e i r t u r n o r c a n f o r c e
information as possible , only                              t h e s c e n a r i o by o p t i m a l p l a y
d e s c r i b i n g what t h e u s e r s h o u l d        s u c h t h a t t h e o p p o n e n t h a s no
o u t p u t f o r edge − c a s e s t h a t c a n n o t    s u c h move l e f t on t h e i r
  be i n f e r r e d from t h e p r o b l e m             subsequent turns .
d e s c r i p t i o n . Do n o t i n c l u d e
anything except for the rewritten                         Given t h e a r r a y s xCoord and
  p r o b l e m i n y o u r r e s p o n s e and do        yCoord , a l o n g w i t h k n o w l e d g e o f
not include the t e s t cases .                           optimal s t r a t e g i e s for both
Question :                                                p l a y e r s , d e t e r m i n e i f A l i c e , who
{ question }                                              s t a r t s t h e game , c a n a l w a y s
Tests :                                                   g u a r a n t e e a win . R e t u r n t r u e i f
{ tests }                                                 Alice has a winning s t r a t e g y , or
                                                          f a l s e i f Bob c a n a l w a y s f o r c e a
G     Example of Post-processed Problems                  win e v e n w i t h A l i c e s t a r t i n g
                                                          first .
MBPP-New Dataset Original Problem:
                                                          Post-Processed Version:
Write a f u n c t i o n t h a t f i l t e r s a
l i s t of usernames s t o r e d in a                     A l i c e and Bob a r e p l a y i n g a
d i c t i o n a r y , r e t u r n i n g only those        s t r a t e g i c game on an i n f i n i t e 2D
a s s o c i a t e d w i t h s t u d e n t s who f a l l   p l a n e w i t h n p o i n t s d e f i n e d by
  w i t h i n a s p e c i f i e d age range .             t h e i r c o o r d i n a t e s i n two i n t e g e r
                                                          a r r a y s , xCoord and yCoord . They
Post-Processed Version:
                                                          a l t e r n a t e l y take turns , with
Write a f u n c t i o n t h a t f i l t e r s a           Alice s t a r t i n g f i r s t , to attack
l i s t of usernames s t o r e d in a                     and p e r m a n e n t l y remove e x a c t l y
d i c t i o n a r y , r e t u r n i n g only those        one p o i n t a t a t i m e . The
a s s o c i a t e d w i t h s t u d e n t s who f a l l   objective is for a player to
  w i t h i n a s p e c i f i e d age range .             l e a v e no p o s s i b i l i t y o f f o r m i n g a
Ensure t h a t the f u n c t i o n r e t u r n s            r e c t a n g l e u s i n g any f o u r o f t h e
r e m a i n i n g p o i n t s . A p l a y e r wins          the p r o f i l e only c o n t a i n s
i f they achieve t h i s or i f they                      lowercase alphabetic characters .
c a n f o r c e a s c e n a r i o where t h e             I f t h e r e a r e no v a l i d p r o f i l e s
o p p o n e n t h a s no s u c h moves l e f t .          t h a t match t h e c r i t e r i a , t h e
Given t h e a r r a y s xCoord and                        f u n c t i o n s h o u l d r e t u r n an empty
yCoord , d e t e r m i n e i f A l i c e h a s a          list .
guaranteed winning s t r a t e g y .
Return t r u e i f A l i c e can always                   Hard M u t a t i o n :
win , and f a l s e i f Bob c a n a l w a y s             Create a function to f i l t e r user
f o r c e a win o r i f t h e r e a r e no                p a s s w o r d s from a d i c t i o n a r y ,
p o i n t s to s t a r t with .                           r e t u r n i n g only those t h a t are
                                                          v a l i d f o r s t u d e n t s whose
                                                          d i m e n s i o n s ( h e i g h t , w i d t h , and
H     Examples of Generated Problems                      weight ) are within a given range .
We note that for conciseness, the examples shown            Each v a l i d p a s s w o r d must i n c l u d e
in this section are before the postprocessing step.         a t l e a s t one u p p e r c a s e l e t t e r ,
In this section, we illuminate the different mecha-       one l o w e r c a s e l e t t e r , one d i g i t ,
nisms through which mutation and crossover gen-           and one s p e c i a l c h a r a c t e r . E n s u r e
erate interesting problems.                                 the solution appropriately
                                                          h a n d l e s and r e t u r n s an empty
H.1    Mutation Operation: Adding or                      d i c t i o n a r y f o r c a s e s where no
       Removing Constraints                               users are provided or a l l e n t r i e s
This example shows how mutation creates three               a r e i n v a l i d due t o d i m e n s i o n o r
variants of the question by adding requirements           password c r i t e r i a .
or removing constraints from the problem. We
can see that all three problems require similar           H.2   Mutation Operation Example: Creative
conceptual understanding, but the harder ones                   Modification
simply require more code or bookkeeping.                  This example shows how mutation creates three
                                                          variants of the question by creatively modifying
Original Question :                                       the central idea of the problem itself. This differs
Write a f u n c t i o n to f i l t e r the                from the previous example; in this case, the harder
h e i g h t and w i d t h o f s t u d e n t s             questions require a fundamental understanding of
which a r e s t o r e d i n a d i c t i o n a r y .       new topics.

Easy M u t a t i o n :                                    Original Question :
Write a f u n c t i o n t h a t f i l t e r s a           Write a f u n c t i o n to f i n d the
l i s t of usernames s t o r e d in a                     perimeter of a r e c t a n g l e .
d i c t i o n a r y , r e t u r n i n g only those
a s s o c i a t e d w i t h s t u d e n t s who f a l l   Easy M u t a t i o n :
  w i t h i n a s p e c i f i e d age range .             Write a f u n c t i o n to f i n d the area
Ensure t h a t the f u n c t i o n r e t u r n s           of a r e c t a n g l e .
an empty l i s t when t h e r e a r e no                  Medium M u t a t i o n :
s t u d e n t s o r when t h e i n p u t                  Write a f u n c t i o n to c a l c u l a t e the
d i c t i o n a r y i s empty .                             area of a t r a p e z o i d given i t s
                                                          b a s e l e n g t h s and h e i g h t .
Medium M u t a t i o n :
Create a function that f i l t e r s                      Hard M u t a t i o n :
u s e r p r o f i l e s b a s e d on a                    Write a f u n c t i o n to f i n d the area
d i c t i o n a r y . The f u n c t i o n s h o u l d       o f a rhombus g i v e n i t s d i a g o n a l s
r e t u r n a l i s t o f u s e r IDs f o r                 and v e r i f y i f t h e rhombus i s
p r o f i l e s where t h e a g e i s w i t h i n         a l s o a s q u a r e by u s i n g i t s s i d e
a s p e c i f i e d r a n g e ( i n c l u s i v e ) and   lengths .
H.3   Crossover Operation: Combining                   o f moves made d u r i n g t h e game
      Concepts                                         t h a t A l i c e can achieve , assuming
This example shows how crossover creates an            both p l a y e r s play optimally .
interesting, novel question by combining two           Note t h a t i n one move , a c h e s s
unrelated concepts. A key difference between           knight has e i g h t p o s s i b l e
crossover and mutation is that crossover does not      p o s i t i o n s i t c a n move t o , a s
introduce any new concepts or content into the         i l l u s t r a t e d below . Each move i s
generated problem as it draws from existing ones.      two c e l l s i n a c a r d i n a l d i r e c t i o n
This demonstrates the necessity of combining           , t h e n one c e l l i n an o r t h o g o n a l
mutation and crossover into one pipeline; mutation     direction .
introduces new concepts into the dataset while
                                                       Question 2:
crossover takes existing concepts and uses them to
                                                       You a r e g i v e n an a r r a y p o i n t s
create richer problems.
                                                       where p o i n t s [ i ] = [ x i , y i ]
                                                       r e p r e s e n t s the c o o r d i n a t e s of a
Seed Problems:
                                                       p o i n t on an i n f i n i t e p l a n e .
Question 1:                                            Your t a s k i s t o f i n d t h e maximum
T h e r e i s a 50 x 50 c h e s s b o a r d            area of a r e c t a n g l e t h a t :
w i t h one k n i g h t and some pawns on
  i t . You a r e g i v e n two i n t e g e r s        Can be f o r m e d u s i n g f o u r o f t h e s e
kx and ky where ( kx , ky ) d e n o t e s                p o i n t s as i t s corners .
t h e p o s i t i o n o f t h e k n i g h t , and a    Does n o t c o n t a i n any o t h e r p o i n t
  2D a r r a y p o s i t i o n s where                 i n s i d e o r on i t s b o r d e r .
p o s i t i o n s [ i ] = [ xi , y i ] d e n o t e s   Has i t s e d g e s p a r a l l e l t o t h e
t h e p o s i t i o n o f t h e pawns on t h e         axes .
chessboard .
A l i c e and Bob p l a y a t u r n − b a s e d        R e t u r n t h e maximum a r e a t h a t you
game , where A l i c e g o e s f i r s t . I n         c a n o b t a i n o r −1 i f no s u c h
each player ' s t u r n :                              rectangle is possible .
                                                       Crossover Generated Question:
The p l a y e r s e l e c t s a pawn t h a t
s t i l l e x i s t s on t h e b o a r d and           A l i c e and Bob a r e p l a y i n g a
c a p t u r e s i t with the knight in                 s t r a t e g i c game on an i n f i n i t e 2D
t h e f e w e s t p o s s i b l e moves . Note         p l a n e w i t h n p o i n t s d e f i n e d by
t h a t t h e p l a y e r c a n s e l e c t any        t h e i r c o o r d i n a t e s i n two i n t e g e r
pawn , i t m i g h t n o t be one t h a t              a r r a y s , xCoord and yCoord . They
c a n be c a p t u r e d i n t h e l e a s t           a l t e r n a t e l y take turns , with
number o f moves .                                     Alice s t a r t i n g f i r s t , to attack
In the process of c a p t u r i n g the                and p e r m a n e n t l y remove e x a c t l y
s e l e c t e d pawn , t h e k n i g h t may           one p o i n t a t a t i m e . The
p a s s o t h e r pawns w i t h o u t                  objective is for a player to
c a p t u r i n g them . Only t h e s e l e c t e d    l e a v e no p o s s i b i l i t y o f f o r m i n g a
  pawn c a n be c a p t u r e d i n t h i s              r e c t a n g l e u s i n g any f o u r o f t h e
turn .                                                 r e m a i n i n g p o i n t s . A p l a y e r wins
                                                       i f they achieve t h i s or i f they
A l i c e i s t r y i n g t o maximize t h e           c a n f o r c e a s c e n a r i o where t h e
sum o f t h e number o f moves made                    o p p o n e n t h a s no s u c h moves l e f t .
by b o t h p l a y e r s u n t i l t h e r e a r e     Given t h e a r r a y s xCoord and
no more pawns on t h e b o a r d ,                     yCoord , d e t e r m i n e i f A l i c e h a s a
w h e r e a s Bob t r i e s t o m i n i m i z e        guaranteed winning s t r a t e g y .
them .                                                 Return t r u e i f A l i c e can always
R e t u r n t h e maximum t o t a l number             win , and f a l s e i f Bob c a n a l w a y s
f o r c e a win o r i f t h e r e a r e no             Question: Write a function that takes a list of
p o i n t s to s t a r t with .                        strings and returns the second shortest string that
                                                       contains all vowels, sorted alphabetically. If no
H.4   Crossover Operation: Multistep                   such string exists, return an empty string.
      Reasoning                                        Initial Solution:
This example shows how crossover sometimes             def s o l u t i o n ( s t r i n g s ) :
creates problems that require multistep reasoning.         """
The new problem effectively requires a test-taker          Returns the second s h o r t e s t
to solve both the seed problems.                           s t r i n g c o n t a i n i n g a l l vowels ,
                                                             sorted alphabetically .
Seed Problems:                                             """
Question 1:                                                all_vowels = s e t ( ' aeiou ' )
Write a python f u n c t i o n to f i n d
t h e sum o f f o u r t h power o f f i r s t                # Fi l t er strings that contain
n odd n a t u r a l numbers .                                  a l l vowels
                                                             f i l t e r e d _ s t r i n g s = [ s for s
Question 2:                                                  i n s t r i n g s i f a l l _ v o w e l s <=
Write a python f u n c t i o n to f i n d                    set ( s ) ]
t h e sum o f x o r o f a l l p a i r s o f
numbers i n t h e g i v e n a r r a y .                      # S o r t them by l e n g t h f i r s t
Crossover Generated Question:                                and t h e n a l p h a b e t i c a l l y
                                                             f i l t e r e d _ s t r i n g s . s o r t ( key =
Write a python f u n c t i o n to                            lambda x : ( l e n ( x ) , x ) )
compute t h e combined m e t r i c o f
two p r o p e r t i e s f o r a g i v e n a r r a y         # Return the second s h o r t e s t
of i n t e g e r s :                                        s t r i n g o r empty s t r i n g i f i t
                                                            doesn ' t e x i s t
1 . The sum o f t h e f o u r t h power o f                 return f i l t e r e d _ s t r i n g s [1] if
  t h e f i r s t ' k ' odd numbers from                      len ( f i l t e r e d _ s t r i n g s ) > 1
the array .                                                 else ' '
2 . The sum o f t h e b i t w i s e XOR o f            { Tests Omitted f o r Conciseness }
a l l p a i r s o f numbers f o r m e d by
s e l e c t i n g one e l e m e n t from t h e         Solution after First Feedback iteration:
f i r s t ' k ' e v e n numbers and one
e l e m e n t from t h e l a s t ' k '                 Let ' s r e v i s e t h e t e s t c a s e s t o
elements in the array .                                ensure they c o r r e c t l y t e s t the
                                                       f u n c t i o n ' s b e h a v i o r and c h e c k t h e
The f u n c t i o n s h o u l d t a k e two              s o l u t i o n i m p l e m e n t a t i o n and i t s
arguments − the array of i n t e g e r s               h a n d l i n g o f e d g e c a s e s . F i r s t , we
  and an i n t e g e r ' k ' . E n s u r e t h a t     ' l l make s u r e t h e s o l u t i o n
' k ' i s l e s s than or equal to h a l f             properly handles s t r i n g s with
  t h e l e n g t h o f t h e a r r a y and t h a t    v a r y i n g c a s e s ( u p p e r c a s e and
  the array contains a s u f f i c i e n t             l o w e r c a s e ) and t h a t i t v e r i f i e s
number o f odd and e v e n numbers .                   t h e f u l l vowel s e t i n a c a s e −
                                                       i n s e n s i t i v e manner . A d d i t i o n a l l y ,
                                                         let ' s a d j u s t the t e s t s to cover
I   Example of Chain-of-Thought Thinking
                                                       more s c e n a r i o s and b e t t e r r e f l e c t
This example shows how the model is able to              the conditions described in the
reason about why its solution and tests are erroring   q u e s t i o n . Here ' s t h e r e v i s e d
due to receiving feedback from the code execution      v e r s i o n o f t h e s o l u t i o n and u n i t
environment.                                           tests :
{ S o l u t i o n s Omitted f o r                        − If multiple techniques are
Conciseness }                                            e s s e n t i a l ( e . g . , DP + B i t m a s k ) ,
{ Tests Omitted f o r Conciseness }                      include both .
                                                         − Do NOT e x c e e d 3 t o p i c s ; o r d e r
Solution after Second Feedback iteration:                them by i m p o r t a n c e .
We n e e d t o e n s u r e t h a t o u r                 − I f nothing f i t s , choose the
s o l u t i o n and t e s t s a l i g n                  c l o s e s t g e n e r a l t a g ( e . g . , " Graph
c o r r e c t l y w i t h t h e t a s k . Let ' s        " , " A r r a y " , " Math " ) , n e v e r i n v e n t
r e f i n e b o t h t h e s o l u t i o n and t h e        tags .
t e s t s so t h a t t he y p as s c o r r e c t l y
  a c c o r d i n g t o t h e given problem              T o p i c Bank ( a l l o w e d v a l u e s o n l y ) :
s t a t e m e n t . The s o l u t i o n n e e d s t o    A r r a y ; S t r i n g ; Hash T a b l e ;
e n s u r e t h a t we f i l t e r s t r i n g s         Dynamic Programming ; Math ;
c o n t a i n i n g a l l v o w e l s i n any c a s e    S o r t i n g ; Greedy ; Depth − F i r s t
, s o r t them , and r e t u r n t h e                   Search ; Binary Search ; Database ;
s e c o n d s h o r t e s t . The t e s t c a s e s      Matrix ; Tree ; Breadth − F i r s t
should r e f l e c t t h i s logic .                     S e a r c h ; B i t M a n i p u l a t i o n ; Two
                                                         P o i n t e r s ; P r e f i x Sum ; Heap (
Here ' s t h e r e f i n e d s o l u t i o n and         P r i o r i t y Queue ) ; S i m u l a t i o n ;
tests :                                                  B i n a r y T r e e ; Graph ; S t a c k ;
                                                         C o u n t i n g ; S l i d i n g Window ; D e s i g n ;
{ S o l u t i o n s Omitted f o r                          E n u m e r a t i o n ; B a c k t r a c k i n g ; Union
Conciseness }                                              F i n d ; L i n k e d L i s t ; Number T h e o r y
{ Tests Omitted f o r Conciseness }                      ; Ordered Set ; Monotonic Stack ;
                                                         Segment T r e e ; T r i e ; C o m b i n a t o r i c s
                                                         ; B i t m a s k ; D i v i d e and Conquer ;
J   Topic-Labeling Prompt                                Queue ; R e c u r s i o n ; Geometry ;
                                                         Binary Indexed Tree ; Memoization ;
You a r e a p r e c i s e t a g g e r f o r                Hash F u n c t i o n ; B i n a r y S e a r c h
coding i n t e r v i e w problems .                      Tree ; S h o r t e s t Path ; S t r i n g
                                                         Matching ; T o p o l o g i c a l S o r t ;
Given a p r o b l e m s t a t e m e n t and              R o l l i n g Hash ; Game T h e o r y ;
s o l u t i o n , c h o o s e up t o THREE               I n t e r a c t i v e ; Data Stream ;
t o p i c s from t h e bank below t h a t                M o n o t o n i c Queue ; B r a i n t e a s e r ;
best describe the core techniques                        Doubly − L i n k e d L i s t ; Randomized ;
/ d a t a s t r u c t u r e s needed to s o l v e        Merge S o r t ; C o u n t i n g S o r t ;
i t . R e t u r n JSON ONLY, no e x t r a                I t e r a t o r ; Concurrency ;
text , as :                                              P r o b a b i l i t y and S t a t i s t i c s ;
{" t o p i c s " : [ " Topic1 " , " Topic2 " ] }         Q u i c k s e l e c t ; S u f f i x Array ; Line
                                                         Sweep ; Minimum S p a n n i n g T r e e ;
                                                         Bucket S o r t ; S h e l l ; R e s e r v o i r
Rules :                                                  Sampling ; S t r o n g l y Connected
− Use EXACT s p e l l i n g s from t h e                 Component ; E u l e r i a n C i r c u i t ;
bank ( c a s e / s p a c i n g must match ) .            Radix S o r t ; R e j e c t i o n Sampling ;
− P r e f e r t h e most s p e c i f i c t a g           B i c o n n e c t e d Component
a v a i l a b l e ( e . g . , " Binary Tree "
over " Tree " , " S h o r t e s t Path " over
  " Graph " when a p p r o p r i a t e ) .               Input :
− If the solution c r i t i c a l l y                    [ Problem ]
r e l i e s on a d a t a s t r u c t u r e ( e . g . ,   { problem }
  " Heap ( P r i o r i t y Queue ) " ) ,
include i t .
[ Solution ]
{ solution }


Output :
JSON w i t h key " t o p i c s " and UP TO
3 s t r i n g s from t h e bank . No p r o s e
, no e x p l a n a t i o n s .
"""
