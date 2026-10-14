                                         Leanabell-Prover-V2: Verifier-integrated Reasoning for Formal
                                                Theorem Proving via Reinforcement Learning

                                             Xingguang Ji, Yahui Liu, Qi Wang♥ , Jingyuan Zhang, Yang Yue, Rui Shi, Chenxi Sun,
                                                                   Fuzheng Zhang, Guorui Zhou, Kun Gai

                                                                                     Klear Team, Kuaishou Technology
arXiv:2507.08649v1 [cs.AI] 11 Jul 2025




                                                                                                  Abstract

                                         We introduce our Leanabell-Prover-V2, a 7B large language models (LLMs) that can pro-
                                         duce formal theorem proofs in Lean 4, with verifier-integrated Long Chain-of-Thoughts (CoT).
                                         Following our previous work Leanabell-Prover-V1, we continual to choose to posttrain
                                         existing strong prover models for further performance improvement. In our V2 version, we
                                         mainly upgrade the Reinforcement Learning (RL) with feedback provided by the Lean 4 verifier.
                                         Crucially, verifier feedback, such as indicating success or detailing specific errors, allows the
                                         LLM to become “self-aware” of the correctness of its own reasoning process and learn to reflex-
                                         ively correct errors. Leanabell-Prover-V2 directly optimizes LLM reasoning trajectories
                                         with multi-turn verifier interactions, together with feedback token masking for stable RL train-
                                         ing and a simple reward strategy. Experiments show that Leanabell-Prover-V2 improves
                                         performance by 3.2% (pass@128) with Kimina-Prover-Preview-Distill-7B and 2.0% (pass@128)
                                         with DeepSeek-Prover-V2-7B on the MiniF2F test set. The source codes, curated data and
                                         models are available at: https://github.com/Leanabell-LM/Leanabell-Prover-V2.


                                                                                                  Baseline   +RL (Ours)
                                                                            80.0
                                                                                                                          78.2
                                                                            77.5
                                                         Passing Rate (%)




                                                                                                                   76.2
                                                                            75.0
                                                                            72.5
                                                                                           70.4
                                                                            70.0
                                                                            67.5    67.2

                                                                            65.0
                                                                               Kimina-Prover-Preview-           DeepSeek-Prover-
                                                                                     Distill-7B                      V2-7B

                                         Figure 1 | Benchmark performance on MiniF2F-test (Zheng et al., 2021). Our method boosts both
                                         the two baseline models after employing RL training. Our framework surpasses Kimina-Prover-
                                         Preview-Distill-7B and DeepSeek-Prover-V2-7B 3.2% and 2.0% at pass@128, respectively.


                                         ♥ Corresponding author.
1. Introduction
Formal reasoning offers powerful techniques for verifying the correctness of complex mathemati-
cal theorems, providing a level of assurance unattainable through traditional testing alone (Huth
and Ryan, 2004). Interactive Theorem Provers (ITPs) like Coq (Coq, 1996), Isabelle/HOL (Nip-
kow et al., 2002), and Lean (De Moura et al., 2015; Moura and Ullrich, 2021) are cornerstone
tools in this domain, enabling mathematicians and engineers to construct machine-checkable
proofs. However, the process of formalization and proof construction often requires significant
expertise and manual effort, creating a bottleneck for wider adoption.
    The advent of reasoning capabilities in Large Language Models (LLMs) has revolutionized
many fields, particularly in the field of informal mathematical reasoning (Guo et al., 2025;
Anthropic, 2025; Team, 2025). Inspired by this, our prior work (Zhang et al., 2025) leverages
reinforcement learning (RL) with verified rewards (e.g., Lean 4 verifier feedback) to foster
reasoning processes exhibiting variable cognitive behaviors, thus automating or assisting in
formal proof generation. Kimina-Prover-Preview (Wang et al., 2025) consolidates this procedure
through a distinct reasoning pattern composed of consecutive blocks integrating informal
reasoning steps and Lean 4 code snippets. DeepSeek-Prover-V2 (Ren et al., 2025) further
develops a thinking pattern suitable for complex theorems through subgoal decomposition.
    However, a critical challenge persists: the sample efficiency in formal reasoning still lags
behind that of informal reasoning models. Formal reasoning models are often evaluated by a
large sampling budget (pass@k, k=32→1024) demands prohibitively large sampling budgets.
Meanwhile, practical RL training rarely exceeds 8–32 rollouts due to computational constraints
and training efficiency. Consequently, effective RL training requires an exceptionally capable
LLM backbone that can operate within constrained sampling budgets and maintain reward
diversity in the rollouts. This necessity is reflected in Kimina-Prover-Preview and DeepSeek-
Prover-V2, which employ the Qwen-2.5-72B (Team, 2024) and DeepSeek-Prover-V2-671B (Ren
et al., 2025) models respectively for RL training. However, smaller and weaker LLMs (such
as those in 7B sizes) generally lack the capacity to satisfy this requirement under standard RL
training configurations.
    In this work, we aim to enhance the formal reasoning performance of small-size LLMs.
We observe that these small-size models often fail to generate high-quality reasoning steps or
corresponding Lean 4 codes with sufficient reliability in a small sampling budget. To address
this limitation, we integrate the Lean 4 code execution as a service use through an instant,
multi-turn interaction paradigm. Our reasoning process may involves consecutive verification
feedback from the formal system itself to iteratively refine outputs. Specifically, whenever
the model generates a Lean 4 snippet—whether within an intermediate reasoning chain or as
part of the final solution—we immediately execute and verify it using the Lean 4 verifier. The
resulting feedback, which ranges from successful proof-state advancement to type errors or
tactic failures, is translated into reward signals that either guide subsequent reasoning steps or
directly compute policy gradients. We train our model with this verifier integrated reasoning
pattern end-to-end via RL (e.g., DAPO (Yu et al., 2025)), effectively guiding the policy to prefer
actions that lead to verifiable proof steps and to avoid those that result in errors.
   Our experiments show that verifier-integrated long chain-of-thought reasoning significantly
enhances the model’s capabilities in formal theorem proving. The resulting Leanabell-Prover-V2
model with 7B parameters establishes a new state-of-the-art in neural theorem proving with a
small-size LLM across multiple benchmarks. On MiniF2F-test, it achieves 78.2% accuracy on
pass@128, surpassing the DeepSeek-Prover-V2-7B (CoT) by a margin of 2%. The model demon-


                                                2
strates strong generalization capabilities to college-level theorem proving, achieving a 6.4%
improvement over the Kimina-Prover-Preview-Distill-7B baseline at pass@128 on ProofNet-test
problems. While Leanabell-Prover-V2 does not exceed DeepSeek-Prover-V2-7B’s overall perfor-
mance on ProverBench, it successfully solves one additional AIME 24&25 problem, indicating
the potential for complex mathematical reasoning tasks.


2. Method

2.1. Problem Formulation

A recent trend involves empowering LLMs to use external tools to overcome their intrinsic
limitations (e.g., performing calculations, accessing real-time information, executing code) (Parisi
et al., 2022; Schick et al., 2023; Yao et al., 2023; Shinn et al., 2023; Patil et al., 2024; Dong et al.,
2024; Ziegenbein et al., 2024; Jin et al., 2025; Song et al., 2025; Wang et al., 2025; Feng et al., 2025;
Qian et al., 2025). These approaches often use RL or sophisticated prompting strategies to learn
tool-using policies. Our work falls squarely within this paradigm. We conceptualize the Lean 4
verifier as a specialized tool that the LLM learns to interact with. The “strategy” the LLM learns
via RL is how to generate proof steps that are acceptable to this verification tool. Unlike general-
purpose tool use, our tool (i.e., Lean 4 verifier) provides highly structured, state-dependent
feedback directly related to the core reasoning task, allowing for a tight feedback loop focused
on logical validity and enabling the model to learn self-correction capabilities for formal proofs.
   We first formulate the problem of verifier-integrated theorem proving. Given an LLM-based
theorem proving model M𝜃 and a formal theorem statement 𝑠 ∈ S, where 𝜃 refers to the model
parameters, we can sample a set of generated proofs P = M𝜃 ( 𝑠) = { 𝑝1 , 𝑝2 , · · · , 𝑝𝑁 }. After feeding
these generated proofs to the Lean 4 verifier, we can obtain the corresponding correctness labels
Y = { 𝑦1 , 𝑦2 , · · · , 𝑦𝑁 } where 𝑦𝑖 ∈ {0, 1}. Then, we denote O = { 𝑜1 , 𝑜2 , · · · , 𝑜𝑁 } as the corresponding
feedbacks from the Lean4 verifier for the generated proofs. We optimize M𝜃 by maximize the
conditional probability:
                                              max E𝑠∼S, 𝑝𝑖 ∼P 𝑃 ( 𝑦𝑖 = 1)                                      (1)
                                               𝜃

where 𝑦𝑖 = 1( 𝑝𝑖 | 𝑠), and 1(·) refers to an indicator function that represents whether the generated
proof 𝑝𝑖 can pass verification by the Lean 4 verifier, given the formal theorem statement 𝑠.
    When we introduce verifier-integrated procedure during the long CoT process and provide
validation feedback to the model, the optimization process becomes:

                                        max E𝑠∼S, 𝑝𝑖 ∼P,𝑜𝑖 ∼O 𝑃 ( 𝑦ˆ𝑖 = 1)                                    (2)
                                           𝜃

where 𝑦ˆ𝑖 = 1( 𝑝ˆ 𝑖 | 𝑝𝑖 , 𝑜𝑖 , 𝑠), and 𝑝ˆ 𝑖 is the rewritten version of 𝑝𝑖 according to the validation feedback
𝑜𝑖 . Therefore, compared to the optimization objective Eq. (1), the focus here is on enabling
the model to learn how to correct erroneously generated proofs after invoking Lean 4 verifier
to obtain feedback, which better demonstrates the model’s reflection and error-correction
capabilities.


2.2. Cold-start for Verifier-integrated Theorem Proving Generation

Cold-start Data. In order to equip the model with the ability to generate formatted Chain-
of-thought (CoT) outputs for verifeir calling, we construct specially styled long CoT data for
cold-start training. In the long CoT data, we employ special markers (e.g., <code></code>,
<interpreter></interpreter>) to explicitly delineate the generated Lean 4 code blocks

                                                        3
and verifier invocation triggers, and verifier feedback information. Figure 2 shows an example
prompt for verifier-integrated theorem proving.
                           Prompt for Verifier-integrated Theorem Proving
  Think step by step and solve the following problem in Lean 4. When you think you’ve
  come up with the final answer, put your Lean 4 code in <code> and </code>. The code
  will be compiled in the Lean 4 compiler. The compilation results will be placed between
  <interpreter> and </interpreter>. Then, revise your answer based on the compilation log and
  provide the final Lean 4 code.

  # Problem: Calculate the value of 115 − 5 · 114 + 10 · 113 − 10 · 112 + 5 · 11 − 1.   The answer is 100000.
  # Formal statement:


  ‘‘‘lean4
  import Mathlib
  import Aesop
  set_option maxHeartbeats 0
  open BigOperators Real Nat Topology Rat

  /-- Calculate the value of 115 − 5 · 114 + 10 · 113 − 10 · 112 + 5 · 11 − 1. Show that it
     is 100000.-/

  theorem my_favorite_theorem : 11^5 - 5 * 11^4 + 10 * 11^3 - 10 * 11^2 + 5
      * 11 - 1 = 100000 := by
  ’’’



Figure 2 | Prompt for verifier-integrated theorem proving, where we encourage the model
employ Lean 4 verifier to verify the correctness of the generated proofs.

   There are four main steps during the automatic construction of the cold-start data:

   • Straightforward Proof Generation. For an input theorem statement, we leverage the existing
     prover LLMs (e.g., Kimina-Prover-distilled-7B (Wang et al., 2025) and DeepSeek-Prover-
     V2-distilled-7B (Ren et al., 2025)) to collect multiple generated proofs.
   • Proof Validation. We employ the Lean 4 verifier to strictly verify the generated proofs and
     filter out incorrect proofs that fail validation.
   • Automatic Correction. Given the incorrect proofs and their corresponding errors provided
     by the Lean 4 verifier, we design a special prompt (See Figure 7 in Appendix A) to ask the
     Claude-3.7-Sonnet (Anthropic, 2025) to rewrite the proofs.
   • Re-verification. We perform the Lean verification again on the rewritten results. Once we
     obtain rewritten proofs that pass verification, we successfully construct a set of high-quality
     training data in the form of “incorrect-corrected” pairs.

    After collecting the “incorrect-corrected” pairs, we consider four scenarios to synthesize data
with long CoTs, as shown in Figure 3, aiming to achieve two goals: on one hand, enabling the
model to explicitly output the thinking process before generating proofs, and on the other hand,
when verifying generated proof failed, combining verification feedback information to learn to
reflect and correct the generated results. Here are the four scenarios:

   • For the case “ 𝑝𝑖 failed but 𝑝ˆ 𝑖 success”, we take the formal statement 𝑠 as input, concatenate
     the long COT and original proof 𝑝𝑖 with the rewritten 𝑝ˆ 𝑖 as the output. In this scenario, we
     collect around 2K samples.

                                                         4
                                 Proof ��               Feedback ��        Rewritten Proof ��
                Formal          Long CoT +                Verifier           Long COT +
              Statement s


        ①        ...                ...                      ...                  ...
        ②        ...                ...                      ...                  ...
                                                                               Proof ��

        ③        ...                ...                      ...                  ...
        ④        ...                ...                      ...                  ...

                Input Prompt                 Supervision in SFT       Feedback Token Masking


Figure 3 | Overview of four scenarios to cold start data synthesis.



   • For the case “ 𝑝𝑖 failed but 𝑝ˆ 𝑖 success”, we concatenate the formal statement 𝑠 with the
     long CoT and the original proof 𝑝𝑖 as input, regard the rewritten 𝑝ˆ 𝑖 as the output. In this
     scenario, we obtain around 2K samples.
   • For the case “ 𝑝𝑖 success”, we use the formal statement 𝑠 as input, and regard the long CoT
     and the original proof 𝑝𝑖 as output. In this scenario, we collect around 2K samples.
   • For the case “ 𝑝𝑖 success”, we use the formal statement 𝑠 and the long CoT as input, and
     the original proof 𝑝𝑖 as output. In this scenario, we collect around 1K samples.

We refer the reader to Figure 8 in Appendix for additional details on the used prompt for the
first two scenarios. Since in the latter two scenarios, we can directly obtain results with long CoT
through concatenation methods, there is no need for special prompts for generation. Finally, we
collect cold-start data for Kimina-Prover-Preview-Distill-7B (Wang et al., 2025) and DeepSeek-
Prover-V2-7B (Ren et al., 2025) respectively. All of these samples are either “incorrect-to-correct”
data or “correct” data with synthesized long CoTs.
Feedback Token Masking. Given that Lean 4 verification information is not generated by the
model itself, we apply a feedback token masking strategy that focuses solely on predicting the
rewritten portions, thereby reducing potential interference during the supervised fine-tuning
(SFT) stage. As shown in Figure 3, we mask the token sequences provided by the Lean 4 verifier
in the four scenarios of the synthesized cold-start data.
Training Setup. We employ two existing powerful models as our baselines, including Kimina-
Prover-Preview-Distill-7B (Wang et al., 2025) and DeepSeek-Prover-V2-7B (Ren et al., 2025).
These two models are not able to utilize Lean 4 verifier to correct the generated proofs within
the long CoTs. During the cold-start SFT training, we set the batch size to 128, the learning rate
to 2e-5, and trained for three epochs. After this lightweight training, we examine the format
of the model’s output and find that the model already satisfy the corresponding formatting
requirements. This indicates that the cold start training process is sufficient.


2.3. Verifier-integrated Theorem Proving via Reinforcement Learning

We integrate Reinforcement Learning (RL) with the Lean 4 theorem prover and Lean 4 verifier
to automate the generation and correction of formal proofs. The RL agent interacts with the

                                                    5
                                                          Reflextion Prompt
                                         Think step by step and solve the following problem in Lean 4.
                                         ...
                                         <think>
                                         # Solving the Number Theory Problem in Lean 4
                                         I'm going to solve the problem:
                                         ...
                                         <code> ... </code>
                                         <interpreter>Compilation failed. Find an error at line 12
                                         no goal to be solved</interpreter>
                                                                                                                       Verfier Feedback



                                                                                                                                             �failed
                                                                                                                      Compilation failed.
                                                                                                                      Find an error at
                                                             Long CoT w/
                                                                                                                      line 12
     Input Prompt                                           Generated Proof                                           no goals to be
  Think step by step and                                  <think>                                                     solved
  solve the following                                     # Solving the Number
  problem in Lean 4.
                                                          Theory Problem in Lean
  ...
                                                          4
  theorem ABC {n : ℕ} :                                   I'm going to solve the
  ∃ m, n^2 ≡ m^2 [MOD                                     problem:
                           LLM-based Prover                                                                            Verfier Feedback

                                                                                                                                             �success
  16] := by                                               ...                                       Lean 4 Verifier
                                                          <code> ... </code>

                                                                                                                      Compilation Success.




                                                            Whole Long CoT
                                         <think>
                                         # Solving the Number Theory Problem in Lean 4
                                         I'm going to solve the problem:
                                         ...
                                         <code> ... </code>
                                         <interpreter>Compilation Success.</interpreter>
                                         </think>
                                         ```lean4
                                         ...
                                         ```




Figure 4 | Overview of our proposed verifier-integrated theorem proving framework.



Lean 4 environment, generating whole proofs and receiving feedback from Lean 4 verifier as
reward signals.
RL Framework. As shown in Figure 4, we first provide the formal statement 𝑠 that needs to
be solved and the format requirements for the solving process as input prompt to the LLM-
based prover. The prover model, after cold-start training, can generate long CoT reasoning
according to the requirements, and provide an initial proof within the long CoT, placing it
between <code></code> delimiters. When the generated initial proof is input to the Lean 4
verifier, there are two possible feedback results: compilation success or compilation failure.
    For cases where compilation is successful, we can return the proof from the already generated
long CoT as the correct result. However, for compilation failed cases, we need to place the
compilation error information between <interpreter></interpreter> delimiters, then
concatenate it with the previous round’s long COT to serve as a reflection prompt for the
prover model, acting as input for a new round regeneration. Additionally, we will calculate and
provide rewards 𝑅success and 𝑅failed respectively in the RL training process, based on whether
the compilation is correct or incorrect.
Policy Optimization Algorithm. We employ the recent DAPO (Yu et al., 2025) as our RL
algorithm, which has been proven to be highly effective on solving several important issues such
as entropy collapse, reward noise, and training instability. DAPO samples a group of output
proofs { 𝑝𝑖 }𝐺𝑖=1 for each formal statement 𝑠, and optimizes the policy for formal proof generation




                                                                         6
via the following objective:
        JDAPO ( 𝜃) = E𝑠∼S,{ 𝑝𝑖 } 𝐺 ∼𝜋𝜃 (· | 𝑞 )
                                 𝑖=1    old
                                         | 𝑝𝑖 |
                     "                𝐺
                                                                                                                   #
                          1         ∑︁ ∑︁                                                                 
                       Í𝐺                       min 𝑟𝑖,𝑡 ( 𝜃) 𝐴ˆ 𝑖,𝑡 , clip 𝑟𝑖,𝑡 ( 𝜃), 1 − 𝜀low , 1 + 𝜀high 𝐴ˆ 𝑖,𝑡     (3)
                        𝑖=1 | 𝑝 𝑖 |  𝑖=1 𝑡 =1

                   s.t.    0 < { 𝑝𝑖 | is_valid ( 𝑝𝑖 )} < 𝐺 ,

where is_valid() refers to the validation status provided by the Lean4 verifier, 𝜀low and 𝜀high
denote the lower and upper clipping ratios, empirically set to 0.2 and 0.28, respectively. 𝑟𝑖,𝑡 and
𝐴ˆ 𝑖,𝑡 are formulated respectively as follows:

                                         𝜋𝜃 ( 𝑝𝑖,𝑡 | 𝑞, 𝑝𝑖,<𝑡 )                        𝑅 𝑖 − mean({ 𝑅 𝑖 }𝐺𝑖=1 )
                          𝑟𝑖,𝑡 ( 𝜃) =                               ,       𝐴ˆ 𝑖,𝑡 =                              .    (4)
                                        𝜋𝜃old ( 𝑝𝑖,𝑡 | 𝑞, 𝑝𝑖,<𝑡 )                          std({ 𝑅 𝑖 }𝐺𝑖=1 )
Notably, 𝑅 𝑖 refers to the reward for the output proof 𝑝𝑖 . During our training, we remain the
strategies used in the original DAPO algorithm, inlcuding clip-higher, and token-level policy
gradient loss. Similar to the cold-start fine-tuning, we also mask the token sequences provied by
the Lean 4 verifier for stable RL training.
Reward Design. In our experiments, we primarily use two rewards: format reward (i.e., 𝑅format )
and compilation status reward (i.e., 𝑅failed and 𝑅success ). The 𝑅format is set to a smaller value (such
as 0.2) compared to 𝑅failed /𝑅success (such as 1.0). For assessing the generated proof quality, we
find that employing the simple 𝑅failed and 𝑅success are sufficient for the efficient RL training.
Based on the detailed verification feedback obtained, we can construct a structured reward
signal. As shown in the Appendix B, we have investigated such method, unfortunately, we have
not obtained favorable results. This leaves behind a crucial question: whether we can design
elaborate rewards based on Abstract Syntax Tree (AST) feedback (See Figure 9 in Appendix) to
help models learn effective reflection capabilities in RL training.
Training Setup. We use NuminaMath (Li et al., 2024) as source to collect the RL training data.
We translate the natural language math problems into formal statements by utilizing the public
Kimina-Autoformalizer-7B (Wang et al., 2025). For each formal statement, we use the supervised
finetuned model, initialized with the cold-start data, to generate multiple proof candidates
and compute the pass rate (i.e., pass@8). Subsequently, we select formal statements achieving
pass rates in the range of 1/8 to 1/2 to constitute our training dataset. For the Kimina-Prover-
Distill-7B (Wang et al., 2025) model, this filtering process results in a curated training dataset of
3.8K valid formal statements. Training hyperparameters are configured as follows: maximum
token length = 16K, batch size = 128, rollout size = 24, learning rate = 1e-6, and temperature
= 0.6. Similarly, for the DeepSeek-Prover-V2-7B (Ren et al., 2025), this filtering process results
in a curated training dataset of 1.7K valid formal statements. Training hyperparameters are
configured as follows: maximum token length = 16K, batch size = 128, rollout size = 24, learning
rate = 1e-6, and temperature = 0.7.


3. Experimental Results
In this section, we present the main experimental results after the SFT and RL stages with
the two baseline models, including Kimina-Prover-Preview-Distill-7B (Wang et al., 2025) and
DeepSeek-Prover-V2-7B (Ren et al., 2025). All experimental results are conducted with Lean
4.9.0, using the same testing environment as the DeepSeek Prover series (Xin et al., 2024; Ren
et al., 2025).

                                                                        7
                         ×104                                                      0.8                                                             1.00
                  1.20
                  1.12                                                             0.6                                                             0.95
                  1.04                                                                                                                             0.90




                                                                                                                               Verifier Use Rate
Response Length




                                                              Reward Score
                  0.96                                                             0.4                                                             0.85
                  0.88
                                                                                   0.2                                                             0.80
                  0.80
                  0.72                                                                                                                             0.75
                                                                                   0.0
                  0.64                                                                                                                             0.70
                  0.56                                                             0.2                                                             0.65
                          0     20   40     60     80   100                                  0   20   40     60     80   100                              0   20   40     60     80   100
                                     Training Step                                                    Training Step                                                Training Step
                                                                                        ×10 1
                  0.4                                                             8.5                                                              0.20
                                                                                  8.0                                                              0.18
                                                                                  7.5
                                                              Test Score avg@32
                  0.3                                                                                                                              0.16
Solve All Ratio




                                                                                  7.0                                                              0.14




                                                                                                                               Entropy
                  0.2                                                             6.5
                                                                                                                                                   0.12
                                                                                  6.0
                                                                                                                                                   0.10
                  0.1                                                             5.5
                                                                                  5.0                                                              0.08
                  0.0                                                             4.5                                                              0.06
                         0      20   40     60     80   100                              0       20   40     60     80   100                              0   20   40     60     80   100
                                     Training Step                                                    Training Step                                                Training Step


 Figure 5 | Several core records in the RL training with DeepSeek-Prover-V2-7B model, including
 Response Length, Reward Score, Verifier Use Rate, Solve All Ratio, Test Score avg@32, and Entropy.


    In Figure 5, we present the RL training records on the DeepSeek-Prover-V2-7B model. We
can see that the response length shows a slight increase as training steps progress, which is
related to the token-level loss introduced by DAPO (Yu et al., 2025), and this aligns with the
official experimental observations. Looking at the two charts showing reward score and solve all
ratio together, we find that the model continuously receives more positive rewards during the
training, with an increasing number of “solve all” problems appearing in the training set. This
indicates that the RL training scheme has improved the model’s problem-solving capabilities.
The averaged test score at pass@32 with our validation set, which is a small subset sampled
from our training data, also shows an upward trend, reflecting that the training is effective. In
addtion, since we encourage the model to use verifier validation in the training prompts, the
“verifier use rate” shows an upward trend during the training process, and after brief training,
almost all problems utilize verifier validation. Finally, during the training process, entropy
shows a slow declining trend without the occurrence of entropy collapse. For a comparison, we
refer the authors to the Appendix C for more details, where we provide the training records with
a GRPO (Shao et al., 2024) algorithm that uses a different token-level loss calculation strategy.
    As shown in Figure 12 and Figure 13 in the Appendix D, we present an example that
 our proposed verifier-integrated long CoT reasoning helps the model to correct the errors in
 the generated proof. In the following part of this section, we present detailed quantitative
 comparison results over multiple benchmarks.

 3.1. Results on MiniF2F Benchmark

Main Results. We first validate the effectiveness of our proposed method on the most commonly-
used MiniF2F-test (Zheng et al., 2021) benchmark. We have two versions of our models post-
trained from two strong prover models: Kimina-Prover-Preview-Distill-7B and Deepseek-Prover-
V2-7B, namely Leanabell-Prover-V2-KM and Leanabell-Prover-V2-DS. We mainly compare
current whole proof generation methods, while ignore those with proof-step methods using

                                                                                                        8
far more inference-compute. As shown in Table 1, our posttraining framework boosts both
Kimina-Prover-Preview-Distill-7B and DeepSeek-Prover-V2-7B models. First, our method boosts
the baseline Kimina-Prover-Preview-Distill-7B by a large margin of 5.3% (pass@32). Remark-
ably, we reach equivalent performance levels, where our method with pass@128 achieves the
comparable performance as the baseline with pass@1024 (i.e., 70.4% v.s. 70.8%), demonstrating
considerable inference efficiency gains. Meanwhile, we obatain a 1% improvement over the
baseline DeepSeek-Prover-V2-7B at pass@32, with the advantage growing larger as the sample
budget increases, ultimately achieving a 2% improvement over the baseline at pass@128.
RL Ablation. In Table 2, we discover that our proposed verifier-integrated reasoning method
yields benefits on both base models Kimina-Prover-Preview-Distill-7B and DeepSeek-Prover-V2-
7B. Furthermore, the improvements are more substantial compared to employing the vanilla
RL method that explores on all plain text CoTs. First, we observe that applying the vanilla
RL method on Kimina-Prover-Preview-Distill-7B yields 2.4% improvement, while our verifier-
integrated RL method achieves a significant 5.3% improvement at pass@32. Second, we discover
that the vanilla RL method achieves no gain on DeepSeek-Prover-V2-7B, while our method can
survive to obtain 1% improvement at pass@32.
    Figure 6 shows the curves of Kimina-Prover-Preview-Distill-7B and DeepSeek-Prover-V2-7B
models’ accuracy on MiniF2F-test as the sample budget varies. We can observe that since the
RL training phase uses a rollout size of 24, which is relatively close to the sample budget range
of 32-128. In this range, the pass@k curve of Kimina-Prover-Preview-Distill-7B has a steep
slope, which is more conducive to RL stimulating exploration capabilities. In contrast, the
curve of DeepSeek-Prover-V2-7B has a flat slope in this range, the exploration capability it can
stimulate is limited. We analyze that this is because DeepSeek-Prover-V2-7B is obtained through
comprehensive large model distillation and subsequent RL enhancement. The previous RL
training has already substantially activated the model’s problem-solving abilities, making it
very challenging to achieve significant gains through an additional RL training.

                                          80
                                                 rollout=24

                                          75
              MiniF2F-test Accuracy (%)




                                          70


                                          65


                                          60


                                          55                  DeepSeek-Prover-V2-7B
                                                              Kimina-Prover-Preview-Distill-7B
                                               1 32    128                                       1024
                                                                  Sample Budget

Figure 6 | The curves of Kimina-Prover-Preview-Distill-7B and DeepSeek-Prover-V2-7B models’
accuracy on MiniF2F-test as the sample budget varies.


On the Verifier Calling Iteration. Although we train the model to perform verifier feedback-
based reflection only once per long CoT during training, in practice, we can verify after each
generated <code></code> block in the long CoT and have the model reflect iteratively until it

                                                                       9
produces correct proofs or hits the maximum iteration threshold. In Table 3, we demonstrate
the effectiveness of verifier calling iteration cycles, finding that the gains are quite significant
during the first round of reflective modifications based on the validation feedback. For example,
Leanabell-Prover-V2-KM improves from 64.7% to 68.4% (i.e., an increase of 3.7%), and Leanabell-
Prover-V2-DS improves from 75.4% to 76.6% (i.e., an increase of 1.2%). When continuously
increasing the iteration cycles from 1 to 3, we can also achieve an improvement by a margin
of 0.8%. The results indicate promissing potential, suggesting Leanabell-Prover-V2-KM may
achieve additional gains with more increased iterations. Unfortunately, we do not observe
improvements on Leanabell-Prover-V2-DS.
    In addition, we have explored to increase the rollout size in each iteration cycle (i.e., expand-
ing into a tree-like branching structure). For example, when the rollout size is increased from
1 to 4 within an iteration cycle, we can achieve a slight improvement of 0.4% (i.e., 68.4% →
68.8%) with Leanabell-Prover-V2-KM. Similarly, we do not obtain improvements with Leanabell-
Prover-V2-DS. Limited by computational resource constraints, we do not evaluate larger “#”
values. Nevertheless, results from Leanabell-Prover-V2-KM indicate promising potential for
additional performance gains via increased tree branching width.

3.2. Results on Undergraduate-level Benchmarks

ProofNet (Azerbayev et al., 2023) consists of 371 problems in Lean 3, drawn from a range of
popular undergraduate pure mathematics textbooks. Similar to DeepSeek-Prover-V2 (Ren et al.,
2025), we use the Lean 4 translation of ProofNet made available in DeepSeek-Prover-V1.5 (Xin
et al., 2024). We employ ProofNet-test for model evaluation, which contains 186 problems. As
shown in Table 4, after applying our verifier-integrated reasoning method on Kimina-Prover-
Preview-Distill-7B, we surpass the performance of the base model at pass@128 when using
pass@32, reaching 13.4%. Compared to Kimina-Prover-Preview-Distill-7B, Leanabell-Prover-
V2-KM achieves an obvious improvement by a margin of 6.4% at pass@128. However, on
DeepSeek-Prover-V2-7B, we only achieved comparable results without significant performance
improvement (Please see our RL discussion in Section 3.1).

3.3. Results on ProverBench Benchmark

ProverBench (Ren et al., 2025) is a benchmark dataset comprising 325 formal statements that are
formalized from the recent AIME competitions (i.e., AIME 24 and 25), and textbook examples and
educational tutorials. This benchmark is designed to enable more comprehensive evaluation
across both high-school competition problems and undergraduate-level mathematics. The
evaluation results are presented in Table 5. With Kimina-Prover-Preview-Distill-7B as the
base model, our Leanabell-Prover-V2-KM achieves obvious improvements by margins of 9.6%
and 8.1% at pass@32 and pass@128, respectively. Similar to Kimina-Prover-Preview-Distill-7B,
Leanabell-Prover-V2-KM does not achieve improved performance on AIME 24&25 problems.
With DeepSeek-Prover-V2-7B as the base model, our Leanabell-Prover-V2-DS exhibits marginally
lower performance than the base model across the entire dataset. However, we observe with
surprise that it correctly solved one additional problem set among the more challenging AIME
24&25 problems.


4. Conclusion, Limitation, and Future Work
In this work, we have presented a novel method to addresses the critical limitation of small
LLMs in generating reliable formal proofs by leveraging instant verification feedback within

                                                 10
          Method                                       Sample budget   MiniF2F-test
          TheoremLlama [31]                                 128           33.6%
          DeepSeek-Prover-v1 [32]                           128        46.1% ± 0.5%
                                                           128         29.7% ± 0.5%
          DeepSeek-Prover-v1.5-Base [33]                   3200            39.2%
                                                           6400            42.2%
                                                            32         48.2% ± 0.6%
                                                            64         49.6% ± 0.7%
          DeepSeek-Prover-v1.5-SFT [33]
                                                           128         50.4% ± 0.4%
                                                           3200        53.3% ± 0.5%
                                                            32         50.0% ± 0.5%
                                                            64         50.7% ± 0.4%
          DeepSeek-Prover-v1.5-RL [33]
                                                           128         51.6% ± 0.5%
                                                           3200        54.9% ± 0.7%
                                                           128         57.7% ± 0.6%
          STP [8]
                                                           3200        61.7% ± 0.6%
                                                            32         57.6% ± 0.7%
          Goedel-Prover-SFT [14]
                                                           3200            62.7%
                                                             32           59.8%
          Leanabell-Prover-GD-RL [37]                        64           60.7%
                                                            128           61.1%
                                                            32            63.1%
          Kimina-Prover-Preview-Distill-7B [30]            128            67.2%
                                                           1024           70.8%
                                                            32         75.6% ± 0.5%
          DeepSeek-Prover-V2-7B (CoT) [20]                 128             76.2%
                                                           1024        79.9% ± 0.3%
                                                             32           68.4%
          Leanabell-Prover-V2-KM (Ours)
                                                            128           70.4%
                                                             32           76.6%
          Leanabell-Prover-V2-DS (Ours)
                                                            128           78.2%

Table 1 | Comparison with state-of-the-art methods on the miniF2F-test dataset. The notation
𝜇 ± 𝜎 denotes the average accuracy 𝜇 and the standard deviation 𝜎. “KM” and “DS” refer to
using the Kimina-Prover-Preview-Distill-7B and DeepSeek-Prover-V2-7B as base models. Our
proposed method employs a rollout size of 1 for subsequent Lean 4 verifier calling iteration
cycles.




                                                  11
   Method                                                      Sample budgets            MiniF2F-test
   Kimina-Prover-Preview-Distill-7B (Wang et al., 2025)                                     63.1%
     + Vanilla RL                                                      32                   65.5%
     + Our RL                                                                               68.4%
   DeepSeek-Prover-V2-7B (Ren et al., 2025)                                                 75.6%
    + Vanilla RL                                                       32                   75.6%
    + Our RL                                                                                76.6%

Table 2 | Comparison between direct RL method (i.e., without using validation feedback infor-
mation) and our proposed verifier-integrated reasoning method. For a fair comparison, both
policy optimization algorithm and reward are with the same configurations.




                                                                               Iterations
    Method                                Sample budgets
                                                                       1           2            3
                                              32 (Vanilla)        64.7%             -            -
    Leanabell-Prover-V2-KM (Ours)                 32-1            68.4%          68.8%        69.2%
                                                  32-4            68.8%             -            -
                                              32 (Vanilla)        75.4%             -            -
    Leanabell-Prover-V2-DS (Ours)                 32-1            76.6%          76.6%        76.6%
                                                  32-4            76.6%             -            -

Table 3 | Evaluation across diverse budget configurations and Lean 4 verifier calling iteration
cycles on MiniF2F-test. “32-#" refers to 32 rollouts in the first round, followed by # rollouts in
each subsequent Lean 4 verifier calling iteration. “Vanilla” refers to evaluating the generated
proof in the first <code></code> block in the long CoTs.




                                                       Model   Sample
            Method                                                          ProofNet-test
                                                        size   budget
            Goedel-Prover-SFT [14]                      7B       32            15.6%
                                                                  32           10.3%
            Kimina-Prover-Preview-Distill-7B [30]       7B
                                                                 128           11.8%
                                                                  32        23.0% ± 0.4%
            DeepSeek-Prover-V2-7B    (CoT) [20]         7B
                                                                 128        25.4% ± 0.7%
                                                                  32           13.4%
            Leanabell-Prover-V2-KM (Ours)               7B
                                                                 128           18.2%
                                                                  32           23.7%
            Leanabell-Prover-V2-DS (Ours)               7B
                                                                 128           25.2%

Table 4 | The experimental results on ProofNet-test.




                                                  12
                                              Model    Sample            ProverBench
      Method
                                               size     budget        All        AIME 24&25
                                                           32     27.5% ± 0.7%       0/15
      STP [8]                                   7B
                                                          128     31.4% ± 1.1%       1/15
                                                           32        30.2%           1/15
      Kimina-Prover-Preview-Distill-7B [30]     7B
                                                          128        34.8%           1/15
                                                           32     49.0% ± 0.3%       1/15
      DeepSeek-Prover-V2-7B     (CoT) [20]      7B
                                                          128     50.8% ± 0.5%       1/15
                                                           32        39.8%           1/15
      Leanabell-Prover-V2-KM (Ours)             7B
                                                          128        42.9%           1/15
                                                           32        47.8%           1/15
      Leanabell-Prover-V2-DS (Ours)             7B
                                                          128        48.7%           2/15

Table 5 | The experimental results on ProverBench. The All category represents the complete
evaluation set consisting of 325 problems, while AIME 24&25 denotes a subset of 15 problems
formalized from recent AIME competitions. The results for STP (Dong and Ma, 2025) are
evaluated using the open-source model weights.



a multi-turn interaction framework. This enables models to learn from real-time feedback,
iteratively refining reasoning steps and developing preference for verifiable proof actions over
error-prone paths. Our contributions establish a new paradigm for theorem proving through
verifier-integrated long chain-of-thought (CoT) reasoning, and provide open access to our
framework and resources for the research community. This work represents a significant step
toward making formal reasoning capabilities more accessible and reliable in language models.
Limitations. As shown in the experimental results, we demonstrate improvements on two
SOTA prover models: Kimina-Prover-Preview-Distill-7B and DeepSeek-Prover-V2-7B. Through
in-depth analysis, we find that when the difficulty of formal statements increases to a certain
level, the potential number of active prompts for RL training decreases for two reasons: first,
the original problem set for harder levels (such as IMO) is much smaller, second we filter out
problems through pass rate (all/none solved) during training. Therefore, for very strong base
models (such as DeepSeek-Prover-V2-7B), our RL framework may suffer from limited active
training prompts used during training, making our benefit shows a diminishing trend.
Future Work. Up to this work, we have completed two exploratory studies on how to improve
models’ cognitive behaviors, including our previous work Leanabell-Prover-V1 (Zhang
et al., 2025), especially their reflection and correction capabilities. This has made us realize that
there are still the following very important problems that urgently need to be solved:

   • Subgoal decomposition via RL. DeepSeek-Prover-V2 (Ren et al., 2025) has proven that subgoal
     decomposition is an efficient method for solving complex formal problems and scaling
     synthetic data generation. We conducted experiments with prompt-based approaches for
     subgoal decomposition but observed consistently low success rates. RL-based methods
     potentially offer more promising avenues for achieving better results. However, how to
     effectively leverage RL methods to enhance subgoal decomposition efficiency remains an
     open research question.
   • Partial rollout. As to address the limitations discussed above, for solved none filtered
     problems, we can try to concatenate some hints into the prompt such as decomposed

                                                 13
     subgoals and partial proofs, and perform rollouts on the remaining reasoning and proof
     parts. A few partial rollout strategies (Bhattacharya et al., 2020; Team et al., 2025; Beck, 2025;
     Xu et al., 2025) have demonstrated great potentials in boosting RL training performance
     for difficult problems.
   • Fine-grained rewards. Based on the detailed verification feedback obtained, in theory, we can
     construct a structured reward signal. As shown in the Appendix B, we have investigated
     such methods, however, by far we have not yet obtained favorable results. Yet, we believe
     that this direction still warrants further exploration.
   • Context pruning strategy. In our verifier-integrated reasoning iteration cycles, we simply
     concatenate the history of long CoTs and feedback errors in a straightforward manner. By
     organizing and analyzing the thinking process, generated proofs, and validation feedback,
     and incorporating the useful information as context into the next iteration cycle, we can
     reduce context length, improve inference efficiency, and strengthen the model’s reflective
     performance.


References
 [1] Anthropic. Claude 3.7 Sonnet System card. 2025. URL https://www.anthropic.com/
     news/claude-3-7-sonnet.
 [2] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad. Proofnet:
     Autoformalizing and formally proving undergraduate-level mathematics. arXiv preprint
     arXiv:2302.12433, 2023.

 [3] J. Beck. Offline rlaif: Piloting vlm feedback for rl via sfo. arXiv preprint arXiv:2503.01062,
     2025.

 [4] S. Bhattacharya, S. Badyal, T. Wheeler, S. Gil, and D. Bertsekas. Reinforcement learning for
     pomdp: Partitioned rollout and policy iteration with application to autonomous sequential
     repair problems. IEEE Robotics and Automation Letters, 5(3):3967–3974, 2020.

 [5] P. Coq. The coq proof assistant-reference manual. INRIA Rocquencourt and ENS Lyon, version,
     5, 1996.

 [6] L. De Moura, S. Kong, J. Avigad, F. Van Doorn, and J. von Raumer. The Lean theorem
     prover (system description). In International Conference on Automated Deduction (CAD), 2015.

 [7] G. Dong, K. Lu, C. Li, T. Xia, B. Yu, C. Zhou, and J. Zhou. Self-play with execution feedback:
     Improving instruction-following capabilities of large language models. arXiv preprint
     arXiv:2406.13542, 2024.

 [8] K. Dong and T. Ma. Stp: Self-play llm theorem provers with iterative conjecturing and
     proving. arXiv preprint arXiv:2502.00212, 2025.

 [9] J. Feng, S. Huang, X. Qu, G. Zhang, Y. Qin, B. Zhong, C. Jiang, J. Chi, and W. Zhong. Retool:
     Reinforcement learning for strategic tool use in llms. arXiv preprint arXiv:2504.11536, 2025.

[10] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
     Deepseek-R1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv
     preprint arXiv:2501.12948, 2025.

[11] M. Huth and M. Ryan. Logic in Computer Science: Modelling and reasoning about systems.
     Cambridge university press, 2004.

                                                 14
[12] B. Jin, H. Zeng, Z. Yue, J. Yoon, S. Arik, D. Wang, H. Zamani, and J. Han. Search-r1: Training
     llms to reason and leverage search engines with reinforcement learning. arXiv preprint
     arXiv:2503.09516, 2025.

[13] J. Li, E. Beeching, L. Tunstall, B. Lipkin, R. Soletskyi, S. C. Huang, K. Rasul, L. Yu, A. Jiang,
     Z. Shen, Z. Qin, B. Dong, L. Zhou, Y. Fleureau, G. Lample, and S. Polu. Numinamath, 2024.

[14] Y. Lin, S. Tang, B. Lyu, J. Wu, H. Lin, K. Yang, J. Li, M. Xia, D. Chen, S. Arora, et al. Goedel-
     prover: A frontier model for open-source automated theorem proving. arXiv preprint
     arXiv:2502.07640, 2025.

[15] L. d. Moura and S. Ullrich. The lean 4 theorem prover and programming language. In
     International Conference on Automated Deduction, 2021.

[16] T. Nipkow, M. Wenzel, and L. C. Paulson. Isabelle/HOL: a proof assistant for higher-order logic.
     Springer, 2002.

[17] A. Parisi, Y. Zhao, and N. Fiedel. Talm: Tool augmented language models. arXiv preprint
     arXiv:2205.12255, 2022.

[18] S. G. Patil, T. Zhang, X. Wang, and J. E. Gonzalez. Gorilla: Large language model connected
     with massive apis. Advances in Neural Information Processing Systems (NeurIPS), 2024.

[19] C. Qian, E. C. Acikgoz, Q. He, H. Wang, X. Chen, D. Hakkani-Tür, G. Tur, and H. Ji. Toolrl:
     Reward is all tool learning needs. arXiv preprint arXiv:2504.13958, 2025.

[20] Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang,
     et al. Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement
     learning for subgoal decomposition. arXiv preprint arXiv:2504.21801, 2025.

[21] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer,
     N. Cancedda, and T. Scialom. Toolformer: Language models can teach themselves to use
     tools. Advances in Neural Information Processing Systems (NeurIPS), 2023.

[22] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
     Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
     arXiv preprint arXiv:2402.03300, 2024.

[23] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao. Reflexion: Language
     agents with verbal reinforcement learning. Advances in Neural Information Processing Systems
     (NeurIPS), 2023.

[24] H. Song, J. Jiang, Y. Min, J. Chen, Z. Chen, W. X. Zhao, L. Fang, and J.-R. Wen. R1-
     searcher: Incentivizing the search capability in llms via reinforcement learning. arXiv
     preprint arXiv:2503.05592, 2025.

[25] K. Team, A. Du, B. Gao, B. Xing, C. Jiang, C. Chen, C. Li, C. Xiao, C. Du, C. Liao, et al. Kimi
     k1.5: Scaling reinforcement learning with llms. arXiv preprint arXiv:2501.12599, 2025.

[26] Q. Team. Qwen2.5: A party of foundation models, September 2024. URL https://qwen
     lm.github.io/blog/qwen2.5/.
[27] Q. Team. Qwq-32b: Embracing the power of reinforcement learning, March 2025. URL
     https://qwenlm.github.io/blog/qwq-32b/.


                                                 15
[28] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings, A. Thakur, and S. Chaud-
     huri. Putnambench: Evaluating neural theorem-provers on the putnam mathematical
     competition. arXiv preprint arXiv:2407.11214, 2024.

[29] H. Wang, C. Qian, W. Zhong, X. Chen, J. Qiu, S. Huang, B. Jin, M. Wang, K.-F. Wong, and
     H. Ji. Otc: Optimal tool calls via reinforcement learning. arXiv preprint arXiv:2504.14870,
     2025.

[30] H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung, M. Vinyes, Z. Ying,
     Z. Zhu, et al. Kimina-prover preview: Towards large formal reasoning models with
     reinforcement learning. arXiv preprint arXiv:2504.11354, 2025.

[31] R. Wang, J. Zhang, Y. Jia, R. Pan, S. Diao, R. Pi, and T. Zhang. Theoremllama: Transforming
     general-purpose llms into lean4 experts. arXiv preprint arXiv:2407.03203, 2024.

[32] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan, W. Li, and X. Liang. Deepseek-
     prover: Advancing theorem proving in llms through large-scale synthetic data. arXiv
     preprint arXiv:2405.14333, 2024.

[33] H. Xin, Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu, L. Zhang, X. Lu, Q. Du, et al.
     Deepseek-prover-v1. 5: Harnessing proof assistant feedback for reinforcement learning
     and monte-carlo tree search. arXiv preprint arXiv:2408.08152, 2024.

[34] Y. E. Xu, Y. Savani, F. Fang, and Z. Kolter. Not all rollouts are useful: Down-sampling
     rollouts in llm reinforcement learning. arXiv preprint arXiv:2504.13818, 2025.

[35] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao. React: Synergizing rea-
     soning and acting in language models. In International Conference on Learning Representations
     (ICLR), 2023.

[36] Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, W. Dai, T. Fan, G. Liu, L. Liu, et al. Dapo:
     An open-source llm reinforcement learning system at scale. arXiv preprint arXiv:2503.14476,
     2025.

[37] J. Zhang, Q. Wang, X. Ji, Y. Liu, Y. Yue, F. Zhang, D. Zhang, G. Zhou, and K. Gai. Leanabell-
     prover: Posttraining scaling in formal reasoning. arXiv preprint arXiv:2504.06122, 2025.

[38] K. Zheng, J. M. Han, and S. Polu. Minif2f: a cross-system benchmark for formal olympiad-
     level mathematics. arXiv preprint arXiv:2109.00110, 2021.

[39] T. Ziegenbein, G. Skitalinskaya, A. B. Makou, and H. Wachsmuth. Llm-based rewriting of
     inappropriate argumentation using reinforcement learning from machine feedback. arXiv
     preprint arXiv:2406.03363, 2024.



A. Cold-start Details
As shown in Figure 7 and Figure 8, we present the prompts for correcting the proof errors and
synthesizing data with long CoT with Claude-Sonnet-3.7, respectively.




                                                16
                           Prompt for Correcting the Proof Errors
  You are an AI assistant proficient in using Lean 4 to solve mathematical problems. At the
  beginning, when solving a problem, you need to think step by step and generate complete
  Lean 4 code, which is then compiled in the Lean 4 environment. The Lean 4 compilation is
  executed in a sandbox environment, and the compilation results are returned. These results
  may include error logs to assist with your reasoning. Now, continue writing based on the
  original thinking process that includes the compilation results to generate an analysis and
  complete, correct Lean 4 code.

  In the original thinking process provided to you, the Lean 4 code block generated by the
  model is enclosed between <code> and </code>, while the compilation result of the Lean 4
  environment is enclosed between <interpreter> and </interpreter>.

  GOAL:
  Continue writing based on the original thinking process. Please first analyze the user’s
  question, the original thinking process, the generated Lean 4 code block, and the error
  logs, and provide the result of the error analysis. Then, present the complete Lean 4 code
  block that you think is correct. After generating the entire error analysis result, end it
  with </think>. Then generate the Lean 4 code block, starting with ‘‘‘lean4 and ending with
  ’’’.

  The output format is as follows:
  {Your analysis result}</think>
  ‘‘‘lean4
  {The revised Lean 4 code block}
  ’’’

  User Question:
  {question}

  Original Thinking Process:
  <original_thinking_process> original_response </original_thinking_process>



Figure 7 | Prompt for correcting the proof errors through Claude-3.7-Sonnet.




                                              17
                         Prompt for Synthesizing Data with Long CoT
  You are an AI assistant proficient in using Lean 4 to solve mathematical problems. At the
  beginning, when solving a problem, you need to think step by step and generate complete
  Lean 4 code, which is then compiled in the Lean 4 environment. The Lean 4 compilation is
  executed in a sandbox environment, and the compilation results are returned. These results
  may include error logs to assist with your reasoning. Now, continue writing based on the
  original thinking process that includes the compilation results to generate an analysis and
  complete, correct Lean 4 code.

  In the original thinking process provided to you, the Lean 4 code block generated by the
  model is enclosed between ‘‘‘lean4 and ’’’, while the compilation result of the Lean 4
  environment is enclosed between <compiler_results> and </compiler_results>.

  GOAL:
  Continue writing based on the original thinking process. Please first analyze the user’s
  question, the original thinking process, the generated Lean 4 code block, and the error
  logs, and provide the result of the error analysis. Then, present the complete Lean 4 code
  block that you think is correct. After generating the entire error analysis result, end it
  with </think>. Then generate the Lean 4 code block, starting with ‘‘‘lean4 and ending with
  ’’’.

  The output format is as follows:
  {{Your analysis result}}
  ‘‘‘lean4The revised Lean 4 code block’’’

  User Question:
  {question}

  Original Thinking Process:
  <original_thinking_process> {original_response} </original_thinking_process>



Figure 8 | Prompt for synthesizing data with long CoT through Claude-3.7-Sonnet.


B. On Reward Design
Besides the aforementioned validation status rewards 𝑅failed and 𝑅success , we also explore a
structured reward signal in the RL training. Although we do not obtain obvious improvements
from such structured reward signal, it can be a useful guidance for researchers who want to
explore this direction in the future. Given an input Lean 4 code and its Abstract Syntax Tree
(AST) obtained by the Lean 4 verifier, as shown in Figure 9 in Appendix, we analyze to evaluate
proof quality. We consider five main aspects for the reward design.

   • Tactic Count Reward. Tactic count measures the total number of individual proof steps,
     where fewer tactics often signal more streamlined and elegant reasoning. Given a formal
     proof 𝑝 and a function 𝐶𝑜𝑢𝑛𝑡 (·) that compute the proof steps, the tactic count reward is
     formulated as:
                                        𝑅tactic count = 𝐶𝑜𝑢𝑛𝑡 ( 𝑝)                         (5)
   • Automation Level Reward. As shown in the Figure 10, we show the different power or
     automation level of tactics. The power/automation level is associated with the frequency
     of a tactic. Automation level reward evaluates the sophistication of the proof steps
     themselves—powerful tactics like ring for algebraic manipulation, simp for simplification,
     or linarith for linear arithmetic can encapsulate complex mathematical reasoning within
     a single command, potentially replacing dozens of manual steps. For the 𝑖-th tactic in the
     proof, let 𝑣𝑖 be its power value from the pre-defined “tactic power” dictionary, as shown in




                                               18
                 Example input (i.e., between <code></code>) Lean 4 code:
import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat

/-- After moving the line 𝑦 = −3𝑥 + 5 down 3 units, the equation of the
   resulting line is ______. Show that it is y = -3x + 2.-/
theorem my_favorite_theorem (y : R → R) (h : y = fun x => -3 * x + 5) :
    ∀ x, y x - 3 = -3 * x + 2 := by
  intro x
  rw [h]
  ring

                        Corresponding AST output in JSON format:
"ast": {
    "tactics": [
         {
            "stateBefore": "y : R → R\nh : y = fun x => -3 * x + 5\n⊢ ∀ (x :
   R), y x - 3 = -3 * x + 2",
            "stateAfter": "y : R → R\nh : y = fun x => -3 * x + 5\nx : R\n⊢
   y x - 3 = -3 * x + 2",
            "pos": 342,
            "endPos": 349
         },
         {
            "stateBefore": "y : R → R\nh : y = fun x => -3 * x + 5\nx : R\n⊢
   y x - 3 = -3 * x + 2",
            "stateAfter": "y : R → R\nh : y = fun x => -3 * x + 5\nx : R\n⊢
   (fun x => -3 * x + 5) x - 3 = -3 * x + 2",
            "pos": 352,
            "endPos": 358
         },
         {
            "stateBefore": "y : R → R\nh : y = fun x => -3 * x + 5\nx : R\n⊢
   y x - 3 = -3 * x + 2",
            "stateAfter": "y : R → R\nh : y = fun x => -3 * x + 5\nx : R\n⊢
   (fun x => -3 * x + 5) x - 3 = -3 * x + 2",
            "pos": 356,
            "endPos": 357
         },
         {
            "stateBefore": "y : R → R\nh : y = fun x => -3 * x + 5\nx : R\n⊢
   (fun x => -3 * x + 5) x - 3 = -3 * x + 2",
            "stateAfter": "no goals",
            "pos": 361,
            "endPos": 364
         }
    ],
    "premises": [0],
    "declarations": [4]
}

Figure 9 | Example of feedback Abstract Syntax Tree (AST) for the generated Lean 4 code.


                                             19
                                                                 Lean Tactic Power/Automation Levels
                    1.0
                                                                                                                                         High Automation ( 0.8)
                                                                                                                                         Medium Automation (0.5-0.7)
                                                                                                                                         Low Automation (0.3-0.4)
                    0.8                                                                                                                  Very Low Automation (<0.3)
Power Level (0-1)




                    0.6


                    0.4


                    0.2


                    0.0
                                                                           m
                              g




                                                       a
                                   th

                                          th




                                                            to
                                                sop




                                                                  p



                                                                                 rw

                                                                                          e




                                                                                                                        ros
                                                                                               lc

                                                                                                        ply

                                                                                                               ses




                                                                                                                                t

                                                                                                                                    lit

                                                                                                                                              ro

                                                                                                                                                   ve

                                                                                                                                                           lt
                                                                                                                              ac
                                                      eg




                                                                                       rit
                           rin




                                                                 sim




                                                                                                                                                         fau
                                                                                              ca
                                                                        nu
                                                           tau




                                                                                                                                    sp
                                  ari

                                           ri




                                                                                                                                           int

                                                                                                                                                   ha
                                                                                                    ap




                                                                                                                              ex
                                                                                                                     int
                                                                                                              ca
                                                ae




                                                                                      rew
                                                      om
                                        na




                                                                          _




                                                                                                                                                        de
                               lin




                                                                       rm
                                     nli




                                                                   no




                                                                                        Tactics

Figure 10 | Lean 4 tactic power/automation levels.



                          Figure 10. Thus, we have:
                                                                                                         𝑛
                                                                                                   1 ∑︁
                                                                               𝑅automation =                  𝑣𝑖                                                       (6)
                                                                                                   𝑛
                                                                                                        𝑖=1

                     • State Change Efficiency Reward. It quantifies how much progress each tactic makes toward
                       the proof goal by comparing the proof state before and after each step, helping identify
                       which tactics contribute most meaningfully to the overall proof construction. For the 𝑖-th
                       tactic in a proof 𝑝 with 𝑔𝑖before goals before execution and 𝑔𝑖after goals after execution, we
                       have the state change efficiency reward:

                                                                                              𝑔𝑖after
                                                       𝑅state change = max(0, 1 −                       ),         for   𝑔𝑖before > 0                                  (7)
                                                                                               before
                                                                                              𝑔𝑖

                          Notably, 𝑔𝑖after = 0 refers to the 𝑖-th tactic solves all goals, 𝑔𝑖after = 𝑔𝑖before refers to no progress
                          made, 𝑔𝑖after > 𝑔𝑖before the 𝑖-th tactic creates more goals, and 0 < 𝑔𝑖after < 𝑔𝑖before means
                          achieving partial progress.

                     Finally, we obtain the overall reward by combining the multiple rewards:
                                     (
                                       𝑅failed                                                               if failed
                            𝑅final =                                                                                                                                   (8)
                                       𝑅success + 𝜆 𝑡𝑐 𝑅tactic count + 𝜆 𝑎𝑡 𝑅automation + 𝜆 𝑠𝑐 𝑅state change if success

where 𝜆 𝑡𝑐 , 𝜆 𝑎𝑡 and 𝜆 𝑠𝑐 are hyperparameters to control the reward strength.
   As shown in Table 6, we employ Kimina-Prover-Preview-Distill-7B as a baseline model and
vary the reward used in the RL algorithm. We find that when using 𝑅tactic count , we achieve slight
gains, but the other two rewards (i.e., 𝑅automation and 𝑅state change ) both perform slightly worse
than using the simple 𝑅failed and 𝑅success reward strategy.



                                                                                       20
                      Method                                                                                                                           Sample budgets                                 MiniF2F-test
                      Kimina-Prover-Preview-Distill-7B (Wang et al., 2025)                                                                                                                                 63.1%
                        + Success/failure reward only                                                                                                                                                      68.4%
                          w/ 𝜆 𝑡𝑐 = 1.0                                                                                                                           32                                       69.2%
                          w/ 𝜆 𝑎𝑡 = 1.0                                                                                                                                                                    68.0%
                          w/ 𝜆 𝑠𝑐 = 1.0                                                                                                                                                                    67.2%

Table 6 | Comparison between the simplest success/failure reward and our proposed fine-
grained rewards.


                  1.04 ×104                                                 ×10 1                                                         ×10 1                                              ×10 1
                                                                        2                                                           5.5                                                4.0
                  0.96                                                                                                                                                                 3.6
                                                                        1                                                           5.0
                  0.88                                                                                                                                                                 3.2
                                                                        0




                                                                                                                Test Score avg@32
                  0.80                                                                                                              4.5
Response Length




                                                                                                                                                                                       2.8
                                                         Reward Score




                                                                        1
                  0.72                                                                                                              4.0




                                                                                                                                                                             Entropy
                                                                        2                                                                                                              2.4
                  0.64                                                                                                              3.5                                                2.0
                  0.56                                                  3
                                                                        4                                                           3.0                                                1.6
                  0.48                                                                                                                                                                 1.2
                                                                        5                                                           2.5
                  0.40                                                                                                                                                                 0.8
                  0.32                                                  6                                                           2.0
                                                                                                                                                                                       0.4
                        0     25   50     75 100   125                       0      25   50     75 100   125                               0      25   50     75 100   125                    0      25   50     75 100   125
                                   Training Step                                         Training Step                                                 Training Step                                      Training Step


Figure 11 | Several core records in the RL training with GRPO (Shao et al., 2024) algorithm and
DeepSeek-Prover-V2-7B model, including Response Length, Reward Score, Test Score avg@32, and
Entropy.


 C. On RL Algorithm
In our main experiments, we follow DAPO (Yu et al., 2025) and employ a token-level loss in
the RL algorithm. We heve investigated the impact of loss aggregation strategies on model
training stability. For comparison, we have explored a sample-level loss calculation (similar to
GRPO (Shao et al., 2024)), which involves first averaging the losses by token within each sample
and then aggregating the losses across samples. However, this approach proves problematic
for this verifier-integrated reasoning task, where responses vary significantly in length and are
generally longer than in conventional reasoning scenarios. The averaging process effectively
reduces the learning signal from longer responses, as each token in these responses contributes
less to the overall loss. This reduction impairs the model’s ability to learn from the rich reasoning
patterns present in the long CoTs. As shown in Figure 11, we encounter training collapse
problems with such a sample-level loss. In contrast, the token-level loss computation employed
by DAPO maintains uniform gradient contributions across all tokens regardless of sequence
length, thereby resulting in more stable and effective training for our task.


 D. Success Example
We show an example that successfully correct the errors with our proposed verifier-integrated in
long CoT reasoning. As shown in Figure 12and Figure 13, we take our Leanabell-Prover-V2-KM
as an example, where there is an error about “type mismatch” in validation feedback at the
first round reasoning. After being informed of such errors, the model generated the correct
proof through reflective attempts. Note that due to differences in the base models themselves,
there are some differences bewteen our Leanabell-Prover-V2-KM and Leanabell-Prover-V2-DS
in reasoning style. However, this does not affect the overall reasoning process, so additional
examples will not be provided here for demonstration.


                                                                                                               21
                        Example prompt for Lean 4 code completion:
You are an expert in mathematics and Lean 4. . . .
Think step by step and solve the following problem in Lean 4. . . .

# Problem: If 𝑟 is rational ( 𝑟 ≠ 0) and 𝑥 is irrational, prove that 𝑟𝑥 is
   irrational.
# Formal statement:
‘‘‘lean4
...
theorem exercise_1_1b
(x : R)
(y : Q)
(h : y ≠ 0)
: ( Irrational x ) -> Irrational ( x * y ) := by
’’’

                   Output long CoT, Lean 4 code and validation feedback:
<think>
# Proving that the Product of a Non-Zero Rational Number and an Irrational
   Number is Irrational
To prove that if 𝑟 is a non-zero rational number and 𝑥 is irrational, then 𝑟𝑥
   is irrational, we can use the properties of rational and irrational
   numbers.
First, let’s think about why this is true. If 𝑟 is rational and non-zero, and 𝑥
    is irrational, then 𝑟𝑥 cannot be rational.
...
<code>
‘‘‘lean4
...
/-- If 𝑟 is rational ( 𝑟 ≠ 0) and 𝑥 is irrational, prove that 𝑟𝑥 is irrational.-/
theorem exercise_1_1b
(x : R)
(y : Q)
(h : y ≠ 0)
: ( Irrational x ) -> Irrational ( x * y ) := by
  intro hx
  have hy : (y : R) ≠ 0 := by exact_mod_cast h
  have h1 : Irrational (x * y) := by
     simpa using hx.mul_rat hy
  exact h1
’’’
</code>
<interpreter>
Compilation failed.\nFind an error at line 24\napplication type mismatch\n
    Irrational.mul_rat hx hy\nargument\n hy\nhas type\n ↑y ≠ 0 : Prop\nbut
    is expected to have type\n y ≠ 0 : Prop
</interpreter>

Figure 12 | Example of correcting the errors with our proposed verifier-integrated in long CoT
reasoning (Part I).




                                             22
                        Corrected proof and final validation feedback:
It seems that the Lean 4 compilation failed and returned some error logs. Let
   me check and analyze the error logs.\n\nThe error in the original code is
   related to the type mismatch in the ‘hx.mul_rat hy‘ expression. The error
   message indicates that ‘hy‘ has type ‘↑y ≠ 0 : Prop‘ but is expected to
   have type ‘y ≠ 0 : Prop‘.

The issue is that we need to cast ‘hy‘ from ‘(y : R) ≠ 0‘ back to ‘y ≠ 0‘.
   The hypothesis ‘h‘ is already ‘y ≠ 0‘ in the context (where ‘y‘ is of type
   ‘Q‘), but we’re trying to use it with ‘hx.mul_rat hy‘ where ‘hy‘ is cast
   to ‘(y : R) ≠ 0‘.

To fix this, we need to explicitly cast ‘hy‘ back to the original type ‘y ≠
    0‘. We can do this using the ‘exact_mod_cast‘ tactic to convert ‘hy‘ back
    to the expected type.
</think>
<code>
‘‘‘lean4
theorem exercise_1_1b
(x : R)
(y : Q)
(h : y ≠ 0)
: ( Irrational x ) -> Irrational ( x * y ) := by
  intro hx
  have hy : y ≠ 0 := h
  have h1 : Irrational (x * y) := by
     simpa using hx.mul_rat hy
  exact h1
’’’
</code>
<interpreter>
Compilation Success!
</interpreter>



Figure 13 | Example of correcting the errors with our proposed verifier-integrated in long CoT
reasoning (Part II).




                                             23
