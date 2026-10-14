                                              Regression Accumulation in Multi-Turn LLM Programming
                                                                  Conversations
                                                Yonghui (Andie) Huang                                       Lin Ma                                  Amjed Tahir
                                                      Massey University                         Alibaba Research Center for                       Massey University
                                                        New Zealand                           Complexity Sciences, Hangzhou                         New Zealand
                                                 andie.huang@massey.ac.nz                           Normal University                           a.tahir@massey.ac.nz
                                                                                                          China
                                                                                                    malin@hznu.edu.cn

                                                         Qian Zhang                                     Liwen Xiao                                    Lysa Xiao
                                                    University of Otago                              University of Otago                         University of Otago
                                                       New Zealand                                     New Zealand                                 New Zealand
arXiv:2607.01855v1 [cs.SE] 2 Jul 2026




                                               zhaqi075@student.otago.ac.nz                    xiali449@student.otago.ac.nz               lysa.xiao@postgrad.otago.ac.nz

                                        Abstract                                                                 CCS Concepts
                                        In LLM-assisted software development, coding is often iterative.         • Software and its engineering → Software testing and debug-
                                        In this paper, single-turn refers to settings where the LLM model        ging; Automatic programming; Software maintenance tools.
                                        responds in one request with one code suggestion, whereas multi-         ACM Reference Format:
                                        turn refers the model responds across multiple sequential requests       Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao,
                                        within the same conversation. The regression accumulation refers         and Lysa Xiao. 2026. Regression Accumulation in Multi-Turn LLM Pro-
                                        to the later code suggestion break the requirements introduced in        gramming Conversations. In Proceedings of 41st IEEE/ACM International
                                        earlier turns. Reliability depends not only on satisfying the current    Conference on Automated Software Engineering (ASE ’26). ACM, New York,
                                        turn, but also on preserving requirements in earlier turns. Yet, there   NY, USA, 12 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                        are limited evaluations of the accumulation of regression in multi-
                                        turn coding conversations.                                               1   Introduction
                                           To address this gap, we conduct an empirical study of multi-          Software programs are rarely developed in a single step. They
                                        turn regression in LLM programming. We construct 542 tasks from          evolve through repeated modifications that add features, broaden
                                        HumanEval+ and MBPP+ benchamrks, construct each task with an             input handling, restructure interfaces, or improve performance. A
                                        8-turn requirement-evolution chain. We evaluate six LLM models           central engineering risk in this process is regression, in which a
                                        on 26,016 turn instances (542 × 6 × 8). At each turn, we check if        change breaks behavior that previously worked correctly. Regres-
                                        the current code suggestion still passes earlier benchmark tests,        sion testing is the typical response to this risk [47]Both early and
                                        and we analyze 384 failure cases drawn from the failure population       later software evolution research suggest that continual modifica-
                                        in our 26,016 turn instances to derive and validate a taxonomy of        tion can increase system complexity and maintenance risk over
                                        multi-turn regression bugs through independent four-annotator            time [5, 6, 13].
                                        labeling. Our results show that regression accumulation appears             AI code-generation systems further highlight this maintenance
                                        across all six models, with 40% to 73% of tasks losing previously        issue. Developers increasingly use these systems in interactive cod-
                                        correct behavior over the full conversation. Final-turn quality is       ing conversations rather than relying only on one-shot prompts [19].
                                        lower than initial-turn quality across models, and especially in turns   In a single-turn setting, the model answers one prompt with one
                                        adding input validation or broader input types. Manual analysis          code suggestion. In a multi-turn setting, the model continues the
                                        shows that Cross-Turn Conflict, where later code conflicts with          same conversation across several turns and produces a new code
                                        earlier requirements, is the main failure class. We further find that    suggestion after each follow-up instruction. In such sessions, each
                                        Verification Gate, which checks new code against prior tests and         turn may address a local requirement, but the current code sug-
                                        triggers rollback and retry, is the only strategy that consistently      gestion must remain consistent with the code suggestions and
                                        improves all models, raising final-turn quality from 75.8% to 87.9%      requirements established in earlier turns [5, 47].
                                        on DeepSeek-V3 and from 31.6% to 47.3% on Llama-3.1-8B.                     Current evaluation practice does not capture this risk well be-
                                           These findings suggest that strong performance on single-turn         cause it is misaligned with how these systems are actually used. In
                                        tasks can overestimate reliability in multi-turn coding conversa-        practice, developers increasingly rely on multi-turn coding conver-
                                        tions. Future evaluation and tool design should test whether later       sations, where each new code suggestion is built on what earlier
                                        code suggestions preserve requirements from earlier turns and            turns already established. By contrast, single-turn benchmarks such
                                        should include Verification Gate mechanisms.                             as HumanEval [8] and MBPP [3] ask whether a model can produce
                                                                                                                 a correct code suggestion for one prompt. Recent multi-turn bench-
                                        ASE ’26, Munich, Germany
                                        2026. ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM                                 marks [30, 39, 43, 44] show that models are less likely to produce
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn                                  a code suggestion that satisfies the latest instruction once require-
                                                                                                                 ments are distributed across several turns in the same conversation.
ASE ’26, October 2026, Munich, Germany                                     Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao, and Lysa Xiao


However, they still focus mainly on whether the code suggestion at          integrated without breaking behavior that already works. Classic
the current turn satisfies the latest instruction. They do not directly     software evolution research explains why this risk persists. Lehman
test whether requirements established in earlier turns are still pre-       and Belady [5] argue that software subject to continual modifica-
served after later changes. This is not a problem with coding tasks         tion tends to accumulate complexity and quality risk. Maintenance
themselves. It is a limitation of what current evaluation practice          research commonly distinguishes corrective, adaptive, perfective,
chooses to measure. As a result, a model can appear successful at           and preventive changes [32]. Other work classifies the concrete
turn 𝑡 while silently breaking requirements introduced at turns 1           edits developers make during software evolution [13]. Regression
to 𝑡 − 1. This mismatch can lead us to overestimate reliability in          testing operationalizes this concern by checking whether existing
realistic workflows and leave users to recover broken functionality         behavior survives new modifications [47]. We adopt this lens for
through extra debugging and repair. We therefore need to under-             conversational code generation. In our setting, each turn acts as a
stand how much regression accumulates across turns, what kinds              maintenance step, and the central question is whether the generated
of failures dominate it, and which interaction-level controls can           update preserves prior behavior.
reduce it.
   We still lack an evaluation of whether later-turn code sugges-           2.2      Interactive and Multi-Turn LLM Coding
tions preserve requirements established in earlier turns. This paper        Recent surveys and perspective papers position LLM-based devel-
addresses that gap by studying whether AI-generated code sug-               opment as a growing software engineering research area [14, 22].
gestions preserve requirements established in earlier turns. We             Empirical work also shows that developers use LLM assistants
construct 8-turn evolution chains and evaluate each code sugges-            through shared, multi-turn interactions in collaborative settings
tion against the benchmark tests. We conduct this study on 542              such as pull requests and issues [19]. These studies motivate eval-
tasks from HumanEval+ and MBPP+ using GPT-4o, DeepSeek-V3,                  uating coding assistants in iterative workflows rather than only
Qwen2.5-Coder-32B, Qwen3-32B, DS-R1-Distill-32B, and Llama-3.1-             through one-shot generation.
8B, for a total of 26,016 turn instances (542 × 6 × 8). Our results show       Recent benchmarks have begun to study multi-turn code genera-
regression accumulation across all model families, with the steep-          tion directly. MT-Sec [39], CodeIF-Bench [43], CodeFlowBench [44],
est losses after error-handling and input-generalization requests.          and CodeAssistBench [27] all evaluate code generation across se-
Our manual analysis shows that these failures more often reflect            quences of instructions. Outside software tasks, Laban et al. [30]
incompatibilities between new code suggestions and earlier-turn             show that multi-turn performance declines across a broad range
requirements than simple context loss. We also find that mitiga-            of domains. These studies establish that turn history matters, but
tion strategies such as Verification Gate, which checks each new            most code benchmarks still score each turn against tests written
code suggestion against earlier-turn tests and allows one retry from        only for the current request. That setup captures turn-level instruc-
the last passing one, are effective when multi-turn coding conver-          tion following. It does not reveal whether later edits preserve prior
sations explicitly verify whether new code suggestions preserve             behavior.
earlier-turn requirements.                                                     Our protocol instead keeps the benchmark’s original tests as a
The main contributions from this work are:                                  fixed regression oracle at every turn, making regression directly
(1) We present a benchmark construction method and exe-                     observable. A model can satisfy the latest instruction while still
    cutable evaluation protocol for studying regression accumu-             breaking behavior introduced earlier in the conversation. We build
    lation in multi-turn LLM programming. The protocol combines             on HumanEval [8], MBPP [3], and their enhanced variants Hu-
    542 HumanEval+ and MBPP+ tasks with 8-turn evolution chains             manEval+ and MBPP+ [35], because their validated tests support
    and a fixed regression oracle derived from benchmark-provided           controlled longitudinal evaluation under repeated change.
    tests.
(2) We conduct a systematic empirical study across six LLMs and             2.3      Failure Modes and Repair in LLM-Generated
    26,016 turn instances to analyze how regression accumulation                     Code
    evolves across turns, model families, and requirement change            Studies of LLM code suggestions have cataloged common single-
    types.                                                                  turn failure modes such as incorrect logic, missing edge cases, and
(3) We develop a multi-turn bug taxonomy with eight multi-turn              API misuse [1]. A separate line of work investigates iterative re-
    bug types in three classes, plus Baseline Failure for Turn 1, from      pair through self-debugging, execution feedback, and learned self-
    manual analysis of 384 failure instances and four-annotator             correction [9, 15, 25, 28, 41]. These systems aim to improve one
    labeling.                                                               candidate solution through repeated repair attempts.
(4) We formulate and evaluate interaction-level mitigation strate-             We study a different failure setting. The model is not revising
    gies for multi-turn coding, including a verification-based rollback-    the same task until it passes. It is responding to a sequence of dis-
    and-retry design for code suggestions that introduce regression.        tinct change requests whose effects must compose over time. This
                                                                            difference exposes bug patterns that do not appear in single-turn
2 Related Work                                                              evaluation, including omission of earlier-turn requirements and fail-
2.1 Software Evolution and Regression Under                                 ures caused by accumulated code changes. In our paper, prior work
    Change                                                                  on long-conversation drift [12] motivates recap-based prompting
                                                                            that restates prior requirements, while one-step recoverability [24]
Regression under change has long been a central concern in soft-
                                                                            motivates a rollback-and-retry strategy that recovers from code
ware engineering. As systems evolve, new functionality must be
Regression Accumulation in Multi-Turn LLM Programming Conversations                                         ASE ’26, October 2026, Munich, Germany


suggestions that introduce regression using the last known-good          Regression Test Strategy. A key challenge arises at Turn 6 (T6) be-
code.                                                                    cause, unlike earlier turns, it changes how the benchmark tests call
                                                                         the code, i.e., from standalone functions to class methods. To pre-
3     Study Design                                                       serve the same benchmark-provided tests across turns, we continue
Our study was carried out in five stages. We begin with 542 Python       to use the benchmark’s original test suite throughout the conversa-
seed tasks drawn from two established benchmarks: 164 Python             tion. For Turns 1 to 5 (T1 to T5), the tests are executed unchanged.
function-level tasks from HumanEval+ and 378 Python function-            For Turns 6 to 8 (T6 to T8), we deterministically rewrite only the
level tasks from MBPP+. We include all tasks from both bench-            invocation sites by prepending object instantiation and replacing
marks and combine them into a single seed-task pool by applying          calls of the form f(args) with _obj.f(args). The assertions them-
the same fixed 8-turn prompt structure and benchmark-provided            selves are left unchanged. This design keeps the evaluation tied to
tests to every task. We then convert each task into a fixed 8-turn       the benchmark’s validated tests while preventing T6 failures from
programming conversation. At Turn 1 (T1), the model is asked to          being counted merely because the required refactoring changes the
produce an initial code suggestion from the benchmark’s original         call interface.
task prompt. For Turns 2 to 8 (T2 to T8), we define controlled re-
quirement changes using six software-maintenance change types            3.2    Cross-Turn Dependency Design
and instantiate them with fixed prompt templates, each designed          Existing multi-turn benchmarks often decompose tasks into in-
to modify code suggestions from earlier turns while preserving           dependent subtasks [39] or separately verifiable instructions [43].
previously established requirements. Next, we execute this conver-       Such designs are useful for measuring whether a model can satisfy
sation once for each task on each model. After each turn, we re-run      the requirement stated at the current turn. However, they are less
the benchmark tests to measure whether requirements established          suitable for studying regression accumulation because a later turn
in earlier turns are preserved. This process yields per-turn code        can be solved without modifying or preserving code suggestions
suggestions, test outcomes, turn-by-turn regression results, and the     from earlier turns. In that setting, a model may succeed at the
failing code suggestions, failed tests, and error messages returned      current turn even if it would fail to maintain earlier-turn require-
by Python execution or assertion failures that are used in the down-     ments under continued code evolution. Our goal is different. We
stream analyses for RQ1 to RQ3 . Figure 1 summarizes this workflow       want later turns to modify code suggestions produced earlier in
and data flow.                                                           the same conversation and to preserve established requirements.
                                                                         This design choice is consistent with software maintenance settings
3.1    Task Construction                                                 in which later modifications depend on and interact with earlier
We source 542 Python seed tasks from two established benchmarks,         ones [5, 6, 13, 46]. We therefore construct each subsequent turn so
HumanEval+ [35] (164 Python function-level tasks) and MBPP+ [35]         that it must be applied on top of the current code suggestion rather
(378 Python function-level tasks). Both benchmarks are widely used       than as an independent new solution. For example, Turn 4 (T4)
in LLM code generation research and provide rigorously validated         adds caching to the code suggestion that already includes Turn 2
test suites. We include all tasks regardless of complexity, using        (T2) validation and Turn 3 (T3) type generalization, and Turn 6 (T6)
the complexity of the benchmark reference solution as a control          refactors the accumulated functionality from Turns 1 to 5 (T1 to T5)
variable rather than a selection criterion.                              into a class while preserving the same requirements. Concretely,
   To account for differences in seed-task size, we use the lines        if T2 requires the code suggestion to reject invalid inputs and T3
of code (LOC) in the benchmark reference solution as a coarse            requires it to accept string representations of numeric inputs, then
structural proxy [20, 37]. We do not treat LOC alone as a complete       a later turn such as T4 must add caching without removing either
measure of software complexity. Rather, we use it only to stratify       the validation introduced in T2 or the input conversion introduced
these short function-level benchmark tasks by reference-solution         in T3.
size. Based on this measure, we group tasks into three strata: easy
(1–3 lines, 𝑛=322), medium (4–8 lines, 𝑛=162), and hard (≥9 lines,       3.3    Requirement Change Types
𝑛=58). We also consider a complementary notion of task difficulty        Turn 1 is treated separately as the initial code-suggestion baseline.
for the models themselves. Specifically, we use Turn 1 (T1) pass rate    For Turns 2 to 8, we derive a pool of maintenance-like follow-
to capture how solvable each task is at the initial code-suggestion      up changes from prior software-maintenance, software-evolution,
turn, so that we can analyze how initial solvability interacts with      and source-code-change literature [7, 13, 32]. We therefore se-
subsequent regression accumulation.                                      lect six change types for benchmark construction based on three
   Each seed task is instantiated as the same fixed 8-turn conversa-     benchmark-design requirements. Each change type should repre-
tion by filling a small set of benchmark-derived fields into the fixed   sent a common follow-up modification, create explicit preservation
turn templates introduced later in this section. These fields include    obligations, and be instantiable consistently across many bench-
the target function name ({entry_point}) and, for the restructur-        mark tasks. We do not claim that these six types exhaust all realistic
ing turn, the derived class name ({class_name}). This deterministic      maintenance turns. Rather, they provide a controlled subset for
instantiation keeps prompt construction consistent across tasks and      reproducible comparison across tasks and models.
avoids introducing additional variation from task-specific prompt        (1) Functional Extension: add new functionality while preserving
writing.                                                                     requirements established in earlier turns [7, 32, 33].
ASE ’26, October 2026, Munich, Germany                                                                               Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao, and Lysa Xiao



           Stage 1                               Stage 2                                                             Stage 3                                    Stage 4                              Stage 5
                                               Task Construction                                                                                            Artifacts Collection
                                                                                                             Execution & Evaluation
                                                                                                                                                                                                 Downstream Analysis
   Seed Benchmarks                           8-turn Evaluation Chain
                                             (Explicit Dependencies)                                                                                                                               RQ1: Regression
                                                                                                     6 LLM models                                                                               Accumulation over Turns
                               T1                T2               T3               T4
    - HumanEval+             Initial            Error            Input        Performance
    (164 tasks)          Implementation        Handling      Generalization   Optimization
                                                                                                                                                                                                   RQ2: LLM Multi-turns Bugs
                                                                                                                                  Turn-level
                                                                                                                                                                                                     Taxonomy Analysis
                                                                                                Model Execution                Regression Oracle        - Generated Codes (GC)
    - MBPP+                                                                                                                    T1-T5: Re-run original   - Pass/Fail of GC
                                                                                               For each task, each model
    (378 tasks)             T1          T2     T3      T4     T5       T6     T7    T8             completes one 8-turn          benchmark tests        - RPR Trajectory
                                                                                                        conversation                                                                            RQ3: LLM Multi-turns Bugs
                                                                                                                                                        - Failure Logs / Error Traces
                                                                                             Total: 3,252 conversations (542   T6-T8: Adapt only test                                                Factor Analysis
    Total 542 tasks           T5                  T6              T7               T8
                                                                                                                               invocation sites, keep
                                                                                                                                                        - Code Size Growth (LOC)
                           Functional          Interface     Non-functional   Performance            tasks × 6 models)
                           Extention         Restructuring                        Opt.                                         assertions unchanged
                                                                 Aug.
                                                                                                                                                                                                   RQ4: Mitigation Strategies
                                                                                                                                                                        Mitigation Strategies            Evaluation




Figure 1: Overall study design and data flow. Seed tasks are instantiated as 8-turn evolution chains, executed once for each task
on each model, and evaluated with the same benchmark-provided tests at every turn.

(2) Error Handling Enhancement: add validation and exception                                                            established in earlier turns. The only task-specific difference is the
    handling to existing code [36].                                                                                     name of the function being modified. This design removes prompt
(3) Input Generalization: extend the code suggestion to support                                                         variability as a confound while keeping the benchmark prompts
    additional input forms [7, 32].                                                                                     recognizable and executable.
(4) Performance Optimization: improve efficiency while keeping                                                             The templates provide a controlled and reproducible represen-
    outputs unchanged [2].                                                                                              tation of common follow-up programming turns. We standard-
(5) Interface Restructuring: refactor the program structure or                                                          ize the prompt structure and keep the wording stable, while al-
    interface while preserving requirements established in earlier                                                      lowing only benchmark-derived fields to vary. Some templates
    turns [21].                                                                                                         include concrete code hooks such as _cache, clear_cache(), and
(6) Non-functional Augmentation: add cross-cutting support                                                              get_stats(self). These hooks make each turn-specific change
    such as logging or call statistics such as counts of calls, cache                                                   operationally precise, comparable across tasks, and directly check-
    hits, and errors [26].                                                                                              able by the same downstream regression tests.
   All 542 tasks follow a fixed 8-turn sequence with one baseline                                                          As shown in Figure 2, Depends on identifies which previously
turn and seven controlled requirement changes (Table 1). The order-                                                     introduced functionality must be understood and modified to com-
ing is designed so that later turns add new requirements while pre-                                                     plete the current turn. Preserve identifies which requirements estab-
serving those established earlier in the conversation, and the same                                                     lished in earlier turns must remain intact after the change. Together,
sequence is applied to all tasks for comparability. Early turns estab-                                                  these two fields make the cross-turn dependency explicit. The result-
lish the initial code suggestion and then add constraints through val-                                                  ing 8-turn sequence covers all six change types with restructuring
idation and broader input support. Turn 4 (T4) adds caching, Turn 5                                                     at the midpoint, remains consistent with empirical evidence that
(T5) adds new functionality, and Turn 6 (T6) refactors the accumu-                                                      developer-facing LLM interactions are typically short multi-turn
lated code suggestion into a class. Turn 7 (T7) adds cross-cutting                                                      conversations [19], and is long enough to expose regression accu-
support such as logging or call statistics, and Turn 8 (T8) optimizes                                                   mulation across turns in the same conversation [30]. In our setting,
the class method’s core algorithm while preserving caching, vali-                                                       this length is also sufficient to reveal the full regression trajectory.
dation, type conversion, logging, and call statistics. The sequence                                                     The full wording of all eight templates is provided in our replica-
also intentionally repeats some broad change families at different                                                      tion package (https://anonymous.4open.science/r/multi-turn-llm-
stages. Turn 5 (T5) revisits functional extension after validation,                                                     regression-E73E).
type generalization, and caching have already been added, and                                                              All 542 tasks receive the same template at each turn. This choice
Turn 8 (T8) revisits algorithm optimization after the codebase has                                                      ensures a controlled comparison across tasks, even though some
been restructured and augmented. This design lets us compare how                                                        turns may be less natural for certain problems and some prompt
similar modification families behave under different levels of accu-                                                    details may be more explicit than in unconstrained developer con-
mulated conversational state. We do not claim that this is the only                                                     versations. We accept this trade-off because the benchmark is de-
realistic ordering of maintenance turns.                                                                                signed to study regression under a fixed and reproducible sequence
Fixed Prompt Templates. We do not ask any LLM to invent a                                                               of evolving requirements. Our goal is not to replay the full diver-
different follow-up turn for each task. Instead, for each turn we                                                       sity of natural maintenance conversations. It is intended to expose
use the same fixed prompt wording across tasks and fill in only a                                                       models to a stable set of follow-up changes that systematically re-
small number of task-specific fields copied from the benchmark.                                                         quire modifications of existing code while preserving requirements
These fields include the target function name (entry_point), the                                                        established in earlier turns. Our regression tests therefore evaluate
benchmark’s original task prompt at Turn 1 (T1), and the class name                                                     whether later code suggestions preserve requirements established
used for the refactoring turn at Turn 6 (T6), which is determinis-                                                      in earlier turns, not whether every turn is equally natural for every
tically derived from entry_point. Figure 2 summarizes the eight                                                         task.
turn templates. For example, the Turn 2 (T2) template always asks
the model to add input validation while preserving requirements
Regression Accumulation in Multi-Turn LLM Programming Conversations                                                                                               ASE ’26, October 2026, Munich, Germany


                                                                                                         Turn 3 (T3)
                                                              Turn 2 (T2)                                                                                Turn 4 (T4)
                Turn 1 (T1)                                                                              Input Generalization
                                                              Error Handling Enhancement                                                                 Performance Optimization
                Initial Implementation                                                                   Prompt “Extend {entry_point} so that it
                                                              Prompt “Update {entry_point} to add                                                        Prompt “Add result caching to
                Prompt “Please implement the function                                                    can also accept string representations of its
                                                              comprehensive input validation” with in-                                                   {entry_point}” using module-level
                {entry_point} according to the following                                                 numeric inputs”; non-convertible strings
                                                              valid type → TypeError and invalid value                                                   _cache + helper clear_cache().
                specification” + {original_prompt}.                                                      → ValueError.
                                                              → ValueError.                                                                              Depends on Accumulated behavior from
                Fields {entry_point},                                                                    Depends on Turn 1 logic and Turn 2 vali-
                                                              Depends on Turn 1 implementation                                                           Turns 1 to 3
                {original_prompt}                                                                        dation
                                                              Preserve All previously correct behavior                                                   Preserve Exactly the same results for all
                Output Complete updated code                                                             Preserve Previous behavior, including
                                                              exactly                                                                                    inputs
                                                                                                         error handling




                Turn 5 (T5)                                   Turn 6 (T6)                                Turn 7 (T7)                                     Turn 8 (T8)
                Functional Extension                          Interface Restructuring                    Non-functional Augmentation                     Performance Optimization
                Prompt “Add a new function                    Prompt “Refactor all code into a sin-      Prompt “Add logging and call statistics to      Prompt “Optimize the core algorithm in
                {entry_point}_batch” over argument-           gle class named {class_name}” so           the {class_name} class” with self.stats         {class_name}.{entry_point}” and briefly
                tuples; failed calls are caught and mapped    {entry_point} and {entry_point}_batch      and get_stats(self).                            explain the strategy in a docstring.
                to None.                                      become methods.                            Depends on The refactored class and             Depends on All previously added func-
                Depends on Earlier validation, conversion,    Depends on Accumulated functionality       prior execution paths                           tional and non-functional behavior
                and caching                                   from Turns 1 to 5                          Preserve Functional behavior under cross-       Preserve Caching, validation, conversion,
                Preserve All prior functionality              Preserve Method signatures and prior       cutting logic                                   logging, and statistics
                                                              behavior




Figure 2: Overview of the eight fixed turn templates used in the benchmark. For space reasons, the boxes show only the
core content of each prompt rather than the full wording. Each turn uses fixed prompt wording, while benchmark-derived
fields such as {entry_point}, {original_prompt}, and {class_name} are filled deterministically. The arrows show the intended
progression of the conversation from Turn 1 to Turn 8.

Table 1: Fixed 8-turn evolution sequence used for all 542                                                   Across subsequent calibration rounds, the same three authors
tasks.                                                                                                   applied the evolving codebook to shared cases and used disagree-
                                                                                                         ments to refine the label set rather than to optimize agreement
      Turn    Turn Type                                Coupling Scope                                    prematurely. These disagreements repeatedly traced back to three
                                                                                                         issues: label overlap, overly abstract definitions, and underspecified
       T1     Initial Code Suggestion                  None (baseline)
       T2     Error Handling Enh.                      T1 control flow                                   decision rules. We therefore added distinguishing rules and made
       T3     Input Generalization                     T1 algorithm, T2 validation                       the single-label decision rule explicit for boundary cases.
       T4     Add Caching                              T1–T3 consistency                                    Once the concrete labels and their boundaries stabilized, we
       T5     Functional Extension                     T1–T4 collectively                                grouped them into higher-level classes based on their primary root
       T6     Interface Restructuring                  T1–T5 all requirements                            cause. In other words, this higher-level organization was introduced
       T7     Non-functional Aug.                      T2,T4,T6 cross-cutting                            after the label set had stabilized, not imposed before coding. We
       T8     Algorithm Opt.                           T1–T7 full codebase                               aligned this organization with established software engineering
                                                                                                         concepts such as regression bugs [47], code decay [5], and feature
3.4    Taxonomy Development                                                                              interaction [48]. We also compared the resulting scheme against
To characterize failures that emerge only after requirements ac-                                         existing bug taxonomies for AI-generated code suggestions [1]
cumulate across turns, we develop a new taxonomy of multi-turn                                           to identify multi-turn failure patterns that are not well captured
bugs and use it as the coding scheme for the annotation study. This                                      by prior single-turn classifications. After the label set and class
taxonomy is not directly adopted from an existing bug taxonomy.                                          structure stabilized, we froze the codebook for the full annotation
Instead, it is derived bottom-up from our failure cases while being                                      study.
informed by qualitative coding and thematic-synthesis practice in                                           The finalized scheme operationalizes annotation as a bug-classification
software engineering [11, 40, 42]. We began with an initial calibra-                                     form rather than a free-response questionnaire. After freezing the
tion subset of 100 failure cases, selected to cover turn positions,                                      codebook, four of the study’s authors independently applied it to
change types, models, and failure severities, and asked the three                                        the 384 sampled failures. For each failed turn instance, annotators
coders (all co-authors) to independently read and open-code the                                          inspect the original task prompt, the turn number and change type,
observed failure patterns without pre-fixing the final labels. This                                      the current-turn prompt for the failing turn (for example, Turn 𝑛 or
bottom-up process produced a provisional pool of fine-grained                                            T𝑛), the last correct code suggestion from the previous successful
failure codes rather than predefined high-level classes. The three                                       turn (for example, Turn 𝑛−1), the failing code suggestion, the failed
coders then compared their codes, merged synonymous or over-                                             tests and error messages, and the regression rate. They then diag-
lapping concepts, split labels whose boundary covered more than                                          nose which previously established requirement or constraint has
one mechanism, and removed candidate codes that were too rare,                                           been broken and encode that diagnosis by assigning one bug label
too ambiguous, or not distinguishable enough to support stable an-                                       from the frozen codebook. We present these options to annotators
notation rules. We refined the remaining labels by writing explicit                                      as closed-choice labels grouped under the higher-level classes, with
definitions, inclusion criteria, exclusion criteria, and illustrative                                    Baseline Failure reserved for Turn 1 cases. The high-level failure
examples for each candidate label. A label was retained in the final                                     mechanism is inferred from the selected label’s class membership
scheme only if it captured a recurring failure pattern, had a bound-                                     rather than being recorded through a separate question. After full
ary that annotators could distinguish from neighboring labels, and                                       annotation begins, the taxonomy is no longer substantially revised,
could be supported by a concrete decision rule.                                                          so that agreement statistics remain interpretable. We apply the
                                                                                                         frozen codebook in the 384-sample annotation study described in
ASE ’26, October 2026, Munich, Germany                                     Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao, and Lysa Xiao


Section 4.4. We present the taxonomy itself, its agreement statistics,      passing code suggestion is available. In that case, the current code
and its empirical distribution in RQ2 .                                     suggestion is rejected and the model receives a rollback prompt
                                                                            with three fixed elements: the number of failed regression tests,
3.5    Mitigation Strategy Design                                           the full code of the last passing code suggestion, and the original
We design mitigation strategies for two risks that arise in multi-          requirement for the current turn. Concretely, the prompt tells the
turn coding conversations. One is that the model may lose track of          model that its previous attempt caused 𝑛 fail of 𝑛 total regression tests
constraints established earlier in the conversation, which is consis-       to fail, provides the last correct code block, and asks it to apply
tent with prior observations of multi-turn quality loss and context         the current requirement to that version instead. The model is then
drift [12, 30]. The other is that a new code suggestion may break           given a single retry. We retain the retry only when it passes at
requirements established in earlier turns when a fresh requirement          least as many benchmark tests as the rejected code suggestion;
is applied to already-evolving code, a recurring concern in change-         otherwise, the current code suggestion is kept. For example, sup-
impact and ripple-effect analysis [6, 46]. We therefore formulate           pose Turn 3 has already added support for string representations
two lightweight interaction-level strategies and evaluate them in-          of numeric inputs, and Turn 4 asks the model to add caching. If
dividually and in combination. Both strategies operate within the           the first Turn 4 code suggestion adds caching but breaks the earlier
ongoing conversation rather than as post-hoc repair procedures, al-         input-conversion requirement, the gate rejects that code suggestion,
lowing us to assess whether they reduce regression as requirements          restores the last passing Turn 3 version, and asks the model to gen-
accumulate.                                                                 erate Turn 4 again from that point. This design bounds intervention
                                                                            cost to at most one additional generation per turn while making
3.5.1 S1: Snowball Recap. Snowball Recap is designed for cases in           the rollback criterion fully observable and reproducible.
which the model may lose track of requirements established earlier
in the conversation. In our protocol, each new turn is appended             3.5.3 S3: Combined (S1 + S2). The combined strategy applies both
to the existing dialogue, so later turns are issued under an increas-       recap and verification gating in the same conversation. It tests
ingly long interaction history. The strategy therefore makes earlier        whether the two interventions address complementary failure mech-
constraints explicit again before each later turn instead of relying        anisms or largely overlap in practice.
on the model to recover them from the growing conversation con-                All three strategies are model-agnostic. They require neither
text alone. Following prior evidence that restating relevant context        fine-tuning nor access to the internal model. Their overhead is also
can reduce quality loss in long LLM interactions [30] and prior             bounded. Snowball Recap adds prompt tokens only, and Verification
observations that long conversations can cause models to lose track         Gate introduces at most one retry per turn.
of earlier requirements [12], this strategy prepends a recap prefix
before each turn 𝑡 ≥ 2. The prefix has three fixed parts: a header stat-    4 Experimental Setup
ing that all requirements from earlier turns must continue to hold,         4.1 Models Under Study
one summary line for each earlier turn in the format “T𝑖. [change
                                                                            We evaluate six LLMs, including two commercial models (GPT-
type]: summary.”, and a fixed transition line before the prompt for
                                                                            4o [38] and DeepSeek-V3 [34]) and four open-source models (Qwen2.5-
the current turn. These summary lines are not generated by an-
                                                                            Coder-32B [23], Qwen3-32B [45], DS-R1-Distill-32B [18], and Llama-
other model. Instead, they are produced deterministically from two
                                                                            3.1-8B [17]). This set allows us to compare commercial models and
metadata fields already stored in the benchmark instance, namely
                                                                            to compare a code-specialized model (i.e., Qwen2.5-Coder-32B) with
the turn index and the turn’s change type. For example, Turn 2
                                                                            general-purpose models (i.e., GPT-4o, DeepSeek-V3, Qwen3-32B,
contributes the recap line “T2. [Error Handling Enhancement]: add
                                                                            and Llama-3.1-8B). It also includes a reasoning-oriented model (i.e.,
input validation (TypeError/ValueError) to all public methods with-
                                                                            DS-R1-Distill-32B) alongside standard-generation models.
out rejecting previously valid inputs,” and Turn 3 contributes “T3.
                                                                               The commercial models are accessed through APIs, whereas the
[Input Generalization]: accept string representations of numeric
                                                                            open-source models are evaluated under a shared local inference
inputs and convert them, while preserving existing validation and
                                                                            setup. Within the local group, Qwen2.5-Coder-32B and Qwen3-32B
logic.” For Turn 4, the final prompt is the fixed header, followed
                                                                            isolate code specialization at the same nominal size, DS-R1-Distill-
by the recap lines for Turns 2 and 3, and then the original Turn 4
                                                                            32B adds a reasoning-oriented variant, and Llama-3.1-8B provides
prompt.
                                                                            a smaller scale contrast.
3.5.2 S2: Verification Gate. Verification Gate is designed for cases           All four open-source models are served locally on a single 32 GB
in which a newly generated code suggestion immediately breaks               NVIDIA RTX 5090 through vLLM [29] with AWQ 4-bit quantization
requirements that were preserved at the previous turn, a familiar           and max-model-len set to 32,768. GPT-4o and DeepSeek-V3 are
regression risk under successive change [6, 46, 47]. Unlike post-hoc        accessed through their official OpenAI-compatible APIs.
repair methods that ask the model to fix a code suggestion only
after it has already failed [9, 28], this strategy checks each turn         4.2      Evaluation Protocol
immediately after generation and applies the one-step recoverabil-          For each task on each model, we run one 8-turn conversation con-
ity principle of Jain et al. [24]. After each turn 𝑡 ≥ 2, we execute        sisting of an initial code-suggestion turn followed by seven con-
the same benchmark-provided tests used throughout the study and             trolled requirement changes. All six models are evaluated on the
compare the current regression pass rate with that of the preceding         same 542 tasks, comprising 164 HumanEval+ tasks and 378 MBPP+
turn. The gate is triggered only when 𝑅𝑃𝑅𝑡 < 𝑅𝑃𝑅𝑡 −1 and a last             tasks, totaling 3,252 conversations and 26,016 turn instances.
Regression Accumulation in Multi-Turn LLM Programming Conversations                                              ASE ’26, October 2026, Munich, Germany


              Table 2: Models evaluated in the study.                         instances with 𝑅𝑃𝑅𝑡 < 1.0, we then stratify this sample across turn
                                                                              number and model so that the annotation set covers the main parts
Model                 Params     Type       Deploy    Comparison              of the experimental space.
GPT-4o                —          General    API       Commercial baseline         The four annotators are the first four authors. Each of the four
DeepSeek-V3           671B       General    API       MoE architecture        independently labels every sampled case using the frozen codebook
Qwen2.5-Coder-32B     32B        Code       Local     Code-specialized
                                                                              developed in Section 3.4. For each sample, annotators inspect the
Qwen3-32B             32B        General    Local     General (same family)   most recent earlier code suggestion that passed the regression
DS-R1-Distill-32B     32B        Reason     Local     Reasoning model         oracle, the failing code suggestion at the current turn, the failed
Llama-3.1-8B          8B         General    Local     Scale comparison        tests and error messages, and the current-turn request. They then
                                                                              assign one bug label from the predefined codebook as the root-cause
    Each conversation starts with a fixed system prompt that asks             label.
the model to return the full code suggestion in a single Python code              To reduce within-annotator inconsistency, each annotator labels
block. At Turn 1, the user message is the benchmark prompt for the            every sample in three passes and keeps the within-annotator ma-
initial code suggestion. At each subsequent turn, the user message            jority label as the final individual judgment. We then aggregate the
is the fixed benchmark request for that turn. At Turn 𝑡, the input            four final judgments across annotators. Of the 384 samples, 277 are
contains the system prompt, the user requests from Turns 1 to 𝑡,              unanimous, and 107 are non-unanimous. For non-unanimous cases
and the model responses from all earlier turns.                               with a majority label, we keep the majority label. For the remaining
    After each response, we extract the code suggestion by taking             42 cases without a majority label, the senior researcher resolves
the last fenced Python block. If no fenced block is present, we use           the tie. We report inter-rater agreement in RQ2 using Fleiss’ 𝜅, be-
the raw response text as the candidate program. We then evaluate              cause each of the 384 samples receives one nominal bug label from
that program against the regression oracle for the current turn. For          each of four annotators, and Fleiss’ 𝜅 provides a chance-corrected
function-level tasks, Turns 1 to 5 use the benchmark’s original tests,        agreement measure for more than two raters, as in prior software
and Turns 6 to 8 use deterministically adapted versions of those              engineering studies with multi-rater labeling [4, 16]. We compute
same tests after the interface is restructured into a class. The adapta-      it on the final annotator labels before majority aggregation so that
tion prepends object instantiation and rewrites direct function calls         it reflects how consistently the bug taxonomy can be applied inde-
into method calls, but leaves the original assertions unchanged. For          pendently.
each test, we build a temporary Python script containing the code
suggestion and the test, run it in an isolated subprocess, and enforce        5 Results
a 15-second timeout. Assert-style tests are executed independently            5.1 RQ1 : How much previously correct behavior
and in parallel, whereas unittest-style suites are executed in a single
                                                                                  is lost as requirements accumulate across
subprocess.
                                                                                  turns in LLM coding conversations?
4.3     Metrics                                                               We organize the results in three parts. Figure 3 shows the end-to-
We use one turn-level metric, Regression Pass Rate, which captures            end trajectories from Turn 1 to Turn 8 for all six models. We report
how much previously correct behavior is still preserved at each turn.         per-turn 𝑅𝑃𝑅 values and identify where the largest losses occur
The remaining three metrics summarize regression accumulation                 in Table 3. Table 4 shows the same pattern after restricting each
over the full conversation.                                                   model to tasks it solved at Turn 1.
• Regression Pass Rate (𝑅𝑃𝑅𝑡 ). For a given task at turn 𝑡, 𝑅𝑃𝑅𝑡 =            Finding 1. Regression accumulates for all six models, but its
  𝑝𝑡 /𝑛𝑡 , where 𝑝𝑡 is the number of benchmark tests that pass at             magnitude differs substantially by model family. As shown in
  turn 𝑡 and 𝑛𝑡 is the total number of benchmark tests for that task.         Figure 3, every trajectory trends downward from Turn 1 to Turn 8.
  Because the same benchmark tests are preserved across turns, a              No model finishes at or above its initial regression pass rate. Across
  lower 𝑅𝑃𝑅𝑡 directly indicates that more prior behavior has been             models, 40–73% of tasks lose previously correct behavior over the
  broken.                                                                     full conversation. DeepSeek-V3 and GPT-4o remain strongest at
• Degradation (Δ). Δ = 𝑅𝑃𝑅8 − 𝑅𝑃𝑅1 . This metric captures the                 Turn 8, reaching 75.8% and 72.4% respectively. The 32B open models
  net change in quality from the first to the last turn.                      form a middle tier, with final-turn 𝑅𝑃𝑅 values ranging from 51.7%
• Degradation Rate. This is the fraction of tasks for which Δ < 0.            to 57.9%. Llama-3.1-8B shows the largest loss and falls to 31.6%.
  It measures how often quality declines over the conversation.               Finding 2. Strong Turn 1 performance does not necessarily
• Survival Rate. This metric is computed only for tasks with                  translate into stronger multi-turn resilience. DeepSeek-V3 be-
  𝑅𝑃𝑅1 = 100%. It reports the fraction of those initially solved tasks        gins below GPT-4o at Turn 1, yet retains more quality by Turn 8.
  that still satisfy 𝑅𝑃𝑅𝑡 ≥ 50% at turn 𝑡.                                    Llama-3.1-8B declines much more sharply than the larger commer-
                                                                              cial models and finishes far below the 32B open models at Turn 8.
4.4     Bug Annotation Protocol                                               Reasoning specialization does not appear to help in this setting,
                                                                              since DS-R1-Distill-32B reaches 51.7% at Turn 8, whereas Qwen3-
To answer RQ2 , we annotate a stratified sample of failure instances.
                                                                              32B reaches 57.9%.
We set the sample size to 384 using Cochran’s standard formula
                                                                              Finding 3. The per-turn results show that regression losses
for proportion estimates with a 95% confidence level, a 5% margin
                                                                              are front-loaded and are concentrated in a small number of
of error, and the conservative choice 𝑝 = 0.5 [10]. From all turn
                                                                              change types. For five of the six models, the largest losses occur
ASE ’26, October 2026, Munich, Germany                                                              Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao, and Lysa Xiao


                                          Qwen3-32B      DS-R1-Distill-32B           Llama-3.1-8B    from 10.6% to 29.2%. The two weakest models, i.e., DS-R1-Distill-
                                          GPT-4o         DeepSeek-V3           Qwen2.5-Coder-32B
                                                                                                     32B and Llama-3.1-8B, lose a substantial fraction of the tasks they
                                                                                                     solve at Turn 1 (T1) to total failure by Turn 8.
                                90

                                                                                                        Regression accumulates for all six LLM models in multi-turn conversa-
                                80                                                                      tions and are concentrated in specific change types (i.e., error-handling
                                                                                                        and input-generalization requests). Subsequent changes to require-
                                                                                                        ments in a multi-turn conversation can introduce regression even when
                                70                                                                      the first-turn code suggestion is correct.
     Regression Pass Rate (%)




                                60                                                                   5.2      RQ2 : What multi-turn-specific bugs emerge,
                                                                                                              and how are they distributed across
                                50
                                                                                                              taxonomy categories and requirement
                                                                                                              change types?
                                                                                                     To answer RQ2, we analyze 384 manually labeled failure cases
                                40
                                                                                                     (Section 4.4). Table 5 reports the taxonomy and its distribution.
                                                                                                     The reported counts and percentages use the finalized label per
                                30                                                                   case, so each annotated case contributes to exactly one row in the
                                                                                                     distribution. Baseline Failure (BF) is reserved for Turn 1 failure
                                                                                                     and is therefore interpreted separately from multi-turn regression
                                20                                                                   failures.
                                     T1    T2      T3      T4      T5     T6       T7     T8         Finding 6. Cross-Turn Conflict is the major source of manu-
                                                        Conversation turn
                                                                                                     ally observed regression failures. As shown in Table 5, Cross-
Figure 3: Regression pass rate trajectories across the eight-                                        Turn Conflict accounts for 55.7% of labeled cases, compared with
turn conversation for all six models (𝑁 = 542 for each model).                                       21.1% for Context-Loss and 10.7% for Accumulation. This indicates
All models end below their Turn 1 pass rate, although the                                            that later revisions more often break previously correct behavior
timing and severity of the losses differ by model.                                                   through incompatibility with existing code than through simple
                                                                                                     forgetting.
at Turn 2 or Turn 3. These error-handling and input-generalization                                   Finding 7. The distribution is concentrated in two conflict
turns are disruptive because the new validation or conversion logic                                  types, and their locations across change requests are inter-
must remain compatible with both the task’s original behavior and                                    pretable. Over-Guarding (CC-4) contributes 28.6% and Seman-
earlier-turn requirements.                                                                           tic Collision (CC-1) contributes 26.6% of all labeled failures. To-
   No model shows sustained recovery once quality drops. Some                                        gether they account for 55.2% of all annotated cases. Within CC-4,
local improvements appear, such as Qwen3 between T5 and T6,                                          more than half of the cases arise from error-handling and input-
but they do not reverse the overall trend. In other words, once                                      generalization requests (59/110, 53.6%), in which stricter checks
regression appears in the conversation, later turns rarely restore                                   must preserve previously valid behavior. Within CC-1, half of the
the lost behavior on their own.                                                                      cases involve functional extension and performance optimization
Finding 4. Regression accumulation appears for both easier                                           (51/102, 50.0%), in which new logic is added on top of existing
and harder seed tasks. For DeepSeek-V3, the hard group (≥9 LOC                                       behavior.
in the benchmark reference solution) declines from 82.5% at Turn 1                                   Finding 8. Accumulation-specific failures are present, but
to 62.7% at Turn 8, while the easy group (1 to 3 LOC) declines from                                  less frequent. Complexity Collapse (AC-2) appears in 9.9% of
88.3% to 77.4%.                                                                                      annotated failures and Regression via Omission (AC-1) appears
Finding 5. Regression accumulation remains substantial even                                          in 0.8%. These patterns are explicitly separated in our taxonomy
among tasks solved perfectly at Turn 1 (i.e., tasks with 𝑅𝑃𝑅𝑇 1 =                                    because they are not well represented in prior single-turn LLM
100%). To isolate the regression signal from baseline inability, we                                  bug taxonomies [1]. Four annotators independently labeled all 384
perform this analysis separately for each model and retain only the                                  samples, with unanimous agreement on 277 samples and Fleiss’ 𝜅 =
tasks on which that model passes all benchmark tests at Turn 1. We                                   0.799 (substantial agreement [31]), which supports the reliability
then report the median task-level 𝑅𝑃𝑅𝑇 8 , the percentage of tasks                                   of the reported distribution.
with 𝑅𝑃𝑅𝑇 8 < 100%, and the percentage of tasks with 𝑅𝑃𝑅𝑇 8 = 0%
in Table 4.                                                                                             Manual labels indicate that multi-turn regression is primarily an integra-
                                                                                                        tion problem rather than solely a Context-Loss problem. Over-Guarding
   The ordering of the models by median task-level 𝑅𝑃𝑅𝑇 8 is un-
                                                                                                        and Semantic Collision account for most cases, while accumulation-
changed after restricting each model to tasks it solved at T1. On this
                                                                                                        specific failures remain observable as code grows.
restricted subset, the median task-level 𝑅𝑃𝑅𝑇 8 remains 100% for
GPT-4o and DeepSeek-V3, while the 32B open models also retain
high median 𝑅𝑃𝑅𝑇 8 values but still exhibit collapse rates ranging
Regression Accumulation in Multi-Turn LLM Programming Conversations                                                                          ASE ’26, October 2026, Munich, Germany


       Table 3: Per-turn 𝑅𝑃𝑅 and LOC for all six models (𝑁 = 542). Bold marks the largest per-turn 𝑅𝑃𝑅 loss for each model.


                                                        GPT-4o            DeepSeek              Qwen-Coder Qwen3    DS-R1 Llama-8B
                          T     Turn Type            𝑅𝑃𝑅 LOC 𝑅𝑃𝑅 LOC 𝑅𝑃𝑅                              LOC 𝑅𝑃𝑅 LOC 𝑅𝑃𝑅 LOC 𝑅𝑃𝑅 LOC
                          1     Initial Impl.         90.2         9      87.6       15         84.5         18   72.7    50      77.5       43    76.1       8
                          2     Error Handling        79.9        18      81.3       31         75.4         30   62.8    76      71.3       47    63.0      16
                          3     Input General.        75.9        28      80.4       49         63.5         42   49.5    99      24.7      175    49.5      25
                          4     Add Caching           75.1        42      78.4       74         62.4         59   59.3    88      47.6      124    47.8      37
                          5     Func. Ext.            75.1        53      78.5      103         62.3         79   63.8    94      51.4      124    47.8      49
                          6     Interface Restr.      74.9        55      78.5      107         61.8         83   66.5    89      56.8      122    47.4      50
                          7     Non-func. Aug.        74.8        79      78.3      147         58.8         94   59.7   135      49.9      163    47.7      67
                          8     Algorithm Opt.        72.4        85      75.8      163         55.0         87   57.9   139      51.7      166    31.6      71

Table 4: Regression outcomes among initially solved tasks                                              Table 6: Mitigation results on 542 tasks. Gates denote the
(𝑅𝑃𝑅𝑇 1 = 100%). “Med.” denotes the median final-turn regres-                                          average number of verification gates triggered per task. 𝑅𝑃𝑅𝑇 1
sion pass rate, and “Collapsed” denotes 𝑅𝑃𝑅𝑇 8 = 0%.                                                   differences for DeepSeek reflect API non-determinism, not
                                                                                                       strategy effects, because mitigation starts at T2.
Model                            𝑁    Med. 𝑅𝑃𝑅𝑇 8        % With Regr.            % Collapsed
GPT-4o                          427          100.0%                 47.8%                 3.0%           Model       Strategy      𝑅𝑃𝑅𝑇 1     𝑅𝑃𝑅𝑇 8      % With Regr.    Gates
DeepSeek-V3                     414          100.0%                 45.9%                 1.9%                       Baseline        87.6         75.8            43.2%   —
Qwen2.5-Coder-32B               440           98.1%                 54.5%                14.3%                       S1 (Recap)      91.2         80.1            36.7%   —
                                                                                                         DeepSeek
Qwen3-32B                       397           98.2%                 50.9%                10.6%                       S2 (Gate)       91.1         87.9            12.5%   1.08
DS-R1-Distill-32B               428           92.8%                 61.2%                29.2%                       S3 (Both)       90.5         87.0            13.8%   1.21
Llama-3.1-8B                    333           16.1%                 81.7%                34.2%
                                                                                                                     Baseline        76.1         31.6            72.9%   —
Table 5: Multi-turn bug taxonomy and bug type distribution                                                           S1 (Recap)      76.1         35.8            68.3%   —
                                                                                                         Llama-8B
                                                                                                                     S2 (Gate)       76.1         47.3            54.8%   2.29
from four-annotator labels (384 samples). ★ marks types not
                                                                                                                     S3 (Both)       76.1         42.3            59.4%   2.33
well represented in prior single-turn taxonomies. BF applies
only to T1 failures.
                                                                                                       5.3    RQ3 : To what extent can interaction-level
ID       Name                         Definition                                 Count     %
                                                                                                              mitigation strategies preserve prior behavior
Baseline
                                                                                                              in multi-turn coding conversations?
BF       Baseline Failure             T1 implementation error, not a multi-         48 12.5            To answer RQ3, we evaluate whether interaction-level controls can
                                      turn bug
                                                                                                       mitigate regression accumulation during the conversation itself.
Class I: Context-Loss
CL-1      Context Loss                Forgets or overwrites a constraint from       63 16.4
                                                                                                       We compare Snowball Recap (S1), Verification Gate (S2), and their
                                      a prior turn                                                     combination (S3). S1 prepends a deterministic recap of prior turns to
CL-3     Partial Recall               Remembers function structure but              18    4.7          each new request. In S2, after each turn, we run regression tests and
                                      misses internal details
                                                                     Subtotal       81 21.1            trigger the gate only when 𝑅𝑃𝑅𝑡 < 𝑅𝑃𝑅𝑡 −1 and a last passing code
Class II: Cross-Turn Conflict                                                                          suggestion exists. We then reject the current code suggestion, send
CC-1      Semantic Collision       New logic contradicts prior logic, pro-         102 26.6            the model a rollback prompt containing the failed-test count, the
                                   ducing wrong results
CC-2     Interface Mismatch        New code breaks prior interfaces or sig-          1    0.3
                                                                                                       full last passing code suggestion, and the current-turn requirement,
                                   natures                                                             and allow exactly one retry. We retain the retry only when it passes
CC-3     Integration Inconsistency Individually correct components fail to           1    0.3
                                   integrate
                                                                                                       at least as many benchmark tests as the rejected code suggestion;
CC-4     Over-Guarding             New validation rejects inputs the speci-        110 28.6            otherwise, the current code suggestion is kept. S3 applies the recap
                                   fication treats as valid                                            (S1) and the verification gate (S2) together. Each strategy is run
                                                                  Subtotal         214 55.7
                                                                                                       on all 542 tasks with the full 8-turn chain on DeepSeek-V3 and
Class III: Accumulation
AC-1★ Regression via Omission         Silently drops necessary prior code dur-       3    0.8
                                                                                                       Llama-3.1-8B. Table 6 reports 𝑅𝑃𝑅𝑇 8 , the fraction of tasks with
                                      ing regeneration                                                 regression, and average gate triggers per task. A gate trigger is
AC-2★ Complexity Collapse             Code exceeds capacity, causing syntax         38    9.9          counted whenever the current code suggestion lowers 𝑅𝑃𝑅 relative
                                      errors or truncation
                                                                      Subtotal      41 10.7            to the previous turn.
                                                                                                       Finding 9. Verification Gate is the only strategy that pro-
                                                                                                       duces large and stable mitigation gains across both models.
                                                                                                       Under S2, DeepSeek-V3 improves from 𝑅𝑃𝑅𝑇 8 = 75.8% to 87.9% and
                                                                                                       reduces tasks with regression from 43.2% to 12.5%. Llama-3.1-8B im-
                                                                                                       proves from 31.6% to 47.3% and reduces tasks with regression from
                                                                                                       72.9% to 54.8%. In contrast, Snowball Recap alone yields smaller
ASE ’26, October 2026, Munich, Germany                                        Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao, and Lysa Xiao


improvements (DeepSeek-V3 80.1%, Llama-3.1-8B 35.8%), and com-                 systems may need stronger mechanisms for preserving earlier-turn
bining recap with gating does not surpass S2 (S3 reaches 87.0% and             requirements, checking compatibility between new and existing
42.3%). This result indicates that online behavioral verification and          logic, and deciding when to revise from a last known-good code
rollback, rather than prompt restatement alone, is the main driver             suggestion instead of continuing from a faulty one. Our mitigation
of mitigation in multi-turn coding.                                            results further suggest that these capabilities should not be left
Finding 10. Mitigation effectiveness depends on model scale                    entirely to prompting. They are likely to benefit from tighter inte-
and correction frequency. Under S2, the average number of trig-                gration between code generation, regression testing, and turn-level
gered gates is 1.08 per task on DeepSeek-V3 and 2.29 on Llama-3.1-             acceptance checks.
8B. The smaller model requires more than twice as many corrections
and still produces lower-quality results. This suggests that Verifica-         6.2      Implications
tion Gate removes a substantial share of regressions, but recovery             (1) Implication for evaluation design. Single-turn scores are in-
after a failed turn remains harder for lower-capacity models.                  sufficient to characterize reliability in conversational programming.
                                                                               Evaluation protocols should track preservation across turns and
  Our results show that Verification Gate is the only strategy that consis-    include regression-aware metrics, because turn-local correctness
  tently and substantially mitigates multi-turn regression accumulation        can coexist with failure to preserve requirements established in
  across both models. Snowball Recap yields smaller gains, and combin-
                                                                               earlier turns. In practice, this means that benchmark design should
  ing the recap with the gate does not outperform the gate alone.
                                                                               pair evolving requirements with stable regression oracles, so that
                                                                               each new turn is evaluated against both new functionality and
6 Discussion                                                                   earlier-turn requirements. Without this structure, evaluations can
6.1 Interpretation of the results                                              overestimate model robustness in maintenance-like workflows.
                                                                               (2) Implication for failure analysis. Cross-Turn Conflict is the
LLM-assisted programming is increasingly used in iterative settings            major failure class, with Over-Guarding and Semantic Collision
where requirements evolve over multiple turns. In this setting, re-            accounting for most manually labeled failures. This suggests that
liability is not only about satisfying the current request but also            future analyses should focus on how new constraints and new logic
requires preserving requirements established in earlier turns. Our             interact with requirements established in earlier turns, rather than
results show that this preservation requirement is where current               attributing multi-turn failure primarily to context loss. A direct con-
models fail systematically. Across all six models, regression accu-            sequence is that failure taxonomies and debugging workflows for
mulates as conversations proceed. For five of the six models, the              multi-turn coding should represent interaction faults explicitly, for
largest early losses appear at Turn 2 or Turn 3, where new vali-               example, incompatible validation changes, conflicting assumptions
dation or input-generalization logic must be integrated without                between turns, or integration breakage after local edits.
breaking earlier-turn requirements. Stronger models degrade more               (3) Implication for tool construction. Tooling should prioritize
gradually and finish at higher 𝑅𝑃𝑅 levels, whereas weaker models               verification-aware interaction loops, including turn-level regression
lose quality more sharply as requirements accumulate across later              checks and rollback-based retry from a known-good state. Our
turns. The dominant failures are cross-turn incompatibilities rather           results indicate that this pattern is more effective than recap-first
than isolated single-turn mistakes.                                            prompting, especially when requirements continue to evolve over
We combine fixed multi-turn evolution chains, regression-oracle                turns. For deployment, this implies that practical assistants should
tracking at every turn, and a manually validated taxonomy of multi-            treat each new code suggestion as a candidate change that requires
turn bugs. This design separates first-turn code-suggestion errors             acceptance checks, rather than assuming that additional prompt
from failures introduced by later requirement changes. It also makes           context alone will preserve earlier-turn requirements.
model-level and turn-level comparisons reproducible.
The mitigation results extend this contribution from diagnosis to              6.3      Threats to Validity
intervention. Snowball Recap helps when the model loses track of
                                                                               Internal validity. Our benchmark uses a fixed 8-turn sequence
requirements established in earlier turns by restating them before
                                                                               and controlled prompt templates. This improves comparability but
each new turn. Verification Gate addresses a different problem: a
                                                                               cannot represent all natural conversation patterns. We mitigate
later code suggestion may still break earlier-turn requirements even
                                                                               this by applying the same protocol to all models, adding stratified
when those requirements are present in the conversation context. In
                                                                               analyses, and reporting initially solved-task results. We also set the
that case, prompt restatement alone is not enough. Verification Gate
                                                                               temperature to 0.0 for reproducibility, while acknowledging that
is therefore the only strategy that yields consistent gains in both
                                                                               stochastic decoding in deployment may behave differently.
stronger and weaker models. Snowball Recap yields smaller gains,
                                                                               Construct validity. We measure preservation with turn-level re-
and adding it to Verification Gate does not improve on Verification
                                                                               gression pass rate (𝑅𝑃𝑅) against benchmark tests. This captures
Gate alone. This pattern suggests that the main problem in our
                                                                               tested behavioral preservation but not all quality dimensions, such
setting is not simply loss of earlier-turn context, but failure to
                                                                               as readability or untested edge cases. To reduce measurement arti-
preserve earlier-turn requirements.
                                                                               facts, we reuse benchmark-validated tests and apply deterministic
These results also suggest several directions for future LLMs for
                                                                               adaptation for interface restructuring turns. For taxonomy label-
code generation. This points to a need for models that treat later
                                                                               ing, we use a frozen codebook, independent four-annotator coding,
turns less as isolated generation steps and more as constrained
                                                                               adjudication, and substantial agreement (𝜅 = 0.799).
code updates over an evolving code state. More specifically, future
Regression Accumulation in Multi-Turn LLM Programming Conversations                                                                 ASE ’26, October 2026, Munich, Germany


External validity. Our tasks are Python function-level problems                               Representations, B. Kim, Y. Yue, S. Chaudhuri, K. Fragkiadaki, M. Khan, and Y. Sun
from HumanEval+ and MBPP+, so effect sizes may not directly                                   (Eds.). 8746–8825.
                                                                                         [10] William G Cochran. 1977. Sampling techniques. Johan Wiley & Sons Inc (1977).
transfer to other languages, repository-scale maintenance, or human-                     [11] Daniela S Cruzes and Tore Dyba. 2011. Recommended steps for thematic synthesis
in-the-loop settings. We partially broaden coverage by evaluating                             in software engineering. In 2011 international symposium on empirical software
                                                                                              engineering and measurement. IEEE, 275–284.
six models from both the commercial and open-source families.                            [12] Vardhan Dongre, Ryan A Rossi, Viet Dac Lai, David Seunghyun Yoon, Dilek
Further replications on larger repositories and additional languages                          Hakkani-Tür, and Trung Bui. 2025. Drift No More? Context Equilibria in Multi-
are needed.                                                                                   Turn LLM Interactions. arXiv preprint arXiv:2510.07777 (2025).
                                                                                         [13] Beat Fluri, Michael Wursch, Martin PInzger, and Harald Gall. 2007. Change
                                                                                              distilling: Tree differencing for fine-grained source code change extraction. IEEE
7    Conclusion                                                                               Transactions on software engineering 33, 11 (2007), 725–743.
                                                                                         [14] Cuiyun Gao, Xing Hu, Shan Gao, Xin Xia, and Zhi Jin. 2025. The current chal-
LLM-assisted programming is increasingly used in iterative soft-                              lenges of software engineering in the era of large language models. ACM Trans-
ware development workflows where requirements evolve over mul-                                actions on Software Engineering and Methodology 34, 5 (2025), 1–30.
tiple turns. In this setting, reliability depends on whether newly                       [15] Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Taco Cohen, and Gabriel
                                                                                              Synnaeve. 2025. RLEF: Grounding Code LLMs in Execution Feedback with
generated code preserves behavior that was correct in earlier turns.                          Reinforcement Learning. In ICML.
This paper investigates the preservation problem through regres-                         [16] Ángel González-Prieto, Jorge Perez, Jessica Diaz, and Daniel López-Fernández.
                                                                                              2023. Reliability in software engineering qualitative research through Inter-Coder
sion accumulation in multi-turn coding conversations.                                         Agreement. Journal of Systems and Software 202 (2023), 111707.
    We conduct a controlled empirical study on 542 tasks, six models,                    [17] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek
and 26,016 turn instances. We provide a reproducible benchmark                                Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex
                                                                                              Vaughan, et al. 2024. The llama 3 herd of models.
protocol for turn-level regression evaluation, a taxonomy of multi-                      [18] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu,
turn regression bugs from a four-annotator analysis of 384 stratified                         Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. 2025. Deepseek-r1: Incen-
failures. We also evaluate interaction-level mitigation strategies                            tivizing reasoning capability in llms via reinforcement learning. arXiv preprint
                                                                                              arXiv:2501.12948 (2025).
based on recap and verification gate mechanisms.                                         [19] Huizi Hao, Kazi Amit Hasan, Hong Qin, Marcos Macedo, Yuan Tian, Steven HH
    Our findings show that regression accumulation appears across                             Ding, and Ahmed E Hassan. 2024. An empirical study on developers’ shared
                                                                                              conversations with ChatGPT in GitHub pull requests and issues. Empirical
all evaluated models. We find that Cross-Turn Conflict is the major                           Software Engineering 29, 6 (2024), 150.
failure class, and that Verification Gate is the only mitigation strat-                  [20] Kim Herzig, Sascha Just, Andreas Rau, and Andreas Zeller. 2013. Predicting
egy that yields consistent gains across both stronger and weaker                              defects using change genealogies. In 2013 IEEE 24th International Symposium on
                                                                                              Software Reliability Engineering (ISSRE). IEEE, 118–127.
models. Taken together, these results suggest that conversational                        [21] Soodeh Hosseini and Mohammad Abdollahi Azgomi. 2008. UML model refactor-
code generation should be treated as an evolving maintenance                                  ing with emphasis on behavior preservation. In 2008 2nd IFIP/IEEE International
process rather than a sequence of isolated prompt outcomes.                                   Symposium on Theoretical Aspects of Software Engineering. IEEE, 125–128.
                                                                                         [22] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo,
                                                                                              David Lo, John Grundy, and Haoyu Wang. 2024. Large language models for
Data Availability                                                                             software engineering: A systematic literature review. ACM Transactions on
                                                                                              Software Engineering and Methodology 33, 8 (2024), 1–79.
Our benchmark (542 tasks × 8 turns), all experimental results across                     [23] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu
6 models, bug annotations, and analysis scripts are available at                              Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder technical
                                                                                              report. arXiv preprint arXiv:2409.12186 (2024).
https://anonymous.4open.science/r/multiturn-code-bugs.                                   [24] Arnav Kumar Jain, Gonzalo Gonzalez-Pumariega, Wayne Chen, Alexander M
                                                                                              Rush, Wenting Zhao, and Sanjiban Choudhury. 2025. Multi-Turn Code Genera-
References                                                                                    tion Through Single-Step Rewards. In 42nd International Conference on Machine
                                                                                              Learning.
 [1] Altaf Allah Abbassi, Leuson Da Silva, Amin Nikanjam, and Foutse Khomh. 2025.
                                                                                         [25] Yiyang Jin, Kunzhao Xu, Hang Li, Xueting Han, Yanmin Zhou, Cheng Li, and
     A Taxonomy of Inefficiencies in LLM-Generated Python Code. In 2025 IEEE
                                                                                              Jing Bai. 2026. ReVeal: Self-Evolving Code Agents via Reliable Self-Verification.
     International Conference on Software Maintenance and Evolution (ICSME). IEEE,
                                                                                              In The 14th International Conference on Learning Representations.
     393–404.
                                                                                         [26] Gregor Kiczales, John Lamping, Anurag Mendhekar, Chris Maeda, Cristina Lopes,
 [2] Davide Arcelli, Vittorio Cortellessa, and Catia Trubiani. 2012. Antipattern-based
                                                                                              Jean-Marc Loingtier, and John Irwin. 1997. Aspect-oriented programming. In
     model refactoring for software performance improvement. In Proceedings of the
                                                                                              European conference on object-oriented programming. Springer, 220–242.
     8th international ACM SIGSOFT conference on Quality of Software Architectures.
                                                                                         [27] Myeongsoo Kim, Shweta Garg, Baishakhi Ray, Varun Kumar, and Anoop Deoras.
     33–42.
                                                                                              2026. CodeAssistBench (CAB): Dataset & benchmarking for multi-turn chat-based
 [3] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk
                                                                                              code assistance. Advances in Neural Information Processing Systems 38.
     Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le,
                                                                                         [28] Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi
     et al. 2021. Program synthesis with large language models. arXiv preprint
                                                                                              Singh, Kate Baumli, Shariq Iqbal, Colton Bishop, Rebecca Roelofs, Lei M Zhang,
     arXiv:2108.07732.
                                                                                              Kay McKinney, Disha Shrivastava, Cosmin Paduraru, George Tucker, Doina
 [4] Peter Bambazek, Iris Groher, and Norbert Seyff. 2023. Requirements engineering
                                                                                              Precup, Feryal Behbahani, and Aleksandra Faust. 2025. Training Language
     for sustainable software systems: a systematic mapping study. Requirements
                                                                                              Models to Self-Correct via Reinforcement Learning. In The 13th International
     Engineering 28, 3 (2023), 481–505.
                                                                                              Conference on Learning Representations.
 [5] Laszlo A. Belady and Meir M Lehman. 1976. A model of large program develop-
                                                                                         [29] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng,
     ment. IBM Systems journal 15, 3 (1976), 225–252.
                                                                                              Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient
 [6] Shawn A Bohner. 2002. Software change impacts-an evolving perspective. In
                                                                                              memory management for large language model serving with pagedattention. In
     International Conference on Software Maintenance, 2002. Proceedings. IEEE, 263–
                                                                                              Proceedings of the 29th symposium on operating systems principles. 611–626.
     272.
                                                                                         [30] Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, and Jennifer Neville. 2025. Llms
 [7] Ned Chapin, Joanne E Hale, Khaled Md Khan, Juan F Ramil, and Wui-Gee Tan.
                                                                                              get lost in multi-turn conversation. arXiv preprint arXiv:2505.06120.
     2001. Types of software evolution and software maintenance. Journal of software
                                                                                         [31] J Richard Landis and Gary G Koch. 1977. The measurement of observer agreement
     maintenance and evolution: Research and Practice 13, 1 (2001), 3–30.
                                                                                              for categorical data. biometrics (1977), 159–174.
 [8] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde
                                                                                         [32] Bennett P Lientz and E Burton Swanson. 1980. Software maintenance management.
     De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph,
                                                                                              Addison-Wesley Longman Publishing Co., Inc.
     Greg Brockman, et al. 2021. Evaluating large language models trained on code.
                                                                                         [33] Bennet P Lientz, E. Burton Swanson, and Gail E Tompkins. 1978. Characteristics
     arXiv preprint arXiv:2107.03374.
                                                                                              of application software maintenance. Commun. ACM 21, 6 (1978), 466–471.
 [9] Xinyun Chen, Maxwell Lin, Nathanael Schaerli, and Denny Zhou. 2024. Teaching
     Large Language Models to Self-Debug. In International Conference on Learning
ASE ’26, October 2026, Munich, Germany                                                  Yonghui (Andie) Huang, Lin Ma, Amjed Tahir, Qian Zhang, Liwen Xiao, and Lysa Xiao


[34] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Cheng-              hierarchical debugging.
     gang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3         [42] Klaas-Jan Stol, Paul Ralph, and Brian Fitzgerald. 2016. Grounded theory in
     technical report. arXiv preprint arXiv:2412.19437 (2024).                                software engineering research: a critical review and guidelines. In Proceedings of
[35] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is your            the 38th International conference on software engineering. 120–131.
     code generated by chatgpt really correct? rigorous evaluation of large language     [43] Peiding Wang, Li Zhang, Fang Liu, Lin Shi, Minxiao Li, Bo Shen, and An Fu. 2025.
     models for code generation. Advances in neural information processing systems            Codeif-bench: Evaluating instruction-following capabilities of large language
     36, 21558–21572.                                                                         models in interactive code generation. arXiv preprint arXiv:2503.22688 (2025).
[36] Robert Miller and Anand Tripathi. 1997. Issues with exception handling in           [44] Sizhe Wang, Zhengren Wang, Dongsheng Ma, Yongan Yu, Rui Ling, Zhiyu Li,
     object-oriented systems. In European Conference on Object-Oriented Programming.          Feiyu Xiong, and Wentao Zhang. 2026. Codeflowbench: A multi-turn, iterative
     Springer, 85–103.                                                                        benchmark for complex code generation. (2026), 4369–4402.
[37] Nachiappan Nagappan and Thomas Ball. 2005. Use of relative code churn mea-          [45] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng,
     sures to predict system defect density. In Proceedings of the 27th international         Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. 2025. Qwen3 technical
     conference on Software engineering. 284–292.                                             report. arXiv preprint arXiv:2505.09388 (2025).
[38] OpenAI. 2024. Hello GPT-4o. https://openai.com/index/hello-gpt-4o/. Official        [46] Stephen S Yau, James S Collofello, and T MacGregor. 1978. Ripple effect analysis
     model announcement.                                                                      of software maintenance. In The IEEE Computer Society’s Second International
[39] Ruchit Rawal, Jeffrey Yang Fan Chiang, Chihao Shen, Jeffery Siyuan Tian, Aastha          Computer Software and Applications Conference, 1978. COMPSAC’78. IEEE, 60–65.
     Mahajan, Tom Goldstein, and Yizheng Chen. 2025. Benchmarking Correctness            [47] Shin Yoo and Mark Harman. 2012. Regression testing minimization, selection
     and Security in Multi-Turn Code Generation. arXiv preprint arXiv:2510.13859              and prioritization: a survey. Software testing, verification and reliability 22, 2
     (2025).                                                                                  (2012), 67–120.
[40] Carolyn B. Seaman. 1999. Qualitative methods in empirical studies of software       [48] Pamela Zave. 1993. Feature interactions and formal specifications in telecommu-
     engineering. IEEE Transactions on software engineering 25, 4 (1999), 557–572.            nications. Computer 26, 8 (1993), 20–28.
[41] Yuling Shi, Songsong Wang, Chengcheng Wan, Min Wang, and Xiaodong Gu.
     2024. From code to correctness: Closing the last mile of code generation with
