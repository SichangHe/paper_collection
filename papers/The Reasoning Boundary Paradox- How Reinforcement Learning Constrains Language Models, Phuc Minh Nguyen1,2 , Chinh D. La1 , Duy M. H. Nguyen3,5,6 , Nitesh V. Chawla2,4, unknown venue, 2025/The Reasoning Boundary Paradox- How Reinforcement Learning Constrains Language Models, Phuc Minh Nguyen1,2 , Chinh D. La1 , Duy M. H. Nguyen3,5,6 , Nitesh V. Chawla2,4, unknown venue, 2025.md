                                        Preprint




                                        T HE R EASONING B OUNDARY PARADOX : H OW R E -
                                        INFORCEMENT L EARNING C ONSTRAINS L ANGUAGE
                                        M ODELS
                                                   Phuc Minh Nguyen1,2 , Chinh D. La1 , Duy M. H. Nguyen3,5,6 , Nitesh V. Chawla2,4
                                                                          Binh T. Nguyen1,2∗ , Khoa D. Doan1,2∗
                                                             1
                                                               College of Engineering and Computer Science, VinUniversity
                                                                  2
                                                                    Center for Environmental Intelligence, VinUniversity
                                                                    3
                                                                      University of Stuttgart, 4 University of Notre Dame
                                                               5
                                                                 German Research Center for Artificial Intelligence (DFKI)
                                                           6
                                                             Max Planck Research School for Intelligent Systems (IMPRS-IS)
arXiv:2510.02230v1 [cs.AI] 2 Oct 2025




                                                                                     A BSTRACT

                                                    Reinforcement Learning with Verifiable Rewards (RLVR) has emerged as a key
                                                    method for improving Large Language Models’ reasoning capabilities, yet re-
                                                    cent evidence suggests it may paradoxically shrink the reasoning boundary rather
                                                    than expand it. This paper investigates the shrinkage issue of RLVR by analyz-
                                                    ing its learning dynamics and reveals two critical phenomena that explain this
                                                    failure. First, we expose negative interference in RLVR, where learning to solve
                                                    certain training problems actively reduces the likelihood of correct solutions for
                                                    others, leading to the decline of Pass@k performance, or the probability of gen-
                                                    erating a correct solution within k attempts. Second, we uncover the winner-
                                                    take-all phenomenon: RLVR disproportionately reinforces problems with high
                                                    likelihood, correct solutions under the base model while suppressing other ini-
                                                    tially low-likelihood ones. Through extensive theoretical and empirical analysis
                                                    on multiple mathematical reasoning benchmarks, we show that this effect arises
                                                    from the inherent on-policy sampling in standard RL objectives, causing the model
                                                    to converge toward narrow solution strategies. Based on these insights, we pro-
                                                    pose a simple yet effective data curation algorithm that focuses RLVR learning
                                                    on low-likelihood problems, achieving notable improvement in Pass@k perfor-
                                                    mance. Our code is available at https://github.com/mail-research/
                                                    SELF-llm-interference.


                                        1       I NTRODUCTION

                                        Large Language Models (LLMs) have recently shown remarkable capabilities in complex logical
                                        tasks such as mathematical reasoning (Cobbe et al., 2021; Hendrycks et al., 2021) and program-
                                        ming (Jimenez et al., 2024; Yang et al., 2024b). A key factor behind this success is Reinforcement
                                        Learning with Verifiable Rewards (RLVR, Lambert et al. 2025; DeepSeek-AI et al. 2025). RLVR
                                        optimizes the LLMs against a binary signal based on objective correctness, eliminating the need
                                        for human annotations (OpenAI et al., 2024; MetaAI, 2024b). It is believed that RLVR encour-
                                        ages the emergence of novel reasoning strategies, such as self-reflection and iterative refinement
                                        (DeepSeek-AI et al., 2025; Zeng et al., 2025; Luo et al., 2025), enabling the LLMs to surpass the
                                        capabilities of their base models.
                                        However, recent studies suggest that RLVR training does not expand the reasoning boundary beyond
                                        what the base model already possesses (Yue et al., 2025; Zhao et al., 2025; Zhu et al., 2025; Liu et al.,
                                        2025b). Notably, Liu et al. (2025c); Zhao et al. (2025) reveal that the base model already exhibits
                                        complex reasoning behaviors even before RLVR, while Yue et al. (2025), using the pass@k metric
                                        (i.e., the probability of generating a correct solution within k attempts), demonstrate that RLVR
                                        can even shrink the reasoning boundary, reducing the set of problems the model can solve within k
                                            ∗
                                                Co-Corresponding Authors: binh.nt2@vinuni.edu.vn & khoa.dd@vinuni.edu.vn


                                                                                            1
Preprint




                                 AIME24                                            AIME25                                            Math500                                          Minerva
            0.76
                          Ours                                              Ours                                0.952         Ours                                0.67         Ours
            0.75
                          GRPO                                 0.70         GRPO                                              GRPO                                             GRPO
            0.74                                                                                                                                                  0.66
                                                                                                                0.950
Pass@1024




                                                   Pass@1024




                                                                                                     Pass@128




                                                                                                                                                       Pass@128
            0.73                                               0.68
                                                                                                                                                                  0.65

            0.72                                                                                                0.948
                                                               0.66                                                                                               0.64
            0.71
                                                                                                                0.946
                                                                                                                                                                  0.63
            0.70                                               0.64

            0.69                                                                                                0.944                                             0.62

                    100      200      300    400                      100      200      300    400                      100      200       300   400                     100      200       300   400
                            Training steps                                    Training steps                                    Training steps                                   Training steps



Figure 1: Pass@k evolution (smoothed) during RLVR training with Qwen2.5-Math-1.5B, compar-
ing our proposed finetuning objective SELF to GRPO under a large sampling budget k. While
GRPO shows a progressive decline, SELF exhibits consistent improvements in Pass@k throughout
the training process.

trials. Identifying why this coverage shrinkage occurs is crucial for understanding and effectively
leveraging RLVR to solve novel problems.
To investigate this issue, this paper analyzes the learning dynamics of RLVR training. Unlike stan-
dard RL, which is effective in learning novel strategies within a single and well-defined Markov
Decision Process (MDP), in LLMs reasoning, each problem x induces its own MDP with a distinct
and unknown reward function r(x, ·) (Setlur et al., 2025; Qu et al., 2025). Consequently, learning to
solve a problem x, defined by one MDP, can affect the ability of the LM to solve another problem x′ ,
defined by another MDP. Indeed, our analysis reveals that RLVR is prone to a negative interference
effect where learning to solve a subset of training problems reduces the likelihood of generating cor-
rect solutions for others. This dynamic can lead to a winner-take-all scenario (Schaul et al., 2019),
where the LLMs disproportionately improve on a limited subset of problems that the base model can
already solve with high likelihood while neglecting or even regressing on others, ultimately leading
to a decline in Pass@k performance or problem coverage. Furthermore, we highlight the failure of
current regularization techniques, such as clipping (Schulman et al., 2017) and KL regularization
in preventing these effects in RLVR. Finally, these findings motivate us to propose SELF, a simple
yet effective data curation algorithm that focuses model learning on a subset of problems with low
likelihood, effectively improving the coverage performance across mathematical benchmarks. In
summary, the main contributions of this work are as follows:

1. We study the learning dynamics of RLVR and reveal negative interference in LLM reasoning,
   where learning to solve a subset of training problems results in a negative effect on others, leading
   to winner-take-all in which the model only concentrates on solving a smaller set of problems.
2. We reveal the winner-take-all learning phenomenon, where RLVR tends to reinforce problems
   highly solvable under the base model while neglecting problems with initially low likelihood
   of correct solutions. Due to the existence of negative interference, these problems with lower
   success rates will progressively have lower likelihoods of generating the correct solutions, and
   on-policy learning cannot provide any explicit learning signal to improve them. This explains
   the reduction in the diversity of previously learned behaviors during RLVR training or reasoning
   boundary shrinkage in RLVR.
3. We propose SELF (Selective Examples with Low-likelihood and Forward-KL), a data curation
   algorithm that selectively solves only problems with low likelihood of arriving at correct answers
   while preserving previously learned behavior during RLVR. Our extensive empirical evaluation
   demonstrates that SELF not only improves sample efficiency but also effectively mitigates the
   coverage shrinkage problem in RLVR.

2                  R ELATED W ORKS
Reinforcement Learning with Verifiable Rewards (RLVR). RLVR has emerged as a powerful
method for improving LLMs in mathematical reasoning and programming (DeepSeek-AI et al.,
2025). However, recent evidence suggests that reasoning abilities already exist in base models, with
RLVR only amplifying rather than creating such capabilities (Shao et al., 2025; Yue et al., 2025; Liu
et al., 2025c). Moreover, RLVR can degrade performance and reduce coverage of correct solutions,
evidenced by decreased pass@k metrics (Yue et al., 2025; Dang et al., 2025; Zhao et al., 2025;


                                                                                                     2
Preprint




Wu et al., 2025). Liu et al. (2025a) attributes coverage reduction to limited RL training and over-
specialization during pretraining, while Zhu et al. (2025) shows that increasing the likelihood of
correct solutions improves accuracy but reduces diversity.

Loss of Plasticity in Neural Networks. Neural networks gradually lose adaptability, a phe-
nomenon called plasticity loss (Klein et al., 2024; Juliani & Ash, 2024), particularly pronounced
in RL due to its non-stationary nature (Klein et al., 2024; Juliani & Ash, 2024; Moalla et al., 2024).
Proposed remedies include resetting parameters (Ash & Adams, 2020; Kielo & Lukin, 2024; D’Oro
et al., 2023) and self-distillation (Igl et al., 2021). In particular, Tang & Berseth (2024); Tang et al.
(2025) show plasticity loss correlates with drastic model confidence changes (churn), which under-
mines regularization techniques like clipping (Moalla et al., 2024). Our work explains why RLVR
reduces behavioral diversity in LLM reasoning, where non-stationarity arises from both shifting
distributions and varying prompt-induced objectives.

Learning Dynamics. Ren & Sutherland (2025) shows negative gradients in off-policy LLM fine-
tuning create a squeezing effect. In RL, interference occurs when learning degrades performance
on unseen or previously learned states (Liu et al., 2020; 2023). Schaul et al. (2019) demonstrates
a winner-take-all effect (Schaul et al., 2019; Guo et al., 2018) in contextual bandits, where policies
excel in some contexts while regressing in others. Our findings reveal negative interference as the
key mechanism through which RLVR reduces solvable problems, with on-policy sampling causing
disproportionate reinforcement of initially successful problems.

3    P ROBLEM SETTING AND P ER - STEP I NFLUENCE IN RLVR
Language Model. We first consider a language model (LM) policy π. For a given       Q prompt x, the
LM policy π will generate a response y in an auto-regressive manner: π(y|x) = t π(yt |x, y<t ),
where yt is the t-th indexed token in y and y<t is the partial completion before yt .

Reinforcement Learning with Verifiable Rewards (RLVR). Given a verifiable reward function
r(x, y) ∈ {0, 1} indicating whether a response y is correct (y + ) or incorrect (y − ), the goal of
RLVR is to learn a new policy πθ , initialized from a base model (usually the pre-trained model)
πb , to generate responses maximizing the reward function with the following reward regularized
maximization objective:
                     max Ex∼D,y∼πθ (·|x) [r(x, y) − βKL (πθ (·|x) ∥ πb (·|x))] ,                        (1)
                       πθ

where β is the KL regularization parameter. Eq. (1) represents a simplified version of common RL
algorithms (PPO (Schulman et al., 2017), GRPO (DeepSeek-AI et al., 2025)). We provide a detailed
derivation of the GRPO and PPO objectives in Appendix B.

Per-step Influence. Learning dynamics describes how the change in the model parameters θ,
induced by problem x, influences or changes the log-likelihood log πθ of other problem-solution
pairs (x′ , y ′ ), which can be either training or test examples. Given an update step in LM parame-
ters θt → θt+1 , the per-step influence measures the change in model confidence log πθ (y ′ |x′ ) on
(x′ , y ′ ):
                         ∆ log πθt (y ′ |x′ ) = log πθt+1 (y ′ |x′ ) − log πθt (y ′ |x′ )               (2)
Using Taylor expansion, assuming with a sufficiently small learning rate η, we can decompose the
per-step influence function as:
Proposition 3.1. Consider a problem-solutions pair (x, y) for updating using policy gradient ob-
jective, a sufficiently small learning rate η, the per-step influence on a problem-solution pair (x′ , y ′ )
is defined as:
                        ∆ log πθt (y ′ |x′ ) = η Kt (x, x′ , y, y ′ )A(x, y) + O(η 2 )                  (3)
where Kt (x, x′ , y, y ′ ) = ∇θ log πθt (y|x)⊤ ∇θ log πθt (y ′ |x′ ) measures the influence between
(x, y) and (x′ , y ′ ), and the advantage function A(x, y) determines the direction of the model’s
update.


                                                        3
Preprint




The dot product between two gradients, Kt (x, x′ , y, y ′ ), can be interpreted as a model-specific
similarity measure between problem–solution pairs, and A(x, y) determines the magnitude and
direction of the model update, indicating whether the gradient contributes positively or negatively.


4     L EARNING DYNAMICS OF RLVR

Calculating Kt (x, x′ , y, y ′ ) for LLMs is extremely expensive due to their large parameter counts.
However, from Proposition 3.1, we have
                               |∆ log πθt (y ′ |x′ )|
                                                      ≤ |Kt (x, x′ , y, y ′ )|,                     (4)
                                      ηC
where C is a constant bounding the advantage function that holds due to finite binary reward val-
ues. This bound indicates that we can use the per-step influence ∆ log πθt (y ′ |x′ ) to approximate
Kt (x, x′ , y, y ′ ). Given this insight, we introduce two quantitative metrics designed to better char-
acterize the properties of K(x, x′ , y, y ′ ) as follows.
Definition 4.1 (Interference in Language Model). Given a behavior policy µ, we define the inter-
ference of a language model policy, πθt , at iteration t as:

                          ∆+ (πθt , µ) = E x′ ∼D, ∆ log πθt (y + |x′ ) ,
                                                                     
                                                                                             (5)
                                              y + ∼µ(·|x)

and the magnitude of the relative changes in model confidence on examples that lie outside of the
training batch as:
                                                                     2
                          ||∆(πθt , µ)|| = E x′ ∼D, ∆ log πθt (y|x′ ) .
                                                y∼µ(·|x)


Intuitively, ∆+ (πθt , µ) measures the direction of the relative influence K(x, x′ , y, y + ) on other
problem–correct solution pairs under the behavior policy µ. A positive ∆ log πθt (y + |x), indicates
improvement, while a negative ∆ log πθt (y + |x) corresponds to negative interference, i.e., learning to
solve a training problem x reduces the likelihood of producing other correct solutions. In our work,
we consider µ to be the base model πb to study how RLVR affects the retention (or overwriting) of
previously correct problem–solution pairs.
On the other hand, ||∆(πθt , µ)|| measures the squared magnitude of the relative influence
K(x, x′ , y, y) – i.e., how drastic the model confidence on examples generated from µ changes
after an update. If ||∆(πθt , πb )|| = 0, we can expect no coverage shrinkage to happen during RLVR
training, as updating on training examples does not affect other non-training examples. An increase
in the magnitude of influence ||∆(πθt , πb )|| indicates that the language model struggles to distin-
guish between different problems, leading to highly correlated gradients across different examples.
We provide a detailed explanation in Appendix C.

4.1   E XPERIMENTAL S ETUP

We focus on mathematical reasoning tasks to investigate the learning dynamics of RLVR. Specifi-
cally, we experiment on 2 series of models: Qwen2.5-Math-1.5B/7B (Yang et al., 2024a) and Llama-
3.2-3B-Instruct (MetaAI, 2024b). We consider DeepScaleR (Luo et al., 2025) as the training dataset
D, which consists of approximately 40k mathematics problems collected from different sources. The
detailed experimental setup is provided in Appendix A. We conduct experiments on 4 mathematical
reasoning benchmarks: AIME24 & AIME25 (Art of Problem Solving), Math500 (Hendrycks et al.,
2021; Lightman et al., 2024), and Minerva (Lewkowycz et al., 2022), following existing works on
LLMs reasoning (Yue et al., 2025; Zhu et al., 2025; Li et al., 2025a). Unless otherwise specified, we
use Dtest to denote the combined test set from all four benchmarks.
To analyze the model’s learning dynamics during training, we create a probing dataset Dprob (based
on the training prompts x ∈ D) using the base model. For each prompt x, we generate 4 re-
sponses {yi }4i=1 , to balance between computation and solution diversity. We then rely on Dprob to
calculate the effect of interference ∆+ and the relative change in model confidence on each update
||∆(πθ , µ)|| throughout the training process. We present our findings in the following section.


                                                      4
Preprint




4.2             N EGATIVE I NTERFERENCE IN RLVR T RAINING OF L ANGUAGE M ODELS

Decreasing Pass@k as training progresses. As shown in Fig. 2(A), RLVR training steadily im-
proves the accuracy (Pass@1) of πθ , averaged across four benchmarks, as training progresses.

                                                                                                                                                                                                                             +
               (A) Pass@k dynamic on Dtest                                      (B) ||∆(πθt , µ)| on Dprob                           (C) ∆+(πθt , µ) on Dprob                                         (D) Log likelihood on Dprob
                                                            0.280                                                        0.002
0.7055                                                              0.018                                                                                                                 −0.21
                                                                                                                         0.000
0.7050                                                              0.016                                                                                                                 −0.22
                                                            0.275
                                                                                                                        −0.002                                                            −0.23




                                                                                                                                                                         Log likelihood
0.7045                                                              0.014
                                                            0.270
                                                                                                                        −0.004                                                            −0.24
0.7040                                                              0.012
                                                            0.265                                                       −0.006                                                            −0.25
0.7035                                                              0.010
                                                                                                                        −0.008                                                            −0.26
0.7030                                                      0.260   0.008
                                                                                                                        −0.010                                                            −0.27
0.7025                            Pass@256                          0.006
                                                            0.255
0.7020                            Pass@1                            0.004
                                                                                                                        −0.012                                                            −0.28


         150    200   250   300     350   400   450   500                   0    100     200    300     400   500                0    100     200    300     400   500                            0     100     200    300     400   500
                        Training steps                                                 Training steps                                       Training steps                                                    Training steps



Figure 2: Learning dynamics of RLVR with key trends: (A) RLVR tends to improve average ac-
curacy, but reduce the coverage of solvable solutions, as measured by Pass@256 (averaged across
4 test benchmarks); (B) the increasing effect of influence strength as training progresses; (C) the
increase in negative interference; and (D) the decline of model confidence on previously correct
solutions.

However, when evaluated with a larger sampling budget (e.g., Pass@256), RLVR displays a clear
decline, as the performance drops below that of the base model πb after about 300 steps and con-
tinues to deteriorate towards the end of training. The results indicate that RLVR provides little to
no improvement in Pass@k at large k’s throughout training, a phenomenon consistent with recent
findings in (Yue et al., 2025).

The increase of influence on other examples in one training batch update. We also observe an
increase in ||∆(πθt , µ)|| during training, as shown in Fig. 2(B). The growing strength of influence at
each update step on outside examples suggests stronger similarity among gradients across samples
(Tang & Berseth, 2024; Tang et al., 2025), indicating that LLMs struggle to differentiate between
distinct problems. As we demonstrate in Sec . 5, this effect can reduce the diversity of previously
learned behaviors, where LLMs tend to concentrate on a single reasoning strategy across different
problems, and also weaken the regularization effect in RLVR.

Increasing effect of negative interferences. We continue to investigate the interference on the
other problem-correct solution pairs in Fig. 2(C), and observe a decreasing trend in ∆+ (πθt , µ);
we also observe a similar decreasing trend in the log-likelihood of correct solutions log πθ (y + |x)
(Fig. 2(D)). These observations indicate that the learned policy increasingly reduces the likelihood of
other problem-correct solution pairs generated by the base model. We call this behavior the negative
interference, where learning to solve certain problems in D inadvertently hinders the performance
on other problem–correct solution pairs.
Later in Sec. 5, we will show that, due to RLVR’s on-policy sampling, highly solvable problems
in the base model tend to capture most of the learning signal. With negative inference, this subset
of problems will increasingly dominate the learning process while “weaker” ones are suppressed,
ultimately constraining the policy to excel only in this subset of contexts while regressing in others.
This also explains why RLVR improves average accuracy but reduces coverage. Under a small
sampling budget k (e.g., k = 1), RLVR incentivizes these “winner” problems to reach higher average
accuracy, but this comes at the cost of negative interference, where the model’s confidence in correct
solutions to other problems is degraded. Consequently, the set of problems solvable under a larger
budget k becomes narrower.

Interference as an indicator of decreasing Pass@k. The previous observations suggest that
the decline in Pass@k performance is likely the result of negative interference in RLVR learn-
ing dynamics. To confirm this hypothesis, we uniformly sample two checkpoints T and T ′ with
T ′ > T during RLVR training. For each pair, we compute the interference ∆+ (πθT ′ , πθT ) under
correct problem-solution pairs of Dtest and the corresponding change in Pass@k, i.e., ∆Pass@k =
Pass@k(πθT ′ ) − Pass@k(πθT ) with k = 128 (the value of k is selected based on the related prior


                                                                                                                    5
Preprint




works (Yue et al., 2025; Liu et al., 2025a)). We then measure the correlation between these two
quantities across four benchmarks.
The correlation results are presented in Fig. 3. As expected, we observe a strong correlation between
∆+ (πθT ′ , πθT ) and the decrease in Pass@k, suggesting that interference is a key factor driving the
degradation of Pass@k performance during training.

5                T HE EFFECT OF on-policy IN RLVR
In this section, we examine which problems RLVR likely prioritizes. First, we show that RLVR
primarily incentivizes the language model πθ to generate responses that already have high likelihood
under the base model, regardless of their correctness. This arises from the nature of on-policy
sampling: for problems where the base model can produce multiple correct solutions, RLVR tends
to reinforce the most probable one; but for those where the correct solutions lie in the “valley”
regions of the distribution, RLVR, instead, reinforces the base model’s highest-confidence – yet
potentially incorrect – responses, offering no meaningful learning signal to escape these incorrect
modes.
                                  AIME24                                                         AIME25                                                       Math500                                                        Minerva
                                                                                                                                         0.8                                                        2
             3
                        Pearson ρ = 0.58                                      6      Pearson ρ = 0.50                                                 Pearson ρ = 0.59                                          Pearson ρ = 0.57
                                                                                                                                         0.6                                                        1
             2                                                                4                                                          0.4
                                                                                                                                                                                                    0
∆Pass@128




                                                                 ∆Pass@128




                                                                                                                            ∆Pass@128




                                                                                                                                                                                       ∆Pass@128
             1                                                                                                                           0.2
                                                                                                                                                                                                   −1
                                                                              2                                                          0.0
             0                                                                                                                                                                                     −2
                                                                                                                                        −0.2
            −1                                                                0
                                                                                                                                        −0.4                                                       −3

            −2                                                                                                                          −0.6                                                       −4
                                                                             −2
                                                                                                                                        −0.8                                                       −5
            −3
                 −0.6   −0.4   −0.2   0.0      0.2   0.4   0.6                    −0.8   −0.6       −0.4       −0.2   0.0                      −4.5         −4.0         −3.5   −3.0                    −3.0   −2.5   −2.0     −1.5    −1.0   −0.5   0.0
                                ∆+ (πθt , µ)                                                    ∆+ (πθt , µ)                                                 ∆+ (πθt , µ)                                               ∆+ (πθt , µ)



                        Figure 3: Interference as an indicator of Pass@k decrease across various benchmarks.


Then, we highlight a winner-take-all effect that leads to a reduction of previously learned behaviors,
as models tend to propagate reasoning strategies from highly solvable problems to others. Finally,
we show that existing regularization techniques fail to prevent this issue.
Experimental Setup. We consider a subset of problems from the Math500 dataset, denoted as D;
the experiments for the other datasets are provided in Appendix H. We utilize the perplexity metric
(Jurafsky & Martin, 2025):
                                                                       
                                                           1
                       PPLµ (π, D) = E x∼D, exp −             log π(y|x)                        (6)
                                         y∼µ(·|x)         |y|
where D = {xi }ni=1 is the set of prompts, the responses are generated by the reference distribution
y ∼ µ(·|x) conditioned on x (|y| denotes the sequence length), and π is the model whose perplexity
is being evaluated. We also define the change in average accuracy between the base policy and the
learned policy for each problem x:
                                                           ∆r(x) = Ey∼πθ (·|x) [r(x, y)] − Ey∼πb (·|x) [r(x, y)]                                                                                                                                     (7)
and then partition D into two subsets: D↓ , containing problems where RLVR reduces the average
accuracy compared to the base model (i.e., ∆r(x) < 0), and D↑ , containing problems where RLVR
improves upon the base model (i.e., ∆r(x) > 0). We provide additional experimental details in
Appendix H.
RLVR tends to increase high likelihood regions under the base model. Fig. 4 shows that during
training, the LM πθ increasingly generates responses that already have high likelihood under the
base model πb (Leftmost), while the initial problem-solution pairs sampled from πb increasingly
have lower likelihood (or higher PPLπb (πθt , D)) in the RLVR policy πθt (Middle). Together, these
results indicate that the sampled responses from πθt concentrate on the highest likelihood regions in
the base model. We also observe in Fig. 4 (Middle) that the problem-correct solution pairs sampled
from πb have even lower model confidence (higher PPLπb (πθt , D+ )) and a similar decreasing trend,
suggesting that for each problem, RLVR collapses into the solution with the highest likelihood


                                                                                                                            6
Preprint




             1.1300
                          PPLπθt (πb , D)                                         1.26
                                                                                             PPLπb (πθt , D)                              1.25
             1.1275                                                               1.24       PPLπb (πθt , D+ )
             1.1250                                                                                                                       1.20
                                                                                  1.22

Perplexity




                                                                     Perplexity
             1.1225
                                                                                  1.20
             1.1200
                                                                                                                                          1.15
                                                                                  1.18
             1.1175
                                                                                  1.16
                                                                                                                                          1.10
             1.1150
                                                                                  1.14
             1.1125
                                                                                  1.12                                                    1.05
             1.1100

                      0     100        200        300   400    500                       0     100         200       300     400   500
                                                                                                                                                 PPLπb (πb , D↓ )          PPLπb (πb , D↑ )
                                       Training steps                                                     Training steps



Figure 4: Perplexity during RLVR training. Leftmost: the data sampled from each intermediate
checkpoint πθt exhibits an increasingly high model confidence under πb . Middle: RLVR models
πθt exhibit reduced confidence in data previously generated by the base model, regardless of their
correctness. Rightmost: problems that RLVR improves already have a high likelihood of generat-
ing correct solutions under πb , while coverage-reduced problems initially have a low likelihood of
producing correct answers.


under πb regardless of whether these high likelihood responses is correct or not. Finally, Fig. 4
(Rightmost) demonstrates that, for problems where the base model already assigns high likelihood
to correct solutions (lower PPL(πθt , D↑ )), RLVR reinforces these responses, leading to performance
gains (or higher average accuracies). In contrast, when the correct responses initially lie in low-
likelihood regions (higher PPL(πθt , D↓ )), RLVR tends to reduce its probability, reinforcing the base
model’s initial biases, resulting in degraded performance.


                                                              πθ 0                                                         πθ 0                                     πθ 0
                                                              πθ 1                                                         πθ 1                                     πθ 1



                                                              y+                              y+                 y+                      y∗          y+             y−
                                                                                               1                  2


Figure 5: An illustration describing the dynamic of on-policy learning in Eq. (8). Leftmost: cor-
rect response y + in low-likelihood regions induce minimal effect. Middle: with multiple correct
responses y1+ and y2+ , updates favor the one with higher initial likelihood. Rightmost: negative
gradients on incorrect response y − can raise correct ones y + , but greedy responses y ∗ increase the
most.

Why does RLVR reinforce problems with high-likelihood correct solutions in the base model?
To explain why this phenomenon happens, we first confirm that it occurs when on-policy sampling
is used for learning (the details are in Appendix D). More specifically, this phenomenon also appears
even in a simple bandit problem with a Softmax policy with V actions. We can look into the on-
policy objective REINFORCE for an action y:
                                            ∇θ LREINFORCE (πθ ) = A(y)∇θ πθ (y) = A(y)πθ (y)∇θ log πθ (y)                                                                                     (8)
and arrive at the following insights (additionally, we utilize Fig. 5 for illustration):

     • Low-likelihood tokens provide less meaningful updates. Eq. (8) suggests that low likelihood,
       correct responses receive infrequent and small updates because of the explicit πθ (y) scaling
       factor and the fact that they are rarely sampled (Fig. 5 Leftmost), while high-likelihood tokens
       dominate the learning process. Moreover, if πθ (y) = 0, the gradient vanishes, creating an
       additional saddle point where zero-probability tokens cannot be updated.
     • When there are multiple optimal actions y1+ and y2+ , the one with with the higher likelihood
       πθ (·) will dominate. Due to the scaling of the model probability in Eq. 8, the update will tilt
       probability toward the already dominant correct mode, as depicted in Fig. 5 (Middle). This
       effect will exacerbate when the gap between the two probabilities increases.
     • Negative gradients tend to reinforce high-likelihood tokens, regardless of their correctness. On-
       policy learning with negative gradient exhibits similar behavior to off-policy with negative gra-
       dient. When the correct solution resides in a “valley” of the distribution, negative gradient tends


                                                                                                            7
Preprint




   to increase high-likelihood tokens regardless of correctness (Fig. 5 Rightmost), further dimin-
   ishing the low-likelihood (but correct) ones (especially when the distribution is peaky). This is
   also observed in Ren & Sutherland (2025).
 • If y + is unlikely to be sampled under the k-sampling budget πθ , RLVR provides no learning
   signal. This arises from the advantage calculation, where A(y) = 0 if all sampled actions are
   incorrect, resulting in no update.

We provide additional theoretical and empirical details of this effect by analyzing the ratio of model
predictions πθt+1 /πθt in Appendix D.
On-policy learning and negative interference lead to Winner-take-all. The above analysis sug-
gests that highly solvable problems dominate the learning signal, while problems with lower success
rates contribute less due to gradient vanishing. Learning primarily on these highly solvable problems
also increases the chance of negative interference on problems with lower success rates, and even-
tually exacerbates the effect of winner-take-all; as training progresses, these problems with lower
success rates will progressively receive less explicit learning signal and have lower likelihoods of
sampling correct solutions.
Winner-take-all explains the coverage shrink-
age and performance degradation in Minerva                                                                         Minerva                                    29.0
                                                                                                                                                                      Base Accuracy in D
Benchmark. Shao et al. (2025) report that the                      0.7
                                                                                                            Code Frequency
                                                                                                                                                              28.5
                                                                                                            Lang Frequency
Qwen2.5-Math model family employs two dis-




                                                                                                                                               Accuracy (%)
                                                                   0.6                                                                                        28.0
                                                       Frequency

tinct reasoning modes: code-based and natural-                     0.5                                                                                        27.5

language reasoning. However, during RLVR                           0.4                                                                                        27.0

training, we observe a progressive collapse to nat-                0.3                                                                                        26.5


ural language reasoning. As shown in Fig. 6                                                                                                                   26.0
                                                                         0                                 100     200    300     400    500                         Lang            Code
(Left), the frequency of the generated solutions                                                                 Training steps

using code reasoning steadily decreases over
training, while the frequency of natural language      Figure 6: The LM switches from code rea-
reasoning dominates at the end of training.            soning to language reasoning in the Minerva
                                                       benchmark, due to the reduction of diversity of
We observe that natural language reasoning has         previously learned behaviors.
a better initial accuracy in the training dataset D
(Fig. 6 (Right)). As RLVR training progresses, the LM tends to concentrate on this subset of prob-
lems that are already highly solvable under the base model. Winner-take-all suggests that RLVR
amplifies the highest-likelihood solutions while suppressing other correct ones, leading to reduced
diversity among these solvable problems and a collapse to natural language reasoning. As the influ-
ence strength ||∆(πθt , µ)|| grows (as shown in Fig. 2), this loss of diversity and the resulting bias
towards high-probability responses under base model πb becomes amplified propagate, affecting
other problem–solution pairs, including the test problems. Consequently, in cases where the base
model’s initial bias is incorrect, this self-bias amplification will result in coverage shrinkage and
negative interference. This explains that on the Minerva benchmark (the test set), while code rea-
soning achieves higher initial accuracy, as RLVR training gradually switches to language reasoning,
the performance on code reasoning problems drops, as observed in Fig. 1.
Existing regularizations fail to mitigate diversity
shrinkage. In RLVR training, trust region constraints      2.0   Probing data D
                                                                 Training data D
                                                                                                                                        prob



such as clipping aim to prevent the learned policy
                                                                             Trust region violations (%)




from deviating too far from the previously updated         1.5


policy. As shown in Fig. 7, the average probability
ratio ρ = πθ /πold that violates the trust region con-     1.0


straint (lies outside the clipping range (1 − ϵ, 1 + ϵ)
                                                           0.5
(ϵ = 0.2)) remains stable in the training batch. How-
ever, under the probing dataset Dprob , this violation     0.0
steadily grows as training progresses. This suggests           0        100      200         300 400 500
                                                                                 Training steps
that the clipping mechanism has little influence on
data outside the training batch, thus failing to pre-
vent the increasing negative interference throughout Figure 7: Clipping violations on training
the training process. Another regularizer, the Reverse data and probing data.
KL, is also ineffective, as Reverse KL is known to exhibit mode-seeking behavior, where it has little


                                                   8
Preprint




to no penalty on regions where πθ puts low probability mass. Furthermore, Reverse KL often favors
collapsing probability mass onto high-likelihood mode under the base model πb .


6        A DATA CURATION TECHNIQUE TO MITIGATE WINNER - TAKE - ALL EFFECT.

Building on the above analysis, we propose a novel and effective algorithm that focuses learning
only on problems where the greedy response fails. This acts as a proxy metric to exclude highly
solvable problems from learning, thus preventing them from dominating the learning signal. To
further preserve the diversity of learned behaviors, we replace the Reverse KL regularization with
a Forward KL (SFT loss) objective, which penalizes the model when it begins to forget previously
learned behaviors. We refer to this method as SELF (Selective Examples with Low-likelihood and
Forward-KL):
                        J (πθ ) = Ex∼D,(y∗ ,y)∼πθ (·|x) [1{r(x, y ∗ ) ∈ C(x)}r(x, y) − βKL(πb ||πθ )]                                                                                                                                  (9)

where y ∗ is the greedy response and C(x) = {y|r(x, y) = 1} is the set of correct completions
given a problem x.

          Train Accuracy (%)                                     Entropy                                       ∆+(πθt , µ)                                     ||∆(πθt , µ)||                           Trust region violations (%)
50
                                                                                            0.0025                                          0.0200
           Ours                             0.30          Ours                                             Ours                                            Ours                               2.0           Ours
                                                                                            0.0000                                          0.0175
40         GRPO                                           GRPO                                             GRPO                                            GRPO                                             GRPO
                                                                                                                                                                                              1.8
                                            0.25                                           −0.0025                                          0.0150
                                                                                                                                                                                              1.6
30                                                                                         −0.0050                                          0.0125
                                            0.20
                                                                                           −0.0075                                                                                            1.4
                                                                                                                                            0.0100
20                                                                                         −0.0100                                                                                            1.2
                                            0.15                                                                                            0.0075
                                                                                           −0.0125                                                                                            1.0
                                                                                                                                            0.0050
10                                          0.10
                                                                                           −0.0150
                                                                                                                                                                                              0.8
     0   100     200    300     400   500          0    100     200    300     400   500             0   100     200    300     400   500            0   100     200    300     400    500          0     100     200    300     400    500
               Training steps                                 Training steps                                   Training steps                                  Training steps                                   Training steps



Figure 8: Learning dynamics of GRPO and the proposed method, with key observations: 1) SELF
focus on learning problems with low success rate, 2) SELF exhibits better diversity, 3) SELF mit-
igates the effect of negative interference and reduce the influence strength to other examples, result
in a strong regularization effect.

We compare SELF learning dynamics against the standard GRPO objective in Fig. 8. Since SELF
focuses on problems with a low likelihood of being solved correctly, it achieves a lower average
training reward than GRPO. However, it preserves better diversity throughout training, as measured
by higher token-level entropy across the training process. In addition, SELF effectively mitigates
the negative interference effect as we observe a significant improvement in ∆+ (πθ , πb ) and a smaller
magnitude of influence ||∆(πθ , µ)|| on other examples. Furthermore, SELF reduces the extent of
trust region violations for examples outside the training batch.

Table 1: Evaluation results on various mathematical benchmarks (%). The best performance under
each dataset is marked with boldface.

                                                                              AIME 2024        AIME 2025         Math500         Minerva
Model                                                  Method
                                                                           Pass@1 Pass@1024 Pass@1 Pass@1024 Pass@1 Pass@256 Pass@1 Pass@256
                                                   Base model 9.73                                   75.86             4.45                 67.80               58.83                 95.58             16.82              70.67
 Qwen2.5-Math-1.5B                                   GRPO     15.16                                  67.77             8.50                 64.05               72.67                 95.0              23.96              65.07
                                                       SELF                  14.33                   80.94             8.05                 69.45                71.0                 96.0              23.14              68.75
                                                   Base model 16.94                                  81.83              6.97                67.57               59.71                 96.0              11.60              66.91
 Qwen2.5-Math-7B                                     GRPO     27.95                                  84.77             14.13                58.60               80.36                 92.8              29.40              60.66
                                                       SELF                  25.81                   89.62             14.62                72.0                79.82                 97.80             30.42              71.70
                                                   Base model 3.53                                    53.7             0.32                 48.22               26.61                 91.4               8.25              49.26
 Llama-3.2-3B-Instruct                               GRPO     11.76                                  49.25             0.38                 25.28               54.06                 88.2              15.81              50.73
                                                       SELF                  13.30                   51.69             0.65                 51.83               52.12                 91.0               17.0              57.35

Table 1 shows the evaluation of SELF and the baselines on various mathematical benchmarks.
SELF achieves comparable Pass@1 performance compared to GRPO, but consistently better per-
formance for larger values of k. While GRPO achieves good Pass@1 performance, it also reinforces


                                                                                                                   9
Preprint




problems that already have high success rates, leading to narrower coverage at larger k. Interest-
ingly, larger models tend to suffer from even more severe coverage shrinkage than smaller models,
despite achieving higher Pass@1. In contrast, SELF scales more effectively, outperforming GRPO
on Pass@1 in some experiments while also frequently surpassing the base model under larger k
budgets. We also provide details of the computational cost of SELF in Appendix G, where SELF
demonstrates a negligible computation difference to GRPO.


7   C ONCLUSION

We investigate why RLVR exhibits coverage shrinkage of solvable problems, indicated by reduced
Pass@k performance, compared to the base model, by analyzing its learning dynamics. We iden-
tify a detrimental effect, which we call negative interference, where learning on a subset of training
problems can hinder performance on others. This phenomenon serves as a key indicator of the per-
formance decline in larger k budgets. Furthermore, we find that RLVR tends to concentrate learning
on highly solvable problems, leading to reduced diversity and amplification of self-bias toward both
previously solvable and unseen problems. Motivated by these findings, we propose SELF, a simple
yet effective algorithm that only learn on problems with low success rates, effectively mitigating the
coverage shrinkage problem.


R EFERENCES
Arash Ahmadian, Chris Cremer, Matthias Gallé, Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin,
  Ahmet Üstün, and Sara Hooker. Back to basics: Revisiting REINFORCE-style optimiza-
  tion for learning from human feedback in LLMs. In Lun-Wei Ku, Andre Martins, and Vivek
  Srikumar (eds.), Proceedings of the 62nd Annual Meeting of the Association for Computa-
  tional Linguistics (Volume 1: Long Papers), pp. 12248–12267, Bangkok, Thailand, August
  2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.662. URL
  https://aclanthology.org/2024.acl-long.662/.

Art of Problem Solving. Aime problems and solutions. https://artofproblemsolving.
  com/wiki/index.php/AIME_Problems_and_Solutions. Accessed: 2025-04-20.

Jordan T. Ash and Ryan P. Adams. On warm-starting neural network training. In
  NeurIPS, 2020. URL https://proceedings.neurips.cc/paper/2020/hash/
  288cd2567953f06e460a33951f55daaf-Abstract.html.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
  Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
  Schulman. Training verifiers to solve math word problems, 2021. URL https://arxiv.
  org/abs/2110.14168.

Xingyu Dang, Christina Baek, J Zico Kolter, and Aditi Raghunathan. Assessing diversity collapse
  in reasoning. In Scaling Self-Improving Foundation Models without Human Supervision, 2025.
  URL https://openreview.net/forum?id=AMiKsHLjQh.

DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Runxin Xu, Qihao Zhu, and
  Yiliang . . . Xiong. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
  learning. arXiv preprint arXiv:2501.12948, January 22 2025. doi: 10.48550/arXiv.2501.12948.
  URL https://arxiv.org/abs/2501.12948.

Pierluca D’Oro, Max Schwarzer, Evgenii Nikishin, Pierre-Luc Bacon, Marc G Bellemare, and
  Aaron Courville. Sample-efficient reinforcement learning by breaking the replay ratio bar-
  rier. In The Eleventh International Conference on Learning Representations, 2023. URL
  https://openreview.net/forum?id=OpC-9aBBVJe.

Michelle Guo, Albert Haque, De-An Huang, Serena Yeung, and Li Fei-Fei. Dynamic task priori-
 tization for multitask learning. In Proceedings of the European Conference on Computer Vision
 (ECCV), September 2018.


                                                 10
Preprint




Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
  Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset.
  In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks
  Track (Round 2), 2021. URL https://openreview.net/forum?id=7Bywt2mQsCe.
Jian Hu, Xibin Wu, Zilin Zhu, Xianyu, Weixun Wang, Dehao Zhang, and Yu Cao. Openrlhf: An
   easy-to-use, scalable and high-performance rlhf framework. arXiv preprint arXiv:2405.11143,
   2024.
Maximilian Igl, Gregory Farquhar, Jelena Luketina, Wendelin Boehmer, and Shimon Whiteson.
 Transient non-stationarity and generalisation in deep reinforcement learning. In International
 Conference on Learning Representations, 2021. URL https://openreview.net/forum?
 id=Qun8fv4qSby.
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R
  Narasimhan. SWE-bench: Can language models resolve real-world github issues? In The Twelfth
  International Conference on Learning Representations, 2024. URL https://openreview.
  net/forum?id=VTF8yNQM66.
Arthur Juliani and Jordan T. Ash. A study of plasticity loss in on-policy deep reinforcement learning.
  In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024. URL
  https://openreview.net/forum?id=MsUf8kpKTF.
Daniel Jurafsky and James H. Martin. Speech and Language Processing: An Introduction to Natural
  Language Processing, Computational Linguistics, and Speech Recognition, with Language Mod-
  els. 3rd edition, 2025. URL https://web.stanford.edu/˜jurafsky/slp3/. Online
  manuscript released August 24, 2025.
Matthew Kielo and Vladimir Lukin. It’s time to move on: Primacy bias and why it helps to forget. In
 The Third Blogpost Track at ICLR 2024, 2024. URL https://openreview.net/forum?
 id=7ZEwqUyKMC.
Timo Klein, Lukas Miklautz, Kevin Sidak, Claudia Plant, and Sebastian Tschiatschek. Plasticity
  loss in deep reinforcement learning: A survey. CoRR, abs/2411.04832, 2024. URL https:
  //doi.org/10.48550/arXiv.2411.04832.
Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brah-
  man, Lester James Validad Miranda, Alisa Liu, Nouha Dziri, Xinxi Lyu, Yuling Gu, Saumya
  Malik, Victoria Graf, Jena D. Hwang, Jiangjiang Yang, Ronan Le Bras, Oyvind Tafjord, Christo-
  pher Wilhelm, Luca Soldaini, Noah A. Smith, Yizhong Wang, Pradeep Dasigi, and Hannaneh Ha-
  jishirzi. Tulu 3: Pushing frontiers in open language model post-training. In Second Conference on
  Language Modeling, 2025. URL https://openreview.net/forum?id=i1uGbfHHpH.
Aitor Lewkowycz, Anders Johan Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski,
  Vinay Venkatesh Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo,
  Yuhuai Wu, Behnam Neyshabur, Guy Gur-Ari, and Vedant Misra. Solving quantitative rea-
  soning problems with language models. In Alice H. Oh, Alekh Agarwal, Danielle Belgrave,
  and Kyunghyun Cho (eds.), Advances in Neural Information Processing Systems, 2022. URL
  https://openreview.net/forum?id=IFXTZERXdM7.
Yuetai Li, Zhangchen Xu, Fengqing Jiang, Bhaskar Ramasubramanian, Luyao Niu, Bill Yuchen Lin,
  Xiang Yue, and Radha Poovendran. Temporal sampling for forgotten reasoning in LLMs. In 2nd
  AI for Math Workshop @ ICML 2025, 2025a. URL https://openreview.net/forum?
  id=1medQAgr1g.
Ziniu Li, Congliang Chen, Tian Xu, Zeyu Qin, Jiancong Xiao, Zhi-Quan Luo, and Ruoyu Sun.
  Preserving diversity in supervised fine-tuning of large language models. In The Thirteenth In-
  ternational Conference on Learning Representations, 2025b. URL https://openreview.
  net/forum?id=NQEe7B7bSw.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan
  Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth
  International Conference on Learning Representations, 2024. URL https://openreview.
  net/forum?id=v8L0pN6EOi.


                                                 11
Preprint




Mingjie Liu, Shizhe Diao, Ximing Lu, Jian Hu, Xin Dong, Yejin Choi, Jan Kautz, and Yi Dong.
 Prorl: Prolonged reinforcement learning expands reasoning boundaries in large language models.
 CoRR, abs/2505.24864, May 2025a. URL https://doi.org/10.48550/arXiv.2505.
 24864.
Vincent Liu, Adam White, Hengshuai Yao, and Martha White. Towards a practical measure of inter-
  ference for reinforcement learning, 2020. URL https://arxiv.org/abs/2007.03807.
Vincent Liu, Han Wang, Ruo Yu Tao, Khurram Javed, Adam White, and Martha White. Measuring
  and mitigating interference in reinforcement learning, 2023. URL https://arxiv.org/
  abs/2307.04887.
Zichen Liu, Changyu Chen, Wenjun Li, Tianyu Pang, Chao Du, and Min Lin. There may not be
  aha moment in r1-zero-like training — a pilot study. https://oatllm.notion.site/
  oat-zero, 2025b. Notion Blog.
Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min
  Lin. Understanding r1-zero-like training: A critical perspective. In 2nd AI for Math Workshop @
  ICML 2025, 2025c. URL https://openreview.net/forum?id=jLpC1zavzn.
Michael Luo, Sijun Tan, Justin Wong, Xiaoxiang Shi, William Y. Tang, Manan Roongta, Colin
 Cai, Jeffrey Luo, Li Erran Li, Raluca Ada Popa, and Ion Stoica. Deepscaler: Surpassing o1-
 preview with a 1.5b model by scaling rl. https://pretty-radio-b75.notion.site/
 DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005b
 2025. Notion Blog.
MetaAI.    Llama 3.2: Revolutionizing edge ai and vision with open, cus-
 tomizable models.     2024b.          URL   https://ai.meta.com/blog/
 llama-3-2-connect-2024-vision-edge-mobile-devices/.
Skander Moalla, Andrea Miele, Razvan Pascanu, and Caglar Gulcehre. No representation, no trust:
  Connecting representation, collapse, and trust issues in PPO. In Seventeenth European Work-
  shop on Reinforcement Learning, 2024. URL https://openreview.net/forum?id=
  8esP9hxdsM.
OpenAI, Josh Achiam, and et al. Steven Adler. Gpt-4 technical report, 2024. URL https://
  arxiv.org/abs/2303.08774.
Yuxiao Qu, Matthew Y. R. Yang, Amrith Setlur, Lewis Tunstall, Edward Emanuel Beeching,
  Ruslan Salakhutdinov, and Aviral Kumar. Optimizing test-time compute via meta reinforce-
  ment finetuning. In Forty-second International Conference on Machine Learning, 2025. URL
  https://openreview.net/forum?id=TqODUDsU4u.
Yi Ren and Danica J. Sutherland. Learning dynamics of LLM finetuning. In The Thirteenth Interna-
  tional Conference on Learning Representations, 2025. URL https://openreview.net/
  forum?id=tPNHOoZFl9.
Tom Schaul, Diana Borsa, Joseph Modayil, and Razvan Pascanu. Ray interference: a source of
  plateaus in deep reinforcement learning. arXiv preprint arXiv:1904.11455, April 25 2019. doi:
  10.48550/arXiv.1904.11455. URL https://arxiv.org/abs/1904.11455.
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
  optimization algorithms. arXiv preprint arXiv:1707.06347, 2017. URL https://arxiv.
  org/abs/1707.06347.
Amrith Setlur, Matthew Y. R. Yang, Charlie Snell, Jeremy Greer, Ian Wu, Virginia Smith, Max Sim-
 chowitz, and Aviral Kumar. e3: Learning to explore enables extrapolation of test-time compute
 for llms, 2025. URL https://arxiv.org/abs/2506.09026.
Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang, Sewoong Oh, Simon Shaolei Du,
  Nathan Lambert, Sewon Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh Hajishirzi, Pang Wei
  Koh, and Luke Zettlemoyer. Spurious rewards: Rethinking training signals in rlvr, 2025. URL
  https://arxiv.org/abs/2506.10947.


                                               12
Preprint




Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng,
  Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. arXiv preprint
  arXiv: 2409.19256, 2024.
Hongyao Tang and Glen Berseth. Improving deep reinforcement learning by reducing the chain
  effect of value and policy churn. In The Thirty-eighth Annual Conference on Neural Information
  Processing Systems, 2024. URL https://openreview.net/forum?id=cQoAgPBARc.
Hongyao Tang, Johan Obando-Ceron, Pablo Samuel Castro, Aaron Courville, and Glen Berseth.
  Mitigating plasticity loss in continual reinforcement learning by reducing churn. In Forty-second
  International Conference on Machine Learning, 2025. URL https://openreview.net/
  forum?id=EkoFXfSauv.
Fang Wu, Weihao Xuan, Ximing Lu, Zaid Harchaoui, and Yejin Choi. The invisible leash: Why rlvr
  may not escape its origin, 2025. URL https://arxiv.org/abs/2507.14843.
An Yang, Beichen Zhang, and et al. Binyuan Hui. Qwen2.5-math technical report: Toward
  mathematical expert model via self-improvement, 2024a. URL https://arxiv.org/abs/
  2409.12122.
John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R Narasimhan,
  and Ofir Press. SWE-agent: Agent-computer interfaces enable automated software engineering.
  In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024b. URL
  https://openreview.net/forum?id=mXpq6ut8J3.
Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Tiantian Fan, Gaohong
  Liu, Lingjun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan Tong, Chi
  Zhang, Mofan Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen, Jiangjie Chen, Chengyi
  Wang, Hongli Yu, Weinan Dai, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-Ying
  Ma, Ya-Qin Zhang, Lin Yan, Mu Qiao, Yonghui Wu, and Mingxuan Wang. Dapo: An open-
  source llm reinforcement learning system at scale. CoRR, abs/2503.14476, March 2025. URL
  https://doi.org/10.48550/arXiv.2503.14476.
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao
  Huang. Does reinforcement learning really incentivize reasoning capacity in llms beyond the
  base model? arXiv preprint arXiv:2504.13837, April 18 2025. URL https://arxiv.org/
  abs/2504.13837.
Weihao Zeng, Yuzhen Huang, Qian Liu, Wei Liu, Keqing He, Zejun Ma, and Junxian He. Simplerl-
 zoo: Investigating and taming zero reinforcement learning for open base models in the wild, 2025.
 URL https://arxiv.org/abs/2503.18892.
Rosie Zhao, Alexandru Meterez, Sham Kakade, Cengiz Pehlevan, Samy Jelassi, and Eran Malach.
  Echo chamber: Rl post-training amplifies behaviors learned in pretraining. arXiv preprint
  arXiv:2504.07912, April 10 2025. URL https://arxiv.org/abs/2504.07912.
Xinyu Zhu, Mengzhou Xia, Zhepei Wei, Wei-Lin Chen, Danqi Chen, and Yu Meng. The surpris-
  ing effectiveness of negative reinforcement in llm reasoning. arXiv preprint arXiv:2506.01347,
  June 2025. URL https://arxiv.org/abs/2506.01347.




                                                13
Preprint




A     E XPERIMENTAL D ETAILS
A.1   T RAINING DETAILS

Models. We utilize two family of models for RLVR training: Qwen2.5-Math-1.5B and Qwen2.5-
Math-7B (Yang et al., 2024a); and Llama-3.2-3B-Instruct (MetaAI, 2024b).
Training configurations. We utilize the VERL framework (Sheng et al., 2024) for RLVR training.
We train each model on 4 GPUs with a constant learning rate of 10−6 , the maximum response
length is 3072 for Qwen2.5-Math models, and 8192 maximum generation tokens for Llama-3.2-3B-
Instruct. We use a mini batch size and a rollout batch size of 64. For each prompt, we collect 8
rollouts to compute advantages for the GRPO update. We use a sampling temperature τ = 1. We do
not apply Reverse KL divergence or entropy loss in our training, and the total training steps are 500,
similar to prior works (Shao et al., 2025; Yu et al., 2025; Luo et al., 2025). We set the hyperparameter
controlling the trade-off between reward maximization and Forward KL regularization to β = 10−4 .
Reward function. For the reward function r(x, y) calculation, we follow the implementation of
(Zeng et al., 2025; Hu et al., 2024) with the following rule for faster convergence:

 • If the response provides a final answer in the boxed format and is correct, it receives a reward
   of +1.
 • If the response provides a final answer in the boxed format, but it is incorrect, we set the reward
   as −0.5.
 • Otherwise, the reward is set to −1 for incorrect answers.

A.2   P ROBING DATASET CONSTRUCTION

One major problem when analyzing learning dynamics is the huge response space Y: the number of
possible responses y ∈ V L , not only includes natural language but also non-sensical texts. In this
paper, we are interested in the response region from the base model πb , due to the following reason:
the concentration coefficient C(πθ , πb ) is small, since RLVR tends to reduce the coverage compared
to the base model, we can expect that base model distribution can provide coverage of the learned
policy πθ .
To create the probing dataset Dprob , for each problem in the training dataset x ∈ D, we sample
k = 4 responses from the base model with temperature τ = 0.9 to ensure diversity and accuracy.

A.3   P ROMPT T EMPLATE

We use the prompt templates for Qwen2.5-Math models and Llama-3.2-3B-Instruct following (Yang
et al., 2024a; Luo et al., 2025), as shown in Table 2 and Table 3.

                            Table 2: Prompt template for Qwen2.5-Math.


  <|im start|>system
  Please reason step by step, and put your final answer within \boxed{}.<|im end|>
  <|im start|>user
  {input}
  Let’s think step by step and output the final answer within \boxed{}.<|im end|>
  <|im start|>assistant




                                                  14
Preprint




                         Table 3: Prompt template for Llama-3.2-3B-Instruct.


  <|begin of text|><|start header id|>system<|end header id|>
  Cutting Knowledge Date: December 2023
  <|start header id|>user<|end header id|>
  {input}
  Let’s think step by step and output the final answer within \boxed{}.<|eot id|>
  <|eot id|><|start header id|>assistant<|end header id|>



A.4    E VALUATION D ETAILS

Across all checkpoints, we evaluate using a temperature τ = 0.6 and a top-p value of 0.95, following
prior works (Yue et al., 2025; Zeng et al., 2025; Lewkowycz et al., 2022), with a maximum gener-
ation of 3072 tokens for Qwen2.5-Math due to limited context length. For Llama-3.2-3B-Instruct,
we allow the model to generate a maximum of 16384 tokens.

B     D ETAILS D ERIVATION OF GRPO
Given a problem x and the generated solutions {y}G     i=1 , where G > 2 is the number of generated
solutions per prompt. We define each token index t in the response y as yt with 1 ≤ t ≤ |y|, where
|y| is the sequence length of the reasoning traces. Specifically, for each problem x, GRPO objective
DeepSeek-AI et al. (2025) will first calculate group-wise normalized advantage function:
                                                    r(x, yi ) − µ̂
                                      A(x, yi ) =                                               (10)
                                                         σ̂
                                      s
                G                              G
              1                           1
                P                              P
where µ̂ = G       r(x, yj ), and σ̂ = G−1       (r(x, yj ) − µ̂)2 .
               j=1                              j=1

Let πold denote the policy from the previous update step that generates the reasoning traces. The
                                 t |x,y<t )
probability ratio ρt = ππoldθ (y
                              (yt |x,y<t ) at each token index t, along with PPO clipping mechanism to
serves as a proxy of trust region contraint with clipping threshold ϵ, the GRPO objective is defined
as:
                                " |y|                                                                     #
                                    X                                                                 
   J(θ) = Ex∼D, y∼πold (·|x)            min ρt (y; θ) A(x, yi ), clip ρt (y; θ), 1 − ϵ, 1 + ϵ A(x, yi )
                                t=1
                                                                         h                      i
                                                                  −β Ex∼D KL πθ (·|x) ∥ πb (·|x) .
                                                                                                       (11)

The KL regularization helps the learned policy not deviate too far from the base model. Recently, Yu
et al. (2025) suggests that removing KL regularization can provide better performance. Following
this, we set β = 0 to eliminate KL regularization in our work.

C     P ER - STEP I NFLUENCE P ROOFS AND F URTHER A NALYSIS
C.1    P ROOF OF P ROPOSITION 3.1

Proposition C.1. Consider a problem-solutions pair (x, y) for updating using policy gradient ob-
jective, a sufficiently small learning rate η, the per-step influence on a problem-solution pair (x′ , y ′ )
is defined as:
                         ∆ log πθt (y ′ |x′ ) = η Kt (x, x′ , y, y ′ )A(x, y) + O(η 2 )              (12)
where Kt (x, x′ , y, y) = ∇θ log πθt (y|x)⊤ ∇θ log πθt (y ′ |x′ ) measures the influence between
(x, y) and (x′ , y ′ ), and the advantage function A(x, y) determines the magnitude and direction
of the model’s update.


                                                      15
Preprint




Proof. We first approximate log πθt+1 (y|x) using Taylor expansion. For simplicity, we denote
πθt = πθt :

              log πθt+1 (y|x) = log πθt (y|x) + ∇θ log πθt (y|x)⊤ (θt+1 − θt ) + O(η 2 )             (13)
Using the definition of stochastic gradient ascent with a sufficiently small learning rate η, we have
that:
                                        θt+1 = θt + η∇θ J (πθ )                                      (14)
where ∇θ J (πθ ) = A(x, y)∇θ log πθ (y|x) is the standard policy gradient objective (Qu et al.,
2025; Ahmadian et al., 2024), we plug in the above objective in Eq. 13:
                        ∆ log πθt (y ′ |x′ ) = ηK(x, x′ , y, y ′ )A(x, y) + O(η 2 )                  (15)
which concludes the proof.

C.2   I NTERPRETATION OF THE RELATIVE STRENGTH OF INFLUENCE ||∆(πθt µ)||

If we view the language model πθ as a neural network with a problem and solution pair o = (x, y)
as an input, where the output is the log-probability
                                                     |y|
                                                 1 X
                               log πθ (y|x) =           log πθ (yt |x, y<t )                         (16)
                                                |y| t=1

where y<t is the partial completion before the token index t. We consider the gradient of πθ with
respect to parameter θ at (x, y) as ∇θ log πθ (y|x) ∈ Rd where d is the parameter dimension. We
can define a matrix of gradient dot products K(x, x′ , y, y ′ ) = K(o, o′ ) across all different prompt-
response pair:
                                                    
              K(o1 , o1 )       K(o1 , o2 )   ···
             K(o2 , o1 )       K(o2 , o2 )   ···                        ⊤
           K=                                        = ∇θ log πθ (Y|X ) ∇θ log πθ (Y|X )           (17)
                                                     
                 ..                ..         ..
                  .                 .            .

where ∇θ log πθ (Y|X ) = [∇θ log πθ (y1 |x1 ), ∇θ log πθ (y2 |x2 ), · · · ] denotes the matrix of the gra-
dient of different prompt-solution pairs (x, y).
In an idealized scenario, the kernel matrix K is diagonal, meaning that all off-diagonal terms are
zeros, i.e., K(oi , oj ) = 0 for i ̸= j. Under this assumption, improving performance on a given
training problem-solution pair would not influence any other unseen problems. Consequently, there
would be neither negative interference, where training on one example degrades performance on
others, nor coverage shrinkage, where the set of solvable problems becomes narrower.
In practice, however, this assumption rarely holds for language models. Because parameters are
shared across all examples, updates to one example inevitably affect others. This manifests as non-
zero off-diagonal entries in K, which capture the degree of cross-influence between examples.
The growing magnitude of the relative influence strength, ||∆(πθt , µ)||, can thus be interpreted as
evidence that the number and magnitude of these off-diagonal interactions are increasing. Specif-
ically, this signals that the gradients of different examples are becoming more linearly dependent,
since the rank of the kernel K is equivalent to the rank of the gradient matrix ∇θ log πθ (Y|X ).
This growing entanglement explains why optimization on a subset of problems may inadvertently
interfere with generalization to others.

D     A NALYZING LEARNING DYNAMIC OF ON - POLICY LEARNING IN TOY
      BANDIT PROBLEM .

We first consider a contextual bandit problem with a parametrized softmax policy with V actions.
where the input data x is a d dimensional feature vector x ∈ Rd . The policy is defined as a linear


                                                     16
Preprint




layer with Softmax output:
                                                              exp(zi (x))
                                         πθ (yi |x) =        V
                                                                                                                     (18)
                                                             P
                                                                exp(zj (x))
                                                            j=1
We consider the objective of REINFORCE and Off-policy maximum likelihood objectives for 2
actions y1 and y2 that receive a positive reward (r(x, y) = 1).
    J REINFORCE (πθ ) = πθ (a1 |x) + πθ (a2 |x), J MLE (πθ ) = log πθ (a1 |x) + log πθ (a2 |x) (19)
Using gradient descent, we can perform parameter update at each update step t with a learning rate
η:
θ t+1 = θ t + η∇θ J REINFORCE = θ t − ηx (πθt (y1 )(πθt (y) − e(y1 ))⊤ + πθt (y2 )(πθt (y) − e(y2 ))⊤
                                                                                                     

θ t+1 = θ t + η∇θ J MLE = θ t − ηx ((πθt (y) − e(y1 )⊤ + (πθt (y) − e(y2 ))⊤
                                                                                
                                                                                               (20)
where πθ (y) ∈ RV is the vector represents probability distribution over all actions, e(y) is a one-hot
vector indicates the target action. A key difference between the REINFORCE and MLE objectives
is that, in REINFORCE, the probability of the sampled actions directly scales the update step. As
a result, actions with higher likelihood receive larger updates, while low-likelihood actions lead to
much smaller changes. To analyze how the model’s probabilities in each action change, we define a
             π t+1
ratio αi = πiti and use The following lemma describes its behavior:
Lemma D.1. The ratio of confidence change for each i can be represented as:
                                    PV        zjt                  PV      zjt
                    MLE   πit+1         j=1 e          REINFORCE     j=1 e
                  αi =           = PV           zjt
                                                    ; αi         = PV        zjt
                                                                                                                     (21)
                            πit       j=1 βj e                      j=1 γj e

Note that the values of βj also depends on whether i ∈ {y1 , y2 }, hence for Case 1 (i ∈ {y1 , y2 }),
and Case 2 (i ∈/ {y1 , y2 }):
Case 1:                                                          
                                                                    −η ′ (∆π t (πjt −πit )+πit )
       −η′ 2(πt −πt +1
           ( j i )                                                                                 if j ∈
                                                                                                        / {y1 , y2 }
      e                         if j ∈
                                      / {y1 , y2 }               e
                                                                
                                                                 
 βj =          1                        if j = y1 ;         γj =           1                              if j = y1 (22)
      
       −2η′ (πt −πt )                                                ′
        e                              if j = y2                  −η ((∆πt −1)(πjt −πit )
                                                                 
               j   i
                                                                  e                                     if j = y2
Case 2:
        ( −2η′ πt −πt                                               ( −η′ ∆πt (πt −πt )
         e    ( j i)                if j ∈
                                         / {y1 , y2 }                e       ( j i )                 if j ∈
                                                                                                          / {y1 , y2 }
   βj =     ′
                                                        ;      γj =     ′
         e−η (2(πj −πi )−1)                                          e−η (∆π (πj −πi )−πj )
                 t    t                                                      t  t   t   t
                                    if j ∈ {y1 , y2 }                                                if j ∈ {y1 , y2 }
                                                                                                                      (23)
where ∆π t = πyt 1 + πyt 2 , η ′ = η||x||22 .

Proof. We first need to link the logits vector z t+1 and z t . From Eq.20, z t+1 can be recursively
written as:
                                 z t+1 = (θ t+1 )⊤ x
                                                         ⊤
                                       = θ t + ηx∇z J ) x
                                                                              ⊤
                                            = (θ t )⊤ x + η (x∇z J ) x
                                            = z t + η ′ ∇z J                                                         (24)

where η ′ = η||x||22 . We can write down for each value in vector z t+1 for MLE and REINFORCE
objectives as:
                                         (
                                   t+1
                                           zit − 2η ′ πit          if i ∈
                                                                        / {y1 , y2 }
                            MLE: zi =        t        ′ t     ′
                                           zi − 2η πi + η if i ∈ {y1 , y2 }
                                         (
                                           z t − η ′ (∆π t · πit )      if i ∈
                                                                             / {y1 , y2 }
                  REINFORCE: zit+1 =         t     ′      t         t
                                           z − η (∆π − 1)πi if i ∈ {y1 , y2 }


                                                             17
Preprint




Then, we can write down the probability change πit+1 for each action i. For case i ∈ {y1 , y2 }, we
have the following derivation for MLE objective:
                       t+1                                                                                                              t                   ′       t           ′
              t      ezi                                                                                                           ezi −2η πi +η
             πy1 = PV                                 =                                            t               ′       t                t                       ′       t                   ′               t                       ′   t               ′               (25)
                          zjt+1                                                            ezj −2η πj + ezy1 −2η πy1 +η + ezy2 −2η πy2 +η
                                                                       P
                    j=1 e
                                                              j ∈{y
                                                                / 1 ,y2 }
                                                                                                               t
                                                                ezi
                  =                                                                                                                                                                                                                                                         (26)
                                            ezj −η (2(πj −πi )+1) + ezy1 −0 + ezy2 −2η (πy2 −πi )
                           P                  t   ′    t   t          t         t     ′  t    t


                      j ∈{y
                        / 1 ,y2 }


Similarly, for REINFORCE objective,
            t+1                                                                                                                t        ′                   t                   t
   t      ezi                                                                                                          ezi −η (∆π −1)πi
  πy1 = PV                         =                                   t           ′                           t                   t                ′                   t                   t                       t               ′               t               t       (27)
               zjt+1                                           ezj −η (∆π ·πj ) + ezy1 −η (∆π −1)πy1 + ezy2 −η (∆π −1)πy2
                                                                                                   t
                                                 P
         j=1 e
                                           j ∈{y
                                             / 1 ,y2 }
                                                                                                       t
                                                                                               ezi
      =                                                                                                                                                                                                                                                                     (28)
                          ezj −η (∆π (πj −πi )+πi ) + ezy1 −0 + ezy2 −η ((∆π −1)(πy2 −πi ))
               P               t       ′          t       t        t           t                           t                                t                   ′                   t                   t               t


            j ∈{y
              / 1 ,y2 }


For case i ∈
           / {y1 , y2 }, we have the following derivation for MLE objective:
                               t+1                                                                                                      t               ′               t
                    ezi                                                                                                            ezi −η (2πi )
            πit = PV                   t+1 =                                           zjt −2η ′ πjt                                    t                       ′       t               ′                   t                   ′       t               ′                   (29)
                                   zj                                                                                      + ezy1 −2η πy1 +η + ezy2 −2η πy2 +η
                                                                P
                          j=1 e
                                                                                       e
                                                          j ∈{y
                                                            / 1 ,y2 }
                                                                                                                               t
                                                                                                                        ezi
                =                                                                                                                                                                                                                                                           (30)
                                           ezj −2η (πj −πi ) + ezy1 −η (2(πy1 −πi )−1) + ezy2 −η (2(πy2 −πi )−1)
                          P                  t            ′    t           t                           t               ′            t                   t                                       t           ′               t               t


                    j ∈{y
                      / 1 ,y2 }

Similarly for REINFORCE objective:
           t+1                                                                                                                 t        ′                   t           t
   t     ezi                                                                                                            ezi −η (∆π ·πi )
  πi = PV                      =                                   t           ′                           t                   t                ′                   t                   t                       t               ′               t               t           (31)
             zjt+1                                            ezj −η (∆π ·πj ) + ezy1 −η (∆π −1)πy1 + ezy2 −η (∆π −1)πy2
                                                                                               t
                                             P
        j=1 e
                                       j ∈{y
                                         / 1 ,y2 }
                                                                                                                               t
                                                                                                                        ezi
      =
                         ezj −η (∆π (πj −πi )) + ezy1 −η (∆π (πy1 −πi )−πy1 ) + ezy2 −η (∆π (πy2 −πi )−πy2 ))
              P            t       ′          t       t        t                           t                   ′           t       t                t                   t                           t               ′               t       t               t           t


           j ∈{y
             / 1 ,y2 }
                                                                                                                                                                                                                                                                            (32)



We can now better understand how each πi changes after one update. Specifically, if αi > 1, the
corresponding πi increases, and vice versa. To determine the value of αi , we can treat any βj > 1
as contributing to the conclusion that αi < 1, while any βj < 1 against it. The value of the
                 t
corresponding ezj and |βj − 1| controls how strong the contribution is.
Low-likelihood tokens tend to receives less meaningful updates. Using the log-derivative trick,
∇θ πy = πy ∇θ log πy , we see that REINFORCE inherently applies a conservative update rule: to-
kens with higher probability receive proportionally larger gradient updates, while low-probability
tokens are updated much more weakly. This disproportionate updating can have a detrimental effect
in cases where optimal actions may reside in low-probability regions of the distribution, yet RE-
INFORCE fails to provide sufficient reinforcement for these tokens to be effectively explored and
learned.
Assuming πyt 1 > πyt 2 , then πyt 1 is guaranteed is increase, i.e., αy1 > 1. To see this, consider the
value of γ in Case 1 of the REINFORCE objective. For any j ∈      / y1 , y2 , we have γj < 1 because
                                   ∆π t (πjt − πit ) + πit = ∆π t πjt + (1 − ∆π t )πit > 0.                                                                                                                                                                                 (33)


                                                                                                                   18
Preprint




Moreover, since γy1 = 1 while γy2 < 1, the probability of the highest-likelihood action y1 will
increase. In addition, because the update step size depends on the probability of the sampled action,
the smaller πyt 1 is, the more strongly πyt 2 will decrease, leading the model to gradually concentrate
its mass on the dominant mode πyt 1 . However, this is not the case for the maximum likelihood
objective; later, as we show in section 2, the maximum likelihood objective will tend to increase the
lower probability πyt 2 , avoiding model collapse.

D.1                                                        E MPIRICAL V ERIFICATION WITH A SIMPLE BANDIT PROBLEM .

To empirically verify the analysis above, we analyze using a simple logistic regression task following
Ren & Sutherland (2025). We set the vocabulary size V = 50, with parameter dimension d = 5, a
learning rate of η = 0.5, and a randomly generated input vector x. We compared the update effect
of MLE and REINFORCE objectives in 2 scenarios: when the initial distribution πθ0 is relatively
uniform and when it’s highly peaked around certain dimensions.
                                                            Probability change in REINFORCE                                            Probability change in MLE                         Probability ratio α in MLE               Probability ratio α in REINFORCE
                                           1.0
                                                                                                          0.7
A: Positive gradient uniform




                                                                                                                                                                              60
                                                                                                  πθ 1                                                                                                                     1.0
                                           0.8                                                            0.6
                                                                                                  πθ 0                                                                        50
                                                                                                                                                                                                                           0.8
                                                                                                          0.5
                                           0.6
                                                                                                                                                                              40
                                                                                                          0.4
                                                                                                                                                                                                                           0.6
                                           0.4                                                            0.3                                                                 30
                                                                                                                    y2+                                                                                                    0.4
                                                                                                          0.2                                                                 20
                                           0.2
                                                     y2+         y1+                                      0.1                     y1+                                                                                      0.2
                                                                                                                                                                              10
                                           0.0
                                                                                                          0.0
                                                                                                                                                                               0                                           0.0
                                                 0               10        20        30      40      50         0                 10          20        30         40   50
                                                                                                                                                                                    y+
                                                                                                                                                                                     1                                y+
                                                                                                                                                                                                                       2         y+
                                                                                                                                                                                                                                  1                             y+
                                                                                                                                                                                                                                                                 2
                                           1.0
B: Negative gradient uniform




                                                                                                          0.4                                                                                                              1.0
                                                                                                                                                                             1.50
                                           0.8
                                                                                                                                                                             1.25                                          0.8
                                                                                                          0.3
                                           0.6
                                                                                                                                                                             1.00                                          0.6
                                                       y∗                                                 0.2         y ∗ y1−
                                           0.4                                                                                                                               0.75
                                                                 y1−                                                                                                                                                       0.4
                                           0.2                                                            0.1                                                                0.50
                                                                                                                                                                                                                           0.2
                                                                                                                                                                             0.25
                                           0.0
                                                                                                          0.0
                                                                                                                                                                             0.00                                          0.0
                                                 0               10        20        30      40      50         0                 10          20        30         40   50
                                                                                                                                                                                    y+                                y∗         y+                              y∗
                                           1.0
                                                                                                          1.0
C: Negative gradient Peaky




                                                                                                                                                                              1.2                                          1.0
                                           0.8
                                                                                                          0.8
                                                                                                                                                                              1.0
                                                                                                                                                                                                                           0.8
                                           0.6
                                                                                                          0.6                                                                 0.8
                                                                                                                                                                                                                           0.6
                                           0.4             y∗                                                             y   ∗                                               0.6
                                                                 y1−                                      0.4
                                                                                                                                                                                                                           0.4
                                                                                                                                                                              0.4
                                           0.2
                                                                                                          0.2                     y1−
                                                                                                                                                                              0.2                                          0.2
                                           0.0
                                                                                                          0.0
                                                                                                                                                                              0.0                                          0.0
                                                 0               10        20        30      40      50         0                 10          20        30         40   50
                                                                                                                                                                                    y+                                y∗         y+                              y∗
                                           1.0                                                            0.8
                                                                                                                                                                               4
                                                                                                                          y2+
D: Positive gradient peaky




                                                                                                                                                                                                                           1.0
                                           0.8
                                                                                                          0.6
                                                           y2+                                                                                                                 3                                           0.8
                                           0.6
                                                                                                          0.4                                                                                                              0.6
                                           0.4                                                                                                                                 2

                                                                 y1+                                                                                                                                                       0.4
                                           0.2                                                            0.2
                                                                                                                                                                               1
                                                                                                                                                                                                                           0.2
                                           0.0
                                                                                                          0.0
                                                                                                                                                                               0                                           0.0
                                                 0               10        20        30      40      50         0                 10          20        30         40   50
                                                                                                                                                                                    y+                                y+         y+                             y+
D: Positive gradient after 10 iterations




                                                                                                                                                                                     1                                 2          1                              2
                                           1.0
                                                                                                          1.0                                                                                                              1.2
                                                                                                                                                                             15.0
                                           0.8
                                                                                                                                                                                                                           1.0
                                                           y2+                                            0.8             y2+                                                12.5
                                           0.6                                                                                                                                                                             0.8
                                                                                                                                                                             10.0
                                                                                                          0.6
                                           0.4                                                                                                                                7.5                                          0.6

                                                                 y1+                                      0.4
                                                                                                                                                                                                                           0.4
                                           0.2                                                                                                                                5.0
                                                                                                          0.2                                                                                                              0.2
                                           0.0                                                                                    y1+                                         2.5

                                                                                                          0.0                                                                 0.0                                          0.0
                                                 0               10        20        30      40      50         0                 10          20        30         40   50
                                                                                                                                                                                    y+
                                                                                                                                                                                     1                                y+
                                                                                                                                                                                                                       2         y+
                                                                                                                                                                                                                                  1                             y+
                                                                                                                                                                                                                                                                 2
                                                                       Index of vocabulary                                                Index of vocabulary
                                                                                                                                                                                                Token Index                                 Token Index




Figure 9: Experimental verification and comparison between REINFORCE and MLE objectives
using a simple contextual bandit problem.


Uniform case: we consider negative and positive gradient effect, in the negative gradient case,
we consider negative label y − = 11 and investigate the ”indirect” push-up effect on y2 = 5. In
the positive gradient scenario, we use 2 positive actions y1 = 11, y2 = 5 for the SGD update.
As demonstrated in the first 2 rows in Fig. 9, both REINFORCE and MLE behave similarly in
both negative and positive gradient scenarios, where both y1 , y2 are increased. However, MLE
aggressively imposes a large update, where the probability is approximately 60 times larger on
these two tokens after the update, as measured by the probability ratio α. Similarly, a negative
gradient tends to increase the highest-likelihood token y ∗ , while decreasing other actions, including
the positive action y2 . This can be explained by REINFORCE by imposing a probability step-size,
resulting in a more conservative update, where the models less deviate from their previous step
compared to the MLE objective.
Peaky case: In LLM regime, the LMs usually initialize from a pre-trained checkpoint, where the
model exhibits a non-uniform distribution. We consider the scenario where the models concentrate
on a few dimensions in action distribution. Similarly, negative label y − = 11 and investigate the


                                                                                                                                                                        19
Preprint




”indirect” push-up effect on y2 = 8. In the positive gradient scenario, we use 2 positive actions
y1 = 11, y2 = 8 for the SGD update. As shown in the last 3 rows in Fig. 9, when the distribution is
peaky, the negative gradient exacerbates the effect of increasing the highest probability token while
decreasing other actions, regardless of correctness Ren & Sutherland (2025). Interestingly, in a
positive gradient scenario, between the 2 positive actions, MLE tends to push up the actions with the
lowest likelihood (as measured by α). In the last row, we observe that after 10 iterations of training,
MLE can converge to a new distribution with equal probabilities between 2 actions. However,
REINFORCE shows favor for the actions with the highest probability; this effect will exacerbate
after multiple updates, where it collapses the highest probability π(y1 = 8). This suggests that
offline learning can still provide benefits compared to REINFORCE in avoiding model collapse.

E            A DDITIONAL R ESULTS ON DIFFERENT MODELS

                                                                                                Qwen2.5-Math-1.5B
                                                                                                                                                                                                                                                +
                     ∆+ (πθt , µ)                                  ||∆(πθt , µ)||                                     Entropy                                     Response Length                                            Log likelihood on Dprob
 0.002                                                                                                                                                                                                           −0.20
                                                0.018
                                                                                                                                                 1050
                                                                                                 0.250
 0.000
                                                0.016                                                                                                                                                            −0.22
                                                                                                 0.225                                           1000
−0.002




                                                                                                                                                                                                Log likelihood
                                                0.014
−0.004                                                                                           0.200                                            950                                                            −0.24
                                                0.012
−0.006                                                                                           0.175                                            900
                                                0.010                                                                                                                                                            −0.26
−0.008                                                                                           0.150                                            850
                                                0.008
−0.010                                                                                                                                                                                                           −0.28
                                                0.006                                            0.125                                            800
−0.012
                                                0.004                                            0.100                                            750                                                            −0.30

         0   100      200    300    400   500           0   100      200    300     400   500            0   100      200   300     400   500           0   100       200   300     400   500                            0    100      200   300     400   500
                   Training steps                                 Training steps                                   Training steps                                  Training steps                                                   Training steps


                                                                                                Qwen2.5-Math-7B
                                                                                                                                                                                                                                                +
                    ∆+ (πθt , µ)                                   ||∆(πθt , µ)||                                     Entropy                                     Response Length                                            Log likelihood on Dprob
 0.00
                                                0.10

−0.01                                                                                                                                                                                                            −0.3
                                                                                                 0.20                                           1000
                                                0.08




                                                                                                                                                                                                Log likelihood
−0.02
                                                                                                                                                                                                                 −0.4
                                                                                                 0.15
                                                0.06                                                                                             900
−0.03
                                                                                                                                                                                                                 −0.5
                                                                                                 0.10
−0.04                                           0.04                                                                                             800

                                                                                                                                                                                                                 −0.6
−0.05                                                                                            0.05
                                                0.02
                                                                                                                                                 700
−0.06                                                                                                                                                                                                            −0.7
         0   100     200     300    400   500           0   100     200     300     400   500            0   100     200    300     400   500           0   100      200    300     400   500                            0   100      200    300     400   500
                   Training steps                                 Training steps                                   Training steps                                  Training steps                                                   Training steps


                                                                                           Llama-3.2-3B-Instruct
                                                                                                                                                                                                                                                +
                    ∆+ (πθt , µ)                                   ||∆(πθt , µ)||                                     Entropy                                     Response Length                                            Log likelihood on Dprob
                                                                                                                                                                                                                 −0.2
 0.00                                           0.14
                                                                                                                                                1100
                                                                                                  1.0
                                                0.12                                                                                                                                                             −0.4
−0.02
                                                                                                                                                1000
                                                                                                                                                                                                Log likelihood




                                                                                                  0.8
                                                0.10
−0.04                                                                                                                                                                                                            −0.6
                                                0.08                                              0.6                                            900

−0.06                                                                                                                                                                                                            −0.8
                                                0.06
                                                                                                  0.4                                            800
−0.08                                           0.04
                                                                                                                                                                                                                 −1.0
                                                                                                  0.2                                            700
                                                0.02
−0.10
                                                                                                                                                                                                                 −1.2
                                                                                                  0.0
         0   100     200     300    400   500           0   100     200     300     400   500            0   100     200    300     400   500           0   100      200    300     400   500                            0   100      200    300     400   500
                   Training steps                                 Training steps                                   Training steps                                  Training steps                                                   Training steps



                                    Figure 10: Learning dynamics of RLVR model with different models.

Consistent learning dynamics across different models. In this section, we provide additional
results that our findings hold across different model families and sizes. Specifically, we conduct
GRPO experiments on a larger model, Qwen2.5-Math-7B, as well as a different family, Llama-3.2-
3B-Instruct. As shown in Fig. 10, our analysis consistently holds across these settings.
Larger models tend to suffer more from negative interference. Interestingly, we find that the
negative interference phenomenon becomes more severe when scaling up to larger models such as
Qwen2.5-Math-7B. This also helps explain why, under RLVR training, the Pass@k performance of
Qwen2.5-Math-7B with large sampling budgets k can even underperform than the smaller Qwen2.5-
Math-1.5B after GRPO.
Detailed Pass@k performance. We present detailed Pass@k curves for Qwen2.5-Math-1.5B and
Qwen2.5-Math-7B of different methods below:




                                                                                                                    20
Preprint




                                                                                                    Qwen2.5-Math-1.5B
                           AIME24                                                      AIME25                                                          Matht500                                                             Minerva
0.8                                                              0.7                                                      0.95
                 GRPO                                                       GRPO                                                            GRPO                                                            GRPO
                                                                 0.6                                                      0.90                                                              0.6
0.7
                 Base                                                       Base                                                            Base                                                            Base
0.6              Ours                                            0.5        Ours                                          0.85              Ours                                                            Ours
                                                                                                                                                                                            0.5

0.5                                                                                                                       0.80
                                                                 0.4
                                                                                                                                                                                            0.4
0.4                                                                                                                       0.75
                                                                 0.3

0.3                                                                                                                       0.70
                                                                                                                                                                                            0.3
                                                                 0.2
0.2                                                                                                                       0.65
                                                                 0.1                                                                                                                        0.2
                                                                                                                          0.60
0.1

       1         4         16       64       256          1024         1    4          16           64     256   1024            1      2        4         8        16    32     64   128         1    2            4       8          16    32    64   128
                                k                                                               k                                                              k                                                                  k

                                                                                                     Qwen2.5-Math-7B
                           AIME24                                                      AIME25                                                          Matht500                                                             Minerva
0.9
                                                                 0.7                                                                                                                        0.7
                 GRPO                                                       GRPO                                          0.95              GRPO                                                            GRPO
0.8
                 Base                                            0.6        Base                                          0.90              Base                                            0.6             Base
0.7
                 Ours                                            0.5
                                                                            Ours                                          0.85
                                                                                                                                            Ours                                                            Ours
                                                                                                                                                                                            0.5
0.6
                                                                 0.4                                                      0.80
0.5                                                                                                                                                                                         0.4
                                                                                                                          0.75
                                                                 0.3
0.4                                                                                                                                                                                         0.3
                                                                                                                          0.70
0.3                                                              0.2
                                                                                                                          0.65                                                              0.2
0.2                                                              0.1
                                                                                                                          0.60
                                                                                                                                                                                            0.1
       1         4         16       64       256          1024         1    4          16           64     256   1024            1      2    4         8       16    32    64 128 256             1   2         4       8         16    32    64 128 256
                                k                                                               k                                                              k                                                                  k

                                                                                                    Llama-3.2-3B-Instruct
                            AIME24                                                     AIME25                                                          Matht500                                                             Minerva
                                                                 0.5                                                      0.9
0.5              GRPO                                                       GRPO                                                            GRPO                                                           GRPO
                                                                                                                                                                                            0.5
                 Base                                            0.4
                                                                            Base                                          0.8               Base                                                           Base
0.4
                 Ours                                                       Ours                                          0.7               Ours                                                           Ours
                                                                                                                                                                                            0.4
                                                                 0.3
0.3                                                                                                                       0.6
                                                                                                                                                                                            0.3
                                                                 0.2                                                      0.5
0.2
                                                                                                                                                                                            0.2
                                                                 0.1                                                      0.4
0.1
                                                                                                                          0.3                                                               0.1
                                                                 0.0

       1         4         16       64        256         1024         1    4          16           64     256   1024            1      2    4         8       16    32    64 128 256             1   2         4       8       16      32    64 128 256
                                k                                                               k                                                              k                                                                  k


               Figure 11: Pass@k curves for base model, RLVR model and SELF with different models.


F              P ERFORMANCE DEGRADATION IN W-REINFORCE
We also experiment with recent work W-REINFORCE Zhu et al. (2025), which upweights the
negative gradient signal to encourage diversity. As shown in Fig. 2, we find that W-REINFORCE
suffers significantly from the catastrophic forgetting issue, where the average accuracy decreases
even before 300 steps. We hypothesize that it is due to the high variance of the REINFORCE objec-

                                          Rewards                                                                       Entropy                                                                       Response Length
 0.1
                                                                                 0.8                                                                                      3000
                 W-REINFORCE                                                                         W-REINFORCE                                                                        W-REINFORCE
 0.0
                                                                                 0.7
−0.1                                                                                                                                                                      2500
                                                                                 0.6
−0.2
                                                                                 0.5
−0.3                                                                                                                                                                      2000
                                                                                 0.4
−0.4
                                                                                 0.3
                                                                                                                                                                          1500
−0.5
                                                                                 0.2
−0.6
                                                                                 0.1                                                                                      1000
−0.7
                                                                                 0.0
           0         100            200             300          400       500              0            100      200             300            400                500          0          100           200               300              400        500
                                    Training steps                                                                Training steps                                                                       Training steps



Figure 12: Learning dynamics of W-REINFORCE, we observe that W-REINFORCE suffer from
training instability under prolong training.

tive. Furthermore, progressively learning with a negative gradient can result in improper increases
in tail probabilities Li et al. (2025b), leading the models to generate non-meaningful tokens.

G              C OMPUTATIONAL COST OF SELF
Our method require an additional greedy generation to filter highly solvable problems. To analyze
the computational cost of SELF and GRPO, we utilize per-iteration time of each update step with 3
factors: total generation time Tgen , backward time Tbackward , and forward time Tforward . We provide


                                                                                                                    21
Preprint




our results in Fig. 13 We find that SELF incurs an additional cost in generation time compared to

                                             Total time                                                                           Forward time                                                                          Generation time                                                                                 Backward time
                     160
                                         GRPO                                                                   20              GRPO                                                               80                  GRPO                                                                   50
                                                                                                                                                                                                                                                                                                                       GRPO
                     150
                                         SELF                                                                   18              SELF                                                               75                  SELF                                                                                            SELF
                                                                                                                                                                                                                                                                                              45
Time (s/step)




                                                                                         Time (s/step)




                                                                                                                                                                                Time (s/step)




                                                                                                                                                                                                                                                                          Time (s/step)
                     140                                                                                                                                                                           70
                                                                                                                16
                     130                                                                                                                                                                           65                                                                                         40
                                                                                                                14
                     120                                                                                                                                                                           60                                                                                         35
                                                                                                                12
                     110                                                                                                                                                                           55
                                                                                                                                                                                                                                                                                              30
                                                                                                                10                                                                                 50
                     100
                                                                                                                 8                                                                                 45                                                                                         25
                         90
                                0       20          40         60        80        100                                 0       20          40        60        80         100                              0          20           40        60          80         100                                    0          20         40          60          80          100
                                              Training steps                                                                         Training steps                                                                          Training steps                                                                                   Training steps

                                    Figure 13: Computational results for training Qwen2.5-Math-1.5B for 100 steps.

GRPO. However, due to the filtering mechanism, both the forward and backward passes are faster,
which compensates for the extra generation time and results in a negligible overall computational
cost relative to GRPO.


 H                              P ERPLEXITY D ETAIL A NALYSIS

In this section, we provide a detailed perplexity analysis. Across all benchmarks, we randomly
sample 16 reasoning traces for each problem in the test dataset to calculate perplexity.
To collect problems that increased after RLVR D↑ , we estimate the average accuracy for each prob-
lem and sort the problem indices according to average accuracy changes between the base policy
and RLVR policy:
                                                                                  ∆r(x) = Ey∼πθ (y|x) [r(x, y)] − Ey∼πb (y|x) [r(x, y)]                                                                                                                                                                                                                        (34)

For AIME 2024/2025, we sample the top-3 problems that increased the most for D↑ and top-3
problems decreased for D− , as these benchmarks only consist of 30 problems. For Math500 and
Minerva, we sample top-64 problems for both D+ and D↓ . We present out results in Fig. 14.

                                                      AIME24                                                                                 AIME25                                                                                  Math500                                                                                           Minerva
                                                                                                            1.150                                                                                  1.130                                                                                      1.144

                     1.140
                                                                                                            1.145                                                                                  1.125                                                                                      1.142
        Perplexity




                                                                                               Perplexity




                                                                                                                                                                                     Perplexity




                                                                                                                                                                                                                                                                                Perplexity




                     1.135
                                                                                                            1.140                                                                                                                                                                             1.140
                                                                                                                                                                                                   1.120
                     1.130
                                                                                                            1.135                                                                                                                                                                             1.138
                                                                                                                                                                                                   1.115
                     1.125                                                                                  1.130                                                                                                                                                                             1.136
                                                                                                                                                                                                   1.110
                                0       100         200       300       400        500                                 0       100         200       300       400        500                                  0       100         200       300         400        500                                        0        100       200        300         400         500
                                                    Training steps                                                                         Training steps                                                                          Training steps                                                                                Training steps
                                                      AIME24                                                                                 AIME25                                                                                  Math500                                                                                           Minerva
                                                                                                                1.24                                                                                                                                                                                 1.6
                                       PPLπb (πb , D)                                                                         PPLπb (πb , D)                                                       1.250              PPLπb (πb , D)                                                                                  PPLπb (πb , D)
                         1.13                                                                                   1.22
                                       PPLπb (πb , D+ )                                                                       PPLπb (πb , D+ )                                                                        PPLπb (πb , D+ )                                                               1.5              PPLπb (πb , D+ )
                                                                                                                1.20                                                                               1.225
                         1.12
            Perplexity




                                                                                                   Perplexity




                                                                                                                                                                                     Perplexity




                                                                                                                                                                                                                                                                                        Perplexity




                                                                                                                                                                                                                                                                                                     1.4
                                                                                                                1.18                                                                               1.200
                         1.11
                                                                                                                1.16                                                                               1.175                                                                                             1.3
                         1.10                                                                                   1.14                                                                               1.150
                                                                                                                                                                                                                                                                                                     1.2
                                                                                                                1.12
                         1.09                                                                                                                                                                      1.125
                                                                                                                1.10                                                                                                                                                                                 1.1
                                0       100         200       300       400        500                                 0       100         200       300       400        500                                  0       100         200       300         400        500                                        0        100       200        300         400         500
                                                    Training steps                                                                         Training steps                                                                          Training steps                                                                                Training steps
                                                      AIME24                                                                                 AIME25                                                                                  Math500                                                                                           Minerva
                                                                                                                                                                                                   1.25                                                                                       1.25
                  1.175                                                                                  1.175
                                                                                                                                                                                                   1.20                                                                                       1.20
                  1.150                                                                                  1.150
     Perplexity




                                                                                            Perplexity




                                                                                                                                                                                      Perplexity




                                                                                                                                                                                                                                                                                 Perplexity




                                                                                                                                                                                                   1.15                                                                                       1.15
                  1.125                                                                                  1.125
                                                                                                                                                                                                                                                                                              1.10
                  1.100                                                                                  1.100                                                                                     1.10
                                                                                                                                                                                                                                                                                              1.05
                  1.075                                                                                  1.075                                                                                     1.05
                                                                                                                                                                                                                                                                                              1.00
                                                −                                                                                      −                                                                                       −
                                    PPLπb (πb , D )                           +
                                                                 PPLπb (πb , D )                                           PPLπb (πb , D )                           +
                                                                                                                                                        PPLπb (πb , D )                                            PPLπb (πb , D )                             +
                                                                                                                                                                                                                                                  PPLπb (πb , D )                                                  PPLπb (πb , D− )               PPLπb (πb , D+ )




Figure 14: Dynamics of Perplexity during RLVR. The first row shows that RLVR increasingly gen-
erates low-perplexity responses under the base model. The second row demonstrates that the initial
base solutions, regardless of correctness, exhibit increasing perplexity; the LMs are less likely to
generate initial, diverse solutions. The final row shows that for problems where the correct solution
already has a high probability to generate under base model, RLVR will incentivize, improving these
problems, while problems with low success rate exhibits performance degradation.



                                                                                                                                                                           22
Preprint




I                         A DDITIONAL DETAILS IN REDUCING PREVIOUSLY LEARNED BEHAVIORS IN
                          RLVR.
Similar to Shao et al. (2025), we define code reasoning are responses that contain the string
python. For each prompt x, the LMs policy can generate either code reasoning traces or lang
reasoning traces. We can define a mixture of distribuion between these two reasoning traces:


                                                              πb (y|x) = α(x)πcode (y|x) + (1 − α(x))πlang (y|x)                                                                                                                                             (35)
where α(x) is the mixture coefficient that depends on the prompt. For each prompt x, we sample
k = 144 responses to estimate the average accuracy of the mixture distributions πcode and πlang ,
denoted as ρcode (x) and ρlang (x). We then define their average accuracies on the test set Dtest as:
                                                                                      Ex∼Dtest [ρcode (x)] ,                               Ex∼Dtest [ρlang (x)] .                                                                                            (36)

We report results for each reasoning behavior in the Qwen2.5-Math models across all benchmarks
below:
                                         AIME24                                                          AIME25                                                         Math500                                                          Minerva
                                                                                                                                                    0.9
                               Code Frequency                                       0.8        Code Frequency                                                  Code Frequency                                                  Code Frequency
                                                                                                                                                    0.8
                    0.7        Lang Frequency                                                  Lang Frequency                                                  Lang Frequency                                       0.7        Lang Frequency
                                                                                    0.7
                                                                                                                                                    0.7
                    0.6                                                                                                                                                                                             0.6
                                                                                    0.6
        Frequency




                                                                    Frequency




                                                                                                                                    Frequency




                                                                                                                                                                                                    Frequency
                                                                                                                                                    0.6

                    0.5                                                             0.5                                                             0.5                                                             0.5


                                                                                    0.4                                                             0.4
                    0.4                                                                                                                                                                                             0.4
                                                                                                                                                    0.3
                                                                                    0.3
                    0.3                                                                                                                                                                                             0.3
                                                                                                                                                    0.2
                                                                                    0.2
                                                                                                                                                    0.1
                          0     100     200     300    400    500                         0     100     200     300    400    500                         0     100     200     300    400    500                         0     100     200     300    400    500
                                      Training steps                                                  Training steps                                                  Training steps                                                  Training steps
                                AIME24 Initial Accuracy                                         AIME25 Initial Accuracy                                        Math500 Initial Accuracy                                         Minerva Initial Accuracy
               10.00                                                                                                                                61                                                              19
                                                                                    10
                9.95
                                                                                                                                                                                                                    18
                                                                                                                                                    60
                9.90                                                                 8
Accuracy (%)




                                                                     Accuracy (%)




                                                                                                                                     Accuracy (%)




                                                                                                                                                                                                     Accuracy (%)   17
                                                                                                                                                    59
                9.85
                                                                                     6
                                                                                                                                                                                                                    16
                9.80
                                                                                                                                                    58
                                                                                     4                                                                                                                              15
                9.75
                                                                                                                                                    57
                                                                                                                                                                                                                    14
                9.70
                                                                                     2

                9.65                                                                                                                                56                                                              13
                              Code                     Lang                                   Code                     Lang                                   Code                     Lang                                   Code                     Lang



Figure 15: Reasoning strategy switching from code to lang throughout training process. While
AIME24/25 and Math500 exhibits initial better accuracy in lang than code, Minerva shows better
performance in code reasoning traces.


We observe that the models eventually switch almost entirely to lang reasoning traces. We hypoth-
esize that this shift explains the improvements on AIME24/25 and Math500, where lang reasoning
traces is more effective initially. However, the loss of code reasoning traces reduces performance
on Minerva, where the base model originally benefited from producing code reasoning traces.

J                         U SAGE OF L ARGE L ANGUAGE M ODELS (LLM S )
We used ChatGPT solely for revising the writing of the paper. Note that revision here strictly means
enhancing the clarity and readability of the text (e.g., fixing typos or constructing latex tables), and
not for any other purposes.




                                                                                                                              23
