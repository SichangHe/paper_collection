                                              CuDIP: Enhancing Theorem Proving in LLMs via
                                               Curriculum Learning-based Direct Preference
                                                              Optimization

                                                     Shuming Shi1 Ruobing Zuo1 Gaolei He2 Jianlin Wang2
                                                                 Chenyang Xu1 Zhengfeng Yang1
arXiv:2502.18532v1 [cs.AI] 25 Feb 2025




                                                            1
                                                                East China Normal University, 2 Henan University
                                                        {smshi, rbzuo}@stu.ecnu.edu.cn, {hegaolei, jlwang}@henu.edu.cn,
                                                                       {cyxu, zfyang}@sei.ecnu.edu.cn


                                                                                            Abstract
                                                  Automated theorem proving (ATP) is one of the most challenging mathematical reasoning tasks for
                                              Large Language Models (LLMs). Most existing LLM-based ATP methods rely on supervised fine-tuning,
                                              which results in a limited alignment between the theorem proving process and human preferences. Direct
                                              Preference Optimization (DPO), which aligns LLMs with human preferences, has shown positive effects
                                              for certain tasks. However, the lack of high-quality preference data for theorem proving presents a
                                              significant challenge. In this paper, we innovatively apply DPO to formal automated theorem proving and
                                              introduces a Curriculum Learning-based DPO Iterative Theorem Proving (CuDIP) method. Specifically,
                                              we propose a method for constructing preference data which utilizes LLMs and existing theorem proving
                                              data to enhance the diversity of the preference data while reducing the reliance on human preference
                                              annotations. We then integrate this preference data construction method with curriculum learning to
                                              iteratively fine-tune the theorem proving model through DPO. Experimental results on the MiniF2F and
                                              ProofNet datasets demonstrate the effectiveness of the proposed method.


                                         1    Introduction
                                         Despite the success of LLMs in various fields [14, 26, 44, 51], they still exhibit significant limitations in
                                         mathematical reasoning tasks, particularly in theorem proving. Enhancing the performance of LLMs in
                                         these tasks remains a challenging problem, especially for automated theorem proving in strictly formalized
                                         interactive theorem provers (ITPs) such as Lean [10] and Isabelle [34]. Many studies integrate LLMs with
                                         ITPs for automated theorem proving. Existing approaches generally fall into two categories: using LLMs
                                         to provide stepwise proof strategies combined with search algorithms to complete proofs [15, 25, 36], and
                                         leveraging LLMs to independently or informally generate complete proofs [21, 43]. While these methods
                                         have achieved some success, most rely on supervised fine-tuning, resulting in limited alignment with human
                                         preferences, and the effectiveness of theorem proving remains constrained.
                                         In recent years, LLM fine-tuning methods aligned with human preferences have gained significant attention.
                                         Recent studies demonstrate that preference-based optimization for LLM fine-tuning can yield substantial
                                         benefits [40, 51]. Reinforcement Learning with Human Feedback (RLHF) [9] is a well-established and effective
                                         method for aligning models with human preferences, typically consisting of two steps: (1) training a reward
                                         model, and (2) optimizing it using reinforcement learning methods such as PPO [39]. However, this approach
                                         has two primary limitations: 1) it is relatively complex; and 2) it entails significant computational overhead.
                                         To address the aforementioned issue, Direct Preference Optimization (DPO) [38] offers a simpler and more


                                                                                                1
efficient alternative. DPO eliminates the need for training a reward model, directly optimizing from preferences,
which makes it both straightforward and effective. DPO has shown promising results in certain mathematical
reasoning tasks [28, 33], but has yet to be applied to theorem proving tasks. However, a key challenge
for preference-based optimization methods in LLM fine-tuning is the requirement for high-quality human
preference labels, which are difficult to obtain.
To overcome the challenges mentioned above, this paper proposes a method for automated theorem proving
that combines DPO and curriculum learning, named Curriculum Learning-based DPO Iterative Theorem
Proving (CuDIP). To the best of our knowledge, this is the first work to integrate DPO with automated
theorem proving, filling a gap in DPO-based automated theorem proving. To address the challenge of
insufficient theorem proving preference data, this paper proposes a method for constructing preference data
based on fine-grained scoring by LLMs, which reduces the reliance on human annotations by utilizing LLMs
for preference data construction, and enhances the diversity of positive samples in the generated preference
data through the incorporation of fine-grained preference scoring. Using the constructed preference data
in conjunction with curriculum learning, we propose a process for iteratively training a prover based on
DPO, which enhances the LLM’s ability to solve difficult problems through progressively challenging DPO
iterations. Specifically, we categorizing automated theorem proving problems into curriculum data based
on predefined difficulty levels, and iteratively construct and fine-tune the DPO preference data following
the principles of curriculum learning. Experimental results indicate that the pass rate reaches 38.5% on the
MiniF2F dataset and 12.7% on the ProofNet dataset, surpassing the baseline methods and highlighting the
superior performance of the proposed method.
Our contributions can be summarized as follows:
    • We propose a method for constructing DPO preference data based on fine-grained preference scoring
      by Large Language Models (LLMs), which facilitates the generation of diverse preference data while
      reducing reliance on human annotations.
    • Based on the proposed preference data construction method and curriculum learning, we introduce
      Curriculum Learning-based DPO Iterative Theorem Proving (CuDIP) method, which enhances the
      capability of LLMs in autumated theorem proving.
    • Experimental results demonstrate that the proposed method outperforms all baseline approaches,
      achieving a maximum improvement of 7.4% on the MiniF2F-valid benchmark, thereby effectively
      enhancing the theorem proving capabilities of LLMs.


2     Related Works
Automated Theorem Proving with LLMs. The rapid advancement of Large Language Models (LLMs)
has spurred significant progress in automated theorem proving. Various approaches integrate interactive
theorem provers (ITP) such as Lean [11], Isabelle [34], and Metamath [31] with language models. A prominent
method, exemplified by GPT-f [36], involves the language model generating the next proof step based on
the current proof state, followed by tree search to find a complete proof for the theorem. PACT [15] jointly
trains a language model with a strategy prediction objective for interactive theorem proving, where the
auxiliary task for extracting self-supervised signals is used. HTPS [25] improves the automated theorem
proving process by enhancing the MCTS-based proof search strategy. Another approach employs LLMs to
derive the complete proof of a theorem, either directly or with the assistance of informal proof languages
[21, 27, 43]. However, most approaches rely on supervised fine-tuning (SFT), which may not align well with
human preferences, potentially limiting their proving capabilities.
Aligning LLMs with Human Preference. Reinforcement Learning from Human Feedback (RLHF)
[9] is a classical and effective method for aligning LLMs with human preferences. This approach involves
initially training a reward model, followed by optimization using reinforcement learning algorithms such as
PPO [39], leading to substantial success in models like ChatGPT [2, 7, 37], LLaMA [12, 42], and Claude [5].


                                                       2
However, using PPO for RLHF is a complex and computationally expensive process. Motivated by this, Direct
Preference Optimization (DPO) [38] has emerged as an effective alternative. DPO directly optimizes using
preference data, without the need to train a reward model. Several works [3, 13, 18, 24, 45, 48] have proposed
variations based on DPO. The simplicity and efficiency of DPO have enabled its application in various
downstream tasks, such as mathematical reasoning [22, 29, 46], multimodal tasks [30], and summarization
[38]. However, DPO still relies on high-quality preference labels to generate preference data, which requires
costly manual annotation. In this paper, we propose a method for constructing DPO preference data and the
generated preference data is utilized in DPO iterative training to enhance the theorem proving capabilities of
LLMs.
Curriculum Learning. Curriculum learning [6] is a method that simulates the human learning process by
progressing from simpler to more complex tasks. Chang et al. [8] applied curriculum learning to data-to-text
generation, achieving improvements in generation quality. By strategically organizing the learning trajectory,
curriculum learning enhances model performance or training efficiency and has shown promise in mathematical
reasoning tasks such as theorem proving. Polu et al. [35] introduced a curriculum of progressively harder
statements by synthesizing inequalities with increasing difficulty, while LeanAgent [23] categorized theorems
into three levels of complexity and utilized curriculum learning to train on mathematical repositories. In this
paper, we propose a curriculum learning iterative training method based on the difficulty of theorem proof
data and demonstrate its effectiveness.


3     Preliminaries and Notation
3.1    Preliminaries
Theorem Proving in Lean. Lean [10, 32] is a reliable interactive theorem proving assistant. Unlike natural
language-based theorem proving, Lean requires a more rigorous proof process. Specifically, the theorem
proving in Lean is interactive, where each step is carefully checked. In Lean, the theorem statement serves as
the initial goal, and each formalized proof strategy, called a ”tactic”, is applied to reach new subgoals. The
proof is considered complete when the ”no goals” state is reached.
Direct Preference Optimization (DPO). DPO [38] is an offline reinforcement learning method that
aligns the outputs of Large Language Model (LLM) with human preferences. Unlike Reinforcement Learning
from Human Feedback (RLHF) [9], which first trains a reward model and then applies reinforcement learning,
DPO directly optimizes based on preference data. Each sample in the DPO preference dataset is a triplet
(x, yw , yl ), where yw is the preferred response and yl is the dispreferred response, both corresponding to the
input prompt x. The training objective is to minimize the following loss:

                                                     h           πθ (yw |x)           πθ (yl |x) i
                 LDP O (πθ ; πref ) = −E(x,yw ,yl )∼D log σ β log              − β log              ,       (1)
                                                                  πref (yw |x)         πref (yl |x)

where D is the preference dataset, σ is the sigmoid function, πθ is the model to be optimized, initialized as
πref , and β is a hyperparameter used to control the degree of divergence between πθ and πref .

3.2    Problem Definition
This paper investigates the problem of automated theorem proving in the Lean language. The theorem
proving process can be abstracted as a tree search process, where the root node represents the theorem
statement to be proven. Each node in the tree corresponds to a proof state s (i.e., a proof subgoal and
corresponding premises), and each edge represents a proof tactic t. The initial state s0 represents the target
theorem statement to be proved. Finding a valid proof for s0 entails identifying a complete path starting
from s0 that successfully resolves the proof goals along the path.



                                                          3
       Stage 1: Preparation                        Stage 2: Preference data generation


          Theorem Data
                   splitting                                           Fine-Grained
                                                   proof tactic
                                Prover Model                         Preference Scoring    Score Data
                                                    samples

                                  DPO          Stage 3: Curriculum-based DPO Iteration           SFT
          Curriculum Data
                   SFT
                                 Preference Data         Filtering
                                                             &
                                                         Pairing
            Base Prover                                                    Preference        Score
                                                                             Score          Generator

Figure 1: Overview of Curriculum Learning-based DPO Iterative Theorem Proving (CuDIP). Stage 1:
Preparation. The original data is partitioned to create curriculum data, and the base prover is trained using
Supervised Fine-Tuning (SFT). Stage 2: Preference Data Generation. A score generator is trained to
assign fine-grained scores to candidate strategies for a given proof state, followed by filtering and pairing to
generate preference data. Stage 3: Curriculum-based DPO Iteration. The prover model undergoes
iterative DPO fine-tuning based on the generated preference dataset, refining both the preference data and
the prover model through successive iterations.


3.3    Notation
In this paper, we define D as the existing formalized theorem dataset with complete proof steps, and
C = {C1 , C2 , ..., Cn } as the curriculum dataset derived from D. P represents the prover model, where Pn
denotes the prover model at the n-th iteration, and P0 refers to the base prover obtained through supervised
fine-tuning (SFT) of the base model. G represents the score generator model used to produce preference data,
and Gn denotes the score generator model at the n-th iteration.
The theorem proving state at step i is denoted as si . di denotes the distance from si to completing the proof,
and DIFi represents the difficulty of si . T represents the set of all candidate tactics for a given proof goal.
SC denotes the dataset of corresponding preference scores for the candidate tactics in T . DP represents the
preference dataset for DPO.


4     Methodology
In this section, we introduce the proposed Curriculum Learning-based DPO Iterative Theorem Proving
(CuDIP). First, we present our key insights and an overview of the framework of the proposed CuDIP method,
which consists of three stages: (1) Preparation, (2) Preference Data Generation, and (3) Curriculum-based
DPO Iteration. Subsequently, we provide a detailed introduction to each of these stages.

4.1    Key Insights and Framework Overview
Our proposed approach is based on the following observations and assumptions.
    1. The preference-based LLM fine-tuning method DPO can be applied to theorem-proving tasks in LLMs
       to enhance reasoning capabilities and align better with human preferences.
    2. Similar to the human learning process, where knowledge is acquired progressively from simple to


                                                        4
      complex, training LLMs in a stepwise manner—from easy to difficult—may enhance their learning
      process and improve their ability to tackle more complex problems.
   3. The off-the-shelf expert data from the theorem proving process can serve as positive examples for DPO
      training. Additionally, existing language models can generate counterexamples and more diverse DPO
      training data based on the available theorem-proving data.
   4. When constructing DPO preference data, applying more fine-grained preference scoring to the data
      prior to forming preference pairs enhances the diversity of positive examples in the preference data.
Based on the aforementioned key insights, we propose a curriculum learning-based DPO iterative theorem
proving method (CuDIP) for the theorem proving problem defined in Section 3.2. To address the lack of
preference data in theorem proving, we propose a fine-grained scoring-based preference data generation
method, which utilizes existing theorem proving data and LLMs to generate more diverse preference data,
thereby reducing the reliance on human annotations. We then apply curriculum learning-based DPO iteration
to the prover, leveraging the proposed preference data generation method and curriculum learning.
Figure 1 gives an overview of our proposed CuDIP method. Specifically, the overall algorithm can be divided
into the following three stages:
Stage 1: Preparation. The existing formal theorem proving dataset D is partitioned based on the difficulty
of the tasks to construct a curriculum learning dataset C. The base model of the prover is then fine-tuned in
a supervised manner using the entire curriculum learning dataset C, resulting in the base prover P0 .
Stage 2: Preference Data Genertion. (1)Based on the current prover model and a subset of the new
round of curriculum learning data Cn , the preference score data SC 0 for training the score generator is derived
through Fine-Grained Preference Scoring (FGPS) process. (2)Supervised fine-tuning (SFT) is applied to the
current generator model using SC 0 , resulting in a new score generator model Gn . (3)Gn is then used to score
the candidate tactics across all states in Cn , and the preference dataset DP is obtained through filtering and
pairing.
Stage 3: Curriculum-based DPO Iteration. The current prover model is fine-tuned using the generated
preference data DP through the DPO method. Stage 2 and 3 are then repeated iteratively until no further
performance improvement is observed.
Next, we will provide a detailed technical description of the three stages of the proposed method.

4.2    Stage 1: Preparation
Before introducing the process of constructing curriculum data, we first define two concepts.
Definition 1. (Distance). For a given proof tree T of a theorem, the distance of a proof state s is defined as
the number of proof tactics that need to be executed from s to the completion of the proof (i.e., reach the ”no
goals” state in Lean).
Definition 2. (Difficulty). The difficulty of resolving a proof goal s is defined as the distance in the proof
tree from s to the final proof goal.
Curriculum Data Construction. The curriculum dataset C is derived by partitioning the original theorem-
proving dataset D based on increasing difficulty values. Specifically, for each theorem and its corresponding
proof process in D, we extract the proof state s at each step of the proof process and the corresponding
subsequent proof tactic t. We then calculate the difficulty DIFi of each proof state si . According to definition
Definition 2 , DIFi of si is defined as the distance di . This process results in intermediate data composed of
triplets, Dtriplet , which can be formally expressed as:


                                  Dtriplet = {(si , ti , DIFi ) | i = 1, 2, . . . , n},                       (2)



                                                           5
where si represents the current theorem proving state, ti denotes the next proving tactic of si , and DIFi
indicates the difficulty of si .
Then, divide the dataset Dtriplet into subsets in ascending order of DIFi . This results in a curriculum dataset
C organized from easy to hard, which can be formally expressed as:


                                C = {Cn | n ∈ {DIFi | (si , ti , DIFi ) ∈ Dtriplet }},                           (3)
                                        Cn = {(si , ti , DIFi ) | DIFi = n},                                     (4)

where C is the set of all subsets Cn , each corresponding to a unique difficulty level n, ensuring that triplets
with the same difficulty are grouped together. In the subsequent training process, further processing is
performed based on dataset C.
Base Prover Training. To achieve better proving performance, we first train the base model used as the
prover model before the subsequent iterations. The entire curriculum learning dataset C is used to perform
supervised fine-tuning (SFT) on the base model, resulting in the base prover P0 .
After obtaining the curriculum learning data and the base prover, we next construct a preference dataset for
DPO fine-tuning.

4.3    Stage 2: Preference Data Generation
We propose a method for constructing preference data by leveraging LLM and existing formal theorem-proving
datasets. First, we define a scoring rule and assign fine-grained preference scores to each theorem proof
state and its corresponding candidate tactics in curriculum dataset acheived in Section 4.2. Next, the data
is filtered and paired based on the scores to form preference pairs, resulting in the final DPO preference
dataset. To enhance the efficiency of the data generation process, we introduce a score generator during the
preference scoring stage, replacing manually defined scoring rules. The proposed method offers the following
benefits: (1) reducing reliance on human annotations by utilizing LLMs for preference data construction, and
(2) enhancing diversity of positive samples through fine-grained preference scoring. The method proceeds as
follows.
Tactic Samples Generation. For each proof state s in the formalized course dataset Cn , k candidate
tactics are generated using the current prover model Pn−1 , forming a candidate tactic set T = {t1 , t2 , ..., tk } .
Fine-Grained Preference Scoring (FGPS). For the candidate tactic set T originating from proof state s,
all tactics in T are evaluated using the following scoring process.
   1. Execute each candidate tactic from s to reach a new proof state and perform nattempt subsequent proof
      search attempts using the current prover Pn−1 and Monte Carlo Tree Search (MCTS).
   2. The score for a given candidate tactic t of proof state s is calculated using the following equation:
                                                                  nsuccess
                                                Score (t | s) =            ,                                     (5)
                                                                  nattempt

      where nsuccess represents the number of successful proofs found after executing the proof tactic t, and
      nattempt is the number of subsequent proof search attempts for each candidate tactic.
As shown in Figure 2, an example of the proposed fine-grained scoring process is provided. However, The
above scoring process necessitates multiple MCTS search attempts for each proof state, incurring significant
time costs. Therefore, we randomly select a subset of the course data Cn for preference scoring to obtain the
original score data SC 0 , and introduce a score generator to score the remaining data in Cn .
REMARK. For the remaining unscored data, language model-based scoring replaces the proof search scoring
process, improving the efficiency of preference data construction.


                                                          6
                                                    abc:ℕ
                                                    ⊢a+b+c=c+b+a



                                     : ring_nf           : rw [add_comm]                   : simp


                               no goals
                                                   abc:ℕ
                                                   ⊢ c + (a + b) = c + b + a
                                                                                ... a⊢ ab +c :bℕ+ c = c + b + a



                                                                       ...
                                                                                     proof attempts




                                                             ...   no goals             ←              +1



                                                       ...

Figure 2: An example of fine-grained preference scoring of all candidate tactics for the initial state of the
Lean theorem (a b c: N): a + b + c = c + b + a.


Score Generator Training. Using SC 0 , the existing language model Gn−1 undergoes SFT to produce the
score generator Gn . The score generator is then used to evaluate the remaining data, resulting in the final
scoring dataset SC, which can be expressed as:

                                         SC = {(si , Ti ) | i = 1, 2, . . . , x},                                 (6)
                                                              
                                          (j)         (j)
                                  Ti = {(ti , Score ti | si ) | j = 1, 2, . . . , k}.                             (7)

Where si represents the i-th proof state in Cn , Ti is the set of candidate proof tactics of si and their
                                   (j)
corresponding preference scores, ti denotes the j-th candidate tactic for si , x is the total number of proof
states in Cn , and k is the number of candidate tactics for a given state.
Filtering and Paring. Perform data filtering and pairing on the dataset SC, which contains all states
along with their corresponding candidate tactics and tactic preference scores. Specifically, for a given proof
state s, candidate tactics from its tactic set T are selected for pairwise comparison if the difference in their
preference scores exceeds a certain threshold Th. A preference pair {s, tw , tl } is considered valid if the
following conditions are met:

                                   Score(tw |s) > Score(tl |s), ∆Scoretw ,tl > Th,                                (8)

where ∆Scoretw ,tl = |Score(tw |s) − Score(tl |s)|.
After the filtering and pairing process, all the preference data (s, tw , tl ) satisfying the conditions constitute
the preference data set DP , which can be expressed as:
                                                     n                 oN
                                                                   (i)
                                                 DP = s(i) , t(i)
                                                              w , tl      ,                                       (9)
                                                                               i=1

where N is the number of all qualified preference pairs in Cn , and si is the state corresponding to the
preference candidate tactic pair.




                                                                   7
Algorithm 1 Curriculum-based DPO Iteration
Input: Curriculum dataset C = {C1 , C2 , . . . , CI }, the base prover model P0 obtained from SFT, Base score
    generator model G0
Output: PI : The final prover model
 1: Initialize: Pref ← P0 , Pθ ← Pref
 2: for n = 1 to I do
 3:    Use Cn as curriculum data.
 4:    T ← Sample candidate tactics from Cn
 5:    SC 0n ← Apply fine-grained scoring to a subset of Cn to obtain scoring dataset
 6:    Gn ← SFT on score generator Gn−1 with SC n0 to obtain new score generator
 7:    SC n ← Use Gn to score the remaining data in Cn and get scoring dataset
 8:    Filter and pair data in SC to form preference pair dataset DP
 9:    Perform DPO on Pn−1 : Pref ← Pn−1 , Pθ ← Pref
10:    Pn ← Minimize the loss LDP O (Pθ , Pref ) to update Pθ
11: end for
12: return Pn



4.4     Stage 3: Curriculum-based DPO Iteration
DPO Fine-tuning. After obtaining the preference dataset DP , we fine-tune the prover model using DPO.
For each triplet (s, tw , tl ) in DP , it corresponds to the triplet (x, yw , yl ) in the DPO preference data discussed
in Section 3.1, where s corresponds to an input, tw denotes the preferred response, and tl denotes the
dispreferred response. We then minimize the optimization objective of Section 3.1, where πref corresponds to
the prover model before DPO fine-tuning.
Curriculum-based Iteration (CI). After obtaining the new prover model, the process enters a new round
of curriculum-based DPO iteration, as outlined in Algorithm 1. Specifically, for the n-th iteration, the dataset
Cn , with difficulty value n, is used as the curriculum data. Tactic sampling is performed using the prover
model Pn−1 from the previous iteration, and fine-grained scoring is applied to a subset of the data in Cn
to obtain the scoring dataset SC 0n . This dataset is used to fine-tune the score generator Gn−1 from the
previous round through supervised learning, yielding the new score generator Gn . Next, Gn is used to score
the remaining data in Cn , resulting in the scoring dataset SC n . Data filtering and pairing are then performed
on SC n to obtain the preference pair dataset, followed by a new round of DPO. In the first iteration, Pref is
the base prover P0 obtained after SFT. In the n-th iteration, Pref is Pn−1 .


5      Experiments
5.1     Experimental Setup
Datasets and Metric. We use the Lean 4 formalized theorem-proving dataset Mathlib41 as the training set
D. To evaluate the performance of the proposed method, we used datasets MiniF2F [49] and ProofNet [4] as
evaluation benchmarks.MiniF2F consists of 488 problems derived from high school mathematics competitions,
with 244 problems in both the test and validation sets. These problems primarily include those sourced from
the MATH [17] dataset, high school mathematics competitions such as AMC, AIME, and IMO, as well as a
set of carefully crafted problems designed to match the difficulty level of those in the competitions. ProofNet
includes 371 examples, each comprising a formal theorem statement, a natural language theorem statement,
and a natural language proof in Lean 3. We manually translated the corresponding Lean 3 proofs in ProofNet
into Lean 4, resulting in 360 examples that are suitable for interaction with Lean 4. We use pass@k as the
    1 https://github.com/leanprover-community/mathlib4




                                                          8
evaluation metric, which represents the probability that the model successfully finds at least one valid proof
within k proof attempts.
Baselines We selected different models as the prover model and score generator model to evaluate the
effectiveness of the proposed method. Specifically, we chose Mathstral-7B-v0.1[20], Llama3.1-8B-Instruct[12],
and Phi-3.5-mini-instruct [1] as the prover models, and Llama3.1-8B-Instruct, gemma-2-9b-it[41], and gemma-
2-2b-it as the score generator models for the experiments. We used the entire Mathlib4 dataset for SFT and
directly tested the base model, with these two approaches serving as baselines for comparison. Both baseline
methods and the proposed method were tested in the Lean 4 environment to assess their performance.
Implementation details The prover’s sampling parameters remain consistent throughout the entire process.
We set its temperature to 1.0 and the number of candidate candidate tactics k to 32 for each proof state. In
the Preference Data Generation stage, for each curriculum dataset Cn , we randomly select 2000 data points
to interact with the Lean environment. After applying the candidate tactic to the current proof state, we
obtain a new proof state. Starting from this updated state, we perform 10 search attempts (nattempt = 10)
and use the frequency of successful proofs as the score of the tactic. For the remaining unscored data, we use
the trained score generator Gn to evaluate the candidate tactic, setting the temperature to 0.1. For each
candidate tactic in each proof state, we perform 10 sampling iterations and compute the average score of
these samples as the tactic’s final score. During the DPO fine-tuning process, the hyperparameter β in the
loss function is set to 0.1. In the evaluation phase, we limit the search time for each theorem to 300 seconds
and employ standard best-first search algorithm to find proofs[16, 47]. For further details, please refer to
Appendix B.

5.2    Main Results
To validate the effectiveness of the proposed method, we apply the CuDIP method to three different model
groups and compare the results with existing baseline methods as well as the corresponding models after
fine-tuning with SFT. The proof pass rates on the MiniF2F and ProofNet are presented in Table 1, where
our method corresponds to the results of the fourth iteration. As shown in Table 1, the use of the CuDIP
method leads to significant improvements over the baseline results. For instance, when using Mathstral
as the prover and Llama-3.1 as the score generator with CuDIP, the pass@1 on MiniF2F reaches 38.5%,
representing a 4.1% improvement over the baseline method after SFT. Additionally, when using Llama-3.1 as
the prover and Gemma2 as the score generator, the highest performance improvements were observed on
both benchmarks, with a 7.4% increase on MiniF2F and a 2.2% increase on ProofNet. In the experiments
with the remaining group of models, the proof pass rate also showed notable improvements. These results
demonstrate the effectiveness of the proposed CuDIP method.

Table 1: Proving success rates (Pass@1) on the MiniF2F and ProofNet datasets. The superscript * denotes
the model as a prover, and † indicates it as a score generator. The highest success rates are bolded.


       Method                                             MiniF2F-valid   MiniF2F-test     ProofNet

       Mathstral                                             23.3%            27.0%           7.2%
       Mathstral + SFT                                       34.4%            34.4%          11.1%
       Mathstral* + Llama-3.1† + CuDIP(ours)                 38.5%            38.5%          12.7%
       Llama-3.1                                             20.1%            22.5%           1.7%
       Llama-3.1 + SFT                                       28.6%            32.3%           9.4%
       Llama-3.1* + gemma2† + CuDIP(ours)                    36.0%            36.8%          11.6%
       Phi-3.5                                                3.7%             3.7%           0%
       Phi-3.5 + SFT                                         29.1%            32.7%          7.7%
       Phi-3.5* + gemma2† + CuDIP(ours)                      33.2%            36.4%          9.7%



                                                      9
                                                 0 L Q L )  )  Y D O L G                                                                          0 L Q L )  )  W H V W                                                                    3 U R R I 1 H W
                                                                                                                                            0 D V W U D O
                                                                                                                                            / / D P D                                                              
                                                                                                                                              3 K L   
                                                                                                                             
                                                                                                                                                                                                                        
       $ F F X U D F \   




                                                                                                     $ F F X U D F \   




                                                                                                                                                                                              $ F F X U D F \   
                                                                                                                               
                                 
                                                                                                                                                                                                                      
                                 
                                                                                                                                                                                                                       
                                                                             0 D V W U D O                                                                                                                                                                            0 D V W U D O
                                                                           / / D P D                                                                                                                                                                           / / D P D   
                                                                             3 K L                                                                                                                                                                                3 K L   
                                                                                                                               
                                                                                                                                                                                                                                                                           
                                                 , W H U D W L R Q  U R X Q G                                                                     , W H U D W L R Q  U R X Q G                                                          , W H U D W L R Q  U R X Q G

Figure 3: Comparison curves of different iteration rounds using the CuDIP method. The performance curves
depicting the proof success rates of the three model groups after four rounds of DPO iteration based on
curriculum learning, evaluated on the MiniF2F-valid, MiniF2F-test, and ProofNet benchmarks.

Table 2: Improvement in pass rates on MiniF2F and ProofNet at Pass@1 with Fine-grained Preference
Scoring (FGPS).


                                                    Model                               FGPS                                             MiniF2F-valid                         MiniF2F-test                                       ProofNet
                                                    Mathstral                             ✗                                                 35.2%                                 35.6%                                              11.6%
                                                    Mathstral                            ✓                                                  36.0%                                 36.0%                                              11.6%


In order to validate the effect of different iteration counts using the CuDIP method, we performed four rounds
of DPO iteration on three sets of models. The testing results of the models after each iteration are shown in
Figure 3. As illustrated in Figure 3, during the first four iterations, the model’s proof capabilities increase
with the number of iterations, thereby confirming the effectiveness of the proposed iterative method. The
specific test results of these three groups of models after four iterations can be found in Appendix A.

5.3               Ablation Studies
To separately investigate the effects of different components of the proposed CuDIP, we conducted ablation
experiments, testing: 1) the effectiveness of the fine-grained preference scoring based on the score generator,
and 2) the effectiveness of DPO iteration based on curriculum learning.
Fine-Grained Preference Scoring (FGPS). In order to verify the effectiveness of fine-grained preference
scoring during the construction of preference data, we used Mathstral as the prover model and tested two
conditions: one where Llama3.1 was used as the score generator in the preference data construction process,
and another where no score generator or scoring rules were applied for fine-grained scoring. The test results
on the MiniF2F and ProofNet benchmarks are presented in the Table 2 The use of the score generator
for fine-grained scoring significantly improved the model’s proof success rate, thereby demonstrating the
effectiveness of the proposed fine-grained preference scoring process.
Curriculum-based Iteration (CI). To validate the effect of Curriculum-based Iteration (CI), we combined
the curriculum data from the first four iterations and conducted one round of training. The results were
then compared with those obtained after four iterations of training. As shown in Table 3 , the test results on
MiniF2F after training with CI were 4.1%, showing an improvement of 2.1% compared to the results without
CI, which further verified the effectiveness of curriculum-based iteration.


                                                                                                                                                        10
Table 3: Improvement in pass rates for MiniF2F and ProofNet at Pass@1 with Curriculum-based Iteration
(CI).


              Model                         CI   MiniF2F-valid      MiniF2F-test     ProofNet
              Mathstral                     ✗       35.6%              36.4%            12.2%
              Mathstral(4 iterations)       ✓       38.5%              38.5%            12.7%


6    Conclusion
In this paper, we present a curriculum learning-based DPO iterative theorem proving method (CuDIP).
Specifically, we first introduce an effective preference data construction approach based on fine-grained
preference scoring by large language models (LLMs), which reduces the reliance on human annotations
and enhances the diversity of the preference data. Subsequently, we integrate the proposed preference
data construction method with curriculum learning to conduct iterative DPO training for the theorem
proving model. Experimental results demonstrate that the method proposed herein significantly improves the
performance of LLMs in theorem proving tasks and enhances their reasoning capabilities in the context of
theorem proving.


References
 [1] Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad Awan, et al. Phi-3
     technical report: A highly capable language model locally on your phone, 2024.
 [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
     Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report.
     arXiv preprint arXiv:2303.08774, 2023.
 [3] Mohammad Gheshlaghi Azar, Zhaohan Daniel Guo, Bilal Piot, Remi Munos, Mark Rowland, Michal
     Valko, and Daniele Calandriello. A general theoretical paradigm to understand learning from human
     preferences. In International Conference on Artificial Intelligence and Statistics, pages 4447–4455. PMLR,
     2024.
 [4] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev, and
     Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics, 2023.
 [5] Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain,
     Stanislav Fort, Deep Ganguli, Tom Henighan, et al. Training a helpful and harmless assistant with
     reinforcement learning from human feedback. arXiv preprint arXiv:2204.05862, 2022.
 [6] Yoshua Bengio, Jérôme Louradour, Ronan Collobert, and Jason Weston. Curriculum learning. In
     Proceedings of the 26th annual international conference on machine learning, pages 41–48, 2009.
 [7] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
     Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners.
     Advances in neural information processing systems, 33:1877–1901, 2020.
 [8] Ernie Chang, Hui-Syuan Yeh, and Vera Demberg. Does the order of training samples matter? improving
     neural data-to-text generation with curriculum learning. arXiv preprint arXiv:2102.03554, 2021.
 [9] Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep
     reinforcement learning from human preferences. Advances in neural information processing systems, 30,
     2017.




                                                      11
[10] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer. The lean
     theorem prover (system description). In Automated Deduction-CADE-25: 25th International Conference
     on Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceedings 25, pages 378–388. Springer,
     2015.
[11] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer. The lean
     theorem prover (system description). In Automated Deduction-CADE-25: 25th International Conference
     on Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceedings 25, pages 378–388. Springer,
     2015.
[12] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
     Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv
     preprint arXiv:2407.21783, 2024.
[13] Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff, Dan Jurafsky, and Douwe Kiela. Kto: Model
     alignment as prospect theoretic optimization. arXiv preprint arXiv:2402.01306, 2024.
[14] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi,
     Yu Wu, YK Li, et al. Deepseek-coder: When the large language model meets programming–the rise of
     code intelligence. arXiv preprint arXiv:2401.14196, 2024.
[15] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W Ayers, and Stanislas Polu. Proof artifact
     co-training for theorem proving with language models. arXiv preprint arXiv:2102.06203, 2021.
[16] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W. Ayers, and Stanislas Polu. Proof artifact
     co-training for theorem proving with language models. CoRR, abs/2102.06203, 2021.
[17] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
     and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv preprint
     arXiv:2103.03874, 2021.
[18] Jiwoo Hong, Noah Lee, and James Thorne. Orpo: Monolithic preference optimization without reference
     model. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing,
     pages 11170–11189, 2024.
[19] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
     Weizhu Chen. Lora: Low-rank adaptation of large language models. arXiv preprint arXiv:2106.09685,
     2021.
[20] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot,
     Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard
     Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée
     Lacroix, and William El Sayed. Mistral 7b, 2023.
[21] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée
     Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem provers
     with informal proofs. arXiv preprint arXiv:2210.12283, 2022.
[22] Fangkai Jiao, Chengwei Qin, Zhengyuan Liu, Nancy F Chen, and Shafiq Joty. Learning planning-based
     reasoning by trajectories collection and process reward synthesizing. arXiv preprint arXiv:2402.00658,
     2024.
[23] Adarsh Kumarappan, Mo Tiwari, Peiyang Song, Robert Joseph George, Chaowei Xiao, and Anima
     Anandkumar. Leanagent: Lifelong learning for formal theorem proving. arXiv preprint arXiv:2410.06209,
     2024.
[24] Xin Lai, Zhuotao Tian, Yukang Chen, Senqiao Yang, Xiangru Peng, and Jiaya Jia. Step-dpo: Step-wise
     preference optimization for long-chain reasoning of llms. arXiv preprint arXiv:2406.18629, 2024.



                                                    12
[25] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury Hayat, Thibaut
     Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural theorem proving. Advances
     in neural information processing systems, 35:26337–26349, 2022.
[26] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan
     Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. arXiv preprint
     arXiv:2305.20050, 2023.
[27] Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean Welleck. Lean-star: Learning to interleave thinking
     and proving. arXiv preprint arXiv:2407.10040, 2024.
[28] Zimu Lu, Aojun Zhou, Ke Wang, Houxing Ren, Weikang Shi, Junting Pan, Mingjie Zhan, and Hongsheng
     Li. Step-controlled dpo: Leveraging stepwise error for enhanced mathematical reasoning. arXiv preprint
     arXiv:2407.00782, 2024.
[29] Zimu Lu, Aojun Zhou, Ke Wang, Houxing Ren, Weikang Shi, Junting Pan, Mingjie Zhan, and Hongsheng
     Li. Step-controlled dpo: Leveraging stepwise error for enhanced mathematical reasoning. arXiv preprint
     arXiv:2407.00782, 2024.
[30] Navonil Majumder, Chia-Yu Hung, Deepanway Ghosal, Wei-Ning Hsu, Rada Mihalcea, and Soujanya
     Poria. Tango 2: Aligning diffusion-based text-to-audio generations through direct preference optimization.
     In Proceedings of the 32nd ACM International Conference on Multimedia, pages 564–572, 2024.
[31] Norman Megill and David A Wheeler. Metamath: a computer language for mathematical proofs. Lulu.
     com, 2019.
[32] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In
     Automated Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual Event,
     July 12–15, 2021, Proceedings 28, pages 625–635. Springer, 2021.
[33] Arka Pal, Deep Karkhanis, Samuel Dooley, Manley Roberts, Siddartha Naidu, and Colin White. Smaug:
     Fixing failure modes of preference optimisation with dpo-positive. arXiv preprint arXiv:2402.13228,
     2024.
[34] Lawrence C Paulson. Isabelle: The next 700 theorem provers. In Logic and computer science, volume 31,
     pages 361–386. Citeseer, 1990.
[35] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya Sutskever.
     Formal mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344, 2022.
[36] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving. arXiv
     preprint arXiv:2009.03393, 2020.
[37] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language
     models are unsupervised multitask learners. OpenAI blog, 1(8):9, 2019.
[38] Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea
     Finn. Direct preference optimization: Your language model is secretly a reward model, 2024.
[39] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
     optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.
[40] Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
     Dario Amodei, and Paul F Christiano. Learning to summarize with human feedback. Advances in Neural
     Information Processing Systems, 33:3008–3021, 2020.
[41] Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju,
     Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, Johan Ferret, Peter Liu, Pouya




                                                      13
    Tafti, et al. Gemma 2: Improving open language models at a practical size. ArXiv, abs/2408.00118,
    2024.
[42] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée
     Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient
     foundation language models. arXiv preprint arXiv:2302.13971, 2023.
[43] Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya Huang,
     Jing Xiong, Han Shi, Enze Xie, et al. Lego-prover: Neural theorem proving with growing libraries. arXiv
     preprint arXiv:2310.00656, 2023.
[44] Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
     Math-shepherd: Verify and reinforce llms step-by-step without human annotations. In Proceedings of the
     62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages
     9426–9439, 2024.
[45] Haoran Xu, Amr Sharaf, Yunmo Chen, Weiting Tan, Lingfeng Shen, Benjamin Van Durme, Kenton
     Murray, and Young Jin Kim. Contrastive preference optimization: Pushing the boundaries of llm
     performance in machine translation. arXiv preprint arXiv:2401.08417, 2024.
[46] Yifan Xu, Xiao Liu, Xinghan Liu, Zhenyu Hou, Yueyan Li, Xiaohan Zhang, Zihan Wang, Aohan Zeng,
     Zhengxiao Du, Wenyi Zhao, et al. Chatglm-math: Improving math problem-solving in large language
     models with a self-critique pipeline. arXiv preprint arXiv:2404.02893, 2024.
[47] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
     Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented language
     models. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, Advances
     in Neural Information Processing Systems, volume 36, pages 21573–21612. Curran Associates, Inc., 2023.
[48] Yongcheng Zeng, Guoqing Liu, Weiyu Ma, Ning Yang, Haifeng Zhang, and Jun Wang. Token-level direct
     preference optimization. arXiv preprint arXiv:2404.11999, 2024.
[49] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for formal
     olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.
[50] Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan Ye, and Zheyan Luo. LlamaFactory: Unified
     efficient fine-tuning of 100+ language models. In Yixin Cao, Yang Feng, and Deyi Xiong, editors,
     Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 3:
     System Demonstrations), pages 400–410, Bangkok, Thailand, August 2024. Association for Computational
     Linguistics.
[51] Daniel M Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B Brown, Alec Radford, Dario Amodei, Paul
     Christiano, and Geoffrey Irving. Fine-tuning language models from human preferences. arXiv preprint
     arXiv:1909.08593, 2019.




                                                    14
A     More Experimental Results
In this paper, we used three groups of models to verify our proposed method. For each group of models, we
performed 4 rounds of iterations. After each round of iteration, we tested the model. Table 4 shows the test
results of the model on the MiniF2F and ProofNet datasets. The results show that the accuracy of the model
gradually increases during the iteration process.

Table 4: Proof success rates for Curriculum Learning-based DPO Iterative Theorem Proving (CuDIP) on
MiniF2F and ProofNet with Lean at different iterations. Results of our CuDIP method after 4 iterations are
shown.


    Model                                     Iterations   MiniF2F-valid     MiniF2F-test      ProofNet
                                                   1          36.0%             36.0%             11.6%
                                                   2          36.4%             36.8%             12.5%
    Mathstral* + Llama-3.1† + CuDIP
                                                   3          37.7%             37.7%             12.7%
                                                   4          38.5%             38.5%             12.7%
                                                   1          31.9%             34.0%             10.8%
                                                   2          34.0%             35.2%             11.1%
    Llama-3.1* + gemma2† + CuDIP
                                                   3          35.6%             36.4%             11.6%
                                                   4          36.0%             36.8%             11.6%
                                                   1          30.3%             33.1%              8.6%
                                                   2          31.5%             34.8%              9.4%
    Phi-3.5* + gemma2† + CuDIP
                                                   3          32.7%             36.4%              9.7%
                                                   4          33.2%             36.4%              9.7%




B     Training Details
B.1    Training Tools
In this paper, we used supervised fine-tuning (SFT) and direct preference optimization (DPO) to train the
model. In terms of training tools, we used LlamaFactory[50], a unified framework that integrates a suite of
cutting-edge efficient training methods. It can help us focus more on the construction of the dataset without
worrying about the implementation of the model training code.

B.2    Base Prover Training
We used LlamaFactory to train the three basic models with SFT. The three models used the same prompt
template, see Appendix C for details. During training, we used the LoRA[19] method, which can help us save
training resources. We set the learning rate to 2.0 × 10−5 , the learning rate scheduler to cosine, the warmup
ratio to 0.03, and trained for 3 epochs. We set the floating point precision to bfloat16 and batch size to 4.

B.3    Score Generator Training
When generating training data for the score generator, we performed a Monte Carlo Tree Search (MCTS) on
each proof state in the subset of the curriculum learning data Cn . For each search, we set the number of
simulations to 1000 and limited the search depth to 10. We did not use a fixed value for the search time
limit, because as the number of iterations increases, the model’s ability gradually increases and the model’s
search time increases. We observed that when the model performs automatic theorem proving, it usually
succeeds within 60 seconds, and the probability of the model proving the theorem after that is very low.
This phenomenon is caused by the model’s insufficient long-chain reasoning ability, which is also one of the


                                                     15
challenges faced by large language models (LLMs) at this stage. In order to balance the quality and quantity
of training data when computing resources are limited, we limited the search time limit to 60 seconds in the
first round of iterations. For each subsequent round, we increased the search time limit by 30 seconds each
time, hoping that the model can perform a deeper search.

B.4    Filtering and Paring
After we score each tactic in the candidate tactic set for a proof state, we need to consider how to construct
a preferred data set for DPO training. For those tactics with non-zero scores, it means that after the current
proof state applies the tactic, the model has the probability of completing the subsequent proof. We use a
pair of tactics with a score difference of more than 0.5 as positive and counterexample in a dpo training data
set. The advantage of this method is that for any proof tactic, when constructing the DPO training data set,
it will not be used as both a positive example and a counterexample, which can be beneficial to the training
of the model. When conducting dpo training, we set β in the DPO loss function to 0.1, set the learning rate
to 5.0 × 10−6 , and trained for 1 epoch.


C     Prompt Templates
C.1     Prove Model Prompt Template
    Prompt Template

    <s>You are using Lean4 for theorem proving[INST] You will be provided with a
    json-formatted data describing the intermediate proof status of the Lean4 theorem.
    You need to give a prediction of a proof tactic based on the data description and
    your knowledge and experience about Lean4 proofs.
    The input json format description is as follows:
    {
        "current theorem state": <current theorem state description>
    }
    Your output must also be json-formatted data in the following format:
    {
        "predict tactic": <A proof tactic that complies with Lean4 syntax. The type
    is a string and the content cannot contain "sorry">
    }
    Your input:
    {
        "current theorem state": "$current theorem state"
    }
    Your output:


We apply this template to an actual proof state and replace the placeholders in the template about the
theorem proof state with specific values. Considering that the proof state of a theorem may contain multiple
proof goals, we set the upper limit of the number of model input tokens to 4096 and the upper limit of the
number of output tokens to 2048, which can meet the needs of the current task. It is worth mentioning that
in order to better help us extract the desired tactics from the model output, we limit the input and output of
the model to json format.
The following is a actual examples of prompts and the responses of the model:




                                                     16
   Input Example

   <s>You are using Lean4 for theorem proving[INST] You will be provided with a
   json-formatted data describing the intermediate proof status of the Lean4 theorem.
   You need to give a prediction of a proof tactic based on the data description and
   your knowledge and experience about Lean4 proofs.
   The input json format description is as follows:
   {
       "current theorem state": <current theorem state description>
   }
   Your output must also be json-formatted data in the following format:
   {
       "predict tactic": <A proof tactic that complies with Lean4 syntax. The type
   is a string and the content cannot contain "sorry">
   }
   Your input:
   {
       "current theorem state": "a b c : N\n h1 : b = 0\n ⊢ a + b + c = c + a"
   }
   Your output:


For the above input, LLM’s response is as follows

   Output Example

   {
        "predict tactic":     "norm num [h1 ]"
   }



C.2    Score Generator Prompt Template
   Prompt Template

    ### Task Description:
  You will be given a ‘tactic‘ generated by a model in the context of a Lean4 theorem
   proving process. Please score the ‘tactic‘ based on the following criteria, where:
  - 0 means the ‘tactic‘ cannot run in Lean4 syntax or does not affect the current
   proof state.
  - 1 means the ‘tactic‘ fully complies with Lean4 syntax and successfully completes
   the proof.
  - A value between 0 and 1 indicates the probability of the ‘tactic‘ completing the
   proof or significantly advancing the proof process.
   Do not provide any additional text, explanations, or responses. Only output the
   score which is a number between 0 and 1.

   ### Output Format:
  - A score (floating-point value):         A number between 0 and 1.

   #### Input:



                                                    17
    {
          "current theorem state":     "$current theorem state"
    }

    #### Generated ‘tactic‘:
    {
        "predict tactic": "$predict tactic"
    }

    ---

    ### Score:




D       Case Studies
D.1       mathd algebra 109
Theorem mathd algebra 109 in the valid validation set of Minif2f is defined as follows:

    Theorem Define

    theorem mathd algebra 109 (a b : R) (h0 : 3 * a + 2 * b = 12) (h1 : a = 4) : b = 0

Each time we replace the theorem state placeholder in the prompt with the intermediate state when proving
the theorem, and then use the proof tactic given by the model to prove the theorem.

    Example

    <s>You are using Lean4 for theorem proving[INST] You will be provided with a
    json-formatted data describing the intermediate proof status of the Lean4 theorem.
    You need to give a prediction of a proof tactic based on the data description and
    your knowledge and experience about Lean4 proofs.
    The input json format description is as follows:
    {
        "current theorem state": <current theorem state description>
    }
    Your output must also be json-formatted data in the following format:
    {
        "predict tactic": <A proof tactic that complies with Lean4 syntax. The type
    is a string and the content cannot contain "sorry">
    }
    Your input:
    {
        "current theorem state": "b : R\n h0 : 3 * 4 + 2 * b = 12\n b = 0"
    }
    Your output:

    {
          "predict tactic":    " linarith"



                                                    18
   }


Theorem mathd algebra 109 can be proved using two proof tactics, "subst h1 " and "linarith", but this does
not mean that there is only one way to prove the theorem. When the model predicts the tactics for the first
proof state, it will not only generate the tactic shown above, but also other proof tactics. If the proof tactic
of the first step, "subst h1 ", is replaced by "rw [h1 ] at h0 ", and the proof tactic of the second step is not
changed, the theorem can also be proved.

D.2     mathd numbertheory 109
The theorem is defined as follows

   Theorem Define

   theorem mathd algebra 109 (v : N → N) (h0 : ∀ n, v n = 2 * n - 1) : (
                                                                              P
                                                                                  k in Finset.Icc 1 100, v k)
   %7=4

   Step 1

   <s>You are using Lean4 for theorem proving[INST] You will be provided with a
   json-formatted data describing the intermediate proof status of the Lean4 theorem.
   You need to give a prediction of a proof tactic based on the data description and
   your knowledge and experience about Lean4 proofs.
   The input json format description is as follows:
   {
       "current theorem state": <current theorem state description>
   }
   Your output must also be json-formatted data in the following format:
   {
       "predict tactic": <A proof tactic that complies with Lean4 syntax. The type
   is a string and the content cannot contain "sorry">
   }
   Your input:
   {
       "current theorem state": "v : N → N h0 : ∀ (n : N), v n = 2 * n - 1 ⊢ (
                                                                                   P
   k ∈ Finset.Icc 1 100, v k) % 7 = 4"
   }
   Your output:

   {
        "predict tactic":       "norm num h0 "
   }


   Step 2

   <s>You are using Lean4 for theorem proving[INST] You will be provided with a
   json-formatted data describing the intermediate proof status of the Lean4 theorem.
   You need to give a prediction of a proof tactic based on the data description and




                                                      19
your knowledge and experience about Lean4 proofs.
The input json format description is as follows:
{
    "current theorem state": <current theorem state description>
}
Your output must also be json-formatted data in the following format:
{
    "predict tactic": <A proof tactic that complies with Lean4 syntax. The type
is a string and the content cannot contain "sorry">
}
Your input:
{
    "current theorem state": "v : N → N h0 :∀ (n : N), v n = 2 * n - 1 ⊢ (
                                                                            P
                                                                                x
∈ Finset.Icc 1 100, 2 * x - 1) % 7 = 4"
}
Your output:

{
    "predict tactic":   "rfl"
}




                                        20
