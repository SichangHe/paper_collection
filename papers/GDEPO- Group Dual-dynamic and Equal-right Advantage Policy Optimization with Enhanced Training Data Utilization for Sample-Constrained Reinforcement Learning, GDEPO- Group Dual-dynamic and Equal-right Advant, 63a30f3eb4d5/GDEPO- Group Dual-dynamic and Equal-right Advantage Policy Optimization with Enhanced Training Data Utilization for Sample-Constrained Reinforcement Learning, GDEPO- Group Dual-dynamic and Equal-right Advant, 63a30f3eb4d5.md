                                                                                                                                                                                      1




                                             GDEPO: Group Dual-dynamic and Equal-right Advantage Policy
                                                     Optimization with Enhanced Training Data Utilization for
                                                                   Sample-Constrained Reinforcement Learning
                                          Zhengqing Yan , Xinyang Liu , Yi Zhang , Fan Guo , ChengXun Jia , Junchen Wan , Yao Liu , Qi Liu ,
                                                                                               Jihao Huang , Kang Song



                                            Abstract—Automated Theorem Proving (ATP) represents a                    availability of extensive training and validation datasets [4]–
arXiv:2601.06795v3 [cs.AI] 22 Jan 2026




                                         fundamental challenge in Artificial Intelligence (AI), requiring            [9]. Notably, AlphaGeometry [10] has demonstrated problem-
                                         the construction of machine-verifiable proofs in formal languages           solving performance approaching International Mathematical
                                         such as Lean to evaluate AI reasoning capabilities. Reinforcement
                                         Learning (RL), particularly the high-performance Group Rela-                Olympiad (IMO) medalist levels, signaling a transition of
                                         tive Policy Optimization (GRPO) algorithm, has emerged as a                 LLM-driven ATP from theoretical exploration toward practical
                                         mainstream approach for this task. However, in ATP scenarios,               deployment.
                                         GRPO faces two critical issues: when composite rewards are
                                         used, its relative advantage estimation may conflict with the                  A prevailing approach integrates LLMs with Reinforcement
                                         binary feedback from the formal verifier; meanwhile, its static             Learning (RL) algorithms, leveraging precise feedback from
                                         sampling strategy may discard entire batches of data if no                  formal verifiers to guide policy optimization. Among these,
                                         valid proof is found, resulting in zero contribution to model
                                         updates and significant data waste. To address these limitations,           Group Relative Policy Optimization (GRPO) [11] has gained
                                         we propose Group Dual-dynamic and Equal-right Advantage                     widespread adoption due to its strong empirical performance.
                                         Policy Optimization (GDEPO), a method incorporating three core              However, GRPO faces three critical limitations in the ATP
                                         mechanisms: 1) dynamic additional sampling, which resamples                 setting. First, when composite rewards are used, its advantage
                                         invalid batches until a valid proof is discovered; 2) equal-right           computation may assign negative advantages to correct trajec-
                                         advantage, decoupling the sign of the advantage function (based
                                         on correctness) from its magnitude (modulated by auxiliary                  tories due to interference from other reward components—a
                                         rewards) to ensure stable and correct policy updates; and 3)                mathematical possibility formally detailed in Section VI. To
                                         dynamic additional iterations, applying extra gradient steps to             avoid this issue, many works resort to a single binary cor-
                                         initially failed but eventually successful samples to accelerate            rectness reward, which forfeits RL’s essential role in aligning
                                         learning on challenging cases. Experiments conducted on three               LLM outputs with human preferences. Second, data efficiency
                                         datasets of varying difficulty (MinF2F-test, MathOlympiadBench,
                                         PutnamBench) confirm the effectiveness of GDEPO, while abla-                is poor: under a single binary reward, groups containing only
                                         tion studies validate the necessity of its synergistic components.          incorrect trajectories yield zero advantages across all samples,
                                         The proposed method enhances data utilization and optimization              leading to the discarding of entire batches despite potentially
                                         efficiency, offering a novel training paradigm for ATP.                     informative partial reasoning—particularly problematic when
                                             Index Terms—automated theorem proving, large language                   challenging samples dominate the training set. Third, a fixed
                                         models, reinforcement learning, advantage function, formal ver-             number of optimization iterations treats all samples uniformly,
                                         ification.                                                                  ignoring their varying learning potential.

                                                                                                                        To address the aforementioned issues, we propose the Group
                                                                  I. I NTRODUCTION                                   Dual-dynamic and Equal-right Advantage Policy Optimization
                                                                                                                     (GDEPO) method, whose workflow is illustrated in Fig.1.
                                         T     HE rapid advancement of Large Language Models
                                               (LLMs) has opened new avenues for applying Artificial
                                         Intelligence (AI) to formal reasoning. Automated Theorem
                                                                                                                     This approach identifies and discards ineffective training data,
                                                                                                                     then re-explores valid solutions. It ensures correct optimiza-
                                         Proving (ATP), a core challenge in AI, requires systems to con-             tion direction under arbitrary reward weight combinations
                                         struct machine-verifiable mathematical proofs in formal lan-                through the equal-right advantage mechanism. Furthermore,
                                         guages such as Lean [1]–[3]. Recent progress in ATP on com-                 for initially invalid training instances that yield correct proofs
                                         plex theorem-proving tasks stems from the strong prior knowl-               after re-exploration, the method applies a dynamic number of
                                         edge and generative capabilities of LLMs, coupled with the                  additional backward passes to rapidly assimilate knowledge
                                                                                                                     that is challenging yet solvable for the model.
                                           Corresponding author: Kang Song.
                                           Zhengqing Yan, Yi Zhang, Fan Guo, and Kang Song are with the State           We first validate the effectiveness of GDEPO on
                                         Key Laboratory of Engines, Tianjin University, 300354 Tianjin, China. (e-   three benchmarks of varying difficulty: MinF2F-test, Math-
                                         mail: songkangtju@tju.edu.cn)                                               OlympiadBench, and PutnamBench. Ablation studies further
                                           Xinyang Liu, ChengXun Jia, Junchen Wan, Yao Liu, Qi Liu, and Jihao
                                         Huang are wih the Artificial Intelligence Center, Cylingo Group, 100080     confirm the necessity of each component and their synergistic
                                         Beijing, China.                                                             interaction within the proposed framework.
                                                                                                                                                                                                                                               2



   Whole-proof Completion 1              Verified in LEAN     Rejected by LEAN   Prompt                                                                           Whole-proof Completion 2             Verified in LEAN     Rejected by LEAN


                                                                                                                                                                  Detailed Proof and Analysis
   Detailed Proof and Analysis                                                   Complete the following Lean 4 code with explanatory comments                     [Chain-of-thought] First, let's understand the problem. We need to
   [Chain-of-thought] First, let's understand the problem. We need to            preceding each line of code:                                                     compute the sum of the geometric series ....
   compute the sum of the geometric series ....                                  ```lean4                                                                         Complete Lean 4 Proof
   Complete Lean 4 Proof                                                         import Mathlib                                                                   ```lean4
   ```lean4
                                                                                 open Real                                                                        theorem sum_of_geometric_series : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1))
   theorem sum_of_geometric_series : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1))
   = 265720 / 531441 := by                                                       theorem sum_of_geometric_series : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1))       = 265720 / 531441 := by
     have h_sum : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1)) = 0 := by             = 265720 / 531441 := by                                                           have h_sum : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1)) = 0 := by
       have h₁ : ∀ i ∈ Finset.range 12, 1 / 3 ^ (i + 1) = 0 := by                ```                                                                                 apply Eq.symm
        intro i hi
                                                                                 Before producing the Lean 4 code to formally prove the given theorem,               rfl
        have h₂ : i < 12 := Finset.mem_range.mp hi
        have h₃ : i ≤ 11 := by linarith                                          provide a detailed proof plan outlining the main proof steps and strategies.      have h_rhs : 265720 / 531441 = 0 := by
        interval_cases i <;> norm_num                                            The plan should highlight key ideas, intermediate lemmas, and proof                 norm_num [Nat.div_eq_of_lt]
       calc                                                                      structures that will guide the construction of the final formal proof.              <;> rfl
        ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1)) = ∑ i ∈ Finset.range 12, 0 :=
                                                                                                                                                                   have h_main : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1)) = 265720 / 531441
   by
         apply Finset.sum_congr                                                                                                                                   := by
         intro i hi                                                              First Sampling                                             Additional Sampling       rw [h_sum, h_rhs]
         rw [h₁ i hi]                                                                                           AutoTheoremProver                                     <;> rfl
        _ = 0 := by simp
                                                                                                                                                                    exact h_main
     have h_div : 265720 / 531441 = 0 := by
                                                                                                                                                                  ```
       norm_num
       <;> rfl
     have h_main : ∑ i ∈ Finset.range 12, (1 / 3 ^ (i + 1)) = 265720 / 531441
   := by
                                                                                                                                                 Advantage Computation                                           Additional Iterations
       rw [h_sum, h_div]
                                                                                   Confirmation for
       <;> rfl                                                                    Additional Sampling
     exact h_main
   ```




Fig. 1. The detailed training procedure of GDEPO: LLMs serve as auto-theorem provers by receiving a standardized prompt containing G identical problem
instances, generating whole-proof completions, and verifying them through a Lean4 server [12]. A sample is deemed invalid if all outputs in the group are
incorrect. For the same prompt, sampling continues up to a maximum number of attempts until at least one correct proof is obtained. When the within-group
accuracy falls below a predefined threshold, the correctness feedback from the verifier contributes a sign term to the advantage function, while other signals
determine its magnitude. For samples initially classified as invalid but later yielding valid proofs through subsequent sampling, an additional backward pass
is performed to refine the model parameters.



                      II. R ELATED W ORK                                                                                    hybrid architectures like DSP+ [24] and Delta-Prover [25]
A. Macroscopic Paradigm for Formal Theorem Proving                                                                          adopt a two-stage method of ”first generating a framework,
                                                                                                                            then filling in details,” although their effectiveness typically
   Existing algorithms aim to enhance proof success rates by
                                                                                                                            relies on costly ultra-large-scale foundational models, such
innovating the inference paradigm.
                                                                                                                            as DSP+ using the 671B parameter DeepSeek-R1 [26] or
   The end-to-end generation paradigm trains models to di-
                                                                                                                            DeepSeek-V3 [27], while Delta-Prover utilizes Gemini [28].
rectly output complete proof sequences that can be veri-
                                                                                                                               Regardless of innovations in macro system architecture,
fied by formal verifiers such as Lean [1]–[3]. Representative
                                                                                                                            ultimate performance remains limited by the underlying strat-
works include DeepSeek-Prover [13], Goedel-Prover [14], and
                                                                                                                            egy’s ability to learn from formalized feedback. The efficiency,
Kimina-Prover [15]. This paradigm leverages LLMs’ sequence
                                                                                                                            stability, and utilization of feedback signals by the algorithm
generation capabilities, condensing the proof process into a
                                                                                                                            directly determine whether the system can fully exploit data
single forward generation. It offers advantages of simple ar-
                                                                                                                            value and achieve reliable optimization.
chitecture and efficient reasoning. However, its performance is
significantly constrained by the reliability of single-generation
outputs, posing robustness challenges for complex theorems.                                                                 B. Inadequate Adaptability of Policy Optimization Algorithms
   The proof search–based paradigm guides the model to                                                                      in Formal Theorem Proving
incrementally construct proofs by exploring derivation paths at                                                                Inspired by informal LLMs in natural language process-
each step using feedback from a verifier. For instance, systems                                                             ing, recent foundational work in formal theorem proving
such as DeepSeek-Prover v1.5 [16], BFS-Prover [17], and                                                                     has adopted similar RL-based policy optimization strategies.
ABEL [18] employ tree search algorithms—including Monte                                                                     Current formal theorem provers primarily rely on policy
Carlo tree search or breadth-first search—to explore multiple                                                               optimization algorithms originally developed for informal
proof trajectories and iteratively assemble valid proofs. This                                                              LLM training, such as Proximal Policy Optimization (PPO)
approach substantially enhances the robustness and provable                                                                 [29], Direct Preference Optimization (DPO) [30], and Group
scope of the system, albeit at the cost of considerable compu-                                                              Relative Policy Optimization (GRPO) [11], which is widely
tational and time overhead.                                                                                                 employed by state-of-the-art (SOTA) systems [5], [15], [22].
   To integrate the strengths of these paradigms or mitigate                                                                While these algorithms have demonstrated effectiveness in
their inherent bottlenecks, a series of hybrid methods and aux-                                                             their native domains—such as language alignment and com-
iliary strategies have been proposed. These include leveraging                                                              plex reasoning—they exhibit significant adaptation limitations
retrieval-augmented generation (RAG) to introduce relevant                                                                  when transferred to the formal theorem proving setting, where
theorems [19]; using informal proof sketches to guide formal                                                                feedback is precise and binary.
step generation [19], [20]; and designing self-verification and                                                                1) Limitations of the PPO and Reward Modeling Paradigm:
iterative optimization loops [21]. The ”verifier-in-the-loop”                                                               PPO and its associated reward-model-based paradigm rely
interactive strategy [22], [23] further highlights the value of                                                             on the assumption that the reward function can accurately
iterative improvement through refined feedback. Additionally,                                                               and stably capture complex, composite qualities—such as
                                                                                                                                    3



proof correctness and conciseness. In formal theorem proving,        and effective learning from challenging examples. Developing
however, designing or learning such a reward model is highly         a novel optimization framework that retains computational
challenging, often leading to training instability and reward        efficiency while fundamentally resolving these conflicts has
overfitting, which in turn hinders effective multi-objective         thus become pivotal to advancing the field.
optimization.                                                           The overall architecture of the GDEPO framework and
   2) Limitations of the Direct Preference Optimization and          its comparison with conventional paradigms are illustrated
Preference Optimization Paradigm: DPO enhances training              in Fig.2. The informal large language model RL paradigm,
simplicity by directly leveraging preference data, thereby           depicted in Fig.2a, relies on a trained reward model to generate
bypassing explicit reward model training. However, its op-           scalar rewards. However, such rewards lack the precise binary
timization signal relies on global pairwise rankings, which          signal required to guarantee formal correctness. In contrast,
are ill-suited to incorporate the highly structured, fine-grained    the standard formal ATP paradigm, shown in Fig.2b, employs
feedback inherent to formal environments. Consequently, DPO          a Lean verifier as the ground-truth judge but inherits two rigid
struggles to support localized, incremental refinement of com-       design choices from generic RL: (i) a single-round sampling
plex proof processes, limiting its effectiveness in interactive      mechanism that struggles to explore low-probability correct
theorem proving scenarios that require stepwise correction.          solutions for complex problems, and (ii) a fixed number
   3) Limitations of the Group Relative Policy Optimization          of iterations applied uniformly across all training samples,
Paradigm: GRPO has become the core optimization algorithm            disregarding their varying learning utility. Moreover, the ad-
in current SOTA provers—such as DeepSeek-Prover-V2 [22],             vantage estimation in this paradigm faces a dilemma: using a
Kimina-Prover [15], and Goedel-Prover-V2 [5]—due to its              composite reward function often leads to misaligned gradient
elimination of a separate reward model and computational             directions, whereas relying solely on the binary correctness
efficiency. However, its fundamental mechanism, which re-            reward results in poor data efficiency and weakens the ability
lies on relative comparisons among samples within a group,           of RL optimization to reflect desired output preferences.
inherently conflicts with the absolute correctness criterion            As shown in Fig.2c, the GDEPO algorithm builds upon
demanded by formal verification. This tension manifests in           the GRPO framework with several key enhancements. During
two critical issues. First, when composite rewards are em-           training, the framework identifies ineffective samples and per-
ployed, GRPO’s advantage computation may assign negative             forms additional rollouts until valid ones are obtained, thereby
advantages to otherwise correct proof trajectories due to sub-       maximizing data utilization. It then computes advantages using
optimal scores in other reward components—a mathematical             a redesigned function that enables proper integration of com-
possibility rigorously established in SectionVI. To avoid this,      posite rewards for policy optimization. Finally, the number of
practitioners often resort to binary rewards alone, thereby          policy update iterations is dynamically adjusted based on the
forfeiting the core capability of RL to align large language         difficulty of each sample, accelerating learning on challenging
model outputs with nuanced human preferences, such as proof          instances.
conciseness or elegance. Second, GRPO exhibits low data uti-
lization efficiency: in batches containing a high proportion of
                                                                          III. G ROUP D UAL - DYNAMIC AND E QUAL -R IGHT
challenging samples, using a single binary reward frequently
                                                                                A DVANTAGE P OLICY O PTIMIZATION
results in zero advantages for all trajectories within a group.
Consequently, all sampled attempts that fail to produce a valid         GDEPO was proposed to address the aforementioned lim-
proof are collectively discarded, wasting valuable training data.    itations of standard RL in formal theorem proving. The
To mitigate these risks, existing SOTA systems [5], [15], [22]       framework simultaneously improves data efficiency and op-
adopt a conservative strategy—using only binary rewards and          timization rationality.
deliberately forgoing the potential benefits of composite re-           As illustrated in Fig.3, GDEPO overcomes these design con-
wards. Moreover, data batches comprising exclusively correct         straints through two dynamic modules and a novel advantage
or incorrect samples are often discarded outright [31]. These        computation method. The first module, dynamic additional
compromises yield dual adverse consequences: (i) the precise         sampling, actively increases the number of rollouts until a
and rich feedback from formal verifiers remains underutilized,       valid proof is found, thereby maximizing the utility of each
and (ii) the already scarce high-quality training data suffers       training instance. The second module, equal-right advantage,
from further reduced effective usage, impeding the model’s           decouples the verifier’s authoritative binary correctness signal
ability to learn from challenging examples. Additionally, the        from auxiliary quality-based rewards, ensuring that policy
use of a fixed number of optimization iterations treats all          updates follow a theoretically sound optimization direction.
samples uniformly, ignoring inherent differences in their learn-     The third component, dynamic additional iterations, allocates
ing value. As a result, the current training framework leaves        extra policy update steps based on the empirical difficulty of
considerable room for more efficient exploitation of formal          each sample. Together, these components form an integrated
proof data.                                                          adaptive learning loop that concentrates exploration and com-
   In summary, the inherent incompatibility between existing         putational resources on the most informative and challenging
policy optimization algorithms—particularly GRPO, which              proof trajectories, leading to robust policy improvement and
serves as the de facto standard—and the formal verification          efficient data utilization.
environment constitutes a fundamental bottleneck that impedes           The implementation details of these three core modules are
efficient data utilization, reliable multi-objective optimization,   elaborated below.
                                                                                                                                                                         4


                                                                                                                                                       
                                                                                                                     (k)      (k) (k)               (k)
 a) Informal LLMs RL Paradigm                                                                          where each ri       = ri,1 , ri,2 , . . . , ri,K is a K-dimensional
                 Iterations                                                                                                                                        (k)
                                                                                                       auxiliary reward vector with components satisfying ri,j ∈
                                                             Advantage
           Model              Loss
                                                            Computation    Single-sample Sampling      [0, 1] for all j = 1, . . . , K.
                                                                           Fixed-number Iteration         Correctness is our primary criterion; we aim to ensure that
                                                                           Weighted Reward             among the G trajectories generated for query q, at least one is
       Output                   Reward Model             Single Reward
                                                                                                       correct to facilitate effective model optimization. Thus, the
                                     Sampling
                                                                                                       dynamic sampling terminates when either a correct output
                                                                                                                                       (k)
 b) Formal LLMs RL Paradigm                                                                            exists in the group, i.e., ∃li = 1, or the number of sampling
                 Iterations                                                                            iterations reaches the maximum limit n. The final valid output
           Model              Loss                           Advantage                                 group for query q is denoted as Gq∗ , along with its associated
                                                            Computation    Single-sample Sampling
                                                                                                       valid rewards L∗q and R∗q . Formally, this is expressed as
                                                                           Fixed-number Iteration

                                                                           Single Reward
       Output                   Lean                    Weighted Reward                                                                      ∗
                                                                                                                                   Gq∗ = Gq(k ) ,                    (4a)
                                     Sampling
                                                                                                                                            ∗
                                                                                                                                  L∗q = L(k   )
                                                                                                                                                ,                    (4b)
 c) Group Dual-dynamic Equal-right-advantage Policy Optimization Ours     （ ）                                                       ∗
                                                                                                                                         q
                                                                                                                                          (k∗ )
         Dynamic Additional Iterations                                                                                            Rq = Rq .                          (4c)
                                                                                                                                             (k)
           Model              Loss
                                                          Equal-Right                                  where,k ∗ = min{k | k = n or ∃ li = 1, k ∈ [0, n], k ∈ Z};
                                                           Advantage
                                                                           Dynamic-number Sampling     q ∼ P (Q) denotes a single problem sampled from the distri-
                                                                                                                                                        (k)
                                                                           Dynamic-number Iterations   bution of mathematical theorem-proving tasks; li ∈ {1, −1}
       Output                   Lean                    Weighted Reward    Weighted Reward
                                                                                                       indicates the binary correctness label (with 1 denoting correct
                                                                                                       and −1 denoting incorrect) associated with the i-th trajectory
                          Dynamic Additional Sampling
                                                                                                       in the k-th sampling; n ∈ Z is the user-specified maximum
                                                                                                       number of sampling (e.g., n = 3).
Fig. 2. Overall architecture of the GDEPO framework and its comparison
with conventional paradigms.                                                                           Algorithm 1 Dynamic Additional Sampling.
                                                                                                       Input: maximum number of sampling n ∈ Z, the query q
A. Dynamic Additional Sampling                                                                         Output: the number of sampling k, valid trajectory group Gq∗ ,
                                                                                                           core reward L∗q , auxiliary reward R∗q
   Standard GRPO performs only a single round of sampling                                               1: initialize k ← 0
per query. When handling challenging samples, the model                                                 2: for k = 0, 1, . . . , n do
may assign low probabilities to correct solutions [32]. Under                                                                                  (k)   (k)   (k)
                                                                                                        3:     do sampling by Eq.1-3 to get Gq , Lq , Rq
this fixed single-round scheme, if all sampled outputs are
                                                                                                        4:     update the counter k ← k + 1
incorrect, the resulting batch contains no positive learning                                                          (k)
                                                                                                        5:     if ∃li = 1 then
signal. Discarding such batches not only wastes computational
                                                                                                        6:          break
resources but also overlooks potentially valid candidates with
                                                                                                        7:     end
low generation probabilities. To mitigate this issue, dynamic
                                                                                                        8: end
additional sampling is introduced to enhance the exploration
                                                                                                        9: do store the latest valid value by Eq.4 to get Gq∗ , L∗    ∗
                                                                                                                                                                 q , Rq
of low-probability correct solutions.                                                                                     ∗ ∗     ∗
                                                                                                       10: return k, Gq , Lq , Rq
   The module follows a simple yet efficient design: if the
initial sampling for a query yields no correct output, the system
performs additional sampling on the same query until either
a valid output is obtained or a preset maximum number of                                               B. Equal-Right Advantage
attempts is reached. The detailed pipeline is summarized in                                               The equal-right advantage is introduced to resolve a fun-
Algorithm1. For a given query q, the set of outputs from the                                           damental conflict that arises when applying GRPO to formal
k-th sampling round is denoted as follows:                                                             theorem proving tasks. Standard GRPO computes advantage
                         n
                            (k) (k)         (k)
                                                o                                                      values through intra-group comparisons. As shown in Sec-
                 Gq(k) = o1 , o2 , . . . , oG ,                (1)                                     tionVI, when composite rewards are used, it is mathematically
where G denotes the fixed number of outputs per group. This                                            possible for a trajectory verified as correct by Lean to receive a
output group corresponds to a core binary reward set                                                   negative advantage due to unfavorable auxiliary rewards. This
                       n                    o                                                          can cause the optimizer to suppress already-validated correct
                         (k) (k)        (k)
               L(k)
                 q = l1 , l2 , . . . , lG     ,         (2)                                            solutions, leading to training instability.
                                                                                                          The detailed code pipeline is summarized in Algorithm2.
                   (k)                                                                                 Equal-right advantage decouples the supervision signal: the
with each li ∈ {1, −1}, where 1 indicates a correct output
and −1 an incorrect one (i.e., the Lean4 reward), and an                                               sign of the advantage—i.e., the direction of policy update—is
auxiliary reward set                                                                                   determined solely by the binary label from the verifier, while
                     n                      o                                                          auxiliary rewards modulate only the magnitude of the advan-
                       (k) (k)          (k)
               R(k)
                 q = r1 , r2 , . . . , rG     ,        (3)                                             tage—i.e., the update strength. This mechanism guarantees
                                                                                                                                                       5




                                                                                                            KL
        GRPO

                                                                 Reference
                                                                  Model
                       Policy                                                                           Advantage
                                                                                                                                       Optimizer
                       Model                                                                           Computation

                                                                    LEAN




                                                 Multiple Sampling                         Dynamic
       GDEPO                                                                               Additonal
                                                                                           Sampling


                                                           LEAN
                                                                                                                                       Dynamic
                       Policy                                                                               Equal-Right
                                                                                                                                       Additonal
                       Model                                                                                Advantage
                                                                                                                                       Iterations
                                                           Extra
                                                          Rewards



                                                                                                                                 Multiple Iterations



Fig. 3. Overall training framework of GDEPO in comparison with GRPO.



that all correct proofs receive positive signals and all incorrect                  auxiliary rewards for trajectory i, mean(S ∗ ) and std(S ∗ ) are
ones receive negative signals, preserving the authority of                          the mean and standard deviation of {Sj∗ }G j=1 over the valid
verification outcomes while enabling multi-objective reward                         output group, respectively; li∗ ∈ {1, −1} is the core binary
shaping. Importantly, it yields correct policy update directions                    correctness label for the i-th trajectory in the valid group
                                                                                                                         ∗
even when all G trajectories for a query are either entirely                        (1 for correct, −1 for incorrect); ri,k  ∈ [0, +∞) is the k-
correct or entirely incorrect.                                                      th non-negative auxiliary reward associated with trajectory
   Furthermore, the module adapts to sample difficulty: when                        i (k ≥ 1); w = (w1 , w2 , . . . , wK ) is a weight
                                                                                                                                  PK vector for
the passing rate of sampled trajectories is low, equal-right                        auxiliary rewards satisfying wk ≥ 0 and          k=1 wk = 1;
                                                                                      ∗
advantage is activated to prioritize proof correctness; once                        Smax  = maxj=1,...,G Sj∗ and Smin
                                                                                                                   ∗
                                                                                                                      = minj=1,...,G Sj∗ denote the
the passing rate exceeds a preset threshold τ , the algorithm                       maximum and minimum of the auxiliary reward sums within
reverts to the standard GRPO advantage computation, allowing                        the valid group; and Ŝi∗ is the min–max normalized value of
auxiliary rewards to refine proof quality within a reliably                         Si∗ mapped into [0, 1].
correct solution set. The equal-right advantage is computed                            Finally, Ti denotes the token length of the i-th trajectory,
as follows:                                                                         with all tokens in the trajectory sharing the same advantage
                                                                                    value Âi,t . Gq∗ , L∗q , R∗q
                           (
                            r̃i ,                  cq > τ,
                Â∗i,t =                                                     (5a)
                            li∗ · L(li∗ , Ŝi∗ ), cq ≤ τ,                           C. Dynamic Additional Iterations
                          l∗ + 1                1 − li∗                                Although the dynamic additional sampling module enhances
         L(li∗ , Ŝi∗ ) = i        · Ŝi∗ +             · (1 − Ŝi∗ ),       (5b)
                                                                                    the exploration of low-probability correct solutions, it intro-
                         2                       2
                         0.5                           ∗
                                                  if Smax       ∗
                                                            = Smin   ,              duces a new issue of sample heterogeneity: proofs obtained
                  Ŝi∗ =       Si∗ − Smin∗
                                                                             (5c)   directly in the initial sampling and those discovered only after
                          ∗               ∗      otherwise.                        repeated exploration possess markedly different instructional
                             Smax − Smin
                                                                                    values for model optimization. The latter—requiring sustained
Here, t denotes the token index, and Â∗i,t remains constant                        search to succeed—deserve deeper RL attention. Applying
across all tokens within the same trajectory; cq ∈ [0, 1] denotes                   identical single-step gradient updates to both cases fails to
the pass rate of the query q;∗ τ ∈ (0,         1) is a predefined                   exploit the richer learning potential of the latter.
                                S −mean(S ∗ )
threshold on pass rate; r̃i = i std(S ∗ )      represents the nor-                     To address this, dynamic additional iterations are pro-
malized advantage of the
                       PK i-th trajectory as  used in conventional                  posed to allocate computational resources proportionally to
GRPO, where Si∗ = k=1 wk · ri,k      ∗
                                         is the weighted sum of                     each sample’s learning value. The detailed code pipeline is
                                                                                                                                           6



Algorithm 2 Equal-Right Advantage.                                           Algorithm 3 Dynamic Additional Iterations.
                                                  (∗)
Input: valid trajectory group                    Gq ,
                                         core binary reward          L∗q ,   Input: advantage value list of the query Âlist , the number of
    auxiliary reward R∗q , weights of auxiliary rewards w =                      sampling k, the number of iterations m, upper and lower
    (w1 , . . . , wK ), the pass rate of the query cq , accuracy                 bounds on the clipping ratio εhigh , lower bounds on the
    threshold τ                                                                  clipping ratio εlow , core binary reward L∗q
Output: advantage value list of the query Â∗list                            Output: updated policy πθ
                                                                                       (∗)
 1: do weighted auxiliary rewards computation to get                          1: if ∃li = 1 and k > 1 then
      ∗
                PK
    Sall ← { k=1 wk · ri,k | i = 1, . . . , G}                                2:      for iter = 0, 1, . . . , m do
 2: for i = 1 to G do                                                         3:          do policy updating with loss by Eq.6-7 to get πθ
 3:      do advantage value per token computation by                          4: else
          Eq.5 to get Âi,t                                                   5:      do policy updating with loss by Eq.6-7 to get πθ
 4:      do advantage values for each token aggregate to get                  6: return πθ
          Â∗list .append(Â∗i,t )
 5: end
 6: return Â∗    list                                                       the pass@32 performance of the DeepSeek-Prover-V2-671B
                                                                             model as a filtering criterion, retaining only those samples
                                                                             for which no correct proof is found across 32 independent
summarized in Algorithm3. The principle is straightforward:                  sampling attempts.
easy queries (correct on the first attempt) and persistently
unsolvable hard queries undergo only one update iteration,
                                                                             B. Benchmarks
whereas medium-difficulty queries—those that yield a correct
proof only after multiple sampling rounds—are subjected to m                    We employ three widely adopted benchmarks for evaluat-
iterations to accelerate optimization. Formally, for a query q,              ing the mathematical theorem-proving performance of LLMs,
if its valid output set Gq∗ contains at least one correct trajectory         ordered by increasing difficulty.
and was not produced in the first sampling round, then all G                    1) MiniF2F-test: MiniF2F-test, the test split of MiniF2F
trajectories for q are used in m consecutive policy updates.                 [4], consists of 244 Lean-formalized problems derived from
The overall objective function is expressed as:                              high school mathematical olympiads, including the Ameri-
   This design adaptively concentrates computational effort on               can Mathematics Competitions (AMC), the American Invita-
parameter updates with higher pedagogical value—particularly                 tional Mathematics Examination (AIME), and the International
those arising from successful multi-round searches. Conse-                   Mathematical Olympiad (IMO). In this study, we adopt the
quently, the model more rapidly internalizes knowledge for                   cleaned version of MiniF2F provided by the Kimina team [15],
solving theorems that are challenging yet solvable.                          which ensures reliability through 13-gram decontamination,
                                                                           removal of duplicates, and correction of unsolvable instances.
                               G, T
                         1 X
                                    i
                                          (s)            (s)
                                                                                2) MathOlympiadBench: MathOlympiadBench [5] raises
                                      min ρi,t Â∗i,t , ρ̄i,t Â∗i,t  (6)
                                                                    
   J (θ) = E q∼P (Q)                                                        the difficulty further by comprising 360 manually verified
              G ∗ ∼π (s) GTi i=1
                q     θ
                          old              t=1                               formal problems, each associated with a unique, complete, and
                                                                             Mathlib-compatible theorem along with an informal statement.
where the auxiliary operators are defined as
                                                                             The problems are drawn from the Compfiles database and the
                (s)             πθ(s) (o∗i,t | q, o∗i,<t )                   IMOSLLean4 codebase, forming a rigorously curated set of
               ρi,t =                                      ,         (7a)
                                πθ(s) (o∗i,t | q, o∗i,<t )                   medium-to-high-difficulty proof tasks.
                                   old
                 (s)         (s)                                               3) PutnamBench: PutnamBench [6] represents the most
               ρ̄i,t = clip ρi,t , 1 − εlow , 1 + εhigh .            (7b)    challenging evaluation in our study, featuring 644 university-
         (s)
Here, ρi,t denotes the policy ratio for the t-th token of the                level problems from the William Lowell Putnam Mathematical
i-th trajectory during the s-th iteration; C(x) = clip(x, 1 −                Competition held between 1962 and 2023. Covering algebra,
εlow , 1 + εhigh ) is an asymmetric clipping function with user-             analysis, number theory, geometry, combinatorics, probability,
defined bounds εlow , εhigh > 0.                                             and set theory, this benchmark demands advanced mathemat-
                                                                             ical insight and precise formal reasoning.
               IV. DATASET AND TRAINING                                         The aforementioned benchmarks collectively form a rigor-
                                                                             ous multi-level evaluation framework for assessing the model’s
A. Dataset for Training
                                                                             generalization capability across continuously varying levels of
   The experiments are conducted on the publicly available                   mathematical complexity.
Lean4 [2] formalized mathematical theorem dataset. To rig-
orously evaluate GDEPO’s core capability—learning from
challenging samples—we construct a targeted high-difficulty                  C. Baselines
training set. The data are sourced from FineLeanCorpus [33],                    We compare GDEPO-Prover with three SOTA models rep-
a high-quality dataset comprising formally verified proposi-                 resenting leading paradigms in the field of ATP, ensuring a
tions with broad domain coverage and inherently high diffi-                  diverse evaluation across model architectures and optimization
culty. To further isolate highly challenging instances, we use               strategies.
                                                                                                                                 7



   1) DeepSeek-Prover-V2: DeepSeek-Prover-V2 [22] adopts           severe redundancy; and a smooth length penalty also in
a recursive subgoal decomposition paradigm. Its training pro-      (−1, 1), computed via a cosine function of the generated
cess integrates multiple stages: problem decomposition and         sequence length—short outputs receive rewards close to +1,
formalization using DeepSeek-V3; recursive subgoal solving         while long outputs receive rewards approaching −1, ensuring a
with a 7 billion parameter model; curriculum learning for          smooth transition across lengths. All three reward components
task generation; RL via GRPO algorithm, complemented by            share equal weights to encourage concise yet correct proofs
supervised fine-tuning and knowledge distillation.                 while eliminating potential bias from unequal weighting. For
   2) Kimina-Prover: Kimina-Prover [15] emphasizes training        all baseline methods, the sampling procedure, weighted reward
stability through KL-constrained RL. It initializes via few-       computation, and advantage estimation follow standard prac-
shot fine-tuning, featuring innovations such as automated          tices without modification. In contrast, our proposed GDEPO
formalization methods for dataset construction, specialized        family of models performs additional sampling only when
tokenized reasoning formats for aligning informal and formal       encountering invalid training data and applies extra optimiza-
reasoning, and techniques like format filtering and negative       tion to promote effective exploration. Outside such exploratory
gradient dropping to enhance stability.                            scenarios, GDEPO models operate identically to the baselines,
   3) Goedel-Prover-V2: Goedel-Prover-V2 [5] is centered           adopting the same sampling strategy and reward weighting
around scaffolded data synthesis and iterative self-correction.    scheme.
Key components include scaffolded data synthesis generating           All baselines use standard procedures for sampling,
progressively challenging tasks, verifier-guided self-correction   weighted reward computation, and advantage estimation. In
leveraging Lean compiler feedback for iterative proof cor-         contrast, GDEPO performs additional sampling and targeted
rection, model averaging to mitigate output diversity decline      optimization only when encountering invalid training data;
in later training stages by blending model checkpoints, and        otherwise, it follows the exact same pipeline as the baselines
hybrid GRPO RL incorporating dynamic sampling [31], com-           in non-exploration mode.
bined with supervised fine-tuning for efficient theorem proving       All reported results are averaged over 10 independent runs
with smaller parameter sizes.                                      with distinct random seeds to ensure statistical reliability.
   These benchmark models cover three core technical direc-
tions in ATP—modular decomposition, constraint optimiza-                                 V. E XPERIMENTS
tion, and feedback-loop enabled synthetic data. By comparing          To comprehensively evaluate the effectiveness of our algo-
GDEPO, which focuses on innovative training algorithms,            rithm from multiple perspectives, our experiments comprised
against these models, we can precisely isolate the performance     four components: (a) assessing the overall performance of our
gains attributed to our proposed dynamic sampling and advan-       method; (b) evaluating its capability to leverage challenging
tage estimation mechanisms.                                        training data; (c) examining the efficacy of the equal-right
                                                                   advantage module in utilizing composite rewards; and (d)
D. Training Details                                                analyzing the individual contribution of each module within
                                                                   the GDEPO framework.
   To ensure a fair comparison, all shared hyperparameters
of the trainable models are standardized and uniformly con-        A. Overall Performance Evaluation
figured. The GDEPO algorithm adopts Godel-Prover-V2-8B
[5] as the base model and is enhanced within the Open-R1              To evaluate the overall performance of GDEPO, we trained
algorithmic framework [34].                                        GOEDEL-Prover-V2 on a dataset of 30,000 samples con-
   The learning rate is set to 1 × 10−6 , with a training batch    taining 30% challenging instances and selected the best-
size of 32 and an evaluation batch size of 128. Training           performing model as the representative of our method. Ta-
is distributed using DeepSpeed ZeRO-3, with bfloat16               bleI reports the performance of this model alongside SOTA
precision and FlashAttention-2 enabled. Asymmetric clipping        baselines, including DeepSeek-Prover-V2 [22], Kimina-Prover
is applied to amplify updates from low-probability correct         [15], and Goedel-Prover-V2 [5], along with their variants of
solutions, with ϵlow = 0.2 and ϵhigh = 0.28 [31]. The optimizer    different parameter scales. To ensure that the performance
is AdamW, and the learning rate follows a cosine schedule          improvement of GDEPO is not affected by uncertainties, the
with a minimum learning rate, using a warmup ratio of 0.1. KL      performance data of untrained SOTA models are obtained
divergence constraints are removed during training to enhance      from their respective official teams. The results show that
exploration capability [5].                                        GDEPO consistently improves performance across all three
   The number of training epochs is set to 2. The sign of the      benchmarks, with a notable 84% gain on the most challenging
advantage function is determined solely by the correctness of      PutnamBench. This demonstrates that GDEPO can effectively
the proof as judged by the Lean4 server [12]. The reward           unlock additional performance potential even in models that
function assigns a +1 reward for a correct theorem-proving         have approached their performance ceilings, highlighting its
trajectory and a −1 penalty for an incorrect one [35], with        strong capability in learning from challenging samples.
this component weighted by 1. Additionally, two auxiliary
penalties are applied: a repetition penalty in the range (−1, 1)   B. Utilization Effect of Challenging Training Data Evaluation
based on N-gram overlap (with N = 5), which yields positive          To evaluate how effectively our method leverages challeng-
rewards when no repetition occurs and negative rewards for         ing samples in the training data, we fixed the total number
                                                                                                                                              8




                                          (a)                                                            (b)
Fig. 4. Performance comparison of the same base model trained with GRPO using a single binary reward versus GDEPO employing composite rewards,
under varying proportions of challenging samples: (a) performances on MathOlympiadBench; (b) performances on PutnamBench.



                            TABLE I                                            TableII, GDEPO reduces both the average output length and
   P ERFORMANCE C OMPARISON OF GDEPO-P ROVER WITH E XISTING                    repetition rate without compromising success rate, by properly
      SOTA M ODELS AND T HEIR VARIANTS ACROSS M ODEL S IZES .
                                                                               computing the advantage based on composite rewards. In
                          MiniF2F-test     MathOlympiadBench     PutnamBench   the table, “number of tokens” denotes the average token
        Model
                          Pass Rate (%)         Number of Problem Solved       count across all completions, and “similarity rate” refers to
 DeepSeek-Prover-V2-7B        75.6                   7                 9       the average 5-gram repetition rate. While directly applying
DeepSeek-Prover-V2-671B       82.4                  50                22       composite rewards in GRPO also suppresses output length
   Kimina-Prover-8B           78.3                  26                15
   Kimina-Prover-72B          84.0                  58                24       and redundancy, it incurs a noticeable drop in correctness—a
  Goedel-Prover-V2-8B         84.6                  60                25       critical metric. In contrast, GDEPO preserves correctness by
GDEPO-Prover-8B(Ours)         86.2                  65                46
                                                                               using it to determine the sign of the advantage function,
                                                                               thereby ensuring a proper policy optimization direction, while
of training problems at 30,000 and constructed five datasets                   leveraging auxiliary rewards to modulate the magnitude of
with varying proportions of challenging samples: 10%, 20%,                     policy updates and balance multiple objectives.
30%, 40%, and 50%. Fig.4a-4b compare the performance
of the same base model trained using the standard GRPO
method with a single binary reward against that trained with                   D. Ablation Evaluation
GDEPO employing a composite reward, across these different
ratios of challenging data. The results show that GDEPO                           To evaluate the individual contributions of dynamic addi-
consistently outperforms GRPO, with the performance gap                        tional sampling, dynamic additional iterations, and the equal-
widening as the proportion of challenging samples increases.                   right advantage module in GDEPO, we conduct an abla-
This indicates that GDEPO makes more effective use of                          tion study. All experiments are trained on a fixed dataset
difficult samples that the model initially fails to solve within a             of 30,000 problems containing 30% challenging samples.
batch. Moreover, by performing additional sampling on such                     TableIII presents the ablation results across three evaluation
challenging instances that do not yield correct outputs on                     benchmarks. Since dynamic additional iterations depend on
the first attempt, GDEPO effectively increases the equivalent                  the outcomes of dynamic additional sampling, we do not test
batch size, thereby enhancing the probability of generating                    the iteration module in isolation. The results show that each
low-likelihood correct solutions and rapidly amplifying their                  component contributes to performance gains to varying de-
output probabilities through the equal-right advantage.                        grees. Collectively, the ablation study confirms the importance
                                                                               of every module in the GDEPO framework.
C. Effectiveness of Equal-Right Advantage Evaluation
   To assess the contribution of the equal-right advantage
module to the effective utilization of composite rewards, we                             VI. T HE I MPORTANCE OF A DVANTAGE
compare three variants: GRPO with a single binary reward,
GRPO with composite rewards, and our proposed GDEPO.                              This section provides a supplementary analysis of the GRPO
To ensure the best performance of the algorithms, GDEPO is                     algorithm [11], showing that the sign of the advantage solely
trained on 30,000 training samples containing 30% challenging                  determines the direction of change in the trajectory’s output
samples, while GRPO with two different reward configurations                   probability. Furthermore, when a correctness-based reward
is trained on 30,000 samples containing 20% challenging sam-                   is combined with other components in a composite reward
ples. The composite reward function used in GRPO matches                       function, it is mathematically possible for a correct trajectory
GDEPO exactly in both reward types and weights to eliminate                    to receive a negative advantage due to penalties from the
any confounding effects from reward weighting. As shown in                     auxiliary rewards.
                                                                                                                                                                                                            9



                                                                TABLE II
     P ERFORMANCE C OMPARISON OF THE E QUAL -R IGHT A DVANTAGE M ODULE AGAINST GRPO WITH S INGLE B INARY R EWARD AND GRPO WITH
                                                     C OMPOSITE R EWARD F UNCTIONS .

                                                                           MiniF2F-test                                  MathOlympiad Bench                                   Putnam Bench
                      Algorithm
                                                         Pass Rate (%) ↑    Tokens ↓      Simi. Rate (%) ↓   Prob. Solved ↑   Tokens ↓    Simi. Rate (%) ↓   Prob. Solved ↑    Tokens ↓      Simi. Rate (%) ↓
Goedel-Prover-V2-8B with GRPO (Single Binary Reward)          84.8           9640.89            49.29             61           28692.96        81.84              27           30148.48           85.23
           Goedel-Prover-V2-8B with GRPO                      83.2           7903.04            46.99             59           14906.10        75.59              24           26215.64           80.76
                       δ Perf.                                -1.6          -1737.85            -2.30             -2          -13786.86        -6.25              -3           -3932.84           -4.47
  Goedel-Prover-V2-8B with Equal-Right Advantage              85.3           9008.35            48.22             62           15632.41        77.33              31           28510.36           83.87
                       δ Perf.                                +0.5           -632.54            -1.07             +1          -13060.55        -4.51              +4           -1638.12           -1.36

The performance difference relative to Goedel-Prover-V2-8B with GRPO (Single Binary Reward) is indicated as ”δ Perf.”. Tokens = Number of Tokens,
Simi. Rate = Similarity Rate, Prob. Solved = Number of Problem Solved. Higher values are preferred for metrics marked with ↑, and lower values are
preferred for those marked with ↓.



                            TABLE III                                                                    update θ. Employing gradient ascent to maximize the objective
A BLATION STUDY RESULTS , SHOWING THE IMPACT OF EACH COMPONENT                                           function, the relationship between the sign of the advantage
                   ON OVERALL PERFORMANCE .
                                                                                                         and the direction of change in the trajectory probability during
            Module                      MiniF2F-test   MathOlympiadBench           PutnamBench           the first iteration is illustrated in Fig.5. Moreover, it follows
                                                                                                                        (s)
D.A.S.     E.R.A.      D.A.I.       Pass Rate (%)         Number of Problems Solved                      that when ρi,t ̸= 1, its relative magnitude with respect to
   –          –             –               84.6               60                         25             unity is uniquely determined by the sign of the advantage.
   ✓          –             –            84.9 (+0.3)         63 (+3)                   36 (+11)                                     (s)
   –          ✓             –            85.3 (+0.7)         62 (+2)                    31 (+6)
                                                                                                         Specifically, whenever ρi,t exceeds the upper clipping bound,
                                                                                                           ∗
   ✓          –             ✓            85.8 (+1.2)         64 (+4)                   41 (+16)          Âi,t > 0 holds invariably, ensuring that the minimum operator
   ✓          ✓             ✓            86.2 (+1.6)         65 (+5)                   46 (+21)                             (s)
The baseline is Godel-Prover-V2-8B. The dynamic additional sampling is
                                                                                                         always selects ρ̄i,t ; the converse also holds symmetrically.
indicated as “D.A.S.”. The equal-right advantage is indicated as “E.R.A.”.                               Consequently, the objective function—after removal of the KL
The dynamic additional iterations is indicated as “D.A.I.”.                                              divergence term—and its gradient can be simplified.

                                                                                                                                                                                   
A. Advantage Sign as Determinant of Trajectory Probability                                                                                                     G, Ti
                                                                                                                                            1       (s)
                                                                                                                                                               X
Direction                                                                                                              J (θ) = E q∼P (Q)          ρ̂ Â∗  ,                                        (11a)
                                                                                                                                                            
                                                                                                                                Gq∗ ∼π (s)  GTi i=1 i,t i,t
 The gradient of the objective function after removing the                                                                                    θ
                                                                                                                                                  old          t=1
KL divergence is given by                                                                                                                                                              
                                                                                                                                                               G, Ti
                                                                                                                                        1         (s)
                                                                                                                                                               X
                                                                                                                                                ∇ρ̂i,t Â∗i,t 
                                                            
                                                                                                                  ∇J (θ) = E q∼P (Q)                                                                (11b)
                                                                                                                                                              
                     G, T i
               1 X             (s)              (s)                                                                       Gq∗ ∼π (s)  GTi i=1
                            min ∇ρi,t Â∗i,t , ∇ρ̄i,t Â∗i,t  (8)
                                                            
  ∇J (θ) = E                                                                                                                                 θ
                                                                                                                                                  old          t=1
                GTi i=1
                                         t=1                                                             where the auxiliary quantities are defined as
where the auxiliary quantities are defined as                                                                         (
                                                                                                                         (s)    (s)                         
                                                                                                                (s)    ρi,t , ρi,t ∈ 1 − εlow , 1 + εhigh
                                πθ(s) (o∗i,t | q, o∗i,<t )                                                    ρ̂i,t =    (s)    (s)                         ,                                       (12a)
                      (s)
                  ρi,t =                                   ,                                    (9a)                   ρ̄i,t , ρi,t ∈/ 1 − εlow , 1 + εhigh
                                πθ(s) (o∗i,t | q, o∗i,<t )                                                            (
                                                                                                                            (s)    (s)                        
                                        old
                                                                                                                (s)    ∇ρi,t , ρi,t ∈ 1 − εlow , 1 + εhigh
                    (s)         (s)                       
                  ρ̄i,t = clip ρi,t , 1 − εlow , 1 + εhigh .                                    (9b)        ∇ρ̂i,t =               (s)                        .                                     (12b)
                                                                                                                       0,        ρi,t ∈/ 1 − εlow , 1 + εhigh
Here, πθ(s) (o∗i,t | q, o∗i,<t ) denotes the probability under the                                          It is proven that the min function, in extreme cases, enforces
          old
old policy and remains constant with respect to θ. The expec-                                            the gradient to zero, thereby preventing excessive deviation
tation operator E is representing expectation over the question                                          in the output probability of the trajectory across multiple
distribution and the effective response groups sampled from                                                                                                     (s)
                                                                                                         iterations. In subsequent iterations, even when ρi,t ̸= 1,
the old policy E q∼P (Q) . Consequently, it can be treated as a                                          the sign of the advantage and the direction of change in
                            Gq∗ ∼π (s)
                                    θ
                                     old                                                                 the trajectory’s output probability remain consistent with the
                                                                                          (s)
fixed quantity during differentiation. The gradients ∇ρi,t and                                           procedure illustrated in Fig.5.
    (s)
∇ρ̄i,t can be further decomposed:                                                                           In summary, the sign of the advantage function uniquely
                                                                                                         determines the direction of change in the trajectory output
                (s)          ∇πθ(s) (o∗i,t | q, o∗i,<t )                                                 probability.
           ∇ρi,t =                                       ,                                  (10a)
                              πθ(s) (o∗i,t | q, o∗i,<t )
                                  old
              (s)          (s)                       
           ∇ρ̄i,t = clip ∇ρi,t , 1 − εlow , 1 + εhigh .                                     (10b)        B. Possibility of Negative Advantages on Correct Trajectories
                                              (s)             (s)            (s)
                                                                                                         under Composite Rewards
   At the first iteration, ρi,t = 1 and ∇ρ̄i,t = ∇ρi,t , rendering
                                                                (s)                                        The advantage function in the GRPO algorithm is computed
the clipping operation inconsequential. The gradient ∇ρi,t                                               as follows:
fundamentally reflects the alignment between the direction of                                                                          ri − mean(r)
change in the policy probability and the direction of parameter                                                          Âi,t = r̃i =                         (13)
                                                                                                                                           std(r)
                                                                                                                                               10



                                                                                 correct and incorrect outputs exist within the group. Moreover,
                                                                                 the standard deviation of the total reward within the group
                                                                                 satisfies σs > 0, thereby excluding the degenerate case
                                                                                 where all outputs receive identical rewards.3) Non-zero Weight
                                                                                 Assumption: The weight assigned to the correctness reward
                                                                                 satisfies α > 0, and each auxiliary reward weight satisfies
                                                                                 wj > 0, guaranteeing that both reward components contribute
                                                                  Numerical
                                                                   Increase      non-trivially to the total reward.
                                                                                    The outputs within the group are partitioned into two subsets
                                                                  Numerical
                                                                  Decrease       based on correctness: the set of correct outputs G1 = {oi |
                                                                                 li = 1}, with cardinality PK G1 = pGPand weighted average
                                                                                 auxiliary reward r̄1 = j=1 wj · G11 oi ∈G1 ri,j ; and the set
                                                                                 of incorrect outputs G0 = {oi | li = 0}, with cardinality
                                                                                 P0K= (1 − p)G
                                                                                 G
                                                                                              1
                                                                                                 Pand weighted average auxiliary reward r̄0 =
                                                                                    j=1 wj · G0     oi ∈G0 ri,j .
                                                                                    Consequently, the group-level mean of the total reward can
                                                                                 be decomposed as follows:
Fig. 5. Relationship between the sign of advantage and the direction of change                    µs = αp + pr̄1 + (1 − p)r̄0               (15)
in trajectory output probabilities.
                                                                                 The average total reward of the correct subset is given by:
   where ri denotes the total reward of the i-th output.                                                 µs,1 = α + r̄1                     (16)
mean(r) and std(r) represent the mean and standard deviation
of the rewards within the group, respectively. The advantage                     There exists a correct output oi ∈ G1 such that Âi < 0 if and
function for all tokens corresponding to a given output is                       only if:
identical and equal to the normalized total reward of that                                                 µs,1 < µs                       (17)
output (i.e., Âi,t remains constant across all timesteps t for                  The necessity is proved as follows. Suppose there exists oi ∈
the same output).                                                                G1 for which Âi < 0. Then, by definition
   For a query q, a sampled trajectory is denoted as Gq =                                                                 P of the advantage
                                                                                 function, si < µs . Since µs,1 = G11 oi ∈G1 si denotes the
{o1 , o2 , . . . , oG }. The correctness binary reward is represented            average total reward over all correct outputs, if si ≥ µs held
by Lq = {l1 , l2 , . . . , lG }, where each li ∈ {0, 1}, with                    for every oi ∈ G1 , it would follow that µs,1 ≥ µs , leading to
1 indicating a correct output and 0 an incorrect one. The                        a contradiction. Hence, it must be that µs,1 < µs .
auxiliary reward is denoted as Rq = {r1 , r2 , . . . , rG }, where                  For sufficiency, suppose µs,1 < µs . By the definition of the
each ri = (ri,1 , ri,2 , . . . , ri,K ) is a K-dimensional auxiliary             arithmetic mean, there necessarily exists at least one oi ∈ G1
reward vector whose components satisfy ri,j ∈ [0, 1] for all                     such that si < µs . Given that σs > 0—which follows from
j = 1, . . . , K.                                                                the non-degeneracy of rewards within the group (as identical
   The weight assigned to the correctness binary reward is                       rewards would render the advantage function undefined)—it
α > 0, and the weights for the auxiliary rewards         PK are given            follows that Âi < 0. Consequently, there exists a correct
by w = (w1 , . . . , wK ), subject to the constraint j=1 wj =                    output exhibiting a negative advantage.
                                                    (k)
1. The raw weighted reward for output oi is defined as                              In summary, when a correctness-based reward is incorpo-
 (k)             (k)    PK           (k)
si = α · li + j=1 wj · ri,j , with its empirical mean and                        rated into a composite reward structure, it is mathematically
                                                  (k)    1
                                                           PG (k)
                                                                                 possible for a correct trajectory to yield a negative advantage
standard deviation  q given     respectively by µs = G        i=1 si
       (k)               1
                           PG       (k)     (k) 2                                due to the influence of other reward components.
and σs =               G−1    i=1 (si    − µs ) . Eq.13 can thus be
reformulated as follows:
                                                                                                      VII. C ONCLUSION
                                    si − µs
                              Âi =                                       (14)      This paper addresses critical limitations in current RL based
                                       σs                                        ATP methods concerning training efficiency and optimization
The sign of the advantage is determined by the numerator:                        direction by proposing the GDEPO framework. GDEPO sys-
Âi < 0 ⇐⇒ si < µs .                                                             tematically enhances the learning efficacy of LLMs in formal
   To simplify the analysis while maintaining generality, the                    reasoning through three key mechanisms. First, it leverages
following reasonable assumptions are introduced. 1) Reward                       the Lean verifier to precisely identify and discard entirely
Independence Assumption: The correctness indicator li and                        invalid training samples while actively exploring potentially
the auxiliary reward vector ri are mutually independent, i.e.,                   correct proof paths via a supplementary sampling strategy.
E[li ri,j ] = E[li ]E[ri,j ] for all j. 2) Non-degeneracy Within                 Second, it introduces the equal-right advantage mechanism,
Group Assumption: The expected correctness rate satisfies                        which preserves the binary correctness signal from the verifier
p = E[li ] ∈ (0, 1), and the expected auxiliary rewards                          as the primary optimization direction while integrating mul-
satisfy µj = E[ri,j ] ∈ (0, 1) for all j, ensuring that both                     tidimensional auxiliary rewards to enrich the policy gradient
                                                                                                                                                        11



representation. Third, it applies dynamic-iteration backpropa-                [11] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang,
gation on challenging samples that initially fail but eventually                   Y. Li, Y. Wu, and D. Guo, “DeepSeekMath: Pushing the Limits of
                                                                                   Mathematical Reasoning in Open Language Models,” arXiv preprint
succeed, accelerating the model’s mastery of difficult yet                         arXiv:2402.03300, 2024.
solvable problems.                                                            [12] M. D. Santos, H. de Saxcé, H. Wang, M. Baksys, M. Unsal,
   We conduct comprehensive experiments on three progres-                          J. Liu, Z. Liu, and J. LI, “Kimina Lean Server: A High-Performance
                                                                                   Lean Server for Large-Scale Verification,” in Proc. 5th Workshop on
sively challenging formal mathematical benchmarks: MinF2F-                         Mathematical Reasoning and AI at NeurIPS 2025, 2025. [Online].
test, MathOlympiadBench, and PutnamBench. Results demon-                           Available: https://openreview.net/forum?id=orPt2nxLoC
strate that GDEPO significantly outperforms existing GRPO-                    [13] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan, W. Li,
                                                                                   and X. Liang, “DeepSeek-Prover: Advancing Theorem Proving in LLMs
based training paradigms, achieving substantial gains in both                      through Large-Scale Synthetic Data,” arXiv preprint arXiv:2405.14333,
proof success rate and data utilization efficiency. Ablation                       2024.
studies further confirm that all three components are essential               [14] Y. Lin, S. Tang, B. Lyu, J. Wu, H. Lin, K. Yang, J. Li, M. Xia, D. Chen,
                                                                                   S. Arora, and C. Jin, “Goedel-Prover: A Frontier Model for Open-Source
and act synergistically.                                                           Automated Theorem Proving,” arXiv preprint arXiv:2502.07640, 2025.
   This work not only delivers a more efficient and robust                    [15] H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung,
                                                                                   M. Vinyes, Z. Ying, Z. Zhu et al., “Kimina-Prover Preview: Towards
training framework for LLM-driven ATP systems but also                             Large Formal Reasoning Models with Reinforcement Learning,” arXiv
offers a novel perspective on designing RL algorithms for                          preprint arXiv:2504.11354, 2025.
tasks equipped with precise verification mechanisms. With                     [16] H. Xin, Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu, L. Zhang,
                                                                                   X. Lu, Q. Du et al., “DeepSeek-Prover-V1.5: Harnessing Proof Assistant
the advancement of AI, nearly all collectible training data                        Feedback for Reinforcement Learning and Monte-Carlo Tree Search,”
have already been exhausted, and the difficulty of acquiring                       arXiv preprint arXiv:2408.08152, 2024.
or generating high-value training data continues to rise. While               [17] R. Xin, C. Xi, J. Yang, F. Chen, H. Wu, X. Xiao, Y. Sun, S. Zheng,
                                                                                   and M. Ding, “BFS-Prover: Scalable Best-First Tree Search for LLM-
prior research has largely focused on increasing data quantity                     based Automatic Theorem Proving,” in Proc. 63rd Annual Meeting of
and quality and on crafting sophisticated reward functions, we                     the Association for Computational Linguistics (ACL), vol. 1, 2025, pp.
argue that future efforts should place equal emphasis on max-                      32 588–32 599.
                                                                              [18] F. Gloeckle, J. Limperg, G. Synnaeve, and A. Hayat, “ABEL:
imizing the utility of existing data and on developing domain-                     Sample Efficient Online Reinforcement Learning for Neural Theorem
informed strategies for computing trajectory advantages in RL                      Proving,” in Proc. 4th Workshop on Mathematical Reasoning and AI at
applications.                                                                      NeurIPS ’24, 2024. [Online]. Available: https://openreview.net/forum?
                                                                                   id=kk3mSjVCUO
                                                                              [19] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,
                                                                                   S. Godil, R. Prenger, and A. Anandkumar, “LeanDojo: Theorem
                             R EFERENCES                                           Proving with Retrieval-Augmented Language Models,” in Proc. 37th
                                                                                   Conf. Neural Information Processing Systems (NeurIPS) Datasets and
 [1] L. de Moura, S. Kong, J. Avigad, F. Van Doorn, and J. von Raumer,             Benchmarks Track, 2023. [Online]. Available: https://openreview.net/
     “The Lean Theorem Prover (System Description),” in Proc. Int. Conf.           forum?id=g7OX2sOJtn
     Automated Deduction (CADE). Springer, 2015, pp. 378–388.                 [20] A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li,
 [2] L. de Moura and S. Ullrich, “The Lean 4 Theorem Prover and Pro-               M. Jamnik, G. Lample, and Y. Wu, “Draft, Sketch, and Prove: Guiding
     gramming Language,” in Proc. Int. Conf. Automated Deduction (CADE).           Formal Theorem Provers with Informal Proofs,” in Proc. 11th Int.
     Springer, 2021, pp. 625–635.                                                  Conf. Learning Representations (ICLR), 2023. [Online]. Available:
 [3] H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen, “Lean                  https://openreview.net/forum?id=SMa9EAovKMC
     Workbook: A large-scale Lean problem set formalized from natural         [21] X. Ji, Y. Liu, Q. Wang, J. Zhang, Y. Yue, R. Shi, C. Sun, F. Zhang,
     language math problems,” in Proc. 38th Conf. Neural Information               G. Zhou, and K. Gai, “Leanabell-Prover-V2: Verifier-integrated Rea-
     Processing Systems (NeurIPS) Datasets and Benchmarks Track, 2024.             soning for Formal Theorem Proving via Reinforcement Learning,” arXiv
     [Online]. Available: https://openreview.net/forum?id=Vcw3vzjHDb               preprint arXiv:2507.08649, 2025.
 [4] K. Zheng, J. M. Han, and S. Polu, “miniF2F: a cross-system               [22] Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang,
     benchmark for formal Olympiad-level mathematics,” in Proc. Int.               Z. Fu, Q. Zhu, D. Yang et al., “DeepSeek-Prover-V2: Advancing For-
     Conf. Learning Representations (ICLR), 2022. [Online]. Available:             mal Mathematical Reasoning via Reinforcement Learning for Subgoal
     https://openreview.net/forum?id=9ZPegFuFTFv                                   Decomposition,” arXiv preprint arXiv:2504.21801, 2025.
 [5] Y. Lin, S. Tang, B. Lyu, Z. Yang, J.-H. Chung, H. Zhao, L. Jiang,        [23] S. Rajaee, K. Pratik, G. Cesa, and A. Behboodi, “Local Look-
     Y. Geng, J. Ge, J. Sun et al., “Goedel-Prover-V2: Scaling Formal              Ahead Guidance via Verifier-in-the-Loop for Automated Theorem
     Theorem Proving with Scaffolded Data Synthesis and Self-Correction,”          Proving,” in Proc. Workshop on Reasoning and Planning for
     arXiv preprint arXiv:2508.03613, 2025.                                        Large Language Models (RapLLMs), 2025. [Online]. Available:
 [6] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings,              https://openreview.net/forum?id=e6VJwdnd8s
     A. Thakur, and S. Chaudhuri, “PutnamBench: Evaluating Neural             [24] C. Cao, L. Song, Z. Li, X. Le, X. Zhang, H. Xue, and F. Yang, “Reviving
     Theorem-Provers on the Putnam Mathematical Competition,” in Proc.             DSP for Advanced Theorem Proving in the Era of Reasoning Models,”
     38th Conf. Neural Information Processing Systems (NeurIPS) Datasets           arXiv preprint arXiv:2506.11487, 2025.
     and Benchmarks Track, vol. 37, 2024, pp. 11 545–11 569.                  [25] Y. Zhou, J. Zhao, Y. Zhang, B. Wang, S. Wang, L. Chen, J. Wang,
 [7] G. Gao, Y. Wang, J. Jiang, Q. Gao, Z. Qin, T. Xu, and B. Dong,                H. Chen, A. Jie, X. Zhang et al., “Solving Formal Math Problems by De-
     “Herald: A Natural Language Annotated Lean 4 Dataset,” in Proc. 13th          composition and Iterative Reflection,” arXiv preprint arXiv:2507.15225,
     Int. Conf. Learning Representations (ICLR), 2025. [Online]. Available:        2025.
     https://openreview.net/forum?id=Se6MgCtRhz                               [26] D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang,
 [8] J. Hu, T. Zhu, and S. Welleck, “miniCTX: Neural Theorem Proving with          S. Ma, X. Bi et al., “DeepSeek-R1 incentivizes reasoning in LLMs
     (Long-)Contexts,” in Proc. 13th Int. Conf. Learning Representations           through reinforcement learning,” Nature, vol. 645, no. 8081, pp. 633–
     (ICLR), 2025. [Online]. Available: https://openreview.net/forum?id=           638, 2025.
     KIgaAqEFHW                                                               [27] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng,
 [9] H. Wang, H. Xin, Z. Liu, W. Li, Y. Huang, J. Lu, Z. YANG, J. Tang,            C. Zhang, C. Ruan et al., “DeepSeek-V3 Technical Report,” arXiv
     J. Yin, Z. Li, and X. Liang, “Proving Theorems Recursively,” in Proc.         preprint arXiv:2412.19437, 2024.
     38th Annual Conf. Neural Information Processing Systems (NeurIPS),       [28] G. Comanici, E. Bieber, M. Schaekermann, I. Pasupat, N. Sachdeva,
     2024. [Online]. Available: https://openreview.net/forum?id=yAa5l92TtQ         I. Dhillon, M. Blistein, O. Ram, D. Zhang, E. Rosen et al., “Gemini
[10] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong, “Solving olympiad          2.5: Pushing the Frontier with Advanced Reasoning, Multimodality,
     geometry without human demonstrations,” Nature, vol. 625, no. 7995,           Long Context, and Next Generation Agentic Capabilities,” arXiv preprint
     pp. 476–482, 2024.                                                            arXiv:2507.06261, 2025.
                                                                              12



[29] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Prox-
     imal policy optimization algorithms,” arXiv preprint arXiv:1707.06347,
     2017.
[30] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and
     C. Finn, “Direct Preference Optimization: Your Language Model is
     Secretly a Reward Model,” in Proc. Advances in Neural Information
     Processing Systems (NeurIPS), vol. 36, 2023, pp. 53 728–53 741.
[31] Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, W. Dai, T. Fan,
     G. Liu, L. Liu et al., “DAPO: An Open-Source LLM Reinforcement
     Learning System at Scale,” arXiv preprint arXiv:2503.14476, 2025.
[32] A. W. He, D. Fried, and S. Welleck, “Rewarding the Unlikely: Lifting
     GRPO Beyond Distribution Sharpening,” in Proc. 2025 Conf. Empirical
     Methods in Natural Language Processing (EMNLP), Suzhou, China,
     Nov. 2025, pp. 25 548–25 560.
[33] Z. Peng, Y. Yao, K. Ma, S. Guo, Y. Li, Y. Zhang, C. Zhang, Y. Zhang,
     Z. Yu, L. Li, M. Liu, Y. Xia, J. Shen, Y. Wu, Y. Cao, Z. Zhang,
     W. Huang, J. Liu, and G. Zhang, “Criticlean: Critic-Guided Rein-
     forcement Learning for Mathematical Formalization,” arXiv preprint
     arXiv:2507.06181, 2025.
[34] Hugging Face, “Open R1: A Fully Open Reproduction of DeepSeek-R1,”
     Jan. 2025. [Online]. Available: https://github.com/huggingface/open-r1
[35] J. Zhang and C. Zuo, “GRPO-LEAD: A Difficulty-Aware Reinforcement
     Learning Approach for Concise Mathematical Reasoning in Language
     Models,” arXiv preprint arXiv:2504.09696, 2025.
