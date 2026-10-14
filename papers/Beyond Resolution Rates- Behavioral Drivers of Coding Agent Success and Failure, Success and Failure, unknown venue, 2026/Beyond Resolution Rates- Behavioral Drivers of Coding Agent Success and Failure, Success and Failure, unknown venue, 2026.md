                                            Beyond Resolution Rates: Behavioral Drivers of Coding Agent
                                                               Success and Failure
                                                                   Tural Mehtiyev                                                     Wesley Assunção
                                                           North Carolina State University                                      North Carolina State University
                                                                 Raleigh, NC, USA                                                     Raleigh, NC, USA

                                        Abstract                                                                   rates increase sharply on harder benchmarks [22], highlighting the
                                        Coding agents represent a new paradigm in automated software en-           need for a deeper understanding of their behavior.
                                        gineering, combining the reasoning capabilities of Large Language             To contribute to the construction of reliable agentic systems,
                                        Models (LLMs) with tool-augmented interaction loops. However,              understanding why and how coding agents fail is therefore criti-
                                        coding agents still have severe limitations. Top-ranked LLM-based          cal. The “why” refers to the underlying causes of failure, namely
                                                                                                                   whether failures arise from task characteristics (e.g., hidden depen-
arXiv:2604.02547v1 [cs.SE] 2 Apr 2026




                                        coding agents still fail on over 20% of benchmarked problems. Yet,
                                        we lack a systematic understanding of why (i.e., the causes) agents        dencies, test requirements), limitations of the LLM (e.g., reasoning
                                        fail, and how failure unfolds behaviorally. We present a large-scale       errors, poor generalization), or constraints imposed by the agent
                                        empirical study analyzing 9,374 trajectories from 19 agents (8 cod-        framework (e.g., tool orchestration, context management). Addition-
                                        ing agent frameworks, 14 LLMs) on 500 tasks. We organize our               ally, the “how” refers to the observable behavioral process through
                                        analysis around three research questions. First, we investigate why        which failure unfolds, primarily captured in the agent’s trajectory
                                        agents fail on specific tasks and find that patch complexity alone         as a sequence of actions such as exploration, editing, testing, and
                                        does not explain difficulty: 12 never-solved tasks require only sim-       iteration [30]. While prior work has studied outcome-level met-
                                        ple patches and were considered easy by human annotators, yet              rics such as resolution rates and fault localization accuracy [19],
                                        all agents fail due to gaps in architectural reasoning and domain          classified failure root causes through manual inspection [15], or
                                        knowledge. Second, we examine how behavioral patterns differen-            analyzed behavioral patterns such as trajectory length and action
                                        tiate success from failure. The widely reported correlation between        sequences in small agent samples [2, 6, 14, 16], these studies rarely
                                        trajectory length and failure reverses direction once task difficulty      connect the why and how dimensions of failure while controlling
                                        is controlled, revealing it as a confound. Instead, trajectory structure   for task difficulty on a large-scale dataset. As a consequence, there
                                        discriminates consistently: agents that gather context before editing      is a lack of systematic understanding of how specific behaviors
                                        and invest in validation succeed more often, and these strategies are      lead to particular failure causes, and which aspects of agent design
                                        agent-determined rather than task-adaptive. Third, we disentangle          or capability should be improved. This gap limits both scientific
                                        LLM capability from framework design and find that the LLM is the          insight and practical progress, as improving agents requires not
                                        primary driver of both outcome and behavior: agents sharing the            just knowing that they fail, but understanding the mechanisms by
                                        same LLM agree on far more tasks than agents sharing the same              which those failures occur.
                                        framework, and the framework performance gap shrinks with each                In this paper, we address this gap by conducting a large-scale
                                        generation of LLM improvement. Framework prompts do influence              empirical study of coding agent behavior. We analyze 9,374 tra-
                                        agent tactics, but this influence diminishes with stronger LLMs.           jectories from 19 agents spanning 8 frameworks and 14 LLMs, all
                                                                                                                   evaluated on the same 500 SWE-bench Verified tasks. In the studied
                                                                                                                   dataset, every agent attempts every task, enabling within-task com-
                                                                                                                   parisons that control for task difficulty, an important confound that
                                        1    Introduction                                                          has undermined prior work. Our goal is to move beyond outcome-
                                        Coding agents represent a new paradigm in automated software               level benchmarking and instead understand the behavioral drivers
                                        engineering, combining the reasoning capabilities of Large Lan-            of success and failure. We focus on three core research questions:
                                        guage Model (LLM) with tool-augmented interaction loops that               RQ1. Why do coding agents fail on certain tasks? Prior work
                                        allow them to operate directly on codebases [13]. Unlike traditional       mainly approximates difficulty through proxy metrics such as patch
                                        code generation systems that produce isolated snippets [5, 10],            size [22] or human-estimated solve time [9, 31]. We test whether
                                        coding agents function as autonomous developers [28, 29]: they             this holds across all 500 tasks and investigate edge cases in which
                                        interpret natural-language issue reports, explore repositories, ex-        some tasks are considered “easy” yet every agent fails. RQ2. How
                                        ecute code, run tests, and iteratively refine patches to resolve a         do the behavioral patterns differentiate success from failure?
                                        task. Frameworks such as SWE-agent [29], OpenHands [26], and               We use within-task paired comparisons to test whether the widely-
                                        AutoCodeRover [33] have demonstrated the feasibility of this ap-           reported length–failure correlation survives difficulty controls, and
                                        proach, leading to increasing adoption in real-world workflows.            characterize how different agents fail on the same tasks. RQ3. Does
                                        Ehsani et al. [8] report over 33k agent-authored pull requests on          LLM capability or framework design drive agent success? By
                                        GitHub, and the SWE-bench leaderboard [11] tracks over 80 unique           leveraging natural variation in LLMs within the same frameworks,
                                        approaches across dozens of competing systems [17]. Despite this           we disentangle the relative contributions of model capability and
                                        rapid progress and growing ecosystem, coding agents remain far             system architecture.
                                        from reliable. State-of-the-art agents still fail on more than 20% of         Through both quantitative and qualitative analysis, our large-
                                        SWE-bench Verified tasks [23] (as of February 2026), and failure           scale, controlled study links coding agent behavior to outcomes
Preprint, 2026, Raleigh, NC, USA                                                                                                                                          Tural Mehtiyev and Wesley Assunção


                                     SWE-agent + Claude 4 Sonnet                                                                                  SWE-agent + GPT-4
                                          37 actions | RESOLVED                                                                                     36 actions | FAILED
                                       UNDERSTAND (steps 0-3)                                                                                    CREATE (steps 0-2)
    FIX REPRODUCE UNDERSTAND




                                 0   view /testbed                          Browse repo root                                         0      create reproduce_issue.py                Acts before reading




                                                                                                                         CREATE
                                 1   view django/template/                  Navigate to module                                       1      edit reproduce_issue.py
                                 2   view defaultfilters.py                 Open relevant file                                       2      python reproduce_issue.py          PASS Bug confirmed
                                 3   view lines 95-207                      Targeted line range                                                  FIND FILE (steps 3-6)
                                        REPRODUCE (steps 4-7)                                                                        3      search_dir "floatformat"                 Find the file




                                                                                                                         FIND
                                 4   create reproduce_issue.py            Repro after reading                                        4      open defaultfilters.py                   Correct file found
                                 5   python reproduce_issue.py       PASS Bug confirmed                                             5-6     scroll_down (x2)                         Browse to target lines
                                 6   create debug_issue.py                Investigate root cause                                              EDIT THRASH (steps 7-34)
                                 7   python debug_issue.py           PASS                                                            7      edit 154:160 (attempt 1)            FAIL Syntax error
                                                FIX (step 8)                                                                         8      edit 154:160 (attempt 2)            FAIL Syntax error
                                 8   str_replace defaultfilters.py          1 edit on source                                         9      edit 154:160 (attempt 3)            FAIL Syntax error




                                                                                                                      THRASH
                                                                                                                       EDIT
                                           VERIFY (steps 9-30)                                                                      ...     ...
                                 9   python reproduce_issue.py       PASS                                                           33      edit 154:160 (attempt 27)           FAIL Syntax error
                               10-13 4 custom test scripts           PASS Edge cases                                                34      edit 154:160 (attempt 28)           FAIL Syntax error
    VERIFY




                               14-17 pytest + runtests (x4)          PASS Project test suite                                        35      exit_cost                                Gives up
                               18-30 more tests + final verify       PASS
                               31-36 cleanup + submit

                                                                     Read / explore               Edit / create                Test / run            Repetitive loop

Figure 1: Contrasting agent trajectories on django-15863. Both agents use the SWE-agent framework. Claude 4 Sonnet (left)
follows a structured workflow: browse the codebase, reproduce the bug, make one surgical edit, then run several verification
cycles before submitting. GPT-4 (right) finds the correct file but then edits the code many times, producing 28 syntax errors,
without ever running the project’s test suite.


across diverse systems. The results lead to several key findings:                                                 return. Thus, it is paramount to understand why and how coding
(i) simple-patch tasks can defeat every agent when they require                                                   agents fail.
architectural reasoning rather than complex edits; (ii) trajectory                                                   To illustrate what can influence an agent’s success, we focus on
length is an ambiguous failure signal: its direction reverses depend-                                             the task django-15863 in SWE-bench Verified [11, 20]: a 1-line fix
ing on whether one controls for agent identity or task difficulty;                                                that causes floatformat to drop precision on Decimal numbers.
(iii) trajectory structure distinguishes success from failure. Agents                                             Three agents in the dataset failed to solve this task. This indicates
that gather context before editing and validate more succeed con-                                                 that the task may be too complex for the same agents (RQ1: Task
sistently, and these strategies are fixed across task complexity; and                                             difficulty). Figure 1 shows trajectories for two agents working on
(iv) LLM capability dominates over framework design. As LLMs                                                      the task django-15863, one with Claude 4 Sonnet (on the left) and
improve, framework differences shrink and agents converge.                                                        one with GPT-4 (on the right), but both using the same framework.
                                                                                                                  The two agents produced similar numbers of actions in their tra-
2            Background and Motivation                                                                            jectories: 37 for Claude 4 Sonnet and 36 for GPT-4. The agent with
Agents are built on top of a framework (also referred to as scaf-                                                 Claude 4 Sonnet makes one edit on the source code, has zero syn-
fold in this paper; e.g., SWE-agent [29] and OpenHands [26]) that                                                 tax errors, and solves the task successfully. GPT-4 makes many
orchestrates tool use, manages context, and structures the problem-                                               edits, with 28 syntax errors, and consequently fails. We observe in
solving loop, wrapped around an LLM that generates each action                                                    this example that, despite having similar numbers of steps in their
in the trajectory [25]. To solve software development tasks, agents                                               trajectories, the actions differ significantly. The trajectory of the
produce a trajectory, a step-by-step sequence of actions (file reads,                                             agent with Claude 4 Sonnet follows a “understand > reproduce
edits, test executions, search queries) and the environment’s re-                                                 > fix > verify” workflow, whereas the agent with GPT-4 follows
sponses (compiler output, test results, error messages). Trajectories                                             “create > find > edit”. Thus, we conjecture that the success
are the behavioral equivalent of a developer’s actions, capturing                                                 or failure of an agent may be related to the patterns of actions in
not just whether the agent succeeded, but how it approached the                                                   its trajectory (RQ2: behavioral patterns). Finally, agents rely on
problem. This behavioral record is the primary data source for                                                    a Framework and have an LLM, which produces the trajectories.
understanding agent strategies, failure modes, and intervention                                                   Therefore, we hypothesize that both LLM and framework, and their
opportunities [2, 16].                                                                                            interactions with the tasks, may contribute to success or failure in
   Coding agents show promising results on several benchmarks [11,                                                ways that existing work has not explored (RQ3: LLM capability
23], but they still present significant limitations. As of February 2026,                                         and framework design).
the best submission on the SWE-bench Verified leaderboard [23]
fails on more than 20%, meaning that even the strongest agent fails
on nearly one in five tasks. When an agent fails, it wastes comput-                                               3        Study Design
ing resources, developer review time, and organizational trust. In                                                This section describes the data collection, trajectory encoding,
the SWE-bench Verified dataset we study, 12.4% of total compute                                                   feature-extraction pipeline, and analytical methods to answer the
is spent on the 55 tasks that no agent solves, resources with zero                                                three RQs of our study.
Behavioral Drivers of Coding Agent Success and Failure                                                                      Preprint, 2026, Raleigh, NC, USA


Table 1: Enriched encoding: 13 sub-phase symbols. Each sym-                    Table 2: Task-level features (90 total) extracted per task, or-
bol is classified from the raw .traj data using deterministic                  ganized by source.
regex rules on the action and observation fields.
                                                                                Category           Count Representative features
 Symbol Meaning                            Source in trajectory                 Patch complexity       12 lines added/deleted, hunks, files modified,
 Lb        Locate → browse whole file view w/o –view_range                                                multi-file flag, hunk size, directory depth
 Lt        Locate → targeted read     view with –view_range, goto               Test demand            15 fail-to-pass     count,     test     assertions,
 Ls        Locate → with search       grep, search_dir, search_file                                       parametrized tests, nesting depth
                                                                                Issue / prompt         53 prompt length (words, sentences), has stack-
 P         Patch (clean edit)              edit with no error in observation
                                                                                                          trace, has repro code, code-to-text ratio,
 Ps        Patch → syntax error            edit followed by SyntaxError
                                                                                                          specificity score, lexical diversity
 Pi        Patch → import error            edit followed by ImportError
                                                                                Metadata               10 repository, version, issue age, repo popular-
 Pr        Re-patch (same file)            edit on previously edited file
                                                                                                          ity, domain
 Vp        Validation passed          test run with no error
 Vf        Validation → test failure  test run with test failure
 Ve        Validation → runtime error test run with RuntimeError
                                                                               complexity features follow the metrics used as difficulty proxies in
 Vr        Reproduction script        reproduce_*.py or similar
                                                                               prior SWE-bench studies [9, 22, 31]; (ii) Test demand features cap-
 E         Environment setup               pip, apt, conda, build              ture how demanding the task’s test infrastructure is, using the fail-
 G         General / other                 submit, cd, pwd, think              to-pass test structure defined by SWE-bench [11]; (iii) Issue/prompt
                                                                               features are informed by the bug report quality literature, which
                                                                               shows that steps to reproduce, stack traces, and code examples are
3.1     Data Collection
                                                                               the most impactful elements for bug resolution [1, 27]; and (iv) Meta-
Our study relies on 9,374 trajectories from 19 agents on the 500               data features include repository, version, and issue age to control
SWE-bench Verified tasks [11, 20], which target real-world bugs                for project-level variation, as cross-project studies show that dif-
across 12 open-source Python repositories. Agents represent 8 cod-             ferent projects have fundamentally different difficulty profiles [35].
ing agent frameworks: SWE-agent, OpenHands, Trae, Skywork,                     Features are computed deterministically using regex-based parsers
CodeSweep, EPAM-AI, SAGE, and Sonar. Additionally, the dataset                 on the issue text and diff-based analysis on the patches. The full
represents 14 LLMs: four Claude variants, three GPT variants, and              list of features is in our supplementary material [18].
seven others (e.g., Kimi-K2, Devstral, Qwen-32B, and Doubao). All
trajectories are collected from submissions to the SWE-bench Ver-              3.4    Analytical Design
ified leaderboard [23], downloaded from the public experiment
bucket maintained by the benchmark authors [11]. Each agent at-                3.4.1 RQ1: Task difficulty and agent resolution analysis. To answer
tempts all 500 tasks, yielding a complete 𝑎𝑔𝑒𝑛𝑡 × 𝑡𝑎𝑠𝑘 matrix, with            RQ1, we conducted a quantitative and qualitative analysis of tasks
minor gaps: three agents have 443–499 runs due to timeouts or in-              considered “easy”, yet all agents failed to solve. We isolate 12 never-
frastructure failures. Since every task is attempted by every agent,           solved tasks that have simple patches (single file, ≤10 changes) and
this enables within-task comparisons that control for task difficulty,         compare them against 25 always-solved tasks with similar patch
a confound that prior studies with 1–3 agents could not address.               characteristics using Mann-Whitney 𝑈 tests and Cliff’s 𝛿 across
                                                                               90 task-level features. Where quantitative features do not fully
3.2     Trajectory Encoding                                                    explain the gap, we turn to qualitative trajectory analysis: for each
                                                                               of the 12 tasks, we examine the trajectories by the best-performing
Previous work classifies agent trajectories at varying granularity:
                                                                               agents and compare their submitted patch against the gold patch
Bouzenia and Pradel [2] define eight action types (Explore, Lo-
                                                                               to identify the failure mode.
cate, Search, Reproduce, Generate fix, Run tests, Refactor, Explain),
while Graphectory [14] abstracts these into four steps (Localization,          3.4.2 RQ2: Paired comparison of agent trajectories. Comparing re-
Patching, Validation, General). Both focus solely on the agent’s               solved and failed trajectories requires controlling for two confounds
actions. We expand this by jointly encoding the agent action and               simultaneously: agent identity, since different agents have different
the environment’s response. For example, a clean patch (i.e., edit)            capabilities; and task difficulty, since harder tasks produce more
is encoded as P, while an edit that triggers a SyntaxError is en-              failures. Thus, we design the analysis around two approaches, for-
coded as Ps, and a test run that passes is Vp (i.e., Validation pass),         malized in Algorithm 1. Approach A fixes the agent and compares
while one that fails is Vf (i.e., Validation fail). Our encoding, shown        its resolved vs. failed trajectories across tasks, controlling for agent
in Table 1, comprises 13 sub-step symbols that capture execution               identity but confounded by task difficulty. Approach B fixes the task
quality and error type information while remaining compact and                 and compares resolved vs. failed trajectories from different agents,
human-readable.                                                                controlling for task difficulty but confounded by agent identity.
                                                                                   We apply this analytical design to answer RQ2, using trajectory
3.3     Task-Level Feature Extraction                                          length as the metric 𝑚 for RQ2a and per-symbol enriched encoding
For each of the 500 tasks, we extract 90 features. Table 2 summarizes          frequency (e.g., proportion of steps spent on validation) for RQ2b.
the four categories and representative features. Our feature selec-            We set 𝑛 min = 5 to ensure stable estimates. Prior studies [2, 16] com-
tion draws on established dimensions from prior work: (i) Patch                pare successes and failures without this control, so their findings
Preprint, 2026, Raleigh, NC, USA                                                                                                          Tural Mehtiyev and Wesley Assunção


Algorithm 1 Two-Approach Success/Failure Comparison                                                      55 never-solved
                                                                                           60             (11% of tasks)
                                                                                                55
Require: Trajectories T , contested tasks C (tasks with both re-                                                                                           29 always-solved
   solved and failed outcomes), behavioral metric 𝑚, min. sample                           50                                                                (6% of tasks)




                                                                         Number of Tasks
                                                                                                                                                     37        37             39
   size 𝑛 min , significance level 𝛼                                                       40                                                                       33             33
Ensure: Per-approach effect sizes and significance                                         30                                                   27        27             29             29
      A positive 𝛿 or Δ indicates 𝑚 is higher for failed trajectories.                                                                  22 24
                                                                                           20             17
                                                                                                                         13 13 11 15
                                                                                                     9         10 11 9
         — Approach A: fix agent, vary all tasks (one-sided) —                             10
    1: for each agent 𝑎 ∈ Agents do                                                        0
                                                                                                0%       10% 20% 30% 40% 50% 60% 70% 80% 90% 100%
    2:    𝑅𝑎 ← {𝑡 ∈ T : 𝑡 .agent = 𝑎, 𝑡 .resolved}                                                                             Resolution Rate
    3:    𝐹𝑎 ← {𝑡 ∈ T : 𝑡 .agent = 𝑎, 𝑡 .failed}
    4:    if |𝑅𝑎 | < 𝑛 min or |𝐹𝑎 | < 𝑛 min then skip                    Figure 2: Task difficulty distribution across 500 SWE-bench
    5:    𝛿𝑎 , 𝑝𝑎 ← Mann-Whitney 𝑈 (one-sided: 𝐹 > 𝑅) + Cliff’s 𝛿        Verified tasks.
       on 𝑚(𝐹𝑎 ) vs 𝑚(𝑅𝑎 )
    6: Aggregate: count agents with 𝛿𝑎 > 0 (𝑝 < 𝛼) vs 𝛿𝑎 < 0 (𝑝 < 𝛼)     Table 3: Twelve never-solved tasks with simple patches. The
                                                                         Human label column shows the official difficulty annotation
         — Approach B: fix task, vary agents (two-sided) —               from SWE-bench Verified’s human annotators [20]. By every
    7: for each task 𝑡 ∈ C do                                            prior difficulty metric and by human judgment, these are
    8: 𝑅𝑡 ← {𝜏 ∈ T : 𝜏 .task = 𝑡, 𝜏 .resolved}                           easy tasks. Zero of 19 agents solve any of them.
    9: 𝐹𝑡 ← {𝜏 ∈ T : 𝜏 .task = 𝑡, 𝜏 .failed}
10:    Δ(𝑡) ← mean(𝑚(𝐹𝑡 )) − mean(𝑚(𝑅𝑡 ))
                                                                                    Task                          Lines      Hunks         Files          Res.       Human label
11: 𝑝 ← Wilcoxon signed-rank (two-sided) on {Δ(𝑡)}𝑡 ∈ C
12: Report: Δ̄, 𝑝, fraction of tasks with Δ(𝑡) > 0                                  django-11477                         2          1            1        0/19       15 min–1 hr
                                                                                    django-15098                         2          1            1        0/19       15 min–1 hr
                                                                                    django-16667                         2          1            1        0/19       15 min–1 hr
                                                                                    sympy-20428                          2          1            1        0/19       15 min–1 hr
are confounded by task difficulty. Our complete agent×task matrix
                                                                                    matplotlib-23476                     3          1            1        0/19       <15 min
makes both within-agent and within-task comparisons possible.                       matplotlib-23299                     5          2            1        0/19       15 min–1 hr
3.4.3 RQ3: Agent framework vs. LLM capability. We exploit a nat-                    django-13794                         6          1            1        0/19       <15 min
ural experiment: by holding the framework constant and varying                      sympy-21930                          6          3            1        0/19       15 min–1 hr
                                                                                    django-10999                         7          1            1        0/19       <15 min
the LLM, we isolate the LLM effect; by holding the LLM constant
                                                                                    django-14792                         7          1            1        0/19       <15 min
and varying the framework, we isolate the framework effect. We                      matplotlib-21568                     7          1            1        0/19       15 min–1 hr
compare both factors using aggregate resolution rates and per-task                  django-15252                         8          1            1        0/19       15 min–1 hr
outcome agreement. Finally, we analyze the prompt’s effect on
overall agent strategy.
                                                                         groups (mean total changes: 4.75 vs. 3.76; with Mann-Whitney 𝑝 =
4        Results and Discussion                                          0.24, Cliff’s 𝛿 = 0.24). Of the 90 task-level features we investigated,1
This section presents the results and discussion organized per RQ.       Table 4 presents the five ones with significant results (𝑝 < 0.05), all
                                                                         of which are test-demand or issue-description features. However,
4.1        RQ1: Why do coding agents fail on certain                     three of the twelve never-solved tasks have the minimum possible
           tasks?                                                        test demand (FTP = 1), and when we restrict the comparison to very
                                                                         simple patches (≤5 changes), the test-demand differences become
4.1.1 Difficulty Landscape and Edge-Case Selection. We classify
                                                                         non-significant. Quantitative features alone do not fully distinguish
each of the 500 tasks by its resolution rate across all agents. The
                                                                         these edge cases, motivating a detailed manual qualitative analysis
distribution is bimodal (Figure 2): 55 tasks (11%) are never solved by
                                                                         of the agent trajectories themselves.
any agent, 416 (83%) are contested, and 29 (6%) are always solved.
   Among the 55 never-solved tasks, 12 require only a single-file        4.1.2 Trajectory Analysis: The Architectural Reasoning Gap. Fig-
patch of ≤10 total changes. Table 3 presents these tasks. Focusing on    ure 3 illustrates what we mean by architectural reasoning gap through
patch complexity, as in prior work [9, 22, 31], these are considered     the task matplotlib-23476. On HiDPI screens (e.g., M1 Mac), mat-
simple tasks by humans and are expected to be solved at high rates       plotlib internally doubles the figure DPI for retina display but
across our dataset. Therefore, these edge cases invalidate the prior     tracks the original value in a separate attribute (_original_dpi).
work’s conclusions that correlate patch complexity with difficulty,      The bug is that Figure.__getstate__(), the method Python’s
suggesting that something beyond patch size must also matter.            pickle protocol calls during serialization, saves the doubled DPI
   To further investigate these cases, we compare the 12 never-          instead of the original. Each pickle/unpickle cycle doubles the
solved tasks with the 25 always-solved tasks that have similarly         DPI (200→400→800→ . . .). The 3-line gold patch resets _dpi to
simple patches (single file, ≤10 changes). The results show that
patch complexity is statistically indistinguishable between the two      1 The complete list of features is available in our supplementary material [18].
Behavioral Drivers of Coding Agent Success and Failure                                                                                              Preprint, 2026, Raleigh, NC, USA


Table 4: The 5 features (of 90 tested) reaching 𝑝 < 0.05 between                matplotlib-23476: DPI doubles on unpickle, M1 Mac (0/19 agents, 3-line fix)
                                                                                                   Agent fixes the display scaling; gold patch fixes the serialization
12 never-solved and 25 always-solved simple-patch tasks. No
                                                                                                                 Symptom: DPI doubles each unpickle
patch or metadata feature is significant.                                                                              200 → 400 → 800 → 1600 → OverflowError
                                                                                                                         Only on HiDPI displays (M1 Mac retina)


      Feature                 Never      Always          Cliff’s 𝛿     𝑝
      Fail-to-pass count         2.42        1.24     +0.61 (L)      <0.001                   Mechanism: HiDPI DPI doubling
                                                                                                 matplotlib doubles fig._dpi for retina display
      FTP test files             2.17        1.20     +0.55 (L)      0.001                     but stores _original_dpi for the pre-scaling value
      Test patch files           1.58        1.00    +0.33 (M)       0.003
      Test patch changes        21.25       12.64    +0.46 (M)       0.025                                                                                    agent
      Has repro code             0.67        0.24    +0.43 (M)       0.014
                                                                                      Root cause: __getstate__ saves doubled DPI
                                                                                                             figure.py:3023
                                                                                           pickle serializes the doubled _dpi, not _original_dpi
Table 5: Architectural gap across all 12 never-solved simple-
patch tasks. The best agent found the gold-patch file in 12/12
                                                                                                             gold
and edited it in 10/12, yet failed every time.
                                                                                    Gold edits figure.py __getstate__                          Agent edits backend code
                                                                                             state["_dpi"] = state.get(                            backend_macosx.py, backend_agg.py,
  Task              Gap type                              Root cause                        '_original_dpi', state['_dpi'])                           backend_bases.py, _macosx.m
                                                                                           Reset DPI before serialization                            Tries to prevent the DPI doubling
  django-11477      Caller → Callee
  django-13794      Symptom → Root cause
  django-14792      Consumer → Producer                                                        The gap: Agent attacks the DPI scaling in display backends.
  mpl-23299         Add → Remove behavior                                                       Gold patch accepts the doubling but fixes what gets serialized.
                                                                                             Requires knowing pickle uses __getstate__ and _original_dpi exists.
  mpl-23476         Display → Serialization               Architectural judg-
  sym-20428         Operations → Type system              ment (10 tasks)
  django-15252      Components → Orchestrator                                   Figure 3: Representative case study: matplotlib-23476. The
  django-10999      Issue’s fix → Redesign                                      agent fixes DPI scaling in display backends (4 files); the gold
  sym-21930         Local + general → Local only                                patch fixes the serialization in __getstate__ (3 lines). Both
  django-16667      Wrong control flow                                          address the same bug from different architectural levels.
  django-15098      Abandoned correct fix                 Behavioral
  mpl-21568         Wrong TeX commands                    Domain knowledge


_original_dpi before serialization. The best agent (61 steps) cor-
rectly finds figure.py, understands the DPI doubling, but tries
to prevent the doubling from happening by editing four backend                      Answering RQ1
files (backend_macosx.py, backend_agg.py, backend_bases.py,
                                                                                    Patch complexity alone does not explain why agents fail.
_macosx.m). It attacks the display scaling layer instead of the seri-
                                                                                    Twelve never-solved tasks require simple patches (≤10
alization layer. Both the agent and the gold patch address the same
                                                                                    changes, single file) and were labeled easy by human anno-
symptom, but at different architectural levels: the agent tries to
                                                                                    tators. Quantitative analysis shows test demand and issue-
stop the value from changing, while the fix ensures the changed
                                                                                    description features distinguish these from always-solved
value is not persisted. The qualitative analysis for all 12 edge cases
                                                                                    tasks, but the deeper cause is an architectural reasoning
is available in our supplementary material [18].
                                                                                    gap: agents correctly localize the bug and produce plausible
    The pattern observed in the example above is systematic. We
                                                                                    fixes, but intervene at the wrong architectural layer (10/12
examined the trajectories of the top-performing agents on all 12
                                                                                    tasks). They patch symptoms rather than root causes.
never-solved simple-patch tasks (Table 3), comparing their submit-
ted patches against the gold patch. Table 5 summarizes the results.
In every case, the agent correctly localizes the bug, finding the
gold-patch file in 12 of 12 tasks and editing it in 10 of 12. Yet it               Implications. RQ1 reveals a ceiling that even top-performing
consistently intervenes at the wrong level. In 10 of 12 tasks, the              agents may not overcome. The 12 never-solved simple-patch tasks
failure traces back to architectural judgment: the agent patches the            fail not because agents lack the right tool or take too few steps, but
symptom (the caller, the consumer, the display layer) while the gold            because they intervene at the wrong architectural layer. Agents
patch fixes the root cause (the callee, the producer, the serialization         find the correct file and produce plausible fixes, yet consistently
layer), or the agent cannot judge the right scope for its fix. The              patch the symptom rather than the root cause. This architectural
remaining two tasks involve a behavioral failure (abandoning a                  reasoning gap suggests that scaling model size or training on more
correct fix mid-trajectory) and a domain knowledge gap (TeX math-               code may not suffice; agents may need explicit mechanisms for rea-
mode formatting). The agent’s fixes compile and pass its own tests;             soning about component boundaries, ownership, and the direction
they fail because the SWE-bench test suite validates behavior at                of causal dependencies in a codebase. For benchmark designers,
the root-cause level.                                                           this implies that test-demand metrics and architectural complexity
                                                                                indicators should complement patch size as difficulty measures.
Preprint, 2026, Raleigh, NC, USA                                                                                                                                Tural Mehtiyev and Wesley Assunção


Table 6: Length–failure effect. Approach A (top): for each                                                                Framework                                                             LLM
                                                                                                                    80      SWE-agent                                                claude-4-sonnet   gpt-4
                                                                                                                            OpenHands                                                claude-opus-4.5   kimi-k2
agent, mean steps of resolved vs. failed runs across all tasks;                                                             EPAM-AI                                                  claude-3.5-s      doubao
                                                                                                                                                                                     claude-3-opus     lm-32b
every agent shows failures are significantly longer (𝑝 < 0.001,                                                     70      Trae                                                     gpt-5             qwen-32b
                                                                                                                            Sonar                                                    gpt-4o            devstral




                                                                                Trajectory Length (encoded steps)
                                                                                                                            SAGE
one-sided Mann-Whitney 𝑈 ). Approach B (bottom): for each                                                                   CodeSweep
                                                                                                                    60      Skywork
contested task, mean steps of resolved vs. failed agents; the
effect reverses: resolved trajectories are longer on 63% of tasks
                                                                                                                    50
(𝑝 < 10−8 , two-sided Wilcoxon signed-rank).
                                                                                                                    40
Agent          LLM                    Res. Rate % Longer Cliff’s 𝛿 Sig.
                                                                                                                    30
      Approach A: fix agent, vary all tasks (one-sided Mann-Whitney 𝑈 )
Sonar     claude-opus-4.5                 79.2%     +30.5%      +0.434    ***                                       20
Trae      doubao-seed-code                78.5%     +65.1%      +0.316    ***
OpenHands claude-opus-4.5                 78.3%     +29.6%      +0.403    ***                                       10
EPAM-AI   claude-4-sonnet                 76.8%     +19.9%      +0.389    ***                                            0-20%          20-40%            40-60%              60-80%                   80-100%
                                                                                                                                          Task Resolution Rate (across all agents)
Trae      claude-4-sonnet+opus            75.4%     +36.7%      +0.503    ***
SAGE      claude-4.5+gpt-5                73.0%     +14.5%      +0.224    ***
                                                                                           Figure 4: Trajectory length by task difficulty for all 19 agents.
OpenHands gpt-5                           71.8%     +14.0%      +0.234    ***
OpenHands claude-4-sonnet                 70.4%     +16.0%      +0.264    ***              Every agent takes more steps on harder tasks (all Spearman
SWE-agent claude-4-sonnet                 66.6%     +17.5%      +0.297    ***              𝜌 < 0, all 𝑝 < 0.01). This universal length–difficulty coupling
OpenHands kimi-k2                         65.4%     +27.6%      +0.388    ***              explains the confounding reversal: length reflects task diffi-
CodeSweep kimi-k2                         53.4%     +89.2%      +0.383    ***              culty, not strategy quality.
OpenHands claude-3.5-sonnet               53.0%     +82.2%      +0.393    ***
OpenHands devstral-small                  46.8%     +44.3%      +0.430    ***
SWE-agent lm-32b                          40.2%    +111.9%      +0.567    ***
Skywork   qwen-32b                        38.1%     +18.9%      +0.173    ***                 Approach B (fix task, vary agents). To control task difficulty, we
SWE-agent claude-3.5-sonnet               33.6%     +35.2%      +0.364    ***              compare resolved and failed trajectories within each contested task.
SWE-agent gpt-4o                          24.9%     +54.4%      +0.386    ***              For each of the 416 contested tasks, we compute the mean trajectory
SWE-agent gpt-4                           22.6%     +59.9%      +0.506    ***              length for resolved and failed agents separately. Interestingly, the
SWE-agent claude-3-opus                   15.1%     +20.4%      +0.506    ***              result reverses: resolved agents average 44.0 steps vs. 39.6 for failed
  Approach B: fix task, vary agents (416 contested tasks, paired Wilcoxon)                 agents (10.0% longer). On 263 of 416 tasks (63%), resolved trajecto-
                                                                                           ries are longer (𝑝 = 1.9 × 10−9 , two-sided Wilcoxon signed-rank).
Within-task aggregate                       —    −10.0%             — ***
                                                                                           On the same task, the agents that succeed take more steps than the
               *** 𝑝 < 0.001, ** 𝑝 < 0.01, * 𝑝 < 0.05.
                                                                                           agents that fail.
                                                                                              The two approaches give opposite answers, revealing that tra-
                                                                                           jectory length simultaneously reflects task difficulty and agent
4.2     RQ2: How do the behavioral patterns                                                capability. This ambiguity motivates RQ2b: we need behavioral
        differentiate success from failure?                                                dimensions that do not co-vary with task difficulty.

4.2.1 RQ2a: Trajectory Length Shows a Confounding Reversal Prior                         4.2.2 RQ2b: Distinguishing Successful Strategies from Failed Ones.
work reports that failed agent trajectories are substantially longer                     We examine how agents allocate their first 10 steps between reading
than successful ones. Majgaonkar et al. [16] find 12.6–82.5% longer                      and patching, and how this relates to resolution rate.
failed trajectories across agents on SWE-bench. However, these                              Context gathering and patch intensity. Figure 6a shows that agents
comparisons pool trajectories across tasks of varying difficulty                         delaying their first edit succeed more (𝜌 = +0.68, 𝑝 < 0.001): agents
without controlling for it. We apply two approaches (see Section 3.4)                    at the top-right (e.g., claude-opus-4.5 at step 9.4) resolve most tasks,
to investigate whether this finding holds.                                               while those at the bottom-left (e.g., claude-3-opus at step 0) fail
   Approach A (fix agent, vary tasks). We replicate the cross-task                       most. To illustrate this trend, Figure 5 presents two agents with the
finding across all agents on SWE-bench Verified. Table 6 shows                           same number of steps (32 each) on astropy-13579 but diverge en-
that for every agent, failed trajectories are significantly longer                       tirely: CodeSweep/kimi-k2 explores the codebase first (4 Lb steps),
(𝑝 < 0.001, one-sided Mann-Whitney 𝑈 ), with percentage gaps                             struggles through a patch-fail loop, and eventually breaks through
from +14.0% to +111.9%. The effect is universal: regardless of frame-                    to a passing test; SWE-agent/gpt-4 patches immediately on step 1
work or LLM, when a given agent fails, it takes more steps than                          and enters a P→Ve spiral from which it never recovers. The inverse
when it succeeds. However, Approach A is confounded by task diffi-                       of context gathering is opening patch intensity (Figure 6b): agents
culty. Figure 4 shows the source: for every agent, trajectory length                     that front-load patching in the first 10 steps succeed less (𝜌 = −0.78,
increases with task difficulty (𝜌 from −0.13 to −0.57, all 𝑝 < 0.01).                    𝑝 < 0.001). These results show how an agent spends its opening
Tasks with a lower resolution rate produce longer trajectories re-                       steps is strongly predictive of its overall success.
gardless of outcome, so the within-agent “failures are longer” effect                       Validation effort. We examine how much of the trajectory agents
may partly reflect that agents fail on harder (and therefore longer)                     spend on validation and how this relates to success. Validation ef-
tasks.                                                                                   fort (Figure 6c) correlates positively with resolution rate (𝜌 = +0.50,
Behavioral Drivers of Coding Agent Success and Failure                                                                                                   Preprint, 2026, Raleigh, NC, USA


                  Same Task (astropy-13579) | Same Length (32 steps)
                                Different LLM → Different Strategy → Different Outcome                        For validation effort (Figure 7c), strong agents validate 35–37% of
                CodeSweep + kimi-k2                                    SWE-agent + gpt-4                      steps across all complexity bins, while weak agents stay at 12–19%.
                      32 steps | RESOLVED ✓                                  32 steps | FAILED ✗
                                                                                                              In all three figures, the vertical separation between agents (the
                          START                                               START
                                                                                                              level) is large, but the slope within each agent is near zero. This
                               s1-4                                                s1
                                                                                                              means the behavioral differences we observe are agent-determined
                                                                                                              rather than task-specific adaptations. Agents apply a fixed strategy
                                                                Syntax error on first try (1 step)
              Explore codebase (4 steps)
                    Lb Lb Lb Lb                                               Ps — no exploration first,
                                                                            jumps straight to patching
                                                                                                              regardless of what the task demands, suggesting that current agent
                                                                                                              designs lack mechanisms to assess task complexity and adjust their
                               s5                                                  s2-3
                                                                                                              approach accordingly.
              First patch attempt (1 step)                         Patch → test PASS (2 steps)
                     1 clean edit (P)                               P → Vp (partial success)
                                                                                                                    Answering RQ2
                               s6-17                                               s4-5


            PATCH-FAIL LOOP (12 steps)
                                                                                                                    Trajectory length is an ambiguous discriminator: the di-
                                                                 Patch → runtime error (2 steps)
                    7× re-edit (Pr), 5× runtime error (Ve)
                      Trying different approaches,                          P → Ve                                  rection reverses depending on whether agent identity or
                          each fails but learns
                                                                                                                    task difficulty is controlled. Trajectory structure discrimi-
                               s18                                                 s6-9
                                                                                                                    nates consistently: agents that gather context before edit-
               First test PASS ✓ (1 step)                      3 blind patches → test pass (4 steps)                ing, avoid premature patching, and invest in validation
                  Vp — breakthrough!                         P P P → Vp (no validation between edits)
                                                                                                                    succeed more. All three dimensions are agent-determined
                               s19-21                                              s10-16                           and stable across task complexity, indicating that agents
                                                                  PATCH-FAIL LOOP (7 steps)
                                                                                                                    employ fixed strategies that do not adapt to a given task.
              Refine + validate (3 steps)                                    P→Ve, P→Ve, P→Pi, Vp
                     P → Vp → P                                           Patches without reading code,
                                                                           runtime errors accumulate



                               s22-29                                              s17-28                        Implications. RQ2 has several practical implications. First, tra-
                                                               ENDLESS PATCH→FAIL (12 steps)
                                                                                                              jectory length should not be used as a standalone signal for failure
          Debug remaining failures (8 steps)
                        Vf, Pr, Pr, Vf, Pr, Vf, Pr, Pr
                                                                        P→Ve × 6 (six consecutive attempts)
                                                                       Never recovers — same error pattern    detection and monitoring. Second, the structural dimensions we
                                                                           repeats without adaptation
                                                                                                              identify offer a more reliable alternative. The opening strategy
                               s30                                                 s29-32
                                                                                                              (read-first vs patch-first) is observable within the first 10 steps and
              Final test PASS ✓ (1 step)                          Give up, browse files (4 steps)             correlates with the outcome across all agents. A monitoring sys-
                                                                           Ls Ls Lb Lb
                     all tests green                                (too late — budget spent)                 tem that detects premature patching in the opening steps could
                               s31-32
                                                                                                              flag runs unlikely to succeed before significant compute is spent.
                                                                                                              Finally, the strategy stability finding (Figure 7) shows that agents
                 SUBMIT ✓ (2 steps)                                                                           use fixed strategies regardless of task complexity, suggesting that
                                                                                                              agent designers should focus on building adaptive strategies that
                                                                                                              adjust their approach to task requirements rather than adopting a
Figure 5: Same task and length (32 steps), different agent, dif-
                                                                                                              one-size-fits-all workflow.
ferent outcome. Left: CodeSweep/kimi-k2 explores, struggles,
breaks through (Vp), submits. Right: SWE-agent/gpt-4 skips
exploration, enters an endless P→Ve spiral, never recovers.
                                                                                                              4.3     RQ3: Does LLM capability or framework
                                                                                                                      design drive agent success?
                                                                                                              To answer this question, we first compare resolution rates across
𝑝 < 0.05), ranging from 0.1% (Trae/doubao) to 39.3% (Sonar/claude-                                            LLMs and frameworks in our dataset. Figure 8 presents the resolu-
opus-4.5). One outlier stands out: Trae/doubao achieves 78% res-                                              tion rate for all 19 agents. Within the same framework, swapping
olution with near-zero validation, suggesting its LLM produces                                                the LLM produces large shifts: 51.5 pp across 6 LLMs in SWE-agent,
correct patches without test-driven iteration. At the other end, SWE-                                         31.5 pp across 6 in OpenHands. Holding the LLM constant, the
agent/gpt-4 validates only 13% of steps and resolves 23%. These                                               framework effect is smaller: 3.8 pp for claude-4-sonnet, 19.4 pp for
results indicate that investing more trajectory steps in validation                                           claude-3.5-sonnet. This gap narrows as LLMs improve (19.4 pp →
is associated with higher success, though sufficiently strong LLMs                                            3.8 pp → 0.9 pp across three generations), and at the frontier, agents
can bypass this need.                                                                                         from 5 different frameworks converge to within 10 pp of the best.
   Task-agnostic agent strategies. A natural question is whether                                                 Per-task agreement confirms LLM dominance. To move beyond
agents adjust the three behavioral dimensions above (i.e., con-                                               aggregate resolution rates, we measure per-task outcome agree-
text gathering, patch intensity, and validation effort) based on                                              ment: for each pair of agents sharing the same LLM (or the same
task characteristics. Figure 7 tests this by plotting each dimen-                                             framework), the fraction of 500 tasks on which both agents produce
sion against patch complexity (lines changed) for six representative                                          the same outcome (both resolve or both fail). Figure 9 shows the
agents. For context gathering (Figure 7a), the lines are flat: claude-                                        results. When the LLM is held constant, and the framework varies
3-opus edits at step 0 on every task regardless of complexity, while                                          (Figure 9a), agreement is high and increases with LLM capability:
OpenHands/claude-4-sonnet waits until step 9.5 on every task. For                                             71% for claude-3.5-sonnet, 85–88% for claude-4-sonnet (3 pairs),
opening patch intensity (Figure 7b), the same pattern holds: agents                                           and 93% for claude-opus-4.5. When the framework is held constant,
that patch aggressively do so on simple and complex tasks alike.                                              and the LLM varies (Figure 9b), agreement drops substantially and
       Preprint, 2026, Raleigh, NC, USA                                                                                                                                                                                                                                            Tural Mehtiyev and Wesley Assunção

                                      (a) Context Gathering vs Success                                                                          (b) Opening Patch Intensity vs Success                                                                                    (c) Validation Effort vs Success
                         80                                                                                                 80                                                                                                           80
                                                                                                                                                                                               = -0.78, p < 0.001
                         70                                                                                                 70                                                                                                           70

                         60                                                                                                 60                                                                                                           60
Resolution Rate (%)




                         50                                                                                                 50                                                                                                           50

                         40                                                                                                 40                                                                                                           40

                         30                                                                                                 30                                                                                                           30

                         20                                                                                                 20                                                                                                           20
                                                                         = +0.68, p < 0.001                                                                                                                                                                                                                 = +0.50, p < 0.05
                              0        2            4             6             8         10                                            0         5       10       15       20        25       30       35     40                                         0         5       10       15     20       25          30   35        40
                                           First Edit Step (out of first 10)                                                                      Opening Patch Intensity (% of first 10 steps)                                                                         Validation Effort (% of trajectory steps)

                                                                                                                                                                          Framework
                                                                                      SWE-agent                                    OpenHands            EPAM-AI            Trae            Sonar        SAGE          CodeSweep                                 Skywork
                                                                                                                                                                          LLM Family
                                                                                                     claude-4-sonnet                                  claude-3.5-s           gpt-5            gpt-4          doubao         qwen-32b
                                                                                                     claude-opus-4.5                                  claude-3-opus          gpt-4o           kimi-k2        lm-32b         devstral



       Figure 6: Three structural dimensions of RQ2b across all agents. (a) Context gathering: agents that delay their first edit succeed
       more (𝜌 = +0.68, 𝑝 < 0.001). (b) Opening patch intensity: agents that spend more of their first 10 steps patching succeed less (𝜌 =
       −0.78, 𝑝 < 0.001). (c) Validation effort: agents that spend more of their trajectory on validation succeed more (𝜌 = +0.50, 𝑝 < 0.05)

                                    (a) Context Gathering by Task Complexity                                                                  (b) Opening Patch Intensity by Task Complexity                                                                            (c) Validation Effort by Task Complexity
                         10
                                                                                                                                   40
                                                                                                                                                                                                                                                     35
                         8
                                                                                                     Opening Patch Intensity (%)




                                                                                                                                   30                                                                                                                30
First Edit Step (0-10)




                                                                                                                                                                                                                             Validation Effort (%)
                         6                              claude-4-son (SWE)                                                                    claude-4-son (SWE)
                                                        gpt-4 (SWE)                                                                           gpt-4 (SWE)
                                                        claude-3-opu (SWE)                                                                    claude-3-opu (SWE)                                                                                     25
                                                        claude-4-son (Ope)                                                         20         claude-4-son (Ope)
                                                        devstral-sma (Ope)                                                                    devstral-sma (Ope)
                         4                              claude-3.5-s (Ope)                                                                    claude-3.5-s (Ope)
                                                                                                                                                                                                                                                     20
                                                                                                                                   10                                                                                                                                                       claude-4-son (SWE)
                         2                                                                                                                                                                                                                                                                  gpt-4 (SWE)
                                                                                                                                                                                                                                                     15                                     claude-3-opu (SWE)
                                                                                                                                                                                                                                                                                            claude-4-son (Ope)
                                                                                                                                                                                                                                                                                            devstral-sma (Ope)
                         0                                                                                                          0                                                                                                                                                       claude-3.5-s (Ope)
                              1-5               6-15                    16-50                  51+                                      1-5                        6-15                       16-50                   51+                                     1-5                   6-15                    16-50                    51+
                                           Patch Complexity (lines changed)                                                                                    Patch Complexity (lines changed)                                                                                  Patch Complexity (lines changed)

      Figure 7: Strategy stability across task complexity for 6 representative agents (3 SWE-agent in red, 3 OpenHands in blue).
      (a) Context gathering, (b) opening patch intensity, and (c) validation effort are plotted against patch complexity (lines changed).


      spreads widely: 47–85% across 15 LLM pairs in SWE-agent and 66–                                                                                                                  claude-4-sonnet, the same switch yields only a 4 pp improvement
      88% in OpenHands. The density distributions in Figure 9b show that                                                                                                               in resolution. Stronger LLMs develop their own strategy and are
      most LLM pairs agree on only 60–80% of tasks, far below the 85–93%                                                                                                               less susceptible to prompt-level steering.
      seen when the same LLM is used across frameworks. This confirms
      that the LLM, not the framework, is the primary determinant of                                                                                                                            Answering RQ3
      which tasks get solved.
         Prompt influence diminishes with LLM capability. We examine                                                                                                                            The LLM is the primary driver of both outcome and be-
      how much the framework’s system prompt shapes agent behav-                                                                                                                                havior; the framework’s contribution shrinks with each
      ior by comparing the same LLM on SWE-agent vs. OpenHands                                                                                                                                  LLM generation. Two agents sharing the same LLM agree
      (Figure 10). These two prompts differ substantially: SWE-agent’s                                                                                                                          on 85–93% of tasks regardless of framework, whereas two
      is 350 characters, OpenHands’ is 5,602. Each prompt does steer                                                                                                                            agents sharing the same framework but different LLMs
      the agent toward different tool usage patterns (e.g., SWE-agent                                                                                                                           agree on only 47–88% (Figure 9). The framework perfor-
      produces more reproduction scripts, OpenHands produces more                                                                                                                               mance gap narrows from 19.4 pp to 3.8 pp to 0.9 pp across
      search actions). However, the total amount of validation work is                                                                                                                          3 successive Claude generations. Framework prompts do
      nearly identical across frameworks (18.2 vs. 20.0 actions per trajec-                                                                                                                     shape tool choices but not overall effort, and this shaping
      tory), indicating that the prompts change which tools the agent uses                                                                                                                      effect diminishes as LLMs grow stronger.
      but not how much work it does. Crucially, this prompt influence
      is capability-dependent: for claude-3.5-sonnet, switching frame-                                                                                                                    Implications. RQ3 shows that at the current frontier, investing
      works yields an additional 20 pp improvement in resolution, but for                                                                                                              in better LLM reasoning will yield larger returns than redesigning
 Behavioral Drivers of Coding Agent Success and Failure                                                                                                                                                                                                   Preprint, 2026, Raleigh, NC, USA


                                                       SWE-agent              CodeSweep
                                                       OpenHands              EPAM-AI                                                                           Sonar / claude-opus-4.5
                                                                                                                                                                                                               prompt detail adds overhead (60 vs. 56 median steps) without im-
                                                       Trae                   SAGE
                                                       Skywork                Sonar                                                                             Trae / doubao-seed-code                        proving outcomes. Prior work has shown that LLMs are highly
                                                                                                                                                                OpenHands / claude-opus-4.5                    sensitive to prompt formatting [21] and that longer inputs can de-
                                                                                                                                                            EPAM-AI / claude-4-sonnet
                                                                                                                                                                                                               grade reasoning performance [12], though larger models exhibit
                                                                                                                                                           Trae / claude-4-sonnet+opus
                                                                                                                                                        SAGE / claude-4.5+gpt-5                                enhanced robustness to prompt variations [34]. Our finding extends
                                                                                                                                                       OpenHands / gpt-5                                       this to the agent setting: for strong LLMs, lean prompts may be
                                                                                                                                                      OpenHands / claude-4-sonnet
                                                                                                                                                                                                               preferable, as the model’s own reasoning compensates for the lack
                                                                                                                                                SWE-agent / claude-4-sonnet
                                                                                                                                              OpenHands / kimi-k2                                              of explicit guidance while verbose prompts add procedural over-
                                                                                                  CodeSweep / kimi-k2                                                                                          head. The effect is capability-dependent, however: weaker LLMs
                                                                                                 OpenHands / claude-3.5-sonnet
                                                                                                                                                                                                               (claude-3.5-sonnet) do benefit from richer prompts, gaining 19.4 pp
                                                                                          OpenHands / devstral-small
                                                                                    SWE-agent / lm-32b                                                                                                         from the same framework switch.
                                                                                Skywork / qwen-32b
                                                                           SWE-agent / claude-3.5-sonnet
                                                                  SWE-agent / gpt-4o
                                                             SWE-agent / gpt-4
                                                   SWE-agent / claude-3-opus
                                                                                                                                                                                                               5    Limitations and Threats to Validity
                                                                                                                                              Within 10 pp of best
                                                                                                                                           (8 agents, 5 frameworks)
                                                                                                                                                                                                                  Internal validity. Our study uses observational data, which may
                                                                                                                                                                                                               introduce confounds. While within-task comparisons control for
                                          10            20          30         40          50                                    60              70          80           90                                   task difficulty, other factors, such as tool API differences (e.g., edit
                                                                                    Resolution Rate (%)
                                                                                                                                                                                                               vs. str_replace) and framework prompting, may influence behav-
Figure 8: Resolution rate for 19 agents on SWE-bench Verified                                                                                                                                                  ior. We mitigate this through cross-framework comparisons with
(500 tasks), colored by framework.                                                                                                                                                                             shared LLMs and within-framework LLM variation, but cannot fully
                                                                                                                                                                                                               eliminate residual confounding. Our trajectory encoding relies on
                                                                                                                                                                                                               deterministic regex parsing, which may introduce minor classifica-
                               (a) Same LLM, different frameworks                                                                      (b) Same framework, different LLMs
                          80                                                     cl-opus-4.5                                                                                                                   tion errors (18/9,374 failures). Additionally, agent trajectories were
                                                                                 (93%, 1 pair)                                   90
                          75                                                                                                                                                               Trae                collected at different points in time, so differences in API versions,
                                                                                                 Framework resolution rate (%)




                                              cl-4-sonnet                                                                                                                                  (87%, 1 pair)
                                           (85 88%, 3 pairs)                                                                     80
LLM resolution rate (%)




                          70                                                                                                                                                                                   hardware, or SWE-bench infrastructure could affect results. We
                                                                                                                                 70
                          65
                                                                                                                                 60                                                       OpenHands            mitigate this by analyzing only final submitted trajectories under
                          60                   kimi-k2                                                                                                                                    (66 88%, 15 pairs)
                                               (77%, 1 pair)
                                                                                                                                 50                                                                            identical evaluation conditions (the SWE-bench harness). Because
                          55                                                                                                                                                         SWE-agent
                                                                                                                                 40                                                  (47 85%, 15 pairs)        we observe each agent on only a single run per task, we cannot
                          50
                          45      cl-3.5-sonnet                                                                                  30                                                                            measure the stochastic variance inherent in LLM-based agents.
                                  (71%, 1 pair)
                                     75           80         85          90
                                                                                                                                 20
                                                                                                                                      40        50         60        70        80         90                   Prior work [3] shows that repeated runs can change outcomes; our
                                  Per-task outcome agreement (%)                                                                              Per-task outcome agreement (%)
                                                                                                                                                                                                               single-run design may therefore over- or under-attribute failures
                                                                                                                                                                                                               to deterministic causes.
Figure 9: Per-task outcome agreement. (a) Same LLM across                                                                                                                                                         Construct validity. Our 13-symbol trajectory encoding captures
frameworks: agreement increases with LLM capability.                                                                                                                                                           actions and outcomes but abstracts away finer-grained differences
(b) Same framework across LLMs: agreement is lower and                                                                                                                                                         in reasoning and chain-of-thought quality. Metrics such as trajec-
more variable, shown as density distributions over all LLM                                                                                                                                                     tory length and validation effort are proxies for strategy and may
pairs.                                                                                                                                                                                                         not fully capture underlying cognition. We mitigate this by combin-
                                                                                                                                                                                                               ing multiple behavioral dimensions with qualitative analysis. The
                                                                                                                                                                                                               classification of tasks into “never-solved,” “contested,” and “always-
the orchestration scaffold. The convergence pattern reinforces this:                                                                                                                                           solved” is population-dependent: a different set of agents could
as LLMs improve, the gaps in the framework shrink. Framework                                                                                                                                                   shift these categories. Similarly, our 90 task features are computed
engineering is not irrelevant, but its marginal value diminishes                                                                                                                                               from observable artifacts (patches, issues, metadata) and may miss
with each generation of LLM. For practitioners selecting an agent,                                                                                                                                             latent difficulty factors such as conceptual reasoning complexity or
this finding suggests that the choice of LLM matters more than the                                                                                                                                             implicit domain knowledge not reflected in the issue text.
choice of framework: allocating budget toward a stronger model                                                                                                                                                    External validity. Our results are based on 500 Python tasks
is likely to produce larger gains than switching scaffolds. For re-                                                                                                                                            across 12 open-source repositories from SWE-bench Verified and
searchers, this result implies that comparing two agents without                                                                                                                                               may not generalize to other programming languages, proprietary
controlling for the underlying LLM conflates model capability with                                                                                                                                             codebases, or development settings.
system design. Future empirical studies should adopt factorial de-                                                                                                                                                Conclusion validity. We use non-parametric statistical tests (Mann-
signs (LLM × framework) to isolate each factor’s contribution. Our                                                                                                                                             Whitney 𝑈 , Wilcoxon signed-rank) and effect sizes (Cliff’s 𝛿) over
results also challenge the assumption that more detailed system                                                                                                                                                a large dataset (9,374 trajectories), supporting robust comparisons.
prompts lead to better agent performance. SWE-agent provides                                                                                                                                                   However, some analyses involve small samples: the 12 never-solved
a minimal prompt (350 characters), while OpenHands prescribes                                                                                                                                                  simple-patch tasks (RQ1) and the 25 always-solved tasks limit sta-
an 8-phase workflow in 5,602 characters—a 16× difference. Yet for                                                                                                                                              tistical power for subgroup comparisons. We complement these
claude-4-sonnet, both produce near-identical core behavioral met-                                                                                                                                              with qualitative analysis to strengthen conclusions. For RQ3, the
rics and only a 4% resolution difference (Figure 10). The additional                                                                                                                                           number of same-LLM and same-framework pairs is constrained
Preprint, 2026, Raleigh, NC, USA                                                                                                                 Tural Mehtiyev and Wesley Assunção



                                                               </>                  SWE-agent
                                                                           Total instructions: ~350 characters
             Opening                      Step 1: Explore        Step 2: Reproduce                       Step 3: Edit           Step 4: Verify                Step 5: Edge Cases
    "You are a helpful             "find and read code      "Create a script to                "Edit the sourcecode of   "Rerun your reproduce           "Think about edgecases
    assistant that can             relevant to the          reproduce the error and            the repo to resolve the   script and confirm the          and make sure your fix
    interact with a                <pr_description>"        execute it"                        issue"                    error is fixed!"                handles them as well"
    computer to solve
    tasks."




                                                               </>                  OpenHands
                                                                 Total instructions: 5,602 characters (8 XML sections)
             Opening                         <ROLE>                  <EFFICIENCY>                       <QUALITY>              <WORKFLOW>                         <DEBUG>
    "You are OpenHands             "assist users by         "Use efficient tools               "Write clean, efficient   "1. EXPLORATION                 "Step back and reflect
    agent, a helpful AI            executing commands,      like find, grep, and               code...focus on making    2. ANALYSIS                     on 5-7 different
    assistant that can             modifying code..."       git commands with                  the minimal changes       3. TESTING                      possible sources of the
    interact with a                                         appropriate filters"               needed"                   4. IMPLEMENTATION               problem"
    computer to solve                                                                                                    5. VERIFICATION"
    tasks."




Figure 10: System prompt comparison for claude-4-sonnet on SWE-agent (top) vs. OpenHands (bottom). Quoted text extracted
verbatim from trajectory files. Despite a 16× difference in instruction length (350 vs. 5,602 characters), the LLM produces
near-identical core behavioral metrics on both frameworks.


by the available leaderboard submissions, which limits the gener-                                ensembling open-source agents that individually score at most
alizability of the agreement analysis to specific LLM–framework                                  27.3%, demonstrating that task-level agreement across agents is
combinations rather than all possible pairings.                                                  low. However, DEI treats each agent as monolithic and does not
                                                                                                 decompose whether the disagreement stems from the LLM or the
6     Related Work                                                                               framework. We address this gap by measuring per-task outcome
                                                                                                 agreement separately for same-LLM/different-framework pairs and
Three lines of work study aspects of coding agent performance:
                                                                                                 same-framework/different-LLM pairs, showing that LLM identity
    Task difficulty characterization. Prior work primarily defines task
                                                                                                 predicts task-level outcomes more than framework identity.
difficulty using patch-based metrics. Multi-SWE-bench [31] cate-
                                                                                                    Across all three lines of work, no prior study has combined
gorizes tasks by human-estimated resolution time, showing that
                                                                                                 within-task behavioral analysis with cross-framework LLM decom-
harder tasks involve larger patches. SWE-bench Pro [22] and Gan-
                                                                                                 position at scale, which shows the novelty of our study.
hotra [9] similarly rely on patch complexity, while Large Language
Monkeys [3] highlights stochastic solvability without analyzing
difficulty drivers. Although such metrics correlate with difficulty
in our data (𝜌 = −0.380), they fail to explain edge cases: 12 tasks                              7      Conclusion
requiring minimal edits (single-file, ≤10 changes) are unsolved by                               This study presents a large-scale behavioral analysis of LLM-based
all agents. Prior work does not investigate why these seemingly                                  coding agents, connecting task characteristics, agent architecture,
simple tasks remain unsolvable.                                                                  and trajectory dynamics to understand how and why agents fail. We
    Behavioral analysis of coding agents. Existing studies examine                               find that standard difficulty metrics leave edge cases unexplained
agent behavior but lack proper controls or scale. Majgaonkar et                                  where the bottleneck is architectural reasoning and domain knowl-
al. [16] report longer failed trajectories but do not control for                                edge rather than patch complexity. Comparing success and failure
task difficulty, leading to confounded conclusions. Bouzenia and                                 trajectories under controlled paired designs shows that trajectory
Pradel [2] identify repetitive loops and cascading errors, but analyze                           length is confounded by task difficulty, but structural properties of
only 120 trajectories across three agents. Chen et al. [6] propose a                             the trajectory, particularly how agents sequence reading, patching,
process-oriented error taxonomy but do not perform within-task                                   and validation, distinguish success from failure consistently. De-
paired comparisons. Chen et al. [7] scale analysis across six LLMs                               composing agent performance reveals that LLM capability drives
but focus only on generated tests, finding that test-writing practices                           both outcome and behavioral strategy, while framework design con-
provide marginal utility rather than differentiating success from                                tributes surface-level variation that diminishes as models improve.
failure.                                                                                         Future work could extend this analysis to multilingual benchmarks,
    Decomposing agent performance. Other work compares agents at                                 develop real-time monitoring tools that leverage behavioral sig-
the architecture or LLM level. Martinez and Franch [17] and Ceka et                              natures for early failure detection, and investigate whether the
al. [4] treat agents as monolithic, conflating LLM and framework ef-                             architectural reasoning gap can be addressed through retrieval-
fects. More recent studies begin to vary LLMs: SWE-bench Pro [22]                                augmented or design-aware agent architectures.
categorizes failures using LLM summaries, SWE-Compass [24] eval-
uates multiple LLMs across frameworks at the outcome level, and
Ehsani et al. [8] analyze large-scale PRs without LLM-level break-
down. At the task level, DEI [32] shows that different agents re-                                Data Availability
solve different sets of tasks and achieves 34.3% resolution through                              This paper includes supplementary artifacts available at [18].
Behavioral Drivers of Coding Agent Success and Failure                                                                                        Preprint, 2026, Raleigh, NC, USA


References                                                                                     Dc5MjkyNDdjODg2ZGU1YTJjZGUxMCJ9.DfDdG85SXug_ZUp1UbkhJuvzaH
                                                                                               xWczC90r8esizwPmdZL-6h9xQ4gqIsFNmyX_S4krpEx0GuVa1TCHfqHjtjKA.
 [1] Nicolas Bettenburg, Sascha Just, Adrian Schröter, Cathrin Weiss, Rahul Premraj,           doi:10.5281/zenodo.19351830
     and Thomas Zimmermann. 2008. What Makes a Good Bug Report?. In Proceedings           [19] Xiangxin Meng, Zexiong Ma, Pengfei Gao, and Chao Peng. 2024. An Empir-
     of the 16th ACM SIGSOFT International Symposium on Foundations of Software                ical Study on LLM-based Agents for Automated Bug Fixing. arXiv preprint
     Engineering (FSE). 308–318. doi:10.1145/1453101.1453146                                   arXiv:2411.10213 (2024).
 [2] Islem Bouzenia and Michael Pradel. 2025. Understanding Software Engineer-            [20] OpenAI. 2024. Introducing SWE-bench Verified. https://openai.com/index/intro
     ing Agents: A Study of Thought-Action-Result Trajectories. In 40th IEEE/ACM               ducing-swe-bench-verified/. 93 human annotators provided difficulty estimates
     International Conference on Automated Software Engineering (ASE).                         for each of the 500 tasks. Annotation instructions: https://cdn.openai.com/intro
 [3] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le, Christo-           ducing-swe-bench-verified/swe-b-annotation-instructions.pdf.
     pher Ré, and Azalia Mirhoseini. 2024. Large language monkeys: Scaling inference      [21] Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane Suhr. 2024. Quantifying
     compute with repeated sampling. arXiv preprint arXiv:2407.21787 (2024).                   Language Models’ Sensitivity to Spurious Features in Prompt Design or: How
 [4] Ira Ceka, Saurabh Pujar, Shyam Ramji, et al. 2025. Understanding Software                 I Learned to Start Worrying about Prompt Formatting. In 12th International
     Engineering Agents Through the Lens of Traceability: An Empirical Study. arXiv            Conference on Learning Representations (ICLR).
     preprint arXiv:2506.08311 (2025).                                                    [22] SWE-Bench Pro Team. 2025. SWE-Bench Pro: Can AI Agents Solve Long-Horizon
 [5] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira              Software Engineering Tasks? arXiv preprint arXiv:2509.16941 (2025).
     Pinto, Jared Kaplan, et al. 2021. Evaluating Large Language Models Trained on        [23] SWE-bench Team. 2025. SWE-bench Verified Leaderboard. https://www.sweben
     Code. arXiv preprint arXiv:2107.03374 (2021).                                             ch.com. Accessed March 2026.
 [6] Zhi Chen et al. 2025. Beyond Final Code: A Process-Oriented Error Analysis of        [24] SWE-Compass Team. 2025. SWE-Compass: Towards Unified Evaluation of Agen-
     Software Development Agents in Real-World GitHub Scenarios. arXiv preprint                tic Coding Abilities. arXiv preprint arXiv:2511.05459 (2025).
     arXiv:2503.12374 (2025). Accepted at ICSE 2026.                                      [25] Lei Wang, Chen Ma, Xueyang Feng, et al. 2024. A Survey on Large Language
 [7] Zhi Chen et al. 2026. Rethinking the Value of Agent-Generated Tests for LLM-              Model based Autonomous Agents. Frontiers of Computer Science 18, 6 (2024),
     Based Software Engineering Agents. arXiv preprint arXiv:2602.07900 (2026).                186345.
 [8] Ramtin Ehsani, Sakshi Pathak, Shriya Rawal, et al. 2026. Where Do AI Coding          [26] Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen
     Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub. arXiv          Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, et al. 2025. OpenHands: An Open Plat-
     preprint arXiv:2601.15195 (2026).                                                         form for AI Software Developers as Generalist Agents. In International Conference
 [9] Jatin Ganhotra. 2025. Cracking the Code: How Difficult Are SWE-Bench-Verified             on Learning Representations (ICLR).
     Tasks Really? https://jatinganhotra.dev/blog/swe-agents/2025/04/15/swe-bench-        [27] Cathrin Weiss, Rahul Premraj, Thomas Zimmermann, and Andreas Zeller. 2007.
     verified-easy-medium-hard.html. Blog post.                                                How Long Will It Take to Fix This Bug?. In Proceedings of the Fourth International
[10] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2024.                    Workshop on Mining Software Repositories (MSR). doi:10.1109/MSR.2007.13
     A Survey on Large Language Models for Code Generation. arXiv preprint                [28] Chunqiu Steven Xia et al. 2025. Agentless: Demystifying LLM-based Software En-
     arXiv:2406.00515 (2024).                                                                  gineering Agents. In ACM International Conference on the Foundations of Software
[11] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,        Engineering (FSE).
     and Karthik Narasimhan. 2024. SWE-bench: Can Language Models Resolve Real-           [29] John Yang, Carlos E. Jimenez, et al. 2024. SWE-agent: Agent-Computer Interfaces
     World GitHub Issues?. In International Conference on Learning Representations             Enable Automated Software Engineering. In Advances in Neural Information
     (ICLR).                                                                                   Processing Systems (NeurIPS).
[12] Mosh Levy, Alon Jacoby, and Yoav Goldberg. 2024. Same Task, More Tokens:             [30] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
     the Impact of Input Length on the Reasoning Performance of Large Language                 and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language
     Models. In 62nd Annual Meeting of the Association for Computational Linguistics           Models. In International Conference on Learning Representations (ICLR).
     (ACL).                                                                               [31] Daoguang Zan et al. 2025. Multi-SWE-bench: A Multilingual Benchmark for
[13] Junwei Liu, Kaixin Wang, Yixuan Chen, Xin Peng, Zhenpeng Chen, Lingming                   Issue Resolving. OpenReview, under review.
     Zhang, and Yiling Lou. 2024. Large Language Model-Based Agents for Software          [32] Kexun Zhang, Weiran Yao, Zuxin Liu, et al. 2024. Diversity Empowers Intelli-
     Engineering: A Survey. arXiv preprint arXiv:2409.02977 (2024).                            gence: Integrating Expertise of Software Engineering Agents. arXiv preprint
[14] Shuyang Liu, Yang Chen, Rahul Krishna, et al. 2026. Process-Centric Analysis of           arXiv:2408.07060 (2024).
     Agentic Software Systems. arXiv preprint arXiv:2512.02393 (2026).                    [33] Yuntong Zhang et al. 2024. AutoCodeRover: Autonomous Program Improve-
[15] Simiao Liu, Fang Liu, Liehao Li, Xin Tan, Yinghao Zhu, Xiaoli Lian, and Li                ment. In ACM SIGSOFT International Symposium on Software Testing and Analysis
     Zhang. 2025. An Empirical Study on Failures in Automated Issue Solving. (2025).           (ISSTA).
     arXiv:2509.13941 [cs.SE] https://arxiv.org/abs/2509.13941                            [34] Jingming Zhuo, Songyang Zhang, Xinyu Fang, Haodong Duan, Dahua Lin, and
[16] Oorja Majgaonkar, Zhiwei Fei, Xiang Li, Federica Sarro, and He Ye. 2025. Un-              Kai Chen. 2024. ProSA: Assessing and Understanding the Prompt Sensitivity of
     derstanding Code Agent Behaviour: An Empirical Study of Success and Failure               LLMs. In Findings of the Association for Computational Linguistics: EMNLP 2024.
     Trajectories. arXiv preprint arXiv:2511.00197 (2025).                                     1950–1976.
[17] Matias Martinez and Xavier Franch. 2025. Dissecting the SWE-Bench Leader-            [35] Thomas Zimmermann, Nachiappan Nagappan, Harald Gall, Emanuel Giger,
     boards: Profiling Submitters and Architectures of LLM- and Agent-Based Repair             and Brendan Murphy. 2009. Cross-project Defect Prediction: A Large Scale
     Systems. arXiv preprint arXiv:2506.17208 (2025).                                          Experiment on Data vs. Domain vs. Process. In Proceedings of the 7th Joint
[18] Tural Mehtiyev and Wesley Assunção. 2026. Supplementary material uploaded as              Meeting of the European Software Engineering Conference and the ACM SIG-
     part of the paper. https://zenodo.org/records/19351830?preview=1&token=eyJh               SOFT Symposium on the Foundations of Software Engineering (ESEC/FSE). 91–100.
     bGciOiJIUzUxMiJ9.eyJpZCI6IjRhN2QwMzAwLTEwYWItNDJiYS1hMDgxLWV                              doi:10.1145/1595696.1595713
     mZmI3MDI1ZjQwNyIsImRhdGEiOnt9LCJyYW5kb20iOiJlMDMyNThjYzQ5Z
