                                                                                                                                      CUHKSZ & SJTU
                                                                                                                                           January 9, 2026




                                                  Milestones over Outcome: Unlocking Geometric
                                                    Reasoning with Sub-Goal Verifiable Reward

                                                 Jianlong Chen1 , Daocheng Fu3 , Shengze Xu4 , Jiawei Chen5 , Yuan Feng2 ,
                                                         Yue Yang2 , Junchi Yan2 , Hongyuan Zha1 , Renqiu Xia2, B
                                            1
                                                The Chinese University of Hong Kong, Shenzhen 2 Shanghai Jiao Tong University
                                                          3
                                                            Fudan University 4 The Chinese University of Hong Kong
arXiv:2601.05073v1 [cs.LG] 8 Jan 2026




                                                                5
                                                                  University of Science and Technology Beijing
                                                                                                                   B
                                                   {jianlongchen}@link.cuhk.edu.cn, {xiarenqiu}@sjtu.edu.cn            Corresponding Authors




                                            Multimodal Large Language Models (MLLMs) struggle with complex geometric reasoning, largely
                                            because "black box" outcome-based supervision fails to distinguish between lucky guesses and
                                            rigorous deduction. To address this, we introduce a paradigm shift towards subgoal-level evaluation
                                            and learning. We first construct GeoGoal, a benchmark synthesized via a rigorous formal verification
                                            data engine, which converts abstract proofs into verifiable numeric subgoals. This structure reveals
                                            a critical divergence between reasoning quality and outcome accuracy. Leveraging this, we propose
                                            the Sub-Goal Verifiable Reward (SGVR) framework, which replaces sparse signals with dense
                                            rewards based on the Skeleton Rate. Experiments demonstrate that SGVR not only enhances
                                            geometric performance (+9.7%) but also exhibits strong generalization, transferring gains to general
                                            math (+8.0%) and other general reasoning tasks (+2.8%), demonstrating broad applicability across
                                            diverse domains.


                                                 code: https://github.com/FrontierX-Lab/SGVR.




                                        1 Introduction

                                        Multimodal Large Language Models (MLLMs) have demonstrated impressive proficiency in diverse vision-
                                        language tasks Achiam et al. (2023); Team et al. (2023); Bai et al. (2025). However, their efficacy diminishes
                                        in domains requiring rigorous multi-step reasoning. Geometric reasoning stands as a formidable frontier,
                                        necessitating the coherent integration of visual perception, symbolic abstraction, and logical deduction Trinh
                                        et al. (2024); He et al. (2024). While specialized neuro-symbolic solvers Trinh et al. (2024); Sicca et al. (2024)
                                        have reached Olympiad-level performance, general-purpose MLLMs continue to struggle with long-horizon
                                        inference, often plagued by hallucinations and logical gaps in natural language.
                                        Standard evaluation benchmarks Chen et al. (2021); Lu et al. (2021) treat reasoning as a black box, assessing
                                        only the final numerical result. This coarse objective creates a misalignment between metric and capability:
                                        it yields false positives via spurious correlations and false negatives via minor arithmetic slips. Crucially,
                                        sparse final-answer signals fail to provide the fine-grained feedback necessary for models to learn robust


                                                                                                1
                                                                                             CUHKSZ & SJTU
                                                                                                  January 9, 2026




Figure 1: Our main goal: Decomposing the "black box" of complex geometric reasoning into a verifiable
chain of fine-grained intermediate milestones.

intermediate deductive steps. More fundamentally, outcome accuracy is not a faithful proxy for step-wise
reasoning reliability: models can sometimes recover the correct final answer despite flawed intermediate
steps, while otherwise valid reasoning can be penalized by small downstream errors. Our solution is to break
open this black box by focusing on the reasoning milestones. As illustrated in Figure 1, we reframe the entire
process as a sequence of verifiable sub-goals. This structure offers a unified solution for both evaluation and
learning: it allows for a granular evaluation of the reasoning path, pinpointing exactly where logic fails, while
simultaneously providing the dense, trustworthy signals required for effective training.
In this work, we introduce a paradigm shift towards subgoal-level evaluation and reinforcement learning,
as depicted in Figure 2. First, we create the GeoGoal benchmark, synthesized via the TrustGeoGen data
engine Fu et al. (2025). Our "proofing-to-solving" transformation convert abstract logical predicates into a
sequence of executable, verifiable numeric sub-goals. This structures the reasoning process into a series
of clear milestones, moving beyond unstructured text generation. Critically, our evaluation using GeoGoal
reveals that reasoning quality and outcome accuracy can diverge, which motivates the need for more granular,
subgoal-level supervision. To address this gap, we then leverage GeoGoal to propose the Sub-Goal Verifiable
Reward (SGVR) framework. This method facilitates Reinforcement Learning with Verifiable Rewards (RLVR)
by replacing sparse outcome rewards with dense, subgoal-oriented signals. Specifically, we use Group
Relative Policy Optimization (GRPO) DeepSeek-AI (2025) to maximize the Skeleton Rate, the ratio of
successfully verified sub-goals. The results show that our proposed SGVR improves both final-answer
performance and intermediate reasoning quality, with gains transferring beyond geometry by achieving
average improvements of +9.7% on geometric reasoning, +8.0% on general mathematics, and +2.8% on
general reasoning tasks.

Our contributions are summarized as follows:
  1. Verifiable Benchmark Construction: We present the first multimodal geometry benchmark GeoGoal
     where intermediate sub-goals are formally verified and automatically checkable, introducing Skeleton
     Rate (SR), Skeleton Completion (SC) and Consistency Ratio (CR) as rigorous metrics for reasoning
     fidelity.
  2. SGVR Framework: We propose a reinforcement learning framework leveraging verifiable numeric
     sub-goals as critical reasoning milestones to provide dense supervision.
  3. Empirical Efficacy: Experiments show that our proposed SGVR framework improves final answer
     accuracy with robust cross-domain transfer to general reasoning tasks and enhances intermediate
     reasoning quality.



                                                       2
                                                                                                                                                                                                                                                                                           CUHKSZ & SJTU
                                                                                                                                                                                                                                                                                                       January 9, 2026



                                                   (1) Formal Skeleton Generation                                                        (2) Decomposition and Sub-goal Mapping                                                             (3) Reorganization and Construction


      Subgaol-aware verifiable reasoning
                                                                               Given square ABCD with side
                                                                                                                                                                                                        prove: ∠DCE = ∠EDC                                             P




                                                                                                                     sub-goal 2 sub-goal 1
                                                                               length AB = 1. Let E be the                                                                        P                                                                                                         P
                                                                               circumcenter of triangle
                                                                                                                                                           P                              P                                                                 P                  P
                                                                               CDA. ∠EAF=2∠EAB. Let G                                                                                                  solve: ∠DCE - ∠EDC =?                                                                       P
                                                                               be the midpoint of segment
                                                                               DE, and let H be any point on                                                                  S                              sub-goal answer: 0                                      S √
                                                                               the circle with center G and                                                                                                                                                                S       √
                                                                                                                                                                                                                                                                                           S √
                                                                               radius GF. Find the length of
                 benchmark

                                                                               CG.                                                                                                                     prove: D E G collinear                                              √
                                                                                                                                                                S                     S                                                                                S           S
                                                                                                                                                                                                                                                                                       ×
                                                                premises from problem                                                                                                                          solve: ∠EGD=?
                                                                                                                                                                              S                                                                                                ×
                                                                                                                                                                                                            sub-goal answer: 180




                                                                                                                                                                                                                                        Subgoal-Aware
                                              Formal Skeleton



                                                                           P                   P
                                                                   P               P                                                                                          ……                                  ……                                        SR Score = 4/(4+2) = 0.67




                                                                                                                                                                                                                                           Metrics
                                                                                                   P




                                                                                                                     sub-goal n
                                                                       S       S           S
                                                                                                                                                                                                        prove: CG = 34/43                                   SC Score = 1x1x1x1x0x0 = 0
                                                                                                                                                           S                      S
                                                                           S           S                                                                                                                        solve: CG=?
                                                                                                                                                                              C                                                                             Final Answer Score = 0
                                                                               C                                                                                                                       sub-goal answer: 34/43



                                                                                                                                                                                  sub-goal 1                       sub-goal 2      ……       sub-goal n                                     P :     premise
      Training with dense sub-goal




                                                                                                                                                               GT                         0                             2          ……                   2                                  S :     state
                                                                                                   Encoder
                                                                                                    Vision




                                                                                                                                                           Pred                           —                            —                                2√                                 C :     conclusion

                                                                                                                                                                                                                                                                                       P
                                                                                                                                             GRPO                                                                                                                                                 state is derived

                                                                                                                                                               X n roll out
                                                                                                                                                                                  t1          t2       t3         t4   t5     t6   …… tn-2 tn-1                 tn             P            P
                                                                                                                                                                                                                                                                                                : from premises
                 reward




                                                                                                                                                                                                                                                                                                  based on rule
                                                                                                               LLM




                                                                                                                                                                                                                                                                                       S
                                                                                                                                                                                  t1          t2       t3         t4   t5     t6   …… tn-2 tn-1                 tn
                                                                                                                                                                                                                                                                                                token predicted
                                           Points A,B,C satisfy AB= AC= BC=4.
                                           Let D be the incenter of ∆ ABC, Let                                                                                                                                                                                                         t : without process-
                                                                                                                                                           Pred                               0√                        1×                              2√                                      aware reward
                                                                                                                                             SGVR (ours)
                                                                                                   Tokenizer




                                           E,… please answer the following                                                                                                                                                                                                                      token predicted
                                           questions:
                                                                                                     Text




                                                                                                                                                                                                                                                                                                with process-
                                                                                                                                                                                                                                                                                       t   :
                                                                                                                                                               X n roll out




                                           [sub-goal 1]: ∠BAE- ∠ABE ?                                                                                                             t1          t2       t3         t4   t5     t6   ……      tn-2 tn-1            tn                              aware reward
                                           [sub-goal 2]: BE:DE ?                                                                                                                                                                                                                                (incorrect)
                                           ……                                                                                                                                                                                                                                                   token predicted
                                           [sub-goal n]: |CF|?                                                                                                                    t1          t2       t3         t4   t5     t6   ……      tn-2 tn-1            tn                     t :      with process-
                                                                                                                                                                                                                                                                                                aware reward
                                                                                                                                                                                                                                                                                                (correct)




Figure 2: Overall framework: (Top) Benchmark construction: Formally verified skeletons from Trust-
GeoGen Fu et al. (2025) are decomposed into numeric sub-goals to enable subgoal-level metrics. (Bottom)
SGVR training: The model generates structured traces; predicted sub-goals are verified against ground truth
to formulate dense rewards for policy optimization via GRPO.

2 GeoGoal: A Verifiable Benchmark for Sub-Goal Reasoning

Standard geometry benchmarks, which evaluate only final answers, cannot distinguish between genuine
reasoning and heuristic shortcuts. This paradigm also precludes subgoal-level evaluation signals, which are
essential for training models that reason robustly. To overcome these limitations, we construct a benchmark
designed for milestones verifiability, where each reasoning step has a verifiable ground truth, and fine-grained
subgoal assessment.


2.1         Construction Pipeline

Our pipeline, illustrated in Figure 2, transforms formal proofs into a benchmark with verifiable sub-goals,
enabling dense reward signals for downstream RL. The overall procedure is organized as:


Step 1: Data Engine: Formal Skeleton Generation We leverage TrustGeoGen (Fu et al., 2025) to
synthesize complete formal problem instances. For each sample, the engine outputs the geometric premise
together with a formally verified solution skeleton {St }Tt=1 . A built-in verifier enforces type constraints,
dependency ordering, and derivability of every predicate, ensuring the logical correctness of the reasoning
chain.


Step 2: Decomposition and Sub-goal Mapping To enable step-wise verification, we first decompose
the formal solution skeleton {St } into atomic reasoning steps. Since formal predicates are abstract and
not directly solvable by standard LLMs, we map each decomposed predicate into a numeric sub-goal via a


                                                                                                                                                                                                   3
                                                                                                 CUHKSZ & SJTU
                                                                                                      January 9, 2026



mapping function1 . For example, a congruence predicate cong(A,B,C,D) is mapped to a length ratio task
(Tt : |AB|/|CD|, yt : 1). This conversion turns abstract reasoning steps into automatically checkable numeric
targets.


Step 3: Reorganization and Sequence Construction Finally, we reorganize these sub-goals into a
sequential format to construct the final benchmark instances. Crucially, the sequence is ordered such that
the last sub-goal Tni corresponds to the original problem’s final goal, while preceding sub-goals represent
intermediate reasoning steps derived from the formal proof. The model is presented with the initial problem
and premises, and is required to find the values for the entire sequence of sub-goals. This structure allows
us to verify the model’s reasoning process step-by-step, rather than just checking the final answer.


2.2    Sub-goal Evaluation Metrics

To capture performance at different granularities, we consider three complementary metrics. Skeleton Rate
(SR) measures average step-wise correctness across sub-goals, Skeleton Completion (SC) measures end-to-
end consistency over complete reasoning chains, and the Consistency Ratio (CR) quantifies the normalized
alignment between the two at the dataset level, i.e., how much subgoal-wise correctness translates into
fully consistent solutions. CR is computed   Pnas   the ratio of the dataset-level SC to the dataset-level SR. For
instance i with ni sub-goals, let pi = n1i t=1  i
                                                   I(ŷi,t = yi,t ) denote the fraction of correctly solved sub-goals,
          Qni
and ci = t=1   I(ŷi,t = yi,t ) indicate whether all sub-goals are correct. By construction, ci ≤ pi for all i, hence
SC ≤ SR.                                              N      ni
                                                     1 X 1 X
                                             SR =                 I(ŷi,t = yi,t ),
                                                     N i=1 ni t=1
                                                           N    ni
                                                    1 XY
                                             SC =                 I(ŷi,t = yi,t ),                                (1)
                                                    N i=1 t=1
                                                    ( SC
                                                         dataset
                                                      SR
                                                                 , if SRdataset > 0,
                                             CR =          dataset
                                                      0,                 otherwise.

Intuitively, CR can be viewed as an IoU-like consistency ratio, measuring the fraction of step-wise correctness
that also forms fully correct chains; larger values indicating stronger reasoning stability and less error
propagation along reasoning chains.


2.3    Dataset Characteristics

We construct balanced Train and Test splits of 256 instances each. The test set is intentionally skewed
toward longer reasoning chains to probe generalization beyond the training distribution. Each instance
contributes multiple verifiable sub-goals, yielding dense signals for both evaluation and RL training. For
detailed proof-length distributions and geometric concept coverage, please refer to Appendix C.


2.4    Benchmark Evaluation of Existing Models

Beyond serving as training data, our benchmark also enables subgoal-level evaluation of existing multimodal
models. We evaluate some widely deployed models spanning both proprietary and open-weight systems us-
ing SR and SC, and also report the standard outcome metric of Final Answer accuracy (FA), i.e., correctness
of the last sub-goal (the original final goal). This analysis provides subgoal baselines and directly tests the
central premise highlighted in the introduction: final-answer accuracy alone is not a faithful proxy for the rigor
and integrity of intermediate deductions..
  1 The complete mapping rules can be found in Tables 5,   6, 7, 8 and 9



                                                                     4
                                                                                               CUHKSZ & SJTU
                                                                                                  January 9, 2026



Table 1: Performance of ten multimodal models on our benchmark. All metrics are reported in %. Gem-
ini 2.5 Pro leads in performance, while skeleton-based metrics reveal differences between per-step correct-
ness (SR), end-to-end consistency (SC), consistency ratio (CR), and outcome-based accuracy (FA). The
best and second-best performances were highlighted using bold and underline, respectively.

                   Model                                     SR ↑ SC ↑ CR ↑             FA ↑
                   Closed-source models
                   Gemini 2.5 Pro Comanici et al. (2025)     88.7 44.5 50.2             82.8
                   o4-mini OpenAI (2025c)                    88.3 37.1 42.0             84.0
                   GPT-5-mini OpenAI (2025b)                 86.4 29.7 34.4             78.5
                   GPT-4o OpenAI (2024b)                     47.9 4.7   9.8             36.3
                   Open-source models
                   Qwen2.5-VL-32B-Instruct Bai et al. (2025) 63.3 3.9   6.2             52.3
                   Qwen2.5-VL-7B-Instruct Bai et al. (2025)  50.5 2.3   4.6             43.4
                   Qwen3-VL-8B-Instruct Team (2025)          48.3 17.2 35.6             37.5
                   Qwen3-VL-30B-A3B-Instruct Team (2025) 46.9 18.8 40.1                 36.7
                   Qwen3-VL-8B-Thinking Team (2025)          44.8 31.6 70.5             42.6
                   Llama-4-Scout AI (2025)                   12.4 0.8   6.5             10.6


Sub-goal baselines. Table 1 reports SR, SC, CR, and FA accuracy, establishing reference points for
step-wise correctness (SR), end-to-end consistency (SC), consistency ratio (CR), and outcome accuracy
(FA). Across models, SC is consistently lower than SR and typically lower than FA, reflecting the strictness of
requiring all intermediate sub-goals to be correct.


How aligned are outcome accuracy and step-wise consistency? We compare SC against Final Answer
accuracy for all models (Figure 3). The relationship is only moderately aligned (Kendall τ = 0.511): multiple
models achieve relatively high Final Answer accuracy despite substantially lower SC. This divergence implies
that outcome-only evaluation can overestimate reasoning reliability, since correct final answers may be
produced even when intermediate sub-goals contain errors.


What failure modes are exposed by the relationship between SR and SC? We further analyze the joint
distribution of SR and SC by plotting models in a two-dimensional space with SR and SC as axes, color-
coding each point by its Consistency Ratio (CR) (Figure 4). While stronger models tend to cluster toward
high SR and high SC, CR still varies substantially, revealing different failure modes. In particular, models
with high SR but low SC exhibit low CR: they solve many individual sub-goals correctly yet fail to maintain
end-to-end consistency, suggesting error propagation along long reasoning chains. By contrast, models
with larger CR are more stable, as step-wise correctness is more consistently reflected in complete-chain
success. Together, SR and SC offer complementary diagnostic signals that cannot be inferred from FA alone,
motivating their use in both evaluation and dense reward training.



3 Sub-Goal Verifiable Reward

Given the step-wise verifiable benchmark in Section 2, we introduce Sub-Goal Verifiable Reward (SGVR), a
training strategy that exploits automatically checkable sub-goals to produce dense feedback. As illustrated in
the training part of Figure 2, the model generates a structured response in which each slot corresponds to a
specific sub-goal; every predicted sub-goal is then verified against ground truth, and the resulting verification
signals are aggregated into rewards.




                                                       5
                                                                                                                       CUHKSZ & SJTU
                                                                                                                           January 9, 2026



                                             50%
                                                     Kendall τ = 0.511
                                                                                                          GEMINI




                                                               FA
                                             40%




                                                             =
                                                          SC
                  Skeleton Completion (SC)
                                                                                                          O4-MINI

                                                                     QWEN3-VL-8B-THINKING
                                             30%                                                  GPT-5-MINI




                                             20%               QWEN3-VL-30B-A3B-INSTRUCT
                                                               QWEN3-VL-8B-INSTRUCT



                                             10%

                                                             GPT4O           QWEN2.5-VL-32B-INSTRUCT
                                                                     QWEN2.5-VL-7B-INSTRUCT
                                             0%
                                                   30%      40%          50%         60%           70%         80%   90%
                                                                         Final Answer Accuracy

Figure 3: Skeleton Completion (SC) versus Final Answer accuracy on our benchmark. Each point denotes a
multimodal model. The light blue background indicates SC < FA. The closer the model is to the line where
SC = FA, the more rigorous its reasoning logic is.


3.1    RL Formulation

We frame multi-step reasoning as a contextual bandit problem where the generation process is decomposed
into a sequence of verifiable sub-goals. Given a problem x, the policy πθ generates a structured response y,
which we partition into segments corresponding to individual sub-goals.


Sub-goal Reward Signal. A key innovation of SGVR is the construction of a dense reward signal from
verifiable intermediate reasoning steps. Unlike outcome-based rewards that only evaluate the final answer,
or learned reward models that may hallucinate, our reward is derived from the strict verification of each
sub-goal in the reasoning chain.

For each sub-goal t in a reasoning trajectory with n sub-goals, we define an intermediate verification:
                                                                      rt = I(verify(ŷt , yt ))                                         (2)
where ŷt is the predicted value for the t-th sub-goal, yt is the ground truth, and I(verify(ŷt , yt )) indicates
whether the prediction matches the verifiable ground truth.

The reward for a complete trajectory is computed as the normalized accumulation of these intermediate
signals, which is mathematically equivalent to the instance-level Skeleton Rate (SR) metric defined in
Section 2.2:                                         n                                i
                                                                                1 X
                                                               R(y) = SRi =            I(ŷi,t = yi,t )                                 (3)
                                                                                ni t=1
This formulation is intrinsically subgoal-level: rather than a single binary outcome, the reward emerges from
the accumulation of verification signals throughout the reasoning chain. A trajectory that correctly solves
80% of the sub-goals receives a significantly higher reward than one that solves only 20%, even if both fail
the final answer. This dense, gradient-like signal provides step-by-step supervision that guides the model to
incrementally improve its reasoning process.


                                                                                 6
                                                                                                                                                   CUHKSZ & SJTU
                                                                                                                                                      January 9, 2026



                                                50%

                                                                                                    GEMINI               0.7

                                                40%
                                                                                                                         0.6
                                                                                                    O4-MINI




                     Skeleton Completion (SC)
                                                                            QWEN3-VL-8B-THINKING
                                                                                                                         0.5




                                                                                                                               Consistency Ratio
                                                30%                                            GPT-5-MINI
                                                                                                                         0.4


                                                                                                                         0.3
                                                20%
                                                                              QWEN3-VL-30B-A3B-INSTRUCT
                                                                               QWEN3-VL-8B-INSTRUCT
                                                                                                                         0.2


                                                10%                                                                      0.1

                                                                    GPT4O
                                                                                          QWEN2.5-VL-32B-INSTRUCT
                                                                                                                         0.0
                                                                                  QWEN2.5-VL-7B-INSTRUCT
                                                0%
                                                      20%    30%    40%     50%     60%       70%   80%       90% 100%
                                                                            Skeleton Rate (SR)

Figure 4: Skeleton Completion (SC) v.s. Skeleton Rate (SR) on our benchmark. Points are color-coded
by the Consistency Ratio (CR), revealing distinct trade-offs between step-wise correctness and end-to-end
consistency.


3.2   Group Relative Policy Optimization

To efficiently optimize the policy using this subgoal-level reward, we employ Group Relative Policy Optimiza-
tion (GRPO) (DeepSeek-AI, 2025). GRPO eliminates the need for a separate value function critic, which is
often computationally expensive and unstable to train, by leveraging the group-based relative advantage.
For each question q, we sample a group of G outputs {o1 , o2 , . . . , oG } from the old policy πθold . For each
output oi , we compute the reward ri using our verifiable subgoal reward function. The advantage Ai for each
output is then computed by normalizing the rewards within the group:
                                                                              ri − mean({r1 , . . . , rG })
                                                                      Ai =                                                                                         (4)
                                                                                std({r1 , . . . , rG }) + ϵ

where ϵ is a small constant for numerical stability.

The GRPO objective function is defined as:

                                                                        πθ (oi | q)
                                                            
                                                                 ρi =
                                                                        θold (oi | q)
                                                            
                                                            
                                                            
                                                            
                                                                      π
                                                            
                                                                                                            
                                                             L̂i (θ) = min ρi Ai , clip(ρi , 1 − ϵ, 1 + ϵ) Ai                                                      (5)
                                                                            "               #
                                                                                   G
                                                            
                                                            
                                                                              1 X
                                                             L(θ) = Eq, o G          L̂i (θ) − β DKL (πθ ∥ πref )
                                                            
                                                            
                                                            
                                                                                  i=1


where DKL is the KL divergence regularization term to prevent the policy from deviating too far from the
reference model πref . In our experiments we primarily adopt GRPO for its simplicity and stability, but the
same SGVR reward can also be optimized with standard PPO Schulman et al. (2017), as explored in the
ablation studies (Section 4.3).



                                                                                          7
                                                                                                                                                                                                                           CUHKSZ & SJTU
                                                                                                                                                                                                                                       January 9, 2026



                                                                                          Geometry Reasoning                                                                                    General Math                  General Reasoning

                100
                                           87.7
                                          (+37.5) 83.1
                                                                                                                  82.1
                                                 (+49.0)                                                          (+6.4)
                                                                                                                           75.6
                 80                                                                                                        (+7.2)
 Accuracy (%)




                                                                                                                                                                                                         63.2
                                                                             58.2                                                   59.4    57.8                                                         (+4.0)   59.0
                                                                             (+2.9)                                                 (+2.4) (+0.4)                                                                 (+2.0)
                 60
                                                                                      50.1
                                                                                      (+5.5)
                                                                                                40.3                                                                                     38.6
                                                                                                (+3.4)
                                                                                                                                                                                        (+12.1) 34.9
                 40                                                                                                                                                   32.1                      (+6.0)
                                                                                                         29.8                                                         (+4.4)                                                               28.5
                                                                                                         (+5.3)                                                                                                                                    27.3
                                                                                                                                                    25.4                       24.1                                                        (+2.1) (+2.4)
                                                                                                                                                    (+5.0)   20.8              (+0.9)                                      20.0    19.5
                                                            17.4    16.4                                                                                     (+4.5)                                                        (+3.5) (+7.0)
                         15.2
                 20              13.7
                        (+12.9) (+12.9)
                                                           (+12.8) (+14.1)




                  0
                         GeoGoal           GeoGoal          GeoGoal           GeoQA            Geometry3K         GeoPQA            GeoPQA          TrustGeo          Olympiad             AMC            MATH             LiveBench       VisuLogic
                           SC                SR               CR                                                    Test             Valid            Test             Bench                               500             Reasoning
                                                                                      Qwen2.5-VL-7B-Instruct (Baseline)                             Qwen2.5-VL-3B-Instruct (Baseline)
                                                                                      Qwen2.5-VL-7B-Instruct (Improvement)                          Qwen2.5-VL-3B-Instruct (Improvement)



Figure 5: Performance comparison of our trained models against baselines on final answer accuracy.
Solid bars represent baseline performance; patterned sections indicate improvements from our training.
Our method achieves consistent gains across model sizes and task domains, with particularly strong
improvements on some datasets (GeoPQA-Test: +6.4% for 7B, +7.2% for 3B; AMC: +12.1% for 7B, +6.0%
for 3B; LiveBench-Reasoning: +3.5% for 7B, +7.0% for 3B).


4 Experiments

4.1                   Experimental Setup

Training Setup. We train Qwen2.5-VL-7B-Instruct and Qwen2.5-VL-3B-Instruct Bai et al. (2025) using our
proposed SGVR algorithm on the training split of GeoGoal benchmark. This training set consists of 256
plane geometry problems, each with step-wise intermediate sub-goals and final answers to enabling precise
subgoal supervision and training details are provided in Appendix E.


Evaluation Benchmarks. To assess distributional robustness and cross-domain generalization, we eval-
uate our models on benchmarks across three categories: 1) Geometric Reasoning: We evaluate plane
geometry problem-solving capabilities using GeoGoal, GeoQA(Chen et al., 2025), Geometry3K(Lu et al.,
2021), GeoPQA(Chen et al., 2025), TrustGeo-Test(Fu et al., 2025), and OlympiadBench-Geo (He et al.,
2024). These datasets provide a diverse testbed for multimodal geometric reasoning across varying distri-
butions. 2) General Mathematics: We employ AMC2 and MATH-500 (Lightman et al., 2023) to examine
whether subgoal-level supervision transfers from geometry to broader mathematical problem-solving. 3)
General Reasoning: We use LiveBench-Reasoning(White et al., 2024) and VisuLogic(Xu et al., 2025b) to
probe reasoning capabilities in wider logical and visual contexts.


Evaluation Metric. We report Final Answer Accuracy as the primary metric across all benchmarks to
assess end-to-end reasoning performance. Numerical equivalence is verified using LLM as a deterministic
checker for mathematical expressions (more details are provided in Appendix F). For our GeoGoal benchmark,
we additionally employ SC, SR and CR to explicitly evaluate the correctness of intermediate sub-goals.
For external benchmarks lacking ground-truth sub-goals, we adopt the established Process Evaluation
Score Zhang et al. (2025b) via an LLM-as-a-Judge approach to assess the quality of intermediate reasoning
steps.
          2 https://huggingface.co/datasets/AI-MO/aimo-validation-amc




                                                                                                                                    8
                                                                                        CUHKSZ & SJTU
                                                                                             January 9, 2026



Table 2: Process evaluation scores Zhang et al. (2025b) across all benchmarks. Models trained with our
method consistently improve the quality of reasoning process over the pretrained baselines across both
model sizes.

                                           Qwen2.5-VL-7B                Qwen2.5-VL-3B
             Benchmark
                                      Baseline    Ours      ∆      Baseline    Ours      ∆
             GeoGoal                     15.7      23.7   +8.0       13.0      26.9    +13.9
             GeoQA                       49.0      50.8   +1.8       40.4      42.6    +2.2
             Geometry3K                  50.5      52.0   +1.5       41.3      43.9    +2.6
             GeoPQA-Test                 47.2      63.6   +16.4      23.3      46.1    +22.8
             GeoPQA-Valid                28.9      35.9   +7.0       29.1      35.1    +6.0
             TrustGeo-Test               23.9      26.1   +2.2       17.8      20.2    +2.4
             OlympiadBench               36.7      39.9   +3.2       29.2      30.7    +1.5
             AMC                         38.0      40.3   +2.3       35.8      40.2    +4.4
             MATH 500                    66.8      69.0   +2.2       65.6      66.5    +0.9
             LiveBench-Reasoning         20.3      22.0   +1.7       17.4      20.5    +3.1
             VisuLogic                   34.7      35.3   +0.6       31.1      31.1    +0.0


4.2   Main Results

We structure our analysis around three key research questions to assess the impact of verifiable sub-goal
supervision on geometric performance, cross-domain generalization, and reasoning quality.

RQ1: Does rewarding verifiable sub-goals improve geometric reasoning?
Figure 5 presents a comprehensive evaluation across geometry benchmarks, demonstrating that our
SGVR framework consistently enhances performance compared to pretrained baselines. On our GeoGoal
benchmark, we observe substantial improvements across all subgoal-level metrics: the 7B model improves
from 50.2% to 87.7% in Skeleton Rate (SR), from 2.3% to 15.2% in Skeleton Completion (SC), and from
4.6% to 17.4% in Consistency Ratio (CR); the 3B model shows even more dramatic gains, improving from
34.1% to 83.1% in SR, from 0.8% to 13.7% in SC, and from 2.3% to 16.4% in CR. These improvements
validate that our verifiable sub-goal supervision effectively guides models toward more reliable reasoning
chains. On external geometry benchmarks, the 7B model achieves an average accuracy gain of 4.0%,
with notable improvements on GeoPQA-Test (+6.4%) and TrustGeo-Test (+5.0%). The 3B model mirrors
this trend with GeoPQA-Test (+7.2%) and Geometry3K (+5.3%). These results demonstrate that verifiable
sub-goal supervision facilitates robust generalization within the geometric domain.

RQ2: Do geometric sub-goal priors generalize to non-geometric domains?

A critical question is whether the reasoning capabilities learned from geometry are specific to that domain
or transferable to broader contexts. Despite being trained exclusively on geometry-focused data without
exposure to general math or logic samples, our models exhibit remarkable plasticity and cross-domain
generalization. In general mathematics, the models demonstrate significant performance boosts, with the
7B model improving by 12.1% on the AMC benchmark and 4.0% on MATH-500, while the 3B model shows
respective gains of 6.0% and 2.0%. This indicates that the verification mechanism learned from geometric
sub-goals effectively supports broader symbolic mathematical reasoning. Moreover, these benefits extend
to general reasoning tasks, as evidenced by the 7B and 3B models achieving gains of 3.5% and 7.0%
respectively on LiveBench-Reasoning, alongside consistent improvements on the visual logic benchmark
VisuLogic. This suggests that the rigorous verification of geometric sub-goals cultivates a fundamental
reasoning capability that naturally transfers to enhance logical consistency across diverse domains.




                                                    9
                                                                                          CUHKSZ & SJTU
                                                                                                 January 9, 2026



Table 3: Ablation study of RL optimizers (Baseline, PPO, GRPO) on Qwen2.5-VL-7B-Instruct and Qwen2.5-
VL-3B-Instruct across benchmarks. Both algorithms use Skeleton Rate as the reward signal. Best results
within each model size are in bold, second-best are underlined.

                                               Qwen2.5-VL-7B               Qwen2.5-VL-3B
             Benchmark
                                           Baseline   PPO    GRPO     Baseline   PPO     GRPO
             Geometry Reasoning
             GeoGoal (SC)                     2.3     10.6    15.2      0.8       11.7    13.7
             GeoGoal (SR)                    50.2     80.8    87.7      34.1      84.0    83.1
             GeoGoal (CR)                     4.6     13.1    17.4      2.3       13.9    16.4
             GeoQA                           55.3     56.2    58.2      44.6      50.1    50.1
             Geometry3K                      36.9     39.1    40.3      24.5      29.8    29.8
             GeoPQA-Test                     75.7     78.8    82.1      68.4      78.6    75.6
             GeoPQA-Valid                    57.0     64.6    59.4      57.4      60.3    57.8
             TrustGeo-Test                   20.4     21.7    25.4      16.3      20.4    20.8
             OlympiadBench                   27.7     29.5    32.1      23.2      25.9    24.1
             Geometry Average                36.7     43.8    46.4      30.2      41.6    41.3
             General Mathematics
             AMC                             26.5     33.7    38.6      28.9      34.9    34.9
             MATH 500                        59.2     62.6    63.2      57.0      59.2    59.0
             General Math Average            42.9     48.2    50.9      43.0      47.1    47.0
             General Reasoning
             LiveBench-Reasoning             16.5     21.0    20.0      12.5      20.5    19.5
             VisuLogic                       26.4     28.6    28.5      24.9      25.9    27.3
             General Reasoning Average       21.5     24.8    24.3      18.7      23.2    23.4
             Overall Average                 33.7     39.0    40.5      30.6      37.3    37.2


RQ3: Does sub-goal alignment improve the quality of the reasoning chain?

To assess reasoning fidelity beyond final outcomes, we evaluate the logical coherence of generated paths
using the established Process Evaluation Score Zhang et al. (2025b). Table 2 reveals a universal improve-
ment in process scores across nearly all evaluated benchmarks for both model sizes, indicating a broad
enhancement in reasoning quality. On GeoGoal, process scores improve from 15.7% to 23.7% (+8.0%) for
the 7B model and from 13.0% to 26.9% (+13.9%) for the 3B model, demonstrating that sub-goal alignment
significantly enhances the quality of intermediate reasoning steps. On external benchmarks, the GeoPQA-
Test process score increases by 16.4% for the 7B model and by an impressive 22.8% for the 3B model.
These findings provide compelling evidence that SGVR encourages the generation of more reliable and
coherent intermediate trajectories.


4.3   Ablation Studies

To identify the optimal configuration for our SGVR framework, we conduct ablation studies focusing on two
critical design choices: the choice of reinforcement learning optimizer and the granularity of the verifiable
reward signal.

RQ4: Is the performance gain sensitive to the choice of RL optimizer?
To evaluate the impact of different optimization strategies within our framework, we compare Group Rel-
ative Policy Optimization (GRPO) (DeepSeek-AI, 2025) against standard Proximal Policy Optimization



                                                      10
                                                                                                CUHKSZ & SJTU
                                                                                                       January 9, 2026



Table 4: Ablation study of reward formulations (Final Answer, Skeleton Completion, Skeleton Rate) on
Qwen2.5-VL-7B-Instruct and Qwen2.5-VL-3B-Instruct across benchmarks in different domains.

                                                 Qwen2.5-VL-7B                  Qwen2.5-VL-3B
             Benchmark
                                           FA         SC       SR         FA         SC       SR
                                         Reward     Reward   Reward     Reward     Reward   Reward
             Geometry Reasoning
             GeoGoal (SC)                  5.9        9.4        15.2     5.9        9.4        13.7
             GeoGoal (SR)                 79.1       82.1        87.7    79.1       67.5        83.1
             GeoGoal (CR)                  7.4       11.4        17.4     7.4       13.9        16.4
             GeoQA                        54.4       53.9        58.2    48.0       48.3        50.1
             Geometry3K                   36.7       36.8        40.3    27.0       26.0        29.8
             GeoPQA-Test                  77.9       77.5        82.1    72.2       74.2        75.6
             GeoPQA-Valid                 42.6       40.8        59.4    57.6       57.4        57.8
             TrustGeo-Test                20.8       19.6        25.4    20.0       13.8        20.8
             OlympiadBench                27.7       24.1        32.1    21.4       21.4        24.1
             Geometry Average             39.2       39.5        46.4    37.6       36.9        41.3
             General Mathematics
             AMC                          31.3       33.7        38.6    31.3       28.9        34.9
             MATH 500                     61.2       65.6        63.2    56.6       54.6        59.0
             General Math Average         46.3       49.7        50.9    44.0       41.8        47.0
             General Reasoning
             LiveBench-Reasoning          17.5       25.0        20.0    17.5       13.5        19.5
             VisuLogic                    25.6       26.5        28.5    25.1       25.0        27.3
             General Reasoning Average    21.6       25.8        24.3    21.3       19.3        23.4
             Overall Average              35.7       38.3        40.5    34.3       32.7        37.2



(PPO) (Schulman et al., 2017), both utilizing identical Skeleton Rate rewards. Our analysis of Table 3 yields
three key observations regarding optimizer efficacy:
(1) Both optimizers consistently improve over the pretrained baseline. Across almost all benchmarks and
both model scales, models trained with PPO and GRPO outperform the baseline. For the 7B model, PPO
and GRPO achieve averages of 39.0% and 40.5% respectively among all benchmark, compared to the
baseline average of 33.7%. For the 3B model, they reach 37.3% and 37.2% versus 30.6%. This indicates
that SGVR framework is effective and robust under different optimization schemes.
(2) GRPO and PPO exhibit complementary strengths for the 7B model. GRPO achieves the best overall
performance of 40.5%, demonstrating stronger results on mathematical and geometric tasks. For instance, it
leads in the Geometry Average with 46.4% versus 43.8% for PPO, and in the General Math Average with
50.9% versus 48.2%. Conversely, PPO performs better on general reasoning tasks, achieving an average of
24.8% compared to 24.3% for GRPO.

RQ5: Which reward formulation maximizes reasoning performance?
To determine the optimal supervision signal, we compare three reward formulations defined in Section 2.2:
1) Skeleton Rate which provides dense sub-goal rewards, 2) Skeleton Completion which enforces strict
sub-goal reward, and 3) Final Answer which relies on sparse outcome signals. Our analysis on Table 4
leads to three key observations:
(1) Skeleton Rate offers the most robust and effective supervision. SR consistently achieves the highest
overall average performance, reaching 40.5% (7B) and 37.2% (3B). On GeoGoal, SR demonstrates superior
reasoning integrity, boosting SC scores to 15.2% (7B) and 13.7% (3B), and CR scores to 17.4% (7B) and
16.4% (3B). This superiority extends beyond geometry, with SR also achieving the highest averages in
general mathematics and competitive results in general reasoning.


                                                       11
                                                                                                             CUHKSZ & SJTU
                                                                                                                               January 9, 2026



                                                          Geometry3K          MATH 500       LiveBench
                                                          TrustGeo Test       AMC            Average
                                                                                                             64.0
          Accuracy (%) - Other Benchmarks   40
                                                                                                             63.5




                                                                                                                    Accuracy (%) - MATH-500
                                            35                                                               63.0


                                                                                                             62.5
                                            30

                                                                                                             62.0
                                            25
                                                                                                             61.5


                                            20                                                               61.0


                                                                                                             60.5
                                                   0%           30%          50%       70%           100%
                                                 (Ours)                                               (FA)
                                                                          Mask Ratio
Figure 6: Performance comparison across different sub-goal mask ratios trained on Qwen2.5-VL-7B-Instruct.


(2) Sparse Final Answer rewards are insufficiently informative for complex reasoning. Outcome-based
supervision fails to foster consistent reasoning chains. On the GeoGoal benchmark, models trained with FA
rewards show a sharp disconnect between subgoal-wise correctness and full-chain validity: despite achieving
high SR scores (e.g., 79.1% for 7B), their SC and CR metrics collapse to just 5.9% and 7.4%, respectively.
This pattern holds across domains, where FA training consistently results in the lowest average performance
for both model sizes, trailing SR by significant margins in geometry (−7.2%), general mathematics (−4.6%)
and general reasoning (-2.7%) for the 7B model.
We therefore adopt Skeleton Rate (SR) as our default reward formulation, as its dense reward offers the
most stable and effective signal for fostering robust reasoning capabilities.

RQ6: Is denser sub-goal supervision always better?
To investigate whether more subgoals always lead to better performance, we conduct an ablation study
by randomly masking a proportion of subgoals during training while maintaining the Skeleton Rate reward
formulation. We train models with 0%, 30%, 50%, 70%, and 100% (Final Answer only) of subgoals masked.
Figure 6 presents the results across five benchmarks, revealing two key observations:
(1) Denser supervision generally improves performance. The 0% mask ratio achieves the highest accuracy
on most benchmarks, with the overall average accuracy decreasing consistently from 37.01% (0%) to 33.49%
(100%). This indicates that additional sub-goals provide valuable supervision signals for learning robust
reasoning strategies.
(2) Optimal sub-goal density for generalization is task-specific. Our results show that while in-domain
geometric tasks demand fine-grained steps to maintain logical rigor, out-of-domain generalization can
sometimes favor sparser signals. For instance, on LiveBench-Reasoning, the 30% configuration achieves
the highest accuracy. This suggests that transferring to broader domains may benefit from focusing on key
milestones rather than pursuing the densest possible in-domain signals.


                                                                              12
                                                                                          CUHKSZ & SJTU
                                                                                              January 9, 2026



5 Conclusion

In this work, we introduce a paradigm shift from outcome-based to subgoal-level supervision. We construct
GeoGoal via a formal verification engine to provide verifiable numeric sub-goals and propose the SGVR
framework to leverage these as dense reward signals. Our approach significantly enhances in-domain
geometric reasoning while demonstrating strong transferability to general mathematics and broader reasoning
tasks. Crucially, our findings suggest that developing post-training methods within in-domain formal engines
capable of providing trustworthy dense signals offers a promising avenue for unlocking robust out-of-
distribution generalization capabilities.



6 Limitations and Future Work

Our benchmark is derived from a specific formal data engine and a mapping into numeric sub-goals,
which may not capture the full diversity of human-written geometric arguments or non-numeric intermediate
reasoning. Moreover, verification relies on deterministic equivalence checking for numeric answers; extending
verification to richer symbolic and diagram-grounded statements remains an open challenge.
Future work includes adopting more general-purpose formal systems (e.g., Lean4) Moura & Ullrich (2021) to
extend beyond geometry into broader mathematical domains, and transferring the SGVR decomposition-
and-verification paradigm to other reasoning tasks where intermediate sub-goals can be designed to be
automatically checkable.




                                                     13
                                                                                        CUHKSZ & SJTU
                                                                                             January 9, 2026



References

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo
  Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint
  arXiv:2303.08774, 2023.

Meta AI. The llama 4 herd: The beginning of a new era of natively multimodal ai innovation. https:
 //ai.meta.com/blog/llama-4-multimodal-intelligence/, 2025.
Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie
 Wang, Jun Tang, et al. Qwen2. 5-vl technical report. arXiv preprint arXiv:2502.13923, 2025.

Jie Cao and Jing Xiao. An augmented benchmark dataset for geometric question answering through dual
  parallel text encoding. In Proceedings of the 29th International Conference on Computational Linguistics,
  pp. 1511–1520, 2022.
Guizhen Chen, Weiwen Xu, Hao Zhang, Hou Pong Chan, Deli Zhao, Anh Tuan Luu, and Yu Rong. Geopqa:
 Bridging the visual perception gap in mllms for geometric reasoning. ArXiv, abs/2509.17437, 2025a. URL
 https://arxiv. org/abs/2509.17437, 2025.
Jiaqi Chen, Jianheng Tang, Jinghui Qin, Xiaodan Liang, Lingbo Liu, Eric Xing, and Liang Lin. Geoqa: A
  geometric question answering benchmark towards multimodal numerical reasoning. In Findings of the
  Association for Computational Linguistics: ACL-IJCNLP 2021, pp. 513–523, 2021.
Jiaqi Chen, Tong Li, Jinghui Qin, Pan Lu, Liang Lin, Chongyu Chen, and Xiaodan Liang. Unigeo: Unifying
  geometry logical reasoning via reformulating mathematical expression. In Proceedings of the 2022
  Conference on Empirical Methods in Natural Language Processing, pp. 3313–3323, 2022a.
Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W Cohen. Program of thoughts prompting: Disen-
 tangling computation from reasoning for numerical reasoning tasks. arXiv preprint arXiv:2211.12588,
 2022b.

Yuri Chervonyi, Trieu H. Trinh, Miroslav Olšák, Xiaomeng Yang, Hoang Nguyen, Marcelo Menegali, Junehyuk
  Jung, Vikas Verma, Quoc V. Le, and Thang Luong. Gold-medalist performance in solving olympiad
  geometry with alphageometry2. ArXiv, 2502.03544, 2025.
Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon,
 Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with ad-
 vanced reasoning, multimodality, long context, and next generation agentic capabilities. arXiv preprint
 arXiv:2507.06261, 2025.
DeepMind. Gemini-2.5-pro. https://deepmind.google/technologies/gemini/pro/, 2025.
DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv
 preprint arXiv:2501.12948, 2025.
Yuan Feng, Yue Yang, Xiaohan He, Jiatong Zhao, Jianlong Chen, Zijun Chen, Daocheng Fu, Qi Liu,
  Renqiu Xia, Bo Zhang, and Junchi Yan. Geobench: Rethinking multimodal geometric problem-solving via
  hierarchical evaluation. arXiv preprint arXiv:2512.24119, 2025.
Chaoyou Fu, Peixian Chen, Yunhang Shen, Yulei Qin, Mengdan Zhang, Xu Lin, Jinrui Yang, Xiawu Zheng,
 Ke Li, Xing Sun, et al. Mme: A comprehensive evaluation benchmark for multimodal large language
 models. arXiv preprint arXiv:2306.13394, 2023.
Daocheng Fu, Jianlong Chen, Renqiu Xia, Zijun Chen, Qi Liu, Yuan Feng, Hongbin Zhou, Renrui Zhang,
 Shiyang Feng, Peng Gao, Hongyuan Zha, Junchi Yan, Botian Shi, Yu Qiao, and Bo Zhang. Trust-
 geogen: Formal-verified data engine for trustworthy multi-modal geometric problem solving. arXiv preprint
 arXiv:2504.15780, 2025.


                                                    14
                                                                                       CUHKSZ & SJTU
                                                                                            January 9, 2026



Jiahui Gao, Renjie Pi, Jipeng Zhang, Jiacheng Ye, Wanjun Zhong, Yufei Wang, Lanqing Hong, Jianhua Han,
   Hang Xu, Zhenguo Li, et al. G-llava: Solving geometric problem with multi-modal large language model.
   In The Thirteenth International Conference on Learning Representations, 2025.
Leo Gao, John Schulman, and Jacob Hilton. Scaling laws for reward model overoptimization. In International
  Conference on Machine Learning, pp. 10835–10866. PMLR, 2023a.

Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and Graham
  Neubig. Pal: Program-aided language models. In International Conference on Machine Learning, pp.
  10764–10799. PMLR, 2023b.
Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Anil Palepu, Petar Sirkovic, Artiom Myaskovsky,
  Felix Weissenberger, Keran Rong, Ryutaro Tanno, et al. Towards an ai co-scientist. arXiv preprint
  arXiv:2502.18864, 2025.
Suriya Gunasekar, Yi Zhang, Jyoti Aneja, Caio César Teodoro Mendes, Allie Del Giorno, Sivakanth Gopi,
  Mojan Javaheripi, Piero Kauffmann, Gustavo de Rosa, Olli Saarikivi, et al. Textbooks are all you need.
  arXiv preprint arXiv:2306.11644, 2023.

Yihan Hao, Mingliang Zhang, Fei Yin, and Lin-Lin Huang. Pgdp5k: A diagram parsing dataset for plane
  geometry problems. In 2022 26th International Conference on Pattern Recognition (ICPR), pp. 1763–1769.
  IEEE, 2022.
Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu, Zhen Leng Thai, Junhao Shen, Jinyi Hu, Xu Han,
 Yujie Huang, Yuxiang Zhang, et al. Olympiadbench: A challenging benchmark for promoting agi with
 olympiad-level bilingual multimodal scientific problems. arXiv preprint arXiv:2402.14008, 2024.
Jian Hu, Xibin Wu, Wei Shen, Jason Klein Liu, Zilin Zhu, Weixun Wang, Songlin Jiang, Haoran Wang, Hao
  Chen, Bin Chen, Weikai Fang, Xianyu, Yu Cao, Haotian Xu, and Yiming Liu. Openrlhf: An easy-to-use,
  scalable and high-performance rlhf framework. arXiv preprint arXiv:2405.11143, 2025.
Dongzhi Jiang, Renrui Zhang, Ziyu Guo, Yanwei Li, Yu Qi, Xinyan Chen, Liuhui Wang, Jianhan Jin, Claire
 Guo, Shen Yan, et al. Mme-cot: Benchmarking chain-of-thought in large multimodal models for reasoning
 quality, robustness, and efficiency. arXiv preprint arXiv:2502.09621, 2025.
Mehran Kazemi, Hamidreza Alvari, Ankit Anand, Jialin Wu, Xi Chen, and Radu Soricut. Geomverse: A
 systematic evaluation of large models for geometric reasoning. arXiv preprint arXiv:2312.12241, 2023.
Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training
  with frozen image encoders and large language models. In International conference on machine learning,
  pp. 19730–19742. PMLR, 2023a.
Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, and Ji-Rong Wen. Evaluating object
  hallucination in large vision-language models. arXiv preprint arXiv:2305.10355, 2023b.

Yuanzhi Li, Sébastien Bubeck, Ronen Eldan, Allie Del Giorno, Suriya Gunasekar, and Yin Tat Lee. Textbooks
  are all you need ii: phi-1.5 technical report. arXiv preprint arXiv:2309.05463, 2023c.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike,
 John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth International
 Conference on Learning Representations, 2023.

Fuxiao Liu, Tianrui Guan, Zongxia Li, Lichang Chen, Yaser Yacoob, Dinesh Manocha, and Tianyi Zhou.
  Hallusionbench: You see what you think? or you think what you see? an image-context reasoning
  benchmark challenging for gpt-4v (ision), llava-1.5, and other multi-modality models. arXiv preprint
  arXiv:2310.14566, 2(3):12, 2023.
Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. Advances in neural
 information processing systems, 36, 2024.


                                                   15
                                                                                        CUHKSZ & SJTU
                                                                                             January 9, 2026



Pan Lu, Ran Gong, Shibiao Jiang, Liang Qiu, Siyuan Huang, Xiaodan Liang, and Song-Chun Zhu. Inter-gps:
  Interpretable geometry problem solving with formal language and symbolic reasoning. arXiv preprint
  arXiv:2105.04165, 2021.
Pan Lu, Hritik Bansal, Tony Xia, Jiacheng Liu, Chunyuan Li, Hannaneh Hajishirzi, Hao Cheng, Kai-Wei
  Chang, Michel Galley, and Jianfeng Gao. Mathvista: Evaluating mathematical reasoning of foundation
  models in visual contexts. In The Twelfth International Conference on Learning Representations, 2024.
Fanqing Meng, Lingxiao Du, Zongkai Liu, Zhixiang Zhou, Quanfeng Lu, Daocheng Fu, Tiancheng Han,
  Botian Shi, Wenhai Wang, Junjun He, Kaipeng Zhang, Ping Luo, Yu Qiao, Qiaosheng Zhang, and Wenqi
  Shao. Mm-eureka: Exploring the frontiers of multimodal reasoning with rule-based reinforcement learning.
  arXiv preprint arXiv:2503.07365, 2025.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In
  Automated Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual Event,
  July 12–15, 2021, Proceedings 28, pp. 625–635. Springer, 2021.
OpenAI. Openai-o1. https://openai.com/o1, 2024a.
OpenAI. Gpt-4o system card, 2024b. URL https://arxiv.org/abs/2410.21276.
OpenAI. Openai-o3. https://openai.com/index/introducing-o3-and-o4-mini, 2025a.
OpenAI. Gpt-5 system card. https://cdn.openai.com/gpt-5-system-card.pdf, 2025b.
OpenAI. Openai o3 and o4-mini system card. https://openai.com/index/introducing-o3-and-o4-mini/,
 2025c.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with
  human feedback. Advances in neural information processing systems, 35:27730–27744, 2022.
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization
  algorithms. arXiv preprint arXiv:1707.06347, 2017.
Zhenwei Shao, Zhou Yu, Meng Wang, and Jun Yu. Prompting large language models with answer heuristics
  for knowledge-based visual question answering. In Proceedings of the IEEE/CVF Conference on computer
  vision and pattern recognition, pp. 14974–14983, 2023.
Vladmir Sicca, Tianxiang Xia, Mathïs Fédérico, Philip John Gorinski, Simon Frieder, and Shangling Jui.
  Newclid: A user-friendly replacement for alphageometry. arXiv preprint arXiv:2411.11938, 2024.
Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut,
 Johan Schalkwyk, Andrew M Dai, Anja Hauth, et al. Gemini: a family of highly capable multimodal models.
 arXiv preprint arXiv:2312.11805, 2023.
InternLM Team. Internlm: A multilingual language model with progressively enhanced capabilities, 2023.
NovelSeek Team, Bo Zhang, Shiyang Feng, Xiangchao Yan, Jiakang Yuan, Zhiyin Yu, Xiaohan He, Songtao
  Huang, Shaowei Hou, Zheng Nie, et al. Novelseek: When agent becomes the scientist–building closed-loop
  system from hypothesis to verification. arXiv preprint arXiv:2505.16938, 2025.
Qwen Team. Qwen3-vl. https://github.com/QwenLM/Qwen3-VL, 2025.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix,
 Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation
 language models. arXiv preprint arXiv:2302.13971, 2023a.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov,
  Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat
  models. arXiv preprint arXiv:2307.09288, 2023b.


                                                    16
                                                                                          CUHKSZ & SJTU
                                                                                              January 9, 2026



Trieu Trinh, Yuhuai Wu, Quoc Le, He He, and Thang Luong. Solving olympiad geometry without human
   demonstrations. Nature, 625(7995):476–482, 2024.
Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell,
  Geoffrey Irving, and Irina Higgins. Solving math word problems with process-and outcome-based feedback.
  arXiv preprint arXiv:2211.14275, 2022.

Xiaofeng Wang, Yiming Wang, Wenhong Zhu, and Rui Wang. Do large language models truly understand
  geometric structures? In International Conference on Learning Representations (ICLR), 2025.
Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid Shwartz-Ziv,
 Neel Jain, Khalid Saifullah, Sreemanti Dey, et al. Livebench: A challenging, contamination-limited llm
 benchmark. arXiv preprint arXiv:2406.19314, 2024.

Zhiyu Wu, Xiaokang Chen, Zizheng Pan, Xingchao Liu, Wen Liu, Damai Dai, Huazuo Gao, Yiyang Ma,
  Chengyue Wu, Bing-Li Wang, Zhenda Xie, Yu Wu, Kai Hu, Jiawei Wang, Yaofeng Sun, Yukun Li, Yishi
  Piao, Kang Guan, Aixin Liu, Xin Xie, Yu mei You, Kaihong Dong, Xingkai Yu, Haowei Zhang, Liang Zhao,
  Yisong Wang, and Chong Ruan. Deepseek-vl2: Mixture-of-experts vision-language models for advanced
  multimodal understanding. arXiv preprint arXiv:2412.10302, 2024.

Renqiu Xia, Bo Zhang, Haoyang Peng, Ning Liao, Peng Ye, Botian Shi, Junchi Yan, and Yu Qiao. Structchart:
  Perception, structuring, reasoning for visual chart understanding. arXiv preprint arXiv:2309.11268, 2023.
Renqiu Xia, Song Mao, Xiangchao Yan, Hongbin Zhou, Bo Zhang, Haoyang Peng, Jiahao Pi, Daocheng
 Fu, Wenjie Wu, Hancheng Ye, et al. Docgenome: An open large-scale scientific document benchmark for
 training and testing multi-modal large language models. arXiv preprint arXiv:2406.11633, 2024.
Renqiu Xia, Mingsheng Li, Hancheng Ye, Wenjie Wu, Hongbin Zhou, Jiakang Yuan, Tianshuo Peng, Xinyu
 Cai, Xiangchao Yan, Bin Wang, Conghui He, Botian Shi, Tao Chen, Junchi Yan, and Bo Zhang. Geox:
 Geometric problem solving through unified formalized vision-language pre-training. In The Thirteenth
 International Conference on Learning Representations, 2025.

Liangyu Xu, Yingxiu Zhao, Jingyun Wang, Yingyao Wang, Bu Pi, Chen Wang, Mingliang Zhang, Jihao
  Gu, Xiang Li, Xiaoyong Zhu, Jun chao Song, and Bo Zheng. Geosense: Evaluating identification and
  application of geometric principles in multimodal reasoning. arXiv preprint arXiv:2504.12597, 2025a.
Weiye Xu, Jiahao Wang, Weiyun Wang, Zhe Chen, Wengang Zhou, Aijun Yang, Lewei Lu, Houqiang Li,
 Xiaohua Wang, Xizhou Zhu, et al. Visulogic: A benchmark for evaluating visual reasoning in multi-modal
 large language models. arXiv preprint arXiv:2504.15279, 2025b.
Ming-Liang Zhang, Fei Yin, and Cheng-Lin Liu. A multi-modal neural geometric solver with textual clauses
  parsed from diagram. arXiv preprint arXiv:2302.11097, 2023a.
Renrui Zhang, Xinyu Wei, Dongzhi Jiang, Yichi Zhang, Ziyu Guo, Chengzhuo Tong, Jiaming Liu, Aojun
 Zhou, Bin Wei, Shanghang Zhang, et al. Mavis: Mathematical visual instruction tuning. arXiv preprint
 arXiv:2407.08739, 2024.
Zhongyue Zhang, Zijie Qiu, Yingcheng Wu, Shuya Li, Dingyan Wang, Zhuomin Zhou, Duo An, Yuhan Chen,
  Yu Li, Yongbo Wang, et al. Origene: A self-evolving virtual disease biologist automating therapeutic target
  discovery. bioRxiv, pp. 2025–06, 2025a.
Zhuosheng Zhang, Aston Zhang, Mu Li, Hai Zhao, George Karypis, and Alex Smola. Multimodal chain-of-
  thought reasoning in language models. arXiv preprint arXiv:2302.00923, 2023b.
Ziyin Zhang, Jiahao Xu, Zhiwei He, Tian Liang, Qiuzhi Liu, Yansi Li, Linfeng Song, Zhenwen Liang, Zhuosheng
  Zhang, Rui Wang, et al. Deeptheorem: Advancing llm reasoning for theorem proving through natural
  language and reinforcement learning. arXiv preprint arXiv:2505.23754, 2025b.




                                                     17
                                                                                         CUHKSZ & SJTU
                                                                                             January 9, 2026



A Ethical Considerations

The GeoGoal benchmark is synthesized using the formal verification engine, TrustGeoGen Fu et al. (2025),
which generates problems and reasoning paths based on rigorous axiomatic systems rather than crawling
private or copyrighted web content. Furthermore, we utilize established open-source datasets (e.g., MATH,
LiveBench) Lightman et al. (2023); White et al. (2024) in strict accordance with their original licensing
terms. All data used in this study is intended for academic research and contains no personally identifiable
information (PII) or harmful content.



B Related Work

B.1    Multimodal LLMs and Visual Mathematical Reasoning

Large language models (LLMs) have achieved remarkable progress in linguistic intelligence across a wide
spectrum of tasks (Ouyang et al., 2022; Touvron et al., 2023a;b; Team, 2023). Building on this foundation,
multimodal large language models (MLLMs) incorporate visual processing capabilities via modality-alignment
modules, such as Q-Former (Li et al., 2023a) and lightweight projection layers (Liu et al., 2024). These
architectures have demonstrated strong performance on general vision-language benchmarks (Fu et al.,
2023; Xia et al., 2024; 2023; Lu et al., 2024; Jiang et al., 2025).

However, a critical "visual-reasoning gap" persists despite these perceptual gains. Recent studies indicate
that MLLMs frequently suffer from object hallucination (Li et al., 2023b) and struggle to maintain logical
consistency between visual perception and textual deduction (Liu et al., 2023). In the geometric domain,
this issue is particularly acute, manifesting as the reasoning illusion” (Wang et al., 2025) where models
may retrieve correct formulas but apply them to hallucinated geometric primitives. As emerging systems
increasingly position MLLMs as scientific agents interacting with complex environments (Team et al., 2025;
Zhang et al., 2025a; Gottweis et al., 2025), the demand for rigorous reasoning has intensified. To address
this, Multimodal Chain-of-Thought strategies (Zhang et al., 2023b; Shao et al., 2023) have been proposed to
bridge the gap between visual perception and answer generation by eliciting intermediate rationales.
Nevertheless, when confronted with visual mathematical content such as geometry diagrams, current MLLMs
continue to exhibit significant performance drops. This is largely attributed to the domain discrepancy
between natural images and schematic figures, as well as the requirement for long-horizon, logically precise
reasoning (Lu et al., 2024). To mitigate these limitations, domain-specialized models have leveraged
targeted data or training objectives: MAVIS synthesizes large-scale chain-of-thought supervision for math
diagrams (Zhang et al., 2024), while G-LLaVA collects supermodel-guided geometric solutions (Gao et al.,
2025). Similarly, GeoX aligns visual features with formal geometric primitives to enable solver-backed
theorem verification (Xia et al., 2025). Our work offers a complementary perspective: rather than proposing
a new architecture, we focus on extracting verifiable process signals from formal geometric structures and
utilizing them as dense rewards to enhance the reasoning reliability of existing MLLMs.


B.2    Geometric Problem Solving with MLLMs and Formal Solvers

Automatic geometric problem solving (GPS) requires understanding diagrams, interpreting symbolic condi-
tions, and composing nontrivial deductive chains. A line of work enhances visual and textual understanding
via unimodal pre-training, cross-modal alignment, and instruction tuning on geometry corpora (Chen et al.,
2021; 2022a; Zhang et al., 2023a; Hao et al., 2022; Xia et al., 2025; Zhang et al., 2024; Gao et al., 2025;
Jiang et al., 2025). These methods typically train MLLMs to directly output final numerical answers or
natural-language solutions given the diagram and problem text.



                                                    18
                                                                                          CUHKSZ & SJTU
                                                                                               January 9, 2026



Another line of research adopts formal geometric solvers or external interpreters. Systems such as Al-
phaGeometry and its successors (Trinh et al., 2024; Chervonyi et al., 2025; Sicca et al., 2024) can solve
problems at the level of international mathematical olympiads by encoding each instance in a formal language
and searching in a rule-based state space. While these approaches offer strong guarantees and IMO-level
performance, they require precise symbolic modeling of each instance, which limits their practicality for
open-ended user-facing applications. To bridge the gap between rigorous calculation and open-ended
reasoning, Program-of-Thought (Chen et al., 2022b) and PAL (Gao et al., 2023b) decouple reasoning from
computation by delegating arithmetic to external Python interpreters. While effective for reducing calculation
errors, these methods largely treat reasoning as a linear script generation task without verifying the logical
soundness of the underlying deductive chain.
Our work lies in between: we rely on a formal geometric backend to generate trusted reasoning skeletons,
but keep the inference model as an MLLM that operates directly over diagrams and text. Instead of asking
the solver to produce complete symbolic proofs at test time, we convert its offline skeletons into verifiable
subgoals and use them to shape the MLLM’s reasoning process through reinforcement learning.


B.3    Datasets and Benchmarks for Geometric Reasoning

High-quality data is critical for improving GPS systems. Existing datasets can be roughly divided into three
construction paradigms (Chen et al., 2021; Cao & Xiao, 2022; Chen et al., 2022a; Lu et al., 2024; He
et al., 2024). The first filters real-world exam or textbook problems and manually annotates diagrams and
solutions, as in GeoQA (Chen et al., 2021), GeoQA+ (Cao & Xiao, 2022), UniGeo (Chen et al., 2022a),
PGDP5K (Hao et al., 2022), MathVista (Lu et al., 2024), and OlympiadBench (He et al., 2024). These
datasets offer human-authored, high-quality questions, but their scalability is constrained by limited source
pools and annotation cost, and the difficulty level is often biased toward middle- or high-school geometry.
In contrast to manual annotation, the second paradigm uses formal engines to synthesize problems and
proofs (Lu et al., 2021; Zhang et al., 2023a; Kazemi et al., 2023). Inter-GPS and PGPS9K generate
diagram–text pairs by sampling from pre-defined geometry configurations (Lu et al., 2021; Zhang et al.,
2023a), while GeomVerse augments authentic questions via LLM-based transformations (Kazemi et al., 2023).
Formal engines can guarantee logical correctness and scale up easily, but the resulting textual solutions may
diverge from natural mathematical discourse. The third paradigm employs LLMs to synthesize reasoning
trajectories (Zhang et al., 2024; Gao et al., 2025), which yields human-like step-by-step explanations but
lacks verifiable guarantees and may introduce subtle logical errors. Recent studies suggest that high-quality
synthetic data is crucial for unlocking complex reasoning capabilities (Li et al., 2023c; Gunasekar et al.,
2023). However, synthesizing reliable geometric reasoning paths remains challenging due to the difficulty of
ensuring cross-modal consistency between diagrams and text.
More recently, TrustGeoGen (Fu et al., 2025) proposes a scalable, rule-driven engine that generates synthetic
geometry problems together with formal proofs, natural-language explanations, and diagrams under a unified
formal language. GeoBench (Feng et al., 2025) further builds on TrustGeoGen to design a hierarchical GPS
benchmark that evaluates four critical abilities: visual perception, goal-oriented planning, rigorous theorem
application, and self-reflective backtracking, moving beyond single final-answer accuracy. Other works such
as GeomRel (Wang et al., 2025) and GeoSense (Xu et al., 2025a) explore structural diagram understanding
and theorem-application patterns but still focus on narrow subskills. In contrast, our work leverages formal
skeletons from a TrustGeoGen-style engine to construct a sequence of verifiable numeric subgoals for each
instance and defines skeleton-based metrics (Skeleton Rate and Skeleton Completion) that jointly capture
local step correctness and global proof coherence. Importantly, we go one step further by using these
verifiable subgoals not only for evaluation but also as dense training signals for reinforcement learning.




                                                     19
                                                                                                                                             CUHKSZ & SJTU
                                                                                                                                                      January 9, 2026



        lconst                                                                     100




                                                               Number of Samples
                                                                                                                                                      Train Mean (10.2)
          free                                                                                                                                        Test Mean (28.9)
                                                                                    80
      on_circle                                                                                                                                       Train

       square                                                                       60                                                                Test

   ninepoints
                                                                                    40
intersection_ll
                                                                                    20
         circle
                                                  Train
      midpoint                                                                       0
                                                  Test




                                                                                              )
                                                                                                   0)

                                                                                                           )

                                                                                                                    )

                                                                                                                           )

                                                                                                                                  )

                                                                                                                                         )

                                                                                                                                                )

                                                                                                                                                       )

                                                                                                                                                              )

                                                                                                                                                                    )
      triangle




                                                                                          ,5



                                                                                                        15

                                                                                                                 20

                                                                                                                        25

                                                                                                                               30

                                                                                                                                      35

                                                                                                                                             40

                                                                                                                                                    45

                                                                                                                                                           50

                                                                                                                                                                   ∞
                                                                                                  ,1




                                                                                                                                                               0,
                                                                                         [0



                                                                                                       0,

                                                                                                             5,

                                                                                                                    0,

                                                                                                                           5,

                                                                                                                                  0,

                                                                                                                                         5,

                                                                                                                                                0,

                                                                                                                                                       5,
                                                                                              [5
                  0.00   0.05    0.10    0.15   0.20




                                                                                                                                                              [5
                                                                                                   [1

                                                                                                            [1

                                                                                                                  [2

                                                                                                                         [2

                                                                                                                                [3

                                                                                                                                       [3

                                                                                                                                              [4

                                                                                                                                                     [4
                                Proportion                                                         Proof Length (Number of Sub-goals)


Figure 7: Dataset characteristics across Train and Test splits. Left: Dumbbell chart showing the
proportion of geometric concepts in both splits, where connecting lines indicate distributional differences.
Right: Histogram showing proof-length distribution, with the test set containing a higher proportion of
instances with longer reasoning chains, providing a more challenging evaluation of multi-step reasoning
capabilities.


B.4     Process Supervision and Reinforcement Learning for Reasoning

There is a growing interest in process-oriented supervision for mathematical and logical reasoning. Recent
benchmarks and evaluators (Lu et al., 2024; Zhang et al., 2025b) analyze the quality of intermediate steps
rather than only final answers, revealing phenomena such as “shortcut” solutions and self-contradictory
chains. In geometric reasoning, GeoBench (Feng et al., 2025) evaluates models at multiple levels (from
perception to backtracking) using structured tasks derived from formal reasoning graphs, but the resulting
signals are used purely for diagnosis.
While Process Reward Models (Lightman et al., 2023; Uesato et al., 2022) have successfully scaled
mathematical reasoning by training discriminator models to score intermediate steps, they face a fundamental
bottleneck: the reliance on expensive human annotations or synthesized labels. Furthermore, learned reward
models are susceptible to “reward hacking,” where the policy model learns to exploit the critic’s inaccuracies
rather than improving reasoning quality (Gao et al., 2023a). In parallel, reasoning-optimized models such
as OpenAI o1/o3 (OpenAI, 2024a; 2025a) and specialized MLLMs (Wu et al., 2024; DeepMind, 2025; Bai
et al., 2025) implicitly incorporate internal process supervision and reinforcement learning, but their training
recipes and reward functions are largely proprietary or rely on learned reward models that can themselves
be unreliable.
Our work is closest in spirit to process-supervised and RL-based reasoning, but differs in two key aspects.
First, we obtain rule-grounded milestone signals by decomposing formal proof skeletons into atomic sub-
goals and mapping them to numeric targets that can be automatically verified for each step. Second, we
transform these verifiable sub-goals into token-level advantages and optimize MLLMs with a PPO-style
objective, thereby turning skeleton-based evaluation into a dense, stable reward signal. This avoids training
a separate reward model and mitigates hallucination in the supervision channel. Experiments across
geometric, mathematical, and general reasoning benchmarks show that such verifiable sub-goal rewards
not only improve final-answer accuracy but also significantly enhance the quality and consistency of the
generated reasoning chains.



C Dataset Characteristics

This section provides detailed statistics and distributions for our step-wise verifiable geometric reasoning
benchmark.



                                                          20
                                                                                          CUHKSZ & SJTU
                                                                                               January 9, 2026



Figure 7 presents comprehensive statistics of our benchmark across Train and Test splits. The left panel
shows the distribution of geometric concepts (predicates and constructions), where both splits exhibit compa-
rable coverage across all major element types, including constant-valued constraints (lconst), free point
constructions (free), circle-related predicates (on_circle), square constructions, and various intersection
and midpoint predicates. The dumbbell chart clearly illustrates where the two splits align (short connecting
lines) and where they differ (longer connecting lines). Specialized constructions like centroids, nine-point
circles, and parallelograms appear less frequently but are present in both splits. The right panel shows the
proof-length distribution, revealing that the test set is intentionally skewed toward longer reasoning chains,
with more instances requiring 8+ sub-goal verifications, providing a diverse range of reasoning complexities
in our benchmark.



D Geometric-to-Numeric Mapping

This section specifies the complete mapping from formal geometric predicates to numeric evaluation tar-
gets used in our benchmark construction. Each predicate in the formal language (based on the Newclid
system (Sicca et al., 2024)) is associated with one or more numeric expressions and their correspond-
ing ground-truth values. All angle measurements are expressed in degrees modulo 180°; all ratios are
dimensionless.


D.1    Notation and Conventions

For each predicate type, we provide:

   • Predicate: The formal predicate identifier and argument pattern
   • Numeric Form: The corresponding numeric expression T to be evaluated
   • Expected Value: The ground-truth value for correct instantiations
   • Notes: Additional specifications regarding orientation, degenerate configurations, or alternative formu-
     lations

Notational conventions:

   • |AB| denotes the Euclidean length of segment AB

   • ∠(AB, CD) denotes the directed angle between line segments AB and CD
   • area_triangle(A, B, C) denotes the signed area of triangle ABC
   • For equality predicates, we adopt ratio-based formulations (expected value 1) rather than difference-
     based formulations (expected value 0) to mitigate numerical instability near zero


D.2    Core Geometric Predicates

Table 5 specifies the numeric mappings for fundamental geometric predicates that commonly appear in
formal proof derivations.




                                                     21
                                                                                                        CUHKSZ & SJTU
                                                                                                           January 9, 2026



D.3    Constant Constraints

Formal proof derivations frequently involve constant-valued constraints on geometric quantities (lengths,
angles, ratios). Table 6 specifies their numeric representations.


D.4    Special Triangle Types

Table 7 defines the numeric verification conditions for predicates characterizing specialized triangle configu-
rations.


D.5    Quadrilaterals and Polygons

Table 8 specifies the verification conditions for predicates pertaining to quadrilaterals and higher-order
polygons.


D.6    Constructed Auxiliary Points

Numerous predicates encode auxiliary point constructions (e.g., on_pline, on_tline) that introduce interme-
diate geometric entities. Table 9 defines the corresponding verification conditions.



E Training Configurations and Hyperparameters

We implement the RLVR training stage using the MM-Eureka Meng et al. (2025) framework, built upon
OpenRLHF Hu et al. (2025). All models, including Qwen2.5-VL-3B and 7B, share an identical hyperparameter
configurations.
Training is conducted on a cluster of 8 NVIDIA H100 GPUs. We utilize DeepSpeed3 ZeRO-3 to manage
memory efficiency. Following the SGVR framework, we employ Group Relative Policy Optimization (GRPO)
to optimize the policy by maximizing the Skeleton Rate (SR). The visual encoder remains frozen during the
reinforcement learning process. Key hyperparameters are detailed in Table 10.




F Evaluation Details

F.1   Answer Verification Protocol

To evaluate numerical answer equivalence across diverse mathematical representations (fractions, decimals,
radical expressions), we employ GPT-5-nano (OpenAI, 2025b) as an automated equivalence checker. The
complete prompt is below:

  Answer Verification Prompt
  Given two solutions from a geometry question, please judge whether the answers are the same or not.
  Basic Rules:

  3 https://github.com/microsoft/DeepSpeed




                                                             22
                                                                                                                      CUHKSZ & SJTU
                                                                                                                         January 9, 2026



                  Table 5: Mapping of core geometric predicates to numeric evaluation targets.

Predicate                                    Numeric Form T                            Expected   Notes
Equality Predicates
cong[A,B,C,D]                                |AB|/|CD|                                    1       Segment equality
eqratio[A,B,C,D,E,F,G,H]                     (|AB|/|CD|)/(|EF |/|GH|)                     1       Ratio equality: AB : CD = EF : GH
eqangle[P_0,P_1,P_2,P_3,P_4,P_5,P_6,P_7]     ∠(P0 P1 , P2 P3 ) − ∠(P4 P5 , P6 P7 )        0       Angle equality (mod 180°)
Parallel and Perpendicular
para[A,B,C,D]                                ∠(AB, CD)                                     0      Parallel: AB ∥ CD
perp[A,B,C,D]                                ∠(AB, CD)                                    90      Perpendicular: AB ⊥ CD
Circle-Related
cyclic[A,B,C,D]                              ∠(AB, CB) + ∠(AD, CD)                       180      Opposite angles sum to 180°
on_circle[X,O,A]                             |OX|/|OA|                                    1       Point X on circle at O
lc_tangent[X,A,O]                            ∠(AX, AO)                                   90       Tangent perpendicular to radius
Similarity and Congruence
simtrir[A,B,C,D,E,F]                         ∠(AB, BC) − ∠(DE, EF )                       0       Similar triangles
Collinearity
coll[A,B,C]                                  area_triangle(A, B, C)                       0       Zero area
on_line[X,A,B]                               ∠(AX, XB)                                    0       Point X on line AB



                             Table 6: Mapping of constant-valued geometric constraints.

                 Predicate             Numeric Form T            Expected            Notes
                 rconst[A,B,C,X,r]     |AB|/|CX|                       r             Constant ratio |AB|/|CX| = r
                 rconst2[X,A,B,r]      |AX|/|BX|                       r             Constant ratio |AX|/|BX| = r
                 aconst[A,B,C,X,θ]     ∠(AB, CX)                       θ             Fixed angle θ (degrees, mod 180°)
                 s_angle[A,B,X,θ]      ∠(AB, BX)                       θ             Angle at vertex B equals θ
                 lconst[A,X,l]         |AX|                            l             Fixed length |AX| = l
                 midp[M,A,B]           |AM |/|M B|                     1             Midpoint: |AM | = |M B|


                                Table 7: Mapping of special triangle type predicates.

                 Predicate             Numeric Form T            Expected        Notes
                 ieq_triangle[A,B,C]   ∠(AB, BC)                     60          Equilateral triangle: all angles 60°
                 iso_triangle[A,B,C]   |AB|/|AC|                      1          Isosceles: |AB| = |AC|
                 r_triangle[A,B,C]     ∠(AB, AC)                     90          Right triangle: right angle at A
                 triangle12[A,B,C]     |AB|/|AC|                     0.5         Triangle with |AB| : |AC| = 1 : 2
                 risos[A,B,C]          ∠(AB, AC)                     90          Isosceles right triangle at A
                 nsquare[X,A,B]        ∠(XA, XB)                     90          Isosceles right triangle: ∠AXB = 90


                             Table 8: Mapping of quadrilateral and polygon predicates.

                 Predicate                    Numeric Form T           Expected         Notes
                 rectangle[A,B,C,D]           ∠(AB, BC)                     90          Rectangle: ∠ABC = 90
                 square[A,B,X,Y]              ∠(AB, AX)                     90          Square: right angle + equal sides
                 trapezoid[A,B,C,D]           ∠(AB, CD)                      0          Trapezoid: AB ∥ CD
                 r_trapezoid[A,B,C,D]         ∠(AB, AD)                     90          Right trapezoid: ∠BAD = 90
                 eq_quadrangle[A,B,C,D]       |AD|/|BC|                      1          Quadrilateral with |AD| = |BC|
                 eqdia_quadrangle[A,B,C,D]    |AC|/|BD|                      1          Equal diagonals: |AC| = |BD|
                 psquare[X,A,B]               ∠(AB, AX)                     90          Rotate B by 90° around A to X




                                                                  23
                                                                                                                  CUHKSZ & SJTU
                                                                                                                        January 9, 2026



                            Table 9: Mapping of auxiliary point construction predicates.

              Predicate                 Numeric Form T              Expected   Notes
              on_pline[X,A,B,C]         ∠(AX, BC)                       0      X on parallel to BC through A
              on_tline[X,A,B,C]         ∠(AX, BC)                      90      X on perpendicular to BC through A
              on_bline[X,A,B]           |XA|/|XB|                       1      X on perpendicular bisector of AB
              on_dia[X,A,B]             ∠(AX, BX)                      90      X on circle with diameter AB
              on_aline[X,A,B,C,D,E]     ∠(BA, AX) − ∠(ED, DC)           0      Angle transfer construction
              reflect[X,A,B,C]          ∠(BA, BC) − ∠(CB, CX)          0       Reflection of A across line BC
              eqangle2[X,A,B,C]         ∠(AX, XB) − ∠(CX, XA)          0       Opposite angles ∠BXA = ∠CXA
              eqangle3[X,A,B,D,E,F]     ∠(AX, XB) − ∠(DE, EF )         0       Angle equality ∠AXB = ∠DEF
              eqratio6[X,A,C,E,F,G,H]   (|AX|/|CX|)/(|EF |/|GH|)        1      Ratio constraint |AX| : |CX| = |EF | : |GH|


                                        Table 10: Hyperparameters for training.

                                 Hyperparameter                                Value
                                 Base Models                       Qwen2.5-VL-3B / 7B Instruct
                                 Optimizer                                 AdamW
                                 Actor Learning Rate                       1 × 10−6
                                 Training Batch Size                          16
                                 Micro Batch Size                              2
                                 Samples per Prompt (G)                        8
                                 KL Coefficient (β)                          0.01
                                 Max Prompt Length                           4096
                                 Max Generation Length                       4096
                                 Precision                                   BF16



  • If the two answers are the same, output 1.
  • If the two answers are different, output 0.
  • If you are not sure, output NOT SURE.
  • Do not consider units in the answers, only consider the numerical values.
  Numerical Comparison Rules:
  1. Fractions and Decimals: 1/2 = 0.5, 1/3 = 0.333, 2/3 = 0.667, etc.
  2. Floating Point Tolerance: Numbers are considered the same if they are within 0.02 of each other. Examples: 1.333 and
      1.334 are the same.
  3. Square  √ Root Expressions:
                          √         Convert
                                       √ square roots to decimal approximations for comparison.
           •   2 ≈ 1.414, 3 ≈ 1.732,√ 5 ≈ 2.236        √
           • For any expression like a b, calculate a ×√ b and convert to decimal.
  4. Complex Expressions: For expressions like (a b)/c or fractions involving square roots, convert the entire expression to
      decimal form.
  Examples:
     √
  • “ √ 2” and “1.414” → Same (<evaluation>1</evaluation>)
  • “2 2” and “2.828” → Same (<evaluation>1</evaluation>)
                                         √
  • “198/7” and “28.29” → Same as “20 2 ≈ 28.28” (<evaluation>1</evaluation>)
  Task:
  Solution 1: {solution1}
  Solution 2: {solution2}
  Please analyze step by step and give your final conclusion in <evaluation>result</evaluation> format.




Output parsing. The evaluator returns structured judgments in XML format (<evaluation>...</evaluation>).
We extract these using regular expressions and encode the results as binary labels (1 for equivalence, 0
for non-equivalence), with “NOT SURE” outcomes recorded separately for ambiguous cases that require
manual inspection.



G Case Studies: Reasoning Failures Leading to Incorrect Answers


                                                               24
                                                                                                        CUHKSZ & SJTU
                                                                                                             January 9, 2026




We present detailed qualitative comparisons between baseline models and SGVR-trained models across
three representative examples spanning probability, logic, and combinatorial reasoning. These cases
illustrate systematic differences in constraint adherence and mathematical rigor, where reasoning errors lead
to incorrect final answers.
Notation: Baseline responses appear in gray boxes, SGVR-trained responses in blue boxes. Red highlights
denote reasoning errors; blue highlights mark corresponding reasoning steps for comparison.


G.1    Case 1: AMC Dataset – Ant Amelia Probability Problem

Problem Statement. Ant Amelia starts on the number line at 0 and crawls in the following manner. For
n = 1, 2, 3, Amelia chooses a time duration tn and an increment xn independently and uniformly at random
from the interval (0, 1). During the nth step of the process, Amelia moves xn units in the positive direction,
using up tn minutes. If the total elapsed time has exceeded 1 minute during the nth step, she stops at the
end of that step; otherwise, she continues with the next step, taking at most 3 steps in all. What is the
denominator plus the numerator of the probability that Amelia’s position when she stops will be greater than
1?
Ground Truth Answer: 5 (probability is 23 )

  Baseline Response:
  To solve this problem, we need to determine the probability that Ant Amelia’s final position exceeds 1 after at most
  three steps. We break down the problem into cases based on the number of steps taken.
  [Case 1 and Case 2 analysis omitted: Baseline correctly finds probabilities 0 and 12 respectively.]
  Case 3: Three steps
  Amelia takes three steps, but only if the first two steps do not cause her to stop early. Her position is P3 = x1 +x2 +x3
  if both t2 ≤ t1 and t3 ≤ t2 . The condition for her position to exceed 1 is:

                                                     x1 + x2 + x3 > 1

  This is more complex to analyze directly, so we use symmetry and the fact that the distribution of the sum of uniform
  random variables is well-known. The probability that the sum of three independent uniform random variables
  exceeds 1 is known to be 85 .
  Combining these probabilities, the overall probability that Amelia’s position exceeds 1 is:
                                                   1  5 4 4 5  13
                                              0+     + = + + =
                                                   2  8 8 8 8  8
   However, since we are asked for the denominator plus the numerator of the simplified fraction representing the
  probability, we have:
                                                 13 + 8 = 21

  Thus, the answer is:
                                                             21



Baseline errors. (1) Directly cites “known result” 58 without derivation; (2) Ignores the stopping condition
t1 + t2 + t3 ≤ 1; (3) Incorrect final answer 21.

  SGVR-trained Response:
  Let D2 = x1 + x2 and D3 = x1 + x2 + x3 . Since t1 ∈ (0, 1) almost surely, Amelia cannot exceed 1 minute during
  step 1, so P (stop after step 1) = 0. Moreover,

                                           stop after step 2 ⇐⇒ t1 + t2 > 1,




                                                             25
                                                                                           CUHKSZ & SJTU
                                                                                                January 9, 2026




                                         stop after step 3 ⇐⇒ t1 + t2 ≤ 1.

  Because {ti } are independent of {xi }, we can factor “time” and “distance” events.
  Case 2: stopping after step 2.


                               P (stop at 2 and D2 > 1) = P (t1 + t2 > 1) P (D2 > 1)
                                                          1 1      1
                                                        = · = .
                                                          2 2      4
  Case 3: stopping after step 3.


                               P (stop at 3 and D3 > 1) = P (t1 + t2 ≤ 1) P (D3 > 1)
                                                          1 5       5
                                                        = · =         .
                                                          2 6      12
  where
                                                Z 1 Z 1−x1 Z 1−x1 −x2        
                                P (D3 ≤ 1) =                             1 dx3 dx2 dx1
                                                 0     0          0
                                                Z 1 Z 1−x1
                                            =                (1 − x1 − x2 ) dx2 dx1
                                                 0     0
                                                1
                                            =     .
                                                6
  Therefore,
                                                          1   5   2
                                             P (D > 1) =    +    = ,
                                                          4   12  3
                                                      2+3=5

                                                             21



Key distinction. The SGVR-trained model makes the step-count constraint explicit (step 2 vs. step 3
determined by t1 + t2 ) and uses independence to factor probabilities; in contrast, the baseline ignores the
stopping rule and (implicitly) treats the distance sum as unconstrained, leading to an invalid probability > 1.


G.2    Case 2: Livebench Reasoning – Logic Puzzle

Problem Statement. There are 3 people standing in a line numbered 1 to 3. Each person has attributes:
Beverage, Food, Movie-Genre, Nationality. Given constraints:
   • Juice drinker is right of soy-milk drinker
   • Thriller watcher is in even position
   • Family watcher drinks juice
   • Apricot eater is right of soy-milk drinker
   • Pakistani is not left of apricot eater
   • Grape eater is left of soy-milk drinker
   • Grape eater is immediately left of British person
Questions: (1) Position of Spanish person? (2) Nationality of grape eater? (3) Beverage at position 2? (4)
Beverage of family watcher?

Ground Truth Answer: 1, Spanish, Soy-milk, Juice




                                                           26
                                                                                                           CUHKSZ & SJTU
                                                                                                                 January 9, 2026




  Baseline Response:
  Let’s solve these step-by-step using the given constraints.
  [Initial constraint analysis omitted: Baseline correctly identifies that grape-eater and British person have an
  immediate left-right relationship, and determines that British person is in position 3, grape-eater in position 2.]
  Now, considering the other constraints: - The person eating apricot must be to the right of the soy-milk drinker. -
  The pakistani person cannot be to the left of the apricot eater.
  Given the British person is at position 3, the apricot eater must be in position 4 (since they’re to the right of the
  soy-milk drinker).
  So far, we have: - Position 1: unknown - Position 2: grape-eater - Position 3: British - Position 4: apricot-eater
  [Remaining attribute assignment steps omitted: Baseline assigns attributes to all positions, including incorrectly
  assigning Pakistani nationality to position 2 (grape-eater).]
  Final Assignment:
  - Position 1: Kale-eater (spanish), Juice-drinker, Family-watcher
  - Position 2: Grapes-eater (pakistani), Soy-milk-drinker, Thriller-watcher
  - Position 3: British, Lemonade-drinker, Action-watcher
  - Position 4: Apricot-eater (pakistani), Soy-milk-drinker, Thriller-watcher
  Answers:
  1. At what position is the person who is Spanish? Answer: 1
  2. What is the nationality of the person who eats grapes? Answer: Pakistani
  3. What beverage does the person in position 2 drink? Answer: Soy-milk
  4. What is the beverage of the person who watches family? Answer: Juice
  <solution>1, Pakistani, Soy-milk, Juice</solution>



Baseline errors. (1) Assumes position 4 exists when only 3 people are present; (2) Incorrectly assigns
Pakistani nationality to grape eater; (3) Final answer incorrectly states grape eater is Pakistani instead of
Spanish.

  SGVR-trained Response:
  We have only three positions {1, 2, 3}. From “grape eater is immediately left of the British person”, the only
  possibilities are (grape, British) = (1, 2) or (2, 3).
  If (2, 3), then grape is in position 2, so soy-milk must be in position 3 (grape is left of soy-milk). But then there is no
  position to the right of soy-milk for juice, contradicting “juice is right of soy-milk”. Hence (2, 3) is impossible.
  Therefore grape-eater is in position 1 and the British person is in position 2. Since grape is left of soy-milk, soy-milk
  cannot be in position 1, and if soy-milk were in position 3 then again no one could be to its right. Thus soy-milk is
  in position 2 and juice is in position 3; by “family watcher drinks juice”, position 3 watches family.
  Finally, apricot is right of soy-milk, so apricot is in position 3; Pakistani is not left of apricot, so Pakistani is also in
  position 3. The remaining nationality at position 1 is Spanish. (Thriller is the even position ⇒ position 2.)
  Answers:
  1. At what position is the person who is spanish? Answer: 1
  2. What is the nationality of the person who eats grapes? Answer: Spanish
  3. What beverage does the person in position 2 drink? Answer: Soy-milk
  4. What is the beverage of the person who watches family? Answer: Juice
  <solution>1, Spanish, Soy-milk, Juice</solution>



Key distinction. Both approaches notice the adjacency between grape eater and the British person.
However, the SGVR-trained model uses the 3-position constraint plus “juice is right of soy-milk” to rule out
the (2, 3) adjacency case, while the baseline invents a non-existent position 4 and derails the remaining
assignments.


G.3    Case 3: Livebench Reasoning – Heptagon Cutting

Problem Statement. Suppose I have a regular heptagon, and I can make four straight cuts. Each cut
cannot pass through any vertices. Also, exactly three of the cuts must intersect at a single point within the


                                                               27
                                                                                                    CUHKSZ & SJTU
                                                                                                          January 9, 2026



heptagon. What is the maximum number of resulting pieces?
Ground Truth Answer: 10

  Baseline Response:
  To solve this problem, we need to understand how cutting a heptagon with specific conditions affects its division
  into pieces.
  1. Initial Setup: We start with one piece: the entire heptagon.
  2. First Cut: The first cut divides the heptagon into two pieces.
  3. Second Cut: The second cut intersects the first cut but does not pass through any vertex. This will divide each
  of the two pieces from the previous step into two more pieces, resulting in 2 + 2 = 4 pieces.
  4. Third Cut: The third cut intersects both of the previous cuts but does not pass through any vertex. This will
  further divide each of the four pieces into two more pieces, resulting in 4 + 4 = 8 pieces.
  5. Fourth Cut: The fourth cut intersects all three previous cuts but does not pass through any vertex. This will
  further divide each of the eight pieces into two more pieces, resulting in 8 + 8 = 16 pieces.
  Thus, after making four such cuts, the maximum number of resulting pieces is 16 .



Baseline errors. (1) Ignores the constraint that exactly three cuts must intersect at a single point; (2)
Incorrectly assumes each cut doubles the region count without accounting for the special intersection
constraint; (3) Incorrect final answer 16.

  SGVR-trained Response:
  To solve this problem, we need to understand how cutting a shape with straight lines affects the number of regions
  it creates. The key insight here is that each new line added can potentially intersect all previous lines, creating
  additional regions.
  Let’s break it down step by step:
  1. Initial Shape: We start with a heptagon, which has 7 sides.
  2. First Cut: When we make the first cut, it will divide the heptagon into two regions. So now we have 2 regions.
  3. Second Cut: The second cut can intersect the first cut and add one more region for each intersection plus one
  more region if it doesn’t intersect the first cut. Since the second cut intersects the first cut once, it adds 2 more
  regions. So now we have 2 + 2 = 4 regions.
  4. Third Cut: The third cut can intersect the first two cuts twice, adding 3 more regions. So now we have 4 + 3 = 7
  regions.
  5. Fourth Cut: The fourth cut can intersect the first three cuts three times, adding 4 more regions. However,
  since exactly three of the cuts must intersect at a single point, this cut will only add 3 more regions because the
  intersection point does not create an extra region due to the condition. So now we have 7 + 3 = 10 regions.
  Thus, the maximum number of resulting pieces after making four straight cuts, with exactly three of them intersecting
  at a single point, is 10 .



Key distinction. Both approaches correctly analyze cuts 1-3 (yielding 2, 4, and 7 regions). However, for
the fourth cut, SGVR-trained model explicitly accounts for the constraint that three cuts intersect at a single
point, recognizing this reduces additional regions from 4 to 3, while baseline applies a generic doubling
heuristic.


G.4    Summary: Constraint Adherence and Reasoning Rigor

A consistent pattern emerges across all three cases: baseline models exhibit plausible initial reasoning but
fail to maintain constraint awareness throughout multi-step derivations, while SGVR-trained models maintain
systematic constraint verification at every reasoning step.
Specifically, in Case 1 (Ant Amelia), baseline cites an unsubstantiated result and fails to condition on the
stopping rule; SGVR-trained model makes the step-count constraint explicit (step 2 vs. step 3 determined by
t1 + t2 ) and computes the distance terms rigorously. In Case 2 (Logic Puzzle), baseline violates the problem


                                                          28
                                                                                                 CUHKSZ & SJTU
                                                                                                      January 9, 2026



specification by introducing a non-existent position 4; SGVR-trained model systematically verifies constraint
compatibility at each inference step. In Case 3 (Heptagon Cutting), baseline applies a generic counting
heuristic without adapting to the special intersection constraint; SGVR-trained model explicitly reasons about
how the constraint modifies region generation.
These examples illustrate that subgoal-level correctness—maintaining rigorous constraint adherence and
mathematical validity throughout the derivation—is essential for reliable problem-solving. SGVR’s step-wise
verification mechanism ensures logical soundness and constraint compliance at each reasoning step, rather
than merely encouraging superficially plausible intermediate steps.



H Case Studies: Correct Answers via Incorrect Reasoning

We present case studies where baseline models arrive at correct final answers through fundamentally flawed
reasoning processes. These examples demonstrate the critical distinction between outcome correctness
and subgoal correctness, illustrating why answer verification alone is insufficient for evaluating mathematical
reasoning capabilities.


H.1    Case 1: AMC Dataset – 4×4 Matrix Problem

Problem Statement. How many 4 × 4 arrays whose entries are 0s and 1s are there such that the row sums
(the sum of the entries in each row) are 1, 2, 3, and 4, in some order, and the column sums (the sum of the
entries in each column) are also 1, 2, 3, and 4, in some order? Output the remainder when the answer is
divided by 100.
For example, the following array satisfies the condition.
                                                                
                                                 1 1 1         0
                                                0 1 1         0 
                                                                
                                                1 1 1         1 
                                                 0 1 0         0

Ground Truth Answer: 76

  Baseline Response:
  To solve this problem, we need to determine how many 4 × 4 matrices with entries either 0 or 1 satisfy both the
  row sums and the column sums being exactly 1, 2, 3, and 4 in some order.
  Firstly, note that if the row sums are 1, 2, 3, and 4, then the column sums must be the same because the total
  number of 1s in the matrix is fixed. This means that the column sums must also be 1, 2, 3, and 4 in some order.
  The only way this can happen is if each row has exactly one more 1 than the previous row up to the fourth row,
  which implies that the rows must be arranged in increasing order of their sums from left to right. Therefore, the
  possible row arrangements are permutations of the sequence (1, 2, 3, 4), and similarly for the columns.
  The number of ways to arrange the rows is 4! (since any permutation of the four distinct numbers will work).
  Similarly, the number of ways to arrange the columns is also 4!. Since these two arrangements are independent,
  the total number of such matrices is:
                                               (4!) × (4!) = 24 × 24 = 576.

  Finally, we need to find the remainder when 576 is divided by 100:

                                            576 ÷ 100 = 5 remainder 76.

  Thus, the remainder when 576 is divided by 100 is:

                                                        76 .



                                                        29
                                                                                                      CUHKSZ & SJTU
                                                                                                            January 9, 2026



Reasoning error. Baseline incorrectly assumes row and column sum arrangements are independent,
treating this as a simple permutation problem rather than recognizing the constrained bipartite matching
structure.


Analysis. The baseline treats row and column sum arrangements as independent (4! × 4! = 576), when
matrix entries must simultaneously satisfy both constraints—a combinatorial structure requiring careful
enumeration. The correct count is indeed 576, but arrives at this value through fundamentally flawed
independence reasoning. The coincidental correctness (576 mod 100 = 76) demonstrates that outcome-only
evaluation fails to detect invalid reasoning paths, underscoring the necessity of subgoal-level verification.


H.2    Case 2: Olympiad Dataset – Spherical Geometry Problem

Problem Statement. The Little Prince lives on a spherical planet which has a radius of 24 km and centre
O. He hovers in a helicopter (H) at a height of 2 km above the surface of the planet. From his position in the
helicopter, what is the distance, in kilometres, to the furthest point on the surface of the planet that he can
see?




                       Figure 8: Geometric diagram for the spherical geometry problem.

Ground Truth Answer: 10

  Baseline Response:
  To determine the distance to the furthest point on the surface of the planet that the Little Prince can see from his
  position in the helicopter, we need to analyze the geometry of the situation. The Little Prince is at a height of 2 km
  above the surface of the planet, and the radius of the planet is 24 km. Therefore, the distance from the center of
  the planet to the Little Prince is 24 + 2 = 26 km.
  We need to find the distance from the Little Prince’s position to the furthest point on the surface of the planet. This
  distance is the hypotenuse of a right triangle where one leg is the radius of the planet (24 km) and the other leg is
  the distance from the center of the planet to the Little Prince (26 km).
  Using the Pythagorean theorem, we can find the distance to the furthest point on the surface of the planet. Let d
  be the distance from the Little Prince to the furthest point on the surface of the planet. Then we have:
                                                       p
                                                   d = (26)2 − (24)2

  Calculating the squares, we get:              √                 √
                                           d=       676 − 576 =       100 = 10 km
  Therefore, the distance to the furthest point on the surface of the planet that the Little Prince can see is 10 km.



Reasoning error. Baseline incorrectly describes the geometry, claiming the sought distance is a triangle
hypotenuse with legs (24 km, 26 km)—a geometrically invalid construction for the tangent-line visibility
problem.


Analysis. The baseline mischaracterizes the geometric configuration: the correct approach identifies
the tangent point T on the sphere where the line of sight from H (helicopter) touches the surface. By the


                                                            30
                                                                                          CUHKSZ & SJTU
                                                                                               January 9, 2026



tangent-secant relationship, HT 2 = HO2 − OT 2 = 262 − 242 = 100, yielding HT = 10 km. Although the
numerical calculation fortuitously produces the correct answer, the underlying geometric reasoning is invalid.
This case exemplifies how answer-only evaluation can fail to detect conceptual errors, reinforcing the value
of step-wise subgoal verification.




                                                     31
