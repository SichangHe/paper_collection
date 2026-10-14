                                         Enhancing Neural Theorem Proving through Data Augmentation
                                                       and Dynamic Sampling Method
                                                                     Rahul Vishwakarma and Subhankar Mishra
                                                     National Institute of Science Education and Research, Bhubaneswar
                                                               Homi Bhabha National Institute, Mumbai, India
arXiv:2312.14188v2 [cs.AI] 15 Feb 2024




                                                                  {rahul.vishwakarma,smishra}@niser.ac.in


                                                                                            Abstract
                                                  Theorem proving is a fundamental task in mathematics. With the advent of large language
                                              models (LLMs) and interactive theorem provers (ITPs) like Lean, there has been growing interest
                                              in integrating LLMs and ITPs to automate theorem proving. In this approach, the LLM generates
                                              proof steps (tactics), and the ITP checks the applicability of the tactics at the current goal. The two
                                              systems work together to complete the proof. In this paper, we introduce DS-Prover, a novel dynamic
                                              sampling method for theorem proving. This method dynamically determines the number of tactics
                                              to apply to expand the current goal, taking into account the remaining time compared to the total
                                              allocated time for proving a theorem. Furthermore, to enhance the prediction capability of the LLM,
                                              we augment the training dataset by decomposing simplification and rewrite tactics with multiple
                                              premises into tactics with single premises. This gives the model more examples to learn from and
                                              helps it to predict the tactics with premises more accurately. We perform our experiments using the
                                              Mathlib dataset of the Lean theorem prover and report the performance on two standard datasets,
                                              MiniF2F and ProofNet. Our methods achieve significant performance gains on both datasets. We
                                              achieved a state-of-the-art performance (Pass@1) of 14.2% on the ProofNet dataset and a performance
                                              of 29.8% on MiniF2F, slightly surpassing the best-reported Pass@1 of 29.6% using Lean.


                                         1    Introduction
                                         Theorem proving in mathematics is a formal and systematic approach to establishing the validity of
                                         mathematical statements, known as theorems. It involves demonstrating that a given mathematical
                                         proposition is true based on a set of axioms and logical rules. The process typically follows a structured
                                         and rigorous method, and it can be done either manually or with the assistance of computer programs
                                         called interactive theorem provers (ITPs). Some popular ITPs include Coq [2], Metamath [12], Isabelle
                                         [15], HOL Light [6], and Lean [14]. ITPs are commonly used for the verification of mathematical proofs
                                         and formalization of mathematics.
                                             Automating the generation of proofs of mathematical theorems has been a topic of interest for a
                                         long time [22, 3]. When using machine learning to generate proofs of theorems, two important features
                                         of interactive theorem provers (ITPs) are used: formalized proofs, which are used as the dataset for
                                         training the machine learning model, and the ability to verify the correctness of proofs. To automate the
                                         generation of mathematical proofs, we combine an ITP with a large language model (LLM). The LLM
                                         generates possible proof steps (tactics) for a given goal that can be applied to it. The ITP checks the
                                         applicability of the generated tactic and creates new edges with the applicable tactics in the proof search
                                         tree, discarding the failed tactics. For our task, we used the Lean interactive theorem prover and ByT5
                                         [30] as the tactic generator model. ITPs have already been helping mathematicians with their work, and
                                         AI-based proof generation can further help them and accelerate research in mathematics.



                                                                                                1
    Although transformer-based language models [23] are very good at learning the pattern of tactic-
goal pairs, we currently have limited formalized proofs in ITP libraries that can be used as a dataset
for training the language model. To overcome the issue of limited data for training the model, various
new approaches have been explored to improve the performance of automated theorem provers, such as
reinforcement learning [19, 27], expert iteration [18], online training [10] and retrieval augmentation [33].
Although these methods improve the performance of the prover to some extent, one of the issues with
these provers is that they require another model along with a tactic generator model to guide/help the
proof search. This makes them computationally expensive to both train and use.
    As an ML model learns to predict tactics based on the tactic-goal pairs it was trained on, we augment
the training dataset by decomposing tactics such as rw (rewrite) and simp (simplify) with multiple
premises into tactics with single premises. We believe this will provide the model with more examples
to learn from and help it predict tactics for diverse goals more accurately. Furthermore, we propose
DS-Prover, a new dynamic sampling method for theorem proving. This method dynamically determines
the number of tactics to apply to expand the current goal, taking into account the remaining time relative
to the total allocated time for proving a theorem. This makes the proof search process more efficient
by adjusting the balance between exploration and exploitation over time. Additionally, we optimized
the LeanDojo [33], which is a tool we used to interact with Lean programmatically. Furthermore, we
introduce a publicly accessible theorem prover website, allowing users to submit the formal statement of
their mathematical theorem in Lean. The prover will then attempt to prove it within a specified time
limit.
    We conducted our experiments using the Lean formal environment and its formalized theorems in
the Mathlib repository as the training dataset. We evaluated our methods on two standard datasets,
MiniF2F and ProofNet, and achieved significant performance gains on both. We achieved a state-of-the-
art performance (Pass@1) of 14.2% on the ProofNet dataset and a performance of 29.8% on MiniF2F,
slightly surpassing the best-reported Pass@1 of 29.6% [18] using Lean. Furthermore, we obtained a
cumulative (across various proving methods used) Pass@1 of 31.4% on the MiniF2F, 15.7% on ProofNet,
and 63.4% on the Mathlib test dataset.


2    Related Works
With the increasing number of formalized theorems in the libraries of interactive theorem provers (ITPs),
various recent attempts have been made to automate theorem proving using machine learning. Before
the advent of the Large Language Model (LLM), the architecture of machine learning agents used for
interacting with the ITPs was based on graph neural networks, as evidenced by studies such as [32,
16], which could explicitly encode the syntax of formal expressions. Additionally, deep learning-based
approaches [7, 26, 1] were employed for this purpose.
    After the success of the attention-based [23] LLM, in [19] authors utilized a GPT-2 [20] model for
tactic generation for a given state, employing a best-first search method to guide the proof using the
log-probability of tactics. Additionally, they incorporated a state-level value function to further enhance
the guidance of the proof search process. Building upon this, PACT [5] made strides by leveraging
both tactic and term-based proofs from Lean’s library Mathlib, utilizing a multi-task training scheme to
train their model. Conversely, in [25], the authors addressed the data scarcity issue by implementing a
method where they learned to prove theorems through the process of generating them. Meanwhile, in the
work [29], synthetic datasets were generated for deduction, induction, and abduction tasks, recognized as
fundamental reasoning primitives [17]. The model was trained on this data to equip it with proficiency in
these three reasoning abilities. Additionally, in TacticZero [27], deep reinforcement learning techniques
were employed, enabling the learning of theorem proving from scratch.
    To enhance the performance of neural theorem provers on datasets that potentially possess distribu-
tions different from the training data, the authors in [18] employed an expert iteration-based method.
This approach intertwines proof search with learning from previous attempts, aiming to improve future
performance. Similarly, HyperTree Proof Search [10] employed a comparable strategy, learning from
previous proof searches through online training. This method facilitates the model’s ability to generalize


                                                     2
to domains significantly distant from the training distribution.
    Given that most of these works rely on a step-level value function to steer the proof search pro-
cess, DT-Solver [24] presents an alternative approach. The authors utilize a dynamic-tree-driven proof
search procedure that integrates state confidence and proof-level values, mirroring human reasoning by
considering the entire proof trajectory. One of the difficulties of the proof step generating agent is to
find the correct premises to be used in a given proof step. To address this issue, some studies [21] have
been conducted, and LeanDojo [33] and [28] have implemented a retrieval-augmented language model
and Magnushammer [13] have used a transformer-based approach to suggest the premises to be used in
tactics. Similar approaches for automating theorem proving have also been applied to other interactive
theorem provers like Isabelle [11, 8, 4, 9].
    Although most of the methods discussed above improve performance, one issue is that most of these
methods use multiple models and multiple training objectives, leading to processes that require higher
computing power (in some cases, up to 1000 GPU hours) for both training and proving. To overcome the
issue of high computation demand, we instead explore the possibility of improving the performance with
a tactic generator model only. To do this, we improved the prover algorithm by introducing DS-Prover,
a Dynamic Sampling method, and explored the option of making the tactic generator model better at
premise-based tactic prediction by giving it more pairs of goals and tactics with premises. This helps the
model to learn the names of the premises and the goals where to use them.


3     Formal Environment
For our experiment, we chose Lean [14] as the formal environment. Lean is an interactive proof assistant
that is designed to assist mathematicians, computer scientists, and engineers in formalizing and proving
the correctness of mathematical theorems and complex software systems. Lean uses a powerful dependent
type system, which allows types to depend on values and expressions. This feature makes it possible
to express precise and intricate mathematical concepts, making it suitable for formalizing advanced
mathematical theories.
   Lean’s metaprogramming capabilities, active community, extensive mathematical library, and robust
tactic system make it a compelling choice for our experiment. These features enable us to effectively
write custom automation procedures, access a wealth of formalized mathematical knowledge, and utilize
a powerful interactive theorem proving environment. Additionally, Lean’s active and growing user com-
munity provides support for newcomers and contributes to its ongoing development, ensuring that we
can utilize the latest advancements and benefit from the collective expertise of the Lean community.
   At the time of conducting our experiments, Lean 4 was the most recent version available. However,
due to its lack of backward compatibility and the ongoing process of migrating the mathematical library
Mathlib from Lean 3 to Lean 4 (Mathlib4), as well as the fact that standard test datasets like MiniF2F
and ProofNet are currently available only in Lean 3, we chose to utilize Lean 3 for our experiments. It’s
worth noting that our experimental procedures can readily be replicated within the Lean 4 environment.

3.1     Proving in Lean
Proving in Lean involves constructing formal proofs to demonstrate the correctness of mathematical
statements. Here’s an example:
    1. Environment Setup: In this step, we set up the mathematical environment in Lean. This involves
       declaring variables and stating assumptions if necessary.
      variables x y z w : nat

      Here, we declare four natural number variables: x, y, z, and w which will be used in the proof.

    2. Formulate the Goal: Define the theorem or proposition to be proved.
      theorem thm1 (h1 : x = y) (h2 : y = z) (h3 : z = w) : x = w :=



                                                    3
        This line defines a theorem statement named thm1. We state our goal, which is to prove that x =
        w. Additionally, we introduce assumptions or hypotheses (h1 : x = y), (h2 : y = z), and
        (h3 : z = w).

  3. Constructing the proof: involves a systematic progression through a series of steps, applying
     various tactics to achieve the goal. The theorem statement serves as the initial goal, and the
     application of valid tactics generates one or more subgoals. The proof is ultimately obtained by
     continually applying new tactics to these subgoals until no further goals remain. In the example
     presented here, we employ two tactics, namely the rw (rewrite) and assumption tactics, to establish
     a chain of equalities that underpin the proof.
            begin
              rw [h1, h2],
              assumption
            end

          • begin: This keyword marks the beginning of the proof. It’s followed by a sequence of tactics
            that will be applied in order to achieve the goal.
          • rw [h1, h2]: We use the rw (rewrite) tactic to simplify the goal by applying rewriting rules
            based on the assumptions h1 and h2. This step simplifies the goal by substituting x with y
            and y with z.
          • assumption: The assumption tactic looks through the assumptions in context of the current
            goal, and if there is one matching the conclusion, it applies it. In this case, it concludes the
            proof by using the third assumption h3 to establish that z is indeed equal to w.
          • end: This keyword marks the end of the proof.

3.2      Dataset
For our experiment, we used Lean’s mathematical library Mathlib 1 with commit 2 (Date: July 26, 2023)
as our dataset which has a total of 98,508 theorems. We created the train, validation, and test datasets
randomly with 96,508, 1,000, and 1,000 theorems respectively. To train the tactic generator model we
used LeanDojo [33] to generate the goal tactic pair for each step in theorems’ proof.

3.2.1     Original data
For the training dataset, we had a total of 212,840 goal tactic pairs. Below we demonstrate the goal
tactic pairs for the proof of theorem ’thm1’ discussed above.
[{"goal": "x y z w: nat
          h1: x = y
          h2: y = z
          h3: z = w
          |- x = w",
  "tactic": "rw [h1, h2]"},
 {"goal": "x y z w: nat
          h1: x = y
          h2: y = z
          h3: z = w
          |- z = w",
  "tactic": "assumptions"}]
  1 https://github.com/leanprover-community/mathlib
  2 d11f435d4e34a6cea0a1797d6b625b0c170be845




                                                      4
3.3      Data Augmentation
To further increase the number of tactic-goal pairs, we decomposed tactics with multiple premises, such
as rw [p1 , ..., pn ] and simp [p1 , ..., pn ], into tactics with single premises. This means we transformed
them into sequences like rw [p1 ]; ...; rw [pn ] and simp [p1 ]; ...; simp [pn ]3 . This adjustment
allowed us to generate a greater variety of examples illustrating the usage of each individual premise.
This approach aids the model in learning the appropriate pairings of premises with specific goals and
helps it remember the names of these premises. Table 3 in the Appendix A.1 summarizes all of these
modifications.
[{"goal": x y z w: nat
          h1: x = y
          h2: y = z
          h3: z = w
          |- x = w
  "tactic": "rw [h1]"},
 {"goal": x y z w: nat
          h1: x = y
          h2: y = z
          h3: z = w
          |- y = w
  "tactic": "rw [h2]"},
 {"goal": x y z w: nat
          h1: x = y
          h2: y = z
          h3: z = w
          |- z = w
  "tactic": "assumptions"}]
   Data Collection: As the list of premises in the rewrite (rw, erw, rwa, equiv rw, assoc rw)
tactics are ordered, so to collect this data we modified all the occurrences of the rewrite tactics in
Mathlib according to Table 3 and then used LeanDojo to extract data from the modified repository.
In this way we were able to generate 41,036 new tactic goal pairs. Since the list of premises in the
simplification (simp, dsimp, simpa, simp rw) tactics is not ordered i.e. the premises can be used in
any order to simplify the goal. So, to collect the goals corresponding to each new simplification tactics
we used LeanDojo to apply all the new tactics one by one at the goal of the step where the original
simplification tactic was supposed to be applied and record the tactic goal pair whichever succeeds and
keep on repeating this task on the subgoals generated by the application of first successful tactic and we
don’t keep the successful tactics in the future list. In this way, we were able to generate 102,682 new
unique tactic goal pairs for simplification tactics.


4      Model
4.1      Model Architecture
We use ByT5-Small as our tactic generator model which has 300m trainable parameters with 12 encoder
and 4 decoder layers. ByT5 [30] is a tokenizer-free version of Google’s T5 [31] language model. It operates
directly on raw UTF-8 bytes, removing the need for any text preprocessing.

4.2      Training Objective
The training objective over here is to generate a tactic for the given goal. For example in the theorem
’thm1’ discussed in section 3 the input and output for the initial state would be as follows:
    3 Order of the generated tactics may vary in the case of simplification tactics.




                                                               5
         Input: ’’’x y z w: nat                  Output: "rw [h1]"
         (goal)    h1: x = y                     (tactic)
                   h2: y = z
                   h3: z = w
                   |- x = w’’’
   For early stopping, we use the validation data set. After each specified number of training steps,
we attempt to prove the theorems in the validation dataset using the model being trained as the tactic
predictor and we stop training at the point where we have the highest Pass@1 value on the validation
dataset.

4.3     Proof Search
To prove a theorem we use LeanDojo which enables programmatic interaction with Lean. To find the
proof of a given theorem we run a proof search. This process begins by selecting the theorem we wish
to prove and obtaining its initial goal from Lean. Then, we use the tactic generator model to generate
possible tactics that can be applied to the goal. We maintain a proof search tree along with a queue of
open goals, sorted by their cumulative log probability as demonstrated in Figure 1. At each step, we
expand the goal with the highest cumulative log probability, i.e., the goal for which the tactic generator
model is most confident. This method of proof search is called the best-first search.

4.3.1   Goal Expansion
Goal expansion is the process of application of tactics to an open goal to generate new subgoals. Unlike
the fixed number of samples employed in prior approaches such as [19] and [33], we adopt a dynamic
sampling approach. In this method, the number of samples is determined dynamically, taking into account
the remaining time compared to the total allocated time for theorem proving.
                                                                 time passed
                            n = a + b · e−c·r       Where, r =                                           (1)
                                                                  total time
    Equation 1 defines the tactic sampling decay function, where a, b, and c are constants. The constant
a determines the minimum number of tactics to sample when the proof search is near the end of the
assigned time limit. The constant b determines the initial number of tactics to sample, and the constant
c determines the rate of decay in the number of samples. For our experiment we used a = 6, b = 12 and
c = 5. The variable time passed is the amount of time passed since the start of the proof search, and the
variable total time is the total amount of time that the proof search is allowed to use (10 minutes in all
the cases). The variable n gives the number of tactics to apply to the given goal. Since it is possible that
not all of the sampled tactics from the model will be successfully applied to the given goal, we sample
5n tactics from the model instead of just n. We then apply at most n successful tactics to the goal.
Whereas, in experiments utilizing the fixed sampling method, we sample n = 64 tactics at each step and
apply all the successful tactics.

4.3.2   Motivation for Dynamic Sampling
The proof search algorithm often encounters situations where the queue, containing the nodes to explore,
becomes empty. This occurs when the number of new nodes being added to the queue is fewer than
the nodes being explored and removed, leading to an early stoppage without any proof. To prevent
such cases, we decided to start with a larger number of tactics to sample. This approach enables us to
add a greater number of nodes to the queue initially, thereby maintaining an adequate number of nodes
throughout the proof search.
    As time passes, we slowly reduce the number of tactics to sample, which aids in curbing the exponential
increase in the number of nodes (at higher depth) as the tree depth grows. Consequently, this method
can delve deeper into the tree, making it an efficient approach to discovering proofs with a larger number
of steps.


                                                     6
             Proof Search Tree
           for Dynamic Sampling                                                t=0
                                                                    root      n = 18




                   tactic 1                                       tactic 5                                        tactic 18
                 logprob = -0.6                              logprob = -1.3                                   logprob = -3.2




                                                                    goal      t = 1.5
                                                                     i        n = 11




                        tactic 1                         tactic 3                                         tactic 11
                     logprob = -0.4                  logprob = -1.1                                   logprob = -3.8



                                          Expansion of
                                             goal j        goal         t = 4.0
                                                            j            n=7




                                      tactic 1           tactic 2                          tactic 7
                                   logprob = -0.5    logprob = -1.0                      logprob = -3.1




                                                                                  goal                    goal
            Cumulative Logprob                      root
                                                                                   i                       j
                 Queue
                                                     0                            -1.3                     -2.4



Figure 1: Navigating the Proof Search Tree with Dynamic Sampling: Deciding the number of tactics (n)
to sample as time (t) progresses in the proof search, guided by Equation 1.


   Another motivation for using a dynamic sampling method is based on exploration and exploitation.
Using a dynamic number of tactics in proof search allows us to adjust the balance between exploration
and exploitation. At the beginning of the proof search, we start with a higher value of n, which means
that we are more likely to explore even less promising tactics. As time passes, we reduce n to focus on
only the most promising tactics, for which the model has high confidence.


5     Experiments
5.1    Training
In our experiments, we used the ByT5-Small model as our tactic generator model, as discussed in Section
4.1. We trained the model using UTF-8 encoding, a batch size of 8, a learning rate of 5e-4, a dropout
probability of 0.5, and the AdamW optimizer.
    We trained two models, one on the original dataset and the other on an augmented dataset. The
original dataset was a collection of tactic-goal pairs extracted from the Mathlib repository without any


                                                                    7
modification.
  For the augmented dataset, we combined the tactic-goal pairs from three datasets:
  1. Tactic-goal pairs extracted from the rewrite modified Mathlib repository.
  2. New tactic-goal pairs generated for simplification tactics.
  3. Tactic-goal pairs generated from the original Mathlib repository.
We kept the tactic-goal pairs from the original Mathlib repository in the training dataset for the aug-
mented model so that the model could see the original longer tactics (with multiple premises) and learn
to use them along with the new smaller tactics (with single premises).

5.1.1   Experimental Setup
We performed all of our experiments on a system with four NVIDIA A100 GPUs, each with 80 GB of
VRAM, and 96 CPU cores with 1TB RAM. On this system, collecting tactic-goal pairs from the original
and rewrite modified Mathlib repository took around two hours each. Generating tactic-goal pairs for
simplification tactics took around one day. Training the tactic generator model on both the original and
augmented datasets on the four GPUs took around one day each, and evaluation took around one week.

    LeanDojo Optimization: LeanDojo is designed for both Lean 3 and Lean 4, but to check which
version is being used, it used to query the GitHub API, which slowed down the prover. To make it faster,
we hardcoded it to always return Lean 3, since we performed all of our experiments in Lean 3. We also
increased the tactic application timeout from the default of 5 seconds to 10 seconds for our experiments.

5.2     Test Datasets
We assess the performance of our methods across a diverse set of test datasets that are designed for
testing purposes only and do not contain any theorems that were used in training. This makes them
challenging datasets to evaluate on.
    MiniF2F Dataset4 : The MiniF2F dataset, serves as a comprehensive cross-system benchmark for
formal theorem proving within the realm of mathematics. Comprising a total of 489 problem statements,
of which 245 constitute the test set and 244 serve as the validation set, this dataset draws its content
from esteemed sources such as the American Mathematics Competition (AMC), American Invitational
Mathematics Examination (AIME), International Mathematical Olympiad (IMO), as well as materials
from high-school and undergraduate mathematics courses.
    ProofNet Dataset5 : ProofNet is a benchmark dataset for formally proving theorems in under-
graduate level mathematics. It consists of 374 examples, each of which is a formal theorem statement
in the Lean 3 theorem prover. The problems are drawn from popular undergraduate pure mathemat-
ics textbooks and cover topics such as real and complex analysis, linear algebra, abstract algebra, and
topology.
    Mathlib Dataset: We also tested our methods on the Mathlib test dataset, which is a dataset we
created by random selection of theorems from the Mathlib repository, as elaborated in Section 3.2. It is
essential to mention that, due to constraints in our computing resources, we limited our evaluation to a
subset of this dataset, comprising 500 theorems, from the original set of 1000 test theorems.

5.3     Results
Table 1 summarizes the performance evaluation (Pass@1) of both models on all of our test datasets using
different proving methods. The Venn diagram in Figure 2 illustrates the subsets of theorems proved from
all the test theorems in Mathlib, Minif2f, and Proofnet using our different proving methods. In Tables
1 and 2, we also report the cumulative Pass@1 performance, which is the percentage of the union of
theorems proved by all of our proving methods.
  4 https://github.com/openai/miniF2F/tree/main/lean
  5 https://github.com/zhangir-azerbayev/ProofNet




                                                       8
Table 1: Performance evaluation (Pass@1) of different approaches on test datasets within a 10-minute
time constraint across all cases.

                                  MiniF2F                        ProofNet                      Mathlib
                           Original Augmented              Original Augmented           Original Augmented
         Method
                            data       data                 data       data              data       data
        LeanDojo            27.8        --                  12.8        --               52.2        --
   Optimized LeanDojo       28.6       29.4                 13.3       14.2              55.0       57.2
      DS-Prover +
                                29.0            29.8        13.7          14.2           55.0          58.8
   Optimized LeanDojo
       Cumulative                        31.4                      15.7                         63.4


   Table 2 compares the performance of our approach to other baselines on the MiniF2F test dataset.
We could not reproduce previous works due to the high computational requirements of most of them,
so we used the performance reported in their papers for our comparison. As depicted in the table, we
have the best performance of 29.8% on MiniF2F, which slightly surpasses the best-reported Pass@1 of
29.6% [18] using Lean; further, we obtained a cumulative (across all the proving methods used) Pass@1
of 31.4% on the MiniF2F dataset.

   Table 2: Comparison with Baseline Performance (Pass@1) on the Testing Data of Lean MiniF2F.

                        S. No.         Method                                Pass@1
                           1           Lean GPT-f [34]                        24.6
                           2           PACT [5]                               24.6
                           3           Lean Expert Iteration [18]             29.6
                           4           ReProver [33]                          26.5
                           5           Augmented data + DS-Prover +           29.8
                                       Optimized LeanDojo (Ours)
                            6          Cumulative (Ours)                         31.4

   On the ProofNet test dataset, we have the best performance (Pass@1) of 14.2% which is higher
than the only reported performance of 13.8% with ReProver [33]. And we got the cumulative Pass@1 of
15.7% on the ProofNet dataset.

5.4    Discussion
Table 1 and the Venn diagram in Figure 2 indicate that on the original dataset, the optimized LeanDojo
has better performance in all cases compared to the default LeanDojo. Furthermore, we can observe from
the Venn diagram that, excluding one theorem proved by the default LeanDojo, all other theorems were
proved by the optimized LeanDojo. Additionally, it is able to prove 20 extra theorems. This shows that
our optimized LeanDojo is more efficient than the default LeanDojo.
    Further, we can observe from Table 1 that using the model trained on augmented data consistently
outperforms the model trained solely on the original data. The augmented model’s training with a
larger number of tactic-goal pairs provides it with the capability to effectively handle diverse goals.
This underscores the augmented dataset’s effectiveness in training the tactic generator model for Neural
Theorem Proving.
    Additionally, from the Venn diagram in Figure 2, we can observe that a total of 440 theorems were
proved using both methods: original data and augmented data with the optimized LeanDojo. Out of these
440 theorems, 361 theorems were proved by both methods, 32 theorems were proved only by the model
trained on the original dataset, and 47 theorems were proved only by the model trained on the augmented
data. The high value of the symmetric difference (32 + 47) between the two sets is attributed to the shift
in the model’s distribution resulting from the inclusion of new tactic-goal pairs in the augmented training


                                                       9
        Optimized LeanDojo                                                      Optimized LeanDojo
            + Original Data                                                     + Augmented Data

                                        4                          6
                                                     0
                                                                                                     LeanDojo +
                               18                                          40                         Original Data
                                                                                                     Optimized LeanDojo
                                                                                                      + Original Data
                                            3                 12                                     Optimized LeanDojo
                                                                                                      + Augmented Data
                           0                                                     7                   Optimized LeanDojo
                                                    346                                               + Augmented Data
                                                                                                     + Dynamic Sampling
                                    0                                  4
                                                1         6
            LeanDojo +
           Original Data                             0                               Optimized LeanDojo
                                                                                     + Augmented Data
                                                                                     + Dynamic Sampling

Figure 2: Venn diagram illustrating subsets of theorems proved from all the test theorems in Mathlib,
Minif2f, and Proofnet using different proving methods.


dataset. This property of shift in models’s distribution can be leveraged in tasks where the utilization of
multiple models is permitted to maximize the number of theorems proved.
    We can also observe from Table 1 that employing dynamic sampling, instead of fixed sampling,
consistently enhances performance in most cases for both the augmented and original datasets. The
dynamic sampling method either outperforms the fixed sampling or performs equally well, but it never
exhibits worse performance. From the Venn diagram in Figure 2, we can observe that for all datasets,
the dynamic sampling method was able to prove 8 more theorems than the fixed sampling method. This
aspect makes the use of the dynamic sampling method a promising new approach for neural theorem
proving.
    Furthermore, to study the effect of using the dynamic sampling method, we ran the prover for various
time limits (2.5, 5, and 10 minutes) using both fixed sampling and dynamic sampling methods on 500
theorems of Mathlib’s test data with model trained on the augmented dataset. We then plotted these
results in Figure 3, and the variation of the number of tactics to be sampled over time has been plotted
in Figure 8 in the Appendix Section. From the plot, we can observe that the dynamic sampling method
outperforms the fixed sampling method for all time limits. This demonstrates the effectiveness of the
dynamic sampling method in calculating the optimal number of tactics to sample as time passes during
theorem proving, taking into account both the total time and the time passed.
    Our website functions as a convenient online platform allowing users to input their Lean problem
statement, after which the prover makes an attempt to provide a proof within the allocated time frame.
Figure 4 displays a screenshot of our website successfully proving a theorem. For a detailed exploration
of how our website facilitates theorem proving, please consult Section A.4 in the Appendix.


6    Conclusion
We have introduced DS-Prover, a dynamic sampling method for Neural Theorem Proving. This method
dynamically determines the number of tactics to apply to expand the current goal, taking into account
the remaining time compared to the total allocated time for proving a theorem. We also studied the
effect of augmenting the training dataset by decomposing tactics with multiple premises into tactics
with single premises. Our experiments show that using the model trained on the augmented dataset
has better performance than using the model trained only on the original dataset. Additionally, we


                                                              10
                                              280   Dynamic Sampling
                                                    Fixed Sampling
                                              270


                     No. of Theorems Proved
                                              260
                                              250
                                              240
                                              230
                                              220
                                                    2.5             5          10
                                                              Time (minutes)
Figure 3: Comparison of Theorems Proved Using Fixed and Dynamic Sampling Methods on 500 Theorems
of Mathlib’s Test Data with Model Trained on Augmented Dataset.


optimized LeanDojo, a tool that we used to interact with Lean programmatically. This establishes our
neural theorem proving methods as a new and promising approach. Further, we release a public website
for theorem proving in Lean 3.


References
 [1] Bansal, K., Loos, S., Rabe, M., Szegedy, C., Wilcox, S.: Holist: An environment for machine
     learning of higher order logic theorem proving. In: International Conference on Machine Learning.
     pp. 454–463. PMLR (2019)
 [2] Barras, B., Boutin, S., Cornes, C., Courant, J., Filliatre, J.C., Gimenez, E., Herbelin, H., Huet, G.,
     Munoz, C., Murthy, C., et al.: The Coq proof assistant reference manual: Version 6.1. Ph.D. thesis,
     Inria (1997)
 [3] De Millo, R.A., Lipton, R.J., Perlis, A.J.: Social processes and proofs of theorems and programs.
     Communications of the ACM 22(5), 271–280 (1979)
 [4] First, E., Rabe, M.N., Ringer, T., Brun, Y.: Baldur: whole-proof generation and repair with large
     language models. arXiv preprint arXiv:2303.04910 (2023)

 [5] Han, J.M., Rute, J., Wu, Y., Ayers, E.W., Polu, S.: Proof artifact co-training for theorem proving
     with language models. arXiv preprint arXiv:2102.06203 (2021)
 [6] Harrison, J.: Hol light: A tutorial introduction. In: International Conference on Formal Methods in
     Computer-Aided Design. pp. 265–269. Springer (1996)

 [7] Irving, G., Szegedy, C., Alemi, A.A., Eén, N., Chollet, F., Urban, J.: Deepmath-deep sequence
     models for premise selection. Advances in neural information processing systems 29 (2016)
 [8] Jiang, A.Q., Li, W., Han, J.M., Wu, Y.: Lisa: Language models of isabelle proofs. In: 6th Conference
     on Artificial Intelligence and Theorem Proving. pp. 378–392 (2021)




                                                                11
Figure 4: Illustration of the Website Successfully Proving a Theorem.




                                 12
 [9] Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygóźdź, T., Miloś, P., Wu, Y., Jamnik, M.:
     Thor: Wielding hammers to integrate language models and automated theorem provers. Advances
     in Neural Information Processing Systems 35, 8360–8373 (2022)
[10] Lample, G., Lacroix, T., Lachaux, M.A., Rodriguez, A., Hayat, A., Lavril, T., Ebner, G., Martinet,
     X.: Hypertree proof search for neural theorem proving. Advances in Neural Information Processing
     Systems 35, 26337–26349 (2022)
[11] Li, W., Yu, L., Wu, Y., Paulson, L.C.: Isarstep: a benchmark for high-level mathematical reasoning.
     arXiv preprint arXiv:2006.09265 (2020)
[12] Megill, N., Wheeler, D.A.: Metamath: a computer language for mathematical proofs. Lulu. com
     (2019)
[13] Mikula, M., Antoniak, S., Tworkowski, S., Jiang, A.Q., Zhou, J.P., Szegedy, C., Kuciński, L., Miloś,
     P., Wu, Y.: Magnushammer: A transformer-based approach to premise selection. arXiv preprint
     arXiv:2303.04488 (2023)
[14] de Moura, L., Kong, S., Avigad, J., Van Doorn, F., von Raumer, J.: The lean theorem prover (system
     description). In: Automated Deduction-CADE-25: 25th International Conference on Automated
     Deduction, Berlin, Germany, August 1-7, 2015, Proceedings 25. pp. 378–388. Springer (2015)
[15] Nipkow, T., Wenzel, M., Paulson, L.C.: Isabelle/HOL: a proof assistant for higher-order logic.
     Springer (2002)
[16] Paliwal, A., Loos, S., Rabe, M., Bansal, K., Szegedy, C.: Graph representations for higher-order logic
     and theorem proving. In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 34, pp.
     2967–2974 (2020)
[17] Peirce, C.S.: Reasoning and the logic of things: The Cambridge conferences lectures of 1898. Harvard
     University Press (1992)
[18] Polu, S., Han, J.M., Zheng, K., Baksys, M., Babuschkin, I., Sutskever, I.: Formal mathematics
     statement curriculum learning. arXiv preprint arXiv:2202.01344 (2022)
[19] Polu, S., Sutskever, I.: Generative language modeling for automated theorem proving. arXiv preprint
     arXiv:2009.03393 (2020)
[20] Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al.: Language models are
     unsupervised multitask learners. OpenAI blog 1(8), 9 (2019)
[21] Szegedy, C., Rabe, M., Michalewski, H.: Retrieval-augmented proof step synthesis (2021)
[22] Thurston, W.P.: On proof and progress in mathematics. Bulletin of the American mathematical
     Society 30(2), 161–177 (1994)
[23] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, L., Polosukhin,
     I.: Attention is all you need. Advances in neural information processing systems 30 (2017)
[24] Wang, H., Yuan, Y., Liu, Z., Shen, J., Yin, Y., Xiong, J., Xie, E., Shi, H., Li, Y., Li, L., et al.: Dt-
     solver: Automated theorem proving with dynamic-tree sampling guided by proof-level value function.
     In: Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume
     1: Long Papers). pp. 12632–12646 (2023)
[25] Wang, M., Deng, J.: Learning to prove theorems by learning to generate theorems. Advances in
     Neural Information Processing Systems 33, 18146–18157 (2020)
[26] Whalen, D.: Holophrasm: a neural automated theorem prover for higher-order logic. arXiv preprint
     arXiv:1608.02644 (2016)


                                                     13
[27] Wu, M., Norrish, M., Walder, C., Dezfouli, A.: Tacticzero: Learning to prove theorems from scratch
     with deep reinforcement learning. Advances in Neural Information Processing Systems 34, 9330–9342
     (2021)

[28] Wu, Y.: Formal premise selection with language models. In: Conference on Artificial Intelligence
     and Theorem Proving (AITP). vol. 4 (2022)
[29] Wu, Y., Rabe, M.N., Li, W., Ba, J., Grosse, R.B., Szegedy, C.: Lime: Learning inductive bias
     for primitives of mathematical reasoning. In: International Conference on Machine Learning. pp.
     11251–11262. PMLR (2021)

[30] Xue, L., Barua, A., Constant, N., Al-Rfou, R., Narang, S., Kale, M., Roberts, A., Raffel, C.: Byt5:
     Towards a token-free future with pre-trained byte-to-byte models. Transactions of the Association
     for Computational Linguistics 10, 291–306 (2022)
[31] Xue, L., Constant, N., Roberts, A., Kale, M., Al-Rfou, R., Siddhant, A., Barua, A., Raffel, C.:
     mt5: A massively multilingual pre-trained text-to-text transformer. arXiv preprint arXiv:2010.11934
     (2020)
[32] Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assistants. In: Interna-
     tional Conference on Machine Learning. pp. 6984–6994. PMLR (2019)
[33] Yang, K., Swope, A.M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger, R., Anand-
     kumar, A.: Leandojo: Theorem proving with retrieval-augmented language models. arXiv preprint
     arXiv:2306.15626 (2023)
[34] Zheng, K., Han, J.M., Polu, S.: Minif2f: a cross-system benchmark for formal olympiad-level math-
     ematics. arXiv preprint arXiv:2109.00110 (2021)




                                                  14
A      Appendix
A.1     Data Augmentation
Table 3 lists all the new tactics generated through our data augmentation method. It is worth noting that
the list of premises in the rewrite (rw, erw, rwa, equiv rw, assoc rw) tactics is ordered. To collect
this data, we modified all occurrences of the rewrite tactics in Mathlib according to Table 3, and then
used LeanDojo to extract data from the modified repository.

    Table 3: Description of new tactic generation (replaced simplification tactics’ order may vary).

      Original tactic                     Replaced tactics
      rw [p1 , ..., pn ]                  rw [p1 ]; ...; rw [pn ]
      rw [p1 , ..., pn ] at h1            rw [p1 ] at h1 ; ...; rw [pn ] at h1
      erw [p1 , ..., pn ]                 erw [p1 ]; ...; erw [pn ]
      erw [p1 , ..., pn ] at h1           erw [p1 ] at h1 ; ...; erw [pn ] at h1
      rwa [p1 , ..., pn ]                 rwa [p1 ]; ...; rwa [pn ]
      rwa [p1 , ..., pn ] at h1           rwa [p1 ] at h1 ; ...; rwa [pn ] at h1
      equiv rw [p1 , p2 ]                 equiv rw [p1 ]; ...; equiv rw [p2 ]
      equiv rw [p1 , ..., pn ] at h1      equiv rw [p1 ] at h1 ; ...; equiv rw [pn ] at h1
      assoc rw [p1 , ..., pn ]            assoc rw [p1 ]; ...; assoc rw [pn ]
      assoc rw [p1 , ..., pn ] at h1      assoc rw [p1 ] at h1 ; ...; assoc rw [pn ] at h1
      simp rw [p1 , ..., pn ]             simp rw [p1 ]; ...; simp rw [pn ]
      simp rw [p1 , ..., pn ] at h1       simp rw [p1 ] at h1 ; ...; simp rw [pn ] at h1
      simp [p1 , ..., pn ]                simp [p1 ]; ...; simp [pn ]
      simp [p1 , ..., pn ] at h1          simp [p1 ] at h1 ; ...; simp [pn ] at h1
      simp only [p1 , ..., pn ]           simp only [p1 ]; ...; simp only [pn ]
      simp only [p1 , ..., pn ] at h1     simp only [p1 ] at h1 ; ...
      dsimp [p1 , ..., pn ]               dsimp [p1 ]; ...; dsimp [pn ]
      dsimp [p1 , ..., pn ] at h1         dsimp [p1 ] at h1 ; ...; dsimp [pn ] at h1
      dsimp only [p1 , ..., pn ]          dsimp only [p1 ]; ...; dsimp only [pn ]
      dsimp only [p1 , ..., pn ] at h1    dsimp only [p1 ] at h1 ; ...
      simpa [p1 , ..., pn ]               simpa [p1 ]; ...; simpa [pn ]
      simpa [p1 , ..., pn ] at h1         simpa [p1 ] at h1 ; ...; simpa [pn ] at h1
      simpa only [p1 , ..., pn ]          simpa only [p1 ]; ...; simpa only [pn ]
      simpa only [p1 , ..., pn ] at h1    simpa only [p1 ] at h1 ; ...

    However, the list of premises in the simplification (simp, dsimp, simpa, simp rw) tactics is not
ordered, meaning the premises can be used in any order to simplify the goal. Therefore, for simplification
tactics, the order shown in the Table 3 is not fixed; the new tactics generated can be applied in any order.
To determine the exact order, we applied them one by one using LeanDojo and recorded the successful
tactic-goal pairs.
    Furthermore, it is important to note that tactics like simpa require all of the premises together to
be applied on a goal. Thus, we also broke them into tactics with single premises but checked their
applicability on the current goals and recorded only the successful tactic-goal pairs. Hence tactics like
simpa do not cause any issues in our data augmentation process.
    To analyse the different set of theorems proved by different methods we plot Venn diagram in Figure
5, 6, and 7 for the test datasets of Mathlib, MiniF2F, and ProofNet respectively.

A.2     Dynamic Sampling
To study the impact of employing dynamic sampling and to ascertain its enhancements in performance,
we conducted an analysis of the theorems’ proofs and the search trees generated for all the theorems


                                                    15
                   Optimized LeanDojo                                                                      Optimized LeanDojo
                       + Original Data                                                                     + Augmented Data

                                                        3                           5
                                                                     0
                                                                                                                                LeanDojo +
                                               14                                                     30                         Original Data
                                                                                                                                Optimized LeanDojo
                                                                                                                                 + Original Data
                                                            2                  9                                                Optimized LeanDojo
                                                                                                                                 + Augmented Data
                                           0                                                                6                   Optimized LeanDojo
                                                                    240                                                          + Augmented Data
                                                                                                                                + Dynamic Sampling
                                                    0                                   3
                                                                0         5
                            LeanDojo +
                           Original Data                             0                                          Optimized LeanDojo
                                                                                                                + Augmented Data
                                                                                                                + Dynamic Sampling

Figure 5: Venn diagram illustrating subsets of theorems proved from the test theorems in Mathlib
dataset using different proving methods.


within our mathlib test dataset. Specifically, we aimed to comprehend the disparity between the tree
structures produced by both dynamic and fixed sampling methods for proof searching. A comparative
plot (Figure 9) depicting the average number of nodes at each level (tree depth) for both methods was
generated for this purpose. Upon examining the plot, noticeable differences emerged: the fixed sampling
method exhibited a rapid increase in the number of nodes initially, reaching its peak at a depth of 3.
In contrast, the dynamic sampling method showcased a slower increase, reaching its peak at depth 4.
Overall, the plot suggests that the fixed sampling method tends to prioritize shorter proofs, whereas
the dynamic sampling method displays a more extensive distribution. It actively explores varied proof
lengths, aiding in the discovery of even longer proofs.
                 300                                        Dynamic sampling                          27
                                                            Fixed sampling
                 250                                                                                  26
                                                                                                      25
                                                                                    No. of theorems




                 200
  No. of nodes




                                                                                                      24
                 150
                                                                                                      23
                 100
                                                                                                      22
                  50                                                                                          Dynamic sampling
                                                                                                      21      Fixed sampling
                   0                                                                                  20      Original proof
                       0           2           4        6            8         10                           1     2       3        4          5      6
                                               Tree depth                                                                 Proof size
   Figure 9: Number of nodes in the search tree at Figure 10: Comparison of proof sizes for theorems
   various depths                                         proven using dynamic and fixed sampling meth-
                                                          ods
   For the theorems successfully proven within the allocated time frame, we generated plot 10, which
compares proof sizes between those achieved using dynamic sampling and fixed sampling, juxtaposed with
the original proof sizes for reference. Our analysis revealed that both methods demonstrated comparable


                                                                               16
        Optimized LeanDojo                                                   Optimized LeanDojo
            + Original Data                                                  + Augmented Data

                                       1                         1
                                                   0
                                                                                                  LeanDojo +
                               2                                         5                         Original Data
                                                                                                  Optimized LeanDojo
                                                                                                   + Original Data
                                           0                1                                     Optimized LeanDojo
                                                                                                   + Augmented Data
                           0                                                  0                   Optimized LeanDojo
                                                   64                                              + Augmented Data
                                                                                                  + Dynamic Sampling
                                   0                                 1
                                               1        1
            LeanDojo +
           Original Data                           0                              Optimized LeanDojo
                                                                                  + Augmented Data
                                                                                  + Dynamic Sampling

Figure 6: Venn diagram illustrating subsets of theorems proved from the test theorems in MiniF2F
dataset using different proving methods.


performance for smaller-sized proofs (consisting of 1 or 2 steps). However, the ratio of the number of
theorems proved using dynamic and fixed sampling methods increases as the proof size increases. This
observation indicates that the dynamic sampling method optimizes time utilization by delving into deeper
levels of the proof search tree. Consequently, it efficiently explores and discovers longer proofs, a capa-
bility not as effectively realized by the fixed sampling method.


A.3     Some Examples
Here we present some of the theorems in the ProofNet dataset which currently do not have a proof in the
published GitHub repo, and they have been proven by our augmented data and dynamic sampling method.
Theorems exercise 2 25 and exercise 1 17 are from the Rudin book, theorem exercise 3 1 22b is
from the Dummit-Foote book, and exercise 5 1 8 is from the Herstein book.



theorem exercise_2_25 {K : Type*} [metric_space K] [compact_space K] :
  ∃ (B : set (set K)), set.countable B ∧ is_topological_basis B :=
begin
  rcases topological_space.exists_countable_basis K with ⟨s, hsc, hsd⟩,
  exact ⟨s, hsc, hsd.2⟩
end

theorem exercise_1_17
  (n : N)
  (x y : euclidean_space R (fin n)) -- R^n
  : ∥x + y∥^2 + ∥x - y∥^2 = 2*∥x∥^2 + 2*∥y∥^2 :=
begin
  rw @norm_add_sq R,
  rw @norm_sub_sq R,
  ring
end


                                                            17
        Optimized LeanDojo                                                   Optimized LeanDojo
            + Original Data                                                  + Augmented Data

                                       0                         0
                                                   0
                                                                                                  LeanDojo +
                               2                                         5                         Original Data
                                                                                                  Optimized LeanDojo
                                                                                                   + Original Data
                                           1                2                                     Optimized LeanDojo
                                                                                                   + Augmented Data
                           0                                                  1                   Optimized LeanDojo
                                                   42                                              + Augmented Data
                                                                                                  + Dynamic Sampling
                                   0                                 0
                                               0        0
            LeanDojo +
           Original Data                           0                              Optimized LeanDojo
                                                                                  + Augmented Data
                                                                                  + Dynamic Sampling

Figure 7: Venn diagram illustrating subsets of theorems proved from all the test theorems in ProofNet
dataset using different proving methods.


theorem exercise_3_1_22b {G : Type*} [group G] (I : Type*) (H : I → subgroup G) (hH : ∀ i : I,
    subgroup.normal (H i)) : subgroup.normal (⊓ (i : I), H i) :=
begin
  split,
  intros n hn g,
  simp only [subgroup.mem_infi] at hn ⊢,
  intro i,
  apply (hH i).conj_mem,
  exact hn i
end

theorem exercise_5_1_8 {p m n: N} {F : Type*} [field F]
  (hp : nat.prime p) (hF : char_p F p) (a b : F) (hm : m = p ^ n) :
  (a + b) ^ m = a^m + b^m :=
begin
  subst hm,
  haveI : fact p.prime := ⟨hp⟩,
  simp only [add_pow_char_pow]
end
   Below, we present some of the theorems in the MiniF2F dataset which have been proven by our
augmented data and dynamic sampling method. Theorems aime 1990 p4 and mathd numbertheory 150
currently do not have a proof in the GitHub repo, and theorem mathd algebra 263 has a proof, but with
our method, we were able to reduce the proof size from 7 in the original proof to 3 proof steps in our
proof.
theorem aime_1990_p4
  (x : R)
  (h0 : 0 < x)
  (h1 : x^2 - 10 * x - 29 ̸= 0)
  (h2 : x^2 - 10 * x - 45 ̸= 0)
  (h3 : x^2 - 10 * x - 69 ̸= 0)
  (h4 : 1 / (x^2 - 10 * x - 29) + 1 / (x^2 - 10 * x - 45) - 2 / (x^2 - 10 * x - 69) = 0) :
  x = 13 :=


                                                            18
                              100
                                                        Fixed Sampling (64 tactics)
                               90                       Dynamic Sampling (10 minutes)
                                                        Dynamic Sampling (5 minutes)
                               80                       Dynamic Sampling (2.5 minutes)
                               70
          Number of tactics



                               60
                               50
                               40
                               30
                               20
                               10
                                    0   2   4             6             8                10
                                             Time (minutes)
Figure 8: Plot showing the number of tactics to be sampled over time using both the fixed sampling and
dynamic sampling methods with varying time limits (2.5, 5, and 10 minutes), as guided by Equation 1.


begin
  field_simp [h0 .ne’] at h4 ,
  rw [sub_eq_zero] at h4 ,
  nlinarith
end

theorem mathd_algebra_263
  (y : R)
  (h0 : 0 ≤ 19 + 3 * y)
  (h1 : real.sqrt (19 + 3 * y) = 7) :
  y = 10 :=
-- Proof generated by our model:
begin
  rw [ real.sqrt_eq_iff_mul_self_eq] at h1 ,
  linarith,
  all_goals {linarith}
end

-- Original proof in the GitHub repo:
begin
  revert y h0 h1 ,
  intros x hx,
  rw real.sqrt_eq_iff_sq_eq hx,
  swap,
  norm_num,
  intro h,
  nlinarith,
end




                                                 19
theorem mathd_numbertheory_150
  (n : N)
  (h0 : ¬ nat.prime (7 + 30 * n)) :
  6 ≤ n :=
begin
  contrapose! h0 ,
  rw nat.prime_def_lt,
  dec_trivial!
end


A.4    Website Description

                        S.No.             Description              Figure
                          1                Home Page              Figure 11
                          2       Theorem Proving in Action       Figure 12
                          3      Successfully Proved a Theorem    Figure 13
                          4         Proof Search Timed Out        Figure 14
                          5               Error Report            Figure 15
                          6      Setting up Local Environment     Figure 16

               Table 4: Table Summarizing the Usage of Website for Theorem Proving.




Figure 11: This is the home page of the theorem prover, featuring a text box where we can input our
formal statement in Lean 3. The website’s backend will then attempt to prove it within the specified
time limit.




                                                20
Figure 12: The website is attempting to prove the given theorem.




 Figure 13: A proof returned by the website when it finds one.




                              21
Figure 14: The prover may not always find a proof for the given statement within the provided time
limit; this is one such example.




Figure 15: If there is any issue with the provided statement, the prover returns an error along with a
description. In this specific example, the identifier ’Rl.is open’ is not defined.



                                                 22
Figure 16: We can set up our local environment of definitions and variables before formulating the
theorem statement.




                                               23
