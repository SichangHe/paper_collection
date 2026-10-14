                                                 Rethinking Fine-Tuning when Scaling Test-Time
                                                    Compute: Limiting Confidence Improves
                                                            Mathematical Reasoning


                                                       Feng Chen∗                    Allan Raventós*                      Nan Cheng
                                                   Stanford University              Stanford University              University of Michigan
arXiv:2502.07154v4 [cs.LG] 24 Nov 2025




                                                   Stanford, CA 94305               Stanford, CA 94305                Ann Arbor, MI 48109
                                                  fengc@stanford.edu             aravento@stanford.edu               nancheng@umich.edu

                                                                 Surya Ganguli                             Shaul Druckmann
                                                               Stanford University                         Stanford University
                                                               Stanford, CA 94305                          Stanford, CA 94305
                                                            sganguli@stanford.edu                        shauld@stanford.edu



                                                                                          Abstract

                                                      Recent progress in large language models (LLMs) highlights the power of scaling
                                                      test-time compute to achieve strong performance on complex tasks, such as mathe-
                                                      matical reasoning and code generation. This raises a critical question: how should
                                                      model training be modified to optimize performance under a subsequent test-time
                                                      compute strategy and budget? To explore this, we focus on pass@N, a simple
                                                      test-time strategy that searches for a correct answer in N independent samples. We
                                                      show, surprisingly, that training with cross-entropy (CE) loss can be misaligned
                                                      with pass@N in that pass@N accuracy decreases with longer training. We explain
                                                      the origins of this misalignment in terms of model overconfidence induced by CE,
                                                      and experimentally verify our prediction of overconfidence as an impediment to
                                                      scaling test-time compute via pass@N. Furthermore we suggest a principled, modi-
                                                      fied training loss that is better aligned to pass@N by limiting model confidence and
                                                      rescuing pass@N test performance. Our algorithm demonstrates improved math-
                                                      ematical reasoning on MATH and MiniF2F benchmarks under several scenarios:
                                                      (1) providing answers to math questions; and (2) proving theorems by searching
                                                      over proof trees of varying shapes. Overall our work underscores the importance of
                                                      co-designing two traditionally separate phases of LLM development: training-time
                                                      protocols and test-time search and reasoning strategies.


                                         1       Introduction

                                         Scaling test-time compute has been integral to unprecedented improvements in LLMs’ reasoning
                                         skills for complex tasks such as math and coding. Thus, test-time compute has emerged as a new
                                         dimension for improving LLMs, leading to a key tradeoff between allocating additional compute to
                                         inference versus pretraining [1]. Diverse test-time strategies include Chain-of-Thought (CoT) [2],
                                         tree-of-thought [3], self-consistency [4], self-reflection [5], self-critique [6], self-verification [7] and
                                         Monte-Carlo tree search [8]. These have shown great success in boosting model performance in the
                                         post-training phase or at inference time. More recently, OpenAI’s O1 model [9] and DeepSeek’s R1
                                         model [10] have combined some of these strategies with reinforcement learning to generate high-
                                             ∗
                                                 Equal Contribution


                                         39th Conference on Neural Information Processing Systems (NeurIPS 2025).
quality reasoning traces for problems of various difficulty levels, demonstrating clear performance
improvements as more test-time compute is allocated.
These successes fit into a broader paradigm in which a frontier model is first fine-tuned on a reasoning
task with supervised fine-tuning (SFT) [2, 11, 12], and then a test-time algorithm is applied to
model outputs or reasoning traces to improve performance [3, 4, 13]. Many test-time algorithms are
independent of the fine-tuning process. As a result, the fine-tuning is agnostic to and thus decoupled
from the test-time algorithm [14]. However, for a given choice of test-time strategy and compute
budget, it is not a priori clear which fine-tuning approach, including the loss objective, would be best
aligned with the test-time strategy so as to maximize the test accuracy under the overall strategy.
Our work studies the problem of aligning fine-tuning with test-time algorithms. We consider what
is perhaps the simplest setting, SFT with CE loss and pass@N as the test-time strategy. This
setting reveals a case of misalignment: standard SFT is not maximizing performance under pass@N.
We believe that this misalignment presents itself in several combinations of fine-tuning/test-time
approaches, motivating our thorough study in this paper. Our main contributions are,

       • We identify a misalignment between standard fine-tuning with CE loss and the pass@N
         coverage metric at test time (Section 4.1).
       • We develop and experimentally verify a framework that suggests this misalignment arises
         from overconfidence induced by training on CE loss (Sections 4.2 and 4.3).
       • We propose a loss function that directly optimizes the pass@N coverage metric, demon-
         strating consistent improvement over the CE loss objective and achieving superior accuracy
         frontiers on MATH and MiniF2F (Sections 5.1 to 5.3).
       • We extend our algorithm to more complex test-time scenarios including searching over
         proof-trees of varying shapes to improve automated theorem proving, and answering math
         questions using Chain-of-Thought reasoning traces, demonstrating improved mathematical
         reasoning in both cases (Sections 5.3 and 5.4).

2   Related Works
Test-time compute and pass@N strategy. A growing body of work explores how training and
test-time strategies interact to shape model performance. Jones [15] highlight a tradeoff between train
and test-time compute in a controlled board game setting. Brown et al. [16] identify an exponentiated
power law between coverage and number of in-context samples, captured phenomenologically in Levi
[17] and Schaeffer et al. [18], while Snell et al. [1] explore compute-optimal strategies for scaling
test-time inference. Our paper focuses primarily on the pass@N test-time strategy. Gui et al. [19]
show that, in the best-of-N setting, the sample distribution is well-aligned with the reward model, and
alignment methods have been proposed to distill this distribution and reduce sampling costs [19, 20].
However, their work focuses on improving the pass@1 performance from the Best-of-N policy, while
we focus on directly improving the pass@N performance. Closely related to our work, Chow et al.
[14] derives a similar training objective for reinforcement learning (RL) to directly optimize for
the best-of-N test-time strategy. Li et al. [21] argue that fine-tuning with cross-entropy loss limits
output diversity and propose a maximum entropy-based method to address this issue. Our work
similarly identifies limitations of cross-entropy when scaling test-time compute, but focuses on the
alignment of training and test-time strategies. In addition, Yue et al. [22] argue that fine-tuning with
Group Relative Policy Optimization (GRPO) does not improve reasoning capabilities beyond the
base model when evaluated with pass@N strategy. We will show that GRPO training may also lead
to overconfidence in Figure 3.
Post-training for mathematical reasoning. Various post-training techniques have been developed to
improve mathematical reasoning in LLMs. Instruction-tuning and reinforcement learning with human
feedback boost model performance on math tasks [23–25], while continued training on domain-
specific math or code data also boosts downstream reasoning [26–30]. Rejection-sampling [31]
and self-improvement [32] methods augment training data for SFT. Recent approaches [9, 10] have
incorporated RL to achieve exceptional reasoning capabilities. GRPO [10, 29] is a newly proposed
RL algorithm demonstrating strong improvements in mathematical reasoning. Several recent studies
have further addressed response length and problem difficulty biases [33], as well as conducted
extensive analyses of accuracy and response length across a wide variety of base models [33, 34].


                                                   2
While our primary focus is SFT, our loss function can be applied to other settings that train under CE
loss, such as continual training, instruction-tuning, and data augmentation.
Data pruning and hard example mining. The loss function we derive below can be viewed from the
lens of data pruning and hard example mining. Data selection is used to curate high-quality datasets
for pretraining [35], where Sorscher et al. [36] show that pruning easy samples can improve loss
scaling as a function of dataset size. Zhou et al. [37], Ye et al. [38] demonstrate that, in SFT, even
small datasets can yield strong alignment and reasoning performance. Hard example mining focuses
on identifying and emphasizing challenging samples to improve model performance [39]. In the
domain of mathematical reasoning, Tong et al. [40] find a difficulty imbalance in rejection-sampled
datasets and show that more extensive training on difficult samples improves model performance.

3     Problem setup
Given a vocabulary set W , we consider a dataset D = {(x(i) , y (i) )}M    i=1 , where x
                                                                                         (i)
                                                                                             ∈ W ni is a
          (i)       mi
prompt, y ∈ W is its ground-truth completion, and ni and mi are the prompt and completion
lengths. In the context of math, x(i) is the problem statement and y (i) is its solution. To model
the conditional distribution p(y (i) |x(i) ) we use an autoregressive transformer model [41], which is
traditionally trained by minimizing the cross-entropy loss
                                       LCE = − E log p̂(y|x)                                         (1)
                                                    (x,y)∼D

where p̂ denotes the model’s distribution.
To use and evaluate the model at test time, we assume the existence of an efficient oracle verifier
V which takes as input an (x, y) pair and returns V (x, y) = 1 if y is a correct completion of x and
0 otherwise. Practical examples of verifiers include compilers or pre-defined unit tests for coding
problems, or automatic proof checkers in mathematical theorem proving. In such applications, a
simple method, known as pass@N, for trading test-time compute for accuracy involves sampling
N completions from p̂ given the test prompt x and applying the verifier V to all of them to search
for a correct solution. The probability of a correct answer is then no longer the probability that 1
completion is correct, but rather the probability that at least one of N is correct. This probability, for
a dataset D, is given by the pass@N coverage metric
                         N
                        CD =           E           P(∃j ∈ [N ] s. t. V (x, yj ) = 1).                 (2)
                                       i.i.d.
                                x∼D,yi ∼ p̂(·|x)

                                                                                              1
Minimizing the CE loss in Equation (1) is equivalent to maximizing the pass@1 metric CD          on a
                                                                                N
training set D. But if we scale up test-time compute so that the pass@N metric CD on a test set D for
N ≫ 1 is the relevant performance metric, is LCE still a good training loss, or can we do better?

4     Misalignment between CE loss and pass@N
4.1   The CE loss induces overfitting for pass@N

To understand the impact of training with CE loss on pass@N test performance, we fine-tune
Llama-3-8B-base [42] on the MATH [43] dataset. We start from the base model rather than Llama-
3-8B-Instruct to avoid potential leakage of the MATH dataset into Llama-3-8B-Instruct through
post-training. We follow Lightman et al. [24] and use 12, 000 problems for training and the remaining
500 for testing. Here we train the model to provide a direct answer without a reasoning trace. We will
discuss training with CoT in Section 5.4. We confirm that the results presented in this section also
hold for a larger model, Llama-3-70B-base, and direct readers to Section C.3 for additional results.
                                                     N
Table 1 reveals that the pass@N performance CD          on a test set monotonically increases with the
                                                                                                       1
number of training epochs only for N = 1, when minimizing CE loss is equivalent to maximizing CD         .
                                                                                                    N
However, for N ≥ 16, minimizing CE loss during training does not monotonically increase CD at
test; indeed for N ≥ 256, pass@N test performance, remarkably, monotonically decreases with the
number of training epochs, despite the fact that pass@1 performance monotonically increases. This
effectively corresponds to a novel type of overfitting, in which test performance degrades over training,
likely due to a mismatch between the test time (pass@N) and training time (pass@1) strategies.


                                                        3
4.2   Overfitting, confidence, and explore-exploit tradeoff

What are the origins of this overfitting? First we show that in the simple case of a single problem
x, overfitting cannot occur. Let p̂(x) denote the probability assigned by the model to all correct
answers for problem x. Then the pass@1 coverage is C 1 = p̂(x) while the pass@N coverage is
C N = 1 − (1 − p̂(x))N = 1 − (1 − C 1 )N . This formula for C N in the single problem case obeys:
                                                       ′
Lemma 4.1. ∀N, N ′ > 0, C N is monotonic in C N .
Thus increasing pass@N′ coverage implies increasing pass@N coverage for any N and N ′ . When
N ′ = 1, this implies minimizing CE loss maximizes pass@N coverage.
However, Theorem 4.1 can fail when there is more than one problem. To understand this in a simple
setting, consider a test set with two problems x1 and x2 with unique correct answers y1 and y2 .
Consider two models. The first model assigns probabilities p̂1 (y1 |x1 ) = 1 and p̂1 (y2 |x2 ) = 0.
If we think of the probability a model assigns to an answer as its confidence in that answer, this
model is highly confident and correct for problem x1 , but highly confident and wrong for x2 .
Its pass@1 coverage is thus 50%. Moreover, since it always gets x1 right and x2 wrong, its
pass@N coverage remains at 50%. In contrast, consider a second model which assigns probabilities
p̂2 (y1 |x1 ) = p̂2 (y2 |x2 ) = 0.1. This model has high confidence (0.9) but unfortunately on incorrect
answers. Therefore its pass@1 accuracy is only 10%. However, it is willing to explore or hedge
by placing some low confidence (0.1) on the other answer, which happens to be correct. Thus if
this model samples N times, the pass@N coverage increases with N , eventually approaching 100%
as N → ∞. Thus the first model outperforms the second in terms of pass@1 but not pass@N for
large N . This indicates a tradeoff amongst policies: those that do better on pass@1 may not do
better at pass@N. Of course the best one can do is be confident and correct, corresponding to the
optimal model with p̂∗ (y1 |x1 ) = p̂∗ (y2 |x2 ) = 1. However, this toy example reveals that if one
cannot guarantee correctness, it can be beneficial to limit confidence and explore more solutions.
To demonstrate more generally the existence of tradeoffs between confident exploitation of a few
answers versus unconfident exploration of many answers, as a function of the number of passes N ,
we prove two lemmas. To set up these lemmas, given any problem, let p̂i denote the model probability
or confidence assigned to answer i, and assume answers are sorted from highest to lowest confidence
so that p̂i ≥ p̂i+1 , ∀ i ≥ 1. Thus p̂1 is the model’s maximal confidence across all answers. Moreover,
let pi be the probability across all the problems that the ith ranked answer is actually correct. Assume
the model policy is approximately well calibrated so that higher confidence implies higher or equal
probability of being correct, i.e. pi ≥ pi+1 , ∀ i ≥ 1. We empirically verify that the model trained
with CE loss on the MATH dataset approximately satisfies this assumption (Figure 13). Indeed,
optimal policies maximizing pass@N coverage in Equation (2) are approximately well calibrated
(See Theorem A.1). p1 is then the model’s maximal accuracy across all answers. We prove:
                                                                                              Pk
Lemma 4.2 (Upper bound on max confidence). Assume a max accuracy p1 , and assume i=1 pi ≥
1 − ϵ for some 0 < ϵ < 1 − p1 . Then optimal policies maximizing pass@N coverage in Equa-
tion (2), subject to the above accuracy and calibration constraints, have a confidence upper bound
u(N, p1 , ϵ, k), which is a non-increasing function of N .
We proved this upper bound as well as the proof in Section A. This upper bound is monotonically
decreasing in N (Figure 12), implying that at large N , an optimal policy for pass@N must limit its
max confidence to be low, thereby favoring exploration and discouraging exploitation. Furthermore,
we prove:


Table 1: Pass@N coverage on the MATH test set for a Llama-3-8B-base model fine-tuned with CE
loss on direct answers from the MATH training set. While pass@1 improves with continued training,
for large N , surprisingly, pass@N decreases with number of training epochs.
                                  pass@1     pass@16       pass@256    pass@4k
                      Epoch 1      4.4%       30.0%         65.2%         82.5%
                      Epoch 2      5.3%       31.4%         64.5%         80.0%
                      Epoch 3      6.5%       28.7%         54.5%         79.2%
                      Epoch 4      7.4%       22.9%         44.5%         63.0%



                                                   4
(a)                          (b)                         (c)                    (d)




Figure 1: A model trained with CE loss becomes overconfident in its greedy completions, which
harms its pass@N coverage; our proposed DCO objective limits this overconfidence. We fine-
tune a Llama-3-8B base model on the MATH dataset to produce direct answers. ŷgreedy is the model’s
greedy completion when choosing the most likely token at each sampling step. (a) The model trained
with CE loss assigns progressively larger confidences p̂(ŷgreedy |x) to its greedy completions over the
course of training. (b) At the end of training, only a small portion of the model’s highly confident
completions are correct. This will harm the model’s pass@N performance when scaling up N . (c)
Same as (a) but shown for the DCO loss with N ′ = 256. The model trained on DCO shows a
much milder overconfidence effect. (d) The confidence distribution of greedy completions after four
epochs with DCO for various choices of N ′ . As N ′ increases, the model’s confidence in its greedy
completion is more stringently limited, directly as a consequence of the overconfidence regularizer F .


Lemma 4.3 (Lower bound on max confidence). Assume top two accuracies p1 > p2 . Then optimal
policies maximizing pass@N coverage in Equation (2), subject to above accuracy and calibration
constraints, must have max confidence obeying

                                                               1     1
                                              (1 − p1 + p2 )p11−N p2N −1
                                 p̂∗1 ≥ 1 −                     1    N     .
                                              1 − p1 + p2 + p11−N p2N −1


This lower bound is a monotonically decreasing function of N (Figure 12), implying that at small
N , optimal policies must have high max confidence, thereby favoring exploitation and discouraging
exploration. Note in the limit N → 1+ , the lower bound is always 1, recovering the intuitive result
that the optimal policy for pass@1 is to place 100% confidence on the highest accuracy answer.


4.3   Overconfidence prevents performance gains from scaling test-time compute

Theorem 4.2 suggests that at large N it is beneficial to unconfidently explore by assigning low model
confidence to many answers, while Theorem 4.3 suggests that at small N it is beneficial to confidently
exploit by assigning high model confidence to one or a few answers. These lemmas make a prediction
that could explain the empirical observation in Table 1: namely, maximization of pass@1 makes the
model overconfident, thereby preventing good performance on pass@N.
To test this theoretical prediction of model overconfidence, we estimated the max confidence of the
model as p̂(ygreedy |x) where ygreedy is the greedy completion to x obtained by sampling autoregres-
sively from the model p̂, and at each step selecting the token with the highest probability. p̂(ygreedy |x)
approximates the max confidence p̂1 in Theorems 4.2 and 4.3. For the model fine-tuned on MATH
with CE loss, we plot the distribution of p̂(ygreedy |x) over the test set in Figure 1 (a). This demon-
strates the model becomes progressively more confident about its greedy completion over training,
thereby confirming our theoretical prediction. In Figure 1 (b) we see why this is a problem: only
some of the model’s highly confident answers are correct. Thus the model becomes overconfident
and largely wrong. Scaling test-time compute cannot easily rescue such a model, as over multiple
samples, it is likely to confidently provide the same wrong answers, explaining the origins of poor
pass@N test performance. In Section C.4, we observe a similar trend of overconfidence on the
out-of-distribution test set AIME24, further highlighting the generality of this failure mode.


                                                     5
5     Direct Coverage Optimization
5.1   A solution that naturally prevents overconfidence

The misalignment between CE training loss and pass@N coverage suggests a simple solution: directly
optimize pass@N coverage for each training example at training time, whenever the pass@N strategy
is to be used at test-time. We thus propose the Direct Coverage Optimization (DCO) objective,
LN                  N
  DCO = E(x,y)∼D ℓDCO (x, y), where
                               ℓN                                     N
                                                                        
                                DCO (x, y) = − log 1 − (1 − p̂(y|x))      ,                       (3)
is the − log probability that the model produces y at least once in N samples given x. Thus for each
prompt x and correct completion y in the training set, we maximize the probability y is found in N
passes. This loss naturally prevents model overconfidence, as can be seen via its gradient
                             ∇θ ℓNDCO (x, y) = F (N, p̂(y|x)) ∇θ ℓCE (x, y)                       (4)
                                                                                                N −1
where ℓCE is the standard CE loss on a single example, and F (N, p̂(y|x)) = N (1−        p̂(y|x))   p̂(y|x)
                                                                                       1−(1−p̂(y|x))N
is an extra overconfidence regularization factor that multiplies the standard CE gradient. Note that
F (N, p̂(y|x)) = 1 for N = 1, so DCO reduces to CE for pass@1. Furthermore F (N, p̂(y|x))
monotonically decreases in the model confidence p̂(y|x) (see Figure 2 (b)). Thus gradients for
examples (x, y) on which the model is more confident are attenuated, and this attenuation is stronger
for larger N . This justifies the interpretation of F (N, p̂(y|x)) as a regularizer that prevents model
overconfidence. Indeed, for large N , F (N, p̂(y|x)) ≈ 0 for confidence p̂(y|x) ≳ 1/N . As soon as
model confidence on an example exceeds 1/N , its gradient becomes negligible. Thus interestingly,
aligning training and test better through DCO naturally yields a simple emergent regularization of
model overconfidence, which was itself identified as an impediment to performance gains through
scaling test-time compute in Figure 1 (a). Indeed, F (N, p̂(y|x)) is smaller for easier examples
(Figure 14, right), effectively regularizing their contribution. This regularization mitigates the
potential detrimental effects of overconfidence from easy examples as discussed in Section C.1.
In practice, the introduction of F can lead to some samples in a batch contributing minimally to the
current gradient step. To maintain a stable effective batch size, we introduce a threshold ϵ, and if for
a given example, (x, y), F (N, p̂(y|x)) < ϵ, we replace the example with a new one.

5.2   DCO can prevent overconfidence and rescue test-time scaling

We next test whether DCO can rescue test-time scaling by preventing model overconfidence. We first
perform experiments on the MATH dataset in this section, and then in the next section we perform
experiments on the LeanDojo automated theorem proving benchmark [44]. We fine-tune Llama-3-8B
base model for 4 epochs on the MATH training set using DCO for N ′ = 256 and confirm that the
model is much less confident in its greedy completion than when trained with CE loss after multiple
epochs (compare Figure 1 (a) and (c)). Moreover, training with DCO at larger N yields lower model
greedy confidences at the end of training (Figure 1 (d)), consistent with Theorem 4.2.
                                                                                                        ′
We next assess pass@N test performance as a function of N for models trained by minimizing LN       DCO
for different values of N ′ (Figure 2 (a)). For any given N , there is an optimal N ′ for the training
         ′
loss LNDCO that maximizes pass@N test coverage, yielding a Pareto optimal performance frontier
(black curve) that is achieved when N ′ is close to N . In particular the model trained with CE loss
(equivalent to pass@1 maximization at training) performs poorly relative to the Pareto frontier at large
N (red curve below black at large N ). Conversely, models trained with DCO at large N ′ perform
poorly relative to the Pareto frontier for small N (green curves below black at small N ).
                                                                            ′
Together these results indicate that the alignment of the training loss LN
                                                                         DCO with the test time strategy
pass@N, with N ′ close to N , is crucial for obtaining Pareto optimal performance. Moreover, these
results once again confirm the tradeoff between exploration and exploitation, with good performance
using pass@N test-time strategies requiring high (low) exploration with low (high) confidence at
large (small) N .

5.3   Improved theorem proving via ensembled tree search through a modified step-wise DCO

To further test our method in realistic settings with a verifier, we conduct experiments in theorem
proving using an interactive proof assistant on the LeanDojo benchmark [44] extracted from the math


                                                    6
(a)                            (b)                       (c)
                                                               Small                         Large
                                                                Theorem        Proof State    Theorem
                                                                               Tactic Edge              Correct proof




Figure 2: (a) DCO improves on CE loss for pass@N test coverage over a broad range of N and
traces a Pareto-optimal frontier. We fine-tune Llama-3-8B base models on MATH to produce direct
                                                     ′
                                                                       ′
answers: one with CE loss and others using LN       DCO for various N (color-coded). Each curve shows
pass@N coverage for a single fine-tuned model. Note that no N ′ is optimal for all N . The black
curve is a Pareto-optimal performance frontier traced by the max of coverage curves for DCO over all
N ′ . (See Figure 6, which highlights N ′ = 256, and Figures 8 and 10 for Llama-3-70B and AIME24
results.) (b) DCO limits overconfidence by attenuating gradients for examples on which the
model is highly confident. We plot the confidence regularization factor F in Equation (4). For CE
loss (N = 1), F = 1 regardless of confidence p̂(y|x). For N > 1, F decreases with p̂(y|x) and drops
to zero around 1/N —once confidence on an example reaches O(1/N ), F vanishes, preventing it from
further increasing. (c) Inverse confidence Neff at training time controls search-tree exploration
shapes at test-time. We provide schematic proof search trees for models trained with DCOstep for
small (left) and large (right) Neff . Circles are proof states; edges are tactics; solid edges are explored,
while dashed edges are not. Small Neff yields a narrow search tree that may miss correct proofs
(red, dashed), while larger Neff expands the tree to include the correct proof. However, if the tree
                        k
becomes too wide (Neff     ≫ N for a k-step proof), sampling the correct path becomes unlikely and
pass@N coverage decreases as C N ≈ N/Neff       k
                                                  . Thus Neff , chosen at training time, is a powerful knob
to control the tradeoff between exploitation and exploration at test time.

library of LEAN4 [45]. In this task, at each step i of the proof, the model is prompted with the current
proof state x[i], and it outputs a proof tactic y[i] with a trainable model probability p̂(y[i]|x[i]). The
proof assistant takes the sampled tactic y[i], verifies whether it is a valid tactic, and if so, returns the
next proof state x[i + 1] after the tactic y[i] is applied. At test time this interactive process between
the model and the assistant continues until either: (1) it terminates in an invalid tactic; (2) hits a
maximal allowed search depth set by computational constraints; or (3) terminates in a successful
proof of the initial proof goal as verified by the proof assistant.
In our experiments, we use LEAN4 [46] as the formal proof language. We start from Qwen2.5-
Math-1.5B [28], and fine-tune it on the LeanDojo benchmark [44]. In contrast to solving math
problems above where the model first autoregressively generates an entire answer y according
to p̂(y|x) and then the entire y is verified for correctness, in theorem proving we must obtain
correct tactics y[i], as verified by the proof assistant, at every proof step i. A straightforward
application of DCO fine-tuning in this setting then involves replacing the model confidence p̂(y|x)
in Equation (3) on a single answer y, with the model confidence on an entire successful, complete
                                           Qk−1
k-step proof p̂(y[0], ..., y[k − 1]|x[0]) = i=0 p̂(y[i]|x[i]). Because of the chain rule, the DCO
gradient on a single proof has the same form as Equation (4) but with F (N, p̂(y|x)) replaced with
       Qk−1
F (N, i=0 p̂ (y[i]|x[i])). We naively applied this DCO fine-tuning method with N ′ = 4k and
evaluated the resulting model, as well as a base model trained with CE loss, on MiniF2F, using
pass@4k. CE loss achieves a proof success rate of 37.4%, while fine-tuning with DCO achieves a
38.7% success rate. Thus, a naive application of DCO to theorem proving by matching the parameter
N ′ in DCO to the parameter N in pass@N achieves only a modest improvement.
In theorem proving, since every single intermediate proof step tactic y[i] must be valid, it is natural to
consider a step-wise generalization of DCO. For example, at each step i, the model chooses a tactic
y[i] with confidence p̂(y[i]|x[i]). Our proposed step-wise DCO optimizes this single-step confidence
according to Equation (4) as before, except now the step-wise confidence regularizer is given by
F (Neff , p̂(y[i]|x[i])). Here one can think of Neff as a step-wise DCO hyperparameter that controls the
exploration width at every proof step. In essence, the confidence regularizer prevents the confidence
of any chosen tactic from becoming much higher than 1/Neff . Since the sum of the confidences
over all tactics at each step must be 1, this means that at test time, model exploration at each step
corresponds to searching on a search tree in which each proof state x[i] allows the exploration of


                                                     7
Table 2: Proof success rates on Mathlib and MiniF2F using pass@4k. DCOstep outperforms CE loss
(Neff = 1) on both datasets for well-chosen Neff . Ensembling models trained with different Neff
leverages complementary strengths, with substantial gains over CE at matched test-time compute.

      Neff    1 (CE loss)       4          8        16         32      Ensemble of         Neff = 1
                                                                        all Neff ’s    (5x test compute)
  Mathlib        55.6%        56.4%     56.1%     56.5%      55.8%        62.2%              57.0%
  MiniF2F        37.4%        39.0%     39.5%     37.0%      37.4%        43.6%              39.5%


approximately only Neff tactics. Thus using Neff in step-wise DCO during fine-tuning selects the
approximate branching factor Neff of the proof search tree at test time (see Figure 2 (c)).
                                                                                       −k
In particular, a valid (partial) proof of length k will have probability of order Neff    . Thus small Neff
limits the exploration at test time to a tree with small branching factor, but allows longer proofs with
larger numbers of steps k to have higher sampling probability. This limited width search strategy
should work well at test time using pass@N as long as two conditions hold: (1) a successful proof of
length k is present in the search tree of branching factor Neff ; and (2) the N in pass@N at test time
                                                       −k
is large enough that this proof of probability O(Neff     ) is selected with high probability in N passes
                                             k
(which starts to occur as soon as N ≳ Neff ). Conversely, larger Neff allows for more exploration at
test time using a wider search tree of larger branching factor, but it makes finding longer proofs with
                                                                                      k
large k harder, since the approximate success condition for pass@N of N > Neff          is harder to satisfy
at fixed N and large Neff and k. However, this wide exploration strategy can work well for short
proofs with small k if a successful short proof does not lie in the limited width search tree obtained at
small Neff , but does lie in a wider search tree at larger Neff (Figure 2, (c) right).
The mean and median lengths of the proofs in the training set are 4.2 and 2, respectively. Thus we
explore fine-tuning with the step-wise DCO algorithm, DCOstep , with Neff ranging from 1 (CE loss)
to Neff = 32. We evaluate pass@4k performance on the Mathlib and MiniF2F test sets and find that
larger Neff improves accuracy over the CE baseline (Table 2). Interestingly, the optimal Neff increases
with more passes at test time (Table 6), similar to the Pareto frontier in Figure 2 (a). Since different
choices of Neff correspond to different search strategies at test time—larger Neff favors short proofs in
wide trees, smaller Neff favors long proofs in narrow trees— we hypothesized that ensembling these
methods could significantly boost performance. This was indeed the case (ensemble entry in Table 2).
The ensemble strategy samples 5 × 4k times, so a proper baseline is CE loss with the same test-time
compute of pass@N with N = 20k. The ensemble strategy outperforms this stringent baseline with
significant excesses of 5.2% on Mathlib and 4.1% on MiniF2F.
These results indicate that varying Neff in DCOstep at training time allows a diversity of tree search
strategies trading depth and breadth that can be exploited by scaling test-time compute via pass@N.

5.4    Approximate DCO also improves performance with chain-of-thought reasoning

In Section 5.2, the model is trained to directly give an answer y to a problem x. In this case, one can
implement DCO at training time by explicitly computing the model confidence p̂(y|x) and using it in
Equation (4). However, in a Chain-of-Thought (CoT) training paradigm, the training data consists of
triplets (x, c, y) where x and y are the problem and answer as before, but now c is a CoT reasoning
trace that explains how to derive y from x. The model is trained on the triplet (x, c, y), and at test
time, given a new problem x′ , it generates a reasoning trace c′ followed by an answer y ′ . Importantly,
the model is evaluated on whether its answer y ′ is correct independent of its reasoning trace c′ .
Thus, to estimate the probability p̂(y|x) that the model assigns to any answer y, one can no longer
compute it directly as in the direct P
                                     answer case. Instead, one must marginalize over all possible rea-
soning traces c to obtain p̂(y|x) = c p̂(y, c|x). Exact marginalization is intractable, so we replace
the marginalization with a Monte Carlo estimate of p̂(y|x), which we insert into the overconfidence
regularization factor F in Equation (4). We call this algorithm approximate DCO, denoted by DCOa .
We also compute Monte Carlo estimates of the probability the model assigns to its most likely final
answer, p̂(y mode |x), as a proxy for the model’s max confidence. Note that in the CoT setting the
greedy answer would correspond to a single most likely reasoning trace, but we want the probability
of the most likely final answer marginalizing over all reasoning traces.


                                                     8
(a)                        (b)                          (c)                       (d)




Figure 3: (a, b) Overconfidence persists in CoT fine-tuning with CE loss. We fine-tune a Llama-3-
8B base model on CoT traces in the MATH dataset and plot the distribution of the estimated model
confidences p̂(y mode |x) over samples in the test set at various points in training. (a) For CE loss, the
model becomes more confident in its most likely answers as training progresses—the confidence
distribution shifts to the right. This effect is milder than in the direct answer setting (Figure 1). (b)
DCOa limits this shift of the confidence distribution over training. (c, d) Overconfidence is also
present in GRPO fine-tuning and can result in a model that is overconfident and wrong. (c) The
model trained with GRPO assigns progressively larger confidences to p̂(y mode |x) over the course of
training. (d) At the end of training, only a small portion of the model’s highly confident completions
are correct, which will harm the model’s pass@N performance when scaling up N .

Table 3: Pass@N coverage on MATH (± indicates standard error of the mean). We fine-tune Llama-
3-8B-base on CoT traces. Training with DCOa using N ′ = 64 underperforms CE loss for pass@1,
but outperforms it for higher N , with the largest improvement when N ′ = N . The GRPO model has
the strongest pass@1 performance, but its performance degrades at larger N due to overconfidence.

                      Epoch 1                           Epoch 3                         Epoch 5
                                       a                              a
 Pass@N        CE      GRPO       DCO         CE        GRPO      DCO        CE         GRPO      DCOa
 Pass@1 4.3±0.1 3.0±0.1 5.0±0.1 9.0±0.1 12.6±0.6 8.3±0.1 9.9±0.1 14.6±0.1 7.8±0.1
 Pass@16 30.2±0.7 27.1±0.7 34.2±0.6 41.6±0.4 35.8±0.3 42.6±0.6 40.9±0.4 29.2±0.2 42.8±0.5
 Pass@64 51.2±1.2 50.6±0.7 55.3±1.0 61.7±0.4 46.3±0.4 63.1±0.8 60.9±0.6 35.4±0.3 64.3±0.6

We conduct experiments on the MATH dataset. As a baseline, we first fine-tune a Llama-3-8B-base
model using CE loss on the golden CoT solutions. We find in Table 3 that pass@1 coverage robustly
improves over the course of CE loss training. Intriguingly, in the CoT setting, overfitting induced by
the misalignment of CE loss at training time with the pass@N strategy at test time, appears less severe
compare with the direct answer setting (cf. Table 1). Nevertheless, we still find a clear increase in the
model’s max confidence through training (Figure 3 (a)). In contrast, training with DCOa mitigates the
rise in the model’s max confidence (Figure 3 (b)). As with the direct answer setup, model trained with
DCOa (N ′ = 64) exhibits lower pass@1 performance compared to the CE baseline but demonstrates
superior performance when evaluated with pass@N for larger N values (Table 3).
To provide a comprehensive comparison, we also evaluate a model trained with reinforcement
learning. Specifically, we use GRPO [29] to train the base model with the r1 [10] prompt template.
Interestingly, we observe that the GRPO-trained model exhibits pronounced overconfidence (Figure 3
(c)), yet only a small portion of the model’s highly confident answers are correct (Figure 3 (d)). This
negatively impacts the model’s pass@N performance when scaling up N (Table 3). Although GRPO
demonstrates superior pass@1 performance, the model trained with DCOa achieves a significantly
stronger performance when evaluated with pass@N for larger N values (Table 3).
Overall these results once again validate our theory and algorithmic approaches, now in a CoT
reasoning setting. In essence, improved performance by scaling test time compute via a pass@N
strategy at large N can be best obtained by aligning the training strategy via choosing DCOa with the
same N , and the origin of the performance improvement comes from limiting model overconfidence.

6     Discussion
In summary, all our results suggest the need for a tight co-design of two traditionally separate phases
of LLM development: (1) model training or fine-tuning and (2) test-time search/reasoning strategies


                                                    9
and budget. If the former is misaligned with the latter, then more training can actually impair
performance gains from scaling test-time compute. But if they are properly co-designed, end-to-end
training and test time performance can be far more effective. We have shown how to modify standard
cross-entropy loss for training to be better aligned to a pass@N strategy for large N at test-time.
Moreover, we have suggested and empirically confirmed why this co-design of training loss and
pass@N strategy is essential, because optimal policies for pass@N at large N should unconfidently
explore while the optimal policies for pass@N at small N should confidently exploit.
Limitations. Our study primarily investigates SFT with the pass@N test-time strategy for its
simplicity. However, this strategy requires a verifier, restricting its applicability to problems where
verification is feasible. Extending our findings to other test-time strategies, such as best-of-N, is an
important direction for future research. Additionally, while we have noted similar overconfidence
phenomena in GRPO, a more comprehensive study of RL methods is beyond the current scope.
Lastly, our work only focuses on mathematical reasoning; generalizing our findings to other domains,
such as coding tasks where unit tests serve as natural verifiers, is left for future work.

Acknowledgments and Disclosure of Funding
We would like to thank Zhinan Cheng, Clémentine Dominé, Marco Fumero, David Klindt, Daniel
Kunin, Ben Sorscher and Atsushi Yamamura for helpful discussions. S.G. thanks the James S.
McDonnell Foundation, Simons Foundation, NTT Research, Schmidt Foundation and an NSF
CAREER Award for support. S.D. and F.C. were partially supported by the McKnight Foundation,
the Simons Foundation and an NIH CRCNS grant R01DC020874. We are also grateful to Adam
Ousherovitch and Hongda Yuan for identifying an error in Theorem 4.2, which has been corrected in
the revised version of this paper.

References
 [1] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute
     optimally can be more effective than scaling model parameters, 2024. URL https://arxiv.
     org/abs/2408.03314.
 [2] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi,
     Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language
     models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors,
     Advances in Neural Information Processing Systems, volume 35, pages 24824–24837. Curran
     Associates, Inc., 2022.
 [3] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik
     Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. In
     A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, Advances in
     Neural Information Processing Systems, volume 36, pages 11809–11822. Curran Associates,
     Inc., 2023.
 [4] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha
     Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
     models. In The Eleventh International Conference on Learning Representations, 2023. URL
     https://openreview.net/forum?id=1PL1NIMMrw.
 [5] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflex-
     ion: language agents with verbal reinforcement learning. In A. Oh, T. Naumann, A. Globerson,
     K. Saenko, M. Hardt, and S. Levine, editors, Advances in Neural Information Processing
     Systems, volume 36, pages 8634–8652. Curran Associates, Inc., 2023.
 [6] William Saunders, Catherine Yeh, Jeff Wu, Steven Bills, Long Ouyang, Jonathan Ward, and Jan
     Leike. Self-critiquing models for assisting human evaluators. CoRR, abs/2206.05802, 2022.
     URL https://doi.org/10.48550/arXiv.2206.05802.
 [7] Yixuan Weng, Minjun Zhu, Fei Xia, Bin Li, Shizhu He, Shengping Liu, Bin Sun, Kang
     Liu, and Jun Zhao. Large language models are better reasoners with self-verification. In


                                                  10
     The 2023 Conference on Empirical Methods in Natural Language Processing, 2023. URL
     https://openreview.net/forum?id=s4xIeYimGQ.

 [8] Zirui Zhao, Wee Sun Lee, and David Hsu. Large language models as commonsense knowledge
     for large-scale task planning. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt,
     and S. Levine, editors, Advances in Neural Information Processing Systems, volume 36, pages
     31967–31987. Curran Associates, Inc., 2023.

 [9] OpenAI. Learning to reason with llms, 2024.          URL https://openai.com/index/
     learning-to-reason-with-llms/.

[10] Haowei Zhang DeepSeek-AI: Daya Guo, Dejian Yang et al. Deepseek-r1: Incentivizing
     reasoning capability in llms via reinforcement learning, 2025. URL https://arxiv.org/
     abs/2501.12948.

[11] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin,
     Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton,
     Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F Christiano,
     Jan Leike, and Ryan Lowe. Training language models to follow instructions with human
     feedback. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors,
     Advances in Neural Information Processing Systems, volume 35, pages 27730–27744. Curran
     Associates, Inc., 2022. URL https://proceedings.neurips.cc/paper_files/paper/
     2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf.

[12] Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan
     Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, Albert Webson, Shixiang Shane
     Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha Chowdhery, Alex Castro-Ros,
     Marie Pellat, Kevin Robinson, Dasha Valter, Sharan Narang, Gaurav Mishra, Adams Yu,
     Vincent Zhao, Yanping Huang, Andrew Dai, Hongkun Yu, Slav Petrov, Ed H. Chi, Jeff Dean,
     Jacob Devlin, Adam Roberts, Denny Zhou, Quoc V. Le, and Jason Wei. Scaling instruction-
     finetuned language models. Journal of Machine Learning Research, 25(70):1–53, 2024. URL
     http://jmlr.org/papers/v25/23-0870.html.

[13] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto,
     Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul
     Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke
     Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad
     Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias
     Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex
     Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
     William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant
     Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie
     Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and
     Wojciech Zaremba. Evaluating large language models trained on code, 2021. URL https:
     //arxiv.org/abs/2107.03374.

[14] Yinlam Chow, Guy Tennenholtz, Izzeddin Gur, Vincent Zhuang, Bo Dai, Aviral Kumar, Rishabh
     Agarwal, Sridhar Thiagarajan, Craig Boutilier, and Aleksandra Faust. Inference-aware fine-
     tuning for best-of-n sampling in large language models. In The Thirteenth International
     Conference on Learning Representations, 2025. URL https://openreview.net/forum?
     id=77gQUdQhE7.

[15] Andy L. Jones. Scaling scaling laws with board games, 2021. URL https://arxiv.org/
     abs/2104.03113.

[16] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré,
     and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated
     sampling, 2024. URL https://arxiv.org/abs/2407.21787.

[17] Noam Levi. A simple model of inference scaling laws, 2024. URL https://arxiv.org/
     abs/2410.16377.


                                               11
[18] Rylan Schaeffer, Joshua Kazdan, John Hughes, Jordan Juravsky, Sara Price, Aengus Lynch, Erik
     Jones, Robert Kirk, Azalia Mirhoseini, and Sanmi Koyejo. How do large language monkeys get
     their power (laws)?, 2025. URL https://arxiv.org/abs/2502.17578.
[19] Lin Gui, Cristina Gârbacea, and Victor Veitch. Bonbon alignment for large language
     models and the sweetness of best-of-n sampling. In A. Globerson, L. Mackey, D. Bel-
     grave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neu-
     ral Information Processing Systems, volume 37, pages 2851–2885. Curran Associates,
     Inc., 2024. URL https://proceedings.neurips.cc/paper_files/paper/2024/file/
     056521a35eacd9d2127b66a7d3c499c5-Paper-Conference.pdf.
[20] Pier Giuseppe Sessa, Robert Dadashi-Tazehozi, Leonard Hussenot, Johan Ferret, Nino Vieillard,
     Alexandre Rame, Bobak Shahriari, Sarah Perrin, Abram L. Friesen, Geoffrey Cideron, Sertan
     Girgin, Piotr Stanczyk, Andrea Michi, Danila Sinopalnikov, Sabela Ramos Garea, Amélie
     Héliou, Aliaksei Severyn, Matthew Hoffman, Nikola Momchev, and Olivier Bachem. BOND:
     Aligning LLMs with best-of-n distillation. In The Thirteenth International Conference on
     Learning Representations, 2025. URL https://openreview.net/forum?id=0tAXMiSufG.
[21] Ziniu Li, Congliang Chen, Tian Xu, Zeyu Qin, Jiancong Xiao, Ruoyu Sun, and Zhi-Quan Luo.
     Entropic distribution matching in supervised fine-tuning of llms: Less overfitting and better
     diversity. CoRR, abs/2408.16673, 2024. URL https://doi.org/10.48550/arXiv.2408.
     16673.
[22] Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao
     Huang. Does reinforcement learning really incentivize reasoning capacity in llms beyond the
     base model?, 2025. URL https://arxiv.org/abs/2504.13837.
[23] Xiang Yue, Xingwei Qu, Ge Zhang, Yao Fu, Wenhao Huang, Huan Sun, Yu Su, and Wenhu
     Chen. MAmmoTH: Building math generalist models through hybrid instruction tuning. In
     The Twelfth International Conference on Learning Representations, 2024. URL https://
     openreview.net/forum?id=yLClGs770I.
[24] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy
     Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step.
     In The Twelfth International Conference on Learning Representations, 2024. URL https:
     //openreview.net/forum?id=v8L0pN6EOi.
[25] Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang,
     Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with
     process- and outcome-based feedback, 2022. URL https://arxiv.org/abs/2211.14275.
[26] Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay
     Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu, Behnam
     Neyshabur, Guy Gur-Ari, and Vedant Misra. Solving quantitative reasoning problems with
     language models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh,
     editors, Advances in Neural Information Processing Systems, volume 35, pages 3843–3857.
     Curran Associates, Inc., 2022.
[27] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen Marcus
     McAleer, Albert Q. Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An
     open language model for mathematics. In The Twelfth International Conference on Learning
     Representations, 2024. URL https://openreview.net/forum?id=4WnqRR915j.
[28] An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu,
     Jianhong Tu, Jingren Zhou, Junyang Lin, Keming Lu, Mingfeng Xue, Runji Lin, Tianyu Liu,
     Xingzhang Ren, and Zhenru Zhang. Qwen2.5-math technical report: Toward mathematical
     expert model via self-improvement, 2024. URL https://arxiv.org/abs/2409.12122.
[29] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
     Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of
     mathematical reasoning in open language models, 2024. URL https://arxiv.org/abs/
     2402.03300.


                                               12
[30] Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou, Yunfan Shao, Zhaoye Fei, Yichuan Ma,
     Jiawei Hong, Kuikun Liu, Ziyi Wang, Yudong Wang, Zijian Wu, Shuaibin Li, Fengzhe Zhou,
     Hongwei Liu, Songyang Zhang, Wenwei Zhang, Hang Yan, Xipeng Qiu, Jiayu Wang, Kai Chen,
     and Dahua Lin. Internlm-math: Open math large language models toward verifiable reasoning.
     CoRR, abs/2402.06332, 2024. URL https://doi.org/10.48550/arXiv.2402.06332.
[31] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. Star: Bootstrapping reasoning with
     reasoning. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors,
     Advances in Neural Information Processing Systems, volume 35, pages 15476–15488. Curran
     Associates, Inc., 2022.
[32] Zhenting Qi, Mingyuan MA, Jiahang Xu, Li Lyna Zhang, Fan Yang, and Mao Yang. Mutual
     reasoning makes smaller LLMs stronger problem-solver. In The Thirteenth International
     Conference on Learning Representations, 2025. URL https://openreview.net/forum?
     id=6aHUmotXaw.
[33] Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee,
     and Min Lin. Understanding r1-zero-like training: A critical perspective, 2025. URL https:
     //arxiv.org/abs/2503.20783.
[34] Weihao Zeng, Yuzhen Huang, Qian Liu, Wei Liu, Keqing He, Zejun Ma, and Junxian He.
     Simplerl-zoo: Investigating and taming zero reinforcement learning for open base models in the
     wild, 2025. URL https://arxiv.org/abs/2503.18892.
[35] Max Marion, Ahmet Üstün, Luiza Pozzobon, Alex Wang, Marzieh Fadaee, and Sara
     Hooker. When less is more: Investigating data pruning for pretraining llms at scale. CoRR,
     abs/2309.04564, 2023. URL https://doi.org/10.48550/arXiv.2309.04564.
[36] Ben Sorscher, Robert Geirhos, Shashank Shekhar, Surya Ganguli, and Ari Morcos. Beyond
     neural scaling laws: beating power law scaling via data pruning. In S. Koyejo, S. Mohamed,
     A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Process-
     ing Systems, volume 35, pages 19523–19536. Curran Associates, Inc., 2022.
[37] Chunting Zhou, Pengfei Liu, Puxin Xu, Srinivasan Iyer, Jiao Sun, Yuning Mao, Xuezhe
     Ma, Avia Efrat, Ping Yu, LILI YU, Susan Zhang, Gargi Ghosh, Mike Lewis, Luke
     Zettlemoyer, and Omer Levy. Lima: Less is more for alignment. In A. Oh, T. Nau-
     mann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, Advances in Neu-
     ral Information Processing Systems, volume 36, pages 55006–55021. Curran Associates,
     Inc., 2023. URL https://proceedings.neurips.cc/paper_files/paper/2023/file/
     ac662d74829e4407ce1d126477f4a03a-Paper-Conference.pdf.
[38] Yixin Ye, Zhen Huang, Yang Xiao, Ethan Chern, Shijie Xia, and Pengfei Liu. Limo: Less is
     more for reasoning, 2025. URL https://arxiv.org/abs/2502.03387.
[39] Abhinav Shrivastava, Abhinav Gupta, and Ross Girshick. Training region-based object detectors
     with online hard example mining. In Proceedings of the IEEE Conference on Computer Vision
     and Pattern Recognition (CVPR), June 2016.
[40] Yuxuan Tong, Xiwen Zhang, Rui Wang, Ruidong Wu, and Junxian He. DART-math: Difficulty-
     aware rejection tuning for mathematical problem-solving. In The Thirty-eighth Annual Con-
     ference on Neural Information Processing Systems, 2024. URL https://openreview.net/
     forum?id=zLU21oQjD5.
[41] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N
     Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In I. Guyon,
     U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, ed-
     itors, Advances in Neural Information Processing Systems, volume 30. Curran Associates,
     Inc., 2017. URL https://proceedings.neurips.cc/paper_files/paper/2017/file/
     3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf.
[42] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, et al. The llama 3 herd
     of models, 2024. URL https://arxiv.org/abs/2407.21783.


                                                13
[43] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset.
     In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks
     Track (Round 2), 2021. URL https://openreview.net/forum?id=7Bywt2mQsCe.
[44] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
     Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-
     augmented language models. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt,
     and S. Levine, editors, Advances in Neural Information Processing Systems, volume 36, pages
     21573–21612. Curran Associates, Inc., 2023.
[45] The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, POPL ’20. ACM, Jan-
     uary 2020. doi: 10.1145/3372885.3373824. URL http://dx.doi.org/10.1145/3372885.
     3373824.
[46] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language. In André Platzer and Geoff Sutcliffe, editors, Automated Deduction – CADE 28,
     pages 625–635, Cham, 2021. Springer International Publishing. ISBN 978-3-030-79876-5.
[47] Jason Ansel, Edward Yang, Horace He, Natalia Gimelshein, Animesh Jain, Michael Voznesen-
     sky, Bin Bao, Peter Bell, David Berard, Evgeni Burovski, Geeta Chauhan, Anjali Chourdia, Will
     Constable, Alban Desmaison, Zachary DeVito, Elias Ellison, Will Feng, Jiong Gong, Michael
     Gschwind, Brian Hirsh, Sherlock Huang, Kshiteej Kalambarkar, Laurent Kirsch, Michael Lazos,
     Mario Lezcano, Yanbo Liang, Jason Liang, Yinghai Lu, CK Luk, Bert Maher, Yunjie Pan,
     Christian Puhrsch, Matthias Reso, Mark Saroufim, Marcos Yukio Siraichi, Helen Suk, Michael
     Suo, Phil Tillet, Eikan Wang, Xiaodong Wang, William Wen, Shunting Zhang, Xu Zhao, Keren
     Zhou, Richard Zou, Ajit Mathews, Gregory Chanan, Peng Wu, and Soumith Chintala. PyTorch
     2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph
     Compilation. In 29th ACM International Conference on Architectural Support for Program-
     ming Languages and Operating Systems, Volume 2 (ASPLOS ’24). ACM, April 2024. doi:
     10.1145/3620665.3640366. URL https://pytorch.org/assets/pytorch2-2.pdf.
[48] Sylvain Gugger, Lysandre Debut, Thomas Wolf, Philipp Schmid, Zachary Mueller, Sourab
     Mangrulkar, Marc Sun, and Benjamin Bossan. Accelerate: Training and inference at scale made
     simple, efficient and adaptable. https://github.com/huggingface/accelerate, 2022.
[49] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu,
     Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language
     model serving with pagedattention. In Proceedings of the 29th Symposium on Operating
     Systems Principles, SOSP ’23, page 611–626, New York, NY, USA, 2023. Association for
     Computing Machinery. ISBN 9798400702297. doi: 10.1145/3600006.3613165. URL https:
     //doi.org/10.1145/3600006.3613165.
[50] Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollar. Focal loss for dense
     object detection. In Proceedings of the IEEE International Conference on Computer Vision
     (ICCV), Oct 2017.
[51] Thomas Anthony, Zheng Tian, and David Barber. Thinking fast and slow with deep learning and
     tree search. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan,
     and R. Garnett, editors, Advances in Neural Information Processing Systems, volume 30. Curran
     Associates, Inc., 2017. URL https://proceedings.neurips.cc/paper_files/paper/
     2017/file/d8e1344e27a5b08cdfd5d027d9b8d6de-Paper.pdf.
[52] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
     Sutskever. Formal mathematics statement curriculum learning. In The Eleventh International
     Conference on Learning Representations, 2023. URL https://openreview.net/forum?
     id=-P7G-8dmSh4.




                                               14
A     Proofs
A.1      Proof of approximately well calibration under optimal policy

Lemma A.1. Given any problem, let p̂i denote the model probability or confidence assigned to answer
i, and assume answers are sorted from highest to lowest confidence so that p̂i ≥ p̂i+1 , ∀ i ≥ 1. Let pi
be the probability that answer i is actually correct across all the problems. Then optimal policies
maximizing pass@N coverage in Equation (2) (denoted by p̂∗i ) is approximately well calibrated, i. e.
higher confidence implies higher or equal probability of being correct, i.e. pi ≥ pi+1 , ∀ i ≥ 1.

Proof. Let R be the total number of answers the model can generate. Here R could possibly equal
infinity. Let p̂∗i denote the model probability or confidence assigned to answer i under optimal policy
maximizing pass@N coverage in Equation (2). Let Ai be the event that the ith ranked answer is not
chosen in the N passes and Bi be the event that ith ranked answer is chosen in the N passes. Let 1Bi
be the indicator function of Bi . Then, given an event ω, the probability of getting the correct answer
   PR
is i=1 pi 1Bi (ω). Hence, the expected probability of getting the correct answer is
       R
                   !     R              R                        R                  R
      X                 X               X                       X                  X
  E        pi 1Bi =         pi P(Bi ) =    pi (1−P(Ai )) = 1−       pi P(Ai ) = 1−     pi (1−p̂∗i )N , (5)
       i=1                 i=1                   i=1                          i=1   i=1
                                                                   ∗          ∗
If the current strategy is already optimal, any small change of (p̂1 , ..., p̂R ) would not increase the
expected probability of getting the correct answer. Now suppose we don’t always have pi ≥ pi+1 , in
other words, pj < pj+1 for some j ≥ 1. If p̂∗j < p̂∗j+1 , we have
                                 j−1
      R
                      !                                   R
      X                          X                        X
 E           pi 1Bi       < 1−         pi (1− p̂∗i )N −           pi (1− p̂∗i )N −pj+1 (1− p̂∗j )N −pj (1− p̂∗j+1 )N , (6)
       i=1                       i=1                      i=j+1

where the last inequality says that we can increase the expected probability of getting the correct an-
swer by swapping the confidence on answer originally labeled as j and j + 1, which is a contradiction.
If p̂∗j = p̂∗j+1 , then for all δ > 0 sufficiently small, we always have
                            j−1
        R
                   !                              R
       X                    X                     X
E         pi 1Bi < 1−            pi (1− p̂∗i )N −    pi (1− p̂∗i )N −pj (1− p̂∗j −δ)N −pj+1 (1− p̂∗j+1 +δ)N ,
      i=1                    i=1                       i=j+1
                                                                                                                      (7)
which also contradict with the current policy being optimal.

A.2      Proof of Lemma 4.2

Assuming p1 is known, an upper bound on p̂∗1 is given by,
                                                  ( k                  )!
                                                    X
                        u = max π1 argmin               pi (1 − p̂i )N
                                          {ps }k
                                               s=1        {p̂i }k
                                                                i=1    i=1
                                                                                                                      (8)
                                          k
                                          X
                                   s.t.         ps = 1 − ϵ, p1 ≥ p2 ... ≥ pk > 0.
                                          s=1

Suppose {pi }ki=1 solves Equation (8), and let {p̂∗i }ki=1 be the optimizer of
                        Xk                       k
                                                 X
                 argmin{   pi (1 − p̂i )N } s.t.   p̂s = 1, 1 ≥ p̂1 ≥ 0, ..., 1 ≥ p̂k ≥ 0.                            (9)
              {p̂i }k
                    i=1 i=1                    s=1
By definition, u = p̂∗1 . Since p1 ≥ p2 ... ≥ pk , we also have p̂∗1 ≥ p̂∗2 ... ≥ p̂∗k . There are k possible
cases.
       1) p̂∗1 = 1 and p̂∗s = 0 for all s ≥ 2.
       j) p̂∗j > 0 but p̂∗j+1 = 0. For 2 ≤ j ≤ k − 1. There are k − 2 cases.
       k) p̂∗k > 0.
We now characterize when each case can occur and derive an upper bound in each case.


                                                                  15
A.2.1   Case k
Lemma A.2. If p̂∗k > 0, then p1 = p2 = ... = pk−1 .

Proof. In this case, we have
                                    (k − 1)p−α                 (k − 1)p−α
                         p̂∗k = 1 − Pk       k
                                            −α
                                               > 0, p̂∗1 = 1 − Pk       1
                                                                       −α
                                                                          .                            (10)
                                       s=1 ps                     s=1 ps

where α = N 1−1 . Suppose, for contradiction, that p1 > pk−1 . We construct a perturbed configuration
{qi }ki=1 such that the corresponding optimizer {q̂i∗ }ki=1 satisfies q̂1∗ > p̂∗1 . Choose a small δ > 0 and
define
          q1 = p1 ,       ...      , qk−2 = pk−2 ,        qk−1 = pk−1 + δ,         qk = pk − δ.
For δ > 0 sufficiently small, we still have q̂k∗ > 0 (by continuity), and moreover q̂1∗ > p̂∗1 , contradict-
ing the optimality of the original configuration {pi }ki=1 . Hence, p1 = p2 = · · · = pk−1 .

By Lemma A.2, we have
                 (k − 1)p1 + pk = 1 − ϵ, (k − 1)p−α
                                                 1  > (k − 2)p−α
                                                              k , p1 ≥ pk > 0.                         (11)
This implies the following range for p1 in Case k:
                               1−ϵ                    1−ϵ
                                      ≤ p1 <                 N −1 .                                   (12)
                                  k
                                                       
                                               k − 1 + k−2
                                                         k−1

Under condition Equation (12), we have
                                                 (k − 1)p−α
                                                          1
                            u=1−                                          .                            (13)
                                      (k − 1)p−α
                                              1  + (1 + p1  − ϵ − kp1 )−α
Moreover, the right hand side of Equation (13) is an increasing function of p1 .

A.2.2   Case j
Lemma A.3. If p̂∗j > 0 but p̂∗j+1 = 0 for some 2 ≤ j ≤ k − 1, then p1 = ... = pj−1 and
pj+1 = ... = pk > 0.

Proof. We proceed in three steps.
Step 1: we prove pk > 0. Suppose, by contradiction, pk = 0. Let s > 2 be the smallest index such
that ps = · · · = pk = 0. If s > j, change pj to pj − δ, pj+1 to δ for some small δ > 0 If s ≤ j,
change ps−1 to ps−1 − δ, pj to δ for some small δ > 0. In either case, for δ sufficiently small, the
new system remains in Case j but has strictly larger p̂∗1 , a contradiction.
Step 2: we prove pj+1 = · · · = pk . Being in Case j implies
                                     cj > 0,
                                     cr ≤ 0, ∀j + 1 ≤ r ≤ k,
                                                                                                       (14)
                                                    (r − 1)p−α
                                                            r
                                     where cr ≡ 1 − Pr      −α .
                                                          p
                                                       t=1 t
If cj+1 < 0, change pj to pj − δ, pj+1 to pj+1 + δ for some small δ > 0. The new system is still in
Case j but with strictly larger p̂∗1 , which leads to contradiction. Hence cj+1 = 0.
If cj+2 < 0, then pj+2 < pj+1 and we can change pj+1 to pj+1 − δ, pj+2 to pj+2 + δ for some
small δ > 0. Under this change, cj+1 decreases, cj+2 increases, cs , s ≥ j + 3 decreases, so the
configuration remains in Case j but with equal p̂∗1 for δ > 0 sufficiently enough. But then cj+1 < 0,
contradicting cj+1 = 0. Iterating this argument yields cj+1 = · · · = ck = 0, which implies
pj+1 = · · · = pk .
Step 3: We prove p1 = · · · = pj−1 . This follows from the same argument as in the proof of
Theorem A.2.


                                                     16
As a direct consequence, we obtain the following corollary.
Corollary A.4. Let pj = q, pj+1 = ... = pk = p. The upper bound u is given by
                                             −     1
                                                                                      1
                                                                              q − N −1
                                                 N −1
                                 (j − 1)p1
                   u=1−              −   1              1
                                                              =               −   1       1
                                                                                              .   (15)
                            (j − 1)p1 N −1 + q − N −1             (j − 1)p1 N −1 + q − N −1
Moreover,
                                              1      1
                                                ≤u<     .                                         (16)
                                              j     j−1
and {q, p, j} satisfies
                             p1 ≥ q ≥ p > 0,
                             (j − 1)p1 + q + (k − j)p = 1 − ϵ,
                                                             1
                             (j − 1)(p−α − p−α
                                            1 )=q
                                                   −α
                                                      , α=      ,                                 (17)
                                                           N −1
                                       N −1
                                   j−2
                             q>               p1 .
                                   j−1

Proof. This is an immediate consequence of Theorem A.3 and its proof (using cj+1 = 0, cj > 0).

Once j is determined, we can compute q and hence u. Equation (17) determines j in the following
sense.
Lemma A.5. If {q0 , p0 , j0 } satisfies Equation (17), then j0 ≥ j.

Proof. Let u0 be the corresponding maximal value associated with {q0 , p0 , j0 }. Then u0 ≤ u.
Combining Equation (17) and Equation (15) we have
                                             1            1
                                                ≤ u0 <        .                                   (18)
                                             j0        j0 − 1
If j < j0 , then u0 > u, which is a contradiction.
Lemma A.6. For any fixed ϵ, p1 and k, j = j(N ) is a non-decreasing function of N . Since
1/j ≥ u > 1/(j − 1), u = u(p1 ) is a non-decreasing function of N .

Proof. Suppose, for contradiction, that j(N + 1) < j(N ). Then
                                           N               N −1
                             j(N + 1) − 2           j(N ) − 2
                                                <                   .                             (19)
                             j(N + 1) − 1           j(N ) − 1
Let {j(N + 1), q(N + 1), p(N + 1)} be the corresponding configuration at N + 1. Using the
inequality above, this configuration can be used to construct a larger value of u at N with index
j = j(N + 1) < j(N ), contradicting the minimality of j in Lemma A.5.

A.2.3    Case 1
This case is impossible.

A.2.4    Summary of the Proof of Lemma 4.2
        • If
                                     1−ϵ                            1−ϵ
                                         ≤ p1 <                            N −1 ,                (20)
                                      k
                                                                     
                                                             k − 1 + k−2
                                                                       k−1

          then Case k applies. In this regime, the upper bound u is an increasing function of p1 and is
          given by
                                                                          1
                                                                      −
                                                             (k − 1)p1 N −1
                            u=1−                    −   1                                 1
                                                                                              .   (21)
                                      (k − 1)p1 N −1 + (1 + p1 − ϵ − kp1 )− N −1

                                                        17
       • Otherwise, Case j applies, and the upper bound is
                                                                                   −     1
                                                                                       N −1
                                                                  (j − 1)p1
                                             u=1−                    −     1                  1
                                                                                                  .                         (22)
                                                       (j − 1)p1 N −1 + q − N −1
         For any fixed ϵ, p1 and k, let j be the smallest positive integer such that the following
         equations (viewing {q, p} as variables) admits a solution:
                                       p1 ≥ q ≥ p > 0,
                                       (j − 1)p1 + q + (k − j)p = 1 − ϵ,
                                                                       1
                                       (j − 1)(p−α − p−α
                                                      1 )=q
                                                             −α
                                                                , α=      .                                                 (23)
                                                                     N −1
                                                 N −1
                                             j−2
                                       q>               p1 .
                                             j−1
         The index j is non-decreasing with respect to N , and u is further bounded by
                                                       1      1
                                                         ≤u<     .                                                          (24)
                                                       j     j−1

A.3   Proof of Lemma 4.3

Proof. The following proof is motivated by the following intuition: given the values of p1 and p2 , p̂∗1
attains its smallest possible value when the pj (j ≥ 3) are as large as possible. Let s be the smallest
integer such that p1 + sp2 ≥ 1. We have,
                       R
                                          !                                s+1
                                                                                              !
                      X                                                    X
    ∗                                   N                             N                     N
  p̂1 = π1 argmin{         pi (1 − p̂i ) } ≥ π1 argmin{p1 (1 − p̂1 ) +         p2 (1 − p̂i ) } . (25)
              {p̂i }R
                    i=1 i=1                                  {p̂i }s+1
                                                                   i=1                                i=2

Second, for a fixed p̂1 , Jensen’s inequality tells us that
                                     s+1
                                     X                                                                  1 − p̂1 N
                  p1 (1 − p̂1 )N +         p2 (1 − p̂i )N ≥ p1 (1 − p̂1 )N + sp2 (1 −                          )            (26)
                                     i=2
                                                                                                          s

Therefore, we have
                                     s+1
                                                             !
                              N
                                     X
                                                      N                                                             1 − p̂1 N
 π1   argmin{p1 (1 − p̂1 ) +               p2 (1 − p̂i ) }        = argmin{p1 (1 − p̂1 )N + sp2 (1 −                       ) }
      {p̂i }s+1                      i=2                                 p̂1                                          s
            i=1
                                                                                                                            (27)
Computing the right hand side of Equation (27) by taking derivatives we have
                                                                                                        1      1
                                                                                                       1−N   N −1
                                                      1 − p̂1 N       sp1 p2
              p̂∗1 ≥ argmin{p1 (1 − p̂1 )N + sp2 (1 −        ) }=1−        1      1  .                                      (28)
                       p̂1                              s           s + p11−N p2N −1
Since s is the smallest integer such that p1 + sp2 ≥ 1, we have
                                                1 + p2 > p1 + sp2 ,                                                         (29)
Combining Equation (29) and Equation (28) we arrive at
                                                                               1          1
                                                  (1 − p1 + p2 )p11−N p2N −1
                                     p̂∗1 ≥ 1 −                                1          N   .                             (30)
                                                  1 − p1 + p2 + p11−N p2N −1




                                                             18
B    Experimental details
Our codebase uses PyTorch [47], Accelerate [48], and deepspeed (https://github.com/
microsoft/DeepSpeed) to enable efficient training with memory constraints, and vllm [49] for
efficient inference. Code will be made available here (https://github.com/allanraventos/refine).
MATH. For experiments with MATH dataset [43] (license: MIT), we fine-tune the Llama-3-8B-
base [42] on the MATH [43] dataset. We start from the base model rather than Llama-3-8B-Instruct to
avoid potential leakage of the MATH dataset into Llama-3-8B-Instruct through post-training process.
We follow Lightman et al. [24] and use 12, 000 problems for training and the remaining 500 for
testing. In Sections 4 and 5.2, Figure 1, Figure 2 (a) and (b), we fine-tune the model for 4 epochs with
a learning rate of 2e-5 and batch size 64. We adopt a linear learning rate warmup in the first 20 steps.
For experiments with DCO, some of the data may have an extreme confidence regularizer value, if the
model is already quite confident in answers to certain problems. To maintain an approximately fixed
batch size, we set a threshold of 0.3 on the confidence regularizer F . Any training data examples
with an F lower than this threshold will be replaced with new training examples to construct the
batch. For the CoT experiments in Section 5.4, we use learning rate 2e-5 and batch size 128, with the
same learning rate warmup.
Theorem proving. We use LeanDojo benchmark[44] (license: CC-BY 2.0) and adopt the random
train and test split as introduced in Yang et al. [44]. The random test set includes 2,000 theorems. We
fine-tune the model Qwen2.5-Math-1.5B [28] on the training set for 3 epochs with learning rate 1e-5
and batch size 64. We adopt a linear learning rate warmup in the first 20 steps. To evaluate the model,
we use LeanDojo [44] to interact with the proof assistant. We impose a maximum wall clock time for
each theorem, in addition to limiting the number of passes per problem. For experiments with 4k
passes, the time budget is fixed at 5,000 seconds. In order to avoid the model going infinitely deep in
the search tree, we limit the number of proof steps to be at most 50.
DCOa objective. The DCOa introduced in Section 5.4 is an approximation for DCO. To construct
a batch of size B with DCOa , we process batches of samples sequentially; for each batch, we run
online inference on each of the samples and discard all samples with probability of success rate larger
than pthresh . We choose to discard samples which have a DCO confidence reguarizer F lower than
0.01, corresponding to pthresh = 0.1 for N ′ = 64. This process continues until we have enough
training data for a single batch. In Figure 4, we plot the number of discarded samples as a function of
training step for our DCOa experiments (same ones as in Table 3).
GRPO. We perform GRPO fine-tuning [10, 29] on problems of all difficulty levels in the MATH
training set. We follow the modifications to GRPO proposed in Dr. GRPO ([33]), that is, we do not
normalize advantages by the standard deviation of the group rewards, do not normalize a roll-out’s
contribution to the loss by its length, and do not include a KL divergence term with respect to the
reference model. Furthermore, we perform only one policy gradient update for each set of model
roll-outs, so there is no need for clipping. This leads to the surrogate objective taking the form,
                                        N ′ |oi |
                                   1 XX              πθ (oi,t | q, oi,<t )
                         L(θ) =                                                  Âi,t
                                   N ′ i=1 t=1 stop_grad (πθ (oi,t | q, oi,<t ))
where we adopt notation similar to [33]; N ′ is the number of roll-outs for a single problem statement
q, oi is the ith roll-out in the group, oi,t is the tth token in oi , and πθ (oi,t | q, oi,<t ) is the probability
assigned by the model to token oi,t conditioned on context oi,<t . The stop_grad operator prevents
the flow of gradients when computing ∇θ L. The advantages, in turn, are computed as Âi,t =
                 PN ′
r(q, oi ) − N1′ i′ =1 r(q, oi′ ), where r(q, oi ) is the binary reward assigned by the verifier to the
solution oi for the problem q.
For our experiments, we use N ′ = 8 and batch size 128, which results in a total of 1,024 roll-outs per
batch. We also perform batch balancing such that each batch contains no problems for which either
r(q, oi ) = 0 for all i or r(q, oi ) = 1 for all i, since these samples do not provide any gradient signal.
We use a constant learning rate of 1e-6,with a 20-step linear warmup; we train for 5 epochs. Note
that batch balancing results in fewer gradient steps. Additionally, we use the r1 template from [10]
for our experiments,
 A conversation between User and Assistant. The User asks a question, and the
  Assistant solves it. The Assistant first thinks about the reasoning process in


                                                       19
  the mind and then provides the User with the answer. The reasoning process is
  enclosed within <think> </think> and the answer is enclosed within <answer> </
  answer> tags, respectively, i.e., <think> reasoning process here </think> <answer
  > answer here </answer>.
 User: {question}
 Assistant: <think>


We strictly require solutions to follow the format specified in the prompt.

                                                            200



                              Number of Discarded Samples
                                                            150

                                                            100

                                                            50

                                                             0
                                                                  0   100      200   300
                                                                             Step

Figure 4: Number of discarded samples as a function of training step for the DCOa experiments. The
step structure reflects the model revisiting examples it has seen previously in training, where each
step closely matches the start of a new epoch.

Implementing online inference. Throughout our experiments and analysis, we extensively use the
open-source vllm package [49] for efficient inference. Integrating inference into the training loop
to enable training under the DCOa objective, as in Section 5.4, poses a challenging implementation
problem. We solve this problem by placing vllm worker processes, which together perform inference
on all GPUs, in a separate process group and use Ray (https://github.com/ray-project/ray)
to isolate them from the training loop. This enables running concurrent training and inference on the
same set of GPUs. We believe this inference in the loop setup will be useful to the community, as it
enables straightforward implementation of online data filtering approaches for LLM training.
Computational cost. All experiments with model size smaller than 10B are performed on machines
with 8 NVIDIA H100 GPUs or 8 NVIDIA A100 GPUs. Experiments with model size larger than
10B are performed on machines with 8 NVIDIA H200 GPUs or 8 NVIDIA B200 GPUs. Specifically,
for DCO on the MATH dataset, each run required approximately 1 NVIDIA H100 GPU-hour when
using the Llama-3-8B-base model, and approximately 4 NVIDIA B200 GPU-hours when using the
Llama-3-70B-base model. For DCOstep on the LeanDojo benchmark with the Qwen2.5-Math-1.5B
model, each run required around 12 NVIDIA H100 GPU-hours. For DCOa on the MATH dataset
with CoT, each run consumed about 60 NVIDIA H100 GPU-hours for the Llama-3-8B-base model.
For both DCO and DCOstep , the additional computational cost is minimal—limited to computing the
DCO factor, which is negligible compared to the cost of forward and backward passes. However,
DCOa , when applied to fine-tuning with CoT traces, introduces significant overhead due to the need
for online Monte Carlo estimation. In the setting of Llama-3 8B, with 32 layers, hidden dimension
4096, context length 1024, and batch size 128, we estimate 5 petaflops for each forward-backward
pass. Generating NM C = 64 CoT’s for each of 128 examples, in turn, requires approximately 50
petaflops. The actual inference compute cost depends on model performance: stronger models, which
will discard more samples, will need to process more samples in order to construct a full batch for the
next training step. Therefore there is a tradeoff: constructing a batch of 128 hard samples requires
running inference on more samples, but also means fewer steps are required to make a full pass
through the dataset.
The memory overhead is approximately 30% of GPU memory, when running one inference engine
per pair of H100 80GB GPUs. We note that while the flop overhead is significant, costly online
inference is also required in RL frameworks for CoT training. Furthermore, the choice of NM C can
be made smaller, leading to less precise estimates of the model’s probability of success on a given
problem, while speeding up training.


                                                                            20
C     Additional results
C.1   Easy data drives overconfidence

                                 Early in 1st epoch              Late in 1st epoch
                             2                               2
                             0                               0
                   g Ntest   2                               2
                             4                               4
                                 1    2 3 4 5                    1    2 3 4 5
                                     Difficulty Level                Difficulty Level
Figure 5: Easy data drives overconfidence and degrades performance when scaling test-time
compute. For the experiments in Figure 1, we compute the directional derivative ∇g LN         test at two
points during the Pfirst training epoch: 11% (early) and 86% (late). At each stage, the gradient
direction g = − (xi ,yi )∈B ∇ℓCE (xi , yi ) is evaluated on batches of previously unseen training data
of each difficulty level defined in the MATH dataset. Early in training, data from all difficulty levels
contribute to decreasing the test loss (left). However, later in training, easier examples (difficulty
level 2) provide no further benefit, while the easiest examples (difficulty level 1) actively degrade
test performance (right). The plotted ∇g LN  test is an average over batches of unseen data, and we use
N = 256, corresponding to pass@256.

We have shown in Section 4.2 that overconfidence limits performance gains from scaling test-time
compute. Here we investigate whether all training data contribute equally to the drop in pass@N
test performance. To quantify       this effect, we define the test loss as the negative log-probability
of coverage, LN                                N              N
                         P
                test = −    (x,y)∈D test log C(x,y) , where C(x,y) denotes the coverage for a single test
example (x, y). To measure how a training batch B influencesPthe final test loss, we compute the
directional derivative ∇g LN test for the gradient direction g = −    (xi ,yi )∈B ∇ℓCE (xi , yi ), where ℓCE
is the standard CE loss on a single example. A negative value, ∇g LN    test < 0, indicates that a gradient
step in the direction of g decreases the test loss.
To analyze the impact of data difficulty, we group training data by difficulty level (as specified in
the MATH dataset) and use the directional derivative to examine how a batch of previously unseen
data from a given difficulty level would affect LN    test at different stages of training. Early in training,
we observe that ∇g LN test is negative across all difficulty levels, indicating that data from all difficulty
levels contribute positively to reducing the test loss (Figure 5, left). However, near the end of the first
epoch, training on easier examples (difficulty levels 1 and 2) no longer improves performance, and
the easiest examples (level 1) actively degrade pass@N test performance (Figure 5, right). This shows
how continued training on easy data can harm test performance when scaling test-time compute.




                                                        21
C.2   Optimality of DCO is achieved when the training objective aligns with the test objective.




                                    1.0                              212
                                    0.8




                                                                          N' used in DCO
                                                                     28
                         Coverage
                                    0.6
                                    0.4
                                                                     24
                                    0.2          N'=256
                                                 DCO Frontier
                                    0.0 0 1 2 3 4 5                  20
                                       10 10 10 10 10 10
                                               N
Figure 6: Pareto-optimality at a given test strategy pass@N for some N is obtained by DCO
training for some N ′ close to N . Same as Figure 1 but with N ′ = 256 highlighted. We fine-tune
Llama-3-8B base models on the MATH dataset to produce direct answers. We fine-tune for 4 epochs
                                                             ′
                                                                                             ′
one model using CE loss and several models under the LN    DCO objective, for choices of N indicated
                                            ′
by color. Note that there is no choice of N that is optimal across all N (different colors are higher at
different N ). The black curve is a Pareto-optimal performance frontier traced by the max of coverage
curves for DCO over all N ′ . Fine-tuning with the DCO loss (N ′ = 256) achieves Pareto-optimality
for 180 ≤ N ≤ 385 at test-time, further confirming that Pareto-optimality at a given test strategy
pass@N for some N on the x-axis is obtained by DCO training for some N ′ close to N .




C.3   Additional results with Llama-3-70B-base


In this section, we present additional results using the larger Llama-3-70B-base model, which are
consistent with the findings reported for Llama-3-8B-base.




Table 4: Same as Table 1 but with Llama-3-70B-base model. Pass@N coverage metric on the MATH
test set for a Llama-3-70B-base model fine-tuned with CE loss on direct answers from the MATH
training set. Surprisingly, Pass@N test accuracy at large N decreases with number of training epochs.
                                      pass@1   pass@16    pass@256        pass@4k
                      Epoch 1          5.9%    34.3%       68.8%                84.2%
                      Epoch 2          6.9%    32.0%       63.0%                81.5%
                      Epoch 3          8.2%    24.2%       48.8%                72.2%
                      Epoch 4          7.9%    22.2%       44.2%                65.9%


                                                  22
Figure 7: Larger-sized model trained with CE loss also becomes overconfident in its greedy
completions; our proposed DCO objective limits this overconfidence on larger-sized models.
Same as Figure 1 but with Llama-3-70B-base. We fine-tune a Llama-3-70B-base model on the MATH
dataset to produce direct answers without a reasoning trace. ŷgreedy is the model’s greedy completion
when sampling autoregressively and choosing the most likely token at each step. Leftmost: The model
trained with CE loss assigns progressively larger confidences p̂(ŷgreedy |x) to its greedy completions
over the course of training. Left: At the end of the training, only a small portion of the model’s
highly confident completions are correct. This will harm the model’s pass@N performance when
scaling up N . Right: Same as leftmost but shown for the DCO loss with N = 256. Relative to the
CE loss, the model trained on DCO shows a much milder overconfidence effect. Rightmost: The
confidence distribution of the greedy completions after four epochs with DCO for various choices of
N . As N increases, the model’s confidence on the greedy completion is more stringently limited,
directly as a consequence of the overconfidence regularizer F .




Figure 8: DCO improves on CE for pass@N test coverage over a broad range of N and traces a
Pareto-optimal frontier with Llama-3-70B-base. Same as Figure 2 (a) but with Llama-3-70B-base
model. We fine-tune Llama-3-70B base models on the MATH dataset to produce direct answers. We
                                                                                     ′
fine-tune for 4 epochs one model using CE loss and several models under the LN      DCO objective, for
choices of N ′ indicated by color. We plot pass@N test coverage as a function of N , with each curve
(solid red or faint blue-green) corresponding to one fine-tuned model. Note that there is no choice
of N ′ that is optimal across all N (different colors are higher at different N ). The black curve is
a Pareto-optimal performance frontier traced by the max of coverage curves for DCO over all N ′ .
Pareto-optimality at a given test strategy pass@N for some N on the x-axis is obtained by DCO
training for some N ′ close to N .




C.4   Out-of-distribution evaluation

In this section, we present additional evaluation results on AIME24. We confirm that overconfidence
persists even on the out-of-distribution test set, and that the DCO algorithm saves test-time scaling by
regularizing the max confidence.


                                                  23
Table 5: Same as Table 1 but evaluate on AIME24 dataset. Pass@N coverage metric on the AIME24
dataset for a Llama-3-8B-base model fine-tuned with CE loss on direct answers from the MATH
training set. Surprisingly, Pass@N test accuracy at large N decreases with number of training epochs.
                                                     pass@1         pass@16        pass@256              pass@4k
                                  Epoch 1             0.2%            3.4%          30.5%                           80.5%
                                  Epoch 2             0.3%            4.1%          31.7%                           75.6%
                                  Epoch 3             0.2%            2.9%          16.0%                           42.0%
                                  Epoch 4             1.9%            4.9%          15.2%                           35.8%

                           CE Loss                          CE Loss                 DCO (N'=256)                                   DCO
              15
                       Epoch 1                          Incorrect                                 Epoch 1                   N0 = 1
                       Epoch 2                                                                    Epoch 2                   N 0 = 16
                       Epoch 3                          Correct                                   Epoch 3                   N 0 = 256
              10       Epoch 4                                                                    Epoch 4                   N 0 = 4k
     Counts




              5

              0
                   8           4           0            4         2       0    8           4                    0      8            4          0
                        logp(ygreedy|x)                 logp(ygreedy|x)             logp(ygreedy|x)                          logp(ygreedy|x)

Figure 9: A model trained with CE loss becomes overconfident in its greedy completions on
out-of-distribution test set; our proposed DCO objective limits this overconfidence on out-of-
distribution test set. Same as Figure 1 but evaluated on AIME24. We fine-tune a Llama-3-8B-base
model on the MATH dataset to produce direct answers without a reasoning trace and evaluate the
model on AIME24. ŷgreedy is the model’s greedy completion when sampling autoregressively and
choosing the most likely token at each step. Leftmost: The model trained with CE loss assigns
progressively larger confidences p̂(ŷgreedy |x) to its greedy completions over the course of training.
Left: At the end of the training, only a small portion of the model’s highly confident completions
are correct. This will harm the model’s pass@N performance when scaling up N . Right: Same
as leftmost but shown for the DCO loss with N = 256. Relative to the CE loss, the model trained
on DCO shows a much milder overconfidence effect. Rightmost: The confidence distribution of
the greedy completions after four epochs with DCO for various choices of N . As N increases, the
model’s confidence on the greedy completion is more stringently limited, directly as a consequence
of the overconfidence regularizer F .


                                                     1.0                                      212
                                                             CELoss
                                                     0.8     DCO Frontier
                                                                                                   N' used in DCO




                                                                                              28
                                          Coverage




                                                     0.6
                                                     0.4
                                                                                              24
                                                     0.2
                                                     0.0 0 1 2 3 4 5                          20
                                                        10 10 10 10 10 10
                                                                    N
Figure 10: DCO improves on CE for pass@N test coverage over a broad range of N and traces
a Pareto-optimal frontier on out-of-distribution test set. Same as Figure 2 (a) but evaluated on
AIME24. We fine-tune Llama-3-8B base models on the MATH dataset to produce direct answers
and evaluate on AIME24. We fine-tune for 4 epochs one model using CE loss and several models
              ′
                                               ′
under the LNDCO objective, for choices of N indicated by color. We plot pass@N test coverage as a
function of N , with each curve (solid red or faint blue-green) corresponding to one fine-tuned model.
Note that there is no choice of N ′ that is optimal across all N (different colors are higher at different
N ). The black curve is a Pareto-optimal performance frontier traced by the max of coverage curves
for DCO over all N ′ . Pareto-optimality at a given test strategy pass@N for some N on the x-axis is
obtained by DCO training for some N ′ close to N .


                                                                          24
C.5   Comparing with Focal Loss




                   MATH                                                 AIME24




Figure 11: DCO outperforms Focal Loss [50] for pass@N test coverage over a broad range of N
both for in- and out-of-distribution test sets. We fine-tune Llama-3-8B base models on the MATH
dataset to produce direct answers, using the Focal Loss [50]: LγFL (x, y) = −(1 − p̂(y | x)γ log p̂(y |
x). We fine-tune several models for 4 epochs under LγFL for choices of γ indicated by color. We plot
pass@N test coverage as a function of N for MATH (left) and AIME24 (right), with each curve
corresponding to one fine-tuned model. The black curve shows the Pareto-optimal performance
frontier traced by the max of coverage curves for DCO over all N ′ . The CE loss curves (red) and the
DCO frontier curves (black) are the same as in Figure 2 (a) for MATH and Figure 10 for AIME24.




C.6   Theorem proving

In Table 6, we show additional results for model performance under the DCOSTEP objective. We find
that the optimal Neff grows with increasing passes, agreeing with results in Sections 5.2 and 5.4. We
also conduct expert iteration [51, 52] on Mathlib with theorems that do not have proof traces in the
training set. We use pass@1k to prove those theorems. We find that our algorithm achieves a stronger
improvement over the baseline for pass@4k after the 1st iteration. This improvement might result
from the fact that the models can prove more easy theorems where the model has a higher confidence.
As a result, we believe our method will perform better with expert iteration.




       Table 6: Success rate on lean-dojo benchmark random test set trained with DCOstep .
                              E XPERT ITERATION 0                    E XPERT ITERATION 1
 DCO STEP       PASS @16 PASS @64 PASS @256 PASS @1 K PASS @4 K PASS @16 PASS @256 PASS @4 K

 Neff = 1 (CE) 30.0%       38.75%      46.05     50.75%     55.55%      40.3%     52.65%     58.55%
 Neff = 4      30.15%      39.5%       47.2%     52.95%     56.35%     40.8%      53.05%     59.45%
 Neff = 8       30.2%      38.9%      47.15%      52.7%      56.1%      40.1%     53.25%      59.5%
 Neff = 16     28.65%       46.7%     46.45%     52.9%      56.5%      39.05%      52.8%     60.05%
 Neff = 32     26.05%       46.7%      45.6%      51.5%      55.8%     37.05%      52.2%     59.15%
 E NSEMBLE      40.6%      49.15%      54.6%      59.0%     62.15%     49.05%      59.3%      64.8%




                                                  25
C.7   Plot of the upper bound and the lower bound




                             1.0                        Upper Bound
                             0.8                        Lower Bound

                       p1*   0.6
                             0.4

                                   100         101         102          103
                                                      N
Figure 12: Plot of the upper bound (Section A.2.4) and the lower bound (Equation (28)). We plot
the upper bound (blue) and lower bound (orange) for p1 = 12 , p2 = 14 , ϵ = 14 and k = 2. Both the
upper bound and the lower decrease monotonically in N and they both tends to 1 as N → 1+ .




C.8   Empirical evaluation of the approximately well calibrated assumption




Figure 13: We empirically verify the assumption that models are approximately well-calibrated.
Left: We fine-tune a Llama-3-8B-base model with CE loss on the MATH dataset without CoT
and perform beam search with a width of 256 to obtain the top 16 most probable completions. We
then measure the accuracy of these completions at each confidence rank. Right: We fine-tune a
Llama-3-8B-base model with CE loss on the MATH dataset with CoT and perform estimate the top
16 most frequent answers after tracing out the reasoning traces. We then measure the accuracy of these
answers at each frequency rank. The results demonstrate that test accuracy decreases approximately
monotonically with model confidence rank, supporting the assumption.




                                                 26
C.9    The data dependency of confidence and factor F

                               Late in 1st epoch                            Late in 1st epoch
                        0.10                                          0.8
                        0.08                                          0.6




                                                       F(N, p(y|x))
                        0.06

               p(y|x)
                                                                      0.4
                        0.04
                        0.02                                          0.2
                        0.00                                          0.0
                               1    2 3 4 5                                 1    2 3 4 5
                                   Difficulty Level                             Difficulty Level
Figure 14: Model is more confident on easy problems; DCO improves test-time scaling by
regularizing the easy examples. We fine-tune a Llama-3-8B-base model on the MATH dataset with
CE loss and plot the model confidence p(y|x) and the factor F (N, p(y|x)) at 86% of the first training
epoch. Both model confidence and factor are evaluated on the unseen data grouped by difficulty
level from the MATH dataset. Model confidence decreases with increasing difficulty, whereas the
regularization factor increases with problem difficulty. As a result, DCO effectively regularizes
contribution from easy examples. This regularization mitigates the potential detrimental effects of
overconfidence from easy examples as discussed in Section C.1. We use N = 256 corresponding to
pass@256 for the plots.



C.10    Quantifying the output diversity of models trained with DCO




Figure 15: DCO enhances output diversity in fine-tuned models. Increasing N ′ leads to greater
diversity in model completions. We fine-tune a Llama-3-8B-base model on the MATH dataset to
generate direct answers without explicit reasoning steps. Shannon entropy of model completions,
conditioned on the input prefix, is estimated using 4096 samples per test example. Left and Middle:
Histograms depicting the estimated entropy distributions for the test of MATH (left) and AIME24
(middle) respectively. Higher values of N ′ shift the entropy distribution to the right, reflecting
increased diversity of model outputs. Right: Mean entropy values plotted against N ′ with standard
errors of the mean. The estimated entropy increases with N ′ .




                                                      27
