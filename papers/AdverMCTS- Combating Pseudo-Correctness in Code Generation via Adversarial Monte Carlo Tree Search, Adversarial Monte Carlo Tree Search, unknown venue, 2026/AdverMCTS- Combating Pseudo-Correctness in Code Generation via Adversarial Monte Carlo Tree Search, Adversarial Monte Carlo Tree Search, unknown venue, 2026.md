                                                 AdverMCTS: Combating Pseudo-Correctness in Code Generation via
                                                             Adversarial Monte Carlo Tree Search


                                                                      Qingyao Li 1 Weiwen Liu 1 Weinan Zhang 1 Yong Yu 1 Bo An 2


                                                                     Abstract                                          A.Standard Search (Static Filter)
                                                                                                                        Solver MCTS                 Solver MCTS
                                                                                                                                                                          B.AdverMCTS (Adversarial Filter)
                                                                                                                                                                        Solver MCTS               Attacker MCTS
                                                                                                                       (Thought/Reasoning)       (Thought/Reasoning)

                                              Recent advancements in Large Language Models
                                                                                                                                                                                       Code
arXiv:2604.10449v1 [cs.SE] 12 Apr 2026




                                              (LLMs) have successfully employed search-based                                                                                           Pool

                                              strategies to enhance code generation. However,                              Code           Code         Code
                                              existing methods typically rely on static, sparse                          Candidate      Candidate    Candidate
                                                                                                                                                                       Screen+                            Adversarial
                                                                                                                                                                       Rerank                               Tests
                                              public test cases for verification, leading to                      Select by                           Public Tests                                     Global
                                                                                                                 Public tests                          (Sparse)                                    Filtering Hub
                                              pseudo-correctness—where solutions overfit                                                                                                          (Accumulating)

                                              the visible public tests but fail to generalize to                                          Code        Explodes on                       Code          Robust
                                                                                                                                        Candidate     Hidden Tests                    Candidate     Correctness
                                              hidden test cases. We argue that optimizing                                       Pseudo-correctness survives

                                              against a fixed, weak environment inherently
                                              limits robustness. To address this, we propose                    Figure 1. Conceptual Comparison. (A) Standard Search relies
                                                                                                                on sparse public tests, creating a “leaky” filter prone to pseudo-
                                              A DVER MCTS, a novel adversarial Monte                            correctness. (B) A DVER MCTS employs an active Attacker to
                                              Carlo Tree Search framework that combats                          co-evolve a progressively stricter environment, exposing hidden
                                              pseudo-correctness by coupling code search with                   bugs and enforcing robust correctness.
                                              active vulnerability discovery. A DVER MCTS
                                              formulates generation as a minimax-style game                     dard programming tasks with remarkable proficiency (Chen,
                                              between a Solver agent, which synthesizes                         2021; Li et al., 2022; Wang et al., 2025). However, as the
                                              code candidates, and an Attacker agent, which                     focus shifts towards complex, competition-level problems
                                              evolves to generate targeted corner test cases that               that demand deep algorithmic reasoning, the paradigm is
                                              exploit logical divergences in the current code                   evolving from simple “System 1” token prediction to “Sys-
                                              pool. These discovered tests form a dynamic,                      tem 2” deliberation (Xiang et al., 2025; Li et al., 2025f),
                                              progressively hostile filter that penalizes fragile               often characterized as Test-Time Compute (TTC) scaling
                                              reasoning. Extensive experiments demonstrate                      (Brown et al., 2024; Snell et al., 2024). Central to this shift
                                              that A DVER MCTS significantly outperforms                        is the reliance on execution-based verification (Zhong et al.,
                                              state-of-the-art baselines, effectively reducing                  2024; Ni et al., 2023; Dong et al., 2025a), where the correct-
                                              false positive rates and forcing the model                        ness of a generated code is inferred from its behavior on a
                                              to generalize beyond the initial constraints.                     set of test cases. In this context, the interplay between code
                                              The resources of this work are available at                       synthesis and test validation has become a pivotal axis for
                                              https://anonymous.4open.science/r/AdverMCTS-                      advancing model performance.
                                              A255.
                                                                                                                To leverage this verification signal, recent research has in-
                                                                                                                troduced various search-guided frameworks that structure
                                                                                                                decoding as a navigation problem (Chen et al., 2024a; Gou
                                         1. Introduction                                                        et al., 2024; Lyu et al., 2025). Prominent approaches such
                                         The advent of Large Language Models (LLMs) has fun-                    as Tree of Thoughts (ToT) (Yao et al., 2023) and Language
                                         damentally transformed the landscape of automated code                 Agent Tree Search (LATS) (Zhou et al., 2023) integrate
                                         generation (Odeh et al., 2024; Jiang et al., 2024a; Yang et al.,       planning with Breadth First Search (Kurant et al., 2010) and
                                         2025b; Dong et al., 2025b), enabling systems to solve stan-            Monte Carlo Tree Search (MCTS) (Browne et al., 2012),
                                                                                                                using the LLM as both a policy and a value estimator. Simi-
                                            1
                                              Shanghai Jiao Tong University, Shanghai, China 2 Nanyang          larly, methods like PG-TD (Zhang et al., 2023) and CodeT
                                         Technological University, Singapore.          Correspondence           (Chen et al., 2022) utilize rollout execution on sample tests
                                         to: Qingyao Li <ly890306@sjtu.edu.cn>, Weinan Zhang
                                         <wnzhang@sjtu.edu.cn>, Bo An <boan@ntu.edu.sg>.                        to guide the generation trajectory. These search-based strate-
                                                                                                                gies have successfully pushed the boundaries of code gen-
                                         Preprint. April 14, 2026.                                              eration, achieving significant performance gains on bench-

                                                                                                            1
                                                          A DVER MCTS

marks by enabling lookahead and backtracking capabilities                VER MCTS is the first to unify code search with an active
that are absent in greedy decoding (Li et al., 2025b).                   adversarial test search at test time to tackle competition-
                                                                         level programming problems.
Despite these advancements, we argue that a key challenge
is still under-addressed: pseudo-correctness—generating                • We develop key mechanisms that make adversarial test-
solutions that overfit the public tests while failing on the un-         time search effective in practice, including a persistent at-
derlying logic required by the hidden test suite. Public tests           tacker tree, divergence-driven test synthesis, and a global
typically sample from simplified sanity checks, whereas                  test filter that turns discovered corner cases into reusable
hidden tests probe the long-tail of corner cases. Conse-                 hard constraints.
quently, static verification signals are frequently insufficient       • Extensive experiments demonstrate that A DVER MCTS
to expose hidden bugs, and even sophisticated search can                 significantly outperforms state-of-the-art baselines. No-
be misled into preferring fragile code, creating a survivor-             tably, our analysis reveals that the adversarial pressure
ship bias where many “surviving” candidates are merely                   effectively reduces the false positive rate of generated
overfitted solutions. We empirically verify this bottleneck              codes, validating the efficacy of “hostile” supervision in
in Appendix C.1, confirming that while search spaces often               test-sparse environments.
contain correct solutions, sparse public tests fail to identify
them. Thus, the bottleneck is not the Solver’s capacity to             2. Related Work
generate correct solutions, but the environment’s capacity
to discriminate them at inference time. This calls for a               Competition-level Code Generation Early LLMs for
mechanism that actively strengthens verification, rather than          code such as OpenAI Codex (Chen, 2021) achieved strong
merely expanding the candidate set.                                    results on standard benchmarks (Zhou et al., 2023), yet
                                                                       remained challenged by competition-level problems that
This paper presents a unique perspective on the problem:               require deeper algorithmic reasoning (Li et al., 2023a;
robust code generation should be viewed as an adversar-                Lozhkov et al., 2024; Hui et al., 2024; Paul et al., 2024).
ial game between a solver that proposes solutions and an               AlphaCode (Li et al., 2022) marked the first non-trivial
attacker that actively searches for failure-inducing tests. In-        breakthrough in competitive programming, reaching me-
tuitively, if the search procedure is only navigating within           dian competitor-level performance on Codeforces (Mirza-
a fixed, weak environment (the public tests), then it is opti-         yanov et al., 2020). Building on this, a growing line of work
mizing the wrong objective. What we need at test time is a             improves reliability via search-guided generation (Princis
mechanism that co-evolves solutions and constraints: as the            et al., 2025; Jiang et al., 2024b; Wang et al., 2024; Chen
solver improves, the environment should become more hos-               et al., 2024c; Gao et al., 2024; Li et al., 2025c;e). Represen-
tile, continuously surfacing new corner cases that invalidate          tative examples include PG-TD (Zhang et al., 2023), which
pseudo-correct codes. Figure 1 illustrates this paradigm               executes candidate programs on sample tests for lookahead
shift: while standard search is limited by static verification,        planning; CodeT (Chen et al., 2022), which generates addi-
our approach constructs a dynamic hostile environment to               tional tests to select solutions and notably improves pass@1
mitigate survivorship bias.                                            on HumanEval (Li & Murr, 2024); and LATS (Zhou et al.,
Building on this perspective, we propose A DVER MCTS,                  2023), which integrates MCTS into code generation with
an adversarial Monte Carlo tree search framework that                  the LLM as the policy. While these methods allocate compu-
addresses pseudo-correctness by coupling solution search               tation to sampling or single-agent search over code, our ap-
with vulnerability discovery. A DVER MCTS instantiates a               proach instead introduces an adversarial MCTS framework
minimax-style interaction between two agents: (i) a Solver             that couples a code-generating Solver with a test-generating
MCTS that searches over chain-of-thought trajectories and              Attacker, enabling targeted failure discovery and more ro-
continuously synthesizes executable candidate codes dur-               bust selection beyond prior single-agent search paradigms.
ing simulation, and (ii) an Attacker MCTS that conditions
on the evolving code pool and searches for discriminative              Test Time Computing Scaling Test-Time Computing
tests via divergence-driven test synthesis. A global test filter       (TTC) frames inference-time compute as a key lever for
adjudicates and accumulates valid corner cases into a dy-              improving model performance (Muennighoff et al., 2025;
namic test suite, which is then used as hard constraints for           Chen et al., 2024b; Zhang et al., 2025; Li et al., 2025a;
screening and final re-ranking codes—forcing the solver to             Zeng et al., 2025), enabling deeper “System 2” style rea-
generalize beyond the initial public tests. Our contributions          soning (Brown et al., 2024; Snell et al., 2024). This moti-
are summarized as follows:                                             vates search-structured decoding, where methods such as
                                                                       Tree of Thoughts (ToT) (Yao et al., 2023) and Reason-
• We propose A DVER MCTS, a dual-agent search frame-                   ing via Planning (RAP) (Hao et al., 2023) extend Chain-
  work that enhances code robustness through iterative ad-             of-Thought (Wei et al., 2022) with lookahead/backtrack-
  versarial interaction. To the best of our knowledge, A D -           ing, and RethinkMCTS (Li et al., 2025e) further repairs

                                                                   2
                                                          A DVER MCTS

erroneous nodes using fine-grained feedback. However,                  s and a child node s′ (reached by action a), the selection
these approaches largely verify against static signals (e.g.,          policy is defined as:
LATS or RethinkMCTS), similar in spirit to fixed-signal                                                                p          !
self-improvement such as Reflexion (Shinn et al., 2023),                  ∗                                               N (s)
                                                                         a = argmax Q(s, a) + cpuct · P (s, a)                      ,
and differ from adversarial training efforts like ATGen (Li                        a                                 1 + N (s, a)
et al., 2025d). A DVER MCTS instead introduces an active                                                                           (1)
adversary at test time: an Attacker that adaptively hardens            where Q(s, a) is the estimated value of the action, P (s, a)
the verification environment, forcing the Solver to general-           is the prior probability given by the LLM, N (s) is the visit
ize beyond the initial constraints.                                    count of the parent node, and cpuct is the exploration constant.
                                                                       This mechanism balances the exploitation of high-quality
3. A DVER MCTS                                                         reasoning paths with the exploration of uncertain branches.

3.1. Problem Formulation                                               Expansion. Once a leaf node sleaf is reached, the Solver
Given a natural language problem description P , robust                expands it by sampling k potential next-step thoughts
code generation aims to synthesize a program C that satis-             {τ (1) , . . . , τ (k) } from the LLM policy πθ (·|sleaf ). These
fies the underlying semantics of P . Correctness is evaluated          thoughts typically represent intermediate reasoning steps or
by executing C on a test suite T , which is split into a small         algorithm designs. Each new thought τ creates a new child
set of public tests Tpub and a larger hidden set Thidden . At          node appended to the current trajectory.
inference time, the solver observes only (P, Tpub ), where
Tpub provides limited verification and may fail to expose              Simulation and Code Synthesis. Standard MCTS typi-
corner cases. Consequently, passing Tpub does not guarantee            cally performs random rollouts to estimate value. In our
generalization to Thidden . Our goal is to learn a policy that,        context, however, we leverage the LLM’s completion ca-
using only (P, Tpub ), produces a solution C ∗ that maximizes          pability to perform a semantic simulation. For a newly
performance on Thidden .                                               expanded thought node snew , the Solver performs a rollout
                                                                       to generate a complete code candidate C. This design en-
3.2. Overview                                                          sures that valid code candidates are generated continuously
                                                                       throughout the search process, rather than only at the search
We propose A DVER MCTS, an adversarial MCTS frame-                     depth limit. Consequently, generated candidates are sub-
work to enhance code generation robustness. As illustrated             jected to immediate screening: only those that pass both the
in Figure 2, the framework operates as an iterative game               public tests Tpub and previous accumulated adversarial suite
between two agents: a Solver and an Attacker. The Solver               in the Global Test Filter Tglobal are deposited into the shared
aims to synthesize robust code that satisfies the problem              Code Pool to support the Attacker’s subsequent operations.
requirements, while the Attacker actively searches for “vul-
nerability” test cases that induce behavioral divergence in            Backpropagation with Hybrid Feedback. After simula-
the Solver’s generated code. The two agents interact through           tion, the generated code C is evaluated to compute a reward
a shared Code Pool and a dynamic Global Test Filter, itera-            R. The reward is a composite signal from two sources:
tively refining both the solution and test quality. The detailed
pseudocode is provided in Algorithm 1 in the Appendix E.               • Intrinsic Correctness (Rpub ): The pass rate on the visible
                                                                         public test cases Tpub .
3.3. Solver MCTS: Robust Code Generation                               • Extrinsic Interaction (Vpenalty ): A penalty signal fed
                                                                         back from the Global Test Filter (see Figure 2, blue arrow
The Solver aims to synthesize a robust program C given                   “Backpropagation(-V)”). If the generated code C is later
the problem description P . The search tree acts as a struc-             found to fail on the global adversarial tests Tglobal or the
tured reasoning space, where the root represents the initial             newly generated Tnew , a penalty −V is applied to the
state s0 = P , and each node st = {P, τ1 , . . . , τt } repre-           current node of the solver.
sents a partial solution consisting of a sequence of Chain-
of-Thought (CoT) steps. The Solver iteratively builds the              The final value estimate Q(s, a) of all nodes along the tra-
search tree through four phases: Selection, Expansion, Sim-            jectory is updated using the collected reward, penalizing
ulation, and Backpropagation.                                          reasoning paths that lead to fragile code and reinforcing
                                                                       those that survive the adversarial filtering.
Selection. In each iteration, the algorithm traverses the
                                                                       3.4. Attacker MCTS: Vulnerability Discovery
tree from the root to a leaf node by recursively selecting
the child node that maximizes the Upper Confidence Bound               Parallel to the Solver, the Attacker operates to expose defects
(UCB) (Silver et al., 2017). Formally, for a parent node               in the generated codes. Unlike standard test generation,

                                                                   3
                                                                                                A DVER MCTS

                                       Solver MCTS (Robust Code Generation)                                                  Attacker MCTS (Vulnerability Discovery)
                                                                     (Problem Description)                                                                      (Problem and Code Pool)
                                           Select/Expand                                                                      Select/Expand

                                                      Solver Thought Nodes                                                       CoT      Attacker Thought Nodes
                                           CoT                                       CoT                                                                                     CoT




                              CoT                     CoT           CoT                            CoT              CoT                        CoT              CoT                       CoT
  Backpropagation(-V)




                                                                                                                                                                                                   Backpropagation(+R)
                         Candidate                 Candidate    Candidate                       Candidate        New Test                 New Test          New Test                 New Test
                                         ...                                         ...         Code
                                                                                                                                 ...                                        ...
                          Code                      Code         Code                                            Case                     Case              Case                     Case



                                                                                           Interaction & Global Filtering Hub
                                                                                                                                                     New Test
                        Blue=Solver Flow;                                                           Global Test Filter
                        Red=Attacker Flow;
                        Grey=Environment/Filter.                              Filtering Pass                                                  Execution Engine
                        Iterative interaction                                     Through                                                                              Divergence Reward(+R)
                                                                                                                                              (Divergence Check)
                        boosts both models.                                  Reject if fails
                                                                             any                                                                                       High Reward for inducing
                                                                                                                                                                       divergence (finding bugs)

                                                                    Penalty Feedback(-V)


Figure 2. Overview of A DVER MCTS. A minimax interaction where the Solver (blue) generates code and the Attacker (red) synthesizes
adversarial tests. The Global Hub turns valid attacks into constraints. Feedback is dual: divergence rewards (+R) for the Attacker and
penalties (-V) for the Solver enforce robust generalization.

which blindly targets the problem description, our Attacker                                                     the probability of discovering a valid corner case.
employs a targeted adversarial strategy conditioned on the
                                                                                                                Since the code pool consists of public-test–passing candi-
evolving Code Pool.
                                                                                                                dates and no ground-truth output is available at test time, we
                                                                                                                reward inputs that expose pseudo-correctness by causing the
Persistent Search with an Evolving Code Pool. The
                                                                                                                candidates in the pool to produce diverging outputs. With
Attacker maintains a persistent search tree that grows incre-
                                                                                                                this principle, we propose to evaluate the Divergence Re-
mentally throughout the searching process. The root state
                                                                                                                ward Rdiv for each candidate. The reward is defined based
represents the problem context Stest = {P, Cpool }, where
                                                                                                                on the disagreement of outputs produced by the Code Pool:
Cpool is the dynamic set of currently accepted code that
have passed all public tests. Crucially, this tree is retained                                                              Rdiv (T ) = I [∃i, j : Oi (T ) ̸= Oj (T )] · wdiv ,                              (2)
across iterations. When Cpool reaches a certain capacity, the                                                   where Oi (T ) denotes the execution output of code Ci ∈
Attacker resumes search from the existing tree structure, al-                                                   Cpool on input T ; wdiv is to normalize this reward by the
lowing it to progressively refine its attack strategies against                                                 number of unique outputs. We select the most discriminative
an increasingly robust population of codes.                                                                     test case T ∗ = argmaxm Rdiv (T (m) ) from the batch.
Selection and Expansion. The selection phase mirrors                                                            While output divergence cannot detect the case where all
the Solver’s logic, using a UCB-based policy to navigate to                                                     candidates agree on the same wrong output, it is aligned with
the most promising attacker thought nodes σ. At the frontier,                                                   our test-time objective: distinguishing pseudo-correct code
the Attacker expands a new thought node σnew representing                                                       that already pass Tpub . In practice, disagreement provides
a specific testing strategy (e.g., “Check boundary condition                                                    a high-signal trigger for discovering latent logical gaps,
for N = 0” or “Test with large prime inputs”). This reason-                                                     and we further guard against invalid via the Arbiter-based
ing step guides the subsequent generation towards specific                                                      validity check.
vulnerability types rather than random fuzzing.
                                                                                                                Backpropagation. The reward Rdiv (T ∗ ) is backpropa-
Simulation: Divergence-driven Test Synthesis. Upon                                                              gated up the Attacker’s tree, reinforcing the reasoning strate-
reaching a new thought node σnew , the Attacker em-                                                             gies that lead to high-divergence scenarios.
ploys a Divergence-driven Multi-sample Test Synthesis
(DMTS) strategy to ensure high-quality test generation.                                                         3.5. Interaction and Global Filtering Hub
The LLM generates a batch of k candidate test inputs
                                                                                                                The interaction module acts as the central “arena” where the
{T (1) , . . . , T (k) } conditioned on the current code pool:
                                                                                                                Solver and Attacker continuously exchange feedback. This
{T (1) , . . . , T (k) } ∼ πadv (·|P, Cpool , σnew ).
                                                                                                                mechanism ensures that only valid, high-quality test cases
By explicitly conditioning on Cpool , the Attacker aims to                                                      are retained to penalize fragile code.
craft inputs that exploit the logical discrepancies observed
among the current code. Generating multiple candidates                                                          LLM-based Output Arbiter. When the Attacker gener-
reduces the variance of the generation process and increases                                                    ates a test case Tnew that induces output divergence among

                                                                                                            4
                                                           A DVER MCTS

the code candidates (i.e., ∃Ci , Cj : Oi (Tnew ) ̸= Oj (Tnew )),        4. Experiments
a ground truth label is required to determine which candi-
date is at fault. Since hidden tests are unavailable during             4.1. Experiment Settings
inference, we introduce an LLM-based Output Arbiter to                  Datasets. We evaluate A DVER MCTS on two challeng-
adjudicate the results. The Arbiter takes the problem de-               ing competition-level code generation benchmarks: APPS
scription P , the generated input Tnew , and the divergent              (Hendrycks et al., 2021) and TACO (Li et al., 2023b). The
outputs {Oi , Oj , . . . } as input. It analyzes the semantic           APPS dataset contains three levels of difficulties: Introduc-
logic of P to identify the correct expected output O∗ .                 tory, Interview, and Competition. And Easy, Medium, and
                                                                        Hard split for TACO. Followin prior work (Li et al., 2025e),
        O∗ , validity ← Arbiter(P, Tnew , {Oi , Oj }).       (3)
                                                                        we evaluate all the methods on the formal 100 problems per
                                                                        split. For each problem, we set the maximum number of
If the Arbiter deems the test input Tnew ambiguous or in-               |Tpub | = 5. Following prior work (Austin et al., 2021; Chen,
valid, the test is discarded. Otherwise, the pair (Tnew , O∗ )          2021; Dong et al., 2025a), we use the standard pass rate
is formalized as a new valid test case.                                 and pass@1 metrics evaluated on the hidden test suite to
                                                                        measure robust correctness.
Global Filtering and Feedback Loops. Successfully ad-
judicated tests are added to the Global Test Filter (Tglobal ), a       Baselines. We compare A DVER MCTS against state-of-
dynamic repository of “hard” corner cases found during the              the-art methods spanning three categories: (1) Direct Syn-
search.                                                                 thesis: Standard Zero-shot prompting and Best-of-N sam-
• Penalty Feedback (-V) for Solver: With the adjudicated                pling (with N = 16) to establish performance lower bounds.
  ground truth O∗ , the system identifies the specific candi-           (2) Search and Planning: Advanced search-based frame-
  dates Cfail that produced incorrect outputs. A penalty value          works including PG-TD (Zhang et al., 2023), Tree of
  −V is backpropagated to their corresponding thought                   Thoughts (ToT) (Yao et al., 2023), and LATS (Zhou et al.,
  nodes in the Solver’s MCTS tree. This signal discourages              2023), which utilize lookahead planning or self-reflection.
  the Solver from pursuing reasoning paths that led to these            (3) MCTS Variants: We also compare with MCTS-Thought
  fragile implementations.                                              (MCTS for reasoning search) and RethinkMCTS (Li et al.,
                                                                        2025e), a recent method focusing on repairing erroneous
• Filtering Mechanism: The Tglobal acts as a gatekeeper.
                                                                        nodes. Due to space constraints, detailed descriptions of
  In subsequent iterations, any new candidate generated by
                                                                        these baselines and their specific configurations are provided
  the Solver must pass all tests in Tglobal before entering the
                                                                        in Appendix B.
  Code Pool. This ensures that the Code Pool monotonically
  improves in robustness.
                                                                        Implementation Details. We employ the Qwen3-4B-
3.6. Inference: Robust Selection                                        Instruct-2507 and Qwen3-8B (non-instruct) (Yang et al.,
                                                                        2025a) as the main backbone LLM for both the Solver
After the search process, the Solver yields a diverse set of            and Attacker agents. We also experiment on DeepSeek-
candidate programs. To select the final submission C ∗ , we             V3.2 (Liu et al., 2025) in the scaling experiment. For the
employ a hierarchical Test-based Reranking strategy that                Solver, we implement a standard MCTS with a UCB ex-
prioritizes robustness against the accumulated adversarial              ploration constant cpuct = 4. For the Attacker, we set a
knowledge.                                                              moderate search budget of N = 2 rollouts per iteration, bal-
The code candidates are ranked by a two-stage criterion:                ancing computational efficiency with adversarial strength.
                                                                        The maximum interaction depth is set to 16 rollouts and
• Primary Sort (Public Integrity): Candidates are first                 penalty value V = 0.1. All experiments are conducted us-
  ranked by their pass rate on the public test suite Tpub . This        ing the vLLM library (Kwon, 2025) for efficient inference.
  step filters out solutions that fail to meet the basic problem
  requirements.                                                         4.2. Main Results
• Secondary Sort (Adversarial Robustness): For candi-
                                                                        Table 1 reports results on APPS and TACO with two back-
  dates with identical public test scores (which is common
                                                                        bones. Overall, A DVER MCTS achieves the best perfor-
  due to the scarcity of Tpub ), we further rank them by their
                                                                        mance across benchmarks and backbones, with especially
  pass rate on the generated adversarial tests in Tglobal .
                                                                        strong gains on APPS and on the TACO average. Comparing
This mechanism effectively resolves ties among “pseudo-                 baselines, we observe a clear granularity effect: token-level
correct” solutions that overfit the public tests, selecting the         lookahead (PG-TD) offers limited gains due to its myopic
candidate that survives the hostile environment constructed             horizon; code-level search (LATS) improves performance
by the Attacker.                                                        but struggles with the sparsity of the full program space;

                                                                    5
                                                                     A DVER MCTS

Table 1. Main Results. We report Pass Rate and Pass@1 accuracy using Qwen3-4B-Instruct/8B backbones under rollout 16. A DVER MCTS
consistently outperforms state-of-the-art search baselines, showing significant gains on the most challenging subsets.

                                                 APPS                                                                                  TACO
      Model                   Pass Rate (%)                     Pass@1 (%)                                  Pass Rate (%)                                      Pass@1 (%)
                     Intro.   Inter. Comp.    Avg.    Intro.   Inter. Comp.          Avg.           Easy    Medium Hard          Avg.                  Easy   Medium Hard          Avg.
 Qwen3-4B-Instruct
 Base                51.94    53.30   31.70   45.64     35      27      15         25.67           57.27      39.97      29.87   42.37                 33      20          10     21.00
 Base (16)           65.27    66.52   48.77   60.18     46      40      23         36.33           68.65      56.15      48.49   57.76                 37      24          12     24.33
 PG-TD               71.88    69.05   40.50   60.48     56      43      27         42.00           70.99      61.81      56.54   63.11                 50      35          20     35.00
 MCTS-Thought        75.56    74.37   58.10   69.34     57      44      29         43.44           82.13      68.10      65.83   72.02                 47      32          14     31.00
 RethinkMCTS         77.77    72.69   61.13   70.53     56      47      29         43.67           83.91      68.79      64.75   72.48                 52      31          18     33.67
 ToT                 65.63    66.46   46.83   59.64     46      43      33         40.67           77.47      64.43      56.98   66.29                 52      34          14     34.00
 LATS                71.88    68.58   53.25   64.57     50      39      27         38.67           75.46      63.94      58.34   65.91                 44      29          17     30.00
 A DVER MCTS         78.63    75.24   64.45   72.77     61      52      36         49.67           84.04      73.05      66.23   74.44                 55      37          22     38.00
 Qwen3-8B
 Base                42.97    40.21   25.95   36.38     21      17       7         15.00           45.06      29.08      24.97   33.04                 22      9           4      11.67
 Base (16)           50.18    46.75   38.87   45.27     26      21      15         20.67           51.13      35.19      34.97   40.43                 23      8           7      12.67
 PG-TD               56.08    53.81   32.67   47.52     30      29      14         24.33           63.59      46.11      44.09   44.09                 39      18          13     23.33
 MCTS-Thought        62.80    60.55   50.40   57.92     37      36      21         31.33           70.15      56.11      49.69   58.65                 36      21          8      21.67
 RethinkMCTS         66.68    62.16   52.18   60.34     37      35      23         31.67           76.35      60.82      48.89   62.02                 42      22          12     25.33
 ToT                 50.52    49.22   33.67   44.47     28      22      16         22.00           66.49      46.73      43.43   52.21                 39      21          13     24.33
 LATS                59.64    56.01   42.30   52.65     30      31      17         26.00           62.52      51.08      38.03   50.54                 32      21          7      20.00
 A DVER MCTS         66.96    63.15   53.27   61.13     44      40      24         36.00           76.99      60.84      52.95   63.94                 44      27          13     28.00

whereas thought-level search (MCTS-Thought) proves most                                                      APPS                                                TACO
                                                                                              80                              73.3                                                  50.0
effective by decomposing complex logic into manageable                                                                                            50
                                                                                                                                                                    38.0
                                                                                 Pass@1 (%)




                                                                                                                                     Pass@1 (%)
planning steps. Crucially, unlike these methods that pri-                                     60                                                  40
                                                                                                              49.7
marily allocate compute to expanding candidate volume,                                                                                            30 28.0
                                                                                              40 36.0
A DVER MCTS strategically directs budget toward adversar-
                                                                                                                                                  20
ial verification. This active purification mechanism filters                                  20
out pseudo-correct solutions, enabling a significantly higher                                 Qwen3          Qwen3        DeepSeek                Qwen3          Qwen3           DeepSeek
                                                                                               8B          4B-Instruct   V3.2 (671B)               8B          4B-Instruct      V3.2 (671B)
conversion of public-test pass rates into robust hidden-test                                       Base           Base (16)               MCTS-Thought                     AdverMCTS
correctness (Pass@1).
                                                                                  Figure 3. Scalability with Model Capabilities. We compare meth-
                                                                                  ods across backbones sorted by intrinsic capability. Despite pa-
4.3. Scaling with Backbone Capability                                             rameter discrepancies, A DVER MCTS consistently amplifies per-
                                                                                  formance, maintaining a significant lead across all model scales.
To verify the scalability and model-agnosticism of A D -
VER MCTS, we extended our evaluation to the state-of-the-                          lection; and (iii) GF-Hub, where we specifically disable
art frontier model, DeepSeek-V3.2 (671B) (Liu et al., 2025).                       pre-admission global screening before a candidate enters
As shown in Figure 3, we order the models on the x-axis by                         the code pool, while keeping the final test-based re-ranking
their baseline sampling performance to visualize the corre-                        unchanged.
lation between intrinsic model capability and method gain.
                                                                                  As shown in Figure 4, all modules contribute positively. Re-
The results reveal a strictly monotonic upward trend: A D -
                                                                                  moving AT-Tree yields the largest drop, since no adversarial
VER MCTS consistently outperforms both the strong sam-
                                                                                  tests are produced and the solver degenerates to verifica-
pling baseline (Base-16) and the search baseline (MCTS-
                                                                                  tion on public tests only, making pseudo-correct candidates
Thought) across all settings. Notably, the performance gain
                                                                                  much harder to eliminate. Disabling DMTS also consistently
remains robust even on the 671B frontier model, confirming
                                                                                  hurts performance, indicating that multi-sample synthesis is
that our adversarial mechanism is agnostic to the underlying
                                                                                  important to reduce variance and reliably surface divergence-
model capacity and effectively scales from smaller open
                                                                                  triggering inputs. Finally, turning off the GF-Hub screening
weights to massive state-of-the-art base models.
                                                                                  step further degrades results, especially on harder splits,
                                                                                  suggesting that early global screening helps prevent fragile
4.4. Ablation Study                                                               solutions from polluting the pool and weakening subsequent
We ablate three core components of A DVER MCTS, remov-                            adversarial refinement and selection.
ing exactly one module at a time while keeping all other set-
tings fixed: (i) AT-Tree, which removes the entire Attacker                        4.5. Extended Analysis
agent and adversarial testing, reverting to standard search
                                                                                   Cost-Performance Trade-off under Test-Time Compute
guided only by public tests; (ii) DMTS, which disables the
                                                                                   Scaling. We investigate the scaling efficiency of A D -
multi-sample test synthesis, relying on a single stochastic
                                                                                   VER MCTS by analyzing the Pareto frontier (Lotov & Mi-
sample for test generation instead of divergence-driven se-
                                                                                   ettinen, 2008) between solution correctness (Pass@1) and

                                                                             6
                                                                                                                                           A DVER MCTS

                                                                                                                         Ablations of AdverMCTS
                                                                                         APPS                                                                                                                                          TACO
                                        70
                                                               61.0
                                                                                                                                                                                    60                          55.0
                                        60      57.059.059.0                                                                                                                                      50.0
                                                                                                                                                                                                         53.0
                                                                                    51.052.0                                                                                        50     47.0
                                        50                                   47.0                                                      48.349.7
                     Final Pass@1 (%)




                                                                                                                                                       Final Pass@1 (%)
                                                                      44.0                                                      46.0
                                                                                                                         43.3                                                       40                                                                                                                     38.0
                                                                                                                                                                                                                              36.037.037.0
                                        40                                                                                                                                                                                                                                                      33.735.3
                                                                                                              35.036.0                                                                                                 32.0                                                              31.0
                                                                                                       32.0                                                                         30
                                        30                                                      29.0
                                                                                                                                                                                                                                                                                  22.0
                                        20                                                                                                                                          20                                                                                     16.0
                                                                                                                                                                                                                                                       14.015.0
                                        10                                                                                                                                          10

                                         0                                                                                                                                          0
                                                  Intro.                 Inter.                   Comp.                     Avg.                                                              Easy                      Medium                                    Hard                       Avg.
                                                                                                                    AdverMCTS with Different Modules Removed
                                                                                               w/o AT-Tree                      w/o DMTS                     w/o GF-Hub                                           AdverMCTS (Full)

Figure 4. Ablation study of A DVER MCTS on APPS and TACO. We report the final Pass@1 (%) under the same inference budget while
removing one component at a time.

computational cost (average token consumption). As shown                                                                                                   (APPS-Competition and TACO-Hard) and tracked two key
in Figure 5, across both APPS and TACO, A DVER MCTS                                                                                                        metrics over 16 rollouts: 1) The Cumulative Number of
consistently dominates the baseline frontier: for a simi-                                                                                                  Valid Adversarial Test Corner Cases (that induce divergence
lar token budget, it achieves higher Pass@1, indicating                                                                                                    among codes) discovered by the Attacker (Orange); and
that the extra compute is spent on more effective verifi-                                                                                                  2) The Hidden Pass Rate of the Solver’s code pool (Blue),
cation rather than producing more redundant samples. No-                                                                                                   which serves as a proxy for true semantic correctness.
tably, on both datasets, A DVER MCTS with a budget of
                                                                                                                                                           Figure 6 presents the dual-axis trajectories. We observe
N = 16 rollouts achieves superior accuracy compared to
                                                                                                                                                           a strong positive correlation between the accumulation of
the baseline with N = 32 rollouts, while consuming signifi-
                                                                                                                                                           adversarial constraints and the improvement of solution ro-
cantly fewer tokens. This observation creates a compelling
                                                                                                                                                           bustness. Initially (Rollout 0-3), the code pool is fragile,
counter-argument to the concern of overhead introduced by
                                                                                                                                                           passing a few hidden tests. As the Attacker actively iden-
the dual-agent architecture: the active “purification” of the
                                                                                                                                                           tifies valid corner cases (indicated by the steep rise in the
search space via adversarial counter-examples proves to be
                                                                                                                                                           orange curve), the filtering mechanism filters out pseudo-
more compute-efficient than brute-force scaling of reason-
                                                                                                                                                           correct codes. By Rollout 16, the accumulation of diverse
ing paths. By filtering out pseudo-correct solutions early,
                                                                                                                                                           test cases acts as a comprehensive logical boundary, guiding
A DVER MCTS achieves “smarter” test-time scaling rather
                                                                                                                                                           the Solver’s pass rate to converge at a significantly higher
than simply “harder” scaling.
                                                                                                                                                           level. This confirms that A DVER MCTS functions as a con-
                         APPS: Performance vs. Cost                                             TACO: Performance vs. Cost                                 structive adversarial process: adversarial test cases evolve
                                                                N = 32                 0.38                                               N = 32
              0.48
                                               N = 16                                                                                                      into strict constraints, effectively pruning fragile solutions
                                                    N = 32 N = 50                                                                       N = 50
                                                                                       0.36                                                                and forcing the Solver to generalize beyond the public tests.
              0.46                           N = 16                                             N=8          N = 16
Pass@1 Rate




              0.44
                                                                                       0.34               N = 16
                                                                                                                         N = 32                                AdverMCTS
                                                                                                                                                                 0.6
                                                                                                                                                                         Dynamics: APPS-Competition 0.5AdverMCTS Dynamics: TACO-Hard
                           N=8                                                                                                                                                           n=100 problems                                                                    n=100 problems
                                                                                                                                                        Avg Pool Hidden Pass Rate




                                                                                                                                                                                                                                             Avg Pool Hidden Pass Rate




                                                                                                                                                                                                                                          2.0
                                                                                                                                                                                                                                              Avg Corner Cases (Cum)




                                                                                                                                                                                                                                                                                                                        Avg Corner Cases (Cum)
                                                                                       0.32      N=8                                                                            0.5
              0.42
                                                                                                                                                                                                                                                                     0.4                                               0.4
                             N=8                                                               N=4                                                                                                                                        1.5
              0.40                                                                     0.30                                                                                     0.4                                                                                                                                    0.3
                         N=4                                                                                                                                                                                                                                         0.3
              0.38                                                                                                                                                              0.3                                                       1.0
                     N=4                                                               0.28 N = 4                                                                                                                                                                    0.2                                               0.2
                                                                                                                                                                                0.2
                                        100k     200k      300k       400k                        100k            200k     300k           400k                                                                                            0.5                                                                          0.1
                                         Avg. Tokens per Problem                                       Avg. Tokens per Problem                                                  0.1                                                                                  0.1
                                                      MCTS-Thought                              AdverMCTS (Ours)                                                                                                                          0.0                                                                          0.0
                                                                                                                                                                                0.0 0                    5             10            15                              0.0 0               5             10         15
                                                                                                                                                                                                    Rollout Index                                                                 Rollout Index
Figure 5. Cost-Performance Pareto Frontiers (upper left is better).                                                                                                                                   Avg Pool Hidden Pass                                                 Avg Corner Cases (Cum)
Comparison of Pass@1 accuracy against average token consump-
tion per problem. A DVER MCTS consistently achieves a superior                                                                                            Figure 6. Visualization of Adversarial Dynamics. We track the co-
Pareto frontier. The labels denote the rollout budget.                                                                                                    evolution process. The synchronous rise of cumulative corner cases
                                                                                                                                                          (Orange) and the Solver’s hidden pass rate (Blue) demonstrates
Co-evolution of Test and Code. To uncover the temporal                                                                                                    that accumulating adversarial constraints drives the Solver toward
mechanism behind A DVER MCTS, we visualize the itera-                                                                                                     robust solutions.
tive interaction between the Attacker and the Solver. We                                                                                                   Discriminative Power of Adversarial Test Generation.
selected 100 distinct problems from the hardest subsets                                                                                                    To show that the Attacker provides a meaningful supervision

                                                                                                                                                   7
                                                                                                   A DVER MCTS

signal (rather than stochastic noise), we evaluate how well                                                 Table 2. Ablation on Attacker Optimization. We analyze the
                                                                                                            impact of Solver Context and Search Strategy. The results validate
its generated adversarial tests discriminate Pseudo-Correct                                                 that both contextual targeting and iterative tree search are essential
solutions (pass Tpub but fail Thidden ) from True Correct ones                                              for finding meaningful vulnerabilities.
(pass all tests). Figure 7 visualizes the impact of the gen-
                                                                                                                                           APPS (Pass@1)                  TACO (Pass@1)
erated adversarial tests on these two groups. The results                                                    Method
                                                                                                                                  Intro.   Inter.   Comp.   Avg.   Easy    Med.   Hard    Avg.
highlight three key observations: (1) High Sensitivity: It
                                                                                                             AdverMCTS (Full)     61.0      52.0    36.0    49.7   55.0    37.0   22.0    38.0
achieves a Recall of 56.7% (165/291), exposing over half                                                     Information Cutoff
of the “silent bugs” missed by standard MCTS; (2) Con-                                                       w/o Solver Context   58.0      49.0    31.0    46.0   52.0    35.0   17.0    34.7
servative Behavior: It maintains a low False Positive Rate                                                   Search Strategy
                                                                                                             Best-of-N            58.0      48.0    31.0    45.7   53.0    31.0   18.0    34.0
of 16.1%, indicating the generated corner cases are largely                                                  Random-MCTS          57.0      47.0    27.0    43.7   47.0    34.0   16.0    32.3
valid; and (3) High Precision: The overall precision of
78.95% confirms that output divergence is a reliable proxy                                                  Output Judging Matters: LLM Arbiter vs. Majority
for semantic correctness without ground truth.                                                              Voting. In A DVER MCTS, accurately determining the ex-
                                                                                                            pected output for a generated test input is critical. Once a
                           Attacker Discriminative Analysis: Filtering Efficacy                             test input induces disagreement among codes in the pool,
                     450                                                                                    we must determine which output is correct to label the test
                              Survived (Retained)
                     400      Effective Filter (True Positive)                                              and update the global test filter. We compare two judging
                              Wrongful Penalty (False Positive)
                     350                                                                                    strategies: (i) Majority Voting, which selects the majority
                               Higher Recall         Attacker Precision
                                                                                  Lower FP
                                 is Better             Precision = TPTP+ FP
   Number of Codes




                     300                                  = 78.95%                is Better                 output among the current code pool, and (ii) our LLM Ar-
                                                                                Mis-killed: 44              biter, where the same backbone LLM adjudicates the correct
                     250                                                       FP Rate: 16.1%
                                Killed: 165                                                                 output by reading the problem specification and the candi-
                     200       Recall: 56.7%
                     150                                                                                    date outputs. As shown in Table 3, the Arbiter significantly
                                                                                 Survived: 230              outperforms Voting on both benchmarks. Crucially, on the
                     100

                      50
                                Survived: 126                                                               TACO dataset, we analyzed the validity of the test pairs
                                                                                                            generated by both methods. The Voting strategy resulted in
                       0
                            Pseudo-Correct Codes                              True Correct Codes            a low rate of valid test pairs, indicating that the majority of
                               (Hidden Bugs)                                       (Robust)
                                                                                                            solutions frequently converged on incorrect outputs. These
Figure 7. Attacker Discriminative Analysis. We evaluate filtering                                           results justify the design choice of using an LLM arbiter:
efficacy on Pseudo-Correct (pass public, fail hidden) versus True                                           it improves both the quality of adversarial labels and the
Correct codes. The green hatched area marks effective bug iden-
tification (True Positives), while the red area indicates wrongful                                          effectiveness of adversarial verification.
penalization (False Positives).
                                                                                                            Table 3. Comparing output-judging strategies for adversarial tests.
                                                                                                            The LLM arbiter yields higher downstream performance and sub-
                                                                                                            stantially higher labeled-test validity(measured against gold code).
Solver-Aware is Crucial for Effective Attacker. We in-
vestigate two critical design choices to see the impact of                                                   Oracle Strategy
                                                                                                                                      Signal Quality (TACO)         Performance (Pass@1)
solver awareness for the attacker: (1) Solver Context, by                                                                             Labeled-test validity (↑)    APPS Avg.      TACO Avg.
ablating the Attacker’s access to the code pool Cpool (“w/o                                                  Majority Voting                    37.88%                43.67          32.67
Solver Context”); and (2) Search Algorithm, we examine                                                       LLM Arbiter (Ours)                 79.88%                49.67          37.33

whether this solver-to-attacker signal can be effectively ex-
ploited by different search strategies, by replacing MCTS                                                   5. Conclusion
with lighter Best-of-N baseline and Random-MCTS base-
                                                                                                            In this paper, we presented A DVER MCTS, a novel frame-
line where the UCB-based selection in MCTS is replaced
                                                                                                            work that addresses pseudo-correctness in code generation
by random selection.
                                                                                                            by shifting the paradigm from static verification to adversar-
Table 2 yields two key insights. First, removing solver con-                                                ial purification. By coupling a Solver MCTS with an active
text significantly degrades performance. Without observing                                                  Attacker MCTS, A DVER MCTS constructs a progressively
Cpool , the Attacker generates generic test cases rather than                                               hostile environment that co-evolves with the solution can-
targeted counter-examples that exploit the Solver’s specific                                                didates. This minimax interaction allows the system to au-
logical gaps. Second, MCTS outperforms Best-of-N and                                                        tonomously discover corner cases and mitigate survivorship
Random-MCTS not simply by searching “harder”, but be-                                                       bias without human-annotated test oracles. Extensive experi-
cause its selection, value estimation, and backpropagation                                                  ments demonstrate that A DVER MCTS outperforms state-of-
can absorb solver-derived feedback. This allows the At-                                                     the-art search-based methods, validating the effectiveness
tacker to refine test reasoning progressively, whereas one-                                                 of adversarial test-time compute. We believe this work
shot sampling is limited to the immediate quality of samples                                                opens new avenues for enhancing LLM reasoning robust-
and cannot reliably leverage the feedback.                                                                  ness through autonomous, adversarial self-improvement.

                                                                                                        8
                                                        A DVER MCTS

Impact Statement                                                     Chen, Z., White, M., Mooney, R., Payani, A., Su, Y., and
                                                                       Sun, H. When is tree search useful for LLM planning? it
This paper presents a method for improving the robustness              depends on the discriminator. In Proceedings of the 62nd
and correctness of automated code generation systems. Our              Annual Meeting of the Association for Computational
work contributes to the reliability of AI-assisted program-            Linguistics (Volume 1: Long Papers), pp. 13659–13678,
ming, potentially reducing software bugs and development               2024c.
costs. However, as with any advanced code generation
technology, there is a potential risk of misuse for generat-         Dong, Y., Ding, J., Jiang, X., Li, G., Li, Z., and Jin, Z.
ing malicious software. We believe the benefits of robust              Codescore: Evaluating code generation by learning code
verification outweigh these risks, as our “Attacker” agent             execution. ACM Transactions on Software Engineering
focuses on logical correctness rather than security exploita-          and Methodology, 34(3):1–22, 2025a.
tion. There are no specific societal consequences that we
feel must be highlighted here.                                       Dong, Y., Jiang, X., Qian, J., Wang, T., Zhang, K., Jin, Z.,
                                                                       and Li, G. A survey on code generation with LLM-based
References                                                             agents. arXiv preprint arXiv:2508.00083, 2025b.

Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,              Gao, S., Gao, C., Gu, W., and Lyu, M. Search-based LLMs
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., et al.         for code optimization. arXiv preprint arXiv:2408.12159,
  Program synthesis with large language models. arXiv                  2024.
  preprint arXiv:2108.07732, 2021.
                                                                     Gou, Q., Dong, Y., Wu, Y., and Ke, Q. Rrgcode: Deep
Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V.,            hierarchical search-based code generation. Journal of
  Ré, C., and Mirhoseini, A. Large language monkeys:                 Systems and Software, 211:111982, 2024.
  Scaling inference compute with repeated sampling. arXiv
  preprint arXiv:2407.21787, 2024.                                   Han, Y., Zhang, L., Meng, D., Zhang, Z., Hu, X., and Weng,
                                                                       S. A value based parallel update mcts method for multi-
Browne, C. B., Powley, E., Whitehouse, D., Lucas, S. M.,               agent cooperative decision making of connected and auto-
  Cowling, P. I., Rohlfshagen, P., Tavener, S., Perez, D.,             mated vehicles. arXiv preprint arXiv:2409.13783, 2024.
  Samothrakis, S., and Colton, S. A survey of monte carlo
  tree search methods. IEEE Transactions on Computa-                 Hao, S., Gu, Y., Ma, H., Hong, J., Wang, Z., Wang, D., and
  tional Intelligence and AI in games, 4(1):1–43, 2012.                Hu, Z. Reasoning with language model is planning with
                                                                       world model. In Proceedings of the 2023 Conference on
Chaffin, A., Claveau, V., and Kijak, E. Ppl-mcts: Con-
                                                                       Empirical Methods in Natural Language Processing, pp.
  strained textual generation through discriminator-guided
                                                                       8154–8173, 2023.
  mcts decoding. In Proceedings of the 2022 Conference of
  the North American chapter of the Association for Com-             Hendrycks, D., Basart, S., Kadavath, S., Mazeika, M., Arora,
  putational Linguistics: Human Language Technologies,                 A., Guo, E., Burns, C., Puranik, S., He, H., Song, D., et al.
  pp. 2953–2967, 2022.                                                 Measuring coding challenge competence with apps. arXiv
Chen, B., Zhang, F., Nguyen, A., Zan, D., Lin, Z., Lou, J.-            preprint arXiv:2105.09938, 2021.
  G., and Chen, W. Codet: Code generation with generated
                                                                     Hui, B., Yang, J., Cui, Z., Yang, J., Liu, D., Zhang, L.,
  tests. arXiv preprint arXiv:2207.10397, 2022.
                                                                       Liu, T., Zhang, J., Yu, B., Lu, K., et al. Qwen2. 5-coder
Chen, J., Hu, X., Li, Z., Gao, C., Xia, X., and Lo, D. Code            technical report. arXiv preprint arXiv:2409.12186, 2024.
  search is all you need? Improving code suggestions with
  code search. In Proceedings of the IEEE/ACM 46th Inter-            Jiang, J., Wang, F., Shen, J., Kim, S., and Kim, S. A survey
  national Conference on Software Engineering, pp. 1–13,                on large language models for code generation. arXiv
  2024a.                                                                preprint arXiv:2406.00515, 2024a.

Chen, M. Evaluating large language models trained on code.           Jiang, X., Dong, Y., Wang, L., Fang, Z., Shang, Q., Li, G.,
  arXiv preprint arXiv:2107.03374, 2021.                                Jin, Z., and Jiao, W. Self-planning code generation with
                                                                        large language models. ACM Transactions on Software
Chen, Z., Wang, W., Cao, Y., Liu, Y., Gao, Z., Cui, E.,                 Engineering and Methodology, 33(7):1–30, 2024b.
  Zhu, J., Ye, S., Tian, H., Liu, Z., et al. Expanding per-
  formance boundaries of open-source multimodal models               Kurant, M., Markopoulou, A., and Thiran, P. On the bias
  with model, data, and test-time scaling. arXiv preprint              of BFS (breadth first search). In 2010 22nd International
  arXiv:2412.05271, 2024b.                                            Teletraffic Congress (LTC 22), pp. 1–8. IEEE, 2010.

                                                                 9
                                                         A DVER MCTS

Kwon, W. vLLM: An Efficient Inference Engine for Large                 Liu, A., Mei, A., Lin, B., Xue, B., Wang, B., Xu, B., Wu,
 Language Models. PhD thesis, University of California,                  B., Zhang, B., Lin, C., Dong, C., et al. Deepseek-v3.
 Berkeley, 2025.                                                         2: Pushing the frontier of open large language models.
                                                                         arXiv preprint arXiv:2512.02556, 2025.
Li, D. and Murr, L. Humaneval on latest GPT models–2024.
   arXiv preprint arXiv:2402.14852, 2024.                              Lotov, A. V. and Miettinen, K. Visualizing the pareto fron-
                                                                         tier. In Multiobjective Optimization: Interactive and
Li, D., Cao, S., Cao, C., Li, X., Tan, S., Keutzer, K., Xing,            Evolutionary Approaches, pp. 213–243. Springer, 2008.
  J., Gonzalez, J. E., and Stoica, I. S*: Test time scaling
  for code generation. arXiv preprint arXiv:2502.14382,                Lozhkov, A., Li, R., Allal, L. B., Cassano, F., Lamy-Poirier,
  2025a.                                                                 J., Tazi, N., Tang, A., Pykhtar, D., Liu, J., Wei, Y., et al.
                                                                         Starcoder 2 and the stack v2: The next generation. arXiv
Li, J., Le, H., Zhou, Y., Xiong, C., Savarese, S., and Sa-               preprint arXiv:2402.19173, 2024.
  hoo, D. Codetree: Agent-guided tree search for code
  generation with large language models. In Proceedings                Lyu, Z., Huang, J., Deng, Y., Hoi, S., and An, B. Let’s revise
  of the 2025 Conference of the Nations of the Americas                  step-by-step: A unified local search framework for code
  Chapter of the Association for Computational Linguistics:              generation with LLMs. arXiv preprint arXiv:2508.07434,
  Human Language Technologies (Volume 1: Long Papers),                   2025.
  pp. 3711–3726, 2025b.
                                                                       Mirzayanov, M., Pavlova, O., MAVRIN, P., Melnikov, R.,
Li, Q., Dai, X., Li, X., Zhang, W., Wang, Y., Tang, R., and             Plotnikov, A., Parfenov, V., and Stankevich, A. Code-
  Yu, Y. Codeprm: Execution feedback-enhanced process                   forces as an educational platform for learning program-
  reward model for code generation. In Findings of the                  ming in digitalization. Olympiads in Informatics, 14
  Association for Computational Linguistics: ACL 2025,                  (133-142):14, 2020.
  pp. 8169–8182, 2025c.
                                                                       Muennighoff, N., Yang, Z., Shi, W., Li, X. L., Fei-Fei,
Li, Q., Dai, X., Liu, W., Li, X., Wang, Y., Tang, R., Yu, Y.,           L., Hajishirzi, H., Zettlemoyer, L., Liang, P., Candès,
  and Zhang, W. Atgen: Adversarial reinforcement learning               E., and Hashimoto, T. B. s1: Simple test-time scaling.
  for test case generation. arXiv preprint arXiv:2510.14635,            In Proceedings of the 2025 Conference on Empirical
  2025d.                                                                Methods in Natural Language Processing, pp. 20286–
                                                                        20332, 2025.
Li, Q., Xia, W., Dai, X., Du, K., Liu, W., Wang, Y., Tang,
  R., Yu, Y., and Zhang, W. Rethinkmcts: Refining er-                  Ni, A., Iyer, S., Radev, D., Stoyanov, V., Yih, W.-t., Wang,
  roneous thoughts in monte carlo tree search for code                   S., and Lin, X. V. Lever: Learning to verify language-
  generation. In Proceedings of the 2025 Conference on                   to-code generation with execution. In International Con-
  Empirical Methods in Natural Language Processing, pp.                  ference on Machine Learning, pp. 26106–26128. PMLR,
  8103–8121, 2025e.                                                      2023.

Li, R., Allal, L. B., Zi, Y., Muennighoff, N., Kocetkov, D.,           Odeh, A., Odeh, N., and Mohammed, A. S. A comparative
  Mou, C., Marone, M., Akiki, C., Li, J., Chim, J., et al.               review of ai techniques for automated code generation
  Starcoder: may the source be with you! arXiv preprint                  in software development: advancements, challenges, and
  arXiv:2305.06161, 2023a.                                               future directions. TEM Journal, 13(1):726, 2024.

Li, R., Fu, J., Zhang, B.-W., Huang, T., Sun, Z., Lyu, C., Liu,        Paul, D. G., Zhu, H., and Bayley, I. Benchmarks and metrics
   G., Jin, Z., and Li, G. Taco: Topics in algorithmic code              for evaluations of code generation: A critical review. In
   generation dataset. arXiv preprint arXiv:2312.14852,                  2024 IEEE International Conference on Artificial Intelli-
   2023b.                                                                gence Testing (AITest), pp. 87–94. IEEE, 2024.

Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J.,           Princis, H., Sharma, A., and David, C. Treecoder: Sys-
  Leblond, R., Eccles, T., Keeling, J., Gimeno, F., Dal Lago,            tematic exploration and optimisation of decoding and
  A., et al. Competition-level code generation with alpha-               constraints for LLM code generation. arXiv preprint
  code. Science, 378(6624):1092–1097, 2022.                              arXiv:2511.22277, 2025.

Li, Z.-Z., Zhang, D., Zhang, M.-L., Zhang, J., Liu, Z., Yao,           Shao, T., Zhang, K., Cheng, K., and Zhang, H. A decision-
  Y., Xu, H., Zheng, J., Wang, P.-J., Chen, X., et al. From              making framework using mcts as a hierarchical task net-
  system 1 to system 2: A survey of reasoning large lan-                 work and deep learning connector. Science Progress, 108
  guage models. arXiv preprint arXiv:2502.17419, 2025f.                  (4):00368504251386308, 2025.

                                                                  10
                                                         A DVER MCTS

Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and              Yang, Z., Chen, S., Gao, C., Li, Z., Hu, X., Liu, K., and Xia,
  Yao, S. Reflexion: Language agents with verbal rein-                   X. An empirical study of retrieval-augmented code gener-
  forcement learning. Advances in Neural Information                     ation: Challenges and opportunities. ACM Transactions
  Processing Systems, 36:8634–8652, 2023.                                on Software Engineering and Methodology, 2025b.
Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L.,           Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y.,
  Van Den Driessche, G., Schrittwieser, J., Antonoglou, I.,              and Narasimhan, K. Tree of thoughts: Deliberate problem
   Panneershelvam, V., Lanctot, M., et al. Mastering the                 solving with large language models. Advances in Neural
   game of go with deep neural networks and tree search.                 Information Processing Systems, 36:11809–11822, 2023.
  Nature, 529(7587):484–489, 2016.
                                                                       Zeng, Z., Cheng, Q., Yin, Z., Zhou, Y., and Qiu, X. Revisit-
Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai,          ing the test-time scaling of o1-like models: Do they truly
   M., Guez, A., Lanctot, M., Sifre, L., Kumaran, D., Grae-              possess test-time scaling capabilities? arXiv preprint
   pel, T., et al. Mastering chess and shogi by self-play                arXiv:2502.12215, 2025.
  with a general reinforcement learning algorithm. arXiv
   preprint arXiv:1712.01815, 2017.                                    Zhang, Q., Lyu, F., Sun, Z., Wang, L., Zhang, W., Hua,
                                                                         W., Wu, H., Guo, Z., Wang, Y., Muennighoff, N., et al.
Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling LLM test-              A survey on test-time scaling in large language mod-
  time compute optimally can be more effective than scal-                els: What, how, where, and how well? arXiv preprint
  ing model parameters. arXiv preprint arXiv:2408.03314,                 arXiv:2503.24235, 2025.
  2024.
                                                                       Zhang, S., Chen, Z., Shen, Y., Ding, M., Tenenbaum, J. B.,
Wang, C., Zhang, J., Feng, Y., Li, T., Sun, W., Liu, Y., and             and Gan, C. Planning with large language models for
 Peng, X. Teaching code LLMs to use autocompletion                       code generation. arXiv preprint arXiv:2303.05510, 2023.
 tools in repository-level code generation. ACM Transac-
 tions on Software Engineering and Methodology, 34(7):                 Zhong, L., Wang, Z., and Shang, J. Ldb: A large language
 1–27, 2025.                                                             model debugger via verifying runtime execution step-by-
                                                                         step. arXiv preprint arXiv:2402.16906, 2024.
Wang, E., Cassano, F., Wu, C., Bai, Y., Song, W., Nath,
 V., Han, Z., Hendryx, S., Yue, S., and Zhang, H. Plan-                Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H.,
 ning in natural language improves LLM search for code                   and Wang, Y.-X. Language agent tree search unifies
 generation. arXiv preprint arXiv:2409.03733, 2024.                      reasoning acting and planning in language models. arXiv
                                                                         preprint arXiv:2310.04406, 2023.
Wang, X. Reward-centered rest-mcts: A robust decision-
 making framework for robotic manipulation in high un-
 certainty environments. arXiv preprint arXiv:2503.05226,
 2025.
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F.,
 Chi, E., Le, Q. V., Zhou, D., et al. Chain-of-thought
 prompting elicits reasoning in large language models.
 Advances in Neural Information Processing Systems, 35:
 24824–24837, 2022.
Wu, T., Chen, J., Lin, W., Zhan, J., Li, M., Kuang,
 K., and Wu, F. Personalized distractor generation via
 mcts-guided reasoning reconstruction. arXiv preprint
 arXiv:2508.11184, 2025.
Xiang, V., Snell, C., Gandhi, K., Albalak, A., Singh, A.,
  Blagden, C., Phung, D., Rafailov, R., Lile, N., Mahan, D.,
  et al. Towards system 2 reasoning in LLMs: Learning
  how to think with meta chain-of-thought. arXiv preprint
  arXiv:2501.04682, 2025.
Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
  Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical
  report. arXiv preprint arXiv:2505.09388, 2025a.

                                                                  11
                                                        A DVER MCTS

A. Introduction of Monte Carlo Tree Search
Monte Carlo Tree Search (MCTS) is a heuristic search algorithm that balances exploration and exploitation to navigate
complex decision spaces, achieving significant success in sequential decision-making tasks (Silver et al., 2016; Shao et al.,
2025; Han et al., 2024; Wang, 2025). MCTS iteratively builds a search tree where nodes represent states and edges represent
actions. The process generally consists of four phases: Selection (select a child node that maximize a tree policy), Expansion
(one or more child nodes are added to represent potential future states), Simulation (simulate until a terminal state and
get reward), and Backpropagation (the reward is propagated back up the tree to the root and update the values of all
traversed nodes). In the context of reasoning or generation tasks, MCTS allows the model to look ahead and evaluate partial
solutions (Chaffin et al., 2022; Wu et al., 2025), guiding the generation process toward higher-quality outcomes compared to
greedy decoding methods.

B. Details of Baselines
To evaluate the effectiveness of A DVER MCTS, we compare it against a comprehensive set of baselines ranging from direct
prompting to advanced tree-search methods. The specific implementation details for each baseline are as follows:

   • Direct Synthesis (Base & Best-of-N): The Base method employs standard zero-shot prompting to generate a single
     solution. Best-of-N scales this by sampling N = 16 independent candidates (T = 0.7) and selecting the best one based
     on public test cases, serving as a strong sampling-based baseline without lookahead search.
   • PG-TD (Zhang et al., 2023): This method effectively utilizes MCTS to perform lookahead search at the token level.
     It explores the probability space of initial tokens to identify promising prefixes, which are then deterministically
     completed into full code solutions, aiming to guide generation through high-likelihood token trajectories.
   • Tree of Thoughts (ToT) (Yao et al., 2023): We implement a structured, two-layer search tree adapted for code
     generation. The first layer expands natural language plans or algorithmic sketches, while the second layer generates
     multiple concrete code implementations for each plan. This hierarchical approach decouples high-level reasoning from
     low-level implementation details.
   • Language Agent Tree Search (LATS) (Zhou et al., 2023): LATS unifies reasoning and planning by searching directly
     in the code space with an integrated reflection mechanism. Upon encountering a failure during simulation, the agent
     generates verbal self-reflection based on the error feedback; this reflection is incorporated into the context to guide the
     value estimation and selection of subsequent nodes.
   • MCTS-Thought: This is a search baseline that performs MCTS over Chain-of-Thought (CoT) reasoning steps rather
     than raw code. In the simulation phase, it synthesizes full code based on the current thought trajectory; crucially,
     execution feedback from these generated codes (e.g., test results) is added to the context to inform the expansion of the
     next reasoning step in a multi-turn manner.
   • RethinkMCTS (Li et al., 2025e): Similar to MCTS-Thought, this method searches in the thought space but introduces
     a specific repair mechanism. Instead of simply discarding nodes that lead to incorrect code, it utilizes fine-grained
     execution feedback to explicitly ”rethink” and refine erroneous thought nodes, allowing the search to recover from
     early reasoning mistakes without restarting.

C. Additional Experiments
C.1. Empirical Validation of Pseudo-Correctness: Is the Solution Generated but Overlooked?
Motivation. A core premise of A DVER MCTS is that existing search methods (e.g., MCTS-Thought) suffer from pseudo-
correctness: they successfully generate correct solutions during the search process, but fail to identify them due to the
sparsity of public test cases (typically |Tpub | = 5.To validate this hypothesis, we conducted a controlled experiment to
decouple “generation capability” from “verification capability”.

Experimental Setup. We employed the MCTS-Thought baseline with the Qwen3-4B-Instruct model. Instead of changing
the search algorithm, we only varied the verification environment used during the selection and backpropagation phases. We
compared three settings:

                                                              12
                                                                                                A DVER MCTS

   • Original (5 Tests): Standard setting with 5 public tests.
   • Half Tests (50%): Using 50% of the hidden test suite as visible constraints.
   • Oracle (All Tests): Using the full hidden test suite (simulate perfect verification).

Results and Analysis. As shown in Figure 8, the performance of the exact same search algorithm improves dramatically
as the verification environment becomes stricter.

   • On APPS, increasing test coverage boosts Pass@1 from 43.44% to 55.33% (+11.89%).
   • On TACO, the gain is even more pronounced, jumping from 31.00% to 43.67% (+12.67%).

These results provide compelling evidence that pseudo-correctness is the primary bottleneck. The search space already
contains robust solutions (as evidenced by the high performance in the Oracle setting), but the standard sparse filter allows
fragile solutions to “survive” and crowd them out. This justifies the design of A DVER MCTS: since we cannot access the
Oracle tests in practice, we must actively generate adversarial tests to approximate this strict verification environment.

                                                                                Impact of Test Sparsity on MCTS Performance
                                                               70
                                                                    Verification Environment
                                                                           Original (5 Tests)
                                                                           Half Tests (~50%)
                                                               60          Oracle (All Tests)
                                                                                                 55.3
                                                                                     51.0
                                                               50

                                                                         43.4                                       43.4      43.7
                                         Pass@1 Accuracy (%)




                                                               40

                                                                                                             31.0
                                                               30


                                                               20


                                                               10


                                                                0
                                                                                    APPS                            TACO

Figure 8. Empirical Validation of Pseudo-Correctness. Comparison of MCTS-Thought performance under varying verification
environments (Original, Half-Hidden, Oracle). The significant performance gap between the standard setting (5 Tests) and the Oracle
setting confirms the prevalence of pseudo-correctness: robust solutions are successfully generated but are filtered out due to the sparsity of
public tests.

C.2. Hard Re-ranking Outperforms Soft Penalties.
We investigate the optimal integration of adversarial feedback by comparing Direct Penalization (continuous value subtrac-
tion) with our Test-based Re-ranking (discrete filtering). Table 4 demonstrates that re-ranking consistently yields superior
performance. This result indicates that adversarial tests are most effective when utilized as hard constraints rather than soft
regularizers. While direct penalization introduces noise due to arbitrary scaling (e.g., equating core logic failures with minor
edge cases), re-ranking aligns with the binary nature of unit testing, strictly filtering brittle solutions that fail to survive the
hostile environment.

C.3. Impact of Attacker Search Budget: More is Not Always Better.
A natural question is whether allocating more test-time compute to the Attacker (i.e., more rollouts) monotonically improves
the Solver by producing increasingly challenging adversarial tests. To study this, we vary the Attacker rollout limit from 1
to 4 while keeping other components fixed, and evaluate downstream Solver performance on APPS.
Figure 9 reveals a clear inverted-U behavior: increasing rollouts from 1 to 2 yields a substantial gain (e.g., Pass@1 on APPS-
Competition improves from 31% to 36%), indicating that a minimal search budget is necessary for MCTS to move beyond

                                                                                                        13
                                                                A DVER MCTS

Table 4. Signal Utilization Strategy. Comparison of using adversarial signals as a continuous penalty (Direct Penalty) versus a discrete
filter (Re-ranking). The Re-ranking strategy consistently outperforms direct penalization, suggesting that adversarial tests are most
effective when treated as hard constraints.

                                                           APPS (Pass@1)                         TACO (Pass@1)
                                      Method
                                                       Intro.   Inter.   Comp.              Easy    Medium     Hard
                                      Direct Penalty   57.0     45.0       36.0             49.0      32.0     17.0
                                      Re-ranking       61.0     52.0       36.0             55.0      37.0     20.0
                                      Improvement      +4.0     +7.0      +0.0              +6.0      +5.0     +3.0


               70Impact of Attacker Search Budget (Rollouts)                            Impact of Attacker Search Budget (Rollouts)
               65      APPS-Intro   APPS-Inter   APPS-Comp                             60          TACO-Easy        TACO-Medium   TACO-Hard
               60
                                                                                       50
               55
  Pass@1 (%)




                                                                          Pass@1 (%)
               50                                                                      40
               45
               40                                                                      30
               35
                                                                                       20
               30
                   1              2            3           4                                 1                 2              3          4
                          Number of Attacker Rollouts                                                  Number of Attacker Rollouts
                                (a) APPS                                                                           (b) TACO
Figure 9. Attacker rollout scaling. Varying the Attacker’s number of rollouts shows an inverted-U trend on both APPS and TACO:
moderate budgets improve Pass@1 across difficulty splits, while larger budgets can saturate or degrade performance.


trivial cases and discover discriminative corner tests. However, further increasing the budget brings diminishing returns
and can even hurt performance. We attribute this to a practical trade-off: a more aggressive search may over-optimize the
divergence objective and produce tests that are less reliable as supervision signals (e.g., brittle constraints or borderline-valid
corner cases), which can distort screening and re-ranking. Based on this observation, we use a moderate rollout budget
(N = 2) in A DVER MCTS as it provides a favorable balance between effectiveness and efficiency.

D. Prompts
In this section, we present the prompts used when an LLM acts as an agent to perform various operations.

D.1. Solver Expansion Prompt
We present the prompt we use to instruct the LLM to sample code generation thoughts based on previous thoughts and
possible previous code execution feedback.

               Prompt D.1: Solver Expansion Prompt

        SY S T E M:
        You are a code reasoning agent.
        Your task is to generate one plan step of reasoning for solving the programming
        problem.
        Strictly output ONLY the thought content without any prefix or formatting.
        Be concise but comprehensive (2-3 sentences maximum).
        US E R PR O M P T:
        [Problem]
        [Previous Thoughts]
        [Previous Code Implementation]



                                                                         14
                                                     A DVER MCTS



    [Previous Execution Results]
    Provide the next logical thought to solve the problem. If previous thoughts exist,
    build upon them to offer deeper insight.
    Ensure the reasoning leads to code that handles edge cases and prevents the current
    error from recurring.



D.2. Solver Code Generation Prompt
We present the prompt used to instruct the LLM to generate code based on previous thoughts.

     Prompt D.2: Solver Code Generation Prompt

    SY S T E M:
    You are a code generator.
    US E R PR O M P T:
    [Problem Description]
    [Previous Thoughts]
    Based on the above problem description and the reasoning process (thoughts), please
    generate the complete Python code to solve the problem.
    The solution should contain the complete program including all the imports.
    Generate the code ONLY. No other explanation or words attached!
    Please wrap the solution into ‘‘‘python ... ‘‘‘ format.



D.3. Attacker Expansion Prompt
We present the prompt we use to instruct the LLM to sample test generation thoughts based on previous thoughts and
possible previous test execution feedback on the code pool.

     Prompt D.3: Attacker Expansion Prompt

    SY S T E M:
    You are a test thought designer specializing in finding bugs through systematic
    testing approaches.
    Your task is to propose a distinct testing thought that could reveal bugs in code
    implementations.
    Output your strategy directly.
    Keep the thought concise (1-2 sentences) and actionable.
    US E R PR O M P T:
    [Problem Description]
    [Previous Thoughts]
    You should propose a MORE SPECIFIC sub-thought that refines the current approach.
    Previous Execution Feedback:
    [feedback context]
    Generate a distinct testing thought that could help find bugs or differences
    between code implementations.
    Focus on:
    1. Edge cases and boundary conditions
    2. Special input patterns
    3. Common algorithmic pitfalls for this type of problem
    4. Input formats that often cause subtle bugs
    DO NOT generate specific test inputs - only describe the STRATEGY/APPROACH.
    Your thought:



D.4. Attacker Test Input Generation Prompt
We present the prompt we use to instruct the LLM to generate test input following previous thoughts and based on current
codes in the code pool.

                                                          15
                                                    A DVER MCTS

     Prompt D.4: Attacker Test Input Generation Prompt

    SY S T E M:
    You are a helpful AI Assistant that provides well-reasoned and detailed
    responses. You first think about the reasoning process as an internal monologue
    and then provide the user with the answer. Respond in the following format:
    <think>...</think><answer>...</answer>. Think concisely in 2-3 sentences.
    US E R PR O M P T:
    [Problem Description]
    [Previous Thoughts]
    Current Code Implementations to Test:
    [codes]
    Based on the testing thought above, generate ONE specific test input that:
    1. Follows the thought approach
    2. Is valid according to the problem description
    3. Is likely to reveal differences between the code implementations OR expose bugs
    The codes have already passed the following public tests (use this context to find
    DIFFERENT corner cases):
    [public tests]
    Format your answer as a JSON object containing only the "input" key, enclosed in
    triple backticks ‘‘‘json ‘‘‘. For example:
    <answer>
    ‘‘‘json
    {"input": "[your generated test case input]"}
    ‘‘‘
    </answer>
    Important: Only provide the INPUT, not the expected output. We will execute the
    codes to compare their outputs.


D.5. Attacker Test Output Arbiter Prompt
We present the prompt we use to instruct the LLM to determine the correct output from the diverse outputs from the code
pool.

     Prompt D.5: Attacker Test Output Arbiter Prompt

    US E R PR O M P T:
    You are an expert programmer. Given a programming problem and test input, multiple
    code implementations produced different outputs. Determine which output is
    CORRECT.
    Problem Description:
    [Problem Description]
    Public Tests (Use as reference for correct behavior):
    [public tests]
    Test Input:
    [Test Input]
    Code Outputs:
    [Outputs]
    Instructions:
    1. Understand what the problem asks
    2. Trace through the logic with the given test input
    3. Determine the CORRECT output and which code(s) produced it
    Respond in the following format:
    <reasoning>
    Brief explanation (2-3 sentences max) of why this is the correct output.
    </reasoning>
    <correct output>
    The correct output value
    </correct output>
    <correct codes id>
    List of correct code indices, e.g., [1, 3] or [2]



                                                          16
                                                              A DVER MCTS



     </correct codes id>



E. Algorithm
We present the detailed procedure of A DVER MCTS in pseudocode in Algorithm 1.

Algorithm 1 The A DVER MCTS Inference-Time Search Procedure.
Require: P : Problem description; Tpub : Public tests; Ns iter : Iterations of Solver; Na iter : Iterations of Attacker.
 1: Output: Robust solution C ∗
 2: # Initialization
 3: Initialize Solver Tree S with root s0 = {P }
 4: Initialize Attacker Tree A with root σ0 = {P, ∅}
 5: Code Pool Cpool ← ∅, Global Test Filter Tglobal ← ∅
 6: for i ← 1 to Ns iter do
 7:    # Phase 1: Solver Tree (Code Generation)
 8:    sleaf ← SELECT(S)
 9:    snew ← EXPAND(sleaf )
10:    C ← GENERATE CODE(snew )
11:    rpub ← EVALUATE(C, Tpub )
12:    # Strict Admission
13:    if rpub = 1.0 and PASS ALL(C, Tglobal ) then
14:       Cpool ← Cpool ∪ {C}
15:       if |Cpool | > Kmax then
16:          Remove oldest/lowest-score code from Cpool
17:       end if
18:    end if
19:    # Phase 2: Attacker Tree (Vulnerability Discovery)
20:    if |Cpool | ≥ 2 then
21:       for i ← 1 to Na iter do
22:          σleaf ← SELECT(A)
23:          # Late-Binding: Thought + Code Pool → Concrete Test
24:          Tcandidates ← GEN TEST(σleaf , Cpool )
25:          t∗ ← arg maxt∈Tcandidates DIV SCORE(t, Cpool )
26:          d∗ ← DIV SCORE(t∗ , Cpool )
27:          if d∗ > θthresh then
28:             # Arbiter determines Ground Truth
29:             o∗ , Cf ail ← ARBITER(P, t∗ , OUTPUTS(Cpool , t∗ ))
30:             if o∗ is valid then
31:                Tglobal ← Tglobal ∪ {(t∗ , o∗ )}
32:                for all C ∈ Cf ail do
33:                   Apply Penalty −V to Solver nodes of C
34:                   Update Code Value Q(s) ← Q(s) − V
35:                end for
36:             end if
37:          end if
38:          EXPAND(σleaf )
39:          BACKPROP(A, d∗ )
40:       end for
41:    end if
42:    # Phase 3: Solver Update
43:    BACKPROP(S, rpub − AccumulatedPenalties)
44: end for
45: # Inference: Hierarchical Test-based Reranking
46: Final Candidates Cf inal ← GET ALL CODES(S)
47: return arg maxC∈Cf inal ⟨PASS(C, Tpub ), PASS(C, Tglobal )⟩




                                                                     17
