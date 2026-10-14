                                             Learning to Correct: Calibrated Reinforcement Learning for Multi-Attempt
                                                                         Chain-of-Thought


                                                              Emrullah Ildiz * 1 Halil Alperen Gozeten * 1 Ege Onur Taga 1 Samet Oymak 1 2


                                                                   Abstract                                     Cobbe et al., 2021; Dhuliawala et al., 2023). However, opti-
                                                State-of-the-art reasoning models utilize long                  mizing these multi-turn interactions through reinforcement
                                                                                                                learning (RL) poses a critical challenge for credit assign-
arXiv:2604.17912v1 [cs.LG] 20 Apr 2026




                                                chain-of-thought (CoT) to solve increasingly com-
                                                plex problems using more test-time computation.                 ment (Ahmadian et al., 2024). Trajectory-level rewards fail
                                                In this work, we explore a long CoT setting where               to leverage dense feedback and can backpropagate success
                                                the model makes up to K successive attempts at                  signals to incorrect/uninformative early attempts (Uesato
                                                solving a problem, in which each attempt is al-                 et al., 2022; Lightman et al., 2023; Cobbe et al., 2021; Sti-
                                                lowed to build on earlier ones after the model                  ennon et al., 2022; Ouyang et al., 2022). In contrast, naive
                                                receives a hard verifier feedback. This motivates               heuristics can introduce systematic biases in policy gradient
                                                RL methods that can harness per-attempt rewards                 estimation, motivating a principled framework (Williams,
                                                by carefully weighting individual attempts. We                  1992; Sutton et al., 1999; Schulman et al., 2018).
                                                study optimizing the Verification@K reward (the                 In this work, we frame long CoT as a Verification@K
                                                model succeeds by the K-th attempt) and show                    (Ver@K) problem: The model makes at most K succes-
                                                that naively weighing the attempts by their pass/-              sive attempts until it solves the problem, and after each
                                                fail results in biased gradients. We introduce Cali-            attempt, it gets to observe a hard pass/fail feedback. Un-
                                                brated Attempt-Level (CAL) GRPO by devising                     der this setting, if a trajectory terminates at ℓ attempts, the
                                                a weighing strategy to obtain unbiased gradients                model receives ℓ 0-1 rewards and this dense feedback can be
                                                while maintaining small variance. Our theory                    used to enhance RL training. This motivates RL algorithms
                                                reveals how incorporating per-attempt rewards                   that weigh individual attempts for better policy gradient
                                                influence the training and the eventual Verifica-               estimation. We ask:
                                                tion@K performance. Experiments, baselines,
                                                and ablations on synthetic and real data corrob-                Q: What RL algorithms efficiently maximize the Ver@K
                                                orate our theory and the benefits of CAL-GRPO                   reward and teach the model better correction capabilities?
                                                over vanilla GRPO as well as naive weighting.
                                                                                                                Specifically, we examine Attempt-Level variations of RE-
                                                                                                                INFORCE Leave-One-Out and GRPO where we weigh the
                                         1. Introduction                                                        gradient contributions at attempt-level rather than trajectory-
                                                                                                                level. An intuitive strategy is weighing the attempts by their
                                         The emergence of advanced reasoning models is fundamen-
                                                                                                                individual pass/fail rewards, which we call Naive Attempt-
                                         tally driven by the scaling of test-time compute, where ex-
                                                                                                                Level (NAL) Algorithm. Interestingly, we establish that
                                         tended CoT traces help solve more complex problems (Wei
                                                                                                                NAL over-emphasizes earlier attempts and results in biased
                                         et al., 2023; Wang et al., 2023; Yao et al., 2023a; Aghajohari
                                                                                                                policy gradients for the Ver@K objective. As our key techni-
                                         et al., 2025). This paradigm effectively shifts the computa-
                                                                                                                cal contribution, we introduce C(alibrated)AL Algorithm by
                                         tional burden to the autoregressive generation process, en-
                                                                                                                correcting the bias of NAL through a theoretically-grounded
                                         abling the model to search for new approaches or revise past
                                                                                                                weight assignment.
                                         proposals (Yao et al., 2023b). While traditional CoT is often
                                         viewed as a single coherent trace, recent research increas-            Remarkably, we demonstrate that CAL achieves the best-of-
                                         ingly approaches reasoning as an iterative, multi-attempt              both worlds: (i) It returns unbiased gradient unlike NAL and
                                         process where models utilize external verifier feedback to             (ii) it achieves lower variance than Trajectory-Level (TL)
                                         build on and correct earlier failures (Lightman et al., 2023;          Algorithm, which employs trajectory-level sparse rewards.
                                            1                                                                   Importantly, all three variants are instantiations of a generic
                                              University of Michigan, Ann Arbor 2 Google Research. Corre-
                                         spondence to: M. Emrullah Ildiz <eildiz@umich.edu>.                    Attempt-Level method with specific weight assignments as
                                                                                                                depicted in Figure 1. As a remark, the number of backprop-
                                         ∗
                                             Equal Contribution                                                 agation steps required is the same across all methods. To

                                                                                                            1
                                     Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

    TL (Trajectory-Level)                                             high variance       policy samples a candidate solution yt ∼ πθ (· | st−1 ), and an
        Attempt 1              Attempt 2                Attempt 3
                                                                                          external verifier returns a binary signal rt ∈ {0, 1} indicating
                                                                                          whether yt is correct with respect to y. If rt = 1, the rollout
    z          Same reward r₁= r₂= r₃ assigned to ALL attempts
                                                                                          terminates immediately. If rt = 0 and t < K, the incorrect
  NAL (Naive Attempt-Level)                                  weights = 1 (uniform)
                                                                             biased
                                                                                          solution yt and feedback are appended to the state, and the
        Attempt 1              Attempt 2                Attempt 3                         process continues with attempt t + 1. If all K attempts are
         Reward: r₁              Reward: r₂              Reward: r₃                       incorrect, the rollout terminates after K attempts.
  CAL (Calibrated Attempt-Level)                                 ✓ best Ver@K
                                                                                          Formally speaking, let the first state s0 be the problem
        Attempt 1              Attempt 2                Attempt 3                         x and let st = (st−1 , yt , rt ) be the state denoting the
        Weight: w₁ · r₁         Weight: w₂ · r₂         Weight: w₃ · r₃                   history up to and including the (t)-th attempt, and let
Figure 1. We consider RLOO and GRPO methods that weigh                                    τ := sT = (x, y1 , r1 · · · yT (τ) , rT (τ) ) denote the resulting ran-
individual attempts. TL is the standard approach that uses the final                      dom trajectory, where the stopping time T (τ) ∈ {1, . . . , K}
Ver@K reward for all attempts. NAL uses per-attempt pass/fail                             is the attempt index at which the rollout stops: T (τ) is the
as weights. Proposed CAL approach calibrates naive weights to                             smallest index t ≤ K with rt = 1 if the model ever succeeds,
obtain unbiased low-variance gradients.                                                   and T (τ) = K if the model never succeeds. We define the
                                                                                          Ver@K reward for trajectory τ as rT (τ) . For notational sim-
                                                                                          plicity, we omit the trajectory τ, so we use T instead of
summarize, we make the following contributions:
                                                                                          T (τ) in this section.
   i We introduce attempt-level variations of both RLOO                                   For fixed (x, y), let pθ (τ | x, y) denote the trajectory dis-
     and GRPO to facilitate finer-grained credit assignment.                              tribution induced by the policy πθ and the verifier. For
                                                                                          notational simplicity we write pθ (τ | x) with the dependence
  ii We formally derive the policy gradient of the Ver@K                                  on y through the verifier implicit. The per-example Ver@K
     objective and introduce CAL as an effective method to                                success probability is
     optimize it.
                                                                                                              ρθ (x, y) := Eτ∼pθ (·|x) rT .
                                                                                                                                       
 iii We establish that CAL corrects the potential bias of
     NAL and prove that it also achieves strictly lower vari-                             Our training objective is to maximize the expected Ver@K
     ance compared to standard TL under mild conditions.                                  success probability:
 iv We demonstrate that CAL consistently outperforms TL                                                       J(θ) := E(x,y)∼P ρθ (x, y) .
                                                                                                                                       
                                                                                                                                                             (1)
    and NAL baselines across a diverse set of reasoning
    tasks, including MATH, Maze navigation, and struc-                                    In this paper, we develop two different approaches to the
    tured Markov Chain benchmarks.                                                        Ver@K problem, namely trajectory-level optimization and
                                                                                          attempt-level optimization. Next, we derive gradients for
2. Problem Setup and Preliminaries                                                        these approaches to provide insight into their behavior. In
                                                                                          the remainder of the paper, we utilize these gradients to max-
We consider a reinforcement learning with verifiable reward                               imize the objective of (1) with the REINFORCE algorithm
(RLVR) setup where a policy model is trained to solve prob-                               (Williams, 1992) and its extension to the leave-one-out ver-
lems using a verification-based multi-attempt procedure.                                  sion (Ahmadian et al., 2024).
For each problem, the model can attempt a solution up to
K times, and an external verifier provides binary feedback                                Trajectory-level Optimization: In this approach, we treat
after each attempt. Each trajectory is assigned a single 0/1                              each trajectory τ as a single solution sampled from the
reward depending on whether the model achieves a correct                                  trajectory distribution pθ (· | x). This formulation allows us
solution within the first K attempts.                                                     to view different trajectories as independent samples from
                                                                                          the same distribution. Applying the log-derivative property,
Let X denote the space of problem inputs and Y the space                                  at the trajectory level, the gradient of (1) for a fixed problem
of correct reference answers. We assume examples (x, y)                                   (x, y) can be written as
are drawn from a distribution P over X × Y. A policy πθ
(e.g., an autoregressive language model) with parameters θ                                          ∇θ ρθ (x, y) = ∇θ Eτ∼pθ (·|x) rT
                                                                                                                                  
                                                                                                                                                             (2)
maps states to distributions over actions (token sequences).                                                     = Eτ∼pθ (·|x) rT ∇θ log pθ (τ | x) .
                                                                                                                                                  

For a fixed problem (x, y), we consider the following rollout
procedure. At attempt t ∈ {1, . . . , K}, the environment is                              The gradient is therefore an expectation over trajectories τ
in state st , which encodes the original problem x together                               drawn from pθ (· | x) and depends on each trajectory only
with the history of previous attempts and rewards. The                                    through its realized reward and log-probability.

                                                                                      2
                                  Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

Attempt-level Optimization: In this approach, we decom-                             called Calibrated Attempt-Level Algorithm (CAL). In Sec-
pose a single trajectory into a sequence of dependent at-                           tion 4, we compare the proposed method with existing
tempts and analyze each attempt individually to derive the                          approaches on a synthetic Markov chain benchmark, the
gradient of (1) for a fixed problem instance (x, y). This                           MATH dataset, and a maze navigation task. Finally, in Sec-
formulation enables attempt-level credit assignment during                          tion 5, we prove the unbiasedness of the proposed gradient
solution generation, improving optimization efficiency by                           estimator and provide variance-reduction guarantees relative
reducing the sparsity of trajectory-level rewards. On the                           to trajectory-level optimization under mild assumptions.
other hand, because the attempts are sequentially dependent,
this approach requires computing more complex conditional                           3. Derivation of RLOO Algorithms
probability distributions. The trajectory distribution (over
valid trajectories) factorizes as pθ (τ | x) = Tt=1 πθ (yt | st−1 ),
                                              Q
                                                                                    In this section, we derive the REINFORCE with leave-one-
and therefore                                                                       out (RLOO) algorithm for trajectory-level and attempt-level
                                                                                    optimization using the gradients provided in Section 2, and
                                    T
                                    X                                               we study the relationship between these two approaches. Fi-
           ∇θ log pθ (τ | x) =            ∇θ log πθ (yt | st−1 ).         (3)
                                                                                    nally, inspired by these two approaches, we define a practical
                                    t=1
                                                                                    reward shaping function over a sampled group to apply a
Substituting (3) into (2) and extending the random upper                            GRPO-based algorithm that maximizes the Verification@K
limit T to K using the indicator 1T ≥i yields                                       reward.
                    K
                    X                                                               We start by defining the REINFORCE with Leave-one-out
   ∇θ ρθ (x, y) =         Eτ∼pθ (·|x) 1T ≥i rT ∇θ log πθ (yi | si−1 ) .             (RLOO) (Ahmadian et al., 2024) algorithm for the trajec-
                                                                    
                    i=1                                                             tory and attempt-level optimization. While defining, we
                                                                                    fix a problem instance (x, y) and draw a group of N ≥ 2
Next, define the continuation success probability                                                                            i.i.d.
                                                                                    independent trajectories τ1 , . . . , τN ∼ pθ (· | x).
 Vθ,i (si ) := E [rT | si ] = P (∃ t ∈ {i + 1, . . . , K} : rt = 1 | si )           RLOO for Trajectory-level Optimization: In this ap-
                                                                                    proach, we assign a single reward to each trajectory in order
and Vθ,K+1 (·) := 0; where si is the state before attempt i.                        to apply the RLOO algorithm for the trajectory-level op-
Since the verifier is deterministic, conditioning on (si , yi )                     timization. If there exists one correct answer inside the
fixes ri , and the remaining Ver@K reward satisfies the one-                        trajectory, we assign 1 reward; otherwise we assign 0 re-
step recursion                                                                      ward. Formally speaking, let T (τ1 ), . . . , T (τN ) be the cor-
                                                                                    responding stopping times for the trajectories. Then, the
             E rT | si−1 , yi = ri + (1 − ri ) Vθ,i (si ),
                            
                                                                                    assigned reward for the nth trajectory is rnTL := rT (τn ) , where
                                                                                    rT (τn ) is the verification@K reward defined in Section 2.
where si = (si−1 , yi , ri ) is the next state. Applying the tower                  REINFORCE with Leave-One-Out (RLOO) replaces the
property to ∇θ ρθ (x, y) gives                                                      trajectory reward rnTL by the leave-one-out advantage
                    K
                    X                                                                                                      1 X TL
  ∇θ ρθ (x, y) =          Eτ∼pθ (·|x) 1T ≥i ri + (1 − ri ) Vθ,i (si )                               ATL = rnTL −                  r ,
                                                                    
                                                                                                     n
                    i=1
                                                                          (4)                                            N − 1 m,n m
                                           ∇θ log πθ (yi | si−1 ) .
                                                                 
                                                                                    and uses the trajectory-level gradient estimator
In attempt-level optimization, the gradient is expressed as an                                                       N
                                                                                                              1 X TL
expectation over attempts and depends on the continuation                                  bTL
                                                                                           G      (θ; x, y) =      A ∇θ log pθ (τn | x).          (5)
success probabilities Vθ,i (si ).
                                                                                             RLOO
                                                                                                              N n=1 n

Trajectory-level optimization requires sampling full trajecto-
ries from the underlying distribution, whereas attempt-level                        RLOO for Attempt-level Optimization: In this approach,
optimization involves computing more complex conditional                            we assign a reward to each attempt (instead of assigning a
probability distributions. In this paper, our goal is to de-                        single reward to the whole trajectory!) using the probabili-
velop a practical algorithm that strikes an effective trade-off                     ties Vθ,i (si ) and P(T ≥ i). Let rn,i be the correctness of nth
between these two approaches.                                                       trajectory ith attempt for n ∈ [N] and i ∈ [T (τn )]. Inspired
                                                                                    by the gradient derivation for the attempt-level optimization
In the remainder of the paper, we describe the REINFORCE                            in (4), we reshape this reward to obtain a reward for the
algorithm with leave-one-out for both trajectory-level and                          attempt-level optimization as follows:
attempt-level optimization in Section 3. We then present a
                                                                                                    AL
                                                                                                        = rn,i + (1 − rn,i )Vθ,i (sn,i )
                                                                                                                                        
practical estimator for Vθ,i (si ) and introduce an algorithm                                      rn,i                                           (6)

                                                                                3
                             Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

Now, we define the advantage for each attempt i. The impor-                    Calibrated Attempt-level Algorithm (CAL): In this al-
tant difference from the previous approach is that we apply                    gorithm, we fix a problem (x, y) and draw a group of N
                                                                                                                        i.i.d.
the leave-one-out centering for each attempt separately. Let                   independent trajectories τ1 , . . . , τN ∼ pθ (· | x). Recall
Si := {n : n ∈ [N], T (τn ) ≥ i}. Then, when |Si | > 1                         that rn,i represents the correctness of the output for the
                                 1       X                                     nth trajectory at ith attempt and recall the definition of
             AAL
              n,i := r AL
                      n,i −                   rAL ,      (7)                   Si = {n : n ∈ [N], T (τn ) ≥ i}. We define an estimate
                             |Si | − 1 m,n,m∈S m,i
                                                   i                           of the success probability for the attempt i ∈ [T (τn )] with
                                                                               leave-one-out as
and when |Si | = 1, AAL
                     n,i = 0. Based on these advantages, we
define the attempt-level gradient estimator as
                                                                                                          P
                                                                                                            m∈Si ,m,n 1rm,i =1
                                                                                                 ρ̂n,i :=                      .
                       K                                                                                      |Si | − 1
                       X 1 X
                                     n,i ∇θ log πθ (yn,i | sn,i−1 ). (8)
 bAL
 G RLOO (θ; x, y) :=                AAL
                       i=1
                           N n∈S                                                                                        AL
                                                                               Then, inspired by the reward definition rθ,i in (6), we assign
                                i
                                                                               the following weight to the attempt i ∈ [K]:
Until now, we have defined the RLOO algorithm for
                                                                                                     n,i = Π j=i+1 (1 − ρ̂n, j ),
                                                                                                    wCAL    K
trajectory-level and attempt-level optimization. Now, we                                                                                              (10)
are ready to state our main result in this section:
                                                                                                 CAL
                                                                               For the reward rn,i     := rn,i and define ACAL   accordingly
Theorem 3.1. Recall the definitions of trajectory and                                                                      n,i
                           bTL (θ; x, y) and G bAL (θ; x, y)                   similar to (7). Then, the gradient estimator for the weighted
attempt-level estimators G    RLOO              RLOO                           attempt-level algorithm is the following:
in (5) and (8), respectively. Then, we have
                                                                                 bCAL (θ; x, y)
         RLOO (θ; x, y) = E G RLOO (θ; x, y) = ∇θ ρθ (x, y).
       bTL                  bAL
                                                                                 G
                                           
    E G                                                                            RLOO
                                                                                            K
Define gn,i := 1Tn ≥i ∇θ log πθ (yn,i | sn,i−1 ) and
                                                                                            X 1 X                                                     (11)
                                                                                                               n,i An,i ∇θ log πθ (yn,i | sn,i−1 ).
                                                                                                              wCAL  CAL
                                                                                       :=
                                                                                            i=1
                                                                                                  N n∈S
                    N                       N                                                             i
                 1 X TL                  1 X AL
       ZiTL :=         An gn,i , ZiAL :=      A gn,i .              (9)
                 N n=1                   N n=1 n,i                             Note that we do not utilize the probability of Vθ,i (si ) in
                                                                               the definition of (11) compared to (6) as we estimate the
Then, we have                                                                  future success probabilities based on the samples inside the
                                                                               sampled. In addition to this algorithm, we also defined two
             Var ZiTL ≥ Var ZiAL
                                
                                              ∀i ∈ [K]
                                                                               different baselines.
where the equality occurs only when K = 1 or Vθ,i (si ) ∈                      Naive Attempt-level Algorithm (NAL): In this algorithm,
{0, 1} for all possible si .                                                   we assign a reward to each attempt in a trajectory, but we
                                                                               do not apply the weight that we defined in (10). Instead,
This theorem yields two conclusions. First, the RLOO
                                                                               we weight with 1 and obtain the gradient estimator for the
gradient estimators for trajectory-level and attempt-level
                                                                               attempt-level algorithm similar to (11).
optimization are unbiased. The key reason is that we define
the rewards riTL and rn,i
                        AL
                           to match the gradients derived in                   Trajectory-level Algorithm (TL): In this algorithm, we
(2) and (4). Second, the attempt-level gradient estimator has                  directly use the gradient estimator defined in (5).
lower variance than the trajectory-level gradient estimator,
                                                                               An important remark is that the number of backpropagation
because it exploits the rewards from individual attempts
                                                                               steps required is the same across all methods. Compared
rather than treating the entire trajectory as a single sample.
                                                                               to the TL algorithm, the NAL and CAL algorithms assign
Under reasonable assumptions on the attempt-level com-
                                                                               rewards to individual attempts rather than a single reward to
ponents, we show the variance reduction for each attempt.
                                                                               the entire trajectory, which reduces the variance of the gra-
Under suitable cross-covariance conditions between the at-
                                       bTL ) ≥ Var(G   bAL ).                  dient estimator (Theorem 3.1). The key distinction between
tempts’ gradients, it implies that Var(G RLOO           RLOO                   the two is that the CAL algorithm assigns attempt-specific
The proof for the above theorem is provided in Appendix C.
                                                                               weights based on future success probabilities, inspired by
The main practical drawback of attempt-level optimization                      (6), whereas the NAL algorithm uses uniform weights. A
is that we assume access to the probabilities Vθ,i (sn,i ) for                 central contribution of this paper is this calibrated attempt-
every possible trajectory. In practice, it is difficult to com-                wise reward assignment, which avoids treating each tra-
pute these probabilities for all trajectories. To overcome this                jectory as a single output generation. In our experiments,
difficulty, we provide a rough estimate of these probabilities.                the NAL algorithm serves as a natural ablation, represent-
We refer to this algorithm as the Calibrated Attempt-level                     ing a naive uniform-weight variant of the proposed CAL
algorithm.                                                                     algorithm.

                                                                           4
                                                   Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                      0.75       TL-GRPO                                                 TL-GRPO                                                  1.60                             TL-GRPO
                                 NAL-GRPO                                          0.6   NAL-GRPO                                                                                  NAL-GRPO
Validation Accuracy

                      0.70




                                                                                                                              Avg # of attempts
                                 CAL-GRPO                                                CAL-GRPO                                                                                  CAL-GRPO




                                                                 Attempt Success
                                                                                   0.5                                                            1.55
                      0.65                                                                                        attempt 1
                                                                                   0.4                            attempt 2
                      0.60                                                                                                                        1.50
                      0.55                                                         0.3
                                                                                                                                                  1.45
                      0.50                                                         0.2
                      0.45                                                         0.1                                                            1.40
                             0    10    20    30       40   50                           10   20        30   40      50                                  0   10   20     30       40   50
                                       Training step                                           Training step                                                      Training step
  (a) Ver@2 validation accuracy on MATH                            (b) Attempt-wise success. Solid: attempt-1                   (c) Average attempts per problem un-
  across training. CAL-GRPO attains the                            success. Dashed: attempt-2 success con-                      der Ver@2. NAL-GRPO reduces attempts
  highest Ver@2, with NAL-GRPO improv-                             ditioned on attempt 1 failing; CAL-GRPO                      the most, while CAL-GRPO trades slightly
  ing over TL-GRPO.                                                notably improves corrections on attempt-2.                   higher attempts for higher Ver@2.
  Figure 2. Optimizing the Ver@2 objective on MATH with GRPO variants. We compare Trajectory-Level GRPO (TL-GRPO), Naive
  Attempt-Level GRPO (NAL-GRPO), and Calibrated Attempt-Level GRPO (CAL-GRPO). (a) CAL-GRPO achieves the best Ver@2 over
  training. (b) The improvement is primarily driven by stronger second-attempt correction, whereas NAL-GRPO emphasizes first-attempt
  success. (c) NAL-GRPO minimizes the number of attempts, while CAL-GRPO uses slightly more attempts but delivers higher overall
  Ver@2.


   4. Experiments on Ver@K                                                                              et al., 2025) and leveraging its multi-attempt rollout and
                                                                                                        interaction framework for iterative verifier feedback. Specif-
  In this section, we evaluate TL-GRPO, NAL-GRPO, and                                                   ically, we use a multi-attempt interaction loop (problem →
  CAL-GRPO on three benchmarks: a synthetic Markov chain                                                attempt → verifier feedback) with K ∈ 2, 4 (Ver@2 and
  task, MATH, and Maze. We first describe the experimental                                              Ver@4), while keeping rollout and group-sampling config-
  setup and then present the main results and analysis on                                               urations fixed across all estimators. For the Maze Ver@2
  Ver@K.                                                                                                results on 5×5 and 9×9, we report mean curves over five
                                                                                                        independent training runs with different random seeds, to-
   4.1. Experimental Setup                                                                              gether with confidence intervals across runs. For the remain-
  We compare three algorithms, namely trajectory-level,                                                 ing settings, we report single-run curves.
  naive attempt-level, and calibrated attempt-level on three                                            MATH Dataset. We train and evaluate on the MATH
  datasets: a synthetic Markov chain task, the MATH dataset                                             dataset (Hendrycks et al., 2021), which contains 12,500
  (Hendrycks et al., 2021), and the Maze navigation task (Ivan-                                         competition-style problems (7,500 train / 5,000 test). We
  itskiy et al., 2023). All algorithms are implemented using                                            use the official train split for RL training and report Ver@K
  Group Relative Policy Optimization (GRPO) (Shao et al.,                                               on the held-out test split. The verifier extracts the model’s
  2024) with the advantage shaping methods described in                                                 final answer and compares it to the ground-truth answer (re-
  Section 3. Different from the previous section’s leave-one-                                           ward rt =1 if correct, else 0). When an attempt is incorrect,
  out formulation, in our experiments we use the standard                                               we append a short, fixed-format feedback message indicat-
  GRPO group normalization: advantages are computed by                                                  ing failure and prompt the model to revise its answer and
  centering rewards with the within-group empirical mean and                                            try again; otherwise the interaction terminates immediately
  scaling by the within-group empirical standard deviation;                                             on success.
  for NAL-GRPO and CAL-GRPO this normalization is ap-
  plied separately at each attempt index over trajectories that                                         Maze Task. We consider a text-based maze navigation task
  reach that attempt. We use this normalization throughout                                              which is a standard benchmark of planning and sequential
  all our experiments as we empirically observe that dividing                                           decision-making for LLMs (Dao & Vu, 2025; Chen et al.,
  by the within-group empirical standard deviation improves                                             2025; Ivanitskiy et al., 2023). We generate synthetic datasets
  optimization, and Appendix B reports an ablation without                                              using the configurable maze-dataset library (Ivanitskiy
  the standard deviation scaling. Following the notation in                                             et al., 2023). For maze sizes 9×9, 7×7, and 5×5, we cre-
  Section 3, in this section we refer to these algorithms as TL-                                        ate 10,000 training and 1,000 test mazes. Each instance
  GRPO, NAL-GRPO, and CAL-GRPO, respectively. Further                                                   provides a maze grid with a designated start and goal. The
  benchmark, verifier, rollout, and GRPO-variant details are                                            model outputs a sequence of discrete moves of {U,D,L,R};
  provided in Sections A.2 to A.5.                                                                      and we deterministically check whether the sequence consti-
                                                                                                        tutes a valid path from start to goal without crossing walls,
   For the MATH and Maze tasks, we implement Ver@K train-                                               and return rt ∈ {0, 1}. We train with the same Ver@K proce-
   ing by extending the open-source verl framework (Sheng

                                                                                                    5
                                               Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                               1.0                                                                        1.0
                                         CAL-GRPO                                                                   CAL-GRPO
                                         NAL-GRPO                                                                   NAL-GRPO
         Validation Accuracy




                                                                                    Validation Accuracy
                                         TL-GRPO                                                          0.8       TL-GRPO
                               0.8
                                                                                                          0.6
                               0.6
                                                                                                          0.4
                               0.4
                                                                                                          0.2
                               0.2                                                                        0.0
                                     0   200 400 600 800 1000 1200 1400 1600                                    0      1000    2000    3000    4000   5000
                                                    Training step                                                              Training step
           (a) No-trap Markov chain Ver@4 (nhubs =5, m=6).                            (b) Trap Markov chain Ver@2 (nhubs =5, m=6). Val-
           Validation success vs. training step; the calibrated                       idation success vs. training step with a sampled pre-
           attempt-level method learns fastest and reaches the                        terminal trap to avoid; the calibrated attempt-level
           highest success.                                                           method reaches higher accuracy earlier.
Figure 3. Optimizing the Ver@4 and Ver@2 objectives on Markov Chain task with GRPO variants. We compare TL-GRPO,
NAL-GRPO, and CAL-GRPO. Success is defined by reaching the absorbing terminal state with a valid shortest-length trajectory; the trap
setting in (b) additionally fails any attempt that visits the trap state. CAL-GRPO consistently reaches higher accuracies in both settings
and breaks the plateau earlier than TL-GRPO and NAL-GRPO in the trap setting.


dure and the same three GRPO estimators as in the previous                          sample start states (and also the trap state in the trap setting),
sections, and report Ver@K on the corresponding test sets                           compute the corresponding shortest valid trajectory to the
for each maze size. We provide further experimental details                         absorbing terminal state on the graph with the trap removed
in Appendix A.                                                                      when applicable, and use the resulting state-id sequence as
                                                                                    the supervised target. We then fine-tune this checkpoint
Markov Chain Task. We introduce a synthetic structured
                                                                                    with the same Ver@K GRPO procedure used in the main
Markov chain task for controlled evaluation of multi-attempt
                                                                                    experiments. Sections A.2 to A.4 provide the benchmark,
reward assignment under a deterministic verifier. The state
                                                                                    verifier, tokenization, rollout, and optimization details.
space is organized into nhubs ordered hubs, each containing
m states, so that nstates = nhubs · m. Transitions are predom-
inantly local within a hub (moves to nearby states, e.g.,                           4.2. Results and Analysis
within ±1 positions), with additional sparse boundary tran-                         We study three questions: (Q1) Does attempt-level
sitions that connect consecutive hubs. The final state in the                       credit assignment (NAL-GRPO/CAL-GRPO) improve over
last hub is an absorbing terminal state. Each instance sam-                         trajectory-level credit assignment (TL-GRPO)? (Q2) Is the
ples a start state s0 from the set of states that can reach the                     calibration in Eq. (10) necessary beyond naive attempt-level
terminal. In each attempt, the model autoregressively pro-                          rewards? (Q3) How does calibration change the accuracy–
poses a candidate state sequence. The verifier returns rt = 1                       compute tradeoff across attempts? On MATH and Maze,
iff the proposed trajectory (i) reaches the absorbing terminal                      attempt-level credit assignment substantially improves over
state, (ii) uses only valid transitions in the Markov chain                         TL-GRPO. On the Markov chain task, however, naive
transition graph, (iii) the state id never decreases, and (iv)                      attempt-level normalization is not uniformly beneficial and
has length equal to the precomputed shortest-path distance                          can underperform TL-GRPO. Across all three benchmarks,
from s0 to the terminal. We also consider a trap variant,                           CAL-GRPO is the most robust method because Eq. (10)
where a trap state is sampled among two pre-terminal states                         reweights each attempt by its estimated marginal contribu-
in the last hub with 1/2 probability. Visiting the trap causes                      tion to final Ver@K.
immediate failure, and shortest-path distances are computed
on the graph with the trap removed. Under Ver@K, failed                             4.2.1. MATH and Maze tasks
attempts reset to the same start state, and the model retries
for up to K attempts with early stopping. The trapped ver-                          Attempt-level credit assignment improves learning over
sion needs Ver@K (K ≥ 2) approach to solve the problem                              trajectory-level credit assignment. Figures 2 and 4 show
as the trap is randomly selected for each trajectory.                               that, on MATH and Maze, moving from trajectory-level
                                                                                    credit assignment (TL-GRPO) to attempt-level credit as-
Models. For MATH and Maze, we train the instruction-                                signment (NAL-GRPO/CAL-GRPO) substantially improves
tuned Qwen3-4B-Instruct model (Yang et al., 2025). For                              learning under Ver@2 and Ver@4 objectives (please see Ap-
the Markov chain benchmark, we initialize the policy from                           pendix B for Ver@4 results). TL-GRPO assigns the same
an SFT checkpoint trained on synthetic optimal trajectories                         binary trajectory success signal to all tokens, so a trajec-
generated from the known transition graph. Concretely, we

                                                                                6
                                                  Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                      1.0       TL-GRPO                                             1.0   TL-GRPO                                                  2.0                            TL-GRPO
                                NAL-GRPO                                                  NAL-GRPO                                                                                NAL-GRPO
Validation Accuracy

                                                                                    0.8




                                                                                                                               Avg # of attempts
                      0.8       CAL-GRPO                                                  CAL-GRPO                                                 1.8                            CAL-GRPO




                                                                  Attempt Success
                      0.6                                                           0.6                                                            1.6
                                                                                          attempt 1
                                                                                          attempt 2
                      0.4                                                           0.4
                                                                                                                                                   1.4
                      0.2                                                           0.2
                                                                                                                                                   1.2
                      0.0                                                           0.0
                            0       5        10         15   20                              5            10      15     20                              0   5        10         15     20
                                        Training step                                             Training step                                                  Training step
  (a) Ver@2 validation accuracy on Maze (b) Attempt-wise success. Solid: attempt-1 (c) Average attempts per instance under
  across training; CAL-GRPO reaches higher success. Dashed: attempt-2 success given early stopping. NAL-GRPO minimizes the
  accuracy earlier, and all methods converge attempt-1 failure; CAL-GRPO yields the number of attempts, mimicking optimiza-
  near-perfect.                              strongest correction on the second attempt. tion of a discounted objective.
  Figure 4. Optimizing the Ver@2 objective on 5x5 Maze with GRPO variants. We compare Trajectory-Level GRPO (TL-GRPO),
  Naive Attempt-Level GRPO (NAL-GRPO), and Calibrated Attempt-Level GRPO (CAL-GRPO). (a) CAL-GRPO reaches higher Ver@2
  accuracy earlier in training. (b) NAL-GRPO increases attempt-1 success, while CAL-GRPO strengthens attempt-2 correction. (c)
  NAL-GRPO uses the fewest attempts, effectively behaving like optimization of a discounted objective.


   tory solved only on attempt 2 still provides positive updates                                           accurately, where further gains in attempt-1 accuracy have
   to the attempt-1 tokens that produced an incorrect first an-                                            diminishing returns for Ver@2 accuracy. As a result, CAL-
   swer. Under multi-attempt procedure, this mixes gradients                                               GRPO preserves more update budget for learning correction-
   for first-attempt correctness and correction-with-feedback,                                             with-feedback when second-attempt correction still con-
   yielding a noisy (and sometimes conflicting) learning signal                                            tributes substantially to Ver@2. Empirically, CAL-GRPO
   for improving attempt-1 behavior. In contrast, NAL-GRPO                                                 yields the best Ver@2 on both tasks (Figures 2a and 4a) by
   normalizes rewards separately per attempt among trajecto-                                               substantially increasing conditional second-attempt success
   ries that actually reach that attempt, which yields cleaner                                             (Figures 2b and 4b), at the cost of a modest increase in av-
   reward assignment: attempt 1 is trained on first-attempt cor-                                           erage attempts relative to NAL-GRPO (Figures 2c and 4c).
   rectness, and attempt 2 is trained on correction conditioned                                            This indicates that if the primary goal is Ver@K accuracy,
   on failure. This sharply accelerates attempt-1 success and                                              the attempt-weighted CAL-GRPO method works well; and
   correspondingly reduces the expected number of attempts                                                 if reducing number of attempts matters, NAL-GRPO can
   executed under early stopping (Figures 2c and 4c).                                                      be preferable. We provide further analysis and additional
                                                                                                           Maze results for 9×9 and 7×7 under Ver@2 and Ver@4 in
  Naive attempt-level normalization induces an early-
                                                                                                           Appendix B.
  attempt bias. However, NAL-GRPO implicitly down-
  weights later attempts as training progresses: because at-
                                                                                                           4.2.2. Markov chain task
  tempt t+1 is visited only on the shrinking subset of failure
  cases, the total gradient contribution of later attempts is ef-                                          A different regime under stricter verifier. Figure 3 pro-
  fectively multiplied by a reach probability, which prioritizes                                           vides a controlled comparison of TL-GRPO, NAL-GRPO,
  earlier-attempt correctness to minimize attempts, closely                                                and CAL-GRPO and highlights a qualitatively different
  aligning with Corollary 5.3. This indicates NAL-GRPO im-                                                 regime from MATH/Maze. We observe that NAL-GRPO
  plicitly optimizes a discounted objective where later steps                                              is the least sample-efficient and underperforms even TL-
  receive smaller weight once earlier steps become more ac-                                                GRPO in both the no-trap and trap settings. With a strict,
  curate.                                                                                                  sequence-level verifier (valid shortest path or nothing), per-
                                                                                                           attempt normalization can over-penalize early failed at-
   Calibration restores learning signal for later-attempts
                                                                                                           tempts and slow down learning progress. Under NAL-
   and improves final Ver@K. Our Calibrated Attempt-
                                                                                                           GRPO, attempt-1 tokens receive zero/negative advantage
   Level GRPO (CAL-GRPO) corrects this misalignment by
                                                                                                           whenever attempt 1 fails, even if the trajectory is “useful”
   reweighting attempts according to Eq. (10), which estimates
                                                                                                           in the sense that it enables a later attempt to succeed after
   the probability that all later attempts fail and therefore mea-
                                                                                                           feedback. On the other hand, TL-GRPO still propagates
   sures the marginal contribution of attempt t to final Ver@K
                                                                                                           eventual Ver@K success back to earlier tokens, which can
   success. Intuitively, this focuses attempt-1 updates on the
                                                                                                           implicitly reward early-attempt behaviors that set up effec-
   hard residual cases where a second attempt is unlikely to
                                                                                                           tive correction, and can therefore remain competitive.
   correct the mistake anyway, while avoiding over-investing
   in attempt-1 improvements when attempt 2 already succeeds                                               Calibration preserves useful correction signal. CAL-


                                                                                                      7
                               Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

GRPO consistently outperforms the other methods as it                    This theorem is a conjugate of Theorem 3.1 for the cal-
keeps attempt-aware reward assignment while explicitly                   ibrated attempt-level algorithm under Assumption 5.1. It
reweighting updates toward the later attempts that still con-            shows that the calibrated attempt-level algorithm is unbiased.
tribute the most to marginal Ver@K success by effectively                The proof is provided in Appendix D. Next, we analyze the
preserving learning budget for the correction behavior that              naive attempt index model. Before, define its single-attempt
drives the remaining improvements.                                       success probability for each attempt i,
                                                                                                                                 
CAL-GRPO breaks the trap-induced plateau earlier. In                            ρθ,i (x, y) := P ri = 1 | x, y, using policy π(i)
                                                                                                                              θ .
the trap variant of the Markov chain task, training exhibits
a plateau around ≈ 0.75 = 1 − (1/2)2 as trap state is random             As before, ri ∈ {0, 1} indicates whether the i-th response is
with 1/2 probability before further gains, which reflects the            correct with respect to the answer y.
additional late-stage failure mode introduced near the termi-            Corollary 5.3. The naive attempt-level algorithm optimizes
                                                                                                                     γi
                                                                           i∈[K] γi P(ri = 1) in expectation where γ j = Πt= j+1 (1 −
nal hub. The policy can learn the general “forward shortest-
                                                                         P                                                   i

path” behavior relatively quickly, but accurately avoiding               ρθ,i (x, y)) for i > j.
the trap while still satisfying the shortest-path constraint is
harder and becomes the dominant error source. CAL-GRPO                   This corollary is a direct result of the unbiasedness of
breaks through this plateau earlier than the other baselines,            bCAL (θ; x, y) by Theorem 5.2 and the definition of wCAL
                                                                         G RLOO                                                  n,i
which matches its intended behavior. Once attempt-1 be-                  in (10). It shows that the naive attempt-level algorithm op-
havior is already reasonably good, further improvements in               timizes a discounted loss as a function of K instead of the
Ver@K come from stabilizing correction behavior on retries               Verification@K loss defined in (1), which is consistent with
for the remaining hard cases (here, trap-related failures),              Figures 2c and 4c. It also shows that the naive attempt-
rather than continuing to over-optimize the first attempt.               level algorithm is biased whereas the proposed calibrated
                                                                         attempt-level algorithm is shown to be unbiased in Theorem
                                                                         5.2.
5. Optimization of Verification@K at Attempt
   Level
                                                                         6. Related Work
In Section 3, we have compared the trajectory-level opti-
mization and attempt-level optimization, and we have pro-                Reinforcement learning with verifiable feedback for rea-
vided a practical estimate of the attempt-level optimization             soning LLMs. Policy-gradient fine-tuning of reasoning
with the weighted attempt-level algorithm. In this section,              LLMs with automatically verifiable rewards has been ac-
we prove the unbiasedness of the weighted attempt-level                  tively explored across a range of settings (Guo et al., 2025;
algorithm and establish variance reduction guarantees under              Cui et al., 2025; Heckel et al., 2026; Wang et al., 2025;
the independent attempt index assumption we state below.                 Zhang et al., 2025b; Su et al., 2025). Several analyses
Furthermore, we provide more insights about the attempt-                 further study what such training changes in the model’s so-
level algorithm that we described in Section 3.                          lution distribution and how it interacts with pass@k-style
                                                                         evaluation (Yue et al., 2025; Wen et al., 2025). Complemen-
The independent attempt-index assumption is the following:               tary work improves optimization stability via refined reward
Assumption 5.1. For a fixed problem (x, y) and any attempt               assignment or denser intermediate learning signals (Kazem-
index i ∈ {1, . . . , K}, we assume that the conditional distribu-       nejad et al., 2025). In contrast, our work explicitly targets
tion of the i-th response depends only on x and the number               sequential retries with dependent attempts and directly opti-
of previous responses. Formally, for any two histories s1:i−1            mizes a Verification@K objective with attempt-level weight-
and s′1:i−1 of the same length,                                          ing to better match the long-CoT setting.
      pθ (yi = y | s1:i−1 ) = pθ (yi = y | s′1:i−1 )   for all y.        Multi-attempt and self-feedback for revision. Multi-
                                                                         attempt prompting and retry-based mechanisms can elicit
Assumption 5.1 implies that there exists a family of policies            iterative reasoning and answer revision in LLMs (Liu et al.,
(π(i)       K                                                            2025; Zelikman et al., 2022). Self-feedback and tool-
  θ (· | x))i=1 such that
                                                                         assisted critique loops further enable iterative refinement
        pθ (yi = y | s1:i−1 ) = π(i)
                                 θ (y | x),     i = 1, . . . , K.        and reflection without requiring per-instance human correc-
                                                                         tions (Madaan et al., 2023; Gou et al., 2024; Shinn et al.,
Now, we are ready to state the theorem:                                  2023). At the same time, several works characterize when
Theorem 5.2. Suppose that Assumption 5.1 holds. Recall                   self-correction succeeds or fails, emphasizing the impor-
                   bTL (θ; x, y) and G
the definitions of G                    bCAL (θ; x, y) in (5)            tance of reliable external feedback (Huang et al., 2024).
                     RLOO                  RLOO
and (11), respectively. Then, we have the following:
                                                                         Multi-turn RL and fine-grained reward assignment. A
                   RLOO (θ; x, y) = ∇θ ρθ (x, y).
                 bCAL           
              E G                                                        line of work studies RL for long-horizon, multi-turn LLM

                                                                     8
                           Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

agents, where sparse terminal rewards make reward assign-              gains, revealing an accuracy–compute trade-off that can be
ment difficult. In search and tool-use settings, recent meth-          tuned depending on whether peak Verification@K or fewer
ods add turn-level verifiable or judge-based rewards, intrin-          retries is the priority.
sic information-gain rewards, or finer step-level advantages
                                                                       A natural next step is to extend calibrated attempt-level
built from grouped trajectories, shared states, or trajectory
                                                                       weighting beyond hard binary verifiers to noisy/learned ver-
graphs (Wei et al., 2025; Wang et al., 2026; Feng et al.,
                                                                       ifiers feedback, and to characterize when unbiasedness and
2025; Li et al., 2025). In code and tool-integrated reasoning,
                                                                       variance-reduction guarantees still hold. It would also be
related approaches leverage execution feedback, learned
                                                                       valuable to scale to larger K and study adaptive compute
verifier scores, single-step rewards, discounted turn returns,
                                                                       allocation (adaptive K values) rather than using a fixed num-
reward shaping, or feedback-conditioned rollout trees to sup-
                                                                       ber of attempts.
port iterative self-correction (Jain et al., 2025; Ding et al.,
2025; Ekbote et al., 2026). Unlike these works, which
mostly improve generic long-horizon agent training with                References
task-specific turn- or step-level rewards, we study repeated           Aghajohari, M., Chitsaz, K., Kazemnejad, A., Chandar, S.,
attempts on the same input under hard verifier feedback and              Sordoni, A., Courville, A., and Reddy, S. The markovian
derive attempt-level weighting specifically for optimizing               thinker: Architecture-agnostic linear scaling of reasoning,
Verification@K.                                                          2025. URL https://arxiv.org/abs/2510.06557.
Verification@K, best-of-N, and verifier-guided test-time
scaling. Verifier-guided selection and reranking, such as              Ahmadian, A., Cremer, C., Gallé, M., Fadaee, M., Kreutzer,
Best-of-N and Pass@K, along with training objectives tai-                J., Pietquin, O., Üstün, A., and Hooker, S. Back to basics:
lored to optimize these criteria, form a common approach for             Revisiting reinforce style optimization for learning from
improving reasoning reliability (Cobbe et al., 2021; Zhang               human feedback in llms, 2024. URL https://arxiv.
et al., 2025a; Thrampoulidis et al., 2025; Mahdavi et al.,               org/abs/2402.14740.
2025). Process-level supervision and step-wise verifiers en-
able richer guidance signals for search and reasoning-time             Chen, Z., Qin, X., Wu, Y., Ling, Y., Ye, Q., Zhao, W. X.,
allocation (Lightman et al., 2023; Khalifa et al., 2025; Park            and Shi, G. Pass@k training for adaptively balancing
et al., 2024). More broadly, work on test-time compute                   exploration and exploitation of large reasoning models,
studies how to allocate sampling, search, and deliberation               2025. URL https://arxiv.org/abs/2508.10751.
budgets and how to adapt models at test time for improved
                                                                       Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
accuracy–compute tradeoffs (Snell et al., 2024; Wang et al.,
                                                                         Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
2023; Yao et al., 2023a; Gozeten et al., 2025).
                                                                         R., Hesse, C., and Schulman, J. Training verifiers to solve
                                                                         math word problems, 2021. URL https://arxiv.org/
7. Conclusion                                                            abs/2110.14168.
In this paper, we introduced a formal view of long chain-of-           Cui, G., Yuan, L., Wang, Z., Wang, H., Zhang, Y., Chen, J.,
thought as a multi-attempt process with dependent samples                Li, W., He, B., Fan, Y., Yu, T., Xu, Q., Chen, W., Yuan,
under verifier feedback, and studied direct optimization                 J., Chen, H., Zhang, K., Lv, X., Wang, S., Yao, Y., Han,
of the resulting Verification@K objective. From the cor-                 X., Peng, H., Cheng, Y., Liu, Z., Sun, M., Zhou, B., and
responding policy-gradient structure, we derived attempt-                Ding, N. Process reinforcement through implicit rewards,
aware credit assignment and proposed Calibrated Attempt-                 2025. URL https://arxiv.org/abs/2502.01456.
Level algorithm (CAL), which reweights per-attempt learn-
ing signals to better match each attempt’s marginal contri-            Dao, A. and Vu, D. B. Alphamaze: Enhancing large lan-
bution to Ver@K while keeping updates well-scaled.                       guage models’ spatial intelligence via grpo, 2025. URL
Across a controlled Markov chain benchmark (including                    https://arxiv.org/abs/2502.14669.
a trap variant) and real reasoning tasks (MATH and text-
                                                                       Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X.,
based Maze navigation), our empirical results show a con-
                                                                         Celikyilmaz, A., and Weston, J. Chain-of-verification
sistent pattern: trajectory-level training (TL) entangles first-
                                                                         reduces hallucination in large language models, 2023.
attempt correctness with later correction behavior, while
                                                                         URL https://arxiv.org/abs/2309.11495.
naive attempt-level training (NAL) yields cleaner optimiza-
tion and faster improvements in early-attempt success and              Ding, Y., Le, H., Han, S., Ruan, K., Jin, Z., Kumar, V.,
efficiency in number of attempts. CAL further improves                   Wang, Z., and Deoras, A. Empowering multi-turn tool-
final Ver@K by sustaining useful learning pressure on later              integrated reasoning with group turn policy optimization,
attempts when they remain the primary driver of additional               2025. URL https://arxiv.org/abs/2511.14846.

                                                                   9
                            Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

Ekbote, C., Lingam, V., Sanghavi, S., Huan, J., Omidvar-                   doi: 10.1038/s41586-025-09422-z. URL http://dx.
  Tehrani, B., Deoras, A., and Soatto, S. Murphy: Multi-                   doi.org/10.1038/s41586-025-09422-z.
  turn grpo for self correcting code generation, 2026. URL
  https://arxiv.org/abs/2511.07833.                                      Heckel, R., Soltanolkotabi, M., and Thramboulidis, C.
                                                                           Asymmetric prompt weighting for reinforcement learning
Feng, L., Xue, Z., Liu, T., and An, B. Group-in-group                      with verifiable rewards. arXiv preprint arXiv:2602.11128,
  policy optimization for llm agent training, 2025. URL                    2026.
  https://arxiv.org/abs/2505.10978.
                                                                         Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,
Gou, Z., Shao, Z., Gong, Y., Shen, Y., Yang, Y., Duan,                     S., Tang, E., Song, D., and Steinhardt, J. Measuring math-
  N., and Chen, W. Critic: Large language models can                       ematical problem solving with the math dataset, 2021.
  self-correct with tool-interactive critiquing, 2024. URL                 URL https://arxiv.org/abs/2103.03874.
  https://arxiv.org/abs/2305.11738.                                      Huang, J., Chen, X., Mishra, S., Zheng, H. S., Yu, A. W.,
                                                                           Song, X., and Zhou, D. Large language models cannot
Gozeten, H. A., Ildiz, M. E., Zhang, X., Soltanolkotabi, M.,
                                                                           self-correct reasoning yet, 2024. URL https://arxiv.
  Mondelli, M., and Oymak, S. Test-time training provably
                                                                           org/abs/2310.01798.
  improves transformers as in-context learners. In Forty-
  second International Conference on Machine Learning,                   Ivanitskiy, M. I., Shah, R., Spies, A. F., Räuker, T., Valen-
  2025. URL https://openreview.net/forum?id=                               tine, D., Rager, C., Quirke, L., Mathwin, C., Corlouer, G.,
  bma2FB5MNs.                                                              Behn, C. D., and Fung, S. W. A configurable library for
                                                                           generating and manipulating maze datasets, 2023. URL
Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q.,                 https://arxiv.org/abs/2309.10498.
 Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu,
 Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A.,             Jain, A. K., Gonzalez-Pumariega, G., Chen, W., Rush,
 Xue, B., Wang, B., Wu, B., Feng, B., Lu, C., Zhao, C.,                    A. M., Zhao, W., and Choudhury, S. Multi-turn code
  Deng, C., Ruan, C., Dai, D., Chen, D., Ji, D., Li, E., Lin,               generation through single-step rewards, 2025. URL
  F., Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H.,               https://arxiv.org/abs/2502.20380.
 Xu, H., Ding, H., Gao, H., Qu, H., Li, H., Guo, J., Li,
 J., Chen, J., Yuan, J., Tu, J., Qiu, J., Li, J., Cai, J. L., Ni,        Kazemnejad, A., Aghajohari, M., Portelance, E., Sordoni,
 J., Liang, J., Chen, J., Dong, K., Hu, K., You, K., Gao,                  A., Reddy, S., Courville, A., and Roux, N. L. Vineppo:
  K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,                    Refining credit assignment in rl training of llms, 2025.
  Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,                   URL https://arxiv.org/abs/2410.01679.
  M., Zhang, M., Tang, M., Zhou, M., Li, M., Wang, M.,                   Khalifa, M., Agarwal, R., Logeswaran, L., Kim, J., Peng,
  Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q., Chen,                  H., Lee, M., Lee, H., and Wang, L. Process reward
  Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R., Chen,                  models that think, 2025. URL https://arxiv.org/
  R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen, S., Ye,             abs/2504.16828.
  S., Wang, S., Yu, S., Zhou, S., Pan, S., Li, S. S., Zhou, S.,
 Wu, S., Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Liu,             Li, J., Wang, Y., Yan, D., Tian, Y., Xu, Z., Song, H., Xu, P.,
 W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao, W. L.,                   and Cheong, L. L. Salt: Step-level advantage assignment
 An, W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng, X.,                  for long-horizon agents via trajectory graph, 2025. URL
  Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su, X., Lin, X.,            https://arxiv.org/abs/2510.20022.
  Li, X. Q., Jin, X., Shen, X., Chen, X., Sun, X., Wang, X.,
  Song, X., Zhou, X., Wang, X., Shan, X., Li, Y. K., Wang,               Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
 Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y., Zhao, Y., Sun,              B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
 Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y., Xiong, Y., He, Y.,              Cobbe, K. Let’s verify step by step, 2023. URL https:
  Piao, Y., Wang, Y., Tan, Y., Ma, Y., Liu, Y., Guo, Y., Ou,               //arxiv.org/abs/2305.20050.
 Y., Wang, Y., Gong, Y., Zou, Y., He, Y., Xiong, Y., Luo,                Liu, L., Wang, Z., Li, L., Xu, C., Lu, Y., Liu, H., Sil, A.,
 Y., You, Y., Liu, Y., Zhou, Y., Zhu, Y. X., Huang, Y., Li,                and Li, M. A simple "try again" can elicit multi-turn
 Y., Zheng, Y., Zhu, Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y.,               llm reasoning, 2025. URL https://arxiv.org/abs/
  Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang,            2507.14295.
  Z., Hao, Z., Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu,
  Z., Li, Z., Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu,                 Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L.,
  Z., Zhang, Z., and Zhang, Z. Deepseek-r1 incentivizes                   Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang,
  reasoning in llms through reinforcement learning. Nature,               Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck,
  645(8081):633–638, September 2025. ISSN 1476-4687.                      S., Yazdanbakhsh, A., and Clark, P. Self-refine: Iterative

                                                                    10
                          Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

  refinement with self-feedback, 2023. URL https://                   Su, Y., Yu, D., Song, L., Li, J., Mi, H., Tu, Z., Zhang, M.,
  arxiv.org/abs/2303.17651.                                             and Yu, D. Crossing the reward bridge: Expanding rl with
                                                                        verifiable rewards across diverse domains, 2025. URL
Mahdavi, S., Li, M., Liu, K., Liao, R., and Thrampoulidis,              https://arxiv.org/abs/2503.23829.
 C. Beyond accuracy: A policy gradient reweighting
 approach for pass@k maximization in LLMs. In 2nd AI                  Sutton, R. S., McAllester, D., Singh, S., and Man-
 for Math Workshop @ ICML 2025, 2025. URL https:                        sour, Y. Policy gradient methods for reinforcement
 //openreview.net/forum?id=Dn3gk9auxd.                                  learning with function approximation.     In Solla,
                                                                        S., Leen, T., and Müller, K. (eds.), Advances in
Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright,                 Neural Information Processing Systems, volume 12.
  C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K.,                MIT Press, 1999.     URL https://proceedings.
  Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L.,            neurips.cc/paper_files/paper/1999/file/
  Simens, M., Askell, A., Welinder, P., Christiano, P., Leike,          464d828b85b0bed98e80ade0a5c43b0f-Paper.pdf.
 J., and Lowe, R. Training language models to follow
                                                                      Thrampoulidis, C., Mahdavi, S., and Deng, W. Advan-
  instructions with human feedback, 2022. URL https:
                                                                        tage shaping as surrogate reward maximization: Uni-
 //arxiv.org/abs/2203.02155.
                                                                        fying pass@k policy gradients, 2025. URL https:
Park, S., Liu, X., Gong, Y., and Choi, E. Ensembling                    //arxiv.org/abs/2510.23049.
  large language models with process reward-guided tree               Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,
  search for better complex reasoning, 2024. URL https:                Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-
  //arxiv.org/abs/2412.15797.                                           ing math word problems with process- and outcome-
                                                                        based feedback, 2022. URL https://arxiv.org/abs/
Schulman, J., Moritz, P., Levine, S., Jordan, M., and                   2211.14275.
  Abbeel, P. High-dimensional continuous control using
  generalized advantage estimation, 2018. URL https:                  Volcengine. veRL: Volcano engine reinforcement learning
  //arxiv.org/abs/1506.02438.                                           for LLMs. https://github.com/volcengine/verl,
                                                                        2024.
Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X.,
  Zhang, H., Zhang, M., Li, Y. K., Wu, Y., and Guo,                   Wang, G., Dai, S., Ye, G., Gan, Z., Yao, W., Deng, Y.,
  D. Deepseekmath: Pushing the limits of mathemat-                     Wu, X., and Ying, Z. Information gain-based policy
  ical reasoning in open language models, 2024. URL                    optimization: A simple and effective approach for multi-
  https://arxiv.org/abs/2402.03300.                                    turn search agents, 2026. URL https://arxiv.org/
                                                                       abs/2510.14967.
Sheng, G., Zhang, C., Ye, Z., Wu, X., Zhang, W., Zhang,
  R., Peng, Y., Lin, H., and Wu, C. Hybridflow: A                     Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang,
  flexible and efficient rlhf framework. In Proceedings                S., Chowdhery, A., and Zhou, D. Self-consistency im-
  of the Twentieth European Conference on Computer                     proves chain of thought reasoning in language models,
  Systems, EuroSys ’25, pp. 1279–1297. ACM, March                      2023. URL https://arxiv.org/abs/2203.11171.
  2025. doi: 10.1145/3689031.3696075. URL http:                       Wang, Y., Yang, Q., Zeng, Z., Ren, L., Liu, L., Peng, B.,
  //dx.doi.org/10.1145/3689031.3696075.                                Cheng, H., He, X., Wang, K., Gao, J., Chen, W., Wang,
                                                                       S., Du, S. S., and Shen, Y. Reinforcement learning for
Shinn, N., Cassano, F., Berman, E., Gopinath, A.,
                                                                       reasoning in large language models with one training
  Narasimhan, K., and Yao, S. Reflexion: Language
                                                                       example, 2025. URL https://arxiv.org/abs/2504.
  agents with verbal reinforcement learning, 2023. URL
                                                                       20571.
  https://arxiv.org/abs/2303.11366.
                                                                      Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,
Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling llm                  Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-thought
  test-time compute optimally can be more effective than               prompting elicits reasoning in large language models,
  scaling model parameters, 2024. URL https://arxiv.                   2023. URL https://arxiv.org/abs/2201.11903.
  org/abs/2408.03314.
                                                                      Wei, Q., Zeng, S., Li, C., Brown, W., Frunza, O., Deng, W.,
Stiennon, N., Ouyang, L., Wu, J., Ziegler, D. M., Lowe,                Schneider, A., Nevmyvaka, Y., Zhao, Y. K., Garcia, A.,
   R., Voss, C., Radford, A., Amodei, D., and Christiano,              and Hong, M. Reinforcing multi-turn reasoning in llm
   P. Learning to summarize from human feedback, 2022.                 agents via turn-level reward design, 2025. URL https:
   URL https://arxiv.org/abs/2009.01325.                               //arxiv.org/abs/2505.11821.

                                                                 11
                          Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

Wen, X., Liu, Z., Zheng, S., Ye, S., Wu, Z., Wang, Y., Xu,            Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H.,
 Z., Liang, X., Li, J., Miao, Z., Bian, J., and Yang, M.                Cao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Bar-
 Reinforcement learning with verifiable rewards implicitly              rett, C., and Sheng, Y. Sglang: Efficient execution of
 incentivizes correct reasoning in base llms, 2025. URL                 structured language model programs, 2024.
 https://arxiv.org/abs/2506.14245.

Williams, R. J. Simple statistical gradient-following algo-
 rithms for connectionist reinforcement learning. Ma-
 chine Learning, 8(3–4):229–256, 1992. doi: 10.
 1007/BF00992696. URL https://doi.org/10.1007/
 BF00992696.

Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng,
  B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu,
  D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin,
  H., Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang,
  J., Zhou, J., Zhou, J., Lin, J., Dang, K., Bao, K., Yang,
  K., Yu, L., Deng, L., Li, M., Xue, M., Li, M., Zhang,
  P., Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo,
  S., Li, T., Tang, T., Yin, W., Ren, X., Wang, X., Zhang,
  X., Ren, X., Fan, Y., Su, Y., Zhang, Y., Zhang, Y., Wan,
  Y., Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., and
  Qiu, Z. Qwen3 technical report, 2025. URL https:
  //arxiv.org/abs/2505.09388.

Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao,
  Y., and Narasimhan, K. Tree of thoughts: Deliberate
  problem solving with large language models, 2023a. URL
  https://arxiv.org/abs/2305.10601.

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
  K., and Cao, Y. React: Synergizing reasoning and acting
  in language models, 2023b. URL https://arxiv.org/
  abs/2210.03629.

Yue, Y., Chen, Z., Lu, R., Zhao, A., Wang, Z., Yue, Y., Song,
  S., and Huang, G. Does reinforcement learning really
  incentivize reasoning capacity in llms beyond the base
  model?, 2025. URL https://arxiv.org/abs/2504.
  13837.

Zelikman, E., Wu, Y., Mu, J., and Goodman, N. D. Star:
  Bootstrapping reasoning with reasoning, 2022. URL
  https://arxiv.org/abs/2203.14465.

Zhang, L., Hosseini, A., Bansal, H., Kazemi, M., Kumar, A.,
  and Agarwal, R. Generative verifiers: Reward modeling
  as next-token prediction, 2025a. URL https://arxiv.
  org/abs/2408.15240.

Zhang, X., Huang, Z., Li, Y., Ni, C., Chen, J., and Oymak, S.
  Bread: Branched rollouts from expert anchors bridge sft
  & rl for reasoning. In The Thirty-ninth Annual Conference
  on Neural Information Processing Systems, 2025b.

                                                                 12
                           Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

A. Experimental Details
A.1. Implementation of Ver@K GRPO Training
We train policies with Ver@K using a multi-turn interaction loop implemented on top of the veRL/HybridFlow frame-
work (Sheng et al., 2025; Volcengine, 2024) and its multi-turn interaction system with an SGLang rollout backend (Zheng
et al., 2024). We modify the veRL source code to support (i) multi-attempt rollout with the same maximum output length
and (ii) attempt-wise GRPO reward normalization and reweighting for the estimators described in Sections 3 and 4.
Each rollout allows up to K assistant attempts. After attempt k, a deterministic verifier returns a binary reward signal
rk ∈ {0, 1}. If rk = 1, the interaction terminates. Otherwise, if attempts remain, we inject a fixed feedback message indicating
the attempt was incorrect and request another attempt. Attempts not reached due to early stopping are excluded from
attempt-wise normalization at that step.

A.2. Datasets and Prompting
MATH. We train and evaluate on the MATH dataset (Hendrycks et al., 2021). Each example is converted into a single-
attempt chat prompt consisting of the problem statement followed by the instruction: “Let’s think step by step and put the
final answer in \boxed{}.”
Maze. We generate maze navigation datasets using the maze-dataset library (Ivanitskiy et al., 2023). For each maze
size (5×5, 7×7, 9×9), we generate 10k training and 1k test instances. Mazes are sampled with the library’s randomized
depth-first-search lattice generator and converted to a text representation for prompting (Ivanitskiy et al., 2023). We follow
prior work studying maze navigation and multi-sample objectives for reasoning models (Dao & Vu, 2025; Chen et al., 2025).
Each maze prompt provides an ASCII grid with walls/free cells and explicit start/goal markers. The model is instructed to
output a move sequence inside <answer>...</answer> using the alphabet {U,D,L,R}.
Markov chain. We construct a synthetic planning benchmark based on a structured Markov chain, designed to isolate
multi-attempt credit assignment under a deterministic verifier with controllable difficulty. The state space is organized into
nhubs ordered hubs with m states per hub (nstates = nhubs · m). The transition graph is fixed across instances: transitions are
predominantly local within a hub (e.g., to nearby states within ±1 positions), with sparse boundary transitions connecting
consecutive hubs; the final state in the last hub is an absorbing terminal state. Each instance samples a start state s0 from the
set of states that can reach the terminal. In each attempt, the model generates a token sequence representing a candidate state
trajectory, and the verifier simulates it on the transition graph and returns rt =1 iff the trajectory reaches the terminal, uses
only valid transitions, never decreases the state id, and has length equal to the precomputed shortest-path distance from s0 to
the terminal (i.e., it is an optimal-length path). We train with Ver@K by separating attempts with a special RETRY token;
after a failed attempt, the interaction resets to the same start state and the model retries up to K attempts with early stopping.
We also consider a trap variant where a trap state is sampled per rollout from two pre-terminal states in the last hub; visiting
the trap causes immediate failure, and shortest-path distances are computed on the transition graph with the trap removed.

A.3. Verifiers and Rewards
MATH verifier. We extract the final boxed expression from the model output, apply normalization, and check equivalence
against the ground-truth answer. The per-attempt reward is rk =1 if correct and 0 otherwise.
Maze verifier. We extract the move string from <answer> tags, normalize to {U,D,L,R}, and simulate the trajectory on the
maze. The per-attempt reward is rk =1 iff the move sequence reaches the goal without crossing walls or leaving the grid;
otherwise 0.
Markov chain verifier. Given a proposed state sequence for an attempt, we simulate it on the chain and return rk ∈ {0, 1}.
An attempt receives rk = 1 iff it reaches the absorbing terminal state, all transitions are valid under the chain’s transition
structure, the state id never decreases, and the attempt length equals the precomputed shortest-path distance from the start
state. In the trap variant, visiting the sampled trap state causes immediate failure and shortest-path distances are computed
with the trap removed.




                                                               13
                           Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

A.4. Rollout, Sampling, and Optimization
Model and algorithm. For MATH and Maze, we fine-tune Qwen3-4B-Instruct-2507 (Yang et al., 2025) using GRPO (Shao
et al., 2024), implemented in veRL (Sheng et al., 2025; Volcengine, 2024) with our multi-turn and estimator modifications
(Appendix A.5). For the Markov chain task, we initialize the policy from an SFT checkpoint and then apply the same
Ver@K GRPO procedure.
Markov-chain SFT initialization. The SFT checkpoint used to initialize the Markov-chain runs is trained on synthetic
optimal state trajectories. For each synthetic instance, we sample a start state from the states that can reach the terminal; in
the trap setting, we additionally sample the trap state from the two pre-terminal states in the last hub. We then compute the
corresponding shortest valid trajectory to the absorbing terminal state on the known transition graph (with the trap removed
when applicable) and train the model to emit that state-id sequence. This SFT checkpoint is used only as initialization, and
all TL-GRPO, NAL-GRPO, and CAL-GRPO runs then use the same Ver@K GRPO setup described below.
Rollout and decoding. We use SGLang for rollout generation (Zheng et al., 2024). Decoding uses temperature 0.6, top-p
0.95, and top-k 20. The GRPO group size (number of rollouts per prompt) is N=20 for MATH and N=16 for Maze. We
evaluate every 5 iterations. Unless otherwise stated, reported curves correspond to a single training run. For the 5×5 and
9×9 Maze Ver@2 experiments, we repeat training with five random seeds and report the mean together with 95% confidence
intervals across runs. We focus this multi-seed evaluation on these Maze Ver@2 settings due to computational constraints.
For Markov chain setting, we generate rollouts with a lightweight token-level simulator (no tool calls): the model emits
discrete state-id tokens in {0, . . . , nstates −1}, with attempts separated by an injected RETRY token that resets the attempt to
the same start state. Concretely, the RETRY token id is set to nstates and the PAD token id to nstates +1, where nstates = nhubs · m.
We sample with temperature 1.0 and disable top-k truncation (top-k=0). For each update, we sample a batch of start states,
repeat each start state to form a rollout group, and roll out K attempts per start. In the trap variant, start states are sampled
only from hubs before the last hub so that the sampled trap remains ahead in the chain.
Sequence lengths. We cap each attempt to 512 output tokens for MATH and for the 5×5 Maze task, and to 1024 new tokens
for the 9×9 Maze task. With K=2, the total assistant budget is 1024 tokens (MATH and 5×5 Maze) or 2048 tokens (9×9
Maze) plus a small buffer for system/feedback, yielding a maximum rollout length of 1280 tokens (MATH and 5×5 Maze)
or 2304 tokens (9×9 Maze).
For the Markov chain setting, we cap the length of each attempt to a fixed token budget. By default this budget is set to the
total number of states, but it is never allowed to exceed the model’s maximum context length. We choose the per-attempt cap
so that all attempts can be packed into a single context window, while also reserving space for the inserted RETRY separator
tokens between attempts. An attempt terminates if it reaches the absorbing terminal state, emits RETRY/PAD/EOS, outputs an
out-of-range state id (invalid), or hits the per-attempt token cap.
Optimization. We train with AdamW at learning rate 10−6 with a KL penalty coefficient of 0.001, a clip ratio ϵ = 0.2, and
no entropy bonus. We use a train batch size of 256, PPO mini-batch size 64, and PPO micro-batch size 8 per GPU with
dynamic batching. We train for 2 epochs on MATH and 1 epoch on Maze. We used 2× NVIDIA L40S or A100 GPUs
during the training.
For Markov chain setting, we use AdamW with parameters (0.9, 0.95), PPO-style ratio clipping with ϵ = 0.2. We use
learning rate 10−5 and a KL penalty coefficient of 0.02. For non-trap runs: We train for 1600 steps, batch size of 8, rollout
group size N = 40, and K = 4 attempts per start state. Trap runs: We train for 5000 steps, batch size of 16, rollout group
size N = 40, and K = 2 attempts per start state. We evaluate using 500 × nstates start states and evaluate every 40 iterations.

    Verification feedback in MATH
    Your previous attempt(s) were incorrect. Review them and try again.
    Solve the problem again from scratch, correcting any mistakes.
    Final answer must be \boxed{<answer>}.


    Verification feedback in Maze
    Your previous attempt(s) were incorrect. Review them and try again.
    Solve the maze again from scratch, correcting any mistakes.



                                                                14
                           Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought


    Final answer must be a move string over U,D,L,R only in <answer>...</answer>.


    Example Answer

                                                    <answer>UU</answer>


    Example Maze Question

    You need to solve the following maze.

   ’*’ denotes the wall that you cannot walk through, ’.’ denotes available area that you can walk
   through. ’S’ denotes the starting point, ’E’ denotes the destination.

    You need to start from the starting point and cross through the available area to reach the
    destination. There are four movement actions, including Left, Right, Up, Down.

    Use L to denote Left movement, R to denote Right movement, U to denote Up movement, and D to
    denote Down movement.

   You can analyze the maze to find the correct path, and you should write the final path in the
   <answer></answer>, e.g., <answer>LLRRDUL</answer>.

   ## Maze
   *********
   *.....*E*
   *****.*.*
   *...*..S*
   *.*****.*
   *.......*
   *.*******
   *.......*
   *********
   Now try to analyze the maze and put the final path in the <answer></answer>.


    Markov Chain reward and termination logic

    For each attempt, the model autoregressively emits state-id tokens.
    Reward=1 iff: (1) the terminal absorbing state is reached; (2) all transitions follow the
    allowed adjacency; (3) the state id never decreases; (4) the number of steps equals the
    shortest-path distance from the start.
    Trap variant: a trap state is sampled per rollout from two pre-terminal states in the last hub;
    visiting it makes Reward=0, and shortest paths are computed with the trap removed.


    Example Trajectories for Markov Chain for Ver@2

    Example parameters: nhubs = 5, m = 6 (nstates = 30), start s0 = 0, terminal=29.
    Attempt 1 (failure, backtrack):     0 → 2 → 0 → 1 → ...
    RETRY
    Attempt 2 (success, shortest path):      0 → 1 → 3 → 5 → ...→ 27 → 29.
    Trap variant (e.g., trap=28): the above success remains valid; any visit to 28 during an
    attempt yields rk = 0.



A.5. GRPO Variants
Fix a prompt instance x (and its ground-truth y), and draw a GRPO group of N i.i.d. multi-attempt trajectories τ1 , . . . , τN ∼
pθ (· | x), as in Section 3. Each trajectory τn executes attempts k ∈ {1, . . . , K} with early stopping: at attempt k the policy

                                                               15
                           Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

produces an output yn,k ∼ πθ (· | sn,k−1 ) and a deterministic verifier returns rn,k ∈ {0, 1}. The stopping time is

                                   T n := min{k ≤ K : rn,k = 1}                 (or T n = K if no success).

Define the reach indicator 1[T n ≥ k] and the reached-set

                                                         S k := {n ∈ [N] : T n ≥ k}.

We also define a token mask mn,t ∈ {0, 1} indicating model-generated tokens, and let turn(n, t) ∈ {1, . . . , K} denote the
attempt index of token t. We use the standard GRPO normalization for all variants below, by dividing centered rewards
by the corresponding within-group empirical standard deviation. This rescaling is not part of the RLOO derivations in
Sections 3 and 5, but we use it in practice because it improves optimization, and Figure 13c reports a direct ablation for this
on Maze Ver@2.
Trajectory-Level GRPO (TL-GRPO). Let the trajectory-level Ver@K reward be
                                                                    h            i
                                                   rnTL := rn,Tn = 1 max rn,k = 1 .
                                                                                k≤K

We compute the usual GRPO group-normalized advantage

                                                                            N
                                        rnTL − µ                  1 X TL
                                    n =
                                   aTL           ,             µ=      r ,                  σ = Std {rnTL }n=1 ,
                                                                                                           N 
                                               σ                  N n=1 n

and assign token-level advantages
                                                               An,t = aTL
                                                                       n · mn,t .


Naive Attempt-Level GRPO (NAL-GRPO). For each attempt k, we normalize the per-attempt verifier outcomes rn,k only
over trajectories that reach attempt k:

                                 rn,k − µk                                           1 X
                         n,k =
                        aNAL                   for n ∈ S k ,            µk =                  rn,k ,   σk = Std {rn,k }n∈S k .
                                                                                                                            
                                     σk                                            |S k | n∈S
                                                                                             k



Each token inherits the attempt-level advantage of its attempt:

                                                            An,t = aNAL
                                                                    n,turn(n,t) · mn,t .


Calibrated Attempt-Level GRPO (CAL-GRPO). CAL-GRPO starts from NAL-GRPO and reweights attempts by a
future-only factor that approximates each attempt’s marginal contribution to final Ver@K success. Define the empirical
per-attempt success rates
                                                            1 X
                                                   p̂k :=            rn,k .
                                                          |S k | n∈S
                                                                                    k


Then define future-only weights:
                                                             K
                                                             Y
                                                   wk =             (1 − p̂ j ),          wK = 1.
                                                            j=k+1

We renormalize weights within the group to keep update scales comparable, e.g.,

                                          1 X                                                                    wk
                                  w̄ =           wk ,      K := {k ∈ [K] : |S k | > 0},                  w̃k =      .
                                         |K| k∈K                                                                 w̄

Final token-level advantages are
                                                        An,t = w̃turn(n,t) aNAL
                                                                            n,turn(n,t) mn,t .


                                                                          16
                                              Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                                                                                     0.50
                       500                                                                                                                         1.3
Mean Response Length




                                                                Attempt Reward Std
                       480
                                                                                             TL-GRPO




                                                                                                                                 Attempt Weights
                              TL-GRPO                                                0.45    NAL-GRPO                                              1.2
                       460    NAL-GRPO              attempt 1                                CAL-GRPO
                              CAL-GRPO              attempt 2                        0.40                                                          1.1                          attempt 1
                       440                                                                                                                                                      attempt 2
                                                                                                                                                   1.0
                       420                                                           0.35
                       400                                                                                           attempt 1                     0.9
                                                                                                                     attempt 2
                       380                                                           0.30                                                          0.8
                             10   20     30    40      50                                   10   20        30   40      50                               10   20    30     40      50
                                   Training step                                                  Training step                                                Training step
  (a) Mean response length per attempt vs. (b) Attempt reward standard deviation (c) Attempt weights used by CAL-GRPO
  training step (baselines labeled in legend: within each GRPO group (signal magnitude (future-only reweighting), plotted for at-
  TL-GRPO, NAL-GRPO, CAL-GRPO).               for normalization), shown separately for at- tempts 1 and 2 over training.
                                              tempts 1 and 2.
  Figure 5. Additional metrics for Ver@2 training on MATH. (a) Response length dynamics per attempt. (b) Per-attempt reward
  variability used by normalization. (c) Learned future-only attempt reweighting in CAL-GRPO.



   B. Additional Experimental Results for Section 4
   Discussion on the additional results. Figures 5, 6, 8, 10, 12 and 13 report additional diagnostics and ablations for the three
   estimators (TL-GRPO/NAL-GRPO/CAL-GRPO). For Maze, we include Ver@2 on 5×5 and 9×9 (see also Figures 7 and 7a),
   as well as Ver@4 on 7×7 and 9×9 (see Figures 9 and 11), and rollout-group-size and standard-deviation-normalization
   ablations under Ver@2 (see Figure 13). We make the following observations:
  Weights track marginal contribution. Across tasks, the future-dependent weights in CAL-GRPO shift learning signal
  away from early attempts and toward later attempts as training progresses. For Ver@2, CAL-GRPO downweights attempt
  1 and upweights attempt 2 over training (Figures 5c, 6c and 8c). For Ver@4, this pattern generalizes: attempts 1–2 are
  increasingly downweighted while attempts 3–4 are upweighted (Figures 10c and 12c), which counteracts the fact that later
  attempts are reached on a shrinking subset of hard failures and would otherwise receive a vanishing share of updates. The
  reweighting is strongest in easier/near-saturating regimes—notably 5×5 under Ver@2 and 7×7 under Ver@4—where retries
  become highly reliable and the marginal value of further improving the first attempt diminishes. On 9×9 (both Ver@2
  and Ver@4), weights remain less extreme, consistent with a harder regime where multiple attempts continue to contribute
  meaningfully to final Ver@K accuracy (Figures 7a and 9a).
   Gains without longer generations. Mean response length decreases over training on MATH and across all Maze settings
   we report, for both Ver@2 and Ver@4 (Figures 5a, 6a, 8a, 10a and 12a), indicating that Ver@K gains are not driven by
   longer generations. On 5×5 (Ver@2), CAL-GRPO notably shortens the second attempt late in training, directly reducing
   test-time compute under early stopping. On 9×9 (Ver@2), the dominant effect is a steady reduction in attempt-1 length
   with controlled retry length, suggesting improved first-pass planning without incurring longer corrections. For Ver@4 on
   7×7 and 9×9, response lengths generally drop across attempts 1-4, with later attempts often shortening substantially late in
   training (Figures 10a and 12a), consistent with learning more efficient correction rather than longer retries.
   Attempt-dependent normalization matters. The within-group reward standard deviation differs across attempts and
   evolves over training for both Ver@2 and Ver@4 (Figures 5b, 6b, 8b, 10b and 12b), reinforcing the claim that a single
   trajectory-level normalization can mis-scale gradients for later attempts. This heterogeneity becomes more salient as K
   grows: under Ver@4, attempts 3–4 can exhibit markedly different reward-variance dynamics than attempts 1–2. On 5×5 with
   Ver@2, attempt-2 variability rises early but collapses late as retry outcomes become near-deterministic once performance
   approaches ceiling; by contrast, on 9×9 with Ver@2 the retry variance remains substantial throughout training, supporting
   the fact that Ver@2 does not fully saturate and learning signal on retries remains informative (Figure 7a). Similarly,
   for Ver@4, variance patterns differ across 7×7 vs. 9×9 (Figures 10b and 12b), aligning with the corresponding Ver@4
   learning curves (Figures 9a and 11a). Overall, these demonstrations help explain why CAL-GRPO’s reweighting becomes
   increasingly important for larger K as it preserves learning pressure on later-attempt correction when those retries remain a
   key driver of marginal Ver@K improvements.
   Ablation on standard deviation normalization. Consistent with the attempt-dependent variance patterns above, the direct
   Maze Ver@2 ablation in Figure 13c shows that dividing by the within-group empirical standard deviation improves sample

                                                                                                      17
                                                   Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                                                                                                0.5       TL-GRPO                                                           2.0
                       500                                    attempt 1
Mean Response Length

                                                              attempt 2                                   NAL-GRPO                                                          1.8




                                                                           Attempt Reward Std
                       480                                                                                CAL-GRPO




                                                                                                                                                        Attempt Weights
                                                                                                0.4                                                                         1.6
                       460                                                                                                                                                  1.4
                       440                                                                      0.3                                                                         1.2
                                  TL-GRPO
                       420        NAL-GRPO                                                                                                                                  1.0                                      attempt 1
                                  CAL-GRPO                                                      0.2                                                                                                                  attempt 2
                       400                                                                                                                                                  0.8
                       380                                                                      0.1                                        attempt 1                        0.6
                       360                                                                                                                 attempt 2                        0.4
                                     5       10          15           20                                      5            10         15           20                                     5         10          15           20
                                         Training step                                                             Training step                                                                Training step
  (a) Mean response length per attempt vs. (b) Attempt reward standard deviation (c) Attempt weights used by CAL-GRPO
  training step (baselines labeled in legend: within each GRPO group, shown separately (future-only reweighting), for attempts 1 and
  TL-GRPO, NAL-GRPO, CAL-GRPO).               for attempts 1 and 2.                    2 over training.
  Figure 6. Additional metrics for Ver@2 training on 5x5 Maze task. (a) Response length dynamics per attempt. (b) Per-attempt reward
  variation used during the per attempt normalization. (c) Learned future-only attempt reweighting in CAL-GRPO.


                       0.7       TL-GRPO                                                        0.6       TL-GRPO                                                           2.0                                  TL-GRPO
                       0.6       NAL-GRPO                                                       0.5       NAL-GRPO                                                                                               NAL-GRPO
Validation Accuracy




                                                                                                                                                                            1.9




                                                                                                                                                        Avg # of attempts
                                 CAL-GRPO                                                                 CAL-GRPO                                                                                               CAL-GRPO
                                                                           Attempt Success




                       0.5                                                                      0.4                                                                         1.8
                       0.4                                                                                attempt 1
                                                                                                0.3       attempt 2                                                         1.7
                       0.3
                                                                                                0.2                                                                         1.6
                       0.2
                       0.1                                                                      0.1
                                                                                                                                                                            1.5
                       0.0                                                                      0.0
                             0   5   10 15 20 25 30 35 40                                             0   5   10      15    20   25   30      35   40                             0   5       10 15 20 25 30 35 40
                                         Training step                                                             Training step                                                               Training step
  (a) Ver@2 validation accuracy on 9×9                                       (b) Attempt-wise success. Solid: attempt- (c) Average attempts Ver@2; NAL/CAL
  Maze across training; CAL-GRPO achieves                                    1 success. Dashed: attempt-2 success reduce number of attempts relative to TL-
  the highest Ver@2, with NAL-GRPO im-                                       given attempt-1 failure; NAL-GRPO boost GRPO.
  proving over TL-GRPO.                                                      attempt-1 success while CAL improves cor-
                                                                             rection.
  Figure 7. Optimizing the Ver@2 objective on 9×9 Maze with GRPO variants. We compare Trajectory-Level GRPO (TL-GRPO),
  Naive Attempt-Level GRPO (NAL-GRPO), and Calibrated Attempt-Level GRPO (CAL-GRPO). (a) CAL-GRPO attains the best Ver@2.
  (b) Improvements mainly come from higher attempt-1 success with competitive attempt-2 correction. (c) NAL/CAL reduce the average
  number of attempts compared to TL-GRPO.



   efficiency for TL-GRPO, NAL-GRPO, and CAL-GRPO, with the clearest gain for CAL-GRPO. Although our theoretical
   derivations are written in an RLOO-style form without this GRPO rescaling, this empirical result motivates our use of the
   standard GRPO normalization in all experiments.
   Ablation on group size. CAL-GRPO estimates its weights directly from the current rollout group. For Ver@2, the quantity
   is p̂2 = |S12 | n∈S 2 rn,2 , which is estimated from the trajectories in the current group that reach attempt 2, and the calibrated
                  P
   weights reduce to w1 = 1 − p̂2 and w2 = 1. Hence, the quality of the calibration depends on how well the current rollouts
   estimate second attempt success. Figures 13a and 13b compares rollout group sizes N = 10 and N = 16 on Maze under
   Ver@2. Using N = 16 improves sample efficiency for all three methods, with the clearest gain for CAL-GRPO early in
   training. Larger groups yield more trajectories that reach attempt 2, so both the per-attempt normalization and the estimate
   of p̂2 are based on a larger and therefore less noisy sample of current rollouts. This becomes increasingly relevant later in
   training, when attempt-1 success rises and the reached set S 2 shrinks. These results motivate our use of a moderately large
   rollout group size for CAL-GRPO throughout our experiments.

   C. Proofs Section 3
   Fix a problem instance (x, y) and suppress (x, y) in notation. Let τ denote a (random) multi-attempt rollout with stopping
   time T ∈ {1, . . . , K} and terminal Verification@K reward R := rT ∈ {0, 1}. For attempt i, let si−1 be the pre-attempt state and

                                                                                                                       18
                                                       Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                       1025                                                                       0.5       TL-GRPO                                                           1.3
                                                             attempt 1
Mean Response Length

                       1000                                  attempt 2                                      NAL-GRPO




                                                                             Attempt Reward Std
                                                                                                            CAL-GRPO                                                          1.2




                                                                                                                                                          Attempt Weights
                        975                                                                       0.4
                        950                                                                                                                                                   1.1
                                                                                                  0.3
                        925           TL-GRPO                                                                                                                                 1.0
                        900           NAL-GRPO                                                    0.2                                                                         0.9                                          attempt 1
                                      CAL-GRPO                                                                                                                                                                             attempt 2
                        875                                                                                                                                                   0.8
                                                                                                  0.1                                    attempt 1
                        850                                                                                                              attempt 2                            0.7
                              0    5     10 15 20 25 30 35 40                                           0   5   10      15    20   25   30   35      40                              0       5       10    15   20   25   30   35      40
                                             Training step                                                           Training step                                                                        Training step
  (a) Mean response length per attempt vs. (b) Attempt reward standard deviation (c) Attempt weights used by CAL-GRPO
  training step (baselines labeled in legend: within each GRPO group, shown separately (future-only reweighting), for attempts 1 and
  TL-GRPO, NAL-GRPO, CAL-GRPO).               for attempts 1 and 2.                    2 over training.
  Figure 8. Additional metrics for Ver@2 training on 9×9 Maze task. (a) Response length dynamics per attempt. (b) Per-attempt reward
  variation used during the per-attempt normalization. (c) Learned future-only attempt reweighting in CAL-GRPO.


                       0.8        TL-GRPO                                                         0.6       TL-GRPO                                                           4.00                                        TL-GRPO
                                  NAL-GRPO                                                                  NAL-GRPO                                                          3.75                                        NAL-GRPO
Validation Accuracy




                       0.7                                                                        0.5




                                                                                                                                                          Avg # of attempts
                                  CAL-GRPO                                                                  CAL-GRPO                                                                                                      CAL-GRPO
                                                                             Attempt Success




                       0.6                                                                                                                                                    3.50
                                                                                                  0.4       attempt 1                                                         3.25
                       0.5                                                                                  attempt 2
                       0.4                                                                        0.3       attempt 3                                                         3.00
                                                                                                            attempt 4                                                         2.75
                       0.3                                                                        0.2
                                                                                                                                                                              2.50
                       0.2                                                                        0.1                                                                         2.25
                       0.1
                                                                                                  0.0                                                                         2.00
                       0.0
                              0   5      10 15 20 25 30 35 40                                           0   5   10      15    20   25   30   35      40                                  0       5    10 15 20 25 30 35 40
                                            Training step                                                            Training step                                                                        Training step
  (a) Ver@4 validation accuracy on 9×9                                         (b) Attempt-wise success. Curves show suc- (c) Average attempts under Ver@4; NAL/-
  Maze across training; CAL-GRPO achieves                                      cess on attempt i conditioned on failing all CAL reduce the number of attempts relative
  the highest Ver@4, with NAL-GRPO im-                                         earlier attempts. NAL-GRPO boosts early- to TL-GRPO.
  proving over TL-GRPO.                                                        attempt success while CAL-GRPO improves
                                                                               later-attempt correction.
  Figure 9. Optimizing the Ver@4 objective on 9×9 Maze with GRPO variants. We compare Trajectory-Level GRPO (TL-GRPO),
  Naive Attempt-Level GRPO (NAL-GRPO), and Calibrated Attempt-Level GRPO (CAL-GRPO). (a) CAL-GRPO attains the best Ver@4.
  (b) Improvements reflect stronger attempt-wise performance, with CAL-GRPO emphasizing correction on later attempts. (c) NAL/CAL
  reduce the average number of attempts compared to TL-GRPO.

                       1025                                                                       0.5       TL-GRPO                                                           1.4
Mean Response Length




                       1000                                                                                 NAL-GRPO
                                                                             Attempt Reward Std




                                                                                                            CAL-GRPO
                                                                                                                                                          Attempt Weights




                        975                                                                       0.4                                                                         1.2
                                      TL-GRPO
                        950           NAL-GRPO                                                                                                                                                                             attempt 1
                                      CAL-GRPO                                                    0.3                                                                         1.0                                          attempt 2
                        925                                                                                                                                                                                                attempt 3
                        900                                                                       0.2                                                                                                                      attempt 4
                                                                                                                                                                              0.8
                        875           attempt 1                                                                                          attempt 1
                                      attempt 2                                                                                          attempt 2
                        850           attempt 3                                                   0.1                                    attempt 3                            0.6
                                      attempt 4                                                                                          attempt 4
                        825
                              0    5     10 15 20 25 30 35 40                                           0   5   10      15    20   25   30   35      40                              0       5       10    15   20   25   30   35      40
                                             Training step                                                           Training step                                                                        Training step
  (a) Mean response length per attempt vs. (b) Attempt reward standard deviation (c) Attempt weights used by CAL-GRPO
  training step (baselines labeled in legend: within each GRPO group, shown separately (future-only reweighting), for attempts 1–4
  TL-GRPO, NAL-GRPO, CAL-GRPO).               for attempts 1–4.                        over training.
  Figure 10. Additional metrics for Ver@4 training on 9×9 Maze task. (a) Response length dynamics per attempt. (b) Per-attempt
  reward variation used during the per-attempt normalization. (c) Learned future-only attempt reweighting in CAL-GRPO.


   yi ∼ πθ (· | si−1 ). Define the attempt-i score (for the whole attempt output) as

                                                                         gi := ∇θ log πθ (yi | si−1 ) · 1{T ≥ i},                                 i ∈ [K],

                                                                                                                         19
                                                       Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                       1.0                                                                             TL-GRPO                                                               4.0                                      TL-GRPO
                                                                                             0.8       NAL-GRPO                                                                                                       NAL-GRPO
Validation Accuracy

                                                                                                                                                                             3.5




                                                                                                                                                         Avg # of attempts
                       0.8                                                                             CAL-GRPO                                                                                                       CAL-GRPO




                                                                        Attempt Success
                                                                                             0.6       attempt 1                                                             3.0
                       0.6                                                                             attempt 2
                                                                                                       attempt 3                                                             2.5
                                                                                             0.4       attempt 4
                       0.4                                                                                                                                                   2.0
                                                             TL-GRPO                         0.2
                       0.2                                   NAL-GRPO                                                                                                        1.5
                                                             CAL-GRPO                        0.0
                              0   5      10 15 20 25 30 35 40                                      0   5     10      15    20    25    30   35      40                             0      5      10 15 20 25 30 35 40
                                            Training step                                                         Training step                                                                       Training step
  (a) Ver@4 validation accuracy on 7×7                                    (b) Attempt-wise success. Line styles (c) Average attempts under Ver@4; NAL/-
  Maze across training; CAL-GRPO achieves                                 denote attempts 1–4. Curves show suc- CAL reduce the number of attempts relative
  the highest Ver@4, with NAL-GRPO im-                                    cess on attempt i given all earlier attempts to TL-GRPO.
  proving over TL-GRPO.                                                   failed; NAL-GRPO boosts early success
                                                                          while CAL-GRPO improves correction.
  Figure 11. Optimizing the Ver@4 objective on 7×7 Maze with GRPO variants. We compare Trajectory-Level GRPO (TL-GRPO),
  Naive Attempt-Level GRPO (NAL-GRPO), and Calibrated Attempt-Level GRPO (CAL-GRPO). (a) CAL-GRPO attains the best Ver@4.
  (b) Improvements reflect stronger attempt-wise performance, with CAL-GRPO emphasizing correction on later attempts. (c) NAL/CAL
  reduce the average number of attempts compared to TL-GRPO.


                       1000                                                                  0.5       TL-GRPO                                                                            attempt 1
Mean Response Length




                                                                                                       NAL-GRPO                                                              2.5          attempt 2
                                                                        Attempt Reward Std




                                                                                                       CAL-GRPO                                                                           attempt 3




                                                                                                                                                         Attempt Weights
                        900                                                                  0.4                                                                                          attempt 4
                                      TL-GRPO                                                                                                                                2.0
                                      NAL-GRPO
                        800           CAL-GRPO                                               0.3                                                                             1.5
                        700           attempt 1                                              0.2                                        attempt 1                            1.0
                                      attempt 2                                                                                         attempt 2
                        600           attempt 3                                                                                         attempt 3                            0.5
                                      attempt 4                                              0.1                                        attempt 4
                              0   5      10 15 20 25 30 35 40                                      0   5     10      15    20    25    30   35      40                             0      5      10    15   20   25   30   35   40
                                             Training step                                                        Training step                                                                       Training step
  (a) Mean response length per attempt vs. (b) Attempt reward standard deviation (c) Attempt weights used by CAL-GRPO
  training step (baselines labeled in legend: within each GRPO group, shown separately (future-only reweighting), for attempts 1–4
  TL-GRPO, NAL-GRPO, CAL-GRPO).               for attempts 1–4.                        over training.
  Figure 12. Additional metrics for Ver@4 training on 7×7 Maze task. (a) Response length dynamics per attempt. (b) Per-attempt
  reward variation used during the per-attempt normalization. (c) Learned future-only attempt reweighting in CAL-GRPO.



   so gi ≡ 0 on trajectories that terminate before attempt i. Let Fi := σ(x, y1 , r1 , . . . , yi , ri ) be the trajectory filtration up to
   attempt i. Define the Doob conditional success probabilities

                                                                               Qi := E[R | Fi ] ,                               i = 0, 1, . . . , K.

   (Under a deterministic verifier, Qi = ri + (1 − ri )Vθ,i (si ) on {T ≥ i}, where Vθ,i (si ) = P(∃ t ∈ {i + 1, . . . , K} : rt = 1 | si ) and
   Vθ,K (·) = 0.)
   Now draw a group of N ≥ 2 i.i.d. trajectories τ1 , . . . , τN ∼ pθ (· | x). Write Rn and Qn,i for the corresponding terminal
   reward and Doob conditional success probability. Let Si := {n ∈ [N] : T (τn ) ≥ i} be the (random) set of trajectories that
   reach attempt i. For notational convenience, define Mi := |Si | and assume Mi ≥ 2 almost surely (or restrict to events where
   Mi ≥ 2).
   Theorem C.1 (Unbiasedness and strict Rao–Blackwell variance reduction at each attempt). Fix (x, y) and N ≥ 2. Define the
   trajectory-level (TL) and attempt-level (AL) RLOO estimators

                                                                                              K                                                          K
                                                       bTL
                                                                                              X Mi          biTL ,          bAL
                                                                                                                                                         X Mi                           biAL ,
                                                       G RLOO (θ; x, y) :=                                 ·Z               G RLOO (θ; x, y) :=                                        ·Z
                                                                                              i=1
                                                                                                  N                                                         i=1
                                                                                                                                                                N

                                                                                                                      20
                                                   Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

                      1.0                                                                 16                                                             1.0
                                 TL-GRPO                                                                    n=10      TL-GRPO                                      TL-GRPO
                                 NAL-GRPO                                                                   n=16      NAL-GRPO                                     NAL-GRPO




                                                                     Reaching Attempt 2
Validation Accuracy




                                                                                                                                   Validation Accuracy
                                                                     Mean # Responses
                      0.8        CAL-GRPO                                                 14                          CAL-GRPO                           0.8       CAL-GRPO
                                 n=10                                                                                                                              std
                      0.6        n=16                                                     12                                                             0.6       w/o std
                      0.4                                                                 10                                                             0.4
                      0.2                                                                 8                                                              0.2
                      0.0                                                                 6                                                              0.0
                             0       5        10         15     20                               5          10        15      20                               0      5        10         15   20
                                         Training step                                                Training step                                                       Training step
  (a) Ver@2 validation accuracy on Maze                               (b) Mean number of responses reaching                          (c) Standard deviation normalization ab-
  for rollout group sizes N=10 and N=16.                              attempt 2. Solid: N=16. Dashed: N=10.                          lation at N=16. Solid: with within-group
  Solid: N=16. Dashed: N=10. Larger                                   Larger groups retain more attempt-2 sam-                       standard deviation scaling. Dashed: without
  groups improve sample efficiency, especially                        ples in the current rollout group, improv-                     standard deviation scaling. Standard devi-
  for CAL-GRPO early in training.                                     ing the stability of per-attempt normaliza-                    ation normalization improves sample effi-
                                                                      tion and CAL-GRPO’s weight estimates.                          ciency for all three methods.
  Figure 13. Effect of rollout group size and standard deviation normalization on Ver@2 training for Maze. We compare GRPO
  group sizes N=10 and N=16 for TL-GRPO, NAL-GRPO, and CAL-GRPO, and also compare the standard GRPO normalization against a
  variant without standard deviation scaling. (a) Larger groups improve early Ver@2, with the most noticeable gain for CAL-GRPO. (b)
  Since CAL-GRPO estimates attempt-wise weights from the current rollout group, larger N provides more trajectories that reach attempt 2
  and therefore yields more accurate estimates of the conditional success rate of attempt 2. (c) Standard deviation normalization improves
  learning for all three estimators and is used in our experiments.


   where, for each attempt index i,

                                                          biTL := 1                                                          1
                                                                     X                                                            X
                                                          Z             ATL gn,i ,                    ATL
                                                                                                       n,i := Rn −                    Rm ,
                                                                  Mi n∈S n,i                                               Mi − 1 m∈S
                                                                                i                                                                  i
                                                                                                                                   m,n


                                                          biAL := 1                                                           1
                                                                     X                                                             X
                                                          Z             AAL gn,i ,                    AAL
                                                                                                       n,i := Qn,i −                   Qm,i .
                                                                  Mi n∈S n,i                                                Mi − 1 m∈S
                                                                                i                                                                         i
                                                                                                                                          m,n

  Then:

                      i Both estimators are unbiased for the Verification@K policy gradient:
                                                        h                i   h                i
                                                           RLOO (θ; x, y) = E G RLOO (θ; x, y) = ∇θ ρθ (x, y).
                                                      EG  bTL                  bAL                   VK



                 ii Let Gi := σ Fn,i : n ∈ [N] be the group filtration up to attempt i. Then, for every i ∈ [K],
                                              

                                               h        i                                                                           h               i
                                              EZ           biAL ,
                                                 biTL Gi = Z                              and hence          biTL ) = Var(Z
                                                                                                         Var(Z            biAL ) + E Var(Z
                                                                                                                                         biTL | Gi ) .

                                                           bAL ) for all i, and the inequality is strict for a given i whenever P Var(R1 | F1,i ) > 0 > 0
                                               bTL ) ≥ Var(Z
                            In particular, Var(Z
                                               i           i
                            and P ∥g1,i ∥2 > 0 > 0.

   Proof. Part (i) Fix i ∈ [K]. Because the trajectories are i.i.d. across n, and because leave-one-out centering preserves
   unbiasedness, it suffices to show that for a single trajectory

                                                                        E 1{T ≥ i} Qi gi = E 1{T ≥ i} R gi ,
                                                                                                       

   and that the sum over i equals ∇θ ρVK
                                      θ (x, y). The first equality is the tower property: since gi is Fi -measurable and
   Qi = E[R | Fi ],

                                     E 1{T ≥ i} R gi = E E 1{T ≥ i} R gi | Fi = E 1{T ≥ i} gi E[R | Fi ] = E 1{T ≥ i} Qi gi .
                                                                                                                  


                                                                                                       21
                            Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

Summing over i gives
                  K
                                           K 
                  X                        X 
                    E 1{T ≥ i} R gi = ER  gi  = E R ∇θ log pθ (τ | x) = ∇θ E[R] = ∇θ ρVK
                                                                         
                                                                                             θ (x, y),
                   i=1                            i=1

where we used ∇θ log pθ (τ | x) = i=1 gi (verifier independent of θ) and the log-derivative identity. Finally, since the
                                      PK
group estimator averages N i.i.d. copies and uses leave-one-out baselines (which are conditionally independent of each
centered trajectory), the expectation is unchanged, proving (i). ep Part (ii) Fix i ∈ [K] and consider the group sigma-field
Gi = σ(Fn,i : n ∈ [N]). Note that Si and Mi are Gi -measurable (reachability is determined by (rn,1 , . . . , rn,i−1 )), and gn,i is
Fn,i -measurable, hence also Gi -measurable. Moreover, for each n,
                                               E[Rn | Gi ] = E[Rn | Fn,i ] = Qn,i ,
because Rn depends only on trajectory n and trajectories are independent across n. Therefore, conditioning ZbTL on Gi
                                                                                                             i
replaces each Rn in the leave-one-out advantage by Qn,i while leaving all other terms fixed:
                                                                                           
                                                                                         
                            h       i    1  X                         1    X
                           E Zi | Gi =                                       E[Rm | Gi ] gn,i = Z
                                                                                                     biAL .
                               TL
                                                 
                                                                                           
                              b                    E[Rn | Gi ] −
                                        Mi     n∈Si
                                                                  Mi − 1            m∈Si
                                                                                               
                                                                                      m,n


Applying the law of total variance yields
                                                      h               i                h               i
                     Var(ZbiTL ) = Var E[Z
                                         biTL | Gi ] + E Var(Z
                                                             biTL | Gi ) = Var(Z
                                                                               biAL ) + E Var(Z
                                                                                              biTL | Gi ) ,

proving the non-strict inequality. Moreover, E[Var(Z  bTL | Gi )] > 0 whenever, with positive probability, there exists residual
                                                       i
randomness in R after conditioning on Fi and the attempt-i score is nonzero. A sufficient (and minimal) condition is:
P(Var(R1 | F1,i ) > 0) > 0 and P(∥g1,i ∥2 > 0) > 0. This implies strict inequality for that ii.                               □

D. Proofs for Section 5
Theorem D.1 (CAL is unbiased under attempt-index independence; per-attempt Rao–Blackwell variance reduction). Fix
(x, y) and suppress (x, y) in notation. Assume Assumption 5.1 holds. Let ρθ (x, y) := E[R] denote the Verification@K success
probability.
Draw N ≥ 2 i.i.d. trajectories τ1 , . . . , τN ∼ pθ (· | x) and define Si := {n ∈ [N] : T (τn ) ≥ i} and Mi := |Si |, assuming Mi ≥ 2
a.s. For each n ∈ Si , define the leave-one-out estimate of the attempt-i success probability
                                                        1     X
                                           ρn,i :=               rm,i ,      n,i := rn,i − ρn,i .
                                                                           ACAL
                                                    Mi − 1 m∈S
                                                                    i
                                                              m,n

Define the CAL future-failure weight
                                                              K
                                                              Y
                                              wCAL                      1 − ρn, j ,
                                                                                 
                                               n,i :=                                     i ∈ [K],                              (12)
                                                              j=i+1

(where for j > i we interpret ρn, j as the leave-one-out average over S j excluding n if n ∈ S j and otherwise as the full
average over S j ; this makes ρn, j well-defined for all n and j and agrees with the above definition when n ∈ S j ). Define the
per-attempt CAL term
                                                     1 X CAL CAL
                                         ZiCAL :=           w     An,i gn,i ,   i ∈ [K],
                                                    Mi n∈S n,i
                                                                i

and the CAL group estimator (in the same scaling as the TL/AL definitions)
                                                        K                             K
                                                        X Mi                      1 X X CAL CAL
                                bCAL (θ; x, y) :=
                                G                                   ZiCAL =                w    An,i gn,i .                     (13)
                                  RLOO
                                                        i=1
                                                               N                  N i=1 n∈S n,i
                                                                                             i


Then:
                                                  h               i
                                                 EG bCAL (θ; x, y) = ∇θ ρθ (x, y).                                              (14)
                                                     RLOO


                                                                          22
                              Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

Proof. Unbiasedness: Let Gi := σ(F1,i , . . . , FN,i ) be the group filtration.
                                                                K
Assumption 5.1 implies that there exist policies π(i)  θ (· | x) i=1 such that pθ (yi | s1:i−1 ) = πθ (yi | x). Hence, conditional on x,
                                                                                                    (i)

the attempt outputs y1 , . . . , yK are independent across i, and so are the correctness indicators (ri )i=1 K
                                                                                                                .
Define the attempt-i success probability (conditional on reaching attempt i)

                                                       ρi := P(ri = 1 | T ≥ i).

Under Assumption 5.1, ρi depends only on (x, i, θ) and not on the content of the prior history.
Let
                                                                                          K
                                                                                          Y
                                ui := P(ri+1 = 0, . . . , rK = 0 | T ≥ i) =                    (1 − ρ j ),         i ∈ [K],
                                                                                          j=i+1

(with uK := 1 by the empty-product convention). Then, on {T ≥ i}, the Doob conditional success probability satisfies

                                        Qi = E[R | Fi ] = 1 − ui (1 − ri ) = (1 − ui ) + ui ri .                                    (15)

We claim that for each n ∈ [N] and i ∈ [K],
                                                  h         i       K
                                                                    Y
                                                 E wn,i | Gi = ui =
                                                    CAL
                                                                      (1 − ρ j ).                                                   (16)
                                                                                       j=i+1


                                 j=t (1 − ρn, j ) for t ∈ {i + 1, . . . , K}, so that wn,i = Wn,i+1 . We prove by backward induction that
                              QK                                                       CAL
To see this, define Wn,t :=
                                                                  K
                                                                  Y
                                        E[Wn,t | Gt−1 ] =           (1 − ρ j ),            t = i + 1, . . . , K.
                                                                  j=t

For the base case t = K, conditional on GK−1 the set SK is fixed and, for each m ∈ SK , rm,K is an i.i.d. Bernoulli(ρK ) draw
independent of GK−1 . Thus ρn,K is an average of i.i.d. Bernoulli(ρK ) variables (with or without leaving out n), and therefore
E[ρn,K | GK−1 ] = ρK , i.e. E[1 − ρn,K | GK−1 ] = 1 − ρK , which is exactly the desired identity at t = K.
For the induction step, assume the identity holds at t + 1: E[Wn,t+1 | Gt ] = Kj=t+1 (1 − ρ j ). Then, by the tower property,
                                                                               Q

                                         E[Wn,t | Gt−1 ] = E E (1 − ρn,t )Wn,t+1 | Gt Gt−1
                                                                                         

                                                         = E (1 − ρn,t ) E[Wn,t+1 | Gt ] Gt−1
                                                                                             

                                                                   K
                                                                  Y                
                                                         =                (1 − ρ j ) · E[1 − ρn,t | Gt−1 ].
                                                                  j=t+1

The same argument as in the base case yields E[ρn,t | Gt−1 ] = ρt (because the attempt-t outcomes among St are conditionally
i.i.d. Bernoulli(ρt ) given Gt−1 ), so E[1 − ρn,t | Gt−1 ] = 1 − ρt and therefore
                                                                                 K
                                                                                 Y
                                                     E[Wn,t | Gt−1 ] =                 (1 − ρ j ).
                                                                                 j=t

Setting t = i + 1 gives (16).
Using (15), the AL leave-one-out advantage at attempt i can be rewritten as
                                         1     X                      1    X       
                        AAL
                         n,i := Qn,i −             Qm,i = ui rn,i −             rm,i = ui ACAL
                                                                                           n,i ,
                                       Mi − 1 m∈S                    Mi − 1 m∈S
                                                          i                                             i
                                                      m,n                                             m,n

since the constant term (1 − ui ) cancels in the leave-one-out difference. Consequently,
                                                  1 X AL                 1 X CAL
                                       ZiAL =           An,i gn,i = ui ·       A gn,i .                                             (17)
                                                 Mi n∈S                  Mi n∈S n,i
                                                              i                                   i



                                                                            23
                          Calibrated Reinforcement Learning for Multi-Attempt Chain-of-Thought

On the other hand, ACAL
                    n,i gn,i is Gi -measurable, so by (16),

                                                                                            
                                                             1
                                                                X                          
                                       E[ZiCAL | Gi ] = E          wCAL  CAL
                                                                        n,i An,i gn,i Gi 
                                                                                         
                                                            Mi n∈S                         
                                                                   i

                                                         1 X CAL
                                                      =           A gn,i · E[wCAL
                                                                              n,i | Gi ]
                                                        Mi n∈S n,i
                                                                i

                                                             1 X CAL
                                                      = ui ·         A gn,i = ZiAL ,                                   (18)
                                                             Mi n∈S n,i
                                                                       i


where the last equality uses (17). Taking expectations in (18) yields

                                              E[ZiCAL ] = E[ZiAL ],              ∀i ∈ [K].                             (19)

From (13) and (19),

                                         i X K   M        X K   M      
                                                    i CAL            i AL
                         h                                                  h                i
                        EG bCAL (θ; x, y) =     E    Zi    =     E    Zi = E G RLOO (θ; x, y) .
                                                                              bAL
                            RLOO
                                            i=1
                                                  N          i=1
                                                                   N

                                                            bAL ] = ∇θ E[R] = ∇θ ρθ (x, y): indeed,
Finally, the standard policy-gradient/Doob argument gives E[G RLOO
                                                                   K         K
                                                                   X  X
                                     ∇θ ρθ (x, y) = ∇θ E[R] = ER  gi  =   E[Qi gi ],
                                                                           i=1        i=1

and the leave-one-out baseline used to form ZiAL does not change the expectation because its multiplier has conditional mean
zero. This proves (14).                                                                                                    □




                                                                  24
