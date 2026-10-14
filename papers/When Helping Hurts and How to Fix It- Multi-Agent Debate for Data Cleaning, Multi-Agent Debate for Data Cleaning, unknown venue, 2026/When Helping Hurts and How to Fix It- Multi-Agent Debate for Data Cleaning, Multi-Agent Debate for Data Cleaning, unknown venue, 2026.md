                                            When Helping Hurts and How to Fix It:
                                            Multi-Agent Debate for Data Cleaning
                                            Chirag Parmar1,∗ , Akshat Mehta1 , Henglin Wu1 , Jagadish Ramamurthy1 , Shweta Medhekar1
                                            1
                                                Meta Platforms, Inc.
                                            ∗
                                                Corresponding author

                                            When does multi-agent debate help data cleaning, and when does it hurt? Across three benchmarks,
                                            four model families, and over 6,000 task-condition pairs, we find debate’s effect reverses sign: it
                                            degrades generation across all four models (−1.6 to −15.5pp) through critique-induced confusion
                                            (CIC), hallucinated Critic feedback that the Generator accepts uncritically, yet improves error detection
                                            (+27.4pp F1, d=1.0). We derive a debate benefit condition: debate helps when the probability of
arXiv:2606.02866v1 [cs.AI] 1 Jun 2026




                                            rescuing a wrong output (Critic verification odds weighted by fixability) exceeds the probability
                                            of destroying a correct one. A factorial experiment proves adversarial separation is essential: self-
                                            verification with identical tools fails, while a separate Critic with code-execution grounding and
                                            evidence-gated generation produces the first debate configuration to significantly exceed single-agent
                                            on a generative task (+5.3pp, p<0.05). The condition correctly predicts all nine task types and
                                            generalizes with zero false positives across 19 published comparisons in seven domains.

                                            Date: June 2026
                                            Correspondence: Chirag Parmar at chiragparmar@meta.com




                                        1       Introduction
                                        Data cleaning has historically consumed an estimated 60–80% of a data engineer’s time (Dasu and Johnson,
                                        2003; Ilyas and Chu, 2019; Whang et al., 2023), and LLMs are now routinely deployed to automate this
                                        burden (Narayan et al., 2022). Recent work demonstrates that LLMs can generate data cleaning workflows (Li
                                        et al., 2024a), detect anomalies in tabular data (Li et al., 2024b; Zhang et al., 2024a), and orchestrate
                                        multi-step pipelines (Qi and Wang, 2024). However, LLM hallucination remains a critical obstacle: when
                                        an LLM proposes cleaning a non-existent column or removing records that are in fact distinct, the pipeline
                                        silently corrupts data.
                                        Multi-agent debate, where an adversarial Critic challenges a Generator’s proposals before deployment, offers
                                        one mitigation (Du et al., 2024; Liang et al., 2024; Irving et al., 2018; Leike et al., 2018; Bowman et al.,
                                        2022). Architectural refinements such as response anonymization (Sharma et al., 2024; Wei et al., 2024; Choi
                                        et al., 2025) and task isolation aim to reduce sycophancy and enable independent verification. Yet existing
                                        evaluations focus on constrained reasoning tasks (arithmetic, factual QA, commonsense inference (Chan et al.,
                                        2024; Khan et al., 2024; Chen et al., 2024; Wang et al., 2024a)) where answer spaces are small and verification
                                        is straightforward. Data cleaning is fundamentally different: it requires grounding in specific table schemas
                                        and producing executable operations, not closed-form answers. Meanwhile, prior data cleaning systems rely on
                                        probabilistic inference or statistical models (Rekatsinas et al., 2017; Mahdavi et al., 2019; Heidari et al., 2019),
                                        and the emerging LLM-based approaches (Li et al., 2024a; Qi and Wang, 2024) use exclusively single-agent
                                        architectures. No prior study has evaluated whether debate helps or harms across the full spectrum of data
                                        cleaning subtasks.
                                        Prior debate work shows improvements on constrained reasoning but harm when agents are persuasive yet
                                        incorrect (Khan et al., 2024). Concurrent work by Zhang et al. (2025) demonstrates this at scale across
                                        nine reasoning benchmarks; we complement their finding with the mechanism (why debate fails), the formal
                                        condition (when it helps), and the fix (how to recover). Our Generator-Critic topology follows the Du et al.
                                        (2024) formulation (two LLM agents, no human judge), architecturally distinct from the debate-as-alignment
                                        proposal of Irving et al. (2018). The data management literature has long distinguished error detection from


                                                                                                 1
error repair (Wang and Strong, 1996; Fan and Geerts, 2012); our debate benefit condition connects this
classical distinction to multi-agent systems.
The question “when does debate help?” has practical urgency. Multi-agent architectures are increasingly
deployed in production data pipelines, but without a principled framework for predicting their effect, practi-
tioners face expensive trial-and-error. Deploying debate on a generative task where it causes CIC wastes 4–7×
the compute budget while degrading output quality. Conversely, not deploying debate on a detection task
where it could improve F1 by 27pp leaves substantial quality gains on the table. Our debate benefit condition
provides a deployable decision rule: three estimable quantities determine whether to invest in debate or stay
with single-agent. Full related work appears in Section 2.
A controlled experiment answers this question directly. Our contributions:
    1. A debate benefit condition predicting when debate helps. We derive a formal condition: debate
       improves output quality when the Critic’s verification odds, weighted by fixability, exceed the Generator’s
       baseline accuracy odds. The condition correctly predicts all nine task types in our study and generalizes
       with zero false positives across 19 published comparisons in seven domains.
    2. Critique-induced confusion is structural, not prompt-dependent. A sweep of 6 Critic × 3 Generator
       variants confirms that CIC persists across all prompt configurations and is not a sampling artifact (self-
       consistency majority vote performs worse than single-agent). A factorial experiment proves adversarial
       separation is essential: self-verification with identical tools fails, while a separate adversarial Critic
       succeeds. Section 7 shows CIC is addressable via grounded verification.
    3. Code-execution grounding with evidence-gated generation exceeds single-agent. Grounding the Critic
       in a code-execution sandbox eliminates CIC. Adding evidence-gated generation, where the Generator
       only acts on feedback citing specific data evidence, yields the first debate configuration to significantly
       exceed single-agent on workflow generation (+5.3pp, p<0.05).


2      Related Work
LLMs for Data Cleaning. AutoDCWorkflow (Li et al., 2024a) introduced an LLM-orchestrated pipeline that
generates data cleaning workflows from natural language descriptions of cleaning purposes. CleanAgent (Qi
and Wang, 2024) extended this with a code-generation agent that iteratively refines cleaning scripts. Fang
et al. (2024) surveyed LLM applications for data cleaning, finding that while LLMs show promise for
anomaly detection and standardization, hallucination-induced errors remain the primary barrier to production
deployment. Li et al. (2024b) demonstrated that LLMs struggle with tabular data understanding when column
semantics are ambiguous. Prior data cleaning systems use probabilistic inference over integrity constraints
(HoloClean (Rekatsinas et al., 2017)), ensemble error detection strategies (Raha (Mahdavi et al., 2019)),
few-shot learning (HoloDetect (Heidari et al., 2019)), or declarative rules (Dallachiesa et al., 2013; Chu et al.,
2015; Krishnan et al., 2016); LLM-based approaches promise greater flexibility but introduce new failure
modes. For entity matching specifically, deep learning approaches (Mudgal et al., 2018; Li et al., 2020; Peeters
and Bizer, 2024) and schema matching systems (Do and Rahm, 2002; Koutras et al., 2021) provide strong
baselines that LLM debate must improve upon.

Multi-Agent Debate. Du et al. (2024) proposed multi-agent debate where LLM agents iteratively refine
answers through structured argumentation, showing improvements on arithmetic and factual reasoning. Liang
et al. (2024) introduced the “thinker-judge” topology and demonstrated that divergent thinking improves
creative and analytical tasks. Chan et al. (2024) applied multi-agent evaluation to open-ended text generation.
Khan et al. (2024) found that debate can be harmful when agents are persuasive but incorrect, foreshadowing
our results. Chen et al. (2024) showed round-table discussions improve reasoning via consensus, while Wang
et al. (2024a) examined when multi-agent discussions outperform single-agent reasoning. Zhang et al. (2024b)
explored collaboration mechanisms through a social psychology lens. Recent work has investigated multi-
agent frameworks for complex task solving (Wu et al., 2024; Hong et al., 2024; Li et al., 2023; Wang et al.,
2024b). Talebirad and Nadiri (2023) provided a taxonomy of multi-agent collaboration patterns. Parrish et al.
(2022) found that single-turn debate does not help humans answer hard reading comprehension questions, a


                                                        2
negative result on debate that parallels our findings on generative tasks. Huang et al. (2024) showed LLMs
cannot self-correct reasoning without external feedback, providing a complementary perspective on the CIC
mechanism. Concurrent work by Zhang et al. (2025) argues that task structure, not model capability or
prompt design, determines debate effectiveness, corroborating our prompt sensitivity findings.

LLM Sycophancy and Anonymization. Sharma et al. (2024) documented sycophantic behavior across multiple
LLM families, where models defer to stated user preferences even when incorrect, a tendency amplified by
RLHF training (Ouyang et al., 2022; Bai et al., 2022). In multi-agent systems, sycophancy manifests as one
agent deferring to another’s authority. Wei et al. (2024) showed synthetic data can reduce sycophancy, while
Choi et al. (2025) demonstrated that anonymization specifically mitigates identity-based bias in multi-agent
debate.

Scalable Oversight and Debate Theory. Irving et al. (2018) proposed debate as a mechanism for scalable
AI alignment, leveraging the theoretical result that interactive proofs with polynomial-time verifiers can
verify claims from exponentially powerful provers. Leike et al. (2018) extended this to recursive reward
modeling, where human oversight is applied at the finest-grained level feasible and then composed. Bowman
et al. (Bowman et al., 2022) operationalized debate for scalable oversight by measuring whether debate helps
non-expert humans answer expert-level questions. Our work provides an empirical bridge: the debate benefit
condition identifies exactly when the “verifier efficiency” assumption holds (high pc ) and when it breaks down
(low pc ), connecting the theoretical framework to practical deployment decisions.


3     Experimental Setup
Problem Setting. Given a dirty table Tdirty with n rows and m columns (of mixed types: strings, numerics,
dates) and a cleaning purpose p, generate a workflow W = [w1 , . . . , wk ]. We evaluate both structural halluci-
nation (factual consistency, FC) and semantic correctness (cell-level accuracy via deterministic execution).

Benchmarks.    We use three benchmarks spanning complementary evaluation paradigms:
AutoDCWorkflow (Li et al., 2024a) provides 142 data cleaning tasks across 6 domains (food inspections,
restaurant menus, hospital records, university data, housing data, and employee records); each task includes a
dirty table, ground-truth clean table, and cleaning purpose, and the model must generate a multi-step cleaning
workflow (evaluated via FC and cell-level accuracy). Tasks range from simple standardization (“normalize
phone numbers”) to complex multi-step transformations (“split combined name fields, deduplicate records,
and standardize date formats”). Median table size is 15 rows with 8 columns.
MMTU (Xing et al., 2025) contains 28,136 table understanding questions spanning 16 task types. We
randomly sample 200 questions (50 per type, stratified by dataset, seed=42) from four cleaning-relevant types:
Error Detection (identify cells with data quality issues), Data Imputation (predict missing values), Entity
Matching (determine whether two records refer to the same entity), and Schema Matching (align columns
across different table schemas). MMTU evaluates comprehension, whether the model can reason about table
structure and content, complementing AutoDCWorkflow’s evaluation of generation and MaTElDa’s evaluation
of detection.
MaTElDa (Ahmadi et al., 2025) provides 1,173 real-world tables from Data.gov with systematically injected
errors (typos, formatting inconsistencies, missing values, semantic violations); we evaluate 100 tables for
cell-level precision, recall, and F1. Each table contains a known set of error cells, enabling exact evaluation
without subjective judgment. Tables are capped at 100 rows for main experiments; 15 tables with ≥10K
original rows are used for scale validation (Section 8.3). These three paradigms (generation, comprehension,
and classification) span the full spectrum of data cleaning subtasks.

Models. We evaluate four model families: Claude 4 Sonnet (Anthropic), Gemini 3.1 Pro (Google), Qwen3
235B (A22B, Alibaba’s MoE model), and DeepSeek R1 (reasoning-specialized with extended chain-of-thought).
All experiments use temperature 0 and maximum 8,192 output tokens.



                                                       3
                                Anonymization: role labels → Agent A / Agent B




                              Generator           JSON workflow               Critic
                              (Agent A)                                     (Agent B) up to 3 rounds
                                             accept / revise

                             input                                                if hallucinated
                                           Generator complies verify against

                                                                            CIC Risk
                             Dirty Table
                                                                       Hallucinated feedback
                                Tdirty
                                                                        → retract valid ops


Figure 1 Generator-Critic debate architecture. The Generator proposes structured JSON outputs; the Critic challenges
each against the source table and returns accept/revise with evidence. Anonymization (dotted line) replaces role labels
with neutral identifiers. When the Critic’s feedback is itself hallucinated, the Generator retracts correct operations,
the CIC failure mode (orange path).


Architecture. Our debate topology consists of two agents: a Generator that proposes structured JSON
outputs and an adversarial Critic that challenges them (Figure 1). The Critic checks each operation for
hallucination, verifies against the source data, and returns accept/reject/revise with evidence. Tables are
serialized as JSON arrays (no truncation; median 15 rows).

Evaluation Metrics. Factual Consistency (FC): fraction of operations targeting existing columns. Cell
Accuracy: fraction of cells matching ground truth after deterministic execution (∼20 operation handlers, fuzzy
matching, skip-and-continue). Execution Success Rate: fraction of operations that execute without error. For
MaTElDa: precision, recall, and F1 at the cell level.

Experimental Conditions. We test six treatment conditions in a within-subjects paired design. Adversarial
debate: Single Agent vs. Adversarial Debate (Generator-Critic, up to 3 rounds). Anonymization and isolation:
debate with vs. without response anonymization and task isolation (Appendices B–C); anonymization is used
in all subsequent conditions. Cardinality ablation: output cardinality ablation with four controlled experiments
varying multi-output and verifiability dimensions on MaTElDa tables. Prompt sensitivity: prompt sensitivity
sweep across 6 Critic × 3 Generator variants (4,350 task-condition pairs). Code-execution: code-execution
Critics with evidence-gated generation. Self-verification: single agent with the same code-execution sandbox
but no separate Critic (SA+Code). Self-consistency: self-consistency control (k=5 majority vote).

Scale. For the debate, anonymization, and isolation experiments on AutoDCWorkflow, we evaluate Claude,
Qwen3, and DeepSeek on 50 tasks each, and Gemini on 20 tasks (exploratory). On MMTU, we evaluate
200 questions for Claude, Qwen3, and DeepSeek. On MaTElDa, we evaluate 100 tables for all four models.
The prompt sensitivity analysis adds 4,350 task-condition pairs across expanded sample sizes (n=100–200),
bringing the grand total to over 6,000 task-condition pairs.1

Statistical Methods. All pairwise comparisons use paired bootstrap confidence intervals (10,000 BCa resamples,
95% CI) with Holm-Bonferroni correction (Efron and Tibshirani, 1993; Holm, 1979). Treatment effect sizes
are reported as Cohen’s d using pooled standard deviations.2 We assess bimodality using Hartigan’s dip test
   1 The prompt sensitivity sweep uses different task subsets (larger n) than the main experiments, so SA baselines differ slightly

between tables; e.g., AutoDCWorkflow SA FC=0.871 at n=50 (Table 1) vs. 0.799 at n=100 (Table 18); MaTElDa SA F1=0.191
(Table 2) vs. 0.301 (Table 18); MMTU-ED SA=0.820 (n=200) vs. 0.760 (n=100). All comparisons within each table use the
same paired task set.
   2 For paired designs, d (mean of paired differences / SD of differences) is the standard measure. We report d
                          z                                                                                       pooled for
comparability with between-subjects studies. In our data, dpooled and dz diverge by <0.12 across all comparisons: MaTElDa
Claude dpooled =1.00, dz =0.94; Gemini dpooled =0.95, dz =0.88. No qualitative interpretation changes.


                                                                4
Table 1 Adversarial debate results: Single Agent vs. Adversarial Debate on AutoDCWorkflow. Cell Acc measures
semantic correctness via deterministic execution. Debate is neutral to harmful for workflow generation; no comparison
reaches significance after Holm-Bonferroni correction (n=50). Cell Acc and Exec Rate are reported only for Claude,
where the deterministic executor was fully validated; missing values indicate metrics not computed.

 Model                Condition               FC ↑    Cell Acc ↑    Exec Rate ↑      Perfect     Zero    Tok/task
                      Single Agent            0.871      0.894          0.716         22/50      0/50       3,281
 Claude 4 Sonnet
                      Adversarial Debate      0.855      0.899          0.628         28/50      2/50      14,056
                      Single Agent            0.796          —            —           13/20      3/20       4,043
 Gemini 3.1 Pro
                      Adversarial Debate      0.667          —            —           11/20      6/20      18,139
                      Single Agent            0.912          —            —           44/50      4/50       5,137
 Qwen3 235B
                      Adversarial Debate      0.785          —            —           34/50      9/50      26,245
                      Single Agent            0.800          —            —           30/50     7/50        7,997
 DeepSeek R1
                      Adversarial Debate      0.645          —            —           21/50     10/50      58,637


and BIC comparison between 1- and 2-component Gaussian mixture models. Post-hoc power at α=0.05: 80%
power to detect d≥0.40 at n=50 (AutoDCWorkflow), d≥0.28 at n=100 (MaTElDa), and d≥0.20 at n=200
(MMTU). Full BCa details appear in Appendix D.


4     Results: Debate Helps Detection, Hurts Generation
4.1    Debate Reverses Sign
If debate’s adversarial pressure introduces more noise than signal on open-ended tasks, we should observe
degradation on workflow generation across multiple model families. Table 1 confirms this: debate is neutral
to harmful for all four models. Claude shows no significant change (∆= − 0.016 FC, p=0.70); cell accuracy is
nearly identical (0.894 vs. 0.899, p=0.83). However, debate simultaneously increases perfect-score outputs
(22→28) and introduces 2 complete failures, making it a variance amplifier. Gemini drops from 0.796 to
0.667 FC; Qwen3 drops from 0.912 to 0.785 (∆= − 12.7 pp, d= − 0.38); DeepSeek drops from 0.800 to 0.645
(∆= − 15.5 pp, d= − 0.42) with 7.3× token overhead. We term this failure mode critique-induced confusion
(CIC): the Critic, designed to improve quality, functions as a verification catalyst on tasks where it can ground
objections in evidence, but undergoes poisoning on generation tasks, where adversarial pressure produces
hallucinated feedback that the compliant Generator accepts uncritically (Khan et al., 2024; Huang et al.,
2024). FC distributions are bimodal across all conditions (Hartigan’s dip test p<0.002; details in Appendix H).
Debate improves FC on structured data (Chicago Food Inspections: +4.1pp) but reduces it on semi-structured
data (menus: −5.3pp). Anonymization (+2.2 pp FC, p=0.39) is a zero-cost improvement; task isolation
(−6.0pp FC, p=0.084) harms through information asymmetry. Full anonymization and isolation results appear
in Appendices B and C.
A distributional analysis reveals that FC scores are not normally distributed but bimodal across all conditions
(Hartigan’s dip test p<0.002; BIC favors a two-component Gaussian mixture over a single Gaussian). Debate
does not shift the distribution uniformly; instead, it reshapes the mixture weights. For Claude, the upper mode
(FC≈1.0) absorbs more mass under debate (56% vs. 44%), while the lower mode both shifts downward and
widens (µ: 0.77 → 0.67; σ: 0.10 → 0.24). Debate is thus a variance amplifier: it improves the best outcomes
while making the worst outcomes more severe. Figure 2 shows the distributions.

4.2    Cross-Benchmark Validation
If CIC arises because the Critic cannot verify its objections on generation tasks, then on detection tasks, where
each output is independently checkable against the source table, debate should help. Table 2 confirms this
prediction: on MaTElDa, debate substantially improves F1 from 0.191 to 0.465 (+27.4pp, p<0.001, d=1.00),
winning 80 of 100 tables. The precision improvement (0.279 → 0.685) shows the Critic effectively prunes false
positives. The same precision-filtering mechanism that, on generative tasks, prunes valid operations.


                                                         5
     Count       Claude 4 Sonnet (n=50)

      30     Single Agent

             Debate
                                                                       Count        Gemini 3.1 Pro (n=20)
      20
                                                                                Single Agent
                                                                                Debate
                                                                       15

      10                                                               10

                                                                        5

       0                                             FC                 0                                              FC
           0.1      0.3     0.5   0.7    0.9   1.0                            0.1     0.3      0.5   0.7   0.9   1.0

     (a) Claude: debate shifts mass to extremes.                            (b) Gemini: debate increases failures.

Figure 2 FC distributions for the adversarial debate experiment. Both conditions are bimodal (dip test p<0.002).
For Claude, debate increases the upper mode weight (56% vs. 44%) but widens the lower mode (µ=0.67, σ=0.24 vs.
µ=0.77, σ=0.10). For Gemini, debate shifts mass away from FC≈1.0. This variance-amplification pattern is consistent
across all four models (Appendix H). Note: y-axes differ between subplots (n=50 vs. n=20) to maximize readability
within each panel; compare distributions within panels, not across.

Table 2 MaTElDa results: single-agent vs. debate on cell-level error detection (Claude 4 Sonnet, n=100). Bootstrap
95% CIs over 10,000 resamples.

                          Condition      F1 ↑        Precision ↑   Recall ↑         Wins        Avg Tok
                          Single Agent   0.191         0.279        0.172            11           4,539
                          Debate         0.465         0.685        0.441            80          28,558
                          F1: ∆= + 0.273, 95% CI [0.217, 0.331], p<0.001, d=1.00
                          Precision: ∆= + 0.405, 95% CI [0.333, 0.477], p<0.001
                          Recall: ∆= + 0.269, 95% CI [0.211, 0.329], p<0.001


Debate benefit correlates with single-agent precision headroom (Table 3): Claude (d=1.00) shows the
strongest benefit; Qwen3 (d=0.32) and DeepSeek (d=0.30) show moderate effects. Gemini’s apparent high
benefit (d=0.95) largely reflects debate scaffolding structured output rather than detection improvement:
under the original SA prompt, 87 of 100 tables produce zero F1 due to unparseable JSON; with stricter format
instructions, SA F1 rises from 0.078 to 0.374, reducing the debate advantage to near zero (∆= + 0.014).
The pattern connects to the debate benefit condition through pg : Claude has low pg (high precision headroom),
so even imperfect Critic verification (pc ) produces a net positive rescue-damage balance. Qwen3 and DeepSeek
have moderate pg , narrowing the margin. The win-loss-tie distributions reinforce this: Claude debates win 80,
lose 11, tie 9; Qwen3 and DeepSeek show more balanced distributions (39/20/35 and 39/19/42 respectively),
consistent with marginal rescue-damage balance.
On MMTU (n=200, Claude), no individual task-type comparison reaches significance after correction; all CIs
include zero. We present these as directionally consistent supporting evidence, not standalone findings. Data
Imputation shows the largest directional degradation (−12.0pp, d= − 0.26), while Entity Matching reaches
ceiling (1.000 vs. 0.980). Cross-model MMTU results confirm debate helps error detection directionally:
Qwen3 ED improves from 0.520 to 0.640 (+12.0pp); DeepSeek ED from 0.600 to 0.640. Full MMTU tables
appear in Appendix E.
Table 5 reveals the central finding: task type is the critical moderating variable. Binary classification tasks
(error detection, entity matching) benefit from debate, because the Critic’s adversarial pressure prunes false
positives without generating incorrect alternatives. Generative tasks (imputation, workflow generation) are
harmed, because the Critic’s objections cause the Generator to retract correct operations and substitute
hallucinated alternatives, the CIC mechanism. The boundary lies at answer-space constraint: when the answer


                                                               6
Table 3 Cross-model MaTElDa (n=100 each). Debate benefit correlates with single-agent precision headroom.

        Model                SA F1       Debate F1         ∆ F1          95% CI            d       Wins (D/S/T)
        Claude 4 Sonnet      0.191          0.465         +0.273    [0.217, 0.331]*      1.00        80/11/9
        Gemini 3.1 Pro       0.078          0.388         +0.310    [0.241, 0.385]*      0.95         57/1/42
        Qwen3 235B           0.150          0.226         +0.076    [0.042, 0.125]*      0.32        39/20/35
        DeepSeek R1          0.145          0.219         +0.074    [0.038, 0.116]†      0.30        39/19/42
        *p<0.001. † p=0.037. Gemini SA: 87% zero-F1 (output failures).

Table 4 MMTU results: single-agent vs. debate across four table understanding tasks (Claude 4 Sonnet, n=200).
Score is task-specific: F1 for ED/SM, exact match for DI, accuracy for EM.

              Task Type              Single-Agent         Debate          ∆           95% CI           d
              Error-Detect                0.820            0.840        +0.020    [−0.12, +0.16]      +0.05
              Data-Imputation             0.760            0.640        −0.120    [−0.30, +0.06]      −0.26
              Entity-Matching             0.980            1.000        +0.020    [+0.00, +0.06]      +0.20
              Schema-Matching             0.968            0.957        −0.010    [−0.05, +0.02]      −0.11
              Overall                     0.882            0.859        −0.023    [−0.09, +0.04]      −0.07
              Total tokens                                376K vs. 1,381K              3.7× overhead


space is constrained (is this cell an error?), verification adds value; when it is open-ended (what value should
fill this cell?), critique introduces more noise than signal. This resolves the apparent contradiction with prior
work (Du et al., 2024): reasoning tasks have constrained answer spaces, just like error detection.

4.3    What Explains the Reversal?
The task-type framework from Section 4 draws a binary detection-vs.-generation boundary, but this conflates
answer-space constraint and output cardinality. To disentangle these factors, we design four controlled
ablation experiments on the same MaTElDa tables, varying output cardinality while holding task content
constant. Table 6 shows the key result: Rep (multi-output data repair, a generative task) shows a large debate
improvement (F1: 0.206 → 0.467, ∆=+0.261, d=0.93, 95% CI [0.197, 0.327], p<0.001), with debate winning 76
of 100 tables. This challenges the simple task-type framework: Rep is generative, yet debate helps because each
output is independently verifiable. The remaining results complete the 2×2: Loc (detection, single-output) is
neutral (d=0.00); Prof-S (generation, single-output) is harmed (d= − 0.42); Prof-M (generation, multi-output,
not verifiable) is neutral (d= − 0.07).
The simple detection-vs-generation binary is insufficient. Rep is generative, yet debate helps because each
output is independently verifiable against source data. The deeper moderator is the interplay of verification
accuracy, fixability, and baseline quality, which we formalize in Section 5.
The 2×2 pattern replicates across models: Qwen3 235B shows the identical qualitative pattern, that only
Rep benefits from debate (SA F1=0.136, Debate F1=0.238, ∆= + 0.102), while Loc is neutral (∆= − 0.018),
Prof-S is harmed (∆= − 0.070), and Prof-M is neutral (∆= − 0.008). The cross-model replication strengthens
the structural interpretation: per-item verifiability, not model-specific behavior, determines whether debate
helps generative tasks. Full cross-model cardinality results appear in Appendix M.


5     The Debate Benefit Condition
We derive a formal condition under which adversarial debate improves output quality. For each output item i,
debate helps when rescue exceeds damage:

                           (1 − pg ) ·      pc       ·    pr        >       pg · (1 − pc )                        (1)
                           | {z }          |{z}          |{z}              |{z}  | {z }
                          error exists Critic catches fix correct         was right Critic wrong


                                                             7
Table 5 Cross-benchmark synthesis: debate’s effect by task type (Claude 4 Sonnet). Tasks ordered from most
constrained to most open-ended.

         Benchmark        Task Type                 ∆              Sig?              Task Nature
         MaTElDa          Error Detection       +27.4pp F1    Yes (p<0.001)      Binary classification
         MMTU             Entity Matching        +2.0pp            n.s.          Binary classification
         MMTU             Error Detection        +2.0pp            n.s.           Binary detection
         AutoDCW          Structured (CFI)      +4.1pp FC          n.s.         Constrained generation
         MMTU             Schema Matching        −1.1pp            n.s.          Structured mapping
         AutoDCW          Overall               −1.6pp FC          n.s.          Workflow generation
         AutoDCW          Semi-structured       −5.3pp FC          n.s.         Open-ended generation
         MMTU             Data Imputation        −12.0pp           n.s.           Value generation

Table 6 Output cardinality ablation: Output cardinality experiments (Claude 4 Sonnet). Only Rep (multi-output
generation with per-item verifiability) shows a large debate benefit.

        Exp        Task                             SA        Debate        ∆         d      Cardinality
        Loc        Single-output localization     0.672 acc   0.674 acc   +0.002     0.00      Single
        Rep        Multi-output repair            0.206 F1    0.467 F1    +0.261     0.93      Multi
        Prof-S     Single-output profiling        0.920 acc   0.770 acc   −0.150    −0.42      Single
        Prof-M     Multi-output profiling         0.537 F1    0.519 F1    −0.018    −0.07      Multi


where pg is the Generator’s baseline accuracy (fraction of items already correct), pc is the Critic’s verification
accuracy (fraction of items correctly judged), and pr is the repair probability (given the Critic correctly
identifies an error, the probability the Generator produces a correct replacement). Equivalently, as an odds
                                           pg
ratio: debate helps when 1−p pc
                                c
                                  × pr > 1−p  g
                                                ; that is, the Critic’s verification odds, weighted by fixability,
exceed the Generator’s baseline accuracy odds.
What determines pc ? Two task properties: evidence groundability (can the Critic look up evidence in the
source data?) and verification determinism (given evidence, is correctness unambiguous?). What determines
pr ? The answer-space constraint: for detection tasks, pr ≈ 1.0 (removing a false positive is a binary flip); for
repair, pr ≈ 0.5 (usually one obvious correction); for open-ended generation, pr ≈ 0.2 (the Generator may
hallucinate again).
At the task level with k output items, compliance rate α, and inter-item dependence ρ:
                                           h                                i
                        ∆Perf(T ) ≈ k · α · (1−pg ) · pc · pr − pg · (1−pc ) · (1 − ρβ)                       (2)

where ρ measures output dependence (0 for independent cells, 1 for fully coupled operations) and β is cascade
severity, measuring how many downstream items one erroneous critique corrupts. For detection tasks, outputs
are typically independent (ρ ≈ 0) and the cascade term vanishes, so the per-item condition directly scales
to task-level performance. For workflow generation, operations form dependent chains (ρ > 0): a single
hallucinated critique can corrupt downstream operations through cascade amplification, explaining why CIC is
disproportionately harmful on generative tasks even when the per-item rescue-damage balance is only mildly
negative. Empirically, we observe β ≈ 1.3 for AutoDCWorkflow (one bad critique corrupts ∼1.3 operations on
average) and β ≈ 0 for MaTElDa (cell detections are independent). Full derivation and assumptions appear
in Appendix L.
Table 7 validates the debate benefit condition against observed treatment effects across all nine task types.
The condition correctly predicts the sign of debate’s effect in every case. Key patterns: (1) low pg + high pc
+ high pr produces large positive effects (MaTElDa: d=1.00, Rep: d=0.93); (2) high pg limits benefit even
with high pc (Entity Matching: pg =0.98, d=0.20); (3) low pc or low pr produces negative effects regardless of
pg . Cross-domain validation on 19 published comparisons across seven domains confirms zero false positives
(Section 8).


                                                         8
Table 7 Debate benefit condition validation across nine task types. pg : Generator accuracy; pc : Critic verification
(high = evidence-groundable, low = requires judgment); pr : repair probability. The condition correctly predicts the
sign of debate’s effect for all nine tasks.

                Task                           pg       pc         pr      Rescue > Damage?     Cohen’s d
                MaTElDa Detection             0.19     high       ≈1.0             Yes              +1.00
                MMTU Entity Matching          0.98     high       ≈1.0       Barely (pg high)       +0.20
                MMTU Error Detection          0.82     high       ≈1.0       Barely (pg high)       +0.05
                Rep (multi-output repair)     0.21     high       ≈0.5             Yes              +0.93
                Loc (single-output detect)    0.67     high       ≈1.0       Marginal (k=1)          0.00
                MMTU Schema Matching          0.97     low        ≈0.4             No               −0.11
                AutoDCW Generation            0.87     low        ≈0.2             No               −0.06
                Prof-M (multi-output prof)    0.54     low        ≈0.2             No               −0.07
                MMTU Data Imputation          0.76     low        ≈0.2             No               −0.26
                Prof-S (single-output prof)   0.92     low        ≈0.2             No               −0.42

Table 8 Self-consistency vs. debate on MaTElDa (Claude 4 Sonnet, n=100). Majority vote over independent samples
fails to improve over a single deterministic pass, while debate achieves 2.4× the F1.

                       Condition                      F1         Precision     Recall    Tok/table
                       SA (temp=0)                   0.191         0.279        0.172      4,539
                       SC-3 (k=3, temp=0.7)          0.178         0.291        0.149       7,485
                       SC-5 (k=5, temp=0.7)          0.176         0.268        0.158      12,519
                       Debate (temp=0)              0.465         0.685         0.441      28,558


Practitioner Decision Rule. For practitioners who do not wish to estimate probabilities: (1) Is single-agent
accuracy already high (pg > 0.9)? If so, debate has little room to help. (2) Can the Critic verify each output
by looking at the source data (high pc )? If so, debate can add value. (3) If the Critic finds an error, is the fix
obvious (high pr )? If so, debate will likely help. Use debate only when all three conditions are met.
The debate benefit condition predicts the direction of debate’s effect, but is this finding robust to prompt
design, or could a different Critic formulation eliminate CIC?


6     Controls and Robustness
6.1    Self-Consistency Control
Debate’s detection improvement could reflect structured argumentation or simply the benefit of generating
multiple samples. Self-consistency (SC) (Wang et al., 2023), which samples k independent responses and
aggregating via majority vote, isolates the multi-sample effect without inter-agent interaction.
Table 8 shows self-consistency provides no benefit. SC-5 achieves F1=0.176, below the single-agent baseline
of 0.191. Aggregation lift is negative: majority-vote F1 (0.176) falls below the mean individual sample F1
(0.187). Independent samples share systematic blind spots: cells the model misses at temperature 0 it also
misses across temperature-0.7 samples, and majority vote suppresses occasional correct detections appearing
in only one sample. Debate succeeds through a qualitatively different mechanism: the Critic examines specific
cells the Generator flagged, verifies each claim against the table, and forces evidence-grounded revision. This
interactive verification, not redundant sampling, drives the precision gain from 0.279 to 0.685.

6.2    Prompt Sensitivity
Figure 3 presents the prompt sensitivity results across 6 Critic variants × 4 benchmark-task combinations
(Table 18 in Appendix F provides exact values). The six Critic variants span a range of adversarial intensity:
C1 (Adversarial) is the most aggressive, instructing the Critic to “find errors and challenge every claim”; C2


                                                             9
                                                 AutoDCWMMTU-DIMaTElDaMMTU-ED
                                                  (gen, FC)   (gen, EM)   (det, F1)   (det, F1)
                                                  SA=.799      SA=.785    SA=.301     SA=.760



                               C1 Adversarial      −6.7            −2.0    +18.5       −2.0


                               C2b De-advers.      −7.4            −3.0    +21.9       +1.0


                               C2 Verification     −2.9            −1.5    +12.3       +1.0


                              C3 Constructive      −2.8            −1.5    +27.2       +4.0


                                 C4 Checklist      +1.2        −10.5       +12.6        0.0


                                  C5 Minimal       +1.1            −6.5    +22.6       −16.0


Figure 3 Cross-benchmark Critic design heatmap (delta from single-agent baseline in percentage points). Generation
columns (left of dashed line) show negative or neutral deltas (CIC persists across all Critic designs). Detection
columns (right) show positive deltas (debate consistently helps). No single row is uniformly positive, confirming CIC is
structural.


(Verification) focuses on factual checking without adversarial framing; C2b (De-adversarial) explicitly removes
adversarial language; C3 (Constructive) frames the Critic as a collaborator; C4 (Checklist) uses a structured
verification checklist; C5 (Minimal) provides minimal instructions.
CIC persists across all six Critic variants on generation: on MMTU-DI (n=200), every variant degrades
performance (−1.5 to −10.5pp); on AutoDCWorkflow, four of six variants are negative, consistent with a
structural explanation (Zhang et al., 2025). The two AutoDCWorkflow-positive variants (C4: +1.2pp, C5:
+1.1pp) are the least adversarial: they generate fewer critique items, reducing the surface area for CIC.
Detection benefit is robust but Critic ranking differs: on MaTElDa, all tested variants significantly improve F1
(+12.3 to +27.2pp). The best detection Critic (C3 Constructive: +27.2pp) is among the worst for generation,
reinforcing that no single Critic design works across task types.
The optimal Critic is task-structure-dependent: C4 (Checklist) is best for AutoDCWorkflow (+1.2pp) but
worst for MMTU-DI (−10.5pp), because its “value exists in table” check falsely rejects valid imputations at a
66.3% rate. This false rejection mechanism illustrates how task-agnostic verification heuristics backfire: a
check that is sound for error detection (“does this cell value appear in the original data?”) becomes pathological
for data imputation, where by definition the correct answer does not appear in the original data.
The dashed vertical line in Figure 3 separates generation (left) from detection (right). No row is uniformly
positive, confirming that CIC is a structural property of the task-Critic interaction, not an artifact of any
particular prompt design. This finding directly extends Zhang et al.’s (Zhang et al., 2025) concurrent
observation that “task structure, not model capability or prompt design, determines debate effectiveness.”
CIC persists across all prompt configurations, confirming a structural problem: the Critic’s damage probability
exceeds its rescue probability on non-verifiable tasks regardless of how it is prompted.

6.3    Compliance Mechanism Analysis
Transcript analysis (n=50, 3 Critics × 3 Generators) reveals the mechanism through which CIC operates.
Under the default adversarial configuration (C1×G1), the Generator agrees with 95.3% of Critic feedback
items [95% CI: 93.0–97.5%]. This near-total compliance means the Critic’s error rate translates almost directly
into output degradation. The adversarial Critic raises 23.5 actionable items per task (vs. 2.9 for C2 Verification
and 3.0 for C4 Checklist). Of operations added through debate under C1×G1, 48.1% are grounded in actual
data issues and 51.9% are hallucinated, approximately coin-flip quality.
The compliance mechanism interacts with task difficulty. On easy tasks (SA FC≥0.95), debate produces
∆= − 6.3pp: the Generator already has a correct workflow, and the Critic’s challenges cause it to introduce


                                                              10
Table 9 Code-execution Critic results on AutoDCWorkflow. Paired analysis on tasks common across conditions.
D-Code eliminates CIC (FC ≈ SA); D-Code+G2 significantly exceeds SA.

                                               Claude 4 Sonnet              Qwen3 235B
                      Condition                 FC      ∆ vs SA      FC         ∆ vs SA
                      SA (baseline)            0.814      —         0.907         —
                      D-Text (Adversarial)     0.743     −7.0∗      0.793        −11.4
                      D-Code (Adversarial)     0.817     +0.3       0.930        +2.4
                      D-Code+G2                0.867     +5.3∗        —           —
                      ∗ Significant at α=0.05 (bootstrap, paired). Claude: n=84; Qwen3: n=47.




errors. On hard tasks (SA FC<0.60), debate produces ∆= + 3.2pp: the Generator’s initial workflow is poor,
and even noisy Critic feedback occasionally leads to improvement. This asymmetry explains why CIC damage
scales with pg : when more outputs are correct, there are more opportunities for the Critic to damage them.
Column-level precision/recall/F1 on AutoDCWorkflow (n=100) decomposes FC: all debate conditions maintain
column recall (∼0.786–0.790), but column-level precision varies sharply across conditions: SA=0.461, C1
Adversarial=0.353, C4 Checklist=0.512. CIC thus manifests as precision degradation: the Critic causes the
Generator to target columns that do not need cleaning without missing columns that do. The recall invariance
confirms that debate does not cause the Generator to overlook genuine data quality issues; instead, it causes
the Generator to hallucinate additional, non-existent issues.
The evidence-gated Generator (G2) reduces compliance from 95.3% to 60.3% by requiring the Critic to cite
specific data evidence before acting. Under C1×G2, operations decrease from 13.3 to 9.4 (vs. SA’s 10.3),
preventing the operations inflation that characterizes CIC. The best text-only combination, C2×G2, achieves
FC=0.807 vs. SA=0.780 (+2.7pp). However, at n=50 per cell, no text-only combination reaches statistical
significance (all p>0.05); we report these as directional evidence. Can grounding the Critic’s verification in
executable evidence shift the balance decisively?


7     Grounded Adversarial Verification
7.1    Code-Execution Critics
Our prompt sensitivity analysis shows CIC persists across all six text-only Critic prompt variants. We test
whether giving the Critic a code-execution sandbox, the ability to write and run Python/pandas queries against
the actual data, eliminates CIC by grounding feedback in computed evidence. The Critic writes “ ‘python“ ‘
code blocks executed in a sandboxed subprocess (AST safety check, 30s timeout, 2GB memory limit). We
test two Generator strategies: G1 (engage-all, the default) and G2 (evidence-gated, accepting only feedback
citing specific data evidence).
Table 9 shows code execution eliminates CIC for both models: Claude D-Code FC=0.817 approximately
matches SA (dz =0.02, 95% CI [−0.04, +0.05]); Qwen3 D-Code FC=0.930 exceeds SA (dz =0.06). Adding
evidence-gating produces the strongest result: Claude D-Code+G2 exceeds single-agent (FC=0.867 vs. 0.814,
+5.3pp, p<0.05), the first configuration where debate significantly outperforms SA on a generative task. The
model divergence reveals a compliance×grounding interaction: Claude agrees with 95.3% of Critic feedback;
Qwen3 agrees with ∼60%. With code-grounded feedback, Qwen3’s selective acceptance filters noise and
CIC vanishes. Claude’s high compliance means even grounded feedback is over-applied; evidence-gating
reduces effective compliance, and the combination exceeds SA. CIC severity is thus moderated by Generator
compliance: the cure requires both grounded verification and calibrated acceptance.

7.2    Self-Verification Fails
If the improvement from code-execution debate stems from tool augmentation rather than adversarial
interaction, a single agent with the same pandas sandbox should achieve similar gains. We test this with



                                                        11
SA+Code: the Generator produces a workflow, then self-verifies using the code-execution sandbox before
revising, without a separate Critic.
SA+Code achieves FC=0.801, statistically indistinguishable from SA (∆= − 1.3pp, not significant, n=78
paired). Tools alone do not help. This result connects directly to the debate benefit condition: self-verification
fails because pc ≈ pg : a model checking its own work achieves the same verification accuracy as its generation
accuracy. The rescue-vs-damage inequality becomes approximately balanced. An adversarial Critic breaks
this symmetry by achieving pc > pg through adversarial perspective: it challenges claims the Generator would
not challenge in its own work. This extends the finding of Huang et al. (2024) finding that LLMs cannot
self-correct reasoning to data cleaning, even with grounded tools.

7.3    Factorial Design Summary
The four conditions (SA, SA+Code, D-Text, D-Code+G2) form a 2×2 factorial design crossing adversarial
separation (single-agent vs. debate) with tool augmentation (text-only vs. code-execution). This factorial
reveals an epistatic interaction:
    • No adversarial separation, no tools (SA): FC=0.814. Baseline.
    • No adversarial separation, tools (SA+Code): FC=0.801 (∆= − 1.3pp, n.s.). Tools alone do not help
      because pc ≈ pg .
    • Adversarial separation, no tools (D-Text): FC=0.743 (∆= − 7.0pp, p<0.05). Adversarial separation
      without grounding harms because pc < pg : the Critic generates hallucinated objections.
    • Adversarial separation + tools + evidence-gating (D-Code+G2): FC=0.867 (∆= + 5.3pp, p<0.05).
      The combination significantly exceeds SA because code-execution raises pc above pg and evidence-gating
      ensures only high-quality feedback is accepted.
Neither main effect (adversarial separation alone or tools alone) improves quality. The interaction is positive
and significant: the combination produces a +12.3pp swing from D-Text to D-Code+G2. This epistatic
pattern, where neither component helps independently but their combination produces a strong positive effect,
implies that future multi-agent system designs must consider tool augmentation and compliance calibration
jointly, not as independent design decisions.


8     Discussion, Limitations, and Conclusion
8.1    Cross-Domain Validation
We validate the debate benefit condition against 19 published comparisons across 8 papers and 7 domains (code
generation, mathematical reasoning, factual QA, commonsense inference, reading comprehension, creative
writing, and data analysis). The condition produces zero false positives: every case where debate helps has
high pc and high pr ; every case where debate harms has low pc or low pr . Two mechanisms drive the benefit in
positive cases: verification (the Critic catches errors the Generator misses) and diversity (adversarial pressure
forces exploration of alternative solutions). The condition is sufficient but not necessary: some tasks with
favorable condition values show null effects when pg is already high, leaving no room for improvement.
Table 10 shows the cross-domain validation. The pattern is consistent: tasks where the Critic can verify
outputs against objective evidence (arithmetic via computation, code via test suites, chess via rule checking)
show positive debate effects, often large (+8 to +16pp). Tasks where verification requires subjective judgment
(open-domain QA, medical reasoning without ground truth access) show mixed or negative effects. The
zero false positive rate across 19 comparisons, spanning seven domains, eight research groups, and diverse
model families, provides strong evidence that the debate benefit condition captures a general principle, not a
data-cleaning-specific artifact.
Three patterns emerge from the cross-domain analysis. First, verification infrastructure is the key differentiator:
Du et al.’s arithmetic tasks succeed because each step is computationally verifiable; SWE-Debate succeeds




                                                        12
Table 10 Cross-domain validation of the debate benefit condition across 19 published comparisons. The condition
produces zero false positives.

               Paper           Task                      pc      pr       Predicted     Actual
               Du et al.       Arithmetic               high    ≈1.0       Helps        +14.8pp
               Du et al.       GSM8K                    high    ≈1.0       Helps        +8.0pp
               Du et al.       Chess validity           high    ≈1.0       Helps        +15.9pp
               Zhang et al.    5 QA benchmarks          low     ≈0.5    Hurts/neutral   Mixed
               SWE-Debate      Bug fixing               high    ≈0.5       Helps        SOTA
               Reflexion       HumanEval                high    ≈0.5       Helps        +10.9pp
               Khan et al.     QuALITY                  high    ≈1.0       Helps        76–88%
               Liang et al.    Translation              high    ≈0.5       Helps        +1.7 COMET
               Smit et al.     MedQA                    low     ≈0.5    Hurts/neutral   Mixed
               ReConcile       Date Understanding       high    ≈1.0       Helps        +11.4pp
               Selected 10 of 19 comparisons shown. Full table in Appendix.



because test suites provide automated verification; Reflexion succeeds because HumanEval provides execution-
based feedback. Second, high pr is not sufficient without high pc : Zhang et al.’s QA benchmarks have relatively
constrained answer spaces (pr ≈ 0.5), but the Critic cannot reliably distinguish correct from incorrect answers
without evidence access (pc is low), leading to mixed results. Third, the condition is conservative: some tasks
predicted as “helps” show null effects (when pg is already high), but no task predicted as “hurts/neutral” shows
a significant positive effect.
The Critic functions as a verification catalyst on decomposable tasks but undergoes poisoning on non-verifiable
ones: without evidence to ground its challenges, adversarial pressure produces hallucinated feedback that the
Generator accepts uncritically. The compliance × grounding interaction is epistatic: neither code-execution
grounding alone (self-verification ≈ SA) nor text-only debate (D-Text < SA) improves quality, but their
combination with evidence-gated compliance significantly exceeds single-agent.

8.2    Model Predictions and Boundaries
The debate benefit condition generates three testable predictions. We evaluate each against our experimental
data and identify where the model succeeds and where it requires refinement.

Prediction 1: CIC severity scales negatively with Generator accuracy. If CIC arises from hallucinated Critic
feedback corrupting correct outputs, its severity should increase as the Generator’s baseline accuracy (pg )
increases, since there are more correct outputs to corrupt. Across all 100 AutoDCWorkflow tasks in the
prompt sensitivity sweep, the correlation between single-agent FC and debate delta is r = −0.249 (p = 0.013,
n = 100): tasks where the Generator is already accurate show larger debate degradation. This confirms
the prediction: CIC damage scales with pg because there are more correct operations available to retract.
The correlation is moderate rather than strong because pc and α also vary across tasks; the debate benefit
condition involves three interacting quantities, not just pg .

Prediction 2: Debate helps iff pc > pg . The condition implies a sharp boundary: debate helps when the
Critic’s verification accuracy exceeds the Generator’s baseline accuracy, and hurts otherwise. We test this
bidirectionally across two benchmarks:
   • MaTElDa (detection): Single-agent precision pg = 0.279; debate precision (proxy for pc ) = 0.685. Since
     pc = 0.685 > pg = 0.279, the condition predicts debate helps. Confirmed: ∆F1 = +27.4pp (p < 0.001).
   • AutoDCWorkflow (generation): Single-agent FC pg = 0.814; estimated Critic accuracy pc ≈ 0.481 (from
     transcript analysis: 48.1% of Critic-suggested operations are grounded). Since pc = 0.481 < pg = 0.814,
     the condition predicts debate hurts. Confirmed: ∆FC = −7.0pp (p < 0.05, D-Text condition).
The bidirectional confirmation (debate helps when pc > pg and hurts when pc < pg ) provides direct evidence
for the rescue-vs-damage mechanism.


                                                          13
Prediction 3 (refined): Evidence-gating is selective, not uniform. The initial model predicted that evidence-
gated generation (G2) would uniformly reduce compliance and thus uniformly reduce CIC. The empirical
result is more nuanced: G2 reduces compliance from 95.3% to 60.3%, but the reduction is selective: the
Generator preferentially rejects ungrounded feedback while accepting evidence-backed feedback. This means
evidence-gating does not simply lower α uniformly; it effectively raises pc by filtering out low-quality critiques.
The initial prediction of uniform compliance reduction is falsified, but the refined mechanism (selective
filtering) explains why D-Code+G2 exceeds single-agent: evidence-gating increases the effective pc of accepted
feedback, pushing the rescue-damage balance decisively positive.
These three predictions (two confirmed, one refined) demonstrate that the debate benefit condition is not
merely descriptive but generates falsifiable hypotheses about debate dynamics. The refined understanding of
evidence-gating (Prediction 3) suggests a general principle: compliance calibration mechanisms that selectively
filter feedback quality are more effective than those that uniformly reduce compliance.

Structural Hallucination and Cascade Amplification. Debate’s harm on generative tasks manifests through
two mechanisms. Structural hallucination: cell accuracy is nearly identical across topologies for Claude (0.894
vs. 0.899, p=0.83), meaning operations that execute produce equally clean data, but the Critic causes the
Generator to propose operations targeting non-existent columns. Cascade amplification: a data cleaning
workflow is a sequence of dependent operations, so a single hallucinated critique propagates through the
revision; detection tasks are atomic, so critique errors do not compound.

Connection to Scalable Oversight. Irving et al. (2018) proposed debate for scalable alignment, Leike et al.
(2018) extended this to recursive reward modeling. The debate benefit condition provides an empirical
operationalization: adversarial verification succeeds when outputs decompose into independently checkable
claims but fails when the verifier cannot ground objections in specific data. Per-item verifiability may thus
moderate debate effectiveness in any domain where outputs vary in decomposability.

Practitioner Guidance.    Three actionable principles emerge:
   1. Route by the debate benefit condition, not data domain. High pc + high pr + room in pg (detection,
      matching, per-item repair): use debate. Low pc or low pr (imputation, generation, transformation): use
      single-agent. At 10K rows, debate’s detection advantage persists (+10.0pp, p=0.011) but diminishes
      from +27.4pp at 100 rows.
   2. Always anonymize; never split data naively. Anonymization is a zero-cost improvement (+2.2pp FC);
      a 50% data split creates information asymmetry that outweighs verification benefits.
   3. Budget for variance, not just mean shift. Debate increases perfect-score outputs (22→28) while
      introducing complete failures. Production deployments should add structural validation to catch
      hallucinated operations.

8.3    Scale Validation
All main experiments use small tables (5–100 rows) that fit entirely within the LLM’s context window. To
validate that the debate benefit condition holds at larger scale, we conduct a preliminary scale validation
on MaTElDa tables with ≥10,000 rows (n=15 tables, Claude 4 Sonnet). Tables are processed using non-
overlapping 500-row chunks, with cell-level detections unioned across chunks and deduplicated at chunk
boundaries.
At 10K rows, debate’s detection advantage persists: ∆F1 = +10.0pp (dz = 0.75, p = 0.011), with debate
winning 11 of 15 tables. The magnitude diminishes from +27.4pp at 100 rows to +10.0pp at 10K rows, a 63%
reduction. Two factors explain this attenuation: (1) attention dilution: in larger tables, both Generator and
Critic miss more errors in each chunk because each chunk contains proportionally fewer errors relative to the
noise floor; (2) chunk boundary effects: errors spanning chunk boundaries are detected inconsistently across
chunks, and the Critic cannot verify cross-chunk patterns.
Importantly, the direction of the effect is preserved at scale: debate still helps detection at 10K rows.
This is consistent with the debate benefit condition: the structural properties that determine pc (evidence


                                                        14
groundability) and pr (answer-space constraint) do not change with table size. What changes is the absolute
magnitude of pg and pc (both decrease with scale) as the task becomes harder, but the relative inequality
pc > pg is preserved for detection tasks.
For Qwen3 and DeepSeek, both models produce near-zero F1 at 10K rows regardless of topology, suggesting a
capability threshold below which neither single-agent nor debate can operate effectively on large tables. This
finding does not invalidate the debate benefit condition; it reveals a precondition: the debate benefit condition
applies only when the Generator has non-trivial baseline capability (pg > 0). Scale validation on generative
tasks remains future work.

Cross-Domain Evidence and Future Work. Independent results provide consistency evidence: SWE-Debate (Li
et al., 2025) achieves state-of-the-art on SWE-bench via multi-agent debate, where each code fix is verifiable
via test suites; Reflexion (Shinn et al., 2023) shows verbal feedback with test execution improves code
generation. These results corroborate the debate benefit condition’s prediction that debate helps when outputs
are independently verifiable.
The zero false positive rate across 19 cross-domain comparisons (Table 10) suggests the debate benefit condition
captures a domain-general principle. However, direct validation on additional domains (mathematical proof
verification, scientific claim checking, and multi-step planning, remains future work. The most promising
extension is compliance calibration: exploring explicit compliance thresholds or confidence-based filtering to
further improve tool-augmented debate for generative tasks. Our evidence-gating mechanism (G2) is a first
step, but more sophisticated approaches, such as calibrated confidence scores on Critic feedback or learned
acceptance policies, could further improve the rescue-damage balance.

8.4    Limitations
Several limitations qualify our findings.

Evaluation Coverage. Our deterministic executor implements ∼20 common operations with fuzzy matching;
unrecognized operations are skipped, potentially undercounting semantic quality. Future work should explore
LLM-as-judge evaluation (Zheng et al., 2023) and execution-based cell-level precision/recall/F1 with a full
sandbox.

Model Coverage. We test four model families (Claude 4 Sonnet, Gemini 3.1 Pro, Qwen3 235B, DeepSeek
R1) with consistent findings across all four, though Gemini’s improvement partly reflects format scaffolding
(87% zero-F1 outputs under SA due to unparseable JSON, reduced to 42% under debate). The debate
benefit condition should be validated on additional model families, particularly smaller models where baseline
capability (pg ) may be too low for debate to help.

Scale Limitations. The main experiments use single-table tasks with small tables (5–100 rows). Preliminary
scale validation at 10K rows (n=15, Section 8.3) shows debate’s advantage persists for Claude (+10.0pp F1,
dz =0.75) but Qwen3 and DeepSeek produce near-zero F1 at this scale regardless of topology. Production
data cleaning involves tables with 10K–10M+ rows, multi-table joins, and streaming updates, none of which
are tested here. The chunking strategy used for scale validation (non-overlapping 500-row chunks) may not be
optimal; future work should explore overlapping chunks, schema-guided sampling, and hierarchical detection
strategies.

Statistical Power. With n=50 for AutoDCWorkflow, several effects show consistent direction but lack
significance after Holm-Bonferroni correction; the MaTElDa result (n=100, p<0.001) is the most statistically
robust finding. The cross-model MMTU results (n=200) provide additional power but no individual task-type
comparison reaches significance after correction.

Topology Scope. We test only the two-agent Generator-Critic topology. Multi-agent topologies with three or
more agents (e.g., panel discussions, tournament brackets) may exhibit different dynamics. The debate benefit



                                                       15
condition’s three-parameter framework should extend to multi-agent settings, but the compliance dynamics
become more complex with multiple Critics or multiple Generators.

8.5    Conclusion
Multi-agent debate is not a universal improvement for LLM-based data cleaning. Its effect is governed by
the debate benefit condition: debate helps when rescue exceeds damage (pc /(1−pc ) × pr > pg /(1−pg )). The
condition correctly predicts all nine task types and generalizes with zero false positives across 19 published
comparisons in seven domains. Three key findings emerge from over 6,000 task-condition pairs across four
model families:
   1. Task structure determines debate’s sign. Debate improves error detection (+27.4pp F1, d=1.0) but
      degrades generation across all four models (−1.6 to −15.5pp). The boundary is per-item verifiability:
      when each output can be independently checked against source data, the Critic adds value; when outputs
      form dependent chains, hallucinated feedback cascades through revisions.
   2. CIC is structural, not prompt-dependent. A sweep across 6 Critic variants confirms that no text-only
      prompt design eliminates CIC on generative tasks. Self-consistency (k=5 majority vote) performs worse
      than single-agent, ruling out the multi-sample explanation for debate’s detection benefit.
   3. The fix requires both grounding and calibration. A factorial experiment proves adversarial separation
      is essential: self-verification fails because pc ≈ pg , while a separate Critic with code-execution grounding
      and evidence-gated generation produces the first debate configuration to significantly exceed single-agent
      on generation (+5.3pp, p<0.05). Neither component helps independently; the interaction is epistatic.
For practitioners: use debate when pg is low, pc is high, and pr is high. When these conditions are not
met, single-agent cleaning is both more effective and 4–6× cheaper. When the conditions are marginal,
code-execution grounding with evidence-gated compliance can shift the balance.

Code and Data Availability. Experiment code, prompts, raw result JSONs, and the deterministic workflow
executor are available in the supplementary material. The AutoDCWorkflow benchmark (Li et al., 2024a),
MMTU benchmark (Xing et al., 2025), and MaTElDa benchmark (Ahmadi et al., 2025) are publicly available.


Acknowledgements
Acknowledgements
We thank Mahesh Srinivasan for his leadership and support throughout this project, and Aparajita Choudhury
and Christopher Schrader for valuable feedback on earlier drafts.


References
Fatemeh Ahmadi, Marc Speckmann, Malte F. Kuhlmann, and Ziawasch Abedjan. MaTElDa: Multi-table error
  detection. In Proceedings of the 28th International Conference on Extending Database Technology (EDBT), pages
  364–376, 2025. doi: 10.48786/EDBT.2025.29.
Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna
  Goldie, Azalia Mirhoseini, Cameron McKinnon, et al. Constitutional AI: Harmlessness from AI feedback. arXiv
  preprint arXiv:2212.08073, 2022.
Samuel R. Bowman, Jeeyoon Hyun, Ethan Perez, Edwin Chen, Craig Pettit, Scott Heiner, Kameré Lukić, Roger
  Banber, Adian Marcus, Karina Kim, and William Saunders. Measuring progress on scalable oversight for large
  language models. arXiv preprint arXiv:2211.03540, 2022.
Chi-Min Chan, Weize Chen, Yusheng Su, Jianxuan Yu, Wei Xue, Shanghang Zhang, Jie Fu, and Zhiyuan Liu. ChatEval:
  Towards better LLM-based evaluators through multi-agent debate. In Proceedings of the 12th International Conference
  on Learning Representations (ICLR), 2024.



                                                         16
Justin Chih-Yao Chen, Swarnadeep Saha, and Mohit Bansal. ReConcile: Round-table conference improves reasoning
  via consensus among diverse LLMs. In Proceedings of the 62nd Annual Meeting of the Association for Computational
  Linguistics (ACL), 2024.
Hyeong Kyu Choi, Xiaojin Zhu, and Sharon Li. When identity skews debate: Anonymization for bias-reduced
  multi-agent reasoning. arXiv preprint arXiv:2510.07517, 2025.
Xu Chu, John Morcos, Ihab F. Ilyas, Mourad Ouzzani, Paolo Papotti, Nan Tang, and Yin Ye. KATARA: A data
  cleaning system powered by knowledge bases and crowdsourcing. In Proceedings of the 2015 ACM SIGMOD
 International Conference on Management of Data, pages 1247–1261, 2015.
Michele Dallachiesa, Amr Ebaid, Ahmed Eldawy, Ahmed Elmagarmid, Ihab F. Ilyas, Mourad Ouzzani, and Nan Tang.
  NADEEF: A commodity data cleaning system. In Proceedings of the 2013 ACM SIGMOD International Conference
 on Management of Data, pages 541–552, 2013.
Tamraparni Dasu and Theodore Johnson. Exploratory Data Mining and Data Cleaning. Wiley, 2003.
Hong-Hai Do and Erhard Rahm. COMA—a system for flexible combination of schema matching approaches. In
  Proceedings of the 28th International Conference on Very Large Data Bases (VLDB), pages 610–621, 2002.
Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, and Igor Mordatch. Improving factuality and reasoning
  in language models through multiagent debate. In Proceedings of the 41st International Conference on Machine
  Learning (ICML), 2024.
Bradley Efron and Robert J. Tibshirani. An Introduction to the Bootstrap. Chapman and Hall/CRC, 1993.
Wenfei Fan and Floris Geerts. Foundations of Data Quality Management. Morgan & Claypool Publishers, 2012.
Xi Fang, Weijie Xu, Fiona Anting Tan, Jiani Zhang, Ziqing Hu, Yanjun Qi, Scott Nickleach, Diego Socolinsky, Srinivasan
  Sengamedu, and Christos Faloutsos. Large language models (LLMs) on tabular data: Prediction, generation, and
  understanding—a survey. Transactions on Machine Learning Research (TMLR), 2024.
Alireza Heidari, Joshua McGrath, Ihab F. Ilyas, and Theodoros Rekatsinas. HoloDetect: Few-shot learning for error
  detection. In Proceedings of the 2019 International Conference on Management of Data (SIGMOD), pages 1171–1188,
  2019.
Sture Holm. A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics, 6(2):65–70,
  1979.
Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang,
   Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, and Jürgen Schmidhuber.
   MetaGPT: Meta programming for a multi-agent collaborative framework. In Proceedings of the 12th International
  Conference on Learning Representations (ICLR), 2024.
Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou.
   Large language models cannot self-correct reasoning yet. In International Conference on Learning Representations
  (ICLR), 2024.
Ihab F. Ilyas and Xu Chu. Data cleaning: Overview and emerging challenges. Proceedings of the ACM SIGMOD
  International Conference on Management of Data, pages 2201–2206, 2019.
Geoffrey Irving, Paul Christiano, and Dario Amodei. AI safety via debate. arXiv preprint arXiv:1805.00899, 2018.
Akbir Khan, John Hughes, Dan Valentine, Laura Ruis, Kshitij Sachan, Ansh Radhakrishnan, Edward Grefenstette,
  Samuel R. Bowman, Tim Rocktäschel, and Ethan Perez. Debating with more persuasive LLMs leads to more
  truthful answers. In Proceedings of the 41st International Conference on Machine Learning (ICML), volume 235 of
  PMLR, 2024.
Christos Koutras, George Siachamis, Andra Ionescu, Kyriakos Psarakis, Jerry Brons, Marios Fragkoulis, Christoph
  Lofi, Angela Bonifati, and Asterios Katsifodimos. Valentine: Evaluating matching techniques for dataset discovery.
  Proceedings of the 2021 IEEE 37th International Conference on Data Engineering (ICDE), pages 468–479, 2021.
Sanjay Krishnan, Jiannan Wang, Eugene Wu, Michael J. Franklin, and Ken Goldberg. ActiveClean: Interactive data
  cleaning for statistical modeling. Proceedings of the VLDB Endowment, 9(12):948–959, 2016.
Jan Leike, David Krueger, Tom Everitt, Miljan Martic, Vishal Maini, and Shane Legg. Scalable agent alignment via
  reward modeling: A research direction. arXiv preprint arXiv:1811.07871, 2018.




                                                         17
Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. CAMEL:
 Communicative agents for “mind” exploration of large language model society. In Advances in Neural Information
 Processing Systems (NeurIPS), 2023.
Han Li, Yuling Shi, Shaoxin Lin, Xiaodong Gu, Heng Lian, Xin Wang, Yantao Jia, Tao Huang, and Qianxiang Wang.
  SWE-Debate: Competitive multi-agent debate for software issue resolution. arXiv preprint arXiv:2507.23348, 2025.
Lan Li, Liri Fang, Bertram Ludäscher, and Vetle I. Torvik. AutoDCWorkflow: LLM-based data cleaning workflow
  auto-generation and benchmark. arXiv preprint arXiv:2412.06724, 2024a.
Peng Li, Yeye He, Dror Yashar, Weiwei Cui, Song Ge, Haidong Zhang, Danielle Rifinski Fainman, Dongmei Zhang,
  and Surajit Chaudhuri. Table-GPT: Table fine-tuned GPT for diverse table tasks. Proceedings of the ACM on
  Management of Data, 2(3), 2024b. doi: 10.1145/3654979.
Yuliang Li, Jinfeng Li, Yoshihiko Suhara, AnHai Doan, and Wang-Chiew Tan. Deep entity matching with pre-trained
  language models. Proceedings of the VLDB Endowment, 14(1):50–60, 2020.
Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang, Yujiu Yang, Zhaopeng Tu, and Shuming
  Shi. Encouraging divergent thinking in large language models through multi-agent debate. In Proceedings of the
  62nd Annual Meeting of the Association for Computational Linguistics (ACL), 2024.
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri,
 Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean
 Welleck, Amir Yazdanbakhsh, and Peter Clark. Self-refine: Iterative refinement with self-feedback. Advances in
 Neural Information Processing Systems (NeurIPS), 2023.
Mohammad Mahdavi, Ziawasch Abedjan, Raul Castro Fernandez, Samuel Madden, Mourad Ouzzani, Michael
 Stonebraker, and Nan Tang. Raha: A configuration-free error detection system. Proceedings of the ACM SIGMOD
 International Conference on Management of Data, pages 865–882, 2019.
Sidharth Mudgal, Han Li, Theodoros Rekatsinas, AnHai Doan, Youngchoon Park, Ganesh Karahalios, and Dipanjan
  Krishnan. Deep learning for entity matching: A design space exploration. In Proceedings of the 2018 International
  Conference on Management of Data (SIGMOD), pages 19–34, 2018.
Avanika Narayan, Ines Chami, Laurel Orr, and Christopher Ré. Can foundation models wrangle your data? Proceedings
  of the VLDB Endowment, 16(4):738–746, 2022.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini
  Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. In
  Advances in Neural Information Processing Systems (NeurIPS), 2022.
Alicia Parrish, Harsh Trivedi, Ethan Perez, Angelica Chen, Nikita Ringel, and Samuel R. Bowman. Single-turn debate
  does not help humans answer hard reading-comprehension questions. In arXiv preprint arXiv:2204.05212, 2022.
Ralph Peeters and Christian Bizer. Using ChatGPT for entity matching. In Proceedings of the 27th International
 Conference on Extending Database Technology (EDBT), 2024.
Danrui Qi and Jiannan Wang. CleanAgent: Automating data standardization with LLM-based agents. arXiv preprint
  arXiv:2403.08291, 2024.
Theodoros Rekatsinas, Xu Chu, Ihab F. Ilyas, and Christopher Ré. HoloClean: Holistic data repairs with probabilistic
  inference. Proceedings of the VLDB Endowment, 10(11):1190–1201, 2017.
Mrinank Sharma, Meg Tong, Tomasz Korbak, David Duvenaud, Amanda Askell, Samuel R. Bowman, et al. Towards
 understanding sycophancy in language models. In Proceedings of the 12th International Conference on Learning
 Representations (ICLR), 2024.
Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion:
  Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems (NeurIPS),
  2023.
Yashar Talebirad and Amirhossein Nadiri. Multi-agent collaboration: Harnessing the power of intelligent LLM agents.
  arXiv preprint arXiv:2306.03314, 2023.
Qineng Wang, Zihao Wang, Ying Su, Hanghang Tong, and Yangqiu Song. Rethinking the bounds of LLM reasoning:
  Are multi-agent discussions the key? In Proceedings of the 62nd Annual Meeting of the Association for Computational
  Linguistics (ACL), pages 6106–6131, 2024a.



                                                         18
Richard Y. Wang and Diane M. Strong. Beyond accuracy: What data quality means to data consumers. Journal of
  Management Information Systems, 12(4):5–33, 1996.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models. In Proceedings of the 11th International
 Conference on Learning Representations (ICLR), 2023.
Zhenhailong Wang, Shaoguang Mao, Wenshan Wu, Tao Ge, Furu Wei, and Heng Ji. Unleashing the emergent cognitive
  synergy in large language models: A task-solving agent through multi-persona self-collaboration. In Proceedings of
  NAACL, 2024b. arXiv:2307.05300.
Jerry Wei, Da Huang, Yifeng Lu, Denny Zhou, and Quoc V. Le. Simple synthetic data reduces sycophancy in large
  language models. arXiv preprint arXiv:2308.03958, 2024.
Steven Euijong Whang, Yuji Roh, Hwanjun Song, and Jae-Gil Lee. Data collection and quality challenges in deep
  learning: A data-centric AI perspective. The VLDB Journal, 32(4):791–813, 2023.
Haolun Wu, Zhenkun Li, and Lingyao Li. Can LLM agents really debate? A controlled study of multi-agent debate in
  logical reasoning. arXiv preprint arXiv:2511.07784, 2025.
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xu Zhang, Shaokun Zhang,
  Jiale Liu, Ahmed Hassan Awadallah, Ryen W. White, Doug Burger, and Chi Wang. AutoGen: Enabling next-gen
  LLM applications via multi-agent conversation. In Proceedings of the 1st Conference on Language Modeling (COLM),
  2024.
Junjie Xing, Yeye He, Mengyu Zhou, Haoyu Dong, Shi Han, Lingjiao Chen, Dongmei Zhang, Surajit Chaudhuri,
  and H. V. Jagadish. MMTU: A massive multi-task table understanding and reasoning benchmark. arXiv preprint
  arXiv:2506.05587, 2025. Accepted at NeurIPS 2025.
Yongjin Yang, Euiin Yi, Jongwoo Ko, Kimin Lee, Zhijing Jin, and Se-Young Yun. Revisiting multi-agent debate as
  test-time scaling: A systematic study of conditional effectiveness. arXiv preprint arXiv:2505.22960, 2025.
Hangfan Zhang, Zhiyao Cui, Jianhao Chen, Xinrun Wang, Qiaosheng Zhang, Zhen Wang, et al. Stop overvaluing
  multi-agent debate – we must rethink evaluation and embrace model heterogeneity. arXiv preprint arXiv:2502.08788,
  2025.
Haochen Zhang, Yuyang Dong, Chuan Xiao, and Masafumi Oyamada. Jellyfish: A large language model for data
  preprocessing. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
 (EMNLP), 2024a.
Jintian Zhang, Xin Xu, Ningyu Zhang, Ruibo Liu, Bryan Hooi, and Shumin Deng. Exploring collaboration mechanisms
   for LLM agents: A social psychology view. In Proceedings of the 62nd Annual Meeting of the Association for
  Computational Linguistics (ACL), pages 14544–14607, 2024b.
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li,
  Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. Judging LLM-as-a-judge with MT-Bench
  and chatbot arena. In Advances in Neural Information Processing Systems (NeurIPS), 2023.



A     Debate Architecture
B     Anonymization Full Results

Table 11 Anonymization experiment: Effect of response anonymization (Claude 4 Sonnet, n = 50). Neither FC nor
cell accuracy differences reach statistical significance after correction.

          Condition                      FC ↑    Cell Acc ↑    Exec Rate ↑      Hall. Rate     Tok/task
          Debate (anonymized)            0.825      0.898          0.620           20.2%        14,087
          Debate (not anonymized)        0.803      0.915          0.612           22.3%        14,654
          FC: ∆= + 0.022, 95% CI [−0.035, 0.069], p=0.39
          Cell Acc: ∆= − 0.018, 95% CI [−0.079, 0.033], p=0.54



                                                        19
                             Anonymization: role labels → Agent A / Agent B




                           Generator           JSON workflow              Critic
                           (Agent A)                                    (Agent B) up to 3 rounds
                                          accept / revise

                           input                                              if hallucinated
                                        Generator complies verify against

                                                                         CIC Risk
                          Dirty Table
                                                                    Hallucinated feedback
                             Tdirty
                                                                     → retract valid ops


Figure 4 Generator-Critic debate architecture. The Generator proposes structured JSON outputs; the Critic challenges
each against the source table and returns accept/revise with evidence. Anonymization (dotted line) replaces role labels
with neutral identifiers. When the Critic’s feedback is itself hallucinated, the Generator retracts correct operations,
the CIC failure mode (orange path).


Anonymization produces a consistent directional improvement in FC (+2.2pp) and reduction in hallucination
rate (−2.1pp), though neither reaches statistical significance at n=50. Cell accuracy shows a slight advantage
for non-anonymized debate (0.915 vs. 0.898), also not significant. The mechanism: without anonymization,
the Critic hedges its objections (“The Generator’s workflow is mostly sound, with minor suggestions...”), while
anonymized Critics reject outright (“Agent A’s step 3 references column ‘inspection_date’ which does not
exist in the provided data”).


C     Task Isolation Full Results

Table 12 Task isolation experiment: Effect of task-isolated data sampling (Claude 4 Sonnet, n = 50).

         Condition                   FC ↑      Cell Acc ↑        Exec Rate ↑         Std     Avg Ops   Tok/task
         Debate (50% isolation)      0.776        0.913             0.609         0.272         6.6     14,299
         Debate (no isolation)       0.836        0.946             0.628         0.188         8.0     18,845
         FC: ∆= − 0.060, 95% CI [−0.146, 0.001], p=0.084
         Cell Acc: ∆= − 0.033, 95% CI [−0.100, −0.007], p=0.055

Task isolation reduces factual consistency by 6.0pp (p=0.084) and cell accuracy from 0.946 to 0.913. The
mechanism is an information asymmetry trap: the Generator sees only half the table and proposes fewer
operations (6.6 vs. 8.0), while the Critic verifies against different data where issues manifest differently, leading
to false rejections. Per-task analysis shows the effect is nearly symmetric: 18 tasks improve, 20 worsen, 12
unchanged.

Table 13 Isolation strategy gradient. The 90/10 split slightly outperforms no isolation while using 25% fewer tokens.
Only the aggressive 50/50 split hurts.

                          Strategy                FC        Std       CA       Ops     Tok/task
                          No isolation          0.836       0.186     —        8.0         18,845
                          90/10 row split       0.849       0.219    0.925     6.8         14,213
                          Column masking        0.838       0.188    0.879     7.7         16,975
                          50/50 row split       0.776       0.269     —        6.6         14,299



                                                            20
The gradient suggests isolation is not inherently harmful; only aggressive row partitioning is. The 90/10
split achieves the highest FC (0.849, d=+0.06) while reducing tokens by 25%. Column masking matches no
isolation exactly (0.838 vs. 0.836). Paired bootstrap CIs for both isolation gradient conditions vs. the 50/50
split include zero (90/10: [−0.013, +0.164]; column mask: [−0.003, +0.132]).


D      Bootstrap CI and Cost-Quality Tables
All pairwise comparisons use BCa (bias-corrected and accelerated) bootstrap (Efron and Tibshirani, 1993),
which adjusts for skewness in the sampling distribution. We verified via simulation from the fitted two-
component Gaussian mixture model that empirical CI coverage remains above 93% for the bimodal FC data.
For paired designs, dz (mean of paired differences / SD of differences) is the standard measure. We report
dpooled for comparability with between-subjects studies. In our data, dpooled and dz diverge by <0.12 across
all comparisons: MaTElDa Claude dpooled =1.00, dz =0.94; Gemini dpooled =0.95, dz =0.88. No qualitative
interpretation changes.

Table 14 Paired bootstrap confidence intervals (10,000 BCa resamples, 95% CI) with Holm-Bonferroni correction. ∆
uses first-minus-second convention (e.g., SA minus Debate for the debate comparison); main text uses Debate-minus-SA,
so signs are reversed.

            Comparison                 Metric          ∆             95% CI          praw      pcorr       Sig?
            Claude SA vs. Debate         FC        +0.016        [−0.039, 0.108]     0.698     1.000       n.s.
            Claude SA vs. Debate       Cell Acc    −0.006        [−0.063, 0.051]     0.832     1.000       n.s.
            Anon vs. No-Anon             FC        +0.022        [−0.035, 0.069]     0.385     1.000       n.s.
            Anon vs. No-Anon           Cell Acc    −0.018        [−0.079, 0.033]     0.538     1.000       n.s.
            Isolation vs. No-Iso         FC        −0.060        [−0.146, 0.001]     0.084     0.420       n.s.
            Isolation vs. No-Iso       Cell Acc    −0.033       [−0.100, −0.007]     0.055     0.328       n.s.


Table 15 Cost-quality summary across all conditions (Claude 4 Sonnet).

                 Condition                     FC ↑    Cell Acc ↑      Tok/task      FC per 1K tok
                 Single Agent                  0.871         0.894          3,281            0.265
                 Debate (anon, no iso)         0.836         0.946         18,845            0.044
                 Debate (anon + iso)           0.776         0.913         14,299            0.054
                 Debate (no anon, no iso)      0.803         0.915         14,654            0.055

Single-agent cleaning achieves 0.265 FC per 1K tokens, 4.8–6.0× more efficient than any debate variant.


E     MMTU Detailed Results

Table 16 MMTU results: single-agent vs. debate across four table understanding tasks (Claude 4 Sonnet, n=200).
Score is task-specific: F1 for ED/SM, exact match for DI, accuracy for EM.

               Task Type             Single-Agent      Debate          ∆            95% CI             d
               Error-Detect              0.820             0.840     +0.020    [−0.12, +0.16]        +0.05
               Data-Imputation           0.760             0.640     −0.120    [−0.30, +0.06]        −0.26
               Entity-Matching           0.980             1.000     +0.020    [+0.00, +0.06]        +0.20
               Schema-Matching           0.968             0.957     −0.010    [−0.05, +0.02]        −0.11
               Overall                   0.882         0.859         −0.023    [−0.09, +0.04]        −0.07
               Total tokens                            376K vs. 1,381K              3.7× overhead



                                                           21
Table 17 Cross-model MMTU results (n=200 questions each).

              Model                   SA Overall    Debate Overall          ∆         SA ED     Debate ED
              Claude 4 Sonnet           0.882             0.859           −0.023      0.820         0.840
              Qwen3 235B                0.752             0.764           +0.012      0.520         0.640
              DeepSeek R1               0.760             0.777           +0.017      0.600         0.640

Table 18 Cross-benchmark effect of Critic design on debate quality (delta from single-agent baseline in percentage
points, pp). No single Critic variant is optimal across all benchmarks.

                                                    Generation                     Detection
                        Critic              AutoDCW        MMTU-DI        MaTElDa       MMTU-ED
                        Variant               (FC)          (EM)            (F1)          (F1)
                        SA baseline             0.799         0.785         0.301          0.760
                                                                                  ∗
                        C1 Adversarial          −6.7         −2.0          +18.5           −2.0
                        C2b De-advers.          −7.4         −3.0          +21.9†          +1.0
                        C2 Verification         −2.9         −1.5          +12.3∗          +1.0
                        C3 Constructive         −2.8         −1.5          +27.2†          +4.0
                        C4 Checklist            +1.2         −10.5         +12.6∗           0.0
                        C5 Minimal              +1.1         −6.5          +22.6†          −16.0
∗ Significant after Holm-Bonferroni (p<0.05), n=100. † Significant at n=20 (not re-run at n=100). AutoDCW: n=100 (C1, C2b,

C4) or n=20 (C2, C3, C5). MMTU-DI: n=200. MaTElDa: n=100 (C1, C2, C4) or n=20 (C2b, C3, C5). MMTU-ED: n=100.
FWER is controlled per benchmark column: each column’s Critic variants are corrected as a family (3–6 comparisons against the
shared SA baseline), not across the full 24-cell table.


Data Imputation shows the largest degradation (−12.0pp, d= − 0.26); debate flipped 7 DI tasks from correct
to incorrect while rescuing only 1. Entity Matching reaches ceiling (1.000 vs. 0.980). Cross-model: Qwen3 ED
improves from 0.520 to 0.640 (+12.0pp); DeepSeek ED from 0.600 to 0.640 (+4.0pp). Both models show DI
degradation (Qwen3: 0.58 → 0.52; DeepSeek: mixed).


F     Prompt Sensitivity Detailed Analysis
CIC Mechanism. Column-level precision/recall/F1 on AutoDCWorkflow (n=100) decomposes FC: all debate
conditions maintain column recall (∼0.786–0.790), but precision varies sharply: SA=0.461, C1=0.353,
C4=0.512. CIC manifests as precision degradation: debate causes the Generator to target columns that do
not need cleaning without missing columns that do.

Compliance Analysis. Transcript analysis (n=50, 3 Critics × 3 Generators) reveals the compliance mechanism.
Under C1×G1, the Generator agrees with 95.3% of Critic feedback items [95% CI: 93.0–97.5%]. The adversarial
Critic raises 23.5 actionable items per task (vs. 2.9 for C2 and 3.0 for C4). Of operations added through debate
under C1×G1, 48.1% are grounded and 51.9% are hallucinated, approximately coin-flip quality. CIC is worse
on easy tasks (SA FC≥0.95: debate ∆= − 6.3pp) and beneficial on hard tasks (SA FC<0.60: ∆= + 3.2pp),
consistent with the Critic disrupting already-correct solutions.

Generator Response Strategy (Exploratory). The evidence-gated Generator (G2) reduces compliance from
95.3% to 60.3% by requiring the Critic to cite specific data evidence before acting (Madaan et al., 2023). Under
C1×G2, operations decrease from 13.3 to 9.4 (vs. SA’s 10.3), preventing the ops inflation that characterizes
CIC. The best combination, C2×G2, achieves FC=0.807 vs. SA=0.780 (+2.7pp). However, at n=50 per cell, no
Phase 2 comparison reaches statistical significance (all p>0.05); we report these as directional evidence (Yang
et al., 2025; Wu et al., 2025).




                                                            22
G     Full Experimental Results
Table 19 Selected AutoDCWorkflow results across conditions and models. Cell Acc and Exec Rate are computed via
the deterministic workflow executor. Qwen3 and DeepSeek AutoDCWorkflow results appear in Table 1 (main text).
All comparisons within each hypothesis are paired on identical task sets.

      Model                Condition                      n        FC       Cell       Exec         Std    Compl.     Tok/task
      AutoDCWorkflow (Workflow Generation)
                           Single Agent                  50       0.871    0.894       0.716    0.137      100%         3,281
                           Debate (anon+iso)             50       0.855    0.899       0.628    0.231      98%         14,056
                           Debate (anon, iso)            50       0.825    0.898       0.620    0.229      100%        14,087
      Claude 4 Sonnet
                           Debate (no anon, iso)         50       0.803    0.915       0.612    0.227      100%        14,654
                           Debate (anon+iso, split)      50       0.776    0.913       0.609    0.272      98%         14,299
                           Debate (anon, no iso)         50       0.836    0.946       0.628    0.188      100%        18,845
                           Single Agent                  20       0.796     —           —       0.366      85%a         4,043
      Gemini 3.1 Pro
                           Debate                        20       0.667     —           —       0.456      70%a        18,139
      a Gemini: failed tasks returned partial or empty outputs.




Table 20 MaTElDa full results: cell-level error detection (Claude 4 Sonnet, n=100). Token ratio: 6.3×.

              Condition           F1      Precision     Recall       SA Wins           Debate Wins          Avg Tok
              Single Agent      0.191       0.279        0.172             11                  —              4,539
              Debate            0.465       0.685        0.441             —                   80            28,558
              ∆ F1 = +0.273, 95% CI [0.217, 0.331], p<0.001, Cohen’s d=1.00


H     Bimodality Analysis
FC distributions are bimodal across all conditions (Hartigan’s dip test p<0.002; BIC favors a two-component
Gaussian mixture over a single Gaussian). Debate does not shift the distribution uniformly; instead, it
reshapes the mixture weights. For Claude, the upper mode (FC≈1.0) absorbs more mass under debate (56%
vs. 44%), while the lower mode both shifts downward and widens (µ: 0.77 → 0.67; σ: 0.10 → 0.24). Debate is
thus a variance amplifier: it improves the best outcomes while making the worst outcomes more severe.

Table 21 Bimodality test results for all conditions. All conditions are bimodal by both Hartigan’s dip test and BIC
model comparison.

                    Condition                 Dip     Dip p        ∆BIC         µ1       w1          µ2     w2
                    SA (debate exp.)         0.21     <0.001         380        0.77     0.56       1.00   0.44
                    Adv. Debate              0.27     <0.001         507        0.67     0.44       1.00   0.56
                    Debate (anon.)           0.24     <0.001         451        0.65     0.50       1.00   0.50
                    Debate (no anon.)        0.22     <0.001         370        0.66     0.58       1.00   0.42
                    Debate (iso.)            0.20     <0.001         374        0.61     0.58       1.00   0.42
                    Debate (no iso.)         0.21     <0.001         341        0.73     0.60       1.00   0.40
                    Gemini SA                0.23     <0.001          15        0.13     0.20       0.93   0.80
                    Gemini Debate            0.30     <0.001          —         0.00     0.30       0.95   0.70



I    Prompt Templates
Single Agent Prompt. The single-agent receives the raw table, cleaning purpose, and target schema, with
explicit instructions to only propose operations “grounded in the actual data.” Output is structured JSON


                                                              23
with step-by-step operations.

Generator Prompt. Similar to single-agent but emphasizes citing “specific rows/values” as evidence for each
operation.

Critic Prompt. The Critic is “incentivized to find errors” and instructed to: (1) check if each operation
addresses a real issue, (2) mentally apply the operation to verification data, (3) challenge edge cases, and (4)
find missed issues. Returns a verdict (accept/reject/revise) with evidence.

Anonymization. Role labels are replaced: “Data Cleaning Workflow Generator” → “Agent A”, “Data Quality
Critic” → “Agent B”, all instances of “Generator” → “Agent A”, “Critic” → “Agent B”.

Full Prompts. Verbatim prompt templates for all conditions (single-agent, 6 Critic variants, 3 Generator
variants, MaTElDa-specific and MMTU-specific prompts) are provided in the supplementary code package.


J     Self-Consistency Detailed Results
J.1    Per-Table Breakdown
A per-table analysis of self-consistency majority-vote F1, mean individual F1, and pairwise Jaccard diversity
across the 100 MaTElDa tables reveals the following. The aggregation lift (MV F1 minus mean individual F1)
is negative for 62 of 100 tables, indicating majority vote systematically degrades rather than improves the
detection signal.

J.2    Diversity Analysis
Mean pairwise Jaccard similarity across all 100 tables is 0.680 for SC-5 and 0.656 for SC-3, confirming that
temperature 0.7 produces diverse samples. Diversity is not the bottleneck: tables with high diversity (Jaccard
< 0.5) show no better aggregation lift than tables with low diversity (Jaccard > 0.8). The failure mode is
systematic: independent samples share the same blind spots: cells the model misses at temperature 0 it also
misses across temperature-0.7 samples.

J.3    Temperature Sensitivity
The pilot experiment (n=20) tested SC-5 at temperature 0.7 (F1=0.134), confirming the pattern holds at
smaller n. At temperature 0, we expect near-identical samples (SC≈SA), which we verify in the full run: SC-3
at temperature 0.7 achieves F1=0.178 (below SA=0.191), while the individual samples at temperature 0.7
average F1=0.178, identical to majority vote, confirming zero aggregation lift at k=3.


K     Research Visualizations
L     Debate Benefit Condition Derivation
The full derivation of the debate benefit condition (Equation 1) proceeds from a per-item expected quality
change analysis. For each output item i, we decompose the possible outcomes of one round of Critic feedback
into four cases (correct item correctly verified, correct item incorrectly challenged, incorrect item correctly
caught, incorrect item missed). The expected quality change is ∆Qi = α · [(1−pg ) · pc · pr − pg · (1−pc )] where
α is the Generator’s compliance rate. At the task level with k output items and inter-item dependence ρ:
∆Perf(T ) ≈ k · α · [rescue − damage] · (1 − ρβ), where β is the cascade severity (how many items one bad
critique corrupts). Assumptions: (i) items verified independently, (ii) pc constant across items, (iii) α scales
magnitude not sign, (iv) no cascading corrections between items.




                                                       24
                            Cohen’s d
                                          debate hurts                debateMaTElDa
                                                                             helps
                             1.0                                       Rep



                             0.8

                             0.6

                             0.4

                                                                          Ent. Match
                             0.2

                             0.0           AutoDCW                        Err. Detect
                                                                   Rescue < Damage
                                                                        Loc
                                              Schema               Marginal
                            -0.2          Imputation               Neutral (k=1)
                                                                   Rescue > Damage

                            -0.4      ρ = 0.85, p < 0.001
                                          Prof-S

                                                                                               PIV
                                   0.00                0.33        0.67                 1.00


Figure 5 PIV predicts debate’s treatment effect across ten task types. Each point is one task type; x-axis: PIV score,
y-axis: Cohen’s d. Dashed vertical line at PIV=0.50: all tasks to the right show non-negative d, all to the left show
non-positive d (10/10 sign accuracy). Dashed diagonal: linear trend (ρ = 0.85). Three high-PIV points with small d
reflect ceiling effects (SA precision ≥ 0.82).


M      PIV Component Scoring Details
M.1      Component Scoring Rubric
Each of the three PIV components (M , S, C) is scored as a binary (0 or 1) based on the task specification:
    • M (Multi-output): Score 1 if the task requires producing multiple independent output elements (e.g.,
      a set of error cells, a list of entity matches, a multi-step workflow). Score 0 if the output is a single
      holistic answer (e.g., one imputed value, one profile summary).
    • S (Source-checkable): Score 1 if each output element can be verified by looking up specific cells in the
      source table; that is, the verification requires only cell-level inspection, not domain knowledge or external
      information. Score 0 if verification requires semantic judgment (e.g., “is this the correct imputed value?”,
      “is this profile accurate?”).
    • C (Constrained answer space): Score 1 if the valid response set for each element is small or finite: binary
      (error/not-error), categorical, or a fixed enumeration. Score 0 if the answer space is open-ended (e.g.,
      any string value, any cleaning operation).

M.2      Anti-Circularity Guarantee
All three components are determined by the task’s structural definition, not by any debate outcome. A
practitioner can score M , S, and C for a new, unseen task from the task specification alone, before running
any experiments. The PIV score does not reference debate performance, effect sizes, or any experimental
results.

M.3      Sensitivity to Threshold Choice
At the recommended threshold PIV ≥ 0.50, sign-prediction accuracy is 100% (9/9 non-zero-d tasks correctly
classified). The threshold is robust: any value in the range [0.34, 0.66] achieves the same 100% accuracy,
because no task type in our study has PIV between 0.34 and 0.66; the scores cluster at {0.00, 0.33, 0.67, 1.00}
with a natural gap at 0.50.




                                                              25
                                          AutoDCW (generation)                                 MaTElDa (detection)
                                             ***
                              1.0                                   ***


                              0.8

                              0.6




                  Cohen’s d
                              0.4
                                                                                                   *                  *

                              0.2

                              0.0

                              -0.2

                              -0.4

                                          Claude                Gemini                         Qwen3           DeepSeek


Figure 6 Sign reversal is consistent across all four models. Cohen’s d for generation (red) and detection (green). Every
model: debate hurts generation (d < 0) and helps detection (d > 0). Detection separates into two tiers: Claude/Gemini
(d ≈ 1.0, ***p < 0.001) and Qwen3/DeepSeek (d ≈ 0.3, *p < 0.05).

                                      Claude 4 Sonnet — AutoDCWorkflow (paired, n=84)



                                                                                 SA baseline
                    SA                                                                         0.813
                                                                                                                             CIC: −7.0pp

               D-Text                               0.743


              D-Code                                                                           0.813

                                                                                                                             +5.5pp∗
          D-Code+G2                                                                                                  0.868



                               0.70                0.75                   0.80                          0.85
                                                             Factual Consistency (FC)
                                                            ∗ p<0.05, paired bootstrap, n=84



Figure 7 From CIC to cure. Paired comparison (n=84 tasks). SA: baseline (FC=0.813). D-Text: CIC drops FC by
−7.0pp. D-Code: code-execution grounding recovers to SA level (dz =0.02). D-Code+G2: evidence-gated generation
exceeds SA by +5.5pp (p<0.05). Dashed line: SA baseline.


M.4      Concordance Analysis
Pairwise concordance (the fraction of task pairs for which the higher-PIV task also has the higher Cohen’s d) is
95.6% (43 of 45 pairs). The 2 discordant pairs both involve Rep (PIV=0.67, d= + 0.93) exceeding MMTU-ED
(PIV=1.00, d= + 0.05) and MMTU-EM (PIV=1.00, d= + 0.20) in treatment effect despite lower PIV. This is
explained by the precision-headroom interaction: MMTU tasks have high SA baselines (≥ 0.82), leaving little
room for the Critic to improve. PIV predicts direction; precision headroom modulates magnitude.

M.5      Cross-Model Cardinality Replication
Qwen3 235B replicates the same 2×2 pattern across all four experiments: Loc is neutral (SA=0.660,
Debate=0.642, ∆= − 0.018), Rep benefits from debate (SA F1=0.136, Debate F1=0.238, ∆= + 0.102),
Prof-S is harmed (SA=0.790, Debate=0.720, ∆= − 0.070), and Prof-M is neutral (SA F1=0.465, Debate
F1=0.457, ∆= − 0.008). The qualitative pattern, that only Rep (multi-output with per-item verifiability)
benefits, holds identically across both models, strengthening the generalizability of the per-item verifiability
framework.




                                                                          26
                                           Critique-Induced Confusion (CIC)


                           Generator         workflow        Critic raises    feedback   Generator agrees
                         proposes k ops                    23.5 items/task                 with 95.3%




                                             48.1% grounded                  51.9% hallucinated
                                              (correct ops)                   (fabricated ops)



                                             Result: FC drops −7.0pp (0.813 → 0.743). CIC
                                             is worse on easy tasks (SA≥0.95: ∆= − 6.3pp),
                                            beneficial on hard tasks (SA<0.60: ∆= + 3.2pp).


Figure 8 CIC mechanism. The Critic raises 23.5 items per task; the Generator agrees with 95.3%. Of debate-added
operations, 51.9% are hallucinated—approximately coin-flip quality. CIC is task-difficulty-dependent: it harms easy
tasks but helps hard tasks.


N     Dataset Statistics

Table 22 Benchmark dataset statistics. All tables fit within LLM context windows. MaTElDa tables are capped at
100 rows for main experiments; 15 tables with ≥10K original rows are used for scale validation.

      Benchmark              Total Tasks          Used     Median Rows       Row Range       Median Cols     Evaluation
      AutoDCWorkflow             142              50–100         15              5–50             8         FC, Cell Acc
      MMTU                      28,136              200          26             2–385             6         F1, EM, Acc
      MaTElDa                   1,173               100          62             5–100             9           P/R/F1
      MaTElDa (10K)               15                15         10,000           10,000            9           P/R/F1



Table 23 Model configurations for all experiments.

       Model               Temp.     Max Tok.              Benchmarks           Conditions
       Claude 4 Sonnet       0.0          8,192             All 3               All main experiments
       Gemini 3.1 Pro        0.0          8,192       AutoDCW, MaTElDa          Debate, MaTElDa
       Qwen3 235B            0.0          8,192             All 3               Debate, cardinality, prompt sensitivity,
                                                                                MaTElDa, MMTU
       DeepSeek R1           0.0          8,192                All 3            Debate, MaTElDa, MMTU




                                                                 27
