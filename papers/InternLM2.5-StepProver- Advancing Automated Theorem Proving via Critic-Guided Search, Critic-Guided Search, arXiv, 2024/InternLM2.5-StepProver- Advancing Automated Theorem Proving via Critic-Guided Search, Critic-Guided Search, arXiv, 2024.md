                                                  InternLM2.5-StepProver: Advancing Automated Theorem Proving via
                                                                        Critic-Guided Search


                                                  Zijian Wu * 1 2 Suozhi Huang * 3 Zhejian Zhou 1 4 Huaiyuan Ying 1 3 Zheng Yuan 2 Wenwei Zhang 1
                                                                                       Dahua Lin 1 2 Kai Chen 1


                                                                     Abstract                                   ing silver-medal performance on International Mathemati-
                                                                                                                cal Olympiad problems using the LEAN 4 proof assistant,
                                                 Large Language Models (LLMs) have emerged as
arXiv:2410.15700v2 [cs.AI] 21 Oct 2025




                                                                                                                particularly excelling in number theory and algebra. The
                                                 powerful tools in mathematical theorem proving,
                                                                                                                training regime of AlphaProof, based on the AlphaZero
                                                 particularly when utilizing formal languages such
                                                                                                                methodology (Silver et al., 2017), encompasses 100 million
                                                 as LEAN. A prevalent proof method involves the
                                                                                                                formal mathematics problems—a scale that significantly
                                                 LLM prover iteratively constructing the proof tac-
                                                                                                                surpasses previous efforts (Polu et al., 2022; Lample et al.,
                                                 tic by tactic, typically following a best-first search
                                                                                                                2022; Xin et al., 2024a;b).
                                                 scheme. However, this method often ignores the
                                                 critical preference information inside the exist-              Existing open-source methods typically train a language
                                                 ing tactic trajectories, hindering the search for              model on tuples of (proof state, next tactic), followed by
                                                 deeper proofs. We propose an intuitive yet ef-                 best-first tree search to find proofs (Polu & Sutskever, 2020;
                                                 fective method, which utilizes a critic model to               Polu et al., 2022; Lample et al., 2022; Yang et al., 2024; Lin
                                                 capture the preference information and to guide                et al., 2024; Wu et al., 2024). The term ”best-first” refers to
                                                 the search of the prover model at runtime. Given               relying on internal indicators from the prover model (e.g.,
                                                 the prover-critic framework, a large-scale expert              the log-probability scores of generated tactics) to guide
                                                 iteration with more than 20,000 CPU days is then               the search. An observation is that such indicators become
                                                 applied to further fine-tune the prover and the                unreliable when searching for deeper proofs, leading to per-
                                                 critic. The trained InternLM2.5-StepProver critic              formance degradation. Experimental results from previous
                                                 significantly boosts the performance of the prover             studies (Wu et al., 2024) have shown that even when the
                                                 model (59.4% → 65.9%). We also analyze the                     prover model is trained on extensive formal language cor-
                                                 impact of the critic on various aspects of the theo-           pora, the ability to discover deeper proofs remains difficult
                                                 rem proving process during expert iteration, pro-              to acquire. For example, although InternLM2-StepProver
                                                 viding insights into its effectiveness. The models             achieves 48.8% on miniF2F-test, the longest proof it discov-
                                                 and the discovered proofs will be open-sourced.                ers contains only 8 tactics—a stark contrast to typical tree
                                                                                                                searches that require 100 to 1000 steps.
                                                                                                                Inspired by recent advances in informal mathematical rea-
                                         1. Introduction                                                        soning (Lightman et al., 2023; Xu et al., 2024), our key
                                         Automated theorem proving has been a challenging topic in              insight is that the tree structure constructed during the
                                         artificial intelligence (Pfenning, 2004; Zheng et al., 2021;           search process is naturally suited for process supervision.
                                         Wu et al., 2022; Polu et al., 2022) which requires complex             The search trajectories inherently provide the data needed
                                         reasoning and a deep understanding of mathematics. Al-                 to train the supervision model—which we term the critic
                                         phaProof1 has demonstrated remarkable progress by achiev-              model. Therefore, a prover-critic framework is built in
                                                                                                                which the critic model estimates the ”value” of each state
                                             *
                                             Equal contribution 1 Shanghai AI Laboratory, Shanghai, China       and decides which states to explore further.
                                         2
                                           The Chinese University of Hong Kong, Hong Kong, China
                                         3
                                           Tsinghua University, Beijing, China 4 University of Southern         Building on this framework, our work then leverages the
                                         California, Los Angeles, USA. Correspondence to: Zijian Wu             Lean-workbook (Ying et al., 2024a), the largest open-source
                                         <wuzijian@pjlab.org.cn>, Kai Chen <chenkai@pjlab.org.cn>.
                                                                                                                problem collection available, to conduct systematic expert
                                         Proceedings of the 42 nd International Conference on Machine           iteration and analyze proving strategies at scale. We ini-
                                         Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025            tiate InternLM2.5-StepProver-critic by collecting roughly
                                         by the author(s).                                                      8000 preference pairs from the search trajectories when
                                             1
                                               https://deepmind.google/discover/blog/                           InternLM2-StepProver is evaluated on its training sets. We
                                         ai-solves-imo-problems-at-silver-medal-level/

                                                                                                            1
                  InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

then perform expert iteration on Lean-workbook. Our ex-                                                                         
tensive experimentation, consuming over 20,000 CPU days,                                              Xi−1                      
yielded several key contributions to the challenge of auto-                          s∗ = arg max                − log p(tj |sj )
                                                                                                 si ∈S                          
mated theorem proving:                                                                                     j=0


                                                                         where S represents the set of all unexpanded states,
   • We present a novel approach that significantly enhances             (s0 , t0 ), · · · , (si−1 , ti−1 ) denotes the proof trajectory lead-
     theorem proving capabilities by utilizing a separate                ing to state si , and log p(tj |sj ) represents the average log
     critic model to guide the search for deeper proofs. Ex-             probability of each generated token conditioned on the state.
     periments demonstrate that the critic model boosts the              The algorithm expands up to N states, achieving success-
     performance of the prover model from 59.4% to 65.6%                 ful proof search upon reaching any proof state with no re-
     on miniF2F (when used without the vanilla best-first                maining goals. Multiple search attempts (K times) can be
     search method) or to 65.9% when combined with it.                   performed to calculate a pass rate pass@K. However, anal-
                                                                         ysis of the search trajectories of our models indicates that
   • We provide an example of massive expert iteration,                  the best-first search method exhibits poor performance (as
     demonstrating the effectiveness of expert iteration on              shown in Fig. 5). Thus, we hypothesize that average log
     synthetic datasets. The enlarged Lean-workbook solu-                probabilities may not serve as an effective metric to guide
     tion set will be open-sourced.                                      the heuristic search process.
   • We identify a log-linear relationship between the num-
                                                                         Critic-Guided Search Recent literature (Lin et al., 2024)
     ber of proved problems and both proof length and com-
                                                                         indicates that best-first search (BFS) methods may be sub-
     putational resources, providing valuable insights for
                                                                         optimal for formal proving. A primary advantage of tree
     resource allocation in future work.
                                                                         search strategies, when compared to whole-proof genera-
                                                                         tion, is their capacity to leverage critical information from
                                                                         intermediate prover states. However, best-first search algo-
2. Methods                                                               rithms, as they only look at the average log probability of
                                                                         tactics, often fail to fully capitalize on this advantage, as
We introduce critic-guided search, a novel framework that
                                                                         shown in Fig 1. Therefore, using best-first-search with log-
enhances automated theorem proving by incorporating criti-
                                                                         probability scores seldom leads to deep proofs and limits
cal evaluation mechanisms into the proof search process, to
                                                                         the proving ability of our model, which is consistent with
address key limitations of existing best-first search methods
                                                                         our experiments (shown in Fig 3). Therefore, we choose to
through structured critique generation and expert iteration
                                                                         train a critic model (Lample et al., 2022; Polu et al., 2022)
(Anthony et al., 2017; Polu et al., 2022). The methodology
                                                                         to better guide our prover model for proof generation.
consists of two main components: First, we present a critic-
guided search algorithm and compare it with traditional                  The critic model (V ) uses the proof state (s) as the input and
best-first search approaches (§2.1). Second, we describe our             outputs a scalar (V (s) ∈ R). At each iteration, the algorithm
expert iteration framework that iteratively refines the proof            selects the optimal state si for expansion by querying the
search strategy through bootstrapping processes.                         critic model. Then it employs the prover model to generate
                                                                         candidate tactics. We train our critic model in a preference
2.1. Search Methods                                                      style which is similar to reward model training in RLHF
                                                                         (Ouyang et al., 2022) instead of binary targets (the state can
Best-First Search. The most widely adopted approach                      be proved or not). Two types of preference pairs are created
for evaluating the theorem proving capabilities of language              in the training process:
models M involves employing best-first search algorithms,
as demonstrated in GPT-f (Polu & Sutskever, 2020; Azer-
                                                                            • Path Pairs: For a successful proof path from the root
bayev et al., 2023b). This method maintains a collection of
                                                                              (initial proof state) to no goals, we hypothesize that
all unexpanded states si . At each iteration, the algorithm
                                                                              a state close to the target is always better. Thus we
selects the optimal state si for expansion and employs the
                                                                              create preference pairs where the positive example
language model to generate S candidate tactics ti,1···S for
                                                                              is a child state closer to no goals and the negative
the current state si . For each valid tactic ti,j , a new state is
                                                                              example is the parent state closer to the initial root state
derived by executing tactic ti,j on state si .
                                                                              (i.e. V (st ) < V (st+∆ )), which implicitly assumes that
Following established conventions (Polu & Sutskever, 2020;                    any legal tactic on a successful path toward no goals
Yang et al., 2024), the state with the highest negative log-                  yields a positive reward r. For a path of lengthn, this
probability is considered optimal. Specifically, we select                    methodology allows us to generate at most n2 pairs
the state s∗ that satisfies:                                                  of positive and negative examples.

                                                                     2
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search




Figure 1: Comparison of Best-first Search and Critic-Guided Search methods. Left: Best-first search relies solely on log
probability scores from tactic logits, under-utilizing intermediate state information. Right: Critic-Guided search employs a
critic model to re-rank states, enabling more informed state expansion decisions. Note that a lower log probability score
indicates a higher priority, whereas a higher critique score also signifies increased priority.


   • Sibling Pairs: We construct preference pairs con-                 formalized propositions might be incorrect. Therefore, ev-
     sisting of a state on the successful path (positive ex-           ery formalized proposition includes its negated version in
     ample) and its sibling state (negative example) (i.e.             the dataset, following the paradigm outlined in (Xin et al.,
     V (ssibling ) < V (st )). Sibling states are defined as           2024a). Proofs are searched using best-first and critic-
     child nodes of the same parent that did not lead to               guided algorithms by generating a tactic as an action (Polu
     no goals. This design is based on the principle that              et al., 2022; Azerbayev et al., 2023b; Wu et al., 2024).
     the state on the successful path (st ) is preferable to its
                                                                       Initially, we conduct a rapid scan of the entire Lean-
     sibling state (ssibling ), which did not lead to a proof.
                                                                       workbook-plus dataset using a relatively small search budget
                                                                       (i.e., a maximum of 10 iterations per problem and a time
2.2. Expert Iteration                                                  limit of 50 seconds). The discovered proofs are added to
                                                                       the training set, and the solved problems, along with their
Bootstrapping The proposed approach utilizes the                       negated statements, are removed from the dataset. This
InternLM2-StepProver(Wu et al., 2024), our latest model                process helps us identify statements that are inherently un-
for formal reasoning, as the foundational prover model,                provable, thereby enhancing the efficiency of the iteration.
along with an initial dataset. This dataset is aggregated from
four distinct sources: the miniF2F-train split, the mathlib            This process is then repeated over multiple rounds, gradually
dataset, the Lean-Workbook, and the Lean-Github dataset.               increasing the search budget for subsequent evaluations until
Collectively, these sources furnish the initial states si , each       a predefined upper bound (at most 2000 iterations and 3600
representing a theorem to be proven. For the initialization            seconds per problem) is reached. After each round, we
of the critic model, the prover model is initially tasked with         retrain our prover and critic models using an expanded set
generating K solution samples (trajectories) per theorem.              of successful proof trajectories. Since some found proofs
Following this, a preference dataset is curated by sampling            are ill-formed and contain many irrelevant proof steps with
preference pairs from successful search trajectories; this             higher CPU consumption, we continue to search for proofs
dataset is then used for training the prover model. The                for these problems, aiming to use shorter and more direct
overall iterative procedure is executed multiple times. The            proofs to improve our models.
process terminates when the critic-guided search method                After model iterations, we use the critic model to re-estimate
achieves performance superior to that of standard (vanilla)            all unproven statements. Next iteration will then focus on
methods on the miniF2F-train benchmark, which serves as                the top 50% of problems that the critic model indicates are
an indicator that the critic model is stabilized.                      most likely to be solvable.

Expert Iteration on Lean-Workbook With our initial-
ized prover and critic models, we perform expert itera-                Prover Model Objective The traditional proofstep ob-
tion on the Lean-Workbook dataset. Due to limitations                  jective, used by GPT-f (Polu & Sutskever, 2020), gener-
in auto-formalization accuracy, it is recognized that some             ates a PROOFSTEP (a Lean tactic) given a GOAL (cur-

                                                                   3
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

---
NAME: square_sub_one_divisible_eight
---
PROOF_BEFORE: rw [h, pow_two]
---
STATE_BEFORE: m n : N
h : n = 2 * m + 1
⊢ 8 | (2 * m + 1) * (2 * m + 1) - 1
---
TACTIC:

rw [← Nat.mod_add_div (2 * m + 1) 8]


Figure 2: An example of the prompt used by the prover
model.




rent Lean tactic state) and the current DECLARATION
(the Lean theorem name to be proved).                The ac-
tual prompt used by GPT-f includes an additional dec-
laration field, i.e., DECL <DECLARATION> \nGOAL
<GOAL> \nPROOFSTEP <PROOFSTEP>.                    However,
such prompts, though easy to integrate with existing de-
ployment frameworks, lack information regarding the pre-
vious proof contents. Hoping to improve the reasoning
performance in deep search trees, we augment our prompt
template with ongoing proof context. The format of the
prompt is modified to include the previous tactics leading to
the state in a field called PROOF BEFORE. An example of             Figure 3: Critic-guided search finds more deep proofs com-
the prompt template is shown in Fig.2.                              pared to best-first-search in ProofNet and miniF2F-test. We
                                                                    calculate the proof length based on the number of tactics.
                                                                    Only the shortest 5 proofs are considered for each solved
3. Experiments and Results                                          problem.
We evaluate our approach on Lean-workbook-plus (Ying
et al., 2024a), one of the largest auto-formalized prob-
lem sets in Lean 4, which provides comprehensive cov-               3.1. Benchmark Performance of
erage of diverse mathematical reasoning tasks. The                       InternLM2.5-StepProver
integration of critic mechanisms enables our system                 A comprehensive analysis of InternLM2.5-StepProver is
to discover deeper proofs while maintaining computa-                conducted on several standard formal benchmarks, in com-
tional efficiency. We trained InternLM2.5-StepProver and            parison with our previous model InternLM2-StepProver,
InternLM2.5-StepProver-critic on Lean-Workbook with                 as well as a number of other frontier language models, to
more than 20000 CPU hours of expert iteration. The mod-             exhibit the strength of our approach.
els are then evaluated on miniF2F(Zheng et al., 2021) and
ProofNet(Azerbayev et al., 2023a).
                                                                    miniF2F We first analyze the performance on the miniF2F
Experimental results show that both critic-guided search            benchmark (Zheng et al., 2021). The original benchmark
and expert iteration boost the theorem proving capabilities         was released in Lean 3 and was later ported to an earlier
of the prover model. The critic-guided search techniques            version of Lean 4. We use the Lean 4 version of miniF2F,
significantly enhance the prover model in its ability to find       as released by the LeanDojo project (Yang et al., 2024),
deeper proofs. We describe our experiments and findings in          with our adaptations to Lean 4.7.0 and corrections of several
detail below.                                                       formalization mistakes.

                                                                4
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

Table 1: Compared with other baselines on the miniF2F (Zheng et al., 2021) dataset. BF represents best-first-search and CG
represents critic-guided search.

          Method                                    Model size               Pass           miniF2F-valid   miniF2F-test
          Whole-Proof Generation Methods
          TheoremLlama (Wang et al., 2024b)              -                cumulative           36.5%          33.6%
          DeepSeek-Prover (Xin et al., 2024a)           7B                   128                  -           46.1%
                                                                          16 × 4096               -           50.0%
          DeepSeek-Prover-V1.5-RL                       7B                     32                 -           50.0%
                                                                               64                 -           50.7%
                                                                              128                 -           51.6%
                                                                             3200                 -           54.9%
                                                                           4 × 6400               -           58.4%
                                                                          16 × 6400               -           60.2%
          Tree Search Methods
          PACT (Han et al., 2021)                     837M               1 × 16 × 512          23.9%          24.6%
                                                                         8 × 16 × 512          29.3%          29.2%
          ReProver (Yang et al., 2024)                229M                      -                 -           26.5%
          Llemma (Azerbayev et al., 2023b)              7B               1 × 32 × 100          26.2%          26.2%
          Llemma (Azerbayev et al., 2023b)             34B               1 × 32 × 100          27.9%          25.8%
          Curriculum Learning (Polu et al., 2022)     837M                1 × 8 × 512          33.6%          29.6%
                                                                          8 × 8 × 512          41.2%          34.5%
                                                                         64 × 8 × 512          47.3%          36.6%
          HTPS (Lample et al., 2022)                  600M                 cumulative          58.6%             -
                                                                           64 × 5000              -           41.0%
          Lean-STaR (Lin et al., 2024)                  7B                64 × 1 × 50             -           46.3%
          InternLM2-Math (Ying et al., 2024b)           7B               1 × 32 × 100          29.9%          30.3%
          InternLM2-Math-Plus                           7B               1 × 32 × 100             -           43.4%
          DeepSeek-Prover-V1.5-RL                       7B                  1 × 3200              -           55.0%
                                                                            4 × 6400              -           59.6%
                                                                           16 × 6400              -           62.7%
                                                                           32 × 6400              -           63.5%
          InternLM2-StepProver (Wu et al., 2024)        7B            1 × 32 × 100 (beam)      59.8%          48.8%
                                                                         64 × 32 × 100         63.9%          54.5%
          InternLM2.5-StepProver-BF                     7B               1 × 32 × 600          55.4%          47.3%
                                                                         4 × 32 × 600          61.3%          52.6%
                                                                         16 × 32 × 600         63.7%          57.3%
                                                                         64 × 32 × 600         64.6%          59.2%
                                                                        256 × 32 × 600         65.1%          59.4%
          InternLM2.5-StepProver-CG                     7B               1 × 32 × 600          49.4%          43.0%
                                                                         4 × 32 × 600          55.9%          56.1%
                                                                         16 × 32 × 600         64.5%          61.7%
                                                                         64 × 32 × 600         67.7%          64.3%
                                                                        256 × 32 × 600         68.4%          65.6%
          InternLM2.5-StepProver-BF+CG                  7B               2 × 32 × 600          56.0%          50.7%
                                                                         4 × 32 × 600          61.4%          58.5%
                                                                         16 × 32 × 600         65.8%          62.5%
                                                                         64 × 32 × 600         68.0%          63.8%
                                                                        256 × 32 × 600         69.6%          65.9%



The best-first-search approach employs an evaluation set-              for both methods can be universally described as P ×S ×K,
ting similar to that of InternLM2-StepProver, where the                where P represents the number of passes, S the number of
model selects states to expand based on the average log-               states, and K the maximum number of state expansions,
likelihood of the tactics leading to those states. In contrast,        or search iterations. In our context, we set S = 32 and
the critic-guided (CG) search method involves the prover               K = 600, with the temperature fixed at T = 0.7. In a
model selecting states to expand based on InternLM2.5-                 BF+CG scenario, the computation budgets are equally dis-
StepProver-critic that grades each state. The search budget            tributed. The test results are presented in Tab. 1.


                                                                  5
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

ProofNet The evaluation setting is mainly the same as                CPUs, the GPU time consumed is proportional to the total
miniF2F. Tab. 2 presents the performance of various models           CPU time (in our case, approximately 1:11). In summary,
on the ProofNet dataset. The BF+CG strategy equally dis-             approximately 21,364 CPU days are consumed throughout
tributes search budgets on two methods. As we are not tak-           the entire expert iteration process. However, these search
ing the validation set of ProofNet for expert iteration, only        budgets are not uniformly distributed across all formalized
the pass rate on the whole dataset is reported. InternLM2.5-         problems. Easier problems are more likely to be solved in
StepProver achieved a pass@256 of 27.0% overall.                     the early rounds of iteration, thereby ceasing to consume
                                                                     search resources in later rounds. The search consumption of
Critic-Guided Search Improves Theorem Proving.                       each problem is a key indicator of the distribution of prob-
From Tab. 1, it is observed that critic-guided search per-           lem difficulty and can provide valuable insights for further
forms significantly better than the best-first method using          scaling. In our case, we selected the CPU time consumed
the same prover model. The critic-guided method achieves             per successful proof as an estimate of resource consumption
an accuracy rate of 68.4% on miniF2F-Valid and 65.6% on              expectations. Consider the set of problems S = {si }. For
miniF2F-Test, which is only slightly lower than the com-             each problem si , let Psi denote the set of all attempts, and
bined methods and substantially higher than the BF method.           Tsi ,j represent the time spent on the j-th attempt of problem
These experimental results indicate that the critic model            si . Define the indicator function valid(si , j), which equals
enhances the inherent proving ability of the prover model,           1 if the j-th attempt on problem si results in a valid solution,
enabling it to discover deeper proofs. Analysis of the length        and 0 otherwise. The CPU time P     consumed per successful
                                                                                                           j Tsi ,j
distribution of the searched solutions (shown in Fig. 3) fur-        proof, Csi , is given by: Csi = P valid(s    i ,j)
                                                                                                                        .
                                                                                                         j
ther validates this observation, as CG methods consistently
discover deeper proofs than BF methods, successfully con-            Table 4 presents a detailed analysis of computational re-
structing proofs with more than 9 tactics.                           source consumption. A key observation is that the majority
                                                                     of CPU resources are expended on problems that are chal-
                                                                     lenging to prove or disprove. Notably, only about 1.5% of
Critic-Guided Search Explores a Distinct Proof Space.
                                                                     CPU resources are used to solve 17.0% of the problems,
Another observation is that the proof distribution discov-
                                                                     while the remaining 98.5% of resources yield no successful
ered by critic-guided (CG) search differs significantly from
                                                                     outcomes.
that of the best-first (BF) approach. The synergistic ef-
fect of combining the two methods highlights this distinc-           Fig 4 provides a more granular analysis of the distribution
tion. For instance, a hybrid model achieves 69.6% accu-              of CPU search time for each problem. A number of ob-
racy on miniF2F-Valid and 65.9% on miniF2F-Test. On                  servations can be made from the graph. First, the graph
the ProofNet benchmark, this synergy is even more pro-               reveals a peak in the near-zero region, suggesting the pres-
nounced: while BF and CG individually solve 22.3% and                ence of numerous trivial problems in the auto-formalized
23.9% of problems, their combination solves 27.0%. These             dataset. Second, a log-linear trend is evident for problems
results strongly indicate that critic-guided search navigates        with CPU search times between approximately 0 and 10,000
the proof space differently, identifying novel solutions that        seconds. Assuming an equal distribution of problem diffi-
a scaled-up BF search alone would not discover. How-                 culties, searching for longer proofs becomes exponentially
ever, with low sampling budgets, CG may overlook simpler             harder due to the search space explosion problem, which
proofs that are trivial for BF. Therefore, a hybrid search was       explains the occurrence of this trend. Unfortunately, the
adopted to leverage the strengths of both methods in our             best-first approach is observed to degrade to a brute-force
experiment.                                                          approach—discovering fewer proofs with larger search bud-
                                                                     gets (¿10,000 s)—while the critic-guided approach performs
3.2. Results of Expert Iteration                                     better, discovering more solutions beyond the log-linear
                                                                     trend.
As Tab. 3 shows, a total of 17.0% of the Lean-workbook-
plus problems are proved or disproved, making a noticeable
improvement since the release of Lean-Workbook. These                Scaling Proof Lengths in Expert Iteration. As analyzed
proved and disproved statements and their corresponding              in the previous section, best-first-search (BF) methods suffer
tactics and states have been released. We also revealed              from an explosion of the search space, rendering it inferior
more facts about the expert iteration process, especially the        under large sampling budgets. In contrast, critic-guided
efficacy of our CG method.                                           (CG) methods are capable of finding longer solutions. The
                                                                     average length of solutions found by the BF method is
Scaling CPU/GPU Computation in Expert Iteration.                     1.66, whereas the same indicator is 4.44 for the CG method,
The search process involves a collaboration of CPU and               demonstrating a significant improvement in deeper reason-
GPU resources. Given the fixed amount of active GPUs and             ing abilities. The distribution of proofs during our expert

                                                                 6
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

                            Table 2: Pass rates on the ProofNet (Azerbayev et al., 2023a) dataset.

                                                                                          ProofNet
                          Method                                      Pass
                                                                                  valid     test      all
                          ReProver (Yang et al., 2024)              -               -     -  13.8%
                                                                1 × 3200         22.0% 21.5% 21.8%
                          Deepseek-Prover-V1.5-RL
                                                                4 × 6400         25.4% 25.3% 25.3%
                          InternLM2-StepProver                1 × 32 × 100          -     -  18.1%
                                                              2 × 32 × 600          -        -       18.8%
                          InternLM2.5-StepProver-BF          32 × 32 × 600          -        -       21.1%
                                                             128 × 32 × 600         -        -       22.3%
                                                              2 × 32 × 600          -        -       17.4%
                          InternLM2.5-StepProver-CG          32 × 32 × 600          -        -       21.9%
                                                             128 × 32 × 600         -        -       23.9%
                                                              4 × 32 × 600          -        -       18.8%
                          InternLM2.5-StepProver-BF+CG       64 × 32 × 600          -        -       23.6%
                                                             256 × 32 × 600         -        -       27.0%


                          Table 3: Results on the Lean-workbook-plus (Ying et al., 2024a) dataset.

                                                                             Lean-workbook-plus
                     Method                        Pass
                                                                  Proved         Disproved           Total
                     InternLM2-StepProver   cumulative 7,909 (9.5%)         -       7,909 (9.5%)
                     InternLM2.5-StepProver cumulative 10,880 (13.1%) 3,195 (3.9%) 14,075 (17.0%)




Table 4: CPU time spent on the Lean-workbook(Ying et al.,
                    2024a) dataset.

     Problem State          Number        Total CPU days
     Proved/Disproved 14,075 (17.0%)  331 (1.5%)
     Remain unproven 68,200 (83.0%) 21,033 (98.5%)



iteration is shown in Fig. 5. To avoid the impact of redundan-
cies, only the shortest proof for each problem is considered
here. A nearly log-linear trend is observed in the distribution
of proof lengths found by best-first search method, while             Figure 4: The distribution of CPU search time per successful
the critic-guided proof method can find much longer proofs.           proof, which is defined as the total CPU resources spent on
However, 83% of the problems in the Lean-workbook re-                 searching the specific problem divided by the number of
main unproven, which can have longer proof lengths and                independent successful search trials. Only problems solved
require much more time to find them based on this estima-             are represented in the figure. 83% of the Lean-workbook
tion. We hope that our proposed method can help facilitate            problems that remain unproven are not depicted. BF and
the scaling of formal proof searching beyond the ”log-linear”         CG are analyzed independently.
boundaries.
                                                                      Another line of work is training to auto-regressively gener-
4. Related Work                                                       ate a whole proof based on a theorem statement from the
                                                                      model itself (Xin et al., 2024a;b) or translating from human
Automatic Theorem Proving. Automated theorem prov-                    informal proofs (Jiang et al., 2022; Wu et al., 2022; Wang
ing does not have a unified approach. A mainstream                    et al., 2024b). Regardless of the learning paradigm used,
paradigm is training a language model on tuples of (proof             most methods rely on expert iteration (Anthony et al., 2017)
state, next tactic), followed by a tree search to find proofs         to improve the model and require the prover model itself
(Polu & Sutskever, 2020; Polu et al., 2022; Lample et al.,            to determine the search direction. In this work, we train
2022; Yang et al., 2024; Lin et al., 2024; Wu et al., 2024).          our prover model to search under the guidance of an exter-

                                                                  7
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

                                                                      Limitations
                                                                      This work is mainly focused on contest-level math problems
                                                                      and pays less attention to other automated theorem-proving
                                                                      scenarios. Besides, we currently do not have a stable metric
                                                                      to measure critic models, which makes iteration of critic
                                                                      models difficult.

                                                                      Impact Statement
                                                                      This paper presents work whose goal is to advance the field
                                                                      of Machine Learning. There are many potential societal
                                                                      consequences of our work, none of which we feel must be
    Figure 5: The distribution of shortest proof length.              specifically highlighted here.

                                                                      References
nal critic model. The models are trained with a state-tactic
paradigm via expert iteration on a large-scale LEAN dataset.          Anthony, T., Tian, Z., and Barber, D. Thinking fast and slow
                                                                        with deep learning and tree search. In Guyon, I., Luxburg,
                                                                        U. V., Bengio, S., Wallach, H., Fergus, R., Vishwanathan,
Process-supervised Reasoning in Informal Mathematics.                   S., and Garnett, R. (eds.), Advances in Neural Information
Recently, numerous studies have shown that allowing an                  Processing Systems, volume 30. Curran Associates, Inc.,
external language model to evaluate the quality of reason-              2017. URL https://proceedings.neurips.
ing steps can boost performance on tasks such as informal               cc/paper_files/paper/2017/file/
math (Lightman et al., 2023; Zheng et al., 2025; Uesato                 d8e1344e27a5b08cdfd5d027d9b8d6de-Paper.
et al., 2022). Although this approach has proven effective,             pdf.
it often requires a significant amount of human-annotated
data or extensive computation (Luo et al., 2024; Wang et al.,         Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,
2024a). Furthermore, such methods are restricted to infor-              Radev, D., and Avigad, J. Proofnet: Autoformaliz-
mal language reasoning tasks. We propose a new scheme                   ing and formally proving undergraduate-level mathemat-
for training a tactic-level critic model that leverages the             ics, 2023a. URL https://arxiv.org/abs/2302.
correctness signal from the formal system.                              12433.

                                                                      Azerbayev, Z., Schoelkopf, H., Paster, K., Santos, M. D.,
5. Conclusion                                                           McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and
                                                                       Welleck, S. Llemma: An open language model for math-
In this paper, we presented critic-guided search, a novel
                                                                        ematics. arXiv preprint arXiv:2310.10631, 2023b.
approach that significantly enhances the theorem proving
capabilities of prover language models in formal mathemat-
                                                                      Cai, Z., Cao, M., Chen, H., Chen, K., Chen, K., Chen, X.,
ics by using an external critic model to rerank intermediate
                                                                        Chen, X., Chen, Z., Chen, Z., Chu, P., Dong, X., Duan,
Lean states. Our method begins with training initial critic
                                                                        H., Fan, Q., Fei, Z., Gao, Y., Ge, J., Gu, C., Gu, Y., Gui,
models from the trajectories of prior prover models to pre-
                                                                        T., Guo, A., Guo, Q., He, C., Hu, Y., Huang, T., Jiang, T.,
dict preference information between Lean states. We further
                                                                        Jiao, P., Jin, Z., Lei, Z., Li, J., Li, J., Li, L., Li, S., Li, W.,
improved the prover and the critic in tandem using expert
                                                                        Li, Y., Liu, H., Liu, J., Hong, J., Liu, K., Liu, K., Liu, X.,
iteration, fine-tuning the models on correct proof trajectories
                                                                        Lv, C., Lv, H., Lv, K., Ma, L., Ma, R., Ma, Z., Ning, W.,
that the prover model samples and verifies using the Lean
                                                                        Ouyang, L., Qiu, J., Qu, Y., Shang, F., Shao, Y., Song, D.,
solver. Our contributions include the introduction of the the-
                                                                        Song, Z., Sui, Z., Sun, P., Sun, Y., Tang, H., Wang, B.,
orem proving dataset Lean-Workbook-Plus, demonstrating
                                                                        Wang, G., Wang, J., Wang, J., Wang, R., Wang, Y., Wang,
that critic-guided search can further improve search depth,
                                                                        Z., Wei, X., Weng, Q., Wu, F., Xiong, Y., Xu, C., Xu,
and achieving new results on the miniF2F-test benchmark,
                                                                        R., Yan, H., Yan, Y., Yang, X., Ye, H., Ying, H., Yu, J.,
increasing the pass rate from 54.5% to 65.9%.
                                                                        Yu, J., Zang, Y., Zhang, C., Zhang, L., Zhang, P., Zhang,
These advancements not only improve the performance of                  P., Zhang, R., Zhang, S., Zhang, S., Zhang, W., Zhang,
automated theorem proving, but also offer concrete guid-                W., Zhang, X., Zhang, X., Zhao, H., Zhao, Q., Zhao, X.,
ance for future developments in automated mathematical                  Zhou, F., Zhou, Z., Zhuo, J., Zou, Y., Qiu, X., Qiao, Y.,
reasoning.                                                              and Lin, D. Internlm2 technical report, 2024.

                                                                  8
                 InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S. Proof         Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai,
  artifact co-training for theorem proving with language                  M., Guez, A., Lanctot, M., Sifre, L., Kumaran, D., Grae-
  models. arXiv preprint arXiv:2102.06203, 2021.                          pel, T., et al. Mastering chess and shogi by self-play
                                                                         with a general reinforcement learning algorithm. arXiv
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,          preprint arXiv:1712.01815, 2017.
   M., Lacroix, T., Wu, Y., and Lample, G. Draft, sketch,
   and prove: Guiding formal theorem provers with informal             Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,
   proofs. arXiv preprint arXiv:2210.12283, 2022.                       Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-
                                                                         ing math word problems with process- and outcome-
Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,                  based feedback, 2022. URL https://arxiv.org/
  Hayat, A., Lavril, T., Ebner, G., and Martinet, X. Hyper-              abs/2211.14275.
  tree proof search for neural theorem proving. Advances in
  neural information processing systems, 35:26337–26349,               Wang, P., Li, L., Shao, Z., Xu, R. X., Dai, D., Li, Y.,
  2022.                                                                 Chen, D., Wu, Y., and Sui, Z. Math-shepherd: Ver-
                                                                        ify and reinforce llms step-by-step without human an-
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,              notations, 2024a. URL https://arxiv.org/abs/
  B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and              2312.08935.
  Cobbe, K. Let’s verify step by step, 2023. URL https:
  //arxiv.org/abs/2305.20050.                                          Wang, R., Zhang, J., Jia, Y., Pan, R., Diao, S., Pi, R., and
                                                                        Zhang, T. Theoremllama: Transforming general-purpose
Lin, H., Sun, Z., Yang, Y., and Welleck, S. Lean-star:                  llms into lean4 experts, 2024b. URL https://arxiv.
  Learning to interleave thinking and proving, 2024. URL                org/abs/2407.03203.
  https://arxiv.org/abs/2407.10040.
                                                                       Wu, Y., Jiang, A. Q., Li, W., Rabe, M., Staats, C., Jam-
Luo, L., Liu, Y., Liu, R., Phatale, S., Guo, M., Lara, H.,              nik, M., and Szegedy, C. Autoformalization with large
  Li, Y., Shu, L., Zhu, Y., Meng, L., Sun, J., and Rastogi,             language models. Advances in Neural Information Pro-
  A. Improve mathematical reasoning in language models                  cessing Systems, 35:32353–32368, 2022.
  by automated process supervision, 2024. URL https:
  //arxiv.org/abs/2406.06592.                                          Wu, Z., Wang, J., Lin, D., and Chen, K. Lean-github:
                                                                        Compiling github lean repositories for a versatile lean
mathlib Community, T. The lean mathematical library. In                 prover, 2024. URL https://arxiv.org/abs/
 Proceedings of the 9th ACM SIGPLAN International                       2407.17227.
 Conference on Certified Programs and Proofs, CPP
 2020, pp. 367–381, New York, NY, USA, 2020. Associa-                  Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B.,
 tion for Computing Machinery. ISBN 9781450370974.                       Ruan, C., Li, W., and Liang, X. Deepseek-prover: Ad-
 doi: 10.1145/3372885.3373824. URL https://doi.                          vancing theorem proving in llms through large-scale
 org/10.1145/3372885.3373824.                                            synthetic data, 2024a. URL https://arxiv.org/
                                                                         abs/2405.14333.
Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wain-
 wright, C. L., Mishkin, P., Zhang, C., Agarwal,                       Xin, H., Ren, Z. Z., Song, J., Shao, Z., Zhao, W., Wang,
  S., Slama, K., Ray, A., Schulman, J., Hilton, J.,                      H., Liu, B., Zhang, L., Lu, X., Du, Q., Gao, W., Zhu,
  Kelton, F., Miller, L. E., Simens, M., Askell, A.,                     Q., Yang, D., Gou, Z., Wu, Z. F., Luo, F., and Ruan,
 Welinder, P., Christiano, P. F., Leike, J., and Lowe,                   C. Deepseek-prover-v1.5: Harnessing proof assistant
  R. J. Training language models to follow instruc-                      feedback for reinforcement learning and monte-carlo tree
  tions with human feedback. ArXiv, abs/2203.02155,                      search. 2024b. URL https://arxiv.org/abs/
  2022. URL https://api.semanticscholar.                                 2408.08152.
  org/CorpusID:246426909.                                              Xu, Y., Liu, X., Liu, X., Hou, Z., Li, Y., Zhang, X., Wang,
Pfenning, F. Automated theorem proving. Lecture notes,                   Z., Zeng, A., Du, Z., Zhao, W., Tang, J., and Dong, Y.
  March, 2004.                                                           Chatglm-math: Improving math problem-solving in large
                                                                         language models with a self-critique pipeline, 2024. URL
Polu, S. and Sutskever, I. Generative language model-                    https://arxiv.org/abs/2404.02893.
  ing for automated theorem proving. arXiv preprint
  arXiv:2009.03393, 2020.                                              Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
                                                                         Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin, I.,             Leandojo: Theorem proving with retrieval-augmented
  and Sutskever, I. Formal mathematics statement curricu-                language models. Advances in Neural Information Pro-
  lum learning. arXiv preprint arXiv:2202.01344, 2022.                   cessing Systems, 36, 2024.

                                                                   9
                InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and Chen, K.
  Lean workbook: A large-scale lean problem set formal-
  ized from natural language math problems, 2024a. URL
  https://arxiv.org/abs/2406.03847.
Ying, H., Zhang, S., Li, L., Zhou, Z., Shao, Y., Fei, Z.,
  Ma, Y., Hong, J., Liu, K., Wang, Z., Wang, Y., Wu, Z.,
  Li, S., Zhou, F., Liu, H., Zhang, S., Zhang, W., Yan,
  H., Qiu, X., Wang, J., Chen, K., and Lin, D. Internlm-
  math: Open math large language models toward verifiable
  reasoning, 2024b. URL https://arxiv.org/abs/
  2402.06332.
Zheng, C., Zhang, Z., Zhang, B., Lin, R., Lu, K., Yu, B.,
  Liu, D., Zhou, J., and Lin, J. Processbench: Identifying
  process errors in mathematical reasoning, 2025. URL
  https://arxiv.org/abs/2412.06559.
Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2021.




                                                              10
                InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

A. Training details
Prover Model Our prover model is built upon InternLM-math-plus-7B (Ying et al., 2024b). We used the same training
setting when we performed the expert iteration process: We used a global batch size of 512 and a learning rate of 2 × 10−5 .
We fine-tuned for 2 epochs to obtain the SFT model. For the learning rate, we used a warm-up in the first 3% steps, followed
by a cosine schedule decaying to zero. The entire expert iteration process generated 2.19 billion tokens of data, with the
final iteration taking approximately 14 hours on 32 A800 GPUs.




Critic Model We initialize the critic model from InternLM2-Chat-1 8b-sft2 (Cai et al., 2024) and fine-tune it for one
epoch. We create preference pairs among miniF2F-valid (Zheng et al., 2021), Mathlib (mathlib Community, 2020), and
Lean-Workbook-Plus (Ying et al., 2024a) using best-first-search. The final-round data includes 454K pairs where we have
removed duplicate pairs and reduced the number of pairs containing no goals to 10% of their original count. We train
critic models with 8 A800 GPUs. We evaluate our critic model using preference pairs generated on the miniF2F-test with
6510 pairs. We use the accuracy metric defined as the proportion of correctly predicted positive and negative pairs. The
model achieved an accuracy of 78.0%, demonstrating its preliminary ability to distinguish between positive and negative
pairs in the proof tree.

B. Case studies
Here we list interesting cases proved by InternLM2.5-StepProver from different datasets.




    Case: Lean-workbook

    Natural Language problem: For natural numbers m and n, if (mn + m + n) mod 6 = 4, then 12 | mn.

    theorem lean_workbook_plus_74374 (m n : N) : (m * n + m + n) % 6 = 4 → 12 | m * n
         := by
    simp [Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
    rw [← Nat.mod_add_div m 6, ← Nat.mod_add_div n 6]
    have h1 : m % 6 < 6 := Nat.mod_lt _ (by norm_num)
    have h2 : n % 6 < 6 := Nat.mod_lt _ (by norm_num)
    interval_cases m % 6 <;> interval_cases n % 6 <;> simp_all (config := {decide :=
        true})
    all_goals ring_nf; simp [Nat.dvd_iff_mod_eq_zero, Nat.mul_mod, Nat.add_mod,
        Nat.mod_mod]




InternLM2.5-StepProver successfully addresses the problem by imposing constraints on the range of variables and then
solving it directly using enumeration techniques. This example illustrates the distinction between formal and informal
reasoning styles.
   2
       https://huggingface.co/internlm/internlm2-chat-1_8b-sft

                                                            11
                InternLM2.5-StepProver: Advancing Automated Theorem Proving via Critic-Guided Search

    Case: miniF2F: mathd algebra 31
                                   r
                                                    √
                                            q   p
    Natural Language problem: If       x+    x + x + x + · · · = 9, find x. Show that it is 72.

    theorem mathd_algebra_31 (x : NNReal) (u : N → NNReal) (h0 : ∀ n, u (n + 1) =
        NNReal.sqrt (x + u n))
        (h1 : Filter.Tendsto u Filter.atTop (N 9)) : 9 = NNReal.sqrt (x + 9) := by
        have h2 := h1 .const_add x
        have h3 : Filter.Tendsto (fun k => NNReal.sqrt (x + u k)) Filter.atTop (N
        (NNReal.sqrt (x + 9))) :=
          NNReal.continuous_sqrt.continuousAt.tendsto.comp h2
        have h4 : (fun k : N => NNReal.sqrt (x + u k)) = fun k : N => u (k + 1) := by
          ext k
          rw [h0 ]
        have h5 : Filter.Tendsto (fun k : N => u (k + 1)) Filter.atTop (N (NNReal.sqrt
        (x + 9))) :=
          h4 ▷ h 3
        have h6 : Filter.Tendsto (fun k => u (k + 1)) Filter.atTop (N 9) := h1 .comp
        (Filter.tendsto_add_atTop_nat 1)
        exact tendsto_nhds_unique h6 h5


This case demonstrates how InternLM2.5-StepProver solves a problem whose formalized version is significantly harder
than
r the     informal one. The informal solution of this problem is not rigorous, which jumps from the equation
      q       p     √                  √
   x + x + x + x + · · · = 9 to x + 9 = 9, involving a substitution that is intuitive but risky. The formalized
version of this problem uses series and limitations to redefine the problem. This is a case where formal reasoning detaches
from informal reasoning. In such cases, it is hard to say that the involvement of informal CoT has any benefit to the
problem. InternLM2.5-StepProver provides a solid proof of the problem without the augmentation of informal information,
successfully solving the problem.

    Case: ProofNet: Munkers 31 2
    Natural Language problem: Show that if X is normal, every pair of disjoint closed sets has neighborhoods whose
    closures are disjoint.

    theorem exercise_Munkers_31_2 {X : Type*}
    [TopologicalSpace X] [NormalSpace X] {A B : Set X}
    (hA : IsClosed A) (hB : IsClosed B) (hAB : Disjoint A B) :
    ∃ (U V : Set X), IsOpen U ∧ IsOpen V ∧ A ⊆ U ∧ B ⊆ V ∧ closure U ∩ closure V = ∅ :=
         by
    obtain ⟨U0 , V0 , hU0 , hV0 , hA0 , hB0 , hAB0 ⟩ := normal_separation hA hB hAB
    obtain ⟨U, hU1 , hU2 , hU3 ⟩ := normal_exists_closure_subset hA hU0 hA0
    obtain ⟨V, hV1 , hV2 , hV3 ⟩ := normal_exists_closure_subset hB hV0 hB0
    refine ⟨U, V, hU1 , hV1 , hU2 , hV2 ,?_⟩
    exact (hAB0 .mono hU3 hV3 ).eq_bot


InternLM2.5-StepProver has an improved capability of solving undergraduate problems, even though it was not fine-tuned
on such data distributions. InternLM2.5-StepProver utilizes premises from the Mathlib to construct valid closure subsets,
effectively demonstrating its mathematical reasoning ability.




                                                             12
