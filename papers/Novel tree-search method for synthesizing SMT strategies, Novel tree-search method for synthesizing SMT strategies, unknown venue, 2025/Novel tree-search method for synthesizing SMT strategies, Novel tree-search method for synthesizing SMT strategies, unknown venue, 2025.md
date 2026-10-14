Acta Informatica (2025) 62:28
https://doi.org/10.1007/s00236-025-00495-x

RESEARCH



Novel tree-search method for synthesizing SMT strategies

Zhengyang John Lu1 · Joel Day2 · Piyush Jha3 · Paul Sarnighausen-Cahn4 ·
Stefan Siemer4 · Florin Manea4,5 · Vijay Ganesh3


Received: 15 December 2024 / Accepted: 26 June 2025 / Published online: 4 August 2025
© The Author(s) 2025



Abstract
Modern SMT solvers, such as Z3, allow solver users to customize strategies to improve
performance on their specific use cases. However, handcrafting an optimized strategy for
a specific class of SMT instances remains a complex and demanding task for both solver
developers and users alike. In this paper, we address the problem of automated SMT
strategy synthesis via a novel method based on Monte-Carlo Tree Search (MCTS). We
formulate strategy synthesis as a sequential decision-making process, where the search
tree corresponds to the strategy space. Subsequently, we employ MCTS to navigate this
vast search space. Compared to the conventional MCTS, we introduce two heuristics—
layered and staged search—that enable our method to identify effective strategies with
lower costs. We implement our method, dubbed Z3alpha, upon the Z3 SMT solver. Our
experiments demonstrate that Z3alpha outperforms the default Z3 solver and the state-
of-the-art synthesis tool Fastsmt on the majority of the evaluated benchmark sets, while
producing more interpretable strategies than FastSMT. At SMT-COMP’24, among the 16
participating logics, Z3alpha improved upon the default Z3 in 12 cases and helped solve
hundreds more instances in QF_NIA and QF_NRA, winning their respective divisions.



1 Introduction

Satisfiability Modulo Theories (SMT) solvers [1] are key tools in diverse fields such as
software engineering [2], verification [3], security [4], and artificial intelligence [5]. It has
long been observed that no single solver excels across all instances from an SMT theory.
As a result, modern SMT solvers, such as Z3 [6], offer user-controllable strategies [7],
enabling users to customize a decision procedure for their own problem class. A strategy can
be considered an algorithmic recipe for selecting, sequencing, and parameterizing tactics.
Each tactic is a well-defined algorithmic proof rule or symbolic reasoning step, provided by
the solver. For example, propagate-values is a Z3 tactic that propagates equalities, while sat
and smt are the tactic wrappers of the main SAT and SMT solver in Z3. A strategy builds a
decision procedure by combining tactics, as shown in an example (if is-pb (then propagate-
values sat) smt). This strategy specifies a solving algorithm that, given an input instance,



Extended author information available on the last page of the article


                                                                                        13
28 Page 2 of 28                                                                       Z. J. Lu et al.


applies propagate-values followed by sat if the instance is a pseudo-boolean problem (as
checked using the built-in probe is-pb), or applies smt otherwise.
    Default solver strategies are typically optimized for well-established benchmarks, such
as those in the SMT-LIB library [8]. However, as the scope of SMT applications continues
to grow rapidly, users frequently encounter specialized, evolving, and unprecedented classes
of instances. In these scenarios, the default or existing strategies might not be as effective.
Consequently, there arises a need for new customized strategies, specifically designed to
efficiently address the unique challenges posed by users’ specific problems. Traditionally,
this task of strategy customization has been undertaken by human experts through extensive
experimentation and benchmark analysis. However, even with their expertise and efforts,
the task remains challenging due to the intricate interactions among tactics and the vast
search space for potential strategies.
    Early attempts have been made to automatically synthesize SMT strategies. For instance,
StratEVO [9] searches for an optimal strategy using evolutionary algorithms, while FastSMT
[10] synthesizes a tailored strategy using imitation learning and decision tree learning tech-
niques. While these methods show promise in automated strategy customization, they suffer
from issues such as unstable performance, limited interpretability, and extensive training
times.
    To address these issues, we introduce an automated SMT strategy synthesis method that
employs Monte-Carlo Tree Search (MCTS) [11, 12]. MCTS is a heuristic search algorithm,
widely applied in computer board game players as a lookahead planning algorithm. Its
prominence further escalated following its successful integration into the groundbreaking
deep reinforcement learning systems AlphaGo [13] and AlphaZero [14], where MCTS was
employed as a policy improvement operator. Recently, MCTS has shown remarkable suc-
cess as a standalone framework in addressing complex symbolic, combinatorial, or opti-
mization problems [15–17]. Its key strengths, including its ability to effectively balance
exploration and exploitation and its adaptiveness to the nuances of varied search problems,
make it an excellent method for such challenging tasks. Our work is the first to apply MCTS
to the SMT strategy synthesis problem.
    This work extends our IJCAI conference paper [18]. In particular, we included more
experimental details and results in Section 5; we added Section 6 to present our preparation
and result analysis of the SMT-COMP participation. Moreover, we expanded the literature
review in Section 2 and the methodology description in Section 4. Our code and data are
available at: https://github.com/JohnLyu2/z3alpha.

1.1 The strategy synthesis problem

The SMT strategy synthesis problem is defined as automatically identifying an optimal
strategy S ∗ that delivers the best performance for a given instance distribution Q, which is
of interest to the user. In practice, this goal is pursued by finding the best strategy SP∗ over
P, a representative finite subset of Q, with the expectation that SP∗ will generalize effectively
to Q. Performance is typically measured using metrics such as the number of instances suc-
cessfully solved within a specified timeout.
   It is important to note that due to the infinite nature of the strategy search space and the
empirical approach to strategy evaluation, finding a rigorously optimal solution is impracti-




13
Novel tree-search method for synthesizing SMT strategies                      Page 3 of 28 28


cal. Consequently, our objective is to discover a near-optimal solution within a reasonable
search time, based on empirical measurements.
   This research focuses on strategy synthesis for Z3, a solver that supports strategy cus-
tomization and is widely regarded as one of the most prevalent SMT solvers in use today.

1.2 Our contributions


1. Z3alpha, an MCTS-based Strategy Synthesizing Solver: We present Z3alpha, an
   MCTS-based framework for the SMT strategy synthesis problem. It automatically con-
   structs tailored solver strategies for a given class of problem instances. To the best of
   our knowledge, this is the first application of MCTS to SMT strategy synthesis.
2. Layered and Staged MCTS: To address the unique challenges inherent to strategy
   synthesis, that cannot be solved by the conventional MCTS alone, we develop two heu-
   ristics, namely, layered search and staged search on top of the MCTS framework. The
   layered search method effectively narrows the search space by treating certain auxiliary
   tasks as independent search problems. On the other hand, the staged search technique
   segments the entire search problem into sequential sub-problems, enabling the use of
   results from early stages to expedite the search in later stages. Together, these two tech-
   niques work symbiotically to enhance the search efficiency in finding the optimal strat-
   egy, an essential improvement given the time-consuming nature of strategy evaluations.
3. Extensive Experimental Evaluation: We implemented Z3alpha on top of Z3. To
   assess its performance, we conducted comprehensive experiments, comparing Z3al-
   pha with the state-of-the-art (SOTA) synthesis tool FastSMT, as well as Z3 ’s own
   handcrafted default strategy. These experiments spanned a broad spectrum, including
   instances from six different SMT logics, namely QF_{BV, LIA, LRA, NIA, NRA, S},
   representing a wide range of problem sizes and solver runtimes. Across the experi-
   ments, Z3alpha demonstrated strong performance, outperforming the default Z3 and
   FastSMT in the majority of cases, while producing more interpretable strategies than
   FastSMT.
4. SMT-COMP’24 Participation and Results: Z3alpha participated in SMT-COMP
   2024 (Single Query Track) as a derived solver based on Z3. Across the 16 participat-
   ing SMT logics, Z3alpha showed improved performance over the default Z3 strategy
   in 12 cases, while delivering similar results in the remaining four. The extent of these
   improvements depends on both the suitability of the default strategy for the benchmark
   set and the flexibility that the strategy language offers for each logic. For instance,
   Z3alpha solved 291 and 343 more benchmarks than Z3 in the QF_NIA and QF_NRA
   logics, respectively, earning first place in their corresponding divisions. In contrast,
   Z3alpha performed slightly worse than the default in logics QF_UFBV and QF_IDL. In
   Section 6, we present the details of our competition preparation and provide an in-depth
   analysis of the results.




                                                                                  13
28 Page 4 of 28                                                                     Z. J. Lu et al.


2 Related work

2.1 MCTS for symbolic/combinatorial problems

MCTS was initially developed for planning in board games [19]. Recently, there has been
a noticeable trend towards its application in solving symbolic and combinatorial problems.
For example, BaMCTS [16] and Symbolic Physics Learner [17] use MCTS to identify back-
doors in Mixed Integer Linear Programming (MIP) problems and to discover nonlinear
mathematical formulas for symbolic regression problems, respectively. KnuthSynthesis
[20] and AlphaMapleSAT [21] optimize branching and splitting heuristics in SAT solvers.
   For program synthesis, AlphaDev [22] is an MCTS-guided deep reinforcement learning
agent that synthesizes assembly programs. Remarkably, it has successfully discovered sort-
ing algorithms that surpass the best previously known human-designed ones. Unlike Alph-
aDev which considers the synthesis as sequencing individual instructions, our approach
represents strategy programs as expression trees. [23] introduced a learning-guided MCTS
method for the Syntax-Guided Synthesis (SyGuS) problem. Similar to our work, they framed
program synthesis as a Markov Decision Process within a context-free grammar (CFG).
Like AlphaDev, they adopted the AlphaZero [14] framework, where a deep neural network
guides the MCTS process. For our problem, the unique challenge of long program evaluation
makes it difficult to generate training data for the neural network during MCTS iterations.
Therefore, we employed a clean MCTS method with new heuristics, effectively addressing
the SMT strategy synthesis problem, without relying on neural-network guidance.

2.2 MCTS variants

It is a well-known problem that the basic MCTS method does not generalize well between
related states and actions. It results in a notably inefficient search in scenarios where the
search space is extensive. To counter this issue, various techniques have been proposed.
    One prevalent technique is the rapid action value estimation (RAVE) algorithm [24],
which incorporates an action-specific term QRAVE into the MCTS tree policy. Its basic
assumption is that there is an intrinsic value associated with each action regardless of its
position. Game abstraction [25] is another common technique, especially used in Poker,
to expedite the search. It abstracts similar actions or states into a single category to reduce
the search space. Option Monte Carlo Tree Search (O-MCTS) [26] uses options [27] in
the MCTS framework, to mimic the human behaviors of defining subgoals and subtasks in
game playings. An option is a predefined method for reaching a specific subgoal, with its
own policy and termination function. In O-MCTS, the agent selects among options instead
of actions.
    Our layered and staged search methods share similarities with the aforementioned MCTS
variants but also exhibit key distinctions. The layered search method reduces action and
state spaces, but, instead of abstracting, it separates certain auxiliary actions aside and
optimizes them in parallel. This separation generalizes values among subtrees, but, unlike
RAVE which shares values between actions in different positions, it merges subtrees. The
staged search, which chooses among previously found rewarding sub-solutions, is similar to
choosing among options, but without a separate predefined policy for each choice.




13
Novel tree-search method for synthesizing SMT strategies                        Page 5 of 28 28


2.3 Algorithm selection, scheduling, and configuration

The strategy synthesis problem, which we define in Section 1.1, is related to algorithm
selection and algorithm configuration. To clarify these relationships, we start with their
most common and narrow definitions: algorithm selection typically involves choosing, from
a set of off-the-shelf algorithms, the most suitable one for each given instance, while algo-
rithm configuration focuses on determining the best parameter settings that optimize per-
formance on an aggregated measure across a given set of instances. Examples of the former
include SATzilla [28], MachSMT [29], and Btor2-Select [30], while ParamILS [31] and
SMAC [32] are notable examples of the latter.
    The objective of our problem is to optimize an aggregated measure over a given instance
set, which is similar to the goal of algorithm configuration. However, our strategy space is
richer than the typical parameter space in algorithm configuration problems. The branching
functionality within the strategy language also implicitly supports per-instance selection of
different algorithms. Unlike typical algorithm selection, our problem selects from tactics, a
more granular and flexible algorithm space. Additionally, the try-for structure in the strat-
egy language enables algorithm scheduling [33], where rather than committing to a single
selected algorithm, a sequence of algorithms is arranged, each constrained by specific time
limits.
    The definition of algorithm configuration can also be expanded in a broader sense with
more flexible parameter space and problem settings, as described in a recent survey paper
[34]. In this broad view, algorithm selection is treated as a special case of per-instance algo-
rithm configuration, where the parameter space contains only one categorical parameter-
the target algorithm choice. Under this framework, our strategy synthesis problem can be
viewed as a per-set configuration task with a rich search space-strategies expressed by a
CFG.

2.4 SMT strategy synthesis

StratEVO and its variants [9, 35] present a pioneering effort in automated strategy genera-
tion, utilizing a genetic programming algorithm [36] to evolve strategies from a predefined
strategy population. Unfortunately, the StratEVO tool is not publicly available, which pre-
cludes us from conducting an empirical comparison.
   FastSMT [10], the SOTA tool in SMT strategy synthesis, employs a dual-phase learning
approach. First, it applies the imitation learning framework DAgger [37] to train a deep
neural network (DNN) that identifies a collection of branch-free strategies, each tailored
for certain instances. In the second phase, these strategies are synthesized into one uni-
fied strategy via an entropy-based decision-tree learning algorithm [38]. [39] proposed a
strategy-synthesis framework specifically for symbolic execution, whose methodology is
similar to FastSMT ’s. Our method also involves two steps. Different from the previous
work, we utilize MCTS for both steps. Compared to FastSMT, our method shows stronger
and more consistent empirical results across six tested SMT logics, as detailed in Section 5.
Further, the strategies synthesized by FastSMT are less interpretable, sometimes involving
more than a thousand branches.




                                                                                    13
28 Page 6 of 28                                                                      Z. J. Lu et al.


   Our earlier exploratory work, AlphaSMT [40], employs the AlphaZero framework to
adaptively select per-instance tactic sequences, achieving promising results on certain chal-
lenging benchmark sets. However, further development is needed for broader applicability.


3 Preliminaries

3.1 SMT solvers, SMT logics, and SMT-LIB

Satisfiability Modulo Theories (SMT) solvers determine the satisfiability of first-order logic
formulas, with the interpretation of symbols constrained by specific theories [41]. SMT-
LIB [8] refers to an international initiative aimed at facilitating research and development
in SMT solvers. The SMT-LIB initiative maintains a large library of SMT benchmarks,
grouped by various SMT logics. A logic consists of one or more theories with certain restric-
tions, and is named after such theories and restrictions. “QF" refers to the restriction to
quantifier-free formulas, “BV" refers to the theory of fixed-size bit-vectors, “S" refers to the
theory of strings and regular expressions, “IA" and “RA" refer to integer and real arithme-
tic. “L" before “IA" or “RA" means the linear fragment of these arithmetics, whereas “N"
represents the non-linear fragment. SMT-COMP [42] is an annually held competition that
arose from the SMT-LIB initiative for SMT solvers.

3.2 The Z3 strategy language

The Z3 SMT solver offers a user-controllable strategy language [7], allowing users to craft
their customized decision procedure algorithm. A strategy selects, sequences, and parame-
terizes tactics, where each tactic is a built-in reasoning step in Z3. The context-free grammar
(CFG) G for the strategy language we consider in this research is shown in Figure 1, where
variables are enclosed in angle brackets and terminals are italicized.
   The start symbol ⟨Strategy⟩ represents a strategy and is defined recursively. A strategy
may consist of a single tactic or a series of tactics linked in sequence by the combinator
then. Each tactic can be configured with a variety of parameters using the using-params
rule. The combinator or-else applies the second strategy if the first strategy fails, while the

Fig. 1 Context-free grammar
G of the Z3 strategy language
that we consider. Variables are
enclosed in angle brackets and
terminals are italicized




13
Novel tree-search method for synthesizing SMT strategies                         Page 7 of 28 28


combinator try-for makes the strategy fail if it does not return within the specified timeout
(in milliseconds). Z3 also provides built-in probes, which evaluate formula measures, e.g.,
the number of constants in the formula. Predicates over them can be built using relational
operators. The if combinator constructs branching strategies based on these predicates. We
refer readers to the official Z3 guide [43] for more information on the strategy language.
   Note that our considered strategy language G does not include some Z3 constructs (e.g.,
repeat), primarily for search-efficiency reasons. We argue that G effectively encapsulates
the core capabilities of the Z3 strategy language and can be easily extended with additional
constructs as needed.

3.3 Monte carlo tree search

Monte Carlo Tree Search (MCTS) is a best-first search technique. It searches for the optimal
decisions by estimating action values from numerous simulated trajectories. To search more
efficiently, the method biases simulations towards previously rewarding trajectories, yet it
maintains a balance by exploring less-visited paths as well. Alongside the simulations, an
MCTS tree is progressively constructed to store the action value estimations.
    Each MCTS simulation consists of 4 steps:

1. Selection: Starting from the root node, a tree-search policy traverses the MCTS tree
   until a leaf node is selected. The Upper Confidence Bounds applied for Trees (UCT)
   [44] is the most commonly used tree-search policy in MCTS. UCT balances exploiting
   the child node with the highest value estimation and exploring the less-visited children.
2. Expansion: The MCTS tree is expanded from the selected leaf node by adding child(ren)
   node(s) representing unexplored actions.
3. Rollout: If the selected leaf node is non-terminal, the simulation continues by subse-
   quently choosing actions according to a rollout policy (usually a random policy) until
   reaching a terminal state.
4. Backup: After evaluation, the episode reward is backed up to update the action values
   alongside the traversed tree path.


4 Methodology: MCTS for strategy synthesisis

4.1 Modeling strategy synthesis as an MDP

If we view strategy synthesis as constructing a strategy string from G by sequentially apply-
ing production rules to the leftmost variable, this process can be modeled as a deterministic
Markov Decision Process (MDP). An MDP is a mathematical framework in which an agent
makes action decisions in a series of states, with each action leading to a state transition. The
agent seeks to maximize rewards over time through choices of actions. In a deterministic
MDP, each action results in a deterministic state transition.
   In our formulation of the strategy synthesis problem, the states are the sentential strings
derived from G, while the actions are the production-rule applications. The entire process of
constructing a strategy is one single episode of the MDP. R denotes the performance mea-
sure of the synthesized strategy over the given benchmark set P. It is a reward received only


                                                                                     13
28 Page 8 of 28                                                                      Z. J. Lu et al.


at the terminal step T during an episode, and thus, also serves as the episode return (sum of
rewards) for our MDP.
    Our reward system prioritizes strategies that solve the highest number of instances
within a specified time limit. Simultaneously, when two strategies solve a close number of
P-instances, we want to steer the search towards the faster strategy. To embody these goals,
we base our reward on the PAR-10 score over P. PAR-10 computes the average runtime for
successfully solved instances and imposes a penalty for unsolved instances. The penalty is
equal to the timeout value multiplied by a factor of 10.
    With this modeling, the MDP search tree represents the strategy space, and the objective
becomes identifying the search-tree path with the highest reward R, which corresponds to
the optimal strategy SP∗ for P.

4.2 The MCTS framework for strategy synthesis

We instantiate MCTS for this optimal strategy search problem defined in Section 4.1. We
use UCT as the tree policy in the selection phase and rollout randomly in the rollout phase.
Notably, in the backup phase, we apply the max-backup rule [45]. This approach updates
the action values with the best observed return, rather than the average. It encourages more
aggressive exploitation towards the previously best-performing strategy, aligning with our
goal.
    Therefore, the MCTS method continuously runs simulations, and in each simulation, the
agent explores and assesses a single strategy, updating and retaining the best strategy seen
so far. The MCTS stops when a simulation budget is reached, either in the number of simu-
lation runs or in total search time. At the end of MCTS, the highest-reward strategy found
during the process is identified as the synthesized SMT strategy for the specified instance
set P.
    Figure 2 illustrates our basic MCTS framework, using a simplified CFG G′ for illustra-
tive purposes. G′ is defined as {⟨S⟩ → ⟨T⟩ ⟨S⟩ | smt, ⟨T⟩ → aig | simplify}, where ⟨S⟩ and
⟨T⟩ symbolize variables for strategy and tactic, respectively.
    The primary challenge in strategy synthesis through this conventional MCTS method is
the extensive time required to evaluate each strategy, which involves calling an SMT solver
on all instances in P. This leads to a very limited exploration of potential paths, particularly
given the immense search space created by the rich strategy language. To address this issue,
we first add domain-knowledge rules restricting valid actions. For example, no tactic could
be applied sequentially following a solver tactic such as smt. Such rules are documented
in Section 4.5. More importantly, we introduce two heuristic methods, namely the layered
search and the staged search, on top of the conventional MCTS, facilitating a deeper and
more effective exploration of the strategy space. These methods are described in Section 4.3
and Section 4.4, respectively.

4.3 Layered search

To solve the aforementioned challenge, we propose a layered search method for tactic-
parameter optimization. As shown in our CFG G, each tactic can be paired with multiple
parameters. For example, there is a Boolean parameter som for the tactic simplify that speci-
fies whether to put polynomials in sum-of-monomials form in this simplification. Another


13
Novel tree-search method for synthesizing SMT strategies                                Page 9 of 28 28




Fig. 2 Illustration of the MCTS framework for strategy synthesis




Fig. 3 Comparison of the conventional MCTS and the layer-search in treating tactic parameter tuning


example is an integer-type parameter max_degree that sets the max degree of algebraic
numbers processed by simplify.
   Using conventional MCTS with the grammar G, the selection of each candidate value
for a parameter, such as choosing True for som, is represented by one production rule.
The agent must make sequential production-rule decisions to configure all parameters for a
given tactic, leading to exponential growth in the problem search tree in terms of the number
of tuneable parameters. As illustrated in Figure 3(a), the two options for som and the three




                                                                                             13
28 Page 10 of 28                                                                      Z. J. Lu et al.


options for max_degree result in a six-fold expansion of the search tree for a single applica-
tion of simplify.
   To address this issue, our layered search method approaches the tuning of each parameter
as a separate Multi-Armed Bandit (MAB) problem [46]. As shown in Figure 3(b), the two
parameters som and max_degree for this simplify are modeled as two MABs respectively.
Each arm in the MAB represents one candidate value. For example, arm 16, 32, and 64 in
the MAB max_degree are three pre-selected candidate values for max_degree. Note that the
parameter MABs are associated with a tree edge, corresponding to one specific application
of a tactic, not to this tactic in general. For instance, simplify may be applied serval times in
the strategy building. For each application, there will be two MABs representing the tuning
of som and max_degree associated with it.
   One key point is that these parameter-tuning MABs are not part of the main MCTS tree.
They are engaged to select parameter values when their associated tree edge is traversed,
and they are updated based on the episode reward during the Backup phase. However, such
MABs do not expand the MCTS search tree after the parameter configuration, since they are
separate components from the main search tree, as shown in Figure 3(b). This is in contrast
to conventional MCTS, which also employs MAB principles to select among children nodes
to explore, where these nodes constitute part of the search tree, as the example shown in
Figure 3(a).
   The rationale behind the layer search is twofold. Firstly, tactics such as simplify may
have dozens of parameters, and it is common for a tactic to be used multiple times within
a strategy. Thus, navigating a search space that is fully expanded by all possible parameter
combinations becomes impractical, especially given the time-intensive nature of strategy
evaluation. Secondly, we argue that parameter tuning, although important, serves more as an
auxiliary task in comparison to the tasks of tactic selection and sequencing. By employing
the layered search method, we maintain the primary focus on the more important task. At
the same time, the isolated MABs efficiently optimize the parameters without overwhelm-
ing the main search process.

4.4 Staged search

While the layered search narrows down the search space, it does not alleviate the issue of
significant time consumption required for each simulation evaluation. To discover a com-
plex strategy, especially one involving nested branching, MCTS must expand over an enor-
mous space and delve deeply, often resulting in an impractically lengthy search time. This
is where the staged search comes into play.
    As shown in Figure 4, the staged search method divides the entire search process into
two stages. In the first stage, the MCTS focuses on finding n high-performing and comple-
mentary linear strategies, S1 , S2 ,..., and Sn (n is a predefined number; the linear-strategy
selection criterion is described later). Here, a linear strategy is defined as a sequence of
tactics without branching. Thus, MDP actions introducing branches are not considered in
this stage. In the second stage, the MCTS looks for a single best strategy SF that combines
the selected linear strategies. In other words, the second-stage MCTS works with the full
grammar G but restricts the actions so that every explored strategy is a combination of S1 ,
S2 ,..., and Sn through branching. By doing so, the key advantage is that the evaluation of the




13
Novel tree-search method for synthesizing SMT strategies                                Page 11 of 28 28




Fig. 4 The Staged MCTS Framework

combined strategies can be done speedily based on the cached performances of S1 , S2 ,...,
and Sn from the first stage, without additional costly SMT solver calls.
    This is possible because, when executing any branched strategy SB on a given instance f,
it can always be transformed into an equivalent finite sequence of branch-free (linear) strat-
egy applications, each paired with an assigned internal time limit. We denote this sequence as
     1 1        2 2
[(SB  , tB ), (SB , tB ), ..., (SB , tB )], where SB
                                 m m                 i
                                                         is the ith linear strategy in the sequence, and tm
                                                                                                          B
is the internal time limit assigned to SB (a “-” indicates that no internal timeout is assigned). For
                                             i

example, if we apply S ′ = ((if is-pb (or-else (try-for (then simplify sat) 4000) smt) smt))
to a pseudo-boolean instance, the execution path is first to try S 1 = (then simplify sat) for
                                                                                ′


4 seconds and, if failed, to execute S 2 = smt. This path is denoted as [(S 1 , 4), (S 2 , −)].
                                               ′                                            ′       ′


    Therefore, when evaluating SB over an input instance f, we first convert SB to its equiva-
                                         1 1         2 2
lent linear-strategy sequence [(SB         , tB ), (SB , tB ), ..., (SB  , tB )], where the performance of
                                                                       m m
                            1    2
each linear strategy SB , SB ,..., SB on f is known and cached during the first stage. Then,
                                           m

the performance of SB can be derived directly from these cached results without further
calls to the SMT solver. Referring to the example in the last paragraph, if we know that for
a pseudo-boolean instance f ′ , S 1 cannot solve it within 4 seconds while S 2 can solve it in
                                         ′                                                    ′

                                             ′
0.5 seconds, we can conclude that S solves f ′ in 4.5 seconds. This approach enables MCTS
to traverse a significantly larger search space in the second stage, facilitating the discovery
of effective complex strategies.
    Note that we may opt for a subset P1 of the complete training benchmark set P for the
first stage. This is because each first-stage MCTS simulation can be expensive for a large
training set. After selecting linear strategies using a smaller subset P1 in the first stage, we
can re-evaluate the selected strategies across all instances in P for the cached results to be
used in the second stage. This approach eliminates the resource-intensive need to evaluate
every first-stage exploration on the full set P, while still providing larger-scale evaluation
data for the second-stage MCTS.

4.4.1 Selection criteria for linear strategies

After the first-stage MCTS, we select n linear strategies for the second-stage synthesis. This
selection is performed iteratively from the pool of linear strategies explored in the first stage
using a greedy algorithm. The idea is to incrementally build a linear strategy portfolio that
collectively performs the best.
   Here, we define the virtual best strategy for a strategy set as an oracle that, for each
instance, perfectly selects the best strategy from the strategy set without any overhead.


                                                                                              13
28 Page 12 of 28                                                                      Z. J. Lu et al.


Then, in each round, the selection criterion is to select the linear strategy that, when added to
the incumbent selected strategy set, maximizes the performance of the virtual best strategy
for the training instance set. Starting from an empty set, we apply this criterion to add one
linear strategy at a time to the set until n strategies are selected, where n is the predefined
number of linear strategies to be selected.

4.4.2 Long time limit

One additional advantage of the staged search method is its adaptiveness to long time limits.
Strategy synthesis typically operates under short timeouts such as 10 seconds [10]. Increas-
ing the timeout linearly raises the total synthesis time, making it prohibitively costly to syn-
thesize strategies with extended timeouts, like 5 minutes or more, through direct evaluation.
   Our staged search method provides a practical approach to synthesizing strategies under
such extended timeouts. In the first stage, the linear strategy candidates are still selected
based on their performance with a short timeout period (e.g., 10 seconds), ensuring broad
exploration. Then, only the selected strategies are re-evaluated under the specified long
timeout (e.g., 5 minutes). The second-stage MCTS leverages these re-evaluation caches,
enabling the synthesis of customized strategies for these extended timeout scenarios.

4.5 Domain knowledge rules

To reduce the search space, we introduce additional domain-knowledge-based simplifica-
tion rules upon G. These rules are listed below:

1. We categorize tactics into two types: simplifiers and solvers. Simplifiers are not applied
   at the end of a sequence of tactic applications, while solvers are not applied in interme-
   diate steps.
2. Avoid using the try-for rule in a nested manner.
3. The if predicate only appears within depth three of the constructed strategy’s abstract
   syntax tree (AST). Moreover, the if rule is not applied after any tactic application, since
   tactic applications may alter the formula measures, disabling the staged search.
4. For continuous parameter settings, e.g., the try-for timeout, we preselect certain discrete
   values for selection.
5. Avoid applying the same theory-transformation tactics such as nla2bv more than once
   in a sequence of tactic applications.
6. Apply bit-blast only immediately after applying simplify.

We recognize that certain simplification rules might eliminate parts of the search space that
include effective strategies. Nevertheless, these rules are instrumental in substantially reduc-
ing the vast search space and enabling efficient search techniques like the stage search. Our
experimental results indicate that the remaining space still encompasses robust strategies.




13
Novel tree-search method for synthesizing SMT strategies                                  Page 13 of 28 28


5 Experiment design, results, and analysis

5.1 Experimental design

In this section, we evaluated Z3alpha across six logics, namely QF_{BV, NIA, NRA, LIA,
LRA, S}. We benchmarked our performance against the SOTA strategy synthesis tool,
FastSMT, as well as the default handcrafted strategy in Z3. cvc5 was also included as a
baseline for comparison. To assess the robustness of Z3alpha, we designed a series of exper-
iments tailored to different scenarios.

5.1.1 Experimental design for specific classes of benchmarks

Section 5.3.1 describes the experiment conducted on six specific SMT-LIB benchmark sets:
Sage2 (QF_BV), core (QF_BV), AProVE (QF_NIA), leipzig (QF_NIA), hycomp (QF_
NRA), and LassoRanker (QF_NRA), covering three different logics. The first five bench-
mark sets were also used in the FastSMT study. We additionally included LassoRanker, a
challenging QF_NRA benchmark set.
   For each benchmark set, we divided the instances into training and testing subsets. Since
the sizes of the benchmark sets vary significantly-from as few as 167 to as many as 7 436
instances-the train-test split ratios were not uniform. In particular, we avoided overly large
training sets to keep the synthesis time manageable. Nonetheless, we followed the general
principle of allocating a training set of sufficient size, typically comprising several hundred
instances. For the benchmark sets used in the FastSMT study, we adopted the same training/
testing splits as theirs. For LassoRanker, we randomly selected 500 instances for training
and used the remaining 321 for testing. The training and testing sizes for all sets are listed
in Table 1.



Table 1 Z3alpha vs. SOTA Solvers: Percentage (%) of instances solved from the selected SMT-LIB bench-
marks across six SMT logics (In each experiment, the result of the leading tool is highlighted in bold, while
the second-best is underlined)
Timeout(s) Logic       Benchmark Train Test        Z3alpha Z3alpha0 FastSMT Z3 cvc5 Z3str4
                                    Size Size
10          QF_BV Sage2             982 6444 52.9               41.3        51.3        37.1 36.6 –
                       core         402 270        99.6         99.6        100.0       75.6 82.6 –
                       entire logic 750 45441 86.9              –           78.0        85.3 85.1 –
            QF_NIA AProVE           697 1712 94.8               92.5        90.3        90.0 69.9 –
                       leipzig      99     68      91.2         89.1        88.2        89.7 25.0 –
                       entire logic 750 24693 67.4              –           63.2        62.2 35.7 –
            QF_        hycomp       770 1982 91.4               90.8        89.1        84.7 85.5 –
            NRA        LassoRanker 500 321         64.0         58.3        54.5        26.5 43.9 –
                       entire logic 750 11384 91.9              –           88.4        86.6 88.1 –
            QF_LIA entire logic 750 12476 76.2                  –           31.2        74.6 64.8 –
            QF_        entire logic 750 1003 73.6               –           74.0        71.0 63.6 –
            LRA
            QF_S       entire logic 750 18173 99.0              –           –           98.2 98.4 97.2
60          QF_BV Sage2             982 6444 69.8               –           67.7        57.7 77.8 –
300         QF_BV Sage2             982 6444 75.8               –           72.6        69.8 93.3 –


                                                                                                13
28 Page 14 of 28                                                                     Z. J. Lu et al.


   A 10-second timeout was chosen for evaluation, a common practice in the SMT strategy
synthesis research [9, 10]. Additionally, in this section, we included a version of our tool,
Z3alpha0, that did not employ staged search, for ablation study purposes.

5.1.2 Experimental design for benchmarks from diverse families

In Section 5.3.2, we extended our experiments to the full SMT-LIB benchmark sets for
the logics QF_{BV, NIA, NRA, LIA, LRA}, each comprising diverse problem families.
These experiments were intended to evaluate the versatility and adaptability of Z3alpha
in handling diverse problem families. For each logic, we randomly selected 750 SMT-LIB
instances for our training set, and utilized all remaining instances in the logic as our testing
set.

5.1.3 Experimental design for long time limits

In Section 5.3.3, we expanded our experiments to include long time limits, specifically
the 1-minute and 5-minute durations. These evaluations were conducted on the most chal-
lenging benchmark set, Sage2, from Section 5.3.1. Z3alpha synthesized new strategies for
long-timeout scenarios, using the method described in Section 4.4. To evaluate FastSMT ’s
performance for long time limits, we used the same strategy synthesized by FastSMT for the
10-second cases, as done in its original paper.

5.1.4 Experimental design for user-defined tactics

Z3 allows users to implement new tactics. Section 5.3.4 evaluated the capability of Z3alpha
in synthesizing strategies that integrate both user-defined and built-in tactics. This experi-
ment targeted the QF_S logic. In recent years, our team implemented new string tactics,
such as the arrangement-based solver Z3str3 [47], the Length Abstraction Solver (LAS)
[48], and specialized rewrite rules for regular expressions [49] for string constraint prob-
lems. These tactics are in addition to the default Z3 sequence solver for the string theory.
Z3str4 [48] combines the aforementioned tactics using a meticulously handcrafted strategy.
In this experiment, we leveraged Z3alpha to construct a strategy using the same set of tactics
as in Z3str4 and then compared their performances. Z3alpha was trained on 750 randomly
chosen QF_S instances from SMT-LIB. The testing was conducted on all the remaining
18 173 instances in the logic.

5.2 Experimental setup

For each experiment, the instance sets for training and testing were completely separate.
Z3alpha, as well as FastSMT, synthesized strategies based on the training set while report-
ing experiment results on the testing set. The approach aligns with our problem statement,
which aims to synthesize a strategy based on a representative set P, that is expected to gen-
eralize effectively to instances from the same distribution.
   In each experiment, Z3alpha first selected n = 20 linear strategies from 800 first-stage
MCTS simulations. During the second stage with 300 000 simulations, Z3alpha searched
for the most effective strategy that combined these linear strategy candidates. The final


13
Novel tree-search method for synthesizing SMT strategies                      Page 15 of 28 28


synthesized strategy SF was the one with the lowest PAR-10 score during the second-stage
search. To keep a similar time budget, the non-staged-search version Z3alpha0 ran MCTS
for 1 000 simulations with the full CFG G, in search of the best strategy.

5.2.1 Competing solvers

In these experiments, Z3alpha was implemented in Python 3.10 and was integrated with
Z3-4.12.2. FastSMT was also integrated with the same version of Z3. Both tools constructed
their strategies from the identical tactic and parameter candidates, which is described in
Appendix A. For FastSMT, we kept the hyperparameters (e.g., number of iterations) the
same as in their paper [10]. For both Z3alpha and FastSMT, the synthesized strategies were
then executed by Z3 for evaluation. We also included Z3-4.12.2 and cvc5-1.0.5 as baseline
solvers. We compared Z3alpha ’s performance with FastSMT ’s in all other than the user-
defined-tactic experiment, since Z3str4 did not provide Python APIs for the user-defined
tactics that were required by FastSMT.

5.2.2 Computational environments

Both our synthesis and testing were conducted on a high-performance CentOS 7 cluster
equipped with Intel E5-2683 v4 (Broadwell) processors running at 2.10 GHz. All solver-
instance pairs were executed with one processor core and 1.5 GB of memory.

5.2.3 Variability

Both the Z3alpha and FastSMT algorithms involve randomization, leading to the possibil-
ity of synthesizing different strategies in separate runs. To account for this variability, the
results in Section 5.3.1 were average from five runs with different random seeds. Since
little variability was found in Section 5.3.1 and given the significantly higher computational
cost of the later experiments, we report results from only a single run from Section 5.3.2 to
Section 5.3.4.

5.3 Results and analysis

We present our experimental results in Table 1 and Table 2, showing the number of solved
instances and the PAR-2 score, respectively. These tables summarize results from various
experiment scenarios. Overall, Z3alpha showed strong performance across different sce-
narios. A detailed analysis of each scenario is provided below.

5.3.1 Results on specific families in QF_BV, QF_NIA, QF_NRA

The first part of Table 1 and 2 summarizes the results on the six specific benchmark sets:
Sage2, core, AProVE, leipzig, hycomp, and LassoRanker, across the QF_BV, QF_NIA, and
QF_NRA logics. Notably, Z3alpha surpassed the default Z3 strategy, as well as cvc5 in all
of these benchmark sets, achieving the leading position in five out of the six sets among all
tested tools. In the particularly challenging QF_BV benchmark set Sage2, Z3alpha excelled
by solving a 42.7% more instances than the default strategy did. Furthermore, Z3alpha


                                                                                   13
28 Page 16 of 28                                                                                Z. J. Lu et al.

Table 2 Z3alpha vs. SOTA Solvers: Average PAR-2 score on the selected SMT-LIB benchmarks across six
SMT logics (In each experiment, the result of the leading tool is highlighted in bold, while the second-best
is underlined)
Timeout(s) Logic Benchmark Train Test             Z3alpha      Z3al-     FastSMT Z3          cvc5 Z3str4
                                 Size Size                     pha0
10           QF_ Sage2           982 6444 11.01                12.97 11.30          13.68 14.02 –
             BV    core          402 270          1.06         1.14      0.89       6.08     5.21 –
                   entire logic 750 45441 2.84                 –         4.70       3.11     3.39 –
             QF_ AProVE          697 1712 1.27                 1.64      2.89       3.28     6.62 –
             NIA leipzig         99      68       2.13         2.58      2.87       2.63     15.72 –
                   entire logic 750 24693 7.58                 –         8.37       8.69     13.63 –
             QF_ hycomp          770 1982 1.90                 1.95      2.29       3.19     3.17 –
             NRA LassoRanker 500 321              8.69         9.46      10.51      15.54 12.74 –
                   entire logic 750 11384 1.87                 –         2.58       2.80     2.71 –
             QF_ entire logic 750 12476 5.23                   –         13.88      5.52     7.61 –
             LIA
             QF_ entire logic 750 1003 5.93                    –         5.92       6.46     7.74 –
             LRA
             QF_S entire logic 750 18173 0.41                  –         –          0.57     0.42 0.71
60           QF_ Sage2           982 6444 43.57                –         43.82      57.41 38.77 –
             BV
300          QF_ Sage2           982 6444 163.26               –         181.00     214.23 80.71 –
             BV



Table 3 Average synthesis time (in minutes) for Z3alpha and FastSMT in the Section 5.3.1 experiments.
Solver-instance executions were run in parallel, with batches of 50 instances
                  Z3alpha                                              FastSMT
                  Stage 1     Caching        Stage 2       Total       Learning Synthesis    Total
Sage2             351.3       62.9           72.5          486.7       273.4    247.4        520.7
core              369.7       11.0           52.7          433.4       276.4    122.0        398.4
AProVE            213.7       26.9           52.5          293.1       630.2    129.3        759.6
leipzig           68.6        4.6            19.8          93.0        140.8    28.7         169.5
hycomp            180.8       39.3           67.2          287.3       743.8    81.4         825.3
LassoRanker       320.8       36.9           39.2          396.8       711.0    290.7        1001.7


outperformed Z3alpha0 across all benchmarks, underscoring the effectiveness of the staged
search.
   As shown in Table 3, the synthesis time for Z3alpha was on par with, and in five out of
six experiments, less than the FastSMT ’s. For instance, while the strategy synthesis for
AProVE took 759.6 minutes for FastSMT, Z3alpha completed the task in 293.1 minutes.

5.3.2 Results on full SMT-LIB QF_{BV, NIA, NRA, LIA, LRA}

Z3alpha also demonstrated solid performance on the full SMT-LIB benchmarks across these
logics. It consistently outperformed Z3, solving 8.4% more instances than the default strat-
egy on QF_NIA. While FastSMT solved four more instances than Z3alpha in QF_LRA, it
solved fewer instances than the default Z3 strategy on both QF_BV and QF_LIA.




13
Novel tree-search method for synthesizing SMT strategies                      Page 17 of 28 28


5.3.3 Results on QF_BV with long time limit

The results for the experiments of 1-minute-timeout and 5-minute-timeout are shown in
the tables as well. In every scenario, Z3alpha continued to maintain superior performance
compared to both FastSMT and Z3. The performance advantage over FastSMT slightly
increased when the timeouts were extended. However, an important shift was the signifi-
cantly better performance of cvc5 over the Z3-based methods for Sage2 under long time-
outs. This suggests a promising future research direction of extending the strategy synthesis
method across different solvers.

5.3.4 Results on QF_S with user-defined tactics

The test results for Z3alpha with user-defined QF_S tactics are shown in the QF_S row
of Table 1 and 2. Z3alpha demonstrated superior performance over all baseline solvers.
Interestingly, the handcrafted Z3str4 strategy, despite employing the same tactic portfolio
as Z3alpha, performed worse than the default Z3 strategy. The under-performance could be
attributed to two factors: (1) the Z3str4 strategy was optimized for logics including both
QF_S and QF_SLIA, which could be sub-optimal for QF_S alone; (2) the tuning of the
Z3str4 strategy was carried out on an earlier version of Z3. These observations underscore
the value of automated strategy customization, in terms of tailoring for specific problem
contexts and adapting to solver versions.

5.3.5 Strategy interpretability

A key distinction between the strategies synthesized by Z3alpha and FastSMT is that Z3al-
pha outputs shorter and more interpretable strategies. In Table 4, we compare the number of
branches in the strategies synthesized by the two tools in different experiments. A branch,
in this context, is introduced by either an if statement or a try-out construct. We found while
Z3alpha strategies have less or equal to five branches, FastSMT strategies can have hun-
dreds or even over a thousand branches, making them difficult to comprehend.




Table 4 Number of branches in                                Z3alpha                 FastSMT
the best strategy synthesized by
                                     Sage2                   3                       60
Z3alpha and FastSMT
                                     core                    3                       6
                                     AProVE                  3                       1093
                                     leipzig                 3                       55
                                     hycomp                  5                       42
                                     LassoRanker             4                       10
                                     QF_BV                   3                       35
                                     QF_NIA                  4                       26
                                     QF_NRA                  4                       609
                                     QF_LIA                  4                       903
                                     QF_LRA                  3                       262


                                                                                   13
28 Page 18 of 28                                                                                                                       Z. J. Lu et al.


6 SMT-COMP 2024 preparation and results

Z3alpha1 participated in the Single Query Track (formerly the main track) at SMT-COMP
2024 [50] as a derived solver based on Z3-4.13.0. Within the Single Query Track, there are
multiple competitive divisions, each consisting of benchmarks from a specific group of
SMT logics. For example, the QF_Strings division includes benchmarks from three log-
ics: QF_S, QF_SLIA, and QF_SNIA. Z3alpha entered the competition in divisions Bitvec,
QF_Bitvec, QF_Datatypes, QF_Equality, QF_Equality+Bitvec, QF_LinearIntArith,
QF_LinearRealArith, QF_NonLinearIntArith, QF_NonLinearRealArith, and
QF_Strings.

6.1 Strategy synthesis

For the competition, we synthesized one customized strategy for each participating logic.
The SMT-COMP benchmarks are selected from the SMT-LIB library [8], based on crite-
ria such as excluding overly simple instances, capping the number of instances per divi-
sion, and ensuring that a subset of newly submitted benchmarks is included when available.
Therefore, our synthesis was based on training instance sets drawn from SMT-LIB.
    It is worth noting that the benchmark sizes for different logics in SMT-LIB vary signifi-
cantly. For instance, QF_BV contains tens of thousands of benchmarks, whereas QF_UFDT
includes only about 200. Our general approach was to include as many benchmarks as
possible in the training set. However, for logics with a large number of challenging bench-
marks, such as QF_BV, we selected a challenging subset for training to maintain practical-
ity. The training sizes for each participating logic are provided in Table 5.
    While SMT-COMP imposes a wall-clock time limit of 20 minutes, due to constraints on
preparation time and resources, we synthesized strategies with a 5-minute timeout setting
and extrapolated them for our competition submissions.
    We spread the synthesis tasks for various logics across three clusters: Cedar2 (nodes
of Intel Platinum 8260 Cascade Lake@2.4GHz) and Graham3 (nodes of Intel E5-2683 v4
Broadwell@2.1GHz) from the Digital Research Alliance of Canada, and GWDG Scientific
Compute Cluster4 (nodes of Intel Cascadelake 9242).
    All of our synthesized competition strategies can be found at: ​h​t​t​p​s​:​/​/​g​i​t​h​u​b​.​c​o​m​/​J​o​h​n​L​
y​u​2​/​z​3​a​lp​ ​h​a​​​​.​​

6.2 SMT-COMP results

The Single Query Track of SMT-COMP 2024 was run on the VerifierCloud5 cluster owned
by the Software and Computational System Lab (SoSy-Lab) at LMU Munich. The competi-
tion runs were managed by BenchExec [51], with each solver assigned to a dedicated Intel


1
 The solver submission is named “Z3-alpha", following the SMT-COMP naming convention for derived
tools.
2
    https://docs.alliancecan.ca/wiki/Cedar
3
    https://docs.alliancecan.ca/wiki/Graham
4
    https://gwdg.de/en/hpc/systems/scc/
5
    ​h​t​t​p​s​:​​/​/​v​c​l​​o​u​d​.​s​o​​s​y​-​l​​a​b​.​o​r​​g​/​c​p​a​​c​h​e​c​k​e​​r​/​w​e​​b​c​l​i​e​n​t​/​m​a​s​t​e​r​/​i​n​f​o


13
Novel tree-search method for synthesizing SMT strategies                                                                                  Page 19 of 28 28

Table 5 Official SMT-COMP re-                            Logic                   Train       Comp          Z3alpha              Z3          Winner
sults: Correctly solved instances                                                Size        Size
across participating logics
                                                         BV                      1335        1040         800                  792   952 (cvc5)
                                                         QF_BV                   564         10703        9020                 8919  10489
                                                                                                                                     (Bitwuzla)
                                                         QF_DT                   566         352          216                  213   218 (Algaroba)
                                                         QF_UFDT                 203         200          106                  103   163 (cvc5)
                                                         QF_AX                   551         300          300                  300   300 (Yices2)
                                                         QF_UF                   7503        3521         3521                 3520 3521 (Yices2)
                                                         QF_AUFBV                75          75           58                   55    64 (Bitwuzla)
                                                         QF_UFBV                 1510        300          231                  235   288 (Bitwuzla)
                                                         QF_IDL                  2528        1208         1047                 1050 1047
                                                                                                                                     (Z3alpha)
                                                         QF_LIA                  470         4825         4169                 3939 4514
                                                                                                                                     (OpenSMT)
                                                         QF_LRA                  503         595          550                  546   574
                                                                                                                                     (OpenSMT)
                                                         QF_RDL                  255         247          207                  207   213 (Yices2)
                                                         QF_NIA                  470         12274        9755                 9464 9755
                                                                                                                                     (Z3alpha)
                                                         QF_NRA                  564         3104         2813                 2470 2813
                                                                                                                                     (Z3alpha)
                                                         QF_S                    535         8867         8810                 8780 8853
                                                                                                                                     (Z3-Noodler)
                                                         QF_SLIA                 470         23722        20767                20394 23272
                                                                                                                                     (Z3-Noodler)


Xeon E3-1230 v5 @ 3.40 GHz processor with 4 cores. Every solver-benchmark execution
had a wall-clock time limit of 20 minutes and a memory limit of 30 GB.
   Table 5 presents the competition results for all 16 SMT logics in which we participated 6.
Z3alpha showed improved performance over the default Z3 strategy 7 in 12 out of 16 logics,
while delivering similar performance in the remaining four.
   It is worth noting that the training instances and competition instances inevitably had
some overlap, so certain positive results may partially stem from overfitting. Indeed, in
some logics, e.g., QF_UFDT, our training set included all the available SMT-LIB bench-
marks, meaning that the competition set may not have contained any truly unseen instances.
   That said, Z3alpha achieved large improvements in several logics where the training sets
were relatively small. For example, it solved 291 more instances in QF_NIA and 343 more
in QF_NRA than the default Z3, earning first place in both divisions. The relatively small
training-to-testing ratios in these cases reduce the likelihood that such gains resulted from
overfitting.
   In contrast, Z3alpha performed slightly worse than the default strategy in QF_UFBV and
QF_IDL, solving 4 and 3 fewer instances, respectively. These differences likely stem from
how well the default strategy fits the benchmark sets and the degree of flexibility that the
strategy language offers for each logic.

6
   Full results are available on the official SMT-COMP website: ​h​t​t​p​s​:​​​/​​/​s​m​​t​-​c​o​m​​p​.​g​i​t​​h​​u​b​.​​​i​o​/​2​​0​​2​4​/​r​e​​s​u​​l​t​​s​/​r​e​s​​u​
l​t​s​-​s​i​​n​g​l​e​-​q​u​e​r​y​/.
7
 Although Z3 did not officially compete, the SMT-COMP organizers included Z3-4.13.0 as a non-competing
solver to provide baseline performance data for comparison.


                                                                                                                                                   13
28 Page 20 of 28                                                                   Z. J. Lu et al.


   There are several differences between our synthesis settings and those used in SMT-
COMP. First, our training instances may differ slightly in distribution from the competition
benchmarks. This is due both to differences in the criteria used for sampling from SMT-
LIB and to the fact that the benchmarks were slightly scrambled for use in SMT-COMP.
Therefore, the SMT-COMP results can be viewed as evaluating our methods on slightly
out-of-distribution cases. Second, due to resource constraints, our strategies were custom-
ized for 5-minute timeouts, whereas the competition used a 20-minute limit. Third, our strat-
egies were not synthesized on the same hardware used for competition, and performance
discrepancies may arise from these hardware differences. These factors may help explain
why, in QF_UFBV and QF_IDL, Z3alpha solved slightly fewer instances compared to Z3.
Nevertheless, the improvements over the base solver across the majority of logics highlight
Z3alpha ’s effectiveness.


7 Conclusions and limitations

In this work, we present Z3alpha, an MCTS-based method for SMT strategy synthesis.
Z3alpha introduces layered and staged search heuristics upon the conventional MCTS
framework, enabling an effective and low-cost search within the expansive strategy space.
The effectiveness of Z3alpha was demonstrated by extensive experiments and the SMT-
COMP’24 participation. Across 16 SMT logics, Z3alpha successfully improved the default
Z3 strategies in most cases, synthesizing more effective and interpretable strategies than the
SOTA tool FastSMT.
    The extent of improvement achieved by Z3alpha varied across applications and logics.
For example, our methods effectively enhanced the default Z3 strategy on the QF_NIA
and QF_NRA SMT-LIB benchmarks, winning their respective SMT-COMP divisions. This
large improvement may be attributed to the availability of diverse tactics that enable the
synthesis of complementary strategies for these logics, as well as the default strategy being
less tuned for these benchmarks. In contrast, for logics such as QF_UFBV and QF_IDL,
Z3alpha performs slightly worse than the default Z3, where the default strategy may already
be well suited and fewer effective alternatives could be synthesized for the logics.
    Our method is currently implemented only on Z3, because other prominent solvers, like
cvc5, to the best of our knowledge, do not offer an interface to group preprocessing and
solving steps flexibly. We hope our positive empirical results will encourage a universal
user-controllable strategy language in the SMT community. There is substantial potential
to further enhance solver performance by applying our method across tactics from different
solvers, thereby leveraging their complementary strengths.




13
Novel tree-search method for synthesizing SMT strategies   Page 21 of 28 28

Table 6 Selected tactic and pa-      Tactic                  Parameter
rameter candidates for QF_BV
                                     simplify                elim_and
                                                             blast_distinct
                                                             local_ctx
                                                             som
                                                             flat
                                                             pull_cheap_ite
                                                             hoist_mul
                                                             push_ite_bv
                                     propagate-values        push_ite_bv
                                     ctx-simplify            –
                                     elim-uncnstr            –
                                     solve-eqs               –
                                     purify-arith            –
                                     max-bv-sharing          –
                                     aig                     –
                                     reduce-bv-size          –
                                     ackermannize_bv         –
                                     bit-blast               –
                                     smt                     random_seed
                                     sat                     –
                                     qfbv                    –




                                                                13
28 Page 22 of 28                                               Z. J. Lu et al.

Table 7 Selected tactic and pa-   Tactic              Parameter
rameter candidates for QF_NIA
                                  simplify            elim_and
                                                      blast_distinct
                                                      local_ctx
                                                      som
                                                      flat
                                                      hi_div0
                                                      pull_cheap_ite
                                                      hoist_mul
                                                      push_ite_bv
                                  propagate-values    push_ite_bv
                                  ctx-simplify        –
                                  elim-uncnstr        –
                                  solve-eqs           –
                                  max-bv-sharing      –
                                  nla2bv              nla2bv_max_bv_size
                                  bit-blast           –
                                  smt                 random_seed
                                  qfnra-nlsat         inline_vars
                                                      factor
                                                      seed
                                  lia2card            –
                                  card2bv             –
                                  cofactor-term-ite   –
                                  qfnia               –




13
Novel tree-search method for synthesizing SMT strategies      Page 23 of 28 28

Table 8 Selected tactic and pa-      Tactic                Parameter
rameter candidates for QF_NRA
                                     simplify              elim_and
                                                           blast_distinct
                                                           local_ctx
                                                           som
                                                           flat
                                                           hi_div0
                                                           pull_cheap_ite
                                                           hoist_mul
                                                           push_ite_bv
                                     propagate-values      push_ite_bv
                                     ctx-simplify          –
                                     elim-uncnstr          –
                                     solve-eqs             –
                                     max-bv-sharing        –
                                     nla2bv                nla2bv_max_bv_size
                                     bit-blast             –
                                     smt                   random_seed
                                     qfnra-nlsat           inline_vars
                                                           factor
                                                           seed
                                     qfnra                 –



Table 9 Selected tactic and pa-      Tactic                  Parameter
rameter candidates for QF_LIA
                                     simplify                elim_and
                                                             blast_distinct
                                                             local_ctx
                                                             som
                                                             flat
                                                             pull_cheap_ite
                                                             push_ite_arith
                                                             hoist_ite
                                                             arith_lhs
                                     propagate-values        push_ite_bv
                                     ctx-simplify            –
                                     elim-uncnstr            –
                                     solve-eqs               –
                                     propagate-ineqs         –
                                     add-bounds              add_bound_lower
                                                             add_bound_upper
                                     normalize-bounds        –
                                     lia2pb                  lia2pb_max_bits
                                     smt                     random_seed
                                     qflia                   –




                                                                   13
28 Page 24 of 28                                                                                 Z. J. Lu et al.

Table 10 Selected tactic and pa-     Tactic                                                    Parameter
rameter candidates for QF_LRA
                                     simplify                                                  elim_and
                                                                                               blast_distinct
                                                                                               local_ctx
                                                                                               som
                                                                                               flat
                                     propagate-values                                          –
                                     ctx-simplify                                              –
                                     elim-uncnstr                                              –
                                     solve-eqs                                                 –
                                     smt                                                       random_seed
                                     qflra                                                     –



Table 11 Selected tactic and         Tactic                                                    Parameter
parameter candidates for QF_S
                                     simplify                                                  elim_and
                                                                                               blast_distinct
                                                                                               local_ctx
                                                                                               som
                                                                                               flat
                                     propagate-values                                          –
                                     ctx-simplify                                              –
                                     elim-uncnstr                                              –
                                     solve-eqs                                                 –
                                     ext_str                                                   –
                                     ext_strSimplify                                           –
                                     ext_strToRegex                                            –
                                     ext_strToWE                                               –
                                     arr                                                       –
                                     las                                                       –
                                     smt                                                       random_seed


Appendix A. Tactic and parameter pools

We list the pool of tactic and parameter candidates for each SMT logic in our Section 5
experiments from Tables 6, 7, 8, 9, 10 and 11. Note that the candidate selection was identical
for both Z3alpha and FastSMT.


Acknowledgements We thank Kate Larson, Arie Gurfinkel, and Mark Crowley for their valuable feedback;
the anonymous referees from AAAI’24, IJCAI’24, SMT’24, and Acta Informatica for their careful reviews
and many helpful suggestions; Kaihang Jiang for his contribution to code testing and data collection; and
the Digital Research Alliance of Canada for providing the computational resources and technical support.

Author contributions All authors contributed to the method development, experimental design, manuscript
writing, and manuscript reviewing. Z.L., P.J., and S.S. executed the experiments in Section 5. Z.L., P.S., and
S.S. executed the preparations for the SMT-COMP.

Funding Open Access funding enabled and organized by Projekt DEAL.



13
Novel tree-search method for synthesizing SMT strategies                                                                             Page 25 of 28 28

Data availability Our code and data are available at: https://github.com/JohnLyu2/z3alpha.

Declarations

Competing interests The authors declare no competing interests.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License,
which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as
you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons
licence, and indicate if changes were made. The images or other third party material in this article are
included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material.
If material is not included in the article’s Creative Commons licence and your intended use is not permitted
by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the
copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.




References
1.    De Moura, L., Bjørner, N.: Satisfiability modulo theories: introduction and applications. Commun.
      ACM 54(9), 69–77 (2011)
2.    Cadar, C., Ganesh, V., Pawlowski, P.M., Dill, D.L., Engler, D.R.: EXE: Automatically generating inputs
      of death. ACM Transactions on Information and System Security (TISSEC) 12(2), 1–38 (2008)
3.    Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The SeaHorn verification framework. In: Inter-
      national Conference on Computer Aided Verification, pp. 343–361 (2015). Springer
4.    Song, D., Brumley, D., Yin, H., Caballero, J., Jager, I., Kang, M.G., Liang, Z., Newsome, J., Poo-
      sankam, P., Saxena, P.: BitBlaze: A new approach to computer security via binary analysis. In: Informa-
      tion Systems Security: 4th International Conference, ICISS 2008, Hyderabad, India, December 16-20,
      2008. Proceedings 4, pp. 1–25 (2008). Springer
5.    Pulina, L., Tacchella, A.: Challenging SMT solvers to verify neural networks. AI Commun. 25(2), 117–
      135 (2012)
6.    De Moura, L., Bjørner, N.: Z3: An efficient SMT solver. In: International Conference on Tools and
      Algorithms for the Construction and Analysis of Systems, pp. 337–340 (2008). Springer
7.    De Moura, L., Passmore, G.O.: The strategy challenge in SMT solving. Automated Reasoning and
      Mathematics: Essays in Memory of William W. McCune, 15–44 (2013)
8.    Barrett, C., Fontaine, P., Tinelli, C.: The Satisfiability Modulo Theories Library (SMT-LIB). ​h​t​t​p​:​/​/​s​m​t​l​
      i​b​.​c​s​.​u​i​o​w​a​.​ed​ ​u​/i​​n​d​e​x​.​s​h​t​m​l​​​​. Accessed: 2024-01-16 (2016)
9.    Ramírez, N.G., Hamadi, Y., Monfroy, E., Saubion, F.: Evolving SMT strategies. In: 2016 IEEE 28th
      International Conference on Tools with Artificial Intelligence (ICTAI), pp. 247–254 (2016). IEEE
10.   Balunovic, M., Bielik, P., Vechev, M.: Learning to solve SMT formulas. In: Advances in Neural Infor-
      mation Processing Systems 31, pp. 10337–10348 (2018). ​h​t​t​p​:​/​​/​p​a​p​e​​r​s​.​n​i​p​​s​.​c​c​​/​p​a​p​e​​r​/​8​2​3​​3​-​l​e​a​r​​n​i​n​g​​-​t​o​-​s​​
      o​l​v​e​-​​s​m​t​-​f​o​​r​m​u​l​​a​s​.​p​d​f
11.   Coulom, R.: Efficient selectivity and backup operators in Monte-Carlo tree search. In: Herik, H.J., Cian-
      carini, P., Donkers, H.H.L.M. (eds.) Computers and Games, 5th International Conference, CG 2006,
      Turin, Italy, May 29-31, 2006. Revised Papers. Lecture Notes in Computer Science, vol. 4630, pp.
      72–83. Springer,??? (2006). https://doi.org/10.1007/978-3-540-75538-8_7
12.   Kocsis, L., Szepesvári, C.: Bandit based Monte-Carlo planning. In: Fürnkranz, J., Scheffer, T., Spilio-
      poulou, M. (eds.) Machine Learning: ECML 2006, 17th European Conference on Machine Learning,
      Berlin, Germany, September 18-22, 2006, Proceedings. Lecture Notes in Computer Science, vol. 4212,
      pp. 282–293 (2006). https://doi.org/10.1007/11871842_29
13.   Silver, D., Huang, A., Maddison, C.J., Guez, A., Sifre, L., Van Den Driessche, G., Schrittwieser, J.,
      Antonoglou, I., Panneershelvam, V., Lanctot, M., et al.: Mastering the game of Go with deep neural
      networks and tree search. nature 529(7587), 484–489 (2016)
14.   Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai, M., Guez, A., Lanctot, M., Sifre, L., Kuma-
      ran, D., Graepel, T., et al.: Mastering chess and shogi by self-play with a general reinforcement learning
      algorithm. arXiv preprint arXiv:1712.01815 (2017)




                                                                                                                                             13
28 Page 26 of 28                                                                                  Z. J. Lu et al.

15. Zhang, Z., Ernst, G., Sedwards, S., Arcaini, P., Hasuo, I.: Two-layered falsification of hybrid systems
    guided by Monte Carlo tree search. IEEE Trans. Comput. Aided Des. Integr. Circuits Syst. 37(11),
    2894–2905 (2018)
16. Khalil, E.B., Vaezipoor, P., Dilkina, B.: Finding backdoors to integer programs: a Monte Carlo tree
    search framework. In: Proceedings of the AAAI Conference on Artificial Intelligence, vol. 36, pp.
    3786–3795 (2022)
17. Sun, F., Liu, Y., Wang, J., Sun, H.: Symbolic physics learner: Discovering governing equations via
    Monte Carlo tree search. In: The Eleventh International Conference on Learning Representations, ICLR
    2023, Kigali, Rwanda, May 1–5, 2023 (2023). https://openreview.net/forum?id=ZTK3SefE8_Z
18. Lu, Z., Siemer, S., Jha, P., Day, J., Manea, F., Ganesh, V.: Layered and staged monte carlo tree search for
    smt strategy synthesis. In: Larson, K. (ed.) Proceedings of the Thirty-Third International Joint Confer-
    ence on Artificial Intelligence, IJCAI-24, pp. 1907–1915. International Joint Conferences on Artificial
    Intelligence Organization, Jeju Island, South Korea (2024). https://doi.org/10.24963/ijcai.2024/211.
    Main Track
19. Browne, C.B., Powley, E., Whitehouse, D., Lucas, S.M., Cowling, P.I., Rohlfshagen, P., Tavener, S.,
    Perez, D., Samothrakis, S., Colton, S.: A survey of Monte Carlo tree search methods. IEEE Transactions
    on Computational Intelligence and AI in games 4(1), 1–43 (2012)
20. Cameron, C., Hartford, J.S., Lundy, T., Truong, T., Milligan, A., Chen, R., Leyton-Brown, K.: UNSAT
    solver synthesis via Monte Carlo Forest Search. In: Dilkina, B. (ed.) Integration of Constraint Program-
    ming, Artificial Intelligence, and Operations Research - 21st International Conference, CPAIOR 2024,
    Uppsala, Sweden, May 28-31, 2024, Proceedings, Part I. Lecture Notes in Computer Science, vol.
    14742, pp. 170–189 (2024). https://doi.org/10.1007/978-3-031-60597-0_12
21. Jha, P., Li, Z., Lu, Z., Bright, C., Ganesh, V.: AlphaMapleSAT: An MCTS-based cube-and-conquer SAT
    solver for hard combinatorial problems. arXiv preprint arXiv:2401.13770 (2024)
22. Mankowitz, D.J., Michi, A., Zhernov, A., Gelmi, M., Selvi, M., Paduraru, C., Leurent, E., Iqbal, S.,
    Lespiau, J.-B., Ahern, A., et al.: Faster sorting algorithms discovered using deep reinforcement learning.
    Nature 618(7964), 257–263 (2023)
23. Parsert, J., Polgreen, E.: Reinforcement learning and data-generation for syntax-guided synthesis. In:
    Wooldridge, M.J., Dy, J.G., Natarajan, S. (eds.) Thirty-Eighth AAAI Conference on Artificial Intelli-
    gence, AAAI 2024, Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence, IAAI
    2024, Fourteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2014, February
    20-27, 2024, Vancouver, Canada, pp. 10670–10678 (2024). https://doi.org/10.1609/AAAI.V38I9.28938
24. Gelly, S., Silver, D.: Monte-Carlo tree search and rapid action value estimation in computer Go. Artif.
    Intell. 175(11), 1856–1875 (2011)
25. Johanson, M.: Measuring the size of large no-limit poker games. arXiv preprint arXiv:1302.7008 (2013)
26. De Waard, M., Roijers, D.M., Bakkes, S.C.: Monte Carlo tree search with options for general video
    game playing. In: 2016 IEEE Conference on Computational Intelligence and Games (CIG), pp. 1–8
    (2016). IEEE
27. Sutton, R.S., Precup, D., Singh, S.: Between MDPs and semi-MDPs: A framework for temporal abstrac-
    tion in reinforcement learning. Artif. Intell. 112(1–2), 181–211 (1999)
28. Xu, L., Hutter, F., Hoos, H.H., Leyton-Brown, K.: Satzilla: Portfolio-based algorithm selection for SAT.
    J. Artif. Intell. Res. 32, 565–606 (2008) https://doi.org/10.1613/jair.2490
29. Scott, J., Niemetz, A., Preiner, M., Nejati, S., Ganesh, V.: Machsmt: A machine learning-based algorithm
    selector for SMT solvers. In: Groote, J.F., Larsen, K.G. (eds.) Tools and Algorithms for the Construction
    and Analysis of Systems - 27th International Conference, TACAS 2021, Held as Part of the European
    Joint Conferences on Theory and Practice of Software, ETAPS 2021, Luxembourg City, Luxembourg,
    March 27 - April 1, 2021, Proceedings, Part II. Lecture Notes in Computer Science, vol. 12652, pp.
    303–325 (2021). https://doi.org/10.1007/978-3-030-72013-1_16
30. Lu, Z., Chien, P.-C., Lee, N.-Z., Gurfinkel, A., Ganesh, V.: Btor2-Select: Machine learning based
    algorithm selection for hardware model checking. In: Proc. CAV (2025). Springer
31. Hutter, F., Hoos, H.H., Leyton-Brown, K., Stützle, T.: ParamILS: an automatic algorithm configuration
    framework. Journal of artificial intelligence research 36, 267–306 (2009)
32. Hutter, F., Hoos, H.H., Leyton-Brown, K.: Sequential model-based optimization for general algorithm
    configuration. In: Learning and Intelligent Optimization: 5th International Conference, LION 5, Rome,
    Italy, January 17-21, 2011. Selected Papers 5, pp. 507–523 (2011). Springer
33. Kadioglu, S., Malitsky, Y., Sabharwal, A., Samulowitz, H., Sellmann, M.: Algorithm selection and
    scheduling. In: Principles and Practice of Constraint Programming–CP 2011: 17th International Con-
    ference, CP 2011, Perugia, Italy, September 12–16, 2011. Proceedings 17, pp. 454–469 (2011). Springer
34. Schede, E., Brandt, J., Tornede, A., Wever, M., Bengs, V., Hüllermeier, E., Tierney, K.: A survey of
    methods for automated algorithm configuration. Journal of Artificial Intelligence Research 75, 425–487
    (2022)


13
Novel tree-search method for synthesizing SMT strategies                                               Page 27 of 28 28

35. Ramírez, N.G., Monfroy, É., Saubion, F., Castro, C.: Improving complex SMT strategies with learning.
    Int. Trans. Oper. Res. 27(2), 1162–1188 (2020). https://doi.org/10.1111/ITOR.12650
36. Koza, J.R.: Genetic programming as a means for programming computers by natural selection. Stat.
    Comput. 4, 87–112 (1994)
37. Ross, S., Gordon, G., Bagnell, D.: A reduction of imitation learning and structured prediction to no-
    regret online learning. In: Proceedings of the Fourteenth International Conference on Artificial Intel-
    ligence and Statistics, pp. 627–635 (2011). JMLR Workshop and Conference Proceedings
38. Poole, D.L., Mackworth, A.K.: Artificial Intelligence: Foundations of Computational Agents. Cam-
    bridge University Press, Cambridge, UK (2010)
39. Chen, Z., Chen, Z., Shuai, Z., Zhang, G., Pan, W., Zhang, Y., Wang, J.: Synthesize solving strategy for
    symbolic execution. In: Proceedings of the 30th ACM SIGSOFT International Symposium on Software
    Testing and Analysis, pp. 348–360 (2021)
40. Lu, Z.: AlphaSMT: A reinforcement learning guided SMT solver. Master’s thesis, University of Water-
    loo (2023)
41. Kroening, D., Strichman, O.: Decision Procedures: An Alogorithm Point of View. Springer, Cham,
    Switzerland (2016)
42. Bobot, F., Bromberger, M., Hoenicke, J.: SMT-COMP 2023. https://smt-comp.github.io/2023/.
    Accessed: 2024-01-16 (2023)
43. Microsoft: Online Z3 Guide. https://microsoft.github.io/z3guide/. Accessed: 2024-01-16 (2023)
44. Kocsis, L., Szepesvári, C.: Bandit based monte-carlo planning. In: European Conference on Machine
    Learning, pp. 282–293 (2006). Springer
45. Sabharwal, A., Samulowitz, H., Reddy, C.: Guiding combinatorial optimization with UCT. In: Integra-
    tion of AI and OR Techniques in Contraint Programming for Combinatorial Optimzation Problems:
    9th International Conference, CPAIOR 2012, Nantes, France, May 28–June1, 2012. Proceedings 9, pp.
    356–361 (2012). Springer
46. Robbins, H.: Some aspects of the sequential design of experiments. Bull. Amer. Math. Soc. 58(5),
    527–535 (1952)
47. Berzish, M., Ganesh, V., Zheng, Y.: Z3str3: A string solver with theory-aware heuristics. In: 2017 For-
    mal Methods in Computer Aided Design (FMCAD), pp. 55–59 (2017). IEEE
48. Mora, F., Berzish, M., Kulczynski, M., Nowotka, D., Ganesh, V.: Z3str4: A multi-armed string solver.
    In: Formal Methods: 24th International Symposium, FM 2021, Virtual Event, November 20–26, 2021,
    Proceedings 24, pp. 389–406 (2021). Springer
49. Berzish, M., Kulczynski, M., Mora, F., Manea, F., Day, J.D., Nowotka, D., Ganesh, V.: An SMT solver
    for regular expressions and linear arithmetic over string length. In: International Conference on Com-
    puter Aided Verification, pp. 289–312 (2021). Springer
50. Bromberger, M., Bobot, F., Jonáš, M.: The 19th International Satisfiability Modulo Theories Competi-
    tion (SMT-COMP 2024). https://smt-comp.github.io/2024/. Accessed: 2024-10-17 (2024)
51. Beyer, D.: Reliable and reproducible competition results with benchexec and witnesses (report on SV-
    COMP 2016). In: Chechik, M., Raskin, J. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems - 22nd International Conference, TACAS 2016, Held as Part of the European Joint Confer-
    ences on Theory and Practice of Software, ETAPS 2016, Eindhoven, The Netherlands, April 2-8, 2016,
    Proceedings. Lecture Notes in Computer Science, vol. 9636, pp. 887–904 (2016). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​
    0​7​/9​ ​7​8​-​3​-​6​6​2​-​4​9​6​7​4​-​9​_​5​5​​​​

Publisher's Note Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations.




Authors and Affiliations

Zhengyang John Lu1 · Joel Day2 · Piyush Jha3 · Paul Sarnighausen-Cahn4 ·
Stefan Siemer4 · Florin Manea4,5 · Vijay Ganesh3

     Zhengyang John Lu
     john.lu2@uwaterloo.ca
     Florin Manea
     florin.manea@informatik.uni-goettingen.de


                                                                                                              13
28 Page 28 of 28                                                                            Z. J. Lu et al.

    Vijay Ganesh
    vganesh45@gatech.edu
    Joel Day
    j.day@lboro.ac.uk
    Piyush Jha
    piyush.jha@gatech.edu
    Paul Sarnighausen-Cahn
    paul.cahn@cs.uni-goettingen.de
    Stefan Siemer
    stefan.siemer@cs.uni-goettingen.de
1
    Electrical and Computer Engineering, University of Waterloo, 200 University Avenue West,
    Waterloo N2L 3G1, ON, Canada
2
    Department of Computer Science, Loughborough University, Epinal Way,
    Loughborough LE11 3TU, UK
3
    School of Computer Science, Georgia Tech, 266 Ferst Dr NW, Atlanta 30332, GA, USA
4
    Institute of Computer Science, University of Göttingen, Goldschmidtstraße, Göttingen 37077,
    Lower Saxony, Germany
5
    Campus Institute Data Science (CIDAS), University of Göttingen, Goldschmidtstraße,
    Göttingen 37077, Lower Saxony, Germany




13
