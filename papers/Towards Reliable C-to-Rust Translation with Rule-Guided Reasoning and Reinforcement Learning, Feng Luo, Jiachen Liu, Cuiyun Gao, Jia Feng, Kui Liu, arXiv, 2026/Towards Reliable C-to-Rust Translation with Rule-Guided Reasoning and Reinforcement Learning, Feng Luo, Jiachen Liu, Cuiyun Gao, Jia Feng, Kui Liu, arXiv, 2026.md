                                                 Towards Reliable C-to-Rust Translation with Rule-Guided
                                                         Reasoning and Reinforcement Learning
                                                               Feng Luo                                  Jiachen Liu                                Cuiyun Gao∗
                                                 Harbin Institute of Technology,               Harbin Institute of Technology,            Harbin Institute of Technology,
                                                           Shenzhen                                      Shenzhen                                   Shenzhen
                                                              China                                         China                                      China
                                                  hitszluofeng@foxmail.com                       jiachenliu@stu.hit.edu.cn                   gaocuiyun@hit.edu.cn

                                                                                   Jia Feng                                     Kui Liu
                                                                       Harbin Institute of Technology,             Huawei Software Engineering
                                                                                 Shenzhen                          Application Technology Lab
                                                                                    China                                     China
                                                                          jiafeng@stu.hit.edu.cn                      kui.liu@huawei.com

                                         Abstract                                                                memory-safety issues in C and C++ [7, 47]. Rust offers memory
                                         The migration of legacy C programs to Rust has become an im-            safety without garbage collection, while retaining the low-level
                                         portant direction for improving software memory safety while            control of C/C++ through its ownership and borrowing model [39].
arXiv:2607.19966v1 [cs.SE] 22 Jul 2026




                                         alleviating the high cost of manual rewriting. Leveraging large         It has seen increasing adoption in practice, including in the Linux
                                         language models (LLMs) for automated C-to-Rust translation has          kernel, AWS Firecracker, and security-critical components of Win-
                                         emerged as a promising direction. However, existing LLM-based           dows [2, 8]. However, manually migrating existing C projects to
                                         approaches remain limited. On the one hand, LLMs exhibit limited        Rust is costly, as developers must learn Rust’s safety model and
                                         capability in identifying Rust-specific rules, and inadequate han-      preserve the semantics of legacy code. Therefore, automated C-to-
                                         dling of Rust syntax often results in incorrect translations. On the    Rust translation, which aims to generate semantically equivalent
                                         other hand, existing LLMs often struggle to accurately capture the      Rust code, has emerged as a promising direction.
                                         semantics of complex code, resulting in incorrect translations.             Early work on C-to-Rust translation mainly relies on rule-based
                                            To address these challenges, we propose a Translation fRAmewo-       techniques [23, 30, 54], with C2Rust [27] as a representative system
                                         rk Via rule-guided reasoning and rEinforcement Learning, namely         built on Clang [31] and LLVM [29], and follow-up work extending
                                         TRAVEL, consisting of two modules. The first module employs             it to specific scenarios such as pointer handling and parallel API
                                         Monte Carlo Tree Search (MCTS)-based reasoning path construc-           migration [11, 12, 22, 55]. While efficient and interpretable, these
                                         tion guided by Rust-specific rules, steering the search toward trans-   methods depend heavily on handcrafted expert rules, making them
                                         lation steps that respect the syntactic rules that LLMs frequently      labor-intensive to develop and limited in coverage when faced with
                                         violate. The second module introduces reinforcement learning that       the diverse patterns of real-world programs [12, 21].
                                         couples execution feedback with reasoning-quality signals, encour-          Recently, large language models (LLMs) have shown strong po-
                                         aging the model to construct reasoning paths that accurately cap-       tential in code generation and translation [34, 41, 42], motivat-
                                         ture program semantics, thereby ensuring that the generated Rust        ing studies that formulate C-to-Rust translation as a sequence-
                                         code preserves the intended behavior of the original C program.         to-sequence task and learn patterns from large-scale code cor-
                                            We evaluate TRAVEL on three datasets: xCodeEval (a public            pora [13, 51]. However, existing LLM-based methods still face two
                                         benchmark), OS-Bench (functions collected from the Linux kernel),       key challenges. First, LLMs often fail to follow Rust-specific rules,
                                         and HW-Bench (an industrial dataset from Huawei). On xCodeEval,         such as ownership, borrowing, and lifetimes (see Fig. 3). These rules
                                         TRAVEL outperforms all baselines across three backbone LLMs. In         are central to Rust’s safety model, but they are not explicitly opti-
                                         particular, compared to the strongest prompting baseline IRENE,         mized during pretraining. As a result, LLMs may generate Rust code
                                         TRAVEL improves computational accuracy (CA) by 26.22% and com-          that violates compilation rules or relies on unsafe constructs to by-
                                         pilation success rate (CSR) by 18.77%. On HW-Bench and OS-Bench,        pass safety checks. Existing methods that use external tools or static
                                         TRAVEL further improves CSR by 18.28% and 16.51%, respectively,         feedback [35, 56] mainly repair errors after generation, and thus
                                         while reducing unsafe rate (UR) by 13.06% and 13.08%, respectively.     provide limited guidance during the translation process. Second,
                                                                                                                 LLMs often struggle to accurately capture the semantics of complex
                                         1    Introduction                                                       code (as shown in Fig. 4). C-to-Rust translation often depends on
                                                                                                                 capturing subtle semantics in the source program. However, these
                                         Memory-safety vulnerabilities remain the dominant source of crit-
                                                                                                                 semantics are not explicitly modeled during generation, making
                                         ical software flaws in modern systems, and are widely exploited
                                                                                                                 it difficult for LLMs to consistently reflect them in the generated
                                         across browsers, operating systems, and cloud infrastructure [10,
                                                                                                                 code.
                                         19]. Prior studies show that around 70% of vulnerabilities in large
                                                                                                                     To address these challenges, we propose TRAVEL, a translation
                                         codebases such as Microsoft products and Android stem from
                                                                                                                 framework via rule-guided reasoning and reinforcement learning,
                                         ∗ Corresponding author.                                                 consisting of two key modules:
                                                                                                                                       Luo et al.


     • Rule-Guided Reasoning Path Search Module: This mod-                2.1    Overview
       ule constructs translation reasoning paths using MCTS              As illustrated in Fig. 1, TRAVEL consists of two main modules.
       guided by Rust-specific rules. These rules capture con-            Rule-Guided Reasoning Path Search Module applies MCTS with
       straints that LLMs often violate, such as ownership, bor-          Rust rule-guided constraints to explore candidate reasoning paths
       rowing and lifetimes. By steering the search toward rule-          and validates each path against our Verifiable Components (§2.2),
       compliant translation steps, this module produces higher-          propagating execution feedback through the search tree to collect
       quality reasoning trajectories for subsequent training.            high-quality training triplets (𝐶, 𝑃, 𝑅), where 𝐶 is the C code, 𝑃
     • Dual-Reward RL Optimization Module: This module                    is the reasoning path, and 𝑅 is the Rust code. Dual-Reward RL
       trains a reward model to evaluate the quality of translation       Optimization Module uses these (𝐶, 𝑃, 𝑅) triplets to train a reward
       reasoning paths, and then optimizes the translation policy         model that scores reasoning path quality, initializes the policy via
       with GRPO using both reasoning-quality rewards and ex-             supervised fine-tuning, and then optimizes it with GRPO using a
       ecution feedback. This encourages the model to preserve            combined reward of an execution reward 𝑟 exec and a reasoning reward
       the semantics of the original C program while producing            𝑟 reason , encouraging the model to produce translations that are both
       Rust code that follows Rust-specific rules.                        semantically correct and Rust-compliant.
   To validate the performance of TRAVEL, We conduct experi-
ments on three datasets: xCodeEval [28], a public function-level          2.2    Module I: Rule-Guided Reasoning Path
benchmark; HW-Bench, an industrial dataset from Huawei; and                      Search
OS-Bench, a set of 107 C functions collected from the Linux ker-
                                                                          This module consists of two components. Verifiable Translation
nel. The three datasets cover complementary domains: xCodeEval
                                                                          Data Construction provides reliable feedback for semantic preserva-
focuses on advanced programming and mathematics tasks, while
                                                                          tion and constructs the verifiable data. MCTS-Based Reasoning Path
HW-Bench and OS-Bench represent industrial and real-world code
                                                                          Exploration enables the model to explicitly explore and compare
scenarios. On xCodeEval, TRAVEL consistently outperforms all
                                                                          alternative translation trajectories under rule-guided constraints.
baselines across three backbone LLMs, achieving average gains of
35.61% in computational accuracy (CA) and 30.08% in compilation
                                                                          2.2.1 Verifiable Components Construction. Evaluating whether a
success rate (CSR). On HW-Bench and OS-Bench, TRAVEL further
                                                                          translated Rust program preserves the semantics of the original
improves CSR by 18.28% and 16.51%, while reducing unsafe rate
                                                                          C code is essential but challenging, as most C-to-Rust datasets
(UR) by 13.06% and 13.08%, respectively. These results show that
                                                                          lack executable test suites. To address this, we introduce Verifiable
TRAVEL is effective for both benchmark programs and real-world
                                                                          Components, which attach test inputs and reference outputs to each
C-to-Rust migration scenarios.
                                                                          C function for semantic verification.
   In summary, our main contributions are as follows:
                                                                              Given a C function, we prompt a strong LLM (Qwen2.5-Coder-
     • We identify two key challenges in LLM-based C-to-Rust              32B-Instruct) to generate 5 test inputs, execute them on the original
       translation: the limited ability of LLMs to follow Rust-specific   program, and collect the outputs. These input-output pairs form
       rules, and the lack of mechanisms to improve reasoning             the Verifiable Components. To verify a Rust translation, we execute
       quality for semantic preservation.                                 it on the same inputs and compare outputs with the references; the
     • We propose TRAVEL, a novel LLM-based framework that                translation is considered correct if all outputs match.
       combines rule-guided MCTS and reinforcement learning.                  Verifiable Components are used throughout TRAVEL: Module I
       The Rule-Guided Reasoning Path Search module discovers             uses them to evaluate candidate reasoning paths during MCTS
       translation paths under Rust-specific rule guidance, while         search, while Module II uses them to compute execution rewards
       the Dual-Reward RL Optimization module improves se-                for reinforcement learning, enabling semantic verification without
       mantic faithfulness using reasoning-quality rewards and            pre-existing test cases.
       execution feedback.
     • We conduct extensive experiments on three datasets that            2.2.2 MCTS-Based Reasoning Path Exploration. Monte Carlo Tree
       cover a broad spectrum of domains, ranging from advanced           Search (MCTS) is a heuristic search algorithm that combines tree
       programming and mathematical tasks to industrial appli-            search with Monte Carlo sampling. It has gained prominence due to
       cations and real-world system code. The results show that          its success in applications such as AlphaGo and is particularly effec-
       TRAVEL consistently outperforms all competitive base-              tive for sequential decision-making problems with large and com-
       lines under comparable model sizes. Notably, our 7B model          plex state spaces where traditional methods become intractable [9,
       achieves performance competitive with strong proprietary           43, 44]. We adopt MCTS to explore diverse candidate reasoning
       models such as GPT-4o.                                             paths for C-to-Rust translation, where each path corresponds to
                                                                          a sequence of reasoning steps that progressively transform a C
                                                                          function into its Rust counterpart.
2   Methodology                                                               Specifically, we formulate reasoning path generation as an MCTS
In this section, we propose TRAVEL, a translation framework via           search process. Each node represents an intermediate reasoning
rule-guided reasoning path search and reinforcement learning. We          state consisting of the accumulated natural-language reasoning
first present the overview of TRAVEL and then elaborate on its            trace generated so far, while each action corresponds to generating
module details in the following subsections                               the next reasoning step conditioned on the current reasoning state.
Towards Reliable C-to-Rust Translation with Rule-Guided Reasoning and Reinforcement Learning



                                        Module Ⅰ: Rule-Guided Reasoning Path Search
        ①Verifiable Translation Data Construction                                 ② MCTS-Based Reasoning Path Exploration

                                                                                         Monte Carlo Tree Search (MCTS)
                                               Verifiable
                             LLM              Components
                                                                                                     Selection             Backpropagation      C Code
                      (Test Cases Gen)
                                                                         C Code          Expansion

           C Code                                                                                                                                 Paths
                                               Test Reference
                                               Cases Output
                                                                                                                     ...   Evaluation
                                                                          Rules
                                                                        Prompting                                                               Rust code
                          Execution




                                              Module Ⅱ: Dual-Reward RL Optimization
    ③③Reasoning
      Reasoning Reward
                 RewardModel
                        ModelTraining
                              Training                                                ④ RL Optimization With GRPO
                                                                                               Reasoning Reward
                                                                               �1                                                �1                         �1
             C Code                   Reasoning Score
                                                                               �2               Paths
                                                                                                          Reward
                                                                                                                 S               �2          Group          �2
                                                                                                           Model                             Comput
              Paths
                                                                               ...             Execution Reward
                                                                                                                                 ...          ation         ...
                                                                Policy Model   ��                                                ��                       ��
                          Reward Model
            Rust code                         Loss                                         Rust Code      Execution




                                                                Figure 1: Overview of TRAVEL.


   During MCTS, TRAVEL starts with the initial state as the root                      deliberately designed to elicit a two-stage reasoning process within
and systematically grows the search tree by adding new nodes.                         each path: the model first analyzes the source C function’s seman-
Within the context of C-to-Rust translation, we customize the four                    tics and then determines how to realize it in Rust by leveraging
key operations of the MCTS algorithm as follows:                                      a Rust-specific translation rule library. Building upon prior C-to-
   Selection. Starting from the root node 𝑠 0 , the tree T𝑘 is traversed              Rust translation studies [12], we summarize and extend this rule
by repeatedly selecting the child with the highest PUCT score [38]                    library (Table 1), which provides structured guidance for generat-
until an unexpanded node is reached. PUCT uses the LLM’s prior                        ing Rust-specific reasoning steps during path construction. This
probability of each action together with visit-based statistics to                    semantics-then-rules organization ensures that every candidate
balance exploitation of high-value paths and exploration of under-                    path jointly attends to behavioral correctness and Rust-specific id-
visited ones. Formally, at state 𝑠𝑡 we select                                         iomatic compliance, providing the dual-objective supervision later
                                                    √︄                              consumed by Module II.
                                                         𝑁 parent (𝑎)                   Evaluation. When a node 𝑠𝑡 contains a complete Rust transla-
    𝑎𝑡 = arg max 𝑄ˆ (𝑠𝑡 , 𝑎) + 𝑐 puct 𝜋𝜃𝑘 (𝑎 | 𝑠𝑡 )
                   
                                                                        , (1)
             𝑎∈ T𝑘                                     1 + 𝑁 (𝑠𝑡 , 𝑎)              tion, we evaluate it with the source function’s Verifiable Components
                                                                                    by executing the translation on the recorded test inputs and assign-
where 𝑄ˆ (𝑠𝑡 , 𝑎) is the estimated action value, 𝜋𝜃𝑘 (𝑎 | 𝑠𝑡 ) is the LLM’s           ing a binary reward:
prior over actions, 𝑁 (𝑠𝑡 , 𝑎) is the visit count of 𝑎 at 𝑠𝑡 , 𝑁 parent (𝑎)                                                (
is the visit count of its parent, and 𝑐 puct controls the exploration                                                  +1,          if all test cases pass,
                                                                                                        𝑉ˆ (𝑠𝑡 ) = 𝑟 =                                            (2)
weight. To bias selection toward idiomatic Rust translations, we                                                       −1,          if any test case fails,
guide the LLM’s action prior implicitly through rule-augmented
prompts and few-shot examples                                                         where the test cases are those stored in the Verifiable Components
   Expansion. At an unexpanded leaf 𝑠𝑡 , we prompt the LLM to                         of the original C function.
sample 𝐾 candidate next-step actions {𝑎𝑡(1) , . . . , 𝑎𝑡(𝐾 ) }, each spawn-              Backpropagation. The reward 𝑉ˆ (𝑠𝑡 ) obtained at a terminal
ing a child node 𝑠𝑡(𝑖+1) that extends the current partial translation.                node is propagated backward along the selected path, updating
To obtain promising steps, in-context exemplars instruct the LLM                      the visit counts and action value estimates of all ancestor nodes.
to wrap every reasoning step between <step> and </step>, and                          Concretely, for each state-action pair (𝑠, 𝑎) on the path, the visit
we truncate generation at the first closing tag. The exemplars are                    count is incremented as 𝑁 (𝑠, 𝑎) ← 𝑁 (𝑠, 𝑎) + 1, and the action value
                                                                                                                                                                        Luo et al.


Table 1: Selected Rust translation rules derived from the translation prompt used in TRAVEL. Each rule is illustrated with a
representative C-to-Rust transformation example. The complete rules can be found in our repository [16].

 Rule                                Description                             C Source                                               Rust Target
 Replace malloc with Ownership       Use ownership types such as Box<T> int *p = malloc(sizeof(int)); *p =                          let mut p = Box::new(42i32);
                                     or Vec<T> instead of malloc.       42;
 Automatic Memory Management         Do not manually free memory; rely on    free(p);                                               (implicit drop when p goes out of scope)
                                     Rust’s ownership and drop system.
 NULL Return Handling                Convert functions returning NULL into   int* find() { return NULL; }                           fn find() -> Option<i32> { None }
                                     Option<T> or Result<T, E>.
 Pointer to Reference                Prefer &T / &mut T over raw pointers    int x; int *p = &x;                                    let x: i32 = 0; let p = &x;
                                     when borrowing semantics allow.


is updated by averaging the propagated rewards:                                            The objective follows the standard language modeling loss:
                                           (𝑠,𝑎)
                                         𝑁∑︁                                                                                    𝑁
                                    1                                                                                   1 ∑︁
                   𝑄ˆ (𝑠, 𝑎) ←                   𝑉ˆ (𝑠𝑡(𝑖 ) ),               (3)                          Lrm = −             log 𝑝𝜙 (𝑣𝑖 | 𝐶𝑖 , 𝑃𝑖 , 𝑅𝑖 )                      (5)
                                 𝑁 (𝑠, 𝑎) 𝑖=1                                                                           𝑁 𝑖=1

where 𝑉ˆ (𝑠𝑡(𝑖 ) ) ∈ +1, −1 is the terminal reward defined in Eq. (2)                   This formulation can be viewed as implicit regression via generative
for the 𝑖-th simulation passing through (𝑠, 𝑎). This process encour-                    modeling, where continuous reward signals are learned through
ages future selections to favor trajectories that consistently lead to                  next-token prediction [3, 33]. Compared to execution-based super-
correct translations. Finally, we aggregate the mean of node value                      vision alone, it provides a denser training signal for evaluating
estimates along each reasoning path as its overall score, which is                      reasoning quality despite sparse binary outcomes from compilation
used to assess the quality of the generated reasoning trajectory.                       and testing.
   After the search terminates, each explored path yields a training
                                                                                        2.3.2 Policy Initialization. Before reinforcement learning, we ob-
triplet (𝐶, 𝑃, 𝑅), where 𝐶 is the input C code, 𝑃 is the reasoning
                                                                                        tain an initial policy model 𝜋𝜃 through a cold-start training stage.
path with its estimated value, and 𝑅 is the resulting Rust transla-
                                                                                        Specifically, the model is first supervised on the high-quality search
tion. These triplets serve as supervision data for the reinforcement
                                                                                        data collected from Module I, so that it learns to generate Rust code
learning stage in Module II.
                                                                                        conditioned on structured reasoning paths. Formally, for each train-
                                                                                        ing example (𝐶𝑖 , 𝑃𝑖 , 𝑅𝑖 ), the policy is optimized with the standard
2.3     Module II: Dual-Reward RL Optimization                                          autoregressive objective:
The goal of this module is to optimize the translation model using
                                                                                                                                  𝑁
the search data collected in Module I. While the Rule-Guided Rea-                                                        1 ∑︁
soning Path Search module identifies promising reasoning paths                                              Lsft = −           log 𝜋𝜃 (𝑃𝑖 , 𝑅𝑖 | 𝐶𝑖 ).                         (6)
                                                                                                                         𝑁 𝑖=1
for individual training instances, this module enables the model
to internalize and reinforce such reasoning patterns for C-to-Rust                      This initialization provides a reasonable behavioral prior over the
translation. To this end, we introduce a dual-reward reinforcement                      task, enabling well-formed reasoning paths and translations.
learning framework that jointly optimizes reasoning quality and
execution outcomes.                                                                     2.3.3 Dual-Reward GRPO Optimization. After cold-start initializa-
   Let the data collected from Module I be represented as                               tion, we further optimize the policy model using Group Relative
                                                                                        Policy Optimization (GRPO) [20].
                                                  𝑁
                        D = {(𝐶𝑖 , 𝑃𝑖 , 𝑅𝑖 , 𝑣𝑖 )}𝑖=1                        (4)
                                                                                            Optimization Objective. For each input C function 𝐶, GRPO [20]
where 𝐶𝑖 denotes the input C code, 𝑃𝑖 denotes the reasoning path                        samples a group of 𝐺 outputs {𝑜 (𝑘 ) }𝐺          𝑘=1
                                                                                                                                             from the previous policy
explored by MCTS, 𝑅𝑖 denotes the corresponding Rust translation                         𝜋𝜃 old , where each 𝑜 (𝑘 ) = (𝑃 (𝑘 ) , 𝑅 (𝑘 ) ) pairs a reasoning path with its
generated along that path, and 𝑣𝑖 denotes the reasoning path value                      resulting Rust translation. The current policy 𝜋𝜃 is then updated
estimated by MCTS through verification-based evaluation and back-                       by maximizing
propagation. Intuitively, 𝑣𝑖 quantifies the quality of a reasoning path
in terms of its ability to produce translations that satisfy the exe-                   JGRPO (𝜃 ) = E𝐶, {𝑜 (𝑘 ) }∼𝜋𝜃         (· |𝐶 )
                                                                                                                        old
cutable test cases.                                                                                        𝐺 
                                                                                                      1   ∑︁
                                                                                                                 min 𝜌𝑘 (𝜃 ) 𝐴 (𝑘 ) , clip(𝜌𝑘 (𝜃 ), 1 − 𝜀, 1 + 𝜀) 𝐴 (𝑘 )
                                                                                                                                                                                 
2.3.1 Reward Model Training. We train a reward model to esti-                                         𝐺
                                                                                                          𝑘=1
mate the quality of reasoning paths and their resulting translations.                                                                   
Instead of explicit regression, we formulate reward prediction as                                      − 𝛽 DKL 𝜋𝜃 ∥ 𝜋𝜃 ref                   ,
a conditional generation task and train the model via supervised                                                                                                 (7)
fine-tuning (SFT). Given a triplet (𝐶𝑖 , 𝑃𝑖 , 𝑅𝑖 ), the model is trained                where 𝜌𝑘 (𝜃 ) = 𝜋𝜃 (𝑜 (𝑘 ) | 𝐶)/𝜋𝜃 old (𝑜 (𝑘 ) | 𝐶) is the importance ratio,
to generate the corresponding path value 𝑣𝑖 from Module I.                              𝜀 is the clipping range, and 𝛽 controls the KL penalty strength.
Towards Reliable C-to-Rust Translation with Rule-Guided Reasoning and Reinforcement Learning


   The advantage 𝐴 (𝑘 ) is computed by normalizing rewards within                     Table 2: Code characteristics statistics of HW-Bench and OS-
the sampled group, eliminating the need for a separate value net-                     Bench.
work:
                           𝑟 (𝑘 ) − mean({𝑟 ( 𝑗 ) }𝐺𝑗=1 )                              Benchmark #Samp. Avg. LOC Avg. Depth Max Depth Avg. Derefs.
                𝐴 (𝑘 ) =                                  ,    (8)
                                  std({𝑟 ( 𝑗 ) }𝐺𝑗=1 )                                 HW-Bench         100     15.33     0.611       0.890        2.22
where 𝑟 (𝑘 ) = 𝑟 (𝐶, 𝑃 (𝑘 ) , 𝑅 (𝑘 ) ) is the combined reward defined above.           OS-Bench         107     26.02     0.607       0.851        4.45
  The KL divergence is estimated via the unbiased estimator:
                   𝜋𝜃 (𝑜 (𝑘 ) | 𝐶)        𝜋𝜃 (𝑜 (𝑘 ) | 𝐶)
   DKL 𝜋𝜃 ∥ 𝜋𝜃 ref = ref (𝑘 )        − log ref (𝑘 )        − 1, (9)                   rules, so that each path jointly strengthens semantic understanding
                       𝜋𝜃 (𝑜   | 𝐶)         𝜋𝜃 (𝑜    | 𝐶)                             and syntactic handling; Module II’s reinforcement learning further
where 𝜋𝜃 ref is the SFT-tuned reference policy obtained before re-                    consolidates both capabilities in the translation model itself.
inforcement learning. This term keeps the updated policy from
drifting excessively from the reference, ensuring training stability.                 3 Experimental Setup
   Execution Reward. The execution reward evaluates the final Rust                    3.1 Research Questions
translation based on executable outcomes. Given a generated Rust                      To evaluate the effectiveness of TRAVEL, we investigate the follow-
program 𝑅, we first check whether it compiles successfully. If com-                   ing research questions:
pilation fails, a penalty of −1 is assigned. Otherwise, we execute
                                                                                               RQ1: How effective is TRAVEL across different model scales
𝑅 on the test cases derived from the Verifiable Components of the
                                                                                                 for C-to-Rust translation?
original C program, and compute the pass rate:
                                                                                               RQ2: How do the major components of TRAVEL contribute
                                          𝑛 pass
                         PassRate(𝑅) =            ,               (10)                           to the final performance?
                                          𝑛 total                                              RQ3: How does TRAVEL perform in industrial scenarios?
   where 𝑛 pass and 𝑛 total denote the number of passed and total test
cases, respectively. If no test case is passed, we assign a reward of                 3.2       Datasets
−1; otherwise, the reward equals the pass rate. Formally,
                                                                                      Training Set. We construct a training dataset based on the training
                      
                      
                       −1,             if 𝑅 fails to compile,                        split of xCodeEval [28], comprising 16,639 samples. Each sample
                                                                                      consists of the original C source code, a sequence of reasoning
                      
                      
          𝑟 exec (𝑅) = −1,              if PassRate(𝑅) = 0,       (11)
                      
                       PassRate(𝑅), otherwise.
                                                                                     paths produced by the Rule-Guided Reasoning Path Search module
                                                                                     of TRAVEL in Section 2, and the corresponding Rust translation,
This design enforces strong penalties for syntactically invalid or                    where both the C and Rust programs have been validated against
completely incorrect programs, while providing graded feedback                        test cases. We partition the data into training and validation sets at
for partially correct translations.                                                   a 9:1 ratio.
   Reasoning Reward. The reasoning reward evaluates the quality                          Evaluation Set. We construct three evaluation sets to com-
of the generated reasoning path and its associated translation using                  prehensively assess the effectiveness of TRAVEL. First, we select
the learned reward model:                                                             515 samples from the evaluation split of xCodeEval, where each
                                                                                      C code sample passes all test cases and has a corresponding Rust
                      𝑟 reason (𝐶, 𝑃, 𝑅) = 𝑓𝜙 (𝐶, 𝑃, 𝑅).                  (12)        implementation. To further evaluate the applicability of TRAVEL
Unlike the execution reward, which only reflects the quality of the                   in real-world open-source and industrial scenarios, we build two
final output, the reasoning reward provides additional supervision                    additional benchmarks. The first one, OS-Bench, contains 107 open-
on the intermediate translation process. It encourages the model to                   source C functions collected from the Linux kernel repository [46].
generate structured and rules-aware reasoning paths that are more                     We choose Linux kernel code because it represents large-scale,
likely to lead to reliable translations.                                              production-quality system software with complex control flow,
                                                                                      low-level memory manipulation, and strict requirements on correct-
  Final Reward. We combine the two reward components into a
                                                                                      ness and safety. These characteristics make it highly aligned with
unified reward:
                                                                                      practical enterprise-level C-to-Rust migration demands, while also
          𝑟 (𝐶, 𝑃, 𝑅) = 𝜆exec 𝑟 exec (𝑅) + 𝜆reason 𝑟 reason (𝐶, 𝑃, 𝑅),    (13)        posing substantial challenges for automated translation. The sec-
where 𝜆exec and 𝜆reason are balancing coefficients. This design allows                ond one, HW-Bench, consists of 100 C functions randomly sampled
the policy to optimize both the final translation quality and the                     from proprietary projects provided by Huawei, covering diverse
reasoning process that leads to it.                                                   industrial scenarios. Table 2 further reports the statistics of code
   Through this dual-reward GRPO optimization, the policy model                       characteristics for both benchmarks.
is encouraged not only to produce correct final translations, but
also to generate reasoning paths that are more likely to lead to                      3.3       Baseline Methods
semantically faithful and Rust-compliant Rust programs. In this                       In C-to-Rust translation experiments, we compare TRAVEL with
way, Module II complements Module I: guided by carefully designed                     baselines as detailed below. Instruction provides the C code along
few-shot exemplars, the reasoning paths in Module I first reason                      with the prompt ‘Translate the following C code to Rust’ with-
about the source program’s semantics and then apply Rust-specific                     out any additional demonstration. In-context Learning (ICL) [5]
                                                                                                                                       Luo et al.


includes several translation examples in the prompt to help the              Computational Accuracy (CA) evaluates whether the candi-
model generate the target Rust code. Retrieval-augment genera-            date translation generates the same outputs as the reference when
tion (RAG) [14] retrieves examples from the corpus similar to the         given the same inputs. It can be formally defined as:
target translation C code and includes them in the input prompt.                                     Í𝑁
Vert [51] uses an LLM with a two-stage refinement process. It first                                       𝑐𝑎(𝑦𝑘 , 𝑦ˆ𝑘 )
                                                                                             CA = 𝑘=1                                   (14)
applies compiler-suggested fixes to the source code, then feeds the                                  (      𝑁
updated code and diagnostics back into the LLM for further cor-                                        1, if 𝐸𝑥𝑒𝑐𝑘 (𝑦𝑘 ) = 𝐸𝑥𝑒𝑐𝑘 (𝑦ˆ𝑘 )
rection. IRENE [32] integrates Rust-specific rules and source-code                   𝑐𝑎(𝑦𝑘 , 𝑦ˆ𝑘 ) =                                    (15)
                                                                                                       0, otherwise
semantics into an LLM-based C-to-Rust translation pipeline, using
rule-guided prompting to steer the model toward safer and more            where 𝑁 is the total number of evaluated code samples. 𝑦𝑘 and 𝑦ˆ𝑘
idiomatic translations. SFT [52] fine-tunes the backbone model on         represent the ground truth and the generated translation for the
our training set using standard supervised learning. It can be viewed     𝑘-th sample, respectively. 𝐸𝑥 ∈𝐶𝑘 (·) denotes the execution result of
as an ablated variant of TRAVEL that removes the reinforcement            a program on the 𝑘-th test case. The indicator function ca(𝑦𝑘 , 𝑦ˆ𝑘 )
learning stage.                                                           equals 1 if both outputs match, and 0 otherwise.
                                                                             Compilation Success Rate (CSR) measures the percentage of
                                                                          translated programs that successfully compile without errors.
3.4    Implementation Details                                                To evaluate the translation safety, following prior work [56], we
Model selection and setup. We use Qwen2.5-Coder-Instruct at               use the metrics below:
7B and 3B scales [26] and CodeGemma-7B-Instruct [45] as the back-            Unsafe Rate (UR) refers to the proportion of unsafe samples in
bone models for training. To provide a comprehensive comparison,          the dataset.
we further include larger open-source models, including Qwen2.5-             Unsafe Loc Rate (ULR) denotes the ratio of unsafe lines of
Coder-14B/32B-Instruct and Qwen3-Coder-30B-Instruct [50], as              code within each individual sample.
well as closed-source proprietary models such as GPT-4o, GPT-4o-
mini [1], GPT-5.4-mini [36], and Claude-Haiku-4.5 [4]. We down-           4 Experimental Results
load open-source models from HuggingFace [48] and utilize Py-             4.1 RQ1: How effective is TRAVEL across
Torch [37] for local deployment and inference, while closed-source
models are accessed via their official APIs.
                                                                              different model scales for C-to-Rust
    Implementation of baselines. For ICL, we follow the prior                 translation?
work [17] and randomly sample four examples from the corpus.              To evaluate the overall effectiveness of TRAVEL, we compare TRAVEL
For RAG, we retrieve the most relevant example using the BM25             with multiple baselines on xCodeEval benchmark. Table 3 reports
algorithm. For Vert, we directly use the replication packages re-         the results, from which we derive the following findings:
leased by the authors and adapt them to our tasks. For IRENE, we             Simple prompting yields limited gains in LLMs’ transla-
select the example with the highest similarity and apply one itera-       tion ability for C-to-Rust. As shown in Table 3, the prompting-
tion of refinement. For TRAVEL, the final reward is computed with         based baselines have limited effectiveness in enhancing model
𝜆𝑒𝑥𝑒𝑐 = 𝜆𝑟𝑒𝑎𝑠𝑜𝑛 = 0.5, and Qwen2.5-Coder-32B-Instruct is used as          translation capabilities. For instance, Qwen2.5-Coder-7B-Instruct
the backbone model for MCTS.                                              with IRENE only reaches 51.84% CA and 83.88% CSR, while the
    Hyperparameter and environment settings. For the MCTS-                remaining prompting variants cluster between 34.56% and 38.83%
based reasoning path exploration module, we set the maximum               CA. Moreover, prompting baselines generally perform poorly on
number of reasoning steps per search episode to 5. For the GRPO-          Codegemma-7B-Instruct; with the exception of IRENE, all other
based reinforcement learning training, we use the VERL frame-             methods achieve at most 19.42% CA and 36.12% CSR. These results
work [40] with the following hyperparameters: the number of can-          suggest that, without parameter-level adaptation, neither in-context
didate samples per prompt 𝐺 = 8, the KL divergence coefficient            examples nor retrieval can teach the model to internalize Rust’s se-
𝛽 = 0.001, the clipping range 𝜀 = 0.2, the learning rate = 1 × 10−6 , a   mantic and syntactic constraints, the dual challenge that motivates
training batch size of 32 prompts (each with 8 sampled responses),        TRAVEL.
2 training epochs, and a maximum sequence length of 4096 to-                 TRAVEL effectively improves models’ translation capabil-
kens. We adopt LoRA [25] for parameter-efficient training with            ities in C-to-Rust, particularly in semantic understanding
rank 𝑟 = 32, scaling factor 𝛼 = 64, and dropout rate = 0. As for the      and Rust-specific rules syntactic handling. As shown in Ta-
hyperparameters of generation, we configure all LLMs with greedy          ble 3, models augmented with TRAVEL demonstrate substantial
decoding (temperature = 0, top-p = 1) to produce deterministic out-       improvements across all metrics. The model achieves strong perfor-
puts. We execute Python programs with Python 3.10.0 and compile           mance after SFT, and further improvements are obtained through
all Rust programs with Rust 1.81.0. All experiments are conducted         subsequent reinforcement learning. For Codegemma-7B-Instruct,
on an Ubuntu-20.04 server equipped with four NVIDIA A100 GPUs.            applying TRAVEL improves performance by 48.19% and 50.26%
                                                                          in terms of CA and CSR on average across all baselines. Notably,
                                                                          TRAVEL outperforms the state-of-the-art baseline SFT by 3.69%
3.5    Performance Metrics                                                and 0.78% on the same metrics. Similarly, for Qwen2.5-Coder-7B-
To evaluate the translation accuracy, we use the following two            Instruct, TRAVEL yields consistent improvements, achieving aver-
widely used performance metrics [53] in our evaluation:                   age gains of 26.77% and 13.53% in CA and CSR, respectively. Both
Towards Reliable C-to-Rust Translation with Rule-Guided Reasoning and Reinforcement Learning


Table 3: Comparison results with baseline models in terms of translation accuracy (CA, CSR) and translation safety (UR, ULR).
The bold figures indicate the best results.

                                                                                           Translation Accuracy   Translation Safety
                                            Approach                      Size/Version
                                                                                            CA          CSR       UR         ULR
                                                                Closed-source Proprietary Models
                                          GPT-5.4-mini                      Mar. 2026      96.31      99.03       5.83       2.75
                                            GPT-4o                          Nov. 2024      69.51      93.59       5.05       2.35
                                          GPT-4o-mini                       July. 2024     58.25      85.63       5.05       1.73
                                        Claude-Haiku-4.5                    Oct. 2025      74.37      95.34       3.11       1.04
                                                                           15B+ Models
                                  Qwen2.5-Coder-32B-Instruct                   32B         59.03      87.18       0.97       0.36
                                  Qwen2.5-Coder-14B-Instruct                   14B         45.44      74.17       2.52       0.67
                                  Qwen3-Coder-30B-Instruct                     30B         52.04      76.50       4.27       1.36
                                                                   7B-level And 3B-level Models
                                                           Instruction          7B         38.83      67.57       3.11       0.49
                                                               ICL              7B         34.95      63.50       0.78       0.10
                                                              RAG               7B         34.56      63.69       0.58       0.17
                          Qwen2.5-Coder-7B-Instruct            Vert             7B         37.28      76.70       3.11       0.86
                                                             IRENE              7B         51.84      83.88       1.36       0.12
                                                               SFT              7B         68.35      87.77       0.00       0.00
                                                            TRAVEL              7B         71.07      87.38       0.00       0.00
                                                           Instruction          7B          4.08      10.87       3.50       0.32
                                                               ICL              7B         19.42      36.12       0.39       0.01
                                                              RAG               7B          9.71      24.85       0.58       0.05
                            Codegemma-7B-Instruct              Vert             7B          2.33       9.51       1.75       0.13
                                                             IRENE              7B         32.43      52.82       0.78       0.02
                                                               SFT              7B         66.99      86.21       0.78       0.03
                                                            TRAVEL              7B         70.68      86.99       0.78       0.03
                                                           Instruction          3B         18.06      36.31       0.19       0.01
                                                               ICL              3B         20.19      47.38       0.00       0.00
                                                              RAG               3B         24.66      52.43       0.00       0.00
                          Qwen2.5-Coder-3B-Instruct            Vert             3B          4.27      22.14       6.99       0.62
                                                             IRENE              3B         37.86      56.50       0.00       0.00
                                                               SFT              3B         57.86      77.48       0.00       0.00
                                                            TRAVEL              3B         59.03      75.15       0.00       0.00


SFT and the TRAVEL substantially outperform all prompting base-                       achieves 71.07% CA and 87.38% CSR on xCodeEval, outperform-
lines, confirming the strength in jointly modeling source semantics                   ing Qwen2.5-Coder-32B-Instruct (59.03% CA), Qwen3-Coder-30B-
and Rust-specific syntactic rules.                                                    Instruct (52.04% CA), and the proprietary GPT-4o-mini (58.25% CA),
   We observe that on Qwen2.5-Coder-3B/7B-Instruct, TRAVEL                            while closing most of the gap to GPT-4o (69.51% CA). Similarly,
yields slightly lower CSR than SFT. This is because our final reward                  Qwen2.5-Coder-3B-Instruct+TRAVEL attains 59.03% CA, on par
optimizes semantic correctness rather than CSR alone. Although                        with Qwen2.5-Coder-32B-Instruct that has roughly 10 times more
compilation failures are penalized, the execution reward mainly                       parameters. These results highlight that through TRAVEL, smaller
provides graded feedback through test-pass outcomes, while the                        models can achieve comparable or superior performance to much
reasoning reward encourages more semantically faithful reasoning                      larger models in C-to-Rust translation.
paths. This can make the policy less conservative than SFT, occa-                        Translation safety. Beyond accuracy, TRAVEL also signifi-
sionally introducing compilation errors while improving behavioral                    cantly improves translation safety. For instance, on Qwen2.5-Coder-
correctness.                                                                          7B-Instruct, TRAVEL reduces UR and ULR by 1.49% and 0.29% on
   Small models augmented with TRAVEL outperform some                                 average compared to all baselines. Notably, it also demonstrates sub-
larger models. By comparing models of different sizes, we find that                   stantial advantages over strong closed-source models; for example,
smaller models enhanced with TRAVEL can outperform substan-                           on CodeGemma-7B-Instruct, TRAVEL achieves average reductions
tially larger ones. For example, Qwen2.5-Coder-7B-Instruct+TRAVEL                     of 3.98% and 1.94% in UR and ULR, respectively, compared to the
                                                                                      four closed-source models shown in Table 3. This indicates that the
                                                                                                                                   Luo et al.


                                                                          Effect of the execution reward. As shown in Table 4, removing
xCodeEval
                                                                       the execution reward (-w/o Execution Reward) leads to a consistent
                                                                       degradation in performance across all three backbones. For ex-
HW-Bench
                                                                       ample, on Qwen2.5-Coder-3B-Instruct, CA drops from 59.03% to
                                                                       55.92% and CSR falls from 75.15% to 71.65%. This confirms that
OS-Bench
                                                                       execution-level feedback provides a concrete and verifiable signal
                                                                       that complements the more abstract reasoning-path reward and
                                                                       anchors the optimization in observable behavior.
                                                                          Effect of reinforcement learning. As shown in Table 4, re-
                                                                       moving the dual-reward RL stage (-w/o RL (SFT with Paths)) results
Figure 2: Application domain distributions of xCodeEval,               in performance declines across all three backbones. For example,
HW-Bench and OS-Bench.                                                 CA drops from 71.07% to 68.35% on Qwen2.5-Coder-7B-Instruct and
                                                                       from 70.68% to 66.99% on Codegemma-7B-Instruct. The marginal
                                                                       CSR rise on the two Qwen backbones reflects a shift in optimization
rule-guided search effectively internalizes Rust safety constraints    behavior: without RL, the model produces more conservative code
during training.                                                       that favors compilation, while dual-reward RL encourages semanti-
                                                                       cally richer reasoning that may occasionally introduce compilation
                                                                       errors. Overall, this trade-off is favorable, as CA gains outweigh
      Answer to RQ1: TRAVEL consistently improves C-to-                the small CSR fluctuations.
      Rust translation across backbones of different families and         Effect of reasoning-path construction. Comparing SFT w/o
      scales: it outperforms all same-scale baselines, matches or      Paths against SFT with Paths isolates the contribution of the MCTS-
      exceeds open-source models up to an order of magnitude           constructed reasoning paths. Across all three backbones, remov-
      larger, and narrows the gap to leading proprietary LLMs,         ing the reasoning paths degrades both metrics. For example, on
      while producing markedly safer Rust code with near-zero          Qwen2.5-Coder-7B-Instruct, CA drops from 68.35% to 67.18% and
      unsafe usage.                                                    CSR drops from 87.77% to 83.30%, indicating that the structured
                                                                       reasoning paths supply explicit semantic and rule-level guidance
                                                                       that plain input–output pairs cannot offer.
4.2     RQ2: How do the major components of
        TRAVEL contribute to the final
        performance?                                                         Answer to RQ2: The major components of TRAVEL
                                                                             jointly drive the final performance. Reasoning-path con-
To quantify the contribution of the major components of TRAVEL,              struction contributes the largest single gain, especially
we conduct an ablation study across all three backbone models, as            on smaller backbones, and the RL stage brings further
shown in Table 4:                                                            consistent improvements in CA across all backbones. The
       • -w/o Reasoning Reward: remove the reasoning-path qual-              reasoning-path and execution rewards play complemen-
          ity reward, retaining only the execution reward during RL.         tary roles: the former favors semantic validity, while the
       • -w/o Execution Reward: remove the execution reward,                 latter balances semantic validity and compilability, and
          retaining only the reasoning-path quality reward during            combining them yields the best overall balance on larger
          RL.                                                                backbones.
       • -w/o RL (SFT with Paths): disable the RL stage and per-
          form supervised fine-tuning on the MCTS-constructed rea-
          soning paths.                                                4.3     RQ3: How does TRAVEL perform in
       • -w/o RL & Paths (SFT w/o Paths): disable both the RL                  industrial scenarios?
          stage and reasoning-path construction, and perform super-    To assess the applicability of TRAVEL in industrial scenarios, we
         vised fine-tuning only on input–output pairs.                 collaborate with Huawei and randomly select 100 C functions from
   Effect of the reasoning reward. As shown in Table 4, removing       their product-line codebase, denoted as HW-Bench. As 100 func-
the reasoning reward (-w/o Reasoning Reward) consistently lowers       tions from a single industrial codebase may not fully reflect this
CA across all three backbones. For example, CA drops from 71.07%       category of code, we additionally collect 107 C functions from the
to 70.29% on Qwen2.5-Coder-7B-Instruct and from 70.68% to 69.71%       Linux kernel, denoted as OS-Bench. Together, the two benchmarks
on Codegemma-7B-Instruct, confirming that the reasoning paths          offer a more representative view of the C code that real-world Rust
encouraged by this reward are highly effective for capturing source    migration efforts target. We apply TRAVEL to translate these func-
semantics. Interestingly, CSR increases on all backbones in this       tions into Rust and compare it against the same baselines used
setting. This is because removing the reasoning reward simplifies      in RQ1. Since no test cases are available for these proprietary or
the optimization signal, leaving the model to rely primarily on        kernel-level functions, the CA metric cannot be computed and we
execution-based feedback. As a result, the model tends to produce      report only CSR, UR, and ULR. The results are shown in Table 5.
more conservative translations that prioritize compilability, often       Comparison of translation accuracy. TRAVEL consistently
at the expense of semantic alignment.                                  achieves the highest CSR across most LLMs on both benchmarks.
Towards Reliable C-to-Rust Translation with Rule-Guided Reasoning and Reinforcement Learning


                         Table 4: Ablation study of the major components of TRAVEL on three backbone models.

                                                         Qwen2.5-Coder-3B-Instruct      Qwen2.5-Coder-7B-Instruct               Codegemma-7B-Instruct
                             Approach
                                                          CA           CSR               CA           CSR                        CA         CSR
                -w/o Reasoning Reward                    58.06          77.48           70.29               88.74               69.71              87.57
                -w/o Execution Reward                    55.92          71.65           70.10               88.54               68.35              86.99
                -w/o RL (SFT with Paths)                 57.86          77.48           68.35               87.77               66.99              86.21
                -w/o RL & Paths (SFT w/o Paths)          48.16          70.87           67.18               83.30               65.63              82.52
                TRAVEL                                   59.03          75.15           71.07               87.38               70.68              86.99


                                          Table 5: Performance comparison on HW-Bench and OS-Bench

                          Qwen2.5-Coder-3B-Instruct                         Qwen2.5-Coder-7B-Instruct                                 Codegemma-7B-Instruct
   Approach
                      HW-Bench                    OS-Bench                HW-Bench                     OS-Bench                     HW-Bench                   OS-Bench
                  CSR      UR     ULR      CSR      UR       ULR    CSR      UR      ULR       CSR       UR       ULR       CSR         UR      ULR       CSR         UR       ULR
  Instruction    20.00    22.00    6.98   6.54      28.04 10.29     20.00   25.00   9.14       10.28     46.73    17.70     9.00      12.00     3.27      2.80      15.89      4.58
      ICL        22.00    14.00    2.75   24.30     19.63 7.46      26.00   35.00   10.02      12.15     25.23    7.62      17.00     14.00     2.75     12.15      25.23      7.62
     RAG         27.00    17.00    5.28   13.08     25.23 10.15     36.00   38.00   10.53      12.15     35.51    13.22     14.00     20.00     8.66      6.54      23.36      7.27
      Vert       40.00    33.00   11.02   14.02     26.17 8.09      35.00   45.00   14.59      28.97     60.75    20.76     22.00     25.00     5.06      9.35      18.69      5.27
    IRENE        39.00    33.00   11.38   17.76     37.38 14.90     30.00   23.00   7.87       23.36     42.99    15.63     31.00     13.00     4.01     15.89      21.50      5.40
      SFT        49.00    11.00    1.88   28.04     9.35 2.18       51.00   10.00   2.14       41.12     27.10     5.50     35.00      7.00     1.15     13.08      4.67       1.67
    TRAVEL       49.00    5.00    0.67    40.19     10.28    1.91   54.00   19.00    5.69      38.32    24.30     4.14     39.00      3.00      0.29     19.63       8.41      1.59


For example, Qwen2.5-Coder-3B-Instruct augmented with TRAVEL                                         QWC’s solution                              TRAVEL’s solution
improves CSR by 16.17% on HW-Bench and 22.90% on OS-Bench.                                                                Syntax
                                                                                                         Question                                        Question
Across the three models, TRAVEL yields average CSR improve-                                                                issue
ments of 18.28% and 16.51%, respectively. These results indicate
                                                                                            fn main() {                                  1. Understand the C program functionality.
that TRAVEL is effective at producing syntactically valid Rust code                             ...
                                                                                                let a = [
for complex industrial programs.                                                                    [numbers[0], numbers[1],             2. Identify the required Rust input structure
   Comparison of translation safety. In terms of safety, Table 5                            numbers[2]],
                                                                                                    [numbers[3], numbers[4],             and program form.
shows that TRAVEL achieves the lowest UR and ULR across most                                numbers[5]],
                                                                                                    [numbers[6], numbers[7],
LLMs. On average, TRAVEL reduces UR and ULR by 13.06% and                                   numbers[8]],                                 3. Apply translation rules and reason
                                                                                                ];                                       about Rust equivalents. The 3x3 C array
4.37% on HW-Bench, respectively, and by 13.08% and 6.64% on                                     a[0][0] = x;
                                                                                                                                         int a[3][3] can be represented in Rust as
                                                                                                a[1][1] = y;
OS-Bench. These results highlight the superiority of TRAVEL in                                  a[2][2] = z;                             a Vec<Vec<i32>> with a fixed size of
                                                                                                ...                                      3x3.
generating safer Rust code compared to other baselines.                                     }                                                                ...
   Overall, the results indicate that TRAVEL not only performs reli-                                                                         fn main() {
                                                                                            Compilation Error                                    ...
ably in the public benchmark, but also generalizes well to industrial                       Reason: `a` is not declared as `mut`,                let mut a: Vec<Vec<i32>> =
scenario. To further characterize the used benchmarks, following                            but its array elements are modified              vec![vec![0; 3]; 3];
                                                                                            later; t                                             ...
prior work [6], we analyze their application-domain distribution                                                                                 a[0][0] = x;
                                                                                            Corresponding Rust Rule: Bindings                    a[1][1] = y;
                                                                                            are immutable by default in Rust, and                a[2][2] = z;
(Fig. 2). Both contain a substantially higher proportion of operating-                      you cannot modify elements of an                     ...
                                                                                                                                             }
system and system-interaction code than xCodeEval, and OS-Bench                             immutable array.

in particular consists entirely of OS-level functions. Given that the                                                                               Pass all test cases

two benchmarks exhibit similar properties, TRAVEL’s strong per-
formance on these benchmarks further shows its robustness in
                                                                                      Figure 3: A case demonstrating that Rule-guided MCTS can
handling real-world systems code.
                                                                                      effectively apply Rust-specific rules to avoid syntax issues.
                                                                                      QWC refers to Qwen2.5-Coder-7B-Instruct, which is also
                                                                                      used as the backbone of our tool.
     Answer to RQ3: TRAVEL improves syntactic validity and
     safety in industrial scenarios. Across HW-Bench and OS-
     Bench under three LLMs, TRAVEL achieves an average                               5 Discussion
     absolute improvement of 17.40% in CSR, together with                             5.1 Why Does TRAVEL Work?
     average reductions of 13.07% in UR and 5.50% in ULR over
     baselines.                                                                       In this section, we identify the following two advantages of TRAVEL,
                                                                                      which can explain its effectiveness in C-to-Rust translation. For
                                                                                                                                                        Luo et al.


           SFT’s solution                             TRAVEL’s solution                    5.2    Threats to Validity
                Question          Semantic                    Question                     For our study, we discuss the following threats to validity.
                                    issue                                                      Dependence on the underlying LLMs. The effectiveness of
       1. Understand the C program               1. Understand the C program
                                                                                           TRAVEL may be influenced by the capability of the base LLM used
       functionality. It simplifies the          functionality. Calculate the difference   for reasoning path generation and translation. Stronger models
       result using the GCD, and                 and divide it by the GCD of the
       prints the simplified fraction.           difference and the larger value.          may generate better candidate reasoning paths during MCTS, while
                                                                                           weaker models may limit the quality of both search and reinforce-
       2. Identify the required Rust                2. Identify the required Rust          ment learning. To mitigate this threat, we evaluate TRAVEL on
       input structure and program                  input structure and program
       form.                                        form.
                                                                                           multiple representative LLMs rather than relying on a single model.
                     ...                                           ...                     The consistent improvements across models suggest that the ef-
                                                                                           fectiveness of TRAVEL does not depend on a specific backbone
    fn main() {                              fn main() {                                   alone.
        ...                                      ...
        let g = gcd(diff, ad);                   let max_val = if a * d > b * c                Imperfect verification from LLM-generated test cases. Our
        let numerator = diff / g;                    {a * d}
        let denominator = ad / g;                else {b * c};                             framework relies on LLM-generated tests to construct Verifiable
        ...
    }                                               let g = gcd(diff, max_val);            Components for evaluation and reinforcement learning rewards.
                                                    let numerator = diff / g;
                                                    let denominator = max_val / g;
    Failed test input: 1 1 3 2                      ...                                    While this enables scalable semantic verification, such tests may not
    Output: 1/2 Expected output: 1/3         }
                                                                                           fully cover corner cases, so translated programs may pass tests yet
    Reason: Step 1 fails to specify that
    the denominator should be the larger                                                   deviate from the original C code on unseen inputs. Prior work [53]
    cross product value when simplifying.                 Pass all test cases
                                                                                           shows that even a 7B model can achieve 87.20% line coverage with
                                                                                           five generated tests, suggesting that LLM-generated tests can pro-
Figure 4: A case showing that dual-reward reinforcement                                    vide reasonably strong coverage. Given that we use a stronger
learning further enhances the model’s semantic understand-                                 model (Qwen2.5-Coder-32B-Instruct), we expect comparable or
ing compared to SFT. All models used here are based on the                                 better coverage. To mitigate this threat, we generate multiple test
same backbone, QWC-7B-Instruct.                                                            inputs per function and ground all outputs by executing the orig-
                                                                                           inal C program. Nevertheless, our evaluation reflects test-based
                                                                                           semantic verification rather than full formal equivalence.
                                                                                               Potential data leakage. As pretraining datasets are not pub-
                                                                                           licly available, we cannot completely rule out potential data leakage.
each advantage, we demonstrate the corresponding cases, as shown                           Nevertheless, the limited performance of standard prompting sug-
in Fig. 3 and Fig. 4.                                                                      gests that any such effect is unlikely to be significant. The notable
   Advantage 1: Rule-guided MCTS enables the model to han-                                 improvements brought by our framework further indicate that the
dle Rust-specific syntactic rules. A common failure of vanilla                             observed gains are attributable to our method rather than simple
LLM translation is the violation of Rust-specific constraints (e.g.,                       memorization by the models. Overall, these results support the
ownership, borrowing, lifetimes, and FFI signatures) that have                             robustness of our approach and its ability to generalize beyond
no direct counterpart in C. As shown in Fig. 3, the QWC base-                              potential training data overlap.
line produces a candidate that looks plausible but breaks Rust’s
borrow-checker rule, leading to a compilation failure. In contrast,
TRAVEL provides rule-aware guidance during each expansion step
via prompt conditioning, which biases the search toward rule-
consistent reasoning paths. As a result, the search converges on a                         6     Related Work
translation that simultaneously respects the language-specific rules                       Rule-based techniques apply hand-crafted transformations on top
and preserves the original behavior. This mechanism explains why                           of compiler infrastructures to map C idioms onto Rust counterparts.
TRAVEL consistently improves CSR across all backbones.                                     A representative example is C2Rust [27], a Clang/LLVM-based
   Advantage 2: Dual-reward reinforcement learning improves                                pipeline that produces syntactically equivalent but largely unsafe
semantic reasoning. SFT provides reasoning supervision but does                            Rust through the C-Rust FFI, and follow-up work extends it along
not ensure that reasoning paths lead to behavior-preserving Rust                           complementary dimensions, including pointer aliasing [11, 12],
code. As shown on the left of Fig. 4, the SFT-only model produces                          concurrent lock APIs [22], ownership inference for pointer-type
syntactically valid Rust, but fails to capture a key semantic con-                         conversion [55], and generics and standard-library substitution [24,
straint: the denominator should use the larger cross-product value,                        49]. While interpretable, these approaches rely on expert-defined
resulting in incorrect behavior.                                                           rules and have limited coverage for real-world programs [21].
   Our dual-reward RL addresses this by combining a paths reward,                             LLM-based methods instead cast translation as a sequence gen-
which favors rule-aligned reasoning steps, and an execution reward,                        eration task and exploit cross-language patterns learned from large
which favors translations that pass the test suite. These signals                          code corpora. Vert [51] combines few-shot prompting with compiler
guide the model to improve both intermediate reasoning and final                           feedback, while several approaches incorporate program analysis or
outputs. As shown on the right of Fig. 4, GRPO enables the same                            hybrid pipelines for iterative repair [35, 56]. Other methods further
QWC backbone to correctly identify the larger cross-product value,                         focus on rewriting raw pointers and eliminating residual safety
producing behavior-preserving code that passes all tests.                                  defects. [15, 18].
Towards Reliable C-to-Rust Translation with Rule-Guided Reasoning and Reinforcement Learning


   In contrast, TRAVEL integrates rule-guided MCTS with rein-                              [10] Cybersecurity and Infrastructure Security Agency (CISA). 2023. The Urgent
forcement learning to jointly improve rule compliance and seman-                                Need for Memory Safety in Software Products. https://www.cisa.gov/news-
                                                                                                events/news/urgent-need-memory-safety-software-products. Accessed: 2026-
tic preservation, producing translations that are both compilable                               04-30.
and behaviorally faithful.                                                                 [11] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and
                                                                                                Ben Hardekopf. 2023. Aliasing Limits on Translating C to Safe Rust. Proc. ACM
                                                                                                Program. Lang. 7, OOPSLA1 (2023), 551–579. doi:10.1145/3586046
7    Conclusion                                                                            [12] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Trans-
                                                                                                lating C to safer Rust. Proc. ACM Program. Lang. 5, OOPSLA (2021), 1–29.
In this paper, we propose TRAVEL, an LLM-based framework for                                    doi:10.1145/3485498
C-to-Rust translation. TRAVEL improves translation quality by                              [13] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria Chris-
                                                                                                takis, Brandon Paulsen, Joey Dodds, and Daniel Kroening. 2024. Towards Trans-
combining rule-guided reasoning-path search with reinforcement                                  lating Real-World Code with LLMs: A Study of Translating to Rust. CoRR
learning to enhance both rule compliance and semantic preserva-                                 abs/2405.11514 (2024). arXiv:2405.11514 doi:10.48550/ARXIV.2405.11514
tion. Extensive experiments demonstrate that TRAVEL consistently                           [14] Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin,
                                                                                                Tat-Seng Chua, and Qing Li. 2024. A Survey on RAG Meeting LLMs: Towards
improves translation accuracy across multiple models and datasets.                              Retrieval-Augmented Large Language Models. In KDD. ACM, 6491–6501.
Ablation studies further confirm the effectiveness of each module.                         [15] Muhammad Farrukh, Smeet Shah, Baris Coskun, and Michalis Polychronakis.
                                                                                                2025. Safetrans: Llm-assisted transpilation from c to rust. arXiv preprint
In future work, we plan to integrate the TRAVEL-trained model                                   arXiv:2505.10708 (2025).
into an agent-based migration framework to support repository-                             [16] Luo feng hitsz. 2026. Luo-feng-hitsz/TRAVEL: v1.0.0. doi:10.5281/zenodo.21132684
level C-to-Rust migration through cross-function reasoning and                             [17] Shuzheng Gao, Xin-Cheng Wen, Cuiyun Gao, Wenxuan Wang, Hongyu Zhang,
                                                                                                and Michael R. Lyu. 2023. What Makes Good In-Context Demonstrations for
dependency analysis. We also plan to construct sandbox-based                                    Code Intelligence Tasks with LLMs?. In 38th IEEE/ACM International Conference
execution environments for larger industrial codebases to enable                                on Automated Software Engineering, ASE 2023, Luxembourg, September 11-15, 2023.
more scalable and rigorous semantic validation, while extending                                 IEEE, 761–773. doi:10.1109/ASE56229.2023.00109
                                                                                           [18] Yifei Gao, Chengpeng Wang, Pengxiang Huang, Xuwei Liu, Mingwei Zheng,
the framework to support additional programming languages.                                      and Xiangyu Zhang. 2025. Pr2: Peephole raw pointer rewriting with llms for
                                                                                                translating c to safer rust. arXiv preprint arXiv:2505.04852 (2025).
                                                                                           [19] Google Project Zero. 2021. Memory Safety and the Prevalence of Ex-
Data Availability Statement                                                                     ploitable Vulnerabilities. https://googleprojectzero.blogspot.com/2021/02/a-year-
                                                                                                of-windows-kernel-exploitation.html. Accessed: 2026-04-30.
All data and code are publicly available at [16].                                          [20] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu,
                                                                                                Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. 2025. DeepSeek-R1 incen-
                                                                                                tivizes reasoning in LLMs through reinforcement learning. Nature 645, 8081
References                                                                                      (2025), 633–638.
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-         [21] Jaemin Hong. 2023. Improving Automatic C-to-Rust Translation with Static
     cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal                   Analysis. In 45th IEEE/ACM International Conference on Software Engineering:
     Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774              ICSE 2023 Companion Proceedings, Melbourne, Australia, May 14-20, 2023. IEEE,
     (2023).                                                                                    273–277. doi:10.1109/ICSE-COMPANION58688.2023.00074
 [2] Alexandru Agache, Marc Brooker, Andreea Florescu, Alexandra Iordache, An-             [22] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An Automatic C-to-Rust Lock
     thony Liguori, Rolf Neugebauer, Phil Piwonka, and Diana-Maria Popa. 2020. Fire-            API Translator for Concurrent Programs. In 45th IEEE/ACM International Confer-
     cracker: Lightweight Virtualization for Serverless Applications. In 17th USENIX            ence on Software Engineering, ICSE 2023, Melbourne, Australia, May 14-20, 2023.
     Symposium on Networked Systems Design and Implementation (NSDI 20). USENIX                 IEEE, 716–728. doi:10.1109/ICSE48619.2023.00069
     Association, 419–434. https://www.usenix.org/conference/nsdi20/presentation/          [23] Jaemin Hong and Sukyoung Ryu. 2024. To Tag, or Not to Tag: Translating C’s
     agache                                                                                     Unions to Rust’s Tagged Unions. In ASE. ACM, 40–52.
 [3] Yash Akhauri, Bryan Lewandowski, Cheng-Hsi Lin, Adrian N Reyes, Grant C               [24] Jaemin Hong and Sukyoung Ryu. 2025. Forcrat: Automatic I/O API Translation
     Forbes, Arissa Wongpanich, Bangding Yang, Mohamed S Abdelfattah, Sagi Perel,               from C to Rust via Origin and Capability Analysis. In 2025 40th IEEE/ACM
     and Xingyou Song. 2025. Performance prediction for large systems via text-to-              International Conference on Automated Software Engineering (ASE) (Seoul, Korea,
     text regression. arXiv preprint arXiv:2506.21718 (2025).                                   Republic of). IEEE Press, 1541–1552. doi:10.1109/ASE63991.2025.00130
 [4] Anthropic. 2023. Introducing Claude. https://www.anthropic.com/index/                 [25] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean
     introducing-claude. Anthropic Blog (2023). Accessed: 2026-04-27.                           Wang, Liang Wang, Weizhu Chen, et al. 2022. Lora: Low-rank adaptation of large
 [5] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan,                    language models. Iclr 1, 2 (2022), 3.
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda            [26] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu
     Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan,              Liu, Jiajun Zhang, Bowen Yu, Keming Lu, Kai Dang, Yang Fan, Yichang Zhang,
     Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter,                 An Yang, Rui Men, Fei Huang, Bo Zheng, Yibo Miao, Shanghaoran Quan, Yunlong
     Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin            Feng, Xingzhang Ren, Xuancheng Ren, Jingren Zhou, and Junyang Lin. 2024.
     Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya                  Qwen2.5-Coder Technical Report. arXiv preprint arXiv:2409.12186 (2024).
     Sutskever, and Dario Amodei. 2020. Language Models are Few-Shot Learners. In          [27] Immunant. 2022. C2Rust. https://github.com/immunant/c2rust.
     NeurIPS.                                                                              [28] Mohammad Abdullah Matin Khan, M. Saiful Bari, Xuan Do Long, Weishi Wang,
 [6] Yao Cheng, Jianfeng Chen, Jie Chen, Li Chen, Liyu Chen, Wentao Chen, Zhengyu               Md. Rizwan Parvez, and Shafiq Joty. 2024. XCodeEval: An Execution-based Large
     Chen, Shijie Geng, Aoyan Li, Bo Li, Bowen Li, Linyi Li, Boyi Liu, Jerry Liu, Kaibo         Scale Multilingual Multitask Benchmark for Code Understanding, Generation,
     Liu, Qi Liu, Shukai Liu, Siyao Liu, Tianyi Liu, Tingkai Liu, Yongfei Liu, Rui Long,        Translation and Retrieval. In Proceedings of the 62nd Annual Meeting of the
     Jing Mai, Guanghan Ning, Z. Y. Peng, Kai Shen, Jiahao Su, Jing Su, Tao Sun,                Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024,
     Yifan Sun, Yunzhe Tao, Guoyin Wang, Siwei Wang, Xuwu Wang, Yite Wang,                      Bangkok, Thailand, August 11-16, 2024, Lun-Wei Ku, Andre Martins, and Vivek
     Zihan Wang, Jinxiang Xia, Liang Xiang, Xia Xiao, Yongsheng Xiao, Chenguang                 Srikumar (Eds.). Association for Computational Linguistics, 6766–6805. doi:10.
     Xi, Shulin Xin, Jingjing Xu, Shikun Xu, Hongxia Yang, Jack Yang, Yingxiang                 18653/V1/2024.ACL-LONG.367
     Yang, Jianbo Yuan, Jun Zhang, Yufeng Zhang, Yuyu Zhang, Shen Zheng, He Zhu,           [29] Chris Lattner and Vikram S. Adve. 2004. LLVM: A Compilation Framework for
     and Ming Zhu. 2024. FullStack Bench: Evaluating LLMs as Full Stack Coders.                 Lifelong Program Analysis & Transformation. In 2nd IEEE / ACM International
     CoRR abs/2412.00535 (2024). arXiv:2412.00535 doi:10.48550/ARXIV.2412.00535                 Symposium on Code Generation and Optimization (CGO 2004), 20-24 March 2004,
 [7] Catalin Cimpanu. 2019. Microsoft: 70 percent of all security bugs are memory               San Jose, CA, USA. IEEE Computer Society, 75–88. doi:10.1109/CGO.2004.1281665
     safety issues. ZDNet. https://www.zdnet.com/article/microsoft-70-percent-of-          [30] Michael Ling, Yijun Yu, Haitao Wu, Yuan Wang, James R. Cordy, and Ahmed E.
     all-security-bugs-are-memory-safety-issues/.                                               Hassan. 2022. In Rust We Trust - A Transpiler from Unsafe C to Safer Rust. In
 [8] Thomas Claburn. 2023. Microsoft is busy rewriting core Windows library code                ICSE-Companion. ACM/IEEE, 354–355.
     in memory-safe Rust. The Register. https://www.theregister.com/2023/04/27/            [31] LLVM Project. [n. d.]. Clang: A C Language Family Frontend for LLVM. https:
     microsoft_windows_rust/.                                                                   //clang.llvm.org/. Accessed: 2025-05-26.
 [9] Rémi Coulom. 2006. Efficient selectivity and backup operators in Monte-Carlo          [32] Feng Luo, Kexing Ji, Cuiyun Gao, Shuzheng Gao, Jia Feng, Kui Liu, Xin Xia, and
     tree search. In International conference on computers and games. Springer, 72–83.          Michael Lyu. 2025. Integrating Rules and Semantics for LLM-Based C-to-Rust
                                                                                                                                                                        Luo et al.


     Translation. In Proceedings of the 41st IEEE International Conference on Software   [55] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership
     Maintenance and Evolution (ICSME). 685–696. doi:10.1109/ICSME64153.2025.                 Guided C to Rust Translation. In Computer Aided Verification - 35th International
     00069                                                                                    Conference, CAV 2023, Paris, France, July 17-22, 2023, Proceedings, Part III (Lecture
[33] Dakota Mahan, Duy Van Phung, Rafael Rafailov, Chase Blagden, Nathan Lile,                Notes in Computer Science, Vol. 13966), Constantin Enea and Akash Lal (Eds.).
     Louis Castricato, Jan-Philipp Fränken, Chelsea Finn, and Alon Albalak. 2024.             Springer, 459–482. doi:10.1007/978-3-031-37709-9_22
     Generative reward models. arXiv preprint arXiv:2410.12832 (2024).                   [56] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill
[34] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.               Levchenko, and Varun Chandrasekaran. 2025. LLM-Driven Multi-step Trans-
     C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic Tech-            lation from C to Rust using Static Analysis. CoRR abs/2503.12511 (2025).
     niques. CoRR abs/2501.14257 (2025).                                                      arXiv:2503.12511 doi:10.48550/ARXIV.2503.12511
[35] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.
     C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic Tech-
     niques. CoRR abs/2501.14257 (2025). arXiv:2501.14257 doi:10.48550/ARXIV.2501.
     14257
[36] OpenAI. 2026. GPT-5.4-mini. https://platform.openai.com. Accessed: 2026-04-30.
[37] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gre-
     gory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga,
     Alban Desmaison, Andreas Kopf, Edward Yang, Zachary DeVito, Martin Raison,
     Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and
     Soumith Chintala. 2019. PyTorch: An Imperative Style, High-Performance Deep
     Learning Library. In Advances in Neural Information Processing Systems, Vol. 32.
[38] Christopher D Rosin. 2011. Multi-armed bandits with episode context. Annals of
     Mathematics and Artificial Intelligence 61, 3 (2011), 203–230.
[39] Rust for Linux. 2024. Nova: a Rust-based GPU Driver. https://rust-for-linux.
     com/nova-gpu-driver. Accessed: 2025-05-19.
[40] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang,
     Yanghua Peng, Haibin Lin, and Chuan Wu. 2024. HybridFlow: A Flexible and
     Efficient RLHF Framework. arXiv preprint arXiv: 2409.19256 (2024).
[41] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A. Seshia, and Koushik Sen.
     2024. Syzygy: Dual Code-Test C to (safe) Rust Translation using LLMs and
     Dynamic Analysis. CoRR abs/2412.14234 (2024).
[42] Momoko Shiraishi and Takahiro Shinagawa. 2024. Context-aware Code Seg-
     mentation for C-to-Rust Translation using Large Language Models. CoRR
     abs/2409.10506 (2024).
[43] David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George
     Van Den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneer-
     shelvam, Marc Lanctot, et al. 2016. Mastering the game of Go with deep neural
     networks and tree search. nature 529, 7587 (2016), 484–489.
[44] David Silver, Julian Schrittwieser, Karen Simonyan, Ioannis Antonoglou, Aja
     Huang, Arthur Guez, Thomas Hubert, Lucas Baker, Matthew Lai, Adrian Bolton,
     et al. 2017. Mastering the game of go without human knowledge. nature 550,
     7676 (2017), 354–359.
[45] CodeGemma Team, Heri Zhao, Jeffrey Hui, Joshua Howland, Nam Nguyen,
     Siqi Zuo, Andrea Hu, Christopher A Choquette-Choo, Jingyue Shen, Joe Kelley,
     et al. 2024. Codegemma: Open code models based on gemma. arXiv preprint
     arXiv:2406.11409 (2024).
[46] Torvalds, Linus and Linux kernel contributors. 2026. Linux kernel source tree.
     https://github.com/torvalds/linux. Accessed: 2026-04-27.
[47] Jeffrey Vander Stoep and Stephen Hines. 2022. Memory Safe Languages in
     Android 13. Google Security Blog. https://security.googleblog.com/2022/12/
     memory-safe-languages-in-android-13.html.
[48] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement De-
     langue, Anthony Moi, Pierric Cistac, Timothee Rault, Remi Louf, Morgan Fun-
     towicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite,
     Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin
     Lhoest, and Alexander M. Rush. 2020. Transformers: State-of-the-Art Natural
     Language Processing. In Proceedings of the 2020 Conference on Empirical Methods
     in Natural Language Processing: System Demonstrations. 38–45.
[49] Xiafa Wu and Brian Demsky. 2025. GenC2Rust: Towards Generating Generic
     Rust Code from C . In 2025 IEEE/ACM 47th International Conference on Software
     Engineering (ICSE). IEEE Computer Society, Los Alamitos, CA, USA, 90–102.
     doi:10.1109/ICSE55347.2025.00127
[50] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng,
     Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. 2025. Qwen3 technical
     report. arXiv preprint arXiv:2505.09388 (2025).
[51] Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel
     Kroening. 2024. Vert: Verified equivalent rust transpilation with large language
     models as few-shot learners. arXiv preprint arXiv:2404.18852 (2024).
[52] Guang Yang, Yu Zhou, Xiang Chen, Xiangyu Zhang, Terry Yue Zhuo, and Taolue
     Chen. 2024. Chain-of-Thought in Neural Code Generation: From and for Light-
     weight Language Models. IEEE Trans. Softw. Eng. 50, 9 (Sept. 2024), 2437–2457.
     doi:10.1109/TSE.2024.3440503
[53] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
     Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and Unleashing the Power
     of Large Language Models in Automated Code Translation. Proc. ACM Softw.
     Eng. 1, FSE (2024), 1585–1608. doi:10.1145/3660778
[54] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership
     Guided C to Rust Translation. In CAV (3) (Lecture Notes in Computer Science,
     Vol. 13966). Springer, 459–482.
