                                             Entropy Regularization: A Free Correction to Cross-Entropy for
                                                                Verified Demonstrations
                                                           Mihir Dhanakshirur          Adam Ousherovitch           Ambuj Tewari
                                                                    Department of Statistics, University of Michigan
                                                            mihirgd@umich.edu aoushero@umich.edu tewaria@umich.edu
arXiv:2609.30572v1 [cs.LG] 24 Sep 2026




                                                                                          Abstract
                                                   Large language models are often post-trained on expert demonstrations using cross-entropy
                                               (CE), even when the downstream objective is not to imitate the demonstrated solution but to
                                               produce any output accepted by a verifier. This mismatch is seen in verifiable domains with
                                               multiple correct solutions, such as mathematical reasoning and code generation, where training
                                               data may contain only one expert solution per problem. We show that minimizing cross-entropy
                                               can be misaligned with minimizing verifier risk; two policies can assign identical likelihood to
                                               the observed demonstrations while placing different probability mass on incorrect outputs. This
                                               is formalized through a learning-theoretic counterexample in which CE minimization selects a
                                               suboptimal policy. We identify that controlling the support of the learned policy can solve this
                                               problem by preventing probability mass from spreading to unsupported outputs. Since support
                                               size is non-differentiable and computationally intractable, we propose entropy-regularized
                                               cross-entropy (ER-CE), using token-level Shannon entropy as a tractable proxy. Finally,
                                               across mathematical reasoning and code-generation benchmarks, we find that entropy-regularized
                                               training consistently improves verifier accuracy over standard cross-entropy. Our results identify
                                               a simple failure mode of imitation-based post-training in verifiable tasks and provide a practical
                                               objective that is better aligned with producing correct outputs.


                                         1    Introduction
                                         Large Language Models (LLMs) learn from demonstrations in two regimes: pretraining and post-
                                         training. Pretraining is fundamentally about imitation; models are trained to mimic the next-token
                                         distribution of vast datasets, making cross-entropy (CE) loss a natural and effective objective
                                         (Radford et al., 2019; Brown et al., 2020). Post-training, however, often targets a fundamentally
                                         different goal: maximizing reward on specialized downstream tasks (Ouyang et al., 2022; Lambert
                                         et al., 2024; DeepSeek-AI et al., 2025). This contrast has real consequences in verifiable domains
                                         with multiple correct solutions, such as mathematical reasoning (Cobbe et al., 2021) or code
                                         generation (Chen et al., 2021; Austin et al., 2021). In these settings, training data typically provides
                                         a single expert demonstration per problem. However, the ultimate objective is not to copy the
                                         expert, but to generate any solution that satisfies the verifier.
                                             Despite these different goals, standard post-training with demonstrations frequently uses super-
                                         vised fine-tuning (SFT) using CE (Chung et al., 2022; Touvron et al., 2023; Wang et al., 2023). While
                                         imitating an expert demonstrator is sufficient to pass a verifier, cross-entropy is misaligned with the
                                         true goal of the task. By penalizing the model for any deviation from the provided demonstration,
                                         cross-entropy forces the LLM to model the idiosyncratic details of the specific expert, rather than
                                         learning to be correct. Joshi et al. (2026) makes this precise by showing that CE fails to PAC-learn


                                                                                               1
the verifier-reward when the policy class cannot perfectly model the demonstrator. However, they
did not provide a tractable way to utilize this insight.
    We provide a tractable method to correct for this misalignment: entropy regularization. Specifi-
cally, we minimize entropy. The verifier-risk of a policy is exactly the probability mass it places
outside the set of correct answers. Cross-entropy pertains only to the answer that happened to
be demonstrated. It says nothing about how the remaining mass is allocated, so two policies with
identical likelihood on the training sample can assign arbitrarily different amounts of mass onto
answers the verifier rejects. We give a precise learning-theoretic example of how this can lead to a
suboptimal policy and show how favoring policies which minimize the entropy of the distribution
naturally corrects for this. This motivates a tractable fine-tuning objective that costs no additional
samples relative to standard SFT. Finally, we demonstrate its practical efficacy in improving verifier
accuracy across benchmarks for math and coding.


Contributions.      Our key contributions are:

    1. We present a counterexample showing that minimizing CE on expert demonstrations need not
       align with the objective of learning a policy that satisfies the verifier (Proposition 3.2).

    2. We introduce entropy-regularized cross-entropy (ER-CE) and establish conditions under which
       it improves upon standard CE minimization (Theorem 4.5).

    3. Finally, across math problem-solving and code-generation tasks, we show empirically that
       entropy-regularized cross-entropy outperforms standard cross-entropy (Section 5).


2     Related Work
2.1    Aligning Post-Training with the Downstream Objective
The observation that the loss minimized during training is a poor proxy for the quantity actually
evaluated at deployment predates LLMs and has been explored for LLMs in other settings.

Decision-focused learning. In the predict-then-optimize literature, a predictive model is fit
upstream of an optimization problem whose solution quality is the real object of interest. Elmachtoub
and Grigas (2022) show that minimizing prediction error doesn’t necessarily minimize downstream
decision regret, and propose a surrogate loss with the decision problem in mind; Donti et al. (2017)
and Wilder et al. (2019) develop variants for different settings, and El Balghiti et al. (2019) give
formal guarantees about this framework. This literature parallels ours. Cross-entropy can be seen
as a predictive loss, and verifier risk plays the role of the decision loss, with no guarantee that
improving the former improves the latter.

Task-loss training for structured prediction. A similar mismatch to ours was identified in
neural sequence modeling, where we have access to a single output, but there are multiple acceptable
outputs. Och (2003) and Shen et al. (2016) optimize the evaluation metric directly, Ranzato et al.
(2016) train at the sequence level rather than the token level, and Norouzi et al. (2016) incorporate
the task reward into maximum likelihood. This final method spreads mass outward from the
reference similar to how ours does.



                                                  2
Surrogate losses and consistency. Proposition 3.2 can be read as a statement that log-loss is
not a consistent surrogate for the verifier-risk over the constructed class. Thus, our work connects
to the family of papers analyzing surrogate consistency (Bartlett et al., 2006; Tewari and Bartlett,
2007). We emphasize what is different here. In the standard classification setting, log-loss is
calibrated and target risk is defined using the conditional label distribution instead of the support
of the demonstrator.

Aligning fine-tuning with test-time strategy. A recent line of work studies a related mis-
alignment on the inference side, asking how training should change given a fixed decoding or search
procedure. Chow et al. (2024) fine-tune directly against a Best-of-N verifier. Chen et al. (2025) show
that cross-entropy degrades pass@N coverage and construct a loss aligned for pass@N. Ousherovitch
and Tewari (2026) generalize this, deriving aligned losses for arbitrary aggregation and filtering.
Our misalignment is upstream of, and complementary to, this line. These methods derive new losses
so that per-sample likelihood gains translate into gains after inference strategies are used. The gap
we identify is present at pass@1 with no search. Both directions belong to the broader principle
that one should train for the quantity the verifier actually measures.

2.2   Entropy Regularization of Output Distributions
Entropy penalties have a long history, though almost always with the opposite sign to ours.
Grandvalet and Bengio (2004) minimize the entropy of predictions on unlabeled data in a semi-
supervised setting. Conversely, Pereyra et al. (2017) penalize low-entropy outputs as a regularizer
for supervised learning; the same sign convention appears as the entropy bonus used to sustain
exploration in reinforcement learning Eysenbach and Levine (2021); Haarnoja et al. (2018). Our
result regularizes entropy in the opposite direction.
    Most closely related, Agarwal et al. (2025) show that minimizing token-level entropy on unlabeled
self-generated outputs substantially improves LLM performance on math, physics, and coding
benchmarks. Their EM-FT objective and ours are similar in form. The contributions are, however,
distinct in both mechanism and justification. Their method is label-free and operates on model
outputs, while ours stems from supervised fine-tuning on labeled demonstrations; more importantly,
their results are purely empirical, while we derive it, showing that the entropy penalty is a tractable
surrogate for a support-minimizing loss that provably PAC-learns the verifier-risk (Theorem 4.5)
where cross-entropy provably does not (Proposition 3.2).

2.3   Learning from an Expert Policy
The work of Joshi et al. (2026) on learning from correct demonstrations is closely related to ours and
considers the same underlying problem setting. Like us, they identify a mismatch between standard
cross-entropy (CE) minimization and the objective of maximizing verifier success, and establish
an impossibility result for CE-based learning. Their approach, however, differs fundamentally
from ours. Rather than modeling the expert policy, they argue for directly learning the verifier
and propose a version-space algorithm that PAC-learns it. We instead retain the policy-modeling
perspective, motivated by the practical setting in which post-training begins from a pretrained
model with rich learned representations rather than training a policy from scratch. Moreover, while
their results provide a compelling theoretical case for departing from standard policy imitation,
their proposed version-space method is generally computationally intractable. In contrast, our
entropy-regularized objective can be incorporated into standard supervised fine-tuning with negligible
additional overhead and yields substantial improvements in verifier accuracy.


                                                  3
3     Limitation of Cross-Entropy
3.1   Problem Setup
Let X denote the space of questions/prompts and Y = {y1 , . . . , yK } denote the finite space of
answers/responses. Setting ∆(Y) to be the set of distributions on Y, we denote H to be a class
of functions from X to ∆(Y). For a hypothesis h ∈ H and question x ∈ X , h(·|x) ∈ ∆(Y) denotes
the distribution over answers and h(y|x) is the probability assigned to answer y ∈ Y for question x.
Finally, let (X × Y)∗ denote ∪m≥1 (X × Y)m .
    Fix a distribution D on X and hypothesis class H. We consider the setting where an unknown
true hypothesis h∗ ∈ H is chosen to be the demonstrator and a sample S := {(Xi , Yi )} is generated
as follows:
                                   X ∼ D and Y |X ∼ h∗ (·|X).
The verifier is a function V : X × Y → {0, 1} that indicates the correctness for every (question,
answer) pair. For a question x ∈ X , denote the set of correct answers by

                                    Cx := {y ∈ Y : V (x, y) = 1} .

For a distribution p ∈ ∆(Y), let supp(p) := {y ∈ Y : p(y) > 0} denote the support of the distribution.
We assume that our demonstrator h∗ satisfies

                                 supp(h∗ (·|x)) ⊂ Cx for all x ∈ X .

The above condition ensures that for every question, the demonstrator always reveals a correct
answer. Given a sample S, we are tasked with finding a hypothesis in H that minimizes the
verifier-risk:
                              R(h) := EX∼D,Y |X∼h(·|X) [1{Y ∈C
                                                            / x } ].

Our theoretical benchmark for evaluating learning algorithms is the notion of Probably Approximately
Correct (PAC) learnability.

Definition 3.1. A hypothesis class H is PAC-learnable with learning algorithm A : (X × Y)∗ → H
and sample complexity m(·, ·) : (0, 1) × (0, 1) → N, if for any ϵ, δ ∈ (0, 1) and m ≥ m(ϵ, δ), for any
D and h∗ ∈ H,                                                       
                            PS∼(D×h∗ )m R(A(S)) > inf R(h) + ϵ         < δ.
                                                        h∈H

    Informally, the PAC-learnability of an algorithm and a hypothesis class certifies that with
high probability over the random training sample, the learned hypothesis has small verifier-risk.
Practically, the most popular strategy is to select the hypothesis that minimizes the cross-entropy:
for a sample S = {(Xi , Yi )}m
                             i=1 ,

                                                       m
                                                 1 X
                              ACE (S) := arg min     − log h(Yi |Xi ).
                                             h∈H m
                                                       i=1


3.2   Counter-example
We demonstrate that minimizing cross-entropy can be misaligned with minimizing verifier risk by
constructing a hypothesis class for which ACE fails to PAC-learn. The full proof is presented in
Appendix A.


                                                   4
Proposition 3.2. Let X = N and Y = {1, 2, 3}. Additionally, let G denote the set of functions
from X to {1, 2}. Consider the following hypothesis class:

                                           H := {u} ∪ {hg }g∈G ,

where                                                     
                                                      1 1
                                       u(·|x) =        , ,0 , ∀x ∈ X
                                                      2 2
and for each g ∈ G,
                                              (
                                                  5 1 1
                                                            
                                  g
                                 h (·|x) =        8, 8, 4      if g(x) = 1
                                                  1 5 1
                                                  8, 8, 4       if g(x) = 2.

The empirical cross-entropy minimizer ACE fails to PAC-learn H.

Proof sketch. Suppose u is our true hypothesis and consider a sample S = {(Xi , Yi )}m  i=1 with all
Xi distinct. We can find a function g ∈ G s.t. g(Xi ) = Yi for every i because Yi are drawn from a
distribution u(·|Xi ) whose support is {1, 2}. The hypothesis hg ∈ H that corresponds to this g will
have a smaller cross-entropy loss on the sample than u because:
                                                      1  5
                                      u(Yi |Xi ) =      < = hg (Yi |Xi )
                                                      2  8
Despite u being the true hypothesis, the empirical minimizer of the cross-entropy loss will always
be hg . As a result, ACE incurs a non-zero risk because it assigns a weight of 14 outside the support
of u. The proof concludes by showing that for every m, there exists a distribution on X that, with
a probability bounded away from zero, draws distinct X1 , . . . , Xm for every m.

   There are a couple of points worth noting here. First, our proof crucially relies on the asymmetry
between cross-entropy and the verifier risk; cross-entropy depends only on the weight assigned to a
sampled Yi while computing the verifier risk involves probabilities on the set Y \ {Yi }. Secondly,
our hypothesis class H is rich when viewed as a class of probabilistic hypotheses but is in fact quite
simple when we ignore the probabilities and focus only on the supports. If we define

                                   R := {x 7→ supp(hx ) : h ∈ H} ,

then in Proposition 3.2,
                                R = {x 7→ {1, 2}} ∪ {x 7→ {1, 2, 3}} ,
so |R| = 2 even though |H| grows exponentially in m. Interestingly, the hypothesis class H above can
be PAC-learned by Atrivial , the algorithm that ignores probabilities and always returns hypothesis
u. This follows from two simple observations: (1) supp(u(·|x)) ⊂ supp(h(·|x)) for all x ∈ X , h ∈ H
and (2) if the support of our selected hypothesis is contained in the support of the true hypothesis
for every question, then its verifier-risk is 0. Even though Atrivial cannot be generalized beyond the
counter-example in Proposition 3.2, it motivates a loss function that explicitly accounts for the
support of the candidate hypothesis.




                                                        5
4        Entropy Regularized Cross-Entropy
Definition 4.1. For a hypothesis class H ⊂ (∆(Y))X , the induced support class is given by

                                          RH := {x 7→ supp(hx ) : h ∈ H} .

    H in Proposition 3.2 was an example of a hypothesis class with an induced support class of size
2. We generalize the setting in the counter-example by studying the PAC-learnability of hypothesis
classes whose induced support class is finite.

Assumption 4.2. For a hypothesis class H, the induced support class is finite, that is, |RH | < ∞.

  Under a minimal assumption, we prove that such hypotheses classes can be PAC-learned by
modifying the cross-entropy loss.1

Assumption 4.3. For a hypothesis class H, ∃ η > 0 s.t. ∀ x ∈ X , y ∈ Y, h ∈ H,

                                                 hx (y) ∈ {0} ∪ [η, 1],

    The counter-example in Proposition 3.2 satisfies Assumption 4.3 with η = 18 . This assumption
is also natural in the LLM-Verifier setting because the soft-max operation prevents a model from
assigning zero probability to a sequence of tokens.

Definition 4.4. For α ̸= 0, 1, define
                                                    X            1
                                      Sα (p) := (       pα (y)) 1−α for p ∈ ∆(Y).
                                                 y∈Y
                                                                       P
Since limα→0 Sα (p) = |supp(p)| and limα→1 Sα (p) = e−                     y∈Y p(y) log(p(y))   , we define
                                                                 P
                       S0 (p) := |supp(p)| and S1 (p) := e−          y∈Y p(y) log(p(y))   for p ∈ ∆(Y).

    For a distribution p, (Sα (p))α>0 is a family of surrogates for the support of p that are also differ-
entiable with respect to p. This family is closely connected to entropy-like measures: S1 (p) = eH(p)
where H(·) is the Shannon Entropy and for α > 0, α =     ̸ 1, Sα (p) = eRα (p) where Rα (·) is the Renyi
Entropy of order α. For a further discussion on (Sα (·)) as a proxy for the support, see Appendix C.


Theorem 4.5. Suppose H satisfies Assumption 4.2 and Assumption 4.3. Consider the loss
lλ,α : ∆(Y) × Y → R̄+ = [0, ∞],

                                         lλ,α (p, y) = − log(p(y)) + λSα (p).

Then the algorithm A that, for a given sample S = {(Xi , Yi )}m
                                                              i=1 , returns

                                                            m
                                                   1 X
                                    A(S) ∈ arg min     lλm ,αm (h(·|Xi ), Yi ),
                                               h∈H m
                                                           i=1

for sequences (λm ) and (αm ) s.t. λm ↑ ∞ and 0 < αm < 1, αm ↓ 0, PAC-learns H.

        The full proof is presented in Appendix B.
    1
        This assumption is true in the LLM-verifier setting with a finite vocabulary and maximum sequence length.


                                                            6
Proof Sketch. The proof proceeds through three steps, progressively replacing 1{y∈supp(p)}
                                                                                 /         with
− log(p(y)) and |supp(p)| with Sα (p).

Step 1: Indicator function + Support Penalty
Show that H is PAC-learnable with the loss:
                                                     1
                                        l(p, y) =      1 /         + |supp(p)|.
                                                     η {y∈supp(p)}



Step 2: Cross-Entropy + Support Penalty
Show that H is PAC-learnable with the loss:

                                       lλ (p, y) = − log(p(y)) + λ|supp(p)|,

if (λm ) is chosen s.t. λm ↑ ∞.


Step 3: Cross-Entropy + Entropy Penalty
Show that H is PAC-learnable with the loss:

                                       lλ,α (p, y) = − log(p(y)) + λ|Sα (p)|,

if (λm ), (αm ) are chosen s.t. λm ↑ ∞ and αm ↓ 0.

    We present the proof idea for Step 1, as it illustrates why adding a support (or support-like)
penalty to losses that depend only on the observed label, such as 1{y∈supp(p)} or − log(p(y))), yields
learnability guarantees that the un-regularized losses otherwise lack.
The proof relies on two key ideas:

 (1) Denote the expected risk of the loss l by R.
                                               e Minimizing the difference R(h) e ∗ ) is sufficient
                                                                           e − R(h
     for minimizing the verifier risk.

 (2) The loss l(p, y), which depends only on the underlying supports of the hypotheses, will
     generalize as the sample size increases.

Throughout we will use the notation rh (x) := supp(h(·|x)). For every x ∈ X ,
              X
                    h(y|x) ≤ |rh (x) \ rh∗ (x)| = |rh∗ (x) \ rh (x)| + |rh (x)| − |rh∗ (x)| .
               y ∈r
                 / h∗ (x)

and
                                   X                            X h∗ (y|x)  1
          |rh∗ (x) \ rh (x)| =               1{y∈rh∗ (x)} ≤                = PY ∼h∗ (·|x) (Y ∈
                                                                                             / rh (x)) .
                                                                      η     η
                                 y ∈r
                                   / h (x)                    y ∈r
                                                                / h (x)

where the inequality follows from Assumption 4.3. Together, the two inequalities allows us to bound
the verifier-risk by a surrogate risk for any hypothesis h ∈ H:

                                             R(h) − R(h∗ ) ≤ R(h)
                                                             e      e ∗ ),
                                                                  − R(h
                                                    | {z }
                                                       =0


                                                                7
where                                                      
                                              1
                              R(h)
                              e    := ED,h∗     1{Y ∈r
                                                    / h (X)} + ED [|rh (X)| .
                                              η
This shows (1). It remains to show (2): that the minimizer of the empirical loss l, PAC-learns H
under the surrogate risk. The loss function class LH := {(x, y) 7→ l(h(·|x), y) : h ∈ H} is finite by
Assumption 4.2 and the loss function l can be uniformly bounded for all x ∈ X , y ∈ Y and h ∈ H by
2
η . A standard application of Hoeffding’s Inequality gives PAC-learnability with sample complexity
                                                                    
                                                8              2|R|
                                     m(ϵ, δ) =      log                    .
                                               η ϵ2
                                                2                δ
This transformation is crucial because even though H may be infinite and cross-entropy may overfit
to the sample, the class of functions LH is finite and will generalize as the sample size increases.

    The following result immediately follows from Theorem 4.5.

Corollary 4.6. If we set λm = m and α = 1/m, then the algorithm A that, for a given sample
S = {(Xi , Yi )}m
                i=1 , returns
                                                     m
                                                1 X
                               A(S) ∈ arg min       lλm ,αm (h(·|Xi ), Yi ),
                                            h∈H m
                                                    i=1

PAC-learns H, with sample complexity
                      &     (                                             )'
                               32          3|R|    4     1          log η
             m(ϵ, δ) = max           log          , log     ,1 +                 .
                              η 2 ϵ2                             log 1 − ηϵ
                                                                            
                                             δ     ϵ     η                4


5    Experiments
We validate our theory by fine-tuning an LLM with entropy-regulated loss and evaluating it in two
settings: math problems (Section 5.1 and Section 5.3) and code generation (Section 5.2). These two
settings closely align with our theoretical setup. At training, for a given problem, we are provided
with only one out of many possible solutions. Concretely, given a question-answer pair (x, y), where
y = (y1 , . . . , yT ), and model π, the loss is given by:
                               T
                           1X                            λ
                              − log (π(yi |x, y1:i−1 )) + H (π(·|x, y1:i−1 )) ,
                           T                             T
                              i=1

where we use the convention that y1:i = (y1 , . . . , yi ) with y1:0 = ϕ.

    For solving math problems, this means that we’re shown one possible approach to obtain the
final numerical answer. In code generation, we’re shown one correct Python program for a given text
description of a program. At test time, the model is evaluated on whether it produces a solution
that passes the verifier, not whether it matches the exact solution in the dataset. Specifically, for
the math problems task, the model’s success depends on the final numerical solution being correct
and is agnostic to the reasoning trace. In code generation, the synthesized program is only required
to pass the test cases and be functionally correct. We include experimental details in Appendices D,
E, and F and relevant ablations in Appendices G, H, and I. These provide additional support for our
proposed mechanism. When CoT reasoning traces are replaced with answer-only targets, removing

                                                     8
multiple paths to the correct answers, gains largely disappear (Appendix I). Under temperature
decoding, which is closer to our theoretical setup, gains are even larger than under the greedy
decoder we use in this section (Appendix G). Finally, improvement is robust across a range of Renyi
order parameters α ∈ [0.5, 2] (Appendix H).

5.1   Math Problems
We evaluate the utility our loss on the GSM8K dataset (Cobbe et al., 2021), which contains high-
school level math problems where the correct answer is always a number. The training dataset
which consists of (problem, Chain-of-Thought answer) pairs is used to fine-tune the model and the
test set is used to verify whether the model has given a correct to a problem by checking if the
solution boxes the correct numerical answer.
    We fine-tune a Qwen2.5-1.5B-Instruct model (Yang et al., 2024) with our entropy-regularized
loss using Low-Rank Adaptation (LoRA) (Hu et al., 2022) across a grid of penalty strengths.
Performance is evaluated using the Pass@1 coverage metric.

                                                            λ                Mean     Std. Dev.
                                                            0.0 (Baseline)   0.4912   ±0.0154
                                                            0.3              0.5056   ±0.0116
                                                            0.5              0.5080   ±0.0064
                                                            1.0              0.5276   ±0.0064
                                                            2.0              0.5388   ±0.0086
                                                            3.0              0.5504   ±0.0083
                                                            4.0              0.5536   ±0.0134
                                                            6.0              0.5748   ±0.0134
                                                            8.0              0.5816   ±0.0161

                                                        Table 1: Accuracy peaks ≈ 9% over
Figure 1: Accuracy monotonically increases              standard cross entropy. GSM8K Pass@1
with penalty strength. Pass@1 accuracy on               accuracy under varying entropy penalties,
GSM8K (CoT) versus entropy penalty λ. Error             aggregated over 5 seeds.
bars show ±1 standard deviation over 5 seeds.


Results. As seen in Figure 1 and Table 1, performance monotonically increases with the strength
of the penalty among the λ we tested. At its peak, ER-CE outperforms standard CE by around 9%
at no added training cost.

5.2   Code Generation
We further evaluate the empirical performance of our loss on the Mostly Basic Python Problems
(MBPP) dataset (Austin et al., 2021). This dataset contains introductory-level Python programming
tasks where correctness is verified dynamically by executing the generated code against a suite of
hidden ‘assert‘ statements.
    We fine-tune a Qwen2.5-1.5B-Instruct model (Yang et al., 2024) with our entropy-regularized
loss using Low-Rank Adaptation (LoRA) (Hu et al., 2022) across a grid of penalty strengths
(λ ∈ [0.0, 6.0]). Performance is evaluated using Greedy Pass@1 accuracy over a sandboxed execution
environment.



                                                9
                                                              λ                Mean     Std. Dev.
                                                              0.0 (Baseline)   0.5270   ±0.0103
                                                              0.3              0.5380   ±0.0129
                                                              0.7              0.5660   ±0.0102
                                                              1.0              0.5710   ±0.0058
                                                              1.5              0.5540   ±0.0073
                                                              2.0              0.5490   ±0.0058
                                                              3.0              0.5340   ±0.0049
                                                              6.0              0.5380   ±0.0103

                                                          Table 2: ER-CE outperforms standard
                                                          CE by 4.4% at λ = 1. MBPP greedy
Figure 2: ER-CE uniformly beat out CE across
                                                          Pass@1 accuracy under varying entropy
all λ. Greedy Pass@1 accuracy on MBPP versus
                                                          penalties, aggregated over 5 seeds.
entropy penalty λ. Error bars show ±1 standard
deviation over 5 seeds.


Results. As shown in Figure 2, applying entropy regularization yields a robust, statistically
significant improvement over the standard Cross-Entropy baseline (λ = 0.0). At the baseline
(λ = 0.0), the model achieves a Pass@1 accuracy of 0.5270 ± 0.0103. As the entropy penalty
increases, performance climbs steeply, peaking at λ = 1.0 with an absolute gain of +4.40%, reaching
0.5710 ± 0.0058. However, continuing to crank up the penalty induces over-sharpening. At λ = 6.0,
the accuracy to degrade back to baseline levels (0.5380 ± 0.0103).

5.3   Scaling: Harder Problems and a Larger Model
The experiments above use a 1.5B model on an easier benchmark. Two questions remain. First, does
the effect survive on a harder benchmark, where the verifier is correspondingly less forgiving? Second,
does it survive at a scale where the base model has substantially richer pretrained representations?
    We evaluate on MATH (Hendrycks et al., 2021), a competition-mathematics benchmark, using
Qwen2.5-7B-Instruct (Yang et al., 2024). As before, we fine-tune with LoRA (Hu et al., 2022)
across a grid of penalty strengths and evaluate. Correctness is determined by symbolic equivalence
to the reference answer rather than string equality, so a model is credited for any expression denoting
the correct value.

Results. Every regularized configuration outperforms the cross-entropy baseline, and the separa-
tion is well outside seed variation: the baseline reaches 0.4200 ± 0.0071 while the weakest penalty
we tried already reaches 0.4583 ± 0.0062. The largest gain is +5.17% absolute at λ = 4. The
regularization clearly improved accuracy, providing evidence of robustness to scaling.


6     Conclusion
We study the mismatch between imitation-based training objectives and verifier accuracy in tasks
with multiple correct solutions. Although cross-entropy is a natural objective when the goal is to
reproduce an expert distribution, it can be poorly aligned to generate any output accepted by a
verifier. We make this mismatch precise through a learning-theoretic counterexample and show that
controlling the support of the learned policy can mitigate the resulting failure mode. Motivated
by this perspective, we propose entropy-regularized cross-entropy, which uses token-level Shannon


                                                  10
                                                            λ                Mean     Std. Dev.
                                                            0.0 (Baseline)   0.4200   ±0.0071
                                                            1.0              0.4583   ±0.0062
                                                            2.0              0.4400   ±0.0163
                                                            4.0              0.4717   ±0.0118
                                                            8.0              0.4667   ±0.0143

                                                        Table 3: ER-CE peaks over normal CE
                                                        by ≈ 5%. MATH greedy Pass@1 accuracy
                                                        across entropy penalties, aggregated over 3
                                                        seeds.
Figure 3: Performance gain from ER-CE uni-
formly remains even for a 7B model. Greedy
Pass@1 accuracy on MATH versus entropy penalty
λ for Qwen2.5-7B-Instruct. Error bars show ±1
standard deviation over 3 seeds; shading denotes the
baseline interval.


entropy as a tractable and differentiable proxy for support size. Our theoretical results identify
settings in which this objective improves upon standard cross-entropy minimization, while our
experiments on mathematical reasoning and code generation result in improved verifier accuracy
with negligible additional training overhead.
    Two important directions remain for future work. First, efficiently selecting the regularization
strength is an important practical challenge, since the minimum nonzero probability is typically
unknown. Understanding how verifier accuracy depends on the regularization strength requires
a deeper analysis of the optimization procedure, which is beyond the scope of this work. Second,
we consider only Pass@1, the probability that a single model-generated response is correct. More
advanced inference-time strategies, such as tree search, majority voting, and Best-of-N sampling,
introduce different objectives that may require different post-training methods. An important open
question is whether entropy minimization remains beneficial under these strategies, or whether
alternative regularization objectives are better suited to them.




                                                11
References
Shivam Agarwal, Zimin Zhang, Lifan Yuan, Jiawei Han, and Hao Peng. The unreasonable effective-
  ness of entropy minimization in llm reasoning. In Advances in Neural Information Processing
  Systems, 2025.

Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan,
  Ellen Jiang, Carrie Cai, Michael Terry, Quoc V. Le, et al. Program synthesis with large language
  models. arXiv preprint arXiv:2108.07732, 2021.

Peter L. Bartlett, Michael I. Jordan, and Jon D. McAuliffe. Convexity, classification, and risk
  bounds. Journal of the American Statistical Association, 101(473):138–156, 2006.

Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal,
  Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are
  few-shot learners. In Advances in Neural Information Processing Systems, volume 33, pages
  1877–1901, 2020.

Feng Chen, Allan Raventos, Nan Cheng, Surya Ganguli, and Shaul Druckmann. Rethinking fine-
  tuning when scaling test-time compute: Limiting confidence improves mathematical reasoning.
  arXiv preprint arXiv:2502.07154, 2025.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arXiv preprint arXiv:2107.03374, 2021.

Yinlam Chow, Guy Tennenholtz, Izzeddin Gur, Vincent Zhuang, Bo Dai, Sridhar Thiagarajan, Craig
  Boutilier, Rishabh Agarwal, Aviral Kumar, and Aleksandra Faust. Inference-aware fine-tuning
  for best-of-n sampling in large language models. arXiv preprint arXiv:2412.15287, 2024.

Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan
 Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, et al. Scaling instruction-finetuned
 language models. arXiv preprint arXiv:2210.11416, 2022.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
 Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to
 solve math word problems. arXiv preprint arXiv:2110.14168, 2021.

Tri Dao. Flashattention-2: Faster attention with better parallelism and work partitioning. arXiv
  preprint arXiv:2307.08691, 2023.

DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu,
 Qihao Zhu, Shirong Ma, Peiyi Wang, et al. Deepseek-r1: Incentivizing reasoning capability in
 llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.

Priya L. Donti, Brandon Amos, and J. Zico Kolter. Task-based end-to-end model learning in
  stochastic optimization. In Advances in Neural Information Processing Systems, 2017.

Othman El Balghiti, Adam N. Elmachtoub, Paul Grigas, and Ambuj Tewari. Generalization bounds
  in the predict-then-optimize framework. In Advances in Neural Information Processing Systems,
  2019.



                                               12
Adam N. Elmachtoub and Paul Grigas. Smart “predict, then optimize”. Management Science, 68
 (1):9–26, 2022.

Benjamin Eysenbach and Sergey Levine. Maximum entropy rl (provably) solves some robust rl
  problems. CoRR, abs/2103.06257, 2021.

Yves Grandvalet and Yoshua Bengio. Semi-supervised learning by entropy minimization. In Advances
 in Neural Information Processing Systems, volume 17, 2004.

Marian Grendar. Entropy and effective support size. Entropy, 8(3):169–174, 2006. doi: 10.3390/
 e8030169.

Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy
  maximum entropy deep reinforcement learning with a stochastic actor. In International Conference
 on Machine Learning, pages 1861–1870, 2018.

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
 Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. In
 Advances in Neural Information Processing Systems Datasets and Benchmarks Track, 2021.

Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
  and Weizhu Chen. Lora: Low-rank adaptation of large language models. In International
 Conference on Learning Representations, 2022.

Nirmit Joshi, Gene Li, Siddharth Bhandari, Shiva Prasad Kasiviswanathan, Cong Ma, and Nathan
  Srebro. Learning to answer from correct demonstrations. arXiv preprint arXiv:2510.15464, 2026.

Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze
 Brahman, Lester James V. Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. Tulu 3: Pushing
 frontiers in open language model post-training. arXiv preprint arXiv:2411.15124, 2024.

Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In International
  Conference on Learning Representations, 2019.

Sourab Mangrulkar, Sylvain Gugger, Lysandre Debut, Younes Belkada, Sayak Paul, and Benjamin
  Bossan. Peft: State-of-the-art parameter-efficient fine-tuning methods. https://github.com/
  huggingface/peft, 2022.

Mohammad Norouzi, Samy Bengio, Zhifeng Chen, Navdeep Jaitly, Mike Schuster, Yonghui Wu, and
 Dale Schuurmans. Reward augmented maximum likelihood for neural structured prediction. In
 Advances in Neural Information Processing Systems, 2016.

Franz Josef Och. Minimum error rate training in statistical machine translation. In Proceedings of
  the 41st Annual Meeting of the Association for Computational Linguistics, pages 160–167, 2003.

Adam Ousherovitch and Ambuj Tewari. Compute aligned training: Optimizing for test time
 inference. arXiv preprint arXiv:2604.24957, 2026.

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong
  Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow
  instructions with human feedback. In Advances in Neural Information Processing Systems,
  volume 35, pages 27730–27744, 2022.


                                               13
Gabriel Pereyra, George Tucker, Jan Chorowski, Lukasz Kaiser, and Geoffrey Hinton. Regularizing
 neural networks by penalizing confident output distributions. In ICLR Workshop, 2017.

Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language
  models are unsupervised multitask learners. Technical report, OpenAI, 2019.

Marc’Aurelio Ranzato, Sumit Chopra, Michael Auli, and Wojciech Zaremba. Sequence level training
 with recurrent neural networks. In International Conference on Learning Representations, 2016.

Shiqi Shen, Yong Cheng, Zhongjun He, Wei He, Hua Wu, Maosong Sun, and Yang Liu. Minimum
  risk training for neural machine translation. In Proceedings of the 54th Annual Meeting of the
  Association for Computational Linguistics, pages 1683–1692, 2016.

Ambuj Tewari and Peter L. Bartlett. On the consistency of multiclass classification methods. Journal
 of Machine Learning Research, 8:1007–1025, 2007.

Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay
 Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation
 and fine-tuned chat models. arXiv preprint arXiv:2307.09288, 2023.

Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A. Smith, Daniel Khashabi, and
  Hannaneh Hajishirzi. Self-instruct: Aligning language models with self-generated instructions. In
  Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume
 1: Long Papers), pages 13484–13508, 2023.

Bryan Wilder, Bistra Dilkina, and Milind Tambe. Melding the data-decisions pipeline: Decision-
  focused learning for combinatorial optimization. In Proceedings of the AAAI Conference on
  Artificial Intelligence, volume 33, pages 1658–1665, 2019.

Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi,
 Pierric Cistac, Tim Rault, Remi Louf, Morgan Funtowicz, et al. Transformers: State-of-the-art
 natural language processing. In Proceedings of the 2020 Conference on Empirical Methods in
 Natural Language Processing: System Demonstrations. Association for Computational Linguistics,
 2020.

An Yang et al. Qwen2 technical report. arXiv preprint arXiv:2407.10671, 2024.




                                                14
A       Proof of Proposition 3.2
Consider the following concrete example: X = N, Y = {1, 2, 3} and G := {1, 2}X . Define the function
u : X → ∆(Y) by
                                  u(·|x) = (1/2, 1/2, 0), ∀ x ∈ X .
For each g ∈ G, define the function hg : X → ∆(Y) by
                                          (
                                  g         ( 58 , 18 , 14 ) if g(x) = 1
                                h (·|x) =
                                            ( 18 , 58 , 14 ) if g(x) = 2.

Denote H := {u} ∪ {hg }g∈G ⊂ (∆(Y))X . Let m ∈ N and Nm ∈ N be a constant (that we will fix
later). Let D ≡ Unif([Nm ]) and h∗ = u. Recall that a sample {(Xi , Yi )}m
                                                                         i=1 is generated as follows:
independently, for all i ∈ [m],
                                  Xi ∼ D and Yi |Xi ∼ h∗ (·|Xi ).
This induces a distribution P over (X × Y)m . Denote the event

                                   Bm := {Xi are distinct ∀ i ∈ [m]} .

Then,
                                    Nm − 1 Nm − 2         Nm − (m − 1)
                       P(Bm ) = 1 ×        ×      × ··· ×
                                     Nm      Nm               Nm
                                 m        
                                Y        i
                              =     1−
                                        Nm
                                   i=1
                                   m−1                  2
                                    Y      − Ni − i 2
                               >          e    m       Nm

                                   i=1
                                      m(m−1)           m(m−1)(2m−1)
                                                   −
                               = e− 2Nm e                 6Nm2
                                                                            .

For Nm = ⌈ m(m−1)
             2    ⌉,
                             m(m−1)       m(m−1)(2m−1)                   2m(m−1)       4m(m−1)(2m−1)
                                      −                                − 2m(m−1) −
                          e− 2Nm e           6Nm2
                                                                ≥e                 e     6m2 (m−1)2

                                                                                2(2m−1)
                                                                            − 3m(m−1)
                                                                = e−1 e
                                                                        3
                                                                ≥ e− 2
                                                                  1
                                                                > .
                                                                  8
So, if Nm = ⌈ m(m−1)
                 2    ⌉, P(Bm ) > 18 . Now, if Bm holds, we receive a sample S with all Xi distinct.
So, ∃ gS ∈ G s.t. ∀ (Xi , Yi ) ∈ S, gS (Xi ) = Yi , because Yi |Xi ∼ uXi and supp(uXi ) = {1, 2}). This
gives:
              m                                                           m
           1 X                                                         1 X
                  − log (hgS (Yi |Xi )) = − log(5/8) < − log(1/2) =         − log (u(Yi |Xi )) .
           m                                                          m
            i=1                                                   i=1
    CE                                                            m
If A   denotes the algorithm that, given a sample S = {(Xi , Yi )}i=1 , returns the empirical risk
minimizer (ERM):
                                                            m
                                                  1 X
                                      arg min         − log(h(Yi |Xi )),
                                              h∈H m
                                                            i=1


                                                                  15
then ACE (S) ̸= u. For all h ∈ {hg }g∈G , R(h) = EX∼D [hX (y3 )] = 14 and R(u) = 0. Hence, for every
m, ∃ h∗ ∈ H and D on X s.t.
                                                         
                                  CE
                                                       1                 1
                         P R A (S) > inf R(h) +             ≥ P(Bm ) > ,
                                             h∈H        8                 8

because inf h∈H R(h) = 0. This shows that ACE does not PAC-learn H with the verifier-risk.


B      Proof of Theorem 4.5
B.1     Step 1
Theorem B.1. Suppose H satisfies Assumption 4.2 and Assumption 4.3. Consider the loss
l : ∆(Y) × Y → R,
                                   1
                         l(p, y) = 1{y∈supp(p)}
                                      /         + |supp(p)|.
                                   η
Then the algorithm A that, for a given sample S = {(Xi , Yi )}m
                                                              i=1 , returns

                                                                 m
                                                 1 X
                                  A(S) ∈ arg min     l(h(·|Xi ), Yi ),
                                             h∈H m
                                                              i=1

PAC-learns H.

     We start with the simple observation that inf h∈H R(h) = R(h∗ ) = 0. For each x ∈ X ,
            X
                    h(y|x) ≤ |supp(h(·|x)) \ supp(h∗ (·|x))|
        y ∈supp(h
          /      ∗ (·|x))


                            = |supp(h∗ (·|x)) \ supp(h(·|x))| + |supp(h(·|x))| − |supp(h∗ (·|x))| .

Now,
                                             X
    |supp(h∗ (·|x)) \ supp(h(·|x))| =                     1{y∈supp(h∗ (·|x))}
                                        y ∈supp(h(·|x))
                                          /
                                             X            h∗ (·|x)(y)
                                   ≤                                     (∵ y ∈ supp(h∗ (·|x)) =⇒ h∗ (y|x) ≥ η)
                                                                η
                                        y ∈supp(h(·|x))
                                          /
                                     1
                                   =   P     ∗     (Y ∈
                                                      / supp(h(·|x)))
                                     η Y ∼h (·|x)
                                                                    
                                                   1
                                   = EY ∼h∗ (·|x) 1{Y ∈supp(h(·|x))}
                                                        /              .
                                                   η

Let PD,h∗ and ED,h∗ denote the probability and expectation for X ∼ D, Y |X ∼ h∗ (·|X). We have
                                              
                           1
            R(h) ≤ ED,h∗     1 /                 + ED [|supp(h(·|X))| − |supp(h∗ (·|X))|].
                           η {Y ∈supp(h(·|X))}

Denote R(h)
       e    = ED,h∗ [l(h(·|X), Y )]. Then

                                            R(h) ≤ R(h)
                                                   e      e ∗ ).
                                                        − R(h


                                                            16
Let ĥ = A(S). Then
                                R(ĥ) − R(h∗ ) > ϵ =⇒ R(      e ∗ ) > ϵ.
                                                      e ĥ) − R(h

We can write
                        e ∗ ) = R(
                e ĥ) − R(h
                R(                      em (ĥ) + R
                                e ĥ) − R         em (ĥ) − R          em (h∗ ) − R(h
                                                             em (h∗ ) +R          e ∗)
                                                  |       {z       }
                                                                       ≤0
                                            em
                                ≤ 2 sup |R (h) − R(h)|,
                                                 e
                                    h∈H

      em (h) = 1 Pm l(h(·|Xi ), Yi ). Denote Lh (Xi , Yi ) := l(h(·|Xi ), Yi ) and let LH := {(x, y) 7→ Lh (x, y) : h ∈ H}.
where R        m   i=1
Then |LH | ≤ |R| < ∞. Further, for all x ∈ X , y ∈ Y, h ∈ H,
                                                                     1
                                            0 ≤ Lh (x, y) ≤            + K.
                                                                     η
So,

           P(R(ĥ) − R(h∗ ) > ϵ) ≤ P(sup |R
                                          em (h) − R(h)|
                                                    e      > ϵ/2)
                                     h∈H
                                                 m
                                          (                                            )!
                                       [      1 X
                                 =P                 Lh (Xi , Yi ) − E[Lh (X, Y )] > ϵ/2
                                             m
                                      h∈H       i=1
                                                                                     )
                                                   m
                                            (
                                       [       1 X
                                 = P                 L(Xi , Yi ) − E[L(X, Y )] > ϵ/2 
                                               m
                                      L∈LH        i=1
                                                m
                                                                                    !
                                    X        1 X
                                 ≤      P           L(Xi , Yi ) − E[L(X, Y )] > ϵ/2
                                            m
                                       L∈LH                  i=1
                                                    2
                                              − mϵ 2
                                                 1 +K
                                   ≤ 2|R|e     2 η    (      ) ,

where the last inequality follows by Hoeffding’s Inequality. Thus, for
                                      2
                                1
                                η +K
                                                            
                                                      2|R|
                     m≥2                    log                  ,   P(R(ĥ) − R(h∗ ) > ϵ) ≤ δ.
                                  ϵ2                    δ

B.2    Step 2
Theorem B.2. Suppose H satisfies Assumption 4.2 and Assumption 4.3. Consider the loss
lλ : ∆(Y) × Y → R̄+ = [0, ∞],

                                   lλ (p, y) = − log(p(y)) + λ|supp(p)|.

Then the algorithm A that, for a given sample S = {(Xi , Yi )}m
                                                              i=1 , returns

                                                                 m
                                                1 X
                                 A(S) ∈ arg min     lλm (h(·|Xi ), Yi ),
                                            h∈H m
                                                              i=1

for a sequence (λm ) s.t. λm ↑ ∞, PAC-learns H.


                                                             17
Proof. Denote
                                                         m
                                                    1 X
                                     ĥm := arg min     lλm (h(·|Xi ), Yi ).
                                                h∈H m
                                                        i=1

Recall
                                            R(h) ≤ R(h)
                                                   e      e ∗ ),
                                                        − R(h
where R(h)
      e    = η1 PD,h∗ (Y ∈
                         / supp(h(·|X))) + ED [|supp(h(·|X))|]. So,

             e ∗ ) = 1 PD,h∗ (Y ∈
   e ĥm ) − R(h
   R(                           / supp(ĥm (·|X))) + ED [|supp(ĥm (·|X))|] − ED [|supp(h∗ (·|X))|].
                     η

Denote rh (x) := supp(h(·|x)). First, observe that
                                                                                         m
                                                                                                         !
                                                                     1 X
             PD,h∗ (Y ∈
                      / supp(ĥm (·|X))) ≤ sup ED,h∗ [1{Y ∈r(X)}
                                                          /      ] −     1{Yi ∈r(X
                                                                              /    i )}
                                                                                                             ,
                                           r∈R                       m
                                                                                        i=1

where we use:
                                               m
                                           1 X
                                               1{Yi ∈r
                                                    / ĥm (Xi )} = 0,
                                           m
                                              i=1

because otherwise
                             m                                         m
                         1 X                           1 X ∗
                             l(ĥm (·|Xi ), Yi ) = ∞ >    l(h (·|Xi ), Yi ),
                         m                             m
                            i=1                                      i=1

which is a contradiction. Secondly,
                                                                                             m
                                                                                        1 X            log(1/η)
   ED [|supp(ĥm (·|X))|] − ED [|supp(h∗ (·|X))|] ≤ 2 sup ED [|r(X)|] −                     |r(Xi )| +          ,
                                                             r∈R                        m                 λm
                                                                                          i=1

because
         m                                                         m
  1 X                                                 1 X
      − log(ĥm (Yi |Xi )) + λm |supp(ĥm (·|Xi ))| =     lλm (ĥm (·|Xi ), Yi )
  m                                                   m
     i=1                                                           i=1
                                                                m
                                                              1 X
                                                         ≤               lλm (h∗ (·|Xi ), Yi )
                                                              m
                                                                   i=1
                                                                m
                                                              1 X
                                                         =               − log(h∗ (Yi |Xi )) + λm |supp(h∗ (·|Xi ))|
                                                              m
                                                                   i=1

and the fact that
                                      ĥm (Yi |Xi ) ≤ 1 and h∗ (Yi |Xi ) ≥ η.
Finally, we get
                                                                                   m
                                                                                                  !
                  R(        e ) ≤ 1 sup ED,h∗ [1{Y ∈r(X)}
                  e ĥm ) − R(h  ∗
                                                   /      ]−
                                                             1 X
                                                                 1{Yi ∈r(X
                                                                      /    i )}
                                  η r∈R                      m
                                                                                  i=1
                                                                           m
                                                                     1     X                  log(1/η)
                                        + 2 sup ED [|r(X)|] −                    |r(Xi )| +
                                            r∈R                      m                           λm
                                                                           i=1



                                                        18
Let ϵ > 0. If λm > 3ϵ log(1/η), then
                                                                    m
                                                                                      !      !
                                                               1  X                       ηϵ
         P(R(ĥm ) − R(h∗ ) > ϵ) ≤ P sup ED,h∗ [1{Y ∈r(X)}
                                                    /      ]−          1{Yi ∈r(X
                                                                            /    i )}
                                                                                        ≥
                                      r∈R                     m                           3
                                                                   i=1
                                                             m
                                                                                 !
                                                         1 X                   ϵ
                                   + P sup ED [|r(X)|] −         |r(Xi )| >          .
                                        r∈R              m                     6
                                                                   i=1

By Hoeffding’s Inequality and the fact that |r(x)| ≤ η1 for all x ∈ X , r ∈ R,

                                                                      mη 2 ϵ2
                               P(R(ĥm ) − R(h∗ ) > ϵ) ≤ 3|R|e− 18 .
                                   n                        n                     oo
                                                 3|R|
Finally, for any δ > 0, if m ≥ max η182 ϵ2 log     δ    , inf  m ∈ N : λ m > 3
                                                                             ϵ log  1
                                                                                    η   ,

                                       P(R(ĥm ) − R(h∗ ) > ϵ) ≤ δ.



Corollary B.3. If we set λm = m, then the algorithm A that, for a given sample S = {(Xi , Yi )}m
                                                                                               i=1 ,
returns
                                                m
                                             1 X
                            A(S) ∈ arg min        lλm (h(·|Xi ), Yi ),
                                       h∈H m
                                                    i=1

PAC-learns H, with sample complexity
                                                            
                                        18        3|R|    3     1
                      m(ϵ, δ) = max     2 2
                                            log          , log       .
                                       η ϵ          δ     ϵ     η

B.3    Step 3
We need a result connecting Sα (·) and |supp(·)| for α close to 0.

Lemma B.4. Let 0 < α < 1. If p ∈ ∆(Y) s.t. p(y) ∈ {0} ∪ [η, 1], then
                                                           1        α
                                                                       
                               0 ≤ |supp(p)| − Sα (p) ≤       1 − η 1−α .
                                                           η


Proof. First, we show that Sα (p) is non-increasing in α, so that if α > 0,

                                       |supp(p)| = S0 (p) ≥ Sα (p).

For 0 ≤ α < β < 1, let                  X                     X
                                 Zα =        p(y)α and Zβ =        p(y)β .
                                         y                     y

with the convention that Z0 := |supp(p)|. Then
                                             X p(y)α              β−α
                                  Zβ = Zα                 p(y)1−α 1−α .
                                              y
                                                  Zα



                                                   19
                β−α
Now, f (x) = x 1−α is concave, so,
                                                            ! β−α
                                      X p(y)α                   1−α                      1−β
                                                                            Zα
                           Zβ ≤ Zα                p(y)1−α             =            1−α
                                                                            β−α = Zα   .
                                             Zα
                                       y                                  Zα1−α
                                    1
Raising both sides to the power of 1−β shows the claim.
To show the other direction:
                    ! 1                  1
                                          1−α
                      1−α
          X                     X                          1     α                            α                α
                  α                    α
Sα (p) =      p(y)        ≥          η      = |supp(p)| 1−α η 1−α = |supp(p)| (|supp(p)|η) 1−α ≥ |supp(p)|η 1−α ,
            y                    y∈supp(p)

where the last inequality follows from |supp(p)| ≥ 1. Since |supp(p)| ≤ η1 , we get
                                                                                             α
                                                                      α
                                                                                 1 − η 1−α
                          |supp(p)| − Sα (p) ≤ |supp(p)| 1 − η        1−α       ≤           .
                                                                                      η


    Now, we’re ready to prove the most general result.
Theorem B.5. Suppose H satisfies Assumption 4.2 and Assumption 4.3. Consider the loss
lλ,α : ∆(Y) × Y → R̄+ = [0, ∞],

                                     lλ,α (p, y) = − log(p(y)) + λSα (p).

Then the algorithm A that, for a given sample S = {(Xi , Yi )}m
                                                              i=1 , returns
                                                      m
                                               1 X
                                A(S) ∈ arg min     lλm ,αm (h(·|Xi ), Yi ),
                                           h∈H m
                                                     i=1

for sequences (λm ) and (αm ) s.t. λm ↑ ∞ and 0 < αm < 1, αm ↓ 0, PAC-learns H.
Proof. Denote
                                                     m
                                                1 X
                                 ĥm := arg min     lλm ,αm (h(·|Xi ), Yi ).
                                            h∈H m
                                                    i=1

Similar to the proof for lλ (p, y), we can write:

             e ∗ ) = 1 PD,h∗ (Y ∈
   e ĥm ) − R(h
   R(                           / supp(ĥm (·|X))) + ED [|supp(ĥm (·|X))|] − ED [|supp(h∗ (·|X))|] .
                     η|            {z            } |                       {z                    }
                                       (1)                                                  (2)

The analysis for (1) is the same as before and we get:
                                                                                        m
                                                                                                   !
                                                                     1 X
             PD,h∗ (Y ∈
                      / supp(ĥm (·|X))) ≤ sup ED,h∗ [1{Y ∈r(X)}
                                                          /      ] −     1{Yi ∈r(X
                                                                              /    i )}
                                                                                                        .
                                           r∈R                       m
                                                                                      i=1

For (2), we first write
                                                                                    m               m                m
                                                                                 1 X            1 X               1 X
ED [|supp(ĥm (·|X))|]−ED [|supp(h∗ (·|X))|] ≤ 2 sup ED [|r(X)|] −                   |r(Xi )| +     |rĥm (Xi )|−     |rh∗ (Xi )|.
                                                    r∈R                          m              m                 m
                                                                                   i=1             i=1               i=1


                                                     20
Observe that
          m                             m                            m
       1 X                            1 X               log(1/η)   1 X                                
                     |rĥm (Xi )| −       |rh∗ (Xi )| ≤          +      |rĥm (Xi )| − Sα (ĥm (·|Xi ))
           m                          m                    λm      m
               i=1                       i=1                                            i=1
                                                                      m
                                                                    1 X
                                                               +               (Sα (h∗ (·|Xi )) − |rh∗ (Xi )|) .
                                                                   m
                                                                         i=1
Using Lemma B.4, we obtain
                                                                                                                    αm
                                                                                                                        
                            m
                          1 X
                                                       m
                                                     1 X                         log(1/η)               1 − η 1−αm
                                   |rĥm (Xi )| −             |rh∗ (Xi )| ≤               +                                  .
                         m                          m                               λm                          η
                             i=1                        i=1
Finally,
                                                                                   m
                                                                                                            !
           R(        e ∗ ) ≤ 1 sup ED,h∗ [1{Y ∈r(X)}
           e ĥm ) − R(h                      /      ]−
                                                        1 X
                                                            1{Yi ∈r(X
                                                                 /    i )}
                             η r∈R                      m
                                                                                  i=1
                                                                                                                                     αm
                                                                                                                                         
                                                                       m
                                                                     1 X                         log(1/η)                1 − η 1−αm
                                      + 2 sup ED [|r(X)|] −                     |r(Xi )| +                +                                   .
                                         r∈R                         m                              λm                           η
                                                                          i=1
                                                         αm
                                                              
                                                    1−η 1−αm
Let ϵ > 0. If λm > 4ϵ log(1/η) and                      η          < 4ϵ ,
                                                                       m
                                                                                         !      !
                                                                  1  X                       ηϵ
            P(R(ĥm ) − R(h∗ ) > ϵ) ≤ P sup ED,h∗ [1{Y ∈r(X)}
                                                       /      ]−          1{Yi ∈r(X
                                                                               /    i )}
                                                                                           ≥
                                         r∈R                     m                           4
                                                                      i=1
                                                                m
                                                                                    !
                                                            1 X                   ϵ
                                      + P sup ED [|r(X)|] −         |r(Xi )| >          .
                                           r∈R              m                     8
                                                                                          i=1
By Hoeffding’s Inequality,
                                                                                              mη 2 ϵ2
                                          P(R(ĥm ) − R(h∗ ) > ϵ) ≤ 3|R|e−                     32       .
Finally, for any δ > 0, if
                                                                                    αm
                                                                                          
            32         
                          3|R|
                                     
                                                   4
                                                         
                                                         1                  1 − η 1−αm
                                                                                            ϵ 
m ≥ max             log          , inf m ∈ N : λm > log      , inf m ∈ N :                <      ,
            η 2 ϵ2         δ                      ϵ     η                      η          4 

then
                                                P(R(ĥm ) − R(h∗ ) > ϵ) ≤ δ.


Corollary B.6. If we set λm = m and α = 1/m, then the algorithm A that, for a given sample
S = {(Xi , Yi )}m
                i=1 , returns
                                                                     m
                                                       1 X
                                        A(S) ∈ arg min     lλm ,αm (h(·|Xi ), Yi ),
                                                   h∈H m
                                                                    i=1
PAC-learns H, with sample complexity
                      &     (                                             )'
                               32          3|R|    4     1          log η
             m(ϵ, δ) = max           log          , log     ,1 +                 .
                              η 2 ϵ2                             log 1 − ηϵ
                                                                            
                                             δ     ϵ     η                4



                                                                    21
C      Discussion on (Sα (·))
For practical purposes, the support penalty is computationally tedious to deal with; it’s non-
differentiable and extremely sensitive to precision limits. We desire a surrogate S(·) for the support
that satisfies certain obvious properties:

    1. S(·) should be continuous and symmetric, i.e. invariant under reordering of labels.

    2. S(δy ) = 1 ≤ S(p) ≤ S(Unif(Y)) = |Y| for any distribution p on Y, where δy places unit mass
       on y ∈ Y and Unif(Y) is the uniform distribution on Y.

    3. For any distribution p on Y, S(p) = S((p, 0)), where (p, 0) is the distribution on Y ∪ {∗} with
       weight p(y) on y ∈ Y and weight 0 on ∗.

    4. For distributions p1 , p2 , S(q) = S(p1 )S(p2 ), where q = p1 ⊗ p2 is the product distribution of
       p1 and p2 .
                                                             P             1
The family of functions {Sα (·)}α>0,α̸=1 given by Sα (p) =           pα (y) 1−α for p ∈ ∆(Y) satisfies
                                                                 y∈Y
all the properties above (Grendar, 2006). Observe that
                                                                         P           
    • For α > 0 and α =                                           1
                       ̸ 1, log(Sα (·)) = Rα (·), where Rα (p) = 1−α log   y∈Y p α (y) is the Renyi

      entropy of order α.

    • In the limit α → 1, log(Sα (·)) → H(·), where H(p) = − y∈Y p(y) log(p(y)) is the Shannon
                                                                P
      entropy.

    • In the limit α → 0, log(Sα (p)) → log(|supp(·)|), the logarithm of the size of the support.




                                                   22
D     Experimental Setup GSM8k
To ensure full reproducibility, we detail the hyperparameters, data processing, and evaluation metrics
used in our empirical validation.

D.1    Data Preparation
We use the GSM8K dataset, a standard benchmark for mathematical reasoning.

    • Train Split: 1,000 randomly sampled problems.

    • Evaluation Split: 500 randomly sampled problems.

    • Formatting: The prompt explicitly instructs the model to ”Solve this step by step” and
      end the response with the format #### <answer>. Calculator annotations (e.g., <<...>>) are
      stripped from the target solutions.

    • Masking: Prompt tokens are masked (label = −100) so that both the cross-entropy loss and
      the entropy penalty are computed strictly over the generated response tokens.

D.2    Model Architecture & LoRA Configuration
Experiments are conducted using the Qwen/Qwen2.5-1.5B-Instruct base model. Due to hardware
constraints and to ensure training stability, we utilize Low-Rank Adaptation (LoRA).

    • Precision: bfloat16 (bf16) with Flash Attention 2 Dao (2023).

    • LoRA Rank (r): 16

    • LoRA Alpha: 32

    • LoRA Dropout: 0.05

    • Target Modules: q proj, k proj, v proj, o proj, gate proj, up proj, down proj.

D.3    Training Hyperparameters
Models are trained using a custom Hugging Face Trainer Wolf et al. (2020) implementation with
PEFT Mangrulkar et al. (2022) that calculates the in-graph token entropy dynamically.

    • Learning Rate: 2 × 10−4

    • LR Scheduler: Cosine decay with a 0.03 warmup ratio.

    • Epochs: 3.0

    • Effective Batch Size: 16 (8 per device × 2 gradient accumulation steps).

    • Optimizer: AdamW Loshchilov and Hutter (2019) (max gradient norm clipped to 1.0).

    • Sequence Lengths: Maximum sequence length of 768 tokens; max new generated tokens
      capped at 512 for CoT.




                                                 23
D.4    Evaluation details
We utilize a pure Greedy Pass@1 evaluation metric. The model performs deterministic generation
(argmax decoding) independently of temperature. Answer correctness is verified via strict string
matching and float tolerance (< 10−4 ) after stripping non-numeric characters from the final boxed
output. To account for variance in LoRA initialization and data shuffling, every λ configuration is
run across 5 distinct random seeds (0 . . . 4), with the mean and standard deviation reported.

Table 4: Detailed per-seed Pass@1 Accuracy on GSM8K across varying entropy penalty (λ) strengths
using the Qwen2.5-1.5B-Instruct model.

                                    Individual Seeds (Pass@1)                    Aggregate
 Entropy Penalty (λ)       Seed 0    Seed 1    Seed 2    Seed 3    Seed 4    Mean     Std. Dev.
 0.0 (Baseline)            0.5080    0.4620    0.4960     0.4940    0.4960   0.4912     ±0.0154
 0.3                       0.4840    0.5140    0.5040     0.5100    0.5160   0.5056     ±0.0116
 0.5                       0.5020    0.5100    0.5100     0.5000    0.5180   0.5080     ±0.0064
 1.0                       0.5220    0.5180    0.5320     0.5340    0.5320   0.5276     ±0.0064
 2.0                       0.5260    0.5500    0.5440     0.5420    0.5320   0.5388     ±0.0086
 3.0                       0.5440    0.5580    0.5400     0.5480    0.5620   0.5504     ±0.0083
 4.0                       0.5460    0.5540    0.5380     0.5780    0.5520   0.5536     ±0.0134
 6.0                       0.5640    0.5600    0.5960     0.5700    0.5840   0.5748     ±0.0134
 8.0                       0.6020    0.5900    0.5540     0.5760    0.5860   0.5816     ±0.0161




                                                24
E     Experimental Setup MBPP
To ensure full reproducibility, we detail the hyperparameters, data processing, and execution-based
evaluation used for the MBPP code generation experiments.

E.1    Data Preparation
We use the sanitized split of the MBPP dataset Austin et al. (2021), which ensures high-quality
problem descriptions and correct unit tests.
    • Train Split: 300 randomly sampled problems.

    • Evaluation Split: 200 randomly sampled problems.

    • Formatting: The prompt explicitly instructs the model to write a complete Python function
      and provides the first unit-test as a hint to enforce proper function naming. The model is
      required to return the code enclosed in standard Markdown Python blocks (‘‘‘python ...
      ‘‘‘).

    • Masking: Prompt tokens are masked (label = −100) so that both the cross-entropy loss and
      the entropy penalty are computed strictly over the generated Python AST (Abstract Syntax
      Tree) tokens.

E.2    Model Architecture & LoRA Configuration
Experiments are conducted using the Qwen/Qwen2.5-1.5B-Instruct base model, utilizing Low-
Rank Adaptation (LoRA) for training stability.
    • Precision: bfloat16 (bf16) with scaled dot-product attention (SDPA).

    • LoRA Rank (r): 16

    • LoRA Alpha: 32

    • LoRA Dropout: 0.05

    • Target Modules: q proj, k proj, v proj, o proj, gate proj, up proj, down proj.

E.3    Training Hyperparameters
Models are trained using a custom Hugging Face Trainer Wolf et al. (2020) implementation with
PEFT Mangrulkar et al. (2022).
    • Learning Rate: 2 × 10−4

    • LR Scheduler: Cosine decay with a 0.03 warmup ratio.

    • Epochs: 3.0

    • Effective Batch Size: 16 (8 per device × 2 gradient accumulation steps).

    • Optimizer: AdamW Loshchilov and Hutter (2019) (max gradient norm clipped to 1.0).

    • Sequence Lengths: Maximum sequence length of 768 tokens; max new generated tokens
      capped at 256 to accommodate multiline code structures.

                                                25
E.4    Execution-Based Evaluation
Because code correctness cannot be determined by static string matching, we utilize a dynamic
evaluation pipeline. We employ a pure Greedy Pass@1 evaluation metric, wherein the model
performs deterministic generation (argmax decoding, T = 0.0).
    The extracted code blocks are passed to a sandboxed Python exec() environment alongside
the suite of dataset-provided assert statements. To prevent hanging from model-generated infinite
loops (e.g., non-terminating while conditions), we wrap the execution environment in a UNIX
signal alarm, enforcing a strict 2.0-second timeout per problem. Code that throws any exception
(AssertionError, SyntaxError, NameError) or exceeds the timeout is marked incorrect. Every λ
configuration is run across 5 distinct random seeds (0 . . . 5) to capture variance in LoRA initialization
and training data order.

Table 5: Detailed per-seed Greedy Pass@1 Accuracy on MBPP across varying entropy penalty (λ)
strengths using the Qwen2.5-1.5B-Instruct model.

                                            Individual Seeds                           Aggregate
 Entropy Penalty (λ)         Seed 0     Seed 1    Seed 2     Seed 3     Seed 4     Mean     Std. Dev.
 0.0 (Baseline)              0.5450     0.5300     0.5150     0.5200     0.5250    0.5270     ±0.0103
 0.3                         0.5300     0.5550     0.5350     0.5200     0.5500    0.5380     ±0.0129
 0.7                         0.5700     0.5700     0.5600     0.5800     0.5500    0.5660     ±0.0102
 1.0                         0.5750     0.5700     0.5750     0.5600     0.5750    0.5710     ±0.0058
 1.5                         0.5600     0.5600     0.5550     0.5400     0.5550    0.5540     ±0.0073
 2.0                         0.5500     0.5450     0.5550     0.5550     0.5400    0.5490     ±0.0058
 3.0                         0.5400     0.5400     0.5300     0.5300     0.5300    0.5340     ±0.0049
 6.0                         0.5250     0.5400     0.5400     0.5550     0.5300    0.5380     ±0.0103




                                                   26
F     Experimental Setup: MATH
We detail the data processing, hyperparameters, answer-equivalence procedure, and the loss imple-
mentation used for the MATH experiments of Section 5.3.

F.1    Data Preparation
We use the MATH dataset (Hendrycks et al., 2021).

    • Train Split: 1,000 problems sampled uniformly at random (seed 42) from the MATH training
      split, pooled across all seven subject categories.

    • Evaluation Split: 200 problems sampled from MATH-500, a held-out subset of the MATH
      test split. Evaluating on a test-split subset guarantees no overlap with the fine-tuning data.

    • Filtering: Training problems whose reference solution contains no \boxed{} expression are
      discarded, since there is no answer to imitate. Problems containing Asymptote figures ([asy])
      are also discarded, to avoid fine-tuning the model to emit diagram markup.

    • Formatting: The prompt instructs the model to solve the problem step by step and to place
      its final answer in \boxed{}. Reference solutions are used verbatim as targets; they already
      terminate in a boxed answer.

    • Masking: Prompt tokens are masked (label = −100) so that both the cross-entropy loss and
      the entropy penalty are computed strictly over response tokens.

F.2    Model Architecture and LoRA Configuration
Experiments use Qwen/Qwen2.5-7B-Instruct (Yang et al., 2024) with Low-Rank Adaptation (Hu
et al., 2022).

    • Precision: bfloat16 (bf16) with FlashAttention-2 (Dao, 2023).

    • LoRA Rank (r): 16

    • LoRA Alpha: 32

    • LoRA Dropout: 0.05

    • Target Modules: q proj, k proj, v proj, o proj, gate proj, up proj, down proj.

F.3    Training Hyperparameters
Models are trained with a custom Hugging Face Trainer (Wolf et al., 2020) implementation using
PEFT (Mangrulkar et al., 2022) that computes the in-graph token entropy dynamically.

    • Learning Rate: 2 × 10−4

    • LR Scheduler: Cosine decay with a 0.03 warmup ratio.

    • Epochs: 3.0

    • Effective Batch Size: 16 (2 per device × 8 gradient accumulation steps), with gradient
      checkpointing enabled.

                                                 27
   • Optimizer: AdamW (Loshchilov and Hutter, 2019) (max gradient norm clipped to 1.0).

   • Sequence Lengths: Maximum sequence length of 1,024 tokens; max new generated tokens
     capped at 1,024, reflecting the longer derivations MATH requires relative to GSM8K.

   • Seeds: Every λ configuration is run across 3 random seeds (0 . . . 2), with mean and standard
     deviation reported.

F.4    Chunked Computation of the Entropy Term
The entropy penalty requires a full softmax over the vocabulary at every response position. Computed
in fp32, as numerical stability demands, this is a tensor of shape N × V with V = 151,936 for
Qwen2.5, where N is the number of response tokens in the batch; several such tensors are live
simultaneously during the backward pass. At 7B this footprint is prohibitive alongside the model
weights.
    We therefore evaluate the loss in chunks of 512 response positions, wrapping each chunk in
gradient checkpointing so that the fp32 intermediates are discarded after the forward pass and
recomputed during backward. Cross-entropy and entropy are accumulated as sums over chunks and
normalized once at the end. The computation is numerically identical to the unchunked form; peak
memory for the loss head falls from O(N V ) to O(CV ) for chunk size C. This costs one additional
forward pass through the softmax and adds negligible wall-clock time relative to the transformer
forward.

F.5    Answer Equivalence
                                                                     √
Unlike GSM8K, MATH answers are arbitrary LATEX expressions ( 34 , 2 3, (−∞, 2], x2 + 1), so string
equality would systematically under-count correct answers written in a different but equivalent form.
We use the following procedure.

  1. Extraction. The last \boxed{} expression in the generation is extracted by brace matching.
     If none is present, an explicit “the final answer is X” pattern is accepted as a fallback. We
     deliberately do not fall back to the last numeral in the generation: on MATH this manufactures
     spurious correctness whenever a digit appearing in the reasoning trace coincides with the
     reference answer, and would bias the comparison toward whichever configuration produces
     shorter derivations.

  2. Normalization. The extracted answer and the reference are each normalized under two
     independent conventions, covering fraction and radical canonicalization, removal of units,
     degree symbols, currency symbols and \text{} wrappers, and digit-group separators. A
     match under either convention is accepted.

  3. Numeric comparison. If both normalized forms parse as reals, they are compared with
     tolerance 10−6 .

  4. Symbolic comparison. As a last resort, both expressions are converted to symbolic form
     and their difference simplified; a difference of zero is accepted. Each such check is guarded by
     a 5-second timeout, since model output can induce pathological simplification.




                                                 28
G     Temperature Ablation
Every result in the main paper is measured with greedy Pass@1. This appendix reports the same
three experiments measured instead with temperature-sampled Pass@1, explains why sampled
evaluation is the closer empirical analogue of the verifier risk our theory is stated in terms of, and
explains why we nonetheless promote the greedy numbers to the main paper.

G.1    Why Sampled Evaluation is Closer to the Theory
The verifier risk of Section 3 is R(h) = EX∼D, Y ∼h(·|X) [1{Y ∈
                                                              / CX }]: an expectation over draws from
the policy, equal to the probability mass the policy places outside the correct set. Sampling k
completions per problem and scoring the fraction that the verifier accepts is a direct Monte Carlo
estimate of 1 − R(h) for the decoded policy. Greedy Pass@1 is not an estimate of this quantity
at all. It is a property of a single argmax trajectory, and it is almost entirely insensitive to how
mass is allocated away from that trajectory, which is precisely the degree of freedom Proposition 3.2
exploits and the entropy penalty is designed to control. Two policies that differ enormously in
verifier risk can decode identically under argmax.
    Sampled evaluation therefore tests the mechanism, not just the outcome. By withdrawing mass
from incorrect outputs rather than by some incidental effect on the argmax path, the measured gains
should be larger under sampling than under greedy decoding. They are, on all three benchmarks.
    One caveat on the match: sampling at T = 0.8 estimates the verifier risk of the tempered policy
  1/T
h , not of h itself. Only T = 1 recovers R(h) exactly. We report T = 0.8 because it is the decoding
temperature in common practical use.

G.2    Protocol
Training is unchanged in every respect, same model, same LoRA configuration, same hyperparameters,
same seeds, same λ grid, same data. Only decoding differs. For each problem we draw k independent
samples at temperature T = 0.8 and report
                                              number of accepted samples
                         sampled Pass@1 =                                .
                                                       neval · k
We use k = 8 on GSM8K and k = 4 on MBPP and MATH. Sampling is from the full tempered
softmax: we set top k = 0 and top p = 1. Truncated sampling discards the tail of the predictive
distribution, which is exactly the region whose mass this paper is about; measuring under truncation
would suppress both the failure mode and the correction. The GSM8K sampled sweep uses a coarser
λ grid and three seeds rather than five; MBPP and MATH use the full main-paper grids and seed
counts.

G.3    Results
The gains are roughly twice as large under sampling. On GSM8K the entropy penalty
buys +9.04% absolute under greedy decoding and +19.00% under sampling (0.3825 → 0.5725). On
MBPP it buys +4.40% greedy and +10.12% sampled (0.4223 → 0.5235). On MATH it buys +5.17%
greedy and +9.79% sampled (0.3696 → 0.4675). The pattern is consistent: the metric that can see
off-argmax probability mass records about twice the improvement of the metric that cannot. This
is the signature the mechanism predicts.




                                                 29
         Under review as a conference paper at ICLR 2027




1404
                                                          Effect of Entropy Regularization on GSM8K
1405
                                               0.60
1406
1407
1408
                                               0.55



                             Pass@1 Coverage
1409
1410                                           0.50
1411
1412                                           0.45
1413                                                                                Best per curve
1414                                                                                CE baseline ( = 0)
                                               0.40                                 Greedy Pass@1 (5 seeds)
1415                                                                                Sampled Pass@1, T = 0.8, k = 8 (3 seeds)
1416                                                  0      1     2       3        4                  6                 8
1417                                                                   Lambda (Entropy Penalty)
1418
1419
       Figure  4: 4:
          Figure  GSM8K
                     GSM8K Pass@1    under
                                Pass@1      greedy
                                         under      decoding
                                                 greedy      and under
                                                        decoding        temperature
                                                                  and under          sampling
                                                                             temperature       (T =(T0.8,=k 0.8,
                                                                                         sampling           = 8)
1420
       versus  entropy  penalty   λ. Dashed   lines mark each  curve’s cross-entropy baseline; stars mark
          k = 8) versus entropy penalty λ. Dashed lines mark each curve’s cross-entropy baseline; stars markeach
1421
       curve’s  best λ. best
          each curve’s  Errorλ. bars  bars ±1
                                Errorshow  show standard deviation
                                                  ±1 standard      overover
                                                              deviation  seeds.
                                                                             seeds.
1422
1423
         Table 6: GSM8K Pass@1 accuracy under varying entropy penalties, under greedy decod-
       G.4   Why
         ing and   the temperature
                 under  Main Paper    Reports
                                   sampling (T Greedy
                                               = 0.8, kPass@1
                                                         = 8 samples per problem).                Model:
1424
1425
         Qwen2.5-1.5B-Instruct.
       There                              The sampled
             are two reasons we use the greedy   numberscolumn
                                                          in theismain paper.on a coarser λ grid and over
                                                                   evaluated
         3 seeds; dashes mark configurations not run under sampling.
1426
1427 Greedy decoding performs better. Greedy Pass@1 is higher than sampled Pass@1 at every λ
     on every benchmark (0.5816 againstGreedy   0.5725Pass@1
                                                        on GSM8K, Sampled
                                                                      0.5710Pass@1       = 0.8)on MBPP, 0.4717
                                                                              against(T0.5235
1428
                           0.0 (Baseline)
1429 against 0.4675 on MATH).                0.4912 ±
                                      A practitioner    0.0154 one of0.3825
                                                     deploying                  ± 0.0023
                                                                         these models   for a single attempt per
                           0.3
1430 problem would decode greedily.          0.5056  ±  0.0116                  –
1431
                           0.5               0.5080 ± 0.0064                    –
                           1                 0.5276 ± 0.0064            0.4942 ± 0.0144
1432 Sampled evaluation at a fixed temperature confounds the policy with its effective
                           2                 0.5388 ± 0.0086                    –
1433 temperature. Minimizing entropy sharpens the predictive distribution. Sampling a sharpened
                           3                 0.5504 ± 0.0083            0.5246 ± 0.0060
1434 distribution at T =40.8 is, in its effect,   similar
                                             0.5536       to sampling the original
                                                     ± 0.0134                   –     distribution at some lower
1435 temperature. A sampled6      comparison  at fixed T  therefore
                                             0.5748 ± 0.0134        cannot  on its
                                                                                –  own  separate ”the regularized
1436 policy places less mass
                           8     on incorrect0.5816
                                               outputs”   from ”the regularized
                                                     ± 0.0161                      policy is being decoded at a
                                                                        0.5725 ± 0.0068
1437 lower effective temperature”. Greedy decoding is immune to this by construction: the argmax
1438 is invariant to any monotone temperature rescaling, so greedy Pass@1 cannot be inflated by an
1439 effective-temperature
        Sampled evaluationeffect.
                                at a fixed temperature confounds the policy with its effective temperature.
1440    Minimizing entropy sharpens the predictive distribution. Sampling a sharpened distribution at T =
1441    0.8 is, in its effect, similar to sampling the original distribution at some lower temperature. A
1442    sampled comparison at fixed T therefore cannot on its own separate ”the regularized policy places
1443    less mass on incorrect outputs” from ”the regularized policy is being decoded at a lower effective
1444    temperature”. Greedy decoding is immune to this by construction: the argmax is invariant to any
1445
        monotone temperature rescaling, so greedy Pass@1 cannot be inflated by an effective-temperature
        effect.
1446
1447
1448
1449
1450
1451
1452
1453                                                                           30
1454
1455
       Table 6: GSM8K Pass@1 accuracy under varying entropy penalties, under greedy decoding and under
       temperature sampling (T = 0.8, k = 8 samples per problem). Model: Qwen2.5-1.5B-Instruct.
       The sampled column is evaluated on a coarser λ grid and over 3 seeds; dashes mark configurations
       not run under sampling.

                                                            Greedy Pass@1          Sampled Pass@1 (T = 0.8)
                          0.0 (Baseline)                   0.4912 ± 0.0154               0.3825 ± 0.0023
                          0.3                              0.5056 ± 0.0116                      –
                          0.5                              0.5080 ± 0.0064                      –
                          1                                0.5276 ± 0.0064               0.4942 ± 0.0144
                          2                                0.5388 ± 0.0086                      –
                          3                                0.5504 ± 0.0083               0.5246 ± 0.0060
                          4                                0.5536 ± 0.0134                      –
                          6                                0.5748 ± 0.0134                      –
                          8                                0.5816 ± 0.0161               0.5725 ± 0.0068

       Table 7: MBPP Pass@1 accuracy under varying entropy penalties, under greedy decoding and under
       temperature sampling (T = 0.8, k = 4 samples per problem). Model: Qwen2.5-1.5B-Instruct.

                                                            Greedy Pass@1          Sampled Pass@1 (T = 0.8)
                        0.0 (Baseline) 0.5270 ± 0.0103                                   0.4223 ± 0.0064
                        0.3              0.5380 ± 0.0129                                 0.4878 ± 0.0117
                        0.7              0.5660 ± 0.0102                                 0.5137 ± 0.0153
         Under review as1a conference paper
                                        0.5710   ± 0.0058
                                            at ICLR 2027                                 0.5235 ± 0.0093
                        1.5              0.5540 ± 0.0073                                 0.5215 ± 0.0106
                        2                0.5490 ± 0.0058                                 0.5170 ± 0.0041
                        3                0.5340 ± 0.0049                                 0.5095 ± 0.0100
                        6                0.5380 ± 0.0103                                 0.5148 ± 0.0033
1458
1459
1460                                                      Effect of Entropy Regularization on MBPP
1461                                           0.58
1462                                           0.56
1463                                           0.54
                             Pass@1 Coverage




1464
                                               0.52
1465
1466                                           0.50
1467                                           0.48
1468                                           0.46
1469                                                                           Best per curve
                                               0.44                            CE baseline ( = 0)
1470                                                                           Greedy Pass@1 (5 seeds)
                                               0.42                            Sampled Pass@1, T = 0.8, k = 4 (5 seeds)
1471
1472                                                  0       1       2        3                                    6
                                                                    Lambda (Entropy Penalty)
1473
1474   Figure  5: 5:
                   MBPP
          Figure     MBPPPass@1
                            Pass@1under
                                     undergreedy
                                           greedydecoding
                                                   decodingand
                                                            and under   temperaturesampling
                                                                 under temperature   sampling(T(T==0.8,
                                                                                                     0.8,k k==4)4)
1475   versus  entropy  penalty
          versus  entropy penaltyλ.λ.Dashed
                                      Dashedlines
                                              linesmark
                                                    markeach
                                                         eachcurve’s
                                                               curve’s cross-entropy
                                                                       cross-entropy baseline; stars
                                                                                               stars mark
                                                                                                     markeacheach
1476   curve’s  best
          curve’s    λ.λ.Error
                   best   Errorbars  show±1
                                barsshow   ±1standard   deviationover
                                               standard deviation  over55seeds.
                                                                           seeds.
1477
1478
1479                                                                      31
1480
1481     Table 7:     MBPP Pass@1 accuracy under varying entropy penalties, under greedy decod-
       Table 8: Detailed per-seed sampled Pass@1 accuracy on MBPP at T = 0.8 with k = 4 samples per
       problem, using Qwen2.5-1.5B-Instruct.

                                                                     Individual Seeds                                          Aggregate
            Entropy Penalty (λ)                      Seed 0       Seed 1     Seed 2      Seed 3         Seed 4          Mean       Std. Dev.
           0.0 (Baseline)          0.4113 0.4300 0.4238                                   0.4200        0.4263        0.4223        ±0.0064
           0.3                     0.5038 0.4688 0.4950                                   0.4863        0.4850        0.4878        ±0.0117
           0.7                     0.5413 0.5175 0.5100                                   0.4975        0.5025        0.5138        ±0.0153
           1                       0.5312 0.5250 0.5100                                   0.5350        0.5162        0.5235        ±0.0093
         Under
           1.5 review as a conference paper at0.5175
                                   0.5125       ICLR 2027
                                                      0.5100                              0.5300        0.5375        0.5215        ±0.0106
           2                       0.5212 0.5138 0.5225                                   0.5150        0.5125        0.5170        ±0.0041
           3                       0.5125 0.5050 0.5162                                   0.4925        0.5212        0.5095        ±0.0100
           6                       0.5175 0.5138 0.5162                                   0.5175        0.5088        0.5148        ±0.0033
1512
1513
1514
1515                                                      Effect of Entropy Regularization on MATH
1516
                                              0.48
1517
1518                                          0.46
                            Pass@1 Coverage




1519
                                              0.44
1520
1521                                          0.42
1522
                                              0.40
1523
                                              0.38                                  Best per curve
1524                                                                                CE baseline ( = 0)
1525                                                                                Greedy Pass@1 (3 seeds)
                                              0.36                                  Sampled Pass@1, T = 0.8, k = 4 (3 seeds)
1526
1527
                                                      0       1      2              4                                    8
                                                                         Lambda (Entropy Penalty)
1528
1529 Figure  6: 6:
                MATH
        Figure     MATHPass@1
                           Pass@1under
                                   undergreedy
                                          greedydecoding
                                                 decodingand
                                                           and under temperaturesampling
                                                               under temperature  sampling(T(T==0.8,
                                                                                                  0.8,k k==4)4)
1530 versus entropy  penalty   λ for Qwen2.5-7B-Instruct.      Dashed  lines mark each curve’s
        versus entropy penalty λ for Qwen2.5-7B-Instruct. Dashed lines mark each curve’s cross-cross-entropy
1531 baseline;
        entropystars mark stars
                 baseline;  each mark
                                  curve’s best
                                       each    λ. Error
                                             curve’s bestbars      ±1 standard
                                                              show bars
                                                          λ. Error       show ±1deviation  over 3 seeds.
                                                                                  standard deviation  over 3
1532    seeds.
1533
1534
       Table 9: MATH Pass@1 accuracy under varying entropy penalties, under greedy decoding and under
1535
       temperature sampling (T = 0.8, k = 4 samples per problem). Model: Qwen2.5-7B-Instruct.
1536
1537
                                                            Greedy Pass@1               Sampled Pass@1 (T = 0.8)
1538
1539     Table 9: MATH 0.0
                        Pass@1    accuracy0.4200
                             (Baseline)     under varying entropy penalties,
                                                   ± 0.0071          0.3696 under  greedy decoding and under
                                                                             ± 0.0121
1540
         temperature sampling
                        1      (T  = 0.8, k  = 4 samples
                                           0.4583 ± 0.0062per problem). Model:  Qwen2.5-7B-Instruct.
                                                                     0.4179 ± 0.0097
1541                    2                  0.4400 ± 0.0163           0.4350 ± 0.0041
1542                    4                    Greedy Pass@1
                                          0.4717 ± 0.0118       Sampled  Pass@1
                                                                     0.4496       (T = 0.8)
                                                                             ± 0.0048
1543                                        0.4200±±0.0143
                        8 0.0 (Baseline) 0.4667       0.0071         0.3696 ±
                                                                    0.4675     0.0145
                                                                             ± 0.0121
1544                      1                 0.4583 ± 0.0062          0.4179 ± 0.0097
1545                      2                 0.4400 ± 0.0163          0.4350 ± 0.0041
1546                      4                 0.4717 ± 0.0118          0.4496 ± 0.0048
                                                         32
1547                      8                 0.4667 ± 0.0143          0.4675 ± 0.0145
1548
1549
Table 10: Detailed per-seed sampled Pass@1 accuracy on MATH at T = 0.8 with k = 4 samples per
problem, using Qwen2.5-7B-Instruct.

                                       Individual Seeds           Aggregate
              Entropy Penalty (λ)   Seed 0   Seed 1   Seed 2   Mean     Std. Dev.
              0.0 (Baseline)        0.3525   0.3775   0.3787   0.3696    ±0.0121
              1                     0.4175   0.4300   0.4062   0.4179    ±0.0097
              2                     0.4300   0.4400   0.4350   0.4350    ±0.0041
              4                     0.4450   0.4475   0.4562   0.4496    ±0.0048
              8                     0.4475   0.4813   0.4738   0.4675    ±0.0145




                                              33
        Under review as a conference paper at ICLR 2027




1566
       H Renyi Order Ablation
        H R ENYI O RDER A BLATION
1567
       Section 4 derives the entropy penalty from the family Sα and then selects α = 1, and Theorem B.4
1568    Section
       proves    4 derives the entropy
              PAC-learnability     for thepenalty
                                            Sα lossfrom  theafamily
                                                     along           Sα α
                                                              sequence    m ↓then
                                                                        and       selects
                                                                              0, with      α = 1, B.5
                                                                                        Corollary  and instantiating
                                                                                                       Theorem B.4
1569    proves
       αm       PAC-learnability
            = 1/m.    The theoryfor     the Sα loss
                                     therefore        along
                                                 points      a sequence
                                                          toward         αm ↓ 0,end
                                                                   the small-α     with
                                                                                      of Corollary  B.5where
                                                                                          the family,   instantiating
                                                                                                              log Sα
1570    αm = 1/m.
       approaches   log The theorywhile
                        |supp(·)|,   therefore  points toward
                                           the objective         the small-α
                                                           we actually  train end
                                                                               withofsits
                                                                                      the at
                                                                                           family,   Thislog
                                                                                             α = 1.where      Sα ap-
                                                                                                           appendix
1571    proaches
       asks       log |supp(·)|,
            what the               while the
                       order parameter        objective
                                           buys          we actually train with sits at α = 1. This appendix asks
                                                 empirically.
1572    what the order parameter buys empirically.
1573   H.1 Objective and Protocol
1574    H.1 O BJECTIVE AND P ROTOCOL
1575   We train with
        We train with                                                                           1       X
1576                                            L = CE + λ Rα ,                 Rα (p) =             log X p(y)α ,
                                                                                              1 − 1α               α
1577                                           L = CE + λ Rα ,                  Rα (p) =               log
                                                                                                         y    p(y) ,
                                                                             y
                                                                                                1−α
1578   evaluated in log space as logsumexp(α log p)/(1 − α) for numerical stability,  with R1 taken to be
1579     evaluated
       the Shannoninentropy,    as logsumexp(α
                     log spacerecovering the mainlog p)/(1 −exactly.
                                                   objective α) for numerical
                                                                     We sweepstability,  0.25,R0.5,
                                                                               α ∈ {0.1,with   1 taken
                                                                                                    1, 2}toand
                                                                                                            be
1580   λ the Shannon
          ∈ {0, 1, 3, 8}.entropy,
                            At λ = recovering      the is
                                       0 the penalty   main    objective
                                                          switched          exactly.
                                                                       off and   the objective         ∈ {0.1,for
                                                                                      We sweepisαidentical      0.25, 0.5,α,
                                                                                                                    every   1, 2}
                                                                                                                               so
1581     and  λ  ∈ {0,   1, 3, 8}.   At  λ =  0 the penalty   is
       that point is trained once and shared across all curves.  switched    off  and the   objective is identical for every   α,
1582     soEverything
            that point iselsetrained   once  and  shared  across   all curves.
                                  follows Appendix C: GSM8K, Qwen2.5-1.5B-Instruct, the same LoRA con-
1583   figuration
         Everything andelsehyperparameters,
                               follows Appendix   greedy   Pass@1. Qwen2.5-1.5B-Instruct,
                                                      C: GSM8K,        Two differences from Table 1 aretheworth    samestating,
                                                                                                                           LoRA
1584   because   they    shift  the  absolute   numbers:    this  sweep   uses  200  evaluation    problems
         configuration and hyperparameters, greedy Pass@1. Two differences from Table 1 are worth stating,    rather  than   500,
1585   and  3 seeds
         because      rather
                   they   shiftthan    5. The cross-entropy
                                  the absolute   numbers: thisbaseline
                                                                  sweep accordingly      reads 0.4717
                                                                           uses 200 evaluation           ± 0.0062
                                                                                                   problems        here
                                                                                                               rather    against
                                                                                                                      than  500,
1586     and 3±
       0.4912   seeds
                  0.0154rather   than 5.1.The
                            in Table           cross-entropy
                                           Comparisons          baseline
                                                           within          accordingly
                                                                    this appendix     are reads 0.4717±0.0062
                                                                                           internally               here against
                                                                                                      consistent; they    should
1587     0.4912
       not       ± 0.0154
            be read    against in the
                                   Table  1. Comparisons
                                       main-paper    tables.within this appendix are internally consistent; they should
1588    not be read against the main-paper tables.
1589   H.2 Results
1590    H.2 R ESULTS
1591
1592                                                       Renyi Order on GSM8K (Greedy Pass@1)
1593                                           0.6
1594
1595
                                               0.5
1596
                             Pass@1 Coverage




1597
1598                                           0.4
1599
1600                                           0.3
1601
1602                                                     CE baseline (0.4717)       = 0.5
                                                          = 0.1                     = 1 (Shannon)
1603
                                               0.2        = 0.25                    =2
1604                                                 0        1                 3                                      8
1605                                                                        Lambda (Entropy Penalty)
1606
1607   Figure
         Figure7:7:Greedy
                    Greedy Pass@1
                             Pass@1 on
                                     on GSM8K for five  five Renyi
                                                             Renyiorders
                                                                    ordersacross
                                                                            acrosspenalty
                                                                                    penalty  strengths.
                                                                                          strengths. TheThe  dashed
                                                                                                         dashed  line
1608     is the
       line     cross-entropy
             is the            baseline,
                    cross-entropy        which
                                   baseline,    all curves
                                              which   all curves   at λ =at
                                                             share share  0. λError
                                                                               = 0.bars show
                                                                                     Error     ±1show
                                                                                            bars        ±1 standard
                                                                                                  standard deviation
1609     over 3 seeds.
       deviation          seeds. α
                   over 3Orders    ∈ {0.5,
                                 Orders  α ∈1,{0.5,
                                               2} are  mutually
                                                    1, 2}         indistinguishable;
                                                           are mutually               α = 0.1
                                                                         indistinguishable;  α =never separates
                                                                                                 0.1 never      from
                                                                                                           separates
1610     the baseline
       from            and α
              the baseline    =α
                            and  0.25 collapses
                                   = 0.25        at λ at
                                           collapses   = λ8.= 8.
1611
1612    Orders in [0.5, 2] are one curve. Taking the largest minus the smallest mean across α ∈
1613    {0.5, 1, 2} at each λ and comparing it to the pooled standard error of that difference gives 1.2σ
                                                      34
1614    at λ = 1, 1.0σ at λ = 3 and 0.6σ at λ = 8. The ordering is not even stable: α = 1 is highest at
1615    λ = 1 and λ = 8 but lowest at λ = 3. Within this range the Renyi order is not a meaningful design
1616    choice at three seeds.
Table 11: Greedy Pass@1 on GSM8K by Renyi order α and penalty strength λ, aggregated over 3
seeds. The λ = 0 baseline (0.4717 ± 0.0062) is shared by all orders.

                                      λ=1                λ=3                λ=8
             α = 0.1             0.4700 ± 0.0082    0.4883 ± 0.0225    0.4483 ± 0.0062
             α = 0.25            0.4733 ± 0.0232    0.5133 ± 0.0366    0.1883 ± 0.0085
             α = 0.5             0.5450 ± 0.0071    0.5717 ± 0.0143    0.5717 ± 0.0103
             α = 1 (Shannon)     0.5517 ± 0.0287    0.5600 ± 0.0147   0.5800 ± 0.0212
             α=2                 0.5283 ± 0.0155    0.5733 ± 0.0170    0.5750 ± 0.0122


Orders in [0.5, 2] are one curve. Taking the largest minus the smallest mean across α ∈ {0.5, 1, 2}
at each λ and comparing it to the pooled standard error of that difference gives 1.2σ at λ = 1, 1.0σ
at λ = 3 and 0.6σ at λ = 8. The ordering is not even stable: α = 1 is highest at λ = 1 and λ = 8
but lowest at λ = 3. Within this range the Renyi order is not a meaningful design choice at three
seeds.

Orders below 0.5 fail. At λ = 1, α = 0.1 reaches 0.4700 and α = 0.25 reaches 0.4733, both
indistinguishable from the un-regularized baseline of 0.4717. At λ = 8, α = 0.25 collapses to 0.1883,
roughly 28 points below baseline, consistently across all three seeds.

The failure is not a numerical artifact. For α < 1 the sum y p(y)α up-weights the tail of
                                                                    P
the distribution, and with |Y| = 151,936 one might worry that at small α the penalty reads the
softmax’s numerical  floor rather than the model’s support. We measured this directly, recording
                     α
              P
the share of y p(y) contributed by tokens outside the top 100. At α = 0.25 that share is 0.053,
0.032 and 0.016 at λ = 1, 3, 8; at α = 0.1 it is 0.480, 0.414 and 0.359. The order that fails most
dramatically, α = 0.25, is the one whose penalty is almost entirely determined by the head of the
distribution. Whatever is going wrong at small α is a property of the objective, not of floating-point
arithmetic.

H.3    Reconciliation With Theorem B.4
These results do not contradict Theorem B.4; they locate the regime in which its constants bind.
The theorem requires αm ↓ 0 and λm ↑ ∞ jointly with the sample size, and its guaranteeis mediated
by Lemma B.3, which bounds the gap between |supp(p)| and Sα (p) by 1 − η α/(1−α) /η, with a
sample complexity scaling as 1/η 2 . In the LLM setting, the softmax assigns no exact zeros, so the
effective η is the smallest probability the model represents and 1/η is astronomically large. The
sample sizes at which the small-α guarantees become operative are therefore far beyond anything
reachable here, and at a fixed finite α and finite m the theorem makes no prediction about which
order should perform better.
    The practical reading is that α = 1 is not a compromise forced on us by tractability. It sits
inside the range that works, and the end of the family the theory idealizes is empirically the worse
end. Shannon entropy is both the convenient choice and, over the orders we tested, an effective one.

H.4    Limitations
Three caveats. This is one model on one dataset at three seeds, so the conclusion that α ∈ [0.5, 2] is
a plateau should be read as an absence of evidence for an ordering rather than evidence of exact


                                                   35
equivalence. The α = 0.1 runs exhibited pre-clipping gradient norms of 7 to 10 against a clipping
threshold of 1.0, roughly an order of magnitude above the other configurations, so the cross-entropy
component of the gradient was attenuated and those cells were effectively optimized under a different
regime; part of their deficit may be attributable to that rather than to the order itself. Finally, we
have not diagnosed the mechanism of the α = 0.25, λ = 8 collapse, and we report it as an observed
instability rather than as a characterized failure mode.




                                                 36
         Under review as a conference paper at ICLR 2027




1674   I I Answer-Only    Negative Control
            A NSWER -O NLY N EGATIVE C ONTROL
1675
1676
       Our account of why the entropy penalty helps is specific: it withdraws probability mass from outputs
       theOur  account
            verifier     of why
                      rejects,    the entropy
                                which    matters  penalty
                                                    only whenhelps the
                                                                    is specific: it withdraws
                                                                         demonstrated           probability
                                                                                            answer  is one ofmass
                                                                                                               manyfrom  outputs
                                                                                                                     acceptable
1677      the verifier  rejects,  which    matters    only    when   the  demonstrated      answer  is one  of many   acceptable
       ones. If the correct set is a singleton, cross-entropy already concentrates all mass on the single
1678      ones. If the correct set is a singleton, cross-entropy already concentrates all mass on the single
       acceptable output and a support penalty has nothing left to correct. The theory therefore makes a
1679      acceptable output and a support penalty has nothing left to correct. The theory therefore makes a
       falsifiable prediction - no real gain when the demonstrated answer is the only accepted one - and
1680      falsifiable prediction - no real gain when the demonstrated answer is the only accepted one - and this
       this  appendix
          appendix       tests
                      tests it. it.
1681
            We test it by removing the chain of thought from GSM8K. The model is trained to emit the
1682      Wenumber
               test it by  removing
       final            and   nothing the
                                        else,chain
                                              so the of target
                                                         thought is from   GSM8K.
                                                                    the unique         The answer
                                                                                  correct    model rather
                                                                                                    is trained to one
                                                                                                            than  emitderivation
                                                                                                                        the final
1683      number    and nothing    else, else
                                          so the
       among     many.    Everything           is target   is the unique
                                                  held fixed:     the same correct  answer
                                                                              dataset,    therather
                                                                                              same than   one derivation among
                                                                                                     Qwen2.5-1.5B-Instruct
1684      many.    Everything     else  is held   fixed:    the  same   dataset,   the  same   Qwen2.5-1.5B-Instruct
       model, the same LoRA configuration and hyperparameters, the same λ grid, the same five seeds, the
1685      model,
       same        the same
              trainer,         LoRAgreedy
                        the same       configuration      and hyperparameters,
                                              Pass@1 verifier,      the same 1,000        same λand
                                                                                     thetraining grid,500
                                                                                                        theevaluation
                                                                                                            same five seeds,  the
                                                                                                                       problems.
1686      same trainer, the same greedy Pass@1 verifier, the same 1,000 training and 500 evaluation problems.
       The only difference from Section 5.1 is the format of the target.
1687     The only difference from Section 5.1 is the format of the target.
1688
1689                                             Entropy Regularization With and Without a Chain of Thought (GSM8K)
1690
                                                        Answer-only accuracy                                                         Change from each regime's own baseline
1691                          0.14                                                         Change from baseline (points)   10
1692                                                                                                                        8
                              0.12
1693                                                                                                                        6
            Pass@1 Coverage




1694                          0.10                                                                                          4
1695                                                                                                                        2
1696                          0.08                                                                                          0
1697                                                                                                                        2
                              0.06                                                                                          4
1698                                     CE baseline (0.1120)                                                                       Chain of thought (Table 1)
                                         Answer-only                                                                        6       Answer-only
1699
                                     0      1       2        3     4               6   8                                        0      1        2        3       4             6   8
1700                                                    Lambda (Entropy Penalty)                                                                    Lambda (Entropy Penalty)
1701
1702 Figure
       Figure8:8:GSM8K
                    GSM8Kwith   withand
                                      andwithout
                                            withoutaa chain
                                                       chain of
                                                             of thought.
                                                                 thought. Left: answer-only greedy Pass@1 against   against
1703   theentropy
     the    entropypenalty,
                      penalty,withwithits
                                       its cross-entropy
                                           cross-entropy baseline
                                                           baseline dashed.
                                                                      dashed. Right: change
                                                                                      change from
                                                                                               from each
                                                                                                      each regime’s
                                                                                                             regime’s own
                                                                                                                       own
1704   baseline,
     baseline,  so so
                    thethe
                         twotwocan can  be compared
                                   be compared          despite
                                                   despite very very    different
                                                                  different       absolute
                                                                            absolute        accuracies.
                                                                                     accuracies.            The chain-of-
                                                                                                   The chain-of-thought
       thought
1705 curve   risescurve    rises monotonically
                    monotonically                  to +9.04
                                       to +9.04 points;    thepoints;   the answer-only
                                                                 answer-only              curve
                                                                                curve is flat    is flat λthrough
                                                                                              through       = 4 and λ then
                                                                                                                      = 4
       and   then  falls  to  −5.60.   Error  bars  show  ±1   standard   deviation over  5 seeds,  and
1706 falls to −5.60. Error bars show ±1 standard deviation over 5 seeds, and on the right the standard    on  the right the
       standard    error  of  the difference
1707 error of the difference from baseline.
                                              from   baseline.
1708
1709    Table 12: GSM8K answer-only greedy Pass@1 under varying entropy penalties, aggregated over 5
1710    seeds, with
       Results.     theanswer-only
                  The   change frombaseline
                                    the cross-entropy baseline
                                            reaches 0.1120.    in percentage
                                                             Accuracy  drifts points (95%through
                                                                              up slightly Welch interval).
                                                                                                 λ = 2, by
1711 +1.68 points with a 95% interval of [+0.48, +2.88], which does not survive correction for the eight
                          λ and which we do Pass@1
1712 comparisons in the sweep                                     Change
                                                 not claim as an effect.    (95%falls
                                                                         It then  CI) sharply: −3.88 points
1713 [−5.80, −1.96] at λ =0.0
                           6 and −5.60 points
                              (Baseline)        [−6.89,
                                           0.1120       −4.31] at λ = 8, halving
                                                   ± 0.0097                —       accuracy relative to the
1714 cross-entropy baseline.
                          0.3This stark  contrast relative to the clear  advantage
                                           0.1164 ± 0.0067 +0.44 [−0.72, +1.60]     entropy penalties gave
1715 the reasoning model provides
                          0.5      evidence0.1204
                                             that the  penalty works
                                                   ± 0.0067     +0.84due    to the
                                                                        [−0.32,    mechanism in Section 3.
                                                                                 +2.00]
1716                                                 1.0                      0.1244 ± 0.0066                                   +1.24 [+0.09, +2.39]
1717                                                 2.0                      0.1288 ± 0.0074                                   +1.68 [+0.48, +2.88]
1718                                                 3.0                      0.1212 ± 0.0047                                   +0.92 [−0.14, +1.98]
1719
                                                     4.0                      0.1148 ± 0.0148                                   +0.28 [−1.45, +2.01]
                                                     6.0                      0.0732 ± 0.0170                                   −3.88 [−5.80, −1.96]
1720
                                                     8.0                      0.0560 ± 0.0089                                   −5.60 [−6.89, −4.31]
1721
1722                                                                                   37
1723     Results. The answer-only baseline reaches 0.1120. Accuracy drifts up slightly through λ = 2, by
1724     +1.68 points with a 95% interval of [+0.48, +2.88], which does not survive correction for the eight
1725     comparisons in the sweep and which we do not claim as an effect. It then falls sharply: −3.88 points
Table 12: GSM8K answer-only greedy Pass@1 under varying entropy penalties, aggregated over 5
seeds, with the change from the cross-entropy baseline in percentage points (95% Welch interval).

                     λ                   Pass@1          Change (95% CI)
                     0.0 (Baseline)   0.1120 ± 0.0097           —
                     0.3              0.1164 ± 0.0067   +0.44 [−0.72, +1.60]
                     0.5              0.1204 ± 0.0067   +0.84 [−0.32, +2.00]
                     1.0              0.1244 ± 0.0066   +1.24 [+0.09, +2.39]
                     2.0              0.1288 ± 0.0074   +1.68 [+0.48, +2.88]
                     3.0              0.1212 ± 0.0047   +0.92 [−0.14, +1.98]
                     4.0              0.1148 ± 0.0148   +0.28 [−1.45, +2.01]
                     6.0              0.0732 ± 0.0170   −3.88 [−5.80, −1.96]
                     8.0              0.0560 ± 0.0089   −5.60 [−6.89, −4.31]




                                               38
J    LLM Disclosure
LLMs were used in 3 primary ways. The first is essentially all experiments were set up and
instantiated with LLM coding. We had a separate LLM check for correctness of the code. The
second is when the paper was drafted, we repeatedly asked LLMs to critique and we incorporated
its feedback if we deemed it to be appropriate. The third was finding related papers. We read all of
these before ever citing them to confirm the relation to our work.




                                                39
