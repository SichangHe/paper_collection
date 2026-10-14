                                          Change2Task: From Repository Changes to Executable Coding Agent Tasks and
                                                                       Environments
                                                                Haomin Qi1,2 , Xingliang Wang1,3 , Xuanqi Gao1,4 , Baihui Sang1,5 ,
                                                               Xin Zhang1 , Minghua Ma1 , Pengfei Gao1 , Yu Kang1 , Qingwei Lin1 ,
                                                                      Saravan Rajmohan1 , Dongmei Zhang1 , Qi Zhang1
                                                                                                             1
                                                                                                             Microsoft
                                                                                            2
                                                                                                University of California San Diego
                                                                                                      3
                                                                                                        Zhejiang University
                                                                                                   4
                                                                                                     Xi’an Jiaotong University
                                                                                                       5
                                                                                                         Nanjing University

                                                                     Abstract
                                           Scaling coding agents requires a continuing supply of exe-
                                           cutable data for training, benchmarking, and continuous eval-
                                           uation. Each task must couple a realistic software state with
                                           a specification, development tools, and reliable verification.
arXiv:2607.28591v1 [cs.SE] 30 Jul 2026




                                           To expand this supply, we present Change2Task, a system
                                           grounded in repository history that converts merged pull re-
                                           quests (PRs) into verified tasks on healthy modern revisions of
                                           the same repository. It aligns historical evidence with evolved
                                           code, reconstructs task states through Patch Reversal, Code
                                           Mapping, or Agent Reconstruction, and validates the lifecy-
                                           cle from a healthy base to a task state and a restored state.
                                           By deriving multiple tasks grounded in developer evidence
                                           from maintained environments, Change2Task provides ex-
                                           ecutable data for coding agent training and evaluation while
                                           reducing repeated environment setup, storage, and task con-
                                           struction effort. We evaluate the system through five of the
                                           most common and widely adopted coding agent task fami-
                                           lies: Bug Fix, Feature Addition, Test Generation, Application
                                           Programming Interface (API) Migration, and Security Repair.
                                           Starting from 1,130 source changes eligible for construction,
                                           Change2Task achieves 79.6% verified task construction suc-
                                           cess across these task families. On a matched candidate set, it
                                           recovers 29.2% more verified tasks than a construction base-
                                           line based on PRs. Historical and reconstructed cases achieve
                                           up to 98.0% matched outcome agreement under agent evalu-                Figure 1: A Change2Task Feature Addition Task Case Con-
                                           ation, while reuse of modern bases reduces measured expen-              struction example.
                                           diture across the complete pipeline by 10.8%.


                                                                 Introduction                                      synthesizes verifiable coding tasks with executable environ-
                                         Coding agents have shifted software automation from sin-                  ments, and GLM-5 develops asynchronous reinforcement
                                         gle turn generation to iterative interaction with development             learning infrastructure for long horizon interaction (Yang
                                         environments. Systems such as SWE-agent and OpenHands                     et al. 2025c; Cao et al. 2026; GLM-5 Team 2026). Producing
                                         search repositories, edit files, invoke tools, run tests, and re-         these environments is expensive: daVinci-Env reports 45,320
                                         vise solutions from execution feedback (Yang et al. 2024;                 Docker environments across more than 12.8K repositories
                                         Wang et al. 2025b). Each executable task therefore acts as a              and approximately $891K in construction cost, while SWE-
                                         unit of agent data, coupling a repository state with dependen-            Universe produces 807,693 verifiable environments using
                                         cies, tools, a specification, and a verifier. We use environment          specialized distributed infrastructure (Fu et al. 2026; Chen
                                         engineering for constructing this executable substrate (Li                et al. 2026). Snapshots dedicated to individual tasks further
                                         et al. 2026a). Its supply bounds the scale and diversity of               multiply images, storage, registry traffic, cold starts, and roll-
                                         agent training, benchmarks, and continuous evaluation.                    out pressure. The central systems question is how to obtain
                                            Recent systems make this dependence explicit. Kimi-Dev                 more verified agent data from every executable repository
                                         adapts agents from public trajectories, Qwen3-Coder-Next                  environment.
   Existing task sources only partly exploit this opportunity.    SWE-agent studies interfaces between agents and computers,
Historical benchmarks preserve developer issues, patches,         OpenHands provides a sandboxed platform, AutoCodeRover
and tests but bind tasks to original revisions (Jimenez           combines program structure with search, and Agentless uses
et al. 2024). Fresh synthesis can generate many instances         fixed localization, repair, and validation stages (Yang et al.
in prepared repositories, as SWE-smith demonstrates for re-       2024; Wang et al. 2025b; Zhang et al. 2024; Xia et al. 2025).
pair (Yang et al. 2025b), yet synthetic failures need not pre-    SWE-bench established issue resolution on repository snap-
serve a real maintenance intent. Reconstructing a repository’s    shots with hidden tests; SWE-Gym and R2E-Gym extend
own historical changes on maintained code can retain devel-       executable feedback to training (Jimenez et al. 2024; Pan
oper grounding, refresh tasks, and increase the data obtained     et al. 2025; Jain et al. 2025). Together, these systems show
from each environment.                                            that performance depends on the model, repository state,
   To address this problem, we introduce Change2Task, a           interaction interface, and exposed verifier.
framework and tool for turning repository history into exe-          Recent benchmarks expand freshness, industrial difficulty,
cutable coding agent data. It starts from a merged pull request   and task breadth through Multi-SWE-bench, SWE-bench-
(PR) and a fixed, runnable descendant revision in the same        Live, SWE-Bench Pro, and SWE-bench Multimodal (Zan
repository. The PR supplies the description, implementa-          et al. 2025; Zhang et al. 2025; Deng et al. 2025; Yang et al.
tion patch, and behavioral evidence; the descendant supplies      2025a). FeatureBench and SWE-Cycle cover feature devel-
the healthy modern base. Construction proceeds through            opment and fuller issue resolution cycles; SWE-EVO and
Level 1, Patch Reversal; Level 2, Code Mapping; and Level         TestEvo-Bench study repository evolution and joint code and
3, Agent Reconstruction, escalating as repository evolution       test evolution (Zhou et al. 2026; Guan et al. 2026; Le et al.
weakens direct correspondence. Each accepted task patch has       2025; Wang, Wang, and Nie 2026). Live, multimodal, and
a restoration patch and is validated across healthy, task, and    evolutionary settings also require environments to remain ex-
restored states. By deriving multiple lightweight task variants   ecutable as code, dependencies, and interfaces change. This
from one maintained base, Change2Task reduces repeated            breadth increases demand for maintained environments, out-
environment setup, storage pressure, and manual construc-         puts specific to each task, and reliable verifiers.
tion and validation effort while expanding executable data
for coding agent training and task generation.                    Executable Repository Infrastructure
   Task objectives are expressed through adapters that define
                                                                  Executable evaluation requires dependencies, services, build
the goal, expected output, executable oracle, and edit scope.
                                                                  commands, test discovery, and isolation. EnvBench and Se-
We evaluate Bug Fix, Feature Addition, Test Generation,
                                                                  tupBench document persistent setup obstacles (Eliseeva et al.
Application Programming Interface (API) Migration, and
                                                                  2025; Arora, Jang, and Moghaddam 2025). Repo2Run syn-
Security Repair because they are among the most common
                                                                  thesizes Dockerfiles from feedback, RepoLaunch automates
and widely adopted coding agent workloads and require dis-
                                                                  setup and test management, and MEnvAgent combines plan-
tinct outputs and verification contracts. The same interface
                                                                  ning, verification, and cross-language reuse (Hu et al. 2025;
naturally supports additional coding tasks whenever their
                                                                  Li et al. 2026b; Guo et al. 2026a). Their focus is recovering
maintenance intent and executable success condition can be
                                                                  or maintaining a runnable revision, an essential prerequisite
derived from historical PR evidence.
                                                                  for agent evaluation. They do not determine how many dis-
   Figure 1 gives a Feature Addition example. Repository
                                                                  tinct, historically grounded task states one prepared base can
history supplies a task grounded in developer evidence, while
                                                                  support.
a maintained revision supplies the environment in which that
task is executed.                                                    At scale, SWE-Factory coordinates environment, test,
                                                                  and instance construction, while daVinci-Env and SWE-
   Our contribution is Change2Task, a general framework
                                                                  Universe combine specialized builders, self-verification, and
and implemented tool that transfers developer-grounded
                                                                  distributed execution (Guo et al. 2026b; Fu et al. 2026; Chen
maintenance changes to current code and verifies their prove-
                                                                  et al. 2026). SWE-smith reuses configured images for syn-
nance, behavior, scope, and restoration. From 1,130 eligible
                                                                  thetic instances (Yang et al. 2025b). These efforts reduce
changes, Change2Task finalizes 900 paired tasks; on 621
                                                                  setup cost or increase corpus scale. Change2Task is com-
matched Bug Fix candidates, it reconstructs 500 versus 387
                                                                  plementary: it begins after a healthy base is executable and
for SWE-smith PR Mirror. The corpus achieves 0.894 task
                                                                  increases the verified, developer-grounded task supply ob-
weighted source change profile fidelity. Under matched agent
                                                                  tained from that investment.
evaluation, historical and reconstructed cases achieve up to
98.0% outcome agreement while preserving the agent rank-
ing. Reusing 388 modern bases reduces environment time            Task Construction for Agents
by 58.4%, storage by 71.2%, and end-to-end expenditure by         Historical benchmarks ground tasks in developer issues,
10.8%.                                                            patches, and tests. Defects4J, SWE-bench, and SWE-Gym
                                                                  preserve realistic outcomes at original revisions (Just, Jalali,
                      Related Work                                and Ernst 2014; Jimenez et al. 2024; Pan et al. 2025); SWT-
                                                                  Bench emphasizes tests that distinguish faulty and repaired
Coding Agents and Repository Environments                         states (Mündler et al. 2024). R2E-Gym and SWE-Synth scale
Agents operating at repository scale inspect code, edit files,    through mutation, model generation, and executable feed-
invoke tools, and revise solutions from execution feedback.       back (Jain et al. 2025; Pham et al. 2026), but generated tasks
                                         Figure 2: Overview of the Change2Task workflow.


need not match a maintenance intent observed in the reposi-        Deriving Task Evidence
tory.                                                              Change2Task derives task evidence from a merged PR in
   The closest method, SWE-smith’s PR Mirror, asks a model         the repository’s own history. Its description, implementation
to undo a historical PR in a current repository and retains        patch, and executable checks identify the changed condition,
candidates that break target tests (Yang et al. 2025b). Fea-       the checks that observe it, and nearby behavior that must
tureBench removes tested feature units to construct feature-       remain intact. This stage produces target checks, regression
development tasks (Zhou et al. 2026). Both demonstrate task        checks, and a source change profile. Target checks expose
generation inside prepared repositories, but emphasize one         the condition to be reconstructed; regression checks protect
construction operator or task objective. A broader construc-       surrounding behavior; the source change profile records the
tion system must adapt to repository evolution, preserve the       affected components and edit extent.
historical maintenance contract, and support different agent          Candidates are excluded when the changed condition is
outputs and oracles.                                               ambiguous, its checks cannot be executed, or the relevant
   Change2Task reconstructs a real maintenance event on a          change cannot be separated from unrelated modifications.
maintained descendant of the same repository. Shared lineage       The retained evidence provides provenance and the source
and target, regression, restoration, scope, and source change      change profile for later validation.
profile checks connect the modern task to its source PR.
One validation core then serves multiple objectives without        Establishing the Modern Task Base
rebuilding the base environment.                                   For each eligible PR, Change2Task selects a fixed descen-
                                                                   dant revision from the same repository lineage as the healthy
                                                                   modern base H. It first honors a declared healthy or tar-
                      Methodology                                  get revision. If neither is available, it resolves the accessible
Change2Task reconstructs, in modern code, the task condi-          upstream default branch in a fixed priority order. A fall-
tion represented by a historical PR. It creates an executable      back to the historical base is recorded separately and is not
task state on a fixed healthy descendant of the same repository    counted as a modern base. Selection is completed before
while retaining the PR as developer evidence. The modern           task construction, and the resolved commit hash is frozen for
revision supplies the environment in which an agent will act.      reproducibility.
                                                                      The selected revision must support a clean checkout, its
   We use one compact notation to describe this lifecycle:         runtime dependencies and services, and executable checks.
                                                                   It must also still host the relevant behavior: the mapped target
                 P                   D       G
                 s
           Vpre −→ Vpost ,              → H ′.
                                 H −→ C −                          and regression checks must pass on H, and there must be a
                                                                   defensible transformation surface in the modern code. Native
The source patch Ps changes the historical state before the        repository configuration or an external preparation tool may
PR, Vpre , into Vpost . Change2Task starts from a healthy          establish this environment; Change2Task operates after the
modern base H, applies a task patch D to obtain task state         base is runnable. Appendix C gives the full resolution order
C, and records a restoration patch G that yields restored state    and acceptance gates.
H ′ . We require H ′ to recover the relevant healthy behavior         PR alignment locates the modern realization of the
of H, not to reproduce it textually. Figure 2 summarizes the       changed behavior, implementation, and checks despite refac-
four stages.                                                       toring, file movement, API changes, or test reorganization. A
candidate advances only when this correspondence is suffi-
ciently grounded and both target and regression checks pass
on H.
   This stage also instantiates a task specification: the goal
presented to the agent, the expected output, the validation
oracle, and the permitted edit scope. Our evaluation adapters
create an unfixed behavior for Bug Fix, a missing capa-
bility for Feature Addition, an observable failure for Test
Generation, old API usage for API Migration, or a sand-
boxed vulnerability for Security Repair. These adapters vary
the objective and oracle while sharing one construction and
validation core. Additional task families can use the same
core whenever their task condition, output contract, and ex-
ecutable oracle can be derived from historical PR evidence
on a healthy descendant revision.

Constructing the Task State
Given the task evidence, healthy modern base, and task
specification, Change2Task constructs D so that C =                   Figure 3: Task state construction in Change2Task.
apply(H, D) presents the intended maintenance condition
while preserving unrelated behavior. Figure 3 expands the
three construction levels. Construction escalates only when       transformation when possible, otherwise constructed as the
an earlier level cannot produce a valid candidate.                corresponding modern repair, and must restore the intended
   Level 1: Patch Reversal. Level 1 reverses the source patch     behavior from C to H ′ .
when it remains compatible with the modern context. This
route preserves the closest structural link to the change writ-   Lifecycle and Scope Validation
ten by the developer.                                             Change2Task validates each candidate over three exe-
   Level 2: Code Mapping. When direct replay fails but            cutable states. On healthy modern base H, target and regres-
a unique source-block correspondence remains, Level 2 lo-         sion checks pass. On task state C, target checks expose the
cates the historical post-change block in the modern file. It     specified task condition while regression checks continue to
allows indentation normalization and replaces the block with      pass. After applying G, both check sets pass on restored state
its reindented pre-change form. The method favors conser-         H ′ . The target checks therefore pass, fail, and pass across
vative local transformations, reparses the result, and requires   the three states, while regression checks pass throughout.
the mapped patch to pass the same scope and executable            Repeated runs reject unstable cases.
gates. Level 2 makes one structure-guided attempt. Missing,          The scope gate permits only artifacts allowed by the task
ambiguous, or incompatible correspondence advances the            specification and prevents protected checks or metadata from
case to Level 3.                                                  manufacturing validity. The fidelity gate compares the source
   Level 3: Agent Reconstruction. When the historical be-         PR with the modern realization using affected components,
havior remains present but structural correspondence is in-       edit extent, and check surface. It rejects scope collapse, in
sufficient, a construction agent receives PR evidence, rel-       which a substantial source change becomes trivial, and scope
evant modern context, the task specification, and feedback        inflation, in which a narrow change requires broad unrelated
from prior attempts. It proposes scoped candidate patches         edits.
and filters them through apply, syntax, and scope checks,            An accepted variant contains H, D, G, the target and re-
then ranks survivors by source change profile fidelity and        gression checks, the task specification, and source PR prove-
edit complexity before lifecycle validation. A failed candi-      nance. Only variants that pass lifecycle, scope, and fidelity
date returns structured evidence identifying an unmet target      validation are frozen for evaluation. The task families there-
condition, broken regression check, restoration failure, or fi-   fore demonstrate different agent goals and scoring rules over
delity deviation. The loop allows at most four attempts and       one reusable construction core.
terminates at acceptance or budget exhaustion. Cases without
a defensible modern behavior host are rejected, and down-                               Experiments
stream agent outcomes never select or revise tasks. Appendix
C gives Level 2 pseudocode and the complete Level 3 proto-        Experiment Setup
col.                                                              Paired task corpus. The construction study begins with
   Patch checks reject candidates that fail to apply, exceed      1,130 construction-eligible source changes: cases for which
the permitted scope, or break basic syntactic and build in-       source PR evidence, executable checks, and same-repository
tegrity. Complexity matching compares their files, hunks,         base prerequisites are available. The process yields 900
changed lines, symbols, and check surface with the source         paired sets: 500 Bug Fix sets and 100 each for Feature
change profile. For an accepted task patch D, Change2Task         Addition, Test Generation, Application Programming Inter-
records a restoration patch G: it is derived as the inverse       face (API) Migration, and Security Repair. We allocate more
                          Figure 4: RQ1 recovery, construction routes, and terminal rejection reasons.


Bug Fix sets because repository-level repair has the broad-           Method                  Verified Recovery       95% CI
est standardized pool of executable tasks. Every set con-             Direct reversal          81/621      13.0% [10.6, 15.9]
tains two provenance-linked branches. The Original Branch             SWE-smith PR Mirror     387/621      62.3% [58.4, 66.0]
is the official benchmark case at its historical revision; the        Change2Task             500/621      80.5% [77.2, 83.4]
Change2Task Branch reconstructs that case on a healthy
modern revision of the same repository. Thus, each modern            Table 1: Matched recovery on 621 Bug Fix candidates.
task has a specific historical counterpart established before
agent evaluation. Appendix B reports the upstream evidence
and readiness funnel.                                              RQ1: How Reliably Does Change2Task
                                                                   Reconstruct Tasks from Repository History?
Tasks and success criteria. Each adapter defines a distinct
output and verification contract:                                  We collect 1,130 construction-eligible changes from 12 pub-
                                                                   lic benchmark collections and releases (Jimenez et al. 2024;
1. Bug Fix. Repair faulty behavior and pass target and re-         Zhang et al. 2025; Deng et al. 2025; Li et al. 2025; Badert-
   gression checks.                                                dinov et al. 2025; Wang et al. 2025a; Islam et al. 2023; Wei
                                                                   et al. 2025; Bui, Scandariato, and Díaz Ferreyra 2022; Wu
2. Feature Addition. Implement the requested missing be-
                                                                   et al. 2023). We define verified task recovery as the fraction
   havior and pass feature and regression checks.
                                                                   reaching the finalized corpus after lifecycle, scope, fidelity,
3. Test Generation. Add a test that fails on the task state,       and semantic qualification. Appendix E reports exact counts
   passes after restoration, and respects the test-only scope.     and Wilson 95% confidence intervals (CIs).
                                                                      Figure 4(a) shows that Change2Task reconstructs 900
4. API Migration. Replace obsolete source-API usage with           of 1,130 eligible changes, yielding 79.6% overall recovery.
   the required target API and pass migration and regression       Family estimates range from 76.3% for API Migration to
   checks.                                                         82.0% for Feature Addition, with wider CIs for the four
5. Security Repair. Remove the vulnerability exposed by            smaller families.
   a deterministic sandboxed oracle and pass security and             Figure 4(b) assigns each finalized task to its first success-
   regression checks.                                              ful construction level. Level 1 contributes 95 tasks directly;
                                                                   Level 2 contributes 190 after Level 1 fails; Level 3 con-
A solution is counted as solved only when its family-specific      tributes 615 after both earlier levels are exhausted. The shares
oracle, regression checks, and scope gate all pass.                are 10.6%, 21.1%, and 68.3%, quantifying the incremental
                                                                   coverage supplied by each level.
Construction and evaluation agents. Agent Reconstruc-                 Figure 4(c) assigns each of the 230 rejected candidates one
tion uses Claude Code with Opus 4.8 in a bounded loop              terminal reason. Lifecycle validation accounts for 50 cases,
that generates, executes, and refines candidates. Evaluation       environment or preflight failures for 44, and exhausted can-
uses Codex CLI with GPT-5.5, Claude Code with Sonnet 5,            didate construction for 42. Attrition is therefore distributed
Gemini CLI with Gemini 3.1 Pro, and GitHub Copilot with            across base readiness, task construction, executable valida-
GPT-5.6 Terra. Each agent receives one clean run on each           tion, and final qualification.
branch. Within a pair, task intent, model, interface, visible         Table 1 compares methods on the same 621 Bug Fix can-
evidence, permissions, context policy, budget, and verifier        didates under one construction and verification envelope.
strength are held constant. Evaluation agents cannot access        Direct reversal recovers 81 tasks and SWE-smith PR Mir-
construction traces, task patches, restoration patches, or hid-    ror 387 (Yang et al. 2025b); Change2Task recovers 500.
den target checks. Appendix D gives the execution limits and       It therefore adds 113 verified tasks, a 29.2% relative and
complete protocol.                                                 18.2-point absolute gain. Appendix C specifies the matched
                                                                   corpus is directly accepted by both judges. Appendix F gives
                                                                   the labels and adjudication protocol.
                                                                      The audit also defines the applicability boundary. An
                                                                   adapter needs a historical PR with identifiable intent, a
                                                                   healthy descendant hosting the behavior, an executable or-
                                                                   acle, and a bounded edit policy. Outputs may include code,
                                                                   tests, configuration, or other artifacts; grounded evidence and
                                                                   executable validation matter more than a fixed task taxonomy.
                                                                   RQ2 Finding. Change2Task preserves the developer-
                                                                   grounded maintenance contract of historical changes while
                                                                   translating their implementation footprint to evolved code.

                                                                   RQ3: How Consistent Are Agent Outcomes Across
Figure 5: Historical to modern source change profile fidelity      the Two Branches?
by task family and construction level.
                                                                   The Original Branch is the historical behavioral anchor, and
                                                                   the Change2Task Branch realizes the same maintenance in-
                                                                   tent on modern code. Table 2 reports branch solve rates, di-
model, evidence, context, attempts, tools, and budgets.            rectional differences, complete paired outcomes, raw agree-
RQ1 Finding. Change2Task transforms repository history             ment, and Cohen’s κ. Agreement is the fraction with the
from a passive record into a recoverable source of verified        same solved or unsolved outcome; κ adjusts for the branches’
coding tasks through progressively adaptive construction.          marginal solve rates.
                                                                      Across 3,600 matched agent-task pairs, each branch con-
RQ2: How Faithfully Does Change2Task Preserve                      tains 1,478 solved outcomes, or 41.1%. Discordance is ex-
Historical Changes?                                                actly balanced: 186 outcomes are solved only on the Original
                                                                   Branch and 186 only on the Change2Task Branch. Aggre-
RQ2 examines how well the 900 finalized tasks retain the
                                                                   gate agreement is 89.7%, Cohen’s κ is 0.787, positive agree-
complexity, scope, and maintenance meaning of their source
                                                                   ment is 87.4%, and solved-set Jaccard overlap is 77.6%. The
changes. We compare each historical source patch with its
                                                                   paired solve-rate difference is 0.0 points with a 95% interval
modern restoration patch along six dimensions: changed
                                                                   of [-1.1, 1.1], and exact McNemar p = 1.0. Appendix G
files, hunks, lines, symbols, target checks, and regression
                                                                   defines these statistics.
checks. Dimension similarity is the ratio between smaller
and larger counts, with identical empty counts assigned 1.            Agent-level behavior is stable. Agreement ranges from
Their weighted combination emphasizes changed lines, fol-          86.4% for Copilot with GPT-5.6 Terra to 95.3% for Gemini
lowed by hunks, files, the two check surfaces, and symbols.1       3.1 Pro, with aggregate κ from 0.729 to 0.852. Gemini 3.1
                                                                   Pro combines the highest agreement with lower solve rates.
   Figure 5(a) reports family means from 0.825 to 0.925,
                                                                   Copilot with GPT-5.6 Terra and Claude Code Sonnet 5 have
with a macro average of 0.887 and task-weighted average of
                                                                   the highest overall solve rates, while Codex with GPT-5.5
0.894. Test Generation scores 0.925, Bug Fix 0.903, Feature
                                                                   performs best on Test Generation and API Migration.
Addition 0.893, API Migration 0.890, and Security Repair
                                                                      Directional changes remain small and dispersed. Claude
0.825. The connected profiles show that the aggregate reflects
                                                                   Code Sonnet 5 and Copilot with GPT-5.6 Terra gain 12 and
multiple aspects of the source change rather than one size
                                                                   10 solved tasks on the Change2Task Branch, Codex with
statistic.
                                                                   GPT-5.5 changes by four, and Gemini 3.1 Pro loses 18. No
   Figure 5(b) reports mean fidelity of 0.992 for Patch Re-        task-family shift exceeds five percentage points, and 11 of
versal, 0.888 for Code Mapping, and 0.881 for Agent Recon-         20 comparisons differ by at most two points. Reconstruction
struction. These values characterize finalized tasks as code
correspondence becomes weaker; route assignment is de-
scriptive rather than randomized.                                                                      Kimi K3           Both judges
                                                                                                       DeepSeek V4 Pro   κ
   Kimi K3 and DeepSeek V4 Pro independently review 912                                          100                                   0.80
                                                                    Intent-preserving rate (%)




anonymized historical and modern pairs without seeing the
construction route, trace, or model. The review records be-                                      95                                    0.75

havioral triggers, expected behavior, affected APIs, source-                                                                                  κ
                                                                                                                                       0.70
to-modern mappings, contrastive checks, and restoration.                                         90

Both judges directly accept 834 pairs. Manual adjudication
                                                                                                                                       0.65
retains 66 of the remaining 78 and excludes 12, producing                                        85
                                                                                                        ix  re  n. on rity rall
                                                                                                     g F tu Ge ati     u   e
900 tasks. Figure 6 reports each judge’s rate, direct joint                                        Bu Fea Test Migr Sec Ov

acceptance, and inter-judge agreement; 92.7% of the final
   1                                                               Figure 6: Semantic                                                             Figure 7: Environment
     Weights allocate 76% to implementation footprint and 24% to
verification surface. Appendix F reports component values and an   alignment audit by task                                                        savings from modern-base
equal-weight check.                                                family.                                                                        reuse.
Task family        Agent            Model            Original solved (%)   Change2Task solved (%)   ∆ pp   Both solved   Original only   Change2Task only   Neither solved   Agree. (%)    κ
                   Codex CLI        GPT-5.5                 41.0                    42.2            ↑1.2      185             20                26               269            90.8      0.811
                   Claude Code      Sonnet 5                47.0                    48.4            ↑1.4      210             25                32               233            88.6      0.772
Bug Fix
                   Gemini CLI       Gemini 3.1 Pro          24.0                    22.0            ↓2.0      102             18                 8               372            94.8      0.853
                   GitHub Copilot   GPT-5.6 Terra           54.0                    53.0            ↓1.0      240             30                25               205            89.0      0.779
                   Codex CLI        GPT-5.5                 46.0                    44.0            ↓2.0       39             7                  5               49             88.0      0.758
                   Claude Code      Sonnet 5                66.0                    68.0            ↑2.0       58             8                 10               24             82.0      0.593
Feature Addition
                   Gemini CLI       Gemini 3.1 Pro          20.0                    19.0            ↓1.0       17             3                  2               78             95.0      0.841
                   GitHub Copilot   GPT-5.6 Terra           50.0                    54.0            ↑4.0       43             7                 11               39             82.0      0.640
                   Codex CLI        GPT-5.5                 55.0                    57.0            ↑2.0       50             5                 7                38             88.0      0.757
                   Claude Code      Sonnet 5                36.0                    40.0            ↑4.0       31             5                 9                55             86.0      0.703
Test Generation
                   Gemini CLI       Gemini 3.1 Pro          24.0                    20.0            ↓4.0       19             5                 1                75             94.0      0.826
                   GitHub Copilot   GPT-5.6 Terra           48.0                    50.0            ↑2.0       42             6                 8                44             86.0      0.720
                   Codex CLI        GPT-5.5                 60.0                    55.0            ↓5.0       52             8                  3               37             89.0      0.776
                   Claude Code      Sonnet 5                45.0                    48.0            ↑3.0       39             6                  9               46             85.0      0.699
API Migration
                   Gemini CLI       Gemini 3.1 Pro          12.0                    11.0            ↓1.0       10             2                  1               87             97.0      0.853
                   GitHub Copilot   GPT-5.6 Terra           42.0                    47.0            ↑5.0       36             6                 11               47             83.0      0.657
                   Codex CLI        GPT-5.5                 35.0                    30.0            ↓5.0       28             7                  2               63             91.0      0.795
                   Claude Code      Sonnet 5                55.0                    51.0            ↓4.0       46             9                  5               40             86.0      0.719
Security Repair
                   Gemini CLI       Gemini 3.1 Pro          10.0                    8.0             ↓2.0        8             2                  0               90             98.0      0.878
                   GitHub Copilot   GPT-5.6 Terra           44.0                    48.0            ↑4.0       37             7                 11               45             82.0      0.638


Table 2: Matched outcomes between the Original and Change2Task branches. Arrows show the direction of the solve-rate
difference. Gray intensity indicates relative solve performance within each task family.


                               One Base Shared Modern                                                construction and historical preparation combine when either
Metric                         per Task     Bases                                 Effect             route alone is insufficient.
Bases prepared               900                                388 56.9% fewer                         Prior systems report costs over different outputs and ac-
Tasks per base              1.00                               2.32      2.32×                       counting boundaries (Yang et al. 2025b; Fu et al. 2026; Chen
Total setup time         3,240 h                            1,349 h 58.4% less                       et al. 2026), so our cost conclusion uses the matched inter-
Setup time per task       3.60 h                             1.50 h 58.4% less                       nal comparison. Reuse lowers expenditure from $1,917 to
Total retained storage 5,580 GB                           1,607 GB 71.2% less                        $1,710. The $207 saving equals $0.23 per task and a 10.8%
Storage per task        6.20 GB                            1.79 GB 71.2% less                        net reduction, including additional automation and Agent
                                                                                                     Reconstruction expense. Appendix H gives the accounting
Table 3: Environment resources with separate and shared                                              breakdown.
modern bases.                                                                                           RepoLaunch supplies a complementary path when modern
                                                                                                     reconstruction is unavailable. It makes another 195 histori-
                                                                                                     cal revisions executable, raising coverage from 900 to 1,095
therefore does not systematically favor one branch, configu-                                         of 1,130 cases, or 96.9%, and leaving 35 unresolved. It is
ration, or task family.                                                                              an environment-preparation complement rather than a task-
RQ3 Finding. Change2Task-generated tasks retain the                                                  construction baseline.
comparative evaluation signal of their historical anchors                                            RQ4 Finding. Change2Task turns executable repositories
across heterogeneous coding agents.                                                                  into reusable task infrastructure and complements histori-
                                                                                                     cal environment preparation when modern reconstruction is
RQ4: How Effectively Does Change2Task Reuse                                                          unavailable.
Executable Repository Environments?
RQ4 measures the systems benefit of deriving multiple final-                                                               Conclusion and Outlook
ized tasks from a healthy modern base. The matched baseline                                          We introduced Change2Task, a history-grounded frame-
prepares and retains one environment for each of 900 tasks.                                          work that reconstructs merged PRs as executable coding-
Change2Task instead prepares 388 healthy modern bases                                                agent tasks on healthy descendant revisions. Its three adaptive
and reuses them across associated variants while accounting                                          construction routes and lifecycle, scope, and fidelity checks
for task-specific materialization and verification. Both condi-                                      transfer developer-grounded tasks onto maintained code.
tions use the same hardware, retention period, and accounting                                        Across five task families, Change2Task finalizes 900 of
rules.                                                                                               1,130 eligible changes, improves matched Bug Fix recovery
   Table 3 contrasts rebuilding an environment for every task                                        by 29.2%, and produces tasks with 0.894 source change pro-
with reusing 388 healthy modern bases. Reuse lowers amor-                                            file fidelity and up to 98.0% matched agent-outcome agree-
tized environment time from 3.60 h to 1.50 h and storage from                                        ment. Modern-base reuse also reduces environment time by
6.20 GB to 1.79 GB per task. Figure 7 reports family-level                                           58.4% and storage by 71.2%. These savings enable more ef-
reductions. Bug Fix achieves the greatest reuse and savings;                                         ficient and lower-cost coding-agent training and executable
API Migration currently maps each task to a distinct base                                            task-data construction.
and benefits less.                                                                                      Future work will extend Change2Task to more task fam-
   Benefits depend on reuse density: families placing several                                        ilies, languages, and build systems. We will improve oracle
tasks on one maintained base save more than those using dis-                                         generation as tests and APIs evolve, and support task trans-
tinct bases. Matched hardware, prices, and retention isolate                                         fer across forks, successor projects, and related dependency
this reuse effect, while RepoLaunch shows how modern re-                                             ecosystems through traceable interface mappings. We will
also repeat paired evaluations across model releases. To-           Guo, L.; Wang, Y.; Li, C.; Tao, W.; Yang, P.; Chen, J.; Song,
gether, these extensions will expand the historical changes         H.; Tang, D.; and Zheng, Z. 2026b. SWE Data Construc-
that can become current executable data for agent training          tion, Automatically! Proceedings of the ACM on Software
and continuous evaluation.                                          Engineering, 3(FSE): 525–546.
                                                                    Hu, R.; Peng, C.; Wang, X.; Xu, J.; and Gao, C. 2025.
                        References                                  Repo2Run: Automated Building Executable Environment for
                                                                    Code Repository at Scale. In Advances in Neural Information
Arora, A.; Jang, J.; and Moghaddam, R. Z. 2025. Setup-
                                                                    Processing Systems, volume 38.
Bench: Assessing Software Engineering Agents’ Ability to
Bootstrap Development Environments. arXiv:2507.09063.               Islam, M.; Jha, A. K.; Nadi, S.; and Akhmetov, I. 2023.
                                                                    PyMigBench: A Benchmark for Python Library Migration.
Badertdinov, I.; Golubev, A.; Nekrashevich, M.; Shevtsov,           In Proceedings of the 20th IEEE/ACM International Confer-
A.; Karasik, S.; Andriushchenko, A.; Trofimova, M.; Litv-           ence on Mining Software Repositories, 511–515.
intseva, D.; and Yangel, B. 2025. SWE-rebench: An Au-
tomated Pipeline for Task Collection and Decontaminated             Jain, N.; Singh, J.; Shetty, M.; Zhang, T.; Zheng, L.; Sen,
Evaluation of Software Engineering Agents. In Advances in           K.; and Stoica, I. 2025. R2E-Gym: Procedural Environment
Neural Information Processing Systems, volume 38.                   Generation and Hybrid Verifiers for Scaling Open-Weights
                                                                    SWE Agents. In Second Conference on Language Modeling.
Bui, Q.-C.; Scandariato, R.; and Díaz Ferreyra, N. E.               Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; Pei, K.; Press,
2022. Vul4J: A Dataset of Reproducible Java Vulnerabilities         O.; and Narasimhan, K. 2024. SWE-bench: Can Language
Geared Towards the Study of Program Repair Techniques.              Models Resolve Real-World GitHub Issues? In The Twelfth
In Proceedings of the 19th IEEE/ACM International Confer-           International Conference on Learning Representations.
ence on Mining Software Repositories, 464–468.
                                                                    Just, R.; Jalali, D.; and Ernst, M. D. 2014. Defects4J: A
Cao, R.; Chen, M.; Chen, J.; Cui, Z.; Feng, Y.; Hui, B.; Jing,      Database of Existing Faults to Enable Controlled Testing
Y.; Li, K.; Li, M.; Lin, J.; Ma, Z.; Shum, K.; Wang, X.;            Studies for Java Programs. In Proceedings of the 2014 In-
Wei, J.; Yang, J.; Zhang, J.; Zhang, L.; Zhang, Z.; Zhao, W.;       ternational Symposium on Software Testing and Analysis,
and Zhou, F. 2026. Qwen3-Coder-Next Technical Report.               437–440.
arXiv:2603.00729.
                                                                    Le, T.; Thai, M. V. T.; Nguyen Manh, D.; Phan Nhat, H.;
Chen, M.; Zhang, L.; Feng, Y.; Wang, X.; Zhao, W.; Cao,             and Bui, N. D. Q. 2025. SWE-EVO: Benchmarking Cod-
R.; Yang, J.; Chen, J.; Li, M.; Ma, Z.; Ge, H.; Zhang, Z.;          ing Agents in Long-Horizon Software Evolution Scenarios.
Cui, Z.; Liu, D.; Zhou, J.; Sun, J.; Lin, J.; and Hui, B. 2026.     arXiv:2512.18470.
SWE-Universe: Scale Real-World Verifiable Environments              Li, J.; Jin, Z.; Men, T.; Hao, Y.; Zhu, K.; Wang, L.; Huang,
to Millions. arXiv:2602.02361.                                      D.; Wang, L.; Hua, S.; Wang, L.; Gao, J.; Yuan, H.; Xu,
Deng, X.; Da, J.; Pan, E.; He, Y. Y.; Ide, C.; Garg, K.; Lauffer,   R.; Liu, K.; and Zhao, J. 2026a. Agentic Environment En-
N.; Park, A.; Pasari, N.; Rane, C.; Sampath, K.; Krishnan, M.;      gineering for Large Language Models: A Survey of Envi-
Kundurthy, S.; Hendryx, S.; Wang, Z.; Bharadwaj, V.; Holm,          ronment Modeling, Synthesis, Evaluation, and Application.
J.; Aluri, R.; Zhang, C. B. C.; Jacobson, N.; Liu, B.; and Ken-     arXiv:2606.12191.
stler, B. 2025. SWE-Bench Pro: Can AI Agents Solve Long-            Li, K.; Li, R.; Zhang, L.; Jin, Q.; Zhu, L.; Huang, X.; Zhang,
Horizon Software Engineering Tasks? arXiv:2509.16941.               G.; Zhang, Y.; He, S.; Xie, C.; Zhang, X.; Jin, Z.; Li, B.;
Eliseeva, A.; Kovrigin, A.; Kholkin, I.; Bogomolov, E.; and         Zhang, C.; Kang, Y.; Huang, Y.; Nallipogu, E.; Rajmohan,
Zharov, Y. 2025. EnvBench: A Benchmark for Automated                S.; Lin, Q.; and Zhang, D. 2026b. RepoLaunch: Automating
Environment Setup. In ICLR 2025 Workshop on Deep Learn-             Build and Management of Code Repositories across Lan-
ing for Code.                                                       guages and Platforms. arXiv:2603.05026.
Fu, D.; Wu, S.; Wu, Y.; Peng, Z.; Huang, Y.; Sun, J.; Zeng, J.;     Li, W.; Zhang, X.; Guo, Z.; Mao, S.; Luo, W.; Peng, G.;
Jiang, M.; Zhang, L.; Li, Y.; Hu, J.; Liu, L.; Hou, J.; and Liu,    Huang, Y.; Wang, H.; and Li, S. 2025. FEA-Bench: A Bench-
P. 2026. daVinci-Env: Open SWE Environment Synthesis at             mark for Evaluating Repository-Level Code Generation for
Scale. arXiv:2603.13023.                                            Feature Implementation. In Proceedings of the 63rd An-
                                                                    nual Meeting of the Association for Computational Linguis-
GLM-5 Team. 2026. GLM-5: from Vibe Coding to Agentic                tics (Volume 1: Long Papers), 17160–17176. Association for
Engineering. arXiv:2602.15763.                                      Computational Linguistics.
Guan, H.; Fu, L.; Zhang, S.; Zhu, Y.; Zhang, K.; Qiu, L.;           Mündler, N.; Müller, M. N.; He, J.; and Vechev, M. 2024.
Cai, X.; Cao, X.; Liu, W.; Zhang, W.; and Yu, Y. 2026.              SWT-Bench: Testing and Validating Real-World Bug-Fixes
SWE-Cycle: Benchmarking Code Agents across the Com-                 with Code Agents. In Advances in Neural Information Pro-
plete Issue Resolution Cycle. arXiv:2605.13139.                     cessing Systems, volume 37, 81857–81887.
Guo, C.; Wu, J.; He, S.; Chen, Y.; Kuang, Z.; Fan, S.; Chen,        Pan, J.; Wang, X.; Neubig, G.; Jaitly, N.; Ji, H.; Suhr, A.;
B.; Bao, S.; Liu, J.; Wu, H.; Zhu, Q.; Che, W.; and Wang, H.        and Zhang, Y. 2025. Training Software Engineering Agents
2026a. MEnvAgent: Scalable Polyglot Environment Con-                and Verifiers with SWE-Gym. In Proceedings of the 42nd
struction for Verifiable Software Engineering. In Interna-          International Conference on Machine Learning, volume 267,
tional Conference on Machine Learning. Spotlight paper.             47717–47737. PMLR.
Pham, M. V. T.; Phan, H. N.; Phan, H. N.; Le, C. C.; Nguyen,      Issue Resolving. In Advances in Neural Information Pro-
T. N.; and Bui, N. D. Q. 2026. Synthetic Repo-Level Bug           cessing Systems, volume 38.
Dataset for Training Automated Program Repair Models. In          Zhang, L.; He, S.; Zhang, C.; Kang, Y.; Li, B.; Xie, C.; Wang,
Proceedings of the 48th IEEE/ACM International Confer-            J.; Wang, M.; Huang, Y.; Fu, S.; Nallipogu, E.; Lin, Q.; Dang,
ence on Software Engineering.                                     Y.; Rajmohan, S.; and Zhang, D. 2025. SWE-bench Goes
Wang, J. A.; Wang, K.; and Nie, P. 2026. TestEvo-Bench:           Live! In Advances in Neural Information Processing Systems,
An Executable and Live Benchmark for Test and Code Co-            volume 38. Datasets and Benchmarks Track.
Evolution. arXiv:2607.02469.                                      Zhang, Y.; Ruan, H.; Fan, Z.; and Roychoudhury, A. 2024.
Wang, L.; Ramalho, L.; Celestino, A.; Pham, P. A.; Liu, Y.;       AutoCodeRover: Autonomous Program Improvement. In
Sinha, U. K.; Portillo, A.; Osunwa, O.; and Maduekwe, G.          Proceedings of the 33rd ACM SIGSOFT International Sym-
2025a. SWE-Bench++: A Framework for the Scalable Gen-             posium on Software Testing and Analysis.
eration of Software Engineering Benchmarks from Open-             Zhou, Q.; Zhang, J.; Wang, H.; Hao, R.; Wang, J.; Han,
Source Repositories. arXiv:2512.17419.                            M.; Yang, Y.; Wu, S.; Pan, F.; Fan, L.; Tu, D.; and Zhang,
Wang, X.; Li, B.; Song, Y.; Xu, F. F.; Tang, X.; Zhuge,           Z. 2026. FeatureBench: Benchmarking Agentic Coding for
M.; Pan, J.; Song, Y.; Li, B.; Singh, J.; Tran, H. H.; Li, F.;    Complex Feature Development. In International Conference
Ma, R.; Zheng, M.; Qian, B.; Shao, Y.; Muennighoff, N.;           on Learning Representations.
Zhang, Y.; Hui, B.; Lin, J.; Brennan, R.; Peng, H.; Ji, H.; and
Neubig, G. 2025b. OpenHands: An Open Platform for AI
Software Developers as Generalist Agents. In The Thirteenth
International Conference on Learning Representations.
Wei, Z.; Zeng, J.; Wen, M.; Yu, Z.; Cheng, K.; Zhu, Y.; Guo,
J.; Zhou, S.; Yin, L.; Su, X.; and Ma, Z. 2025. PATCHEVAL:
A New Benchmark for Evaluating LLMs on Patching Real-
World Vulnerabilities. arXiv:2511.11019.
Wu, Y.; Jiang, N.; Pham, H. V.; Lutellier, T.; Davis, J.; Tan,
L.; Babkin, P.; and Shah, S. 2023. How Effective Are Neural
Networks for Fixing Security Vulnerabilities. In Proceedings
of the 32nd ACM SIGSOFT International Symposium on
Software Testing and Analysis, 1282–1294.
Xia, C. S.; Deng, Y.; Dunn, S.; and Zhang, L. 2025. Demys-
tifying LLM-Based Software Engineering Agents. Proceed-
ings of the ACM on Software Engineering, 2(FSE): 801–824.
Yang, J.; Jimenez, C. E.; Wettig, A.; Lieret, K.; Yao, S.;
Narasimhan, K.; and Press, O. 2024. SWE-agent: Agent-
Computer Interfaces Enable Automated Software Engineer-
ing. In Advances in Neural Information Processing Systems,
volume 37, 50528–50652.
Yang, J.; Jimenez, C. E.; Zhang, A. L.; Lieret, K.; Yang,
J.; Wu, X.; Press, O.; Muennighoff, N.; Synnaeve, G.;
Narasimhan, K. R.; Yang, D.; Wang, S. I.; and Press, O.
2025a. SWE-bench Multimodal: Do AI Systems Generalize
to Visual Software Domains? In The Thirteenth International
Conference on Learning Representations.
Yang, J.; Lieret, K.; Jimenez, C. E.; Wettig, A.; Khandpur,
K.; Zhang, Y.; Hui, B.; Press, O.; Schmidt, L.; and Yang,
D. 2025b. SWE-smith: Scaling Data for Software Engineer-
ing Agents. In Advances in Neural Information Processing
Systems, volume 38. Datasets and Benchmarks Spotlight.
Yang, Z.; Wang, S.; Fu, K.; He, W.; Xiong, W.; Liu, Y.; Miao,
Y.; Gao, B.; Wang, Y.; Ma, Y.; Li, Y.; Liu, Y.; Hu, Z.; Zhang,
K.; Wang, S.; Chen, H.; Sung, F.; Liu, Y.; Gao, Y.; Yang, Z.;
and Liu, T. 2025c. Kimi-Dev: Agentless Training as Skill
Prior for SWE-Agents. arXiv:2509.23045.
Zan, D.; Huang, Z.; Liu, W.; Chen, H.; Xin, S.; Zhang, L.;
Liu, Q.; Li, A.; Chen, L.; Zhong, X.; Liu, S.; Xiao, Y.; Chen,
L.; Zhang, Y.; Su, J.; Liu, T.; Long, R.; Ding, M.; and Xiang,
L. 2025. Multi-SWE-bench: A Multilingual Benchmark for
                       Appendix                                         Task family       Source corpus                 Cases
                                                                        Bug Fix           SWE-bench Live                 129
A     Limitations                                                       Bug Fix           SWE-bench Lite                  30
Change2Task reconstructs changes along the lineage of                   Bug Fix           SWE-Bench Pro                  101
their source repository. This setting requires a traceable              Bug Fix           SWE-bench Original             151
source PR, an identifiable behavior, executable checks, and             Bug Fix           SWE-bench Verified              89
a healthy descendant that still hosts the behavior. Changes             Feature Addition FEA-Bench                        30
whose behavior has disappeared from the maintained code,                Feature Addition SWE-rebench V2 PRs               68
and changes without a stable modern execution path, remain              Feature Addition SWE-Bench++                       2
outside the construction-eligible pool. The reported recov-
                                                                        Test Generation   SWE-bench Live                  20
ery rates characterize changes that satisfy these evidence and
                                                                        Test Generation   SWE-bench Lite                   2
readiness conditions.                                                   Test Generation   SWE-bench Verified              39
   Lifecycle qualification depends on executable target and             Test Generation   SWE-Bench Pro                    5
regression checks. Repositories with sparse, unstable, or               Test Generation   SWE-bench Original              34
platform-specific checks provide a narrower observable be-
                                                                        API Migration     PyMigBench                     100
havior surface and are less likely to reach construction eli-
gibility. Additional project-specific oracles are required for          Security Repair   PatchEval executable subset     84
maintenance obligations expressed primarily through per-                Security Repair   Vul4J                           15
formance, distributed service interactions, user interfaces, or         Security Repair   VJBench                          1
hardware behavior.                                                      Table 5: Provenance of the paired evaluation sets.
   The evaluation covers five task families drawn from public
Python and Java software corpora and four coding agent con-       C     Construction and Validation Protocol
figurations. Other maintenance families, languages, reposi-
tory structures, and agent interfaces may exhibit different       C.1    Modern Base Selection
reconstruction and solving behavior. Environment savings          Change2Task selects a base within the upstream lineage of
also depend on the number of task variants supported by           the source PR. It resolves a declared healthy revision first,
each healthy modern base, along with the compute prices,          followed by a declared target revision and the repository’s
storage policies, and retention period used by an organiza-       remote default revision. If the default cannot be resolved, it
tion. Section H reports the matched accounting boundary           tries the main, master, devel, develop, and trunk branches in
used in this study.                                               that order. The historical base revision is the final fallback.
                                                                  We tag these fallbacks separately and exclude them from
B     Corpus and Task Provenance                                  the descendant modern bases used in the environment reuse
B.1    Eligibility Funnel                                         analysis.
The main paper defines recovery over 1,130 construction-             Before freezing the resolved commit hash, Change2Task
eligible changes. Table 4 reports the preceding data readi-       requires a clean checkout, available runtime dependencies
ness stages. A source pull request (PR) enters the eligible       and services, collectable mapped checks, passing target and
set after its evidence, executable checks, same-repository        regression checks on the healthy state, a surviving modern
modern base, behavior alignment, and task specification are       host for the PR behavior, and a permitted transformation
complete enough for controlled construction. These stages         surface. The first eligible resolution is frozen before con-
use automatic or rule-based filters and are completed before      struction, preventing post-hoc base selection.
construction and agent evaluation.
                                                                  C.2    Code Mapping and Agent Reconstruction
             Stage                         Cases                  Level 2: Code Mapping uses a unique source-block corre-
             Raw source records            1,783                  spondence. It extracts consecutive edit groups from non-test
             Evidence-qualified            1,521                  source hunks. Removed lines form the historical pre-change
             Runnable modern base          1,233                  block, and added lines form the post-change block. Pure ad-
             Behavior and check aligned    1,197                  ditions, pure deletions, import-only changes, and missing
             Construction-eligible         1,130                  modern files are outside this route. Algorithm 1 summarizes
             Construction-verified           912                  the conservative configuration used in our study.
             Finalized task                  900                     The optional abstract syntax tree fallback matches a whole
Table 4: Candidate funnel from raw source records to final-       function by an identical qualified name and reparses the re-
ized tasks.                                                       sulting file. The reported conservative configuration disables
                                                                  this fallback to preserve modern logic outside the uniquely
B.2    Task Provenance                                            matched block. Code Mapping handles indentation and local
Table 5 reports the provenance of the 900 paired evalua-          context drift. Renamed or relocated symbols, split or merged
tion sets. Each Original Branch is the official case from the     functions, repeated target blocks, and behavior moved across
listed source, and its Change2Task Branch is reconstructed        abstraction layers require Level 3: Agent Reconstruction.
from that same case. The task families include Application           Agent Reconstruction receives the historical PR evidence,
Programming Interface (API) Migration.                            the modern behavior host and call context, task checks, pro-
 Algorithm 1: Level 2: Code Mapping                                C.4    Fidelity Gate
 Input: source patch Ps , healthy modern base H                    The fidelity gate compares the historical source patch Ps
 Output: task patch D, or Fail                                     and modern restoration patch G across files, hunks, changed
                                                                   lines, symbols, target checks, and regression checks. Both
 1. E ← paired pre-change and post-change blocks from
                                                                   patches encode the forward maintenance change, while task
    eligible source hunks.
                                                                   patch D constructs the task state in the inverse direction. The
 2. for each (b− , b+ , p) ∈ E do                                  six fidelity weights are 0.18, 0.20, 0.28, 0.10, 0.12, and 0.12.
 3. f ← resolve p, then its source-directory variant, in H.        The gate requires an aggregate score of at least 0.65, line,
 4. if f is unresolved then return Fail.                           hunk, and file ratios of at least 0.50, a line ratio no greater
 5. L ← exact occurrences of b+ in f .                             than 2.50, and a regression-check ratio of at least 0.25. These
 6. if |L| ̸= 1 then L ← indentation-normalized occur-             thresholds reject localized simplifications, over-expanded ed-
    rences of b+ .                                                 its, and insufficient regression surfaces. The equal-weight
                                                                   sensitivity analysis is reported in Section F.
 7. if |L| ̸= 1 then return Fail.
 8. Reindent b− to the unique location in L.                       D     Prompts and Agent Configuration
 9. Replace b+ with the reindented b− .                            D.1    Agent Execution Protocol
10. end for                                                        Agent Reconstruction uses Claude Code with Opus 4.8 and
11. Reparse modified files and compute D = diff(H, H ′ ).          bounded execution feedback. Evaluation uses the Codex
12. if D is empty, invalid, or touches a protected artifact then   command line interface (CLI) with GPT-5.5, Claude Code
    return Fail.                                                   with Sonnet 5, Gemini CLI with Gemini 3.1 Pro, and GitHub
13. return D.                                                      Copilot with GPT-5.6 Terra. Each agent, set, and branch re-
                                                                   ceives one authoritative clean run with a limit of 1,800 sec-
                                                                   onds. Final verification has a 300-second limit. Infrastructure
 tected regression checks, the source change profile, and prior    failures are rerun separately and do not replace completed
 failure evidence. Scoped diff generation handles bounded          behavioral outcomes.
 code contexts, while full-agent worktree editing supports            Within each pair, the two branches use the same model
 cases that require call-chain inspection. Larger changes can      version, interface, task intent, visible evidence, tool permis-
 enable adaptive multi-candidate generation within the same        sions, context policy, and budgets. A solution is accepted only
 attempt budget. Each candidate first passes non-empty-diff,       when its target and regression checks pass and its changes sat-
 apply, syntax, permitted-artifact, and basic fidelity checks.     isfy the task-specific scope. Evaluation agents cannot access
 Surviving candidates are ranked by source change profile fi-      construction prompts or traces, the task patch, the restoration
 delity and edit complexity, and the highest-ranked candidate      patch, or hidden target checks.
 enters full lifecycle validation. The construction agent re-
 ceives structured feedback for application, target-condition,     D.2    Prompt Templates
 regression, restoration, scope, or fidelity failures. The loop    The following prompts contain the complete instruction-
 terminates after acceptance or at most four attempts. For an      bearing text used by the corresponding stage. Placehold-
 accepted task patch D, the restoration patch G comes from a       ers enclosed by angle brackets are filled from the frozen
 clean inverse modern transformation or a scoped modern re-        task record. Repository files are exposed through an isolated
 pair that passes the same lifecycle and fidelity checks. Cases    worktree, while task evidence and verifier feedback are in-
 without a modern behavior host are rejected.                      serted into the named fields.
                                                                     Agent Reconstruction System Prompt
 C.3    Matched PR Mirror Protocol
 The PR Mirror baseline and Change2Task operate on the               Role and mission. You are the construction agent for
                                                                     Change2Task. Your mission is to reconstruct, in a healthy mod-
 same 621 Bug Fix candidates, healthy modern bases, source
                                                                     ern base, the maintenance condition represented by a historical
 PR evidence, mapped checks, and relevant modern context.            PR. The resulting repository must express the same developer-
 Both use Claude Code with Opus 4.8 under the same to-               facing obligation under the modern implementation. Construct
 tal attempt limit, token and time budgets, tool permissions,        the task state while leaving the maintenance task unresolved.
 and final verifier. Their prompts share the same evidence           Preserve the modern repository structure and avoid a wholesale
 scaffold and output constraints. PR Mirror generates in-            restoration of historical source code.
 dependent one-shot reversal candidates. Each method can             Provided evidence.
 generate at most four candidates. Both receive the same             1. Source request: <issue_or_pr_description>.
 aggregate token and wall-clock budget across those candi-           2. Source change: <historical_implementation_patch>.
 dates. Change2Task can continue with Code Mapping and               3. Modern         base:      an     isolated   worktree      at
 structured verifier feedback when direct reversal fails. This           <healthy_modern_commit>.
 matched protocol holds the candidate pool and execution             4. Behavior mapping: <modern_host_files>, <symbols>,
 envelope fixed while measuring the construction procedures.             and <call_chain>.
 Bug Fix provides the matched comparison because its failure-        5. Verification contract: <target_checks> and <pro-
 inducing reversal, repair output, and test contract align with          tected_regression_checks>.
 the original PR Mirror task definition.
6. Source profile: changed files, hunks, lines, symbols, target     behavior introduced or repaired by the source PR is reversed.
   checks, and regression checks.                                   Retain modern code that is unrelated to the source change,
7. Prior      feedback,       when         present:       <ap-      including later parameters, helpers, wrappers, and adjacent
   ply_or_verification_feedback>.                                   features.
                                                                    Constraints.
Required procedure.
                                                                    1. Produce a source-code patch that applies to the supplied
1. Inspect the mapped files and trace the modern call path             modern revision.
   that implements the source PR’s behavior. Confirm that the
   behavior remains present.                                        2. Modify permitted implementation paths and preserve tests,
                                                                       fixtures, dependencies, build files, and repository metadata.
2. Identify the smallest coherent modern semantic slice whose
   transformation recreates the source maintenance condition.       3. Preserve current interfaces and unrelated behavior.
3. Edit the isolated worktree to construct that condition. Pre-     4. Do not introduce test-specific logic, hard-coded outputs,
   serve modern APIs, signatures, imports, wrappers, caching,          broad exception handling, or unrelated cleanup.
   and behavior introduced after the source PR unless they im-      Return format. Return one unified diff and no explanatory
   plement the target obligation itself.                            prose. This is a one-shot construction prompt. No verifier
4. Review the resulting diff for completeness across affected       feedback or prior candidate is provided. The candidate is eval-
   call sites. Keep the transformation comparable to the source     uated under the same final verifier and execution budget as
   change in files, hunks, changed lines, symbols, and verifi-      Change2Task.
   cation surface.
5. Run focused syntax or build checks that are available within     Coding-Agent Evaluation System Prompt
   the worktree. Leave the final candidate applied for external
                                                                    Mission. Resolve the supplied repository task. Work directly in
   verification.
                                                                    the visible checkout, inspect relevant implementation and tests,
Hard constraints.                                                   execute available commands, and leave a minimal solution in
1. Modify implementation files permitted by <al-                    the worktree.
   lowed_source_paths>.                                             Visible inputs.
2. Preserve tests, fixtures, continuous integration files, gener-   1. task statement: <task_statement>,
   ated files, dependency manifests, lock files, and repository     2. repository checkout: <branch_workspace>,
   metadata.                                                        3. visible source code, tests, documentation, and repository
3. Preserve protected adjacent behavior and current public              tools, and
   interfaces.                                                      4. task-family output contract: <output_contract>.
4. Do not add test-specific branches, hard-coded expected val-      Execution protocol.
   ues, broad exception handling, dead code, stubs, or unre-        1. Reproduce or localize the requested behavior using repos-
   lated deletions.                                                     itory evidence.
5. Do not collapse a multi-site obligation into one local short-    2. Inspect the relevant call path before editing.
   cut or expand the task through unrelated refactoring.            3. Implement the smallest complete change that satisfies the
Final response. Return a concise CONSTRUCTION_REPORT                    task.
containing the modified files, the behavioral slice recon-          4. Run focused checks, then broader repository checks when
structed, the expected target effect, the protected behavior, and       feasible.
the checks executed. The authoritative output is the clean uni-     5. Review the final diff for scope, completeness, and acciden-
fied diff left in the worktree.                                         tal changes.
Feedback rounds. If a previous candidate failed, use the sup-
plied failure category and evidence to revise the transforma-       Task-family contracts.
tion. Application errors identify the rejected hunk and modern      1. Bug Fix: repair the described defect while preserving pass-
location. Target failures identify the unmet task condition. Re-        ing behavior.
gression failures identify protected checks. Fidelity feedback      2. Feature Addition: implement the requested behavior and
reports files, hunks, lines, symbols, and ratios. Scope feedback        its integration with the existing interface.
identifies forbidden artifacts. Remove the previous transforma-     3. Test Generation: add tests that exercise the requested be-
tion before producing the next candidate.                               havior. The accepted patch is restricted to test artifacts.
                                                                    4. API Migration: replace obsolete source API usage with
Matched PR Mirror Baseline Prompt                                       the target API and preserve externally observable behavior.
                                                                    5. Security Repair: remove the vulnerable behavior while
Role. You are given a historical PR patch and the correspond-
                                                                        preserving valid functionality under the supplied security
ing files from a healthy modern base of the same repository.
                                                                        oracle.
Generate one candidate patch that reverses the PR’s change in
the modern code.                                                    Acceptance condition. The final repository state must sat-
Inputs.         <source_request>,          <historical_patch>,      isfy hidden target checks, protected regression checks, and the
<aligned_modern_files>, <allowed_source_paths>, and                 task-specific scope contract. Construction traces, task patches,
<target_and_regression_checks>.                                     restoration patches, and hidden checks are unavailable during
Task. Read the historical diff together with the complete mod-      the run.
ern file context. Rewrite each affected modern file so that the     Final response. Summarize the implemented change and the
                                                                    checks run. The authoritative answer is the final worktree diff.
    Semantic-Alignment Judge Prompt                                   Family             Eligible    Finalized     Rejected     Recovery [95% CI]
                                                                      Bug Fix                621          500          121         80.5 [77.2, 83.4]
    Role. Act as an independent judge of whether a reconstructed      Feature Addition       122          100           22         82.0 [74.2, 87.8]
    modern task preserves the maintenance intent of its historical    Test Generation        126          100           26         79.4 [71.5, 85.5]
    source task. Base the comparison on behavioral obligations.       API Migration          131          100           31         76.3 [68.4, 82.8]
                                                                      Security Repair        130          100           30         76.9 [69.0, 83.3]
    Ignore textual patch similarity and implementation style.
    Historical     record.     <historical_request>,     <histori-    Overall              1,130          900          230         79.6 [77.2, 81.9]
    cal_trigger>, <historical_expected_behavior>, <histor-                      Table 6: Finalized task recovery by family.
    ical_invariant>, <historical_affected_api>, and <histori-
    cal_checks>.                                                           Family                   Level 1      Level 2      Level 3   Total
    Modern record. <modern_task_statement>, <mod-
    ern_trigger>,                  <modern_expected_behavior>,             Bug Fix                      63          106          331      500
    <modern_invariant>,                  <modern_affected_api>,            Feature Addition              1           25           74      100
    <source_to_modern_mapping>,            <contrastive_checks>,           Test Generation              12           17           71      100
    and <restoration_behavior>.                                            API Migration                10           24           66      100
    Decision procedure.                                                    Security Repair               9           18           73      100
    1. Compare the user-visible trigger and precondition.                  Overall                      95          190          615      900
    2. Compare the expected observable behavior and violated               Table 7: Construction routes among finalized tasks.
       invariant.
    3. Check whether API or symbol changes are justified by          because the historical and reconstructed tasks were not se-
       repository evolution.                                         mantically aligned with sufficient confidence.
    4. Use positive, negative, boundary, adjacent, and restoration
       checks to detect weakened or shifted obligations.             F     Source Change Profile and Semantic
    5. Assign exactly one label: exact intent match, intent-               Alignment
       preserving adaptation, related but weakened, related but
       shifted, non-equivalent, or insufficient evidence.            F.1     Source Change Profile Components
    Return format. Return one JavaScript Object Nota-                Table 9 reports the component means underlying Figure 5(a)
    tion (JSON) object with fields label, trigger_match,             of the main paper. The macro average gives each task family
    behavior_match, invariant_match, mapping_valid, con-             equal weight. The task-weighted average over all 900 final-
    trastive_evidence, and brief_justification. The construction     ized tasks is 0.894.
    route, construction model, construction trace, profile score,
    candidate ranking, and downstream agent outcomes are not         F.2     Score Distributions
    provided.
                                                                     Table 10 complements the family means with the within-
                                                                     family distribution of finalized-task scores. Median fidelity
E      Verified Task Recovery                                        ranges from .812 to .928, and the interquartile ranges remain
E.1      Recovery by Task Family                                     above each family’s minimum qualification threshold. The
                                                                     broader lower tail for API Migration and Security Repair re-
Table 6 gives the exact denominators and Wilson 95% con-             flects the larger implementation drift accommodated by their
fidence intervals (CIs) used in Figure 4(a) of the main paper.       task specifications. Every finalized task satisfies its declared
Here, finalized denotes tasks that pass every construction and       profile gate.
qualification stage and enter the evaluation corpus.
                                                                     F.3     Fidelity by Construction Level
E.2      Construction Routes
                                                                     Table 11 uses the same construction route assignments re-
Routes are assigned by the first construction procedure that         ported for the first research question and summarizes the
produces a finalized task. Patch Reversal directly accounts for      profile fidelity achieved by each route.
95 tasks. Code Mapping adds 190 tasks whose source blocks              As a sensitivity check, replacing the declared weights with
require modern correspondence, bringing deterministic con-           equal weights yields family scores of .923, .909, .937, .903,
struction to 285 tasks. Agent Reconstruction contributes the         and .851 for Bug Fix, Feature Addition, Test Generation, API
remaining 615 tasks after the two earlier routes are exhausted.      Migration, and Security Repair. The ordering of the five task
The table below reports disjoint route assignments, so each          families is unchanged.
finalized task appears exactly once.
                                                                     F.4     Semantic Alignment Audit
E.3      Terminal Rejection Reasons                                  The semantic audit examines all 912 construction-verified
Each unsuccessful candidate is assigned one terminal rea-            candidates before the downstream corpus is finalized. The
son after all permitted retries. Environment/Preflight denotes       profile gate qualifies the edit and verification surface, and
repository or task readiness failures. Infrastructure/Harness        the semantic audit evaluates the maintenance trigger, obliga-
denotes persistent execution failures after reruns.                  tion, and invariant. For every paired case, the audit records
   The final qualification category combines scope or fidelity       the historical and modern trigger, expected behavior, vio-
failures with semantic review exclusions. Twelve of its 31           lated invariant, affected API, source-to-modern symbol or
cases had passed executable construction but were removed            call-chain mapping, and any semantic-drift justification. The
 Reason                       Bug      Feature       Test    Migration      Security     Total    Family                        Minimum 25th pct. Median 75th pct.
 Environment/Preflight          26            4        3               8           3       44
 Behavior Alignment             18            3        5               2           5       33     Bug Fix                                 .750                  .837              .907               .977
 Candidate Construction         22            5        6               4           5       42     Feature Addition                        .750                  .816              .890               .958
 Lifecycle Validation           23            3        4              11           9       50
 Final Qualification Gate       12            5        5               4           5       31     Test Generation                         .750                  .860              .928               .982
 Infrastructure/Harness         20            2        3               2           3       30     API Migration                           .700                  .776              .884               .949
 Total rejected                121           22       26              31          30      230     Security Repair                         .650                  .732              .812               .902
    Table 8: Mutually exclusive terminal rejection reasons.                                                Table 10: Distribution of weighted fidelity scores.
Family             Cases    Files    Hunks   Lines     Symbols     Target   Regression   Score                      Level 1: Patch Reversal   Level 2: Code Mapping        Level 3: Agent Reconstruction

Bug Fix             500     .928      .855    .832          .920    1.000        1.000    .903   Family             Cases            Score    Cases              Score     Cases                      Score
Feature Addition    100     .920      .884    .810          .840    1.000        1.000    .893   Bug Fix               63            1.000      106               .882          331                     .891
Test Generation     100     .972      .880    .872          .900    1.000        1.000    .925   Feature Addition       1             .990       25               .910           74                     .886
API Migration       100     .935      .860    .820          .800    1.000        1.000    .890   Test Generation       12            1.000       17               .920           71                     .914
Security Repair     100     .900      .800    .680          .726    1.000        1.000    .825   API Migration         10             .970       24               .910           66                     .871
                                                                                                 Security Repair        9             .950       18               .837           73                     .807
Macro average       900     .931      .856    .803          .837    1.000        1.000    .887
                                                                                                 Overall               95             .992      190               .888          615                     .881
Table 9: Mean source change profile fidelity by task family.                                     Table 11: Source change profile fidelity by construction level.
evidence also includes positive triggers, negative or non-                                       is (n01 − n10 )/N , and the exact McNemar test evaluates the
trigger cases, boundary inputs, adjacent invariants, unrelated                                   two discordant cells n10 and n01 .
behavior checks, and restoration checks defined by the task
contract.                                                                                        H         Environment Reuse and Cost Accounting
   Kimi K3 and DeepSeek V4 Pro independently receive an                                          H.1        Family-Level Resource Accounting
anonymized pair containing the historical and modern tasks.
                                                                                                 Table 14 reports the totals underlying Figure 7 of the main pa-
They do not see the construction level, construction model,
                                                                                                 per. The 388 bases are distinct revision-bound environments
construction trace, profile score, candidate ranking, or down-
                                                                                                 in the evaluated corpus. Setup time includes checkout, de-
stream outcome. Each judge assigns one of the following
                                                                                                 pendency and service preparation, build and check discovery,
labels: exact intent match, intent-preserving adaptation, re-
                                                                                                 and healthy-state preflight. Retained storage includes base ar-
lated but weakened, related but shifted, non-equivalent, or
                                                                                                 tifacts and task-specific patches, checks, and metadata, with
insufficient evidence. The first two labels qualify a pair as an
                                                                                                 shared layers counted once. Total shared cost also includes
intent-preserving match.
                                                                                                 task materialization and verification. Storage is reported in
   Both judges independently assign an intent-preserving la-
                                                                                                 gigabytes (GB).
bel to 834 of the 912 audit entrants. Two authors manually ad-
judicate the remaining 78 using the historical maintenance in-                                   Family             Tasks    Bases    Tasks/base       Time      Time/task            Storage   Storage/task
                                                                                                 Bug Fix               500     116            4.31     530 h           1.06 h         495 GB        0.99 GB
tent, behavioral trigger, expected behavior, source-to-modern                                    Feature Addition      100      39            2.56     141 h           1.41 h         162 GB        1.62 GB
mapping, contrastive checks, and restoration behavior. They                                      Test Generation
                                                                                                 API Migration
                                                                                                                       100
                                                                                                                       100
                                                                                                                                49
                                                                                                                               100
                                                                                                                                              2.04
                                                                                                                                              1.00
                                                                                                                                                       163 h
                                                                                                                                                       275 h
                                                                                                                                                                       1.63 h
                                                                                                                                                                       2.75 h
                                                                                                                                                                                      202 GB
                                                                                                                                                                                      406 GB
                                                                                                                                                                                                    2.02 GB
                                                                                                                                                                                                    4.06 GB
accept 66 as exact intent matches or intent-preserving adap-                                     Security Repair       100      84            1.19     240 h           2.40 h         342 GB        3.42 GB

tations and exclude 12. The exclusions arise from shifted                                        Overall               900     388            2.32    1,349 h          1.50 h    1,607 GB           1.79 GB

behavioral triggers, weakened boundary conditions, ambigu-                                        Table 14: Family-level environment resource accounting.
ous source-to-modern mappings, or insufficient contrastive
evidence. The resulting corpus contains 834 + 66 = 900                                           H.2        Monetary Cost Accounting
finalized tasks. Within this corpus, the two judges agree di-                                    We price environment compute at $0.3333 per hour and stor-
rectly on 92.7% of cases. Their direct joint acceptance over                                     age plus registry retention at an effective $0.0484 per GB over
all audit entrants is 91.4%.                                                                     the study period. Automation and model calls cover environ-
                                                                                                 ment preparation and task construction. Execution compute
G        Paired Agent Outcome Statistics                                                         is counted in the environment compute row. Failed construc-
G.1       Paired Agreement Statistics                                                            tion attempts are included in the Change2Task condition.
                                                                                                 Both conditions use the same prices and retention boundary.
Table 13 aggregates the 20 contingency tables formed by                                          The separate-setup condition charges the matched prepara-
four agents and five task families in Table 2 of the main                                        tion and retained-storage components once per task. The
paper. Positive and negative agreement summarize concor-                                         reuse condition charges shared components once per frozen
dance on solved and unsolved outcomes, respectively. The                                         modern base and adds each task-specific variant. Costs are
paired solve-rate interval uses the paired binary-outcome                                        computed from unrounded measurements; the displayed re-
standard error, and the McNemar result is two-sided and                                          source totals and unit prices are rounded.
exact.
   Let n11 , n10 , n01 , and n00 denote both solved, Original                                    Component                         Separate task setup          Reused modern bases             Difference
                                                                                                 Environment compute                           $1,080.00                           $449.67        -$630.33
only, Change2Task only, and neither solved. Raw agree-                                           Storage and registry                            $270.00                            $77.76        -$192.24
ment is (n11 + n00 )/N , and Cohen’s κ adjusts this value                                        Automation and model calls                     $567.00                          $1,182.57        +$615.57
for agreement expected from the two branch marginals. Pos-                                       Total                                         $1,917.00                         $1,710.00        -$207.00
                                                                                                 Cost per finalized task                           $2.13                             $1.90          -$0.23
itive agreement is 2n11 /(2n11 + n10 + n01 ), while negative
agreement replaces n11 with n00 . Solved-set Jaccard overlap                                     Table 15: Matched cost decomposition for 900 finalized
is n11 /(n11 + n10 + n01 ). The paired solve-rate difference                                     tasks.
 Family             Cases   Kimi K3   DeepSeek V4 Pro   Both judges    κ
                                                                              ture, and unrelated fragment creation behavior. The resulting
 Bug Fix             500       96.2              95.8          94.4   .77
 Feature Addition    100       95.0              96.0          92.0   .73
                                                                              task patch spans two implementation files, 11 hunks, and 121
 Test Generation     100       97.0              95.0          93.0   .76     changed lines. The paired restoration patch reintroduces the
 API Migration       100       94.0              93.0          89.0   .69     section-aware behavior in the modern code.
 Security Repair     100       92.0              93.0          88.0   .68     Executable evidence. Four target checks cover explicit selec-
 Overall             900       95.4              95.1          92.7   .74     tion, default selection, interactive selection, and invalid names.
Table 12: Semantic alignment among the 900 finalized tasks.                   Sixteen regression checks protect existing fragment creation
Rates are percentages.                                                        and later command behavior. Target checks follow pass, fail,
                                                                              pass across the healthy, task, and restored states. All regression
      Statistic                                Value                          checks pass in every state.

      Matched agent and task pairs          3,600                              This case captures the central distinction between recon-
      Both solved / Original only / 1,292 / 186 / 186 /                     struction and source checkout. A historical rollback would
      Change2Task only / neither            1,936                           also remove behavior introduced after PR 603. Change2Task
      Raw agreement                         89.7%                           preserves that later behavior and materializes the missing
      Cohen’s κ                             0.787                           feature inside the repository’s current implementation con-
      Positive agreement                    87.4%                           text.
      Negative agreement                    91.2%
      Solved-set Jaccard overlap            77.6%                           I.2   Bug Fix with a Modernized Implementation
      Paired solve-rate difference [95% CI] 0.0 pp [-1.1, 1.1]
      Exact McNemar p-value                 1.0                               Bug Fix Case: Django Migration State
Table 13: Aggregate paired statistics for the third research                  Historical maintenance request. Preserve the Project-
question.                                                                     State.real_apps invariant. The constructor may receive None or
                                                                              a set, and a non-empty value must already satisfy the set con-
H.3        Complementarity with RepoLaunch                                    tract. The historical fix prevents permissive conversion from
                                                                              concealing an invalid caller state.
RepoLaunch prepares the historical repository revision.                       Historical evidence. The source implementation patch
Change2Task reconstructs the task on a healthy modern                         changes seven lines in one file and one hunk. Its target check
base. Across the same 1,130 construction-eligible changes,                    distinguishes a valid set from an invalid collection passed to
both routes succeed on 680 cases, Change2Task alone suc-                      the migration state.
ceeds on 220, RepoLaunch alone succeeds on 195, and                           Healthy modern base. The invariant remains in the evolved
both fail on 35. Change2Task covers 79.6% of the eligible                     migration-state implementation. The surrounding migration
pool. RepoLaunch adds 17.3%, raising combined coverage                        code, imports, and test harness have changed, while the mapped
to 96.9% and leaving 3.1% unresolved.                                         target check and 32 adjacent regression checks pass on the se-
                                                                              lected base.
                                                                              Task shown to the coding agent. “Correct Project-
I      Additional Analyses and Case Studies                                   State.real_apps handling so that the migration state preserves
I.1      Feature Addition Across Repository Evolution                         the documented set invariant without changing valid migration
                                                                              behavior.”
    Feature Addition Case: Towncrier PR 603                                   Constructed task state. Agent Reconstruction restores the
    Historical maintenance request. Add section-aware fragment                earlier permissive conversion in the modern constructor. The
    creation. The command-line interface accepts a section name,              six-line task patch touches one file and one hunk. Its restoration
    validates it against the project configuration, supports inter-           patch reinstates the invariant without changing the modern
    active section selection, and resolves the selected fragment              method signature or adjacent migration logic. The source-to-
    directory through a shared path abstraction.                              modern profile score is .960.
    Historical evidence. The source PR adds the section option, in-           Executable evidence. The target check follows pass, fail, pass
    troduces the section validation path, and centralizes fragment-           across the healthy, task, and restored states. All 32 protected
    directory resolution. Its implementation patch spans four files,          migration checks pass throughout the lifecycle.
    13 hunks, and 160 changed lines.
    Healthy modern base. The selected descendant still im-
                                                                               The case demonstrates that Agent Reconstruction also han-
    plements the section-aware behavior. Its command path has               dles compact maintenance obligations. It retains the histori-
    evolved and now includes later functionality such as the sub-           cal trigger and expected behavior while keeping the modern
    issue option, updated parameter plumbing, and a refactored              edit surface aligned with the seven-line source change.
    path helper. The four mapped target checks pass before con-
    struction.
    Task shown to the coding agent. “Restore section-aware frag-
    ment creation. The command must accept an explicit section,
    support the default and interactive selection paths, and reject
    unknown section names while preserving the current command
    interface.”
    Constructed task state. Agent Reconstruction removes the
    modern semantic slice that implements section selection and
    validation. It preserves sub-issue, the evolved command struc-
