                                                                    Rewarding the Unlikely: Lifting GRPO
                                                                      Beyond Distribution Sharpening


                                                     Andre He                           Daniel Fried                                      Sean Welleck
                                             Carnegie Mellon University           Carnegie Mellon University                        Carnegie Mellon University




                                                                                                     Theorem x                                     Correct Proofs y1 , . . . , yG
                                                                Abstract
                                                                                                     /-- Prove that the sum of two even numbers        := by
                                                                                                     is also even -/                                      -- use closure property of evens
                                              Reinforcement learning is emerging as a pri-                                                              Proof 2
arXiv:2506.02355v2 [cs.LG] 20 Jun 2025




                                                                                                     theorem even_add_even_is_even (a b : N)              exact
                                                                                                                                                         Proof
                                                                                                                                                         Proof 1
                                                                                                                                                                2 Even.add ha hb
                                                                                                     (ha : Even a) (hb : Even b) : Even (a + b)
                                              mary driver for improving language model
                                              reasoning capabilities. A fundamental ques-
                                              tion is whether current reinforcement learn-                                           likely to be included in N samples
                                              ing algorithms—such as Group Relative Pol-
                                              icy Optimization (GRPO), the de facto stan-                          Base Model
                                              dard algorithm used to improve language model                          π0 (y | x)
                                              reasoning—merely sharpen the base model’s
                                                                                                                                                  y1     y2        ...   yG−1 yG
                                              distribution around problems it can already
                                              solve. We investigate this question in the con-
                                              text of formal theorem proving, which has ac-                           GRPO
                                              cess to a perfect verifier. We identify a de-                       πGRPO (y | x)
                                              generate rank bias in GRPO in which highly
                                              probable trajectories are reinforced and rare                                                       y1     y2        ...   yG−1 yG

                                              ones are neglected. This results in distribution
                                              sharpening: the model can solve some prob-                     GRPO-Unlikeliness
                                              lems with fewer samples, but underperforms                        πGRPO−UR (y | x)
                                              simply sampling more solutions from the origi-
                                              nal model. To overcome GRPO’s rank bias we                                                          y1     y2        ...   yG−1 yG
                                              introduce unlikeliness reward, a simple method
                                              for explicitly up-weighting rare but correct so-       Figure 1: We identify a rank bias in GRPO in which
                                              lutions. We show that unlikeliness reward              model updates only reinforce already probable solutions
                                              mitigates rank bias and improves pass@N                and fail to surface new ones. This sharpens the distribu-
                                              across a large range of N in both synthetic            tion and impairs pass@N performance for large N. Our
                                              and real theorem proving settings. We also un-         unlikeliness reward addresses rank bias by explicitly
                                              cover an unexpected link between rank bias             encouraging uplifting low-probability correct solutions.
                                              and a seemingly mundane hyperparameter—
                                              the number of updates per batch—that leads             ation, RL has been applied at scale to elicit com-
                                              to a second, complementary mitigation. We              plex reasoning behaviors using only problem in-
                                              combine our insights into a revised GRPO train-        stances and their corresponding outcome rewards
                                              ing recipe for formal theorem proving, yield-
                                                                                                     (DeepSeek-AI et al., 2025; Yu et al., 2025).
                                              ing an open pipeline that achieves competi-
                                              tive performance to DeepSeek-Prover-V1.5-RL               Formal theorem proving is a particularly attrac-
                                              on the miniF2F-test benchmark. We release              tive domain for studying LLM reasoning. For-
                                              our implementation at https://github.com/              mal systems such as Lean and Isabelle (de Moura
                                              AndreHe02/rewarding-unlikely-release.                  et al., 2015; Paulson, 1994) can verify mathemat-
                                                                                                     ical proofs step-by-step, ensuring that models are
                                                                                                     only rewarded for fully correct solutions. Since ver-
                                         1    Introduction                                           ification is fully automated and immune to spurious
                                         Reinforcement learning (RL) has recently emerged            solutions, formal mathematics serves as an ideal
                                         as a powerful framework for enhancing the reason-           testbed for reinforcement learning algorithms.
                                         ing capabilities of large language models (LLMs).              An important open challenge is designing rein-
                                         In domains such as mathematics and code gener-              forcement learning algorithms that do more than

                                                                                                 1
“sharpen the distribution”—that is, we want the            miniF2F-test benchmark.
RL-trained model to solve problems that cannot
be solved by simply sampling more from the orig-           2     Problem Setup
inal model. Consistent with the findings of Yue            We study the problem of training a language model
et al. (2025), our initial experiments identify this       for formal theorem proving, where the goal is to
as a key limitation of existing RL recipes based on        generate valid proofs of theorems in a proof as-
Group Relative Policy Optimization (GRPO) (Shao            sistant. We use Lean (de Moura et al., 2015), a
et al., 2024), the de facto standard algorithm for         proof assistant based on dependent type theory that
improving LLM reasoning. While GRPO improves               supports the construction and verification of mathe-
single-sample accuracy, it often fails to improve          matical proofs. Lean has recently attracted interest
and can even impair pass@N metrics at larger N             in the AI and mathematics communities (e.g., Yang
in our theorem proving setting (Figure 2). This is         et al. (2024); Tao (2025)).
a significant limitation in domains with a perfect            Let D = {xi }M i=1 be a dataset of theorem state-
verifier, such as formal mathematics, since these          ments. Each statement consists of a natural lan-
domains naturally lend themselves to sampling and          guage description and a formal statement express-
verifying many candidates at test time.                    ing the theorem in Lean. Let R denote the verifier,
   We argue that improving pass@N performance              which also functions as the reward function. Given
requires specifically increasing the probability of        a theorem statement x and a candidate proof y,
low probability correct responses under the model.         the Lean verifier returns a binary reward indicating
We construct a toy model to demonstrate this phe-          whether y constitutes a successful proof of x:
nomenon, and reveal empirically that GRPO suf-
fers from rank bias: a tendency to reinforce already                   R(x, y) = 1{y proves x}.
high-likelihood responses while neglecting the long        We assume access to an initial prover model
tail of rare but correct ones. This reduces sample         πbase (y | x), a large language model (LLM) with
diversity and degrades multi-sample performance            some basic capability to generate proofs. Given
over time. To address this, we introduce Unlike-           a theorem statement x, the model samples a com-
liness Reward, which up-weights correct outputs            pletion y that attempts to prove the statement. Our
that are less likely than others. Doing so dramat-         goal is to fine-tune this model to improve its proof
ically changes how GRPO learns from less likely            success rate, using problem instances from D and
trajectories, translating to more output diversity         the reward signal provided by R.
and higher pass@N across a range of N values.
   Furthermore, we uncover an unexpected link be-          2.1    Evaluation Metric
tween GRPO’s distribution sharpening and a seem-           To evaluate the prover’s performance, we use the
ingly mundane hyperparameter: the number of                pass@N metric, which measures the probability
PPO epochs per batch. Increasing the number of             that at least one of N independently sampled proof
epochs adds extra gradient steps on low-likelihood         attempts succeeds. This metric is widely adopted
sequences after the high-likelihood ones saturate,         in prior work due to its simplicity and close align-
amplifying training signal for unlikely solutions.         ment with the practical use case of generating and
Tuning this often-ignored hyperparameter is a com-         verifying many proof attempts per theorem to find
plementary approach to the unlikeliness reward,            at least one that succeeds.
and offers insight into the optimization dynamics             Let x ∈ Dtest be a theorem, and let {yj }Nj=1 ∼
that can lead to distribution sharpening.                  πθ (· | x) denote N independent samples drawn
   We demonstrate that our revised training recipe         from the model. The empirical pass@N metric for
substantially improves pass@N metrics across a             a single theorem is defined as:
range of values for N , while also substantially                                                         
outperforming standard expert iteration. We com-              pass@N (x; πθ ) = 1 max R(x, yj ) = 1
                                                                                      1≤j≤N
bine unlikeliness reward and our insights into PPO
epochs into a full recipe for reinforcement learn-         The average pass@N score on a test set Dtest =
ing in formal theorem proving. We apply our                {xi }M
                                                                i=1 is the average over individual theorems:
recipe to theorem proving in Lean, resulting in                                       M
a fully open pipeline that achieves competitive per-                            1 X
                                                                 pass@N (πθ ) =     pass@N (xi ; πθ )
formance with DeepSeek-Prover-V1.5-RL on the                                    M
                                                                                    i=1


                                                       2
In the context of reinforcement learning, a high              choice and hyperparameter settings, though we cu-
pass@N also indicates that we are likely to receive           rate our own dataset, as theirs has not been released.
a positive reward signal when sampling N comple-
tions per problem.                                            3.1   Dataset
                                                              The Lean Workbook dataset is a large-scale col-
2.2     Reinforcement Learning
                                                              lection of approximately 140K Lean 4 theorem
We use Group Relative Policy Optimization                     statements that were auto-formalized from natural
(GRPO) as the foundation of our reinforcement                 language math problems (Ying et al., 2024). Since
learning experiments. GRPO was introduced by                  unsolvable problems do not provide useful gradi-
(Shao et al., 2024) and has been successfully ap-             ents during RL, we select a 10K subset of prob-
plied to train models such as DeepSeek-R1 and                 lems that were found to be solvable in Wu et al.
DeepSeek-Prover-V1.5-RL (DeepSeek-AI et al.,                  (2024). These statements are still moderately chal-
2025; Xin et al., 2024), showing strong perfor-               lenging, as the solutions were discovered through
mance in both informal and formal settings.                   an extremely compute-intensive search process. In
   GRPO is an extension of Proximal Policy Opti-              addition, we also include the 244 problems from
mization (PPO) (Schulman et al., 2017) that omits             miniF2F-valid (Zheng et al., 2021).
the critic model. For each question x, GRPO sam-                 From this combined dataset, we hold-out 200
ples a group of outputs {y1 , . . . , yG } ∼ πθold (y |       theorems for validation, leaving 9.6K for training.
x) from the current policy and maximizes the fol-             Although miniF2F-test (Zheng et al., 2021) is a
lowing objective:                                             standard benchmark for theorem proving, we found
                                                              high variance and inconsistent results on it when
      JGRP O (θ)
                                                              training at our scale, likely due to distribution shift
              G
          1 X             πθ (yi | x)                         and large difficulty gaps between problems. Thus,
      =          min                    Ai ,
          G              πθold (yi | x)                       we primarily evaluate on our I.I.D. held-out set
             i=1
                                                !            (Dval ) and only use miniF2F-test for our final large-
                   πθ (yi | x)
                
           clip                  , 1 − ϵ, 1 + ϵ Ai            scale experiments. We will refer to our training and
                  πθold (yi | x)                              validation sets as Dtrain and Dval , respectively.
          − βKL DKL [πθ ∥ πref ]
                                                              3.2   Training
  GRPO differs from PPO in how it computes the                Our implementation of GRPO is built on the verl
advantages Ai . Instead of subtracting a baseline             framework (Sheng et al., 2024), with modifications
predicted by the critic model, GRPO normalizes                to support reward feedback from the Lean REPL.
rewards within the group of samples. Let ri =                 We use the Python wrapper for the Lean REPL
R(x, yi ), then the advantages are computed as:               released by Xin et al. (2024), which we found
                                                              to be more robust than previous open-source al-
                   ri − mean({r1 , . . . , rG })
            Ai =                                              ternatives. The base model is DeepSeek-Prover-
                       std({r1 , . . . , rG })
                                                              V1.5-SFT, which has moderate theorem-proving
  Note that when all or none of the samples solve             capabilities (Xin et al., 2024). We adopt the hy-
the problem, Ai = 0 for all i and there is no                 perparameters reported in Xin et al. (2024) where
gradient with respect to model parameters θ (ex-              available:
cept for the KL term). To be more efficient with
model updates, we implement a trick similar to                   • Learning rate = 5e-6
Dynamic Sampling (Yu et al., 2025). We maintain
                                                                 • KL loss coefficient = 0.02
a buffer of recent samples that have nonzero ad-
vantage and only perform model updates once the
                                                                 • Number of samples per problem = 32.
buffer reaches the target batch size.
                                                              However, we found the original learning rate to be
3     Does GRPO Improve Pass@N?
                                                              unstable and use a reduced value of 1e-6. Due to
We begin by investigating how GRPO behaves                    compute constraints, we only train for one epoch
when applied to formal theorem proving. Our setup             on Dtrain and truncate the response length to 512
closely follows Xin et al. (2024) in terms of model           tokens, which suffices for over 99.5% of samples.

                                                          3
         0.85            Model                                                                                                0.05                                                  p0 values
                    DeepSeek-Prover-V1.5-SFT




                                                                                            Predicted Improvement in pass@N
         0.80
                    GRPO-Default                                                                                                                                                        p0 = 12
                                                                                                                              0.04                                                      p0 = 18
         0.75
                                                                                                                                                                                        p0 = 321
                                                                                                                              0.03
         0.70                                                                                                                                                                           p0 = 128
                                                                                                                                                                                               1
Pass@N




         0.65
                                                                                                                                                                                        p0 = 512
                                                                                                                                                                                               1
                                                                                                                              0.02
         0.60
                                                                                                                              0.01
         0.55

         0.50                                                                                                                 0.00
                1         2         4          8   16       32   64   128   256   512                                                 1    2       4   8   16       32   64   128    256     512
                                                        N
                                                                                                                                                                N
Figure 2: Finetuning DeepSeek-Prover-V1.5-SFT with
                                                                                            Figure 3: Improvement in expected pass@N assuming
GRPO, evaluated on Dval . GRPO improves pass@N
                                                                                            RL increases correct solution probabilities by a factor
significantly for small N , but performs worse than the
                                                                                            of 1 + ϵ with ϵ = 0.2. Each curve corresponds to an
base model for large N . We aim to understand this
                                                                                            initial p0 ∈ 1/2, 1/8, 1/32, 1/128, 1/512.
behavior and develop methods to overcome it.

                                                                                            term. The simplified GRPO objective is:
3.3             GRPO Fails to Improve Pass@N
Figure 2 presents model performance on Dval , eval-                                                                                  JGRPO (θ)
uated up to pass@512. GRPO substantially boosts                                                                                                G
                                                                                                                                          1 X            πθ (yi | x)
pass@1 to pass@16, but the improvement dimin-                                                                                        =          min                  Ai ,
ishes for larger N. This pattern suggests that GRPO                                                                                      G               π0 (yi | x)
                                                                                                                                            i=1
is effective at increasing the likelihood of already                                                                                                                   !
                                                                                                                                            πθ (yi | x)
                                                                                                                                          
probable correct solutions but fails to surface new                                                                                  clip               , 1 − ϵ, 1 + ϵ Ai .
                                                                                                                                            π0 (yi | x)
ones into the high-probability set, which is con-
sistent with the findings of Yue et al. (2025) and                                            We make the simplifying assumption that the
Shao et al. (2024). Note that this is not an inherent                                       probability of each positive sample y+ with Ai >
failure of RL—boosting single-sample accuracy in-                                           0 can be optimized independently. In the GRPO
creases expected reward, but the benefit for formal                                         objective, each sample stops contributing gradient
theorem proving is limited. Next, we consider if                                            once πθ (y+ | x)/π0 (y+ | x) ≥ 1 + ϵ, thus we
and how RL can improve pass@N at large N .                                                  expect that the final ratio is close to the clipping
3.4             Can RL Optimize Pass@N?                                                     bound:
                                                                                                          πRL (y+ | x)
                                                                                                                         ≈ 1 + ϵ.
In this section, we argue that improving pass@N                                                            π0 (y+ | x)
for large N specifically requires RL to increase                                            We can then predict the accuracy of the trained
the probability of low-probability correct solutions                                        model:
under the model.
                                                                                                          pRL ≈ (1 + ϵ)p0
   Suppose that the initial model π0 has a probabil-
ity p0 to solve a problem x, i.e.,                                                                                        E[pass@N (πRL )] ≈ 1 − (1 − (1 + ϵ)p0 )N .
                X                                                                           Figure 3 plots the expected improvement in
                         π0 (y | x) = p0 .
                                                                                            pass@N for different initial p0 . When p0 is large,
                          y s.t. R(x,y)=1
                                                                                            the marginal gain in pass@512 is small. Con-
The expected pass@N can then be expressed as:                                               versely, when p0 is small, gains are negligible
                                                                                            for pass@1. In general, we see that increasing
                    E[pass@N (π0 )] = 1 − (1 − p0 )N .                                      pass@N requires the training algorithm to increase
                                                                                            the probability of solutions with p0 ≈ 1/N . Thus,
Now, we consider how RL training affects p0 . The                                           RL must specifically uplift the probability of low-
exact outcome of taking gradient steps against the                                          probability correct solutions to achieve improve-
GRPO objective is impossible to predict analyti-                                            ments in pass@N for large N .
cally, but we can make estimates by assuming that
we maximize the objective.                                                                  3.5 Does GRPO Reinforce Unlikely Solutions?
   For simplicity, we only consider early training                                          The analysis above, and our empirical observation
steps, so that πθold ≈ π0 , and disregard the KL                                            that GRPO is not increasing pass@N , together

                                                                                        4
                                                                      GRPO-Default           4     Improving GRPO for Multi-Sample
                    0.30
                                                                                                   Performance
                    0.25

                    0.20
                                                                                             While the GRPO objective itself does not inherently
      Uplift Rate



                                                                                             favor high-probability solutions, our earlier analy-
                    0.15
                                                                                             sis revealed a clear empirical bias: low-probability
                    0.10
                                                                                             correct solutions are rarely reinforced. This be-
                    0.05                                                                     havior is counterintuitive – when π0 (y | x) is
                           0      5    10       15       20      25          30
                                                                                             small, increasing the ratio πRL (y | x)/π0 (y | x)
                                       Rank of Sample in Group                               requires less absolute probability mass and con-
Figure 4: Uplift rate uj as a function of rank j among                                       tributes equally to the GRPO objective. In prin-
positive samples. GRPO rarely increases the probability                                      ciple, this should make low-probability solutions
of lowest-ranked (i.e. rarest) correct samples.                                              more attractive to optimize. The observed rank
                                                                                             bias is therefore not a feature of the GRPO loss but
suggest that GRPO may not be effectively uplifting                                           likely a consequence of the optimizer’s biases.
low-probability correct solutions. To verify this,                                              In this section, we introduce the unlikeliness re-
we examine training samples for the first 800 prob-                                          ward to directly counteract this implicit bias, with
lems, computing their probabilities under the initial                                        the goal of improving pass@N performance at
model and final GRPO-trained model.                                                          large N . We also provide complementary analysis
   Let xi be the i-th training problem and yi,j be the                                       on the effect of certain hyperparameters on rank
j-th corresponding solution. We compute π0 (yi,j |                                           bias, which we later incorporate into our overall
xi ) and πGRPO (yi,j | xi ) for all pairs. We are                                            training recipe.
interested in whether πGRPO (yi,j | xi )/π0 (yi,j |                                          4.1    Unlikeliness Reward
xi ) ≈ 1 + ϵ, especially when π0 (yi,j | xi ) is small.
   We find that the raw probability ratios are highly                                        To explicitly correct for rank bias, we propose the
variable, containing extreme outliers, and the scale                                         unlikeliness reward – a simple modification to
of π0 (yi,j | xi ) also differs widely across prob-                                          the reward function that discourages reinforcing
lems. This makes it difficult to analyze the raw                                             already high-probability solutions. For a group of
model probabilities directly. Instead, we use the                                            samples y1 , . . . , yG , let rank(yi ) ∈ {1, 2, . . . , G}
rank of a sample within its group as a proxy for its                                         denote the rank of yi under the current policy
probability and consider the simpler, binary met-                                            πθold (yi | x), with rank 0 corresponding to the
ric of whether πGRPO (yi,j | xi ) is greater than                                            highest-probability sample. We modify the reward
π0 (yi,j | xi ).                                                                             to be
   Formally, for each problem xi , we sort the                                                                     
                                                                                                                               G − rank(yi )
                                                                                                                                               
solutions {yi,1 , . . . , yi,G } in descending order of                                          ri = R(x, yi ) 1 − βrank                          .
                                                                                                                                      G
π0 (yi,j | xi ) to obtain {ỹi,1 , . . . , ỹi,G }. We are in-
terested in the relationship between the rank of a so-                                       A multiplicative penalty is applied to higher-
lution and how likely it is to be uplifted by GRPO.                                          probability solutions, increasing the relative advan-
For each rank j ∈ {1, . . . , G}, we compute the                                             tage of rarer positive samples. Incorrect solutions
"uplift rate", averaging over positive samples:                                              remain unaffected, receiving ri = 0 regardless of
                                                                                             rank. The coefficient βrank controls the strength
  uj =                         mean                                                          of this perturbation; we fix βrank = 0.25 in our
                      i: R(xi ,ỹi,j )=1
                                                                                             experiments.
                           1{πGRPO (ỹi,j | xi ) > π0 (ỹi,j | xi )}
                                                                                     
                                                                                                Moreover, we continue to skip all samples that
   Figure 4 shows a clear positive correlation:                                              have zero advantage before the perturbation. This
GRPO is more likely to increase the probability of                                           ensures that no batch is dominated solely by the
already high-probability correct solutions. In con-                                          unlikeliness reward, and R(x, yi ) still determines
trast, the low-probability positive samples – those                                          the direction of optimization for each sample.
most critical for improving pass@N at large N –
are almost never uplifted. We confirm this behavior                                          4.2    Effects of PPO Epochs
in a controlled toy environment (see Appendix A)                                             In addition to perturbing rewards, we find that in-
and refer to this phenomenon as rank bias.                                                   creasing the number of optimization steps per sam-

                                                                                         5
ple (ppo-epochs) also mitigates rank bias. Stan-             Model                        Solved        ∆ Static
dard implementations of PPO and GRPO typically               Static (V1.5-SFT)          7707 / 9600        –
use a single optimization step per batch (Sun, 2024;         GRPO-Default               7860 / 9600      +153
Sheng et al., 2024; Yu et al., 2025), which we found         GRPO-Epochs-2              8008 / 9600      +301
to produce biased updates. When taking multiple              GRPO-Epochs-3              8006 / 9600      +299
gradient steps, the initial steps may push high-rank         GRPO-Unlikeliness-1        8023 / 9600      +316
solutions beyond the clipping threshold, so that             GRPO-Unlikeliness-2        8065 / 9600      +358
subsequent steps are forced to focus on low-rank
                                                            Table 2: Number of training problems solved during
samples that are still unclipped. In this way, in-
                                                            one epoch on Dtrain . GRPO variants improve over the
creasing ppo-epochs indirectly amplifies learning           static model, with GRPO-Unlikeliness-2 achieving the
signal for low-rank samples.                                largest gain.
   However, increasing ppo-epochs makes training
substantially slower (Appendix B.1) and potentially
unstable. Thus, we prefer the unlikeliness reward           model with no updates. Table 2 reports the number
as the more direct and efficient solution to address        of problems solved by each variant. All GRPO
rank bias.                                                  variants outperform the static model, with GRPO-
                                                            Unlikeliness-2 solving the most problems. Since
5     Experiments                                           training runs for only one epoch, each example is
                                                            effectively unseen at the time of sampling, indicat-
For our main experiments, we use Dtrain and Dval            ing generalization within the epoch.
for training and evaluation. We compare several
GRPO variants with different hyperparameter set-            5.2   Analysis: Rank Bias
tings, summarized in Table 1. We increase the
                                                            To assess whether the proposed methods mitigate
KL penalty because we found that it helps pre-
                                                            rank bias, we repeat the analysis from Section 3.5
vent deteriorating pass@N , but this change alone
                                                            by computing the uj metrics over the training sam-
was not enough to improve pass@N substantially
                                                            ples for each GRPO variant. The results, shown in
(discussed in Appendix D). All unlisted hyperpa-
                                                            Figure 6, indicate substantial changes in GRPO’s
rameters are kept the same.
                                                            behavior. GRPO-Unlikeliness-2 reverses the orig-
      Model                   K    βKL     βrank            inal pattern and is more likely to reinforce low-
                                                            probability solutions. We also show that unlikeli-
      GRPO-Default            1    0.02      –
                                                            ness reward mitigates rank bias in our controlled
      GRPO-Unlikeliness-1     1    0.10    0.25
                                                            environment (see Appendix A.4).
      GRPO-Unlikeliness-2     2    0.10    0.25
                                                               In GRPO-Epochs-2 and GRPO-Epochs-3, the
      GRPO-Epochs-2           2    0.10      –
                                                            bias remains, but the overall strength of reinforce-
      GRPO-Epochs-3           3    0.10      –
                                                            ment is increased so that low-probability solutions
Table 1: Hyperparameter settings for GRPO variants in       are also sufficiently uplifted.
our experiments. K is the number of PPO epochs.
                                                            5.3   Analysis: Sample Diversity
                                                            Throughout training, we track the number of
5.1    Results: Pass@N                                      unique proofs generated per step, shown in Figure 7.
Figure 5 shows the performance of GRPO variants             GRPO-Unlikeliness-2 exhibits unique dynamics
evaluated on Dval . Introducing the unlikeliness re-        where diversity initially drops but later recovers, un-
ward leads to substantial improvements in pass@N            like other variants where diversity declines mono-
at large N, with a minor tradeoff in pass@1 and             tonically. This may reflect a self-correcting mech-
pass@2. Interestingly, increasing PPO epochs also           anism: initially dominant solutions are penalized,
leads to improvements, consistent with our analysis         allowing low-probability correct solutions to resur-
in Section 4.2. However, increasing PPO epochs              face. This continuous rebalancing helps preserve a
leads to a significant increase in training time (Ap-       broad distribution of strategies throughout training.
pendix B.1).                                                   We also observe that higher PPO epochs consis-
   We also track the cumulative accuracy of the             tently increases sample diversity, up to ppo-epochs
32 samples generated per problem during train-              = 4 where training becomes unstable. While this
ing, including the baseline performance of a static         may seem counterintuitive – since more optimiza-

                                                        6
                                        0.90

                                        0.85

                                        0.80

                                        0.75
                               Pass@N
                                        0.70

                                        0.65                                                                                                                      Model
                                                                                                                                                            DeepSeek-Prover-V1.5-SFT
                                        0.60                                                                                                                GRPO-Default
                                                                                                                                                            GRPO-Unlikeliness-1
                                        0.55                                                                                                                GRPO-Unlikeliness-2
                                                                                                                                                            GRPO-Epochs-2
                                        0.50                                                                                                                GRPO-Epochs-3
                                                1         2        4           8        16                                       32            64           128         256         512
                                                                                             N
Figure 5: Performance of GRPO variants on Dval . Both the unlikeliness reward and additional PPO epochs improve
pass@N. Appendix C details how we compute these metrics.


              0.6                                                                                                                450
                                                                  GRPO-Default
                                                                  GRPO-Epochs-2
                                                                                             Number of Unique Proofs Generated

              0.5                                                 GRPO-Epochs-3                                                  400
                                                                  GRPO-Unlikeliness-1
                                                                  GRPO-Unlikeliness-2                                            350
              0.4
                                                                                                                                 300
Uplift Rate




              0.3                                                                                                                250

                                                                                                                                            GRPO-Default
                                                                                                                                 200        GRPO-Unlikeliness-1
              0.2                                                                                                                           GRPO-Unlikeliness-2
                                                                                                                                            GRPO-Epochs-2
                                                                                                                                 150        GRPO-Epochs-3
              0.1                                                                                                                       0             100         200         300         400   500   600
                                                                                                                                                                          Training Step

              0.0                                                                            Figure 7: Number of unique proofs generated at each
                     0     5            10       15        20       25         30
                                        Rank of Sample in Group                              training step (smoothed with EMA). Unlikeliness re-
                                                                                             ward significantly improves sample diversity during
Figure 6: Uplift rate uj as a function of rank j for                                         training.
GRPO variants. The proposed methods improve the rate
of reinforcing low-probability correct solutions.
                                                                                             RL (Xin et al., 2024) on both datasets.

tion steps deviate the model further from its initial                                        6                                         Related Work
distribution – it aligns with our earlier analysis.
Higher PPO epochs indirectly amplifies rare so-                                              Automated Theorem Proving:                Polu and
lutions, thereby mitigating the sharpening effect                                            Sutskever (2020) pioneered transformer-based the-
typically caused by GRPO updates.                                                            orem provers that interact with proof assistants like
                                                                                             Lean or Isabelle (de Moura et al., 2015; Paulson,
                                                                                             1994). Subsequent work has developed state-tactic
5.4                 Putting It All Together
                                                                                             models (Polu et al., 2022; Wu et al., 2024; Xin
Finally, we evaluate GRPO-Unlikeliness-2 in a                                                et al., 2025) that generate one proof step at a time
large-scale experiment. We train the model on a                                              and full-proof models (Xin et al., 2024; Lin et al.,
dataset of 11k theorems, a larger and more chal-                                             2025b) that produce complete proofs autoregres-
lenging subset of Lean-Workbook that was solved                                              sively, reducing interaction overhead.
and released by Lin et al. (2025b), making sure to                                              Recent work has explored various directions in
exclude theorems in Dval . We evaluate the result-                                           LLM-based theorem proving. Lample et al. (2022),
ing model on MiniF2F-test (Zheng et al., 2021),                                              Xin et al. (2024), and Xin et al. (2025) explore the
a widely recognized benchmark for neural theo-                                               application of inference-time algorithms for proof
rem proving, as well as Dval . As reported in Ta-                                            discovery. Jiang et al. (2023) and Lin et al. (2025a)
ble 3, GRPO-Unlikeliness-2 achieves competi-                                                 use informal reasoning to guide formal proofs by
tive results compared to DeepSeek-Prover-V1.5-                                               integrating LLMs capable of reasoning in natural

                                                                                         7
    Model          pass@32      pass@128                    by building models that can engage in long chain-
                   MiniF2F-test                             of-thought style reasoning, either calling formal
    V1.5-SFT      47.1 ± 0.6% 49.2 ± 0.6%                   proof models as subroutines (Ren et al., 2025) or
    V1.5-RL       49.2 ± 0.6% 51.2 ± 0.3%                   devising hierarchical strategies to break down the
    Ours          48.8 ± 0.7% 50.6 ± 0.5%                   problem (Wang et al., 2025).
                       Dval                                    RL for Multi-Sample Performance: Several
    V1.5-SFT      78.3 ± 0.9% 83.1 ± 0.2%                   existing works specifically investigate the issue
    V1.5-RL       84.8 ± 0.9% 87.5 ± 0.7%                   of RL’s pass@N performance. Yue et al. (2025)
    Ours          84.3 ± 0.9% 88.8 ± 0.9%                   argues that instead of learning novel capabilities,
Table 3: pass@N performance of our model compared           RL with verifier reward mainly concentrates the
to DeepSeek-Prover-V1.5-SFT and -RL from Xin et al.         model’s outputs around correct answers already
(2024) on MiniF2F-test and Dval . Our model achieves        present in the base model’s samples. Their experi-
competitive performance with DeepSeek-Prover-V1.5-          ments also show an improvement in pass@ small
RL while being fully open.                                  N and deterioration at large N . Chow et al. (2024)
                                                            and Tang et al. (2025) consider novel RL formu-
                                                            lations that explicitly optimize for best-of-N per-
language. Hu et al. (2024) investigates training
                                                            formance. They derive BoN-aware RL algorithms
models that can incorporate novel context at test
                                                            and demonstrate improved performance, but still
time. Our work is mainly focused on the post-
                                                            consider a smaller range of N (pass@32) than is
training of theorem provers using reinforcement
                                                            typical in formal theorem proving. In the expert
learning, which we detail next.
                                                            iteration setting, Dang et al. (2025) identifies that
   Expert Iteration for Theorem Proving: Ex-
                                                            pass@N deteriorates due to diversity collapse and
pert iteration alternates between search and learn-
                                                            shows that interpolating model weights with an
ing (Anthony et al., 2017), and was first applied
                                                            early checkpoint mitigates this issue.
to theorem proving by Polu et al. (2022). It has
since become the dominant paradigm, appearing                  Compared to these previous works, we are the
in recent work like Wu et al. (2024), Xin et al.            first to attribute RL’s poor multi-sample perfor-
(2025), and Lin et al. (2025b). Xin et al. (2025)           mance to an inability to reinforce low-probability
explores the viability of best-first search for data        samples. We also provide a simple and direct so-
collection, while Wu et al. (2024) and Lin et al.           lution to address this issue and improve pass@N
(2025b) achieve state-of-the-art performance at the         performance.
time by performing large-scale expert iteration on
autoformalized theorem statements.
   RL for Theorem Proving: Compared to expert               7   Conclusion
iteration, the use of more general RL algorithms
is relatively underexplored. A notable exception            We investigated GRPO’s poor multi-sample perfor-
is Xin et al. (2024), which showed GRPO can en-             mance in the setting of formal theorem proving, the-
hance a SFT model using only additional theorem             orizing a connection between degraded pass@N at
statements and the verifier reward. In the low-             large N and the failure to reinforce low-probability
data setting, Gloeckle et al. (2024) successfully           solutions. Our analysis revealed an implicit bias
trained a strong theorem prover by adapting the             in GRPO: it preferentially reinforces already high-
AlphaZero algorithm (Silver et al., 2017) to proof          probability sequences while largely ignoring rare
trees. Xin et al. (2025) used direct preference op-         but correct ones. To address this, we introduced the
timization (Rafailov et al., 2023) in their pipeline,       unlikeliness reward, a simple yet effective modifi-
but only for the minor role of training against proof       cation that directly shifts reinforcement toward rare
steps that cause immediate errors.                          samples. Our experiments confirm that the unlike-
   More recent work has begun adapting tech-                liness reward enables GRPO to make significant
niques from OpenAI o1 (OpenAI et al., 2024) and             gains in pass@N at large N and drastically im-
DeepSeek-R1 (DeepSeek-AI et al., 2025) to train             proves sample diversity compared to existing meth-
reasoning models for theorem proving (Wang et al.,          ods. Using our revised recipe, we train a model
2025; Ren et al., 2025; Zhang et al., 2025). These          that is competitive with DeepSeek-Prover-V1.5-RL
works have achieved state-of-the-art performance            and release our implementation publicly.

                                                        8
Limitations                                                   Fabian Gloeckle, Jannis Limperg, Gabriel Synnaeve,
                                                                and Amaury Hayat. 2024. ABEL: Sample efficient
While we offer a lightweight solution for improving             online reinforcement learning for neural theorem
GRPO’s multi-sample performance, future work                    proving. In The 4th Workshop on Mathematical Rea-
                                                                soning and AI at NeurIPS’24.
could explore other strategies for uniformly rein-
forcing correct samples or for directly optimizing            Jiewen Hu, Thomas Zhu, and Sean Welleck. 2024.
performance under specific inference-time algo-                  minictx: Neural theorem proving with (long-) con-
rithms. In particular, developing inference-aware                texts. arXiv preprint arXiv:2408.03350.
reinforcement learning algorithms that are efficient          Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda
to train remains an open direction.                             Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix,
   Moreover, recent applications of RL have shifted             Yuhuai Wu, and Guillaume Lample. 2023. Draft,
                                                                sketch, and prove: Guiding formal theorem provers
toward the reasoning paradigm, where models                     with informal proofs. Preprint, arXiv:2210.12283.
generate long reasoning paths often involving be-
haviors such as planning, backtracking, and self-             Guillaume Lample, Marie-Anne Lachaux, Thibaut
critique. In these settings, the behavior of algo-              Lavril, Xavier Martinet, Amaury Hayat, Gabriel
                                                                Ebner, Aurélien Rodriguez, and Timothée Lacroix.
rithms like GRPO may differ qualitatively due to                2022. Hypertree proof search for neural theorem
the increased diversity and complexity of possible              proving. Preprint, arXiv:2205.11491.
reasoning paths. We leave as future work to deter-
                                                              Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming
mine whether methods that amplify rare but correct              Yang. 2025a. Lean-star: Learning to interleave think-
solutions can similarly enhance exploration and                 ing and proving. Preprint, arXiv:2407.10040.
generalization in reasoning models.
                                                              Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
                                                                Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
Acknowledgements                                                Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
                                                                2025b. Goedel-prover: A frontier model for
Sean Welleck thanks Convergent Research and the                 open-source automated theorem proving. Preprint,
Lean FRO for their support.                                     arXiv:2502.07640.

                                                              OpenAI, :, Aaron Jaech, Adam Kalai, Adam Lerer,
References                                                      Adam Richardson, Ahmed El-Kishky, Aiden Low,
                                                                Alec Helyar, Aleksander Madry, Alex Beutel, Alex
Thomas Anthony, Zheng Tian, and David Barber. 2017.             Carney, Alex Iftimie, Alex Karpenko, Alex Tachard
  Thinking fast and slow with deep learning and tree            Passos, Alexander Neitz, Alexander Prokofiev,
  search. Preprint, arXiv:1705.08439.                           Alexander Wei, Allison Tam, and 244 others. 2024.
                                                                Openai o1 system card. Preprint, arXiv:2412.16720.
Yinlam Chow, Guy Tennenholtz, Izzeddin Gur, Vincent
  Zhuang, Bo Dai, Sridhar Thiagarajan, Craig Boutilier,       Lawrence C. Paulson. 1994. Isabelle: A Generic Theo-
  Rishabh Agarwal, Aviral Kumar, and Aleksandra                 rem Prover. Springer Verlag.
  Faust. 2024. Inference-aware fine-tuning for best-
                                                              Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-
  of-n sampling in large language models. Preprint,
                                                                 tas Baksys, Igor Babuschkin, and Ilya Sutskever.
  arXiv:2412.15287.
                                                                 2022. Formal mathematics statement curriculum
                                                                 learning. Preprint, arXiv:2202.01344.
Xingyu Dang, Christina Baek, Kaiyue Wen, Zico Kolter,
  and Aditi Raghunathan. 2025. Weight ensembling              Stanislas Polu and Ilya Sutskever. 2020. Generative
  improves reasoning in language models. Preprint,               language modeling for automated theorem proving.
  arXiv:2504.10478.                                             Preprint, arXiv:2009.03393.
Leonardo Mendonça de Moura, Soonho Kong, Jeremy               Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-
  Avigad, Floris van Doorn, and Jakob von Raumer.               pher D Manning, Stefano Ermon, and Chelsea Finn.
  2015. The lean theorem prover (system description).           2023. Direct preference optimization: Your language
  In CADE.                                                      model is secretly a reward model. In Thirty-seventh
                                                                Conference on Neural Information Processing Sys-
DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang,               tems.
  Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
  Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang,            Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhi-                  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
  hong Shao, Zhuoshu Li, Ziyi Gao, and 181 others.               Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-
  2025. Deepseek-r1: Incentivizing reasoning capa-               rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
  bility in llms via reinforcement learning. Preprint,           Daya Guo, and Chong Ruan. 2025. Deepseek-prover-
  arXiv:2501.12948.                                              v2: Advancing formal mathematical reasoning via


                                                          9
  reinforcement learning for subgoal decomposition.             Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
  Preprint, arXiv:2504.21801.                                     Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Kai Shen.
                                                                  2025. Bfs-prover: Scalable best-first tree search
John Schulman, Filip Wolski, Prafulla Dhariwal,                   for llm-based automatic theorem proving. Preprint,
  Alec Radford, and Oleg Klimov. 2017. Prox-                      arXiv:2502.03438.
  imal policy optimization algorithms. Preprint,
  arXiv:1707.06347.                                             Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,
                                                                  Kristin Lauter, Swarat Chaudhuri, and Dawn Song.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,                   2024. Formal mathematical reasoning: A new fron-
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan                  tier in ai. Preprint, arXiv:2412.16075.
  Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
  Deepseekmath: Pushing the limits of mathemati-                Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
  cal reasoning in open language models. Preprint,                Dahua Lin, and Kai Chen. 2024. Lean work-
  arXiv:2402.03300.                                               book: A large-scale lean problem set formalized
                                                                  from natural language math problems. Preprint,
Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin                  arXiv:2406.03847.
  Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin
  Lin, and Chuan Wu. 2024. Hybridflow: A flexible               Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan,
  and efficient rlhf framework. arXiv preprint arXiv:             Xiaochen Zuo, Yu Yue, Tiantian Fan, Gaohong
  2409.19256.                                                     Liu, Lingjun Liu, Xin Liu, Haibin Lin, Zhiqi Lin,
                                                                  Bole Ma, Guangming Sheng, Yuxuan Tong, Chi
David Silver, Thomas Hubert, Julian Schrittwieser, Ioan-          Zhang, Mofan Zhang, Wang Zhang, Hang Zhu,
  nis Antonoglou, Matthew Lai, Arthur Guez, Marc                  and 16 others. 2025. Dapo: An open-source llm
  Lanctot, Laurent Sifre, Dharshan Kumaran, Thore                 reinforcement learning system at scale. Preprint,
  Graepel, Timothy Lillicrap, Karen Simonyan, and                 arXiv:2503.14476.
  Demis Hassabis. 2017. Mastering chess and shogi
  by self-play with a general reinforcement learning            Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai
  algorithm. Preprint, arXiv:1712.01815.                          Wang, Yang Yue, Shiji Song, and Gao Huang. 2025.
                                                                  Does reinforcement learning really incentivize rea-
Zhiqing Sun. 2024. Gpt-accelera: Simple and efficient
                                                                  soning capacity in llms beyond the base model?
  pytorch-native transformer training and inference
                                                                  Preprint, arXiv:2504.13837.
  (batched).    https://github.com/Edward-Sun/
  gpt-accelera.                                                 Jingyuan Zhang, Qi Wang, Xingguang Ji, Yahui Liu,
Yunhao Tang, Kunhao Zheng, Gabriel Synnaeve, and                   Yang Yue, Fuzheng Zhang, Di Zhang, Guorui
  Rémi Munos. 2025. Optimizing language models                     Zhou, and Kun Gai. 2025. Leanabell-prover: Post-
  for inference time objectives using reinforcement                training scaling in formal reasoning. Preprint,
  learning. Preprint, arXiv:2503.19595.                            arXiv:2504.06122.

Terence Tao. 2025. Machine-assisted proof. Notices of           Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  the American Mathematical Society, 72(1):6–15.                  2021. Minif2f: a cross-system benchmark for for-
                                                                  mal olympiad-level mathematics. arXiv preprint
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas                     arXiv:2109.00110.
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jian-                 A     Toy Environment
  qiao Lu, Hugues de Saxcé, Bolton Bailey, Chen-
  dong Song, Chenjun Xiao, Dehao Zhang, Ebony                   After observing that GRPO failed to improve
  Zhang, Frederick Pu, Han Zhu, and 21 others. 2025.            pass@N metrics, we constructed a simplified toy
  Kimina-prover preview: Towards large formal rea-
  soning models with reinforcement learning. Preprint,
                                                                environment to isolate the issue and efficiently test
  arXiv:2504.11354.                                             potential solutions. This appendix details the de-
                                                                sign of the environment and presents our experi-
Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan                 mental results within it.
  Ying, Jiayu Wang, Dahua Lin, and Kai Chen. 2024.
   Internlm2.5-stepprover: Advancing automated theo-
   rem proving via expert iteration on large-scale lean
                                                                A.1    Environment Design
   problems. Preprint, arXiv:2410.15700.                        We design a minimalistic toy environment for rapid
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao,             experimentation. The environment is fully observ-
  Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,              able, with state space S = R10 and discrete action
  Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, De-                space A = {1, . . . , 128}. Each action a ∈ A is
  jian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and                associated with a fixed, randomly initialized but
  Chong Ruan. 2024. Deepseek-prover-v1.5: Har-
  nessing proof assistant feedback for reinforcement
                                                                hidden vector va ∈ R10 .
  learning and monte-carlo tree search. Preprint,                 The binary reward function Rτ : S × A →
  arXiv:2408.08152.                                             {0, 1} is defined as:

                                                           10
                                                                Analyzing uplift rate metrics (Section 3.5), we
            Rτ (s, a) = 1{s⊤ va ≥ τ }                        identify a rank bias in GRPO, showing preferen-
   Here, τ is a threshold controlling environment            tial reinforcement of already high-probability solu-
difficulty. Higher τ values restrict the reward to           tions:
fewer actions, thus increasing difficulty. We fix τ =
1.0 during training but vary τ during evaluation to
simulate different difficulty levels.
A.2   Policy Model
The policy model πθ (a | s) is a simple two-layer
multilayer perceptron (MLP) mapping state s to a
probability distribution over actions in A.
A.3   GRPO Training and Diagnosis
We train the model using GRPO for 200 steps and
evaluate pass@N metrics at N ∈ {1, 4, 8, 16, 32}.
Initial evaluations at training difficulty τ = 1.0           A.4   Unlikeliness Reward
suggest GRPO improves pass rates across all N :              We investigate the impact of unlikeliness reward
                                                             within this toy environment. It effectively neutral-
                                                             izes the rank bias, making the uplift rates notably
                                                             more uniform:




   However, evaluations at increased difficulties
(τ = 4.0 and τ = 5.0) reveal pass@32 deterio-
rates over training, aligning with observations in
the original setting:
                                                                Consequently, the unlikeliness reward signifi-
                                                             cantly improves pass@32 performance in the dif-
                                                             ficult setting τ = 5.0, contrasting sharply with de-
                                                             fault GRPO, whose pass@32 performance declines
                                                             to near chance levels:




                                                               Additionally, incorporating the unlikeliness re-
                                                             ward substantially increases the entropy of the pre-
                                                             dicted action distribution:

                                                        11
                                                                      0.90

                                                                      0.85

                                                                      0.80

                                                                      0.75




                                                             Pass@N
                                                                      0.70

                                                                      0.65

                                                                      0.60
                                                                                                                                                            Model
                                                                                                                                                      DeepSeek-Prover-V1.5-SFT
                                                                                                                                                      GRPO-Default
                                                                      0.55                                                                            GRPO-Unlikeliness-1
                                                                                                                                                      GRPO-Unlikeliness-2
                                                                      0.50                                                                            GRPO-High-KL
                                                                                     1               2   4   8      16            32        64        128         256    512
                                                                                                                              N

                                                             Figure 8: Performance of GRPO variants including
                                                             GRPO-High-KL on Dval . For readability, we omit some
B     Training Setup                                         variants.

The main experiments in Section 5 are conducted                                                                   GRPO-Default
on 4 NVIDIA L40S GPUs, with 500GB of RAM                                                                          GRPO-Unlikeliness-1
                                                                                           0.5                    GRPO-Unlikeliness-2
                                                                                                                  GRPO-High-KL
and 48–64 CPUs allocated for running parallel in-
                                                                                           0.4
stances of the Lean REPL.


                                                                             Uplift Rate
                                                                                           0.3
B.1    Training Time
                                                                                           0.2
All training runs in the main experiment complete
                                                                                           0.1
within 36 hours. Each training step primarily con-
sists of three stages: sequence generation, proof                                          0.0
                                                                                                 0       5   10          15            20        25          30
                                                                                                             Rank of Sample in Group
verification, and policy model updates. The gener-
ation and verification stages are shared across all          Figure 9: Uplift rates of GRPO variants including
                                                             GRPO-High-KL.
methods and take approximately 120 seconds per
batch (16 problems × 32 attempts). The duration
of the policy update step depends on the number of           increased sampling, up to hundreds of thousands
PPO epochs, as shown below:                                  of passes (Lin et al., 2025b). This suggests that
                                                             the distribution of the base model is highly diverse
      PPO Epochs      Policy Update Time (s)                 and crucial to preserve during fine-tuning. Prior
      1                        ≈ 70                          work addressed this in the SFT setting by ensem-
      2                       ≈ 140                          bling fine-tuned model weights with the original
      3                       ≈ 210                          (Dang et al., 2025). Since GRPO already has a
                                                             regularization mechanism through the KL penalty,
C     Evaluation Metrics                                     we simply increase the KL loss coefficient to 0.1
                                                             to better preserve the original distribution.
We begin by selecting a maximum sample size
                                                                To isolate the contribution from unlikeliness re-
Nmax (512 in our experiments) and generate Nmax
                                                             ward and PPO epochs, we conduct a control run
responses for each problem. To compute pass@n,
                                                             that only increases the KL penalty from GRPO-
we divide the responses for each problem into
                                                             Default. This corresponds to an additional row for
Nmax /n chunks and assign each chunk a binary
                                                             Table 1:
reward indicating whether any proof within it is
valid. The i-th trial of pass@n is then computed by                      Model                                    K               βKL            βrank
averaging the binary rewards across the i-th chunk                       GRPO-High-KL                             1               0.10             –
of all problems. We report the mean and standard
deviation across trials. Note that for pass@512,                We find that, while this change prevented the
there is only a single trial, so we omit the standard        deterioration of pass@N performance, it did not
deviation in our plots.                                      bring a substantial improvement over the base
                                                             model (Figure 8). This is likely because the RL up-
D     Effects of KL Penalty                                  dates still fail to uplift low-rank samples (Figure 9).
                                                             Thus, we treat KL regularization as a supporting
Recent results have shown that the pass rates of the-
                                                             modification rather than a solution in itself.
orem prover models can continue to improve with

                                                        12
