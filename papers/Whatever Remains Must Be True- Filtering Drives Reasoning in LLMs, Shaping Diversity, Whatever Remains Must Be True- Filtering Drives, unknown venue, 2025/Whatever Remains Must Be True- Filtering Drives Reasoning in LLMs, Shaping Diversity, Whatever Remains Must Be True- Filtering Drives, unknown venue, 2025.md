                                                                                                                                                 March, 2026




                                        Whatever Remains Must Be True: Filtering Drives
                                        Reasoning in LLMs, Shaping Diversity
                                        Germán Kruszewski1,* Pierre Erbacher1,* Jos Rozen1 Marc Dymetman2
                                        1 NAVER Labs Europe    2 Independent Researcher

                                        * Equal contribution


                                        {german.kruszewski,pierre.erbacher,jos.rozen}@naverlabs.com                 marc.dymetman@gmail.com


                                        Abstract

                                        Reinforcement Learning (RL) has become the de facto standard for tuning LLMs to solve tasks involving
arXiv:2512.05962v2 [cs.LG] 6 Mar 2026




                                        reasoning. However, growing evidence shows that models trained in such way often suffer from a
                                        significant loss in diversity. We argue that this arises because RL implicitly optimizes the “mode-
                                        seeking” or “zero-forcing” Reverse KL to a target distribution causing the model to concentrate mass on
                                        certain high-probability regions of the target while neglecting others. In this work, we instead begin
                                        from an explicit target distribution, obtained by filtering out incorrect answers while preserving the
                                        relative probabilities of correct ones. Starting from a pre-trained LLM, we approximate this target
                                        distribution using the 𝛼-divergence family, which unifies prior approaches and enables direct control of
                                        the precision–diversity trade-off by interpolating between mode-seeking and mass-covering divergences.
                                        On a Lean theorem-proving benchmark, our method achieves state-of-the-art performance along the
                                        coverage–precision Pareto frontier, outperforming all prior methods on the coverage axis.



                                        1. Introduction
                                              “How often have I said to you that when you have eliminated the impossible, whatever remains,
                                              however improbable, must be the truth?”
                                                                                                           — Arthur Conan Doyle, The Sign of Four
                                        Large Language Models (LLMs) have made striking progress on reasoning tasks. A leading approach is Reinforce-
                                        ment Learning from Verifiable Rewards (RLVR) [16, 31], where policy-gradient methods such as PPO [49] or
                                        GRPO [50] optimize against a reward that combines a binary verifier of correctness with a KL penalty to keep the
                                        tuned model close to its base distribution.
                                        While RLVR has been credited with enabling exploration of new solutions [16], recent studies challenge this
                                        view. In particular, they find that base models already contain these solutions given a sufficient sampling budget,
                                        and that tuned models often exploit additional samples less effectively due to reduced output diversity [14,19,
                                        60,67]. Earlier, with RLHF [9,70], similar diversity reductions were observed, sometimes described as “mode
                                        collapse” [27,42].
                                        We argue that this loss of diversity stems from the implicit objective of RL-based training: optimizing the Reverse KL
                                        divergence to a target distribution that favors correct answers [30]. Reverse KL is “mode-seeking” or “zero-forcing,”
                                        emphasizing precision on a subset of solutions while ignoring others [5,23,33]. This explains why RLVR models
                                        become accurate but less diverse.
                                        To address this, we explicitly define the desired target distribution: one that always outputs correct solutions while
                                        remaining as close as possible to the base model, thus preserving any solution included therein [25,26]. Direct
                                        sampling is infeasible, but we can approximate it with an autoregressive policy using Distributional Policy Gradient
                                        Algorithms [DPG 18,25,43]. Concretely, we apply 𝑓 -DPG [18], which minimizes an 𝑓 -divergence [45] to this target.
                                        Different divergences trade off precision (probability of sampling a correct solution) and coverage (probability of
                                        sampling at least one correct solution given a sufficiently large sampling budget): Reverse KL emphasizes the
                                        Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



                                                                                                                                                                                                                                     Pareto Frontier
Precision

                                         Reverse KL ( 1)                                                                                                                                                                              -DPG models
                                      Mode-seeking, less diversity                                                                                                     -DPG ( =0.25)                                                 Baseline methods
                             GRPO                                    Target distribution                                                                             -DPG ( =0)
                                                                     Model distribution                            0.88
                                                                                                                                     GRPO-Pass@k
                                                                                                                                                             GRPO (High-KL)
                                                                                                                                  Base SFT                                                  -DPG ( =0.75)




                                                                                             Coverage (pass@256)
                                                                                                                                                                             -DPG ( =0.5)                     GRPO-Rw-Ulkly
                                            Balanced ( = 0.5)
-divergence trade-off




                                                Trade-off                                                          0.86
                                                                                                                                                                                                            -DPG ( =0.9)        -DPG ( =0.96)
                              -DPG                                   Target distribution
                                                                     Model distribution                                                                                                                              -DPG ( =0.95)
                                                                                                                                                                                                                        ReMax
                                                                                                                   0.84
                                                                                                                                                                                                                   -DPG ( =0.98)       -DPG ( =0.997)
                                           Forward KL ( 0)
                                      Mass-covering, more diversity                                                                                                                                                -DPG ( =0.99)     -DPG ( =0.995)
                             RS-FT/KL-DPG                            Target distribution                                                                                                                                  -DPG ( =0.97)
                                                                     Model distribution                            0.82
                                                                                                                                                                                                                                     -DPG ( =0.999)
Diversity




                                                                                                                                                                                                                            RLOO
                                                                                                                                                                                                                          GRPO        GPG
                                                                                                                          0.550              0.575   0.600           0.625             0.650           0.675            0.700           0.725
                                                                                                                                                                             Precision (pass@1)


 Figure 1: Left: Illustration of our method. RLVR policy-gradient approaches (e.g., GRPO, PPO) concentrate
 probability on a narrow region of the target distribution, while methods like KL-DPG increase diversity but allocate
 mass to low-quality regions. 𝛼-DPG balances these extremes. Right: Model precision (pass@1) and coverage
 (pass@256). The Pareto frontier is the upper-right boundary of the convex hull; the shaded band shows one
 bootstrap standard deviation. 𝛼-DPG and baseline models lie along the frontier, with 𝛼-DPG achieving the highest
 coverage and precision for low and high values of 𝛼, respectively.


 former, Forward KL the latter [5]. To interpolate between them, we introduce 𝛼-DPG, based on 𝛼-divergences [3,
 12,48]. Notably, this method unifies RLVR (Reverse KL) and both KL-DPG [18,25,43] and Rejection Sampling
 Fine-Tuning (Forward KL) [65,68] under a single umbrella. We call this approach Distributional Matching with
 Verifiable Rewards (DMVR), positioning it under the general framework of Distributional Matching [25,29,30].
  We evaluate 𝛼-DPG in Lean, a proof assistant that automatically verifies formal mathematical proofs.In this setting,
  success requires not only correct candidates but also diversity across proof attempts, since harder theorems may
  be solvable only through rare derivations. We find that 𝛼-DPG achieves state-of-the-art performance, producing
  models that lie on the Pareto frontier between precision (pass@1) and coverage (pass@256), and that surpass
  prior methods in coverage1 .

   Contributions.
                        • We introduce the DMVR framework, which trains models by approximating an explicitly defined verifier-
                          based target distribution.
                        • We clarify how the implicit dynamics of RL-based methods lead to reduced diversity.
                        • We highlight the role of the divergence family in trading off precision and diversity, and propose 𝛼-DPG to
                          smoothly interpolate between Forward and Reverse KL.
                        • We show on the Lean benchmark that 𝛼-DPG achieves results along a Pareto coverage-precision frontier,
                          with the 𝛼 parameter allowing to trade-off between precision and coverage. Moreover, 𝛼-DPG achieves the
                          best coverage results among all considered methods when using low values of 𝛼.

   2. Background
 Reinforcement Learning with Verifiable Rewards (RLVR) Let 𝜋𝜃 (·| 𝑥 ) : Y → ℝ be an LLM with parameters 𝜃
 defining a probability distribution over sequences 𝑦 ∈ Y conditioned on a prompt 𝑥 . A verifier 𝑣 ( 𝑦, 𝑥 ) ∈ {0, 1} is a
 binary function that discriminates between correct and incorrect responses to 𝑥 . Given a dataset D of prompts
 (and, optionally, ground-truth answers for the verifier), RLVR uses a standard reinforcement learning objective
 derived from previous work on Reinforcement Learning from Human Feedback (RLHF) [9,70]:

                                                                                    JRLVR = arg max 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 (· | 𝑥 ) 𝑅𝜃 ( 𝑦, 𝑥 ) ,                                                                                                          (1)
                                                                                                                          𝜃

                        1We make the code available at https://github.com/naver/alpha-dpg.




                                                                                                                                                                                                                                                        2
                     Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



where the “pseudo-reward” [30] 𝑅𝜃 is defined as follows:

                                                                                         𝜋𝜃 ( 𝑦 | 𝑥 )
                                                     𝑅𝜃 ( 𝑦, 𝑥 ) = 𝑣 ( 𝑦, 𝑥 ) − 𝛽 log                   .                                                 (2)
                                                                                        𝜋base ( 𝑦 | 𝑥 )

Here, 𝜋base is the base LLM and 𝛽 is a tunable parameter that controls the trade-off between maximizing the reward
and minimizing divergence from the original model. Some authors fall back to setting 𝛽 = 0, just optimizing the
expected verifier reward [38,39,64].

Policy Gradient (PG) Algorithms We can maximize Eq. 2 following multiple algorithms. One of the simplest
ones is KL-Control [24,57], with the following gradient

                                         ∇𝜃 JKL-Control ( 𝜃) = 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 𝐴ˆ( 𝑦, 𝑥 )∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) ,                                               (3)

where 𝐴ˆ( 𝑦, 𝑥 ) = 𝑅𝜃 ( 𝑦, 𝑥 ) − 𝐵 ( 𝑥 ) is the advantage function and 𝐵 ( 𝑥 ) is a baseline that doesn’t depend on 𝑦 to keep
the objective unbiased used for variance reduction [53, Chapter 2, Section 7]. Some options for an unbiased
baseline could include a constant, a critic [54], or a leave-one-out average in a batch of rewards [RLOO; 1,28]2 .
When 𝛽 = 0, Eq. 3 reduces to the original policy gradient algorithm REINFORCE [59]. Another popular choice is
PPO [49], which optimizes the following clipped surrogate objective:
                                             " |𝑦|                                                                                                #
                                                                                                                                             
              J PPO ( 𝜃) = 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃𝑜𝑙𝑑           min 𝜌 ( 𝑦𝑡 | 𝑥, 𝑦<𝑡 ) 𝐴ˆ( 𝑦, 𝑥 ) , clip ( 𝜌 ( 𝑦𝑡 | 𝑥, 𝑦<𝑡 ) , 1 − 𝜖, 1 + 𝜖) 𝐴ˆ( 𝑦, 𝑥 )
                                              ∑︁
                                                                                                                                                      ,   (4)
                                              𝑡 =1

where 𝜌 ( 𝑦𝑡 | 𝑥, 𝑦<𝑡 ) = 𝜋𝜃 ( 𝑦𝑡 | 𝑥, 𝑦<𝑡 )/𝜋𝜃𝑜𝑙𝑑 ( 𝑦𝑡 | 𝑥, 𝑦<𝑡 ) is the ratio between the current and the previous policy token
probabilities and 𝜖 is a small hyperparameter. PPO discourages large policy updates that would move 𝜌 outside
the interval [1 − 𝜖, 1 + 𝜖], which improves training stability by constraining the new policy to be close to the old
one. GRPO [16] and other recent methods use the same clipping strategy, but differ in the form of the baseline.
While PPO is commonly understood to use a critic model as a baseline, GRPO uses the group-level reward average.

Distribution Matching (DM) DM [18,25,26,29,30] is a family of techniques for aligning LLMs to meet certain
constraints. For instance, let’s suppose that we want to constrain the LM so that all sequences 𝑦 meet 𝑟 ( 𝑥, 𝑦 ) = 1
for some binary filter 𝑟 ( 𝑥, 𝑦 ) ∈ {0, 1}3 . The method expresses this as a target distribution we want to approximate,
which in this case is given by
                                                  𝑝𝑥 ( 𝑦 ) ∝ 𝜋base ( 𝑦 | 𝑥 ) 𝑟 ( 𝑦, 𝑥 ) .                           (5)
This distribution is the only distribution 𝑝′ that fulfills the following two desirable conditions: (i) it satisfies the
constraint 𝑟 ( 𝑦, 𝑥 ) = 1, ∀ 𝑦 ∈ Supp( 𝑝′ (·| 𝑥 )), and (ii) it is the closest to 𝜋base (·| 𝑥 ) in terms of 𝐷KL ( 𝑝′ (·| 𝑥 )|| 𝜋base (·| 𝑥 )).
The second condition guarantees the preservation of all the diversity contained in the original model. In information
geometric terms, 𝑝𝑥 is the I-projection of 𝜋base (·| 𝑥 ) into the manifold of all distributions that satisfy the constraint
given by 𝑟 [13].

Distributional Policy Gradient (DPG) Algorithms Given a target distribution, we can optimize an autoregressive
policy 𝜋𝜃 to approximate it. Khalifa et al. [25] used for this the DPG algorithm [29,30,43], later denoted KL-
DPG [18], which minimizes the Forward KL 𝐷KL ( 𝑝𝑥 || 𝜋𝜃 ) to the target distribution 𝑝𝑥 :
                                                                                                    
                     DPG                                                              𝑝𝑥 ( 𝑦 )
                ∇𝜃 L     ( 𝜃) = ∇𝜃 𝔼𝑥 ∼D 𝐷KL ( 𝑝𝑥 || 𝜋𝜃 ) = −𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 (· | 𝑥 )                − 1 ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) . (6)
                                                                                     𝜋𝜃 ( 𝑦 | 𝑥 )

The negative one term acts as a constant baseline. Computing 𝑝𝑥 ( 𝑦 | 𝑥 ) requires estimating a normalization constant
denoted as the partition function, 𝑍 𝑥 , which can be estimated by importance sampling [41]. Note that in the
case of a binary constraint, 𝑍 𝑥 is the acceptance rate of the constraint when sampling from the base model [26]:
𝑍 𝑥 = 𝑦 ∈ Y 𝑎 ( 𝑦 | 𝑥 ) 𝑟 ( 𝑦, 𝑥 ) = 𝔼 𝑦 ∼𝑎 (· | 𝑥 ) 𝑟 ( 𝑦, 𝑥 ) = ℙ 𝑦 ∼𝑎 (· | 𝑥 ) [ 𝑟 ( 𝑦, 𝑥 ) = 1]. (See App. E for additional details.)
     Í

   2 Note that the average of all samples, as is used in GRPO, is biased instead.
   3 If the reader notices a strong similarity between a constraint 𝑟 ( 𝑥, 𝑦 ) and a verifier 𝑣 ( 𝑥, 𝑦 ), this is no coincidence: It is exactly this

connection that we will exploit in this paper.




                                                                                                                                                           3
                   Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Later, Go et al. [18] introduced 𝑓 -DPG, effectively generalizing this technique to any 𝑓 -divergence by minimizing
𝐷 𝑓 ( 𝜋𝜃 , 𝑝𝑥 ):

                 ∇𝜃 L 𝑓 -DPG ( 𝜃) = ∇𝜃 𝔼𝑥 ∼D 𝐷 𝑓 ( 𝜋𝜃 (·| 𝑥 )|| 𝑝𝑥 ) = 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 (· | 𝑥 ) − 𝐴ˆ 𝑓 ( 𝑦, 𝑥 )∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) ,          (7)
                                                                                                                            

                                                                               
where 𝐴ˆ 𝑓 ( 𝑦, 𝑥 ) = 𝑅𝜃𝑓 ( 𝑦, 𝑥 ) − 𝐵 ( 𝑥 ), 𝑅𝜃𝑓 ( 𝑦, 𝑥 )  − 𝑓 𝜋𝑝𝜃𝑥( (𝑦𝑦| 𝑥) ) is a “pseudo-reward”, 𝐵 ( 𝑥 ) is a context-dependent
                                                                ′


baseline, and 𝑓 is a convex function that parametrizes the 𝑓 -divergence where 𝑓 : (0, ∞) → ℝ s.t. 𝑓 (1) = 0. If
𝑝𝑥 ( 𝑦 ) = 0, then, 𝑅𝜃 ( 𝑦, 𝑥 ) = − 𝑓 (∞), where 𝑓 (∞)  lim𝑡→0 𝑡 𝑓 ( 1𝑡 ).
                      𝑓              ′                     ′




3. Distributional Matching with Verifiable Rewards (DMVR)
Here, we adopt the DM framework, and propose that the ideal target distribution for tuning a language model
𝜋base (·| 𝑥 ) to solve problems 𝑥 ∼ D by means of a verifier 𝑣 ( 𝑦, 𝑥 ) ∈ {0, 1} is simply the result of applying the verifier
as a binary constraint, i.e. 𝑟 ( 𝑦, 𝑥 ) = 𝑣 ( 𝑦, 𝑥 ), as follows:

                                                   𝑝𝑥 ( 𝑦 ) ∝ 𝜋base ( 𝑦 | 𝑥 ) 𝑣 ( 𝑦, 𝑥 ) ∀𝑥 ∈ D .                                          (8)

This distribution filters out all incorrect responses, leaving out only correct ones with the same relative probabilities as
the reference LLM. This is the single distribution that (i) always answers correctly to 𝑥 , and (ii) it is closest to the
base model 𝜋base as measured by 𝐷KL (·|| 𝜋base ) [25]. In the following discussion, we argue that (1) the distribution
approximated by RLVR is closely related, becoming equivalent to 𝑝𝑥 in the limit 𝛽 → 0, (2) for any fixed 𝛽 > 0,
RLVR optimizes the Reverse KL to a target distribution, which has a mode-seeking behavior, incentivizing the
policy to put high probability mass in small regions of high reward at the cost of diversity, and (3) we propose
an alternative based on 𝑓 -DPG parametrized with 𝛼-divergences to trade-off precision and diversity. Of these,
points (1) and (3) are original to our work, whereas point (2) is reproduced from Korbak et al. [30]. Moreover,
the target distribution and the 𝑓 -DPG technique to approximate it were defined in prior art [18,25].

3.1. From RLVR to DMVR
Consider the following lemma, reproducing the argument from Korbak et al. [30]:
Lemma 1. Define

                               1                                                              ∑︁
                                     𝜋base ( 𝑦 | 𝑥 ) exp 𝑣 ( 𝑦, 𝑥 )/ 𝛽 ,                            𝜋base ( 𝑦 | 𝑥 ) exp 𝑣 ( 𝑦, 𝑥 )/ 𝛽 .
                                                                                                                                    
              𝑝𝑥,𝛽 ( 𝑦 ) =                                                        𝑍𝑥 ( 𝛽) =
                             𝑍𝑥 ( 𝛽)                                                            𝑦


Then,

                                                                      1
                                                                                                       
                                                                                          𝜋𝜃 ( 𝑦 | 𝑥 )
                    ∇𝜃 𝔼𝑥 KL( 𝜋𝜃 ∥ 𝑝𝑥,𝛽 ) = −𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃               𝑣 ( 𝑦, 𝑥 ) − log                 ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )               (9)
                                           
                                                                      𝛽                  𝜋base ( 𝑦 | 𝑥 )
                                                                                                      
                                                                                                      
                                                   1
                                                                                                      
                                                                                        𝜋𝜃 ( 𝑦 | 𝑥 ) 
                                                = − 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 𝑣 ( 𝑦, 𝑥 ) − 𝛽 log                    ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) .            (10)
                                                                  
                                                   𝛽                                 𝜋base ( 𝑦 | 𝑥 ) 
                                                                  |               {z               }
                                                                           RLVR pseudo-reward
                                                                                                      
                                                                                                      
(Proof in App. B).
From Eq. 10, we can see that the gradient of the KL-Control’s objective (right-hand-side, optimizing the expected
RLVR pseudo-reward) is proportional to the gradient of the Reverse KL of 𝜋𝜃 to 𝑝𝑥,𝛽 (left-hand-side), up to a
negative constant that flips the direction of optimization. Therefore, maximizing the regularized reward implies
minimizing the divergence, and vice versa.
Furthermore, we note that the distribution 𝑝𝑥,𝛽 is a smooth approximation to the ideal distribution defined in Eq.
8, 𝑝𝑥 , converging to it as 𝛽 → 0+ :
Lemma 2.
                                                   lim 𝑝𝑥,𝛽 = 𝑝𝑥 .                                           (11)
                                                                 𝛽 →0

(Proof in App. C).



                                                                                                                                            4
                   Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



However, the gradient of the Reverse KL is dominated by − 1𝛽 ∇𝜃 𝔼 𝑦 ∼𝜋𝜃 [ 𝑣 ( 𝑦, 𝑥 )] (Eq. 9), revealing why minimizing
Reverse KL becomes an increasingly aggressive mode-seeking proxy for maximizing expected reward, at the cost
of diversity even if the diversity of responses is well-captured by the target 𝑝𝑥 . In the limit, with 𝛽 = 0, the Reverse
KL becomes undefined, the KL-Control algorithm reduces to plain REINFORCE, and no safeguard remains to
preserve diversity.

3.2. And back (as a special case of 𝛼-DPG)
Having defined the target distribution 𝑝𝑥 , we are left with the task of picking a divergence to train a policy 𝜋𝜃 to
approximate it. As we have seen, the Reverse KL 𝐷KL ( 𝜋𝜃 || 𝑝) implicitly employed by RLVR, is a mode-seeking or
zero-forcing divergence [5,23,34]. This means that it will penalize placing probability mass in regions where 𝑝
assigns little or none, but it is relatively indifferent to ignoring modes of 𝑝 altogether. As a result, the learned
policy tends to concentrate on a small subset of high-probability modes while disregarding other plausible regions
of the target distribution, which can reduce diversity and lead to brittle or degenerate behavior.
In contrast, the Forward KL, 𝐷KL ( 𝑝 ∥ 𝜋𝜃 ), is mass-covering. Here, the divergence becomes large whenever 𝜋𝜃
assigns insufficient probability to regions where 𝑝 has support, encouraging the policy to cover all modes of
the target distribution. While this can improve diversity and robustness, it often comes at the cost of assigning
non-negligible probability mass to low-reward or unlikely regions, leading to less precise approximations of the
target.
This tension between mode-seeking and mass-covering behavior motivates considering a broader family of
divergences. The 𝛼-divergences family [3,12,48] –a subfamily of 𝑓 -divergences– provides exactly such a continuum,
interpolating smoothly between the Forward KL (as 𝛼 → 0) and the Reverse KL (as 𝛼 → 1). In between (for
𝛼 = 0.5) lies the squared Hellinger distance [20]. By tuning 𝛼, one can balance the degree of mode-seeking versus
mass-covering behavior, potentially capturing the benefits of both extremes while mitigating their drawbacks. We
refer to Table 1 for a full characterization. We denote the parametrization of 𝑓 -DPG with 𝛼-divergences as 𝜶-DPG,
which has the following pseudo-reward:
                                                                                         1−𝛼   !
                                                                       1
                                                                         
                                                  ′ 𝜋𝜃 ( 𝑦 | 𝑥 )             𝑝𝑥 ( 𝑦 )
                                𝑅𝜃 ( 𝑦, 𝑥 ) = − 𝑓                  =                          −1 .            (12)
                                                     𝑝𝑥 ( 𝑦 )        1 − 𝛼 𝜋𝜃 ( 𝑦 | 𝑥 )

Because for low values of 𝛼, peaks in the 𝑝/𝜋 ratios can induce large variance in 𝑅𝜃 , we clip the parenthetical
factor to a maximum 𝑀 . We also rescale by discounting the constant 1/(1 − 𝛼):
                                                                     1−𝛼       !
                                                         𝑝𝑥 ( 𝑦 )
                                    ˆ𝜃 ( 𝑦, 𝑥 )  min
                                    𝑅                                      − 1, 𝑀 .                        (13)
                                                        𝜋𝜃 ( 𝑦 | 𝑥 )

Finally, we use the gradient formula in Eq. 7, setting the baseline 𝐵 ( 𝑥 ) to the leave-one-out per-context average of
the pseudo rewards [1,28].
It is interesting to note its behavior when setting 𝛼 = 1 − 𝜖 (i.e., close to the Reverse KL). Then,
                                                                                           
                                                                           ′ 𝜋𝜃 ( 𝑦 | 𝑥 )
                               ∇𝜃 𝐷 𝑓𝛼 ( 𝜋𝜃 (·| 𝑥 )|| 𝑝𝑥 ) = 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 𝑓𝛼                   ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )    (14)
                                                                                𝑝𝑥 ( 𝑦 )
                                                                                           𝜖
                                                                                𝑝𝑥 ( 𝑦 )
                                                           ∝ −𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃                     ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )    (15)
                                                                               𝜋𝜃 ( 𝑦 | 𝑥 )
                                                      ≈ 𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃 − 𝑣 ( 𝑦, 𝑥 )∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) .                (16)

by discounting for simplicity the scaling constant and the baselines in Eq. 15, and noting that for 0 < 𝜖 ≪ 1
and if | 𝑥 | is bounded then 𝑥 𝜖 ≈ 𝕀[ 𝑥 ≠ 0] and 𝑝𝑥 ( 𝑦 ) ≠ 0 ⇔ 𝑣 ( 𝑦, 𝑥 ) = 1 in the last step. Thus, for 𝛼 that is lower
but very close to 1, we are again recovering the REINFORCE learning rule. In contrast, when 𝛼 = 0, then 𝐷 𝑓𝛼
becomes exactly the Forward KL, and thus we recover the original KL-DPG algorithm [25,43], which conserves
more diversity from the original distribution sacrificing some precision:
                                                                                        
                                                                          𝑝𝑥 ( 𝑦 )
                           ∇𝜃 𝐷 𝑓𝛼 ( 𝜋𝜃 (·| 𝑥 )|| 𝑝𝑥 ) = −𝔼𝑥 ∼D ,𝑦 ∼𝜋𝜃                − 1 ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )          (17)
                                                                         𝜋𝜃 ( 𝑦 | 𝑥 )



                                                                                                                         5
                 Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Parameter   Name/Correspondence       Generator 𝑓𝛼 ( 𝑡 ) (generic)     𝑓𝛼′ ( 𝑡 ) (generic)     𝑓𝛼′ ( 𝜋/ 𝑝)              𝑓𝛼′ (∞)
                                                                       𝑡 𝛼 −1 − 1                1        𝑝 1− 𝛼        𝛼 < 1 : 1−1 𝛼
                                                                                                                 
                                      𝑡 𝛼 − 𝛼𝑡 − (1 − 𝛼)
𝛼 ≠ 0, 1    𝛼–divergence ( 𝑓 -div.)                                                                              −1
                                           𝛼 ( 𝛼 − 1)                     𝛼−1                  𝛼−1 𝜋                    𝛼 > 1 : +∞
𝛼→1         Reverse KL KL(𝜋 ∥ 𝑝)      lim 𝑓𝛼 ( 𝑡 ) = 𝑡 log 𝑡 − 𝑡 + 1   lim 𝑓𝛼′ ( 𝑡 ) = log 𝑡   log ( 𝜋/ 𝑝)              +∞
                                      𝛼→1                              𝛼→1
                                                                                           1
𝛼→0         Forward KL KL( 𝑝 ∥ 𝜋)     lim 𝑓𝛼 ( 𝑡 ) = − log 𝑡 + 𝑡 − 1   lim 𝑓𝛼 ( 𝑡 ) = 1 − 𝑡
                                                                              ′
                                                                                               1 − 𝑝/𝜋                  1
                                      𝛼→0
                                        √                              𝛼→0
𝛼 = 21      Hellinger (exact)         −4 𝑡 + 2𝑡 + 2                    − √2   +2               −2 𝑝/𝜋 + 2               2
                                                                                                  √︁
                                                                          𝑡


                    Table 1: Parametrization of the 𝛼-divergence as an 𝑓 -divergence 𝐷 𝑓𝛼( 𝜋, 𝑝).


Notably, it is easy to see that if a fixed amount of samples are obtained just from 𝜋base instead of 𝜋𝜃 , KL-DPG
reduces to RS-FT [65,68], as it optimizes the cross-entropy to samples from the base model filtered by the verifier
(see App. D for more details).
Finally, while the general formal properties of 𝛼-divergences are well-studied, our specific setup, with a target
distribution that has a restricted support (over verifiable outputs only) has some interesting novel formal properties
that we describe in App. H.

4. Experiments
Informal vs Formal Mathematics Informal mathematics has become a common paradigm for training large
language models (LLMs) on reasoning tasks, with widely used benchmarks such as MATH [21] and AIME [52].
These methods have achieved impressive performance [17], but they also face inherent challenges. Informal
proofs and solutions often lack guarantees of rigor, making large-scale verification difficult and requiring heuristics
like majority voting rather than provable correctness. While effective in many scenarios, these approaches may be
less suited for tasks that aim to explore novel results or a wide variety of solutions. Formal methods provide a
promising alternative [56]. Proof assistants such as Lean [15], COQ [4], and Isabelle [40] represent statements
and proofs in a formally verifiable language. This not only allows for efficient and rigorous proof generation
but also reduces dependence on labeled data. At inference, the paradigm shifts from achieving consensus over
a large pool of candidates (eg., via majority voting) to ensuring sufficient diversity among them to guarantee
larger coverage. Theorem provers must therefore go beyond producing a single correct proof but should generate
diverse candidate proofs to more fully explore the solution space. Prior work in Lean has applied reinforcement
learning (e.g., GRPO [47, 58, 62]), but such methods can result in decreased diversity [19]. In this work, we
present an approach to formal theorem proving in Lean that seeks to improve both precision for better efficiency
and diversity to guarantee high coverage, highlighting the potential of formal reasoning for scalable discovery.

Models For these experiments we consider DeepSeek-Prover-V1.5-SFT [62] a 7B parameters models based on
DeepSeek model and further pre-trained on high-quality mathematics and code data, with a focus on formal
languages such as Lean, Isabelle, and Metamath, and finetuned on Lean4 code completion datasets [62].

Dataset We follow the experimental setup introduced in prior work [19]. The training set is composed of
10K solvable Lean problems extracted and filtered from the Lean Workbook dataset [61,63], from which 200
problems are kept unseen as a test set.

Reward function and Lean4 Verifier The reward function extracts the last Lean4 code block in the generated
sequence and verifies it automatically by the Lean proof assistant. The sequence is given a reward of 1 if
it is verified as correct and 0 otherwise. In our experiments we used the same Lean4 and Mathlib4 version
(lean4:v4.9.0) as used in DeepSeek-ProverV1.5 [62].

Baselines We compare against several baselines, focusing on critic-free methods, which have become standard
thanks to not requiring an additional copy of the model: GRPO [16] –for which we only consider its unbiased
instantiation, Dr. GRPO [38]– and other variants with diversity-preserving regularization: High-KL with a strong
KL penalty( 𝛽 = 0.1), Rw-Ulkly [19] with a rank bias promoting diversity 𝛽 = 0.25, and Pass@k training [8,55]
directly optimizes pass@𝑘 via a leave-one-out advantage formulation that reduces variance. We further include




                                                                                                                                        6
                Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



in our comparison GPG [10], ReMax [36] and RLOO [1]. For reference, Base-SFT is the model used as a base for
all methods.

Training All trainings are done on a single node of 4xA100 with 28 CPUs dedicated for running proof assessment
in parallel. Due to the high variance in Lean compilation and verification time, the reward function is executed
asynchronously. All training scripts are based on veRL [51]. By default, since we use a verifiable reward, we follow
Liu et al. [38],Mistral-AI et al. [39] and disable advantage normalization while setting the KL divergence penalty
to 𝛽 = 0. For all 𝛼-DPG training, we set the clipping value to 𝑀 = 10, train on float16 following Qi et al. [46],
and constrain the partition function on the lower side as 𝑍 𝑥 ≥ 𝜖 with 𝜖 = 1𝑒−4 . The partition function is computed
online using the sampled responses for each problem, thus not incurring any additional computational cost with
respect to baseline methods. See App. E for more details on the estimation of Z and an ablation experiment using
more samples to compute the partition function. Across all methods, we fix the maximum response length to
1024 tokens and use 512 generated sequences per step for 200 iterations (≈ 3 epochs). See App. F for additional
details on hyperparameters.

Evaluation Metric To evaluate model performance on reasoning and generation tasks, we report pass@k [6],
a standard metric widely used in code generation and problem-solving benchmarks. The metric measures the
probability that at least one correct solution is found within the top-𝑘 sampled outputs of the model. For a problem
with 𝑛 generated outputs with 𝑛 ≥ 𝑘, of which 𝑐 are correct, an unbiased estimate of the probability that at least
one of 𝑘 sampled outputs is correct is [6]
                                                                   𝑛− 𝑐
                                               pass@𝑘 = 1 −      𝑘
                                                                 𝑛   .
                                                                 𝑘

Averaging over problems gives the overall pass@𝑘. We generate responses using temperature 𝑇 = 1 and nucleus
sampling [22] with parameter 𝑝 = 0.99.

4.1. Results
Coverage vs. precision analysis We analyze models along the trade-off between coverage, measured by
pass@256, and precision, measured by pass@1 (Fig. 1). The results reveal a clear precision–coverage frontier.
The base SFT model attains relatively broad coverage but low precision, indicating the ability to solve diverse
problems but with a low single-sample success probability, placing it far from the frontier. Pass@k training improves
coverage while leaving precision largely unchanged. Training strategies such as GRPO with KL regularization and
GRPO-Rw-Ulkly improve precision without substantially affecting coverage, still shifting performance toward a
more favorable region of the trade-off space. In contrast, RLOO, GRPO without KL regularization, and GPG achieve
high precision at the cost of reduced coverage. Across 𝛼-DPG variants, lower-𝛼 settings (e.g., 𝛼 = 0.25) achieve the
highest coverage while still considerably improving precision over SFT. Increasing 𝛼 further improves precision,
reaching parity with RL-based methods at large values (e.g., 𝛼 ≥ 0.995), while typically retaining higher coverage.
Importantly, most 𝛼-DPG models lie on or near the Pareto frontier, demonstrating that the method provides a
controllable and efficient trade-off between precision and coverage, outperforming or matching competing RL
baselines across much of the spectrum.

Pass@𝑘 curves Figure 2 illustrates the pass@𝑘 performance on the test set measured over 𝑛 = 256 samples for
a few chosen models. First, looking at the left panel, we note that we have reproduced the results reported by He
et al. [19], where the GRPO model starts with a much higher pass@1 score, but then the base model overpasses
it as it reaches pass@16. Furthermore, there is no single model that dominates all others across all values of
𝑘 indicating a Pareto trade-off between precision (pass@1) and coverage (pass@256). Nonetheless, 𝛼-DPG
(𝛼 = 0.999) generally dominates GRPO and other pure RL-based techniques, with the only exception of ReMax
that has better coverage albeit somewhat lower precision. On the other hand, 𝛼 = 0.25 dominates the base model
and other diversity-preserving baselines such as Pass@k training and GRPO with KL regularization, achieving
the best performance on pass@256. Rw-Ulkly, in turn, starts with higher pass@1, but 𝛼 = 0.25 outperforms
for 𝑘 ≥ 4. The middle panel highlights the RL-based baselines, confirming that KL regularization helps prevent
diversity collapse and Pass@k training and Rw-Ulkly baselines offer competitive results. The rightmost panel is




                                                                                                                   7
                                        Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



                               Pass@k for highlighted models                                                                                          Pass@k for RL models
         0.90
                                                                                                                                                                                                                                        0.90
                                                                                                                                                                                                                                                                              Pass@k for -DPG variants
                                                                                                                   0.85
         0.85
                                                                                                                                                                                                                                        0.85

         0.80                                                                                                      0.80
                                                                                                                                                                                                                                        0.80

         0.75                                                                                                      0.75
                                                                                                                                                                                                                                        0.75
pass@k




                                                                                                          pass@k




                                                                                                                                                                                                                               pass@k
                                                                                    Models
         0.70                                                               Base SFT                               0.70                                                                                 Models                          0.70                                                                           Models
                                                                             -DPG ( =0.999)                                                                                                            Base SFT                                                                                                      Base SFT
                                                                             -DPG ( =0.25)                         0.65
                                                                                                                                                                                                       GRPO                                                                                                           -DPG ( =0)
         0.65                                                               GRPO                                                                                                                       GRPO (High-KL)                   0.65                                                                          -DPG ( =0.25)
                                                                            GRPO (High-KL)                                                                                                             ReMax                                                                                                          -DPG ( =0.5)
         0.60                                                               ReMax                                  0.60                                                                                GPG                                                                                                            -DPG ( =0.75)
                                                                            GPG                                                                                                                        RLOO                             0.60
                                                                                                                                                                                                                                                                                                                      -DPG ( =0.9)
                                                                            GRPO-Pass@k                                                                                                                GRPO-Pass@k                                                                                                    -DPG ( =0.99)
         0.55                                                               GRPO-Rw-Ulkly                          0.55                                                                                GRPO-Rw-Ulkly                    0.55                                                                          -DPG ( =0.999)
                   1      2    4        8           16   32         64               128       256                            1      2     4              8          16               32          64     128     256                                1    2              4         8      16            32      64       128         256
                                                    k                                                                                                                    k                                                                                                               k


                         Figure 2: Pass@𝑘 curves on the test set for the Base-SFT model tuned with different methods.

                easy    64         0           0              0                        easy          64                   0           0           0                            easy        56             0              0                     0                      easy        56            0              0                0


             medium     26         37          1              0                     medium           53                   7           2           2                          medium        34            37              0                     0                   medium         62            5              1                3
  Base SFT




                                                                         Base SFT




                                                                                                                                                              Base SFT




                                                                                                                                                                                                                                                        Base SFT
                hard     0         14          28             3                         hard         14               10              7          14                            hard         0             8             34                     3                      hard        18            4              2              21


             unsolved    0         1           6           20                       unsolved         1                    1           4          21                      unsolved           0             0              4                     24                  unsolved       1             0              2              25

                        easy   medium         hard       unsolved                                easy               medium          hard       unsolved                                    easy         medium          hard              unsolved                               easy         medium          hard        unsolved
                                    -DPG ( =0.25)                                                                         -DPG ( =0.999)                                                                  GRPO (High-KL)                                                                               GRPO



Figure 3: Problem Difficulty Transition Matrices showing the number of problems that transition from an initial
difficulty classification under the base model (Base-SFT) (y-axis) to a final difficulty after post-training (x-axis).
The results highlight a polarizing effect: 𝛼-DPG (𝛼 = 0.999) and GRPO exhibit similar behavior, improving
performance on a majority of medium-difficulty problems by making them easy, but also degrading performance
on hard problems, causing many of them to become unsolved. 𝛼-DPG (𝛼 = 0.25) and GRPO (High-KL) are more
conservative, improving sample efficiency on fewer problems but harder problems remain solvable.


comparing different variants of 𝛼-DPG in relation to the base model. While the base model surpasses and matches
models with 𝛼 ≥ 0.75, models with lower values of alpha dominate the base model.

Problem difficulty analysis In this section, we examine how training affects problem solvability. We categorize
problem difficulty based on model performance, measured as the proportion of correctly solved sequences. A
problem is considered easy for a given model if at least 80% of the sampled sequences are correct, medium if
20–80% are correct, and hard if fewer than 20% are correct. This notion of difficulty has a direct relation with
the efficiency of the model at solving a given problem as the number of samples until generating one correct
solution follows a geometric distribution whose parameter is the model’s sampling accuracy. In Figure 3 we plot
how the problems difficulties evolve after having trained the Base SFT model using various methods. Problems on
the diagonal (grey) remain unaffected by training. Elements in the lower-left triangle (blue) represent problems
for which solving efficiency improved, while elements in the upper-right triangle (red) indicate problems where
sampling efficiency decreased. As we can see, many problems that were medium or hard for the base model
became easy after training both for GRPO and 𝛼 = 0.999. However, this came at the cost of other problems
in these same categories becoming unsolvable given the same sampling budget. 𝛼-DGP (𝛼 = 0.25) and GRPO
(High-KL) on the other hand, improve sample efficiency on fewer problems at the cost of just three problems
becoming unsolvable.

Diversity Analysis We investigate the relationship between proof diversity and model performance. We split this
analysis into two components: the tactics and premises used in candidate Lean proofs. A tactic is a command that
transforms a proof goal into simpler subgoals (e.g., intro, apply, rw), while a premise is a lemma or previously
proven theorem that can be used within a proof (e.g., mul_comm, mul_assoc) . As measures of diversity, we
employ the Shannon index and the Gini-Simpson index. For each problem, we evaluate 256 generated proof
sequences. At every proof state, we compute both the Simpson index and Shannon entropy over the choices
of tactics and premises. Concretely, for a given problem, we count the occurrences of each premise and tactic,




                                                                                                                                                                                                                                                                                                                                          8
                                                  Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



                            Premise Diversity (Shannon Entropy) vs Model Pass@k
         0.80
                                                                                                             -DPG ( =0.5)
                                                                                                                                                                                                      Perplexity under Base/Tuned model
                                                                                                                      -DPG ( =0)                                           1.8                                                                        Metric Type
                                                                                                                                          0.88
                                                                                                       -DPG ( =0.75)
                                                                                                                                                                                                                                                Base Model Perplexity
                                                                                                                            GRPO-Pass@k
                                                                                                      -DPG ( =0.25)                                                        1.7                                                                  Self-Perplexity
         0.75                                                                                    GRPO (High-KL)
                                                                          -DPG ( =0.9)
                                                  -DPG ( =0.999)                                                    Base SFT              0.86
                                        RLOO          ReMax
                                                                                                                                                                           1.6
                     GRPO                 GPG
                                                            ReMax
                                                                                                                                          0.84                             1.5




                                                                                                                                                        Perplexity Value
         0.70                                   -DPG ( =0.999)
                                 RLOO
                      pass@1




                                                                                                                                             Pass@256
                                                     GRPO-Rw-Ulkly                                                                                                         1.4
Pass@1




                      Linear Regression ( -DPG)
                      pass@256                                                           -DPG ( =0.9)                                     0.82
         0.65         Linear Regression ( -DPG)
                                                                                                                                                                           1.3
                                   GPG             GRPO-Rw-Ulkly                                        -DPG ( =0.75)
                                                                                                                                          0.80
                                                                                                               -DPG ( =0.5)                                                1.2
                                                                                                              GRPO (High-KL)
         0.60                                                                                                     -DPG ( =0.25)
                                                                                                                        -DPG ( =0)        0.78                             1.1

                                                                                                                                                                           1.0
         0.55 GRPO                                                                                                  GRPO-Pass@k           0.76                                   Base model   Alpha=0.0    Alpha=0.25      Alpha=0.5    Alpha=0.999             GRPO
                                                                                                                              Base SFT                                                                     Model Generating Solutions
                                  2.5                         3.0                3.5                          4.0
                                                         Premise Shannon Entropy Index



Figure 4: Left: Relationship between premise diversity measured by Shannon index and model performance
(pass@1 and pass@256). The regression lines are computed for 𝛼-DPG models. The left y-axis shows pass@1
performance, and the right y-axis shows pass@256 performance. Right: Perplexity analysis showing the distri-
bution of perplexity for responses to a single problem sampled from various models under the base SFT model
distribution.


and compute the Simpson index as 𝐷 = 1 − 𝑆𝑖=1 𝑝2𝑖 and the Shannon index as 𝐻 = − 𝑆𝑖=1 𝑝𝑖 ln 𝑝𝑖 where 𝑝𝑖 is the
                                            Í                                        Í

relative abundance of premise or tactic 𝑖, and 𝑆 is the total number of premises or tactics. These metrics are
then aggregated across all problems to capture the overall diversity of candidate sequences. Higher diversity in
tactics and premises in candidate proofs generally correlates with improved pass@256 performance, whereas it
is anticorrelated with pass@1 as shown on the left panel of Figure 4 (and, additionally, in Appendix Figure 10).

Perplexity Analysis Recent work on RLVR [66] shows that RL-trained models do not truly discover new solutions,
instead the solutions they generate are already likely under the base model. To further investigate whether 𝛼-DPG
stays close to the base model, we conduct a perplexity analysis. We sample a single problem from the test set
and have each model generate 16 solutions. For each solution, we compute perplexity both under the model
that generated it (self-perplexity) and under the base model (Base SFT). As shown in the right panel of Figure
4, across all models, the generated sequences are already highly probable according to the base model, with
very similar perplexities. Note also that for this particular problem, GRPO collapsed and produces 16 identical
sequences, which were also highly probable under the base model.

5. Other Related Work
Improving test-time scaling (pass@𝑘) Popular RL-based post-training methods, such as PPO [49] or GRPO [50]
optimize inherently mode-seeking objectives, which can lead to mode collapse. The resulting models often achieve
high accuracy, but exhibit very low entropy, generating less diverse sequences [67]. This issue is particularly
pronounced when scaling test-time compute for solution search, with the SFT models often achieving better
performances due to higher diversity [7,19,55,66,69]. Multiple approaches try to overcome this issue, mainly
by adapting the advantage function. [19] proposed to add a rank bias penalty, that increases the advantage
of unlikely sequences. [8] modify the reward from pass@1 equivalent to pass@𝑘 , allowing better sampling
efficiency. They obtain a better pass@𝑘 at inference than training with entropy regularization. Tang et al. [55]
propose a leave one out strategy to reduce variance and therefore improving pass@k at test-time.

Reinforcement Learning from Proof Assistant Feedback Significant efforts in the community have focused on
training LLMs integrated with interactive proof assistants such as Lean [15], Coq [4], and Isabelle [40]. Early
approaches leveraged LLMs to generate the next proof step or tactic [2,44,61], often combined with explicit search
strategies [32]. More recent work has shifted towards training models to generate complete proofs directly [47,
58, 62] where the last training stage relies on reinforcement learning from proof assistant feedback (RLPAF),
where the proof assistant verification serves as a reward signal. However, RLPAF algorithms such as GRPO are




                                                                                                                                                                                                                                                                        9
                Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



mode-seeking, strongly truncating/filtering the original distribution, which inherently limits the diversity of
generated proofs and introduces significant inefficiencies in inference scaling [69].

6. Final Remarks and Conclusions
We have introduced DMVR, a general framework for optimizing a policy to produce only correct answers according
to a verifier function. This perspective casts RLVR training in a new light and helps diagnose its failure modes. In
particular, building on the work of Korbak et al. [30], we established that RLVR methods optimize toward a filtered
version of the original distribution, even if they do it in a way that especially focuses on certain regions of high
verifier reward. From this viewpoint, we can revisit recent debates on whether RL alone can create new skills [16,
19,60,67] and understand why RLVR does not generate fundamentally new capabilities but instead reweights
and amplifies behaviors already present in the base model. Moreover, because RLVR is tied to a mode-seeking
divergence, it sacrifices distributional breadth, leading models to forget solutions that the base model could
originally provide.
However, the core principle of filtering the base model is sound and can be independently motivated; it enforces
correctness while preserving the multiplicity of valid responses. The true source of diversity loss, therefore, lies
not in the target distribution itself, but in the divergence used to approximate it with gradient descent within a
restricted parametric family.
By explicitly defining the target distribution, DMVR enables optimization with divergences that balance the two
competing goals: correctness and diversity. In particular, we explored 𝛼-divergences, which smoothly interpolate
between Forward and Reverse KL. This approach generates a Pareto frontier of models: setting 𝛼 near the Reverse
KL recovers models that match or exceed the performance of RL-based alternatives, while low values of 𝛼 produce
models that preserve substantial diversity while still improving sampling precision over the base model.
The choice of divergence impacts the resulting models in at least two different ways: On one hand, loss landscapes
associated with different divergences can produce different training dynamics. On the other hand, within a
restricted parametric family, each divergence can induce different optima. To disentangle the contribution that
each of these factors has in the resulting models we could adopt a curriculum in which we gradually increase 𝛼
during training, thus encouraging coverage at the beginning of training, and precision towards the end. If the
resulting models preserve more diversity, this could be an indication that training dynamics matter. If, on the
contrary, they reach as much coverage as using a high value of 𝛼 from the start, then this would be an indication
that it is the optima for the given parametric family that dominates. We leave these questions for future work.

Known Limitations Without clipping, 𝛼-DPG is unstable for small values of 𝛼 (e.g., ≤ 0.5). Khalifa et al. [25]
use an offline version of DPG where the sampling policy is only updated from the training policy if the divergence
to the target probability is estimated to have improved. Here, we avoided keeping in memory a second copy of the
model, and preferred to manage variance by clipping the pseudo rewards. Also, the evidence for the effectiveness
of 𝛼-DPG centers on the Lean task using the DeepSeek Prover base model. Generalization to other tasks (e.g.,
code generation) and larger model families remains limited and is acknowledged as future work.




                                                                                                                 10
                Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Ethics statement
LLMs tuned using verifier feedback have attracted considerable attention from the research community and the
general public because of their strong problem-solving abilities. The techniques introduced in this paper aim to
preserve more of a model’s initial diversity than existing RL-based approaches at the cost of less strict adherence
to the verifier’s feedback.
In the specific setting we study—training models to prove theorems—this trade-off carries little risk of harm. In
broader applications, however, such as attempts to “align” language models with specific policies or behaviors,
weaker adherence to constraints could be more concerning. We note that recent proposals within the distributional
matching framework may help address this issue [26], even though they rely on the availability of a verifier at
inference time.
More importantly, the distributional perspective makes explicit the central choice of a target distribution to
optimize. Although the training techniques used for approximation also influence model behavior, we believe
that making the choice of target distribution open and transparent can promote accountability and clarity. We
therefore encourage this practice when tuning models for specific goals.

Reproducibility statement
We will make publicly available all the code to reproduce our experiments after publication. The Lean Workbook
dataset we used in our experiments is already open [61,63], as so it is the base model DeepSeek-Prover-V1.5-SFT
we use for training [62]. In addition to the experiment details we describe in Section 4, we report additional
details such as hyperparameter choices in in App. F.

Acknowledgements
We thank Thibaut Thonet for the very helpful comments on an early draft of this paper and anonymous reviewers
for suggestions that helped improve this work.

References
 [1] Arash Ahmadian, Chris Cremer, Matthias Gallé, Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin, Ahmet
     Üstün, and Sara Hooker. Back to Basics: Revisiting REINFORCE Style Optimization for Learning from Human
     Feedback in LLMs, February 2024. URL http://arxiv.org/abs/2402.14740. arXiv:2402.14740 [cs].
     3, 5, 7
 [2] AlphaProof and AlphaGeometry teams. AI achieves silver-medal standard solving International Mathe-
     matical Olympiad problems. Blog post, July 2024. URL: https://deepmind.google/discover/blog/
     ai-solves-imo-problems-at-silver-medal-level/. 9
 [3] Shun-ichi Amari. 𝛼-Divergence and 𝛼-Projection in Statistical Manifold. In Shun-ichi Amari (ed.), Differential-
     Geometrical Methods in Statistics, pp. 66–103. Springer, New York, NY, 1985. ISBN 978-1-4612-5056-2. doi:
     10.1007/978-1-4612-5056-2_3. 2, 5
 [4] Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Jean-Christophe Filliâtre, Eduardo Giménez,
     Hugo Herbelin, Gérard Huet, César Muñoz, Chetan Murthy, Catherine Parent, Christine Paulin-Mohring,
     Amokrane Saïbi, and Benjamin Werner. The Coq Proof Assistant Reference Manual : Version 6.1. Research
     Report RT-0203, INRIA, May 1997. URL https://inria.hal.science/inria-00069968. Projet COQ.
     6, 9
 [5] Christopher M. Bishop. Pattern recognition and machine learning. Information science and statistics. Springer,
     New York, 2006. ISBN 978-0-387-31073-2. 1, 2, 5
 [6] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared Kaplan,
     Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael
     Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov,
     Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such,
     Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen
     Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
     William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan
     Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder,
     Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating large


                                                                                                                 11
               Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



     language models trained on code. CoRR, abs/2107.03374, 2021. URL http://dblp.uni-trier.de/
     db/journals/corr/corr2107.html. 7
 [7] Zhipeng Chen, Xiaobo Qin, Youbin Wu, Yue Ling, Qinghao Ye, Wayne Xin Zhao, and Guang Shi. Pass@k
     training for adaptively balancing exploration and exploitation of large reasoning models. arXiv preprint
     arXiv:2508.10751, 2025. 9
 [8] Zhipeng Chen, Xiaobo Qin, Youbin Wu, Yue Ling, Qinghao Ye, Wayne Xin Zhao, and Guang Shi. Pass@k
     Training for Adaptively Balancing Exploration and Exploitation of Large Reasoning Models, August 2025.
     URL http://arxiv.org/abs/2508.10751. arXiv:2508.10751 [cs] version: 1. 6, 9
 [9] Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep Reinforcement
     Learning from Human Preferences. In Advances in Neural Information Processing Systems, volume 30. Curran
     Associates, Inc., 2017. URL https://proceedings.neurips.cc/paper_files/paper/2017/hash/
     d5e2c0adad503c91f91df240d0cd4e49-Abstract.html. 1, 2
[10] Xiangxiang Chu, Hailang Huang, Xiao Zhang, Fei Wei, and Yong Wang. GPG: A Simple and Strong
     Reinforcement Learning Baseline for Model Reasoning, May 2025. URL http://arxiv.org/abs/2504.
     02546. arXiv:2504.02546 [cs]. 7
[11] Andrzej Cichocki and Shun-ichi Amari. Families of alpha-, beta- and gamma-divergences: Flexible and
     robust measures of similarities. Entropy, 12(6):1532–1568, 2010. doi: 10.3390/e12061532. URL https:
     //www.mdpi.com/1099-4300/12/6/1532. 24
[12] Noel Cressie and Timothy R. C. Read. Multinomial Goodness-of-Fit Tests. Journal of the Royal Statistical
     Society. Series B (Methodological), 46(3):440–464, 1984. ISSN 0035-9246. URL https://www.jstor.
     org/stable/2345686. Publisher: [Royal Statistical Society, Oxford University Press]. 2, 5
[13] I. Csiszár and P. C. Shields. Information Theory and Statistics: A Tutorial. Foundations and Trends® in
     Communications and Information Theory, 1(4):417–528, December 2004. ISSN 1567-2190, 1567-2328.
     doi: 10.1561/0100000004. URL https://www.nowpublishers.com/article/Details/CIT-004.
     Publisher: Now Publishers, Inc. 3
[14] Xingyu Dang, Christina Baek, J. Zico Kolter, and Aditi Raghunathan. Assessing Diversity Collapse in
     Reasoning. February 2025. URL https://openreview.net/forum?id=AMiKsHLjQh. 1
[15] Leonardo Mendonça de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer.
     The lean theorem prover (system description). In CADE, 2015. URL https://api.semanticscholar.
     org/CorpusID:232990. 6, 9
[16] DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
     Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao,
     Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang
     Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun
     Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu,
     Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jiawei
     Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen,
     Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao,
     Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Meng
     Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang, Qinyu Chen,
     Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao
     Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting
     Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding
     Zeng, Wanjia Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An,
     Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu
     Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen
     Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei,
     Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan Shi,
     Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan
     Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan
     Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian
     Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda
     Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu,


                                                                                                          12
                Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



     Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, and Zhen Zhang.
     DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, January 2025. URL
     http://arxiv.org/abs/2501.12948. arXiv:2501.12948 [cs]. 1, 3, 6, 10
[17] Gemini       team.            Advanced      version   of   gemini    with    deep    think    officially
     achieves       gold     medal     standard     at   the    international   mathematical      olympiad.
     Blog      post,      July    2025.             URL:    https://deepmind.google/discover/blog/
     advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the
     6
[18] Dongyoung Go, Tomasz Korbak, Germán Kruszewski, Jos Rozen, Nahyeon Ryu, and Marc Dymetman.
     Aligning Language Models with Preferences through f-divergence Minimization, June 2023. URL http:
     //arxiv.org/abs/2302.08215. arXiv:2302.08215 [cs]. 1, 2, 3, 4
[19] Andre He, Daniel Fried, and Sean Welleck. Rewarding the Unlikely: Lifting GRPO Beyond Distribution
     Sharpening, June 2025. URL http://arxiv.org/abs/2506.02355. arXiv:2506.02355 [cs]. 1, 6, 7, 9,
     10
[20] E. Hellinger. Neue Begründung der Theorie quadratischer Formen von unendlichvielen Veränderlichen.
     Journal für die reine und angewandte Mathematik, 1909(136):210–271, July 1909. ISSN 1435-5345, 0075-
     4102. doi: 10.1515/crll.1909.136.210. URL https://www.degruyter.com/document/doi/10.1515/
     crll.1909.136.210/html. 5
[21] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and
     Jacob Steinhardt. Measuring Mathematical Problem Solving With the MATH Dataset, November 2021. URL
     http://arxiv.org/abs/2103.03874. arXiv:2103.03874 [cs]. 6
[22] Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. The Curious Case of Neural Text Degeneration.
     arXiv:1904.09751 [cs], February 2020. URL http://arxiv.org/abs/1904.09751. arXiv: 1904.09751.
     7
[23] Ferenc Huszár. How (not) to Train your Generative Model: Scheduled Sampling, Likelihood, Adversary?,
     November 2015. URL http://arxiv.org/abs/1511.05101. arXiv:1511.05101 [stat]. 1, 5
[24] B. Kappen, V. Gomez, and M. Opper. Optimal control as a graphical model inference problem. Machine
     Learning, 87(2):159–182, May 2012. ISSN 0885-6125, 1573-0565. doi: 10.1007/s10994-012-5278-7.
     URL http://arxiv.org/abs/0901.0633. arXiv:0901.0633 [math]. 3
[25] Muhammad Khalifa, Hady Elsahar, and Marc Dymetman. A Distributional Approach to Controlled Text
     Generation, May 2021. URL http://arxiv.org/abs/2012.11635. arXiv:2012.11635 [cs]. 1, 2, 3, 4, 5,
     10
[26] Minbeom Kim, Thibaut Thonet, Jos Rozen, Hwaran Lee, Kyomin Jung, and Marc Dymetman. Guaran-
     teed Generation from Large Language Models, July 2025. URL http://arxiv.org/abs/2410.06716.
     arXiv:2410.06716 [cs]. 1, 3, 11
[27] Robert Kirk, Ishita Mediratta, Christoforos Nalmpantis, Jelena Luketina, Eric Hambro, and Edward Grefen-
     stette. Understanding the Effects of RLHF on LLM Generalisation and Diversity. 2024. 1
[28] Wouter Kool. Buy 4 REINFORCE Samples, Get a Baseline for Free!, July 2019. URL https://wouterkool.
     github.io/publication/buy-4-samples-free-baseline/. 3, 5
[29] Tomasz Korbak, Hady Elsahar, German Kruszewski, and Marc Dymetman. Controlling Conditional Lan-
     guage Models without Catastrophic Forgetting, June 2022. URL http://arxiv.org/abs/2112.00791.
     arXiv:2112.00791 [cs]. 2, 3
[30] Tomasz Korbak, Hady Elsahar, Germán Kruszewski, and Marc Dymetman. On Reinforcement Learning and
     Distribution Matching for Fine-Tuning Language Models with no Catastrophic Forgetting, November 2022.
     URL http://arxiv.org/abs/2206.00761. arXiv:2206.00761 [cs]. 1, 2, 3, 4, 10
[31] Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman, Lester
     James V. Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, Yuling Gu, Saumya Malik, Victoria Graf, Jena D.
     Hwang, Jiangjiang Yang, Ronan Le Bras, Oyvind Tafjord, Chris Wilhelm, Luca Soldaini, Noah A. Smith,
     Yizhong Wang, Pradeep Dasigi, and Hannaneh Hajishirzi. Tulu 3: Pushing Frontiers in Open Language
     Model Post-Training, April 2025. URL http://arxiv.org/abs/2411.15124. arXiv:2411.15124 [cs]. 1
[32] Guillaume Lample, Timothee Lacroix, Marie anne Lachaux, Aurelien Rodriguez, Amaury Hayat, Thibaut
     Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural theorem proving. In Alice H.



                                                                                                              13
                Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



     Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho (eds.), Advances in Neural Information Processing
     Systems, 2022. URL https://openreview.net/forum?id=J4pX8Q8cxHH. 9
[33] Cheuk Ting Li and Farzan Farnia. Mode-Seeking Divergences: Theory and Applications to GANs. In
     Proceedings of The 26th International Conference on Artificial Intelligence and Statistics, pp. 8321–8350. PMLR,
     April 2023. URL https://proceedings.mlr.press/v206/ting-li23a.html. ISSN: 2640-3498. 1
[34] Long Li, Jiaran Hao, Jason Klein Liu, Zhijian Zhou, Xiaoyu Tan, Wei Chu, Zhe Wang, Shirui Pan, Chao Qu,
     and Yuan Qi. The Choice of Divergence: A Neglected Key to Mitigating Diversity Collapse in Reinforce-
     ment Learning with Verifiable Reward, September 2025. URL http://arxiv.org/abs/2509.07430.
     arXiv:2509.07430 [cs] version: 1. 5
[35] Yingzhen Li and Yarin Gal. Dropout inference in bayesian neural networks with alpha-divergences, 2017.
     URL https://arxiv.org/abs/1703.02914. 25
[36] Ziniu Li, Tian Xu, Yushun Zhang, Zhihang Lin, Yang Yu, Ruoyu Sun, and Zhi-Quan Luo. ReMax: A Simple,
     Effective, and Efficient Reinforcement Learning Method for Aligning Large Language Models, May 2024.
     URL http://arxiv.org/abs/2310.10505. arXiv:2310.10505 [cs]. 7
[37] Friedrich Liese and Igor Vajda. On divergences and informations in statistics and information theory. IEEE
     Transactions on Information Theory, 52(10):4394–4412, 2006. doi: 10.1109/TIT.2006.881731. 25
[38] Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin.
     Understanding r1-zero-like training: A critical perspective. In Conference on Language Modeling (COLM),
     2025. 3, 6, 7
[39] Mistral-AI, Abhinav Rastogi, Albert Q. Jiang, Andy Lo, Gabrielle Berrada, Guillaume Lample, Jason Rute,
     Joep Barmentlo, Karmesh Yadav, Kartik Khandelwal, Khyathi Raghavi Chandu, Léonard Blier, Lucile Saulnier,
     Matthieu Dinot, Maxime Darrin, Neha Gupta, Roman Soletskyi, Sagar Vaze, Teven Le Scao, Yihan Wang,
     Adam Yang, Alexander H. Liu, Alexandre Sablayrolles, Amélie Héliou, Amélie Martin, Andy Ehrenberg,
     Anmol Agarwal, Antoine Roux, Arthur Darcet, Arthur Mensch, Baptiste Bout, Baptiste Rozière, Baudouin De
     Monicault, Chris Bamford, Christian Wallenwein, Christophe Renaudin, Clémence Lanfranchi, Darius Dabert,
     Devon Mizelle, Diego de las Casas, Elliot Chane-Sane, Emilien Fugier, Emma Bou Hanna, Gauthier Delerce,
     Gauthier Guinet, Georgii Novikov, Guillaume Martin, Himanshu Jaju, Jan Ludziejewski, Jean-Hadrien
     Chabran, Jean-Malo Delignon, Joachim Studnia, Jonas Amar, Josselin Somerville Roberts, Julien Denize,
     Karan Saxena, Kush Jain, Lingxiao Zhao, Louis Martin, Luyu Gao, Lélio Renard Lavaud, Marie Pellat,
     Mathilde Guillaumin, Mathis Felardos, Maximilian Augustin, Mickaël Seznec, Nikhil Raghuraman, Olivier
     Duchenne, Patricia Wang, Patrick von Platen, Patryk Saffer, Paul Jacob, Paul Wambergue, Paula Kurylowicz,
     Pavankumar Reddy Muddireddy, Philomène Chagniot, Pierre Stock, Pravesh Agrawal, Romain Sauvestre,
     Rémi Delacourt, Sanchit Gandhi, Sandeep Subramanian, Shashwat Dalal, Siddharth Gandhi, Soham Ghosh,
     Srijan Mishra, Sumukh Aithal, Szymon Antoniak, Thibault Schueller, Thibaut Lavril, Thomas Robert, Thomas
     Wang, Timothée Lacroix, Valeriia Nemychnikova, Victor Paltz, Virgile Richard, Wen-Ding Li, William Marshall,
     Xuanyu Zhang, and Yunhao Tang. Magistral, June 2025. URL http://arxiv.org/abs/2506.10910.
     arXiv:2506.10910 [cs]. 3, 7
[40] Tobias Nipkow, Markus Wenzel, and Lawrence C. Paulson. Isabelle/HOL: a proof assistant for higher-order
     logic. Springer-Verlag, Berlin, Heidelberg, 2002. ISBN 3540433767. 6, 9
[41] Art B Owen. Importance Sampling. In Monte Carlo theory, methods and examples. Chapter 9, 2013. URL
     https://statweb.stanford.edu/Ëœowen/mc/Ch-var-is.pdf. 3, 19
[42] Laura O’Mahony, Leo Grinsztajn, Hailey Schoelkopf, and Stella Biderman. ATTRIBUTING MODE COLLAPSE
     IN THE FINE-TUNING OF LARGE LANGUAGE MODELS. 2024. 1
[43] Tetiana Parshakova, Jean-Marc Andreoli, and Marc Dymetman. Distributional Reinforcement Learn-
     ing for Energy-Based Sequential Models, December 2019. URL http://arxiv.org/abs/1912.08517.
     arXiv:1912.08517 [cs]. 1, 2, 3, 5
[44] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya Sutskever.
     Formal mathematics statement curriculum learning. In The Eleventh International Conference on Learning
     Representations, 2023. URL https://openreview.net/forum?id=-P7G-8dmSh4. 9
[45] Yury Polyanskiy and Yihong Wu. Information Theory: From Coding to Learning. Cambridge University Press,
     2025. ISBN 978-1108832908. 1, 26
[46] Penghui Qi, Zichen Liu, Xiangxin Zhou, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin. Defeating



                                                                                                                  14
                Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



     the Training-Inference Mismatch via FP16, October 2025. URL http://arxiv.org/abs/2510.26788.
     arXiv:2510.26788 [cs]. 7
[47] Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
     Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao, Daya
     Guo, and Chong Ruan. Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement
     learning for subgoal decomposition, 2025. URL https://arxiv.org/abs/2504.21801. 6, 9
[48] Alfréd Rényi. On Measures of Entropy and Information. In Proceedings of the Fourth Berkeley Symposium
     on Mathematical Statistics and Probability, Volume 1: Contributions to the Theory of Statistics, volume
     4.1, pp. 547–562. University of California Press, January 1961. URL https://projecteuclid.
     org/ebooks/berkeley-symposium-on-mathematical-statistics-and-probability/
     Proceedings-of-the-Fourth-Berkeley-Symposium-on-Mathematical-Statistics-and/
     chapter/On-Measures-of-Entropy-and-Information/bsmsp/1200512181. 2, 5
[49] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal Policy Optimization
     Algorithms, August 2017. URL http://arxiv.org/abs/1707.06347. arXiv:1707.06347 [cs]. 1, 3, 9
[50] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang,
     Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open
     Language Models, April 2024. URL http://arxiv.org/abs/2402.03300. arXiv:2402.03300 [cs]. 1, 9
[51] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin
     Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. arXiv preprint arXiv: 2409.19256,
     2024. 7
[52] Haoxiang Sun, Yingqian Min, Zhipeng Chen, Wayne Xin Zhao, Lei Fang, Zheng Liu, Zhongyuan Wang,
     and Ji-Rong Wen. Challenging the Boundaries of Reasoning: An Olympiad-Level Math Benchmark for
     Large Language Models, May 2025. URL http://arxiv.org/abs/2503.21380. arXiv:2503.21380 [cs]
     version: 2. 6
[53] Richard S. Sutton and Andrew Barto. Reinforcement learning: an introduction. Adaptive computation and
     machine learning. The MIT Press, Cambridge, Massachusetts London, England, second edition edition, 2020.
     ISBN 978-0-262-03924-6. 3
[54] Richard S Sutton, David McAllester, Satinder Singh, and Yishay Mansour. Policy Gradient Methods for
     Reinforcement Learning with Function Approximation. In Advances in Neural Information Processing Systems,
     volume 12. MIT Press, 1999. URL https://proceedings.neurips.cc/paper_files/paper/1999/
     hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html. 3
[55] Yunhao Tang, Kunhao Zheng, Gabriel Synnaeve, and Remi Munos. Optimizing language models for inference
     time objectives using reinforcement learning. In Forty-second International Conference on Machine Learning,
     2025. URL https://openreview.net/forum?id=ZVWJO5YTz4. 6, 9
[56] Terence Tao. Machine-assisted proof. Notices of the American Mathematical Society, 72:1, 01 2025. doi:
     10.1090/noti3041. 6
[57] Emanuel Todorov. Linearly-solvable Markov decision problems. In Advances in Neural Information Processing
     Systems, volume 19. MIT Press, 2006. URL https://papers.nips.cc/paper_files/paper/2006/
     hash/d806ca13ca3449af72a1ea5aedbed26a-Abstract.html. 3
[58] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung, Marina
     Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey, Chendong Song, Chenjun
     Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu, Jonas Bayer, Julien Michel, Longhui
     Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi Pagani, Moreira Machado, Pauline Bourigault, Ran Wang,
     Stanislas Polu, Thibaut Barroyer, Wen-Ding Li, Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu,
     Zihan Wang, Zhilin Yang, Zhengying Liu, and Jia Li. Kimina-prover preview: Towards large formal reasoning
     models with reinforcement learning, 2025. URL https://arxiv.org/abs/2504.11354. 6, 9
[59] Ronald J. Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning.
     Machine Learning, 8(3):229–256, May 1992. ISSN 1573-0565. doi: 10.1007/BF00992696. URL https:
     //doi.org/10.1007/BF00992696. 3
[60] Fang Wu, Weihao Xuan, Ximing Lu, Mingjie Liu, Yi Dong, Zaid Harchaoui, and Yejin Choi. The Invisible
     Leash: Why RLVR May or May Not Escape Its Origin, September 2025. URL http://arxiv.org/abs/
     2507.14843. arXiv:2507.14843 [cs]. 1, 10



                                                                                                                15
                   Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



[61] Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai Chen. Internlm2.5-
     stepprover: Advancing automated theorem proving via expert iteration on large-scale lean problems, 2024.
     URL https://arxiv.org/abs/2410.15700. 6, 9, 11
[62] Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
     Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang, Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F. Wu, Fuli Luo,
     and Chong Ruan. Deepseek-prover-v1.5: Harnessing proof assistant feedback for reinforcement learning
     and monte-carlo tree search. In The Thirteenth International Conference on Learning Representations, 2025.
     URL https://openreview.net/forum?id=I4YAIwrsXa. 6, 9, 11
[63] Huaiyuan Ying, Zijian Wu, Yihan Geng, JIayu Wang, Dahua Lin, and Kai Chen. Lean workbook: A large-scale
     lean problem set formalized from natural language math problems. In The Thirty-eight Conference on Neural
     Information Processing Systems Datasets and Benchmarks Track, 2024. URL https://openreview.net/
     forum?id=Vcw3vzjHDb. 6, 11
[64] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Tiantian Fan, Gaohong Liu,
     Lingjun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan Tong, Chi Zhang, Mofan
     Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen, Jiangjie Chen, Chengyi Wang, Hongli Yu, Weinan
     Dai, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-Ying Ma, Ya-Qin Zhang, Lin Yan, Mu Qiao,
     Yonghui Wu, and Mingxuan Wang. DAPO: An Open-Source LLM Reinforcement Learning System at Scale,
     March 2025. URL http://arxiv.org/abs/2503.14476. arXiv:2503.14476 [cs] version: 1. 3
[65] Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Keming Lu, Chuanqi Tan, Chang Zhou, and
     Jingren Zhou. Scaling Relationship on Learning Mathematical Reasoning with Large Language Models,
     September 2023. URL http://arxiv.org/abs/2308.01825. arXiv:2308.01825 [cs]. 2, 6, 18
[66] Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao Huang. Does
     reinforcement learning really incentivize reasoning capacity in llms beyond the base model? arXiv preprint
     arXiv:2504.13837, 2025. 9
[67] Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao Huang. Does
     Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?, May 2025.
     URL http://arxiv.org/abs/2504.13837. arXiv:2504.13837 [cs]. 1, 9, 10
[68] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. STaR: Bootstrapping Reasoning With Reasoning,
     May 2022. URL http://arxiv.org/abs/2203.14465. arXiv:2203.14465 [cs]. 2, 6, 18
[69] Xinyu Zhu, Mengzhou Xia, Zhepei Wei, Wei-Lin Chen, Danqi Chen, and Yu Meng. The surprising effectiveness
     of negative reinforcement in llm reasoning. arXiv preprint arXiv:2506.01347, 2025. 9, 10
[70] Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B. Brown, Alec Radford, Dario Amodei, Paul Christiano,
     and Geoffrey Irving. Fine-Tuning Language Models from Human Preferences, January 2020. URL http:
     //arxiv.org/abs/1909.08593. arXiv:1909.08593 [cs]. 1, 2

A. LLM Usage
We have required the assistance from LLMs (ChatGPT, Gemini) in the production of this paper on many stages
during its development. The most prevalent usage has been on writing code and debugging, but we have also
discussed research directions and mathematical statements, used them to simplify and format mathematical
proofs, proof-reading of the paper and improving the flow of the text, and they even assisted us in producing the
cartoon illustrating our method. The authors take full responsibility for the contents in this paper.

B. Proof of the correspondence between RLVR and Reverse KL
We work in the contextual setting where contexts 𝑥 are drawn from 𝜇 ( 𝑥 ), the policy is 𝜋𝜃 ( 𝑦 | 𝑥 ), the reward is
𝑣 ( 𝑦, 𝑥 ), and the prior (reference policy) is 𝜋ref ( 𝑦 | 𝑥 ). Define for each context 𝑥 and inverse temperature 𝛽 > 0

                               1                                                      ∑︁
                                     𝜋ref ( 𝑦 | 𝑥 ) exp 𝑣 ( 𝑦, 𝑥 )/ 𝛽 ,                    𝜋ref ( 𝑦 | 𝑥 ) exp 𝑣 ( 𝑦, 𝑥 )/ 𝛽 .
                                                                                                                          
              𝑝𝑥,𝛽 ( 𝑦 ) =                                                𝑍𝑥 ( 𝛽) =
                             𝑍𝑥 ( 𝛽)                                                  𝑦



Fix a context 𝑥 . The reverse KL divergence (from 𝜋𝜃 (· | 𝑥 ) to 𝑝𝑥,𝛽 ) is
                                                                                         
                                                                             𝜋𝜃 ( 𝑦 | 𝑥 )
                                  KL 𝜋𝜃 (· | 𝑥 ) 𝑝𝑥,𝛽 = 𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 ) log
                                                     
                                                                                            .
                                                                              𝑝𝑥,𝛽 ( 𝑦 )



                                                                                                                                16
                      Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Substituting 𝑝𝑥,𝛽 ( 𝑦 ) = 𝑍 𝑥 1( 𝛽 ) 𝜋ref ( 𝑦 | 𝑥 ) 𝑒𝑣 ( 𝑦,𝑥 )/ 𝛽 gives
                                                        h                                                             i
                                 KL 𝜋𝜃 ∥ 𝑝𝑥,𝛽 = 𝔼 𝑦 ∼𝜋𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) − log 𝑍 𝑥 1( 𝛽 ) 𝜋ref ( 𝑦 | 𝑥 ) 𝑒𝑣 ( 𝑦,𝑥 )/ 𝛽
                                             

                                                        h    𝜋𝜃 ( 𝑦 | 𝑥 )    1             i
                                               = 𝔼 𝑦 ∼𝜋𝜃 log                − 𝑣 ( 𝑦, 𝑥 ) + log 𝑍 𝑥 ( 𝛽 ) .
                                                             𝜋ref ( 𝑦 | 𝑥 )  𝛽

Equivalently (rearranging signs),
                                                            h1                𝜋𝜃 ( 𝑦 | 𝑥 ) i
                                    KL 𝜋𝜃 ∥ 𝑝𝑥,𝛽 = − 𝔼 𝑦 ∼𝜋𝜃 𝑣 ( 𝑦, 𝑥 ) − log                + log 𝑍 𝑥 ( 𝛽 ) .
                                                
                                                             𝛽                𝜋ref ( 𝑦 | 𝑥 )

Now take the gradient with respect to 𝜃 and average over contexts 𝑥 ∼ 𝜇 . Since 𝑍 𝑥 ( 𝛽 ) depends only on 𝜋ref and 𝑣
(not on 𝜃), ∇𝜃 log 𝑍 𝑥 ( 𝛽 ) = 0. Thus
                                                                               1
                                                                                                             
                                                                                               𝜋𝜃 ( 𝑦 | 𝑥 )
                       ∇𝜃 𝔼𝑥 ∼𝜇 KL( 𝜋𝜃 ∥ 𝑝𝑥,𝛽 ) = − ∇𝜃 𝔼𝑥 ∼𝜇 𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 ) 𝑣 ( 𝑦, 𝑥 ) − log
                                              
                                                                                                                .
                                                                               𝛽               𝜋ref ( 𝑦 | 𝑥 )

To proceed we use the score-function (REINFORCE) identity: for any function ℎ ( 𝑦, 𝑥 ) independent of 𝜃,

                          ∇𝜃 𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 ) [ ℎ ( 𝑦, 𝑥 )] = 𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 ) ℎ ( 𝑦, 𝑥 ) ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) .
                                                                                                            


Applying this identity (and noting the dependence of the log 𝜋𝜃 term must be handled consistently) yields the
explicit gradient form
                                                                    1
                                                                                                                        
                                                                                       𝜋𝜃 ( 𝑦 | 𝑥 )
             ∇𝜃 𝔼𝑥 ∼𝜇 KL( 𝜋𝜃 ∥ 𝑝𝑥,𝛽 ) = − 𝔼𝑥 ∼𝜇 𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 )      𝑣 ( 𝑦, 𝑥 ) − log                  ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) . (18)
                                    
                                                                    𝛽                  𝜋ref ( 𝑦 | 𝑥 )

This is the standard policy-gradient / score-function expression for the gradient of the reverse-KL objective in the
contextual case.
Finally, an equivalent compact form is obtained by moving the ∇𝜃 inside the expectation and noticing the factor
1/ 𝛽 :
                                                 1
                                                                                                   
                                                                                     𝜋𝜃 ( 𝑦 | 𝑥 )
                        ∇𝜃 𝔼𝑥 KL( 𝜋𝜃 ∥ 𝑝𝑥,𝛽 ) = − ∇𝜃 𝔼𝑥 ∼𝜇, 𝑦 ∼𝜋𝜃 𝑣 ( 𝑦, 𝑥 ) − 𝛽 log
                                            
                                                                                                      .
                                                 𝛽                                   𝜋ref ( 𝑦 | 𝑥 )

                                                                                                                                                     □
Maximizing the expected reward under the conditional policy:
                                                                                            𝜋𝜃 ( 𝑦 | 𝑥 )
                                                          𝔼𝑥,𝑦 ∼𝜋𝜃 [ 𝑣 ( 𝑦, 𝑥 ) − 𝛽 log                    ]
                                                                                            𝜋ref ( 𝑦 | 𝑥 )

is equivalent (up to constants) to minimizing:
                                                                                     
                                      𝔼𝑥 ∼𝜇 ( 𝑥 ) 𝐷KL ( 𝜋𝜃 ( 𝑦 | 𝑥 ) ∥ 𝑝𝑥,𝛽 ( 𝑦 | 𝑥 )) .


C. Proof that 𝑝 𝛽 becomes 𝑝 as 𝛽 → 0
Proposition 1.
                                                                       lim 𝑝𝑥,𝛽 = 𝑝𝑥 ,                                                             (19)
                                                                       𝛽 →0

in the formal sense that ∥ 𝑝𝑥,𝛽 − 𝑝𝑥 ∥ TV → 0 as 𝛽 ↓ 0. In particular 𝑝𝑥,𝛽 ( 𝑦 ) → 𝑝𝑥 ( 𝑦 ) for every fixed 𝑦 .
Proof. The proof is a direct adaptation, for a context 𝑥 , of the following Lemma.
Lemma 3. Let 𝜋base be a probability distribution on a countable set 𝑌 , let 𝑟 : 𝑌 → {0, 1} and assume 𝑍 :=
  𝑦 𝜋base ( 𝑦 ) 𝑟 ( 𝑦 ) ∈ (0, 1]. Define
Í

                                  𝜋base ( 𝑦 ) 𝑟 ( 𝑦 )                      𝜋base ( 𝑦 ) 𝑒𝑟 ( 𝑦 )/ 𝛽                ∑︁
                        𝑝( 𝑦) =                       ,       𝑝𝛽 ( 𝑦 ) =                           ,     𝑍 𝛽 :=        𝜋base ( 𝑦 ) 𝑒𝑟 ( 𝑦 )/ 𝛽 .
                                         𝑍                                         𝑍𝛽                             𝑦

Then ∥ 𝑝 𝛽 − 𝑝 ∥ TV → 0 as 𝛽 ↓ 0. In particular 𝑝 𝛽 ( 𝑦 ) → 𝑝 ( 𝑦 ) for every fixed 𝑦 ∈ 𝑌 .


                                                                                                                                                     17
                      Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Proof. Set 𝑆0 := 𝑟 ( 𝑦 )=0 𝜋base ( 𝑦 ) = 1 − 𝑍 and 𝜀 := 𝑒−1/ 𝛽 𝑆0 = 𝑒−1/ 𝛽 (1 − 𝑍 ). A short computation gives 𝑍 𝛽 = 𝑒1/ 𝛽 𝑍 + 𝑆0
                Í

and hence, after multiplying numerator and denominator by 𝑒−1/ 𝛽 ,
                                                                   𝜋base ( 𝑦 )
                                                                                                    𝑟 ( 𝑦 ) = 1,
                                                                 
                                                                 
                                                                  𝑍+𝜀 ,
                                                                 
                                                                 
                                                                 
                                                      𝑝𝛽 ( 𝑦 ) =
                                                                  𝑒−1/ 𝛽 𝜋base ( 𝑦 )
                                                                                                    𝑟 ( 𝑦 ) = 0.
                                                                 
                                                                                     ,
                                                                        𝑍+𝜀
                                                                 
                                                                 
Therefore                           ∑︁                                 𝜀                  ∑︁                                𝜀
                                              𝑝𝛽 ( 𝑦 ) − 𝑝 ( 𝑦 ) =           ,                      𝑝𝛽 ( 𝑦 ) − 𝑝 ( 𝑦 ) =       ,
                                                                     𝑍+𝜀                                                   𝑍+𝜀
                                  𝑟 ( 𝑦 )=1                                             𝑟 ( 𝑦 )=0

                                     2𝜀
so                                      and
     Í
         𝑦 | 𝑝 𝛽 ( 𝑦 ) − 𝑝 ( 𝑦 )| =
                                    𝑍+𝜀
                                                       1 ∑︁                           𝜀      𝑒 −1/ 𝛽 (1 − 𝑍 )
                                  ∥ 𝑝 𝛽 − 𝑝 ∥ TV =          | 𝑝 𝛽 ( 𝑦 ) − 𝑝 ( 𝑦 )| =     =                      .
                                                       2 𝑦                           𝑍+𝜀   𝑍 + 𝑒 −1/ 𝛽 (1 − 𝑍 )

Since 𝑒−1/ 𝛽 → 0 as 𝛽 ↓ 0, the right-hand side tends to 0, proving total-variation convergence. The pointwise
convergence 𝑝 𝛽 ( 𝑦 ) → 𝑝 ( 𝑦 ) follows immediately because | 𝑝 𝛽 ( 𝑦 ) − 𝑝 ( 𝑦 )| ≤ 𝑦 ′ | 𝑝 𝛽 ( 𝑦 ′ ) − 𝑝 ( 𝑦 ′ )| = 2∥ 𝑝 𝛽 − 𝑝 ∥ TV . □
                                                                                    Í


D. RS-FT optimizes the Forward KL
Rejection sampling fine tuning [65,68] generates a sample set from the base model 𝜋base , S ∼ 𝜋base (·| 𝑥 ), filters
them using the verifier to obtain S ′ = { 𝑦𝑖 : 𝑣 ( 𝑦𝑖 , 𝑥 ) = 1, 𝑦𝑖 ∈ S}, and then trains the policy using standard
cross-entropy on this filtered set:


                                                       ∇𝜃 L RS-FT = −𝔼 𝑦 ∼S ′ ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )                                    (20)

Now, starting from KL-DPG, we note that:

                                                                                                   
                                                                             𝑝𝑥 ( 𝑦 )
                                 ∇𝜃 𝐷KL ( 𝑝𝑥 || 𝜋𝜃 ) = −𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 )                  − 1 ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) .                  (21)
                                                                            𝜋𝜃 ( 𝑦 | 𝑥 )
                                                                            𝑝𝑥 ( 𝑦 )
                                                     = −𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 )                ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) .                        (22)
                                                                         𝜋𝜃 ( 𝑦 | 𝑥 )
                                                                                 ( 𝑦 | 𝑥 ) 𝑝𝑥 ( 𝑦 )
                                                     = −𝔼 𝑦 ∼𝜋𝜃 (· | 𝑥 ) base
                                                                         𝜋
                                                                                                           ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )       (23)
                                                                         𝜋base ( 𝑦 | 𝑥 ) 𝜋𝜃 ( 𝑦 | 𝑥 )
                                                                                𝑝𝑥 ( 𝑦 )
                                                     = −𝔼 𝑦 ∼𝜋base (· | 𝑥 )                     ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )                  (24)
                                                                            𝜋base ( 𝑦 | 𝑥 )
                                                         1                                ( 𝑦 | 𝑥 ) 𝑣 ( 𝑦, 𝑥 )
                                                     = − 𝔼 𝑦 ∼𝜋base (· | 𝑥 ) base
                                                                                 𝜋
                                                                                                               ∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 )   (25)
                                                        𝑍𝑥                             𝜋base ( 𝑦 | 𝑥 )
                                                       ∝ 𝔼 𝑦 ∼𝜋base (· | 𝑥 ) 𝑣 ( 𝑦, 𝑥 )∇𝜃 log 𝜋𝜃 ( 𝑦 | 𝑥 ) ,                         (26)

which exactly corresponds to the objective in Eq. 20. There are two crucial differences between the two: One
is their sample efficiency: whereas RS-FT is limited to using samples from the base model, many of which may
be rejected from the verifier, KL-DPG makes use of the updated policy which has a higher acceptance rate. The
second one is that whereas RS-FT uses a finite pool of samples, and thus can over-fit to them, KL-DPG uses an
unbounded number of samples.

E. Estimation of the partition function
Define

                                                              𝑃 𝑥 ( 𝑦 ) = 𝜋base ( 𝑦 | 𝑥 ) 𝑣 ( 𝑦, 𝑥 ) .                               (27)

over a discrete space Y, with partition function 𝑍 𝑥
                                                                                 ∑︁
                                                                      𝑍𝑥 =             𝑃𝑥 ( 𝑦) .                                     (28)
                                                                                 𝑦∈Y




                                                                                                                                       18
                 Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Using importance sampling [41] we can estimate 𝑍 𝑥 by using 𝑁 samples [ 𝑦𝑖 ] 𝑖 ∈ {0...𝑁 } generated from a proposal
distribution 𝑞 with Supp( 𝑃 ) ⊆ Supp( 𝑞), as follows.
                              ∑︁                                              ∑︁ 𝑞 ( 𝑦 | 𝑥 )                                                                    𝑃𝑥 ( 𝑦)     1 ∑︁ 𝑃 𝑥 ( 𝑦𝑖 )
                       𝑍𝑥 =                                 𝑃𝑥 ( 𝑦) =                                       𝑃 𝑥 ( 𝑦 ) = 𝔼 𝑦 ∼𝑞 (· | 𝑥 )                                   ≈                   .                     (29)
                                                                                         𝑞( 𝑦 | 𝑥)                                                              𝑞( 𝑦 | 𝑥)   𝑁    𝑞 ( 𝑦𝑖 | 𝑥 )
                              𝑦∈Y                                             𝑦∈Y                                                                                                          𝑖



Note that in the specific case that use 𝑞 = 𝜋base , then


                                                                       𝜋base ( 𝑦 | 𝑥 ) 𝑣 ( 𝑦, 𝑥 )                                1 ∑︁
                         𝑍 𝑥 = 𝔼 𝑦 ∼𝑞 (· | 𝑥 )                                                    = 𝔼 𝑦 ∼𝑞 (· | 𝑥 ) 𝑣 ( 𝑦, 𝑥 ) ≈      𝑣 ( 𝑦𝑖 , 𝑥 ) .                                                                (30)
                                                                          𝜋base ( 𝑦 | 𝑥 )                                        𝑁
                                                                                                                                                                                      𝑖



E.1. Ablation experiment: Role of the partition function calculation
To analyze whether a more precise calculation of the partition function affects the results, we compared the
reported results using an online-computed partition function based on just 4 sampled responses with a pre-
computed partition function using 128 samples from the base model. The results are displayed on Fig. 5, showing
no clear advantage for pre-computing the partition function. As a result, we favored the online computation as it
offers a drop-in replacement for GRPO and other similar variants without any additional computational burden.

                                                                                                 Ablation Study: Online vs Precomputed Z
                                                                       -DPG ( =0.25)
                                                     0.89
                                                                                        -DPG ( =0.25)

                                                                                          -DPG ( =0.5)
                                                     0.88        -DPG ( =0)             -DPG ( =0)


                                                                                                         -DPG ( =0.75)
                                                     0.87
                                                                                                                         -DPG ( =0.75)
                                                                                                -DPG ( =0.5)
                                                                                                                                    -DPG ( =0.9)     -DPG ( =0.9)
                               Coverage (Pass@256)




                                                     0.86

                                                                                                                                         -DPG ( =0.99)

                                                     0.85



                                                     0.84



                                                     0.83
                                                                                                                                                                                  -DPG ( =0.99)

                                                     0.82                                                                                                                 Online Z Points
                                                                                                                                                                          Online Z Frontier
                                                                                                                                                                                     -DPG ( =0.999)
                                                                                                                                                                          Precomputed-DPGZ (Points
                                                                                                                                                                                             =0.999)
                                                                                                                                                                          Precomputed Z Frontier
                                                              0.60               0.62                    0.64                    0.66                    0.68           0.70                   0.72
                                                                                                                    Precision (Pass@1)


Figure 5: Comparison of 𝛼-DPG with 𝑍 𝑥 computed online on the basis of just 4 samples per problem versus using
128 samples to compute the partition function offline.


F. Additional Experimental Details and Hyperparameters

       Method                                                                     Learning Rate                                          Batch Size                       Rollout Size (N)             KL Penalty
       Pass@k                                                                               1 × 10−6                                               16                                           32       0.001
       Rwrd. Unlkly (rank plty=0.25)                                                        2 × 10−6                                               16                                           32       0.001
       Dr. GRPO                                                                             2 × 10−6                                               128                                          4         0.0
       RLOO                                                                                 2 × 10−6                                               128                                          4         0.0
       GPG                                                                                  2 × 10−6                                               128                                          4         0.0
       ReMax                                                                                2 × 10−6                                               128                                          4         0.0
       Dr. GRPO with High KL                                                                2 × 10−6                                               128                                          4         0.1
       𝛼-DPG                                                                                2 × 10−6                                               128                                          4          -

                      Table 2: Summary of key hyper parameters for different training runs.




                                                                                                                                                                                                                     19
               Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity




 Figure 6: Training curves of both 𝛼-DPG and dr-GRPO. Sequence entropy on the right and reward on the left




Figure 7: Training curves of 𝛼-DPG for various alpha values. Sequence entropy on the right and reward on the
left. (Truncated curves are runs that have been stopped and resumed )




Figure 8: Training curves various dr-grpo baselines (dr-grpo, +high KL, +entropy). Sequence entropy on the
right and reward on the left. (Truncated curves are runs that have been stopped and resumed )


G. Additional Experimental Results




                                                                                                          20
                                       Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity




               easy    56       0             0        0                     easy    56       0               0        0                     easy    56       8              0        0                     easy    64       0                0      0


            medium     34      37             0        0                  medium     62       5               1        3                  medium      2      62              0        0                  medium     53       9                2      0
 Base SFT




                                                               Base SFT




                                                                                                                               Base SFT




                                                                                                                                                                                              Base SFT
               hard     0       8            34        3                     hard    18       4               2       21                     hard     0       3             40        2                     hard     6      10             22        7


            unsolved    0       0             4       24                  unsolved    1       0               2       25                  unsolved    0       0              4       23                  unsolved    0       1                5     21

                       easy   medium         hard   unsolved                         easy   medium           hard   unsolved                         easy   medium          hard   unsolved                         easy   medium          hard   unsolved
                                GRPO (High-KL)                                                       GRPO                                                      GRPO-Pass@k                                                   GRPO-Rw-Ulkly


               easy    64       0             0        0                     easy    63       1               0        0                     easy    63       1              0        0                     easy    62       2                0      0


            medium     57       5             1        1                  medium     54       6               3        1                  medium     54       6              1        3                  medium     25      38                1      0
 Base SFT




                                                               Base SFT




                                                                                                                               Base SFT




                                                                                                                                                                                              Base SFT
               hard    14       7            11       13                     hard     8      13              15        9                     hard    13       8             12       12                     hard     0      12             29        4


            unsolved    1       0             2       24                  unsolved    1       0               5       21                  unsolved    0       1              4       22                  unsolved    0       1                6     20

                       easy   medium         hard   unsolved                         easy   medium           hard   unsolved                         easy   medium          hard   unsolved                         easy   medium          hard   unsolved
                                       GPG                                                           ReMax                                                           RLOO                                                        -DPG ( =0)


               easy    64       0             0        0                     easy    64       0               0        0                     easy    64       0              0        0                     easy    64       0                0      0


            medium     26      37             1        0                  medium     30      33               1        0                  medium     34      29              1        0                  medium     42      21                1      0
 Base SFT




                                                               Base SFT




                                                                                                                               Base SFT




                                                                                                                                                                                              Base SFT
               hard     0      14            28        3                     hard     2       9              28        6                     hard     2       9             30        4                     hard     3      12             25        5


            unsolved    0       1             6       20                  unsolved    0       1               5       21                  unsolved    0       2              2       23                  unsolved    1       1                2     23

                       easy   medium         hard   unsolved                         easy   medium           hard   unsolved                         easy   medium          hard   unsolved                         easy   medium          hard   unsolved
                                 -DPG ( =0.25)                                                    -DPG ( =0.5)                                                 -DPG ( =0.75)                                                     -DPG ( =0.9)


               easy    64       0             0        0                     easy    64       0               0        0                     easy    64       0              0        0                     easy    64       0                0      0


            medium     49      12             3        0                  medium     51      10               2        1                  medium     53       9              1        1                  medium     55       6                2      1
 Base SFT




                                                               Base SFT




                                                                                                                               Base SFT




                                                                                                                                                                                              Base SFT




               hard     8      11            19        7                     hard    10      10              21        4                     hard    12       8             12       13                     hard    11       6             19        9


            unsolved    1       0             2       24                  unsolved    1       0               3       23                  unsolved    1       0              3       23                  unsolved    1       1                2     23

                       easy   medium         hard   unsolved                         easy   medium           hard   unsolved                         easy   medium          hard   unsolved                         easy   medium          hard   unsolved
                                 -DPG ( =0.95)                                                 -DPG ( =0.96)                                                   -DPG ( =0.97)                                                  -DPG ( =0.98)


               easy    64       0             0        0                     easy    64       0               0        0                     easy    64       0              0        0                     easy    64       0                0      0


            medium     55       6             2        1                  medium     54       9               0        1                  medium     54       7              2        1                  medium     53       7                2      2
 Base SFT




                                                               Base SFT




                                                                                                                               Base SFT




                                                                                                                                                                                              Base SFT




               hard    15       3            16       11                     hard    12       9              12       12                     hard    14       7             13       11                     hard    14      10                7     14


            unsolved    0       1             3       23                  unsolved    2       1               2       22                  unsolved    1       1              4       21                  unsolved    1       1                4     21

                       easy   medium         hard   unsolved                         easy   medium           hard   unsolved                         easy   medium          hard   unsolved                         easy   medium          hard   unsolved
                                 -DPG ( =0.99)                                                -DPG ( =0.995)                                                  -DPG ( =0.997)                                                 -DPG ( =0.999)



Figure 9: Problem Difficulty Transition Matrix from the Base-SFT to GRPO. The matrix shows the number of
problems that transition from an initial difficulty classification under the base model (Base-SFT) (y-axis) to a final
classification after post-training (x-axis).




                                                                                                                                                                                                                                                             21
                                                           Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity




                              Premise Diversity (Simpson Index) vs Model Pass@k                                                                                                                                                                                                         Tactic Diversity (Simpson Index) vs Model Pass@k

                                                                                                                                                    -DPG ( =0.5)                                                                         0.75                                                                                                                                                                                                 -DPG ( =0.5)
                                                                                                                                                                           -DPG ( =0)                                                                                                                                                                                                                                                                                            -DPG ( =0)
                                                                                                                                                                                                      0.88                                                                                                                                                                                                                                                                                             0.88
                                                                                                                                                                                                                                                                             -DPG ( =0.999)
          0.80                                                                                                                                            -DPG ( =0.75)                                                                                                                                                                                                                                                                    -DPG ( =0.75)
                                                                                                                                               -DPG ( =0.25) GRPO-Pass@k                                                                                                                 RLOO                                                                                                                                  -DPG ( =0.25) GRPO-Pass@k
                                                                                                                                                                                                                                                             GPG
                                                                                                                                   -DPG ( =0.9) GRPO (High-KL)                                                                                             GRPO                                                                                                                                                    -DPG ( =0.9) GRPO (High-KL)
                                                                                                                                                            Base SFT                                  0.86                                                                                                                              ReMax                                                                                                  Base SFT                                                0.86
                                                                                                                                                                                                                                         0.70
          0.75                                                             ReMax                                                                                                                                                                                                                                   ReMax

                                                                             -DPG ( =0.999)
                                                                                                                                                                                                      0.84                                                                                                                                                                GRPO-Rw-Ulkly                                                                                                                0.84
                                          GPG RLOO RLOO                     -DPG ( =0.999)                                                                                                                                                                                              RLOO
                 GRPO                                                                                                                                                                                                                                       -DPG ( =0.999)                                                                                                                                                                   -DPG ( =0.9)
                                                                                 ReMax
          0.70          pass@1                                                                                                                                                                                                                                     pass@1




                                                                                                                                                                                                         Pass@256




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Pass@256
 Pass@1




                                                                                                                                                                                                                                Pass@1
                        Linear Regression ( -DPG)                                                                                                                                                                                        0.65                      Linear Regression ( -DPG)
                        pass@256                                                            GRPO-Rw-Ulkly
                                                                                                                                                                                                      0.82                                                         pass@256                                                                                                                                                                                                                            0.82
                        Linear Regression ( -DPG)                                                                                                   -DPG ( =0.9)                                                                                                   Linear Regression ( -DPG)                                                                                                                                                 -DPG ( =0.75)
          0.65                                   GPG                 GRPO-Rw-Ulkly                                                                                                                                                                                        GPG                                                                    GRPO-Rw-Ulkly                                                                                      -DPG ( =0.5)
                                                                                                                                                                                                      0.80                                                                                                                                                                                                                                                                                             0.80
                                                                                                                                                     -DPG ( =0.75)
                                                                                                                                                            -DPG ( =0.5)                                                                 0.60                                                                                                                                                                                      GRPO (High-KL) -DPG ( =0.25)
                                                                                                                                                  GRPO (High-KL)                                                                                                                                                                                                                                                                                         -DPG ( =0)
          0.60                                                                                                                                                         -DPG ( =0.25)                  0.78                                                                                                                                                                                                                                                                                             0.78
                                                                                                                                                                           -DPG ( =0)


                                                                                                                                                                   GRPO-Pass@k                        0.76                               0.55                                                                                                                                                                                                                             GRPO-Pass@k                  0.76
          0.55   GRPO                                                                                                                                                                                                                                       GRPO
                                                                                                                                                                           Base SFT                                                                                                                                                                                                                                                                                                 Base SFT

                  0.60                     0.65                       0.70                            0.75                         0.80                    0.85                    0.90                                                                                                0.55                            0.60                                        0.65                          0.70                                           0.75                                 0.80
                                                                           Premise Simpson Index Index                                                                                                                                                                                                                                      Tactic Simpson Index Index


                             Premise Diversity (Shannon Entropy) vs Model Pass@k                                                                                                                                                                                                       Tactic Diversity (Shannon Entropy) vs Model Pass@k
          0.80
                                                                                                                                                           -DPG ( =0.5)                                                                                                                                                                                                                                                      -DPG ( =0.5)
                                                                                                                                                                                                                                         0.75                                                                                                                                                                                                                                -DPG ( =0)
                                                                                                                                                                    -DPG ( =0)
                                                                                                                                                                                                      0.88                                                                                                                                                                                                                                                                                             0.88
                                                                                                                                                 -DPG ( =0.75)                                                                                                                                -DPG ( =0.999)                                                                                                                       -DPG ( =0.75)
                                                                                                                                                                      GRPO-Pass@k                                                                                                                                                                                                                                                 -DPG ( =0.25) GRPO-Pass@k
                                                                                                                                                -DPG ( =0.25)
          0.75                                                                                                                             GRPO (High-KL)                                                                                                                                      RLOO                                                                                        -DPG ( =0.9)
                                                                                                                                                                                                                                                                                                                                                                                                                            GRPO (High-KL)
                                                                                                             -DPG ( =0.9)
                                                                                                                                                              Base SFT                                0.86                                                                               GPG                                                                                                                                                    Base SFT                                               0.86
                                                                -DPG ( =0.999)                                                                                                                                                                                 GRPO                                                                 ReMax
                                                RLOO                ReMax                                                                                                                                                                0.70                                                                     ReMax
                      GRPO                        GPG
                                                                           ReMax                                                                                                                                                                                                                                                                                                                                                                                                                       0.84
          0.70                                                 -DPG ( =0.999)                                                                                                                         0.84                                                                                RLOO                                               GRPO-Rw-Ulkly
                                         RLOO                                                                                                                                                                                                                 -DPG ( =0.999)
                                                                                                                                                                                                                                                                                                                                                                                                                     -DPG ( =0.9)
                        pass@1                                                                                                                                                                                                                                     pass@1




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Pass@256
                                                                                                                                                                                                         Pass@256




                                                                   GRPO-Rw-Ulkly
                                                                                                                                                                                                                                Pass@1
 Pass@1




                        Linear Regression ( -DPG)                                                                                                                                                                                        0.65                      Linear Regression ( -DPG)
                        pass@256                                                                                                   -DPG ( =0.9)                                                       0.82                                                         pass@256                                                                                                                                                                                                                            0.82
          0.65          Linear Regression ( -DPG)                                                                                                                                                                                                                  Linear Regression ( -DPG)
                                                                                                                                                                                                                                                                                                                                                                                                                                                   -DPG ( =0.75)
                                           GPG                    GRPO-Rw-Ulkly                                                                       -DPG ( =0.75)                                                                                                                     GPG                      GRPO-Rw-Ulkly                                                                                                                          -DPG ( =0.5)
                                                                                                                                                                                                      0.80                                                                                                                                                                                                                                                                                             0.80
                                                                                                                                                             -DPG ( =0.5)
                                                                                                                                                                                                                                                                                                                                                                                                                                                        GRPO (High-KL)
                                                                                                                                                            GRPO (High-KL)
                                                                                                                                                                                                                                         0.60                                                                                                                                                                                                                 -DPG ( =0.25)
          0.60                                                                                                                                                  -DPG ( =0.25)                                                                                                                                                                                                                                                                                     -DPG ( =0)
                                                                                                                                                                      -DPG ( =0)                      0.78                                                                                                                                                                                                                                                                                             0.78


                                                                                                                                                                     GRPO-Pass@k                      0.76                               0.55 GRPO                                                                                                                                                                                                                               GRPO-Pass@k           0.76
          0.55 GRPO
                                                                                                                                                                              Base SFT                                                                                                                                                                                                                                                                                               Base SFT

                                         2.5                                  3.0                                            3.5                            4.0                                                                                             1.4                          1.6                     1.8                            2.0                       2.2                           2.4                                  2.6                           2.8
                                                                       Premise Shannon Entropy Index                                                                                                                                                                                                                                      Tactic Shannon Entropy Index



                                                                                                                                           Figure 10: Diversity index vs Pass@k
                                                                                                                                                                                                                                                                                                                                                                                                                                                        𝛼-DPG (𝛼=0.995)




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     𝛼-DPG (𝛼=0.997)




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          𝛼-DPG (𝛼=0.999)
                                                                                                                                                                                                               𝛼-DPG (𝛼=0.25)




                                                                                                                                                                                                                                                                      𝛼-DPG (𝛼=0.75)




                                                                                                                                                                                                                                                                                                                       𝛼-DPG (𝛼=0.95)




                                                                                                                                                                                                                                                                                                                                                  𝛼-DPG (𝛼=0.96)




                                                                                                                                                                                                                                                                                                                                                                          𝛼-DPG (𝛼=0.97)




                                                                                                                                                                                                                                                                                                                                                                                                  𝛼-DPG (𝛼=0.98)




                                                                                                                                                                                                                                                                                                                                                                                                                            𝛼-DPG (𝛼=0.99)
                                                                                     GRPO (High-KL)




                                                                                                             GRPO-Rw-Ulkly




                                                                                                                                                                                                                                           𝛼-DPG (𝛼=0.5)




                                                                                                                                                                                                                                                                                                 𝛼-DPG (𝛼=0.9)
                                                 GRPO-Pass@k




                                                                                                                                                                                        𝛼-DPG (𝛼=0)
                              Base SFT




                                                                                                                                   ReMax
                                                                    GRPO




                                                                                                                                                    RLOO




                                                                                                                                                                     GPG




Base SFT        55.3/86.5    -1.0     +5.5       -0.5     +0.5      +2.0      +5.0      +5.5       -1.5      -2.0     +0.0      +0.0      +0.5      +2.0      +0.5      +5.0      +3.0      +4.0      +4.0      +3.0      +5.0
GRPO-Pass@k       +0.6    55.9/87.5   +6.5      +0.5      +1.5      +3.0      +6.0      +6.5       -0.5      -1.0     +1.0      +1.0      +1.5      +3.0      +1.5      +6.0      +4.0      +5.0      +5.0      +4.0      +6.0
GRPO             +14.7     +14.1    70.0/81.0    -6.0      -5.0      -3.5      -0.5     +0.0       -7.0      -7.5      -5.5      -5.5      -5.0      -3.5      -5.0      -0.5      -2.5      -1.5      -1.5      -2.5      -0.5
GRPO (High-KL)    +5.4      +4.8       -9.3   60.7/87.0   +1.0      +2.5      +5.5      +6.0       -1.0      -1.5     +0.5      +0.5      +1.0      +2.5      +1.0      +5.5      +3.5      +4.5      +4.5      +3.5      +5.5
GRPO-Rw-Ulkly    +12.4     +11.8       -2.4     +6.9    67.7/86.0   +1.5      +4.5      +5.0       -2.0      -2.5      -0.5      -0.5      -0.0     +1.5       -0.0     +4.5      +2.5      +3.5      +3.5      +2.5      +4.5
ReMax            +14.3     +13.7       -0.5     +8.8      +1.9    69.5/84.5   +3.0      +3.5       -3.5      -4.0      -2.0      -2.0      -1.5     +0.0       -1.5     +3.0      +1.0      +2.0      +2.0      +1.0      +3.0
RLOO             +15.2     +14.6      +0.5      +9.8      +2.9      +1.0    70.5/81.5   +0.5       -6.5      -7.0      -5.0      -5.0      -4.5      -3.0      -4.5     +0.0       -2.0      -1.0      -1.0      -2.0     +0.0
GPG              +16.5     +15.9      +1.8     +11.1      +4.2      +2.3      +1.3    71.8/81.0    -7.0      -7.5      -5.5      -5.5      -5.0      -3.5      -5.0      -0.5      -2.5      -1.5      -1.5      -2.5      -0.5
𝛼-DPG (𝛼=0)       +6.5      +5.9       -8.2     +1.1       -5.9      -7.8      -8.7     -10.0   61.8/88.0    -0.5     +1.5      +1.5      +2.0      +3.5      +2.0      +6.5      +4.5      +5.5      +5.5      +4.5      +6.5
𝛼-DPG (𝛼=0.25)    +6.7      +6.2       -8.0     +1.3       -5.6      -7.5      -8.5      -9.8     +0.3    62.0/88.5   +2.0      +2.0      +2.5      +4.0      +2.5      +7.0      +5.0      +6.0      +6.0      +5.0      +7.0
𝛼-DPG (𝛼=0.5)     +7.5      +6.9       -7.2     +2.1       -4.9      -6.8      -7.7      -9.0     +1.0      +0.8    62.8/86.5    -0.0     +0.5      +2.0      +0.5      +5.0      +3.0      +4.0      +4.0      +3.0      +5.0
𝛼-DPG (𝛼=0.75)    +9.5      +8.9       -5.2     +4.1       -2.9      -4.8      -5.7      -7.0     +3.0      +2.7      +2.0    64.8/86.5   +0.5      +2.0      +0.5      +5.0      +3.0      +4.0      +4.0      +3.0      +5.0
𝛼-DPG (𝛼=0.9)    +11.7     +11.1       -3.0     +6.3       -0.6      -2.5      -3.5      -4.8     +5.2      +5.0      +4.2      +2.2    67.0/86.0   +1.5       -0.0     +4.5      +2.5      +3.5      +3.5      +2.5      +4.5
𝛼-DPG (𝛼=0.95)   +13.3     +12.8       -1.4     +7.9      +1.0       -0.9      -1.9      -3.2     +6.8      +6.6      +5.8      +3.9      +1.6    68.6/84.5    -1.5     +3.0      +1.0      +2.0      +2.0      +1.0      +3.0
𝛼-DPG (𝛼=0.96)   +14.3     +13.7       -0.4     +8.9      +2.0      +0.1       -0.9      -2.2     +7.8      +7.6      +6.8      +4.8      +2.6      +1.0    69.6/86.0   +4.5      +2.5      +3.5      +3.5      +2.5      +4.5
𝛼-DPG (𝛼=0.97)   +15.1     +14.5      +0.3      +9.6      +2.7      +0.8       -0.2      -1.5     +8.6      +8.3      +7.5      +5.6      +3.3      +1.7      +0.7    70.3/81.5    -2.0      -1.0      -1.0      -2.0     +0.0
𝛼-DPG (𝛼=0.98)   +14.5     +13.9       -0.2     +9.0      +2.1      +0.2       -0.7      -2.1     +8.0      +7.7      +7.0      +5.0      +2.8      +1.1      +0.1       -0.6   69.8/83.5   +1.0      +1.0       -0.0     +2.0
𝛼-DPG (𝛼=0.99)   +15.3     +14.7      +0.6      +9.9      +2.9      +1.0      +0.1       -1.2     +8.8      +8.5      +7.8      +5.8      +3.6      +2.0      +1.0      +0.2      +0.8    70.6/82.5    -0.0      -1.0     +1.0
𝛼-DPG (𝛼=0.995)  +16.7     +16.1      +2.0     +11.3      +4.4      +2.5      +1.5      +0.2     +10.2     +10.0      +9.2      +7.3      +5.0      +3.4      +2.4      +1.7      +2.3      +1.4    72.0/82.5    -1.0     +1.0
𝛼-DPG (𝛼=0.997)  +16.9     +16.3      +2.2     +11.5      +4.6      +2.7      +1.7      +0.4     +10.4     +10.2      +9.4      +7.4      +5.2      +3.6      +2.6      +1.9      +2.5      +1.6      +0.2    72.2/83.5   +2.0
𝛼-DPG (𝛼=0.999)  +16.4     +15.8      +1.7     +11.0      +4.1      +2.2      +1.2       -0.1     +9.9      +9.7      +8.9      +6.9      +4.7      +3.1      +2.1      +1.4      +2.0      +1.1       -0.3      -0.5   71.7/81.5




Table 3: Pairwise performance comparison. Diagonal: Absolute Pass@1 / Pass@256 scores (%). Upper Triangle:
Pass@256 differences (Row − Column). Lower Triangle: Pass@1 differences (Row − Column). Bold indicates
statistical significance ( 𝑝 < 0.05) via paired bootstrap.




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      22
                   Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity




                   Premise Simpson Index   Tactic Simpson Index   Tactic Entropy Index   Premise Entropy Index   pass@256    pass@1
 Model
 Base SFT                      0.884013              0.793399               2.814039                 4.138613    0.865000   0.553008
 GRPO-Pass@k                   0.893146              0.793183               2.840828                 4.271897    0.875000   0.558867
 GRPO                          0.668813              0.558731               1.641007                 2.597491    0.810000   0.700332
 GRPO (High-KL)                0.867052              0.775942               2.665062                 3.936221    0.870000   0.607383
 GRPO-Rw-Ulkly                 0.794354              0.686514               2.127269                 3.231985    0.860000   0.676836
 ReMax                         0.712695              0.614204               1.861515                 2.920214    0.845000   0.695762
 RLOO                          0.651459              0.557749               1.614147                 2.448276    0.815000   0.705332
 GPG                           0.670303              0.550061               1.607887                 2.538284    0.810000   0.718320
 𝛼-DPG (𝛼=0)                   0.869384              0.775301               2.636581                 3.899748    0.880000   0.617969
 𝛼-DPG (𝛼=0.25)                0.864668              0.776839               2.654524                 3.873548    0.885000   0.620527
 𝛼-DPG (𝛼=0.5)                 0.864517              0.770372               2.616379                 3.855439    0.865000   0.628066
 𝛼-DPG (𝛼=0.75)                0.849480              0.759164               2.519318                 3.678993    0.865000   0.647949
 𝛼-DPG (𝛼=0.9)                 0.826129              0.735853               2.344282                 3.473220    0.860000   0.670332
 𝛼-DPG (𝛼=0.95)                0.793030              0.699298               2.144001                 3.191290    0.845000   0.686562
 𝛼-DPG (𝛼=0.96)                0.792300              0.670038               2.035383                 3.155785    0.860000   0.696621
 𝛼-DPG (𝛼=0.97)                0.731704              0.635556               1.884774                 2.848516    0.815000   0.703691
 𝛼-DPG (𝛼=0.98)                0.741682              0.635610               1.877606                 2.881272    0.835000   0.697891
 𝛼-DPG (𝛼=0.99)                0.718106              0.584643               1.699220                 2.735522    0.825000   0.706055
 𝛼-DPG (𝛼=0.995)               0.683162              0.554934               1.603550                 2.593344    0.825000   0.720449
 𝛼-DPG (𝛼=0.997)               0.702118              0.584954               1.693736                 2.687643    0.835000   0.722520
 𝛼-DPG (𝛼=0.999)               0.662599              0.546542               1.573962                 2.536636    0.815000   0.717402


Table 4: Diversity and performance metrics across models. For each problem statement, we evaluate 256 generated
proof sequences. At every proof state, we compute the Simpson Index (SI) and Shannon entropy over both
tactic choices and premise selections. The metrics are then aggregated across all problems to capture the overall
diversity of candidate sequences. Higher diversity in tactics and premises generally correlates with improved
pass@256 performance.




                                                                                                                                  23
                    Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



H. Formal complements on 𝛼-divergence
H.1. Smoothness of 𝛼-divergence, behaviour for 𝛼 → 0 and 𝛼 → 1
The fact that 𝐷 𝑓𝛼 ( 𝜋, 𝑝) is a continuous function of 𝛼 and that it converges to the forward 𝐾 𝐿 ( 𝑝 || 𝜋) for 𝛼 → 0 and
to the reverse 𝐾 𝐿 ( 𝜋 || 𝑝) for 𝛼 → 1 — including cases where these KL-divergences may be infinite — is well-known
in the literature, e.g. Cichocki & Amari [11].
In our specific situation, while typically the autoregressive policy 𝜋 is full-support (𝜋 ( 𝑦 ) > 0, ∀ 𝑦 ∈ Y), the support
𝐴 := { 𝑦 : 𝑝 ( 𝑦 ) > 0} of 𝑝 is a proper subset of Y. In such cases, while 𝐾 𝐿 ( 𝑝 || 𝜋) is (typically) finite,4 𝐾 𝐿 ( 𝜋 || 𝑝) is
infinite.

H.2. Comparing different policies, illustration
In order to provide a “non gradient” interpretation of what happens at the edges, it is instructive to compare
𝐷 𝑓𝛼 ( 𝜋, 𝑝) with 𝐷 𝑓𝛼 ( 𝜋′ , 𝑝) for different candidate policies 𝜋 and 𝜋′ .

Illustration We provide an illustration in Fig. 11, on a toy example with a small finite sample space Y, with
𝐴 ⊊ Y, and with three policies. The policy 𝜋1 is more “covering” than 𝜋2 and 𝜋3 , with a lower forward 𝐾 𝐿 ( 𝑝 || 𝜋),
but it is less “focussed” on the valid region 𝐴 than either 𝜋2 or 𝜋3 , which are both concentrated on 𝐴 (with
𝜋2 ( 𝐴) = 𝜋3 ( 𝐴) = 0.9), but with different peaks. Despite the fact that the reverse 𝐾 𝐿 ( 𝜋 || 𝑝) is infinite for the three
policies, the divergences, for 𝛼 close to 1 — while large (and tending to infinity) — still show a clear order, with
𝐷 𝑓𝛼 ( 𝜋1 , 𝑝) much higher than 𝐷 𝑓𝛼 ( 𝜋3 , 𝑝), which in turn is slightly higher than 𝐷 𝑓𝛼 ( 𝜋2 , 𝑝).

More in detail, we consider the discrete space Y = { 𝑦1 , 𝑦2 , 𝑦3 }, over which the base model 𝜋𝑏𝑎𝑠𝑒 has an (almost)
uniform distribution 𝜋𝑏𝑎𝑠𝑒 = (0.33, 0.34, 0.33), and where the binary verifier 𝑣 ( 𝑦 ) takes the values (1, 0, 1), i.e.
accepts 𝑦1 and 𝑦3 and rejects 𝑦2 . This results in the target distribution:
                                                             𝑝 = (0.5, 0, 0.5) .

We study three alternative policies, with distributions:
                   𝜋1 = 𝜋𝑏𝑎𝑠𝑒 = (0.33, 0.34, 0.33) ,              𝜋2 = (0.8, 0.1, 0.1) ,           𝜋3 = ( 𝜖, 0.1, 1 − 𝜖) ,

taking 𝜖 = 0.01. 𝜋1 is the more diverse/covering of the three, but has some significant mass on the invalid point
𝑦2 , while 𝜋2 and 𝜋3 waste less mass on the invalid point, and are peaky on the first point and the third point
respectively, even more so for 𝜋3 .
The endpoints recover the forward and reverse KL divergences:
                                    lim 𝐷 𝑓𝛼 ( 𝜋 ∥ 𝑝) = KL( 𝑝 ∥ 𝜋) ,       lim 𝐷 𝑓𝛼 ( 𝜋 ∥ 𝑝) = KL( 𝜋 ∥ 𝑝) ,
                                    𝛼→0                                    𝛼→1

where we adopt the usual conventions that KL( 𝑝 ∥ 𝜋) = +∞ whenever 𝑝 charges a point on which 𝜋 vanishes, and
similarly for KL( 𝜋 ∥ 𝑝).
In our setting, 𝑝 ( 𝑦2 ) = 0 while each 𝜋𝑖 assigns positive mass to 𝑦2 , so KL( 𝜋𝑖 ∥ 𝑝) = +∞ for 𝑖 = 1, 2, 3.

Numerical values. Table 5 reports 𝐷 𝑓𝛼 ( 𝜋𝑖 ∥ 𝑝) for a range of representative 𝛼 values, including the limiting cases
𝛼 = 0 and 𝛼 = 1.

Curves as a function of 𝛼.           Figure 11 shows the curves 𝛼 ↦→ 𝐷 𝑓𝛼 ( 𝜋𝑖 ∥ 𝑝) for 𝑖 = 1, 2, 3 on 𝛼 ∈ (0, 1).
On the left of the plot, with 𝛼 at 0, we see that 𝜋1 , which is the more diverse/covering of the three relative to 𝑝,
has the lowest value of forward KL, 𝐾 𝐿 ( 𝑝, 𝜋), while 𝜋3 , which is even more “peaky” than 𝜋2 has a larger forward
KL. On the right of the plot, with 𝛼 tending to 1, the divergences all tend to infinity, but their order stabilizes, with
the divergence of 𝜋1 getting and staying much larger than both those of 𝜋2 and 𝜋3 . As we will see in Theorem 5
and equation 32 below, the relative behaviour of the policies for 𝛼 close to 1 is determined predominantly by their
relative values of 𝜋 ( 𝐴), and here, with 𝜋2 ( 𝐴) = 𝜋3 ( 𝐴) = 0.9 > 𝜋1 ( 𝐴) = 0.66, 𝜋1 “loses” relative to 𝜋2 and 𝜋3 . For
two policies, such as 𝜋2 , 𝜋3 , which have exactly the same “valid” mass, their order is determined by a secondary
term, the one appearing to the right of ‘+’ in equation 32.
  4 In some “pathological” situations, and for an infinite sample space Y, 𝐾𝐿 ( 𝑝 | | 𝑞 ) can be infinite even when the supports coincide.




                                                                                                                                             24
                  Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



          Distribution                             𝛼→0        𝛼 = 0.1        𝛼 = 0.5    𝛼 = 0.7   𝛼 = 0.9   𝛼 = 0.99   𝛼→1
          𝜋1 = (0.33, 0.34, 0.33)                  0.4155     0.4522         0.7504     1.2018    3.4666    34.0658     ∞
          𝜋2 = (0.8, 0.1, 0.1)                     0.5697     0.5585         0.5758     0.6816    1.3252    10.3160     ∞
          𝜋3 = (0.01, 0.1, 0.89)                   1.6677     1.4693         1.0488     1.1827    1.7766    10.5828     ∞

Table 5: Values of 𝐷 𝑓𝛼 ( 𝜋𝑖 ∥ 𝑝) for 𝑝 = (0.5, 0, 0.5) and 𝜋1 , 𝜋2 , 𝜋3 at selected 𝛼 values. For 𝛼 → 0 and 𝛼 → 1 we
recover the forward and reverse KL divergences, respectively.




Figure 11: The divergence 𝐷 𝑓𝛼 ( 𝜋, 𝑝) for 𝜋1 = (0.33, 0.34, 0.33), 𝜋2 = (0.8, 0.1, 0.1), and 𝜋3 = ( 𝜀, 0.1, 0.9 − 𝜀) with
𝜀 = 0.01.


H.3. A decomposition theorem for the 𝛼-divergence for targets with partial support
We now state a useful (and apparently novel) result, which permits a better understanding of what happens in
the situation where the support 𝐴 of the target 𝑝 is strictly contained in the support of the model 𝜋. This result
says that, with 𝜋 ( 𝐴) the 𝜋 mass of 𝐴, and with 𝜋 𝐴 is the “renormalization” of 𝜋 to 𝐴, that is, 𝜋 𝐴 ( 𝑦 ) = 𝜋 ( 𝑦 )/𝜋 ( 𝐴)
for 𝑦 ∈ 𝐴, and for 𝛼 ∈ (0, 1), we have the identity 𝐷 𝑓𝛼 ( 𝜋, 𝑝) = 1−  𝜋 ( 𝐴) 𝛼
                                                                    𝛼 (1− 𝛼 )
                                                                                + 𝜋 ( 𝐴) 𝛼 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝).
This identity is especially interesting for the case of 𝛼 tending to 1. In that case, with 𝜋 full support and 𝜋 ( 𝐴) < 1,
the support of 𝜋 𝐴 is equal to the support of 𝑝, and therefore 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝) tends to a finite value 𝐾 𝐿 ( 𝜋 𝐴 , 𝑝), and the
second term of the identity tends towards a finite value. On the other hand, the first term tends to infinity at a
rate closer and closer to 1−1−𝜋 ( 𝐴)
                                𝛼
                                     , meaning that 𝜋 ( 𝐴) > 𝜋′ ( 𝐴) implies that the divergence of 𝜋 becomes and stays
lower than the divergence of 𝜋 after a certain point 𝛼0 .
                                    ′


In other words, when 𝐴 is the subset of Y for which the binary reward 𝑣 ( 𝑦 ) is equal to 1, and for 𝛼 sufficiently close
to 1, minimizing 𝐷 𝑓𝛼 ( 𝜋𝜃 , 𝑝) is essentially equivalent to maximizing 𝔼𝜋𝜃 𝑣 ( 𝑦 ), the same objective as pure REINFORCE.

Formal Result: the Support Decomposition of 𝛼-Divergence
Let 𝜋 and 𝑝 be probability distributions on a countable sample space 𝑌 . We consider the 𝛼-divergence defined by
the generator function 𝑓𝛼 ( 𝑡 ) = 𝑡 −𝛼𝛼𝑡( 𝛼−−1)
                                            (1− 𝛼 )
                                   𝛼
                                                    for 𝛼 ∈ (0, 1).
First, we establish the algebraic relationship between the divergence and the “Hellinger sum” (the discrete
counterpart to the Hellinger integral [37], see also Appendix B of [35]).
Lemma 4 (Connection to Hellinger sum). Let 𝛼 ∈ (0, 1). Let 𝐴 = supp( 𝑝) ⊆ 𝑌 . The 𝛼-divergence satisfies:

                                                                             1 − 𝐻𝛼 ( 𝜋, 𝑝)
                                                            𝐷 𝑓𝛼 ( 𝜋, 𝑝) =                  ,                                (31)
                                                                               𝛼 (1 − 𝛼)

where 𝐻𝛼 ( 𝜋, 𝑝) =                          𝑝 ( 𝑦 ) 1− 𝛼 is the Hellinger sum. This holds even if supp( 𝜋) ⊈ 𝐴.
                     Í
                         𝑦 ∈𝑌 𝜋 ( 𝑦 )
                                        𝛼




                                                                                                                               25
                  Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Proof. We use the extended definition of 𝑓 -divergence [45] which includes the boundary term for the set where
𝑝 ( 𝑦 ) = 0 but 𝜋 ( 𝑦 ) > 0. Let 𝐴𝑐 = 𝑌 \ 𝐴 and let 𝜖 = 𝜋 ( 𝐴𝑐 ) be the “leakage” mass.
                                                                             
                                                       ∑︁               𝜋( 𝑦)
                                        𝐷 𝑓𝛼 ( 𝜋, 𝑝) =     𝑝 ( 𝑦 ) 𝑓𝛼           + 𝑓𝛼′ (∞) · 𝜋 ( 𝐴𝑐 ) .
                                                       𝑦∈𝐴
                                                                        𝑝( 𝑦)

1. The Boundary Term: The term to the right uses the constant 𝑓𝛼′ (∞) = lim𝑡→∞ 𝑓𝛼 ( 𝑡 )/𝑡 . For 𝛼 < 1, 𝑡 𝛼−1 → 0, so:
𝑓𝛼′ (∞) = 𝛼 ( 𝛼−−1)
                𝛼
                    = 1−1 𝛼 . See also Table 1.
2. The Sum on Support 𝐴: Note that 𝑦 ∈ 𝐴 𝜋 ( 𝑦 ) = 1 − 𝜖 and 𝑦 ∈ 𝐴 𝑝 ( 𝑦 ) = 1.
                                                    Í                         Í

                                                                "                                                 #
                                                           1
                                                 
                          ∑︁                𝜋( 𝑦)                 ∑︁
                                                                            𝛼      1− 𝛼
                               𝑝 ( 𝑦 ) 𝑓𝛼           =                  𝜋( 𝑦) 𝑝( 𝑦)      − 𝛼 (1 − 𝜖) − (1 − 𝛼) (1)
                          𝑦∈𝐴
                                            𝑝( 𝑦)     𝛼 ( 𝛼 − 1) 𝑦 ∈ 𝐴
                                                      1
                                            =                 [ 𝐻𝛼 ( 𝜋, 𝑝) − 1 + 𝛼𝜖] .
                                                𝛼 ( 𝛼 − 1)

3. Combination: Adding the boundary term: Boundary = 1−𝜖 𝛼 = 𝛼 (−𝛼𝛼𝜖
                                                                  −1) . The terms involving 𝜖 cancel perfectly:

                                                    𝐻𝛼 ( 𝜋, 𝑝) − 1 + 𝛼𝜖 − 𝛼𝜖   1 − 𝐻𝛼 ( 𝜋, 𝑝)
                                   𝐷 𝑓𝛼 ( 𝜋, 𝑝) =                            =                .
                                                            𝛼 ( 𝛼 − 1)           𝛼 (1 − 𝛼)
                                                                                                                            □

Using Lemma 4, we now derive the main decomposition theorem.
Theorem 5 (Support Decomposition). Assume that 𝐴 = supp( 𝑝) is strictly included in supp( 𝜋). Let 𝜋 𝐴 be the
renormalization of 𝜋 on 𝐴, i.e., 𝜋 𝐴 ( 𝑦 ) = 𝜋 ( 𝑦 )/𝜋 ( 𝐴) for 𝑦 ∈ 𝐴, or, equivalently 𝜋 𝐴 ( 𝑦 ) = 𝜋 ( 𝑦 | 𝐴). The divergence
decomposes as:
                                                     1 − 𝜋 ( 𝐴) 𝛼
                                     𝐷 𝑓𝛼 ( 𝜋, 𝑝) =               + 𝜋 ( 𝐴) 𝛼 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝) .                            (32)
                                                      𝛼 (1 − 𝛼)     |        {z           }
                                                                             Shape Divergence
                                                     | {z }
                                                          Leakage Penalty


Proof. Since 𝑝 ( 𝑦 ) = 0 for 𝑦 ∉ 𝐴, the Hellinger sum restricts to 𝐴. Substituting 𝜋 ( 𝑦 ) = 𝜋 ( 𝐴) 𝜋 𝐴 ( 𝑦 ):

                                                ( 𝜋 ( 𝐴) 𝜋 𝐴 ( 𝑦 )) 𝛼 𝑝 ( 𝑦 ) 1−𝛼 = 𝜋 ( 𝐴) 𝛼 𝐻𝛼 ( 𝜋 𝐴 , 𝑝) .
                                             ∑︁
                                𝐻𝛼 ( 𝜋, 𝑝) =
                                             𝑦∈𝐴

From Lemma 4, we have 𝐻𝛼 ( 𝜋 𝐴 , 𝑝) = 1 − 𝛼 (1 − 𝛼) 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝). Substituting this back into the global divergence
formula:
                                                      1 − 𝜋 ( 𝐴) 𝛼 𝐻𝛼 ( 𝜋 𝐴 , 𝑝)
                                     𝐷 𝑓𝛼 ( 𝜋, 𝑝) =
                                                            𝛼 (1 − 𝛼)
                                                      1 − 𝜋 ( 𝐴) 𝛼 1 − 𝛼 (1 − 𝛼) 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝)
                                                                                                
                                                    =
                                                                       𝛼 (1 − 𝛼)
                                                      1 − 𝜋 ( 𝐴) 𝛼
                                                    =              + 𝜋 ( 𝐴) 𝛼 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝) .
                                                       𝛼 (1 − 𝛼)
                                                                                                                            □

Consequences for Fixed Target 𝑝
We analyze the case where 𝜋 has full support and 𝑝 has strictly partial support 𝐴.
Remark 1 (Limit 𝛼 → 1: The Strong Constraint). As 𝛼 → 1, 𝐷 𝑓𝛼 converges to the Reverse KL divergence 𝐷 𝐾𝐿 ( 𝜋 ∥ 𝑝) =
+∞. The Mass Penalty term diverges:
                                              1 − 𝜋 ( 𝐴) 𝛼
                                            lim            = +∞             (if 𝜋 ( 𝐴) < 1) .
                                           𝛼→1 𝛼 (1 − 𝛼)

This acts as a strong constraint, heavily penalizing support leakage.
As for the Shape divergence term 𝜋 ( 𝐴) 𝛼 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝), it remains finite, and is dominated by the first term.


                                                                                                                           26
                   Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity



Remark 2 (Limit 𝛼 → 0: The Weak Constraint). As 𝛼 → 0, 𝐷 𝑓𝛼 converges to the Forward KL divergence 𝐷 𝐾𝐿 ( 𝑝 ∥ 𝜋).
The Mass Penalty term remains finite:
                                          1 − 𝜋 ( 𝐴) 𝛼
                                      lim              = − ln( 𝜋 ( 𝐴)) .
                                      𝛼→0 𝛼 (1 − 𝛼)

This acts as a soft constraint (“Surprise Penalty”), allowing a trade-off between coverage (𝜋 ( 𝐴)) and conditional shape
matching ( 𝐷 𝐾𝐿 ( 𝑝 ∥ 𝜋 𝐴 )). The Shape divergence term 𝜋 ( 𝐴) 𝛼 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝) also remains finite and converges to 𝐷 𝑓𝛼 ( 𝜋 𝐴 , 𝑝).




                                                                                                                                   27
