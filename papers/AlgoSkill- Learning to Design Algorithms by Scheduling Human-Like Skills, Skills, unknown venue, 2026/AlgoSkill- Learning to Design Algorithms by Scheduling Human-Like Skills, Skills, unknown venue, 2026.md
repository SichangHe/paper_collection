                                             AlgoSkill: Learning to Design Algorithms by Scheduling Human-Like
                                                                            Skills

                                                               Xinyuan Song1 Zekun Cai2,3 Liang Zhao1
                                                1
                                                  Emory University, Atlanta, GA, USA 2 The University of Tokyo, Tokyo, Japan
                                                                          3
                                                                            LocationMind, Tokyo, Japan
                                                 {xinyuan.song,liang.zhao}@emory.edu, caizekun@csis.u-tokyo.ac.jp



                                                              Abstract                               read the constraints, infer a feasible complexity
                                                                                                     class, choose an algorithmic paradigm, justify cor-
                                             Designing an algorithm from a natural-
                                                                                                     rectness, and refine the solution until it satisfies
arXiv:2606.29999v1 [cs.AI] 29 Jun 2026




                                             language problem statement requires iden-
                                             tifying the problem structure, reading con-             time and memory limits. Human programmers usu-
                                             straints, choosing a suitable paradigm, check-          ally handle this through a sequence of reusable
                                             ing correctness, and refining complexity. Ex-           steps: problem abstraction, brute-force construc-
                                             isting large language model (LLM) methods               tion, state design, data-structure selection, proof
                                             often rely on direct generation or generic              checking, and complexity refinement, echoing clas-
                                             self-refinement, leaving these steps implicit.          sic views of algorithm selection and reusable tem-
                                             We propose AlgoSkill, which models algo-
                                                                                                     poral abstractions (Rice, 1976; Burke et al., 2013;
                                             rithm design as sequential decision-making
                                             over a typed library of algorithmic skills, in-         Sutton et al., 1999). This suggests that algorithm
                                             cluding abstraction, constraint analysis, state         design is better viewed as a state-dependent pro-
                                             design, data-structure selection, proof check-          cess over reasoning skills, rather than as a single
                                             ing, counterexample construction, and com-              generation step.
                                             plexity refinement. A learned scheduler pro-               Large language models (LLMs) have made
                                             poses skills from the current design state,             strong progress in code generation. Codex (Chen
                                             while a Monte Carlo Tree Search (MCTS)                  et al., 2021), AlphaCode (Li et al., 2022), and
                                             controller explores skill sequences using ver-
                                                                                                     DeepSeek-Coder (Guo et al., 2024) perform well
                                             ification feedback from compilation, testing,
                                             stress testing, and complexity analysis. Ex-            on HumanEval and competitive programming
                                             periments on competitive programming and                benchmarks, especially with large sampling bud-
                                             combinatorial optimization benchmarks show              gets. Prompting and revision methods, such as
                                             that AlgoSkill improves over direct LLM                 chain-of-thought reasoning (Wei et al., 2022), self-
                                             generation, chain-of-thought prompting, self-           refinement (Madaan et al., 2023), Reflexion (Shinn
                                             refinement, and MCTS without typed skills.              et al., 2023), and Tree of Thoughts (Yao et al.,
                                             Ablations show that typed skills, verification-
                                                                                                     2023), improve multi-step reasoning. Still, these
                                             based repair, and search-based scheduling
                                             each contribute to performance. These results           methods usually operate on free-form text or code.
                                             support treating automatic algorithm design             They do not make the algorithmic design steps part
                                             as verification-guided skill scheduling rather          of the search space. As a result, LLMs can fail on
                                             than one-shot code generation. Our code is              hard problems by choosing the wrong paradigm,
                                             available at: https://github.com/Hik289/                missing the intended complexity, defining an in-
                                             algorithm_skill.git.                                    complete state, or using a greedy rule without a
                                                                                                     valid argument (Figure 1).
                                         1   Introduction
                                                                                                        Search-based systems offer another path. Fun-
                                         Designing efficient algorithms from natural-                Search (Romera-Paredes et al., 2024) uses evolu-
                                         language problem statements is difficult be-                tionary program search with LLM-generated mu-
                                         cause the solver must do more than write code;              tations, and AlphaEvolve (Novikov et al., 2025)
                                         this challenge appears across program synthesis,            extends this idea to broader algorithm design tasks.
                                         code generation, and competitive-programming                These systems show that search is useful, but
                                         benchmarks (Gulwani, 2011; Alur et al., 2013;               searching over raw programs or free-form solution
                                         Hendrycks et al., 2021; Li et al., 2022; Jain et al.,       drafts can be hard to inspect and reuse. A more
                                         2024). It must understand the input/output format,          structured alternative is to search over algorithmic

                                                                                                 1
                                                               Figure 2: AlgoSkill overview. Given a problem q, the
                                                               skill scheduler πθ uses MCTS to select from twenty
Figure 1: Core intuition. Existing LLM methods of-             typed algorithmic skills. Skill applications update the
ten rely on free-form generation, which can lead to            design state, which is decoded into a candidate algo-
paradigm, complexity, or proof errors. AlgoSkill struc-        rithm and scored by a verifier to improve scheduling.
tures algorithm design as typed, verifiable skill steps.

                                                               where D is the natural-language statement, I and
skills, where each step has a typed role and can be            O are the input and output formats, K contains the
checked by verification signals.                               constraints, and M is the evaluation metric.
   Reusable skill libraries have also proved use-                Let O = {o1 , o2 , . . . , oN } be the skill library,
ful in language-agent settings (Chen et al., 2023;             with N = 20 in our experiments. At step t, Algo-
Wang et al., 2023). We propose AlgoSkill, a frame-             Skill keeps a design state
work for skill-guided algorithm design. AlgoSkill
uses a library of twenty typed algorithmic skills,                      st = (q, rt , pt , xt , κt , Et , ht ) ∈ S.   (2)
including problem abstraction, constraint analy-
                                                               Here, rt stores the parsed problem type, task type,
sis, brute-force construction, state design, data-
                                                               and key entities; pt is the current solution plan; xt
structure selection, proof checking, counterexam-
                                                               is the current code, if available; κt is the current
ple construction, and complexity refinement. Given
                                                               time and memory estimate; Et stores failed tests,
a design state, a scheduler selects useful skills, and
                                                               counterexamples, and verifier messages; and
a Monte Carlo Tree Search controller explores skill
sequences under feedback from compilation, test-                              ht = (o0 , o1 , . . . , ot−1 )          (3)
ing, stress testing, and complexity analysis. In
this way, AlgoSkill turns algorithm design into a              records the skills used so far.
process of skill selection, composition, and verifi-              At each step, only skills whose preconditions
cation.                                                        hold can be selected:
   Our contributions are:                                            Ovalid (st ) = {oi ∈ O : ϕpre
                                                                                               i (st ) = 1}.          (4)
• We define a library of twenty typed algorithmic              The scheduler samples a valid skill
  skills for common steps in algorithm design.
                                                                      ot ∼ πθ (· | st ),        ot ∈ Ovalid (st ),    (5)
• We introduce AlgoSkill, a skill-guided frame-
  work that composes these skills under verifica-              and the selected skill updates the state by
  tion feedback.
                                                                                    st+1 = T (st , ot ),              (6)
• We evaluate AlgoSkill on competitive program-
                                                               where T : S × O → S is the skill transition.
  ming and combinatorial optimization bench-
                                                                  After at most Tmax steps, the terminal state
  marks, where it improves over direct generation,
                                                               is decoded into a candidate algorithm, aT =
  prompting, refinement, and search baselines.
                                                               Decode(sT ), including both code and explanation.
                                                               A full trajectory is
2   Problem Formulation
                                                                        τ = (s0 , o0 , s1 , o1 , . . . , sT , aT ).   (7)
As shown in Figure 2, we view algorithm design as
a sequence of choices over typed algorithmic skills.           The scheduler is trained to maximize the expected
A problem instance is written as                               verifier reward:

               q = (D, I, O, K, M),                 (1)                       max Eτ ∼πθ [R(aT , q)] .                (8)
                                                                                θ


                                                           2
The reward contains correctness, efficiency, expla-                   on the design state, and assign credit to specific al-
nation, repair, and risk terms:                                       gorithmic decisions. The full skill descriptions and
                                                                      the complete library table are given in Appendix A.
    R(aT , q) = Rcor (aT , q) + Reff (aT , q)
                                                          (9)         4     Skill Scheduling and Search
    + Rexpl (aT , q) + Rrep (τ, q) − Rrisk (τ, q).
                                                                      AlgoSkill schedules skills in three steps: it first
We define these terms in Section 5.
                                                                      masks invalid skills, then scores the remaining
   This setup keeps the original constraints K sepa-
                                                                      skills with a learned policy, and finally uses MCTS
rate from the inferred complexity κt , and separates
                                                                      to search over skill sequences.
intermediate code xt from the final algorithm aT .
It also avoids a naming conflict between the out-                     4.1    Valid-Skill Filter
put format O and the skill library O. Compared
                                                                      At state st , a skill can be selected only if its precon-
with direct code generation, AlgoSkill keeps an
                                                                      dition is satisfied:
explicit design state. Compared with free-form
self-refinement, each update is a typed skill step.                          Ovalid = {oi ∈ O : ϕpre
                                                                              t                  i (st ) = 1}.             (12)
Compared with evolutionary search over programs,
it searches over skill trajectories. Figure 3 gives                   The preconditions are checked from fields in the
one example on Maximum Subarray Sum.                                  design state. For example, if the current complexity
                                                                      estimate suggests a timeout risk, the filter enables
3     Algorithmic Skill Library                                       ocomplex , ods , odecomp , and omono . If Et contains
AlgoSkill uses a typed library of algorithmic skills.                 failed tests or verifier messages, the filter enables
Each skill is written as                                              ocounter , ostate , oinv , and oexchange . This masking
                                                                      step removes skills that do not fit the current state
          oi = (ϕpre       post
                 i , τi , ϕi    , ci , vi , ri ),        (10)         and reduces the branching factor in search.

where ϕpre
         i   checks whether the skill is applicable,                  4.2    Learned Skill Policy
τi updates the design state, ϕpost
                                i   specifies the ex-                 The scheduler uses a neural policy fθ to score valid
pected outcome, ci records the intended complexity                    skills:
effect, vi defines the verification rule, and ri lists
common failure modes.                                                            πθ (o | st ) = softmax(fθ (st )).         (13)
   The library contains twenty skills:
                                                                      The input to fθ includes the parsed problem type,
O = {oabs , oconstraint , obrute , omono , oinv , ostate ,            constraint profile, current plan pt , current complex-
        odecomp , orelax , oexchange , ods , odual , ocounter ,       ity estimate κt , recent failure signals in Et , and
                                                                      skill history ht . A greedy scheduler, used as one
        ocomplex , oanalogy , omath , osym , orandom ,
                                                                      baseline, selects
        oapprox , ocache , oparallel }.                  (11)
                                                                                   ot = arg max πθ (o | st ).              (14)
   These skills cover the main steps that appear in                                          o∈Ovalid
                                                                                                t

algorithm design. Early-stage skills, such as oabs
and oconstraint , parse the problem and infer the fea-                4.3    MCTS Search Controller
sible complexity range. Construction skills, such as                  The search controller uses MCTS (Silver et al.,
obrute , ostate , and ods , build candidate algorithms                2017) over design states. Each node is a state s,
or replace inefficient operations. Verification and                   and each edge is a skill application o.
repair skills, such as oinv , oexchange , ocounter , and                 Selection. Starting from s0 , the controller se-
ocomplex , check correctness, test failure cases, and                 lects the skill with the largest UCB score (Auer
refine inefficient solutions. The remaining skills                    et al., 2002):
handle special structures, including decomposition,                                       "                          p           #
relaxation, duality, formulas, symmetry, randomiza-                    ∗                                                N (s)
                                                                      o = argmax Q(s, o) + βPθ (o | s)                             .
tion, approximation, caching, and parallelization.                           o∈Ovalid (s)                          1 + N (s, o)
   We keep the library typed rather than treating                                                                          (15)
skills as free-form prompts. This lets the scheduler                  Here, Q(s, o) is the current value estimate for ap-
mask invalid actions, track the effect of each skill                  plying skill o at state s, Pθ (o | s) is the policy prior,

                                                                  3
Figure 3: Concrete skill trajectory. Example on Maximum Subarray Sum. Starting from s0 , AlgoSkill applies
oabs to identify the optimization and prefix-sum structure, oconstraint to infer an O(n) time and O(1) space target,
obrute to build an O(n3 ) baseline, ostate to define the DP state dp[i] = max sum ending at i, and ocomplex to reach
Kadane’s O(n) algorithm. Each transition st → st+1 is typed and precondition-checked, and the terminal state
decodes to a verified solution.


N (s) and N (s, o) are visit counts, and β controls           We also run the implementation on input sizes n1 <
exploration.                                                  n2 < · · · < nk and fit
   Expansion. The selected skill produces a new
state:                                                                        T̂ (n) = cnα (log n)γ .             (21)
                  s′ = T (s, o∗ ).             (16)           If the fitted exponent α disagrees with the symbolic
  Simulation. The new state is decoded into a                 estimate, AlgoSkill adds a complexity-risk penalty.
candidate algorithm,                                             Algorithm 1 gives the full search procedure.

                  a = Decode(s′ ),                 (17)       5     Training with Verification Rewards
                                                              AlgoSkill trains the scheduler πθ with policy-
which is evaluated by the verifier using compilation,
                                                              gradient reinforcement learning. The reward is
unit tests, stress tests, and complexity checks.
                                                              computed by an external verifier, so the scheduler
  Backpropagation. The verifier reward is propa-
                                                              is trained from signals that are tied to execution,
gated to the visited state-skill pairs:
                                                              complexity, and repair quality rather than from final
         Q(s, o) ← (1 − η)Q(s, o) + ηR.            (18)       pass/fail labels alone.

The visit counts are updated by N (s) ← N (s) + 1             5.1    Reward Decomposition
and N (s, o) ← N (s, o) + 1.                                  For a trajectory τ = (s0 , o0 , . . . , sT , aT ), the re-
                                                              ward is
4.4 Symbolic Complexity Tracking
For complexity checking, AlgoSkill represents                 R(aT , q) = Rcor + Reff + Rexpl + Rrep − Rrisk .
an algorithm plan as an operation graph Ga =                                                            (22)
(Va , Ea ), where nodes are operation blocks and
edges denote data flow. The complexity is esti-                 The correctness term combines several test sig-
mated by simple composition rules:                            nals:
                                      Q
C(A; B) = C(A) + C(B),      C(loop) = i ni C(body),
                                                               Rcor = w1 Rcpl + w2 Runit + w3 Rstr + w4 Rora ,
 C(sort) = O(n log n),      C(BFS) = O(|V | + |E|),
                                                                                                                 (23)
C(heap) = O(k log n),        C(seg) = O((u + q) log n),
 C(DP) = O(|S| · |A|).
                                                              where Rcpl ∈ {0, 1} is compilation success,
                                                              Runit ∈ [0, 1] is the public-test pass rate, Rstr is the
Given the maximum input size nmax , the time and              stress-test pass rate against the brute-force oracle,
memory penalties are                                          and Rora is the oracle agreement rate.
                                                                 The efficiency term penalizes time, memory, and
 PT (a, q) = [log T (a, nmax ) − log Tmax ]+ , (19)           empirical runtime violations:

  PM (a, q) = [log M (a, nmax ) − log Mmax ]+ .               Reff = −λT PT (a, q)−λM PM (a, q)−λR Prt (a, q).
                                             (20)                                                        (24)

                                                          4
Algorithm 1 AlgoSkill Search Procedure                    The full loss is
Require: Problem q, skill library O, scheduler πθ ,
                                                                 L = LRL + λV LV + λH Lentropy ,            (29)
    verifier V , search budget B
Ensure: Best verified algorithm a∗ found in               with entropy regularization
    search tree T                                                         X
 1: Construct the initial state s0 from q                  Lentropy = −       πθ (o | st ) log πθ (o | st ). (30)
 2: Initialize T with root s0                                                o
 3: for b = 1, . . . , B do                               This term keeps the scheduler from collapsing too
 4:     Select a state s from T by tree traversal         early to a small set of skills.
 5:     Compute valid skills Ovalid (s) = {o :
    ϕpre
      o (s) = 1}                                          5.3    Skill Credit Assignment
 6:     Select             o∗         √        =        A trajectory may contain several useful or harmful
                                         N (s)
    arg maxo Q(s, o) + βPθ (o | s) 1+N (s,o)              skill choices, so AlgoSkill assigns credit at both
                                                          the step level and the state-action level. The local
 7:     Apply the skill: s′ = T (s, o∗ )
                                                          change after applying ot is
 8:     Decode s′ into a candidate algorithm a′
 9:     Estimate symbolic time T (a′ ) and memory                       ∆t = R(st+1 ) − R(st ),             (31)
    M (a′ )
10:     Evaluate a′ with verifier V and obtain re-        and the corresponding skill value is updated by
    ward R(a′ , q)
                                                                    Q(ot ) ← (1 − η)Q(ot ) + η∆t .          (32)
11:     Add s′ to T
12:     Update Q(s, o) ← (1 − η)Q(s, o) + ηR              AlgoSkill also learns a context-dependent value
13:     Update N (s) ← N (s) + 1 and N (s, o) ←           function
    N (s, o) + 1
14:     Assign local skill credit ∆t = R(s′ )−R(s)                      Qω (s, o) = E[R | s, o],            (33)
    and update Qω (s, o)
                                                          which estimates the return of applying skill o in
15:     Update πθ using the trajectory reward
                                                          state s. The policy and this value function are
16: end for
                                                          trained together using trajectory-level returns.
17: return best verified algorithm a∗ found in T
                                                          6     Experiments
  The explanation term checks whether the final           6.1    Experimental Setup
answer contains the main algorithm idea, pseu-          We evaluate AlgoSkill on a randomly sam-
docode, complexity analysis, and correctness ar-        pled benchmark from four public competitive-
gument:                                                 programming platforms: Codeforces (Codeforces,
Rexpl = λI Ridea + λP Rpsd + λC Rcplx + λA Rarg .       2026), AtCoder (AtCoder Inc., 2026), Kattis (Kat-
                                                 (25) tis, 2026), and LeetCode Hard (LeetCode, 2026).
  The repair term gives credit when a failed candi- The benchmark contains 275 problems in total:
date is turned into a passing one:                      100 from Codeforces, 100 from AtCoder, and 75
                                                        from LeetCode Hard. The problems cover com-
          Rrep = λfix 1[failed → passing].       (26) mon algorithmic paradigms, including dynamic
                                                        programming, graph algorithms, binary search,
5.2 Policy Gradient Update                              greedy methods, data structures, and mathemat-
The scheduler is updated by                             ical formulas. All methods receive the same
              "T −1                                  # problem statement, without editorial hints, solu-
                X                                       tion tags, or official explanations. We evaluate
∇θ J(θ) = E         ∇θ log πθ (ot | st ) (R − b(st )) , API and released-model backbones using provider
                t=0
                                                 (27) documentation or model reports for GPT-family
where b(st ) = Vω (st ) is a learned value baseline. and gpt-oss models (OpenAI, 2024, 2025, 2026),
The value model is trained with                         Claude models (Anthropic, 2024, 2026), Gem-
                                                        ini (Google, 2025), Llama (Meta AI, 2024, 2025),
                                    2
              LV = (Vω (st ) − R) .              (28) and Qwen (Qwen Team, 2025).

                                                      5
   We report pass@1 and pass@5 as the main met-              Table 1: Cross-platform 275-problem benchmark cor-
rics. pass@1 measures whether a single generated             rectness (%, n = 275) on positive-gain backbones. ∆
                                                             denotes AlgoSkill minus Direct.
solution passes all tests, while pass@5 measures
whether at least one of five independently sampled            Method                            Haiku           Gemini
solutions passes all tests. Implementation details,
                                                              Direct                        78.2 (215/275)    11.6 (32/275)
including the backbone LLM, MCTS rollout bud-                 CoT                           79.3 (218/275)    16.0 (44/275)
get, exploration coefficient, and reward weights,             AlgoSkill                     80.7 (222/275)    18.2 (50/275)
are reported in Appendix B.                                   ∆ (AlgoSkill vs. Direct)           +2.5             +6.6

6.2   Baselines
                                                             Table 2: CP-275 T-opt (%, judged ≈175 problems per
We compare AlgoSkill with the following base-                method) on positive-gain backbones. T-opt is computed
lines. Direct LLM generates a solution in a single           over problems where the judge returned a determinate
forward pass. CoT LLM uses chain-of-thought                  complexity verdict.
prompting (Wei et al., 2022) to produce a reasoning
                                                              Method                           Haiku            GPT-4o
trace before code generation. Self-Refine (Madaan
                                                              Direct                       91.4% (160/175)   94.5% (120/127)
et al., 2023) generates an initial solution, critiques        CoT                          94.8% (165/174)   95.9% (117/122)
it, and revises it for up to three rounds. Reflex-            AlgoSkill-G                  96.0% (168/175)   96.2% (102/106)
                                                              AlgoSkill                    93.7% (163/174)    97.6% (83/85)
ion (Shinn et al., 2023) uses natural-language re-            ∆ (AlgoSkill-G vs. Direct)       +4.6 %            +1.7 %
flections from failed attempts to guide up to five
retries. MCTS (no skills) applies Monte Carlo
Tree Search (Silver et al., 2016, 2017; Yao et al.,          from 91.4% to 96.0%, while the full AlgoSkill vari-
2023) over free-form reasoning steps rather than             ant reaches 97.6% on GPT-4o.
typed skill applications. AlgoSkill w/o MCTS
(Greedy) uses the learned scheduler greedily with
                                                             6.4    Skill Ablation
the same skill library but without tree search. Algo-
Skill Full uses the complete framework, including            Table 3 reports the version 1 leave-one-skill-out
typed skills, MCTS scheduling, complexity-aware              sensitivity analysis with 60 sampling runs. Each
rewards, repair reward, and skill credit assignment.         variant removes one skill and is evaluated on the
   For the Hard Benchmark in Section 10, we also             full benchmark sample.
compare with two published algorithm design sys-                Table 3 reports a leave-one-skill-out sensitivity
tems. MapCoder (Islam et al., 2024) is a multi-              analysis. Removing Problem Abstraction causes
agent framework for competitive programming that             the largest drop, reducing pass@1 from 95.0% to
uses separate agents for retrieval, planning, code           73.3%, showing that early problem typing is crit-
generation, and debugging. We implement Map-                 ical for skill scheduling. Removing Brute-Force
Coder following the original paper and evaluate it           Oracle or State Design lowers both pass@1 and
on our benchmark with Claude 3 Haiku (Anthropic,             pass@5 to 88.3%, while removing Data-Structure
2024) and Gemini-2.5-Flash (Google, 2025) back-              Substitution or Constraint Reading reduces pass@1
bones. FunSearch (Romera-Paredes et al., 2024)               to 85.0%. Overall, the full skill library performs
uses an evolutionary LLM loop for mathematical               best, suggesting that abstraction, verification, state
function discovery. Since FunSearch is designed              design, and efficiency-oriented refinement provide
for open-ended combinatorial discovery rather than           complementary gains.
standard competitive programming, we report its
published solve rates on combinatorial tasks as a            6.5    MCTS Ablation
reference point.
                                                             Table 4 evaluates the search controller by replac-
6.3   Main Results                                           ing the greedy scheduler with beam search while
Table 1 reports the audited version 2 CP-275 re-             keeping the same hard 20-problem sample.
sults after filtering to positive-gain backbones. Al-          Greedy Policy and Beam Search achieve the
goSkill improves Haiku from 78.2% to 80.7% and               same pass@1 of 90.0%. Greedy Policy has a
improves Gemini from 11.6% to 18.2%.                         small pass@5 advantage, solving 19/20 problems
  Table 2 shows the positive T-opt results.                  within five attempts compared with 18/20 for Beam
AlgoSkill-G improves time-optimality on Haiku                Search.

                                                         6
Table 3: Leave-one-skill-out sensitivity analysis with                                        MCTS Controller Ablation
AlgoSkill Greedy and 60 sampling runs. Each row re-                                             (Haiku-4-5, HB-20)
moves one skill from the full skill library. Results are                          100
reported as solved problems over the total number of




                                                                  Pass rate (%)
evaluated trials, with pass rates in parentheses.                                                95%
                                                                                   95

                                                                                        90%                         90%   90%
 Variant                           pass@1        pass@5                            90
 Full skill library           57/60 (95.0) 58/60 (96.7)
                                                                                   85                                     pass@1
 w/o Problem Abstraction      44/60 (73.3)     51/60 (85.0)
 w/o Brute-Force Oracle       53/60 (88.3)     53/60 (88.3)                                                               pass@5
 w/o State Design             53/60 (88.3)     53/60 (88.3)                        80
 w/o Monotonicity Detection   52/60 (86.7)     52/60 (86.7)                             Greedy Policy           Beam Search
 w/o Counterexample Check     52/60 (86.7)     52/60 (86.7)                             (AlgoSkill-G)              (k=3)
 w/o Complexity Refinement    52/60 (86.7)     52/60 (86.7)
 w/o Data-Structure Sub.      51/60 (85.0)     52/60 (86.7)       Figure 4: MCTS/search controller ablation. Greedy
 w/o Constraint Reading       51/60 (85.0)     52/60 (86.7)       Policy and Beam Search achieve identical pass@1 of
                                                                  90.0%; Greedy Policy has a small pass@5 advantage.
Table 4: MCTS/search controller ablation on a 20-
problem hard sample with Haiku-4-5 and three seeds.               Table 5: Standard code-generation benchmarks on
pass@1 is over 60 trajectories; pass@5 is over 20 prob-           Gemini-2.5-Flash. Direct uses the full benchmark; other
lems.                                                             methods use 50-problem subsets. AlgoSkill pass@1 is
                                                                  averaged over three runs per problem.
      Search Controller   Passed    p@1         p@5
                                                                  Method                    n           HumanEval          MBPP
      Greedy Policy       54/60      90.0    95.0 (19/20)
      Beam Search (k=3)   54/60      90.0    90.0 (18/20)         Direct       164 / 100 90.85% (149/164) 100.00% (100/100)
                                                                  AlgoSkill†      50     94.67% (155/164) 100.00% (50/50)
                                                                  CoT†            50       98.00% (49/50)  100.00% (50/50)
6.6     Standard Code Generation Benchmarks                       Reflexion†      50      100.00% (50/50)  100.00% (50/50)
                                                                  Self-Refine†    50      100.00% (50/50)  100.00% (50/50)
We evaluate AlgoSkill on HumanEval (Chen et al.,
2021) and MBPP (Austin et al., 2021) using
Gemini-2.5-Flash. These standard benchmarks                       algorithmic solutions from new benchmark.
contain function-level problems that are likely well                 Table 6 shows that AlgoSkill keeps its advantage
represented in LLM training corpora. They test                    across backbone sizes. On the procedurally gener-
whether AlgoSkill preserves performance on famil-                 ated benchmark, where direct memorization is un-
iar coding tasks while improving on novel hard                    likely, AlgoSkill achieves the highest T-optimality
problems.                                                         with both Haiku (89% vs. 45% for Direct LLM and
   Table 5 shows that AlgoSkill remains strong                    68% for CoT) and Llama 8B (100% vs. 63% for
on standard function-level code generation bench-                 Direct LLM and 57% for CoT). This suggests that,
marks. On HumanEval, AlgoSkill reaches 94.67%                     even under a lower-memorization setting, explicit
on the 50-problem subset, while Direct obtains                    skill guidance leads to more complexity-optimal
90.85% on the full set. On MBPP, AlgoSkill                        algorithm design than direct prompting or CoT.
reaches 100.00%, matching the strongest baselines
on the evaluated subset.                                          6.8              Post-Cutoff Real-World Benchmark
                                                                  The synthetic rule-based benchmark controls for
6.7     Contamination Analysis                                    contamination by construction, but one may still
A persistent concern is that performance gaps on                  ask whether its artificial problem structure transfers
competitive-programming benchmarks may reflect                    to real contest settings. To address this concern, we
editorial memorization (Chen et al., 2021) rather                 curate a real-world benchmark of 40 problems from
than algorithmic reasoning. We address this con-                  AtCoder and LeetCode contest rounds released af-
cern along two axes. First, the rule-based bench-                 ter 2024-08-01, which is later than the pretraining
mark in Table 18 provides contamination-free evi-                 cutoff of the oldest model in our evaluation suite.
dence because the problems are procedurally gen-                     The benchmark contains 40 problems, sampled
erated. Second, we compare a large backbone,                      across Easy, Medium, and Hard difficulty levels
Claude Haiku-4, with a smaller backbone, Llama                    from both platforms. We evaluate each method
3.1 8B, which has less capacity to memorize new                   using the public example test cases. We test four

                                                              7
                                                                                                                                                                                            AlgoSkill Improves Across Training Cutoff Regimes
Table 6: Contamination analysis on the 200-problem                                                                                                              100
                                                                                                                                                                                                                                 Post-cutoff ( 2024-11)
rule-based benchmark across six backbone/method com-
                                                                                                                                                                80       Pre-cutoff
                                                                                                                                                                        ( 2023-12)
binations. T/S-opt are conditioned on correctness and                                                                                                                                                               67%                             65%
judged by an LLM-as-judge.                                                                                                                                      60                                                                                                    57%




                                                                                                                                                  Correct (%)
                                                                                                                                                                40
Method                                Backbone                                         Correct                  T-opt         S-opt                                                   27%

                                                                                                                                                                20                                                                                             Direct LLM
                                                                                                                                                                                                                                                               CoT
Direct LLM Haiku                                                           75% (151/200)                        45%  95%                                                                                                                                       AlgoSkill-G (Greedy)
                                                                                                                                                                                                                                                               AlgoSkill (MCTS)
CoT        Haiku                                                           73% (147/200)                        68%  99%                                         0
                                                                                                                                                                        Llama 3.1                      Llama 4                         Qwen 3              Claude
                                                                                                                                                                           8B                           Scout                           32B                Haiku 4
AlgoSkill  Haiku                                                           77% (155/200)                        89% 100%                                                                        40 AtCoder / LeetCode problems released after 2024-08-01


Direct LLM Llama 8B                                                        69% (139/200)  63%  87%
                                                                                                                                                  Figure 6: AlgoSkill (red) versus Direct LLM and CoT
CoT†       Llama 8B                                                        67% (134/200)  57%  71%
AlgoSkill† Llama 8B                                                        70% (140/200) 100% 100%                                                on the post-cutoff benchmark, across four backbone
                                                                                                                                                  models. The dashed line separates pre-cutoff models
                                                                                                                                                  (left; training data cannot include the test problems)
                                                      Contamination Analysis: Large vs. Small Backbone
                                 Correct (%)                                     T-opt (%)                            S-opt (%)                   from post-cutoff models (right; training include the prob-
                                            69                                         63                                         87              lems).
    Direct LLM
                                                 75                              45                                                    95



                                            67                                        57                                     71
             CoT
                                              73                                           68                                           99        beyond one-step skill selection. Although CoT is a
                                             70                                                      100                                100       strong baseline in this setting, AlgoSkill matches
       AlgoSkill
                                                  77 Haiku                                      89                                      100
                                                     Llama 8B                                                                                     or exceeds it across all three post-cutoff backbones
                   0%   20% 40% 60% 80% 100%                       0%      20% 40% 60% 80% 100%            0%   20% 40% 60% 80% 100%
                                Score
AlgoSkill Llama 8B T-opt=100%: n=19 judged (subset of correct solutions)
                                                                                   Score                                Score                     while producing interpretable skill traces.
                                                                                                                                                     The comparison with the pre-cutoff model fur-
Figure 5: Contamination analysis comparing Claude                                                                                                 ther supports the robustness of AlgoSkill. The large
Haiku-4 and Llama 3.1 8B backbones on the rule-based                                                                                              gap between pre-cutoff and post-cutoff backbones
benchmark. AlgoSkill’s T-optimality advantage is pre-
                                                                                                                                                  likely reflects both stronger model capability and
served across backbone sizes (89% on Haiku and 100%†
on Llama 8B).                                                                                                                                     possible training exposure. However, AlgoSkill
                                                                                                                                                  improves over Direct prompting in both regimes,
                                                                                                                                                  which is consistent with the trend observed on the
backbone models spanning two temporal regimes:                                                                                                    contamination-controlled rule-based benchmark in
• Pre-cutoff (≤2023-12): Llama 3.1 8B, whose                                                                                                      Section 6.7.
  reported pretraining data ends in December 2023.
  This model cannot have seen contests released                                                                                                   6.9                 Problem Modification Robustness
  after August 2024, providing a contamination-                                                                                                   We test whether AlgoSkill remains effective when
  free reference point.                                                                                                                           known benchmark problems are transformed into
• Post-cutoff (≥2024-11): Llama 4 Scout 17B                                                                                                       novel variants. Starting from 270 cross-platform
  (≈2024-11), Qwen 3 32B (≈2025-01), and                                                                                                          problems, we construct three transformation types:
  Claude Haiku 4 (≈2025-01). These models may                                                                                                     Constraint Mutation, which changes input bounds
  have been trained on data from the contest pe-                                                                                                  or value ranges; Dimension Extension, which adds
  riod, so their results may reflect both stronger                                                                                                a new parameter such as a k-th objective or opera-
  model capability and possible exposure to the                                                                                                   tion budget; and Objective Shift, which changes the
  test problems.                                                                                                                                  optimization target while preserving the underlying
   Table 7 compares Direct LLM, CoT, AlgoSkill-                                                                                                   structure. Claude Haiku-4 is used as the modifi-
Greedy, and AlgoSkill across the four backbones.                                                                                                  cation oracle to generate the revised statement, a
On the pre-cutoff Llama 3.1 8B model, all methods                                                                                                 reference Python solution, and five new test inputs.
perform poorly, with scores of 22%, 17%, 17%,                                                                                                     Expected outputs are obtained by executing the ref-
and 27%, respectively. This confirms that the se-                                                                                                 erence solution. This yields 270 verified variants,
lected post-2024-08 problems are difficult for a                                                                                                  with 90 variants per transformation type.
model whose training predates their release.                                                                                                         Table 8 shows that AlgoSkill is more robust
   For the post-cutoff models, AlgoSkill consis-                                                                                                  to modified problem settings. Overall, AlgoSkill
tently achieves the strongest performance. It im-                                                                                                 reaches 67.8% pass@1, outperforming Direct LLM
proves over Direct prompting by up to 17 percent-                                                                                                 at 58.9% and CoT at 60.0%. The strongest improve-
age points and also outperforms AlgoSkill-Greedy,                                                                                                 ment appears under Objective Shift, where the re-
showing that iterative skill refinement adds value                                                                                                quired algorithm often changes rather than only the

                                                                                                                                              8
Table 7: Post-cutoff real-world benchmark on 40 AtCoder/LeetCode contest problems released after 2024-08-01.
Pre-cutoff indicates that training ends before the contest release date, while post-cutoff indicates possible exposure
to the contest period. AlgoSkill-G denotes single-step greedy skill selection, and AlgoSkill denotes MCTS with up
to 3 rounds of skill refinement.

                  Backbone              Cutoff    Seen?             Direct          CoT AlgoSkill-G      AlgoSkill
                  Pre-cutoff: training data ends before contest release
                  Llama 3.1 8B         ≈2023-12      ✗      22% (9/40)         17% (7/40)   17% (7/40) 27% (11/40)
                  Post-cutoff: training data may include contest problems
                  Llama 4 Scout ≈2024-11             ✓     50% (20/40) 55% (22/40) 45% (18/40) 67% (27/40)
                  Qwen 3 32B     ≈2025-01            ✓     47% (19/40) 60% (24/40) 52% (21/40) 65% (26/40)
                  Claude Haiku 4 ≈2025-01            ✓     47% (19/40) 52% (21/40) 47% (19/40) 57% (23/40)


Table 8: Problem modification robustness over 270 ver-                    Table 10: Pass@k curves on Hard Bench (Gemini-2.5-
ified variants. Results report pass@1 (%). ∆ denotes                      Flash, n = 20, five runs per problem). Values are
AlgoSkill improvement over Direct LLM.                                    percentages rounded to one decimal place.

 Transformation          N      Direct CoT AlgoSkill            ∆             Method           k=1    k=2    k=3     k=4    k=5
 Constraint Mutation     90      66.7    70.0     76.7      +10.0             Direct           94.0   95.0   95.0    95.0   95.0
 Dimension Extension     90      53.3    53.3     60.0      +6.7              CoT              89.0   90.0   90.0    90.0   90.0
 Objective Shift         90      56.7    56.7     76.7      +20.0             Self-Refine      87.0   90.0   90.0    90.0   90.0
 Overall                 270     58.9    60.0     67.8      +8.9              Reflexion        90.0   90.0   90.0    90.0   90.0
                                                                              MCTS-NoSkills    90.0   90.0   90.0    90.0   90.0
                                                                              AlgoSkill-G      87.0   90.0   90.0    90.0   90.0
Table 9: Average token consumption per problem on                             AlgoSkill-Full   93.0   94.5   95.0    95.0   95.0
the Hard Bench (n = 15), Direct vs. AlgoSkill-G.

     Backbone                Direct AlgoSkill-G          OH               8    Pass@k Curves
     Claude Haiku-4-5          5,130         5,708       1.1×             9    Skill Usage Analysis
     GPT-4o                    2,625         4,433       1.7×
     Claude Sonnet-4-5         4,266         4,908       1.2×             As shown in Figure 8, we further inspect the skill
     GPT-OSS-120B              7,791        11,237       1.4×
                                                                          operators selected during search. AlgoSkill does
                                                                          not use a fixed template across tasks. In dynamic-
surface statement. AlgoSkill also remains better                          programming cases, trajectories often include oabs ,
under Constraint Mutation and Dimension Exten-                            oconstraint , ostate , ocache , and ocomplex , reflecting
sion, suggesting that typed skill scheduling helps                        the need to define states and then reduce the result-
the model adapt when constraints, dimensions, or                          ing complexity. In graph problems, oanalogy , oinv ,
objectives are changed. These results indicate that                       ods , and ocounter appear more often, since these
AlgoSkill’s gains are not simply due to recalling                         tasks usually require mapping to a known graph
original problem templates; the method remains                            primitive, checking invariants, and testing edge
effective when the algorithmic requirements are                           cases. For monotone optimization tasks, omono
modified.                                                                 is frequently selected before obrute , because the
                                                                          brute-force step is used to validate the feasibility
                                                                          predicate. We summarize these trends using skill-
7   Token Efficiency Analysis
                                                                          frequency statistics and the learned Qω (s, o) val-
AlgoSkill introduces additional token cost because                        ues.
each trajectory applies several skills. Table 9 re-
                                                                          10     Hard Benchmark and
ports the audited version 2 average token consump-
tion per problem on the Hard Benchmark.
                                                                                 Cross-Backbone Generalization
   The overhead is modest for the greedy AlgoSkill                        The classical problems in our main benchmark in
controller, ranging from about 1.1× for Claude                            Table 1 are widely studied and may appear in LLM
Haiku-4-5 to 1.7× for GPT-4o. These numbers                               pretraining data. To better separate algorithmic rea-
replace the earlier high-overhead token table and                         soning from memorization, we construct a Hard
the old token-cost figures.                                               Benchmark by selecting difficult problems from

                                                                      9
                                                         Pass@k Curves                                                                         Table 11: Hard Bench (HB-15, pass@5) correctness
                                                     (Gemini-2.5-Flash, HB-20)                                                                 and T-opt on positive-gain backbones. AlgoSkill in this
                       98                                                                                                                      table refers to the greedy variant; the full MCTS variant
                       96                                                                                                                      is reported separately on Haiku in Table 12.
    pass@k (%)




                       94
                                                                                                                                                                                       Haiku                 Sonnet-4-5
                                                                                                                                                Method
                       92                                                                                                                                                      Corr.           T-opt      Corr.          T-opt
                       90                                                                                                                       Direct                       20% (3/15)    100% (3/3)   27% (4/15)    0% (0/4)
                                                                                                                                                CoT                          27% (4/15)    100% (4/4)   40% (6/15)   83% (5/6)
                       88                                                Direct                                 MCTS-NoSkill                    AlgoSkill-G                  27% (4/15)    100% (4/4)   40% (6/15)   83% (5/6)
                                                                         CoT                                    AlgoSkill-G
                       86                                                                                                                       ∆ (AlgoSkill-G vs. Direct)     +7 %            0%         +13 %          +83 %
                                                                         Self-Refine                            AlgoSkill
                       84                                                Reflexion
                                                                                                                                               Table 12: Hard Bench (HB-15, pass@5): iterative base-
                                     1                       2                    3                          4                       5
                                                                                                                                               lines and AlgoSkill MCTS on Haiku-4-5.
                                                                                  k
                                                                                                                                                Method                                     Correct.      T-opt (of correct)
 Figure 7: Pass@k curves (Gemini-2.5-Flash, Hard
                                                                                                                                                Reflexion                                 47% (7/15)          86% (6/7)
 Bench 20-problem subset, five runs per problem). Di-                                                                                           Self-Refine                               27% (4/15)             —
 rect leads at k = 1 with 94.0%, while AlgoSkill-Full                                                                                           AlgoSkill (MCTS)                          47% (7/15)         100% (6/6)
 reaches 95.0% at k = 5.                                                                                                                        ∆ (AlgoSkill-MCTS vs. Direct)              +27 %                     —


                                                               Skill Usage Frequency (Top 10)
                  60
                            53                                                                                                                 11      Additional Audited Experiments
                  50                     49
                                                    46

                  40                                                                                                                           12      Algorithm Complexity Profile
Usage Frequency




                  30
                                                                        24
                  20
                                                                23
                                                                                  18           18
                                                                                                                                               Correctness alone, as reported in Section 10, indi-
                                                                                                           17

                  10
                                                                                                                     12         12             cates whether a generated solution passes the tests,
                  0
                                                                                                                                               but it does not fully characterize the quality of algo-
                        constraint    problem counterexample state     brute   data struct. complexity   analogy    greedy monotonicity
                         reading     abstraction construction design   force     subst.     refinement   mapping   exchange
                                                                                                                                               rithm design. Beyond pass/fail correctness, an algo-
Figure 8: Skill usage frequency across 100 sampled                                                                                             rithm should also be evaluated by its time complex-
AlgoSkill trajectories. Constraint Reading, Problem                                                                                            ity, space complexity, and whether it matches the
Abstraction, and Counterexample Construction are the                                                                                           known optimal complexity for the problem class.
most frequently invoked skills, reflecting their role in                                                                                       We therefore conduct an algorithm-design analy-
early-stage problem understanding and verification.                                                                                            sis: for each generated solution, we first extract
                                                                                                                                               the underlying algorithmic idea, then use an LLM
                                                                                                                                               judge to read the code and summarize its time com-
several independent sources, including Codeforces,                                                                                             plexity, space complexity, and optimality relative
AtCoder, Kattis, and LeetCode Hard. We focus                                                                                                   to the reference solution. This allows us to com-
on problems that require non-standard algorithmic                                                                                              pare methods not only by whether they solve the
variants, such as alternating-cost interval DP, k-                                                                                             problem, but also by whether they produce efficient
day cooldown stock trading, dynamic connectivity                                                                                               and complexity-optimal algorithms.
with edge deletions, slope-trick non-decreasing se-                                                                                               We report this analysis on a contamination-free
quences, and digit DP with 64-bit bounds. These                                                                                                rule-based benchmark with known optimal com-
problems are selected to reduce direct recall from                                                                                             plexities, and separately summarize audited hard-
standard benchmark examples and to test whether                                                                                                benchmark complexity numbers for the overlap-
a method can derive a correct algorithm from con-                                                                                              ping methods.
straints and problem structure.
   Table 11 reports the audited version 2 Hard                                                                                                 12.1      Rule-Based Benchmark
Bench numbers after filtering to positive-gain back-                                                                                           Standard competitive-programming benchmarks
bones. The full MCTS variant is reported sepa-                                                                                                 such as Codeforces (Codeforces, 2026), At-
rately on Haiku in Table 12.                                                                                                                   Coder (AtCoder Inc., 2026), Kattis (Kattis, 2026),
   Table 11 shows that the greedy skill scheduler                                                                                              and LeetCode (LeetCode, 2026) may appear ver-
improves over Direct on Haiku and Sonnet-4-5.                                                                                                  batim in LLM pretraining corpora. Therefore, a
Table 12 shows that the full MCTS variant reaches                                                                                              model that returns an optimal solution may be re-
47% on Haiku, matching Reflexion and improving                                                                                                 calling an editorial rather than reasoning about
over Direct by 27 percentage points.                                                                                                           algorithmic complexity. To obtain contamination-

                                                                                                                                          10
                                                                          Hard Bench (HB-15): Correctness by Method & Backbone
                          60
                                            Haiku
                                            Sonnet
Correctness (%, pass@5)


                          50                GPT-5.5
                                                                                                                                                             Δ+13pp
                                            120b(((*)))
                                                                           40%                                      40%          40%                          40%              40%
                          40                GPT-4o

                                                                    33%                                                    33%          33%                            33%
                                                                                                                                                     Δ+7pp
                          30                          27%                             27%          27%                                               27%                               27%


                                            20%
                          20


                          10


                               0
                                                               Direct                                                      CoT                                    AlgoSkill

Figure 9: Hard Bench (HB-15, pass@5) correctness across backbones. AlgoSkill-MCTS and Reflexion co-top on
Haiku at 47% (7/15), while greedy AlgoSkill and CoT reach 27% (4/15).

Table 13: Version 4 Hard Corpus (192 problems, pass@1) on positive-gain backbones. ∆ denotes AlgoSkill minus
Direct.

              Method                                                                   Haiku                          Sonnet-4-5                  GPT-5.5                    gpt-oss-120b
              Direct                                                          70.3 (135/192)                        75.0 (144/192)            81.8 (157/192)             54.7 (105/192)
              CoT                                                             67.7 (130/192)                        77.1 (148/192)            76.6 (147/192)             52.6 (101/192)
              AlgoSkill                                                       71.4 (137/192)                        77.1 (148/192)            83.3 (160/192)             75.0 (144/192)
              ∆ (AlgoSkill vs. Direct)                                                  +1.1                                +2.1                     +1.5                        +20.3


                                                      Version 4 (192): Correctness                                         Table 14: Version 4 Hard T-opt on positive-gain back-
                                                                                     +1.5                                  bones (Haiku judge, % of all 192 problems that are both
                          80                                       +2.1                                +20.3
                                           +1.1                                                                            correct and time-optimal).
   Correctness (%)




                          60
                                                                                                                            Method                   Sonnet-4-5        GPT-5.5       gpt-oss-120b
                          40                                                                                                Direct                         40.6         72.9             35.4
                                                                                                                            CoT                            41.7         67.2             44.8
                                                                                                                            AlgoSkill                      41.7         76.0             55.2
                          20
                                                                                                        Direct              ∆ AlgoSkill vs. Direct         +1.1         +3.1            +19.8
                                                                                                        AlgoSkill
                           0
                                       u                   t-4.5               5.5                0b
                                   Haik                e                  GPT-               ss-12
                                                  Sonn                                 gpt-o                               Table 15: Positive AlgoSkill gains across in-distribution
                                                                                                                           corpora. ∆AS denotes AlgoSkill minus Direct in per-
Figure 10: Version 4 correctness by backbone after fil-                                                                    centage points.
tering to positive-gain backbones (Direct vs. AlgoSkill,
pass@1, n = 192).                                                                                                           Backbone          Corpus                ∆AS Corr.        ∆AS T-opt
                                                                                                                            Haiku-4-5         CP-275                  +2.5 %          +2.3 %
                                                                                                                            Haiku-4-5         Hard Bench 15           +27.0 %          +20 %
                                                                                                                            GPT-5.5           version 4 (192)         +1.5 %          +3.1 %
free evidence, we construct a synthetic benchmark                                                                           gpt-oss-120b      version 4 (192)         +20.3 %         +19.8 %
of 200 procedurally generated problems that are
absent from public benchmark sources.
   We define ten algorithm families with analyti-                                                                             Correctness is measured by exact-output match-
cally known optimal time and space complexities,                                                                           ing against reference outputs. For each correct
and sweep over problem sizes and constraint param-                                                                         solution, an LLM judge reads the generated code,
eters to produce 20 variants per family, yielding                                                                          infers its time and space complexities, and com-
10×20 = 200 problems. Test cases are generated                                                                             pares them with the known optimal complexities
from reference solutions on seeded random inputs.                                                                          of that family to determine T-opt and S-opt.
The families and their optimal complexities are:                                                                              Table 18 shows a large gap in time-complexity

                                                                                                                      11
                                                                 Version 4 (192): T-opt                                         Table 16: Version 4 Space-Optimality (S-opt) on
                                                                                                                                positive-gain backbones (Haiku judge, % of all 192
                                  80                                                +3.1                                        problems that are both correct and space-optimal).

                                  60                                                                         +19.8               Backbone              Direct S-opt            AS S-opt            ∆AS
 T-opt (%)




                                                        +1.1                                                                     GPT-5.5             69.8 (134/192)         75.5 (145/192)         +5.7
                                  40
                                                                                                                                 gpt-oss-120b         41.7 (80/192)         57.3 (110/192)         +15.6

                                  20
                                                                                                             Direct             Table 17: Algorithm families used in the rule-based
                                                                                                             AlgoSkill          benchmark. Each family has a known target time and
                                   0
                                                                                                                                space complexity.
                                                t-4.5                  GPT-
                                                                              5.5                     120b
                                       Sonn
                                            e                                                    oss-
                                                                                            gpt-
                                                                                                                                Algorithm Family                       Time Complexity   Space Complexity
                                                                                                                                Binary Search on Answer                O(N log S)        O(N )
Figure 11: Version 4 T-opt by backbone after filtering to                                                                       Sliding Window Max (monotonic deque)   O(N )             O(K)
positive-gain backbones (Direct vs. AlgoSkill, pass@1,                                                                          Two Pointers (sorted array)            O(N log N )       O(N )
                                                                                                                                Prefix Sum Range Query                 O(N +Q)           O(N )
n = 192).                                                                                                                       Greedy Interval Scheduling             O(N log N )       O(N )
                                                                                                                                Patience Sort / LIS                    O(N log N )       O(N )
                                                                                                                                BFS Shortest Path                      O(N M )           O(N M )
                                                                                                                                Top-K Frequent (Heap)                  O(N log K)        O(N )
                                                        Positive AlgoSkill Gains Across Corpora                                 Monotonic Stack (NGE)                  O(N )             O(N )
                                                                                                        Correctness gain        Merge Sort Inversions                  O(N log N )       O(N )
AlgoSkill gain over Direct (pp)




                                  30
                                                                +27                                     T-opt gain

                                  25
                                                                        +20                            +20.3 +19.8
                                  20
                                                                                                                                13     Related Work
                                  15

                                  10                                                                                            13.1     LLM-Based Code Generation
                                   5                                                         +3.1
                                          +2.5 +2.3                                  +1.5                                       Large language models (LLMs) have become a ma-
                                   0                                                                                            jor approach for code generation. Codex (Chen
                                         Haiku                 Haiku            GPT-5
                                                                                      .5                  0b
                                                                                                     ss-12 4
                                             5                     5                  n4       gpt-o                            et al., 2021) fine-tuned GPT-3 on GitHub code
                                        CP-27                  HB-1            Versio              Versio
                                                                                                          n

                                                                                                                                and introduced HumanEval to measure functional
Figure 12: Positive AlgoSkill gains (∆AS = AlgoSkill                                                                            correctness. AlphaCode (Li et al., 2022) ex-
− Direct, percentage points) across corpora.                                                                                    tended code generation to competitive program-
                                                                                                                                ming by combining large-scale sampling with test-
                                                                                                                                based filtering. AlphaCode 2 (AlphaCode Team,
quality. AlgoSkill achieves 89% T-optimality                                                                                    2023) further improved competitive programming
among correct solutions, compared with 45% for                                                                                  performance through stronger training data and
Direct LLM, giving a +44 % advantage on prob-                                                                                   sampling strategies. The DeepSeek-Coder se-
lems that are procedurally generated rather than                                                                                ries (Guo et al., 2024) released open-source code
copied from existing programming benchmarks.                                                                                    LLMs trained with fill-in-the-middle objectives
This supports the claim that AlgoSkill improves                                                                                 and showed strong results on standard code bench-
complexity-aware algorithm selection rather than                                                                                marks.
merely exploiting memorized editorials.                                                                                            However, code LLMs still struggle with algo-
                                                                                                                                rithmically difficult problems. Prior studies report
12.2                                     Complexity Analysis on Novel Hard
                                                                                                                                sharp performance drops on tasks requiring dy-
                                         Problems
                                                                                                                                namic programming, graph reasoning, number the-
We evaluate the overlapping methods on the full 15-                                                                             ory, or careful complexity control (Zheng et al.,
problem Novel Hard Benchmark using the audited                                                                                  2024). These limits motivate AlgoSkill: instead
version 2 Hard Bench numbers where available.                                                                                   of relying mainly on more samples, we model the
MapCoder is retained from the prior version be-                                                                                 reasoning structure behind algorithm design.
cause version 2 does not report a corresponding                                                                                    Code generation benchmarks have also moved
MapCoder rerun.                                                                                                                 beyond HumanEval. SWE-Bench (Jimenez et al.,
   Table 19 shows that AlgoSkill-MCTS and Re-                                                                                   2024) evaluates models on real GitHub issues.
flexion solve 7/15 problems on the audited Hard                                                                                 LiveCodeBench (Jain et al., 2024) reduces con-
Bench. AlgoSkill-MCTS attains 100% T-opt over                                                                                   tamination risk by collecting recent programming
the judged correct solutions, while the greedy Al-                                                                              problems. CodeContests (Li et al., 2022) provides
goSkill variant solves 4/15 problems.                                                                                           competitive programming tasks with public and

                                                                                                                           12
Table 18: Rule-based benchmark (200 contamination-                                                            Table 19: Complexity audit on the Novel Hard Bench-
free problems). Correct denotes the fraction of gen-                                                          mark (15 problems). T-opt is conditioned on correctness.
erated solutions. T-opt denotes the fraction of correct                                                       Rows marked prior-only are retained from version 1 be-
solutions whose time complexity matches the known op-                                                         cause version 2 does not report that method.
timal time complexity for the corresponding algorithm
family. S-opt denotes corresponding optimal space com-                                                        Method                     Correct/15    T-opt (corr)   Source
plexity. “Llama 8B” denotes llama-3.1-8b-instant.                                                             Direct LLM                  3/15 (20%)         100%     version 2
                                                                                                              CoT                         4/15 (27%)         100%     version 2
                                                                                                              Self-Refine                 4/15 (27%)            —     version 2
  Method                             Backbone                          Correct T-opt          S-opt           Reflexion                   7/15 (47%)          86%     version 2
                                                                                                              MapCoder                    6/15 (40%)          50%     prior-only
  Direct LLM                         Haiku                    75% (151/200)       45%              95%        AlgoSkill-Greedy (ours)     4/15 (27%)         100%     version 2
  CoT                                Haiku                    73% (147/200)       68%              99%
  Direct LLM                         Llama 8B                 69% (139/200)       63%              87%        AlgoSkill-MCTS (ours)     7/15 (46.7%)         100%     version 2

  AlgoSkill (ours)                   Haiku                    77% (155/200)       89%        100%


                        Rule-Based Benchmark (200 problems, contamination-free)                               ple, rStar-Math (Guan et al., 2025) uses MCTS
                   Correct (%)                                                    * Best overall
                   T-opt (% of correct)                  99                                  100
            100%                95
                   S-opt (% of correct)
                                                                                       89
                                                                                                              guided by process-level signals for mathematical
                                                                             87
            80%    75                                                             77                          reasoning.
                                          73
                                                 68               69
                                                                        63
                                                                                                                 AlgoSkill uses search in a different space. Rather
Score (%)




            60%
                         45                                                                                   than treating tree edges as free-form thoughts or
            40%
                                                                                                              code edits, it treats them as typed skill applica-
            20%
                                                                                                              tions. This reduces the branching space and makes
             0%                                                                                               each step easier to interpret and verify. Process
                    Direct LLM                   CoT               Direct LLM     AlgoSkill (*)
                      (Haiku)                  (Haiku)             (Llama 8B)       (Haiku)
                                                                                                              reward models (PRMs) are also related: they score
Figure 13: Rule-based benchmark results across four
                                                                                                              intermediate reasoning steps rather than only fi-
method/backbone combinations. AlgoSkill achieves the                                                          nal answers (Lightman et al., 2024), and Math-
highest T-optimality (89%) and correctness (77%).                                                             Shepherd (Wang et al., 2024) trains process super-
                                                                                                              vision without manual step annotations. AlgoSkill
                                                                                                              provides a natural setting for such feedback be-
hidden tests.                                                                                                 cause each design state records tests, complexity
                                                                                                              estimates, and proof-related checks.
13.2 Iterative Refinement and Self-Correction
Iterative refinement methods improve an initial
answer through feedback and revision. Self-                                                                   13.4     Reinforcement Learning for Code and
Refine (Madaan et al., 2023) asks an LLM to                                                                            Algorithm Synthesis
critique and revise its own output over multiple
rounds. Reflexion (Shinn et al., 2023) stores                                                                 Reinforcement learning has been used for code
natural-language reflections from failed attempts                                                             generation through human feedback and execution
and uses them in later trials. These methods are                                                              feedback. CodeRL (Le et al., 2022) uses unit-test
simple and broadly useful, but their repair steps are                                                         outcomes as rewards for code generation. Other
still mostly free-form. The model decides what to                                                             work applies policy optimization to improve mod-
change without an explicit algorithmic structure.                                                             els using execution-based signals (Shojaee et al.,
AlgoSkill differs by organizing repair around typed                                                           2023). A common challenge is reward sparsity: a
algorithmic skills, such as counterexample analysis,                                                          program is often judged only after full generation.
invariant revision, and complexity refinement.                                                                  AlgoSkill addresses this issue by assigning feed-
                                                                                                              back to skill-level decisions. Its reward separates
13.3               Tree Search for LLM Reasoning                                                              correctness, efficiency, explanation quality, and re-
Tree of Thoughts (Yao et al., 2023) extends chain-                                                            pair progress, allowing more informative credit
of-thought prompting by maintaining and search-                                                               assignment across a design trajectory. Recent work
ing over multiple reasoning paths. Monte Carlo                                                                on reinforcement learning with verifiable rewards
Tree Search (MCTS) has a long history in decision-                                                            (RLVR) further shows the value of training with
making systems, including AlphaGo and Alp-                                                                    objective feedback in reasoning tasks (Guo et al.,
haZero (Silver et al., 2016, 2017). Recent work                                                               2025). AlgoSkill applies this idea to typed skill
also applies MCTS to LLM reasoning; for exam-                                                                 scheduling for algorithm design.

                                                                                                         13
13.5    Algorithm Design Automation and                     algorithmic derivation. These results suggest that
        Evolution                                           structured skill composition is an effective way to
Search-based algorithm discovery has produced               improve LLM-based algorithm design.
strong results on selected problems.         Fun-
                                                            15   Limitations
Search (Romera-Paredes et al., 2024) combines
LLM-generated program mutations with evolution-             AlgoSkill still has several limitations. First, its
ary selection and discovers improved solutions for          performance depends on the coverage and quality
tasks such as cap set and bin packing. AlphaE-              of the predefined skill library; problems requir-
volve (Novikov et al., 2025) follows a related di-          ing skills outside the library may not be handled
rection for broader algorithm design tasks.                 well. Second, the MCTS-based search process in-
   These methods search over raw programs or pro-           troduces extra token and computation cost com-
gram mutations. AlgoSkill instead searches over             pared with direct generation. Third, the verifier
structured sequences of algorithmic skills. This            may miss corner cases when tests or symbolic
gives the search process a stronger algorithmic             complexity checks are incomplete. Finally, our ex-
prior, makes intermediate decisions more readable,          periments are limited to competitive programming
and supports transfer across problem types.                 and selected combinatorial optimization tasks, so
                                                            broader evaluation on real-world software engineer-
13.6    Skill Libraries and Structured Problem              ing and scientific computing problems is needed.
        Solving
Reusable skill libraries have been widely studied
in robotics, hierarchical reinforcement learning,           References
and LLM agents. The options framework (Sut-                 AlphaCode Team. 2023. AlphaCode 2 technical report.
ton et al., 1999) formalizes temporally extended              Technical report, Google DeepMind.
actions through initiation and termination condi-
tions, which is closely related to typed skill oper-        Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo
                                                              M K Martin, Mukund Raghothaman, Sanjit A Se-
ators. Voyager (Wang et al., 2023) builds a skill             shia, Rishabh Singh, Armando Solar-Lezama, Emina
library for a Minecraft agent and reuses generated            Torlak, and Abhishek Udupa. 2013. Syntax-guided
programs to solve later tasks.                                synthesis. In Formal Methods in Computer-Aided
   Program-aided reasoning is also related. Pro-              Design (FMCAD).
gram of Thoughts (Gao et al., 2023) uses Python             Anthropic. 2024.  Claude 3 haiku: Our fastest
as an intermediate representation for mathe-                  model yet. https://www.anthropic.com/news/
matical computation, while Toolformer (Schick                 claude-3-haiku. Accessed: 2026-05-10.
et al., 2023) trains LLMs to call external tools.
                                                            Anthropic. 2026.     Claude models overview.
Scratchpad-style reasoning (Nye et al., 2021)
                                                              https://docs.anthropic.com/en/docs/
shows that explicit intermediate states can improve           about-claude/models/overview.     Accessed:
multi-step reasoning. AlgoSkill combines these                2026-06-27.
ideas by maintaining a structured design state that
is updated through typed algorithmic skills.                AtCoder Inc. 2026. Atcoder. https://atcoder.jp/.
                                                              Accessed: 2026-05-10.
14     Conclusion                                           Peter Auer, Nicolò Cesa-Bianchi, and Paul Fischer.
                                                              2002. Finite-time analysis of the multiarmed ban-
We introduced AlgoSkill, a framework that treats              dit problem. Machine Learning, 47(2):235–256.
automatic algorithm design as skill-guided sequen-
tial decision-making rather than direct code gener-         Jacob Austin, Augustus Odena, Maxwell Nye, Maarten
ation. AlgoSkill uses a library of typed algorithmic           Bosma, Henryk Michalewski, David Dohan, Ellen
                                                               Jiang, Carrie Cai, Michael Terry, Quoc Le, and 1
skills and combines learned scheduling, MCTS                   others. 2021. Program synthesis with large language
search, and verification feedback to construct cor-            models. arXiv preprint arXiv:2108.07732.
rect and efficient solutions. Experiments on com-
petitive programming and hard benchmarks show               Edmund K Burke, Michel Gendreau, Matthew Hyde,
                                                              Graham Kendall, Gabriela Ochoa, Ender Özcan, and
that AlgoSkill improves over direct LLM genera-               Rong Qu. 2013. Hyper-heuristics: A survey of the
tion, iterative refinement, and search-based base-            state of the art. Journal of the Operational Research
lines, especially on problems that require genuine            Society, 64(12):1695–1724.


                                                       14
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,              Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia
 Henrique Ponde de Oliveira Pinto, Jared Kaplan, Har-            Yan, Tianjun Zhang, Sida Wang, Armando Solar-
 rison Edwards, Yuri Burda, Nicholas Joseph, Greg                Lezama, Koushik Sen, and Ion Stoica. 2024. Live-
 Brockman, and 1 others. 2021. Evaluating large                  CodeBench: Holistic and contamination free eval-
 language models trained on code. arXiv preprint                 uation of large language models for code. arXiv
 arXiv:2107.03374.                                               preprint arXiv:2403.07974.

Mayee F. Chen, Nicholas Roberts, Kush Bhatia, Jue              Carlos E Jimenez, John Yang, Alexander Wettig,
 Wang, Ce Zhang, Frederic Sala, and Christopher Ré.              Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
 2023. Skill-it! a data-driven skills framework for un-          Narasimhan. 2024. SWE-bench: Can language mod-
 derstanding and training language models. Preprint,             els resolve real-world GitHub issues? In Inter-
 arXiv:2307.14430.                                               national Conference on Learning Representations
                                                                 (ICLR).
Codeforces. 2026. Codeforces. https://codeforces.
  com/. Accessed: 2026-05-10.                                  Kattis. 2026. Kattis problem archive. https://open.
                                                                 kattis.com/. Accessed: 2026-05-10.
Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon,                  Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio
  Pengfei Liu, Yiming Yang, Jamie Callan, and Gra-               Savarese, and Steven CH Hoi. 2022. CodeRL: Mas-
  ham Neubig. 2023. PAL: Program-aided language                  tering code generation through pretrained models and
  models. In International Conference on Machine                 deep reinforcement learning. In Advances in Neural
  Learning (ICML).                                               Information Processing Systems (NeurIPS).
Google. 2025. Gemini 2.5 flash. https://ai.google.             LeetCode. 2026. Leetcode. https://leetcode.com/.
  dev/gemini-api/docs/models. Accessed: 2026-                    Accessed: 2026-05-10.
  05-10.
                                                               Yujia Li, David Choi, Junyoung Chung, Nate Kushman,
Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang,                Julian Schrittwieser, Rémi Leblond, Tom Eccles,
  Youran Sun, Yi Zhu, Fan Yang, and Mao Yang. 2025.              James Keeling, Felix Gimeno, Agustin Dal Lago, and
  rStar-Math: Small LLMs can master math reason-                 1 others. 2022. Competition-level code generation
  ing with self-evolved deep thinking. arXiv preprint            with AlphaCode. Science, 378(6624):1092–1097.
  arXiv:2501.04519.
                                                               Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
Sumit Gulwani. 2011. Automating string processing in             son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  spreadsheets using input-output examples. In ACM               John Schulman, Ilya Sutskever, and Karl Cobbe.
  SIGPLAN Notices (POPL).                                        2024. Let’s verify step by step. In International
                                                                 Conference on Learning Representations (ICLR).
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao
  Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shi-                Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
  rong Ma, Peiyi Wang, Xiao Bi, and 1 others. 2025.             Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
  DeepSeek-R1: Incentivizing reasoning capability in            Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
  LLMs via reinforcement learning. arXiv preprint               Shashank Gupta, Bodhisattwa Prasad Majumder,
  arXiv:2501.12948.                                             Karl Moritz Hermann, Sean Welleck, Amir Yazdan-
                                                                bakhsh, and Peter Clark. 2023. Self-refine: Iterative
                                                                refinement with self-feedback. In Advances in Neu-
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai               ral Information Processing Systems.
  Dong, Wentao Zhang, Guanting Chen, Xiao Bi,
  Yu Wu, Yuxuan Li, and 1 others. 2024. DeepSeek-              Meta AI. 2024. Introducing Llama 3.1. https://
  Coder: When the large language model meets pro-               ai.meta.com/blog/meta-llama-3-1/. Accessed:
  gramming — the rise of code intelligence. arXiv               2026-06-27.
  preprint arXiv:2401.14196.
                                                               Meta AI. 2025. The Llama 4 herd. https://ai.meta.
Dan Hendrycks, Steven Basart, Saurav Kadavath, Man-             com/blog/llama-4-multimodal-intelligence/.
  tas Mazeika, Akul Arora, Ethan Guo, Collin Burns,             Accessed: 2026-06-27.
  Samir Puranik, Horace He, Dawn Song, and 1 others.
  2021. Measuring coding challenge competence with             Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Em-
  APPS. In Advances in Neural Information Process-               ilien Dupont, Po-Sen Huang, Adam Zsolt Wagner,
  ing Systems (NeurIPS).                                         Sergey Shirobokov, Borislav Kozlovskii, Francisco
                                                                 J. R. Ruiz, Abbas Mehrabian, M. Pawan Kumar, Abi-
Md. Ashraful Islam, Mohammed Eunus Ali, and                      gail See, Swarat Chaudhuri, George Holland, Alex
 Md Rizwan Parvez. 2024. Mapcoder: Multi-agent                   Davies, Sebastian Nowozin, Pushmeet Kohli, and
 code generation for competitive problem solving. In             Matej Balog. 2025. AlphaEvolve: A coding agent for
 Proceedings of the 62nd Annual Meeting of the Asso-             scientific and algorithmic discovery. arXiv preprint
 ciation for Computational Linguistics.                          arXiv:2506.13131.


                                                          15
Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari,              Richard S Sutton, Doina Precup, and Satinder Singh.
 Henryk Michalewski, Jacob Austin, David Bieber,                  1999. Between MDPs and semi-MDPs: A framework
 David Dohan, Aitor Lewkowycz, Maarten Bosma,                     for temporal abstraction in reinforcement learning.
 David Luan, and 1 others. 2021. Show your work:                  Artificial Intelligence, 112(1-2):181–211.
 Scratchpads for intermediate computation with lan-
 guage models. arXiv preprint arXiv:2112.00114.                 Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Man-
                                                                  dlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and
OpenAI. 2024. Hello GPT-4o. https://openai.com/                   Anima Anandkumar. 2023. Voyager: An open-ended
  index/hello-gpt-4o/. Accessed: 2026-06-27.                      embodied agent with large language models. arXiv
                                                                  preprint arXiv:2305.16291.
OpenAI. 2025. Introducing gpt-oss. https://openai.
  com/index/introducing-gpt-oss/. Accessed:                     Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
  2026-06-27.                                                     Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
                                                                  2024. Math-Shepherd: Verify and reinforce LLMs
OpenAI. 2026.     OpenAI models documentation.                    step-by-step without human annotations. In Associa-
  https://platform.openai.com/docs/models.                        tion for Computational Linguistics (ACL).
  Accessed: 2026-06-27.                                         Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
                                                                   Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and
Qwen Team. 2025. Qwen3: Think deeper, act faster.                  Denny Zhou. 2022. Chain-of-thought prompting elic-
 https://qwenlm.github.io/blog/qwen3/. Ac-                         its reasoning in large language models. In Advances
 cessed: 2026-06-27.                                               in Neural Information Processing Systems (NeurIPS).
John R Rice. 1976. The algorithm selection problem.             Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
  Advances in Computers, 15:65–118.                               Thomas L Griffiths, Yuan Cao, and Karthik
                                                                  Narasimhan. 2023. Tree of thoughts: Deliberate
Bernardino    Romera-Paredes,      Mohammadamin                   problem solving with large language models. In Ad-
  Barekatain, Alexander Novikov, Matej Balog,                     vances in Neural Information Processing Systems
  M. Pawan Kumar, Emilien Dupont, Francisco J. R.                 (NeurIPS).
  Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar
  Fawzi, Pushmeet Kohli, and Alhussein Fawzi. 2024.             Zibin Zheng, Kaiwen Ning, Yanlin Wang, Jingwen
  Mathematical discoveries from program search with               Zhang, Dewu Zheng, Mingxi Ye, and Jiachi Chen.
  large language models. Nature, 625:468–475.                     2024. A survey of large language models for
                                                                  code: Evolution, benchmarking, and future trends.
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta              Preprint, arXiv:2311.10372.
  Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola
  Cancedda, and Thomas Scialom. 2023. Toolformer:
  Language models can teach themselves to use tools.
  In Advances in Neural Information Processing Sys-
  tems (NeurIPS).

Noah Shinn, Federico Cassano, Edward Berman, Ash-
  win Gopinath, Karthik Narasimhan, and Shunyu Yao.
  2023. Reflexion: Language agents with verbal rein-
  forcement learning. In Advances in Neural Informa-
  tion Processing Systems.

Parshin Shojaee, Aneesh Jain, Sindhu Tipirneni, and
  Chandan K Reddy. 2023. Execution-based code gen-
  eration using deep reinforcement learning. arXiv
  preprint arXiv:2301.13816.

David Silver, Aja Huang, Chris J Maddison, Arthur
  Guez, Laurent Sifre, George Van Den Driessche, Ju-
  lian Schrittwieser, Ioannis Antonoglou, Veda Pan-
  neershelvam, Marc Lanctot, and 1 others. 2016. Mas-
  tering the game of Go with deep neural networks and
  tree search. Nature, 529(7587):484–489.

David Silver, Julian Schrittwieser, Karen Simonyan,
  Ioannis Antonoglou, Aja Huang, Arthur Guez,
  Thomas Hubert, Lucas Baker, Matthew Lai, Adrian
  Bolton, and 1 others. 2017. Mastering chess and
  shogi by self-play with a general reinforcement learn-
  ing algorithm. arXiv preprint arXiv:1712.01815.


                                                           16
A     Full Algorithmic Skill Library                                • State Design (ostate ) defines states for dynamic
                                                                      programming or graph search by deciding what
This appendix gives the full specification of the                     information is sufficient for future decisions, writ-
twenty algorithmic skills used by AlgoSkill. Each                     ten as P (future | history) = P (future | st ).
skill is represented as a typed transformation oper-
ator:                                                               • Decomposition (odecomp ) splits a separable prob-
                                                                      lem into subproblems, q → {q1 , . . . , qm },
         oi = (ϕpre       post
                i , τi , ϕi    , ci , vi , ri ),        (34)          and combines their solutions through A(q) =
                                                                      Combine(A(q1 ), . . . , A(qm )).
where ϕpre
         i   is the precondition predicate, τi is the
                                                                    • Relaxation (orelax ) solves a simpler version of
state transformation, ϕpost
                         i    is the expected postcon-
                                                                      the problem by removing or softening constraints,
dition, ci is the expected complexity effect, vi is
                                                                      then maps the solution back through Relax →
the verification rule, and ri describes known failure
                                                                      SolveRelaxed → Round → Repair.
modes.
   The complete skill library is:                                   • Exchange Argument (oexchange ) checks a
                                                                      greedy rule by trying to build an exchange proof.
O = {oabs , oconstraint , obrute , omono , oinv , ostate ,            Given an optimal solution O and a greedy choice
       odecomp , orelax , oexchange , ods , odual , ocounter ,        g, the goal is to construct O′ containing g with
       ocomplex , oanalogy , omath , osym , orandom ,                 cost(O′ ) ≤ cost(O).
       oapprox , ocache , oparallel }.                  (35)        • Data-Structure Substitution (ods ) replaces re-
                                                                      peated scans or quadratic loops with suitable data
A.1    Core Skills                                                    structures, changing Q · O(n) into Tbuild + Q ·
• Problem Abstraction (oabs ) maps the raw state-                     Tquery .
  ment to a structured representation, including the                • Duality (odual ) maps the problem to an equiva-
  problem type, task type, and main objects. This                     lent dual form. Examples include minimum ver-
  step controls which later algorithmic choices are                   tex cover to maximum matching through König’s
  considered.                                                         theorem, and max-flow to min-cut.
• Constraint Reading (oconstraint ) reads the input                 • Counterexample (ocounter ) creates adversarial
  limits and infers a feasible complexity range. We                   tests, such as empty cases, singleton inputs, all-
  use simple rules such as n ≤ 20 ⇒ O(2n ), n ≤                       equal arrays, sorted arrays, extreme values, dis-
  103 ⇒ O(n2 ), n ≤ 105 ⇒ O(n log n), and                             connected graphs, and cycles. These tests expose
  n ≤ 109 ⇒ O(log n). The skill restricts the                         incorrect states, invariants, or greedy choices.
  search to algorithms satisfying Avalid = {a :
  T (a, n) ≤ Tmax (n)}.                                             • Complexity Refinement (ocomplex ) improves a
                                                                      correct but slow algorithm by locating the bot-
• Brute-Force First (obrute ) builds a correct but                    tleneck and replacing it with a faster operation.
  slow baseline by exhaustive enumeration. This                       Common paths include O(n3 ) → O(n2 ) →
  baseline is useful for small-case testing and for                   O(n log n) → O(n).
  finding the bottleneck that must be removed.                      • Analogy (oanalogy ) maps a problem to a known
                                                                      template, such as shortest path, knapsack, inter-
• Monotonicity Detection (omono ) checks whether
                                                                      val covering, topological dynamic programming,
  a decision predicate supports binary search. If
                                                                      or min-cut, and adapts the template to the current
  F (x1 ) = 1 and x1 ≤ x2 imply F (x2 ) = 1,
                                                                      statement.
  the search range can be reduced from O(U ) to
  O(log U ).                                                        A.2   Additional Skills
                                                                    • Mathematical Formula (omath ) derives a closed
• Invariant Design (oinv ) constructs an invariant
                                                                      form for counting, combinatorics, or number-
  I(st ) such that I(st ) = 1 and st+1 = T (st , ot )
                                                                      theory tasks, often giving O(1) or O(log n) time.
  imply I(st+1 ) = 1. This skill supports cor-
  rectness arguments for iterative and greedy al-                   • Symmetry (osym ) merges equivalent states to
  gorithms.                                                           reduce the state space.

                                                               17
• Randomization (orandom ) introduces random-
  ized algorithms when exact deterministic meth-
  ods are too costly.

• Approximation (oapprox ) relaxes exact optimal-
  ity and returns an efficient approximate solution
  with a stated quality target.

• Caching (ocache ) adds memoization to recursive
  computation, turning repeated subproblems into
  a finite state table.

• Parallelization (oparallel ) identifies independent
  sub-computations and schedules them concur-
  rently.

   Table 20 summarizes the preconditions, state
effects, complexity changes, and failure modes of
all skills.

B   Implementation Details
Unless otherwise stated, all LLM components use
GPT-4o-mini (OpenAI, 2026) as the backbone.
Each method is evaluated with five sampling runs
per problem. During inference, AlgoSkill uses an
MCTS budget of B = 32 rollouts per problem and
exploration coefficient β = 1.0. The correctness
reward weights are set to w1 = 0.1, w2 = 0.4,
w3 = 0.3, and w4 = 0.2 for compilation, unit tests,
stress tests, and oracle agreement, respectively. The
efficiency weights are set to λT = λM = 0.5 and
λR = 0.3.




                                                        18
Table 20: Complete algorithmic skill library. Each skill oi is specified by its precondition ϕpre
                                                                                              i , effect on the design
state, expected complexity change, and common failure mode.

Skill                             Precondition                  Effect on State                Complexity Change        Key Failure Mode

Problem Abstraction (oabs )       Raw problem not typed         Sets problem and task type     O(|q|)                   Wrong task type
Constraint               Reading Explicit constraints           Sets feasible complexity budget O(1)                    Wrong complexity bound
(oconstraint )
Brute Force (obrute )             Small input is feasible       Builds correct slow baseline   Tbrute                   TLE on large input
Monotonicity           Detection Ordered decision target        Adds binary-search reduction   O(U ) → O(log U )        Non-monotone predicate
(omono )
Invariant Design (oinv )          Iterative or greedy process   Adds correctness invariant     O(T )                    Invalid invariant
State Design (ostate )            Overlapping subproblems       Defines state and transition   TDP                      Missing state variable
                                                                                               P
Decomposition (odecomp )          Separable structure           Splits into subproblems          i T (qi ) + Tcombine   False independence
Relaxation (orelax )              Hard constraints              Solves softened problem        Trelax + Tround          Large gap after rounding
Exchange               Argument Candidate greedy rule           Checks greedy choice           O(T )                    Failed exchange proof
(oexchange )
Data-Structure Sub. (ods )        Repeated query pattern        Replaces scan with data structure Q · O(log n)          Wrong operation mapping
Duality (odual )                  Known primal-dual form        Maps to dual problem           Tdual                    Invalid dual mapping
Counterexample (ocounter )        Candidate algorithm exists    Generates adversarial tests    Ttest                    Incomplete coverage
Complexity          Refinement Correct but slow algorithm       Replaces bottleneck            Tnew < Told              Wrong bottleneck
(ocomplex )
Analogy (oanalogy )               Template match exists         Maps to known paradigm         Ttemplate                Surface match only
Math Formula (omath )             Large n or pattern            Derives closed form            O(1) or O(log n)         Wrong formula
Symmetry (osym )                  Symmetric states exist        Merges equivalent states       Treduced                 Invalid equivalence
Randomization (orandom )          Exact method too costly       Adds randomized method         Trand                    Unstable result
Approximation (oapprox )          Exact optimization too hard   Relaxes optimality target      Tapprox                  Weak approximation
Caching (ocache )                 Repeated subproblems          Adds memoization               Exp → |S|                Missing cache key
Parallelization (oparallel )      Independent subproblems       Schedules parallel computation Tparallel                Hidden dependency




                                                                               19
