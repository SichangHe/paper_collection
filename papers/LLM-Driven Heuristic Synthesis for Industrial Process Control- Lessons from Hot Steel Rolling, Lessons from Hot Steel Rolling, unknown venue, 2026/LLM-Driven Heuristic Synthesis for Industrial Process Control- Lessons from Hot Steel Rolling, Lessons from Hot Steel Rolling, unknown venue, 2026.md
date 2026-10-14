                                                 LLM-Driven Heuristic Synthesis for Industrial Process Control:
                                                              Lessons from Hot Steel Rolling

                                                                  Nima H. Siboni∗1 , Seyedreza Kiamousavi2 , and Emad Scharifi2
                                                                              1 Juna.ai, Kastanienallee 32, 10435 Berlin , nima@juna.ai
                                                                        2 Institute of Metal Forming, RWTH Aachen, Intzestr. 10, 52072 Aachen ,

                                                                        {Seyedreza.kiamousavi,emad.scharifi}@ibf.rwth-aachen.de


                                                                                            ∗ Corresponding author
arXiv:2603.20537v1 [cs.AI] 20 Mar 2026




                                         Abstract                                                                a domain expert cannot inspect why a particular action was
                                                                                                                 chosen, making deployment in safety-critical settings difficult.
                                         Industrial process control demands policies that are inter-             One-shot code generation by large language models (LLMs)
                                         pretable and auditable, requirements that black-box neural              offers interpretability but lacks the iterative refinement needed
                                         policies struggle to meet. We study an LLM-driven heuristic             for complex multi-objective control.
                                         synthesis framework for hot steel rolling, in which a language             Recent work on LLM-driven heuristic search [Romera-
                                         model iteratively proposes and refines human-readable Python            Paredes et al., 2024, Liu et al., 2024, Ye et al., 2024] has
                                         controllers using rich behavioral feedback from a physics-              shown that iterative code generation can discover effective
                                         based simulator. The framework combines structured strategic            strategies in combinatorial domains. We present a case study
                                         ideation, executable code generation, and per-component feed-           applying this paradigm to industrial process control, where
                                         back across diverse operating conditions to search over control         interpretability and safety auditability are first-class require-
                                         logic for height reduction, interpass time, and rolling veloc-          ments. The main contribution is a case study with practical
                                         ity. Our first contribution is an auditable controller-synthesis        design lessons about auditable heuristic synthesis and restart
                                         pipeline for industrial process control. The generated con-             budgeting, rather than a comprehensive benchmark against all
                                         trollers are explicit programs accessible to expert review, and         alternative control methods. Our contributions are:
                                         we pair them with an automated audit pipeline that formally             1. A search loop with rich behavioral feedback—per-
                                         verifies key safety and monotonicity properties for the best                component reward decompositions across diverse operating
                                         synthesized heuristic. Our second contribution is a principled              conditions—rather than scalar fitness, enabling rapid con-
                                         budget allocation strategy for LLM-driven heuristic search: we              vergence to competent control policies.
                                         show that Luby-style universal restarts—originally developed            2. A budget allocation analysis across 52 independent runs
                                         for randomized algorithms—transfer directly to this setting,                on a physics-based hot rolling simulator, showing that
                                         eliminating the need for problem-specific budget tuning. A                  splitting a fixed budget into several short runs outperforms
                                         single 160-iteration Luby campaign approaches the hindsight-                a single long run, and a Luby-style universal restart
                                         optimal budget allocation derived from 52 ad-hoc runs totalling             strategy that operationalises this finding without requiring
                                         730 iterations.                                                             retrospective analysis.
                                                                                                                 3. A five-layer automated audit pipeline that checks each
                                         1    Introduction                                                           generated heuristic against domain-grounded safety, mono-
                                                                                                                     tonicity, responsiveness, and consistency specifications—
                                         Hot steel rolling is a multi-pass sequential decision problem               formally proving key safety properties via Z3 SMT and
                                         in which a heated slab is progressively reduced in thickness                verifying the remainder through property-based testing—
                                         through a series of rolling passes. At each pass, the operator              bridging the gap between human-readable code and
                                         must choose a height reduction, an interpass waiting time, and              deployment-oriented verification evidence.
                                         a rolling velocity—balancing competing objectives including
                                         dimensional accuracy, metallurgical quality (grain size, temper-        2     Method
                                         ature), equipment constraints, and process efficiency. Industrial
                                         pass schedules are traditionally designed by experienced engi-          2.1    Problem Formulation
                                         neers using empirical rules and iterative simulation, limiting          We formulate hot rolling pass schedule design as an episodic
                                         adaptability to new product specifications.                             control problem. The environment, FlatRollingEnv, wraps
                                            Reinforcement learning (RL) can learn effective policies for         the PyRoll physics simulator [Weiner et al., 2023] in a
                                         such problems, but the resulting neural networks are opaque:            Gymnasium-compatible interface [Towers et al., 2024]. The


                                                                                                             1
state is a 10-dimensional vector comprising the current and                                Table 1: Search configuration.
target thickness, grain size, and temperature, plus rolling force,
torque, height reduction (HR) limit, and step count. The action                     Parameter                                 Value
space has three components: height reduction (0–50 mm in                            LLM model                        Gemini 2.5 Pro
0.1 mm steps, 501 levels), interpass time (1–120 s, 121 levels),                    Temperature                                  0.7
and rolling velocity (7 discrete levels). Episodes terminate                        Outer iterations per run                   1–30
when the target thickness is reached or after 25 passes.                            Independent runs                              52
   Each candidate heuristic is a deterministic Python function:                     Ideas per iteration                            3
def heuristic(info: dict,
                                                                                    Repair attempts per heuristic                  3
            action_mask: dict) -> list[int]                                         Evaluation scenarios                           8
                                                                                    Max episode length                    25 passes
receiving the physical state and a validity mask that constrains                    Stagnation threshold                6 iterations
actions to physically feasible values. Heuristics execute in a                      Conversation compaction         max 25, keep 10
sandboxed environment restricted to numpy and math.
   The reward function has five components per step: (1) a
step penalty (−5.0) encouraging efficiency, (2) a grain size
progress bonus with asymmetric penalties for undershooting,
(3) a height reduction efficiency bonus (0–10) rewarding use               the weakest reward component), and Radical Exploration (stag-
of equipment capacity, and terminal bonuses for (4) grain                  nation exceeds threshold—demand fundamentally different
size accuracy (0–25) and (5) temperature accuracy (0–25).                  strategies). When the conversation exceeds a length threshold,
Performance during search is measured as the mean total                    older messages are replaced by an LLM-generated summary
reward across 8 search feedback scenarios spanning four axes               (produced by the same Gemini 2.5 Pro model) that preserves
of variation: thickness targets, grain size targets, equipment             strategies attempted, their results, key errors, and learnings;
limits, and temperature targets. These same scenarios provide              the most recent messages are retained verbatim.
the per-component behavioral feedback that guides the LLM’s
refinement at each iteration.                                              2.3    LLM Configuration
2.2    Search Algorithm                                                    We use Gemini 2.5 Pro [Google DeepMind, 2025] via the
The search proceeds over 𝑁 outer iterations, each consisting of            Google Generative AI API with function calling. The sys-
four phases (Figure 1 shows the resulting reward trajectories              tem prompt includes the complete environment and reward
across runs):                                                              function source code alongside structured domain knowl-
   Phase 1: Strategic Ideation. The LLM generates 𝑘=3                      edge on S355 steel hot rolling metallurgy. Two tools
distinct strategy proposals in natural language, each addressing           are exposed: read_file for inspecting source code and
reduction scheduling, interpass timing, velocity strategy, grain           suggest_a_heuristic for submitting candidate implemen-
size management, and the roughing-to-finishing transition.                 tations.
This separation of strategic reasoning from code prevents
premature commitment to implementation details.
   Phase 2: Idea Selection. The LLM selects the most                       3     Experimental Setup
promising strategy with a justification grounded in the multi-
objective reward structure.                                                We conduct 52 independent search runs with the configuration
   Phase 3: Implementation. The LLM implements the se-                     in Table 1, totalling 730 iterations (mean 14.0 per run, range
lected strategy as executable Python via a tool-calling interface.         1–30). For the budget allocation analysis, we use all available
Failed compilations or runtime crashes trigger up to 3 repair              data.
attempts.
   Phase 4: Evaluation and Feedback. The heuristic is          The 8 search feedback scenarios span four axes of variation:
                                                            (1) two thickness specifications (80→12 mm and 120→8 mm),
executed across all 8 scenarios. For each scenario, the system
                                                            (2) two grain size targets (10 𝜇m and 15 𝜇m), (3) two equipment
returns the total reward, step count, completion status, final state
errors, per-component reward breakdowns, and action mask    limits (HR limit 20 mm and 50 mm), and (4) two temperature
                                                            targets (±50 K from nominal). A heuristic’s primary metric
violations. This rich behavioral feedback—rather than a single
scalar fitness—enables the LLM to diagnose which reward     during search is the mean reward across these 8 scenarios; the
components underperform and in which operating conditions.  secondary metric is the completion rate (fraction of scenarios
                                                            reaching target thickness). For generalization evaluation, we
                                                            additionally test on a held-out grid of 81 scenarios constructed
Adaptive mode selection. The framework employs three from the full combinatorial product of these axes (§4.5).
modes: Exploration (no incumbent best—generate from
scratch, informed by the top-𝑁 best and last-𝑀 recent          A typical 30-iteration run completes in approximately 38 min-
heuristics), Refinement (incumbent exists, stagnation below utes of wall time and consumes 5.7M input tokens and 139K out-
threshold—propose targeted single-variable modifications to put tokens.


                                                                       2
4     Results                                                                                                                   Search convergence (49 runs)
                                                                                                    60

4.1    Baseline Heuristic                                                                           40




                                                                          Best mean reward so far
To contextualise the search results, we define a hand-coded                                         20
baseline heuristic that captures straightforward domain reason-                                         0
ing without any LLM involvement. The baseline uses three                                            20
simple rules: (1) height reduction: apply 80% of the per-pass
                                                                                                    40
HR limit until close to the target thickness, then use the remain-
ing thickness to determine the final reduction; (2) interpass                                       60                                                                        10th-90th pctl
                                                                                                                                                                              IQR (25th-75th)
time: fixed at 10 s regardless of conditions; (3) rolling velocity:                                                                                                           Median
                                                                                                    80                                                                        Mean
a coarse six-level lookup on the temperature error (speed up
                                                                                                                0           5           10          15           20            25                    30
when too cold, slow down when too hot), with no grain size or                                               n=48        n=32            n=25   Iteration
                                                                                                                                                   n=18          n=13         n=12       n=11
force awareness.
   This baseline achieves a mean reward of 41.0 on the 8 search           Figure 1: Best-so-far reward across 52 independent runs. The
feedback scenarios (100% completion) and 46.7 on the 81-case              red line shows the median, the dark band the IQR (25th–
held-out grid. Its thickness precision is strong (0.04 mm mean            75th percentile), and the light band the 10th–90th percentile.
error), but it has no grain size control (7.8 𝜇m mean error—the           Individual traces shown in light blue. Labels indicate how
final grain size is effectively constant regardless of target) and        many runs reached each iteration.
only coarse temperature management (38.8 K mean error). It
also incurs 4 constraint violations (3 force, 1 torque) across the                                                   Iterations to best heuristic (49 runs)
81 test cases.                                                                                                                                                                          1.0
                                                                                                                        50th pctl = 4           90th pctl = 21
   By comparison, the best heuristic discovered by the LLM                                          8




                                                                                                                                                                                          Cumulative fraction of runs
search achieves 55.5 on the 8 search scenarios and 60.9 on                                                                       Mean = 7.8
                                                                                                                                                                                        0.8
the held-out grid—a 30% improvement over the baseline. The
                                                                          Number of runs


                                                                                                    6
improvement is concentrated in temperature control (7.7 K vs.                                                                                                                           0.6
                                                                                                                                                                      Count
38.8 K mean error) and grain size management (6.3 𝜇m vs.                                                                                                              Empirical CDF
7.8 𝜇m), where the LLM-generated heuristic employs propor-                                          4
                                                                                                                                                                                        0.4
tional controllers and strain-based scheduling that the baseline
lacks. We note that this baseline is deliberately simple; a                                         2                                                                                   0.2
more carefully engineered hand-coded controller could narrow
the gap, and the comparison primarily illustrates the type of                                       0                                                                                   0.0
reasoning the search discovers rather than claiming a definitive                                            0           5          10          15          20            25
                                                                                                                    Iteration at which best heuristic was found
advantage over all possible baselines.

4.2    Convergence Behavior                                               Figure 2: Distribution of the iteration at which each run
                                                                          discovers its best heuristic. The 50th percentile is at iteration 4;
Figure 1 shows the best-so-far reward trajectory across all               the mean is at iteration 8.
52 runs. The median converges to approximately 40 within
the first 5 iterations, with rapid initial improvement followed
by diminishing returns. The interquartile range tightens over             radical departures prompted by stagnation crashed with deeply
iterations, indicating that most runs converge to a similar               negative rewards, suggesting that escaping these attractors
performance band despite exploring different strategies.                  remains a challenge for the current prompting strategy.
   Figure 2 reveals that 50% of runs find their best heuristic by
iteration 4 (mean: iteration 8). This early convergence supports          4.3                               Budget Allocation
the budget allocation argument in §4.3: most value is extracted           A key practical question is how to allocate a fixed compute
in the first few iterations.                                              budget: run one long search or many short ones? Comparing
   The best single heuristic across all 52 runs achieves a mean           the expected marginal gain from continuing a run versus
reward of 55.5, discovered via a counterintuitive decoupled               restarting fresh (Figure 3), restarting yields substantially higher
controller architecture in which height reduction controls thick-         marginal gain during the first few iterations, as each fresh start
ness, rolling velocity controls temperature, and interpass time           explores a new region of the strategy space. The two curves
controls grain size. This mapping contradicts standard metallur-          converge around iteration 4, after which both strategies offer
gical reasoning (which assigns temperature control to interpass           diminishing returns—consistent with the early convergence
time) and was discovered by only one run. We observe a strong             observed in Figure 1.
tendency for the LLM to converge on domain-conventional                      Figure 3 formalises this using the empirical best-so-far distri-
strategies—in particular, Thermomechanical Controlled Pro-                butions from the same 52 runs. For each candidate run length 𝐿,
cessing (TMCP) paradigms—which we refer to as mode col-                   we extract the best-so-far reward at iteration 𝐿−1 across all
lapse to familiar architectures. In one 30-iteration run, all four        eligible runs and construct its empirical CDF 𝐹𝐿 . A budget


                                                                      3
                                                                         Table 2: Luby restart campaigns vs. ad-hoc independent runs.
                                                                         “Best” is the global best reward on the 8 search feedback
                                                                         scenarios. “Med.” is the median best-per-run. “Wall” is total
                                                                         wall-clock time.

                                                                                  Strategy                           Runs             Iters             Best            Med.            Wall
                                                                                  Ad-hoc (52 runs)                         52          730              55.5            33.5           ∼36 h
                                                                                  Luby (unseeded)                          15          160              51.6            35.1            4.1 h
                                                                                  Luby (seeded)                            15          160              48.3            41.7            4.1 h


                                                                                              Restart vs depth: first iteration and subsequent rewards
                                                                                                                                           it 0                                                it 23
                                                                                  50
                                                                                                     it 7                   it 9                          it 9
                                                                                  40          it 1
                                                                                                                    it 4
                                                                                                                                   it 16                                 it 4
                                                                                       it 3                  it 4

                                                                                  30
Figure 3: Expected best reward (median) as a function of total




                                                                         Reward
                                                                                                                                                  it 3           it 4
iteration budget for uniform strategies (𝐿=1, 5, 10, 20) and the                  20                                                                                                    it 4
                                                                                                                                                                                it 6
optimal mixed allocation. Labels on the optimal mix curve                         10
show the allocation chosen. Diversified restarts consistently                      0
outperform both single long runs and many short ones.
                                                                                  10
                                                                                          Later iterations
                                                                                          First iteration
                                                                                  20
                                                                                       R1     R2      R3     R4     R5       R6     R7     R8     R9     R10     R11     R12    R13     R14    R15
of 𝑇 iterations allocated as 𝑘 independent runs of length 𝐿                            (5)    (5)    (10)    (5)    (5)     (10)   (20)    (5)    (5)    (10)    (5)     (5)    (10)    (20)   (40)
                                                                                                                                Sub-run (iterations)
yields a global-best CDF of 𝐹𝐿𝑘 (assuming independence); the
expected reward is the median of this distribution. We compare           Figure 4: Per-sub-run decomposition of an unseeded Luby
uniform strategies (all runs of length 𝐿 ∈ {1, 5,Í10, 20}) against       campaign (unit 𝑢=5, 15 sub-runs, 160 total iterations). Hollow
         Î mixed allocation [𝑙 1 , 𝑙2 , . . .] with 𝑙 𝑖 = 𝑇, whose
an optimal                                                               bars show the first-iteration reward; dots show all subsequent
CDF is 𝑖 𝐹𝑙𝑖 . The mixed strategy consistently outperforms               iterations. Labels mark the iteration that achieved each sub-
any uniform strategy. For example, at budget 𝑇=20, the opti-             run’s best reward. Depth consistently improves over the restart
mal mix (10+10) outperforms a single run of 20 by allocating             baseline, but sub-run 8 shows that fresh restarts can also strike
iterations to independent explorations of the strategy space.            gold immediately.
   This finding—diversified restarts outperform single long
runs or many short ones—is a central practical recommenda-
tion. Each run needs enough iterations to reach a reasonable           them). Table 2 compares two Luby campaigns against the
local optimum (pure 𝐿=1 breadth underperforms), but not so             52-run ad-hoc baseline.
many that budget is wasted on diminishing returns (pure 𝐿=20              Figure 4 shows the per-sub-run breakdown. For each of
depth also underperforms). The sweet spot is runs of 5–10              the 15 sub-runs, the hollow bar marks the reward obtained
iterations: long enough to converge, short enough to afford            on the very first iteration (the “restart” contribution), while
multiple independent explorations of the strategy space.               the dots show all subsequent iteration rewards (the “depth”
4.4 Luby-Style Universal Restarts                                      contribution). Labels indicate which iteration achieved the
                                                                       sub-run’s best reward. In 14 of 15 sub-runs, the best reward
The budget allocation analysis above is retrospective: it requires
                                                                       comes from a later iteration—typically between iterations
running many independent searches first and analysing the
                                                                       3 and 9—demonstrating that depth within each sub-run is
empirical distributions after. A practitioner starting a new
                                                                       essential. The sole exception is sub-run 8, where the first
problem cannot know the optimal mix in advance. Luby-
                                                                       iteration immediately produced a reward of 50.0, illustrating
style universal restarts [Luby et al., 1993] offer a principled
                                                                       the complementary value of fresh restarts: a lucky initialisation
alternative: the restart schedule [1, 1, 2, 1, 1, 2, 4, . . .] (scaled
                                                                       can outperform extended refinement.
by a unit 𝑢) is provably within a constant factor of the optimal
fixed-cutoff strategy for any unknown runtime distribution—
requiring no problem-specific tuning.                                  Budget-matched comparison. The optimal mix analysis in
   We implement a Luby restart runner that executes §4.3 is retrospective: computing it required 52 independent
15 sub-runs with unit 𝑢=5, yielding the schedule ad-hoc runs totalling 730 iterations to build reliable empirical
[5, 5, 10, 5, 5, 10, 20, 5, 5, 10, 5, 5, 10, 20, 40] for a total of CDFs. A practitioner starting a new problem has no such data.
160 iterations per campaign. Each sub-run is a fresh search Figure 5 compares the Luby campaign’s actual cumulative best-
with conversation reset; the top 3 heuristics discovered so far so-far against the ad-hoc optimal mix curve. Despite using
can optionally be seeded into subsequent runs as informational only 160 iterations in a single automated session, the Luby
context (the LLM sees them but is not constrained to refine trajectory approaches the optimal mix—which itself required


                                                                     4
                                         Budget-matched comparison: Luby vs ad-hoc strategies                                                            Greedy portfolio: ad-hoc vs Luby
                                50
                                                                                                                                        64              K=4
Expected best reward (median)


                                45                                                                                                                            K=6




                                                                                                                   Mean oracle reward
                                40                                                                                                      62

                                35
                                                                                                                                        60
                                30
                                                                                                                                        58
                                25

                                20                                                                                                      56
                                                                                  Ad-hoc optimal mix                                                                                Ad-hoc (50 runs) (18 heur.)
                                15                                                Luby restarts (best=51.6)                                                                         Luby restarts (156 heur.)
                                     0     20     40      60      80      100     120         140        160                            54
                                                         Total iteration budget                                                              1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
                                                                                                                                                                    Portfolio size (K)
Figure 5: Budget-matched comparison. The black curve
                                                                                                                   Figure 6: Greedy portfolio construction: ad-hoc (18 heuristics)
shows the expected best reward (median) under the optimal
                                                                                                                   vs. Luby (156 heuristics), evaluated on 81 held-out test cases.
mixed allocation, computed retrospectively from 52 ad-hoc
                                                                                                                   Both curves exhibit sharp diminishing returns. The ad-hoc
runs (730 total iterations). The green staircase shows the
                                                                                                                   pool starts higher (single best 60.9 vs. 54.5) but the Luby pool
actual cumulative best achieved by a single unseeded Luby
                                                                                                                   converges to a comparable oracle (64.5 vs. 65.1). Dashed lines
campaign (160 iterations). The Luby schedule approaches the
                                                                                                                   mark the 𝐾 at which 90% of the full-pool gain is captured.
hindsight-optimal strategy without requiring prior data.

                                                                                                                   size, HR limit, and temperature variations).
4.5× as many iterations and hindsight analysis to identify.
                                                                                                                      For the ad-hoc pool, the single best heuristic achieves 60.9
   The best ad-hoc outlier (55.5) was not matched by the Luby
                                                                                                                   and the full oracle reaches 65.1—a portfolio of 𝐾=4 captures
campaign, consistent with the high variance of LLM-driven
                                                                                                                   90% of the gain. The Luby pool starts lower (single best 54.5)
search: exceptional results require either many independent
                                                                                                                   because its heuristics are drawn from many short sub-runs,
trials or fortunate initialisation. However, Luby restarts provide
                                                                                                                   but it converges rapidly: by 𝐾=5 it reaches 63.3 (90% of its
a reliable, automated path to near-top-decile performance
                                                                                                                   10.0-point gain), and the full oracle of 64.5 is within 1% of
without the cost of running 50+ independent searches or the
                                                                                                                   the ad-hoc oracle despite requiring 4.5× fewer total search
need for retrospective budget analysis.
                                                                                                                   iterations to generate. This means that even if evaluating
4.5 Inference Strategies: From Pool to Deploy-                                                                     many candidates per job is undesirable, a pruned portfolio of
    ment                                                                                                           3–5 heuristics provides near-oracle performance at minimal
                                                                                                                   computational cost.
Multiple search runs produce a pool of diverse heuristics. A
key advantage of heuristic policies over neural networks is that
each candidate is a lightweight Python function: evaluating it                                                     Evaluation sets and reported metrics. To clarify compa-
on the physics simulator takes milliseconds per episode, and                                                       rability: the reward of 55.5 (best heuristic across all 52 runs)
verifying it against safety specifications takes under 5 seconds                                                   and 57.4 (best-of-𝑁 across runs) are measured on the 8 search
(§4.8). This makes it practical to evaluate the entire pool on                                                     feedback scenarios used during the search loop. The reward of
each new job specification, filter out candidates with audit                                                       60.9 (best single heuristic) and 65.1 (oracle portfolio) are mea-
failures, and select the best result—the simulator serves as                                                       sured on the separate 81-case held-out grid, which was never
ground truth, eliminating the need for a learned classifier.                                                       used during search. The higher absolute values on the 81-case
   We apply greedy portfolio construction to both the ad-hoc                                                       grid reflect the inclusion of easier scenario combinations in
pool and the Luby pool (Figure 6): starting from an empty                                                          the full combinatorial product; the two sets are not directly
set, at each step 𝐾 we add the heuristic that maximises the                                                        comparable.
oracle reward—defined as the mean, over all test cases, of                                                            The mode collapse discussed in §4.1 becomes an advantage at
the maximum reward achieved by any portfolio member on                                                             the pool level: because different runs converge to different local
that test case. This selects for complementary specialists: the                                                    optima, the resulting heuristics specialise on complementary
second heuristic chosen is not the one with the second-highest                                                     subsets of the operating space, making the portfolio more
individual mean, but the one that best covers scenarios where                                                      diverse than any single run’s trajectory.
the first heuristic underperforms. The ad-hoc pool contains
18 heuristics from the single run that produced the global best                                                    4.6                       Interpretability of the Search Process
heuristic (19 iterations); the Luby pool contains 156 heuristics                                                   Unlike black-box optimization, the LLM search produces a
from all 15 sub-runs of the unseeded campaign. Both are                                                            complete reasoning trace: at every iteration, the model artic-
evaluated on the same 81-case held-out grid (thickness, grain                                                      ulates its strategy in natural language before generating code.


                                                                                                               5
Table 3: Strategy evolution over a 20-iteration search. The 1 # --- Height Reduction Logic ---
LLM’s natural language reasoning reveals how it diagnoses 2 remaining = current_thickness - target_thickness
weaknesses, manages trade-offs, and synthesizes solutions. 34 if remaining < max_hr_mm:
                                                                 # CONSERVATIVE: split into two passes
Reward is the mean across 8 scenarios.                      5    target_hr = remaining * 0.5
                                                                     else:
                                                                     6
                                                                     7  # AGGRESSIVE: strain-based reduction
      Iter    LLM’s stated strategy                      Reward    8    if grain_size > target_grain * 2.0:
                                                                   9       strain = 0.8 # heavy refinement
       0      “Adaptive Two-Phase: bulk reduction          23.5   10    elif grain_size > target_grain:
                                                                  11       strain = 0.4 # moderate refinement
              then precision finishing”                           12    else:
       1      “Fix catastrophic temperature failure:       28.1   13       strain = 0.1 # preservation
                                                                  14    target_hr = thickness * (1 - exp(-strain))
              every scenario loses ∼2.0 pts”                      15
       3      “Proactive heat conservation via             33.8   16 # --- Interpass Time (Temperature Control) ---
                                                                  17 temp_error = temperature - target_temperature
              interpass time modulation”                          18 if temp_error > 25.0:
       8      “Temperature excels but core reduction       35.2   19    frac = clip((temp_error - 25) / 125, 0, 1)
                                                                  20    interpass = 5.0 + frac * 35.0 # 5-40s
              strategy has systemic flaws”                        21 else:
      10      “Radical departure: the conflict between     24.3   22    interpass = 1 # minimal wait
                                                                  23
              thermal and metallurgical efficiency                24 # --- Rolling Velocity (Force Management) ---
              requires a fundamentally new approach”              25 force_limit = 4_000_000
                                                                  26 if force > force_limit * 0.70:
      14      “Fuse strain-based HR with re-tuned          38.0   27    velocity = 2 # slow for safety
              thermal response—hybrid synthesis”                  28 elif force < force_limit * 0.25:
                                                                  29    velocity = 6 # fast for throughput
                                                                  30 else:
                                                                  31    velocity = 5 # default

Table 3 shows a representative excerpt from a 20-iteration run,          Listing 1: Condensed excerpt from the best heuristic (reward
illustrating how the LLM’s understanding deepens through                 55.5). Helper functions and variable unpacking omitted.
interaction with the evaluation feedback.
   Three patterns emerge. First, the LLM explicitly diagnoses
weaknesses using the per-component feedback (iteration 1:
“every scenario loses ∼2.0 pts on temperature”). Second, it                A domain expert can inspect each decision, verify it against
discovers trade-offs between objectives (iteration 8: thermal            metallurgical principles, and modify specific thresholds before
efficiency vs. reduction strategy) and eventually synthesizes            deployment—none of which is possible with a neural network
solutions that balance them (iteration 14). Third, radical               policy. However, manual inspection does not scale: a search run
departures prompted by stagnation (iteration 10) often regress           produces dozens of candidates, and even for a single heuristic,
before enabling later breakthroughs—the hybrid at iteration 14           the number of input combinations is effectively infinite. This
combines insights from both the conservative and radical                 motivates the automated audit described next.
branches.
   This process-level interpretability is a distinctive advantage:       4.8    Automated Safety Auditing
a domain expert can audit not only what the final policy does but        Deploying LLM-generated code in safety-critical industrial
why specific design choices were made, tracing each decision             settings requires more than interpretability: the code must be
back to a diagnosed weakness and a reasoned response.                    systematically verified against domain specifications. Inspired
                                                                         by the formalized specification approach of SpecVerify [Wang
4.7        Interpretability of the Generated Policy                      et al., 2025], we developed a five-layer automated audit pipeline
Each generated policy is a readable Python function with                 that verifies each candidate heuristic:
explicit control logic. Listing 1 shows a condensed excerpt              1. AST structural & security checks (29 checks, 8 categories):
from the best-performing heuristic (reward 55.5). The code                   validates function signature, sandbox compliance, action
reveals three layers of metallurgical reasoning:                             mask usage, bounds clipping, division safety, and return
1. Hybrid height reduction (lines 2–13): A schedule detec-                   path completeness.
   tor distinguishes low-reduction scenarios (conservative 50%           2. Interval analysis: propagates input value ranges through
   split to avoid equipment penalties) from bulk-reduction sce-              the heuristic’s arithmetic to statically verify that all three
   narios (strain-based targets with grain-size-aware schedul-               outputs remain within action bounds.
   ing).                                                                 3. Domain specifications: 11 formal requirements (SPEC-
2. Proportional temperature control (lines 15–20): Inter-                    001–011) covering safety (no overshoot, HR-limit respect),
   pass time computed as a proportional controller on temper-                monotonicity, responsiveness, and consistency properties.
   ature error, with a 25 K deadband and linear scaling up to            4. Z3 SMT verification: proves specs hold for all valid inputs
   40 s of cooling.                                                          by translating the heuristic AST to Z3 constraints. Safety
3. Force-aware velocity (lines 22–26): Rolling velocity                      specs use scalar mask decomposition; monotonicity specs
   adapts to force as a fraction of the equipment limit, reducing            use a two-translation technique that creates two independent
   speed when force exceeds 70% capacity.                                    symbolic evaluations of the heuristic and proves relational


                                                                     6
Table 4: Audit results for the best heuristic (reward 55.5).                                         Audit evolution
                                                                                                              55.5 across search iterations
Five analysis layers produce 65 checks with 0 errors. Z3




                                                                           Reward
                                                                                    40
proves safety specifications for all valid inputs; remaining                        20
specs verified via randomized property testing.                                                                                 3.5
                                                                         Structural    P P P P P P P P P P P P P W P P P P
    Layer                Checks   Pass    Notes                               Security P P P P P W W W W W W W W W W W W W
                                                                         Action mask P P P P P W W W W W W W W P W W W W
    AST (8 categories)      29    27/29   2 warn
    Interval analysis        9     8/9    1 warn                               Bounds P P P P P P P P P P P P P P P P P P
    Z3 SMT prover           10     9/10   5 proved ∀, 4 deferred       Division safety W W W W W P P W W P W P W W W P W W
    Property testing        17    17/17   207 inputs, 0 failures           Info usage P P P P P P P P P P P P P P P P P P
                                                                        Return paths P P P P P P P P P P P P P P P P P P
    Total: 65 checks              61/65   0 errors
                                                                       Domain specs P P W P W P P P P P W P P P P W P P
                                                                                         0   1   2   4     5   7      8   9 10 11 12 13 14 15 16 17 18 19
                                                                                                                           Iteration
                                                                                                         All passed        Warnings only   Has errors
    properties between their outputs.
5. Property-based testing: randomized testing (207 inputs
    including 7 edge cases) verifies specs that Z3 cannot handle Figure 7: Traffic-light heatmap of per-category audit results
    due to complex numpy operations, and catches runtime across 18 iterations of the best ad-hoc run (the same run used
    exceptions.                                                     for portfolio construction in §4.5). Green = all checks passed,
                                                                    amber = warnings only, red = errors. All iterations achieve
   Table 4 shows the audit results for the best heuristic (re-
                                                                    zero errors; warnings appear intermittently in division safety
ward 55.5). The pipeline executes 65 checks with zero errors.
                                                                    and domain specification categories.
Z3 formally proves 5 specifications for all valid inputs, including
three safety properties (no-overshoot, HR-limit respect, non-
negative reduction), HR–thickness monotonicity, and interpass– scenario reward decomposition enables targeted refinement.
grain monotonicity. For the monotonicity specs, the verifier The generated heuristics embed recognizable metallurgical
translates the heuristic’s Python AST to Z3 constraints twice reasoning—grain-size-aware strain scheduling, proportional
with different symbolic inputs to compare outputs—a two- temperature controllers, force-adaptive velocity—despite re-
translation technique that enables proving relational properties ceiving this knowledge only through the system prompt. The
of the generated code. One spec (SPEC-006, velocity de- interpretability of the outputs is a qualitative advantage over RL
creases with force) yields a Z3 counterexample at a degenerate in safety-critical industrial settings, and the automated audit
boundary (force near zero), though property-based testing con- pipeline (§4.8) strengthens this with quantitative verification
firms the property holds across realistic operating ranges. The evidence: Z3 formally proves key safety and monotonicity
remaining 4 specs, involving responsiveness or epsilon-delta properties for all valid inputs, while property-based testing
continuity reasoning, are deferred to property-based testing covers specifications involving constructs beyond Z3’s reach.
with zero failures.
   The audit pipeline runs in under 5 seconds per heuristic and
can be integrated into the search loop as a post-evaluation filter, What fails. Three limitations emerged. First, radical ex-
automatically rejecting candidates that fail safety specifications ploration is unreliable: all four radical departures in one
before they enter the pool.                                         30-iteration run produced architectures that crashed catas-
                                                                    trophically (rewards −79 to −88), suggesting that the current
   Figure 7 shows how audit results evolve across the 18 it-
                                                                    “try something completely different” prompt lacks sufficient
erations of the best ad-hoc run. Structural integrity, security,
                                                                    guidance. Second, conversation compaction causes amnesia:
action mask compliance, bounds, and return paths pass con-
                                                                    effective micro-modifications (e.g., strain-aware roughing, pro-
sistently across all iterations—these categories are effectively
                                                                    portional temperature control) were rediscovered multiple times
enforced by the sandbox and prompt constraints. Division
                                                                    within the same run, indicating that the compaction mechanism
safety and domain specification compliance show intermittent
                                                                    fails to preserve actionable insights. Third, mode collapse
warnings, but no iteration produces an error. Notably, warn-
                                                                    to familiar architectures limits exploration diversity within a
ing counts do not correlate with reward: the best iteration 8
                                                                    single run—the LLM gravitates toward domain-conventional
(reward 55.5) has 3 warnings, while iteration 15 (reward 12.6)
                                                                    reasoning (TMCP-style controllers) and struggles to discover
has 7 warnings. This confirms that the audit captures safety
                                                                    unconventional-but-effective mappings like the decoupled con-
properties orthogonal to reward, making it a complementary
                                                                    troller.
signal for deployment decisions.

                                                              Memory strategy. To address conversation amnesia, we com-
5      Discussion                                             pared two memory strategies: compaction (the default, which
What works. The structured 4-phase loop with rich be- summarises old messages when the context grows too large)
havioral feedback is effective: the LLM consistently gener- and synthesis (which resets the conversation each iteration and
ates competent policies within a few iterations, and the per- provides the LLM with a structured knowledge document main-


                                                                   7
                          60                                n=11                n=9
                                                                                                      n=4       strates LLM-driven policy evolution on LunarLander using
                                           n=12                                                       n=9
                                                                                n=11
                          40n=16           n=23
                                                            n=17                                                population-based search with behavioral feedback; our work
Best mean reward so far


                          20n=35
                                                                                                                differs in using a single-trajectory search with adaptive modes
                                                                                                                (refinement, radical exploration) rather than a population, and
                           0
                                                                                                                focuses on a complex industrial domain with multi-objective
                          20                                                                                    rewards. MLES [Hu et al., 2025] enriches the evolutionary
                          40                                                                                    loop with visual feedback from rollout videos; we pursue a
                                                                                                                complementary direction, using structured per-component re-
                          60
                                                                                                                ward decompositions as feedback. Vulcan [Dwivedula et al.,
                                                                                  Compaction (n=36)
                          80                                                      Synthesis (n=16)              2025] applies LLM-driven heuristic search to systems prob-
                               0   2   4          6   8      10       12   14          16   18        20        lems (cache eviction, memory tiering), demonstrating that
                                                          Iteration                                             the approach generalises beyond RL benchmarks to applied
                                                                                                                domains. While these works focus on the search algorithm or a
Figure 8: Best-so-far reward by memory strategy. Synthesis                                                      single-run evaluation, our case study contributes an empirical
resets the conversation each iteration and provides the LLM                                                     budget allocation analysis across 52 independent runs on a
with a structured ∼800-word knowledge summary synthesised                                                       realistic industrial simulator, showing that diversified restarts
by a narrator; Compaction preserves the full conversation                                                       outperform single long runs in this setting—a practical finding
and summarises old messages when the context grows too                                                          that may generalise to other LLM-driven search settings.
large. Solid lines show medians; shaded bands show IQR. Run
counts decrease at higher iterations as shorter runs drop out.                                                    Hot rolling optimization. Traditional approaches use ge-
The synthesis strategy shows higher median reward in early                                                      netic algorithms [Carreon et al., 2019], mathematical program-
iterations, though sample sizes are modest (16 vs. 36 runs)                                                     ming, or expert systems for pass schedule design. Recent work
and the two groups were run sequentially, so this comparison                                                    applies RL to simplified rolling models [Idzik et al., 2024], but
should be interpreted cautiously.                                                                               typically with analytical rather than physics-based simulators.
                                                                                                                Our environment uses PyRoll [Weiner et al., 2023] for physi-
                                                                                                                cally grounded state transitions including realistic force/torque
tained by a narrator agent). Figure 8 shows that synthesis runs                                                 calculations and microstructural evolution.
achieve higher median reward throughout, with the gap most
pronounced in the first 5 iterations. The best overall heuristic                                                7    Conclusion
(reward 55.5) came from a synthesis run. However, we caution
that sample sizes are modest (16 synthesis vs. 36 compaction                                                    We presented a case study applying LLM-driven heuristic
runs) and the two groups were run sequentially rather than                                                      search to hot steel rolling, demonstrating that this paradigm
interleaved, so confounds such as prompt refinements between                                                    can produce auditable control policies in a realistic industrial
batches cannot be ruled out. More controlled experiments are                                                    simulator. Across 52 independent runs, the framework reliably
needed to establish a robust conclusion.                                                                        produces competent policies within the first few iterations. A
                                                                                                                budget allocation analysis shows that splitting a fixed budget
Practical recommendations. Based on our analysis: (1) allo-                                                     into several short runs outperforms a single long run, as most
cate budget to many short runs (5–10 iterations) rather than few                                                value is extracted early and fresh starts explore diverse strategy
long ones—or use Luby-style restarts (§4.4) to automate this                                                    regions. The generated heuristics are human-readable Python
allocation without problem-specific tuning, (2) use best-of-𝑁                                                   functions embedding explicit metallurgical reasoning, and the
selection across runs (which achieved a reward of 57.4 in our                                                   automated audit pipeline provides deployment assurance by
experiments), (3) invest in structured memory mechanisms                                                        formally proving key safety properties via Z3 for all valid inputs
to mitigate conversation amnesia, and (4) run the automated                                                     and verifying the remaining specifications through property-
audit on all deployment candidates—the pipeline takes under                                                     based testing. Future work includes structured architectural
5 seconds per heuristic and catches safety violations that reward                                               mutations to counteract mode collapse, persistent cross-run
alone cannot detect (§4.8).                                                                                     memory to mitigate conversation amnesia, extending the Z3 ver-
                                                                                                                ifier to cover array-dependent specifications currently deferred
                                                                                                                to property testing, and integrating the audit as an in-loop filter
6                           Related Work                                                                        that rejects unsafe candidates before evaluation. We validated
LLM-driven heuristic and code generation.                   Fun-                                                Luby-style universal restarts [Luby et al., 1993] as a principled
Search [Romera-Paredes et al., 2024] uses LLMs with an                                                          restart strategy (§4.4): a single 160-iteration Luby campaign
evolutionary algorithm to discover mathematical functions at a                                                  approaches the hindsight-optimal budget allocation derived
scale of ∼1M evaluations. Evolution of Heuristics (EoH) [Liu                                                    from 52 ad-hoc runs totalling 730 iterations, achieving near-
et al., 2024] maintains (thought, code) pairs and uses the LLM                                                  top-decile performance without prior data or manual tuning.
as a crossover/mutation operator. ReEvo [Ye et al., 2024]                                                       Extending this to adaptive schedules that adjust the unit size
adds a reflective mechanism with separate generator and critic                                                  online based on observed convergence rates is a promising
LLM roles. Concurrent work by Guo et al. [2026] demon-                                                          direction. Code and data are available at Siboni [2026].


                                                                                                            8
References                                                          A     Domain Specification Catalog
B. Romera-Paredes, M. Barekatain, A. Novikov, et al. Mathe- Table 5 lists all 11 domain specifications verified by the audit
   matical discoveries from program search with large language pipeline. Each specification encodes a physical requirement of
   models. Nature, 625:468–475, 2024.                             the hot rolling process as a formal property that can be checked
                                                                  automatically. Specifications are grouped into four categories
F. Liu, C. Xialiang, Z. Zhuangdi, et al. Evolution of heuristics:
                                                                  reflecting different aspects of controller correctness.
   Towards efficient automatic algorithm design using large
   language model. In Proc. ICML, 2024.                              Safety specifications (SPEC-001–003) are rated error sever-
                                                                  ity: violation means the controller could damage equipment or
H. Ye, J. Wang, Z. Cao, F. Song, and G. Chen. ReEvo: Large produce out-of-spec steel. No-overshoot (SPEC-001) ensures
   language models as hyper-heuristics with reflective evolution. the height reduction never thins the slab below the target gauge—
   In Proc. NeurIPS, 2024.                                        a fundamental constraint in rolling, since under-thick slabs
                                                                  cannot be corrected. HR-limit respect (SPEC-002) prevents
P. Guo, C. Li, Y. Feng, and C. Zhang. Code evolution for
                                                                  exceeding the mill’s per-pass reduction capacity.
   control: Synthesizing policies via LLM-driven evolutionary
   search. arXiv preprint arXiv:2601.06845, 2026.                    Monotonicity specifications (SPEC-004–006) encode ex-
                                                                  pected physical relationships. SPEC-004 requires that a thicker
Q. Hu, X. Tong, M. Yuan, F. Liu, Z. Lu, and Q. Zhang. slab (larger remaining reduction) triggers a proportionally
   Discovering interpretable programmatic policies via mul- larger height reduction—a controller that reduces less when
   timodal LLM-assisted evolutionary search. arXiv preprint the slab is further from target would be pathological. SPEC-
   arXiv:2508.05433, 2025.                                        005 requires longer interpass waiting times when grain size is
                                                                  below target, since grain growth during the interpass period
R. Dwivedula, D. Saxena, S. Yadalam, D. Kim, and A. Akella.
                                                                  is the primary mechanism for achieving target microstructure.
   Vulcan: Instance-optimal systems heuristics through LLM-
                                                                  SPEC-006 requires that higher rolling force produces lower
   driven search. arXiv preprint arXiv:2512.25065, 2025.
                                                                  velocity, protecting the mill from overload.
M. Weiner, C. Schmidtchen, and R. Kawalla. PyRoll — an open-         Responsiveness specifications (SPEC-007–009) verify that
   source rolling framework. In Proc. International Conference each output dimension actually responds to its relevant inputs.
   on the Technology of Plasticity, 2023.                         A controller that outputs a constant height reduction regardless
                                                                  of thickness (failing SPEC-007) would be degenerate. These
M. Towers, A. Kwiatkowski, J. Terry, et al. Gymnasium: A
                                                                  are existential properties: we check that there exist input
   standard interface for reinforcement learning environments.
                                                                  conditions producing different outputs.
   arXiv preprint arXiv:2407.17032, 2024.
                                                                     Consistency specifications (SPEC-010–011) verify deter-
Google DeepMind. Gemini 2.5: Pushing the frontier minism and continuity. SPEC-010 ensures no hidden stochastic-
   with advanced reasoning, multimodality, long context, ity (which would make the controller unpredictable). SPEC-011
   and next generation agentic capabilities. arXiv preprint checks that small input perturbations do not cause discontinu-
   arXiv:2507.06261, 2025.                                        ous output jumps—important for smooth mill operation.
C. A. H. Carreon, J. E. M. Tolama, G. C. Valdez, et al. Multi-
  objective optimization of the hot rolling scheduling of steel Table 5: Complete domain specification catalog. Sever-
  using a genetic algorithm. MRS Advances, 4:3373–3380, ity:            E = Error (safety-critical), W = Warning, I = Info.
  2019.                                                         Method:   Z3 = formally proved; H = property testing; 2T = two-
                                                                translation (heuristic AST translated twice with different sym-
C. Idzik, A. Kramer, G. Hirt, and J. Lohmar. Coupling of an bolic inputs).
  analytical rolling model and reinforcement learning to design
  pass schedules: towards properties controlled hot rolling. ID        Category     Property                      Sev. Meth.
  Journal of Intelligent Manufacturing, 35:1469–1490, 2024.
                                                                    001   Safety      HR ≤ thickness − target          E    Z3
W. Wang, M. Farrell, L. Cordeiro, and L. Zhao. Supporting           002   Safety      HR/10 ≤ hr_limit                 E    Z3
  software formal verification with large language models: An       003   Safety      HR ≥ 0                           E    Z3
  experimental study. In Proc. IEEE International Require-          004   Monoton.   Thicker ⇒ larger HR               W    2T
  ments Engineering Conference (RE), 2025.                          005   Monoton.   Smaller grain ⇒ longer wait       I    Z3
                                                                    006   Monoton.   Higher force ⇒ lower velocity     I    2T/H
M. Luby, A. Sinclair, and D. Zuckerman. Optimal speedup
 of Las Vegas algorithms. Information Processing Letters,           007   Respons.   HR varies with thickness          W    H
 47(4):173–180, 1993.                                               008   Respons.   Interpass varies with temp/-      W    H
                                                                                     grain
N. H. Siboni. PSO: LLM-driven heuristic synthesis for pro-          009   Respons.   Velocity varies with force/temp   I    H
  cess scheduling and optimisation. https://github.com/             010   Consist.    Deterministic output             E    H
  nima-siboni/pso, 2026.                                            011   Consist.    Continuous output                W    H


                                                                9
   The “Method” column shows the verification technique for ∈ [5, 110] and target_thickness ∈ [5, 15], the ex-
the best heuristic (reward 55.5). Z3 formally proves 5 spec- pression remaining_reduction = current_thickness
ifications: three safety properties (SPEC-001–003) and two - target_thickness yields the interval [−10, 105].
monotonicity properties (SPEC-004 via two-translation, SPEC-
005). SPEC-006 (velocity decreases with force) yields a Z3 Table 7: Input value ranges for interval analysis and Z3 con-
counterexample at a degenerate boundary (force near zero), straints.
though property-based testing confirms the property holds
across realistic operating ranges. The remaining 4 specs, in-         Variable           Min        Max Unit
volving responsiveness or epsilon-delta continuity reasoning,         current_thickness   5.0      110.0 mm
are deferred to property-based testing.                               target_thickness    5.0       15.0 mm
                                                                                hr_limit              20.0       50.0   mm
B     Verification Methodology Details                                          stock_temperature     800       1523    K
                                                                                target_temperature   1073       1273    K
B.1    AST-Based Static Analysis (Layer 1)                                      current_grain_size       5       500    𝜇m
                                                                                target_grain_size        5        25    𝜇m
The first audit layer performs 29 static checks organized into                  rolling_force        −100      4×106    N
8 categories, executed via AST visitors without running the                     rolling_torque       −100    1.3×105    N·m
heuristic. Table 6 summarizes the categories.                                   step_count               0         25   —

Table 6: AST-based check categories. Each category targets a         Interval arithmetic handles all standard operations: addition
specific failure mode of LLM-generated code.                      (intervals add), subtraction (lo subtracts hi), multiplication
                                                                  (product of all endpoint pairs), and division (with explicit zero-
Category                  Chk What it catches                     crossing detection). The evaluator also handles np.clip, min,
Structural integrity        4 Wrong signature, missing re- max, int(), round(), and if/else branching (union of branch
                               turns, global state, class defini- intervals). The output is three interval checks (RNG-001–003)
                               tions                              verifying that the HR, interpass, and velocity outputs remain
Security / sandbox          6 Imports, exec/eval, file I/O, dun- within their action bounds for all possible input combinations.
                                  der access, forbidden modules
Action mask compliance       3    Mask not referenced, not             B.3    Z3 Formal Verification (Layer 4)
                                  checked, no fallback
                                                                       The Z3 verification layer translates the heuristic’s Python AST
Bounds & clipping            3    Outputs      outside    [0, 500],
                                                                       into Z3 SMT constraints and proves that domain specifications
                                  [1, 120], [1, 6]
Division safety              2    Unguarded divisions, NaN/Inf         hold for all valid inputs—not just sampled ones.
                                  risk
Info dict usage              4    Missing critical keys, force un-     AST-to-Z3               translation. The              translator
                                  awareness                            (HeuristicZ3Translator) creates a symbolic Z3 variable
Return path complete.        3    Dead paths, wrong length, no         for each of the 10 input keys (Table 7), with domain constraints
                                  fallback                             bounding their ranges. It then walks the heuristic’s function
Control logic quality        4    Ignores thickness, constant out-     body, translating each Python construct:
                                  puts                                 • Arithmetic: +, −, ×, ÷, floor division, power → Z3 arith-
                                                                          metic
   Security checks deserve special attention because LLMs              • Comparisons: <, ≤, >, ≥, =, ≠ → Z3 boolean expressions
occasionally generate code that stores mutable state on the func-      • Control flow: if/else → Z3 If(cond, then, else)
tion object (e.g., heuristic.prev_hr = val) or accesses                   with branch merging
dunder attributes. The audit flags these via SEC-006 (allowed          • Calls: np.clip(x,lo,hi) → If(x<lo, lo, If(x>hi,
modules check), which requires all attribute-set targets to be            hi, x)); similarly for max, min, abs, int, round,
whitelisted. In the best ad-hoc run (Figure 7), all 18 itera-             math.ceil/floor
tions pass security checks—no mutable state or dunder access           • Dict access: info[’key’] → corresponding Z3 variable
patterns were observed. Other runs in our 52-run corpus do             Constructs that cannot be translated—notably numpy array op-
exhibit these patterns, confirming the check’s value.                  erations such as np.where, np.argmin, and array indexing—
                                                                       cause a Z3TranslationError. The translator handles this
B.2    Interval Analysis (Layer 2)                                     gracefully: failed assignments are excluded from the envi-
The interval analysis layer propagates input value ranges              ronment, and if a return value references an untranslatable
through the heuristic’s arithmetic to verify output bounds stat-       variable, that output dimension is marked as None and the spec
ically—without executing the code. Starting from known                 is deferred to property-based testing.
input ranges (Table 7), the evaluator walks the AST and
computes a closed interval [lo, hi] for every intermedi- Contiguous mask decomposition. The action mask for
ate variable. For example, given current_thickness height reduction is a 501-element binary array where mask[𝑖] =


                                                                      10
1 iff 𝑖/10 ≤ min(hr_limit, 0.7 × thickness, thickness − 5. Force sentinel: force = −100 N (pre-first-pass sentinel
target). Because this mask is contiguous (all 1s up to some       value from environment)
index, then all 0s), it can be decomposed to a single scalar 6. Equal grain sizes: current = target (tests zero-error han-
max_valid_idx. This avoids reasoning about arrays entirely        dling)
and enables Z3 to prove safety properties (SPEC-001–003) by 7. Equal temperatures: stock = target (tests zero-error han-
showing that any action within the mask satisfies the constraint. dling)

Two-translation technique. Monotonicity and relational                Random inputs. The 200 random inputs are sampled uni-
specifications require comparing the heuristic’s output under         formly from the ranges in Table 7, with the constraint that
two different input conditions. The verifier creates two inde-        current_thickness ≥ target_thickness. For each in-
pendent translator instances with prefixed variable names (e.g.,      put, a consistent action mask is generated from the physical
a_current_thickness, b_current_thickness), trans-                     constraints (HR limit, 70% thickness rule, minimum gauge).
lates the heuristic AST twice, and builds a property comparing
the two outputs:                                                      Per-input checks. Each test input runs 6 basic checks (PBT-
1. Create translators 𝑇𝑎 (prefix a_) and 𝑇𝑏 (prefix b_).              001–006): no exceptions, correct return type, HR/interpass/ve-
2. Translate the function body with each, extracting return           locity within bounds, and mask compliance (the selected HR
    expressions.                                                      action must not be masked out). Additionally, all domain
3. Equalize all shared inputs: ∀𝑘 ≠ 𝑘 vary : 𝑎 𝑘 = 𝑏 𝑘 .              specs deferred from Z3 are verified by calling the spec’s check
4. Add ordering constraint on the varied input: 𝑎 𝑘vary > 𝑏 𝑘vary .   function with the test input.
5. Prove the output relationship: e.g., out𝑎 ≥ out𝑏 for in-
    creasing monotonicity.                                            Z3-to-Hypothesis deferral. The Z3 layer produces a list of
Z3 then checks whether the negation of this property is satisfi-      deferred spec IDs that it could not verify. These are passed to
able. If unsatisfiable (UNSAT), the property is proved for all        the property testing layer, which verifies them via execution.
valid inputs. If satisfiable (SAT), Z3 provides a concrete coun-      The deferral is transparent in the audit report: each deferred
terexample. For SPEC-006 (velocity decreases with force), this        spec appears in both the Z3 section (marked “deferred to
technique proves the property in under 0.1s. For SPEC-004             Hypothesis”) and the property testing section (marked “deferred
(HR monotonicity), the technique succeeds on simpler heuris-          from Z3”), ensuring complete traceability.
tics but falls back to Hypothesis when the HR computation
uses np.argmin—an untranslatable construct.

If/else branch merging. A subtle correctness issue arises
when one branch of an if/else translates successfully but the
other does not (e.g., the if remaining_reduction < 0.1:
hr_action = 0 branch succeeds, but the else branch fails
because it uses np.argmin). Naïvely using the one-sided
value would produce a false proof. The translator handles this
by tracking which variables existed before the branch point:
variables introduced in only one branch (due to translation
failure in the other) are excluded from the merged environment,
correctly marking that output as untranslatable.

B.4    Property-Based Testing (Layer 5)
The final layer executes the heuristic with actual numpy opera-
tions on 207 test inputs (200 random + 7 deterministic edge
cases) and verifies all specs that Z3 could not handle.

Edge cases. Seven edge cases encode domain expertise about
which operating conditions are most likely to trigger failures:
1. Near target: thickness = 10.1 mm, target = 10.0 mm (tests
   minimal-reduction logic)
2. Maximum state: all inputs at upper bounds (tests saturation
   behavior)
3. Minimum state: all inputs at lower bounds (tests boundary
   handling)
4. Tight mask: remaining reduction = 0.5 mm (only a few
   valid HR actions)


                                                                  11
