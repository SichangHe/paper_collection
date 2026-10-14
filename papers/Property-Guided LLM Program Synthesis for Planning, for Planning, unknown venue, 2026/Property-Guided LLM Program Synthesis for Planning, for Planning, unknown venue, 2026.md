                                                      Property-Guided LLM Program Synthesis
                                                                   for Planning


                                                       André G. Pereira                       Augusto B. Corrêa             Jendrik Seipp
                                             Federal University of Rio Grande do Sul          University of Oxford       Linköping University
                                                              Brazil                           United Kingdom                  Sweden
arXiv:2605.16142v2 [cs.AI] 18 May 2026




                                                                                         Abstract
                                                     LLMs have shown impressive success in program synthesis, discovering programs
                                                     that surpass previously known solutions. However, these approaches rely on simple
                                                     numeric scores to signal program quality, such as the value of the solution or the
                                                     number of passed tests. Because such a score offers no guidance on why a program
                                                     failed, the system must generate and evaluate many candidates per problem in
                                                     the hope that some succeed, increasing both LLM inference and evaluation costs.
                                                     We study a different approach: property-guided LLM program synthesis. Instead
                                                     of scoring programs after evaluation, we check whether a candidate satisfies a
                                                     formally defined property. When the property is violated, we stop the evaluation
                                                     early and provide the LLM with a concrete counterexample showing exactly how
                                                     the program failed. This feedback drastically reduces both the number of program
                                                     generations and the evaluation cost, and can guide the LLM to generate stronger
                                                     programs. We evaluate this approach on PDDL planning domains, asking the LLM
                                                     to synthesize direct heuristic functions: every state reachable by strictly improving
                                                     transitions has a strictly improving successor. A heuristic with this property leads
                                                     hill-climbing algorithm directly to a goal state. A counterexample-guided repair
                                                     loop generates one candidate program, checks the property over a training set, and
                                                     returns the first case that violates the property. We evaluate our approach on ten
                                                     planning domains with an out-of-distribution test set. The synthesized heuristics
                                                     are effectively direct on virtually all test tasks, and compared to the best prior
                                                     generation method our approach generates seven times fewer programs per domain
                                                     on average, solves more tasks without using search, and requires several orders of
                                                     magnitude less computation to evaluate candidates. Whenever a problem admits a
                                                     verifiable property, property-guided LLM program synthesis can reduce synthesis
                                                     and evaluation cost while improving program quality.


                                         1    Introduction
                                         Using large language models (LLMs) for program synthesis yields programs that surpass previously
                                         known solutions on problems ranging from competitive programming [36] to open mathematical
                                         questions [50] and algorithmic discovery [42, 39, 62, 16, 12]. These approaches use simple numeric
                                         scores to rank candidate programs, such as the average value of the solution or the number of passed
                                         tests. Because such a score offers no guidance on why a program failed, the system must generate and
                                         evaluate many candidates per problem in the hope that some succeed, increasing both LLM inference
                                         cost and evaluation cost.
                                         There is an idea from formal methods that replaces this fitness score with something more informative:
                                         counterexample-guided inductive synthesis (CEGIS) [57, 35, 1]. A verifier checks each candidate
                                         against a formal specification, and on failure it returns a concrete input on which the candidate is
                                         wrong; the synthesizer can then repair or discard the candidate using that witness instead of a single
                                         number. CEGIS underpins much of classical program synthesis, yet it has seen little use with LLMs.

                                         Preprint.
         Initial Prompt                                                                  Validator
                                        LLM                Candidate Heuristic
           Domain &                                                                     Checks Direct
                                  Program Synthesis          (Python Code)
          Training Task                                                                   Property

                                   Repair                                                             Pass
                                                                                 ed)
                                                                             olat
                                                                         y Vi
                                  Counterexample                  Propert                 Verified
                                                                 (
                                      Prompt                Fail                           Direct
                                    Failing State                                         Heuristic
                                   and Successors

Figure 1: Counterexample-driven repair loop for property-guided heuristic function synthesis. Given
a planning domain and a task from the training set, the LLM proposes a candidate heuristic function
in Python. The validator evaluates this heuristic on the training set, verifying the direct property. If
the property is satisfied, the valid heuristic is output. If the property is violated, evaluation stops early,
and a concrete counterexample is returned.



We use an LLM as the synthesizer in a CEGIS-style loop with a property checker as the verifier. On
every failed candidate, we hand the LLM a concrete counterexample of where and how the program
went wrong, which lets us stop evaluation as soon as the property is violated. This reduces the number
of candidates the LLM has to generate and steers it toward stronger programs.
We evaluate this idea on classical planning [26], a problem known to be challenging for LLMs [64,
63, 59]. Given a planning domain, we ask the LLM to synthesize a heuristic function as Python
code, which is then automatically injected into a planner. Ideally, such a heuristic would guide
hill climbing from the initial state to a goal without ever getting stuck, solving tasks without any
combinatorial search. To capture this requirement formally, we target the direct property [19]: a
heuristic is direct if every state reachable from the initial state via strictly improving transitions has a
strictly improving successor. This property is a natural fit for property-guided synthesis, since any
violation immediately yields a concrete counterexample. Synthesizing a direct heuristic is challenging
both in theory [32, 19] and in practice [e.g., 24]: it requires reasoning about every state on every
strictly improving path, and a single state without an improving successor is enough to break the
property. In fact, synthesizing a direct heuristic for a given task is as hard as solving the task itself.
Our counterexample-driven repair loop takes a PDDL (Planning Domain Definition Language)
domain together with a training set of PDDL tasks from this domain as input, and validates the direct
property over the training set. Validation terminates as soon as a counterexample is found. In this
case, we prompt the LLM with the failing task and the counterexample: the state where the property
fails, its heuristic value, and the successor states with their heuristic values. The LLM is asked to
provide a new heuristic that is direct for this task. This loop repeats until the heuristic passes the
full training set. Although validation is confined to the training tasks, we aim for the synthesized
heuristic to generalize, remaining direct on the much harder, out-of-distribution test tasks. Figure 1
illustrates this process. To our knowledge, our work is the first to use LLMs to synthesize heuristics
via property-guided repair.
On the ten planning domains from the Learning Track of the International Planning Competition
(IPC) 2023 [60], evaluated on an out-of-distribution test set, our approach generates seven times
fewer programs per domain on average compared to the best prior generation method [16], requires
significantly less computation to evaluate candidates, and solves more tasks via hill climbing without
any combinatorial search. Our repair loop always finds a heuristic that is direct on every training
task within the iteration budget, and the synthesized heuristics remain direct on virtually all out-of-
distribution test tasks, confirming that the property generalizes beyond the training set.


2   Background

Classical planning asks for a sequence of deterministic actions, a plan, that transforms a given
initial state into a state satisfying a goal in a fully-observable, discrete environment with a single
agent. Planning tasks are commonly described in the Planning Domain Definition Language (PDDL)
[40, 30], and our work directly uses this representation.


                                                      2
   h=3           a            s0                                  h=3      c        a        s0

   h=2           c                          b                     h=2                                      b

   h=1                                     d                      h=1                                      d

   h=0                        g                                   h=0                        g

(a) Descending heuristic: every alive state has at least       (b) Direct heuristic: the same state space with a differ-
one strictly improving successor, including state a            ent heuristic admits a strictly improving path (s0 →
which will never be expanded by GBFS or HC.                    b → d → g), but state a is a plateau (h(a) = h(s0 )).
Figure 2: Example descending and direct heuristics for the same state space. Nodes are placed on
horizontal heuristic layers; downward transitions strictly decrease the heuristic value h. State s0 is the
initial state and g is the goal state. Both heuristics are dead-end avoiding since all states are solvable.
The left heuristic is descending and thus also direct; the right heuristic is direct but not descending.


A PDDL task is defined by a set of objects and predicates. Together they form ground atoms,
i.e., predicates instantiated with concrete objects, which describe the current state. Actions have
preconditions that must hold for the action to be applicable, and effects that add or remove ground
atoms from the state. The task also specifies an initial state s0 and a goal. PDDL separates the domain
(shared actions and predicates) from the task (specific objects, initial state, and goal), typically stored
in two separate files.
We consider satisficing planning, where any plan is acceptable regardless of its length, and we
assume all actions have unit cost. Most satisficing planners are based on greedy best-first search
(GBFS) [47, 8, 33, 31, 49, 37], a state-space search algorithm guided by a heuristic function h that
maps each state s to a value h(s) ∈ R ∪ {∞} estimating the cost to reach a goal from s [46]. Infinite
values indicate that the goal is unreachable from s. GBFS starts from s0 and maintains a priority
queue of generated states ordered by their heuristic value. At each step, it expands the most promising
state s, i.e., the one with the smallest heuristic value h(s), generating its successors succ(s) and
adding them to the open list. This process continues until a goal state is reached. GBFS is complete:
if a solution exists, it will eventually find one, regardless of the heuristic, as long as all generated
states are eventually expanded
In contrast to the global nature of GBFS, hill climbing (HC) is a simple local-search algorithm:
starting from the initial state, it greedily moves to a successor with a strictly smaller heuristic value
and terminates when it reaches a goal state. Because HC keeps no open list, it is very memory
efficient. However, HC is incomplete: it can fail at plateaus (where no successor strictly improves
the heuristic) or local minima (where every successor has a larger heuristic value), even when the
goal is reachable. Completeness of HC therefore depends on the heuristic.
A descending and dead-end avoiding heuristic [54] eliminates both failure modes by construction.
Following Seipp et al. [54], we call a state alive if it is reachable, solvable, and not a goal.
Definition 1 (Descending and Dead-End Avoiding Heuristics [54, 32]). A heuristic h is descending
for a planning task Π if every alive state s has at least one successor s′ ∈ succ(s) with h(s′ ) < h(s),
and it is dead-end avoiding if every such improving successor is solvable.
Proposition 1 (Seipp et al. [54]). Let h be a descending, dead-end avoiding heuristic for a solvable
planning task Π. Then hill climbing guided by h reaches the goal from s0 .
The proof is straightforward: every reachable non-goal state has an improving successor, so heuristic
values strictly decrease at each step. Strict decrease prevents revisiting a state, and since the reachable
state space is finite, the search must reach a goal in finitely many steps.
The DDA property is, however, unnecessarily strong. It enforces that all alive states have improving
successors, even when these states would never be expanded by a planner. For example, the heuristic
h in Figure 2a is DDA because all alive states have improving successors. But this includes a, which is
never expanded by GBFS or HC using h, because h(b) < h(a), and b already has a strictly improving


                                                           3
path to the goal (i.e., h strictly decreases at every step). To address this issue, Dold and Helmert
[19] introduce a relaxation that only considers states reachable from s0 by repeatedly taking strictly
improving transitions. They call this property wet descending and dead-end avoiding (WDDA). For
brevity, we refer to a heuristic with this property as a direct heuristic throughout the rest of the paper.
Definition 2 (Direct Heuristic [19]). Let S↓ be the set of alive states reachable from s0 via strictly
improving transitions. A heuristic h is direct if every s ∈ S↓ has at least one successor s′ ∈ succ(s)
with h(s′ ) < h(s), and every such improving successor is either a goal state or itself in S↓ .
For instance, state a in Figure 2b is alive but has h(a) = h(s0 ), so a ∈
                                                                        / S↓ and the direct property
places no requirement on it, whereas DDA would still demand an improving successor. This seemingly
minor relaxation can make the property substantially easier to satisfy and to synthesize [19]. DDA
implies directness, but not the other way round. HC guided by a direct heuristic also reaches a goal
state without ever getting stuck.
Synthesizing a direct heuristic for a single PDDL task is also theoretically hard. A direct heuristic
exists for a task Π if and only if Π is solvable: any solvable task has a direct heuristic (e.g., the
perfect heuristic), and any direct heuristic guides hill climbing to a goal. Deciding whether a direct
heuristic exists is therefore equivalent to deciding plan existence, which is EXPSPACE-hard for
PDDL planning (a.k.a., “lifted planning”) [22, 14]. We sidestep this per-task cost by synthesizing a
single domain-general direct heuristic from a small training set, amortizing the synthesis effort over
the potentially infinite distribution of tasks in the domain.

3     Property-Guided LLM Heuristic Function Synthesis
We use an LLM to synthesize a domain-dependent heuristic function, implemented as Python code,
for a given PDDL domain. Our approach uses a single counterexample-driven repair loop: the LLM
generates one candidate, we validate it on a set of training tasks, and if it fails we return a concrete
counterexample to the LLM and ask for a new candidate. This loop repeats until the heuristic passes
the full training set or a generation budget is exhausted. The following subsections discuss the
property we target (Section 3.1), the prompts used in the repair loop (Section 3.2), and the validation
procedure (Section 3.3).

3.1   Targeting Direct Heuristics

The DDA property is a strict global requirement: it must hold at every alive state, and a single
violating state is enough to fail, even at states that hill climbing would never reach. We therefore
target heuristics with the direct property: every alive state reachable from s0 by strictly improving
transitions must have a strictly improving successor. A direct heuristic still guarantees that hill
climbing reaches a goal, but it focuses only on the subgraph that hill climbing can actually traverse.
Crucially for our method, every direct-property failure yields a concrete, local counterexample. The
first type of failure occurs at a state s on some strictly improving path from s0 whose successors s′ all
satisfy h(s′ ) ≥ h(s); the counterexample reports s, its heuristic value h(s), and the list of successors
together with their heuristic values. In domains with dead ends, a second type of failure can occur
when the DFS reaches a non-goal state s with no applicable action via a strictly improving transition
from a parent s′ ; the counterexample reports s, its heuristic value h(s), and the parent’s heuristic
value h(s′ ), together with the actionable suggestion that s should be assigned a value ≥ h(s′ ) so
that hill climbing never enters this dead end. This information is directly actionable and gives the
LLM precise feedback on how to improve the heuristic. Although validation is confined to the
training tasks, we aim for the synthesized heuristic to generalize and remain direct on the much
harder, out-of-distribution test tasks.

3.2   Counterexample-Driven Repair Loop

The repair loop maintains a history of all previously generated heuristics and their failure feedback.
It starts with an initial prompt that requests the first candidate and uses a repair prompt after each
validation failure.
Initial Prompt. We use the same prompt as Corrêa et al. [16] to make a direct comparison easier. It
provides the PDDL domain, the smallest and largest training PDDL tasks from this domain, heuristic


                                                    4
Python code examples for two domains disjoint from the evaluated domains, relevant planner code,
and a checklist. Note that the prompt does not instruct the LLM to generate a direct heuristic.
Repair Prompt. When a candidate fails validation on a training task, the repair prompt asks the
LLM to propose a heuristic that is direct on this task as well, and provides the definition of the direct
property. It also includes:

       1. the PDDL domain file;
       2. the PDDL task on which validation failed;
       3. the failure feedback: the failing state, its heuristic value, and the successor states with their
          heuristic values;
       4. all previously generated heuristic functions, together with their failure feedback;
       5. a checklist similar to the one in the initial prompt.

Items 2 and 3 give the LLM the exact nature of the failure. Item 4 lets the LLM reason about what has
already been tried and avoid repeating the same mistakes (see Appendix D for an example prompt).

3.3    Validation

To check whether a candidate heuristic h satisfies the direct property on a task Π, we run a depth-first
search (DFS) from s0 . At each expanded non-goal state s, we check whether it has at least one
successor s′ with h(s′ ) < h(s). If not, the direct property fails; we record s, its heuristic value, and
all its successor states with their heuristic values as the counterexample. Otherwise, the DFS pushes
onto the stack only the successors s′ with h(s′ ) < h(s).
We apply this check to each task in the training set. As soon as a failure is found, we return the
counterexample and stop, without checking the remaining tasks. We consider the heuristic a success
if all expanded states have a strictly improving successor across all training tasks.
Even modestly sized planning tasks can admit exponentially many strictly improving paths to a goal,
so validation cannot be expected to finish within a reasonable time on every task. We therefore
impose a per-task time limit during validation. If this limit is reached before a counterexample is
found, we treat the heuristic as direct on the task and continue with the next task.

4     Experimental Results
Experimental Setting. We run all experiments using Downward Lab [55] on AMD EPYC 7742
processors running at 2.25 GHz. We use Pyperplan [3] with PyPy 7.3.9 as our planning framework
for both training and testing. We generate all heuristics with Gemini 3.1 Pro [25], using default API
parameters. We use the ten domains together with their training and test tasks from the IPC 2023
Learning Track [60]; we summarise each domain in Appendix A.1 The test set contains 90 tasks per
domain (900 in total) and is out-of-distribution with respect to the training set: test tasks are generally
much larger and may differ structurally from training tasks. Figure 3 shows the range of the main
domain parameter on training and testing tasks. During training, each validation run is limited to
30 seconds and 8 GiB per task, and the repair loop runs for at most 10 iterations, i.e., 10 LLM calls.
During testing, each run is limited to 5 minutes and 8 GiB. For our methods, we report averages over
three runs. The source code, prompts, generated heuristics, and experimental data are included as
supplementary material; we will additionally release them publicly upon acceptance.
Scope. We evaluate whether property-guided synthesis reduces inference and evaluation cost while
improving heuristic quality; a single representative LLM suffices to answer this question. For a
comparison of different LLMs on heuristic generation for planning, see Corrêa et al. [16]. We study
the LLM as a program synthesizer: the LLM is called once per domain to generate a heuristic, which
is then used to solve all tasks in that domain, including unseen test tasks. In end-to-end planning, by
contrast, the LLM is invoked separately for each training and test task, incurring much higher costs
and losing all soundness guarantees on the resulting plans. For end-to-end planning performance
across LLM families, sizes, and reasoning models, see Corrêa et al. [16]; for frontier LLMs in this
    1 Two domains, Ferry and Satellite, use negative preconditions not supported by Pyperplan. We convert them to equivalent

domains via a transformation that eliminates negative preconditions.


                                                             5
                                               Training            Testing
                       29
    Blocks. 25                          488                    Rovers 11         4
                                                                                  30
                       10                                                        10
Childsnack 14                     292                         Satellite 12             99
       Ferry 12        20
                                                      974     Sokoban 11         4
                                                                                      79
                       30                                                        10
   Floortile 122                                      980     Spanner 11                              487
                       10                                                        7
   Miconic 11                           485                    Transp. 13            50

                   0        200   400   600   800 1,000                      0            200   400   600   800 1,000
                                              Main domain parameter
Figure 3: Size of training and test tasks measured by the main domain parameter. Each line spans the
range of values for the corresponding set; maximum endpoints are annotated with their numeric values.
The parameter counts blocks (Blocksworld), children (Childsnack), cars (Ferry), tiles (Floortile),
passengers (Miconic), rovers (Rovers), satellites (Satellite), boxes (Sokoban), spanners (Spanner),
and vehicles (Transport). The test set is out-of-distribution: in most domains the testing range extends
well beyond the training range, and test tasks may also differ structurally from training tasks.


setting, see Corrêa et al. [17]. For analyses regarding data contamination, obfuscated tasks and
evaluation on domains absent from LLM training data, see Corrêa et al. [16] and Chen et al. [12].
Baselines. The FF heuristic [33] is one of the most commonly used heuristics for satisficing
planning [e.g., 10, 15, 27]. It is a delete-relaxation heuristic computed in polynomial time by solving
a relaxed planning problem that ignores delete effects; it is not designed to be direct. Corrêa et al.
[16] introduce the current state-of-the-art method for LLM-based heuristic function generation for
planning: it uses an LLM to independently generate a fixed budget of 25 candidate heuristics per
domain and selects the one with the highest GBFS coverage on the training set and runs it with GBFS
on the test set; it is also not designed to be direct. We refer to this method as sample-and-select
throughout (abbreviated S&S in tables). We re-run this method with Gemini 3.1 Pro (the same model
used by our approach) to ensure a fair comparison.
Inference and Evaluation Costs of Candidate Heuristics. Our repair loop is much more efficient
than fixed-budget sample-and-select regarding the number of candidates the LLM must produce
and the time spent evaluating them. Across the ten IPC domains and three independent runs per
domain (30 runs in total), our method generates 101 candidate heuristics, on average 3.4 per run with
standard deviation 3.0. Eight of the ten domains converge (i.e., generate a heuristic that is direct on
the full training set) within at most 5 candidates per run, and four converge within 2 candidates on
average. Sokoban and Floortile are the clear outliers: Sokoban averages 9 candidates per run with a
maximum of 11 (initial attempt plus 10 repairs), and Floortile averages 8 with a maximum of 9. By
comparison, the sample-and-select baseline of Corrêa et al. [16] fixes a budget of 25 candidates per
domain regardless of difficulty, so the repair loop yields roughly a 7.4× reduction in inference cost
per run. Table 3 in Appendix C reports the per-domain breakdown.
Evaluation cost shrinks even more dramatically. In sample-and-select [16], each domain evaluates a
fixed pool of candidates with GBFS, so evaluation cost scales with the number of candidates. In our
repair loop, we validate one candidate at a time and stop at the first counterexample, which makes
failed candidates cheap to reject. The average evaluation time per domain is 10.75 minutes, while
Corrêa et al. [16] report 206.25 CPU-hours per domain. This corresponds to roughly a 1.15 × 103
reduction in evaluation cost.
Direct Heuristics vs. State of the Art. We compare the direct heuristics to the two baselines: the
FF heuristic [33] and the sample-and-select method by Corrêa et al. [16]. Both baselines use GBFS,
which may backtrack extensively before finding a solution. Our method uses HC, which follows a
single greedy path and reaches the goal without any search. Table 1 reports results for the baselines
under both GBFS and HC.
The main result is that our direct heuristics with HC solve 623.3 tasks by going directly to the goal,
while sample-and-select with GBFS solves 573 tasks, and FF with GBFS solves only 298. That is,
we solve more tasks than the best prior LLM method, and we do so without any search. Running the


                                                          6
Table 1: Per-domain coverage (number of solved tasks) on the 900 IPC 2023 test tasks. FF is the
classical delete-relaxation heuristic; S&S is our re-run of the sample-and-select baseline [16] with
Gemini 3.1 Pro. Both baselines are run using GBFS and HC. Direct is our proposed method (direct
heuristics run with HC). Cov. is the ablation that replaces the direct-property check with numeric
coverage feedback (see “Ablation” paragraph), run using GBFS and HC. All proposed and ablation
values are averages over three independent runs. Bold marks the best value per domain (ties are
co-bolded). The full table with standard deviations is in Appendix B (Table 2).
                                         Baselines                Ablation       Ours
                                                           FF                 S&S                      Cov.            Direct
                      Domain                          GBFS      HC    GBFS           HC         GBFS          HC            HC
                      Blocksworld (90)                     23    0            84         90          81.0     49.7          77.3
                      Childsnack (90)                      12    0            58         70          58.0     46.7          71.7
                      Ferry (90)                           45    0            67         71          64.7     49.3          72.3
                      Floortile (90)                       11    0            30          0          39.0     15.7          40.7
                      Miconic (90)                         61    1            83          7          82.0     34.0          90.0
                      Rovers (90)                          29    2            44         12          36.7     20.7          42.7
                      Satellite (90)                       35   17            57         60          56.0     57.3          55.7
                      Sokoban (90)                         29    1            30          0          26.0     12.7          30.0
                      Spanner (90)                         30    6            66         79          66.0     79.0          75.0
                      Transport (90)                       23    3            54         41          62.7     47.3          68.0
                      Total (900)                         298   30        573        430            572.7   412.3          623.3



                     Blocksworld      Rovers
                     Childsnack       Satellite
              105
                     Ferry            Sokoban
                     Floortile        Spanner
              104
Direct + HC




                     Miconic          Transport

              103

              102

              101


                    101     102      103      104   105         101     102        103        104             101    102    103     104   105
                                   FF + GBFS                      Sample-And-Select + GBFS                            Cov. + GBFS

Figure 4: State expansions of direct + HC versus each baseline, on test tasks solved by both methods.
Each point is one task, colored by domain. Points below the diagonal favor direct + HC. Note that
restricting to tasks solved by both methods, in general, favors the method that solves fewer tasks.


sample-and-select heuristics under HC solves only 430 tasks, confirming that the gain comes from
the property our repair loop trains for, not merely from the choice of search algorithm. FF under
HC collapses to 30 solved tasks. It is not a descending heuristic and offers no guarantee of progress
at every state, so HC fails at the first plateau or local minimum it encounters. Figures 4a and 4b
make the efficiency gap concrete: on tasks solved by both methods, our heuristics with HC expand
far fewer states than sample-and-select, sometimes by several orders of magnitude. Together with
the 7.4× reduction in inference cost and the 1.15 × 103 reduction in evaluation cost reported above,
these results show that property-guided synthesis is generally better than sample-and-select: it solves
more tasks, reaches the goal with fewer expansions, and costs far less to synthesize.

Generalization of the Direct Property. We validate the direct property only on small training
tasks, and there is no guarantee that a heuristic that passes this check will remain direct on the much
larger, out-of-distribution test tasks. At test time, hill climbing fails as soon as it reaches a state s with
no successor s′ satisfying h(s′ ) < h(s), which is exactly a violation of the direct property. Across
the three independent runs over all 900 test tasks (2,700 evaluations in total), only a single evaluation
stops for this reason (in Floortile). The remaining evaluations either find a plan or hit the time limit.
The synthesized heuristics are therefore effectively direct on the out-of-distribution test set as well.


                                                                         7
This is especially striking in Sokoban, a PSPACE-complete domain [18], where no test evaluation
across any of the three runs ever fails because of a property violation. The heuristics we generate
from small training tasks therefore generalize robustly to much harder test tasks.
Ablation. To isolate the contribution of the direct property, we run the same repair loop but replace
the property check with a numeric coverage score: the repair prompt reports which training task
the heuristic failed to solve within the time limit and how many states were expanded before timing
out, and asks for a new heuristic that solves more tasks with GBFS. We refer to this ablation as
Cov. Under GBFS, Cov. solves 572.7 (±15.95) tasks, roughly matching sample-and-select (573).
Under HC, however, Cov. degrades sharply to 412.3 tasks, well below our direct heuristics with HC
(623.3, ±6.7). Coverage feedback alone is therefore not sufficient to obtain heuristics that guide HC.
Figure 4c reinforces this point: on tasks solved by both methods, direct heuristics consistently require
fewer expansions.
Qualitative Analysis. Inspecting what the repair loop changes in the heuristic reveals why the
direct property is a useful synthesis target. Two domains illustrate the outcomes.
Blocksworld. Blocksworld has a single arm that rearranges blocks into goal stacks by picking up,
putting down, stacking, and unstacking one block at a time. The initial heuristic counts 2 actions
per misplaced block (one to pick it up, one to put it down), subtracts 1 if a block is currently held,
and adds 2 for each deadlock it detects. It uses two different deadlock conditions: for blocks on
the table, the penalty activates only when the target block is itself misplaced; for a held block, the
penalty activates whenever its target is not ready, meaning the target is either misplaced or covered
by another block. Consider the state where b1 is on b2 and b3 is on b4 , with the goal of swapping
them: b1 should go on b4 and b3 on b2 , while b2 and b4 are already correctly on the table. Both b1
and b3 are misplaced, giving h = 4. Since b2 and b4 are correctly on the table, the first condition
does not activate and no penalty is added. After unstacking b3 , the arm holds b3 and needs to place it
on b2 , but b1 still covers b2 , so b2 is not ready: the second condition activates and adds +2, giving
h = 2 × 2 − 1 + 2 = 5. The same happens when unstacking b1 . The inconsistency is that the
arm-empty state and the holding state use different conditions, so the mutual blocking between b1
and b3 is invisible in the arm-empty state but penalized in every successor, creating a local minimum.
The final heuristic fixes this by building a dependency graph among misplaced blocks. It adds an
edge from b3 to b1 (because b3 covers b4 , the target of b1 ) and from b1 to b3 (because b1 covers b2 ,
the target of b3 ), detects the cycle, and adds +2 in the arm-empty state itself, giving h = 6. The
successors then give h = 5, restoring descent. The final heuristic is effectively direct on all test tasks.
Satellite. Satellite requires a satellite to switch on an instrument, turn to one of its calibration targets,
calibrate it, and then point to the image direction before taking the image. The initial heuristic
estimates each missing image goal independently by adding costs for switching on an instrument,
calibrating it, turning to the needed directions, and taking the image. This gives an estimate of goal
distance, but it ignores the ordering constraints created by calibration and by the single power slot
on each satellite. An action may temporarily move the satellite away from the image goal direction,
and switching from one instrument to another can force recalibration. The final heuristic fixes this
by reasoning separately about each satellite’s remaining work as a short action sequence. For each
satellite, it groups the images that still need to be taken, considers which instrument should achieve
them, and counts the actions still needed to finish them in order: switching instruments, calibrating,
turning, and taking the images. It no longer treats the remaining requirements as an unordered set of
subgoals, but as a sequence whose order matters. Because of this, each improving move removes a
real remaining step in that sequence, which is why the final heuristic becomes direct.

5   Related Work
Counterexample-Guided Inductive Synthesis. Counterexample-guided inductive synthesis
(CEGIS) [57, 35, 1] alternates between a synthesizer that proposes candidate programs and a verifier
that checks them against a formal specification. When a candidate fails, the verifier returns a concrete
counterexample, and the synthesizer uses it to rule out or repair the candidate. Our work and that
of Orvalho et al. [43] are recent examples of CEGIS-style counterexample feedback applied to
LLM-based program synthesis.
LLM-Based Program Synthesis. Most LLM-based program synthesis evaluates candidates with
numeric scores such as test-pass rates or the value of the produced solutions, and uses these scores


                                                     8
to rank or select among many candidates [36, 39, 62, 12, 50, 42]. In general, these approaches can
combine multiple scores and use specific prompt strategies to guide the LLM toward better candidates,
but they do not provide concrete feedback on how to improve a candidate.

LLM-Based Heuristic Generation. Our closest precursor is Corrêa et al. [16], who sample a fixed
budget of heuristic candidates with an LLM and select the one that solves the most training tasks.
Other recent work that generates heuristics with LLMs includes Tuisov et al. [62], who focus on a
different planning formalism, and Chen et al. [12], who focus on generalized policies.

Descending Heuristics. The descending and dead-end avoiding (DDA) property was coined
by Seipp et al. [54]. Helmert et al. [32] showed that verifying or synthesizing DDA potential
heuristics [48] is PSPACE-complete for planning tasks encoded in propositional logic, with structural
relaxations dropping the complexity to lower levels of the polynomial hierarchy. Dold and Helmert
[19] introduce the direct (orig. “wet DDA”) variant, which only requires descent along states
reachable from s0 by strictly improving transitions. These properties are useful to estimate the
hardness of planning tasks based on the simplest form of their DDA/direct heuristics [54, 19].

Learning Search Control. Francès et al. [24] synthesize generalized potential heuristics as
weighted sums over description-logic features [5] and prove DDA on the covered domains; their
approach is restricted to domains admitting a DDA heuristic representable in their specific feature
class and is therefore not directly comparable to ours. Several lines of work synthesize or learn search
control mechanisms for planning domains [9, 20, 21]. There is also a long history of approaches
that learn heuristics for planning [53, 13, 52, 4]. These include methods that learn for specific
tasks [23, 45, 6] and methods that learn for entire domains [56, 58, 11, 29].

LLMs for Planning. In addition, there is a large body of recent work that uses LLMs for planning in
several settings such as end-to-end plan generation [7, 59, 34], PDDL domain or task construction [61,
28, 44, 38], and generalized planning [51, 41].


6   Limitations

Our method depends on the existence of a property that can be efficiently checked and turned into
actionable feedback. In planning, the direct property provides exactly this. For problems where no
such informative property is available, or where the training set is too small to expose meaningful
counterexamples, the repair loop loses its main advantage and degenerates to score-based ranking.
A second limitation concerns the scope of verification. We check the direct property only on a small
training set under bounded resources, so passing this check does not certify that the heuristic is direct
on unseen tasks. Our experiments show that the property typically generalizes well to much larger
out-of-distribution tasks, but counterexamples on test tasks remain possible in principle.
A third limitation is that we synthesize unconstrained Python code. This flexibility is useful, but it
makes the resulting heuristics harder to interpret and verify than structured representations such as
fixed feature sets or linear potentials. A promising direction for future work is to combine our repair
loop with strategies that automatically prove the synthesized heuristic to be direct on an entire domain,
as has been done in restricted settings [2], possibly using theorem provers powered by LLMs.


7   Conclusions

In this paper, we studied property-guided LLM program synthesis for planning and showed that a
counterexample-driven repair loop can synthesize direct heuristic functions efficiently. Across the ten
IPC 2023 Learning Track domains, and compared to the previous best heuristic generation method, our
method requires about 7.4× fewer LLM calls for heuristic generation, reduces candidate evaluation
cost by roughly 1.15 × 103 , and solves more out-of-distribution test tasks by hill climbing directly
to the goal. The direct property is effective both as a synthesis target and as a feedback mechanism:
when violated, it provides concrete counterexamples that guide repair, and when satisfied on the
training tasks, it often generalizes to much larger unseen tasks. More broadly, our results suggest
that whenever a synthesis problem admits a checkable property with actionable counterexamples,
property-guided LLM repair can be a practical alternative to score-based candidate ranking.


                                                   9
Acknowledgments
This work was supported by the Wallenberg AI, Autonomous Systems and Software Program (WASP)
funded by the Knut and Alice Wallenberg Foundation. André G. Pereira acknowledges support
from FAPERGS with projects 21/2551-0000741-9 and 25/2551-0002590-7. This study was financed
in part by the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior – Brasil (CAPES) –
Finance Code 001.

References
 [1] Alessandro Abate, Cristina David, Pascal Kesseli, Daniel Kroening, and Elizabeth Polgreen.
     Counterexample guided inductive synthesis modulo theories. In International Conference
     Computer Aided Verification, 2018.
 [2] Mohammad Abdulaziz, Florian Pommerening, and Augusto B. Corrêa. Mechanically proving
     guarantees of generalized heuristics: First results and ongoing work. In ICAPS Workshop on
     Heuristics and Search for Domain-independent Planning, 2022.
 [3] Yusra Alkhazraji, Matthias Frorath, Markus Grützner, Malte Helmert, Thomas Liebetraut,
     Robert Mattmüller, Manuela Ortlieb, Jendrik Seipp, Tobias Springenberg, Philip Stahl, and Jan
     Wülfing. Pyperplan. https://doi.org/10.5281/zenodo.3700819, 2020.
 [4] Shahab J. Arfaee, Sandra Zilles, and Robert C. Holte. Learning heuristic functions for large
     state spaces. Artificial Intelligence, 175:2075–2098, 2011.
 [5] Franz Baader, Ian Horrocks, Carsten Lutz, and Uli Sattler, editors. An Introduction to Descrip-
     tion Logic. Cambridge University Press, 2017.
 [6] Rafael V Bettker, Pedro P Minini, André G Pereira, and Marcus Ritt. Understanding sample
     generation strategies for learning heuristic functions in classical planning. Journal of Artificial
     Intelligence Research, 80:243–271, 2024.
 [7] Bernd Bohnet, Azade Nova, Aaron T Parisi, Kevin Swersky, Katayoon Goshvadi, Hanjun Dai,
     Dale Schuurmans, Noah Fiedel, and Hanie Sedghi. Exploring and benchmarking the planning
     capabilities of large language models. arXiv:2406.13094 [cs.CL], 2024.
 [8] Blai Bonet and Héctor Geffner. Planning as heuristic search. Artificial Intelligence, 129(1):
     5–33, 2001.
 [9] Blai Bonet, Guillem Francès, and Héctor Geffner. Learning features and abstract actions for
     computing generalized plans. In Proc. AAAI 2019, pages 2703–2710, 2019.
[10] Clemens Büchner, Remo Christen, Augusto B. Corrêa, Salomé Eriksson, Patrick Ferber, Jendrik
     Seipp, and Silvan Sievers. Fast Downward Stone Soup 2023. In IPC-10 Planner Abstracts,
     2023.
[11] Dillon Z. Chen, Sylvie Thiébaux, and Felipe Trevizan. Learning domain-independent heuristics
     for grounded and lifted planning. In Proc. AAAI 2024, pages 20078–20086, 2024.
[12] Dillon Z. Chen, Johannes Zenn, Tristan Cinquin, and Sheila A. McIlraith. Language models for
     generalised pddl planning: Synthesising sound and programmatic policies. arXiv:2508.18507
     [cs.CL], 2025.
[13] Jens Christensen and Richard E Korf. A unified theory of heuristic evaluation functions and its
     application to learning. In Tom Kehler and Stanley J. Rosenschein, editors, Proc. AAAI 1986,
     pages 148–152, 1986.
[14] Augusto B. Corrêa and Giuseppe De Giacomo. Lifted planning: Recent advances in planning
     using first-order representations. In Proc. IJCAI 2024, pages 8010–8019, 2024.
[15] Augusto B. Corrêa, Guillem Francès, Markus Hecher, Davide Mario Longo, and Jendrik Seipp.
     Scorpion Maidu: Width search in the Scorpion planning system. In IPC-10 Planner Abstracts,
     2023.


                                                  10
[16] Augusto B. Corrêa, André Grahl Pereira, and Jendrik Seipp. Classical planning with LLM-
     generated heuristics: Challenging the state of the art with Python code. In Proc. NeurIPS 2025,
     2025.
[17] Augusto B. Corrêa, André G. Pereira, and Jendrik Seipp. The 2025 planning performance of
     frontier large language models. arXiv:2511.09378 [cs.CL], 2025.
[18] Joseph C. Culberson. Sokoban is PSPACE-complete. Technical Report TR 97-02, Department
     of Computing Science, The University of Alberta, Edmonton, Alberta, Canada, 1997.
[19] Simon Dold and Malte Helmert. Novelty vs. potential heuristics: A comparison of hardness
     measures for satisficing planning. In Proc. AAAI 2024, pages 20692–20699, 2024.
[20] Dominik Drexler, Jendrik Seipp, and Hector Geffner. Learning sketches for decomposing
     planning problems into subproblems of bounded width. In Proc. ICAPS 2022, pages 62–70,
     2022.
[21] Dominik Drexler, Jendrik Seipp, and Hector Geffner. Expressing and exploiting subgoal
     structure in classical planning using sketches. Journal of Artificial Intelligence Research, 80:
     171–208, 2024.
[22] Kutluhan Erol, Dana S. Nau, and V. S. Subrahmanian. Complexity, decidability and unde-
     cidability results for domain-independent planning. Artificial Intelligence, 76(1–2):75–88,
     1995.
[23] Patrick Ferber, Florian Geißer, Felipe Trevizan, Malte Helmert, and Jörg Hoffmann. Neural
     network heuristic functions for classical planning: Bootstrapping and comparison to other
     methods. In Proc. ICAPS 2022, pages 583–587, 2022.
[24] Guillem Francès, Augusto B. Corrêa, Cedric Geissmann, and Florian Pommerening. Generalized
     potential heuristics for classical planning. In Proc. IJCAI 2019, pages 5554–5561, 2019.
[25] Gemini Team Google. Gemini 3.1 Pro model card. Google DeepMind, 2026.
[26] Malik Ghallab, Dana Nau, and Paolo Traverso. Automated Planning: Theory and Practice.
     Morgan Kaufmann, 2004.

[27] Daniel Gnad, Álvaro Torralba, and Alexander Shleyfman. DecStar-2023. In IPC-10 Planner
     Abstracts, 2023.
[28] Lin Guan, Karthik Valmeekam, Sarath Sreedharan, and Subbarao Kambhampati. Leveraging
     pre-trained large language models to construct and utilize world models for model-based task
     planning. In Proc. NeurIPS 2023, pages 79081–79094, 2023.
[29] Mingyu Hao, Felipe Trevizan, Sylvie Thiébaux, Patrick Ferber, and Jörg Hoffmann. Guiding
     GBFS through learned pairwise rankings. In Proc. IJCAI 2024, pages 6724–6732, 2024.
[30] Patrik Haslum, Nir Lipovetzky, Daniele Magazzeni, and Christian Muise. An Introduction
     to the Planning Domain Definition Language, volume 13 of Synthesis Lectures on Artificial
     Intelligence and Machine Learning. Morgan & Claypool, 2019.
[31] Malte Helmert. The Fast Downward planning system. Journal of Artificial Intelligence Research,
     26:191–246, 2006.
[32] Malte Helmert, Silvan Sievers, Alexander Rovner, and Augusto B. Corrêa. On the complexity
     of heuristic synthesis for satisficing classical planning: Potential heuristics and beyond. In Proc.
     ICAPS 2022, pages 124–133, 2022.
[33] Jörg Hoffmann and Bernhard Nebel. The FF planning system: Fast plan generation through
     heuristic search. Journal of Artificial Intelligence Research, 14:253–302, 2001.
[34] Sukai Huang, Trevor Cohn, and Nir Lipovetzky. Chasing progress, not perfection: Revisiting
     strategies for end-to-end LLM plan generation. arXiv:2412.10675 [cs.CL], 2024.


                                                  11
[35] Susmit Jha, Sumit Gulwani, Sanjit A. Seshia, and Ashish Tiwari. Oracle-guided component-
     based program synthesis. In ACM/IEEE International Conference on Software, 2010.
[36] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond,
     Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy,
     Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl,
     Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson,
     Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. Competition-level
     code generation with AlphaCode. arXiv:2203.07814 [cs.PL], 2022.
[37] Nir Lipovetzky and Hector Geffner. Best-first width search: Exploration and exploitation in
     classical planning. In Proc. AAAI 2017, pages 3590–3596, 2017.
[38] Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Pe-
     ter Stone. LLM+P: Empowering large language models with optimal planning proficiency.
     arXiv:2304.11477 [cs.CL], 2023.
[39] Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and
     Qingfu Zhang. Evolution of heuristics: Towards efficient automatic algorithm design using
     large language model. In Proc. ICML 2024, 2024.
[40] Drew McDermott. The 1998 AI Planning Systems competition. AI Magazine, 21(2):35–55,
     2000.
[41] Andrew Murray, Danial Dervovic, Alberto Pozanco, and Michael Cashmore. GenePlan: Evolv-
     ing better generalized PDDL plans using large language models. In Proc. ICAPS 2026, 2026.
[42] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt
     Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian,
     M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies, Sebastian
     Nowozin, Pushmeet Kohli, and Matej Balog. Alphaevolve: A coding agent for scientific and
     algorithmic discovery. arXiv:2506.13131 [cs.CL], 2025.
[43] Pedro Orvalho, Mikolás Janota, and Vasco M. Manquinho. Counterexample guided program
     repair using zero-shot learning and maxsat-based fault localization. In AAAI Conference on
     Artificial Intelligence, 2025.
[44] James Oswald, Kavitha Srinivas, Harsha Kokel, Junkyu Lee, Michael Katz, and Shirin Sohrabi.
     Large language models as planning domain generators. In Proc. ICAPS 2024, pages 423–431,
     2024.
[45] Stefan O’Toole, Miquel Ramirez, Nir Lipovetzky, and Adrian R. Pearce. Sampling from pre-
     images to learn heuristic functions for classical planning (extended abstract). In Proc. SoCS
     2022, pages 308–310, 2022.
[46] Judea Pearl. Heuristics: Intelligent Search Strategies for Computer Problem Solving. Addison-
     Wesley, 1984.
[47] Ira Pohl. First results on the effect of error in heuristic search. In Bernard Meltzer and Donald
     Michie, editors, Machine Intelligence 5, pages 219–236. Edinburgh University Press, 1969.
[48] Florian Pommerening, Malte Helmert, Gabriele Röger, and Jendrik Seipp. From non-negative
     to general operator cost partitioning. In Proc. AAAI 2015, pages 3335–3341, 2015.
[49] Silvia Richter and Matthias Westphal. The LAMA planner: Guiding cost-based anytime
     planning with landmarks. Journal of Artificial Intelligence Research, 39:127–177, 2010.
[50] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang,
     Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from program
     search with large language models. Nature, 625(7995):468–475, 2024.
[51] Nicholas Rossetti, Massimiliano Tummolo, Alfonso Emilio Gerevini, Luca Putelli, Ivan Serina,
     Mattia Chiari, and Matteo Olivato. Learning general policies for planning through GPT models.
     In Proc. ICAPS 2024, pages 500–508, 2024.


                                                 12
[52] Mehdi Samadi, Ariel Felner, and Jonathan Schaeffer. Learning from multiple heuristics. In
     Proc. AAAI 2008, pages 357–362, 2008.
[53] Arthur L Samuel. Some studies in machine learning using the game of checkers. IBM Journal
     of research and development, 1959.
[54] Jendrik Seipp, Florian Pommerening, Gabriele Röger, and Malte Helmert. Correlation complex-
     ity of classical planning domains. In Proc. IJCAI 2016, pages 3242–3250, 2016.
[55] Jendrik Seipp, Florian Pommerening, Silvan Sievers, and Malte Helmert. Downward Lab.
     https://doi.org/10.5281/zenodo.790461, 2017.
[56] William Shen, Felipe Trevizan, and Sylvie Thiébaux. Learning domain-independent planning
     heuristics with hypergraph networks. In Proc. ICAPS 2020, pages 574–584, 2020.
[57] Armando Solar-Lezama, Rodric M. Rabbah, Rastislav Bodík, and Kemal Ebcioglu. Program-
     ming by sketching for bit-streaming programs. In Vivek Sarkar and Mary W. Hall, editors, ACM
     SIGPLAN 2005 Conference on Programming anguage Design and Implementation, 2005.
[58] Simon Ståhlberg, Blai Bonet, and Hector Geffner. Learning general optimal policies with graph
     neural networks: Expressive power, transparency, and limits. In Proc. ICAPS 2022, pages
     629–637, 2022.
[59] Kaya Stechly, Karthik Valmeekam, and Subbarao Kambhampati. Chain of thoughtlessness? an
     analysis of CoT in planning. In Proc. NeurIPS 2024, pages 29106–29141, 2024.
[60] Ayal Taitler, Ron Alford, Joan Espasa, Gregor Behnke, Daniel Fišer, Michael Gimelfarb, Florian
     Pommerening, Scott Sanner, Enrico Scala, Dominik Schreiber, Javier Segovia-Aguas, and
     Jendrik Seipp. The 2023 International Planning Competition. AI Magazine, 45(2):280–296,
     2024. doi: 10.1002/aaai.12169.
[61] Marcus Tantakoun, Christian Muise, and Xiaodan Zhu. LLMs as planning formalizers: A survey
     for leveraging large language models to construct automated planning models. In Findings of
     the Association for Computational Linguistics: ACL 2025, 2025.
[62] Alexander Tuisov, Yonatan Vernik, and Alexander Shleyfman. Successor-generator planning
     with LLM-generated heuristics. In Proc. ICAPS 2026, 2026.
[63] Karthik Valmeekam, Matthew Marquez, Alberto Olmo, Sarath Sreedharan, and Subbarao
     Kambhampati. PlanBench: An extensible benchmark for evaluating large language models on
     planning and reasoning about change. In Proc. NeurIPS 2023, pages 38975–38987, 2023.
[64] Karthik Valmeekam, Matthew Marquez, Sarath Sreedharan, and Subbarao Kambhampati. On
     the planning abilities of large language models - A critical investigation. In Proc. NeurIPS 2023,
     pages 75993–76005, 2023.




                                                  13
A    Benchmark Domains
We evaluate on the ten domains of the Learning Track of the IPC 2023 [60]. We give a brief
description of each domain below, based on the PDDL definitions distributed by the competition.
Blocksworld. A single arm rearranges distinguishable blocks into a goal configuration of stacks.
The arm holds at most one block at a time and supports four actions: pick a clear block up from the
table, put a held block down on the table, stack a held block onto another clear block, and unstack a
clear block from the block below it. Goals specify the desired stacking via on and on-table atoms.
Childsnack. An agent must prepare sandwiches in a kitchen and serve them to children seated at
tables. Each child is either gluten-allergic or not; gluten-free sandwiches require both gluten-free
bread and gluten-free content, both of which are scarce. Sandwiches are placed on trays that move
between the kitchen and the tables. The goal is to have every child served a sandwich compatible
with their allergy.
Ferry. A single ferry transports cars between locations on a sea. The ferry carries at most one car
at a time and alternates between sailing (empty or loaded), boarding, and disembarking. The goal
specifies the target location of each car.
Floortile. Robots paint tiles on a rectangular grid in two colors. Each robot can move onto an
adjacent unpainted tile, change the color it currently holds, or paint the tile immediately above or
below itself. A robot cannot step onto a painted tile, so the planner must reason about painting order
and about positioning robots so they do not block each other.
Miconic. A single elevator picks up passengers at their origin floors and delivers them to their
destination floors. The four actions are board, depart, drive up, and drive down; passenger capacity is
unbounded. The goal is to have every passenger served at their destination.
Rovers. A team of rovers performs scientific operations on a network of waypoints and communi-
cates results to a lander. Operations include sampling soil and rock at the current waypoint, calibrating
an on-board camera against a calibration target, taking images of objectives, and communicating data
via line of sight to the lander. Rovers differ in what they can traverse and which instruments they
carry, so plans must allocate tasks across heterogeneous agents.
Satellite. A fleet of satellites takes calibrated images of celestial directions in particular imaging
modes. Before an image can be acquired, the relevant instrument must be switched on, calibrated
against a calibration target, and the satellite must be pointing at the target direction. Each satellite has
a single power slot, so instruments must be switched on one at a time.
Sokoban. An agent on a grid pushes boxes onto designated goal cells. The agent can move into a
clear adjacent cell or, if a box sits in the adjacent cell, push it one cell further in the same direction,
provided the destination cell is clear. Boxes cannot be pulled, so a box pushed against a wall or into a
corner in the wrong orientation creates an unrecoverable dead end.
Spanner. A man walks along a directed chain of locations to a workshop, where he must tighten
a number of loose nuts. Spanners are scattered along the way; each spanner can be used to tighten
exactly one nut and the chain cannot be retraversed. The man must therefore pick up enough usable
spanners before reaching the workshop.
Transport. Trucks with bounded discrete capacity move packages along a road network. Pick-up
and drop actions consume and free one unit of capacity, encoded as a chain of size objects related by
a predecessor predicate. The plan must coordinate truck routes and remaining capacity to deliver
every package to its goal location.

B    Full Coverage Results with Standard Deviations
Table 2 reports the same per-domain coverage numbers as Table 1 in the main text, but additionally
includes standard deviations across the three independent runs for the Cov. ablation (GBFS and HC)
and the Direct proposed method (HC). The baseline columns (FF and S&S under GBFS and HC) are
reproduced without standard deviations because they are deterministic.


                                                    14
Table 2: Per-domain coverage (number of solved tasks) on the 900 IPC 2023 test tasks. This is the
full version of Table 1 in the main text, including standard deviations across three independent runs
for the ablation and proposed method. FF is the classical delete-relaxation heuristic; S&S is our
re-run of the sample-and-select baseline [16] with Gemini 3.1 Pro. Both baselines are run using
GBFS and HC. Direct is our proposed method (direct heuristics run with HC). Cov. is the ablation
that replaces the direct-property check with numeric coverage feedback, using both GBFS and HC.
Bold marks the best value per domain (ties are co-bolded).
                                Baseline                      Ablation                Our Method
                           FF           S&S                        Cov.                    Direct
    Domain             GBFS HC GBFS HC                         GBFS                HC               HC
    Blocksworld (90)      23     0       84       90     81.00 ± 2.00      49.67 ± 3.79   77.3 ± 11.5
    Childsnack (90)       12     0       58       70     58.00 ± 0.00     46.67 ± 40.41    71.7 ± 0.6
    Ferry (90)            45     0       67       71     64.67 ± 4.04     49.33 ± 22.48    72.3 ± 1.2
    Floortile (90)        11     0       30        0    39.00 ± 11.36     15.67 ± 16.01    40.7 ± 9.0
    Miconic (90)          61     1       83        7     82.00 ± 8.00     34.00 ± 48.59    90.0 ± 0.0
    Rovers (90)           29     2       44       12     36.67 ± 5.69     20.67 ± 14.15   42.7 ± 13.6
    Satellite (90)        35    17       57       60     56.00 ± 1.73      57.33 ± 5.51   55.7 ± 14.5
    Sokoban (90)          29     1       30        0     26.67 ± 1.15      12.67 ± 6.43    30.0 ± 0.0
    Spanner (90)          30     6       66       79     66.00 ± 0.00      79.00 ± 0.00    75.0 ± 0.0
    Transport (90)        23     3       54       41     62.67 ± 4.04     47.33 ± 28.54    68.0 ± 0.0
    Total (900)          298    30      573 430 572.67 ± 15.95 412.33 ± 41.93             623.3 ± 6.7


C     Synthesis Statistics
Table 3 summarises how many candidate direct heuristics the repair loop generates before the property
check passes on the full training set. We report per-domain statistics over the three independent runs:
the minimum, mean (with standard deviation), and maximum number of candidates generated in a
single run, and the total over the three runs.

Table 3: Number of candidate direct heuristics generated by the repair loop per synthesis run,
summarised across the three independent runs per domain. n is the number of runs, and the Min,
Mean ± SD, and Max columns are computed over the per-run candidate counts.
                       Domain          n Min Mean ± SD Max
                          Blocksworld         3        1    2.33 ± 2.31        5
                          Childsnack          3        1    2.00 ± 1.00        3
                          Ferry               3        1    2.00 ± 1.00        3
                          Floortile           3        7    8.33 ± 1.15        9
                          Miconic             3        1    1.67 ± 0.58        2
                          Rovers              3        2    2.33 ± 0.58        3
                          Satellite           3        2    2.33 ± 0.58        3
                          Sokoban             3        5    9.00 ± 3.46       11
                          Spanner             3        1    1.33 ± 0.58        2
                          Transport           3        2    2.33 ± 0.58        3
                          Overall         30           1    3.37 ± 2.99       11



D     Example Repair Prompt
Below we show the repair prompt used in the repair loop, instantiated for the Blocksworld domain at
iteration 3. We edit the prompt to highlight its main structural components and match the nomenclature
used in the paper.
< role >



                                                       15
You are a highly - skilled AI planning researcher and a proficient Python programmer
      creating a domain - dependent heuristic function for the PDDL domain blocksworld .
</ role >

< objective >
Produce a revised heuristic where every non - goal state reachable by Depth - First Search ,
      which only expands strictly improving successors , has at least one improving
      successor , regardless of the order in which operators are applied .
</ objective >

< evaluation - method >
The heuristic is validated using a Depth - First Search ( DFS ) that enforces the direct
      property at every step :
- Only successors with h (s ’) < h ( s ) are added to the DFS stack .
- A property violation occurs when DFS expands a non - goal state and finds no successor
      with a strictly lower heuristic value .
...
</ evaluation - method >

< success - criteria >
1. Alive State : reachable from the initial state , solvable , and not a goal state .
2. Improving Successor : a successor s ’ such that h (s ’) < h ( s ) .
3. Direct : every alive state reachable from the initial state via a sequence of strictly
      decreasing h values has at least one improving successor . All states that DFS can
      reach must contain an improving successor .
4. Dead - End Avoiding : no improving successor of an alive state reachable by DFS is itself
       unsolvable ( h = infinity ) .
</ success - criteria >

< previous - iterations >
Iteration 0:
- Prompt Type : Init
- Solved 5 instances ( Average expanded nodes : 2.4)
- Direct validated on 5 tasks ( last index : 4)
- Failure Analysis :
   Failure Type : property
   Failing Task : p06 . pddl
   Property Failure Kind : direct
   State : [ ’( clear b1 ) ’, ’( clear b2 ) ’, ’( holding b3 ) ’, ’( on - table b1 ) ’, ’( on - table b2 ) ’]
   Heuristic Value : 3
   Reason : State has h =3 but no successor has h < 3.
   Successors :
     1. action =( stack b3 b2 ) , h =6 , added =[ ’( clear b3 ) ’, ’( on b3 b2 ) ’, ’( arm - empty ) ’] ,
           deleted =[ ’( holding b3 ) ’, ’( clear b2 ) ’]
     2. action =( stack b3 b1 ) , h =6 , added =[ ’( clear b3 ) ’, ’( on b3 b1 ) ’, ’( arm - empty ) ’] ,
           deleted =[ ’( holding b3 ) ’, ’( clear b1 ) ’]
     3. action =( putdown b3 ) , h =4 , added =[ ’( clear b3 ) ’, ’( on - table b3 ) ’, ’( arm - empty ) ’] ,
           deleted =[ ’( holding b3 ) ’]
< previous - heuristic - code >
...
</ previous - heuristic - code >

Iteration 1:
- Prompt Type : Property
- Main Idea : ...
- Solved 16 instances ( Average expanded nodes : 7.0)
- Direct validated on 16 tasks ( last index : 15)
- Failure Analysis :
   Failure Type : property
   Failing Task : p17 . pddl
   Property Failure Kind : direct
   State : [ ’( arm - empty ) ’, ’( clear b1 ) ’, ’( clear b3 ) ’, ’( clear b4 ) ’, ’( on b2 b5 ) ’, ’( on b3
        b2 ) ’, ’( on - table b1 ) ’, ’( on - table b4 ) ’, ’( on - table b5 ) ’]
   Heuristic Value : 10
   Reason : State has h =10 but no successor has h < 10.
   Successors :
     1. action =( unstack b3 b2 ) , h =11 , added =[ ’( holding b3 ) ’, ’( clear b2 ) ’] , deleted =[ ’(
           clear b3 ) ’, ’( on b3 b2 ) ’, ’( arm - empty ) ’]
     2. action =( pickup b4 ) , h =11 , added =[ ’( holding b4 ) ’] , deleted =[ ’( on - table b4 ) ’, ’(
           clear b4 ) ’, ’( arm - empty ) ’]
     3. action =( pickup b1 ) , h =11 , added =[ ’( holding b1 ) ’] , deleted =[ ’( clear b1 ) ’, ’( on -
           table b1 ) ’, ’( arm - empty ) ’]
< previous - heuristic - code >
...
</ previous - heuristic - code >

Iteration 2:
- Prompt Type : Property
- Main Idea : ...
- Solved 17 instances ( Average expanded nodes : 7.8)
- Direct validated on 17 tasks ( last index : 16)



                                                      16
- Failure Analysis :
   Failure Type : property
   Failing Task : p18 . pddl
   Property Failure Kind : direct
   State : [ ’( arm - empty ) ’, ’( clear b1 ) ’, ’( clear b3 ) ’, ’( clear b5 ) ’, ’( on b2 b4 ) ’, ’( on b5
        b2 ) ’, ’( on - table b1 ) ’, ’( on - table b3 ) ’, ’( on - table b4 ) ’]
   Heuristic Value : 8
   Reason : State has h =8 but no successor has h < 8.
   Successors :
     1. action =( unstack b5 b2 ) , h =9 , added =[ ’( holding b5 ) ’, ’( clear b2 ) ’] , deleted =[ ’( on
           b5 b2 ) ’, ’( clear b5 ) ’, ’( arm - empty ) ’]
     2. action =( pickup b1 ) , h =9 , added =[ ’( holding b1 ) ’] , deleted =[ ’( clear b1 ) ’, ’( on - table
             b1 ) ’, ’( arm - empty ) ’]
     3. action =( pickup b3 ) , h =9 , added =[ ’( holding b3 ) ’] , deleted =[ ’( clear b3 ) ’, ’( on - table
             b3 ) ’, ’( arm - empty ) ’]
< previous - heuristic - code >
...
</ previous - heuristic - code >
</ previous - iterations >

< current - status >
Domain Progress : solving 99 instances of increasing difficulty .
Validation Time Limit : 30 seconds per task .
Current Result : The heuristic was direct on 73 instances , but failed on p74 . pddl .
</ current - status >

< failure - analysis >
Failure Type : property
Property Failure Kind : direct
State : [ ’( arm - empty ) ’, ’( clear b10 ) ’, ’( clear b11 ) ’, ’( clear b15 ) ’, ’( clear b17 ) ’, ’(
      clear b2 ) ’, ’( clear b21 ) ’, ’( clear b22 ) ’, ’( clear b3 ) ’, ’( clear b4 ) ’, ’( clear b5 ) ’,
      ’( clear b6 ) ’, ’( clear b8 ) ’, ’( clear b9 ) ’, ’( on b1 b14 ) ’, ’( on b12 b18 ) ’, ’( on b14
      b13 ) ’, ’( on b15 b12 ) ’, ’( on b18 b7 ) ’, ’( on b21 b1 ) ’, ’( on b6 b20 ) ’, ’( on b7 b19 ) ’,
      ’( on b9 b16 ) ’, ’( on - table b10 ) ’, ’( on - table b11 ) ’, ’( on - table b13 ) ’, ’( on - table b16 )
      ’, ’( on - table b17 ) ’, ’( on - table b19 ) ’, ’( on - table b2 ) ’, ’( on - table b20 ) ’, ’( on - table
        b22 ) ’, ’( on - table b3 ) ’, ’( on - table b4 ) ’, ’( on - table b5 ) ’, ’( on - table b8 ) ’]
Heuristic Value : 38
Reason : State has h =38 but no successor has h < 38.
Successor Analysis :
1. action =( unstack b15 b12 ) , h =39 , added =[ ’( holding b15 ) ’, ’( clear b12 ) ’] , deleted =[ ’(
      clear b15 ) ’, ’( on b15 b12 ) ’, ’( arm - empty ) ’]
2. action =( unstack b9 b16 ) , h =39 , added =[ ’( holding b9 ) ’, ’( clear b16 ) ’] , deleted =[ ’( on b9
        b16 ) ’, ’( clear b9 ) ’, ’( arm - empty ) ’]
3. action =( pickup b11 ) , h =39 , added =[ ’( holding b11 ) ’] , deleted =[ ’( on - table b11 ) ’, ’( clear
        b11 ) ’, ’( arm - empty ) ’]
4. action =( pickup b8 ) , h =39 , added =[ ’( holding b8 ) ’] , deleted =[ ’( arm - empty ) ’, ’( clear b8 )
      ’, ’( on - table b8 ) ’]
5. action =( pickup b3 ) , h =39 , added =[ ’( holding b3 ) ’] , deleted =[ ’( clear b3 ) ’, ’( on - table b3
      ) ’, ’( arm - empty ) ’]
6. action =( pickup b4 ) , h =39 , added =[ ’( holding b4 ) ’] , deleted =[ ’( on - table b4 ) ’, ’( clear b4
      ) ’, ’( arm - empty ) ’]
7. action =( pickup b17 ) , h =39 , added =[ ’( holding b17 ) ’] , deleted =[ ’( clear b17 ) ’, ’( on - table
        b17 ) ’, ’( arm - empty ) ’]
8. action =( unstack b6 b20 ) , h =39 , added =[ ’( holding b6 ) ’, ’( clear b20 ) ’] , deleted =[ ’( clear
        b6 ) ’, ’( on b6 b20 ) ’, ’( arm - empty ) ’]
9. action =( pickup b10 ) , h =39 , added =[ ’( holding b10 ) ’] , deleted =[ ’( on - table b10 ) ’, ’( clear
        b10 ) ’, ’( arm - empty ) ’]
10. action =( pickup b22 ) , h =39 , added =[ ’( holding b22 ) ’] , deleted =[ ’( on - table b22 ) ’, ’(
      clear b22 ) ’, ’( arm - empty ) ’]
11. action =( pickup b5 ) , h =39 , added =[ ’( holding b5 ) ’] , deleted =[ ’( on - table b5 ) ’, ’( clear
      b5 ) ’, ’( arm - empty ) ’]
12. action =( unstack b21 b1 ) , h =39 , added =[ ’( clear b1 ) ’, ’( holding b21 ) ’] , deleted =[ ’(
      clear b21 ) ’, ’( on b21 b1 ) ’, ’( arm - empty ) ’]
13. action =( pickup b2 ) , h =39 , added =[ ’( holding b2 ) ’] , deleted =[ ’( clear b2 ) ’, ’( on - table
      b2 ) ’, ’( arm - empty ) ’]
</ failure - analysis >

This is the current Python code of the heuristic function :
< heuristic - code - file >
...
</ heuristic - code - file >

This is the PDDL domain file of the blocksworld domain :
< domain - file >
...
</ domain - file >

This is the first PDDL instance file of the blocksworld domain where the heuristic is
      failing the direct property :
< task - file >
...



                                                       17
</ task - file >

Here is a checklist to help you with your code :
< checklist >
   1) All used modules are imported .
   2) The information from static facts is extracted into suitable data structures in the
        constructor .
   3) Use the failure analysis and iteration history to preserve what worked and fix what
        failed .
   4) The name of the heuristic should be B l o c k s w o r l d H e u r i s t i c .
</ checklist >

< final - instruction >
   Return a new heuristic function code that satisfies the direct property in the instance
          in < task - file > as well .

   Output your answer in the following XML format :
   < generated - main - idea >
      A short paragraph describing only the idea of the new heuristic you are returning . Do
             not include any other information .
   </ generated - main - idea >
   < generated - heuristic - code >
      Provide the Python code of the domain - dependent heuristic for the blocksworld .
   </ generated - heuristic - code >
</ final - instruction >




                                            18
