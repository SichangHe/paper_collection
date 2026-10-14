                                            BFS-Prover: Scalable Best-First Tree Search for LLM-based Automatic
                                                                      Theorem Proving
                                                                                                                                      †
                                                                Ran Xin1,*        Chenguang Xi1,*     Jie Yang2,*    Feng Chen 3,*,
                                                            Hang Wu2            Xia Xiao1     Yifan Sun1   Shen Zheng1         Kai Shen1
                                                   1                        2                                             3
                                                       ByteDance Seed           ByteDance Applied Machine Learning            Stanford University
                                                                    Correspondence: {ran.xin, shen.kai}@bytedance.com

                                                                  Abstract                           enables the generation of machine-verified proofs
                                                Recent advancements in large language mod-
                                                                                                     for complex mathematical propositions, ensuring
                                                els (LLMs) have spurred growing interest in          logical correctness (Moura and Ullrich, 2021; Polu
arXiv:2502.03438v3 [cs.AI] 9 Oct 2025




                                                automatic theorem proving using Lean4, where         and Sutskever, 2020). Despite the remarkable suc-
                                                effective tree search methods are crucial for        cess of LLMs in natural language mathematics
                                                navigating the underlying large proof search         and reasoning tasks (Lewkowycz et al., 2022; Ope-
                                                spaces. While the existing approaches primar-        nAI, 2023), theorem proving in formal languages
                                                ily rely on value functions and/or Monte Carlo       presents unique challenges (Yang et al., 2024b; Wu
                                                Tree Search (MCTS), the potential of simpler
                                                                                                     et al., 2022; He et al., 2024; Wang et al., 2023,
                                                methods like Best-First Tree Search (BFS) re-
                                                mains underexplored. In this paper, we investi-      2024; Lin et al., 2024; Xin et al., 2024a). Un-
                                                gate whether BFS can achieve competitive per-        like informal reasoning, formal systems require
                                                formance in large-scale theorem proving tasks.       strict adherence to syntax and semantics, as well as
                                                We present BFS-Prover, a scalable expert itera-      the ability to generate valid steps within a highly
                                                tion framework, featuring three key innovations.     constrained formal framework. Additionally, the
                                                First, we implement strategic data filtering at      action (tactic) space in ATP is vast, as each proof
                                                each expert iteration round, excluding problems      state can lead to numerous potential tactics, making
                                                solvable via beam search node expansion to fo-
                                                cus on harder cases. Second, we improve the
                                                                                                     the search process for valid proofs computationally
                                                sample efficiency of BFS through Direct Pref-        intensive (Polu et al., 2022).
                                                erence Optimization (DPO) applied to state-
                                                tactic pairs automatically annotated with com-       Tree search algorithms are fundamental to ATP,
                                                piler error feedback, refining the LLM’s pol-        allowing policy models to navigate large and com-
                                                icy to prioritize productive expansions. Third,      plex proof space efficiently (Polu and Sutskever,
                                                we employ length normalization in BFS to             2020). Among these methods, Monte Carlo Tree
                                                encourage exploration of deeper proof paths.
                                                                                                     Search (MCTS) (Coulom, 2006) has gained popu-
                                                BFS-Prover achieves a state-of-the-art score of
                                                72.95% on the MiniF2F test set and therefore         larity due to its ability to balance exploration and
                                                challenges the perceived necessity of complex        exploitation using value functions (critic models)
                                                tree search methods, demonstrating that BFS          or intrinsic rewards (Browne et al., 2012; Silver
                                                can achieve competitive performance when             et al., 2016). MCTS has demonstrated remarkable
                                                properly scaled. To facilitate further research      success in AlphaZero-style frameworks for games
                                                and development in this area, we have open-          like chess and Go (Silver et al., 2017), where the
                                                sourced our model at https://huggingface.            underlying state spaces are vast but terminal states
                                                co/ByteDance-Seed/BFS-Prover-V1-7B.
                                                                                                     are well-defined. However, applying MCTS and/or
                                        1       Introduction                                         value functions to ATP comes with distinct com-
                                                                                                     plications. While games have clear winning and
                                        Automatic theorem proving (ATP) in formal lan-               losing conditions, proof search lacks such definitive
                                        guages has recently become a critical benchmark              end states: a proof attempt can theoretically con-
                                        for evaluating the reasoning capabilities of large           tinue indefinitely until a proof or counterexample is
                                        language models (LLMs). By encoding mathemat-                found, making it challenging to assess intermediate
                                        ical problems into formal systems like Lean4, ATP            progress (Han et al., 2021; Lample et al., 2022).
                                            * Key contributors.                                      Additionally, ATP involves a much larger and more
                                            †
                                                Work done during an internship at ByteDance Seed.    dynamic branching factor, sparse and delayed feed-
back, and an open-ended reasoning process. These               ing tree search. From a given proof state, each
differences highlight the unique demands of ATP                preference pair consists of a positive tactic,
and advocate the need for specialized adaptations              which lies on the proof path, and a negative
of search methods to address its complexities.                 tactic, which leads to a Lean compiler error.
                                                               DPO sharpens policy’s distribution, enabling
Best-First Tree Search (BFS) (Pearl, 1984) offers a
                                                               it to avoid unproductive tactics and thereby
simpler and more lightweight alternative to MCTS
                                                               improving the sample efficiency of BFS.
by prioritizing expansions based on accumulated
log probabilities from the current node to the root.         • Length normalization for deeper explo-
While its straightforward nature and computational             ration. We incorporate a length-normalized
simplicity make it attractive, BFS is often consid-            scoring function in BFS to mitigate its inher-
ered suboptimal for theorem proving in the existing            ent bias against deeper reasoning paths. By
literature (Wu et al., 2024a; Li et al., 2024b; Xin            normalizing log probabilities relative to path
et al., 2024b) due to the following hypothesis:                length, BFS can explore deeper proof paths
                                                               more effectively, enabling it to solve theorems
   • Lack of efficient exploration: BFS prioritizes            requiring long tactic chains.
     high-probability paths, overlooking less likely
     but valid solutions. Without exploration mech-          • Empirical results on MiniF2F. BFS-Prover
     anisms like upper confidence bounds or value              achieves an accumulative score of 72.95%
     functions, it struggles to balance exploiting             on the MiniF2F test set, surpassing all state-
     promising nodes and exploring diverse paths.              of-the-art theorem provers in the literature,
                                                               including DeepSeek-Prover-V1.5 (Xin et al.,
   • Bias against deep reasoning paths: BFS’s re-              2024b), InternLM2.5-StepProver (Wu et al.,
     liance on cumulative log probabilities intrinsi-          2024a), and HunyuanProver (Li et al., 2024b).
     cally penalizes longer paths, as deeper expan-            This result underscores that BFS-Prover can
     sions tend to accumulate lower scores. This               scale to competitive levels in automated theo-
     bias makes BFS less effective for theorems re-            rem proving while maintaining a lightweight
     quiring deep proofs, where intermediate states            design that avoids the complexities of MCTS
     may seem unpromising but are essential for                and value functions.
     finding a solution.
                                                         Roadmap. The remainder of this paper is orga-
1.1   Our Contributions                                  nized as follows. Section 2 gives an overview of the
This paper challenges the prevailing perception that     BFS-Prover system, detailing the expert iteration
BFS is inherently unsuitable for large-scale ATP.        framework, data filtering, DPO for policy refine-
We present the BFS-Prover system, which trans-           ment, and length normalization in BFS. Section 3
forms BFS into a simple yet powerful algorithm           describes practical implementation and experimen-
through targeted scaling strategies. Our key contri-     tal results on the MiniF2F benchmark against lead-
butions are as follows.                                  ing prover systems. Section 4 concludes the paper.

   • Expert iteration with self-filtering. We de-        2     The BFS-Prover system
     velop an expert iteration (Anthony et al., 2017)
                                                         In this section, we detail the BFS-Prover system
     framework that strategically filters out prob-
                                                         design; see Fig. 1 for an illustration.
     lems solvable by beam search (Steinbiss et al.,
     1994) node expansions in each round. This           2.1    Lean4 Environment and Policy LLM
     filtering is critical as it directs training data
                                                         We adopt LeanDojo (Yang et al., 2024c) as an inter-
     accumulation towards harder theorems. As ex-
                                                         active Python interface for Lean4 integration within
     pert iteration progresses, the policy LLM con-
                                                         BFS-Prover. It transforms Lean4 into a gym-like
     tinuously improves, learning a diverse range
                                                         environment (Brockman, 2016), facilitating interac-
     of tactics and deeper proofs via BFS.
                                                         tion between the policy LLM and the formal proof
   • Direct preference optimization (DPO) from           assistant. Specifically, LeanDojo manages state
     compiler feedback. We use DPO (Rafailov             transitions by executing tactics generated by the
     et al., 2024) to refine the policy LLM by lever-    policy LLM in the Lean4 compiler. If a tactic can-
     aging preference pairs naturally generated dur-     not be executed, LeanDojo captures and returns the
                                                     Proof state update



                     LeanDojo                                                                                             Language
                    Environment                                                      Tactic generation                  Model as Policy


                            Root Node    1
                                                                                          SFT Data
                                                     Tactics
                                                                                            1           3       A
                                3                      2
                                                                                           ………
                                                                  Tactics


                                A       B
                                                                                          DPO Data
                         Best-First                                                                         3
                                             1   2         3     …
                        Search Order
                                                                                                            >
                          Identified         1             3           A
                          Proof Path
                                                                                                 A                  B
                       a) Best-First Tree Search for                                        ………
                       Automatic Theorem Proving                                           b) Training Data Generation
                  Proof Finish Nodes    Error Nodes            Intermediate Nodes    Unexplored Nodes                     Diﬀerent Tactics




Figure 1: An overview of BFS-Prover. The figure illustrates two key components: a) Best-First Tree Search (BFS)
mechanism for automatic theorem proving, showing how the system explores proof paths by expanding nodes
based on accumulated probabilities, with different node types (proof finish, error, intermediate, and unexplored)
represented via color coding. The identified proof path demonstrates a successful state-tactic sequence. b) The
training data accumulation process, depicting how the system leverages both successful proofs for Supervised
Fine-Tuning (SFT) and compiler error feedback for Direct Preference Optimization (DPO). The system integrates
LeanDojo as a python interface for Lean4 and employs a language model as the policy network for tactic generation.


corresponding error messages, providing critical                                        • L is the total length of the path from the root
feedback for DPO to refine the policy LLM.                                                to the current state sL , and

2.2   Length-Normalized Best-First Tree                                                 • α ∈ [0, 1] is a tunable length normalization
      Search                                                                              parameter.
BFS-Prover incorporates a version of Best-First                                     This scoring mechanism, combined with a tunable
Tree Search (BFS) to navigate the vast state-tactic                                 node expansion width, enables BFS to dynamically
space of proof search. The BFS engine maintains                                     allocate computational resources across the proof
a priority queue of proof nodes (states), where the                                 space, balancing the trade-off between exploration
priority of each node (state) is defined by a length-                               and exploitation. For example, increasing α and/or
normalized scoring heuristic:                                                       reducing the expansion width drives the search sys-
                           PL−1                                                     tem toward exploring deeper paths, encouraging
                                t=0 log p(at |st )                                  the discovery of complex proofs that may require a
         score(sL ) =                              ,                       (1)
                                     Lα                                             long chain of tactics.
where we have the following:                                                        At each node expansion step, the policy LLM gen-
   • st represents the proof state at step t,                                       erates, via a certain sampling mechanism, a list of
                                                                                    tactics which correspond to edges in the proof tree.
   • at is the tactic applied at step t,                                            LeanDojo then executes these sampled tactics in
                                                                                    Lean4 compiler and returns their outcomes. For
   • {(st , at ) : t = 0, 1, ..., L − 1} denotes the
                                                                                    each tactic application, three outcomes are possi-
     proof path formed by applied tactics and state
                                                                                    ble: (1) if the tactic results in a valid proof state, a
     transitions,
                                                                                    regular tree node is created and added to the node
   • p(at |st ) is the model’s predicted probability                                queue; (2) if the tactic completes the proof, a proof
     of applying tactic at at state st ,                                            finish node is created and the proof is returned; (3)
otherwise, a terminal error node is generated to               stead of re-training the policy LLM using SFT,
represent an invalid path.                                     DPO can be applied as an alternative method
                                                               to refine the current policy model by leverag-
2.3   Expert Iteration                                         ing the on-policy Lean error data collected in
BFS-Prover employs an expert iteration pipeline                step 2. Along the proof path, certain gener-
to iteratively enhance the policy LLM’s ability to             ated tactics, expanded from a proof state but
navigate complex proof spaces. Given a corpus of               not part of the verified proof path, result in
unsolved formal statements in Lean4, each round                Lean compiler errors. These erroneous tactics
of expert iteration consists of the following steps.           naturally serve as negative examples when
                                                               compared to their corresponding valid proof
  1. Beam Search Filtering: Formal statements
                                                               tactics, forming preference tuples. Specifi-
     that can be proved through BFS with beam
                                                               cally, for a state s on a proof path, we may
     search node expansions are identified. These
                                                               form pairs (aw , al ) where aw is the tactic on
     statements are then removed from the corpus
                                                               the proof path and al is an error-causing tactic
     and their corresponding proof data, although
                                                               expanded from s if exists; see Fig. 1 for an
     new, is deliberately not added to the cumu-
                                                               illustration. The DPO loss LDPO (θ) (Rafailov
     lative training dataset. Beam search, being
                                                               et al., 2024) is then defined as
     deterministic, reliably selects the most con-
     fident tactics produced by the current policy             −E(s,aw ,al ) [log σ(β(rθ (s, aw ) − rθ (s, al )))],
     LLM. Therefore, proofs solvable under this
     approach are considered relatively simple, as             where the differemce, i.e., implicit reward,
     they align closely with the strengths of the              rθ (s, a) = log(pθ (a|s)) − log(pref (a|s)) is
     current BFS-Prover system. By strategically               the log probability ratio between the policy
     filtering out these simpler proofs, the training          model pθ and reference model pref , β is a KL
     data corpus is iteratively enriched with more             regularization parameter controlling the sharp-
     challenging and diverse examples. This itera-             ness of the learned preferences, and σ is the
     tive refinement ensures that the policy LLM               sigmoid function. By explicitly incorporating
     is progressively exposed to increasingly com-             these negative signals that are absent in SFT,
     plex reasoning patterns, thereby enhancing                DPO sharpens the LLM’s output distribution,
     its capability to address harder theorems in              thereby improving the sample efficiency and
     subsequent iterations.                                    scalability of BFS within the expert iteration
                                                               framework.
  2. Data Collection: We then perform BFS with
     temperature-based sampling expansions to            This expert iteration pipeline enables the policy
     search for proofs of the remaining unproved         LLM to continually enhance its ability to generate
     formal statements in the corpus. Upon com-          productive tactics while adapting to progressively
     pletion, the system collects all valid (proof       more challenging proof scenarios as the training
     state, tactic) pairs encountered along success-     data corpus grows.
     ful proof paths, which are subsequently added
                                                         3     Practical Implementation and
     to the cumulative training dataset. The corre-
     sponding proved statements are then removed
                                                               Benchmark Results
     from the corpus. Additionally, invalid tac-         In this section, we discuss practical implementation
     tics that result in Lean compiler errors are        details of the BFS-Prover system and present its
     recorded as on-policy negative examples to          benchmark results on MiniF2F test. Throughout
     support DPO refinement.                             all experiments, we use Lean 4.7.0.
  3. Supervised Fine-Tuning (SFT): After each            3.1    Model, Data, and Training Setup
     data collection phase, a new policy LLM is
                                                         Base model and initial training data. For illus-
     trained by performing SFT on a base model us-
                                                         tration purposes, we use Qwen2.5-Math-7B (Yang
     ing the full accumulated training data corpus,
                                                         et al., 2024a) as the base model for fine-tuning
     which consists of all (proof state, tactic) pairs
                                                         the policy LLM in BFS-Prover. In order to prop-
     generated during previous expert iterations.
                                                         erly initialize the expert iteration process, we lever-
  4. Direct Preference Optimization (DPO): In-           age proof data extracted by LeanDojo (Yang et al.,
2024c) from Mathlib (Moura and Ullrich, 2021),          3.2   Distributed Best-First Search
which serves as the cold-start dataset. As expert             Infrastructure
iteration progresses, we further incorporate state-     To enable efficient large-scale parallel proof search,
tactic datasets from Lean-Github (Wu et al., 2024b),    we implement a distributed system using Ray for
a compilation of Lean4 repositories from GitHub,        distributed theorem proving across multiple ma-
and Lean-Workbook (Ying et al., 2024), which fo-        chines, each equipped with 8 A100 80GB GPUs
cuses on Olympia-level algebra and analysis. These      and 128 CPU cores. The target theorems are evenly
datasets span a diverse range of mathematical top-      divided across machines, with each machine run-
ics and formal reasoning tasks, equipping the policy    ning an independent proving pipeline. The system
model with the foundational skills necessary for        is composed of three main components:
effective tactic generation and proof navigation.
                                                           • GPU-Based Policy LLM Pool: Each local
Formal statement corpus. To construct our ex-                machine deploys 8 instances of our 7B policy
pert iteration data corpus, we autoformalize the             LLM, each powered by an asynchronous vLLM
NuminaMath-CoT dataset (Li et al., 2024a) using              engine running on a dedicated A100 GPU.
proprietary tools. We augment this with unproven             These instances form a shared pool that pro-
theorems from Mathlib and formal statements from             cesses concurrent tactic generation requests.
Lean-Workbook. The resulting corpus comprises
approximately 900,000 formal mathematical state-           • CPU-Based Prover Pool: Each machine runs
ments without proofs, providing a comprehensive              96 concurrent prover instances, reserving re-
foundation for expert iteration.                             maining CPU cores for standard system op-
                                                             erations. Each prover instance executes inde-
Training setup and procedures. At each expert it-            pendent BFS runs for its assigned theorems.
eration round, we obtain a new policy LLM through            In order to achieve balanced GPU utilization,
either SFT or DPO based on the procedures de-                provers distribute their requests across the pol-
scribed in Section 2.3. For SFT, we conduct train-           icy LLM instances in a round-robin fashion
ing over 3 epochs using cosine learning rate decay,          based on their index modulo 8. Each prover
initializing at 2 × 10−5 and decaying to 1 × 10−6 ,          asynchronously interacts with its assigned pol-
with a global batch size of 128. For DPO, we per-            icy LLMs and LeanDojo environments.
form a single epoch of training with cosine learn-
ing rate decay, beginning at 5 × 10−6 and decaying         • Asynchronous interactions: The overall dis-
to 5 × 10−7 , utilizing a global batch size of 16,           tributed search system leverages asyncio to
while maintaining a KL regularization parameter of           manage the high-concurrency workflow be-
β = 10. All training is performed on A100 80GB               tween provers and policy LLMs. Both the pol-
GPUs. The selection between SFT and DPO at                   icy LLM and prover pools are implemented as
each expert iteration round depends on the volume            Ray actors, enabling dynamic resource man-
of data generated in each iteration: SFT is imple-           agement through Ray’s runtime system. To en-
mented when substantial new data has been gen-               sure system responsiveness, we enforce time-
erated during the past iteration(s), whereas DPO             out thresholds for both tactic execution (via
is preferred for iterations with limited data genera-        LeanDojo) and model inference (via vLLM).
tion, leveraging its sample efficiency through the
                                                        This distributed infrastructure design achieves near-
incorporation of negative examples.
                                                        linear scaling through efficient theorem distribu-
BFS configuration in expert iteration. We set the       tion across machines while maximizing hardware
length normalization parameter α to 0.0 through-        utilization within each machine without cross-
out, to minimize inductive bias in expert iteration.    machine communication overhead.
During the beam search filtering stage, we utilize a
beam width of 32 to identify easily solvable theo-      3.3   Distribution Shift in Expert Iteration
rems. In the subsequent data collection phase, we       In this subsection, we discuss and illustrate how dis-
employ temperature-based sampling with a temper-        tribution shifts emerge at both the proof level and
ature of 1.0, nucleus sampling parameter 1.0, and       the tactic level throughout expert iteration, shed-
a sampling width of 2, 4, or 8 to explore diverse       ding light on the progressively improving capabili-
proof paths.                                            ties of BFS-Prover in theorem proving.
                                           Evolution of Proof Length Distribution




                                      Mean: 10.2



                                                         Mean: 16.7
                                                                               Sample Distribution from An Earlier Iteration
Percentage of Proofs (%)

                           10.0                                                Sample Distribution from A Later Iteration
                            7.5
                            5.0
                            2.5
                            0.0
                                  0   10                              20                    30                    40
                                                   Proof Length (Number of Tactics)
Figure 2: Sample evolution of proof length distribution across expert iteration rounds. The blue distribution shows a
sample distribution of proof lengths in an earlier iteration, with a mean of 10.2 tactics per proof and a concentration
between 6-12 tactics. The red distribution represents a sample from a later iteration, showing a clear shift toward
longer proofs with a mean of 16.7 tactics and a broader spread extending beyond 30 tactics. This shift illustrates the
growing capability of BFS-Prover to solve increasingly complex theorems requiring deeper reasoning chains.


Proof level. A critical indicator of the effective-                    BFS-Prover learns to generate more sophisticated
ness of a prover system, such as BFS-Prover, is its                    tactics while maintaining the capability to use sim-
ability to discover deep proofs. We define proof                       pler ones when appropriate. The preservation of
length as the number of tactics found by a system to                   tactic diversity is crucial for effective theorem prov-
complete a proof. We observe that the distribution                     ing, as different proof states require different levels
of proof length at each expert iteration round often                   of tactical complexity, from simple term rewriting
exhibits a Gaussian or mixture of Gaussians, reflect-                  to complex algebraic manipulations.
ing the diversity of theorem complexities within
the formal statement corpus. Intriguingly, as expert                   3.4     Results on MiniF2F
iteration progresses, the mean proof length tends                      In this subsection, we discuss BFS-Prover’s per-
to increase, indicating that BFS can find increas-                     formance on the MiniF2F test benchmark (Zheng
ingly deeper and more challenging proofs as the                        et al., 2021) that is a widely recognized dataset for
policy LLM improves; see Fig. 2 for an illustra-                       evaluating formal mathematics systems. MiniF2F
tion. This observation highlights the effectiveness                    is consisted of a diverse collection of formalized
of the expert iteration framework and the scalabil-                    competition-level mathematics problems. The pol-
ity of BFS, i.e., its ability to progressively tackle                  icy LLM checkpoint for tactic generation used for
more complex proofs by leveraging iterative policy                     evaluation was obtained by performing SFT on all
refinement and improved search capabilities.                           state-tactic pairs accumulated through 10 rounds of
                                                                       expert iteration pipeline of BFS-Prover, followed
Tactic level. Beyond proof-level evolution, we also
                                                                       by an additional round of DPO refinement using
observe interesting distributional shifts at the tac-
                                                                       Lean error signals as described in Section 2.3.
tic level throughout expert iteration; see Fig. 3. No-
tably, the policy LLM in the BFS-Prover system                         3.4.1     Comparison with the State of the Art
maintains a diverse range of tactic lengths without                    We now compare BFS-Prover developed in this
collapsing to a narrow distribution - a common fail-                   work against leading theorem provers in the lit-
ure mode in reinforcement learning where models                        erature, including DeepSeek-Prover-V1.5 (Xin
tend to converge to a limited set of high-reward                       et al., 2024b), InternLM2.5-StepProver (Wu et al.,
actions (Sutton, 2018). Instead, we observe a mod-                     2024a), and HunyuanProver (Li et al., 2024b).
erate but meaningful shift from very simple tactics
(1-10 tokens) towards more commonly used tac-                          Fixed tactic generation budget. We first evaluate
tical patterns (11-50 tokens). This shift suggests                     performance under a fixed tactic generation budget,
that through expert iteration, the policy LLM in                       defined as K × W × N , where K is the total num-
Percentage of Total Tactics (%)           -2.33%
                                                                          Tactic Token Distribution
                                   102
                                                   +1.27%                              Sample Distribution from An Earlier Iteration
                                   101                                                 Sample Distribution from A Later Iteration
                                                            +0.76%
                                   100                               +0.23%
                                                                              +0.06%
                                  10 1                                                 -0.01%            +0.01%
                                  10 2                                                          +0.00%

                                  10 3
                                          0

                                                 -20

                                                         -30

                                                                 -40

                                                                          -50

                                                                                   -60

                                                                                            -70

                                                                                                     -80

                                                                                                              -90

                                                                                                                          0

                                                                                                                         07
                                         1-1




                                                                                                                       -10

                                                                                                                      1-1
                                               11

                                                       21

                                                               31

                                                                        41

                                                                                 51

                                                                                          61

                                                                                                   71

                                                                                                            81

                                                                                                                     91

                                                                                                                    10
                                                                              Token Number Range
Figure 3: Sample evolution of tactic token length distribution across expert iteration rounds. The plot shows the
log-scaled percentage of tactics falling into different token length bins. We have two observations: (1) robustness
against mode collapse during expert iteration, evidenced by the maintained diversity across token lengths, and (2) a
gradual shift from an emphasis on very short tactics (1–10 tokens, decreasing by about 2.3%) to a higher prevalence
of moderate-length tactics (11–50 tokens, with incremental increases ranging from approximately 1.27% to 0.06%).
This evolution reflects the improved ability of BFS-Prover to generate more complex, informative tactics while still
retaining the capacity to produce concise ones when needed.


ber of passes, W is the expansion width, and N is                                      attempts is limited.
the maximum number of proof state expansions per
pass. This budget represents the total number of                                       3.4.2    Scaling Law of BFS and Advantage of
LLM inference calls required during proof search.                                               Negative Signals from DPO
During BFS proof search, BFS-Prover uses a sam-
pling temperature of 1.1, an expansion width of 2,                                     Finally, we investigate the search-time scaling law
and a length normalization factor of α = 0.5 de-                                       of BFS-Prover by examining how its performance
fined in (1) to maximize the variance of explored                                      on the MiniF2F test benchmark improves with
proof paths across different search attempts. As                                       increasing proof search passes and evaluate the
shown in Table 1, BFS-Prover achieves state-of-                                        advantage of applying DPO to learn from nega-
the-art performance under this setting without re-                                     tive signals in enhancing the system. We perform
quiring either a critic model or MCTS-based search.                                    a total of pass@4096 and evaluate intermediate
We note that the incorporation of a critic model                                       performance at pass@64, pass@128, pass@256,
effectively doubles the number of inference calls                                      pass@1024, and pass@2048, where the confidence
since each state expansion requires both policy and                                    band for each intermediate pass count is computed
value computations.                                                                    by sampling multiple pass@64 runs. The exper-
                                                                                       imental results are presented in Fig. 4, where x-
Accumulative results. In order to maximize po-                                         axis is in the log scale and the shaded region rep-
tential proof discovery, we conduct BFS searches                                       resents min-max range, i.e., the confidence band.
under multiple hyperparameter configurations and                                       In the following, we make several observations
aggregate the successful proofs. Specifically, we                                      about key characteristics of BFS scaling in formal
vary the BFS length normalization factor α defined                                     theorem proving. Here, SFT refers to supervised
in (1) over {0.0, 0.5, 1.0} to execute different ex-                                   fine-tuning performed on all state-tactic pairs accu-
ploration and exploitation trade-offs, while other                                     mulated through the expert iteration pipeline, while
parameter settings remain unchanged. This diverse                                      SFT+DPO indicates an additional round of DPO
search strategy allows BFS-Prover to accumula-                                         refinement applied on top of the SFT model using
tively achieve a score of 72.95% on the MiniF2F                                        on-policy negative examples from Lean4 compiler
test, setting a new state-of-the-art result in the for-                                feedback as described in Section 2.3. Both SFT and
mal theorem proving literature. See Fig. 4 for the                                     SFT+DPO employ the following BFS parameter
performance of BFS-Prover when the number of                                           configuration: a sampling temperature of 1.1, an
    Prover System                                    Critic     Search     Tactic Budget         MiniF2F-test
    Whole-Proof Generation Methods
    DeepSeek-Prover-V1.5 (Xin et al., 2024b)          No        MCTS       32 × 16 × 400             63.5%
    Tactic Step Proving Methods
    InternLM2.5-StepProver (Wu et al., 2024a)         Yes        BFS      256 × 32 × 600             65.9%
    HunyuanProver (Li et al., 2024b)                  Yes        BFS       600 × 8 × 400             68.4%
    BFS-Prover (this work)                            No         BFS      2048 × 2 × 600       70.83% ± 0.89%
    BFS-Prover (this work)                            No         BFS        accumulative            72.95%

Table 1: Comparison between BFS-Prover and leading theorem provers in the literature on the MiniF2F test set.
Each prover’s performance is evaluated using its reported tactic generation budget, which represents the total number
of inference calls during proof search. Note that DeepSeek-Prover-V1.5 is a whole-proof generation method and we
decompose its tactic budget for ease of comparison. BFS-Prover achieves state-of-the-art performance without
requiring a critic model (value function) and MCTS.

expansion width of 2, and a length normalization              rem proving with LLMs. Through the development
factor of α = 0.5.                                            of BFS-Prover, we argue that a carefully designed
                                                              BFS system with expert iteration which incorpo-
     • Both SFT and SFT+DPO training methods                  rates strategic data filtering, direct preference opti-
       exhibit logarithmic scaling as the number of           mization, and length normalization can exceed the
       proof search passes increases. Specifically,           performance of existing approaches while maintain-
       SFT improves from 64.58% to 70.38% and                 ing computational simplicity. Our empirical results
       SFT+DPO from 64.98% to 70.83% when scal-               on the MiniF2F benchmark, achieving a state-of-
       ing passes from 64 to 2048, showing consis-            the-art score of 72.95%, validate the scalability of
       tent but diminishing returns with doubled com-         this approach.
       putational budget.
                                                              The success of BFS-Prover has several implica-
     • The SFT+DPO training method consistently
                                                              tions for the field of ATP. First, it demonstrates that
       outperforms the SFT baseline, demonstrat-
                                                              algorithmic simplicity, when combined with care-
       ing the effectiveness of incorporating negative
                                                              ful scaling strategies, can outperform more com-
       feedback from Lean4 compiler errors. This
                                                              plex approaches. This finding suggests that future
       refinement enables the model to better distin-
                                                              research in ATP might benefit from focusing on re-
       guish between successful and unsuccessful
                                                              fining and scaling simpler methods rather than nec-
       proof strategies, leading to improved proof
                                                              essarily pursuing increasingly sophisticated archi-
       search efficiency and higher success rates.
                                                              tectures. Second, the observed logarithmic scaling
     • Examining the min-max ranges, both meth-               law of BFS performance with respect to computa-
       ods exhibit similar variance in performance            tional resources suggests that while additional com-
       (around 3-4% range). This indicates that while         putation consistently yields improvements, there
       DPO improves overall success rates, it main-           may be fundamental limitations to what can be
       tains comparable stability in proof search to          achieved through increased search alone. This ob-
       the SFT baseline.                                      servation motivates future research into methods
                                                              that can achieve better than logarithmic scaling.
4     Conclusion and Discussion
                                                              Limitations
This work shows that Best-First Search (BFS) can
scale efficiently and achieve state-of-the-art perfor-        While the BFS-Prover system demonstrates strong
mance in automatic theorem proving (ATP). Our                 performance in automated theorem proving, several
results challenge the conventional belief that more           limitations should be acknowledged, particularly
complex search methods like MCTS and/or value                 regarding model size considerations. Our current
function are necessary for large-scale formal theo-           implementation relies on a relatively small 7B pa-
                                         72
                                                                                            70.8
                                         70                                       69.7
                                                                                            70.4



                      Success Rate (%)
                                                                        68.7
                                                             67.7                 69.3
                                         68                             68.2
                                                   66.6
                                                             67.2
                                         66 65.0
                                                   65.9
                                                                                    SFT
                                         64 64.6                                    SFT+DPO
                                              64   128       256        512      1024      2048
                                                          Pass@k (log-scale)
Figure 4: Evolution of proof accuracies with increasing number of proof search passes on the MiniF2F test. We
compare two training methods: (blue) only using SFT on all state-tactic pairs accumulated in the expert iteration
pipeline of BFS-Prover; and (red), on top of (blue), perform another round of DPO refinement using negative tactic
examples described in Section 2.3. It can be seen that DPO achieves consistent improvement in terms of both
sample efficiency and overall accuracy.


rameter policy model, which may limit the system’s                  monte carlo tree search methods. IEEE Transactions on
ability to learn and utilize more sophisticated math-               Computational Intelligence and AI in Games, 4(1):1–43.
ematical reasoning patterns. While larger models                    Rémi Coulom. 2006. Efficient selectivity and backup
(e.g., 32B or 70B parameters) could potentially cap-                operators in monte-carlo tree search. In International
ture more complex mathematical insights and gen-                    conference on computers and games, pages 72–83.
erate more nuanced tactics, they would introduce                    Springer.
significant computational challenges for both train-                Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W
ing and inference in the context of tree search. This               Ayers, and Stanislas Polu. 2021. Proof artifact co-
trade-off becomes particularly evident when con-                    training for theorem proving with language models.
sidering that larger models typically require more                  arXiv preprint arXiv:2102.06203.
GPU memory and have longer inference latency,                       Yuhang He, Jihai Zhang, Jianzhu Bao, Fangquan Lin,
which could significantly reduce the number of                      Cheng Yang, Bing Qin, Ruifeng Xu, and Wotao Yin.
states that can be explored within a fixed time bud-                2024. Bc-prover: Backward chaining prover for formal
get. Additionally, complex mathematical proofs                      theorem proving. In Proceedings of the 2024 Confer-
                                                                    ence on Empirical Methods in Natural Language Pro-
can generate extensive state descriptions that may                  cessing, pages 3059–3077.
exceed the practical context window of a 7B model,
potentially causing the model to miss crucial infor-                Guillaume Lample, Timothée Lacroix, and 1 others.
mation needed for generating appropriate tactics.                   2022. Hypertree proof search for neural theorem prov-
                                                                    ing. Advances in Neural Information Processing Sys-
                                                                    tems, 35:26337–26349.

References                                                          Aitor Lewkowycz and 1 others. 2022. Solving quantita-
                                                                    tive reasoning problems with language models. arXiv
Thomas Anthony, Zheng Tian, and David Barber. 2017.                 preprint arXiv:2206.14858.
Thinking fast and slow with deep learning and tree
search. Advances in neural information processing sys-              Jia Li, Edward Beeching, Lewis Tunstall, Ben Lip-
tems, 30.                                                           kin, Roman Soletskyi, Shengyi Huang, Kashif Rasul,
                                                                    Longhui Yu, Albert Q Jiang, Ziju Shen, and 1 others.
G Brockman. 2016. Openai gym. arXiv preprint                        2024a. Numinamath: The largest public dataset in
arXiv:1606.01540.                                                   ai4maths with 860k pairs of competition math problems
                                                                    and solutions. Hugging Face repository, 13.
Cameron B Browne, Edward Powley, Daniel White-
house, Simon M Lucas, Peter I Cowling, Philipp                      Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang
Rohlfshagen, Stephen Tavener, Diego Perez, Spyridon                 Wang, Tao Yang, and Haitao Mi. 2024b. Hunyuan-
Samothrakis, and Simon Colton. 2012. A survey of                    prover: A scalable data synthesis framework and guided
tree search for automated theorem proving.        arXiv     Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan
preprint arXiv:2412.20735.                                  Ying, Jiayu Wang, Dahua Lin, and Kai Chen. 2024a.
                                                            Internlm2. 5-stepprover: Advancing automated theorem
Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming           proving via expert iteration on large-scale lean problems.
Yang. 2024. Lean-star: Learning to interleave thinking      arXiv preprint arXiv:2410.15700.
and proving. arXiv preprint arXiv:2407.10040.
                                                            Zijian Wu, Jiayu Wang, Dahua Lin, and Kai Chen.
Leonardo de Moura and Sebastian Ullrich. 2021. The          2024b. Lean-github: Compiling github lean repos-
lean 4 theorem prover and programming language.             itories for a versatile lean prover. arXiv preprint
In International Conference on Automated Deduction          arXiv:2407.17227.
(CADE), pages 625–635. Springer.
                                                            Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
OpenAI. 2023. Gpt-4 technical report. arXiv preprint        Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and Xiao-
arXiv:2303.08774.                                           dan Liang. 2024a. Deepseek-prover: Advancing theo-
                                                            rem proving in llms through large-scale synthetic data.
Judea Pearl. 1984. Heuristics: intelligent search strate-   arXiv preprint arXiv:2405.14333.
gies for computer problem solving. Addison-Wesley
Longman Publishing Co., Inc.                                Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao,
                                                            Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, and 1      Xuan Lu, Qiushi Du, and 1 others. 2024b. Deepseek-
others. 2022. Formal mathematics statement curriculum       prover-v1. 5: Harnessing proof assistant feedback for re-
learning. arXiv preprint arXiv:2202.01344.                  inforcement learning and monte-carlo tree search. arXiv
                                                            preprint arXiv:2408.08152.
Stanislas Polu and Ilya Sutskever. 2020. Generative lan-
guage modeling for automated theorem proving. arXiv         An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
preprint arXiv:2009.03393.                                  Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong
                                                            Tu, Jingren Zhou, Junyang Lin, and 1 others. 2024a.
Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-     Qwen2. 5-math technical report: Toward mathemati-
pher D Manning, Stefano Ermon, and Chelsea Finn.            cal expert model via self-improvement. arXiv preprint
2024. Direct preference optimization: Your language         arXiv:2409.12122.
model is secretly a reward model. Advances in Neural
Information Processing Systems, 36.                         Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,
                                                            Kristin Lauter, Swarat Chaudhuri, and Dawn Song.
David Silver, Aja Huang, Chris J Maddison, Arthur           2024b. Formal mathematical reasoning: A new frontier
Guez, Laurent Sifre, George Van Den Driessche, Julian       in ai. arXiv preprint arXiv:2412.16075.
Schrittwieser, Ioannis Antonoglou, Veda Panneershel-
vam, Marc Lanctot, and 1 others. 2016. Mastering the        Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala,
game of go with deep neural networks and tree search.       Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger,
Nature, 529(7587):484–489.                                  and Animashree Anandkumar. 2024c. Leandojo: Theo-
                                                            rem proving with retrieval-augmented language models.
David Silver, Thomas Hubert, and 1 others. 2017. Mas-       Advances in Neural Information Processing Systems,
tering chess and shogi by self-play with a general rein-    36.
forcement learning algorithm. In Advances in Neural
Information Processing Systems, volume 30.                  Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
                                                            Dahua Lin, and Kai Chen. 2024.         Lean work-
Volker Steinbiss, Bach-Hiep Tran, and Hermann Ney.          book: A large-scale lean problem set formalized
1994. Improvements in beam search. In ICSLP, vol-           from natural language math problems. arXiv preprint
ume 94, pages 2143–2146.                                    arXiv:2406.03847.
Richard S Sutton. 2018. Reinforcement learning: An          Kunhao Zheng, Jesse Michael Han, and Stanislas
introduction. A Bradford Book.                              Polu. 2021. Minif2f: a cross-system benchmark for
                                                            formal olympiad-level mathematics. arXiv preprint
Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin             arXiv:2109.00110.
Li, Zhengying Liu, Qingxing Cao, Yinya Huang, Jing
Xiong, Han Shi, Enze Xie, and 1 others. 2023. Lego-
prover: Neural theorem proving with growing libraries.
                                                            Appendix: Lean Proofs for IMO Problems
arXiv preprint arXiv:2310.00656.                            Found by BFS-Prover
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe       We present the Lean 4 proofs found by BFS-Prover
Diao, Renjie Pi, and Tong Zhang. 2024. Theoremllama:        for several IMO problems in MinF2F test. These
Transforming general-purpose llms into lean4 experts.       examples demonstrate that BFS-Prover can han-
arXiv preprint arXiv:2407.03203.
                                                            dle complex mathematical reasoning in formal sys-
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus           tems, including number theory, inequalities, and
Rabe, Charles Staats, Mateja Jamnik, and Christian          geometric relationships. See Fig. 5, 6, 7, 8, and 9
Szegedy. 2022. Autoformalization with large language
models. Advances in Neural Information Processing           for detailed proofs.
Systems, 35:32353–32368.
theorem imo_1959_p1 (n : N)
 (h0 : 0 < n) :
 Nat.gcd (21 * n + 4) (14 * n + 3) = 1 := by {
   apply Nat.isCoprime_iff_coprime.mp
   simp [IsCoprime, h0]
   refine' 〈-2, 3, by ring〉
 }

                Figure 5: Lean 4 proof of IMO-1959-P1 found by BFS-Prover.




theorem imo_1964_p2 (a b c : R)
 (h0 : 0 < a and 0 < b and 0 < c)
 (h1 : c < a + b)
 (h2 : b < a + c)
 (h3 : a < b + c) :
 a^2*(b + c - a) + b^2*(c + a - b) + c^2*(a + b - c) <= 3 * a * b * c := by {
   nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
 }

                   Figure 6: BFS-Prover’s Lean 4 proof of IMO-1964-P2.




theorem imo_1960_p2 (x : R)
  (h0 : 0 <= 1 + 2 * x)
  (h1 : (1 - sqrt(1 + 2 * x))^2 != 0)
  (h2 : 4 * x^2 / (1 - sqrt(1 + 2 * x))^2 < 2 * x + 9) :
  -1/2 <= x and x < 45/8 := by {
  refine' 〈_, _〉
  all_goals field_simp at h1 h2 |-
  all_goals rw [div_lt_iff (by positivity)] at h2
  all_goals nlinarith [
    sqrt_nonneg (1 + 2 * x), sqrt_nonneg x,
    mul_nonneg h0 (sqrt_nonneg (1 + 2 * x)),
    mul_nonneg h0 (sqrt_nonneg x), mul_self_sqrt h0]
  }

                Figure 7: Lean 4 proof of IMO-1960-P2 found by BFS-Prover.
theorem imo_1962_p2 (x : R)
  (h0 : 0 <= 3 - x)
  (h1 : 0 <= x + 1)
  (h2 : 1/2 < sqrt(3 - x) - sqrt(x + 1)) :
  -1 <= x and x < 1 - sqrt(31)/8 := by {
    constructor
    linarith
    rw [<- sub_pos]
    field_simp [Real.sqrt_lt] at h2 |-
    apply lt_of_le_of_lt
    rw [mul_comm]
    rw [sub_eq_add_neg]
    apply lt_of_le_of_lt
    rw [<- lt_sub_iff_add_lt]
    ring_nf
    rw [<- lt_sub_iff_add_lt]
    linarith [Real.sq_sqrt (by linarith : 0 <= 1 + x)]
    rw [Real.sqrt_lt (by norm_num)]
    rw [Real.sqrt_lt] <;> nlinarith
    norm_num at this
  }

                Figure 8: Lean 4 proof of IMO-1962-P2 found by BFS-Prover.




theorem imo_1983_p6 (a b c : R)
  (h0 : 0 < a and 0 < b and 0 < c)
  (h1 : c < a + b)
  (h2 : b < a + c)
  (h3 : a < b + c) :
  0 <= a^2 * b * (a - b) + b^2 * c * (b - c) + c^2 * a * (c - a) := by {
    have h1' := sq_nonneg (a - b)
    have h2' := sq_nonneg (a - c)
    have h3' := sq_nonneg (b - c)
    nlinarith [
      mul_nonneg (sub_nonneg.mpr h1.le) h1',
      mul_nonneg (sub_nonneg.mpr h2.le) h2',
      mul_nonneg (sub_nonneg.mpr h3.le) h3'
    ]
  }

                Figure 9: Lean 4 proof of IMO-1983-P6 found by BFS-Prover.
