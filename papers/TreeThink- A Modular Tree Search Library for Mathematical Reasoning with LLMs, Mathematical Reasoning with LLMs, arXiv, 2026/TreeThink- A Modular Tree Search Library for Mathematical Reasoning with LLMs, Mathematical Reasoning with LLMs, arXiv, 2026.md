                                                          T REE T HINK: A Modular Tree Search Library for
                                                                 Mathematical Reasoning with LLMs
                                               Burak S. Akbudak1 , Zeynel A. Ulusan2, 5 , Can S. Erer1 , Gözde Gül Şahin2, 3, 4
                                                  1
                                                    Computer Engineering Department, Bogazici University, Istanbul, Turkey
                                                     2
                                                       Computer Engineering Department, Koç University, Istanbul, Turkey
                                             3
                                               Friedrich-Alexander-Universität Erlangen-Nürnberg, Intelligent Language Systems
                                                                      4
                                                                        KUIS AI Lab, Istanbul, Turkey
                                                                    5
                                                                      Codeway Studios, Istanbul, Turkey
                                                                      https://gglab-ku.github.io/

                                                             Abstract
                                            Tree search algorithms enable systematic ex-
arXiv:2607.11258v2 [cs.CL] 8 Sep 2026




                                            ploration of the proof space in neural theo-
                                            rem proving. Existing LLM tree search li-
                                            braries primarily target natural language rea-
                                            soning and do not provide native integration
                                            with formal verifiers, while theorem proving
                                            systems often rely on task-specific search im-
                                            plementations. We introduce T REE T HINK, an
                                            open-source Python library for modular, fully
                                            asynchronous tree search in neural theorem
                                            proving. It integrates established tree search
                                            methods with vLLM-based inference pipelines
                                            and diverse node evaluation techniques, rang-          Figure 1: NTP tree search process. 1. Select: search
                                            ing from lightweight heuristics to neural eval-        method selects a node using a search algorithm. 2. Ex-
                                            uators. We support Lean 4, Rocq, and Is-               pand: the policy LLM generates child nodes. 3. Evalu-
                                            abelle/HOL alongside natural language. It con-         ate: evaluator strategy scores the generated nodes. W
                                            nects directly to each language’s Read-Eval-           stands for the value assigned to a node. 4. Verify: exter-
                                            Print Loop (REPL) server for real-time veri-           nal systems verify the correctness of the proof. Main op-
                                            fication and proof state extraction. We evalu-         erations in individual sections are in red while batched
                                            ate T REE T HINK on miniF2F and MATH500,               processes are in blue.
                                            demonstrating cross-language formal proof
                                            search, natural language reasoning support,            combines these approaches by using LLMs to pro-
                                            and up to 8.0× wall-clock speedup from asyn-           pose proof steps while relying on the ITP as a strict
                                            chronous execution. Source code is released un-
                                                                                                   verification environment. However, NTP remains
                                            der the MIT license at https://github.com/
                                            GGLAB-KU/treethink, and the library is ac-             a highly difficult problem as the action space of
                                            cessible as a downloadable package at https:           valid mathematical tactics is vast. To guide models
                                            //pypi.org/project/treethink/.                         into successful trajectories, recent works integrate
                                                                                                   structured search algorithms into the inference pro-
                                        1   Introduction
                                                                                                   cess (Li et al., 2024). Fig. 1 illustrates a typical tree
                                        Mathematical reasoning remains a fundamental               search loop: the search algorithm selects which
                                        challenge for artificial intelligence, spanning both       partial proof to expand, an LLM proposes the next
                                        informal and formal paradigms (Wang et al.,                tactic, an evaluator scores nodes, and the proof
                                        2026). While large language models (LLMs) have             assistant checks validity. Developing novel proof
                                        achieved impressive performance in informal math-          search systems often requires researchers to reim-
                                        ematical reasoning, they remain susceptible to log-        plement standard execution and verification compo-
                                        ical hallucinations and non-monotonic errors (Anh          nents, resulting in substantial engineering overhead.
                                        et al., 2025). This has motivated an increasing in-        For instance, to show the effectiveness of their pro-
                                        terest in formal theorem proving, where interactive        posed proof level reward evaluator, Wang et al.,
                                        theorem provers (ITPs) such as Lean (de Moura and          2023a implement a tree search mechanism from the
                                        Ullrich, 2021), Rocq (The Coq Dev Team, 2024),             ground up, and Li et al., 2025 orchestrate a search
                                        and Isabelle (Nipkow et al., 2002) verify mathe-           system to evaluate the proposed process reward
                                        matical statements. Neural theorem proving (NTP)           models. General LLM tree search libraries such as

                                                                                               1
                    Search Methods     #Policy   #Evaluators   Language       Formal Verifier   Async.&Batched   Proof Cache   Graph Vis.
    FETCH           MCTS, BFS, Beam      1           1         NL                   ✗                 ✗              ✗             ✗
    LLM Reasoners   MCTS, BFS, Beam,     6           ~         NL                   ✗                 ✗              ✗            ✓
                    DFS, CoT, ToT
    LiTS            MCTS, BFS, Beam      5           ~         NL                   ✗                 ✗              ✗            ✓
    Ours            MCTS, BFS, Beam      2           8         Lean, Rocq,          ✓                 ✓              ✓            ✓
                                                               Isabelle, NL


Table 1: Comparison of the proposed framework with existing search libraries. NL stands for natural language.
#Policy: number of supported LLM providers. #Evaluators: number of node evaluation strategies. Formal Verifier:
integration capabilities with formal theorem provers. Proof Cache: presence of proof caching mechanisms. ~ symbol
means there exists no implementation that would work in NTP scenario out of the box, and users are required to
implement it.

LLM Reasoners (Hao et al., 2024), FETCH (Wang                            tion. In formal reasoning, existing tools typically
et al., 2025), and LiTS (Li and Tao, 2026) provide                       address individual parts of the pipeline: extract
reusable search abstractions, however users must                         proof state information (Yang et al., 2023), exe-
still implement formal proof verification, proof-                        cute proofs (Aniva et al., 2025), or support premise
state extraction, and domain-specific evaluators for                     retrieval (Gao et al., 2026). Furthermore, recent
NTP.                                                                     formal math theorem-proving systems (Xin et al.,
   To reduce duplication of effort and acceler-                          2025; Li et al., 2025; Xin et al., 2024; Wu et al.,
ate experimentation, we present T REE T HINK, a                          2025) are designed as task-specific prover pipelines
modular Python library for tree search in neu-                           rather than reusable, multi-language tree-search li-
ral theorem proving. T REE T HINK is designed                            braries. Thus, existing systems either provide a
around formal verifier interaction with natural lan-                     general-purpose LLM tree search without formal
guage support. Our contributions are threefold:                          verifier integration, or the provided infrastructure
T REE T HINK decouples search algorithms, LLM                            lacks reusable, multi-language, asynchronous tree-
policies, evaluators, and environment interaction                        search abstractions. T REE T HINK fills this gap
into reusable components; provides unified REPL                          by combining reusable tree-search components,
clients for Lean 4, Rocq, and Isabelle/HOL; and                          batched LLM inference, heterogeneous evaluators,
supports fully asynchronous and batched execution                        and unified REPL interaction across Lean, Rocq,
with vLLM for high throughput inference (Kwon                            and Isabelle/HOL. We compare our framework
et al., 2023). We evaluate the system on miniF2F                         with other general tree search systems in Table 1.
for formal mathematics (Zheng et al., 2021) and
MATH500 for natural language mathematical rea-                           3     T REE T HINK
soning (Lightman et al., 2024), showing support
                                                                         T REE T HINK is designed around three principles:
for both settings and up to 8.0× speedup over syn-
                                                                         component interchangeability, verifier-agnostic en-
chronous execution. Alongside the open source
                                                                         vironment interaction, and asynchronous execu-
code1 , we release the framework as a download-
                                                                         tion. Component interchangeability is achieved
able package in PyPI2 , and provide a demo video3 .
                                                                         by modularizing search methods §3.1, candidate-
2   Previous Systems                                                     generating policies §3.2, and step evaluators §3.3.
                                                                         Verifier-agnostic interaction is managed by environ-
Recent efforts in LLM-based reasoning increas-                           ment interactors §3.4, which standardize commu-
ingly treat tree search as a reusable infrastruc-                        nication with formal proof checkers and informal
ture by separating search logic from model in-                           verifiers. All components support asynchronous,
ference (Wang et al., 2025; Hao et al., 2024; Li                         batched execution. In addition, T REE T HINK incor-
and Tao, 2026). These systems provide useful                             porates several features to accelerate experimenta-
abstractions for natural-language reasoning, but                         tion §3.5. An overview is shown in Figure 2.
they do not natively integrate formal proof verifi-
cation, proof-state extraction, or multi-ITP execu-                      3.1     Search Algorithms
    1
      https://github.com/GGLAB-KU/treethink
                                                                         Search algorithms construct the proof tree by itera-
    2
      https://pypi.org/project/treethink/                                tively selecting and expanding nodes via a policy
    3
      https://youtu.be/vKFXxnjlk8M                                       model, guided by leaf value estimates from eval-

                                                                     2
                                                                        Batched Sampler


                                                                                                          REPL Client
                                                                                                    Environment Interaction

                                                                                  Evaluator
      YAML Configuration




                                    CLI & Parsing
                                                                                 Node scoring




                                                    Input pipeline
           System settings
                                                                                                         Search Method             REPL Runtime            REPL server
                                                                                                         Main orchestrator         REPL orchestrator   Formal proof verification
        Datasets Registry                                                           Policy
      Dataset related information
                                                                                Node generator
                                                                                                                     TreeThink      Proof Cache
                                                                                                                                   Checked proof set




                                                                                    vLLM
                                                                                Inference engine



                                                    Input pipeline                     Core components         Helper units      External system

Figure 2: Overview of the system. Our framework accepts search configuration as a YAML file and a dataset registry.
Then, we parse the given parameters and initiate search components. We embed the environment interaction logic
into helper classes for modularity. Dashed lines denote optional relationships as some features may require the
indicated connection under specific configurations (e.g., when the evaluator is selected as neural model).


uators. Each algorithm features an asynchronous                                                             children across all expansions form the next beam,
counterpart to enable concurrent selection, expan-                                                          i.e., parent nodes do not survive.
sion, and evaluation. We adapt four algorithms
with varying exploration behavior and computa-                                                             Traditional Monte Carlo Tree Search (MCTS)
tional cost that have demonstrated effectiveness in                                                        (Kocsis and Szepesvári, 2006) systematically ex-
recent NTP studies (Polu and Sutskever, 2020; Xin                                                          plores search spaces by balancing exploration and
et al., 2025; Wu et al., 2025; Shao et al., 2024).                                                         exploitation. Each iteration involves selection, ex-
                                                                                                           pansion, simulation, and backpropagation. During
Best-First Search (Pearl, 1984) aims to priori-                                                            selection, the tree is traversed using the Upper Con-
tize the most promising frontier nodes according                                                           fidence Bounds for Trees (UCT) formula:
to evaluator scores. It does so by maintaining a                                                                                    "          s           #
priority queue of leaf nodes that are eligible for                                                                ∗                               ln N (s)
expansion and expanding the most promising node                                                                  s = arg max Q(si ) + c
                                                                                                                       si ∈child(s)                N (si )
at each iteration:
                                                                                                           where Q(si ) is the mean value estimate of child si ,
                           s∗ = arg max V (s)
                                                    s∈F                                                    N denotes visit counts, and c controls exploration.
                                                                                                           The policy expands the state into new child nodes,
where F is the frontier of leaf nodes and V(s) is the                                                      from which n terminal rollouts are generated. An
previously assigned evaluator score. The algorithm                                                         evaluator scores these rollouts, assigning the mean
expands the selected node by generating candidate                                                          value V to the child node. Finally, values are back-
tactics and evaluates the generated states using the                                                       propagated up to the root via Q(s) ← N (s)·Q(s)+V   .
                                                                                                                                                     N (s)+1
specified evaluation strategy.
                                                                                                           Rollout-Free Value-Guided MCTS Traditional
Beam Search (Bisiani, 1987) focuses on prun-                                                               simulation is computationally expensive in NTP
ing low-quality branches early. The algorithm ex-                                                          as each node requires terminal rollouts. Therefore,
pands the proof tree level-by-level, keeping the                                                           we implement a rollout-free variant inspired by
top-k most promising states at each depth:                                                                 AlphaZero (Silver et al., 2017), replacing simula-
                                                                                                         tion with direct value evaluation. The algorithm
                                                                                                           selects an expandable node using the aforemen-
                        [
       Bd+1 = top-k        children(s)
                                                                 s∈Bd
                                                                                                           tioned UCT rule and generates candidate proof
                                                                                                           steps. T REE T HINK then directly evaluates these
where states are ranked by evaluator scores. At                                                            candidates to produce a value estimate, which is
each level, we expand all beam states in parallel,                                                         backpropagated to update ancestor nodes. Un-
generating multiple candidates per state. The top-k                                                        like AlphaZero, T REE T HINK utilizes generic UCT

                                                                                                     3
rather than PUCT with learned priors. This ac-                Evaluator                   Signal Type   REPL?   RM?

commodates arbitrary pluggable evaluators better              LogprobEvaluator            Continuous     ✗      ✗
                                                              NormLenEvaluator            Continuous     ✗      ✗
suiting the computational constraints of NTP.                 ProofLevelRewardEvaluator    Discrete      ✗      ✓
                                                              StateLevelRewardEvaluator    Discrete      ✗      ✓
                                                              JudgeEvaluator              Continuous     ✓      ✓
3.2   Policies                                                TournamentEvaluator         Continuous     ✓      ✓
                                                              RMaxTSEvaluator             Continuous     ✗      ✗
Policies enlarge the search tree by generating child          REPLEvaluator                 Binary       ✓      ✗
nodes from LLM outputs. T REE T HINK supports lo-
cal and remote inference via vLLM’s LLM and vllm           Table 2: Supported evaluators with their signal type,
serve interfaces respectively. We use AsyncLLM             REPL requirement, and neural reward model (RM) us-
for handling concurrent generation across search           age. Due to the modular design, all evaluators are suit-
                                                           able for both informal and formal math problem solving.
branches. When the policy is called, the model is
prompted with the current proof trajectory starting
from the root node to selected child node. Full            where L is node depth, α controls the strength of
model outputs are stored in each node, allowing            the length penalty, st and at are proof step and
heuristic evaluators such as LogprobEvaluator              applied tactic at time t respectively, and p(at |st )
to leverage it. Output text is parsed in two               the predicted probability of model generating the
modes: newline-delimited (default) and XML-tag-            next tactic at at state st . Normalizing by Lα en-
delimited. In newline-delimited mode, we give              ables more fine-grained control over the shape of
the newline token as the stop token to vLLM’s              the tree, e.g., increasing α would lead the tree into
sampling parameters. For XML mode, users spec-             deeper proof paths.
ify a tag such as <PROOF_STEP>; we set the corre-          ProofLevelRewardEvaluator scores a node by
sponding closing tag as the stop token and extract         evaluating the complete generated proof with a
the inner content to construct nodes. Using XML            discriminative reward model via vLLM pooling
tags allows LLMs to separate reasoning from proof          mode. The pooling operation can be either “clas-
steps independent of the selected search compo-            sify” for sequence reward models outputting a
nents. With this approach, models that produce             scalar value, or “token_classify” for process re-
more structured outputs can be natively integrated         ward models (PRM) producing a per-token score,
into our framework. Optionally, T REE T HINK dedu-         which can be reduced to a single scalar by taking
plicates child nodes by comparing their text before        the mean. The final score reflects how promising
adding them to the search tree. This eliminates            the partial proof is, judged in the context of the
redundant candidates, conserving the expansion             entire proof rather than a single step. Wang et al.,
budget and ensuring each expansion yields a dis-           2023a use this approach in a formal proof search
tinct exploration path.                                    setting with their DT-Solver system.
                                                           StateLevelRewardEvaluator is similar to the
3.3   Evaluators                                           proof-level variant but uses only the current node’s
Evaluators score generated nodes to determine the          text rather than the full proof, acting as a PRM. It
search algorithm’s expansion priorities (§3.1). We         judges the sensibility of an individual step indepen-
implement adaptable approaches established in the          dent of history. Zhang et al., 2024 uses a similar
literature. Asynchronous complements for heuris-           evaluator system in their self-training pipeline.
tic evaluators wrap synchronous implementations,           JudgeEvaluator utilizes a REPL to extract state
while neural reward systems leverage vLLM’s asyn-          information and a generative reward model (GRM)
chronous capabilities. Table 2 summarizes the sup-         that assigns quality scores to proof steps. The
ported evaluators detailed below:                          model is prompted with current goals, applied tac-
LogprobEvaluator scores nodes by cumulative                tic, and solved goals, and is asked to give a score
log-probability of the generated text within that          on a fixed scale (e.g. 0–20). Given score is then
individual node, favoring more likely reasoning            parsed, and normalized to [0, 1]. We can see this
steps. This technique is a fundamental approach            evaluator in action in STILL (Jiang et al., 2024)
used by GPT-f (Polu and Sutskever, 2020).                  framework, where authors use a GRM.
NormLenEvaluator pioneered by Xin et al., 2025,            TournamentEvaluator ranks candidate proof
applies a length-normalized scoring function,              steps using a single-elimination tournament. Af-
                     ΣL−1                                  ter extracting proof states via batched REPL calls,
                      t=0 log p(at |st )
           V (s) =                                         a separate LLM judge performs batched pairwise
                           Lα

                                                       4
comparisons. Candidates are scored based on their             submissions. Proof caching is especially important
elimination round, with the overall winner receiv-            in tree search with NTP as branches often produce
ing the total number of rounds. Normalizing these             duplicate terminal proof candidates.
scores to [0, 1] yields a continuous quality signal
                                                              Graph Interaction Graphviz-based (Ellson
reflecting tournament advancement. Mahdavi et al.,
                                                              et al., 2004) visualizations with auto-computed
2026 employ a similar pairwise strategy for proof-
                                                              statistics facilitate visual debugging of search
level selection.
                                                              components. Additionally, search states can
RMaxTSEvaluator designed by Xin et al., 2024,
                                                              be saved and reloaded to resume interrupted
assigns a novelty bonus to previously unseen proof
                                                              experiments.
states, which are tracked via SHA-256 hashing.
When extrinsic rewards from proof verification are            Configuration and Execution Dataset metadata
sparse, it gives the search a continuous incentive to         is stored in TOML (Preston-Werner and commu-
explore new parts of the proof space.                         nity, 2021) files to ensure reproducibility, while
REPLEvaluator returns binary type-check feed-                 experiments run via a unified command-line inter-
back by executing proof steps in a formal REPL. It            face that accepts all search configurations, making
is mainly intended for traditional MCTS rollouts              the framework well-suited for HPC systems (see
where binary signals suffice.                                 Appendices B and C).

3.4   Environment Interaction                                 4     Evaluation of the System
We implement a unified client interface for commu-            Our evaluation approach consists of three stages:
nicating with formal proof checkers’ REPL servers:            cross-language formal proof search §4.1 where we
i) Kimina Lean Server (Santos et al., 2025) for               illustrate our framework’s capability of interact-
Lean 4 by adapting its existing sync/async clients,           ing with different ITPs, comparison between asyn-
ii) isabelle-server (Nipkow et al., 2002) via isabelle-       chronous and synchronous runs §4.2 to observe
client (Koepke et al., 2022) for Isabelle, and iii)           the gained speedups, and informal proof search
rocq-ml-server from rocq-ml-toolbox (Stoskopf,                with fixed-budget §4.3 to showcase the effective-
2025) for Rocq. Both rocq-ml-server and isabelle-             ness of tree search. We demonstrate the system’s
server accept proof paths rather than raw strings.            modularity in Appendix D.1 by detailing the lines
Therefore, we provide proofs inside temporary files           of code required to switch languages. Addition-
that are cleaned up after use, incurring a negligi-           ally, Appendix D.2 outlines the smoke tests used to
ble I/O overhead. To batch the inputs and allow               validate approaches outside our main evaluation.
concurrency, we connect to servers via multiple                  Our aim with these experiments is to demon-
clients.                                                      strate our framework’s ability to act as a reusable
    T REE T HINK supports three modes of formal-              tree-search system rather than a SOTA theorem
language REPL interaction: (1) evaluator-driven               proving system. Unless otherwise stated, the de-
interactions, where evaluators query the REPL dur-            fault experimental configuration uses a search bud-
ing the search process (e.g., JudgeEvaluator); (2)            get of 512 expansions with 3 children per expan-
post-search verification, which validates completed           sion, a vLLM policy backend, a NormLenEvaluator
proof candidates after search termination; and (3)            formal evaluator, the miniF2F test and MATH500
online verification, which evaluates candidates at            as formal and informal datasets respectively, and
terminal nodes (e.g. those with triple ticks as their         a single NVIDIA A40 GPU. We provide a com-
text) during search to enable early stopping. All             prehensive list of experiment parameters in Ap-
verification methods support batched execution to             pendix E for reproducibility purposes.
balance accuracy against runtime overhead.
                                                              4.1    Cross-Language Formal Proof Search
3.5   Additional Features                                     We evaluate our system on formal reasoning using
Beyond core components, T REE T HINK includes                 the miniF2F dataset, which serves as an appropri-
features that improve search speed, enable visual             ate benchmark for cross-language evaluation, as
inspection, and simplify usage.                               it is available in all three formal languages that
                                                              TreeThink supports. We use DeepSeekProverV2-
Proof Caching An LRU cache keyed by SHA-                      7B (Ren et al., 2025) for Lean, Qwen2.5-Coder-
256 hash of proof text prevents duplicate REPL                14B-Instruct (Hui et al., 2024) for Isabelle, and

                                                          5
       Method     Lean (%) Isab. (%) Rocq (%)                  4.3    Informal Mathematical Reasoning
       pass@1        49.4      42.2       0.8                  To demonstrate our framework’s support for nat-
       BFTS          54.9      65.1       1.2
       RF-MCTS       57.4      61.8       2.0                  ural language mathematical reasoning, we use
                                                               MATH500, a subset of the MATH (Hendrycks
Table 3: Formal proof-search pass rates on miniF2F             et al., 2021) dataset. It contains challenging
dataset. RF-MCTS denotes our rollout-free value-               competition-level problems stated in natural lan-
guided MCTS variant. Tree-search methods use the               guage. We select LLama3-8B (Grattafiori et al.,
same expansion budget, child budget, policy backend,
                                                               2024) as our policy model. For the evaluator,
and evaluator.
                                                               we use JudgeEvaluator with the judge model as
                                                               RISE-Judge-Qwen2.5-7B (Yu et al., 2025).
Qwen3.5-9B (Qwen Team, 2026) for Rocq for our                     To compare the models’ answers with the ground
runs. Since model availability differs across formal           truth (GT), we prompt the model to provide the
languages, we select a strong publicly available               final answer inside \boxed{}. After extracting
model for each language, using prior work when                 the contents, we parse the text into expressions
available (Hu et al., 2025).                                   compatible with the symbolic mathematics library
   Table 3 shows tree search consistently improves             SymPy (Meurer et al., 2017) to verify equality be-
pass@1 rates across all three languages. RF-MCTS               tween GT and the proposed solution.
outperforms BFTS in Lean and Rocq, while the re-
verse holds for Isabelle, demonstrating the value                              Method     Pass (%)
of modular search methods. The overall perfor-                                 pass@1         23.0
mance in Rocq remains comparatively low, which                                 maj@12         34.8
                                                                               RF-MCTS        40.0
we attribute to the limited availability of Rocq-
specialized public models and prior benchmarks.
                                                               Table 5: Natural-language mathematical reasoning re-
                                                               sults on MATH500. RF-MCTS indicates rollout-free
4.2   Asynchronous Execution                                   value-guided MCTS with a judge-based evaluator.
We evaluate the asynchronous features by vary-                    We report pass rates for pass@1, majority vot-
ing the concurrency level, with pass rate and aver-            ing@12 (Wang et al., 2023b) and our tree search
age wall-clock time per question results presented             run on MATH500 at Table 5. We choose maj@12,
in Table 4. Across all runs, we maintain Isabelle              since RF-MCTS produces approximately 12 termi-
as the formal language, and Qwen2.5-Coder-14B-                 nated paths per problem on average. Among tested
Instruct as the policy model. We aim to demon-                 methods, RF-MCTS achieves the highest score,
strate how concurrency affects the average solu-               suggesting that TreeThink’s search abstraction can
tion time, rather than an improvement in accuracy.             also benefit natural language mathematical reason-
For demonstration purposes, we use a subset of                 ing. Moreover, this experiment demonstrates our
miniF2F with 32 random samples.                                framework’s capability to model natural language
                                                               reasoning without structural changes.
 Mode / Concur. Pass (n=32) Avg. Time / Q. Speedup
 Sync / 1              18.50          3.72m     x1.00          5     Conclusion
 Async / 2             17.75          2.42m     x1.53
 Async / 4             17.00          1.05m     x3.54          We present T REE T HINK, a modular, open-source
 Async / 8             17.75          0.74m     x5.02
 Async / 16            16.25          0.46m     x8.08          library for tree search in neural theorem proving.
                                                               By decoupling infrastructure into reusable search
Table 4: Effect of asynchronous execution and concur-          algorithms, evaluators, and a vLLM-backed policy
rency level. All settings use the same model, evaluator,       layer, it eliminates significant engineering over-
expansion and child budget. Avg. Time/Q. denotes av-           head. Its fully asynchronous architecture yields
erage wall-clock time per question. We run each Mode           substantial wall-clock speedups without accuracy
/ Concurrency experiment four times and report the av-
                                                               loss. Furthermore, a unified REPL client enables
erage pass rates and Avg. Time/Q.
                                                               identical search configurations across three ITPs.
   As shown in Table 4, asynchronous runs signifi-             We also test the support for natural language rea-
cantly reduces the wall-clock time at a small cost             soning, and achieve higher results compared to
of accuracy. Specifically, we achieve 8.0× speedup             single-pass inference. We believe that TreeThink’s
when concurrency level is set to 16.                           extensible design simplifies the integration of new

                                                           6
components, providing a practical foundation for             batched execution reduce the computational over-
future research in formal and informal reasoning.            head and environmental footprint typically associ-
                                                             ated with large-scale reasoning tasks.
Limitations
                                                             Acknowledgements
Evaluation strategy Our evaluation showcases
the framework’s capabilities; large-scale bench-             This work has been partially supported by the
marking across diverse datasets and model families           Scientific and Technological Research Council of
is left for future work.                                     Türkiye (TÜBİTAK) as part of the project “Au-
                                                             tomatic Learning of Procedural Language from
Inference provider support T REE T HINK cur-                 Natural Language Instructions for Intelligent As-
rently supports only vLLM-based inference (local             sistance” with the number 121C132. We also grate-
or vllm serve). Other backends are not yet inte-             fully acknowledge KUIS AI Lab for providing com-
grated, though the policy abstraction can accom-             putational support.
modate them via subclassing.

Tool-assisted reasoning T REE T HINK does not                References
yet support interleaving proof steps with external
                                                             Dang Hoang Anh, Vu Tran, and Le Minh Nguyen. 2025.
tool calls (e.g., symbolic computation). Incorpo-              Analyzing logical fallacies in large language models:
rating tool-use into the search loop is left as future         A study on hallucination in mathematical reasoning.
work.                                                          In New Frontiers in Artificial Intelligence, pages 179–
                                                               195, Singapore. Springer Nature Singapore.
Domain scope The library is currently tailored               Leni Aniva, Chuyue Sun, Brando Miranda, Clark
to mathematical theorem proving. Extending the                 Barrett, and Sanmi Koyejo. 2025. Pantograph:
framework to other reasoning domains such as code              A machine-to-machine interaction interface for ad-
generation, agentic task planning, or scientific dis-          vanced theorem proving, high level reasoning, and
                                                               data extraction in lean 4. In Tools and Algorithms
covery would require additional environment inter-
                                                               for the Construction and Analysis of Systems: 31st
actors and domain-specific evaluation strategies.              International Conference, TACAS 2025, Held as Part
                                                               of the International Joint Conferences on Theory and
Search visualization While the framework pro-                  Practice of Software, ETAPS 2025, Hamilton, ON,
vides Graphviz-based static visualizations of com-             Canada, May 3–8, 2025, Proceedings, Part I, page
pleted search trees, it does not support animated or           104–123, Berlin, Heidelberg. Springer-Verlag.
interactive exploration of the search process (e.g.,         R. Bisiani. 1987. Beam search. In S. C. Shapiro, editor,
step-by-step playback or live tree expansion in a               Encyclopedia of Artificial Intelligence, pages 56–58.
browser interface).                                             John Wiley and Sons.
                                                             Leonardo de Moura and Sebastian Ullrich. 2021. The
Component benchmarking T REE T HINK sup-                       lean 4 theorem prover and programming language.
ports multiple search methods and evaluators, but              In Automated Deduction - CADE 28 - 28th Interna-
our main experiments evaluate only representative              tional Conference on Automated Deduction, Virtual
configurations. A full factorial benchmark over                Event, July 12-15, 2021, Proceedings, volume 12699
                                                               of Lecture Notes in Computer Science, pages 625–
all search methods, evaluators, models, and proof
                                                               635. Springer.
assistants is computationally expensive and left for
future work.                                                 John Ellson, Emden R. Gansner, Eleftherios Koutsofios,
                                                               Stephen C. North, and Gordon Woodhull. 2004.
                                                               Graphviz and Dynagraph — Static and Dynamic
Broader Impact Statement                                       Graph Drawing Tools, pages 127–148. Springer
                                                               Berlin Heidelberg, Berlin, Heidelberg.
By allowing researchers to easily extend its capabil-
ities with new search methods, evaluators, policies,         Guoxiong Gao, Zeming Sun, Jiedong Jiang, Yutong
or formal languages, TreeThink lowers the engi-                Wang, Jingda Xu, Peihao Wu, Bryan Dai, and
                                                               Bin Dong. 2026. Leansearch v2: Global premise
neering barriers to automated formal reasoning re-             retrieval for lean 4 theorem proving. Preprint,
search. It provides mathematicians and researchers             arXiv:2605.13137.
in neural theorem proving with accessible, LLM-
                                                             Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
driven tools to explore complex proof spaces, aid-             Abhinav Pandey, Abhishek Kadian, Ahmad Al-
ing the advancement of mathematical understand-                Dahle, Aiesha Letman, Akhil Mathur, Alan Schel-
ing. Furthermore, the library’s asynchronous and               ten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh


                                                         7
  Goyal, Anthony Hartshorn, Aobo Yang, Archi Mi-              Zhaoyu Li, Jialiang Sun, Logan Murphy, Qidong Su,
  tra, Archie Sravankumar, Artem Korenev, Arthur                Zenan Li, Xian Zhang, Kaiyu Yang, and Xujie Si.
  Hinsvark, and 542 others. 2024. The llama 3 herd of           2024. A survey on deep learning for theorem proving.
  models. Preprint, arXiv:2407.21783.                           In First Conference on Language Modeling.
Shibo Hao, Yi Gu, Haotian Luo, Tianyang Liu, Xiyan            Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
  Shao, Xinyuan Wang, Shuhua Xie, Haodi Ma,                     son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  Adithya Samavedhi, Qiyue Gao, and 1 others. 2024.             John Schulman, Ilya Sutskever, and Karl Cobbe.
  Llm reasoners: New evaluation, library, and analysis          2024. Let’s verify step by step. In The Twelfth In-
  of step-by-step reasoning with large language models.         ternational Conference on Learning Representations,
  arXiv preprint arXiv:2404.05221.                              ICLR 2024, Vienna, Austria, May 7-11, 2024. Open-
                                                                Review.net.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  Arora, Steven Basart, Eric Tang, Dawn Song, and             Sadegh Mahdavi, Branislav Kisacanin, Shubham Tosh-
  Jacob Steinhardt. 2021. Measuring mathematical                niwal, Wei Du, Ivan Moshkov, George Armstrong,
  problem solving with the math dataset. NeurIPS.               Renjie Liao, Christos Thrampoulidis, and Igor Git-
Jilin Hu, Jianyu Zhang, Yongwang Zhao, and Talia                man. 2026. Scaling generative verifiers for natural
   Ringer. 2025. Hybridprover: Augmenting theorem               language mathematical proof verification and selec-
   proving with llm-driven proof synthesis and refine-          tion. In Forty-third International Conference on Ma-
   ment. Preprint, arXiv:2505.15740.                            chine Learning.

Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang,                 Aaron Meurer, Christopher P. Smith, Mateusz Pa-
  Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun                   procki, Ondřej Čertík, Sergey B. Kirpichev, Matthew
  Zhang, Bowen Yu, Kai Dang, and 1 others. 2024.                Rocklin, Amit Kumar, Sergiu Ivanov, Jason K.
  Qwen2. 5-coder technical report. arXiv preprint               Moore, Sartaj Singh, Thilina Rathnayake, Sean Vig,
  arXiv:2409.12186.                                             Brian E. Granger, Richard P. Muller, Francesco
                                                                Bonazzi, Harsh Gupta, Shivam Vats, Fredrik Johans-
Jinhao Jiang, Zhipeng Chen, Yingqian Min, Jie Chen,             son, Fabian Pedregosa, and 8 others. 2017. Sympy:
   Xiaoxue Cheng, Jiapeng Wang, Yiru Tang, Haoxiang             symbolic computing in python. PeerJ Computer Sci-
   Sun, Jia Deng, Wayne Xin Zhao, Zheng Liu, Dong               ence, 3:e103.
   Yan, Jian Xie, Zhongyuan Wang, and Ji-Rong Wen.
   2024. Enhancing llm reasoning with reward-guided           Tobias Nipkow, Markus Wenzel, and Lawrence C. Paul-
   tree search. arXiv preprint arXiv:2411.11694.                son. 2002. Isabelle/HOL: a proof assistant for
                                                                higher-order logic. Springer-Verlag, Berlin, Heidel-
Levente Kocsis and Csaba Szepesvári. 2006. Ban-                 berg.
  dit based monte-carlo planning. In Proceedings of
  the 17th European Conference on Machine Learn-              Judea Pearl. 1984. Heuristics - intelligent search strate-
  ing, ECML’06, page 282–293, Berlin, Heidelberg.               gies for computer problem solving. In Addison-
  Springer-Verlag.                                              Wesley series in artificial intelligence.
Peter Koepke, Anton Lorenzen, and Boris Shminke.              Stanislas Polu and Ilya Sutskever. 2020. Generative
  2022. Cicm’22 system entries. In Intelligent Com-              language modeling for automated theorem proving.
  puter Mathematics, pages 344–348, Cham. Springer              CoRR, abs/2009.03393.
  International Publishing.
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying                  Tom Preston-Werner and TOML community. 2021.
 Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.                   TOML: Tom’s obvious, minimal language. https:
 Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-               //toml.io/en/.
 cient memory management for large language model
 serving with pagedattention. In Proceedings of the           Qwen Team. 2026. Qwen3.5: Towards native multi-
 ACM SIGOPS 29th Symposium on Operating Systems                modal agents.
 Principles.
                                                              Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
Xinzhe Li and Yaguang Tao. 2026. LiTS: A modular                 Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
  framework for LLM tree search. In Proceedings of               Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-
  the 64th Annual Meeting of the Association for Com-            rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
  putational Linguistics (Volume 3: System Demonstra-            Daya Guo, and Chong Ruan. 2025. Deepseek-prover-
  tions), pages 47–56, San Diego, California, United             v2: Advancing formal mathematical reasoning via
  States. Association for Computational Linguistics.             reinforcement learning for subgoal decomposition.
                                                                 Preprint, arXiv:2504.21801.
Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang
  Wang, Tao Yang, and Haitao Mi. 2025. Hunyuan-               Marco Dos Santos, Haiming Wang, Hugues de Saxcé,
  prover: A scalable data synthesis framework and              Ran Wang, Mantas Baksys, Mert Unsal, Junqi Liu,
  guided tree search for automated theorem proving.            Zhengying Liu, and Jia Li. 2025. Kimina lean server:
  Preprint, arXiv:2412.20735.                                  Technical report. Preprint, arXiv:2504.21230.


                                                          8
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,                  Ding. 2025. BFS-prover: Scalable best-first tree
  Junxiao Song, Mingchuan Zhang, Y. K. Li, Y. Wu,                search for LLM-based automatic theorem proving.
  and Daya Guo. 2024. Deepseekmath: Pushing the                  In Proceedings of the 63rd Annual Meeting of the
  limits of mathematical reasoning in open language              Association for Computational Linguistics (Volume 1:
  models. CoRR, abs/2402.03300.                                  Long Papers), pages 32588–32599, Vienna, Austria.
                                                                 Association for Computational Linguistics.
David Silver, Thomas Hubert, Julian Schrittwieser, Ioan-
  nis Antonoglou, Matthew Lai, Arthur Guez, Marc               Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-
  Lanctot, L. Sifre, Dharshan Kumaran, Thore Graepel,            mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  Timothy P. Lillicrap, Karen Simonyan, and Demis                Prenger, and Anima Anandkumar. 2023. Leandojo:
  Hassabis. 2017. Mastering chess and shogi by self-             theorem proving with retrieval-augmented language
  play with a general reinforcement learning algorithm.          models. In Proceedings of the 37th International
  ArXiv, abs/1712.01815.                                         Conference on Neural Information Processing Sys-
                                                                 tems, NIPS ’23, Red Hook, NY, USA. Curran Asso-
Théo Stoskopf. 2025. rocq-ml-toolbox. https://                   ciates Inc.
  github.com/LLM4Rocq/rocq-ml-toolbox.
                                                               Jiachen Yu, Shaoning Sun, Xiaohui Hu, Jiaxu Yan,
The Coq Dev Team. 2024. The Coq reference manual                  Kaidong Yu, and Xuelong Li. 2025. Improve llm-
  – release 8.19.0. https://coq.inria.fr/doc/V8.                  as-a-judge ability as a general ability. Preprint,
  19.0/refman.                                                    arXiv:2502.11689.
Ante Wang, Linfeng Song, Ye Tian, Dian Yu, Haitao Mi,          Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue,
  Xiangyu Duan, Zhaopeng Tu, Jinsong Su, and Dong                Yuxiao Dong, and Jie Tang. 2024. ReST-MCTS*:
  Yu. 2025. Don’t getlost in the trees: Streamlining             LLM self-training via process reward guided tree
  llm reasoning by overcoming tree search exploration            search. In The Thirty-eighth Annual Conference on
  pitfalls. Preprint, arXiv:2502.11183.                          Neural Information Processing Systems.
Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen,            Kunhao Zheng, Jesse Michael Han, and Stanislas
  Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun               Polu. 2021. Minif2f: a cross-system benchmark
  Li, Lin Li, Jian Yin, Zhenguo Li, and Xiaodan Liang.           for formal olympiad-level mathematics. CoRR,
  2023a. DT-solver: Automated theorem proving with               abs/2109.00110.
  dynamic-tree sampling guided by proof-level value
  function. In Proceedings of the 61st Annual Meeting
  of the Association for Computational Linguistics (Vol-
  ume 1: Long Papers), pages 12632–12646, Toronto,
  Canada. Association for Computational Linguistics.
Peng-Yuan Wang, Tian-Shuo Liu, Chenyang Wang,
  Ziniu Li, Yidi Wang, Shu Yan, Chengxing Jia, Xu-
  Hui Liu, Xinwei Chen, Jiacheng Xu, and Yang Yu.
  2026. A survey on large language models for mathe-
  matical reasoning. ACM Comput. Surv., 58(8).
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le,
  Ed H. Chi, Sharan Narang, Aakanksha Chowdhery,
  and Denny Zhou. 2023b. Self-consistency improves
  chain of thought reasoning in language models. In
  The Eleventh International Conference on Learning
  Representations.
Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan
  Ying, Zheng Yuan, Wenwei Zhang, Dahua Lin, and
   Kai Chen. 2025. InternLM2.5-stepprover: Advanc-
   ing automated theorem proving via critic-guided
   search. In 2nd AI for Math Workshop @ ICML 2025.
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao,
  Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian
  Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and Chong
  Ruan. 2024. Deepseek-prover-v1.5: Harnessing
  proof assistant feedback for reinforcement learning
  and monte-carlo tree search. CoRR, abs/2408.08152.
Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
  Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Ming


                                                           9
     Appendix                                                62       visible_devices: "0"
                                                             63
     A     Full List of Controllable Parameters              64 evaluator:
                                                             65       func_name: "cumulative_logprob_evaluator"
     We provide the full list of controllable parameters 66           length_norm: 0.5 #
                                                         67           client_args: # client args as before
     in our framework below. Note that, REPL client, 68
     model and sampling parameters are not given mul- 69              # for JudgeEvaluator
     tiple times as they share the same dataclass.       70           llm_as_judge_model: # model args as before
                                                             71       llm_as_judge_sampling: # sampling args as before
                                                             72       llm_as_judge_system_prompt: "You are
 1 treethink:                                                73       an LLM judge..."
 2       method_name: "BFTS"                                 74       llm_as_judge_visible_devices: "1"
 3       max_children: 3                                     75
 4       expansion_count: 512                                76       # for Discriminative reward models
 5       timeout: 480                                        77       reward_model: # model args as before
 6       graph_path: /path/to/graph/output                   78       reward_pooling_task: "classify"
 7       termination_str: "```"                              79       reward_score_reduction: "mean"
 8       store_method_class: false                           80       reward_system_prompt: "Give reward based on..."
 9       store_graph_stats: true                             81       reward_visible_devices: "0"
10       remove_duplicate_children: true
11       parse_tag: "\n"
12
13       # REPL / termination                                     B     Example Dataset Registry Entry
14       language: "lean"
15       client_args:
16         host: "localhost"                                      We implement a simple dataset registry for en-
17         port: "5000"                                           hanced reproducibility in our experiments. An
18         batch_size: 8
19         num_proc: 4                                            entry includes a name, dataset path, system and
20         timeout: 200                                           user prompts, what data key to use and its renamed
21         enable_cache: true                                     counterparts for compatibility with the framework.
22         cache_maxsize: 4096
23       termination_on_encounter:                                An example dataset registry is given below:
24           batch_size: 2
25       termination_on_paths:
26           max_repl: 16
27       max_concurrent_expansions: 8                        1 [configs.minif2f_lean]
28                                                           2 name="minif2f_lean"
29       # Special to Search Methods                         3 path_or_name="/path/to/minif2f/lean/dataset"
30       beam_width: 4                                       4 dataset_split="test"
31       exploration_weight: 1.414                           5 prompt_format="""Complete  the following lean
32       final_decision_mode: "native"                       6 code:  \n```\n{}"""
33       tie_breaker: "random"                                7 system_prompt = "You are an expert in Lean 4
34                                                            8 formal proof language."
35       # Rollout (TraditionalMCTS)                          9 data_keys=["formal_with_headers", "problem_id"]
36       rollout_evaluator_args: null                        10 renamed_data_keys=["problem", "problem_id"]
37       rollout_max_tokens: 4096                            11 format_type="huggingface_disk"
38       rollout_n: 1
39       rollout_temperature: 1.0
40       rollout_top_p: 0.9
41                                                                C     treethink run Command Example
42 policy:
43       func_name: "vllm_policy"
44       model:                                                   Below is an example command for running a tree
45         model: "deepseek-ai/DeepSeek-Prover-V2-7B"             search using our framework:
46         max_model_len:
47         tensor_parallel_size: 1
48         gpu_memory_utilization: 0.95
49       sampling:                                       1        treethink run \
50         max_tokens: 2048                              2          --gen-config-path "search_params.yaml" \
51         temperature: 1.0                              3          --data-config-path "dataset_config.yaml" \
52         top_k: -1                                     4          --data-config-name "minif2f_lean" \
53         top_p: 0.95                                   5          --batch-size 8 \
54         seed:                                         6          --num-iterations 1 \
55         stop: ["\n"]                                  7          --output-dir "/output_folder/" \
56         n: 3                                          8          --run-name "minif2f_lean" \
57         logprobs: 1                                   9          -v debug \
58       server: # vLLM server mode                     10          --continue-from-prev \
59         base_url: "http://localhost:8000/v1"         11          --async # auto-converts all components to
60         api_key: ""                                  12                  # async implementations
61         timeout: 600


                                                         10
    Classification       Components                              E   Experiment Variables for
    Language-Agnostic    Search method, Evaluator,                   Reproducibility Purposes
                         Policy, Search&Child budget
    Language-Specific    REPL client, Policy model,
                         Prompt template                          Parameter                 Value
                                                                  TreeThink commit hash     4887eb86a15f2b2bd5c4
Table 6: Classification of TreeThink’s components in                                        cf2fa0bdd34502eac357
terms of language dependency. Notably, REPL client                TreeThink PyPI package    v0.1.0
is not choosable, as it is determined upon selecting the          version
language.                                                         vLLM version              v0.21.0
                                                                  Lean/Rocq/Isabelle ver-   v4.21.0 / 9.0 / 2025-2
                                                                  sions
D     Further Discussion on System
                                                                  REPL server versions      v1.0.1 / v0.1.0 / v0.3.5
      Evaluation                                                  Exact     HuggingFace     deepseek-ai/DeepSeek-Prover-
                                                                  model IDs                 V2-7B, Qwen/Qwen2.5-Coder-
D.1     Modularity                                                                          14B-Instruct, Qwen/Qwen3.5-
As detailed in Section 3, the modular architec-                                             9B
ture of T REE T HINK allows individual components                 Exact     HuggingFace     HaimingW/miniF2F-lean4 /
                                                                  dataset IDs               LLM4Rocq/miniF2F-rocq /
to be swapped independently, facilitating highly                                            erer-can/minif2f-isabelle
reusable search processes. For example, migrat-                   Sampling parameters       temperature: 0.3, top_k: -1,
ing a tree search from Lean to Isabelle requires                                            top_p: 0.95
                                                                  Timeout behavior          Max. 480s for a single proof
modifying only four lines in configuration files:                                           search. Max. 120s for REPL .
language name, selected policy model, prompt and                  Hardware                  AMD EPYC 9224 24-Core
the dataset used. To clarify this separation of con-              (CPU/RAM/GPU)             Processor / 32 GB RAM /
cerns, Table 6 categorizes all components as either                                         Nvidia A40
                                                                  Is averaged over multi-   All experiments are single runs,
language-dependent or language-agnostic.                          ple runs?                 except for §4.2, which is aver-
                                                                                            aged over 4 runs.
D.2     Component Coverage
While we do not exhaustively evaluate every combi-               Table 8: Experiment details: version numbers, Hugging-
nation of search method, evaluator, and policy, our              Face model/dataset IDs, sampling parameters, timeout
experiments focus on a representative subset that                behavior, hardware and whether the experiments are
demonstrates the core functionality of our frame-                averaged over multiple runs or not.
work. To validate the remaining components, we
employ smoke testing, i.e. successful end-to-end                    The list of experiment variables can be found
execution on a small held-out set shown in Table 7.              in Table 8. For the datasets we use, we construct
                                                                 columns containing both the header and the prob-
Scope         Covered Components                                 lem statement. To incentivize proof generation by
                                                                 the model, we modify the target language syntax:
Main eval.    Best-first search, RF-MCTS, NormLenEvalua-
              tor, JudgeEvaluator                                replacing sorry with by in Lean 4 and with proof
Smoke test    Best-first search, Beam search, Traditional        in Isabelle, while appending the Proof. keyword
              MCTS, RF-MCTS, LogprobEvaluator, Norm-             to Rocq statements.
              LenEvaluator, Reward evaluators, JudgeEval-
              uator, REPLEvaluator, TournamentEvaluator,
              RMaxTSEvaluator

Table 7: Coverage of T REE T HINK components in our
evaluation. Main experiments use representative config-
urations, while the remaining components are verified
through integration smoke tests.

   In our formal proof search experiments, we se-
lect NormLenEvaluator as our evaluator due to
its lightweight and deterministic features. For in-
formal language test, we use JudgeEvaluator to
demonstrate our framework’s ability to integrate
reward models into the search process.

                                                            11
