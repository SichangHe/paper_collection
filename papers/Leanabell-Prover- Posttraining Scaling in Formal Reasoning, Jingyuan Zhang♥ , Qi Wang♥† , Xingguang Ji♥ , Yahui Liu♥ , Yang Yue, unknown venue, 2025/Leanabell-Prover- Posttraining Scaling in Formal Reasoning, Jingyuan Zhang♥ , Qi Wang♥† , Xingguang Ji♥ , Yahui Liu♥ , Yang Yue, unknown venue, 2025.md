                                          Leanabell-Prover: Posttraining Scaling in Formal Reasoning

                                                      Jingyuan Zhang♥ , Qi Wang♥† , Xingguang Ji♥ , Yahui Liu♥ , Yang Yue,
                                                             Fuzheng Zhang, Di Zhang, Guorui Zhou, Kun Gai

                                                                                                Kuaishou Technology



                                                                                                        Abstract
arXiv:2504.06122v3 [cs.AI] 14 Jul 2025




                                         Recent advances in automated theorem proving (ATP) through LLMs have highlighted the
                                         potential of formal reasoning with Lean 4 codes. However, ATP has not yet be revolutionized
                                         by the recent posttraining scaling as demonstrated by Open AI O1/O3 and Deepseek R1. In this
                                         work, we investigate the entire posttraining of ATP, aiming to align it with breakthroughs in
                                         reasoning models in natural languages. To begin, we continual train current ATP models with a
                                         hybrid dataset, which consists of numerous statement-proof pairs, and additional data aimed at
                                         incorporating cognitive behaviors that emulate human reasoning and hypothesis refinement.
                                         Next, we explore reinforcement learning with the use of outcome reward returned by Lean 4
                                         compiler. Through our designed continual training and reinforcement learning processes, we
                                         have successfully improved existing formal provers, including both DeepSeek-Prover-v1.5 and
                                         Goedel-Prover, achieving state-of-the-art performance in the field of whole-proof generation.
                                         For example, we achieve a 59.8% pass rate (pass@32) on MiniF2F. This is an on-going project
                                         and we will progressively update our findings, release our data and training details.

                                                                          65.0
                                                                                                       SFT    RL      Ours RL
                                                                          62.5
                                                                          60.0                                                   59.8
                                                       Passing Rate (%)




                                                                                                                      57.6
                                                                          57.5                  56.6
                                                                          55.0
                                                                          52.5
                                                                          50.0           50.0
                                                                                  48.2
                                                                          47.5
                                                                          45.0 DeepSeek-Prover-v1.5                    Goedel-Prover

                                         Figure 1 | Benchmark performance on MiniF2F-test (Zheng et al., 2021). Our method boosts both
                                         the two baseline models after employing RL training. Goedel-Prover-RL is our implementation.
                                         Our framework surpasses DeepSeek-Prover-v1.5-RL and Goedel-Prover-SFT 6.6% and 2.2%,
                                         respectively.




                                         ♥ Equal contributions, and order alphabetically by first name. † Corresponding author.
1. Introduction
Recent large language models (LLMs), such as Open AI O1/O3 and Deepseek R1, which are
enhanced by posttraining scaling, emerge with numerous powerful and intriguing reasoning
behaviors (Guo et al., 2025; Anthropic, 2025; Team, 2025). Such LLMs have shown impressive
performance in solving math problems with natural language. However, the long chain-of-
thoughts (CoTs) and final answers in natural language (NL) are substantially challenging for
peer review (Wang et al., 2024), especially for theorem proving. Meanwhile, the key advantage
of formal languages lies in their verifiability—each reasoning step can be validated by formal
theorem verifiers, e.g., Lean (De Moura et al., 2015; Moura and Ullrich, 2021) and Isabelle (Paul-
son, 1994). As a promising direction, automated theorem proving (ATP) with formal languages
(FL) has attracted booming attention from the community of large language models (LLMs).
    Contrary to solving math problems with natural language, generating proofs using Lean
4 codes (or other formal languages) is more challenging. For example, DeepSeek-Prover-
v1.5-RL (Xin et al., 2024) achieves only 50.0% (pass@32) on the Olympiad-level mathematics
benchmark MiniF2F (Zheng et al., 2021). However, DeepSeek-R1 (Guo et al., 2025) can achieve
100% on the same math problems, but in natural language. DeepSeek-Prover-v1.5 (Lin et al.,
2025) and STP (Dong and Ma, 2025) show that using extensive synthetic dataset of formal
statements and expert iteration (Polu et al., 2022) can boost the whole-proof prover. Meanwhile,
some methods (Yang et al., 2023; Wu et al., 2024; Xin et al., 2025) scale up the search budget (e.g.,
more than 2 million in BFS-Prover (Xin et al., 2025)) for step-wise tactic generation, which seems
extremely computational.
    Although RL strategies have already proven their effectiveness in natural language for math
problem solving, the performance in formal reasoning has been rather ordinary so far. We find
that only Deepseek-Prover releases it RL version, and DeepSeek-Prover-v1.5-RL marginally
improves 1.8% than its supervised fine-tuned model. Compared to the success of reinforcement
learning (RL) in natural language reasoning, the potential for improvement in formal language
reasoning may still be vast. However, replicating the current successful RL training approaches,
which primarily focus on the Qwen2.5 model series, is not straightforward.
    To verify the posttraining scaling in ATP, we begin with the standard whole-proof generation
models DeepSeek-Prover-v1.5-SFT and Goedel-Prover-SFT. There are three training stages in
our optimization framework. We first collect public and synthetic data to continue training.
We also utilize automatic synthetic CoT data to embed the self-reflection capabilities, such as
backtracking (abandoning failing approaches) and verification (systematic error-checking), to
the fine-tuned model. Next, we employ the GRPO algorithm (Shao et al., 2024) to perform
reinforcement learning from proof assistant feedback (RLPAF) on the supervised fine-tuned
model. Similar to DeepSeek-Prover-v1.5-RL, the verification results from the Lean compiler
serve as reward supervision. After analyzing the validation results on benchmarks, we find our
posttraining strategies can effectively boost the overall performance on MiniF2F (Zheng et al.,
2021) benchmark.
   In summary, here are our main contributions:

   • We continue train current APT models with more high quality statement-proof data
     pairs. More importantly, we design synthetic data to enhance the models’ self-reflection
     capabilities, enabling us to pilot cognitive behaviors in our models before applying the RL
     algorithm.
   • We investigate the RL training to boost the ATP prover that generates whole mathematical
     proofs in Lean 4 codes. During training, we employ the Lean 4 verifier to serve as a reward

                                                 2
     supervision.
   • The proposed Leanabelle-Prover achieves state-of-the-art performance through our metic-
     ulously designed strategy, 59.8% (pass@32) on MiniF2F-test.
   • Currently, we collect around 1.52M formal statements, and 0.22M formal statements with
     detailed informal CoTs and verified proofs. All intermediate models and training data are
     released to the community1 .


2. Related Work
Lean4 Theorem Proving using LLMs. With the rapid progress of LLMs, research has explored
applying LLMs in FL reasoning to automate theorem proving. Prior research can be briefly
classified into two strategies, namely proof-step generation and whole-proof generation.
    Proof-step generation methods train an LLM agent to iteratively generate proof steps by
predicting the next tactic based on the current proof state (Polu and Sutskever, 2020; Polu et al.,
2022; Lample et al., 2022; Azerbayev et al., 2023; Yang et al., 2023; Lin et al., 2024; DeepMind, 2024;
Trinh et al., 2024; Wu et al., 2024,; Xin et al., 2024; Li et al., 2024; Xin et al., 2025). These methods
apply FL executor to verify after each step of generation and is able to discover some non-trivial
proofs. For example, LeanDojo (Yang et al., 2023) first establishes relationship models between
various tactic states within proofs. It then retrieves relevant premises from the mathematical
library based on the current output state (as collected from a Lean verifier) and inputs these
premises into an encoder-decoder model to generate the subsequent tactic. Employing Monte-
Carlo tree search (MCTS) (Coulom, 2006) is another common solution in this field. However, as
the complexity of the proof increases, tree search methods become computationally expensive
and lack high-level NL planning to control the overall structure of the proof (Wang et al., 2025).
    Whole-proof generation methods treat theorem proving as a kind of code generation problem,
where LLMs generate the entire proof in a single attempt by using supervised training or
prompt engineering (Xin et al., 2024,; Lin et al., 2025; Dong and Ma, 2025; Wang et al., 2025).
This approach leverages the NL reasoning and high-level planning capabilities of LLMs with
predictable computation costs, but lacks intermediate feedback from FL executors. Thus, the
core challenge for improving whole-proof generation is that there are no sufficient Lean 4 codes
to eliminate the gaps between NL and FL modalities. However, generating such data requires
high levels of expertise, making it difficult to scale. As a result, the generated proofs often
lack post-hoc analysis of errors and tend to perform badly on tedious questions that require
non-trivial solutions.


Reinforcement Learning for Lean4 Theorem Proving. There are two typical solutions to
utilize RL for Lean4 Theorem Proving. In DeepSeek-Prover-v1.5-RL (Xin et al., 2024), the authors
employ GRPO algorithm and takes the feedback signals from Lean 4 verifier as reward that
reveals the proofs verified as correct or wrong. Such methods only uses the compilation feedback
from the entire proof process as the reward result. In this paper, we employ the whole-proof
generation approach, so we continue with this same solution. In contrast, Xin et al. (2025) use
DPO (Rafailov et al., 2023) to refine the policy LLM by leveraging preference pairs naturally
generated during tree search such as MCTS (Coulom, 2006). Therefore, the second solution
utilizes the tactic state of each step during the compilation process. However, the effectiveness
of existing methods still need improvement.

   1 https://github.com/Leanabell-LM/Leanabell-Prover



                                                   3
Cognitive Behaviors Gandhi et al. (2025) first reveal that models without integrating human-
like reasoning abilities (e.g., verification, backtracking, subgoal setting and backward chaining)
are hard to obtain significant improvements by directly applying RL algorithms. Similarly, Wan
et al. (2025) propose that LLMs lack a specialized design for acquiring meta-thinking, resulting
in low efficacy. Zeng et al. (2025) and Liu et al. (2025) propose that the training may directly start
from the base models with such cognitive behaviors—a paradigm referred to as zero RL training.
Considering the barely satisfactory performance of RL strategies in the formal reasoning field,
we have reasons to suspect whether this is due to this fundamental reason.


3. Model Training

3.1. Continual Training

Base Model. We begin with the previous whole-proof generation models DeepSeek-Prover-
v1.5-SFT (Xin et al., 2024) and Goedel-Prover (Lin et al., 2025) that are two well-trained versions
after the supervised fine-tuning stage. Both of these two models are with 7 billion parameters.
Specifically, the two models are trained with proofs added detailed explanatory informal
comments. Therefore, the model possesses the basic ability to align natural language descriptions
with Lean 4 codes.

                                                            Math Domain Distributions
                               Lean Workbook   STP Lean            MiniF2F
                               Geodel-Prover   NuminaMath          ProofNet
                        0.4
Ratio of Math Domains




                        0.3

                        0.2

                        0.1

                        0.0
                                            set theory




                                                  order
                                                   data
                                         pre-calculus
                                               calculus
                                      combinatorics
                                 logic and puzzles




                                            inequality
                                        group theory

                                              topology
                                           probability
                                   measure theory
                                     number theory
                                            arithmetic
                                            geometry
                                             induction
                                               analysis
                                                   logic
                                complex numbers


                                                algebra
                                        real analysis
                                        trigonometry

                                    category theory
                                      linear algebra
                              applied mathematics




                                 complex analysis

                                            divisibility
                                   abstract algebra
                              functional equations




Figure 2 | Distributions of math domains in various Lean 4 dataset. Lean Workbook, Goedel-
Prover, STP Lean and NuminaMath are training set. MiniF2F and ProofNet are test set.



Statement Formalization. Similar to Lin et al. (2025), we train a formalizer, based on Qwen2.5-
32B-Coder-Instruct (Hui et al., 2024), to convert the olympiad-level math problems in natural
langauge into formal statements. We collect the formal and informal statement pairs sourced




                                                                      4
                   Data Source                            FS     FS+IC+PF
                   Lean Workbook (Ying et al., 2024)     140K       40K
                   STP-Lean (Dong and Ma, 2025)          400K       36K
                   NuminaMath (Li et al., 2024)          520K       97K
                   AoPS (AoPS)                           370K       26K
                   PromptCoT (Zhao et al., 2025)          90K       20K
                   Total                                1.52M      0.22M

Table 1 | Distribution of our training sources, including released data by existing models and
synthetic data from informal math problems. FS, PF and IC refer to formal statements, proofs
and informal comments, respectively.


from Goedel-Prover 2 (around 30K). The training details of our formalizer are presented in
Appendix A. With the trained formalizer, we convert the natural language statement and then
verify with Lean 4 compiler. After these procedures, we finally get 520K formal statements
from NuminaMath (Li et al., 2024) and 370K formal statements from AoPS (AoPS). Recently,
Zhao et al. (2025) proposed to utilize LLMs to synthesize math problems through mathematical
concepts. Based on the data analysis in Figure 2, we employ the PromptCoT framework to
synthesize math problems at different levels, including AMC, AIME and USAMO, on three
majority math domains (i.e., algebra, number theory and calculus).


Data Curation. We develop a comprehensive Lean 4 code completion dataset for the super-
vised fine-tuning, as shown in Table 1. These theorems are sourced from various projects, such
as the standard Lean 4 math library Mathlib4 (mathlib4, 2025), Lean Workbook (Ying et al.,
2024), synthetic theorems from Goedel-Prover (Lin et al., 2025) and STP (Dong and Ma, 2025).
Besides the above-mentioned public data, we use deepseek-prover and goedel-prover to sample
proofs that can be correctly verified by Lean 4 compiler. In this manner, we collect Lean data
from NuminaMath and AoPS. Similarly, we formalize around 90K math problems synthesized
through PromptCoT. In DeepSeek-Prover-v1.5 (Xin et al., 2024), the authors claim that incorpo-
rating natural language reasoning before generating theorem proof code can eliminate the gap
between problem solving strategies in natural language and theorem proving in Lean. Thus, we
also collect comments for part of the data. Finally, we collected around 1.52M formal statements
and 0.22M statemens with detailed informal comments and verified proofs.
    As shown in Figure 2, we find that the data distributions of Lean Workbook, Goedel-Prover,
STP Lean and NuminaMath cover well the MiniF2F test set. On the contrast, there is an obvious
domain bias for ProofNet, which is also revealed by (Lin et al., 2025). It indicates a promising
direction for further improvement by expanding data in specific mathematical domains. For
fairness, we do not adjust the distributions of the training set in our optimizations.


Implementation After obtaining a large collection of formalized statements with proofs, we
continuously train once. We use the lightweight framework SWIFT 3 for the supervised fine-
tuning (SFT). The SFT experiment is trained on 8 NVIDIA H100 GPUs with the following
hyperparameters: a learning rate of 5 × 10−5 , a global batch size of 32 over 2 epochs, and a
weight decay coefficient of 0.1.
   2 https://huggingface.co/datasets/Goedel-LM/Lean-workbook-proofs
   3 https://github.com/modelscope/ms-swift



                                               5
3.2. Integrating Cognitive Behaviors

Gandhi et al. (2025) have revealed the importance of cognitive behaviors in base models before
utilizing RL strategies. Following a similar idea, we induce reflection-like behaviors through
specially designed interventions. We propose two kinds of CoT templates to integrate the
self-reflection capabilities: Lean completion and rewriting.


Lean Completion. We sample 5K formal statements used in our previous continue training
stage, which are not 100% correct in the pass@16 sampling. We find the position where the first
error tactic appears, and re-sample for completion. Once collecting new valid proofs, we can use
the following prompt to ask Claude (Anthropic, 2025) to generate the reflection response. We
observe that an effective reflection process can only be achieved by combining incorrect proofs,
correct proofs, and tactic error messages. Thus, the feedback collected from Lean verifier is also
used to create the prompt. An example is presented in Section B.1.

                                Lean Completion Prompt (Claude)
  # Initial Proof
  ‘‘‘lean4
  {old_code}
  ’’’

  # Lean Feedback
  {error}

  # Correct Proof
  ‘‘‘lean4
  {new_code}
  ’’’

  Your task is to generate a reflection of a Lean4 proof as follows:
  1. You are provided with a lean proof code that failed to complete the proof, the verify
  feedback, and a revised correct proof.
  2. You need to act as a verifier to check the code step by step and point out where the
  code fails with incorrect tactics.
  3. Provide an alternative method, such as those in the correct proof.
  4. Act as you are verifying your own proof.

  Here are some rules you need to follow:
  1. At the beginning, you should start with a conjunction phrase such as ‘let’s verify’ and
  claim you need to verify the proof.
  2. Instead of directly pointing out the issue, your answer should show the process to
  identify the incorrect step.
  3. Do not refer to Lean Feedback, Correct Proof, or anything that shows you have already
  known the issue before your reflection.
  4. Do not provide any new Lean4 code block, you don’t need to write a correct proof.
  5. Do not include a summary section.
  6. Again, do not refer to Lean Feedback, Correct Proof, do not write anything like ‘as
  shown in the correct proof’.

  Now, start with a conjunction phrase and require you need to check the proof, do not
  directly claim there is an issue.



Rewriting. Based on the above-mentioned Lean completion, there are two main steps in the
rewriting strategy. First, we suspect that the generation of incorrect proofs is, to some extent, due
to the incorrect problem-solving comments being generated. Therefore, we introduce Qwen2.5-
72B-instruct (Team, 2024) to evaluate the problem-solving comments and then regenerate the
correct problem-solving comments. Second, we provide Claude with both the invalid and newly
rewritten valid Lean 4 code to generate comprehensive Chains of Thought (CoTs) that explain


                                                 6
the reasoning process. In this manner, we collect 19K samples with CoTs (See the detailed
examples in Appendix B.2). Here are the prompt templates for these two steps:

                               Rewriting - Step 1 (Qwen2.5-72B-Instruct)
   You are an experienced mathematics evaluation teacher. You will be provided with a math
   problem and the corresponding solution idea.
   Please determine whether the solution idea is correct. If it is, please output "Correct",
   otherwise please output "Incorrect". If the solution idea is incorrect, please provide the
   correct solution idea, and the output of the solution idea should be included within ‘‘‘
   and ’’’.

   The output format is as follows:

   1.   Judgement:   Incorrect.       Solution:      ‘‘‘Solution idea’’’
   2.   Judgement:   Correct.

  [math problem start]
  {problem}
  [math problem end]

  [solution idea start]
  {solution}
  [solution idea end]



   With these synthesized data, we employ our sencond-stage continual training, with a learn-
ing rate of 5 × 10−5 and overall batch size of 1024 for one epoch. Finally, we obtain the model,
named as Leanabell-Prover-SFT.

3.3. Reinforcement Learning

We integrate reinforcement learning (RL) with the Lean 4 theorem prover to automate the
discovery of valid proofs. The RL agent interacts with the Lean 4 environment, generating
whole proofs and receiving feedback from Lean 4 compiler as reward signals. The agent’s
objective is to maximize cumulative rewards by learning to generate syntactically correct,
logically valid proofs for an input formal statement.


Policy Optimization Algorithms. We employ the recent GRPO (Shao et al., 2024) as our RL
algorithm. For each input formal statement 𝑞, GRPO samples a group of outputs { 𝑜1 , 𝑜2 , · · · , 𝑜𝐺 }
from the old policy 𝜋𝜃𝑜𝑙𝑑 and then collect the feedback {𝜏1 , 𝜏2 , · · · , 𝜏𝐺 } for the group of responses
through Lean 4 compiler. According to each feedback status 𝜏𝑖 , we assign a particular reward.
Then, the advantage of the 𝑖-th output is calculated by normalizing the group-level rewards
{ 𝑅1 , 𝑅2 , · · · , 𝑅𝐺 }:
                                              𝑟𝑖 − mean({ 𝑅 𝑖 }𝐺𝑖=1 )
                                     𝐴ˆ 𝑖,𝑡 =                         .                                 (1)
                                                  std({ 𝑅 𝑖 }𝐺𝑖=1 )
Finally, we optimizes the policy model 𝜋𝜃 by maximizing the following objective:

              JGRPO ( 𝜃) = E ( 𝑞,𝑎 )∼D,{ 𝑜𝑖 } 𝐺 ∼𝜋𝜃 (· | 𝑞 )
                                                 𝑖=1  old
                                         |     |
                        " 𝐺                                                                                   !#
                          1 ∑︁ 1 ∑︁
                                           𝑜 𝑖                                                                 (2)
                                                    min 𝑟𝑖,𝑡 ( 𝜃) 𝐴ˆ 𝑖,𝑡 , clip 𝑟𝑖,𝑡 ( 𝜃), 1 − 𝜀, 1 + 𝜀 𝐴ˆ 𝑖,𝑡 ,
                         𝐺        | 𝑜𝑖 |
                                𝑖=1       𝑡 =1

where
                                                           𝜋𝜃 ( 𝑜𝑖,𝑡 | 𝑞, 𝑜𝑖,<𝑡 )
                                            𝑟𝑖,𝑡 ( 𝜃) =                               ,                            (3)
                                                          𝜋𝜃old ( 𝑜𝑖,𝑡 | 𝑞, 𝑜𝑖,<𝑡 )

                                                               7
𝜀 is a hyperparameter. In our experiments, we set 𝜀 = 0.2. Notably, we do not use the Kullback-
Leibler (KL) divergence penalty.

                                   Rewriting - Step 2 (Claude)
  # Wrong code
  ‘‘‘lean4
  lean code1
  ’’’

  # Correct code
  ‘‘‘lean4
  lean code2
  ’’’

  I have given you with two Lean4 code solutions to the same problem. The first solution
  fails to compile in Lean4, while the second solution compiles successfully.
  Your task is to:
  1. Act as a verification assistant and carefully compare these two code snippets.
  2. Identify the specific errors or flawed strategies in the first solution that caused
  compilation failure.
  3. Explain the reasoning process that would lead someone from the incorrect approach to
  the correct solution.

  When analyzing the code, please simulate the thought process of someone examining their own
  proof. Begin sections of your analysis with phrases like “Let’s verify my proof...", “Wait,
  I see an issue here...", or “Let me reconsider this approach..." This should demonstrate
  how someone might catch and correct their own mistakes.

  The analysis emphasizes conceptual understanding over syntax details, explaining the
  fundamental logical or strategic errors in the initial solution and demonstrating how the
  corrected solution properly addresses these conceptual problems.

   Please structure your response with:
  - Identification of specific errors in the first solution.
  - Explanation of the conceptual issues that led to these errors.
  - How to fix the conceptual problems in error so as to generate the problem-solving idea of
   the second solution?

  Do not provide any new Lean4 code beyond what I’ve given you - focus exclusively on
  analyzing the provided code. Don’t include the phased titles in the output results, such
  as "Identification of Specific Errors in the First Solution", "Conceptual Issues That
  Led to These Errors", etc. Also, don’t use expressions like "the first solution" or "the
  second solution". Use "current solution" to represent "first solution". Although you used
  the second solution for auxiliary analysis, avoid revealing in your response that you’ve
  seen its content. For example, refrain from saying things like ‘I noticed that in the new
  solution.’ Instead, respond as if you’re thinking independently, based solely on the first
  solution.



Reward Function. Unlike stepwise rewards, the feedback is provided only after the full proof
is compiled by Lean 4 verifier in our experiments. Our rewards are derived from: (1) Terminal
reward 𝑅success : a scalar reward granted if the entire proof is validated successfully by Lean 4
verifier. (2) Penalty 𝑅fail : a negative reward for proofs with critical errors (e.g., type mismatches,
infinite loops, unsolved goals and etc). Moreover, we observe that there are warnings in
the feedback, such as some unnecessary or redundant steps have no negative effects on the
final validation. In our experiments, we ignore warning cases as long as the compilation and
verification process passes successfully. So, given the feedback 𝜏 from Lean 4 compiler, our final
reward function can be formulated as:
                                  (
                                    𝑅success if Lean 4 fully validates 𝜏
                        𝑅 ( 𝜏) =                                                                    (4)
                                    𝑅fail    otherwise (syntax errors/timeout)



                                                  8
Implementation We conduct RL training based on the Leanabell-Prover-SFT. We use a constant
learning rate of 1 × 10−6 . For each theorem, we sample a group of 32 candidate proofs, with
maximal rollout length set to 8192. The training global batch size is set to 32 × 32 = 1024. On the
RL training data, we select samples from those whose number of validations in Pass@32 falls
within the range of [2, 16]. We believe this subset of data has a certain level of difficulty while
providing exploration space, making it effective for updating the policy model. The detailed
distribution of pass@32 is presented in Figure 6 in Appendix C. Finally, we obtain the RL version
model named as Leanabell-Prover-RL.


4. Experiments
Benchmarks We follow the previous work (Lin et al., 2025; Xin et al., 2024,; Wang et al., 2024)
and mainly validate the effectiveness of our proposed method on the most commonly-used
MiniF2F-test (Zheng et al., 2021).


Results on MiniF2F. We have two versions of our models posttrained from two strong prover
models: Deepseek-Prover-v1.5-SFT and Goedel-Prover-SFT, namely Leanabell-Prover-DS and
Leanabell-Prover-GD. We mainly compare current whole proof generation methods, while ig-
nore those with proof-step methods using far more inference-compute. As shown in Table 2, our
posttraining framework boosts both DeepSeek-Prover-v1.5-SFT and Goedel-Prover-SFT models.
On the minimum sample budget, Leanabell-Prover-GD-RL achieves the SOTA of MiniF2F (59.8%
on pass@32), which gains up to 2.2% (i.e. from Goedel-Prover SFT, from 57.6% to 59.8%). We
can observe that following our continual training phase, our method (Leanabell-Prover-DS-SFT)
shows improvement over its base model (DeepSeek-Prover-v1.5-SFT), and the RL version con-
tinues to effectively enhance its performance. Meanwhile, Leanabell-Prover-GD-SFT performs
almost identically to Leanabell-Prover-DS-SFT. This is reasonable, as Goedel-Prover-SFT is
finetuned from DeepSeek-Pover-v1.5-base, with a significantly larger amount of data compared
to our continual training stage. Therefore, our continual training on Leanabell-Prover-GD-SFT
primarily adjusts the model’s reasoning ability across different math domain distributions and
incorporates the proper CoT format with cognitive behaviors into the current training data. This
makes the checkpoint more conducive to RL training.
     We also increase the sampling budget to compare the performance gains. For the SFT models,
as can be seen, the baseline DeepSeek-Prover-v1.5-SFT achieves around 2.2% performance gains
(i.e., 48.2% to 50.4%), as increasing sampling budget from 32 to 128. Within our configura-
tions, our Leanabell-Prover-DS-SFT and Leanabell-Prover-GD-SFT models also achieve 1.8%
(i.e., 54.9% to 56.7%) and 1.2% (i.e., 58.2% to 59.4%) performance gains on the same inference
scaling experiments, respectively. For the RL models, DeepSeek-Prover-v1.5-RL achieves 1.6%
performance gains (i.e., 50.0% to 51.6%), while our Leanabell-Prover-DS-RL achieves more gains
(i.e., 56.6% to 59.0%). Therefore, after the model has undergone SFT and RL training, our models
still maintain the exploration capabilities.


Exploration Abilities and RL. We first examine our two SFT models, with their pass@16
accuracy at different sampling temperatures. This metric can serve as an indicator of the policy’s
exploration ability and is particularly relevant for RL, as it reflects the policy’s ability to generate
responses that can achieve a positive reward. As shown in Figure 3, we find both SFT models
are exploratory, and thus ready for RL. The RL training rewards are shown in Figure 4. During
our experiments, we also compared the original GRPO with Dr. GRPO (Liu et al., 2025), and


                                                   9
             Method                                Sample budget   miniF2F-test
             TheoremLlama [28]                          128           33.6%
             DeepSeek-Prover-v1 [32]                    128        46.1% ± 0.5%
                                                        128        29.7% ± 0.5%
             DeepSeek-Prover-v1.5-Base [33]            3200            39.2%
                                                       6400            42.2%
                                                        32         48.2% ± 0.6%
                                                        64         49.6% ± 0.7%
             DeepSeek-Prover-v1.5-SFT [33]
                                                        128        50.4% ± 0.4%
                                                       3200        53.3% ± 0.5%
                                                        32         50.0% ± 0.5%
                                                        64         50.7% ± 0.4%
             DeepSeek-Prover-v1.5-RL [33]
                                                        128        51.6% ± 0.5%
                                                       3200        54.9% ± 0.7%
                                                        128        57.7% ± 0.6%
             STP [7]
                                                       3200        61.7% ± 0.6%
                                                        32         57.6% ± 0.7%
             Goedel-Prover-SFT [15]
                                                       3200            62.7%
                                                        32            54.9%
                                                        64            55.3%
             Leanabell-Prover-DS-SFT
                                                        128           56.7%
                                                        32            56.6%
                                                        64            57.4%
             Leanabell-Prover-DS-RL
                                                        128           59.0%
                                                        32            58.2%
                                                        64            59.0%
             Leanabell-Prover-GD-SFT
                                                        128           59.4%
                                                        32            59.8%
                                                        64            60.7%
             Leanabell-Prover-GD-RL
                                                        128           61.1%

Table 2 | Comparison with state-of-the-art methods on the miniF2F-test dataset. The notation
𝜇 ± 𝜎 denotes the average accuracy 𝜇 and the standard deviation 𝜎. “DS” and “GD” refer to
using the DeepSeek-Prover-v1.5-SFT and Goedel-Prover-SFT as base models to continue SFT
and RL training, respectively.




                                              10
                                                            Exploration Ability
                                             60
                                             57
                                             54


                          Pass@16 Rate (%)
                                             51
                                             48
                                             45
                                             42              Goedel-Prover-SFT
                                                             DeepSeek-Prover-v1.5-SFT
                                             39              Leanabell-Prover-DS-SFT
                                             36              Leanabell-Prover-GD-SFT
                                                  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
                                                                 Temperature

Figure 3 | Exploration ability: pass@16 measures how well base models explore.

         0.31                                                                  0.38
         0.30                                                                  0.36
         0.28                                                                  0.34
         0.27                                                                  0.33
         0.26
Reward




                                                                      Reward




                                                                               0.32
         0.24                                                                  0.30
         0.22                                                                  0.28
         0.21
                                                                               0.27
         0.19
                     Leanabell-Prover-DS-RL                                    0.26          Leanabell-Prover-GD-RL
         0.18
                0   20           40         60                                        0   20    40       60      80   100
                       Training Step                                                           Training Step

Figure 4 | Left: Reward curve during training Leanabell-Prover-Prover-DS-RL. Right: Reward
curve during training Leanabell-Prover-Prover-GD-RL.


found that the training dynamics remained largely consistent under these two RL training
algorithms. This may be attributed to the fact that the length of different rollout responses,
regardless of whether they are correct or incorrect, does not vary significantly in formal language
reasoning. We have also observed that selecting an appropriate prompt set is crucial for RL
training. Merely using pass@N as the sole criterion is insufficient to unlock the full potential of
RL. As shown in Figure 5, we analyze the distributions of error problems across different source
types in the MiniF2F-test set. We observed that, based on DeepSeek-Prover-v1.5-SFT, errors can
be reduced across all data source types in MiniF2F-test set, especially for AMC, MATH, and
CUSTOM. However, this improvement is significantly reduced in optimization results based on
Goedel-Prover-SFT. This suggests that such as the intrinsic difficulty level of the statements (e.g.,
whether they are at the AIME or IMO level), the coverage of mathematical domains, and the
balance with the prover model’s capabilities, are also important.




                                                                 11
                                DeepSeek-Prover-v1.5-SFT                                                   30         Goedel-Prover-SFT
                     35         Leanabell-Prover-DS-RL                                                                Leanabell-Prover-GD-RL

                     30                                                                                    25
Number of Failures




                                                                                      Number of Failures
                     25
                                                                                                           20
                     20
                                                                                                           15
                     15

                     10                                                                                    10
                          IMO            AIME              AMC   MATH   CUSTOM                                  IMO            AIME            AMC   MATH   CUSTOM

  Figure 5 | Distribution of problem types that failed verification on the MiniF2F-test set.


  5. Conclusion, Limitation, and Future Work
 We present a series of ATP models, named Leanabell-Proverseries, by investigating the posttrain-
 ing scaling of current provers. Leanabell-Prover is started with DeepSeek-Prover-v1.5-SFT and
 Goedel-Prover-SFT which are two well-trained whole-proof generation models. We first collect a
 large collection of formalized statements with proofs to continue training. More importantly, we
 embed cognitive behaviors into the base models by applying a second-stage continual training
 on such synthetic data. With such prepared SFT models, we finally achieve the final performance
 through the RL optimization.


 Limitations. As we find that the base prover model (i.e., DeepSeek-Prover-v1.5) is a weak
 LLM compared to those used for posttraining scaling in natural languages, such as Deepseek
 v3 and the Qwen2.5 family. Although we have piloted to integrate cognitive behaviors into
 the model and selected the prompt set of RL according to the ability of our SFT models, the
 expected stronger RL performance has not fully materialized. Our findings right now are more
 in line with the replication on weak LLMs with RL (Liu et al., 2025; Zeng et al., 2025). Moreover,
 although we achieved performance gains, we observe that the integrated sefl-reflection capacities
 demonstrate a weakening trend after RL training. This suggests that effectively integrating
 cognitive behaviors into such weak base LLMs remains highly challenging.


  Future Work. Our goal is to fully invoke formal reasoning abilities, and thus we will continual
  to explore the following directions (hopefully can achieve some improvement):

                      • Bridging formal reasoning with natural languages. Reasoning in formal languages has
                        natural benefits for theorem proving, including no mathematical knowledge hallucination,
                        and all steps and states with verified feedback. However, reasoning abilities of current
                        formal provers (including our current work) still lag behind those of natural language
                        reasoning models. We have made the first step to design a CoT template and synthesize
                        data accordingly, which is intended to insert natural language information to help formal
                        reasoning. We also tried Deepseek R1 with prompting for formal proof generation, which
                        achieves 51.6% (pass@32) on MiniF2F-test. Therefore, we hope to develop more effective
                        manners that can transfer the math knowledge and reasoning abilities in natural languages
                        into formal proof generation.
                      • Bridging whole proof generation with proof-step methods. We believe current RL frame-
                        work can help bridging these two lines of methods. For example, we can replace the


                                                                                 12
      sampling-based response-level rollout in RL into proof-step rollout for better exploration
      (but still rollout into a whole proof or reach the maximum length, then calculate the
      response-level reward), thus improving the learning efficiency of the RL training stage.


References
 [1] Anthropic. Claude 3.7 Sonnet System card. 2025. URL https://www.anthropic.com/
     news/claude-3-7-sonnet.
 [2] AoPS. Art of problem solving. https://artofproblemsolving.com/. Accessed:
     [date].

 [3] Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. McAleer, A. Q. Jiang, J. Deng,
     S. Biderman, and S. Welleck. Llemma: An open language model for mathematics. arXiv
     preprint arXiv:2310.10631, 2023.

 [4] R. Coulom. Efficient selectivity and backup operators in monte-carlo tree search. In
     International conference on computers and games, pages 72–83. Springer, 2006.

 [5] L. De Moura, S. Kong, J. Avigad, F. Van Doorn, and J. von Raumer. The Lean theorem
     prover (system description). In International Conference on Automated Deduction (CAD), 2015.

 [6] DeepMind. Alphaproof and Alphageometry, July 2024. URL https://deepmind.googl
     e/discover/blog/ai-solves-imo-problems-at-silver-medal-level/.
 [7] K. Dong and T. Ma. Stp: Self-play llm theorem provers with iterative conjecturing and
     proving. arXiv preprint arXiv:2502.00212, 2025.

 [8] K. Gandhi, A. Chakravarthy, A. Singh, N. Lile, and N. D. Goodman. Cognitive behaviors
     that enable self-improving reasoners, or, four habits of highly effective stars. arXiv preprint
     arXiv:2503.01307, 2025.

 [9] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
     Deepseek-R1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv
     preprint arXiv:2501.12948, 2025.

[10] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Dang, et al.
     Qwen2. 5-coder technical report. arXiv preprint arXiv:2409.12186, 2024.

[11] G. Lample, T. Lacroix, M.-A. Lachaux, A. Rodriguez, A. Hayat, T. Lavril, G. Ebner, and
     X. Martinet. Hypertree proof search for neural theorem proving. Advances in Neural
     Information Processing Systems (NeurIPS), 35, 2022.

[12] J. Li, E. Beeching, L. Tunstall, B. Lipkin, R. Soletskyi, S. C. Huang, K. Rasul, L. Yu, A. Jiang,
     Z. Shen, Z. Qin, B. Dong, L. Zhou, Y. Fleureau, G. Lample, and S. Polu. Numinamath, 2024.

[13] Y. Li, D. Du, L. Song, C. Li, W. Wang, T. Yang, and H. Mi. Hunyuanprover: A scalable data
     synthesis framework and guided tree search for automated theorem proving. arXiv preprint
     arXiv:2412.20735, 2024.

[14] H. Lin, Z. Sun, Y. Yang, and S. Welleck. Lean-star: Learning to interleave thinking and
     proving. arXiv preprint arXiv:2407.10040, 2024.



                                                 13
[15] Y. Lin, S. Tang, B. Lyu, J. Wu, H. Lin, K. Yang, J. Li, M. Xia, D. Chen, S. Arora, et al. Goedel-
     prover: A frontier model for open-source automated theorem proving. arXiv preprint
     arXiv:2502.07640, 2025.

[16] Z. Liu, C. Chen, W. Li, P. Qi, T. Pang, C. Du, W. S. Lee, and M. Lin. Understanding
     r1-zero-like training: A critical perspective. arXiv preprint arXiv:2503.20783, 2025.

[17] mathlib4. The math library of lean 4, 2025. URL https://github.com/leanprover-c
     ommunity/mathlib4.
[18] L. d. Moura and S. Ullrich. The lean 4 theorem prover and programming language. In
     International Conference on Automated Deduction, 2021.

[19] L. C. Paulson. Isabelle: A generic theorem prover. Springer, 1994.

[20] S. Polu and I. Sutskever. Generative language modeling for automated theorem proving.
     arXiv preprint arXiv:2009.03393, 2020.

[21] S. Polu, J. M. Han, K. Zheng, M. Baksys, I. Babuschkin, and I. Sutskever. Formal mathemat-
     ics statement curriculum learning. arXiv preprint arXiv:2202.01344, 2022.

[22] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn. Direct prefer-
     ence optimization: Your language model is secretly a reward model. Advances in Neural
     Information Processing Systems (NeurIPS), 2023.

[23] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
     Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
     arXiv preprint arXiv:2402.03300, 2024.

[24] Q. Team. Qwen2.5: A party of foundation models, September 2024. URL https://qwen
     lm.github.io/blog/qwen2.5/.
[25] Q. Team. Qwq-32b: Embracing the power of reinforcement learning, March 2025. URL
     https://qwenlm.github.io/blog/qwq-32b/.
[26] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong. Solving olympiad geometry without
     human demonstrations. Nature, 625(7995):476–482, 2024.

[27] Z. Wan, Y. Li, Y. Song, H. Wang, L. Yang, M. Schmidt, J. Wang, W. Zhang, S. Hu, and Y. Wen.
     Rema: Learning to meta-think for llms with multi-agent reinforcement learning. arXiv
     preprint arXiv:2503.09501, 2025.

[28] R. Wang, J. Zhang, Y. Jia, R. Pan, S. Diao, R. Pi, and T. Zhang. Theoremllama: Transforming
     general-purpose llms into lean4 experts. arXiv preprint arXiv:2407.03203, 2024.

[29] R. Wang, R. Pan, Y. Li, J. Zhang, Y. Jia, S. Diao, R. Pi, J. Hu, and T. Zhang. Ma-lot: Multi-
     agent lean-based long chain-of-thought reasoning enhances formal theorem proving. arXiv
     preprint arXiv:2503.03205, 2025.

[30] Z. Wu, S. Huang, Z. Zhou, H. Ying, J. Wang, D. Lin, and K. Chen. Internlm2.5-Stepprover:
     Advancing automated theorem proving via expert iteration on large-scale lean problems.
     arXiv preprint arXiv:2410.15700, 2024.

[31] Z. Wu, J. Wang, D. Lin, and K. Chen. Lean-github: Compiling github lean repositories for a
     versatile lean prover. arXiv preprint arXiv:2407.17227, 2024.

                                                 14
[32] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan, W. Li, and X. Liang. Deepseek-
     prover: Advancing theorem proving in llms through large-scale synthetic data. arXiv
     preprint arXiv:2405.14333, 2024.

[33] H. Xin, Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu, L. Zhang, X. Lu, Q. Du, et al.
     Deepseek-prover-v1. 5: Harnessing proof assistant feedback for reinforcement learning
     and monte-carlo tree search. arXiv preprint arXiv:2408.08152, 2024.

[34] R. Xin, C. Xi, J. Yang, F. Chen, H. Wu, X. Xiao, Y. Sun, S. Zheng, and K. Shen. Bfs-prover:
     Scalable best-first tree search for llm-based automatic theorem proving. arXiv preprint
     arXiv:2502.03438, 2025.

[35] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and
     A. Anandkumar. Leandojo: Theorem proving with retrieval-augmented language models.
     Advances in Neural Information Processing Systems (NeurIPS), 2023.

[36] H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen. Lean workbook: A large-
     scale lean problem set formalized from natural language math problems. arXiv preprint
     arXiv:2406.03847, 2024.

[37] W. Zeng, Y. Huang, Q. Liu, W. Liu, K. He, Z. Ma, and J. He. Simplerl-zoo: Investigating
     and taming zero reinforcement learning for open base models in the wild. arXiv preprint
     arXiv:2503.18892, 2025.

[38] X. Zhao, W. Wu, J. Guan, and L. Kong. Promptcot: Synthesizing olympiad-level problems
     for mathematical reasoning in large language models. arXiv preprint arXiv:2503.02324, 2025.

[39] K. Zheng, J. M. Han, and S. Polu. Minif2f: a cross-system benchmark for formal olympiad-
     level mathematics. arXiv preprint arXiv:2109.00110, 2021.




                                              15
Appendix
A. Formalizer Details
We start with Qwen25-Coder-32B-Instruct (Hui et al., 2024) and use following instruct prompt
to train the formalizer:

                                        Formalizer Prompt
  Please translate the mathematical statement {informal_statement} into a theorem statement
  in Lean 4 code.

  Please do not generate codes of proof or comment sentences (e.g., starting with ’/-’ or
  ’–’).

  The Lean 4 codes are required to complete the ‘statement’ in the following text:


  ‘‘‘lean4
  theorem lean_workbook ‘statement’ := by sorry
  ‘‘‘



    As shown in Table 3, the formalizer is targeted to translate the natural language statement to
formal statement in Lean 4 codes. We take use of the 29.7K data released by Goedel-Prover (Lin
et al., 2025), which provides pairs of informal statement and formal statement in each sample.
We train the formalizer with a fixed learning rate 5 × 10−6 for 2 epochs. We verify the Compiling
Correctness (CC) Test, and Faithfulness and Completeness (FC) Test by following the prompts
in Goedel-Prover. As shown in Table 4, our formalizer performs similarly to the Formalizer
A (Lin et al., 2025).

               Example 1                                     Example 2
 Informal      Solve for 𝑥 in the given inequality: 𝑥 2 −    Prove that ln( 𝑒𝜋 ) is equal to 𝜋.
 Statement     2 𝑥 − 24 < 0
 Formalizer
 Output        theorem lean_workbook (x : R)                 theorem lean_workbook :
                  : x^2 - 2*x - 24 < 0 ↔ x ∈                    Real.log (Real.exp 𝜋) = 𝜋
                  Set.Ioo (-4) 6 := by sorry                    := by sorry



Table 3 | Examples of formalizer inputs and outputs for two examples.


                  Model                               CC Test (%)      FC Test (%)
                  Formalizer A (Lin et al., 2025)           76.7           48.1
                  Formalizer B (Lin et al., 2025)           88.5           80.4
                  Ours Formalizer                           77.6           49.0

Table 4 | Quality assessment of the formalized statement. “CC” refers to Compiling Correctness
(CC) Test and “FC” refers to Faithfulness and Completeness (FC) Test.




                                                 16
B. Cognitive Behaviors Design

B.1. Lean Completion Example

Input:
Complete the following Lean 4 code with explanatory comments preceding each
   line of code:

‘‘lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

/-- Given sin( 𝜋4 − 𝑥 ) = 53 , find the value of sin 2𝑥 . Show that it is \frac{7}{25}.-/
theorem sin_2x_value (x : R) (h : sin (Real.pi / 4 - x) = 3 / 5) : sin (2 *
   x) = 7 / 25         := by

/-
     Given \(\sin \left(\frac{\pi}{4} - x\right) = \frac{3}{5}\), we need to
      find the value of \(\sin 2x\). We start by using the trigonometric
      identity for the sine of a difference and the double-angle formula for
      sine. Specifically, we use the identity \(\sin(a - b) = \sin a \cos b -
      \cos a \sin b\) and the double-angle formula \(\sin 2x = 2 \sin x \cos x\).
     1. Substitute \(\sin \left(\frac{\pi}{4} - x\right) = \frac{3}{5}\) into
      the identity for the sine of a difference:
        \[
        \sin \left(\frac{\pi}{4} - x\right) = \sin \left(\frac{\pi}{4}\right)
      \cos \left(x\right) - \cos \left(\frac{\pi}{4}\right) \sin \left(x\right)
        \]
     2. Calculate \(\sin \left(\frac{\pi}{4}\right)\) and \(\cos
      \left(\frac{\pi}{4}\right)\):
        \[
        \sin \left(\frac{\pi}{4}\right) = \cos \left(\frac{\pi}{4}\right) =
      \frac{\sqrt{2}}{2}
        \]
     3. Substitute these values into the equation:
        \[
        \frac{3}{5} = \frac{\sqrt{2}}{2} \cos \left(x\right) -
      \frac{\sqrt{2}}{2} \sin \left(x\right)
        \]
     4. Simplify the equation:
        \[
        \frac{3}{5} = \frac{\sqrt{2}}{2} (\cos \left(x\right) - \sin
      \left(x\right))
        \]
     5. Solve for \(\cos \left(x\right) - \sin \left(x\right)\):
        \[
        \cos \left(x\right) - \sin \left(x\right) = \frac{3}{5} \cdot
      \frac{2}{\sqrt{2}} = \frac{3}{5} \cdot \sqrt{2} = \frac{3 \sqrt{2}}{5}
        \]
     6. Use the double-angle formula for sine:
        \[


                                           17
        \sin 2x = 2 \sin \left(x\right) \cos \left(x\right)
        \]
     7. Substitute \(\cos \left(x\right) - \sin \left(x\right) = \frac{3
      \sqrt{2}}{5}\) into the equation:
        \[
        \sin 2x = 2 \sin \left(x\right) \cos \left(x\right) = 2 \left(\frac{3
      \sqrt{2}}{5}\right) \left(\frac{\sqrt{2}}{2}\right) = 2 \cdot \frac{3
      \sqrt{2}}{5} \cdot \frac{\sqrt{2}}{2} = \frac{3 \sqrt{2}}{5} \cdot
      \sqrt{2} = \frac{3 \cdot 2}{5} = \frac{6}{5}
        \]
     8. Simplify the final expression:
        \[
        \sin 2x = \frac{7}{25}
        \]
-/

Wrong Proof :
     -- Use the trigonometric identity for the sine of a difference and the
      double-angle formula for sine.
     simp [Real.sin_sub, Real.sin_two_mul, Real.cos_two_mul,
      Real.sin_pi_div_four, Real.cos_pi_div_four] at h ⊢
     -- Simplify the expression using field operations.
     field_simp at h ⊢
     -- Normalize the expression by expanding and simplifying it.
     ring_nf at h ⊢
     -- Use non-linear arithmetic to verify the final result.
     nlinarith [Real.sin_sq_add_cos_sq x, Real.sin_le_one x, Real.cos_le_one x]

Tactic Error Messages:
linarith failed to find a contradiction
case h1.h
x : R
    √                √
h : 2 * x.cos * 5 - 2 * x.sin * 5 = 6
at : x.cos * x.sin * 50 < 7
⊢ False
failed

Searched Valid Proof :
     -- Use the trigonometric identity for the sine of a difference and the
      double-angle formula for sine.
     simp [Real.sin_sub, Real.sin_two_mul, Real.cos_two_mul,
      Real.sin_pi_div_four, Real.cos_pi_div_four] at h ⊢
     -- Simplify the expression using field operations.
     field_simp at h ⊢
     -- Normalize the expression by expanding and simplifying it.
     ring_nf at h ⊢
     -- Use the Pythagorean identity to simplify further.
     nlinarith [Real.sin_sq_add_cos_sq x, Real.sqrt_nonneg 2, sq_sqrt (show 0 ≤
      2 by norm_num)]"

Claude CoTs:
<think>

                                         18
let’s verify this proof to make sure it’s working correctly. I need to check
   each step of the proof to ensure it’s valid and identify any potential
   issues.

First, let’s examine what we’re trying to prove. It appears to be a
   trigonometric identity involving sine and cosine functions.

The proof begins with:
‘‘‘
simp [Real.sin_sub, Real.sin_two_mul, Real.cos_two_mul, Real.sin_pi_div_four,
    Real.cos_pi_div_four] at h ⊢
‘‘‘
This step seems reasonable - we’re using standard trigonometric identities to
    simplify both the hypothesis h and the goal.

Next, we have:
‘‘‘
field_simp at h ⊢
‘‘‘
This tactic simplifies expressions involving field operations, which is
    appropriate for real-valued trigonometric expressions.

Then:
‘‘‘
ring_nf at h ⊢
‘‘‘
This normalizes ring expressions, which should help simplify our algebraic
    expressions further.

Finally, we have:
‘‘‘
nlinarith [Real.sin_sq_add_cos_sq x, Real.sin_le_one x, Real.cos_le_one x]
‘‘‘

This is where I need to be careful. The ‘nlinarith‘ tactic is trying to use
   non-linear arithmetic with the Pythagorean identity ‘sin^2(x) + cos^2(x) =
   1‘ and the bounds on sine and cosine functions.

The issue might be that we’re using bounds (‘Real.sin_le_one x,
   Real.cos_le_one x‘) rather than equalities. When dealing with
   trigonometric identities, we often need exact relationships rather than
   just bounds. The Pythagorean identity is an equality, but we’re also
   including inequalities in our reasoning.

A better approach would be to focus on using the Pythagorean identity
   directly, possibly with additional facts about square roots. The ‘sqrt(2)‘
   in our expressions suggests we might need properties about square roots,
   such as ‘sq_sqrt‘ to handle expressions like ‘(\sqrt{2})^‘.

Additionally, we should ensure that we’re providing all the necessary facts
   to the arithmetic solver. For instance, we might need to explicitly
   include that ‘\sqrt{2} ≥ 0‘, which could be done with ‘Real.sqrt_nonneg 2‘.




                                      19
B.2. Rewriting Example

Input:
Complete the following Lean 4 code with explanatory comments preceding each
   line of code:

‘‘‘lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

/-- Prove that if 𝑛 ≥ 2, then 𝑛 distinct integers can be given such that the
   sum of any two of them is divisible by their difference.-/
theorem lean_workbook : ∀ n : N, 2 ≤ n → ∃ l : List Z, l.length = n ∧ ∀ x
   y, x ∈ l ∧ y ∈ l ∧ x ≠ y → (x + y) % (x - y) = 0      := by

Wrong Proof :
/-
     We need to prove that for any natural number \( n \geq 2 \), there exists a
      list of \( n \) distinct integers such that the sum of any two integers in
      the list is divisible by their difference.
     1. **Base Case**: When \( n = 2 \), we can choose the list \([0, 1]\). For
      any \( x \) and \( y \) in this list, if \( x \neq y \), then \( (x + y)
      \mod (x - y) = 0 \).
     2. **Inductive Step**: Assume the statement holds for some \( n \geq 2 \).
      We need to show it holds for \( n + 1 \). By the inductive hypothesis,
      there exists a list of \( n \) distinct integers \( l \) such that the sum
      of any two elements in \( l \) is divisible by their difference. We can
      add one more integer to this list and show that the new list still
      satisfies the condition.
     -/
     intro n hn
     -- Use a base case for n = 2
     use [0, 1]
     -- Verify that the base case satisfies the conditions
     simp
     -- Use Aesop to handle the general case
     <;> aesop

Revised Comments and Proofs:
/-We need to prove that for any natural number \( n \geq 2 \), there exists a
   list of \( n \) distinct integers such that the sum of any two integers in
   the list is divisible by their difference.

1. **Base Case**: When \( n = 2 \), we can choose the list \([0, 2]\). For
   any \( x \) and \( y \) in this list, if \( x \neq y \), then \( (x + y)
   \mod (x - y) = 0 \). For example, \( (0 + 2) \mod (0 - 2) = 2 \mod -2 = 0
   \).

2. **Inductive Step**: Assume the statement holds for some \( n \geq 2 \). We
   need to show it holds for \( n + 1 \). By the inductive hypothesis, there

                                         20
    exists a list of \( n \) distinct integers \( \{a_1, a_2, \ldots, a_n\} \)
    such that the sum of any two elements in this list is divisible by their
    difference. We can add one more integer to this list to form a new list of
    \( n + 1 \) integers. A good choice for the new integer is \( a_{n+1} =
    a_n + (n+1)! \). This ensures that for any \( i \) and \( j \) in the
    range \( 1 \leq i, j \leq n+1 \) with \( i \neq j \), the sum \( a_i + a_j
    \) is divisible by their difference \( a_i - a_j \). This is because \(
    (a_i + a_j) - (a_i - a_j) = 2a_j \), and since \( a_j \) is an integer, \(
    2a_j \) is always divisible by \( a_i - a_j \).

Thus, the list \( \{a_1, a_2, \ldots, a_n, a_{n+1}\} \) satisfies the
    condition, completing the inductive step.
-/
-- Introduce the natural number n and the assumption that n ≥ 2
   intro n hn
   -- Use a construction to construct the list of integers
   use List.replicate n 0
   -- Simplify the conditions given the assumption n ≥ 2
   simp [hn, List.length, List.mem_replicate, List.mem_range, List.mem_filter]
   -- Use Aesop to complete the proof
   <;> aesop"

Claude CoTs:
Let me verify my proof for this problem about distinct integers with
   divisibility properties. . .

Looking at my current solution, I’m trying to prove that for any n ≥ 2, there
   exist n distinct integers where the sum of any two is divisible by their
   difference.

Wait, I see an issue here. I’ve used ‘[0, 1]‘ as my example list, but let me
   check if this actually satisfies the condition:
- For x = 0 and y = 1: (x + y) % (x - y) = (0 + 1) % (0 - 1) = 1 % (-1) = 0?

Let me verify this calculation. We have 1 % (-1) which should be the
   remainder when 1 is divided by -1. Since -1 divides 1 as -1 × (-1) = 1,
   the remainder is 0. So this seems correct.

But wait, there’s another issue. I’ve only constructed a list for n = 2, but
    my proof needs to work for any n ≥ 2. The line:
‘‘‘
use [0, 1]
‘‘‘
only provides a list of length 2, but I need to handle cases where n > 2 as
    well.

I need to generalize my construction. Perhaps I should create a list of
   length n instead of just assuming the base case will handle everything.
   The ‘simp‘ and ‘aesop‘ tactics might not be able to automatically
   construct this list for arbitrary n.

Let me reconsider this approach. . . What if I use a more general construction?
   I could use ‘List.replicate n 0‘ to create a list of n zeros. But then all
   elements would be the same, and the problem requires distinct integers.



                                       21
Actually, I should think more carefully about what list would satisfy the
   divisibility condition. If I have integers a and b where a ≠ b, then I
   need (a + b) % (a - b) = 0.

For the general case, I might need to use a more sophisticated construction
   like arithmetic sequences or something based on factorials to ensure the
   divisibility property holds.

The issue with my current proof is that I’m not providing a general
   construction for n elements - I’m only handling n = 2. And even if ‘aesop‘
   could somehow extend this, I haven’t given it enough guidance on how to
   construct the larger list.

To fix this, I should:
1. Either provide an explicit construction for arbitrary n
2. Or use induction properly, showing how to extend from n to n+1 elements

I think I need to reconsider what list would work for this problem. Maybe
   something like powers of 2, or a list where consecutive elements have a
   specific relationship? The factorial approach mentioned in my comment
   might be promising - adding elements like a1 , a2 , . . ., a𝑛 where each new
   element is constructed to maintain the divisibility relationship with all
   previous elements.

I should try constructing a list like [0, 1!, 2!, . . ., (n-1)!] or something
   similar and verify that it satisfies the divisibility condition. This
   would give me distinct integers with potentially useful divisibility
   properties.



C. RL Details
Figure 6 shows the overall distribution of valid proofs in pass@32 testing. We collect the
distribution base on our Leanabell-Prover-GD-SFT model.




                                           22
                       40

                       35

                       30
Ratio of samples (%)




                       25

                       20

                       15

                       10

                       5

                       0
                            1-2 3-4 5-6 7-8 9-10 11-12 13-14 15-16 17-18 19-20 21-22 23-24 25-26 27-28 29-30 31-32
                                                             Num of pass@32
 Figure 6 | Distribution of valid proofs in pass@32. We calculate this distribution based on the
 Leanabell-Prover-GD-SFT model. To build this set, we remain the formal statements who has at
 least sampled proofs are valid by Lean 4 compiler.




                                                                  23
