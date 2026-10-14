                                                    Quantifying Empirical Compute-Supervision Tradeoffs in RLVR


                                                     Ryo Mitsuhashi * 1 Patrick Chen * 1 Isabelle Tseng * 1 Jasin Cekinmez * 1 Addison J. Wu * 1


                                                                  Abstract                                    negatives, fail to capture all aspects of correctness, or pro-
                                                                                                              vide delayed and sparse signals (Cai et al., 2025; Plesner
                                              Reinforcement learning with verifiable rewards
                                                                                                              et al., 2026). Despite the growing reliance on such im-
                                              (RLVR) has become a standard paradigm for post-
                                                                                                              perfect supervision, it remains unclear whether additional
arXiv:2605.25252v2 [cs.LG] 27 May 2026




                                              training language models, but in practice, verifiers
                                                                                                              compute can offset errors in the verifier, or whether such
                                              are rarely perfect. Recent theoretical work pre-
                                                                                                              errors ultimately cap or even degrade true performance.
                                              dicts that verifier noise affects the rate of learning
                                              but not its final outcome, implying that sufficient             In this work, we study the compute–supervision tradeoff in
                                              compute should close any gap induced by im-                     RLVR by jointly scaling post-training compute and verifier
                                              perfect supervision. We test this prediction em-                quality. Our central question is whether additional compute
                                              pirically by post-training Qwen2.5 (0.5B, 1.5B)                 can compensate for degraded supervision, and whether this
                                              with GRPO on GSM8K while injecting controlled                   compensation is complete, partial, or fundamentally lim-
                                              false-positive and false-negative noise into the bi-            ited. Recent theoretical work predicts that verifier noise
                                              nary correctness signal, and varying rollouts per               affects only the rate of learning, not its final outcome (Rad
                                              prompt as a compute axis. In practice, the gap                  et al., 2026). To investigate the degree to which this finding
                                              in validation accuracy persists under substantial               transfers in practice, we treat verifier reliability as a control-
                                              compute scaling, with returns to compute that are               lable scaling variable alongside compute. We train language
                                              sharply diminishing. We further find a structural               models on tasks with exact ground-truth evaluation, using
                                              asymmetry where false negatives monotonically                   a simple baseline setting of mathematical reasoning, while
                                              degrade performance more quickly than false pos-                systematically introducing controlled imperfections into the
                                              itives. These findings suggest verifier quality and             training verifier and varying the total amount of compute
                                              training compute are not interchangeable, and that              that can be used.
                                              reducing false negatives is a more effective lever
                                                                                                              Our primary goal is to recover compute–verifier tradeoff
                                              than scaling compute alone.
                                                                                                              curves that quantify how much additional compute is re-
                                                                                                              quired to reach a fixed level of true performance under
                                                                                                              degraded supervision. By making this tradeoff explicit, we
                                         1. Introduction                                                      aim to clarify when RLVR can rely on imperfect automated
                                         Reinforcement learning with verifiable rewards (RLVR) has            feedback. Empirically, we find that performance improves
                                         recently emerged as a scalable paradigm for training lan-            only sub-linearly with additional compute and cannot close
                                         guage models without relying on costly human supervision             the gap induced by noisy verifiers, shedding light on prac-
                                         (Lambert et al., 2024; Guo et al., 2025). Reward signals are         tical limitations of previous theoretical claims stating that
                                         produced by automatic evaluators such as symbolic check-             compute alone is sufficient.
                                         ers or unit tests, enabling large-scale optimization driven
                                         entirely by programmatic feedback (Le et al., 2022; Liu              2. Related Work
                                         et al., 2023). However, in realistic settings, these verifiers
                                         are rarely perfect: they may produce false positives or false        2.1. Scaling Laws
                                           *
                                             Equal contribution 1 Princeton University. Correspon-            Scaling laws are a central component of machine learning,
                                         dence to:     Ryo Mitsuhashi <rm4411@princeton.edu>,                 providing a framework for understanding how model perfor-
                                         Patrick Chen <patrickchen@princeton.edu>,        Isabelle            mance varies with compute, data, and model size. Kaplan
                                         Tseng <isabelletseng@princeton.edu>, Jasin Cekinmez                  et al. (2020) show that language model performance fol-
                                         <jasincekinmez@princeton.edu>, Addison J. Wu <addis-
                                         onwu@princeton.edu>.
                                                                                                              low power law relationships with these factors. However,
                                                                                                              Hoffmann et al. (2022) demonstrate that many models are
                                         Accepted to the 1st Workshop on Combining Theory and Bench-          undertrained relative to their available data, highlighting the
                                         marks, CTB@ICML 2026, Seoul, South Korea. Copyright 2026             importance of properly balancing these variables. Given
                                         by the author(s).

                                                                                                          1
                                              Quantifying Empirical Compute-Supervision Tradeoffs in RLVR



                                                                    Response             Ground-truth               Perturbed
                                                                     Rollouts          verifier responses      verifier responses




                                                                       ...




                                                                                              ...




                                                                                                                      ...
                                                                       4
                                                                                                       Flip w.p. 𝑝
              If Bob has 7 apples and gives




                                                                       ...




                                                                                              ...
                                                                                                                                    GRPO




                                                                                                                      ...
                 Alice 3 apples, how many
                apples does Bob have left?
                                                                       9
                                                                                                       Flip w.p. 𝑥




                                                                       ...




                                                                                              ...




                                                                                                                      ...
Figure 1. Noisy-reward GRPO pipeline. Given a prompt, the policy model samples a group of response rollouts that are scored by a
ground-truth verifier. We then perturb the verifier signal by independently flipping correct rewards to incorrect with probability pp p and
incorrect rewards to correct with probability xx x, yielding an asymmetrically noisy reward that is passed to GRPO for policy updates.


the importance of allocating compute and data effectively                           RLVR post-training for frontier LLMs. Baker et al. (2025)
and the lack of strong understanding of scaling laws in                             show that optimization pressure against a CoT monitor pro-
RL settings, developing scaling laws under RLVR becomes                             duces obfuscated reward hacking rather than eliminating it,
paramount.                                                                          and Von Arx et al. (2025) report that more capable models
                                                                                    hack more aggressively. Our research question and setting
2.2. Reinforcement Learning with Verifiable Rewards                                 differs in that we model the verifier as stochastically noisy
                                                                                    rather than systematically exploitable. Concretely, we ask
Verifiable rewards are signals with objective, checkable out-                       whether additional training-time compute compensates for
puts that enable more stable reinforcement learning. How-                           degraded verifier quality rather than whether optimization
ever, many settings rely on noisier rewards for example                             induces drift against a fixed flawed objective.
RLHF (Yan et al., 2024). Rad et al. (2026) characterize
learning dynamics under noisy verification, showing that
positive signal leads to improvement and proving that noise                         3. Methodology
affects the rate but not the asymptotic outcome of learning.                        Training setup
We complement this by quantifying how much compute is
required to realize this equivalence in practice, and find that                     We post-train Qwen2.5 0.5B and 1.5B (Qwen Team, 2025)
the gap persists well beyond realistic training budgets. Other                      with GRPO (Shao et al., 2024) on GSM8K (Cobbe et al.,
work studies correcting noisy rewards during training (Cai                          2021), using the NeMo-RL codebase (NVIDIA, 2025)1
et al., 2025) or the limits of inference-time scaling under im-                     modified to support a configurable noisy verifier. We chose
perfect verifiers (Stroebl et al., 2026), but does not address                      GSM8K because its binary correctness signal provides a
training-time tradeoffs. In contrast, we study training-time                        clean base reward into which we can inject controlled noise.
compute scaling under imperfect supervision, directly                               All runs use AdamW with learning rate 5 × 10−6 , weight
testing whether increased optimization can offset degraded                          decay 0.01, betas (0.9, 0.999), and gradient clipping at 1.0.
verifier quality or instead leads to persistent performance                         A linear warmup over 50 steps (from factor 0.1) is followed
gaps.                                                                               by a constant schedule. KL regularization against the refer-
                                                                                    ence policy uses a coefficient of 0.01 with the k3 estimator,
2.3. Reward Overoptimization and Hacking                                            and PPO-style importance-ratio clipping at 0.2. Generation
                                                                                    is handled by vLLM (Kwon et al., 2023) at temperature 1.0.
An adjacent line of work examines flawed signals in reward
functions and their downstream consequences of optimizing                           Noisy verifier model
to these signals. Gao et al. (2023) establish scaling laws
for reward model overoptimization, showing that KL diver-                           We model an imperfect verifier as a stochastic perturbation
gence from the initial policy predicts the gap between proxy                        of the ground-truth binary reward. Given the true correct-
and true reward as the policy exploits reward model weak-                           ness label y ⋆ ∈ {0, 1} produced by the GSM8K checker,
nesses, a phenomenon formalized as reward hacking (Skalse                              1
                                                                                       Our code is available here: https://github.com/
et al., 2022; Pan et al., 2022). Recent work documents this in                      rm-3284/RLVR_noisy_rewards.git


                                                                                2
                                   Quantifying Empirical Compute-Supervision Tradeoffs in RLVR




Figure 2. Validation accuracies for Qwen2.5 1.5B after GRPO post-training with verifiers of varying degradation, for rollout counts of 8,
16, 32, respectively, in the three sub-plots. Higher validation accuracies are obtained for lower false positive and negative rates, and this is
also increased with additional rollouts. All heatmaps in this paper use the same universal color-accuracy scale. See Section 4 for the
specific scaling trends.




                                       Figure 3. Scaling laws on 1.5B with best validation accuracy


the training reward is flipped independently with probability              liminary experiments varying both rollouts and batch size
p when y ⋆ = 1 (false negative) and with probability x when                showed that batch size had a negligible effect on the training
y ⋆ = 0 (false positive). The effective reward is                          curve while rollout count materially affected training stabil-
                  
                           ⋆              ⋆
                                                                           ity and final performance, so we fix batch size at 32 and vary
                  1 − y w.p. p if y = 1,
                                                                          only r. This is consistent with the view that rollout count
              r = 1 − y w.p. x if y ⋆ = 0,
                           ⋆
                                                                           directly controls the effective number of gradient updates
                  
                   ⋆
                     y         otherwise.                                  per unit of training data in GRPO, making it the natural
                                                                           compute axis for this setting.
as shown in Figure 1. This parameterization lets us inde-
pendently vary the false-negative rate p and false-positive
                                                                           Training and evaluation protocol
rate x, covering the full space of symmetric and asymmetric
noise regimes. We sweep p, x ∈ {0, 0.1, 0.2, 0.3, 0.4, 0.5},               For each (p, x, r) configuration, we run one seed for one
where (p, x) = (0, 0) is the perfect verifier and (0.5, 0.5)               epoch. We chose one epoch because preliminary runs
corresponds to completely random noise. Noise is applied                   showed that the training reward curve plateaus well before
only during training. All hold-out evaluations use the ex-                 the end of an epoch across all noise levels, so additional
act GSM8K verifier, so reported accuracies measure true                    epochs do not reflect further learning but only additional
capability rather than noisy reward.                                       exposure to the same data under the same noise realization.
                                                                           We report both final-step validation accuracy (main text)
Compute axis                                                               and best-step validation accuracy across training (appendix)
                                                                           as a robustness check against late-training instability. For
We treat the number of GRPO rollouts per prompt r as our
                                                                           both the 1.5B model and 0.5B model, we ran N = 108
compute-scaling variable, sweeping r ∈ {8, 16, 32}. Pre-

                                                                       3
                                Quantifying Empirical Compute-Supervision Tradeoffs in RLVR

                                                                       strongest degradation when both are high. Increasing com-
                                                                       pute (r = 8 → 32) improves performance across all noise
                                                                       levels but cannot eliminate noise-induced gaps. False neg-
                                                                       atives additionally impact validation accuracy more than
                                                                       false positives.
                                                                       Maximizing the fitted surface over the sampled region
                                                                       [0, 0.5]2 yields an optimum at (p, x) ≈ (0, 0.3), with pre-
                                                                       dicted accuracy roughly 0.07 higher than a perfect verifier
                                                                       (0, 0). The optimum sits on the p = 0 boundary, indicating
                                                                       that false negatives monotonically hurt training while a mod-
                                                                       erate rate of false positives is beneficial. This asymmetry
                                                                       is consistent with prior analyses in which false negatives
                                                                       deprive the policy of informative gradients, whereas false
                                                                       positives act as a form of reward perturbation that can regu-
                                                                       larize training (Plesner et al., 2026).
                                                                       To ensure robustness, we also report our findings using the
Figure 4. Predicted vs. actual final validation accuracy on 1.5B       best validation accuracy in each configuration across all
model. Adjusted R2 = 0.782.                                            time steps. We observed a similar trend, including with the
                                                                       0.5B model, and full results can be found in Appendix A.

configurations across the full (p, x, r) grid.
                                                                       5. Conclusion
4. Results                                                             We provide a compute-constrained perspective on RL post-
                                                                       training, showing that performance improves minimally
Model details                                                          with additional compute, leading to diminishing returns.
We model trained-model accuracy as a second-order polyno-              As a result, increased compute cannot eliminate the perfor-
mial in the verifier’s false-positive rate x and false-negative        mance degradation caused by noisy verifiers, and the gap
rate p, plus a log-linear term in rollouts r to get validation         persists under substantial scaling. These findings quantify
accuracy                                                               the limits of compute as a substitute for verifier quality and
                                                                       suggest a more practical takeaway, improving the verifier
y ≈ a · x2 + b · x · p + c · p2 + d · x + e · p + f log r + g          particularly by reducing false negatives is a far more ef-
                                                                       fective route for performance gains than scaling compute
The polynomial part is a second-order Taylor expansion                 alone.
of an arbitrary smooth dependence on the two error rates
around the perfect verifier point (0, 0). Our r-values are             Due to compute constraints, our post-training experiments
geometrically spaced r ∈ {8, 16, 32}, so log r treats them             are limited to relatively small Qwen models, however the
as evenly spaced in the regressor; we do not claim to resolve          observed trends are consistent with our underlying hy-
the functional form in r from only three values. We chose              pothesis and are likely to extend to larger and more di-
log r because it aligns with the standard practice of studying         verse model families. Our experiments are conducted on
RL training effects on a multiplicative compute scale.                 GSM8K (Cobbe et al., 2021), which consists of relatively
                                                                       simple arithmetic reasoning tasks. However, the fact that
Scaling observations on 1.5B model                                     gaps still persist in this simpler setting likely suggest that
                                                                       such trends still hold in more complex settings where im-
To provide better generalization of our results, we report our         perfect verifiers are more common. While we quantify the
findings on the final validation accuracy for each configura-          impact of noisy supervision, particularly false negatives as
tion. Across our configurations on the 1.5B model, we have             a key limitation, we do not propose mitigation strategies in
N = 108 observations and get the curve                                 this work, and developing methods to address these issues
                                                                       remains an important direction for future work. Lastly, we
  y = −0.936x2 − 1.052p2 − 1.978xp                                     run one seed per configuration due to compute constraints.
            + 0.565x + 0.577p + 0.0344 log2 r + 0.508                  The overall trends are robust across the sweep, although
                                                                       individual configurations, especially the boundary optimum
with adjusted R2 = 0.782. See Figure 4 for the detailed fit.           near (p, x) ≈ (0, 0.3), should be interpreted carefully.
As visible from Figure 2, validation accuracy decreases
as false positive and false negative rates increase, with

                                                                   4
                               Quantifying Empirical Compute-Supervision Tradeoffs in RLVR

References                                                           Liu, J., Zhu, Y., Xiao, K., Fu, Q., Han, X., Yang, W., and Ye,
                                                                       D. RLTF: Reinforcement learning from unit test feedback.
Baker, B., Huizinga, J., Gao, L., Dou, Z., Guan, M. Y.,
                                                                       TMLR, 2023.
  Madry, A., Zaremba, W., Pachocki, J., and Farhi, D. Mon-
  itoring reasoning models for misbehavior and the risks of          NVIDIA. Nemo rl: A scalable and efficient post-training li-
  promoting obfuscation. arXiv preprint arXiv:2503.11926,             brary. https://github.com/NVIDIA-NeMo/RL,
  2025.                                                               2025. GitHub repository.

Cai, X.-Q., Wang, W., Liu, F., Liu, T., Niu, G., and                 Pan, A., Bhatia, K., and Steinhardt, J. The effects of reward
  Sugiyama, M. Reinforcement learning with verifiable yet              misspecification: Mapping and mitigating misaligned
  noisy rewards under imperfect verifiers. arXiv preprint              models. In ICLR, 2022.
  arXiv:2510.00915, 2025.
                                                                     Plesner, A., Guzman, F., and Athalye, A. An imperfect
Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,              verifier is good enough: Learning with noisy rewards.
  Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,            arXiv preprint arXiv:2604.07666, 2026.
  R., Hesse, C., and Schulman, J. Training verifiers to solve
                                                                     Qwen Team. Qwen2.5 technical report. arXiv preprint
  math word problems. arXiv preprint arXiv:2110.14168,
                                                                      arXiv:2412.15115, 2025.
  2021.
                                                                     Rad, A., Filom, K., Keivan, D., Esfahani, P. M., and Ka-
Gao, L., Schulman, J., and Hilton, J. Scaling laws for reward          malinejad, E. Rate or fate? RLVε R: Reinforcement
  model overoptimization. In ICML, 2023.                               learning with verifiable noisy rewards. arXiv preprint
                                                                       arXiv:2601.04411, 2026.
Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu,
  Q., Xu, R., Zhang, R., Ma, S., Bi, X., et al. Deepseek-            Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
  r1 incentivizes reasoning in llms through reinforcement              H., Zhang, M., Li, Y. K., Wu, Y., and Guo, D. DeepSeek-
  learning. Nature, 2025.                                              Math: Pushing the limits of mathematical reasoning in
                                                                       open language models. arXiv preprint arXiv:2402.03300,
Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E.,               2024.
  Cai, T., Rutherford, E., de Las Casas, D., Hendricks,
  L. A., Welbl, J., Clark, A., et al. An empirical analysis of       Skalse, J., Howe, N. H. R., Krasheninnikov, D., and Krueger,
  compute-optimal large language model training. NeurIPS,              D. Defining and characterizing reward hacking. In
  2022.                                                                NeurIPS, 2022.

Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B.,              Stroebl, B., Kapoor, S., and Narayanan, A. The limits of
  Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and             inference scaling through resampling. In ICLR, 2026.
  Amodei, D. Scaling laws for neural language models.                Von Arx, S., Chan, L., and Barnes, E. Recent frontier
  arXiv preprint arXiv:2001.08361, 2020.                               models are reward hacking. METR Blog, 2025.
Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,              Yan, Y., Lou, X., Li, J., Zhang, Y., Xie, J., Yu, C., Wang,
 C. H., Gonzalez, J. E., Zhang, H., and Stoica, I. Efficient           Y., Yan, D., and Shen, Y. Reward-robust RLHF in LLMs.
 memory management for large language model serving                    arXiv preprint arXiv:2409.15360, 2024.
 with pagedattention. In Proceedings of the ACM SIGOPS
 29th Symposium on Operating Systems Principles, 2023.

Lambert, N., Morrison, J., Pyatkin, V., Huang, S., Ivison,
  H., Brahman, F., Miranda, L. J. V., Liu, A., Dziri, N., Lyu,
  X., Gu, Y., Malik, S., Graf, V., Hwang, J. D., Yang, J.,
  Le Bras, R., Tafjord, Ø., Wilhelm, C., Soldaini, L., Smith,
  N. A., Wang, Y., Dasigi, P., and Hajishirzi, H. Tülu 3:
  Pushing frontiers in open language model post-training.
  arXiv preprint arXiv:2411.15124, 2024.

Le, H., Wang, Y., Gotmare, A. D., Savarese, S., and Hoi,
  S. C. H. CodeRL: Mastering code generation through
  pretrained models and deep reinforcement learning. In
  NeurIPS, 2022.

                                                                 5
                              Quantifying Empirical Compute-Supervision Tradeoffs in RLVR

A. Extended Results
  Model size    Final/Best                                Fit equation                                 Adj.-R2
    1.5B          Final       −0.936x2 − 1.052p2 − 1.978xp + 0.565x + 0.577p + 0.0344 log2 r + 0.508    0.782
    1.5B           Best       −0.668x2 − 0.867p2 − 1.694xp + 0.450x + 0.506p + 0.0213 log2 r + 0.604    0.720
    0.5B          Final       −0.389x2 − 0.617p2 − 0.926xp − 0.088x + 0.114p + 0.0621 log2 r + 0.216    0.850
    0.5B           Best       −0.386x2 − 0.601p2 − 0.990xp + 0.077x + 0.204p + 0.0317 log2 r + 0.366    0.862
                                            Table A1. Curves for each configuration


We show the full results for 1.5B and 0.5B in Table A1.

B. Supplementary Figures




                                 Figure A1. Scaling laws on 0.5B with final validation accuracy




                             Figure A2. Predicted vs. Actual final validation accuracy on 0.5B model




                                 Figure A3. Scaling laws on 0.5B with best validation accuracy


                                                               6
                                Quantifying Empirical Compute-Supervision Tradeoffs in RLVR




                              Figure A4. Predicted vs. Actual best validation accuracy on 0.5B model


C. Analysis on Symmetric Error Cases
On cases with symmetric error rates (p = x), we expand the number of rollouts to r ∈ {4, 8, 16, 32, 64}.
Figure A5 shows the final accuracy with various error rates and rollouts. In most cases, the final accuracy increases as you
increase the number of rollouts. However, we could see some plateaus with the bigger model when the number of rollouts is
large, and the error rate is low, suggesting that the model has reached its capacity limit. This also shows the shortcomings of
our polynomial approximation, as it does not take into account the model size and treats every rollout increase (4 to 8 vs
32 to 64) equally. It is notable that in many cases, the increase in compute eventually compensates for the error rate, as
(p, r) = (0.3, 64) beats (0.0, 4) in Qwen 1.5B and (0.4, 64) beats (0.0, 4) in Qwen 0.5B.




Figure A5. The relationship between the final accuracy and number of rollouts with symmetric noise. Qwen2.5 1.5B on the left and
Qwen2.5 0.5B on the right.

Figure A6 shows the accuracy curves of the GRPO with extreme rollouts, 4 and 64. Increasing the error rates not only
affects the final accuracy but also the slope of the accuracy curve. When the error rate is high, it takes considerably more
steps to reach the final accuracy level. This suggests another compute-error rate tradeoff that we do not explore in this paper,
which is the steps it takes to a certain accuracy and the error rate of the verifier. Also, the rollout influences the stability of
the accuracy curve, especially when the error rate is high. This shows another reason, other than the final accuracy and the
speed of learning, why it is better to have a large number of rollouts when the verifier is noisy.



                                                                7
                       Quantifying Empirical Compute-Supervision Tradeoffs in RLVR




(a) The learning curve of GRPO with rollout 4.                   (b) The learning curve of GRPO with rollout 64.
  Figure A6. The changes in validation accuracy throughout the training of Qwen2.5-1.5B with symmetric noise.




                                                      8
