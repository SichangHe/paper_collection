![](_page_0_Picture_1.jpeg)

![](_page_0_Picture_2.jpeg)

![](_page_0_Picture_3.jpeg)

![](_page_0_Picture_4.jpeg)

![](_page_0_Picture_5.jpeg)

![](_page_0_Picture_6.jpeg)

![](_page_0_Picture_7.jpeg)

# **EvoClaw: Evaluating AI Agents on Continuous Software Evolution**

**Gangda Deng**1,\***, Zhaoling Chen**2,\***, Zhongming Yu**<sup>3</sup> **, Haoyang Fan**<sup>1</sup> **, Yuhong Liu**<sup>1</sup> **, Yuxin Yang**<sup>1</sup> **, Dhruv Parikh**<sup>1</sup> **, Rajgopal Kannan**<sup>4</sup> **, Le Cong**<sup>5</sup> **, Mengdi Wang**<sup>6</sup> **, Qian Zhang**<sup>2</sup> **, Viktor Prasanna**<sup>1</sup> **, Xiangru Tang**7,† **, Xingyao Wang**<sup>8</sup> <sup>1</sup>USC <sup>2</sup>UCR <sup>3</sup>UCSD <sup>4</sup>Army Research Office <sup>5</sup>Stanford <sup>6</sup>Princeton <sup>7</sup>Haven <sup>8</sup>OpenHands

- **DeepCommit Pipeline: [github.com/DeepCommit-ai/DeepCommit](https://github.com/DeepCommit-ai/DeepCommit)**
- **EvoClaw Benchmark: [github.com/EvoClaw-Bench/EvoClaw](https://github.com/EvoClaw-Bench/EvoClaw)**
- **Data: [huggingface.co/datasets/EvoClaw-Bench/EvoClaw-data](https://huggingface.co/datasets/EvoClaw-Bench/EvoClaw-data)**
- **Leaderboard: [evo-claw.com](https://evo-claw.com/)**

**With AI agents increasingly deployed as long-running systems, it becomes essential to autonomously construct and continuously evolve customized software to enable interaction within dynamic environments. Yet, existing benchmarks evaluate agents on isolated, one-off coding tasks, neglecting the temporal dependencies and technical debt inherent in real-world software evolution. To bridge this gap, we introduce DeepCommit, an agentic pipeline that reconstructs verifiable Milestone DAGs from noisy commit logs, where milestones are defined as functionally cohesive development goals. These executable sequences enable EvoClaw, a novel benchmark that requires agents to sustain system integrity and limit error accumulation, dimensions of long-term software evolution largely missing from current benchmarks. Our evaluation of 12 frontier models across 4 agent frameworks reveals a critical vulnerability: overall performance scores drop significantly from** >**80% on isolated tasks to at most 38% in continuous settings, exposing agents' profound struggle with long-term maintenance and error propagation.**

<span id="page-0-0"></span>![](_page_0_Figure_16.jpeg)

Figure 1 | Milestone-level task granularity optimally balances functional coherence and evolutionary awareness for benchmarking continuous software evolution.

# **1. Introduction**

Frontier LLM-powered agents (e.g., Claude Code [\(Anthropic,](#page-19-0) [2025\)](#page-19-0), Codex [\(OpenAI,](#page-21-0) [2025\)](#page-21-0)) are increasingly deployed as long-running systems (e.g., OpenClaw [\(OpenClaw,](#page-21-1) [2026\)](#page-21-1) and Hermes [\(Nous](#page-21-2) [Research,](#page-21-2) [2026\)](#page-21-2)) into complex, open-ended environments. To operate effectively in these dynamic settings, such agents must treat their environment-facing interfaces as a maintainable software system—one that requires autonomous development and continuous refinement rather than a fixed, hand-crafted tool. As the agent iteratively adapts to successive requirements from end-users and ongoing environmental feedback, its continuous development efforts accumulate, naturally forming a complete repository evolution history.

<sup>\*</sup>Equal Contribution †Corresponding Author

<span id="page-1-0"></span>Table 1 | Representative software engineering benchmarks for LLMs. Unlike other categories of benchmarks that evaluate agents on isolated snapshots or against ground-truth states at each step, *Repository Evolution* requires agents to continuously build upon their own accumulated development history, exposing them to error propagation across tasks. EvoClaw adopts the *Milestone-level* granularity, a functionally coherent group of commits that collectively advance a development objective, avoiding the noise of individual commits and the excessive scope of full releases. *Dev History* denotes the agent's own development trace accumulated from preceding tasks.

| Category             | Benchmark                              | Language | Task Properties |         |                        | Cross-task    | Task        |
|----------------------|----------------------------------------|----------|-----------------|---------|------------------------|---------------|-------------|
| duregory             |                                        | Zungunge | Granularity     | Avg LoC | Additional Context     | Dependency    | Collection  |
| Function Completion  | HumanEval (Chen et al., 2021)          | Python   | Function-level  | 6.8     | -                      | -             | Manual      |
|                      | SWE-bench (Jimenez et al., 2024)       | Python   | Commit-level    | 32.8    | Codebase               | _             | Rule-based  |
|                      | SWE-rebench (Badertdinov et al., 2026) | Python   | Commit-level    | 142     | Codebase               | _             | Rule-based  |
| Issue Resolution     | Multi-SWE-bench (Zan et al., 2026)     | Multi    | Commit-level    | 246     | Codebase               | _             | Rule-based  |
|                      | SWE-bench Pro (Deng et al., 2025)      | Multi    | Commit-level    | 107     | Codebase               | _             | Rule-based  |
|                      | SWE-CI (Chen et al., 2026)             | Python   | Commit-level    | ~60     | Codebase + Oracle Test | Commit Chain  | Rule-based  |
|                      | SWE-Dev (Du et al., 2026)              | Python   | Feature-level   | 190     | Codebase               | _             | Rule-based  |
|                      | FeatureBench (Zhou et al., 2026)       | Python   | Feature-level   | 790     | Codebase               | _             | Test-driven |
| Codebase Generation  | SWE-EVO (Thai et al., 2025)            | Python   | Release-level   | 611     | Codebase               | _             | Rule-based  |
| Codebase Generation  | Commit0 (Zhao et al., 2025)            | Python   | Project-level   | >3k     | Codebase Skeleton      | _             | Rule-based  |
|                      | NL2Repo (Ding et al., 2026)            | Python   | Project-level   | >3k     | _                      | _             | Rule-based  |
|                      | ProgramBench (Yang et al., 2026)       | Multi    | Project-level   | >8k     | Executable             | -             | Agentic     |
| Repository Evolution | EvoClaw (Ours)                         | Multi    | Milestone-level | 570     | Codebase + Dev History | Milestone DAG | Agentic     |

Yet, evaluation for such long-running agent systems remains largely under-explored. While benchmarks for agents on coding tasks have advanced from isolated function completion (Chen et al., 2021) to full-scale codebase generation (Yang et al., 2026; Zhao et al., 2025) (Table 1), they predominantly treat development as independent tasks (Deng et al., 2025; Jimenez et al., 2024; Zan et al., 2026). A critical dimension remains unaddressed: the temporal structure of software evolution. A true *repository evolution* benchmark must capture the full evolution itinerary—a continuous stream of dependent tasks where early implementation decisions constrain subsequent ones. Ignoring these dependencies allows agents to take expedient shortcuts that satisfy immediate tests but silently accumulate technical debt (Chen et al., 2026; Orlanski et al., 2026), undermining the long-term maintainability of the codebase, a failure mode that remains invisible to current isolated evaluations (Yao, 2025).

To capture these long-term dynamics, our benchmark replays the dependency-rich evolution of high-quality open-source repositories (Badertdinov et al., 2026; Fu et al., 2026; Jain et al., 2025; Pan et al., 2025) as a high-fidelity proxy for the continuous *repository evolution* that *software as a skill* demands. However, determining the appropriate **task granularity** is non-trivial (Figure 1). Intuitively, one might attempt to measure evolution at the **release-level** (Thai et al., 2025). However, this granularity is **too coarse**: release snapshots collapse the hundreds of interdependent commits between versions into a single update, flattening the fine-grained dependency structure that drives evolutionary changes. In contrast, the **commit-level** history (Chen et al., 2026; Jimenez et al., 2024) is **too fine-grained and imbalanced**: many commits are trivial (e.g., typo fixes) while a few are substantive, and the linear commit sequence encodes only chronological apply order, introducing spurious dependencies between unrelated changes (Fan et al., 2024; Herzig et al., 2016).

To address this, we propose modeling software evolution at the **Milestone-level**. We define a milestone as a coherent functional unit that preserves dependency constraints. This granularity strikes a crucial balance: unlike releases, it retains the fine-grained development dependencies and structural evolution of the codebase; unlike commits, it encapsulates realistic and coherent functional goals. Functional dependencies among milestones naturally form a Directed Acyclic Graph (DAG), which captures genuine prerequisite constraints while allowing independent features to proceed in parallel. However, constructing Milestone DAGs requires reordering and grouping commits, which disrupts the native

git history. This poses a severe challenge to correctness: applying reordered patches often breaks **compilation** and **test collection**, jeopardizing the benchmark's executability and realism.

To resolve this, we introduce **DeepCommit**, an automated agentic pipeline that reconstructs *verifiable* software evolution itineraries in the form of *Milestone DAGs*. By synergizing static analysis, LLMagent-driven milestone construction, and runtime validation, DeepCommit ensures the synthesized milestones are executable and testable. Powered by Claude Opus 4.5, it achieves a high average test collection success rate of 87.1%, ensuring comprehensive verification coverage. Designed as a scalable agentic framework, DeepCommit is poised to leverage future LLM advancements to harvest increasingly accurate and extensive evolution itineraries from the vast open-source ecosystem [\(Fu](#page-20-3) [et al.,](#page-20-3) [2026;](#page-20-3) [Jain et al.,](#page-20-4) [2025;](#page-20-4) [Pan et al.,](#page-21-5) [2025\)](#page-21-5).

Building on this foundation, we present **EvoClaw**, a benchmark for evaluating LLM agents under continuous software evolution. EvoClaw comprises 98 human-verified milestones across 7 evolution itineraries (Milestone DAGs), each from a release range of a unique high-impact open-source repository, and spanning five programming languages. Rather than solving independent tasks, agents in EvoClaw are tasked with evolving a codebase through streams of these dependency-constrained milestones, closely mirroring real-world development scenarios. A single full evaluation costs approximately \$500 with frontier models such as Claude Opus 4.5. To achieve a high score in this setting, an agent must maintain long-term context, manage architectural consistency, and prevent error accumulation across extended development horizons.

Using EvoClaw, we conduct a comprehensive evaluation of 4 frontier agent frameworks and 12 state-of-the-art LLMs. We assess performance using a unified **Score** (Section [5.1\)](#page-9-0), which balances **Recall** (completeness of new feature implementation) and **Precision** (robustness against regressions), along with a strict **Resolve Rate** for fully completed milestones. Our evaluation reveals the following key findings regarding agent capabilities in continuous software evolution:

- **A fundamental performance gap: Continuous vs. Independent.** (Section [5.2\)](#page-10-0) Frontier models exhibit a substantial degradation from independent to continuous task evaluation. Scores drop from over ∼80% on isolated tasks to at most 38.03% (Claude Opus 4.6) in continuous environments, with a mere 13.37% Resolve Rate (Gemini 3 Pro).
- **Recall grows linearly but Precision saturates.** We identify a fundamental asymmetry in continuous software evolution (Section [5.4\)](#page-12-0): while frontier agents retain the capability to implement new features (linear Recall growth), they fail to prevent regressions as the system evolves (saturated Precision). This indicates that agents struggle primarily with system-level maintenance rather than local implementation.
- **Accumulated errors stall downstream progress.** Unresolved regressions trigger a "snowball effect" where errors accumulate faster than agents can fix them (Section [5.5\)](#page-14-0). Early bugs propagate through dependency chains to contaminate downstream tasks, eventually stalling development entirely.
- **Proactive exploration and verification mitigate technical debt.** Behavioral analysis shows that successful sustained evolution relies on proactive codebase exploration and disciplined test verification, whereas both blind trial-and-error and the absence of verification accelerate failure (Section [5.6\)](#page-15-0).

# **2. Related Work**

**LLM-Driven Coding Agents**. While basic Bash tools alone can drive an LLM through software tasks [\(Yang et al.,](#page-22-5) [2025\)](#page-22-5), specialized scaffolding is what unlocks reliable, efficient, and user-friendly behavior. Scaffolds have evolved from predefined pipelines [\(Xia et al.,](#page-22-6) [2025\)](#page-22-6) to fully autonomous

systems [\(Wang et al.,](#page-21-6) [2025;](#page-21-6) [Yang et al.,](#page-22-7) [2024\)](#page-22-7). Commercial deployments span complementary use cases: Devin [\(Labs,](#page-20-7) [2024\)](#page-20-7), GitHub Copilot [\(GitHub,](#page-20-8) [2025\)](#page-20-8), Cursor [\(Cursor,](#page-19-5) [2024\)](#page-19-5), Trae [\(TRAE,](#page-21-7) [2025\)](#page-21-7), and Antigravity [\(Google,](#page-20-9) [2025a\)](#page-20-9) integrate agents into IDE and cloud workflows, while Claude Code [\(Anthropic,](#page-19-0) [2025\)](#page-19-0), Codex [\(OpenAI,](#page-21-0) [2025\)](#page-21-0), and Gemini CLI [\(Google,](#page-20-10) [2025b\)](#page-20-10) run in the terminal. While these agents are well-validated on independent, interactive tasks, their reliability under longhorizon, fully autonomous operation remains a formidable challenge. EvoClaw addresses this gap with a standardized, quantitative evaluation that surfaces fine-grained progress-level feedback.

**Automated SWE Environment Synthesis**. A growing line of work automatically constructs testable Dockerized environments from open-source repository snapshots. These environments primarily serve to continuously refresh evaluation data [\(Badertdinov et al.,](#page-19-2) [2026;](#page-19-2) [Zhang et al.,](#page-22-8) [2026\)](#page-22-8) and scale agent training [\(Fu et al.,](#page-20-3) [2026;](#page-20-3) [Jain et al.,](#page-20-4) [2025;](#page-20-4) [Pan et al.,](#page-21-5) [2025\)](#page-21-5). Unlike these snapshotbased approaches, DeepCommit preserves the temporal structure of development trajectories by reorganizing commit histories into Milestone DAGs, thereby synthesizing long-horizon tasks with verifiable progress checkpoints.

**Issue Resolution Tasks**. Unlike Terminal-Bench [\(Merrill et al.,](#page-21-8) [2026\)](#page-21-8), which tests agents on shell commands isolated from any codebase, SWE benchmarks require modifying real-world GitHub repositories. SWE-bench [\(Jimenez et al.,](#page-20-0) [2024\)](#page-20-0) pioneered this line by pairing issues with hidden tests, followed by SWE-bench Pro [\(Deng et al.,](#page-19-3) [2025\)](#page-19-3) for data hygiene and Multi-SWE-bench [\(Zan](#page-22-0) [et al.,](#page-22-0) [2026\)](#page-22-0) for multilingual coverage.

**Codebase Generation Tasks**. Codebase generation benchmarks pursue longer-horizon evaluation by progressively enlarging the scope of a single task. At the feature level, SWE-Dev [\(Du et al.,](#page-20-1) [2026\)](#page-20-1) and FeatureBench [\(Zhou et al.,](#page-22-1) [2026\)](#page-22-1) require agents to implement complete features against curated test suites. At the release level, SWE-EVO [\(Thai et al.,](#page-21-3) [2025\)](#page-21-3) bundles all changes between consecutive release tags into a single task. At the repository level, Commit0 [\(Zhao et al.,](#page-22-2) [2025\)](#page-22-2), NL2Repo [\(Ding et al.,](#page-20-2) [2026\)](#page-20-2), and ProgramBench [\(Yang et al.,](#page-22-3) [2026\)](#page-22-3) push agents toward synthesizing entire repositories from scratch. Despite the enlarged scope, these benchmarks evaluate task instances in isolation on a reset codebase, leaving inter-task dependencies and accumulated technical debt unmodeled. EvoClaw instead links milestones through a dependency DAG over a persistent repository, making both intermediate progress and cross-task error propagation directly measurable.

**Continuous SWE Tasks**. Real software development involves a stream of dependent tasks on the same codebase. While LLMs are known to degrade in this setting relative to single-shot evaluation [\(Laban](#page-20-11) [et al.,](#page-20-11) [2026\)](#page-20-11), dedicated benchmarks remain nascent. SlopCodeBench [\(Orlanski et al.,](#page-21-4) [2026\)](#page-21-4) measures structural erosion and verbosity drift on hand-crafted tasks where an agent extends a codebase built from scratch. A complementary thread evaluates agents via continuous integration (CI) loops on real repositories [\(XU et al.,](#page-22-9) [2026\)](#page-22-9). SWE-CI [\(Chen et al.,](#page-19-4) [2026\)](#page-19-4), for instance, chains commit-to-commit CI rounds by exposing ground-truth tests to a dual-agent protocol following the native commit order. EvoClaw instead adopts a coarser, functionally coherent granularity by grouping commits into selfcontained milestones whose dependencies form a DAG. This approach offers a more faithful and flexible model of continuous software evolution than scattered commit-level CI.

<span id="page-3-0"></span>**Performance Optimization Tasks**. A parallel direction evaluates whether agents can speed up code across repositories [\(He et al.,](#page-20-12) [2025;](#page-20-12) [Ma et al.,](#page-20-13) [2025;](#page-20-13) [Shetty et al.,](#page-21-9) [2026\)](#page-21-9), numerical algorithms [\(Press](#page-21-10) [et al.,](#page-21-10) [2026\)](#page-21-10), and GPU kernels [\(Ouyang et al.,](#page-21-11) [2025\)](#page-21-11). While these works instantiate long-horizon evaluation, they focus on closed-ended optimization objectives, such as wall-clock time against an expert reference. In contrast, EvoClaw addresses the open-ended challenge of general functional software development.

<span id="page-4-0"></span>![](_page_4_Figure_1.jpeg)

Figure 2 | The DeepCommit pipeline architecture. **Phase 1** extracts structured data from commit history through static analysis, including source filtering, commit extraction, PR/Issues, releases, commit DAG, code metrics, and symbol changes. **Phase 2** employs an LLM agent to construct a Milestone DAG via four iterative stages: seed discovery, milestone consolidation, dependency inference, and milestone decomposition. **Phase 3** resolves runtime dependencies through testbed construction and test collection, with DAG refinement and fallback patches as repair strategies, followed by flaky test filtering to produce an executable testbed. **Quality Assurance** validates outputs at textual, compilation, and test collection levels. See Appendix B.4 for all DAG visualizations.

# 3. DeepCommit: An Automated Pipeline for Reconstructing Software Evolution

### 3.1. From Raw Commits to Milestone DAGs

Software repositories encode rich evolutionary trajectories, yet raw commit histories remain noisy, fragmented, and inadequate as executable development sequences. Commits vary widely in granularity, semantic clarity, and dependency structure, while parallel branches, squash merges, and non-functional changes obscure true developmental relationships. Relying on documentation or release notes alone lacks sufficient resolution to reconstruct precise code evolution. DeepCommit addresses this challenge by transforming linear git histories into structured, verifiable *Milestone DAGs*, where each node represents a coherent, testable unit of development and edges encode dependency constraints across evolution phases.

### 3.2. Overall Agent-Driven Pipeline

As illustrated in Figure 2, DeepCommit reconstructs software evolution itineraries through an end-to-end pipeline that sequentially integrates: (1) commit history preprocessing, (2) Milestone DAG construction, and (3) executable environment resolution.

# *3.2.1. Commit History Preprocessing*

We model each repository's main-branch range between release tags as a linear sequence of commits. This linearization aligns naturally with the squash-and-merge workflow, the most widely adopted convention in actively-maintained, high-quality repositories, where each main-branch commit maps to a Pull Request (PR) or Issue together with its internal sub-commits. We collect all main-branch commits and their PR, Issue, and Release metadata. An LLM agent then prepares a per-repo configuration of source directories, test patterns, and exclusion rules that separates product-logic source from test code and filters out commits touching only non-source files such as docs, CI configs, and build assets (Appendix [A.1\)](#page-23-0). To enable downstream milestone discovery and dependency inference, we extract three structural signals via static analysis: (i) a commit-level DAG built with git blame to capture line-level textual dependencies, (ii) symbol-level modifications identifying changes in classes and functions, and (iii) file-level co-change statistics reflecting evolutionary coupling.

# *3.2.2. Milestone DAG Construction*

Organizing hundreds of discrete commits into functionally coherent milestones requires integrating structural dependencies with code-level reasoning. We employ a four-stage LLM-agent-driven process to progressively construct the Milestone DAG. Each stage is orchestrated with automated data preparation, agent-accessible validation tools, and a post-stage quality gate. A stage runs in a forward pass and may iterate internally against its self-checks. At stage boundaries, the pipeline can also fan out into multiple parallel instantiations of the next stage and retain the variant that best satisfies the downstream quality gate.

**Seed Discovery.** Each milestone is initiated by a *seed commit*, namely a foundational anchor that introduces a distinct development theme. An LLM agent identifies such seeds by jointly evaluating commit semantics (commit messages and linked discussion context) and structural signals (DAG topology, including out-degree and descendant count), filtering out cosmetic edits, hotfixes, and follow-up patches that lack downstream structural influence.

**Milestone Consolidation.** For each seed, parallel sub-agents expand the milestone boundary using shared file modifications, temporal proximity, and PR/Issue references, growing each seed into a milestone that bundles all commits realizing its development theme. Since the sub-agents operate independently, the same commit may be claimed by several milestones. A coordinating agent then resolves these overlapping claims so that each commit belongs to exactly one milestone, enforces complete coverage of the range, and certifies acyclicity.

**Dependency Inference.** The majority of inter-milestone edges follow directly from the line-level textual dependencies extracted during preprocessing. More subtle dependencies, such as call relationships that share no common hunk, are proposed and validated by an LLM agent using symbol-level analysis and file co-change patterns. Even so, certain dependencies surface only when milestones are built and executed. These residual edges are recovered later during runtime environment resolution (Section [3.2.3\)](#page-5-0).

<span id="page-5-0"></span>**Milestone Decompose.** Oversized milestones are decomposed into functionally independent submilestones while underspecified ones are merged into adjacent neighbors, with dependencies synchronously updated to preserve a valid DAG. When an oversized milestone is dominated by a single squashed PR-commit, the agent further re-segments the commit's diff along feature boundaries and remaps the affected dependency edges via line-level blame, promoting the resulting sub-units to first-class milestones. The pipeline targets a coefficient of variation CV < 1.0 over per-milestone LoC, achieving CV = 0.96 on EvoClaw (Appendix [A.2\)](#page-24-0).

# *3.2.3. Runtime Environment Resolution*

To transform the Milestone DAG into an executable evaluation environment, a *MainAgent* orchestrates a multi-agent workflow that produces, for every milestone, a reproducible Docker image that yields stable test signals. From a whole-evolution perspective, the *MainAgent* balances testbed quality against the cost of automated resolution. To achieve high quality at reasonable cost, the pipeline additionally relies on human-expert guidance to steer the *MainAgent* at key decision points. The *MainAgent* then dispatches sub-agents for batch analysis and problem localization, routing the surfaced issues to two specialized repair modules that iterate together until every milestone reaches a stable, fully collected state.

**Milestone DAG Optimization and Testbed Preparation.** A *MilestoneAgent* reconstructs each milestone's code state by cherry-picking its commits in topological order onto the codebase at the base release tag. When a cherry-pick conflict arises, the agent repairs the DAG, primarily by adding the missing cross-milestone dependency edge and, when necessary, relocating misattributed commits to the correct milestone. Commits that still cannot be applied are marked as deferred, so that every milestone is reconstructed into a complete, DAG-consistent state.

**Environment Configuration and Test Collection.** For each milestone, an *EnvAgent* generates a Dockerfile from the repository's CI/CD workflows and enforces three hard gates: the source compiles, the test framework collects successfully, and as many tests referenced by the milestone's patch as possible are captured in the collected set. A characteristic failure mode arises when the configured test environment runs ahead of the cherry-picked source state, so that functional modules referenced by the collected tests do not yet exist. These cases cannot be fixed locally and are deferred to the DAG optimization module for refinement (Appendix [A.3\)](#page-25-0).

# **3.3. Automated Quality Assurance**

To ensure the reliability and reproducibility of our evaluation, we rigorously validate each milestone testbed and report the aggregate evidence across three core dimensions, complementing the permilestone gates enforced in Section [3.2.3:](#page-5-0)

**Milestone Graph Validity.** We verify the structural integrity of the reconstructed history. This includes confirming *commit completeness* (100% coverage of the target range), *dependency consistency* (ensuring milestone dependencies respect underlying commit dependencies), and *DAG correctness* (validating acyclicity).

**Runtime Executability.** We ensure that errors stem from agent code, not infrastructure. We verify *testbed compilability* by ensuring successful build and test collection in both states. We also strictly monitor execution logs to ensure environment-induced errors remain negligible (≤0.10%).

**Evaluation Reliability.** We assess the stability of the test suites. We achieve a high *test collection rate* (87.1%). We ensure *test consistency* by validating a negligible Pass-to-Fail rate (≤0.026%) and filtering flaky tests through three repeated runs. Finally, we require each retained milestone to expose at least one F2P or N2P test signal (details in Appendix [A.4\)](#page-25-1).

# **4. EvoClaw: Benchmarking Continuous Software Evolution**

EvoClaw introduces a novel evaluation paradigm designed to assess an agent's ability to evolve and maintain a software codebase over an extended lifecycle. As shown in Figure [3,](#page-7-0) unlike traditional benchmarks that focus on resolving independent issues, EvoClaw simulates a realistic, continuous development process where requirements arrive as a stream, and tasks have strict sequential dependencies.

# <span id="page-7-0"></span>a. Independent Task Evaluation (e.g., SWE-bench) Issue Agent Repo Snapshot Patch Test Evaluation Result (fail/pass)

### b. Continuous Task Evaluation (EvoClaw) (iii) Task Stream Task Dependency Task Dependence Task List Task List Task List SRS 1 SRS 1 (ii) SRS 2 (i) SRS 1 SRS 2 SRS 3 SRS 2 SRS 3 Fetch Next Task Finished Task M1&M2 Finished Task M3 Agent Loop Check the new tasks All Tasks Done Codebase Tag-M1 **Base Snapshot** (1) (1) [= \ </>\ (I) In state (i), M1 and M2 were unlocked, while M3 remained locked %= %= In State (ii) Unlock M3 when Result "M1. M2 done" (fail/pass)

Figure 3 | Illustration of the evaluation pipelines. (a) In the Independent Task Evaluation Workflow, the environment resets after each task. (b) In the Continuous Task Evaluation Workflow, tasks are organized as a dependency graph. The agent continuously evolves the Codebase from a base snapshot. Upon completing a task (e.g., M1 & M2), the repository is snapshotted for Isolated Evaluation while the planner unlocks subsequent tasks (e.g., M3) for the agent to fetch, ensuring a continuous and stateful development loop.

### 4.1. The Continuous Task Evaluation Framework

The framework orchestrates a continuous development pipeline: an external planner dynamically unlocks tasks based on a dependency graph, the agent implements them in a persistent codebase, and the framework asynchronously evaluates snapshots upon submission. This design explicitly decouples **roadmap planning** from **implementation**, allowing us to assess the agent's ability to maintain and evolve software within a structured workflow. The framework comprises three core components:

**Dependency-Driven Task Stream.** Requirements are not presented in a static batch but are unlocked dynamically. The system maintains a DAG-based task scheduler where a new milestone  $M_i$  becomes available to the agent if and only if all its prerequisite milestones  $\{M_j \mid M_i \text{ depends on } M_j\}$  have been completed. This simulates real-world constraints in which foundational features must be established before dependent features are implemented.

**Continuous Evolution Environment.** The agent operates within a persistent, stateful environment where modifications from each task persist into the next. This compels the agent to maintain the long-term health of the codebase, as early technical debt or latent bugs can accumulate and impede future progress.

**Snapshot-Based Isolated Evaluation.** To reconcile the need for a continuous development flow with rigorous verification, we employ a "develop-in-place, evaluate-in-isolation" strategy. Upon task completion, the agent's implementation state is *snapshotted* and transferred to an isolated evaluation container to run the test suite. This ensures that the scoring process is reproducible and unaffected by the agent's ongoing development, while the agent's working environment remains uninterrupted.

### 4.2. Benchmark Construction

We construct a high-quality dataset through a rigorous pipeline that transforms open-source repositories into verified evolutionary suites.

<span id="page-8-0"></span>![](_page_8_Figure_1.jpeg)

![](_page_8_Figure_2.jpeg)

(a) Distribution of milestones across the 7 repositories in EvoClaw. Each bar represents the number of verified milestones extracted from the corresponding open-source project.

(b) Distribution of SRS word counts (left) and gold patch LOC (right), stratified by estimated human effort.

Figure 4 | Dataset statistics and characteristics of EvoClaw.

**Repository and Range Selection.** We identify projects with high community impact and diverse programming languages. We specifically select release ranges that exhibit rich dependency structures, ensuring the benchmark captures complex, non-linear development scenarios rather than trivial sequences.

Itinerary Extraction via DeepCommit. Leveraging the DeepCommit pipeline (Section 3), we mine the evolutionary history of selected projects. To guarantee the benchmark's quality and evaluation efficiency, we apply strict post-processing filters to the generated milestones. We retain only milestones that: (1) represent core functional changes (filtering out pure documentation updates); (2) possess executable F2P tests to serve as definitive success criteria; and (3) fall within a manageable context window to maintain task solvability. This step ensures that every task in the benchmark is grounded in a verified, executable state transition.

Reverse-Engineering Software Requirement Specifications (SRS). Relying solely on original GitHub issues or PR descriptions is often insufficient, as they can be underspecified, outdated, or disconnected from the final code implementation. To bridge this gap, we employ an agent-driven *reverse-engineering approach* to synthesize high-fidelity Software Requirement Specifications (SRS). We first dispatch an LLM agent to analyze the ground-truth patches to draft precise functional requirements. This draft then undergoes a refinement phase to align acceptance criteria strictly with the verified Fail-to-Pass tests. Finally, environment-specific instructions (e.g., dependency updates) are appended by analyzing build configuration changes, ensuring a complete execution context.

**Human-in-the-Loop Verification.** Automated generation can yield logical inconsistencies and misalignment with edge cases. To mitigate this, expert annotators conduct a final review focused on *task solvability*. Annotators verify that the SRS provides all necessary information to solve the problem without leaking implementation details and that the acceptance criteria are unambiguous. Simultaneously, we validate the stability of the test suites to rule out flaky tests. This hybrid verification ensures that EvoClaw provides a fair assessment, distinguishing genuine agent errors from artifacts of ambiguous specifications (Appendix B.1).

### 4.3. Benchmark Statistics

EvoClaw comprises **98 verified milestones** across **7 diverse open-source repositories**, spanning five programming languages (Go, Rust, Java, TypeScript, Python) with a total of 109 inter-milestone

dependencies. As shown in Figure [4a,](#page-8-0) the milestones are distributed across repositories with varying complexity, ranging from 9 to 23 milestones per repository. The dataset captures diverse real-world development patterns, including *major architectural changes* (e.g., multi-library support), *feature-rich iterations* (e.g., cloud-native enhancements), *stability-focused releases* (e.g., compatibility fixes), and *large-scale refactoring* (e.g., type system overhauls). This ensures EvoClaw evaluates agents across the full spectrum of software engineering tasks.

Figure [4b](#page-8-0) illustrates the distribution of task complexity. The dataset exhibits substantial diversity in both specification length (SRS mean: 1,348 words) and implementation scope (gold patch LOC ranging from < 100 to > 1, 500). On average, each milestone modifies 27.4 files and involves 17.1 Fail-to-Pass tests for verification alongside 6,218 Pass-to-Pass tests for regression prevention. Detailed per-repository statistics are provided in Appendix [B.3,](#page-29-0) and the full Milestone DAG visualizations for all repositories are shown in Appendix [B.4.](#page-31-0)

# **5. Results and Analysis**

# <span id="page-9-0"></span>**5.1. Experimental Setup**

**Evaluation Settings** To isolate how error accumulation across milestones affects agent performance, we evaluate methods under two different settings based on the Milestone DAG: (1) **Continuous Task Evaluation**, the standard EvoClaw setting where agents continuously evolve a codebase under streaming requirements. This setting introduces real-world challenges such as error accumulation and technical debt management. (2) **Independent Task Evaluation**, a stateless baseline (similar to SWE-bench [\(Jimenez et al.,](#page-20-0) [2024\)](#page-20-0)) in which each milestone is treated as an isolated task by providing agents with the canonical codebase snapshot, thereby decoupling performance from the cumulative effects of prior modifications.

**Evaluation Metrics** Evaluating agents in a continuous evolution setting requires metrics that capture two competing objectives: implementing new functionality and preserving existing behavior. Traditional benchmarks such as SWE-bench rely on binary success criteria (all tests pass or fail), which are too coarse-grained to capture the nuance of incremental progress and regression. Simple pass-rate metrics conflate these two objectives, failing to distinguish an agent that implements features but introduces regressions from one that avoids regressions but makes no progress.

To address this limitation, we decompose agent performance along two complementary dimensions:

• **Recall** measures *feature implementation completeness*: the proportion of required functional changes successfully implemented by the agent.

$$Recall_m = \frac{N_{\text{fixed},m}}{N_{\text{requried},m}} \tag{1}$$

where required, denotes the total number of *Fail-to-Pass* (F2P) tests for milestone (tests that transition from failing at the start state to passing after the milestone's gold patch is applied), and fixed, is the count of such tests that the agent successfully fixes.

• **Precision** measures *modification reliability*: the proportion of test status changes that are improvements rather than regressions, quantifying the safety of the agent's edits.

$$Precision_m = \frac{N_{\text{fixed},m} + \epsilon}{N_{\text{fixed},m} + N_{\text{broken},m} + \epsilon}$$
 (2)

where  $N_{\text{broken},m}$  is the number of *Pass-to-Pass* (P2P) tests (tests that pass at the start state and must remain passing after the agent's changes) that regress (fail or error out) due to the agent's changes. The term  $\epsilon = 1$  is a smoothing factor to handle cases where the agent makes no impact (i.e., when both fixed and broken counts are zero).

We then define the score for each milestone as the harmonic mean of Recall and Precision:

$$Score_m = \frac{2 \cdot Precision_m \cdot Recall_m}{Precision_m + Recall_m}$$
(3)

The final reported metric is the average Score across all milestones: Score =  $\frac{1}{|M|} \sum_{m \in M} \text{Score}_m$ . This ensures that neither dimension can be neglected: an agent that implements all features but introduces severe regressions will score as poorly as one that preserves existing functionality but fails to implement any changes.

Consistent with prior work like SWE-bench, we also report the **Milestone Resolve Rate**, where a milestone is considered *resolved* only if the agent passes all associated F2P and P2P tests. We report the average resolve rate across all repositories. While Score quantifies partial progress, Resolve Rate assesses whether the task was fully resolved.

Evaluated Models and Agents We evaluate a diverse set of frontier LLMs across four agent frameworks. Specifically, we test (1) Claude Code with Claude Opus 4.5, Claude Sonnet 4.5, Claude Opus 4.6, and Claude Sonnet 4.6, (2) Codex CLI with GPT 5.2, GPT 5.2-Codex, and GPT 5.3-Codex (all set to xhigh reasoning effort), (3) Gemini CLI with Gemini 3 Pro, Gemini 3.1 Pro, and Gemini 3 Flash (all by default with 1M context), and (4) Open-Hands (Wang et al., 2025) with Claude Opus 4.6, GPT 5.3-Codex, Gemini 3 Flash, Kimi K2.5, and MiniMax M2.5. Detailed framework versions, context management configurations, and the unified agent system prompt (Figure 18) are provided in Section B.2.

<span id="page-10-1"></span>

| Agent       | Model             | Score* (%)↑ | Precision (%)↑ | Recall (%)↑  | Resolve (%)↑ | Cost (\$)          | Out Tok. (K)     | Time (h) | Turns            |
|-------------|-------------------|-------------|----------------|--------------|--------------|--------------------|------------------|----------|------------------|
|             | Claude Sonnet 4.5 | 15.16       | 18.88          | 28.50        | 5.49         | 27.02              | 243              | 2.06     | 770              |
| claude-code | Claude Opus 4.5   | 25.85       | 28.04          | 40.80        | 6.28         | 71.10              | 309              | 2.35     | 999              |
| ciaude-code | Claude Sonnet 4.6 | 29.58       | 29.62          | 47.63        | 5.88         | 68.88              | 852              | 4.41     | 1538             |
|             | Claude Opus 4.6   | 36.29       | 37.84          | 56.32        | 11.57        | 88.22              | 578              | 2.73     | 1891             |
|             | GPT 5.2-Codex     | 13.46       | 12.65          | 26.65        | 4.78         | 38.11              | 701              | 3.56     | 1259             |
| codex       | GPT 5.2           | 23.30       | 20.89          | 45.76        | 8.18         | 56.90              | 814              | 5.35     | 1717             |
|             | GPT 5.3-Codex     | 28.88       | 27.81          | 49.70        | 9.58         | 25.01              | 392              | 8.23     | 1109             |
|             | Gemini 3 Pro      | 24.25       | 25.46          | 32.70        | 13.37        | 114.96             | 294              | 3.65     | 676              |
| gemini-cli  | Gemini 3.1 Pro    | 23.32       | 21.59          | 37.22        | 10.95        | 62.97              | 207              | 3.89     | 1208             |
|             | Gemini 3 Flash    | 24.22       | 24.31          | 42.12        | 8.37         | 12.10              | 255              | 5.02     | 1512             |
|             | MiniMax M2.5      | 17.60       | 22.48          | 34.60        | 1.30         | 3.57               | 598              | 11.88    | 1846             |
| openhands   | Kimi K2.5         | 20.20       | 26.29          | 31.37        | 8.49         | 4.32               | 279              | 6.85     | 800              |
|             | Gemini 3 Flash    | 22.32       | 25.20          | 37.13        | 6.59         | 16.90              | 1516             | 7.16     | 2632             |
|             | GPT 5.3-Codex     | 26.47       | 25.01          | 37.32        | 12.50        | 30.13 <sup>†</sup> | 553 <sup>†</sup> | 18.75    | $1047^{\dagger}$ |
|             | Claude Opus 4.6   | 38.03       | <u>37.33</u>   | <u>55.21</u> | 8.46         | 75.73 <sup>†</sup> | $524^{\dagger}$  | 7.54     | $1970^{\dagger}$ |

Table 2 | Performance of coding agents on EvoClaw under continuous task evaluation. All metrics are per-evolution-range averages. Out Tok. (K): total generated tokens in thousands, including reasoning where applicable. \*Primary metric (shaded). **Bold**: best in column. <sup>†</sup>Token tracking unavailable for some repos; averaged over available data.

### <span id="page-10-0"></span>5.2. Overall Performance

Table 2 presents results across 15 agent-model configurations. Claude Opus 4.6 achieves the highest Score (38.03% in Openhands and 36.29% in Claude Code), followed by Claude Sonnet

<span id="page-11-1"></span>![](_page_11_Figure_1.jpeg)

Figure 5 | Per-repository score comparison under two evaluation modes. High independent-task performance across all repositories confirms that milestones are individually solvable.

4.6 (29.58%) and GPT 5.3-Codex (28.88%). Across all models, the gap between Score (~38% at best) and Resolve Rate (~13%) is substantial: agents achieve partial progress on most milestones but rarely complete them fully. Moreover, the resolved milestones are predominantly early ones with few upstream dependencies, confirming that accumulated upstream errors increasingly hinder downstream task completion. Unless otherwise noted, subsequent analyses focus on configurations where each model is paired with its vendor-provided agent framework.

Across model families, generational improvements emerge: Claude 4.6 models significantly outperform their 4.5 predecessors, and GPT 5.3–Codex substantially improves over its predecessors. However, comparing GPT 5.2 and GPT 5.2–Codex reveals that Codex-specific optimization may be counterproductive for long-horizon development, where sustained codebase maintenance demands broader analytical capabilities beyond isolated task solving. The three Gemini models achieve comparable scores, with Gemini 3 Flash matching Gemini 3 Pro at one-ninth the cost. Gemini 3 Pro uses the fewest turns, possibly indicating insufficient

<span id="page-11-0"></span>![](_page_11_Figure_5.jpeg)

Figure 6 | Overall Score vs. cost trade-off across all repositories.

exploration. Figure 6 visualizes the cost-score trade-off. Higher cost does not uniformly translate into higher performance: Gemini 3 Pro exceeds \$100 per evolution range yet scores below Opus 4.6 (\$88), and Sonnet 4.6 (\$69) trails Opus 4.6 by 6.7 points despite a similar cost tier. On the Pareto frontier, Gemini 3 Flash (\$12, 24.2%) and GPT 5.3-Codex (\$25, 28.9%) offer the best cost-effectiveness, achieving competitive scores at a fraction of the cost of top-performing models. OpenHands trials exhibit notably longer execution times (e.g., 18.49 h for GPT 5.3-Codex) because its runner permits up to 3,000 iterations per milestone with automatic session resumption, allowing the agent to retry extensively when stuck. This additional compute does not consistently improve scores: Claude Code with Opus 4.6 achieves a comparable score in under 4 hours.

Figure 5 compares per-repository performance under both evaluation modes. High independent-task performance across all repositories confirms that milestones are individually solvable, indicating that the difficulty stems from long-horizon error accumulation rather than inherent task complexity. This effect varies significantly by repository. scikit-learn exhibits the largest degradation: Claude Sonnet 4.6 achieves 93.2% independently but only 21.1% under continuous evaluation.

<span id="page-12-1"></span>![](_page_12_Figure_1.jpeg)

Figure 7 | Task complexity effects on Score (top) and Resolve Rate (bottom), binned by code size, specification length, execution order, and DAG layer. Dashed lines are per-bin averages across models.

Overall, these results highlight that EvoClaw poses a significant challenge to current frontier models, and reliable long-horizon continuous development remains an open problem.

### <span id="page-12-2"></span>5.3. Task Complexity and Topological Effects

Figure 7 examines how milestone characteristics correlate with agent performance. Gold patch LOC, a traditional measure of task complexity, shows a clear monotonic relationship. Larger patches require more code changes and yield lower scores across all models. SRS (Software Requirements Specification) word count, however, exhibits a non-monotonic pattern, with a clear sweet spot for specifications of moderate length (around 500 to 1500 words). When specifications are concise, agents must autonomously locate relevant context from the repository, increasing exploration burden. When specifications are verbose, the sheer volume of requirements increases implementation workload. Milestones with moderate-length SRSs achieve the highest accuracy, suggesting that task difficulty depends not only on implementation effort but also on the cost of information acquisition.

Beyond these static factors, the continuous evaluation setting introduces structural complexity unique to EvoClaw. Both the milestone execution order and the DAG topological layer show statistically significant negative correlations with the score. Later milestones and deeper topological layers consistently yield lower performance. This reflects the compounding effect of upstream errors, as agents must build upon their own (potentially flawed) prior work. These topological factors are absent in independent evaluation and represent the distinctive challenge of long-horizon software evolution. The Resolve Rate (bottom row of Figure 7) makes this effect even starker: it drops drastically beyond the earliest milestones and the shallowest DAG layers, indicating that current agents can only fully resolve milestones that appear early in the sequence or have no upstream dependencies. Once prior errors accumulate, agents may still achieve partial progress (reflected in Score) but rarely produce a completely correct solution.

### <span id="page-12-0"></span>5.4. Evolution Dynamics: Recall Scales while Precision Saturates

The declining performance at later milestones raises a natural question: does agent capability degrade over time, or does accumulated technical debt overwhelm otherwise competent agents?

To answer this, we model cumulative score trajectories using a saturation function  $y = a(1 - e^{-bx})$ ,

<span id="page-13-0"></span>![](_page_13_Figure_1.jpeg)

Figure 8 | Evolution dynamics across models. (Left) Multi-window extrapolation of saturation curves fitted with  $y = a(1 - e^{-bx})$ , showing projected ceilings beyond the observed window. Legend annotations report init = ab (marginal efficiency at the onset of the sequence) and retain =  $e^{-b}$  (fraction of efficiency preserved after each observation window). (Middle) Continuous vs. Independent comparison for GPT 5.3–Codex (better retain) and Gemini 3.1 Pro (better init). (Right) Continuous vs. Independent comparison for the Claude model family.

<span id="page-13-1"></span>![](_page_13_Figure_3.jpeg)

Figure 9 | Per-model cumulative Recall (solid) and Precision (dotted) over evolution progress. Stronger models achieve near-linear Recall growth, yet Precision saturates across all evaluated configurations.

where a small *b* yields near-linear growth while a large *b* produces rapid saturation toward the ceiling *a*. As shown in Figure 8 (left), all models under exhibit clear performance ceilings, and multi-window extrapolation (fitting the saturation model to progressively larger subsets of milestones and projecting forward) confirms that these ceilings persist beyond the observed window. Comparing continuous and independent evaluation (middle, right), independent scores grow near-linearly while continuous scores saturate, with the gap widening monotonically as evolution progresses.

We decompose the cumulative score into *Recall* (successful feature implementation) and *Precision* (preservation of existing functionality) to isolate the underlying mechanism. Figure 9 reveals a fundamental asymmetry: Recall continues to grow near-linearly across all models (especially frontier models), indicating that agents retain the ability to solve newly assigned tasks. Precision, however, saturates rapidly across all evaluated configurations. This means the performance ceiling is not caused by agents forgetting how to code, but by their inability to prevent regressions from accumulating. Stronger models achieve higher Precision plateaus, yet none avoid saturation entirely. This Recall-Precision divergence provides a mechanistic explanation for the snowball effect: as unresolved regressions compound, each new milestone operates on an increasingly degraded codebase, eventually

<span id="page-14-1"></span>![](_page_14_Figure_1.jpeg)

Figure 10 | Propagation type analysis for Opus 4.6. **Left**: Selected error chain patterns across repositories, where each column is an error chain and each row a milestone. **Right**: Distribution of propagation event types across milestone progress bins (averaged over all repositories), showing how inherited failures (P1) and infrastructure effects (PX) increasingly dominate in later stages. overwhelming the agent's capacity for productive development.

### <span id="page-14-0"></span>5.5. Failure Analysis: Error Generation and Propagation

Understanding *why* agents fail in continuous evaluation is inherently difficult. A single early mistake can trigger cascading test failures across dozens of downstream milestones, making it challenging to disentangle root causes from their propagated consequences. To enable systematic analysis, we introduce the concept of **error chains**: for each test that transitions from passing to failing during the evolution, we trace its status across all subsequent milestones until it is either healed or the trial ends. This yields a per-test timeline that captures the full lifecycle of an error. We focus this analysis on the strongest configuration, Claude Opus 4.6, to characterize failure mechanisms at the frontier of current agent capabilities.

We decompose error chains along two orthogonal dimensions. The first, **Propagation Type**, captures *how* a fault affects downstream milestones. This is determined statistically from evaluation results: we track each test's status across the milestone timeline and classify events as P0 Root Cause (the originating failure), P0 Induced (cross-chain contamination from unrelated changes), P1 Inherited (propagated through dependency), PX Missing (skipped execution), or PH Healed (successfully recovered). Figure 10 (right) shows that propagation events (P1, PX) increasingly dominate in later stages, confirming the compounding degradation observed in Section 5.3. The left panel visualizes representative error chain patterns across repositories, illustrating how a single root cause event can cascade through the entire remaining evolution.

The second dimension, **Root Cause Type**, captures *why* the initial fault originates. Since root cause attribution requires understanding the agent's intent, we employ Claude Sonnet 4.6 as a reviewer agent that compares the task agent's code changes against the ground-truth patch, the SRS specification, and evaluation artifacts. The reviewer classifies each error chain's root cause into three categories: Logic Error (correct target, buggy implementation), Omission (missing a required component), or Extraneous (unnecessary

<span id="page-14-2"></span>![](_page_14_Figure_7.jpeg)

Figure 11 | Root Cause Type  $\times$  Propagation Type heatmap. Each cell shows the macro-averaged event proportion across all repositories.

<span id="page-15-1"></span>![](_page_15_Figure_1.jpeg)

Figure 12 | Continuous-to-Independent turns ratio across normalized execution progress (10 bins). Values above 1× indicate the agent expends more effort under continuous evaluation than on the same milestone independently. The ratio remains near or below 1× for most of the sequence but rises sharply in the final bin. This reflects increased rework and error-recovery effort as accumulated technical debt compounds.

<span id="page-15-2"></span>![](_page_15_Figure_3.jpeg)

Figure 13 | Exploration ratio and context wave for Claude Code (powered by Opus 4.6) on element-web. Top plot shows milestone progression (M1 to M18). Middle plot shows per-minute exploration ratio (read/search vs. write/execute). Bottom plot shows total context token usage over active time, with compaction and eviction events marked.

modifications that break existing functionality). Figure [11](#page-14-2) presents the joint distribution of Root Cause Type × Propagation Type. Logic Error is the dominant root cause (∼57% of all error chain events), with its chains exhibiting both the highest inherited propagation (P1, 12%) and the highest proportion of missing test execution (PX Missing, 17%), indicating that buggy implementations frequently prevent downstream tests from running at all.

# <span id="page-15-0"></span>**5.6. Agent Behavior: The Struggle Against Accumulating Complexity**

Beyond aggregate scores, we examine how agents allocate effort and manage state when facing accumulating technical debt during long-horizon iterations. By instrumenting tool calls, context usage, and interaction turns, we reveal distinct behavioral patterns.

**Effort Fluctuation and Extremes.** As shown in Figure [12,](#page-15-1) all evaluated agents exhibit a shared

<span id="page-16-0"></span>![](_page_16_Figure_1.jpeg)

Figure 14 | Exploration tool-call count aggregated across all repositories, grouped by agent framework and sorted by count within each cluster. Diamond markers show average F1 score. Higher-performing agents consistently devote greater effort to exploration (e.g., reading and searching).

trend in their effort allocation (measured by the continuous-to-independent turns ratio). In the initial phase (progress  $\sim$ 0.1), continuous effort is slightly higher than independent effort, as agents must conduct large-scale exploration to build a mental model of the unfamiliar repository. During the middle phase (progress 0.1–0.5), the ratio drops below 1× (with the median falling to  $\sim$ 0.83×): agents successfully reuse their established context, bypassing the redundant exploration required in independent evaluation. However, in the late stage (progress 0.6–0.9), effort rises significantly as accumulating errors demand extensive debugging. Finally, near completion (progress  $\sim$ 1.0), agent behavior diverges sharply. Some agents resort to frantic thrashing, while others prematurely give up. Notably, GPT 5.3–Codex demonstrates the most stable effort profile, maintaining consistent variance throughout the project lifecycle.

Context Stability and Exploration Patterns. To sustain this fluctuating effort, agents must effectively manage their context. Figure 13 illustrates this using Claude Code with Opus 4.6 as a representative example. The context window shows stable, controllable wave patterns, demonstrating that modern agent frameworks paired with frontier models can effectively support long-horizon programming without catastrophic context overflow. The framework employs two compression strategies: partial compression (evicting specific tool results) and heavy compaction (summarizing extensive histories). Crucially, agent exploration behavior (reading and searching) tightly couples with this state management. Exploration surges at the beginning of each new milestone and immediately following major context compaction events, as the agent works to rebuild its mental model.

The Impact of Exploration. This exploration behavior directly dictates downstream success. Figure 14 demonstrates that within their respective agent frameworks, models from the same family exhibit a consistent pattern: higher exploration counts correlate with better performance. For instance, Claude Opus 4.6 and Claude Sonnet 4.6 hold a distinct advantage because they aggressively dispatch subagents to analyze the codebase, executing over 7,000 exploration commands. Conversely, models like Gemini 3 Pro allocate too little effort to reading, indicating that many current models still lack proactive exploration for long-horizon tasks.

**Verification vs. Blind Thrashing.** Alongside exploration, we analyze verification behavior (test execution). Figure 15 shows that average verification effort generally follows an inverted-U shape, increasing as the codebase grows more complex before declining near the end. However, this masks two problematic extremes: Gemini 3.1 Pro verifies excessively, while GPT 5.2-Codex rarely verifies at all, and both achieve lower scores. Figure 16 further isolates this dynamic by mapping the score landscape against edit thrashing and verification frequency. A clear sweet spot emerges for

<span id="page-17-0"></span>![](_page_17_Figure_1.jpeg)

<span id="page-17-1"></span>Figure 15 | Average verification tool-call count per milestone progress bin (10 bins), for the six strongest agent configurations. Verification effort generally increases with progress. It peaks around 70% to 80% completion before declining in the final bin.

![](_page_17_Figure_3.jpeg)

Figure 16 | Score landscape in the edit-thrashing (repeat edit ratio) vs. verification (test execution frequency) space, aggregated across all repositories. A sweet spot of moderate thrashing and moderate verification yields the highest scores. The blind thrashing quadrant (high thrash, low verify) produces the worst outcomes.

moderate, disciplined verification. In contrast, the worst outcomes concentrate in the high-thrash and low-verify quadrant—a blind thrashing trap where agents repeatedly modify the same files without executing tests to guide them, effectively accelerating the snowball effect.

# 5.7. DeepCommit vs Human-Annotated Milestone DAG

We conducted a case study (Appendix C.3) that compares the human-annotated and DeepCommit Milestone DAGs for the scikit-learn v1.5.2-v1.6.0 release interval. The Human DAG organizes milestones by semantic release intent, whereas DeepCommit derives groups from dependency topology in the commit graph. As a result, DeepCommit covers a smaller but tightly connected subset of commits, recovers human-like boundaries when technical structure is clear (e.g., documentation), but tends to fragment cross-module, intent-defined milestones into topological phases. Overall, this case study shows that the Human DAG captures semantically coherent and process-aware milestone structure,

whereas DeepCommit more strongly reflects dependency topology and phase-wise code organization.

# **6. Conclusion**

We introduced DeepCommit, a pipeline that distills verifiable software evolution into coherent Milestone DAGs from noisy, fine-grained git histories, and EvoClaw, a benchmark for evaluating LLM agents under continuous, dependency-driven development. Our results reveal a fundamental gap between independent task-solving and continuous evolution: frontier models achieve over 80% on isolated milestones but drop below 38% in continuous settings. This degradation stems from a critical inability to maintain code integrity: while agents can implement new features, they fail to prevent regressions, causing a snowball effect of accumulating technical debt. Even the strongest agents resolve only ∼13% of milestones in full evolutionary sequences, establishing sustained, maintainable repository evolution as a central open challenge for autonomous software agents.

# **Limitations**

EvoClaw and the DeepCommit pipeline have several limitations that bound the conclusions to be drawn and the settings to which they currently apply.

**Test-Suite Dependency.** Our construction relies on repositories with well-maintained, executable test suites that provide reliable F2P and P2P signals. Projects that lack rich test coverage, or whose tests depend on inaccessible external services, cannot currently be incorporated into the benchmark.

**Filtering Bias.** The pipeline retains only commits that touch source code with non-trivial intercommit dependencies, dropping documentation-only commits and commits without resolvable structural ties. This filtering improves DAG quality and evaluation tractability, but it may bias the resulting benchmark toward dependency-rich evolution and underrepresent independent maintenance work.

**Data Contamination Risk.** The repositories used in EvoClaw are high-impact open-source projects whose commit histories may have appeared in the pretraining corpora of frontier models. The substantial performance gaps we observe among frontier models suggest contamination has limited impact on relative ranking, but we cannot fully rule out memorization on individual milestones. Continuously refreshing the benchmark with newly merged commits, or applying DeepCommit to private repositories, would mitigate this risk.

**Human-in-the-Loop Reliance.** Two stages of DeepCommit still require human-expert oversight: (i) the *MainAgent*'s scheduling decisions during runtime environment resolution, where humans guide the trade-off between testbed quality and resolution cost, and (ii) the SRS verification stage, where human annotators run the three-step refinement loop described in Appendix [B.1.](#page-26-0) Fully automating these stages remains an open engineering problem.

**Scale Limit.** The current pipeline targets release ranges whose source-code gold patch is under roughly 30k LoC. Larger ranges produce Milestone DAGs that exceed the agent's resolution budget and frequently fail the testbed-construction gates. Scaling DeepCommit to longer histories will require further improvements to both DAG construction and runtime resolution.

# **Acknowledgements**

The authors of this work are supported in part by the U.S. Army Research Office under Grant W911NF-242-0194, the National Science Foundation under Grants OAC-2505107 and CCF-2426161, a Google Research Credit Award, and UCR Senate Awards. We thank OpenHands for providing the API credits that support most of the evaluations in this study. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of these organizations.

# **Impact Statement**

This paper presents a benchmark for evaluating LLM agents in continuous software evolution, a prerequisite for deploying autonomous agents in real-world production environments. Beyond code generation, we emphasize the ability to sustainably evolve systems over time, which is essential for long-running agent runtimes to iteratively customize software for diverse user needs. This capability unlocks a new productivity paradigm: agents serving as adaptive interfaces that bridge human intent and complex digital systems. Although highly capable coding agents may impact the software development workforce, we expect them to lower the barrier to entry for software creation, empowering a broader range of users to leverage the power of code for problem-solving

# **References**

<span id="page-19-0"></span>Anthropic. Claude code: Best practices for agentic coding. [https://www.anthropic.com/](https://www.anthropic.com/engineering/claude-code-best-practices) [engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices), 2025.

- <span id="page-19-2"></span>I. Badertdinov, A. Golubev, M. Nekrashevich, A. Shevtsov, S. Karasik, A. Andriushchenko, M. Trofimova, D. Litvintseva, and B. Yangel. SWE-rebench: An automated pipeline for task collection and decontaminated evaluation of software engineering agents. In *The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2026. URL [https:](https://openreview.net/forum?id=nMpJoVmRy1) [//openreview.net/forum?id=nMpJoVmRy1](https://openreview.net/forum?id=nMpJoVmRy1).
- <span id="page-19-4"></span>J. Chen, X. Xu, H. Wei, C. Chen, and B. Zhao. Swe-ci: Evaluating agent capabilities in maintaining codebases via continuous integration, 2026. URL <https://arxiv.org/abs/2603.03823>.
- <span id="page-19-1"></span>M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba. Evaluating large language models trained on code, 2021. URL <https://arxiv.org/abs/2107.03374>.

<span id="page-19-5"></span>Cursor. Cursor: The AI-first code editor. <https://cursor.sh>, 2024.

<span id="page-19-3"></span>X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park, N. Pasari, C. Rane, K. Sampath, M. Krishnan, S. Kundurthy, S. Hendryx, Z. Wang, V. Bharadwaj, J. Holm, R. Aluri, C. B. C. Zhang, N. Jacobson, B. Liu, and B. Kenstler. Swe-bench pro: Can ai agents solve long-horizon software engineering tasks?, 2025. URL <https://arxiv.org/abs/2509.16941>.

- <span id="page-20-2"></span>J. Ding, S. Long, C. Pu, H. Zhou, H. Gao, X. Gao, C. He, Y. Hou, F. Hu, Z. Li, W. Shi, Z. Wang, D. Zan, C. Zhang, X. Zhang, Q. Chen, X. Cheng, B. Deng, Q. Gu, K. Hua, J. Lin, P. Liu, M. Li, X. Pan, Z. Peng, Y. Qin, Y. Shan, Z. Tan, W. Xie, Z. Wang, Y. Yuan, J. Zhang, E. Zhao, Y. Zhao, H. Zhu, L. Zhu, C. Zou, M. Ding, J. Jiao, J. Liu, M. Liu, Q. Liu, C. Tao, J. Yang, T. Yang, Z. Zhang, X. Chen, W. Huang, and G. Zhang. Nl2repo-bench: Towards long-horizon repository generation evaluation of coding agents, 2026. URL <https://arxiv.org/abs/2512.12730>.
- <span id="page-20-1"></span>Y. Du, Y. Cai, Y. Zhou, C. Wang, Y. Qian, X. Pang, Q. Liu, Y. Hu, and S. Chen. Swe-dev: Evaluating and training autonomous feature-driven software development, 2026. URL [https://arxiv.org/](https://arxiv.org/abs/2505.16975) [abs/2505.16975](https://arxiv.org/abs/2505.16975).
- <span id="page-20-5"></span>M. Fan, W. Zhang, H. Zhao, G. Liang, and Z. Jin. Detect hidden dependency to untangle commits. In *Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering*, pages 179–190, 2024.
- <span id="page-20-3"></span>D. Fu, S. Wu, Y. Wu, Z. Peng, Y. Huang, J. Sun, J. Zeng, M. Jiang, L. Zhang, Y. Li, J. Hu, L. Liu, J. Hou, and P. Liu. davinci-env: Open swe environment synthesis at scale, 2026. URL [https:](https://arxiv.org/abs/2603.13023) [//arxiv.org/abs/2603.13023](https://arxiv.org/abs/2603.13023).
- <span id="page-20-8"></span>GitHub. Github copilot: Meet the new coding agent. [https://github.blog/news-insights/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/) [product-news/github-copilot-meet-the-new-coding-agent/](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/), 2025.
- <span id="page-20-9"></span>Google. Antigravity: An agentic development platform. <https://antigravity.google/>, 2025a.
- <span id="page-20-10"></span>Google. Gemini CLI: An open-source AI agent for the terminal. [https://github.com/](https://github.com/google-gemini/gemini-cli) [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli), 2025b.
- <span id="page-20-12"></span>X. He, Q. Liu, M. Du, L. Yan, Z. Fan, Y. Huang, Z. Yuan, and Z. Ma. Swe-perf: Can language models optimize code performance on real-world repositories?, 2025. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2507.12415) [2507.12415](https://arxiv.org/abs/2507.12415).
- <span id="page-20-6"></span>K. Herzig, S. Just, and A. Zeller. The impact of tangled code changes on defect prediction models. *Empirical Software Engineering*, 21(2):303–336, 2016.
- <span id="page-20-4"></span>N. Jain, J. Singh, M. Shetty, T. Zhang, L. Zheng, K. Sen, and I. Stoica. R2e-gym: Procedural environment generation and hybrid verifiers for scaling open-weights SWE agents. In *Second Conference on Language Modeling*, 2025. URL <https://openreview.net/forum?id=7evvwwdo3z>.
- <span id="page-20-0"></span>C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. R. Narasimhan. SWE-bench: Can language models resolve real-world github issues? In *The Twelfth International Conference on Learning Representations*, 2024. URL <https://openreview.net/forum?id=VTF8yNQM66>.
- <span id="page-20-11"></span>P. Laban, H. Hayashi, Y. Zhou, and J. Neville. LLMs get lost in multi-turn conversation. In *The Fourteenth International Conference on Learning Representations*, 2026. URL [https://openreview.net/](https://openreview.net/forum?id=VKGTGGcwl6) [forum?id=VKGTGGcwl6](https://openreview.net/forum?id=VKGTGGcwl6).
- <span id="page-20-7"></span>C. Labs. Introducing Devin, the first AI software engineer. [https://cognition.ai/blog/](https://cognition.ai/blog/introducing-devin/) [introducing-devin/](https://cognition.ai/blog/introducing-devin/), 2024.
- <span id="page-20-13"></span>J. J. Ma, M. Hashemi, A. Yazdanbakhsh, K. Swersky, O. Press, E. Li, V. J. Reddi, and P. Ranganathan. Swe-fficiency: Can language models optimize real-world repositories on real workloads?, 2025. URL <https://arxiv.org/abs/2511.06090>.

- <span id="page-21-8"></span>M. A. Merrill, A. G. Shaw, N. Carlini, B. Li, H. Raj, I. Bercovich, L. Shi, J. Y. Shin, T. Walshe, E. K. Buchanan, J. Shen, G. Ye, H. Lin, J. Poulos, M. Wang, M. Nezhurina, D. Lu, O. M. Mastromichalakis, Z. Xu, Z. Chen, Y. Liu, R. Zhang, L. L. Chen, A. Kashyap, J.-L. Uslu, J. Li, J. Wu, M. Yan, S. Bian, V. Sharma, K. Sun, S. Dillmann, A. Anand, A. Lanpouthakoun, B. Koopah, C. Hu, E. K. Guha, G. H. S. Dreiman, J. Zhu, K. Krauth, L. Zhong, N. Muennighoff, R. K. Amanfu, S. Tan, S. Pimpalgaonkar, T. Aggarwal, X. Lin, X. Lan, X. Zhao, Y. Liang, Y. Wang, Z. Wang, C. Zhou, D. Heineman, H. Liu, H. Trivedi, J. Yang, J. Lin, M. Shetty, M. Yang, N. Omi, N. Raoof, S. Li, T. Y. Zhuo, W. Lin, Y. Dai, Y. Wang, W. Chai, S. Zhou, D. Wahdany, Z. She, J. Hu, Z. Dong, Y. Zhu, S. Cui, A. Saiyed, A. Kolbeinsson, C. M. Rytting, R. Marten, Y. Wang, J. Jitsev, A. Dimakis, A. Konwinski, and L. Schmidt. Terminal-bench: Benchmarking agents on hard, realistic tasks in command line interfaces. In *The Fourteenth International Conference on Learning Representations*, 2026. URL <https://openreview.net/forum?id=a7Qa4CcHak>.
- <span id="page-21-2"></span>Nous Research. Hermes Agent: The agent that grows with you. [https://hermes-agent.](https://hermes-agent.nousresearch.com/) [nousresearch.com/](https://hermes-agent.nousresearch.com/), 2026.
- <span id="page-21-0"></span>OpenAI. Introducing codex. <https://openai.com/index/introducing-codex/>, 2025.
- <span id="page-21-1"></span>OpenClaw. OpenClaw: Your own personal AI assistant. [https://github.com/openclaw/](https://github.com/openclaw/openclaw) [openclaw](https://github.com/openclaw/openclaw), 2026.
- <span id="page-21-4"></span>G. Orlanski, D. Roy, A. Yun, C. Shin, A. Gu, A. Ge, D. Adila, N. Roberts, F. Sala, and A. Albarghouthi. SlopCodeBench: Benchmarking how coding agents degrade over long-horizon iterative tasks, 2026. URL <https://arxiv.org/abs/2603.24755>.
- <span id="page-21-11"></span>A. Ouyang, S. Guo, S. Arora, A. L. Zhang, W. Hu, C. Re, and A. Mirhoseini. Kernelbench: Can LLMs write efficient GPU kernels? In *Forty-second International Conference on Machine Learning*, 2025. URL <https://openreview.net/forum?id=yeoN1iQT1x>.
- <span id="page-21-5"></span>J. Pan, X. Wang, G. Neubig, N. Jaitly, H. Ji, A. Suhr, and Y. Zhang. Training software engineering agents and verifiers with SWE-gym. In *Forty-second International Conference on Machine Learning*, 2025. URL <https://openreview.net/forum?id=Cq1BNvHx74>.
- <span id="page-21-10"></span>O. Press, B. Amos, H. Zhao, Y. Wu, S. Ainsworth, D. Krupke, P. Kidger, T. Sajed, B. Stellato, J. Park, N. Bosch, E. Meril, A. Steppi, A. Zharmagambetov, F. Zhang, D. Pérez-Piñeiro, A. Mercurio, N. Zhan, T. Abramovich, K. Lieret, H. Zhang, S. Huang, M. Bethge, and O. Press. Algotune: Can language models speed up general-purpose numerical programs? In *The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2026. URL [https:](https://openreview.net/forum?id=dF1tD9hjvn) [//openreview.net/forum?id=dF1tD9hjvn](https://openreview.net/forum?id=dF1tD9hjvn).
- <span id="page-21-9"></span>M. Shetty, N. Jain, J. Liu, V. Kethanaboyina, K. Sen, and I. Stoica. GSO: Challenging software optimization tasks for evaluating SWE-agents. In *The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2026. URL [https://openreview.](https://openreview.net/forum?id=I5qDL315bQ) [net/forum?id=I5qDL315bQ](https://openreview.net/forum?id=I5qDL315bQ).
- <span id="page-21-3"></span>M. V. Thai, T. Le, D. N. Manh, H. P. Nhat, and N. D. Bui. Swe-evo: Benchmarking coding agents in long-horizon software evolution scenarios. *arXiv preprint arXiv:2512.18470*, 2025.
- <span id="page-21-7"></span>TRAE. Trae: The real AI engineer. <https://www.trae.ai/>, 2025.
- <span id="page-21-6"></span>X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan, Y. Song, B. Li, J. Singh, H. H. Tran, F. Li, R. Ma, M. Zheng, B. Qian, Y. Shao, N. Muennighoff, Y. Zhang, B. Hui, J. Lin, R. Brennan, H. Peng, H. Ji, and G. Neubig. Openhands: An open platform for AI software developers as

- generalist agents. In *The Thirteenth International Conference on Learning Representations*, 2025. URL <https://openreview.net/forum?id=OJd3ayDDoF>.
- <span id="page-22-6"></span>C. S. Xia, Y. Deng, S. Dunn, and L. Zhang. Demystifying llm-based software engineering agents. *Proceedings of the ACM on Software Engineering*, 2(FSE):801–824, 2025.
- <span id="page-22-9"></span>W. XU, J. Xiong, C. Zhao, Q. Chen, H. Wang, H. Shen, Z. Wan, J. Dai, T. Wu, H. Xiao, C. Tao, Z. Mao, Y. Sheng, Z. Guo, H. Yang, B. Yu, L. Kong, Q. Gu, and N. Wong. SWINGARENA: Adversarial programming arena for long-context github issue solving. In *The Fourteenth International Conference on Learning Representations*, 2026. URL <https://openreview.net/forum?id=YuxgSGFaqb>.
- <span id="page-22-7"></span>J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. R. Narasimhan, and O. Press. SWE-agent: Agent-computer interfaces enable automated software engineering. In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024. URL [https://openreview.net/](https://openreview.net/forum?id=mXpq6ut8J3) [forum?id=mXpq6ut8J3](https://openreview.net/forum?id=mXpq6ut8J3).
- <span id="page-22-5"></span>J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. R. Narasimhan, and O. Press. mini-SWE-agent: A minimal ai software engineering agent. <https://github.com/SWE-agent/mini-swe-agent>, 2025.
- <span id="page-22-3"></span>J. Yang, K. Lieret, J. Ma, P. Thakkar, D. Pedchenko, S. Sootla, E. McMilin, P. Yin, R. Hou, G. Synnaeve, D. Yang, and O. Press. Programbench: Can language models rebuild programs from scratch?, 2026. URL <https://arxiv.org/abs/2605.03546>.
- <span id="page-22-4"></span>S. Yao. The second half. <https://ysymyth.github.io/The-Second-Half/>, 2025. Accessed: 2025.
- <span id="page-22-0"></span>D. Zan, Z. Huang, W. Liu, H. Chen, S. Xin, L. Zhang, Q. Liu, A. Li, L. Chen, X. Zhong, S. Liu, Y. Xiao, L. Chen, Y. Zhang, J. Su, T. Liu, R. LONG, M. Ding, and liang xiang. Multi-SWE-bench: A multilingual benchmark for issue resolving. In *The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2026. URL [https://openreview.](https://openreview.net/forum?id=MhBZzkz4h9) [net/forum?id=MhBZzkz4h9](https://openreview.net/forum?id=MhBZzkz4h9).
- <span id="page-22-8"></span>L. Zhang, S. He, C. Zhang, Y. Kang, B. Li, C. Xie, J. Wang, M. Wang, Y. Huang, S. Fu, E. Nallipogu, Q. Lin, Y. Dang, S. Rajmohan, and D. Zhang. SWE-bench goes live! In *The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2026. URL <https://openreview.net/forum?id=OGWkr7gXka>.
- <span id="page-22-2"></span>W. Zhao, N. Jiang, C. Lee, J. T. Chiu, C. Cardie, M. Gallé, and A. M. Rush. Commit0: Library generation from scratch. In *The Thirteenth International Conference on Learning Representations*, 2025. URL <https://openreview.net/forum?id=MMwaQEVsAg>.
- <span id="page-22-1"></span>Q. Zhou, J. Zhang, H. Wang, R. Hao, J. Wang, M. Han, Y. Yang, S. Wu, F. Pan, L. Fan, D. Tu, and Z. Zhang. Featurebench: Benchmarking agentic coding for complex feature development. In *The Fourteenth International Conference on Learning Representations*, 2026. URL [https://](https://openreview.net/forum?id=41xrZ3uGuI) [openreview.net/forum?id=41xrZ3uGuI](https://openreview.net/forum?id=41xrZ3uGuI).

# **Table of Contents**

| A |     | DeepCommit Pipeline Implementation Details                  | 24 |
|---|-----|-------------------------------------------------------------|----|
|   | A.1 | Commit History Preprocessing Details<br>                    | 24 |
|   | A.2 | Milestone DAG Construction Details                          | 25 |
|   | A.3 | Runtime Environment Resolution Details                      | 26 |
|   | A.4 | Testbed Validation<br>                                      | 26 |
| B |     | EvoClaw Benchmark Details                                   | 27 |
|   | B.1 | Software Requirement Specifications<br>                     | 27 |
|   | B.2 | Evaluation Configuration Details<br>                        | 28 |
|   | B.3 | Detailed Dataset Statistics<br>                             | 30 |
|   | B.4 | Milestone DAG Visualizations<br>                            | 32 |
| C |     | Extended Experimental Analysis and Discussion               | 33 |
|   | C.1 | Agent Code Quality Analysis                                 | 33 |
|   | C.2 | Cumulative Error Analysis on element-web                    | 38 |
|   | C.3 | Case Study: Human vs. DeepCommit Milestone DAG Construction | 38 |

# <span id="page-23-1"></span>**A. DeepCommit Pipeline Implementation Details**

This appendix documents the per-stage implementation of the DeepCommit pipeline introduced in Section [3,](#page-3-0) covering commit history preprocessing, Milestone DAG construction, runtime environment resolution, and testbed validation.

# <span id="page-23-0"></span>**A.1. Commit History Preprocessing Details**

In open-source projects, version tags are applied in various ways, posing challenges for determining the mainline commit range. Commonly, tags are placed directly on the main branch, making the commits between start and end tags the target range. However, many projects use a release branch model: a release branch is created from main for stabilization before release, and the tag is ultimately placed on the release branch rather than main. In such cases, directly comparing two tags would include release branch commits while missing parallel development on main.

To address this, we employ a *branch-out/first-parent* strategy to recover the mainline range. First, we use git merge-base to find each tag's branch-out point from the main branch. Then, we collect all commits between these two branch-out points along the main branch's first-parent chain. First-parent traversal ensures we only follow direct commits on main, ignoring internal commits from merged feature branches, thus obtaining a clean mainline evolution sequence.

**Data Collection.** For each entity, we collect metadata and content: commit change details and parent relationships; PR descriptions, constituent commits, linked Issues, and code review discussions; Issue descriptions and discussions; Release version tags and notes.

**Per-Repo Configuration.** Source-file filtering is driven by a small per-repository configuration with four fields: repo\_src\_dirs (source-module directories to retain), test\_dirs (test-file glob patterns), exclude (build artifacts and generated files to strip from within source directories), and main\_branch (the branch used for range extraction). An LLM agent bootstraps this configuration by detecting the repository language from build markers (e.g., pyproject.toml, pom.xml, go.mod) and proposing source and test patterns from the repository layout and tag-range history. A human curator then verifies coverage, confirming which directories constitute product-logic source code. The rules below apply on top of this configuration.

**Filtering Rules.** Raw data contains numerous changes irrelevant to core functionality. We apply multi-layer filtering:

- 1. **Source directory whitelist**: Retain only changes under designated source directories (e.g., src/, lib/), excluding documentation, configuration files, and CI/CD scripts.
- 2. **Test file exclusion**: Exclude test code via filename patterns (e.g., \*\_test.go, test\_\*.py) and directory patterns (e.g., tests/, \_\_tests\_\_/).
- 3. **Empty commit removal**: Commits containing no valid source changes after filtering are removed.
- 4. **Reference consistency**: When commits are removed, the system checks PR and Issue references, removing orphaned PRs and Issues no longer referenced by any commit.

# <span id="page-24-0"></span>**A.2. Milestone DAG Construction Details**

**Topological Features for Seed Discovery.** We utilize the following Commit DAG topological metrics to identify milestone seeds: (1) *Out-degree*: commits depended upon by multiple subsequent commits typically introduce foundational functionality; (2) *Topological level*: commits at higher levels represent later architectural changes; (3) *Descendant count*: commits with many descendants have broad impact and are often key nodes. The Agent typically identifies fewer than 20 seed commits.

**Expansion Rules for Milestone Consolidation.** Sub-agents expand seed boundaries using the following rules: (1) *File modification overlap*: commits modifying the same files likely belong to the same feature; (2) *Temporal proximity*: commits close in time are more likely part of the same development task; (3) *Semantic association*: commit messages containing similar keywords or referencing the same Issue/PR. The system first pre-groups seeds based on commit subgraph overlap.

**Heuristics for Dependency Inference.** For potential dependencies not covered by structural analysis, the system generates and ranks candidate edges using heuristic rules: (1) *File overlap ratio*: the proportion of shared files modified by two milestones; (2) *Symbol references*: whether downstream milestones call functions/classes defined in upstream ones; (3) *Temporal ordering*: whether the upstream milestone's median commit time precedes the downstream's; (4) *Author overlap*: milestones by the same author are more likely to have dependencies. After Agent verification, dependencies are classified into two types: *strong dependencies* indicate that missing upstream milestones will cause downstream build or test failures; *weak dependencies* indicate functionality can degrade gracefully without affecting basic operation.

**Balancing Strategy for Milestone Decomposition.** The system computes the source lines of code (LOC) for each milestone and uses the coefficient of variation (CV = std/mean) to measure granularity uniformity, targeting CV < 1.0. On EvoClaw, the final partition achieves CV = 0.96. Abnormally sized milestones are flagged in two cases: *too large*, when LOC exceeds mean +, and *too small*, when LOC falls below mean − and under 100 lines.

**PR-Commit Splitting.** An oversized milestone is sometimes dominated by a single squashed PRcommit, which cannot be rebalanced by regrouping commits. In this case, an LLM agent re-segments the squashed diff into smaller commits along feature boundaries, optionally emitting one integrationtest commit. Dependencies among the resulting pieces, together with edges to downstream milestones, are recomputed via line-level git blame, so each split unit inherits only the edges it truly depends on, and the units are promoted to first-class milestones in the DAG. When no clear feature boundary exists, the agent falls back to chronological grouping, and test-only commits are never emitted as standalone milestones.

# <span id="page-25-0"></span>**A.3. Runtime Environment Resolution Details**

**Motivation for Testbed Reconstruction.** The original repository's commit history reflects the actual chronological order of development, not the logical dependencies between functional modules. For example, a developer may implement feature A before feature B, even though B logically depends on A. Using the original history directly would cause milestone code states to be inconsistent with the DAG's dependency structure. Therefore, we re-cherry-pick commits according to the DAG's topological order, generating a new history organized by functional logic.

**Flaky Test Filtering.** Flaky tests produce inconsistent results on the same code, severely affecting evaluation reliability. We identify such tests by running the test suite three times. If a test produces different results across runs (e.g., sometimes passing, sometimes failing), it is marked as flaky and excluded. Common causes of flakiness include: dependencies on external services, time-sensitive assertions, race conditions in concurrent code, and random data generation.

# <span id="page-25-1"></span>**A.4. Testbed Validation**

To ensure the reliability and reproducibility of our evaluation, we rigorously validate each milestone testbed across three core dimensions: milestone graph validity, runtime executability, and evaluation reliability.

# *A.4.1. Milestone Graph Validity*

We first verify the structural properties of the reconstructed history by construction. **Commit Completeness:** The commit set across all milestones is cross-checked against git log v\_start..v\_end, confirming 100% coverage with no gaps. **Dependency Consistency:** If commit in milestone depends on commit in milestone according to the commit-level DAG, then must depend on in the Milestone DAG. This constraint is verified for all inter-milestone commit pairs. **DAG Correctness:** DFS cycle detection and Kahn's topological sort confirm valid acyclic DAGs for all 7 repos.

# *A.4.2. Runtime Executability*

A reliable testbed must guarantee that errors stem from agent code, not infrastructure. Following the Milestone DAG, we reconstruct repository states by sequentially cherry-picking milestone commits

in topological order. **Testbed Compilability:** We verify that docker build completes without error and that the test framework's collection command (e.g., pytest –collect-only) succeeds in both START and END states for all repos in EvoClaw. **No Environment-Induced Errors:** We strictly monitor execution logs to ensure tests classified as error (reflecting environment/setup failures rather than assertion failures) remain negligible (≤0.10% across all repos).

# *A.4.3. Evaluation Reliability*

Finally, we assess the runtime behavior of the test suites to ensure they provide accurate evaluation signals. **Test Collection and Size Stability:** We statically extract test names from commit diffs and match them against runtime-collected node IDs, achieving an overall collection rate of 87.1% (3,563 of 4,090 tests). Furthermore, we compare test counts across milestones, confirming that the delta matches expected N2P (None-to-Pass, newly added tests) additions and removals. **Test Consistency:** To prevent false penalties, we ensure a negligible Pass-to-Fail (P2F) rate (≤0.026%), indicating no unintended regressions are introduced by milestone transitions. Additionally, each milestone is run three times to filter out flaky tests (yielding only 0–16 flaky tests per repo). **Coverage:** Every milestone with source changes must contain at least one F2P or N2P test. Milestones lacking test signals are labeled as maintenance tasks and excluded from the evaluation path, with their structural dependencies transitively bypassed to maintain DAG connectivity.

# <span id="page-26-1"></span>**B. EvoClaw Benchmark Details**

This appendix collects the construction artifacts of EvoClaw: the Software Requirement Specifications, the unified evaluation configuration shared across all agents, per-repository dataset statistics, and the full Milestone DAG visualizations.

# <span id="page-26-0"></span>**B.1. Software Requirement Specifications**

This appendix details the design, structural format, verification protocol, and refinement statistics of the SRS that serves as the task instruction for every milestone in EvoClaw.

**Design Principles.** Each milestone's SRS is written as a *minimally solvable* behavior- and contractlevel specification rather than a patch-reconstruction hint. The SRS deliberately avoids line-level edits, patch-like instructions, and identifiers such as file paths or function names unless those identifiers are themselves part of the public contract or are essential to making the requirement unambiguous. Three deliberately competing principles govern this trade-off. First, *specify what is required, not how to implement it*: state motivation, behavior, and acceptance criteria without prescribing the implementation. Second, *align with test intent, not test artifacts*: cover the evaluated behaviors without revealing test names, concrete inputs, or asserted values, exposing only public interface constraints when strictly necessary. Third, *ensure solvability*: include the essential formats, function signatures, edge cases, and non-inferable conventions needed to derive a correct implementation.

**SRS Structure.** Each milestone's SRS is organized as a sequence of *Feature Requirements*, each containing three fields: a *Problem* statement describing the symptoms and context that motivate the change, a *Requirements* block stating the intended functionality and constraints in an implementationagnostic way, and an *Acceptance* clause listing observable pass criteria without referencing test artifacts. Together, the three fields bound the implementation space while leaving the agent free to choose any compliant solution. Figure [17](#page-28-0) shows the Overview and two illustrative Feature Requirements from

the SRS for milestone M001 of zeromicro/go-zero, with the remaining requirements omitted for space. Full SRS instances for all milestones are released with the benchmark dataset.

**Human-in-the-Loop Verification.** The reverse-engineered SRS is refined through an agent-assisted, human-led verification loop. Human annotators iterate over three checks. In *static verification*, annotators read each SRS against the three design principles and revise any obvious violations until the document is internally consistent. In *independent dry-run verification*, annotators dispatch a strong coding agent to attempt each milestone in isolation using only the refined SRS, then inspect the failed Fail-to-Pass tests and add the minimal non-inferable conventions required for solvability. After several iterations, state-of-the-art models typically achieve 80% to 90% on independent runs, in line with the per-repository independent-task scores reported in Section [5.2.](#page-10-0) This indicates that residual unsolvability is small. In *continuous dry-run verification*, annotators replay each repository's DAG end-to-end to surface missing cross-milestone dependencies and SRS gaps that only emerge under sustained execution. A final end-to-end review by an independent senior expert closes the loop.

**Refinement Outcomes.** The verification loop converges quickly. Across EvoClaw, 71% of milestones underwent at least one revision, distributed across four categories: removing implementation leakage (39%), removing test leakage (31%), tightening inaccurate or underspecified requirements (25%), and adding missing functional requirements (5%). The convergence is also visible in evaluation impact. The first refinement round shifts per-milestone scores by approximately 5%, whereas the second round shifts them by at most 2%, indicating that residual SRS noise has limited effect on the relative ranking of agents.

# <span id="page-27-0"></span>**B.2. Evaluation Configuration Details**

We evaluate multiple model-agent configurations across four agent frameworks:

- **Claude Code** (v2.1.50)[1](#page-27-1) is Anthropic's terminal-based agent that operates with full shell access and autonomous multi-step planning. We pair it with Claude Opus 4.5, Claude Sonnet 4.5, Claude Opus 4.6, and Claude Sonnet 4.6, all supporting a 200K-token context window. Claude Code triggers automatic context compaction at approximately 80% of the context window (∼160K tokens), summarizing prior conversation history via server-side compression while preserving key context.
- **Codex CLI** (v0.105.0)[2](#page-27-2) is OpenAI's open-source CLI agent designed for code generation and editing tasks. We pair it with GPT 5.2, GPT 5.2-Codex, and GPT 5.3-Codex, all configured with xhigh reasoning effort and operating with a 272K-token context window. Codex CLI triggers auto-compaction at approximately 90% of context capacity (∼245K tokens). The underlying model is natively trained for multi-context-window operation, automatically summarizing the session and creating a fresh context window while preserving recent messages alongside the summary.
- **Gemini CLI** (v0.29.5)[3](#page-27-3) is Google's command-line agent for interacting with Gemini models in development workflows. We pair it with Gemini 3 Pro, Gemini 3.1 Pro, and Gemini 3 Flash, all supporting a 1M-token context window. Gemini CLI triggers context compression at approximately 50% of the context window. The compression mechanism invokes a specialized

<span id="page-27-1"></span><sup>1</sup><https://docs.anthropic.com/en/docs/claude-code>

<span id="page-27-2"></span><sup>2</sup><https://github.com/openai/codex>

<span id="page-27-3"></span><sup>3</sup><https://github.com/google-gemini/gemini-cli>

# <span id="page-28-0"></span>**Milestone M001 SRS (zeromicro/go-zero, v1.6.0**→**v1.9.3):** *go-redis v9 Upgrade with API Modernization*

**Overview.** This milestone upgrades the go-redis dependency from v8 to v9 across the Redis module (core/stores/redis, core/iox, zrpc/internal/clientinterceptors), requiring a new package import path, migration from callback-based to middleware-based hooks, error handling via errors.Is()/errors.As(), and updated sorted-set API signatures.

### **FR1: Migrate go-redis Import Path**

**Problem.** The Redis client library import path has changed from github.com/go-redis/redis/v8 to github.com/redis/go-redis/v9, causing compilation failures. **Requirements.**

- Update all import statements referencing the old go-redis v8 package to use the new v9 package path.
- Ensure all Redis-related source files compile with the new import path.
- Maintain the red alias convention for the imported package.

### **Acceptance.**

- When building the project, no import errors occur for the Redis package.
- All files in the redis module successfully import from the v9 package location.

### **FR2: Implement New Hook Interface Pattern**

**Problem.** The go-redis v9 library replaced the callback-based hook interface (BeforeProcess/AfterProcess methods) with a middleware-style hook interface (ProcessHook/ProcessPipelineHook functions that wrap the next handler). Existing hook implementations fail to compile.

### **Requirements.**

- Implement the DialHook(next red.DialHook) red.DialHook method that passes through to the next handler.
- Replace BeforeProcess/AfterProcess with a single ProcessHook(next red.ProcessHook) red.ProcessHook that captures the start time, starts the tracing span, invokes the next handler, ends the span, and records metrics and slow query logs.
- Replace BeforeProcessPipeline/AfterProcessPipeline with a single ProcessPipelineHook method with equivalent behavior for pipeline operations.
- Remove the context-based start-time storage mechanism used by the old hook pattern.
- Update the startSpan helper to return both the context and an endSpan closure.

### **Acceptance.**

- When a Redis command is executed, the tracing span is properly created and completed with correct status.
- When a Redis command exceeds the slow threshold, the slow query is logged.
- When a Redis command fails, the error is properly recorded in the span and metrics.
- When a pipeline of commands is executed, the combined duration is measured and logged appropriately.

· · ·

**Environment Dependency Changes.** The SRS additionally lists the Go package upgrades and additions required by this milestone (e.g., github.com/redis/go-redis/v9 v9.4.0 added, github.com/go-redis/redis/v8 removed, along with updates to roughly forty transitive dependencies). The full dependency list is included with each milestone's SRS in the released dataset.

Figure 17 | Excerpt of the SRS for milestone M001 of the zeromicro/go-zero repository (v1.6.0→v1.9.3) in EvoClaw, showing the Overview, two of the seven Feature Requirements (FR1 and FR2), and the trailing Environment Dependency section. Each Feature Requirement specifies a **Problem**, a **Requirements** block, and an **Acceptance** clause. Full SRS instances for all milestones are available at <https://huggingface.co/datasets/EvoClaw-Bench/EvoClaw-data>.

summarizer that distills the conversation into a structured snapshot preserving the overall goal, key knowledge, file system state, and the agent's current plan.

• **OpenHands** (v1.2.1)[4](#page-29-1) [Wang et al.](#page-21-6) [\(2025\)](#page-21-6) is an open-source platform for autonomous software development agents. Unlike the provider-specific frameworks above, OpenHands serves as a model-agnostic harness, enabling cross-provider evaluation under a unified agent architecture. We pair it with Claude Opus 4.6, GPT 5.3-Codex, Gemini 3 Flash, Kimi K2.5, and MiniMax M2.5. OpenHands uses an LLMSummarizingCondenser that triggers compression when total tokens surpass a model-dependent threshold (500K for Gemini 3 Flash, Gemini 3 Pro, and Gemini 3.1 Pro; 160K for all others), preserving the first 4 events (task description and initial context) and using the same underlying model to summarize the remainder.

**Runtime Configuration.** All agents operate within identical sandboxed Docker environments.

**Agent System Prompt.** Under the Continuous Task Evaluation setting, every agent receives the same system prompt (Figure [18\)](#page-30-0) regardless of framework or model. The prompt declares the agent's role as a software engineer, exposes the working directory, source-code paths, task-queue file, and per-milestone SRS directory, lists the four critical constraints (continuous context, in-scope edit boundaries, one-shot tagged submission, and an asynchronously updated streaming queue), and defines the monitor-implement-submit loop in which a git tag on the milestone identifier is the sole signal that triggers external evaluation.

# <span id="page-29-0"></span>**B.3. Detailed Dataset Statistics**

Table [3](#page-31-1) presents comprehensive per-repository statistics for EvoClaw. The table is organized into six major categories:

**Repository.** Basic repository information including the organization/repository name on GitHub, the number of source files (#Files), and total lines of code (#LoC) at the end version of the analyzed range.

**Release Range.** The version span analyzed by DeepCommit, specified by start and end tags, along with the delta lines of code (ΔLoC) representing the total code changes between these versions.

**Milestone DAG.** Statistics about the extracted milestone directed acyclic graph: the number of graded milestones (#M; the 3 non-graded context milestones are excluded), inter-milestone dependencies (#Deps), and the coefficient of variation (CV) of patch LOC across milestones. A higher CV indicates greater diversity in milestone complexity within the repository.

**Fix Patches.** Metrics characterizing the gold patches: average lines of code (Avg.LoC), average number of files modified (Avg.#F), and estimated human development time (HumanDT) required to implement each milestone.

<span id="page-29-1"></span><sup>4</sup><https://github.com/All-Hands-AI/OpenHands>

# <span id="page-30-0"></span>**Continuous Task Evaluation Agent System Prompt (e2e/prompt/v2.md)**

You are an expert **Software Engineer** working in a continuous integration environment. Your role is to sequentially implement software development tasks from a dynamic queue, maintaining a single continuous context throughout the entire session. You are responsible for writing code, running tests, and managing version control directly.

### **Environment**

- **Working Directory**: /testbed (the repository root).
- **Source Code**: {src\_dirs}.
- **Task Queue File**: /e2e\_workspace/TASK\_QUEUE.md (read-only, updated asynchronously by the system).
- **SRS Directory**: /e2e\_workspace/srs/ (contains {milestone\_id}\_SRS.md files).

### **Critical Constraints**

- 1. **Continuous Context**: You maintain FULL MEMORY of all previous tasks, decisions, and code changes. Use this knowledge to ensure consistency and avoid regressing previous fixes.
- 2. **Scope**: Only changes within the Source Code directories ({src\_dirs}) are validated for the final submission. However, you MAY (and should) modify or add tests to verify your work locally.
- 3. **One-Shot Submission**: Once you create a submission tag, the task is considered done and removed from the queue. You cannot edit a tagged submission.
- 4. **Streaming Queue**: The Task Queue is dynamic. New tasks may appear asynchronously as dependencies are satisfied. You must poll it continuously.

**Workflow.** Follow this continuous loop.

**Step 1: Monitor Task Queue.** Constantly read /e2e\_workspace/TASK\_QUEUE.md to see available tasks. If multiple tasks are available, prioritize them based on the order listed or dependency logic.

**Step 2: Implement Task.** For each task found in the queue:

- 1. **Read Requirements** from the SRS file at the path shown in TASK\_QUEUE.md (format: /e2e\_workspace/srs/{milestone\_id}\_SRS.md).
- 2. **Plan and Implement**: analyze the codebase, plan changes, and modify the code in {src\_dirs}. **Verify** by running existing tests or by creating new reproduction scripts to ensure that no existing functionality regresses.
- 3. **Refine** the implementation until satisfied.

**Step 3: Finalize and Submit.** When the implementation is complete and verified:

- 1. **Commit changes** with git add {src\_dirs} followed by git commit -m "Implement {milestone\_id}".
- 2. **Tag for submission** via git tag agent-impl-{milestone\_id}. This is the ONLY signal that the task is complete, and tagging immediately triggers the external evaluator and updates the Task Queue.

**Step 4: Loop.** After tagging, IMMEDIATELY re-read /e2e\_workspace/TASK\_QUEUE.md and repeat Step 2 for any new or remaining tasks. Leverage your memory of previous tasks to handle integration points and shared components effectively.

**Exit Condition.** Only stop when /e2e\_workspace/TASK\_QUEUE.md shows "(No tasks currently available)" AND you have completed processing all previously claimed tasks.

Figure 18 | System prompt provided to every agent under the Continuous Task Evaluation setting in EvoClaw. The prompt is framework-agnostic and is loaded as the agent's system message before the first SRS task is read. Variable placeholders such as {src\_dirs} and {milestone\_id} are filled in per repository and milestone at runtime.

<span id="page-31-1"></span>Table 3 | Detailed per-repository statistics for EvoClaw. HumanDT and HumanWT are average humanestimated development time and SRS writing time, respectively. #M counts graded milestones; the 3 non-graded context milestones are excluded.

|                           | Codebase |       | Release Range |          |        | Milestone DAG |       |        |
|---------------------------|----------|-------|---------------|----------|--------|---------------|-------|--------|
| Org/Repo                  | #Files   | #LoC  | Start         | End      | ΔLoC   | #M            | #Deps | LoC CV |
| zeromicro/go-zero         | 1,021    | 110K  | v1.6.0        | v1.9.3   | 6,403  | 23            | 25    | 1.29   |
| apache/dubbo              | 4,279    | 350K  | 3.3.3         | 3.3.6    | 4,154  | 12            | 9     | 0.76   |
| BurntSushi/ripgrep        | 159      | 48K   | 14.1.1        | 15.0.0   | 1,474  | 11            | 12    | 0.83   |
| nushell/nushell           | 1,727    | 264K  | 0.106.0       | 0.108.0  | 15,520 | 13            | 28    | 1.10   |
| element-hq/element-web    | 2,430    | 476K  | v1.11.95      | v1.11.97 | 7,657  | 18            | 12    | 0.87   |
| navidrome/navidrome       | 1,110    | 144K  | v0.57.0       | v0.58.0  | 5,900  | 9             | 9     | 1.02   |
| scikit-learn/scikit-learn | 1,314    | 280K  | 1.5.2         | 1.6.0    | 7,372  | 12            | 14    | 0.84   |
| Total/Average             | 12,040   | 1.67M | —             | —        | 48,480 | 98            | 109   | 0.96   |

|                           | Fix Patches |        |         |        | SRS     | Unit Tests |        |
|---------------------------|-------------|--------|---------|--------|---------|------------|--------|
| Org/Repo                  | Avg.LoC     | Avg.#F | HumanDT | Avg.#W | HumanWT | F2P        | P2P    |
| zeromicro/go-zero         | 278         | 10.2   | 4h-1d   | 1,330  | 4h+     | 2.2        | 1,812  |
| apache/dubbo              | 346         | 10.8   | 1-3d    | 1,138  | 1-2h    | 1.1        | 6,924  |
| BurntSushi/ripgrep        | 134         | 5.5    | 1-3d    | 879    | 30m-1h  | 1.3        | 1,057  |
| nushell/nushell           | 1,268       | 63.3   | 1-3d    | 1,528  | 1-2h    | 7.6        | 4,736  |
| element-hq/element-web    | 445         | 27.2   | 1-3d    | 1,546  | 2-4h    | 7.1        | 5,235  |
| navidrome/navidrome       | 656         | 13.2   | 1-3d    | 1,954  | 30m-1h  | 3.0        | 1,452  |
| scikit-learn/scikit-learn | 1,167       | 58.6   | 1-3d    | 1,580  | 30m-1h  | 97.2       | 22,308 |
| Total/Average             | 570         | 27.4   | 1-3d    | 1,348  | 2-4h    | 17.1       | 6,218  |

**SRS.** Software Requirement Specification statistics: average word count (Avg.#W) measuring specification length, and estimated human writing time (HumanWT) for authoring equivalent specifications. Note that SRS data is currently available for 5 repositories (dubbo, ripgrep, nushell, navidrome, scikit-learn).

**Unit Tests.** Test suite metrics: average Fail-to-Pass (F2P) tests that verify new functionality, and average Pass-to-Pass (P2P) tests ensuring backward compatibility. Notably, scikit-learn exhibits the highest F2P count (97.2) due to its comprehensive test coverage requirements.

# <span id="page-31-0"></span>**B.4. Milestone DAG Visualizations**

Figures [19](#page-33-0) to [22](#page-36-0) present the full Milestone DAGs for all seven repositories in EvoClaw. Each node is a card-style box representing a milestone, containing (top to bottom): a short ID, a descriptive title, summary statistics (number of commits, lines of code changed, and number of fail-to-pass tests), and one or more category tags. The border color of each node reflects its primary category: **Feature** (blue), **Bugfix** (red), **Refactor** (orange), **Enhance** (teal), or **Chore** (gray). Milestones belonging to multiple categories display all applicable tags. Gray nodes with dashed borders indicate non-graded milestones (3 in total: 2 in ripgrep, 1 in dubbo), which are included in the execution sequence for context continuity but excluded from scoring. The benchmark therefore contains 98 graded milestones and 3 non-graded milestones across all repositories (101 total). Solid red edges denote strong dependencies (upstream removal causes build or test failures downstream), while dashed gray edges denote weak dependencies (functionality degrades gracefully without the upstream milestone). Orange dashed

edges represent additional dependencies inferred during the DAG refinement stage. The DAGs are laid out top-to-bottom from upstream prerequisites to downstream dependents. Milestones with no dependency edges are grouped in a dashed "Independent Milestones" box at the bottom of each DAG.

# <span id="page-32-0"></span>**C. Extended Experimental Analysis and Discussion**

This appendix provides additional experimental analyses: qualitative agent-code quality patterns, per-model cumulative error trajectories on element-web, and a comparison case study against human-annotated Milestone DAGs.

# <span id="page-32-1"></span>**C.1. Agent Code Quality Analysis**

Beyond aggregate metrics, we examine representative cases to understand *how* agent-generated patches differ from human-written patches in structural quality. We identify three recurring quality anti-patterns through qualitative analysis.

**Responsibility Boundary Misplacement.** Figure [23](#page-37-2) illustrates a case from apache/dubbo (M004) where the agent correctly identifies the logic to implement but places it at the wrong abstraction level. The task requires skipping deserialization for stream parameters in FallbackArgumentResolver. The ground truth inserts the check in resolveValue(), allowing accept() to still claim the parameter, after which the framework injects the real stream instance. The agent instead places the check in accept(), causing the terminal resolver to reject the parameter entirely and triggering 3 P2P regressions. The agent's solution is *functionally plausible*—checking isStream() before processing is a reasonable heuristic—but violates the resolver chain's structural contract, revealing a quality gap in architectural reasoning.

**Shotgun Fixes.** Figure [24](#page-38-0) shows a pattern from nushell where the agent replaces targeted validation with overly permissive error suppression. The task requires break/continue outside loops to produce compile-time errors. The ground truth adds an is\_in\_loop() guard in compile\_break() and precisely exempts only the known catch block false positive. The agent instead deletes the is\_in\_loop() API entirely, removes all guards from compile\_break(), and globally suppresses NotInALoop errors across all block expressions. Tests still pass because an internal fallback in push\_break() happens to catch the error—but the SRS-mandated API contract is violated, and the deleted API blocks future evolution of the compiler's context-tracking infrastructure. This pattern exemplifies a broader quality gap: agents achieve test-passing behavior through coarse-grained suppression rather than precise, contract-preserving fixes.

**API Signature Degradation.** Figure [25](#page-39-0) demonstrates how a local algorithm choice can silently degrade a public API. In nushell's multi-output type checking, the ground truth iterates per inputoutput pair, keeping the expected field of OutputMismatch as a structured Type enum, adds a reusable utility in ty.rs, and cleans up obsolete workarounds (7 files modified). The agent groups by unique input types, which forces the expected field to become an opaque String (losing patternmatchability), defines only a local helper (leaving 35 lines of duplicate logic elsewhere), and retains stale FIXME workarounds (2 files modified). Both pass all F2P tests, but the agent's patch introduces architectural debt—weaker type signatures, missed deduplication, and retained technical debt—that compounds across milestones.

<span id="page-33-0"></span>![](_page_33_Figure_1.jpeg)

(a) element-web, v1.11.95  $\rightarrow$  v1.11.97 (18 milestones)

![](_page_33_Figure_3.jpeg)

(b) ripgrep,  $14.1.1 \rightarrow 15.0.0$  (13 milestones)

Figure 19 | Milestone DAGs for EvoClaw repositories (Part 1/4).

![](_page_34_Figure_1.jpeg)

(a) dubbo,  $3.3.3 \rightarrow 3.3.6$  (13 milestones)

![](_page_34_Figure_3.jpeg)

Figure 20 | Milestone DAGs for EvoClaw repositories (Part 2/4).

v0.58.0 (9 milestones)

![](_page_35_Figure_1.jpeg)

(a) nushell,  $0.106.0 \rightarrow 0.108.0$  (13 milestones)

Figure 21 | Milestone DAGs for EvoClaw repositories (Part 3/4).

<span id="page-36-0"></span>![](_page_36_Figure_1.jpeg)

(a) go-zero, v1.6.0  $\rightarrow$  v1.9.3 (23 milestones)

Figure 22 | Milestone DAGs for EvoClaw repositories (Part 4/4).

<span id="page-37-2"></span>![](_page_37_Figure_1.jpeg)

Figure 23 | Responsibility boundary misplacement in apache/dubbo (M004). The ground truth checks stream parameters in resolveValue(), preserving the resolver chain contract. The agent checks in accept(), ejecting the parameter from the terminal resolver and causing 3 P2P regressions.

These cases reveal a common quality pattern: agent-generated patches achieve *superficial correctness* (tests pass) while introducing *structural and maintainability issues*—misplaced abstractions, coarsegrained suppression, and degraded API contracts—that are invisible to automated evaluation but consequential in long-horizon development.

# <span id="page-37-1"></span>**C.2. Cumulative Error Analysis on element-web**

Figure [26](#page-39-1) contrasts continuous and independent evaluation on element-web across multiple models. Under continuous evaluation, errors introduced at early milestones, such as regressions and unresolved bugs, propagate through subsequent development stages, producing a pronounced *snowball effect* in which agents must operate on an increasingly unstable codebase. In contrast, Gemini 3 Flash under independent evaluation achieves substantially higher performance than all continuous runs, including those of frontier models such as GPT 5.2 and Claude Opus 4.5. This gap illustrates that independent-task evaluation effectively serves as an optimistic upper bound, substantially overstating an agent's ability to sustain coherent software evolution. Together, these results highlight long-horizon codebase maintenance as a central bottleneck: even state-of-the-art agents struggle to control error accumulation and technical debt when development unfolds continuously.

# <span id="page-37-0"></span>**C.3. Case Study: Human vs. DeepCommit Milestone DAG Construction**

We conduct a structured comparison between the Human-annotated Milestone DAG and the Deep-Commit DAG for the scikit-learn v1.5.2–v1.6.0 release interval (373 commits over 7 months). As shown in Figures [27](#page-40-0) and [28,](#page-41-0) the Human DAG consists of 14 milestones organized into 6 semantic groups with 20 dependency edges, whereas the DeepCommit DAG consists of 12 milestones organized into 6 data-driven groups with 14 dependency edges.

Both DAGs adopt a two-level hierarchy (groups → milestones). However, the Human DAG is structured

<span id="page-38-0"></span>![](_page_38_Figure_1.jpeg)

Figure 24 | Shotgun fix in nushell. The gold patch uses a *whitelist* strategy: compile\_break() returns NotInALoop as required by the SRS, and only the known catch-block false positive is exempted in parse\_internal\_call. The agent uses a *blacklist* strategy: it suppresses *all* NotInALoop errors across every block expression and deletes the is\_in\_loop() API. Tests pass only because push\_break() has an internal fallback.

around manually defined release-planning themes (e.g., framework evolution, backend compatibility, quality assurance), while the DeepCommit DAG reflects phases and clusters induced from commitlevel dependency topology. In addition, the Human DAG distinguishes functional and process-level dependencies with explicit strength annotations, whereas the DeepCommit DAG encodes dependencies derived from structural signals in the commit graph.

This case study is not intended as a performance comparison. Rather, it examines how distinct construction principles—semantic curation versus topology-driven aggregation—lead to systematically different milestone abstractions and dependency structures.

# *C.3.1. Commit Coverage*

The 201 DeepCommit commits form a strict subset of the 373 Human commits. The 172 filtered commits result from the pipeline's source-file filtering and F2P test requirements, which preferentially exclude Human milestones whose commits have low inter-dependency, since such commits tend to

<span id="page-39-0"></span>![](_page_39_Figure_1.jpeg)

<span id="page-39-1"></span>Figure 25 | API signature degradation in nushell's type checker. The agent's group-by-input algorithm forces OutputMismatch.expected from a structured Type enum to an opaque String, losing pattern-match capability. The agent also omits workaround cleanup and utility deduplication (2 vs. 7 files modified).

![](_page_39_Figure_3.jpeg)

Figure 26 | Continuous vs Independent evaluation on element-web. The shaded area highlights how error accumulation in continuous mode causes a cost-effective model (Gemini 3 Flash, Independent) to outperform frontier models in continuous mode.

modify isolated files and fail to form strongly connected components in the dependency-induced commit DAG. Among the most affected categories, 73% of build system modernization commits and 78% of Array API interface adaptation commits are excluded, followed by CI/release engineering (56%) and small independent bug fixes (39%). This strategy retains a tighter, more interconnected

<span id="page-40-0"></span>![](_page_40_Figure_1.jpeg)

Figure 27 | Human-annotated and DeepCommit milestone decompositions for scikit-learn v1.5.2– v1.6.0. Top: Milestones grouped by human analyzers (M1–M6). Bottom: milestone grouped by DeepCommit (G1–G6). Each block summarizes representative commits, commit count, LoC, and time span.

<span id="page-41-0"></span>![](_page_41_Figure_1.jpeg)

Figure 28 | Structural comparison of Human and DeepCommit Milestone DAGs. The Human DAG contains 14 milestones and 19 dependencies; The DeepCommit DAG contains 12 milestones and 14 dependencies. Edges denote functional or process-level dependencies with strong/weak strength.

Table 4 | Structural overview of the DeepCommit Milestone DAG and the Human-annotated Milestone DAG

| Dimension       | Human DAG           | DeepCommit DAG      |  |  |  |
|-----------------|---------------------|---------------------|--|--|--|
| Leaf milestones | 14                  | 12                  |  |  |  |
| Groups          | 6                   | 6                   |  |  |  |
| Covered commits | 373                 | 201                 |  |  |  |
| DAG edges       | 20                  | 14                  |  |  |  |
| Edge types      | FUNC (15) + NFR (5) | FUNC (13) + NFR (1) |  |  |  |
| Strong edges    | 2                   | 8                   |  |  |  |
| Weak edges      | 18                  | 6                   |  |  |  |

subgraph suited for benchmark construction, but omits process-level patterns such as "code first, document later" that the Human DAG captures via NFR edges.

# C.3.2. Clustering Divergence and Structural Differences

Although both DAGs have 6 groups, their clustering methods are fundamentally different, producing an Adjusted Rand Index (ARI) of only 0.538, indicating moderate agreement despite identical group counts.

**Top-down semantics vs. bottom-up topology.** The human annotator reads the release notes<sup>5</sup> and resolved issues<sup>6</sup> to define semantic cluster centers (e.g., "Estimator Tags System Redesign"  $\rightarrow$  M1.2, "Deprecations and Removals"  $\rightarrow$  M3.2), then assigns commits by *developer intent*. DeepCommit instead constructs a commit-level DAG from code dependencies and partitions it via seed discovery and consolidation. The resulting chain M1.1 $\rightarrow$ M1.2 $\rightarrow$ M2.1 $\rightarrow$ M2.2 $\rightarrow$ M2.3 is a contiguous topological ordering.

The contingency matrix (Figure 29) illustrates this difference from both directions. Human M5.1 (Stability Fixes, 37 shared commits) groups bug fixes spanning the entire release window by shared intent, but DeepCommit distributes them across eight milestones (M1.1:13, M1.2:12, M2.1–M2.3:7, etc.) according to which code regions they touch. Conversely, DeepCommit M1.1 (41 commits) clusters code-adjacent early-phase work into a single topological block, drawing from four distinct Human categories: stability fixes (13), deprecation cleanup (9), usability improvements (6), and release engineering (6).

**Group semantics and dependency structure.** The two construction methods yield different group semantics. Human groups reflect *strategic release themes* with high internal coherence (e.g., M1: testing  $\rightarrow$  tags  $\rightarrow$  validation  $\rightarrow$  routing, all under "Framework Evolvability"), whereas DeepCommit groups reflect *topological phases*: M1 ("Framework Evolvability," 76 commits) aggregates license cleanup, metadata routing, and estimator bug fixes—commits that are code-adjacent in time but span multiple developer-facing themes. This difference extends to edges. The Human DAG distinguishes FUNC edges (15, functional preconditions) from NFR edges (5, process-level dependencies pointing to Documentation) and annotates predominantly weak couplings (18 weak / 2 strong), expressing that most milestones can proceed in parallel. DeepCommit has 8 strong / 6 weak edges, with the main phase chain entirely strong, reflecting strict topological ordering rather than semantic coupling.

<span id="page-42-0"></span><sup>&</sup>lt;sup>5</sup>https://scikit-learn.org/stable/auto\_examples/release\_highlights/plot\_release\_highlights\_1\_6\_0.html

<span id="page-42-1"></span><sup>&</sup>lt;sup>6</sup>https://github.com/scikit-learn/scikit-learn/milestone/57?closed=1

<span id="page-43-0"></span>![](_page_43_Figure_1.jpeg)

Figure 29 | Contingency matrix of commit assignments (Human  $\times$  DeepCommit) for the 201 shared commits. The dominant Human M6.1  $\leftrightarrow$  DeepCommit M6.1 block (71 commits) reflects high agreement on documentation, while the dispersed pattern across DeepCommit M1.1–M2.3 reveals how phase-based partitioning fragments intent-based Human milestones.

Similarly, the Human DAG models cross-cutting workflows—five milestones connect to M6.1 via NFR edges ("code first, document later")—while DeepCommit's M6.1 has only 2 incoming edges, since its bottom-up construction does not capture process-level conventions.

# C.3.3. Agreement Analysis and Summary

Despite moderate overall agreement (ARI = 0.538, Normalized Mutual Information = 0.444), certain regions converge strongly. We measure per-milestone overlap as the fraction of a Human milestone's shared commits that map to a single DeepCommit milestone. Documentation shows the highest overlap: 89% of Human M6.1 commits (71 of 80) land in DeepCommit M6.1. Array API milestones also align well (Human M2.1→DeepCommit M5.1: 100%; Human M2.2: 60%), as do performance optimizations (Human M5.2→DeepCommit M6.2: 60%). These high-overlap milestones share distinctive file-modification patterns and isolated module boundaries. Conversely, intent-defined milestones show low overlap—Human M5.1 (Stability Fixes: 35%), M3.2 (Deprecation Cleanup: 39%), M1.4 (Metadata Routing: 30%)—because their commits span multiple modules and time periods, united by purpose rather than code proximity.

In summary, DeepCommit recovers milestone boundaries consistent with human annotation when technical boundaries are clear, but falls back to phase-based partitioning for cross-module, intent-defined work. The Human DAG's structure (strategically coherent groups, FUNC/NFR edge distinction, and cross-cutting workflow modeling) captures developer reasoning that remains difficult to infer from dependency topology alone.