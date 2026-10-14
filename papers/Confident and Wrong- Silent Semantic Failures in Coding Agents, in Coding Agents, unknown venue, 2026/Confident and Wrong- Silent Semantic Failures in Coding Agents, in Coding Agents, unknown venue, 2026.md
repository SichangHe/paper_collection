                                         Confident and Wrong: Silent Semantic Failures
                                         in Coding Agents

                                             Aman Mehta
                                             Snowflake AI Research
                                             aman.mehta@snowflake.com



                                                                                    Abstract

                                                  As coding agents move into production workflows, teams need to know
arXiv:2603.25764v3 [cs.SE] 21 Jun 2026




                                                  not only whether an agent completes a task, but whether its action can be
                                                  trusted. We show that completion and trustworthiness diverge sharply and
                                                  systematically. Across 1,750 trajectories on 50 SWE-bench Verified tasks, we
                                                  compare four frontier models over repeated runs and separate submit rate
                                                  from test-verified resolve rate. GPT-5 submits a patch on 100% of runs but
                                                  resolves only 44%; Llama 4 submits on 99% but resolves 18%; and Gemini,
                                                  despite submitting least often at 70%, resolves more tasks than GPT-5 (50%
                                                  versus 44%). These gaps are not random: they concentrate in one dangerous
                                                  failure mode we call silent semantic failure. Qualitatively, on a buggy task the
                                                  agent submits a plausible-looking patch on all five runs, yet none pass, the
                                                  same misinterpretation repeated rather than random error. Quantitatively,
                                                  it dominates failure, covering 80% of Llama 4’s failing runs and 68% of
                                                  GPT-5’s, and it is invisible: the outcomes are confidently and consistently
                                                  wrong, so completion-based and consistency-based monitoring both look
                                                  healthy exactly when the agent should not be trusted. Lightweight pre-
                                                  edit prompts do not close the gap. A second probe isolates the instinct to
                                                  act: given an already-fixed bug, where the right move is to abstain, most
                                                  models still edit the correct code. This action bias, acting when no action is
                                                  warranted, is exactly what completion metrics reward. The throughline is
                                                  measurement: submit rate captures action, but trust requires validity. So
                                                  evaluation must catch up: score agents by test-verified correctness over
                                                  repeated runs, report its uncertainty, and reward those that know when not
                                                  to act.


                                         1     Introduction

                                         How reliable are deployed coding agents? The answer depends entirely on what you measure.
                                         By submit rate, meaning whether the agent produces a patch, GPT-5 looks perfect: 100%
                                         across 250 runs on SWE-bench (Jimenez et al., 2024). By resolve rate, whether the patch passes
                                         the project’s tests, it drops to 44%. The gap is not noise. On 19 of 50 tasks GPT-5 submits a
                                         confident-looking patch on every run and every patch fails. An operator watching submit
                                         rate sees flawless completion; only test execution reveals the patches are wrong.
                                         This is, at heart, a measurement problem. Submit rate is a cheap, always-available indicator,
                                         and the field quietly treats it as a stand-in for what we actually care about: the agent’s ability
                                         to fix the bug. We show this stand-in has poor construct validity. It mismeasures ability, and
                                         not evenly: the error is concentrated in one specific, dangerous, and invisible failure mode.
                                         We borrow the language of measurement science and psychometrics on purpose (Messick,
                                         1989; Jacobs & Wallach, 2021). An evaluation is reliable if it gives the same score when
                                         repeated, and valid if that score reflects what we mean to measure. The two are independent:
                                         a test can be perfectly reliable yet completely invalid. Our central object, silent semantic
                                         failure, is exactly this case: an agent that reliably (5/5 runs) submits a patch that is always
                                         (0/5) wrong. It is silent (invisible to submit- or completion-based monitoring: no crash,
                                         no empty patch, the run looks done) and semantic (the patch is well-formed yet wrong in


                                                                                         1
meaning). It is the most dangerous failure mode: confidently and consistently wrong, so
reliability reads as competence with nothing to warn you.
Agent scoring also breaks the i.i.d. assumption behind single-run leaderboards: a trajectory
is a chain of dependent steps, so a model’s per-task outcome is a random variable, and
one run is a noisy estimate. Measuring agents well means estimating it from repeats, with
uncertainty, not reading it off once.
Underneath both halves of our study is one tendency, action bias: agents lean toward acting
rather than being right. When a bug exists, an over-eager agent submits a confident wrong
patch (silent semantic failure); when none exists, it edits already-correct code instead of
abstaining. Submit rate rewards the first; our specificity probe exposes the second.
We study these issues empirically across four frontier models on 50 SWE-bench Verified
tasks spanning five repositories, five runs each, plus 750 guard-intervention trajectories.
Our contributions are:

     1. A measurement framework (Section 2) that casts coding-agent evaluation as con-
        struct measurement (construct, indicator, criterion) and organizes outcomes into a
        reliability × validity grid in which silent semantic failure is the reliable-but-invalid
        cell.
     2. Convergent-validity failure of submit rate. Submit rate and test-verified resolve
        rate disagree on model ranking. GPT-5 submits 100%/resolves 44%; Llama 4
        submits 99%/resolves 18%; and although Gemini submits least often (70%), it
        resolves more tasks than GPT-5 (50% versus 44%). Bootstrap leaderboards reverse
        the GPT-5/Gemini ranking depending on the indicator.
     3. A failure taxonomy grounded in resolve rate. Silent semantic failure (5/5 submit,
        0/5 resolve) affects 33/50 Llama 4 tasks (SSFR 80%) and 19/50 GPT-5 tasks (68%),
        but only 4/50 Gemini tasks (16%). Gemini fails honestly, by abstaining.
     4. Reliability is multi-faceted, stable, but not validity. We measure consistency at
        three levels (pacing via step CV, procedure via command similarity, product via
        patch similarity) and find they are near-orthogonal (r ≤ 0.14), so step counts alone
        are insufficient. The hierarchy holds across all five repositories, yet consistency only
        amplifies whatever interpretation the model commits to.
     5. A mechanism for silent failure. Within a model, silent-failure patches are far more
        self-similar than variable-failure patches: the agent re-derives the same wrong fix
        (convergent misinterpretation, not random error). Across models, silent failures
        cluster on shared “interpretation-trap” tasks (8 tasks resolved by no model).
     6. An abstention (specificity) probe. Pre-applying the gold patch so the bug is already
        fixed, we measure whether agents recognize there is nothing to do. Models edit
        already-correct code (false action) on a large fraction of tasks, the specificity mirror
        of the same validity failure.
     7. Process measures and a null intervention. Two cheap trajectory signals (3-gram
        loop detection; trajectory length, r = −0.26) partially recover the missing validity
        signal without running tests, while two pre-edit guard interventions fail to improve
        resolve rate. Interpretation failures resist lightweight prompting.


2   A Measurement Framework for Coding Agents

Construct, indicator, criterion. We treat coding-agent capability on a task as a hidden quan-
tity θ: how likely the agent is to produce a patch that actually fixes the issue. We never see θ
directly, only indicators of it. The cheapest, the one a quick evaluation or monitoring dash-
board reaches for, is the submit rate: did the agent return a non-empty patch (exit status
== "Submitted")? Our criterion, the closest thing to ground truth, is the resolve rate: does
the patch pass the project’s full test suite under the SWE-bench harness (OpenAI, 2024)?
Construct validity asks whether the indicator tracks the criterion. It does not.


                                               2
Reliability vs. validity. An indicator is reliable if repeated runs give the same value, and
valid if that value reflects θ (Messick, 1989). The two are separate. Since we run each (model,
task) pair five times, we can place every outcome on a reliability × validity grid (populated
per model in Figure 7, Appendix D). The cell that matters most is reliable-but-invalid: the
agent returns the same confident, wrong patch every run. That is silent semantic failure, and
it is dangerous precisely because we usually read reliability as a good sign.

Scores are noisy draws, not fixed numbers. A trajectory’s steps are dependent, so each
task’s outcome is a random variable, not a fixed score. We therefore estimate its resolve
probability ptask from k repeats with bootstrap uncertainty; a single-run leaderboard reports
one draw and mistakes noise for capability. We quantify that noise with the coefficient of
variation (CV) of step counts; throughout, CV is our reliability measure and resolve rate our
validity criterion.


3   Related Work

Measurement and benchmark validity. A growing line of work treats AI benchmarks as
measurement instruments: Jacobs & Wallach (2021) import construct-validity theory into
ML, Raji et al. (2021) critique general-ability claims, Burnell et al. (2023) and Liang et al.
(2023) push instance-level, multi-metric reporting, and Kapoor et al. (2024) argue agent
evaluation should prioritize deployment-relevant metrics. We operationalize this for coding
agents: we name a concrete validity failure (the submit-rate trap), quantify it across models,
and tie it to the reliability/validity distinction (Messick, 1989).

Agent benchmarks. SWE-bench (Jimenez et al., 2024) and SWE-bench Verified (OpenAI,
2024) evaluate agents on real GitHub issues; WebArena (Zhou et al., 2024) and OSWorld (Xie
et al., 2024) target web and computer use. Most report single-run aggregates, leaving
reliability unexamined.

Consistency, agents, and safety. Variance under repetition is documented for reasoning
and QA (Wang et al., 2023; Elazar et al., 2021; Mehta, 2026); self-consistency (Wang et al.,
2023) exploits it via voting but assumes independent samples, which breaks for path-
dependent trajectories. Agent-failure studies cover error categorization (Liu et al., 2024),
recovery (Shinn et al., 2023), tool misuse (Ruan et al., 2024), and planning limits (Valmeekam
et al., 2023). We characterize when failures are reliable yet invalid: confident, consistent, and
silent.


4   Experimental Setup

Benchmark and tasks. We use SWE-bench Verified, selecting 50 tasks (10 per repository)
across five mature Python projects: django (web), sympy (symbolic math), scikit-learn (ML),
matplotlib (visualization), and astropy (astronomy), chosen for diversity in domain, size,
and bug type.

Models. We compare four models across capability and cost tiers: Claude 4.5 Sonnet
(claude-sonnet-4-5), GPT-5 (openai-gpt-5), Gemini 3.1 Pro (gemini-3.1-pro), and Llama
4 Maverick (llama4-maverick). All use hosted APIs with identical tools, system prompts,
and task descriptions. Hosted snapshots can drift, so we pin the identifiers above and
ran everything in a single 2026 window; the lack of immutable snapshot hashes is an
acknowledged limit.

Agent framework and protocol. We use mini-SWE-agent, a minimal bash-interface scaf-
fold; each action executes in an isolated Docker container with fresh repository state. For
each model–task pair we run 5 independent trials at temperature 0.5, max 250 steps. This
yields 250 runs per model (1,000 baseline trajectories), plus 750 guard trajectories (below).


                                               3
                  Table 1: Main results across 50 tasks and 5 repositories.
                  Metric              Claude    GPT-5      Llama 4    Gemini
                  Tasks                    50         50        50         50
                  Total Runs              250        250       250        250
                  Mean CV (%)            17.7       30.3      58.1       44.9
                  Median CV (%)          16.3       30.2      49.9       33.0
                  Mean Steps             53.3       10.5      28.6       78.5
                  Submit Rate            0.97       1.00      0.99       0.70
                  Resolve Rate           0.65       0.44      0.18       0.50




Figure 1: The submit-rate trap at a glance. (a) Every model submits far more often than it
resolves (bar labels are percentages); even though Gemini submits least often, it resolves
more tasks than GPT-5 (50% vs. 44%). (b) Outcome breakdown over 50 tasks: silent semantic
failure (red; 5/5 submit, 0/5 resolve) dominates Llama 4 (33 tasks) and GPT-5 (19).


Metrics. Submit rate is the fraction of runs producing a non-empty submitted patch
(the indicator). Resolve rate is the fraction of runs whose patch passes all tests under the
SWE-bench harness (OpenAI, 2024) (the criterion). Coefficient of variation of step counts,
CV = σsteps /µsteps × 100%, is our reliability measure; lower is more consistent.

Guard interventions. To test whether validity can be repaired by pre-edit prompting, we
inject two guards before the agent’s first code edit: an interpretation guard (state your
understanding of the bug and fix strategy first; run on Claude and GPT-5, 500 trajectories)
and a test-anchored guard (write and run a minimal failing test first; run on GPT-5, 250
trajectories).


5     Results

5.1   Reliability: a stable behavioral-consistency hierarchy

Table 1 shows a clear reliability hierarchy: Claude (CV 17.7%) is the most consistent, then
GPT-5 (30.3%), Gemini (44.9%), and Llama 4 (58.1%). All pairwise differences are significant
after Bonferroni correction except GPT-5 vs. Gemini and Gemini vs. Llama 4 (Appendix E),
and the ordering holds in all five repositories (Appendix C). So reliability is a stable property
of each model. But as we show next, being reliable does not make a measure valid.


                                                4
Table 2: Reliability has three facets that do not coincide. Pacing = step-count CV (lower is
more consistent); procedure = mean cross-run command-sequence similarity; product = mean
cross-run similarity of submitted patches (higher is more consistent). Pooled across all 200
(model, task) cells, step-CV correlates only weakly with command divergence (r =0.14) and
essentially not with patch divergence (r ≈0): the facets are near-orthogonal, so step counts
alone do not capture procedural or product consistency.
                                   Pacing         Procedure           Product
                  Model      Step-CV (%) ↓    Command sim. ↑      Patch sim. ↑
                  Claude               17.7                0.13           0.13
                  GPT-5                30.3                0.07           0.29
                  Gemini               44.9                0.32           0.42
                  Llama 4              58.1                0.12           0.31



Reliability is multi-faceted; step counts are only one facet. One objection is that step-
count CV is a thin measure of reliability: two runs can take the same number of steps yet run
different commands and produce different patches. So we measure reliability at three levels
(Table 2): pacing (step-count CV), procedure (how similar the command sequences are across
runs), and product (how similar the submitted patches are). The three do not line up. Across
all 200 (model, task) cells, step-CV barely correlates with command differences (r =0.14) and
not at all with patch differences (r ≈0). Claude is the most consistent in pacing but among
the least consistent in product (patch similarity 0.13): it works at a steady rhythm but reaches
the fix through genuinely different edits. Gemini is the reverse, with high patch similarity
(0.42) driven partly by repeated command loops. The lesson: no single consistency number
is enough, so we report all three and use them together below.

5.2   Validity: submit rate fails convergent validity

The indicator and the criterion disagree (Figure 1a). GPT-5 submits 100% but resolves 44%;
Llama 4 submits 99% but resolves 18%. Most tellingly, Gemini submits the least often
(70%) but resolves more tasks than GPT-5 (50% versus 44%), second only to Claude: the
indicator ranks Gemini last while the criterion ranks it second. A practitioner optimizing
submit rate would pick the wrong model.
This convergent-validity failure is not just an artifact of point estimates. In bootstrap
leaderboards (Appendices E and G), submit rate ranks GPT-5 first in 98% of resamples and
Gemini last in 100%; the resolve-rate bootstrap flips the GPT-5/Gemini order and ranks
Claude first every time. The two metrics do not even agree on the podium. Claude and
GPT-5 also look tied on submit rate (overlapping CIs) but are clearly apart on resolve rate,
so a single-run submit comparison would call that gap real when it is not.

Is submit rate a straw man? Rigorous leaderboards do report resolve rate, and we are not
claiming otherwise. We have two targets. First, in deployment monitoring there is rarely a
trustworthy test for each fix, so operators watch completion signals (did the agent return a
patch; did the run finish), which are submit-rate proxies. Second, the headline leaderboard
number is single-attempt pass@1 (official SWE-bench, SWE-bench Pro, most agent scores),
and a single run is high-variance; pass@k is the multi-run estimate we recommend, but
pass@1 still dominates. More broadly, submit rate interests us less as a flawed test surrogate
than as a window onto an action bias in evaluation: rewarding acting over being right.

5.3   Reliable but invalid: the failure taxonomy

Using resolve rates, we classify each (model, task) pair by its 5-run submission/resolution
pattern (Figure 1b): consistent resolve (5/5 resolved), variable resolve (1–4/5), silent semantic
failure (5/5 submit, 0/5 resolve), variable failure (partial submit, 0/5 resolve), and no-submit
(abstention; 0/5 submit). These map directly onto the reliability × validity grid (Figure 7).


                                               5
Figure 2: Per-task resolve distribution: how many tasks (of 50) have k of 5 runs resolve.
Mass piles up at 0/5 and 5/5 for every model, sparse in between. Reliability amplifies
whatever interpretation the model commits to: Claude peaks at 5/5, Llama 4 at 0/5.


Each model has a distinct profile (Figure 1b). Claude is healthiest (27/50 consistent resolve,
7 SSF). GPT-5 is the most concerning of the high-submit models: 19/50 tasks are silent
semantic failures, submitting on all 5 and resolving none. Llama 4 is dominated by SSF
(33/50). Gemini’s failures are split between honest abstention (5 tasks at 0/5 submit) and
variable outcomes. The per-task resolve distribution is sharply bimodal (Figure 2): for
almost every task either all five runs resolve or none do, so reliability amplifies whatever
interpretation the model commits to rather than averaging it out.
We summarize the reliable-but-invalid cell with a silent semantic failure rate (SSFR): the
fraction of non-resolving runs coming from tasks where all 5 runs submit but none resolve,
                                     Ntasks: 5/5 submit, 0/5 resolve × 5
                           SSFR =                                        .                    (1)
                                         Ntotal non-resolving runs
Llama 4’s SSFR is 80% and GPT-5’s 68%: over two-thirds of their failures are invisible to
submission-based monitoring. Claude’s is 40%; Gemini’s only 16%. This is the paper’s
central measurement finding: the most dangerous failure mode is not failing to act, but
acting reliably and wrongly, and submit-rate monitoring is blind to exactly this cell.

5.4   Why do silent failures happen? Convergent misreadings and shared traps

Failing tests is no surprise; the measurement question is why the failure is silent and reliable.
Two findings from the trajectories explain it.
(1) Within a model, the wrong patches are nearly identical. If silent failure were random
error, the five wrong patches for a task would differ. They do not. On three measures
(textual diff overlap, code-token Jaccard, sentence-embedding cosine), SSF patches are far
more alike than a cross-task baseline (Table 3): unrelated patches score near zero, while SSF
patches score many times higher. The agent rebuilds the same wrong fix each run, a fixed
misreading rather than bad luck, so reliability just reproduces the mistake.
(2) Across models, silent failures cluster on the same tasks. The SSF task-sets of GPT-5
and Llama 4 overlap heavily (Jaccard 0.49); 7 tasks are SSF for at least 3 of the 4 models, and
8 are solved by no model on any run (Figure 8). These are interpretation traps: the obvious
reading of the issue points away from the real fix. But 16 tasks trap only one model, so silent
failure has two sources, hard tasks and over-eager models, and good evaluation must vary
both.

5.5   Cheap process measures recover part of the missing signal

Can we flag the reliable-but-invalid cell without running tests? From the 1,000 baseline
trajectories we extract a few cheap features. A 3-gram loop detector (any run of 3 commands
that repeats ≥ 3 times) catches 100% of Gemini’s 0/5 no-submit (abstention) tasks, with no
false positives on Claude or GPT-5; a step-ceiling rule (>245 steps) catches 80%. Trajectory
length also predicts silent semantic failure: across the 200 (model, task) cells, shorter average


                                                 6
Table 3: Why silent failures happen: when an agent silently fails (5/5 submit, 0/5 resolve),
its five patches are far more similar to one another than unrelated patches from different
tasks (cross-task baseline), on every similarity measure: textual diff overlap, code-token
Jaccard, and sentence-embedding cosine. The agent converges on the same wrong fix rather
than failing randomly. (GPT-5 has no variable-failure tasks: it submits on every run, so all
its non-resolving tasks are silent semantic failures.)
                         SSF   Cross-run patch similarity (SSF / cross-task baseline)
             Model     tasks   Textual diff   Token Jaccard       Embedding cosine
             Claude        7    0.18 / 0.01      0.41 / 0.10              0.85 / 0.48
             GPT-5        19    0.27 / 0.01      0.36 / 0.05              0.85 / 0.53
             Gemini        4    0.39 / 0.01      0.67 / 0.09              0.91 / 0.57
             Llama 4      33    0.26 / 0.01      0.38 / 0.05              0.80 / 0.52



runs go with it (r = −0.26, p < 0.001), and silent-failure cells have slightly higher phase-mix
entropy (r = +0.20, p < 0.01). Models that lock onto a wrong reading early produce short,
confident, wrong runs. These are test-free signals that recover part of what submit rate
throws away.

5.6   Validity is not repaired by pre-edit prompting

If invalid submissions stem from interpretation errors, can a pre-edit nudge fix them? We
test two guards on GPT-5 (interpretation, test-anchored) and one on Claude (interpretation);
full numbers in Appendix B (Table 4).
Neither guard moves overall resolve rate: the interpretation guard leaves Claude at 65.2% →
64.8% and GPT-5 at 44.4% → 46.0%; the test-anchored guard leaves GPT-5 at 44.4% → 44.0%.
The test-anchored guard helps and hurts unevenly across repositories, gaining on isolated
bugs (astropy +4pp, django +6pp, matplotlib +6pp) but losing on complex suites (scikit-
learn −10pp, sympy −8pp), because writing a test first (17.2 vs 10.5 steps) burns budget on
hard tasks. It does cut GPT-5’s SSF tasks from 19/50 to 16/50. Two very different prompts
both failing moves the conclusion from “one prompt didn’t work” to “a whole class of
pre-edit prompts doesn’t repair validity.”


6     Specificity: do agents know when to abstain?

Resolve rate measures sensitivity: when a bug exists, does the agent fix it? A good capability
measure also needs specificity: when there is nothing to fix, does the agent notice and stop?
We test this directly. For a subset of tasks across repositories, we apply and commit the gold
patch before the agent starts, so the bug in the issue is already fixed; the agent still gets the
original bug report. A well-calibrated agent should reproduce the issue, see it is resolved,
and abstain (submit nothing). An over-confident one will “fix” the non-bug anyway, editing
code that is already correct. We label each run false action (submits a non-empty patch), clean
abstain (submits an empty patch), or no submit (runs out of steps without deciding).
All four models routinely act on non-bugs. On 60–90% of runs (n = 50 per model), every
model edits correct code instead of abstaining (Figure 3); only GPT-5 abstains cleanly with
any frequency (40%), yet still over-acts on the majority. “Fixing” something that is not
broken is the specificity side of the same validity failure: a metric that rewards acting even
when the right output is no change. Abstention is a real capability that submission-based
evaluation punishes.


7     Discussion: a measurement protocol

We turn the findings into a measurement protocol.


                                                7
Figure 3: Abstention probe: the gold patch is pre-applied so the bug is already fixed and the
agent should do nothing. Per-model split into false action (a spurious edit to correct code),
clean abstain (empty submit), and no submit (timeout). All four models edit correct code on
a majority of runs (n = 50 per model, five per task).


     1. Score against a criterion, not an indicator: report test-verified resolve rate; GPT-5’s
        100%/44% gap shows submit rate is far from sufficient.
     2. Estimate, don’t read off: run k ≥ 3 trials with bootstrap CIs. Best-of-3 raises Claude
        65→74% and GPT-5 44→58% (Appendix F).
     3. Report reliability beside accuracy: high agreement with low resolve is the silent-
        failure danger sign.
     4. Add test-free process measures: 3-gram loop detection (100% recall, 0% FP) and
        short-trajectory flags.
     5. Measure specificity too: an agent that cannot abstain on already-fixed code is
        miscalibrated even at high resolve rate.

Underlying all five: reliability helps only conditional on validity; absent a criterion, high
consistency just manufactures false confidence.

8   Limitations
Criterion validity. Resolve rate is an imperfect criterion (SWE-bench suites can be incom-
plete) but far closer to the construct than submit rate. Single benchmark and language. All
tasks are SWE-bench Verified Python; compiled languages (Java, C++, Rust) add a compiler
that may catch over-confident edits, so SSF rates there are an open question. Single scaffold.
One minimal scaffold (mini-SWE-agent); richer scaffolds may shift rates, though our null
guard suggests lightweight fixes are insufficient. Scale. 50 tasks is modest; we mitigate with
paired tests and bootstrap CIs. Abstention scope. The specificity probe (Section 6) uses
n = 50 per model on a 10-task subset, not the full benchmark.

Future work. Cross-language and cross-scaffold replication, structural interventions
(multi-agent debate, self-verification) for the interpretation failures prompting could not fix,
and scaling the abstention probe into a full specificity benchmark paired with resolve rate.

9   Conclusion
Submit rate measures whether a coding agent acts, not whether it is right, and the two diverge
dangerously. It reverses the GPT-5/Gemini resolve ranking, and its errors concentrate in
silent semantic failure (SSFR up to 80%): reliable, confident, test-failing patches where agents
repeat the same wrong fix. As agents move into production, measurement must follow:
test-verified, multi-run estimation reporting reliability and specificity, not the submit-rate
trap.


                                               8
References
Ryan Burnell, Wout Schellaert, John Burden, Tomer D Ullman, Fernando Martinez-Plumed,
  Joshua B Tenenbaum, Danaja Rutar, Lucy G Cheke, Jascha Sohl-Dickstein, Melanie
  Mitchell, et al. Rethinking the reporting of evaluation results in AI. Science, 380(6641):
  136–138, 2023.
Yanai Elazar, Nora Kassner, Shauli Ravfogel, Abhilasha Ravichander, Eduard Hovy, Hin-
  rich Schütze, and Yoav Goldberg. Measuring and improving consistency in pretrained
  language models. Transactions of the Association for Computational Linguistics (TACL), 9:
  1012–1031, 2021.
Abigail Z Jacobs and Hanna Wallach. Measurement and fairness. In ACM Conference on
 Fairness, Accountability, and Transparency (FAccT), pp. 375–385, 2021.
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and
  Karthik Narasimhan. Swe-bench: Can language models resolve real-world github issues?
  International Conference on Learning Representations (ICLR), 2024.
Sayash Kapoor, Benedikt Stroebl, Zachary S Siegel, Nitya Nadgir, and Arvind Narayanan.
  AI agents that matter. arXiv preprint arXiv:2407.01502, 2024.
Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, Dilara Soylu, Michihiro Yasunaga,
  Yian Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Kumar, et al. Holistic evaluation of
  language models. Transactions on Machine Learning Research (TMLR), 2023.
Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang
  Ding, Kaiwen Men, Kejuan Yang, et al. Agentbench: Evaluating llms as agents. Interna-
  tional Conference on Learning Representations (ICLR), 2024.
Aman Mehta. When agents disagree with themselves: Measuring behavioral consistency in
 LLM-based agents. arXiv preprint arXiv:2602.11619, 2026.
Samuel Messick. Validity. In Robert L Linn (ed.), Educational Measurement, pp. 13–103.
  American Council on Education and Macmillan, 3rd edition, 1989.
OpenAI.       Introducing swe-bench verified.                  https://openai.com/index/
 introducing-swe-bench-verified/, 2024.
Inioluwa Deborah Raji, Emily M Bender, Amandalynne Paullada, Emily Denton, and Alex
  Hanna. AI and the everything in the whole wide world benchmark. In Advances in Neural
  Information Processing Systems (NeurIPS) Datasets and Benchmarks Track, 2021.
Yangjun Ruan, Honghua Dong, Andrew Wang, Silviu Pitis, Yongchao Zhou, Jimmy Ba,
  Yann Dubois, Chris J Maddison, and Tatsunori Hashimoto. Identifying the risks of LM
  agents with an LM-emulated sandbox. International Conference on Learning Representations
  (ICLR), 2024.
Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
 Reflexion: Language agents with verbal reinforcement learning. Advances in Neural
 Information Processing Systems (NeurIPS), 2023.
Karthik Valmeekam, Matthew Marquez, Alberto Olmo, Sarath Sreedharan, and Subbarao
  Kambhampati. On the planning abilities of large language models: A critical investigation.
 Advances in Neural Information Processing Systems (NeurIPS), 2023.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha
  Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in
  language models. International Conference on Learning Representations (ICLR), 2023.
Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao,
  Toh Jing Hua, Zhoujun Cheng, Dongchan Shi, Zhaoyang Lu, et al. Osworld: Benchmark-
  ing multimodal agents for open-ended tasks in real computer environments. Advances in
  Neural Information Processing Systems (NeurIPS), 2024.


                                             9
Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng,
  Yonatan Bisk, Daniel Fried, Uri Alon, et al. Webarena: A realistic web environment for
  building autonomous agents. International Conference on Learning Representations (ICLR),
  2024.


A    Case Studies

Silent semantic failure (astropy-13236). Adding a structured numpy array to an Astropy
Table silently converts it to NdarrayMixin; the fix is to remove the conversion (4 lines). Claude
instead read the task as “add a deprecation warning but preserve behavior,” spending 30–50
steps per run on a FutureWarning. All 5 runs submitted; none resolved. GPT-5 made the
same interpretation error in 7 steps (submit 5/5, resolve 0/5). This is the reliable-but-invalid
cell in miniature: perfect submission, zero resolution, no behavioral variance to signal the
problem.

The read-loop trap (matplotlib-25311). A draggable-legend figure cannot be pickled; the
fix needs getstate / setstate on an offsetbox class. Claude (5/5, mean 74 steps) and
GPT-5 (5/5, mean 10 steps) resolved it. Gemini submitted 0/5, exhausting the 250-step limit
on every run in a degenerate read loop, cycling the same grep/sed commands without ever
editing (Figure 4). This failure is costly but honest: 0/5 submit, no variance suggesting a
retry would help, and caught perfectly by the 3-gram loop detector.




Figure 4: Gemini trajectory timelines on matplotlib-25311 (one row per run; teal=explore,
blue=understand, yellow=edit, red=verify). All five runs are degenerate read-loops with no
edit phase.


B   Guard Intervention Details




                                               10
Table 4: Effect of guard interventions on GPT-5 and Claude. Neither interpretation guard
nor test-anchored guard significantly improves resolve rate.
                                     GPT-5            GPT-5        GPT-5
                    Metric         Baseline   Interp. Guard   Test Guard
                    Resolve Rate      0.444           0.460        0.440
                    Submit Rate       1.000           0.996        0.976
                    Mean Steps         10.5            11.7         17.2
                    SSF tasks        19/50             n/a        16/50
                                    Claude           Claude
                    Metric         Baseline   Interp. Guard
                    Resolve Rate      0.652           0.648         n/a
                    Submit Rate       0.968           0.972         n/a
                    Mean Steps         53.3            50.3         n/a


C   Cross-Repository Reliability




Figure 5: Mean CV by repository and model; the reliability hierarchy holds across all five
repositories.




Figure 6: Steps vs. behavioral consistency (CV); each point is one task. Claude clusters high-
step/low-CV; GPT-5 is fast with moderate variance; Llama spans high variance; Gemini
ranges widely. Speed and reliability do not imply validity.




                                              11
                       Table 5: Mean CV (%) by repository and model.
                     Repository     Claude    GPT-5     Llama 4     Gemini
                     django            17.8      26.6        54.0       46.4
                     sympy             23.4      29.3        64.7       46.8
                     scikit-learn      18.0      26.8        67.9       50.4
                     matplotlib        13.9      36.7        44.4       35.4
                     astropy           15.2      32.2        59.8       45.5


D    Supplementary Consistency Figures




Figure 7: The reliability × validity grid populated with task counts per model (of 50).
Each model’s mass sits in a different quadrant: Claude in reliable-and-valid (27 consistent
resolves), Llama 4 and GPT-5 in the reliable-but-invalid silent semantic failure cell (33 and 19),
and Gemini spread toward the honest-failure quadrant.




Figure 8: Cross-model silent-semantic-failure overlap. (a) Jaccard overlap of SSF task-sets:
GPT-5 and Llama 4 share most. (b) Number of tasks that are SSF for exactly k models; 7
tasks trap ≥ 3 models (shared interpretation traps), while many are model-specific.




                                               12
Figure 9: Per-task behavioral consistency (CV) across four models (50 tasks each). The gap
between Claude and the others is visually stark.




Figure 10: The three facets of reliability per model. (a) procedure (command-sequence) and
product (patch) similarity; (b) pacing (step CV). The facets do not coincide.




Figure 11: Per-task step-CV vs. patch divergence (pooled, colored by model). The near-zero
correlation shows step-count consistency does not capture patch-level consistency.



                                           13
Figure 12: Cross-run patch similarity for silent-semantic-failure tasks vs. variable-failure
tasks. SSF patches are far more self-similar: agents converge on the same wrong fix.




                                            14
E   Statistical Details

Pairwise CV comparisons (paired t-tests on per-task CV, 50 shared tasks; Bonferroni
α = 0.0083): Claude vs. GPT-5 ∆ = −12.6%, p < 0.001; Claude vs. Gemini ∆ = −27.2%,
p < 0.001; Claude vs. Llama 4 ∆ = −40.4%, p < 0.001; GPT-5 vs. Gemini ∆ = −14.6%,
p = 0.009 (borderline); GPT-5 vs. Llama 4 ∆ = −27.8%, p < 0.001; Gemini vs. Llama 4
∆ = −13.2%, p = 0.02 (n.s. after correction).

Submit-rate bootstrap (n = 1000): Claude 0.969 [0.936, 0.996] (rank-1 in 1.7%); GPT-5
1.000 [1.000, 1.000] (98.3%); Gemini 0.697 [0.600, 0.796] (0%); Llama 4 0.988 [0.972, 1.000]
(0%).

Resolve-rate bootstrap (n = 1000): Claude 0.651 [0.600, 0.700] (rank-1 in all samples);
Gemini 0.498 [0.420, 0.560]; GPT-5 0.444 [0.360, 0.520]; Llama 4 0.180 [0.100, 0.260]. The
resolve-rate bootstrap reverses the GPT-5 vs. Gemini ranking relative to submit rate.

F   Cost-Benefit of Multi-Run Evaluation




                                            15
Table 6: Cost-benefit analysis of multi-run evaluation strategies on submit rate. Cost is mean
actual API cost per task. Majority vote uses hard majority; Best-of-k is the oracle upper
bound (task counts as submitted if any of k runs submits). Resolve-rate-based best-of-k
values appear in the recommendations text.
    Model       Strategy               Submit       Cost ($)      Rel. Cost      Gain/$
    Claude      Single (k=1)              0.968         3.26            1.0x         n/a
    Claude      Majority (k=3)            0.974         9.78            3.0x        0.001
    Claude      Majority (k=5)            0.980        16.31            5.0x        0.001
    Claude      Best-of-3                 1.000         9.81            3.0x        0.003
    Claude      Best-of-5                 1.000        16.31            5.0x        0.002
    GPT-5       Single (k=1)              1.000          0.62           1.0x         n/a
    GPT-5       Majority (k=3)            1.000          1.85           3.0x        0.000
    GPT-5       Best-of-5                 1.000          3.08           5.0x        0.000
    Llama 4     Single (k=1)              0.988          0.34           1.0x         n/a
    Llama 4     Majority (k=3)            1.000          1.03           3.0x        0.012
    Llama 4     Best-of-3                 1.000          1.09           3.2x        0.011
    Gemini      Single (k=1)              0.696         3.56            1.0x         n/a
    Gemini      Majority (k=3)            0.712        10.68            3.0x        0.001
    Gemini      Best-of-3                 0.840        10.32            2.9x        0.014
    Gemini      Best-of-5                 0.900        17.80            5.0x        0.011

G    Leaderboard Bootstrap




                                             16
Table 7: Leaderboard contextualization via bootstrap resampling (1000 samples) on submit
rate. Rank-k is the fraction of bootstrap samples in which the model achieved that rank.
Single-run reliability is the fraction of runs agreeing with the 5-run majority vote.
  Model       Mean Submit              95% CI      Rank-1     Rank-2     Reliability
  Claude                0.969    [0.936, 0.996]      1.7%      14.5%           0.972
  GPT-5                 1.000    [1.000, 1.000]     98.3%       1.7%           1.000
  Llama 4               0.988    [0.972, 1.000]      0.0%      83.8%           0.988
  Gemini                0.697    [0.600, 0.796]      0.0%       0.0%           0.876




                                          17
