                                                                      Layered and Staged Monte Carlo Tree Search for
                                                                        SMT Strategy Synthesis (extended version)∗
                                                                    Zhengyang (John) Lu1 , Stefan Siemer2 , Piyush Jha3 ,
                                                                        Joel Day4 , Florin Manea2 and Vijay Ganesh3
                                                                                         1
                                                                                           University of Waterloo
                                                                                2
                                                                                  University of Göttingen and CIDAS
                                                                                   3
                                                                                     Georgia Institute of Technology
                                                                                      4
                                                                                        Loughborough University
                                                        john.lu2@uwaterloo.ca, stefan.siemer@cs.uni-goettingen.de, piyush.jha@gatech.edu,
arXiv:2401.17159v2 [cs.AI] 30 Apr 2024




                                                        j.day@lboro.ac.uk, florin.manea@informatik.uni-goettingen.de, vganesh@gatech.edu

                                                                      Abstract                                 ware engineering [Cadar et al., 2008], verification [Gurfinkel
                                                                                                               et al., 2015], security [Song et al., 2008], and artificial intelli-
                                                 Modern SMT solvers, such as Z3, offer user-
                                                                                                               gence [Pulina and Tacchella, 2012]. It has long been observed
                                                 controllable strategies, enabling users to tailor solv-
                                                                                                               that no single solver or algorithm excels across all instances
                                                 ing strategies for their unique set of instances, thus
                                                                                                               of a given SMT logic or of a problem class. As a result, mod-
                                                 dramatically enhancing the solver performance for
                                                                                                               ern SMT solvers, such as Z3 [De Moura and Bjørner, 2008],
                                                 their use case. However, this approach of strat-
                                                                                                               offer user-controllable strategies [De Moura and Passmore,
                                                 egy customization presents a significant challenge:
                                                                                                               2013], enabling users to customize a decision procedure for
                                                 handcrafting an optimized strategy for a class of
                                                                                                               their class of instances. A strategy can be thought of as an
                                                 SMT instances remains a complex and demanding
                                                                                                               algorithmic recipe for selecting, sequencing, and parameter-
                                                 task for both solver developers and users alike.
                                                                                                               izing tactics. Each tactic is a well-defined algorithmic proof
                                                 In this paper, we address this problem of automatic           rule or symbolic reasoning step, provided by the solver. For
                                                 SMT strategy synthesis via a novel Monte Carlo                example, propagate-values is a Z3 tactic that propagates
                                                 Tree Search (MCTS) based method. Our method                   equalities, while sat and smt are the tactic wrappers of the
                                                 treats strategy synthesis as a sequential decision-           main SAT and SMT solver in Z3. A strategy builds a de-
                                                 making process, whose search tree corresponds to              cision procedure by combining tactics, as shown in an ex-
                                                 the strategy space, and employs MCTS to navigate              emplar strategy (if is-pb (then propagate-values sat) smt).
                                                 this vast search space. The key innovations that              This strategy specifies a solving algorithm that, given an input
                                                 enable our method to identify effective strategies,           instance, applies propagate-values followed by sat if the in-
                                                 while keeping costs low, are the ideas of layered             stance is a pseudo-boolean problem (as checked using is-pb),
                                                 and staged MCTS search. These novel heuristics                or applies smt otherwise.
                                                 allow for a deeper and more efficient exploration of
                                                 the strategy space, enabling us to synthesize more               Default solver strategies are typically optimized for well-
                                                 effective strategies than the default ones in state-of-       established benchmarks, such as those in the SMT-LIB li-
                                                 the-art (SOTA) SMT solvers. We implement our                  brary [Barrett et al., 2016]. However, as the scope of SMT
                                                 method, dubbed Z3alpha, as part of the Z3 SMT                 applications continues to grow rapidly, users frequently en-
                                                 solver. Through extensive evaluations across six              counter specialized, evolving, and unprecedented classes of
                                                 important SMT logics, Z3alpha demonstrates su-                instances. In these scenarios, the default or the existing cus-
                                                 perior performance compared to the SOTA synthe-               tomized strategies might not be as effective. Consequently,
                                                 sis tool FastSMT, the default Z3 solver, and the              there arises a need for novel customized strategies, specif-
                                                 CVC5 solver on most benchmarks. Remarkably,                   ically designed to efficiently address the unique challenges
                                                 on a challenging QF BV benchmark set, Z3alpha                 posed by users’ specific problems. Traditionally, this task
                                                 solves 42.7% more instances than the default strat-           of strategy customization has been undertaken by human ex-
                                                 egy in the Z3 SMT solver.                                     perts through extensive experimentation and benchmark anal-
                                                                                                               ysis. However, even with their expertise and efforts, the task
                                                                                                               remains challenging due to the intricate interactions among
                                         1       Introduction                                                  tactics and the vast search space for potential strategies.
                                         Satisfiability Modulo Theories (SMT) solvers [De Moura and               Early attempts have been made to synthesize SMT strate-
                                         Bjørner, 2011] are key tools in diverse fields such as soft-          gies automatically. For instance, StratEVO [Ramı́rez et al.,
                                             ∗
                                              This paper is an extended version of our IJCAI 2024 paper with   2016] searches for an optimal strategy using evolutionary al-
                                         the same title. The code and data are available at: https://github.   gorithms, while FastSMT [Balunovic et al., 2018] synthe-
                                         com/JohnLyu2/z3alpha.                                                 sizes a tailored strategy using imitation learning and decision
tree learning techniques. While these methods show promise               stages to expedite the search in later stages. Together,
in automating strategy customization, they suffer from issues            these two techniques work symbiotically to enhance the
such as a lack of robustness, limited interpretability, and ex-          search efficiency and effectiveness in finding the opti-
tensive training times.                                                  mal strategy, an essential improvement given the time-
   To address these issues, we introduce a novel SMT strat-              consuming nature of strategy evaluations.
egy synthesis method that employs Monte Carlo Tree Search             3. Extensive Experimental Evaluation: We implemented
(MCTS). MCTS is a heuristic search algorithm, widely ap-                 our proposed method, dubbed Z3alpha, on top of the
plied in computer board game players as a lookahead plan-                leading SMT solver Z3. To assess its performance,
ning algorithm [Browne et al., 2012]. Its prominence further             we conducted comprehensive experiments, comparing
escalated following its successful integration into the ground-          Z3alpha with the state-of-the-art (SOTA) synthesis
breaking deep reinforcement learning systems AlphaGo [Sil-               tool FastSMT, as well as Z3’s own handcrafted de-
ver et al., 2016] and AlphaZero [Silver et al., 2017], where             fault strategy and the CVC5 solver. These experi-
MCTS was employed as a policy improvement operator.                      ments spanned a broad spectrum, including instances
Recently, MCTS has shown remarkable success as a stan-                   from six different SMT logics (namely, QF {BV, LIA,
dalone algorithm in solving complex symbolic or combinato-               LRA, NIA, NRA, S}), representing a wide range of
rial search problems, as evidenced in Khalil et al. [2022] and           problem sizes and solver runtimes. Across all ex-
Sun et al. [2023]. Its key strengths, including its ability to           periments, Z3alpha consistently demonstrated supe-
effectively balance exploration and exploitation and its adap-           rior and robust performance. This impressive perfor-
tiveness to the nuances of varied search problems, make it an            mance strongly highlights the benefits of automatic strat-
excellent method for such challenging tasks. Our work is the             egy customization, promoting broader adoption of user-
first to apply MCTS to the SMT strategy synthesis problem.               controllable strategies within the SMT community.
1.1   The Strategy Synthesis Problem
The SMT strategy synthesis problem is defined as automati-        2     Related Work
cally identifying an optimal strategy that yields the best per-   2.1     MCTS for Symbolic/Combinatorial Problems
formance for a given benchmark set P . This performance is
typically measured in terms of metrics such as the number of      MCTS has long been viewed as a powerful planning algo-
P -instances successfully solved within a specified wallclock     rithm for board games [Browne et al., 2012]. Recently,
timeout t. P is intended to be a representative subset of the     there has been a noticeable trend towards its application in
broader benchmark set Q, which is of interest to the user, with   solving symbolic and combinatorial problems. For instance,
the expectation that a strategy performing well on P general-     BaMCTS [Khalil et al., 2022], an MCTS-based method,
izes effectively to Q. It is important to note that due to the    has shown remarkable success in identifying backdoors in
infinite nature of the strategy search space and the empirical    Mixed Integer Linear Programming (MIP) problems. Sym-
approach to strategy evaluation, finding a rigorously optimal     bolic Physics Learner [Sun et al., 2023] uses MCTS to dis-
solution is impractical. Consequently, our objective is to dis-   cover nonlinear mathematical formulas for symbolic regres-
cover a near-optimal solution within a reasonable search time,    sion problems. Cameron et al. [2022] proposed an extension
based on empirical measurements. This research focuses on         to MCTS, Monte Carlo Forest Search (MCFS), which steers
strategy synthesis for Z3, a solver that is widely regarded as    the SAT branching policy. AlphaMapleSAT [Jha et al., 2024]
one of the most prevalent SMT solvers in use today.               is an MCTS-based cube-and-conquer SAT solver. AlphaDev
                                                                  [Mankowitz et al., 2023] is an MCTS-guided deep reinforce-
1.2   Our Contributions                                           ment learning agent that synthesizes assembly programs. Re-
 1. Z3alpha: An MCTS-based Strategy Synthesizing                  markably, it has successfully discovered sorting algorithms
    Solver: We present a novel MCTS-based framework,              that surpass the best previously known human-designed algo-
    dubbed Z3alpha, for the SMT strategy synthesis                rithms.
    problem, which automatically constructs tailored solver          Our work is, to the best of our knowledge, the first appli-
    strategies for a given class of problem instances. To the     cation of MCTS to address the SMT strategy synthesis prob-
    best of our knowledge, Z3alpha is the first MCTS-             lem. Different from AlphaDev, which considers the synthe-
    based method developed for the SMT strategy synthesis         sis of assembly programs as sequencing individual instruc-
    problem.                                                      tions, we present the strategy program as an expression tree.
 2. Layered and Staged MCTS: To address the unique                The increased complexity in program structure and the ex-
    challenges inherent to strategy synthesis, that cannot be     tended program evaluation time present unique challenges to
    solved by the conventional MCTS alone, we develop             the strategy synthesis problem.
    two innovative heuristics, namely, layered search and
    staged search on top of the MCTS framework. The lay-          2.2     MCTS Variants
    ered search method effectively narrows the search space       It is a well-known problem that the basic MCTS method does
    by treating certain auxiliary tasks as independent search     not generalize well between related states and actions. It re-
    problems. On the other hand, the staged search tech-          sults in a notably inefficient search in scenarios where the
    nique segments the entire search problem into sequen-         search space is extensive. To counter this issue, various tech-
    tial sub-problems, enabling the use of results from early     niques have been proposed.
   One prevalent technique is the rapid action value estima-
tion (RAVE) algorithm [Gelly and Silver, 2011], which in-                ⟨Strategy⟩ → ⟨Tactic⟩
corporates an action-specific term QRAVE into the MCTS tree                          | (using-params ⟨Strategy⟩ ⟨ParamSettings⟩)
policy. Its basic assumption is that there is an intrinsic value                     | (then ⟨Tactic⟩ ⟨Strategy⟩)
associated with each action regardless of its position. Game                         | (or-else ⟨Strategy⟩ ⟨Strategy⟩)
abstraction [Johanson, 2013] is another common technique,                            | (try-for ⟨Strategy⟩ ⟨Constant⟩)
especially used in Poker, to expedite the search. It abstracts
                                                                                     | (if ⟨Predicate⟩ ⟨Strategy⟩ ⟨Strategy⟩)
similar actions or states into a single category to reduce the
search space. Option Monte Carlo Tree Search (O-MCTS)                      ⟨Tactic⟩ → simplify | smt | sat | solve-eqs | elim-uncnstr | ...
[De Waard et al., 2016] uses options [Sutton et al., 1999]         ⟨ParamSettings⟩ → ⟨ParamSetting⟩ | ⟨ParamSetting⟩ ⟨ParamSettings⟩
in the MCTS framework, to mimic the human behaviors of              ⟨ParamSetting⟩ → : ⟨Parameter⟩ ⟨Constant⟩
defining subgoals and subtasks in game playings. An option             ⟨Parameter⟩ → som | flat | seed | elim and | ...
is a predefined method for reaching a specific subgoal, with            ⟨Predicate⟩ → ⟨BProbe⟩ | (⟨Operator⟩ ⟨NProbe⟩ ⟨Constant⟩)
its own policy and termination function. In O-MCTS, the
agent selects among options instead of actions.                           ⟨BProbe⟩ → is-unbounded | is-pb | is-qflia | ...
   Our layered and staged search methods share similarities             ⟨Operator⟩ → > | < | ≥ | ≤ | = | ̸=
with these MCTS variants. The layered search method re-                   ⟨NProbe⟩ → num-consts | num-exprs | size | ...
duces action and state spaces, but, instead of abstracting, it          ⟨Constant⟩ → true | false | 0 | -1 | 1 | ...
separates certain auxiliary actions aside and optimizes them
in parallel. This separation generalizes values among sub-
trees, but, unlike RAVE which shares values between actions
in different positions, it merges subtrees. The staged search         Figure 1: Context-free grammar G the Z3 strategy language
chooses among previously found rewarding sub-solutions, is
similar to choosing among options. However, it does not have
a separate predefined policy for each choice.                      of symbols constrained by specific theories [Kroening and
                                                                   Strichman, 2016]. SMT-LIB refers to an international initia-
2.3    SMT Strategy Synthesis                                      tive aimed at facilitating research and development in SMT
                                                                   solvers [Barrett et al., 2016]. The SMT-LIB initiative main-
StratEVO [Ramı́rez et al., 2016] presents a pioneering
                                                                   tains a large library of SMT benchmarks, grouped by vari-
effort in automated strategy generation, utilizing a genetic
                                                                   ous SMT logics. A logic consists of one or more theories
programming algorithm [Koza, 1994] to evolve strategies
                                                                   with certain restrictions, and is named after such theories and
from a predefined strategy population. Unfortunately, the
                                                                   restrictions. “QF” refers to the restriction to quantifier-free
StratEVO tool is not publicly available, which precludes
                                                                   formulas, “BV” refers to the theory of fixed-size bit-vectors,
us from conducting an empirical comparison.
                                                                   “S” refers to the theory of strings and regular expressions,
   FastSMT [Balunovic et al., 2018], recognized as the             “IA” and “RA” refer to integer and real arithmetic. “N” be-
SOTA tool in SMT strategy synthesis, applies a dual-phase          fore “IA” or “RA” means the non-linear fragment of these
learning approach. First, it applies the DAgger [Ross et           arithmetics. SMT-COMP [Bobot et al., 2023] is an annually
al., 2011] algorithm to train a deep neural network (DNN),         held competition that arose from the SMT-LIB initiative for
in order to discover a collection of branch-free strategies,
                                                                   SMT solvers.
each tailored for specific instances. These strategies are
then synthesized into one single, unified strategy through         The Z3 Strategy Language: The Z3 SMT solver offers a
an entropy-based decision-tree learning algorithm [Poole and       user-controllable strategy language, allowing users to craft
Mackworth, 2010]. Chen et al. [2021] proposed a strategy           their customized decision procedure algorithm. A strategy
synthesis method specifically for symbolic execution, where,       selects, sequences, and parameterizes tactics, where each tac-
similar to FastSMT, strategies are synthesized with decision       tic is a built-in reasoning step in Z3. The context-free gram-
tree techniques from a list of branch-free strategies found by     mar (CFG) G for the strategy language we consider in this
an offline trained DNN.                                            research is shown in Figure 1, where variables are enclosed
   Our method also adopts a two-step structure in our staged       in angle brackets and terminals are highlighted in bold.
search approach. However, we utilize MCTS for both steps.             The start symbol ⟨Strategy⟩ represents a strategy and is de-
Compared to FastSMT, our method shows superior and                 fined recursively. A strategy may consist of either a single
more robust empirical results across six SMT logics, as de-        tactic or a series of tactics linked in sequence by the tactic
tailed in Section 5. Further, the strategies synthesized by        combinator then. Each tactic can be configured with a vari-
FastSMT tend to be less interpretable, sometimes involving         ety of parameters. The combinator or-else applies the second
more than a thousand branches.                                     strategy if the first strategy fails, while the combinator try-for
                                                                   makes the strategy fail if it does not return within the speci-
                                                                   fied timeout (millisecond). Z3 also provides built-in probes,
3     Preliminaries                                                which evaluate formula measures, e.g., the number of con-
SMT Solvers, SMT Logics, and SMT-LIB: Satisfiabil-                 stants in the formula. Predicates over them can be built using
ity Modulo Theories (SMT) solvers determine the satisfia-          relational operators. The if combinator constructs branching
bility of first-order logic formulas, with the interpretation      strategies based on these predicates. We refer readers to the
official Z3 guide [Microsoft, 2023] for more information on
the strategy language.
Monte Carlo Tree Search: Monte Carlo Tree Search
(MCTS) is a best-first search technique. It searches for the
optimal decisions by estimating action values from numerous
simulated trajectories. To search more efficiently, the method
biases simulations towards previously rewarding trajectories,
yet it maintains a balance by exploring less-visited paths as
well. Alongside the simulations, an MCTS tree is progres-
sively constructed to store the action value estimations.
Each MCTS simulation consists of 4 steps:
    1. Selection: Starting from the root node, a tree-search pol-   Figure 2: Illustration of the MCTS framework for strategy synthesis
       icy traverses the MCTS tree until a leaf node is selected.
       The Upper Confidence Bounds applied for Trees (UCT)
       [Kocsis and Szepesvári, 2006] is the most common al-           With this modeling, the MDP search tree is directly rep-
       gorithm used for the tree-search policy in MCTS. UCT         resentative of the strategy space, and the objective becomes
       balances exploiting the child node with the highest value    identifying the path with the highest reward Rt in the search
       estimation and exploring the less-visited children.          tree, corresponding to the optimal strategy for P .
    2. Expansion: The MCTS tree is expanded from the se-
       lected leaf node by adding child(ren) node(s) represent-     4.2   The MCTS Framework for Strategy Synthesis
       ing unexplored actions.                                      We instantiate MCTS for this optimal strategy search prob-
    3. Rollout: If the selected leaf node is non-terminal, the      lem. We use UCT as the tree policy in the selection phase and
       simulation continues by subsequently choosing actions        rollout randomly in the rollout phase. Notably, in the backup
       according to a rollout policy (usually a random policy)      phase, we apply the max-backup rule [Sabharwal et al., 2012;
       until reaching a terminal state.                             Sun et al., 2023]. This approach updates the action values
                                                                    with the best observed return, rather than the average. It en-
    4. Backup: After evaluation, the episode reward is backed       courages more aggressive exploitation towards the previously
       up to update the action values alongside the traversed       best-performing strategy, aligning with our goal.
       tree path.
                                                                       Therefore, the MCTS method continuously runs simula-
                                                                    tions, and in each simulation, the agent explores and assesses
4     Z3alpha: MCTS for Strategy Synthesisis                        a single strategy, updating and retaining the best strategy seen
4.1     Modeling Strategy Synthesis as an MDP                       so far. The MCTS stops when a simulation budget is reached.
If we view strategy synthesis as constructing a strategy string     At the end of this process, the strategy with the highest re-
from G by sequentially applying production rules to the left-       ward RT is selected and presented as the synthesized SMT
most variable, this process can be modeled as a deterministic       strategy for the specified instance set P . Figure 2 illustrates
Markov Decision Process (MDP). An MDP is a mathemati-               our basic MCTS framework, using a simplified CFG G′ for
cal framework in which an agent makes action decisions in a         illustrative purposes. G′ is defined as S → T S | smt and
series of states, with each action leading to a new state. The      S → T simplify | aig, where S and T symbolize variables for
agent seeks to maximize rewards over time through choices           strategy and tactic, respectively.
of actions. In a deterministic MDP, each action results in a           The primary challenge in synthesizing strategies through
deterministic state transition.                                     this conventional MCTS method is the extensive time re-
   In our formulation of the strategy synthesis problem, the        quired to evaluate each strategy, which involves calling an
states are the sentential strings derived from G, while the ac-     SMT solver on all instances in P . This leads to a very lim-
tions are the production-rule applications. The entire process      ited exploration of potential paths, particularly given the im-
of constructing a strategy is one single episode of the MDP.        mense search space created by the rich strategy language. To
In an episode, the reward RT is only received at the terminal       address this issue, we first add domain-knowledge rules re-
step T . RT is determined by the performance measure of the         stricting valid actions. For example, no tactic could be ap-
synthesized strategy over a given benchmark set P .                 plied sequentially following a solver tactic such as smt. We
   Our reward system is designed to align with the evalua-          refer readers to the Appendix for a comprehensive list of such
tion criteria of SMT-COMP, prioritizing strategies that solve       rules. More importantly, we have introduced two heuristic
the highest number of instances. Simultaneously, when two           methods, namely the layered search and the staged search, on
strategies solve a similar number of P -instances, we want to       top of the conventional MCTS, facilitating a deeper and more
steer the search towards the faster strategy. To embody these       effective exploration of the strategy space.
goals, we base our reward on the PAR-10 score over P . PAR-
10 computes the average runtime for successfully solved in-         4.3   Layered Search
stances and imposes a penalty for unsolved instances. The           To solve the above-mentioned challenge, we propose a lay-
penalty is equal to the timeout value multiplied by a factor of     ered search method to optimize the tactic parameters within
10.                                                                 strategy synthesis. As shown in our CFG G, each tactic can
                                                                     it is common for a tactic to be used multiple times within
                                                                     a strategy. Thus, navigating a search space that is fully ex-
                                                                     panded by all possible parameter combinations becomes im-
                                                                     practical, especially given the time-intensive nature of strat-
                                                                     egy evaluation. Secondly, we argue that parameter tuning,
                                                                     although important, serves more as an auxiliary task in com-
                                                                     parison to the tasks of tactic selection and sequencing. By
                                                                     employing the layered search method, we maintain the pri-
                                                                     mary focus on the more important task. At the same time,
                                                                     the isolated MABs efficiently optimize the parameters with-
                                                                     out overwhelming the main search process.

                                                                     4.4   Staged Search
                                                                     While the layered search method successfully narrows down
                                                                     the search space, it does not alleviate the issue of signifi-
                                                                     cant time consumption required for each simulation evalua-
Figure 3: Comparison of the conventional MCTS and the layer-
search in treating tactic parameter tuning                           tion. To discover a complex strategy, especially one involv-
                                                                     ing nested branching, MCTS must expand over a broad space
                                                                     and delve deeply, often resulting in an impractically lengthy
be paired with multiple parameters. Using the conventional           search time. This is where the staged search comes into play.
MCTS with the grammar G, the selection of each candidate                The staged search method divides the entire search pro-
value for a parameter is represented by one production rule,         cess into two stages. In the first stage, the MCTS focuses
and the agent needs to make sequential production-rule deci-         on finding high-performing linear strategies (actions intro-
sions to configure all parameters for a given tactic, leading to     ducing branches are not considered in the first stage). Here,
exponential growth in the problem search tree, as shown in           a linear strategy is defined as a sequence of tactics without
Figure 3(a).                                                         branching, where tactics are only connected with the combi-
   To address this issue, our layered search method ap-              nator then. In the second stage, the MCTS looks for a sin-
proaches the tuning of each tactic parameter as a sepa-              gle best strategy that combines these selected linear strate-
rate Multi-Armed Bandit (MAB) problem [Robbins, 1952].               gies. In other words, the second-stage MCTS works with the
As shown in Figure 3(b), the two parameters som and                  full grammar of G but restricts the actions so that every ex-
max degree for one application of the tactic simplify are            plored strategy is a combination of the selected linear strate-
modeled as two MABs respectively. Each arm in the MAB                gies through branching. By doing so, the key advantage is
represents one candidate value. For example in Figure 3(b),          that the evaluation of the combined strategies can be done
arm 16, 32, and 64 in the MAB max degree are three pre-              speedily based on the cached linear-strategy performances in
selected candidate values for this parameter. Note that the          the first stage, without costly SMT solver calls.
parameter MABs are associated with a tree edge, correspond-             This is possible because, when executing any branched
ing to one specific application of a tactic, not to this tactic in   strategy Sc on a given instance f , there is always an
general. For instance, simplify may be applied serval times          equivalent sequence of branch-free strategy applications,
in the strategy building. For each application, there will be        [S0 , S1 , ..., SN ]. For example, if we apply ((if is-pb (or-else
two MABs representing the tuning of som and max degree               (try-for (then simplify sat) 4000) smt) smt)) to a pseudo-
associated with it.                                                  boolean instance, the execution path is first to try (then sim-
   One key point is that these parameter-tuning MABs are             plify sat), a linear strategy, for 4 seconds and then to execute
not part of the main MCTS tree. They are engaged to se-              smt, another linear strategy. Thus, when evaluating Sc for
lect parameter values when their associated tree edge is tra-        each input instance f , we first convert Sc to its equivalent
versed, and they are updated based on the episode reward dur-        linear strategy sequence [S0 , S1 , ..., SN ], where the perfor-
ing the Backup phase. However, such MABs do not expand               mance of each linear strategy S0 , S1 , ..., SN on f is known
the MCTS search tree after the parameter configuration, since        and cached in the first stage. Then, the performance of Sc can
they are separate components from the main search tree. This         be derived directly from these cached results without further
is in contrast to conventional MCTS, which also employs              call to the SMT solver. This approach enables MCTS to tra-
MAB principles to select among children nodes to explore,            verse a significantly larger search space in the second stage,
where these nodes constitute part of the search tree. For ex-        facilitating the discovery of effective complex strategies.
ample, in Figure 3(a), the search tree is expanded sixfold to           Another advantage of our staged search method is its adap-
accommodate all possible combinations of these two param-            tiveness to long timeouts. Strategy synthesis typically op-
eters in the conventional MCTS framework. In contrast, in            erates under short solver-instance timeouts, for example, 10
the layered search framework (Figure 3(b)), MABs for the             seconds in the FastSMT study. Increasing the timeout lin-
two parameters are isolated from the search tree, creating no        early raises the total synthesis time, making it prohibitively
additional branches in the tree.                                     costly to synthesize strategies with extended timeouts, like
   The rationale behind the layer search is twofold. Firstly,        5 minutes or more, through direct evaluation. Our staged
tactics such as simplify may have dozens of parameters, and          search method provides a practical approach to synthesiz-
         Timeout(s)      Logic     Benchmark      Test Size   Z3alpha       Z3alpha0       FastSMT         Z3    CVC5    Z3str4
                                   Sage2            6444        52.9           41.3          51.3         37.1    36.6      -
                       QF BV
                                   core             270         99.6           99.6          100.0        75.6    82.6      -
                                   AProVE           1712        94.8           92.5           90.3        90.0    69.9      -
                       QF NIA
                                   leipzig           68         91.2           89.1          88.2         89.7    25.0      -
              10
                       QF NRA      hycomp           1982        91.4           90.8           89.1        84.7    85.5      -
                       QF LIA      entire logic    12476        76.2            -             31.2        74.6    64.8      -
                       QF LRA      entire logic     1003        73.6            -             74.0        71.0    63.6      -
                       QF S        entire logic    18173        99.0            -              -          98.2    98.4     97.2
             60        QF BV       Sage2            6444        69.8            -             67.7        57.7    77.8      -
             300       QF BV       Sage2            6444        75.8            -             72.6        69.8    93.3      -

Table 1: Z3alpha vs. SOTA Solvers: Percentage (%) of instances solved from the selected SMT-LIB benchmarks across six SMT logics (
In each experiment, the result of the leading tool is highlighted in bold, while the second-best is underscored.)


ing strategies under such extended timeouts. In the first           instances for our training set, and utilized all remaining in-
stage, the linear strategy candidates are still selected based on   stances in the logic (12,476 instances and 1,003 instances for
their performance with a short timeout period (e.g., 10 sec-        QF LIA and QF LRA, respectively) as our testing set.
onds), ensuring broad exploration. These strategies are then        Experimental Design for Long Timeout: In Section 5.5,
re-evaluated under the specified long timeout (e.g., 5 min-         we expanded our experiments to include longer timeouts,
utes). The second-stage MCTS leverages these re-evaluation          specifically 1-minute and 5-minute durations. These evalu-
results, enabling the synthesis of customized strategies opti-      ations were conducted on the most challenging benchmark
mized for these extended timeout scenarios.                         set, Sage2, from Section 5.3. Z3alpha synthesized new
                                                                    strategies for these scenarios, using the method described in
5     Experiment Design, Results, and Analysis                      Section 4.4. FastSMT used the identical strategy as in Sec-
                                                                    tion 5.3 for these extended timeout cases, adhering to the ap-
5.1    Experimental Design                                          proach described in its paper.
                                                                    Experimental Design for User-defined Tactics: Z3 al-
We evaluated Z3alpha across six logics, namely QF {BV,              lows users to implement new rewrite rules or solver algo-
NIA, NRA, LIA, LRA, S}. We benchmarked our perfor-                  rithms as tactics. Section 5.6 evaluated the capability of
mance against the SOTA strategy synthesis tool, FastSMT,            Z3alpha in synthesizing strategies that integrate both user-
as well as the default handcrafted strategy in Z3. CVC5 was         defined and built-in tactics. This experiment targeted the
also included as a baseline for comparison. To assess the ro-       QF S logic. In recent years, the Z3 String Constraint Solver
bustness of Z3alpha, we designed a series of experiments            team 1 implemented new tactics, such as the arrangement-
tailored to different scenarios.                                    based solver Z3str3 [Berzish et al., 2017], the Length Ab-
Experimental Design for Specific Classes of Benchmarks:             straction Solver (LAS) [Mora et al., 2021], and specialized
In Section 5.3, we describe the evaluation of the solvers on        rewrite rules for regular expressions [Berzish et al., 2021] for
five important SMT-LIB benchmark sets, namely, Sage2                string constraint problems. These tactics are in addition to the
(QF BV), core (QF BV), AProVE (QF NIA), leipzig                     default built-in sequence solver in Z3. Z3str4 [Mora et al.,
(QF NIA), and hycomp (QF NRA), covering three differ-               2021] combines the aforementioned tactics using a meticu-
ent logics. These specific benchmark sets were chosen as            lously handcrafted strategy. In this experiment, we leveraged
they were also utilized in the FastSMT study, following the         Z3alpha to construct a strategy using the same set of tac-
same training-testing split. The size of these benchmark sets       tics as in Z3str4 and then compared their performances.
varies, ranging from 167 to 7436 instances. A 10-second             Z3alpha was trained on 750 randomly chosen QF S in-
timeout was chosen for evaluation, a common practice in             stances from SMT-LIB. The testing was conducted on all the
the SMT strategy synthesis research [Ramı́rez et al., 2016;         remaining 18,173 instances in the logic.
Balunovic et al., 2018]. This timeout period was also justi-
fied as Z3alpha was able to solve over 90% of the testing in-       5.2       Experimental Setup
stances in four out of the five benchmark sets within this time     For every experiment, there were a training instance set and a
frame. Additionally, in this section, we included a version of      testing instance set. Z3alpha, as well as FastSMT, synthe-
our tool, Z3alpha0, that did not employ staged search, for          sized strategies based on the training set while reporting ex-
ablation study purposes.                                            periment results on the testing set. The approach aligns with
Experimental Design for Benchmarks from Diverse Ap-                 our problem statement, wherein our goal is to synthesize a
plications: In Section 5.4, we extended our experiments             strategy based on a representative set P , and the strategy is
to the entire SMT-LIB QF LIA and QF LRA benchmarks,                 expected to generalize well.
which are obtained from diverse applications. These experi-            In each experiment, Z3alpha first selected 20 linear
ments were intended to evaluate the versatility and adaptabil-      strategies from 800 first-stage MCTS simulations. Subse-
ity of Z3alpha in handling diverse problem sets. For both
                                                                        1
QF LIA and QF LRA, we randomly selected 750 SMT-LIB                         https://z3string.github.io/
quently, during the second stage with 300,000 simulations,          the synthesized strategies from Z3alpha and FastSMT was
Z3alpha searched for the most effective strategy that com-          that Z3alpha strategies are more interpretable. For exam-
bined these linear strategy candidates. The final synthesized       ple, the FastSMT strategies for AProVE can have more than
strategy was the one that yielded the lowest PAR-10 score           a thousand branches, while Z3alpha strategies usually have
during the second-stage search. To keep a similar time bud-         less than five branches.
get, the non-staged-search version Z3alpha0 ran MCTS for
1,000 simulations with the full CFG G, in search of the best        5.4    Analysis of QF LIA and QF LRA Results
strategy (including branching ones).                                When tested across SMI-LIB benchmarks in the entire logic
Competing Solvers: Z3alpha was implemented in Python                of QF LIA and QF LRA, Z3alpha also demonstrated con-
3.10 and was integrated with Z3-4.12.2. FastSMT was                 sistent performance, as shown in rows of QF LIA and
also integrated with the same version of Z3. Both tools             QF LRA in Table 1. Z3alpha solved 2.2% and 3.7% more
constructed their strategies using the identical tactic and pa-     instances than Z3 in QF LIA and QF LRA, respectively.
rameter set offered by Z3, and executed these strategies            While FastSMT solved 4 more instances than Z3alpha in
with Z3. See the Appendix for a detailed description of             QF LRA, its performance suffered significantly in QF LIA,
the tactic and parameter candidates for each SMT logic.             solving 58.2% fewer instances than the default Z3 strategy.
Baseline solvers used in the experiment were Z3-4.12.2
and CVC5-1.0.5. We compared our performance with                    5.5    Analysis of QF BV Results with Long Timeout
FastSMT in all experiments other than the experiment de-            The results for experiments of 1-minute-timeout and 5-
scribed in Section 5.6, since Z3str4 does not provide               minute-timeout are shown in Table 1. In every scenario,
Python APIs for the user-defined tactics that are required by       Z3alpha continued to maintain superior performance com-
FastSMT.                                                            pared to both FastSMT and Z3. The performance advantage
Computational Environments: Both our synthesis and test-            over FastSMT slightly increased when the timeouts were
ing were conducted on a high-performance CentOS 7 cluster           extended. However, an important shift was the significantly
equipped with Intel E5-2683 v4 (Broadwell) processors run-          better performance of CVC5 over the Z3-based methods for
ning at 2.10 GHz, accompanied by 75 gigabytes of memory.            Sage2 under long timeouts. This suggests a promising fu-
Variability: Both the Z3alpha and FastSMT algorithms                ture research direction of extending the strategy synthesis
make use of randomness, leading to the possibility of synthe-       method across different solvers.
sizing different strategies in separate runs. To account for this
variability, the results in Section 5.3 were average from 5 runs    5.6    Results with User-Defined Tactics for QF S
with different random seeds. Since little variability was found
                                                                    The test results for Z3alpha with user-defined QF S tactics
in Section 5.3 and the much more intense computational na-
                                                                    are shown in the QF S row of Table 1. Z3alpha demon-
ture of the later experiments, we only report results from one
                                                                    strated superior performance over all baseline solvers. Inter-
run in later sections.
                                                                    estingly, the handcrafted Z3str4 strategy, despite employ-
Metrics: Consistent with the evaluation criteria used in the
                                                                    ing the same tactic portfolio as Z3alpha, performed worse
SMT-COMP, our performance metric was based on the num-
                                                                    than the default Z3 strategy. The under-performance could
ber of correctly solved instances. For clearer comprehension
                                                                    be attributed to two factors: (1) the Z3str4 strategy was op-
by our readers, we present these results as a percentage, re-
                                                                    timized for logics including both QF S and QF SLIA, which
flecting the proportion of solved instances out of the total
                                                                    could be sub-optimal for QF S alone; (2) the tuning of the
tested. Additionally, we include results, such as PAR-2 and
                                                                    Z3str4 strategy was carried out on an earlier version of Z3.
PAR-10 scores, in the Appendix for further reference.
                                                                    These points emphasize the importance and benefits of auto-
5.3   Analysis of QF BV, QF NIA, QF NRA Results                     mated strategy customization, tailored for specific problems
                                                                    and updated base solvers.
The first part of Table 1 summarizes the results on the five
selected benchmark sets, namely Sage2, core, AProVE,
leipzig, and hycomp, across the QF BV, QF NIA, and                  6     Conclusions
QF NRA logics. Notably, Z3alpha surpassed the de-                   In this work, we present Z3alpha, a novel MCTS-based
fault Z3 strategy, as well as CVC5 in all of these bench-           method for SMT strategy synthesis. Z3alpha introduces
mark sets, achieving the leading position in four of the five       layered and staged search heuristics upon the conventional
sets among all tested tools. In the particularly challenging        MCTS framework, enabling a low-cost and effective search
QF BV benchmark set Sage2, Z3alpha excelled by solv-                within the expansive strategy space. The superiority of
ing an impressive 42.7% more instances than the default strat-      Z3alpha was demonstrated by extensive experiments across
egy did. Furthermore, Z3alpha outperformed Z3alpha0                 six SMT logics. In all the experiments, Z3alpha consis-
across all benchmarks, underscoring the effectiveness of the        tently surpassed the default Z3 solver and outperformed both
staged search. The synthesis time for Z3alpha was on par            FastSMT and CVC5 in the majority of cases.
with, and in most experiments, less than, the synthesis time           Our method is currently implemented only upon Z3, be-
for FastSMT. For instance, while the strategy synthesis for         cause other prominent solvers, like CVC5, to the best of our
AProVE took 759.6 minutes, Z3alpha completed the task               knowledge, do not offer an interface to group preprocessing
in 293.1 minutes, in which the stage-1 and stage-2 took 213.7       and solving steps flexibly. We hope our strong empirical re-
and 79.4 minutes respectively. One key distinction between          sults will encourage a universal user-controllable strategy lan-
guage in the SMT community. There is substantial poten-          [Chen et al., 2021] Zhenbang Chen, Zehua Chen, Ziqi
tial to further enhance solver performance by applying our         Shuai, Guofeng Zhang, Weiyu Pan, Yufeng Zhang, and
method across tactics from different solvers, thereby leverag-     Ji Wang. Synthesize solving strategy for symbolic execu-
ing their complementary strengths.                                 tion. In Proceedings of the 30th ACM SIGSOFT Interna-
                                                                   tional Symposium on Software Testing and Analysis, pages
Acknowledgements                                                   348–360, 2021.
We thank Kate Larson, Arie Gurfinkel, and Mark Crowley for       [De Moura and Bjørner, 2008] Leonardo De Moura and
their valuable feedback; Kaihang Jiang for his contribution        Nikolaj Bjørner. Z3: An efficient SMT solver. In In-
to code testing and data collection; and the Digital Research      ternational conference on Tools and Algorithms for the
Alliance of Canada for providing the computational resources       Construction and Analysis of Systems, pages 337–340.
and technical support.                                             Springer, 2008.
   The work of Zhengyang Lu is supported by the Engineer-        [De Moura and Bjørner, 2011] Leonardo De Moura and
ing Excellence Doctoral Fellowship (EEDF) at the University        Nikolaj Bjørner. Satisfiability modulo theories: intro-
of Waterloo; the work of Florin Manea was supported by the         duction and applications. Communications of the ACM,
DFG-Heisenberg grant no. 466789228.                                54(9):69–77, 2011.

References                                                       [De Moura and Passmore, 2013] Leonardo De Moura and
                                                                   Grant Olney Passmore. The strategy challenge in SMT
[Balunovic et al., 2018] Mislav Balunovic, Pavol Bielik, and       solving. Automated Reasoning and Mathematics: Essays
  Martin Vechev. Learning to solve SMT formulas. In                in Memory of William W. McCune, pages 15–44, 2013.
  Advances in Neural Information Processing Systems 31,
  pages 10337–10348. Curran Associates, 2018.                    [De Waard et al., 2016] Maarten De Waard, Diederik M Roi-
[Barrett et al., 2016] Clark Barrett, Pascal Fontaine, and Ce-     jers, and Sander CJ Bakkes. Monte carlo tree search with
                                                                   options for general video game playing. In 2016 IEEE
  sare Tinelli. The satisfiability modulo theories library
                                                                   Conference on Computational Intelligence and Games
  (SMT-LIB). http://smtlib.cs.uiowa.edu/index.shtml, 2016.
                                                                   (CIG), pages 1–8. IEEE, 2016.
  Accessed: 2024-01-16.
[Berzish et al., 2017] Murphy Berzish, Vijay Ganesh, and         [Gelly and Silver, 2011] Sylvain Gelly and David Silver.
  Yunhui Zheng. Z3str3: A string solver with theory-aware          Monte-carlo tree search and rapid action value estima-
  heuristics. In 2017 Formal Methods in Computer Aided             tion in computer go. Artificial Intelligence, 175(11):1856–
  Design (FMCAD), pages 55–59. IEEE, 2017.                         1875, 2011.
[Berzish et al., 2021] Murphy Berzish, Mitja Kulczynski,         [Gurfinkel et al., 2015] Arie Gurfinkel, Temesghen Kahsai,
  Federico Mora, Florin Manea, Joel D Day, Dirk Nowotka,           Anvesh Komuravelli, and Jorge A Navas. The SeaHorn
  and Vijay Ganesh. An SMT solver for regular expressions          verification framework. In International Conference on
  and linear arithmetic over string length. In International       Computer Aided Verification, pages 343–361. Springer,
  Conference on Computer Aided Verification, pages 289–            2015.
  312. Springer, 2021.                                           [Jha et al., 2024] Piyush Jha, Zhengyu Li, Zhengyang Lu,
[Bobot et al., 2023] François Bobot, Martin Bromberger,            Curtis Bright, and Vijay Ganesh. AlphaMapleSAT: An
  and Jochen Hoenicke. SMT-COMP 2023. https://                      MCTS-based cube-and-conquer SAT solver for hard com-
  smt-comp.github.io/2023/, 2023. Accessed: 2024-01-16.             binatorial problems. arXiv preprint arXiv:2401.13770,
[Browne et al., 2012] Cameron B Browne, Edward Pow-                 2024.
  ley, Daniel Whitehouse, Simon M Lucas, Peter I Cowl-           [Johanson, 2013] Michael Johanson. Measuring the size
  ing, Philipp Rohlfshagen, Stephen Tavener, Diego Perez,           of large no-limit poker games.     arXiv preprint
  Spyridon Samothrakis, and Simon Colton. A survey of               arXiv:1302.7008, 2013.
  monte carlo tree search methods. IEEE Transactions on
  Computational Intelligence and AI in games, 4(1):1–43,         [Khalil et al., 2022] Elias B Khalil, Pashootan Vaezipoor,
  2012.                                                            and Bistra Dilkina. Finding backdoors to integer pro-
                                                                   grams: a monte carlo tree search framework. In Proceed-
[Cadar et al., 2008] Cristian Cadar, Vijay Ganesh, Peter M         ings of the AAAI Conference on Artificial Intelligence, vol-
  Pawlowski, David L Dill, and Dawson R Engler. EXE: Au-           ume 36, pages 3786–3795, 2022.
  tomatically generating inputs of death. ACM Transactions
  on Information and System Security (TISSEC), 12(2):1–          [Kocsis and Szepesvári, 2006] Levente Kocsis and Csaba
  38, 2008.                                                        Szepesvári. Bandit based monte-carlo planning. In Eu-
                                                                   ropean conference on machine learning, pages 282–293.
[Cameron et al., 2022] Chris Cameron, Jason Hartford, Tay-
                                                                   Springer, 2006.
  lor Lundy, Tuan Truong, Alan Milligan, Rex Chen, and
  Kevin Leyton-Brown. Monte carlo forest search: UNSAT           [Koza, 1994] John R Koza. Genetic programming as a means
  solver synthesis via reinforcement learning. arXiv preprint      for programming computers by natural selection. Statistics
  arXiv:2211.12581, 2022.                                          and computing, 4:87–112, 1994.
[Kroening and Strichman, 2016] Daniel Kroening and Ofer               self-play with a general reinforcement learning algorithm.
   Strichman. Decision Procedures: An Alogorithm Point of             arXiv preprint arXiv:1712.01815, 2017.
   View. Springer, 2016.                                           [Song et al., 2008] Dawn Song, David Brumley, Heng Yin,
[Mankowitz et al., 2023] Daniel J Mankowitz, Andrea                   Juan Caballero, Ivan Jager, Min Gyung Kang, Zhenkai
   Michi, Anton Zhernov, Marco Gelmi, Marco Selvi,                    Liang, James Newsome, Pongsin Poosankam, and Prateek
   Cosmin Paduraru, Edouard Leurent, Shariq Iqbal, Jean-              Saxena. BitBlaze: A new approach to computer secu-
   Baptiste Lespiau, Alex Ahern, et al. Faster sorting                rity via binary analysis. In Information Systems Security:
   algorithms discovered using deep reinforcement learning.           4th International Conference, ICISS 2008, Hyderabad, In-
   Nature, 618(7964):257–263, 2023.                                   dia, December 16-20, 2008. Proceedings 4, pages 1–25.
[Microsoft, 2023] Microsoft. Online Z3 guide. https://                Springer, 2008.
   microsoft.github.io/z3guide/, 2023. Accessed: 2024-01-          [Sun et al., 2023] Fangzheng Sun, Yang Liu, Jian-Xun
   16.                                                                Wang, and Hao Sun. Symbolic physics learner: Discov-
[Mora et al., 2021] Federico Mora, Murphy Berzish, Mitja              ering governing equations via monte carlo tree search. In
   Kulczynski, Dirk Nowotka, and Vijay Ganesh. Z3str4: A              The Eleventh International Conference on Learning Rep-
   multi-armed string solver. In Formal Methods: 24th Inter-          resentations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023.
   national Symposium, FM 2021, Virtual Event, November               OpenReview.net, 2023.
   20–26, 2021, Proceedings 24, pages 389–406. Springer,           [Sutton et al., 1999] Richard S Sutton, Doina Precup, and
   2021.                                                              Satinder Singh. Between MDPs and semi-MDPs: A
[Poole and Mackworth, 2010] David L Poole and Alan K                  framework for temporal abstraction in reinforcement
   Mackworth. Artificial Intelligence: foundations of com-            learning. Artificial intelligence, 112(1-2):181–211, 1999.
   putational agents. Cambridge University Press, 2010.
[Pulina and Tacchella, 2012] Luca Pulina and Armando Tac-
   chella. Challenging SMT solvers to verify neural net-
   works. Ai Communications, 25(2):117–135, 2012.
[Ramı́rez et al., 2016] Nicolás Gálvez Ramı́rez, Youssef
   Hamadi, Eric Monfroy, and Frédéric Saubion. Evolving
   SMT strategies. In 2016 IEEE 28th International Confer-
   ence on Tools with Artificial Intelligence (ICTAI), pages
   247–254. IEEE, 2016.
[Robbins, 1952] Herbert Robbins. Some aspects of the se-
   quential design of experiments. Bull. Amer. Math. Soc.,
   58(5):527–535, 1952.
[Ross et al., 2011] Stéphane Ross, Geoffrey Gordon, and
   Drew Bagnell. A reduction of imitation learning and struc-
   tured prediction to no-regret online learning. In Proceed-
   ings of the fourteenth international conference on artificial
   intelligence and statistics, pages 627–635. JMLR Work-
   shop and Conference Proceedings, 2011.
[Sabharwal et al., 2012] Ashish Sabharwal, Horst Samu-
   lowitz, and Chandra Reddy. Guiding combinatorial op-
   timization with UCT. In Integration of AI and OR Tech-
   niques in Contraint Programming for Combinatorial Opti-
   mzation Problems: 9th International Conference, CPAIOR
   2012, Nantes, France, May 28–June1, 2012. Proceedings
   9, pages 356–361. Springer, 2012.
[Silver et al., 2016] David Silver, Aja Huang, Chris J Maddi-
   son, Arthur Guez, Laurent Sifre, George Van Den Driess-
   che, Julian Schrittwieser, Ioannis Antonoglou, Veda Pan-
   neershelvam, Marc Lanctot, et al. Mastering the game
   of go with deep neural networks and tree search. nature,
   529(7587):484–489, 2016.
[Silver et al., 2017] David Silver, Thomas Hubert, Julian
   Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur
   Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran,
   Thore Graepel, et al. Mastering chess and shogi by
Appendix
A    Additional Methodology Details
Domain Knowledge Rules: In Section 4.2, we mention
that, in order to reduce the action space, additional domain-
knowledge-based simplification rules are introduced to the
problem modeling. Such rules include:
  1. When ⟨Strategy⟩ → ⟨Tactic⟩ is applied, ⟨Tactic⟩ can
     only choose a solver-wrapper tactic, e.g., smt. When                        Figure 4: The Staged MCTS Framework
     ⟨Strategy⟩ → (then ⟨Tactic⟩ ⟨Strategy⟩) is applied,
     solver-wrapper tactics cannot be chosen for ⟨Tactic⟩.
  2. Do not apply the try-for rule for a strategy that has al-       greedy algorithm. The idea is to incrementally build a linear
     ready been set for a try-for timeout.                           strategy portfolio that collectively performs the best. Here,
                                                                     we define the virtual best strategy for a strategy set as an or-
  3. The if predicate can only appear at the first three depths      acle that, for each instance, perfectly selects the best strategy
     of the constructed strategy’s syntax tree. Moreover, do         from the strategy set without any overhead. Then, the selec-
     not apply the if rule after any tactic application, since       tion criterion is to select the linear strategy that, when added
     tactic applications may alter the formula measures, dis-        to the incumbent selected strategy set, maximizes the virtual
     abling the staged search.                                       best strategy performance for a given instance set. Starting
  4. Certain candidate values are preselected for numerical          from an empty set, we apply this criterion to add one linear
     tactic parameters, try-for timeouts, and numerical probe        strategy at a time to the set until n strategies are selected.
     comparisons.                                                    Consistent with the entire synthesis process, performance is
                                                                     measured by the average PAR-10 score.
  5. Do not apply the tactic nla2bv more than once in a se-
     quence of tactic applications.
                                                                     B     Additional Experimental Details
  6. Apply the tactic bit-blast only immediately after apply-
     ing the tactic simplify.                                        B.1    Training and Testing Benchmarks
   We recognize that certain simplification rules might elim-        In experiments for specific benchmark classes (Section 5.3),
inate parts of the search space that include effective strate-       we used the same experimental benchmark sets that were
gies. Nevertheless, these rules are instrumental in substan-         used in the FastSMT study [Balunovic et al., 2018]. They
tially reducing the vast search space and enabling efficient         divided each benchmark set, i.e., Sage2, core, AProVE,
search techniques like the stage search. Our empirical exper-        leipzig, and hycomp, into a training set, a validation set,
imental results strongly indicate that the remaining space still     and a test set. For Z3alpha synthesis, we retained the test
encompasses robust strategies.                                       set for evaluation and merged the training and validation sets
Tactic and Parameter Pools: We list the pool of tactic and           to form the Z3alpha training benchmark set P . Within it,
parameter candidates for each tested SMT logic in a series           the FastSMT training set was specifically used as the train-
of tables, specifically from Table 4 to Table 9. Note that           ing subset P1 for the first-stage MCTS.
the candidate selection is identical for both Z3alpha and               For QF LIA, QF LRA, and QF S experiments, we ran-
FastSMT.                                                             domly selected 750 instances to constitute the Z3alpha
Staged Search Framework: Figure 4 illustrates the staged             training set P , while designating all remaining instances in
MCTS framework. A set of n linear strategies is selected             the SMT-LIB as the test set. From P , 250 instances were
from the first-stage MCTS, and these linear strategies are syn-      chosen as the stage-1 training subset P1 . Our experiments
thesized into one final combined strategy SF in the second-          showed that this training size was sufficient to develop robust
stage MCTS. Note that we may opt for a subset P1 of the              strategies for the logic. In these experiments, P1 served as the
complete training benchmark set P for the first stage. This is       training set for FastSMT, and the set difference P \ P1 con-
because each stage-1 MCTS simulation can be expensive for            stituted the validation set, aligning with the FastSMT bench-
a large training set, since it involves calling an SMT solver        mark split sizes for large sets. All competing solvers were
for every training instance. After selecting linear strategies       evaluated on the same test set.
using a smaller subset, we can evaluate the selected strategies
across all instances in P , with results cached for the second       B.2    Experimental Results in PAR-2 and PAR-10
stage. This approach eliminates the resource-intensive need          Table 2 and Table 3 show the experimental results as average
to evaluate every strategy explored in the first stage on the full   PAR-2 and PAR-10 scores, respectively. The PAR-2 score
set P , while still providing larger-scale evaluation data for the   was calculated based on the solver runtime for each success-
second-stage MCTS.                                                   fully solved instance in the test set, and a penalty of twice
Selection Criteria of Linear Strategies: After the first-            the timeout for unsolved instances. Similarly, the PAR-10
stage MCTS, we select n linear strategies for the second-            score imposed a penalty of ten times the timeout for the un-
stage synthesis. This selection is performed iteratively from        solved. A lower score in both PAR-2 and PAR-10 indicates
the pool of linear strategies explored in the first stage using a    superior performance. Notably, the PAR-2 and PAR-10 re-
        Timeout(s)     Logic    Benchmark      Test Size   Z3alpha   Z3alpha0      FastSMT         Z3    CVC5     Z3str4
                                Sage2            6444        11.01     12.97         11.30      13.68    14.02        -
                     QF BV
                                core              270         1.06      1.14          0.89       6.08     5.21        -
                                AProVE           1712        1.27       1.64          2.89       3.28     6.62        -
                     QF NIA
                                leipzig            68        2.13       2.58          2.87       2.63    15.72        -
            10
                     QF NRA     hycomp           1982        1.90       1.95          2.29       3.19     3.17        -
                     QF LIA     entire logic    12476        5.23         -          13.88        5.52    7.61        -
                     QF LRA     entire logic     1003        5.93         -           5.92       6.46     7.74        -
                     QF S       entire logic    18173        0.41         -             -        0.57     0.42      0.71
            60       QF BV      Sage2            6444        43.57        -          43.82       57.41   38.77        -
           300       QF BV      Sage2            6444       163.26        -         181.00      214.23   80.71        -

Table 2: Z3alpha vs. SOTA Solvers: Average PAR-2 score on the selected SMT-LIB benchmarks across six SMT logics ( In each
experiment, the result of the leading tool is highlighted in bold, while the second-best is underscored.)

       Timeout(s)     Logic     Benchmark      Test Size   Z3alpha   Z3alpha0     FastSMT        Z3      CVC5     Z3str4
                                Sage2            6444        48.66     59.97        50.27      64.01     64.71        -
                     QF BV
                                core              270         1.36      1.49         0.89      25.64     19.14        -
                                AProVE           1712         5.45      7.64        10.63      11.27     30.69        -
                     QF NIA
                                leipzig            68         9.19     11.29        12.28      10.87      75.72       -
            10
                     QF NRA     hycomp           1982         8.82      9.27        10.98      14.69     14.75        -
                     QF LIA     entire logic    12476        24.23        -         68.93       25.81     35.78       -
                     QF LRA     entire logic     1003        27.06        -         26.74      29.67     36.85        -
                     QF S       entire logic    18173         1.23        -            -        2.00       1.72     2.96
            60       QF BV      Sage2            6444       188.30        -        198.68      260.47    145.52       -
           300       QF BV      Sage2            6444       743.14        -        837.61      940.12    240.86       -

Table 3: Z3alpha vs. SOTA Solvers: Average PAR-10 score on the selected SMT-LIB benchmarks across six SMT logics ( In each
experiment, the result of the leading tool is highlighted in bold, while the second-best is underscored.)


sults strongly aligned with the results of the number of solved
instances, as presented in Table 1.
                                                                                     Tactic           Parameter
                                                                                                       elim and
                                                                                                     blast distinct
                                                                                                       local ctx
                                                                                                          som
                                                                                simplify
                                                                                                           flat
                                                                                                     pull cheap ite
                                                                                                       hoist mul
                                                                                                      push ite bv
                                                                                propagate-values      push ite bv
                                                                                ctx-simplify                 -
                                                                                elim-uncnstr                 -
                                                                                solve-eqs                    -
                                                                                purify-arith                 -
                                                                                max-bv-sharing               -
                                                                                aig                          -
                                                                                reduce-bv-size               -
                                                                                ackermannize bv              -
                                                                                bit-blast                    -
                                                                                smt                  random seed
                                                                                sat                          -
                                                                                qfbv                         -

                                                                     Table 4: Selected tactic and parameter candidates for QF BV
                                                                              Tactic               Parameter
                Tactic           Parameter                                                          elim and
                                                                                                  blast distinct
                                  elim and
                                                                                                    local ctx
                                blast distinct
                                                                                                       som
                                  local ctx
                                                                        simplify                       flat
                                     som
                                                                                                 pull cheap ite
        simplify                      flat
                                                                                                  push ite arith
                                   hi div0
                                                                                                    hoist ite
                                pull cheap ite
                                                                                                    arith lhs
                                  hoist mul
                                                                        propagate-values           push ite bv
                                 push ite bv
                                                                        ctx-simplify                     -
        propagate-values         push ite bv
                                                                        elim-uncnstr                     -
        ctx-simplify                    -
                                                                        solve-eqs                        -
        elim-uncnstr                    -
                                                                        propagate-ineqs                  -
        solve-eqs                       -
                                                                                               add bound lower
        max-bv-sharing                  -                               add-bounds
                                                                                               add bound upper
        nla2bv               nla2bv max bv size
                                                                        normalize-bounds                 -
        bit-blast                       -
                                                                        lia2pb                  lia2pb max bits
        smt                     random seed
                                                                        smt                       random seed
                                 inline vars
                                                                        qflia                            -
        qfnra-nlsat                 factor
                                     seed                      Table 7: Selected tactic and parameter candidates for QF LIA
        lia2card                        -
        card2bv                         -                                        Tactic          Parameter
        cofactor-term-ite               -                                                         elim and
        qfnia                           -                                                       blast distinct
                                                                           simplify               local ctx
Table 5: Selected tactic and parameter candidates for QF NIA
                                                                                                     som
                                                                                                     flat
                                                                           propagate-values            -
                                                                           ctx-simplify                -
                Tactic           Parameter                                 elim-uncnstr                -
                                                                           solve-eqs                   -
                                  elim and
                                                                           smt                  random seed
                                blast distinct
                                                                           qflra                       -
                                  local ctx
                                     som                       Table 8: Selected tactic and parameter candidates for QF LRA
        simplify                      flat
                                   hi div0                                       Tactic          Parameter
                                pull cheap ite
                                                                                                  elim and
                                  hoist mul
                                                                                                blast distinct
                                 push ite bv
                                                                           simplify               local ctx
        propagate-values         push ite bv                                                         som
        ctx-simplify                    -                                                            flat
        elim-uncnstr                    -                                  propagate-values            -
        solve-eqs                       -                                  ctx-simplify                -
        max-bv-sharing                  -                                  elim-uncnstr                -
        nla2bv               nla2bv max bv size                            solve-eqs                   -
        bit-blast                       -                                  ext str                     -
        smt                     random seed                                ext strSimplify             -
                                 inline vars                               ext strToRegex              -
        qfnra-nlsat                 factor                                 ext strToWE                 -
                                     seed
                                                                           arr                         -
        qfnra                           -
                                                                           las                         -
Table 6: Selected tactic and parameter candidates for QF NRA               smt                  random seed

                                                                Table 9: Selected tactic and parameter candidates for QF S
