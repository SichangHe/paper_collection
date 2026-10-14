                                                         Search, Verify and Feedback: Towards Next Generation
                                                  Post-training Paradigm of Foundation Models via Verifier Engineering


                                                           Xinyan Guan* Yanjiang Liu* Xinyu Lu* Boxi Cao Ben He Xianpei Han Le Sun
                                                                          Jie Lou† Bowen Yu† Yaojie Lu† Hongyu Lin†
                                                                                  Chinese Information Processing Laboratory,
                                                                              Institute of Software, Chinese Academy of Sciences
arXiv:2411.11504v1 [cs.AI] 18 Nov 2024




                                                                                         E-mail to: hongyu@iscas.ac.cn
                                                                           https://github.com/icip-cas/Verifier-Engineering


                                                                                                                                Feature Engineering   Data Engineering         Verifier Engineering

                                                                    Abstract                                     Representative Machine Learning
                                                                                                                 Models         Models
                                                                                                                                                      Deep Learning
                                                                                                                                                      Models
                                                                                                                                                                               Foundation Models

                                                                                                                 e.g.           SVM, XGBoost          CNN, LSTM                LLMs, VLMs
                                                 The evolution of machine learning has increas-
                                                                                                                 Supervision    Manual Features       Human Annotations        Verifier Feedback
                                                 ingly prioritized the development of powerful                   Scope          Task-Specific         Multiple Related Tasks   General Intelligence
                                                 models and more scalable supervision signals.                   Generalization Limited               Relatively high          High
                                                 However, the emergence of foundation models                     Scalability    Limited               Moderate                 High
                                                 presents significant challenges in providing ef-
                                                 fective supervision signals necessary for further              Table 1: Comparison of feature engineering, data engineer-
                                                 enhancing their capabilities. Consequently, there              ing, and verifier engineering
                                                 is an urgent need to explore novel supervision
                                                 signals and technical approaches. In this paper,
                                                 we propose verifier engineering, a novel post-
                                                 training paradigm specifically designed for the                both model capacity and the scale of supervision signals
                                                 era of foundation models. The core of verifier en-             have escalated in a synergistic manner. Powerful models
                                                 gineering involves leveraging a suite of automated             necessitate more scalable and effective supervision signals
                                                 verifiers to perform verification tasks and deliver            to fully utilize their parameters. Conversely, the expansion
                                                 meaningful feedback to foundation models. We                   of supervision signals requires models with enhanced capac-
                                                 systematically categorize the verifier engineering             ities to effectively exploit these signals, thereby achieving
                                                 process into three essential stages: search, ver-              more generalized capabilities.
                                                 ify, and feedback, and provide a comprehensive                 In the early stages of machine learning, models were con-
                                                 review of state-of-the-art research developments               strained by their limited capacity. This period was character-
                                                 within each stage. We believe that verifier engi-              ized as feature engineering, during which domain experts
                                                 neering constitutes a fundamental pathway toward               manually designed and extracted relevant features. Classical
                                                 achieving Artificial General Intelligence.                     algorithms, such as Support Vector Machines (Hearst et al.,
                                                                                                                1998) and Decision Trees (Quinlan, 1986), relied heavily on
                                                                                                                meticulously crafted features due to their architectural lim-
                                         1. Introduction                                                        itations. These algorithms achieved optimal performance
                                                                                                                through carefully designed feature extraction techniques,
                                         The evolution of machine learning (Jordan & Mitchell,
                                                                                                                with Term Frequency-Inverse Document Frequency (Robert-
                                         2015) has undergone a progressive journey characterized
                                                                                                                son et al., 2009) serving as a prominent example.
                                         by the pursuit of increasingly powerful models and the scal-
                                         ing of supervision signals (Friedland & Krell, 2018; Cao               However, as addressed increasingly complex problems, the
                                         et al., 2024; Sevilla et al., 2022). Over the past decades,            limitations of manual feature engineering became more
                                             *
                                                                                                                pronounced, underscoring the need for more scalable ap-
                                              Equal contribution.
                                             †                                                                  proaches to construct features. The emergence of deep
                                              Corresponding authors. Bowen Yu is affiliated with Qwen
                                         Team, Alibaba Group. Jie Lou is affiliated with Xiaohongshu Inc.       learning (Schmidhuber, 2015) approximately two decades
                                         This work is initiated by 4 corresponding authors in a personal        ago marked a transformative shift, inaugurating the data
                                         meeting.                                                               engineering era. This new paradigm represented a funda-

                                                                                                            1
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering


                                     Verifier Engineering
                Search                                Verify                          Feedback                    Examples
                                                                                                               RLHF
                                            Verifier
                                                                      Code
                                                                                                                                 PPO
                                                        Human      interpreter
                                                                                                               OmegaPRM
                                                                                                                                Verifier
                                                                    Reward
                                          Data Base                                                                             Guided
                                                        Rules       Model

                                                                                                               Experiential Co-Learning
                                                                                                                                 Verifier
                                         Verifier               (nearly) Golden                                                  Aware
             Candidate Response          Combinations           Verification


Figure 1: Framework of verifier engineering: The fundamental stages of verifier engineering include Search, Verify, and
Feedback. Given an instruction, the process begins with generating candidate responses (Search), followed by evaluating
these candidates using appropriate verifier combinations (Verify), and concludes with optimizing the model’s output
distribution (Feedback). This framework can explain various approaches, from training-based methods like RLHF (Ouyang
et al., 2022a) to inference-based techniques such as OmegaPRM (Luo et al., 2024b) and Experiential Co-Learning (Qian
et al., 2023). We systematically categorize existing approaches into these three stages in Table 3.


mental departure from handcrafted features, emphasizing                      struction of supervision signals beyond traditional manual
instead the curation of high-quality datasets and annotations                feature extraction and data annotation. Instead, it utilizes
to facilitate automated knowledge acquisition and pattern                    a suite of effective automated verifiers to perform verifica-
recognition across diverse domains and tasks. The remark-                    tion tasks and provide meaningful feedback to foundation
able success of landmark projects such as ImageNet (Deng                     models. Table 1 delineates the key distinctions among fea-
et al., 2009) and BERT (Brown et al., 2020a) validated the                   ture engineering, data engineering, and verifier engineering.
effectiveness of this data-centric approach.                                 This progression from annotate and learn to search and
                                                                             verify signifies a fundamental advancement in enhancing
Unfortunately, the emergence of foundation models in re-
                                                                             the capabilities of foundation models. Compared to preced-
cent years (Ouyang et al., 2022a; Touvron et al., 2023a;
                                                                             ing paradigms, verifier engineering streamlines the creation
Betker et al.; Dosovitskiy et al., 2021) has made it increas-
                                                                             of verifiers and facilitates efficient feedback to foundation
ingly difficult to enhance model capabilities solely through
                                                                             models through automated verification processes. Specif-
data engineering. Specifically, foundation models, particu-
                                                                             ically, given an instruction, verifier engineering initiates
larly large language models (LLMs) (Ouyang et al., 2022a;
                                                                             by generating candidate responses, subsequently verifying
Touvron et al., 2023a), have demonstrated extraordinary
                                                                             these candidates using appropriate combinations of veri-
abilities, increasingly matching or surpassing human per-
                                                                             fiers, and ultimately optimizes the model’s output distribu-
formance across various domains. Nevertheless, the tra-
                                                                             tion. Unlike existing methodologies such as Reinforcement
ditional data engineering approach of augmenting these
                                                                             Learning from Human Feedback (RLHF) (Stiennon et al.,
models through large-scale data construction has reached
                                                                             2020; Ouyang et al., 2022a), which depend on a limited set
its practical limitations. This limitation is evident in two
                                                                             of verifier sources and feedback mechanisms, verifier engi-
primary challenges: the difficulty and unsustainable costs
                                                                             neering integrates multiple diverse verifiers to deliver more
associated with high-quality human annotations for post-
                                                                             accurate and generalizable feedback signals. By shifting
training (Anthropic, 2024; Burns et al., 2023), and the com-
                                                                             the improvement of foundation models from a data-centric
plexity involved in providing meaningful guidance that can
                                                                             endeavor to a systematic engineering challenge, verifier en-
further enhance model performance (Wen et al., 2024a).
                                                                             gineering emphasizes the design and orchestration of com-
Consequently, the central challenge in the current era is de-
                                                                             plex verification systems to ensure effective and efficient
termining how to supply more effective supervision signals
                                                                             feedback. Analogous to how feature engineering and data
to foundation models to achieve general artificial intelli-
                                                                             engineering achieved scalability in their respective eras, we
gence capabilities.
                                                                             posit that verifier engineering represents a crucial step to-
In this paper, we propose verifier engineering, a novel post-                ward the advancement of general artificial intelligence.
training paradigm designed for the foundation model era.
                                                                             To this end, this paper provides a comprehensive exploration
The essence of verifier engineering lies in extending the con-

                                                                       2
              Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering




                                                                        Speculative Decoding (Leviathan et al., 2023); Reject
                                                Linear Search         Sampling (Yuan et al., 2023c); CoT (Wei et al., 2022); etc.
                               Search §3
                                                                             Beam Search (Vijayakumar et al., 2018);
                                                Tree Search                MCTS ;ToT (Yao et al., 2024); PoT (Luo et al.,
                                                                            2024c); CoT-SC (Wang et al., 2023d); etc.

                                                                                                    CAI (Bai et al., 2022b);
                                                                        Ranking
                                                                                                PairRM (Jiang et al., 2023a); etc.

                                                                                                   Code Interpreter (Gao et al.,
                                                                         Binary                     2023); Game Scoring Sys-
                                                                                                   tem (Tsai et al., 2023); etc.

                                                                                                  Bradley-Terry RM (Christiano
                                                 Verification                                     et al., 2017; Askell et al., 2021;
                                                    Form                                        Bai et al., 2022a); Hinge RM (Mu
                                                                         Score                  et al., 2024); Focal RM (Cai et al.,
                                                                                                2024); Cross-Entropy RM (Cobbe
                                                                                               et al., 2021; Wang et al., 2024a) etc.

                                                                                                  LLM-as-a-Judge (Zheng et al.,
                                                                                              2024a); Calculator; Browser (Nakano
                                                                          Text                  et al., 2021); Self-Critique (Saun-
                                                                                                  ders et al., 2022); Critique-of-
                                                                                                Critique (Sun et al., 2024b) ; etc.
             Verifier           Verify §4
           Engineering                                                Token-level             Value Model (Chen et al., 2024b); etc.
                                                   Verify            Thought-level             PRM (Lightman et al., 2023b); etc.
                                                 Granularity
                                                                       Trajectory-
                                                                                                 ORM (Cobbe et al., 2021); etc.
                                                                          level
                                                                                                   Self-Rewarding (Yuan et al.,
                                                                          Self-                   2024; Wu et al., 2024); Self-
                                                                       Supervised               Critique (Saunders et al., 2022);
                                                                                             Quiet-STaR (Zelikman et al., 2024); etc.
                                               Verifier Source
                                                                         Other-                 Human (Christiano et al., 2017);
                                                                       Supervised            Teacher Model (Wen et al., 2024b); etc.

                                                                        Imitation                  SFT (Ouyang et al., 2022a);
                                                                        Learning                     KD (Hinton, 2015); etc.

                                                                                                  DPO (Rafailov et al., 2024);
                                                                       Preference
                                               Training Based                                      IPO (Azar et al., 2024);
                                                                        Learning
                                                                                                KTO (Ethayarajh et al., 2024) etc.

                                                                                                  PPO (Schulman et al., 2017);
                                                                     Reinforcement
                                                                                                 PPO-max (Zheng et al., 2023);
                                                                       Learning
                              Feedback §5                                                       RLMEC (Chen et al., 2024c) etc.

                                                                                                  PRM (Lightman et al., 2023a);
                                                                     Verifier Guided                BON (Sun et al., 2024a);
                                                                                                   RAIN (Li et al., 2024a); etc.
                                                  Inference
                                                    Based                                       Self-Debug (Chen et al., 2023b);
                                                                     Verifier Aware           ReAct (Yao et al., 2022); Experiential
                                                                                               Co-Learning (Qian et al., 2023); etc.


Figure 2: Overview of verifier engineering methodologies, categorized into three main stages: Search, Verify, and Feedback.
Each stage is further broken down into specific approaches, with references to notable works in each area.




                                                                 3
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

of the verifier engineering landscape, breaking it down into           S and action a ∈ A. Specifically, in large language models,
three core stages: search, verify, and feedback. These stages          the state transition is a deterministic function. That is, once
are defined as follows:                                                the current state and selected action (the generated token)
                                                                       are given, the next state is fully determined. The search
  1. Search: Sampling representative or potentially prob-              stage of the verifier engineering thus can be regarded as
     lematic samples from model output distribution to re-             exploration in the action-state space in the condition of T .
     veal performance boundaries and limitations.
                                                                       Goal Space G represents the various goals related to model
  2. Verify: Utilizing various verifiers to provide verifica-          capabilities. Each goal g ∈ G corresponds to a specific
     tion results on candidate responses, which may include            model capability, such as code, math, writing, and so on.
     evaluation metrics, rule detection, or selective manual           The goal space is multi-dimensional and can encompass
     annotation.                                                       various aspects of model capabilities.
  3. Feedback: Leveraging verification results to enhance              Goal Distribution pg is the probability distribution over
     model performance through methods such as Super-                  goals from the goal space G . It represents the likelihood of
     vised Fine-Tuning or In-Context Learning.                         a specific goal g ∈ G being selected at any given time. This
                                                                       distribution can be learned from human feedback or other
To showcase the latest state-of-the-art research develop-              external signals.
ments in these three stages, we provide a comprehensive                Reward Function Rg (s, a) or Rg (s′ ) represents the reward
review in the remainder of this paper: Section 2 presents the          the model receives given the goal g, when taking action a
formal definition and preliminaries of verifier engineering.           from state s or at the transformed state s′ . This reward thus
Sections 3-5 detail the three fundamental stages: search,              reflects the verification result of verifier engineering for the
verify, and feedback. Section 6 discusses current trends and           specific goal g. For example, if the goal g is ”fairness,” the
limitations, followed by concluding remarks in Section 7.              reward might be based on whether the generated text avoids
                                                                       bias.
2. Verifier Engineering
                                                                       The objective for improving model capabilities can be de-
In this section, we formalize verifier engineering as a Goal-          fined as a goal-conditioned policy π : S × G × A → [0, 1]
Conditioned Markov Decision Process (GC-MDP) (Schaul                   that maximizes the expectation of the cumulative return over
et al., 2015; Plappert et al., 2018; Liu et al., 2022), enabling       the goal distribution.
a unified and systematic perspective on the field of verifier                                            "                   #
engineering. Then, we introduce how the concepts of search,                                               X
                                                                                                               t
                                                                             J(π) = Eat ∼π(·|st ,g),g∼pg      γ Rg (st , at )   (1)
verify, and feedback correspond within this modeling frame-                              st+1 ∼T (·|st ,at )   t
work, and analyze them through examples. Furthermore,
we provide a comprehensive overview of the verifier en-
                                                                       The reward function can be decomposed into sub-functions
gineering landscape by categorizing existing post-training
                                                                       for different capability dimensions:
approaches into three core stages, as summarized in Table 3.
                                                                                  Rg (s, a) = F (Rg,i (s, a) | i ∈ Sg )             (2)
2.1. Preliminary
                                                                       where Sg represents selected sub-functions for goal g, and
While LLMs are typically trained to maximize generation
                                                                       F combines their evaluations. Following Probably Approx-
likelihood given input, this objective alone cannot guarantee
                                                                       imately Correct Theory (PAC) (Vapnik, 2000), even with
desired post-training capabilities. To bridge this gap, we
                                                                       imperfect sub-functions, we can achieve reliable overall
formalize verifier engineering as a GC-MDP, denoted as
                                                                       evaluation by combining multiple weak verifiers.
tuple (S, A, T , G, Rg , pg ), where:
State Space S represents the model’s state during interac-             2.2. Verifier Engineering Overview
tion, including input context, internal states, and intermedi-
ate outputs.                                                           Building upon the GC-MDP framework, we demonstrate
                                                                       how the three stages of verifier engineering—Search, Ver-
Action Space A represents the possible token selections at             ify, and Feedback—naturally align with specific compo-
each generation step:                                                  nents of this formalism. This mapping provides both theoret-
                                                                       ical grounding and insights into how each stage contributes
                   A = {a1 , a2 , . . . , aN }
                                                                       to optimizing the policy distribution π toward desired goals.
Transition Function T typically defines the probability                As illustrated in Figure 1, the search stage can be divided
distribution over the next states, given the current state s ∈         into linear search and tree search methods. The verify stage

                                                                   4
              Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

selects appropriate verifiers and invokes them to provide              • Linear Search is a widely used search method where
verification results based on the candidate responses. The               the model starts from an initial state and proceeds step
feedback stage improve the model’s output using either                   by step, selecting one token at a time until reaching
training-based methods or inference-based methods. For                   the terminal state (Brown et al., 2020b; Wang & Zhou,
example, RLHF utilizes linear search to generate batches                 2024).
of responses, employs a reward model as the verifier, and                The key advantage of linear search is its low computa-
applies the Proximal Policy Optimization (PPO) (Schulman                 tional cost, which makes it efficient in scenarios where
et al., 2017) algorithm to optimize the model based on the               actions can be selected sequentially to progress toward
reward model’s verification result. OmegaPRM (Luo et al.,                a goal. However, a notable limitation is that if a sub-
2024a) employs a process reward model as a verifier and                  optimal action is chosen early in the process, it may be
searches for the best result based on the PRM by maximiz-                challenging to rectify the subsequent sequence. Thus,
ing the process reward scores. Experimental Co-Learning                  during the progress of verifier engineering, careful ver-
(Qian et al., 2023) collaborative verifiers through multi-               ification at each step is crucial to ensure the overall
ple LLMs, enhancing both verify and model performance                    effectiveness of the generation path.
through historical interaction data.
                                                                       • Tree Search involves exploring multiple potential ac-
In the GC-MDP framework, the three stages manifest as
                                                                         tions at each step of generation, allowing for a broader
follows: Search corresponds to action selection, where state
                                                                         exploration of the state-action space. For instance, tech-
s represents the current context or partial sequence, and
                                                                         niques like Beam Search and ToT (Yao et al., 2024)
action a denotes the next tokens to generate. Verify maps
                                                                         incorporate tree structures to enhance exploration, im-
to the reward function Rg (s, a), evaluating how well the
                                                                         proving model performance in reasoning tasks. TouT
generated outputs align with the specified goal g. Feedback
                                                                         (Mo & Xin, 2023) introduces uncertainty measurement
relates to policy distribution π optimization, maximizing
                                                                         based on Monte Carlo dropout, providing a more accu-
the expected cumulative return J(π) based on verification
                                                                         rate evaluation of intermediate reasoning processes.
results.
                                                                         This approach significantly improves the likelihood
                                                                         of discovering global optimal solution, particularly in
3. Search
                                                                         environments with complex state spaces. By simultane-
Search aims to identify high-quality generated sequences                 ously considering multiple paths, tree search mitigates
that align with the intended goals, forming the foundation               the risk of being locked into sub-optimal decisions
of verifier engineering, which is critical for evaluating and            made early on, making it more robust in guiding the
refining foundation models. However, it is impractical to                model toward an optimal outcome. However, this in-
exhaustively search the entire state-action space due to its             creased exploration comes at a higher computational
exponential growth—driven by the large vocabulary size N                 cost, making tree search more suitable for scenarios
and the maximum generation length T . To address this chal-              when the optimal path is challenging to identify. To
lenge, efficient searching, which seeks to navigate this vast            make tree search effective, the model must be continu-
space by prioritizing diverse and goal-oriented exploration,             ously verified and prioritize paths that align better with
plays a critical role in improving model’s performance.                  the goal conditions.
In this section, we first introduce how to implement diverse
search from the perspective of search structure and discuss         3.2. Additional Enhancement
additional methods for further enhancing search diversity           While search structures provide the foundational framework
after the search structure is determined.                           for navigating the state-action space, further enhancement is
                                                                    also crucial to enhance search performance. These enhance-
3.1. Search Structure                                               ments address challenges such as balancing exploration and
Search structure denotes the framework or strategy used to          exploitation, escaping local optima, and improving the di-
navigate the state-action space, which significantly influ-         versity of generated results. The enhancement strategies
ences the effectiveness and efficiency of the search process.       can be broadly categorized into two approaches: adjusting
Currently, there are two widely adopted structures for im-          exploration parameters and intervening in the original state.
plementing search: linear search and tree search. Linear
search progresses sequentially, making it effective for tasks       Adjusting Exploration Parameters Techniques such as
involving step-by-step actions, while tree search examines          Monte Carlo Tree Search (MCTS), Beam Search, and Reject
multiple paths at each decision point, making it well-suited        Sampling focus on refining the exploration process by ad-
for tasks requiring complex reasoning.                              justing parameters like temperature, Top-k (Fan et al., 2018),
                                                                    or Top-p (Holtzman et al., 2020). The challenge lies in bal-

                                                                5
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

ancing the trade-off between generating diverse outputs and            increasing gradient of information richness, providing more
maintaining high-quality sequences. For example, increas-              information to the optimization algorithm. For instance,
ing the temperature parameter promotes greater randomness,             classic Bradley–Terry reward models (Bradley & Terry,
fostering diversity but potentially reducing coherence.                1952) can provide continuous score feedback which sim-
                                                                       ply indicates correctness, while text-based feedback from
Intervening in the Original State Another enhancement                  generative reward models (Zhang et al., 2024d) and critique
approach involves modifying the initial state to guide the             models (Sun et al., 2024b) offer more detailed information,
search process toward specific goals. Methods like Chain of            potentially including rationals for scores or critiques.
Thought (CoT) (Wei et al., 2022), Logical Inference via Neu-
rosymbolic Computation (LINC) (Olausson et al., 2023),                 Perspective of Verify Granularity The verify granular-
and Program of Thoughts (PoT) (Chen et al., 2023a) exem-               ity of verifiers can be divided into three levels: token-
plify this strategy. These interventions address the challenge         level (Chen et al., 2024b), thought-level (Lightman et al.,
of overcoming biases in the default state distribution. CoT            2023a), and trajectory-level (Cobbe et al., 2021). These
enhances reasoning by introducing intermediate steps, im-              levels correspond to the scope at which the verifier engages
proving interpretability and depth in generated sequences.             with the model’s generation. Token-level verifiers focus on
LINC uses logical scenarios to encourage more structured               individual next-token predictions, thought-level verifiers
and goal-oriented outputs. Similarly, PoT provides pro-                assess entire thought steps or sentences, and trajectory-
grammatic examples that guide models toward systematic                 level verifiers evaluate the overall sequence of actions. Al-
problem-solving, effectively expanding the scope of explo-             though most RLHF practices (Ouyang et al., 2022b; Bai
ration beyond the original state distribution.                         et al., 2022a) currently rely on full-trajectory scoring, coarse-
                                                                       grained ratings are challenging to obtain accurately (Wen
4. Verify                                                              et al., 2024b), as they involve aggregating finer-grained
                                                                       verification. Generally, from the perspective of human an-
Due to the long delay and high cost associated with hu-                notators, assigning finer-grained scores is easier when the
man feedback, we cannot directly employ human efforts                  full trajectory is visible. From a machine learning perspec-
to evaluate each candidate response sampled by the model               tive, fine-grained verification is preferable (Lightman et al.,
during training (Leike et al., 2018a). Therefore, we employ            2023a), as it mitigates the risks of shortcut learning and bias
verifiers as proxies for human supervision in the training             associated with coarse-grained verification, thereby enhanc-
of foundation models. The verifiers play a crucial role in             ing generalization. A credit-assignment mechanism (Leike
search-verify-feedback pipeline, and the quality and robust-           et al., 2018b) can bridge the gap between coarse-grained
ness of the verifiers directly impact the performance of the           ratings and fine-grained verification.
downstream policy (Wen et al., 2024c).
In the context of GC-MDP, verify is typically defined as               Perspective of Verifier Source Verifiers can be divided
using a verifier that provides verification results based on           into program-based and model-based from the perspective
the current state and a predefined goal:                               of verifier source. Program-based verifiers provide deter-
                                                                       ministic verification, typically generated by predefined rules
                     F ← Rg (st−1 , at )                     (3)       or logic embedded in fixed programs. These program-based
                                                                       verifiers offer consistent and interpretable evaluations but
where F represents the verification results provided by the            may lack flexibility when dealing with complex, dynamic
verifier. g denotes the predefined goal we aim to achieve              environments. On the other hand, model-based verifiers
(e.g., helpfulness, honesty). The state s is typically com-            rely on probabilistic models to generate verification results.
posed of two concatenated components: the user’s query or              These verifiers adapt to varying contexts and tasks through
input and the model’s output content {a1 , . . . , at }.               learning, allowing for more nuanced and context-sensitive
                                                                       evaluations. However, model-based verifiers introduce an el-
In this section, we classify individual verifiers across several
                                                                       ement of uncertainty and can require significant training and
key dimensions and summarize the representative type of
                                                                       computational resources to ensure accuracy and robustness.
verifiers in Table 2.
                                                                       Perspective of Extra Training Verifiers can also be di-
4.1. A Comprehensive Taxonomy of Verifiers
                                                                       vided into two categories based on whether they require ad-
Perspective of Verification Form The verification result               ditional specialized training. Verifiers requiring additional
form of verifiers can be divided into four categories: bi-             training are typically fine-tuned on specific task-related data,
nary feedback (Gao et al., 2023), score feedback (Bai et al.,          allowing them to achieve higher accuracy in particular prob-
2022a), ranking feedback (Jiang et al., 2023a), and text feed-         lem domains (Markov et al., 2023). However, their perfor-
back (Saunders et al., 2022). These categories represent an            mance can be heavily influenced by the distribution of the

                                                                   6
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering


 Verifier Type        Verification Form         Verify Granularity                       Verifier Source   Extra Training

 Golden Annotation    Binary/Text               Thought Step/Full Trajectory             Program Based     No
 Rule-based           Binary/Text               Thought Step/Full Trajectory             Program Based     No
 Code Interpreter     Binary/Score/Text         Token/Thought Step/Full Trajectory       Program Based     No
 ORM                  Binary/Score/Rank/Text    Full Trajectory                          Model Based       Yes
 Language Model       Binary/Score/Rank/Text    Thought Step/Full Trajectory             Model Based       Yes
 Tool                 Binary/Score/Rank/Text    Token/Thought Step/Full Trajectory       Program Based     No
 Search Engine        Text                      Thought Step/Full Trajectory             Program Based     No
 PRM                  Score                     Token/Thought Step                       Model Based       Yes
 Knowledge Graph      Text                      Thought Step/Full Trajectory             Program Based     No

Table 2: A comprehensive taxonomy of verifiers across four dimensions: verification form, verify granularity, verifier
source, and the need for extra training.


training data, potentially making them less generalizable             et al., 2024), which balance interpretability with generaliza-
to different contexts. On the other hand, verifiers that do           tion capabilities. Integrating verifiers into both the training
not require extra training are often based on pre-existing            and deployment phases allows foundation models to align
models (Zelikman et al., 2024; Zheng et al., 2024a). While            more closely with safety requirements, reducing the likeli-
they may not reach the same level of accuracy as their task-          hood of unintended or harmful outputs.
specific counterparts, they are generally more robust to vari-
ations in data distribution, making them less dependent on            Reasoning In tasks requiring logical deduction or
specific training sets. This trade-off between accuracy and           problem-solving, verifiers can assess the correctness and
data sensitivity is a key consideration when selecting a veri-        coherence of each reasoning step. Token-level verifiers of-
fier for a given application.                                         fer fine-grained evaluations of individual tokens or symbols,
                                                                      which is particularly useful in mathematical computations
                                                                      and code generation (Wang et al., 2023b). Thought-level
4.2. Constructing Verifiers across Tasks
                                                                      verifiers, on the other hand, evaluate entire sentences or
Different tasks have varying requirements for verifiers, serv-        reasoning steps to ensure that each component of the ar-
ing as critical tools to enhance the performance of founda-           gument is both valid and logically consistent (Lightman
tion models. In this section, we will highlight key practices         et al., 2023a; Li et al., 2023b; Xie et al., 2024). Trajectory-
for constructing verifiers in representative fields, including        level verifiers assess the overall solution or proof, providing
safety and reasoning.                                                 comprehensive verification results on the coherence of the
                                                                      model’s reasoning (Cobbe et al., 2021; Yu et al., 2024; Wang
                                                                      et al., 2024a). For instance, in mathematical theorem prov-
Safety In safety-critical applications, verifiers play a cru-         ing, a program-based verifier like Lean (de Moura et al.,
cial role in ensuring that foundation models adhere to ethi-          2015) can check each proof step’s validity against formal
cal standards and avoid generating harmful or inappropriate           logic rules (Lin et al., 2024), while a model-based verifier
content. Program-based verifiers can enforce strict guide-            can assess the plausibility of reasoning steps through scores
lines by filtering out outputs that include prohibited con-           and natural language explanations (Zhang et al., 2024c), of-
tent, such as hate speech or sensitive personal information.          fering critiques for further refinement (Kumar et al., 2024).
For instance, a content moderation system might employ                A simpler yet widely-used approach involves using manu-
predefined keywords and patterns to identify and block of-            ally annotated correct answers as verifiers to filter model
fensive language. However, a limitation of program-based              outputs, progressively enhancing model performance (Ze-
approaches is their vulnerability to adversarial attacks, as          likman et al., 2022b).
paraphrased content can often bypass these filters (Krishna
et al., 2020). In contrast, model-based verifiers, such as            5. Feedback
toxicity classifiers (Lees et al., 2022; Markov et al., 2023;
Inan et al., 2023), offer probabilistic assessments of con-           After obtaining the verification result, we aim to enhance
tent safety, enabling more nuanced evaluations. A middle-             the capabilities of the foundation model, we define this pro-
ground approach is rule-based reward models (RRMs) (Mu                cess as the feedback stage. In this paper, feedback specifi-

                                                                  7
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

cally refers to enhancing the foundation model’s capabilities        pipeline of verifiers to check complexity, quality, and diver-
based on the verification results. The feedback stage is crit-       sity before selecting suitable data for SFT.
ical, as the effectiveness of the feedback method directly
determines whether the foundation model’s capabilities can           Preference Learning Preference Learning leverages veri-
be appropriately enhanced in response to the verification            fication results to construct pairwise comparison data and
results.                                                             employs optimization methods like DPO (Rafailov et al.,
In this section, we explore how verifier engineering uti-            2024), KTO (Ethayarajh et al., 2024), IPO (Azar et al.,
lizes search algorithms and verifiers to feedback verifica-          2024), and PRO (Song et al., 2024). Through this approach,
tion results on foundation models. To maximize the ob-               models learn to align their outputs with verifier-provided
jective function J(π), the distribution of the policy π can          preferences.
be optimized by adjusting st or the parameters of π. This            Various techniques are adopted to boost the foundation
leads to two distinct feedback approaches: training-based            model’s capabilities in specific areas through preference
feedback and inference-based feedback. Training-based                learning. For mathematical reasoning enhancement, MCTS-
feedback involves updating model parameters using data               DPO (Xie et al., 2024) combines Monte Carlo Tree
efficiently obtained through searching and verifying. In             Search (Coulom, 2006; Kocsis & Szepesvári, 2006) with
contrast, inference-based feedback modifies the output dis-          preference learning to generate and learn from step-level
tribution by incorporating search and verification results as        pairwise comparisons in an iterative online manner. For cod-
auxiliary information during inference, without altering the         ing capability improvement, CodeUltraFeedback (Weyssow
model parameters.                                                    et al., 2024) constructs pairwise training data by using LLM
                                                                     verifiers to rank code outputs, then applies preference learn-
5.1. Training-based Feedback                                         ing algorithms to optimize the model’s performance. For
We categorize the common training strategies for training-           instruction-following enhancement, Self-Rewarding (Yuan
based feedback into three types, based on the nature and             et al., 2024) enables models to generate their own verifica-
organization of the data utilized:                                   tion results for creating pairwise comparison data, followed
                                                                     by iterative self-improvement using the DPO method.

Imitation Learning Imitation Learning typically uses                 Reinforcement Learning Reinforcement Learning opti-
high-quality data selected by verifiers, employing super-            mizes models using reward signals from verifiers. Through
vised fine-tuning objectives like cross-entropy or knowledge         environmental interaction and policy updates using algo-
distillation training objectives like Kullback-Leibler diver-        rithms like PPO (Schulman et al., 2017), PPO-max (Zheng
gence (Hinton, 2015) to optimize the model.                          et al., 2023), models iteratively improve their generation
Various approaches are employed to enhance specific ca-              quality.
pabilities of the foundation model through imitation learn-          Multiple approaches are used to enhance the foundation
ing. To enhance mathematical reasoning capabilities in               model’s capabilities in specific domains using reinforce-
LLMs, approaches like STaR (Zelikman et al., 2022b) and              ment learning. For mathematical reasoning enhancement,
RFT (Yuan et al., 2023b) use rule-based verifiers to compare         Math-Shepherd (Wang et al., 2023c) implements step-wise
solution outcomes, while WizardMath (Luo et al., 2023a),             reward mechanisms to guide progressive improvement in
MARIO (Liao et al., 2024), and MetaMath (Yu et al., 2023a)           mathematical problem-solving capabilities. For coding ca-
leverage verifiers to select responses from advanced LLMs            pability improvement, methods like RLTF (Liu et al., 2023a)
or human inputs. Other methods such as MAmmoTH (Yue                  and PPOCoder (Shojaee et al., 2023a) leverage code exe-
et al., 2023) and MathCoder (Wang et al., 2023a) utilize             cution results as reward signals to guide models toward
programmatic tools to verify comprehensive and detailed              more effective coding solutions. For instruction-following
solutions. For coding capability improvement, various meth-          enhancement, approaches like InstructGPT (Ouyang et al.,
ods including Code Alpaca (Chaudhary, 2023), Wizard-                 2022a) and Llama (Touvron et al., 2023a;b; Dubey et al.,
Coder (Luo et al., 2023b), WaveCoder (Yu et al., 2023b),             2024) employ reward models trained to evaluate response
and OpenCodeInterpreter (Zheng et al., 2024b) construct              helpfulness, optimizing models for better instruction adher-
code instruction-following datasets by distilling knowledge          ence.
from advanced LLMs. To enhance instruction-following
abilities, approaches like LLaMA-GPT4 (Peng et al., 2023),
                                                                     5.2. Inference-based Feedback
Baize (Xu et al., 2023), and Ultrachat (Ding et al., 2023) em-
ploy verifiers to distill responses from advanced LLMs for           In inference-based feedback, we modify inputs or inference
supervised fine-tuning. Other methods such as Deita (Liu             strategies to obtain better outputs without changing model
et al., 2024) and MoDS (Du et al., 2023) implement a                 parameters. This approach is divided into two categories

                                                                 8
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

                                                                                 Q
based on the visibility of verification results to the model:                                          Q                     Q

verifier-guided feedback and verifier-aware feedback.

Verifier-Guided In verifier-guided feedback, verifiers
evaluate and select the most appropriate outputs from model-
generated content without direct model interaction.
                                                                              (a) SFT              (b) DPO              (c) RLHF
For example, Lightman et al. (2023a) and Snell et al. (2024)
implement tree search algorithms guided by progress re-
wards, while ToT (Yao et al., 2024) employs language model              Figure 3: A verifier engineering perspective on SFT, DPO,
verifiers to direct its tree search process. In the realm of con-       and RLHF: gray nodes represent sample paths not used
trastive decoding (Li et al., 2022; O’Brien & Lewis, 2023),             in training, while non-gray nodes represent sample paths
advanced language models serve as token logits verifiers to             actively used in the training process.
optimize output distributions.

Verifier-Aware Verifier-Aware feedback integrates veri-                 itive signal, while treating all other tokens as negatives.
fier feedback directly into a model’s operational context to            Subsequently, the foundational model is optimized through
enhance the content generation process. This approach al-               imitation learning using a cross-entropy loss function.
lows the model to actively consider and incorporate verifier
                                                                        Similarly, DPO employs a linear search strategy, maintain-
feedback while producing its output.
                                                                        ing only two distinct search paths: one corresponding to the
Various strategies are employed to enhance specific capabil-            “chosen” data derived from preference pairs and the other to
ities of foundation models through verifier-aware feedback.             the “rejected” data. The verifier treats the path associated
For mathematical and coding enhancement, CRITIC (Gou                    with the chosen data as positive signals and the path associ-
et al., 2023) utilizes feedback from calculators and code               ated with the rejected data as negative signals. Subsequently,
interpreters to refine solutions, while Self-debug (Chen                the foundational model is optimized through the application
et al., 2023b) improves code quality through execution re-              of pairwise loss functions.
sult analysis. For hallucination mitigation, approaches like
                                                                        RLHF employs a linear search strategy during the search
ReAct (Yao et al., 2022), KGR (Guan et al., 2024), and
                                                                        stage, which is further enhanced by adjusting parameters
CRITIC (Gou et al., 2023) integrate continuous feedback
                                                                        such as Top-p and temperature to promote exploration
from search engines and knowledge graphs to ensure fac-
                                                                        within the candidate response generation process. As de-
tual accuracy. In a similar vein, Self-Refine (Madaan et al.,
                                                                        picted in Figure 3(c), after search, a value function is utilized
2024) employs language model verifiers to iteratively im-
                                                                        to assign scores to each state within the generation trajec-
prove response quality.
                                                                        tory. This scoring mechanism estimates the expected return,
                                                                        thereby informing and guiding the optimization process
6. Discussion and Insights                                              through PPO algorithm.
In this section, we provide a detailed examination of the in-           By mapping these methods to the stages of verifier engineer-
sights derived from our framework. We begin by revisiting               ing, we gain a clearer understanding of how each approach
SFT, DPO, and RLHF through the lens of verifier engineer-               in the search, verify, and feedback stage enhances founda-
ing. Subsequently, we conduct an independent analysis of                tion model capabilities.
each stage within the framework. Finally, we offer a sys-
tematic evaluation of potential challenges inherent to the              6.2. Discussion on three stages of Verifier Engineering
framework as a whole.
                                                                        The three stages of verifier engineering play a distinct and
                                                                        critical role in enhancing the capabilities of foundation mod-
6.1. Revisiting SFT, DPO and RLHF from Verifier
                                                                        els. This discussion delves into current challenges and pro-
     Engineering
                                                                        poses future research directions, focusing on search effi-
Our proposed approach to verifier engineering provides a                ciency, verifier design, and the effectiveness of feedback
unified perspective on commonly used post-training algo-                methods.
rithms, offering valuable insights into their mechanisms.
                                                                        6.2.1. A DVANCED S EARCH M ETHODS
SFT generates candidate responses by employing a linear
search strategy that adheres to a singular search path de-              The efficiency and effectiveness of candidate response gen-
fined by its training data. Throughout this process, the                eration are crucial for model performance. The challenge
verifier classifies each token along the search path as a pos-          lies in balancing exploration and exploitation, as well as

                                                                    9
                 Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering




                                                  Search   Verify                             Feedback                 Task

 STar (Zelikman et al., 2022a)
                                                  Linear   Golden Annotation                  Imitation Learning       Math
 RFT (Yuan et al., 2023c)
 CAG (Pan et al., 2024)                           Linear   Golden Annotation                  Imitation Learning       RAG
 Self-Instruct (Wang et al., 2023e)               Linear   Rule-based                         Imitation Learning       General
 Code Alpaca (Chaudhary, 2023)
                                                  Linear   Rule-based                         Imitation Learning       Code
 WizardCoder (Luo et al., 2024d)
 ILF-Code (Chen et al., 2024a)                    Linear   Rule-based & Code interpreter      Imitation Learning       Code
 RAFT (Dong et al., 2023)
                                                  Linear   ORM                                Imitation Learning       General
 RRHF (Yuan et al., 2023a)
 SSO (Xiang et al., 2024)                         Linear   Rule-based                         Preference Learning      Alignment
 CodeUltraFeedback (Weyssow et al., 2024)         Linear   Language Model                     Preference Learning      Code
 Self-Rewarding (Yuan et al., 2024)               Linear   Language Model                     Preference Learning      Alignment
 StructRAG (Li et al., 2024b)                     Linear   Language Model                     Preference Learning      RAG
 LLAMA-BERRY (Zhang et al., 2024a)                Tree     ORM                                Preference Learning      Reasoning
 Math-Shepherd (Wang et al., 2024b)               Linear   Golden Annotation & Rule-based     Reinforcement Learning   Math
 RLTF (Liu et al., 2023b)
                                                  Linear   Code Interpreter                   Reinforcement Learning   Code
 PPOCoder (Shojaee et al., 2023b)
 RLAIF (Lee et al., 2023)                         Linear   Language Model                     Reinforcement Learning   General
 SIRLC (Pang et al., 2023)                        Linear   Language Model                     Reinforcement Learning   Reasoning
 RLFH (Wen et al., 2024d)                         Linear   Language Model                     Reinforcement Learning   Knowledge
 RLHF (Ouyang et al., 2022a)                      Linear   ORM                                Reinforcement Learning   Alignment
 Quark (Lu et al., 2022)                          Linear   Tool                               Reinforcement Learning   Alignment
 ReST-MCTS (Zhang et al., 2024b)                  Tree     Language Model                     Reinforcement Learning   Math
 CRITIC (Gou et al., 2024)                        Linear   Code Interpreter & Tool & Search   Verifier-Aware           Math, Code &
                                                           Engine                                                      Knowledge &
                                                                                                                       General
 Self-Debug (Chen et al., 2023c)                  Linear   Code Interpreter                   Verifier-Aware           Code
 Self-Refine (Madaan et al., 2023)                Linear   Language Model                     Verifier-Aware           Alignment
 ReAct (Yao et al., 2022)                         Linear   Search Engine                      Verifier-Aware           Knowledge
 Constrative decoding (Li et al., 2023a)          Linear   Language Model                     Verifier-Guided          General
 Chain-of-verfication (Dhuliawala et al., 2023)   Linear   Language Model                     Verifier-Guided          Knowledge
 Inverse Value Learning (Lu et al., 2024)         Linear   Language Model                     Verifier-Guided          General
 PRM (Lightman et al., 2023b)                     Linear   PRM                                Verifier-Guided          Math
 KGR (Guan et al., 2023)                          Linear   Knowledge Graph                    Verifier-Guided          Knowledge
 UoT (Hu et al., 2024)                            Tree     Language Model                     Verifier-Guided          General
 ToT (Yao et al., 2024)                           Tree     Language Model                     Verifier-Guided          Reasoning


Table 3: This paper provides a comprehensive exploration of the verifier engineering landscape, breaking it down into three
core stages: search, verify, and feedback.




                                                                  10
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

aligning the search process with specific optimization goals.          quently, we explore the complexities associated with com-
In this subsection, we first discuss the trade-off between ex-         bining multiple verifiers, highlighting the challenges that
ploration and exploitation, and then discuss how goal-aware            must be addressed to achieve comprehensive and scalable
search can further optimize the search process.                        verification systems.

Balancing Exploration and Exploitation The balance                     Verifier Design and Systematic Evaluation Designing
between exploration and exploitation is a core issue in the            specific verifiers for different types of instructions is essen-
search stage of verifier engineering. Given an instruction,            tial. For instructions with explicit output constraints (such
we need to search for candidate responses. For example, in             as grammatical format and length limitations), rule-based
DPO scenarios, we aim to obtain pair-wise responses with               verifiers should be implemented due to their definitive re-
different verification results. Regardless of the objective,           liability. For question-answering instructions, LLM-based
how to sample desired responses through the trade-off be-              verifiers are typically more effective in evaluating subjective
tween exploration and exploitation remains a key challenge.            metrics like response fluency and information content. How-
Exploration refers to exploring new action spaces to obtain            ever, recent studies (Wen et al., 2024c) have revealed only
verified results with larger variance candidate responses,             weak correlations between existing verifier evaluation met-
while exploitation utilizes known effective strategies to ob-          rics and downstream task performance, highlighting signifi-
tain responses that meet expected validation results. Ex-              cant limitations in the current verifier evaluation framework.
ploration helps foundation models better understand the                Therefore, a systematic evaluation framework is needed to
outcomes of different actions, while exploitation can obtain           comprehensively assess the effectiveness, applicable scope,
satisfactory responses at a lower cost. However, recent re-            and limitations of different types of verifiers. Such a frame-
search (Wilson, 2024; Nguyen & Satoh, 2024; Murthy et al.,             work would not only guide the selection and combination
2024) suggests that existing methods in the post-training              of verifiers but also establish best practices for verifier de-
process often rely too heavily on exploitation while neglect-          ployment across various task scenarios.
ing the importance of exploration. This imbalance may
cause foundation models to get stuck in local optima, lim-             Challenges of Verifier Combinations As mentioned
iting their generalization ability. Therefore, how to better           above, it is impossible to obtain effective verification results
balance these two strategies during training is crucial for            using a single verifier alone. Therefore, integrating multi-
improving model performance.                                           ple verifiers is essential to address the diverse requirements
                                                                       of candidate response evaluation. To comprehensively en-
                                                                       hance foundation model performance across various task
Goal-Aware Search As shown in Section 3, existing                      scenarios, an effective verifier combination system must
search methods primarily rely on probability search from               be developed. Building an effective verifier combination
the next token distribution and adjust the search direction            system faces three key challenges:
through verifier feedback. However, this approach has a fun-
damental issue: the current search approach often lacks a                 • Instruction Coverage: The verifier combination must
direct correlation with the optimization goal. Consequently,                be capable of handling various types of instructions
we cannot guide foundation models to generate candidate re-                 to ensure the completeness of the evaluation system.
sponses that meet our goals during the search stage and can                 Building a comprehensive verifier framework requires
only rely on post-hoc verification results to filter responses              a deep understanding of different task characteristics
that align with our intentions. This delayed verification                   and evaluation needs, including structured output vali-
mechanism significantly reduces search efficiency and in-                   dation, open-ended question assessment, creative task
creases computational overhead. To address this challenge,                  evaluation, etc.
search algorithms like A* (Zeng & Church, 2009) fuse the
cost of the current node with heuristic estimates of the future           • Automatic Routing Mechanism: Different tasks typ-
cost to the goal. Future work can focus on developing more                  ically require verifiers with varying forms and granu-
robust goal estimation and fusion methods.                                  larity, demanding an intelligent verifier routing system.
                                                                            This system needs to analyze instruction characteristics
6.2.2. O PEN Q UESTIONS TO V ERIFIER D ESIGN                                and select appropriate verifier combinations accord-
                                                                            ingly. Based on the PAC theory discussed in Section
Designing effective verifiers is pivotal for enhancing the                  2, the chosen verifier combinations should effectively
performance and reliability of foundation models. How-                      approximate our ultimate optimization objective.
ever, several unresolved issues remain regarding the optimal
design and integration of verifiers. In this subsection, we               • Verification Results Integration Strategy: When mul-
first examine the considerations involved in verifier design                tiple verifiers produce different verification results, a re-
and the need for systematic evaluation frameworks. Subse-                   liable decision-making mechanism is needed. This in-

                                                                  11
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

     cludes dynamic adjustment of different verifier weights,          6.3. Verifier Engineering Implementation
     conflict resolution strategies, and methods for synthe-
                                                                       In this section, we will discuss the problems we may meet
     sizing final scores. Especially, when there are differ-
                                                                       in verifier engineering implementation in different stages to
     ences in verification results, factors such as the cred-
                                                                       ensure efficiency, scalability, and reliability.
     ibility and task relevance of each verifier need to be
     considered to make reasonable judgments.
                                                                       Search Achieving high search efficiency is a key objective
                                                                       in verifier engineering. Excessive search often slows down
                                                                       the entire verifier engineering pipeline.
6.2.3. E FFECTIVENESS OF F EEDBACK M ETHODS
                                                                       To address this, most current LLM-based PPO algorithms
The effectiveness of feedback methods plays a crucial role
                                                                       sample only a single response for optimization. On the
in shaping the performance and adaptability of foundation
                                                                       other hand, RLHF-like algorithms commonly incorporate
models. In particular, we focus on two key questions: 1)
                                                                       importance sampling (Schulman et al., 2017; Xie et al.,
whether the feedback method can accurately and efficiently
                                                                       2019) techniques to enhance search efficiency, minimizing
improve the model’s performance, and 2) whether it can
                                                                       the need for frequent switching between search, verify, and
generalize effectively to other queries.
                                                                       feedback stages while simultaneously improving sample
                                                                       utilization.
Key Factors in Designing Feedback Methods Differ-
ent feedback methods have different impacts on foundation              Verify Verifier efficiency is also a key goal in verifier en-
model capabilities. When selecting feedback methods, it                gineering for giving timely and effective verification results.
is essential to carefully balance several key factors. Firstly,        When handling multiple instructions from various sources,
the algorithm should demonstrate sufficient robustness to              it’s crucial to employ different combinations of verifiers
noise in verification results, ensuring the stability of the           with different abilities to ensure accurate verification results.
feedback process. Secondly, it is crucial to assess how the            Determining the optimal approach to deploy all verifiers on-
feedback algorithm based on specific types of verification             line and dynamically schedule them each time to minimize
results impacts the model. Over-optimizing certain capabili-           resource consumption while maximizing efficiency presents
ties can undermine the model’s fundamental capabilities and            a challenging problem.
overall generalization, potentially leading to performance
degradation. Furthermore, foundation models with differ-               Delivering effective verification results involves addressing
ent capacities may require distinct optimization approaches.           two major challenges: (1) ensuring the verifier’s knowl-
Larger models might benefit from more sophisticated feed-              edge remains synchronized with the policy model, and (2)
back methods, while smaller models may need more conser-               selecting the optimal verifier combination when capabili-
vative feedback methods to prevent capacity saturation. It is          ties vary or conflict across verifiers. For instance, Instruct-
crucial to find an appropriate balance between these factors           GPT (Ouyang et al., 2022a) employs a human-annotated
while considering the model’s inherent capabilities.                   reward model as a verifier, and to counter the limitations of a
                                                                       static verifier, it periodically re-annotates reward model data
                                                                       to align its evaluation capabilities with the evolving policy
Generalization over Queries Equipped with reliable veri-               model outputs. Furthermore, Quan (2024) leverages a Mix-
fiers and effective feedback methods, the ideal scenario is to         ture of Experts architecture to combine multiple verifiers
achieve comprehensive improvements in foundation model                 with different strengths. Experiential Co-Learning (Qian
capabilities through optimization on a limited set of queries.         et al., 2023) also draws on the knowledge of diverse founda-
This necessitates feedback methods to possess strong cross-            tion models to provide more robust verification results.
query generalization abilities. Specifically, when we en-
hance certain foundation model capabilities through feed-              Feedback For highly efficient feedback, it’s essential not
back on specific queries, these improved capabilities should           only to enhance the feedback algorithm itself but also to
effectively transfer and persist when handling novel queries.          optimize the entire workflow.
However, generalization also faces significant challenges:
                                                                       To increase training and inference efficiency, LoRA (Hu
different queries may require the model to invoke distinct
                                                                       et al., 2021; Xin et al., 2024) improves training effi-
capabilities, and incorrect generalization might lead to the
                                                                       ciency by reducing the number of trainable parameters and
model inappropriately applying certain capabilities in unsuit-
                                                                       vLLM (Kwon et al., 2023) enhance inference efficiency.
able scenarios, potentially degrading performance. There-
fore, feedback methods must not only promote effective                 To optimize the entire workflow, deciding when to apply
generalization but also prevent over-generalization and in-            feedback methods is crucial (Tang et al., 2024). For training-
correct transfer of capabilities.                                      based feedback, understanding the performance gap be-

                                                                  12
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

tween online and offline feedback methods is key. Research            Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., Das-
has shown that online feedback methods can maximize the                 Sarma, N., Drain, D., Fort, S., Ganguli, D., Henighan,
capabilities of foundation models by providing timely veri-             T., et al. Training a helpful and harmless assistant with
fication results on the on-policy candidate responses, albeit           reinforcement learning from human feedback. ArXiv
requiring frequent sampling, which can be time-intensive.               preprint, abs/2204.05862, 2022a. URL https://arxiv.
In contrast, offline feedback methods enable comprehensive              org/abs/2204.05862.
response exploration by leveraging pre-prepared datasets for
                                                                      Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J.,
training, thereby streamlining the process. However, this ap-
                                                                        Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKin-
proach tends to have lower data utilization efficiency. This
                                                                        non, C., et al. Constitutional ai: Harmlessness from ai
highlights the importance of balancing online and offline
                                                                        feedback. ArXiv preprint, abs/2212.08073, 2022b. URL
feedback methods. In inference-based feedback, deciding
                                                                        https://arxiv.org/abs/2212.08073.
when to call a verifier is essential. Jiang et al. (2023b)
demonstrate that retrieval based on detecting uncertainty in          Betker, J., Goh, G., Jing, L., Brooks, T., Wang, J., Li, L.,
foundation model internal states enables the model to per-              Ouyang, L., Zhuang, J., Lee, J., Guo, Y., Manassra, W.,
form better, suggesting that invoking the verifier on demand            Dhariwal, P., Chu, C., Jiao, Y., and Ramesh, A. Improving
yields more effective and efficient outcomes for maximizing             image generation with better captions. URL https://
foundation model capabilities.                                          api.semanticscholar.org/CorpusID:264403242.
                                                                      Bradley, R. A. and Terry, M. E. Rank analysis of in-
7. Conclusion                                                           complete block designs: I. the method of paired com-
This paper introduces the concept of verifier engineering               parisons. Biometrika, 39:324, 1952. URL https:
and explores the significant shift in research paradigms from           //api.semanticscholar.org/CorpusID:125209808.
feature engineering to data engineering, and ultimately to            Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan,
verifier engineering. Our framework provides implications               J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,
and insights demonstrating that verifier engineering can                Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G.,
optimize the capabilities of foundation models through a                Henighan, T., Child, R., Ramesh, A., Ziegler, D. M.,
closed-loop feedback cycle encompassing search, verifica-               Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E.,
tion, and feedback. Furthermore, we categorize existing                 Litwin, M., Gray, S., Chess, B., Clark, J., Berner,
search algorithms based on their granularity and schemes,               C., McCandlish, S., Radford, A., Sutskever, I., and
review current verifiers, and classify feedback methods from            Amodei, D. Language models are few-shot learners.
both training-based and inference-based perspectives. Fi-               In Larochelle, H., Ranzato, M., Hadsell, R., Balcan,
nally, we discuss the challenges that verifier engineering              M., and Lin, H. (eds.), Advances in Neural Information
currently faces. Through this paper, we aim to stimulate                Processing Systems 33: Annual Conference on Neural
further discussions and promote practical applications in the           Information Processing Systems 2020, NeurIPS 2020,
field of verifier engineering for achieving Artificial General          December 6-12, 2020, virtual, 2020a. URL https:
Intelligence.                                                           //proceedings.neurips.cc/paper/2020/hash/
                                                                        1457c0d6bfcb4967418bfb8ac142f64a-Abstract.
References                                                              html.
Anthropic. Measuring the persuasiveness of language mod-              Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan,
  els, 2024. https://www.anthropic.com/research/                        J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,
  measuring-model-persuasiveness/.                                      Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G.,
                                                                        Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu,
Askell, A., Bai, Y., Chen, A., Drain, D., Ganguli, D.,                  J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M.,
  Henighan, T., Jones, A., Joseph, N., Mann, B., DasSarma,              Gray, S., Chess, B., Clark, J., Berner, C., McCandlish,
  N., et al. A general language assistant as a laboratory for           S., Radford, A., Sutskever, I., and Amodei, D. Language
  alignment. ArXiv preprint, abs/2112.00861, 2021. URL                  models are few-shot learners, 2020b. URL https://
  https://arxiv.org/abs/2112.00861.                                     arxiv.org/abs/2005.14165.
                                                                      Burns, C., Izmailov, P., Kirchner, J. H., Baker, B., Gao,
Azar, M. G., Guo, Z. D., Piot, B., Munos, R., Rowland, M.,              L., Aschenbrenner, L., Chen, Y., Ecoffet, A., Joglekar,
  Valko, M., and Calandriello, D. A general theoretical                 M., Leike, J., Sutskever, I., and Wu, J. Weak-to-strong
  paradigm to understand learning from human preferences.               generalization: Eliciting strong capabilities with weak su-
  In International Conference on Artificial Intelligence and            pervision, 2023. URL https://arxiv.org/abs/2312.
  Statistics, pp. 4447–4455. PMLR, 2024.                                09390.

                                                                 13
              Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

Cai, Z., Cao, M., Chen, H., Chen, K., Chen, K., Chen, X.,            Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., and Fei-Fei,
  Chen, X., Chen, Z., Chen, Z., Chu, P., et al. Internlm2              L. Imagenet: A large-scale hierarchical image database.
  technical report. arXiv preprint arXiv:2403.17297, 2024.             In 2009 IEEE conference on computer vision and pattern
                                                                       recognition, pp. 248–255. Ieee, 2009.
Cao, B., Lu, K., Lu, X., Chen, J., Ren, M., Xiang, H., Liu,
  P., Lu, Y., He, B., Han, X., Sun, L., Lin, H., and Yu, B.          Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X.,
  Towards scalable automated alignment of llms: A survey,              Celikyilmaz, A., and Weston, J. Chain-of-verification
  2024. URL https://arxiv.org/abs/2406.01252.                          reduces hallucination in large language models, 2023.
                                                                       URL https://arxiv.org/abs/2309.11495.
Chaudhary, S. Code alpaca: An instruction-following
  llama model for code generation. https://github.com/               Ding, N., Chen, Y., Xu, B., Qin, Y., Zheng, Z., Hu, S., Liu,
  sahil280114/codealpaca, 2023.                                        Z., Sun, M., and Zhou, B. Enhancing chat language mod-
                                                                       els by scaling high-quality instructional conversations.
Chen, A., Scheurer, J., Korbak, T., Campos, J. A., Chan,               arXiv preprint arXiv:2305.14233, 2023.
  J. S., Bowman, S. R., Cho, K., and Perez, E. Improv-
  ing code generation by training with natural language              Dong, H., Xiong, W., Goyal, D., Zhang, Y., Chow, W.,
  feedback, 2024a. URL https://arxiv.org/abs/2303.                     Pan, R., Diao, S., Zhang, J., SHUM, K., and Zhang,
  16749.                                                              T. RAFT: Reward ranked finetuning for generative
                                                                       foundation model alignment. Transactions on Machine
Chen, G., Liao, M., Li, C., and Fan, K. Alphamath almost              Learning Research, 2023. ISSN 2835-8856. URL
  zero: process supervision without process. arXiv preprint            https://openreview.net/forum?id=m7p5O7zblY.
  arXiv:2405.03553, 2024b.
                                                                     Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn,
Chen, W., Ma, X., Wang, X., and Cohen, W. W. Program                   D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer,
  of thoughts prompting: Disentangling computation from                M., Heigold, G., Gelly, S., Uszkoreit, J., and Houlsby, N.
  reasoning for numerical reasoning tasks, 2023a. URL                 An image is worth 16x16 words: Transformers for image
  https://arxiv.org/abs/2211.12588.                                    recognition at scale, 2021. URL https://arxiv.org/
                                                                       abs/2010.11929.
Chen, X., Lin, M., Schärli, N., and Zhou, D. Teaching large
  language models to self-debug, 2023b.                              Du, Q., Zong, C., and Zhang, J. Mods: Model-oriented
                                                                       data selection for instruction tuning. arXiv preprint
Chen, X., Lin, M., Schärli, N., and Zhou, D. Teaching                 arXiv:2311.15653, 2023.
  large language models to self-debug, 2023c. URL https:
  //arxiv.org/abs/2304.05128.                                        Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle,
                                                                      A., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan,
Chen, Z., Zhou, K., Zhao, W. X., Wan, J., Zhang, F., Zhang,           A., et al. The llama 3 herd of models. arXiv preprint
  D., and Wen, J.-R. Improving large language models                   arXiv:2407.21783, 2024.
  via fine-grained reinforcement learning with minimum
                                                                     Ethayarajh, K., Xu, W., Muennighoff, N., Jurafsky, D., and
  editing constraint, 2024c.
                                                                       Kiela, D. Kto: Model alignment as prospect theoretic
Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg,             optimization. arXiv preprint arXiv:2402.01306, 2024.
  S., and Amodei, D. Deep reinforcement learning from                Fan, A., Lewis, M., and Dauphin, Y. Hierarchical neural
  human preferences. Advances in neural information pro-               story generation, 2018. URL https://arxiv.org/abs/
  cessing systems, 30, 2017.                                           1805.04833.
Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,            Friedland, G. and Krell, M. A capacity scaling law for
  Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,            artificial neural networks, 2018. URL https://arxiv.
  R., Hesse, C., and Schulman, J. Training verifiers to solve          org/abs/1708.06019.
  math word problems, 2021.
                                                                     Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang,
Coulom, R. Efficient selectivity and backup operators in              Y., Callan, J., and Neubig, G. Pal: Program-aided lan-
  monte-carlo tree search. In International conference on              guage models. In International Conference on Machine
  computers and games, pp. 72–83. Springer, 2006.                      Learning, pp. 10764–10799. PMLR, 2023.
de Moura, L. M., Kong, S., Avigad, J., van Doorn, F.,                Gou, Z., Shao, Z., Gong, Y., Shen, Y., Yang, Y., Duan, N.,
  and von Raumer, J. The lean theorem prover (sys-                     and Chen, W. Critic: Large language models can self-
  tem description). In CADE, 2015. URL https://api.                    correct with tool-interactive critiquing. arXiv preprint
  semanticscholar.org/CorpusID:232990.                                 arXiv:2305.11738, 2023.

                                                                14
              Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

Gou, Z., Shao, Z., Gong, Y., Shen, Y., Yang, Y., Duan,               Jordan, M. I. and Mitchell, T. M. Machine learning: Trends,
  N., and Chen, W. Critic: Large language models can                   perspectives, and prospects. Science, 349(6245):255–260,
  self-correct with tool-interactive critiquing, 2024. URL             2015.
  https://arxiv.org/abs/2305.11738.
                                                                     Kocsis, L. and Szepesvári, C. Bandit based monte-carlo
Guan, X., Liu, Y., Lin, H., Lu, Y., He, B., Han, X., and Sun,          planning. In European conference on machine learning,
  L. Mitigating large language model hallucinations via                pp. 282–293. Springer, 2006.
  autonomous knowledge graph-based retrofitting, 2023.
  URL https://arxiv.org/abs/2311.13314.                              Krishna, K., Wieting, J., and Iyyer, M. Reformulating un-
                                                                       supervised style transfer as paraphrase generation. In
Guan, X., Liu, Y., Lin, H., Lu, Y., He, B., Han, X., and               Webber, B., Cohn, T., He, Y., and Liu, Y. (eds.), Proceed-
  Sun, L. Mitigating large language model hallucinations               ings of the 2020 Conference on Empirical Methods in
 via autonomous knowledge graph-based retrofitting. In                 Natural Language Processing (EMNLP), pp. 737–762,
 Proceedings of the AAAI Conference on Artificial Intelli-             Online, November 2020. Association for Computational
  gence, volume 38, pp. 18126–18134, 2024.                             Linguistics. doi: 10.18653/v1/2020.emnlp-main.55. URL
Hearst, M. A., Dumais, S. T., Osuna, E., Platt, J., and                https://aclanthology.org/2020.emnlp-main.55.
  Scholkopf, B. Support vector machines. IEEE Intelligent
                                                                     Kumar, A., Zhuang, V., Agarwal, R., Su, Y., Co-Reyes,
  Systems and their applications, 13(4):18–28, 1998.
                                                                       J. D., Singh, A., Baumli, K., Iqbal, S., Bishop, C.,
Hinton, G. Distilling the knowledge in a neural network.               Roelofs, R., Zhang, L. M., McKinney, K., Shrivas-
  arXiv preprint arXiv:1503.02531, 2015.                               tava, D., Paduraru, C., Tucker, G., Precup, D., Behba-
                                                                       hani, F., and Faust, A. Training language models to
Holtzman, A., Buys, J., Du, L., Forbes, M., and Choi, Y.               self-correct via reinforcement learning, 2024. URL
 The curious case of neural text degeneration, 2020. URL               https://arxiv.org/abs/2409.12917.
  https://arxiv.org/abs/1904.09751.
                                                                     Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,
Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,
                                                                      C. H., Gonzalez, J. E., Zhang, H., and Stoica, I. Efficient
  S., Wang, L., and Chen, W. Lora: Low-rank adaptation of
                                                                      memory management for large language model serving
  large language models. arXiv preprint arXiv:2106.09685,
                                                                      with pagedattention. In Proceedings of the ACM SIGOPS
  2021.
                                                                      29th Symposium on Operating Systems Principles, 2023.
Hu, Z., Liu, C., Feng, X., Zhao, Y., Ng, S.-K., Luu,
 A. T., He, J., Koh, P. W., and Hooi, B. Uncertainty                 Lee, H., Phatale, S., Mansoor, H., Mesnard, T., Ferret, J.,
  of thoughts: Uncertainty-aware planning enhances infor-              Lu, K., Bishop, C., Hall, E., Carbune, V., Rastogi, A., and
  mation seeking in large language models, 2024. URL                   Prakash, S. Rlaif: Scaling reinforcement learning from
  https://arxiv.org/abs/2402.03271.                                    human feedback with ai feedback, 2023.

Inan, H., Upasani, K., Chi, J., Rungta, R., Iyer, K.,                Lees, A., Tran, V. Q., Tay, Y., Sorensen, J., Gupta, J., Met-
  Mao, Y., Tontchev, M., Hu, Q., Fuller, B., Testug-                   zler, D., and Vasserman, L. A new generation of perspec-
  gine, D., et al. Llama guard: Llm-based input-output                 tive api: Efficient multilingual character-level transform-
  safeguard for human-ai conversations. arXiv preprint                 ers. In Proceedings of the 28th ACM SIGKDD conference
  arXiv:2312.06674, 2023.                                              on knowledge discovery and data mining, pp. 3197–3207,
                                                                       2022.
Jiang, D., Ren, X., and Lin, B. Y. LLM-blender: En-
   sembling large language models with pairwise ranking              Leike, J., Krueger, D., Everitt, T., Martic, M., Maini, V., and
   and generative fusion. In Rogers, A., Boyd-Graber, J.,              Legg, S. Scalable agent alignment via reward modeling:
   and Okazaki, N. (eds.), Proceedings of the 61st Annual              a research direction. arXiv preprint arXiv:1811.07871,
   Meeting of the Association for Computational Linguistics            2018a.
   (Volume 1: Long Papers), pp. 14165–14178, Toronto,
   Canada, July 2023a. Association for Computational Lin-            Leike, J., Krueger, D., Everitt, T., Martic, M., Maini, V., and
   guistics. doi: 10.18653/v1/2023.acl-long.792. URL                   Legg, S. Scalable agent alignment via reward modeling:
   https://aclanthology.org/2023.acl-long.792.                         a research direction, 2018b. URL https://arxiv.org/
                                                                       abs/1811.07871.
Jiang, Z., Xu, F. F., Gao, L., Sun, Z., Liu, Q., Dwivedi-Yu,
   J., Yang, Y., Callan, J., and Neubig, G. Active retrieval         Leviathan, Y., Kalman, M., and Matias, Y. Fast inference
   augmented generation. arXiv preprint arXiv:2305.06983,              from transformers via speculative decoding, 2023. URL
   2023b.                                                              https://arxiv.org/abs/2211.17192.

                                                                15
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

Li, X. L., Holtzman, A., Fried, D., Liang, P., Eisner, J.,            Liu, M., Zhu, M., and Zhang, W. Goal-conditioned rein-
  Hashimoto, T., Zettlemoyer, L., and Lewis, M. Con-                    forcement learning: Problems and solutions, 2022. URL
  trastive decoding: Open-ended text generation as opti-                https://arxiv.org/abs/2201.08299.
  mization. arXiv preprint arXiv:2210.15097, 2022.
                                                                      Liu, W., Zeng, W., He, K., Jiang, Y., and He, J. What
Li, X. L., Holtzman, A., Fried, D., Liang, P., Eisner, J.,              makes good data for alignment? a comprehensive study
  Hashimoto, T., Zettlemoyer, L., and Lewis, M. Con-                    of automatic data selection in instruction tuning. In The
  trastive decoding: Open-ended text generation as opti-                Twelfth International Conference on Learning Represen-
  mization, 2023a. URL https://arxiv.org/abs/2210.                      tations, 2024. URL https://openreview.net/forum?
  15097.                                                                id=BTKAeLqLMw.
Li, Y., Lin, Z., Zhang, S., Fu, Q., Chen, B., Lou, J.-G.,             Lu, X., Welleck, S., Hessel, J., Jiang, L., Qin, L., West, P.,
  and Chen, W. Making language models better reasoners                  Ammanabrolu, P., and Choi, Y. Quark: Controllable text
  with step-aware verifier. In Rogers, A., Boyd-Graber, J.,             generation with reinforced unlearning, 2022.
  and Okazaki, N. (eds.), Proceedings of the 61st Annual
  Meeting of the Association for Computational Linguis-               Lu, X., Wen, X., Lu, Y., Yu, B., Lin, H., Yu, H., Sun, L.,
  tics (Volume 1: Long Papers), pp. 5315–5333, Toronto,                 Han, X., and Li, Y. Transferable post-training via inverse
  Canada, July 2023b. Association for Computational Lin-                value learning, 2024. URL https://arxiv.org/abs/
  guistics. doi: 10.18653/v1/2023.acl-long.291. URL                     2410.21027.
  https://aclanthology.org/2023.acl-long.291.
                                                                      Luo, H., Sun, Q., Xu, C., Zhao, P., Lou, J., Tao, C., Geng, X.,
Li, Y., Wei, F., Zhao, J., Zhang, C., and Zhang, H. RAIN:               Lin, Q., Chen, S., and Zhang, D. Wizardmath: Empow-
  Your language models can align themselves without                     ering mathematical reasoning for large language models
  finetuning. In The Twelfth International Conference                   via reinforced evol-instruct, 2023a.
  on Learning Representations, volume abs/2309.07124,
  2024a. URL https://openreview.net/forum?id=                         Luo, L., Liu, Y., Liu, R., Phatale, S., Lara, H., Li, Y., Shu,
  pETSfWMUzy.                                                           L., Zhu, Y., Meng, L., Sun, J., and Rastogi, A. Improve
                                                                        mathematical reasoning in language models by automated
Li, Z., Chen, X., Yu, H., Lin, H., Lu, Y., Tang, Q., Huang,             process supervision, 2024a. URL https://arxiv.org/
  F., Han, X., Sun, L., and Li, Y. Structrag: Boosting                  abs/2406.06592.
  knowledge intensive reasoning of llms via inference-time
  hybrid information structurization, 2024b. URL https:               Luo, L., Liu, Y., Liu, R., Phatale, S., Lara, H., Li, Y., Shu,
  //arxiv.org/abs/2410.08815.                                           L., Zhu, Y., Meng, L., Sun, J., et al. Improve mathemati-
                                                                        cal reasoning in language models by automated process
Liao, M., Luo, W., Li, C., Wu, J., and Fan, K. Mario: Math              supervision. arXiv preprint arXiv:2406.06592, 2024b.
  reasoning with code interpreter output – a reproducible
  pipeline, 2024.                                                     Luo, X., Zhu, Q., Zhang, Z., Qin, L., Zhang, X., Yang,
                                                                        Q., Xu, D., and Che, W. Python is not always the best
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
                                                                        choice: Embracing multilingual program of thoughts,
  B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
                                                                        2024c. URL https://arxiv.org/abs/2402.10691.
  Cobbe, K. Let’s verify step by step. arXiv preprint
  arXiv:2305.20050, 2023a.                                            Luo, Z., Xu, C., Zhao, P., Sun, Q., Geng, X., Hu, W., Tao, C.,
                                                                        Ma, J., Lin, Q., and Jiang, D. Wizardcoder: Empowering
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
                                                                        code large language models with evol-instruct. arXiv
  B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
                                                                        preprint arXiv:2306.08568, 2023b.
  Cobbe, K. Let’s verify step by step, 2023b.

Lin, H., Sun, Z., Yang, Y., and Welleck, S. Lean-star:                Luo, Z., Xu, C., Zhao, P., Sun, Q., Geng, X., Hu, W., Tao,
  Learning to interleave thinking and proving, 2024.                    C., Ma, J., Lin, Q., and Jiang, D. Wizardcoder: Empow-
                                                                        ering code large language models with evol-instruct. In
Liu, J., Zhu, Y., Xiao, K., Fu, Q., Han, X., Yang, W., and Ye,          The Twelfth International Conference on Learning Rep-
  D. Rltf: Reinforcement learning from unit test feedback.              resentations, 2024d. URL https://openreview.net/
  arXiv preprint arXiv:2307.04349, 2023a.                               forum?id=UnUwSIgK5W.

Liu, J., Zhu, Y., Xiao, K., Fu, Q., Han, X., Yang, W., and Ye,        Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao,
  D. Rltf: Reinforcement learning from unit test feedback,             L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S.,
  2023b. URL https://arxiv.org/abs/2307.04349.                         Yang, Y., Gupta, S., Majumder, B. P., Hermann, K.,

                                                                 16
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

  Welleck, S., Yazdanbakhsh, A., and Clark, P. Self-                  Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.,
  refine: Iterative refinement with self-feedback. In Thirty-           Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A.,
  seventh Conference on Neural Information Processing                   et al. Training language models to follow instructions
  Systems, volume 36, pp. 46534–46594, 2023. URL                        with human feedback. Advances in neural information
  https://openreview.net/forum?id=S37hOerQLB.                           processing systems, 35:27730–27744, 2022a.

Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao,                 Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright,
 L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S.,                C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K.,
 Yang, Y., et al. Self-refine: Iterative refinement with self-          Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L.,
 feedback. Advances in Neural Information Processing                    Simens, M., Askell, A., Welinder, P., Christiano, P., Leike,
 Systems, 36, 2024.                                                    J., and Lowe, R. Training language models to follow
                                                                        instructions with human feedback, 2022b. URL https:
Markov, T., Zhang, C., Agarwal, S., Nekoul, F. E., Lee, T.,            //arxiv.org/abs/2203.02155.
 Adler, S., Jiang, A., and Weng, L. A holistic approach to
 undesired content detection in the real world. In Proceed-           Pan, R., Cao, B., Lin, H., Han, X., Zheng, J., Wang, S.,
 ings of the AAAI Conference on Artificial Intelligence,                Cai, X., and Sun, L. Not all contexts are equal: Teaching
 volume 37, pp. 15009–15018, 2023.                                      llms credibility-aware generation, 2024. URL https:
                                                                        //arxiv.org/abs/2404.06809.
Mo, S. and Xin, M. Tree of uncertain thoughts reasoning
                                                                      Pang, J.-C., Wang, P., Li, K., Chen, X.-H., Xu, J., Zhang,
 for large language models, 2023. URL https://arxiv.
                                                                        Z., and Yu, Y. Language model self-improvement by
 org/abs/2309.07694.
                                                                        reinforcement learning contemplation, 2023. URL https:
Mu, T., Helyar, A., Heidecke, J., Achiam, J., Vallone,                  //arxiv.org/abs/2305.14483.
 A., Kivlichan, I., Lin, M., Beutel, A., Schulman, J.,                Peng, B., Li, C., He, P., Galley, M., and Gao, J. Instruction
 and Weng, L. Rule based rewards for language model                     tuning with gpt-4, 2023.
 safety. Advances in Neural Information Processing Sys-
 tems, 2024.                                                          Plappert, M., Andrychowicz, M., Ray, A., McGrew, B.,
                                                                        Baker, B., Powell, G., Schneider, J., Tobin, J., Chociej,
Murthy, R., Heinecke, S., Niebles, J. C., Liu, Z., Xue, L.,             M., Welinder, P., Kumar, V., and Zaremba, W. Multi-
 Yao, W., Feng, Y., Chen, Z., Gokul, A., Arpit, D., Xu,                 goal reinforcement learning: Challenging robotics envi-
 R., Mui, P., Wang, H., Xiong, C., and Savarese, S. Rex:                ronments and request for research, 2018. URL https:
 Rapid exploration and exploitation for ai agents, 2024.                //arxiv.org/abs/1802.09464.
 URL https://arxiv.org/abs/2307.08962.
                                                                      Qian, C., Dang, Y., Li, J., Liu, W., Xie, Z., Wang, Y., Chen,
Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim,            W., Yang, C., Cong, X., Che, X., et al. Experiential co-
  C., Hesse, C., Jain, S., Kosaraju, V., Saunders, W., et al.           learning of software-developing agents. arXiv preprint
  Webgpt: Browser-assisted question-answering with hu-                  arXiv:2312.17025, 2023.
  man feedback. arXiv preprint arXiv:2112.09332, 2021.
                                                                      Quan, S. Dmoerm: Recipes of mixture-of-experts for effec-
Nguyen, H.-T. and Satoh, K. Balancing exploration and                   tive reward modeling. arXiv preprint arXiv:2403.01197,
  exploitation in llm using soft rllf for enhanced negation             2024.
  understanding. arXiv preprint arXiv:2403.01185, 2024.
                                                                      Quinlan, J. R. Induction of decision trees. Machine learning,
O’Brien, S. and Lewis, M. Contrastive decoding improves                1:81–106, 1986.
  reasoning in large language models. arXiv preprint
                                                                      Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Er-
  arXiv:2309.09117, 2023.
                                                                        mon, S., and Finn, C. Direct preference optimization:
Olausson, T., Gu, A., Lipkin, B., Zhang, C., Solar-Lezama,              Your language model is secretly a reward model. Ad-
  A., Tenenbaum, J., and Levy, R. Linc: A neurosym-                     vances in Neural Information Processing Systems, 36,
  bolic approach for logical reasoning by combining lan-                2024.
  guage models with first-order logic provers. In Pro-                Robertson, S., Zaragoza, H., et al. The probabilistic rele-
  ceedings of the 2023 Conference on Empirical Meth-                    vance framework: Bm25 and beyond. Foundations and
  ods in Natural Language Processing, pp. 5153–5176.                    Trends® in Information Retrieval, 3(4):333–389, 2009.
  Association for Computational Linguistics, 2023. doi:
  10.18653/v1/2023.emnlp-main.313. URL http://dx.                     Saunders, W., Yeh, C., Wu, J., Bills, S., Ouyang, L., Ward, J.,
  doi.org/10.18653/v1/2023.emnlp-main.313.                              and Leike, J. Self-critiquing models for assisting human

                                                                 17
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

  evaluators. ArXiv preprint, abs/2206.05802, 2022. URL               Sun, S., Li, J., Yuan, W., Yuan, R., Li, W., and Liu, P.
  https://arxiv.org/abs/2206.05802.                                     The critique of critique. ArXiv preprint, abs/2401.04518,
                                                                        2024b. URL https://arxiv.org/abs/2401.04518.
Schaul, T., Horgan, D., Gregor, K., and Silver, D. Uni-
  versal value function approximators. In Bach, F. and                Tang, Y., Guo, D. Z., Zheng, Z., Calandriello, D., Cao, Y.,
  Blei, D. (eds.), Proceedings of the 32nd International                Tarassov, E., Munos, R., Pires, B. Á., Valko, M., Cheng,
  Conference on Machine Learning, volume 37 of Pro-                     Y., et al. Understanding the performance gap between
  ceedings of Machine Learning Research, pp. 1312–1320,                 online and offline alignment algorithms. arXiv preprint
  Lille, France, 07–09 Jul 2015. PMLR. URL https:                       arXiv:2405.08448, 2024.
  //proceedings.mlr.press/v37/schaul15.html.
                                                                      Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux,
Schmidhuber, J. Deep learning in neural networks:                       M.-A., Lacroix, T., Rozière, B., Goyal, N., Hambro, E.,
  An overview. Neural Networks, 61:85–117, 2015.                        Azhar, F., et al. Llama: Open and efficient foundation lan-
  ISSN 0893-6080. doi: https://doi.org/10.1016/j.neunet.                guage models. arXiv preprint arXiv:2302.13971, 2023a.
  2014.09.003. URL https://www.sciencedirect.com/                     Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi,
  science/article/pii/S0893608014002135.                                A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P.,
                                                                        Bhosale, S., et al. Llama 2: Open foundation and fine-
Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and
                                                                        tuned chat models. arXiv preprint arXiv:2307.09288,
  Klimov, O. Proximal policy optimization algorithms,
                                                                        2023b.
  2017.
                                                                      Tsai, C. F., Zhou, X., Liu, S. S., Li, J., Yu, M., and Mei,
Sevilla, J., Heim, L., Ho, A., Besiroglu, T., Hobbhahn, M.,             H. Can large language models play text games well?
  and Villalobos, P. Compute trends across three eras of                current state-of-the-art and open questions. arXiv preprint
  machine learning. In 2022 International Joint Conference              arXiv:2304.02868, 2023.
  on Neural Networks (IJCNN), pp. 1–8. IEEE, July 2022.
  doi: 10.1109/ijcnn55064.2022.9891914. URL http://                   Vapnik, V. N. The Nature of Statistical Learning Theory.
  dx.doi.org/10.1109/IJCNN55064.2022.9891914.                           Springer, 2000.

Shojaee, P., Jain, A., Tipirneni, S., and Reddy, C. K.                Vijayakumar, A. K., Cogswell, M., Selvaraju, R. R., Sun, Q.,
  Execution-based code generation using deep reinforce-                 Lee, S., Crandall, D., and Batra, D. Diverse beam search:
  ment learning. arXiv preprint arXiv:2301.13816, 2023a.                Decoding diverse solutions from neural sequence models,
                                                                        2018. URL https://arxiv.org/abs/1610.02424.
Shojaee, P., Jain, A., Tipirneni, S., and Reddy, C. K.
  Execution-based code generation using deep reinforce-               Wang, K., Ren, H., Zhou, A., Lu, Z., Luo, S., Shi, W., Zhang,
  ment learning, 2023b. URL https://arxiv.org/abs/                     R., Song, L., Zhan, M., and Li, H. Mathcoder: Seam-
  2301.13816.                                                          less code integration in llms for enhanced mathematical
                                                                       reasoning. arXiv preprint arXiv:2310.03731, 2023a.
Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling llm test-
                                                                      Wang, K., Ren, H., Zhou, A., Lu, Z., Luo, S., Shi, W.,
  time compute optimally can be more effective than scal-
                                                                       Zhang, R., Song, L., Zhan, M., and Li, H. Mathcoder:
  ing model parameters. arXiv preprint arXiv:2408.03314,
                                                                       Seamless code integration in llms for enhanced mathe-
  2024.
                                                                       matical reasoning, 2023b. URL https://arxiv.org/
Song, F., Yu, B., Li, M., Yu, H., Huang, F., Li, Y., and Wang,         abs/2310.03731.
  H. Preference ranking optimization for human alignment.             Wang, P., Li, L., Shao, Z., Xu, R., Dai, D., Li, Y., Chen,
  In Proceedings of the AAAI Conference on Artificial In-              D., Wu, Y., and Sui, Z. Math-shepherd: A label-free
  telligence, volume 38, pp. 18990–18998, 2024.                        step-by-step verifier for llms in mathematical reasoning.
                                                                       arXiv preprint arXiv:2312.08935, 2023c.
Stiennon, N., Ouyang, L., Wu, J., Ziegler, D., Lowe, R.,
  Voss, C., Radford, A., Amodei, D., and Christiano,                  Wang, P., Li, L., Shao, Z., Xu, R. X., Dai, D., Li, Y., Chen,
   P. F. Learning to summarize with human feedback. Ad-                D., Wu, Y., and Sui, Z. Math-shepherd: Verify and
   vances in Neural Information Processing Systems, 33:                reinforce llms step-by-step without human annotations,
   3008–3021, 2020.                                                    2024a.
Sun, H., Haider, M., Zhang, R., Yang, H., Qiu, J., Yin,               Wang, P., Li, L., Shao, Z., Xu, R. X., Dai, D., Li, Y., Chen,
  M., Wang, M., Bartlett, P., and Zanette, A. Fast best-               D., Wu, Y., and Sui, Z. Math-shepherd: Verify and
  of-n decoding via speculative rejection, 2024a. URL                  reinforce llms step-by-step without human annotations,
  https://arxiv.org/abs/2410.20290.                                    2024b. URL https://arxiv.org/abs/2312.08935.

                                                                 18
              Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

Wang, X. and Zhou, D. Chain-of-thought reasoning without            Xiang, H., Yu, B., Lin, H., Lu, K., Lu, Y., Han, X., Sun, L.,
 prompting. ArXiv preprint, abs/2402.10200, 2024. URL                 Zhou, J., and Lin, J. Aligning large language models via
 https://arxiv.org/abs/2402.10200.                                    self-steering optimization, 2024. URL https://arxiv.
                                                                      org/abs/2410.17131.
Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi,
 E. H., Narang, S., Chowdhery, A., and Zhou, D. Self-               Xie, T., Ma, Y., and Wang, Y.-X. Towards optimal off-policy
 consistency improves chain of thought reasoning in lan-              evaluation for reinforcement learning with marginalized
 guage models. In The Eleventh International Confer-                  importance sampling. Advances in neural information
 ence on Learning Representations, 2023d. URL https:                  processing systems, 32, 2019.
 //openreview.net/forum?id=1PL1NIMMrw.
                                                                    Xie, Y., Goyal, A., Zheng, W., Kan, M.-Y., Lillicrap, T. P.,
Wang, Y., Kordi, Y., Mishra, S., Liu, A., Smith, N. A.,               Kawaguchi, K., and Shieh, M. Monte carlo tree search
 Khashabi, D., and Hajishirzi, H. Self-instruct: Align-               boosts reasoning via iterative preference learning. arXiv
 ing language models with self-generated instructions. In             preprint arXiv:2405.00451, 2024.
 Rogers, A., Boyd-Graber, J., and Okazaki, N. (eds.), Pro-
 ceedings of the 61st Annual Meeting of the Association             Xin, C., Lu, Y., Lin, H., Zhou, S., Zhu, H., Wang, W.,
 for Computational Linguistics (Volume 1: Long Papers),               Liu, Z., Han, X., and Sun, L. Beyond full fine-tuning:
 pp. 13484–13508, Toronto, Canada, 2023e. Association                 Harnessing the power of LoRA for multi-task instruction
 for Computational Linguistics. doi: 10.18653/v1/2023.                tuning. In Calzolari, N., Kan, M.-Y., Hoste, V., Lenci,
 acl-long.754. URL https://aclanthology.org/2023.                     A., Sakti, S., and Xue, N. (eds.), Proceedings of the
 acl-long.754.                                                        2024 Joint International Conference on Computational
                                                                      Linguistics, Language Resources and Evaluation (LREC-
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi,           COLING 2024), pp. 2307–2317, Torino, Italia, May 2024.
 E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting           ELRA and ICCL. URL https://aclanthology.org/
 elicits reasoning in large language models. Advances in              2024.lrec-main.206.
 neural information processing systems, 35:24824–24837,
 2022.                                                              Xu, C., Guo, D., Duan, N., and McAuley, J. Baize: An
                                                                      open-source chat model with parameter-efficient tuning
Wen, J., Zhong, R., Khan, A., Perez, E., Steinhardt, J.,              on self-chat data. arXiv preprint arXiv:2304.01196, 2023.
 Huang, M., Boman, S. R., He, H., and Feng, S. Language
 models learn to mislead humans via rlhf. arXiv preprint            Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
 arXiv:2409.12822, 2024a.                                             K. R., and Cao, Y. React: Synergizing reasoning and
                                                                      acting in language models. In The Eleventh International
Wen, J., Zhong, R., Khan, A., Perez, E., Steinhardt, J.,              Conference on Learning Representations, 2022.
 Huang, M., Bowman, S. R., He, H., and Feng, S. Lan-
 guage models learn to mislead humans via rlhf, 2024b.              Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y.,
 URL https://arxiv.org/abs/2409.12822.                                and Narasimhan, K. Tree of thoughts: Deliberate problem
                                                                      solving with large language models. Advances in Neural
Wen, X., Lou, J., Lu, Y., Lin, H., Yu, X., Lu, X., He, B.,            Information Processing Systems, 36, 2024.
 Han, X., Zhang, D., and Sun, L. Rethinking reward model
 evaluation: Are we barking up the wrong tree? arXiv                Yu, F., Gao, A., and Wang, B. OVM, outcome-supervised
 preprint arXiv:2410.05584, 2024c.                                    value models for planning in mathematical reasoning.
                                                                      In Duh, K., Gomez, H., and Bethard, S. (eds.), Find-
Wen, X., Lu, X., Guan, X., Lu, Y., Lin, H., He, B.,
                                                                      ings of the Association for Computational Linguistics:
 Han, X., and Sun, L. On-policy fine-grained knowl-
                                                                      NAACL 2024, pp. 858–875, Mexico City, Mexico, June
 edge feedback for hallucination mitigation, 2024d. URL
                                                                      2024. Association for Computational Linguistics. doi:
 https://arxiv.org/abs/2406.12221.
                                                                      10.18653/v1/2024.findings-naacl.55. URL https://
Weyssow, M., Kamanda, A., and Sahraoui, H. Codeultra-                 aclanthology.org/2024.findings-naacl.55.
 feedback: An llm-as-a-judge dataset for aligning large
                                                                    Yu, L., Jiang, W., Shi, H., Yu, J., Liu, Z., Zhang, Y., Kwok,
 language models to coding preferences, 2024.
                                                                      J. T., Li, Z., Weller, A., and Liu, W. Metamath: Boot-
Wilson, D.     Llm tree search.            arXiv preprint             strap your own mathematical questions for large language
 arXiv:2410.19117, 2024.                                              models. arXiv preprint arXiv:2309.12284, 2023a.
Wu, T., Yuan, W., Golovneva, O., Xu, J., Tian, Y., Jiao, J.,        Yu, Z., Zhang, X., Shang, N., Huang, Y., Xu, C., Zhao,
 Weston, J., and Sukhbaatar, S. Meta-rewarding language               Y., Hu, W., and Yin, Q. Wavecoder: Widespread and
 models: Self-improving alignment with llm-as-a-meta-                 versatile enhanced instruction tuning with refined data
 judge. arXiv preprint arXiv:2407.19594, 2024.                        generation. arXiv preprint arXiv:2312.14187, 2023b.

                                                               19
               Towards Next Generation Post-training Paradigm of Foundation Models via Verifier Engineering

Yuan, H., Yuan, Z., Tan, C., Wang, W., Huang, S., and                   Zhang, D., Zhoubian, S., Hu, Z., Yue, Y., Dong, Y., and
  Huang, F. RRHF: Rank responses to align language mod-                   Tang, J. Rest-mcts*: Llm self-training via process reward
  els with human feedback. In Thirty-seventh Conference                   guided tree search, 2024b. URL https://arxiv.org/
  on Neural Information Processing Systems, 2023a. URL                    abs/2406.03816.
  https://openreview.net/forum?id=EdIGMCHk4l.
                                                                        Zhang, L., Hosseini, A., Bansal, H., Kazemi, M., Ku-
Yuan, W., Pang, R. Y., Cho, K., Sukhbaatar, S., Xu, J.,                   mar, A., and Agarwal, R. Generative verifiers: Re-
  and Weston, J. Self-rewarding language models. ArXiv                    ward modeling as next-token prediction. arXiv preprint
  preprint, abs/2401.10020, 2024. URL https://arxiv.                      arXiv:2408.15240, 2024c.
  org/abs/2401.10020.
                                                                        Zhang, L., Hosseini, A., Bansal, H., Kazemi, M., Kumar, A.,
Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou,              and Agarwal, R. Generative verifiers: Reward modeling
  C., and Zhou, J. Scaling relationship on learning mathe-                as next-token prediction, 2024d. URL https://arxiv.
  matical reasoning with large language models, 2023b.                    org/abs/2408.15240.

Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou,            Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu,
  C., and Zhou, J. Scaling relationship on learning math-                 Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., et al.
  ematical reasoning with large language models, 2023c.                   Judging llm-as-a-judge with mt-bench and chatbot arena.
  URL https://arxiv.org/abs/2308.01825.                                   Advances in Neural Information Processing Systems,
                                                                          36:46595–46623, 2024a. URL https://proceedings.
Yue, X., Qu, X., Zhang, G., Fu, Y., Huang, W., Sun, H., Su,               neurips.cc/paper files/paper/2023/hash/
  Y., and Chen, W. Mammoth: Building math generalist                      91f18a1287b398d378ef22505bf41832-Abstract-Datasets
  models through hybrid instruction tuning. arXiv preprint                and Benchmarks.html.
  arXiv:2309.05653, 2023.
                                                           Zheng, R., Dou, S., Gao, S., Hua, Y., Shen, W., Wang, B.,
Zelikman, E., Wu, Y., Mu, J., and Goodman, N. Star:          Liu, Y., Jin, S., Liu, Q., Zhou, Y., Xiong, L., Chen, L.,
  Bootstrapping reasoning with reasoning. In Koyejo, S.,     Xi, Z., Xu, N., Lai, W., Zhu, M., Chang, C., Yin, Z.,
  Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and       Weng, R., Cheng, W., Huang, H., Sun, T., Yan, H., Gui,
  Oh, A. (eds.), Advances in Neural Information Processing   T., Zhang, Q., Qiu, X., and Huang, X. Secrets of rlhf in
  Systems, volume 35, pp. 15476–15488. Curran Asso-          large language models part i: Ppo, 2023.
  ciates, Inc., 2022a.      URL https://proceedings.
  neurips.cc/paper files/paper/2022/file/                  Zheng, T., Zhang, G., Shen, T., Liu, X., Lin, B. Y., Fu, J.,
  639a9a172c044fbb64175b5fad42e9a5-Paper-Conference. Chen, W., and Yue, X. Opencodeinterpreter: Integrating
  pdf.                                                       code generation with execution and refinement, 2024b.

Zelikman, E., Wu, Y., Mu, J., and Goodman, N. Star: Boot-
  strapping reasoning with reasoning. Advances in Neu-
  ral Information Processing Systems, 35:15476–15488,
  2022b.

Zelikman, E., Harik, G., Shao, Y., Jayasiri, V., Haber, N.,
  and Goodman, N. D. Quiet-star: Language models can
  teach themselves to think before speaking. ArXiv preprint,
  abs/2403.09629, 2024. URL https://arxiv.org/abs/
  2403.09629.

Zeng, W. and Church, R. L. Finding shortest paths on
  real road networks: the case for a*. Int. J. Geogr. Inf.
  Sci., 23(4):531–543, April 2009. ISSN 1365-8816. doi:
  10.1080/13658810801949850. URL https://doi.org/
  10.1080/13658810801949850.

Zhang, D., Wu, J., Lei, J., Che, T., Li, J., Xie, T., Huang, X.,
  Zhang, S., Pavone, M., Li, Y., Ouyang, W., and Zhou, D.
  Llama-berry: Pairwise optimization for o1-like olympiad-
  level mathematical reasoning, 2024a. URL https://
  arxiv.org/abs/2410.02884.

                                                                   20
