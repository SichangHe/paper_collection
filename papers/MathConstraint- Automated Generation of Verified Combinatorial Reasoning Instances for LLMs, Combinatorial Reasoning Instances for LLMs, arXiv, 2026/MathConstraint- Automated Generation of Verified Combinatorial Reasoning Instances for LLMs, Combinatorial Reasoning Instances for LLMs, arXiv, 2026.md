                                            MathConstraint: Automated Generation of Verified
                                              Combinatorial Reasoning Instances for LLMs


                                            Viresh Pati1† , Zhengyu Li1 , Piyush Jha1 , Rahul Garg1 , Yatharth Sejpal 2 , Vijay Ganesh1†
                                                       1
                                                         Georgia Institute of Technology, USA 2 KNOWIDEA Technologies
                                                                      †
                                                                        {vireshpati, vganesh}@gatech.edu
arXiv:2605.08498v1 [cs.LG] 8 May 2026




                                                                                       Abstract

                                                    We introduce M ATH C ONSTRAINT, a hard, adaptive benchmark for evaluating the
                                                    combinatorial reasoning capabilities of LLMs. We combine constraint satisfaction
                                                    problems with rigorous solver-based verification and design an adaptive generator
                                                    to create instances that remain challenging as the LLMs improve in their reasoning
                                                    capabilities. Unlike existing benchmarks that quickly saturate on fixed datasets
                                                    or use LLM-as-a-judge for checking solutions, M ATH C ONSTRAINT uses param-
                                                    eterized problem types that enable scalable generation of arbitrarily difficult and
                                                    automatically verifiable instances. We release M ATH C ONSTRAINT-E ASY (266
                                                    instances), on which frontier models achieve between 72.6% (GEMINI -3.1- FLASH -
                                                    LITE ) and 87.6% ( GPT-5.5) accuracy, and M ATH C ONSTRAINT (329 instances)
                                                    on which the same models drop to between 18.5% (CLAUDE -4.6- SONNET) and
                                                    66.9% (GPT-5.5) accuracy, demonstrating the resilience of our benchmark genera-
                                                    tor against rapid progress in LLM reasoning capabilities. We evaluate 12 frontier
                                                    and open-weight models with and without access to a sandboxed Python environ-
                                                    ment that includes generic SAT/SMT solvers. Tool access roughly doubles frontier
                                                    accuracy on M ATH C ONSTRAINT (mean +28pp; up to +52pp for CLAUDE -4.6-
                                                    SONNET ). Further, halving the tool-call budget from 8 to 4 rounds erases up to
                                                    37 points — a sensitivity that most single-budget benchmarks miss. We release
                                                    the generator, dataset, and evaluation harness as a robust environment for study-
                                                    ing combinatorial reasoning and tool-use behavior under adversarially-tunable
                                                    difficulty.


                                        1     Introduction

                                        Large language models are improving quickly on mathematical and algorithmic tasks, but evaluating
                                        that progress reliably is becoming harder. Fixed benchmarks saturate, public leaderboards age quickly,
                                        and contamination becomes increasingly difficult to rule out as models ingest larger fractions of the
                                        open web and common benchmark corpora. These problems are especially acute for reasoning tasks,
                                        where a benchmark can stop being useful long before it stops being cited. What is needed is not
                                        merely another static test set, but a benchmark generator: evaluation infrastructure that can keep
                                        producing fresh, hard, automatically gradable instances as model capabilities change.
                                        Combinatorial reasoning is a particularly attractive setting for such infrastructure. Many combinatorial
                                        problems admit a natural difficulty dial through instance size or structural parameters; the answer
                                        space is too large to memorize; and correctness is brittle, since a single violated constraint invalidates
                                        an otherwise plausible solution. At the same time, these tasks are well matched to exact solvers,
                                        which makes it possible to grade outputs against solver-verified ground truth rather than relying on
                                        heuristics or LLM-as-a-judge. This combination of scalable hardness and rigorous verification makes
                                        combinatorial reasoning a natural stress test for LLMs.


                                        Preprint.
Recent NP-hard and SAT-oriented evaluations demonstrate that combinatorial reasoning remains
challenging for current models, but many are fixed collections of instances or narrow slices of problem
families [25, 63, 59, 40]. Verified mathematical benchmarks provide strong grading guarantees, but
often emphasize proof or olympiad-style mathematics rather than broad, parameterized combinatorial
search and reasoning [66, 55, 5]. Finally, adaptive benchmarks mitigate saturation and contamination,
yet typically do not pair continuous difficulty control with solver-backed verification over a broad
pool of combinatorial families [60, 6, 62].
We introduce M ATH C ONSTRAINT to combine these ingredients in a single evaluation framework.
M ATH C ONSTRAINT is an adaptive benchmark generator for combinatorial reasoning. Starting from
parameterized problem families drawn from constraint programming and graph construction domains,
it automatically writes natural-language problem instances, uses a solver to determine the correct
answer, and, when a concrete solution exists, stores a solver-verified example solution. Because
difficulty is controlled through generation rather than through a fixed test set, the same framework can
be rerun at cranked parameters to produce harder benchmarks without changing the prompt format or
the verification contract. This makes M ATH C ONSTRAINT better viewed as evaluation infrastructure
than as a one-off benchmark release.
This setup also lets us study tool use in a way that is tightly coupled to reasoning quality. We evaluate
models both without tools and with access to a sandboxed Python environment that includes generic
SAT/SMT solving support. In this regime, performance depends not only on whether a model can
reason about a combinatorial instance, but also on whether it can encode the problem correctly,
decide when to delegate to a solver, and manage a limited sequence of tool calls. Our experiments
show that solver access substantially changes the leaderboard, and that measured accuracy is highly
sensitive to the available tool budget. Together, these results suggest that budgeted tool use is not an
implementation detail of evaluation, but a representative capability in its own right. We introduce
SIM @k, a replay metric that scores logged traces under smaller tool budgets, and show that measured
accuracy is highly sensitive to that budget. Strong performance requires not just abstract reasoning,
but effective orchestration of external computation under constraints.
Our contributions are:

1. We introduce M ATH C ONSTRAINT, an adaptive benchmark framework that generates parameter-
   ized constraint-programming and graph/SAT-style problem types, with solver-certified satisfiability
   labels and verifier-checked candidate witnesses.
2. We instantiate this framework as two evaluation datasets, M ATH C ONSTRAINT-E ASY (266 in-
   stances, 25 types) and M ATH C ONSTRAINT (329 instances, 39 types), and demonstrate adaptive
   resistance to saturation. Frontier no-tools accuracy falls from 72.6–87.6% on M ATH C ONSTRAINT-
   E ASY to 18.5–66.9% on M ATH C ONSTRAINT.
3. We evaluate 12 frontier and open-weight models across no-tools and tool-enabled settings. On
   M ATH C ONSTRAINT, only 3/12 models exceed 50% accuracy without tools, while tool access
   raises mean accuracy by 28 percentage points and improves CLAUDE -4.6- SONNET by 52 points.
4. We introduce SIM @k, a tool-budget replay metric, and highlight tool-use efficiency as a first-class
   dimension of combinatorial reasoning abilities: halving the budget from 8 to 4 rounds erases up to
   37 pp of accuracy.
5. We release an open source library for evaluating LLMs with agentic tool-use capabilities on
   combinatorial reasoning tasks. Our evaluation code is available at this link. Our datasets, M ATH -
   C ONSTRAINT and M ATH C ONSTRAINT-E ASY are available on HuggingFace.

2   Related Work
In this section, we discuss important prior approaches to evaluating the combinatorial and mathemati-
cal reasoning abilities of LLMs.

Combinatorial and NP-hard reasoning benchmarks. Combinatorial search is a natural stress
test for LLMs. Hardness rises continuously with problem size, the answer space is too large to
memorize, and a single missed constraint makes a candidate wrong. A recent line of work grounds
this evaluation in computational complexity, anchored by NPH ARD E VAL [25] and NPPC [63];


                                                   2
NP-E NGINE [38] pushes the same idea toward optimization reasoning. A second line stays close
to constraint-programming and SAT. Z EBRA L OGIC [40] indexes hardness by Z3 conflict count
and reports a sharp accuracy collapse with scale, a pattern echoed by SATB ENCH [59], by the
natural-language combinatorial-optimization suite of Jiang et al. [31], and by E NIGMATA [10]. Graph
and logic-puzzle variants such as G RAPH A RENA [53] and H ARDCORE L OGIC [39] extend the lens
to structured objects and long-tail rule shifts. CO-B ENCH [52] sits a level above by scoring agents
that design solvers, while M ATH C ONSTRUCT [5] applies programmatic verifiers to constructive
Olympiad problems that are themselves often NP-hard.


Verified mathematical benchmarks As LLMs are deployed on longer and more open-ended
mathematics, automatic verification with formal contracts becomes essential for grading at scale
[32]. Verified benchmarks such as MINI F2F [66] and P UTNAM B ENCH [55] provide olympiad-
and Putnam-level targets that have driven a substantial body of prover work in Lean4 [18]. A
complementary thread verifies the object a model produces rather than its proof, via Python checkers
in M ATH C ONSTRUCT [5] or SAT-solver ground truth in SATB ENCH [59].


Adaptive and contamination-resistant benchmarks. Frontier capabilities now advance on a
timescale that outpaces benchmark construction. Any fixed test set is on borrowed time, as leader-
boards saturate, and contamination from training data becomes hard to rule out. L IVE B ENCH [60]
and M ATH A RENA [6] respond by drawing continuously from newly released competitions, the latter
producing direct contamination evidence on AIME 2024. GSM-S YMBOLIC [44] shows that even
surface symbolic re-skinning of GSM8K [14] can move accuracy by tens of points. More recently,
M ATH D UELS [62] lets difficulty co-evolve with participants by casting evaluation as self-play be-
tween authors and solvers, F RONTIER CS [42] curates open-ended tasks from expert programmers,
and the ARC-AGI series [11, 12] pursues memorization-resistant puzzles by design. Together, these
efforts mark a shift away from one-shot benchmarks and toward evaluation infrastructure that is
expected to keep producing harder problems as models improve and inspire our benchmark in this
way.


Tool-use evaluation benchmarks. Tool use is now a frontier capability in its own right. Deciding
when to delegate to a solver, search engine, or interpreter is at least as load-bearing as the underlying
reasoning. BFCL [47] anchors a line that scores whether tool calls are well-formed, largely orthogonal
to the reasoning content of the call. Mathematical benchmarks have begun reporting paired runs
with and without a Python sandbox. Both M ATH C ONSTRUCT [5] and M ATH A RENA [6] observe that
code access roughly doubles accuracy at a several-fold cost increase. Most mathematical tool-use
benchmarks employ a single tool call budget (M ATH C ONSTRUCT uses a 4 round budget). We identify
this as a category gap and analyze tool use under varied synthetic budgets in Section 4.2.


3     MathConstraint

M ATH C ONSTRAINT is a generator-verifier loop for natural-language combinatorial decision problems.
A released dataset is a finite slice of this loop. Each instance carries a prompt, a backend encoding,
a solver-certified polarity, optional witness data, difficulty metadata, and a verifier contract. This
section describes the generator first, then the evaluation interface used in our experiments.


3.1   Problem Families

M ATH C ONSTRAINT contains 39 parameterized problem types. Each type is a decision problem: the
model must either produce a witness satisfying all constraints, or correctly report that no witness
exists. The registry spans combinatorial designs (BIBD, Hadamard matrices, Latin squares), graph
threshold problems (maximum clique, vertex cover, k-colorability), number-theoretic and sequence
constructions (Golomb rulers, van der Waerden colorings), placement and scheduling problems
(n-queens, social golfers), and extremal graph-construction tasks (Ramsey graphs, triangle-free
graphs).


                                                   3
Encodings come from two solver-facing backends. The pycsp3-models1 corpus supplies constraint-
programming formulations solved with general-purpose CP/SAT backends [37]. The pysms library2
supplies SAT encodings with symmetry-breaking predicates for extremal graph families [35]. The
backends are not exposed to the model in the no-tools condition; they define the ground-truth and
verification semantics.
A detailed description of the problem set can be found in Section D and Section I.

3.2   Automated Generation

Generation is profile-driven. A profile names types, parameter domains, per-type counts, prompt
templates, and a seed. For each sampled parameter tuple, the generator instantiates the backend
encoding, solves it with the reference solver, renders the prompt, and writes a self-contained record.

             Generation profile                        pycsp3 encoder
                                               N-queens, Golomb, Sudoku, ...



         {Ti } types, Θi domains,                                                     Solvers
                                                        pysms encoder
         ni counts, s seed, NL templates
                                              Ramsey, chromatic, k-coloring, ...




           Instance
           prompt "Place 4 queens on a 4×4 board such that no two attack..."
           verdict SAT      solution [1, 3, 0, 2]
           solver 810 ms    size     |V |=4, |C|=3

Figure 1: Generation pipeline. A profile samples from a large registry of problem types and a
parameter domain. Each instance is encoded via pycsp3 or pysms and solved by the reference
back-end, producing an output bundling the natural-language prompt with solver-verified ground
truth.


Polarity. Polarity is determined by the reference solver after parameter sampling. We do not
balance SAT and UNSAT by construction; the split is induced by the parameter domains of each
problem type. M ATH C ONSTRAINT is 69.3% SAT, while M ATH C ONSTRAINT-E ASY is 77.4% SAT.
UNSAT instances are first-class: the model must identify infeasibility rather than provide a witness,
and the verifier applies the same polarity contract to both tool and no-tool runs.

Partial assignments. SAT instances may include a partial assignment that fixes a subset of decision-
variable positions to values from a reference solution. These fixed values are appended to the prompt
and enforced by the verifier. Partial assignments create a scaffolding axis orthogonal to instance size.
They can reduce search while preserving the same formal constraint system.

Difficulty. Each instance records reference solver wall time. We also store structural proxies such as
variable counts, constraint counts, edge counts, and a search-space estimate when available. Difficulty
is tunable before generation by changing profile ranges, and after generation by filtering on recorded
solver metadata.

3.3   Verification and Tool Interface

Verification is handled by formal contracts. A response is parsed as a satisfiability claim plus an
optional solution. UNSAT claims are compared to the solver-certified polarity. SAT claims are graded
up to isomorphism. The candidate is injected as hard unit constraints on top of the original encoding
  1 https://github.com/xcsp3team/PyCSP3-models
  2 https://github.com/markirch/sat-modulo-symmetries




                                                   4
Table 1: Generation-time difficulty of the released datasets. Solver-time columns report reference
solver wall time in seconds.
                   Component                               n     Types               SAT   p50 p90 p99 Max
                   M ATH C ONSTRAINT-E ASY 266                     25       206 (77.4%) 0.20 1.79 11.8 56.5
                   M ATH C ONSTRAINT       329                     39       228 (69.3%) 2.52 75.6 653 1372



and re-solved, so any witness in the same canonical equivalence class is accepted. This grades the
submitted object, not a textual derivation, and naturally handles multiple correct solutions.
We evaluate each model in two conditions. In NO _ TOOLS, the model returns only a final JSON
answer. In TOOLS, the model may interleave reasoning with calls to execute_python, a sandboxed
Python interpreter with generic SAT/SMT libraries, and must finish with submit_answer. The tool
budget is capped at eight rounds. If a model reaches the cap without an explicit submission, the
evaluator force-submits the final natural-language response through a strict parser; we report this
behavior separately in Table 21. Metric definitions are given in Section C.

                                 max 8 rounds
                              execute_python
                           fresh subprocess, no net,
                              pysat / z3 / pycosat


                                                                                                                  correct

    Prompt                                                                                     Validator
                                                               submit_answer                                    wrong-soln
    instance NL prompt                                      satisfiable, solution,
                                                                                             re-solve with
                                    LLM
    system prompt                                                reasoning
                                                                                            submission as
    tool schemas (tools)                                                                    unit constraints
                                                                                                               wrong-polarity

                                         force-submit (parser)                                                   parse-fail



Figure 2: Evaluation pipeline. The model interleaves execute_python (sandboxed, max 8 rounds)
and submit_answer; on budget exhaustion the parser force-submits the last NL response. The
validator re-solves with the submission injected as constraints, distinguishing four outcomes.



3.4    Adaptivity

M ATH C ONSTRAINT’s adaptivity is a crucial property of the framework. The generator-verifier-filter
loop (Figure 3) can be rerun by changing parameter ranges, changing the frontier-model admission
filter, or adding new families from pycsp3-models (which contains over 400 problem models) and
pysms (for graph problems). Like M ATH A RENA, we treat benchmark refresh as an explicit release
cycle rather than a one-time dataset construction, and adopt a similar refresh cadence. However, each
refresh is manufactured from our own parameterized, solver-backed registry rather than harvested
from new external competitions [6]. M ATH C ONSTRAINT-E ASY and M ATH C ONSTRAINT are the
first two slices from this loop. M ATH C ONSTRAINT-E ASY is retained as a lower-difficulty slice, while
the headline M ATH C ONSTRAINT release reruns the same machinery with harder profile regimes and
admits instances that remain discriminative under frontier-model evaluation.


4     Evaluation

Setup. We evaluate twelve models. Ten are frontier or near-frontier systems: GPT-5.5 [46],
CLAUDE - OPUS -4.7 [3], CLAUDE -4.6- SONNET [4], GEMINI -3.1- PRO and GEMINI -3.1- FLASH -
LITE [19], GROK -4.20 [61], DEEPSEEK - V 4- PRO and DEEPSEEK - V 4- FLASH [20], QWEN 3.6-
PLUS [48], and KIMI - K 2.6 [54]. The remaining two are open-weight baselines: GPT- OSS -120 B [1]
and LLAMA -3.3-70 B - INSTRUCT [27]. Models are accessed through OpenRouter at temperature 0;
model configuration, pricing, and implementation details are in Sections A and E.


                                                                        5
                                                 cranked params
                                    new types
                                    (optional)


                                                   Generator



                                 M ATH -                             Evaluation
                              C ONSTRAINT                           + verification


                                      yes         ≥ 1 frontier
                                                    failed?

                                                        no

                                                     drop


Figure 3: Adaptivity loop. The generator produces candidates; each is evaluated and verified, and
admitted into M ATH C ONSTRAINT only if at least one frontier model fails. M ATH C ONSTRAINT
feeds back into the generator, which cranks parameters across cycles (self-loop) and may optionally
introduce new problem types. The benchmark refreshes itself as models improve.


4.1   Main Results

The adaptive refresh: E ASY to M ATH C ONSTRAINT. Tables 2 and 3 show that rerunning the
generator with harder profiles restores discrimination. Among frontier and near-frontier systems, mean
no-tools accuracy falls from 80.5% on M ATH C ONSTRAINT-E ASY to 42.0% on M ATH C ONSTRAINT;
across all twelve models, the number above 70% drops from 10 to 0, and the number above 50% drops
from 11 to 3. The headline M ATH C ONSTRAINT benchmark remains challenging and unsaturated:
GPT-5.5 solves 220/329 (66.9%), GROK -4.20 solves 191/329 (58.1%), and the cohort spans down
to CLAUDE -4.6- SONNET at 18.5%.

The witness gap. Across no-tools runs, SAT-polarity accuracy systematically exceeds end-to-
end verifier accuracy. The gap (Table 24) is largest for LLAMA -3.3-70 B - INSTRUCT (+54.4 pp),
CLAUDE -4.6- SONNET (+53.5 pp), and GEMINI -3.1- FLASH - LITE (+51.4 pp). Trace audits show two
contributing patterns: models declare SAT and submit invalid witnesses, or fail to find a witness for
a SAT instance and resolve UNSAT. Deciding existence is easier than constructing an object that
survives exact verification. The witness gap is the dominant no-tools failure mode and the lever that
tools pull on Section 4.2.

Free-UNSAT baseline. 30.7% of M ATH C ONSTRAINT is UNSAT, so a model that always answers
UNSAT scores 30.7% overall and 100% on the UNSAT subset. By contrast, CLAUDE -4.6- SONNET
(16.8% UNSAT-conditional accuracy) and LLAMA -3.3-70 B - INSTRUCT (24.8%) perform far below
the UNSAT-subset ceiling. They actively guess wrong on UNSAT rather than free-riding on polarity

Table 2: No-tools performance on the full 329-instance M ATH C ONSTRAINT release. Accuracy and
SAT Acc. are defined in Section C.
                  Model                           Correct Accuracy (%) SAT Acc. (%)
                  GPT-5.5                           220           66.9               79.0
                  CLAUDE - OPUS -4.7                140           42.6               56.8
                  CLAUDE -4.6- SONNET               61            18.5               72.0
                  GEMINI -3.1- PRO                  170           51.7               67.2
                  GEMINI -3.1- FLASH - LITE          82           24.9               76.3
                  GROK -4.20                        191           58.1               67.8
                  DEEPSEEK - V 4- PRO               130           39.5               49.2
                  DEEPSEEK - V 4- FLASH             112           34.0               61.4
                  QWEN 3.6- PLUS                    156           47.4               72.3
                  KIMI - K 2.6                      118           35.9               42.9
                  GPT- OSS -120 B                   130           39.5               47.7
                  LLAMA -3.3-70 B - INSTRUCT         28            8.5               62.9



                                                       6
Backend asymmetry. Stratifying by backend reveals a structural gap. On M ATH C ONSTRAINT
no-tools, mean accuracy across all twelve models is 61.1% on pysms instances versus 29.0% on
pycsp; the six-model frontier cohort shows a similar split, 66.5% versus 33.6%. Extremal-graph
pysms instances admit many witnesses with structural symmetry, while pycsp encodings often
constrain a unique numeric object. Tools narrow the gap Section 4.2. Full per-model stratification
can be found in Table 27.

Table 3: Performance on M ATH C ONSTRAINT-E ASY (n = 266). Accuracy is verifier acceptance;
SAT Acc. is polarity accuracy (Section C). The same frontier models that span 18.5–66.9% on
M ATH C ONSTRAINT (Table 2) cluster between 72.6% and 87.6% here without tools and approach
saturation with tools.
                                                     no_tools                   tools
            Model                         Acc. (%) SAT Acc. (%) Acc. (%) SAT Acc. (%)
            GPT-5.5                           87.6         91.4          91.7           96.6
            CLAUDE - OPUS -4.7                85.3         88.7          90.2           94.7
            CLAUDE -4.6- SONNET               75.2         94.0          89.8           94.7
            GEMINI -3.1- PRO                  84.2         89.8          91.4           95.5
            GEMINI -3.1- FLASH - LITE         72.6         94.4          89.5           94.0
            GROK -4.20                        85.0         87.2          87.2           92.5
            DEEPSEEK - V 4- PRO               82.7         85.7          71.8           75.2
            DEEPSEEK - V 4- FLASH             74.4         86.5          71.4           78.2
            QWEN 3.6- PLUS                    81.2         87.6          88.3           93.6
            KIMI - K 2.6                      77.1         81.2          82.3           86.8
            GPT- OSS -120 B                   69.2         75.9          71.4           84.6
            LLAMA -3.3-70 B - INSTRUCT        22.9         52.6          27.8           37.6



4.2   Tool-use

Table 4 evaluates the same M ATH C ONSTRAINT instances with a sandboxed Python tool budget.
Tool access changes both absolute accuracy and the ranking. GPT-5.5 rises from 66.9% to 80.9%,
CLAUDE -4.6- SONNET rises from 18.5% to 70.5%, and GEMINI -3.1- PRO rises from 51.7% to 72.9%.
The gains are not uniform: models that already emit compact, direct answers sometimes improve
only modestly, while models that can synthesize solver encodings from the prompt gain sharply. Thus
tool access measures the additional skill of translating informal constraints into executable search
under a fixed interaction budget. Representative traces in Section H illustrate these regimes.

Table 4: Tool-enabled performance on the full 329-instance M ATH C ONSTRAINT release. Accuracy
and SAT Acc. are defined in Section C.
                  Model                          Correct Accuracy (%) SAT Acc. (%)
                  GPT-5.5                            266          80.9          94.2
                  CLAUDE - OPUS -4.7                 255          77.5          90.9
                  CLAUDE -4.6- SONNET                232          70.5          91.8
                  GEMINI -3.1- PRO                   240          72.9          86.3
                  GEMINI -3.1- FLASH - LITE          205          62.3          87.5
                  GROK -4.20                         219          66.6          83.3
                  DEEPSEEK - V 4- PRO                136          41.3          51.1
                  DEEPSEEK - V 4- FLASH              120          36.5          47.7
                  QWEN 3.6- PLUS                     218          66.3          83.3
                  KIMI - K 2.6                       197          59.9          71.4
                  GPT- OSS -120 B                    120          36.5          57.8
                  LLAMA -3.3-70 B - INSTRUCT         105          31.9          48.0


Tools substitute for inference-time reasoning. The cohort’s largest tool-induced gain is CLAUDE -
4.6- SONNET: 18.5% no-tools → 70.5% (+52 pp). Sonnet runs in our setup with no extended-thinking
budget (Section E). With less inference-time reasoning, it commits to invalid witnesses, producing


                                                      7
                                                                                              GPT          Grok
                            GPT       Sonnet    Grok      Qwen                      80%
                                                                                              Opus         DSPro
                            Opus      GPro      DSPro
                                                                                              Sonnet       Qwen
           90%                                                                      60%       GPro




                                                                         Accuracy
           80%

           70%
                                                                                    40%
Accuracy




           60%

           50%
                                                                                    20%
           40%

           30%
                                                                                    0%
           20%
                                                                                          1            2       4     8
                  Easy             Easy          MC          MC
                 no tools          tools       no tools     tools                                Tool-round budget

Figure 4: Accuracy across datasets and tool con-                        Figure 5: SIM @k curves on M ATH C ON -
ditions for selected models. The plotted aggre-                         STRAINT. Halving the budget from 8 to 4 rounds
gates are reported in Tables 2 to 4.                                    erases up to 37 pp. Table 11 reports sensitivities
                                                                        for all models.



the cohort’s largest witness gap (+53.5 pp) (Table 24). Tool access restores the missing computation.
Solver calls externalize witness construction, and the witness gap closes. Tool budget and inference-
time reasoning are partially fungible. SIM @k Section 4.3 measures how much orchestration depth
the substitution requires.
On M ATH C ONSTRAINT-E ASY, tools further compress the frontier-model spread. Top models cluster
around 90% verifier accuracy (Table 3). This reinforces M ATH C ONSTRAINT-E ASY’s position as
a useful but less discriminative slice rather than the headline benchmark, motivating the adaptive
construction of M ATH C ONSTRAINT in Section 3.4. A four-condition comparison across datasets and
tool settings is provided in Figure 4.


Tool fingerprints. Models also differ in what they call. On M ATH C ONSTRAINT tools, GROK -
4.20 uses z3 for 44% of its execute_python calls; GEMINI -3.1- PRO balances pysat (32%) and
z3 (26%); the CLAUDE models default to brute-force loops (60% for SONNET, 54% for OPUS) with
pysat as the secondary mode; LLAMA -3.3-70 B - INSTRUCT relies on networkx (50%). A full
breakdown can be found in Table 20.


4.3          SIM @k: Tool-Budget Replay


A single 8-round number hides large variance (Table 11). We replay logged tool trajectories under
smaller caps: SIM @k truncates each trace after at most k tool rounds and re-applies the verifier and
force-submit logic (Section C). SIM @k is a conservative lower bound on what a budget-aware policy
could achieve; a model told it has k rounds in advance might prune exploratory calls and do better.
The curve shapes expose policy differences that a scalar leaderboard hides. LLAMA -3.3-70 B -
INSTRUCT is early-saturating: it reaches its full replayed accuracy by SIM @2. GPT-5.5 and GROK -
4.20 are steadier, with useful work spread across the budget. CLAUDE -4.6- SONNET and GEMINI -3.1-
FLASH - LITE are late-gain profiles, with much of their accepted mass appearing only after four rounds.
These patterns indicate that most successful tool runs are not one-shot solver calls, but multi-round
attempts to formulate, debug, execute, and submit a certificate.
The same behavior appears from two other angles in the appendix. Models with steep SIM @k
curves also tend to use many rounds on M ATH C ONSTRAINT (Table 19), and runs without explicit
submit_answer can still be rescued by final-response parsing (Table 21). This rescue effect is
substantial for some models: GPT-5.5 passes 67/88 force-submitted traces (76.1%), while DEEPSEEK -
V 4- FLASH passes only 19/180 (10.6%). Thus tool-budget sensitivity, round usage, and force-submit
rescue are three views of the same agentic behavior.


                                                                    8
4.4   Difficulty and Efficiency

Parameter ranges as an LLM difficulty dial. M ATH C ONSTRAINT is harder at generation time
than M ATH C ONSTRAINT-E ASY: median solver time rises from 0.20 to 2.52 seconds, and p99 rises
from 11.8 to 653 seconds (Table 1). The same shift transfers to models. Frontier no-tools accuracy
drops from the 72.6–87.6% band on M ATH C ONSTRAINT-E ASY to 18.5–66.9% on M ATH C ON -
STRAINT, reopening separation that the easy slice largely compresses (Tables 2 and 3).


Solver time is not a within-regime proxy. Within the hard release, reference solver time weakly
predicts model accuracy: log solver time correlates only −0.15 with no-tools cross-model accuracy
and −0.14 with tool-enabled accuracy, and Figure 9 is roughly flat across solver-time quartiles. We
treat this as a diagnostic result rather than a failure of the difficulty dial. Cranked ranges reliably
harden the distribution, but ranking individual natural-language instances by LLM difficulty requires
features that solver wall time alone does not expose.
Tool use also changes efficiency. Some models become both more accurate and cheaper per accepted
answer because tool calls shorten long free-form reasoning traces; others spend many rounds encoding
or debugging. We report per-instance tokens, latency, and provider-billed cost in Tables 12 to 15,
token-type breakdowns in Tables 16 and 17, and the cost–accuracy scatter in Figure 6.

4.5   Diagnostics

Additional diagnostics appear in the appendix: model-correctness correlations, polarity/backend
stratification, failure buckets, and per-type breakdowns (Figures 7 and 8 and Tables 22, 23 and 27
to 32).


5     Conclusion

M ATH C ONSTRAINT is designed as evaluation infrastructure for combinatorial reasoning rather
than another fixed benchmark. By grounding each instance in solver-certified satisfiability and
verifier-checked witnesses, the framework can be rerun at harder settings as models improve. The
M ATH C ONSTRAINT-E ASY→M ATH C ONSTRAINT transition is the first example of that refresh cycle:
the same generator-verifier machinery, drawing harder parameters and problems from our two solver-
backed registries (pycsp3-models and pysms), restores separation between frontier models that the
easier benchmark had begun to compress.
Our experiments also show that tool-enabled evaluation measures a different capability, i.e., whether
models can turn natural language constraints into working solver programs under limited budgets.
On the harder release, access to a sandboxed Python environment with generic SAT/SMT solvers
raises frontier mean accuracy by 28 points, with gains as large as 52 points for CLAUDE -4.6- SONNET.
The SIM @k analysis makes the same point from another angle: halving the tool budget from 8 to 4
rounds erases up to 37 points of accuracy. Strong reasoning increasingly depends not only on finding
the right answer, but also on using external computation effectively.
Our study also has limitations. The released benchmarks use a fixed prompt format and a fixed
maximum tool budget, and SIM @k only approximates how models would behave under smaller
native budgets. Future work could explore adaptive prompting, budget-aware policies, and broader
classes of reasoning tools.
More broadly, M ATH C ONSTRAINT moves toward a different kind of reasoning benchmark that is
adaptive, solver-verified, and tool-aware. As models increasingly rely on external computation, future
evaluations should measure not only reasoning ability, but also how effectively models coordinate
search, verification, and tool use together.


Acknowledgments

We gratefully acknowledge KNOWIDEA Technologies for providing model inference credits used in
our evaluations. We also thank Vidhi Patra for helpful discussions and feedback.


                                                  9
References
 [1] Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus,
     Rahul K Arora, Yu Bai, Bowen Baker, Haiming Bao, et al. gpt-oss-120b & gpt-oss-20b model
     card. arXiv preprint arXiv:2508.10925, 2025.
 [2] William Symes Andrews. Magic squares and cubes. Open Court Publishing Company, 1917.
 [3] Anthropic. System card: Claude opus 4.7. Technical report, Anthropic, April 2026. URL
     https://www.anthropic.com/system-cards. Accessed: 2026-04-27.
 [4] Anthropic. System card: Claude sonnet 4.6. Technical report, Anthropic, Feburary 2026. URL
     https://www.anthropic.com/system-cards. Accessed: 2026-04-27.
 [5] Mislav Balunović, Jasper Dekoninck, Nikola Jovanović, Ivo Petrov, and Martin Vechev. Math-
     construct: Challenging llm reasoning with constructive proofs. arXiv preprint arXiv:2502.10197,
     2025.
 [6] Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, and Martin Vechev. Math-
     arena: Evaluating llms on uncontaminated math competitions. arXiv preprint arXiv:2505.23281,
     2025.
 [7] Jakob Bernasconi. Low autocorrelation binary sequences: statistical mechanics and configura-
     tion space analysis. Journal de Physique, 48(4):559–567, 1987.
 [8] Max Bezzel. Proposal of 8-queens problem. Berliner Schachzeitung, 3(363), 1848.
 [9] G.S. Bloom and S.W. Golomb. Applications of numbered undirected graphs. Proceedings of
     the IEEE, 65(4):562–570, 1977. doi: 10.1109/PROC.1977.10517.
[10] Jiangjie Chen, Qianyu He, Siyu Yuan, Aili Chen, Zhicheng Cai, Weinan Dai, Hongli Yu, Qiying
     Yu, Xuefeng Li, Jiaze Chen, et al. Enigmata: Scaling logical reasoning in large language models
     with synthetic verifiable puzzles. arXiv preprint arXiv:2505.19914, 2025.
[11] Francois Chollet, Mike Knoop, Gregory Kamradt, and Bryan Landers. Arc prize 2024: Technical
     report. arXiv preprint arXiv:2412.04604, 2024.
[12] Francois Chollet, Mike Knoop, Gregory Kamradt, Bryan Landers, and Henry Pinkard. Arc-
     agi-2: A new challenge for frontier ai reasoning systems. arXiv preprint arXiv:2505.11831,
     2025.
[13] Vasek Chvátal and Paul Erdös. A note on hamiltonian circuits. Discret. Math., 2(2):111–113,
     1972.
[14] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
     Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to
     solve math word problems. arXiv preprint arXiv:2110.14168, 2021.
[15] Charles J Colbourn. The complexity of completing partial latin squares. Discrete Applied
     Mathematics, 8(1):25–30, 1984.
[16] J.P. Costas. A study of a class of detection waveforms having nearly ideal range—doppler
     ambiguity properties. Proceedings of the IEEE, 72(8):996–1009, 1984. doi: 10.1109/PROC.
     1984.12967.
[17] Nicolaas Govert De Bruijn. A combinatorial problem. Proceedings of the Section of Sciences
     of the Koninklijke Nederlandse Akademie van Wetenschappen te Amsterdam, 49(7):758–764,
     1946.
[18] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language (system description).
[19] Google Deepmind. Gemini 3.1 pro model card. Technical report, Google, Feburary 2026.
     URL https://deepmind.google/models/model-cards/gemini-3-1-pro/. Accessed:
     2026-04-28.


                                                10
[20] DeepSeek-AI. Deepseek-v4: Towards highly efficient million-token context intelligence, 2026.
[21] Paul Erdös. Graph theory and probability. Canadian Journal of Mathematics, 11:34–38, 1959.
[22] Paul Erdos and Horst Sachs. Reguläre graphen gegebener taillenweite mit minimaler knotenzahl.
     Wiss. Z. Martin-Luther-Univ. Halle-Wittenberg Math.-Natur. Reihe, 12(251-257):22, 1963.
[23] Leonhard Euler. Solution d’une question curieuse que ne paroit soumise à aucune analyse.
     Mémoires de l’académie des sciences de Berlin, pages 310–337, 1766.
[24] Leonhard Euler. Recherches sur un nouvelle espéce de quarrés magiques. Verhandelingen
     uitgegeven door het zeeuwsch Genootschap der Wetenschappen te Vlissingen, pages 85–239,
     1782.
[25] Lizhou Fan, Wenyue Hua, Lingyao Li, Haoyang Ling, and Yongfeng Zhang. Nphardeval:
     Dynamic benchmark on reasoning ability of large language models via complexity classes.
     In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
     (Volume 1: Long Papers), pages 4092–4114, 2024.
[26] Martin Gardner.      Mathematical games.      Scientific American, 223(6):110–115, De-
     cember 1970.        ISSN 0036-8733 (print), 1946-7087 (electronic).         doi: https:
     //doi.org/10.1038/scientificamerican1270-110.        URL https://doi.org/10.1038/
     scientificamerican1270-110.
[27] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian,
     Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama
     3 herd of models. arXiv preprint arXiv:2407.21783, 2024.
[28] Jacques Hadamard. Résolution d’une question relative aux déterminants. Bull. des sciences
     math., 2:240–246, 1893.
[29] Warwick Harvey. CSPLib problem 010: Social golfers problem. http://www.csplib.org/
     Problems/prob010.
[30] Holger H Hoos. Sat-encodings, search space structure, and local search performance. In IJCAI,
     volume 99, pages 296–303, 1999.
[31] Xia Jiang, Jing Chen, Cong Zhang, Jie Gao, Chengpeng Hu, Chenhao Zhang, Yaoxin Wu, and
     Yingqian Zhang. Reasoning in a combinatorial and constrained world: Benchmarking llms on
     natural-language combinatorial optimization. arXiv preprint arXiv:2602.02188, 2026.
[32] Haocheng Ju and Bin Dong. Ai for mathematics: Progress, challenges, and prospects. arXiv
     preprint arXiv:2601.13209, 2026.
[33] Richard M. Karp. Reducibility among Combinatorial Problems, pages 85–103. Springer US,
     Boston, MA, 1972. ISBN 978-1-4684-2001-2. doi: 10.1007/978-1-4684-2001-2_9. URL
     https://doi.org/10.1007/978-1-4684-2001-2_9.
[34] Markus Kirchweger and Stefan Szeider. Sat modulo symmetries for graph generation. In 27th
     International Conference on Principles and Practice of Constraint Programming (CP 2021),
     pages 34–1. Schloss Dagstuhl–Leibniz-Zentrum für Informatik, 2021.
[35] Markus Kirchweger and Stefan Szeider. Sat modulo symmetries for graph generation and
     enumeration. ACM Transactions on Computational Logic, 25(3):1–30, 2024.
[36] C. Dudley Langford. Problem. The Mathematical Gazette, 42(341):228–228, 1958. doi:
     10.2307/3610395.
[37] Christophe Lecoutre and Nicolas Szczepanski. Pycsp3: modeling combinatorial constrained
     problems in python. arXiv preprint arXiv:2009.00326, 2020.
[38] Xiaozhe Li, Xinyu Fang, Shengyuan Ding, Linyang Li, Haodong Duan, Qingwen Liu, and Kai
     Chen. Np-engine: Empowering optimization reasoning in large language models with verifiable
     synthetic np problems. arXiv preprint arXiv:2510.16476, 2025.


                                               11
[39] Jingcong Liang, Shijun Wan, Xuehai Wu, Yitong Li, Qianglong Chen, Duyu Tang, Siyuan
     Wang, and Zhongyu Wei. Hardcorelogic: Challenging large reasoning models with long-tail
     logic puzzle games. arXiv preprint arXiv:2510.12563, 2025.
[40] Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter
     Clark, and Yejin Choi. Zebralogic: On the scaling limits of llms for logical reasoning. arXiv
     preprint arXiv:2502.01100, 2025.
[41] J. A. Lindon. Anti-magic squares. Recreational Mathematics Magazine, (7):16–19, February
     1962.
[42] Qiuyang Mang, Wenhao Chai, Zhifei Li, Huanzhi Mao, Shang Zhou, Alexander Du, Hanchen
     Li, Shu Liu, Edwin Chen, Yichuan Wang, et al. Frontiercs: Evolving challenges for evolving
     intelligence. arXiv preprint arXiv:2512.15699, 2025.
[43] W Mantel. Problem 28, wiskundige opgaven. 1907.
[44] Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad
     Farajtabar. Gsm-symbolic: Understanding the limitations of mathematical reasoning in large
     language models. arXiv preprint arXiv:2410.05229, 2024.
[45] Jan Mycielski. Sur le coloriage des graphs. In Colloquium Mathematicae, volume 3, pages
     161–162, 1955.
[46] OpenAI. Gpt-5.5 system card. Technical report, OpenAI, April 2026. URL https://openai.
     com/index/gpt-5-5-system-card/. Accessed: 2026-04-27.
[47] Shishir G Patil, Huanzhi Mao, Fanjia Yan, Charlie Cheng-Jie Ji, Vishnu Suresh, Ion Stoica, and
     Joseph E Gonzalez. The berkeley function calling leaderboard (bfcl): From tool use to agentic
     evaluation of large language models. In Forty-second International Conference on Machine
     Learning, 2025.
[48] Qwen Team. Qwen3.6-Plus: Towards real world agents, April 2026. URL https://qwen.ai/
     blog?id=qwen3.6. Accessed: 2026-04-28.
[49] F. P. Ramsey. On a problem of formal logic. Proceedings of the London Mathematical
     Society, s2-30(1):264–286, 1930. doi: https://doi.org/10.1112/plms/s2-30.1.264. URL https:
     //londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms/s2-30.1.264.
[50] Alexander Rosa et al. On certain valuations of the vertices of a graph. In Theory of Graphs
     (Internat. Symposium, Rome, pages 349–355, 1966.
[51] John Slaney, Masayuki Fujita, and Mark Stickel. Automated reasoning and exhaustive search:
     Quasigroup existence problems. Computers & mathematics with applications, 29(2):115–132,
     1995.
[52] Weiwei Sun, Shengyu Feng, Shanda Li, and Yiming Yang. Co-bench: Benchmarking language
     model agents in algorithm search for combinatorial optimization. In Proceedings of the AAAI
     Conference on Artificial Intelligence, volume 40, pages 33126–33134, 2026.
[53] Jianheng Tang, Qifan Zhang, Yuhan Li, Nuo Chen, and Jia Li. Grapharena: Evaluating and
     exploring large language models on graph computation. arXiv preprint arXiv:2407.00379,
     2024.
[54] Kimi Team. Kimi k2: Open agentic intelligence. 2025. URL https://arxiv.org/abs/
     2507.20534. Referenced for Kimi K2.6; techincal report for version K2.
[55] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers
     on the putnam mathematical competition. Advances in Neural Information Processing Systems,
     37:11545–11569, 2024.
[56] Paul Turán. On an external problem in graph theory. Mat. Fiz. Lapok, 48:436–452, 1941.


                                                12
[57] Bartel Leendert Van der Waerden. Beweis einer baudetschen vermutung. Nieuw Arch. Wiskunde,
     15:212–216, 1927.
[58] Pascal Van Hentenryck. Constraint satisfaction in logic programming. 1989.
[59] Anjiang Wei, Yuheng Wu, Yingjia Wan, Tarun Suresh, Huanmi Tan, Zhanke Zhou, Sanmi
     Koyejo, Ke Wang, and Alex Aiken. Satbench: Benchmarking llms’ logical reasoning via
     automated puzzle generation from sat formulas. In Proceedings of the 2025 Conference on
     Empirical Methods in Natural Language Processing, pages 33820–33837, 2025.
[60] Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid
     Shwartz-Ziv, Neel Jain, Khalid Saifullah, Sreemanti Dey, et al. Livebench: A challenging,
     contamination-limited llm benchmark. arXiv preprint arXiv:2406.19314, 2024.
[61] xAI.           Grok 4 model card,               2025.        URL https://data.x.ai/
     2025-08-20-grok-4-model-card.pdf.               Referenced for Grok 4.2; technical report
     for version 4. Accessed: 2026-04-28.
[62] Zhiqiu Xu, Shibo Jin, Shreya Arya, and Mayur Naik. Mathduels: Evaluating llms as problem
     posers and solvers. arXiv preprint arXiv:2604.21916, 2026.
[63] Chang Yang, Ruiyu Wang, Junzhe Jiang, Qi Jiang, Qinggang Zhang, Yanchen Deng, Shuxin
     Li, Shuyue Hu, Bo Li, Florian T Pokorny, et al. Nondeterministic polynomial-time problem
     challenge: An ever-scaling reasoning benchmark for llms. arXiv preprint arXiv:2504.11239,
     2025.
[64] F. YATES. Incomplete randomized blocks. Annals of Eugenics, 7(2):121–140, 1936. doi:
     https://doi.org/10.1111/j.1469-1809.1936.tb02134.x. URL https://onlinelibrary.wiley.
     com/doi/abs/10.1111/j.1469-1809.1936.tb02134.x.
[65] Takayuki Yato and Takahiro Seta. Complexity and completeness of finding another solution and
     its application to puzzles. IEICE TRANSACTIONS on Fundamentals, E86-A(5):1052–1060,
     May 2003.
[66] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
     formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.


A    Implementation Details
This appendix records the implementation choices needed to reproduce the generation and evaluation
contract.

Generation. For pysms graph problems we solve with PySAT/Cadical and bypass smsg’s canonical-
form filter, which produced false negatives on non-canonical valid graphs. For pycsp problems we
use the upstream-recommended backend (Cadical, z3, pycosat, or AbsCon) per type. Each candidate
instance is bounded by a 3600 s reference-solver cap; timeouts are dropped rather than released.
Generation parallelizes across CPU workers with per-worker checkpointing, so a profile can resume
without duplicating accepted instances.

Sandbox. execute_python dispatches each tool call to a fresh subprocess in a pinned virtualenv
with the Python standard library plus python-sat, pycosat, and z3-solver==4.13.0.0. Network
access and outbound subprocess spawning are blocked, and the math_constraint, pycsp3, and
pysms packages are excluded so models cannot reach the benchmark verifier. Per-call wall time
defaults to 15 s with a 60 s hard cap; stdout/stderr are truncated at 32 KB. Traces were audited for
sandbox-escape attempts; none were found.

Force-submit fallback. If a tool-enabled run reaches the round cap without calling
submit_answer, the evaluator parses the final natural-language response as a fallback: strict JSON,
then fenced JSON blocks (last valid block when several appear), then brace-balanced extraction
anchored at the first "satisfiable" key. The model is not told the round budget, so logged
tool_call_chain sequences can be replayed at smaller caps for the SIM @k analysis.


                                                13
Verification. For SAT claims, the submitted solution is added as hard unit constraints on top
of the original encoding and re-solved by the reference backend (PySAT/Cadical only for pysms);
witnesses are accepted up to backend-level isomorphism. For UNSAT claims, only polarity is checked.
Hinted M ATH C ONSTRAINT-E ASY instances additionally require compliance with the fixed partial
assignment. Each verification attempt has a 60 s hard timeout, recorded in the trace rather than treated
as accepted.


System prompt. Identical across all models and conditions. The italicized block is concatenated
only in the tools condition.

You are solving constraint satisfaction problems. Analyze the problem
carefully and determine:
1. Whether the problem is satisfiable (SAT) or unsatisfiable (UNSAT)
2. If satisfiable, provide a valid solution

Respond with a JSON object in the following format:
{
    "satisfiable": true/false,
    "solution": [list of values] or null if unsatisfiable,
    "reasoning": "Brief explanation of your reasoning"
}

Important:
- For satisfiability, true means a solution exists, false means it’s
  mathematically impossible
- Solutions should be provided as a list of integers
- Be precise with your answer - incorrect solutions will be rejected
[tools-only:]
You may optionally call tools before submitting your final answer:
- execute_python(code, timeout_seconds): run Python code in an isolated
  subprocess. Standard library plus pysat/z3/pycosat available; cannot
  import math_constraint/pycsp3/pysms, access network, or spawn
  subprocesses. Default timeout 15s, max 60s.
- submit_answer(satisfiable, solution, reasoning): submit your final
  answer.
If you use tools, always finish by calling submit_answer.


B     Methodological Notes

This appendix collects three points of justification for methodological design choices beyond what
the main text provides.


B.1   Frozen dataset, single generator seed

M ATH C ONSTRAINT is released as two frozen slices (E ASY and M ATH C ONSTRAINT) generated
under fixed profile seeds. We do not resample per evaluation, and we do not release multiple seeded
draws of the same profile. Frozen instances are necessary for reproducible comparison across future
models, and multi-seed generation would leak difficulty variance into every reported number since
two draws from the same profile produce slices of different empirical hardness. Adaptivity enters
through explicit refresh cycles described in Section 3.4 rather than per-evaluation resampling, and
the E ASY→M ATH C ONSTRAINT progression is the first such refresh. Model-side, all results use
temperature 0 with one run per (model, instance, condition) cell, following standard practice for
frontier-API benchmarks. With n = 329 instances, the binomial standard error is at most 2.8 pp
at 50% accuracy and below 2.3 pp at top-model accuracy levels, well under the gaps driving the
headline claims.


                                                  14
B.2   The frontier-failure admission filter

The adaptivity loop in Figure 3 admits a candidate only if at least one frontier model fails it. This is a
common sense choice because a refresh whose new instances are already solved by the cohort would
not restore discrimination, which is the entire purpose of running the loop. The filter does couple the
released slice to the cohort used at construction time, so a model evaluated post-release stands in a
slightly different relationship to the benchmark than a cohort member; we treat this as a property of
filter-based adaptive evaluation rather than an artifact specific to M ATH C ONSTRAINT.

B.3   SIM @k as a lower bound

Models are never told their tool-round budget; the cap of 8 is enforced by the harness, not communi-
cated in the prompt (Section A). SIM @k takes the traces produced under that condition and truncates
them to at most k rounds. It is therefore a lower bound in two ways. First, the original 8-round runs
themselves were budget-unaware, so the trajectories include exploration that a budget-aware policy
might prune. Second, truncating at k < 8 scores a strictly shorter prefix of an already budget-unaware
trace; a model told in advance that it had k rounds could allocate differently and likely do better. We
retain this framing intentionally. Native-budget reruns at every k for every model would multiply
evaluation cost without changing the qualitative finding, which is that measured tool-use capability
can collapse by tens of points as the cap shrinks (S ONNET: 70.5 → 33.7 at k = 4). A floor that low
is informative regardless of whether budget-aware policies could lift it. We therefore treat SIM @k as
a cheap, conservative diagnostic that exposes policy structure invisible to a single-budget number,
and leave native-budget studies to future work that targets specific models rather than the full cohort.

B.4   Thin-tail problem types

A handful of problem types in M ATH C ONSTRAINT are represented by very few instances. Per-type
accuracies for n ≤ 2 types should be read as existence proofs rather than rates; the benchmark is not
designed to support per-type significance testing on these tail entries. We retain them to preserve
registry coverage of qualitatively distinct combinatorial phenomena that would otherwise drop out of
the headline aggregates.


C     Evaluation Metrics

Let D be an evaluated dataset and let yi ∈ {SAT, UNSAT} be the solver-certified polarity of instance
i. The evaluator parses a model output into a submitted polarity ŷi and, for SAT claims, an optional
witness x̂i . Let
                                           pi = 1{ŷi = yi }
denote polarity correctness, and let
  vi = 1{(ŷi = UNSAT ∧ yi = UNSAT) ∨ (ŷi = SAT ∧ yi = SAT ∧ x̂i satisfies the verifier)}
denote end-to-end verifier acceptance.

Accuracy and SAT Acc.        The main accuracy metric is verifier acceptance:
                                                         1 X
                                       Accuracy(D) =         vi .
                                                        |D|
                                                             i∈D

SAT ACC . is polarity accuracy:
                                                         1 X
                                       SATAcc(D) =           pi .
                                                        |D|
                                                            i∈D

Thus SAT ACC . can be high even when accuracy is low: a model may correctly decide that a SAT
instance is satisfiable but still submit an invalid witness. On UNSAT instances, correct polarity is
sufficient for verifier acceptance because no witness is required.


                                                   15
Tool-budget replay. For a logged tool-enabled trace i, let ri be the number of tool rounds used
before the accepted final submission in the original run. We report
                                                1 X
                               sim@k(D) =               vi 1{ri ≤ k}.
                                               |D|
                                                          i∈D

This is a conservative replay metric: it truncates observed traces and applies the same parsing and
verification logic, but it does not allow a model to adapt its strategy after being told a smaller budget.
Consequently SIM @k is best interpreted as a lower bound on what the same model might achieve if
run natively with a k-round budget and an adapted policy.

Force-submit and rescue. An explicit submission is an instance in which the model calls
submit_answer. A force-submitted instance is one with no explicit submission, so the evalua-
tor parses the final natural-language response. The rescue rate is
                                            P
                                                 vi 1{force-submitted i}
                              RescueRate = Pi                            ,
                                                 i 1{force-submitted i}

with value 0 when the denominator is zero.

Efficiency and behavior. Token, latency, and cost columns are per-instance means from provider
usage logs. Tool calls and rounds are per-instance means; execute and submit columns are total
tool-call counts. Failure-bucket tables partition non-accepted runs after parsing and verification,
while stratification tables recompute Accuracy on SAT, UNSAT, pycsp, and pysms subsets.

D     Extended Dataset Description
This section expands the dataset-level statistics used in the main text. We report M ATH C ONSTRAINT
first, then M ATH C ONSTRAINT-E ASY, matching the order of the experiments.

Table 5: Extended dataset difficulty statistics. Solver-time columns are reference generation-time
wall time in seconds. Structural columns report medians and 90th percentiles from each instance’s
recorded difficulty metadata; search-space values are log10 of the recorded search-space proxy.
                                     Backend        Solver time (s)     Variables     Constraints    log10 space
Dataset                         n    CP/SMS     p50      p90     p99    p50    p90    p50     p90    p50      p90
M ATH C ONSTRAINT-E ASY     266      110/156   0.20      1.79    11.8   17.5   42.1   16.5    263    8.68    27.9
M ATH C ONSTRAINT           329      227/102   2.52      75.6     653   46.0    210    154    949    18.7     106



                     Table 6: Problem-type composition of M ATH C ONSTRAINT.
Problem type               n        SAT   UNSAT         Problem type                         n      SAT     UNSAT
all_interval                5         5         0       number_partitioning                  10      10         0
antimagic_square            4         4         0       ortholatin                            2       2         0
bibd                        9         9         0       pysms_chromatic_girth                47      20        27
costas_array                8         8         0       pysms_clique_coloring                 4       4         0
debruijn                    1         1         0       pysms_combined_graph                  1       0         1
golomb                      5         5         0       pysms_contains_cliques                1       0         1
graceful_graph             21        21         0       pysms_degree_bounds                   2       2         0
graph_k_coloring           22        18         4       pysms_girth_degree                   32      15        17
hadamard                    4         4         0       pysms_graph_builder                   6       2         4
hamilton_cycle              1         0         1       pysms_independent_connectivity        6       6         0
knight_tour                 4         4         0       pysms_min_girth                       1       1         0
langford                    9         9         0       pysms_mtf                             1       1         0
latin_square_completion     4         4         0       pysms_ramsey                          1       0         1
low_autocorrelation        14        14         0       quasigroup_idempotent                 5       2         3
magic_sequence              1         0         1       queens                                6       6         0
magic_square                2         2         0       ramsey                               14      13         1
max_clique                 26        15        11       social_golfers                       16      16         0
max_independent_set        22         1        21       sudoku                                2       2         0
non_transitive_dice         2         2         0       van_der_waerden                       3       0         3
                                                        vertex_cover                          5       0         5




                                                        16
                    Table 7: Problem-type composition of M ATH C ONSTRAINT-E ASY.
Problem type                       n    SAT   UNSAT     Problem type                     n     SAT    UNSAT
all_interval                    12       12       0     pysms_degree_bounds              12     11        1
costas_array                     9        9       0     pysms_girth_degree               12      6        6
golomb                           6        6       0     pysms_graph_builder              12      6        6
graceful_graph                   8        8       0     pysms_independent_connectivity   12     12        0
knight_tour                      4        4       0     pysms_min_connectivity           12     12        0
langford                         8        6       2     pysms_min_degree                 12     12        0
low_autocorrelation             12       12       0     pysms_min_girth                  12     12        0
magic_sequence                  12       10       2     pysms_mtf                        12     12        0
pigeons                         12        0      12     pysms_num_edges_bounds           12     12        0
pysms_chromatic_girth           12        9       3     queens                           12     12        0
pysms_clique_coloring           12       12       0     ramsey                           12      8        4
pysms_combined_graph            12        0      12     sudoku                            3      3        0
pysms_contains_cliques          12        0      12




Table 8: No-tools hint stratification on M ATH C ONSTRAINT-E ASY. Entries are verifier accuracy
percentages for hinted SAT, unhinted SAT, and UNSAT instances.
           Model                                 Hinted SAT            Unhinted SAT           UNSAT
           GPT-5.5                                      76                      95               95
           CLAUDE - OPUS -4.7                           75                      93               90
           CLAUDE -4.6- SONNET                          66                      80               83
           GEMINI -3.1- PRO                             75                      91               88
           GEMINI -3.1- FLASH - LITE                    57                      81               85
           GROK -4.20                                   75                      91               92
           DEEPSEEK - V 4- PRO                          72                      90               88
           DEEPSEEK - V 4- FLASH                        61                      79               90
           QWEN 3.6- PLUS                               70                      86               92
           KIMI - K 2.6                                 62                      87               85
           GPT- OSS -120 B                              53                      74               88
           LLAMA -3.3-70 B - INSTRUCT                    3                      26               52




Table 9: Tool-enabled hint stratification on M ATH C ONSTRAINT-E ASY. Entries are verifier accuracy
percentages for hinted SAT, unhinted SAT, and UNSAT instances.
           Model                                 Hinted SAT            Unhinted SAT           UNSAT
           GPT-5.5                                      83                      98               95
           CLAUDE - OPUS -4.7                           81                      99               92
           CLAUDE -4.6- SONNET                          84                      98               85
           GEMINI -3.1- PRO                             83                     100               90
           GEMINI -3.1- FLASH - LITE                    82                      99               87
           GROK -4.20                                   74                      96               95
           DEEPSEEK - V 4- PRO                          58                      79               83
           DEEPSEEK - V 4- FLASH                        60                      81               75
           QWEN 3.6- PLUS                               79                      97               90
           KIMI - K 2.6                                 72                      91               85
           GPT- OSS -120 B                              52                      80               90
           LLAMA -3.3-70 B - INSTRUCT                    5                      17               85




                                                         17
E       Models, Configurations, and Pricing
Model configuration. All models use temperature 0, max_tokens= 16,384, and OpenRouter
routing with fallbacks. The tool condition allows up to eight tool-calling rounds. Reasoning
controls follow provider-native options through OpenRouter (configs/models.yaml): models
exposing a discrete reasoning-effort level run at the maximum (GEMINI -3.1- FLASH - LITE at medium);
Anthropic’s API uses a budget_tokens cap on thinking tokens rather than a discrete effort level, set
to 8k for CLAUDE - OPUS -4.7 and unset for CLAUDE -4.6- SONNET; remaining models run with no
reasoning configuration.

Frontier cohort. Throughout this paper, “frontier” refers to a fixed cohort of six models used
both for the admission filter (Section Section B.2) and for cohort-level summary statistics: GPT-
5.5, C LAUDE -O PUS -4.7, C LAUDE -4.6-S ONNET, G ROK -4.20, G EMINI -3.1-P RO, and G EMINI -
3.1-F LASH -L ITE. The remaining six evaluated models (D EEP S EEK -V4-P RO, D EEP S EEK -V4-
F LASH, Q WEN 3.6-P LUS, K IMI -K2.6, GPT-OSS-120B, L LAMA -3.3-70B-I NSTRUCT) are reported
alongside the frontier cohort but did not participate in admission. Future refreshes will update this
cohort and document the change in the corresponding release notes.

Model    slugs. The   exact     model   slugs    are   openai/gpt-5.5-20260423,
anthropic/claude-opus-4.7,               anthropic/claude-4.6-sonnet-20260217,
google/gemini-3.1-pro-preview-20260219,
google/gemini-3.1-flash-lite-preview-20260303,         x-ai/grok-4.20-20260309,
deepseek/deepseek-v4-pro-20260423,         deepseek/deepseek-v4-flash-20260423,
qwen/qwen3.6-plus-04-02,                         moonshotai/kimi-k2.6-20260420,
openai/gpt-oss-120b:free, and meta-llama/llama-3.3-70b-instruct.

Table 10: Model configuration and token pricing. Prices are USD per million tokens from
configs/model_pricing.yaml, correct as of 2026-04-30. Dashes indicate models without an
explicit paid price entry in the pricing file.
Model                        Reasoning config                                      Input       Output
GPT-5.5                      effort=high, exclude=False                                5           30
CLAUDE - OPUS -4.7           max_tokens=8000, exclude=False                            5           25
CLAUDE -4.6- SONNET          none                                                      3           15
GEMINI -3.1- PRO             effort=high, exclude=False                                2           12
GEMINI -3.1- FLASH - LITE    effort=medium, exclude=False                           0.25          1.5
GROK -4.20                   effort=high, exclude=False                                2            6
DEEPSEEK - V 4- PRO          effort=high, exclude=False                            0.435         0.87
DEEPSEEK - V 4- FLASH        none                                                    0.14        0.28
QWEN 3.6- PLUS               effort=high, exclude=False                            0.325         1.95
KIMI - K 2.6                 effort=high, exclude=False                           0.7448        4.655
GPT- OSS -120 B              none                                                      –           –
LLAMA -3.3-70 B - INSTRUCT   none                                                      –           –




F       Extended Experimental Results
The following tables are audit material for the main results: efficiency, token composition, tool
behavior, force-submit behavior, failure categories, stratification, and per-type accuracy.




                                                  18
Table 11: Tool-budget sensitivity on the full 329-instance M ATH C ONSTRAINT release. SIM @k is a
conservative replay metric defined in Section C; SIM @8 is the full tool-enabled setting.
                       Model                         SIM @1 SIM @2 SIM @4 SIM @8

                       GPT-5.5                         19.5   41.0   63.2       80.9
                       CLAUDE - OPUS -4.7               3.3   30.4   59.3       77.5
                       CLAUDE -4.6- SONNET             0.0     6.1   33.7       70.5
                       GEMINI -3.1- PRO                0.9    18.2   50.2       72.9
                       GEMINI -3.1- FLASH - LITE        0.6   4.9    28.0       62.3
                       GROK -4.20                      7.9    28.0   45.3       66.6
                       DEEPSEEK - V 4- PRO              4.3   10.3   23.1       41.3
                       DEEPSEEK - V 4- FLASH            3.0    7.0   23.1       36.5
                       QWEN 3.6- PLUS                   0.3   14.0   41.0       66.3
                       KIMI - K 2.6                     2.7   10.9   28.9       59.9
                       GPT- OSS -120 B                 13.1   23.4   31.0       36.5
                       LLAMA -3.3-70 B - INSTRUCT       1.5   31.9   31.9       31.9




Table 12: No-tools evaluation efficiency on the full 329-instance M ATH C ONSTRAINT release. Token
and latency columns are per-instance averages from API usage logs; cost is dollars per instance from
provider-reported billing.
         Model                                     Tokens            Lat. (s)           Cost
         GPT-5.5                                   10880              174.8            0.282
         CLAUDE - OPUS -4.7                        18170              125.6            0.425
         CLAUDE -4.6- SONNET                        5420               51.1            0.067
         GEMINI -3.1- PRO                          13221              129.7            0.141
         GEMINI -3.1- FLASH - LITE                  3994                9.2            0.005
         GROK -4.20                                21899              235.9            0.068
         DEEPSEEK - V 4- PRO                       23822              778.9            0.073
         DEEPSEEK - V 4- FLASH                     22295              275.0            0.006
         QWEN 3.6- PLUS                            52707              976.0            0.101
         KIMI - K 2.6                              26030              936.9            0.100
         GPT- OSS -120 B                            1353                21.5           0.000
         LLAMA -3.3-70 B - INSTRUCT                 2365                38.0           0.001




Table 13: Tool-enabled evaluation efficiency on the full 329-instance M ATH C ONSTRAINT release.
Token and latency columns are per-instance averages from API usage logs; cost is dollars per instance
from provider-reported billing.
         Model                                     Tokens            Lat. (s)           Cost
         GPT-5.5                                   12081               91.0            0.151
         CLAUDE - OPUS -4.7                        23441               68.3            0.208
         CLAUDE -4.6- SONNET                       35046               94.0            0.174
         GEMINI -3.1- PRO                          23181              115.0            0.132
         GEMINI -3.1- FLASH - LITE                 33977               48.8            0.015
         GROK -4.20                                22526              131.9            0.039
         DEEPSEEK - V 4- PRO                       32361              362.5            0.058
         DEEPSEEK - V 4- FLASH                     21711              283.3            0.004
         QWEN 3.6- PLUS                            35036              211.3            0.027
         KIMI - K 2.6                              37166              704.5            0.064
         GPT- OSS -120 B                           12717                78.3           0.000
         LLAMA -3.3-70 B - INSTRUCT                 4012                27.3           0.001




                                                       19
Table 14: No-tools evaluation efficiency on M ATH C ONSTRAINT-E ASY (n = 266). Token and
latency columns are per-instance averages from API usage logs; cost is dollars per instance from
provider-reported billing.
         Model                                 Tokens            Lat. (s)             Cost
         GPT-5.5                                3249                48.9              0.091
         CLAUDE - OPUS -4.7                     4548                30.6              0.105
         CLAUDE -4.6- SONNET                    2222                23.2              0.029
         GEMINI -3.1- PRO                       5097                51.5              0.052
         GEMINI -3.1- FLASH - LITE              2330                 7.0              0.003
         GROK -4.20                             8102                89.1              0.047
         DEEPSEEK - V 4- PRO                    7620              242.5               0.025
         DEEPSEEK - V 4- FLASH                  6693               80.3               0.002
         QWEN 3.6- PLUS                        21593              421.2               0.042
         KIMI - K 2.6                           8593              334.0               0.034
         GPT- OSS -120 B                         955                22.5              0.000
         LLAMA -3.3-70 B - INSTRUCT             1580                33.0              0.001




Table 15: Tool-enabled evaluation efficiency on M ATH C ONSTRAINT-E ASY (n = 266). Token and
latency columns are per-instance averages from API usage logs; cost is dollars per instance from
provider-reported billing.
         Model                                 Tokens            Lat. (s)             Cost
         GPT-5.5                                2126                21.9              0.035
         CLAUDE - OPUS -4.7                     6249                19.7              0.058
         CLAUDE -4.6- SONNET                   13493                36.4              0.068
         GEMINI -3.1- PRO                       6549                48.2              0.047
         GEMINI -3.1- FLASH - LITE              8069                14.5              0.005
         GROK -4.20                             7815                48.3              0.027
         DEEPSEEK - V 4- PRO                   10499              314.2               0.027
         DEEPSEEK - V 4- FLASH                 12620              174.6               0.002
         QWEN 3.6- PLUS                         9072               68.8               0.008
         KIMI - K 2.6                           7864              225.8               0.017
         GPT- OSS -120 B                        5022                40.5              0.000
         LLAMA -3.3-70 B - INSTRUCT             1853                11.3              0.000




Table 16: No-tools token breakdown on the full 329-instance M ATH C ONSTRAINT release. Entries
are per-instance averages; completion tokens are the response-length proxy.
     Model                            Prompt            Compl.              Reason.     Cached
     GPT-5.5                           1761              9119                 8849            113
     CLAUDE - OPUS -4.7                1438             16732                 2185              0
     CLAUDE -4.6- SONNET               1161              4259                    0              0
     GEMINI -3.1- PRO                  1717             11504                11082              0
     GEMINI -3.1- FLASH - LITE         1029              2965                 1849              0
     GROK -4.20                         909             20991                18967            162
     DEEPSEEK - V 4- PRO               1236             22586                21161            226
     DEEPSEEK - V 4- FLASH             1100             21195                16896            288
     QWEN 3.6- PLUS                     924             51783                48207              0
     KIMI - K 2.6                      1288             24743                17886            144
     GPT- OSS -120 B                    849               504                  274            172
     LLAMA -3.3-70 B - INSTRUCT        1090              1276                    0             18




                                                   20
Table 17: Tool-enabled token breakdown on the full 329-instance M ATH C ONSTRAINT release.
Entries are per-instance averages; completion tokens are the response-length proxy.
        Model                                Prompt            Compl.            Reason.              Cached
        GPT-5.5                               8051               4030              2018                2281
        CLAUDE - OPUS -4.7                   18894               4547               191                   0
        CLAUDE -4.6- SONNET                  29344               5702                 0                   0
        GEMINI -3.1- PRO                     14349               8831              5272                1554
        GEMINI -3.1- FLASH - LITE            27238               6740               979                7220
        GROK -4.20                           12629               9897              6361                5959
        DEEPSEEK - V 4- PRO                  23648               8713              3490                9283
        DEEPSEEK - V 4- FLASH                15716               5995              1850                3589
        QWEN 3.6- PLUS                       25594               9442              3643                   0
        KIMI - K 2.6                         24213              12953              6078                8560
        GPT- OSS -120 B                      10815               1902               310                7231
        LLAMA -3.3-70 B - INSTRUCT            3119                893                 0                   0




Table 18: Tool-use behavior on M ATH C ONSTRAINT-E ASY. Calls and rounds are per-instance
averages; execute and submit are total tool-call counts. Submit and forced are instance rates in percent.
Submit is the explicit submit_answer instance rate; forced is the evaluator forced_submit flag
rate." Also change both column headers from "Forced %" to "Flagged %
Model                                Calls    Rounds         Execute    Submit             Submit %        Forced %
GPT-5.5                              0.73        1.41           111        83                  31.2             2.6
CLAUDE - OPUS -4.7                   2.08        2.09           295       259                  97.4             1.9
CLAUDE -4.6- SONNET                  3.57        3.77           753       197                  74.1            25.6
GEMINI -3.1- PRO                     2.68        2.68           455       258                  97.0             2.3
GEMINI -3.1- FLASH - LITE            3.13        3.17           592       241                  90.6             7.9
GROK -4.20                           2.83        2.87           534       218                  82.0            13.9
DEEPSEEK - V 4- PRO                  2.63        2.93           539       161                  60.5            16.9
DEEPSEEK - V 4- FLASH                3.35        3.53           693       199                  74.8             6.0
QWEN 3.6- PLUS                       2.79        2.85           500       243                  91.4             5.6
KIMI - K 2.6                         2.73        2.74           476       248                  93.2             0.8
GPT- OSS -120 B                      2.51        3.35           667         1                   0.4            18.4
LLAMA -3.3-70 B - INSTRUCT           1.89        1.89           236       266                 100.0             0.0




Table 19: Tool-use behavior on the full 329-instance M ATH C ONSTRAINT release. Calls and rounds
are per-instance averages; execute and submit are total tool-call counts. Submit and forced are
instance rates in percent. Submit is the explicit submit_answer instance rate; forced is the evaluator
forced_submit flag rate." Also change both column headers from "Forced %" to "Flagged %
Model                                Calls    Rounds         Execute    Submit             Submit %        Forced %
GPT-5.5                              2.87        3.07           703       241                  73.3             4.0
CLAUDE - OPUS -4.7                   3.65        3.65           915       287                  87.2            11.2
CLAUDE -4.6- SONNET                  5.34        5.39          1543       215                  65.3            34.0
GEMINI -3.1- PRO                     4.25        4.26          1130       267                  81.2            11.2
GEMINI -3.1- FLASH - LITE            5.31        5.34          1525       222                  67.5            31.9
GROK -4.20                           4.50        4.53          1270       209                  63.5            29.8
DEEPSEEK - V 4- PRO                  4.49        4.72          1303       173                  52.6            11.6
DEEPSEEK - V 4- FLASH                3.95        4.33          1150       149                  45.3             9.7
QWEN 3.6- PLUS                       4.56        4.59          1255       244                  74.2            13.1
KIMI - K 2.6                         5.20        5.22          1496       213                  64.7            14.3
GPT- OSS -120 B                      3.96        4.62          1300         4                   1.2            35.9
LLAMA -3.3-70 B - INSTRUCT           1.84        1.84           278       329                 100.0             0.0




                                                        21
Table 20: Tool-call composition on M ATH C ONSTRAINT TOOLS. Fractions of execute_python
calls categorized by primary library import or use; classification follows priority order pysat → z3
→ pycosat → networkx → brute-force (loops without solver imports) → other. C ALLS is the total
number of execute_python invocations in MC traces.
         Model                          Calls pysat z3 pycosat networkx brute-force other
         GPT-5.5                          703         21     20         0               1            47             10
         CLAUDE - OPUS -4.7               915         26      8         0               3            54             8
         CLAUDE -4.6- SONNET             1542         22     8          0                3           60             7
         GEMINI -3.1- PRO                1130         32     26         0                8           26             8
         GEMINI -3.1- FLASH - LITE       1525          7     13         0               11           61              9
         GROK -4.20                      1270          4     44         0                8           39             5
         DEEPSEEK - V 4- PRO             1297         35     24         1               2            36             3
         DEEPSEEK - V 4- FLASH           1143         19     24         1                1           49             6
         QWEN 3.6- PLUS                  1252         29     18         0               1            50             2
         KIMI - K 2.6                    1489         21     21         2               1            49              7
         GPT- OSS -120 B                  106          1     18         0               4            55             23
         LLAMA -3.3-70 B - INSTRUCT       275          1      0         0               50           48              1




Table 21: Force-submit fallback analysis for tool-enabled runs on the full 329-instance M ATH C ON -
STRAINT release. Explicit submissions, force submissions, and rescue rate are defined in Section C.
If every force-submitted instance is scored incorrect, the top-three model set is unchanged, though its
order becomes CLAUDE - OPUS -4.7, GEMINI -3.1- PRO, GPT-5.5.
Model                                 Total       Explicit              Forced           Forced correct             Rescue (%)
GPT-5.5                                329                 241               88                      67                   76.1
CLAUDE - OPUS -4.7                     329                 287               42                      24                   57.1
CLAUDE -4.6- SONNET                    329                 215              114                      56                   49.1
GEMINI -3.1- PRO                       329                 267               62                      23                   37.1
GEMINI -3.1- FLASH - LITE              329                 222              107                      44                   41.1
GROK -4.20                             329                 209              120                      58                   48.3
DEEPSEEK - V 4- PRO                    329                 173              156                      32                   20.5
DEEPSEEK - V 4- FLASH                  329                 149              180                      19                   10.6
QWEN 3.6- PLUS                         329                 244               85                      32                   37.6
KIMI - K 2.6                           329                 213              116                      41                   35.3
GPT- OSS -120 B                        329                   4              325                      118                  36.3
LLAMA -3.3-70 B - INSTRUCT             329                 329                0                        0                   0.0




Table 22: No-tools failure buckets on the full 329-instance M ATH C ONSTRAINT release. Accepted
counts are verifier-accepted answers; other columns partition non-accepted runs by the evaluator’s
failure bucket. Other includes API/content-filter buckets not shown separately.
                                              Wrong          Wrong                                          Max
Model                        Accept                                          Length          Parse                        Other
                                               pol.           sol.                                         rounds
GPT-5.5                        220               10                40              55           0              0             4
CLAUDE - OPUS -4.7             140               12                47             128           0              0             2
CLAUDE -4.6- SONNET             61               75               175              16           2              0             0
GEMINI -3.1- PRO               170               18                51              31          56              0             3
GEMINI -3.1- FLASH - LITE       82               73               169               5           0              0             0
GROK -4.20                     191              101                32               1           0              0             4
DEEPSEEK - V 4- PRO            130               20               32              135           2              0            10
DEEPSEEK - V 4- FLASH          112               49               90               68           6              0             4
QWEN 3.6- PLUS                 156               36               82                1          21              0            33
KIMI - K 2.6                   118               14               23              163           0              0            11
GPT- OSS -120 B                130              172                27              0            0              0             0
LLAMA -3.3-70 B - INSTRUCT      28               78               179              4           39              0             1




                                                            22
Table 23: Tool-enabled failure buckets on the full 329-instance M ATH C ONSTRAINT release. Accepted
counts are verifier-accepted answers; other columns partition non-accepted runs by the evaluator’s
failure bucket. Other includes API/content-filter buckets not shown separately.
                                               Wrong       Wrong                                   Max
Model                               Accept                                  Length   Parse                  Other
                                                pol.        sol.                                  rounds
GPT-5.5                                  266       7           44              10         0           0        2
CLAUDE - OPUS -4.7                       255      25           44               4         0           0        1
CLAUDE -4.6- SONNET                      232      25           70               1         1           0        0
GEMINI -3.1- PRO                         240      20           44               3         0          22        0
GEMINI -3.1- FLASH - LITE                205      39           83               1         0           1        0
GROK -4.20                               219      40           55               0         0          14        1
DEEPSEEK - V 4- PRO                      136      43           32              11         27         57       23
DEEPSEEK - V 4- FLASH                    120      24           37               9         36         44       59
QWEN 3.6- PLUS                           218      13           56               0          3         36        3
KIMI - K 2.6                             197      25           38              41          6         17        5
GPT- OSS -120 B                          120     130           70               0          0          9        0
LLAMA -3.3-70 B - INSTRUCT               105     171           53               0          0          0        0




Table 24: Witness gap on M ATH C ONSTRAINT no-tools. G AP is SAT polarity accuracy minus
end-to-end verifier accuracy. It measures how often a model decides existence correctly but fails to
construct a witness that survives exact verification (Section C). Sorted by gap descending.
                        Model                          SAT Acc. (%) Accuracy (%) Gap (pp)
                        LLAMA -3.3-70 B - INSTRUCT        62.9                 8.5         54.4
                        CLAUDE -4.6- SONNET               72.0                18.5         53.5
                        GEMINI -3.1- FLASH - LITE         76.3                24.9         51.4
                        DEEPSEEK - V 4- FLASH             61.4                34.0         27.4
                        QWEN 3.6- PLUS                    72.3                47.4         24.9
                        GEMINI -3.1- PRO                  67.2                51.7         15.5
                        CLAUDE - OPUS -4.7                56.8                42.6         14.3
                        GPT-5.5                           79.0                66.9         12.2
                        GROK -4.20                        67.8                58.1          9.7
                        DEEPSEEK - V 4- PRO               49.2                39.5          9.7
                        GPT- OSS -120 B                   47.7                39.5          8.2
                        KIMI - K 2.6                      42.9                35.9          7.0




Table 25: No-tools polarity and backend stratification on M ATH C ONSTRAINT-E ASY. Entries are
verifier accuracy percentages. CP denotes pycsp; SMS denotes pysms.
            Model                                SAT                UNSAT            CP              SMS
            GPT-5.5                               85                   95            75                97
            CLAUDE - OPUS -4.7                    84                   90            71                96
            CLAUDE -4.6- SONNET                   73                   83            51                92
            GEMINI -3.1- PRO                      83                   88            68                96
            GEMINI -3.1- FLASH - LITE             69                   85            45                92
            GROK -4.20                            83                   92            69                96
            DEEPSEEK - V 4- PRO                   81                   88            65                95
            DEEPSEEK - V 4- FLASH                 70                   90            58                86
            QWEN 3.6- PLUS                        78                   92            65                92
            KIMI - K 2.6                          75                   85            63                87
            GPT- OSS -120 B                       64                   88            43                88
            LLAMA -3.3-70 B - INSTRUCT            15                   52            22                24




                                                          23
Table 26: Tool-enabled polarity and backend stratification on M ATH C ONSTRAINT-E ASY. Entries are
verifier accuracy percentages. CP denotes pycsp; SMS denotes pysms.
        Model                           SAT            UNSAT            CP           SMS
        GPT-5.5                          91               95            84             97
        CLAUDE - OPUS -4.7               90               92            84             95
        CLAUDE -4.6- SONNET              91               85            84             94
        GEMINI -3.1- PRO                 92               90            86             95
        GEMINI -3.1- FLASH - LITE        90               87            83             94
        GROK -4.20                       85               95            80             92
        DEEPSEEK - V 4- PRO              68               83            65             77
        DEEPSEEK - V 4- FLASH            70               75            76             68
        QWEN 3.6- PLUS                   88               90            82             93
        KIMI - K 2.6                     82               85            77             86
        GPT- OSS -120 B                  66               90            47             88
        LLAMA -3.3-70 B - INSTRUCT       11               85            34             24




Table 27: No-tools polarity and backend stratification on the full 329-instance M ATH C ONSTRAINT
release. Entries are verifier accuracy percentages. CP denotes pycsp; SMS denotes pysms.
        Model                           SAT            UNSAT            CP           SMS
        GPT-5.5                          62               77            56             91
        CLAUDE - OPUS -4.7               45               38            33             64
        CLAUDE -4.6- SONNET              19               17            12             32
        GEMINI -3.1- PRO                 46               64            40             77
        GEMINI -3.1- FLASH - LITE        18               41            11             56
        GROK -4.20                       43               93            49             78
        DEEPSEEK - V 4- PRO              40               38            30             60
        DEEPSEEK - V 4- FLASH            29               46            21             64
        QWEN 3.6- PLUS                   43               56            35             75
        KIMI - K 2.6                     36               36            30             50
        GPT- OSS -120 B                  15               95            28             66
        LLAMA -3.3-70 B - INSTRUCT        1               25             3             21




Table 28: Tool-enabled polarity and backend stratification on the full 329-instance M ATH C ON -
STRAINT release. Entries are verifier accuracy percentages. CP denotes pycsp; SMS denotes
pysms.
        Model                           SAT            UNSAT            CP           SMS
        GPT-5.5                          75               95            75             94
        CLAUDE - OPUS -4.7               73               87            74             84
        CLAUDE -4.6- SONNET              66               80            72             68
        GEMINI -3.1- PRO                 70               79            73             74
        GEMINI -3.1- FLASH - LITE        54               82            60             68
        GROK -4.20                       56               91            62             77
        DEEPSEEK - V 4- PRO              41               42            41             42
        DEEPSEEK - V 4- FLASH            42               25            38             32
        QWEN 3.6- PLUS                   61               77            68             63
        KIMI - K 2.6                     57               67            63             54
        GPT- OSS -120 B                  21               71            22             70
        LLAMA -3.3-70 B - INSTRUCT        4               96            25             48




                                               24
                                        Table 29: Per-type no-tools performance on M ATH C ONSTRAINT. Each entry is Accuracy/SAT Acc. in percent.
     Problem type                     GPT-5.5 CLAUDE - OPUS -4.7 CLAUDE -4.6- SONNET GEMINI -3.1- PRO GEMINI -3.1- FLASH - LITE GROK -4.20 DEEPSEEK - V 4- PRO DEEPSEEK - V 4- FLASH QWEN 3.6- PLUS KIMI - K 2.6 GPT- OSS -120 B LLAMA -3.3-70 B - INSTRUCT

     all_interval                      20/100             20/100                20/80            20/100                   20/80       20/60               20/80                20/80          20/100       20/80          80/80                      0/100
     antimagic_square                   50/50                0/0                0/100               0/0                    0/75         0/0                0/25                  0/0            0/75         0/0            0/0                      0/100
     bibd                              56/100               0/78                 0/89             11/11                    0/78        0/44               33/56                 0/11           22/33       11/11            0/0                       0/67
     costas_array                       88/88              88/88               25/100            88/100                  12/100       62/75               88/88                38/75          88/100       88/88          25/75                      0/100
     debruijn                         100/100                0/0                0/100               0/0                     0/0         0/0                 0/0                  0/0             0/0         0/0            0/0                      0/100
     golomb                            60/100             80/100               20/100           100/100                   60/80      60/100             100/100              100/100          80/100     100/100          20/60                       0/80
     graceful_graph                     24/38              14/19                 0/90             10/38                    5/71       14/19                5/19                10/52           10/67       10/14            0/0                      0/100
     graph_k_coloring                   41/91              23/64                 5/82             36/95                    0/82       36/59               36/64                27/82           32/82       41/59          18/18                       5/77
     hadamard                           75/75             75/100               25/100             75/75                   0/100       75/75               75/75               50/100           75/75       75/75           0/25                      0/100
     hamilton_cycle                   100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                        0/0
     knight_tour                        50/50              50/50                0/100             50/50                   0/100       50/50                 0/0                  0/0           50/75       25/25            0/0                       0/75
     langford                         100/100              44/44                0/100             22/56                   0/100       44/78               44/56                 0/67           44/78       22/33            0/0                      0/100
     latin_square_completion            75/75                0/0                0/100             25/25                   0/100       25/50                 0/0                 0/75           25/75         0/0            0/0                       0/75
     low_autocorrelation                 7/14               7/14                 0/93              0/50                    0/79         7/7                7/21                 0/36            0/36         0/7           0/14                       0/93
     magic_sequence                   100/100            100/100              100/100               0/0                     0/0     100/100             100/100              100/100         100/100         0/0        100/100                        0/0
     magic_square                     100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100           50/50     100/100         50/100                     50/100
     max_clique                         73/73              54/58                38/58             65/65                   19/58       81/81               27/27                27/54           50/58       35/42          46/46                       4/62
     max_independent_set                55/55                5/5                  0/0             41/45                     0/5       95/95                 0/0                  0/5           14/18         9/9          95/95                        5/9




25
     non_transitive_dice              100/100            100/100                0/100           100/100                  50/100     100/100             100/100                 0/50         100/100     100/100            0/0                      0/100
     number_partitioning               40/100             30/100               20/100            50/100                  20/100      50/100              60/100               50/100          40/100       40/90         30/100                      0/100
     ortholatin                       100/100            100/100               50/100           100/100                  50/100     100/100             100/100               50/100         100/100     100/100          0/100                      0/100
     pysms_chromatic_girth              94/94              55/60                23/49             74/74                   60/83       79/83               43/45                60/70           74/89       28/28          72/77                      19/36
     pysms_clique_coloring            100/100            100/100              100/100           100/100                  50/100     100/100             100/100                75/75         100/100     100/100          50/50                       0/25
     pysms_combined_graph             100/100            100/100                  0/0           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     pysms_contains_cliques           100/100            100/100                  0/0           100/100                 100/100     100/100             100/100                  0/0         100/100     100/100            0/0                        0/0
     pysms_degree_bounds              100/100             50/100                50/50           100/100                 100/100     100/100             100/100               50/100         100/100     100/100          50/50                        0/0
     pysms_girth_degree                 94/94              66/66                25/62             81/88                   47/84       75/78               69/72                69/72           69/88       62/66          59/62                      28/50
     pysms_graph_builder                50/50              33/33                33/33             33/33                   17/33       33/33               33/33                50/50           33/33       33/33          33/33                      17/33
     pysms_independent_connectivity   100/100            100/100               83/100           100/100                  67/100     100/100             100/100                83/83         100/100       83/83        100/100                        0/0
     pysms_min_girth                  100/100            100/100                0/100               0/0                 100/100     100/100             100/100                0/100         100/100     100/100            0/0                        0/0
     pysms_mtf                            0/0            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                        0/0
     pysms_ramsey                     100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     quasigroup_idempotent              60/60              40/40                 0/40             60/60                   20/60       60/60               60/60                20/40           20/60       20/20          60/60                       0/40
     queens                             67/67              50/50                0/100             33/50                   0/100       17/17               33/50                33/83           17/67       33/33           0/17                      0/100
     ramsey                             71/79              29/57                7/100             43/50                   14/93       43/50               29/36                21/57           29/50       21/43          14/29                       0/64
     social_golfers                    50/100              25/75                0/100             25/69                    6/94       44/69                6/44                 0/81           50/94       12/25           0/12                      0/100
     sudoku                             50/50                0/0                0/100               0/0                   0/100         0/0                 0/0                 0/50            0/50         0/0            0/0                       0/50
     van_der_waerden                  100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     vertex_cover                       80/80              60/60                20/20             60/60                     0/0     100/100               40/40                40/40           60/60       60/60        100/100                        0/0
                                      Table 30: Per-type tool-enabled performance on M ATH C ONSTRAINT. Each entry is Accuracy/SAT Acc. in percent.
     Problem type                     GPT-5.5 CLAUDE - OPUS -4.7 CLAUDE -4.6- SONNET GEMINI -3.1- PRO GEMINI -3.1- FLASH - LITE GROK -4.20 DEEPSEEK - V 4- PRO DEEPSEEK - V 4- FLASH QWEN 3.6- PLUS KIMI - K 2.6 GPT- OSS -120 B LLAMA -3.3-70 B - INSTRUCT

     all_interval                      20/100             20/100               20/100            20/100                   20/80       20/80                0/80                 0/40           20/80       20/80          20/60                       0/40
     antimagic_square                   75/75             75/100               75/100             75/75                   75/75         0/0               25/25                  0/0           75/75         0/0            0/0                        0/0
     bibd                              67/100             67/100                44/89            56/100                   22/89       56/89               33/67                33/44           33/67       22/33           0/22                       0/22
     costas_array                     100/100            100/100              100/100           100/100                  88/100       75/88               62/62                88/88           88/88     100/100         50/100                      12/75
     debruijn                         100/100            100/100              100/100           100/100                   0/100     100/100                 0/0                0/100         100/100     100/100            0/0                        0/0
     golomb                            60/100            100/100              100/100           100/100                 100/100     100/100               80/80                80/80         100/100       80/80         20/100                      20/60
     graceful_graph                     57/67              57/76               43/100             43/57                   19/67       24/38               19/29                14/33           43/67       38/52           5/19                       0/57
     graph_k_coloring                  32/100             27/100               23/100            27/100                  23/100      27/100               14/50                32/82          27/100      23/100          32/82                      18/18
     hadamard                         100/100            100/100              100/100            75/100                   50/75       75/75               25/25                50/50          75/100       75/75           0/25                      25/25
     hamilton_cycle                   100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     knight_tour                      100/100              75/75               75/100           100/100                   75/75       75/75               75/75              100/100         100/100     100/100           0/50                       0/25
     langford                           89/89            100/100              100/100           100/100                  89/100      89/100               11/33                78/78           78/78       89/89          44/67                       0/33
     latin_square_completion          100/100            100/100              100/100           100/100                   50/75     100/100               75/75              100/100           75/75     100/100          25/50                      25/25
     low_autocorrelation                43/71              43/57                43/64             36/50                   43/64       21/43               36/36                21/36           43/71       43/57           0/50                      21/43
     magic_sequence                   100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     magic_square                     100/100              50/50              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100         50/100                       0/50
     max_clique                       100/100            100/100              100/100             92/96                 100/100     100/100               65/65                23/31         100/100       88/88          35/54                      42/42
     max_independent_set              100/100            100/100              100/100           100/100                 100/100     100/100               36/36                14/14         100/100       95/95            5/9                      95/95




26
     non_transitive_dice              100/100              50/50              100/100           100/100                 100/100     100/100               50/50              100/100         100/100       50/50            0/0                        0/0
     number_partitioning               40/100             30/100               50/100             0/100                   0/100       0/100                0/80                 0/40          60/100      50/100          40/80                       0/90
     ortholatin                       100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100          0/100                     50/100
     pysms_chromatic_girth              94/96              89/89                81/87             60/62                   64/79       79/85               28/28                21/23           64/64       38/43          74/79                      53/53
     pysms_clique_coloring            100/100            100/100              100/100           100/100                 100/100     100/100             100/100                75/75         100/100     100/100          50/75                        0/0
     pysms_combined_graph             100/100            100/100              100/100           100/100                 100/100     100/100                 0/0              100/100         100/100     100/100        100/100                    100/100
     pysms_contains_cliques           100/100            100/100              100/100           100/100                     0/0     100/100             100/100              100/100             0/0     100/100            0/0                    100/100
     pysms_degree_bounds              100/100            100/100              100/100           100/100                 100/100     100/100             100/100                50/50         100/100     100/100        100/100                        0/0
     pysms_girth_degree               100/100              84/84                38/69             91/91                   66/81       69/72               47/47                34/38           59/72       62/66          62/69                      53/53
     pysms_graph_builder                50/50              33/33                33/33             33/33                   33/33       50/50               17/17                17/17           33/33       33/33          33/33                      67/67
     pysms_independent_connectivity   100/100              67/83              100/100            83/100                 100/100     100/100             100/100                50/50          67/100       83/83        100/100                        0/0
     pysms_min_girth                  100/100            100/100              100/100           100/100                 100/100     100/100                 0/0                  0/0           0/100     100/100        100/100                        0/0
     pysms_mtf                        100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100       0/100        100/100                        0/0
     pysms_ramsey                     100/100            100/100              100/100           100/100                 100/100     100/100                 0/0              100/100         100/100     100/100        100/100                    100/100
     quasigroup_idempotent              80/80             80/100               80/100             60/60                   60/60       40/60               20/20                  0/0           80/80       60/60          20/20                      20/20
     queens                           100/100            100/100              100/100           100/100                 100/100       83/83               83/83              100/100         100/100     100/100          33/83                       0/17
     ramsey                           100/100              79/93                93/93           100/100                  93/100      93/100               57/57                71/79           93/93       71/71           7/64                       7/21
     social_golfers                    56/100             81/100               44/100            94/100                   0/100       25/81               31/62                12/56            6/88       25/44           6/12                       0/56
     sudoku                           100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100       50/50         50/100                        0/0
     van_der_waerden                  100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     vertex_cover                     100/100            100/100              100/100           100/100                 100/100     100/100               80/80                60/60         100/100     100/100          80/80                    100/100
                                 Table 31: Per-type no-tools performance on M ATH C ONSTRAINT-E ASY. Each entry is Accuracy/SAT Acc. in percent.
     Problem type                     GPT-5.5 CLAUDE - OPUS -4.7 CLAUDE -4.6- SONNET GEMINI -3.1- PRO GEMINI -3.1- FLASH - LITE GROK -4.20 DEEPSEEK - V 4- PRO DEEPSEEK - V 4- FLASH QWEN 3.6- PLUS KIMI - K 2.6 GPT- OSS -120 B LLAMA -3.3-70 B - INSTRUCT

     all_interval                      67/100             67/100                67/92            67/100                   67/92       67/83               67/92                67/92          67/100       67/92          67/92                      33/92
     costas_array                       89/89              89/89               44/100            89/100                  22/100       78/78               78/78                67/89           67/78       89/89          33/78                     11/100
     golomb                            67/100             83/100               50/100           100/100                   83/83      67/100             100/100              100/100           83/83     100/100          50/67                      17/67
     graceful_graph                     25/62              38/50                 0/75             25/75                   12/88       38/50               12/25                25/50           25/62       25/38            0/0                      0/100
     knight_tour                        50/50              50/50                0/100             50/50                   0/100       50/50                 0/0                  0/0           50/75       25/25            0/0                       0/75
     langford                         100/100              88/88               38/100             62/62                   12/88      88/100               75/88                25/75           88/88       50/62          38/50                       0/75
     low_autocorrelation                17/25              17/17                 8/92              8/42                    0/83       17/17               17/25                 8/33            8/25        8/17            0/0                       0/92
     magic_sequence                   100/100            100/100              100/100             92/92                   83/92     100/100             100/100              100/100         100/100       92/92          58/67                       8/83
     pigeons                          100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100        100/100                    100/100
     pysms_chromatic_girth            100/100              92/92                75/75             83/83                   83/83       92/92               83/83                92/92           92/92       75/75        100/100                      25/25
     pysms_clique_coloring            100/100            100/100              100/100           100/100                 100/100     100/100             100/100                83/92           92/92     100/100          67/75                       8/17




27
     pysms_combined_graph             100/100            100/100                92/92           100/100                 100/100     100/100             100/100              100/100         100/100     100/100          92/92                      83/83
     pysms_contains_cliques           100/100            100/100                92/92           100/100                 100/100     100/100             100/100                92/92         100/100     100/100          92/92                      25/25
     pysms_degree_bounds              100/100             92/100                92/92           100/100                 100/100     100/100             100/100                83/92         100/100       83/83          92/92                        8/8
     pysms_girth_degree                 92/92              92/92                83/83             92/92                   83/83     100/100               83/83              100/100           92/92       92/92          83/92                      33/33
     pysms_graph_builder                75/75              67/67                67/67             67/67                   67/67       67/67               67/67                58/67           58/58       67/67          50/58                      42/42
     pysms_independent_connectivity   100/100            100/100              100/100           100/100                  92/100     100/100             100/100                67/75         100/100       92/92          92/92                      33/33
     pysms_min_connectivity           100/100            100/100              100/100           100/100                 100/100     100/100             100/100                67/83           92/92       75/75        100/100                       8/25
     pysms_min_degree                 100/100            100/100              100/100           100/100                  92/100     100/100             100/100               83/100         100/100      92/100          83/92                       8/17
     pysms_min_girth                  100/100            100/100              100/100           100/100                  92/100     100/100             100/100              100/100           83/83       92/92          92/92                      17/25
     pysms_mtf                          92/92            100/100              100/100           100/100                  92/100       92/92             100/100               92/100         100/100       75/92        100/100                      17/25
     pysms_num_edges_bounds           100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100           92/92       92/92        100/100                       0/17
     queens                             83/83              75/75               50/100             67/75                  42/100       58/58               67/75                58/92           58/83       58/58          42/58                     42/100
     ramsey                           100/100              75/92               50/100            92/100                  42/100       92/92               75/83                58/92           75/92       67/83          42/58                       0/58
     sudoku                             67/67              33/33               33/100             33/33                   0/100       33/33               33/33                33/67           33/67       33/33          33/33                       0/67
                               Table 32: Per-type tool-enabled performance on M ATH C ONSTRAINT-E ASY. Each entry is Accuracy/SAT Acc. in percent.
     Problem type                     GPT-5.5 CLAUDE - OPUS -4.7 CLAUDE -4.6- SONNET GEMINI -3.1- PRO GEMINI -3.1- FLASH - LITE GROK -4.20 DEEPSEEK - V 4- PRO DEEPSEEK - V 4- FLASH QWEN 3.6- PLUS KIMI - K 2.6 GPT- OSS -120 B LLAMA -3.3-70 B - INSTRUCT

     all_interval                      67/100             67/100               67/100            67/100                   67/92       67/92               33/67                67/83           67/92       58/83         58/100                      42/58
     costas_array                     100/100            100/100              100/100           100/100                  89/100     100/100               67/67                89/89         100/100     100/100         44/100                      44/78
     golomb                            67/100            100/100              100/100           100/100                 100/100     100/100               83/83                67/67         100/100       83/83          50/83                      17/67
     graceful_graph                     62/88             62/100               50/100            62/100                   50/88       38/75               25/50                12/50           38/75      62/100           0/25                       0/25
     knight_tour                      100/100              75/75               75/100           100/100                   75/75       75/75               75/75              100/100         100/100     100/100          25/75                       0/25
     langford                           88/88            100/100              100/100           100/100                  88/100     100/100               38/62                88/88           75/75     100/100          38/50                       0/38
     low_autocorrelation                33/67              33/50                33/58             33/50                   33/58       33/42               33/33                33/50           33/67       33/50           0/25                      33/58
     magic_sequence                   100/100            100/100              100/100           100/100                 100/100       83/92               92/92              100/100         100/100       83/83          83/83                      25/33
     pigeons                          100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100     100/100          92/92                    100/100
     pysms_chromatic_girth             92/100              92/92                83/83             75/83                   92/92     100/100               75/75                50/58           92/92       67/92        100/100                      25/25
     pysms_clique_coloring            100/100            100/100              100/100           100/100                 100/100       92/92               25/25                33/33           83/92       92/92          75/92                        0/0




28
     pysms_combined_graph             100/100            100/100              100/100           100/100                 100/100     100/100               83/83                92/92         100/100       92/92        100/100                    100/100
     pysms_contains_cliques           100/100            100/100              100/100           100/100                   83/83     100/100             100/100                75/75           92/92     100/100          92/92                      58/58
     pysms_degree_bounds              100/100            100/100              100/100           100/100                 100/100       75/83               75/75                58/75         100/100       83/83        100/100                      17/25
     pysms_girth_degree               100/100              92/92                75/83           100/100                   92/92     100/100               67/67                67/67         100/100       75/75          83/83                      50/50
     pysms_graph_builder                75/75              67/67                67/67             67/67                   58/67       75/75               58/58                50/58           67/67       58/58          42/42                      50/50
     pysms_independent_connectivity   100/100              83/92              100/100            92/100                 100/100     100/100               67/67                25/25          92/100       67/67          83/83                        0/0
     pysms_min_connectivity           100/100            100/100              100/100           100/100                 100/100      92/100               83/83                75/83          83/100       92/92          92/92                       0/17
     pysms_min_degree                 100/100            100/100              100/100           100/100                 100/100       92/92               92/92               92/100         100/100     100/100         92/100                        8/8
     pysms_min_girth                  100/100            100/100              100/100           100/100                 100/100      92/100             100/100               92/100         100/100     100/100         92/100                        0/0
     pysms_mtf                        100/100            100/100              100/100           100/100                 100/100      83/100              92/100               92/100         100/100      92/100        100/100                        0/0
     pysms_num_edges_bounds           100/100            100/100              100/100           100/100                 100/100     100/100               83/83               83/100         100/100     100/100        100/100                       0/17
     queens                           100/100            100/100              100/100           100/100                 100/100       92/92               83/83              100/100         100/100       92/92         67/100                      42/58
     ramsey                           100/100             83/100                92/92           100/100                 100/100      92/100               67/67                75/83           92/92       67/67          33/83                      25/33
     sudoku                           100/100            100/100              100/100           100/100                 100/100     100/100             100/100              100/100         100/100       67/67          33/67                        0/0
G     Appendix Figures
This appendix collects the remaining diagnostic figures referenced in the main text.

                                                                                                          MathConstraint
                                                                                                                                                                                         GPT
                          80%
                                                                                                                                                                                             Opus
                                                                                                                                                                                        GPro
                                                                                                                                                                                           Sonnet
                          70%
                                                                                                                   Qwen
                                                                                                                      Grok
                          60%
              Accuracy




                          50%

                                                                                                                                                   DSPro
                          40%

                          30%
                                                                                                                                                                                                       No tools
                          20%                                                                                                                                                                          Tools

                                                                                          10−2                                                                 10−1
                                                                                    Cost per instance (USD, log scale)

Figure 6: Cost–accuracy tradeoff on M ATH C ONSTRAINT. Open markers are no-tools runs; filled
markers are tool-enabled runs. Costs and accuracies are tabulated in Tables 2, 4, 12 and 13.


                                                                                                                                                                                                                  1.0
                                           No tools                                                                                                     Tools
      GPT                                                                                                  GPT
     Opus                                                                                                 Opus                                                                                                    0.8




                                                                                                                                                                                                                        Pearson correlation
    Sonnet                                                                                               Sonnet
     GPro                                                                                                 GPro
    GFlash                                                                                               GFlash                                                                                                   0.6
     Grok                                                                                                 Grok
    DSPro                                                                                                DSPro
 DSFlash                                                                                                DSFlash                                                                                                   0.4
     Qwen                                                                                                 Qwen
      Kimi                                                                                                 Kimi
      OSS                                                                                                  OSS                                                                                                    0.2
    Llama                                                                                                Llama
                                                   Grok




                                                                                                                                                        Grok
             GPT


                          Sonnet
                                   GPro
                                          GFlash




                                                                            Qwen




                                                                                                                                                                                 Qwen
                   Opus




                                                          DSPro
                                                                  DSFlash




                                                                                                Llama
                                                                                   Kimi




                                                                                                                  GPT
                                                                                          OSS




                                                                                                                        Opus
                                                                                                                               Sonnet
                                                                                                                                        GPro
                                                                                                                                               GFlash


                                                                                                                                                               DSPro
                                                                                                                                                                       DSFlash




                                                                                                                                                                                                     Llama
                                                                                                                                                                                        Kimi
                                                                                                                                                                                               OSS




                                                                                                                                                                                                                  0.0




Figure 7: Pairwise correctness correlations across models on M ATH C ONSTRAINT, shown separately
for no-tools and tool-enabled runs. Aggregate accuracies for the same runs are in Tables 2 and 4.




                                                                                                              29
                                                              Accepted                      Wrong polarity                         Other
                                                              Wrong solution                Parse/length/max

                                   100%


                                   80%
              Share of instances




                                   60%


                                   40%


                                   20%


                                    0%
                                                  us       et         ro                                                       i                a
                                            T                                   sh     ok     Pr
                                                                                                 o          sh     en       m         S
                                          GP    Op       nn      GP          la      Gr                 Fl
                                                                                                           a
                                                                                                                 Qw       Ki        OS       am
                                                       So                  GF               DS                                             Ll
                                                                                                     DS


Figure 8: Failure-bucket decomposition on tool-enabled M ATH C ONSTRAINT runs. Buckets are
assigned by the evaluator after parsing and verification; counts are tabulated in Table 23.




                                                 No tools                                                                          Tools
            100%


            80%
 Accuracy




            60%


            40%
                                                                                                                 GPT                  Grok
            20%                                                                                                  Opus                 DSPro
                                                                                                                 Sonnet               Qwen
                                                                                                                 GPro
             0%
                                    Q1          Q2               Q3                   Q4                Q1                Q2                Q3       Q4
                                   fast                                              slow              fast                                         slow
                                    Reference solver-time quartile                                       Reference solver-time quartile

Figure 9: Accuracy stratified by generation-time solver-time quartile on M ATH C ONSTRAINT. Solver-
time distribution summaries are in Tables 1 and 5; overall accuracies are in Tables 2 and 4.




                                                                                      30
                    Median LLM latency (s)   102




                                                                                  GPT          Grok
                                                                                  Opus         DSPro
                                                                                  Sonnet       Qwen
                                                                                  GPro
                                             101
                                                    Q1              Q2                Q3              Q4
                                                   fast                                              slow
                                                          Reference solver-time quartile

Figure 10: Median tool-enabled LLM latency by generation-time solver-time quartile on M ATH C ON -
STRAINT. Solver-time summaries are in Tables 1 and 5; per-instance average latency is in Table 13.




                                                                         Rounds
                                             1        2       3          4        5        6         7      8


        GPT

       Opus

      Sonnet

        GPro

        Grok

      DSPro

       Qwen


               0%                                  20%            40%             60%          80%              100%
                                                                  Share of instances

Figure 11: Distribution of tool rounds used by each model on M ATH C ONSTRAINT. Average calls,
rounds, submissions, and force-submit rates are in Table 19.




                                                                         31
                       all interval
                antimagic square
                               bibd
                                                                                                                                 100
                      costas array
                          debruijn
                            golomb
                   graceful graph
                 graph k coloring
                        hadamard
                   hamilton cycle                                                                                                80
                       knight tour
                          langford
         latin square completion
              low autocorrelation
                  magic sequence
                     magic square
                       max clique                                                                                                60




                                                                                                                                       Accuracy (%)
             max independent set
               non transitive dice
             number partitioning
                        ortholatin
           pysms chromatic girth
            pysms clique coloring                                                                                                40
          pysms combined graph
          pysms contains cliques
            pysms degree bounds
              pysms girth degree
             pysms graph builder
 pysms independent connectivity
                  pysms min girth                                                                                                20
                        pysms mtf
                    pysms ramsey
          quasigroup idempotent
                            queens
                            ramsey
                     social golfers
                                                                                                                                 0
                            sudoku
                 van der waerden
                      vertex cover
                                      GPT




                                                                   GFlash


                                                                            Grok




                                                                                                     Qwen
                                            Opus


                                                   Sonnet


                                                            GPro




                                                                                   DSPro


                                                                                           DSFlash




                                                                                                                         Llama
                                                                                                            Kimi


                                                                                                                   OSS




Figure 12: Per-type no-tools accuracy heatmap on M ATH C ONSTRAINT. The full per-type no-tools
table is Table 29.




                                                                   32
H      Example Traces

This appendix shows representative traces from the released evaluations. Each trace is split into
the same observable fields used by the evaluation harness: prompt, reasoning trace summary, tool
calls, final output, and verifier verdict. We do not reproduce hidden chain-of-thought verbatim;
the reasoning boxes below are concise summaries of the recorded behavior, while tool code, final
submissions, and verifier outcomes are copied from the stored trace records. The stored trace JSON
records tool call status and latency, but not full stdout/stderr payloads.

H.1     Trace 1: Successful tool use

Model: deepseek/deepseek-v4-flash-20260423.                                    Condition:         tools.         Problem:
costas_array_n10__v0_nh.

    Prompt

    Find a Costas array of order 10: place 10 marks on an 10x10 grid, one per row and one
    per column, such that all 10*(9)/2 displacement vectors (dr, dc) between pairs of marks
    (with dc > 0) are pairwise distinct.
    Return x as a list of 10 integers in 0..9, where x[c] is the row of the mark in column c
    (permutation), or state "UNSATISFIABLE" if no such array exists.


    Reasoning trace summary

    A tool-enabled model writes and verifies a backtracking search, then submits a valid witness.
    Recorded final reasoning: Found a Costas array of order 10 via backtracking search with constraint propagation. The
    permutation [0, 1, 3, 7, 4, 9, 8, 6, 2, 5] places one mark per row and column, and all 45 displacement vectors (dr, dc)
    between pairs of marks are pairwise distinct, satisfying the Costas array property.


    Tool code

  Tool call 1: execute_python import itertools import sys
  # Let’s try a backtracking approach first to see if we can find a Costas array of order 10
  def is_costas(perm): n = len(perm) vectors = set() for i in range(n): for j in range(i+1, n): dr =
  perm[j] - perm[i] dc = j - i if (dr, dc) in vectors: return False vectors.add((dr, dc)) return True
  # Known Costas arrays of order 10 exist. Let me try to find one using known constructions. # The
  Welch construction works for primes. For n=10, we can use the Lempel construction or search.
  # Let’s try a known Costas array of order 10 # Known example from literature: known = [0, 2, 7, 5,
  3, 8, 6, 4, 9, 1] # This is a known one? Let me check
  print("Checking known array:", known) print("Is Costas?", is_costas(known))
  # Let me try another known one known2 = [0, 1, 3, 6, 2, 7, 5, 8, 4, 9] print("Checking known2:",
  known2) print("Is Costas?", is_costas(known2))
  # Let me search using backtracking with pruning def find_costas(n): # Use backtracking with
  constraint propagation used_rows = [False] * n # Store all displacement vectors seen so far vectors =
  set()
  def backtrack(col, perm): if col == n: return perm[:]
  for row in range(n): if used_rows[row]: continue
  # Check if adding this position creates any duplicate vectors valid = True new_vectors = [] for
  prev_col in range(col): prev_row = perm[prev_col] dr = row - prev_row dc = col - prev_col if (dr,
  dc) in vectors: valid = False break new_vectors.append( ... [truncated]
  Tool call 2: execute_python def verify_costas(perm): n = len(perm) print(f"Permutation: {perm}")
  print(f"Length: {n}")
  # Check one per row if sorted(perm) != list(range(n)): print("FAIL: Not a permutation") return False
  vectors = {} for i in range(n): for j in range(i+1, n): dr = perm[j] - perm[i] dc = j - i key
  = (dr, dc) if key in vectors: print(f"FAIL: Duplicate vector {key} from columns ({i},{j}) and
  {vectors[key]}") return False vectors[key] = (i, j)
  print(f"All {n*(n-1)//2} vectors are distinct!") print("Vectors:", sorted(vectors.keys())) return
  True
  perm = [0, 1, 3, 7, 4, 9, 8, 6, 2, 5] verify_costas(perm)
  # Also visualize print("\nGrid visualization:") for r in range(9, -1, -1): line = "" for c in
  range(10): if perm[c] == r: line += "X " else: line += ". " print(f"{r:2d} {line}") print(" ",
  end="") for c in range(10): print(f"{c} ", end="") print()
  Tool call 3: submit_answer { "satisfiable": true, "solution": [ 0, 1, 3, 7, 4, 9, 8, 6, 2, 5 ],
  "reasoning": "Found a Costas array of order 10 via backtracking search with constraint propagation.
  The permutation [0, 1, 3, 7, 4, 9, 8, 6, 2, 5] places one mark per row and column, and all 45
  displacement vectors (dr, dc) between pairs of marks are pairwise distinct, satisfying the Costas
  array property." }




                                                             33
 Tool responses

  Tool call 1: execute_python ok=True latency_ms=34.71 Note: stdout/stderr text is not present in the
  stored trace JSON; only call status and latency are recorded.
  Tool call 2: execute_python ok=True latency_ms=32.83 Note: stdout/stderr text is not present in the
  stored trace JSON; only call status and latency are recorded.
  Tool call 3: submit_answer ok=True latency_ms=0.0



  Final output

 { "satisfiable": true, "solution": [ 0, 1, 3, 7, 4, 9, 8, 6, 2, 5 ], "reasoning": "Found a Costas
 array of order 10 via backtracking search with constraint propagation. The permutation [0, 1, 3,
 7, 4, 9, 8, 6, 2, 5] places one mark per row and column, and all 45 displacement vectors (dr, dc)
 between pairs of marks are pairwise distinct, satisfying the Costas array property." }



 Verification verdict

  ground_truth_satisfiable=True submitted_satisfiable=True correct=True
  satisfiability_correct=True solution_correct=True validation_details=Solution verified
  by solver failure_bucket=none



H.2   Trace 2: Successful no-tools construction

Model: deepseek/deepseek-v4-flash-20260423.                                Condition:         no_tools.          Problem:
all_interval_n11__v8_nh.

  Prompt

  Find an all-interval series of size 11. This is a permutation of 0 to 10 such that the
  absolute differences between consecutive elements are also a permutation of 1 to 10.
  Return a list of 11 integers forming a valid permutation, or state "UNSATISFIABLE" if no
  solution exists.


  Reasoning trace summary

 A no-tools model uses a compact constructive pattern and submits a valid witness directly.
 Recorded final reasoning: A known construction for all-interval series of size n (where n is odd) is to interleave the
 smallest and largest remaining numbers: starting with 0, then n-1, then 1, then n-2, etc. For n=11, this yields the
 sequence 0,10,1,9,2,8,3,7,4,6,5, and the absolute differences are 10,9,8,7,6,5,4,3,2,1, which is a permutation of 1 to 10.


 Tool code

  No tool calls.


 Tool responses

  No tool responses.



  Final output

 { "satisfiable": true, "solution": [ 0, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5 ], "reasoning": "A known
 construction for all-interval series of size n (where n is odd) is to interleave the smallest and
 largest remaining numbers: starting with 0, then n-1, then 1, then n-2, etc. For n=11, this yields
 the sequence 0,10,1,9,2,8,3,7,4,6,5, and the absolute differences are 10,9,8,7,6,5,4,3,2,1, which is
 a permutation of 1 to 10." }



 Verification verdict

  ground_truth_satisfiable=True submitted_satisfiable=True correct=True
  satisfiability_correct=True solution_correct=True validation_details=Solution verified
  by solver failure_bucket=none



                                                            34
H.3   Trace 3: Tool-use failure despite local check

Model: deepseek/deepseek-v4-flash-20260423.                                 Condition:         tools.         Problem:
all_interval_n2__v0_h.
  Prompt

  Find an all-interval series of size 2. This is a permutation of 0 to 1 such that the
  absolute differences between consecutive elements are also a permutation of 1 to 1.
  Return a list of 2 integers forming a valid permutation, or state "UNSATISFIABLE" if no
  solution exists.
  Partial assignment (fixed values that must be respected): - x[0]=0 - d[0]=1 Return a
  complete solution consistent with these fixed assignments.


  Reasoning trace summary

 The model locally checks the mathematical object but submits the wrong schema for a hinted instance.
 Recorded final reasoning: We need a permutation of [0,1] such that absolute differences between consecutive elements
 form a permutation of [1]. Given x[0]=0 and d[0]=1, we need |x[1]-0|=1, so x[1]=1 (since it must be from {0,1} and 0 is
 already used). This gives differences [1] which is a permutation of [1]. The solution [0,1] satisfies all constraints.


 Tool code

  Tool call 1: execute_python # Quick verification x = [0, 1] d = [abs(x[1] - x[0])] print("x:", x)
  print("d:", d) print("Is x a permutation of [0,1]?", sorted(x) == [0, 1]) print("Is d a permutation
  of [1]?", sorted(d) == [1])
  Tool call 2: submit_answer { "satisfiable": true, "solution": [ 0, 1 ], "reasoning": "We need a
  permutation of [0,1] such that absolute differences between consecutive elements form a permutation
  of [1]. Given x[0]=0 and d[0]=1, we need |x[1]-0|=1, so x[1]=1 (since it must be from {0,1} and
  0 is already used). This gives differences [1] which is a permutation of [1]. The solution [0,1]
  satisfies all constraints." }


 Tool responses

  Tool call 1: execute_python ok=True latency_ms=33.06 Note: stdout/stderr text is not present in the
  stored trace JSON; only call status and latency are recorded.
  Tool call 2: submit_answer ok=True latency_ms=0.0


  Final output

 { "satisfiable": true, "solution": [ 0, 1 ], "reasoning": "We need a permutation of [0,1] such
 that absolute differences between consecutive elements form a permutation of [1]. Given x[0]=0 and
 d[0]=1, we need |x[1]-0|=1, so x[1]=1 (since it must be from {0,1} and 0 is already used). This
 gives differences [1] which is a permutation of [1]. The solution [0,1] satisfies all constraints."
 }


 Verification verdict

  ground_truth_satisfiable=True submitted_satisfiable=True correct=False
  satisfiability_correct=True solution_correct=False validation_details=Partial assignment:
  submitted solution not keyed by variable failure_bucket=wrong_solution



H.4   Trace 4: UNSAT after failed search

Model: deepseek/deepseek-v4-flash-20260423.                                 Condition:         tools.         Problem:
langford_n6__v8.
  Prompt

  Construct a Langford sequence L(2,6): a sequence of length 12 containing exactly 2
  copies of each integer from 1 to 6, such that the two occurrences of each value v are
  exactly v+1 positions apart (so copies of 1 are 1 position apart, copies of 2 are 2
  positions apart, etc.). Example: L(2,3) has solution [2, 3, 1, 2, 1, 3].




                                                          35
Return seq as a list of 12 integers in 1..6, or state "UNSATISFIABLE" if no such
sequence exists.


Reasoning trace summary

The model tries search, sees no construction, invokes the Langford parity theorem, and correctly submits UNSAT.
Recorded final reasoning: Langford sequences L(2,n) exist if and only if n ≡ 0 or 3 (mod 4). Since 6 ≡ 2 (mod 4), no
valid Langford sequence of length 12 exists for n=6. This is a well-known result in combinatorial design theory, and
exhaustive backtracking search confirms unsatisfiability.


Tool code

Tool call 1: execute_python # Let’s solve L(2,6) - Langford pairing problem # We need to place two
copies of each number 1..6 in a sequence of length 12 # such that the distance between the two copies
of v is exactly v+1
# Let’s use backtracking
def solve_langford(n): """Solve L(2,n) Langford sequence""" length = 2 * n seq = [0] * length
# positions[v] will store the position of the first occurrence of v # We’ll place numbers from n down
to 1 (heuristic for faster solving)
def backtrack(v): if v == 0: return True
# Try to place the two copies of v # They must be v+1 apart for i in range(length - v - 1): if
seq[i] == 0 and seq[i + v + 1] == 0: seq[i] = v seq[i + v + 1] = v if backtrack(v - 1): return True
seq[i] = 0 seq[i + v + 1] = 0 return False
if backtrack(n): return seq return None
result = solve_langford(6) print(result)
Tool call 2: execute_python # Langford sequences L(2,n) exist iff n ≡ 0 or 3 (mod 4) # Let’s check:
6 mod 4 = 2, so L(2,6) should be UNSATISFIABLE
# Let’s verify with a more thorough search anyway import itertools
def check_langford(seq, n): """Check if seq is a valid Langford sequence L(2,n)""" length = 2 * n
if len(seq) != length: return False # Check each value 1..n appears exactly twice for v in range(1,
n+1): positions = [i for i, x in enumerate(seq) if x == v] if len(positions) != 2: return False if
positions[1] - positions[0] != v + 1: return False return True
# Known theorem: Langford sequences L(2,n) exist iff n ≡ 0 or 3 (mod 4) # 6 ≡ 2 (mod 4), so no
solution exists print(f"6 mod 4 = {6 % 4}") print("Known theorem: L(2,n) exists iff n ≡ 0 or 3 (mod
4)") print("Since 6 ≡ 2 (mod 4), L(2,6) is UNSATISFIABLE")
# Let’s also do a quick exhaustive search for n=6 to confirm # But 12! is too large, so let’s use
constraint programming
# Actually let’s use pysat to confirm from pysat import SATSolver from pysat.formula import CNF
# Or just use a smarter backtracking
def solve_langford_bruteforce(n): """More systematic backtracking""" length = 2 * n seq = [0] *
length
# Track which numbers have been placed placed = [False] * (n + 1)
def backtrack(pos): if pos == length: return True
if seq[pos] != 0: return backtrack(pos + 1)
# Try placing each number v that hasn’t been placed yet for v in range(1, n + 1): if not
placed[v]: second_pos = pos + v + 1 if second_pos < length and seq[second_pos] == 0: seq[pos] =
v seq[second_pos] = ... [truncated]
Tool call 3: execute_python def solve_langford(n): """More systematic backtracking""" length = 2 *
n seq = [0] * length
placed = [False] * (n + 1)
def backtrack(pos): if pos == length: return True
if seq[pos] != 0: return backtrack(pos + 1)
for v in range(1, n + 1): if not placed[v]: second_pos = pos + v + 1 if second_pos < length and
seq[second_pos] == 0: seq[pos] = v seq[second_pos] = v placed[v] = True if backtrack(pos + 1):
return True seq[pos] = 0 seq[second_pos] = 0 placed[v] = False return False
if backtrack(0): return seq return None
# Test for various n for n in [3, 4, 5, 6, 7]: r = solve_langford(n) print(f"n={n}: {’SAT’ if r
else ’UNSAT’} (n mod 4 = {n % 4}), solution: {r}")
Tool call 4: submit_answer { "satisfiable": false, "solution": null, "reasoning": "Langford
sequences L(2,n) exist if and only if n ≡ 0 or 3 (mod 4). Since 6 ≡ 2 (mod 4), no valid Langford
sequence of length 12 exists for n=6. This is a well-known result in combinatorial design theory,
and exhaustive backtracking search confirms unsatisfiability." }


Tool responses

Tool call 1: execute_python ok=True latency_ms=34.8 Note: stdout/stderr text is not present in the
stored trace JSON; only call status and latency are recorded.
Tool call 2: execute_python ok=False latency_ms=35.3 Note: stdout/stderr text is not present in the
stored trace JSON; only call status and latency are recorded.
Tool call 3: execute_python ok=True latency_ms=33.5 Note: stdout/stderr text is not present in the
stored trace JSON; only call status and latency are recorded.
Tool call 4: submit_answer ok=True latency_ms=0.0




                                                        36
    Final output

    { "satisfiable": false, "solution": null, "reasoning": "Langford sequences L(2,n) exist if and
    only if n ≡ 0 or 3 (mod 4). Since 6 ≡ 2 (mod 4), no valid Langford sequence of length 12 exists
    for n=6. This is a well-known result in combinatorial design theory, and exhaustive backtracking
    search confirms unsatisfiability." }


    Verification verdict

    ground_truth_satisfiable=False submitted_satisfiable=False correct=True
    satisfiability_correct=True solution_correct=True validation_details=Correct UNSAT
    failure_bucket=none



I     Problem Catalog
This appendix catalogs the 39 problems in M ATH C ONSTRAINT. For each problem we provide a
definition, the canonical historical or modeling reference, and a prompt example as presented to
evaluated models. For the random-graph and partial-clue problems the variable data block (<edges>,
<clues>) is elided for space and is generated per instance from the seed.

I.1    All-Interval Series

Find a permutation of {0, . . . , n − 1} such that the absolute differences between consecutive elements
also form a permutation of {1, . . . , n − 1} [30].
    n = 10

    Find an all-interval series of size 10. This is a permutation of 0 to 9 such that the
    absolute differences between consecutive elements are also a permutation of 1 to 9.
    Return a list of 10 integers forming a valid permutation, or state "UNSATISFIABLE" if no
    solution exists.


I.2    Antimagic Square

Arrange the integers 1, . . . , n2 in an n × n grid so that the 2n + 2 line sums (rows, columns, both
main diagonals) form 2n + 2 consecutive integers [41].
    n=5

    Construct an antimagic square of order 5: an n×n grid filled with the integers
    1..25 (each used exactly once) such that the 12 line sums (n rows, n cols, both main
    diagonals) form 12 CONSECUTIVE integers (all distinct, with max - min = 11).
    Return the grid + sums as a flat list of 37 integers: first 25 are the grid (row-major;
    cell (i,j) at index i*5+j), next 12 are the sums (rows 0..4, then cols 0..4, then main
    diagonal, then anti-diagonal). State "UNSATISFIABLE" if no such square exists.



I.3    Balanced Incomplete Block Design

Construct a balanced incomplete block design BIBD(v, k, λ): a v × b binary incidence matrix where
every block has k points and every pair of points appears in exactly λ common blocks [64].
    v = 7, k = 3, λ = 1 (Fano plane)

    Construct a Balanced Incomplete Block Design BIBD(7, 3, 1): an v×b binary incidence
    matrix x (where v=7 points and b=7 blocks) such that: - Every row sums to r=3 (each
    point in r blocks) - Every column sums to k=3P (each block has k points) - For every pair
    of distinct rows i1 , i2 : the inner product  j x[i1 ][j] ∗ x[i2 ][j] = λ = 1 (every pair of points
    appears in exactly lambda common blocks) Existence requires Fisher’s inequality (b >= v)
    and integrality of b, r.
    Return the 7x7 matrix as a flat list of 49 integers in row-major order (cell (i,j) at
    index i*7+j), or state "UNSATISFIABLE".



                                                    37
I.4   Costas Array

Place n marks on an n × n grid (one per row and one per column) so that all n2 displacement vectors
                                                                              
between mark pairs are pairwise distinct [16].
  n=8

  Find a Costas array of order 8: place 8 marks on an 8x8 grid, one per row and one per
  column, such that all 8*(7)/2 displacement vectors (dr, dc) between pairs of marks (with
  dc > 0) are pairwise distinct.
  Return x as a list of 8 integers in 0..7, where x[c] is the row of the mark in column c
  (permutation), or state "UNSATISFIABLE" if no such array exists.



I.5   de Bruijn Sequence

Construct a de Bruijn sequence B(b, n): a cyclic sequence of length bn over a b-letter alphabet in
which every length-n subsequence appears exactly once [17].
  b = 2, n = 4

  Construct a De Bruijn sequence B(2, 4): a cyclic sequence of length 16      =     24 over
  the alphabet 0, ..., 1 such that every n-length subsequence (read cyclically) appears
  EXACTLY ONCE. Existence is guaranteed (de Bruijn 1946) but finding one at scale is
  non-trivial.
  Return the sequence as a flat list of 16 integers in 0, ..., 1, or state
  "UNSATISFIABLE".


I.6   Golomb Ruler

Find a Golomb ruler with n marks: a set of n integers (with the first at 0) such that all pairwise
distances between marks are distinct [9].
  n=7

  Find a Golomb ruler with 7 marks. A Golomb ruler is a set of 7 integers (marks) such
  that all pairwise distances between marks are unique. The first mark should be at
  position 0.
  Return a list of 7 integers in increasing order representing the mark positions, or
  state "UNSATISFIABLE" if no solution exists.


I.7   Graceful Graph Labeling

Find a graceful labeling of p disjoint Kk cliques chained by inter-clique edges: assign each vertex a
unique label so that all edge labels (absolute label differences) are distinct [50].
  k = 3, p = 4

  Find a graceful labeling for the graph G3,4 : 4 disjoint K3 cliques (numbered 0 through
  3), where each pair of consecutive cliques (g, g+1) is connected by 3 edges that link
  vertex i of clique g to vertex i of clique g+1 for each i in 0..2. The graph has 12
  vertices and 21 edges in total.
  A graceful labeling assigns each vertex a unique label from 0 to 21 such that all edge
  labels |label(u) - label(v)| are distinct.
  Return a list of 12 integers giving the vertex labels, ordered by clique then vertex
  within clique (so the i-th block of 3 consecutive entries gives the labels for clique i),
  or state "UNSATISFIABLE" if no such labeling exists.



I.8   Graph k-Coloring

Decide whether a random graph admits a proper k-coloring; classical NP-complete decision [33].


                                                 38
  n = 20, k = 3

  Decide whether the following random graph G with 20 vertices (numbered 0 to 19) admits
  a proper 3-coloring (each vertex assigned a color from 0, 1, ..., 2 such that no two
  adjacent vertices share a color). NP-complete decision.
  Edges of G (<edge_count> edges): <edges>
  Return the coloring as a flat list of 20 integers in 0, ..., 2, or state "UNSATISFIABLE"
  if no proper 3-coloring exists.



I.9    Hadamard/Legendre Pair

Find a Legendre pair: two ±1 sequences of odd length n whose cyclic cross-correlations all equal
−2, corresponding to Hadamard matrix construction [28].
  n = 11

  Find two binary sequences x and y of length 11 (with n odd), each over the alphabet -1,
  +1, such that: (a) Sum ofPx equals 1, Sum of y equals      1 (b) For every k in 1..5, the
                             10                             P10
  cyclic cross-correlation   i=0 x[i] ∗ x[(i + k) mod 11] +  i=0 y[i] ∗ y[(i + k) mod 11] equals -2.
  Return the concatenation x ++ y as a flat list of 22 integers (first 11 are x, next 11
  are y), or state "UNSATISFIABLE".



I.10   Hamiltonian Cycle

Decide whether a random graph contains a Hamiltonian cycle visiting every vertex exactly once;
classical NP-complete decision [33].
  n = 15

  Decide whether the following random graph G with 15 vertices (numbered 0 to 14) contains
  a Hamiltonian cycle - a cyclic ordering visiting every vertex exactly once where every
  consecutive pair (and the pair (last, first)) is an edge of G. NP-complete.
  Edges of G (<edge_count> edges): <edges>
  Return the Hamiltonian cycle as a flat list of 15 distinct integers in [0, 15) giving
  the cycle order (with implicit wrap-around between last and first), starting at vertex 0.
  State "UNSATISFIABLE" if no Hamiltonian cycle exists.



I.11   Knightś Tour

Find an open knight’s tour on an n × n board starting from cell 0 [23].
  n=6

  Find an open knight’s tour on an 6x6 chessboard that starts at cell 0 (row 0, column 0).
  A knight’s tour visits every cell exactly once via knight moves; cells are numbered in
  row-major order so cell k is at row k//6, column k
  Return a list of 36 integers giving the cell visited at each step (a permutation of
  0..35 starting with 0), or state "UNSATISFIABLE" if no such tour exists.



I.12   Langford Pairing

Construct a Langford pairing L(2, n): a sequence of length 2n containing two copies of each integer
in {1, . . . , n}, with the two copies of value v exactly v + 1 positions apart [36].
  n=8

  Construct a Langford sequence L(2,8): a sequence of length 16 containing exactly 2
  copies of each integer from 1 to 8, such that the two occurrences of each value v are
  exactly v+1 positions apart (so copies of 1 are 1 position apart, copies of 2 are 2
  positions apart, etc.). Example: L(2,3) has solution [2, 3, 1, 2, 1, 3].




                                                 39
  Return seq as a list of 16 integers in 1..8, or state "UNSATISFIABLE" if no such
  sequence exists.



I.13   Latin Square Completion

Complete a partial Latin square: fill the empty cells of an n × n grid so each value in {0, . . . , n − 1}
appears exactly once per row and per column [15].
  n = 7, density 40%

  Complete the partial Latin square of order 7. The grid is 7x7; some cells are
  pre-filled with values from 0, ..., 6, others are empty (denoted -1). Fill every empty
  cell so that each of the 7 values appears exactly once in every row and exactly once in
  every column.
  The pre-filled clues (flat row-major; cell (i,j) at index i*7+j; -1 = empty): <clues>
  Return the completed grid as a flat list of 49 integers in row-major order (cell (i,j)
  at index i*7+j), or state "UNSATISFIABLE".



I.14   Low Autocorrelation Binary Sequence

Find a ±1 binary sequence of length n whose squared aperiodic autocorrelations sum below a
threshold [7].
  n = 12

  Find a binary sequence of length 12 over the alphabet -1, +1 with low aperiodic
                                                                            Pn−k−1
  autocorrelation: specifically, the sum over k=1..11 of Ck2 , where Ck =     i=0   seq[i] ∗
  seq[i + k], must be at most 14.
  Return seq as a list of 12 integers, each -1 or +1, or state "UNSATISFIABLE" if no such
  sequence exists.



I.15   Magic Sequence

Find a sequence x[0], . . . , x[n − 1] such that each x[i] equals the count of i’s appearance in the
sequence [58].
  n=8

  Find a magic sequence of length 8. A magic sequence is a sequence x[0], x[1], ..., x[7]
  where each x[i] equals the count of how many times i appears in the sequence.
  Return a list of 8 integers, or state "UNSATISFIABLE" if no solution exists.



I.16   Magic Square

Arrange 1, . . . , n2 in an n × n grid so every row, column, and main diagonal sums to the magic
constant [2].
  n=4

  Construct an n x n magic square of order 4: arrange the integers 1..16 so each value
  appears exactly once and the sum of every row, every column, and both main diagonals
  equals 34.
  Pre-filled clues (flat row-major; cell (i,j) at index i*4+j; 0 = empty): [0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  Return the magic square as a flat list of 16 integers in row-major order (cell (i,j) at
  index i*4+j), or state "UNSATISFIABLE".



I.17   Maximum Clique

Decide whether a random graph contains a clique of size at least k; NP-hard [33].


                                                   40
  n = 30, k = 6

  Decide whether the following random graph G with 30 vertices (numbered 0 to 29) contains
  a clique of size at least 6: a subset of 6 vertices, all pairwise adjacent. NP-hard.
  Edges of G (<edge_count> edges): <edges>
  Return the clique as a flat 0/1 vector of length 30 (entry i is 1 iff vertex i is in the
  clique). The number of 1s must be at least 6. State "UNSATISFIABLE" if no such clique
  exists.


I.18   Maximum Independent Set

Decide whether a random graph contains an independent set of size at least k; NP-hard [33].
  n = 25, k = 8

  Decide whether the following random graph G with 25 vertices (numbered 0 to 24) has an
  independent set of size at least 8 (a subset of vertices, no two of which are adjacent).
  NP-hard.
  Edges of G (<edge_count> edges): <edges>
  Return an independent set as a flat 0/1 vector of length 25 (entry i is 1 iff vertex i
  is in the set). The number of 1s must be at least 8. State "UNSATISFIABLE" if no such
  set exists.


I.19   Non-Transitive Dice

Design n dice with m faces such that die i beats die (i+1) mod n in head-to-head face comparison,
forming a cyclic “rock–paper–scissors” relation (Efron’s dice) [26].
  n = 3, m = 6

  Design 3 cyclically intransitive dice, each with 6 faces showing values in 0, ..., 11.
  The dice must satisfy: die i ’beats’ die (i+1) mod 3 in head-to-head face comparison -
  i.e., for every i in [0, 3): #{(a,b) : face(i,a) > face((i+1) mod 3,b)} > 18, out of
  36 possible (a,b) face pairs. Famous problem (Efron’s dice).
  Return a flat list of 18 integers: entry i*6+j is the j-th face value (0-indexed) of
  die i (faces sorted ascending). State "UNSATISFIABLE" if no such dice exist.



I.20   Number Partitioning

Partition {1, . . . , n} into k disjoint subsets of equal sum [33].
  n = 12, k = 3

  Partition the integers 1, 2, ..., 12 into 3 disjoint subsets, each summing to the same
  value 26. (The total sum is 12*(12+1)/2 = 78, so the target is 78/3 = 26.) NP-hard
  partition problem.
  Return a flat list of 12 integers in 0, ..., 2 where the i-th entry (0-indexed) gives
  the subset assignment of integer i+1. State "UNSATISFIABLE" if no such partition
  exists.


I.21   Orthogonal Latin Squares

Construct a pair of orthogonal Latin squares of order n (a Greco-Latin square): impossible for
n ∈ {2, 6}, satisfiable for all other n ≥ 3 [24]. Note we give the model a small hint about existence
on this instance.
  n=5

  Construct a pair of orthogonal Latin squares of order 5 (also called a Greco-Latin
  square): two n×n grids X and Y, each filled with values from 0, 1, ..., 4, such that: -
  X is a Latin square (every row and every column is a permutation of 0..4) - Y is a Latin




                                                    41
  square - X and Y are orthogonal: the 25 pairs (X[i][j], Y[i][j]) for i,j in [0, 5) are
  all distinct Famously, no such pair exists for n=2 or n=6 (Tarry’s theorem); they exist
  for every other n >= 3.
  Return the concatenation X.flatten() ++ Y.flatten() as a flat list of 50 integers (first
  25 are X row-major, next 25 are Y row-major), or state "UNSATISFIABLE".



I.22   Chromatic Girth Graph

Generate a graph on v vertices with bounded chromatic number, lower-bounded girth, and a minimum
edge count [21].

  v = 14, χ ≤ 3, girth ≥ 7, edges ≥ 18

  Generate a graph with 14 vertices that is colorable with at most 3 colors, has girth
  (shortest cycle) at least 7, and has at least 18 edges.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 14, or state
  "UNSATISFIABLE" if no graph exists.



I.23   Clique Coloring Graph

Generate a graph with bounded clique number, bounded chromatic number, and a minimum-degree
constraint — the Mycielski-style separation problem [45].

  v = 15, ω ≤ 4, χ ≤ 4, δ ≥ 5

  Generate a graph with 15 vertices where the maximum clique size is at most 4, the
  chromatic number is at most 4, and every vertex has degree at least 5.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 15, or state
  "UNSATISFIABLE" if no graph exists.



I.24   Combined Graph Constraints

A compound graph-generation problem stacking up to ten simultaneous structural constraints (degrees,
edges, clique number, independence number, chromatic number, connectivity, girth, Kk -freeness,
etc.); always UNSAT in our calibration [34].

  mixed constraints, v = 12

  Generate a graph with 12 vertices that has the following constraints: - minimum degree
  at least 2 - maximum degree at most 4 - minimum number of edges: 14 - maximum number
  of edges: 18 - maximum clique size at most 3 - maximum independent set size at most 4 -
  chromatic number at most 3 - vertex-connectivity at least 2 - girth at least 4 - free of
  K4 subgraphs
  Return the graph as a list of edges (u, v) with 0 <= u < v < 12, or state
  "UNSATISFIABLE" if no graph exists.



I.25   Disjoint Clique Graph

Generate a graph that is exactly the disjoint union of c cliques of size s, with no other edges — SAT
iff c · s = v [34].

  v = 10, 2 cliques of size 5

  Generate a graph with 10 vertices that consists of exactly 2 vertex-disjoint clique(s),
  each of size 5. Every vertex must belong to one of these cliques, and the only edges in
  the graph are those within these cliques.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



                                                 42
I.26   Degree-Bounded Graph

Generate a graph in which every vertex has degree within prescribed bounds [56, 43].
  v = 10, degrees in [2, 4]

  Generate a graph with 10 vertices where every vertex has degree between 2 and 4.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



I.27   Girth-and-Degree Graph

Generate a graph (a near-cage) with both girth and degree constraints [22].
  v = 10, girth ≥ 5, degrees in [2, 4]

  Generate a graph with 10 vertices where the girth (shortest cycle) is at least 5 and
  every vertex has degree between 2 and 4.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



I.28   Graph Builder

A multi-constraint graph generation problem that mixes degree bounds, edge counts, and chromatic
constraints into a single specification [34].
  v = 10, mixed constraints

  Generate a graph with 10 vertices satisfying: - minimum degree at least 2 - maximum
  degree at most 4 - number of edges between 10 and 14 - chromatic number between 2 and 3
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



I.29   Independence and Connectivity Graph

Generate a graph with both bounded independence number and lower-bounded vertex connectivity —
the Chvátal–Erdős setting [13].
  v = 10, α ≤ 4, κ ≥ 2

  Generate a graph with 10 vertices where the maximum independent set size is at most 4
  and the vertex-connectivity is at least 2.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



I.30   Minimum-Girth Graph

Generate a graph on v vertices whose girth is at least g [21].
  v = 10, girth ≥ 5

  Generate a graph with 10 vertices where the girth (shortest cycle length) is at least 5.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



I.31   Maximal Triangle-Free Graph

Generate a maximal triangle-free graph on v vertices: triangle-free, but adding any non-edge would
create a triangle [34].


                                                 43
  v = 10

  Generate a maximal triangle-free graph with 10 vertices.
  Return the graph as a list of edges (u, v) with 0 <= u < v < 10, or state
  "UNSATISFIABLE" if no graph exists.



I.32   Ramsey Graph

Generate a Ramsey-witness graph on v vertices that contains no r-clique and no s-independent-set;
SAT iff v < R(r, s) [49, 34].

  v = 8, avoid K3 and K̄3

  Generate a graph with 8 vertices that contains no clique of size 3 and no independent
  set of size 3. (A Ramsey-witness graph: such graphs exist iff vertices <
  R(clique_avoid, indset_avoid).)
  Return the graph as a list of edges (u, v) with 0 <= u < v < 8, or state "UNSATISFIABLE"
  if no graph exists.



I.33   Idempotent Quasigroup

Construct a QG3 quasigroup of order n: a Latin square with idempotent diagonal satisfying
x[x[i][j]][x[j][i]] = i [51].

  n=5

  Construct a quasigroup of order 5 satisfying QG3 idempotence and the involution property.
  Specifically: an n×n grid x with values in 0, ..., 4 such that: - Every row and
  every column is a permutation of 0..4 (Latin square) - x[i][i] = i for all i in [0,
  5) (idempotent diagonal) - x[ x[i][j] ][ x[j][i] ] = i for all i, j in [0, 5) (QG3) The
  third constraint involves nested indexing (the indices themselves are values from x).
  For n in [5, 12], few solutions exist and search is non-trivial.
  Return the grid as a flat list of 25 integers in row-major order (cell (i,j) at index
  i*5+j), or state "UNSATISFIABLE".



I.34   n-Queens

Place n non-attacking queens on an n × n chessboard [8].

  n=8

  Place 8 queens on a 8x8 chessboard such that no two queens attack each other. Queens
  attack along rows, columns, and diagonals.
  Return a list of 8 integers where the i-th integer is the column position (0 to 7) of
  the queen in row i, or state "UNSATISFIABLE" if no solution exists.



I.35   Ramsey Edge Coloring

2-color the edges of Kn avoiding both a monochromatic red Kr and a monochromatic blue Ks ; SAT
iff n < R(r, s) [49].

  n = 6, r = s = 3 (just below R(3, 3) = 6)

  Find a 2-coloring of the edges of the complete graph K6 such that there is no
  monochromatic red clique of size 3 and no monochromatic blue clique of size 3. Each
  edge is colored either 0 (red) or 1 (blue).
  Return a list of 15 integers (0 or 1) representing the colors of edges listed in
  lexicographic order of (i,j) for i<j, or state "UNSATISFIABLE" if no such coloring
  exists.



                                               44
I.36   Social Golfers

Schedule g · s golfers in g groups of s over w weeks so that no pair plays together more than once [29].
  4 groups of 3, 4 weeks

  Social Golfers (CSPLib problem 10): schedule 12 = 4*3 golfers over 4 weeks. Each week,
  the 12 golfers are partitioned into 4 groups of 3 players each. Constraint: NO PAIR
  of golfers may be in the same group on more than one week. SAT iff a valid schedule
  exists; classic NP-hard scheduling problem.
  Return a flat list of 48 integers: entry w*12 + p gives the group (in 0..3) of golfer p
  in week w. State "UNSATISFIABLE" if no schedule exists.


I.37   Sudoku

Fill an n2 × n2 Sudoku grid (with n × n blocks) so each row, column, and block contains every value
in {1, . . . , n2 } exactly once [65].
  n = 3 (standard 9 × 9)

  Fill a Sudoku grid with block size 3 (so the full grid is 9x9, containing 9 rows, 9
  columns, and 9 non-overlapping 3x3 blocks). Each row, column, and block must contain
  every integer from 1 to 9 exactly once.
  Return a list of 81 integers (the grid in row-major order: cell at row i, column j is
  at index i*9+j), or state "UNSATISFIABLE" if no solution exists.



I.38   Van der Waerden Coloring

Color {1, . . . , n} with k colors avoiding any monochromatic arithmetic progression of length L; SAT
iff n < W (k, L) [57].
  n = 20, k = 2, L = 3 (below W (2, 3) = 9? No: SAT past W is impossible)

  Color the integers 1, 2, ..., 20 with 2 colors (numbered 0 to 1) such that NO
  monochromatic arithmetic progression of length 3 exists: there is no a >= 1, d >= 1
  with a + (2)*d <= 20 where the 3 positions a, a+d, ..., a+(2)*d all share the same color.
  Such a coloring exists iff 20 < W(2, 3). Known values: W(2,3)=9, W(2,4)=35, W(3,3)=27,
  W(2,5)=178.
  Return a list of 20 integers, each 0 or 1, representing the color of integer i+1
  (0-indexed), or state "UNSATISFIABLE" if no such coloring exists.



I.39   Vertex Cover

Decide whether a random graph admits a vertex cover of size at most k; classical NP-complete
decision [33].
  n = 30, k = 12

  Decide whether the following random graph G with 30 vertices (numbered 0 to 29) has a
  vertex cover of size at most 12: a subset S of vertices such that every edge of G has
  at least one endpoint in S, and |S| <= 12. NP-complete.
  Edges of G (<edge_count> edges): <edges>
  Return the cover as a flat 0/1 vector of length 30 (entry i is 1 iff vertex i is in S).
  The number of 1s must be at most 12. State "UNSATISFIABLE" if no such cover exists.




                                                    45
