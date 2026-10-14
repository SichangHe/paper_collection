                                         Preprint




                                         AGENT 2W ORLD : L EARNING TO G ENERATE S YM -
                                         BOLIC W ORLD M ODELS VIA A DAPTIVE M ULTI -
                                         AGENT F EEDBACK
                                             Mengkang Hu♠♡∗ Bowei Xia♠♢ ∗ Yuran Wu♠ Ailing Yu♠ Yude Zou♠ Qiguang Chen♣
                                             Shijian Wang♡ Jiarui Jin♡ Kexin Li♢ Wenxiang Jiao♡ Yuan Lu♡ Ping Luo♠ †
                                             ♠
                                               The University of Hong Kong ♡ Xiaohongshu Inc.
                                             ♢
                                               UESTC ♣ Harbin Institute of Technology
arXiv:2512.22336v1 [cs.AI] 26 Dec 2025




                                                                                        A BSTRACT

                                                      Symbolic world models (e.g., PDDL domains or executable simulators) are cen-
                                                      tral to model-based planning, but training LLMs to generate such world models
                                                      is limited by the lack of large-scale verifiable supervision. Current approaches
                                                      rely primarily on static validation methods that fail to catch behavior-level errors
                                                      arising from interactive execution. In this paper, we propose AGENT 2W ORLD, a
                                                      tool-augmented multi-agent framework that achieves strong inference-time world-
                                                      model generation and also serves as a data engine for supervised fine-tuning, by
                                                      grounding generation in multi-agent feedback. AGENT 2W ORLD follows a three-
                                                      stage pipeline: (i) A Deep Researcher agent performs knowledge synthesis by
                                                      web searching to address specification gaps; (ii) A Model Developer agent im-
                                                      plements executable world models; And (iii) a specialized Testing Team conducts
                                                      adaptive unit testing and simulation-based validation. AGENT 2W ORLD demon-
                                                      strates superior inference-time performance across three benchmarks spanning
                                                      both Planning Domain Definition Language(PDDL) and executable code repre-
                                                      sentations, achieving consistent state-of-the-art results. Beyond inference, Testing
                                                      Team serves as an interactive environment for the Model Developer, providing
                                                      behavior-aware adaptive feedback that yields multi-turn training trajectories. The
                                                      model fine-tuned on these trajectories substantially improves world-model gen-
                                                      eration, yielding an average relative gain of 30.95% over the same model before
                                                      training. Project page: agent2world.github.io.


                                         1       I NTRODUCTION

                                         In recent years, researchers have explored symbolic world models, a formal representation of an en-
                                         vironment’s dynamics and constraints, which is widely used in model-based planning (Guan et al.,
                                         2023; LeCun, 2022; Craik, 1967). The task of symbolic world-model generation involves automat-
                                         ically synthesizing these models from natural language descriptions, eliminating the need for do-
                                         main experts to manually design and specify complex rules and dynamics. Large language models
                                         (LLMs) (Guo et al., 2025; Zhao et al., 2023; Bai et al., 2023) have made this automation possi-
                                         ble by combining two key capabilities: commonsense knowledge about how the world works, and
                                         code generation abilities that formalize this knowledge into executable representations (Chen et al.,
                                         2025a). However, learning to generate such models from natural language remains difficult: cor-
                                         rectness is behavioral and execution-dependent, while large-scale, verifiable supervision is scarce.
                                         As illustrated in Figure 1, prior work in this domain largely follows two paradigms: (i) direct gen-
                                         eration of symbolic world models, and (ii) scripted workflows that couple generation with iterative
                                         verification and repair. Across both PDDL-style domains (Guan et al., 2023; Hu et al., 2025a) and
                                         executable code world models (Dainese et al., 2024), the second paradigm typically couples gener-
                                         ation with a pre-specified verification interface (e.g., parsers/planners/validators, fixed sets of evalu-
                                         ation trajectories). While such static validation improves syntactic validity, it misses behavior-level
                                         errors that only appear under interactive execution (e.g., inconsistent state updates or unreachable
                                             ∗
                                                 Equal contribution. Corresponding to mkhu@connect.hku.hk, pluo.lhi@gmail.com.


                                                                                               1
Preprint




         Direct                        Workflow                                         Agent (ours)
                                                                                                                                              39




                                                                                                                               Text2World
              LLM                 LLM                  World Model           Searcher                              Developer
                                                                                                                                                    60
    World Model                         Excution                             Required                     World Model
                                                                             Action
                                                                                                                                                         75
                              ❌                ❌                     √ Power
                        ❌
                                                                     √ Bread
                                                                     √ Temperature
                                                                                                                                             26




                                                                                                                               CWMB
                        × Power
                        × Bread
                                        × Bread
                                                                     Simulation Tester                    Unit Tester                         35
                                                                                                             Require
                                                                                                                                                   48
                        + power_on()    + bread_in()
                                                                                                              power
         Results
                                   Fix / Improve                      Plug           Insert
                                                                                                              Require




                                                                                                                               Bytesized32
                                                                                                               bread                                    70
                                          Results                    Success         Press
              ❌
                                                                                        ✅                    Required                                    73
                                        ✅
     ❌                                            √ Power   pass                                            Temperature
                                                  √ Bread
                                                                                                                                                          79
    × Power   × Bread                                                                         √ Power    √ Bread
                                             × Temperature unknown   Results                                          pass
     Do not Pass                                                                                 √ Temperature
                                                                                                                                                  Score


    Figure 1: Comparison of AGENT 2W ORLD and previous world-model generation paradigms.

goals). Furthermore, existing studies on generating symbolic world models with LLMs have pri-
marily focused on training-free methods for one particular type of world models (Yu et al., 2025;
Kong et al., 2025; Zhang et al., 2025), rather than fundamentally enhancing the world modeling
capabilities of the LLMs themselves.
In this paper, we propose AGENT 2W ORLD, a tool-augmented multi-agent framework that evaluates
and improves world models through interactive execution. Given a natural-language description,
AGENT 2W ORLD coordinates multiple LLM-based agents with access to external tools (e.g., web
retrieval and code execution) to iteratively produce an executable world model. At a high level,
AGENT 2W ORLD consists of three stages (Figure 2): a Deep Researcher resolves underspecified de-
tails by gathering missing background knowledge, a Model Developer implements the world model
in the target representation, and a Testing Team evaluates the resulting artifact under adaptive ex-
ecution (unit tests and simulation-style evaluation) and returns structured feedback for repair. Un-
like prior pipelines that rely on static validators or fixed test suites, AGENT 2W ORLD conditions
evaluation on observed execution behavior and iteratively produces targeted checks, which expose
behavior-level failures that predetermined checks often miss.
Most importantly, the same developer-tester interaction loop can be viewed as an interactive en-
vironment for the Model Developer, naturally producing multi-turn trajectories that capture how
world models are revised under feedback and providing verifiable reward. We use this property
to turn inference-time feedback into training data for improving the Model Developer policy via
verifier-guided rejection sampling (Section 3.2) and construct a dataset consisting of 1526 high-
quality verified trajectories covering four distinct types of world models across diverse domains.
We conducted experiments on three benchmark datasets to evaluate the performance of
AGENT 2W ORLD: (i) Text2World (Hu et al., 2025a) for PDDL-based domain generation, (ii) Code-
based World Models Benchmark (CWMB) (Dainese et al., 2024) for MuJoCo-style environment
generation, and (iii) ByteSized32 (Wang et al., 2023) for reasoning-heavy text game generation.
First, we validated the inference-time performance of AGENT 2W ORLD with two different mod-
els: GPT-4.1-mini (Achiam et al., 2023) and Llama-3.1-8b (Grattafiori et al., 2024). Our results
demonstrate that AGENT 2W ORLD consistently achieves state-of-the-art performance across all three
benchmarks with both models. This highlights its robust capabilities in symbolic world model gen-
eration, regardless of the underlying model. Furthermore, we also validated the effectiveness of
AGENT 2W ORLD through training experiments. We performed supervised fine-tuning on the same
Llama-3.1-8b model. Our results show consistent improvements across all benchmarks, indicat-
ing that the model is able to refine its world-model generation process effectively through iterative
multi-agent feedback.


2    P ROBLEM D EFINITION

We investigate the problem of symbolic world-model generation from natural language. Given a
textual description x, the objective is to synthesize an executable program WM that faithfully cap-


                                                                             2
Preprint




                           Figure 2: Overall Pipeline of AGENT 2W ORLD.


tures the dynamics and constraints of the environment. Such a program may take various forms,
for instance, a specification in the Planning Domain Definition Language (PDDL) (Hu et al., 2025a;
McDermott et al., 1998) or an implementation in Python (Dainese et al., 2024; Wang et al., 2023).
Formally, an environment is defined by a set of predicates Penv , a set of actions Aenv , and a transition
function Tenv : Senv × Aenv → Senv , where Senv denotes the set of possible states. Semantically,
WM encodes these components to represent the environment in an executable manner. We there-
fore define the task as a mapping F (x) = WM where WM = ⟨Penv , Aenv , Tenv ⟩, and F is a
synthesis procedure that generates the world-model program from natural language input x.


3     M ETHODOLOGY

3.1     A RCHITECTURAL D ESIGN

As is shown in Figure 2, AGENT 2W ORLDMulti unfolds in three stages: (i) Knowledge Synthesis
(§3.1.1): As outlined in Section 1, a key challenge in symbolic world-model construction arises from
incomplete descriptions. For example, commonsense knowledge may be missing both from LLMs
and from the given specifications. To address this limitation, we employ a deep researcher agent that
interacts with external resources such as the internet or structured databases, thereby enriching the
specification and producing an intermediate representation. (ii) World Model Generation (§3.1.2):
At this stage, a developer agent equipped with a code execution tool constructs the symbolic world
model. The process is iteratively refined based on execution feedback, ensuring both correctness
and executability. (iii) Evaluation-Driven Refinement (§3.1.3): We enhance the semantic fidelity
by designing two complementary test agents: one that generates unit tests to validate functional
behavior, and another that simulates downstream usage to evaluate performance through trajectory-
based testing. We also provide a pseudo code in Algorithm 1.

3.1.1      S TAGE I: K NOWLEDGE S YNTHESIS

We introduce a Deep Researcher agent designed to gather background knowledge and fill in miss-
ing details that are not explicitly provided in the world model description. By leveraging external
information sources, this agent not only compensates for potential knowledge gaps inherent in large
language models but also enhances the factual reliability of world model descriptions. Equipped
with web search and retrieval tools, it iteratively retrieves the knowledge required for world model
construction from the internet and ultimately outputs a structured intermediate representation with
the missing information completed.


                                                    3
Preprint




3.1.2      S TAGE II: W ORLD M ODEL G ENERATION

After obtaining the comprehensive world-model description from the previous stage, the Model
Developer takes this as input and generates a concrete implementation of the world model in the
required formalism (e.g., PDDL or executable code). To support iterative refinement, the Model
Developer is equipped with a sandboxed code-execution tool, enabling it to test and debug imple-
mentations in multiple rounds until the code is functional and consistent with the specification.


3.1.3      S TAGE III: E VALUATION -D RIVEN R EFINEMENT

A key component of our approach is the refinement of a bug-free, code-based world model. Unlike
prior works that rely on annotated gold trajectories (Dainese et al., 2024) or human feedback (Guan
et al., 2023), our method is fully autonomous and does not require manual labels. More specifically,
we introduce a two-agent Testing Team to evaluate and diagnose the generated models: (i) The Unit
Tester conducts systematic, programmatic verification to validate the basic functionality of gener-
ated world model. It automatically generates Pytest-style unit tests targeting the predicates, actions,
and invariants specified in the world-model descriptions. (ii) The Simulation Tester evaluates the
world model in a play-testing manner by attempting to perform tasks, explore actions, and issue
queries within the environment. Specifically, it interacts with the environment in a ReAct-style (Yao
et al., 2023) loop to collect trajectories for subsequent behavior and reward analysis, which uncovers
execution-time failures such as unreachable goals, missing preconditions, or inconsistent state up-
dates. Together, these agents produce a detailed test report that assesses the quality of the generated
world model and provides fine-grained diagnostic signals on correctness, coverage, logical consis-
tency, and compliance with physical requirements. Unlike prior methods such as Text2World (Hu
et al., 2025a), which uses PDDL validators, or GIF-MCTS (Dainese et al., 2024), which relies on a
fixed set of offline agent trajectories, our Testing Team dynamically synthesizes test cases based on
the specific errors exhibited by each world model, enabling precision-guided debugging rather than
generic checks. This adaptive feedback is propagated back to the Model Developer; if inconsisten-
cies or failures are detected, the Model Developer revises the implementation, triggering another
evaluation round. This loop continues until all checks are satisfied or a predefined convergence
criterion is reached.


3.2     T RAINING PARADIGM

So far, AGENT 2W ORLDMulti has been described as an inference-time multi-agent workflow in which
a frozen backbone LLM plays all the agent roles. However, the interaction between the Model
Developer and the Testing Team naturally defines a learning environment that can be used to train
more effective world-model agents.


3.2.1      AGENT- IN - THE -L OOP F ORMALIZATION

We view each role in AGENT 2W ORLDMulti as a tool-augmented LLM agent that interleaves gen-
eration with tool use. Let T = {t1 , . . . , tm } be the available tools (e.g., code execution, testing,
retrieval). At step t, the agent maintains a history ht = (x, o≤t , a<t ), where x is the task specifica-
tion, o are tool observations (e.g., execution logs and test reports), and a are past tool calls or edits.
A policy πθ (implemented by an LLM) selects the next action: at ∼ πθ (· | ht ), at ∈ T .
To connect this view to training, we model the Model Developer as an agent acting in an induced
Markov Decision Process (MDP): MMD = (S, A, P, R, γ). Here, the state st ∈ S concatenates the
world-model specification with diagnostics produced by the Testing Team; the action at ∈ A is a
new implementation or a patch to the current world model. The transition P is realized by executing
the candidate model in a sandbox and re-running the Testing Team to obtain updated diagnostics.
The reward R(st , at ) aggregates testing outcomes (e.g., unit-test pass rates and simulation perfor-
mance), capturing both local correctness and downstream utility. This formalization lets us treat
world-model synthesis as sequential decision making and naturally yields multi-turn interaction tra-
jectories for training.


                                                    4
Preprint




3.2.2      V ERIFIER -G UIDED R EJECTION S AMPLING
The agent-in-the-loop view naturally yields multi-turn interaction trajectories between the Model
Developer and the Testing Team. We leverage this interaction as a data engine to construct training
trajectories without manual labels via verifier-guided rejection sampling. Given a world-model
specification x, we run AGENT 2W ORLDMulti to produce a sequence of developer proposals and
                                   −1
feedback, τ = {(st , at , ot+1 )}Tt=0 , where ot+1 contains execution logs and testing diagnostics.
We define a verifier outcome V (τ ) ∈ {0, 1} based on the final candidate model produced in τ .
Concretely, V (τ ) = 1 if the final world model (i) executes successfully in the sandbox and (ii)
satisfies the Testing Team’s evaluation, i.e., it passes the synthesized unit tests and meets simulation-
based checks (when applicable); otherwise V (τ ) = 0. Rejection sampling keeps only accepted
trajectories: DRS = {(x, τ ) | V (τ ) = 1}. Intuitively, the Testing Team acts as a verifier that
filters for executable and behaviorally consistent solutions, while preserving the intermediate repair
steps. As a result, DRS contains multi-turn training traces that teach a Model Developer policy to
iteratively revise world models under execution-grounded feedback, rather than producing a single-
shot solution.


4     E XPERIMENTS

In this section, we first describe the training dataset (§ 4.1), baselines (§ 4.2), and implementa-
tion details (§ 4.3), and then present experiments on three benchmarks: (i) Text2World (Hu et al.,
2025a) (§ 4.4): A PDDL-centric benchmark for text-to-symbolic world modelling. (ii) Code World
Models Benchmark (CWMB) (Dainese et al., 2024) (§ 4.5): A code-based world-model benchmark
comprising MuJoCo-style environments, designed to assess predictive correctness and downstream
control utility under both discrete and continuous action settings. (iii) ByteSized32 (Wang et al.,
2023) (§ 4.6): A suite of reasoning-heavy text games requiring executable Python environments. A
side-by-side comparison and a detailed metric explanation are shown in Appendix C.

4.1     DATASET C ONSTRUCTION

Our data construction follows a staged pipeline in which we (i) synthesize diverse world-model
specifications spanning multiple representations (PDDL, Mujoco-style environments, text games,
MCP-style tool environments). (ii) run AGENT 2W ORLD with gpt-4.1-mini to generate executable
world models and record the full multi-agent interaction traces (including iterative repairs under ex-
ecution feedback); iii apply verification mechanisms, such as legality, executability, and compliance
checks, while combining semantic quality assessments regarding completeness, rationality, behav-
ioral diversity, and execution consistency. Only retain the trajectories that meet these criteria.More
detail show in Appendix E. To reduce the risk of training–evaluation leakage, we avoid using any
benchmark instances as prompts or templates for rewriting/augmentation. Instead, we follow the
environment synthesis method in AgentGen (Hu et al., 2025b) and using LIMA (Zhou et al., 2023)
dataset as the inspiration corpus.

4.2     BASELINES

We compare AGENT 2W ORLDMulti against the following methods:
(i) Direct Generation (Direct): Single-shot generation of the symbolic world model without tool
use, external retrieval, or feedback. (ii) Agent2Worldsingle : A single agent closes the loop by in-
voking code execution/validators/web search tools for self-repair and information synthesis, with-
out multi-agent specialization. (iii) Text2World (EC=k) (Hu et al., 2025a): directly using large
language models to generate PDDL-based world model and iteratively repairing with planner/-
validator signals, where EC denotes the error-correction budget. (iv) WorldCoder (Tang et al.,
2024): A plan–code–execute–repair search that scores and iteratively improves candidate programs
using simulator/planner signals to select runnable hypotheses. (v) GIF-MCTS (Dainese et al.,
2024): A macro-action MCTS that orchestrates Generate/Improve/Fix steps, guided by unit tests
and trajectory-based feedback for code world-model synthesis. We also introduced an enhanced
version of GIF-MCTS where a Deep Researcher agent gathers additional research data. (vi) Byte-
Sized32 baseline (Wang et al., 2023). The reference pipeline introduced by Wang et al. (2023). In


                                                   5
Preprint




Table 1: Benchmark results on Text2World (Hu et al., 2025a). Following the reporting convention
in Text2World, all metrics are presented as percentage scores (%).

                                                                              Component-wise F1 (↑)
 Methods                    Executability (↑)   Similarity (↑)                                                      F1AVG (↑)
                                                                 F1 PRED       F1 PARAM    F1 PRECOND   F1 EFF
 gpt-4.1-mini
 Text2WorldEC=3             78.2                81.1             73.4          64.5        49.3         53.3        60.1
 Direct Generation          45.5                82.8             45.0          40.3        33.9         34.9        38.5
 GIF-MCTS                   44.6                81.1             42.8          39.4        33.4         32.2        36.9
 Best-of-N                  54.5                84.0             54.1          53.5        44.9         47.0        49.9
 Self-Consistency           50.5                84.2             50.4          48.5        41.2         43.0        45.8
 AGENT 2W ORLDSingle        79.2                82.5             76.5          75.8        60.1         66.0        69.6
 AGENT 2W ORLDMulti         93.1                81.0             87.2          82.3        63.7         68.2        75.4
 llama-3.1-8b-instruct
 Text2WorldEC=3             0.0                 74.9             0.0           0.0         0.0          0.0         0.0
 Direct Generation          5.0                 79.0             4.0           3.9         2.2          1.9         3.0
 GIF-MCTS                   4.0                 72.9             0.0           0.0         0.0          0.0         0.0
 Best-of-N                  4.0                 79.1             3.9           3.7         1.7          2.0         2.8
 Self-Consistency           2.0                 79.1             1.0           0.2         0.0          0.0         0.3
 AGENT 2W ORLDSingle        19.8                81.9             19.5          18.7        13.8         12.8        16.2
 AGENT 2W ORLDMulti         27.7                81.0             27.5          25.5        16.4         17.8        21.8
 AGENT 2W ORLDMulti (SFT)   44.6 +16.9          81.9 +0.9        41.4 +13.9    32.6 +7.1   17.4 +1.0    21.5 +3.7   28.2 +6.4



order to avoid metric leakage, we do not use the official checker’s evaluation signals. (vii) Best-of-
N (Stiennon et al., 2020; Yu et al., 2025): A method that performs reasoning over multiple samples
and selects the best result. (viii) Self-Consistency (Wang et al., 2022): A multi-sample reasoning
method that votes over the results to improve consistency in decision-making.

4.3   I MPLEMENTATION D ETAILS

We employ the OpenAI GPT-4.1-mini model via the official API and Llama-3.1-8b-instruct via the
official Huggingface repo. We set the decoding temperature to 0 and top_p to 1 for deterministic
reproducibility. All agents operate within a ReAct (Yao et al., 2023) framework, following a "think
→ act (tool) → observe" loop for a maximum of 10 steps. The Deep Researcher agent utilizes
the Serper API for web searching. We blocked some websites to ensure experimental integrity and
prevent information leakage 1 Regarding the configuration of refinement turns, we set Text2World
and ByteSized32 to 2 iterations and CWMB to 3 iterations based on the complexity of environments.
For automated evaluation on the ByteSized32 benchmark, we leverage GPT-4o (Hurst et al., 2024)
as the LLM evaluator. All experiments with gpt-4.1-mini are conducted on a CPU server without
GPU acceleration. The experiments with llama-3.1-8b-instruct (including training and inference)
are conducted with an 8xA100 server. The prompt examples could be found at Appendix G. As for
the training experiments, we leverage the LlamaFactory (Zheng et al., 2024) to manage and execute
the training procedure. We perform supervised fine-tuning (SFT) on the llama-3.1-8b models, and
truncate input sequences to a maximum length of 30,000 tokens. We train the model for 5 epochs
with learning rate of 1 × 10−6 .

4.4   T EXT 2W ORLD

We evaluate the Planning Domain Definition Language (PDDL)-based world model generation of
AGENT 2W ORLD on Text2World Hu et al. (2025a), which comprises 103 PDDL domains paired
with natural language descriptions. The evaluation metrics are: (i) Executability: whether the gen-
erated PDDL can be parsed and validated; (ii) Structural Similarity: the normalized Levenshtein
similarity; (iii) Component-wise F1: the macro-averaged F1 of predicates (F1 PRED ) and action com-
ponents, including parameters (F1 PARAM ), preconditions (F1 PRECOND ), and effects (F1 EFF ).

Results. We can draw several conclusions from Table 1: (i) Direct Generation attains the highest
Similarity (82.8) yet performs poorly on executability (45.5) and all component-wise F1s, under-
scoring that surface-level textual overlap is a weak proxy for runnable, semantically correct PDDL.
  1
    For example, the original Text2World and ByteSized32 huggingface pages, CWMB source code, OpenAI-
Gym code repository are blocked.


                                                            6
Preprint




Table 2: Benchmark results on CWMB. † We adopted the official implementation of GIF-
MCTS (Dainese et al., 2024) and their reimplementation of WorldCoder (Tang et al., 2024).
GIF-MCTS⋆ denotes the enhanced version that we obtain by connecting the deep research agent
with the original GIF-MCTS pipeline.

                                   Discrete Action Space            Continuous Action Space                      Overall
   Method
                              Accuracy (↑)     R (↑)            Accuracy (↑)     R (↑)            Accuracy (↑)       R (↑)
   gpt-4.1-mini
   WorldCoder†                0.9024           0.5399           0.3303           0.2097           0.5210             0.3197
   GIF-MCTS†                  0.9136           0.6842           0.2748           0.1811           0.4877             0.3488
   GIF-MCTS⋆                  0.8876           0.7955           0.3030           0.1495           0.4979             0.3649
   Direct Generation          0.7321           0.4527           0.3038           0.1666           0.4466             0.2620
   Best-of-N                  0.7488           0.6012           0.2642           0.1970           0.4257             0.3317
   Self-Consistency           0.7870           0.4912           0.2479           0.2158           0.4276             0.3076
   AGENT 2W ORLDSingle        0.7897           0.5418           0.1917           0.2420           0.3911             0.3419
   AGENT 2W ORLDMulti         0.9174           0.8333           0.3575           0.3050           0.5441             0.4811
   llama-3.1-8b-instruct
   WorldCoder†                0.5192           0.2779           0.1173           0.1073           0.2513             0.1642
   GIF-MCTS†                  0.5983           0.3357           0.1332           0.1427           0.2883             0.2070
   GIF-MCTS⋆                  0.4691           0.3752           0.1934           0.1457           0.2853             0.2222
   Best-of-N                  0.2236           0.0004           0.1544           0.1404           0.1775             0.0937
   Self-Consistency           0.4626           0.1667           0.0000           0.0036           0.1542             0.0580
   AGENT 2W ORLDSingle        0.1531           0.0000           0.2690           0.1418           0.2304             0.0945
   AGENT 2W ORLDMulti         0.5797           0.2998           0.1826           0.1945           0.3150             0.2296
   AGENT 2W ORLDMulti (SFT)   0.6857 +0.1060   0.5333 +0.2335   0.2203 +0.0377   0.2128 +0.0183   0.3754 +0.0604     0.3197 +0.0901




(ii) While agent-based methods achieve executability comparable to the reference solution (e.g.,
AGENT 2W ORLDSingle with 79.2 vs. Text2WorldEC=3 with 78.2), they exhibit substantial gaps in F1
scores (AGENT 2W ORLDSingle : 69.6 vs. Text2WorldEC=3 : 60.1). This suggests that while integrating
validators for iterative correction can significantly improve syntactic validity, the semantic utility
of the generated world models remains limited without comprehensive knowledge synthesis. (iii)
AGENT 2W ORLDMulti achieves both the highest executability (+14.9 points over Text2WorldEC=3 )
and superior F1 performance (+15.3 points), demonstrating the synergistic benefits of multi-agent
specialization. These patterns align with our design philosophy: knowledge synthesis combined
with evaluation-driven refinement steers the model to recover the correct predicate inventory and
logical gating constraints, producing domains that are both syntactically valid and semantically
solvable, even when surface-level representations diverge from reference implementations. (iv)
Based on the Llama3.1-8b-instruct model, AGENT 2W ORLDMulti (SFT) significantly improved exe-
cutability (+16.9 points over AGENT 2W ORLDMulti ) and optimized F1 performance (+6.4 points over
AGENT 2W ORLDMulti ). This demonstrates that our SFT data effectively reduced the model’s errors
in PDDL code and enhanced its understanding of task descriptions, improving the semantic struc-
ture of the generated code. In terms of structural similarity, the model scored 81.9, nearly equivalent
to the Llama 4.1-mini model (81.0), indicating that the generated PDDL is structurally close to the
reference standard.

4.5    C ODE W ORLD M ODELS B ENCHMARK (CWMB)

The CWMB (Dainese et al., 2024) evaluates the ability of generated executable code to serve as
faithful world models across 18 MuJoCo-style environments. It measures both the predictive accu-
racy of next-state dynamics and the normalized return (R) when the model is used by a planner,
where R reflects the gap between a random policy and an oracle planner with the true environment.
This setup ensures CWMB jointly assesses the correctness of the simulation code and its practical
utility for downstream control.

Results. Table 2 reveals several key findings. (i) All methods demonstrate superior performance in
discrete spaces compared to continuous settings, reflecting the inherent difficulty of modeling con-
tinuous dynamics. (ii) Workflow-based approaches consistently outperform both Direct Generation
and AGENT 2W ORLDSingle , indicating that LLMs’ native world model generation capabilities are
limited and require expert-designed iterative refinement to achieve competitive performance. (iii)
AGENT 2W ORLDMulti establishes new state-of-the-art results, surpassing the previous best method
GIF-MCTS by +0.132 R points in overall normalized return. Notably, while other methods achieve
comparable predictive accuracy (e.g., 0.917 vs 0.914 on discrete settings), our simulation-based


                                                                7
Preprint




Table 3: Technical Validity and Physical Reality Alignment (Physical Align.) scores on Byte-
Sized32.

   Method                                         Technical Validity (↑)                    Physical Align. (↑)
                                 Game Init.         Possible Actions      Runnable Game     Alignment Score
   gpt-4.1-mini
   ByteSized320-shot             0.9792             0.9375                0.7292            0.0600
   ByteSized321-shot             0.9792             0.8958                0.7500            0.1748
   GIF-MCTS                      0.8021             0.7083                0.4375            0.0656
   Direct Generation             0.9271             0.8854                0.7604            0.0738
   Best-of-N                     0.9583             0.8750                0.7604            0.2347
   Self-Consistency              0.9688             0.8021                0.6875            0.3562
   AGENT 2W ORLDSingle           0.9792             0.9375                0.7708            0.1920
   AGENT 2W ORLDMulti            0.9896             0.9583                0.8958            0.4768
   llama-3.1-8b-instruct
   ByteSized320-shot             0.5417             0.3958                0.3125            0.0023
   ByteSized321-shot             0.6458             0.5833                0.2540            0.0287
   Direct Generation             0.4286             0.3333                0.1458            0.0168
   GIF-MCTS                      0.4167             0.3021                0.125             0.0237
   Best-of-N                     0.4479             0.3854                0.1042            0.0660
   Self-Consistency              0.5729             0.4792                0.1354            0.0424
   AGENT 2W ORLDSingle           0.5474             0.4842                0.1579            0.0281
   AGENT 2W ORLDMulti            0.7850             0.6355                0.1963            0.0837
   AGENT 2W ORLDMulti (SFT)      0.8229 +0.0379     0.6458 +0.0103        0.2812 +0.0849    0.1040 +0.0203



testing framework significantly enhances the downstream utility of generated world models, demon-
strating that accurate next-state prediction alone is insufficient for effective model-based planning.
(iv) AGENT 2W ORLDMulti (SFT) further improves ByteSized32 by enhancing executability and spec-
ification compliance. It significantly improves the "runnable game" score (0.0849 points higher than
multi) and greatly improves the compliance of "key actions" and "distractors" (0.2944 points higher
than multi), thereby increasing the "winnable game" rate (0.0388 points higher than multi). The
training data improves the model’s understanding of task and execution-based iterative debugging,
thereby reducing missing necessary components and generating more runnable implementations.


4.6   B YTE S IZED 32


            Table 4: Specification Compliance and Winnability scores on ByteSized32.

      Method                                  Specification Compliance (↑)                  Winnability (↑)
                                   Critical Objects    Critical Actions    Distractors      Winnable Game
      gpt-4.1-mini
      ByteSized320-shot            0.9375              0.9375              0.8750           0.0625
      ByteSized321-shot            1.0000              0.9375              0.9375           0.1354
      GIF-MCTS                     0.9062              0.9375              0.9375           0.0729
      Direct Generation            1.0000              0.9375              0.9375           0.1354
      Best-of-N                    1.0000              0.9375              0.9062           0.1354
      Self-Consistency             1.0000              0.9375              0.8125           0.1267
      AGENT 2W ORLDSingle          1.0000              1.0000              0.8438           0.1354
      AGENT 2W ORLDMulti           1.0000              0.9688              0.8750           0.1458
      llama-3.1-8b-instruct
      ByteSized320-shot            1.0000              0.8125              0.0938           0.0000
      ByteSized321-shot            0.9688              0.8125              0.0938           0.0433
      Direct Generation            0.9375              0.7812              0.0312           0.0000
      GIF-MCTS                     1.0000              0.7812              0.1875           0.0312
      Best-of-N                    0.9688              0.8438              0.0625           0.0417
      Self-Consistency             0.9688              0.6250              0.0312           0.0433
      AGENT 2W ORLDSingle          0.9688              0.6875              0.0323           0.0433
      AGENT 2W ORLDMulti           0.9688              0.6744              0.0938           0.0654
      AGENT 2W ORLDMulti (SFT)     0.9688 +0.0000      0.9688 +0.2944      0.1875 +0.0937   0.1042 +0.0388



                                                        8
Preprint




                                                                                                Win        Tie       Loss


                                                 Text2World   14%             80%                     7%         46.5%         28.7%     24.8%



                                                   CWMB               68.8%                31.2%                    66.7%           16.7% 16.7%



                                                 Bytesize32                   93%                     7%                 87%                   13%


                                                                    Final Turn vs. First Turn                Agent2Worldmulti vs. Prev. SOTA



      Figure 3: Ablation Study on CWMB.               Figure 4: Pair-wise Win–Tie–Loss analysis.


The ByteSized32 (Wang et al., 2023) benchmark consists of 32 reasoning-heavy text games, each
implemented as an executable Python environment. Models are required to generate runnable game
code that captures task-specific dynamics, objects, and rules, allowing direct interaction and eval-
uation. The benchmark evaluates four dimensions: Technical Validity (whether the code runs),
Specification Compliance (whether all required elements are present), Winnability (whether the
task can be completed), and Physical Reality Alignment (whether the environment dynamics are
consistent with commonsense constraints). This setting emphasizes both logical fidelity and practi-
cal executability, making it a stringent testbed for language models as world-model generators.

Results. Several conclusions could be drawn from Table 3 and 4: (i) The official reference
pipeline outperforms direct generation with in-context learning and shows comparable performance
to AGENT 2W ORLDSingle on certain metrics. (ii) The AGENT 2W ORLDSingle baseline shows mod-
erate gains in game solvability, yet its alignment with physical reality is slightly weaker. (iii)
AGENT 2W ORLDMulti outperforms both baselines across almost all dimensions, especially +0.2848
physical alignment score, which stems from Deep Researcher agent synthesizing the commonsense
knowledge required for reasoning-heavy games. (iv)

5     A NALYSIS
5.1    A BLATION S TUDY

Ablations from Figure 3 and Table 7 clarify where the lift comes from: (i) Removing the Unit Tester
causes the most significant performance drop, with accuracy declining by 0.3008 and reward R by
0.4470 in discrete action spaces. (ii) The Deep Researcher primarily impacts reward R quality,
showing a substantial decrease of 0.3926 for discrete spaces when removed. (iii) Although the re-
moval of Simulation Tester results in the smallest overall performance drops, the reward R decreases
by 0.2615 and 0.1473 for discrete space and continuous space, respectively. These results collec-
tively validate our design choices and highlight the complementary nature of the three components.

5.2    PAIR - WISE E VALUATION

To quantify the effect of AGENT 2W ORLDMulti and the refinement procedure, we perform instance-
level pairwise comparisons, recording a Win–Tie–Loss (WTL) outcome according to the bench-
marks’ primary metric: (i) F1AVG for Text2World; (ii) R for CWMB; and (iii) the mean of all official
metrics for ByteSized32. As shown in Figure 4, the left panel contrasts the final-turn model with its
first-turn counterpart. Refinement yields consistent gains on CWMB and ByteSized32 (68.8% and
93% wins, respectively; no losses), largely preserves performance on Text2World while delivering
occasional improvements (14% wins vs. 7% losses). The right panel compares AGENT 2W ORLDMulti
against previous state-of-the-art systems. AGENT 2W ORLDMulti attains clear advantages across all
three benchmarks, most notably on ByteSized32 (87% wins) and CWMB (66.7% wins).

5.3    F EEDBACK I TERATION

To understand the dynamics of performance improvement through iterative feedback, we analyze
how model performance evolves as the number of testing team feedback iterations increases. Fig-
ure 5 illustrates the relationship between feedback iteration count and model performance across the


                                                  9
Preprint




                     Executability          Domain Text Similarity      Predicate F1                                                                         Critical distractor      Critical object      Critical action    Winnable
                                                                                                                            ACC         R                                                             Runnable      Alignment Score
                     Action F1 Effect         Action F1 Params       Action F1 Preconds                                                                      Game Init        Possible Actions


                     100                                                                                 60                                                                      100
 Average Score (%)




                                                                                     Average Score (%)




                                                                                                                                                             Average Score (%)
                       90                                                                                                                                                        80
                                                                                                         50
                       80                                                                                                                                                        60
                                                                                                         40
                       70                                                                                                                                                        40
                                                                                                         30
                       60                                                                                                                                                        20

                       50                                                                                20                                                                       0
                                        0              1               2                                      0         1           2          3                                              0              1    2

                                              Text2World                                                                CWMB                                                                        Bytesized32


Figure 5: Primary performance evolution across successive rounds of testing team feedback
(§ 3.1.3.)


                                                                           Success
                                                                                                              Success

                                                                                                                                            Success
                                                                           signature-mismatch
                                                                                                                                                                                       Success

                                                                                                              dynamics-error
                                            Input                                                                                                                                                     Output
                                                                           schema-mismatch
                                                                                                                                            dynamics-error
                                                                           dynamics-error                     signature-mismatch                                                       dynamics-error

                                                                           non-deterministic                  schema-mismatch               signature-mismatch                         invariant-violation
                                                                                                              invariant-violation                                                      signature-mismatch
                                                                           judgment-bug                       judgment-bug                  judgment-bug                               judgment-bug




Figure 6: Error distribution on CWMB of evaluation-driven refinement. Due to page limit, the error
distribution of other benchmarks is presented in Appendix F.


evaluation benchmarks. The results reveal several key patterns: (i) Text2World shows rapid initial
improvements. Notably, execution-based metrics improve substantially while similarity measures
remain stable, suggesting that refinement enhances functional correctness rather than surface-level
similarities. (ii) CWMB demonstrates sustained improvement across iterations, reflecting the com-
pound complexity of physics simulation where numerical accuracy and dynamics must be jointly
optimized. (iii) ByteSized32 exhibits the most dramatic gains, with several metrics showing step-
function improvements that reflect the discrete nature of game logic debugging.

5.4                         M ANUAL E RROR A NALYSIS

We conducted a manual error analysis to examine the evolution of error patterns throughout the
refinement process of AGENT 2W ORLDMulti . Taken CWMB in Figure 6 as an example, the initial
turn predominantly exhibits superficial errors like signature-arity mismatches and representation
mismatches, stemming from inadequate adherence to world model specifications. Throughout the
iterative refinement process, these surface-level inconsistencies are systematically eliminated, with
the error landscape shifting toward more fundamental dynamics mismatches in later iterations. This
pattern demonstrates remarkable consistency across all benchmarks: refinement consistently shifts
the error distribution from form-oriented problems (syntax, arity) to substance-oriented challenges
(dynamics, state transitions) as shown in Figure 7 and 8. The systematic progression from surface
to substance reflects the hierarchical nature of world model correctness and validates our multi-turn
refinement architecture. We also provide the detailed proportion of each error type in Appendix F.

5.5                         M ULTI -AGENT VS . S INGLE -AGENT A RCHITECTURE A NALYSIS

To quantify the cost of multi-agent specialization, we analyze the token consumption reported in
Appendix K. Compared to AGENT 2W ORLDSingle , AGENT 2W ORLDMulti incurs a higher computa-
tional cost during the generation phase. This increase stems from the proactive testing loop, where


                                                                                                                             10
Preprint




agents autonomously generate unit tests and simulation trajectories to diagnose errors. However,
this additional cost represents a finite upfront investment rather than a recurring inefficiency, which
is incurred only once during the synthesis of the world model. In exchange, the framework secures
a permanent performance gain in the quality of the generated artifact (e.g., raising the Normalized
Return R from 0.3419 to 0.4811 on CWMB).


6   R ELATED W ORK

World Models. World models are widely applied in reinforcement learning, robotics, and au-
tonomous systems for planning, etc (Hao et al., 2023; Ha & Schmidhuber, 2018). Generally, there
are two types of world models: (i) neural world models, which employ neural networks to approx-
imate dynamics (Ha & Schmidhuber, 2018; Hafner et al., 2019), and (ii) symbolic world models,
which are represented using formal languages such as the Planning Domain Definition Language
(PDDL) or code-based implementations. In this paper, we investigate symbolic world-model gen-
eration, which involves transforming world model descriptions into formal representations that can
subsequently be utilized for applications such as model-based planning (Guan et al., 2023; Dainese
et al., 2024), dataset construction (Hu et al., 2025b), and so on. Most prior work follows a draft-
repair workflow where the model first proposes an initial implementation, then gradually refines
under closed-loop diagnosis from some kind of feedback. The feedback mechanisms can vary sig-
nificantly across different approaches. For instance, Guan et al. (2023) employs human feedback
to provide corrective signals and perform iterative modifications. Other works, such as Hu et al.
(2025a) and Tang et al. (2024), utilize executors and validators to generate feedback. GIF-MCTS
(Dainese et al., 2024) leverages gold experiences as feedback signals. Compared to these scripted
workflows, the AGENT 2W ORLD paradigm introduced in this paper can more flexibly adjust subse-
quent strategies based on feedback signals.
Large Language Model-based Agent. In recent years, benefiting from the rapid advancement of
large language models (LLMs), LLM-based agents have emerged as particularly powerful systems
that accept natural language user intentions as input and achieve goal states through planning and se-
quential decision-making (Hu et al., 2024; Yao et al., 2023; Schick et al., 2023). These autonomous
agents have demonstrated remarkable effectiveness across diverse applications, ranging from web
navigation (Yao et al., 2022; Nakano et al., 2021; Wang et al., 2025) and software development (Qian
et al., 2023; Hong et al., 2024) to scientific research (Lu et al., 2024; Chen et al., 2025b) and robotic
planning (Huang et al., 2022). Prominent examples of such systems include ReAct (Yao et al., 2023),
which synergizes reasoning and acting in language models by interleaving thought, action, and ob-
servation steps; Existing research has explored how world models can assist LLM-based agents in
planning, such as RAP (Hao et al., 2023), which uses Monte Carlo Tree Search with world mod-
els for improved reasoning, and Guan et al. (2023), which leverages pre-trained LLMs to construct
world models for model-based task planning. These approaches primarily focus on utilizing exist-
ing world models rather than generating them. Similarly, recent work has investigated how world
models can enhance training of LLM-based agents, as demonstrated by AgentGen (Hu et al., 2025b)
and Kimi-K2 (Team et al., 2025). To our best knowledge, our work represents the first systematic
investigation into using autonomous agents for world model generation, bridging the gap between
agent-based problem solving and symbolic world modeling.


7   C ONCLUSION

We introduced AGENT 2W ORLDMulti , a unified multi-agent framework that employs autonomous
LLM-based agents to generate symbolic world models across both PDDL and executable code rep-
resentations. The framework operates through three specialized stages: knowledge synthesis via web
search, world model development with iterative refinement, and evaluation-driven testing through
unit tests and simulation. Experimental results demonstrate consistent state-of-the-art performance
across three world-model generation benchmarks of different types. By enabling fully autonomous
world model generation without human feedback or manual annotations, this work opens new pos-
sibilities for AI systems that can reliably understand and formalize complex environments from
natural language.


                                                   11
Preprint




E THICS S TATEMENT
All authors have read and will adhere to the ICLR Code of Ethics. This work does not involve human
subjects, personal data, demographic attributes, or user studies; IRB approval was therefore not
required. Our experiments use public, non-sensitive benchmarks: Text2World, Code World Models
Benchmark (CWMB), and ByteSized32. We complied with dataset licenses and did not attempt to
deanonymize or enrich any data with personal information. Because AGENT 2W ORLD uses web
search as a tool (§ 3.1.1), we enforced safeguards to reduce legal and research-integrity risks: we
retrieved only publicly accessible pages, implemented a denylist to avoid solution leakage from
benchmark source repositories or discussion pages as discussed in Section 4.3; We have no conflicts
of interest or undisclosed sponsorship related to this work.

R EPRODUCIBILITY S TATEMENT
Implementation details needed to re-create agents, tools, and evaluation are specified in Section 4.3
and Appendix B.1; algorithmic workflow and role specialization are detailed in §3.1.2–§3.1.3 (with
pseudo code in Alg. 1); prompts are provided in Appendix G. For datasets and metrics, benchmark
compositions and metric definitions are summarized in §C and Appendix C.2; ablation settings and
additional figures/tables appear in Appendix D. As discussed in Section 4.3, to facilitate exact runs,
we fix decoding parameters (temperature = 0, top_p = 1) and cap agent turns, specify external ser-
vices (web search API) and denylisted domains to prevent leakage, and report hardware assumptions
(CPU-only). We also provide the source code of our methods in supplementary materials.




                                                 12
Preprint




R EFERENCES
Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Ale-
  man, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical
  report. arXiv preprint arXiv:2303.08774, 2023.
Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge,
   Yu Han, Fei Huang, et al. Qwen technical report. arXiv preprint arXiv:2309.16609, 2023.
Qiguang Chen, Libo Qin, Jinhao Liu, Dengyun Peng, Jiannan Guan, Peng Wang, Mengkang Hu,
  Yuhang Zhou, Te Gao, and Wanxiang Che. Towards reasoning era: A survey of long chain-of-
  thought for reasoning large language models. arXiv preprint arXiv:2503.09567, 2025a.
Qiguang Chen, Mingda Yang, Libo Qin, Jinhao Liu, Zheng Yan, Jiannan Guan, Dengyun Peng,
  Yiyan Ji, Hanjing Li, Mengkang Hu, et al. Ai4research: A survey of artificial intelligence for
  scientific research. arXiv preprint arXiv:2507.01903, 2025b.
Kenneth James Williams Craik. The nature of explanation, volume 445. CUP Archive, 1967.
Nicola Dainese, Matteo Merler, Minttu Alakuijala, and Pekka Marttinen. Generating code
  world models with large language models guided by monte carlo tree search. arXiv preprint
  arXiv:2405.15383, 2024. URL https://arxiv.org/abs/2405.15383. Introduces the Code World
  Models Benchmark (CWMB).
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
  Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd
  of models. arXiv preprint arXiv:2407.21783, 2024.
Lin Guan, Karthik Valmeekam, Sarath Sreedharan, and Subbarao Kambhampati. Leveraging pre-
  trained large language models to construct and utilize world models for model-based task plan-
  ning. In Advances in Neural Information Processing Systems (NeurIPS), volume 36, pp. 79081–
  79094, 2023. URL https://arxiv.org/abs/2305.14909.
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
  Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
  via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
David Ha and Jürgen Schmidhuber. World models. 2018. doi: 10.5281/ZENODO.1207631. URL
  https://zenodo.org/record/1207631.
Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning
  behaviors by latent imagination. arXiv preprint arXiv:1912.01603, 2019.
Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting Hu.
  Reasoning with language model is planning with world model. arXiv preprint arXiv:2305.14992,
  2023.
Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin
  Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. Metagpt: Meta programming for
  a multi-agent collaborative framework. International Conference on Learning Representations,
  ICLR, 2024.
Mengkang Hu, Tianxing Chen, Qiguang Chen, Yao Mu, Wenqi Shao, and Ping Luo. Hiagent: Hier-
 archical working memory management for solving long-horizon agent tasks with large language
 model. arXiv preprint arXiv:2408.09559, 2024.
Mengkang Hu, Tianxing Chen, Yude Zou, Yuheng Lei, Qiguang Chen, Ming Li, Yao Mu, Hongyuan
 Zhang, Wenqi Shao, and Ping Luo. Text2world: Benchmarking large language models for sym-
 bolic world model generation, 2025a. URL https://arxiv.org/abs/2502.13092.
Mengkang Hu, Pu Zhao, Can Xu, Qingfeng Sun, Jianguang Lou, Qingwei Lin, Ping Luo, and
 Saravan Rajmohan. Agentgen: Enhancing planning abilities for large language model based agent
 via environment and task generation. arXiv preprint arXiv:2408.00764, 2025b. URL https:
 //arxiv.org/abs/2408.00764. Accepted by KDD 2025 (Research Track).


                                               13
Preprint




Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot
 planners: Extracting actionable knowledge for embodied agents. In International conference on
 machine learning, pp. 9118–9147. PMLR, 2022.
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Os-
  trow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. arXiv preprint
  arXiv:2410.21276, 2024.
Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu,
  Wei Yin, Xiaotao Hu, Mingkai Jia, et al. 3d and 4d world modeling: A survey. arXiv preprint
  arXiv:2509.07996, 2025.
Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. Open
  Review, 62(1):1–62, 2022.
Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The ai scien-
  tist: Towards fully automated open-ended scientific discovery. arXiv preprint arXiv:2408.06292,
  2024.
Drew McDermott, Malik Ghallab, Adele Howe, Craig Knoblock, Ashwin Ram, Manuela Veloso,
  Daniel Weld, and David Wilkins. Pddl – the planning domain definition language (version 1.2).
  Technical Report CVC TR-98-003 / DCS TR-1165, Yale Center for Computational Vision and
  Control, 1998. URL https://www.cs.cmu.edu/~mmv/planning/readings/98aips-PDDL.pdf.
Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Long Ouyang, Christina Kim, Christo-
  pher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, et al. Webgpt: Browser-assisted
  question-answering with human feedback. arXiv preprint arXiv:2112.09332, 2021.
Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen,
  Yusheng Su, Xin Cong, et al. Chatdev: Communicative agents for software development. arXiv
  preprint arXiv:2307.07924, 2023.
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro,
  Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can
  teach themselves to use tools. Advances in Neural Information Processing Systems, 36:68539–
  68551, 2023.
Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
  Dario Amodei, and Paul F Christiano. Learning to summarize with human feedback. Advances
  in neural information processing systems, 33:3008–3021, 2020.
Hao Tang, Darren Key, and Kevin Ellis. Worldcoder: A model-based llm agent for building world
  models by writing code and interacting with the environment. In Advances in Neural Information
  Processing Systems (NeurIPS), volume 37, pp. 70148–70212, 2024.
Kimi Team, Yifan Bai, Yiping Bao, Guanduo Chen, Jiahao Chen, Ningxin Chen, Ruijue Chen,
  Yanru Chen, Yuankun Chen, Yutian Chen, et al. Kimi k2: Open agentic intelligence. arXiv
  preprint arXiv:2507.20534, 2025.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Niko-
  lay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open founda-
  tion and fine-tuned chat models. arXiv preprint arXiv:2307.09288, 2023.
Peng Wang, Ruihan Tao, Qiguang Chen, Mengkang Hu, and Libo Qin. X-webagentbench: A
  multilingual interactive web benchmark for evaluating global agentic system. arXiv preprint
  arXiv:2505.15372, 2025.
Ruoyao Wang, Graham Todd, Xingdi Yuan, Ziang Xiao, Marc-Alexandre Côté, and Peter Jansen.
  Bytesized32: A corpus and challenge task for generating task-specific world models expressed
  as text games. In Proceedings of the 2023 Conference on Empirical Methods in Natural Lan-
  guage Processing (EMNLP), 2023. doi: 10.18653/v1/2023.emnlp-main.830. URL https:
  //aclanthology.org/2023.emnlp-main.830/.


                                               14
Preprint




Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdh-
  ery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models.
  arXiv preprint arXiv:2203.11171, 2022.

Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable
  real-world web interaction with grounded language agents. Advances in Neural Information Pro-
  cessing Systems, 35:20744–20757, 2022.

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models. In International Conference on
  Learning Representations (ICLR), 2023. URL https://arxiv.org/abs/2210.03629.

Zhouliang Yu, Yuhuan Yuan, Tim Z Xiao, Fuxiang Frank Xia, Jie Fu, Ge Zhang, Ge Lin, and
  Weiyang Liu. Generating symbolic world models via test-time scaling of large language models.
  arXiv preprint arXiv:2502.04728, 2025.

Jiayi Zhang, Yiran Peng, Fanqi Kong, Yang Cheng, Yifan Wu, Zhaoyang Yu, Jinyu Xiang, Jianhao
   Ruan, Jinlin Wang, Maojia Song, et al. Autoenv: Automated environments for measuring cross-
   environment agent learning. arXiv preprint arXiv:2511.19304, 2025.

Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min,
 Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. arXiv
 preprint arXiv:2303.18223, 1(2), 2023.

Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan Ye, Zheyan Luo, Zhangchi Feng, and
  Yongqiang Ma. Llamafactory: Unified efficient fine-tuning of 100+ language models. In Pro-
  ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume
  3: System Demonstrations), Bangkok, Thailand, 2024. Association for Computational Linguis-
  tics.

Chunting Zhou, Pengfei Liu, Puxin Xu, Srini Iyer, Jiao Sun, Yuning Mao, Xuezhe Ma, Avia Efrat,
  Ping Yu, Lili Yu, Susan Zhang, Gargi Ghosh, Mike Lewis, Luke Zettlemoyer, and Omer Levy.
  Lima: Less is more for alignment, 2023. URL https://arxiv.org/abs/2305.11206.

Appendix
A     T HE U SE OF L ARGE L ANGUAGE M ODELS

We used a large language model (LLM) strictly as a general-purpose writing assistant for surface-
level editing, such as grammar correction, wording polish, and minor style consistency. The LLM
was not used for conceptual ideation, literature review, algorithm or model design, data collection
or labeling, experiment setup, result analysis, or drafting of technical content.


B     M ORE D ETAILS ON M ETHODOLOGY

B.1   P ER - AGENT T OOL C ONFIGURATION

                                    Table 5: Per-agent configuration.

                     Agent                                  Tools
                Deep Researcher                 browser_search; browser_open
                Model Developer                  file_tool; sandbox; run_code
                Simulation Tester                      play_env; file_tool
                   Unit Tester                   run_code; run_bash; file_tool


Detailed per-agent tool configuration is presented in Table 5.


                                                   15
Preprint




Algorithm 1: The execution pipeline of AGENT 2W ORLDMulti
Input: T, N
Output: e
Nr ← predefined integers;
R←∅;
E ←∅;
Q ← ExtractQuestions(T );
for r ← 1 to Nr do
    q ← ResearchAgent(select, {Q, E, R});
    if q = ∅ then
         break
    L ← WebSearch (q);
    E ← E ∪ ResearchAgent(summarize, {L});
    R ← ResearchAgent(update, {T, E, R});
Ft ← R;
Clast ← ∅;
for n ← 1 to N do
    Cd ← DevelopAgent(T, Ft );
    if Cd ̸= ∅ then
         Clast ← Cd ;
         pcode ← FileTool(save, Cd );
    else
         continue
    Ct ← UnitTestAgent(Cd , T, R);
    ptest ← FileTool(save, Ct );
    Ut ← CodeTool(run_tests, {pcode , ptest });
    St⋆ ← PlayEnv(Cd );
    St ← SimulationTestAgent(St⋆ , T );
    if Ut .pass ∧ St .pass then
         e ← Clast ;
         return e;
    Ft ← MergeFeedback(Ut , St );
e ← Clast ;
return e


B.2   P SEUDO C ODE OF AGENT 2W ORLDMulti

We formalize the process of AGENT 2W ORLDMulti in Algorithm 1.


C     M ORE D ETAILS ON B ENCHMARKS

C.1   S IDE - BY- SIDE C OMPARISON

Table 6: Overview of Text2World (Hu et al., 2025a), Code World Models Benchmark
(CWMB) (Dainese et al., 2024), and ByteSized32 (Wang et al., 2023). “Type” denotes the tar-
get representation (PDDL vs. executable code). Metrics are shown at the family level. A detailed
explanation of each metric is presented in Appendix C.2.

 Benchmark     #Environments         Type                         Metrics (core)
 Text2World         103            PDDL             Executability; Domain similarity; F1 scores
 CWMB                18         Code (Python)   Accuracy; Normalized return R (discrete/continuous)
                                                   Technical validity; Specification compliance;
 ByteSized32         32         Code (Python)
                                                      Winnability; Physical reality alignment


A side-by-side comparison of the evaluated benchmarks in this paper is presented in Table 6


                                                16
Preprint




C.2    M ETRIC E XPLANATION

Text2World
Executability. Name: Exec. Range: [0, 1] (higher is better). Whether the generated {domain,
   problem} can be successfully parsed and validated by standard PDDL validators; reported as the
   fraction (percentage) over all test cases. Fine-grained metrics below are computed only when
   Exec= 1.
Domain similarity. Name: Sim. Range: [0, 1] (higher is better). Textual/structural similarity be-
   tween the generated and gold PDDL measured by a normalized Levenshtein ratio.
   Let X and Y be the character sequences of the two files with lengths |X| and |Y |, and let
   Lev(X, Y ) denote their Levenshtein distance, then
                                                   Lev(X, Y )
                           Sim(X, Y ) = 1 −                       ∈ [0, 1].                   (1)
                                                 max{|X|, |Y |}
F1 scores. Range: [0, 1] (higher is better). When Exec= 1, we parse both generated and gold
   PDDL into structured representations and report macro-averaged F1 for the following compo-
   nents: Predicates (F1PRED ), Parameters (F1PARAM ), Preconditions (F1PRECOND ), and Effects
   (F1EFF ).We use the standard definition of F1 , where P and R denote precision and recall, re-
   spectively:
                                                    2PR
                                            F1 =
                                                    P+R
CWMB
Prediction Accuracy. Symbol: Accpred . Range: [0, 1] (higher is better). Definition: We use the
   same accuracy metric as in the evaluation phase of GIF–MCTS (Sec. 4). Given a validation set
                                                                          ˆ
                                   i=1 and CWM predictions (ŝi , r̂i , di ) = CWM.step(si , ai ), the accuracy
   D = {(si , ai , ri , s′i , di )}N                                ′

   uniformly weights next state, reward, and termination:
                                        N
                                     1 Xh 1                                                     i
                    Accpred =               3 1(ŝ′i = s′i ) + 13 1(r̂i = ri ) + 31 1(dˆi = di ) .          (2)
                                    N i=1
Normalized Return. Symbol: R. Range: unbounded (higher is better; R > 0 means better than
   random; R → 1 approaches the oracle). Definition:
                                       R(πCWM ) − R(πrand )
                                 R=                            ,                             (3)
                                        R(πtrue ) − R(πrand )
   where R(π) denotes the return. Protocol: as in the original setup, we use vanilla MCTS for
   discrete action spaces and CEM for continuous action spaces; R(·) is averaged across a fixed
   number of episodes per environment (10 in the original), and R(πrand ) uses the environment’s
   random policy baseline.

ByteSized32
Technical Validity. Range: [0, 1]. Measured in the order of API calls, such that failure of an earlier
   function implies failure of subsequent tests. Game initialization is evaluated once at the
   beginning of the game, whereas GENERATEPOSSIBLEACTIONS() and STEP() are evaluated at every
   step. We check:
      • Game initialization: the game/world initializes without errors;
      • Valid actions generation: the routine that enumerates valid actions for the current state
        returns without errors (verified via a bounded path crawl);
      • Runnable game: a bounded-depth crawl of trajectories executes without errors.
Specification Compliance. Range: [0, 1]. An LLM acts as the judge for true/false compliance
   against the task specification. The prompt provides the task spec {GAME_SPEC}, the game code
   {GAME_CODE}, and an evaluation question {EVAL_QUESTION}; the LLM is instructed to first out-
   put Yes/No and then a brief rationale. To reduce variance, we use a fixed prompt template and
   perform multiple independent runs with majority vote/mean aggregation. We report three sub-
   measures: Task-critical objects, Task-critical actions, and Distractors.


                                                      17
Preprint




Physical Reality Alignment. Range: [0, 1]. Automatic evaluation proceeds in two stages:
   (1) Trajectory generation: perform a breadth-first crawl using the action strings returned by
   GENERATEPOSSIBLEACTIONS() at each step; actions are grouped by verb (first token) and ex-
   panded in a bounded manner. If an error occurs, the error message is recorded as the observation,
   and the search continues.
   (2) Sampling and judgment: group paths by the last action verb, draw a fixed-size subsample ap-
   proximately balanced across groups, and submit each path—together with the task description
   {GAME_TASK}—to an LLM for a binary judgment (yes/no; errors are treated as failures). The
   final score is the fraction judged aligned.
Winnability. Range: [0, 1]. A text-game agent (LLM agent) attempts to reach a terminal win within
  horizon H; we report the fraction of tasks deemed winnable. Given the limited agreement
  between automatic and human assessments for this metric, we prioritize human evaluation in the
  main results and use the automatic estimate asan auxiliary reference.

D     M ORE D ETAILS ON A BLATION S TUDY

           Table 7: Ablation Study of AGENT 2W ORLD on CWMB (Dainese et al., 2024).

                           Discrete Action Space         Continuous Action Space                    Overall
 Method
                        Accuracy (↑)       R (↑)        Accuracy (↑)       R (↑)        Accuracy (↑)          R (↑)
 AGENT 2W ORLD             0.9174          0.8333          0.3575          0.3050          0.5441             0.4811
 No Deep Researcher     0.8794−0.0380   0.4407−0.3926   0.3404−0.0171   0.2201−0.0849   0.5201−0.0240   0.2936−0.1875
 No Simulation Tester   0.8920−0.0254   0.5718−0.2615   0.3288−0.0287   0.1577−0.1473   0.5275−0.0166   0.3039−0.1772
 No Unit Tester         0.6166−0.3008   0.3863−0.4470   0.3025−0.0550   0.1704−0.1346   0.4072−0.1369   0.2423−0.2388


Detailed experimental results of the ablation study are presented in Table 7.

E     M ORE D ETAILS ON DATA C ONSTRUCTION

                               Table 8: Train Data Before and After Filtering

                           Status         CWMB          ByteSized32     PDDL        MCP
                           Unfiltered       500             500           600       800
                           Filtered         266             277           483       500



F     M ORE D ETAILS ON E RROR A NALYSIS
F.1   E RROR A NALYSIS ON T EXT 2W ORLD AND B YTE S IZED 32

We visualize the error patterns during evaluation-driven refinement on Text2World and ByteSized32
in Figure 7 and Figure 8.

F.2   D ISTRIBUTION OF E RROR T YPES

A detailed proportion of error types on Text2World, CWMB, ByteSized32 are presented in Table 9,
Table 10 and Table 11, respectively.

F.3   E RROR D ISTRIBUTION OF BASELINES AND C OMPARISON

As shown in Table 12, both WorldCoder and GIF-MCTS still exhibit several residual dynamics-
related failures in their final outputs: although they no longer trigger signature- or schema-mismatch
errors, they retain multiple dynamics-error and judgment-bug cases, together with non-trivial
invariant-violation counts. This suggests that their search procedures are effective at ironing out


                                                         18
Preprint




                                Success
                                                        Success

     Input                                                                       Success

                                                                                                          Output


                                type-mismatch
                                                        incorrect-parentheses
                                undefined-constant
                                                        undefined-constant
                                incorrect-parentheses                            undefined-constant
                                undefined-type          type-mismatch
                                                                                 type-mismatch
                                unsupported-feature     undefined-type           duplicate-definition
                                duplicate-definition    duplicate-definition




                 Figure 7: Error distribution of AGENT 2W ORLDMulti on Text2World.




                                Success
                                                        Success

      Input                                                                      Success
                                                                                                         Output

                                state-bug

                                invalid-action          state-bug
                                syntax-error
                                                        invalid-action           state-bug
                                contract-fail
                                                        contract-fail
                                undefined-symbol                                 undefined-symbol
                                                        undefined-symbol



                Figure 8: Error distribution of AGENT 2W ORLDMulti on ByteSized32.

                 Table 9: Distribution of Syntax Errors in Text2World Across Turns

                                                                                               Turn 0 Turn 1 Turn 2
Error Type               Explanation
                                                                                                (%)    (%)    (%)
undefined-constant       Reference to undeclared constants in predicates or actions.              8.91      7.92    6.93
type-mismatch            Parameter type conflict with declared type constraints.                  2.97      4.95    2.97
incorrect-parentheses    Invalid or mismatched parentheses.                                       2.97      1.98    0.00
undefined-type           Undeclared parent type in hierarchical type definitions.                 1.98      0.99    0.00
unsupported-feature      Parser-incompatible features (e.g.,either types).                        1.98      0.00    0.00
duplicate-definition     Multiple declarations of identical domain elements.                      0.99      0.99    0.99


                   Table 10: Distribution of Syntax Errors in CWMB Across Turns

                                                                                 Turn 0 Turn 1 Turn 2 Turn 3
Error Type              Explanation
                                                                                  (%)    (%)    (%)    (%)
signature-mismatch      Arity/types do not match the declared signature.          27.78          11.11      11.11    5.56
schema-mismatch         Value type/shape/dtype violates the expected schema.      22.22          5.56        0.00    0.00
dynamics-error          State or reward deviates from expected dynamics.          11.11          44.44      33.33   11.11
non-deterministic       Results are inconsistent under fixed conditions.          11.11          0.00        0.00    0.00
judgment-bug            Environment setup inconsistent with the description.      11.11          5.56       11.11    5.56
invariant-violation     Internal invariants are broken (e.g., illegal config).     0.00          5.56        0.00    5.56



                                                         19
Preprint




                Table 11: Distribution of Syntax Errors in ByteSized32 Across Turns

                                                                                       Turn 0 Turn 1 Turn 2
Error Type         Explanation
                                                                                        (%)    (%)    (%)
state-bug          State inconsistency across steps.                                   19.82   13.51       7.21
contract-fail      Task/API contract not satisfied.                                    6.31     3.60       0.00
undefined-symbol   Reference to undeclared name/type/domain/constant.                  5.41     2.70       1.80
invalid-action     Unknown or unsupported action not safely handled.                   2.70     0.90       0.00
syntax-error       Load/parse failure (e.g., null bytes, syntax/indentation errors).   0.90     0.00       0.00


            Table 12: Distribution of Syntax Errors in CWMB Across Methods and Turns

                                 signature- schema- dynamics-     non-      judgment- invariant-
 Method
                                 mismatch mismatch    error   deterministic    bug     violation
 WorldCoder (Last Turn)              0            0            3              0            2           2
 GIF-MCTS (Last Turn)                0            0            2              0            3           2
 AGENT 2W ORLDMulti (Turn 1)         2            1            8              0            1           1
 AGENT 2W ORLDMulti (Turn 2)         2            0            6              0            2           0
 AGENT 2W ORLDMulti (Turn 3)         1            0            2              0            1           1



interface- and type-level inconsistencies, but are less successful at fully aligning the learned dynam-
ics with the intended environment specification.
In contrast, AGENT 2W ORLDMulti starts from a broader spectrum of error types at turn 1 (includ-
ing signature/schema mismatches and a larger number of dynamics errors), and progressively
suppresses them over subsequent refinement rounds. By turn 3, schema mismatches and nNon-
deterministicbehaviors have disappeared, signature mismatches are reduced to a single case, and
dynamics errors, judgment bugs, and invariant violations are all substantially lower than those of
the baselines. This trajectory is consistent with the qualitative analysis in Section 5.4: the Testing
Team first drives the Model Developer to resolve structural and specification-level issues, and then
focuses on subtle dynamics and invariant failures, ultimately producing world models that are both
syntactically robust and semantically faithful to the target environments.


G     P ROMPT E XAMPLES

    Deep Researcher

    You are a world-class Systems Analyst and Technical Specification Writer, specializing in
    creating reinforcement learning environments compliant with the Gymnasium API. Your mis-
    sion is to transform an ambiguous task description into a precise, actionable, and verifiable
    technical specification.
    <Environment Name>
    CliffWalking-v0
    </Environment Name>
    <TASK DESCRIPTION>
    Cliff walking involves crossing a gridworld from start to goal while avoiding falling off a cliff.
    ## Description ...
    </TASK DESCRIPTION>
    <Workflow>
    Please strictly follow the following six-step process:
           • Deconstruction and Analysis (Use Version Locking)
                – Identify all ambiguities, gaps, and conflicts in the task description.
                – Lock the exact environment version and all key library versions (record name,
                  version, and source link).


                                                      20
Preprint




               – Categorize gaps by type:          missing value/unit/range boundary/time-
                 sensitive/ambiguous reference/unclosed list/conflict/no provenance.
           • Planning and Investigation (Authoritative Search + Evidence Log)
               – For each high/mid-level project, write 1–2 focused queries that include: syn-
                 onyms/abbreviations, site filters, authoritative domains (e.g., site:numpy.org,
                 site:mujoco.readthedocs.io, site:doi.org), and recency windows (e.g., after 2024-
                 01-01 or “last 2 years”).
               – Execute the query using browser_search and open >= 2 trusted results with
                 browser_open.
               – If the top source disagrees, open >= 1 additional authoritative sources and trian-
                 gulate.
               – Create an evidence log entry for each opened page: Title | Organization/Author
                 | Version/Submission | URL (+ archived URL) | Publication Date | Access Date
                 (Asia/Singapore) | 3 Key Facts | Confidence (High/Medium/Low).
           • Synthesis and Citation (Conflict Resolution)
               – Integrate the findings into a concise evidence summary with citations.
               – When sources conflict, explain the differences and justify the chosen resolution
                 (related to version locking).
           • Refinement and Improvement (Specification Patch)
               – Generate a structured “diff”: action/observation space; rewards; termina-
                 tion/truncation; timing (dt/frame_skip); seeding and certainty; numerical tol-
                 erances; dependencies; interface flags.
           • Formalization and Finalization (Ready-to-Use Specification)
               – Write the final specification according to the <Output Format> , including the
                 public API, core logic, usage scenarios, and a verification plan aligned with
                 metrics and statistical validation.
           • Review and Self-Correction (Compliance Check)
               – Verify     conformance     to the <Output  Constraints>    (OUT-
                 PUT_CONSTRAINTS>), version consistency, SI units, ISO dates, and
                 the inclusion of any code.
  </Workflow>
  <OUTPUT_CONSTRAINTS>
           • Strictly adhere to the structure defined in <PLANNING_STRUCTURE>.
           • Do NOT output runnable code definitions (classes, functions). Only may include
             short illustrative snippets or pseudo-code.
           • All claims about industry standards or common practices MUST be supported by
             citations.
           • Use ISO-8601 dates (e.g., 2025-09-02).
           • Use SI units for physical and mathematical quantities.
           • Data-leakage rule: Do not access, copy, quote, or derive from raw source code in the
             OpenAI/Gym/Gymnasium repositories or similar code repositories. Do not include
             any repository code in the output. Prefer official documentation, standards, papers,
             or reputable secondary sources. If the only available evidence is a code repository,
             summarize behavior without copying code and mark it as an inference with risks.
  <PLANNING_STRUCTURE>
           • Your output must begin with this planning and analysis section.
           • Ambiguity Analysis
               – List each ambiguity/vagueness/conflict and mark Impact: High / Medium / Low.




                                                  21
Preprint




               – Cover at least: missing numeric value, missing unit, missing boundary/range,
                 time-sensitive items, unclear references, open lists (“etc.”/“e.g.”), conflicts, and
                 missing citation.
           • Investigation Plan
               – For each High/Medium item, provide one atomic question.
               – For each question, provide 1–2 executable queries including: synonyms/ab-
                 breviations, a site filter to authoritative domains, and a time window (e.g.,
                 after:2024-01-01 or “past 2 years”).
               – State the minimum evidence policy: High/Medium → ≥ 2 credible sources; if
                 disagreement → add ≥ 1 more for triangulation.
  <Formula requirements>
           • For any formula, define all symbols, units, and applicability constraints.
           • Cite the source of the formula immediately after its definition.
           • Provide the complete formula rather than a descriptive explanation.
  <OUTPUT_FORMAT>
           • Please provide the final specification document structured as follows. This is the
             primary deliverable. Do NOT include code.
           • <Version & Provenance>
           • <Evidence Summary>
           • <Spec Patch>
           • <Theoretical Foundations>
           • <Final Specification>
           • <Assumptions & Risks>
           • <Third-Party Library Usage>

  Model Developer

  <TASK DESCRIPTION>
  Cliff walking involves crossing a gridworld from start to goal while avoiding falling off a cliff.
  ## Description ...
  </TASK DESCRIPTION>
  <Research Report>
  # CliffWalking-v0 Environment Specification
  Version & Provenance
         • Environment: CliffWalking-v0
         • Gymnasium version: v0.26.3 (2022-09-15) and latest documentation snapshot (2025-
           01-01)
         • Scope: This specification normalizes the CliffWalking environment as implemented
           in Gymnasium v0.26.3, aligning with the classic gridworld cliff walking task.
         • Accessed date: 2024-06-01 (Asia/Singapore)
  Evidence Summary
         • The environment is a 4x12 grid with 48 discrete states indexed by row-major flatten-
           ing: state = row * 12 + col.
         • Valid states exclude cliff cells ([3,1..10]) and the goal ([3,11]). The player can occupy
           all cells in the first 3 rows plus the bottom-left cell [3,0].
         • The start state is 36 (row=3, col=0), and the goal state is 47 (row=3, col=11).
         • The action space is Discrete(4) with actions: 0 (up), 1 (right), 2 (down), 3 (left).
         • Each step yields a reward of -1. Stepping into the cliff yields a reward of -100 and
           resets the player to the start state; the episode continues.


                                                  22
Preprint




           • The episode terminates only when the player reaches the goal state.
           • The set_state method is not explicitly documented but is inferred to accept any valid
             non-terminal, non-cliff state and sets the environment to not done.
           • No explicit error handling for invalid actions is documented; valid inputs are as-
             sumed.
           • The environment is deterministic.
  Spec Patch
           • action.space = Discrete(4), values {0,1,2,3}, shape (1,)
           • observation.space = Discrete(48), integer in [0,47], representing flattened grid index:
             row * 12 + col
           • valid states = all grid cells except cliff cells ([3,1..10]) and goal ([3,11])
           • start_state = 36 (row=3, col=0)
           • goal_state = 47 (row=3, col=11)
           • reward.step = -1 per step
           • reward.cliff = -100 on stepping into cliff
           • episode termination = True if state == goal_state; else False
           • stepping into cliff resets player to start_state, episode continues
           • set_state(state: int) sets environment state to given valid state, done = False
           • no maximum episode length or truncation condition
           • no explicit error handling for invalid actions; assume valid input
           • environment deterministic transitions
  Theoretical Foundations
           • MDP Definition:
                – State space S = {0, . . . , 47} \ {cliff states, goal state}.
                – Action space A = {0, 1, 2, 3}.
                – Transition function T (s, a, s′ ) (deterministic):
                         ′
                   * If s is a cliff cell, next state = start_state.
                   * Else next state = s + δ(a) (with grid boundary checks).
                – Reward function R(s, a, s′ ):
                                      ′
                   * R = −100 if s is a cliff cell.
                   * R = −1 otherwise.
                – Episode ends when s′ = goal_state.
           • Symbol Table:
                – s: state (int), flattened grid index, 0 ≤ s ≤ 47, s not in cliff or goal.
                – a: action (int), in {0 : up, 1 : right, 2 : down, 3 : left}.
                – r: reward (float), −100 or −1.
                – done: boolean, True if s = goal_state.
                – start_state: 36 (int).
                – goal_state: 47 (int).
                – cliff_cells: set of ints corresponding to grid positions [3, 1..10].
                – nrows: 4 (int).
                – ncols: 12 (int).
           • Assumptions:
                – No shaping rewards.
                – Deterministic environment.
                – No truncation or max step limit.



                                                    23
Preprint




  Final Specification
           • Environment Name
               – CliffWalking-v0
           • Public API
               – __init__()
               – set_state(state: int)
               – step(action: int) → (observation: int, reward: float, done: bool)
           • Core Logic Description
               – __init__:
                  * Initialize grid size (4 rows × 12 columns).
                  * Define start_state = 36 (row=3, col=0).
                  * Define goal_state = 47 (row=3, col=11).
                  * Define cliff cells as positions [3, 1..10].
                  * Initialize current state to start_state.
                  * Initialize done flag to False.
               – set_state(state: int):
                  * Validate that state is a valid observation (not cliff or goal).
                  * Set current state to state.
                  * Set done flag to False.
               – step(action: int) → (obs, reward, done):
                  * Validate action is in {0, 1, 2, 3}.
                  * Compute next position based on action with boundary checks:
                     · 0: move up (row −1)
                     · 1: move right (col +1)
                     · 2: move down (row +1)
                     · 3: move left (col −1)
                  * If next position is outside grid, remain in current position.
                  * If next position is a cliff cell:
                     · reward = −100
                     · next state = start_state
                     · done = False
                  *  Else if next position is goal_state:
                     · reward = −1
                     · done = True
                     · next state = goal_state
                  *  Else:
                     · reward = −1
                     · done = False
                     · next state = computed position
                  *  Update   current state to next state and return (next state, reward, done).
           • Usage Scenarios
               – Scenario 1: Normal move into cliff
                  * Initial state: 36 ([3,0])
                  * Action: 1 (right)
                  * Next state: 37 ([3,1]) is cliff → reset to 36
                  * Reward: −100
                  * done: False
               – Scenario 2: Move to goal
                  * Current state: 46 ([3,10])
                  * Action: 1 (right)



                                                   24
Preprint




              * Next state: 47 ([3,11]) goal
              * Reward: −1
              * done: True
           – Scenario 3: Move up from start
              * Current state: 36 ([3,0])
              * Action: 0 (up)
              * Next state: 24 ([2,0])
              * Reward: −1
              * done: False
  Assumptions & Risks
            • No truncation or maximum episode length specified; risk of infinite episodes if goal
              not reached.
            • set_state accepts only valid non-terminal, non-cliff states; no explicit error handling
              for invalid states.
            • No explicit error handling for invalid actions; assumed caller responsibility.
            • Reward and reset behavior on cliff stepping inferred from documentation; no episode
              termination on cliff.
            • Observation space includes all grid cells but player never occupies cliff or goal states.
            • Potential future Gymnasium version changes may alter behavior.
  Third-Party Library Usage
            • Gymnasium API conventions inform environment interface: discrete action and ob-
              servation spaces, step and reset semantics.
            • No new runtime dependencies introduced.
            • RNG seeding not specified; environment deterministic.
            • No source code copied; specification based on official Gymnasium documentation
              and Sutton & Barto RL book.
            • Numpy indexing conventions used for grid flattening.
  </Research Report>

  <Workflow>
  1. Deconstruct Specification: Carefully review the <Task Describe>,<Research Report>
  to fully understand the environment’s specification, including state/action spaces, dynamics,
  reward function, and termination conditions.
  2. Physics Engine Selection: Evaluate if the task requires physics simulation. If so, choose
  an appropriate physics engine for the specific task requirements.
  3. Model Design: If using a physics engine, design the model structure and embed it as
  needed in the Python file.
  4. Plan Class Structure: Outline the ‘Environment‘ class, including its internal state
  variables, helper methods, and the public interface (‘__init__‘, ‘reset‘, ‘set_state‘, ‘step‘).
  5. Implement Complete Code: Write the full implementation of the ‘Environment‘ class. 6.
  Self-Correction Review: Meticulously check that the generated code fully complies with the
  <TASK DESCRIPTION>, the <Research Report>, and all <ImplementationRequirements>.
  7. Finalize Output: Present the complete, reviewed, and runnable single-file code in the
  specified final format.
  </Workflow>

  <ImplementationRequirements>
           1. Interface (single file):
                 • Implement a complete, self-contained Python class Environment with:
                    – __init__(self, seed: int | None = None)




                                                    25
Preprint




                   – reset(self, seed: int | None = None) → ndarray (reinitialize the episode and
                     return the initial observation in canonical shape)
                   – set_state(self, state) (must accept ndarray or list/tuple in canonical shape)
                   – step(self, action) → tuple[ndarray, float, bool] (returns: observation, reward,
                     done)
                • Requirements:
                   – Single-file constraint: all code, including any model definitions, must be
                     contained in one Python file.
                   – For physics-based environments, embed model definitions as string con-
                     stants within the class.
                   – Explicitly define state, action, and observation spaces (types, shapes, ranges,
                     formats).
                   – Provide reproducibility (seeding) via the constructor and/or a seed(int)
                     method.
                   – Be robust to common representations:
                     * set_state: accept list/tuple/ndarray of the same logical content.
                     * step: accept int / NumPy integer scalar / 0-D or 1-D len-1 ndarray (convert
                        to canonical form; raise clear TypeError/ValueError on invalid inputs).
                   – No dependence on external RL frameworks; no Gym inheritance.
                   – No external file dependencies (model definitions must be embedded).
                   – Maintain internal state consistency; allow reconstruction from observations
                     where applicable.
                   – Clean, readable code suitable for RL experimentation.
           2. Determinism & validation:
                • Provide reproducibility via seed (constructor and/or seed(int) method).
                • Normalize inputs: accept equivalent representations (e.g., NumPy scalar/int/len-
                  1 array) and convert to a canonical form.
                • Validate inputs; raise clear one-line errors (ValueError/TypeError) on invalid
                  shapes or ranges.
           3. Dynamics (MCTS/control oriented):
                • For physics-based tasks, prefer suitable physics simulation methods with em-
                  bedded model definitions over custom physics implementations.
                • Choose and document an integration scheme (e.g., implicit integrator, explicit
                  Euler) consistent with the research report.
                • Use a stable time step dt; clamp to safety bounds; keep all values finite (no
                  NaN/Inf).
                • Keep per-step computation efficient and allocation-light.
           4. Dependencies & style:
                • No Gym inheritance or external RL frameworks unless explicitly allowed.
                • Allowed: third-party libraries as needed (e.g., NumPy, physics engines, SciPy,
                  Numba, JAX, PyTorch, etc.).
                • For robotics/physics tasks, physics engines with embedded model definitions are
                  recommended over custom implementations.
                • Clean, readable code suitable for RL experimentation.
                • All dependencies must be importable standard libraries or commonly available
                  packages.
  </ImplementationRequirements>
  <Output Format>
  <final> <code_file_path> The entrypoint file path of the generated code. </code_file_path>
  <entrypoint_code> “‘python # Your complete, runnable single-file implementation here. “‘
  </entrypoint_code> </final>
  </Output Format>



                                                  26
Preprint




  Unit Tester
  <TASK DESCRIPTION> Cliff walking involves crossing a gridworld from start to goal
  while avoiding falling off a cliff.
  ## Description ...
  </TASK DESCRIPTION>
  <CodeArtifact path="environment.py"> {code} </CodeArtifact>
  <ExecutionPolicy>
           • Do not modify the student’s source file.
           • Create exactly one pytest file at “tests/test_env.py” using file_tool(“save”).
           • Import the module from “environment.py” via importlib (spec_from_file_location +
             module_from_spec).
           • Run tests with code_tool(“run”, “pytest -q”); capture exit_code, duration, and std-
             out/stderr tail.
  </ExecutionPolicy>
  <TestPlan>
           • Sanity:   class Environment          can   be    imported      and   instantiated,   e.g.,
             Environment(seed=0).
           • Contract:
                1. set_state accepts list/tuple/ndarray of the same logical content (convert to
                   canonical).
                2. step(action) returns a 3-tuple: (observation, reward, done) with expected type-
                   s/shapes.
                3. Determinism: with the same seed and same initial state, the first step with the
                   same action yields identical outputs.
                4. Action space validation: actions within bounds are accepted, out-of-bounds ac-
                   tions are handled gracefully.
                5. Observation space validation: observations match declared space bounds and
                   shapes.
                6. State space consistency: internal state dimensions match expected environment
                   specifications.
           • Acceptance: success iff pytest exit_code == 0 (all tests pass).
  </TestPlan>
  <ReportingGuidelines>
           • Summarize pytest results in 2–4 sentences; mention the first failing nodeid/assert if
             any.
           • Provide a brief contract coverage assessment and the most probable root cause for
             failures.
           • If failing, add 1–3 concise actionable fixes (no long logs).
  </ReportingGuidelines>
  <OutputFormat> Return exactly one <final> block containing a single JSON object that
  matches PytestReport: {
  "success": true|false,
  "analysis": "<2–4 sentence summary/diagnosis>",
  "suggest_fix": " 1–3 bullets with minimal actionable changes>"
  } No extra text outside <final>. No additional code fences.
  <final> { "success": false, "code_result": "", "analysis": "", "suggest_fix": "" } </final>
  </OutputFormat>




                                                   27
Preprint




  Simulation Tester
  Your task is to interact with the environment code and then analyze the feedback from the
  interaction and propose modifications
  <TASK DESCRIPTION>
  Cliff walking involves crossing a gridworld from start to goal while avoiding falling off a cliff.
  ## Description ...
  </TASK DESCRIPTION>
  <CodeArtifact path="environment.py">
  {code}
  </CodeArtifact>

  <ExecutionPolicy>
  - Use the play_env tool exactly once on "environment.py" - If the tool throws or cannot run,
  perform diagnosis from static review only; still produce output in the required format.
  </ExecutionPolicy>
  <Rubric>
  Success (boolean) must be decided from the available signals with graceful degradation:
           • Primary (step-level signals present):
               – success = true iff the run finished without exceptions AND there is NO misclas-
                  sified_transition with (valid == false OR state_matches == false).
               – If only observation deltas are available, use obs_matches instead of
                  state_matches.
               – When numeric deltas are provided, treat matches = true if max_abs_error ≤
                  10−3 or rel_error ≤ 10−3 .
           • Secondary (no per-step signals):
               – If success_rate exists: success = true iff no exceptions AND success_rate ≥
                  0.95.
               – Else: success = true iff no exceptions AND no invariant/contract violations you
                  can substantiate from code and logs.
           • Reward/termination:
               – If reward_matches == true AND done_matches == true, explicitly state they
                  match and DO NOT propose changes to reward or termination logic.
           • Action space consistency (discrete & continuous):
               – If GT exposes Box(low, high, shape): align predicted bounds and expose them
                  (e.g., env.action_space or a getter). Never place clipping inside the integrator;
                  clamp only at action ingestion or at observation.
               – If GT exposes Discrete(n): actions must be integer indices in [0, n−1]; expose
                  n (e.g., gym.spaces.Discrete(n)); if indices map to continuous commands/-
                  torques, list the mapping table and align it with GT; never float-clip discrete
                  actions.
               – If action-space info is missing, skip these checks (do not speculate).
           • Internal vs observation:
               – If clipping or angle normalization is found inside the integrator step (e.g., in
                  _rk4_step), this likely causes trajectory drift; propose moving them to the ob-
                  servation path (e.g., _get_observation) unless GT specifies otherwise.
               – If latent state is unavailable but observations exist, compare observations instead
                  and state this explicitly.
           • Integrator & timestep:
               – Mismatches in integrator method (e.g., RK4 vs Euler) or dt can cause state di-
                  vergence even when reward/done match; acknowledge and, if state mismatches
                  persist, propose aligning method/dt to GT.
           • Batched/multiple transitions:


                                                  28
Preprint




               – If multiple transitions are reported, aggregate sensibly (e.g., mean success_rate
                 or fraction matched ≥ 0.95) before deciding success.
    </Rubric>
    <Procedure>
    1) Static review: scan for action bounds, clipping/normalization inside integrator, integrator/dt
    choice, and how observation is formed.
    2) Execute: call play_env once.
    3) Diagnose: reconcile play_env signals with code; if reward/done matched, explicitly say so.
    If state mismatched, point to ONE OR TWO most likely roots.
    4) Suggest: 1–3 smallest patches that directly address the identified root causes.
    </Procedure>
    <OutputFormat>
    Return exactly one <final> block containing a single JSON object that matches PlayReport:
    { "success": true|false, "analysis": "<2–4 sentences summarizing what happened and why;
    mention matches/mismatches explicitly>", "suggest_fix": "- bullet 1\n- bullet 2\n- bullet 3
    (optional)" } No extra text outside <final>. No additional code fences.
    </OutputFormat>


H     E XAMPLES OF D EEP R ESEARCHER R EPORT
    Deep Researcher’s Report

    <Version & Provenance>
          • Environment: Pusher-v4
          • MuJoCo version: ≥ 2.1.3 and < 3.0.0
          • Source release date: 2024-01-01 (approximate for v4)
          • Accessed date: 2025-06-01 (Asia/Singapore)
    <Spec Patch>
          • action.space = Box(low=-2.0, high=2.0, shape=(7,), dtype=np.float32)
          • observation.space: Box with low = −∞, high = ∞, shape (23, ), dtype np.float64
          • reward.weights = {dist: 1.0, ctrl: 0.1, near: 0.5}
          • reward.formula: reward = reward_dist + 0.1 reward_ctrl + 0.5 reward_near
          • reward_ctrl = −∥a∥22 (negative squared Euclidean norm)
          • reward_dist = −∥o − g∥2 (negative Euclidean distance)
          • reward_near = −∥f − o∥2 (negative Euclidean distance)
          • episode.max_steps = 100
          • episode.termination: never (terminated always False)
          • episode.truncation: True if step count ≥ max_steps or any observation value is non-
            finite
          • dt = 0.05 s (frame_skip= 5, frame_duration= 0.01)
          • initial_state.joint_positions = 07
          • initial_state.joint_velocities: each joint ∼ U (−0.005, 0.005)
          • initial_state.object_position: x ∼ U (−0.3, 0), y ∼ U (−0.2, 0.2); resample until
            ∥(x, y)∥2 > 0.17
          • initial_state.object_velocity = 03
          • initial_state.goal_position = [0.45, −0.05, −0.323]
          • initial_state.goal_velocity = 03
          • step_function:



                                                   29
Preprint




            – clips action to action-space bounds
            – applies action torques to joints
            – advances MuJoCo simulation by dt
            – updates observation vector from simulation state
            – computes reward components and total reward
            – checks for finite observation values
            – increments step count
            – returns (observation, reward, terminated=False, truncated=done_flag,
               info) with reward components in info
       • seeding: via reset(seed=. . . ) method only
       • info dict keys: “reward_dist”, “reward_ctrl”, “reward_near”
       • fingertip position: MuJoCo site “tips_arm”
       • object & goal positions: MuJoCo bodies “object” and “goal”
       • internal state: corresponds to MuJoCo simulation state
  <Theoretical Foundations>
       • MDP tuple: (S, A, P, R)
            – S: continuous state space R23 (23-dimensional real vector)
            – A: continuous action space R7 with elementwise bounds [−2, 2] (torques)
            – P : transition probability induced by MuJoCo physics with dt = 0.05 s
            – R: reward function as defined below
       • Reward function
            – Definition:
                     r(s, a) = − Pobject − Pgoal 2 − 0.1 ∥a∥22 − 0.5 Pfingertip − Pobject 2
               – Where:
                                                     3
                   * Pobject , Pgoal , Pfingertip ∈ R are positions in meters
                   * ∥·∥  2  is  the Euclidean   norm
                               7
                   * a ∈ R is the action torque vector in N ·m
           • Episode ending
               – Truncation after 100 steps or if any observation value is non-finite
               – No termination condition (i.e., terminated=False always)
           • Fingertip position
               – Computed via forward kinematics internally by MuJoCo
           • Symbol Table
               – a: Action torque vector; Unit N ·m; Range: each element in [−2, 2]
               – Pfingertip : Fingertip 3D position; Unit m; Range: real values, unbounded
               – Pobject : Object 3D position; Unit m; Range: real values, unbounded
               – Pgoal : Goal 3D position; Unit m; Value: fixed at [0.45, −0.05, −0.323]
               – r: Reward; Unit: unitless; Range: real values (sum of negative components)
               – dt: Simulation timestep; Unit s; Value: 0.05
               – step_count: Current timestep count; Unit: integer; Range: 0 to 100
           • Final Specification
               – Environment Name: Pusher-v4
               – Class Name: Environment
               – Public API
                   * __init__(self)
                      · Initializes the MuJoCo simulation environment with Pusher-v4 model



                                                30
Preprint




                   · Sets initial internal variables including step count
                   · Defines action and observation spaces as specified
                   · Sets fixed goal position
               * set_state(self, state: np.ndarray) -> None
                   · Input: state vector of shape (23, ) matching observation space
                   · Sets the internal MuJoCo simulation state to correspond to the given ob-
                     servation
                   · Resets step count to zero; assumes state is valid and episode not done
               * step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool,
                  dict]
                   · Input: action vector of shape (7, ) clipped to [−2, 2]
                   · Applies action torques to the simulation joints and advances by dt =
                     0.05 s
                   · Updates observation vector; computes reward components and total re-
                     ward
                   · Truncates if any observation value is non-finite or if step count ≥ 100
                   · Returns: observation (23, ) float64, reward float, terminated
                     False, truncated bool, info with keys “reward_dist”, “reward_ctrl”,
                     “reward_near”
           – Core Logic
               * Simulates a 7-DOF robotic arm pushing an object to a goal
               * State includes joint angles/velocities, fingertip, object, and goal positions
               * Actions are joint torques clipped to [−2, 2]
               * Physics advances by 0.05 s per step
               * Reward encourages moving object to goal, penalizes large actions, and en-
                  courages fingertip proximity to object
               * Episode truncates after 100 steps or on non-finite state
               * Fingertip and object positions come from MuJoCo sites/bodies
               * Seeding via reset(seed=. . . ) (not shown here)
           – Usage Scenarios & Examples
               * Scenario 1: Initial step with zero action
                   · Observation: initial state vector with zero joint positions, small velocity
                     noise, specified object and goal
                   · Action: np.zeros(7, dtype=np.float32)
                   · Reward: negative sum of distances (control penalty = 0)
                   · Terminated: False; Truncated: False
                   · Info: {"reward_dist": value, "reward_ctrl": 0.0, "reward_near":
                     value}
               * Scenario 2: Non-zero action moves fingertip closer
                   · Observation: updated state after physics step
                   · Action: np.array([1.0, -0.5, 0.0, 0.2, 0.0, -1.0, 0.5],
                     dtype=np.float32)
                   · Reward: computed per formula
                   · Terminated: False; Truncated: False (unless step count reached 100)
                   · Info: {"reward_dist": value, "reward_ctrl": negative squared norm
                     of action, "reward_near": value}
  <Assumptions & Risks>
       • Assumes MuJoCo physics engine is used as backend with version constraints.
       • Assumes internal MuJoCo state can be set and queried to implement set_state and
         step.
       • Fingertip position is assumed to be accessible via MuJoCo site “tips_arm”.
       • Reward weights are fixed as per v4; no user-configurable weights.



                                               31
Preprint




            • Episode termination is only by truncation; no natural termination.
            • Seeding is only via reset(seed=. . . ); no separate seed method.
            • Risks include dependency on MuJoCo simulation correctness and numerical stability.
            • No explicit handling of invalid actions beyond clipping.
            • No rendering or visualization included.
    <Library Usage>
            • Uses Python standard library and NumPy only.
            • NumPy used for array operations, clipping (np.clip), norm calculations
              (np.linalg.norm), and finite checks (np.isfinite).
            • No external dependencies beyond MuJoCo simulation backend (assumed).
            • All units are SI: torque in N·m, angles in radians, positions in meters, time in seconds.
            • No source code copied; specification based on official documentation and API stan-
              dards.
    </final>


I     C ASE STUDY

I.1     T EXT 2W ORLD

Task Describe.Prepare and deliver sandwiches to a set of children: assemble sandwiches in the
kitchen (optionally gluten-free), place them on a tray, move the tray to the child’s location, and
serve subject to allergy constraints. Gluten-allergic children must receive a gluten-free sandwich;
non-allergic children may receive any sandwich. Serving requires the sandwich on the tray and the
tray at the child’s location; making a sandwich switches it from “notexist” to “prepared.” The goal
is that all children become served.
Prev. SOTA.
 (define (domain child-snack)
   (:requirements :typing :negative-preconditions)
   (:types
     child
     bread-portion
     content-portion
     sandwich
     tray
     place
   )

      (:constants
        kitchen - place
      )

      (:predicates
        (at_kitchen_bread ?b - bread-portion)
        (at_kitchen_content ?c - content-portion)
        (at_kitchen_sandwich ?s - sandwich)
        (no_gluten_bread ?b - bread-portion)
        (no_gluten_content ?c - content-portion)
        (ontray ?s - sandwich ?t - tray)
        (no_gluten_sandwich ?s - sandwich)
        (allergic_gluten ?c - child)
        (not_allergic_gluten ?c - child)
        (served ?c - child)
        (waiting ?c - child ?p - place)
        (at ?t - tray ?p - place)


                                                    32
Preprint




       (notexist ?s - sandwich)
   )

   ;; Action: make_sandwich_no_gluten
   (:action make_sandwich_no_gluten
     :parameters (?s - sandwich ?b - bread-portion ?c - content-portion)
     :precondition (and
       (at_kitchen_bread ?b)
       (at_kitchen_content ?c)
       (no_gluten_bread ?b)
       (no_gluten_content ?c)
       (notexist ?s)
     )
     :effect (and
       (not (at_kitchen_bread ?b))
       (not (at_kitchen_content ?c))
       (notexist ?s)
       (not (notexist ?s))
       (at_kitchen_sandwich ?s)
       (no_gluten_sandwich ?s)
     )
   )

   ;; Action: make_sandwich
   (:action make_sandwich
     :parameters (?s - sandwich ?b - bread-portion ?c - content-portion)
     :precondition (and
       (at_kitchen_bread ?b)
       (at_kitchen_content ?c)
       (notexist ?s)
     )
     :effect (and
       (not (at_kitchen_bread ?b))
       (not (at_kitchen_content ?c))
       (notexist ?s)
       (not (notexist ?s))
       (at_kitchen_sandwich ?s)
       ;; no effect on gluten status, sandwich may or may not be gluten-free
     )
   )

   ;; Action: put_on_tray
   (:action put_on_tray
     :parameters (?s - sandwich ?t - tray)
     :precondition (and
       (at_kitchen_sandwich ?s)
       (at ?t kitchen)
     )
     :effect (and
       (not (at_kitchen_sandwich ?s))
       (ontray ?s ?t)
     )
   )

   ;; Action: serve_sandwich_no_gluten
   (:action serve_sandwich_no_gluten
     :parameters (?s - sandwich ?c - child ?t - tray ?p - place)
     :precondition (and
       (ontray ?s ?t)
       (no_gluten_sandwich ?s)
       (allergic_gluten ?c)
       (waiting ?c ?p)
       (at ?t ?p)
     )
     :effect (and


                                             33
Preprint




             (not (ontray ?s ?t))
             (served ?c)
             (not (waiting ?c ?p))
         )
     )

     ;; Action: serve_sandwich
     (:action serve_sandwich
       :parameters (?s - sandwich ?c - child ?t - tray ?p - place)
       :precondition (and
         (ontray ?s ?t)
         (not (no_gluten_sandwich ?s))
         (not_allergic_gluten ?c)
         (waiting ?c ?p)
         (at ?t ?p)
       )
       :effect (and
         (not (ontray ?s ?t))
         (served ?c)
         (not (waiting ?c ?p))
       )
     )

     ;; Action: move_tray
     (:action move_tray
       :parameters (?t - tray ?p1 - place ?p2 - place)
       :precondition (at ?t ?p1)
       :effect (and
         (not (at ?t ?p1))
         (at ?t ?p2)
       )
     )
 )

Agent2World.
 (define (domain child-snack)
   (:requirements :typing :negative-preconditions :strips)
   (:types
     child
     bread-portion
     content-portion
     sandwich
     tray
     place
   )
   (:constants
     kitchen - place
   )
   (:predicates
     (at_kitchen_bread ?b - bread-portion)
     (at_kitchen_content ?c - content-portion)
     (at_kitchen_sandwich ?s - sandwich)
     (no_gluten_bread ?b - bread-portion)
     (no_gluten_content ?c - content-portion)
     (ontray ?s - sandwich ?t - tray)
     (no_gluten_sandwich ?s - sandwich)
     (allergic_gluten ?c - child)
     (not_allergic_gluten ?c - child)
     (served ?c - child)
     (waiting ?c - child ?p - place)
     (at ?t - tray ?p - place)
     (notexist ?s - sandwich)
   )



                                               34
Preprint




   (:action make_sandwich_no_gluten
     :parameters (?s - sandwich ?b - bread-portion ?c - content-portion)
     :precondition (and
       (at_kitchen_bread ?b)
       (at_kitchen_content ?c)
       (no_gluten_bread ?b)
       (no_gluten_content ?c)
       (notexist ?s)
     )
     :effect (and
       (not (notexist ?s))
       (at_kitchen_sandwich ?s)
       (no_gluten_sandwich ?s)
       (not (at_kitchen_bread ?b))
       (not (at_kitchen_content ?c))
     )
   )

   (:action make_sandwich
     :parameters (?s - sandwich ?b - bread-portion ?c - content-portion)
     :precondition (and
       (at_kitchen_bread ?b)
       (at_kitchen_content ?c)
       (notexist ?s)
     )
     :effect (and
       (not (notexist ?s))
       (at_kitchen_sandwich ?s)
       (not (at_kitchen_bread ?b))
       (not (at_kitchen_content ?c))
     )
   )

   (:action put_on_tray
     :parameters (?s - sandwich ?t - tray)
     :precondition (and
       (at_kitchen_sandwich ?s)
       (at ?t kitchen)
     )
     :effect (and
       (ontray ?s ?t)
       (not (at_kitchen_sandwich ?s))
     )
   )

   (:action serve_sandwich_no_gluten
     :parameters (?s - sandwich ?c - child ?t - tray ?p - place)
     :precondition (and
       (ontray ?s ?t)
       (no_gluten_sandwich ?s)
       (allergic_gluten ?c)
       (waiting ?c ?p)
       (at ?t ?p)
     )
     :effect (and
       (served ?c)
       (not (ontray ?s ?t))
     )
   )

   (:action serve_sandwich
     :parameters (?s - sandwich ?c - child ?t - tray ?p - place)
     :precondition (and
       (ontray ?s ?t)


                                             35
Preprint




            (waiting ?c ?p)
            (not_allergic_gluten ?c)
            (at ?t ?p)
          )
          :effect (and
            (served ?c)
            (not (ontray ?s ?t))
          )
      )

      (:action move_tray
        :parameters (?t - tray ?p1 - place ?p2 - place)
        :precondition (at ?t ?p1)
        :effect (and
          (at ?t ?p2)
          (not (at ?t ?p1))
        )
      )
 )

Analysis. Compared to the baseline domain, our Child-Snack formulation introduces three task-
aligned modifications that improve state consistency, compositionality, and plan feasibility. (i)
Creation-valid effects. During sandwich construction we flip the existence status from “non-
existent” to “prepared,” and record gluten-free status when applicable, thereby avoiding contradic-
tory postconditions at creation time; this yields deterministic successor states and reduces backtrack-
ing caused by ill-defined truth values. (ii) Serve-focused effects. During serving we only transfer the
item off the tray and mark the child as served, leaving the waiting label untouched; this separation of
concerns prevents nonessential side-effects, preserves modular composability with downstream rou-
tines (e.g., queueing or follow-up allocation), and promotes goal-monotonic progress on the served
objective. (iii) Permissive-serving preconditions. For non-allergic children we do not exclude
gluten-free items, weakening preconditions to accept any admissible sandwich; this enlarges the
feasible search space and prevents avoidable dead-ends when only gluten-free inventory remains,
while safety for allergic children is still enforced via a dedicated gluten-free serving action. Collec-
tively, these choices align with the ground-truth specification, produce cleaner state transitions, and
yield empirically favorable search dynamics—smaller inconsistent-state frontiers and fewer spuri-
ous deletions—resulting in a more robust make→put-on-tray→move-tray→serve pipeline for the
objective of “serving each child an acceptable sandwich.”

I.2       CWMB

Task Describe. Control a 3D Ant (one free-body torso with four 2-DoF legs; nine bodies, eight
hinge joints) to move forward along the +x axis by applying torques to the eight joints at each
step. The action space is Box([−1, 1]8 ) (joint torques). Observations list positions then velocities
(27-D by default; 29-D if current x, y are included), and optionally +84 contact-force terms when
use_contact_forces=True or version < v4. The reward is r = rhealthy + rforward − ctrl_cost (and
−contact_cost if contact forces are used), where rforward ≈ ∆x/∆t is positive for motion in +x and
∆t = frame_skip × 0.01 = 0.05 by default. Episodes start from an upright, slightly noisy state,
truncate at 1000 steps, and (by default) terminate early if the agent becomes unhealthy (non-finite
state or torso z ∈
                 / [0.2, 1.0]).
Prev SOTA vs Agent2World.
 import numpy as np
 from typing import Optional, Tuple
 # [D-0] Toggle: False = Ours (physics-like integration), True = Baseline (simple
      ,→ kinematics + noise)
 BASELINE = False

 class Environment:
     def __init__(
         self,
         # ---- Common params ----


                                                  36
Preprint




           frame_skip: int = 5,
           max_episode_steps: int = 1000,
           healthy_reward: float = 1.0,
           terminate_when_unhealthy: bool = True,
           healthy_z_range: Tuple[float, float] = (0.2, 1.0),
           ctrl_cost_weight: float = 0.5,
           # ---- Ours-only params ----
           contact_cost_weight: float = 5e-4,
           contact_force_range: Tuple[float, float] = (-1.0, 1.0),
           exclude_current_positions_from_observation: bool = True,
           use_contact_forces: bool = False,
           reset_noise_scale_ours: float = 0.1,
           forward_reward_weight: float = 1.0,
           # ---- Baseline-only params ----
           reset_noise_scale_baseline: float = 0.01,
           seed: Optional[int] = None,
     ):
           # Core configuration
           self.frame_skip = frame_skip
           self.dt = 0.01 * frame_skip
           self.max_episode_steps = max_episode_steps
           self.healthy_reward = healthy_reward
           self.terminate_when_unhealthy = terminate_when_unhealthy
           self.healthy_z_range = healthy_z_range
           self.ctrl_cost_weight = ctrl_cost_weight
           self.forward_reward_weight = forward_reward_weight # [D-5] Only used by Ours.
           self.np_random = np.random.RandomState(seed)

         # [D-1] Observation schema differs:
         # Baseline: fixed 27 = 13 positions (z, quat4, joint8) + 14 velocities (flat
      ,→ vector).
         # Ours:       positions(15) + velocities(14) (+ optional torso_xy, contact forces),
         #             with option to exclude torso x,y from observation.
         self.exclude_current_positions_from_observation = (
             False if BASELINE else bool(exclude_current_positions_from_observation)
         )

           # [D-2] Contacts: Baseline has no contact forces/cost; Ours can include 84-dim
      ,→ contact forces + cost.
           self.use_contact_forces = False if BASELINE else bool(use_contact_forces)
           self.contact_cost_weight = 0.0 if BASELINE else float(contact_cost_weight)
           self.contact_force_range = contact_force_range

           self.step_count = 0

           if BASELINE:
               # Baseline state: flat (27,) observation vector
               self.obs_shape = (27,)
               self.state = np.zeros(self.obs_shape, dtype=np.float64)
               self.x_position = 0.0 # [D-4] Progress tracked separately (not in observation)
               self.y_position = 0.0
               self.reset_noise_scale = float(reset_noise_scale_baseline) # [D-4]
               self.contact_forces = None
               self.observation_dim = 27 # [D-1]
           else:
               # Ours state: split positions(15) / velocities(14)
               self.pos_dim = 15 # torso_pos(3), torso_quat(4), joint_angles(8)
               self.vel_dim = 14 # torso_lin_vel(3), torso_ang_vel(3), joint_vel(8)
               self.positions = np.zeros(self.pos_dim, dtype=np.float64)
               self.velocities = np.zeros(self.vel_dim, dtype=np.float64)
               self.reset_noise_scale = float(reset_noise_scale_ours) # [D-4]
               self.last_x_position = 0.0 # [D-4] (used when restoring state)
               self.contact_forces = (
                   np.zeros(84, dtype=np.float64) if self.use_contact_forces else None
               )


                                               37
Preprint




             # Compute observation length for Ours
             base_pos_len = self.pos_dim
             if self.exclude_current_positions_from_observation:
                 base_pos_len -= 2 # drop torso x,y
             self.obs_pos_len = base_pos_len
             self.obs_vel_len = self.vel_dim
             self.obs_contact_len = 84 if self.use_contact_forces else 0
             self.obs_torso_xy_len = 0 if self.exclude_current_positions_from_observation
      ,→ else 2
             self.observation_dim = (
                 self.obs_pos_len + self.obs_vel_len + self.obs_torso_xy_len +
      ,→ self.obs_contact_len
             )

           self.reset(seed)

     # ---------------- Helpers (shared) ----------------
     def _is_healthy(self, z_value: Optional[float] = None) -> bool:
         # [D-3] Health z-source differs:
         # Baseline: use state[0] (z) from flat observation.
         # Ours:       use positions[2] (torso z) from split state.
         if BASELINE:
             st = self.state
             if not np.all(np.isfinite(st)):
                 return False
             z = st[0] if z_value is None else z_value
             return self.healthy_z_range[0] <= z <= self.healthy_z_range[1]
         else:
             if not np.all(np.isfinite(self.positions)) or not
      ,→ np.all(np.isfinite(self.velocities)):
                 return False
             z = self.positions[2]
             return self.healthy_z_range[0] <= z <= self.healthy_z_range[1]

     def _get_observation(self) -> np.ndarray:
         # [D-1] Observation layout differs (see __init__ comment).
         if BASELINE:
             return self.state.copy()
         if self.exclude_current_positions_from_observation:
             pos_obs = self.positions[2:].copy() # exclude torso x,y
             torso_xy = np.array([], dtype=np.float64)
         else:
             pos_obs = self.positions.copy()
             torso_xy = self.positions[0:2].copy()
         vel_obs = self.velocities.copy()
         obs = np.concatenate((pos_obs, vel_obs))
         if not self.exclude_current_positions_from_observation:
             obs = np.concatenate((obs, torso_xy))
         if self.use_contact_forces:
             obs = np.concatenate((obs, self.contact_forces))
         return obs

     @staticmethod
     def _quat_multiply(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
         w1, x1, y1, z1 = q1
         w2, x2, y2, z2 = q2
         return np.array(
             [
                 w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                 w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                 w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                 w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
             ],
             dtype=np.float64,
         )


                                             38
Preprint




     # ---------------- Public API ----------------
     def set_state(self, state: np.ndarray) -> None:
         state = np.asarray(state, dtype=np.float64)
         if BASELINE:
             # [D-8] Baseline expects a flat 27-dim observation (pos13+vel14).
             if state.shape != (27,):
                 raise ValueError(f"set_state input must have shape (27,), got
      ,→ {state.shape}")
             if not np.all(np.isfinite(state)):
                 raise ValueError("set_state input contains non-finite values")
             self.state = state.copy()
             self.step_count = 0
             self.x_position = 0.0 # [D-4] progress variable is external to obs
             self.y_position = 0.0
         else:
             # [D-8] Ours expects the current obs layout length and reconstructs split
      ,→ state.
             expected_len = self.observation_dim
             if state.ndim != 1 or state.shape[0] != expected_len:
                 raise ValueError(f"State must be 1D array of length {expected_len}, got
      ,→ shape {state.shape}")
             pos_len = self.obs_pos_len
             vel_len = self.obs_vel_len
             pos_part = state[:pos_len]
             vel_part = state[pos_len : pos_len + vel_len]
             if self.exclude_current_positions_from_observation:
                 full_positions = np.zeros(self.pos_dim, dtype=np.float64)
                 full_positions[2:] = pos_part
                 full_positions[0] = 0.0
                 full_positions[1] = 0.0
             else:
                 full_positions = pos_part.copy()
             self.positions = full_positions
             self.velocities = vel_part.copy()
             self.step_count = 0
             self.last_x_position = self.positions[0] # [D-4]

     def reset(self, seed: Optional[int] = None) -> np.ndarray:
         if seed is not None:
             self.np_random.seed(seed)
         self.step_count = 0

         if BASELINE:
             # [D-2][D-4] Baseline init: 13 pos (z, quat, joints) + 14 vel; small noise.
             pos = np.zeros(13, dtype=np.float64)
             pos[0] = 0.75 # z
             pos[1:5] = np.array([1.0, 0.0, 0.0, 0.0]) # quaternion (w,x,y,z)
             noise_pos = self.np_random.uniform(-self.reset_noise_scale,
      ,→ self.reset_noise_scale, size=13)
             pos = pos + noise_pos
             vel = self.np_random.normal(0, self.reset_noise_scale, size=14)
             self.state = np.concatenate([pos, vel])
             self.x_position = 0.0 # [D-4] progress variable
             self.y_position = 0.0
         else:
             # Ours init: positions(15) / velocities(14) with larger noise and full torso
      ,→ pose.
             base_positions = np.zeros(15, dtype=np.float64)
             base_positions[2] = 0.75 # torso z
             base_positions[3] = 1.0 # quat.w
             noise_pos = self.np_random.uniform(-self.reset_noise_scale,
      ,→ self.reset_noise_scale, size=15)
             self.positions = base_positions + noise_pos



                                             39
Preprint




              self.velocities = self.np_random.normal(loc=0.0, scale=self.reset_noise_scale,
      ,→ size=14)
               self.last_x_position = self.positions[0] # [D-4]
               if self.use_contact_forces and self.contact_forces is not None:
                   self.contact_forces[:] = 0.0
           return self._get_observation()

     def step(self, action: np.ndarray):
         action = np.asarray(action, dtype=np.float64)
         if action.shape != (8,):
             raise ValueError(f"Action must be of shape (8,), got {action.shape}")

           # [D-6] Action bound handling differs:
           # Baseline: out-of-bounds raises; Ours: clip to [-1, 1].
           if BASELINE:
               if np.any(action < -1.0) or np.any(action > 1.0):
                   raise ValueError("Action values must be in [-1, 1] for Baseline")
           else:
               action = np.clip(action, -1.0, 1.0)

           # ---- Inline divergence (single function, two branches) ----
           if BASELINE:
               # Forward progress proxy from hip joints
               prev_x_pos = self.x_position # [D-4] external tracker (not in obs)
               forward_force = float(np.sum(action[[0, 2, 4, 6]]))
               self.x_position += forward_force * self.dt * 0.1 # arbitrary scale

             # Stochastic updates (no true physics)
             z = float(np.clip(self.state[0] + self.np_random.uniform(-0.01, 0.01), 0.0,
      ,→ 2.0))
             # [D-7] Orientation update: Baseline = add noise to quaternion then
      ,→ renormalize.
             orientation = self.state[1:5] + self.np_random.uniform(-0.01, 0.01, size=4)
             norm = float(np.linalg.norm(orientation))
             orientation = orientation / norm if norm > 0 else np.array([1.0, 0.0, 0.0,
      ,→ 0.0], dtype=np.float64)
             # Joint angles: integrate action + small noise; wrap to [-pi, pi]
             joint_angles = self.state[5:13] + action * self.dt +
      ,→ self.np_random.uniform(-0.005, 0.005, size=8)
             joint_angles = (joint_angles + np.pi) % (2 * np.pi) - np.pi
             # Velocities: torso (noise) + joints (\approx action + noise)
             torso_vel = self.np_random.normal(0, 0.01, size=6)
             # Velocities: torso (noise) + joints (\approx action + noise)
             velocities = np.concatenate([torso_vel, joint_vel])
             # Compose new flat state
             pos = np.empty(13, dtype=np.float64)
             pos[0] = z
             pos[1:5] = orientation
             pos[5:13] = joint_angles
             self.state = np.concatenate([pos, velocities])

             healthy = self._is_healthy(z_value=z) # [D-3]
             forward_delta = self.x_position - prev_x_pos
             contact_cost = 0.0 # [D-2] no contacts in Baseline
             weight = 1.0        # [D-5] forward reward weight fixed to 1.0
         else:
             # Physics-like integration
             old_x = float(self.positions[0]) # [D-4] directly from torso x in positions
             # Joint dynamics: dv = (u - damp*v)*dt; dq = v*dt
             joint_damping = 0.1
             joint_vel_prev = self.velocities[6:]
             joint_acc = action - joint_damping * joint_vel_prev # [D-1] acts on split
      ,→ state
             joint_vel_new = joint_vel_prev + self.dt * joint_acc
             joint_ang_new = self.positions[7:] + self.dt * joint_vel_new


                                               40
Preprint




             # Torso linear & angular velocity damping
             lin_damping = 0.1
             ang_damping = 0.1
             torso_lin_vel_new = self.velocities[0:3] * (1 - lin_damping * self.dt)
             torso_ang_vel_new = self.velocities[3:6] * (1 - ang_damping * self.dt)
             # Integrate torso position
             torso_pos_new = self.positions[0:3] + self.dt * torso_lin_vel_new
             # [D-7] Orientation update: Ours = quaternion integration from angular
      ,→ velocity.
             q = self.positions[3:7]
             omega = torso_ang_vel_new
             omega_quat = np.array([0.0, omega[0], omega[1], omega[2]], dtype=np.float64)
             q_dot = 0.5 * self._quat_multiply(omega_quat, q)
             q_new = q + self.dt * q_dot
             norm = float(np.linalg.norm(q_new))
             q_new = q_new / norm if norm > 0 else np.array([1.0, 0.0, 0.0, 0.0],
      ,→ dtype=np.float64)
             # Write back split state
             self.positions[0:3] = torso_pos_new
             self.positions[3:7] = q_new
             self.positions[7:] = joint_ang_new
             self.velocities[0:3] = torso_lin_vel_new
             self.velocities[3:6] = torso_ang_vel_new
             self.velocities[6:] = joint_vel_new
             # Contacts (optional)
             if self.use_contact_forces and self.contact_forces is not None:
                 self.contact_forces.fill(0.0) # [D-2]
             new_x = float(self.positions[0])
             healthy = self._is_healthy() # [D-3]
             forward_delta = new_x - old_x
             # Contact cost (if enabled)
             if self.use_contact_forces and self.contact_forces is not None:
                 clipped = np.clip(self.contact_forces, self.contact_force_range[0],
      ,→ self.contact_force_range[1])
                 contact_cost = self.contact_cost_weight *
      ,→ float(np.sum(np.square(clipped))) # [D-2]
             else:
                 contact_cost = 0.0
             weight = self.forward_reward_weight # [D-5]

         # ---- Shared reward & termination (single exit) ----
         forward_reward = weight * (forward_delta / self.dt) # [D-5]
         ctrl_cost = self.ctrl_cost_weight * float(np.sum(np.square(action)))
         reward = (self.healthy_reward if healthy else 0.0) + forward_reward - ctrl_cost -
      ,→ contact_cost

         self.step_count += 1
         done = (self.terminate_when_unhealthy and not healthy) or (self.step_count >=
      ,→ self.max_episode_steps)
         return self._get_observation(), reward, done

Analysis. On the Ant-v4 forward-locomotion task, AGENT 2W ORLD surpasses the Baseline with
higher success, smoother gait, and lower energy per meter under identical horizons and z-health
checks. (i) State & sensing. The Baseline exposes a flat 27-D observation, while we adopt a task-
aligned layout that separates positions/velocities and can hide global (x, y) by default ([D-1]). We
additionally support contact forces for foot–ground cues ([D-2]). Health uses torso z from split state
rather than the flat vector slot ([D-3]). State restoration matches each layout: the Baseline ingests a
27-D vector, whereas ours reconstructs split buffers from the current observation setting ([D-8]). (ii)
Dynamics & orientation. The Baseline updates orientation by quaternion noise plus renormaliza-
tion, and treats actions as noisy joint velocities; we integrate damped joint accelerations and update
attitude via q̇ = 21 ωq⊗q with renormalization ([D-7]). This physically consistent pipeline—enabled
by the split state design ([D-1])—low-passes high-frequency actuation, reduces roll/pitch jitter, and
yields more phase-coordinated gaits. (iii) Control semantics & reward. The Baseline hard-errors


                                                  41
Preprint




on out-of-range actions and uses a fixed forward-reward weight; forward progress is tracked by an
external x variable and reset noise is smaller. Ours clips actions to [−1, 1] ([D-6]), uses a tunable
forward-reward weight ([D-5]), measures progress directly from torso x in the state and employs a
different reset scale ([D-4]); an optional contact-cost term can be included when contact signals are
enabled ([D-2]). Together these choices stabilize training signals and improve sample efficiency.
Summary of diffs. [D-1] Observation schema: Baseline uses a flat 27-D vector; Ours uses split
positions+velocities with optional hidden (x, y) and optional contact forces; [D-2] Contacts: Base-
line has no contact forces/cost; Ours optionally exposes 84-D contact forces and a contact-cost term;
[D-3] Health source: Baseline takes z from the flat vector slot; Ours uses torso z from split posi-
tions; [D-4] Progress & reset: Baseline tracks forward x as an external variable and uses smaller
reset noise; Ours reads torso x from state and uses a different reset scale; [D-5] Forward-reward
weight: Baseline fixed to 1.0; Ours is tunable; [D-6] Action bounds: Baseline errors on out-of-range
actions; Ours clips to [−1, 1]; [D-7] Orientation update: Baseline adds noise then renormalizes
quaternion; Ours integrates q̇ = 12 ωq ⊗q then renormalizes; [D-8] State setting: Baseline ingests a
flat 27-D state; Ours reconstructs split buffers from the current observation layout.

I.3   B YTE S IZED 32

Task Description. We build a lightweight, text-interactive micro-simulation of pea growth in a small
garden. The world contains a Pea, a FlowerPot, a Jug, and a Sink; water is represented as scalar
levels in the Jug and FlowerPot and as an internal level in the Pea. The agent can look/examine,
take/put objects, switch the sink on/off, fill the jug from the sink (effective only when the sink is on),
and pour water from the jug into the flower pot. After each action, a tick advances processes: the
sink supplies water if on; the pot passively transfers its water to the pea; and the pea consumes water
and progresses from seed → sprout → young plant → mature → reproducing when sufficiently
hydrated for several consecutive ticks. Episodes start with an unplanted pea and an empty pot; the
goal is to plant the pea and water it repeatedly until it reaches the reproducing stage.
Prev SOTA vs Agent2World.
 import random

 # [D0] Toggle: False = Ours, True = Baseline
 BASELINE = False

 # ---------------- Core object model (minimal API) ----------------
 class GameObject:
     def __init__(self, name):
         self.name, self.parent, self.contains = name, None, []
         self.props = {"isContainer": False, "isMoveable": True}
     def get(self, k, d=None):
         return self.props.get(k, d)
     def add(self, obj):
         obj.removeSelf(); self.contains.append(obj);
         obj.parent = self
     def remove(self, obj):
         self.contains.remove(obj); obj.parent = None
     def removeSelf(self):
         if self.parent: self.parent.remove(self)
     def allContained(self):
         out = []
         for o in self.contains: out += [o] + o.allContained()
         return out
     def tick(self): pass

 class Container(GameObject):
     def __init__(self, name): super().__init__(name);
         self.props["isContainer"] = True
     def place(self, obj):
         if not obj.get("isMoveable"):
         return ("Can't move that object.", False)
         self.add(obj); return ("OK.", True)


                                                   42
Preprint




     def take(self, obj):
         if obj not in self.contains:
             return ("Object not here.", None, False)
         if not obj.get("isMoveable"):
             return ("Can't move that object.", None, False)
         obj.removeSelf(); return ("OK.", obj, True)

 class Device(Container):
     def __init__(self, name): super().__init__(name);
         self.props.update({"isDevice": True, "isOn": False})
     def turnOn(self):
         if self.props["isOn"]:
             return (f"{self.name} is already on.", False)
         self.props["isOn"] = True
         return (f"{self.name} turned on.", True)
     def turnOff(self):
         if not self.props["isOn"]:
             return (f"{self.name} is already off.", False)
         self.props["isOn"] = False
         return (f"{self.name} turned off.", True)

 class World(Container):
     def __init__(self): super().__init__("world")

 class Agent(Container):
     def __init__(self): super().__init__("entity")

 # ---------------- Task objects ----------------
 class Pea(GameObject):
     STAGES = ["seed","sprout","young plant","mature plant","reproducing"]
     MAX_WATER, CONSUME, NEED, TICKS = 100, 5, 30, 3
     def __init__(self):
         super().__init__("pea"); self.props["isMoveable"]=True
         self.stage, self.water, self.hydrated = 0, 0, 0
     @property
     def stage_name(self):
         return self.STAGES[self.stage]
     def addWater(self, n):
         self.water = min(self.water + n, self.MAX_WATER)
     def tick(self):
         # [D3] Growth rule: Baseline = simple (>=2 -> +stage, else -1 if >0); Ours =
      ,→ threshold + accumulation.
         if BASELINE:
             if self.stage < len(self.STAGES)-1:
                 if self.water >= 2: self.water -= 2; self.stage += 1
                 elif self.water > 0: self.water -= 1
             return
         self.water = max(self.water - self.CONSUME, 0)
         if self.water >= self.NEED:
             self.hydrated += 1
             if self.hydrated >= self.TICKS and self.stage < len(self.STAGES)-1:
                 self.stage += 1; self.hydrated = 0

 class FlowerPot(Container):
     MAX_WATER = 100
     def __init__(self):
         super().__init__("flower pot")
         self.water = 0
     def addWater(self, n):
         add = min(self.MAX_WATER - self.water, n);
         self.water += add; return add
     def consume(self, n):
         use = min(self.water, n); self.water -= use; return use
     def tick(self):



                                             43
Preprint




           # [D2] Passive transfer: Baseline = none; Ours = transfer pot.water to pea on each
      ,→ tick.
           if BASELINE: return
           pea = next((o for o in self.contains if isinstance(o, Pea)), None)
           if pea and self.water > 0:
               x = self.consume(min(self.water, Pea.MAX_WATER))
               pea.addWater(x)

 class Jug(Container):
     MAX_WATER = 100
     def __init__(self):
         super().__init__("jug")
         self.water = 0
     def fill(self, n):
         add = min(self.MAX_WATER - self.water, n)
         self.water += add
         return add
     def pour(self, n):
         out = min(self.water, n
         self.water -= out
         return out

 class Sink(Device):
     MAX_WATER = 1000
     def __init__(self): super().__init__("sink");
         self.water = self.MAX_WATER
     def tick(self):
         self.water = self.MAX_WATER if self.props["isOn"] else 0

 # ------- Minimal game scaffold (only actions we need) -----
 class TextGame:
     MAX_STEPS = 50
     def __init__(self, seed=0):
         random.seed(seed)
         self.world, self.agent = World(), Agent(); self.world.add(self.agent)
         self.pea, self.pot, self.jug, self.sink = Pea(), FlowerPot(), Jug(), Sink()
         # [D7] Movability: Baseline pins the sink as immovable (ours keeps defaults).
         if BASELINE: self.sink.props["isMoveable"] = False
         for o in (self.pot, self.jug, self.sink, self.pea):
             self.world.add(o)
         self.score = self.steps = 0
         self.over = self.won = False

     # API of interest (matching both variants); unchanged helpers omitted for brevity.
     def _obj(self, name):
         for o in [self.world] + self.world.allContained():
             if o.name == name: return o
         for o in self.agent.contains:
             if o.name == name: return o
         return None

     def calculateScore(self):
         # [D5] Reward: Baseline = stage*10; Ours = stage*20 + water bonus (<=20).
         if BASELINE:
             self.score = self.pea.stage*10
         else:
             self.score = self.pea.stage*20 + int(self.pea.water/Pea.MAX_WATER*20)
         if self.pea.stage_name == "reproducing":
             self.won = self.over = True
         if self.steps >= self.MAX_STEPS and not self.won:
             self.over = True

     # ---------- actions ----------
     def take(self, name):
         o = self._obj(name);


                                               44
Preprint




           if not o: return f"No {name}."
           if not o.get("isMoveable"): return f"Can't take {name}."
           if o.parent != self.world: return f"{name} not here."
           _, got, ok = self.world.take(o);
           if ok: self.agent.add(got);
           return "OK." if ok else "Fail."

     def put(self, obj, cont):
         o, c = self._obj(obj), self._obj(cont)
         if not o or o.parent != self.agent:
             return f"No {obj} in inventory."
         if not c or not c.get("isContainer"):
             return f"{cont} not a container."
         # [D6] Placement constraint: Ours restricts pea -> pot only; Baseline has no
      ,→ special rule.
         if (not BASELINE) and isinstance(o, Pea) and not isinstance(c, FlowerPot):
             return "Pea must go into flower pot."
         _, ok = c.place(o); return "OK." if ok else "Fail."

     def turn_on(self, dev):
         d = self._obj(dev);
         if not d or not d.get("isDevice"): return f"No device {dev}."
         msg,_ = d.turnOn(); return msg
     def turn_off(self, dev):
         d = self._obj(dev);
         if not d or not d.get("isDevice"): return f"No device {dev}."
         msg,_ = d.turnOff(); return msg

     def fill_from_sink(self):
         # [D1] Fill gating: Baseline ignores sink.on; Ours requires sink.on == True.
         if (not BASELINE) and (not self.sink.props["isOn"]): return "Sink is off."
         need = self.jug.MAX_WATER - self.jug.water
         if need <= 0: return "Jug already full."
         self.jug.fill(need) # treat sink as infinite when allowed
         return "Jug filled."

     def pour_to_pot(self):
         if self.jug.water <= 0: return "Jug empty."
         # [D8] Pour semantics: Baseline feeds pea directly; Ours fills pot; pea drinks via
      ,→ [D2].
         poured = self.jug.pour(10)
         if BASELINE and (self.pea in self.pot.contains):
             self.pea.addWater(3); return "Poured; pea absorbs water."
         added = self.pot.addWater(poured)
         if added < poured: self.jug.fill(poured - added)
         return "Poured into pot."

     # ---------- driver ----------
     def step(self, cmd):
         self.steps += 1
         # [D4] Update order: Baseline ticks BEFORE action; Ours ticks AFTER.
         if BASELINE:
             for o in [self.world] + self.world.allContained(): o.tick()

           parts = cmd.lower().strip().split()
           out = "Unknown."
           try:
                if parts[:1]==["take"]: out = self.take(" ".join(parts[1:]))
                elif parts[:1]==["put"] and "in" in parts:
                    i = parts.index("in");
                    out = self.put(" ".join(parts[1:i]), " ".join(parts[i+1:]))
                elif parts[:2]==["turn","on"]:
                    out = self.turn_on(" ".join(parts[2:]))
                elif parts[:2]==["turn","off"]:
                    out = self.turn_off(" ".join(parts[2:]))


                                               45
Preprint




               elif parts[:3]==["fill","jug","from"]:
                   out = self.fill_from_sink()
               elif parts[:4]==["pour","water","from","jug"] and "in" in parts:
                   out = self.pour_to_pot()
               # distractor (spec only)
               elif parts[:1]==["use"]: out = "Nothing happens."
           except Exception as e:
               out = f"Error: {e}"

           if not BASELINE:
               for o in [self.world] + self.world.allContained(): o.tick()
           old = self.score; self.calculateScore();
           reward = self.score - old
           return out, self.score, reward, self.over, self.won

Analysis. Under identical initialization and evaluation (capacity limits and preconditions enforced),
AGENT 2W ORLD outperforms a Baseline on the pea–growing (water-transfer) task, yielding higher
success, shorter trajectories, and fewer invalid actions.(i) Action space and dynamics. We expose
a precondition-aware interface and decouple water flow from uptake: fill is effective only when
the sink is on ([D1]); pour increases the pot’s water and the pea hydrates asynchronously via tick
([D2], [D8]). We advance environment dynamics after the action to preserve causal credit assign-
ment ([D4]). By contrast, the Baseline exposes fill irrespective of sink state, credits hydration at
pour time, and updates before acting.(ii) Physical consistency and constraints. We enforce finite
capacities with overflow returned to the jug and constrain placement so the pea can only be planted
in the flower pot ([D6]). These constraints prune degenerate branches without removing valid so-
lutions. The Baseline omits the planting constraint and hydrates synchronously, which increases
misleading transitions. (Regarding movability, the Baseline pins the sink as immovable while Ours
keeps defaults; this ablation affects search but not preconditions, [D7].)(iii) Growth model and
reward. Plant physiology follows thresholded, accumulated growth with per tick water consump-
tion ([D3]). Reward shaping combines stage progress with a bounded water bonus, and immediate
rewards are score deltas ([D5]). The Baseline uses a stage-only score without water shaping, weak-
ening the learning signal.
Summary of diffs: [D1] preconditioned fill; [D2] passive pot→pea transfer; [D3]
threshold+consumption growth; [D4] post-action ticking; [D5] shaped reward (stage+water); [D6]
pea→pot placement constraint; [D7] sink movability ablation; [D8] pour affects pot first (not the
pea).

J   DATA C ONTAMINATION A NALYSIS
To address the concern that the web-search-based Deep Researcher may accidentally retrieve or
copy target solutions from the internet, we perform a post-hoc contamination analysis over all its
retrieval logs on our benchmarks.

Setup. For each evaluation instance where the Deep Researcher is invoked at least once, we con-
struct a pair (G, L), where (i) G is the gold world model for that instance (PDDL or Python code,
depending on the benchmark), and (ii) L is the concatenation of all textual contents retrieved by the
Deep Researcher for that instance, including page bodies and snippets from all visited URLs.
We tokenize both G and L using simple whitespace tokenization and extract all contiguous 10-token
n-grams from each. For a given pair, we mark it as contaminated if there exists at least one shared
10-gram between G and L.
For code and PDDL, an exact 10-token overlap is a strong signal of near-copying of a specific
implementation rather than generic programming idioms. Our use of a relatively long 10-token
threshold follows common practice in contamination analyses for Llama 2 (Touvron et al., 2023).

Results.    Table 13 reports, for each benchmark, the instance count, contamination count.
Across all three benchmarks, we find no exact 10-gram overlaps between the Deep Researcher’s
retrieved contents and the corresponding gold world models. This suggests that the Deep Researcher


                                                 46
Preprint




                    benchmark                         #instances     #contamination
                    ByteSized32                             32              0
                    Code World Models Benchmark             18              0
                    Text2World                             101              0

Table 13: Contamination analysis between Deep Researcher retrieval logs and gold world models
using exact 10-token n-gram overlap.


is not directly copying target solutions from the web, and that the performance gains we observe are
unlikely to be due to egregious test-set leakage.

K    E FFICIENCY A NALYSIS
To assess the practical cost of our multi-agent pipeline, we measure both LLM token usage and wall-
clock time for all methods on the three benchmarks. As is shown in Table 14, Table 16, and Table 15,
for each method and stage, the total number of input/output tokens consumed by the backbone LLM
and the average time per instance.

Results. Our experiments show that the test time of AGENT 2W ORLDMulti is comparable to that of
other workflow-based methods. The core reason for this is that, in order to enable a fair comparison,
we use fewer turns in our approach compared to previous methods (e.g., GIF-MCTS uses 10 turns
while our method uses only 3 turns in the refinement stage). Furthermore, the adaptive agents are
able to apply early stopping during the testing process.
In terms of token consumption, the AGENT 2W ORLDMulti model developer consumes fewer to-
kens compared to other methods. However, it is important to highlight that the testing stage
in AGENT 2W ORLDMulti is proactive, i.e., at each turn, we generate targeted testing cases and
player agent trajectories, whereas other methods use static test cases. This proactive approach in
AGENT 2W ORLDMulti naturally results in higher token consumption during the testing phase. De-
spite this, we still maintain competitive efficiency relative to existing methods.

                                                                   Tokens
                Method                 Stage                                    Time (s)
                                                             Input     Output
                Text2WorldEC=3         Total                 7,812     3,914          65
                Direct Generation      Total                  431       700           14
                AGENT 2W ORLDSingle    Total                22,531     2,141          26
                                       Deep Researcher      20,563     1,316
                                       Model Developer      4,728      2,038
                AGENT 2W ORLDMulti                                                    63
                                       Simulation Tester    4,145       528
                                       Unit Tester          9,712      1,562

            Table 14: Token usage and time efficiency on the Text2World benchmark.


L    T RAINING DATASET C ONSTRUCTION
To train the Model Developer agent, we construct a diverse training dataset that reflects both sym-
bolic world-model specifications and real-world simulation tasks. The dataset is composed of three
main components, designed to cover various styles of world-model generation:
(i) PDDL-style Tasks: We sample 200 tasks from the dataset released by AgentGen (Hu et al.,
2025b), which generates symbolic PDDL specifications for world-model tasks. These tasks include
a variety of symbolic reasoning challenges, each accompanied by a gold world model.
(ii) MCP Server Data: We also curate 200 tasks based on publicly available Model Context Pro-
tocol (MCP) servers, which provide interactive tools and data interfaces that allow agents to engage
in complex reasoning and decision-making tasks.


                                                 47
Preprint




                                                               Tokens
                Method                 Stage                                 Time (s)
                                                           Input    Output
                WorldCoder             Total               23,147    9,315        232
                GIF-MCTS               Total               24,677   10,838        259
                Direct Generation      Total                1,901    1,787         59
                Best-of-N              Total               65,470   19,520         70
                Self-Consistency       Total               61,837   19,924         68
                AGENT 2W ORLDSingle    Total               35,153    1,954         71
                                       Deep Researcher     29,056   2,108
                                       Model Developer     12,104   6,578
                AGENT 2W ORLDMulti                                                236
                                       Simulation Tester   18,658    564
                                       Unit Tester         24,788   3,379

   Table 15: Token usage and time efficiency on the Code World Models Benchmark (CWMB).

                                                               Tokens
                Method                 Stage                                 Time (s)
                                                           Input    Output
                ByteSized321-shot      Total               32,069   19,928        291
                Direct Generation      Total                7,046   4,301          71
                AGENT 2W ORLDSingle    Total               31,131    5,142         82
                                       Deep Researcher     20,852    1,071
                                       Model Developer     16,351   12,309
                AGENT 2W ORLDMulti                                                260
                                       Simulation Tester   20,528     584
                                       Unit Tester         32,352   2,158

            Table 16: Token usage and time efficiency on the ByteSized32 benchmark.


(iii) Game-style and Mujoco-style Tasks: Additionally, we include 50 tasks from each of the
game-style and Mujoco-style domains, where the tasks involve dynamic simulations with continuous
action spaces. These tasks are designed to mimic real-world, high-dimensional environments in
which agents must navigate, plan, and interact with physical systems. The tasks are synthesized
using a method similar to AgentGen (Hu et al., 2025b).
For each of these datasets, we perform the following steps to build our training set:
(i) For each dataset, we generate 3 distinct world-model rollouts using the same
llama-3.1-8b-instruct model. These rollouts are generated by running the Model Developer
agent through each task, resulting in different candidate solutions for each problem. (ii) Reward
Filtering: We then evaluate these rollouts using the Testing-Team feedback mechanism, which in-
cludes unit tests, simulation performance, and control tasks. The rollouts are ranked based on their
reward scores, and we select the one with the highest reward as the final solution for the task.




                                                 48
