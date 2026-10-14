                                             MerLean-Prover: A Recursive Looping Harness for Lean 4 Theorem Proving


                                                                                Jinzheng Li * 1 Zeru Zhu * 2 Yuanjie Ren * 3


                                                                   Abstract                                   Bench (Tsoukalas et al., 2024) is nearing closure, and
                                                                                                              Numina-Lean-Agent (Liu et al., 2026) and Axiom (Axiom
                                              M ER L EAN -P ROVER is an end-to-end Lean 4 the-                Math, 2025) have fully formalized Putnam 2025. PhD-
                                              orem prover that replaces sorry declarations                    qualifying-exam difficulty (Math, Inc., 2026a) remains an
arXiv:2605.26959v2 [cs.LO] 27 May 2026




                                              with kernel-checkable proofs. It is built from                  open challenge; at this scale, the central difficulty shifts
                                              three agent types (Planning, Check, and Lean)                   from individual proof attempts to long-horizon agent behav-
                                              composed by a recursive outer loop whose unit of                ior.
                                              revision is the proof plan itself, and uses no fine-
                                              tuning, no custom RL objective, and no theorem-                 Long proof attempts expose two well-documented LLM
                                              specific scaffolding. On F ORMAL Q UAL B ENCH,                  weaknesses at once. Context pressure: long-context recall
                                              a benchmark of 23 PhD-qualifying-exam theo-                     degrades non-monotonically with input length (Liu et al.,
                                              rems, M ER L EAN -P ROVER solves 10/23, surpass-                2024). Constraint pressure: instruction-following accuracy
                                              ing the strongest published open-source baseline                decays as simultaneous constraints accumulate (Jaroslawicz
                                              (OpenGauss, 8/23). On Putnam 2025, the same                     et al., 2025). A graduate-level proof attempt accumulates
                                              harness closes 12/12 with substantially lower                   dozens of dependencies and a long error history, while every
                                              total wall-clock than the next-best system that                 invocation must also preserve the original signature, avoid
                                              closes the full set. The harness also transfers to              axiom, stay tactical, and not weaken hypotheses. In the-
                                              smaller models: Sonnet closes all four tested F OR -            orem proving, errors have high downstream cost: a single
                                              MAL Q UAL B ENCH problems, and Haiku closes                     slip can change the target statement, admit an inadmissible
                                              the two short ones. These results suggest that                  axiom, or invalidate downstream proofs.
                                              harness design is a central factor in end-to-end                These weaknesses suggest a harness-level response: keep
                                              Lean 4 theorem proving, alongside raw model ca-                 global state outside the prompt, give each agent invocation
                                              pability, and that a relatively simple harness can              one focused task, and let the harness enforce global con-
                                              already be effective.                                           straints. The proof plan externalizes memory; each invoca-
                                                                                                              tion sees a local proof object and one local objective; recur-
                                                                                                              sion revisits the plan after failures without packing the entire
                                         1. Introduction                                                      proof history into one context. M ER L EAN -P ROVER instan-
                                                                                                              tiates this principle as an end-to-end harness that replaces
                                         Language-model agents can now compile Lean 4, parse er-
                                                                                                              sorry declarations in a Lean 4 file with kernel-checkable
                                         ror messages, and iterate (Polu & Sutskever, 2020; Han et al.,
                                                                                                              proofs of the same signatures, using three agent types com-
                                         2022; Yang et al., 2023). A growing family of agentic har-
                                                                                                              posed by a recursive outer loop (Section 2). We demonstrate
                                         nesses (including OpenGauss (Math, Inc., 2026b), Numina-
                                                                                                              this loop end-to-end on an example (Section 3). The empiri-
                                         Lean-Agent (Liu et al., 2026), Seed-Prover 1.5 (Chen et al.,
                                                                                                              cal claim of this paper is that this relatively simple architec-
                                         2025), Hilbert (Varambally et al., 2025), Ax-Prover (Breen
                                                                                                              ture can solve a substantial subset of graduate-level formal-
                                         et al., 2025), Archon (Ju et al., 2026), and unmodified
                                                                                                              ization problems without fine-tuning or theorem-specific
                                         general-purpose coding agents such as Claude Code, Codex,
                                                                                                              scaffolding.
                                         and opencode) has achieved strong performance across
                                         formal mathematics benchmarks. Earlier targets are now               In this work, M ER L EAN -P ROVER achieves 10/23 on F OR -
                                         largely closed: Seed-Prover 1.5 (Chen et al., 2025) re-              MAL Q UAL B ENCH , with nine solves within the matched
                                         portedly saturates MiniF2F (Zheng et al., 2022), Putnam-             4-hour budget and one in an extended 4h40m run, surpass-
                                             1
                                                                                                              ing the published open-source state of the art (OpenGauss,
                                               Northeastern University 2 Stony Brook University               8/23). On the Putnam 2025 slice, the same harness closes
                                         3
                                          Massachusetts Institute of Technology.   Correspondence
                                         to: Jinzheng Li <li.jinzh@northeastern.edu>, Zeru Zhu                12/12 and is the fastest system on 8 of 12 problems. We
                                         <zeru.zhu@stonybrook.edu>, Yuanjie Ren <yuanjie@mit.edu>.            additionally report a repeated-run stability study showing
                                                                                                              that closures are reproducible across attempts, and a Son-
                                         Preprint. May 28, 2026.

                                                                                                          1
                                                                   MerLean-Prover

                                                                                       any FAIL → replan


                                                                                                                                 3 | Check Agent


                                                          PASS : next si
                                                                                                                                  ¥ Faithfulness
                                                                                                            PASS : clean build   whether the clean-build
                                                                                                                                  Lean file still proves
                                                                                                                                     the original si

                 1                                                                         2
                                                                                               ∀ Lean Agent
   D Input            Planning Agent                    Proof Plan             pick si                                          Σ Math check
                                             edits                      ⋆                      edits Lean code for   sorrys
   .lean file         edits the proof plan           s1 → s2 → · · · → sN                                                            whether si is
                                                                                               one proof-plan node               mathematically correct
  with sorry                                             ⋆ target theorem
                                                                                                sorrys allowed

                                                                                                                                             PASS


                                                                   all si PASS                                 PASS : retry      ú Decomposition
                                                                                                                                  whether si should
                                                                                                                                       be split



                                                      c Prove finished

Figure 1. M ER L EAN -P ROVER’s recursive looping architecture. The shared proof plan is the unit of revision. The Lean Agent works on
one statement at a time; fresh Check Agent instances each answer one decision question. Math: whether si is mathematically correct;
Decomposition: whether si should be split; Faithfulness: whether the clean-build Lean file still proves the original si . A clean build
goes to Faithfulness before the loop advances to the next si ; if the Lean file has any sorry in it, the Lean file is checked by Math, then
Decomposition, before the Lean Agent resumes. Any FAIL invokes the Planning Agent for a replan, invalidating affected downstream
statements and restarting from the top of the revised plan. The success exit is available only when all plan statements pass and the target
theorem still matches the original Lean signature.


net/Haiku variant study showing that the harness still pro-                       conclusion—that the final proof must preserve. When a
duces kernel-audited proofs when run with smaller models                          node changes, the harness invalidates the downstream state-
(Section 4).                                                                      ments that depend on it, so later invocations see a consistent
                                                                                  local view of the revised plan.
2. Architecture
                                                                                 Three agent types. We use agent type to mean a role class
Figure 1 sketches the full pipeline. The system accepts a                        with a fixed authority boundary: the Planning Agent may
.lean file with one or more sorry declarations, gener-                           edit the proof plan, the Lean Agent may edit Lean code, and
ates a proof plan, and runs a recursive compile-and-revise                       the Check Agent is read-only and answers one true/false
loop until the target theorem is closed or an external stop                      question. Within each type, different task prompts define dif-
condition is reached. We describe this shared object first,                      ferent variants, but the authority boundary remains the same.
then the three single-objective agent roles, and finally the                     Every invocation is given exactly one objective with the
recursive loop. The key design choice is to keep global state                    minimum context it needs. This three-role decomposition
in the proof plan while giving each agent invocation one                         follows the harness-agent paradigm, where the harness co-
local task.                                                                      ordinates planning, code execution, and verification across
                                                                                 separate LLM calls (Ning et al., 2026).

Shared proof plan. The proof plan is the only global
                                                                                      • The Planning Agent proposes or edits the proof plan.
object shared across invocations. Conceptually, it is a topo-
                                                                                        It is invoked in four situations: initial plan construction
logically sorted list of proof statements: helper nodes ap-
                                                                                        from the input file, and three recovery cases triggered
pear before the statements that depend on them, and each
                                                                                        by the check agents: faithfulness failure, mathematical-
node contains an informal statement, a proof sketch, its
                                                                                        correction failure, and decomposition-driven replan-
dependencies, and its completion status. For the target
                                                                                        ning. Its output is either the initial plan or a proposed
theorem, the plan stores an anchor: the original Lean decla-
                                                                                        plan diff.
ration with its sorry body. This anchor records the exact
theorem signature—name, parameters, assumptions, and                                  • The Lean Agent writes Lean for one statement in

                                                                             2
                                                        MerLean-Prover

     the proof plan and then iteratively fixes it until lake          prompt set, and default model (claude-opus-4-7) are
     build passes or exhausts its compile budget. sorry               used on every problem. Initial planning, Lean writing and re-
     placeholders are allowed in its output—intermediate              pair, and the Math, Decomposition, and Faithfulness checks
     scaffolding is acceptable during this step, since any            are all delegated to standard calls to a general-purpose LLM
     surviving sorry is caught downstream by the harness              with single-objective prompts. This input format is an in-
     and handled by the Math check or the Decomposition               terface choice rather than a conceptual restriction: broader
     check. It reports either a build result or a compile-            inputs, such as a natural-language proof in LATEX, can be
     exhaustion signal.                                               handled by a preprocessing converter that produces the same
                                                                      Lean-with-sorry interface (Ren et al., 2026). Such con-
   • The Check Agent audits outputs produced by the other
                                                                      verters are separate from the recursive proof loop and are
     agents. Each invocation runs independently from the
                                                                      outside the present evaluation.
     producer session, sees the output rather than the pro-
     ducer’s chain-of-thought, and returns one true/false ver-
     dict. Its variants ask three decision questions: whether         3. Example Discussion
     a statement is mathematically correct as stated, whether
                                                                      Before turning to aggregate numbers, one worked example
     a stuck statement should be split into smaller sub-
                                                                      makes the recursive loop concrete. We use B URNSIDE -
     statements, and whether a clean-build Lean file still
                                                                      P RIME D EGREE T HEOREM because its trace exercises all
     proves the original statement.
                                                                      three recovery cases from Section 2: faithfulness failure,
                                                                      mathematical-correction failure, and decomposition-driven
No single prompt is asked to carry all global constraints at          replanning. The anchored target is the main theorem, and
once; instead, the harness enforces signature preservation,           node labels below match Figure 2, with the full node map
axiom-freedom, and faithfulness across the loop.                      in Section B.

Recursive loop. The outer loop repeatedly walks the proof
plan in dependency order and applies the Lean Agent to
each open statement. The Lean Agent’s build result and                BurnsidePrimeDegreeTheorem. The Planning Agent’s
the relevant Check Agent verdicts determine the next step:            initial plan contains 6 nodes: the anchored target (node #1)
close the statement, try the same statement again, or ask             and five prerequisites (nodes #2–#6). The Lean Agent then
the Planning Agent to revise the plan. The normal stopping            processes the prerequisites, closes four of them, and leaves
point is closure of the current plan, including the anchored          node #2. Node #2 reaches a clean lake build, but the
target; if the run reaches an external time limit before this         Faithfulness check rejects it as weakened at frame 6, a
point, the proof is not counted as solved. A clean build is           faithfulness failure. The Planning Agent revises the plan
sent to the Faithfulness check; if it passes, the loop advances       in response: it rewrites node #2’s statement to remove
to the next statement. When the Lean Agent cannot close               the weakening (a mathematical-correction step) and intro-
the current statement, the Math check first asks whether              duces node #7 as a new helper to carry the missing con-
the statement is mathematically correct as stated. If the             tent (decomposition-driven replanning). The Lean Agent
statement is sound, the Decomposition check asks whether              then works on node #7 until it exhausts its repair budget at
it should be split into smaller sub-statements. If the answer         frame 16, at which point the Decomposition check votes
is no, the Lean Agent retries the same statement; if the              for a split, and the Planning Agent replaces node #7 with
answer is yes, the Planning Agent turns the failure into a            smaller helpers, another instance of decomposition-driven
plan diff. Failed Math and Faithfulness checks also ask the           replanning. The same pattern recurs at nodes #8, #13, and
Planning Agent to revise the plan. When the diff is accepted,         #23. Mathematical-correction failure arises explicitly dur-
the harness invalidates affected downstream statements and            ing the node #13 replan: the Math check identifies that
restarts from the top of the updated plan.                            one of the helpers under node #13 has a signature miss-
                                                                      ing a required hypothesis (without it the lemma would be
A run is counted as solved only when every statement in               mathematically false), so the Planning Agent rewrites the
the current plan is closed, the target theorem still has the          statement before introducing further sub-helpers. Each re-
original Lean signature, and the final proof contains no              covery case becomes a plan revision; the plan grows from
forbidden sorry, admit, or user-introduced axiom. For                 6 to 12 nodes, then to 21, then to 32. By frame 51 the
benchmark reporting, an external goal audit checks this               node set has stabilized. The Lean Agent then closes the re-
condition; if it fails, we count the run as unfinished.               maining nodes bottom-up, and frame 63 closes the anchored
                                                                      target #1. The final goal check reports that the anchored dec-
Design scope. We did not fine-tune any model, introduce a             laration is present and that no sorry, admit, or axiom
custom RL objective, engineer theorem-specific prompts, or            remains in the proof closure. The closed Lean source for
include manually written proof sketches. The same harness,            nodes #1 and #2 is reproduced in Section C.

                                                                  3
                                                                                                   MerLean-Prover

  frame 0                                                    0/6 formalized   frame 6                                                           4/6 formalized       frame 20                                                      6/12 formalized
                                    1                                                                                  1                                                                                      1



                                                                                                                                                                                                              2



                                    2                                                                                  2                                                                                      7



                                                                                                                                                                                                              9



                  3                                      4                                         3                                        4                                                                 10



                                                                                                                                                                                          3                   4                    11



                  5                                      6                                         5                                        6                                             5              6         12              8



  frame 31                                               9/19 formalized      frame 51                                                 20/32 formalized              frame 63                                                 32/32 formalized
                                    1                                                                                  1                                                                                      1


                                                                                                                       2                                                                                      2
                                    2

                                                                                                                       7                                                                                      7

                                    7
                                                                                                                       8                                                                                      8


                                    9                                                                                  13                                                                                     13


                                                                                9                                                                               22     9                                                                                22
             10                                              8

                                                                                10                                     23                                       24     10                                     23                                        24

             3            4         11         14            13
                                                                                3         4                 11         14         25                 26         30     3         4                 11         14         25                  26         30


             5        6   12   15        16   17    18       19                 5    6   12   15       16    17   20   18   21   19    27       28    29   31   32     5    6   12   15       16    17   20   18   21   19    27        28    29   31   32




                                                                      ■ formalized                      ■ not yet                      ■ currently failing
Figure 2. Evolution of the dependency graph for B URNSIDE P RIME D EGREE T HEOREM (F ORMAL Q UAL B ENCH). Each panel is a snapshot
at one frame; each node represents a statement, and the node map appears in Section B. Vertical position shows dependency depth in the
displayed graph: base helper nodes appear at level 0, and a node is placed one level above the deepest displayed node it uses. Node color:
blue = formalized, gray = present but not yet, red = currently failing. The node set stabilizes by frame 51, and the final frame closes with
all displayed connected statements formalized.


Proof cone structure. We use proof cone as a visual term                                                                    4. Results and Discussion
for the dependency shape produced by this recursion: many
small helper nodes feed fewer intermediate nodes, and those                                                                 Setup. We evaluate on F ORMAL Q UAL B ENCH as the
feed the anchored target. In this run, the cone is not an                                                                   primary benchmark. The remaining experiments report
asymptotic claim; it is the concrete record of how a 6-node                                                                 a P UTNAM B ENCH slice, repeated-run stability, and Son-
plan becomes a 32-node plan as decomposition-driven re-                                                                     net/Haiku model variants. A problem counts as solved only
planning is invoked four times on hard nodes. This is the                                                                   if the produced Lean builds cleanly, preserves the original
key behavior of the harness. It does not ask one invocation                                                                 theorem signature, and passes the transitive #print
to solve the whole hard step; it asks the Planning Agent                                                                    axioms audit with sorryAx excluded and only
to make the next proof statement smaller, then lets the                                                                     {propext, Quot.sound, Classical.choice}
Lean Agent close the smaller pieces. The faithfulness and                                                                   permitted. Unless stated otherwise, the budget is 4 hours
mathematical-correction cases play complementary roles:                                                                     of wall-clock time per problem. Cost is reported in
faithfulness failure catches the rare clean-build Lean file                                                                 USD of LLM API spend. M ER L EAN -P ROVER uses
that has drifted from the anchored signature before that drift                                                              claude-opus-4-7 with default settings; Lean 4 v4.28.0
propagates downstream, and mathematical-correction fail-                                                                    with Mathlib (The mathlib Community, 2020) v4.28.0.
ure catches helper statements whose signature is internally
inconsistent before the Lean Agent burns its budget on a                                                                    F ORMAL Q UAL B ENCH. Table 1 reports the primary
target that cannot be true.                                                                                                 leaderboard comparison, while Table 2 gives the cost and
                                                                                                                            time profile of the solved problems. The problem IDs in
                                                                                                                            Table 2 are mapped to full theorem names in Section A; IDs
                                                                                                                            11–23 are the remaining benchmark problems not closed
                                                                                                                            by M ER L EAN -P ROVER. M ER L EAN -P ROVER solves 10/23,
                                                                                                                            surpassing OpenGauss (the strongest published open-source

                                                                                                                       4
                                                              MerLean-Prover

Table 1. F ORMAL Q UAL B ENCH closure rate. Baseline numbers are           Table 3. Per-problem wall-clock time (minutes) on Putnam 2025.
from (Math, Inc., 2026a); *Aristotle results are unvalidated. † Nine       Comparison columns for Aristotle (Achim et al., 2025), Seed-
of the ten M ER L EAN -P ROVER solves close within the 4-hour              Prover 1.5 (Chen et al., 2025), Axiom (Axiom Math, 2025), and
budget; one solve closes in an extended 4h40m run.                         Numina-Lean-Agent (NLA) (Liu et al., 2026) are reproduced from
                                                                           Table 3 of (Liu et al., 2026); “–” marks problems not solved.
           System                           Solved / 23
                                                                                   Prob.       Arist. Seed 1.5 Axiom      NLA    Ours
           M ER L EAN -P ROVER (ours)           10†
           OpenGauss                             8                                 A1            30         60     110      97     27
           Aristotle*                            6                                 A2            60         30     180      30     31
           Claude Code (Skills)                  5                                 A3            30        120     165      44     44
           Codex                                 5                                 A4           180        240     107     169     38
           opencode (Opus)                       5                                 A5             –          –     518    2040    235
           Claude Code                           4                                 A6            60        240     259      89     25
           Claude Code (MCP)                     3                                 B1           150        540     270      55    161
           Codex (Skills + MCP)                  3                                 B2            25        360      65     142     55
                                                                                   B3            40         30      43      30     16
                                                                                   B4             –        120     112     308     53
Table 2. Cost and wall-clock time for the ten M ER L EAN -P ROVER                  B5           420        240     254      88     43
solves on F ORMAL Q UAL B ENCH. Problem IDs are mapped to                          B6           180        180     494     797     61
theorem names in Section A. Token costs are computed from
model-provider usage logs. n/r marks per-problem costs the leader-                 Solved 10/12           11/12   12/12 12/12 12/12
board does not report. — means OpenGauss did not solve the                         Total     —               —     2577 3889    789
theorem. † ID 9 is the only solve outside the 4-hour budget.
                                                                           Table 4. Repeated-run timing stability on four selected F OR -
            M ER L EAN -P ROVER (ours)       OpenGauss                     MAL Q UAL B ENCH problems. Each problem is run eight times
      ID     Time             Cost          Time       Cost                and all attempts produce clean proofs. Time, statements, and min-
                                                                           utes per statement report mean ± std.; median and min–max report
       1     3h41m          $220.50        2h13m        n/r
                                                                           wall-clock time. Problem IDs follow Section A.
       2    3h12m           $184.27          —          —
       3     1h52m          $127.28        1h50m      $27.68
                                                                              ID        Time      Median Min–max         Stmts   Min/stmt
       4      11m           $10.05          12m        $2.54
       5    1h24m            $78.21        1h52m        n/r                    1 3.83±0.39h       3.85h    3.27–4.40h 16.1±3.4 14.9±3.5
       6    2h13m           $118.33        3h20m        n/r                    3 1.49±0.63h       1.22h    0.86–2.77h 7.3±2.8 12.5±3.0
       7      16m           $13.53          24m        $9.99                   4 0.22±0.04h       0.21h    0.17–0.29h 2.0±0.0 6.5±1.1
       8    1h01m            $62.16        1h34m      $15.70                   7 0.31±0.06h       0.30h    0.25–0.44h 2.9±1.0 6.8±1.2
       9    4h40m†          $273.66          —          —
      10    1h23m            $95.47        2h50m        n/r
                                                                           Prover 1.5 (Chen et al., 2025) (11/12). It is also the fastest
                                                                           system on 8 of the 12 problems, and the lowest total wall-
baseline) and every other published system on the leader-                  clock among systems that close the full set: 789 minutes
board. Nine solves close within the published 4-hour wall-                 against Axiom’s 2,577 and Numina-Lean-Agent’s 3,889.
clock budget; ID 9 is the one extended run and closes in                   The slowest M ER L EAN -P ROVER solve (A5) closes in 235
4h40m. Across the ten solves, total LLM API spend is                       minutes against Numina’s 2040 and Axiom’s 518. Every
$1,183.45 and total wall-clock time is 19h54m, for averages                solve passes the same kernel-level #print axioms au-
of $118.35 and 1h59m per solved problem. The cost-to-                      dit.
time ratio is higher than OpenGauss’s because the recursive
loop accumulates a large volume of prompt-cache reads
and writes across replans: cache traffic is much faster to                 Stability. Because the harness is stochastic and recursively
process than fresh generation, but every token is still billed,            revises its own proof plan, a single successful run does not
so the harness stays within a tight wall-clock budget while                show whether the behavior is typical. We therefore run
the per-problem dollar cost grows with plan size. Every                    M ER L EAN -P ROVER eight times on each of four selected
solve passes the C OMPARATOR-style transitive #print                       problems from F ORMAL Q UAL B ENCH, independent from
axioms audit, i.e. is axiom-free in the kernel sense. This                 Table 2, and report the timing distribution in Table 4. All
performance is achieved without fine-tuning or theorem-                    runs produce clean proofs. The variation is mainly explained
specific scaffolding.                                                      by two quantities: the number of statements in the final proof
                                                                           plan and the average time needed to close each statement. In
                                                                           the reported samples, both quantities vary only moderately
P UTNAM B ENCH. On the Putnam 2025 slice, M ER L EAN -
                                                                           across runs, giving a reasonably stable timing profile.
P ROVER closes 12/12 (Table 3), matching the per-set count
of Numina-Lean-Agent (Liu et al., 2026) and Axiom while                    In a separate pilot run on ID 1 (Banach–Stone), outside the
exceeding Aristotle (Achim et al., 2025) (10/12) and Seed-                 eight repeated runs reported in Table 4, we observed one

                                                                       5
                                                           MerLean-Prover

Table 5.      Per-problem wall-clock time and cost across               Strength. Model leverage.          The main strength of
model variants (claude-opus-4-7, claude-sonnet-4-6,
claude-haiku-4-5) on the same four F ORMAL Q UAL B ENCH
                                                                        M ER L EAN -P ROVER is that it turns a general-purpose rea-
problems as Table 4. Problem IDs follow Section A. — marks              soning model into a competitive Lean prover through har-
runs that did not finish; Haiku did not close IDs 1 or 3 within a       ness design alone. Without fine-tuning, a custom RL objec-
12-hour wall-clock budget.                                              tive, or theorem-specific scaffolding, it closes 10/23 F OR -
                                                                        MAL Q UAL B ENCH problems and outperforms the strongest
            Opus                Sonnet             Haiku                published open-source baseline. Repeatability. On the four
  ID   Time      Cost      Time       Cost     Time      Cost           selected F ORMAL Q UAL B ENCH problems in the stability
   1 3h41m $220.50 11h00m $111.89  —   —                                study, all eight repeated runs close cleanly. This suggests
   3 1h52m $127.28 5h09m $32.33    —   —                                that the recursive loop is not merely finding a single lucky
   4 11m   $10.05   17m    $3.37  29m $2.25                             trajectory: when the problem is within reach, the harness
   7 16m   $13.53 1h00m $12.00 4h34m $26.24                             can repeatedly build a complete proof plan and close it.
                                                                        Model flexibility. The same harness also transfers to smaller
                                                                        models: Sonnet closes all four shared problems, and Haiku
genuine outlier: the final plan grew to 58 statements and               closes the two short ones. This suggests that part of the
took 17 hours, while still closing the target theorem. We               capability comes from the harness structure itself, not only
hypothesize that repeated replanning can occasionally select            from the default Opus model.
a proof plan that is poorly supported by existing Mathlib
lemmas, causing the loop to introduce too many helper state-
ments before it converges. A comprehensive explanation of               Weakness. Model-capability floor. Because the harness
this behavior remains under investigation.                              does not use theorem-specific scaffolding or fine-tuning, its
                                                                        capability still depends strongly on the underlying reason-
                                                                        ing model. The model must propose useful decompositions,
Sonnet and Haiku. Table 5 compares the default Opus                     write Lean repairs, and judge mathematical correctness and
run with Sonnet and Haiku variants on the four F OR -                   faithfulness. If the model is too weak on any of these roles,
MAL Q UAL B ENCH problems also used for stability analysis.             the recursive loop loses much of its advantage. Haiku sits
Sonnet closes all four under the same harness, with cost                near this boundary: it closes the short problems in Table 5
2–4× lower than Opus on three of the four problems (and                 but does not finish the harder ones within 12 hours. Mathlib
roughly on par on ID 7) at a 1.5–4× wall-clock penalty.                 coverage. The system relies strongly on support from Math-
Haiku closes only the two short problems (IDs 4 and 7)                  lib. The initial proof plan, generated helper statements, and
and does not finish IDs 1 or 3 within a 12-hour budget. On              final Lean repairs all depend on having relevant library facts
ID 7, the cost pattern reverses: Haiku spends 4h34m for                 available and usable. On hard targets, the loop may require
$26.24 against Opus’s 16m for $13.53. Haiku produces a                  facts that are missing from Mathlib, or facts that exist but
clean proof but only after decomposing the target into a nine-          are difficult for the model to locate and use. This limitation
statement plan against Opus’s three, and the accumulated                is common to Lean-based theorem-proving systems that
token traffic over that longer plan outweighs Haiku’s 15×               rely on the existing library. Cost. The recursive loop is
lower per-token rate. We read this experiment as evidence               expensive: failed compile attempts, replanning steps, and
that the harness itself, rather than the strongest model alone,         repeated reads of a growing proof plan all create additional
contributes substantially to the decomposition; on small                model calls and token traffic. This makes the current system
problems the cheaper models reduce cost, but on harder                  costly to scale and difficult to use in cost-sensitive settings.
ones a weaker model can lengthen the proof plan enough to
offset the per-token cost advantage.

5. Conclusion                                                           Forward look. Three extensions are natural. (i) The cur-
                                                                        rent implementation is not optimized; engineering work
M ER L EAN -P ROVER is built around one architectural com-              to reduce redundant compile attempts, repeated planning,
mitment: one objective per agent invocation. With three                 and accumulated cache traffic could lower per-problem
agent types and a recursive outer loop, it matches the                  cost without changing the design. (ii) Because the har-
strongest published open-source result on F ORMAL Q UAL -               ness still closes problems with smaller models (Table 5),
B ENCH, without fine-tuning, a custom RL objective, or                  pairing it with an open-source Lean-specific model such
theorem-specific scaffolding. These results suggest that                as Leanstral (Mistral AI, 2026) is a natural direction for
harness design is a central factor in end-to-end Lean 4 the-            reducing cost further. (iii) Failed decompositions can be
orem proving, alongside raw model capability, and that a                used as signals for missing or under-documented Mathlib
relatively simple harness can already be effective.                     components.

                                                                    6
                                                         MerLean-Prover

References                                                             Math, Inc. OpenGauss: an open source, state of the art aut-
                                                                        oformalization harness. https://www.math.inc/
Achim, T., Best, A., Bietti, A., Der, K., Fédérico, M., Gukov,
                                                                        opengauss, 2026b. Accessed 2026-05.
  S., Halpern-Leistner, D., Henningsgard, K., Kudryashov,
  Y., Meiburg, A., Michelsen, M., Patterson, R., Rodriguez,            Mistral AI. Leanstral: Open-source foundation for trust-
  E., Scharff, L., Shanker, V., Sicca, V., Sowrirajan, H.,              worthy vibe-coding. https://mistral.ai/news/
  Swope, A., Tamas, M., Tenev, V., Thomm, J., Williams,                 leanstral, 2026. Accessed 2026-05.
  H., and Wu, L. Aristotle: IMO-level automated theorem
  proving, 2025. URL https://arxiv.org/abs/                            Ning, X., Tieu, K., Fu, D., Wei, T., Li, Z., et al. Code
  2510.01346.                                                            as agent harness, 2026. URL https://arxiv.org/
                                                                         abs/2605.18747.
Axiom Math. From seeing why to checking every-
  thing. https://axiommath.ai/territory/       Polu, S. and Sutskever, I. Generative language modeling
  from-seeing-why-to-checking-everything,        for automated theorem proving, 2020. URL https:
  2025.                                          //arxiv.org/abs/2009.03393.
Breen, B., Tredici, M. D., McCarran, J., Mijares, J. A.,               Ren, Y., Li, J., and Qi, Y. MerLean: An agentic framework
  Yin, W. W., Sulimany, K., Taylor, J. M., Koppens, F.                   for autoformalization in quantum computation, 2026.
  H. L., and Englund, D. Ax-Prover: A deep reasoning                     URL https://arxiv.org/abs/2602.16554.
  agentic framework for theorem proving in mathematics
  and quantum physics, 2025. URL https://arxiv.                        The mathlib Community. The Lean mathematical library.
  org/abs/2510.12787.                                                    In Proceedings of the 9th ACM SIGPLAN International
                                                                         Conference on Certified Programs and Proofs (CPP), pp.
Chen, J., Chen, W., Du, J., Hu, J., Jiang, Z., Jie, A., Jin, X.,         367–381, 2020. doi: 10.1145/3372885.3373824.
  Jin, X., Li, C., Shi, W., Wang, Z., Wang, M., Wei, C., Wei,
  S., Xin, H., Yang, F., Gao, W., Yuan, Z., Zhan, T., Zheng,           Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jen-
  Z., Zhou, T., and Zhu, T. H. Seed-Prover 1.5: Mastering                nings, M., Thakur, A., and Chaudhuri, S. PutnamBench:
  undergraduate-level theorem proving via learning from                  A multilingual competition-mathematics benchmark for
  experience, 2025. URL https://arxiv.org/abs/                           formal theorem-proving. In NeurIPS Datasets and Bench-
  2512.17260.                                                            marks Track, 2024.
Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S. Proof         Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and Ye,
  artifact co-training for theorem proving with language                 K. Hilbert: Recursively building formal proofs with in-
  models. In ICLR, 2022.                                                 formal reasoning, 2025. URL https://arxiv.org/
                                                                         abs/2509.22819.
Jaroslawicz, D., Whiting, B., Shah, P., and Maamari, K.
  How many instructions can LLMs follow at once?, 2025.                Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  URL https://arxiv.org/abs/2507.11538.                                  P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
Ju, H., Gao, G., Jiang, J., Wu, B., Sun, Z., Chen, L., Wang,             LeanDojo: Theorem proving with retrieval-augmented
  Y., Wang, Y., Wang, Z., He, W., Wu, P., Xiao, L., Liu, R.,             language models. In NeurIPS Datasets and Benchmarks
  Dai, B., and Dong, B. Automated conjecture resolution                  Track, 2023.
  with formal verification, 2026. URL https://arxiv.                   Zheng, K., Han, J. M., and Polu, S. miniF2F: A cross-system
  org/abs/2604.03789.                                                    benchmark for formal olympiad-level mathematics. In
Liu, J., Zhou, Z., Zhu, Z., Santos, M. D., He, W., Liu, J.,              ICLR, 2022.
  Wang, R., Xie, Y., Zhao, J., Wang, Q., Zhi, L., Li, J.,
  and Li, W. Numina-Lean-Agent: An open and general
  agentic reasoning system for formal mathematics, 2026.
  URL https://arxiv.org/abs/2601.14027.
Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua,
  M., Petroni, F., and Liang, P. Lost in the middle: How
  language models use long contexts. Transactions of the
  Association for Computational Linguistics, 2024.
Math, Inc. FormalQualBench: 23 graduate-level theorems
 formalized in Lean 4. https://www.math.inc/
 formalqualbench, 2026a. Accessed 2026-05.

                                                                   7
                                                            MerLean-Prover

A. F ORMAL Q UAL B ENCH Problem ID Map
Table 6. Problem IDs used in Table 2. IDs 1–10 are the problems closed by M ER L EAN -P ROVER; IDs 11–23 are the remaining
F ORMAL Q UAL B ENCH problems.

                            Closed by M ER L EAN -P ROVER                        Remaining benchmark problems
               ID    Theorem                                              ID   Theorem
                1    BanachStoneTheorem                                   11   BorsukUlamTheorem
                2    BurnsidePrimeDegreeTheorem                           12   CollatzMapAlmostBoundedValues
                3    ColorfulCaratheodoryTheorem                          13   ErdosDiscrepancyProblem
                4    DeBruijnErdos                                        14   GreenTaoTheorem
                5    DLOQuantifierElimination                             15   Hilbert17thProblem
                6    GleasonKahaneZelazkoTheorem                          16   JordanCycleTheorem
                7    JordanDerangementTheorem                             17   KakeyaTheorem3D
                8    ParisHarringtonPrinciple                             18   MaynardTaoBoundedPrimeGaps
                9    RungeTheorem                                         19   PontryaginDuality
               10    VonNeumannDoubleCommutantTheorem                     20   QuillenSuslinTheorem
                                                                          21   SchauderFixedPointTheorem
                                                                          22   SkolemMahlerLechTheorem
                                                                          23   TernaryGoldbachTheorem



B. BurnsidePrimeDegreeTheorem Node Map
                                            Table 7. Display node labels used in Figure 2.

        Node Statement id                                    Frame   Node Statement id                                   Frame
          #1 Thm MainTheorem                                     0       #17 Lem PiShiftImageEqShiftImage                   24
          #2 Lem BurnsideDichotomyCore                           0       #18 Lem PolynomialEvalAffine                       24
          #3 Lem CyclicSubgroupActsRegularly                     0       #19 Lem VandermondePowerSumsContradiction          24
          #4 Lem ExistsElementOfPrimeOrder                       0       #20 Lem PolyShiftIdentity                          24
          #5 Lem PrimeOrderElementIsCycle                        0       #21 Lem PowerSumsBinomialExpansion                 24
          #6 Lem PrimeDvdGroupOrder                              0       #22 Lem KeyDegreeInequality                        33
          #7 Lem MuellerAffineConjugation                       11       #23 Lem CoeffAtNwMinusROfLhs                       33
          #8 Lem AffinePermOfDifferenceSetPreserving            16       #24 Lem SumCompPowEqOfPerm                         33
          #9 Lem NotTwoTransitiveYieldsDifferenceSet            16       #25 Lem LagrangeInterpolantLeadingCoeffNeZero      33
         #10 Lem TauOrbitEquivConjTau                           16       #26 Lem SumCompPowEqOfShiftIdentity                33
         #11 Def TauOrbitEquiv                                  16       #27 Lem NatChooseNotDvdBySmallPrime                33
         #12 Lem AffineConjugatesTranslation                    16       #28 Lem PolyEqHigherCoeffZero                      33
         #13 Lem PowerSumsAllZeroForSmallK                      23       #29 Lem RhsLowerTermsNatDegreeBound                33
         #14 Lem PowerSumPiTranslate                            24       #30 Lem CoeffSumGCompXAddCuVanishLow               46
         #15 Lem DifferenceSetWLOGSmall                         24       #31 Lem LhsEqSumFwCompXAddCu                       46
         #16 Lem LagrangeInterpolantOfPerm                      24       #32 Lem CoeffSumGCompXAddCuExpansion               46




C. Sample Closed Lean Source: Nodes #1 and #2 of the BurnsidePrimeDegreeTheorem Trace
The two listings below reproduce the closed Lean source emitted by M ER L EAN -P ROVER for the first two nodes of
the worked example in Section 3: node #1 is the anchored target Thm MainTheorem, and node #2 is the helper
Lem BurnsideDichotomyCore after the faithfulness-driven rewrite at frame 11. Each file builds under lake build
and passes the transitive #print axioms audit with no sorry, admit, or user-introduced axiom.

Node #1: Thm MainTheorem. The anchored target, closed at frame 63 once the cone below has stabilized. The proof
case-splits on 2-pretransitivity and delegates the non-trivial direction to node #2.
import Mathlib.GroupTheory.GroupAction.MultipleTransitivity
import FormalQualBench.BurnsidePrimeDegreeTheorem.Auxiliary.BurnsideDichotomyCore

namespace BurnsidePrimeDegreeTheorem
open MulAction

/-- Burnside’s theorem on transitive permutation groups of prime
degree: a transitive permutation group of prime degree is either
2-transitive, or it has a normal regular subgroup. -/

                                                                     8
                                                    MerLean-Prover

theorem MainTheorem
    {α : Type*} [Fintype α]
    {G : Subgroup (Equiv.Perm α)}
    (htrans : IsPretransitive G α)
    (hp : (Fintype.card α).Prime) :
    IsMultiplyPretransitive G α2 ∨
      ∃N : Subgroup G, N.Normal ∧IsPretransitive N α∧
        ∀a : α, MulAction.stabilizer N a = ⊥:= by
  classical
  rcases Classical.em (IsMultiplyPretransitive G α2) with h2 | hNot2
  ·exact Or.inl h2
  ·haveI : IsPretransitive G α:= htrans
    exact Or.inr (burnside_dichotomy_core hp hNot2)

end BurnsidePrimeDegreeTheorem



Node #2: Lem BurnsideDichotomyCore. The substantive direction of Burnside’s prime-degree theorem, in the form
Müller (2005) gives. The Planning Agent’s initial plan contained a weaker statement of this node, which the Faithfulness
check rejected at frame 11; the listing below is the post-rewrite form that ultimately closes through node #8 and its
descendants. The three FormalQualBench imports correspond to the three outgoing edges of node #2 in Figure 2. The
file is shown in full: the module docstring is the human-readable plan that the Planning Agent committed to before any
compile attempts; the two helper theorems cyclicSubgroup normal and burnside dichotomy core card are
bookkeeping that the Lean Agent introduced inside the node’s file (without inflating the plan-level node count) for use by
the main lemma and by the cardinality statement of Burnside’s theorem.
/-
Copyright (c) 2026 MerLean Autoresearch. All rights reserved.
Released under MIT license.
-/
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.GroupTheory.GroupAction.Transitive
import Mathlib.GroupTheory.GroupAction.MultipleTransitivity
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Algebra.Group.Subgroup.ZPowers.Basic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Fintype.Card
import FormalQualBench.BurnsidePrimeDegreeTheorem.Auxiliary.ExistsElementOfPrimeOrder
import FormalQualBench.BurnsidePrimeDegreeTheorem.Auxiliary.CyclicSubgroupActsRegularly
import FormalQualBench.BurnsidePrimeDegreeTheorem.Auxiliary.MuellerAffineConjugation

/-!
# Burnside dichotomy core

Let ‘α‘ be a finite type with ‘p := Fintype.card α‘ prime, and let
‘G ≤Equiv.Perm α‘ act pretransitively on ‘α‘. Assume ‘G‘ is not 2-pretransitive.
Then there exists a subgroup ‘N ≤G‘ such that:

1. ‘N‘ is normal in ‘G‘,
2. ‘N‘ acts pretransitively on ‘α‘,
3. for every ‘x : α‘, the stabilizer in ‘N‘ of ‘x‘ is trivial (‘= ⊥‘).

These conditions together state that ‘N‘ acts regularly on ‘α‘; in particular
‘Nat.card N = p‘.

This is the substantive direction of Burnside’s classical 1911 theorem on
transitive permutation groups of prime degree, in the elementary form proved
by P. Müller, *Permutation groups of prime degree, a quick proof of Burnside’s
theorem*, Arch. Math. 85 (2005), 15--17.

## Strategy

                                                            9
                                       MerLean-Prover


* **Step 1.** Extract ‘τ : G‘ with ‘orderOf τ = p‘ via
  ‘exists_element_of_prime_order‘.
* **Step 2.** Take ‘N := Subgroup.zpowers τ ‘, the cyclic subgroup of ‘G‘
  generated by ‘τ ‘.
* **Step 3.** Pretransitivity and trivial stabilizers come from
  ‘cyclicSubgroup_isPretransitive‘ and ‘cyclicSubgroup_stabilizer_eq_bot‘.
* **Step 4.** Normality follows from ‘mueller_affine_conjugation‘: for every
  ‘g : G‘, ‘g τ g−1 ∈Subgroup.zpowers τ ‘. We extend to all integer powers
  using ‘conj_zpow‘ and ‘Subgroup.zpow_mem‘.

## Main result

* ‘BurnsidePrimeDegreeTheorem.burnside_dichotomy_core‘ : the existence of ‘N‘
  with all four properties.
-/

namespace BurnsidePrimeDegreeTheorem

open MulAction

variable {α : Type*} [Fintype α] [DecidableEq α]
variable {G : Subgroup (Equiv.Perm α)}

section BurnsideDichotomy

/-- **Normality of the cyclic subgroup generated by ‘τ ‘.**

Under the hypotheses of ‘mueller_affine_conjugation‘, the cyclic subgroup
‘Subgroup.zpowers τ ≤G‘ is normal in ‘G‘.

The argument: every element of ‘Subgroup.zpowers τ ‘ is ‘τ ˆ k‘ for some
‘k : Z‘. For any ‘g : G‘, we have ‘g * τ ˆ k * g−1 = (g * τ * g−1 ) ˆ k‘ by
‘conj_zpow‘. Since ‘g * τ * g−1 ∈Subgroup.zpowers τ ‘ (by Müller’s affine
conjugation lemma), and subgroups are closed under integer powers
(‘Subgroup.zpow_mem‘), the conjugate lies back in ‘Subgroup.zpowers τ ‘. -/
theorem cyclicSubgroup_normal
    [MulAction.IsPretransitive G α]
    (hp : (Fintype.card α).Prime)
    (hNot2 : ¬MulAction.IsMultiplyPretransitive G α2)
    (τ : G)
    (hord : orderOf τ = Fintype.card α) :
    (Subgroup.zpowers τ ).Normal := by
  refine ⟨?_⟩
  intro h hh g
  -- h ∈Subgroup.zpowers τ , so h = τ ˆ k for some k : Z.
  rw [Subgroup.mem_zpowers_iff] at hh
  obtain ⟨k, hk⟩ := hh
  -- Substitute h = τ ˆ k.
  rw [← hk]
  -- g * τ ˆk * g−1 = (g * τ * g−1 )ˆk.
  rw [← conj_zpow]
  -- Now (g * τ * g−1 ) ∈Subgroup.zpowers τ by Müller’s lemma.
  have hconj : g * τ * g−1 ∈Subgroup.zpowers τ :=
    mueller_affine_conjugation hp hNot2 τ hord g
  -- Subgroups are closed under integer powers.
  exact Subgroup.zpow_mem _ hconj k

/-- **Burnside dichotomy core.**

Let ‘α‘ be a finite type with ‘p := Fintype.card α‘ prime, and let
‘G ≤Equiv.Perm α‘ act pretransitively on ‘α‘. Assume ‘G‘ is not
2-pretransitive on ‘α‘. Then there exists a subgroup ‘N ≤G‘ such that:



                                            10
                                        MerLean-Prover

1. ‘N‘ is normal in ‘G‘,
2. ‘N‘ acts pretransitively on ‘α‘,
3. for every ‘x : α‘, the stabilizer in ‘N‘ of ‘x‘ is trivial.

These conditions state that ‘N‘ acts regularly on ‘α‘. -/
theorem burnside_dichotomy_core
    [MulAction.IsPretransitive G α]
    (hp : (Fintype.card α).Prime)
    (hNot2 : ¬MulAction.IsMultiplyPretransitive G α2) :
    ∃N : Subgroup G,
      N.Normal ∧
      MulAction.IsPretransitive N α∧
      ∀x : α, MulAction.stabilizer N x = ⊥:= by
  -- Step 1: extract τ : G with orderOf τ = p.
  obtain ⟨τ , hord⟩ := exists_element_of_prime_order (G := G) hp
  -- Step 2: take N := Subgroup.zpowers τ .
  refine ⟨Subgroup.zpowers τ , ?_, ?_, ?_⟩
  ·-- Normality, by ‘cyclicSubgroup_normal‘.
    exact cyclicSubgroup_normal hp hNot2 τ hord
  ·-- Pretransitivity, by ‘cyclicSubgroup_isPretransitive‘.
    exact cyclicSubgroup_isPretransitive τ hp hord
  ·-- Trivial stabilizers, by ‘cyclicSubgroup_stabilizer_eq_bot‘.
    intro x
    exact cyclicSubgroup_stabilizer_eq_bot τ hp hord x

/-- **Cardinality of the regular subgroup.**

Under the same hypotheses as ‘burnside_dichotomy_core‘, the regular subgroup
‘N := Subgroup.zpowers τ ‘ (with ‘τ ‘ of order ‘p‘) has ‘Nat.card N = p‘. This
follows from ‘Nat.card_zpowers‘ and ‘orderOf τ = p‘. -/
theorem burnside_dichotomy_core_card
    [MulAction.IsPretransitive G α]
    (hp : (Fintype.card α).Prime)
    (hNot2 : ¬MulAction.IsMultiplyPretransitive G α2) :
    ∃N : Subgroup G,
      N.Normal ∧
      MulAction.IsPretransitive N α∧
      (∀ x : α, MulAction.stabilizer N x = ⊥) ∧
      Nat.card N = Fintype.card α:= by
  obtain ⟨τ , hord⟩ := exists_element_of_prime_order (G := G) hp
  refine ⟨Subgroup.zpowers τ , ?_, ?_, ?_, ?_⟩
  ·exact cyclicSubgroup_normal hp hNot2 τ hord
  ·exact cyclicSubgroup_isPretransitive τ hp hord
  ·intro x
    exact cyclicSubgroup_stabilizer_eq_bot τ hp hord x
  ·rw [Nat.card_zpowers]
    exact hord

end BurnsideDichotomy

end BurnsidePrimeDegreeTheorem




                                               11
