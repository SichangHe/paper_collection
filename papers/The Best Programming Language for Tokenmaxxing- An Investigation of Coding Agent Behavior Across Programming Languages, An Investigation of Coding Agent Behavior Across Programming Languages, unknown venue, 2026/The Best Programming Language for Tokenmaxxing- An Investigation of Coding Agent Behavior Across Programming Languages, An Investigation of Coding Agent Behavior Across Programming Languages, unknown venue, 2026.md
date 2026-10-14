                                                          The Best Programming Language for Tokenmaxxing
                                                 An Investigation of Coding Agent Behavior Across Programming Languages


                                                  Zixuan Wu                          Carolyn Jane Anderson                 Arjun Guha
                                             Northeastern University                    Wellesley College             Northeastern University




                                                               Abstract                           that are widely used by programmers. Although
                                             Although coding agents are now very effective        many programmers use agents by choice, others
                                             in a variety of programming languages, this pa-      feel compelled to do so to meet corporate targets
                                             per first shows that the cost (in tokens) can very   for AI adoption. There are even reports of orga-
                                             significantly by programming language. We            nizations running internal leaderboards for token
                                             evaluate five recent models on programming           consumption. Following Goodhart’s Law (Strath-
                                             problems in Python, Java, Rust, and OCaml.           ern, 1997), some have resorted to tokenmaxxing,
                                             We carefully control for problem difficulty, and     or giving agents tasks for the purpose of increas-
arXiv:2607.22807v1 [cs.SE] 24 Jul 2026




                                             show that there can be stark variation in token
                                             consumption that is consistent across models.
                                                                                                  ing LLM spending, without regard to whether it is
                                             To understand why, we analyze both the struc-        worth the cost. We, the authors of this paper, think
                                             ture and content of agent trajectories. First,       this is definitely pointless and possibly unethical.
                                             we re-execute every intermediate solution and        But, for those who must tokenmax, we present a
                                             abstract each trajectory as a sequence of test-      principled way to do so: work in the programming
                                             outcome vectors, then label the work between         language that makes the agent consume the most
                                             successive solutions. This reveals agents repeat-    tokens. Naively, one might think that this is the
                                             edly producing noncompiling solutions in un-
                                                                                                  language in which programs are the longest, but
                                             familiar languages and revising solutions that
                                             already pass. Second, we analyze trajectory          this isn’t the case with agents that reason and self-
                                             text, finding that agents plan solutions in code     correct. What matters is not the number of tokens
                                             comments, distrust the provided tests in favor       in the final solution, but the amount of reasoning
                                             of inputs they invent, and sidestep unfamiliar       and revision needed to get to the solution.
                                             target languages by prototyping in Python.
                                             Our results show that by-language token effi-           More seriously, the goal of this paper is to study
                                             ciency is a metric that should be considered         how the behavior of software-engineering agents
                                             when benchmarking and developing multilin-           varies by programming language. We evaluate four
                                             gual agents, and, for the tokenmaxxer, a guide       programming languages (Java, OCaml, Python,
                                             to the most expensive language to work in.           and Rust) and five models on a 100-problem subset
                                              Let’s say you have a software engi-                 of LiveCodeBench, gathering 2,000 agent trajecto-
                                              neer or AI researcher and you pay them              ries for analysis.
                                              $500,000 a year. We do that all the time.              Our basic finding is that the choice of program-
                                              That $500,000 engineer, at the end of the           ming language has a significant effect on output
                                              year, I’m going to ask them, how much               tokens produced by the agent, even after carefully
                                              did you spend in tokens? If that person             controlling for problem difficulty. The effect is
                                              said, $5,000, I will go ape... something            most pronounced for OCaml across all models, but
                                              else. If that $500,000 engineer did not             is significant for Rust and Java too. Models are
                                              consume at least $250,000 worth of to-              most efficient when they work in Python.
                                              kens, I’m going to be deeply alarmed. —                However, we go beyond counting tokens and an-
                                              Jensen Huang (All-In Podcast)                       alyze agent trajectories in several ways. First, we
                                                                                                  evaluate every intermediate solution that the agents
                                         1   Introduction
                                                                                                  produce, which allows us to study an agent’s pro-
                                         Over the past 1½ years, coding agents have gone          gression on the unit tests for a problem. This al-
                                         from research idea (Yang et al., 2024) to tools          lows us to observe and quantify several behaviors:
agents repeatedly struggling with the same compile        a new benchmark, but use LiveCodeBench in a
error; agents that get stuck revising a solution even     multi-language context to study agent trajectories.
when all tests pass; and so forth. Second, we label
the actions in every trajectory with an LLM using a       2.2    Agentic Coding and Process Cost
12-category taxonomy that we develop. This allows         Beyond correctness, prior work measures several
us to ask what an agent is doing as it works through      notions of code-generation cost. One line studies
a problem. These labels allow us to determine the         the efficiency of the generated program itself—its
turns spent on bug fixes, optimizations, exploration,     runtime and memory across languages (Fan et al.,
refactors, and more. Finally, we analyze the text the     2025; Qing et al., 2025). Another studies the to-
agents produce as they work, which reveals specific       ken cost of the program’s surface representation,
behaviors: agents sometimes plan in comments be-          where formatting and verbose recurring patterns
fore writing code; they sometimes second-guess            add tokens without functional benefit (Pan et al.,
and re-derive already-passing solutions; they can         2026; Sun et al., 2025). In an agentic setting, how-
distrust the provided tests in favor of inputs they in-   ever, multi-turn reasoning and tool use can cost
vent; and they can sidestep an unfamiliar language        far more than the final program. Existing work
by prototyping in Python first.                           on this process cost focuses almost entirely on
                                                          Python (Bai et al., 2026). We instead make the
Contributions We make the following contri-
                                                          target language the independent variable: process
butions. (1) We study how token cost in agentic
                                                          cost is not surface cost, and the language in which
coding varies across programming languages, con-
                                                          an agent spends the most tokens need not be the
trolling for problem difficulty. (2) We find that,
                                                          one whose programs are longest.
at comparable success rates, lower-resource lan-
                                                             Prior work documents particular sources of agent
guages cost significantly more than Python. (3) We
                                                          inefficiency, including continuing to generate after
introduce a novel analysis approach that involves
                                                          finding a passing solution (Solovyeva and Castor,
testing every intermediate solution that an agent
                                                          2026) and looping when stuck (Fan et al., 2025).
writes in an external test harness, which allows us
                                                          Related methods stop trajectories early or prune
to analyze agents’ test progression. (4) We classify
                                                          redundant work (Guo et al., 2026; Gao and Peng,
the steps between intermediate solutions as seman-
                                                          2026; Xiao et al., 2026; Yang et al., 2025a). On
tic actions, revealing specific agent behaviors and
                                                          less familiar languages, agents may instead proto-
where they fall on the path to a solution.
                                                          type and debug in Python before translating to the
   These findings show how the choice of program-         target language (Sharma et al., 2026). Recent anal-
ming language shapes an agent’s token cost and            yses open up the trajectory by decomposing token
which behaviors drive the difference between lan-         cost by development phase (Salim et al., 2026) or
guages, offering insight toward building more ef-         agent action (Bouzenia and Pradel, 2025; Liu et al.,
ficient agents across programming languages. We           2026). Our analysis likewise resolves a trajectory
plan to release all code and data publicly upon pub-      into phases, but grounds those phases in changes
lication.                                                 in externally verified test outcomes between suc-
                                                          cessive program snapshots. This lets us localize
2     Background and Related Work                         behaviors—including stalling, reworking a pass-
2.1    Multilingual Code Evaluation                       ing solution, and sidestepping through Python—to
                                                          particular stages of solution progress.
Many benchmarks evaluate how the choice of
programming language affects models’ code gen-            3     Methods
eration performance. The earliest benchmarks
translated single-function code completion tasks          We first present how we setup the multi-language
into other languages (Cassano et al., 2023; Athi-         environment, the models we use, how we prompt
waratkun et al., 2022). Multi-SWE-bench and               agents, and how we run our experiments.
SWE-bench Multilingual (Zan et al., 2026; Yang
et al., 2025b) evaluate agents on their ability to        3.1 Choice of Agents, Models, and Languages
solve real-world issues in large code repositories.       We use mini-swe-agent (Yang et al., 2024), a cus-
The tasks that we study lie between code comple-          tomizable agent that supports any model and has a
tion and repository-level tasks. We do not introduce      stable interface. It is also an established baseline
Table 1: We run agents in a container based on Ubuntu 24.04. The container has the language versions shown below,
along with optional packages that may help agents solve programming tasks. We build and run agents’ solutions
with the compile and run commands shown below, and we provide these commands to the agent in the prompt as
part of the task.

 Language            Version     Extra Packages                  Compile command                    Run command
 Python              3.12.3      numpy, pandas, scipy, sympy     —                                  python3 solution.py
 OCaml               5.4.1       core, base, zarith              dune build ./solution.exe          dune exec ./solution.exe
 Java (OpenJDK)      21.0.11     —                               javac Solution.java                java Solution
 Rust                1.96        —                               cargo build -–release              ./target/release/solution



agent that is widely used (Merrill et al., 2026; Zhou            impose a 256MB memory limit on each container,
et al., 2026; Li et al., 2026; Zhang et al., 2026).              and as described below, take steps to prevent code
   We work with five models: Q WEN 3.6-35B-                      execution from causing timeouts. §A describes the
A3B, G EMMA -4-26B-A4B, GLM-5.2, GPT-5.5,                        host machine configuration.
and C LAUDE -S ONNET-4.6 (Qwen Team, 2026;
Google, 2026; GLM-5-Team et al., 2026; An-                       3.3    The MiniLCB Benchmark
thropic, 2026; OpenAI, 2026). We run the open-                   LiveCodeBench (Jain et al., 2025) consists of prob-
weight Qwen and Gemma models locally and ac-                     lems from programming contest websites and is
cess the open-weight GLM model via the Hug-                      typically used to evaluate models in a single at-
ging Face Inference API; all three are amenable to               tempt. Version 6 contains 880 problems, of which
reproducibility. We also evaluate the proprietary                381 have Python starter code; the remaining 499
GPT-5.5 and Sonnet models that power Codex and                   are effectively language-neutral and test solutions
Claude Code, respectively. We enable reasoning                   over standard I/O. Agnostics (Boruch-Gruszecki
for all models. Additional implementation details                et al., 2026) and MultiLCB (Ivanova et al., 2026)
and hyperparameters are provided in §A.                          use this observation to evaluate models across lan-
   We test agents in Python, Java, Rust, and OCaml.              guages with per-language compile-and-run config-
Python is the language used most widely to bench-                urations. We rely on the same observation to con-
mark models’ programming abilities. Although                     struct an agent benchmark.
Java is not popular in ML research, it remains                      With five models, four programming languages,
widely used. Rust and OCaml help illuminate                      and these 499 language-agnostic tasks, we have
agent behavior on languages that are not as well-                the opportunity to run 9,980 agent sessions. To
represented in pretraining data.1                                conserve tokens and budget, we instead randomly
                                                                 sample 100 tasks (yielding 2,000 sessions), and
3.2    Environment Configuration                                 we refer to this subset as MiniLCB. Test cases per
We run agents in a containerized environment that                problem range from 2 to 45, with a median of 22.
includes the standard toolchain for each program-                   In standard LiveCodeBench evaluation, test
ming language, and common packages (Table 1).                    cases run in an external harness to validate a
Table 1 also shows how we compile and run solu-                  model’s single solution offline. In MiniLCB, we
tions to verify agents’ results. For OCaml and Rust,             make all tests and the test harness visible to the
the environment includes a working configuration                 agent. Specifically, we present each problem as a
for Dune and Cargo, so that the agent does not need              small repository: a tests/ directory holding all in-
to spend turns configuring the compiler. The agent               put/output pairs and a test.sh script that runs the
is thus free to edit the Dune/Cargo configuration,               agent’s solution and reports successes and failures
or write a solution that spans several files.                    on individual tests.2 The prompt explicitly states3 :
   At runtime, we limit the agent to 40 turns and                    2
                                                                       We put some effort into building a robust test script that
10 minutes of execution for each problem. We also                works even for a weak model/agent. We set timeouts on each
                                                                 test, to help agents recover when they write non-terminating
   1                                                             programs. The test script takes care of recompilation when
     We are assuming that the pretraining corpora of propri-
etary models has a distribution similar to the few public pre-   needed, in case the agent forgets to compile. Our first version
training code corpora available for inspection, such as The      only printed failure and used exit code 0 to indicate success.
Stack v2 (Lozhkov et al., 2024). After deduplication, The        We found that Qwen and Gemma had trouble with this format,
Stack v2 has around 200GB of Java and of Python, but only        so we switched to printing PASS and FAIL.
                                                                     3
12GB of Rust and even less OCaml.                                      See §F for the complete prompt template.
      To test your program, run exactly ./test.sh                                GPT-5.5
      [...] These are the only tests I care about.                       90
                                                                         85                Sonnet 4.6
   We believe that this setup is a realistic way to                      80




                                                          Accuracy (%)
study agent behavior: in everyday use, program-                          75     GLM-5.2
mers don’t hide their tests from agents. Instead,                                                          Qwen 3.6
                                                                         70
programmers direct their agents to keep working
until all tests pass. It is this type of task that                       65
MiniLCB simulates, and we get to observe how                             60       Language
                                                                               Python        Rust
agents iterate on their solutions when they have test                    55    Java          OCaml                    Gemma 4
feedback available. With this configuration, there                            1,000                     10,000
is a risk that the agent will cheat, but we only find                                   Output tokens
cheating in 2 out of all traces (§B).
                                                          Figure 1: Accuracy versus median output token usage
   There is also a risk that an agent will timeout        for each model and programming language. The output
while running test cases, if it writes an inefficient     token axis is shown on a logarithmic scale.
or non-terminating solution. To mitigate this, the
test.sh script imposes a 10-second timeout on
each test case. An agent run terminates when the          Controlling for problem difficulty A limita-
agent submits its solution, exhausts its 40-turn bud-     tion of the medians above is that they conflate
get, or exceeds the 600 s wall-clock limit.               programming-language difficulty with problem dif-
                                                          ficulty, both of which affect output tokens. To
4     Results                                             isolate the effect of language, we fit mixed-effects
                                                          models for each LLM: a linear model that assigns
For a complex task, agents may engage in multiple
                                                          a baseline token cost to each problem, so the lan-
turns of reasoning, interleaving different kinds of
                                                          guage coefficients reflect cost differences on the
behavior. Thus, when looking at agent behavior
                                                          same problem. We treat language as a fixed effect
across languages, we can look both at differences
                                                          with Python as the reference level, and the choice
in the turns they take, and in the content of those
                                                          of problem as a random effect. The intraclass corre-
turns. We explore both aspects below.
                                                          lation (ICC) measures what fraction of token-cost
4.1    Token Cost and Accuracy by Language                variance is explained by problem identity; the high
                                                          values (0.80–0.97) confirm that problem difficulty
When comparing agent behavior across program-             dominates, justifying why we control for it.
ming languages, the most basic question is how
                                                             The mixed-effect model allows us to quantify
many tokens are consumed to solve a problem,
                                                          the token penalty (or advantage) for choosing a
which we measure as the total output tokens gener-
                                                          language other than Python, after controlling for
ated over the trajectory (§E).
                                                          problem difficulty (Tables 2 and 7). Across all
Median token cost and accuracy In Figure 1 we             models, OCaml traces consume significantly more
report the median output token usage and accuracy         tokens than Python traces (1.28–1.69× vs. Python,
by language and model. For the models we explore,         p < 0.001). The penalty for using Rust or Java is
accuracy on MiniLCB is not affected very much by          model-dependent, but not significant for Gemma.
language, with the notable exception that Gemma           Overall, these results strongly suggest that token-
performs much worse on OCaml. However, output             maxxers should not use Python, and of these lan-
tokens vary substantially by language. We report          guages, OCaml is best for tokenmaxxing.
medians because token costs are heavy-tailed: a
few hard problems inflate the mean. For all mod-          4.2             Where Do All Those Tokens Go?
els, agents produce significantly more tokens when
writing OCaml, and the fewest tokens when writing         In the rest of this paper, we go beyond accuracy
Python. We consider token usage across all traces,        and try to shed light on what these agents are doing
and not just the succeeding traces. We believe this       with all of these tokens. We present the results
is realistic: if an agent runs for hours and fails, you   for open-weight models below; the corresponding
don’t get a refund.                                       results for proprietary models are provided in §D.
Table 2: Mixed-effects model results: multiplicative           dreds or thousands more tokens after they find their
output token cost relative to Python, after controlling for    first working solution.
problem difficulty. OCaml has a significant penalty with
all models; Java and Rust effects are model-dependent.         4.2.2 Progression on provided unit tests
                                                               We now analyze trajectories by running the test
 Model       Contrast             Extra toks    Significance
                                                               suite on every intermediate solution that the agent
             Java vs. Python          0.85×     p = 0.114      writes to disk and record the list of test outcomes.
             Rust vs. Python          1.07×     p = 0.480
 Gemma                                                         This allows us to abstract each trajectory to a list
             OCaml vs. Python         1.44×     p < 0.001
             ICC                        0.80    —              of solution snapshots, s0 , s1 , . . . , sn , where each
             Java vs. Python          1.21×     p < 0.05       si is a list of test outcomes. We then classify each
             Rust vs. Python          1.20×     p < 0.05       consecutive pair (si−1 , si ) based on how the test
 Qwen
             OCaml vs. Python         1.69×     p < 0.001
             ICC                        0.89    —              outcomes change from si−1 to si :
                                                                 • breakthrough: some tests were failing and all
             Java vs. Python          1.34×     p < 0.01
             Rust vs. Python          1.57×     p < 0.001          now pass;
 GLM
             OCaml vs. Python         1.54×     p < 0.001        • stay: all tests passed before and after, i.e.,
             ICC                        0.73    —
                                                                   model rewrote a correct solution);
                                                                 • improved: some failing tests now pass (but not
Table 3: We run all intermediate solutions that the agent          all);
generates and report the number of tokens (turns) to the
                                                                 • regressed: some passing tests now fail (but not
first solution that passes all tests, and the tokens (turns)
spent after that solution.                                         all fail);
                                                                 • churn: some passing tests now fail, and failing
                          Tokens (Turns)    Tokens (Turns)         tests now pass (improvement and regression);
 Model       Language
                            to Solution      after Solution      • broke: some tests were passing, but now all fail,
             Python             1743 (1)           3554 (3)        e.g., a compile error
             Java               2454 (1)           4546 (2)      • stuck: some tests fail, and no change in test
 Gemma
             Rust               2026 (1)           7311 (3)
             OCaml              1760 (2)           1173 (2)        outcomes
             Python             1755 (1)            283 (3)
                                                                  We build a graph where nodes represent these
             Java               2138 (1)            272 (2)    outcome changes, as well as special nodes for the
 Qwen
             Rust               2409 (3)            370 (4)    start state, a submission (which may be wrong!), or
             OCaml              3177 (5)            405 (4)
                                                               reaching a resource limit.
             Python              758 (1)            117 (2)       In Figure 2, we show the graphs for Gemma and
             Java                729 (1)             97 (1)
 GLM                                                           GLM on Python and OCaml. (The corresponding
             Rust               1574 (1)            122 (2)
             OCaml              1374 (3)            109 (2)    GPT-5.5 graphs appear in §D.) These graphs al-
                                                               low us to quickly discover interesting behavior in
                                                               the models. For example, Gemma has exactly one
4.2.1    Tokens after the first correct solution               breakthrough→broke edge across all Python prob-
One surprisingly common behavior that we observe               lems in a trajectory that has this shape:
                                                                                     1x
is that agents continue to refine their solutions after
they get it right, sometimes even after all tests pass.         break
                                                               through      broke   stuck
                                                                                             break
                                                                                            through   regressed   stuck   submit
We study this behavior by splitting successful tra-
jectories into two pieces: the turns before and after          Examining it reveals performance anxiety: despite
the agent produces the first correct solution.4                the breakthrough, the model’s reasoning text states:
   Table 3 shows the median number of tokens that                        seems to be correct. However, it might be
each model needed to produce a working solution                          too slow for the given constraints—let’s
for each language and the median number of ad-                           optimize
ditional tokens produced afterward. Our prompt
                                                               Unfortunately, the optimization fails all tests. It cor-
directs the model to print a sentinel message when
                                                               rects it (the second breakthrough), then regresses,
it is done, which requires a few tokens. But, the
                                                               and finally submits broken code.
smaller models (Gemma and Qwen) produce hun-
                                                               4.2.3 Text analysis of snapshot spans
   4
    We test intermediate solutions after the agent concludes
execution. Thus we identify all correct solutions. The agent   The test outcomes of the solution snapshots show
may not test every solution.                                   stages in the agent’s progress, but they do not reveal
                                                                        1

                                                       churn
                                  4    1                                1

                                                                        2
                                                                   7
                       improved                                                 regressed                                             improved                                                  regressed
                                                               2
                                                                                                                                                                                          2
             10                                                                                                                 1
                       17 4       4                                                                                                   26                9
                                                                       2 3                                                             20                                                                2
                                       6                               2                  2        1                                                        1                         13                      1
                                                                   5                                                                                                                 14
 start       17         stuck                                                    broke                      submit   start       78        stuck                                                 broke                      submit
                                           9                                                                                                                    37
                                                                                               7
                                                                                                                                                                                                                  35
           52                     1                                                                                          1196                                                    21
                  15                                                        1             40           34                             1                                                                                14
                       12                                                                9                                                54                                                             10
            73                                     1                                                                            21

                                                                                                                                                                13
                        break                                          54         stay                                                     break                                      28          stay
                       through                 6                                                                                          through
                                                                                                                                                                     2
                                                              205                                                                                               42                   56
                                               4       4                                                                                                                                   1
                                                                                     1
                                                                            9                                                                                                               3
                                                                                                                                                                3
                                                           limit                                                                                                             limit


                                 (a) Gemma Python                                                                                                   (b) Gemma OCaml
                                                                                                                                                        2

                                                                                                                             start    23            stuck                            improved

                                                                                                                                      7
                                                                                                                                                   22                                              1
                                                                                                                                      52
                                                                                     1                                                                                   2

         start         75        break                        74                                                                                    break                       76
                                through                                     submit                 limit                                           through                                 submit                 limit


                                      (c) GLM Python                                                                                                    (d) GLM OCaml

Figure 2: We test every solution that the agent writes to the solution file, which allows us to abstract each trajectory
into a list of solution snapshots with test outcomes. We then classify each consecutive pair of test outcomes based
on how outcomes change from the previous snapshot to the current snapshot. We describe the outcomes labels
in detail in §4.2.2. The breakthrough and stay nodes are those where all tests pass in the snapshot, and all other
colored nodes are cases where some tests fail. We consolidate trajectories for model-language pairs into individual
graphs to see how models behave on each language.


what kinds of actions the agent takes during these                                                                   • implement: commits real algorithmic logic,
stages. A natural unit for analysis is the turn, but                                                                   building on the current approach; prior code
turns are not semantically coherent: an agent often                                                                    is kept and extended;
needs several turns to accomplish a one action:                                                                      • rewrite: abandons the current approach and
running a test, reading the output, are three turns                                                                    rewrite with a new algorithm;
that make one logical bugfix action. We therefore                                                                    • execute plan: fills in stubs or #TODO placehold-
analyze at the level of snapshot spans. A span                                                                         ers from the prior snapshot with real logic;
consists of everything the agent does as it moves                                                                    • fix bug: named cause, focused patch — the
between two consecutive solution snapshots: the                                                                        agent identified the bug and targets it directly;
resulting solution snapshot, the unified diff to the                                                                 • debug failure: cause unknown — speculative
previous snapshot, the change in test outcomes, and                                                                    tweaks, debug prints, or repeated attempts with-
the agent’s reasoning, bash command tool calls,                                                                        out a named cause;
and outputs up to and including the ending write.                                                                    • infra confusion: struggling with scaffolding
                                                                                                                       rather than the algorithm: wrong file conven-
   We develop a taxonomy of twelve span labels
                                                                                                                       tions, misread test output, or build plumbing;
by hand-examining a sample of trajectories and
                                                                                                                     • revert: returns to a previously seen solution,
iterating until the labels were mutually exclusive
                                                                                                                       discarding recent changes;
and covered the full range of behaviors. We then
                                                                                                                     • verify: confirms correctness with no code
labeled all spans by prompting an LLM judge (GPT-
                                                                                                                       change, before final submission;
5-Mini) with the taxonomy and the span content:
                                                                                                                     • edge case: proactively hardens a specific input
 • explore: working out a tentative approach —                                                                         class with no failing test pointing at it;
   stubs, comments, or exploratory scripts;
                                                      Execute   Fix   Debug       Infra                        Edge     Optimize Cosmetic
      Model     Lang Implement Explore      Rewrite
                                                       plan     bug   failure   confusion
                                                                                             Revert   Verify
                                                                                                               case      perf.   refactor


      Gemma     java   31%        8%         7%         –        8%    4%         1%          –       26%      2%        4%        7%
                ocaml 17%          6%        2%        1%       16%   15%         5%         23%       7%      1%         –        5%
                python 25%         8%        4%        2%        8%   3%          1%         4%       19%      1%        10%      16%
                rust   27%        10%        5%        1%        8%   2%          1%         3%       23%      3%        4%       14%
      Qwen      java   36%        5%         8%         –       16%    7%          1%           –     27%       –         –         –
                ocaml 19%         6%         5%        1%       37%    8%         12%           –     11%       –         –        2%
                python 35%        4%         8%         –       14%    4%           –           –     29%       –        4%        1%
                rust   36%        4%         8%         –       15%    3%          1%           –     29%      1%         –        2%
      GLM       java   50%        1%          –         –        1%     –          –            –     49%        –         –        –
                ocaml 41%          –          –         –       13%    1%         4%            –     41%        –         –       1%
                python 49%         –          –         –       1%      –         1%            –     49%        –         –        –
                rust   48%        1%          –         –        4%     –          –            –     47%        –         –        –

Table 4: Percentage of spans assigned each label, for every (model,language) pair. GLM is mostly implement + verify;
debugging labels concentrate in OCaml; post-success labels are Gemma-dominated.


  • optimize perf : improves time/memory;                             by revert (31%): the agent rewrites a byte-identical
  • cosmetic refactor: renaming, reformatting, or                     solution that it has already tried, oscillated between
    commenting with no behavioral change.                             2-3 broken attempts. The agent is fighting OCaml
   For example, the following three-turn span is                      syntax, not the algorithm: 92% of failed snapshots
labeled fix bug:                                                      are compile-time errors and 8% are wrong-answer
                                                                      failures. The model rarely gets far enough to learn
 Assistant: Let me test this optimized solution with the              whether its algorithm is correct. Escape, when it
 sample cases first, then run the full test suite.                    comes, is a language learning event: fix bug domi-
 Assistant: The output is wrong. Let me debug...                      nates breakthrough at 60% (Table 5), the moment
 Assistant: I see the bug ... Let me fix:                             the agent finally names a concrete OCaml-specific
                                                                      error and the unchanged algorithm immediately
   The next two-turn span is an implement, where                      passes. Python breakthroughs, by contrast, are
Qwen first solves the problem in Python and then                      spread across implement, execute plan, and opti-
translates to OCaml:                                                  mize perf —there is no single bottleneck to escape.
                                                                         On task abc311_d, for instance, Gemma loops
 Assistant: The v3 formula passes all 31 tests. Let me
 verify it more carefully and then implement it in OCaml:             on stuck 14 times before escape:
                                                                                14x
 cat << 'PYEOF' > analyze7.py
 ...
                                                                      ▶                      break    stay
                                                                                stuck       through            submit
 Assistant: Now let me implement the solution in OCaml:
                                                                      Gemma keeps the same algorithm throughout but
   For every model–language pair, we report the                       cannot get it to compile, cycling on the same
breakdown of span labels in Table 4. Across mod-                      OCaml type errors. Turns 8–14 oscillate between
els, error-recovery labels—fix bug, debug failure,                    two earlier attempts, re-emitting byte-for-byte iden-
infra confusion, and revert—are disproportionately                    tical code, until it finally names the error and the
associated with OCaml, suggesting that solving                        unchanged algorithm compiles and passes all tests.
OCaml problems requires more iterative correction.
Post-success labels (optimize perf, cosmetic refac-                   4.4       Cosmetic Refactoring
tor) are most prevalent for Gemma, consistent with
its large post-solution token costs in Table 3.                       As a second case study, we examine how Gemma
                                                                      revises perfect solutions (stay loops). Figure 2
4.3    How Do Agents Get (Un)Stuck?                                   shows 205 stay self-loops in Python, the most of
We can use the span labels (§4.2.3) to ask how                        any language. These loops are unnecessary polish-
agents get unstuck on problems, using Gemma on                        ing: cosmetic refactor and optimize perf account
OCaml as an example. This model-lanugage pair                         for half the edges into STAY (Table 6). For exam-
has 1,196 self-loops on the stuck state, dominated                    ple, Gemma solves arc194_e in Python on Turn
2, but then second-guesses its solution and spends             mentions per turn). These keywords appear in both
remaining turns on polish before a timeout:                    affirmative and negative contexts (e.g., “correct”
                                 9x
                                                               and “incorrect”), suggesting that the models re-
      ▶     improved    break    stay   limit
                                                               peatedly reevaluate whether their current solution
                       through
                                                               is correct. The trajectory example in §4.4 illus-
                                                               trates this behavior: after producing a solution that
 Assistant: Turn 3/12. The logic was not quite right. I        retrospectively passes all tests, Gemma remarks,
 need to rewrite. . . .
                                                              “Wait, the input could be quite large,” and repeatedly
 Assistant: Turn 9/12. My current code seems to be work-
 ing on these samples. Is there any other condition? . . .
                                                               rewrites the solution.
 Assistant: Turn 12/12. Okay, the current solution seems      Testing and self-examination. Gemma and
 to be working for the sample cases. “Wait, the input could   Qwen often rewrite solutions without running pro-
 be quite large” . . .
                                                              vided tests: over 70% of their snapshot spans into
                                                              STAY are bare solution writes with no preceding
Turn 3 reformulates the correct solution, Turn 9
adds only inline comments, and Turn 12 changes                test execution. Instead, they frequently challenge
the recursion depth, even though the solution is not          their solutions by replaying the sample inputs or
recursion. It hits the timeout and never submits.             constructing their own test cases.
                                                                 For example, on arc194_e Gemma repeatedly
4.5       Text-Level Analysis                                 revises the solution using tests that it writes itself.
                                                              However, it continues to do so even after it pro-
The case studies above analyzed the structure of
                                                              duces a solution that passes all provided tests—
trajectories—which nodes agents visit and how
                                                              unfortunately, it never runs the provided tests on
they move between them. We now move beyond
                                                              this problem despite directions to do so. This is in
the graph to analyze the content: the text agents
                                                              contrast to GLM, uses the provided tests to stop
produce as they work through a problem.
                                                              much earlier.
Planning in code comments Models sometimes
solve problems in comments before writing code.
                                                               5   Conclusion
E.g., on abc359_d, Gemma spends two turns deriv-              We examine how the choice of programming lan-
ing a DP solution in comments, before translating             guage affects the behavior of coding agents. Our
it into working code. On arc194_a, Qwen writes a              most basic finding is that token consumption can
35-line Java solution with 3,439 lines of comments.           vary significantly by programming language, and
                                                              agents can spend far more tokens on a lower-
Solve in Python, then translate. Models some-
                                                              resource language than higher-resource languages.
times solve problems in Python before translating
                                                                 What is more revealing is what the agent is doing
the solution to an unfamliar target language. E.g.,
                                                              with its tokens on each language. We investigate
to solve abc359_c in OCaml, Qwen first takes 12
                                                              this by abstracting agent trajectories into trajec-
turns to write a Python solution, including a trans-
                                                              tories of intermediate solutions and their test re-
lated test harness. Similarly, to solve arc194_e in
                                                              sults. This analysis exposes a range of token waste
Rust, GLM spends 11 turns in Python testing math-
                                                              patterns—agents polishing solutions after all tests
ematical invariants against a brute-force checker
                                                              pass, and fighting a low-resource language’s syntax
before writing a Rust solution that works immedi-
                                                              rather than improving the solution’s algorithm—
ately. It then returns to Python to stress-test the
                                                              and also more deliberate strategies, such as plan-
solution on a large inputs before submitting.
                                                              ning in code comments and prototyping in Python
Second-guessing in reasoning. Reasoning traces                before translating to an unfamiliar target. We
show that models frequently reconsider their ap-              hope these findings point the way toward designing
proach. Gemma and Qwen reason very reflectively,              agents that work more efficiently across all pro-
frequently using words such as wait and actually              gramming languages.
(7.70 and 7.72 occurrences per turn, respectively),
                                                               Limitations
alongside frequent mentions of correctness (3.89
and 1.70) and efficiency (2.02 and 1.65). GLM                  Our study covers four programming languages and
shows the same tendency more moderately (4.27                  five models; the behaviors we identify may not gen-
second-guessing, 1.65 correctness, 0.87 efficiency             eralize to other models, and the language-specific
effects we observe may change as future models                  generation. IEEE Transactions on Software Engi-
improve pretraining coverage of lower-resource                  neering. ArXiv:2208.08227.
languages. MiniLCB consists of self-contained                 Zhiyu Fan, Kirill Vasilevski, Dayi Lin, Boyuan Chen,
competitive-programming problems with visible                   Yihao Chen, Zhiqing Zhong, Jie M Zhang, Pinjia He,
test cases, solved using a single agent scaffold                and Ahmed E Hassan. 2025. Swe-effi: Re-evaluating
(mini-swe-agent) with a fixed prompt, turn limit,               software ai agent system effectiveness under resource
                                                                constraints. arXiv preprint arXiv:2509.09853.
and timeout. Our findings may therefore not gener-
alize to repository-scale software engineering tasks,         Pengfei Gao and Chao Peng. 2026. More with less: An
or to other agent harnesses.                                    empirical study of turn-control strategies for efficient
                                                                coding agents. In Proceedings of the 48th IEEE/ACM
                                                                International Conference on Software Engineering,
Ethical Considerations                                          ICSE ’26.
Our paper title is a joke. Our intent is to understand        GLM-5-Team, :, Aohan Zeng, Xin Lv, Zhenyu Hou,
why agents tokens in low-resource programming                   Zhengxiao Du, Qinkai Zheng, Bin Chen, Da Yin,
languages so that more efficient multilingual agents            Chendi Ge, Chenghua Huang, Chengxing Xie,
can be built. We discourage using these findings to             Chenzheng Zhu, Congfeng Yin, Cunxiang Wang,
                                                                Gengzheng Pan, Hao Zeng, Haoke Zhang, Hao-
deliberately increase token consumption.                        ran Wang, and 168 others. 2026. Glm-5: from
                                                                vibe coding to agentic engineering.  Preprint,
                                                                arXiv:2602.15763.
References
                                                              Google. 2026.  Gemma 4: Byte for byte, the
All-In Podcast. Jensen huang: Nvidia’s future, physical         most capable open models.    https://blog.
  ai, rise of the agent, inference explosion, ai pr crisis.     google/innovation-and-ai/technology/
                                                                developers-tools/gemma-4/. Accessed: 2026-
Anthropic. 2026.     Claude Sonnet 4.6 System                   06-17.
  Card.        https://www-cdn.anthropic.com/
  78073f739564e986ff3e28522761a7a0b4484f84.                   Yaoqi Guo, Ying Xiao, Jie M. Zhang, Mark Harman,
  pdf. Accessed: 2026-06-17.                                    Yiling Lou, Yang Liu, and Zhenpeng Chen. 2026.
                                                                EET: Experience-driven early termination for cost-
Ben Athiwaratkun, Sanjay Krishna Gouda, Zijian Wang,            efficient software engineering agents. In Findings of
  Xiaopeng Li, Yuchen Tian, Ming Tan, Wasi Uddin                the Association for Computational Linguistics: ACL
  Ahmad, Shiqi Wang, Qing Sun, Mingyue Shang, and               2026.
  1 others. 2022. Multi-lingual evaluation of code gen-
  eration models. arXiv preprint arXiv:2210.14868.            Maria Ivanova, Pavel Zadorozhny, Rodion Levichev,
                                                               Ivan Petrov, Adamenko Pavel, Ivan Lopatin, Alexey
Longju Bai, Zhemin Huang, Xingyao Wang, Jiao Sun,              Kutalev, and Dmitrii Babaev. 2026. Multi-LCB: Ex-
  Rada Mihalcea, Erik Brynjolfsson, Alex Pentland,             tending livecodebench to multiple programming lan-
  and Jiaxin Pei. 2026. How do ai agents spend                 guages. In The Fourteenth International Conference
  your money? analyzing and predicting token con-              on Learning Representations.
  sumption in agentic coding tasks. arXiv preprint
  arXiv:2604.22750.                                           Naman Jain, Alex Gu, Wen-Ding Li, Fanjia Yan, Tian-
                                                                jun Zhang, Sida Wang, Armando Solar-Lezama,
Aleksander Boruch-Gruszecki, Yangtian Zi, Zixuan                Koushik Sen, and Ion Stoica. 2025. Livecodebench:
  Wu, Tejas Oberoi, Carolyn Jane Anderson, Joydeep              Holistic and contamination free evaluation of large
  Biswas, and Arjun Guha. 2026. Agnostics: Learning             language models for code. In International Con-
  to code in any programming language via reinforce-            ference on Learning Representations, volume 2025,
  ment with a universal learning environment. In In-            pages 58791–58831.
  ternational Conference on Learning Representations
  (ICLR).                                                     Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
                                                               Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gon-
Islem Bouzenia and Michael Pradel. 2025. Understand-           zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
   ing software engineering agents: A study of thought-        memory management for large language model serv-
   action-result trajectories. In 2025 IEEE/ACM 40th           ing with pagedattention. In Proceedings of the 29th
   International Conference on Automated Software En-          Symposium on Operating Systems Principles, SOSP
   gineering, ASE ’25.                                         ’23, page 611–626, New York, NY, USA. Association
                                                               for Computing Machinery.
Federico Cassano, John Gouwar, Daniel Nguyen, Syd-
  ney Nguyen, Luna Phipps-Costin, Donald Pinckney,            Han Li, Letian Zhu, Bohan Zhang, Rili Feng, Ji-
  Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson,              aming Wang, Yue Pan, Earl T Barr, Federica Sarro,
  Molly Q Feldman, Arjun Guha, Michael Greenberg,               Zhaoyang Chu, and He Ye. 2026. Contextbench:
  and Abhinav Jangda. 2023. MultiPL-E: A scalable               A benchmark for context retrieval in coding agents.
  and extensible approach to benchmarking neural code           arXiv preprint arXiv:2602.05892.
Shuyang Liu, Yang Chen, Rahul Krishna, Saurabh             Yuan-An Xiao, Pengfei Gao, Chao Peng, and Yingfei
  Sinha, Jatin Ganhotra, and Reyhaneh Jabbarvand.            Xiong. 2026. Reducing cost of llm agents with trajec-
  2026. Process-centric analysis of agentic software         tory reduction. Proceedings of the ACM on Software
  systems. Proceedings of the ACM on Programming             Engineering, 3.
  Languages, 10(OOPSLA1):1961–1988.
                                                           Bruce Yang, Xinfeng He, Huan Gao, Yifan Cao, Xi-
Anton Lozhkov, Raymond Li, Loubna Ben Allal, Fed-            aofan Li, and David Hsu. 2025a. Codeagents: A
  erico Cassano, Joel Lamy-Poirier, Nouamane Tazi,           token-efficient framework for codified multi-agent
  Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,          reasoning in llms. arXiv preprint arXiv:2507.03254.
  Tianyang Liu, Max Tian, Denis Kocetkov, Arthur
  Zucker, Younes Belkada, Zijian Wang, Qian Liu,           John Yang, Carlos E Jimenez, Alexander Wettig, Kilian
  Dmitry Abulkhanov, Indraneil Paul, and 47 others.          Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir
  2024. StarCoder 2 and The Stack v2: The Next               Press. 2024. Swe-agent: Agent-computer interfaces
  Generation. Preprint, arXiv:2402.19173.                    enable automated software engineering. Advances in
                                                             Neural Information Processing Systems, 37:50528–
Mike A Merrill, Alexander G Shaw, Nicholas Carlini,          50652.
  Boxuan Li, Harsh Raj, Ivan Bercovich, Lin Shi,
  Jeong Yeon Shin, Thomas Walshe, E Kelly Buchanan,        John Yang, Kilian Lieret, Carlos E. Jimenez, Alexan-
  and 1 others. 2026. Terminal-bench: Benchmarking           der Wettig, Kabir Khandpur, Yanzhe Zhang, Binyuan
  agents on hard, realistic tasks in command line inter-     Hui, Ofir Press, Ludwig Schmidt, and Diyi Yang.
  faces. arXiv preprint arXiv:2601.11868.                    2025b. Swe-smith: Scaling data for software engi-
                                                             neering agents. Preprint, arXiv:2504.21798.
OpenAI. 2026. GPT-5.5 System Card. https://
  openai.com/index/gpt-5-5-system-card/. Ac-               Daoguang Zan, Zhirong Huang, Wei Liu, Hanwu
  cessed: 2026-06-17.                                        Chen, Shulin Xin, Linhao Zhang, Qi Liu, Li Aoyan,
Dangfeng Pan, Zhensu Sun, Cenyuan Zhang, David Lo,           Lu Chen, Xiaojian Zhong, and 1 others. 2026. Multi-
  and Xiaoning Du. 2026. The hidden cost of read-            swe-bench: A multilingual benchmark for issue re-
  ability: How code formatting silently consumes your        solving. Advances in Neural Information Processing
  LLM budget. In Proceedings of the 48th IEEE/ACM            Systems, 38.
  International Conference on Software Engineering,
                                                           Shaoqiu Zhang, Yuhang Wang, Jialiang Liang, Yul-
  ICSE ’26. Distinguished Paper Award.
                                                             ing Shi, Wenhao Zeng, Maoquan Wang, Shilin He,
Yuhao Qing, Boyu Zhu, Mingzhe Du, Zhijiang Guo,              Ningyuan Xu, Siyu Ye, Kai Cai, and 1 others. 2026.
  Terry Yue Zhuo, Qianru Zhang, Jie M Zhang, Heming          Swe-explore: Benchmarking how coding agents ex-
  Cui, Siu-Ming Yiu, Dong Huang, See-Kiong Ng, and           plore repositories. arXiv preprint arXiv:2606.07297.
  Luu Anh Tuan. 2025. Effibench-x: A multi-language
  benchmark for measuring efficiency of llm-generated      Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue
  code. Advances in neural information processing             Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos
  systems.                                                    Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark
                                                              Barrett, and Ying Sheng. 2024. SGLang: Efficient
Qwen Team. 2026. Qwen3.6-35B-A3B: Agentic coding              execution of structured language model programs.
  power, now open to all.                                     In The Thirty-eighth Annual Conference on Neural
                                                             Information Processing Systems.
Mohamad Salim, Jasmine Latendresse, SayedHassan
 Khatoonabadi, and Emad Shihab. 2026. Tokenomics:          Qixing Zhou, Jiacheng Zhang, Haiyang Wang, Rui
 Quantifying where tokens are used in agentic soft-          Hao, Jiahe Wang, Minghao Han, Yuxue Yang,
 ware engineering. arXiv preprint arXiv:2601.14470.          Shuzhe Wu, Feiyang Pan, Lue Fan, and 1 others.
Aman Sharma, Sushrut Thorat, and Paras Chopra.               2026. Featurebench: Benchmarking agentic coding
 2026. Frontier coding agents use metaprogram-               for complex feature development. arXiv preprint
 ming to adapt to unfamiliar programming languages.          arXiv:2602.10975.
 Preprint, arXiv:2606.10933.
Lola Solovyeva and Fernando Castor. 2026. Babbling
  suppression: Making LLMs greener one token at a
  time. Preprint, arXiv:2604.06755.
Marilyn Strathern. 1997. ‘improving ratings’: audit
 in the british university system. European Review,
 5(3):305–321.
Zhensu Sun, Chengran Yang, Xiaoning Du, Zhou Yang,
  Li Li, and David Lo. 2025. Token sugar: Mak-
  ing source code sweeter for LLMs through token-
  efficient shorthand. In 2025 IEEE/ACM 40th Interna-
  tional Conference on Automated Software Engineer-
  ing, ASE ’25, pages 2440–2451.
A    Hyperparameters and Configurations                D    Proprietary Model Results
                                                       Table 7 reports the mixed-effects model for the pro-
We run open-weight models containers on a server
                                                       prietary models. As with the open-weight models,
with a Xeon Gold 6342 CPU, H100 GPUs, and 1TB
                                                       every language incurs a significant output-token
RAM. We serve models locally with vLLM(Kwon
                                                       cost penalty relative to Python after controlling for
et al., 2023), with a 128K context length. We use
                                                       problem difficulty.
the official FP8 checkpoint for Qwen 3.6. We use
                                                          The higher token costs for non-Python languages
the model’s recommended sampling parameters.
                                                       are reflected in the trajectory patterns shown in
Gemma 4: temperature 1.0, top-p 0.95, top-k 64;
                                                       Figure 3, the GPT-5.5 counterpart to Figure 2 in
Qwen 3.6: temperature 1.0, top-p 0.95, top-k 20.
                                                       the main text. On Python, GPT-5.5 almost al-
We impose a 6K token reasoning budget on both
                                                       ways reaches a correct solution on the first write
models. For GLM, we use the HuggingFace Infer-
                                                       (start→breakthrough: 90), with almost no stuck
ence API with temperature 1.0, top-p 0.95, high-
                                                       activity. On OCaml, it enters stuck more often
effort reasoning, and a maximum output length of
                                                       (start→stuck: 27) and accumulates 13 stuck self-
11,000 tokens per turn (covering both reasoning
                                                       loops before recovering.
and visible output). Finally, we run GPT-5.5 with
                                                          Tables 8 and 9 show that proprietary models
‘medium’ reasoning, and run C LAUDE -S ONNET-
                                                       follow a much more direct workflow than the open-
4.6 with reasoning enabled and a 10K token reason-
                                                       weight models. Most trajectories consist of a sin-
ing budget. Reproducing our full experiment (400
                                                       gle implementation phase followed by verification,
tasks per model) requires approximately 28 GPU-
                                                       indicating that the models typically write the solu-
hours for Gemma and 19 GPU-hours for Qwen
                                                       tion once, immediately run ./test.sh, and submit
on H100s if run sequentially (request-level concur-
                                                       if all tests pass. Despite this streamlined execu-
rency can reduce this substantially), and approx-
                                                       tion, proprietary models still externalize substantial
imately $100 for GPT-5.5, $150 for Sonnet, and
                                                       reasoning into code. For example, on arc194_a,
$25 for GLM at standard API rates as of July 2026.
                                                       GPT-5.5 first writes a draft solution.py contain-
                                                       ing only commented-out derivations and a pass,
B   Do Agents Cheat on MiniLCB?                        then overwrites it with a complete implementation
                                                       in the same turn. Similarly, Sonnet sometimes rea-
A natural concern with visible tests is that agents    sons in separate scratch files, solving one problem
may cheat by hard-coding expected outputs rather       in a 700-line think.py before writing the final
than solving the problem. To check for this, we task   Rust solution. Proprietary models also frequently
an LLM judge to flag suspicious solutions from the     use Python as a reasoning language before translat-
problem and final code, and we manually inspect        ing to the target language. On arc194_e in OCaml,
every flagged case. Across all problems, languages,    Sonnet spends 23 turns exploring the problem in
and models we find only two instances, both from       Python, writing a series of brute-force scripts to
GPT-5.5 on the same problem instance: the model        discover and verify the invariant before produc-
derives a nearly-correct rule, hits one visible test   ing an OCaml solution that passes all 32 tests on
that contradicts it, and adds an exact-match guard     the first write. Likewise, GPT-5.5 often embeds
for that case. Cheating is therefore negligible and    Python directly via python3 -c or heredocs to pro-
does not affect our analysis.                          totype algorithms or validate invariants, especially
                                                       for OCaml (27% of problems), Rust (19%), and
C    Snapshot Span Label Distributions                 Java (18%). These Python executions range from
                                                       quick scratch calculations to full solution proto-
Tables 5 and 6 give the full label breakdowns for      types before translation. This behavior becomes
Gemma discussed in §4.3 and §4.4. Table 5 shows        more frequent on harder problems, suggesting that
fix bug dominating OCaml’s stuck→breakthrough          models adapt their workflow when additional algo-
escapes, versus a spread across implement, exe-        rithmic exploration is required.
cute plan, and optimize perf on Python. Table 6
                                                       E   Measuring Agents’ Token Usage
shows Gemma spends turns looping on STAY doing
cosmetic refactor and optimize perf —unnecessary       For any nontrivial problem that takes more than
polishing under the benchmark’s design.                one turn to solve, the agent’s conversation history
                                                                                                                   1
                     improved                                                             improved                         limit


                1                                                                   4
                      1    1                                                               1                               1


                 2                                                                   27                                   1
     start             stuck                                 submit         start          stuck                                    submit
                                                92                                                                        89
                                                                                    13
                                1                            1                                       3
                      2                                                                   25
                90                                                                  61

                       break                1        stay                                  break
                      through                                                             through


                          (a) GPT-5.5 Python                                                   (b) GPT-5.5 OCaml

 Figure 3: Solution-snapshot transition graphs for GPT-5.5, using the same node and edge semantics as Figure 2.


                                                                      Table 7: Mixed-effects model results for GPT-5.5 and
                                                                      Sonnet: All three languages incur a significant output-
                                                                      token cost penalty relative to Python after controlling
             Label                   Python      OCaml                for problem difficulty.
                                    (n = 12)    (n = 53)
             implement                  17%                  4%        Model         Contrast                   Extra toks         Significance
             rewrite                      –                  4%                      Java vs. Python                1.30×          p < 0.001
             execute plan               25%                  6%                      Rust vs. Python                1.36×          p < 0.001
             fix bug                    33%                 60%        GPT-5.5
                                                                                     OCaml vs. Python               1.30×          p < 0.001
             debug failure                –                  6%                      ICC                              0.94         —
             infra confusion              –                  9%
             optimize perf              25%                   –                      Java vs. Python                1.18×          p < 0.001
             cosmetic refactor            –                 11%                      Rust vs. Python                1.16×          p < 0.001
                                                                       Sonnet
                                                                                     OCaml vs. Python               1.28×          p < 0.001
                                                                                     ICC                              0.97         —
Table 5: Label distribution on edges from stuck to break-
through for Gemma. OCaml breakthroughs are primar-
ily due to fix bug.                                                   Table 8: We run all intermediate solutions that the agent
                                                                      generates and report the number of tokens (turns) to the
                                                                      first solution that passes all tests. Proprietary models
                                                                      tend to submit their solution directly.

                                                                                                         Tokens (Turns)        Tokens (Turns)
                                                                       Model         Language
                                                                                                           to Solution          after Solution
                                                                                     Python                     601 (2)                  42 (1)
             Label                  % of edges into STAY                             Java                       841 (2)                  42 (1)
                                                                       GPT-5.5
                                                                                     Rust                       782 (3)                  43 (1)
             cosmetic refactor                              34%                      OCaml                      910 (2)                  44 (1)
             optimize perf                                  22%
             implement                                      18%                      Python                     878 (2)                103 (1)
             verify                                          8%                      Java                      1149 (1)                 95 (1)
                                                                       Sonnet
             fix bug                                         5%                      Rust                      1134 (1)                136 (2)
             revert                                          4%                      OCaml                     1484 (2)                136 (1)
             edge case                                       3%
             explore                                         2%
             debug failure                                   2%
             infra confusion                                 1%       is fed back into the model, turn after turn. So
             execute plan                                    1%       output tokens become input tokens, and the total
             rewrite                                         1%       number of input tokens over several turns can grow
                                                                      enormous. However, on a good inference platform,
Table 6: Label distribution across all edges entering
                                                                      input processing is much cheaper than generating
STAY for Gemma on Python (n=258). Over half are cos-
metic refactoring or performance micro-optimization—                  outputs, especially when the platform supports pre-
changes that are unnecessary under the benchmark’s                    fix caching (Zheng et al., 2024). When an agent
stated objective.                                                     works autonomously to solve a problem over sev-
                                                                      eral turns, prefix caching is very effective, and what
                                                                      matters most is the time required to generate out-
                                                                      puts. This is why, like many others, we report
                                                    Execute   Fix   Debug       Infra                       Edge   Optimize Cosmetic
    Model       Lang Implement Explore    Rewrite
                                                     plan     bug   failure   confusion
                                                                                          Revert   Verify
                                                                                                            case    perf.   refactor


    GPT-5.5     java   49%         –        –         –       2%     1%         1%          –      49%       –       –         –
                ocaml 41%         1%        –         –       7%      –        11%          –      39%       –       –         –
                python 48%         –       1%        1%       2%      –        1%           –      48%       –      1%         –
                rust   49%         –       1%         –       1%      –         1%          –      49%       –       –         –
    Sonnet      java   45%        1%       2%         –       7%     1%          –          –      44%       –       –         –
                ocaml 45%         1%       2%         –       8%      –          –          –      42%       –       –         –
                python 45%        4%       1%         –       2%     1%         1%          –      41%       –      3%         –
                rust   47%        1%       1%         –       4%     1%         1%          –      45%       –       –         –

Table 9: Percentage of spans assigned each label, for every (model, language) pair. GPT-5.5 and Sonnet are mostly
implement + verify; debugging labels concentrate in OCaml; optimizations concentrate in python.


the total number of output tokens generated over a                      • Your solution will be compiled and run as: COM-
                                                                          PILE_AND_RUN
single conversation.                                                    • A test runner is provided at ./test.sh. It runs the
   With contemporary reasoning models, the out-                           solution against every visible test, diffs the output,
put tokens include both the reasoning and normal                          and prints PASS or FAIL with each test input/output
                                                                          filename.
output. In this paper, we work with both closed and                     • To test your program, run exactly: ./test.sh
open-weight and reasoning models. The closed                            • These are the only tests I care about. If ./test.sh exits
models that we use, from OpenAI and Anthropic,                            with status 0, the solution passes the tests; empty
                                                                          diff output means success.
do not expose the reasoning output to users, but
                                                                     ## Submission
users are still charged for the reasoning tokens pro-                   When ./test.sh exits with status 0,                    im-
duced. From the perspective of the user, output                      mediately submit by running:                 echo COM-
tokens cost the same, whether or not the output is                   PLETE_TASK_AND_SUBMIT_FINAL_OUTPUT
visible to the user.                                                 User: Solve the following competitive programming prob-
                                                                     lem in PROGRAMMING_LANGUAGE.
F   System Prompt                                                    # Programming Problem:
                                                                        PROBLEM
What follows is the template for the agent’s prompt.
We substitute the template variables (italicized)
with the problem text and the language configu-
ration.

 System: You are a competitive programming solver that
 can interact with a computer shell to solve programming
 tasks.
    You are operating in an environment where you will
 think and issue AT LEAST ONE command, the system
 executes the command(s) in a subshell, you see the result,
 then you think and issue your next command(s).
    **CRITICAL REQUIREMENTS:**
     • Your response SHOULD include reasoning text ex-
        plaining what you’re doing
     • Your response MUST include AT LEAST ONE bash
        tool call. You can make MULTIPLE tool calls in
        a single response when the commands are indepen-
        dent (e.g., reading multiple files).
 # Task Instructions
 ## Environment
     • Your working directory contains a tests/ directory,
        with test cases (0-indexed)
     • the input is tests/input_N.txt and the expected output
        is tests/output_N.txt
     • The problem statement is provided below in this
        message.
     • Write your solution to: FILENAME
