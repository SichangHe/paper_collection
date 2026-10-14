                                                                                                                                                   2025-11-18



                                         Scaling Generative Verifiers For Natural Language
                                         Mathematical Proof Verification And Selection
                                           Sadegh Mahdavi1,2* , Branislav Kisacanin1,3 , Shubham Toshniwal1 , Wei Du1 , Ivan Moshkov1 ,
                                                  George Armstrong1 , Renjie Liao2† , Christos Thrampoulidis2† , Igor Gitman1†
                                                              1 NVIDIA, 2 University of British Columbia, 3 Institute for AI R&D of Serbia




                                         Abstract: Large language models have achieved remarkable success on final-answer mathematical problems,
                                         largely due to the ease of applying reinforcement learning with verifiable rewards. However, the reasoning
                                         underlying these solutions is often flawed. Advancing to rigorous proof-based mathematics requires reliable
                                         proof verification capabilities. We begin by analyzing multiple evaluation setups and show that focusing on a
arXiv:2511.13027v1 [cs.AI] 17 Nov 2025




                                         single benchmark can lead to brittle or misleading conclusions. To address this, we evaluate both proof-based
                                         and final-answer reasoning to obtain a more reliable measure of model performance. We then scale two major
                                         generative verification methods (GenSelect and LLM-as-a-Judge) to millions of tokens and identify their
                                         combination as the most effective framework for solution verification and selection. We further show that
                                         the choice of prompt for LLM-as-a-Judge significantly affects the model’s performance, but reinforcement
                                         learning can reduce this sensitivity. However, despite improving proof-level metrics, reinforcement learning
                                         does not enhance final-answer precision, indicating that current models often reward stylistic or procedural
                                         correctness rather than mathematical validity. Our results establish practical guidelines for designing and
                                         evaluating scalable proof-verification and selection systems.1


                                         1. Introduction
                                         Large Language Models (LLMs) have achieved remarkable progress in mathematical reasoning tasks, reaching
                                         near-saturation on high-school competition benchmarks such as MATH [11] and AIME [22]. This success
                                         is driven in large part by the simplicity of evaluating final-answer problems: correctness can be checked
                                         automatically, either through string matching or with lightweight equivalence checks [24]. This makes such
                                         tasks well-suited for reinforcement learning with verifiable rewards (RLVR) [25], enabling steady improvements
                                         in model performance.
                                            Closer inspection, however, reveals a major gap: LLMs often arrive at correct answers through flawed
                                         reasoning [10]. Common failure modes include circular reasoning where models assume what they need to
                                         prove, pattern-matching by testing small cases rather than formal proof, adding extra assumptions to the
                                         problem, and fabricating theorems or lemmas that sound plausible but are incorrect [20]. However, advancing
                                         to harder competitions such as the IMO or USAMO requires a shift in focus: solutions demand rigorous
                                         proofs, not just final answers. Unlike final-answer verification, which can be automated through simple checks,
                                         proof verification is inherently more challenging as it requires assessing logical structure, mathematical rigor,
                                         and the validity of each reasoning step.
                                             Developing reliable verification mechanisms in this context could enable RLVR-style approaches to
                                         enhance proof generation, mirroring their demonstrated success with final-answer tasks. This motivates
                                         investigation of two critical verification settings: (1) Selection: Given multiple candidate proofs, identify the
                                         most sound one, valuable for test-time compute scaling and curating high-quality data for self-improvement
                                         or expert iteration [33, 8]. (2) Verification: Given a single proof, determine its correctness, enabling precise
                                         reward signals for policy-gradient reinforcement learning approaches such as GRPO [25]. Both settings have
                                         received substantial recent attention [18, 7], with LLM-based generative verification emerging as particularly
                                         promising [34, 14].
                                            In this work, we systematically study LLM-based proof verification and selection. In particular, our
                                         contributions are as follows:
                                           1 Code is available at https://github.com/NVIDIA-NeMo/Skills/tree/main/recipes/proof-gen-verification
                                           ∗ Work done during internship at NVIDIA. † Corresponding authors.




                                         © 2025 NVIDIA. All rights reserved.
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



   • We establish a rigorous evaluation framework that exposes significant limitations in existing datasets,
     demonstrating the necessity of a multi-faceted evaluation suite to mitigate exploitable correlations and
     avoid drawing conclusions from insufficiently sized datasets.
   • We analyze multiple variants of LLM-as-a-Judge methodologies for both proof selection and verification,
     revealing that prompt design exerts substantial influence on performance, and that reinforcement learning
     fine-tuning can effectively reduce this sensitivity.
   • We investigate diverse strategies for scaling test-time compute in proof selection, demonstrating that a
     synergistic combination of LLM-as-a-Judge with GenSelect tournaments and parallel judgments achieves
     improved compute trade-off.


2. Related Work
Test-Time Scaling for Mathematical Reasoning. Prior research has demonstrated that test-time
compute scaling substantially improves performance on mathematical reasoning tasks. Early approaches
focused on sampling multiple solution trajectories from LLMs and employing majority-voting-based selection
methods [29], while more recent breakthroughs such as long reasoning [13, 9] scale the length of chain-of-thought
reasoning within the model. Contemporary approaches involve generating multiple candidate solutions and
selecting the most promising one using a judge model through generative verification [16, 28, 7], or iteratively
refining solutions based on feedback from a judge model [19]. In this work, we build upon GenSelect [28]
and LLM-as-a-Judge [36] methodologies, combining them to achieve superior performance on mathematical
reasoning tasks, particularly those requiring formal proofs.
Mathematical Reasoning Beyond Final Answers. Recent research focuses on advancing mathematical
reasoning beyond simply producing final answers. Datasets such as PRM800K [15] and ProcessBench [35]
pioneer the training and evaluation of LLMs on process-level errors, moving past traditional final-answer-based
assessment. More recent efforts target proof-based and challenging mathematical problems, including those
from the International Mathematical Olympiad (IMO). Mahdavi et al. [20] evaluate state-of-the-art LLMs
on proof-based tasks, revealing common pitfalls such as overgeneralization from limited examples, circular
reasoning, and fabricating non-existent theorems. Dekoninck et al. [7] make a significant contribution to this
field by introducing new benchmarks for rigorously evaluating LLMs in the verification and selection of proofs,
alongside the first large-scale dataset for this task. They conclude that LLMs are approaching human-level
performance in proof evaluation. Ma et al. [18] introduce a dataset for grading math competition proofs, with
a focus on 0-7 point grading, going beyond the binary verification task. Pandit et al. [23] propose a dataset
with a focus on step-level correctness verification of mathematical proofs.
Reward Models for Hard-to-Verify Tasks. In contrast to tasks with easily verifiable answers, proof
verification in natural language is an inherently challenging task, even for humans. Recent works have explored
training reward models to tackle hard-to-verify tasks. Although no publicly available work specifically explores
training LLMs with LLM-based reward models for proof generation, similar approaches have been applied
in other domains, such as open-ended writing. The current mainstream approach is to train generative
verifiers or use off-the-shelf LLMs to judge the correctness or ranking of model-generated solutions, and use
the verifiers to guide the generation of better solutions. Kimi K2 [27] use a self-critique-based approach to
generate responses and act as its own critique to judge the response given a predefined rubric for the task.
Lu [17] also use a self-critique approach to rank the generated model responses of the underlying LLM for
open-ended writing tasks. These rankings are then used to produce rewards for training a reward model,
which is then used to further finetune the LLM using reinforcement learning.


3. Background and Setup
We begin by introducing the two primary paradigms for automated proof verification using large language
models: LLM-as-a-Judge and GenSelect. In the LLM-as-a-Judge paradigm [30, 34, 26], a language model
directly evaluates the correctness of a single proof, typically producing either a binary judgement or a fine-
grained score (e.g., on a 7-point scale). To improve reliability, practitioners often sample multiple independent
judgements and aggregate them by averaging scores or taking majority votes. We denote the number of
sampled judgement per proof as 𝑛𝑗 . Since this method assigns a numerical score to each proof, it is useful when
evaluating individual proofs, as well as for selecting the best proof among multiple candidates by choosing


                                                                                                               2
             Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



the proof with the highest score. GenSelect [28, 7] takes a comparative approach: rather than evaluating
proofs individually, the model compares many proofs in-context, and selects the best one. This method is
often used in a pairwise format, and a tournament structure is employed to select the best proof among
multiple candidates. A knockout tournament operates in single-elimination format, requiring exactly 𝑛𝑝(︀− )︀1
comparisons to select a winner from 𝑛𝑝 candidates. Alternatively, a pairwise tournament compares all 𝑛2𝑝
pairs and selects the proof winning the most comparisons. This achieves higher accuracy than knockout
tournaments but requires quadratically many comparisons. When multiple candidate proofs are available for
a single problem, the goal is to select the best proof from among them. We now describe the datasets used to
evaluate these methods.

3.1. Datasets Details

Evaluating proof verification requires datasets that test different capabilities. We use six complementary
datasets, which we name as follows for better clarity:
VerProofArena: A collection of proofs from USAMO 2025, IMO 2025, and IMC 2025, with human-labeled
judgements from MathArena [5]. We augment this dataset with recent solutions to IMO 2025 from Gemini [6]
and OpenAI [21] to improve diversity. This dataset contains 204 proofs with binary correctness labels. The
majority of proofs are graded by at least two human graders or are officially accepted solutions. Although
the dataset has the highest label reliability, the majority of correct proofs are generated by Gemini. We
discuss potential implications of the dataset composition in Section 4. We use this dataset to evaluate proof
verification methods.
VerProofBench: This benchmark includes 429 proofs from recent proof-based competitions, scored on a
7-point rubric by expert human graders from ProofBench [18]. The task requires judging proof quality on this
7-point scale. In this work, we binarize the scores into correct (score ≥ 6) and incorrect (score < 6) for proof
verification judgement.
VerOPC: A large scale dataset of mathematical proofs with human-labeled correctness from OPC [7]. This
dataset contains 3K training proofs, and 292 test proofs.
Challenge-19: We select the 19 most challenging problems from AIME 2024, HMMT 2024, and CMIMC
2025 with integer final answers (called Challenge-19). We retain only problems where GPT-OSS-120B [3]
with high-reasoning mode generates at least one correct answer but maintains a solve rate below 70%. These
problems serve dual purposes: evaluating test-time compute methods and assessing proof-level judgement
precision on generated solutions.
SelOPC: The pass@n subset from the OPC [7] dataset consisting of 60 problems with 8 proofs per problem
generated by the OpenAI o4-mini model. We use this dataset to evaluation selection of the best proof among
8 generated proofs per problem.
SelProofBench: The best-of-n subset from the ProofBench [18] dataset consisting of 29 problems, each with
16 proofs generated by OpenAI o3. We use this dataset to evaluate proof-selection among 16 generated proofs
per problem. 14 out of the 29 problems have at least one correct proof (i.e., score at least 6/7).


4. Challenges in Building Reliable Evaluation Sets
We find that the choice of evaluation set is crucial for developing and benchmarking proof judgement models.
We identify two primary sources of challenge in building reliable evaluation sets.
Challenge 1: Human Label Noise. Human label noise can be significant, making it difficult to obtain
large-scale reliable ground truth judgement labels. While the VerOPC [7] represents a valuable contribution as
the first large-scale training set for proof verification with over 3K training examples, the noise in human labels
poses challenges for evaluating and training the strongest models. For instance, GPT-OSS-120B achieves
87.67% accuracy on the VerOPC (maj@8), whereas the estimated human labeler accuracy on this set is
90.4% [7]. This small gap between model and human performance indicates that the VerOPC test set is not
suitable for evaluating strong proof graders, as the noise ceiling is too low. Such limitations make the dataset
challenging to use for further training strong models such as GPT-OSS-120B via RL. Consequently, in the
main experiments, we only use the training set to train a weaker model, Qwen3-30B-A3, as a proof grader.
Challenge 2: Dataset Imbalances. Model and problem imbalances in the dataset may lead models to
exploit spurious correlations to achieve high accuracy without genuinely understanding the mathematical
content of proofs. We demonstrate this issue through two case studies using VerOPC [7].


                                                                                                                 3
             Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



Case Study 1: Simple MLP Classifier. We train a two-layer Multi-Layer Perceptron (MLP) binary classifier
on text embeddings of (problem, proof) pairs using a small Qwen3-0.6B [31] embedding model. Despite its
simplicity, this model achieves 75.34% accuracy on the OPC test set, outperforming Claude-Sonnet-4 by more
than 5% (see Table 1 in the Appendix for numerical comparisons to all the LLMs).
Case Study 2: Trivial Heuristic. We implement a simple rule-based classifier: predict “incorrect” if the
problem contains the word “triangle”, “correct” if it contains “––-”, and “incorrect” otherwise. This trivial
heuristic achieves 65.07% accuracy, outperforming both Qwen3-8B and GPT-4.1.
   Both methods attain high accuracy without any genuine understanding of proof correctness by exploiting
two types of dataset imbalances: (1) LLMs frequently generate incorrect geometry proofs, making “predict
incorrect for all geometry problems” a surprisingly effective strategy. (2) OpenAI reasoning models, which
produce more correct proofs than other LLMs, consistently use “––-” to separate proof sections—creating an
unintended marker for correctness.
    These imbalances echo concerns raised by Shi and Jin [26] in the context of training judge models for
final-answer judgement. They show that including entorely correct or incorrect solutions in the RL pipeline
from individual models lead to lower performance than balanced sets where each model produces both correct
and incorrect answers. While their work addresses training set composition, we reveal that similar imbalances
in test sets can introduce substantial evaluation bias, inflating accuracy metrics without reflecting true
verification capability.
    To mitigate this issue, we use final-answer correctness as an auxiliary evaluation metric alongside proof-level
judgement. We generate an equal number of correct-final-answer and incorrect-final-answer solutions for
each problem using GPT-OSS-120B and Qwen3-235B-A22-Thinking-2507. The solutions in this dataset are
particularly useful since we can monitor the precision of a judge on this dataset. That is, if a judge predicts a
proof to be correct, precision computes how likely it is that the proof has the correct final answer. Monitoring
precision allows us to distinguish between judges that rely primarily on superficial features (e.g., stylistic
cues) versus those that genuinely assess the mathematical content. Because of its balanced construction, this
final-answer dataset provides a robust benchmark for precision-based evaluation, and any decision based on
either model or problem type or both receives no better than random chance.

  Takeaway 1: Reliable evaluation requires proofs with (a) high quality ground-truth labels and (b) a
  balanced problem-difficulty nature and model diversity. Incorporating a balanced final-answer evaluation
  set can further help better distinguish judges that assess genuine mathematical content from those
  exploiting stylistic features.


5. Proof Verification via Single-Proof Judgement
LLM-as-a-Judge is one of the most widely used ways of verification in hard-to-verify tasks [27]. We start by
prompt design, and evaluate three prompts for LLM-as-a-Judge: a general-purpose prompt adapted from
ProcessBench [35], and two proof-specific prompts from the OPC [7] and a Gemini Agent [12]. To standardize
their outputs, we only modify the formatting to use XML tags, leaving the prompt content unchanged. We
refer to these prompts as General Summary, OPC, and GIMO. Figure 1 (right) reports majority@5 results on
both proof-level and final-answer judgements. The results show that prompt choice has a substantial impact
on LLM-as-a-Judge performance: General Summary achieves high recall but low precision, GIMO achieves high
precision but low recall, and OPC strikes a balance between the two. Based on this trade-off, we adopt OPC as
the default prompt in our main experiments.
    Given the high variation in the performance of different prompts, we experiment with using RL to fine-tune
a language model to be a better judge. We use the OPC training set to train a Qwen3-30B-A3B-Thinking-2507
model using Group Relative Policy Optimization (GRPO) [25] with a binary reward, measuring whether
the model judgement matches the ground truth judgement. Figure 1 shows the training curve of the RL
training with different prompts. Aligned with prior works [7], we observe that RL training significantly
improves the performance. Interestingly, we find that this performance gain is prompt agnostic, and the
high performance variance across prompts is eliminated, as the performance gap is closed between OPC and
GIMO prompts in Figure 1. Although the OPC prompt initially exhibits lower performance compared to the
GIMO prompt, RL training leads to convergence to similar results. It is important to note that the VerOPC



                                                                                                                 4
                                  Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



                                                                                                               Proofs           Final Answers*
                                      GRPO Validation Curves                      Prompt
                                                                                                       Prec     Rec      F1     Prec     Rec

                      0.86                                                        General Summary      18.28   99.89    30.91   58.21   74.86
                                                                                  GIMO                 57.58   87.06    69.28   64.85   15.53
Validation Accuracy




                      0.84                                                        OPC                  22.88   99.96    37.23   60.41   67.43
                      0.82                                                        OPC (Rubric)         24.46   99.89    39.30   92.25   77.45
                      0.80                                     GIMO               OPC RL               54.03   94.57    68.75   62.59   17.18
                                                               OPC                GIMO RL              49.66   95.81    65.40   66.29   22.65
                      0.78                                     OPC + GT Proof     OPC RL (Rubric)      39.72   98.98    56.69   98.15   50.02
                      0.76                                     OPC + Rubric       OPC RL
                                                                                                       39.09   98.64    55.99   98.12   49.06
                                                                                  (GT-Proof→Rubric)
                             0   20   40    60    80     100   120   140    160
                                             Training Steps                       OPC RL
                                                                                                       59.74   95.09    73.35   99.31   21.27
                                                                                  (No-Rubric→Rubric)

Figure 1: Left: Training curves for RL training of Qwen3-30B-A3B-Thinking-2507 on the OPC dataset. (1)
Different prompts converge to similar performance after RL training. (2) Including the ground-truth proof or
rubric in the prompt improves validation performance by 2–3%. (3) Training with both rubric and
ground-truth proof achieves comparable performance. Right: Majority@5 results for the VerProofArena and
Challenge-19 evaluation using Qwen3-30B-A3. See Tables 5 and 6 in the Appendix for full results, additional
models, datasets, and prompt ablations. 𝑎 → 𝑏 denotes trained on 𝑎 evaluated on 𝑏. * For final-answer
problems, precision and recall are computed based solely on the correctness of the final answer.


and VerProofArena datasets differ significantly in their distribution, which influences model performance
discrepancy. The VerProofArena (out-of-distribution) dataset is more challenging, with correct proofs being
scarce, having lower label noise, and correct proofs being generated by stronger models. In contrast, the
VerOPC (in-distribution) dataset has higher correct proofs and easier problems. These dataset differences
explain the discrepancies between validation accuracy and the results shown in the table.

            Takeaway 2: LLM-as-a-Judge shows high variation across different prompts. However, RL training can
            significantly (1) improve performance and (2) reduce prompt sensitivity.
    While we observe that RL improves performance on the proof judgement (Figure 1 Right), it does not
improve precision on the final-answer problems. The precision improves by about 2%, but this change is
within the standard deviation of performance, as noted in Table 5 in the Appendix. We hypothesize that
the proof performance gain is likely due to the model being able to identify incorrect style of proofs such as
missing justifications and getting better calibrated rather than improvement in truly reasoning about the
mathematical content of the proofs. This will likely require scaling up the training data with challenging
proofs, as well as scaling up the reinforcement learning training to larger number of steps to gain more
significant gains on the mathematical content judgement.

            Takeaway 3: RL significantly improves proof-level metrics, but the performance gain mainly serves as
            a calibration process rather than improved mathematical reasoning.
Adding rubric does not significantly improve performance. Recent studies show that having ground-
truth rubric can help LLMs better judge the quality generate content in general areas [4], as well as mathematical
proofs [4]. Assuming access to a ground-truth solution or rubric could potentially help with training better
proof judges by collecting pairs of (problem, ground-truth-proof) and using them at training time to
guide the training of proof verifiers or generators. We evaluate whether including a ground-truth proof
or rubric in the prompt during verification improves the model’s ability to judge proofs and enables more
effective auto-labeling. Overall, adding the rubric does not lead to a substantial performance gain in proof
judgement, except for improvement in final-answer precision (see Figure 1 Right). Surprisingly, models trained
without a rubric outperform those trained with rubric on the VerProofArena (out-of-distribution), although
they underperform on the VerOPC (in-distribution) validation curves shown in Figure 1. Interestingly,
our best-performing model is one that was trained without a rubric but was given a rubric at test time,
demonstrating particularly high precision.
Ensembling different judges does not outperform the best single judge. As an alternative scaling
strategy, we evaluate ensembles that average correctness scores across different judges. We test this approach



                                                                                                                                                 5
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



on the SelOPC proof selection task and find that ensembling generally fails to surpass the best individual judge.
The only exception occurs when one judge is a model trained on the VerOPC dataset with reinforcement
learning (see Figure 4 in the Appendix), which we attribute to adaptation to in-distribution training data.
Step-based Judgement does not improve performance. Recent work has explored step-based judgement,
where the model first decomposes a proof into individual steps by inserting step separators, then evaluates
each step independently and aggregates the results to form a final judgement. Guo et al. [10] report improved
performance using such approaches. We implement a step-based judgement model with two prompts: (1)
the model decomposes the proof into steps, and (2) the model is reprompted with each step highlighted and
asked to judge whether the step is correct. We aggregate the results by marking a proof as correct only
if all steps are judged to be correct. Results are shown in Table 3 in the Appendix. We observe higher
precision, but significantly lower recall and accuracy. The strict all-steps-correct requirement likely leads to
many false negatives that outweigh the precision gains. Exploring better aggregation methods, RL strategies,
or step decomposition techniques is a promising direction for future work to improve step-based judgement
performance.
   We conduct additional ablation studies on the number of sampled judgments and the impact of different
base models in Appendix B.

  Takeaway 4: Whole-proof LLM-as-a-Judge provides the best performance among different proof
  judgement strategies. Adding a ground-truth proof or rubric to the prompt slighly improves the
  performance, but the gain is not significant.


6. Revisiting Proof Selection Methods
Two of the most prevalent algorithms for proof selection are GenSelect [28, 7] and LLM-as-a-Judge [30, 34, 26].
Here, we first revisit these two methods and run extensive experiments to compare their performance on
existing best-of-n proof selection benchmarks, namely the SelProofBench and SelOPC. Dekoninck et al. [7]
report that a pairwise GenSelect tournament outperforms LLM-as-a-Judge on the OPC-PassN benchmark,
while Ma et al. [18] report that LLM-as-a-Judge, using a 7-point grading prompt outperforms GenSelect
tournament. Furthermore, both studies show that 7-point grading prompts outperform binary judgement
prompts for LLM-as-a-Judge. To reconcile these conflicts, we conduct experiments on both LLM-as-a-Judge
and GenSelect using two models: GPT-OSS-120B and Qwen3-235B-A22-Thinking-2507.
    First, we scale the number of sampled judgements per proof in LLM-as-a-Judge, as higher number of
judgements generally leads to better estimates of the proof correctness [26]. Indeed, we find that higher number
of judgements lead to better proof selection up to 32 judgements per proof, after which the performance
saturates (see Figure 4 in the Appendix).
                                       (︀ )︀ For the Pairwise GenSelect tournament, we use the same setup
as Ma et al. [18], where we perform 𝑛2𝑝 pairwise comparisons, and choose the proof with highest number
of wins as the winner. We repeat all the experiments with 8 seeds as the results show high variance. The
results are depicted in Figure 2. We make the following observations: (1) There is no clear winner between
pairwise GenSelect tournament and LLM-as-a-Judge; the best method varies by dataset and model. (2)
Contrary to prior findings, 7-point grading does not show a consistent advantage over binary grading, although
it outperforms binary grading on 7-point scoring metric. This means that the 7-point grading prompt is
better at finding the best incorrect proof, although more research is needed as the 7-point-based results on
SelProofBench may not transfer to other datasets such as SelOPC and vice versa. (3) Including a ground-truth
proof or rubric in the prompt does not lead to better performance for either methods, and in fact, Qwen3-235B
shows worse performance when given a ground-truth proof and rubric in the prompt. Despite these findings,
we note that the SelProofBench consists of only 29 problems, therefore, 3.44% accuracy difference is only one
problem difference. Our findings highlight the challenges in the significant effort required to build reliable
evaluation sets for proof selection, as discussed in Section 3.

  Takeaway 5: LLM-as-a-Judge and Pairwise GenSelect Tournament are both strong proof selection
  methods, and there is not clear winner between the two.




                                                                                                               6
                                      Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection


                                        GPT-OSS-120B OPC                                                  GPT-OSS-120B ProofBench                                                          GPT-OSS-120B ProofBench
                      45.0                                                                                                                                                     40
                                                                                             4.0
                      42.5
                                                                                                                                                                               35
Binary Accuracy (%)




                                                                                                                                                         Binary Accuracy (%)
                      40.0                                                                   3.5




                                                                             7-Point Score
                      37.5                                                                                                                                                     30
                      35.0                                                                   3.0
                                                                                                                                                                               25
                      32.5
                                                                                             2.5                                                                               20
                      30.0
                      27.5
                                                                                             2.0                                                                               15
                             1   2      3     4      5      6      7     8                         2      4     6     8     10        12   14       16                              2      4    6     8     10        12   14   16
                                         Number of Proofs (n)                                                  Number of Proofs (n)                                                            Number of Proofs (n)
                                     Qwen3-235B-Thinking OPC                                           Qwen3-235B-Thinking ProofBench                                                   Qwen3-235B-Thinking ProofBench
                      45.0                                                                   4.0                                                                               35
                      42.5
Binary Accuracy (%)




                                                                                                                                                         Binary Accuracy (%)
                      40.0
                                                                             7-Point Score   3.5                                                                               30
                      37.5
                                                                                             3.0                                                                               25
                      35.0
                      32.5
                                                                                             2.5                                                                               20
                      30.0
                      27.5                                                                                                                                                     15
                                                                                             2.0
                             1   2      3     4      5      6      7     8                         2      4     6     8     10        12   14       16                              2      4    6     8     10        12   14   16
                                         Number of Proofs (n)                                                  Number of Proofs (n)                                                            Number of Proofs (n)

                                 Pairwise Tournament            LLMJ (Binary OPC)                       LLMJ (Binary ProofBench)                LLMJ (7-Point, Rubric + GT Proof)                           LLMJ (7-Point)

 Figure 2: Best-of-n proof selection results on SelProofBench and SelOPC using GPT-OSS-120B and
 Qwen3-235B-A22-Thinking-2507. We compare pairwise GenSelect tournament with LLM-as-a-Judge
 (averaging 32 judgements per proof) using both binary and 7-point grading prompts. Results are averaged
 across 8 random seeds. No single method consistently outperforms the others; the best approach varies by
 dataset and model.


   7. Scaling Proof Selection
  A knockout GenSelect tournament uses pairwise comparisons in a knockout tournament format, requiring
  exactly 𝑛𝑝 − 1 comparisons to select the best proof from 𝑛𝑝 candidates. While this approach is token-efficient,
  it has a sequential depth of at least log(𝑛𝑝 ), limiting parallelization. Furthermore, it is less performant than a
  pairwise tournament that compares all pairs of proofs [7, 18]. In contrast, LLM-as-a-Judge evaluates each
  proof independently by sampling 𝑛𝑗 judgements per proof, requiring 𝑛𝑗 × 𝑛𝑝 LLM calls total. This method is
  highly parallelizable but more computationally expensive due to the larger number of required evaluations.
      When scaling proof generation to hundreds of proofs, pairwise tournaments and LLM-as-a-Judge become
   prohibitively expensive, while a knockout tournament is less expensive. We propose to unify these two
   approaches into a single framework that strikes a balance between compute intensiveness, efficiency, and
   accuracy. Given a problem, we first generate 𝑛𝑝 candidate proofs by temperature sampling from a language
   model. Then we run a knockout GenSelect tournament to select the top 𝑛𝑠 proofs among the candidates
   using the same language model. Finally, we run LLM-as-a-Judge to estimate the correctness score of each
   proof by sampling 𝑛𝑗 judgements for each proof, and select the proof with the highest average correctness
   score as the final proof to solve the problem. This unified framework naturally subsumes both individual
   methods: setting 𝑛𝑠 = 1 and 𝑛𝑗 = 0 reduces to pure knockout GenSelect, while setting 𝑛𝑠 = 𝑛𝑝 reduces to
   pure LLM-as-a-Judge.
   Final Answer Evaluation. Figure 3 illustrates the proposed method and accuracy results for different
   configurations on GPT-OSS-120B. We focus our experiments on the final-answer problems since they provide
   faster evaluation feedback. Our combined approach works on par with, and sometimes outperforms, each
   method individually. We find that this combined method significantly outperforms majority voting, and
   consistently matches or outperforms GenSelect [28], and is more scalable than LLM-as-a-Judge. Notably it
   achieve 100% accuracy on AIME-2025 across all 8 runs with different random seeds using GPT-OSS-120B.
   Proof Evaluation. As discussed in Section 6, constructing reliable evaluation sets for proof selection is
   challenging due to the need for a large number of graded proofs to effectively distinguish between different
   proof selection methods. However, we run preliminary experiments using our test-time scaling method with



                                                                                                                                                                                                                                     7
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection


                                                                                           Challenge-19 Results
                                                                               𝑛𝑝     𝑛𝑠      𝑛𝑗   Acc (%)        Compute
                                                                             GenSelect Knockout Tournament
                                                                               64    1    –     88.81     ×127
                                                                              128    1    –     91.44     ×255
               Proof                                                          256    1    –     92.10     ×511
                                                 Judge
                                                                              512    1    –     90.80    ×1023
                         Proof
                                                                             LLM-as-a-Judge
                                     Proof                                    256 256 32             91.44         ×8448
                                      10         Judge
                          Proof                    2                         Hybrid (ours)
                                                                Discarded     128    16    32       91.44          ×752
                           10
                                                 Judge                        256    16    32       96.05          ×1008
Problem                                            1
                                                                              512    16    32       94.07          ×1520
               Proof
                 3                               Judge                              maj@512          82.23         ×512
                          Proof
                                                                                    pass@1           47.07          ×1
                            7
               Proof                 Proof       Judge                                     AIME 2025 Results
                 2                     2           2             Chosen        𝑛𝑝     𝑛𝑠      𝑛𝑗   Acc (%)        Compute
                          Proof
                                                 Judge
                            2                      1
                                                                             GenSelect Knockout Tournament
               Proof                                                          128    1    –      97.5     ×255
                 1
                                                                             LLM-as-a-Judge
                                                                              128 128 32              100          ×4224
                                                                             Hybrid (ours)
                                                                              128    16    32         100          ×752
                                                                                    maj@128          97.08         ×128
                                                                                    pass@1           91.26          ×1

Figure 3: Left: Overview of our proposed test-time scaling method to combine GenSelect with
LLM-as-a-Judge for proof selection. Given a question, we first generate 𝑛𝑝 candidate proofs by sampling from
a language model. Then we run a knockout GenSelect tournament to select the best proof among the
candidates using the same language model to select the top 𝑛𝑠 proofs. We estimate the correctness score of
each proof using LLM-as-a-Judge by sampling 𝑛𝑗 judgements for each proof. Finally, we select the proof with
the highest average correctness score as the final proof to solve the problem. Right: The tables show accuracy
results for different configurations of our method on GPT-OSS-120B, averaged across 8 seeds on AIME-2025
and Challenge-19. Compute is reported as the total number of LLM calls per problem. The hybrid
combination of LLM-as-a-Judge with GenSelect performs substantially better than GenSelect alone, or
majority voting.


𝑛𝑝 = 256, 𝑛𝑠 = 16, 𝑛𝑗 = 32 on the USAMO-2025. We focus on problem 2, since it is at the boundary of being
solvable by GPT-OSS-120B with high-reasoning mode. We observe that our method selects a correct proof
50% of the time, compared with zero correct proofs from the no-test-time-scaling GenSelect method. We
provide a correct example from the test-time scaling method, and an incorrect example from the baseline in
Appendix D.

  Takeaway 6: Combining a knockout GenSelect tournament with LLM-as-a-Judge for proof selection
  strikes a balance between compute efficiency and accuracy compared to individual methods.


8. Experimental Details
RL Training. We train Qwen3-30B-A3B-Thinking-2507 and Qwen3-8B using the DAPO algorithm [32] on
the VerOPC [7] training set. We set aside 277 proofs from the training set as our validation set to monitor the
training progress. The training is done on policy, without length penalty, with a batch size of 1024 sequences
(64 prompts with 16 rollouts each), and maximum generation length of 16384 on 128 H100 GPUs.


                                                                                                                            8
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



Inference Settings. We allocate a 100K completion length budget to all the models, and use the recommended
sampling parameters by the model providers. For GPT-OSS models, we sample with temperature 1.0 and
top-p 1.0, for Qwen models, we sample with temperature 0.6, top-p 0.95 and top-k 20. For other models, we
use temperature of 0.7 and top-p 0.95. We use Nemo-Skills [1] as our codebase, and SGLang [2] and VLLM [2]
for efficient LLM inference. All the inference workloads are executed on a mix of A100, H100, and GB200
GPUs.
Dataset Details. In all the datasets, we filter out the proofs that exceed 10K Qwen3 tokens, as they are too
long or contain many thinking steps, and are all incorrect proofs. We use the rubrics and ground-truth proofs
as provided by the datasets, and generate rubrics using LLMs when needed. For the ProofBench datasets, we
use the ground-truth proof and rubrics provided by the dataset [18]. For the proofs taken from MathArena [7],
we use the provided rubric directly. For the OPC datasets [7], we directly use the ground-truth proof provided
in the dataset, and generate a rubric using GPT-OSS-120B based on the ground-truth proof when needed.
For the final-answer problems, we use the expected final answer as the rubric. This makes verification with
rubric a simpler task as the model only needs to compare two answer and does not need to check other
computational details.


9. Discussion: Are LLMs ready to be reliable Mathematical Judges?
While all SOTA LLMs are able to achieve high accuracy in proof judgement (e.g.., > 90% accuracy on
ProofBench [18]), we observe that this still does not translate to high reliability, especially when scaling
test-time compute or judging hard problems. For instance, we attempted to use GPT-5 (high thinking mode)
to judge proofs of various test-time scaling methods generated by GPT-OSS in Section 7 on the USAMO 2025
hard problems (problems 5 and 6). For each problem, we generated proofs using different methods, reaching
24 candidate proofs per problem. We then used GPT-5 as a judge, aiming to automate the grading process at
scale for faster feedback. Surprisingly, GPT-5 judged 7 out of the 48 candidates as correct, despite all of them
having critical mathematical errors. Although GPT-5 has 41/48 = 87.2% accuracy on judging these proofs,
this still means that it cannot be fully trusted to reliably judge mathematical proofs, especially when the
correct proofs are rare. We found that providing a ground-truth solution in the prompt or using majority
voting over five judgements did not alleviate this issue. One example of such an incorrect judgement is shown in
Appendix D. Notably, this issue persists despite the fact that the generator (GPT-OSS) is significantly weaker
than the verifier (GPT-5). Therefore, we advise caution when using large language models as mathematical
judges in high-stakes scenarios, especially for complex problems where correct solutions are infrequent, and
human verification is necessary.


10. Conclusion
In this work, we addressed the critical challenge of verifying and selecting natural-language mathematical
proofs using LLMs. We showed that a unified test-time scaling approach that combines GenSelect tournaments
with LLM-as-a-Judge evaluation performs the best at scale. We made surprising findings: while reinforcement
learning eliminates prompt variation and improves proof-level metrics, it does not improve final-answer
precision, suggesting current approaches may rely more on recognizing stylistic features rather than deep
mathematical understanding.
Future Directions. An important direction for future work is to focus on problems at the frontier of current
LLMs’ solving capabilities. By carefully selecting such challenging problems and rigorously labeling them, we
aim to create high-quality benchmarks that drive further improvements in proof-judgment and problem-solving
models. We also plan to leverage RL to further scale up the performance of LLM-based judges and solvers, as
well as explore other scaling methods such as step-level judgement, where intermediate reasoning steps are
supervised rather than the final outcome.
Limitations. While we provide an extensive study over the current state-of-the-art LLMs for proof verification
and selection, our experiments and conclusions are limited to the models and datasets available at the time of
writing. It might be possible that future models, trained exclusively on LLM-as-a-Judge or GenSelect tasks,
could yield different results. Furthermore, as model capabilities improve, the effectiveness or brittleness of
prompts, as well as the effectiveness of rubrics within those prompts, may also change.



                                                                                                              9
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



References
 [1] NeMo-Skills. https://github.com/NVIDIA-NeMo/Skills, 2025. GitHub repository.

 [2] SGLang. https://github.com/sgl-project/sglang, 2025. GitHub repository.
 [3] Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus, Rahul K
     Arora, Yu Bai, Bowen Baker, Haiming Bao, et al. gpt-oss-120b & gpt-oss-20b model card. arXiv preprint
     arXiv:2508.10925, 2025.
 [4] Rahul K Arora, Jason Wei, Rebecca Soskin Hicks, Preston Bowman, Joaquin Quiñonero-Candela,
     Foivos Tsimpourlas, Michael Sharman, Meghan Shah, Andrea Vallone, Alex Beutel, et al. Healthbench:
     Evaluating large language models towards improved human health. arXiv preprint arXiv:2505.08775,
     2025.
 [5] Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, and Martin Vechev. Matharena:
     Evaluating llms on uncontaminated math competitions, February 2025. URL https://matharena.ai/.

 [6] DeepMind.       Advanced version of gemini with deep think officially achieves gold-medal
     standard at the international mathematical olympiad.      https://deepmind.google/blog/
     advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-interna
     2025. Blog post.

 [7] Jasper Dekoninck, Ivo Petrov, Kristian Minchev, Mislav Balunovic, Martin Vechev, Miroslav Marinov,
     Maria Drencheva, Lyuba Konova, Milen Shumanov, Kaloyan Tsvetkov, et al. The open proof corpus: A
     large-scale study of llm-generated mathematical proofs. arXiv preprint arXiv:2506.21621, 2025.
 [8] Kefan Dong and Tengyu Ma. Stp: Self-play llm theorem provers with iterative conjecturing and proving.
     arXiv preprint arXiv:2502.00212, 2025.

 [9] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong
     Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
     learning. arXiv preprint arXiv:2501.12948, 2025.
[10] Jiaxing Guo, Wenjie Yang, Shengzhong Zhang, Tongshan Xu, Lun Du, Da Zheng, and Zengfeng Huang.
     Right is not enough: The pitfalls of outcome supervision in training llms for math reasoning. arXiv
     preprint arXiv:2506.06877, 2025.
[11] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
     and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. CoRR,
     abs/2103.03874, 2021. URL https://arxiv.org/abs/2103.03874.
[12] Yichen Huang and Lin F Yang. Gemini 2.5 pro capable of winning gold at imo 2025. arXiv preprint
     arXiv:2507.15855, 2025.
[13] Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Hel-
     yar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. arXiv preprint
     arXiv:2412.16720, 2024.
[14] Shalev Lifshitz, Sheila A McIlraith, and Yilun Du. Multi-agent verification: Scaling test-time compute
     with multiple verifiers. arXiv preprint arXiv:2502.20379, 2025.
[15] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John
     Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. arXiv preprint arXiv:2305.20050,
     2023.

[16] Yantao Liu, Zijun Yao, Rui Min, Yixin Cao, Lei Hou, and Juanzi Li. Pairjudge rm: Perform best-of-n
     sampling with knockout tournament. arXiv preprint arXiv:2501.13007, 2025.
[17] Xun Lu. Writing-zero: Bridge the gap between non-verifiable problems and verifiable rewards. arXiv
     preprint arXiv:2506.00103, 2025.



                                                                                                              10
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



[18] Wenjie Ma, Andrei Cojocaru, Neel Kolhe, Bradley Louie, Robin Said Sharif, Haihan Zhang, Vincent
     Zhuang, Matei Zaharia, and Sewon Min. Reliable fine-grained evaluation of natural language math proofs.
     arXiv preprint arXiv:2510.13888, 2025.
[19] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
     Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement with self-feedback.
     Advances in Neural Information Processing Systems, 36:46534–46594, 2023.
[20] Hamed Mahdavi, Alireza Hashemi, Majid Daliri, Pegah Mohammadipour, Alireza Farhadi, Samira Malek,
     Yekta Yazdanifard, Amir Khasahmadi, and Vasant Honavar. Brains vs. bytes: Evaluating llm proficiency
     in olympiad mathematics. arXiv preprint arXiv:2504.01995, 2025.
[21] OpenAI. Openai imo 2025 proofs. https://github.com/aw31/openai-imo-2025-proofs, 2025. GitHub
     repository.
[22] OpenAI. Gpt-5 system card. Technical report, OpenAI, 2025. URL https://cdn.openai.com/
     gpt-5-system-card.pdf. Accessed: 2025-09-19.
[23] Shrey Pandit, Austin Xu, Xuan-Phi Nguyen, Yifei Ming, Caiming Xiong, and Shafiq Joty. Hard2verify:
     A step-level verification benchmark for open-ended frontier math. arXiv preprint arXiv:2510.13744, 2025.
[24] ByteDance Seed, Jiaze Chen, Tiantian Fan, Xin Liu, Lingjun Liu, Zhiqi Lin, Mingxuan Wang, Chengyi
     Wang, Xiangpeng Wei, Wenyuan Xu, et al. Seed1. 5-thinking: Advancing superb reasoning models with
     reinforcement learning. arXiv preprint arXiv:2504.13914, 2025.
[25] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
     Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open
     language models. arXiv preprint arXiv:2402.03300, 2024.
[26] Wenlei Shi and Xing Jin. Heimdall: test-time scaling on the generative verification. arXiv preprint
     arXiv:2504.10337, 2025.
[27] Kimi Team, Yifan Bai, Yiping Bao, Guanduo Chen, Jiahao Chen, Ningxin Chen, Ruijue Chen, Yanru Chen,
     Yuankun Chen, Yutian Chen, et al. Kimi k2: Open agentic intelligence. arXiv preprint arXiv:2507.20534,
     2025.
[28] Shubham Toshniwal, Ivan Sorokin, Aleksander Ficek, Ivan Moshkov, and Igor Gitman. Genselect: A
     generative approach to best-of-n. arXiv preprint arXiv:2507.17797, 2025.
[29] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery,
     and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. arXiv preprint
     arXiv:2203.11171, 2022.
[30] Chenxi Whitehouse, Tianlu Wang, Ping Yu, Xian Li, Jason Weston, Ilia Kulikov, and Swarnadeep Saha.
     J1: Incentivizing thinking in llm-as-a-judge via reinforcement learning. arXiv preprint arXiv:2505.10320,
     2025.
[31] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
     Chengen Huang, Chen Zhang, Chuanqi Tan, Daxin Jiang, Dongdong Zhang, Fandong Meng, Fuli Luo,
     Guolin Ke, Hang Yan, Hao Tian, Hong Chen, Hongbin Zhang, Hongyi Yuan, Huanbo Luan, Hui Liu,
     Jiayi Wang, Jidong Zhai, Jindong Chen, Jinhui Liu, Jinqiu Sun, Jiong Cai, Jizhou Huang, Jun Xie,
     Junyang Lin, Kai Chen, Lei Li, Lei Wang, Liang Wang, Lianxin Jiang, Linjun Shou, Liyang Lu, Lu Chen,
     Lu Wang, Mengdi Wang, Ming Gong, Ming Yan, Ming Zhou, Nan Duan, Pengcheng Shi, Qian Liu,
     Qiang Qu, Qianqian Dong, Qiang Wang, Qingsong Wen, Qun Liu, Renjie Zheng, Ruofei Zhang, Rui
     Wang, Shuming Ma, Shuo Ren, Shuxin Zheng, Songlin Hu, Tao Yu, Tianyu Liu, Tong Xiao, Wei Li, Wei
     Wang, Wenbin Jiang, Wenhao Huang, Wenxuan Wang, Xiaodong Liu, Xiaofei Sun, Xiaohui Yan, Xiaojun
     Wan, Xiaolei Wang, Xiaoyan Zhu, Xin Jiang, Xing Xie, Xinyan Xiao, Xipeng Qiu, Xu Tan, Xuefeng
     Bai, Xuejun Ma, Xun Wang, Yan Gao, Yang Liu, Yanghua Xiao, Yanyan Lan, Yao Meng, Yaqing Wang,
     Yichong Xu, Yifan Wang, Yihong Chen, Yiming Cui, Yining Wang, Yiqun Liu, Yixuan Su, Yongbin Li,
     Yongfeng Zhang, Yongxin Lian, Yu Bai, Yu Sun, Yuan Yao, Yuanhang Zhang, Yucheng Wang, Yufan
     Jiang, Yujie Zhang, Yujing Wang, Yunchang Yang, Yunzhi Yao, Zhenzhong Lan, Zhiwei Zhao, Zhiwu Lu,


                                                                                                              11
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



    Zhiye Liu, Zhiwei Wang, Zhiyuan Liu, Zihang Jiang, and Zixuan Zhang. Qwen3 technical report. arXiv
    preprint arXiv:2505.09388, 2025. URL https://arxiv.org/abs/2505.09388.
[32] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, YuYue, Weinan Dai, Tiantian Fan,
     Gaohong Liu, Juncai Liu, LingJun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng,
     Yuxuan Tong, Chi Zhang, Mofan Zhang, Ru Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen,
     Jiangjie Chen, Chengyi Wang, Hongli Yu, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu,
     Wei-Ying Ma, Ya-Qin Zhang, Lin Yan, Yonghui Wu, and Mingxuan Wang. DAPO: An open-source LLM
     reinforcement learning system at scale. In The Thirty-ninth Annual Conference on Neural Information
     Processing Systems, 2025. URL https://openreview.net/forum?id=2a36EMSSTp.
[33] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. Star: Bootstrapping reasoning with reasoning.
     Advances in Neural Information Processing Systems, 35:15476–15488, 2022.
[34] Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal.
     Generative verifiers: Reward modeling as next-token prediction. arXiv preprint arXiv:2408.15240, 2024.
[35] Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jingren
     Zhou, and Junyang Lin. ProcessBench: Identifying process errors in mathematical reasoning. In Wanxiang
     Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of the 63rd
     Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1009–
     1024, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-251-0.
     doi: 10.18653/v1/2025.acl-long.50. URL https://aclanthology.org/2025.acl-long.50/.
[36] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
     Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena.
     Advances in neural information processing systems, 36:46595–46623, 2023.


A. Pitfalls of imbalanced evaluation set

Table 1: Benchmarking LLMs as proof graders. All LLM numbers are taken from Dekoninck et al. [7]. We
observe that a simple MLP classifier and a simple heuristic can outperform many LLMs.

                                        Judge                         pass@1
                                        Human                           90.4
                                        Gemini-2.5-Pro                  85.4
                                        OPC-R1-8B                       83.8
                                        OpenAI-O4-Mini                  83.8
                                        OpenAI-O3                       83.1
                                        Gemini-2.5-Flash                82.7
                                        Qwen3-235B-A22                  81.8
                                        DeepSeek-R1                     80.9
                                        MLP Classifier                  75.3
                                        Qwen3-30B-A3                    74.0
                                        DeepSeek-R1-Qwen3-8B            70.7
                                        Claude-4-Sonnet                 70.6
                                        Format Heuristic               65.07
                                        Qwen3-8B                        64.4
                                        GPT-4.1                         61.4
                                        Baseline                        53.2


B. Further Ablation Experiments
GenSelecting judgements improves proof verification performance. Inspecting the judgements
generated by LLM-as-a-Judge, we find that the LLM often finds the mistake in at least one of the sampled


                                                                                                              12
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




                                                     n=2                                                            n=3
                           0.34
                                                                                          0.38

                           0.33                                                           0.37
                                                                                          0.36
                Accuracy




                                                                               Accuracy
                           0.32
                                                                                          0.35

                           0.31                                                           0.34
                                                                                          0.33
                           0.30
                                                                                          0.32
                                                                                          0.31
                                  1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31                     1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31
                                          Number of Judgements (nj)                                      Number of Judgements (nj)
                                                     n=4                                                            n=5

                           0.40                                                           0.42


                           0.38                                                           0.40
                Accuracy




                                                                               Accuracy
                                                                                          0.38
                           0.36
                                                                                          0.36
                           0.34
                                                                                          0.34
                                  1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31                     1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31
                                          Number of Judgements (nj)                                      Number of Judgements (nj)
                                                     n=6                                                            n=7
                                                                                          0.46
                           0.44
                                                                                          0.44
                           0.42
                                                                                          0.42
                Accuracy




                                                                               Accuracy




                           0.40
                                                                                          0.40
                           0.38
                                                                                          0.38
                           0.36
                                                                                          0.36
                           0.34
                                  1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31                     1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31
                                          Number of Judgements (nj)                                      Number of Judgements (nj)
                                                     n=8
                           0.48
                                                                                             gpt-oss 120B
                           0.46                                                              Qwen3-8B OPC RL
                                                                                             Qwen3-32B Step Agent
                           0.44                                                              Qwen3-235B-A22B-Thinking
                Accuracy




                                                                                             gpt-oss 120B + Qwen3-8B OPC RL
                           0.42                                                              Qwen3-32B Step Agent + gpt-oss 120B
                                                                                             gpt-oss 120B + Qwen3-235B-A22B-Thinking
                           0.40                                                              Qwen3-32B Step Agent + Qwen3-8B OPC RL
                                                                                             Qwen3-235B-A22B-Thinking + Qwen3-8B OPC RL
                           0.38                                                              Qwen3-32B Step Agent + Qwen3-235B-A22B-Thinking
                           0.36
                                  1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31
                                          Number of Judgements (nj)

Figure 4: LLM-as-a-Judge performance on selecting the best proof among 8 generated proofs from SelOPC.
Higher number of judgements leads to better performance, plateauing around 20-30 judgements. Furthermore,
ensembling multiple models does not lead to any performance gain, and often the result does not exceed the
strongest LLM, except for ensembling an 8B model trained with RL on the training set of OPC. We suspect
that the improvement comes from the fact that the 8B model trained with RL is trained on the same
distribution as the test set, and therefore is complementary to other LLMs.




                                                                                                                                               13
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection


Table 2: List of challenging final-answer problems from HMMT, AIME, and CMIMC used in the
Challenge-19 dataset. All problems have an integer final answer.

                                  Index     Problem ID
                                  1         CMIMC 2025 P5
                                  2         CMIMC 2025 P7
                                  3         CMIMC 2025 P18
                                  4         CMIMC 2025 P34
                                  5         AIME 2024 P7
                                  6         AIME 2024 P14
                                  7         AIME 2024 P26
                                  8         HMMT Nov 2024 HMIC 1
                                  9         HMMT Nov 2024 Guts 19
                                  10        HMMT Nov 2024 Theme 7
                                  11        HMMT Nov 2024 Theme 9
                                  12        HMMT Feb 2024 Guts 28
                                  13        HMMT Feb 2024 Guts 29
                                  14        HMMT Feb 2024 Combinatorics 1
                                  15        HMMT Feb 2024 Combinatorics 4
                                  16        HMMT Feb 2024 Combinatorics 9
                                  17        HMMT Feb 2024 Combinatorics 10
                                  18        HMMT Feb 2024 Algebra 10
                                  19        HMMT Feb 2025 Team 4

Table 3: Comparison of step-based judgment versus vanilla LLM-as-a-Judge on VerProofBench using
GPT-OSS-120B. Results are averaged over majority@5 across 32 seeds. Step-based judgment shows higher
precision but significantly lower recall compared to vanilla LLM-as-a-Judge.

   Method                         Precision            Recall                F1           Correct Judgements
   Vanilla LLM-as-a-Judge        73.62 ± 1.76      78.51 ± 2.18        75.97 ± 1.60            89.12 ± 0.72
   Step-based Judgment          89.43 ± 2.43        36.36 ± 1.29        51.69 ± 1.46            85.11 ± 0.39


judgements. This motivates us to use GenSelect to select the best judgement among multiple judgements
generated by the LLM. Since GenSelect shows strong performance in proof selection, we hypothesize that it
can also help in selecting better judgements too. That is, given a problem, a proof, and 𝑛𝑗 judgements, we
use GenSelect to select the best judgement among the 𝑛𝑗 judgements and use that judgement to evaluate
the proof. We run this genselect for 𝑛𝑗 seeds and report the majority@5 results in Table 4. We observe
improvements in precision and F1 for both GPT-OSS-120 and Qwen3-30B-A3-Thinking, while recall drops
slightly. However, when incorporating GenSelect into proof-selection (i.e., selecting the best proof among
candidates), we observe no performance improvement. This suggests that GenSelect is particularly beneficial
for absolute judgement selection, where choosing a threshold is not possible, but does not provide gains in the
proof-selection setting.




                                                                                                               14
           Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




                                                           OPC best of n=6
                                          41
                                          40
                           Accuracy (%)


                                          39
                                          38
                                          37
                                                                                GPT-OSS 120B
                                               5   10     15    20   25    30       35   40   45
                                                        Number of Judgements (nj)

Figure 5: GPT-OSS-120B LLM-as-a-Judge performance on selecting the best proof among 6 generated proofs
from OPC pass@n subset. We vary the number of judgements from 1 to 45 and observe that the performance
saturates at around 32 judgements.




Table 4: GPT-OSS-120B and Qwen3-30B-A3-Thinking evaluation. We report precision, recall, and F1 for
proof problems, and precision for final-answer problems.

                                                               VerProofArena              Final-Answer (Challenge-19)
 Model                        Judgement
                                                         Precision   Recall      F1                Precision
 GPT-OSS-120                  LLM-as-Judge                46.28      99.17      63.10                86.18
 GPT-OSS-120                  Judge GenSelect             54.46      91.21      68.19                90.13
 Qwen3-30B-A3-Thinking        LLM-as-Judge                22.08      99.96      37.23                60.41
 Qwen3-30B-A3-Thinking        Judge GenSelect             30.65      94.49      46.29                66.26




                                                                                                                        15
              Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




Table 5: Majority@5 Results for VerProofArena and Challenge-19 Evaluation sets, averaged across 32 seeds.
We ablate various prompts under Prompt 𝑖 (Ablation).

                                                  VerProofArena                               Final Answers (Challenge-19)
 Prompt
                               Precision        Recall          F1         Avg Tokens     Precision        Recall      Avg Tokens
                                              Qwen3-30B-A3B-Thinking-2507
 General Summary              18.28 ± 0.28   99.89 ± 0.45   30.91 ± 0.41      8587      58.21 ± 1.37    74.86 ± 2.19     11813
 GIMO                         57.58 ± 2.30   87.06 ± 2.95   69.28 ± 2.09      8503      64.85 ± 5.88    15.53 ± 2.39     10025
 GIMO (Ablation 1)            56.01 ± 1.95   88.72 ± 2.34   68.65 ± 1.87      8664      62.04 ± 4.59    17.14 ± 1.83     10352
 GIMO (Ablation 2)            54.69 ± 2.53   88.98 ± 2.31   67.70 ± 2.17      8779      65.31 ± 3.97    18.55 ± 1.74     10716
 OPC                          22.88 ± 0.57   99.96 ± 0.26   37.23 ± 0.76      6327      60.41 ± 1.52    67.43 ± 2.30      8609
 OPC (Rubric)                 24.46 ± 0.51   99.89 ± 0.45   39.30 ± 0.67      6046      92.25 ± 1.44    77.45 ± 2.25     10211
 Prompt 1 (Ablation)          19.43 ± 0.30      100.00      32.54 ± 0.42      7276      58.23 ± 1.40    78.39 ± 1.70     9793
 Prompt 2 (Ablation)          20.68 ± 0.35      100.00      34.27 ± 0.49      6856      59.21 ± 1.21    73.08 ± 1.91     9323
 Prompt 3 (Ablation)          21.99 ± 0.47   99.36 ± 0.97   36.01 ± 0.65      7774      61.42 ± 1.32    76.27 ± 1.92     10994
 Prompt 4 (Ablation)          23.77 ± 0.46   99.96 ± 0.26   38.41 ± 0.60      6634      60.32 ± 1.90    64.41 ± 2.73      8995
 Prompt 5 (Ablation)          16.65 ± 0.21   99.96 ± 0.26   28.54 ± 0.32      7757      56.64 ± 1.17    81.63 ± 1.98     11123
 Prompt 5 (Rubric)            22.27 ± 0.38   96.53 ± 1.15   36.18 ± 0.55      5999      98.54 ± 0.64    94.76 ± 1.35     11273
 Prompt 6 (Rubric)            27.28 ± 0.69   99.02 ± 1.15   42.77 ± 0.88      5656      95.21 ± 1.68    74.61 ± 2.77     10182
 OPC RL                       54.03 ± 1.81   94.57 ± 2.44   68.75 ± 1.76      5271      62.59 ± 3.59    17.18 ± 1.50      6070
 OPC RL (Rubric)              39.72 ± 1.06   98.98 ± 1.32   56.69 ± 1.15      5380      98.15 ± 0.68    50.02 ± 2.60      8238
 OPC RL (GT-Proof→Rubric)     39.09 ± 1.24   98.64 ± 1.25   55.99 ± 1.38      5362      98.12 ± 1.28    49.06 ± 2.67      8216
 OPC RL (No-Rubric→Rubric)    59.74 ± 2.53   95.09 ± 2.33   73.35 ± 2.27      4997      99.31 ± 1.59    21.27 ± 1.95      6897
 GIMO RL                      49.66 ± 1.50   95.81 ± 2.21   65.40 ± 1.52      6008      66.29 ± 3.47    22.65 ± 1.87      7041
                                                         GPT-OSS-120B
 General Summary              41.82 ± 1.44   95.47 ± 1.73   58.15 ± 1.57     17443      86.32 ± 2.53    52.67 ± 2.31     30709
 GIMO                         94.11 ± 3.26   45.09 ± 3.07   60.90 ± 2.96     15599      94.60 ± 12.18    2.00 ± 1.41     24512
 GIMO (Ablation 1)            96.22 ± 2.78   54.26 ± 3.95   69.29 ± 3.24     12933      83.50 ± 26.90    1.84 ± 1.09     21280
 GIMO (Ablation 2)            94.82 ± 3.08   55.13 ± 4.36   69.62 ± 3.62     12977      85.78 ± 19.59    2.86 ± 1.33     22172
 OPC                          46.28 ± 1.24   99.17 ± 1.08   63.10 ± 1.22     16807       86.18 ± 2.53   50.29 ± 1.89     32529
 OPC (Rubric)                 44.32 ± 1.29   99.89 ± 0.45   61.39 ± 1.25     10502       99.61 ± 0.79   49.22 ± 2.70     16848
 Prompt 1 (Ablation)          47.65 ± 1.40   97.96 ± 1.12   64.10 ± 1.38     11267       82.23 ± 2.38   37.84 ± 2.42     24112
 Prompt 2 (Ablation)          46.99 ± 0.94   98.04 ± 1.36   63.52 ± 0.97     10616       81.56 ± 2.47   33.35 ± 1.59     21565
 Prompt 3 (Ablation)          48.29 ± 1.39   97.21 ± 1.15   64.52 ± 1.34     10468       83.16 ± 2.07   34.88 ± 1.98     21268
 Prompt 4 (Ablation)          46.12 ± 1.00   98.83 ± 1.30   62.88 ± 1.07     11388       81.75 ± 1.78   39.06 ± 2.30     20479
 Prompt 5 (Ablation)          44.55 ± 1.21   99.58 ± 0.78   61.56 ± 1.21     12478       85.22 ± 1.88   49.12 ± 2.00     24336
 Prompt 5 (Rubric)            47.36 ± 1.25   89.51 ± 1.74   61.93 ± 1.29      4587          100.00      67.39 ± 2.87     13153
 Prompt 6 (Rubric)            46.47 ± 1.18   98.34 ± 1.29   63.11 ± 1.26      9273      99.81 ± 0.57    50.76 ± 2.33     16418
                                                          GLM-4.5-Air
 General Summary              20.49 ± 0.56   94.53 ± 1.86   33.68 ± 0.82     16168      62.01 ± 1.92    60.65 ± 2.82     20373
 GIMO                         54.63 ± 3.16   83.89 ± 3.50   66.13 ± 3.04     11006      70.35 ± 6.45    20.75 ± 2.65     13866
 OPC                          20.90 ± 0.49   95.89 ± 1.72   34.32 ± 0.71     13331      67.88 ± 2.14    66.02 ± 2.74     19184




                                                                                                                                 16
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




Table 6: Majority@5 results for VerProofBench. The setting is similar to Table 5.

                                                                     VerProofBench
        Prompt
                                               Precision          Recall              F1         Avg Tokens
                                      Qwen3-30B-A3B-Thinking-2507
        General Summary                      33.40 ± 0.68      86.55 ± 1.20     48.19 ± 0.78         8389
        GIMO                                 75.76 ± 2.34      55.81 ± 1.99     64.25 ± 1.83         8048
        GIMO (Ablation 1)                    77.45 ± 2.58      56.81 ± 2.02     65.52 ± 1.85         8128
        GIMO (Ablation 2)                    73.73 ± 2.12      58.23 ± 1.76     65.05 ± 1.38         8231
        OPC                                  39.16 ± 0.70      91.13 ± 1.01     54.77 ± 0.75         6150
        OPC (Rubric)                         60.76 ± 1.47      84.74 ± 2.18     70.77 ± 1.57         4796
        Prompt 1 (Ablation)                  36.16 ± 0.67      89.96 ± 1.23     51.58 ± 0.79         7123
        Prompt 2 (Ablation)                  38.34 ± 0.78      90.51 ± 1.20     53.86 ± 0.88         6637
        Prompt 3 (Ablation)                  39.20 ± 0.82      88.15 ± 1.35     54.26 ± 0.94         7180
        Prompt 4 (Ablation)                  43.25 ± 0.99      86.98 ± 1.81     57.76 ± 1.16         6277
        Prompt 5 (Ablation)                  32.04 ± 0.51      91.26 ± 0.96     47.43 ± 0.65         7466
        Prompt 5 (Rubric)                    59.84 ± 1.42      88.02 ± 1.36     71.24 ± 1.23         4904
        Prompt 6 (Rubric)                    63.54 ± 1.67      82.26 ± 1.65     71.68 ± 1.39         4650
        OPC RL                               73.66 ± 1.93      66.15 ± 2.28     69.68 ± 1.81         4644
        OPC RL (Rubric)                      77.21 ± 1.76      75.85 ± 1.62     76.51 ± 1.33         3926
        OPC RL (GT-Proof→Rubric)             75.79 ± 1.70      76.19 ± 1.90     75.98 ± 1.56         3948
        OPC RL (No-Rubric→Rubric)            86.71 ± 2.48      59.00 ± 2.39     70.19 ± 2.00         3747
                                                 GPT-OSS-120B
        General Summary                      67.66 ± 2.37      67.09 ± 1.25     67.35 ± 1.41         14980
        GIMO                                 94.95 ± 1.88      26.19 ± 1.88     41.02 ± 2.33         12723
        GIMO (Ablation 1)                    95.50 ± 1.35      26.15 ± 1.58     41.03 ± 1.96         12534
        GIMO (Ablation 2)                    95.03 ± 1.89      26.53 ± 2.30     41.43 ± 2.86         12628
        OPC                                  73.62 ± 1.76      78.51 ± 2.18     75.97 ± 1.60         12650
        OPC (Rubric)                         80.00 ± 1.55      79.91 ± 1.98     79.94 ± 1.42          6672
        Prompt 1 (Ablation)                  76.97 ± 1.66      70.98 ± 1.56     73.84 ± 1.18         11351
        Prompt 2 (Ablation)                  77.92 ± 1.85      71.02 ± 1.45     74.30 ± 1.18          9934
        Prompt 3 (Ablation)                  78.76 ± 1.96      69.57 ± 1.56     73.87 ± 1.33          9526
        Prompt 4 (Ablation)                  76.06 ± 1.83      74.91 ± 2.07     75.47 ± 1.53         10781
        Prompt 5 (Ablation)                  74.75 ± 1.67      74.15 ± 1.43     74.44 ± 1.27         12130
        Prompt 5 (Rubric)                    81.77 ± 1.76      80.06 ± 1.58     80.89 ± 1.23          4609
        Prompt 6 (Rubric)                    81.11 ± 1.84      79.72 ± 1.85     80.40 ± 1.59          5902
                                                  GLM-4.5-Air
        General Summary                      37.86 ± 0.89      82.04 ± 1.72     51.80 ± 1.05         14638
        GIMO                                 72.90 ± 2.66      60.85 ± 3.18     66.29 ± 2.60         10539
        OPC                                  42.47 ± 1.02      88.89 ± 1.61     57.47 ± 1.08         12437




                                                                                                              17
              Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



C. Prompts
We take our proof generation prompt from the OPC [7]. To generate proofs for final-answer problems, we add
one more sentence to the prompt and ask it to put its final answer within boxed.

  OPC Proof Generation Prompt

  Your task is to write a proof solution to the following problem. Your proof will be graded by human judges for accuracy,
       thoroughness, and clarity. When you write your proof, follow these guidelines:

  − You are creating a proof, not a proof outline. Each step should be carefully explained and documented. If not properly
        explained, the judge will assume that you cannot explain it, and therefore decrease your grade.
  − You can use general theorems and lemmas, but only if they are well−known. As a rule of thumb: if the result has a
       name and is famous enough to have a Wikipedia page or something similar to describe it, it is allowed. Any result
       from papers that would not be taught in high−school or low−level bachelor courses in mathematics should not be
       used. Any use of such results will immediately give you a zero grade.
  − Do not skip computation steps in your proof. Clearly explain what transformations were done and why they are
       allowed in each step of a calculation.
  − You should use correct LaTeX notation to write equations and mathematical symbols. You should encompass these
       equations in appropriate symbols ("\(" and "\)" for inline math, "\[" and "\]" for block math) to enhance the clarity
        of your proof. Do not use any unicode characters.
  − Your proof should be self−contained.
  − If you are not sure about a specific step, or do not know how to prove an intermediate result, clearly state this. It is
       much preferable to indicate your uncertainty rather than making incorrect statements or claims.

  {problem}



  OPC Judgement Prompt
  You are judging the correctness of an LLM−generated proof for a math problem.

  ### Input:

  Your input will consist of the following components:
  − ∗∗Problem Statement∗∗: A mathematical problem that the proof is attempting to solve.
  − ∗∗Proof Solution∗∗: The proof that you need to evaluate. This proof may contain errors, omissions, or unclear steps.
       The proof was generated by another language model, which was given the following instructions:
  <model_prompt>
  − You are creating a proof, not a proof outline. Each step should be carefully explained and documented. If not properly
        explained, the judge will assume that you cannot explain it, and therefore decrease your grade.
  − You can use general theorems and lemmas, but only if they are well−known. As a rule of thumb: if the result has a
       name and is famous enough to have a Wikipedia page or something similar to describe it, it is allowed. Any result
       from papers that would not be taught in high school or low−level bachelor courses in mathematics should not be
       used. Any use of such results will immediately give you a zero grade.
  − Do not skip computation steps in your proof. Clearly explain what transformations were done and why they are
       allowed in each step of a calculation.
  − You should use correct LaTeX notation to write equations and mathematical symbols. You should encompass these
       equations in appropriate symbols ("\\(" and "\\)" for inline math, "\\[" and "\\]" for block math) to enhance the
       clarity of your proof. Do not use any unicode characters.
  − Your proof should be self−contained.
  − If you are not sure about a specific step, or do not know how to prove an intermediate result, clearly state this. It is
       much preferable to indicate your uncertainty rather than making incorrect statements or claims.
  </model_prompt>

  ### How the solution should be graded:
  A solution should be considered correct even if it would earn 5+/7 points in a standard grading format. Examples of
       small penalties worth 1 point are if the solution:
  − Makes a small computational mistake that can be easily fixed
  − Misses an edge case which can be easily proven/disproven
  − Skips over a step that follows without much reasoning or manual work
  Depending on the severity and the context, you may also not penalise a given error. On the other hand, a solution should
        be marked as incorrect if:
  − It marks a step as trivial, if it is not immediately obvious with little reasoning why this would be the case.
  − It omits algebra−heavy computational steps, regardless of whether or not it has outlined the methodology. Skipping
       shorter computations should be permitted.
  − Generalizes over a pattern without rigorously describing the pattern, or without proving any relevant properties.




                                                                                                                               18
             Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



− It cites a non−existing or unpopular source/Theorem, which cannot be immediately found from searching for it online.
      Thus, any theorems that can be immediately found and have a Wikipedia article are allowed.

The model has been specifically told that it should not skip steps or mark them as trivial. Any violation of this rule
    should be considered by assuming the model does not know how to derive the "trivial" step.

### Scoring instructions

If you believe the proof is correct, end your analysis with the following two tags:
<summary>One−paragraph summary explaining why the proof is correct</summary>
<judgement>Judgement: Yes</judgement>.

If you believe the proof is incorrect, end your analysis with the following two tags:
<summary>One−paragraph summary explaining why the proof is incorrect</summary>
<judgement>Judgement: No</judgement>.

### Problem Statement:
{problem}

### Model Solution:
{proof}



General Summary Judgement Prompt

[Instructions]

I will provide a math problem along with a solution. Your task is to review each step of the solution in sequence,
      analyzing, verifying, and critiquing the reasoning in detail. You need to provide the analyses and the conclusion in
      the following format:

∗ When you analyze each step, you should use proper verification, recalculation, or reflection to indicate whether it is
      logically and mathematically valid. Please elaborate on the analysis process carefully.
∗ If an error is detected in any step, you should describe the nature and cause of the error in detail, and suggest how to
      correct the error or the correct approach. Once a step is found to contain any error, stop further analysis of
      subsequent steps and provide your judgement.
∗ If no error is detected in any step, you should provide your judgement.

[Format]

After your analysis and conclusion, your response MUST follow this exact format:

For correct solutions, you must end your response with:
<summary>One−paragraph summary explaining why the solution is correct</summary>
<judgement>Judgement: Yes</judgement>

For incorrect solutions, you must end your response with:
<summary>One−paragraph summary explaining why the solution is incorrect</summary>
<judgement>Judgement: No</judgement>

[Problem]

{problem}

[Solution]

{proof}



GIMO Judgement Prompt
You are an expert mathematician and a meticulous grader for an International Mathematical Olympiad (IMO) level
     exam. Your primary task is to rigorously verify the provided mathematical solution. A solution is to be judged
     correct ∗∗only if every step is rigorously justified.∗∗ A solution that arrives at a correct final answer through flawed
     reasoning, educated guesses, or with gaps in its arguments must be flagged as incorrect or incomplete.

### Instructions ###




                                                                                                                                19
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




∗∗1. Core Instructions∗∗
∗ Your sole task is to find and report all issues in the provided solution. You must act as a ∗∗verifier∗∗, NOT a solver. ∗∗
     Do NOT attempt to correct the errors or fill the gaps you find.∗∗
∗ You must perform a ∗∗step−by−step∗∗ check of the entire solution. This analysis will be presented in a ∗∗Detailed
     Verification Log∗∗, where you justify your assessment of each step: for correct steps, a brief justification suffices; for
      steps with errors or gaps, you must provide a detailed explanation.

∗∗2. How to Handle Issues in the Solution∗∗
When you identify an issue in a step, you MUST first classify it into one of the following two categories and then follow
     the specified procedure.

∗ ∗∗a. Critical Error:∗∗
  This is any error that breaks the logical chain of the proof. This includes both ∗∗logical fallacies∗∗ (e.g., claiming that ‘
       A>B, C>D‘ implies ‘A−C>B−D‘) and ∗∗factual errors∗∗ (e.g., a calculation error like ‘2+3=6‘).
  ∗ ∗∗Procedure:∗∗
      ∗ Explain the specific error and state that it ∗∗invalidates the current line of reasoning∗∗.
      ∗ Do NOT check any further steps that rely on this error.
      ∗ You MUST, however, scan the rest of the solution to identify and verify any fully independent parts. For
            example, if a proof is split into multiple cases, an error in one case does not prevent you from checking the
            other cases.

∗ ∗∗b. Justification Gap:∗∗
  This is for steps where the conclusion may be correct, but the provided argument is incomplete, hand−wavy, or lacks
       sufficient rigor.
  ∗ ∗∗Procedure:∗∗
      ∗ Explain the gap in the justification.
      ∗ State that you will ∗∗assume the step’s conclusion is true∗∗ for the sake of argument.
      ∗ Then, proceed to verify all subsequent steps to check if the remainder of the argument is sound.

∗∗3. Output Format∗∗
Your response MUST be structured into three XML sections with the tags: <summary>, <detailed_verification>, and <
     judgement>.

∗ ∗∗a. Summary∗∗
  Wrap this section within <summary>...</summary> tags.
  This section MUST be at the very beginning of your response. It must contain two components:
  ∗ ∗∗Final Verdict∗∗: A single, clear sentence declaring the overall validity of the solution. For example: "The solution is
         correct," "The solution contains a Critical Error and is therefore invalid," or "The solution’s approach is viable
        but contains several Justification Gaps."
  ∗ ∗∗List of Findings∗∗: A bulleted list that summarizes ∗∗every∗∗ issue you discovered. For each finding, you must
        provide:
      ∗ ∗∗Location:∗∗ A direct quote of the key phrase or equation where the issue occurs.
      ∗ ∗∗Issue:∗∗ A brief description of the problem and its classification (∗∗Critical Error∗∗ or ∗∗Justification Gap∗∗).

∗ ∗∗b. Detailed Verification Log∗∗
  Wrap this section within <detailed_verification>...</detailed_verification> tags.
  Following the summary, provide the full, step−by−step verification log as defined in the Core Instructions. When you
       refer to a specific part of the solution, ∗∗quote the relevant text∗∗ to make your reference clear before providing
       your detailed analysis of that part.

∗ ∗∗c. Judgement∗∗
  This section MUST be at the very end of your response. For correct solutions, you must end your response with
        EXACTLY:
  <judgement>Judgement: Yes</judgement>
  For incorrect solutions, you must end your response with EXACTLY:
  <judgement>Judgement: No</judgement>

∗∗Example of the Required Summary Format∗∗
∗This is a generic example to illustrate the required format. Your findings must be based on the actual solution provided
     below.∗

<summary>
∗∗Final Verdict:∗∗ The solution is ∗∗invalid∗∗ because it contains a Critical Error.

∗∗List of Findings:∗∗
∗ ∗∗Location:∗∗ "By interchanging the limit and the integral, we get..."
  ∗ ∗∗Issue:∗∗ Justification Gap − The solution interchanges a limit and an integral without providing justification, such
        as proving uniform convergence.




                                                                                                                                  20
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



∗ ∗∗Location:∗∗ "From $A > B$ and $C > D$, it follows that $A−C > B−D$"
  ∗ ∗∗Issue:∗∗ Critical Error − This step is a logical fallacy. Subtracting inequalities in this manner is not a valid
       mathematical operation.
</summary>

======================================================================

### Problem ###

{problem}

======================================================================

### Solution ###

{proof}

======================================================================

### Verification Task Reminder ###

Your task is to act as an IMO grader. Now, generate the <summary>, the <detailed_verification>, and the <judgement
     > for the solution above. In your log, justify each correct step and explain in detail any errors or justification gaps
     you find, as specified in the instructions above. End your response with the required XML tags.



Proof GenSelect Prompt

[Instructions]
You are a senior mathematician. You are given a math problem and a list of {num_participants} candidate solutions
      written by different students.
Your task as a senior mathematician is to carefully analyze the solutions and pick the best solution from the list.

[Format]
Your output must end with the following tags:
<analysis>One−paragraph summary of your analysis of the solutions</analysis>
<best_solution>Index</best_solution>

The best_solution tag MUST ONLY contain an integer between 1 and {num_participants} (inclusive).



ProofBench 7-Point Grading Prompt
You are an ∗∗expert math proof grader∗∗. You are judging the
correctness of an LLM−generated proof for a math problem.

### Input

Your input will consist of:

∗ ∗∗Problem Statement∗∗: A mathematical problem that the proof is
attempting to solve.
∗ ∗∗Proof Solution∗∗: The proof that you need to evaluate. This
proof may contain errors, omissions, or unclear steps. The proof
was generated by another language model.

### Task

Analyze the proof carefully.

∗ Identify logical errors, incorrect steps, or unclear reasoning.
∗ Give an ∗∗integer∗∗ score between 0 and 7 with a brief overall
assessment.

### Output Format

Respond with ∗∗only∗∗ well−formed XML using the structure below.




                                                                                                                               21
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



Do not include any extra text or Markdown.

∗∗Requirements:∗∗
− ‘<score>‘ must be an integer in [0, 7].
− ‘<assessment>‘ must be a ∗∗detailed analysis∗∗ that explains your
reasoning step−by−step and provides a clear ∗∗rationale for the
score∗∗. Reference specific claims/lines if present.
− ‘<errors>‘ must be a list of specific issues (empty if score = 7).

Example output:

<score>0</score>
<assessment>The proof shows a good understanding of the main idea,
but has some unclear reasoning and minor mistakes...</assessment>
<errors>
  1. specific error 1,
  2. specific error 2,
  ...
</errors>

### Scoring Guidelines (0−7 scale)

∗ ∗∗0∗∗: Completely incorrect; proof is irrelevant, nonsensical, or
shows no understanding.
∗ ∗∗1−2∗∗: Very poor; major logical flaws, does not solve the problem,
but may contain fragments of relevant reasoning.
∗ ∗∗3−4∗∗: Partial progress; captures some correct reasoning or key
ideas, but has significant logical errors, missing steps, or
incomplete arguments that make the proof invalid overall.
∗ ∗∗5−6∗∗: Largely correct; the proof is overall valid and reaches
the correct conclusion. Contains only ∗∗minor issues∗∗ (e.g., small
calculation mistakes, notation slips, or slightly unclear wording)
that do not undermine correctness.
∗ ∗∗7∗∗: Fully correct; the proof is complete, logically sound, and
clearly presented with no substantive errors.

−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
∗∗Problem Statement∗∗
{problem}

∗∗Proof Solution∗∗
{proof}



ProofBench 7-Point Binary Prompt

You are an ∗∗expert math proof grader∗∗. You are judging the
correctness of an LLM−generated proof for a math problem.

### Input

Your input will consist of:

∗ ∗∗Problem Statement∗∗: A mathematical problem that the proof is
attempting to solve.
∗ ∗∗Proof Solution∗∗: The proof that you need to evaluate. This
proof may contain errors, omissions, or unclear steps. The proof
was generated by another language model.

### Task

Analyze the proof carefully and determine if it is correct or incorrect.

∗ Identify logical errors, incorrect steps, or unclear reasoning.
∗ Evaluate the proof using the scoring guidelines below to decide if
it should be considered correct (score 6−7) or incorrect (score 0−5).

### Output Format




                                                                                                              22
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




If you believe the proof is correct (would score 6 or 7), end your analysis with:
<summary>One−paragraph summary explaining why the proof is correct</summary>
<judgement>Judgement: Yes</judgement>

If you believe the proof is incorrect (would score 0−5), end your analysis with:
<summary>One−paragraph summary explaining why the proof is incorrect</summary>
<judgement>Judgement: No</judgement>

### Scoring Guidelines (0−7 scale)

∗ ∗∗0∗∗: Completely incorrect; proof is irrelevant, nonsensical, or
shows no understanding.
∗ ∗∗1−2∗∗: Very poor; major logical flaws, does not solve the problem,
but may contain fragments of relevant reasoning.
∗ ∗∗3−4∗∗: Partial progress; captures some correct reasoning or key
ideas, but has significant logical errors, missing steps, or
incomplete arguments that make the proof invalid overall.
∗ ∗∗5−6∗∗: Largely correct; the proof is overall valid and reaches
the correct conclusion. Contains only ∗∗minor issues∗∗ (e.g., small
calculation mistakes, notation slips, or slightly unclear wording)
that do not undermine correctness.
∗ ∗∗7∗∗: Fully correct; the proof is complete, logically sound, and
clearly presented with no substantive errors.

−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
∗∗Problem Statement∗∗
{problem}

∗∗Proof Solution∗∗
{proof}



ProofBench 7-Point Grading + Ground Truth + Rubric Prompt

You are an ∗∗expert math proof grader∗∗. You are judging the
correctness of an LLM−generated proof for a math problem.

### Input

Your input will consist of:

∗ ∗∗Problem Statement∗∗: A mathematical problem that the proof
is attempting to solve.
∗ ∗∗Reference Solution∗∗: A correct solution or proof provided
for reference. This is ∗∗not necessarily the only valid solution∗∗.
If the problem requires a final numeric or algebraic answer, this
section contains the correct answer, which should be the only
accepted final answer (though alternative reasoning paths are valid).
∗ ∗∗Marking Scheme∗∗: A problem−specific grading rubric (0−7 scale)
with checkpoints, zero−credit items, and deductions. ∗∗Treat this
scheme as advisory guidance, not a script.∗∗ Use it to anchor
scoring, but ∗∗do not require∗∗ the proof to follow the same
order, lemmas, or technique if its reasoning is mathematically
sound.
∗ ∗∗Proof Solution∗∗: The proof that you need to evaluate. This
proof may contain errors, omissions, or unclear steps. The proof
was generated by another language model.

### Task

Analyze the proof carefully.

∗∗Core principles (in order of precedence):∗∗
1) ∗∗Mathematical validity∗∗ of the proof’s reasoning and conclusion.
2) ∗∗Problem constraints∗∗ (e.g., unique required final value;
forbidden tools if stated).
3) ∗∗Advisory mapping to the marking scheme∗∗ (checkpoints/




                                                                                                              23
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



deductions), allowing different orders and techniques.
4) ∗∗Reference solution∗∗ as an anchor for sufficiency, not
exclusivity.

∗∗Alternative−approach policy:∗∗
− If the proof uses a different but valid method, ∗∗map its
steps to equivalent rubric checkpoints∗∗ (same logical role)
and award points accordingly.
− ∗∗Do not penalize∗∗ solely for re−ordering steps, using
different lemmas, or giving a correct shortcut, ∗∗unless∗∗
the problem forbids it.
− Apply zero−credit items/deductions ∗∗only when the underlying
issue actually occurs∗∗ in the given proof’s approach; ∗∗do not
auto−penalize∗∗ for omitting a rubric step that is unnecessary
under the alternative method.
− Avoid double−counting mutually exclusive items; if two items
solve the same logical gap, ∗∗award the larger only∗∗.
− If the final numeric/algebraic answer is wrong where uniqueness
is required, award only partial credit justified by correct
intermediate reasoning.

∗∗Rigor and evidence:∗∗
− Award credit for intermediate claims ∗∗only if adequately
justified∗∗ within the proof (not merely asserted).
− If a step is plausible but under−justified, award ∗∗conservative
partial credit∗∗ and note what is missing.

∗∗What to produce:∗∗
− Identify logical errors, incorrect steps, or unclear reasoning.
− Give a ∗∗score between 0 and 7∗∗ with a ∗∗detailed assessment∗∗.
− ∗∗Within the assessment text∗∗, show clearly how the score was
derived:
  − Which rubric checkpoints (or their ∗∗mapped equivalents∗∗)
  were earned and the points you awarded.
  − Any zero−credit items or deductions you applied (and why).
  − How these add up to the final integer score in [0−7].

### Output Format

Respond with ∗∗only∗∗ well−formed XML using the structure below.
Do not include any extra text or Markdown.

∗∗Requirements:∗∗
− ‘<score>‘ must be an integer in [0, 7].
− ‘<assessment>‘ must be a ∗∗detailed analysis∗∗ that explains
your reasoning step−by−step and provides a clear ∗∗rationale for
the score∗∗. Reference specific claims/lines if present. Include
the scoring breakdown ∗∗in prose∗∗ here (earned checkpoints or
mapped equivalents, deductions, and subtotal −> final score).
− ‘<errors>‘ must be a list of specific issues (empty if score = 7).

Example output:

<score>0</score>
<assessment>The proof shows a good understanding of the main idea,
but has some unclear reasoning and minor mistakes...</assessment>
<errors>
  1. specific error 1,
  2. specific error 2,
  ...
</errors>

−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
∗∗Problem Statement∗∗
{problem}

∗∗Reference Solution∗∗
{ground_truth_proof}




                                                                                                              24
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



 ∗∗Marking Scheme∗∗
 {rubric}

 ∗∗Proof Solution∗∗
 {proof}




D. Output Examples

  Incorrect GPT-5-thinking-high Judgement for USAMO2025-P5.

  Problem: Determine, with proof, all positive integers 𝑘 such that
                                                                          𝑛       (︂ )︂𝑘
                                                                 1 ∑︁ 𝑛
                                                                𝑛+1   𝑖
                                                                         𝑖=0

  is an integer for all positive integers 𝑛.

  GPT-OSS Generated Solution:
                                                                         𝑛    (︂ )︂𝑘
                                                           1 ∑︁ 𝑛
                                                 𝐴𝑘 (𝑛) =                                ,          𝑛 ≥ 1.
                                                          𝑛+1   𝑖
                                                                        𝑖=0
 ——————————————————————–
 ### 1. Odd exponents do **not** work
 Let 𝑘 be odd and let 𝑝 ≥ 3 be a prime. Put 𝑛 = 𝑝 − 1; then 𝑛 + 1 = 𝑝.
 For a prime 𝑝 one has the well-known congruence
                                           (︂        )︂
                                                𝑝−1
                                                          ≡ (−1)𝑖      (mod 𝑝)               (0 ≤ 𝑖 ≤ 𝑝 − 1)                       (1)
                                                 𝑖
                            (︂    )︂
                             𝑝−1              (𝑝 − 1)!
  (easily proved from                  =                  and Wilson’s theorem).
                              𝑖            𝑖!(𝑝 − 1 − 𝑖)!
  Hence, using (1),
                                   𝑝−1 (︂   )︂ 𝑘               𝑝−1                 𝑝−1
                                   ∑︁    𝑝−1                   ∑︁                  ∑︁
                                                           ≡         (−1)𝑖𝑘 =            (−1)𝑖 ≡ 1       (mod 𝑝).
                                                 𝑖
                                   𝑖=0                         𝑖=0                 𝑖=0
                                                                                                                    𝑝−1 (︂   )︂𝑘
                                                                                                                    ∑︁    𝑝−1
  The last congruence holds because the number of terms, 𝑝, is odd. Thus 𝑝 does **not** divide                                       ,
                                                                                                                               𝑖
                                                                                                                    𝑖=0
  so for the admissible 𝑛 = 𝑝 − 1
                                                                       𝑝−1   (︂          )︂ 𝑘
                                                                     1 ∑︁ 𝑝 − 1
                                                      𝐴𝑘 (𝑛) =                                  ∈
                                                                                                / Z.
                                                                     𝑝      𝑖
                                                                       𝑖=0

 Consequently no odd integer 𝑘 satisfies the required property.
 ——————————————————————–
 ### 2. Even exponents always work
 Now let 𝑘 = 2𝑚 (𝑚 ≥ 1). For a fixed 𝑛 denote
                      {︁                         ⃒                                                                        }︁
          ℳ𝑛,𝑚 =           𝑀 ∈ {0, 1} 𝑛×2𝑚 ⃒ each of the 2𝑚 columns of 𝑀 contains the same number of 1’s .
                                                 ⃒

  If the common column sum equals 𝑖 then the 𝑖 positions of the 1’s can be chosen independently in each column;
  therefore
                                                                           𝑛 (︂ )︂2𝑚
                                                                          ∑︁   𝑛
                                                            |ℳ𝑛,𝑚 | =                           .                                  (2)
                                                                                     𝑖
                                                                             𝑖=0
 ——————————————————————–
 #### 2.1 A cyclic action whose orbits have size 𝑛 + 1




                                                                                                                                         25
          Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



Consider a regular (𝑛 + 1)-gon whose vertices are labelled 0, 1, . . . , 𝑛 clockwise. Choose one vertex to be
*distinguished*; colour it by a special symbol *. On every remaining vertex place a colour taken from

                                𝐴 = {0, 1}2𝑚             (the set of binary 2𝑚-vectors).
The colouring is required to satisfy
                                                   ∑︁
                                                              𝑣 = (𝑖, 𝑖, . . . , 𝑖)                          (3)
                                                𝑣∈𝐴 placed

for some integer 𝑖 (0 ≤ 𝑖 ≤ 𝑛); in other words, the sum of the vectors attached to the 𝑛 ordinary vertices is a
constant vector. Let 𝒞𝑛,𝑚 be the set of all such coloured polygons.
The cyclic group 𝐶𝑛+1 acts on 𝒞𝑛,𝑚 by rotating the polygon one step clockwise. Because the special colour *
occurs on exactly one vertex, no non-trivial rotation can fix an element of 𝒞𝑛,𝑚 ; the action is **free**. Hence
every orbit of this action contains precisely 𝑛 + 1 elements and therefore

                                                |𝒞𝑛,𝑚 | ≡ 0      (mod 𝑛 + 1).                                (4)
——————————————————————–
#### 2.2 Bijection with ℳ𝑛,𝑚
Starting from a coloured polygon 𝑃 ∈ 𝒞𝑛,𝑚 read the colours of the ordinary vertices in clockwise order,
beginning with the vertex that follows the distinguished one. The obtained ordered list of 𝑛 binary vectors is
an element of ℳ𝑛,𝑚 .
Conversely, given a matrix 𝑀 ∈ ℳ𝑛,𝑚 , place its rows round a circle in the given order and insert the
distinguished vertex after the last row. Because the rows of 𝑀 have the same column sum, condition (3) is
fulfilled, so we obtain a coloured polygon belonging to 𝒞𝑛,𝑚 .
These two constructions are inverse to each other; consequently

                                                       |𝒞𝑛,𝑚 | = |ℳ𝑛,𝑚 |.                                    (5)
——————————————————————–
#### 2.3 Divisibility
From (2), (4) and (5) we get
                                    𝑛 (︂ )︂2𝑚                                         𝑛     (︂ )︂2𝑚
                                        𝑛                                  1 ∑︁ 𝑛
                                 ⃒ ∑︁
                             𝑛+1⃒                  ,       hence                                      ∈ Z.
                                 ⃒
                                            𝑖                             𝑛+1   𝑖
                                    𝑖=0                                               𝑖=0

Thus the required quotient is an integer for **every** even exponent 𝑘 = 2𝑚.
——————————————————————–
### 3. Conclusion
                      𝑛 (︂ )︂𝑘
                 1 ∑︁ 𝑛
The expression                   is an integer for all positive integers 𝑛 **iff** 𝑘 is even.
               𝑛+1          𝑖
                       𝑖=0

                                          𝑘 must be an even positive integer.
                                                                                       (︀     )︀
The proof uses only elementary number theory (the congruence 𝑝−1        𝑖
                                                                            ≡ (−1)𝑖 (mod 𝑝)) and a simple
combinatorial argument (a free cyclic action on coloured polygons). No deep theorems besides these well-known
facts are required.

GPT5-thinking-high Judgement:
<summary>The
(︀𝑝−1)︀           proof correctly shows that odd k fail by a modular arithmetic argument using the congruence
              𝑖
   𝑖
        ≡ (−1)  (𝑚𝑜𝑑𝑝), and that even k work via a clean combinatorial construction with a free cyclic group
action guaranteeing divisibility by n+1. The bijection and counting are clear, and the conclusion matches the
ground truth.</summary>
<judgement>Judgement: Yes</judgement>

Ground Truth Judgement:
The proof is incorrect due to erroneous combinatorial construction.




                                                                                                                   26
           Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



A correct proof to USAMO2025-P2 provided by our test-time scaling method.

Problem: Let 𝑛 and 𝑘 be positive integers with 𝑘 < 𝑛. Let 𝑃 (𝑥) be a polynomial of degree 𝑛 with real
coefficients, nonzero constant term, and no repeated roots. Suppose that for any real numbers 𝑎0 , 𝑎1 , . . . , 𝑎𝑘
such that the polynomial 𝑎𝑘 𝑥𝑘 + · · · + 𝑎1 𝑥 + 𝑎0 divides 𝑃 (𝑥), the product 𝑎0 𝑎1 · · · 𝑎𝑘 is zero. Prove that 𝑃 (𝑥)
has a nonreal root.

GPT-OSS Generated Solution:

                                                                Let 𝑛, 𝑘 ∈ N, 𝑘 < 𝑛.
                                                         𝑛
                    Theorem.                            ∏︁
                                       Let 𝑃 (𝑥) = 𝑐           (𝑥 − 𝑟𝑖 ), 𝑐 ̸= 0, 𝑟𝑖 ̸= 0, 𝑟𝑖 ̸= 𝑟𝑗 (𝑖 ̸= 𝑗).
                                                         𝑖=1

Assume that

                  for every real 𝑎0 , . . . , 𝑎𝑘 with 𝑎𝑘 𝑥𝑘 + · · · + 𝑎0 | 𝑃 (𝑥) one has 𝑎0 𝑎1 · · · 𝑎𝑘 = 0.      (1)
Then 𝑃 possesses a non-real zero.
———————————————————————
### 1. Reformulation in terms of elementary symmetric sums
For a set 𝑆 ⊆ {1, . . . , 𝑛} put
                                                                 |𝑆|
                                             ∏︁                  ∑︁
                                  𝑄𝑆 (𝑥) =         (𝑥 − 𝑟𝑖 ) =         (−1)|𝑆|−𝑗 𝑒|𝑆|−𝑗 (𝑆) 𝑥𝑗 ,                  (2)
                                             𝑖∈𝑆                 𝑗=0

where
                                                        ∑︁ ∏︁
                                           𝑒𝑚 (𝑆) =                  𝑟𝑖      (𝑚 ≥ 0)
                                                         𝐼⊆𝑆 𝑖∈𝐼
                                                        |𝐼|=𝑚

is the elementary symmetric sum of the numbers {𝑟𝑖 | 𝑖 ∈ 𝑆} (𝑒0 (𝑆) = 1). The coefficient of 𝑥𝑗 in (2) is a
non-zero constant multiple of 𝑒|𝑆|−𝑗 (𝑆). Consequently a divisor of degree 𝑘 of 𝑃 has a zero coefficient **iff**
for the corresponding 𝑘-subset 𝑆 we have

                                         𝑒𝑚 (𝑆) = 0      for some 𝑚 ∈ {1, . . . , 𝑘}.                             (3)
Thus condition (1) is equivalent to
> (*****) *Every* 𝑘-subset 𝑆 of {𝑟1 , . . . , 𝑟𝑛 } satisfies > (3).
———————————————————————

### 2. A combinatorial lemma
Lemma.

Let 𝑅 = {𝑥1 , . . . , 𝑥𝑘+1 } ⊂ R∖{0} be distinct. Then there exists a 𝑘-subset 𝑆 ⊂ 𝑅 with 𝑒𝑚 (𝑆) ̸= 0 (1 ≤ 𝑚 ≤ 𝑘).
                                                                                                             (4)
*Proof.* Suppose that (4) is false; then each of the 𝑘 + 1 subsets

                                         𝑆𝑖 := 𝑅 ∖ {𝑥𝑖 }           (𝑖 = 1, . . . , 𝑘 + 1)
contains a zero elementary symmetric sum. For each 𝑖 let

                                     𝑗𝑖 = min{ 𝑚 | 𝑒𝑚 (𝑆𝑖 ) = 0 } ∈ {1, . . . , 𝑘 − 1}                            (5)
                                                        ∏︀
(the case 𝑗𝑖 = 𝑘 cannot occur because 𝑒𝑘 (𝑆𝑖 ) = 𝑗̸=𝑖 𝑥𝑗 ̸= 0).
Because there are only 𝑘 − 1 possible values for the numbers 𝑗𝑖 and 𝑘 + 1 indices, the pigeon-hole principle
yields distinct 𝑖 ̸= ℓ with

                                                         𝑗𝑖 = 𝑗ℓ =: 𝑗.                                            (6)
Set 𝑇 := 𝑆𝑖 ∩ 𝑆ℓ = 𝑅 ∖ {𝑥𝑖 , 𝑥ℓ } (so |𝑇 | = 𝑘 − 1). From (2) we have for any 𝑡 ∈ R

                                           𝑒𝑗 (𝑇 ∪ {𝑡}) = 𝑒𝑗 (𝑇 ) + 𝑡 𝑒𝑗−1 (𝑇 ).                                  (7)
Applying (7) with 𝑡 = 𝑥𝑖 and with 𝑡 = 𝑥ℓ and using (6) gives




                                                                                                                         27
          Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection




                              𝑒𝑗 (𝑇 ) + 𝑥𝑖 𝑒𝑗−1 (𝑇 ) = 0,         𝑒𝑗 (𝑇 ) + 𝑥ℓ 𝑒𝑗−1 (𝑇 ) = 0.
Subtracting the two equalities and using 𝑥𝑖 ̸= 𝑥ℓ we obtain

                                            𝑒𝑗−1 (𝑇 ) = 0,           𝑒𝑗 (𝑇 ) = 0.                                 (8)
Hence the polynomial
                                           ∏︁
                                𝑄𝑇 (𝑥) =         (𝑥 − 𝑡) = 𝑥𝑘−1 + 𝑐𝑘−2 𝑥𝑘−2 + · · · + 𝑐0
                                           𝑡∈𝑇

has the two consecutive coefficients 𝑐𝑘−𝑗 = (−1)𝑗−1 𝑒𝑗−1 (𝑇 ) and 𝑐𝑘−𝑗−1 = (−1)𝑗 𝑒𝑗 (𝑇 ) equal to zero.


 Claim.    A polynomial whose zeros are distinct real numbers cannot have two consecutive zero coefficients.
                                                                                                               (9)
*Proof of the claim.* Let 𝑓 (𝑥) = 𝑥𝑚 + 𝑎𝑚−1 𝑥𝑚−1 + · · · + 𝑎0 have distinct real zeros. If 𝑎𝑟 = 𝑎𝑟−1 = 0 for some
1 ≤ 𝑟 ≤ 𝑚 − 1, then

                              𝑓 (𝑟) (0) = 𝑟!𝑎𝑟 = 0,       𝑓 (𝑟−1) (0) = (𝑟 − 1)!𝑎𝑟−1 = 0.
Thus 0 is a common zero of 𝑓 (𝑟−1) and 𝑓 (𝑟) . For a polynomial with simple real zeros, each derivative also
has simple real zeros and the zeros of 𝑓 (𝑟) interlace those of 𝑓 (𝑟−1) . Therefore two consecutive derivatives
cannot share a zero; otherwise that zero would be a multiple root of 𝑓 (𝑟−1) , contradicting simplicity. Hence the
assumption is impossible, proving the claim. ■
Applying the claim to 𝑄𝑇 contradicts (8). Consequently our assumption that every 𝑘-subset of 𝑅 is “bad” is
false, and (4) holds. ■
———————————————————————

### 3. From the lemma to the polynomial
Assume, to obtain a contradiction, that **all** zeros of 𝑃 are real. Let

                                     𝑅 := {𝑟1 , . . . , 𝑟𝑛 } ⊂ R ∖ {0}           (𝑛 > 𝑘).
If |𝑅| > 𝑘 + 1 choose an arbitrary subset 𝑅0 ⊂ 𝑅 with |𝑅0 | = 𝑘 + 1. Any 𝑘-subset of 𝑅0 is also a 𝑘-subset of 𝑅;
hence the hypothesis (*) for 𝑅 also holds for 𝑅0 . Applying the Lemma to 𝑅0 we obtain a 𝑘-subset 𝑆 ⊂ 𝑅0 for
which

                                            𝑒𝑚 (𝑆) ̸= 0        (1 ≤ 𝑚 ≤ 𝑘).                                      (10)
For this set 𝑆 the divisor
                                                             ∏︁
                                                  𝑄𝑆 (𝑥) =           (𝑥 − 𝑟𝑖 )
                                                             𝑟𝑖 ∈𝑆

has, by Vieta’s formulas, the coefficients (−1)𝑚 𝑒𝑚 (𝑆) (𝑚 = 0, . . . , 𝑘); (10) shows that none of them vanishes.
Hence 𝑄𝑆 is a divisor of 𝑃 of degree 𝑘 **with all coefficients non-zero**, contradicting the assumption (1).
Thus the assumption that all zeros of 𝑃 are real is impossible; at least one zero of 𝑃 is non-real. ■
———————————————————————

### 4. Remarks on the tools used
* Vieta’s formulas relate coefficients of a monic polynomial to the elementary symmetric sums of its zeros – a
standard algebraic fact.
* Rolle’s theorem (or the equivalent statement that a polynomial with simple real zeros has simple real zeros
for all its derivatives) is a classical result from elementary calculus and was used only in the proof of claim (9).
* The pigeon-hole principle and elementary counting were the only combinatorial tools needed.
All arguments are elementary; no deep results beyond those mentioned are required. ■


An incorrect proof to USAMO2025-P2 without test-time scaling method.

Problem: Let 𝑛 and 𝑘 be positive integers with 𝑘 < 𝑛. Let 𝑃 (𝑥) be a polynomial of degree 𝑛 with real
coefficients, nonzero constant term, and no repeated roots. Suppose that for any real numbers 𝑎0 , 𝑎1 , . . . , 𝑎𝑘
such that the polynomial 𝑎𝑘 𝑥𝑘 + · · · + 𝑎1 𝑥 + 𝑎0 divides 𝑃 (𝑥), the product 𝑎0 𝑎1 · · · 𝑎𝑘 is zero. Prove that 𝑃 (𝑥)




                                                                                                                         28
          Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



has a nonreal root.

GPT-OSS Generated Solution:
**Proof.** Let
                                                                         𝑛
                                                                        ∏︁
                                    𝑛 > 𝑘 ≥ 1,            𝑃 (𝑥) = 𝑐           (𝑥 − 𝑟𝑖 )         (𝑐 ̸= 0)
                                                                        𝑖=1

be a polynomial of degree 𝑛 with real coefficients, non-zero constant term, and without repeated roots. Thus
every root 𝑟𝑖 is a non-zero real number.
Assume, for a contradiction, that **all the roots of 𝑃 are real**. Consequently the roots 𝑟1 , . . . , 𝑟𝑛 are distinct
non-zero real numbers.
——————————————————————–
### 1. What we have to find
For a subset 𝑆 ⊂ {1, . . . , 𝑛} of size |𝑆| = 𝑘 set
                               ∏︁
                    𝑄𝑆 (𝑥) =         (𝑥 − 𝑟𝑖 ) = 𝑥𝑘 − 𝑒1 (𝑆)𝑥𝑘−1 + 𝑒2 (𝑆)𝑥𝑘−2 − · · · + (−1)𝑘 𝑒𝑘 (𝑆).                    (1)
                               𝑖∈𝑆

Here
                                                         ∑︁
                                      𝑒𝑗 (𝑆) =                     𝑟𝑖1 · · · 𝑟𝑖𝑗        (1 ≤ 𝑗 ≤ 𝑘)
                                                 {𝑖1 ,...,𝑖𝑗 }⊂𝑆

is the 𝑗-th elementary symmetric sum of the numbers {𝑟𝑖 | 𝑖 ∈ 𝑆}. Because none of the 𝑟𝑖 equals 0, the constant
term (−1)𝑘 𝑒𝑘 (𝑆) = (−1)𝑘 𝑖∈𝑆 𝑟𝑖 is never 0.
                          ∏︀
Hence a divisor 𝑄𝑆 of degree 𝑘 has **all its coefficients non-zero** iff

                                             𝑒𝑗 (𝑆) ̸= 0      for every 𝑗 = 1, . . . , 𝑘.                                (2)
If we can exhibit a subset 𝑆 of size 𝑘 satisfying (2), then the monic divisor 𝑄𝑆 of 𝑃 has all coefficients non-zero,
so the product of its coefficients is non-zero, contradicting the hypothesis that for every real divisor of degree at
most 𝑘 the product of its coefficients must be 0. Therefore it suffices to prove the existence of such a subset 𝑆.
——————————————————————–
### 2. The combinatorial Nullstellensatz
We shall use the following well-known result (Alon’s *Combinatorial Nullstellensatz*).
> **Theorem (Combinatorial Nullstellensatz).** > Let 𝐹 be a field, 𝑓 ∈ 𝐹 [𝑥1 , . . . , 𝑥𝑚 ] a polynomial. > Write
>                                         ∑︁
                                 >𝑓 =          𝑐𝛼 𝑥𝛼 1        𝛼𝑚
                                                   1 · · · > 𝑥𝑚 >      (𝑐𝛼 ∈ 𝐹 ). >
                                            𝛼∈N𝑚

> Suppose that for a particular 𝛽 = (𝛽1 , . . . , 𝛽𝑚 ) we > have 𝑐𝛽 = ̸ 0. Let 𝑆𝑖 ⊂ 𝐹 be finite sets with > |𝑆𝑖 | > 𝛽𝑖
for each 𝑖. Then there exist > (𝑠1 , . . . , 𝑠𝑚 ) ∈ 𝑆1 × · · · × 𝑆𝑚 > such that 𝑓 (𝑠1 , . . . , 𝑠𝑚 ) ̸= 0.
The theorem is valid over any field; we shall apply it over the field R.
——————————————————————–
### 3. Two auxiliary polynomials
For indeterminates 𝑥1 , . . . , 𝑥𝑘 let
                                                              ∑︁
                               𝐸𝑗 (𝑥1 , . . . , 𝑥𝑘 ) =                   𝑥𝑖1 · · · 𝑥𝑖𝑗         (1 ≤ 𝑗 ≤ 𝑘)
                                                     1≤𝑖1 <···<𝑖𝑗 ≤𝑘

be the elementary symmetric polynomial of degree 𝑗; thus 𝑒𝑗 (𝑆) = 𝐸𝑗 (𝑟𝑖1 , . . . , 𝑟𝑖𝑘 ) when 𝑆 = {𝑖1 , . . . , 𝑖𝑘 }.
Define
                                                                       𝑘
                                                                      ∏︁
                                            𝐹 (𝑥1 , . . . , 𝑥𝑘 ) =          𝐸𝑗 (𝑥1 , . . . , 𝑥𝑘 ).                       (3)
                                                                      𝑗=1

Next introduce the Vandermonde polynomial
                                                                         ∏︁
                                             𝑉 (𝑥1 , . . . , 𝑥𝑘 ) =                (𝑥𝑖 − 𝑥𝑗 ).                           (4)
                                                                      1≤𝑖<𝑗≤𝑘

𝑉 is non-zero exactly when the arguments are pairwise distinct and its total degree in each variable equals
𝑘 − 1.




                                                                                                                               29
            Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



Finally set

                                    𝐻(𝑥1 , . . . , 𝑥𝑘 ) = 𝐹 (𝑥1 , . . . , 𝑥𝑘 ) 𝑉 (𝑥1 , . . . , 𝑥𝑘 ).                               (5)
——————————————————————–
### 4. A monomial with a non-zero coefficient in 𝐻
Consider the monomial obtained from 𝐹 by taking from the factor 𝐸𝑗 the term 𝑥1 𝑥2 · · · 𝑥𝑗 (the product of the
first 𝑗 variables). This contributes the exponent vector

                                                        (𝑘, 𝑘 − 1, . . . , 1).                                                     (6)
                                                                           𝑘

                                                                                 𝑥𝑖𝑖−1 = 𝑥01 𝑥12 · · · 𝑥𝑘−1
                                                                         ∏︁
From the Vandermonde polynomial 𝑉 choose the term                                                       𝑘   , which corresponds to the
                                                                          𝑖=1
identity permutation in the usual expansion of the determinant. Adding the exponent vectors (6) and
(0, 1, . . . , 𝑘 − 1) gives

                                                            (𝑘, 𝑘, . . . , 𝑘).                                                     (7)
Hence the monomial

                                                𝑀 (𝑥1 , . . . , 𝑥𝑘 ) = 𝑥𝑘1 𝑥𝑘2 · · · 𝑥𝑘𝑘
appears in 𝐻 with coefficient 1 (̸= 0) (the product of the coefficients 1 from the two selected monomials).
Consequently the polynomial 𝐻 satisfies the hypothesis of the Nullstellensatz with

                                                   𝛽1 = 𝛽2 = · · · = 𝛽𝑘 = 𝑘.                                                       (8)
——————————————————————–
### 5. Applying the Nullstellensatz
Let

                                                  𝑆 = {𝑟1 , 𝑟2 , . . . , 𝑟𝑛 } ⊂ R.
Because the constant term of 𝑃 is non-zero, none of the 𝑟𝑖 is zero; moreover 𝑛 > 𝑘. For each variable 𝑥𝑖 we
take the same set 𝑆𝑖 = 𝑆. Then |𝑆𝑖 | = 𝑛 > 𝑘 = 𝛽𝑖 for all 𝑖, so the requirements of the Nullstellensatz are
fulfilled.
Hence there exist numbers

                                                           𝛼1 , . . . , 𝛼𝑘 ∈ 𝑆
such that

                                                      𝐻(𝛼1 , . . . , 𝛼𝑘 ) ̸= 0.                                                    (9)
Because the factor 𝑉 divides 𝐻, (9) implies 𝑉 (𝛼1 , . . . , 𝛼𝑘 ) ̸= 0; therefore the 𝛼𝑖 are **pairwise distinct**.
Consequently the set

                                            𝑆0 = {𝛼1 , . . . , 𝛼𝑘 } ⊂ {𝑟1 , . . . , 𝑟𝑛 }
has exactly 𝑘 elements.
From the definition (5) we have

                                   𝐻(𝛼1 , . . . , 𝛼𝑘 ) = 𝐹 (𝛼1 , . . . , 𝛼𝑘 ) 𝑉 (𝛼1 , . . . , 𝛼𝑘 ).
Since the second factor is non-zero, we must have 𝐹 (𝛼1 , . . . , 𝛼𝑘 ) ̸= 0. But 𝐹 is the product of the elementary
symmetric polynomials, hence
                                                            𝑘                               𝑘
                                                           ∏︁                              ∏︁
                                  𝐹 (𝛼1 , . . . , 𝛼𝑘 ) =         𝐸𝑗 (𝛼1 , . . . , 𝛼𝑘 ) =         𝑒𝑗 (𝑆0 ).
                                                           𝑗=1                             𝑗=1

Thus each elementary symmetric sum 𝑒𝑗 (𝑆0 ) is non-zero; i.e. condition (2) holds for 𝑆0 .
——————————————————————–
### 6. Constructing a divisor with all non-zero coefficients
Consider the monic polynomial




                                                                                                                                         30
          Scaling Generative Verifiers For Natural Language Mathematical Proof Verification And Selection



                            ∏︁
                   𝑄(𝑥) =          (𝑥 − 𝑟) = 𝑥𝑘 − 𝑒1 (𝑆0 )𝑥𝑘−1 + 𝑒2 (𝑆0 )𝑥𝑘−2 − · · · + (−1)𝑘 𝑒𝑘 (𝑆0 ).
                            𝑟∈𝑆0

Because each 𝑒𝑗 (𝑆0 ) ̸= 0, every coefficient of 𝑄 is non-zero. By construction 𝑄 divides 𝑃 (its roots are a subset
of the roots of 𝑃 ). Consequently the product of the coefficients of 𝑄 is non-zero, contradicting the hypothesis
of the problem, which states that *any* real divisor of degree at most 𝑘 must have a zero coefficient.
——————————————————————–
### 7. Conclusion
The assumption that all roots of 𝑃 are real leads to a contradiction. Therefore 𝑃 must possess at least one
non-real root.
■




                                                                                                                      31
