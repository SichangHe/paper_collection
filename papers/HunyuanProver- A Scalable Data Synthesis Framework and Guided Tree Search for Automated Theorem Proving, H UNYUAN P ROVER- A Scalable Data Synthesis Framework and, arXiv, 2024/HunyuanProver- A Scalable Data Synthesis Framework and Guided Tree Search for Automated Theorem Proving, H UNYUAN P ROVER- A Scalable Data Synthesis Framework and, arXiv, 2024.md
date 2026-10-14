                                         Technical Report




                                         H UNYUAN P ROVER: A Scalable Data Synthesis Framework and
                                         Guided Tree Search for Automated Theorem Proving

                                             Yang Li∗, Dong Du*, Linfeng Song*, Chen Li*, Weikang Wang, Tao Yang and Haitao Mi
                                             Tencent Hunyuan Teams
                                             {youngyli,dongdu,vegetali,daxianwang,rigorosyang}@tencent.com
                                             {lfsong,haitaomi}@global.tencent.com



                                                                                         Abstract
arXiv:2412.20735v3 [cs.AI] 21 Mar 2025




                                                       We introduce H UNYUAN P ROVER, an language model finetuned from the H UN -
                                                       YUAN 7B for interactive automatic theorem proving with LEAN4. To alleviate
                                                       the data sparsity issue, we design a scalable framework to iterative synthesize
                                                       data with low cost. Besides, guided tree search algorithms are designed to enable
                                                       effective “system 2 thinking“ of the prover. H UNYUAN P ROVER achieves state-
                                                       of-the-art (SOTA) performances on major benchmarks. Specifically, it achieves
                                                       a pass of 68.4% on the miniF2F-test compared to 65.9%, the current SOTA re-
                                                       sults. It proves 4 IMO statements (IMO 1960 P 2, IMO 1962 P 2, IMO 1964 P 2
                                                       and IMO 1983 P 6) in miniF2F-test.


                                         1        Introduction

                                         Recent advancements in large language models (LLMs) have profoundly impacted mathematical
                                         reasoning and theorem proving in artificial intelligence. Despite notable progress in natural lan-
                                         guage domains, language models still encounter substantial challenges in formal theorem proving
                                         (e.g., using LEAN (Moura & Ullrich, 2021) or Isabelle (PAULSON, 1994)) probably due to the
                                         massive search space of Olympiad-level theorem proving and limited data in such scenario. As
                                         the results, even the most advanced models like GPT-4o Hurst et al. (2024) struggle with complex
                                         formal-statement proving (Xin et al., 2024a). A formal theorem-proving model should be capable of
                                         understanding both the syntax and semantics of a formal system, enabling it to generate valid next
                                         steps within the system. More critically, it must integrate this capability with its abstract mathemat-
                                         ical reasoning skills to perform effective and efficient deductions.
                                         We propose H UNYUAN P ROVER, an LLM-based automatic theorem prover obtained by a pragmatic
                                         framework for addressing the aforementioned challenges. The framework takes two core modules:
                                         a scalable prover-data generator and guided tree-search algorithms. The prover-data generator only
                                         takes open-source data for theorem proving to train the initial autoformalizer and prover. The aut-
                                         oformalizer then converts a large amount of existing math questions into the format of the target
                                         prover (e.g., LEAN4). The prover is lastly iteratively improved on such data where new proof data
                                         is generated at each iteration to train the prover. At testing time, tree-search algorithms and multi-
                                         ple critic models are designed to perform “slow thinking” that is empirically essential for solving
                                         complex theorem-proving tasks.
                                         Evaluations show that H UNYUAN P ROVER yields an accuracy of 68.4% on the miniF2F benchmark.
                                         In addition, we also observe several key findings: 1) using explicitly trained critic for tree-search
                                         guidance is helpful; 2) the scale of finetuning data for theorem proving is critical, thus designing
                                         efficient data scaling framework is important; 3) data curation and selection is important as well
                                         when there is sufficient amount of training data.
                                         Our key contributions includes:

                                         • We introduce a scalable pipeline that utilizes open-source data for theorem proving and massive
                                           math problems in natural language to generate a large number of new training data for automatic
                                           theorem proving.
                                              ∗
                                                  Equal contribution


                                                                                              1
Technical Report




• We develop several critic models and evaluate their effectiveness using two widely adopted search
  algorithms: best-first search and Monte Carlo tree search.

2     Scalable Data Generation for Prover Improving
One major bottleneck for automated theorem proving is the lack of training data. For example, as
one of the largest open-source LEAN4 datasets, mathlib4 (Moura & Ullrich, 2021) only contains
around 50k theorems(with tactics) for training. This is far from sufficient to train a stronger prover
given the difficulty of automatic theorem proving. On the other hand, massive high-quality math
problems in natural language have been released in recent years (Yu et al., 2024; Luo et al., 2023).
Our efforts fall into two critical aspects to scale the training data for automatic theorem proving: aut-
oformalization (Section 2.1) that maps a natural language problem (Section 2.2) into LEAN format
statement, and tactic generation for iterative theorem proving.

2.1   Autoformalization Data Generation

For autoformalization, we start with 130k high-quality natural language to LEAN statement pairs,
which includes 50k from lean workbook (Ying et al., 2024) and 80k from MMA (Jiang et al., 2024).
We first translate the natural language part of the 130k data into Chinese to double the dataset size,
and with such data we train a autoformalization model, it can translate both English and Chinese
problems to lean4 format statement.
In the next step, 30 million internal math problems in natural language are converted into formal
statement by the autoformalization model. For each natural language problem, we sample 8 outputs
with different temperatures.We obtain a dataset Dq of 20 million LEAN statements after filtering
out these do not conform with LEAN grammar or do not satisfy other rules adopted by previous
practices (Ying et al., 2024).
In addition to using internal data, we also utilized open-source natural language mathematical data
NuminaMath CoT(LI et al., 2024).

2.2   Prover Improving via Iterative Tactic-Level Proving Data Generation

We design a iterative framework that takes a LEAN engine Γ and statement dataset Dq from aut-
oformalization to generate new tactic data for prover improving. Specifically, in iteration t, we
leverage best-first search (Section 3.1) algorithm with the prover from the previous iteration πt−1
on all unsolved statements so far in D. We collect the proving trajectories (e.g., τ ) for newly solved
statements (e.g., q) if there is any:
                   Dt = {(q, τ ) | q ∈ Dq − Dt−1 , τ ∼ B FS(q), τ ̸= null} ∪ Dt−1                    (1)
Then the prover is updated using rejection finetuning (RFT) with the proving trajectories in Dt after
filtering out easy statements solved in early iterations. The initial prover π0 is trained on public data
including mathlib4. After more than 10 rounds of iteration, more than 20 million tactic-level data is
obtained.

Enhancing Diversity As indicated by previous work (Xin et al., 2024c), prover diversity is im-
portant due to the massive search space of theorem proving. We further develop two methods to
enhance the prover diversity within the iterative data-generation framework. For the first method,
we design rules to convert the last state of an unfinished proving trajectory into a new statement.
In this way, more diverse proving data is obtained for prover training. For the second method, we
collect data from proving more challenging statements, including those Olympiad-level algebraic
inequalities Wei et al. (2024) and lean workbook Ying et al. (2024).

3     Guided Tree Search
As described in Section 2, our task involves iterative interaction with LEAN as the environment,
where for each iteration the policy predicts a new tactic given from a state in the proving process.


                                                   2
Technical Report




                 Selection          Expansion                     Simulation             Backprop


             0.7         0.3


      -0.3 0.1     0.9




Figure 1: Comparing best-first search (BFS) with Monte-Carlo tree search (MCTS). BFS only takes
Selection and Expansion in one iteration, while MCTS takes all four steps. The numbers represent
critic-assigned scores.


We abstract this process as tree search where a state si in the proving process corresponds to a tree
node ni with the input statement q being the root n0 . An edge that points from ni to nj represents
applying a tactic on node (state) ni to yield node (state) nj . To handle this problem, we design two
major tree search algorithms as described in Section 3.1. We also design several critics, as shown in
Section 3.2, to guide these algorithms.

3.1      Tree Search Algorithms

We explore two search algorithms: best-first search (BFS) and Monte-Carlo tree search (MCTS) for
the tactic-level iterative statement proving process.

Best-First Search We first study BFS due to its simplicity and effectiveness. As demoed in the
left part of Figure 1, BFS can be viewed as an iterative process of selection and expansion. The
search process continues until either the statement q is successfully proved or the maximal number
of iteration T is reached.
In the selection step, the node n̂ with the highest critic score is selected (without return) from the set
of active nodes N :
                                        n̂ = arg max C RITIC(n)                                        (2)
                                                n∈N

                                                                                                 ˆ of
where C RITIC represents the critic function. In the expansion step, the policy π samples a set (C)
K candidate tactics under n̂:
                                Cˆ = {ĉi |ĉi ∼ π(q, n̂), i ∈ [0, . . . , K]}                        (3)

Each tactic in Cˆ is then executed against the LEAN engine to yield a new tree node if the tactic is
valid under state n̂. After removing those that are identical to previously explored tree nodes, the
remaining are merged into the active node set N . We check two nodes are identical simply by string
matching.

ηMCTS Thought being simple and effective in general, BFS has several limitations on handling
complex search problems. One limitation is that each node is only visited once with a fixed amount
of expansion budget. Besides, BFS only takes the critic score as guidance, thus it can suffer from
any bias and misjudgment inherent in the critic model.
We additionally adapt ηMCTS (Tian et al., 2024) to handle such limitations. As shown in Fig-
ure 1, the original ηMCTS algorithm takes 4 steps of selection, expansion, simulation and back-
propagation in each iteration. Here we remove the step of simulation, leaving it for future work. As
another major, our ηMCTS follows the setting of BFS to sample K candidate tactics (instead of one
in Tian et al. (2024)) at a time given a state. Different from BFS, our ηMCTS algorithm can sample
a tree node multiple times, and the expansion budget for each node is updated by its importance
score that can be dynamically changed throughout the search process. Following Tian et al. (2024),


                                                      3
Technical Report




the importance score for any node n is defined as the maximal value difference between it and its
descendant:
                          I(n) = max |C RITIC(n̂) − C RITIC(n)|,                             (4)
                                       n̂∈S UCC(n)

where S UCC(n) represents all succeeding nodes of node n. Then, the adapted expansion budget for
node n is defined as:
                           E(n) = max(Bmin , min(Bmax , ⌊αI(n)⌋ + 1))                                    (5)
where α, Bmin , Bmax are the corresponding factor, lower bound and upper bound, respectively.
As another major difference from BFS, ηMCTS selects nodes based on Upper Confidence Bound
(UCB) defined as:
                                               s
                                                        C NT(P RNT(n))
                    U CB(n) = C RITIC(n) + α × 2 × ln                                  (6)
                                                            C NT(n)

where P RNT(n) denotes the parent node of n in the search tree, and C NT(n) represents the number
of visiting times so far for n. Generally, UCB can be viewed as a balance between exploration and
exploitation, where the first term of the equation prefers nodes with high critic score (exploitation)
while the second term prefers under-explored nodes (exploration).

3.2   Critics for Search Guidance

Critic modeling is a central component in tree search as it provides the guidance. We design three
types of critic models to guide the search process.

Policy Confidence (PC) We first leverage policy confidence as guidance for a cold start of guided
search due to limited tree-search data for training critic models at the beginning. Particularly, for
tactic c under state n in the proving process of statement q, we define its policy confidence f π (c) as
token-level average log probability:
                                                     |c|
                                               1 X
                                  f π (c) =           log pπ (cj |q, n, c<j )                            (7)
                                              |c| j=1

where |c| is the number of tokens in c.

Process Reward Model (PRM) The process reward model (PRM), denoted as vϕπ (q, n) (parame-
terized by ϕ), represents the possibility of tree node n for proving statement q when starting from it
and following policy π thereafter.
To train a parameterized PRM vϕπ using statement set D = [q 1 , . . . ], we first generate a search
tree for each statement q k by following policy π under the guidance of the critic from the previous
iteration. Next, for each node nki in the search tree, a score is assigned to reflect its quality. Ideally,
human experts are hired for rating the node quality, but the cost is dramatic. Following Wang et al.
(2024c), we simply assign a score of +1 or -1 to each node by indicating whether it can reach the final
state that indicates successful proving of q k . This approximation has been proven effective in the
experiments of Wang et al. (2024c). As the results, we obtain a PRM dataset Dv = [(q k , nki , lik ), . . . ]
with lik indicating the score for node nki .
With dataset Dv , the PRM is then optimized by minimizing the mean squared error for each node:
                               vϕπ = −E(qk ,nki ,lik )∼Dv (vϕπ (q k , nki ) − lik )2                     (8)
Similar to Wang et al. (2024c), vϕπ is a LLM with an MLP layer on top to output a scalar for each
token. We use the scalar prediction at the last token of each state as the value.

Distance Critic (DC) PRM only captures the possibility of proving the input statement q starting
from a tree node n, therefore we further design a distance-based critic model to predict the estimated
remaining number of steps to prove q from n.


                                                           4
Technical Report




One naive solution can be training the critic model to directly predict the distance, while it is likely
to suffer from data sparsity issue. When the state is very complex, it is very difficult to predict an
accurate number of the remaining steps. We train the critic model to predict not only the exact num-
ber of remaining steps but also the range in which this number falls, represented using a balanced
binary tree structure. This approach helps mitigate the data sparsity issue by enabling the model to
make predictions in a hierarchical, coarse-to-fine manner. Specifically, the critic model is trained to
identify a path on the balanced binary tree, progressively narrowing down to the exact number of
remaining steps.
Figure 2 illustrates a 4-level binary tree capable of representing numbers from 1 to 8. Each level
of the tree corresponds to a progressively finer division of the numerical range. For instance, at the
second level, there are two nodes: 1/2 and 2/2, which split the entire range into a left half [1, 4]
and a right half [5, 8]. If a number falls within the range [1, 4], the corresponding path through the
tree includes the node 1/2. Empirically, nodes at higher levels of the tree are easier to predict than
leaf nodes. This hierarchical structure helps reduce prediction errors during tree search by enabling
the model to first make broader, more reliable predictions before refining them. For example, two
numbers that are close in distance share a common prefix in their paths on the tree. Therefore,
representing numbers using their paths on the tree effectively captures the distance relationship
between them, enabling the model to predict this information more directly and intuitively.

                                                                root

                                            1/2                                           2/2

                                1/4                     2/4                   3/4                     4/4

                          1/8         2/8         3/8         4/8       5/8         6/8         7/8         8/8

Figure 2: Balanced binary tree structure for coarse-to-fine number representation. When the level of
tree is 4, the max number can be represented is 8. The path of number 6 is root → 2/2 → 3/4 →
6/8. The tuple associated with the path is (2, 3, 6).

In practice, we use an 8-level binary tree to represent numbers up to 64, where each node on
the tree is represented by a separate special token. For instance, 1/2 is represented by the token
<|num-1-of-2|>, and 5/8 is represented by <|num-5-of-8|>. When constructing training
data, if the number of remaining steps exceeds 64, we set it to 64.
A path on the binary tree is essentially a tuple of numbers, such as (2,3,6) shown in Figure 2. During
the tree-search stage with the distance critic, we compare two states by directly comparing their
corresponding tuples. This approach inherently evaluates states in a coarse-to-fine manner.


4     Experiments

4.1   Setup

Benchmarks We evaluate theorem-proving performance on the following benchmarks to pinpoint
the effectiveness of each proposed module:

• MiniF2F (Zheng et al., 2022) examines LLM’s automatic formal problem-solving skills targeted
  at high-school-level exercises and competitions, such as AMC, AIME, and IMO, with a particular
  focus on algebra and number theory. The benchmark comprises 244 validation problems and 244
  test problems.

Inference We use the LEAN engine from LeanDojo (Yang et al., 2024) as the engine to conduct
both tactic data generation and benchmark evaluation. Whole and per-step timeout for tactic exe-
cuting in LEAN are set to 3600 seconds and 60 seconds, respectively. At most 800 search steps
are conducted for both BFS and MCTS. For each search step, K = 8 tactics are sampled from the


                                                                    5
Technical Report




      System                                    Model Size     Sample Budget      MiniF2F-test
      Whole-Proof Generation Methods
      DeepSeek-Prover-V1.5-RL+MCTS                    7B          16 × 6400           60.2%
      DeepSeek-Prover-V1.5-RL+RMaxTS                  7B          32 × 6400           63.5%
      Interactive Step Proving Methods
      Lean-STaR+BFS+CG                                7B         64 × 1 × 50          46.3%
      InternLM2.5-StepProver+BFS                      7B       256 × 32 × 600         59.4%
      InternLM2.5-StepProver+BFS+CG                   7B       256 × 32 × 600         65.9%
      HunyuanProver v16+BFS                           7B        600 × 8 × 400         64.8%
      HunyuanProver v16+BFS+DC                        7B        600 × 8 × 400         68.4%

Table 1: Main comparison regarding accuracy and sampling cost with other systems on MiniF2F-
test. CG indicates critic-guided search, while DC represents taking our proposed distance critic as
guidance. For BFS methods, the cost is represented as #Pass × #Beam × #Iteration, while for MCTS,
the cost is defined as #Pass × #Iteration.


given LEAN state under temperatures 0.7, 0.8, 1.0 and 1.1, where two tactic are sampled under each
temperature. These temperature values are empirically decided. The prompts for policy and distance
critic are listed in Appendix B and C.

Finetuning Hyperparameters Our prover is obtained by fine-tuning a H UNYUAN 7B model on
our self-generated tactic data. During fine-tuning, at most 4 epochs are conducted and checkpoint
is selected based on miniF2F valid set. The maximum sequence length, learning rate, minimal
learning rate and batch size are set to 4096, 2 × 10−5 , 1 × 10−6 and 256, respectively. Cosine
learning schedule is used.

Comparing Systems We compare HunyuanProver with former state-of-the-art systems. Among
them, Lean-STaR (Lin et al., 2024) and InternLM2.5-StepProver (Wu et al., 2024) are interactive
step-level proving methods, while on the other hand, DeepSeek-Prover-V1.5 (Xin et al., 2024b) is a
whole-proof generation method.

4.2   Results and Analysis

Table 1 shows the comparison between HunyuanProver with other existing state-of-the-art systems.
Among these systems, our HunyuanProver with distance-tritic as guidance shows the best accu-
racy on miniF2F, advancing the previous SOTA system (InternLM2.5-StepProver+BFS+CG) by
2.5% points using less search budget. Though InternLM2.5-StepProver+BFS+CG is slightly better
than DeepSeek-Prover-V1.5-RL+MCTS, the later does not take any critic for guidance. We believe
MCTS can be more beneficial to the task of automatic theorem proving, and this potential has not
been fully revealed. In addition, we can also probe the importance of critic guidance by incorporat-
ing DCG on HunyuanProver, which shows 3.6%-point gain. We list multiple statements solved by
HunyuanProver in Appendix A.

Effectiveness of Iterative Tactic Data Generation Figure 3 visualizes the changes regarding
miniF2F-test accuracy and the amount of training data during the prover improving process based on
iterative tactic data generation. We initially see performance boosts in early iterations until version
v8, and then minor improvements are observed by further increase the number of training tokens
from roughly 2.75B (v8) to 4.25B (v12). After v12, we remove some data generated from early
iterations(before v8), Most of the removed training data are relatively easy statements.We can see
the performance boost is achieved by removing these easy data. This highlights the importance of
data selection in the iterative improving process.

Effectiveness of Different Critics and Tree Search Methods As shown in Table 2, we conduct an
ablation study on different search and critic combinations under three different versions of Hunyuan-
Prover. Due to limitation on time and computation resources, MCTS is executed together with PRM.
The MCTS-with-PRM combination is consistently better than the BFS with policy confidence. Due


                                                  6
Technical Report




     66                                                                                    4.5

     64                                                                                    4

     62                                                                                    3.5
                                                                                           3
     60
                                                                                           2.5
     58
                                                                                           2
     56
                                                                                           1.5
     54                                                                                    1
     52                                                                                    0.5
     50                                                                                    0
              v2        v5       v7        v8        v10         v12       v14     v16
                              miniF2F-test acc(%)          #Tokens (Billion)

Figure 3: The trend regarding miniF2F-test accuracy and the number of finetuning tokens during the
iterative tactic data generation process for prover improving, where “v” represents “version”. The
version number is approximately equivalent to the number of iterations. After v12, we remove some
easy training data. BFS with policy confidence as the critic is adopted.

                             Model + Search                MiniF2F-test
                             H UNYUAN P ROVER V 12
                              + (BFS, PC)                     61.07%
                              + (MCTS, PRM)                   62.29%
                             H UNYUAN P ROVER V 14
                              + (BFS, PC)                     62.70%
                              + (BFS, DC)                     65.57%
                              + (MCTS, PRM)                   66.39%
                             H UNYUAN P ROVER V 16
                              + (BFS, PC)                     64.75%
                              + (BFS, DC)                     68.44%

               Table 2: Ablation study on different variations of guided tree search.


to the limitation of time and computation resources, we leave separately examining the effectiveness
of MCTS and PRM in future work. In addition, simply replacing policy confidence with distance
critic is also significant effective. Since both PRM and DC only require prover generated data with
natural labels, thus they are both superior choices than policy confidence as critic.
Figure 4 visualizes the distribution over solved miniF2F-test theorems for HunyuanProver v16 and
HunyuanProver v16+DC. HunyuanProver v16+DC finds more deep proofs compared to Hunyuan-
Prover v16 in miniF2F. Interestingly, HunyuanProver v16+DC takes more steps than HunyuanProver
v16 on some of the easiest theorems. We follow previous work to calculate the proof length based
on the number of steps in the shortest proof for each theorem.


5   Conclusions

In this report, we present HunyuanProver, a system that enhances automatic theorem-proving ca-
pabilities using LEAN through iterative tactic data generation and guided tree search. The iterative
tactic data generation method expands the training dataset by nearly 40-fold, resulting in a signif-
icant performance improvement. Meanwhile, critic-guided tree search algorithms further enhance
the overall effectiveness of the prover.


                                                 7
Technical Report




     100
      90
      80
      70
      60
      50
      40
      30
      20
      10
       0
                   1          2           3          4         5-6         7-9         >9
                                       BFS        BFS w/ DC

Figure 4: Proof length distributions of BFS using policy confidence and distance critic respectively
for guidance.


Future work includes better curation for prover training data and exploring other more cost-efficient
tree search algorithms such as Q* (Wang et al., 2024a;b).

References
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Os-
  trow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. arXiv preprint
  arXiv:2410.21276, 2024.
Albert Qiaochu Jiang, Wenda Li, and Mateja Jamnik. Multilingual mathematical autoformalization,
  2024. URL https://openreview.net/forum?id=QqdloE1QH2.
Jia LI, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Costa Huang,
   Kashif Rasul, Longhui Yu, Albert Jiang, Ziju Shen, Zihan Qin, Bin Dong, Li Zhou, Yann
   Fleureau, Guillaume Lample, and Stanislas Polu. Numinamath. [https://huggingface.
   co/AI-MO/NuminaMath-CoT](https://github.com/project-numina/
   aimo-progress-prize/blob/main/report/numina_dataset.pdf), 2024.
Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming Yang. Lean-star: Learning to interleave
  thinking and proving. In The 4th Workshop on Mathematical Reasoning and AI at NeurIPS’24,
  2024.
Haipeng Luo, Qingfeng Sun, Can Xu, Pu Zhao, Jianguang Lou, Chongyang Tao, Xiubo Geng, Qing-
  wei Lin, Shifeng Chen, and Dongmei Zhang. Wizardmath: Empowering mathematical reasoning
  for large language models via reinforced evol-instruct. arXiv preprint arXiv:2308.09583, 2023.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language.
  In Automated Deduction–CADE 28: 28th International Conference on Automated Deduction,
  Virtual Event, July 12–15, 2021, Proceedings 28, pp. 625–635. Springer, 2021.
LC PAULSON. Isabelle: A generic theorem prover. Lecture Notes in Computer Science, 828, 1994.
Ye Tian, Baolin Peng, Linfeng Song, Lifeng Jin, Dian Yu, Haitao Mi, and Dong Yu. Toward self-
  improvement of llms via imagination, searching, and criticizing. In Proceedings of Neurips 2024,
  2024.


                                                 8
Technical Report




Ante Wang, Linfeng Song, Ye Tian, Baolin Peng, Dian Yu, Haitao Mi, Jinsong Su, and Dong Yu.
  Litesearch: Efficacious tree search for llm. arXiv preprint arXiv:2407.00320, 2024a.
Chaojie Wang, Yanchen Deng, Zhiyi Lyu, Liang Zeng, Jujie He, Shuicheng Yan, and Bo An.
  Q*: Improving multi-step reasoning for llms with deliberative planning. arXiv preprint
  arXiv:2406.14283, 2024b.
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang
  Sui. Math-shepherd: Verify and reinforce llms step-by-step without human annotations. In Pro-
  ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume
  1: Long Papers), pp. 9426–9439, 2024c.
Chenrui Wei, Mengzhou Sun, and Wei Wang. Proving olympiad algebraic inequalities without hu-
  man demonstrations, 2024. URL https://openreview.net/forum?id=8kFctyli9H.
Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai Chen.
  Internlm2. 5-stepprover: Advancing automated theorem proving via expert iteration on large-scale
  lean problems. arXiv preprint arXiv:2410.15700, 2024.
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale
  synthetic data. arXiv preprint arXiv:2405.14333, 2024a.
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
  Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F.
  Wu, Fuli Luo, and Chong Ruan. Deepseek-prover-v1.5: Harnessing proof assistant feedback
  for reinforcement learning and monte-carlo tree search, 2024b. URL https://arxiv.org/
  abs/2408.08152.
Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
  Zhang, Xuan Lu, Qiushi Du, et al. Deepseek-prover-v1.5: Harnessing proof assistant feedback
  for reinforcement learning and monte-carlo tree search. arXiv preprint arXiv:2408.08152, 2024c.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-
  augmented language models. Advances in Neural Information Processing Systems, 36, 2024.
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean workbook:
  A large-scale lean problem set formalized from natural language math problems. arXiv preprint
  arXiv:2406.03847, 2024.
Longhui Yu, Weisen Jiang, Han Shi, YU Jincheng, Zhengying Liu, Yu Zhang, James Kwok, Zhen-
  guo Li, Adrian Weller, and Weiyang Liu. Metamath: Bootstrap your own mathematical questions
  for large language models. In The Twelfth International Conference on Learning Representations,
  2024.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. In International Conference on Learning Representations,
  2022. URL https://openreview.net/forum?id=9ZPegFuFTFv.




                                                9
Technical Report




A    Examples Theorems Proved by HunyuanProver

    Example 1 (From Chinese High School Mathematics League)

       Natural Language Problem
       The sequences {an } and {bn } satisfy a1 = 1, b1 = 2, an+1 = 1+anb+a
                                                                         n
                                                                           n bn
                                                                                , bn+1 =
       1+bn +an bn
           an      . Prove that : a2008 < 5.


    theorem theorem_11044972_a81f_4ea2_afa4_339d23e89245 (a b : N → R)
    (a1 : a 1 = 1)
    (b1 : b 1 = 2)
    (a_rec : ∀ n, a (n + 1) = (1 + a n + a n * b n) / b n)
    (b_rec : ∀ n, b (n + 1) = (1 + b n + a n * b n) / a n) :
    a 2008 < 5 := by

    induction 2008 <;> simp_all [Nat.add_succ, Nat.succ_add,
        Nat.mul_succ, Nat.succ_mul]
    contrapose! a1
    all_goals have h1 : a 0 ̸= 0 := fun h => by simp [h] at b1
    field_simp at b1 ⊢
    intro h
    all_goals
      have := a_rec 0
      have := b_rec 0
      simp_all [div_eq_mul_inv, mul_add, add_mul, mul_comm, mul_assoc,
        mul_left_comm]
    field_simp at h
    have h2 : b 0 ̸= 0 := fun hb => by simp [hb] at h
    field_simp at h
    nlinarith
    have h2 : b 0 ̸= 0 := fun h => by simp [h] at a1
    field_simp at a1 b1 ⊢
    have h3 : 0 < 1 + a 0 + a 0 * b 0 := by nlinarith
    have h4 := mul_self_pos.mpr h1
    rw [div_lt_iff] <;> nlinarith




                                              10
Technical Report




   Example 2 (From IMO 1962 P2)

      Natural Language Problem
      Determine all real numbers x which satisfy the inequality:
                                    √           √
                                  q
                                                           1
                                       3−x− x+1>
                                                           2
                     "            √     !
                                    127
      Show that it is − 1, 1 −             .
                                    32


   theorem imo_1962_p2 (x : R) (h0 : 0 ≤ 3 - x) (h1 : 0 ≤ x + 1)
       (h2 : 1 / 2 < Real.sqrt (Real.sqrt (3 - x) - Real.sqrt (x +
       1))) : -1 ≤ x ∧ x < 1 - Real.sqrt 127 / 32 := by

   rw [← sub_nonneg] at h0 h1
   refine’ ⟨by linarith [Real.sqrt_nonneg (3 - x), Real.sqrt_nonneg (x
       + 1)], _⟩
   contrapose! h2
   norm_num at h0 h1
   rw [Real.sqrt_le_iff]
   norm_num
   rw [Real.sqrt_le_left]
   rw [sq, add_mul_self_eq]
   field_simp
   norm_num
   rw [← sub_nonneg]
   swap
   refine’ add_nonneg _ (sqrt_nonneg _)
   linarith [Real.sqrt_nonneg (x + 1)]
   have h3 : 0 ≤ Real.sqrt (x + 1) := sqrt_nonneg _
   nlinarith [Real.sq_sqrt h1 , Real.sq_sqrt (by positivity : (0:R) ≤
       127)]




   Example 3 (From lean workbook 2061)

      Natural Language Problem
      Prove the theorem: Let a, b, c be three integer numbers so that abc ̸= 0. Then the
      equation ax + by = c has at least an integer solution if and only if the greatest
      common divisor of the numbers a and b divides the number c.

   theorem lean_workbook_2061 (a b c : Z) (habc : a * b * c ̸= 0) :
       (∃ x y : Z, a * x + b * y = c) ↔ (gcd a b) | c := by

   constructor
   rintro ⟨x, y, h⟩
   rw [← h]
   exact dvd_add (dvd_mul_of_dvd_left (GCDMonoid.gcd_dvd_left a b) x)
       (dvd_mul_of_dvd_left (GCDMonoid.gcd_dvd_right a b) y)
   intro h
   obtain ⟨x, y, hxy⟩ := exists_gcd_eq_mul_add_mul a b
   obtain ⟨z, rfl⟩ := h
   exact ⟨x * z, y * z, by rw [← mul_assoc, ← mul_assoc, hxy]; ring⟩




                                               11
Technical Report




   Example 4 (From AIPS)

      Naturalp Language Problem
                              p 3           p
      abc/(a (a3 + c3 ) + b (ap   + b3 ) + c (b3 + c3 ))p
                                                        <= (a2 + b2 )(a2 + c2 )(b2 +
      c )/(2((a +pb )(a + c ) (a + c ) + (a + b ) (a3 + b3 )(b2 + c2 ) + (a2 +
       2        2    2    2     2  3      3     2    2

      c2 )(b2 + c2 ) (b3 + c3 )))


   theorem theorem_dc0af938_4a25_4093_8ed3_7f4999a556ed {a b c : R}
       (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : a * b * c / (a *
       Real.sqrt (a ˆ 3 + c ˆ 3) + b * Real.sqrt (a ˆ 3 + b ˆ 3) + c *
       Real.sqrt (b ˆ 3 + c ˆ 3)) ≤ (a ˆ 2 + b ˆ 2) * (a ˆ 2 + c ˆ 2) *
        (b ˆ 2 + c ˆ 2) / (2 * (a ˆ 2 + b ˆ 2) * (a ˆ 2 + c ˆ 2) *
       Real.sqrt (a ˆ 3 + c ˆ 3) + 2 * (a ˆ 2 + b ˆ 2) * Real.sqrt (a
       ˆ 3 + b ˆ 3) * (b ˆ 2 + c ˆ 2) + 2 * (a ˆ 2 + c ˆ 2) * (b ˆ 2 +
       c ˆ 2) * Real.sqrt (b ˆ 3 + c ˆ 3)) := by

   have h1 : 0 ≤ (a - b) ˆ 2 * (aˆ2 + cˆ2) * (bˆ2 + cˆ2) := by
       positivity
   rw [mul_assoc]
   rw [← sub_nonneg]
   have h2 : 0 ≤ (a - c) ˆ 2 * (a ˆ 2 + b ˆ 2) * (b ˆ 2 + c ˆ 2) :=
       by positivity
   have h3 : 0 ≤ (b - c) ˆ 2 * (a ˆ 2 + b ˆ 2) * (a ˆ 2 + c ˆ 2) :=
       by positivity
   field_simp [ha.ne’, hb.ne’, hc.ne’, h1, h2, h3]
   have h4 : 0 ≤ a ˆ 2 * b ˆ 2 := mul_nonneg (sq_nonneg _) (sq_nonneg
       _)
   have h5 : 0 ≤ (a * Real.sqrt (a ˆ 3 + c ˆ 3) - b * Real.sqrt (a ˆ
       3 + b ˆ 3)) ˆ 2 := sq_nonneg _
   have h6 := sq_nonneg (a * Real.sqrt (bˆ3 + cˆ3) - b * Real.sqrt
       (aˆ3 + cˆ3))
   have h7 : 0 ≤ (a * Real.sqrt (a ˆ 3 + c ˆ 3) - c * Real.sqrt (b ˆ
       3 + c ˆ 3)) ˆ 2 := sq_nonneg _
   have h8 : 0 ≤ (b * Real.sqrt (a ˆ 3 + c ˆ 3) - c * Real.sqrt (a ˆ
       3 + b ˆ 3)) ˆ 2 := sq_nonneg _
   have h9 : 0 ≤ a ˆ 2 * c ˆ 2 := mul_nonneg (sq_nonneg _) (sq_nonneg
       _)
   have h10 : 0 ≤ (bˆ2 + cˆ2) * (aˆ2 + cˆ2) := by positivity
   have h11 : 0 ≤ (aˆ2 + bˆ2) * (aˆ2 + cˆ2) := by positivity
   have h12 : 0 ≤ (aˆ2 + bˆ2) * (bˆ2 + cˆ2) := by positivity
   have h13 : 0 ≤ (a * Real.sqrt (a ˆ 3 + c ˆ 3) - b * Real.sqrt (a ˆ
       3 + b ˆ 3)) ˆ 2 := sq_nonneg _
   have h14 := sq_nonneg (a * Real.sqrt (b ˆ 3 + c ˆ 3) - c *
       Real.sqrt (a ˆ 3 + c ˆ 3))
   have h15 : 0 ≤ (a * Real.sqrt (aˆ3 + cˆ3) - b * Real.sqrt (aˆ3 +
       bˆ3))ˆ2 := sq_nonneg _
   have h16 : 0 ≤ (a * Real.sqrt (a ˆ 3 + b ˆ 3) - b * Real.sqrt (b ˆ
       3 + c ˆ 3)) ˆ 2 := sq_nonneg _
   have h17 := sq_nonneg (a * Real.sqrt (bˆ3 + cˆ3) - b * Real.sqrt
       (aˆ3 + cˆ3))
   have h18 : 0 ≤ (a * Real.sqrt (aˆ3 + cˆ3) - b * Real.sqrt (aˆ3 +
       bˆ3))ˆ2 := sq_nonneg _
   have h19 := sq_nonneg (a * Real.sqrt (aˆ3 + cˆ3) - c * Real.sqrt
       (bˆ3 + cˆ3))
   have h20 : 0 ≤ a ˆ 2 * b ˆ 2 := mul_nonneg (sq_nonneg _)
       (sq_nonneg _)
   have h21 : 0 ≤ a * Real.sqrt (aˆ3 + cˆ3) := mul_nonneg ha.le
       (Real.sqrt_nonneg _)
   have h22 : 0 ≤ b * Real.sqrt (a ˆ 3 + b ˆ 3) := by positivity
   have h23 : 0 ≤ c * Real.sqrt (b ˆ 3 + c ˆ 3) := by positivity
   refine’ div_nonneg (by nlinarith) (by positivity)



                                           12
Technical Report




    Example 5 (From NuminaMath)

       Natural Language Problem 
                                     21−x          (x ⩽ 1)
       Given the function f (x) =                          , find the range of x that satisfies
                                     1 − log2 x    (x > 1)
       f (x) ⩽ 2.

       A: [−1, 2]
       B: [0, 2]
       C: [1, +∞)
       D: [0, +∞)

       answer: [0, +∞)


    theorem theorem_5319d37e_b470_42f5_a42f_b4221daceb81 (f : R → R)
        (x : R) (hf: f x = if x ≤ 1 then 2ˆ(1-x) else 1 - Real.logb 2
        x) : f x ≤ 2 ↔ x ≥ 0 := by

    rw [hf]
    refine’ ⟨fun h => _, fun h => _⟩
    split_ifs at h with h_1
    contrapose! h
    rw [← Real.rpow_one 2]
    rw [← rpow_mul (by norm_num)]
    rw [one_mul, Real.rpow_lt_rpow_left_iff (by norm_num)]
    linarith
    all_goals aesop
    case neg =>
      linarith
    rw [← Real.rpow_one 2]
    rw [← Real.rpow_mul zero_lt_two.le]
    rw [one_mul, Real.rpow_le_rpow_left_iff (by norm_num)]
    linarith
    linarith [logb_pos (show (1 : R) < 2 by norm_num) <_>]




B    Policy Prompt


    An example of the policy model

    Prompt
    Given the Lean 4 tactic state, suggest a next tactic.
    Tactic state:
    a b : R
    hab : a > 0 ∧ b > 0
    h1 : 0 < Real.log 2
    h : Real.log (a * b) = Real.log (2 ˆ 6)
    ⊢ a + b ≥ 16

    Next tactic:
    Response
    rw [Real.log_mul] at h




                                                  13
Technical Report




C    Distance Critic Prompt

    An example of the critic model

    Prompt
    Here is a Lean4 state:
    case refine’_1.intro
    a : R
    h : (∀ x ∈ Set.Icc 0 1, a ≥ rexp x) ∧ ∃ x, x ˆ 2 + 4 * x + a = 0
    hx1 : R
    hx2 : hx1 ˆ 2 + 4 * hx1 + a = 0
    ⊢ a ∈ Set.Icc (rexp 1) 4

    case refine’_2
    a : R
    h : a ∈ Set.Icc (rexp 1) 4
    x : R
    hx : x ∈ Set.Icc 0 1
    ⊢ a ≥ rexp x

    case refine’_3
    a : R
    h : a ∈ Set.Icc (rexp 1) 4
    ⊢ ∃ x, x ˆ 2 + 4 * x + a = 0

    ----------------
    Please tell me how many more tactic steps are needed to finish
        this state.
    Response
    Let me think step by step.
    ... ...
    So, there is <num_box><num-1-of-2><num-1-of-4><num-1-of-8>
    <num-2-of-16><num-4-of-32><num-7-of-64></num_box> more tactic
         steps are needed to finish this state.




                                     14
