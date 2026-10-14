                                         Reward-Oracle MCTS for Formal Theorem Proving: Sample-Efficient Search and
                                                         the Need for Kernel-Level Proof Auditing
                                                                                    Bodla Krishna Vamshi, Haizhao Yang∗
                                                                                           University of Maryland, College Park
                                                                                           kbodla@umd.edu, hzyang@umd.edu



                                                                     Abstract                                   fundamental challenge of efficiently exploring proof search
arXiv:2608.28639v1 [cs.AI] 11 Aug 2026




                                                                                                                spaces remains open.
                                           Formal theorem proving with large language models remains
                                           challenging due to the difficulty of navigating large proof             We propose a three-role Monte Carlo Tree Search (MCTS)
                                           search spaces efficiently. Existing tree search approaches ei-       framework built around a distinct architectural principle: the
                                           ther feed verbose compiler error messages directly into the          Lean 4 compiler is used exclusively as a reward oracle, rather
                                           generation context, increasing context usage during search,          than as a source of textual feedback for subsequent genera-
                                           or employ non-standard evaluation protocols that prevent di-         tions. Unlike compiler-guided approaches that append error
                                           rect comparison with established baselines. We propose a             messages or proof-state diagnostics to the model context, our
                                           three-role Monte Carlo Tree Search (MCTS) framework that             method converts compilation outcomes into scalar rewards
                                           treats the Lean 4 compiler purely as a reward oracle using           that are propagated through the search tree and used only for
                                           compiler output as a scalar signal for UCB-guided tree up-           UCB-guided node selection. This separation between verifi-
                                           dates without feeding error content into the generation con-
                                                                                                                cation and generation prevents compiler feedback from accu-
                                           text. Our framework decomposes proof search into three roles:
                                           a generator for proof attempts, a decomposer for subgoal de-         mulating with search depth, while still allowing formal veri-
                                           composition, and a critic for subgoal quality evaluation. We         fication signals to influence future exploration through value
                                           evaluate across 4 benchmarks spanning competition mathe-             backpropagation. Consequently, the framework performs it-
                                           matics and physics (MiniF2F, PutnamBench, LeanPhysBench,             erative, verifier-guided search over natural-language proof
                                           PhysLeandata) with three prover models at standard proof at-         plans without requiring compiler-error-conditioned genera-
                                           tempt budgets (PAB@16 to PAB@256). Our method achieves               tion.
                                           87.1% on MiniF2F with Goedel-Prover-V2-8B at PAB@256                    Our framework decomposes proof search into three dis-
                                           and solves 26/659 PutnamBench problems at PAB@32 sur-                tinct roles: a generator that produces complete proof at-
                                           passing base sampling 18/659 at same proof attempt budget.
                                                                                                                tempts, a decomposer that breaks problems into subgoals
                                           Through an exhaustive axiom-level audit of every compiled
                                           proof, we further identify reward hacking in search-based the-       with temperature-decayed sampling to balance exploration
                                           orem proving: DeepSeek-Prover-V2-7B produces proofs on               and exploitation, and a critic that evaluates subgoal quality
                                           PutnamBench that pass compilation and the standard sorry-            to provide a richer reward signal than binary compiler output
                                           token scan while depending on sorryAx. The audit removes             alone. At each MCTS iteration, the UCB policy traverses
                                           4 and 8 such proofs from whole-proof sampling at PAB@32              the current tree from the root to select a leaf node based on
                                           and PAB@128, and 11 and 19 from MCTS. We do not at-                  backpropagated compiler and critic rewards.
                                           tribute these counts to the search procedure; we report them to         We restrict our primary comparison to whole-proof sam-
                                           establish that kernel-level auditing is necessary for compiler-      pling on the same frozen checkpoint, rather than to meth-
                                           verified evaluation.
                                                                                                                ods such as BFS-Prover (Xin et al. 2025) , HunyuanProver
                                                                                                                (Li et al. 2025a), which retrain or fine-tune the underlying
                                                                 Introduction                                   prover model. Because these methods change the checkpoint
                                         Formal theorem proving with large language models has                  itself via retrained value/policy networks, additional RL, or
                                         emerged as a challenging frontier in AI reasoning, requiring           adversarially generated training data any performance delta
                                         models to navigate exponentially large proof search spaces             conflates search-procedure gains with model gains, and can-
                                         while satisfying the strict correctness requirements of in-            not isolate the contribution of the search algorithm. Whole-
                                         teractive theorem provers such as Lean 4 (de Moura and                 proof sampling provides the cleanest primary baseline for
                                         Ullrich 2021) and Isabelle (Nipkow, Paulson, and Wenzel                isolating the effect of inference-time search while holding
                                         2002). Recent advances in specialized prover models (Lin               the prover checkpoint fixed. We additionally compare with
                                         et al. 2025c; Ren et al. 2025; Wang et al. 2025) have demon-           inference-time structured-search baselines that use the same
                                         strated promising results on established benchmarks, yet the           frozen checkpoints, prompts, and evaluation environment.
                                                                                                                Throughout the paper, we use the terms proof attempt bud-
                                            ∗                                                                   get and budget interchangeably, and denote it by P AB@.
                                             Corresponding author.
                                         Preprint. Under review.                                                   We evaluate across four benchmarks spanning competi-
tion mathematics and theoretical physics MiniF2F (Zheng,         performs iterative compiler-guided search within a tree-
Han, and Polu 2022), PutnamBench (Tsoukalas et al. 2024),        based framework.
LeanPhysBench (Li et al. 2025b), and PhysLeandata (Zhang
et al. 2026) using three specialized prover models (Goedel-      Monte Carlo Tree Search in Language Model
Prover-V2-8B (Lin et al. 2025c), DeepSeek-Prover-V2-7B           Reasoning
(Ren et al. 2025), Kimina-Prover-Preview-Distill-7B (Wang        MCTS has been applied broadly to improve LLM reason-
et al. 2025)) at standard proof attempt budgets (PAB@16          ing beyond theorem proving. Yao et al. (2023) introduced
to PAB@256). On PutnamBench, our method solves 26/659            Tree of Thoughts, using LLM-guided search over reason-
problems with Goedel-Prover-V2-8B at PAB@32 surpassing           ing steps with value estimation for intermediate states. Hao
base sampling’s 18/659 at same proof attempt budget. On          et al. (2023) proposed Reasoning via Planning, applying
MiniF2F, our method achieves 87.1% with Goedel-Prover-           MCTS with LLM-based world models for multi-step rea-
V2-8B at PAB@256 and continues to improve consistently           soning tasks. Feng et al. (2024) extended AlphaZero-style
as the proof attempt budget increases.                           self-play to mathematical reasoning, training value and pol-
   Beyond strong empirical results, we identify and charac-      icy networks jointly.
terize a reward-hacking phenomenon. DeepSeek-Prover-V2-
7B, which was previously reported to exploit a Lean 4.9.0        Whole-Proof Generation
interface vulnerability (Ren et al. 2025), produces exploit-
dependent successful proofs under both whole-proof sam-          A complementary research direction focuses on whole-proof
pling and MCTS on PutnamBench. At PAB@32, the audit              generation (First et al. 2023), where the model generates a
removes 4 successful proofs from whole-proof sampling and        complete Lean proof script in a single pass, typically accom-
11 from MCTS; at PAB@128, it removes 8 and 19, respec-           panied by an extended reasoning trajectory. Recent advances
tively. This finding highlights a fundamental evaluation risk,   in this paradigm have been driven by two major approaches.
making kernel-level proof auditing essential for search-based    The first employs expert-iteration frameworks, which itera-
theorem-proving evaluation. We further conduct a systematic      tively incorporate successfully verified proofs into the train-
multi-agent analysis showing that, for the evaluated models,     ing corpus to progressively improve the prover (Polu et al.
selectively using a heterogeneous critic can improve proof       2022; Wu et al. 2021, 2025; Lin et al. 2025a; Dong and Ma
search, whereas heterogeneous decomposition consistently         2025; Lin et al. 2025b,c). The second leverages reinforce-
degrades performance.                                            ment learning guided by proof-assistant verification signals,
                                                                 enabling models to refine proof generation through verifier-
                                                                 based feedback (Kaliszyk et al. 2018; Xin et al. 2024; Zhang
                      Related work                               et al. 2025; Wang et al. 2025; Ren et al. 2025; Gloeckle et al.
Formal Theorem Proving with Large Language                       2024; Ji et al. 2025; Lin et al. 2025c).
Models
Early approaches to neural theorem proving focused on train-     Reward Hacking in Reinforcement Learning
ing specialized models to generate complete proof attempts       Reward hacking where agents exploit unintended patterns in
in a single forward pass (First et al. 2023). GPT-f (Polu and    reward signals rather than solving the intended task is a well-
Sutskever 2020) demonstrated that language models pre-           documented failure mode in reinforcement learning (Wang
trained on mathematical text could generate useful proof         et al. 2026). In the LLM context, reward hacking has been
steps when fine-tuned on proof corpora, establishing the         observed in RLHF settings where models learn to exploit re-
foundation for subsequent work. ReProver (Yang et al. 2023)      ward model weaknesses (Gao, Schulman, and Hilton 2022).
introduced retrieval-augmented generation for tactic predic-     In formal theorem proving specifically, Ren et al. (2025) re-
tion, improving performance by conditioning proof genera-        ported that DeepSeek-Prover-V2-7B exploited a Lean 4.9.0
tion on relevant premises retrieved from Mathlib.                compiler vulnerability where the apply? tactic failed to
                                                                 emit sorry declarations under certain conditions producing
Tree Search for Theorem Proving                                  proofs that passed compilation without being mathematically
Tree search methods have a long history in formal reason-        valid.
ing (Dong and Ma 2025; Xin et al. 2025; Li et al. 2025a).
HyperTree Proof Search (Lample et al. 2022) applies Monte        Lean 4 Proof Evaluation Infrastructure
Carlo Tree Search (MCTS) to Lean proof search using a            Automated evaluation of Lean 4 proofs requires interactive
learned value function jointly trained with the proof model      theorem prover infrastructure that can compile tactic-level
to guide node expansion. COPRA (Thakur et al. 2024) per-         proof attempts and return verification results programmat-
forms context-sensitive proof search by maintaining proof        ically. Several tools have been developed for this purpose,
state across attempts and incorporating compiler feedback        each with different design tradeoffs.
into subsequent generations. Draft-Sketch-Prove (Jiang et al.       LeanDojo (Yang et al. 2023) is an open-source framework
2023) decomposes proofs into high-level sketches that are        that provides a programmatic interface to Lean 4 through a
subsequently completed by a tactic model, anticipating the       REPL-based interaction model, enabling extraction of proof
use of intermediate proof decomposition. ReProver (Yang          states, tactic execution, and premise retrieval from Mathlib.
et al. 2023) improves tactic prediction through retrieval-       LeanDojo has become the standard evaluation infrastructure
augmented generation, while Prover Agent (Baba et al. 2026)      for many theorem proving benchmarks including MiniF2F
and PutnamBench, and its premise extraction capabilities
underpin retrieval-augmented approaches such as ReProver                                     v                     
                                                                                             u ln N parent(nP
                                                                                             u
(Yang et al. 2023).                                                                                           d,k )
                                                                    UCB(nP          P
                                                                         d,k ) = Q(nd,k ) + c                         (1)
                                                                                             t
   LeanInteract (Poiroux, Kuncak, and Bosselut 2025) ex-
tends the REPL-based approach with improved session man-                                            N (nP
                                                                                                        d,k )
agement and support for parallel proof evaluation, reducing        where Q(n) is the empirical mean√rollout reward of node n,
the overhead of maintaining multiple concurrent Lean pro-
cesses. PyPantograph (Aniva et al. 2024) takes a different         N (n) is its visit count, and c = 2 is the exploration con-
approach, providing a Python-native interface to the Lean          stant. For an unvisited node, the exploration term is treated as
4 kernel through direct FFI bindings rather than a REPL            +∞, ensuring that every newly generated child is evaluated
subprocess.                                                        before previously visited children are reselected. Traversal
                                                                   continues until a leaf node is reached that is either terminal
   Kimina Lean Server (Santos et al. 2025) is purpose-built
                                                                   or has not yet been fully expanded. If the selected node is non-
for large-scale parallel proof evaluation in the context of re-
                                                                   terminal and has not yet been expanded, it is expanded into
inforcement learning and tree search methods. Unlike REPL-
                                                                   K child nodes. Previously expanded internal nodes remain
based tools that maintain sequential interaction with a single
                                                                   eligible for future traversal, and their children are repeatedly
Lean process, Kimina Lean Server manages a pool of per-
                                                                   selected according to the UCB policy as the search proceeds.
sistent Lean REPL instances that handle concurrent proof
                                                                   Thus, the tree is incrementally refined over successive itera-
compilation requests enabling high-throughput evaluation at
                                                                   tions as visit counts and value estimates are updated through
the sampling budgets required by tree search methods. The
                                                                   backpropagation.
server exposes an HTTP interface that accepts complete Lean
4 proof strings and returns compilation results including suc-
                                                                   Expansion
cess status, error messages, and sorry usage detection. Our
method uses Kimina Lean Server as the compiler reward              The selected node n at depth d is expanded by generating
oracle throughout all experiments.                                 K=4 child subgoals (gk ) using the decomposer role. The
                                                                   decomposer is prompted with the original theorem and the
                                                                   trajectory from the root to the current node, namely, the
   Comparison with Existing Inference-Time                         sequence of subgoals accumulated along that path. It pro-
              Search Methods                                       poses the next intermediate proof step as a natural language
To clarify the algorithmic distinctions between our frame-         subgoal, producing K diverse candidates that become child
work and prior inference-time search methods for formal the-       nodes nnd+1,1 , . . . , nnd+1,K in the tree.
orem proving, Table 1 summarizes the major design choices.            A key design choice in expansion is temperature decay:
Unlike methods that condition future generation on com-            the decomposer sampling temperature τd is annealed accord-
piler feedback or proof-state diagnostics, our approach treats     ing to both the current depth d and the iteration index i as:
the Lean verifier exclusively as a reward oracle: only the
scalar reward is propagated through MCTS, while compiler                        τd = τ0 · e−0.12 d · e−0.03 ln(1+i)            (2)
messages are never inserted into the LLM context. Further-         starting from τ0 =0.7. At shallow depths and early iterations,
more, our search operates over natural-language proof plans        the higher temperature encourages diverse subgoal propos-
rather than formal proof states, allowing the search policy        als, enabling broad exploration of distinct proof strategies.
to allocate compute through UCB-guided exploration while           At greater depths and later iterations, the lower temperature
remaining independent of compiler-specific feedback.               concentrates sampling on more focused, committed proof
                                                                   directions. This schedule directly governs the exploration–
                          Method                                   exploitation balance of the search. Our ablation analysis,
Our framework decomposes proof search into three special-          provided in the supplementary appendix submitted with the
ized roles: a generator, a decomposer, and a critic coordi-        paper, shows that removing temperature decay consistently
nated by a Monte Carlo Tree Search procedure. Each node            degrades performance across the evaluated models, indicat-
nP                                                                 ing that it is a critical architectural component of our frame-
  d,k in the search tree represents a subgoal state at depth
d, child index k, with parent node P (where P =r denotes           work.
the root). The tree is initialized with a single root node nr0,0
corresponding to the original theorem T . We describe the          Evaluation
four phases of each MCTS iteration below, with the over-           Each newly expanded child node nnd+1,k is evaluated using
all procedure illustrated in Figure 1. Throughout this paper,      two complementary reward signals that together form the
“states” in our method refer to natural-language proof-plan        rollout reward rt = rc + rs .
search states rather than formal Lean 4 proof states.
                                                                   Critic reward rc ∈ [0, 1]. The critic role assesses the qual-
                                                                   ity of the proposed subgoal gk by sampling the critic LLM
Selection                                                          five times at a fixed low temperature of τ =0.3 and averaging
Beginning from the root node nr0,0 , the selection phase tra-      the scores. The low temperature ensures stable, consistent
verses the tree by repeatedly choosing the child node that         evaluation rather than diverse sampling. The critic provides
maximizes the UCB criterion:                                       a soft quality signal that compensates for the binary nature
Table 1: Architectural comparison between our framework and closely related inference-time search methods. “Compiler usage”
refers to how Lean verification is incorporated into the search process.

 Method                                Search                      Search             Generator Receives         LLM           Search              Reward
                                    Representation                Strategy            Compiler Feedback          Critic       Allocation          Backprop.
 COPRA                            Formal proof state        Sequential refinement       ✓ Compiler text           –              Fixed                –
 Prover Agent                       Proof attempts            Tree refinement           ✓ Compiler text           –       Heuristic expansion   Method-specific
 BFS+CG                         Natural-language plans          Breadth-first       × (scalar evaluation only)    ✓          Breadth-first            –
 One-shot decomposition         Natural-language plans        Single expansion      × (scalar evaluation only)    ✓         Flat expansion            –
 Reward-Oracle MCTS (Ours)   Natural-language proof plans   UCB-guided MCTS          × Scalar reward only         ✓           Adaptive                ✓



of compiler feedback a subgoal that does not immediately
yield a compiling proof may still receive high critic reward                                 PAB@B = N × K × S = 4 × 4 × S                                  (3)
if it represents a promising intermediate step toward the final
                                                                                giving S=2 for PAB@32, S=4 for PAB@64, S=8 for
proof. The critic outputs a score r̂c ∈ [0, 100], which we
                                                                                PAB@128, and S=16 for PAB@256. Throughout this paper,
normalize as rc = r̂c /100 ∈ [0, 1].
                                                                                PAB@B denotes proof-attempt budget.
Server reward rs ∈ [0, 1]. The generator role produces S
complete Lean 4 proof attempts for each child node, con-                                                          Results
ditioned on the full trajectory from root to that node at a                     We evaluate our framework across four benchmarks MiniF2F
fixed temperature of τ =0.7. Each attempt is submitted to                       (Zheng, Han, and Polu 2022), PutnamBench (Tsoukalas
the Kimina Lean server (Santos et al. 2025), which compiles                     et al. 2024), PhysLeandata (Zhang et al. 2026), and Lean-
the proof and checks for the absence of sorry declarations.                     PhysBench (Li et al. 2025b) using three specialized prover
Let sk denote the number of attempts that compile success-                      models: Goedel-Prover-V2-8B (Lin et al. 2025c), DeepSeek-
fully. We define the normalized server reward as rs = sk /S,                    Prover-V2-7B (Ren et al. 2025), and Kimina-Prover-Preview-
rs ∈ {0, 1/S, 2/S . . . , 1}. Crucially, we use compiler output                 Distill-7B (Wang et al. 2025). All results are averaged over
solely as a scalar count signal no error message content is                     5 random seeds. Unlike much prior work in this area, we re-
fed back into the generation context.                                           port mean ± standard deviation across 5 random seeds for all
                                                                                experiments to support statistical reliability of the reported
Backpropagation
                                                                                gains.
After rollout evaluation, the obtained rollout reward rt is
propagated from the expanded node back to the root along                        Baseline description BFS+CG. Breadth-first expansion
the selected search path. For every node on this path, the visit                of the decomposition tree in which the critic score alone
count and cumulative reward are updated as                                      ranks and selects nodes for expansion at each level, with no
                                                                                UCB criterion and no backpropagation of compiler reward
       N (n) ← N (n) + 1,          W (n) ← W (n) + rt ,                         along the search path.
and the node value used by UCB is computed as                                      One-shot decomposition. All 16 subgoal candidates are
                                                                                generated in a single flat expansion from the root and each
                                   W (n)
                          Q(n) =         .                                      is evaluated independently, with no iterative reselection iso-
                                   N (n)                                        lating whether gains derive from decomposition scaffolding
These updates follow the standard MCTS backpropagation                          alone rather than from iterative, reward-guided search.
procedure. These updated statistics are subsequently used by                       Both baselines use the identical frozen checkpoints for the
the UCB selection policy during future iterations to balance                    generator, decomposer, and critic roles as our framework,
exploration and exploitation.                                                   and identical prompt templates and decoding configurations;
   After backpropagation, the next iteration begins with a                      they differ from our method only in the search mechanism
fresh selection phase from the root. The updated visit counts                   that allocates the fixed proof-attempt budget.
and value estimates allow the UCB policy to allocate more
search effort to promising subtrees while continuing to ex-                     Main Results
plore less-visited alternatives.                                                Table 2 and 3 reports results on MiniF2F test set. Our method
                                                                                consistently outperforms whole proof sampling methods
Proof attempt Budget                                                            across all three models at matched proof attempt budgets.
At each of N MCTS iterations, one leaf node is selected ac-                     On Goedel-Prover-V2-8B our method achieves 84.2 ± 0.5%
cording to the UCB policy and expanded into K child nodes.                      at PAB@32, surpassing whole-proof baseline (82.4%) (Ta-
Each child is evaluated using S complete proof attempts, re-                    ble 3). To analyze the importance of individual reward func-
sulting in K × S generator rollouts per iteration. Therefore,                   tions, we perform ablations comparing the critic-only reward
the total proof-attempt sampling budget is exactly N ×K ×S                      against the combined critic + verifier reward (Table 4).
per problem. We scale the proof attempt budget by varying                          To directly compare against a feedback-driven baseline
S while keeping N and K fixed:                                                  on the same checkpoint, we reproduce Prover Agent (Baba
                                                                              Root
                                                                             Node

                                                 Input problem




                                                                         Decomposer agent
                                                                                               UCB
                                                         rt                                        select
                                                        rop.
                                                   Backp

                                         nrd,1                   nrd,2                   nrd,3                      nrd,4    Depth ( d ) = 1

                          rt
                                 .
                           rop
                        ckp




                                                                                                                   ct
                                                                                                                ele
                      Ba




                                                                                                              Bs
                                                                                                            UC
                  n1d,1          n1d,2           n1d,3           n1d,4                      n4d,1           n4d,2           n4d,3         n4d,4   Depth ( d ) = 2




                                                                                                                                                  Proo
                                                                                                                                                      f atte
                                                                                                                            Generator agent                 mpts



                                                                                     Critic agent

                                                                                                                                                  Kimina Server
                                     n4d,2
                                                         Rollout reward         = Critic reward        +    Server reward
                                                              ( rt )                  ( rc )                    ( rs )



Figure 1: Overview of the proposed search framework. Each node nP
                                                                d,N represents the k-th child at depth d, with parent P :P =
r denotes the root.


et al. 2026) using their released implementation with Goedel-                                 averaged across five complete runs per sample. We use vLLM
Prover-V2-8B as the prover model, under our evaluation                                        package for inference with one model instance loaded per
environment (Lean 4.15.0, Mathlib commit 9837ca9d). At                                        GPU; the same instance serves the generator, decomposer,
their native sample budget of 260, we obtain 86.2 ± 0.1%                                      and critic roles. We use 4 Nvidia H200-SXM GPUs for in-
on MiniF2F, compared to 87.1 ± 0.2% for our method at                                         ference. Multiple completions are generated within batched
PAB@256, despite Prover Agent’s use of direct compiler-                                       requests: whole-proof sampling produces 32 outputs from
error feedback in context versus our oracle-only signal.                                      one request, while each critic evaluation produces five out-
   On PutnamBench (Table 5), our method solves 26/659                                         puts in one request whose scores are subsequently averaged.
problems with Goedel-Prover-V2-8B at PAB@32 and                                               To ensure strict budget matching, neither method terminates
36/659 at PAB@128, compared to 18/659 and 22/659                                              early after finding a valid proof.
for whole-proof sampling. On PhysLeandata and LeanPhys-
Bench (Tables 6, 7), our method consistently outperforms                                         Despite the additional decomposition and critic compu-
whole-proof sampling across all three models at the matched                                   tations, our framework consistently consumes fewer infer-
budget of PAB@16, with gains of +1.9% to +2.4% on                                             ence tokens across all three models. Relative to whole-
PhysLeandata and +1.5% to +2.0% on LeanPhysBench with                                         proof sampling, total token usage decreases by 32.29% for
PhysLib context. Notably, our method without PhysLib con-                                     Goedel-Prover-V2-8B, 33.17% for DeepSeek-Prover-V2-7B,
text approaches the performance of whole-proof sampling                                       and 33.07% for Kimina-Prover-7B. Output-token usage de-
with PhysLib suggesting that structured search partially com-                                 creases by 35.35%, 36.07%, and 36.05%, respectively. Aver-
pensates for the absence of domain-specific library context.                                  aged across the three models, our framework reduces output-
Consistent gains across both physics benchmarks demon-                                        token generation by 35.83% and total token consumption
strate that our method generalizes beyond mathematical do-                                    by 32.84%. These results show that the short decomposer
mains where model familiarity is minimal.                                                     and critic interactions substantially reduce the number of
                                                                                              generator output tokens consumed under the same proof-
             Inference-token efficiency                                                       attempt budget, more than offsetting their additional token
                                                                                              overhead. Both methods use an identical vLLM deployment
In this section we additionally compare cumulative inference-                                 with one model instance per GPU and the same maximum
token usage at PAB@32 (Table 8). All reported counts are                                      GPU-memory-utilisation setting of 0.95.
                  Table 2: Results on the miniF2F test set for different methods. All results are averaged over
                  5 random seeds.

                  Model      Method                    Size Generator Decomposer      Critic    Success (%)
                                                            completions completions completions
                             BFS+CG                            4×2×4            4×4           4×4     62.5 ± 0.6
                  Kimina     One-shot decomposition 7B        16 × 2 × 1       16 × 1        16 × 1   61.3 ± 0.6
                             Agent (ours)                      4×2×4            4×4           4×4     64.3 ± 0.8
                           BFS+CG                              4×2×4            4×4           4×4     75.4 ± 0.6
                  DeepSeek One-shot decomposition 7B          16 × 2 × 1       16 × 1        16 × 1   74.5 ± 0.3
                           Agent (ours)                        4×2×4            4×4           4×4     77.1 ± 0.3
                             BFS+CG                            4×2×4            4×4           4×4     82.7 ± 0.4
                  Goedel     One-shot decomposition 8B        16 × 2 × 1       16 × 1        16 × 1   81.7 ± 0.4
                             Agent (ours)                      4×2×4            4×4           4×4     84.2 ± 0.5
                     BFS indicates breadth first search, CG indicates critic guided search


Effect of Adaptive Decomposer Temperature                              models evaluated here, an appropriately chosen heteroge-
Table 9 reports the effect of removing temperature decay               neous critic can provide complementary evaluation signals
from the decomposer, replacing the annealed schedule                   that improve search quality, although this benefit is not ob-
                                                                       served for every model substitution.
             τd = τ0 · e−0.12 d · e−0.03 ln(1+i)             (4)          The decomposer role exhibits a different trend. Replacing
                                                                       the homogeneous Goedel-Prover-V2-8B decomposer with ei-
   (Equation 4) with a fixed temperature of τ =0.7 through-            ther DeepSeek-Prover-V2-7B or Kimina-Prover-7B consis-
out. Removing temperature decay consistently degrades per-             tently reduces performance, achieving 83.8 ± 0.4% (−0.4
formance across all three models: Kimina-Prover-7B drops               points) and 82.2 ± 0.5% (−2.0 points), respectively. Further-
from 64.3 ± 0.8% to 62.5 ± 0.5% (−1.8%), DeepSeek-                     more, combining heterogeneous models in both supporting
Prover-V2-7B from 77.1 ± 0.3% to 74.6 ± 0.3% (−2.5%),                  roles does not preserve the critic improvement. For exam-
and Goedel-Prover-V2-8B from 84.2 ± 0.5% to 81.9 ± 0.3%                ple, using DeepSeek-Prover-V2-7B as both decomposer and
(−2.3%).                                                               critic achieves only 80.9 ± 0.3%, substantially below both
   These consistent drops across all models confirm that tem-          the homogeneous baseline (84.2 ± 0.5%) and the configura-
perature decay is a critical architectural component rather            tion that changes only the critic (86.1 ± 0.3%). This suggests
than a model-specific artifact. Without decay, the decom-              that, for the evaluated models, the performance gain from a
poser maintains high temperature throughout the search con-            heterogeneous critic depends on maintaining a homogeneous
tinuing to propose diverse subgoals even at deeper depths              generator–decomposer pair.
and later iterations where the search should be commit-                   Overall, within the scope of the evaluated models and
ting to promising proof directions. This prevents the tree             benchmark, the strongest configuration pairs a Goedel-
from effectively exploiting high-reward subtrees identified            Prover-V2-8B generator and decomposer with a DeepSeek-
by backpropagated compiler rewards, reducing the search to             Prover-V2-7B critic. These findings suggest that selectively
essentially diverse but unguided sampling.                             introducing heterogeneity into the critic role is a promis-
                                                                       ing direction for improving theorem-proving search, while
Multi-Agent Role Analysis                                              additional experiments across a broader range of generator
Table 10 reports results from our systematic multi-agent               models and benchmarks are needed to determine the extent
analysis on Minif2f test set for proof attempt budget of               to which these observations generalize.
32 (PAB@32), where Goedel-Prover-V2-8B is fixed as the                 Effect of the Iteration–Branching Allocation
generator and all combinations of Goedel-Prover-V2-8B,
DeepSeek-Prover-V2-7B, and Kimina-Prover-7B are evalu-                 We study how the fixed proof-attempt budget should be dis-
ated in the decomposer and critic roles. The objective is              tributed between the number of MCTS iterations N and the
to examine whether introducing heterogeneous models into               branching factor K. We keep the number of complete proof
supporting roles can improve proof search performance over             attempts per child fixed at S = 2 and vary N and K such
the homogeneous baseline.                                              that
   Among the evaluated critic assignments, heterogeneous                                    N × K × S = 32
critics exhibit mixed behavior. Using DeepSeek-Prover-V2-              for every configuration. Consequently, all settings use the
7B as the critic achieves the best overall performance                 same maximum number of complete proof generations, de-
(86.1 ± 0.3%), improving upon the homogeneous config-                  composition calls, and critic evaluations. Specifically, each
uration (84.2 ± 0.5%) by 1.9 percentage points. In contrast,           configuration produces N K = 16 decomposition candi-
replacing the critic with Kimina-Prover-7B decreases perfor-           dates, 5N K = 80 critic evaluations, and N KS = 32 com-
mance to 82.7 ± 0.4%. These results indicate that, for the             plete proof attempts. The configurations therefore differ pri-
Table 3: Results on miniF2F test set for different proof at-       Table 4: Results on miniF2F test set for reward ablations. All
tempt budgets and methods. All results are averaged over 5         results are averaged over 5 random seeds.
random seeds. Prover Agent is reproduced under our evalu-
ation setting at a proof attempt budget of 260, since only at        Model       Method                    Size PAB Success (%)
this budget does its full iterative-refinement pipeline execute.
                                                                                                                   32      73.7 ± 0.7
                                                                                 Agent (critic only)
                                                                                                                   64      74.2 ± 0.3
     Model       Method         Size Budget Success (%)              DeepSeek                               7B
                                                                                                                   32      77.1 ± 0.3
                                       32     62.8 ± 0.8                                                           64      79.3 ± 0.4
                 Whole-proof                                                     Agent (critic+reward)
                                       64     65.1 ± 0.3                                                           128     81.4 ± 0.2
     Kimina                     7B     32     64.3 ± 0.8                                                           256     82.6 ± 0.1
                 Agent (ours)
                                       64     66.9 ± 0.2                                                           32      81.6 ± 0.6
                                                                                 Agent (critic only)
                                       32     75.2 ± 0.5                                                           64      82.5 ± 0.5
                 Whole-proof
                                       64     76.3 ± 0.7             Goedel                                 8B     32     84.2 ± 0.5
                                      128     77.5 ± 0.3                                                           64     85.6 ± 0.4
     DeepSeek                   7B    256     78.2 ± 0.1                         Agent (critic+reward)
                                                                                                                   128    86.3 ± 0.2
                 Prover Agent         260     81.7 ± 0.3                                                           256    87.1 ± 0.2
                                       32     77.1 ± 0.3
                 Agent (ours)          64     79.3 ± 0.4           Table 5: Results on PutnamBench for different methods and
                                      128     81.4 ± 0.2           proof attempt budgets. Following prior PutnamBench eval-
                                      256     82.6 ± 0.1           uations, results are reported as a single benchmark run over
                                       32     82.4 ± 0.6           all 659 problems
                 Whole-proof
                                       64     83.3 ± 0.4
                                      128     83.9 ± 0.2                   Model       Method           Size PAB #Solved
                                      256     84.7 ± 0.1
     Goedel                     8B                                                                              32   9/659
                                                                           DeepSeek Whole-proof 7B
                 Prover Agent         260     86.2 ± 0.1                                                       32∗ 13/659
                                       32     84.2 ± 0.5                                                       128 10/659
                                       64     85.6 ± 0.4                                                       128∗ 18/659
                 Agent (ours)
                                      128     86.3 ± 0.2                                                        32   16/659
                                      256     87.1 ± 0.2                                                       32∗ 27/659
                                                                                       Agent (ours)
                                                                                                               128 25/659
                                                                                                               128∗ 44/659
marily in how these calls are distributed across sequential                                                       32     18/659
                                                                                       Whole-proof
MCTS iterations.                                                                                                 128     22/659
   As shown in Table 11, shallow configurations with large                 Goedel                        8B       32     26/659
                                                                                       Agent (ours)
branching factors are computationally efficient but achieve                                                      128     36/659
lower proof success. The N = 1, K = 16 and N = 2, K = 8                                   ∗
                                                                                              Potential exploit.
configurations obtain success rates of 82.1% and 82.3%,
respectively. In these settings, most of the budget is allocated
to generating a broad set of decompositions, with limited          ing 2.8× the wall-clock time of the N = 1, K = 16 setting,
opportunity to use intermediate rewards to guide subsequent        compared with 1.5× for N = 4, K = 4. This difference in
node selection.                                                    success is small relative to the variation across random seeds.
   Increasing the number of MCTS iterations to N = 4 im-              These results reveal an accuracy–latency trade-off. Broad,
proves success to 84.2%. Notably, the N = 1, K = 16 and            shallow search reduces inference latency but provides in-
N = 4, K = 4 configurations use the same numbers of de-            sufficient iterative refinement, whereas very narrow search
composition calls, critic evaluations, and complete proof at-      increases sequential search overhead without yielding a
tempts. Their performance difference therefore cannot be at-       meaningful improvement in proof success. We therefore use
tributed to a larger component-call budget. Instead, the result    N = 4, K = 4, S = 2 in the main experiments, as it pro-
indicates that distributing node expansions across multiple        vides the best practical balance between proof success and
MCTS iterations, with intermediate reward backpropagation          wall-clock efficiency under the fixed proof-attempt budget.
and subsequent UCB-guided selection, is more effective than
generating all decomposition candidates in a single expan-         Reward Hacking Analysis. DeepSeek-Prover-V2-7B ex-
sion.                                                              hibits a substantially different pattern on PutnamBench. Be-
   Further increasing the number of iterations produces di-        fore exploit auditing, whole-proof sampling solves 13/659
minishing returns. The N = 8, K = 2 configuration                  problems at PAB@32 and 18/659 at PAB@128, whereas
achieves 83.7%, while the narrowest configuration, N =             our method solves 27/659 and 44/659, respectively. How-
16, K = 1, achieves 84.3%. The latter is only 0.1 percentage       ever, screening the successful proofs using previously re-
points above the N = 4, K = 4 configuration, while requir-         ported exploit indicators identifies a substantial number
Table 6: Results on PhysLeandata test set. Results are aver-      Lean context required for the documented exploit pattern to
aged across 5 random seeds.                                       succeed. We therefore observe successful exploit-dependent
                                                                  proofs primarily on PutnamBench, where the underlying
   Model       Method               Size PAB Success (%)          prover already exhibits the documented behaviour. We re-
               Whole-proof                   16     25.2 ± 0.6    port both unaudited and audited results transparently in Ta-
   Kimina                            7B                           ble 5 and recommend kernel-level proof auditing for models
               Agent (critic+reward)         16     27.5 ± 0.6
                                                                  that exhibit anomalous increases in compiler-verified solve
               Whole-proof                   16     33.8 ± 0.5    counts under search-based inference.
   DeepSeek                          7B
               Agent (critic+reward)         16     36.2 ± 0.6
               Whole-proof                   16     31.9 ± 0.7    Potential Exploit Identification. To investigate the gener-
   Goedel                            8B
               Agent (critic+reward)         16     33.8 ± 0.4    ation of exploitative proof strategies, we adopt a conservative
                                                                  multi-stage audit protocol. We first identify potentially suspi-
Table 7: Results on LeanPhysBench (proof attempt budget           cious proof attempts using the exploit patterns reported in the
(PAB@B) = 16). Results are averaged across 5 random               DeepSeek-Prover-V2-7B technical report (Ren et al. 2025).
seeds. The PhysLib library is directly passed as context.         That work reports that the 7B model occasionally exploits a
Critic+server rewards used for all our method configurations.     Lean 4.9.0 compiler/interface bug on PutnamBench through
                                                                  characteristic proof structures involving the apply? tactic
                                                                  together with specific Cardinal-related lemmas, including
      Model       Method                      Success (%)
                                                                  Cardinal.toNat and Cardinal.natCast_inj. We
                  Whole-proof                      9.3 ± 0.3      use these patterns only as an initial screening mechanism;
                  Whole-proof (w/ PhysLib)        13.5 ± 0.7      their lexical presence is never treated as sufficient evidence
      Kimina
                  Agent (ours, no PhysLib)        11.5 ± 0.6      that a proof is exploitative. Because we are not Lean 4 domain
                  Agent (ours, w/ PhysLib)        15.0 ± 0.7
                                                                  experts, we rely on the indicators documented in prior work
               Whole-proof                        11.5 ± 0.2      rather than independently deriving new exploit signatures.
               Whole-proof (w/ PhysLib)           14.5 ± 0.2      Accordingly, our initial screening can detect recurrences of
      DeepSeek
               Agent (ours, no PhysLib)           13.0 ± 0.4      the documented exploit family but cannot by itself rule out
               Agent (ours, w/ PhysLib)           16.5 ± 0.6      undocumented exploit patterns.
                  Whole-proof                     10.0 ± 0.2         For every successfully compiled proof, including proofs
                  Whole-proof (w/ PhysLib)        15.0 ± 0.2      that do not contain the previously reported lexical indica-
      Goedel
                  Agent (ours, no PhysLib)        12.0 ± 0.4      tors, we append #print axioms <theorem_name>
                  Agent (ours, w/ PhysLib)        16.5 ± 0.3      and recompile the resulting code using the same Lean eval-
                                                                  uation environment. A proof is classified as a potential ex-
                                                                  ploit only when the resulting theorem declaration depends on
containing the apply? tactic and Cardinal-family lem-             sorryAx. For proofs that also contain a documented suspi-
mas (Cardinal.toNat, Cardinal.natCast_inj).                       cious construction, we additionally remove that construction
These patterns were identified in the DeepSeek-Prover-V2-         and verify that the proof no longer compiles. Thus, neither the
7B technical report (Ren et al. 2025) as being associated         presence of apply? nor the use of Cardinal-family lemmas
with a Lean 4.9.0 compiler/interface vulnerability in which       is independently sufficient for classification. Only successful
apply? may fail to emit an explicit sorry declaration             proofs whose resulting declarations depend on sorryAx are
under certain conditions, producing proof declarations that       removed from the audited solve counts. Since the underlying
compile despite depending on sorryAx.                             Lean behaviour has already been documented in prior work
   After excluding proofs confirmed by our audit to depend        (Ren et al. 2025), we use the term potential exploit rather than
on sorryAx, the whole-proof solve counts decrease from            claiming to have independently established a new compiler
13/659 to 9/659 at PAB@32 and from 18/659 to 10/659 at            vulnerability.
PAB@128. Thus, the audit removes 4 and 8 whole-proof                 Across all experiments, successful exploit-dependent
solutions at the two budgets. For our method, the solve           proofs are observed only for DeepSeek-Prover-V2-7B on Put-
counts decrease from 27/659 to 16/659 at PAB@32 and               namBench. Under whole-proof sampling, the audit removes
from 44/659 to 25/659 at PAB@128, removing 11 and 19              4 successful proofs at PAB@32 and 8 at PAB@128. Under
solutions, respectively. Consequently, our method produces 7      our MCTS framework, it removes 11 successful proofs at
more exploit-dependent successful proofs than whole-proof         PAB@32 and 19 at PAB@128. No successful proof gen-
sampling at PAB@32 and 11 more at PAB@128.                        erated by Goedel-Prover-V2-8B or Kimina-Prover-Preview-
   Critically, successful exploitation is not observed on the     Distill-7B is found to depend on sorryAx under the same
physics benchmarks. On PhysLeandata, DeepSeek-Prover-             audit protocol. Although DeepSeek-Prover-V2-7B occasion-
V2-7B generates exploit-related patterns for only 1 of the        ally generates proof attempts containing exploit-related pat-
200 evaluated problems, and none of these attempts com-           terns on PhysLeandata, LeanPhysBench, and the MiniF2F
pile successfully. Likewise, no exploit-dependent successful      test set, none of these attempts both compile successfully
proof is identified on LeanPhysBench. These results suggest       and produce a theorem declaration depending on sorryAx.
that the prover lacks sufficient familiarity with the graduate-   They therefore do not contribute to the reported solve counts.
level physics formalizations to construct the surrounding         These observations suggest that our MCTS framework does
Table 8: Role-level inference-token usage at PAB@32, averaged across five runs. Token counts are cumulative across all role
completions in one complete benchmark run.

                                   Model                    Role/Method   Input   Output           Total
                                                            Decomposer    1,438     1,449         2,887
                                                            Critic        4,126       196         4,322
                                   Goedel-Prover-V2-8B
                                                            Generator     4,231   203,580       207,811
                                                            Whole-proof     117   317,420       317,537
                                                            Decomposer    1,347     1,392         2,739
                                                            Critic        4,021       187         4,208
                                   DeepSeek-Prover-V2-7B
                                                            Generator     4,058   204,113       208,171
                                                            Whole-proof     117   321,762       321,879
                                                            Decomposer    1,427     1,466         2,893
                                                            Critic        4,083       185         4,268
                                   Kimina-Prover-7B
                                                            Generator     4,135   203,611       207,746
                                                            Whole-proof     117   320,986       321,103


Table 9: Results with and without temperature variation on            Table 11: Effect of the iteration–branching-factor allocation
miniF2F test set (proof attempt budget = 32; critic + server          under a fixed proof-attempt budget on MiniF2F with Goedel-
rewards used for all configurations). Results are averaged            Prover-V2-8B. We fix S = 2 proof attempts per child and
across 5 random seeds.                                                vary the number of MCTS iterations N and children per
                                                                      expansion K, such that N KS = 32 for all configurations.
  Model       Method                              Success (%)         Wall-clock time is reported relative to the N = 1, K = 16
                                                                      configuration. Results are averaged over five random seeds.
              Agent (ours, w/ temp. variation)    64.3 ± 0.8
  Kimina
              Agent (ours, w/o temp. variation)   62.5 ± 0.5
                                                                            N     K        S    Success (%)      Rel. Wall-Clock
              Agent (ours, w/ temp. variation)    77.1 ± 0.3
  DeepSeek
              Agent (ours, w/o temp. variation)   74.6 ± 0.3                 1    16       2    82.1 ± 0.4             1.0×
              Agent (ours, w/ temp. variation)    84.2 ± 0.5                 2     8       2    82.3 ± 0.3             1.2×
  Goedel
              Agent (ours, w/o temp. variation)   81.9 ± 0.3                4†     4       2    84.2 ± 0.5             1.5×
                                                                             8     2       2    83.7 ± 0.4             2.1×
                                                                            16    1        2    84.3 ± 0.2             2.8×
Table 10: Multi-agent analysis with different models in differ-
                                                                                  †
ent roles on miniF2F test set with sampling budget PAB@32.                            Configuration used in our main results.
Results are averaged across 5 random seeds.

     Generator Decomposer Critic              Success (%)             Lean 4.15.0 and Mathlib environment.
     Goedel       Kimina            Kimina    81.4 ± 0.4                 To ensure that the audit is not limited to proofs match-
     Goedel       Kimina            Goedel    82.2 ± 0.5              ing the previously reported lexical indicators, we exe-
     Goedel       Goedel            Kimina    82.7 ± 0.4              cute #print axioms on every successfully compiled
     Goedel       DeepSeek          DeepSeek 80.9 ± 0.3               proof generated by all three prover models, across all four
     Goedel       Goedel            DeepSeek 86.1 ± 0.3               benchmarks, methods, and proof-attempt budgets. Because
     Goedel       DeepSeek          Goedel    83.8 ± 0.4              #print axioms queries the dependencies of the resulting
     Goedel       Goedel            Goedel   84.2 ± 0.5 †             Lean declaration rather than relying on the evaluation wrap-
                           †
                               Baseline.                              per’s surface-level compilation status or source-level sorry
                                                                      scan, it directly determines whether a successful declaration
                                                                      depends on kernel axioms such as sorryAx. This exhaus-
not introduce a new exploit strategy; instead, it could increase      tive audit finds no sorryAx dependency among successful
the number of successful exploit-dependent proofs produced            proofs generated by Goedel-Prover-V2-8B or Kimina-Prover-
by a model that already exhibits the documented behavior.             Preview-Distill-7B under any evaluated configuration.
   All our experiments, including the baselines, are con-                The same audit procedure is applied uniformly to whole-
ducted using Lean 4.15.0, Mathlib v4.15.0 (commit                     proof sampling and MCTS-generated proofs, enabling a con-
9837ca9d, dated 2025-01-05), and the Kimina Lean Server               trolled comparison between the two inference procedures.
2.0.0 container image. Although the underlying interface be-          We emphasize that this procedure verifies axiom-level de-
havior was originally documented under Lean 4.9.0 (Ren                pendencies as reported by Lean; it does not constitute an
et al. 2025), we verify that proof attempts exhibiting the doc-       independent mathematical or semantic validation beyond the
umented apply?-based pattern continue to produce theo-                guarantees provided by Lean’s kernel and axiom-dependency
rem declarations depending on sorryAx under our pinned                tracking.
               Implementation details                                 depend on. The protocol is applied identically to whole-proof
Reproduction protocol and comparability to published                  sampling and to our framework at every budget, so the with-
results . All baselines in the paper are re-run in-house              /without contrast varies only the presence of library context.
under a single pinned environment (Lean 4.15.0, Mathlib
v4.15.0 commit 9837ca9d dated 2025-01-05, Kimina Lean
                                                                      Inference configuration.
Server 2.0.0), using the prompt templates in Section and              The three agent roles use different decoding configurations
the decoding configurations in Section . Our whole-proof              tailored to their respective objectives.
sampling numbers are consequently not directly comparable              • Generator. Maximum generation length is 16,384 tokens
to the pass@k figures reported in the original model re-                 with decoding temperature τ = 0.7. This relatively higher
leases, and we do not present them as reproductions of those             temperature encourages diverse proof attempts while re-
figures. The factors accounting for the difference are, first,           maining sufficiently stable for formal proof generation.
published numbers are obtained under substantially older
toolchain pins, and solve rates are highly sensitive to this           • Decomposer. Maximum generation length is 1,024 to-
choice: (Gu et al. 2025) measure the same Goedel-Prover-                 kens. The decomposer uses the adaptive temperature
V2-32B checkpoint at 90% pass@64 on MiniF2F and 86                       schedule described in Equation 4, allowing broader explo-
solves on PutnamBench at pass@184 under Mathlib 4.9, but                 ration during early search and progressively more focused
at 80% and 75 solves respectively under Mathlib 4.19 a ten-              subgoal generation at deeper levels.
point swing on MiniF2F attributable to the toolchain alone,            • Critic. Maximum generation length is limited to 3 to-
with no change to the model. Second, published figures use               kens with decoding temperature τ = 0.3. Since the critic
model-specific prompt templates and, for Goedel-Prover-V2,               produces only scalar quality ratings rather than proofs, a
an optional compiler-guided self-correction mode; we in-                 low temperature is used to obtain stable and reproducible
stead use one uniform prompt template and decoding config-               evaluations.
uration across all three provers and disable self-correction,
so that every method under comparison differs only in its             Prompt Configurations
search procedure and not in its inference stack.                      We report the exact system prompts used for each of the three
   Our decision to pin a recent toolchain rather than re-             agent roles below. The same prompt template is used across
produce the original evaluation environment is deliberate.            all three prover models (Goedel-Prover-V2-8B, DeepSeek-
The axiom-level audit in the main paper (Subsections: Re-             Prover-V2-7B, Kimina-Prover-7B) and all four benchmarks
ward Hacking Analysis, Potential Exploit Identification)              (MiniF2F, PutnamBench, PhysLeandata, LeanPhysBench);
shows that the Lean 4.9.0-era interface behaviour docu-               only the theorem statement, decomposition trajectory, and
mented by (Ren et al. 2025) admits proof declarations that            (where applicable) domain-specific library context are sub-
compile successfully, pass the standard source-level sorry            stituted into the template placeholders at inference time.
scan, and nonetheless depend on sorryAx. Compiler-verified
solve counts obtained under that toolchain therefore can-              Generator System Prompt
not be taken at face value without a kernel-level audit, and     1     You are an expert Lean4 theorem prover.
re-deriving every baseline within a single pinned and ex-        2     Given a theorem and a decomposition that
haustively audited environment is what makes the internal                  breaks it into tractable steps,
comparisons in this paper meaningful. Every result reported                produce a complete Lean4 proof.
in the main paper whole-proof sampling, BFS+CG, one-              3
shot decomposition, our reproduction of Prover Agent, and         4    THEOREM:
our framework is internal to this environment, uses identi-       5    {theorem}
cal frozen checkpoints, and varies only the inference-time        6
                                                                  7    DECOMPOSITION:
procedure.                                                        8    {decomposition}
Physlib library PhysLib is a Lean 4 support library intro-        9
                                                                 10    INSTRUCTIONS:
duced alongside LeanPhysBench in Lean4Physics (Li et al.
                                                                 11    - You may use a <think>...</think> block
2025b). It formalizes standard physical units, dimensional                 for internal reasoning
constants, and the associated definitions against which the      12    - After the thinking block, output ONLY
benchmark’s theorem statements are written. Following the                  the raw Lean4 proof, no markdown
evaluation protocol of (Li et al. 2025b), we supply PhysLib                fences, no prose
as direct input context: the library is prepended to the theo-   13    - Start your Lean4 output directly with
rem statement within the prompt, rather than being exposed                 the theorem declaration or ‘by‘
through premise retrieval or an import mechanism.                14    - Use ‘have‘ statements to encode each
   We report LeanPhysBench results both with and without                   decomposition step as an intermediate
this context Table 7. The with-PhysLib condition matches                    goal
                                                                 15    - The proof must typecheck and close all
the setting used in the original benchmark evaluation and is               goals
the primary comparison; the no-PhysLib condition measures        16    - Do not output anything after the
how far a prover can proceed on physics formalizations with-               closing ‘done‘ or final tactic
out access to the domain-specific definitions its statements
     Critic System Prompt                               Decomposer Prompt
1    You are an expert Lean4 theorem proving     1      You are an expert Lean4 proof strategist.
         evaluator.                              2      You will be given a theorem and
2    You will be given:                                     optionally a list of decomposition
3    1. A main Lean4 theorem to prove                       steps already planned.
4    2. A decomposition trajectory of prior      3      Your task is to output the single most
         steps (if any)                                     useful NEXT proof step.
5    3. A candidate next decomposition step to    4
          evaluate                                5     THEOREM:
6                                                 6     {theorem}
7    Rate the candidate step on how useful it     7     {prior_steps_block}
         is for making the main theorem           8
         provable.                                9     INSTRUCTIONS:
 8                                               10     - Output EXACTLY ONE next step, one
 9   Scoring criteria:                                      sentence, plain English
10   - Does it meaningfully reduce the proof     11     - The step must be a concrete proof-
         burden of the main theorem? (0-25 pts              structural move: an induction scheme,
         )                                                   a case split,
11   - Is it consistent with and builds on the   12       a key lemma to establish, a rewrite rule
           prior trajectory? (0-25 pts)                        to apply, or an algebraic
12   - Is it specific and immediately                         transformation
         actionable in Lean4? (0-25 pts)         13     - It must directly reduce what remains to
13   - Does it avoid redundancy with prior                   be proven
         steps? (0-25 pts)                       14     - Do NOT write Lean4 code or pseudocode
14                                               15     - Do NOT explain your reasoning
15   Score anchors:                              16     - Do NOT repeat prior steps
16   - 0-20: Irrelevant, wrong direction, or     17     - Do NOT state what the final answer is
         harmful to the proof                    18
17   - 21-40: Vaguely related but not            19     Valid examples:
         actionable                              20      "Apply induction on n, handling the base
18   - 41-60: Reasonable but generic or                       case n=0 and step case separately."
         partially useful                        21      "Rewrite the goal using the identity a^2
19   - 61-80: Clearly useful and directly                     - b^2 = (a-b)(a+b)."
         reduces proof burden                    22      "Case split on whether k is even or odd
20   - 81-100: Optimal next step, precise and                ."
         immediately actionable                  23      "Establish the auxiliary lemma that f(n)
21                                                            is monotone increasing, then apply
22   Theorem: {theorem}                                      it to bound the sum."
23   Trajectory: {trajectory}                    24      "Reduce to showing divisibility by
24   Candidate step: {candidate_step}                        expressing the left side as a
25   Score:                                                  telescoping product."
                                                 25
                                                 26     Next step:

                                                      Example: A Potential Compiler Exploit
                                                      Listing     1     shows       a     representative     Agent
                                                      (critic+reward)                 proof        attempt        for
                                                      putnam_1997_b5 generated by DeepSeek-Prover-
                                                      V2-7B that was flagged by our audit protocol ((Subsections:
                                                      Reward Hacking Analysis, Potential Exploit Identification),
                                                      stated in the main paper). The proof compiles successfully
                                                      under the Kimina Lean server and superficially follows a
                                                      standard structure: a base case (h_base), an inductive
                                                      step (h_inductive), and a chain of trivial exact
                                                      forwarding (h_main, h_final) that gives the appearance
                                                      of a completed induction. Critically, however, the inductive
                                                      step’s proof obligation is discharged not through valid tactics
                                                      but through a cascade of try blocks that falls back to the
                                                      apply? tactic (highlighted, line 46) when omega and
                                                      simp_all fail to close the goal.
                                                         Following our audit protocol, we append an axiom check
                                                      to the compiled proof:
1    #print axioms putnam_1997_b5                                      33            <;> ring_nf at * <;> omega
     which returns:                                                    34       rw [h1]; rw [h2]
1    ’putnam_1997_b5’ depends on axioms: [propext                      35       have h3 : (2:Nat) ^ (2 ^ (tetration 2 (k
         , sorryAx, Classical.choice, Quot.sound]                                   - 1))) = 2 ^ (2 ^ (tetration 2 (k -
                                                                                    1))) := rfl
     The presence of sorryAx confirms that, despite compiling          36       have h4 : (2:Nat) ^ (2 ^ (tetration 2 (k
     without an explicit sorry token in the source and despite                      - 1))) = 2 ^ (2 ^ (tetration 2 (k -
     passing the Kimina server’s sorry-token scan, the proof                        1))) := rfl
     does not in fact close all goals apply? silently discharges       37       simp_all [Nat.ModEq, Nat.ModEq]
     an unproved obligation via the Lean 4.9.0 interface bug doc-      38       <;> (try omega) <;>
     umented in Ren et al. (2025), rather than genuinely estab-        39       (try { cases k with
     lishing the inductive step. Removing the flagged apply?           40             | zero => contradiction
     branch causes the proof to fail to compile, satisfying the sec-   41             | succ k =>
     ond criterion of our audit protocol ((Subsections: Reward         42               cases k with
                                                                       43               | zero => contradiction
     Hacking Analysis, Potential Exploit Identification), stated in    44               | succ k => simp_all [tetration,
     the main paper)) and confirming classification as a potential                          Nat.pow_succ, Nat.ModEq] <;>
     exploit.                                                                               omega }) <;>
     Listing 1: A DeepSeek-Prover-V2-7B proof attempt for              45       (try { simp_all [tetration, Nat.pow_succ,
     putnam_1997_b5 flagged as a potential exploit. Line 46                          Nat.ModEq] <;> omega }) <;>
                                                                       46       (try { apply? })
     shows the fallback apply? tactic responsible for the              47       <;> omega
     sorryAx dependency.                                               48
1    import Mathlib                                                    49     have h_main : forall k >= 2, tetration 2 k
2    def tetration : Nat -> Nat -> Nat                                              === tetration 2 (k-1) [MOD k] := by
3      | _, 0 => 1                                                     50       intro k hk
4      | b, (m + 1) => b^(tetration b m)                               51       induction’ hk with k hk ih
5                                                                      52       . norm_num [tetration, Nat.ModEq]
6    theorem putnam_1997_b5                                            53       . cases k with
7    (n : Nat)                                                         54         | zero => contradiction
8    (hn : n >= 2)                                                     55         | succ k =>
9    : tetration 2 n === tetration 2 (n-1) [MOD n                      56           cases k with
          ] := by                                                      57           | zero => norm_num [tetration, Nat.
10     have h_base : n = 2 -> tetration 2 n ===                                         ModEq] at *
            tetration 2 (n-1) [MOD n] := by                            58           | succ k =>
11       intro hn2                                                     59             have h1 := h_inductive (k + 2) (by
12       rw [hn2]                                                                         omega) ih
13       norm_num [tetration, Nat.ModEq]                               60             simp_all [tetration, Nat.ModEq]
14       <;> decide                                                    61             <;> omega
15                                                                     62
16     have h_inductive : forall k >= 2,                               63     exact h_main n hn
            tetration 2 k === tetration 2 (k-1) [
            MOD k]
17         -> tetration 2 (k+1) === tetration 2 k
                                                                                                    Datasets
                [MOD (k+1)] := by                                           We evaluate our framework on four publicly available Lean
18       intro k hk h                                                       4 theorem-proving benchmarks spanning competition math-
19       have h1 : tetration 2 (k + 1) = 2 ^ (                              ematics and college- to graduate-level physics.
              tetration 2 k) := by                                              MiniF2F (Zheng, Han, and Polu 2022) is a benchmark
20         rw [tetration]
21         <;> simp [Nat.add_comm, Nat.add_assoc,
                                                                            consisting of 244 test problems formalized in Lean 4. The
                Nat.add_left_comm]                                          problems are derived from international mathematics compe-
22         <;> induction k <;> simp_all [tetration                          titions, including the International Mathematical Olympiad
                , Nat.pow_succ]                                             (IMO), the American Invitational Mathematics Examina-
23         <;> ring_nf at * <;> omega                                       tion (AIME), and related contests. The benchmark covers
24      have h2 : tetration 2 k = 2 ^ (tetration                            a diverse range of mathematical domains, including alge-
              2 (k - 1)) := by                                              bra, number theory, geometry, inequalities, combinatorics,
25        cases k with                                                      induction, and analysis, making it a standard benchmark for
26        | zero => contradiction                                           evaluating formal theorem provers.
27        | succ k =>
28           cases k with
                                                                                PutnamBench (Tsoukalas et al. 2024) is a collection of
29           | zero => contradiction                                        formally verified problems compiled from the William Low-
30           | succ k =>                                                    ell Putnam Mathematical Competition. It contains challeng-
31             simp_all [tetration]                                         ing undergraduate-level mathematical theorems spanning al-
32             <;> simp_all [tetration, Nat.                                gebra, analysis, geometry, combinatorics, number theory, and
                   pow_succ]                                                linear algebra, providing a rigorous benchmark for assessing
mathematical reasoning and proof-generation capabilities.        ings, 625–635. Berlin, Heidelberg: Springer-Verlag. ISBN
   LeanPhysBench (Li et al. 2025b) is a benchmark of for-        978-3-030-79875-8.
mally verified college-level physics problems written in Lean    Dong, K.; and Ma, T. 2025. STP: Self-play LLM The-
4. The dataset covers multiple introductory and intermedi-       orem Provers with Iterative Conjecturing and Proving.
ate physics domains, including mechanics, oscillations and       arXiv:2502.00212.
waves, electromagnetism, thermodynamics, optics, and re-
lated topics. We evaluate both with and without the accom-       Feng, X.; Wan, Z.; Wen, M.; McAleer, S. M.; Wen, Y.;
panying PhysLib context following the benchmark protocol.        Zhang, W.; and Wang, J. 2024. Alphazero-like Tree-Search
   PhysLeanData (Zhang et al. 2026) is a large-scale Lean        can Guide Large Language Model Decoding and Training.
4 benchmark containing graduate-level theoretical physics        arXiv:2309.17179.
formalizations. The benchmark includes problems from ad-         First, E.; Rabe, M. N.; Ringer, T.; and Brun, Y. 2023. Baldur:
vanced domains such as classical particle mechanics, clas-       Whole-Proof Generation and Repair with Large Language
sical string theory, relativity, quantum mechanics, quan-        Models. arXiv:2303.04910.
tum field theory, and related areas, providing an out-of-        Gao, L.; Schulman, J.; and Hilton, J. 2022. Scaling Laws for
distribution evaluation setting for assessing the generaliza-    Reward Model Overoptimization. arXiv:2210.10760.
tion capability of theorem-proving systems.                      Gloeckle, F.; Limperg, J.; Synnaeve, G.; and Hayat, A. 2024.
                                                                 ABEL: Sample Efficient Online Reinforcement Learning for
            Conclusion and Limitations                           Neural Theorem Proving. In The 4th Workshop on Mathe-
We present a three-role MCTS framework that treats the Lean      matical Reasoning and AI at NeurIPS’24.
4 compiler purely as a reward oracle, this prevents compiler-    Gu, A.; Piotrowski, B.; Gloeckle, F.; Yang, K.; and
error content from accumulating in the generation context        Markosyan, A. H. 2025. ProofOptimizer: Training Language
as search depth increases. This keeps compiler-feedback          Models to Simplify Proofs without Human Demonstrations.
overhead constant with search depth. Under matched proof-        arXiv:2510.15700.
attempt budgets, our method outperforms whole-proof sam-
pling across four benchmarks spanning competition math-          Hao, S.; Gu, Y.; Ma, H.; Hong, J. J.; Wang, Z.; Wang, D. Z.;
ematics and graduate-level theoretical physics, reaching         and Hu, Z. 2023. Reasoning with Language Model is Plan-
87.1% on MiniF2F with Goedel-Prover-V2-8B at PAB@256,            ning with World Model. arXiv:2305.14992.
while consuming 32.8% fewer total inference tokens on av-        Ji, X.; Liu, Y.; Wang, Q.; Zhang, J.; Yue, Y.; Shi, R.; Sun, C.;
erage than the whole-proof baseline. Ablations show that         Zhang, F.; Zhou, G.; and Gai, K. 2025. Leanabell-Prover-V2:
both the temperature-decayed decomposer and the distribu-        Verifier-integrated Reasoning for Formal Theorem Proving
tion of a fixed budget across multiple MCTS iterations, rather   via Reinforcement Learning. arXiv:2507.08649.
than a single wide expansion, are responsible for these gains.   Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Li, W.; Liu, J.; Jamnik,
We also present an exhaustive axiom-level audit. We ran          M.; Lacroix, T.; Wu, Y.; and Lample, G. 2023. Draft, Sketch,
#print axioms on every successfully compiled proof               and Prove: Guiding Formal Theorem Provers with Informal
produced by all three prover models across all four bench-       Proofs. arXiv:2210.12283.
marks, methods, and budgets not only on proofs match-            Kaliszyk, C.; Urban, J.; Michalewski, H.; and Olšák,
ing previously reported lexical indicators. This audit shows     M. 2018. Reinforcement Learning of Theorem Proving.
that a substantial fraction of DeepSeek-Prover-V2-7B’s suc-      arXiv:1805.07563.
cesses on PutnamBench depend on sorryAx despite compil-
ing cleanly and passing the standard source-level sorry scan:    Lample, G.; Lachaux, M.-A.; Lavril, T.; Martinet, X.;
4 of 13 and 8 of 18 whole-proof successes at PAB@32 and          Hayat, A.; Ebner, G.; Rodriguez, A.; and Lacroix, T.
PAB@128, and 11 of 27 and 19 of 44 under our framework.          2022. HyperTree Proof Search for Neural Theorem Prov-
The underlying apply? interface behaviour was documented         ing. arXiv:2205.11491.
for Lean 4.9.0 by Ren et al. (2025); we confirm it persists      Li, Y.; Du, D.; Song, L.; Li, C.; Wang, W.; Yang, T.; and
under our pinned Lean 4.15.0 and Mathlib environment.            Mi, H. 2025a. HunyuanProver: A Scalable Data Synthesis
                                                                 Framework and Guided Tree Search for Automated Theorem
                       References                                Proving. arXiv:2412.20735.
Aniva, L.; Sun, C.; Miranda, B.; Barrett, C.; and Koyejo, S.     Li, Y.; Liu, M.; Wang, R.; Ji, W.; He, Z.; Pan, R.; Huang, J.;
2024. Pantograph: A Machine-to-Machine Interaction Inter-        Zhang, T.; and Fung, Y. R. 2025b. Lean4Physics: Compre-
face for Advanced Theorem Proving, High Level Reasoning,         hensive Reasoning Framework for College-level Physics in
and Data Extraction in Lean 4. arXiv:2410.16429.                 Lean4. arXiv:2510.26094.
Baba, K.; Liu, C.; Kurita, S.; and Sannai, A. 2026. Prover       Lin, H.; Sun, Z.; Welleck, S.; and Yang, Y. 2025a.
Agent: An Agent-Based Framework for Formal Mathemati-            Lean-STaR: Learning to Interleave Thinking and Proving.
cal Proofs. arXiv:2506.19923.                                    arXiv:2407.10040.
de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theorem           Lin, Y.; Tang, S.; Lyu, B.; Wu, J.; Lin, H.; Yang, K.; Li, J.;
Prover and Programming Language. In Automated Deduc-             Xia, M.; Chen, D.; Arora, S.; and Jin, C. 2025b. Goedel-
tion – CADE 28: 28th International Conference on Auto-           Prover: A Frontier Model for Open-Source Automated The-
mated Deduction, Virtual Event, July 12–15, 2021, Proceed-       orem Proving. arXiv:2502.07640.
Lin, Y.; Tang, S.; Lyu, B.; Yang, Z.; Chung, J.-H.; Zhao, H.;     Xin, H.; Ren, Z. Z.; Song, J.; Shao, Z.; Zhao, W.; Wang,
Jiang, L.; Geng, Y.; Ge, J.; Sun, J.; Wu, J.; Gesi, J.; Lu, X.;   H.; Liu, B.; Zhang, L.; Lu, X.; Du, Q.; Gao, W.; Zhu,
Acuna, D.; Yang, K.; Lin, H.; Choi, Y.; Chen, D.; Arora,          Q.; Yang, D.; Gou, Z.; Wu, Z. F.; Luo, F.; and Ruan, C.
S.; and Jin, C. 2025c. Goedel-Prover-V2: Scaling Formal           2024. DeepSeek-Prover-V1.5: Harnessing Proof Assistant
Theorem Proving with Scaffolded Data Synthesis and Self-          Feedback for Reinforcement Learning and Monte-Carlo Tree
Correction. arXiv:2508.03613.                                     Search. arXiv:2408.08152.
Nipkow, T.; Paulson, L. C.; and Wenzel, M. 2002. Is-              Xin, R.; Xi, C.; Yang, J.; Chen, F.; Wu, H.; Xiao, X.; Sun,
abelle/HOL: A Proof Assistant for Higher-Order Logic, vol-        Y.; Zheng, S.; and Shen, K. 2025. BFS-Prover: Scalable
ume 2283 of Lecture Notes in Computer Science. Springer-          Best-First Tree Search for LLM-based Automatic Theorem
Verlag.                                                           Proving. arXiv:2502.03438.
Poiroux, A.; Kuncak, V.; and Bosselut, A. 2025. LeanInter-        Yang, K.; Swope, A. M.; Gu, A.; Chalamala, R.; Song, P.; Yu,
act: A Python Interface for Lean 4.                               S.; Godil, S.; Prenger, R.; and Anandkumar, A. 2023. Le-
Polu, S.; Han, J. M.; Zheng, K.; Baksys, M.; Babuschkin,          anDojo: Theorem Proving with Retrieval-Augmented Lan-
I.; and Sutskever, I. 2022. Formal Mathematics Statement          guage Models. arXiv:2306.15626.
Curriculum Learning. arXiv:2202.01344.                            Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T. L.;
Polu, S.; and Sutskever, I. 2020. Generative Language Mod-        Cao, Y.; and Narasimhan, K. 2023. Tree of Thoughts:
eling for Automated Theorem Proving. arXiv:2009.03393.            Deliberate Problem Solving with Large Language Models.
                                                                  arXiv:2305.10601.
Ren, Z. Z.; Shao, Z.; Song, J.; Xin, H.; Wang, H.; Zhao,
W.; Zhang, L.; Fu, Z.; Zhu, Q.; Yang, D.; Wu, Z. F.; Gou,         Zhang, H.; Wang, R.; Pan, R.; Wang, W.; Meng, B.; and
Z.; Ma, S.; Tang, H.; Liu, Y.; Gao, W.; Guo, D.; and Ruan,        Zhang, T. 2026. PhysProver: Advancing Automatic Theorem
C. 2025. DeepSeek-Prover-V2: Advancing Formal Mathe-              Proving for Physics. arXiv:2601.15737.
matical Reasoning via Reinforcement Learning for Subgoal          Zhang, J.; Wang, Q.; Ji, X.; Liu, Y.; Yue, Y.; Zhang, F.; Zhang,
Decomposition. arXiv:2504.21801.                                  D.; Zhou, G.; and Gai, K. 2025. Leanabell-Prover: Posttrain-
                                                                  ing Scaling in Formal Reasoning. arXiv:2504.06122.
Santos, M. D.; Wang, H.; de Saxcé, H.; Wang, R.; Baksys,
M.; Unsal, M.; Liu, J.; Liu, Z.; and Li, J. 2025. Kimina Lean     Zheng, K.; Han, J. M.; and Polu, S. 2022. MiniF2F: a cross-
Server: Technical Report. arXiv:2504.21230.                       system benchmark for formal Olympiad-level mathematics.
                                                                  arXiv:2109.00110.
Thakur, A.; Tsoukalas, G.; Wen, Y.; Xin, J.; and Chaudhuri,
S. 2024. An In-Context Learning Agent for Formal Theorem-
Proving. arXiv:2310.04353.
Tsoukalas, G.; Lee, J.; Jennings, J.; Xin, J.; Ding, M.; Jen-
nings, M.; Thakur, A.; and Chaudhuri, S. 2024. Putnam-
Bench: Evaluating Neural Theorem-Provers on the Putnam
Mathematical Competition. arXiv:2407.11214.
Wang, H.; Unsal, M.; Lin, X.; Baksys, M.; Liu, J.; San-
tos, M. D.; Sung, F.; Vinyes, M.; Ying, Z.; Zhu, Z.; Lu,
J.; de Saxcé, H.; Bailey, B.; Song, C.; Xiao, C.; Zhang, D.;
Zhang, E.; Pu, F.; Zhu, H.; Liu, J.; Bayer, J.; Michel, J.; Yu,
L.; Dreyfus-Schmidt, L.; Tunstall, L.; Pagani, L.; Machado,
M.; Bourigault, P.; Wang, R.; Polu, S.; Barroyer, T.; Li, W.-
D.; Niu, Y.; Fleureau, Y.; Hu, Y.; Yu, Z.; Wang, Z.; Yang,
Z.; Liu, Z.; and Li, J. 2025. Kimina-Prover Preview: To-
wards Large Formal Reasoning Models with Reinforcement
Learning. arXiv:2504.11354.
Wang, X.; Tian, M.; Zeng, Y.; Huang, Z.; Yuan, J.; Chen, B.;
Xu, J.; Zhou, M.; Liu, W.; Wu, M.; Guo, Z.; Qian, Q.; Wang,
Y.; Zhang, F.; Yin, R.; Dou, S.; Lv, C.; Chen, T.; Song, K.;
Tan, X.; Gui, T.; Zheng, X.; and Huang, X. 2026. Reward
Hacking in the Era of Large Models: Mechanisms, Emergent
Misalignment, Challenges. arXiv:2604.13602.
Wu, M.; Norrish, M.; Walder, C.; and Dezfouli, A. 2021.
TacticZero: Learning to Prove Theorems from Scratch with
Deep Reinforcement Learning. arXiv:2102.09756.
Wu, Z.; Huang, S.; Zhou, Z.; Ying, H.; Yuan, Z.; Zhang,
W.; Lin, D.; and Chen, K. 2025. InternLM2.5-StepProver:
Advancing Automated Theorem Proving via Critic-Guided
Search. arXiv:2410.15700.
