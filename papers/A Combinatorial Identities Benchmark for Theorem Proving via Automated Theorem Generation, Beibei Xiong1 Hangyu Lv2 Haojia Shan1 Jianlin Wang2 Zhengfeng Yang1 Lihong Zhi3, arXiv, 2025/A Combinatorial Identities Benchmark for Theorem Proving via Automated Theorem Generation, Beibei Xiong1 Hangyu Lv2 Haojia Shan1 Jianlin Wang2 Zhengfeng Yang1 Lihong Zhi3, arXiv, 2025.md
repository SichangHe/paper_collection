                                           A C OMBINATORIAL I DENTITIES B ENCHMARK FOR T HEOREM
                                               P ROVING VIA AUTOMATED T HEOREM G ENERATION


                                               Beibei Xiong1      Hangyu Lv2      Haojia Shan1       Jianlin Wang2      Zhengfeng Yang1    Lihong Zhi3
arXiv:2502.17840v1 [cs.AI] 25 Feb 2025




                                                       1                                  2                      3
                                                           East China Normal University       Henan University       Chinese Academy of Sciences

                                                     {bbxiong,hjshan}@stu.ecnu.edu.cn, hangyvlu@gmail.com, jlwang@henu.edu.cn,
                                                                   zfyang@sei.ecnu.edu.cn, lzhi@mmrc.iss.ac.cn




                                                                                               A BSTRACT
                                                  Large language models (LLMs) have significantly advanced formal theorem proving, yet the scarcity
                                                  of high-quality training data constrains their capabilities in complex mathematical domains. Com-
                                                  binatorics, a cornerstone of mathematics, provides essential tools for analyzing discrete structures
                                                  and solving optimization problems. However, its inherent complexity makes it particularly challeng-
                                                  ing for automated theorem proving (ATP) for combinatorial identities. To address this, we manu-
                                                  ally construct LeanComb, combinatorial identities benchmark in Lean, which is, to our knowledge,
                                                  the first formalized theorem proving benchmark built for combinatorial identities. We develop an
                                                  Automated Theorem Generator for Combinatorial Identities, ATG4CI, which combines candidate
                                                  tactics suggested by a self-improving large language model with a Reinforcement Learning Tree
                                                  Search approach for tactic prediction. By utilizing ATG4CI, we generate a LeanComb-Enhanced
                                                  dataset comprising 260K combinatorial identities theorems, each with a complete formal proof in
                                                  Lean, and experimental evaluations demonstrate that models trained on this dataset can generate
                                                  more effective tactics, thereby improving success rates in automated theorem proving for combina-
                                                  torial identities.


                                         1 Introduction

                                         The formal theorem proving entails translating theorems and their proofs into a machine-readable format, which allows
                                         computers to autonomously execute logical reasoning and verification, thereby ensuring the absolute correctness of
                                         the theorems [25]. This process is vital to eliminate potential reasoning errors. Formal proofs have been successfully
                                         applied to significant results such as the Kepler Conjecture [30], the Four Color Theorem [26], and the Clausen-
                                         Scholze Conjecture [15]. However, interactive theorem proving (ITP) is labor-intensive, particularly when tackling
                                         complex theorems, demanding a high degree of expertise from human specialists. For instance, the formalization
                                         of the Kepler Conjecture spanned 11 years and involved more than 20 researchers, culminating in a proof through
                                         hundreds of thousands of logical steps [30].
                                         To reduce the high cost of manual formalization, a practical approach is to implement automated theorem proving
                                         (ATP), which streamlines the interaction between human experts and proof assistants. In recent years, with the rapid
                                         advancement of artificial intelligence (AI), large language models (LLMs) have begun to play a role in ATP, integrating
                                         with proof assistants to enhance the capabilities of theorem provers. Some approaches exploit the generative capabili-
                                         ties of LLMs to build complete proofs of theorems in a single decoding process [42, 103, 9]. At the same time, other
                                         mainstream methods utilize fine-tuned models to generate single-step candidate proof tactics based on the current
                                         state of the proof [93, 105, 44, 72, 32], gradually building complete proofs by integrating various search algorithms.
                                         The works described above primarily focus on fundamental mathematical problems, typically at the high school and
                                         undergraduate levels.
                                         Regarding advanced mathematics or more complex mathematical fields, theorem provers based on LLMs still face sig-
                                         nificant challenges. AlphaProof and AlphaGeometry 2 [88] successfully solved four of the six problems in this year’s
International Mathematical Olympiad (IMO) but have yet to tackle the remaining two combinatorics problems [56].
One of the main issues lies in the scarcity of training data, which cannot impact training LLMs. For example, while
the Lean formal proof language library, Mathlib4 [61], contains more than 180K theorems, the distribution between
different mathematical branches is uneven, with only over one hundred in combinatorics.
To break through this predicament, we choose combinatorics as our starting point [85, 52]. Based on Lean [19], a
proof assistant widely embraced by mathematicians, we build a combinatorial identities benchmark, LeanComb, and
introduce an automated theorem generator that combines a self-improving large language model (LLM) [39] with a
reinforcement learning (RL) search method inspired by Monte Carlo Tree Search (MCTS) for generating new theorems
and their proofs. To our knowledge, LeanComb is the first formalized theorem proving benchmark explicitly created
for combinatorial identities. Fine-tuning and evaluating multiple language models with the LeanComb benchmark and
LeanComb-Enhanced dataset, the experimental results show that the models achieved a proof success rate of up to
26%, with each fine-tuned model improving success rates by over 17% compared to the baseline models. The main
contributions of this paper are summarized as follows:

       • We introduce LeanComb, a benchmark for combinatorial identities, comprising 418 identities and 209 lem-
         mas in the training set and 100 identities in the test set.
       • We propose a data augmentation method that combines a self-improving language model with an MCTS-
         inspired search algorithm. Based on the LeanComb benchmark, a LeanComb-Enhanced dataset containing
         260, 466 theorems is automatically generated.
       • Extensive experiments demonstrate that models trained on the LeanComb-Enhanced dataset significantly
         improve the success rate of automated proofs for combinatorial identities. Moreover, evaluations on the
         miniF2F dataset also show improved performance in automated theorem proving.

2 Related Work
Automated theorem proving has gained prominence in artificial intelligence [79, 94, 101], yet its application remains
largely restricted to relatively simple mathematical problems and struggles with proving more complex statements.
Data scarcity and its uneven distribution across different mathematical domains is a key challenge.
Among the largest publicly available datasets in AI4Maths, Numina [58] contains 860K competition-level math prob-
lems with solutions following the Chain of Thought (CoT) [98] reasoning paradigm. In contrast, Mathlib [61], the
community-maintained Lean formal mathematics dataset, provides a rigorously structured repository spanning algebra,
number theory, and combinatorics. However, both datasets rely heavily on manual formalization, leading to limited
coverage and uneven representation across specialized mathematical fields.
To address the limitations of data scarcity, researchers have explored automated theorem generation [70]. In recent
years, theorem generation techniques based on neural networks and LLMs have emerged as a promising direction,
opening up new possibilities for both theorem generation and automated proving [24, 99]. Existing approaches
leverage various strategies for theorem generation: INT [99] integrates inequalities to construct new theorems, Lean-
dojo [105] retrieves and synthesizes formal statements from Mathlib, and MetaGen [95] transplants proof trees while
employing reinforcement learning to align theorem generation with human reasoning. Meanwhile, another class of
generators relies on LLMs to assist in theorem generation. Specifically, these models are often employed as premise
selectors to identify key reasoning steps or to iteratively sample from existing theorems, generating new ones that
adhere to specific rules [89, 92, 67, 72, 100]. Furthermore, the PACT method [32] extracts data from theorems and
generates nine distinct language modeling tasks, enabling data augmentation within the Lean theorem prover.
However, most existing theorem generators expand datasets by extracting sub-theorems from complete theorems or
synthesizing new ones. Against this backdrop, we combine LLMs’ broad knowledge coverage with RL’s exploration-
driven capabilities to conduct tactic prediction research based on our manually constructed benchmark, LeanComb.
Our goal is to generate high-quality, novel theorems that contribute to developing data resources in specialized mathe-
matical fields while advancing the capabilities of automated theorem-proving systems.

3 A Combinatorial Identities Benchmark
In this section, we introduce LeanComb, a manually formalized benchmark for combinatorial identities based on Lean
4 [19]. To the best of our knowledge, LeanComb is the first formal theorem benchmark specifically dedicated to
combinatorial identities, covering a broad range of combinatorics topics, including classical and modern identities.
The dataset aims to provide a rigorously verified and formalized collection of combinatorial identities that can be used

                                                           2
to evaluate the performance of ATP tools. Lean is an interactive theorem prover and programming language developed
by Microsoft Research, which is based on dependent type theory [10]. It is supported by a comprehensive and actively
maintained mathematical library, Mathlib4 [61], developed by its community. In the following paper, Lean refers to
Lean 4 by default.
Our dataset is mainly derived from the classical combinatorial mathematics literature [84, 27, 82]. We manually trans-
late informal statements into formal definitions and theorems, including their statements and proofs. The combinatorial
identities in the training set of LeanComb are primarily selected from [84], while those in the test set are drawn from
[27, 82]. The benchmark consists of 727 combinatorial identities, with 627 theorems in the training set (418 identities
and 209 lemmas) and 100 in the test set (100 identities).

                                   Theorem Categories                           Training Set   Test Set
                                  The Generalized Binomial Coefficient              42           16
               Basic Techniques Absorption Identity                                 35           12
                                  Binomial Inversion                                46            6
                                  Choosing with Replacement                         26            6
               Combinatorics      Alternating Binomial Sums & Involutions           23            6
                                  Inclusion-Exclusion                               27            5
                                  Differentiation                                   20            5
               Calculus           Integration                                       26            3
                                  Beta Integral & Gamma Function                    22            6
                                  Binomial & Hypergeometric Distributions           13            5
               Probability
                                  Expected Values & Moments                         16            3
                Special Numbers                                                     25           10
                Generating Functions                                                29            5
                Recurrence Relations & Finite Differences                           56            6
                Miscellaneous Techniques & Mechanical Summation                     12            6
                Total                                                               418          100
                             Table 1: Theorem categories with training and test set counts


We have formalized 9 new definitions, encompassing theorems related to Stirling numbers of the first and second kind
and their properties. We treat each tactic as a single proof step, e.g., a lemma introduced by the “have” tactic counts
as one step. The maximum number of proof steps in the training set is 98, with an average of 8.9 steps. LeanComb
Benchmark contains many classical theorems, such as:
                                                           Pr
                              Vandermonde ’ s Identity : k=0 Cnk Cm     r−k     r
                                                                             = Cn+m  ,
                              Cassini’s Identity : ∀n ∈ Z, Fn+1 Fn−1 − Fn2 = (−1)n ,
                              Parallel Summation : m        k      m
                                                     P
                                                       k=0 Cn+k = Cn+m+1 .

As shown in Table 1, all identities in the training set and test sets are classified into 8 categories, including Combi-
natorics, Calculus, Probability, and others. The Basic Techniques category contains the most significant samples in
training and test sets, with 123 and 40 samples, respectively. In the “Basic Techniques” category, the Binomial Coef-
ficient and Binomial Inversion, along with the Recurrence Relations & Differences categories, have relatively higher
sample counts, totaling 42, 46, and 56, respectively.
We now use a simple example to demonstrate the formalization of a combinatorial identity in Lean 4.

                                                n
                                                X                n−1
                                                                 X
                                                        k−1             l
                                                      nCn−1 =n         Cn−1 .                                       (1)
                                                k=1              l=0



                                                           3
  1 theorem sum_mul_congr {n : N}:
  2 Σ k in Ico 1 (n + 1), n * choose (n-1) (k-1) = n * Σ l in range n, choose (n-1) l := by
  3     rw [mul_sum]
  4     rw [sum_Ico_eq_sum_range]
  5     simp

                                      Listing 1: A combinatorial identity in Lean 4.

We formalize the statement of the combinatorial identity (1), named sum_mul_congr, in Line 2, with the detailed
proof process presented in Lines 3 through 5. In particular, Line 3 applies the “rw [mul_sum]” tactic to factor the
constant n out of the summation. Then, in Line 4, the “rw [sum_Ico_eq_sum_range]” tactic is used to perform
variable substitution. Finally, the “simp” tactic automatically simplifies the subgoal, successfully advancing the proof
to the “no goals” state. The tactics employed must be predefined or established within the Lean library or associated
files. Since each theorem depends on these tactics, discovering additional high-quality tactics is essential for advancing
the generation of automated theorems.




                                         Figure 1: The Framework of ATG4CI.


4 Lean4Kit
Lean4Kit, built on Lean 4, provides offline data extraction and interaction capabilities, significantly enhancing au-
tomated theorem generation and proving. First, Lean4Kit extracts state-tactic pairs from Lean code to construct a
training set. Second, it enables programmatic interaction with the Lean system, supporting tactic prediction and auto-
mated theorem proving.
Data Extraction. Lean4Kit can access the current proof state in run-time during the Lean theorem proving process.
By interacting with the Lean system, it tracks the proof process and dynamically updates the proof state.
State Information: Our toolkit constructs the sequence of proof states by extracting the Lean code and the proof goal.
Additionally, it captures the error message if an error occurs after invoking a tactic and identifies whether a proof state
has been successfully resolved after executing a tactic.
Premises and Tactics: For the Lean code of a given theorem, the toolkit extracts all premises and variable types,
ensuring that the premises’ names align with those of the Lean libraries. If the proof state is valid at each step of the
proof, it also captures the corresponding tactic used.
Interaction. Another key feature of the toolkit is its ability to interact with Lean 4. It can initialize the proof state,
update it after executing the tactic, and trace the feedback information, including error messages or proof completion.
Lean4kit can also be utilized for tactic prediction, filtering candidate tactics that can efficiently modify the proof state.
Below is a detailed description of the interactive features:
get_init_state (theorem): Given a theorem, our toolkit obtains its initial proof state and extracts data from that state. If
a theorem, including statement and proof, fails validation during interaction, its initial state will be marked as an error.

                                                             4
run_tactic (state, tactic): After applying a tactic to a given state, the updated proof state is returned. If an inapplicable
tactic is executed, an error state and the corresponding error message are generated. If the input state is already an
error, the result will also be an error.

5 The Framework of Automated Theorem Generator for Combinatorial Identities
This section introduces ATG4CI, an iterative framework for automated theorem generation for combinatorial identi-
ties. We propose a tactic prediction method combining a fine-tuned LLM with a reinforcement learning algorithm.
The framework generates candidate theorems using tactic prediction, verifies them through theorem validation, and
compiles the results to build an enhanced dataset. The generated theorem dataset can fine-tune the LLM through iter-
ative refinements, enhancing its tactic prediction capabilities. Meanwhile, with its enhanced predictive capability, the
improved LLM can boost the quantity and quality of automatically generated theorems.
As shown in Fig. 1, ATG4CI comprises three essential stages: Partial Proof Paths (P3s) Construction, Candidate
Theorem Generation, and Theorem Validation. The procedure begins with the LeanComb training set L∗t , consisting
of formalized combinatorial identities, serving as the foundational data for data augmentation and model fine-tuning.
Building upon this, the pipeline enters the P3s Construction phase, where the Lean4Kit tool is employed to transform
each theorem into a proof tree. Their corresponding state-policy pairs are extracted from these trees. The states are
then corrected to ensure their quality and correctness.
Following this, in the Candidate Theorem Generation phase (top right of Fig. 1), the procedure begins with generating
candidate tactics using a fine-tuned model Mct . The candidate tactics are then refined by selecting the most appropriate
ones for each partial proof path (P3) through a Reinforcement Learning-based search tailored to address the specific
requirements of the combinatorial identities domain. This tactic prediction process is repeated to ultimately derive
candidate theorems, followed by the Theorem Validation stage (bottom of Fig. 1), where redundant theorems are
eliminated, and the correctness of the theorems is verified. Specifically, this stage consists of two key steps: Theorem
Deduplication and Error Correction, both of which ensure the uniqueness and correctness of the dataset.
Ultimately, the validated theorems are compiled into a new dataset G∗ , fed to train the model Mct , enhancing its ability
to generate more effective candidate tactics. Finally, the generated dataset is combined with the LeanComb training set
L∗t to form the LeanComb-Enhanced dataset E ∗ , which subsequently improves the performance of automated theorem
proving.

5.1 Partial Proof Paths (P3s) Construction
We focus on the P3s construction process, explaining how to use Lean4Kit to extract partial proof path Ps from
formalized theorems. To facilitate the exploration of new proof paths for P3s, we visualize all tactics within the proof
environment, capturing the state transitions that occur before and after applying each tactic. A fully formalized proven
theorem, consisting of n tactics, can be represented as a proof tree: the root theorem forms the root node, tactics are the
                                                                                                                       n−1
edges, intermediate states are the child nodes, and the “no goals” state is the leaf node. From this tree, Ps = {pi }i=1
is extracted by tracing the paths from the root to the intermediate states.
As shown in Example 1, the root theorem, represented by the root node in (1), transits through three sequential tactics
and eventually reaches the “no goals” state at the leaf node, resulting in a four-layer proof tree. From this tree, two
P3s are extracted: one from the root to the state after applying “rw[mul_sum]”, and another from the root to the state
after applying “rw[sum_Ico_eq_sum_range]”.

5.2 Candidate Theorem Generation
The section explains how to generate candidate theorems from a given partial proof path, which consists of two key
steps: candidate tactic generation, produced by a fine-tuned model, and tactic prediction, based on a reinforcement
learning search for combinatorial identities (RLSCI).
Candidate Tactic Generation. We start with employing a fine-tuned model Mct , trained by the training set of Lean-
Comb, to generate candidate tactics cts for P3s. To enhance the quality and diversity of candidate tactics, we adopt
an iterative refinement tactic inspired by self-improvement techniques for fine-tuning models. Initially, the model is
fine-tuned on the training set of the LeanComb benchmark L∗t and Lean’s foundational library, Mathlib4. Given a
partial proof path, the improved model can generate t candidate tactics, where t is a prior positive integer. The model
will be continuously refined in subsequent iterations through fine-tuning with the augmented theorems generated from
the previous iteration. This iterative framework not only enhances the model’s capacity to propose effective tactics but
also broadens its exploration of diverse tactic spaces.

                                                             5
Tactic Prediction. The tactic prediction, based on RLSCI, consists of three primary steps: selecting candidate tactics,
expanding the P3s, and back-propagating values from the leaf nodes to the root. These steps are iteratively performed
until the proof is completed or no viable tactic is identified. If successful, the process discovers a complete proof path
for the root theorem RT ; otherwise, it generates a candidate proof path cpk for k = 0, 1, . . . , s.
Our RL framework comprises a critic model Cθ and a policy model Pθ . Completed proof nodes are assigned a value
of 1, while failed nodes are assigned a value of −1. Unresolved nodes are evaluated using the Polynomial Upper
Confidence Trees (PUCT) method [83]:
                                                                        pP
                                                                            b N (s, b)
                              QP UCT (s) = Q(s, t) + cpuct · P (s, t) ·                ,
                                                                        N (s, t) + 1
where Q(s, t) is the estimated value of the state-tactic pair, obtained from the value network or learned from past
simulations, and P (s, t) is the probability of selecting a tactic in state s based on the policy network, and cpuct is the
exploration coefficient. In contrast, N (s, t) is the count of executions of tactic t in state s during the prediction process.
All successful tactics are stored as training data for LLMs. During backpropagation, values from the leaf nodes are
propagated to the root, updating the visit counts N (s, t) and cumulative action values.
The process aims to propagate proof paths as far as possible, terminating when the proof is complete or when no viable
tactic can be found. In the former case, the leaf node is marked as “no goals”, indicating the discovery of a new proof
for the root theorem RT . In the latter case, the goals corresponding to the leaf nodes of the candidate proof paths are
treated as candidate theorems, CTm = {CTi }m    i=0 .
To generate new proofs, we incorporate the original root theorem RT into the hypotheses and then apply tactics
from the candidate path until the goal aligns with the target. Once aligned, the “assumption” tactic resolves the goal,
completing the proof. The following example illustrates the above procedure for ATG4CI.
Example 1 Continued. Below is one of the generated candidate proof paths:

  1 theorem cp_1 {n : N} :
  2  Σ k in Ico 1 (n + 1), n * choose (n - 1) (k - 1) = n * Σ k in range n, choose (n - 1) k
        := by
  3     rw [mul_sum]
  4     -- Prediction start!
  5     rw [range_eq_Ico]
  6     rw [sum_Ico_eq_sum_range]
  7     rw [add_tsub_cancel_right]
  8     rw [range_eq_Ico]
  9     -- Prediction end


The P3s spanning Lines 1 to 3 is extracted from Example 1 during the P3s construction phase. It originates from
the root node and extends to the child node after applying the tactic rw[mul_sum]. The tactic prediction process
begins at Line 5, where the LLM is prompted to provide 8 candidate tactics for the current state. Among these,
RLSCI successfully selects four new nodes during the first round. The process proceeds with iterative expansion and
backpropagation, repeating these steps for each new node and ultimately generating over 100 candidate proof paths.
In one instance, after four steps (Lines 5–8), the prediction process identifies that no feasible tactic exists for a specific
path, leaving the subgoal corresponding to its leaf node as follows:
                                            Pn        1+k−1     Pn        l
                                               k=0 nCn−1      = l=0 nCn−1      .                                           (2)

The subgoal presented in (2) is treated as a new candidate theorem:

  1 theorem CT_1 (n : N)
  2   (h : Σ k in Ico 1 (n + 1), n * choose (n - 1) (k - 1) = n * Σ l in range n, choose (n -
        1) l) :
  3   -- Candidate theorem
  4   Σ k in range n, n * Nat.choose (n - 1) k = Σ x in Ico 0 n, n * Nat.choose (n - 1) x :=
        by
  5     rw [mul_sum] at h
  6     rw [range_eq_Ico] at h
  7     rw [sum_Ico_eq_sum_range] at h
  8     rw [add_tsub_cancel_right] at h
  9     assumption


                                                              6
Line 2 shows that the root theorem is adopted as the new hypothesis h. Then, in Lines 5–8, all tactics along the
candidate path are applied sequentially to rewrite h until it aligns with the target goal. Finally, the tactic “assumption”
in Line 9 is used to conclude the proof.

5.3 Theorem Validation

Note that not all candidate theorems are correct or unique, so a validation process, including theorem deduplication
and correction, is necessary to retain the valid theorems.
Theorem Deduplication: Candidate theorems are deduplicated from two perspectives. First, textual duplication is
identified by comparing the goals, premises, and proof steps. Identical theorems are merged, retaining only one.
Second, mathematical equivalence is checked by simplifying redundant terms (e.g., +0, −0, ∗1, and /1), ensuring that
only one mathematically equivalent version is kept.
Theorem Correction: After deduplication, as some candidate theorems may still contain expression errors or fail to
pass the proof process, correctness refinement is performed. After candidate theorems are verified successfully by
interacting with Lean, they are directly added to the generated dataset G∗ . Those that fail verification are categorized
by error type and corrected using the corresponding correction methods. The corrected theorems are then added to G∗ .
The following section elaborates on the error types and their corresponding correction tactics.
       • Incomplete Errors. An incomplete error occurs when a candidate tactic generates multiple subgoals, all of
         which are correct, but at least one subgoal remains unproven, preventing the completion of the theorem’s
         proof. The standard MCTS [17] method can be applied to recover incomplete theorems and generate addi-
         tional proof steps to complete the proof.
       • Type Errors. Type errors arise due to Lean’s representation methods, where variable types in subgoals are
         not always explicitly stated during interactions with Lean or during the data extraction process. For example,
         if the original theorem’s goal contains the term “(−1 : R)”, the extraction may capture only “(−1) ↑”. To
         address this, we identify the type information from the original theorem and annotate the newly generated
         theorems with the correct type labels.
       • Logical Errors. Logical errors occur when applying a candidate tactic generates multiple subgoals, but at
         least one contains a logical inconsistency, preventing further progress in the proof. For instance, consider the
                                                                  Pn        k−1        Pn−1 l
         following theorem where n must be a natural number: k=1 nCn−1            = n l=1 Cn−1       . After applying the
         tactic “rw[sum_Ico_succ_top]”, two subgoals are generated, one of which is 1 ≤ n, which contradicts the
         definition of natural numbers. Theorems with such logical inconsistencies are considered irreparable at this
         stage and must be discarded.
Then, we briefly introduce the main steps of ATG4CI implemented in Algorithm 1. The procedure takes as inputs the
training set of LeanComb Benchmark L∗t , the model Mct that provides candidate tactics cts , search method RLSCI,
the maximum number of iterations n, and returns the LeanComb-Enhanced dataset E ∗ .

Algorithm 1 The Framework of ATG4CI
Require: The training set of LeanComb Benchmark L∗t , the model Mct that provides candidate tactics cts , search
    method RLSCI, maximum number of iterations n
Ensure: LeanComb-Enhanced dataset E∗
 1: Ps ← Construct_P3s(L∗t )
 2: G0 ← L∗t
 3: for i = 0 → n do
           i
 4:     Mct  ← F intune(Gi )
                                  i
 5:     cts ← P roduce_cts (Ps , Mct )
 6:     Gi ← Generate_CTs (cts , RLSCI)
 7:     G∗i ← V alidation(Gi )
 8:     E ∗ ← E ∗ + G∗i
 9: end for
10: return E∗

We first construct partial proof paths Ps and initialize the generated dataset as G0 based on the LeanComb training set
L∗t . Subsequently, the following steps are iteratively performed within a predefined maximum number of iterations.
First, the model Mct is fine-tuned using the current generated dataset (as described in Line 4). Next, based on P3s,
Mct is employed to generate candidate tactics (line 5). Subsequently, the search algorithm RLSCI is applied to

                                                            7
generate candidate theorems (Line 6). The generated candidate theorems must undergo rigorous validation before
being incorporated into the generated dataset G∗i and further integrated into the enhanced dataset E ∗ (Line 7).

6 Experiments
In this section, we employ ATG4CI to construct the LeanComb-Enhanced dataset for combinatorial identities. Subse-
quently, we evaluate the performance of fine-tuned LLMs in automated theorem proving on both the LeanComb test
set and the miniF2F dataset. Our models, trained on both the LeanComb benchmark and the Enhanced dataset, consis-
tently achieve higher proof success rates compared to the baseline, demonstrating the effectiveness of our dataset.

6.1 LeanComb-Enhanced Dataset Generated by ATG4CI

In this experiment, we iteratively fine-tune the general-purpose LLM Llama3.1-8b [6] to assist the theorem generation
process by providing candidate tactics for tactic prediction. The number of tactics suggested by the model for each
node is limited to 16.
Tactic Prediction Model Architecture. In tactic prediction process, the RL component of the RLSCI search algorithm
is implemented using two neural networks: a policy network and a critic network. Each network comprises two linear
layers, each with a dimensionality of 16. The training process spans a total of 10 iterations. During each decision-
making step, the algorithm performs 100 simulations, with the total number of full events per iteration fixed at 20.
Furthermore, each node is allowed to propose up to 16 candidate theorems. The search time is restricted to 300
seconds.

                           Table 2: The performance with varying candidate tactic counts.

                                                                    # Candidate Tactics
                      # Iteration     Theorem Types
                                                                4             8            16

                                         # Candidate          211,087     364,789      592,811
                                       # Deduplicated         73,385      229,541      392,818
                        1st Iter          # Correct           16,296       52,220         68,771
                                         # Corrected           6,395       21,916         31,306
                                    Subtotal                  22,691       74,136      100,077

                                         # Candidate          247,996     376,158      440,199
                                       # Deduplicated         185,850     225,797      238,425
                       2nd Iter           # Correct           69,765      132,791      135,796
                                         # Corrected          13,912       24,147         24,593
                                    Subtotal                  83,677      156,938      160,389

                                     Total                    106,368     231,074      260,466


Results. Table 2 presents the theorems generated by our ATG4CI under different candidate tactic settings (4, 8,
and 16) based on the LeanComb training set. The experiment consists of two iterations. In the first iteration, with
16 candidate tactics, 592, 811 theorems are generated, which are reduced to 392, 818 deduplicated theorems after
deduplication. Among these, 68, 771 are correct, and 31, 306 incorrect theorems are successfully repaired, yielding
100, 077 new theorems. For candidate tactic settings 4 and 8, the numbers of new theorems obtained are 22, 691 and
74, 136, respectively.
After training models with the generated data, the second iteration produced 156, 938 new theorems for tactic settings
8 and 160, 389 for 16. The LeanComb-Enhanced dataset, obtained by merging and deduplicating results from both
iterations, contains 260, 466 new theorems.
In the first iteration, the proportion of correct theorems after deduplication ranges from 17.5% to 22.7%, increasing
significantly to a maximum of 75.0% in the second iteration. The proportion of newly generated theorems is also im-

                                                          8
proved from 10.7%, 20.3%, and 16.9% in the first iteration to 33.7%, 41.7%, and 36.4% in the second, demonstrating
the effectiveness of iterative refinement. The 16-tactic setting produces the highest number of theorems, while the
8-tactic setting achieves the highest success rate for generating new theorems.
These results emphasize the importance of deduplication in reducing redundancy and improving data quality, while
correction steps can improve the success rate. The observed improvement in the second iteration validates the effec-
tiveness of iterative optimization in refining theorem generation.
Prediction Steps. Fig.2 presents the distribution of theorem counts across different prediction steps, categorized into
four groups: deduplicated, correct, corrected, and new theorems. The data reveal a peak around a prediction step
of 6, indicating that most theorems are concentrated at this length regardless of their classification. The number of
deduplicated theorems exhibits the highest count, peaking at 121, 457. In contrast, the correct and new theorems
follow similar trends but at lower magnitudes, suggesting that a significant proportion of generated theorems are either
duplicates or require correction. The corrected theorems, represented by the green triangles, remain consistently lower
than the other categories, highlighting the challenges in refining generated theorems through correction mechanisms.

                                                                                                       Deduplicated
                                        120
                                                                                                         Correct
                                                                                                        Corrected
                Theorem Number (×103)




                                        100                                                               New

                                        80

                                        60

                                        40

                                        20

                                         0
                                              0                        5                       10                     15
                                                                            Prediction Steps

                                                  Figure 2: Distribution of Theorem Numbers on Prediction Steps

Additionally, the distribution demonstrates a sharp decline in theorem numbers beyond a prediction step of 6, implying
that longer proof sequences are less frequent and potentially more challenging to generate and verify. These findings
suggest that optimizing theorem generation should focus on mid-range prediction steps, where the balance between
uniqueness, correctness, and novelty is most favorable.

6.2 Theorem Proving on LeanComb Benchmark and MiniF2F

We evaluate the theorem-proving capabilities of LLMs on the test sets of LeanComb benchmark and miniF2F [107],
utilizing Pass@1 (%) as the primary evaluation metric. Pass@1 is defined as the success rate of constructing a valid
proof within a single attempt, constrained by a strict wall time limit of 10 minutes. The experiment involves four
models: Gemma2 [86], Mathstral3 [2], Llama3 [28], and Mistral [41]. The baseline models are initially pre-trained
on Mathlib4 and subsequently fine-tuned on the LeanComb training set. To further enhance their performance, an
additional fine-tuning stage is conducted using an augmented dataset generated by our theorem generator. During
inference, the number of candidate tactics generated by the models is restricted to a maximum of 16.
Evaluation on LeanComb Benchmark. We utilize the LeanComb benchmark to optimize the tactic selection of
LLMs, thereby substantially enhancing their theorem-proving capabilities. As presented in Table 3, experimental
results indicate that all models exhibit significant performance improvements after fine-tuning on the LeanComb and
LeanComb-Enhanced datasets, with success rate increases ranging from 5% to 17%. Notably, models trained on the
first iteration of generated data (1st Iter) show substantial improvements, with success rates increasing by up to 13%
over the baseline. However, further refinement in the second iteration (2nd Iter) leads to even more significant gains,
with a maximum success rate of 26%. This iterative process underscores the necessity of multiple fine-tuning stages
to fully unlock the potential of the generated datasets.

                                                                               9
These findings highlight the importance of continued training and the effectiveness of the generated datasets in advanc-
ing model performance in ATP tasks for combinatorial identities.

                          Table 3: Success rates on the LeanComb test set with Pass@1 (%).

                                                                              LeanComb-Enh.
                 Model                       Base        LeanComb
                                                                           1st Iter        2nd Iter
                 Gemma2 - 9B                 10%               15%           17%             23%
                 Mathstral3 - 8B              9%               19%           22%             25%
                 Llama3 - 8B                  9%               15%           17%             22%
                 Mistral - 7B                 9%               17%           18%             26%

Evaluation on MiniF2F. Table 4 provides a comparative analysis of different LLMs fine-tuned with LeanComb and
LeanComb-Enhanced, on the miniF2F-test dataset. We evaluate the impact of our datasets on the success rates of
fine-tuned models when tested on the miniF2F dataset. The success rate of the model trained on Mathlib+LeanComb,
is about 0.4% to 4.1% higher than that of the model trained solely on Mathlib, with an average improvement of 1.45%.
Meanwhile, the success rate of the model trained on Mathlib+LeanComb-Enhanced, shows an increase of about 3.3%
to 6.2% compared to the model trained solely on Mathlib, with an average improvement of 4.9%.
Notably, when we look at the performance of the models fine-tuned with LeanComb-Enhanced in two iterations,
significant improvements are observed across all models. The first iteration (1st Iter) provides an increase of around
1.0% to 3.7% over LeanComb, and further fine-tuning in the second iteration (2nd Iter) leads to even more substantial
improvements, with success rates rising by 1.1% to 2.8%. For example, the Gemma2 model’s success rate increases
from 27.9% (1st Iter) to 30.3% (2nd Iter), and similarly, the Mathtral3 model improves from 33.6% to 36.1%. These
results clearly demonstrate the effectiveness of the iterative fine-tuning process, with the second iteration playing a
crucial role in achieving the highest performance across all models.

                           Table 4: Success rates on the miniF2F test set with Pass@1(%).

                                                                              LeanComb-Enh.
                  Model                      Base        LeanComb
                                                                           1st Iter        2nd Iter

                 Gemma2 - 9B                26.2%           27.0%           27.9%           30.3%
                 Mathtral3 - 8B             29.9%           30.3%           33.6%           36.1%
                 Llama3 - 8B                29.1%           31.1%           34.0%           34.8%
                 Mistral - 7B               28.7%           32.8%           33.2%           34.8%

The above analysis can also support that our datasets are a necessary complement to enhance the automated theorem
proving capabilities of existing LLMs.

7 Conclusion
In this work, we presented a novel automated theorem generator, ATG4CI, for combinatorial identities, which started
by calling LLM to yield the candidate tactics and then applied deep reinforcement learning for tactic prediction.
We manually built LeanComb benchmark for combinatorial identities and automatically generated the LeanComb-
Enhanced dataset obtained from ATG4CI. To evaluate its impact, we fine-tuned LLMs on these datasets. Experimental
results indicate that our benchmark and dataset significantly improve the performance of LLMs in automated theorem
proving.




                                                          10
References
 [1] Marah Abdin, Sam Ade Jacobs, Ammar Ahmad Awan, Jyoti Aneja, Ahmed Awadallah, Hany Awadalla, Nguyen
     Bach, Amit Bahree, Arash Bakhtiari, Harkirat Behl, et al. Phi-3 technical report: A highly capable language
     model locally on your phone. arXiv preprint arXiv:2404.14219, 2024.
 [2] Mistral AI. Mathstral: Advancing mathematical reasoning with 7b parameters. Technical Report, 2024. Avail-
     able at https://mistral.ai/news/mathstral/.
 [3] Peter Auer, Nicolo Cesa-Bianchi, and Paul Fischer. Finite-time analysis of the multiarmed bandit problem.
     Machine learning, 47:235–256, 2002.
 [4] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev, and Jeremy
     Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics. arXiv preprint
     arXiv:2302.12433, 2023.
 [5] Kshitij Bansal, Sarah Loos, Markus Rabe, Christian Szegedy, and Stewart Wilcox. Holist: An environment for
     machine learning of higher order logic theorem proving. In International Conference on Machine Learning,
     pages 454–463. PMLR, 2019.
 [6] Stella Biderman, Hailey Schoelkopf, Quentin Gregory Anthony, Herbie Bradley, Kyle O’Brien, Eric Hallahan,
     Mohammad Aflah Khan, Shivanshu Purohit, USVSN Sai Prashanth, Edward Raff, et al. Pythia: A suite for
     analyzing large language models across training and scaling. In International Conference on Machine Learning,
     pages 2397–2430. PMLR, 2023.
 [7] Richard A Brualdi. Introductory combinatorics. Pearson Education India, 2004.
 [8] Kevin Buzzard. The future of mathematics. Technical report, CRNS-Imperial Lecture, 2019.
 [9] Zheng Cai, Maosong Cao, Haojiong Chen, Kai Chen, Keyu Chen, Xin Chen, Xun Chen, Zehui Chen, Zhi Chen,
     Pei Chu, et al. Internlm2 technical report. arXiv preprint arXiv:2403.17297, 2024.
[10] Adam Chlipala. Certified programming with dependent types: a pragmatic introduction to the Coq proof
     assistant. MIT Press, 2022.
[11] William J. Clancey. Transfer of Rule-Based Expertise through a Tutorial Dialogue. Ph.D. diss., Dept. of
     Computer Science, Stanford Univ., Stanford, Calif., 1979.
[12] William J. Clancey. Communication, Simulation, and Intelligent Agents: Implications of Personal Intelligent
     Machines for Medical Education. In Proceedings of the Eighth International Joint Conference on Artificial
     Intelligence (IJCAI-83), pages 556–560, Menlo Park, Calif, 1983. IJCAI Organization.
[13] William J. Clancey. Classification Problem Solving. In Proceedings of the Fourth National Conference on
     Artificial Intelligence, pages 45–54, Menlo Park, Calif., 1984. AAAI Press.
[14] William J. Clancey. The Engineering of Qualitative Models. Forthcoming, 2021.
[15] Mathlib Community. Completion of the liquid tensor experiment. https://leanprover-community.
     github.io/blog/posts/lte-final/, 2022.
[16] Projet Coq. The coq proof assistant-reference manual. INRIA Rocquencourt and ENS Lyon, version, 5, 1996.
[17] Rémi Coulom. Efficient selectivity and backup operators in monte-carlo tree search. In International conference
     on computers and games, pages 72–83. Springer, 2006.
[18] Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In International conference on Tools and
     Algorithms for the Construction and Analysis of Systems, pages 337–340. Springer, 2008.
[19] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer. The lean
     theorem prover (system description). In Automated Deduction-CADE-25: 25th International Conference on
     Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceedings 25, pages 378–388. Springer, 2015.
[20] Tim Dettmers, Mike Lewis, Sam Shleifer, and Luke Zettlemoyer. 8-bit optimizers via block-wise quantization,
     2022.
[21] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,
     Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv preprint
     arXiv:2407.21783, 2024.
[22] Robert Engelmore and Anthony Morgan, editors. Blackboard Systems. Addison-Wesley, Reading, Mass., 1986.
[23] Emily First, Markus N Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation and repair with
     large language models. In Proceedings of the 31st ACM Joint European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering, pages 1229–1241, 2023.

                                                       11
[24] Thibault Gauthier. Deep reinforcement learning for synthesizing functions in higher-order logic. arXiv preprint
     arXiv:1910.11797, 2019.
[25] Herman Geuvers. Proof assistants: History, ideas and future. Sadhana, 34:3–25, 2009.
[26] Georges Gonthier et al. Formal proof–the four-color theorem. Notices of the AMS, 55(11):1382–1393, 2008.
[27] H. W. Gould. Combinatorial Identities. West Virginia University, Morgantown, WV, 1972.
[28] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle,
     Aiesha Letman, Akhil Mathur, Alan Schelten, and et al Alex Vaughan. The llama 3 herd of models, 2024.
[29] Sorin Grigorescu, Bogdan Trasnea, Tiberiu Cocias, and Gigel Macesanu. A survey of deep learning techniques
     for autonomous driving. Journal of field robotics, 37(3):362–386, 2020.
[30] Thomas Hales, Mark Adams, Gertrud Bauer, Tat Dat Dang, John Harrison, Hoang Le Truong, Cezary Kaliszyk,
     Victor Magron, Sean McLaughlin, Tat Thang Nguyen, et al. A formal proof of the Kepler conjecture. In Forum
     of Mathematics, Pi, volume 5, page e2. Cambridge University Press, 2017.
[31] Jesse Michael Han. Contributions to Neural Theorem Proving. PhD thesis, University of Pittsburgh, 2023.
[32] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W Ayers, and Stanislas Polu. Proof artifact co-training for
     theorem proving with language models. arXiv preprint arXiv:2102.06203, 2021.
[33] John Harrison. Hol light: A tutorial introduction. In International Conference on Formal Methods in Computer-
     Aided Design, pages 265–269. Springer, 1996.
[34] Diane Warner Hasling, William J. Clancey, and Glenn Rennels. Strategic explanations for a diagnostic consul-
     tation system. International Journal of Man-Machine Studies, 20(1):3–19, 1984.
[35] Diane Warner Hasling, William J. Clancey, Glenn R. Rennels, and Thomas Test. Strategic Explanations in
     Consultation—Duplicate. The International Journal of Man-Machine Studies, 20(1):3–19, 1983.
[36] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu
     Chen. Lora: Low-rank adaptation of large language models, 2021.
[37] Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever. Gamepad: A learning environment for
     theorem proving. arXiv preprint arXiv:1806.00608, 2018.
[38] Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever. Gamepad: A learning environment for
     theorem proving. arXiv preprint arXiv:1806.00608, 2018.
[39] Jiaxin Huang, Shixiang Shane Gu, Le Hou, Yuexin Wu, Xuezhi Wang, Hongkun Yu, and Jiawei Han. Large
     language models can self-improve. arXiv preprint arXiv:2210.11610, 2022.
[40] Sam Ade Jacobs, Masahiro Tanaka, Chengming Zhang, Minjia Zhang, Shuaiwen Leon Song, Samyam Rajbhan-
     dari, and Yuxiong He. Deepspeed ulysses: System optimizations for enabling training of extreme long sequence
     transformer models, 2023.
[41] Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las
     Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al. Mistral 7b. arXiv preprint
     arXiv:2310.06825, 2023.
[42] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix,
     Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem provers with informal
     proofs. arXiv preprint arXiv:2210.12283, 2022.
[43] Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han, and Yuhuai Wu. Lisa: Language models of isabelle proofs.
     In 6th Conference on Artificial Intelligence and Theorem Proving, pages 378–392, 2021.
[44] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr Miłoś,
     Yuhuai Wu, and Mateja Jamnik. Thor: Wielding hammers to integrate language models and automated theorem
     provers. Advances in Neural Information Processing Systems, 35:8360–8373, 2022.
[45] Justin Johnson, Bharath Hariharan, Laurens Van Der Maaten, Li Fei-Fei, C Lawrence Zitnick, and Ross Gir-
     shick. Clevr: A diagnostic dataset for compositional language and elementary visual reasoning. In Proceedings
     of the IEEE conference on computer vision and pattern recognition, pages 2901–2910, 2017.
[46] Cezary Kaliszyk, François Chollet, and Christian Szegedy. Holstep: A machine learning dataset for higher-order
     logic theorem proving. corr abs/1703.00426 (2017). arXiv preprint arXiv:1703.00426, 2017.
[47] Matt Kaufmann and J Strother Moore. An acl2 tutorial. In International Conference on Theorem Proving in
     Higher Order Logics, pages 17–21. Springer, 2008.

                                                       12
[48] M. J. Kearns. Computational Complexity of Machine Learning. PhD thesis, Department of Computer Science,
     Harvard University, 1989.
[49] Adam Kilgarriff, Vít Baisa, Jan Bušta, Miloš Jakubíček, Vojtěch Kovář, Jan Michelfeit, Pavel Rychlỳ, and Vít
     Suchomel. The sketch engine: ten years on. Lexicography, 1(1):7–36, 2014.
[50] Levente Kocsis and Csaba Szepesvári. Bandit based monte-carlo planning. In European conference on machine
     learning, pages 282–293. Springer, 2006.
[51] Laura Kovács and Andrei Voronkov. First-order theorem proving and vampire. In International Conference on
     Computer Aided Verification, pages 1–35. Springer, 2013.
[52] SG Krantz. An Episodic History of Mathematics: Mathematical Culture through Problem Solving. Maa, 2010.
[53] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E Hinton. Imagenet classification with deep convolutional neural
     networks. Communications of the ACM, 60(6):84–90, 2017.
[54] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury Hayat, Thibaut
     Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural theorem proving. Advances in
     neural information processing systems, 35:26337–26349, 2022.
[55] P. Langley. Crafting papers on machine learning. In Pat Langley, editor, Proceedings of the 17th International
     Conference on Machine Learning (ICML 2000), pages 1207–1216, Stanford, CA, 2000. Morgan Kaufmann.
[56] LessWrong . Ai achieves silver medal standard solving international mathematics olympiad problems, 2024.
     Retrieved January 4, 2025.
[57] Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh,
     Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, et al. Solving quantitative reasoning problems
     with language models. Advances in Neural Information Processing Systems, 35:3843–3857, 2022.
[58] Jia Li, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Huang, Kashif Rasul, Longhui
     Yu, Albert Q Jiang, Ziju Shen, et al. Numinamath: The largest public dataset in ai4maths with 860k pairs of
     competition math problems and solutions. Hugging Face repository, 13, 2024.
[59] Wenda Li, Lei Yu, Yuhuai Wu, and Lawrence C Paulson. Isarstep: a benchmark for high-level mathematical
     reasoning. arXiv preprint arXiv:2006.09265, 2020.
[60] Ben Mann, N Ryder, M Subbiah, J Kaplan, P Dhariwal, A Neelakantan, P Shyam, G Sastry, A Askell, S Agar-
     wal, et al. Language models are few-shot learners. arXiv preprint arXiv:2005.14165, 1, 2020.
[61] The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN International
     Conference on Certified Programs and Proofs, POPL ’20. ACM, January 2020.
[62] William McCune. Release of prover9. In Mile high conference on quasigroups, loops and nonassociative
     systems, Denver, Colorado, 2005.
[63] Norman Megill. A computer language for pure mathematics, 1997.
[64] T. M. Mitchell. The need for biases in learning generalizations. Technical report, Computer Science Department,
     Rutgers University, New Brunswick, MA, 1980.
[65] NASA. Pluto: The ’other’ red planet. https://www.nasa.gov/nh/pluto-the-other-red-planet, 2015.
     Accessed: 2018-12-06.
[66] Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang,
     Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Mad-
     die Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe. Training language
     models to follow instructions with human feedback, 2022.
[67] Joseph Palermo, Johnny Ye, and Jesse Michael Han. Synthetic proof term data augmentation for theorem
     proving with language models. In Proceedings of the 7th Conference on Artificial Intelligence and Theorem
     Proving, 2022.
[68] Lawrence C Paulson. Natural deduction as higher-order resolution. The Journal of Logic Programming,
     3(3):237–258, 1986.
[69] Judea Pearl. Heuristics: intelligent search strategies for computer problem solving. Addison-Wesley Longman
     Publishing Co., Inc., USA, 1984.
[70] Bartosz Piotrowski and Josef Urban. Atpboost: Learning premise selection in binary setting with atp feedback.
     In Automated Reasoning: 9th International Joint Conference, IJCAR 2018, Held as Part of the Federated Logic
     Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings 9, pages 566–574. Springer, 2018.

                                                        13
[71] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya Sutskever. Formal
     mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344, 2022.
[72] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving. arXiv preprint
     arXiv:2009.03393, 2020.
[73] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models
     are unsupervised multitask learners. OpenAI blog, 1(8):9, 2019.
[74] Tom Reichel, R Henderson, Andrew Touchet, Andrew Gardner, and Talia Ringer. Proof repair infrastructure
     for supervised models: Building a large proof repair dataset. In 14th International Conference on Interactive
     Theorem Proving (ITP 2023). Schloss-Dagstuhl-Leibniz Zentrum für Informatik, 2023.
[75] James Rice. Poligon: A System for Parallel Problem Solving. Technical Report KSL-86-19, Dept. of Computer
     Science, Stanford Univ., 1986.
[76] Arthur L. Robinson. New ways to make microcircuits smaller. Science, 208(4447):1019–1022, 1980.
[77] Arthur L. Robinson. New Ways to Make Microcircuits Smaller—Duplicate Entry. Science, 208:1019–1026,
     1980.
[78] German Ros, Laura Sellart, Joanna Materzynska, David Vazquez, and Antonio M Lopez. The synthia dataset:
     A large collection of synthetic images for semantic segmentation of urban scenes. In Proceedings of the IEEE
     conference on computer vision and pattern recognition, pages 3234–3243, 2016.
[79] David Saxton, Edward Grefenstette, Felix Hill, and Pushmeet Kohli. Analysing mathematical reasoning abilities
     of neural models. arXiv preprint arXiv:1904.01557, 2019.
[80] Stephan Schulz. System description: E 1.8. In In International Conference on Logic for Programming Artificial
     Intelligence and Reasoning, page 735–743. Springer, 1983.
[81] Stephan Schulz. E–a brainiac theorem prover. Ai Communications, 15(2-3):111–126, 2002.
[82] Jihuai Shi. Combinatorial Identities. University of Science and Technology of China Press, 2001.
[83] David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc
     Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, et al. Mastering chess and shogi by self-play with
     a general reinforcement learning algorithm. arXiv preprint arXiv:1712.01815, 2017.
[84] Michael Z Spivey. The art of proving binomial identities. Chapman and Hall/CRC, 2019.
[85] Richard P Stanley. What is enumerative combinatorics? Springer, 1986.
[86] Gemma Team, Shreya Pathak Morgane Riviere, and et al. Gemma 2: Improving open language models at a
     practical size, 2024.
[87] Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju,
     Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, et al. Gemma 2: Improving open
     language models at a practical size. arXiv preprint arXiv:2408.00118, 2024.
[88] Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving olympiad geometry without human
     demonstrations. Nature, 625(7995):476–482, 2024.
[89] Josef Urban and Jan Jakubǔv. First neural conjecturing datasets and experiments. In Intelligent Computer
     Mathematics: 13th International Conference, CICM 2020, Bertinoro, Italy, July 26–31, 2020, Proceedings 13,
     pages 315–323. Springer, 2020.
[90] Ashish Vaswani. Attention is all you need. arXiv preprint arXiv:1706.03762, 2017.
[91] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser,
     and Illia Polosukhin. Attention is all you need, 2017.
[92] Rahul Vishwakarma and Subhankar Mishra. Enhancing neural theorem proving through data augmentation and
     dynamic sampling method. arXiv preprint arXiv:2312.14188, 2023.
[93] Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen, Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun Li,
     Lin Li, et al. Dt-solver: Automated theorem proving with dynamic-tree sampling guided by proof-level value
     function. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume
     1: Long Papers), pages 12632–12646, 2023.
[94] Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen, Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun Li,
     Lin Li, Jian Yin, Zhenguo Li, and Xiaodan Liang. DT-solver: Automated theorem proving with dynamic-tree
     sampling guided by proof-level value function. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki,
     editors, Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1:
     Long Papers), pages 12632–12646, Toronto, Canada, July 2023. Association for Computational Linguistics.

                                                      14
 [95] Mingzhe Wang and Jia Deng. Learning to prove theorems by learning to generate theorems. Advances in Neural
      Information Processing Systems, 33:18146–18157, 2020.
 [96] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and
      Denny Zhou. Self-consistency improves chain of thought reasoning in language models. arXiv preprint
      arXiv:2203.11171, 2022.
 [97] Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M.
      Dai, and Quoc V. Le. Finetuned language models are zero-shot learners, 2022.
 [98] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
      and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In Proceedings of
      the 36th International Conference on Neural Information Processing Systems, NIPS ’22, Red Hook, NY, USA,
      2022. Curran Associates Inc.
 [99] Yuhuai Wu, Albert Q. Jiang, Jimmy Ba, and Roger Baker Grosse. INT: an inequality benchmark for evaluating
      generalization in theorem proving. In 9th International Conference on Learning Representations, ICLR 2021,
      Virtual Event, Austria, May 3-7, 2021. OpenReview.net, 2021.
[100] Yuhuai Wu, Markus N Rabe, Wenda Li, Jimmy Ba, Roger B Grosse, and Christian Szegedy. Lime: Learning
      inductive bias for primitives of mathematical reasoning. In International Conference on Machine Learning,
      pages 11251–11262. PMLR, 2021.
[101] Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai Chen. Internlm2.5-
      stepprover: Advancing automated theorem proving via expert iteration on large-scale LEAN problems. CoRR,
      abs/2410.15700, 2024.
[102] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and Xiaodan
      Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale synthetic data. arXiv preprint
      arXiv:2405.14333, 2024.
[103] Huajian Xin, Haiming Wang, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya Huang, Jing
      Xiong, Han Shi, Enze Xie, et al. Lego-prover: Neural theorem proving with growing libraries. arXiv preprint
      arXiv:2310.00656, 2023.
[104] Kaiyu Yang and Jia Deng. Learning to prove theorems via interacting with proof assistants. In International
      Conference on Machine Learning, pages 6984–6994. PMLR, 2019.
[105] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger,
      and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented language models. Ad-
      vances in Neural Information Processing Systems, 36, 2024.
[106] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for formal
      olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.
[107] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for formal
      olympiad-level mathematics, 2022.
[108] Xinyu Zhu, Junjie Wang, Lin Zhang, Yuxiang Zhang, Yongfeng Huang, Ruyi Gan, Jiaxing Zhang, and Yu-
      jiu Yang. Solving math word problems via cooperative reasoning induced language models. arXiv preprint
      arXiv:2210.16257, 2022.




                                                       15
A     Identities in LeanComb Benchmark
The LeanComb benchmark dataset is constructed based on authoritative literature in the field of classical combina-
torics [84, 27, 82], aiming to provide a high-quality mathematical reasoning benchmark to support automated theorem
proving for combinatorial identities. The dataset comprises a total of 727 theorems, with the training set consisting
of 627 theorems (including 418 combinatorial identities and 209 general theorems), while the test set contains 100
theorems. Additionally, we have formally introduced 9 new mathematical definitions, covering fundamental concepts
such as Bell numbers, Stirling numbers of the first and second kinds, and combinations and permutations, thereby
enhancing the expressiveness of the benchmark dataset.
This dataset encompasses numerous classical theorems in combinatorics, including the Negative Binomial Series,
Binet’s Formula, Vandermonde’s Identity, Trinomial Revision. For example:
                                                                                  ∞        
                                                                         1       X    n+k k
              Negative Binomial Series: ∀x ∈ [0, 1] and n ∈ Z≥0 ,              =             x ,
                                                                    (1 − x)n+1          n
                                                                                        k=0
                                         φn − ψ n
              Binet’s Formula: Fn =         √      .
                                               5

The expressions nk and Cnk are equivalent. To systematically illustrate the diversity of the dataset and the core math-
                    
ematical structures involved, we have selected several representative combinatorial identity examples and categorized
them based on their roles within the dataset. The selected examples are divided into two parts: one from the training set
and the other from the test set. Each part includes various types of combinatorial identities, covering key topics such
as the properties of Stirling numbers, classical combinatorial identities, and their variants. These examples not only
provide an intuitive understanding of the dataset’s composition but also establish a solid foundation for subsequent
theoretical analysis and model evaluation.

A.1 Training Set

         idt_15
               Pm
         Goal: k=0 n+k           n+m+1
                                       
                    k    =         m


         idt_101
                 Pn         k+1 k+1 n−k
                         n (x2 −x1 )y       1
                                               Pn ((x2 +y)k+1 −(x1 +y)k+1 )yn−k
         Goal:     k=0   k      (k+1)2   = n+1  k=0            k+1


         idt_105

         Premises: a, b ∈ R≥0

         Goal: B(a, b) = Γ(a)Γ(b)
                          Γ(a+b)


         idt_106

         Premises: n − k > −1
                             R1
         Goal: nk!k = (n + 1) 0 xk (1 − x)n−k dx

         idt_109

         Premises: x > 0
              Pn            k
         Goal: k=0 nk (−1)          n!
                       
                         k+x = x(x+1)...(x+n)


         idt_112

                                                          16
               Pn         n
                                                     n−2
       Goal:        k=0   k k(k + m) = n(n + 2m + 1)2


       idt_115

       Goal: rk=0 r−k
                   n
             P         m+k   k              n−m−1
                                                    
                         m (−1) =               r


       idt_117
            Pn
       Goal: k=0 nk (n+1)(n+2)(n+3)      n+3
                                             − 1 − (n + 3) − (n+2)(n+3)
                   
                     (k+1)(k+2)(k+3) = 2                         2


       idt_121
                     2n
             P∞
       Goal: n=0 (2n+1)      = π2
                          n)
                        (2n

       idt_124
                                Rπ
       Goal:    1
                      = 2(n + 1) 02 sin2k+1 θ cos2n−2k+1 θdθ
               (nk)

       idt_131

       Premises: 0 ≤ p ≤ 1

       Goal: nk=0 nk pk (1 − p)n−k k 2 = n2 p2 + np(1 − p)
            P        


       idt_132
             Pm
       Goal: k=0 m
                    n               m+n rm
                                          
                 k  r−k k =            r  m+n


       idt_179

       Premises: n ≤ m

       Goal: ∆n Fm = Fm−n

       idt_212
               Pn         n
                               (−1)k          Hn+m −Hm
       Goal:        k=1   k k(k+1)···(k+m) = −    m!


       idt_285

       Premises: 0 < y
            Pn
       Goal: k=0 nk ik y n−k = (y 2 + 1)n/2 ei n arctan(1/y)
                     


       idt_318
                   n             2n
                                    sin nπ
                       k
                       3 (−1)k = √
             P
       Goal: k≥0 2k+1             3      3



A.2 Test Set

       test_002

                                                          17
                                       n+k
         Goal: nk+1 = (k + 1)! ×
                                             
                                       k+1

         test_005
         Premises: n : N; n ≥ 1
         Goal: nk=1 k1 2(k−1)
                                2(n−k)                2n
                                         = 21
               P                                             
                          k−1     n−k                    n

         test_011
         Premises: n, m : N; m ≥ 2n; 1 ≤ n
                n                   
               X           n    m − 2k
         Goal:    (−1)k                   = 0.
                           k     n−1
                k=0

         test_025
               P⌊n/2⌋            √  n+1    √  n+1 
         Goal: k=0 n−k      √1    1+ 5        1− 5
                        
                      k   =   5     2      −    2       .

         test_037
         Goal: nk=0 (−1) k nk m−k                    m−n
               P                                      
                               r    =                r−n .

         test_054
         Premises: 1 ≤ n
               Pm
         Goal: k=0 k+n−1              n+m
                                          
                       n−1   =         n  .

         test_069
         Premises: n ≥ 3
         Goal: n3 = 6 n3 + 6 n2 +                n
                                               
                                                 1

         test_076
               Pn−1             n
         Goal: k=0  (−1)k cos kπ
                              n
                                         n
                                     = 2 n−1 .

         test_088
         Premises: 1 ≤ n
               Pn
         Goal: k=0 2n       2n−1
                                 + 21 2n
                                       
                       k =2           n

         test_100
         Premises: k ≤ n
         Goal: nk · B(k + 1, n − k + 1) = n+1
                                           1
                 



B Lean4Kit

In our automated theorem generator ATG4CI, Lean4Kit plays a key role in data extraction and interaction. During the
experimental evaluation and testing phase, Lean4Kit assists LLMs in theorem proving through interaction with Lean
4. In fact, given any repo in Lean 4, our offline toolkit can convert Lean files into JSON format data, extracting all
state-tactic pairs.

B.1   Data Extraction from Lean Codes

The complete Lean code (including imports) is converted into a JSON-formatted data structure tree (infotree) in the
static extraction process. The conversion function run_all_tactics(self, code, env=None, verbose=True) returns data
in a format that includes the tactic, as well as the before-and-after states of the goals (goalsBefore and goalsAfter), for
example:

                                                                 18
      pp: rw [abelidentity_eq_add]
      name : Lean.Parser.Tactic.rwSeq
      goalsBefore :

        1 n : N
        2 x y : R
        3 hn1 : 1 ≤ n
        4 hx : x 6= 0
        5 hy : y 6= 0
        6 ⊢ abelidentity x y (-1) (-1) n = (1 / x + 1 / y) * (x + y + ↑n) ^ (n - 1)


      goalsAfter :

        1 n : N
        2 x y : R
        3 hn1 : 1 ≤ n
        4 hx : x 6= 0
        5 hy : y 6= 0
        6 ⊢ abelidentity x (y + 1) (-1) (-1 + 1) (n - 1) + abelidentity (x + 1) y (-1 + 1)
              (-1) (n - 1) = (1 / x + 1 / y) * (x + y + ↑n) ^ (n - 1)
        7
        8 case hn
        9 n : N
       10 x y : R
       11 hn1 : 1 ≤ n
       12 hx : x 6= 0
       13 hy : y 6= 0
       14 ⊢ n ≥ 1




B.2    Dynamic Interaction with Lean for Theorem Proving

In the dynamic interaction process, we interact with Lean to perform automated theorem proving. The process mainly
relies on the following functions:

        • run_import(self, code, env=None, verbose=False) : Used to import necessary environments and dependen-
          cies.

        • new_thm(self, code, env=None, verbose=False) : Generates a new theorem based on the provided theorem
          description.

The provided code parameter represents the description of the initial theorem, for example:

  1   theorem idt_84(n: N)(h: m < n): Σ k in range (n + 1), n.choose k (n - k)^m (-1 : R)^k = 0
          := by sorry



This function returns an initial state for subsequent tactic applications:

        • run_tactic(self, tactic, proofState, cmd_type= ’tactic’, verbose=False): Executes a tactic and returns the new
          state after the tactic is applied.

        • run_have_tactic(self, tactic, proofState, cmd_type=’have’, verbose=False) : Executes a “have” tactic.

During the interaction, we can also use function is_correct_and_f inished(self, code, verbose            =
F alse, timeout = 160) to check if the theorem is correct and whether the proof is complete, with the judg-
ment based on the information view (Lean Infoview) on the right side.

                                                            19
        ProcessingCmd :

          1   example (a b c : 2115)(h : a = b): a ^ 2 + c= b ^ 2 + c:= by sorry“”
          2   env: 0

        proofstates : [0],
        goals :

          1   a b c : N      h : a = b ⊢ a ^ 2 + c = b ^ 2 + c

        error: False
        messages: [{’severity’: ’warning’, ’pos’: {’line’: 1,’column’: 0}, ’endPos’: {’line’: 1,’column’: 7}, ’data’:
        “declaration uses ’sorry’”}]
        sorries: [{’proofState’ : 0, ’pos’: {’line’ : 1,’column’ : 58}, ’goals’, ’endPos’ : {’line’: 1,’column’: 63}}]
        is finish: False

The returned Tactic State format includes the following key fields:

           • messages: Contains information during the interaction, such as “no goals,” “declare use sorry,” “unknown
             tactic,” etc.
           • proofstates : An integer list uniquely identifies the current state, where each integer corresponds to a subgoal’s
             state.
           • goals : The current subgoals.
           • error, finishFlag : These parameters are assigned by analyzing messages . The error indicates whether an
             error occurred (True for error), and finishFlag indicates whether the proof is complete (True for completed
             proof).

C        An Illustrative Example for ATG4CI
For the LeanComb benchmark, data augmentation is performed using our theorem generator, ATG4CI. Some theorems
in the dataset are augmented to generate up to 4,000 new instances in one iteration, resulting in a total of 260,466 newly
generated theorems. Among these, 56,747 erroneous theorems are successfully corrected. Below, P        we demonstrate  the
                                                                                                          n
workflow of ATG4CI using a typical example, which corresponds to the mathematical formula k=0 nk Fm+k =
                                                                                                                 
F2n+m :

    1    import Mathlib
    2    import Theorem.valid.idt_179
    3
    4    open Finset Nat
    5
    theorem idt_182 (m n : N) : Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k)
    6
        = Nat.fib (2 * n + m) := by
  7   suffices Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k) = (Nat.fib (2 * n
        + m) : R) by
  8     norm_cast at this
  9   let g := fun k => Nat.fib (m + n + k)
 10   -- $\sum_{k=0}^{n} \binom{n}{k} * fib(m+k) = \sum_{k=0}^{n} \binom{n}{k} * fib(m+n-n+k)$
 11   have h1 : Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k) =
 12     Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + n - n + k) := by
 13     congr! 1 with k hk
 14     simp at hk
 15     congr; omega
 16   rw [h1 ]
 17   -- $\sum_{k=0}^{n} \binom{n}{k} * fib(m+n-n+k) = \sum_{k=0}^{n} \binom{n}{k} *
        fib(m+n-k)$
 18   rw [← Finset.sum_flip]
 19   have h2 : Σ k ∈ range (n + 1), n.choose (n - k) * fib (m + n - n + (n - k)) = Σ k ∈
        range (n + 1), n.choose k * fib (m + n - k) := by


                                                                20
 20      congr! 1 with k hk
 21      simp at hk
 22      rw [choose_symm (by linarith)]
 23      congr; omega
 24    rw [h2 ]
 25    -- $\sum_{k=0}^{n} \binom{n}{k} * \text{fib}(m+n-k) = \sum_{k=0}^{n} \binom{n}{k} *
         \sum_{j=0}^{k} \binom{k}{j} * g(j)*(-1)^k*(-1)^j$
 26
 27    ... ...
 28
 29    have h7 : Σ k ∈ range (n + 1), n.choose k * g k * (-1) ^ k * Σ x ∈ range (n - k + 1), (n
         - k).choose (x) * (-1 : R) ^ (x + k) =
 30      Σ k ∈ range (n + 1), n.choose k * g k * Σ x ∈ range (n - k + 1), (n - k).choose (x) *
         (-1 : R) ^ x := by
 31      congr! 1 with k _
 32      rw [mul_assoc, mul_sum]
 33      congr 1
 34      congr! 1 with j _
 35      rw [mul_comm, pow_add, ← mul_assoc, mul_assoc, ← pow_add, ← two_mul, pow_mul]
 36      ring
 37    rw [h7 , ← Finset.sum_range_add_sum_Ico _ (m := n) (by omega), show 2 * n + m = m + n +
         n by omega]
 38    simp [g]
 39    apply sum_eq_zero
 40    intro k hk
 41    rw [_root_.mul_eq_zero]
 42    right
 43    simp at hk
 44    rw [show (0 : R) = (-1 + 1) ^ (n - k) by simp; rw [zero_pow (by omega)], add_pow]
 45    simp [mul_comm]


Combinatorial Identity 182 encompasses key concepts such as binomial coefficients, Fibonacci numbers, and gen-
erating functions. The proof consists of 77 lines involving 23 distinct tactics, resulting in a proof length and tactic
diversity of 23. Structurally, it forms a 24-layer proof tree, from which 22 distinct P3s can be extracted. The longest
and shortest P3s are highlighted as follows:

  1 theorem P3s_1 (m n : N) : Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k) =
         Nat.fib (2 * n + m) := by
  2   suffices Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k) = (Nat.fib (2 * n
         + m) : R) by
  3     norm_cast at this
  4   ... ...
  5   rw [h1 ]


  1 theorem P3s_22 (m n : N) : Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k) =
          Nat.fib (2 * n + m) := by
  2   suffices Σ k in Finset.range (n + 1), Nat.choose n k * Nat.fib (m + k) = (Nat.fib (2 * n
         + m) : R) by
  3     norm_cast at this
  4   ... ...
  5   rw [show (0 : R) = (-1 + 1) ^ (n - k) by simp; rw [zero_pow (by omega)], add_pow]


Based on these P3s, our RLSCI framework facilitates tactic prediction, enabling the generation of candidate theorems.
We further construct their proofs, followed by deduplication and correctness verification. Below, we present a selection
of intriguing combinatorial identities generated by our theorem generator using the aforementioned examples:

         idt_182_3_12:
                                     n  X k  
                                     X   n     k
                                       (         Fm+n+j (−1)j )(−1)k = F2n+m
                                         k j=0 j
                                     k=0


                                                          21
         idt_182_1_3:
                                                   n  
                                                   X  n
                                                        Fm+n−k = F2n+m
                                                      k
                                                   k=0


         idt_182_0_5:
                                       n Xx         
                                      X      n n−k
                                                        Fm+n+k (−1)x+k = F2n+m
                                      x=0
                                             k   x − k
                                           k=0


         idt_182_0_72
                                                   n  
                                                   X  n
                                                        Fm+n−k = F2n+m
                                                      k
                                                   k=0


         idt_182_6_5
                                   n               n−k
                                                     X n − k 
                                   X  n            k
                                        Fm+n+k (−1)            (−1)x+k = F2n+m
                                      k              x=0
                                                          x
                                   k=0


         idt_182_6_23
                                           n−1
                                           X              n−k
                                                            X n − k 
                                                  n
                                                     Fm+n+k           (−1)j = 0
                                                  k         j=0
                                                                 j
                                           k=0



         idt_182_6_49
                                                     n−k
                                                       X n − k
                                              n
                                                Fm+n+k           (−1)x = 0
                                              k        x=0
                                                            x


         idt_182_2_52
                                                    n−k
                                                    X         
                                                           n−k
                                                                 (−1)x = 0
                                                    x=0
                                                            x


         idt_182_2_45
                                                  n     
                                                 X    n
                                                          Fm+(n−r) = F2n+m
                                                 r=0
                                                     n−r



D     Dataset Statistic
D.1   Proof Steps

We analyzed the proof steps of the LeanComb benchmark and the enhanced dataset on a per-tactic basis and visualized
their distributions in Fig. 3 and 4. Proof steps per tactic serve as an indicator of theorem complexity. Notably, as proof
steps increase, the distribution of theorem steps becomes less concentrated. This phenomenon may result from the
broader range of theorem steps observed in more complex cases. For instance, short proof steps (e.g., between 1 and
10) correspond to a higher number of theorems, which are more densely distributed. In contrast, when the proof steps
exceed 40, the number of theorems decreases significantly, and their distribution becomes sparser.
Specifically, in the LeanComb benchmark, the maximum proof steps reach 166, with 10 theorems having proof steps
exceeding 100 lines. This suggests that the LeanComb benchmark contains a small number of highly complex theo-
rems. In contrast, the maximum number of proof steps in the enhanced dataset is 124, with 800 theorems having proof
steps exceeding 100 lines. This indicates that the enhanced dataset contains a more significant number of long-proof

                                                           22
theorems, reflecting a broader range of difficulty levels. As a result, the enhanced dataset offers greater diversity in
terms of theorem complexity, potentially presenting a more comprehensive challenge for reasoning systems.
Furthermore, these differences suggest that while the LeanComb benchmark includes a few highly complex theorems,
its overall complexity distribution remains relatively concentrated. On the other hand, the enhanced dataset provides
more extensive coverage of longer proofs, which may offer a more thorough evaluation of reasoning tactics regarding
adaptability and generalization capabilities.

                                       80
                                                                                                                               LeanComb
                                                69



                                       60
             Theorem Number




                                                        48   50%


                                       40
                                                             32
                                                                              75%


                                       20            25%
                                                                                          9

                                                                                                                                             3

                                       0
                                                        5         10     15     20         25     30        35     40         45        50       55
                                                                                          Proof Steps

                                       Figure 3: Theorem count distribution across proof steps in LeanComb benchmark.

                                            3
                                                                                                                         LeanComb-Enhanced
                                                             2.564
                                                                        50%               75%
                                       2.5
              Theorem Number (×103 )




                                            2

                                                                  25%
                                       1.5


                                            1

                                                                                      0.488
                                       0.5      0.391


                                                                                                                 0.047             0.008
                                            0
                                                              5          10          15           20        25           30        35            40
                                                                                              Proof Steps

                    Figure 4: Theorem count distribution across proof steps in LeanComb-Enhanced dataset.

Distribution of Theorems in E ∗ by Theorem Type Count. Fig. 5 shows the distribution of deduplicated, correct,
corrected, and new theorems by proof steps in the enhanced dataset E ∗ , including newly added data. Deduplicated
theorems peak at proof step 6 with approximately 50, 000 and decline as steps increase, indicating shorter proofs
dominate. Correct theorems peak slightly earlier at step 5 with 22, 000, showing that many deduplicated theorems
fail correctness checks. Corrected theorems are fewer and decrease rapidly after step 5, suggesting that errors in
longer proofs are harder to address. The new data aligns with these trends, peaking at step 6 with 28, 000 theorems

                                                                                              23
but maintaining a steady count for longer proofs, highlighting improved generation of extended proofs yet persistent
challenges in verification.
These results emphasize two key challenges in automated theorem proving: the gap between deduplicated and correct
theorems, particularly for longer proofs, underscores the need for more robust verification methods, and the rapid de-
cline in corrected theorems highlights the difficulty of resolving errors in complex proofs. Improving proof generation
and error correction tactics—especially for longer proofs—remains a crucial direction, alongside integrating advanced
validation mechanisms to enhance correctness and diversity.


                               50                                                                           New
                                                                                                         Deduplicated
                                                                                                           Correct
      Theorem Number (×103 )




                               40                                                                         Corrected


                               30


                               20


                               10


                               0
                                          5                10             15                20      25                  30
                                                                        Proof Steps

                                                    Figure 5: Theorem distribution by proof Steps



D.2                     Tactic Types Distribution

This section presents a statistical analysis of the distribution of two datasets based on the number of tactic types
involved in the proof of each theorem. A greater number of tactic types employed in the proof of a theorem gener-
ally indicates a higher level of complexity in the proof, as well as reflecting the diversity and depth of the problem.
Moreover, the more tactic types used in the generated theorems, the stronger the model’s ability to explore and apply
different tactics.
Figure 6 illustrates the distribution of theorem counts as a function of the number of tactic types in the enhanced
dataset E ∗ . The theorem count peaks at 25,753 when the number of tactic types reaches six, after which a gradual
decline is observed as the number of tactic types increases. This decline becomes particularly steep when the number
of tactic types exceeds 20. This trend suggests that most theorems can be proven using a relatively small set of tactic
combinations, reflecting the dominance of simpler theorems in combinatorial mathematics. However, the sparsity of
theorems requiring many tactic types points to an underrepresentation of complex theorems in the dataset, presenting
a significant challenge for automated theorem-proving systems.
Figure 7 presents the distribution of theorem counts across different numbers of tactic types in the LeanComb bench-
mark L∗ . The chart shows that the majority of theorems are concentrated in the lower ranges of tactic types, with a
peak occurring at tactic type 6. This suggests that simpler tactics are sufficient to prove most theorems, highlighting
the prevalence of less complex theorem structures. However, as the number of tactic types increases, the theorem
counts decrease significantly, indicating that highly complex theorems are relatively rare. This distribution implies
that while simpler tactics are effective for many theorems, more sophisticated tactics are necessary for handling sparse
but complex cases.
The distribution of tactic types is predominantly concentrated within the first ten types, with the highest theorem count
occurring at six tactic types. Beyond this, the theorem count gradually decreases; however, hundreds to thousands
of theorems remain even for tactic types ranging from 20 to 40. This demonstrates that the dataset contains many
complex theorems, offering a significant challenge and utility for evaluating automated theorem-proving systems.

                                                                         24
                                             25.753
                           25
   Theorem Number (×103)


                           20
                                                           16.258

                           15


                           10
                                5.885

                           5                                                                              3.440
                                                                                                                                                                                                          2.162
                                                                                                                                                      1.153

                           0
                                                             10                                           20                 30                                                                       40                                   50
                                                                                                          Numbers of Tactic Types

                                               Figure 6: Theorem Distribution by Tactic Types of Enhanced Dataset E ∗


E More Evaluation Results on LeanComb Benchmark
E.1                    Evaluation on LeanComb with Varying Time Limits and Candidate Tactic Numbers
The results in Table 5 demonstrate the performance of several models on the LeanComb test set under the constraints of
a 300-second time limit and a maximum of 8 candidate tactics. The success rates across different models consistently
show improvements when fine-tuned on LeanComb and further enhanced with LeanComb-Enhanced.

                           50
                                   45



                           40
                                        36
          Theorem Number




                                         31
                                30
                           30
                                                            24
                                               23
                                                      22

                           20                    17    17                                  17

                                                               13
                                                                 11                                                           11
                                                                          10                10       10
                           10                                         8                                       8
                                                                                                                  7       7                     7 7                          7
                                                                                       6                                           6 6 6                                                                  6
                                                                               5                                                                                   5                      5                                            5
                                                                                                 4        4                                                4                      4               4
                                                                                                                      3                    3           3       3       3 3                                             3         3 3
                                                                                                                                                                                      2               2
                                                                                   1                                                                                                          1               1 1 1        1 1
                            0
                                                               10                                    20                                    30                                40                                   50
                                                                                                      Numbers of Tactic Types
                                         Figure 7: Theorem Distribution by Tactic Types of LeanComb Benchmark L∗

Gemma2-9B exhibits a modest increase, with a success rate of 13% in the base setting, rising to 14% with LeanComb
and further improving to 15% with LeanComb-Enhanced. Mathstral-3-8B demonstrates the most significant gains,
increasing from 6% in the base set to 11% with LeanComb, and reaching 21% with LeanComb-Enhanced, reflecting
a substantial +15% improvement over the base model. Llama3-8B follows a similar trend, improving from 5% to
10% with LeanComb, and to 18% with LeanComb-Enhanced. Mistral-7B, while starting with a slightly higher base

                                                                                                                          25
performance of 8%, shows a smaller increase to 9% with LeanComb, but a more substantial jump to 20% with the
enhanced dataset.
Under the same conditions, the model’s proof success rate is generally lower than the proof success rate with a 600-
second time limit and up to 16 candidate tactics, as shown in Table 4, with a decrease range of 1% to 8%.

             Table 5: Success rates on the LeanComb test set with 300 seconds and 8 candidate tactics.

                     Model                       Base          LeanComb       LeanComb-Enh.

                     Gemma2 - 9B                 13%             14%                15%
                     Mathstral3 - 8B              6%             11%                21%
                     Llama3 - 8B                  5%             10%                18%
                     Mistral - 7B                 8%             9%                 20%

These results indicate that all models benefit from the additional training data, with the LeanComb-Enhanced dataset
yielding the highest performance gains across the board. Notably, Mathstral3-8B and Llama3-8B exhibit the most pro-
nounced improvements, suggesting that models with stronger baseline capabilities can leverage the enriched dataset
more effectively. This underscores the value of LeanComb-Enhanced in advancing automated theorem proving, par-
ticularly for combinatorial identities.

E.2   Automated Proof Results of Our Models

In this section, we analyze the proof process of the models. The table summarizes the average proof lengths across all
models, revealing that the proof lengths range from 2.7 to 3.9. Notably, for both the Mathstral and Llama models, the
enhanced versions consistently exhibit shorter proof lengths compared to their comb counterparts. This suggests that
the models have learned to adopt more efficient and simpler tactics for generating proofs through extensive training on
large datasets. For instance, as shown in the example for test_087, Mathstral comb requires 11 steps to complete the
proof, whereas Llama3 enhanced accomplishes the proof in just four steps.

  1 theorem test_087_Mathstral_comb {n:N} (hn : 0 < n):
  2   (ascPochhammer R n).eval x = (x - 1 + n) * (ascPochhammer R (n-1)).eval x := by
  3   unfold ascPochhammer
  4   cases n
  5   all_goals simp only [Polynomial.eval_one, CharP.cast_eq_zero, add_zero, mul_one]
  6   cases hn
  7   rename_i n
  8   cases n
  9   all_goals simp
 10   rename_i n
 11   rw [ascPochhammer_succ_right]
 12   simp only [Polynomial.eval_mul, Polynomial.eval_add, Polynomial.eval_X,
        Polynomial.eval_natCast]
 13   ring
 14
 15 theorem test_087_llama3_enhanced {n:N} (hn : 0 < n):
 16   (ascPochhammer R n).eval x = (x - 1 + n) * (ascPochhammer R (n-1)).eval x := by
 17   have h1 : n = n - 1 + 1 := by
 18     rw [tsub_add_cancel_of_le]
 19     exact hn
 20   rw [h1, ascPochhammer_succ_right]
 21   simp only [Polynomial.eval_mul, Polynomial.eval_add, Polynomial.eval_X,
        Polynomial.eval_natCast,
 22     cast_add, cast_one, sub_add_add_cancel, add_tsub_cancel_right]
 23   rw [← mul_comm]


Furthermore, we observed that after training on the enhanced dataset, models tend to rely heavily on the theorems from
the LeanComb training set when generating proofs. However, despite this increased dependence on known theorems,
the models occasionally introduce invalid or redundant steps in the proof process. For instance, in the following

                                                          26
example, the step “lemma this” is an unnecessary operation; the proof remains valid even if this step is removed.
Below, we present several interesting examples of automatically generated proofs:

  1 theorem test_062 (m n:N)(hn:n≥2)(hm:m≥2) :
  2 Nat.choose (m+n-2) (m-1) = Nat.choose (m+n-3) (m-2)+Nat.choose (m+n-3) (m-1) := by
  3     have h1 : 2 ≤ m := by linarith
  4     have h2 : 2 ≤ n := by linarith
  5     have h3 : m - 1 + 1 = m := by omega
  6     have h4 : m - 2 + 2 = m := by
  7       rw [Nat.sub_add_cancel]
  8       exact h1
  9     have h5 : m + n - 2 = m + n - 3 + 1 := by omega
 10     rw [h5]
 11     rw [← h3, ← h4]
 12     simp only [Nat.add_one_sub_one, add_tsub_cancel_right, reduceSubDiff]
 13     rw [Nat.choose_succ_succ]


  1 theorem test_077 (n:N) :
  2 2 ^ n = Σ k ∈ Finset.range (n + 1),(-1 : R) ^ k * Nat.choose n k * 3 ^ (n - k) := by
  3   let f : R → R := fun x => x ^ n
  4   have h := add_pow (-1 : R) 3 n
  5   have h1 : (-1 : R) + 3 = 2 := by norm_num
  6   rw [h1] at h
  7   have h2 : Σ k in Finset.range (n + 1), (-1 : R) ^ k * 3 ^ (n - k) * (n.choose k) = Σ k
        in Finset.range (n + 1), (-1 : R) ^ k * (n.choose k) * 3 ^ (n - k) := by
  8    refine’ sum_congr rfl fun k _ => _
  9    ring
 10   rw [h2] at h
 11   assumption


  1 theorem test_031 (n : N) :
  2   Σ k in Finset.range (n / 2 + 1), (-1 : R) ^ k * Nat.choose (n - k ) k =(2 / Real.sqrt
        3) * Real.sin ((n + 1) * Real.pi / 3) := by
  3   obtain h1 := Idt_32 n (-1 : R)
  4   have h2 :
  5     Σ k in range (n / 2 + 1), ((n - k).choose k * (-1 : R) ^ k) = Σ k in range (n / 2 +
        1), ((-1) : R) ^ k * choose (n - k) k := by
  6       refine’ sum_congr rfl fun k _ => _
  7       rw [mul_comm]
  8   rw [h2] at h1
  9   rw [h1]
 10   have : 1 + 4 * (-1 : R) = -3 := by norm_num
 11   rw [this]
 12   exact_mod_cast complex_sqrt_neg n



F Experiments Details
F.1 Theorem Correction Details


During the theorem generation process, we classify theorems and verify the correctness of candidate theorems. Incor-
rect theorems are grouped separately, and different correction methods are applied based on their types.
The standard MCTS with our fine-tuned Llama 3.1 corrects these theorems. We set the number of candidate tactics (i.e.,
visit counts) per node to 16 and the number of simulations per node to 100. It generates full-proof search trees through
selection, expansion, and backpropagation, and complete-proof steps are engendered accordingly. The selection phase
considers the average reward and exploration of nodes, using the UCB1 algorithm to select the optimal node [3]:
                                                                  r
                                                   Wi                 lnNp
                                           U CB1 =    +C×                  .                                        (3)
                                                   Ni                  Ni

                                                          27
 Error Types                          Error Example                                     Correction Example

                                                                                    CorrectedT heorem1 (n : N)
                                 ErrorExample1 (n : N)
                                                                                 (goal : the goal of sum_mul_congr) :
                            (goal : the goal of sum_mul_congr) :         Pn                    Pn      k
                                                                                                             Pn       k
                      Pn                   Pn      k+1 Pn      k          k=0 kC2n+1 = 2n        k=0 C2n + 1   k=0 C2n := by
 Incomplete Proofs      k=0 kC2n+1 = 2n       k=0 C2n    k=0 C2n := by
                                                                                      rw[range_eq_Ico] at goal
                                 rw[range_eq_Ico] at goal
                                                                                        rw[add_mul] at goal
                                        assumption
                                                                                             assumption

                           ErrorExample2 (m : N)(hm : 0 < m) :            Corrected_T heorem2 (m : N)(hm : 0 < m) :
 Type Errors
                           2 + −1/(m + 1) = (2m + 1)/(m + 1)                  2 + (−1 : R)/(m + 1) = (2m + 1)/(m + 1)

                                 ErrorExample3 (n : N) :
                                                                                    CorrectedT heorem3 (n : N) :
                                 2n + 1 − n = n + 1 := by
                                                                                      2n + 1 − n = n + 1 := by
                                       rw[two_mul]
                                                                                           rw[two_mul]
 Redundant Steps                      rw[add_assoc]
                                                                                           rw[add_assoc]
                                      rw[add_comm]
                                                                                          rw[add_comm]
                                           simp
                                                                                                simp
                                       rw[two_mul]

                                   Table 6: The Error Types and Correction Process


Detailed descriptions of the different types of errors and their respective correction methods are provided in the table
6.

Example1: Incomplete Proofs


  1 theorem congr_Ico_succ__2__73(n : N) :
  2    Σ k in Ico 1 (n + 1), k Nat.choose (n - 1) (k - 1) = Σ l in
  3    Ico 0 n, (l + 1) Nat.choose (n - 1) l := by
  4   rw [sum_Ico_eq_sum_range]
  5   simp
  6   refine’ sum_congr rfl fun y _ => _
  7   rw [add_mul]
  8   rW [choose_eq_zero_of_lt]
  9   rw [add_comm]

                                   Listing 2: Type Error: unsolved goal n − 1 < y.


After Corrected:

  1 theorem congr_Ico_succ_2_73 (n : N) :
  2    Σ k in Ico 1 (n + 1), k Nat.choose (n - 1) (k - 1) = Σ l
  3    in Ico 0 n, (l + 1) Nat.choose (n - 1) l := by
  4   rw[sum_Ico_eq_sum_range]
  5   simp
  6   refine’ sum_congr rfl fun x _ => _
  7   simp
  8   rw [add_comm]
  9   exact Or.inl rfl



Example2: Type Errors

                                                            28
  1 theorem sum_mul_add_distrib__0__36(n : N)(h : Σ k in range (n + 1), (k + 1) Nat.choose n
        k = Σ k in range (n + 1), (k*Nat.choose n k + 1*Nat.choose n k)) :
  2  (1 + y) Nat.choose n y = y * Nat.choose n y + Nat.choose n y := by
  3   refine’ sum_congr rfl fun y _ => _
  4   simp [mul_assoc] at h
  5   rw [add_comm] at h
  6   assumption

                          Listing 3: Type Error : metavariables AddCommMonoid ?m.90801.


After Corrected:

  1 theorem sum_mul_add_distrib__0__36(n : N)(h: Σ k in range (n + 1), (k + 1) Nat.choose n
        k = Σ k in range (n + 1), (k Nat.choose n k + 1*Nat.choose n k)) :
  2    (1 + y)*Nat.choose n y = y*Nat.choose n y + Nat.choose n y := by
  3   rw [add_mul]
  4   rw [one_mul]
  5   rw [add_comm]




F.2 Details and Hyperparameters

      Prompt Example:

      You are using Lean 4 for theorem proving. You are proving a theorem in Lean 4. Based on the current state of
      the theorem, provide the most reasonable proof tactic. Ensure your tactic is syntactically correct according to
      Lean 4’s tactic syntax and effectively progresses the proof.

      [Current State]:
      n:N                       P
      ⊢ N at.choose (2 ∗ n) n ≤   x ∈ range n, N at.choose (2 ∗ n) x + N at.choose (2 ∗ n) n

      [Output Tactic]:
               rw [sum_range_add], −0.30987493962877327
               rw [sum_range_add_choose] , −0.3457271686162461
               rw [sum_range_add_choose_add] , −0.3690287694334984
               rw [sum_range_add_choose_eq] , −0.44889247231185436
               rw [sum_range_add_sum_range] , −0.4555072601741323
               rw [sum_range_add] , −0.46009636194341713
               rw [sum_range_add_choose] , −0.4931001846085895
               rw [← choose_range_choose] , −0.5118355770239511
               rw [← add_assoc] , −0.5198788805936602
               rw [sum_range_choose_add] , −0.5362029924396087
               rw [sum_range_add_sum] , −0.5367179045623
               rw [sum_range_choose] , −0.5484384259002076
               rw [choose_range_choose] , −0.590293240112563
               rw [sum_range_succ] , −0.6008733134302828
               rw [two_mul] , −0.6277757014509656
               simp , −1.4107935726642609



                                                            29
In this experiment, we employed Llama-3.1-8B-Instruct as the candidate tactic model within our generator ATG4CI.
This model is a transformer-based, autoregressive language model optimized for high performance. To enhance its
alignment with human preferences in terms of utility and safety, we fine-tuned the model using Supervised Fine-
Tuning (SFT) [97] . All training tasks were conducted on a cluster of six NVIDIA L40 GPUs (48GB each). For SFT,
we employed Low-Rank Adaptation (LoRA) [36], leveraging bfloat16 mixed precision and DeepSpeed ZeRO Stage
0 [40] for memory optimization. LoRA was applied to all layers of the model. We used the AdamW optimizer [20]
with a batch size of 4. The learning rate was linearly warmed up from 0 to 5.0 × 10−5 over the initial 5% of training
steps, followed by a cosine decay schedule for subsequent updates.
We adopted a best-first search (BFS) [69] tactic for evaluation. At each search step, the model generated 8 or 16 tactic
candidates, deduplicated and ranked according to their log-likelihoods. Each candidate was subsequently verified
using Lean 4, determining whether it should have been discarded or expanded into new proof states. The ranking of
states is based on the cumulative log-likelihood of the tactics leading to the current state. The model is prompted using
a structured (state, tactic) format, enabling the generation of tactics conditioned on the current proof state.




                                                           30
