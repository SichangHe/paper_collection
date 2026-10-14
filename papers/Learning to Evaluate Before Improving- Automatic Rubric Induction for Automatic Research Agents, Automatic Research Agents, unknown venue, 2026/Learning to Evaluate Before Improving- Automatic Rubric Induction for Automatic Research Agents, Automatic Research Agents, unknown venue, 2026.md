                                                   Learning to Evaluate Before Improving: Automatic Rubric Induction for
                                                                        Automatic Research Agents
                                         Xuehai Wang1 , Haowei Qin2 , Tongxin Liu3 , Junkai Li4 , Buqiang Xu1 , Jintian Zhang1 , Yijun Chen1 ,
                                                                           Zirui Xue1 , Shumin Deng1∗
                                                                                                       1
                                                                                                         Zhejiang University
                                                                                2
                                                                                    University of Electronic Science and Technology of China
                                                                                     3
                                                                                       Beijing University of Posts and Telecommunications
                                                                                               4
                                                                                                 Zhejiang University of Technology
                                                                                           22651308@zju.edu.cn, 231sm@zju.edu.cn
arXiv:2608.31076v1 [cs.CL] 31 Aug 2026




                                                                       Abstract                                         Open-ended Research Task               Implicit Requirements
                                                                                                                                                                    Objectives
                                           Autonomous scientific research agents are increasingly ap-                  Combine diverse observations to               Methods
                                           plied to end-to-end scientific workflows, including literature              measure global glacier mass loss…             Evidence
                                           review, data analysis, experimentation, and report generation.                                                         Success Criteria
                                           However, open-ended research tasks often do not clearly spec-
                                           ify the analyses, methods, and success criteria required to
                                           complete the task. As a result, agents may miss important anal-                                                     Final Report
                                           yses, use inappropriate methods, or draw conclusions that are                              Planning             Missed Analyses
                                           insufficiently supported by evidence. To address the problem,                                               Wrong Procedures
                                           we present AutoSciRub, an evaluation-first framework that in-                             Execution
                                                                                                                                                       Unsupported Conclusions
                                           duces a task-specific executable rubric before research execu-
                                           tion, and uses it to guide execution, criterion-level verification
                                           as well as iterative revision. AutoSciRub decomposes an un-
                                           derspecified instruction into atomic scientific goals, grounds         Figure 1: Why autonomous research agents struggle with
                                           them in relevant literature and task-visible data, and synthe-         open-ended research tasks.
                                           sizes specific, actionable, and verifiable criteria. The resulting
                                           rubric makes implicit experimental and evidential require-
                                           ments explicit, providing guidance for experiments and analy-
                                           ses. During revision, rubric-guided verification identifies un-        artifacts (Lu et al. 2024; Schmidgall et al. 2025; Mitchener
                                           met criteria and enables targeted refinement of the research re-       et al. 2025). However, as their execution capabilities im-
                                           port and its supporting artifacts. On ResearchClawBench, Au-           prove, a fundamental challenge becomes more pressing: how
                                           toSciRub consistently improves all tested configurations, with         can we ensure that the resulting research actually fulfills the
                                           an average gain of 2.08 points across three backbone LLMs              scientific intent of the original instruction? Scientific instruc-
                                           under the fixed Codex harness and 2.95 points across three             tions often specify only a high-level objective while leaving
                                           agent harnesses using a fixed DeepSeek-V4-Flash backbone.              intermediate goals, methodological requirements, expected
                                           On a randomly sampled 20-task subset of AstaBench E2E Dis-             evidence, and success conditions implicit. As a result, an
                                           covery, AutoSciRub further achieves an average improvement
                                           of 16.8 points across three agent harnesses, while maintain-
                                                                                                                  agent may produce a plausible-looking report while omit-
                                           ing or increasing the number of successfully completed tasks.          ting essential analyses, using inappropriate procedures, or
                                           These results demonstrate that evaluation-first guidance pro-          making claims unsupported by experimental evidence. Fig-
                                           vides an effective and generalizable control mechanism for             ure 1 illustrates how these implicit requirements can lead to
                                           autonomous scientific research1 .                                      failures throughout research planning and execution.
                                                                                                                     Existing scientific-agent benchmarks evaluate research
                                                                                                                  outputs using executable metrics, expert-authored rubrics,
                                                                 1    Introduction                                and LLM-based judgments (Yehudai et al. 2026). Expert-
                                         Large language model agents are increasingly being used to               authored rubrics are particularly useful because they provide
                                         automate scientific research workflows, including literature             explicit and interpretable criteria for assessing complex re-
                                         review, hypothesis formulation, experimental design, code                search artifacts (Starace et al. 2025). However, constructing
                                         implementation, result analysis, and scientific report genera-           them requires substantial domain expertise and manual ef-
                                         tion (Wei et al. 2025). Recent systems have further advanced             fort, making them difficult to scale to new research tasks.
                                         toward multi-agent and long-horizon research processes that              Recent work on automatic rubric generation offers a promis-
                                         produce both scientific reports and supporting experimental              ing alternative by deriving task-specific criteria from natural-
                                                                                                                  language instructions and contextual information (Chen et al.
                                            1                                                                     2026a; Siro, Aliannejadi, and Aliannejadi 2026; Ding 2026).
                                                The code is available at https://github.com/zjunlp/AutoSciRub.
                                            ∗
                                                Corresponding author.                                             Nevertheless, scientific rubric generation is especially chal-
lenging because valid criteria depend not only on the in-          port persistent agents through structured long-horizon mem-
struction, but also on task-relevant literature, available data,   ory (Xu et al. 2026a; Li et al. 2026a), cache-efficient context
domain conventions, and execution constraints. Without such        control (Xu et al. 2026b), and hierarchical multimodal ex-
grounding, automatically generated criteria may be incom-          perience storage (Chen et al. 2026c). In parallel, scientific-
plete, scientifically unjustified, or infeasible to verify.        agent benchmarks have progressed from executable coding
    Moreover, rubrics in existing scientific-agent benchmarks      and model-development tasks under fixed objectives (Chen
are predominantly treated as post-hoc evaluation instru-           et al. 2025; Chan et al. 2025), to research reproduction that
ments. They score completed artifacts, but do not help the         requires reconstructing methods and experiments (Starace
agent determine what evidence should be produced or how            et al. 2025; Luo et al. 2026), and further to end-to-end
an incomplete artifact should be improved. We argue that           settings that assess experiment formulation, raw-evidence
rubrics should instead serve as intermediate scientific spec-      analysis, and scientific report generation from high-level in-
ifications. They should make the implicit requirements of          structions (Bragg et al. 2025; Garikaparthi, Patwardhan, and
a research task explicit and connect task interpretation, re-      Cohan 2026; Wang et al. 2026; Xu et al. 2026c).
search execution, output verification, and iterative revision.        Rubric-Guided Evaluation and Iterative Refinement.
Under this view, a reliable research agent should learn to         Rubric-based evaluation offers a structured alternative
evaluate before improving.                                         to holistic judging through explicit, fine-grained crite-
    Based on this principle, we introduce AutoSciRub, a            ria (Hashemi et al. 2024; Chen et al. 2026a). Expert-authored
framework that automatically induces evidence-grounded             hierarchical rubrics decompose complex research artifacts
scientific rubrics and uses them to guide iterative research       into independently assessable components (Starace et al.
improvement. AutoSciRub consists of two stages. First, Auto-       2025; Sharma et al. 2025), while later benchmarks introduce
matic Rubric Induction decomposes the original instruction         atomic, verifiable criteria and question-specific scoring or de-
into atomic scientific goals and grounds them in relevant lit-     duction points (Li et al. 2026b; Fan et al. 2024). Rubric con-
erature, web evidence, available task data, and environmental      struction has become increasingly automated (Siro, Alian-
constraints. The resulting task-specific rubric makes the re-      nejadi, and Aliannejadi 2026; Ding 2026; Yu et al. 2026).
quired analyses, evidence, and success conditions explicit.        Recent methods generate dataset- or instance-specific cri-
Second, after the agent produces a research report and sup-        teria (Wang and Blanco 2026), retrieve rubric knowledge
porting artifacts, Rubric-Guided Iterative Revision evaluates      from related queries (Dhole and Agichtein 2026; Chen et al.
the available evidence criterion by criterion, identifies un-      2026b), or recursively expand questions into structured crite-
met scientific requirements, and provides targeted feedback        ria trees (Gao et al. 2026; Zhu et al. 2026); recursive decom-
for revision.                                                      position and filtering further reduce redundancy, overlap, and
    We evaluate AutoSciRub on all 40 tasks in Research-            preference misalignment (Shen et al. 2026; Hong et al. 2026).
ClawBench and a fixed subset of 20 end-to-end scientific           Recent refinement frameworks combine explicit rubrics with
discovery tasks from AstaBench. On ResearchClawBench,              test-time verifiers or pre-execution checks to assess outputs
AutoSciRub yields an average improvement of 2.08 points            against task-specific criteria (Wan et al. 2026; LeVine et al.
across three backbone LLMs under the fixed Codex harness           2026; Ye et al. 2026; Zheng et al. 2026). Criterion-level diag-
and 2.95 points across three agent harnesses using the fixed       noses are then fed back into generation for targeted revision
DeepSeek-V4-Flash backbone. On AstaBench, it further im-           of responses (Madaan et al. 2023; Gou et al. 2024), agent
proves scores by an average of 16.8 points across three agent      trajectories, and tool-use programs (LeVine et al. 2026).
systems. These results demonstrate that automatically in-
duced, evidence-grounded rubrics can provide scalable eval-
uation criteria while also serving as effective guidance for
autonomous scientific research.                                                            3    Method

                    2   Related Work                               Autonomous research agents often revise their outputs with-
Autonomous Scientific Research Agents and Bench-                   out an explicit specification of the scientific requirements
marks. Early systems organize end-to-end scientific research       that the task entails. Our framework addresses this limita-
as single-agent pipelines or centrally orchestrated work-          tion by first transforming an underspecified research instruc-
flows, coordinating literature review, experimentation, and        tion into a task-specific executable rubric and then using the
manuscript preparation within a unified process (Lu et al.         rubric to guide research execution, verification, and revi-
2024; Yamada et al. 2025; Ifargan et al. 2024). Multi-agent        sion. As illustrated in Figure 2, Automatic Rubric Induction
systems instead distribute these stages across specialized         first constructs an instruction-derived rubric skeleton through
roles for collaborative ideation, critical discussion, experi-     Rubric Skeleton Induction, and then transforms it into a
ment execution, and research coordination (Schmidgall et al.       task-specific executable rubric through Scientific Literature
2025; Ghareeb et al. 2026; Tang et al. 2025; Gottweis et al.       Grounding, Task-Data Exploration, and Criterion Synthesis.
2026), while shared research states support long-horizon ex-       Rubric-Guided Iterative Revision subsequently evaluates the
ploration, failure recovery, and iterative hypothesis refine-      generated research artifact criterion by criterion and provides
ment (Mitchener et al. 2025; Lyu et al. 2026; Gao, Fang, and       targeted feedback on missing experiments, comparisons, and
Zitnik 2026; Liu et al. 2026; Lu et al. 2026). Complemen-          evidence. We first formulate the research task and then de-
tary memory and context-management systems further sup-            scribe the two stages in detail.
  Ⅰ. Automatic Rubric Induction                           Scientific Literature                                                                 Ⅱ. Rubric-Guided
                                                          2   Grounding                Filtering                 Grounded                       Iterative Revision
                                                                                                                               Rubric
                                                                                                                 Knowledge      Rubr
                                                                                                                                Rub
                                   goal 1               query 1              papers                                             Rubr
                                                                                                                                 Rub
                                                                                                                               Goal: to ……
                                                                                                                                 Rubr
                                                                                                                                 Rub
                                                                                                                               DataSources:
                                                                                                                                  ic
                                                                                                                                 ric
                                                                                                                                   ic
                                                                                                                                  ric
                                                                                                                               Experiments:
                                                                                                                                    ic
                                                                                                                                   ric
                                                                                                                               Metrics:
                                   goal 2               query 2          data docs                                             Artifacts:
  Instruction
                                   goal 3               query 3         method docs
      Data                                                                                                                         Input
                                                 Search tool set                                                                              Execution
                    Rubric Skeleton
                                                                                       Methods & Protocols
                    1 Induction                                                        Metrics & Baselines
  Earth Chem.                                                                          Controls & Ablations
                                                                                       Evidence Artifacts
                                                                                                                                Feedback
                                                                                                                                  Missing
   Info.   Energy
                                                                                      4 Criterion               Rubric
                                                                                                               Rubric1
                                                                                                                                experiment
                                                                                                                                 Rubric
                                       Data Profile                Goals                                       Rubric1          Incomplete                   Final
                                                                   Goal
                                                                   Goal 23              Synthesis             Goal:
                                                                                                               Goal:to ……
                                       Format                                                                   Goal:toto……
                                                                                                              DataSources:……    comparison                   Report
  Physics Astro.                                                                                                 Rubric
                                                                                                               DataSources:
                                                                                                                  Rubric
                                                                                                                DataSources:
                                                                                                                   Rubric
                                                                                                              Experiments:
                                                                                                               Expreiments:
                                        Fields                                                                  Expreiments:
                                                                                                              Metrics:
                    3 Task-Data                                                                                Metrics:
                                                                                                                Metrics:
                                       Data Relations                                                         Artifacts:
                                                                                                               Artifacts:
  Math Neuro.        Exploration                                                                                Artifacts:
                                                                                                                                              Verification
  …                                   …


Figure 2: Overview of AutoSciRub. (1) Automatic Rubric Induction: starting from a multi-domain scientific task, AutoSciRub
induces a rubric skeleton, grounds it in scientific literature, explores the task-visible data, and synthesizes a task-specific
executable rubric. (2) Rubric-Guided Iterative Revision: the induced rubric guides research execution and supports an iterative
feedback loop that verifies and improves the generated artifact into the final report.


3.1        Task Formulation                                                                3.2        Automatic Rubric Induction
                                                                                           Rather than selecting criteria from a fixed library, we induce
We consider a collection of multi-domain, end-to-end au-
                                                                                           a task-specific executable rubric at inference time. As shown
tonomous scientific research tasks D spanning Astronomy,
                                                                                           in Figure 2, this process consists of four steps: Rubric Skele-
Chemistry, Earth Science, Energy Science, Information Sci-
                                                                                           ton Induction, Scientific Literature Grounding, Task-Data
ence, Life Science, Materials Science, Mathematics, Neu-
                                                                                           Exploration, and Criterion Synthesis. These steps make the
roscience, and Physics. Each task is represented as τi =
                                                                                           instruction’s implicit requirements explicit, ground them in
(xi , Ei ), where xi is a high-level research instruction and Ei
                                                                                           established scientific practice and task-visible resources, and
is the task-visible environment, including available literature,
                                                                                           convert them into verifiable criteria.
data, search, code execution, and domain-specific tools.
    Given τi , a research agent π performs scientific reasoning,                           Rubric Skeleton Induction. A high-level research instruc-
experimentation, and analysis to produce                                                   tion often implies multiple analyses, comparisons, and inter-
                                                                                           pretations without listing them explicitly. We organize these
                     Aπi = π(xi , Ei ) = (ri , Si ),                         (1)           requirements into a compact set of atomic scientific goals:
                                                                                                                                      K
where ri is the scientific report and Si contains its supporting                                           Gbi = ϕinst (xi ) = {gi,k } i ,    k=1    (4)
code, results, analyses, tables, and figures.                                              where Ki is the number of induced goals and gi,k =
   Research instructions are typically underspecified: they                                (ni,k , si,k ) contains a concise goal name ni,k and a con-
state a broad objective without fully defining the scientific                              crete scientific requirement si,k . Together, these goals form
questions, comparisons, or evidence required. We therefore                                 an instruction-derived rubric skeleton.
associate each task with a latent scientific specification                                    The goals must be traceable to the instruction, cover its
                                                                                           main requirements, and avoid unnecessary overlap. At this
                           Zi∗ = (Gi∗ , Ci∗ ),                               (2)           stage, the agent observes only xi and does not introduce
                                                                                           specific methods, metrics, baselines, or expected results. The
where Gi∗ denotes the required scientific goals and Ci∗ the                                skeleton therefore defines what the task should address, while
evidence requirements for verifying them. Artifact quality is                              later steps determine how each goal should be established.
defined by                                                                                 Scientific Literature Grounding. The rubric skeleton de-
                        qiπ = Eval (Aπi ; Zi∗ ) ,                            (3)           fines the task scope but not the scientific practice needed
                                                                                           to satisfy each goal. For every gi,k , the agent forms broad
where Eval(·) assesses goal coverage and evidence adequacy.                                queries over relevant concepts, methods, metrics, and stan-
Our objective is to improve the artifact quality across tasks.                             dard protocols. It first consults task-provided related litera-
   Since neither Zi∗ nor its evaluator is available during ex-                             ture and then supplements missing coverage through the na-
ecution, AutoSciRub induces an instruction-derived rubric                                  tive web-search capability of the agent harness and external
skeleton Gbi and a task-specific executable rubric Rb i from the                           services, including arXiv, OpenAlex, Semantic Scholar, and
instruction, scientific literature, and task-visible data. The                             Tavily. The retrieved sources may include papers, preprints,
rubric operationalizes the latent specification and guides ex-                             official dataset or benchmark pages, method repositories, and
ecution, criterion-level verification, and iterative revision.                             software documentation.
                                                                                 100
   Queries avoid long instruction spans, task identifiers, and
                                                                                                                           Vanilla           + AutoSciRub
task-specific filenames. Candidate papers are ranked by rel-                                     20/20
                                                                                  90                                                                        20
                                                                                                 90.62                 20/20
evance to the induced goals. Before full-text access, the re-




                                                                                                                                                             Successful Tasks
                                                                                                                                                 86.34




                                                                                         +19.4
trieval layer removes candidates whose titles match a hidden                                                           84.35




                                                                    Mean Score
                                                                                  80




                                                                                                               +12.6




                                                                                                                                     +18.4
target-paper blocklist maintained by the evaluation harness                                                                              19/20 19/20
                                                                                                                                                            19
and unavailable to the induction agent. The agent then retains                    70                          71.74
                                                                                        71.26
five to seven core papers for the task and consults additional                                                                       67.96
documentation when needed.                                                              18/20                18/20
                                                                                  60                                                                        18
   For each goal, the selected sources are summarized as
                                                                                50    Claude Code                Codex               OpenClaw
                    Ki,k = ϕlit gi,k ; Lei ,                (5)
                                                                    Figure 3: Performance comparison on AstaBench. Au-
where Lei is the filtered source set. Ki,k records relevant         toSciRub consistently improves mean benchmark scores
methods and protocols, typical analyses, metrics, baselines,        across all three evaluated agent configurations.
controls, ablations, robustness checks, and useful evidence
forms. The information is organized by scientific goal rather
than by individual paper. Retrieved sources guide experi-           Criterion-Level Verification. The initial execution may
ment and evidence design but are not treated as experimental        still leave some rubric requirements unmet. At revision round
evidence for the current task.                                      t, a verifier checks each criterion against the current artifact:
Task-Data Exploration. Literature grounding describes                              
                                                                                      (t) (t)
                                                                                                        
                                                                                                                  (t)
                                                                                                                      
what is scientifically appropriate, but the proposed analy-                          zi,j , di,j = Verify ρi,j , Ai ,             (8)
ses must also be supported by the available resources. The
                                                                                        (t)
agent therefore performs a lightweight inspection of the task-      where zi,j ∈ {0, 1} indicates whether the criterion is sat-
visible data:                                                                                    (t)
                        Pi = ϕdata (Ei ) ,                  (6)     isfied, and di,j describes the remaining evidence gap. The
                                                                    verifier considers the required experiments, reported results,
where Pi records the available files and datasets, their for-       supporting artifacts, and whether the conclusions are ade-
mats and dimensions, key fields, units, labels, experimental        quately supported. This criterion-level check identifies spe-
conditions, cross-source relations, and relevant constraints.       cific omissions rather than returning only a holistic score.
   This profile identifies which data sources support each goal
and which literature-suggested analyses are feasible without        Targeted Revision. Failed criteria and their diagnoses
                                                                                                     (t)
assuming unavailable labels, conditions, or reference values.       form the revision feedback ∆i . The agent then updates
It is used only for planning; full experiments and analyses         the current artifact by addressing these gaps:
are deferred to task execution.                                                                                   
                                                                                  (t+1)            (t)   (t)
Criterion Synthesis. Finally, the agent combines the                            Ai       = πrev Ai , ∆i , Ei | R bi .  (9)
rubric skeleton, literature-grounded knowledge, and task-
                                                                    A revision may add missing experiments or comparisons,
data profile. It selects feasible experiments and analyses for
                                                                    correct evidence artifacts, strengthen the analysis, or remove
each goal and specifies the evidence needed to support the
                                                                    unsupported claims. The process stops when all criteria are
resulting claims. These requirements are synthesized into a
                                                                    satisfied or the revision budget is reached, yielding the final
task-specific executable rubric:                                                      (T )
                                                                  artifact A∗i = Ai .
       Rb i = ϕsyn Gbi , {Ki,k }Ki , Pi = {ρi,j }Mi , (7)
                                 k=1               j=1
                                                                                                         4   Experiments
where Mi is the number of synthesized criteria. Each crite-
rion ρi,j links to one or more scientific goals and specifies the   4.1                Experimental Setup
relevant data sources, required experiments or analyses, eval-      Benchmarks and Metrics. We evaluate AutoSciRub on
uation metrics and comparisons, expected evidence artifacts,        ResearchClawBench (Xu et al. 2026c) and the End-to-End
and its satisfaction condition.                                     Discovery category of AstaBench (Bragg et al. 2025). Re-
   The resulting rubric aligns established scientific practice      searchClawBench contains 40 tasks across ten scientific do-
with the evidence that can be produced from the current task,       mains. AstaBench evaluates end-to-end AI and NLP research
providing an explicit specification for subsequent research         from experimentation to report generation, and we randomly
execution and verification.                                         sample 20 tasks from its Easy split. We report the average
                                                                    rubric-based score on both benchmarks and task completion
3.3   Rubric-Guided Iterative Revision                              on AstaBench. Further details are provided in Appendix A.
The induced rubric is provided to the backbone research             Implementation Details. We compare each vanilla agent
agent as an execution-time specification. Conditioned on R    bi,
                                                                    with its AutoSciRub-augmented counterpart under identi-
the agent performs the required experiments and analyses and        cal task inputs, tools, and execution environments. For Re-
                               (0)       (0)    (0)
produces an initial artifact Ai = (ri , Si ), containing            searchClawBench, we evaluate both cross-model and cross-
the report and its supporting code, results, tables, and figures.   harness generalization. In cross-model evaluation, we fix
A. Cross-Model Generalization Fixed agent harness:       Codex
Backbone LLM Setting          Overall      Astro.         Chem.          Earth       Energy         Info.        Life        Mater.        Math         Neuro.         Phys.
                vanilla       18.66        29.69        10.97        21.25        17.87        17.61        16.02        17.55        16.65               5.60         33.43
  GPT-5.4
                +AutoSciRub 21.04 ↑ 2.38 31.43 ↑ 1.74 11.62 ↑ 0.65 22.22 ↑ 0.97 22.70 ↑ 4.83 13.92 ↓ 3.69 19.85 ↑ 3.83 22.70 ↑ 5.15 20.57 ↑ 3.92       7.72 ↑ 2.12   37.69 ↑ 4.26
                vanilla       20.86        31.56        11.96        23.99        17.95        15.69        16.88        22.14        24.20         5.84        38.40
  GLM-5.2
                +AutoSciRub 22.73 ↑ 1.87 31.99 ↑ 0.43 17.85 ↑ 5.89 23.25 ↓ 0.74 20.70 ↑ 2.75 18.00 ↑ 2.31 17.34 ↑ 0.46 23.48 ↑ 1.34 23.03 ↓ 1.17 12.58 ↑ 6.74 39.06 ↑ 0.66
                vanilla       19.05        28.01        13.36        19.14        19.65         9.31        15.10        22.31        22.96         6.30        34.37
  MiniMax-M3
                +AutoSciRub 21.04 ↑ 1.99 27.10 ↓ 0.91 13.94 ↑ 0.58 21.53 ↑ 2.39 26.46 ↑ 6.81 12.20 ↑ 2.89 17.58 ↑ 2.48 20.86 ↓ 1.45 22.38 ↓ 0.58 12.25 ↑ 5.95 36.10 ↑ 1.73

B. Cross-Harness Generalization Fixed backbone LLM: DeepSeek-V4-Flash
Agent Harness Setting          Overall    Astro.   Chem.      Earth                  Energy         Info.        Life        Mater.        Math         Neuro.         Phys.
                vanilla       16.60        28.35            9.39         15.32        24.60         9.27        13.57        20.09        12.64           4.04         28.70
  Claude Code
                +AutoSciRub 18.74 ↑ 2.14 28.15 ↓ 0.20    9.48 ↑ 0.09   20.30 ↑ 4.98 24.75 ↑ 0.15 11.06 ↑ 1.79 12.79 ↓ 0.78 21.30 ↑ 1.21 17.91 ↑ 5.27   7.67 ↑ 3.63   33.95 ↑ 5.25
                vanilla       17.25        24.26         8.90        22.39        18.93         9.29        15.70        19.07        15.08               5.11         33.71
  OpenClaw
                +AutoSciRub 20.36 ↑ 3.11 30.31 ↑ 6.05 12.59 ↑ 3.68 22.85 ↑ 0.45 25.24 ↑ 6.32 16.20 ↑ 6.90 17.18 ↑ 1.47 17.95 ↓ 1.13 23.12 ↑ 8.03       8.56 ↑ 3.45   29.62 ↓ 4.09
                vanilla       14.49        21.12         9.59        15.20        16.96        10.68         9.29        20.28        12.05               7.05         22.73
  OpenScience
                +AutoSciRub 18.09 ↑ 3.60 26.58 ↑ 5.46 12.04 ↑ 2.45 19.34 ↑ 4.14 22.94 ↑ 5.98 13.82 ↑ 3.14 17.53 ↑ 8.24 16.02 ↓ 4.26 17.45 ↑ 5.40       7.06 ↑ 0.01   28.11 ↑ 5.38


Table 1: Main results on ResearchClawBench. Panel A evaluates generalization across backbone LLMs under the fixed Codex
harness, while Panel B evaluates generalization across agent harnesses using the fixed DeepSeek-V4-Flash backbone. Vanilla
denotes the unmodified configuration, and +AutoSciRub denotes the same configuration augmented with our plugin layer.
Bold values indicate the better result within each paired comparison. Green and red arrows denote absolute improvements and
degradations, respectively.


Codex (OpenAI 2026a) as the agent harness and use GPT-                                   Code, 3.11 points for OpenClaw, and 3.60 points for Open-
5.4 (OpenAI 2026b), GLM-5.2 (Z.ai 2026), and MiniMax-                                    Science. The larger OpenClaw and OpenScience gains fur-
M3 (MiniMax 2026) as backbone models. In cross-harness                                   ther show that AutoSciRub remains effective across agent
evaluation, we fix DeepSeek-V4-Flash (DeepSeek-AI 2026)                                  systems with distinct workflows and baseline capabilities. At
as the backbone model and compare Claude Code (An-                                       the domain level, AutoSciRub improves 49 of 60 paired com-
thropic 2026), OpenClaw (OpenClaw Foundation 2026),                                      parisons, including consistent gains in chemistry, energy sci-
and OpenScience (Synthetic Sciences 2026). Following                                     ence, and neuroscience across all six configurations. Overall,
the benchmark-specific evaluation protocols, we use GPT-                                 the improvements across backbone models, agent harnesses,
5.1 (OpenAI 2025) to evaluate report quality.                                            and scientific domains demonstrate that AutoSciRub gener-
   For AstaBench, we evaluate three representative agent con-                            alizes well to heterogeneous scientific research agents.
figurations: Claude Code with DeepSeek-V4-Flash, Open-
Claw with DeepSeek-V4-Flash, and Codex with GPT-5.4-                                     Generalization to AstaBench. We further evaluate
mini. The generated artifacts are evaluated using MiniMax-                               whether these benefits transfer to a different task collection
M3 as the evaluator. Across both benchmarks, each resulting                              and evaluation protocol. As shown in Figure 3, AutoSciRub
submission is independently scored three times, and the mean                             substantially improves the mean scores of all three evaluated
score is reported. Additional implementation details, includ-                            agents on the fixed 20-task AstaBench End-to-End Discovery
ing agent configurations, prompts, and execution settings, are                           subset. It yields gains of 19.36 points for Claude Code, 12.61
provided in Appendix A.                                                                  points for Codex, and 18.38 points for OpenClaw, corre-
                                                                                         sponding to an average improvement of 16.78 points. Claude
4.2    Overall Performance                                                               Code and Codex also increase their successful-task counts
                                                                                         from 18/20 to 20/20. OpenClaw completes 19/20 tasks under
Results on ResearchClawBench. As shown in Table 1,                                       both settings while gaining 18.38 points, showing that Au-
AutoSciRub improves the overall ResearchClawBench score                                  toSciRub improves the quality of completed research outputs
in all six model–harness configurations. Under the fixed                                 in addition to task completion.
Codex harness, AutoSciRub yields gains of 2.38 points
for GPT-5.4, 1.87 points for GLM-5.2, and 1.99 points for
MiniMax-M3. These gains remain consistent across model                                   4.3      Ablation Study
families and baseline strengths. Among these configurations,                             Table 2 presents a cumulative stage-wise ablation on all 40
GLM-5.2 with AutoSciRub achieves the highest overall score                               ResearchClawBench tasks using OpenClaw with DeepSeek-
of 22.73. Together, the consistent gains across three backbone                           V4-Flash. Starting from the vanilla agent, Rubric Skeleton
LLMs indicate that the effectiveness of AutoSciRub is not                                Induction (Skel.) increases the score from 17.25 to 17.61.
model-specific.                                                                          This modest gain suggests that making the instruction’s im-
   The improvements are similarly preserved when varying                                 plicit scientific requirements explicit helps the agent identify
the agent harness. With DeepSeek-V4-Flash as the shared                                  what should be investigated, but offers limited guidance on
backbone, AutoSciRub yields gains of 2.14 points for Claude                              how these requirements should be carried out and verified.
                                                                                                                  Rubric Skeleton                               Executable Rubric                     0      10           20          30       40            50
                                 Specificity                                                                                                                                                          03
                                                                                                        r = 0.63                                        r = 0.55                            Life002                                             Score gain
                                                                                                                                                                                                                                                              Info.0
                                                    5                                                                                                                                               0                                                         Math 04
                                                                                                        ρ = 0.63                                        ρ = 0.59                          Earth003                                                                  0
                                                                                                     40 R 2 = 0.39                                                                              th                                              Score loss    Ener 03
                                                                                                                                                        R 2 = 0.31                        Ear 04                                                                   g
                                                                                                                                                                                                   .0                                                         Chemy002
                                                3                                                                                                                                       Chem 001                                                              Chem.003
                                                                                                                                                                                          Math 02
                                                                                                                                                                                             tr  o .0                                                         Chem.001
                                                                                                                                                                                         As 001
                                                                                                     30                                                                                          r.                                                           Mate .002
                                                                                                                                                                                        Mate .002




                                                                      Actionability
                                            1
Verifiability




                                                                                                                                                                                                                                                                   r.
                                                                                                                                                                                                                                                              Ener 002




                                                                                      Report score
 Evidence




                                                                                                                                                                                                 o
                                                                                                                                                                                        Neur y001                                                                  g
                                                                                                                                                                                                                                                              Earth y003
                                                                                                                                                                                          n e rg
                                                                                                                                                                                        E
                                                                                                                                                                                                 o.00
                                                                                                                                                                                                       1                                                      Phys 004
                                                                                                                                                                                         Astr .003                                                                 .0
                                                                                                                                                                                                 o                                                            Astr 03
                                                                                                     20                                                                                  Astr .002                                                                o
                                                                                                                                                                                           Info 01                                                            Math .004
                                                                                                                                                                                                                                                                    0
                                                                                                                                                                                            Life001                                                           Phys 04
                                                                                                                               slope = 9.94                              slope = 6.80                                                                              .0
                                                                                                                                                                                           Info.001                                                           Ener 04
                                                                                                                                                                                                                                                                   gy00
                                                                                                                                                                                                 o.0                                                          Life0     4
                                                                                                     10                                                                                 Neur .004                                                             Neur 02
                                                                                                                                                                                                 o
                                                                                                                                                                                        Neur .003                                                                  o
                                                                                                                                                                                                                                                              Phys .003
                                                                                                                                                                                           In  fo                                                                  .0
                          Scientific Core                                                                                                                                                             04                                                      Mate 02
                             Coverage                                                                                                                                                       Life001                                                                r.
                                                                                                                                                                                                    0                                                         Math 004
                Rubric Skeleton      Executable Rubric                                                0                                                                                   Earth 01                                                                  002
                                                                                                          1        2      3     4      5               1        2      3     4      5             .0                                                          M
                                                                                                                                                                                          Phys          50   40           30          20       10            0 ater.003
                                                                                                              Scientific Core Coverage                     Scientific Core Coverage
                     (a) Rubric quality
                                                                                                     (b) Scientific core coverage vs. report score.                                                          (c) Task-level score changes.

Figure 4: Rubric quality and its downstream effects. (a) Mean quality profiles of rubric skeletons and executable rubrics across
40 tasks. (b) Association between scientific core coverage and downstream report score. (c) Task-level report-score changes
from rubric skeletons to executable rubrics.


                     Input: Monolayer epitaxial graphene samples and mid-infrared pump excitation parameters                                                                    Setting                           Skel.        Grd.   Rev.     Score↑        ∆Base
                     (wavelength: 5 μm, intensity, polarization angle). Output: Direct, energy- and momentum-resolved
                     observation of Floquet-Bloch states (replica bands of the Dirac cone) via time-resolved and
                TASK angle-resolved photoemission spectroscopy (tr-ARPES).
                     Scientific Goal: To experimentally confirm the existence of Floquet-Bloch states in a
                                                                                                                                                                                Base                               ✗            ✗          ✗   17.25           –
                     paradigmatic 2D material and elucidate the underlying scattering mechanism involving photon-
                     dressed Volkov final states.
                                                                                                                                                                                w/ Skeleton                        ✓            ✗          ✗   17.61         +0.36
                                                                                                                                                                                w/ Grounded Rubric                 ✓            ✓          ✗   18.31         +1.06
                           Executable Rubric                        2/5                                              Golden Checklist                  1/3
                   goal: "Identify and characterize Floquet-Bloch
                   replica bands, including gap measurements at avoided                                       content: "Energy-momentum map from tr-                            Full                               ✓            ✓          ✓   20.36         +3.11
                   crossings.",                                                                               ARPES showing the main Dirac cone and a
                   experiments: "Extract EDCs at Γ point and at                                               clear replica band induced by the 5 μm pump
                   avoided-crossing momenta",                                                                 excitation."
                             "Fit multi-peak Voigt profiles to EDCs", "..."                                   keywords
                   required_artifacts: { “type”: “figure”, “must_show”:                                       • Clear visualization of the main Dirac cone.                  Table 2: Stage-wise cumulative ablation on ResearchClaw-
                   “EDC fits revealing n = -1, 0, and +1 sidebands”,                                          • Clear visualization of a replica band shifted
                   “description_requirement”: “Demonstrate sidebands                                            from the main cone                                           Bench. Skel. denotes Rubric Skeleton Induction; Grd. adds
                   with peak separation matching ħω ≈ 248                                                     • Axes labeled with energy (eV) and
                   meV ...” },{"..."}
                                                                                                                momentum (Å ⁻¹ ).                                            Scientific Literature Grounding, Task-Data Exploration, and
                   metrics: "ħω from peak separation (~248 meV)", "..."
                                                                                                              • Data acquired at a time delay of ~1 ps after
                   baselines: "Compare measured gap 2Δ with Floquet
                   theory", "..."
                                                                                                                pump excitation                                              Criterion Synthesis; and Rev. adds Rubric-Guided Iterative
                   data_sources: “data/raw_trARPES_data.h5”, "..."
                                                                                                                                                                             Revision. Scores are averaged over the same 40 tasks, and
                   Report                                                                                 Target Paper
                                                                                                                                                                             ∆Base denotes the improvement over the base setting.


                                                                                                                                                                             4.4        Analysis
                                                                                                                                                                             Rubric Induction Produces Executable Guidance.
Figure 5: Comparison between an AutoSciRub executable                                                                                                                        Open-ended research instructions rarely specify the experi-
rubric and the benchmark-provided golden checklist.                                                                                                                          ments, evidence, and success conditions needed to complete
                                                                                                                                                                             a task. Figure 5 shows how AutoSciRub addresses this un-
                                                                                                                                                                             derspecification. While the benchmark checklist mainly de-
   Adding the grounded-rubric stage (Grd.) further raises                                                                                                                    scribes what should appear in the final report, the executable
the score to 18.31, corresponding to a gain of 1.06 points                                                                                                                   rubric also specifies how the required evidence should be
over the base and an additional 0.70 points over skeleton                                                                                                                    produced and verified through concrete experiments, arti-
induction alone. By grounding the induced goals in scientific                                                                                                                facts, metrics, baselines, and data sources. It therefore serves
literature, examining the task-visible data, and synthesizing                                                                                                                as an execution-time specification rather than only a post-hoc
feasible experiments and evidence requirements, this stage                                                                                                                   evaluation instrument.
turns a high-level rubric skeleton into more concrete and                                                                                                                       For each of the 40 ResearchClawBench tasks, we compare
verifiable criteria.                                                                                                                                                         the instruction-derived rubric skeleton with the task-specific
   Rubric-Guided Iterative Revision (Rev.) achieves the best                                                                                                                 executable rubric produced after literature grounding, task-
score of 20.36, improving by 3.11 over the base and 2.05                                                                                                                     data exploration, and criterion synthesis. As shown in Fig-
over the grounded-rubric setting. This largest incremental                                                                                                                   ure 4a, the mean score across the four evaluated dimensions
gain indicates that the rubric is most effective when it is                                                                                                                  increases from 2.20 to 3.84. The largest improvement occurs
used not only to guide execution, but also to identify unmet                                                                                                                 in specificity, which increases from 1.65 to 4.40 (+2.75),
criteria and support targeted revision of the report and its                                                                                                                 followed by evidence verifiability from 1.78 to 4.08 (+2.30)
supporting artifacts. Overall, the monotonic gains show that                                                                                                                 and actionability from 2.00 to 3.83 (+1.83). These improve-
rubric skeleton induction, grounding, and iterative revision                                                                                                                 ments show that rubric induction effectively operationalizes
play complementary roles in turning underspecified research                                                                                                                  broad scientific goals into concrete, actionable, and verifiable
instructions into better-supported research outputs.                                                                                                                         requirements for research execution and verification.
                                                                                                      25                                  11
                  30       Stopped tasks               Overall     Stop@R2          Held after stop                                                                           10                                                Math                                                       +4.12
                           Verifier-passed tasks       Stop@R1     Stop@R3          Stopping point
                                                                                                      24                                  10
                                                                                                                                                                                     9   9             Improved tasks (n=36)    Earth                                                 +3.73
                                                                                                      23                                   9
                  25                                   21.92
                                                                                                      22                                                                                               Declined tasks (n=4)     Info.                                             +3.32
                                                                                                                                           8




                                                                                                                        Number of tasks
Number of tasks




                  20
                            20.47                    23/23         20.08              20.36           21                                   7                                                                                     Life                                +2.00




                                                                                                           Mean score
                                                     19.47                             19.23          20                                   6                                                                                   Chem.                                 +1.93
                  15        18.31                                                                     19                                                                                                                                                             +1.92
                                                       18.04                                                                               5                                                                                   Astro.
                             17.63                                    17.71                           18
                                                                                                                                           4                                                                                   Neuro.                          +1.69
                  10                                                 17.34                            17
                                                                                       1/6                                                 3                                                                                   Energy                        +1.43
                                                                                                      16                                                     2                               2     2     2
                   5                                                11/11
                                                                                                      15                                   2                                                                                   Mater.                +0.48                    Improved domains
                                                    15.12                                                                                           1                 1                                        1        1
                                                                                     1 passed
                                                                                                      14                                   1                                                                                    Phys     -0.11                                Declined domains
                           14.16
                   0                                                                                                                       0
                           Initial                 Revision 1    Revision 2       Revision 3                                                   -3       -2       -1       0        +1 +2 +3 +4 +5 +6 +7 +14 +15                     -1           0     +1       +2           +3       +4           +5

                           (a) Overall refinement dynamics.                                                             (b) Distribution of task-level score changes.                                                               (c) Domain-level mean improvement.
Figure 6: Analysis of rubric-guided refinement. (a) Overall score and task stopping behavior across refinement steps. (b)
Distribution of score changes from the initial reports to the final reports. (c) Mean score improvement across scientific domains.

Revision Round
                                          Rubric-Free Self-Refinement                                 Rubric-Guided Revision                                                                     cumulative improvement of 2.05, compared with only 0.77
                                                   Score                      ∆                       Score                                                       ∆                              without rubrics. Thus, rubric-guided revision achieves ap-
                       1                           18.80                    +0.49                      19.47                                                     +1.16                           proximately 2.7 times the cumulative improvement of rubric-
                       2                           18.52                    +0.21                      20.08                                                     +1.77                           free self-refinement. This result shows that the gain does not
                       3                           19.08                    +0.77                      20.36                                                     +2.05
                                                                                                                                                                                                 come from repeated rewriting alone: explicit criteria identify
                                                                                                                                                                                                 concrete deficiencies and direct the agent toward unsatisfied
Table 3: Comparison of rubric-free self-refinement and
                                                                                                                                                                                                 scientific requirements, whereas generic self-refinement pro-
rubric-guided revision across three revision rounds on all 40
                                                                                                                                                                                                 duces less stable improvements.
ResearchClawBench tasks. ∆ values denote score changes
                                                                                                                                                                                                    Figure 6a further shows how the guided improvement ac-
relative to the shared unrevised baseline score of 18.31.
                                                                                                                                                                                                 cumulates across revision rounds. The first revision raises
                                                                                                                                                                                                 the average score from 18.31 to 19.47, contributing an im-
                                                                                                                                                                                                 provement of 1.16. The second and third rounds add im-
Rubric Induction Improves Operationalization but Not
                                                                                                                                                                                                 provements of 0.61 and 0.28, respectively. This decrease in
Scientific Framing. Although rubric induction substan-
                                                                                                                                                                                                 aggregate gain mainly results from adaptive stopping rather
tially improves specificity, actionability, and evidence verifi-
                                                                                                                                                                                                 than ineffective later revisions. After the first round, 23 tasks
ability, scientific core coverage slightly decreases from 3.35
                                                                                                                                                                                                 have already passed the verifier, leaving only 17 tasks for
to 3.07. This contrast suggests that AutoSciRub is more ef-                                                                                                                                      a second revision and six for a third. For these remaining
fective at translating an identified scientific direction into                                                                                                                                   tasks, the average per-round improvements are still 1.43 and
concrete and verifiable requirements than at revising the un-                                                                                                                                    1.89, respectively. Overall, 35 of the 40 tasks pass within
derlying framing of the research problem.                                                                                                                                                        three revisions. These results suggest that one revision offers
   As shown in Figure 4b, scientific core coverage remains                                                                                                                                       a strong default cost/performance trade-off, while additional
positively associated with report quality for both rubric skele-                                                                                                                                 rounds provide targeted improvements for harder tasks.
tons and executable rubrics. Figure 4c further shows that                                                                                                                                           The task- and domain-level results in Figures 6b and 6c
executable rubrics yield a mean report-score gain of 0.70                                                                                                                                        show that the overall gain is broadly distributed rather than
across all 40 tasks, with improvements observed on 34 tasks.                                                                                                                                     dominated by a few high-improvement cases. Specifically, 36
These results suggest that AutoSciRub is effective at trans-                                                                                                                                     of the 40 reports improve over their initial versions, and pos-
lating an identified scientific core into concrete experiments                                                                                                                                   itive average gains are observed in most scientific domains.
and verifiable evidence requirements, but is less effective at                                                                                                                                   Mathematics, earth science, and information science achieve
identifying that core when it is missing from the initial rubric                                                                                                                                 the largest average improvements of 4.12, 3.73, and 3.32, re-
skeleton. In such cases, grounding and synthesis may elabo-                                                                                                                                      spectively. These results demonstrate that the improvement
rate secondary or off-target analyses rather than correct the                                                                                                                                    of rubric-guided revision is consistent across tasks and do-
research direction. Higher-level scientific judgment therefore                                                                                                                                   mains, rather than being driven by a single high-scoring case.
remains largely dependent on the backbone model.
Rubric-Guided Revision Outperforms Generic Self-                                                                                                                                                                                   5       Conclusion
Refinement. We analyze whether the improvement from                                                                                                                                              We introduced AutoSciRub, a general framework that au-
iterative revision is caused by rubric guidance or merely by                                                                                                                                     tomatically induces task-specific scientific rubrics and uses
giving the agent additional opportunities to rewrite its re-                                                                                                                                     them as execution-time guidance for autonomous research
port. Starting from the same checkpoint-0 reports, we com-                                                                                                                                       agents. AutoSciRub decomposes underspecified research in-
pare rubric-guided revision with a rubric-free self-refinement                                                                                                                                   structions into scientific goals, grounds evaluation criteria
baseline, which asks the agent to inspect and improve its pre-                                                                                                                                   in external evidence, and guides criterion-level verification
vious output without criterion-level feedback. As shown in                                                                                                                                       and revision of generated research artifacts. Experiments on
Table 3, rubric-free refinement increases the average score                                                                                                                                      ResearchClawBench and AstaBench show that AutoSciRub
from 18.31 to only 19.08 after three rounds and even causes                                                                                                                                      consistently improves different backbone models and agent
a regression at checkpoint 2. In contrast, rubric-guided revi-                                                                                                                                   harnesses, demonstrating its effectiveness and generalizabil-
sion improves the score monotonically to 20.36, yielding a                                                                                                                                       ity as a plugin layer for autonomous scientific research.
                        References                                 Garikaparthi, A.; Patwardhan, M.; and Cohan, A. 2026. Re-
Anthropic. 2026.       Claude Code.       https://github.com/      searchGym: Evaluating Language Model Agents on Real-
anthropics/claude-code.                                            World AI Research. CoRR, abs/2602.15112.
Bragg, J.; D’Arcy, M.; Balepur, N.; Bareket, D.; Dalvi,            Ghareeb, A. E.; Chang, B.; Mitchener, L.; Yiu, A.;
B.; et al. 2025. AstaBench: Rigorous Benchmarking                  Szostkiewicz, C. J.; et al. 2026. A Multi-Agent System for
of AI Agents with a Scientific Research Suite. CoRR,               Automating Scientific Discovery. Nature, 655: 497–505.
abs/2510.21652.                                                    Gottweis, J.; Weng, W.-H.; Daryin, A.; Tu, T.; Sirkovic,
Chan, J. S.; Chowdhury, N.; Jaffe, O.; Aung, J.; Sherburn,         P.; et al. 2026. Accelerating Scientific Discovery with Co-
D.; et al. 2025. MLE-bench: Evaluating Machine Learning            Scientist. Nature, 655: 487–496.
Agents on Machine Learning Engineering. In The Thir-               Gou, Z.; Shao, Z.; Gong, Y.; Shen, Y.; Yang, Y.; Duan, N.; and
teenth International Conference on Learning Representa-            Chen, W. 2024. CRITIC: Large Language Models Can Self-
tions, ICLR 2025, Singapore, April 24-28, 2025. OpenRe-            Correct with Tool-Interactive Critiquing. In The Twelfth In-
view.net.                                                          ternational Conference on Learning Representations, ICLR
Chen, H.; Han, Z.; Yan, Y.; Zhu, Q.; Sun, M.; and Che,             2024, Vienna, Austria, May 7-11, 2024. OpenReview.net.
W. 2026a. From Holistic Evaluation to Structured Crite-            Hashemi, H.; Eisner, J.; Rosset, C.; Durme, B. V.; and Kedzie,
ria: Rubrics Across the Evolving LLM Landscape. CoRR,              C. 2024. LLM-Rubric: A Multidimensional, Calibrated Ap-
abs/2606.08625.                                                    proach to Automated Evaluation of Natural Language Texts.
Chen, Y.; Maiga, A.; Rahmani, H. A.; and Yilmaz, E. 2026b.         In Ku, L.; Martins, A.; and Srikumar, V., eds., Proceedings
Automated Rubrics for Reliable Evaluation of Medical Dia-          of the 62nd Annual Meeting of the Association for Compu-
logue Systems. arXiv preprint arXiv:2601.15161.                    tational Linguistics (Volume 1: Long Papers), ACL 2024,
Chen, Y.; Xiao, B.; Zhao, Y.; Xia, H.; Xu, B.; Fang, J.; Li, Y.;   Bangkok, Thailand, August 11-16, 2024, 13806–13834. As-
Zheng, Y.; Wang, X.; Xue, Z.; Zhang, L.; Li, H.; and Zhang,        sociation for Computational Linguistics.
N. 2026c. LightMem-Ego: Your AI Memory for Everyday                Hong, H.; Li, Y.; Chen, J.; Huy, L. G.; Ananiadou, S.; Kim,
Life. CoRR, abs/2607.11487.                                        J.-j.; and Lin, C. 2026. Can LLMs Write Reliable Rubrics?
Chen, Z.; Chen, S.; Ning, Y.; Zhang, Q.; Wang, B.; et al.          A Meta-Evaluation for Experiment Reproduction. arXiv
2025. ScienceAgentBench: Toward Rigorous Assessment of             preprint arXiv:2607.12835.
Language Agents for Data-Driven Scientific Discovery. In           Ifargan, T.; Hafner, L.; Kern, M.; Alcalay, O.; and Kishony,
The Thirteenth International Conference on Learning Repre-         R. 2024. Autonomous LLM-driven research from data to
sentations, ICLR 2025, Singapore, April 24-28, 2025. Open-         human-verifiable research papers. CoRR, abs/2404.17605.
Review.net.
                                                                   LeVine, W.; Evers, B.; Saltwick, S.; and Venkatesh, A.
DeepSeek-AI. 2026.         DeepSeek-V4: Towards Highly             2026. RubricRefine: Improving Tool-Use Agent Reliabil-
Efficient Million-Token Context Intelligence.           CoRR,      ity with Training-Free Pre-Execution Refinement. CoRR,
abs/2606.19348.                                                    abs/2605.09730.
Dhole, K. D.; and Agichtein, E. 2026. RubricRAG: To-               Li, D.; Liu, Z.; Wang, J.; Huang, J.; Li, F.; Jia, B.; Hu, B.;
wards Interpretable and Reliable LLM Evaluation via Do-            and Zhang, M. 2026a. LycheeMemory V2: Efficient Long-
main Knowledge Retrieval for Rubric Generation. In Moffat,         Term Memory for LLM Agents via Semantic Segment-Level
A.; Scholer, F.; Bast, H.; Najork, M.; and Zhang, M., eds.,        Consolidation. arXiv:2608.12990.
Proceedings of the 49th International ACM SIGIR Confer-
ence on Research and Development in Information Retrieval,         Li, R.; Du, M.; Xu, B.; Zhu, C.; Wang, X.; et al. 2026b.
SIGIR 2026, Melbourne, VIC, Australia, July 20–24, 2026,           DeepResearch Bench II: Diagnosing Deep Research Agents
3681–3687. ACM.                                                    via Rubrics from Expert Report. CoRR, abs/2601.08536.
Ding, L. 2026. AdaRubric: Task-Adaptive Rubrics for LLM            Liu, J.; Qiu, S.; Li, M.; Li, B.; Ji, H.; et al. 2026. AutoRe-
Agent Evaluation. CoRR, abs/2603.21362.                            searchClaw: Self-Reinforcing Autonomous Research with
                                                                   Human-AI Collaboration. CoRR, abs/2605.20025.
Fan, Z.; Wang, W.; Wu, X.; and Zhang, D. 2024. SedarEval:
Automated Evaluation using Self-Adaptive Rubrics. In               Lu, C.; Lu, C.; Lange, R. T.; Foerster, J. N.; Clune, J.; et al.
Al-Onaizan, Y.; Bansal, M.; and Chen, Y., eds., Findings           2024. The AI Scientist: Towards Fully Automated Open-
of the Association for Computational Linguistics: EMNLP            Ended Scientific Discovery. CoRR, abs/2408.06292.
2024, Miami, Florida, USA, November 12-16, 2024, volume            Lu, Z.; Li, D.; Shi, Y.; Wang, B.; Wang, L.; and Hu, B. 2026.
EMNLP 2024 of Findings of ACL, 16916–16930. Associa-               Structured Episodic Event Memory. In Liakata, M.; Mor-
tion for Computational Linguistics.                                eira, V. P.; Zhang, J.; and Jurgens, D., eds., Proceedings of
Gao, S.; Fang, A.; and Zitnik, M. 2026. AutoScientists:            the 64th Annual Meeting of the Association for Computa-
Self-Organizing Agent Teams for Long-Running Scientific            tional Linguistics (Volume 1: Long Papers), ACL 2026, San
Experimentation. CoRR, abs/2605.28655.                             Diego, California, United States, July 2-7, 2026, 6125–6141.
Gao, S.; Su, Y.; Sui, P.; Ginder, C.; and Zitnik, M. 2026.         Association for Computational Linguistics.
Qworld: Question-Specific Evaluation Criteria for LLMs.            Luo, Y.; Yu, Z.; Wang, X.; Zhu, Y.; Zhang, N.; Wei, L.;
CoRR, abs/2603.23522.                                              Du, L.; Zheng, D.; and Chen, H. 2026. What Makes AI
Research Replicable? Executable Knowledge Graphs as Sci-          EACL 2026, Rabat, Morocco, March 24-29, 2026, Findings
entific Knowledge Representations. In Liakata, M.; Moreira,       of ACL, 6371–6389. Association for Computational Linguis-
V. P.; Zhang, J.; and Jurgens, D., eds., Proceedings of the       tics.
64th Annual Meeting of the Association for Computational          Starace, G.; Jaffe, O.; Sherburn, D.; Aung, J.; Chan, J. S.; et al.
Linguistics (Volume 2: Short Papers), ACL 2026, San Diego,        2025. PaperBench: Evaluating AI’s Ability to Replicate AI
California, United States, July 2-7, 2026, 841–861. Associ-       Research. In Singh, A.; Fazel, M.; Hsu, D.; Lacoste-Julien,
ation for Computational Linguistics.                              S.; Berkenkamp, F.; Maharaj, T.; Wagstaff, K.; and Zhu,
Lyu, Y.; Zhang, X.; Yi, X.; Zhao, Y.; Guo, S.; et al. 2026.       J., eds., Forty-second International Conference on Machine
EvoScientist: Towards Multi-Agent Evolving AI Scientists          Learning, ICML 2025, Vancouver, BC, Canada, July 13-
for End-to-End Scientific Discovery. CoRR, abs/2603.08127.        19, 2025, volume 267 of Proceedings of Machine Learning
Madaan, A.; Tandon, N.; Gupta, P.; Hallinan, S.; Gao, L.;         Research. PMLR / OpenReview.net.
Wiegreffe, S.; Alon, U.; Dziri, N.; Prabhumoye, S.; Yang,         Synthetic Sciences. 2026. OpenScience: The Open-Source
Y.; Gupta, S.; Majumder, B. P.; Hermann, K.; Welleck, S.;         AI Workbench for Scientific Research. https://github.com/
Yazdanbakhsh, A.; and Clark, P. 2023. Self-Refine: Iterative      synthetic-sciences/openscience.
Refinement with Self-Feedback. In Oh, A.; Naumann, T.;            Tang, J.; Xia, L.; Li, Z.; and Huang, C. 2025. AI-Researcher:
Globerson, A.; Saenko, K.; Hardt, M.; and Levine, S., eds.,       Autonomous Scientific Innovation. CoRR, abs/2505.18705.
Advances in Neural Information Processing Systems 36: An-
nual Conference on Neural Information Processing Systems          Wan, Y.; Fang, T.; Li, Z.; Huo, Y.; Wang, W.; Mi, H.; Yu,
2023, NeurIPS 2023, New Orleans, LA, USA, December 10             D.; and Lyu, M. R. 2026. Inference-Time Scaling of Verifi-
- 16, 2023.                                                       cation: Self-Evolving Deep Research Agents via Test-Time
                                                                  Rubric-Guided Verification. In Liakata, M.; Moreira, V. P.;
MiniMax. 2026. MiniMax M3: Frontier Coding, 1M Con-               Zhang, J.; and Jurgens, D., eds., Findings of the Associa-
text, Native Multimodality—All in One Model. https:               tion for Computational Linguistics, ACL 2026, San Diego,
//www.minimax.io/blog/minimax-m3. Accessed: 2026-07-              California, United States, July 2-7, 2026, 24822–24835. As-
24.                                                               sociation for Computational Linguistics.
Mitchener, L.; Yiu, A.; Chang, B.; Bourdenx, M.; Nadolski,        Wang, Z.; Bai, F.; Luo, Z.; Su, J.; Sun, K.; Yu, X.; Liu, J.;
T.; et al. 2025. Kosmos: An AI Scientist for Autonomous           Zhou, K.; Cardie, C.; Dredze, M.; Xing, E. P.; and Hu, Z.
Discovery. CoRR, abs/2511.02824.                                  2026. FIRE-Bench: Evaluating Agents on the Rediscovery
OpenAI. 2025. GPT-5.1: A Smarter, More Conversational             of Scientific Insights. CoRR, abs/2602.02905.
ChatGPT. https://openai.com/index/gpt-5-1/. Accessed:             Wang, Z.; and Blanco, E. 2026. Generating and Refining
2026-07-24.                                                       Dynamic Evaluation Rubrics for LLM-as-a-Judge. CoRR,
OpenAI. 2026a. Codex. https://github.com/openai/codex.            abs/2605.30568.
OpenAI. 2026b. Introducing GPT-5.4. https://openai.com/           Wei, J.; Yang, Y.; Zhang, X.; Chen, Y.; Zhuang, X.; Gao,
index/introducing-gpt-5-4/. Accessed: 2026-07-24.                 Z.; Zhou, D.; Wang, G.; Gao, Z.; Cao, J.; Qiu, Z.; He, X.;
OpenClaw Foundation. 2026. OpenClaw. https://github.              Zhang, Q.; You, C.; Zheng, S.; Ding, N.; Ouyang, W.; Dong,
com/openclaw/openclaw.                                            N.; Cheng, Y.; Sun, S.; Bai, L.; and Zhou, B. 2025. From AI
Schmidgall, S.; Su, Y.; Wang, Z.; Sun, X.; Wu, J.; et al. 2025.   for Science to Agentic Science: A Survey on Autonomous
Agent Laboratory: Using LLM Agents as Research Assis-             Scientific Discovery. CoRR, abs/2508.14111.
tants. In Christodoulopoulos, C.; Chakraborty, T.; Rose, C.;      Xu, B.; Chen, Y.; Fang, J.; Zhong, R.; Yao, Y.; Zhu, Y.; Du,
and Peng, V., eds., Findings of the Association for Computa-      L.; and Deng, S. 2026a. StructMem: Structured Memory
tional Linguistics: EMNLP 2025, Suzhou, China, November           for Long-Horizon Behavior in LLMs. In Liakata, M.; Mor-
4-9, 2025, 5977–6043. Association for Computational Lin-          eira, V. P.; Zhang, J.; and Jurgens, D., eds., Proceedings of
guistics.                                                         the 64th Annual Meeting of the Association for Computa-
Sharma, M.; Zhang, C. B. C.; Bandi, C.; Wang, C.; Aich,           tional Linguistics (Volume 2: Short Papers), ACL 2026, San
A.; Nghiem, H.; Rabbani, T.; Htet, Y.; Jang, B.; Basu, S.;        Diego, California, United States, July 2-7, 2026, 122–146.
Balwani, A.; Peskoff, D.; Ayestaran, M.; Hendryx, S. M.;          Association for Computational Linguistics.
Kenstler, B.; and Liu, B. 2025. ResearchRubrics: A Bench-         Xu, B.; Xue, Z.; Chen, D.; Fu, C.; Wu, C.; Huang, C.;
mark of Prompts and Rubrics For Evaluating Deep Research          Jiang, C.; Fang, J.; Deng, X.; Chen, Y.; Yao, Y.; Wang, X.;
Agents. CoRR, abs/2511.07685.                                     Shang, J.; Yu, G.; and Zhang, N. 2026b. TokenPilot: Cache-
Shen, W. F.; Qiu, X.; Whitehouse, C.; Alazraki, L.; Goel,         Efficient Context Management for LLM Agents. CoRR,
S.; et al. 2026. Rethinking Rubric Generation for Improving       abs/2606.17016.
LLM Judge and Reward Modeling for Open-ended Tasks.               Xu, W.; Li, S.; Ye, T.; Cao, Q.; Chen, Y.; et al. 2026c.
CoRR, abs/2602.05125.                                             ResearchClawBench: A Benchmark for End-to-End Au-
Siro, C.; Aliannejadi, P.; and Aliannejadi, M. 2026. Learn-       tonomous Scientific Research. CoRR, abs/2606.07591.
ing to Judge: LLMs Designing and Applying Evaluation              Yamada, Y.; Lange, R. T.; Lu, C.; Hu, S.; Lu, C.; et al. 2025.
Rubrics. In Demberg, V.; Inui, K.; and Marquez, L., eds.,         The AI Scientist-v2: Workshop-Level Automated Scientific
Findings of the Association for Computational Linguistics:        Discovery via Agentic Tree Search. CoRR, abs/2504.08066.
Ye, H.; Lin, H.; Tang, J.; Luo, Y.; Yang, C.; Su, C.; Thapa, R.;   these criteria. The resulting task score ranges from 0 to 100,
Yang, R.; Liu, R.; Li, Z.; Gao, C.; Ding, D.; He, G.; Zhang,       with a score around 50 intended to represent approximately
M.; Sun, L.; Wang, W.; Zhong, Y.; Shen, Z.; He, D.; Ma, J.;        target-paper-level re-discovery under the benchmark proto-
Ermon, S.; Li, T.; Chu, X.; Wang, J. Z.; and Xu, Y. 2026.          col.
Evaluation-driven Scaling for Scientific Discovery. CoRR,             For each configuration, the overall score is the arithmetic
abs/2604.19341.                                                    mean over all 40 tasks. Each domain score is the arithmetic
Yehudai, A.; Eden, L.; Li, A.; Uziel, G.; Zhao, Y.; Bar-           mean over the four tasks belonging to that domain. All re-
Haim, R.; Cohan, A.; and Shmueli-Scheuer, M. 2026. A               ported improvements are absolute differences between paired
Survey on Evaluation of LLM-based Agents. In Liakata,              vanilla and +AutoSciRub scores on the same task set.
M.; Moreira, V. P.; Zhang, J.; and Jurgens, D., eds., Findings     AstaBench End-to-End Discovery. We additionally eval-
of the Association for Computational Linguistics, ACL 2026,        uate AutoSciRub on a fixed subset of 20 tasks from the Easy
San Diego, California, United States, July 2-7, 2026, 26690–       split of the AstaBench End-to-End Discovery benchmark.
26714. Association for Computational Linguistics.                  The subset is sampled once from the original 40-task test
Yu, J.; Xu, Z.; Wang, J.; and Yang, Y. 2026. Think-with-           set using random seed 20260707. The sampling procedure
Rubrics: From External Evaluator to Internal Reasoning             does not preserve the order of the source dataset; instead, the
Guidance. CoRR, abs/2605.07461.                                    sampled order is retained as the execution order. The same
Z.ai. 2026. GLM-5.2: Built for Long-Horizon Tasks. https:          fixed subset and execution order are used for all evaluated
//z.ai/blog/glm-5.2. Accessed: 2026-07-24.                         configurations. Table 4 lists the exact task identifiers and task
                                                                   names.
Zheng, J.; Zhang, J.; Luo, Y.; Mao, Y.; Gao, Y.; Du, L.;
                                                                      Each AstaBench task requires an agent to complete an
Chen, H.; and Zhang, N. 2026. Can We Predict Before Exe-
                                                                   end-to-end research cycle involving experimental implemen-
cuting Machine Learning Agents? In Liakata, M.; Moreira,
                                                                   tation, execution, result analysis, and technical report gener-
V. P.; Zhang, J.; and Jurgens, D., eds., Proceedings of the
                                                                   ation. We use the official task-specific rubrics and LLM-as-
64th Annual Meeting of the Association for Computational
                                                                   judge evaluation pipeline, with MiniMax-M3 serving as the
Linguistics (Volume 1: Long Papers), ACL 2026, San Diego,
                                                                   evaluator.
California, United States, July 2-7, 2026, 3941–3974. Asso-
                                                                      For every rubric criterion, the evaluator independently ex-
ciation for Computational Linguistics.
                                                                   amines three output facets: the generated report, the gen-
Zhu, M.; Wei, C.; Xu, J.; Cheng, Y.; Chen, Z.; and He, J.          erated code, and the supporting artifacts, including datasets,
2026. DEEPRUBRIC: Evidence-Tree Rubric Supervision for             execution logs, figures, and model outputs. Each facet is clas-
Efficient Reinforcement Learning of Deep Research Agents.          sified as meets criterion, fails criterion, or no evidence either
CoRR, abs/2606.17029.                                              way. The facet-level assessments are then combined into a bi-
                                                                   nary verdict for the corresponding criterion. The official task
                                                                   score is the arithmetic mean of the binary criterion verdicts,
         A    Additional Experimental and                          multiplied by 100 for presentation.
                Methodological Details                                In addition to the mean evaluation score, we report the
A.1    Benchmark and Evaluation Details                            number of successfully completed tasks. A task is consid-
                                                                   ered successfully completed when the agent run terminates
ResearchClawBench. ResearchClawBench contains 40                   without an execution-level failure and produces a valid sub-
end-to-end scientific research tasks, with four tasks from each    mission that can be processed and scored by the official
of ten domains: astronomy, chemistry, earth science, energy        evaluator.
science, information science, life science, materials science,
mathematics, neuroscience, and physics. Each task is con-          Models and agent harnesses. We evaluate generalization
structed from a published target paper with a clearly defined      along two complementary axes on ResearchClawBench. In
scientific question and accessible raw data. The evaluated         cross-model evaluation, we hold the Codex agent harness
agent is provided with a task instruction, related literature,     fixed and vary the backbone LLM among GPT-5.4, GLM-
raw data, and a workspace in which it can inspect files, im-       5.2, and MiniMax-M3. In cross-harness evaluation, we hold
plement analyses, execute experiments, generate figures, and       the DeepSeek-V4-Flash backbone fixed and vary the sur-
write a final scientific report. The hidden target paper and       rounding agent implementation among Claude Code, Open-
its official evaluation rubric are not accessible to the agent     Claw, and OpenScience.
during rubric induction, research execution, verification, or         For AstaBench, we evaluate three representative configu-
revision.                                                          rations: Claude Code with DeepSeek-V4-Flash, OpenClaw
    We use the official ResearchClawBench evaluator with-          with DeepSeek-V4-Flash, and Codex with GPT-5.4-mini.
out modifying its scoring protocol. Each benchmark rubric          The complete configurations and corresponding benchmark
consists of weighted criteria associated with concrete scien-      evaluators are summarized in Table 5.
tific artifacts in the hidden target paper. The rubric contains       For every paired comparison, the vanilla setting denotes
both textual criteria, which assess scientific claims, meth-       the original agent without AutoSciRub. The +AutoSciRub
ods, quantitative results, and explanations, and image crite-      setting uses the same backbone model, agent harness, task
ria, which assess figure-level evidence. GPT-5.1 is used to        instruction, task-visible data, workspace, and available tools,
evaluate the final report and its supporting artifacts against     while additionally performing rubric induction, criterion-
    Order    Task ID                          Task name
       1     idea-226-simplified              simple-knowledge-enhanced-vqa
       2     idea-206-simplified              selective-entity-quantization
       3     idea-131-simplified              simple-semantic-backdoor-defense
       4     idea-21-simplified               text-to-code-prompt-retrieval
       5     idea-78-simplified               simple-bias-detection-worldmodel
       6     idea-337-simplified              medical-verbalization-calibration
       7     idea-17-simplified               topic-focused-memory-summarization
       8     idea-86-simplified               simple-language-skill-transfer
       9     idea-259-simplified              simple-relevance-metrics
      10     idea-174-simplified              simple-position-aware-prompts
      11     idea-5-simplified                simple-entity-debate
      12     idea-159-simplified              confidence-based-contamination-detection
      13     idea-304-simplified              dual-task-adversarial-robustness
      14     idea-192-simplified              simple-fact-unlearning
      15     idea-147-simplified              mini-socratic-code-generation
      16     idea-301-simplified              simplified-task-learning-transfer
      17     idea-134-simplified              simple-cross-lingual-backdoor
      18     idea-278-simplified              visual-entity-knowledge-test
      19     idea-68-simplified               evolutionary-prompt-optimization
      20     idea-141-simplified              biobert-pet-ner

Table 4: The fixed 20-task subset used for AstaBench evaluation, listed in the retained execution order. The tasks were sampled
from the original 40-task test set using random seed 20260707.

 Benchmark                    Setting                     Agent harness                  Backbone LLM                       Evaluator
 ResearchClawBench            Cross-model                 Codex                          GPT-5.4                            GPT-5.1
 ResearchClawBench            Cross-model                 Codex                          GLM-5.2                            GPT-5.1
 ResearchClawBench            Cross-model                 Codex                          MiniMax-M3                         GPT-5.1
 ResearchClawBench            Cross-harness               Claude Code                    DeepSeek-V4-Flash                  GPT-5.1
 ResearchClawBench            Cross-harness               OpenClaw                       DeepSeek-V4-Flash                  GPT-5.1
 ResearchClawBench            Cross-harness               OpenScience                    DeepSeek-V4-Flash                  GPT-5.1
 AstaBench                    Transfer                    Claude Code                    DeepSeek-V4-Flash                  MiniMax-M3
 AstaBench                    Transfer                    OpenClaw                       DeepSeek-V4-Flash                  MiniMax-M3
 AstaBench                    Transfer                    Codex                          GPT-5.4-mini                       MiniMax-M3

  Table 5: Model, agent-harness, and evaluator configurations used in the ResearchClawBench and AstaBench experiments.


level verification, and targeted revision. Accordingly, the              Within each paired comparison, the vanilla and
paired configurations are controlled for the underlying agent         +AutoSciRub settings receive the same task inputs, task-
and execution environment, but are not compute-matched,               visible resources, workspace, and tool access. Available tools
because AutoSciRub introduces the additional model calls              include the native capabilities of the corresponding agent har-
required by the method.                                               ness, such as file inspection, code execution, and web search,
                                                                      as well as the external retrieval services used by AutoSciRub.
Execution and evaluation protocol. Each task–                         The hidden target paper and the official benchmark evaluation
configuration pair is executed once, producing one                    rubric remain inaccessible to both settings during research
scientific report and one set of supporting artifacts. Each           execution.
resulting submission is then independently evaluated three
times using the same benchmark evaluator and evaluation                  We do not impose a shared explicit cap on tokens, tool
protocol. The arithmetic mean of the three judge scores is            calls, wall-clock runtime, or monetary cost across heteroge-
used as the task-level score.                                         neous agent harnesses. Each system instead operates under
                                                                      the execution, context, and tool constraints of its native envi-
   For ResearchClawBench, the overall score is computed as
                                                                      ronment. Our primary evaluation therefore focuses on output
the arithmetic mean over all 40 task-level scores, and each
                                                                      quality rather than budget-normalized efficiency.
domain score is computed over its four constituent tasks. For
AstaBench, the mean score is computed over the fixed 20-task             Rubric-guided verification and revision use a maximum
subset. Successful-task counts are computed independently             of three revision rounds with adaptive early stopping. To dis-
from the rubric-based evaluation scores.                              tinguish the effect of structured rubric guidance from that of
additional opportunities for revision, we additionally evalu-         not guarantee that an executable plan addresses the task’s
ate a three-round rubric-free self-refinement baseline starting       scientific core.
from the same initial reports and using the same underlying               Evidence Verifiability. Evidence Verifiability measures
research agent. The complete verification, revision, early-           whether the rubric requires inspectable and traceable ev-
stopping, and self-refinement protocols are described in the          idence that permits independent verification of both task
following subsection.                                                 completion and the resulting scientific claims. Verifiable
                                                                      evidence may include quantitative tables, figures, machine-
A.2    Rubric Quality Evaluation                                      readable outputs, controls, baseline comparisons, uncertainty
Compared rubric variants and scoring protocol. For                    estimates, provenance, and explicit links between claims and
each of the 40 ResearchClawBench tasks, we evaluate                   generated results. This dimension evaluates the checkability
two rubric variants: the instruction-derived rubric skele-            and diagnostic value of the evidence rather than the number
ton produced after Rubric Skeleton Induction, and the task-           of artifacts requested.
specific executable rubric produced after Scientific Litera-              Scientific Core Coverage. Scientific Core Coverage mea-
ture Grounding, Task-Data Exploration, and Criterion Syn-             sures the extent to which the rubric faithfully covers and op-
thesis.                                                               erationalizes the task’s core scientific success conditions. It
   Each rubric is evaluated along four dimensions: Speci-             evaluates whether the rubric’s objectives, methods or scien-
ficity, Actionability, Evidence Verifiability, and Scientific         tifically equivalent alternatives, metrics, comparisons, arti-
Core Coverage. All dimensions use a five-point ordinal scale,         facts, scope, conventions, evidence, and required conclusions
where a higher value indicates stronger rubric quality. We use        collectively target the intended scientific problem. Scores
MiniMax-M3 as the rubric-quality judge for all evaluations.           decrease when important success conditions are omitted or
To reduce cross-dimensional interference, we use four stan-           underweighted, when the rubric drifts toward an adjacent
dalone judge prompts, each of which evaluates exactly one             problem, or when core goals are replaced by non-equivalent
dimension. The judge receives only one candidate rubric in            proxies. Alternative methods and artifacts receive full credit
each call and is explicitly instructed not to score the other         when they provide scientifically equivalent or stronger evi-
three dimensions.                                                     dence for the same core claim.
   For every judge call, the evaluator is provided with the               The four dimensions capture complementary properties.
task instruction, a description of the task-visible data, the         A rubric may be highly specific and actionable but receive
candidate rubric, and the official benchmark checklist. The           a low Scientific Core Coverage score if it precisely opera-
checklist is used only as evaluator-side evidence for identi-         tionalizes the wrong analysis. Conversely, a concise rubric
fying the intended scientific success conditions. It is never         may identify the correct scientific core but receive lower
exposed to the agent during rubric construction, research ex-         Specificity or Actionability scores if important implemen-
ecution, verification, or revision. The judge is instructed to        tation choices remain unspecified. Evidence Verifiability is
assess semantic and scientific equivalence rather than lexical        assessed separately: a scientifically aligned and executable
overlap with the checklist.                                           plan may still be difficult to verify when it does not require
   The rubric skeleton and executable rubric are evaluated in         inspectable outputs that directly support its conclusions.
separate calls. The judge is not provided with the generated          Complete rubric-quality scoring prompts. The follow-
report or the alternative rubric variant. The overall quality         ing four prompts are used independently. In the JSON tem-
score of rubric R is computed as the unweighted arithmetic            plates, the value of score is replaced with an integer from
mean of the four dimension scores:                                    1 to 5. Rubric item identifiers refer to goal IDs for rubric
                    1                                                 skeletons and criterion IDs for executable rubrics.
          Q(R) = (sspec + sact + sver + score ) ,
                    4
where each score is an integer between 1 and 5.
Evaluation dimensions. Specificity. Specificity measures
how precisely the rubric states what is to be done and pro-
duced. A specific rubric names the relevant methods or exper-
iments, variables, conditions, metrics, comparators, thresh-
olds, and expected artifacts at a level that makes the intended
analysis unambiguous. Specificity concerns the concreteness
of the specification; it does not by itself establish that the plan
is executable, scientifically valid, or directed at the correct
scientific objective.
   Actionability. Actionability measures whether a compe-
tent agent can execute the rubric using the available inputs
without inventing consequential parts of the plan. An ac-
tionable rubric provides sufficient operational steps, depen-
dencies, parameter or method choices, decision rules, and
expected outputs to support implementation. Actionability
does not reward detail that is irrelevant to execution and does
Complete Rubric-Quality Scoring Prompts
  The following four prompts independently evaluate Specificity, Actionability, Evidence Verifiability, and Scientific Core
Coverage. Each judge call receives one candidate rubric and evaluates exactly one dimension.
  Specificity Scoring Prompt

  You are a senior scientific−methods reviewer. Evaluate exactly one construct: SPECIFICITY.

  Definition:
  Specificity is the precision with which the rubric states what is to be done and produced. It concerns whether the relevant methods or
  experiments, variables, conditions, metrics, comparators, thresholds, and expected artifacts are concrete enough to make the intended
  analysis unambiguous.

  Evaluation rules:
  1. Inspect the rubric’s core items rather than rewarding length or technical jargon.
  2. Credit concrete methods, conditions, variables, metrics, comparisons, thresholds, named outputs, and artifact requirements when
  they remove genuine ambiguity.
  3. Do not reward irrelevant detail or copied wording from the task or benchmark checklist.
  4. Do not lower the score merely because the specified plan may be difficult to execute, scientifically questionable, weakly evidenced,
  or misdirected; those properties belong to other dimensions.
  5. Cite rubric item IDs and identify the most consequential specified and unspecified details.

  Score anchors:
  1 = The rubric is almost entirely generic; core methods, conditions, metrics, and outputs are not concretely specified.
  2 = A few concrete details are present, but most consequential aspects remain ambiguous.
  3 = The main analysis is identifiable, but important conditions, metrics, comparisons, thresholds, or artifacts are underspecified.
  4 = Nearly all core details are explicit; only minor ambiguities remain.
  5 = The core analysis is precise and unambiguous across methods, conditions, variables, metrics, comparisons, thresholds, and
  expected artifacts.

  Return JSON only. Set "score" to an integer from 1 to 5:
  {
    "dimension": "specificity",
    "score": 1,
    "evidence": "Concise justification citing rubric item IDs.",
    "specified_strengths": ["..."],
    "remaining_ambiguities": ["..."]
  }

  TASK INSTRUCTION:
  [task_instruction]

  AVAILABLE−DATA DESCRIPTION:
  [available_data]

  BENCHMARK CHECKLIST −− EVALUATOR−ONLY CONTEXT:
  [benchmark_checklist]

  RUBRIC TO SCORE:
  [rubric]


  Actionability Scoring Prompt

  You are a senior scientific−methods reviewer. Evaluate exactly one construct: ACTIONABILITY.

  Definition:
  Actionability is the degree to which a competent agent can execute the rubric using the available inputs without inventing
  consequential parts of the plan. It concerns operational steps, dependencies, method and parameter choices, decision rules, and
  deliverables that reduce implementation uncertainty.

  Evaluation rules:
  1. Determine whether the rubric supplies an executable route from the available data to the required outputs.
2. Identify consequential methods, parameters, dependencies, preprocessing choices, decision rules, or deliverables that the agent
would otherwise have to invent.
3. Credit flexibility when multiple choices are genuinely interchangeable and the rubric supplies a sound decision rule or acceptable
range.
4. Do not reward detail that does not help execution. Do not judge whether the chosen scientific target is the correct one; that belongs
to Scientific Core Coverage.
5. Cite rubric item IDs and focus on implementation consequences.

Score anchors:
1 = No executable route is supplied; the agent must design nearly the entire plan.
2 = Major methods, dependencies, parameters, or decisions must be invented.
3 = An executable outline exists, but some consequential implementation choices remain unresolved.
4 = The core workflow is directly executable, with only minor or low−impact choices left open.
5 = An end−to−end operational plan specifies all consequential steps, dependencies, decision rules, and outputs needed for execution.

Return JSON only. Set "score" to an integer from 1 to 5:
{
  "dimension": "actionability",
  "score": 1,
  "evidence": "Concise justification citing rubric item IDs.",
  "executable_elements": ["..."],
  "missing_decisions": ["..."]
}

TASK INSTRUCTION:
[task_instruction]

AVAILABLE−DATA DESCRIPTION:
[available_data]

BENCHMARK CHECKLIST −− EVALUATOR−ONLY CONTEXT:
[benchmark_checklist]

RUBRIC TO SCORE:
[rubric]


Evidence Verifiability Scoring Prompt

You are a senior scientific−methods reviewer. Evaluate exactly one construct: EVIDENCE VERIFIABILITY.

Definition:
Evidence Verifiability is the degree to which the rubric requires inspectable and traceable evidence that allows an independent
reviewer to verify task completion and evaluate whether the scientific claims follow from the generated results.

Evaluation rules:
1. Inspect required quantitative tables, figures, machine−readable outputs, controls, baseline comparisons, uncertainty estimates,
provenance, and claim−to−evidence links when scientifically applicable.
2. Judge the diagnostic and confirmatory value of evidence, not the number of files.
3. Credit explicit must−show criteria, metrics, uncertainty, comparison targets, and traceable paths that make an artifact
independently checkable.
4. Penalize rubrics that allow conclusions to be asserted without supporting results, or request decorative outputs that cannot test the
claims.
5. Do not judge whether the rubric targets the correct scientific goal; that belongs to Scientific Core Coverage.

Score anchors:
1 = Conclusions can be asserted without any inspectable supporting evidence.
2 = Outputs are requested only vaguely or lack checkable criteria and claim links.
3 = Some core results are inspectable, but important claims, comparisons, uncertainty, or diagnostics remain weakly supported.
4 = Core claims are supported by checkable quantitative artifacts and appropriate diagnostics; only minor traceability gaps remain.
5 = The evidence chain is complete and traceable from method to result to claim, including controls, uncertainty, comparisons, and
provenance where relevant.
Return JSON only. Set "score" to an integer from 1 to 5:
{
  "dimension": "evidence_verifiability",
  "score": 1,
  "evidence": "Concise justification citing rubric item IDs.",
  "verifiable_artifacts": ["..."],
  "verification_gaps": ["..."]
}

TASK INSTRUCTION:
[task_instruction]

AVAILABLE−DATA DESCRIPTION:
[available_data]

BENCHMARK CHECKLIST −− EVALUATOR−ONLY CONTEXT:
[benchmark_checklist]

RUBRIC TO SCORE:
[rubric]


Scientific Core Coverage Scoring Prompt

You are a senior scientific−methods reviewer. Evaluate exactly one construct: SCIENTIFIC CORE COVERAGE.

Definition:
Scientific Core Coverage is the extent to which the rubric faithfully covers and operationalizes the task’s core scientific success
conditions through aligned objectives, scientifically equivalent methods, metrics, comparisons, artifacts, scope, conventions, evidence,
and required conclusions. It excludes material omission, goal drift, and substitution by adjacent but non−equivalent proxies.

Evaluation rules:
1. Infer the task’s core scientific success conditions from the instruction and available data. Use the benchmark checklist and its
criterion weights, when available, only as evaluator−side evidence of importance.
2. Map each core condition to rubric items and classify it as aligned, scientifically equivalent, partial, proxy, missing, or conflicting.
3. Judge semantic and scientific−function equivalence, never wording overlap. Alternative methods and artifacts deserve full credit
when they provide equivalent or stronger evidence for the same core claim.
4. Penalize omission or underweighting of high−importance goals, goal drift, non−equivalent proxy substitution, artifact or metric
mismatch, scope dilution, incompatible conventions, and conclusion anchoring.
5. Missing low−level implementation detail alone belongs to Specificity or Actionability and must not reduce this score when the
scientific target remains intact.

Score anchors:
1 = The rubric operationalizes a substantially different problem, contradicts a core success condition, or is dominated by
non−equivalent proxies.
2 = Major omissions, conflicts, or proxy substitutions affect one or more core or high−importance success conditions.
3 = The main objective is recognizable, but an important success condition is missing, weakened, underweighted, or replaced.
4 = Core success conditions are faithfully operationalized; only minor or peripheral mismatches remain, and valid equivalent
alternatives are used appropriately.
5 = All core success conditions are tightly covered by aligned or scientifically equivalent objectives, methods, metrics, comparisons,
artifacts, scope, and evidence, with no material drift, omission, or proxy replacement.

Return JSON only. Set "score" to an integer from 1 to 5. The allowed values of "importance" are "core", "important", and
"peripheral". The allowed values of "status" are "aligned", "equivalent", "partial", "proxy", "missing", and "conflicting":
{
  "dimension": "scientific_core_coverage",
  "score": 1,
  "evidence": "Concise justification citing rubric item IDs and core consequences.",
  "criterion_audit": [
   {
     "criterion": "...",
     "importance": "core",
     "status": "aligned",
      "rubric_items": ["R1"],
      "rationale": "..."
      }
    ],
    "core_gaps_or_drift": ["..."]
}

TASK INSTRUCTION:
[task_instruction]

AVAILABLE−DATA DESCRIPTION:
[available_data]

BENCHMARK CHECKLIST −− EVALUATOR−ONLY CONTEXT:
[benchmark_checklist]

RUBRIC TO SCORE:
[rubric]
A.3    Rubric-Guided Revision Evaluation                           requirement may instead be justified in free text while the
Experimental configuration and shared initialization.              corresponding structured field remains Boolean.
We compare rubric-guided revision with rubric-free holis-            The expected verifier output follows the schema below.
tic self-refinement on all 40 ResearchClawBench tasks. All
                                                                     Verifier Output Schema
checkpoint-0 reports, verification calls, targeted revisions,
and rubric-free revisions are executed with OpenClaw us-             {
ing deepseek/deepseek-v4-flash. There is no sep-                         "source": "rcbench_report_verifier",
arately instantiated verifier model. Instead, the same Open-             "overall_pass": false,
Claw agent invokes the report-verifier skill within                      "goal_checks": [
the task session.                                                          {
   Both revision strategies start from the same set of 40 frozen             "goal_id": "G1",
checkpoint-0 reports and figures. These checkpoint-0 outputs                 "pass": false,
                                                                             "coverage": {
are generated under the task-specific executable rubric after
                                                                              "experiment": true,
planning, literature grounding, experiment design, experi-                    "results": true,
ment execution, figure generation, and initial report writing,                "figure_or_table": false,
but before any verifier call or verifier-driven revision. Their               "conclusion": true,
mean ResearchClawBench score is 18.309083, reported as                        "mechanism_or_analysis": false
18.31 in the main paper.                                                     },
   For the rubric-free condition, the canonical checkpoint-                  "missing": ["..."],
0 report.md file and its figures are copied into a new                       "fixes": ["..."]
isolated workspace. SHA-256 hashes are computed before                     }
and after copying to verify that the starting report and fig-            ],
                                                                         "rubric_item_checks": [
ures are unchanged. We do not claim that the two strategies                {
share an identical complete workspace: checkpoint-0 code                     "rubric_item_id": "R1",
and output directories are not frozen or copied because they                 "pass": false,
may contain rubric-related state and later feedback. Instead,                "missing": ["..."],
the rubric-free workspace is supplied again with the original                "fixes": ["..."]
instruction, task data, and related work, and the agent may                }
create new code, outputs, and analyses during refinement.                ],
                                                                         "feedback_items": [
Criterion-level verification. Before each guided revision,                 {
the current artifact is evaluated by the same OpenClaw agent                 "feedback_id": "F001",
through a verification-only call. The verifier examines the                  "goal_id": "G1",
current report, generated experiments and results, figures                   "rubric_item_id": "R1",
and tables, quantitative values, conclusions, and mechanistic                "issue": "...",
or analytical explanations. It also checks whether the artifacts             "required_action": "..."
                                                                           }
required by the task-specific executable rubric are present or           ],
explicitly represented in the report, including their filenames,         "artifact_checks": [
titles, captions, display names, and detailed descriptions.                "path/name, present?, described?, issue"
    The verifier is instructed to distinguish generated exper-           ],
imental evidence from statements supported only by prior                 "required_iterations": ["..."]
literature. Conclusions are considered adequately supported          }
only when they follow from evidence produced within the
current task execution.                                               The runner reads the top-level overall_pass value
    For each scientific goal, the verifier records whether the     directly and does not independently reconstruct the pass de-
report contains the required experiment, results, figure or        cision from the individual checks. If the verifier output is
table, conclusion, and mechanism or analytical explanation.        missing or cannot be parsed, the runner treats the artifact
It also evaluates individual rubric items and produces sta-        as not passing and proceeds to revision. No separate JSON-
ble feedback items specifying the remaining issue and the          schema validation or verifier-specific retry is performed. A
required corrective action.                                        task run is marked as failed only when the OpenClaw process
    The top-level overall_pass field is an LLM judgment            exits with a nonzero status.
rather than a deterministic conjunction of all criterion-level
Boolean values. An artifact passes when all scientific goals       Targeted revision and early stopping. If verification does
have sufficient experimental support, interpretation, and con-     not pass, the current report_rubric_check.json is
clusion coverage, and all high-priority rubric items are ei-       supplied to the same OpenClaw agent for one targeted revi-
ther satisfied or explicitly and scientifically justified by the   sion. The revision call has access to the current workspace,
generated evidence. Lower-priority items are not required          INSTRUCTIONS.md, the current report, the executable
to pass individually. The verifier does not produce a sep-         rubric, goal-level experiment plans, existing code, outputs,
arate structured not_applicable state; an inapplicable             figures, and the current verifier feedback.
   The agent may modify code, rerun or add experiments              Each resulting report is independently scored three times by
and analyses, regenerate figures or tables, correct numerical       the same GPT-5.1 judge.
results, revise unsupported claims, and update the complete            This baseline controls for repeated opportunities to inspect
report/report.md. The revision call is instructed not               and revise the report, but it is not a strictly compute-matched
to invoke the verifier itself; verification and revision are ex-    or workspace-identical control. Guided revision separates
ecuted as separate agent calls.                                     verification and revision into two calls and uses adaptive
   We allow at most three revision rounds. The resulting            stopping, whereas rubric-free refinement combines review
execution sequence is                                               and revision into one call and always performs three rounds.
                                                                    Guided revision also retains the original code and output
 V (0) → R(1) → V (1) → R(2) → V (2) → R(3) → V (3) ,               state, while the rubric-free condition starts from the frozen
                                                                    report and figures in a newly initialized workspace.
where V (t) denotes verification of checkpoint t, and R(t)
denotes the revision producing checkpoint t. Consequently,
each task receives at most three revision calls and four ver-
ification calls. The procedure terminates immediately when
a verification call returns overall_pass=true. If the
artifact does not pass earlier, a final verification is performed
after the third revision.
Adaptive stopping and checkpoint aggregation. Rubric-
guided revision generates and evaluates only reports that
are actually produced. Across the 40 tasks, the experiment
contains 103 distinct report checkpoints: 40 checkpoint-0
reports, 40 checkpoint-1 reports, 17 checkpoint-2 reports,
and 6 checkpoint-3 reports.
   When a task passes verification, no artificial reports are
generated for later revision budgets. Instead, its most re-
cent real report and its previously obtained score are carried
forward when computing later checkpoint-level means. The
carried-forward report is not rerun or rescored. Thus, every
reported guided checkpoint mean is computed over all 40
tasks, while only tasks that have not yet stopped produce a
new report at the next revision round.
   Each actually generated report checkpoint is indepen-
dently scored three times by the GPT-5.1 ResearchClaw-
Bench judge, and the arithmetic mean of the three scores is
used as its task-level score.
Rubric-free holistic self-refinement. The rubric-free
baseline starts from the same frozen checkpoint-0 re-
port and figures and uses the same OpenClaw and
deepseek/deepseek-v4-flash configuration. It is
explicitly prohibited from accessing, constructing, inferring,
or searching for the task-specific executable rubric, the hid-
den benchmark checklist, the target study, rubric scores, or
prior verifier feedback.
   At     each     round,     the    agent     invokes     the
holistic-self-review skill and performs a
holistic scientific review followed immediately by one
revision within the same agent call. The agent may use tools,
write code, rerun or add experiments and analyses, modify
figures and tables, revise results and claims, and update the
complete report.
   Unlike rubric-guided revision, rubric-free self-refinement
does not use verifier-based early stopping. All 40 tasks exe-
cute three review–revision cycles, producing 40 real reports
at each of checkpoints 1, 2, and 3. In the first round, the
runner requires between one and six prioritized issues. In the
second and third rounds, an empty issue list and a no-op revi-
sion are allowed when no substantive deficiency is identified.
                                                  B     Rubric Output Formats
This section presents the output formats of the instruction-derived rubric skeleton and the task-specific executable rubric. One
complete entry is shown for each format; the remaining entries are omitted for brevity.
Instruction-derived rubric skeleton. The rubric skeleton represents the task as a set of atomic scientific goals. Each goal
contains a unique identifier, a concise title, and a concrete task description.
  Instruction-Derived Rubric Skeleton
  {
    "goals": [
      {
        "goal_id": "G1",
        "title": "Characterize spatial concentration of cloud−seeding projects",
        "task": "Analyze the geographic distribution of cloud−seeding projects across U.S. states using the published records, and identify
  which states account for the majority of reported activity."
      },
      {
        "...": "Additional scientific goals are omitted."
      }
    ]
  }


Task-specific executable rubric. The executable rubric augments the scientific goals with concrete experiments, required
evidence artifacts, metrics, comparisons, data sources, expected conclusions, priorities, and execution constraints.
  Task-Specific Executable Rubric

  {
   "source": "rcbench_experiments_design",
   "task_summary": "Reproduce and validate the central empirical conclusions from a published NOAA weather−modification dataset
  of U.S. cloud seeding projects (2000−2025). Generate spatial concentration maps, annual activity dynamics, purpose composition,
  and agent−apparatus deployment patterns using transparent, script−based analysis.",
   "selected_environment": ".venv−rcb−base",
   "environment_reason": "The selected environment provides the packages required for tabular analysis, statistical computation, and
  geospatial visualization.",
   "selected_strategy": "Independently compute the required statistics and figures from the structured dataset and synthesize the results
  into an empirical assessment.",

   "rubric_items": [
     {
       "id": "R1",
       "linked_goal_ids": [
         "G1"
       ],
       "goal": "Quantify state−level spatial concentration of cloud seeding projects and produce a choropleth map showing geographic
  distribution.",
       "experiment_plan_path": "outputs/goals/G1/experiment_plan.md",
       "experiments_to_run": [
         "Group records by state and count projects",
         "Compute rank, percentage share, and Gini coefficient",
         "Merge state counts with GeoJSON and generate a choropleth map",
         "Create a state−by−purpose heatmap"
       ],
       "required_artifacts": [
         {
           "type": "figure",
           "name": "spatial_distribution.png",
           "expected_path": "report/images/spatial_distribution.png",
           "must_show": "A choropleth map of U.S. states colored by the number of cloud seeding projects, showing strong western
  concentration and identifying California, Colorado, Texas, and Utah among the leading states.",
           "description_requirement": "Explain the geographic pattern of cloud seeding activity and the factors associated with western
  concentration."
          },
          {
            "type": "figure",
            "name": "state_purpose_heatmap.png",
            "expected_path": "report/images/state_purpose_heatmap.png",
            "must_show": "A state−by−purpose heatmap demonstrating how project purposes vary across states.",
            "description_requirement": "Describe how project purposes vary across states and regions."
          },
          {
            "type": "table",
            "name": "top_states_table",
            "expected_path": "report/report.md",
            "must_show": "A ranked list of the leading states with project counts and percentage shares.",
            "description_requirement": "Summarize the state−level concentration statistics."
          }
        ],
        "metrics_or_values": [
          "Projects per state",
          "Percentage share of the top three and top five states",
          "Gini coefficient"
        ],
        "baselines_or_comparisons": [
          "Expected geographical concentration in water−stressed western states"
        ],
        "data_sources": [
          "data/dataset1_cloud_seeding_records/cloud_seeding_us_2000_2025.csv[state]",
          "data/dataset1_cloud_seeding_records/us_states.geojson"
        ],
        "expected_conclusions": [
          "Cloud seeding is heavily concentrated in western U.S. states",
          "California has the highest project count",
          "The spatial distribution reflects water−resource management priorities"
        ],
        "priority": "high",
        "risk_if_missing": "Loss of the primary spatial evidence supporting geographic concentration claims."
      },
      {
        "...": "Additional executable rubric items are omitted."
      }
    ],

    "execution_plan": [
      {
        "...": "Task−level execution steps are omitted."
      }
    ],

    "claims_to_avoid": [
      "Do not claim causal relationships between cloud seeding and precipitation changes.",
      "... additional unsupported claims are omitted ..."
    ]
}
