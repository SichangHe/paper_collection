# **VeriSkill: A Self-Evolution Framework for Program Verification Skills**

**Changguo Jia**<sup>1</sup><sup>∗</sup> **, Tianqi Zhao**<sup>2</sup><sup>∗</sup> **, Zhiyou Xiao**<sup>1</sup> **, Weiming Zhang**<sup>3</sup> **, Minghui Zhou**<sup>1</sup>†

<sup>1</sup>Peking University, Beijing, China <sup>2</sup>Zhongguancun Laboratory, Beijing, China <sup>3</sup>Shanghai Jiao Tong University, Shanghai, China jiachangguo@stu.pku.edu.cn, zhaotq@zgclab.edu.cn, xiaozhiyou@stu.pku.edu.cn, WeimingZhang\_2020@sjtu.edu.cn, zhmh@pku.edu.cn

### **Abstract**

Automating program verification with LLM agents requires generating specifications, annotations, auxiliary lemmas, and tool invocations, all of which depend on reusable skills. A natural remedy is skill self-evolution: distilling skills from trajectories and refining them through feedback. However, existing evolution methods struggle with program verification tasks because they cannot reliably identify skill-specific failures or extract actionable signals from opaque verifier feedback. In this paper, we propose VeriSkill, a self-evolution framework built for program verification. It attributes verification failures to skill deficiencies, distills diagnostic signatures into reusable lessons, and iteratively refines candidate skills, admitting only revisions that improve verification performance while preserving program semantics. Experiments show that VeriSkill consistently outperforms all baselines across multiple verification tools, agent frameworks, and LLM backends.

# **1 Introduction**

Program verification aims to establish that a program implementation satisfies its formal specification (Hoare 1969). In practice, users manually annotate programs with function contracts, intermediate assertions, and auxiliary lemmas, after which verification tools generate the corresponding verification conditions and invoke Satisfiability Modulo Theories (SMT) solvers to discharge them. Constructing correct annotations requires considerable expertise and manual effort, making program verification at scale challenging. Recently, the emergence of LLM agents and agent skills has made fully automated program verification increasingly feasible.

Agent skills encapsulate reusable operational knowledge that enables LLM agents to perform specialized tasks. A skill typically contains task-specific workflows, tool-use instructions, and error-handling procedures. Empirical studies show that skill quality substantially affects agent behavior (Li et al. 2026; Zhou et al. 2026). Yet writing and maintaining a high-quality skill requires expert effort that is always in short supply. *Skill self-evolution* addresses this bottleneck by automatically revising skills based on accumulated task experience.

Most existing methods of skill self-evolution are domainagnostic, extracting lessons from successful and failed execution trajectories and incorporating them into skills. Representative methods follow this trajectory-based paradigm in different ways. Trace2Skill distills trajectory-local experience into transferable instructions (Ni et al. 2026). SkillOpt-Lite streamlines skill self-evolution into file-system-based trajectory exploration, consensus attribute mining, and independent validation gating (Shen, Li, and Zhang 2026), while EvoSkill analyzes execution failures to iteratively refine structured skills under validation-based frontier selection (Alzubi et al. 2026).

However, general methods of skill self-evolution are not well suited to program verification. A failed verification attempt does not necessarily indicate a skill deficiency, making it difficult to determine whether the skill should be revised. For example, even when the source program and its annotations are both correct, verification may fail because of limitations in the underlying SMT solver, which are unrelated to the skill. Moreover, outputs from verification tools report failed verification conditions, which are not directly reusable procedural knowledge. For example, an incorrect loop invariant often results from a flawed mathematical derivation, while the resulting failed verification conditions provide little guidance for correcting the derivation. As a result, program verification skills require a specialized self-evolution framework.

In this paper, we propose VeriSkill, a self-evolution framework for program verification skills that turns verification failures into actionable improvements. Unlike generic evolution approaches, VeriSkill precisely isolates skillrelated failures, extracts generalizable lessons while discarding instance-specific noise, and admits only validated lessons that measurably boost verification success without breaking program semantics—making skill self-evolution both targeted and trustworthy. The framework operates in three steps. First, to determine whether a failed verification attempt indicates a skill deficiency, VeriSkill performs responsibility attribution for each verification failure by examining the failed task, verifier feedback, current skill, generated artifact, human-verified artifact, and evolution memory. It distinguishes failures and retains only the skill-responsible failures as evolution signals. Second, to turn failed verification conditions into reusable procedural knowledge, VeriSkill clusters failures by diagnostic signatures and abstracts a reusable lesson from each failure pattern. Each signature captures where

<sup>∗</sup>These authors contributed equally.

<sup>†</sup>Corresponding author.

the verification attempt fails, what kind of skill deficiency is exposed, and what procedural guidance is missing. Humanverified artifacts are used as evidence for the missing guidance, but instance-specific verification details are removed so that the resulting lesson specifies general applicability conditions and non-applicable cases. Finally, Veriskill iteratively refines candidate skills through executable validation. Each lesson is integrated into a candidate skill and revised on same-pattern attribution and transfer sets until it passes local checks. Locally valid candidates are admitted only if they improve validation performance while preserving program semantics. All outcomes are stored in evolution memory to guide later revisions.

We evaluate VeriSkill across different verification tools, including Dafny, Frama-C, and VeriFast. VeriSkill consistently outperforms non-evolution and existing baselines of skill self-evolution, while ablation studies confirm the contribution of its core components. Moreover, the evolved skills retain their effectiveness across different agent frameworks and LLM backends. A case study further shows how VeriSkill turns a specific verifier failure into a reusable skill update, explaining its advantage over generic methods of skill self-evolution. To conclude, our primary contributions are as follows:

- We identify validated verification-responsibility patterns as the proper learning unit for reliable skill evolution in program verification.
- We propose the first self-evolution framework for program verification skills, which attributes reusable deficiencies, abstracts transferable knowledge, and iteratively validates revisions before admission.
- We implement the framework as a prototype tool. Experiments show that VeriSkill consistently outperforms all baselines across multiple verification tools, agent frameworks, and LLM backends.

### 2 Related Work

#### 2.1 Skill Self-evolution

Recent work learns reusable skills from agent experience. Trace2Skill consolidates trajectory-local lessons into transferable instructions (Ni et al. 2026). SkillOpt and SkillOpt-Lite refine skill text from rollout feedback and retain revisions through validation (Yang et al. 2026a; Shen, Li, and Zhang 2026). EvoSkill analyzes execution failures and preserves effective skill folders through validation (Alzubi et al. 2026), while SkillCAT contrasts successful and failed trajectories before replaying candidate revisions (Chen et al. 2026). CoEvoSkills co-evolves a surrogate verifier to provide revision signals (Zhang et al. 2026), whereas AutoSkill derives and reuses skills from dialogue and interaction traces for lifelong learning (Yang et al. 2026b). These methods mainly rely on task outcomes or learned verification; VERISKILL instead uses formal-verifier evidence to attribute skill-responsible failures and admits revisions only under semantic-preservation constraints.

### 2.2 LLM-Assisted Program Verification

Recent studies investigate how LLMs can assist programverification tasks. DafnyBench establishes a benchmark protocol for proof-hint generation with iterative verifier feedback (Loughridge et al. 2024), while FM-Bench decomposes program verification into multiple subtasks across several specification languages to evaluate distinct verification capabilities (Cao et al. 2025). AxDafny further demonstrates that iterative generation and verification can be orchestrated through an agentic workflow (Breen et al. 2026).

A second line of work synthesizes specifications and annotations through verifier-guided refinement. SpecGen generates pre- and postconditions (Ma et al. 2024), AutoSpec iteratively refines specifications according to verifier feedback (Wen et al. 2024), and Laurel first localizes a missing Dafny assertion from verifier diagnostics before generating it (Mugnier et al. 2025). Preguss extends this paradigm to large C programs by combining static-analysis-guided decomposition with verifier-driven refinement of interprocedural specifications (Wang et al. 2026).

Other systems focus on invariant synthesis and structured proof repair. Lemur integrates LLM-generated lemmas and invariants into deductive verification through backtracking (Wu, Barrett, and Narodytska 2024), LaM4Inv couples LLM generation with bounded model checking (Wu et al. 2024), and Loopy applies Houdini-style filtering to candidate invariants (Kamath et al. 2023). AutoVerus further orchestrates specialized agents for different verifier error types and performs staged proof refinement (Yang et al. 2025), resembling VeriSkill's use of diagnostic signatures to organize verification failures. However, across these systems, verifier feedback is primarily consumed within individual attempts to repair a specific artifact. The resulting procedural knowledge is not externalized as a persistent skill reusable across tasks, verifiers, and model backbones. VeriSkill fills this gap by converting validated verifier feedback into a portable skill artifact.

## 3 Problem Formulation

Our goal is to evolve a verification skill into a more effective one that improves the agent's performance on program-verification tasks. Specifically, let  $\pi$  denote the agent's solution-generation policy. Then  $\pi(\cdot \mid x, S)$  is the conditional distribution over candidate solutions given task x and skill S, where  $\cdot$  denotes the candidate-solution argument of the distribution. Given a skill S, a distribution  $\mathcal D$  over verification tasks, a program-verification task  $x \sim \mathcal D$ , and a candidate solution  $a \sim \pi(\cdot \mid x, S)$ , the expected verification success rate of S is defined as

$$J(S) = \mathbb{E}_{x \sim \mathcal{D}} \mathbb{E}_{a \sim \pi(\cdot | x, S)} [V(x, a)], \tag{1}$$

where  $V(x,a) \in \{0,1\}$  indicates whether the candidate solution passes the verifier. Therefore, the objective of skill self-evolution is to find a better skill:

$$S^* \in \arg\max_{S} J(S). \tag{2}$$

At the same time, any candidate solution must satisfy the semantic-preservation constraint:

$$M(x,a) = 1, (3)$$

![](_page_2_Figure_0.jpeg)

Figure 1: Overview of VeriSkill. The framework (1) attributes failures and retains only skill-responsible cases, (2) clusters compatible diagnostic signatures to abstract reusable lessons, and (3) iteratively refines candidate skills through executable validation.

where M(x, a) indicates that the candidate solution should not modify the original executable program.

During this process, a verification failure cannot be directly equated with a defect in the skill. A failure may arise from the program or annotation itself, from the limits of the verification tool's solving capabilities, or from the agent failing to follow the existing skill guidance. If a skill is modified directly based on failure evidence, the system might encode problems that cannot be solved by skill updates, or accidental execution errors, into the skill, potentially pushing the skill self-evolution in the wrong direction.

Therefore, reliable skill self-evolution for program verification requires three stages. First, it performs responsibility attribution to identify failures that can serve as valid signals for skill updates. Second, it conducts fine-grained diagnosis of skill defects and abstracts reusable lessons from failure clusters. Finally, it uses executable validation and an admission mechanism to determine whether a candidate revision truly improves the complete skill. Together, these requirements transform skill optimization from "modify whenever a failure is observed" into "admit only updates that have been attributed, abstracted, and validated".

# **4 VeriSkill**

This section presents the proposed skill-evolution framework, with three stages detailed in the following subsections. We also illustrate the overall workflow in Figure 1 and provide the corresponding pseudocode in Algorithm 1.

### **4.1 Stage 1: Failure Attribution and Filtering**

The first stage determines whether a verification failure should trigger skill revision. Its purpose is to distinguish failures attributable to the skill from those caused by the task or verification environment. Given a failed task, VeriSkill performs responsibility attribution by jointly considering the generated result, verifier output, skill, human-verified reference solution, and evolution memory. It classifies the failure into the following four categories.

- *Task unsatisfiability*: The source program and annotations do not support the verification objective.
- *Prover limitation*: The proof obligation is reasonable, but the current prover lacks the capability to discharge it.
- *Skill noncompliance*: The skill provides relevant guidance, but the agent fails to follow it.
- *Skill knowledge gap*: The skill lacks the reusable procedural knowledge required for the verification task.

The first two categories are excluded from skill evolution, whereas the latter two are retained as skill-related failures.

VeriSkill also consults historical attribution evidence in evolution memory. Records identifying similar failures as task unsatisfiability, prover limitation, or outcomes of invalid revisions help prevent repeated misattribution. Based on the current evidence and this history, VeriSkill retains only skill-related failures that are likely to be improved through textual updates. These evolvable failures form the basis for lesson abstraction and revision generation in the subsequent stages.

# **4.2 Stage 2: Lesson Abstraction via Pattern-Level Defect Clustering**

After Stage 1 identifies skill-related failures, Stage 2 determines how the skill should be revised without generating a patch directly from an individual example. VeriSkill extracts diagnostic signatures, clusters failures with shared patterns, abstracts their common verification responsibility, and generates candidate lessons using evolution memory.

VeriSkill first extracts a diagnostic signature for each failure. The diagnostic signature contains the following three components.

- Proof-obligation localization: Identify where the proof fails, such as invariant initialization, invariant preservation, memory safety, or termination.
- *Verification-responsibility abstraction*: Identify the reusable proof responsibility missing from the candidate solution, such as establishing entry facts, preserving an invariant, or supplying an intermediate lemma.
- A skill failure mechanism: Identifies how the skill text causes the failure, such as missing, unclear, overly abstract, or difficult-to-locate guidance.

Using these signatures, VeriSkill groups failures with a shared structure into failure-pattern clusters. It then abstracts the common verification responsibility within each cluster as its aggregate diagnosis. Reasoning over a cluster allows VeriSkill to capture semantically equivalent proof responsibilities across syntactically different solutions and avoids overfitting a revision to a single example.

When abstracting verification responsibility, Veriskill refers to human-verified reference artifacts, but does not directly turn them into lessons. A reference solution typically contains two kinds of information: reusable verification responsibilities for the same type of task, and the specific path used for the current example, such as a particular invariant form, assertion location, lemma expression, or constant choice. Veriskill retains only the former and removes the latter, thereby avoiding the hard-coding of example-level outputs into the skill.

To better leverage historical experience when reasoning about strategies of skill self-evolution, Veriskill also retrieves records from evolution memory for the current failure pattern, including prior attributions, abstracted responsibilities, lessons, validation outcomes, and applicability conditions. Accepted revisions provide reusable procedural knowledge as guidance, whereas rejected or skipped revisions prevent repeated ineffective or unsafe updates. With memory, lesson generation becomes a pattern-level update constrained by historical validation evidence rather than a local induction from the current failed examples.

Finally, Veriskill generates candidate lessons based on the failure pattern, shares verification responsibility, and evolution memory. A candidate lesson must specify its applicability conditions, concrete proof steps, and inapplicable cases, while avoiding task IDs, file names, concrete variable names, or constants. The resulting lesson is thus not an example-level patch, but reusable procedural knowledge for a class of similar failure patterns.

#### 4.3 Stage 3: Executable Validation and Admission

The goal of the third stage is to iteratively refine the candidate skill so that it transfers to unseen cases with the same failure pattern before admission. Given the current skill  $S_t$ , a

### Algorithm 1 VeriSkill Evolution Loop

```
Require: Current skill S, evolution tasks T, validation tasks
     \mathcal{V}, evolution memory EM
 1: loop
 2:
        // Stage 1: Failure attribution and filtering
 3:
         E \leftarrow \text{ExecuteAndCollect}(S, T)
         F \leftarrow \text{AttributeFailures}(E, S, EM)
 4:
 5:
         F_{\text{skill}} \leftarrow \text{FilterEvolvable}(F, EM)
 6:
        if F_{\text{skill}} = \emptyset then
 7:
           break
 8:
         end if
 9:
        // Stage 2: Lesson abstraction via pattern-level defect
         clustering
10:
         \mathcal{C} \leftarrow \text{DiagnoseAndCluster}(F_{\text{skill}}, S, EM)
11:
         C \leftarrow \text{SelectCluster}(\mathcal{C}, EM)
12:
         (A_C, T_C) \leftarrow \text{SplitAttributionTransfer}(C)
13:
         K \leftarrow \text{AbstractResponsibility}(A_C, S, EM)
14:
        if K = \emptyset then
15:
            EM \leftarrow \text{RecordSkipped}(EM, C)
16:
           continue
17:
         end if
18:
        // Stage 3: Executable validation and admission
19:
20:
            \ell \leftarrow \text{BuildLesson}(K, S, EM)
            S' \leftarrow \text{ConstructCompleteCandidate}(S, \ell, EM)
21:
            Z \leftarrow \text{EvaluateLocalCandidate}(S, S', A_C, T_C)
22:
            EM \leftarrow \text{RecordLocalOutcome}(EM, C, \ell, S', Z)
23:
24:
         until LocalPasses(Z) \vee BudgetExhausted(C)
25:
        if \neg \text{LocalPasses}(Z) then
           continue
26:
27:
        if \widehat{J}_{\mathcal{V}}(S') > \widehat{J}_{\mathcal{V}}(S) \wedge M(x_i, a_i^{S'}) = 1, \ \forall x_i \in \mathcal{V} then
28:
29:
30:
            EM \leftarrow \text{RecordAccepted}(EM, C, \ell, S', Z, \mathcal{V})
31:
            EM \leftarrow \text{RecordRejected}(EM, C, \ell, Z, \mathcal{V})
32:
33:
        end if
34: end loop
35: return S
```

candidate lesson  $\ell_c$ , and evolution memory EM, VeriSkill first constructs a candidate skill:

$$S' = \text{Revise}(S_t, \ell_c, EM). \tag{4}$$

This is a controlled revision rather than a textual append. The lesson is integrated into the appropriate part of the skill according to its applicability scope and revision type. For example, the candidate may rewrite an unclear process, add conditional guidance for an uncovered case, or turn an abstract principle into explicit execution steps, while preserving unrelated sections and the original task contract.

VeriSkill then reruns the agent and verifier with the candidate skill S' on attribution cases and held-out transfer cases from the same failure pattern. Let  $\mathcal{A}_c$  denote the attribution cases used to analyze the failure pattern and construct the lesson, and let  $\mathcal{T}_c$  denote same-pattern disjoint transfer cases that were not involved in lesson construction. Their local

effects are defined as

$$\widehat{\tau}_{\text{attr}}(S') = \frac{1}{|\mathcal{A}_c|} \sum_{x_i \in \mathcal{A}_c} \left[ V(x_i, a_i^{S'}) - V(x_i, a_i^{S_t}) \right],$$

$$\widehat{\tau}_{\text{trans}}(S') = \frac{1}{|\mathcal{T}_c|} \sum_{x_i \in \mathcal{T}_c} \left[ V(x_i, a_i^{S'}) - V(x_i, a_i^{S_t}) \right].$$
(5)

Here,  $\widehat{\tau}_{attr}$  checks whether the candidate skill repairs the failures that motivated the revision, while  $\widehat{\tau}_{trans}$  checks whether the same revision transfers to unseen cases with the same failure pattern. Local testing also rejects pass-to-fail regressions or modifications to the original executable code. If the candidate fails either local test, Veriskill uses the resulting repair and regression evidence to refine the lesson and revise the skill again for the same failure pattern. This revise—test loop continues until a candidate passes both local tests or the failure-pattern budget is exhausted.

Only a locally valid candidate proceeds to the disjoint validation set  $\mathcal V$ . The success rate on the validation set is defined as

$$\widehat{J}_{\mathcal{V}}(S) = \frac{1}{|\mathcal{V}|} \sum_{x_i \in \mathcal{V}} V(x_i, a_i^S), \tag{6}$$

where  $a_i^S$  denotes the candidate artifact generated by the agent for task  $x_i$  under the guidance of skill S. A candidate that passes frozen validation is admitted directly. Specifically, Veriskill requires the candidate skill to strictly improve the validation-set success rate while preserving the integrity of all validation tasks:

$$S_{t+1} = \begin{cases} S', & \widehat{J}_{\mathcal{V}}(S') > \widehat{J}_{\mathcal{V}}(S_t) \land M(x_i, a_i^{S'}) = 1, \\ & \forall x_i \in \mathcal{V}, \\ S_t, & \text{otherwise.} \end{cases}$$
 (7)

An admitted skill becomes the evolution target for the next round. Meanwhile, every candidate revision, whether accepted, rejected, or skipped, is recorded in evolution memory with its failure pattern, attribution, lesson, validation outcome, and applicability conditions. Later rounds reuse these records to guide verification-responsibility attribution and lesson generation while avoiding revisions already shown to be ineffective or risky.

Thus, through local probing, iterative validation, and memory updates, VERISKILL turns candidate lessons into skill self-evolution constrained by executable verification evidence.

### 5 Experimental Setup

**Datasets and Benchmarks.** We evaluate on three verification tools with disjoint datasets and benchmarks.

*Dafny*: Datasets and benchmarks are constructed from DafnyBench (Loughridge et al. 2024). Because DafnyBench comprises a large set of Dafny programs and is not inherently intended as a benchmark for C-to-Dafny translation, we sample 200 tasks, manually construct plain-C inputs paired with hidden Dafny references, and split them 4:1:5 into training, validation, and benchmark.

Frama-C: Datasets are built by searching GitHub with Frama-C/WP and ACSL keywords, inspecting candidate repositories in descending relevance order, and selecting four relevant repositories as data sources (Frama-C 2026b; Blanchard 2020; Frama-C 2026a; Fraunhofer FOKUS 2026). We parse function-level examples, strip ACSL annotations to form plain-C inputs, filter and deduplicate verifier-passing references, and manually check the resulting pairs. Two experts with formal-verification experience cross-validate the correctness of the annotations. This yields 85 C-to-ACSL evolution tasks split 68/17 for training and validation. The benchmark is the Frama-C-Problems benchmark (Patnaik 2020).

*VeriFast*: Since little existing C-to-VeriFast benchmark is available, we construct both the datasets and benchmarks from GitHub sources (VeriFast 2026; Jacobs 2026), following the same procedures as Frama-C. After function parsing, VeriFast-annotation stripping, verifier filtering, deduplication, and manual checking, we obtain 200 C-to-VeriFast tasks, split them 4:1:5 into training, validation, and benchmark.

**Agents and baselines.** The main comparison uses two agent/backbone pairs: **Claude Code** (Anthropic 2026b) with **Opus 4.8**, and **Codex** (OpenAI 2026) with **GPT 5.6 Sol**. For cross-model transfer, we run GLM-5.2, Kimi-K2.7, Qwen3.7-Max, DeepSeek-V4-Pro, and Qwen3-Coder through the same Terminus terminal-agent wrapper (Terminal-Bench 2026), keeping prompts, verifier commands, and task environments fixed while varying only the backend model.

We compare VeriSkill against 7 baselines. No Skill gives the agent only the task prompt, while LLM Skill adds a onepass generated verifier skill following the practice (Yan et al. 2026). Human Skill uses GitHub-sourced expert skills for Dafny and Frama-C, both validated by a formal-verification expert with seven years of experience; for VeriFast, where little suitable public skill was found, the same expert authored the skill. **Skill-Creator** is Anthropic's official skill-authoring framework, which drafts reusable skill folders and iteratively revises them from self-graded feedback (Anthropic 2026a). EvoSkill maintains a Pareto frontier of agent programs and mutates selected frontier members by proposing new skill folders from sampled failure batches (Alzubi et al. 2026). AutoSkill derives reusable skills from dialogue and interaction traces (Yang et al. 2026b). SkillOpt-Lite evolves skill text through trajectory exploration and validation gating (Shen, Li, and Zhang 2026). All methods receive the same inputs, verifier settings, and target-agent configuration.

Metrics. Following patch-correctness assessment in automated program repair and execution-based evaluation in program translation (Le et al. 2018; Ye, Martinez, and Monperrus 2021; Rozière et al. 2020), our primary metric is PASS, defined as the percentage of benchmark tasks for which the generated artifact is accepted by the target verifier and also passes semantic-preservation checks. The semantic-preservation check rejects artifacts that edit executable behavior or introduce verification-bypass constructs. For annotation-only tracks, this requires the executable C

| Verifier                                              | No Skill | LLM Skill | Human Skill | Skill-Creator | EvoSkill | AutoSkill | SkillOpt-Lite | VeriSkill | ∆     |
|-------------------------------------------------------|----------|-----------|-------------|---------------|----------|-----------|---------------|-----------|-------|
| Agent framework: Claude Code • LLM backbone: Opus 4.8 |          |           |             |               |          |           |               |           |       |
| Dafny                                                 | 14.0     | 21.3      | 7.7         | 39.3          | 32.3     | 41.0      | 42.3          | 57.3      | +43.3 |
| Frama-C                                               | 56.9     | 47.1      | 58.2        | 58.2          | 54.2     | 60.8      | 65.4          | 74.5      | +17.6 |
| VeriFast                                              | 38.0     | 32.0      | 24.3        | 58.3          | 53.0     | 62.7      | 78.3          | 84.0      | +46.0 |
| Agent framework: Codex • LLM backbone: GPT 5.6 Sol    |          |           |             |               |          |           |               |           |       |
| Dafny                                                 | 17.0     | 27.3      | 12.3        | 21.7          | 30.3     | 35.7      | 62.7          | 66.0      | +49.0 |
| Frama-C                                               | 57.5     | 38.6      | 59.5        | 56.2          | 55.6     | 60.1      | 66.7          | 83.0      | +25.5 |
| VeriFast                                              | 41.7     | 44.0      | 35.0        | 63.0          | 58.0     | 67.7      | 76.0          | 93.0      | +51.3 |

Table 1: Verifier PASS rate (%) on three verification tracks under two agent configurations. **Bold** marks the best score per row; underline marks the second-best. The ∆ column reports the absolute improvement of VeriSkill over the *No Skill* baseline.

projection to match the input after erasing annotations, comments, and whitespace. For C-to-Dafny, the check compares aligned callables, control flow, state updates, returns, and assertions across the source and generated artifacts. For every evaluation setting, we run each method three times and report the average as the final result.

# **6 Experimental Results**

To provide a comprehensive evaluation, we conduct extensive experiments covering baseline comparisons, ablation studies, and cross-model transferability. Because each experiment requires repeated LLM-agent execution and formal verification over multiple evolution iterations, the complete evaluation incurred approximately US\$15K in API costs.

### **6.1 Main Results**

To evaluate whether VeriSkill produces a stronger skill than other baselines, we evaluate all methods on three verification tracks under two agent/backbone configurations and report the three-trial mean PASS rate in Table 1.

VeriSkill achieves the best score in all six verifier–agent configurations. Against *No Skill*, it improves PASS by **+43.3**, **+17.6**, and **+46.0** pp on Dafny, Frama-C, and VeriFast with Claude Code/Opus 4.8, and by **+49.0**, **+25.5**, and **+51.3** pp with Codex/GPT 5.6 Sol. Compared with the strongest competing baseline in each row, VeriSkill still adds **+15.0**, **+9.1**, and **+5.7** pp under Claude, and **+3.3**, **+16.3**, and **+17.0** pp under GPT. Thus, the gains exceed prompt strength alone and remain above the strongest baseline SkillOpt-Lite.

Overall, evolved skills are clearly stronger than nonevolved skills: one-pass LLM Skill and Human Skill are inconsistent, sometimes falling below No Skill, whereas methods of skill self-evolution usually provide larger gains. However, these generic methods of skill self-evolution still lag behind VeriSkill, suggesting that program verification benefits from a customized evolution loop built around responsibility attribution, lesson abstraction, and executable validation.

# **6.2 Ablation Study**

To explore which parts of VeriSkill are responsible for the outstanding performance, we isolate the three core mecha-

| Setting                        | PASS<br>(%) | ∆ vs. Full |
|--------------------------------|-------------|------------|
| Full<br>VeriSkill              | 57.3        | —          |
| w/o Responsibility Attribution | 44.3        | −13.0      |
| w/o Lesson Abstraction         | 49.0        | −8.3       |
| w/o Executable Validation      | 36.0        | −21.3      |

Table 2: Component ablation on the Dafny track (Opus 4.8). Each row removes one stage of VeriSkill while leaving the rest of the pipeline unchanged. ∆ **vs. Full**reports the absolute drop from full VeriSkill.

nisms by removing one stage at a time on the Dafny track with Claude Code/Opus 4.8, while keeping the remaining pipeline and evaluation setting unchanged:

- **w/o Responsibility Attribution**: every verification failure is treated as a reusable skill deficiency, regardless of alternative failure sources.
- **w/o Lesson Abstraction**: candidate guidance is derived from direct generated–reference differences rather than their proof functions.
- **w/o Executable Validation**: candidate skills skip the revise–test loop on attribution and transfer cases, proceeding directly to validation.

Table 2 shows that all three mechanisms are necessary, with executable validation contributing the largest margin. Removing the revise–test loop over attribution and transfer cases lowers PASS from 57.3 to 36.0, a **21.3** pp drop. The loop uses cases from the same failure pattern to iteratively improve lesson accuracy before validation. Bypassing this process leaves lesson errors unresolved, limiting samepattern generalization and propagating faulty guidance to later tasks.

Responsibility attribution is the second most important component, with a **13.0** pp drop when removed. This indicates that treating every verifier failure as a skill defect injects noisy supervision into evolution, because some failures are caused by task unsatisfiability or prover limitations rather than missing reusable guidance. Removing lesson abstraction causes a smaller but still substantial **8.3** pp drop, show-

|              | EvoSkill                        | VeriSkill                                                   |  |  |  |
|--------------|---------------------------------|-------------------------------------------------------------|--|--|--|
| Source code  | Null-pointer Judgement:         | if (ptr == NULL) { abort(); }                               |  |  |  |
| Skill update | Preserve failure-guard branches | Do not fabricate branches for untranslatable failure guards |  |  |  |
| Evaluation   | Dafny PASS: 32.3%               | Dafny PASS: 57.3%                                           |  |  |  |

Table 3: A Dafny case study on branch-count deficits.

![](_page_6_Figure_2.jpeg)

Figure 2: Cross-model transferability under the Terminus agent framework.

ing that abstract lessons act as reasoning guidance toward the correct revision direction rather than letting examplespecific details dominate the update. Together, the ablations support the design of VeriSkill: attribution controls which failures become learning signals, abstraction derives reusable lessons, and executable validation iteratively improves lesson accuracy on same-pattern cases before global validation.

### **6.3 Cross-Model Transferability**

We evaluate whether an evolved skill has cross-model transferability as reusable knowledge rather than remaining a model-specific prompt artifact. A skill is meant to externalize and stabilize procedural knowledge, so once useful verification guidance is extracted and written into the skill, it should transfer to other capable LLMs instead of remaining tied to the model used during evolution. To test this, we take the final skill evolved with Codex, deploy it unchanged in the Terminus agent framework, and compare each Terminusbacked LLM against its No Skill setting on the same Dafny benchmark.

The results in Figure 2 support this view. The Codexevolved skill improves every Terminus-backed LLM, with gains ranging from +15.3 to +43.7 pp, even though no modelspecific evolution is performed. This transferability indicates that VeriSkill does not merely tune agent- or LLM-specific behavior. It extracts verification procedures that can be reused as external knowledge by different models. Transferability is strongest for models that already have moderate no-skill performance, where the skill can redirect existing reasoning ability toward Dafny program construction. For weaker backends, the skill still helps, but the lower final PASS shows that reusable knowledge does not replace the model's ability to execute the verification strategy faithfully.

# **7 Case Study**

We conduct a case study to explain why VeriSkill outperforms generic baselines of skill self-evolution. We compare with EvoSkill because it is conceptually closest to VeriSkill: both methods iteratively update skills from failures, but EvoSkill uses a generic failure-driven evolution loop rather than a program-verification-specific one.

Table 3 illustrates why VeriSkill improves over generic baselines of skill self-evolution. The same C fragment can lead to opposite skill updates: EvoSkill interpretation preserves the null-check branch to match source control flow, whereas VeriSkill recognizes that the branch is a host-level executability guard and should not be fabricated in Dafny when it carries no verified data-state behavior. This case explains why VeriSkill stands out: it does not merely react to failure signals, but interprets them through programverification-specific attribution and lesson abstraction before updating the skill.

# **8 Conclusion**

This paper presents VeriSkill, a self-evolution framework tailored to program verification that turns verification failures into targeted and trustworthy skill improvements. First, it performs responsibility attribution to retain only skillresponsible failures as evolution signals. Second, it clusters these failures by diagnostic signatures and abstracts reusable lessons that capture missing procedural guidance while removing instance-specific details. Finally, it iteratively refines candidate skills through executable validation and admits only revisions that improve verification performance while preserving program semantics. Evolution outcomes are stored in memory to guide subsequent revisions.

The experiments show that this program-verificationspecific evolution framework VeriSkill consistently outperforms other methods across Dafny, Frama-C, and VeriFast. The ablation study confirms that responsibility attribution, lesson abstraction, and executable-validation checks each contribute to the final skill quality. The cross-model transferability experiment further shows that evolved skills can benefit other LLMs, supporting the view that VeriSkill extracts reusable verification knowledge rather than a model-specific prompt artifact. Finally, the case study explains this advantage concretely: VeriSkill does not merely react to failure signals, but interprets them through program-verificationspecific attribution and lesson abstraction before updating the skill.

### References

- Alzubi, S.; Provenzano, N.; Bingham, J.; Chen, W.; and Vu, T. 2026. Evoskill: Automated skill discovery for multi-agent systems. *arXiv preprint arXiv*:2603.02766.
- Anthropic. 2026a. Agent Skills. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Accessed: 2026-07-22.
- Anthropic. 2026b. Claude Code Documentation. https://code.claude.com/docs/en/overview.
- Blanchard, A. 2020. Allan Blanchard's WP Tutorial Repository. https://github.com/AllanBlanchard/tutoriel\_wp.
- Breen, B.; Letson, A.; Pozo, B. R.; and Sarra, L. 2026. AxDafny: Agentic Verified Code Generation in Dafny. *arXiv* preprint arXiv:2606.32007.
- Cao, J.; Lu, Y.; Li, M.; Ma, H.; Li, H.; He, M.; Wen, C.; Sun, L.; Zhang, H.; Qin, S.; et al. 2025. From informal to formal—incorporating and evaluating llms on natural language requirements to verifiable formal proofs. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 26984–27003.
- Chen, K.; Zhong, Q.; Liu, J.; and Du, B. 2026. Skillcat: Contrastive assessment and topology-aware skill self-evolution for llm agents. *arXiv preprint arXiv:2606.13317*.
- Frama-C. 2026a. Frama-C Open-Source Case Studies Repository. https://github.com/Frama-C/open-source-case-studies.
- Frama-C. 2026b. Frama-C Snapshot Repository. https://github.com/Frama-C/Frama-C-snapshot.
- Fraunhofer FOKUS. 2026. ACSL by Example Repository. https://github.com/fraunhoferfokus/acsl-by-example.
- Hoare, C. A. R. 1969. An axiomatic basis for computer programming. *Communications of the ACM*, 12(10): 576–580.
- Jacobs, B. 2026. VeriFast Examples Index. https://people.cs.kuleuven.be/~bart.jacobs/verifast/examples/.
- Kamath, A.; Senthilnathan, A.; Chakraborty, S.; Deligiannis, P.; Lahiri, S. K.; Lal, A.; Rastogi, A.; Roy, S.; and Sharma, R. 2023. Finding inductive loop invariants using large language models. *arXiv preprint arXiv:2311.07948*.
- Le, X.-B. D.; Thung, F.; Lo, D.; and Le Goues, C. 2018. Overfitting in Semantics-Based Automated Program Repair. *Empirical Software Engineering*, 23(5): 3007–3033.
- Li, X.; Liu, Y.; Chen, W.; You, B.; Di, Z.; He, Y.; Zheng, S.; Choe, K. W.; Sun, J.; Wang, S.; et al. 2026. SkillsBench: Benchmarking how well agent skills work across diverse tasks. *arXiv preprint arXiv:2602.12670*.
- Loughridge, C.; Sun, Q.; Ahrenbach, S.; Cassano, F.; Sun, C.; Sheng, Y.; Mudide, A.; Misu, M. R. H.; Amin, N.; and Tegmark, M. 2024. Dafnybench: A benchmark for formal software verification. *arXiv preprint arXiv:2406.08467*.
- Ma, L.; Liu, S.; Li, Y.; Xie, X.; and Bu, L. 2024. Specgen: Automated generation of formal program specifications via large language models. *arXiv preprint arXiv:2401.08807*.

- Mugnier, E.; Gonzalez, E. A.; Polikarpova, N.; Jhala, R.; and Yuanyuan, Z. 2025. Laurel: Unblocking automated verification with large language models. *Proceedings of the ACM on Programming Languages*, 9(OOPSLA1): 1519–1545.
- Ni, J.; Liu, Y.; Liu, X.; Sun, Y.; Zhou, M.; Cheng, P.; Wang, D.; Zhao, E.; Jiang, X.; and Jiang, G. 2026. Trace2skill: Distill trajectory-local lessons into transferable agent skills. *arXiv preprint arXiv:2603.25158*.
- OpenAI. 2026. Get Started with Codex. https://openai.com/codex/get-started/.
- Patnaik, M. 2020. A Repository Dedicated for Problems Related to Verification of Programs Using the Tool Frama-C. https://github.com/manavpatnaik/frama-c-problems.
- Rozière, B.; Lachaux, M.-A.; Chanussot, L.; and Lample, G. 2020. Unsupervised Translation of Programming Languages. In *Advances in Neural Information Processing Systems*, volume 33, 20601–20611.
- Shen, Y.; Li, B.; and Zhang, X. 2026. SkillOpt-Lite: Better and Faster Agent Self-evolution via One Line of Vibe. *arXiv* preprint arXiv:2607.03451.
- Terminal-Bench. 2026. Terminus. https://www.tbench.ai/news/terminus.
- VeriFast. 2026. VeriFast Repository. https://github.com/verifast/verifast.
- Wang, Z.; Lin, T.; Chen, M.; Li, H.; Yang, M.; Yi, X.; Qin, S.; Luo, Y.; Li, X.; Gu, B.; et al. 2026. A tale of 1001 loc: Potential runtime error-guided specification synthesis for verifying large-scale programs. *Proceedings of the ACM on Programming Languages*, 10(OOPSLA1): 1874–1902.
- Wen, C.; Cao, J.; Su, J.; Xu, Z.; Qin, S.; He, M.; Li, H.; Cheung, S.-C.; and Tian, C. 2024. Enchanting program specification synthesis by large language models using static analysis and program verification. In *International Conference on Computer Aided Verification*, 302–328. Springer.
- Wu, G.; Cao, W.; Yao, Y.; Wei, H.; Chen, T.; and Ma, X. 2024. Llm meets bounded model checking: Neuro-symbolic loop invariant inference. In *Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering*, 406–417.
- Wu, H.; Barrett, C.; and Narodytska, N. 2024. Lemur: Integrating large language models in automated program verification. In *International Conference on Learning Representations*, volume 2024, 2968–2978.
- Yan, Z.; Song, D.; Zhang, H.; Liang, W.; Zhang, Y.; Dai, Y.; He, L.; Yu, P. S.; Xu, R.; Li, X.; and Sun, L. 2026. OpenSkill: Open-World Self-Evolution for LLM Agents. *arXiv preprint arXiv:2606.06741*.
- Yang, C.; Li, X.; Misu, M. R. H.; Yao, J.; Cui, W.; Gong, Y.; Hawblitzel, C.; Lahiri, S.; Lorch, J. R.; Lu, S.; et al. 2025. Autoverus: Automated proof generation for rust code. *Proceedings of the ACM on Programming Languages*, 9(OOP-SLA2): 3454–3482.
- Yang, Y.; Gong, Z.; Huang, W.; Yang, Q.; Zhou, Z.; Huang, Z.; Li, Y.; Gao, X.; Dai, Q.; Liu, B.; et al. 2026a. Skillopt: Executive strategy for self-evolving agent skills. *arXiv preprint arXiv*:2605.23904.

- Yang, Y.; Li, J.; Pan, Q.; Zhan, B.; Cai, Y.; Du, L.; Zhou, J.; Chen, K.; Chen, Q.; Li, X.; Zhang, B.; and He, L. 2026b. AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution. *arXiv preprint arXiv:2603.01145*.
- Ye, H.; Martinez, M.; and Monperrus, M. 2021. Automated Patch Assessment for Program Repair at Scale. *Empirical Software Engineering*, 26(2): 20.
- Zhang, H.; Fan, S.; Zou, H. P.; Chen, Y.; Wang, Z.; Zhou, J.; Li, C.; Huang, W.-C.; Yao, Y.; Zheng, K.; et al. 2026. Co-EvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification. *arXiv preprint arXiv:2604.01687*.
- Zhou, Y.; Zhang, Z.; Cheng, Z.; Zhang, S.; Lan, Q.; Chen, Z.; Yang, Z.; Chen, R.; Wang, H.; Hu, S.; et al. 2026. Skillgenbench: Benchmarking skill generation pipelines for llm agents. *arXiv preprint arXiv:2605.18693*.